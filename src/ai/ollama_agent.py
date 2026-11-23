"""
Ollama Agent
Talks to a local Ollama model, decides which shell commands to run,
streams the response, and executes approved commands automatically.
"""

import json
import subprocess
import os
import requests
from typing import Generator, List, Dict, Optional


OLLAMA_URL   = "http://localhost:11434"
DEFAULT_MODEL = "llama3.1:8b"

SYSTEM_PROMPT = """You are NeuroShell AI — an expert DevOps and shell assistant running INSIDE the user's terminal.

You have the ability to run shell commands directly on the user's machine (or whatever server they are SSH'd into).

RULES:
1. When you need to run a command, output it in this EXACT format on its own line:
   RUN: <command>
2. After seeing the output, you can run more commands or give a final answer.
3. Be concise. No fluff. Just do the task.
4. For destructive commands (rm -rf, DROP TABLE, etc.) always ask first with CONFIRM: <reason>
5. If the user is SSH'd into a remote server, all RUN: commands run on THAT server.
6. Always explain briefly what you found after running commands.

You can chain multiple RUN: commands to investigate step by step.
"""


class OllamaAgent:
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model      = model
        self.messages:  List[Dict] = []
        self.context_info: Dict    = {}

    def set_context(self, cwd: str, recent_commands: List[str], ssh_host: Optional[str] = None):
        """Give the agent awareness of the current shell state."""
        self.context_info = {
            "cwd":             cwd,
            "recent_commands": recent_commands[-10:],
            "ssh_host":        ssh_host,
            "hostname":        subprocess.getoutput("hostname"),
            "user":            os.environ.get("USER", "unknown"),
        }

    def _build_context_block(self) -> str:
        c = self.context_info
        lines = [
            f"Current directory : {c.get('cwd', os.getcwd())}",
            f"User              : {c.get('user')}",
            f"Hostname          : {c.get('hostname')}",
        ]
        if c.get("ssh_host"):
            lines.append(f"SSH target        : {c['ssh_host']}")
        if c.get("recent_commands"):
            lines.append("Recent commands   :")
            for cmd in c["recent_commands"]:
                lines.append(f"  $ {cmd}")
        return "\n".join(lines)

    def _stream_ollama(self, messages: List[Dict]) -> Generator[str, None, None]:
        """Stream tokens from Ollama API."""
        payload = {
            "model":    self.model,
            "messages": messages,
            "stream":   True,
        }
        try:
            with requests.post(f"{OLLAMA_URL}/api/chat",
                               json=payload, stream=True, timeout=120) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        token = chunk.get("message", {}).get("content", "")
                        if token:
                            yield token
                        if chunk.get("done"):
                            break
        except requests.ConnectionError:
            yield "\n❌ Ollama not reachable. Is it running? (ollama serve)\n"
        except Exception as e:
            yield f"\n❌ Error: {e}\n"

    def run_command_on_shell(self, command: str, ssh_host: Optional[str] = None) -> str:
        """Actually execute a command and return its output."""
        if ssh_host:
            full_cmd = f"ssh {ssh_host} '{command}'"
        else:
            full_cmd = command
        try:
            result = subprocess.run(
                full_cmd, shell=True, capture_output=True,
                text=True, timeout=30, cwd=self.context_info.get("cwd", os.getcwd())
            )
            out = result.stdout.strip()
            err = result.stderr.strip()
            combined = out
            if err:
                combined += f"\n[stderr]: {err}" if out else err
            return combined or "(no output)"
        except subprocess.TimeoutExpired:
            return "⏱ Command timed out after 30s"
        except Exception as e:
            return f"Error running command: {e}"

    def chat(self, user_message: str, executor_callback=None) -> Generator[str, None, None]:
        """
        Send a message, stream the AI response, auto-run any RUN: commands,
        feed output back to the AI, and continue until done.
        executor_callback: optional fn(cmd) -> str override for execution
        """
        # Build system message with live context
        system_with_context = SYSTEM_PROMPT + "\n\n--- CURRENT SHELL CONTEXT ---\n" + self._build_context_block()

        if not self.messages:
            self.messages.append({"role": "system", "content": system_with_context})
        else:
            # Update context in system message each turn
            self.messages[0] = {"role": "system", "content": system_with_context}

        self.messages.append({"role": "user", "content": user_message})

        ssh_host = self.context_info.get("ssh_host")

        # Agentic loop — keep going until AI stops issuing RUN: commands
        for _ in range(10):   # max 10 command rounds per prompt
            full_response  = ""
            pending_buffer = ""

            # Stream tokens
            for token in self._stream_ollama(self.messages):
                full_response  += token
                pending_buffer += token
                yield token

            self.messages.append({"role": "assistant", "content": full_response})

            # Parse out any RUN: or CONFIRM: directives
            commands_to_run = []
            confirm_needed  = None

            for line in full_response.splitlines():
                stripped = line.strip()
                if stripped.startswith("RUN:"):
                    cmd = stripped[4:].strip()
                    if cmd:
                        commands_to_run.append(cmd)
                elif stripped.startswith("CONFIRM:"):
                    confirm_needed = stripped[8:].strip()

            if confirm_needed:
                yield f"\n\n⚠️  CONFIRM needed: {confirm_needed}\n"
                break

            if not commands_to_run:
                break   # AI is done — pure text response, no more commands

            # Execute each command and feed output back
            for cmd in commands_to_run:
                yield f"\n\n```\n$ {cmd}\n"
                if executor_callback:
                    output = executor_callback(cmd)
                else:
                    output = self.run_command_on_shell(cmd, ssh_host)
                yield output
                yield "\n```\n"

                # Feed command output back to AI so it can continue reasoning
                self.messages.append({
                    "role":    "user",
                    "content": f"Command output:\n```\n{output}\n```"
                })

    def reset(self):
        """Clear conversation history."""
        self.messages = []

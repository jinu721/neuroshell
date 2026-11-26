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

    def set_model(self, model: str) -> None:
        """Switch the Ollama model used for future requests."""
        self.model = model

    def get_model(self) -> str:
        """Return the currently configured Ollama model name."""
        return self.model

    def message_count(self) -> int:
        """Return number of messages in the current conversation history."""
        return len(self.messages)

    def trim_history(self, keep_last: int = 20) -> None:
        """Keep only the system prompt plus the last N messages to save context."""
        if len(self.messages) <= keep_last + 1:
            return
        system = self.messages[:1]
        recent = self.messages[-(keep_last):]
        self.messages = system + recent

    def inject_system_note(self, note: str) -> None:
        """Append a system-level note to the conversation without user attribution."""
        self.messages.append({"role": "system", "content": note})

    def export_chat(self, path: str) -> None:
        """Save the full conversation history as a JSON file."""
        import json, pathlib
        pathlib.Path(path).write_text(
            json.dumps(self.messages, indent=2, ensure_ascii=False)
        )

    def load_chat(self, path: str) -> bool:
        """Restore conversation history from a JSON file. Returns False if missing."""
        import json, pathlib
        p = pathlib.Path(path)
        if not p.exists():
            return False
        self.messages = json.loads(p.read_text())
        return True

    def available_models(self) -> list:
        """Query Ollama for the list of locally pulled models."""
        try:
            r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
            r.raise_for_status()
            return [m["name"] for m in r.json().get("models", [])]
        except Exception:
            return []

    def is_ollama_running(self) -> bool:
        """Return True if the Ollama server is reachable on localhost."""
        try:
            requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
            return True
        except Exception:
            return False

    def get_last_user_message(self) -> str:
        """Return the most recent user message text, or empty string."""
        for msg in reversed(self.messages):
            if msg.get("role") == "user":
                return msg.get("content", "")
        return ""

    def get_last_assistant_message(self) -> str:
        """Return the most recent assistant response text, or empty string."""
        for msg in reversed(self.messages):
            if msg.get("role") == "assistant":
                return msg.get("content", "")
        return ""

    def conversation_tokens_estimate(self) -> int:
        """Estimate total token count in conversation history (4 chars per token)."""
        total_chars = sum(len(m.get("content", "")) for m in self.messages)
        return total_chars // 4

    def add_user_message(self, text: str) -> None:
        """Append a user message directly to history without sending it."""
        self.messages.append({"role": "user", "content": text})

    def add_assistant_message(self, text: str) -> None:
        """Inject an assistant message directly into the conversation history."""
        self.messages.append({"role": "assistant", "content": text})

    def set_system_prompt(self, prompt: str) -> None:
        """Replace the system prompt. Clears all previous conversation history."""
        self.messages = [{"role": "system", "content": prompt}]

    def get_system_prompt(self) -> str:
        """Return the current system prompt text."""
        if self.messages and self.messages[0].get("role") == "system":
            return self.messages[0].get("content", "")
        return ""

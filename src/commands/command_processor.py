"""
Command Processor
Executes shell commands and handles built-in NeuroShell commands.
"""

import subprocess
import os
import shutil
from typing import Dict, Any, List, Optional


BUILTIN_HELP = {
    "help":       "Show this help",
    "exit":       "Exit NeuroShell",
    "quit":       "Exit NeuroShell",
    "clear":      "Clear the screen",
    "history":    "Show command history",
    "top":        "Show your most-used commands",
    "stats":      "Show session stats",
    "cd <dir>":   "Change directory",
}


class CommandProcessor:
    def __init__(self):
        self.execution_count = 0
        self._session_history: List[str] = []
        self._aliases: Dict[str, str] = {}
        self._last_result: Dict[str, Any] = {}
        self.DEFAULT_TIMEOUT = 30

    # ── Built-in commands ────────────────────────────────────────────────────

    def is_builtin(self, command: str) -> bool:
        base = command.strip().split()[0] if command.strip() else ""
        return base in ("help", "exit", "quit", "clear", "history", "top",
                        "stats", "cd", "alias", "unalias")

    def handle_builtin(self, command: str, neural_engine=None) -> Dict[str, Any]:
        parts = command.strip().split(None, 1)
        cmd   = parts[0].lower()
        arg   = parts[1] if len(parts) > 1 else ""

        if cmd in ("exit", "quit"):
            return {"success": True, "output": "EXIT", "builtin": True}

        if cmd == "clear":
            os.system("clear")
            return {"success": True, "output": "", "builtin": True}

        if cmd == "help":
            lines = ["\n🧠 NeuroShell — Built-in Commands\n"]
            for k, v in BUILTIN_HELP.items():
                lines.append(f"  {k:<18} {v}")
            lines.append("\nAll other commands run in your shell as normal.\n")
            return {"success": True, "output": "\n".join(lines), "builtin": True}

        if cmd == "history":
            if not self._session_history:
                return {"success": True, "output": "No history yet.", "builtin": True}
            lines = [f"  {i+1:3d}  {c}" for i, c in enumerate(self._session_history)]
            return {"success": True, "output": "\n".join(lines), "builtin": True}

        if cmd == "top":
            if neural_engine:
                top = neural_engine.top_commands(15)
                lines = ["\n  Most-used commands:"] + [f"  {c}" for c in top]
                return {"success": True, "output": "\n".join(lines), "builtin": True}
            return {"success": True, "output": "Neural engine not loaded.", "builtin": True}

        if cmd == "stats":
            lines = [
                f"\n  Session commands : {self.execution_count}",
                f"  Success rate     : {neural_engine.success_rate:.0%}" if neural_engine else "",
                f"  Known commands   : {len(neural_engine._unigrams)}" if neural_engine else "",
            ]
            return {"success": True, "output": "\n".join(l for l in lines if l), "builtin": True}

        if cmd == "cd":
            target = os.path.expanduser(arg) if arg else str(os.path.expanduser("~"))
            try:
                os.chdir(target)
                return {"success": True, "output": "", "builtin": True}
            except FileNotFoundError:
                return {"success": False, "output": "", "error": f"cd: {target}: No such directory", "builtin": True}

        if cmd == "alias":
            if "=" in arg:
                name, _, val = arg.partition("=")
                self._aliases[name.strip()] = val.strip().strip("'\"")
                return {"success": True, "output": f"alias {name.strip()} set.", "builtin": True}
            # list aliases
            if self._aliases:
                lines = [f"  {k}='{v}'" for k, v in self._aliases.items()]
                return {"success": True, "output": "\n".join(lines), "builtin": True}
            return {"success": True, "output": "No aliases set.", "builtin": True}

        if cmd == "unalias":
            if arg in self._aliases:
                del self._aliases[arg]
                return {"success": True, "output": f"alias {arg} removed.", "builtin": True}
            return {"success": False, "output": "", "error": f"unalias: {arg}: not found", "builtin": True}

        return {"success": False, "output": "", "error": f"Unknown builtin: {cmd}", "builtin": True}

    # ── Shell execution ──────────────────────────────────────────────────────

    def execute(self, command: str, prediction: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a shell command and return structured result."""
        self.execution_count += 1
        cmd = self._resolve_alias(command.strip())

        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.DEFAULT_TIMEOUT,
                env=os.environ.copy(),
                cwd=os.getcwd(),
            )
            self._last_result = {
                "success": result.returncode == 0,
                "output":  result.stdout,
                "error":   result.stderr,
            }
            return self._last_result

        except subprocess.TimeoutExpired:
            return {"success": False, "output": "", "error": f"⏱ Command timed out after {self.DEFAULT_TIMEOUT}s"}
        except Exception as e:
            return {"success": False, "output": "", "error": str(e)}

    def _resolve_alias(self, command: str) -> str:
        base = command.split()[0]
        if base in self._aliases:
            rest = command[len(base):]
            return self._aliases[base] + rest
        return command

    def last_exit_code(self) -> int:
        return 0 if self._last_result.get("success") else 1

    def add_to_history(self, command: str):
        self._session_history.append(command)


    def execute_pipeline(self, commands: list) -> list:
        """Run multiple commands in sequence, stopping on first failure."""
        results = []
        for cmd in commands:
            r = self.execute(cmd)
            results.append(r)
            if not r.get("success"):
                break
        return results

    def execute_with_timeout(self, command: str, timeout: int = 30) -> dict:
        """Execute command with a custom timeout instead of the default."""
        import subprocess, os
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True,
                text=True, timeout=timeout, env=os.environ.copy(), cwd=os.getcwd()
            )
            return {"success": result.returncode == 0,
                    "output": result.stdout, "error": result.stderr}
        except subprocess.TimeoutExpired:
            return {"success": False, "output": "", "error": f"timed out after {timeout}s"}
        except Exception as e:
            return {"success": False, "output": "", "error": str(e)}

"""
Terminal Interface
Left panel: real interactive shell with AI autocomplete
Right panel: Ollama AI chat that can read context and run commands
"""

import os
import sys
import threading
import textwrap
from typing import Optional, List

from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML, ANSI
from prompt_toolkit.key_binding import KeyBindings
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich.rule import Rule
from rich.live import Live
from rich.markdown import Markdown
from rich import box

console = Console()
err_console = Console(stderr=True)

# ── ANSI helpers ──────────────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BLUE   = "\033[94m"
MAGENTA= "\033[95m"

def clr(color, text): return f"{color}{text}{RESET}"

# ── Neural Completer ──────────────────────────────────────────────────────────
class NeuralCompleter(Completer):
    def __init__(self, neural_engine):
        self.engine = neural_engine

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        if not text.strip():
            return
        try:
            result = self.engine.predict_intent(text)
            for s in result.get("suggestions", []):
                if s != text:
                    if s.startswith(text):
                        yield Completion(s[len(text):], start_position=0, display=s)
                    else:
                        yield Completion(s, start_position=-len(text), display=s)
        except Exception:
            pass

SHELL_STYLE = Style.from_dict({
    "prompt":       "#00ff87 bold",
    "prompt.path":  "#666666",
    "completion-menu.completion":         "bg:#1a1a1a #aaaaaa",
    "completion-menu.completion.current": "bg:#00ff87 #000000 bold",
    "auto-suggestion":                    "#444444 italic",
})

# ── Chat Panel ────────────────────────────────────────────────────────────────
class ChatPanel:
    """Right-side AI chat panel rendered in the terminal."""

    def __init__(self, agent):
        self.agent          = agent
        self.history: List  = []   # list of (role, content)
        self._ssh_host: Optional[str] = None

    def set_ssh(self, host: Optional[str]):
        self._ssh_host = host
        self.agent.context_info["ssh_host"] = host

    def _divider(self, label: str = ""):
        width = min(console.width, 80)
        if label:
            pad = (width - len(label) - 2) // 2
            print(clr(DIM, "─" * pad) + clr(CYAN + BOLD, f" {label} ") + clr(DIM, "─" * pad))
        else:
            print(clr(DIM, "─" * width))

    def _header(self):
        model = self.agent.model
        ssh   = f"  {clr(YELLOW, '⟶ SSH: ' + self._ssh_host)}" if self._ssh_host else ""
        print()
        print(clr(MAGENTA + BOLD, "╭─ 🤖 NeuroShell AI") + clr(DIM, f"  model: {model}") + ssh)
        print(clr(MAGENTA, "│"))

    def render_user(self, msg: str):
        print(clr(MAGENTA, "│ ") + clr(CYAN + BOLD, "You: ") + msg)
        print(clr(MAGENTA, "│"))

    def render_ai_streaming(self, user_message: str):
        """Stream AI response with live token output + command execution display."""
        from src.commands.command_processor import CommandProcessor

        self._header()
        self.render_user(user_message)
        print(clr(MAGENTA, "│ ") + clr(GREEN + BOLD, "AI:  "), end="", flush=True)

        full_text        = ""
        in_code_block    = False
        line_buf         = ""

        def stream_print(token: str):
            nonlocal full_text, in_code_block, line_buf
            full_text += token
            line_buf  += token
            # Pretty-print code blocks differently
            if "```" in line_buf:
                parts = line_buf.split("```")
                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        print(clr(RESET, part), end="", flush=True)
                    else:
                        in_code_block = not in_code_block
                        if in_code_block:
                            print(clr(YELLOW, "\n│ ┌─ command ─────────────────"), flush=True)
                        else:
                            print(clr(YELLOW, "\n│ └───────────────────────────"), flush=True)
                line_buf = ""
            else:
                # Flush on newlines
                if "\n" in line_buf:
                    lines = line_buf.split("\n")
                    for ln in lines[:-1]:
                        if ln.startswith("$ ") or ln.startswith("RUN:"):
                            print(clr(YELLOW + BOLD, f"\n│   $ {ln.replace('RUN:','').strip()}"), flush=True)
                        elif ln.startswith("[stderr]"):
                            print(clr(RED, f"\n│   {ln}"), flush=True)
                        elif ln.strip():
                            print(f"\n│   {ln}", end="", flush=True)
                    line_buf = lines[-1]

        # Run the agent and stream output
        try:
            for chunk in self.agent.chat(user_message):
                stream_print(chunk)
        except Exception as e:
            print(clr(RED, f"\n│   ❌ Agent error: {e}"))

        # Flush remaining buffer
        if line_buf.strip():
            print(f"\n│   {line_buf}", flush=True)

        print(clr(MAGENTA, "\n╰" + "─" * (min(console.width, 80) - 1)))
        print()

        self.history.append(("user", user_message))
        self.history.append(("ai",   full_text))


# ── Main Terminal Interface ───────────────────────────────────────────────────
class TerminalInterface:
    def __init__(self, neural_engine=None, command_processor=None):
        self.neural_engine     = neural_engine
        self.command_processor = command_processor
        self.running           = True
        self._history_file     = os.path.expanduser("~/.neuroshell_prompt_history")
        self._recent_commands: List[str] = []
        self._ssh_host: Optional[str]    = None

        # Set up AI agent
        from src.ai.ollama_agent import OllamaAgent
        self.agent      = OllamaAgent(model="llama3.1:8b")
        self.chat_panel = ChatPanel(self.agent)

    def _build_prompt(self) -> HTML:
        cwd  = os.getcwd().replace(os.path.expanduser("~"), "~")
        ssh  = f" <ssh>[{self._ssh_host}]</ssh>" if self._ssh_host else ""
        return HTML(f'<prompt>🧠 neuroshell</prompt>'
                    f'<path> {cwd}</path>'
                    f'{ssh}'
                    f'<prompt> ❯ </prompt>')

    def _prompt_style(self):
        return Style.from_dict({
            "prompt": "#00ff87 bold",
            "path":   "#666666",
            "ssh":    "#ffaa00 bold",
            "completion-menu.completion":         "bg:#1a1a1a #aaaaaa",
            "completion-menu.completion.current": "bg:#00ff87 #000000 bold",
            "auto-suggestion":                    "#444444 italic",
        })

    def print_banner(self):
        print(clr(GREEN + BOLD, r"""
  _   _                      ____  _          _ _
 | \ | | ___ _   _ _ __ ___ / ___|| |__   ___| | |
 |  \| |/ _ \ | | | '__/ _ \___ \| '_ \ / _ \ | |
 | |\  |  __/ |_| | | | (_) |__) | | | |  __/ | |
 |_| \_|\___|\__,_|_|  \___/____/|_| |_|\___|_|_|
"""))
        print(clr(DIM, "  AI-powered terminal  ·  ") +
              clr(CYAN, "type 'help' for commands") +
              clr(DIM, "  ·  ") +
              clr(YELLOW, "prefix with '@' to chat with AI"))
        print(clr(DIM, "  Example: ") + clr(CYAN, "@ check why nginx is failing") +
              clr(DIM, "  or  ") + clr(CYAN, "@ show me errors in /var/log/syslog"))
        print()

    def start_interactive_mode(self):
        self.print_banner()

        completer = NeuralCompleter(self.neural_engine) if self.neural_engine else None
        session   = PromptSession(
            history               = FileHistory(self._history_file),
            completer             = completer,
            auto_suggest          = AutoSuggestFromHistory(),
            style                 = self._prompt_style(),
            complete_while_typing = True,
        )

        while self.running:
            # Keep agent context fresh
            self.agent.set_context(
                cwd             = os.getcwd(),
                recent_commands = self._recent_commands,
                ssh_host        = self._ssh_host,
            )

            try:
                raw     = session.prompt(self._build_prompt)
                command = raw.strip()
                if not command:
                    continue

                # ── AI chat mode — prefix with @ ──────────────────────────
                if command.startswith("@"):
                    user_msg = command[1:].strip()
                    if not user_msg:
                        print(clr(DIM, "  Usage: @ <your question or task>"))
                        continue
                    self.chat_panel.render_ai_streaming(user_msg)
                    continue

                # ── Special AI commands ───────────────────────────────────
                if command.startswith("ssh "):
                    # Track SSH host so AI knows it
                    parts = command.split()
                    if len(parts) >= 2:
                        self._ssh_host = parts[-1]
                        self.chat_panel.set_ssh(self._ssh_host)
                        print(clr(YELLOW, f"  🔗 SSH context set to: {self._ssh_host}"))

                if command in ("ai reset", "@reset"):
                    self.agent.reset()
                    print(clr(DIM, "  🧠 AI conversation cleared."))
                    continue

                # ── Built-in shell commands ───────────────────────────────
                if self.command_processor.is_builtin(command):
                    result = self.command_processor.handle_builtin(
                        command, self.neural_engine)
                    if result.get("output") == "EXIT":
                        print(clr(GREEN, "\nGoodbye! 🧠\n"))
                        self.running = False
                        return
                    if result.get("output"):
                        print(result["output"])
                    if result.get("error"):
                        print(clr(RED, result["error"]))
                    if self.neural_engine:
                        self.neural_engine.learn_from_usage(command, result["success"])
                    self._recent_commands.append(command)
                    continue

                # ── Normal shell command ──────────────────────────────────
                result = self.command_processor.execute(command)
                if result.get("output"):
                    print(result["output"], end="")
                if result.get("error"):
                    print(clr(RED, result["error"].rstrip()))
                if self.neural_engine:
                    self.neural_engine.learn_from_usage(command, result["success"])
                self._recent_commands.append(command)
                self.command_processor.add_to_history(command)

            except KeyboardInterrupt:
                print(clr(DIM, "\n  (Ctrl+C — type exit to quit)"))
            except EOFError:
                print(clr(GREEN, "\nGoodbye! 🧠\n"))
                break

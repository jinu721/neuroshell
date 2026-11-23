"""
Terminal Interface
Real interactive shell using prompt-toolkit with live AI autocomplete.
"""

import os
from typing import Optional, List

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings
from rich.console import Console
from rich.text import Text


console = Console()


# ── Neural Completer ─────────────────────────────────────────────────────────

class NeuralCompleter(Completer):
    """Feeds prompt-toolkit completions from the NeuralPredictionEngine."""

    def __init__(self, neural_engine):
        self.engine = neural_engine

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        if not text.strip():
            return
        try:
            result = self.engine.predict_intent(text)
            for suggestion in result.get("suggestions", []):
                if suggestion != text:
                    # Only show the part after what's already typed if it's a prefix
                    if suggestion.startswith(text):
                        yield Completion(suggestion[len(text):], start_position=0,
                                         display=suggestion)
                    else:
                        yield Completion(suggestion, start_position=-len(text),
                                         display=suggestion)
        except Exception:
            pass


# ── Styles ───────────────────────────────────────────────────────────────────

SHELL_STYLE = Style.from_dict({
    "prompt":       "#00ff87 bold",
    "prompt.path":  "#888888",
    "completion-menu.completion":         "bg:#1e1e1e #aaaaaa",
    "completion-menu.completion.current": "bg:#00ff87 #000000 bold",
    "auto-suggestion":                    "#555555 italic",
})


# ── Terminal Interface ───────────────────────────────────────────────────────

class TerminalInterface:
    def __init__(self, neural_engine=None, command_processor=None):
        self.neural_engine     = neural_engine
        self.command_processor = command_processor
        self.running           = True
        self._history_file     = os.path.expanduser("~/.neuroshell_prompt_history")

    def _build_prompt(self) -> HTML:
        cwd  = os.getcwd()
        home = os.path.expanduser("~")
        display_cwd = cwd.replace(home, "~")
        return HTML(f'<prompt>🧠 neuroshell</prompt> '
                    f'<prompt.path>{display_cwd}</prompt.path> '
                    f'<prompt>❯</prompt> ')

    def print_banner(self):
        console.print("""
[bold green]
  _   _                      ____  _          _ _
 | \\ | | ___ _   _ _ __ ___ / ___|| |__   ___| | |
 |  \\| |/ _ \\ | | | '__/ _ \\___ \\| '_ \\ / _ \\ | |
 | |\\  |  __/ |_| | | | (_) |__) | | | |  __/ | |
 |_| \\_|\\___|\\__,_|_|  \\___/____/|_| |_|\\___|_|_|
[/bold green]
[dim]  AI-powered terminal  •  type [bold]help[/bold] to get started[/dim]
""")

    def start_interactive_mode(self):
        self.print_banner()

        completer   = NeuralCompleter(self.neural_engine) if self.neural_engine else None
        session     = PromptSession(
            history        = FileHistory(self._history_file),
            completer      = completer,
            auto_suggest   = AutoSuggestFromHistory(),
            style          = SHELL_STYLE,
            complete_while_typing = True,
            mouse_support  = False,
        )

        while self.running:
            try:
                raw = session.prompt(self._build_prompt)
                command = raw.strip()

                if not command:
                    continue

                self._run_command(command)

            except KeyboardInterrupt:
                console.print("\n[dim]  (Ctrl+C — type exit to quit)[/dim]")
            except EOFError:
                console.print("\n[bold green]Goodbye! 🧠[/bold green]")
                break

    def _run_command(self, command: str):
        """Route command to builtin handler or shell executor."""
        from src.commands.command_processor import CommandProcessor

        proc = self.command_processor

        # Add to session history
        proc.add_to_history(command)

        # Check builtins first
        if proc.is_builtin(command):
            result = proc.handle_builtin(command, self.neural_engine)
            if result.get("output") == "EXIT":
                console.print("[bold green]Goodbye! 🧠[/bold green]")
                self.running = False
                return
            if result.get("output"):
                console.print(result["output"])
            if result.get("error"):
                console.print(f"[red]{result['error']}[/red]")
            # Learn even from builtins
            if self.neural_engine:
                self.neural_engine.learn_from_usage(command, result["success"])
            return

        # Execute as shell command
        result = proc.execute(command)

        if result.get("output"):
            print(result["output"], end="")
        if result.get("error"):
            console.print(f"[red]{result['error'].rstrip()}[/red]")

        # Teach the engine
        if self.neural_engine:
            self.neural_engine.learn_from_usage(command, result["success"])

"""
NeuroShell TUI
Left  (65%) -- real shell with prompt, history nav, tab complete
Right (35%) -- AI chat panel, full history, input at bottom
No emoji. Clean minimal text UI.
"""

import os, sys, subprocess, threading
from pathlib import Path
from typing import List

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Input, RichLog, Static
from rich.text import Text
from rich.markup import escape


# -----------------------------------------------------------------------------
# Shell executor
# -----------------------------------------------------------------------------
class ShellExecutor:
    def __init__(self):
        self.cwd     = os.path.expanduser("~")
        self.env     = os.environ.copy()
        self.history: List[str] = []

    def short_cwd(self) -> str:
        return self.cwd.replace(os.path.expanduser("~"), "~")

    def run(self, cmd: str):
        """Returns (stdout, stderr, success)."""
        cmd = cmd.strip()
        if not cmd:
            return "", "", True

        if cmd.startswith("cd"):
            parts  = cmd.split(None, 1)
            target = os.path.expanduser(parts[1].strip()) if len(parts) > 1 \
                     else os.path.expanduser("~")
            if not os.path.isabs(target):
                target = os.path.join(self.cwd, target)
            target = os.path.normpath(target)
            if os.path.isdir(target):
                self.cwd = target
                return "", "", True
            return "", f"cd: {target}: No such file or directory", False

        self.history.append(cmd)
        try:
            r = subprocess.run(
                cmd, shell=True, capture_output=True,
                text=True, timeout=30, cwd=self.cwd, env=self.env
            )
            return r.stdout, r.stderr, r.returncode == 0
        except subprocess.TimeoutExpired:
            return "", "timed out after 30s", False
        except Exception as e:
            return "", str(e), False


# -----------------------------------------------------------------------------
# Shell input  --  up/down history  +  tab path-complete
# -----------------------------------------------------------------------------
class ShellInput(Input):
    DEFAULT_CSS = """
    ShellInput {
        height: 1;
        border: none;
        background: #0d0d0d;
        color: #00ff87;
        padding: 0 0;
    }
    ShellInput:focus { border: none; }
    """

    def __init__(self, shell: ShellExecutor, **kwargs):
        super().__init__(**kwargs)
        self.shell     = shell
        self._hist_idx = -1
        self._saved    = ""

    def on_key(self, event) -> None:
        if event.key == "up":
            event.stop()
            hist = self.shell.history
            if not hist:
                return
            if self._hist_idx == -1:
                self._saved    = self.value
                self._hist_idx = len(hist) - 1
            elif self._hist_idx > 0:
                self._hist_idx -= 1
            self.value           = hist[self._hist_idx]
            self.cursor_position = len(self.value)

        elif event.key == "down":
            event.stop()
            hist = self.shell.history
            if self._hist_idx == -1:
                return
            self._hist_idx += 1
            if self._hist_idx >= len(hist):
                self._hist_idx = -1
                self.value     = self._saved
            else:
                self.value = hist[self._hist_idx]
            self.cursor_position = len(self.value)

        elif event.key == "tab":
            event.stop()
            self._tab_complete()

        else:
            self._hist_idx = -1

    def _tab_complete(self):
        typed  = self.value
        if not typed:
            return
        parts  = typed.split()
        prefix = parts[-1] if parts else ""
        base   = os.path.expanduser(
                     os.path.join(self.shell.cwd, os.path.dirname(prefix)))
        stem   = os.path.basename(prefix)
        try:
            matches = sorted(p for p in os.listdir(base) if p.startswith(stem))
        except Exception:
            matches = []
        if len(matches) == 1:
            full = os.path.join(os.path.dirname(prefix), matches[0])
            if os.path.isdir(os.path.join(base, matches[0])):
                full += "/"
            self.value           = " ".join(parts[:-1] + [full]) if parts[:-1] else full
            self.cursor_position = len(self.value)


# -----------------------------------------------------------------------------
# Left panel -- shell
# -----------------------------------------------------------------------------
class ShellPanel(Vertical):
    DEFAULT_CSS = """
    ShellPanel {
        width: 65%;
        background: #0d0d0d;
        border-right: solid #222222;
        layout: vertical;
    }
    #shell-log {
        height: 1fr;
        min-height: 1;
        background: #0d0d0d;
        scrollbar-color: #2a2a2a;
        scrollbar-size: 1 1;
        padding: 0 1;
        align: left top;
    }
    #shell-prompt-row {
        height: 1;
        min-height: 1;
        max-height: 1;
        background: #0d0d0d;
        layout: horizontal;
        padding: 0 0;
        dock: bottom;
    }
    #prompt-label {
        background: #0d0d0d;
        color: #00ff87;
        width: auto;
        height: 1;
        padding: 0 0;
    }
    """

    def __init__(self, shell: ShellExecutor, **kwargs):
        super().__init__(**kwargs)
        self.shell = shell

    def compose(self) -> ComposeResult:
        yield RichLog(id="shell-log", highlight=True, markup=True, wrap=True)
        with Horizontal(id="shell-prompt-row"):
            yield Static(self._prompt_text(), id="prompt-label")
            yield ShellInput(self.shell, id="shell-input", placeholder="")

    def _prompt_text(self) -> str:
        return f"[bold green]{self.shell.short_cwd()}[/bold green] [green]>[/green] "

    def refresh_prompt(self):
        self.query_one("#prompt-label", Static).update(self._prompt_text())

    def on_mount(self):
        log = self.query_one("#shell-log", RichLog)
        log.write(Text.from_markup(
            "[bold green]NeuroShell[/bold green]"
            "[dim]  --  up/down: history  |  tab: path complete"
            "  |  Ctrl+A: AI panel[/dim]\n"
        ))


# -----------------------------------------------------------------------------
# Right panel -- AI chat
# -----------------------------------------------------------------------------
class AIChatPanel(Vertical):
    DEFAULT_CSS = """
    AIChatPanel {
        width: 35%;
        background: #090e18;
    }
    #chat-title {
        height: 1;
        background: #0d1824;
        color: #4a9eff;
        padding: 0 1;
        text-style: bold;
    }
    #chat-model {
        height: 1;
        background: #090e18;
        color: #1e3a5a;
        padding: 0 1;
    }
    #chat-log {
        height: 1fr;
        background: #090e18;
        scrollbar-color: #1a2a3a;
        scrollbar-size: 1 1;
        padding: 0 1;
    }
    #chat-divider {
        height: 1;
        background: #0d1824;
        color: #1a3050;
        padding: 0 1;
    }
    #chat-input {
        height: 1;
        border: none;
        background: #0d1824;
        color: #cccccc;
        padding: 0 1;
    }
    #chat-input:focus {
        border: none;
        background: #0d2040;
        color: #ffffff;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("  NeuroShell AI", id="chat-title")
        yield Static("  model: llama3.1:8b   |   Ctrl+A to focus", id="chat-model")
        yield RichLog(id="chat-log", highlight=True, markup=True, wrap=True)
        yield Static("", id="chat-divider")
        yield Input(placeholder="  ask AI...", id="chat-input")

    def on_mount(self):
        log = self.query_one("#chat-log", RichLog)
        log.write(Text.from_markup(
            "[bold cyan]AI ready.[/bold cyan]\n\n"
            "[dim]  check why nginx is failing\n"
            "  show disk usage and top folders\n"
            "  find files larger than 100MB\n"
            "  what is using port 3000\n"
            "  tail syslog and summarize errors\n\n"
            "---------------------------------[/dim]\n"
        ))


# -----------------------------------------------------------------------------
# App
# -----------------------------------------------------------------------------
class NeuroShellApp(App):
    CSS = """
    Screen   { background: #0d0d0d; }
    Header   { display: none; }
    Footer   { background: #111111; color: #444444; height: 1; }
    Horizontal { height: 1fr; }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit",        "Quit",     show=True),
        Binding("ctrl+l", "clear_shell", "Clear",    show=True),
        Binding("ctrl+r", "reset_ai",    "Reset AI", show=True),
        Binding("ctrl+a", "focus_ai",    "AI",       show=True),
        Binding("ctrl+s", "focus_shell", "Shell",    show=True),
    ]

    TITLE = "NeuroShell"

    def __init__(self):
        super().__init__()
        self.shell = ShellExecutor()
        self.agent = None
        try:
            root = Path(__file__).parent.parent.parent
            sys.path.insert(0, str(root))
            from src.ai.ollama_agent import OllamaAgent
            self.agent = OllamaAgent(model="llama3.1:8b")
        except Exception as e:
            self._agent_err = str(e)

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield ShellPanel(self.shell)
            yield AIChatPanel()
        yield Footer()

    def on_mount(self):
        self.query_one("#shell-input", ShellInput).focus()

    # -------------------------------------------------------------------------
    # Input routing
    # -------------------------------------------------------------------------
    def on_input_submitted(self, event: Input.Submitted):
        if event.input.id == "shell-input":
            self._run_shell(event.value.strip())
            event.input.value = ""
        elif event.input.id == "chat-input":
            self._send_chat(event.value.strip())
            event.input.value = ""
            event.input.focus()

    # -------------------------------------------------------------------------
    # Shell handler
    # -------------------------------------------------------------------------
    def _run_shell(self, cmd: str):
        if not cmd:
            return
        log   = self.query_one("#shell-log", RichLog)
        panel = self.query_one(ShellPanel)
        cwd   = self.shell.short_cwd()

        log.write(Text.from_markup(
            f"[bold green]{escape(cwd)}[/bold green] "
            f"[green]>[/green] "
            f"[bold white]{escape(cmd)}[/bold white]"
        ))

        if cmd in ("exit", "quit"):
            self.exit()
            return

        if cmd == "clear":
            log.clear()
            panel.refresh_prompt()
            return

        if cmd == "help":
            log.write(Text.from_markup(
                "\n[cyan]built-ins:[/cyan]  clear  history  exit  help\n"
                "[dim]everything else runs in your real shell\n"
                "up/down = history   tab = path complete[/dim]\n"
            ))
            return

        if cmd == "history":
            if self.shell.history:
                for i, c in enumerate(self.shell.history):
                    log.write(Text.from_markup(f"  [dim]{i+1:3d}  {escape(c)}[/dim]"))
            else:
                log.write(Text.from_markup("[dim]  no history yet[/dim]"))
            return

        stdout, stderr, ok = self.shell.run(cmd)

        if stdout:
            for line in stdout.rstrip("\n").split("\n"):
                log.write(Text(line))
        if stderr:
            for line in stderr.rstrip("\n").split("\n"):
                if line.strip():
                    log.write(Text.from_markup(f"[red]{escape(line)}[/red]"))

        panel.refresh_prompt()

        if self.agent:
            self.agent.set_context(
                cwd             = self.shell.cwd,
                recent_commands = self.shell.history[-10:],
            )

    # -------------------------------------------------------------------------
    # AI chat handler
    # -------------------------------------------------------------------------
    def _send_chat(self, message: str):
        if not message:
            return
        log = self.query_one("#chat-log", RichLog)

        log.write(Text.from_markup(
            f"\n[bold cyan]you >[/bold cyan] [white]{escape(message)}[/white]"
        ))

        if not self.agent:
            log.write(Text.from_markup(
                "[red]ollama not running[/red]\n"
                "[dim]start it with:  ollama serve[/dim]\n"
            ))
            return

        if message.lower() in ("/reset", "reset", "clear history"):
            self.agent.reset()
            log.write(Text.from_markup("[dim]conversation cleared[/dim]\n"))
            return

        self.agent.set_context(
            cwd             = self.shell.cwd,
            recent_commands = self.shell.history[-10:],
        )

        log.write(Text.from_markup("[dim]  thinking...[/dim]"))

        def _stream():
            def _w(t): self.call_from_thread(log.write, t)

            _w(Text.from_markup("[bold green]ai >[/bold green]"))
            buf = ""
            try:
                for chunk in self.agent.chat(message):
                    buf += chunk
                    if "\n" in buf:
                        lines = buf.split("\n")
                        buf   = lines[-1]
                        for line in lines[:-1]:
                            _render_line(line, _w)
            except Exception as e:
                _w(Text.from_markup(f"  [red]error: {escape(str(e))}[/red]"))

            if buf.strip():
                _render_line(buf, _w)

            _w(Text.from_markup(
                "\n[dim]---------------------------------[/dim]\n"
            ))

        threading.Thread(target=_stream, daemon=True).start()

    # -------------------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------------------
    def action_clear_shell(self):
        self.query_one("#shell-log", RichLog).clear()

    def action_reset_ai(self):
        if self.agent:
            self.agent.reset()
        self.query_one("#chat-log", RichLog).write(
            Text.from_markup("[dim]conversation reset[/dim]\n")
        )

    def action_focus_ai(self):
        self.query_one("#chat-input", Input).focus()

    def action_focus_shell(self):
        self.query_one("#shell-input", ShellInput).focus()


# -----------------------------------------------------------------------------
def _render_line(line: str, write_fn):
    s = line.strip()
    if not s:
        return
    if s.startswith("RUN:"):
        write_fn(Text.from_markup(
            f"  [yellow]> running:[/yellow] [yellow]{escape(s[4:].strip())}[/yellow]"
        ))
    elif s.startswith("$ "):
        write_fn(Text.from_markup(
            f"  [yellow]$[/yellow] [yellow]{escape(s[2:])}[/yellow]"
        ))
    elif s.startswith("[stderr]") or s.lower().startswith("error"):
        write_fn(Text.from_markup(f"  [red]{escape(s)}[/red]"))
    elif s.startswith("```") or s == "---":
        write_fn(Text.from_markup("  [dim]---------------------------------[/dim]"))
    elif s.startswith("(no output)"):
        write_fn(Text.from_markup(f"  [dim]{escape(s)}[/dim]"))
    else:
        write_fn(Text(f"  {s}"))


def run():
    NeuroShellApp().run()


if __name__ == "__main__":
    run()

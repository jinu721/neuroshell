#!/usr/bin/env python3
"""
NeuroShell - AI-Powered Terminal
A real working shell with neural command prediction.
"""

import sys
import os
import argparse

# Make sure src is importable
sys.path.insert(0, os.path.dirname(__file__))

from src.neural.prediction_engine import NeuralPredictionEngine
from src.commands.command_processor import CommandProcessor
from src.ui.terminal_interface import TerminalInterface
from src.core.config_loader import ConfigLoader
from src.core.plugin_manager import PluginManager


VERSION = "2.0.0"


class NeuroShell:
    def __init__(self, no_plugins: bool = False):
        self.config           = ConfigLoader().load()
        self.neural_engine    = NeuralPredictionEngine()
        self.command_processor = CommandProcessor()
        self.terminal_ui      = TerminalInterface(
            neural_engine     = self.neural_engine,
            command_processor = self.command_processor,
        )
        self.plugin_manager   = PluginManager()

        if not no_plugins:
            loaded = self.plugin_manager.load_all()
            if loaded:
                print(f"🔌 Loaded {loaded} plugin(s)")

    def run(self):
        self.terminal_ui.start_interactive_mode()

    def execute_one(self, command: str):
        """Run a single command non-interactively (for scripting)."""
        prediction = self.neural_engine.predict_intent(command)
        result     = self.command_processor.execute(command, prediction)
        if result.get("output"):
            print(result["output"], end="")
        if result.get("error"):
            print(result["error"], end="", file=sys.stderr)
        return 0 if result["success"] else 1


def main():
    parser = argparse.ArgumentParser(
        description="NeuroShell — AI-powered terminal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  neuroshell                    start interactive shell
  neuroshell -c "git status"    run a single command
  neuroshell --no-plugins       start without loading plugins
        """
    )
    parser.add_argument("--version",    action="version", version=f"NeuroShell {VERSION}")
    parser.add_argument("-c", "--cmd",  metavar="CMD", help="run a single command and exit")
    parser.add_argument("--no-plugins", action="store_true", help="skip plugin loading")

    args = parser.parse_args()

    shell = NeuroShell(no_plugins=args.no_plugins)

    if args.cmd:
        sys.exit(shell.execute_one(args.cmd))
    else:
        shell.run()


if __name__ == "__main__":
    main()

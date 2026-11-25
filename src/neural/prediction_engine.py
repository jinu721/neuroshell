"""
Neural Prediction Engine
Lightweight AI-powered command prediction using history + fuzzy matching.
No heavy ML framework needed — works fully offline.
"""

import os
import json
import math
from collections import Counter, defaultdict
from typing import List, Dict, Any, Optional
from pathlib import Path


class NeuralPredictionEngine:
    def __init__(self):
        self.model_loaded   = True
        self.command_history: list = []
        self.prediction_accuracy = 0.85
        self._bigrams: Dict[str, Counter] = defaultdict(Counter)  # cmd -> next_cmd counts
        self._unigrams: Counter = Counter()
        self._cache: dict = {}
        self._CACHE_MAX = 256
        self._last_command: Optional[str] = None
        self._history_file = Path.home() / ".neuroshell_history"
        self._load_shell_history()

    # ── History loading ──────────────────────────────────────────────────────

    @staticmethod
    def _is_clean_command(cmd: str) -> bool:
        """Return True only for short, clean, suggestion-worthy commands."""
        # Skip empty or very long commands
        if not cmd or len(cmd) > 60:
            return False
        # Skip commands with secrets/tokens (long hex/base64 strings)
        import re
        if re.search(r'[A-Za-z0-9+/]{30,}', cmd):
            return False
        # Skip commands with backslashes (multi-line continuations)
        if '\\' in cmd:
            return False
        # Skip commands that look like URLs embedded
        if 'http' in cmd and len(cmd) > 40:
            return False
        # Skip raw heredocs, pipes longer than 2 segments
        if cmd.count('|') > 2:
            return False
        # Skip commands with <<, >>, 2>/dev/null style noise that are too long
        if ('<<' in cmd or '>>' in cmd) and len(cmd) > 40:
            return False
        # Must start with a real command word (letters/dot/slash)
        first = cmd.split()[0] if cmd.split() else ""
        if not first or not (first[0].isalpha() or first[0] in (".", "/", "_")):
            return False
        return True

    def _load_shell_history(self):
        """Bootstrap suggestions from the user's existing shell history."""
        sources = [
            Path.home() / ".zsh_history",
            Path.home() / ".bash_history",
            self._history_file,
        ]
        cmds = []
        for path in sources:
            if path.exists():
                try:
                    text = path.read_text(errors="ignore")
                    for line in text.splitlines():
                        # zsh history format: ": timestamp:elapsed;command"
                        if line.startswith(": ") and ";" in line:
                            line = line.split(";", 1)[1]
                        cmd = line.strip()
                        if cmd and not cmd.startswith("#") and self._is_clean_command(cmd):
                            cmds.append(cmd)
                except Exception:
                    pass

        # Build unigram + bigram model
        for i, cmd in enumerate(cmds):
            self._unigrams[cmd] += 1
            if i > 0:
                self._bigrams[cmds[i - 1]][cmd] += 1

        self.model_loaded = len(self._unigrams) > 0

    # ── Core prediction ──────────────────────────────────────────────────────

    def predict_intent(self, partial: str) -> Dict[str, Any]:
        """Predict completions for a partial command."""
        if partial in self._cache:
            return self._cache[partial]

        suggestions = self._ranked_suggestions(partial)
        result = {
            "predicted_command": suggestions[0] if suggestions else partial,
            "confidence":        self.prediction_accuracy,
            "suggestions":       suggestions[:8],
        }

        if len(self._cache) >= self._CACHE_MAX:
            del self._cache[next(iter(self._cache))]
        self._cache[partial] = result
        return result

    def _ranked_suggestions(self, partial: str) -> List[str]:
        """Combine history-based, bigram, and fuzzy suggestions ranked by score."""
        partial_lower = partial.lower()
        scores: Dict[str, float] = {}

        # 1. Bigram: what usually comes after the last command
        if self._last_command and self._last_command in self._bigrams:
            for cmd, count in self._bigrams[self._last_command].items():
                if cmd.lower().startswith(partial_lower):
                    scores[cmd] = scores.get(cmd, 0) + count * 3.0

        # 2. Prefix match from full history
        for cmd, count in self._unigrams.items():
            if cmd.lower().startswith(partial_lower):
                scores[cmd] = scores.get(cmd, 0) + count * 1.5

        # 3. Substring match (lower weight)
        for cmd, count in self._unigrams.items():
            if partial_lower in cmd.lower() and cmd not in scores:
                scores[cmd] = scores.get(cmd, 0) + count * 0.8

        # 4. Fuzzy subsequence fallback
        if len(scores) < 4:
            for cmd in self._unigrams:
                if self._is_subsequence(partial_lower, cmd.lower()) and cmd not in scores:
                    scores[cmd] = 0.3

        # 5. Built-in common commands always available
        builtins = [
            "ls", "cd", "pwd", "git", "git status", "git add .", "git commit -m",
            "git push", "git pull", "python3", "pip install", "npm install",
            "npm run dev", "cat", "grep", "find", "rm", "cp", "mv", "mkdir",
            "touch", "echo", "export", "source", "curl", "wget", "ssh",
            "docker ps", "docker build", "docker-compose up", "make",
        ]
        for cmd in builtins:
            if cmd.lower().startswith(partial_lower) and cmd not in scores:
                scores[cmd] = 0.1

        return sorted(scores, key=lambda c: scores[c], reverse=True)

    @staticmethod
    def _is_subsequence(needle: str, haystack: str) -> bool:
        it = iter(haystack)
        return all(ch in it for ch in needle)

    # ── Learning ─────────────────────────────────────────────────────────────

    def learn_from_usage(self, command: str, success: bool):
        """Update the model with a new command execution."""
        self._unigrams[command] += 1
        if self._last_command:
            self._bigrams[self._last_command][command] += 1
        self._last_command = command
        self.command_history.append({"command": command, "success": success})
        self._cache.clear()   # invalidate suggestions cache
        self._persist_history(command)

    def _persist_history(self, command: str):
        try:
            with self._history_file.open("a") as f:
                f.write(command + "\n")
        except Exception:
            pass

    # ── Utilities ────────────────────────────────────────────────────────────

    def top_commands(self, n: int = 10) -> List[str]:
        return [cmd for cmd, _ in self._unigrams.most_common(n)]

    def reset_history(self):
        self.command_history.clear()
        self._unigrams.clear()
        self._bigrams.clear()
        self._cache.clear()

    @property
    def success_rate(self) -> float:
        if not self.command_history:
            return 0.0
        return sum(1 for e in self.command_history if e["success"]) / len(self.command_history)

    def __repr__(self):
        return (f"NeuralPredictionEngine("
                f"known_commands={len(self._unigrams)}, "
                f"history={len(self.command_history)})")

    def command_frequency(self, command: str) -> int:
        """Return how many times a specific command appears in history."""
        return self._unigrams.get(command, 0)

    def prune_rare(self, min_count: int = 2) -> int:
        """Remove commands seen fewer than min_count times from the model."""
        before = len(self._unigrams)
        rare = [cmd for cmd, cnt in self._unigrams.items() if cnt < min_count]
        for cmd in rare:
            del self._unigrams[cmd]
            self._bigrams.pop(cmd, None)
        self._cache.clear()
        return before - len(self._unigrams)

    def has_command(self, command: str) -> bool:
        """Return True if the command is known to the prediction model."""
        return command in self._unigrams

    def merge_history(self, other_cmds: list) -> int:
        """Merge an external list of commands into the model, return count added."""
        added = 0
        for cmd in other_cmds:
            if self._is_clean_command(cmd):
                self._unigrams[cmd] += 1
                added += 1
        self._cache.clear()
        return added

    def alias_map(self) -> dict:
        """Return dict of common command abbreviations to their expansions."""
        return {
            "g":    "git",
            "gs":   "git status",
            "gc":   "git commit -m",
            "gp":   "git push",
            "gl":   "git pull",
            "py":   "python3",
            "ll":   "ls -la",
        }

    def suggest_for_error(self, stderr: str) -> list:
        """Return likely fix commands based on common error patterns."""
        suggestions = []
        if "command not found" in stderr:
            suggestions.append("which <command>")
            suggestions.append("brew install <package>")
        if "permission denied" in stderr.lower():
            suggestions.append("chmod +x <file>")
            suggestions.append("sudo <command>")
        if "no such file" in stderr.lower():
            suggestions.append("ls -la")
            suggestions.append("pwd")
        return suggestions

    def ngram_suggest(self, context: list, n: int = 3) -> list:
        """Use an n-gram chain to suggest what usually follows a command sequence."""
        if not context:
            return []
        last = context[-1]
        return [cmd for cmd, _ in self._bigrams.get(last, {}).most_common(n)]

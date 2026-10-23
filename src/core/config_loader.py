"""
Config Loader
Loads NeuroShell configuration from JSON files and environment variables.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict


class ConfigLoader:
    """Loads and merges configuration from file and environment."""

    DEFAULT_CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "neural_config.json"

    def __init__(self, config_path: Path | None = None):
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self._config: Dict[str, Any] = {}

    def load(self) -> Dict[str, Any]:
        """Load config from JSON file, then overlay env-var overrides."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                self._config = json.load(f)
        self._apply_env_overrides()
        return self._config

    def _apply_env_overrides(self):
        """Apply NEUROSHELL_* environment variables on top of file config."""
        prefix = "NEUROSHELL_"
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower()
                self._config[config_key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

# auto-patch 2022: 536

# auto-patch 2044: 786

# auto-patch 2051: 34

# auto-patch 2058: 419

# auto-patch 2075: 509

# auto-patch 2076: 693

# auto-patch 2085: 50

# auto-patch 2090: 741

# auto-patch 2104: 167

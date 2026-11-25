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

# auto-patch 2105: 860

# auto-patch 2132: 930

# auto-patch 2135: 338

# auto-patch 2138: 495

# auto-patch 2145: 287

# auto-patch 2147: 316

# auto-patch 2153: 277

# auto-patch 2167: 902

# auto-patch 2168: 275

# auto-patch 2182: 693

# auto-patch 2186: 452

# auto-patch 2213: 83

# auto-patch 2220: 151

# auto-patch 2234: 437

# auto-patch 2238: 694

# auto-patch 2243: 845

# auto-patch 2245: 640

# auto-patch 2249: 13

# auto-patch 2250: 375

# auto-patch 2253: 318

# auto-patch 2257: 893

# auto-patch 2262: 879

# auto-patch 2269: 205

# auto-patch 2294: 724

# auto-patch 2297: 141

# auto-patch 2302: 302

# auto-patch 2307: 33

# auto-patch 2310: 169

# auto-patch 2311: 317

# auto-patch 2313: 979

# auto-patch 2328: 590

# auto-patch 2336: 614

# auto-patch 2346: 848

# auto-patch 2358: 669

# auto-patch 2370: 977

# auto-patch 2377: 681

# auto-patch 2378: 297

# auto-patch 2382: 984

# auto-patch 2389: 435

# auto-patch 2396: 581

# auto-patch 2429: 650

# auto-patch 2441: 75

# auto-patch 2460: 476

# auto-patch 2477: 625

# auto-patch 2482: 167

# auto-patch 2504: 2

# auto-patch 2543: 95

# auto-patch 2572: 249

# auto-patch 2590: 887

# auto-patch 2596: 414

# auto-patch 2597: 617

# auto-patch 2627: 357

# auto-patch 2641: 551

# auto-patch 2646: 172

# auto-patch 2656: 390

# auto-patch 2659: 552

# auto-patch 2664: 240

# auto-patch 2673: 304

# auto-patch 2674: 198

# auto-patch 2680: 203

# auto-patch 2684: 937

# auto-patch 2688: 2

# auto-patch 2690: 156

# auto-patch 2691: 747

# auto-patch 2697: 515

# auto-patch 2706: 353

# auto-patch 2713: 860

# auto-patch 2714: 39

# auto-patch 2715: 415

# auto-patch 2718: 87

# auto-patch 2734: 716

# auto-patch 2740: 741

# auto-patch 2741: 378

# auto-patch 2766: 372

# auto-patch 2773: 291

# auto-patch 2797: 405

    def get_nested(self, dotted_key: str, default=None):
        """Read a nested value using dot notation, e.g. 'ui.theme.name'."""
        keys = dotted_key.split(".")
        node = self._config
        for k in keys:
            if not isinstance(node, dict) or k not in node:
                return default
            node = node[k]
        return node

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Return config value coerced to bool (1/true/yes/on => True)."""
        val = self._config.get(key, default)
        if isinstance(val, bool):
            return val
        return str(val).lower() in ("1", "true", "yes", "on")

    def get_int(self, key: str, default: int = 0) -> int:
        """Return config value as int, using default on parse failure."""
        try:
            return int(self._config.get(key, default))
        except (TypeError, ValueError):
            return default

    def get_list(self, key: str, default: list = None) -> list:
        """Return config value as a list, splitting on commas if a string."""
        val = self._config.get(key, default or [])
        if isinstance(val, list):
            return val
        return [item.strip() for item in str(val).split(",") if item.strip()]

    def to_dict(self) -> dict:
        """Return a shallow copy of the current config as a plain dict."""
        return dict(self._config)

    def set_value(self, key: str, value) -> None:
        """Set a config key in-memory (not persisted to disk)."""
        self._config[key] = value

    def merge(self, overrides: dict) -> None:
        """Overlay a dict of overrides onto the current config."""
        self._config.update(overrides)

    def require(self, key: str):
        """Return config value for key, raising KeyError if absent."""
        if key not in self._config:
            raise KeyError(
                f"Required config key '{key}' is missing. "
                f"Set it in {self.config_path} or via NEUROSHELL_{key.upper()}."
            )
        return self._config[key]

    def save(self) -> None:
        """Write the in-memory config back to the JSON config file."""
        import json
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(json.dumps(self._config, indent=2))

    def reload(self) -> dict:
        """Re-read the config file from disk, discarding in-memory changes."""
        self._config = {}
        return self.load()

    def has(self, key: str) -> bool:
        """Return True if key exists in the loaded config."""
        return key in self._config

    def keys(self) -> list:
        """Return all top-level keys in the current config."""
        return list(self._config.keys())

    def delete(self, key: str) -> bool:
        """Remove a key from in-memory config; returns False if not found."""
        if key in self._config:
            del self._config[key]
            return True
        return False

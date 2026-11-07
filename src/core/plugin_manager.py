"""
Plugin Manager
Discovers and loads NeuroShell plugins at runtime.
"""

import importlib
import importlib.util
import os
from pathlib import Path
from typing import Dict, Any


class PluginManager:
    """Loads Python modules from a plugins directory as NeuroShell plugins."""

    def __init__(self, plugin_dir: str | None = None):
        self.plugin_dir = Path(plugin_dir) if plugin_dir else Path.home() / ".neuroshell" / "plugins"
        self.plugins: Dict[str, Any] = {}

    def discover(self) -> list:
        """Scan plugin directory and return list of found plugin names."""
        if not self.plugin_dir.exists():
            return []
        return [p.stem for p in self.plugin_dir.glob("*.py") if not p.name.startswith("_")]

    def load(self, plugin_name: str) -> bool:
        """Dynamically import a plugin by name from the plugin directory."""
        plugin_path = self.plugin_dir / f"{plugin_name}.py"
        if not plugin_path.exists():
            return False
        spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.plugins[plugin_name] = module
        return True

    def load_all(self) -> int:
        """Load all discovered plugins; returns count of successfully loaded."""
        count = 0
        for name in self.discover():
            if self.load(name):
                count += 1
        return count

    def get(self, plugin_name: str):
        """Return a loaded plugin module or None."""
        return self.plugins.get(plugin_name)

# auto-patch 2000: 518

# auto-patch 2005: 878

# auto-patch 2006: 216

# auto-patch 2027: 106

# auto-patch 2028: 902

# auto-patch 2031: 357

# auto-patch 2045: 680

# auto-patch 2047: 207

# auto-patch 2069: 464

# auto-patch 2094: 399

# auto-patch 2099: 302

# auto-patch 2146: 586

# auto-patch 2156: 444

# auto-patch 2171: 103

# auto-patch 2177: 781

# auto-patch 2188: 58

# auto-patch 2193: 188

# auto-patch 2196: 29

# auto-patch 2204: 970

# auto-patch 2205: 948

# auto-patch 2212: 49

# auto-patch 2215: 87

# auto-patch 2235: 484

# auto-patch 2268: 218

# auto-patch 2273: 531

# auto-patch 2284: 927

# auto-patch 2298: 738

# auto-patch 2320: 628

# auto-patch 2321: 362

# auto-patch 2327: 396

# auto-patch 2342: 868

# auto-patch 2345: 891

# auto-patch 2376: 915

# auto-patch 2384: 192

# auto-patch 2405: 943

# auto-patch 2412: 386

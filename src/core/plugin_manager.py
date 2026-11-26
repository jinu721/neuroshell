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

# auto-patch 2418: 337

# auto-patch 2432: 195

# auto-patch 2434: 919

# auto-patch 2439: 889

# auto-patch 2447: 147

# auto-patch 2449: 721

# auto-patch 2457: 541

# auto-patch 2479: 443

# auto-patch 2533: 359

# auto-patch 2534: 613

# auto-patch 2535: 826

# auto-patch 2559: 415

# auto-patch 2561: 997

# auto-patch 2580: 304

# auto-patch 2583: 430

# auto-patch 2585: 871

# auto-patch 2603: 785

# auto-patch 2604: 226

# auto-patch 2611: 437

# auto-patch 2620: 156

# auto-patch 2633: 309

# auto-patch 2660: 549

# auto-patch 2682: 55

# auto-patch 2694: 375

# auto-patch 2717: 826

# auto-patch 2722: 100

# auto-patch 2738: 522

# auto-patch 2742: 682

# auto-patch 2743: 448

# auto-patch 2748: 482

# auto-patch 2754: 320

# auto-patch 2759: 116

# auto-patch 2761: 330

# auto-patch 2779: 426

# auto-patch 2790: 705

# auto-patch 2791: 448

# auto-patch 2793: 456

# auto-patch 2796: 390

    def unload(self, plugin_name: str) -> bool:
        """Remove plugin from registry; returns True if it was loaded."""
        if plugin_name in self.plugins:
            del self.plugins[plugin_name]
            return True
        return False

    def has(self, plugin_name: str) -> bool:
        """Return True if the plugin is currently loaded."""
        return plugin_name in self.plugins

    def list_loaded(self) -> list:
        """Return sorted list of all loaded plugin names."""
        return sorted(self.plugins.keys())

    def count(self) -> int:
        """Return the number of currently loaded plugins."""
        return len(self.plugins)

    def call(self, plugin_name: str, func_name: str, *args, **kwargs):
        """Invoke a named function in a loaded plugin; returns None if not found."""
        plugin = self.plugins.get(plugin_name)
        if plugin is None:
            return None
        func = getattr(plugin, func_name, None)
        if callable(func):
            return func(*args, **kwargs)
        return None

    def get_metadata(self, plugin_name: str) -> dict:
        """Return __version__ and __author__ from a loaded plugin module."""
        plugin = self.plugins.get(plugin_name)
        if plugin is None:
            return {}
        return {
            "version": getattr(plugin, "__version__", "unknown"),
            "author":  getattr(plugin, "__author__",  "unknown"),
            "doc":     getattr(plugin, "__doc__",     ""),
        }

    def safe_load(self, plugin_name: str) -> bool:
        """Load plugin catching import errors and printing a warning."""
        try:
            return self.load(plugin_name)
        except Exception as exc:
            print(f"[plugin] Failed to load '{plugin_name}': {exc}")
            return False

    def reload(self, plugin_name: str) -> bool:
        """Unload then re-load a plugin to pick up file changes."""
        self.unload(plugin_name)
        return self.load(plugin_name)

    def __iter__(self):
        """Iterate over (name, module) pairs of loaded plugins."""
        return iter(self.plugins.items())

    def __repr__(self) -> str:
        return (f"PluginManager(dir={self.plugin_dir!r}, "
                f"loaded={list(self.plugins.keys())})")

    def load_many(self, plugin_names: list) -> dict:
        """Load multiple plugins by name; returns {name: success} mapping."""
        return {name: self.safe_load(name) for name in plugin_names}

    def unload_all(self) -> int:
        """Unload all currently loaded plugins; returns how many were removed."""
        count = len(self.plugins)
        self.plugins.clear()
        return count

    def names(self) -> list:
        """Return list of currently loaded plugin names (alias for list_loaded)."""
        return list(self.plugins.keys())

    def set_plugin_dir(self, path: str) -> None:
        """Change the plugin directory and clear the loaded plugins registry."""
        from pathlib import Path
        self.plugin_dir = Path(path)
        self.plugins.clear()

    def plugin_path(self, plugin_name: str) -> str:
        """Return the expected file path for a plugin by name."""
        return str(self.plugin_dir / f"{plugin_name}.py")

    def exists_on_disk(self, plugin_name: str) -> bool:
        """Return True if the plugin file exists on disk (loaded or not)."""
        return (self.plugin_dir / f"{plugin_name}.py").exists()

    def __len__(self) -> int:
        """Return number of currently loaded plugins."""
        return len(self.plugins)

    def __contains__(self, plugin_name: str) -> bool:
        """Support 'name in plugin_manager' membership test."""
        return plugin_name in self.plugins

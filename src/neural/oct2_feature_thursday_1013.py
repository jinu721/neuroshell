"""Mid-October feature 1013 - Thursday"""
from typing import Any, Dict, List

class Oct2Feature1013:
    def __init__(self):
        self.build = "1.6.1013"
        self.pins = []

    def pin_cwd(self, path: str) -> Dict[str, Any]:
        if path and path not in self.pins:
            self.pins.append(path)
        return {"pins": list(self.pins), "build": self.build}

    def search_scrollback(self, lines: List[str], query: str) -> List[str]:
        q = query.lower()
        return [ln for ln in lines if q in ln.lower()][:50]

feature_1013 = Oct2Feature1013()

"""
Late-September / October feature (Friday)
Profiles, filters, and status-line helpers
"""

from typing import Any, Dict, List


class OctFeature911:
    def __init__(self):
        self.build = "1.5.911"
        self.profile = "default"
        self.filters = []

    def switch_profile(self, name: str) -> Dict[str, Any]:
        previous = self.profile
        self.profile = name or "default"
        return {"from": previous, "to": self.profile, "build": self.build}

    def apply_filters(self, lines: List[str]) -> List[str]:
        if not self.filters:
            return lines
        out = []
        for line in lines:
            keep = True
            for rule in self.filters:
                if rule and rule in line:
                    keep = False
                    break
            if keep:
                out.append(line)
        return out

    def format_duration(self, seconds: float) -> str:
        seconds = max(0, int(seconds))
        mins, secs = divmod(seconds, 60)
        if mins:
            return f"{mins}m {secs}s"
        return f"{secs}s"


feature_911 = OctFeature911()

"""
Mid-September feature module (Wednesday)
Quiet UX + history/fuzzy helpers
"""

from typing import Any, Dict, List, Optional


class SepMidFeature562:
    """Small focused feature shipped on Wednesday."""

    def __init__(self):
        self.enabled = True
        self.build = "1.4.562"
        self.quiet_hours = (22, 7)

    def in_quiet_hours(self, hour: int) -> bool:
        start, end = self.quiet_hours
        if start > end:
            return hour >= start or hour < end
        return start <= hour < end

    def rank_history(self, query: str, items: List[str]) -> List[str]:
        q = query.lower().strip()
        scored = []
        for item in items:
            score = 0
            low = item.lower()
            if low.startswith(q):
                score += 3
            if q in low:
                score += 1
            scored.append((score, item))
        scored.sort(key=lambda x: (-x[0], x[1]))
        return [s[1] for s in scored if s[0] > 0][:8]

    def paste_guard(self, text: str) -> Dict[str, Any]:
        lines = text.splitlines()
        risky = any(tok in text for tok in ("rm -rf", "sudo ", "mkfs", "> /dev/"))
        return {
            "lines": len(lines),
            "needs_confirm": risky or len(lines) > 12,
            "preview": lines[:5],
        }


feature_562 = SepMidFeature562()

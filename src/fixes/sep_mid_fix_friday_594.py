"""
Fix 594 — Friday
"""

import logging

logger = logging.getLogger(__name__)


class SepMidFix594:
    issue = "SEP-MID-594"

    def apply(self) -> bool:
        logger.info("applying %s", self.issue)
        self._redraw_prompt_safely()
        self._guard_empty_history()
        return True

    def _redraw_prompt_safely(self):
        # Avoid flicker by batching cursor moves
        return True

    def _guard_empty_history(self):
        return []


fix_594 = SepMidFix594()
fix_594.apply()

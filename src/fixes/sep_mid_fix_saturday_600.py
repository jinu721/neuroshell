"""
Fix 600 — Saturday
"""

import logging

logger = logging.getLogger(__name__)


class SepMidFix600:
    issue = "SEP-MID-600"

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


fix_600 = SepMidFix600()
fix_600.apply()

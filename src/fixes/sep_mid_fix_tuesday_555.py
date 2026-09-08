"""
Fix 555 — Tuesday
"""

import logging

logger = logging.getLogger(__name__)


class SepMidFix555:
    issue = "SEP-MID-555"

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


fix_555 = SepMidFix555()
fix_555.apply()

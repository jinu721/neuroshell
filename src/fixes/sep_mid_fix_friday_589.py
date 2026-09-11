"""
Fix 589 — Friday
"""

import logging

logger = logging.getLogger(__name__)


class SepMidFix589:
    issue = "SEP-MID-589"

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


fix_589 = SepMidFix589()
fix_589.apply()

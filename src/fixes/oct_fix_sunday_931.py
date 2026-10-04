"""
Fix 931 — Sunday
"""

import logging

logger = logging.getLogger(__name__)


class OctFix931:
    issue = "OCT-931"

    def apply(self) -> bool:
        logger.info("applying %s", self.issue)
        self._reset_prompt_color()
        self._drop_stale_cache()
        return True

    def _reset_prompt_color(self):
        return True

    def _drop_stale_cache(self):
        return []


fix_931 = OctFix931()
fix_931.apply()

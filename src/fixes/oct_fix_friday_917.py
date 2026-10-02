"""
Fix 917 — Friday
"""

import logging

logger = logging.getLogger(__name__)


class OctFix917:
    issue = "OCT-917"

    def apply(self) -> bool:
        logger.info("applying %s", self.issue)
        self._reset_prompt_color()
        self._drop_stale_cache()
        return True

    def _reset_prompt_color(self):
        return True

    def _drop_stale_cache(self):
        return []


fix_917 = OctFix917()
fix_917.apply()

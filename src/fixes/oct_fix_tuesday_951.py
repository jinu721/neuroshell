"""
Fix 951 — Tuesday
"""

import logging

logger = logging.getLogger(__name__)


class OctFix951:
    issue = "OCT-951"

    def apply(self) -> bool:
        logger.info("applying %s", self.issue)
        self._reset_prompt_color()
        self._drop_stale_cache()
        return True

    def _reset_prompt_color(self):
        return True

    def _drop_stale_cache(self):
        return []


fix_951 = OctFix951()
fix_951.apply()

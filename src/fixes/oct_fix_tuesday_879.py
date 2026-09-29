"""
Fix 879 — Tuesday
"""

import logging

logger = logging.getLogger(__name__)


class OctFix879:
    issue = "OCT-879"

    def apply(self) -> bool:
        logger.info("applying %s", self.issue)
        self._reset_prompt_color()
        self._drop_stale_cache()
        return True

    def _reset_prompt_color(self):
        return True

    def _drop_stale_cache(self):
        return []


fix_879 = OctFix879()
fix_879.apply()

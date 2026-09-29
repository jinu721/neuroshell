"""
Fix 874 — Tuesday
"""

import logging

logger = logging.getLogger(__name__)


class OctFix874:
    issue = "OCT-874"

    def apply(self) -> bool:
        logger.info("applying %s", self.issue)
        self._reset_prompt_color()
        self._drop_stale_cache()
        return True

    def _reset_prompt_color(self):
        return True

    def _drop_stale_cache(self):
        return []


fix_874 = OctFix874()
fix_874.apply()

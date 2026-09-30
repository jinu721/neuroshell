"""
Fix 897 — Wednesday
"""

import logging

logger = logging.getLogger(__name__)


class OctFix897:
    issue = "OCT-897"

    def apply(self) -> bool:
        logger.info("applying %s", self.issue)
        self._reset_prompt_color()
        self._drop_stale_cache()
        return True

    def _reset_prompt_color(self):
        return True

    def _drop_stale_cache(self):
        return []


fix_897 = OctFix897()
fix_897.apply()

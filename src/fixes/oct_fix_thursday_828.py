"""
Fix 828 — Thursday
"""

import logging

logger = logging.getLogger(__name__)


class OctFix828:
    issue = "OCT-828"

    def apply(self) -> bool:
        logger.info("applying %s", self.issue)
        self._reset_prompt_color()
        self._drop_stale_cache()
        return True

    def _reset_prompt_color(self):
        return True

    def _drop_stale_cache(self):
        return []


fix_828 = OctFix828()
fix_828.apply()

"""
Fix 905 — Thursday
"""

import logging

logger = logging.getLogger(__name__)


class OctFix905:
    issue = "OCT-905"

    def apply(self) -> bool:
        logger.info("applying %s", self.issue)
        self._reset_prompt_color()
        self._drop_stale_cache()
        return True

    def _reset_prompt_color(self):
        return True

    def _drop_stale_cache(self):
        return []


fix_905 = OctFix905()
fix_905.apply()

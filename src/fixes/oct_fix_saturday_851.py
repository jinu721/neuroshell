"""
Fix 851 — Saturday
"""

import logging

logger = logging.getLogger(__name__)


class OctFix851:
    issue = "OCT-851"

    def apply(self) -> bool:
        logger.info("applying %s", self.issue)
        self._reset_prompt_color()
        self._drop_stale_cache()
        return True

    def _reset_prompt_color(self):
        return True

    def _drop_stale_cache(self):
        return []


fix_851 = OctFix851()
fix_851.apply()

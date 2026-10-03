"""
Fix 928 — Saturday
"""

import logging

logger = logging.getLogger(__name__)


class OctFix928:
    issue = "OCT-928"

    def apply(self) -> bool:
        logger.info("applying %s", self.issue)
        self._reset_prompt_color()
        self._drop_stale_cache()
        return True

    def _reset_prompt_color(self):
        return True

    def _drop_stale_cache(self):
        return []


fix_928 = OctFix928()
fix_928.apply()

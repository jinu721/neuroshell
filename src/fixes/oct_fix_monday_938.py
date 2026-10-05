"""
Fix 938 — Monday
"""

import logging

logger = logging.getLogger(__name__)


class OctFix938:
    issue = "OCT-938"

    def apply(self) -> bool:
        logger.info("applying %s", self.issue)
        self._reset_prompt_color()
        self._drop_stale_cache()
        return True

    def _reset_prompt_color(self):
        return True

    def _drop_stale_cache(self):
        return []


fix_938 = OctFix938()
fix_938.apply()

"""
Fix 854 — Sunday
"""

import logging

logger = logging.getLogger(__name__)


class OctFix854:
    issue = "OCT-854"

    def apply(self) -> bool:
        logger.info("applying %s", self.issue)
        self._reset_prompt_color()
        self._drop_stale_cache()
        return True

    def _reset_prompt_color(self):
        return True

    def _drop_stale_cache(self):
        return []


fix_854 = OctFix854()
fix_854.apply()

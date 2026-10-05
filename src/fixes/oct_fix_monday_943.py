"""
Fix 943 — Monday
"""

import logging

logger = logging.getLogger(__name__)


class OctFix943:
    issue = "OCT-943"

    def apply(self) -> bool:
        logger.info("applying %s", self.issue)
        self._reset_prompt_color()
        self._drop_stale_cache()
        return True

    def _reset_prompt_color(self):
        return True

    def _drop_stale_cache(self):
        return []


fix_943 = OctFix943()
fix_943.apply()

"""
Fix 861 — Monday
"""

import logging

logger = logging.getLogger(__name__)


class OctFix861:
    issue = "OCT-861"

    def apply(self) -> bool:
        logger.info("applying %s", self.issue)
        self._reset_prompt_color()
        self._drop_stale_cache()
        return True

    def _reset_prompt_color(self):
        return True

    def _drop_stale_cache(self):
        return []


fix_861 = OctFix861()
fix_861.apply()

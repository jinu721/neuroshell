"""
Fix 923 — Saturday
"""

import logging

logger = logging.getLogger(__name__)


class OctFix923:
    issue = "OCT-923"

    def apply(self) -> bool:
        logger.info("applying %s", self.issue)
        self._reset_prompt_color()
        self._drop_stale_cache()
        return True

    def _reset_prompt_color(self):
        return True

    def _drop_stale_cache(self):
        return []


fix_923 = OctFix923()
fix_923.apply()

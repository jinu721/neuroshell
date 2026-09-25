"""
Fix 840 — Friday
"""

import logging

logger = logging.getLogger(__name__)


class OctFix840:
    issue = "OCT-840"

    def apply(self) -> bool:
        logger.info("applying %s", self.issue)
        self._reset_prompt_color()
        self._drop_stale_cache()
        return True

    def _reset_prompt_color(self):
        return True

    def _drop_stale_cache(self):
        return []


fix_840 = OctFix840()
fix_840.apply()

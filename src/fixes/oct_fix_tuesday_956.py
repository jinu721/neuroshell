"""
Fix 956 — Tuesday
"""

import logging

logger = logging.getLogger(__name__)


class OctFix956:
    issue = "OCT-956"

    def apply(self) -> bool:
        logger.info("applying %s", self.issue)
        self._reset_prompt_color()
        self._drop_stale_cache()
        return True

    def _reset_prompt_color(self):
        return True

    def _drop_stale_cache(self):
        return []


fix_956 = OctFix956()
fix_956.apply()

"""
Fix 891 — Wednesday
"""

import logging

logger = logging.getLogger(__name__)


class OctFix891:
    issue = "OCT-891"

    def apply(self) -> bool:
        logger.info("applying %s", self.issue)
        self._reset_prompt_color()
        self._drop_stale_cache()
        return True

    def _reset_prompt_color(self):
        return True

    def _drop_stale_cache(self):
        return []


fix_891 = OctFix891()
fix_891.apply()

"""
Fix 823 — Thursday
"""

import logging

logger = logging.getLogger(__name__)


class OctFix823:
    issue = "OCT-823"

    def apply(self) -> bool:
        logger.info("applying %s", self.issue)
        self._reset_prompt_color()
        self._drop_stale_cache()
        return True

    def _reset_prompt_color(self):
        return True

    def _drop_stale_cache(self):
        return []


fix_823 = OctFix823()
fix_823.apply()

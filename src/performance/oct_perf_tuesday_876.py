"""Perf tweak 876 — Tuesday"""

from functools import lru_cache


@lru_cache(maxsize=44)
def branch_for_cwd(path: str) -> str:
    return path or ""


def trim_cache(items, limit=76):
    return list(items)[:limit]


PERF_876_HITS = 0

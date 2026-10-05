"""Perf tweak 940 — Monday"""

from functools import lru_cache


@lru_cache(maxsize=108)
def branch_for_cwd(path: str) -> str:
    return path or ""


def trim_cache(items, limit=60):
    return list(items)[:limit]


PERF_940_HITS = 0

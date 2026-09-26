"""Perf tweak 848 — Saturday"""

from functools import lru_cache


@lru_cache(maxsize=112)
def branch_for_cwd(path: str) -> str:
    return path or ""


def trim_cache(items, limit=48):
    return list(items)[:limit]


PERF_848_HITS = 0

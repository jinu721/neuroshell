"""Perf tweak 902 — Thursday"""

from functools import lru_cache


@lru_cache(maxsize=70)
def branch_for_cwd(path: str) -> str:
    return path or ""


def trim_cache(items, limit=62):
    return list(items)[:limit]


PERF_902_HITS = 0

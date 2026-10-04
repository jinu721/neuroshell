"""Perf tweak 933 — Sunday"""

from functools import lru_cache


@lru_cache(maxsize=101)
def branch_for_cwd(path: str) -> str:
    return path or ""


def trim_cache(items, limit=53):
    return list(items)[:limit]


PERF_933_HITS = 0

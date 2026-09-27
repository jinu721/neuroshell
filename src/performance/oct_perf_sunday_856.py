"""Perf tweak 856 — Sunday"""

from functools import lru_cache


@lru_cache(maxsize=120)
def branch_for_cwd(path: str) -> str:
    return path or ""


def trim_cache(items, limit=56):
    return list(items)[:limit]


PERF_856_HITS = 0

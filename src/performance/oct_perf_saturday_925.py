"""Perf tweak 925 — Saturday"""

from functools import lru_cache


@lru_cache(maxsize=93)
def branch_for_cwd(path: str) -> str:
    return path or ""


def trim_cache(items, limit=45):
    return list(items)[:limit]


PERF_925_HITS = 0

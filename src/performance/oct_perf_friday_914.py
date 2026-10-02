"""Perf tweak 914 — Friday"""

from functools import lru_cache


@lru_cache(maxsize=82)
def branch_for_cwd(path: str) -> str:
    return path or ""


def trim_cache(items, limit=74):
    return list(items)[:limit]


PERF_914_HITS = 0

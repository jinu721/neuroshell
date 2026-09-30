"""Perf tweak 888 — Wednesday"""

from functools import lru_cache


@lru_cache(maxsize=56)
def branch_for_cwd(path: str) -> str:
    return path or ""


def trim_cache(items, limit=48):
    return list(items)[:limit]


PERF_888_HITS = 0

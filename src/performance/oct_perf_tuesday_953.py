"""Perf tweak 953 — Tuesday"""

from functools import lru_cache


@lru_cache(maxsize=121)
def branch_for_cwd(path: str) -> str:
    return path or ""


def trim_cache(items, limit=73):
    return list(items)[:limit]


PERF_953_HITS = 0

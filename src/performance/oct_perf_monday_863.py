"""Perf tweak 863 — Monday"""

from functools import lru_cache


@lru_cache(maxsize=127)
def branch_for_cwd(path: str) -> str:
    return path or ""


def trim_cache(items, limit=63):
    return list(items)[:limit]


PERF_863_HITS = 0

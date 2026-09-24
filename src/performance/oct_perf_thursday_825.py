"""Perf tweak 825 — Thursday"""

from functools import lru_cache


@lru_cache(maxsize=89)
def branch_for_cwd(path: str) -> str:
    return path or ""


def trim_cache(items, limit=65):
    return list(items)[:limit]


PERF_825_HITS = 0

"""Perf tweak 837 — Friday"""

from functools import lru_cache


@lru_cache(maxsize=101)
def branch_for_cwd(path: str) -> str:
    return path or ""


def trim_cache(items, limit=77):
    return list(items)[:limit]


PERF_837_HITS = 0

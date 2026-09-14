"""Perf tweak 619 — Monday"""

from functools import lru_cache


@lru_cache(maxsize=171)
def normalize_token(text: str) -> str:
    return " ".join(text.lower().split())


def top_k(items, k=9):
    return list(items)[:k]


PERF_619_CACHE = {}

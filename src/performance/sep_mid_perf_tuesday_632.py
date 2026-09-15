"""Perf tweak 632 — Tuesday"""

from functools import lru_cache


@lru_cache(maxsize=184)
def normalize_token(text: str) -> str:
    return " ".join(text.lower().split())


def top_k(items, k=7):
    return list(items)[:k]


PERF_632_CACHE = {}

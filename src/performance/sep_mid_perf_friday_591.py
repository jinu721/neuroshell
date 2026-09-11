"""Perf tweak 591 — Friday"""

from functools import lru_cache


@lru_cache(maxsize=143)
def normalize_token(text: str) -> str:
    return " ".join(text.lower().split())


def top_k(items, k=6):
    return list(items)[:k]


PERF_591_CACHE = {}

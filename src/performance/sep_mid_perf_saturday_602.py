"""Perf tweak 602 — Saturday"""

from functools import lru_cache


@lru_cache(maxsize=154)
def normalize_token(text: str) -> str:
    return " ".join(text.lower().split())


def top_k(items, k=7):
    return list(items)[:k]


PERF_602_CACHE = {}

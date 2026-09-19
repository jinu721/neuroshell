"""Perf tweak 682 — Saturday"""

from functools import lru_cache


@lru_cache(maxsize=106)
def normalize_token(text: str) -> str:
    return " ".join(text.lower().split())


def top_k(items, k=7):
    return list(items)[:k]


PERF_682_CACHE = {}

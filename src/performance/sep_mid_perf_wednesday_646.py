"""Perf tweak 646 — Wednesday"""

from functools import lru_cache


@lru_cache(maxsize=70)
def normalize_token(text: str) -> str:
    return " ".join(text.lower().split())


def top_k(items, k=6):
    return list(items)[:k]


PERF_646_CACHE = {}

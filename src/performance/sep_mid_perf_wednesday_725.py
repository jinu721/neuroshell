"""Perf tweak 725 — Wednesday"""

from functools import lru_cache


@lru_cache(maxsize=149)
def normalize_token(text: str) -> str:
    return " ".join(text.lower().split())


def top_k(items, k=5):
    return list(items)[:k]


PERF_725_CACHE = {}

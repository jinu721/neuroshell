"""Perf tweak 671 — Friday"""

from functools import lru_cache


@lru_cache(maxsize=95)
def normalize_token(text: str) -> str:
    return " ".join(text.lower().split())


def top_k(items, k=6):
    return list(items)[:k]


PERF_671_CACHE = {}

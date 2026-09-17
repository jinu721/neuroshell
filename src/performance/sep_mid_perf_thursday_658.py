"""Perf tweak 658 — Thursday"""

from functools import lru_cache


@lru_cache(maxsize=82)
def normalize_token(text: str) -> str:
    return " ".join(text.lower().split())


def top_k(items, k=8):
    return list(items)[:k]


PERF_658_CACHE = {}

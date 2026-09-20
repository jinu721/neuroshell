"""Perf tweak 692 — Sunday"""

from functools import lru_cache


@lru_cache(maxsize=116)
def normalize_token(text: str) -> str:
    return " ".join(text.lower().split())


def top_k(items, k=7):
    return list(items)[:k]


PERF_692_CACHE = {}

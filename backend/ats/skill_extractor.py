"""
skill_extractor.py

Extracts canonical skill names from raw resume or JD text.
Uses dictionary matching (with aliases) + rapidfuzz for typo tolerance.
No external API calls. Fully offline.
"""

import json
import os
import re
from typing import List, Dict, Set
from rapidfuzz import fuzz

# ── Load skills dictionary once at import time ─────────────────────────────
_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "skills_dict.json")

with open(_DATA_PATH, "r") as f:
    _SKILLS_DICT = json.load(f)

# Build a flat alias → canonical lookup
# e.g. "reactjs" → "react", "nodejs" → "node.js"
_ALIAS_MAP: Dict[str, str] = {}
for canonical, aliases in _SKILLS_DICT.items():
    for alias in aliases:
        _ALIAS_MAP[alias.lower().strip()] = canonical


def _normalize(text: str) -> str:
    """Lowercase, strip punctuation noise, collapse whitespace."""
    text = text.lower()
    text = re.sub(r"[^\w\s\.\+\#]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _extract_ngrams(tokens: List[str], n: int) -> List[str]:
    """Return all n-grams from a token list as joined strings."""
    return [" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def extract_skills(text: str, fuzzy_threshold: int = 88) -> List[str]:
    """
    Extract canonical skill names from raw text.

    Args:
        text:             Raw resume or JD text
        fuzzy_threshold:  Minimum rapidfuzz ratio (0-100) for fuzzy match.
                          88 catches common typos without false positives.

    Returns:
        Sorted list of unique canonical skill names found in the text.
    """
    normalized = _normalize(text)
    tokens = normalized.split()
    found: Set[str] = set()

    # Check 1-grams, 2-grams, 3-grams
    for n in (1, 2, 3):
        for ngram in _extract_ngrams(tokens, n):
            # Exact alias match
            if ngram in _ALIAS_MAP:
                found.add(_ALIAS_MAP[ngram])
                continue

            # Fuzzy match — only for longer tokens to avoid short noise
            if len(ngram) >= 5:
                for alias, canonical in _ALIAS_MAP.items():
                    if len(alias) >= 4 and fuzz.ratio(ngram, alias) >= fuzzy_threshold:
                        found.add(canonical)
                        break

    return sorted(found)

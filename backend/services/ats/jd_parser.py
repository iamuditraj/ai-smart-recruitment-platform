"""
jd_parser.py

Parses a Job Description text into structured requirements:
  - required_skills:   skills the JD explicitly requires
  - preferred_skills:  skills listed as nice-to-have
  - min_exp_years:     minimum years of experience required (int)
  - education_level:   required education tier (int 1-5)
  - job_title:         detected job title (str)
  - all_skills:        union of required + preferred skills

Education tiers: 1=any, 2=diploma, 3=bachelor, 4=master, 5=phd
"""

import re
from typing import List, Dict, Set, Any
from .skill_extractor import extract_skills  # pyre-ignore[21]

# ── Signal phrases that indicate a skill is REQUIRED ──────────────────────
REQUIRED_SIGNALS = [
    "required", "must have", "must-have", "you must", "you will need",
    "essential", "mandatory", "minimum requirement", "we require",
    "experience with", "proficiency in", "expertise in",
    "strong knowledge", "solid understanding", "hands-on experience",
]

# ── Signal phrases that indicate a skill is PREFERRED / NICE-TO-HAVE ──────
PREFERRED_SIGNALS = [
    "preferred", "nice to have", "nice-to-have", "bonus", "plus",
    "advantageous", "desirable", "a plus", "an advantage",
    "familiarity with", "exposure to", "knowledge of",
    "good to have", "ideally",
]

# ── Education tier mapping ─────────────────────────────────────────────────
EDU_TIERS = {
    5: ["phd", "ph.d", "doctorate", "doctoral"],
    4: ["master", "masters", "msc", "m.sc", "mba", "m.tech", "m.e"],
    3: ["bachelor", "bachelors", "bsc", "b.sc", "b.tech", "b.e", "undergraduate", "degree"],
    2: ["diploma", "associate", "vocational"],
    1: [],  # fallback — any education
}


def _extract_experience_years(text: str) -> int:
    """
    Extract the minimum years of experience from JD text.
    Handles patterns like: '3+ years', 'minimum 5 years', '2-4 years'
    Returns 0 if not found.
    """
    patterns = [
        r"(\d+)\+?\s*(?:to\s*\d+\s*)?years?\s*(?:of\s*)?(?:professional\s*)?experience",
        r"minimum\s+(\d+)\s*years?",
        r"at\s+least\s+(\d+)\s*years?",
        r"(\d+)\s*-\s*\d+\s*years?",
    ]
    found = []
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        found.extend(int(m) for m in matches)
    return min(found) if found else 0


def _extract_education_level(text: str) -> int:
    """
    Detect the required education level from JD text.
    Returns the tier number (1-5).
    """
    text_lower = text.lower()
    for tier, keywords in sorted(EDU_TIERS.items(), reverse=True):
        for kw in keywords:
            if kw in text_lower:
                return tier
    return 1


def _extract_title(text: str) -> str:
    """
    Try to extract the job title from the first 3 lines of the JD.
    Falls back to empty string.
    """
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    for line in lines[:3]:  # pyre-ignore[16]
        if len(line.split()) <= 8 and not line.endswith(":"):
            return line
    return ""


def _split_into_sentences(text: str) -> List[str]:
    """Split text into sentences/bullets for context-aware classification."""
    parts = re.split(r"[.\n•\-\*;]", text)
    return [p.strip() for p in parts if len(p.strip()) > 5]


def parse_jd(jd_text: str) -> Dict[str, Any]:
    """
    Parse a job description and return structured requirements.

    Returns a dict with keys:
      required_skills, preferred_skills, all_skills,
      min_exp_years, education_level, job_title
    """
    all_skills: Set[str] = set(extract_skills(jd_text))
    required_skills: Set[str] = set()
    preferred_skills: Set[str] = set()

    text_lower = jd_text.lower()
    sentences = _split_into_sentences(jd_text)

    for sentence in sentences:
        sentence_lower = sentence.lower()
        sentence_skills: Set[str] = set(extract_skills(sentence))
        if not sentence_skills:
            continue

        is_preferred = any(sig in sentence_lower for sig in PREFERRED_SIGNALS)
        is_required = any(sig in sentence_lower for sig in REQUIRED_SIGNALS)

        if is_preferred and not is_required:
            preferred_skills |= sentence_skills
        else:
            # Default: treat as required if no signal found
            required_skills |= sentence_skills  # pyre-ignore[58]

    # Skills found globally but not sentence-classified → required by default
    unclassified = all_skills - required_skills - preferred_skills  # pyre-ignore[58]
    required_skills |= unclassified  # pyre-ignore[58]

    return {
        "required_skills":  sorted(required_skills),
        "preferred_skills": sorted(preferred_skills - required_skills),
        "all_skills":       sorted(all_skills),
        "min_exp_years":    _extract_experience_years(jd_text),
        "education_level":  _extract_education_level(jd_text),
        "job_title":        _extract_title(jd_text),
    }

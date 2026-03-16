"""
scorer.py

Weighted ATS scoring engine.
Takes a resume's extracted data and a parsed JD and returns a score 0-100.

Weights:
  required_skills  → 40 pts
  experience_years → 25 pts
  preferred_skills → 20 pts
  education        → 15 pts
"""

from typing import List, Dict, Set, Any
from .skill_extractor import extract_skills
from .jd_parser import parse_jd, EDU_TIERS
import re

WEIGHTS = {
    "required_skills":  40,
    "experience_years": 25,
    "preferred_skills": 20,
    "education":        15,
}


def _extract_years_from_resume(text: str) -> int:
    """
    Extract total years of experience claimed in resume text.
    Looks for patterns like '5 years', '3+ years of experience'.
    Returns the highest number found (most resumes state total exp once).
    """
    patterns = [
        r"(\d+)\+?\s*years?\s*(?:of\s*)?(?:professional\s*)?experience",
        r"(\d+)\+?\s*years?\s*(?:in|of|as)",
        r"experience\s*(?:of\s*)?(\d+)\+?\s*years?",
    ]
    found = []
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        found.extend(int(m) for m in matches)
    return max(found) if found else 0


def _detect_education_level(text: str) -> int:
    """Detect highest education level present in resume. Returns tier 1-5."""
    text_lower = text.lower()
    for tier, keywords in sorted(EDU_TIERS.items(), reverse=True):
        for kw in keywords:
            if kw in text_lower:
                return tier
    return 1


def _extract_name(text: str) -> str:
    """
    Best-effort name extraction: use first short non-email line.
    """
    for line in text.strip().splitlines():
        line = line.strip()
        if (
            line
            and len(line.split()) <= 5
            and "@" not in line
            and not re.search(r"\d{4}", line)
            and not re.search(r"[:/\\]", line)
        ):
            return line
    return "Unknown"


def score_resume(resume_text: str, jd_text: str, filename: str = "") -> Dict[str, Any]:
    """
    Score a single resume against a job description.

    Returns a dict matching the existing API response shape:
      name, score, status, badgeClass, skills, experience,
      category, score_breakdown, matched_skills, key_gaps
    """
    jd = parse_jd(jd_text)
    resume_skills: Set[str] = set(extract_skills(resume_text))

    required: Set[str] = set(jd["required_skills"])
    preferred: Set[str] = set(jd["preferred_skills"])

    # ── Dimension 1: Required skills ──────────────────────────────────────
    if required:
        req_matched = resume_skills & required
        req_ratio = len(req_matched) / len(required)
    else:
        req_matched = set()
        req_ratio = 1.0  # no requirements = full score

    req_score = round(req_ratio * WEIGHTS["required_skills"])

    # ── Dimension 2: Experience years ─────────────────────────────────────
    resume_years = _extract_years_from_resume(resume_text)
    jd_min_years = jd["min_exp_years"]

    if jd_min_years == 0:
        exp_score = WEIGHTS["experience_years"]
    elif resume_years == 0:
        exp_score = 0
    else:
        exp_ratio = min(resume_years / jd_min_years, 1.0)
        exp_score = round(exp_ratio * WEIGHTS["experience_years"])

    # ── Dimension 3: Preferred skills ─────────────────────────────────────
    if preferred:
        pref_matched = resume_skills & preferred
        pref_ratio = len(pref_matched) / len(preferred)
    else:
        pref_matched = set()
        pref_ratio = 1.0

    pref_score = round(pref_ratio * WEIGHTS["preferred_skills"])

    # ── Dimension 4: Education ────────────────────────────────────────────
    resume_edu = _detect_education_level(resume_text)
    jd_edu = jd["education_level"]

    if resume_edu >= jd_edu:
        edu_score = WEIGHTS["education"]
    elif resume_edu == jd_edu - 1:
        edu_score = round(WEIGHTS["education"] * 0.6)
    else:
        edu_score = 0

    # ── Final score ───────────────────────────────────────────────────────
    final_score = req_score + exp_score + pref_score + edu_score
    final_score = max(0, min(100, final_score))

    # ── Status + badge ────────────────────────────────────────────────────
    if final_score >= 80:
        status = "Shortlist"
        badge_class = "badge-success"
    elif final_score >= 60:
        status = "Review"
        badge_class = "badge-warning"
    else:
        status = "Reject"
        badge_class = "badge-danger"

    # ── Gap analysis ──────────────────────────────────────────────────────
    key_gaps = list(sorted(required - resume_skills))[:5]
    all_matched = list(sorted(req_matched | pref_matched))

    # ── Experience summary string ─────────────────────────────────────────
    if resume_years > 0:
        exp_summary = f"{resume_years} years experience"
    else:
        exp_summary = "Experience not specified"

    # ── Category detection (simple rule-based) ───────────────────────────
    category = _detect_category(resume_skills | set(jd["all_skills"]))

    # ── Candidate name ────────────────────────────────────────────────────
    name = _extract_name(resume_text) or filename

    return {
        "name":       name,
        "score":      final_score,
        "status":     status,
        "badgeClass": badge_class,
        "skills":     sorted(resume_skills & (required | preferred))[:4],
        "experience": exp_summary,
        "category":   category,
        "score_breakdown": {
            "required_skills":  req_score,
            "experience_years": exp_score,
            "preferred_skills": pref_score,
            "education":        edu_score,
        },
        "matched_skills": all_matched,
        "key_gaps":        key_gaps,
    }


def _detect_category(skills: Set[str]) -> str:
    """Simple rule-based domain detection from skill set."""
    it_skills = {
        "python", "javascript", "java", "react", "node.js", "docker",
        "kubernetes", "aws", "machine learning", "sql", "git",
    }
    finance_skills = {"financial modeling", "excel", "accounting", "bloomberg"}
    healthcare_skills = {"healthcare", "hl7", "fhir", "clinical"}

    it_overlap = len(skills & it_skills)
    fin_overlap = len(skills & finance_skills)
    health_overlap = len(skills & healthcare_skills)

    best = max(it_overlap, fin_overlap, health_overlap)
    if best == 0:
        return "OTHER"
    if best == it_overlap:
        return "INFORMATION-TECHNOLOGY"
    if best == fin_overlap:
        return "FINANCE"
    return "HEALTHCARE"

"""
scorer.py

Weighted ATS scoring engine.
Takes a resume's extracted data and a parsed JD and returns a score 0-100.

Weights (Total: 100):
  required_skills      → 30 pts
  experience_years     → 20 pts
  preferred_skills     → 15 pts
  education            → 10 pts
  job_title_match      → 10 pts
  certifications       → 8 pts
  keyword_density      → 4 pts
  resume_completeness  → 3 pts
"""

from typing import List, Dict, Set, Any

from .jd_parser import parse_jd, EDU_TIERS
import re
from rapidfuzz import fuzz
from services.ai_service import parse_resume_against_jd

WEIGHTS = {
    "required_skills": 30,
    "experience_years": 20,
    "preferred_skills": 15,
    "education": 10,
    "job_title_match": 10,
    "certifications": 8,
    "keyword_density": 4,
    "resume_completeness": 3,
}


# Heuristic extractors replaced by LLM parsing


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


def _score_job_title(candidate_title: str, jd_title: str) -> int:
    """
    Compare the candidate's latest job title against jd_title using rapidfuzz.
    """
    if not jd_title:
        return 10

    if not candidate_title:
        candidate_title = ""

    ratio = fuzz.partial_ratio(candidate_title.lower(), jd_title.lower())
    if ratio >= 75:
        return 10
    elif ratio >= 55:
        return 6
    return 0


# _score_certifications replaced by LLM parsing


def _score_keyword_density(resume_text: str, jd_text: str) -> int:
    """
    Tokenise jd_text into lowercase words, filter out stopwords.
    Score = round(ratio * 4), capped at 4.
    """
    stopwords = {
        "and", "or", "the", "a", "an", "in", "of", "to", "for", "with", "on", "at",
        "is", "are", "be", "that", "this", "we", "you", "your", "our", "as", "by",
        "from", "have", "will", "must", "should", "can", "who", "which", "it",
        "its", "not", "all", "any", "their", "they", "them", "also", "well",
        "more", "other", "such", "per", "etc"
    }
    
    # Extract unique words of length >= 4 from JD
    jd_words = re.findall(r"\b\w{4,}\b", jd_text.lower())
    unique_jd_words = {w for w in jd_words if w not in stopwords}
    
    if not unique_jd_words:
        return 4
    
    resume_text_lower = resume_text.lower()
    matched = sum(1 for word in unique_jd_words if word in resume_text_lower)
    
    ratio = matched / len(unique_jd_words)
    score = round(ratio * 4)
    return min(score, 4)


def _score_resume_completeness(resume_text: str) -> int:
    """
    Count total words in resume_text for completeness scoring.
    """
    word_count = len(resume_text.split())
    if word_count >= 300:
        return 3
    elif word_count >= 150:
        return 2
    elif word_count >= 50:
        return 1
    return 0


def score_resume(
    resume_text: str,
    jd_text: str,
    filename: str = "",
    structured_jd: Dict[str, str] | None = None,
) -> Dict[str, Any]:
    """
    Score a single resume against a job description.

    Returns a dict with:
      name, score, status, badgeClass, skills, experience,
      category, score_breakdown, matched_skills, key_gaps
    """
    # ── Build full JD text from all available fields ──────────────────────
    if structured_jd:
        sections = []
        if structured_jd.get("requiredSkills"):
            sections.append(f"Required Skills: {structured_jd['requiredSkills']}")
        if structured_jd.get("keyResponsibilities"):
            sections.append(f"Key Responsibilities: {structured_jd['keyResponsibilities']}")
        if structured_jd.get("preferredQualifications"):
            sections.append(f"Preferred Qualifications: {structured_jd['preferredQualifications']}")
        if structured_jd.get("educationalBackground"):
            sections.append(f"Educational Background: {structured_jd['educationalBackground']}")
        if sections:
            jd_text = "\n".join(sections) + "\n\n" + jd_text

    jd = parse_jd(jd_text)
    
    llm_parsed_data = parse_resume_against_jd(resume_text, jd_text)
    if not llm_parsed_data:
        llm_parsed_data = {
            "total_years_experience": 0,
            "education_tier": 1,
            "latest_job_title": "",
            "skills_found": [],
            "certifications_found": []
        }

    resume_skills: Set[str] = set(llm_parsed_data.get("skills_found", []))

    required: Set[str] = set(jd["required_skills"])
    preferred: Set[str] = set(jd["preferred_skills"])

    # 1. Required skills (30 pts)
    if required:
        req_matched = resume_skills & required
        req_ratio = len(req_matched) / len(required)
    else:
        req_matched = set()
        req_ratio = 1.0
    req_score = round(req_ratio * WEIGHTS["required_skills"])

    # 2. Experience years (20 pts)
    resume_years = max(0, llm_parsed_data.get("total_years_experience") or 0)
    jd_min_years = jd["min_exp_years"]
    if jd_min_years == 0:
        exp_score = WEIGHTS["experience_years"]
    elif resume_years == 0:
        exp_score = 0
    else:
        exp_ratio = min(resume_years / jd_min_years, 1.0)
        exp_score = round(exp_ratio * WEIGHTS["experience_years"])

    # 3. Preferred skills (15 pts)
    if preferred:
        pref_matched = resume_skills & preferred
        pref_ratio = len(pref_matched) / len(preferred)
    else:
        pref_matched = set()
        pref_ratio = 1.0
    pref_score = round(pref_ratio * WEIGHTS["preferred_skills"])

    # 4. Education (10 pts)
    resume_edu = llm_parsed_data.get("education_tier") or 1
    jd_edu = jd["education_level"]
    if resume_edu >= jd_edu:
        edu_score = WEIGHTS["education"]
    elif resume_edu == jd_edu - 1:
        edu_score = round(WEIGHTS["education"] * 0.6)
    else:
        edu_score = 0

    # 5. Job Title Match (10 pts)
    title_score = _score_job_title(llm_parsed_data.get("latest_job_title", ""), jd["job_title"])

    # 6. Certifications (8 pts)
    jd_certs = set(jd.get("certifications", []))
    resume_certs = set(c.lower() for c in llm_parsed_data.get("certifications_found", []))
    
    if not jd_certs:
        cert_score = 8
    else:
        matched_certs = len(jd_certs & resume_certs)
        cert_score = min(round((matched_certs / len(jd_certs)) * 8), 8)

    # 7. Keyword Density (4 pts)
    density_score = _score_keyword_density(resume_text, jd_text)

    # 8. Resume Completeness (3 pts)
    comp_score = _score_resume_completeness(resume_text)

    # ── Final score (sum of all 8 components, clamped 0-100) ───────────────
    final_score = (
        req_score + exp_score + pref_score + edu_score +
        title_score + cert_score + density_score + comp_score
    )
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
    exp_summary = f"{resume_years} years experience" if resume_years > 0 else "Experience not specified"

    # ── Category detection ────────────────────────────────────────────────
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
            "required_skills":     req_score,
            "experience_years":    exp_score,
            "preferred_skills":    pref_score,
            "education":           edu_score,
            "job_title_match":     title_score,
            "certifications":      cert_score,
            "keyword_density":     density_score,
            "resume_completeness": comp_score,
        },
        "matched_skills": all_matched,
        "key_gaps":        key_gaps,
    }

"""
jd_parser.py

Parses a Job Description text into structured requirements:
  - required_skills:   skills the JD explicitly requires
  - preferred_skills:  skills listed as nice-to-have
  - min_exp_years:     minimum years of experience required (int)
  - education_level:   required education tier (int 1-5)
  - job_title:         detected job title (str)
  - certifications:    list of detected certifications (list)
  - all_skills:        union of required + preferred skills

Education tiers: 1=any, 2=diploma, 3=bachelor, 4=master, 5=phd
"""

import re
from typing import List, Dict, Set, Any


def parse_jd(jd_text: str) -> Dict[str, Any]:
    """
    Parse a job description and return structured requirements using Groq AI.

    Returns a dict with keys:
      required_skills, preferred_skills, all_skills,
      min_exp_years, education_level, job_title, certifications
    """
    from services.ai_service import parse_job_description
    
    parsed = parse_job_description(jd_text)
    if not parsed:
        parsed = {
            "required_skills": [],
            "preferred_skills": [],
            "min_exp_years": 0,
            "education_level": 1,
            "job_title": "",
            "certifications": []
        }
        
    req_skills = parsed.get("required_skills", [])
    pref_skills = parsed.get("preferred_skills", [])
    
    # Merge into all_skills safely avoiding dupes
    all_skills = list(set(req_skills + pref_skills))
    
    return {
        "required_skills": sorted(req_skills),
        "preferred_skills": sorted(pref_skills),
        "all_skills": sorted(all_skills),
        "min_exp_years": parsed.get("min_exp_years", 0),
        "education_level": parsed.get("education_level", 1),
        "job_title": parsed.get("job_title", ""),
        "certifications": parsed.get("certifications", []),
    }

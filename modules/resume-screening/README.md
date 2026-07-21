# 🔍 Resume Screening Module (Weighted ATS Engine)

The **Resume Screening Module** is the core of the HireAI platform. It uses a **Weighted ATS Engine** to calculate the compatibility of a candidate's resume with a given job description.

---

## 🚀 Overview

The screening module automates the initial evaluation of resumes, reducing hundreds of hours of manual review to matter of seconds. It uses **Groq AI (Llama 3.1)** to extract structured content and then a custom **Weighted Scorer** for the final matching results.

### Key Logic Flow
1.  **Parsing**: Uses `ai_service.py` and `parser_service.py` to extract resume and JD data.
2.  **Analysis**: Deep comparisons are made for skills, experience, education, job titles, and certifications.
3.  **Fuzzy Matching**: Employs `rapidfuzz` for intelligent skill comparison.
4.  **Scoring**: A final score (0-100) is calculated based on weights.

---

## 📊 Scoring Weights (Total: 100)

The final score is composed of several key performance indicators (KPIs), each weighted according to its importance:

| KPI Category | Weight (Pts) | Description |
|---|---|---|
| **Required Skills** | 30 | Fuzzy match between resume skills and JD's required list. |
| **Experience Years** | 20 | Comparison of candidate's total years vs job's minimum requirement. |
| **Preferred Skills** | 15 | Bonus points for matching "nice-to-have" skills. |
| **Education** | 10 | Tier-based matching (e.g., Degree vs Master's vs PhD). |
| **Job Title Match** | 10 | Semantic similarity between candidate's latest title and the JD. |
| **Certifications** | 8 | Check for mandatory or relevant industry certifications. |
| **Keyword Density** | 4 | Comparison of unique term frequency across both documents. |
| **Completeness** | 3 | Evaluation of the overall depth and word count of the resume. |

---

## 🧠 Technical Highlights

### Fuzzy Skill Comparison
Instead of simple string matching, the engine uses **Token Sort Ratio** from `rapidfuzz`. This allows it to match synonyms and variations (e.g., "JavaScript" vs "JS" or "React.js" vs "React") with a default threshold of **80%**.

```python
# Example fuzzy logic from scorer.py
if fuzz.token_sort_ratio(jd_skill.lower(), res_skill.lower()) >= threshold:
    matched.add(jd_skill)
```

### Gap Analysis
Beyond just scoring, the module automatically identifies the **top 5 missing skills** ("key gaps") to help recruiters understand where a candidate might fall short.

---

## 📁 Key Components

- **Scoring Engine**: `backend/services/ats/scorer.py`
- **AI Integration**: `backend/services/ai_service.py`
- **JD Parsing**: `backend/routes/ai_routes.py`

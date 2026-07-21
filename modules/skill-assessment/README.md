# 🧪 Skill Assessment Module

The **Skill Assessment Module** generates and evaluates technical technical tests for candidates, providing an objective, automated way to baseline their technical knowledge.

---

## 🚀 Overview

Instead of static, repetitive tests, the Skill Assessment Module uses **Groq AI (Llama 3.1)** to generate fresh, role-specific multiple-choice questions (MCQs) for every candidate. This ensures that the assessments remain relevant and hard to predict.

### Key Logic Flow
1.  **Role Selection**: The candidate selects their targeted professional role (e.g., Backend Dev, ML Engineer).
2.  **AI Generation**: The backend (`ai_routes.py`) requests 5 unique technical questions from Groq AI.
3.  **Active Test**: The candidate has a 10-minute window to complete the assessment.
4.  **Automatic Scoring**: The system immediately calculates and displays the final score.

---

## 📊 Evaluation Thresholds

Candidates receive a final score (0-100%) and a corresponding recommendation label based on their performance:

| Score Range | Recommendation Label |
|---|---|
| **80 – 100%** | 🏆 Excellent — Recommended for shortlist |
| **60 – 79%** | ✅ Good — Move to interview round |
| **0 – 59%** | ❌ Below threshold — Needs improvement |

---

## 📁 Key Components

- **Frontend View**: `src/views/candidate/SkillAssessmentView.vue`
- **Backend Route**: `/api/generate-assessment` (in `ai_routes.py`)
- **UI Components**: `src/components/AppEmptyState.vue`, `src/components/AppSpinner.vue`
- **Frontend Utility**: `utils/api.js` (`generateAssessment` function)

# 📝 AI Resume Generation Module

The **AI Resume Generation Module** allows candidates to create professional, high-impact resume content with the help of **Groq AI (Llama 3.1)**.

---

## 🚀 Overview

This module leverages Large Language Models (LLMs) to transform simple user inputs into structured, professional experience descriptions, skill summaries, and career objectives. This ensures that every candidate has access to top-tier resume phrasing and formatting.

### Key Capabilities
- **Content Expansion**: Turn bullet points into detailed professional achievements.
- **Role-Based Suggestions**: Get content tailored for specific job titles.
- **Professional Tone**: Ensures the language is concise, action-oriented, and impactful.
- **Direct Firestore Save**: Once generated, resumes are automatically stored to the user's profile.

---

## 🛠️ Implementation Details

### Workflow

1.  **Input**: The user provides a "prompt" and "context" (e.g., job title and key responsibilities).
2.  **API Call**: The prompt is processed by the **Groq AI Service**.
3.  **Refinement**: The AI returns a professional version of the input.
4.  **Integration**: The content is formatted and ready for the candidate’s resume.

### Interaction

- **Backend Route**: `/api/generate-content` (in `ai_routes.py`)
- **Backend Service**: `ai_service.py` (Orchestrates the Groq LLM)
- **Frontend Utility**: `utils/api.js` (`generateContent` function)

---

## 📁 Key Components

- **View**: `src/views/candidate/CandidateProfileView.vue`
- **Logic**: `src/composables/useProfileForm.js`
- **Validators**: `src/utils/resumeValidator.js`

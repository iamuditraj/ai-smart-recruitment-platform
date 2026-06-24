# 🤖 HireAI — AI-Based Smart Recruitment Platform

> An end-to-end AI-powered recruitment platform that automates resume generation, resume screening, skill assessments, job postings, and camera-based mock interview analysis.

---

## 📌 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [ML Model Setup](#ml-model-setup)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Development Methodology](#development-methodology)
- [Team](#team)

---

## About the Project

**HireAI** bridges the gap between job seekers and recruiters using the power of AI. Candidates can generate professional resumes using Gemini AI, upload them, apply for jobs, and practice interview skills. Recruiters can post jobs, screen resumes against a job description, and get AI-ranked candidate profiles — all in one platform.

---

## ✨ Features

### For Candidates
- 📝 **AI Resume Generation** — Generate professional resume content using Google Gemini AI
- 📤 **Resume Upload & Parsing** — Upload a PDF resume and auto-extract structured data (skills, experience, education)
- 💼 **Job Board** — Browse and apply to jobs posted by recruiters
- 🧠 **Skill Assessment** — Take AI-generated technical quizzes tailored to a specific role
- 🎥 **Mock Interview** — AI-powered camera-based interview practice with feedback
- 👤 **Profile Management** — Manage personal profile, bio, and resume

### For Recruiters
- 📋 **Job Posting** — Post jobs with requirements and descriptions
- 📊 **Resume Screening** — Bulk upload resumes, match them against a JD using Gemini AI, and get shortlist/review/reject recommendations
- 👥 **Candidate Dashboard** — View and manage all applications with candidate details
- 🏷️ **AI Scoring** — Candidates scored 0–100% with match badges and skill highlights

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Vue.js 3 (Composition API), Vue Router, Pinia |
| **Backend** | Python, Flask, Flask-CORS |
| **AI / LLM** | Google Gemini API (`google-generativeai`) |
| **Database** | Firebase Firestore (NoSQL) |
| **Auth** | Firebase Auth + Custom JWT (Werkzeug password hashing) |
| **File Parsing** | PyMuPDF (`fitz`), python-docx |
| **ML Model** | scikit-learn (TF-IDF + Logistic Regression) |
| **Storage** | Firestore Base64 encoding (free-tier friendly, max 900KB) |
| **Dev Tools** | Git, Vite, ESLint |

---

## 📁 Project Structure

```
ai-smart-recruitment-platform/
├── backend/                    # Flask API server
│   ├── app.py                  # App entry point
│   ├── routes/
│   │   └── api_routes.py       # All API endpoints
│   ├── services/
│   │   ├── firebase_service.py # Firestore connection
│   │   ├── ai_service.py       # Gemini AI connection
│   │   └── parser_service.py   # PDF/DOCX text extractor
│   ├── .env                    # Environment variables (not committed)
│   ├── .env.example            # Template for env setup
│   ├── requirements.txt        # Python dependencies
│   └── serviceAccountKey.json  # Firebase service account (not committed)
│
├── frontend/                   # Vue.js 3 SPA
│   └── src/
│       ├── views/              # Page-level components
│       │   ├── HomeView.vue
│       │   ├── LoginView.vue
│       │   ├── SignupView.vue
│       │   ├── ProfileView.vue
│       │   ├── DashboardView.vue
│       │   ├── CandidateDashboardView.vue
│       │   ├── ResumeGenerationView.vue
│       │   ├── ResumeScreeningView.vue
│       │   ├── SkillAssessmentView.vue
│       │   ├── MockInterviewView.vue
│       │   ├── BrowseJobsView.vue
│       │   ├── RecruiterJobsView.vue
│       │   └── CandidatesView.vue
│       ├── components/         # Reusable UI components
│       ├── stores/             # Pinia state management
│       ├── router/             # Vue Router config
│       └── utils/              # Helper utilities
│
├── ml_model/                   # ML pipeline (Resume Classifier)
│   ├── preprocess.py           # Data preprocessing + model training
│   ├── datasets/               # Training datasets (Kaggle resume data)
│   ├── models/                 # Saved .pkl model + vectorizer
│   └── requirements.txt        # ML-specific dependencies
│
├── agile/                      # Agile/Scrum documentation
├── docs/                       # Project documentation
├── modules/                    # Feature module specs
├── future-scope.md
└── risks-and-limitations.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** and **npm**
- A **Firebase project** with Firestore enabled
- A **Google Gemini API key**

---

### Backend Setup

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
copy .env.example .env
# Then fill in your API keys in .env

# 5. Place your Firebase service account key
# Download serviceAccountKey.json from Firebase Console
# and place it in the /backend directory

# 6. Run the Flask server
python app.py
```

The backend will start at: `http://localhost:5000`

---

### Frontend Setup

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
```

The frontend will start at: `http://localhost:5173`

---

### ML Model Setup

```bash
# 1. Navigate to ML model directory
cd ml_model

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run preprocessing and training
python preprocess.py
```

Trained model and vectorizer will be saved in `ml_model/models/`.

---

## 🔐 Environment Variables

Create a `.env` file inside the `backend/` directory based on `.env.example`:

```env
GEMINI_API_KEY=your_google_gemini_api_key
FIREBASE_CREDENTIALS_PATH=serviceAccountKey.json
FLASK_ENV=development
```

> ⚠️ Never commit `.env` or `serviceAccountKey.json` to version control.

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/signup` | Register a new user (candidate/recruiter) |
| `POST` | `/api/login` | Login and receive user session |
| `GET/POST` | `/api/profile` | Get or update user profile |
| `POST` | `/api/profile/upload-resume` | Upload PDF resume + auto-parse via Gemini |
| `POST` | `/api/generate-content` | AI-generate resume section content |
| `POST` | `/api/save-resume` | Save structured resume to Firestore |
| `POST` | `/api/analyze` | Bulk resume screening against a JD |
| `POST` | `/api/generate-assessment` | Generate role-specific MCQ quiz via AI |
| `GET/POST` | `/api/jobs` | List all jobs or post a new job |
| `POST` | `/api/jobs/apply` | Apply for a job |
| `GET` | `/api/recruiter/applications` | Get all applications for recruiter's jobs |
| `GET` | `/api/check-db` | Health check — Firestore connectivity |

---

## 📅 Development Methodology

| Field | Details |
|---|---|
| **Methodology** | Agile Scrum |
| **Sprints** | 3 Sprints |
| **Team Size** | 3 Members |
| **Status** | Active Development |

---

## 👥 Team

Built with ❤️ by a team of 3 as part of an Agile-driven academic/capstone project.

---

## 📄 License

This project is for educational purposes. All rights reserved by the team.

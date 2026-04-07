# 🤖 HireAI — AI-Powered Smart Recruitment Platform

> An end-to-end AI-driven recruitment platform that automates resume parsing, weighted ATS screening, skill assessments, job management, and interactive mock interviews.

---

## 📌 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Development Methodology](#development-methodology)
- [Team](#team)

---

## About the Project

**HireAI** is a modern recruitment ecosystem designed to streamline the hiring process for both candidates and recruiters. Leveraging **Groq AI (Llama 3.1)** and a custom **Weighted ATS Engine**, the platform provides deep insights into candidate-job fit, automates repetitive tasks, and offers candidates tools to improve their employability.

---

## ✨ Features

### 👤 For Candidates
- 📝 **AI Resume Hub** — Create, manage, and store multiple resumes (uploaded or AI-generated).
- 📤 **Intelligent Parsing** — Upload PDF resumes and auto-extract structured data (skills, experience, education) using Groq AI.
- 💼 **Job Tracking** — Browse jobs, track application statuses, and see real-time ATS match scores.
- 🧠 **Smart Assessments** — Take AI-generated technical quizzes (MCQs) tailored to specific roles to validate your skills.
- 🎥 **Mock Interviews** — Practice with a camera-based AI interviewer and receive simulated performance feedback.
- 🎯 **ATS Preview** — Preview how your resume matches a job before applying.

### 💼 For Recruiters
- 📋 **Job Lifecycle Management** — Post, edit, and manage job listings with detailed requirements.
- 📊 **Advanced ATS Screening** — Bulk analyze resumes against JDs with a weighted scoring logic (Skills, Experience, Education, etc.).
- 👥 **Candidate Dashboard** — View and manage all applications with AI-ranked candidate profiles and match badges.
- 🏷️ **Fuzzy Skill Matching** — Intelligent skill comparison using `rapidfuzz` to account for variations in terminology.
- 🔍 **Gap Analysis** — Automatically identify missing skills and requirements for each candidate.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Vue.js 3 (Composition API), Pinia, Vue Router, Vanilla CSS |
| **Backend** | Python, Flask, Flask-CORS |
| **AI / LLM** | Groq AI API (`llama-3.1-8b-instant`) |
| **ATS Engine** | Weighted Analysis + `rapidfuzz` (Fuzzy Matching) |
| **Database** | Firebase Firestore (NoSQL) |
| **Auth** | Firebase Auth (Lookup) + Custom JWT Logic (`Werkzeug` hashing) |
| **File Parsing** | PyMuPDF (`fitz`), `python-docx` |
| **Dev Tools** | Vite, ESLint, Git |

---

## 📁 Project Structure

```
ai-smart-recruitment-platform/
├── backend/                    # Flask API server
│   ├── app.py                  # Entry point & Initialization
│   ├── routes/                 # Modularized API routes
│   │   ├── auth_routes.py      # Login & Signup logic
│   │   ├── ai_routes.py        # Groq AI & ATS orchestration
│   │   ├── job_routes.py       # Job lifecycle management
│   │   ├── profile_routes.py   # Candidate & Recruiter profiles
│   │   ├── candidate_routes.py # Candidate-specific actions
│   │   └── recruiter_routes.py # Recruiter Dashboard logic
│   ├── services/
│   │   ├── ai_service.py       # Groq AI integration
│   │   ├── firebase_service.py # Firestore database wrapper
│   │   ├── parser_service.py   # PDF/DOCX text extraction
│   │   └── ats/                # Weighted ATS Scoring Engine
│   │       └── scorer.py       # Core ranking & fuzzy logic
│   ├── requirements.txt        # Python dependencies
│   └── .env.example            # Environment variables template
│
├── frontend/                   # Vue.js 3 SPA
│   ├── src/
│   │   ├── views/              # View components (Candidate/Recruiter/Shared)
│   │   ├── components/         # Reusable UI components
│   │   ├── stores/             # Pinia state management
│   │   ├── assets/             # Main CSS & Styles
│   │   ├── utils/              # API helpers & Validators
│   │   └── router/             # Vue Router configuration
│   └── package.json            # Node dependencies
│
├── modules/                    # Feature specifications & Documentation
└── docs/                       # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** & **npm**
- **Firebase Project** with Firestore enabled
- **Groq AI API Key** (Get it from [Groq Console](https://console.groq.com/))

---

### Backend Setup

1. **Navigate to backend:**
   ```bash
   cd backend
   ```

2. **Setup Virtual Environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # macOS/Linux
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   ```bash
   copy .env.example .env
   # Fill in your GROQ_API_KEY and Firebase paths
   ```

5. **Run the Server:**
   ```bash
   python app.py
   ```
   *The backend starts at `http://localhost:5000`*

---

### Frontend Setup

1. **Navigate to frontend:**
   ```bash
   cd frontend
   ```

2. **Install Dependencies:**
   ```bash
   npm install
   ```

3. **Start Development Server:**
   ```bash
   npm run dev
   ```
   *The frontend starts at `http://localhost:5173`*

---

## 🔐 Environment Variables

Create a `.env` file in the `backend/` directory:

```env
GROQ_API_KEY=your_groq_api_key_here
FIREBASE_SERVICE_ACCOUNT_KEY=firebase/serviceAccountKey.json
FLASK_ENV=development
```

> [!IMPORTANT]
> Never commit `.env` or any `serviceAccountKey.json` files to the repository.

---

## 📡 API Reference (Core)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/signup` | User registration (Candidate/Recruiter) |
| `POST` | `/api/auth/login` | Session authentication |
| `GET/POST` | `/api/profile` | Handle user profile data |
| `POST` | `/api/analyze` | Bulk ATS resume analysis (Recruiter) |
| `POST` | `/api/score-resume` | Individual ATS score calculation |
| `POST` | `/api/generate-content` | AI-generated resume content via Groq |
| `POST` | `/api/generate-assessment` | Generate technical MCQs for a specific role |
| `GET/POST` | `/api/jobs` | Fetch job board or post new job listings |
| `GET/PUT/DEL` | `/api/jobs/<id>` | Manage specific job details |
| `GET` | `/api/profile/resumes` | Retrieve all stored resumes for a candidate |
| `POST` | `/api/jobs/apply` | Submit job application with ATS results |

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

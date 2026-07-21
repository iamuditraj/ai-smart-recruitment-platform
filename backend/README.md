# ⚙️ HireAI — Backend Service

Welcome to the backend of **HireAI**, an AI-driven smart recruitment platform. This service is a **Flask-based REST API** that orchestrates AI resume parsing, weighted ATS scoring, and recruiter workflows.

---

## 🚀 Overview

The backend is responsible for the core intelligence of the platform, including:
- **AI Orchestration**: Direct integration with **Groq AI** for resume parsing and content generation.
- **ATS Engine**: Custom-built, weighted scoring logic for candidate-job matching.
- **Data Persistence**: seamless integration with **Firebase Firestore** for application data.
- **File Processing**: Extraction of text from PDF and DOCX resumes.

---

## 🛠️ Tech Stack

- **Framework**: Flask (Python 3.10+)
- **AI/LLM**: Groq Cloud API (`llama-3.1-8b-instant`)
- **Database**: Firebase Admin SDK (Firestore)
- **Fuzzy Matching**: `rapidfuzz`
- **NLP**: `spacy` (en-core-web-sm)
- **File Parsing**: `pypdf`, `python-docx`
- **Security**: custom JWT-based authentication

---

## 📁 Directory Structure

```
backend/
├── routes/                 # Modular API endpoints
│   ├── auth_routes.py      # User authentication (Login/Signup)
│   ├── ai_routes.py        # AI generation & ATS analysis
│   ├── job_routes.py       # Job postings & management
│   ├── profile_routes.py   # Candidate & Recruiter profiles
│   ├── candidate_routes.py # Candidate-specific features
│   └── recruiter_routes.py # Recruiter Dashboard analytics
├── services/               # Core business logic
│   ├── ai_service.py       # Groq AI prompt engineering & parsing
│   ├── db_helpers.py       # Firestore CRUD helpers
│   ├── firebase_service.py # Firebase initialization
│   ├── parser_service.py   # Resume text extraction logic
│   └── ats/                # Weighted ATS Scoring Engine
│       └── scorer.py       # Core ranking & matching algorithm
├── firebase/               # (Git Ignored) serviceAccountKey holder
├── app.py                  # API entry point & registration
└── requirements.txt        # Python dependencies
```

---

## ⚙️ Backend Setup

### Prerequisites
- **Python 3.10+**
- **pip** and **venv**
- **Firebase Project** with a service account key

### Installation

1.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # macOS/Linux:
    # source .venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

Create a `.env` file in the `backend/` directory:

```env
GROQ_API_KEY=your_api_key_here
FIREBASE_SERVICE_ACCOUNT_KEY=firebase/serviceAccountKey.json
FLASK_ENV=development
```

> [!IMPORTANT]
> Ensure your Firebase service account JSON is placed at `backend/firebase/serviceAccountKey.json`. This path must match your `.env` configuration.

---

## 📡 API Endpoints (Quick Reference)

### Authentication
- `POST /api/auth/signup`: Create a new account.
- `POST /api/auth/login`: Authenticate and receive a session.

### AI & ATS
- `POST /api/analyze`: Bulk analysis of resumes against a job description.
- `POST /api/generate-content`: AI-powered resume content generation.
- `POST /api/generate-assessment`: Role-based technical MCQ generation.

### Jobs & Applications
- `GET /api/jobs`: List all public job openings.
- `POST /api/jobs/apply`: Submit an application with calculated ATS scores.

---

## 🧪 Development

To start the Flask development server:

```bash
python app.py
```

The backend server will live at `http://localhost:5000`.

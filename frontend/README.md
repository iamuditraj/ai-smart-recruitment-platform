# 🎨 HireAI — Frontend

Welcome to the frontend of **HireAI**, an AI-powered smart recruitment platform. This application is built as a modern Single Page Application (SPA) using **Vue.js 3** and **Vite**.

---

## 🚀 Overview

The HireAI frontend provides a seamless, responsive experience for both candidates and recruiters. It handles complex workflows like interactive mock interviews with camera/microphone access, AI-generated technical assessments, and a comprehensive recruiter dashboard for ATS screening.

### Key Features
- **Candidate Hub**: Resume management, job browsing, and application tracking.
- **Recruiter Dashboard**: Job posting, applicant management, and bulk ATS analysis.
- **AI Mock Interview**: Interactive camera-based session with real-time performance feedback.
- **Skill Assessment**: Role-specific technical MCQs generated on-the-fly.

---

## 🛠️ Tech Stack

- **Core**: Vue.js 3 (Composition API)
- **State Management**: Pinia
- **Routing**: Vue Router
- **HTTP Client**: Axios
- **Styling**: Vanilla CSS (Modern CSS variables & Grid/Flexbox)
- **Build Tool**: Vite
- **AI Integration**: Backend-driven Groq AI API

---

## 📁 Project Structure

```
frontend/
├── src/
│   ├── views/          # Page components (Candidate, Recruiter, Shared)
│   ├── components/     # Reusable UI components (Modals, Cards, Spinners)
│   ├── stores/         # Pinia global state (Auth, Jobs)
│   ├── assets/         # Global styles (index.css) and static images
│   ├── utils/          # API services, formatters, and validators
│   ├── router/         # Application routing configuration
│   └── App.vue         # Root component
├── public/             # Static assets (Favicon, robots.txt)
├── index.html          # HTML entry point
├── vite.config.js      # Vite configuration
└── package.json        # Dependencies and scripts
```

---

## ⚙️ Project Setup

### Prerequisites
- **Node.js**: v18 or higher
- **npm**: v9 or higher

### Installation

```bash
npm install
```

### Development

Start the development server with hot-reload:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`.

### Production

Compile and minify for production:

```bash
npm run build
```

### Code Quality

Run ESLint to check for code quality:

```bash
npm run lint
```

---

## 🎨 Design System

The project uses a custom design system defined in `src/assets/index.css`.
- **Colors**: Deep indigo/violet theme with success/warning/danger status colors.
- **Components**: Pre-styled cards, buttons, and inputs for consistency.
- **Layout**: Mobile-responsive grid system with a sidebar-based dashboard layout.

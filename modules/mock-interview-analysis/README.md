# 🎥 Mock Interview Analysis Module

The **Mock Interview Analysis Module** provides candidates with an AI-powered simulation of a technical interview, capturing real-time performance indicators and generating a comprehensive post-session report.

---

## 🚀 Overview

The mock interview is designed to provide candidates with a safe space to practice their communication skills and technical explanations. It simulates the high-pressure environment of a real interview and gives immediate, actionable feedback.

### Key Workflow
- **Setup**: Ensures camera and microphone permissions are active.
- **Active Session**: A series of 5 dynamically generated questions are presented to the candidate.
- **Real-time Monitoring**: The module simulates active metrics during the session.
- **Performance Report**: A structured analysis of communication, sentiment, and technical accuracy.

---

## 📊 Performance Metrics

| Metric | Analysis Type | Description |
|---|---|---|
| **Eye Tracking** | Real-time Overlay | Monitors gaze patterns to ensure consistent maintainance of eye contact. |
| **Speech Rate** | Live Monitor | Calculates words-per-minute (WPM) to help avoid speaking too fast or slow. |
| **Confidence Level** | AI Sentiment | Evaluates tone of voice and posture to estimate overall candidate confidence. |
| **Sentiment Analysis** | Post-Session | Categorizes responses into Enthusiastic, Professional, and Empathetic. |

---

## 📁 Key Components

- **Frontend View**: `src/views/candidate/MockInterviewView.vue`
- **UI Components**: `src/components/PageHeader.vue`, `src/components/AppSpinner.vue`
- **AI Backend**: `ai_service.py` (Used for future response analysis)

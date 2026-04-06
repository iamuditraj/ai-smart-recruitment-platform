<template>
  <div class="mock-interview">
    <div class="content-area">
      <!-- ====== Header ====== -->
      <PageHeader
        title="AI Mock Interview"
        subtitle="Practice with our AI interviewer and receive real-time feedback on your performance"
      />

      <!-- ====== STAGE 0: Setup & Intro ====== -->
      <div v-if="stage === 'setup'" class="setup-container card animate-fade-in-up">
        <div class="setup-layout">
          <div class="setup-text">
            <h2 class="subsection-title">Prepare for your Session</h2>
            <p>Our AI will ask you 5 questions based on your profile and the role you're targeting. To begin, please ensure:</p>
            <ul class="setup-list">
              <li><span class="setup-check">✓</span> You are in a well-lit and quiet room.</li>
              <li><span class="setup-check">✓</span> Your camera and microphone are working.</li>
              <li><span class="setup-check">✓</span> You are ready to speak clearly and confidently.</li>
            </ul>
            <div class="setup-actions">
              <button class="btn btn-primary btn-lg" @click="startInterview" :disabled="!isMediaReady">
                {{ isMediaReady ? 'Start AI Interview' : 'Initializing Media...' }}
              </button>
            </div>
          </div>
          <div class="setup-preview">
            <div class="video-window">
              <video ref="setupVideo" autoplay muted playsinline class="preview-video"></video>
              <div v-if="!isMediaReady" class="video-overlay">
                <AppSpinner size="sm" />
                <span>Accessing Camera...</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ====== STAGE 1: Active Interview ====== -->
      <div v-else-if="stage === 'active'" class="interview-container animate-fade-in">
        <div class="interview-layout">

          <!-- Question Panel -->
          <div class="question-panel card">
            <div class="interview-progress">
              <span class="progress-label">Question {{ currentQuestionIndex + 1 }} of {{ questions.length }}</span>
              <div class="progress-bar-outer">
                <div class="progress-bar-inner" :style="`width: ${((currentQuestionIndex + 1) / questions.length) * 100}%`"></div>
              </div>
            </div>

            <div class="ai-prompt-box">
              <div class="ai-avatar">✨</div>
              <div class="question-content">
                <h3 v-if="!isTransitioning" class="current-question animate-fade-in">{{ questions[currentQuestionIndex] }}</h3>
                <div v-else class="question-skeleton"></div>
              </div>
            </div>

            <div class="recording-controls">
              <div class="rec-status" :class="{ 'rec-active': true }">
                <span class="rec-dot"></span>
                LIVE ANALYSIS ACTIVE
              </div>
              <button class="btn btn-primary" @click="nextQuestion">
                {{ currentQuestionIndex === questions.length - 1 ? 'Finish Interview' : 'Next Question' }}
              </button>
            </div>
          </div>

          <!-- Video Panel -->
          <div class="video-panel">
            <div class="main-video-box card">
              <video ref="interviewVideo" autoplay muted playsinline class="active-video"></video>

              <!-- Real-time AI Overlays (Mock) -->
              <div class="ai-overlay ai-eye-track">
                <div class="ai-tooltip">👁️ Eye Contact: Good</div>
              </div>

              <div class="live-metrics">
                <div class="metric">
                  <span class="metric-label">Speech Rate</span>
                  <div class="metric-bar"><div class="metric-fill" style="width: 70%;"></div></div>
                </div>
                <div class="metric">
                  <span class="metric-label">Confidence</span>
                  <div class="metric-bar"><div class="metric-fill" style="width: 85%;"></div></div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- ====== STAGE 2: Analysis & Report ====== -->
      <div v-else-if="stage === 'analysis'" class="analysis-container animate-fade-in-up">
        <div class="report-header card">
          <div class="report-brief">
            <div class="report-badge">SESSION COMPLETE</div>
            <h2 class="report-title">Interview Performance Report</h2>
            <p class="report-subtitle">Analyzed on {{ new Date().toLocaleDateString() }} · 5 Questions Attempted</p>
          </div>
          <div class="overall-score-box">
            <span class="score-label">Overall Match</span>
            <span class="score-value gradient-text">88%</span>
          </div>
        </div>

        <div class="analysis-grid">
          <!-- Main Metrics -->
          <div class="card metric-card">
            <h3>Communication Score</h3>
            <div class="big-score">A-</div>
            <p class="metric-desc">You showed excellent verbal clarity and maintained steady eye contact throughout the session.</p>
            <div class="metric-sub-list">
              <div class="sub-metric"><span>Fluency</span> <span class="v-badge badge-success">High</span></div>
              <div class="sub-metric"><span>Vocabulary</span> <span class="v-badge badge-primary">Professional</span></div>
              <div class="sub-metric"><span>Confidence</span> <span class="v-badge badge-success">85%</span></div>
            </div>
          </div>

          <!-- Key Learnings -->
          <div class="card sentiment-card">
            <h3>AI Sentiment Analysis</h3>
            <div class="sentiment-bars">
              <div class="sent-row">
                <label>Enthusiasm</label>
                <div class="sent-bar-bg"><div class="sent-bar-fill" style="width: 90%; background: var(--clr-primary);"></div></div>
              </div>
              <div class="sent-row">
                <label>Professionalism</label>
                <div class="sent-bar-bg"><div class="sent-bar-fill" style="width: 82%; background: #10b981;"></div></div>
              </div>
              <div class="sent-row">
                <label>Empathy</label>
                <div class="sent-bar-bg"><div class="sent-bar-fill" style="width: 65%; background: #fbbf24;"></div></div>
              </div>
            </div>
          </div>

          <!-- Feedback -->
          <div class="card feedback-card full-width">
            <h3 class="mb-4">Personalized Recommendations</h3>
            <div class="feedback-grid">
              <div class="feedback-item">
                <div class="fb-icon">🎯</div>
                <div class="fb-content">
                  <h4>Strong Technical Anchoring</h4>
                  <p>You correctly used industry-specific terms like "TF-IDF" and "Lifecycle Hooks" which improves your authority score.</p>
                </div>
              </div>
              <div class="feedback-item">
                <div class="fb-icon">💡</div>
                <div class="fb-content">
                  <h4>Watch Your Pace</h4>
                  <p>You tend to speak faster when discussing complex projects. Try to pause for 1-2 seconds between key points.</p>
                </div>
              </div>
              <div class="feedback-item">
                <div class="fb-icon">🚀</div>
                <div class="fb-content">
                  <h4>Improve Closing Statements</h4>
                  <p>Your answers were technically sound but could benefit from a stronger "Impact Statement" at the end of each response.</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="analysis-actions">
          <button class="btn btn-outline" @click="resetInterview">Retake Session</button>
          <button class="btn btn-primary" @click="$router.push('/dashboard')">Back to Dashboard</button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import PageHeader from '@/components/PageHeader.vue'
import AppSpinner from '@/components/AppSpinner.vue'

const stage = ref('setup') // 'setup' | 'active' | 'analysis'
const isMediaReady = ref(false)
const setupVideo = ref(null)
const interviewVideo = ref(null)
const currentQuestionIndex = ref(0)
const isTransitioning = ref(false)

const questions = [
  "Can you start by introducing yourself and your background in software development?",
  "Technical skills aside, how do you approach solving a problem when you encounter a significant roadblock?",
  "Tell me about a time you had a conflict with a team member. How did you handle it?",
  "Where do you see yourself professionally in the next three to five years?",
  "Finally, why should we hire you for this role instead of other highly qualified candidates?"
]

let mediaStream = null

async function initMedia() {
  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    isMediaReady.value = true
    if (setupVideo.value) {
      setupVideo.value.srcObject = mediaStream
    }
  } catch (err) {
    console.error('Error accessing media devices:', err)
    alert('Could not access camera/microphone. Please check permissions.')
  }
}

function startInterview() {
  stage.value = 'active'
  nextTick(() => {
    if (interviewVideo.value && mediaStream) {
      interviewVideo.value.srcObject = mediaStream
    }
  })
}

function nextQuestion() {
  if (currentQuestionIndex.value < questions.length - 1) {
    isTransitioning.value = true
    setTimeout(() => {
      currentQuestionIndex.value++
      isTransitioning.value = false
    }, 400)
  } else {
    finishInterview()
  }
}

function finishInterview() {
  stage.value = 'analysis'
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop())
  }
}

function resetInterview() {
  stage.value = 'setup'
  currentQuestionIndex.value = 0
  initMedia()
}

onMounted(() => {
  initMedia()
})

onUnmounted(() => {
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop())
  }
})
</script>

<style scoped>
.mock-interview {
  min-height: 100vh;
}

/* Setup Stage */
.setup-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0;
  overflow: hidden;
}

.setup-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 480px;
}

.setup-text {
  padding: var(--sp-12);
  display: flex;
  flex-direction: column;
  gap: var(--sp-6);
  background: var(--clr-surface);
}

.setup-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
}

.setup-check {
  color: #10b981;
  font-weight: 800;
  margin-right: 10px;
}

.setup-preview {
  background: #000;
  position: relative;
}

.video-window {
  width: 100%;
  height: 100%;
  position: relative;
}

.preview-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--sp-4);
  color: white;
}

/* Active Interview Stage */
.interview-container {
  max-width: 1200px;
  margin: 0 auto;
}

.interview-layout {
  display: grid;
  grid-template-columns: 420px 1fr;
  gap: var(--sp-6);
  min-height: 600px;
}

.question-panel {
  display: flex;
  flex-direction: column;
  gap: var(--sp-8);
  padding: var(--sp-8);
}

.ai-prompt-box {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--sp-6);
  justify-content: center;
}

.ai-avatar {
  width: 64px;
  height: 64px;
  background: var(--gradient-brand);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  box-shadow: 0 0 30px rgba(99,102,241,0.3);
}

.current-question {
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1.4;
  color: var(--clr-text);
}

.question-skeleton {
  height: 100px;
  width: 100%;
  background: var(--clr-surface-2);
  border-radius: var(--radius-md);
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 0.5; }
  50% { opacity: 0.8; }
  100% { opacity: 0.5; }
}

.recording-controls {
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
}

.rec-status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 0.1em;
  padding: 0.6rem;
  border-radius: var(--radius-full);
  background: rgba(255,255,255,0.05);
}

.rec-active { color: #ef4444; }
.rec-dot {
  width: 8px;
  height: 8px;
  background: currentColor;
  border-radius: 50%;
  box-shadow: 0 0 10px currentColor;
  animation: blink 1s infinite;
}

@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

.video-panel {
  position: relative;
}

.main-video-box {
  width: 100%;
  height: 100%;
  background: #000;
  padding: 0;
  overflow: hidden;
  position: relative;
  border: 1px solid var(--clr-border);
}

.active-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.live-metrics {
  position: absolute;
  bottom: 2rem;
  right: 2rem;
  width: 200px;
  background: rgba(16,20,31,0.8);
  backdrop-filter: blur(10px);
  padding: 1.25rem;
  border-radius: var(--radius-lg);
  border: 1px solid rgba(255,255,255,0.1);
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
}

.metric { display: flex; flex-direction: column; gap: 6px; }
.metric-label { font-size: 0.7rem; font-weight: 700; color: rgba(255,255,255,0.6); text-transform: uppercase; }
.metric-bar { height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; }
.metric-fill { height: 100%; background: var(--clr-primary); border-radius: 2px; }

.ai-overlay {
  position: absolute;
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
}

.ai-eye-track {
  width: 200px;
  height: 100px;
  border: 1px solid rgba(16, 185, 129, 0.4);
  border-radius: 100px;
}

.ai-tooltip {
  position: absolute;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  background: #10b981;
  color: white;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 0.65rem;
  font-weight: 800;
}

/* Analysis Stage */
.analysis-container {
  max-width: 1000px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: var(--sp-6);
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--sp-8) var(--sp-10);
  background: var(--gradient-brand);
  color: white;
  border: none;
}

.report-badge {
  display: inline-block;
  background: rgba(255,255,255,0.2);
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 0.7rem;
  font-weight: 800;
  margin-bottom: var(--sp-3);
  letter-spacing: 0.05em;
}

.report-title { font-size: 1.75rem; font-weight: 800; }
.report-subtitle { opacity: 0.8; font-size: 0.9rem; margin-top: 4px; }

.overall-score-box {
  text-align: right;
  background: white;
  padding: 1.5rem 2rem;
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
}

.score-label { color: var(--clr-text-muted); font-size: 0.8rem; font-weight: 700; text-transform: uppercase; }
.score-value { font-size: 3rem; font-weight: 800; font-family: var(--font-heading); }

.analysis-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--sp-6);
}

.full-width { grid-column: 1 / -1; }

.metric-card .big-score {
  font-size: 4rem;
  font-weight: 800;
  color: var(--clr-primary);
  margin-block: var(--sp-2);
}

.sub-metric {
  display: flex;
  justify-content: space-between;
  padding-block: var(--sp-3);
  border-bottom: 1px solid var(--clr-border);
}

.sent-row {
  margin-bottom: var(--sp-4);
}

.sent-row label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 8px;
}

.sent-bar-bg { height: 8px; background: var(--clr-surface-3); border-radius: 4px; }
.sent-bar-fill { height: 100%; border-radius: 4px; }

.feedback-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--sp-6);
}

.feedback-item {
  display: flex;
  gap: 1rem;
}

.fb-icon { font-size: 1.5rem; flex-shrink: 0; }
.fb-content h4 { font-size: 1rem; font-weight: 700; margin-bottom: 4px; }
.fb-content p { font-size: 0.875rem; color: var(--clr-text-light); line-height: 1.6; }

.analysis-actions {
  display: flex;
  justify-content: center;
  gap: var(--sp-4);
  margin-top: var(--sp-4);
}

@media (max-width: 900px) {
  .setup-layout, .interview-layout, .analysis-grid {
    grid-template-columns: 1fr;
  }
}
</style>

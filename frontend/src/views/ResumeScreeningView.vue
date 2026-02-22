<template>
  <div class="resume-screening section">
    <div class="container">
      <div class="page-header animate-fade-in-up">
        <div>
          <h1 class="page-title">Resume Screening</h1>
          <p class="page-subtitle">Upload resumes and let AI extract, parse, and score candidates</p>
        </div>
      </div>

      <!-- Upload Zone -->
      <div
        class="upload-zone card animate-fade-in-up"
        :class="{ 'upload-zone--active': isDragging, 'upload-zone--has-files': files.length }"
        style="animation-delay:0.1s"
        @dragover.prevent="isDragging = true"
        @dragleave="isDragging = false"
        @drop.prevent="onDrop"
        id="resume-upload-zone"
      >
        <div class="upload-zone__icon animate-float">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="url(#uploadGrad)" stroke-width="1.5">
            <defs>
              <linearGradient id="uploadGrad" x1="0" y1="0" x2="24" y2="24" gradientUnits="userSpaceOnUse">
                <stop stop-color="#6366f1"/><stop offset="1" stop-color="#06b6d4"/>
              </linearGradient>
            </defs>
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
        </div>
        <p class="upload-zone__text">Drag & drop resumes here</p>
        <p class="upload-zone__sub">Supports PDF, DOCX · Max 10MB per file</p>
        <label class="btn btn-outline upload-zone__btn" for="file-input" id="resume-file-label">
          Browse Files
        </label>
        <input
          id="file-input"
          type="file"
          multiple
          accept=".pdf,.docx,.doc"
          class="upload-zone__input"
          @change="onFileChange"
        />
      </div>

      <!-- Job Description -->
      <div class="job-desc-section card animate-fade-in-up" style="animation-delay:0.2s">
        <h2 class="subsection-title">Job Description</h2>
        <p class="subsection-subtitle">Paste the JD to enable AI matching and scoring</p>
        <textarea
          id="job-description-input"
          v-model="jobDescription"
          class="form-input job-desc__textarea"
          placeholder="e.g. We are looking for a Senior Machine Learning Engineer with 3+ years of experience in Python, TensorFlow, and NLP..."
          rows="5"
        ></textarea>
        <button
          class="btn btn-primary"
          id="analyze-btn"
          :disabled="files.length === 0 || !jobDescription.trim()"
          @click="analyze"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          Analyze Resumes ({{ files.length }})
        </button>
      </div>

      <!-- Results -->
      <div v-if="results.length" class="results-section animate-fade-in-up">
        <h2 class="subsection-title">Screening Results</h2>
        <div class="results-list">
          <div v-for="(r, i) in results" :key="i" class="result-card card" :id="`result-${i}`">
            <div class="result-card__rank">
              <span class="rank-badge" :class="i === 0 ? 'top' : ''">{{ i + 1 }}</span>
            </div>
            <div class="result-card__info">
              <div class="result-card__name-row">
                <span class="result-card__name">{{ r.name }}</span>
                <span class="badge" :class="r.badgeClass">{{ r.status }}</span>
              </div>
              <div class="result-card__skills">
                <span v-for="skill in r.skills" :key="skill" class="skill-tag">{{ skill }}</span>
              </div>
              <span class="result-card__exp">{{ r.experience }}</span>
            </div>
            <div class="result-card__score">
              <div class="score-ring">
                <svg viewBox="0 0 36 36" class="score-ring__svg">
                  <path class="score-ring__bg"
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none" stroke="#1f2540" stroke-width="3"/>
                  <path class="score-ring__fill"
                    :style="`stroke-dasharray: ${r.score}, 100; stroke: ${r.score >= 80 ? '#10b981' : r.score >= 60 ? '#f59e0b' : '#ef4444'}`"
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none" stroke-width="3" stroke-linecap="round"/>
                </svg>
                <span class="score-ring__label" :class="r.score >= 80 ? 'high' : r.score >= 60 ? 'mid' : 'low'">
                  {{ r.score }}%
                </span>
              </div>
              <span class="score-ring__text">AI Score</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isDragging = ref(false)
const files = ref([])
const jobDescription = ref('')
const results = ref([])

function onFileChange(e) {
  files.value = Array.from(e.target.files)
}

function onDrop(e) {
  isDragging.value = false
  files.value = Array.from(e.dataTransfer.files)
}

function analyze() {
  // Simulated AI screening results
  results.value = [
    { name: 'Priya_Sharma_Resume.pdf', score: 92, status: 'Shortlist', badgeClass: 'badge-success', skills: ['Python', 'NLP', 'TensorFlow', 'BERT'], experience: '5 years — Senior ML Engineer at TechCorp' },
    { name: 'Arjun_Mehta_Resume.pdf', score: 78, status: 'Review', badgeClass: 'badge-warning', skills: ['Python', 'Scikit-learn', 'SQL'], experience: '3 years — Data Scientist at StartupX' },
    { name: 'Riya_Kapoor_Resume.pdf', score: 85, status: 'Shortlist', badgeClass: 'badge-success', skills: ['PyTorch', 'MLOps', 'Docker', 'AWS'], experience: '4 years — ML Engineer at DataOps Inc.' },
    { name: 'Unknown_Candidate.docx', score: 42, status: 'Rejected', badgeClass: 'badge-danger', skills: ['Excel', 'Word'], experience: '1 year — Intern (unrelated field)' },
  ].slice(0, files.value.length || 4)
}
</script>

<style scoped>
.page-header {
  margin-bottom: var(--sp-8);
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.page-subtitle {
  color: var(--clr-text-muted);
  margin-top: var(--sp-1);
}

/* Upload Zone */
.upload-zone {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--sp-4);
  padding: var(--sp-12) var(--sp-6);
  border: 2px dashed var(--clr-border-hover);
  border-radius: var(--radius-xl);
  background: var(--clr-surface);
  cursor: pointer;
  transition: all var(--transition-base);
  margin-bottom: var(--sp-6);
  text-align: center;
}

.upload-zone--active,
.upload-zone:hover {
  border-color: var(--clr-primary);
  background: rgba(99,102,241,0.05);
}

.upload-zone--has-files {
  border-color: var(--clr-success);
  background: rgba(16,185,129,0.04);
}

.upload-zone__icon {
  background: var(--clr-surface-2);
  width: 80px;
  height: 80px;
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--clr-border-hover);
}

.upload-zone__text {
  font-size: 1.1rem;
  font-weight: 600;
}

.upload-zone__sub {
  font-size: 0.85rem;
  color: var(--clr-text-muted);
}

.upload-zone__btn {
  display: inline-flex;
  gap: var(--sp-2);
}

.upload-zone__input {
  display: none;
}

/* Job Desc */
.job-desc-section {
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
  margin-bottom: var(--sp-8);
}

.subsection-title {
  font-size: 1.2rem;
  font-weight: 700;
}

.subsection-subtitle {
  color: var(--clr-text-muted);
  font-size: 0.875rem;
  margin-top: -0.5rem;
}

.job-desc__textarea {
  resize: vertical;
  min-height: 120px;
}

.btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none !important;
}

/* Results */
.results-section {
  margin-top: var(--sp-8);
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
}

.result-card {
  display: flex;
  align-items: center;
  gap: var(--sp-4);
  padding: var(--sp-4) var(--sp-6);
}

.result-card__rank {
  flex-shrink: 0;
}

.rank-badge {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  background: var(--clr-surface-3);
  border: 1px solid var(--clr-border-hover);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.85rem;
}

.rank-badge.top {
  background: var(--gradient-brand);
  border: none;
  color: white;
}

.result-card__info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--sp-2);
}

.result-card__name-row {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  flex-wrap: wrap;
}

.result-card__name {
  font-weight: 600;
  font-size: 0.95rem;
}

.result-card__skills {
  display: flex;
  gap: var(--sp-2);
  flex-wrap: wrap;
}

.skill-tag {
  background: var(--clr-surface-3);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-full);
  padding: 0.15rem 0.6rem;
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--clr-text-light);
}

.result-card__exp {
  font-size: 0.8rem;
  color: var(--clr-text-muted);
}

.badge-danger {
  background: rgba(239,68,68,0.12);
  color: #fca5a5;
  border: 1px solid rgba(239,68,68,0.25);
}

/* Score Ring */
.result-card__score {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--sp-1);
  flex-shrink: 0;
}

.score-ring {
  position: relative;
  width: 64px;
  height: 64px;
}

.score-ring__svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.score-ring__fill {
  transition: stroke-dasharray 1s ease;
}

.score-ring__label {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 800;
}

.score-ring__label.high { color: #6ee7b7; }
.score-ring__label.mid  { color: #fcd34d; }
.score-ring__label.low  { color: #fca5a5; }

.score-ring__text {
  font-size: 0.72rem;
  color: var(--clr-text-muted);
}

@media (max-width: 600px) {
  .result-card {
    flex-wrap: wrap;
  }
}
</style>

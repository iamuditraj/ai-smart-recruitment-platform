<template>
  <div class="resume-screening">
    <div class="content-area">
      <PageHeader
        title="Resume Screening"
        subtitle="Upload resumes and let AI extract, parse, and score candidates"
      />

      <!-- Upload Zone -->
      <AppDropzone
        inputId="file-input"
        :multiple="true"
        accept=".pdf,.docx,.doc"
        customClass="animate-fade-in-up"
        @files-selected="handleFiles"
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
      </AppDropzone>

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
          :disabled="files.length === 0 || !jobDescription.trim() || isAnalyzing"
          @click="analyze"
        >
          <svg v-if="!isAnalyzing" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <AppSpinner v-else size="sm" />
          {{ isAnalyzing ? 'Analyzing...' : `Analyze Resumes (${files.length})` }}
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

              <!-- Score breakdown (shown if local ATS returned it) -->
              <div v-if="r.score_breakdown && Object.keys(r.score_breakdown).length" class="result-breakdown">
                <span class="breakdown-item">
                  Skills <strong>{{ r.score_breakdown.required_skills ?? '—' }}/40</strong>
                </span>
                <span class="breakdown-sep">·</span>
                <span class="breakdown-item">
                  Exp <strong>{{ r.score_breakdown.experience_years ?? '—' }}/25</strong>
                </span>
                <span class="breakdown-sep">·</span>
                <span class="breakdown-item">
                  Preferred <strong>{{ r.score_breakdown.preferred_skills ?? '—' }}/20</strong>
                </span>
                <span class="breakdown-sep">·</span>
                <span class="breakdown-item">
                  Education <strong>{{ r.score_breakdown.education ?? '—' }}/15</strong>
                </span>
              </div>

              <!-- Key gaps -->
              <div v-if="r.key_gaps && r.key_gaps.length" class="result-gaps">
                <span class="gaps-label">Missing:</span>
                <span v-for="gap in r.key_gaps" :key="gap" class="gap-tag">{{ gap }}</span>
              </div>
            </div>
            <div class="result-card__score">
              <ScoreRing :score="r.score" :size="64" />
              <span class="score-ring__text">ATS Score</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { analyzeResumes } from '@/utils/api'
import PageHeader from '@/components/PageHeader.vue'
import ScoreRing from '@/components/ScoreRing.vue'
import AppSpinner from '@/components/AppSpinner.vue'
import AppDropzone from '@/components/AppDropzone.vue'

const files = ref([])
const jobDescription = ref('')
const results = ref([])
const isAnalyzing = ref(false)

function handleFiles(newFiles) {
  files.value = newFiles
}

async function analyze() {
  if (files.value.length === 0 || !jobDescription.value.trim()) return
  
  isAnalyzing.value = true
  try {
    const formData = new FormData()
    files.value.forEach(file => {
      formData.append('resumes', file)
    })
    formData.append('jobDescription', jobDescription.value)

    const data = await analyzeResumes(formData)
    results.value = data.results
    console.log('✅ Analysis complete:', data.message)
  } catch (error) {
    console.error('❌ Error calling backend:', error)
    alert(error.message || 'Could not connect to the backend. Please make sure it is running.')
  } finally {
    isAnalyzing.value = false
  }
}
</script>

<style scoped>
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

/* Score Ring */
.result-card__score {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--sp-1);
  flex-shrink: 0;
}

.score-ring__text {
  font-size: 0.72rem;
  color: var(--clr-text-muted);
}

.result-breakdown {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.25rem;
  margin-top: 0.4rem;
  font-size: 0.75rem;
  color: var(--clr-text-muted);
}

.breakdown-item strong {
  color: var(--clr-text-light);
  font-weight: 700;
}

.breakdown-sep {
  color: var(--clr-border-hover);
}

.result-gaps {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.3rem;
  margin-top: 0.4rem;
}

.gaps-label {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--clr-danger, #ef4444);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.gap-tag {
  font-size: 0.72rem;
  padding: 0.1rem 0.5rem;
  border-radius: 999px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.25);
  color: #fca5a5;
}

@media (max-width: 600px) {
  .result-card {
    flex-wrap: wrap;
  }
}
</style>

<template>
  <div class="jobs-view">
    <div class="content-area">
      <!-- Header -->
      <div class="jobs-header animate-fade-in-up">
        <div>
          <h1 class="jobs-title">Available Opportunities</h1>
          <p class="jobs-subtitle">Find jobs and internships posted by recruiters</p>
        </div>
        <div class="search-bar card">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input v-model="searchQuery" type="text" placeholder="Search by title, company or role...">
        </div>
      </div>

      <!-- Filters -->
      <div class="filters-row animate-fade-in-up" style="animation-delay: 0.1s">
        <button
          v-for="f in ['All', 'Full-time', 'Internship', 'Remote']"
          :key="f"
          @click="activeFilter = f"
          :class="['filter-btn', { active: activeFilter === f }]"
        >
          {{ f }}
        </button>
      </div>

      <!-- Jobs Grid -->
      <div v-if="isLoading" class="jobs-loading">
        <div class="loader-lg"></div>
        <p>Fetching opportunities...</p>
      </div>

      <div v-else-if="filteredJobs.length === 0" class="empty-state card">
        <h3>No opportunities found</h3>
        <p>Try adjusting your search or filters.</p>
      </div>

      <div v-else class="jobs-grid grid animate-fade-in-up" style="animation-delay: 0.2s">
        <div v-for="job in filteredJobs" :key="job.id" class="job-card card">
          <div class="job-card__header">
            <div class="job-company-logo">{{ job.company[0] }}</div>
            <div class="job-meta">
              <h3 class="job-title">{{ job.title }}</h3>
              <p class="job-company">{{ job.company }}</p>
            </div>
            <div class="job-type-badge">{{ job.type }}</div>
          </div>

          <div class="job-details">
            <div class="detail-item">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              <span>{{ job.location }}</span>
            </div>
            <div class="detail-item">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
              <span>{{ job.salary }}</span>
            </div>
          </div>

          <p class="job-description">{{ job.jobSummary || job.description }}</p>

          <div class="job-actions">
            <button
              v-if="appliedJobIds.has(job.id)"
              class="btn btn-applied w-full"
              disabled
            >
              ✓ Already Applied
            </button>
            <button
              v-else
              @click="initiateApply(job)"
              class="btn btn-primary w-full"
            >
              Apply Now
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Pre-Application Modal Overlay -->
    <Transition name="fade">
      <div v-if="selectedJobForApply" class="modal-overlay" @click.self="closeApplyModal">
        <div class="modal-content apply-modal">
          <button class="modal-close" @click="closeApplyModal">&times;</button>
          
          <div class="modal-split">
            <!-- Left Pane: Job Info -->
            <div class="modal-pane job-info-pane">
              <h2 class="job-title-modal">{{ selectedJobForApply.title }}</h2>
              <p class="subtitle">{{ selectedJobForApply.company }} &bull; {{ selectedJobForApply.location }}</p>
              
              <div class="info-badges mt-2">
                <span class="badge">{{ selectedJobForApply.type }}</span>
                <span class="badge" v-if="selectedJobForApply.salary">{{ selectedJobForApply.salary }}</span>
              </div>
              
              <div class="mt-4 job-desc">
                <h4>Job Description</h4>
                <p>{{ selectedJobForApply.jobSummary || selectedJobForApply.description }}</p>
                <div v-if="selectedJobForApply.requiredSkills">
                  <h4 class="mt-4">Requirements</h4>
                  <p>{{ selectedJobForApply.requiredSkills }}</p>
                </div>
              </div>
            </div>
            
            <!-- Right Pane: Upload/Preview -->
            <div class="modal-pane action-pane">
              <h3 class="font-bold mb-4" style="font-size: 1.25rem;">Application Preview</h3>
              
              <div v-if="!previewResult && !isPreviewing" class="upload-dropzone">
                 <p class="mb-4 text-center">Upload your resume to see your ATS score before applying.</p>
                 <label class="btn btn-outline apply-upload-btn w-full">
                   <span>Select Resume (PDF/DOCX)</span>
                   <input type="file" accept=".pdf,.docx,.doc" class="hidden-input" @change="handlePreviewUpload" />
                 </label>
              </div>
              
              <div v-else-if="isPreviewing" class="scanning-state text-center">
                 <div class="scanner"></div>
                 <p class="mt-4 text-primary font-bold">Scanning against ATS...</p>
                 <p class="text-sm text-muted mt-2">Parsing skills and experience.</p>
              </div>
              
              <div v-else-if="previewResult" class="preview-results">
                  <div class="ats-overall">
                    <div class="ats-score-header">
                      <div class="flex items-center">
                        <span class="ats-score-number" :style="{ color: getScoreColor(previewResult.score) }">{{ previewResult.score }}</span>
                        <span class="ats-score-denom">/100</span>
                      </div>
                      <span :class="['badge', previewResult.badgeClass]">{{ previewResult.status }}</span>
                    </div>
                    <div class="ats-main-bar">
                      <div class="ats-main-bar-fill" :style="{ width: previewResult.score + '%', backgroundColor: getScoreColor(previewResult.score) }"></div>
                    </div>

                    <div class="breakdown-section">
                      <h4 class="breakdown-title">Score Breakdown</h4>
                      <div v-for="dim in scoreDimensions" :key="dim.key" class="breakdown-row">
                        <span class="breakdown-label">{{ dim.label }}</span>
                        <div class="breakdown-bar-track">
                          <div 
                            class="breakdown-bar-fill" 
                            :style="{ 
                              width: ((previewResult.score_breakdown?.[dim.key] || 0) / dim.max * 100) + '%',
                              backgroundColor: getBreakdownColor(previewResult.score_breakdown?.[dim.key] || 0, dim.max)
                            }"
                          ></div>
                        </div>
                        <span class="breakdown-score">{{ previewResult.score_breakdown?.[dim.key] || 0 }}/{{ dim.max }}</span>
                      </div>
                    </div>

                    <div v-if="previewResult.matched_skills?.length" class="skills-section">
                      <h4 class="breakdown-title">Matched Skills</h4>
                      <div class="chips-row">
                        <span v-for="skill in previewResult.matched_skills.slice(0, 6)" :key="skill" class="chip chip-green">{{ skill }}</span>
                        <span v-if="previewResult.matched_skills.length > 6" class="chip chip-more">+{{ previewResult.matched_skills.length - 6 }} more</span>
                      </div>
                    </div>

                    <div v-if="previewResult.key_gaps?.length" class="skills-section">
                      <h4 class="breakdown-title">Missing Keywords</h4>
                      <div class="chips-row">
                        <span v-for="gap in previewResult.key_gaps.slice(0, 5)" :key="gap" class="chip chip-red">{{ gap }}</span>
                      </div>
                    </div>
                  </div>

                  <div class="submit-section">
                    <button class="btn btn-primary w-full" @click="submitFinalApplication" :disabled="isSubmitting">
                      <span v-if="!isSubmitting">Submit Official Application</span>
                      <span v-else class="loader-sm"></span>
                    </button>
                    <button class="btn-text w-full" @click="resetPreview" :disabled="isSubmitting">Upload Different Resume</button>
                  </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Notification -->
    <Transition name="fade">
      <div v-if="toast.show" :class="['toast', toast.type]">
        {{ toast.message }}
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()
const jobs = ref([])
const isLoading = ref(true)
const searchQuery = ref('')
const activeFilter = ref('All')
const selectedJobForApply = ref(null)
const selectedResumeFile = ref(null)
const previewResult = ref(null)
const parsedResumeResult = ref(null)
const isPreviewing = ref(false)
const appliedJobIds = ref(new Set())
const isSubmitting = ref(false)

const scoreDimensions = [
  { key: "required_skills",    label: "Required Skills",    max: 30 },
  { key: "experience_years",   label: "Experience",         max: 20 },
  { key: "preferred_skills",   label: "Preferred Skills",   max: 15 },
  { key: "education",          label: "Education",          max: 10 },
  { key: "job_title_match",    label: "Job Title Match",    max: 10 },
  { key: "certifications",     label: "Certifications",     max:  8 },
  { key: "keyword_density",    label: "Keyword Density",    max:  4 },
  { key: "resume_completeness",label: "Completeness",       max:  3 },
]

const getBreakdownColor = (score, max) => {
  const ratio = max > 0 ? score / max : 0
  if (ratio >= 0.75) return '#10b981'
  if (ratio >= 0.4)  return '#f59e0b'
  return '#ef4444'
}

const getScoreColor = (score) => {
  if (score >= 80) return '#10b981'
  if (score >= 60) return '#f59e0b'
  return '#ef4444'
}

const toast = ref({ show: false, message: '', type: 'success' })

function showToast(message, type = 'success') {
  toast.value = { show: true, message, type }
  setTimeout(() => toast.value.show = false, 3000)
}

async function fetchAppliedJobs() {
  try {
    const email = authStore.user?.email
    if (!email) return
    const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:5001'}/api/candidate/applied-jobs?email=${encodeURIComponent(email)}`)
    const data = await res.json()
    if (data.status === 'success') {
      appliedJobIds.value = new Set(data.applied_job_ids)
    }
  } catch (err) {
    console.error('Fetch applied jobs error:', err)
  }
}

async function fetchJobs() {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:5001'}/api/jobs`)
    const data = await res.json()
    if (data.status === 'success') {
      jobs.value = data.jobs
    }
  } catch (err) {
    console.error('Fetch jobs error:', err)
  } finally {
    isLoading.value = false
  }
}

const filteredJobs = computed(() => {
  return jobs.value.filter(job => {
    const matchesSearch = job.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         job.company.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesFilter = activeFilter.value === 'All' ||
                         (activeFilter.value === 'Remote' && job.location.toLowerCase() === 'remote') ||
                         job.type === activeFilter.value
    return matchesSearch && matchesFilter
  })
})

function initiateApply(job) {
  selectedJobForApply.value = job
  selectedResumeFile.value = null
  previewResult.value = null
  parsedResumeResult.value = null
  isPreviewing.value = false
  isSubmitting.value = false
}

function closeApplyModal() {
  if (isSubmitting.value || isPreviewing.value) return
  selectedJobForApply.value = null
}

function resetPreview() {
  previewResult.value = null
  parsedResumeResult.value = null
  selectedResumeFile.value = null
}

async function handlePreviewUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  selectedResumeFile.value = file;
  isPreviewing.value = true;
  
  try {
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_id', selectedJobForApply.value.id);

    const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:5001'}/api/jobs/preview_score`, {
      method: 'POST',
      body: formData
    })
    
    const data = await res.json()
    if (data.status === 'success') {
      previewResult.value = data.ats_result
      parsedResumeResult.value = data.llm_parsed_resume
    } else {
      showToast(data.message || 'Failed to generate preview', 'error')
      selectedResumeFile.value = null
    }
  } catch (err) {
    console.error(err)
    showToast('Failed to connect to server.', 'error')
    selectedResumeFile.value = null
  } finally {
    isPreviewing.value = false;
    event.target.value = ''; // Reset file input
  }
}

async function submitFinalApplication() {
  if (!selectedResumeFile.value || !selectedJobForApply.value) return;

  isSubmitting.value = true;
  
  try {
    const formData = new FormData();
    formData.append('resume', selectedResumeFile.value);
    formData.append('job_id', selectedJobForApply.value.id);
    formData.append('candidate_email', authStore.user?.email || '');
    if (previewResult.value) {
      formData.append('ats_result', JSON.stringify(previewResult.value));
    }
    if (parsedResumeResult.value) {
      formData.append('llm_parsed_resume', JSON.stringify(parsedResumeResult.value));
    }

    const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:5001'}/api/jobs/apply`, {
      method: 'POST',
      body: formData
    })
    
    const data = await res.json()
    if (data.status === 'success') {
      showToast('Successfully applied! Your ATS score was saved.')
      // Mark this job as applied immediately so the button updates
      appliedJobIds.value = new Set([...appliedJobIds.value, selectedJobForApply.value.id])
      isSubmitting.value = false
      selectedJobForApply.value = null
    } else {
      showToast(data.message || 'Failed to submit application', 'error')
    }
  } catch (err) {
    console.error(err)
    showToast('Failed to apply. Check your connection.', 'error')
  } finally {
    isSubmitting.value = false;
  }
}

onMounted(() => {
  fetchJobs()
  fetchAppliedJobs()
})
</script>

<style scoped>
.jobs-view { min-height: 100vh; background-color: var(--clr-bg); color: var(--clr-text); }
.jobs-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 2rem; margin-bottom: 2rem; }
.jobs-title { font-size: 2rem; font-weight: 800; color: var(--clr-text); }
.jobs-subtitle { color: var(--clr-text-muted); }

.search-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0.75rem 1.25rem;
  width: 100%;
  max-width: 400px;
  background: var(--clr-surface);
}
.search-bar input {
  background: transparent;
  border: none;
  color: var(--clr-text);
  width: 100%;
  outline: none;
}

.filters-row { display: flex; gap: 0.75rem; margin-bottom: 2rem; flex-wrap: wrap; }
.filter-btn {
  padding: 0.5rem 1.25rem;
  border-radius: var(--radius-full);
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  color: var(--clr-text-muted);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}
.filter-btn.active, .filter-btn:hover {
  background: var(--clr-primary);
  color: #ffffff;
  border-color: var(--clr-primary);
}

.jobs-grid { grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; }
.job-card { padding: 1.5rem; display: flex; flex-direction: column; gap: 1rem; background: var(--clr-surface); border: 1px solid var(--clr-border); }
.job-card__header { display: flex; align-items: center; gap: 12px; position: relative; }
.job-company-logo {
  width: 48px;
  height: 48px;
  background: var(--clr-surface-2);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1.2rem;
  color: var(--clr-primary);
  border: 1px solid var(--clr-border);
}
.job-meta { flex: 1; }
.job-title { font-size: 1.1rem; font-weight: 700; color: var(--clr-text); }
.job-company { font-size: 0.9rem; color: var(--clr-text-muted); }
.job-type-badge {
  background: var(--gradient-glow);
  color: var(--clr-primary);
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 700;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.job-details { display: flex; gap: 1rem; }
.detail-item { display: flex; align-items: center; gap: 6px; font-size: 0.85rem; color: var(--clr-text-light); }

.job-description {
  font-size: 0.9rem;
  color: var(--clr-text-muted);
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.w-full { width: 100%; }

.btn-applied {
  background: rgba(16, 185, 129, 0.12);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.25);
  font-weight: 700;
  cursor: default;
  opacity: 0.9;
}

.hidden-input {
  display: none;
}

.apply-upload-btn {
  position: relative;
  overflow: hidden;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0.75rem 1rem;
}

.btn-text {
  background: transparent;
  color: var(--clr-text-muted);
  border: none;
  cursor: pointer;
}
.btn-text:hover {
  text-decoration: underline;
  color: var(--clr-text);
}
.mt-2 { margin-top: 0.5rem; }
.text-sm { font-size: 0.85rem; }

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-content.apply-modal {
  background: var(--clr-bg);
  width: 90%;
  max-width: 900px;
  height: 80vh;
  border-radius: var(--radius-lg);
  position: relative;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-xl);
  overflow: hidden;
}

.modal-close {
  position: absolute;
  top: 1rem; right: 1.5rem;
  background: transparent;
  border: none;
  font-size: 2rem;
  color: var(--clr-text-muted);
  cursor: pointer;
  z-index: 10;
}
.modal-close:hover { color: var(--clr-text); }

.modal-split {
  display: flex;
  flex-direction: row;
  height: 100%;
  overflow: hidden;
}

@media (max-width: 768px) {
  .modal-split {
    flex-direction: column;
    overflow-y: auto;
  }
}

.modal-pane {
  flex: 1;
  padding: 2.5rem;
  overflow-y: auto;
}

.job-info-pane {
  border-right: 1px solid var(--clr-border);
  background: var(--clr-surface);
}

.job-title-modal { font-size: 1.5rem; font-weight: 800; color: var(--clr-text); margin-bottom: 0.25rem; }
.subtitle { color: var(--clr-text-muted); font-size: 0.95rem; margin-bottom: 0.75rem; }

.action-pane {
  background: var(--clr-bg);
  display: flex;
  flex-direction: column;
}

.info-badges { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.badge {
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 700;
  background: var(--clr-surface-2);
  color: var(--clr-text);
}
.badge.badge-success { background: rgba(16, 185, 129, 0.2); color: #10B981; }
.badge.badge-warning { background: rgba(245, 158, 11, 0.2); color: #F59E0B; }
.badge.badge-danger { background: rgba(239, 68, 68, 0.2); color: #EF4444; }

.job-desc {
  font-size: 0.95rem;
  color: var(--clr-text-muted);
  line-height: 1.6;
}
.job-desc h4 { color: var(--clr-text); font-weight: 700; margin-bottom: 0.5rem; }

.upload-dropzone {
  border: 2px dashed var(--clr-border);
  border-radius: var(--radius-md);
  padding: 3rem 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--clr-surface);
  transition: border-color 0.2s;
}
.upload-dropzone:hover { border-color: var(--clr-primary); }

.scanner {
  width: 100%;
  height: 8px;
  background: var(--clr-surface-2);
  border-radius: 4px;
  overflow: hidden;
  position: relative;
  margin-top: 2rem;
}
.scanner::after {
  content: '';
  position: absolute;
  top: 0; left: 0; height: 100%;
  width: 30%;
  background: var(--clr-primary);
  animation: scan 1.5s infinite ease-in-out;
}
@keyframes scan {
  0% { transform: translateX(-100%); }
  50% { transform: translateX(330%); }
  100% { transform: translateX(-100%); }
}

.ats-overall {
  padding: 1rem;
  border-radius: 10px;
  border: 1px solid var(--clr-border);
  margin-bottom: 1rem;
  background: var(--clr-surface);
}

.ats-score-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.ats-score-number {
  font-size: 2.5rem;
  font-weight: 800;
  line-height: 1;
}

.ats-score-denom {
  font-size: 1rem;
  color: var(--clr-text-muted);
  margin-left: 4px;
}

.ats-main-bar {
  height: 8px;
  border-radius: 4px;
  background: var(--clr-surface-3);
  overflow: hidden;
  margin-bottom: 1rem;
}

.ats-main-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.6s ease;
}

.breakdown-section {
  margin-bottom: 1rem;
}

.breakdown-title {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--clr-text-muted);
  margin-bottom: 0.5rem;
}

.breakdown-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.4rem;
}

.breakdown-label {
  font-size: 0.75rem;
  color: var(--clr-text-muted);
  width: 120px;
  flex-shrink: 0;
}

.breakdown-bar-track {
  flex: 1;
  height: 5px;
  background: var(--clr-surface-3);
  border-radius: 3px;
  overflow: hidden;
}

.breakdown-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.breakdown-score {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--clr-text);
  width: 36px;
  text-align: right;
  flex-shrink: 0;
}

.skills-section {
  margin-bottom: 1rem;
}

.chips-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  margin-top: 0.35rem;
}

.chip {
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 600;
}

.chip-green {
  background: rgba(16, 185, 129, 0.12);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.chip-red {
  background: rgba(239, 68, 68, 0.12);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.chip-more {
  background: var(--clr-surface-2);
  color: var(--clr-text-muted);
  border: 1px solid var(--clr-border);
}

.submit-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1rem;
}

.flex { display: flex; }
.justify-between { justify-content: space-between; }
.items-center { align-items: center; }
.gap-1 { gap: 0.25rem; }
.flex-wrap { flex-wrap: wrap; }
.mb-1 { margin-bottom: 0.25rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-4 { margin-bottom: 1rem; }
.mt-3 { margin-top: 0.75rem; }
.mt-4 { margin-top: 1rem; }
.text-center { text-align: center; }
.font-bold { font-weight: 700; }
.font-semibold { font-weight: 600; }
.text-primary { color: var(--clr-primary); }
.p-4 { padding: 1rem; }
.bg-surface { background: var(--clr-surface); }

.jobs-loading { text-align: center; padding: 4rem; }
.loader-lg {
  border: 4px solid var(--clr-surface-2);
  border-top-color: var(--clr-primary);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

.empty-state { text-align: center; padding: 4rem; }

.toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  padding: 1rem 2rem;
  border-radius: var(--radius-md);
  color: white;
  font-weight: 600;
  box-shadow: var(--shadow-lg);
  z-index: 9999;
}
.toast.success { background: var(--clr-success); }
.toast.error { background: var(--clr-danger); }

@keyframes spin { to { transform: rotate(360deg); } }
.fade-enter-active, .fade-leave-active { transition: opacity 0.5s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>

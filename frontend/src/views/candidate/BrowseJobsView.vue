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
      <AppFilterTabs
        v-model="activeFilter"
        :tabs="['All', 'Full-time', 'Internship', 'Remote']"
      />

      <!-- Jobs Grid -->
      <div v-if="isLoading" class="jobs-loading">
        <AppSpinner size="lg" />
        <p>Fetching opportunities...</p>
      </div>

      <AppEmptyState
        v-else-if="filteredJobs.length === 0"
        icon="🔍"
        title="No opportunities found"
        description="Try adjusting your search or filters."
      />

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
    <AppModal :show="!!selectedJobForApply" customClass="apply-modal" @close="closeApplyModal">
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
                  <AtsScorePanel
                    v-if="previewResult"
                    :score="previewResult.score || previewResult.ats_score"
                    :breakdown="previewResult.score_breakdown"
                    :matchedSkills="previewResult.matched_skills"
                    :missingSkills="previewResult.key_gaps || previewResult.missing_skills"
                  />

                  <div class="submit-section">
                    <button class="btn btn-primary w-full" @click="submitFinalApplication" :disabled="isSubmitting">
                      <span v-if="!isSubmitting">Submit Official Application</span>
                      <AppSpinner v-else size="sm" />
                    </button>
                    <button class="btn-text w-full" @click="resetPreview" :disabled="isSubmitting">Upload Different Resume</button>
                  </div>
              </div>
            </div>
          </div>
    </AppModal>

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
import AppModal from '@/components/AppModal.vue'
import { scoreDimensions } from '@/utils/atsConstants'
import { getScoreColor, getBreakdownColor } from '@/utils/uiHelpers'
import AppSpinner from '@/components/AppSpinner.vue'
import AppAlert from '@/components/AppAlert.vue'
import AppEmptyState from '@/components/AppEmptyState.vue'
import AppFilterTabs from '@/components/AppFilterTabs.vue'
import AtsScorePanel from '@/components/AtsScorePanel.vue'

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

/* Modal Integration Styles */
:deep(.apply-modal) {
  max-width: 900px;
}

.modal-split {
  display: flex;
  flex-direction: row;
  gap: 2rem;
}

@media (max-width: 768px) {
  .modal-split {
    flex-direction: column;
  }
}

.modal-pane {
  flex: 1;
}

.job-info-pane {
  padding-right: 1.5rem;
  border-right: 1px solid var(--clr-border);
}

@media (max-width: 768px) {
  .job-info-pane {
    padding-right: 0;
    padding-bottom: 1.5rem;
    border-right: none;
    border-bottom: 1px solid var(--clr-border);
  }
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



.jobs-loading { text-align: center; padding: 4rem; }




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

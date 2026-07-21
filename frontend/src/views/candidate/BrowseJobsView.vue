<template>
  <div class="jobs-view">
    <div class="content-area">
      <!-- Header -->
      <PageHeader 
        title="Available Opportunities" 
        subtitle="Find jobs and internships posted by recruiters">
        <template #actions>
          <div class="search-bar card hide-mobile">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <input v-model="searchQuery" type="text" placeholder="Search by title, company or role...">
          </div>
          <button 
            class="icon-btn hide-desktop" 
            :class="{ 'btn-primary': isMobileSearchVisible }"
            @click="isMobileSearchVisible = !isMobileSearchVisible"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          </button>
        </template>
      </PageHeader>

      <!-- Mobile Search Input (Toggleable) -->
      <Transition name="fade-down">
        <div v-if="isMobileSearchVisible" class="mobile-search hide-desktop animate-fade-in-up">
          <div class="search-bar card">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <input v-model="searchQuery" type="text" placeholder="Search for jobs..." ref="mobileSearchInput">
          </div>
        </div>
      </Transition>

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
        <JobCard v-for="job in filteredJobs" :key="job.id" :job="job" :showCompanyInfo="true">
          <template #actions>
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
          </template>
        </JobCard>
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

              <!-- Tab Switcher -->
              <div v-if="!previewResult && !isPreviewing" class="apply-mode-tabs">
                <button :class="['mode-tab', { active: applyMode === 'upload' }]" @click="switchApplyMode('upload')">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                  Upload File
                </button>
                <button :class="['mode-tab', { active: applyMode === 'hub' }]" @click="switchApplyMode('hub')">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
                  Choose from Hub
                </button>
              </div>
              
              <!-- Upload Mode -->
              <AppDropzone
                v-if="applyMode === 'upload' && !previewResult && !isPreviewing"
                customClass="upload-dropzone"
                inputId="browse-jobs-upload"
                accept=".pdf,.docx,.doc"
                @files-selected="handlePreviewUpload"
              >
                 <p class="mb-4 text-center">Upload your resume to see your ATS score before applying.</p>
                 <label class="btn btn-outline apply-upload-btn w-full" for="browse-jobs-upload">
                   <span>Select Resume (PDF/DOCX)</span>
                 </label>
              </AppDropzone>

              <!-- Hub Mode -->
              <div v-if="applyMode === 'hub' && !previewResult && !isPreviewing" class="hub-resume-section">
                <div v-if="isLoadingHubResumes" class="text-center" style="padding: 2rem 0;">
                  <AppSpinner size="sm" />
                  <p class="text-muted mt-2" style="font-size: 0.85rem;">Loading your resumes...</p>
                </div>
                <div v-else-if="hubResumes.length === 0" class="hub-empty-state">
                  <p>No resumes in your hub yet.</p>
                  <button class="btn btn-outline btn-sm mt-2" @click="switchApplyMode('upload')">
                    Upload one now
                  </button>
                </div>
                <div v-else class="hub-resume-list">
                  <div
                    v-for="resume in hubResumes" :key="resume.id"
                    class="hub-resume-item"
                    :class="{ selected: selectedHubResume?.id === resume.id }"
                    @click="selectHubResume(resume)"
                  >
                    <div class="hub-resume-info">
                      <span class="hub-resume-name">{{ resume.resumeName }}</span>
                      <span class="hub-resume-date">{{ formatHubDate(resume.uploadedAt) }}</span>
                    </div>
                    <span v-if="resume.isDefault" class="hub-default-tag">Default</span>
                    <svg v-if="selectedHubResume?.id === resume.id" class="hub-check-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                  </div>
                  <button
                    v-if="selectedHubResume"
                    class="btn btn-primary w-full mt-4"
                    @click="previewFromHub"
                  >
                    Preview ATS Score
                  </button>
                </div>
              </div>
              
              <div v-if="isPreviewing" class="scanning-state text-center">
                 <div class="scanner"></div>
                 <p class="mt-4 text-primary font-bold">Scanning against ATS...</p>
                 <p class="text-sm text-muted mt-2">Parsing skills and experience.</p>
              </div>
              
              <div v-if="previewResult" class="preview-results">
                  <AtsScorePanel
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
                    <button class="btn-text w-full" @click="resetPreview" :disabled="isSubmitting">Choose Different Resume</button>
                  </div>
              </div>
            </div>
          </div>
    </AppModal>

    <!-- Notification -->
    <AppToast :show="toast.show" :message="toast.message" :type="toast.type" @hide="hideToast" />
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
import AppToast from '@/components/AppToast.vue'
import PageHeader from '@/components/PageHeader.vue'
import JobCard from '@/components/JobCard.vue'
import AppDropzone from '@/components/AppDropzone.vue'
import { getCandidateAppliedJobs, getJobs, previewScore, applyForJob } from '@/utils/api'

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
const isMobileSearchVisible = ref(false)

// Hub resume state
const applyMode = ref('upload')       // 'upload' | 'hub'
const hubResumes = ref([])
const selectedHubResume = ref(null)
const isLoadingHubResumes = ref(false)



import { useToast } from '@/composables/useToast'

const { toast, showToast, hideToast } = useToast()

async function fetchAppliedJobs() {
  try {
    const email = authStore.user?.email
    if (!email) return
    const data = await getCandidateAppliedJobs(email)
    appliedJobIds.value = new Set(data.applied_job_ids)
  } catch (err) {
    console.error('Fetch applied jobs error:', err)
  }
}

async function fetchJobs() {
  try {
    const data = await getJobs()
    jobs.value = data.jobs
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
  applyMode.value = 'upload'
  selectedHubResume.value = null
}

function closeApplyModal() {
  if (isSubmitting.value || isPreviewing.value) return
  selectedJobForApply.value = null
}

function resetPreview() {
  previewResult.value = null
  parsedResumeResult.value = null
  selectedResumeFile.value = null
  selectedHubResume.value = null
}

function switchApplyMode(mode) {
  applyMode.value = mode
  resetPreview()
  if (mode === 'hub') fetchHubResumes()
}

async function fetchHubResumes() {
  if (!authStore.user?.email) return
  isLoadingHubResumes.value = true
  try {
    await authStore.fetchResumes()
    hubResumes.value = authStore.resumes || []
  } catch (err) {
    console.error('Failed to load hub resumes:', err)
  } finally {
    isLoadingHubResumes.value = false
  }
}

function selectHubResume(resume) {
  selectedHubResume.value = selectedHubResume.value?.id === resume.id ? null : resume
}

async function previewFromHub() {
  if (!selectedHubResume.value || !selectedJobForApply.value) return
  isPreviewing.value = true
  try {
    const formData = new FormData()
    formData.append('job_id', selectedJobForApply.value.id)
    formData.append('resume_id', selectedHubResume.value.id)
    formData.append('candidate_email', authStore.user?.email || '')
    const data = await previewScore(formData)
    previewResult.value = data.ats_result
    parsedResumeResult.value = data.llm_parsed_resume
    showToast('ATS Score generated successfully!', 'success')
  } catch (err) {
    console.error(err)
    showToast(err.message || 'Failed to generate preview.', 'error')
  } finally {
    isPreviewing.value = false
  }
}

function formatHubDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

async function handlePreviewUpload(filesOrEvent) {
  const file = filesOrEvent.target ? filesOrEvent.target.files[0] : filesOrEvent[0];
  if (!file) return;

  selectedResumeFile.value = file;
  isPreviewing.value = true;
  
  try {
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_id', selectedJobForApply.value.id);

    const data = await previewScore(formData)
    
    previewResult.value = data.ats_result
    parsedResumeResult.value = data.llm_parsed_resume
    showToast('ATS Score generated successfully!', 'success')
  } catch (err) {
    console.error(err)
    showToast(err.message || 'Failed to connect to server.', 'error')
    selectedResumeFile.value = null
  } finally {
    isPreviewing.value = false;
    event.target.value = ''; // Reset file input
  }
}

async function submitFinalApplication() {
  const hasFile = applyMode.value === 'upload' && selectedResumeFile.value
  const hasHub = applyMode.value === 'hub' && selectedHubResume.value
  if ((!hasFile && !hasHub) || !selectedJobForApply.value) return;

  isSubmitting.value = true;
  
  try {
    const formData = new FormData();
    formData.append('job_id', selectedJobForApply.value.id);
    formData.append('candidate_email', authStore.user?.email || '');

    if (applyMode.value === 'upload') {
      formData.append('resume', selectedResumeFile.value);
    } else {
      formData.append('resume_id', selectedHubResume.value.id);
    }

    if (previewResult.value) {
      formData.append('ats_result', JSON.stringify(previewResult.value));
    }
    if (parsedResumeResult.value) {
      formData.append('llm_parsed_resume', JSON.stringify(parsedResumeResult.value));
    }

    await applyForJob(formData)
    
    showToast('Successfully applied! Your ATS score was saved.')
    // Mark this job as applied immediately so the button updates
    appliedJobIds.value = new Set([...appliedJobIds.value, selectedJobForApply.value.id])
    isSubmitting.value = false
    selectedJobForApply.value = null
  } catch (err) {
    console.error(err)
    showToast(err.message || 'Failed to apply. Check your connection.', 'error')
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

@media (max-width: 480px) {
  .jobs-grid {
    grid-template-columns: 1fr;
  }
}

.mobile-search {
  margin-top: -1rem;
  margin-bottom: 2rem;
}

.mobile-search .search-bar {
  max-width: 100%;
}

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

/* Apply Mode Tabs */
.apply-mode-tabs {
  display: flex;
  gap: 0;
  margin-bottom: 1.25rem;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--clr-border);
}
.mode-tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 0.65rem 0.75rem;
  font-size: 0.85rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  background: var(--clr-surface);
  color: var(--clr-text-muted);
}
.mode-tab:first-child { border-right: 1px solid var(--clr-border); }
.mode-tab.active {
  background: var(--clr-primary);
  color: white;
}
.mode-tab:not(.active):hover {
  background: var(--clr-surface-2);
}

/* Hub Resume Section */
.hub-resume-section {
  min-height: 120px;
}
.hub-empty-state {
  text-align: center;
  padding: 2rem 1rem;
  color: var(--clr-text-muted);
  font-size: 0.9rem;
}
.hub-resume-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 280px;
  overflow-y: auto;
}
.hub-resume-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.85rem 1rem;
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
  background: var(--clr-surface);
}
.hub-resume-item:hover {
  border-color: var(--clr-primary);
  background: rgba(99, 102, 241, 0.04);
}
.hub-resume-item.selected {
  border-color: var(--clr-primary);
  background: rgba(99, 102, 241, 0.08);
  box-shadow: 0 0 0 1px var(--clr-primary);
}
.hub-resume-info {
  flex: 1;
  min-width: 0;
}
.hub-resume-name {
  display: block;
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--clr-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.hub-resume-date {
  font-size: 0.75rem;
  color: var(--clr-text-muted);
}
.hub-default-tag {
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  padding: 2px 8px;
  border-radius: 999px;
  background: rgba(99, 102, 241, 0.12);
  color: var(--clr-primary);
  flex-shrink: 0;
}
.hub-check-icon {
  color: var(--clr-primary);
  flex-shrink: 0;
}

.jobs-loading { text-align: center; padding: 4rem; }
</style>

<template>
  <div class="jobs-view">
    <div class="content-area">
      <!-- Header -->
      <PageHeader 
        title="Available Opportunities" 
        subtitle="Find jobs and internships posted by recruiters">
        <template #actions>
          <div class="search-bar card">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <input v-model="searchQuery" type="text" placeholder="Search by title, company or role...">
          </div>
        </template>
      </PageHeader>

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
              
              <AppDropzone
                v-if="!previewResult && !isPreviewing"
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



.jobs-loading { text-align: center; padding: 4rem; }
</style>

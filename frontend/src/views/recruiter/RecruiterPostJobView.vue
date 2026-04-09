<template>
  <div class="post-job-view">
    <div class="content-area">
      <PageHeader
        :title="isEditMode ? 'Edit Hiring Request' : 'Post a Hiring Request'"
        :subtitle="isEditMode ? 'Update your job opportunity details.' : 'Publish a comprehensive job opportunity to attract top talent.'"
        backTo="/manage-jobs"
        backLabel="Back to Jobs"
      />

      <div class="form-card card animate-fade-in-up" style="animation-delay: 0.1s">
        <div v-if="isLoading" class="loading-state">
          <AppSpinner size="sm" />
          <p>Loading job details...</p>
        </div>
        <form v-else @submit.prevent="submitJob" class="detailed-form">
          <AppAlert v-if="message" :message="message" :type="messageType" />
          
          <!-- Basic Info -->
          <fieldset class="form-section">
            <legend class="section-title">Basic Information</legend>
            <div class="form-grid">
              <div class="form-group">
                <label class="form-label">Job Title <span class="required">*</span></label>
                <input v-model="formData.title" type="text" class="form-input" placeholder="e.g. Senior Frontend Engineer" required>
              </div>
              <div class="form-group">
                <label class="form-label">Company Name <span class="required">*</span></label>
                <input :value="formData.company" type="text" class="form-input disabled" disabled required>
              </div>
              <div class="form-group">
                <label class="form-label">Department / Team</label>
                <input v-model="formData.department" type="text" class="form-input" placeholder="e.g. Engineering">
              </div>
              <div class="form-group">
                <label class="form-label">Location <span class="required">*</span></label>
                <input v-model="formData.location" type="text" class="form-input" placeholder="e.g. San Francisco, CA or Remote" required>
              </div>
            </div>
          </fieldset>

          <div class="divider"></div>

          <!-- Logistics & Comp -->
          <fieldset class="form-section">
            <legend class="section-title">Logistics & Compensation</legend>
            <div class="form-grid">
              <div class="form-group">
                <label class="form-label">Work Arrangement <span class="required">*</span></label>
                <select v-model="formData.workArrangement" class="form-input" required>
                  <option value="On-site">On-site</option>
                  <option value="Hybrid">Hybrid</option>
                  <option value="Remote">Remote</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Employment Type <span class="required">*</span></label>
                <select v-model="formData.type" class="form-input" required>
                  <option value="Full-time">Full-time</option>
                  <option value="Contract">Contract</option>
                  <option value="Internship">Internship</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Experience Level <span class="required">*</span></label>
                <select v-model="formData.experienceLevel" class="form-input" required>
                  <option value="Entry-level">Entry-level</option>
                  <option value="Mid-Level">Mid-Level</option>
                  <option value="Senior">Senior</option>
                  <option value="Lead/Manager">Lead/Manager</option>
                  <option value="Executive">Executive</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Salary Range / Compensation <span class="required">*</span></label>
                <input v-model="formData.salary" type="text" class="form-input" placeholder="e.g. $120,000 - $150,000 + Equity" required>
              </div>
            </div>
          </fieldset>

          <div class="divider"></div>

          <!-- Role Details -->
          <fieldset class="form-section">
            <legend class="section-title">Role Details</legend>
            <div class="form-group mb-4">
              <label class="form-label">Company Overview <span class="required">*</span></label>
              <textarea v-model="formData.companyOverview" class="form-input" rows="3" placeholder="Brief statement about the company's mission..." required></textarea>
            </div>
            <div class="form-group mb-4">
              <label class="form-label">Job Summary <span class="required">*</span></label>
              <textarea v-model="formData.jobSummary" class="form-input" rows="3" placeholder="High-level overview of the position..." required></textarea>
            </div>
            <div class="form-group mb-4">
              <label class="form-label">Key Responsibilities <span class="required">*</span></label>
              <textarea v-model="formData.keyResponsibilities" class="form-input" rows="5" placeholder="Bullet points of daily tasks/responsibilities..." required></textarea>
            </div>
          </fieldset>

          <div class="divider"></div>

          <!-- Qualifications -->
          <fieldset class="form-section">
            <legend class="section-title">Qualifications</legend>
            <div class="form-grid">
              <div class="form-group">
                <label class="form-label">Required Skills (Hard Skills) <span class="required">*</span></label>
                <input v-model="formData.requiredSkills" type="text" class="form-input" placeholder="e.g. Vue.js, Python, Firebase (Comma separated)" required>
              </div>
              <div class="form-group">
                <label class="form-label">Soft Skills <span class="required">*</span></label>
                <input v-model="formData.softSkills" type="text" class="form-input" placeholder="e.g. Communication, Team Leadership (Comma separated)" required>
              </div>
              <div class="form-group" style="grid-column: 1 / -1;">
                <label class="form-label">Educational Background <span class="required">*</span></label>
                <input v-model="formData.educationalBackground" type="text" class="form-input" placeholder="e.g. BS in Computer Science or Equivalent Experience" required>
              </div>
            </div>
            <div class="form-group mt-4">
              <label class="form-label">Preferred Qualifications (Nice-to-Haves)</label>
              <textarea v-model="formData.preferredQualifications" class="form-input" rows="3" placeholder="Additional skills or specific industry experience..."></textarea>
            </div>
          </fieldset>

          <div class="divider"></div>

          <!-- Application Process -->
          <fieldset class="form-section">
            <legend class="section-title">Application Process</legend>
            <div class="form-grid">
              <div class="form-group">
                <label class="form-label">Application Deadline <span class="required">*</span></label>
                <input v-model="formData.applicationDeadline" type="date" class="form-input" required>
              </div>
              <div class="form-group">
                <label class="form-label">Required Documents <span class="required">*</span></label>
                <div class="checkbox-group">
                  <label class="checkbox-label"><input type="checkbox" v-model="formData.reqResume"> Resume / CV</label>
                  <label class="checkbox-label"><input type="checkbox" v-model="formData.reqCoverLetter"> Cover Letter</label>
                  <label class="checkbox-label"><input type="checkbox" v-model="formData.reqPortfolio"> Portfolio/Project Links</label>
                </div>
              </div>
            </div>
          </fieldset>

          <div class="divider"></div>

          <!-- Hiring Pipeline -->
          <fieldset class="form-section">
            <legend class="section-title">Hiring Pipeline</legend>
            <p class="section-desc">Define the stages candidates will progress through. The first round ("Applied") is fixed. Max 10 rounds.</p>

            <div class="pipeline-rounds" id="pipeline-rounds-editor">
              <div
                v-for="(round, idx) in formData.rounds"
                :key="idx"
                class="round-chip"
                :class="{ 'round-chip--locked': idx === 0, 'round-chip--last': idx === formData.rounds.length - 1 }"
              >
                <span class="round-chip__index">{{ idx + 1 }}</span>
                <span class="round-chip__name">{{ round }}</span>
                <button
                  v-if="idx !== 0"
                  type="button"
                  class="round-chip__remove"
                  @click="removeRound(idx)"
                  title="Remove round"
                  :disabled="pipelineLocked"
                >
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
                <!-- Connector arrow -->
                <svg v-if="idx < formData.rounds.length - 1" class="round-connector" width="20" height="14" viewBox="0 0 20 14">
                  <path d="M0 7h14M10 2l5 5-5 5" fill="none" stroke="var(--clr-text-muted)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.4"/>
                </svg>
              </div>
            </div>

            <div v-if="!pipelineLocked && formData.rounds.length < 10" class="add-round-row">
              <input
                v-model.trim="newRound"
                type="text"
                class="form-input add-round-input"
                placeholder="e.g. Portfolio Review"
                maxlength="40"
                @keydown.enter.prevent="addRound"
                id="input-add-round"
              />
              <button type="button" class="btn btn-outline btn-sm" @click="addRound" id="btn-add-round">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                Add Round
              </button>
            </div>
            <p v-if="formData.rounds.length >= 10" class="pipeline-limit-msg">Maximum of 10 rounds reached.</p>
            <p v-if="pipelineLocked" class="pipeline-locked-msg">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              Pipeline is locked because candidate advancement has already begun.
            </p>
          </fieldset>

          <!-- Submit -->
          <div class="submit-section mt-8">
            <button type="submit" class="btn btn-primary submit-btn" :disabled="isPosting">
              <span v-if="!isPosting">{{ isEditMode ? 'Update Job Posting' : 'Publish Job Posting' }}</span>
              <AppSpinner v-else size="sm" />
            </button>
          </div>

        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { getJob, createJob, updateJob } from '@/utils/api'
import AppSpinner from '@/components/AppSpinner.vue'
import AppAlert from '@/components/AppAlert.vue'
import PageHeader from '@/components/PageHeader.vue'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const isPosting = ref(false)
const isLoading = ref(false)
const message = ref('')
const messageType = ref('success')

const isEditMode = computed(() => !!route.params.id)

const fallbackCompany = authStore.user?.companyName || authStore.user?.name || 'Recruiting Company'

const formData = ref({
  title: '',
  department: '',
  company: fallbackCompany,
  location: authStore.user?.location || '',
  workArrangement: 'Remote',
  type: 'Full-time',
  experienceLevel: 'Mid-Level',
  salary: '',
  companyOverview: authStore.user?.companyDescription || '',
  jobSummary: '',
  keyResponsibilities: '',
  requiredSkills: '',
  softSkills: '',
  educationalBackground: '',
  preferredQualifications: '',
  applicationDeadline: '',
  reqResume: true,
  reqCoverLetter: false,
  reqPortfolio: false,
  recruiter_email: authStore.user?.email || '',
  rounds: ['Applied', 'Screening', 'Technical', 'HR', 'Hired'],
})

const newRound = ref('')
const pipelineLocked = ref(false)

function addRound() {
  const name = newRound.value.trim()
  if (!name || formData.value.rounds.length >= 10) return
  const dup = formData.value.rounds.some(r => r.toLowerCase() === name.toLowerCase())
  if (dup) return
  formData.value.rounds.push(name)
  newRound.value = ''
}

function removeRound(idx) {
  if (idx === 0 || pipelineLocked.value) return
  formData.value.rounds.splice(idx, 1)
}

function goBack() {
  router.push('/manage-jobs')
}

async function fetchJobDetails() {
  isLoading.value = true
  try {
    const data = await getJob(route.params.id)
    const job = data.job
    // Populate form data
    Object.keys(formData.value).forEach(key => {
      if (job[key] !== undefined) {
        formData.value[key] = job[key]
      }
    })
    // Map back required documents list to checkboxes
    if (job.requiredDocumentsList && Array.isArray(job.requiredDocumentsList)) {
      formData.value.reqResume = job.requiredDocumentsList.includes('Resume/CV')
      formData.value.reqCoverLetter = job.requiredDocumentsList.includes('Cover Letter')
      formData.value.reqPortfolio = job.requiredDocumentsList.includes('Portfolio')
    }
    // Pipeline rounds
    if (job.rounds && Array.isArray(job.rounds)) {
      formData.value.rounds = job.rounds
    }
    pipelineLocked.value = (job.current_round_index || 0) > 0
  } catch (err) {
    console.error('Fetch job error:', err)
    message.value = 'Error loading job details.'
    messageType.value = 'error'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  if (isEditMode.value) {
    fetchJobDetails()
  }

  if (!authStore.user) {
    authStore.refreshUser().then(() => {
      if (!isEditMode.value) { // Only set these defaults if NOT in edit mode
        formData.value.company = authStore.user?.companyName || authStore.user?.name || 'Recruiting Company'
        formData.value.companyOverview = authStore.user?.companyDescription || ''
        formData.value.recruiter_email = authStore.user?.email || ''
        if (!formData.value.location && authStore.user?.location) {
          formData.value.location = authStore.user.location
        }
      }
    })
  } else if (!isEditMode.value) {
    // Already have user and not in edit mode, ensure standard defaults just in case
    formData.value.company = fallbackCompany
    formData.value.recruiter_email = authStore.user.email
  }
})

async function submitJob() {
  isPosting.value = true
  message.value = ''
  
  // Format required documents based on checkboxes
  let reqDocs = []
  if (formData.value.reqResume) reqDocs.push('Resume/CV')
  if (formData.value.reqCoverLetter) reqDocs.push('Cover Letter')
  if (formData.value.reqPortfolio) reqDocs.push('Portfolio')
  
  // Payload sent to API (mapping specific fields if needed, or sending raw)
  const payload = { ...formData.value, requiredDocumentsList: reqDocs }

  try {
    if (isEditMode.value) {
      await updateJob(route.params.id, payload)
      message.value = 'Job updated successfully! Redirecting...'
    } else {
      await createJob(payload)
      message.value = 'Job posted successfully! Redirecting...'
    }
    
    messageType.value = 'success'
    setTimeout(() => {
      router.push('/manage-jobs')
    }, 1500)
  } catch (err) {
    console.error('Submit job error:', err)
    message.value = err.message || `Network error while trying to ${isEditMode.value ? 'update' : 'post'} job.`
    messageType.value = 'error'
  } finally {
    isPosting.value = false
  }
}
</script>

<style scoped>
.post-job-view { min-height: 100vh; padding-bottom: 4rem; }

.form-card { padding: 2.5rem; max-width: 900px; margin: 0 auto; }

.section-title { font-size: 1.25rem; font-weight: 800; color: var(--clr-text); margin-bottom: 1.5rem; display: block; border: none; }
.form-section { border: none; padding: 0; margin: 0; }

.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }

.required { color: var(--clr-danger); }

.disabled { background-color: var(--clr-surface-alt); cursor: not-allowed; opacity: 0.8; }

.checkbox-group { display: flex; flex-direction: column; gap: 0.5rem; padding-top: 0.5rem; }
.checkbox-label { display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; cursor: pointer; color: var(--clr-text); }



.submit-section { display: flex; justify-content: flex-end; border-top: 1px solid var(--clr-border); padding-top: 2rem; }
.submit-btn { padding: 0.75rem 2.5rem; font-size: 1.1rem; }

/* ═══ Hiring Pipeline ════════════════════════════════════════ */
.section-desc {
  font-size: 0.85rem;
  color: var(--clr-text-muted);
  margin-bottom: 1.25rem;
  line-height: 1.5;
}

.pipeline-rounds {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.round-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  background: var(--clr-surface-2);
  border: 1px solid var(--clr-border);
  border-radius: 99px;
  padding: 0.4rem 0.85rem 0.4rem 0.5rem;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--clr-text);
  position: relative;
  transition: all 0.2s;
}
.round-chip:hover { border-color: var(--clr-primary); }

.round-chip--locked {
  background: var(--gradient-glow);
  border-color: rgba(99, 102, 241, 0.25);
  color: var(--clr-primary);
}

.round-chip--last {
  background: rgba(16, 185, 129, 0.08);
  border-color: rgba(16, 185, 129, 0.25);
  color: #10b981;
}

.round-chip__index {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--clr-surface);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: 800;
  color: var(--clr-text-muted);
  flex-shrink: 0;
}
.round-chip--locked .round-chip__index { background: var(--clr-primary); color: white; }
.round-chip--last .round-chip__index { background: #10b981; color: white; }

.round-chip__name { white-space: nowrap; }

.round-chip__remove {
  background: none; border: none; cursor: pointer; padding: 2px;
  color: var(--clr-text-muted); border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.15s;
}
.round-chip__remove:hover { color: #ef4444; background: rgba(239, 68, 68, 0.1); }
.round-chip__remove:disabled { opacity: 0.3; cursor: not-allowed; }

.round-connector {
  flex-shrink: 0;
  margin: 0 -0.1rem;
}

.add-round-row {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.add-round-input {
  max-width: 240px;
  height: 38px;
  font-size: 0.85rem;
}

.pipeline-limit-msg {
  font-size: 0.8rem;
  color: var(--clr-text-muted);
  font-style: italic;
}

.pipeline-locked-msg {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.82rem;
  color: #f59e0b;
  font-weight: 600;
  background: rgba(245, 158, 11, 0.08);
  border: 1px solid rgba(245, 158, 11, 0.2);
  padding: 0.6rem 1rem;
  border-radius: 8px;
}

@media (max-width: 800px) {
  .form-grid { grid-template-columns: 1fr; }
  .form-card { padding: 1.5rem; }
  .submit-btn { width: 100%; }
  .pipeline-rounds { gap: 0.35rem; }
  .add-round-row { flex-direction: column; align-items: stretch; }
  .add-round-input { max-width: 100%; }
}


</style>

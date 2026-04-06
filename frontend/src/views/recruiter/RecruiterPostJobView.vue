<template>
  <div class="post-job-view">
    <div class="content-area">
      <div class="header-section animate-fade-in-up">
        <button class="back-btn" @click="goBack">
          &larr; Back to Jobs
        </button>
        <h1 class="page-title mt-4">{{ isEditMode ? 'Edit Hiring Request' : 'Post a Hiring Request' }}</h1>
        <p class="page-subtitle">{{ isEditMode ? 'Update your job opportunity details.' : 'Publish a comprehensive job opportunity to attract top talent.' }}</p>
      </div>

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
import AppSpinner from '@/components/AppSpinner.vue'
import AppAlert from '@/components/AppAlert.vue'

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
  recruiter_email: authStore.user?.email || ''
})

function goBack() {
  router.push('/manage-jobs')
}

async function fetchJobDetails() {
  isLoading.value = true
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:5001'}/api/jobs/${route.params.id}`)
    const data = await res.json()
    if (data.status === 'success') {
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
    } else {
      message.value = 'Failed to load job details.'
      messageType.value = 'error'
    }
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
    const method = isEditMode.value ? 'PUT' : 'POST'
    const url = isEditMode.value 
      ? `${import.meta.env.VITE_API_URL || 'http://localhost:5001'}/api/jobs/${route.params.id}`
      : `${import.meta.env.VITE_API_URL || 'http://localhost:5001'}/api/jobs`

    const res = await fetch(url, {
      method: method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    const data = await res.json()
    if (data.status === 'success') {
      message.value = isEditMode.value ? 'Job updated successfully! Redirecting...' : 'Job posted successfully! Redirecting...'
      messageType.value = 'success'
      setTimeout(() => {
        router.push('/manage-jobs')
      }, 1500)
    } else {
      message.value = data.message || (isEditMode.value ? 'Failed to update job' : 'Failed to post job')
      messageType.value = 'error'
      isPosting.value = false
    }
  } catch (err) {
    console.error('Submit job error:', err)
    message.value = `Network error while trying to ${isEditMode.value ? 'update' : 'post'} job.`
    messageType.value = 'error'
    isPosting.value = false
  }
}
</script>

<style scoped>
.post-job-view { min-height: 100vh; padding-bottom: 4rem; }
.header-section { margin-bottom: 2rem; }
.back-btn { background: none; border: none; font-size: 0.9rem; font-weight: 600; color: var(--clr-primary); cursor: pointer; display: inline-flex; align-items: center; }
.back-btn:hover { text-decoration: underline; }
.page-title { font-size: 2rem; font-weight: 800; }
.page-subtitle { color: var(--clr-text-muted); }

.form-card { padding: 2.5rem; max-width: 900px; margin: 0 auto; }

.section-title { font-size: 1.25rem; font-weight: 800; color: var(--clr-text); margin-bottom: 1.5rem; display: block; border: none; }
.form-section { border: none; padding: 0; margin: 0; }

.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }

.required { color: var(--clr-danger); }

.disabled { background-color: var(--clr-surface-alt); cursor: not-allowed; opacity: 0.8; }

.mb-4 { margin-bottom: 1.25rem; }
.mt-4 { margin-top: 1.25rem; }
.mt-8 { margin-top: 3rem; }

.divider { height: 1px; background: var(--clr-border); margin: 2.5rem 0; }

.checkbox-group { display: flex; flex-direction: column; gap: 0.5rem; padding-top: 0.5rem; }
.checkbox-label { display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; cursor: pointer; color: var(--clr-text); }



.submit-section { display: flex; justify-content: flex-end; border-top: 1px solid var(--clr-border); padding-top: 2rem; }
.submit-btn { padding: 0.75rem 2.5rem; font-size: 1.1rem; }

@media (max-width: 800px) {
  .form-grid { grid-template-columns: 1fr; }
  .form-card { padding: 1.5rem; }
  .submit-btn { width: 100%; }
}


</style>

<template>
  <div class="post-jobs-view">
    <div class="content-area">
      <div class="jobs-header animate-fade-in-up">
        <div>
          <h1 class="jobs-title">Manage Job Postings</h1>
          <p class="jobs-subtitle">Create and track job opportunities</p>
        </div>
        <button @click="showModal = true" class="btn btn-primary">+ Post New Job</button>
      </div>

      <div class="jobs-grid grid animate-fade-in-up" style="animation-delay: 0.1s">
        <div v-if="jobs.length === 0" class="empty-state card full-width">
          <h3>No jobs posted yet</h3>
          <p>Click the button above to post your first job opportunity.</p>
        </div>

        <div v-for="job in jobs" :key="job.id" class="job-card card">
          <div class="job-card__header">
            <h3 class="job-title">{{ job.title }}</h3>
            <span class="job-type-badge">{{ job.type }}</span>
          </div>
          <div class="job-details">
            <span class="detail-item">{{ job.location }}</span>
            <span class="detail-item">{{ job.salary }}</span>
          </div>
          <p class="job-description">{{ job.description }}</p>
          <div class="job-footer">
            <button class="btn btn-ghost btn-sm">Edit</button>
            <button class="btn btn-ghost btn-sm text-danger">Delete</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Post Job Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal card animate-fade-in-up">
        <div class="modal-header">
          <h2>Post New Opportunity</h2>
          <button @click="showModal = false" class="close-btn">&times;</button>
        </div>
        <form @submit.prevent="postJob" class="modal-form">
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">Job Title</label>
              <input v-model="formData.title" type="text" class="form-input" placeholder="e.g. Senior Product Designer" required>
            </div>
            <div class="form-group">
              <label class="form-label">Company Name</label>
              <input v-model="formData.company" type="text" class="form-input" placeholder="e.g. TechFlow Inc" required>
            </div>
            <div class="form-group">
              <label class="form-label">Type</label>
              <select v-model="formData.type" class="form-input">
                <option value="Full-time">Full-time</option>
                <option value="Internship">Internship</option>
                <option value="Part-time">Part-time</option>
                <option value="Contract">Contract</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Location</label>
              <input v-model="formData.location" type="text" class="form-input" placeholder="e.g. Remote or Bengaluru, India">
            </div>
          </div>
          <div class="form-group mt-4">
            <label class="form-label">Description</label>
            <textarea v-model="formData.description" class="form-input" rows="4" placeholder="Briefly describe the role..."></textarea>
          </div>
          <div class="modal-footer mt-6">
            <button type="button" @click="showModal = false" class="btn btn-outline">Cancel</button>
            <button type="submit" class="btn btn-primary" :disabled="isPosting">
              <span v-if="!isPosting">Post Opportunity</span>
              <span v-else class="loader-sm"></span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()
const jobs = ref([])
const showModal = ref(false)
const isPosting = ref(false)

const formData = ref({
  title: '',
  company: '',
  type: 'Full-time',
  location: 'Remote',
  description: '',
  recruiter_email: authStore.user?.email || ''
})

async function fetchMyJobs() {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:5001'}/api/jobs`)
    const data = await res.json()
    if (data.status === 'success') {
      // Filter by current recruiter in real world we'd use a specific backend query
      jobs.value = data.jobs.filter(j => j.recruiter_email === authStore.user?.email)
    }
  } catch (err) {
    console.error('Fetch my jobs error:', err)
  }
}

async function postJob() {
  isPosting.value = true
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:5001'}/api/jobs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData.value)
    })
    const data = await res.json()
    if (data.status === 'success') {
      jobs.value.unshift(data.job)
      showModal.value = false
      // Reset form
      formData.value = {
        title: '',
        company: '',
        type: 'Full-time',
        location: 'Remote',
        description: '',
        recruiter_email: authStore.user?.email || ''
      }
    }
  } catch (err) {
    console.error('Post job error:', err)
  } finally {
    isPosting.value = false
  }
}

onMounted(fetchMyJobs)
</script>

<style scoped>
.post-jobs-view { min-height: 100vh; }
.jobs-header { display: flex; justify-content: space-between; align-items: start; margin-bottom: 2rem; }
.jobs-title { font-size: 2rem; font-weight: 800; }
.jobs-subtitle { color: var(--clr-text-muted); }

.jobs-grid { grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }
.job-card { padding: 1.5rem; display: flex; flex-direction: column; gap: 0.75rem; }
.job-card__header { display: flex; justify-content: space-between; align-items: center; }
.job-title { font-size: 1.1rem; font-weight: 700; color: var(--clr-text); }
.job-type-badge { font-size: 0.75rem; background: rgba(99, 102, 241, 0.1); color: var(--clr-primary); padding: 2px 8px; border-radius: 4px; font-weight: 600; }
.job-details { display: flex; gap: 1rem; font-size: 0.85rem; color: var(--clr-text-light); }
.job-description { font-size: 0.9rem; color: var(--clr-text-muted); line-height: 1.5; display: -webkit-box;  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
 overflow: hidden; }
.job-footer { margin-top: auto; display: flex; gap: 0.5rem; padding-top: 1rem; border-top: 1px solid var(--clr-border); }

.empty-state { grid-column: 1 / -1; text-align: center; padding: 4rem; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0, 0, 0, 0.75); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 1rem; }
.modal { width: 100%; max-width: 600px; padding: 2rem; }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
.modal-header h2 { font-size: 1.5rem; }
.close-btn { background: none; border: none; color: var(--clr-text-muted); font-size: 1.5rem; cursor: pointer; }

.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }
.modal-footer { display: flex; justify-content: flex-end; gap: 1rem; }

.text-danger { color: var(--clr-danger); }
.mt-4 { margin-top: 1rem; }
.mt-6 { margin-top: 1.5rem; }

@media (max-width: 600px) {
  .form-grid { grid-template-columns: 1fr; }
}
</style>

<template>
  <div class="post-jobs-view">
    <div class="content-area">
      <div class="jobs-header animate-fade-in-up">
        <div>
          <h1 class="jobs-title">Manage Job Postings</h1>
          <p class="jobs-subtitle">Create and track job opportunities</p>
        </div>
        <router-link to="/post-job" class="btn btn-primary">+ Post New Job</router-link>
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
            <router-link :to="`/edit-job/${job.id}`" class="btn btn-ghost btn-sm">Edit</router-link>
            <button @click="deleteJob(job.id)" class="btn btn-ghost btn-sm text-danger">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()
const jobs = ref([])

async function fetchMyJobs() {
  if (!authStore.user?.email) {
    // Retry if user is not loaded yet
    setTimeout(fetchMyJobs, 500)
    return
  }
  
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:5001'}/api/jobs?recruiter_email=${authStore.user.email}`)
    const data = await res.json()
    if (data.status === 'success') {
      jobs.value = data.jobs
    }
  } catch (err) {
    console.error('Fetch my jobs error:', err)
  }
}

async function deleteJob(jobId) {
  if (!confirm('Are you sure you want to delete this job posting?')) return;
  
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:5001'}/api/jobs/${jobId}`, {
      method: 'DELETE'
    })
    const data = await res.json()
    if (data.status === 'success') {
      jobs.value = jobs.value.filter(j => j.id !== jobId)
    } else {
      alert(data.message || 'Failed to delete job')
    }
  } catch (err) {
    console.error('Delete job error:', err)
    alert('An error occurred while deleting the job')
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

.text-danger { color: var(--clr-danger); }

@media (max-width: 600px) {
  .jobs-header { flex-direction: column; gap: 1rem; }
}
</style>

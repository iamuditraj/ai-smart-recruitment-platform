<template>
  <div class="post-jobs-view">
    <div class="content-area">
      <PageHeader
        title="Manage Job Postings"
        subtitle="Create and track job opportunities"
      >
        <template #actions>
          <router-link to="/post-job" class="btn btn-primary">+ Post New Job</router-link>
        </template>
      </PageHeader>

      <div class="jobs-grid grid animate-fade-in-up" style="animation-delay: 0.1s">
        <AppEmptyState
          v-if="jobs.length === 0"
          title="No jobs posted yet"
          description='Click the button above to post your first job opportunity.'
          class="full-width"
        />

        <JobCard v-for="job in jobs" :key="job.id" :job="job" :showCompanyInfo="false">
          <template #actions>
            <router-link :to="`/manage-jobs/${job.id}/applications`" class="btn btn-primary btn-sm">Manage Applications</router-link>
            <router-link :to="`/edit-job/${job.id}`" class="btn btn-ghost btn-sm">Edit</router-link>
            <button @click="deleteJob(job.id)" class="btn btn-ghost btn-sm text-danger">Delete</button>
          </template>
        </JobCard>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import AppEmptyState from '@/components/AppEmptyState.vue'
import PageHeader from '@/components/PageHeader.vue'
import JobCard from '@/components/JobCard.vue'
import { getJobs, deleteJob as deleteJobApi } from '@/utils/api'

const authStore = useAuthStore()
const jobs = ref([])

async function fetchMyJobs() {
  if (!authStore.user?.email) {
    // Retry if user is not loaded yet
    setTimeout(fetchMyJobs, 500)
    return
  }
  
  try {
    const data = await getJobs(authStore.user.email)
    jobs.value = data.jobs
  } catch (err) {
    console.error('Fetch my jobs error:', err)
  }
}

async function deleteJob(jobId) {
  if (!confirm('Are you sure you want to delete this job posting?')) return;
  
  try {
    await deleteJobApi(jobId)
    jobs.value = jobs.value.filter(j => j.id !== jobId)
  } catch (err) {
    console.error('Delete job error:', err)
    alert(err.message || 'An error occurred while deleting the job')
  }
}

onMounted(fetchMyJobs)
</script>

<style scoped>
.post-jobs-view { min-height: 100vh; }

.jobs-grid { grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }


@media (max-width: 600px) {
  .jobs-header { flex-direction: column; gap: 1rem; }
}
</style>

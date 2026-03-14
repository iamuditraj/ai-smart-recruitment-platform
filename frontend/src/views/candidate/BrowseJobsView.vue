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
            <!-- If we are currently applying to this job, hide standard button and show file input -->
            <div v-if="applyingTo === job.id" class="apply-upload-area">
               <label class="btn btn-outline apply-upload-btn w-full">
                 <span v-if="!isUploading">Select Resume (PDF/DOCX)</span>
                 <span v-else class="loader-sm"></span>
                 <input type="file" accept=".pdf,.docx,.doc" class="hidden-input" @change="(e) => finalizeApplication(e, job)" />
               </label>
               <button class="btn btn-text w-full mt-2 text-sm" @click="applyingTo = null" :disabled="isUploading">Cancel</button>
            </div>
            
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
const applyingTo = ref(null)
const isUploading = ref(false)

const toast = ref({ show: false, message: '', type: 'success' })

function showToast(message, type = 'success') {
  toast.value = { show: true, message, type }
  setTimeout(() => toast.value.show = false, 3000)
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
  applyingTo.value = job.id
}

async function finalizeApplication(event, job) {
  const file = event.target.files[0];
  if (!file) return;

  isUploading.value = true;
  
  try {
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_id', job.id);
    formData.append('candidate_email', authStore.user?.email || '');

    const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:5001'}/api/jobs/apply`, {
      method: 'POST',
      body: formData // Let the browser set the multi-part boundary headers automatically
    })
    
    const data = await res.json()
    if (data.status === 'success') {
      showToast('Successfully applied! Your ATS score was computed.')
    } else {
      showToast(data.message || 'Failed to submit application', 'error')
    }
  } catch (err) {
    console.error(err)
    showToast('Failed to apply. Check your connection.', 'error')
  } finally {
    isUploading.value = false;
    applyingTo.value = null;
    event.target.value = ''; // Reset file input
  }
}

onMounted(fetchJobs)
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

.hidden-input {
  display: none;
}

.apply-upload-area {
  display: flex;
  flex-direction: column;
  animation: fadeIn 0.3s ease;
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
}
.btn-text:hover {
  text-decoration: underline;
  color: var(--clr-text);
}
.mt-2 { margin-top: 0.5rem; }
.text-sm { font-size: 0.85rem; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}

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
  z-index: 1000;
}
.toast.success { background: var(--clr-success); }
.toast.error { background: var(--clr-danger); }

@keyframes spin { to { transform: rotate(360deg); } }
.fade-enter-active, .fade-leave-active { transition: opacity 0.5s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>

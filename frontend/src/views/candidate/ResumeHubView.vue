<template>
  <div class="resume-hub-view">
    <div class="content-area">
      <PageHeader
        title="Resume Hub"
        subtitle="Manage, view, and organize all your uploaded and AI-generated resumes."
      >
        <template #actions>
          <div class="action-bar animate-fade-in-up" style="animation-delay: 0.1s; margin-bottom: 0;">
            <div class="upload-container">
              <input type="file" ref="resumeInput" class="hidden-input" accept="application/pdf" @change="handleResumeUpload">
              <button type="button" class="btn btn-primary" @click="$refs.resumeInput.click()" :disabled="isUploading">
                <span v-if="!isUploading">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="btn-icon"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                  Upload PDF Resume
                </span>
                <AppSpinner v-else size="sm" />
              </button>
            </div>
            <RouterLink to="/resume-generation" class="btn btn-outline">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="btn-icon"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
              Build AI Resume
            </RouterLink>
          </div>
        </template>
      </PageHeader>

      <AppAlert v-if="message" :message="message" :type="messageType" />

      <!-- Resume List -->
      <div class="resume-grid animate-fade-in-up" style="animation-delay: 0.2s">
        <AppEmptyState
          v-if="!resumes.length"
          title="No resumes yet"
          description="Upload a PDF or use our AI builder to create your first resume."
          :showCard="false"
        >
          <template #icon>
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
          </template>
        </AppEmptyState>

        <div v-else class="resume-card" v-for="resume in resumes" :key="resume.id || resume.resume_id" :class="{ 'is-default': resume.isDefault }">
          <div class="resume-card-header">
            <div class="resume-icon-wrapper" :class="resume.type">
              <svg v-if="resume.type === 'uploaded'" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
            </div>
            <div class="resume-meta">
              <h3 class="resume-name" :title="resume.resumeName">{{ resume.resumeName }}</h3>
              <p class="resume-date">{{ formatDate(resume.uploadedAt) }} • <span class="resume-type">{{ resume.type }}</span></p>
            </div>
            <div v-if="resume.isDefault" class="default-badge">
              Default
            </div>
          </div>
          
          <div class="resume-card-actions">
            <button v-if="!resume.isDefault" @click="setAsDefault(getResumeId(resume))" class="btn btn-sm btn-outline text-primary" :disabled="isSettingDefault === getResumeId(resume)">
              <span v-if="isSettingDefault === getResumeId(resume)" class="loader-xs"></span>
              <span v-else>Set Default</span>
            </button>
            <button v-else disabled class="btn btn-sm btn-ghost text-muted outline-none" style="cursor:default">
              Current Default
            </button>
            
            <button v-if="resume.type === 'uploaded'" @click="viewResume(resume.resumeUrl)" class="btn btn-sm btn-ghost">
              View PDF
            </button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { formatDate } from '@/utils/dateUtils'
import AppSpinner from '@/components/AppSpinner.vue'
import AppAlert from '@/components/AppAlert.vue'
import AppEmptyState from '@/components/AppEmptyState.vue'
import PageHeader from '@/components/PageHeader.vue'

const authStore = useAuthStore()
const resumes = computed(() => {
  const list = authStore.resumes || []
  // Sort: default first, then newest first
  return [...list].sort((a, b) => {
    if (a.isDefault) return -1
    if (b.isDefault) return 1
    return new Date(b.uploadedAt) - new Date(a.uploadedAt)
  })
})

onMounted(() => {
  authStore.fetchResumes()
})

const resumeInput = ref(null)
const isUploading = ref(false)
const isSettingDefault = ref(null)
const message = ref('')
const messageType = ref('success')

// Get the best available stable ID for a resume (supports legacy records without id field)
function getResumeId(resume) {
  return resume.id || resume.resume_id || resume.uploadedAt || null
}



async function handleResumeUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  if (file.type !== 'application/pdf') {
    showMessage('Please upload a PDF file', 'error')
    return
  }

  if (file.size > 900 * 1024) {
    showMessage('Resume size must be less than 900KB', 'error')
    return
  }

  isUploading.value = true
  message.value = ''

  const result = await authStore.uploadResume(file)

  isUploading.value = false
  if (result.success) {
    showMessage('Resume uploaded successfully!', 'success')
  } else {
    showMessage(result.message || 'Failed to upload resume', 'error')
  }
}

async function setAsDefault(id) {
  if (!id) return
  isSettingDefault.value = id
  message.value = ''
  
  const result = await authStore.setDefaultResume(id)
  
  isSettingDefault.value = null
  if (result.success) {
    showMessage('Default resume updated', 'success')
  } else {
    showMessage(result.message || 'Failed to set default', 'error')
  }
}



function showMessage(msg, type) {
  message.value = msg
  messageType.value = type
  setTimeout(() => message.value = '', 4000)
}
</script>

<style scoped>
.resume-hub-view { min-height: 100vh; }
.action-bar {
  display: flex;
  gap: var(--sp-4);
  flex-wrap: wrap;
}

.btn-icon {
  margin-right: 8px;
  vertical-align: middle;
}
.hidden-input {
  display: none;
}

.resume-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--sp-6);
}

.resume-card {
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  transition: all 0.2s ease;
}
.resume-card:hover {
  border-color: var(--clr-border-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
.resume-card.is-default {
  border-color: var(--clr-primary);
  background: linear-gradient(to bottom right, var(--clr-surface), rgba(99, 102, 241, 0.03));
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.08);
}

.resume-card-header {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  position: relative;
}

.resume-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.resume-icon-wrapper.uploaded {
  background: rgba(239, 68, 68, 0.1);
  color: var(--clr-danger);
}
.resume-icon-wrapper.generated {
  background: rgba(99, 102, 241, 0.1);
  color: var(--clr-primary);
}

.resume-meta {
  flex: 1;
  min-width: 0;
}
.resume-name {
  font-size: 1.05rem;
  font-weight: 700;
  margin: 0 0 4px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--clr-text);
  padding-right: 60px; /* space for default badge */
}
.resume-date {
  font-size: 0.8rem;
  color: var(--clr-text-muted);
  margin: 0;
}
.resume-type {
  text-transform: capitalize;
  font-weight: 600;
}

.default-badge {
  position: absolute;
  top: 0;
  right: 0;
  background: var(--clr-primary);
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 999px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.resume-card-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: auto;
  padding-top: 1rem;
  border-top: 1px solid var(--clr-border);
}

.btn-sm {
  padding: 0.4rem 0.8rem;
  font-size: 0.8rem;
}
.text-primary {
  color: var(--clr-primary);
}
.outline-none {
  border-color: transparent !important;
}

.loader-xs {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(99, 102, 241, 0.2);
  border-top-color: var(--clr-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 480px) {
  .resume-grid {
    grid-template-columns: 1fr;
  }
}
</style>

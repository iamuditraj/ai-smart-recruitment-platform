<template>
  <div class="resume-hub-view">
    <div class="content-area">
      <div class="hub-header animate-fade-in-up">
        <h1 class="hub-title">Resume Hub</h1>
        <p class="hub-subtitle">Manage, view, and organize all your uploaded and AI-generated resumes.</p>
      </div>

      <!-- Action Bar -->
      <div class="action-bar animate-fade-in-up" style="animation-delay: 0.1s">
        <div class="upload-container">
          <input type="file" ref="resumeInput" class="hidden-input" accept="application/pdf" @change="handleResumeUpload">
          <button type="button" class="btn btn-primary" @click="$refs.resumeInput.click()" :disabled="isUploading">
            <span v-if="!isUploading">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="btn-icon"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
              Upload PDF Resume
            </span>
            <span v-else class="loader-sm"></span>
          </button>
        </div>
        <RouterLink to="/resume-generation" class="btn btn-outline">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="btn-icon"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
          Build AI Resume
        </RouterLink>
      </div>

      <div v-if="message" :class="['message-banner', messageType, 'animate-fade-in-up']" style="animation-delay: 0.15s">
        {{ message }}
      </div>

      <!-- Resume List -->
      <div class="resume-grid animate-fade-in-up" style="animation-delay: 0.2s">
        <div v-if="!resumes.length" class="empty-state">
          <div class="empty-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
          </div>
          <h3>No resumes yet</h3>
          <p class="text-muted">Upload a PDF or use our AI builder to create your first resume.</p>
        </div>

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
import { ref, computed } from 'vue'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()
const resumes = computed(() => {
  const list = authStore.user?.resumes || []
  // Sort: default first, then newest first
  return [...list].sort((a, b) => {
    if (a.isDefault) return -1
    if (b.isDefault) return 1
    return new Date(b.uploadedAt) - new Date(a.uploadedAt)
  })
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

function formatDate(isoString) {
  if (!isoString) return 'Unknown date'
  const d = new Date(isoString)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
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

function viewResume(dataUri) {
  if (!dataUri) return

  try {
    const base64 = dataUri.split(',')[1]
    const binary = atob(base64)
    const array = []
    for (let i = 0; i < binary.length; i++) {
      array.push(binary.charCodeAt(i))
    }
    const blob = new Blob([new Uint8Array(array)], { type: 'application/pdf' })
    const url = URL.createObjectURL(blob)
    window.open(url, '_blank')
  } catch (error) {
    console.error('Error viewing resume:', error)
    window.open(dataUri, '_blank')
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
.hub-header { margin-bottom: var(--sp-6); }
.hub-title { font-size: 2.2rem; font-weight: 800; letter-spacing: -0.02em; }
.hub-subtitle { color: var(--clr-text-muted); margin-top: var(--sp-1); font-size: 1.05rem; }

.action-bar {
  display: flex;
  gap: var(--sp-4);
  margin-bottom: var(--sp-8);
  flex-wrap: wrap;
}

.btn-icon {
  margin-right: 8px;
  vertical-align: middle;
}
.hidden-input {
  display: none;
}

.message-banner {
  padding: 1rem;
  border-radius: var(--radius-md);
  margin-bottom: 1.5rem;
  font-weight: 600;
  text-align: center;
  font-size: 0.9rem;
}
.message-banner.success {
  background: rgba(16, 185, 129, 0.1);
  color: var(--clr-success);
  border: 1px solid rgba(16, 185, 129, 0.2);
}
.message-banner.error {
  background: rgba(239, 68, 68, 0.1);
  color: var(--clr-danger);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.resume-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--sp-6);
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 4rem 2rem;
  background: var(--clr-surface);
  border: 1px dashed var(--clr-border-hover);
  border-radius: var(--radius-lg);
}
.empty-icon {
  color: var(--clr-text-muted);
  opacity: 0.5;
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
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
.loader-sm {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.2);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>

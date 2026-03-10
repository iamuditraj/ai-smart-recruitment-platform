<template>
  <div class="profile-view">
    <div class="content-area">
      <div class="profile-header animate-fade-in-up">
        <h1 class="profile-title">Your Profile</h1>
        <p class="profile-subtitle">Manage your personal information and preferences</p>
      </div>

      <div class="profile-content grid">
        <!-- Left: Static Info -->
        <div class="profile-card card animate-fade-in-up" style="animation-delay: 0.1s">
          <div class="profile-avatar-container" @click="$refs.fileInput.click()">
            <div class="profile-avatar-large">
              <img v-if="formData.photo" :src="formData.photo" alt="Profile" class="avatar-img">
              <span v-else>{{ authStore.user?.name?.charAt(0).toUpperCase() }}</span>
            </div>
            <div class="avatar-overlay">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
            </div>
            <input type="file" ref="fileInput" class="hidden-input" accept="image/*" @change="handlePhotoUpload">
          </div>
          <h2 class="text-center mt-4">{{ authStore.user?.name }}</h2>
          <p class="text-center text-muted text-sm">{{ authStore.user?.email }}</p>
          <div class="badge badge-primary mt-2 mx-auto">{{ authStore.role }}</div>

          <div class="profile-info-list">
            <div class="info-item">
              <span class="label">Member Since</span>
              <span class="value">{{ new Date().getFullYear() }}</span>
            </div>
            <div class="info-item">
              <span class="label">Account Type</span>
              <span class="value capitalize">{{ authStore.role }}</span>
            </div>
          </div>
        </div>

        <!-- Right: Edit Form -->
        <div class="profile-form card animate-fade-in-up" style="animation-delay: 0.2s">
          <form @submit.prevent="saveProfile">
            <h3 class="subsection-title">Basic Information</h3>

            <div v-if="message" :class="['message-banner', messageType]">
              {{ message }}
            </div>

            <div class="form-grid">
              <div class="form-group">
                <label class="form-label">Full Name</label>
                <input v-model="formData.name" type="text" class="form-input" placeholder="Your Name" required>
              </div>
              <div class="form-group">
                <label class="form-label">Email Address</label>
                <input :value="authStore.user?.email" type="email" class="form-input" disabled>
                <small class="text-muted">Email cannot be changed</small>
              </div>
              <div class="form-group">
                <label class="form-label">Phone Number</label>
                <input v-model="formData.phone" type="tel" class="form-input" placeholder="+91 98765 43210">
              </div>
              <div class="form-group">
                <label class="form-label">Location</label>
                <input v-model="formData.location" type="text" class="form-input" placeholder="City, Country">
              </div>
            </div>

            <div class="divider my-8"></div>

            <h3 class="subsection-title">Resume</h3>
            <div class="resume-section">
              <div v-if="authStore.user?.resumeUrl" class="current-resume-card">
                <div class="resume-info">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="resume-icon"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
                  <div class="resume-details">
                    <span class="resume-name">{{ authStore.user?.resumeName || 'Your Resume.pdf' }}</span>
                    <a href="javascript:void(0)" @click="viewResume" class="view-link">View File</a>
                  </div>
                </div>
              </div>

              <div class="upload-container mt-4">
                <input type="file" ref="resumeInput" class="hidden-input" accept="application/pdf" @change="handleResumeUpload">
                <button type="button" class="btn btn-outline" @click="$refs.resumeInput.click()" :disabled="isUploadingResume">
                  <span v-if="!isUploadingResume">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="btn-icon"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                    {{ authStore.user?.resumeUrl ? 'Replace Resume (PDF)' : 'Upload Resume (PDF)' }}
                  </span>
                  <span v-else class="loader-sm"></span>
                </button>
                <p class="text-xs text-muted mt-2">Free Tier: PDFs up to 900KB are stored directly in your profile.</p>
              </div>
            </div>

            <div class="divider my-8"></div>

            <h3 class="subsection-title">Professional Bio</h3>
            <div class="form-group">
              <label class="form-label">About You</label>
              <textarea v-model="formData.bio" class="form-input" rows="4" placeholder="Tell us about yourself..."></textarea>
            </div>

            <div class="profile-actions mt-8">
              <button type="submit" class="btn btn-primary" :disabled="isSaving">
                <span v-if="!isSaving">Save Changes</span>
                <span v-else class="loader-sm"></span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const isSaving = ref(false)
const isUploadingResume = ref(false)
const message = ref('')
const messageType = ref('success')

const fileInput = ref(null)
const resumeInput = ref(null)
const formData = ref({
  name: authStore.user?.name || '',
  phone: authStore.user?.phone || '',
  location: authStore.user?.location || '',
  bio: authStore.user?.bio || '',
  photo: authStore.user?.photo || ''
})

function handlePhotoUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  // Basic validation (limit to 1MB effectively for small base64)
  if (file.size > 1024 * 1024) {
    message.value = 'Image size must be less than 1MB'
    messageType.value = 'error'
    return
  }

  const reader = new FileReader()
  reader.onload = (e) => {
    formData.value.photo = e.target.result
  }
  reader.readAsDataURL(file)
}

async function handleResumeUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  if (file.type !== 'application/pdf') {
    message.value = 'Please upload a PDF file'
    messageType.value = 'error'
    return
  }

  if (file.size > 900 * 1024) {
    message.value = 'Resume size must be less than 900KB for the free tier'
    messageType.value = 'error'
    return
  }

  isUploadingResume.value = true
  message.value = ''

  const result = await authStore.uploadResume(file)

  isUploadingResume.value = false
  if (result.success) {
    message.value = 'Resume saved successfully!'
    messageType.value = 'success'
  } else {
    message.value = result.message || 'Failed to save resume'
    messageType.value = 'error'
  }

  setTimeout(() => message.value = '', 3000)
}

function viewResume() {
  const dataUri = authStore.user?.resumeUrl
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
    // Fallback: try opening the data URI directly if blob fails
    window.open(dataUri, '_blank')
  }
}

async function saveProfile() {
  isSaving.value = true
  message.value = ''

  const result = await authStore.updateProfile(formData.value)

  isSaving.value = false
  if (result.success) {
    message.value = 'Profile updated successfully!'
    messageType.value = 'success'
  } else {
    message.value = result.message || 'Failed to update profile'
    messageType.value = 'error'
  }

  // Clear message after 3s
  setTimeout(() => message.value = '', 3000)
}

onMounted(() => {
  authStore.refreshUser().then(() => {
    formData.value = {
      name: authStore.user?.name || '',
      phone: authStore.user?.phone || '',
      location: authStore.user?.location || '',
      bio: authStore.user?.bio || '',
      photo: authStore.user?.photo || ''
    }
  })
})
</script>

<style scoped>
.profile-view { min-height: 100vh; }
.profile-header { margin-bottom: var(--sp-8); }
.profile-title { font-size: 2rem; font-weight: 800; }
.profile-subtitle { color: var(--clr-text-muted); margin-top: var(--sp-1); }

.profile-content {
  grid-template-columns: 320px 1fr;
  align-items: start;
  gap: var(--sp-8);
}

.profile-avatar-container {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto;
  cursor: pointer;
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.profile-avatar-large {
  width: 100%;
  height: 100%;
  background: var(--gradient-brand);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  font-weight: 800;
  box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.profile-avatar-container:hover .avatar-overlay {
  opacity: 1;
}

.hidden-input {
  display: none;
}

.profile-info-list {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-item .label {
  font-size: 0.75rem;
  color: var(--clr-text-muted);
  text-transform: uppercase;
  font-weight: 600;
}

.info-item .value {
  font-weight: 600;
  color: var(--clr-text);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--sp-6);
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

.my-8 { margin-block: 2rem; }
.mt-8 { margin-top: 2rem; }
.mt-4 { margin-top: 1rem; }
.mt-2 { margin-top: 0.5rem; }
.mx-auto { margin-inline: auto; }
.capitalize { text-transform: capitalize; }

@media (max-width: 1000px) {
  .profile-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}

.loader-sm {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.2);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.resume-section {
  background: rgba(99, 102, 241, 0.03);
  padding: 1.5rem;
  border-radius: var(--radius-md);
  border: 1px dashed rgba(99, 102, 241, 0.2);
}

.current-resume-card {
  background: white;
  padding: 1rem;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  margin-bottom: 1rem;
}

.resume-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.resume-icon {
  color: var(--clr-primary);
}

.resume-details {
  display: flex;
  flex-direction: column;
}

.resume-name {
  font-weight: 600;
  color: var(--clr-text);
  font-size: 0.95rem;
}

.view-link {
  color: var(--clr-primary);
  font-size: 0.85rem;
  font-weight: 500;
  text-decoration: underline;
  margin-top: 2px;
  cursor: pointer;
}

.btn-icon {
  margin-right: 8px;
  vertical-align: middle;
}

.text-xs { font-size: 0.75rem; }
</style>

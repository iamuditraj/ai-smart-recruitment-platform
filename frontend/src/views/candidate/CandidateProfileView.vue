<template>
  <ProfileLayout
    title="Your Profile"
    subtitle="Manage your personal information and preferences"
    :message="message"
    :messageType="messageType"
    :isSaving="isSaving"
    @save="handleSave"
  >
    <!-- Left: Static Info -->
    <template #left-pane>
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
    </template>

    <template #form-title>
      <h3 class="subsection-title">Basic Information</h3>
    </template>

    <template #form-fields>

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

            <h3 class="subsection-title">Current Default Resume</h3>
            <div class="resume-section">
              <div v-if="defaultResume" class="current-resume-card">
                <div class="resume-info">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="resume-icon"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
                  <div class="resume-details">
                    <span class="resume-name">{{ defaultResume.resumeName || 'Your Resume' }}</span>
                    <a v-if="defaultResume.type === 'uploaded'" href="javascript:void(0)" @click="viewResume(defaultResume.resumeUrl)" class="view-link">View PDF File</a>
                    <span v-else class="view-link text-muted" style="text-decoration:none">AI Generated Template</span>
                  </div>
                </div>
              </div>

              <div v-else class="text-muted text-sm my-4">
                You haven't set a default resume yet. Upload or generate a resume in the Resume Hub.
              </div>

              <div class="upload-container mt-4">
                <RouterLink to="/resume-hub" class="btn btn-outline" style="text-decoration:none">
                  <span>
                    Manage Resumes in Resume Hub →
                  </span>
                </RouterLink>
                <p class="text-xs text-muted mt-2">Go to the Resume Hub to add, generate, or change your default resume.</p>
              </div>
            </div>

            <div class="divider my-8"></div>

            <!-- AI Parsed Resume Section -->
            <ParsedResumeDisplay v-if="parsedResume" :parsedResume="parsedResume" />

            <div class="divider my-8"></div>

            <h3 class="subsection-title">Professional Bio</h3>
            <div class="form-group">
              <label class="form-label">About You</label>
              <textarea v-model="formData.bio" class="form-input" rows="4" placeholder="Tell us about yourself..."></textarea>
            </div>

    </template>
  </ProfileLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { viewResume } from '@/utils/resumeUtils'
import AppSpinner from '@/components/AppSpinner.vue'
import AppAlert from '@/components/AppAlert.vue'
import ParsedResumeDisplay from '@/components/ParsedResumeDisplay.vue'
import ProfileLayout from '@/components/ProfileLayout.vue'
import { useProfileForm } from '@/composables/useProfileForm'

const authStore = useAuthStore()
const { isSaving, message, messageType, saveProfile } = useProfileForm()

const defaultResume = computed(() => authStore.resumes?.find(r => r.isDefault) || null)

const parsedResume = computed(() => defaultResume.value?.parsedResume || null)

const fileInput = ref(null)
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



const handleSave = () => saveProfile(formData.value)

onMounted(() => {
  authStore.refreshUser().then(async () => {
    await authStore.fetchResumes()
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
  flex-wrap: wrap;
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

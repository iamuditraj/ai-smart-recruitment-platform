<template>
  <div class="profile-view">
    <div class="content-area">
      <div class="profile-header animate-fade-in-up">
        <div class="header-content">
          <div>
            <h1 class="profile-title">Recruiter Profile</h1>
            <p class="profile-subtitle">Manage your company and recruiter details</p>
          </div>
          <router-link to="/manage-jobs" class="btn btn-primary">
            Post Hiring Request
          </router-link>
        </div>
      </div>
      <div class="profile-content grid">
        <!-- Left: Static Info -->
        <div class="profile-card card animate-fade-in-up" style="animation-delay: 0.1s">
            <h2 class="text-center mt-4">{{ authStore.user?.name }}</h2>
            <p class="text-center text-muted text-sm">{{ authStore.user?.email }}</p>
            <div class="badge badge-primary mt-2 mx-auto capitalize">{{ authStore.role }}</div>
            
            <div class="profile-info-list" v-if="authStore.user?.companyName">
              <div class="info-item">
                <span class="label">Company</span>
                <span class="value">{{ authStore.user?.companyName }}</span>
              </div>
            </div>
        </div>

        <!-- Right: Edit Form -->
        <div class="profile-form card animate-fade-in-up" style="animation-delay: 0.2s">
          <form @submit.prevent="saveProfile">
            <h3 class="subsection-title">Recruiter Information</h3>
            
            <AppAlert v-if="message" :message="message" :type="messageType" />

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
                <label class="form-label">Contact Phone</label>
                <input v-model="formData.phone" type="tel" class="form-input" placeholder="+91 98765 43210">
              </div>
            </div>
            
            <div class="divider my-8"></div>
            
            <h3 class="subsection-title">Company Details</h3>
            
            <div class="form-grid">
              <div class="form-group">
                <label class="form-label">Company Name</label>
                <input v-model="formData.companyName" type="text" class="form-input" placeholder="e.g. Acme Corp">
              </div>
              <div class="form-group">
                <label class="form-label">Industry</label>
                <input v-model="formData.industry" type="text" class="form-input" placeholder="e.g. Information Technology">
              </div>
              <div class="form-group">
                <label class="form-label">Website</label>
                <input v-model="formData.website" type="url" class="form-input" placeholder="https://example.com">
              </div>
              <div class="form-group">
                <label class="form-label">Location</label>
                <input v-model="formData.location" type="text" class="form-input" placeholder="City, Country">
              </div>
            </div>

            <div class="form-group mt-4">
              <label class="form-label">Company Description</label>
              <textarea v-model="formData.companyDescription" class="form-input" rows="4" placeholder="Tell us about your company..."></textarea>
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
import { useAuthStore } from '../../stores/auth'
import AppSpinner from '@/components/AppSpinner.vue'
import AppAlert from '@/components/AppAlert.vue'

const authStore = useAuthStore()

const isSaving = ref(false)
const message = ref('')
const messageType = ref('success')

const formData = ref({
  name: authStore.user?.name || '',
  phone: authStore.user?.phone || '',
  companyName: authStore.user?.companyName || '',
  companyDescription: authStore.user?.companyDescription || '',
  industry: authStore.user?.industry || '',
  website: authStore.user?.website || '',
  location: authStore.user?.location || ''
})

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
      companyName: authStore.user?.companyName || '',
      companyDescription: authStore.user?.companyDescription || '',
      industry: authStore.user?.industry || '',
      website: authStore.user?.website || '',
      location: authStore.user?.location || ''
    }
  })
})
</script>

<style scoped>
.profile-view { min-height: 100vh; }
.profile-header { margin-bottom: var(--sp-8); }
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.profile-title { font-size: 2rem; font-weight: 800; }
.profile-subtitle { color: var(--clr-text-muted); margin-top: var(--sp-1); }

.profile-content {
  grid-template-columns: 320px 1fr;
  align-items: start;
  gap: var(--sp-8);
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

.my-8 { margin-block: 2rem; }
.mt-8 { margin-top: 2rem; }
.mt-4 { margin-top: 1rem; }
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
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
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

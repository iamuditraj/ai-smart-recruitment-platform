<template>
  <ProfileLayout
    :message="message"
    :messageType="messageType"
    :isSaving="isSaving"
    @save="handleSave"
  >
    <!-- Header Override (because it has the Post Hiring Request button) -->
    <template #header>
      <div class="header-content">
        <div>
          <h1 class="profile-title">Recruiter Profile</h1>
          <p class="profile-subtitle">Manage your company and recruiter details</p>
        </div>
        <router-link to="/manage-jobs" class="btn btn-primary">
          Post Hiring Request
        </router-link>
      </div>
    </template>

    <!-- Left: Static Info -->
    <template #left-pane>
      <h2 class="text-center mt-4">{{ authStore.user?.name }}</h2>
      <p class="text-center text-muted text-sm">{{ authStore.user?.email }}</p>
      <div class="badge badge-primary mt-2 mx-auto capitalize">{{ authStore.role }}</div>
      
      <div class="profile-info-list" v-if="authStore.user?.companyName">
        <div class="info-item">
          <span class="label">Company</span>
          <span class="value">{{ authStore.user?.companyName }}</span>
        </div>
      </div>
    </template>

    <template #form-title>
      <h3 class="subsection-title">Recruiter Information</h3>
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

    </template>
  </ProfileLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import AppSpinner from '@/components/AppSpinner.vue'
import AppAlert from '@/components/AppAlert.vue'
import ProfileLayout from '@/components/ProfileLayout.vue'
import { useProfileForm } from '@/composables/useProfileForm'

const authStore = useAuthStore()
const { isSaving, message, messageType, saveProfile } = useProfileForm()

const formData = ref({
  name: authStore.user?.name || '',
  phone: authStore.user?.phone || '',
  companyName: authStore.user?.companyName || '',
  companyDescription: authStore.user?.companyDescription || '',
  industry: authStore.user?.industry || '',
  website: authStore.user?.website || '',
  location: authStore.user?.location || ''
})

const handleSave = () => saveProfile(formData.value)

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


<template>
  <div class="form-step">
    <h2 class="step-title">Personal Information</h2>
    <p class="step-desc">Your contact details will appear at the top of the resume.</p>
    <div class="form-grid">
      <div class="form-group">
        <label class="form-label" for="rg-fullName">Full Name *</label>
        <input id="rg-fullName" type="text" class="form-input" v-model="store.formData.personal.fullName" placeholder="e.g. Priya Sharma" />
      </div>
      <div class="form-group">
        <label class="form-label" for="rg-jobTitle">Job Title / Role *</label>
        <input id="rg-jobTitle" type="text" class="form-input" v-model="store.formData.personal.jobTitle" placeholder="e.g. Senior ML Engineer" />
      </div>
      <div class="form-group">
        <label class="form-label" for="rg-email">Email *</label>
        <input id="rg-email" type="email" class="form-input" v-model="store.formData.personal.email" placeholder="priya@example.com" />
      </div>
      <div class="form-group">
        <label class="form-label" for="rg-phone">Phone</label>
        <input id="rg-phone" type="tel" class="form-input" v-model="store.formData.personal.phone" placeholder="+91 98765 43210" />
      </div>
      <div class="form-group">
        <label class="form-label" for="rg-location">Location</label>
        <input id="rg-location" type="text" class="form-input" v-model="store.formData.personal.location" placeholder="Mumbai, India" />
      </div>
      <div class="form-group">
        <label class="form-label" for="rg-linkedin">LinkedIn URL</label>
        <input id="rg-linkedin" type="text" class="form-input" v-model="store.formData.personal.linkedin" placeholder="linkedin.com/in/priyasharma" />
      </div>
      <div class="form-group">
        <label class="form-label" for="rg-github">GitHub URL</label>
        <input id="rg-github" type="text" class="form-input" v-model="store.formData.personal.github" placeholder="github.com/priyasharma" />
      </div>
      <div class="form-group">
        <label class="form-label" for="rg-website">Portfolio / Website</label>
        <input id="rg-website" type="text" class="form-input" v-model="store.formData.personal.website" placeholder="priyasharma.dev" />
      </div>
      <div class="form-group form-group--full">
        <label class="form-label">Profile Photo (Optional)</label>
        <div class="photo-upload-container">
          <div v-if="store.formData.personal.photo" class="photo-preview">
            <img :src="store.formData.personal.photo" alt="Profile Preview" />
            <button @click="store.formData.personal.photo = ''" class="remove-photo-btn">×</button>
          </div>
          <label v-else class="photo-upload-placeholder">
            <input type="file" @change="handlePhotoUpload($event, store.formData)" accept="image/*" class="photo-file-input" />
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
            <span>Upload Photo</span>
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useResumeStore } from '../../../stores/resume.js'
import { useResumeAI } from '../../../composables/useResumeAI.js'

const store = useResumeStore()
const { handlePhotoUpload } = useResumeAI()
</script>

<style scoped>
.photo-upload-container {
  margin-top: 0.5rem;
}

.photo-upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 120px;
  height: 120px;
  border: 2px dashed var(--clr-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
  color: var(--clr-text-muted);
}

.photo-upload-placeholder:hover {
  border-color: var(--clr-primary);
  color: var(--clr-primary);
  background: rgba(99, 102, 241, 0.05);
}

.photo-file-input {
  display: none;
}

.photo-preview {
  position: relative;
  width: 120px;
  height: 120px;
}

.photo-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: var(--radius-md);
  border: 1px solid var(--clr-border);
}

.remove-photo-btn {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--clr-danger);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

/* Form grid */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--sp-4);
}

.form-group--full {
  grid-column: 1 / -1;
}

@media (max-width: 600px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>

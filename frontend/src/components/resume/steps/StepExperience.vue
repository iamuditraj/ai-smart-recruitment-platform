<template>
  <div class="form-step">
    <div class="step-header-row">
      <div>
        <h2 class="step-title">Work Experience</h2>
        <p class="step-desc">Add your roles in reverse-chronological order.</p>
      </div>
      <button class="btn btn-primary" id="rg-add-exp-btn" @click="store.addExperience()">+ Add Role</button>
    </div>

    <div v-if="store.formData.experience.length === 0" class="rg-empty-hint">
      Click <strong>"+ Add Role"</strong> to start adding work experience.
    </div>

    <ResumeEntryBlock
      v-for="(exp, i) in store.formData.experience"
      :key="exp.id"
      :index="i"
      label="Role"
      @remove="store.removeExperience(exp.id)"
    >
      <div class="form-grid">
        <div class="form-group">
          <label class="form-label">Job Title</label>
          <input type="text" class="form-input" v-model="exp.title" placeholder="e.g. ML Engineer" :id="`rg-exp-title-${i}`"/>
        </div>
        <div class="form-group">
          <label class="form-label">Company</label>
          <input type="text" class="form-input" v-model="exp.company" placeholder="e.g. Google" :id="`rg-exp-company-${i}`"/>
        </div>
        <div class="form-group">
          <label class="form-label">Location</label>
          <input type="text" class="form-input" v-model="exp.location" placeholder="e.g. Bangalore, India" :id="`rg-exp-location-${i}`"/>
        </div>
        <div class="form-group form-group--check">
          <label class="rg-checkbox-label" :for="`rg-exp-current-${i}`">
            <input type="checkbox" :id="`rg-exp-current-${i}`" v-model="exp.current" />
            Currently working here
          </label>
        </div>
        <div class="form-group">
          <label class="form-label">Start Date</label>
          <input type="month" class="form-input" v-model="exp.startDate" :id="`rg-exp-start-${i}`"/>
        </div>
        <div class="form-group" v-if="!exp.current">
          <label class="form-label">End Date</label>
          <input type="month" class="form-input" v-model="exp.endDate" :id="`rg-exp-end-${i}`"/>
        </div>
      </div>
      <div class="form-group" style="margin-top: var(--sp-3)">
        <div class="flex items-center justify-between" style="margin-bottom: 4px; display: flex; justify-content: space-between; align-items: center;">
          <label class="form-label">Description / Achievements</label>
          <button
            class="btn-ghost rg-ai-btn-inline"
            :disabled="isGenerating"
            @click="generateAIExperience(store.formData, i)"
          >
            <span v-if="!isGenerating">✨ Improve with AI</span>
            <AppSpinner v-else size="sm" />
          </button>
        </div>
        <textarea class="form-input" v-model="exp.description" rows="4"
          :id="`rg-exp-desc-${i}`"
          placeholder="• Led a team of 4 engineers to build an NLP-based resume parser reducing screening time by 60%&#10;• Deployed models serving 10K+ requests/day on AWS SageMaker...">
        </textarea>
      </div>
    </ResumeEntryBlock>
  </div>
</template>

<script setup>
import { useResumeStore } from '../../../stores/resume.js'
import { useResumeAI } from '../../../composables/useResumeAI.js'
import AppSpinner from '@/components/AppSpinner.vue'
import ResumeEntryBlock from '@/components/ResumeEntryBlock.vue'

const store = useResumeStore()
const { generateAIExperience, isGenerating } = useResumeAI()
</script>

<style scoped>
/* Entry Block */


/* Empty Hint */
.rg-empty-hint {
  background: var(--clr-surface-2);
  border: 1px dashed var(--clr-border-hover);
  border-radius: var(--radius-md);
  padding: var(--sp-6);
  text-align: center;
  color: var(--clr-text-muted);
  font-size: 0.875rem;
  margin-top: var(--sp-4);
}

.rg-ai-btn-inline {
  background: none;
  border: none;
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--clr-primary-2);
  cursor: pointer;
  padding: 0;
}
.rg-ai-btn-inline:hover { text-decoration: underline; }



/* Form grid */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--sp-4);
}

.form-group--check {
  display: flex;
  align-items: center;
  padding-top: 1.4rem;
}

.rg-checkbox-label {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  cursor: pointer;
  font-size: 0.875rem;
  color: var(--clr-text-light);
}

.rg-checkbox-label input {
  accent-color: var(--clr-primary);
  width: 15px;
  height: 15px;
}

@media (max-width: 600px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>

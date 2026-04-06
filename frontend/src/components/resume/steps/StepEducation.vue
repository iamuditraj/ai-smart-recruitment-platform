<template>
  <div class="form-step">
    <div class="step-header-row">
      <div>
        <h2 class="step-title">Education</h2>
        <p class="step-desc">List your highest degree first.</p>
      </div>
      <button class="btn btn-primary" id="rg-add-edu-btn" @click="store.addEducation()">+ Add Education</button>
    </div>

    <div v-if="store.formData.education.length === 0" class="rg-empty-hint">
      Click <strong>"+ Add Education"</strong> to add your academic background.
    </div>

    <ResumeEntryBlock
      v-for="(edu, i) in store.formData.education"
      :key="edu.id"
      :index="i"
      label="Education"
      @remove="store.removeEducation(edu.id)"
    >
      <div class="form-grid">
        <div class="form-group form-group--full">
          <label class="form-label">Degree / Qualification</label>
          <input type="text" class="form-input" v-model="edu.degree" placeholder="e.g. B.Tech in Computer Science" :id="`rg-edu-degree-${i}`"/>
        </div>
        <div class="form-group">
          <label class="form-label">Institution</label>
          <input type="text" class="form-input" v-model="edu.institution" placeholder="e.g. IIT Bombay" :id="`rg-edu-inst-${i}`"/>
        </div>
        <div class="form-group">
          <label class="form-label">Location</label>
          <input type="text" class="form-input" v-model="edu.location" placeholder="e.g. Mumbai, India" :id="`rg-edu-loc-${i}`"/>
        </div>
        <div class="form-group">
          <label class="form-label">Start Year</label>
          <input type="number" class="form-input" v-model="edu.startYear" placeholder="2019" min="1990" max="2030" :id="`rg-edu-start-${i}`"/>
        </div>
        <div class="form-group">
          <label class="form-label">End Year</label>
          <input type="number" class="form-input" v-model="edu.endYear" placeholder="2023" min="1990" max="2030" :id="`rg-edu-end-${i}`"/>
        </div>
        <div class="form-group">
          <label class="form-label">CGPA / GPA</label>
          <input type="text" class="form-input" v-model="edu.gpa" placeholder="e.g. 8.7 / 10" :id="`rg-edu-gpa-${i}`"/>
        </div>
      </div>
    </ResumeEntryBlock>
  </div>
</template>

<script setup>
import { useResumeStore } from '../../../stores/resume.js'
import ResumeEntryBlock from '../../ResumeEntryBlock.vue'

const store = useResumeStore()
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

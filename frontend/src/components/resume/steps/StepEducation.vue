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

    <div v-for="(edu, i) in store.formData.education" :key="edu.id" class="rg-entry-block">
      <div class="rg-entry-block__header">
        <span class="rg-entry-index">Education {{ i + 1 }}</span>
        <button class="btn btn-ghost rg-remove-btn" :id="`rg-remove-edu-${i}`" @click="store.removeEducation(edu.id)">Remove</button>
      </div>
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
    </div>
  </div>
</template>

<script setup>
import { useResumeStore } from '../../../stores/resume.js'

const store = useResumeStore()
</script>

<style scoped>
/* Entry Block */
.rg-entry-block {
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-md);
  padding: var(--sp-4) var(--sp-5);
  display: flex;
  flex-direction: column;
  gap: var(--sp-3);
  margin-top: var(--sp-4);
}

.rg-entry-block__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.rg-entry-index {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--clr-primary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.rg-remove-btn {
  font-size: 0.8rem;
  color: var(--clr-danger);
  padding: 0.3rem 0.6rem;
}

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

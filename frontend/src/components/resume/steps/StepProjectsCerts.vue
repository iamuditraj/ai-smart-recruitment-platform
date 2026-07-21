<template>
  <div class="form-step">
    <!-- Projects -->
    <div class="step-header-row">
      <div>
        <h2 class="step-title">Projects</h2>
        <p class="step-desc">Showcase your most relevant work.</p>
      </div>
      <button class="btn btn-primary" id="rg-add-proj-btn" @click="store.addProject()">+ Add Project</button>
    </div>

    <div v-if="store.formData.projects.length === 0" class="rg-empty-hint">
      Click <strong>"+ Add Project"</strong> to add your projects.
    </div>

    <div v-for="(proj, i) in store.formData.projects" :key="proj.id" class="rg-entry-block">
      <div class="rg-entry-block__header">
        <span class="rg-entry-index">Project {{ i + 1 }}</span>
        <button class="btn btn-ghost rg-remove-btn" :id="`rg-remove-proj-${i}`" @click="store.removeProject(proj.id)">Remove</button>
      </div>
      <div class="form-grid">
        <div class="form-group">
          <label class="form-label">Project Name</label>
          <input type="text" class="form-input" v-model="proj.name" placeholder="e.g. AI Resume Screener" :id="`rg-proj-name-${i}`"/>
        </div>
        <div class="form-group">
          <label class="form-label">Tech Stack (comma-separated)</label>
          <input type="text" class="form-input" v-model="proj.tech" placeholder="Python, FastAPI, Vue.js" :id="`rg-proj-tech-${i}`"/>
        </div>
        <div class="form-group form-group--full">
          <label class="form-label">Project URL / GitHub Link</label>
          <input type="text" class="form-input" v-model="proj.link" placeholder="https://github.com/..." :id="`rg-proj-link-${i}`"/>
        </div>
      </div>
      <div class="form-group" style="margin-top: var(--sp-3)">
        <label class="form-label">Description</label>
        <textarea class="form-input" v-model="proj.description" rows="3" :id="`rg-proj-desc-${i}`"
          placeholder="Brief description of what the project does and your contributions...">
        </textarea>
      </div>
    </div>

    <!-- Certifications -->
    <div class="step-header-row" style="margin-top: var(--sp-8)">
      <div>
        <h2 class="step-title">Certifications</h2>
        <p class="step-desc">Optional: add any professional certifications.</p>
      </div>
      <button class="btn btn-outline" id="rg-add-cert-btn" @click="store.addCertification()">+ Add Cert</button>
    </div>

    <div v-for="(cert, i) in store.formData.certifications" :key="cert.id" class="rg-entry-block">
      <div class="rg-entry-block__header">
        <span class="rg-entry-index">Cert {{ i + 1 }}</span>
        <button class="btn btn-ghost rg-remove-btn" :id="`rg-remove-cert-${i}`" @click="store.removeCertification(cert.id)">Remove</button>
      </div>
      <div class="form-grid cert-grid">
        <div class="form-group">
          <label class="form-label">Certification Name</label>
          <input type="text" class="form-input" v-model="cert.name" placeholder="e.g. AWS Certified ML Specialist" :id="`rg-cert-name-${i}`"/>
        </div>
        <div class="form-group">
          <label class="form-label">Issuing Organization</label>
          <input type="text" class="form-input" v-model="cert.issuer" placeholder="e.g. Amazon Web Services" :id="`rg-cert-issuer-${i}`"/>
        </div>
        <div class="form-group">
          <label class="form-label">Year</label>
          <input type="number" class="form-input" v-model="cert.year" placeholder="2024" min="2000" max="2030" :id="`rg-cert-year-${i}`"/>
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

.cert-grid {
  grid-template-columns: 1fr 1fr 1fr;
}

@media (max-width: 800px) {
  .cert-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 600px) {
  .form-grid, .cert-grid {
    grid-template-columns: 1fr;
  }
}
</style>

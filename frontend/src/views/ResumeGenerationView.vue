<template>
  <div class="rg-page">
    <div class="rg-container container">

      <!-- ===== Page Header ===== -->
      <div class="rg-header animate-fade-in-up">
        <div>
          <h1 class="rg-title">Resume Builder</h1>
          <p class="rg-subtitle">Fill in your details and get a professional resume instantly</p>
        </div>
        <div class="rg-header-actions">
          <button class="btn btn-ghost" id="rg-reset-btn" @click="confirmReset">Reset</button>
          <button class="btn btn-outline" id="rg-print-btn" @click="printResume">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
            Download PDF
          </button>
        </div>
      </div>

      <!-- ===== Main Split Layout ===== -->
      <div class="rg-split">

        <!-- ====== LEFT: Form Panel ====== -->
        <div class="rg-form-panel">

          <!-- Step Progress -->
          <div class="rg-stepper" id="rg-stepper">
            <div
              v-for="(step, i) in steps"
              :key="step.id"
              class="rg-step"
              :class="{
                'rg-step--active':    currentStep === i,
                'rg-step--done':      currentStep > i,
              }"
              :id="`rg-step-indicator-${i}`"
              @click="goToStep(i)"
            >
              <div class="rg-step__bullet">
                <svg v-if="currentStep > i" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                <span v-else>{{ i + 1 }}</span>
              </div>
              <span class="rg-step__label">{{ step.label }}</span>
            </div>
          </div>

          <!-- Step Content -->
          <div class="rg-form-body card">
            <Transition name="stepslide" mode="out-in">
              <div :key="currentStep">

                <!-- ---- Step 0: Personal Info ---- -->
                <div v-if="currentStep === 0" class="form-step">
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
                  </div>
                </div>

                <!-- ---- Step 1: Summary ---- -->
                <div v-else-if="currentStep === 1" class="form-step">
                  <h2 class="step-title">Professional Summary</h2>
                  <p class="step-desc">A 2–4 sentence overview of your experience and value proposition.</p>
                  <div class="form-group">
                    <label class="form-label" for="rg-summary">Summary</label>
                    <textarea
                      id="rg-summary"
                      class="form-input rg-textarea"
                      v-model="store.formData.summary"
                      rows="8"
                      placeholder="e.g. Results-driven ML Engineer with 5+ years of experience building NLP and computer vision systems. Passionate about deploying AI models at scale..."
                    ></textarea>
                    <span class="rg-char-count">{{ store.formData.summary.length }} characters</span>
                  </div>

                  <!-- AI Tip -->
                  <div class="rg-tip">
                    <span class="rg-tip__icon">💡</span>
                    <span>Include your years of experience, top technical skills, and a key achievement.</span>
                  </div>
                </div>

                <!-- ---- Step 2: Experience ---- -->
                <div v-else-if="currentStep === 2" class="form-step">
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

                  <div v-for="(exp, i) in store.formData.experience" :key="exp.id" class="rg-entry-block">
                    <div class="rg-entry-block__header">
                      <span class="rg-entry-index">Role {{ i + 1 }}</span>
                      <button class="btn btn-ghost rg-remove-btn" :id="`rg-remove-exp-${i}`" @click="store.removeExperience(exp.id)">Remove</button>
                    </div>
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
                      <label class="form-label">Description / Achievements</label>
                      <textarea class="form-input" v-model="exp.description" rows="4"
                        :id="`rg-exp-desc-${i}`"
                        placeholder="• Led a team of 4 engineers to build an NLP-based resume parser reducing screening time by 60%&#10;• Deployed models serving 10K+ requests/day on AWS SageMaker...">
                      </textarea>
                    </div>
                  </div>
                </div>

                <!-- ---- Step 3: Education ---- -->
                <div v-else-if="currentStep === 3" class="form-step">
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

                <!-- ---- Step 4: Skills ---- -->
                <div v-else-if="currentStep === 4" class="form-step">
                  <h2 class="step-title">Skills</h2>
                  <p class="step-desc">Type a skill and press <kbd>Enter</kbd> or comma to add it.</p>

                  <!-- Technical Skills -->
                  <div class="form-group">
                    <label class="form-label" for="rg-tech-skill-input">Technical Skills</label>
                    <div class="rg-tag-input">
                      <div class="rg-tag-input__tags">
                        <span
                          v-for="skill in store.formData.skills.technical"
                          :key="skill"
                          class="rg-skill-tag"
                          :id="`rg-tech-tag-${skill}`"
                        >
                          {{ skill }}
                          <button @click="store.removeSkill('technical', skill)" class="rg-tag-remove" :aria-label="`Remove ${skill}`">×</button>
                        </span>
                      </div>
                      <input
                        id="rg-tech-skill-input"
                        type="text"
                        class="rg-tag-field"
                        v-model="techInput"
                        placeholder="e.g. Python, TensorFlow..."
                        @keydown.enter.prevent="addTechSkill"
                        @keydown.188.prevent="addTechSkill"
                      />
                    </div>
                    <p class="rg-input-hint">{{ store.formData.skills.technical.length }} skills added</p>
                  </div>

                  <!-- Soft Skills -->
                  <div class="form-group" style="margin-top: var(--sp-6)">
                    <label class="form-label" for="rg-soft-skill-input">Soft Skills</label>
                    <div class="rg-tag-input">
                      <div class="rg-tag-input__tags">
                        <span
                          v-for="skill in store.formData.skills.soft"
                          :key="skill"
                          class="rg-skill-tag rg-skill-tag--soft"
                          :id="`rg-soft-tag-${skill}`"
                        >
                          {{ skill }}
                          <button @click="store.removeSkill('soft', skill)" class="rg-tag-remove">×</button>
                        </span>
                      </div>
                      <input
                        id="rg-soft-skill-input"
                        type="text"
                        class="rg-tag-field"
                        v-model="softInput"
                        placeholder="e.g. Leadership, Communication..."
                        @keydown.enter.prevent="addSoftSkill"
                        @keydown.188.prevent="addSoftSkill"
                      />
                    </div>
                    <p class="rg-input-hint">{{ store.formData.skills.soft.length }} skills added</p>
                  </div>
                </div>

                <!-- ---- Step 5: Projects & Certifications ---- -->
                <div v-else-if="currentStep === 5" class="form-step">
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
                    <div class="form-grid">
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

                <!-- ---- Step 6: Review & Export ---- -->
                <div v-else-if="currentStep === 6" class="form-step">
                  <ReviewStep
                    :structured="store.structuredResume"
                    :validation="store.validationResult"
                    :breakdown="store.completenessBreakdown"
                    :score="store.completenessScore"
                    @print="printResume"
                  />
                </div>

              </div>
            </Transition>

            <!-- Navigation Buttons -->
            <div class="rg-form-nav">
              <button class="btn btn-outline" id="rg-prev-btn" :disabled="currentStep === 0" @click="currentStep--">
                ← Back
              </button>
              <span class="rg-step-counter">{{ currentStep + 1 }} / {{ steps.length }}</span>
              <button
                v-if="currentStep < steps.length - 1"
                class="btn btn-primary"
                id="rg-next-btn"
                @click="nextStep"
              >
                Next →
              </button>
              <button
                v-else
                class="btn btn-primary"
                id="rg-finish-btn"
                @click="printResume"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
                Download PDF
              </button>
            </div>
          </div>
        </div>

        <!-- ====== RIGHT: Preview Panel ====== -->
        <div class="rg-preview-panel">
          <div class="rg-preview-header">
            <span class="rg-preview-label">Live Preview</span>
            <!-- Template Switcher -->
            <div class="rg-template-switcher" id="rg-template-switcher">
              <button
                v-for="tmpl in templates"
                :key="tmpl.id"
                class="rg-tmpl-btn"
                :class="{ 'rg-tmpl-btn--active': store.selectedTemplate === tmpl.id }"
                :id="`rg-tmpl-btn-${tmpl.id}`"
                @click="store.selectedTemplate = tmpl.id"
              >
                {{ tmpl.label }}
              </button>
            </div>
          </div>

          <!-- Scaled Resume Preview -->
          <div class="rg-preview-scroll">
            <div class="rg-preview-scale-outer" id="rg-preview-wrapper">
              <div class="rg-preview-scale-inner" :style="{ transform: `scale(${previewScale})`, transformOrigin: 'top left' }">
                <div id="printable-resume">
                  <ClassicTemplate v-if="store.selectedTemplate === 'classic'" :data="store.formData" />
                  <ModernTemplate  v-else-if="store.selectedTemplate === 'modern'" :data="store.formData" />
                  <MinimalTemplate v-else-if="store.selectedTemplate === 'minimal'" :data="store.formData" />
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Print styles are injected globally via a style tag below -->
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useResumeStore } from '../stores/resume.js'

import ClassicTemplate from '../components/resume/ClassicTemplate.vue'
import ModernTemplate  from '../components/resume/ModernTemplate.vue'
import MinimalTemplate from '../components/resume/MinimalTemplate.vue'
import ReviewStep      from '../components/resume/ReviewStep.vue'

const store = useResumeStore()

const currentStep = ref(0)
const techInput  = ref('')
const softInput  = ref('')

const steps = [
  { id: 'personal',    label: 'Personal'    },
  { id: 'summary',     label: 'Summary'     },
  { id: 'experience',  label: 'Experience'  },
  { id: 'education',   label: 'Education'   },
  { id: 'skills',      label: 'Skills'      },
  { id: 'projects',    label: 'Projects'    },
  { id: 'review',      label: 'Review'      },
]

const templates = [
  { id: 'classic', label: 'Classic' },
  { id: 'modern',  label: 'Modern'  },
  { id: 'minimal', label: 'Minimal' },
]

// Responsive preview scale
const previewScale = ref(0.5)

function computePreviewScale() {
  const wrapperEl = document.querySelector('.rg-preview-scale-outer')
  if (!wrapperEl) return
  const availWidth = wrapperEl.clientWidth - 16
  previewScale.value = Math.min(availWidth / 794, 0.7)
}

onMounted(() => {
  computePreviewScale()
  window.addEventListener('resize', computePreviewScale)
})
onUnmounted(() => window.removeEventListener('resize', computePreviewScale))

// Step navigation
function goToStep(i) {
  // Auto-save snapshot when arriving at the Review step
  if (i === steps.length - 1) store.saveSnapshot()
  currentStep.value = i
}

// Override next button to trigger snapshot on entering review
function nextStep() {
  if (currentStep.value === steps.length - 2) store.saveSnapshot()
  currentStep.value++
}

// Skill input
function addTechSkill() {
  store.addSkill('technical', techInput.value)
  techInput.value = ''
}
function addSoftSkill() {
  store.addSkill('soft', softInput.value)
  softInput.value = ''
}

// Print / PDF
function printResume() {
  window.print()
}

// Reset
function confirmReset() {
  if (confirm('Reset all resume data? This cannot be undone.')) {
    store.resetForm()
    currentStep.value = 0
  }
}
</script>

<style scoped>
/* ===== Page Layout ===== */
.rg-page {
  min-height: 100vh;
  padding-block: var(--sp-8);
}

.rg-container {
  max-width: 1400px;
}

/* Header */
.rg-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--sp-4);
  margin-bottom: var(--sp-8);
  flex-wrap: wrap;
}

.rg-title    { font-size: 2rem; font-weight: 800; letter-spacing: -0.02em; }
.rg-subtitle { color: var(--clr-text-muted); margin-top: var(--sp-1); }

.rg-header-actions {
  display: flex;
  gap: var(--sp-3);
  align-items: center;
}

/* ===== Split Layout ===== */
.rg-split {
  display: grid;
  grid-template-columns: 1fr 420px;
  gap: var(--sp-6);
  align-items: start;
}

/* ===== Form Panel ===== */
.rg-form-panel {
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
  min-width: 0;
}

/* Step Progress */
.rg-stepper {
  display: flex;
  gap: 0;
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  flex-wrap: wrap;
}

.rg-step {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  padding: 0.7rem 1rem;
  cursor: pointer;
  flex: 1;
  min-width: 80px;
  transition: background var(--transition-fast);
  position: relative;
}

.rg-step::after {
  content: '';
  position: absolute;
  right: 0;
  top: 25%;
  height: 50%;
  width: 1px;
  background: var(--clr-border);
}

.rg-step:last-child::after { display: none; }

.rg-step:hover {
  background: rgba(255,255,255,0.03);
}

.rg-step--active {
  background: rgba(99,102,241,0.1);
}

.rg-step__bullet {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 1.5px solid var(--clr-border-hover);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 700;
  flex-shrink: 0;
  color: var(--clr-text-muted);
  transition: all var(--transition-base);
}

.rg-step--active .rg-step__bullet {
  background: var(--clr-primary);
  border-color: var(--clr-primary);
  color: white;
  box-shadow: 0 0 12px rgba(99,102,241,0.4);
}

.rg-step--done .rg-step__bullet {
  background: var(--clr-success);
  border-color: var(--clr-success);
  color: white;
}

.rg-step__label {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--clr-text-muted);
  white-space: nowrap;
}

.rg-step--active .rg-step__label {
  color: var(--clr-primary);
}
.rg-step--done .rg-step__label {
  color: var(--clr-success);
}

/* Form Body Card */
.rg-form-body {
  display: flex;
  flex-direction: column;
  gap: var(--sp-6);
  padding: var(--sp-8);
  min-height: 500px;
}

.form-step {
  display: flex;
  flex-direction: column;
  gap: var(--sp-5);
}

.step-title { font-size: 1.3rem; font-weight: 700; letter-spacing: -0.01em; }
.step-desc  { color: var(--clr-text-muted); font-size: 0.875rem; margin-top: -var(--sp-3); }

.step-header-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--sp-4);
  flex-wrap: wrap;
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

/* Textarea */
.rg-textarea {
  resize: vertical;
  min-height: 140px;
  line-height: 1.7;
}

.rg-char-count {
  font-size: 0.75rem;
  color: var(--clr-text-muted);
  text-align: right;
}

/* Tip */
.rg-tip {
  display: flex;
  align-items: flex-start;
  gap: var(--sp-3);
  background: rgba(99,102,241,0.07);
  border: 1px solid rgba(99,102,241,0.2);
  border-radius: var(--radius-md);
  padding: var(--sp-4);
  font-size: 0.85rem;
  color: var(--clr-text-light);
}

.rg-tip__icon { font-size: 1.1rem; flex-shrink: 0; }

/* Entry Block */
.rg-entry-block {
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-md);
  padding: var(--sp-4) var(--sp-5);
  display: flex;
  flex-direction: column;
  gap: var(--sp-3);
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
}

/* Tag Input */
.rg-tag-input {
  background: var(--clr-surface-2);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-md);
  padding: var(--sp-3);
  display: flex;
  flex-direction: column;
  gap: var(--sp-2);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.rg-tag-input:focus-within {
  border-color: var(--clr-primary);
  box-shadow: 0 0 0 3px rgba(99,102,241,0.15);
}

.rg-tag-input__tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sp-2);
}

.rg-skill-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: rgba(99,102,241,0.12);
  border: 1px solid rgba(99,102,241,0.3);
  border-radius: var(--radius-full);
  padding: 0.2rem 0.6rem 0.2rem 0.8rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: #a5b4fc;
}

.rg-skill-tag--soft {
  background: rgba(16,185,129,0.1);
  border-color: rgba(16,185,129,0.3);
  color: #6ee7b7;
}

.rg-tag-remove {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  opacity: 0.7;
  padding: 0;
  transition: opacity var(--transition-fast);
}

.rg-tag-remove:hover { opacity: 1; }

.rg-tag-field {
  background: none;
  border: none;
  outline: none;
  color: var(--clr-text);
  font-size: 0.875rem;
  font-family: var(--font-body);
  width: 100%;
  padding: var(--sp-1) var(--sp-2);
}

.rg-tag-field::placeholder { color: var(--clr-text-muted); }

.rg-input-hint {
  font-size: 0.75rem;
  color: var(--clr-text-muted);
  margin-top: var(--sp-1);
}

/* Form Nav */
.rg-form-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-4);
  margin-top: auto;
  padding-top: var(--sp-4);
  border-top: 1px solid var(--clr-border);
}

.rg-step-counter {
  font-size: 0.85rem;
  color: var(--clr-text-muted);
  font-weight: 600;
}

.btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
  transform: none !important;
}

kbd {
  background: var(--clr-surface-3);
  border: 1px solid var(--clr-border-hover);
  border-radius: 4px;
  padding: 0.1rem 0.4rem;
  font-size: 0.8em;
  font-family: monospace;
}

/* ===== Preview Panel ===== */
.rg-preview-panel {
  position: sticky;
  top: 80px;
  display: flex;
  flex-direction: column;
  gap: var(--sp-3);
}

.rg-preview-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-3);
  flex-wrap: wrap;
}

.rg-preview-label {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--clr-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.rg-template-switcher {
  display: flex;
  gap: var(--sp-1);
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-full);
  padding: 3px;
}

.rg-tmpl-btn {
  padding: 0.3rem 0.85rem;
  border-radius: var(--radius-full);
  border: none;
  background: none;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--clr-text-muted);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-family: var(--font-body);
}

.rg-tmpl-btn:hover { color: var(--clr-text); }

.rg-tmpl-btn--active {
  background: var(--gradient-brand);
  color: white;
  box-shadow: 0 2px 8px rgba(99,102,241,0.3);
}

/* Preview Scale Wrapper */
.rg-preview-scroll {
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  padding: 8px;
}

.rg-preview-scale-outer {
  width: 100%;
  overflow: hidden;
}

.rg-preview-scale-inner {
  width: 794px;  /* A4 width in px at 96dpi */
}

/* ===== Step Slide Transition ===== */
.stepslide-enter-active, .stepslide-leave-active {
  transition: all 0.2s ease;
}
.stepslide-enter-from {
  opacity: 0;
  transform: translateX(16px);
}
.stepslide-leave-to {
  opacity: 0;
  transform: translateX(-16px);
}

/* ===== Responsive ===== */
@media (max-width: 1100px) {
  .rg-split {
    grid-template-columns: 1fr;
  }
  .rg-preview-panel {
    position: static;
    order: -1;
  }
}

@media (max-width: 600px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  .rg-step__label {
    display: none;
  }
}
</style>

<style>
/* ===== Global Print Styles ===== */
@media print {
  body * { visibility: hidden !important; }
  #printable-resume,
  #printable-resume * {
    visibility: visible !important;
  }
  #printable-resume {
    position: fixed !important;
    inset: 0 !important;
    transform: none !important;
    width: 210mm !important;
    min-height: 297mm !important;
    margin: 0 !important;
    padding: 0 !important;
    z-index: 9999 !important;
    background: white !important;
  }
  /* Override dark theme for print */
  .classic-resume,
  .modern-resume,
  .minimal-resume {
    color: #111 !important;
  }
}
</style>

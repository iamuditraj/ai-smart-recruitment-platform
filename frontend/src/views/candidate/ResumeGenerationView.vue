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
          <button class="btn btn-outline hide-desktop" @click="isPreviewVisible = !isPreviewVisible">
            {{ isPreviewVisible ? 'Hide Preview' : 'Show Preview' }}
          </button>
          <button class="btn btn-ghost hide-mobile" id="rg-reset-btn" @click="confirmReset">Reset</button>
          <button class="btn btn-outline" id="rg-print-btn" @click="printResume">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
            Download PDF
          </button>
        </div>
      </div>

      <!-- ===== Main Split Layout ===== -->
      <div class="rg-split" :class="{ 'rg-show-preview': isPreviewVisible }">

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
                'rg-step--done':      isStepDone(i, store.formData)
              }"
              :id="`rg-step-indicator-${i}`"
              @click="goToStep(i, store.saveSnapshot)"
            >
              <div class="rg-step__bullet">
                <svg v-if="isStepDone(i, store.formData)" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                <span v-else>{{ i + 1 }}</span>
              </div>
              <span class="rg-step__label">{{ step.label }}</span>
            </div>
          </div>

          <!-- Step Content -->
          <div class="rg-form-body card">
            <Transition name="stepslide" mode="out-in">
              <div :key="currentStep">
                <StepPersonal      v-if="currentStep === 0" />
                <StepSummary       v-else-if="currentStep === 1" />
                <StepExperience    v-else-if="currentStep === 2" />
                <StepEducation     v-else-if="currentStep === 3" />
                <StepSkills        v-else-if="currentStep === 4" />
                <StepProjectsCerts v-else-if="currentStep === 5" />
                <div v-else-if="currentStep === 6" class="form-step">
                  <ReviewStep
                    :structured="store.structuredResume"
                    :validation="store.validationResult"
                    :breakdown="store.completenessBreakdown"
                    :score="store.completenessScore"
                    :is-submitting="store.isSaving"
                    @print="printResume"
                    @save="handleSubmit"
                  />
                  <div v-if="submitStatus" class="rg-status-toast" :class="submitStatus.type">
                    {{ submitStatus.message }}
                  </div>
                </div>
              </div>
            </Transition>

            <!-- Navigation Buttons -->
            <div class="rg-form-nav">
              <button class="btn btn-outline" id="rg-prev-btn" :disabled="currentStep === 0" @click="prevStep()">
                ← Back
              </button>
              <span class="rg-step-counter">{{ currentStep + 1 }} / {{ steps.length }}</span>
              <button
                v-if="currentStep < steps.length - 1"
                class="btn btn-primary"
                id="rg-next-btn"
                @click="nextStep(store.saveSnapshot)"
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
            <span class="rg-preview-label">Live Preview (Minimal)</span>
            <span v-if="isGenerating" class="rg-ai-indicator">
              <span class="rg-ai-dot"></span> AI generating…
            </span>
          </div>

          <!-- Scaled Resume Preview -->
          <div class="rg-preview-scroll">
            <div class="rg-preview-scale-outer" id="rg-preview-wrapper">
              <div class="rg-preview-scale-inner" :style="{ transform: `scale(${previewScale})`, transformOrigin: 'top left' }">
                <MinimalTemplate :data="store.formData" />
              </div>
            </div>
            <!-- Hidden print target — lives outside the scaled container -->
            <Teleport to="body">
              <div id="printable-resume" aria-hidden="true">
                <MinimalTemplate :data="store.formData" />
              </div>
            </Teleport>
          </div>
        </div>

      </div>
    </div>

    <!-- Print styles are injected globally via a style tag below -->
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useResumeStore } from '../../stores/resume.js'
import { useResumeWizard } from '../../composables/useResumeWizard.js'
import { useResumeAI } from '../../composables/useResumeAI.js'

import StepPersonal from '../../components/resume/steps/StepPersonal.vue'
import StepSummary from '../../components/resume/steps/StepSummary.vue'
import StepExperience from '../../components/resume/steps/StepExperience.vue'
import StepEducation from '../../components/resume/steps/StepEducation.vue'
import StepSkills from '../../components/resume/steps/StepSkills.vue'
import StepProjectsCerts from '../../components/resume/steps/StepProjectsCerts.vue'

import MinimalTemplate from '../../components/resume/MinimalTemplate.vue'
import ReviewStep      from '../../components/resume/ReviewStep.vue'

const store = useResumeStore()
const { steps, currentStep, isStepDone, goToStep, nextStep, prevStep } = useResumeWizard()
const { isGenerating } = useResumeAI()

// Responsive preview scale
const previewScale = ref(0.5)
const isPreviewVisible = ref(false)

function computePreviewScale() {
  const wrapperEl = document.getElementById('rg-preview-wrapper')
  const innerEl = document.querySelector('.rg-preview-scale-inner')
  if (!wrapperEl || !innerEl) return
  
  const availWidth = wrapperEl.clientWidth
  if (availWidth === 0) return

  const scale = Math.min(availWidth / 794, 0.7)
  previewScale.value = scale
  
  // Force the wrapper height to match the scaled height of the content
  // This removes "ghost space" below the scaled element.
  nextTick(() => {
    const rect = innerEl.getBoundingClientRect()
    wrapperEl.style.height = `${rect.height}px`
  })
}

// Re-calculate scale on mount, resize, and data changes
onMounted(() => {
  setTimeout(computePreviewScale, 100) // Small delay for layout
  window.addEventListener('resize', computePreviewScale)
})
onUnmounted(() => window.removeEventListener('resize', computePreviewScale))

watch(() => store.formData, () => {
  computePreviewScale()
}, { deep: true })

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

// Platform Submission
const submitStatus = ref(null)

async function handleSubmit() {
  try {
    await store.saveToFirestore()
    submitStatus.value = { type: 'success', message: 'Resume successfully saved to platform!' }
    setTimeout(() => { submitStatus.value = null }, 5000)
  } catch {
    submitStatus.value = { type: 'error', message: 'Failed to save resume. Please check your backend connection.' }
  }
}
</script>

<style scoped>
.rg-status-toast {
  margin-top: var(--sp-4);
  padding: var(--sp-3) var(--sp-4);
  border-radius: var(--radius-md);
  font-size: 0.85rem;
  font-weight: 600;
  text-align: center;
  animation: fade-in 0.3s ease;
}
.rg-status-toast.success { background: rgba(16,185,129,0.1); color: #10b981; border: 1px solid rgba(16,185,129,0.2); }
.rg-status-toast.error { background: rgba(239,68,68,0.1); color: #ef4444; border: 1px solid rgba(239,68,68,0.2); }

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
  overflow-x: auto;
  overflow-y: hidden;
  scrollbar-width: none;   /* Firefox */
}
.rg-stepper::-webkit-scrollbar { display: none; } /* Chrome/Safari */

.rg-step {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0.65rem 1rem;
  cursor: pointer;
  flex: 1;
  min-width: 110px;   /* enough to show the longest label without truncating */
  transition: background var(--transition-fast);
  position: relative;
  flex-shrink: 0;
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
  font-size: 0.75rem;
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

/* Make form step utility class available to internal components like ReviewStep when wrapping */
::v-deep .form-step {
  display: flex;
  flex-direction: column;
  gap: var(--sp-5);
}

::v-deep .step-title { font-size: 1.3rem; font-weight: 700; letter-spacing: -0.01em; }
::v-deep .step-desc  { color: var(--clr-text-muted); font-size: 0.875rem; margin-top: -var(--sp-3); }
::v-deep .step-header-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--sp-4);
  flex-wrap: wrap;
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

#printable-resume {
  display: none;
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

/* On small screens, keep stepper scrollable — labels stay visible */
@media (max-width: 900px) {
  .rg-step {
    padding: 0.65rem 0.75rem;
    min-width: 80px;
  }
}

@media (max-width: 768px) {
  .rg-split {
    gap: var(--sp-3);
  }

  .rg-preview-panel {
    display: none;
  }

  .rg-show-preview .rg-preview-panel {
    display: flex;
  }

  .rg-form-body {
    padding: var(--sp-4);
  }

  .rg-form-nav .btn {
    min-width: 80px;
  }
}

@media (max-width: 500px) {
  .rg-step__bullet {
    width: 18px;
    height: 18px;
    font-size: 9px;
  }
}

/* AI generating indicator */
.rg-ai-indicator {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--clr-primary);
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.2);
  padding: 3px 10px;
  border-radius: 999px;
}

.rg-ai-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--clr-primary);
  animation: rg-pulse 1s ease-in-out infinite;
  flex-shrink: 0;
}

@keyframes rg-pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.4; transform: scale(0.7); }
}
</style>

<style>
/* ===== Global Print Styles ===== */
@media print {
  body > *:not(#printable-resume) {
    display: none !important;
  }
  #printable-resume {
    display: block !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    width: 210mm !important;
    min-height: 297mm !important;
    transform: none !important;
    margin: 0 !important;
    padding: 0 !important;
    background: white !important;
    z-index: 9999 !important;
  }
  .minimal-resume,
  .classic-resume,
  .modern-resume {
    color: #111 !important;
    background: white !important;
  }
}
</style>

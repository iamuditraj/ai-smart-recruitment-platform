<template>
  <div class="form-step">
    <div class="step-header-row">
      <div>
        <h2 class="step-title">Professional Summary</h2>
        <p class="step-desc">A 2–4 sentence overview of your experience and value proposition.</p>
      </div>
      <button
        class="btn btn-outline btn-sm rg-ai-btn"
        :disabled="isGenerating"
        @click="generateAISummary(store.formData)"
      >
        <span v-if="!isGenerating">✨ AI Generate</span>
        <span v-else class="loader-sm"></span>
      </button>
    </div>
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
</template>

<script setup>
import { useResumeStore } from '../../../stores/resume.js'
import { useResumeAI } from '../../../composables/useResumeAI.js'

const store = useResumeStore()
const { generateAISummary, isGenerating } = useResumeAI()
</script>

<style scoped>
.rg-ai-btn {
  font-size: 0.75rem;
  padding: 0.35rem 0.8rem;
  border-color: var(--clr-primary-2);
  color: var(--clr-primary-2);
}
.rg-ai-btn:hover {
  background: rgba(139,92,246,0.1);
}

.loader-sm {
  width: 12px;
  height: 12px;
  border: 2px solid rgba(255,255,255,0.2);
  border-top-color: currentColor;
  border-radius: 50%;
  animation: rotate 1s linear infinite;
  display: inline-block;
}

@keyframes rotate { to { transform: rotate(360deg); } }

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
  display: block;
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
</style>

<template>
  <div class="skill-assessment">
    <div class="content-area">
      <div class="page-header animate-fade-in-up">
        <div>
          <h1 class="page-title">Skill Assessment</h1>
          <p class="page-subtitle">Auto-generated role-specific technical tests for early-stage evaluation</p>
        </div>
        <button class="btn btn-primary" id="generate-test-btn" @click="generateTest" :disabled="isGenerating">
          <svg v-if="!isGenerating" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          <span v-else class="loader-sm"></span>
          {{ isGenerating ? 'Creating AI Test...' : 'Generate AI Test' }}
        </button>
      </div>

      <!-- Role Selector -->
      <div class="role-selector animate-fade-in-up card" style="animation-delay:0.1s">
        <h2 class="subsection-title">Select Role</h2>
        <div class="role-grid">
          <button
            v-for="role in roles"
            :key="role.id"
            class="role-btn"
            :class="{ 'role-btn--selected': selectedRole === role.id }"
            :id="`role-btn-${role.id}`"
            @click="selectedRole = role.id"
          >
            <span class="role-btn__icon" v-html="role.icon"></span>
            {{ role.name }}
          </button>
        </div>
      </div>

      <!-- Questions -->
      <div v-if="questions.length" class="questions-section animate-fade-in-up" style="animation-delay:0.2s">
        <div class="questions-header">
          <h2 class="subsection-title">Assessment Questions</h2>
          <div class="timer" :class="{ 'timer--warning': timeLeft < 300 }" id="assessment-timer">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            {{ formattedTime }}
          </div>
        </div>
        <div class="questions-list">
          <div
            v-for="(q, i) in questions"
            :key="i"
            class="question-card card"
            :id="`question-${i}`"
          >
            <div class="question-num">Q{{ i + 1 }}</div>
            <p class="question-text">{{ q.text }}</p>
            <div class="question-options">
              <label
                v-for="(opt, j) in q.options"
                :key="j"
                class="option-label"
                :class="{ 'option-label--selected': q.answer === j }"
                :id="`q${i}-opt${j}`"
              >
                <input type="radio" :name="`q${i}`" :value="j" v-model="q.answer" class="option-radio" />
                <span class="option-letter">{{ String.fromCharCode(65 + j) }}</span>
                {{ opt }}
              </label>
            </div>
          </div>
        </div>
        <div class="submit-row">
          <button class="btn btn-primary" id="submit-assessment-btn" @click="submit">
            Submit Assessment
          </button>
          <p class="submit-note">{{ answeredCount }} / {{ questions.length }} answered</p>
        </div>
      </div>

      <!-- Score Result -->
      <div v-if="showResult" class="result-section card animate-fade-in-up text-center">
        <div class="result-icon">🎯</div>
        <h2 class="result-title">Assessment Complete!</h2>
        <p class="result-score gradient-text">{{ resultScore }}%</p>
        <p class="result-label">{{ resultLabel }}</p>
        <button class="btn btn-outline" @click="showResult = false; questions = []" id="retake-btn">
          Retake Assessment
        </button>
      </div>

      <!-- Empty State -->
      <AppEmptyState
        v-if="!questions.length && !showResult"
        icon="⚡"
        title="Ready to Assess?"
        description="Select a role above and click 'Generate Test' to auto-create a skill assessment."
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import axios from 'axios'
import AppEmptyState from '@/components/AppEmptyState.vue'

const selectedRole = ref('ml')
const questions = ref([])
const showResult = ref(false)
const resultScore = ref(0)
const timeLeft = ref(1800)
const isGenerating = ref(false)
let timerInterval = null

const roles = [
  { id: 'ml', name: 'ML Engineer', icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>` },
  { id: 'backend', name: 'Backend Dev', icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>` },
  { id: 'frontend', name: 'Frontend Dev', icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>` },
  { id: 'devops', name: 'DevOps', icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/><path d="M4.93 4.93a10 10 0 0 0 0 14.14"/></svg>` },
]

const answeredCount = computed(() => questions.value.filter(q => q.answer !== null).length)
const formattedTime = computed(() => {
  const m = Math.floor(timeLeft.value / 60).toString().padStart(2, '0')
  const s = (timeLeft.value % 60).toString().padStart(2, '0')
  return `${m}:${s}`
})

const resultLabel = computed(() => {
  if (resultScore.value >= 80) return '🏆 Excellent — Recommended for shortlist'
  if (resultScore.value >= 60) return '✅ Good — Move to interview round'
  return '❌ Below threshold — Needs improvement'
})

async function generateTest() {
  isGenerating.value = true
  try {
    const roleObj = roles.find(r => r.id === selectedRole.value)
    const response = await axios.post('http://localhost:5001/api/generate-assessment', {
      role: roleObj ? roleObj.name : selectedRole.value
    })

    if (response.data.status === 'success') {
      questions.value = response.data.questions.map(q => ({ ...q, answer: null }))
      showResult.value = false
      timeLeft.value = 600 // 10 minutes for 5 questions

      if (timerInterval) clearInterval(timerInterval)
      timerInterval = setInterval(() => {
        if (timeLeft.value > 0) timeLeft.value--
        else {
          clearInterval(timerInterval)
          submit() // Auto-submit on time out
        }
      }, 1000)
    }
  } catch (err) {
    console.error('Failed to generate test:', err)
    alert('Could not generate AI test. Make sure the backend is running.')
  } finally {
    isGenerating.value = false
  }
}

function submit() {
  if (!questions.value.length) return

  const total = questions.value.length
  const correct = questions.value.filter(q => q.answer === q.correct).length
  resultScore.value = Math.round((correct / total) * 100)

  showResult.value = true
  if (timerInterval) clearInterval(timerInterval)
}

onUnmounted(() => { if (timerInterval) clearInterval(timerInterval) })
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--sp-4);
  margin-bottom: var(--sp-8);
  flex-wrap: wrap;
}
.page-title  { font-size: 2rem; font-weight: 800; letter-spacing: -0.02em; }
.page-subtitle { color: var(--clr-text-muted); margin-top: var(--sp-1); }

/* Role Selector */
.role-selector {
  margin-bottom: var(--sp-6);
}
.subsection-title { font-size: 1.2rem; font-weight: 700; margin-bottom: var(--sp-4); }
.role-grid {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sp-3);
}
.role-btn {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  padding: 0.6rem 1.2rem;
  border-radius: var(--radius-full);
  border: 1px solid var(--clr-border-hover);
  background: var(--clr-surface-2);
  color: var(--clr-text-light);
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all var(--transition-base);
}
.role-btn:hover { border-color: var(--clr-primary); color: var(--clr-primary); }
.role-btn--selected { background: rgba(99,102,241,0.1); border-color: var(--clr-primary); color: var(--clr-primary); }

/* Questions */
.questions-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-4);
  margin-bottom: var(--sp-4);
  flex-wrap: wrap;
}
.timer {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--clr-text-light);
  background: var(--clr-surface-2);
  padding: 0.4rem 0.9rem;
  border-radius: var(--radius-full);
  border: 1px solid var(--clr-border);
}
.timer--warning { color: #ef4444; border-color: rgba(239,68,68,0.3); }

.questions-list {
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
  margin-bottom: var(--sp-6);
}
.question-card {
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
}
.question-num {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--clr-primary);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
.question-text {
  font-size: 0.975rem;
  font-weight: 600;
  line-height: 1.5;
}
.question-options {
  display: flex;
  flex-direction: column;
  gap: var(--sp-2);
}
.option-label {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  padding: 0.7rem 1rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--clr-border);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: 0.875rem;
}
.option-label:hover { border-color: var(--clr-primary); background: rgba(99,102,241,0.04); }
.option-label--selected { border-color: var(--clr-primary); background: rgba(99,102,241,0.1); color: #a5b4fc; }
.option-letter {
  width: 24px;
  height: 24px;
  border-radius: var(--radius-full);
  background: var(--clr-surface-3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  flex-shrink: 0;
}
.option-radio { display: none; }

/* Submit */
.submit-row {
  display: flex;
  align-items: center;
  gap: var(--sp-6);
}
.submit-note {
  color: var(--clr-text-muted);
  font-size: 0.875rem;
}

/* Result */
.result-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--sp-4);
  padding: var(--sp-12);
}
.result-icon { font-size: 3rem; }
.result-title { font-size: 1.5rem; font-weight: 800; }
.result-score {
  font-size: 4rem;
  font-weight: 800;
  font-family: var(--font-heading);
  letter-spacing: -0.03em;
}
.result-label { color: var(--clr-text-light); font-size: 1rem; }

/* Empty State */

</style>

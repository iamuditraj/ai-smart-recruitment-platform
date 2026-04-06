<template>
  <div class="ats-score-panel" :class="{ 'animate-fade-in-up': animate }">
    <!-- Overall Score -->
    <div class="ats-overall">
      <div class="ats-score-header">
        <div class="flex items-center">
          <span class="ats-score-number" :style="{ color: getScoreColor(score) }">{{ score }}</span>
          <span class="ats-score-denom">/100</span>
        </div>
        <span v-if="showBadge" :class="['badge', badgeClass]">{{ statusLabel }}</span>
      </div>
      <div class="ats-main-bar">
        <div class="ats-main-bar-fill" :style="{ width: score + '%', backgroundColor: getScoreColor(score) }"></div>
      </div>

      <!-- Breakdown -->
      <div v-if="breakdown" class="breakdown-section">
        <h4 class="breakdown-title">Score Breakdown</h4>
        <div v-for="dim in scoreDimensions" :key="dim.key" class="breakdown-row">
          <span class="breakdown-label">{{ dim.label }}</span>
          <div class="breakdown-bar-track">
            <div 
              class="breakdown-bar-fill" 
              :style="{ 
                width: ((breakdown[dim.key] || 0) / dim.max * 100) + '%',
                backgroundColor: getBreakdownColor(breakdown[dim.key] || 0, dim.max)
              }"
            ></div>
          </div>
          <span class="breakdown-score">{{ breakdown[dim.key] || 0 }}/{{ dim.max }}</span>
        </div>
      </div>

      <!-- Matched Skills -->
      <div v-if="matchedSkills && matchedSkills.length" class="skills-section">
        <h4 class="breakdown-title">Matched Skills</h4>
        <div class="chips-row">
          <span v-for="skill in matchedSkills.slice(0, 10)" :key="skill" class="chip chip-green">{{ skill }}</span>
          <span v-if="matchedSkills.length > 10" class="chip chip-more">+{{ matchedSkills.length - 10 }} more</span>
        </div>
      </div>

      <!-- Missing Keywords -->
      <div v-if="missingSkills && missingSkills.length" class="skills-section">
        <h4 class="breakdown-title">Missing Keywords</h4>
        <div class="chips-row">
          <span v-for="gap in missingSkills.slice(0, 10)" :key="gap" class="chip chip-red">{{ gap }}</span>
          <span v-if="missingSkills.length > 10" class="chip chip-more">+{{ missingSkills.length - 10 }} more</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { scoreDimensions } from '@/utils/atsConstants'
import { getScoreColor, getBreakdownColor } from '@/utils/uiHelpers'

const props = defineProps({
  score: { type: Number, required: true },
  breakdown: { type: Object, default: null },
  matchedSkills: { type: Array, default: () => [] },
  missingSkills: { type: Array, default: () => [] },
  showBadge: { type: Boolean, default: true },
  animate: { type: Boolean, default: true }
})

const statusLabel = computed(() => {
  if (props.score >= 80) return 'Exceptional Match'
  if (props.score >= 60) return 'Strong Candidate'
  if (props.score >= 40) return 'Potential Match'
  return 'Low Relevance'
})

const badgeClass = computed(() => {
  if (props.score >= 80) return 'badge-success'
  if (props.score >= 60) return 'badge-primary'
  if (props.score >= 40) return 'badge-warning'
  return 'badge-danger'
})
</script>

<style scoped>
.ats-score-panel {
  width: 100%;
}

.ats-overall {
  padding: 1.25rem;
  border-radius: 12px;
  border: 1px solid var(--clr-border);
  background: var(--clr-surface);
  margin-bottom: 1.5rem;
}

.ats-score-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.ats-score-number {
  font-size: 2.5rem;
  font-weight: 800;
  line-height: 1;
}

.ats-score-denom {
  font-size: 1rem;
  color: var(--clr-text-muted);
  margin-left: 4px;
}

.ats-main-bar {
  height: 8px;
  border-radius: 4px;
  background: var(--clr-surface-3);
  overflow: hidden;
  margin-bottom: 1.25rem;
}

.ats-main-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.breakdown-section {
  margin-bottom: 1.25rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--clr-border);
}

.breakdown-title {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--clr-text-muted);
  margin-bottom: 0.75rem;
}

.breakdown-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.6rem;
}

.breakdown-label {
  font-size: 0.8rem;
  color: var(--clr-text-muted);
  width: 130px;
  flex-shrink: 0;
  font-weight: 500;
}

.breakdown-bar-track {
  flex: 1;
  height: 6px;
  background: var(--clr-surface-3);
  border-radius: 3px;
  overflow: hidden;
}

.breakdown-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.6s ease-out;
}

.breakdown-score {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--clr-text);
  width: 40px;
  text-align: right;
  flex-shrink: 0;
}

.skills-section {
  margin-top: 1.25rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--clr-border);
}

.chips-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-top: 0.4rem;
}

.chip {
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.chip-green {
  background: rgba(16, 185, 129, 0.12);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.chip-red {
  background: rgba(239, 68, 68, 0.12);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.chip-more {
  background: var(--clr-surface-2);
  color: var(--clr-text-muted);
  border: 1px solid var(--clr-border);
}

.flex { display: flex; }
.items-center { align-items: center; }
</style>

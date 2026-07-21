<template>
  <div class="simple-bar-container" :style="{ width: size + 'px' }">
    <span v-if="showLabel" class="bar-score-text" :style="{ color: colorClass }">{{ score }}</span>
    <div class="bar-bg">
      <div class="bar-fill" :style="`width: ${score}%; background: ${colorClass}`"></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  score: {
    type: Number,
    required: true
  },
  size: {
    type: Number,
    default: 44
  },
  showLabel: {
    type: Boolean,
    default: true
  }
})

const colorClass = computed(() => {
  if (props.score >= 80) return '#10b981'
  if (props.score >= 50) return '#f59e0b'
  return '#ef4444'
})
</script>

<style scoped>
.simple-bar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin: 0 auto;
}
.bar-score-text {
  font-weight: 800;
  font-size: 1rem;
}
.bar-bg {
  width: 100%;
  height: 6px;
  background: var(--clr-surface-3);
  border-radius: 99px;
  overflow: hidden;
}
.bar-fill {
  height: 100%;
  border-radius: 99px;
  transition: width 0.5s ease;
}
</style>

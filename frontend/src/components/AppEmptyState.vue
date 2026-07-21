<template>
  <div class="app-empty-state" :class="{ 'card': showCard, 'animate-fade-in-up': animate }">
    <div v-if="$slots.icon || icon" class="empty-icon">
      <slot name="icon">
        <span v-if="isEmoji(icon)">{{ icon }}</span>
        <span v-else v-html="icon"></span>
      </slot>
    </div>
    <h3 v-if="title">{{ title }}</h3>
    <div class="empty-description">
      <slot>{{ description }}</slot>
    </div>
    <div v-if="$slots.action" class="empty-action">
      <slot name="action"></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  icon: {
    type: String,
    default: ''
  },
  title: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  showCard: {
    type: Boolean,
    default: true
  },
  animate: {
    type: Boolean,
    default: true
  }
})

function isEmoji(str) {
  // Simple check for common emoji ranges or single characters that aren't tags
  return str && !str.includes('<') && str.length <= 4;
}
</script>

<style scoped>
.app-empty-state {
  text-align: center;
  padding: 4rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  width: 100%;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-icon :deep(svg) {
  width: 48px;
  height: 48px;
  color: var(--clr-text-muted);
  opacity: 0.6;
}

h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
  color: var(--clr-text);
}

.empty-description {
  color: var(--clr-text-muted);
  max-width: 400px;
  line-height: 1.6;
  font-size: 0.95rem;
}

.empty-action {
  margin-top: 1rem;
}

/* Ensure card context doesn't add extra padding if already in one */
.card.app-empty-state {
  border: 1px solid var(--clr-border);
  box-shadow: var(--shadow-sm);
}
</style>

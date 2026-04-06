<template>
  <div class="page-header animate-fade-in-up">
    <div>
      <RouterLink v-if="backTo" :to="backTo" class="back-link">
        ← {{ backLabel }}
      </RouterLink>
      <h1 class="page-title">{{ title }}</h1>
      <p v-if="subtitle" class="page-subtitle">{{ subtitle }}</p>
    </div>
    <div v-if="$slots.actions" class="header-actions">
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  },
  backTo: {
    type: String,
    default: ''
  },
  backLabel: {
    type: String,
    default: 'Back'
  }
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.page-subtitle {
  color: var(--clr-text-muted);
  margin-top: 0.25rem;
}

.back-link {
  display: inline-block;
  margin-bottom: 0.5rem;
  color: var(--clr-primary);
  font-weight: 600;
  text-decoration: none;
  font-size: 0.9rem;
}
.back-link:hover {
  text-decoration: underline;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}
</style>

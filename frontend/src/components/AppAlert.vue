<template>
  <div v-if="message" class="app-alert" :class="[type, animate ? 'animate-fade-in-up' : '']">
    <div class="alert-content">
      <slot>{{ message }}</slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'error',
    validator: (v) => ['success', 'error', 'warning', 'info'].includes(v)
  },
  animate: {
    type: Boolean,
    default: true
  }
})
</script>

<style scoped>
.app-alert {
  padding: 0.85rem 1rem;
  border-radius: var(--radius-md);
  margin-bottom: 1.5rem;
  font-weight: 600;
  text-align: center;
  font-size: 0.875rem;
  width: 100%;
}

.alert-content {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.error {
  background: rgba(239, 68, 68, 0.1);
  color: var(--clr-danger);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.success {
  background: rgba(16, 185, 129, 0.1);
  color: var(--clr-success);
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.warning {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.2);
}

.info {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.2);
}
</style>

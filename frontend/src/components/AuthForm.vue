<template>
  <form @submit.prevent="$emit('submit')" class="login-form">
    <AppAlert :message="error" type="error" />

    <slot></slot>

    <div class="login-footer">
      <button type="submit" class="btn btn-primary w-full" :disabled="loading">
        <span v-if="!loading">{{ submitText }}</span>
        <AppSpinner v-else size="sm" />
      </button>
    </div>
  </form>
</template>

<script setup>
import AppSpinner from '@/components/AppSpinner.vue'
import AppAlert from '@/components/AppAlert.vue'

defineProps({
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  },
  submitText: {
    type: String,
    default: 'Submit'
  }
})

defineEmits(['submit'])
</script>

<style scoped>
.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--sp-5);
}

.login-footer {
  margin-top: var(--sp-2);
}

:global(.role-tabs) {
  display: flex;
  background: var(--clr-surface-2);
  padding: 4px;
  border-radius: var(--radius-md);
  margin-bottom: var(--sp-2);
}

:global(.role-tab) {
  flex: 1;
  padding: 0.6rem;
  border: none;
  background: transparent;
  color: var(--clr-text-muted);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  border-radius: var(--radius-sm);
  transition: all var(--transition-base);
}

:global(.role-tab.active) {
  background: var(--clr-surface);
  color: var(--clr-primary);
  box-shadow: var(--shadow-sm);
}

:global(.gradient-text) {
  background: var(--gradient-brand);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>

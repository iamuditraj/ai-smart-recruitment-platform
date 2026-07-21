<template>
  <div class="resume-entry-block animate-fade-in-up">
    <div class="entry-header">
      <span class="entry-index">{{ label }} {{ index + 1 }}</span>
      <button 
        type="button" 
        class="btn-remove" 
        @click="$emit('remove')"
        :title="`Remove ${label}`"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 2-2 2-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
        Remove
      </button>
    </div>
    <div class="entry-body">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  index: {
    type: Number,
    required: true
  },
  label: {
    type: String,
    required: true
  }
})

defineEmits(['remove'])
</script>

<style scoped>
.resume-entry-block {
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  margin-top: 1.5rem;
  transition: all 0.2s ease;
}

.resume-entry-block:hover {
  border-color: var(--clr-primary);
  box-shadow: var(--shadow-sm);
}

.entry-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--clr-surface-3);
}

.entry-index {
  font-size: 0.75rem;
  font-weight: 800;
  color: var(--clr-primary);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.btn-remove {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.75rem;
  font-weight: 700;
  color: #ef4444;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0.4rem 0.6rem;
  border-radius: 6px;
  transition: all 0.2s;
}

.btn-remove:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #dc2626;
}

.entry-body {
  width: 100%;
}
</style>

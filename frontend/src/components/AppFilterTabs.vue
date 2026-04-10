<template>
  <div class="app-filter-tabs" :class="{ 'animate-fade-in-up': animate }">
    <button
      v-for="tab in tabs"
      :key="getValue(tab)"
      class="filter-tab"
      :class="{ active: modelValue === getValue(tab) }"
      @click="$emit('update:modelValue', getValue(tab))"
      type="button"
    >
      <span class="tab-label">{{ getLabel(tab) }}</span>
      <span v-if="counts && counts[getValue(tab)]" class="tab-count">
        {{ counts[getValue(tab)] }}
      </span>
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  tabs: {
    type: Array, // Array of strings or { label, value } objects
    required: true
  },
  modelValue: {
    type: [String, Number],
    required: true
  },
  counts: {
    type: Object,
    default: null
  },
  animate: {
    type: Boolean,
    default: true
  }
})

defineEmits(['update:modelValue'])

function getLabel(tab) {
  return typeof tab === 'object' ? tab.label : tab
}

function getValue(tab) {
  return typeof tab === 'object' ? tab.value : tab
}
</script>

<style scoped>
.app-filter-tabs {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .app-filter-tabs {
    overflow-x: auto;
    flex-wrap: nowrap;
    scrollbar-width: none;
    padding-bottom: 2px;
    -webkit-overflow-scrolling: touch;
  }

  .app-filter-tabs::-webkit-scrollbar {
    display: none;
  }
}

.filter-tab {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 1.25rem;
  border-radius: var(--radius-full);
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  color: var(--clr-text-muted);
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.filter-tab:hover {
  border-color: var(--clr-primary);
  color: var(--clr-primary);
}

.filter-tab.active {
  background: var(--clr-primary);
  color: white;
  border-color: var(--clr-primary);
}

.tab-count {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.1rem 0.4rem;
  border-radius: 99px;
  font-size: 0.72rem;
  font-weight: 700;
}

.filter-tab:not(.active) .tab-count {
  background: var(--clr-surface-2);
  color: var(--clr-text-muted);
}
</style>

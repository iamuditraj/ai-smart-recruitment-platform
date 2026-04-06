<template>
  <span class="app-spinner" :class="sizeClass"></span>
</template>

<script setup>
const props = defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v)
  }
})

const sizeClass = `spinner-${props.size}`
</script>

<style scoped>
.app-spinner {
  border-radius: 50%;
  animation: app-spin 1s linear infinite;
  display: inline-block;
}

.spinner-sm {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.2);
  border-top-color: #fff;
}

.spinner-md {
  width: 36px;
  height: 36px;
  border: 3px solid var(--clr-surface-3);
  border-top-color: var(--clr-primary);
  margin: 0 auto 1rem;
}

.spinner-lg {
  width: 40px;
  height: 40px;
  border: 4px solid var(--clr-surface-2);
  border-top-color: var(--clr-primary);
  margin: 0 auto 1rem;
}

@keyframes app-spin {
  to { transform: rotate(360deg); }
}
</style>

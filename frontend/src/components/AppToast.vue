<template>
  <Transition name="fade">
    <div v-if="show" :class="['toast', type]">
      {{ message }}
    </div>
  </Transition>
</template>

<script setup>
import { watch } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  message: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'success'
  }
})

const emit = defineEmits(['hide'])

watch(() => props.show, (newVal) => {
  if (newVal) {
    setTimeout(() => {
      emit('hide')
    }, 3000)
  }
})
</script>

<style scoped>
.toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  padding: 1rem 2rem;
  border-radius: var(--radius-md);
  color: white;
  font-weight: 600;
  box-shadow: var(--shadow-lg);
  z-index: 9999;
}
.toast.success { background: var(--clr-success); }
.toast.error { background: var(--clr-danger); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.5s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>

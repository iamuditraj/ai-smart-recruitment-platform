<template>
  <Transition name="v-modal">
    <div v-if="show" class="v-modal-overlay" @click.self="$emit('close')" @wheel.self="handleOverlayScroll">
      <div class="v-modal-card card" :class="customClass">
        <button class="v-modal-close" @click="$emit('close')">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>

        <div class="v-modal-content-scroll" ref="scrollContentRef">
          <slot></slot>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch, onUnmounted } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    required: true
  },
  customClass: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['close'])

const scrollContentRef = ref(null)

function handleOverlayScroll(e) {
  e.preventDefault();
  if (scrollContentRef.value) {
    scrollContentRef.value.scrollTop += e.deltaY;
  }
}

watch(() => props.show, (newVal) => {
  if (newVal) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

onUnmounted(() => {
  document.body.style.overflow = ''
})
</script>

<style scoped>
.v-modal-overlay {
  position: fixed; inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  z-index: 2000;
  display: flex; align-items: center; justify-content: center;
  padding: 2rem;
}

.v-modal-card {
  width: 100%; max-width: 720px;
  background: var(--clr-surface);
  border-radius: var(--radius-xl);
  padding: var(--sp-8);
  position: relative;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  display: flex;
  flex-direction: column;
}

.v-modal-card:hover { transform: none; }

.v-modal-content-scroll {
  overflow-y: auto;
  max-height: calc(90vh - 4rem);
  padding-right: 0.5rem;
}

.v-modal-content-scroll::-webkit-scrollbar {
  width: 6px;
}
.v-modal-content-scroll::-webkit-scrollbar-track {
  background: transparent;
}
.v-modal-content-scroll::-webkit-scrollbar-thumb {
  background: var(--clr-surface-3);
  border-radius: var(--radius-full);
}
.v-modal-content-scroll::-webkit-scrollbar-thumb:hover {
  background: var(--clr-primary);
}

.v-modal-close {
  position: absolute; top: 1.5rem; right: 2.5rem;
  background: var(--clr-surface-2); border: none;
  width: 36px; height: 36px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; color: var(--clr-text-muted);
  z-index: 10;
}

.v-modal-close:hover {
  color: var(--clr-text);
}

/* Animations */
.v-modal-enter-active, .v-modal-leave-active { transition: opacity 0.3s ease; }
.v-modal-enter-from, .v-modal-leave-to { opacity: 0; }
.v-modal-enter-from .v-modal-card { transform: scale(0.95) translateY(20px); }

/* Responsive */
@media (max-width: 768px) {
  .v-modal-card {
    padding: var(--sp-4);
    width: 100%;
    max-width: 100%;
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
    position: fixed;
    bottom: 0;
    max-height: 92vh;
  }
  .v-modal-content-scroll {
    max-height: calc(92vh - 2rem);
  }
  .v-modal-overlay {
    padding: 0;
  }
}
</style>

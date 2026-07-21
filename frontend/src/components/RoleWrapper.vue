<template>
  <Suspense>
    <component :is="ActiveComponent" />
    <template #fallback>
      <div class="role-wrapper-loading">Loading…</div>
    </template>
  </Suspense>
</template>

<script setup>
import { computed, defineAsyncComponent } from 'vue'
import { useAuthStore } from '../stores/auth'

const props = defineProps({
  recruiterComponent: {
    type: String,
    required: true
  },
  candidateComponent: {
    type: String,
    required: true
  }
})

const authStore = useAuthStore()

const views = import.meta.glob('../views/**/*.vue')

const ActiveComponent = computed(() => {
  const path = authStore.isRecruiter ? props.recruiterComponent : props.candidateComponent
  
  // Convert standard router paths (starting with ../views/)
  const exactPath = path.startsWith('../') && !path.includes('../views/') 
    ? path.replace('../', '../views/') 
    : path

  if (views[exactPath]) {
    return defineAsyncComponent(views[exactPath])
  } else if (views[path]) {
    return defineAsyncComponent(views[path])
  }
  
  console.error("Component not found for path:", path)
  return null
})
</script>

<style scoped>
.role-wrapper-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 60vh;
  color: var(--clr-text-muted);
  font-size: 1rem;
}
</style>

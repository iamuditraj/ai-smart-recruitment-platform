<template>
  <Suspense>
    <RecruiterDashboard v-if="authStore.isRecruiter" />
    <CandidateDashboard v-else />
    <template #fallback>
      <div class="dashboard-loading">Loading dashboard…</div>
    </template>
  </Suspense>
</template>

<script setup>
import { defineAsyncComponent } from 'vue'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()

const RecruiterDashboard = defineAsyncComponent(() => import('../recruiter/DashboardView.vue'))
const CandidateDashboard = defineAsyncComponent(() => import('../candidate/CandidateDashboardView.vue'))
</script>

<style scoped>
.dashboard-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 60vh;
  color: var(--clr-text-muted);
  font-size: 1rem;
}
</style>

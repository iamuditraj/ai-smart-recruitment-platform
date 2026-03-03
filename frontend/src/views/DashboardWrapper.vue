<template>
  <div class="dashboard-wrapper">
    <!-- Component is determined reactively by authStore.role -->
    <component :is="activeDashboard" />
  </div>
</template>

<script setup>
import { computed, defineAsyncComponent } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

// Dynamically and reactively import the correct dashboard
const RecruiterDashboard = defineAsyncComponent(() => import('./DashboardView.vue'))
const CandidateDashboard = defineAsyncComponent(() => import('./CandidateDashboardView.vue'))

const activeDashboard = computed(() => {
  return authStore.role === 'recruiter' ? RecruiterDashboard : CandidateDashboard
})
</script>

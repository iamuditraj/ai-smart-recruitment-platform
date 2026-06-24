<template>
  <Suspense>
    <RecruiterProfile v-if="authStore.isRecruiter" />
    <CandidateProfile v-else />
    <template #fallback>
      <div class="profile-loading">Loading profile…</div>
    </template>
  </Suspense>
</template>

<script setup>
import { defineAsyncComponent } from 'vue'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()

const RecruiterProfile = defineAsyncComponent(() => import('../recruiter/RecruiterProfileView.vue'))
const CandidateProfile = defineAsyncComponent(() => import('../candidate/CandidateProfileView.vue'))
</script>

<style scoped>
.profile-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 60vh;
  color: var(--clr-text-muted);
  font-size: 1rem;
}
</style>

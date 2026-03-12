<template>
  <div class="profile-view">
    <div class="content-area">
      <div class="profile-header animate-fade-in-up">
        <h1 class="profile-title">Recruiter Profile</h1>
        <p class="profile-subtitle">Manage your company and recruiter details</p>
      </div>
      <div class="profile-content grid">
        <div class="profile-card card animate-fade-in-up" style="animation-delay: 0.1s">
            <h2 class="text-center mt-4">{{ authStore.user?.name }}</h2>
            <p class="text-center text-muted text-sm">{{ authStore.user?.email }}</p>
            <div class="badge badge-primary mt-2 mx-auto">{{ authStore.role }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '../../stores/auth'
const authStore = useAuthStore()
</script>

<style scoped>
.profile-view { min-height: 100vh; }
.profile-header { margin-bottom: var(--sp-8); }
.profile-title { font-size: 2rem; font-weight: 800; }
.profile-subtitle { color: var(--clr-text-muted); margin-top: var(--sp-1); }

.profile-content {
  grid-template-columns: 320px 1fr;
  align-items: start;
  gap: var(--sp-8);
}
</style>

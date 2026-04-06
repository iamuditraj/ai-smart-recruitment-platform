<template>
  <div class="login-view section">
    <div class="container small-container">
      <div class="login-card card animate-fade-in-up">
        <div class="login-header text-center">
          <div class="login-logo-container">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="url(#grad-login)" stroke-width="2" stroke-linejoin="round"/>
              <path d="M2 17L12 22L22 17" stroke="url(#grad-login)" stroke-width="2" stroke-linejoin="round"/>
              <path d="M2 12L12 17L22 12" stroke="url(#grad-login)" stroke-width="2" stroke-linejoin="round"/>
              <defs>
                <linearGradient id="grad-login" x1="2" y1="2" x2="22" y2="22" gradientUnits="userSpaceOnUse">
                  <stop stop-color="#6366f1"/>
                  <stop offset="0.5" stop-color="#8b5cf6"/>
                  <stop offset="1" stop-color="#06b6d4"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <h1 class="login-title">Create Account</h1>
          <p class="login-subtitle">Join HireAI to start your journey</p>
        </div>

        <form @submit.prevent="handleSignup" class="login-form">
          <AppAlert :message="errorMessage" type="error" />

          <div class="form-group">
            <label class="form-label">I am a...</label>
            <div class="role-tabs">
              <button
                type="button"
                @click="role = 'candidate'"
                class="role-tab"
                :class="{ active: role === 'candidate' }"
              >
                Candidate
              </button>
              <button
                type="button"
                @click="role = 'recruiter'"
                class="role-tab"
                :class="{ active: role === 'recruiter' }"
              >
                Recruiter
              </button>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label" for="signup-name">Full Name</label>
            <input
              v-model="name"
              type="text"
              id="signup-name"
              class="form-input"
              placeholder="Your Name"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="signup-email">Email Address</label>
            <input
              v-model="email"
              type="email"
              id="signup-email"
              class="form-input"
              placeholder="name@example.com"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="signup-password">Password</label>
            <input
              v-model="password"
              type="password"
              id="signup-password"
              class="form-input"
              placeholder="Min. 8 characters"
              required
              minlength="8"
            />
          </div>

          <div class="login-footer">
            <button type="submit" class="btn btn-primary w-full" :disabled="isLoading">
              <span v-if="!isLoading">Create Free Account</span>
              <AppSpinner v-else size="sm" />
            </button>
          </div>
        </form>

        <div class="login-extra text-center mt-6">
          <p class="text-sm text-muted">Already have an account? <RouterLink to="/login" class="gradient-text font-bold">Sign in</RouterLink></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import AppSpinner from '@/components/AppSpinner.vue'
import AppAlert from '@/components/AppAlert.vue'

const router = useRouter()
const authStore = useAuthStore()

const role = ref('candidate')
const name = ref('')
const email = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

async function handleSignup() {
  isLoading.value = true
  errorMessage.value = ''

  const result = await authStore.signup({
    email: email.value,
    password: password.value,
    role: role.value,
    name: name.value
  })

  isLoading.value = false
  if (result.success) {
    router.push('/dashboard')
  } else {
    errorMessage.value = result.message || 'Signup failed'
  }
}
</script>

<style scoped>


.login-view {
  min-height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.small-container {
  max-width: 440px;
}

.login-card {
  padding: var(--sp-10);
  border: 1px solid var(--clr-border);
  box-shadow: var(--shadow-lg);
}

.login-header {
  margin-bottom: var(--sp-8);
}

.login-logo-container {
  margin-bottom: var(--sp-4);
  display: flex;
  justify-content: center;
}

.login-title {
  font-size: 1.75rem;
  font-weight: 800;
  margin-bottom: var(--sp-2);
}

.login-subtitle {
  color: var(--clr-text-muted);
  font-size: 0.95rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--sp-5);
}

.role-tabs {
  display: flex;
  background: var(--clr-surface-2);
  padding: 4px;
  border-radius: var(--radius-md);
  margin-bottom: var(--sp-2);
}

.role-tab {
  flex: 1;
  padding: 0.6rem;
  border: none;
  background: transparent;
  color: var(--clr-text-muted);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  border-radius: var(--radius-sm);
  transition: all var(--transition-base);
}

.role-tab.active {
  background: var(--clr-surface);
  color: var(--clr-primary);
  box-shadow: var(--shadow-sm);
}

.login-footer {
  margin-top: var(--sp-2);
}



.text-muted {
  color: var(--clr-text-muted);
}

.mt-6 {
  margin-top: 1.5rem;
}

.font-bold {
  font-weight: 700;
}
</style>

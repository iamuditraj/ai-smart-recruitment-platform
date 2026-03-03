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
          <h1 class="login-title">Hire<span class="gradient-text">AI</span> Portal</h1>
          <p class="login-subtitle">Connect to your recruitment workspace</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <!-- Role Selection -->
          <div class="role-tabs" style="display: none;"> <!-- Role is now determined by backend on login, but for login we might just need email/pass -->
          </div>

          <div v-if="errorMessage" class="error-banner animate-fade-in">
            {{ errorMessage }}
          </div>

          <div class="form-group">
            <label class="form-label" for="login-email">Email Address</label>
            <input
              v-model="email"
              type="email"
              id="login-email"
              class="form-input"
              placeholder="name@company.com"
              required
            />
          </div>

          <div class="form-group">
            <div class="flex justify-between items-center mb-1">
               <label class="form-label mb-0" for="login-password">Password</label>
               <a href="#" class="forgot-link">Forgot?</a>
            </div>
            <input
              v-model="password"
              type="password"
              id="login-password"
              class="form-input"
              placeholder="••••••••"
              required
            />
          </div>

          <div class="login-footer">
            <button type="submit" class="btn btn-primary w-full" :disabled="isLoading">
              <span v-if="!isLoading">Sign In to Dashboard</span>
              <span v-else class="loader-sm"></span>
            </button>
          </div>
        </form>

        <div class="login-extra text-center mt-6">
          <p class="text-sm text-muted">Don't have an account? <RouterLink to="/signup" class="gradient-text font-bold">Sign up</RouterLink></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

async function handleLogin() {
  isLoading.value = true
  errorMessage.value = ''

  const result = await authStore.login(email.value, password.value)

  isLoading.value = false
  if (result.success) {
    router.push('/dashboard')
  } else {
    errorMessage.value = result.message || 'Invalid credentials'
  }
}
</script>

<style scoped>
.error-banner {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  padding: 0.75rem;
  border-radius: var(--radius-md);
  font-size: 0.85rem;
  font-weight: 600;
  border: 1px solid rgba(239, 68, 68, 0.2);
  text-align: center;
}

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

.forgot-link {
  font-size: 0.75rem;
  color: var(--clr-primary);
  text-decoration: none;
}

.forgot-link:hover {
  text-decoration: underline;
}

.login-footer {
  margin-top: var(--sp-2);
}

.loader-sm {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.2);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  display: inline-block;
}

@keyframes spin {
  to { transform: rotate(360deg); }
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

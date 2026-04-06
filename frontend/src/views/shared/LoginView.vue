<template>
  <AuthLayout subtitle="Connect to your recruitment workspace">
    <template #title>Hire<span class="gradient-text">AI</span> Portal</template>

        <form @submit.prevent="handleLogin" class="login-form">
          <!-- Role Selection -->
          <div class="role-tabs" style="display: none;"> <!-- Role is now determined by backend on login, but for login we might just need email/pass -->
          </div>

          <AppAlert :message="errorMessage" type="error" />

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
              <AppSpinner v-else size="sm" />
            </button>
          </div>
        </form>

        <template #footer>
          <p class="text-sm text-muted">Don't have an account? <RouterLink to="/signup" class="gradient-text font-bold">Sign up</RouterLink></p>
        </template>
  </AuthLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import AppSpinner from '@/components/AppSpinner.vue'
import AppAlert from '@/components/AppAlert.vue'
import AuthLayout from '@/components/AuthLayout.vue'

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

:deep(.gradient-text) {
  background: var(--gradient-brand);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>

<template>
  <AuthLayout subtitle="Connect to your recruitment workspace">
    <template #title>Hire<span class="gradient-text">AI</span> Portal</template>

        <AuthForm 
          @submit="handleLogin" 
          :loading="isLoading" 
          :error="errorMessage" 
          submitText="Sign In to Dashboard"
        >
          <!-- Role Selection -->
          <div class="role-tabs" style="display: none;"> <!-- Role is now determined by backend on login, but for login we might just need email/pass -->
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
        </AuthForm>

        <div class="divider">
          <span>OR</span>
        </div>

        <GoogleAuthButton @error="errorMessage = $event" />

        <template #footer>
          <p class="text-sm text-muted">Don't have an account? <RouterLink to="/signup" class="gradient-text font-bold">Sign up</RouterLink></p>
        </template>
  </AuthLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import AuthLayout from '@/components/AuthLayout.vue'
import AuthForm from '@/components/AuthForm.vue'
import GoogleAuthButton from '@/components/GoogleAuthButton.vue'

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
.forgot-link {
  font-size: 0.75rem;
  color: var(--clr-primary);
  text-decoration: none;
}

.forgot-link:hover {
  text-decoration: underline;
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 1.5rem 0 0.5rem;
  color: var(--clr-text-muted);
  font-size: 0.875rem;
}
.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid var(--clr-border);
}
.divider span {
  padding: 0 10px;
}
</style>

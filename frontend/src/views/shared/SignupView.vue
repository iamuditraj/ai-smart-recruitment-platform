<template>
  <AuthLayout title="Create Account" subtitle="Join HireAI to start your journey">

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

        <template #footer>
          <p class="text-sm text-muted">Already have an account? <RouterLink to="/login" class="gradient-text font-bold">Sign in</RouterLink></p>
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

:deep(.gradient-text) {
  background: var(--gradient-brand);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>

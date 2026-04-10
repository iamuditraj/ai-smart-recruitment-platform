<template>
  <button 
    type="button" 
    class="google-auth-btn" 
    @click="handleGoogleAuth" 
    :disabled="isLoading"
  >
    <img 
      v-if="!isLoading" 
      src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" 
      alt="Google Logo" 
      class="google-icon" 
    />
    <div v-else class="spinner"></div>
    <span v-if="!isLoading">Sign in with Google</span>
    <span v-else>Connecting...</span>
  </button>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const props = defineProps({
  role: {
    type: String,
    default: null // In login it will be null, in signup it will be 'candidate' or 'recruiter'
  }
})

const emit = defineEmits(['error'])

const router = useRouter()
const authStore = useAuthStore()
const isLoading = ref(false)

const handleGoogleAuth = async () => {
  isLoading.value = true
  emit('error', '') // Clear any previous errors

  const result = await authStore.loginWithGoogle(props.role)

  isLoading.value = false
  if (result.success) {
    router.push('/dashboard')
  } else {
    emit('error', result.message || 'Google Auth failed')
  }
}
</script>

<style scoped>
.google-auth-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 0.75rem 1rem;
  margin-top: 1rem;
  background-color: white;
  color: #3c4043;
  border: 1px solid #dadce0;
  border-radius: var(--radius-md);
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.2s, box-shadow 0.2s;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.google-auth-btn:hover {
  background-color: #f8f9fa;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.google-auth-btn:active {
  background-color: #e8eaed;
}

.google-auth-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.google-icon {
  width: 18px;
  height: 18px;
  margin-right: 0.75rem;
}

.spinner {
  width: 18px;
  height: 18px;
  margin-right: 0.75rem;
  border: 2px solid transparent;
  border-top-color: #4285F4;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>

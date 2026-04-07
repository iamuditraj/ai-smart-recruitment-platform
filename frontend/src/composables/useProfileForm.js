import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'

export function useProfileForm() {
  const authStore = useAuthStore()
  const isSaving = ref(false)
  const message = ref('')
  const messageType = ref('success')

  const saveProfile = async (formData) => {
    isSaving.value = true
    message.value = ''

    const result = await authStore.updateProfile(formData)

    isSaving.value = false
    if (result.success) {
      message.value = 'Profile updated successfully!'
      messageType.value = 'success'
    } else {
      message.value = result.message || 'Failed to update profile'
      messageType.value = 'error'
    }

    setTimeout(() => message.value = '', 3000)
  }

  return { isSaving, message, messageType, saveProfile }
}

import { ref } from 'vue'

export function useToast() {
  const toast = ref({ show: false, message: '', type: 'success' })
  let timeoutId = null

  const showToast = (message, type = 'success') => {
    toast.value = { show: true, message, type }
    if (timeoutId) clearTimeout(timeoutId)
    timeoutId = setTimeout(() => {
      toast.value.show = false
    }, 3000)
  }

  const hideToast = () => {
    toast.value.show = false
    if (timeoutId) clearTimeout(timeoutId)
  }

  return {
    toast,
    showToast,
    hideToast
  }
}

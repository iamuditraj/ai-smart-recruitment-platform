import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('auth_user') || 'null'))

  // Derive role directly from user object so it is always in sync.
  // Falls back to localStorage so the sidebar renders correctly on first load.
  const role = computed(() => user.value?.role || localStorage.getItem('user_role') || null)

  const isAuthenticated = computed(() => !!user.value)
  const isRecruiter = computed(() => role.value === 'recruiter')
  const isCandidate = computed(() => role.value === 'candidate')

  async function login(email, password) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      const data = await response.json()

      if (data.status === 'success') {
        user.value = data.user
        role.value = data.user.role
        localStorage.setItem('auth_user', JSON.stringify(data.user))
        localStorage.setItem('user_role', data.user.role)
        return { success: true }
      } else {
        return { success: false, message: data.message }
      }
    } catch (error) {
      console.error('Login error:', error)
      return { success: false, message: 'Server connection failed' }
    }
  }

  async function signup(userData) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      })
      const data = await response.json()

      if (data.status === 'success') {
        // Auto login after signup
        user.value = data.user
        role.value = data.user.role
        localStorage.setItem('auth_user', JSON.stringify(data.user))
        localStorage.setItem('user_role', data.user.role)
        return { success: true }
      } else {
        return { success: false, message: data.message }
      }
    } catch (error) {
      console.error('Signup error:', error)
      return { success: false, message: 'Server connection failed' }
    }
  }

  async function updateProfile(profileData) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/profile`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...profileData, email: user.value.email })
      })
      const data = await response.json()

      if (data.status === 'success') {
        user.value = data.user
        localStorage.setItem('auth_user', JSON.stringify(data.user))
        return { success: true }
      } else {
        return { success: false, message: data.message }
      }
    } catch (error) {
      console.error('Profile update error:', error)
      return { success: false, message: 'Server connection failed' }
    }
  }

  async function refreshUser() {
    if (!user.value?.email) return
    try {
      const response = await fetch(`${API_BASE_URL}/api/profile?email=${user.value.email}`)
      const data = await response.json()
      if (data.status === 'success') {
        user.value = data.user
        localStorage.setItem('auth_user', JSON.stringify(data.user))
        // Keep user_role in sync so role computed stays correct even before vue reactivity settles
        if (data.user.role) {
          localStorage.setItem('user_role', data.user.role)
        }
      }
    } catch (error) {
      console.error('Refresh user error:', error)
    }
  }

  async function uploadResume(file) {
    if (!user.value?.email) return { success: false, message: 'Not logged in' }

    try {
      const formData = new FormData()
      formData.append('resume', file)
      formData.append('email', user.value.email)

      const response = await fetch(`${API_BASE_URL}/api/profile/upload-resume`, {
        method: 'POST',
        body: formData
      })
      const data = await response.json()

      if (data.status === 'success') {
        // Refresh user data to get the new resume URL
        await refreshUser()
        return { success: true, url: data.resumeUrl, name: data.resumeName }
      } else {
        return { success: false, message: data.message }
      }
    } catch (error) {
      console.error('Resume upload error:', error)
      return { success: false, message: 'Server connection failed' }
    }
  }

  async function setDefaultResume(resume_id) {
    if (!user.value?.email) return { success: false, message: 'Not logged in' }

    try {
      const response = await fetch(`${API_BASE_URL}/api/profile/set-default-resume`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: user.value.email, resume_id })
      })
      const data = await response.json()

      if (data.status === 'success') {
        // Refresh user data to get the new default statuses
        await refreshUser()
        return { success: true }
      } else {
        return { success: false, message: data.message }
      }
    } catch (error) {
      console.error('Set default resume error:', error)
      return { success: false, message: 'Server connection failed' }
    }
  }

  function logout() {
    user.value = null
    localStorage.removeItem('auth_user')
    localStorage.removeItem('user_role')
  }

  return {
    user,
    role,
    isAuthenticated,
    isRecruiter,
    isCandidate,
    login,
    signup,
    updateProfile,
    uploadResume,
    setDefaultResume,
    refreshUser,
    logout
  }
})

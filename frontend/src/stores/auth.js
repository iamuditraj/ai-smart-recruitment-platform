import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { loginUser, signupUser, updateProfile as updateProfileApi, getProfile } from '../utils/api'
import { useResumeActions } from '../composables/useResumeActions'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('auth_user') || 'null'))
  const resumes = ref([])

  // Derive role directly from user object so it is always in sync.
  // Falls back to localStorage so the sidebar renders correctly on first load.
  const role = computed(() => user.value?.role || localStorage.getItem('user_role') || null)

  const isAuthenticated = computed(() => !!user.value)
  const isRecruiter = computed(() => role.value === 'recruiter')
  const isCandidate = computed(() => role.value === 'candidate')

  const handleApiError = (context, error) => {
    console.error(`${context} error:`, error)
    return { success: false, message: error.message || 'Server connection failed' }
  }

  async function login(email, password) {
    try {
      const data = await loginUser(email, password)
      user.value = data.user
      localStorage.setItem('auth_user', JSON.stringify(data.user))
      localStorage.setItem('user_role', data.user.role)
      return { success: true }
    } catch (error) {
      return handleApiError('Login', error)
    }
  }

  async function signup(userData) {
    try {
      const data = await signupUser(userData)
      user.value = data.user
      localStorage.setItem('auth_user', JSON.stringify(data.user))
      localStorage.setItem('user_role', data.user.role)
      return { success: true }
    } catch (error) {
      return handleApiError('Signup', error)
    }
  }

  async function loginWithGoogle(role = null) {
    try {
      const { signInWithPopup } = await import('firebase/auth')
      const { auth, googleProvider } = await import('../utils/firebase')
      
      const result = await signInWithPopup(auth, googleProvider)
      const idToken = await result.user.getIdToken()
      
      // We import googleAuth from api here since it acts nicely alongside the others
      const { googleAuth } = await import('../utils/api')
      const data = await googleAuth(idToken, role)
      
      user.value = data.user
      localStorage.setItem('auth_user', JSON.stringify(data.user))
      localStorage.setItem('user_role', data.user.role)
      return { success: true }
    } catch (error) {
      if (error.code === 'auth/popup-closed-by-user') {
         return { success: false, message: 'Google sign in was cancelled' };
      }
      return handleApiError('Google Auth', error)
    }
  }

  async function updateProfile(profileData) {
    try {
      const data = await updateProfileApi({ ...profileData, email: user.value.email })
      user.value = data.user
      localStorage.setItem('auth_user', JSON.stringify(data.user))
      return { success: true }
    } catch (error) {
      return handleApiError('Profile update', error)
    }
  }

  async function refreshUser() {
    if (!user.value?.email) return
    try {
      const data = await getProfile(user.value.email)
      user.value = data.user
      localStorage.setItem('auth_user', JSON.stringify(data.user))
      // Keep user_role in sync so role computed stays correct even before vue reactivity settles
      if (data.user.role) {
        localStorage.setItem('user_role', data.user.role)
      }
    } catch (error) {
      console.error('Refresh user error:', error)
    }
    await resumeActions.fetchResumes()
  }

  function logout() {
    user.value = null
    localStorage.removeItem('auth_user')
    localStorage.removeItem('user_role')
  }

  const storeInstance = { user, resumes, refreshUser }
  const resumeActions = useResumeActions(storeInstance)

  return {
    user,
    role,
    resumes,
    isAuthenticated,
    isRecruiter,
    isCandidate,
    login,
    signup,
    loginWithGoogle,
    updateProfile,
    uploadResume: resumeActions.uploadResume,
    setDefaultResume: resumeActions.setDefaultResume,
    refreshUser,
    fetchResumes: resumeActions.fetchResumes,
    logout
  }
})

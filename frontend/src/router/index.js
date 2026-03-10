import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: { name: 'dashboard' },
    },
    {
      path: '/welcome',
      name: 'welcome',
      component: HomeView,
      meta: { title: 'Welcome — HireAI' },
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { title: 'Login — HireAI' },
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/SignupView.vue'),
      meta: { title: 'Sign Up — HireAI' },
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { title: 'My Profile — HireAI', requiresAuth: true },
    },
    {
      path: '/jobs',
      name: 'jobs',
      component: () => import('../views/BrowseJobsView.vue'),
      meta: { title: 'Find Jobs — HireAI', requiresAuth: true },
    },
    {
      path: '/manage-jobs',
      name: 'manage-jobs',
      component: () => import('../views/RecruiterJobsView.vue'),
      meta: { title: 'Post Jobs — HireAI', requiresAuth: true },
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardWrapper.vue'),
      meta: { title: 'Dashboard — HireAI', requiresAuth: true },
    },
    {
      path: '/resume-generation',
      name: 'resume-generation',
      component: () => import('../views/ResumeGenerationView.vue'),
      meta: { title: 'Resume Builder — HireAI', requiresAuth: true, role: 'candidate' },
    },
    {
      path: '/candidate-ranking',
      name: 'candidate-ranking',
      component: () => import('../views/CandidatesView.vue'),
      meta: { title: 'Candidate Ranking — HireAI', requiresAuth: true, role: 'recruiter' },
    },
    {
      path: '/skill-assessment',
      name: 'skill-assessment',
      component: () => import('../views/SkillAssessmentView.vue'),
      meta: { title: 'Skill Assessment — HireAI', requiresAuth: true, role: 'candidate' },
    },
    {
      path: '/mock-interview',
      name: 'mock-interview',
      component: () => import('../views/MockInterviewView.vue'),
      meta: { title: 'AI Mock Interview — HireAI', requiresAuth: true, role: 'candidate' },
    },
  ],
  scrollBehavior() {
    return { top: 0, behavior: 'smooth' }
  },
})

// Navigation Guard
router.beforeEach((to) => {
  const auth = useAuthStore()

  // Update page title
  document.title = to.meta?.title || 'HireAI — Smart Recruitment Platform'

  // Check if route requires auth
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'login' }
  }

  // Check role-based access
  if (to.meta.role && auth.role !== to.meta.role) {
    return { name: 'dashboard' }
  }
})

export default router

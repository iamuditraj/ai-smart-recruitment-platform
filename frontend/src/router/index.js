import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import HomeView from '../views/shared/HomeView.vue'

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
      component: () => import('../views/shared/LoginView.vue'),
      meta: { title: 'Login — HireAI' },
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/shared/SignupView.vue'),
      meta: { title: 'Sign Up — HireAI' },
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/shared/ProfileWrapper.vue'),
      meta: { title: 'My Profile — HireAI', requiresAuth: true },
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/shared/DashboardWrapper.vue'),
      meta: { title: 'Dashboard — HireAI', requiresAuth: true },
    },

    // ── Candidate Routes ──────────────────────────────────────────────────────
    {
      path: '/jobs',
      name: 'jobs',
      component: () => import('../views/candidate/BrowseJobsView.vue'),
      meta: { title: 'Find Jobs — HireAI', requiresAuth: true, role: 'candidate' },
    },
    {
      path: '/resume-generation',
      name: 'resume-generation',
      component: () => import('../views/candidate/ResumeGenerationView.vue'),
      meta: { title: 'Resume Builder — HireAI', requiresAuth: true, role: 'candidate' },
    },
    {
      path: '/skill-assessment',
      name: 'skill-assessment',
      component: () => import('../views/candidate/SkillAssessmentView.vue'),
      meta: { title: 'Skill Assessment — HireAI', requiresAuth: true, role: 'candidate' },
    },
    {
      path: '/mock-interview',
      name: 'mock-interview',
      component: () => import('../views/candidate/MockInterviewView.vue'),
      meta: { title: 'AI Mock Interview — HireAI', requiresAuth: true, role: 'candidate' },
    },

    // ── Recruiter Routes ──────────────────────────────────────────────────────
    {
      path: '/manage-jobs',
      name: 'manage-jobs',
      component: () => import('../views/recruiter/RecruiterJobsView.vue'),
      meta: { title: 'Post Jobs — HireAI', requiresAuth: true, role: 'recruiter' },
    },
    {
      path: '/candidate-ranking',
      name: 'candidate-ranking',
      component: () => import('../views/recruiter/CandidatesView.vue'),
      meta: { title: 'Candidate Ranking — HireAI', requiresAuth: true, role: 'recruiter' },
    },
    {
      path: '/resume-screening',
      name: 'resume-screening',
      component: () => import('../views/recruiter/ResumeScreeningView.vue'),
      meta: { title: 'Resume Screening — HireAI', requiresAuth: true, role: 'recruiter' },
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

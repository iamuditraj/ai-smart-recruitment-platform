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
      meta: { title: 'Welcome — hireAI' },
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/shared/LoginView.vue'),
      meta: { title: 'Login — hireAI' },
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/shared/SignupView.vue'),
      meta: { title: 'Sign Up — hireAI' },
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../components/RoleWrapper.vue'),
      props: {
        recruiterComponent: '../views/recruiter/RecruiterProfileView.vue',
        candidateComponent: '../views/candidate/CandidateProfileView.vue'
      },
      meta: { title: 'My Profile — hireAI', requiresAuth: true },
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../components/RoleWrapper.vue'),
      props: {
        recruiterComponent: '../views/recruiter/DashboardView.vue',
        candidateComponent: '../views/candidate/CandidateDashboardView.vue'
      },
      meta: { title: 'Dashboard — hireAI', requiresAuth: true },
    },

    // ── Candidate Routes ──────────────────────────────────────────────────────
    {
      path: '/jobs',
      name: 'jobs',
      component: () => import('../views/candidate/BrowseJobsView.vue'),
      meta: { title: 'Find Jobs — hireAI', requiresAuth: true, role: 'candidate' },
    },
    {
      path: '/my-applications',
      name: 'my-applications',
      component: () => import('../views/candidate/MyApplicationsView.vue'),
      meta: { title: 'My Applications — hireAI', requiresAuth: true, role: 'candidate' },
    },
    {
      path: '/resume-generation',
      name: 'resume-generation',
      component: () => import('../views/candidate/ResumeGenerationView.vue'),
      meta: { title: 'Resume Builder — hireAI', requiresAuth: true, role: 'candidate' },
    },
    {
      path: '/resume-hub',
      name: 'resume-hub',
      component: () => import('../views/candidate/ResumeHubView.vue'),
      meta: { title: 'Resume Hub — hireAI', requiresAuth: true, role: 'candidate' },
    },
    {
      path: '/skill-assessment',
      name: 'skill-assessment',
      component: () => import('../views/candidate/SkillAssessmentView.vue'),
      meta: { title: 'Skill Assessment — hireAI', requiresAuth: true, role: 'candidate' },
    },
    {
      path: '/mock-interview',
      name: 'mock-interview',
      component: () => import('../views/candidate/MockInterviewView.vue'),
      meta: { title: 'AI Mock Interview — hireAI', requiresAuth: true, role: 'candidate' },
    },

    // ── Recruiter Routes ──────────────────────────────────────────────────────
    {
      path: '/manage-jobs',
      name: 'manage-jobs',
      component: () => import('../views/recruiter/RecruiterJobsView.vue'),
      meta: { title: 'Post Jobs — hireAI', requiresAuth: true, role: 'recruiter' },
    },
    {
      path: '/post-job',
      name: 'post-job',
      component: () => import('../views/recruiter/RecruiterPostJobView.vue'),
      meta: { title: 'Post Hiring Request — hireAI', requiresAuth: true, role: 'recruiter' },
    },
    {
      path: '/edit-job/:id',
      name: 'edit-job',
      component: () => import('../views/recruiter/RecruiterPostJobView.vue'),
      meta: { title: 'Edit Hiring Request — hireAI', requiresAuth: true, role: 'recruiter' },
    },
    {
      path: '/manage-jobs/:jobId/applications',
      name: 'job-applications',
      component: () => import('../views/recruiter/JobApplicationsView.vue'),
      meta: { title: 'Manage Applications — hireAI', requiresAuth: true, role: 'recruiter' },
    },
    {
      path: '/resume-screening',
      name: 'resume-screening',
      component: () => import('../views/recruiter/ResumeScreeningView.vue'),
      meta: { title: 'Resume Screening — hireAI', requiresAuth: true, role: 'recruiter' },
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
  document.title = to.meta?.title || 'hireAI — Smart Recruitment Platform'

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

import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { title: 'HireAI — Smart Recruitment Platform' },
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: { title: 'Dashboard — HireAI' },
    },
    {
      path: '/resume-generation',
      name: 'resume-generation',
      component: () => import('../views/ResumeGenerationView.vue'),
      meta: { title: 'Resume Builder — HireAI' },
    },
    {
      path: '/resume-screening',
      name: 'resume-screening',
      component: () => import('../views/ResumeScreeningView.vue'),
      meta: { title: 'Resume Screening — HireAI' },
    },
    {
      path: '/candidates',
      name: 'candidates',
      component: () => import('../views/CandidatesView.vue'),
      meta: { title: 'Candidates — HireAI' },
    },
    {
      path: '/skill-assessment',
      name: 'skill-assessment',
      component: () => import('../views/SkillAssessmentView.vue'),
      meta: { title: 'Skill Assessment — HireAI' },
    },
  ],
  scrollBehavior() {
    return { top: 0, behavior: 'smooth' }
  },
})

// Update page title on route change
router.afterEach((to) => {
  document.title = to.meta?.title || 'HireAI'
})

export default router

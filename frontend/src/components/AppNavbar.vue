<template>
  <aside class="sidebar" :class="{ 'sidebar--collapsed': uiStore.isSidebarCollapsed }">
    <!-- Sidebar Header -->
    <div class="sidebar__header" @click="uiStore.toggleSidebar" style="cursor: pointer;">
      <div v-if="!uiStore.isSidebarCollapsed" class="sidebar__brand">
        <div class="brand-logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
            <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
          </svg>
        </div>
        <span class="brand-text">hire<span class="brand-text--accent">AI</span></span>
      </div>
      <div v-else class="brand-logo">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
          <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
          <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
        </svg>
      </div>
    </div>

    <!-- Navigation -->
    <div class="sidebar__content">
      <div v-for="group in filteredGroups" :key="group.name" class="sidebar__group">
        <h3 v-if="group.name && !uiStore.isSidebarCollapsed" class="group-title">{{ group.name }}</h3>
        <div class="group-links">
          <RouterLink
            v-for="link in group.links"
            :key="link.name"
            :to="link.to"
            class="nav-item"
            active-class="nav-item--active"
            :title="uiStore.isSidebarCollapsed ? link.name : ''"
          >
            <span class="nav-icon" v-html="link.icon"></span>
            <span class="nav-text" v-if="!uiStore.isSidebarCollapsed">{{ link.name }}</span>
          </RouterLink>
        </div>
      </div>
    </div>

    <!-- Footer / User Profile -->
    <div class="sidebar__footer">
      <div class="sidebar__user" v-if="authStore.isAuthenticated">
        <div class="user-avatar" :title="authStore.user?.name">
          <img v-if="authStore.user?.photo" :src="authStore.user.photo" alt="Avatar" class="avatar-img">
          <span v-else>{{ authStore.user?.name?.charAt(0).toUpperCase() }}</span>
        </div>
        <div class="user-info" v-if="!uiStore.isSidebarCollapsed">
          <span class="user-name">{{ authStore.user?.name }}</span>
          <span class="user-role">{{ authStore.role }}</span>
        </div>
        <button v-if="!uiStore.isSidebarCollapsed" @click="handleLogout" class="logout-btn" title="Sign Out">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
        </button>
      </div>
      <button v-if="uiStore.isSidebarCollapsed" @click="handleLogout" class="nav-item signout-btn-collapsed" title="Logout">
        <span class="nav-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
        </span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useUIStore } from '../stores/ui'

const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUIStore()

const sidebarGroups = [
  {
    name: 'Dashboard',
    links: [
      {
        name: 'Overview',
        to: '/dashboard',
        roles: ['recruiter', 'candidate'],
        icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>`,
      },
      {
        name: 'Profile',
        to: '/profile',
        roles: ['recruiter', 'candidate'],
        icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`,
      },
    ]
  },
  {
    name: 'Candidate Hub',
    links: [
      {
        name: 'Browse Jobs',
        to: '/jobs',
        roles: ['candidate'],
        icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>`,
      },
      {
        name: 'My Applications',
        to: '/my-applications',
        roles: ['candidate'],
        icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><path d="M9 14l2 2 4-4"/></svg>`,
      },
      {
        name: 'Resume Builder',
        to: '/resume-generation',
        roles: ['candidate'],
        icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>`,
      },
      {
        name: 'Resume Hub',
        to: '/resume-hub',
        roles: ['candidate'],
        icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>`,
      },
      {
        name: 'Skill Assessment',
        to: '/skill-assessment',
        roles: ['candidate'],
        icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>`,
      },
      {
        name: 'Mock Interview',
        to: '/mock-interview',
        roles: ['candidate'],
        icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>`,
      },
    ]
  },
  {
    name: 'Recruiter Suite',
    links: [
      {
        name: 'Manage Jobs',
        to: '/manage-jobs',
        roles: ['recruiter'],
        icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>`,
      },
      {
        name: 'ATS Scanner',
        to: '/resume-screening',
        roles: ['recruiter'],
        icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>`,
      },
    ]
  }
]

const filteredGroups = computed(() => {
  if (!authStore.isAuthenticated) return []
  return sidebarGroups
    .map(group => ({
      ...group,
      links: group.links.filter(link => link.roles.includes(authStore.role))
    }))
    .filter(group => group.links.length > 0)
})

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  width: 280px;
  height: 100vh;
  background: var(--clr-surface);
  border-right: 1px solid var(--clr-border);
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  flex-shrink: 0;
  z-index: 1000;
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.02);
}

.sidebar--collapsed {
  width: 80px;
}

.sidebar__header {
  height: 70px;
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  border-bottom: 1px solid var(--clr-border);
}

.sidebar--collapsed .sidebar__header {
  justify-content: center;
  padding: 0;
}

.sidebar__brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-logo {
  width: 32px;
  height: 32px;
  background: var(--clr-primary);
  color: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.brand-text {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--clr-text);
  letter-spacing: -0.02em;
  font-family: var(--font-heading);
}

.brand-text--accent {
  color: var(--clr-primary);
}

.sidebar__content {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.sidebar__content::-webkit-scrollbar {
  width: 4px;
}

.sidebar__content::-webkit-scrollbar-thumb {
  background: var(--clr-surface-3);
  border-radius: 10px;
}

.group-title {
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--clr-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 0 1rem;
  margin-bottom: 0.75rem;
}

.group-links {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  color: var(--clr-text-muted);
  text-decoration: none;
  font-size: 0.925rem;
  font-weight: 500;
  transition: all 0.2s ease;
  cursor: pointer;
  border: none;
  background: transparent;
  width: 100%;
}

.nav-item:hover {
  background: var(--clr-surface-2);
  color: var(--clr-text);
}

.nav-item--active {
  background: var(--gradient-glow);
  color: var(--clr-primary);
  font-weight: 600;
  box-shadow: inset 0 0 0 1px rgba(99, 102, 241, 0.1);
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  flex-shrink: 0;
}

.nav-text {
  white-space: nowrap;
}

.sidebar__footer {
  padding: 1rem 0.75rem;
  border-top: 1px solid var(--clr-border);
  background: var(--clr-bg);
}

.sidebar__user {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0.5rem;
  border-radius: 10px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: var(--clr-primary);
  color: white;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  flex-shrink: 0;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-info {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.user-name {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--clr-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 0.75rem;
  color: var(--clr-text-muted);
  text-transform: capitalize;
}

.logout-btn {
  background: transparent;
  border: none;
  color: var(--clr-text-light);
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: var(--clr-danger);
  color: white;
  opacity: 0.1; /* This was meant to be background opacity but it affects content, will fix to rgba in real css if needed but here keeping simplicity */
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.signout-btn-collapsed {
  justify-content: center;
  color: var(--clr-danger);
}

.signout-btn-collapsed:hover {
  background: rgba(239, 68, 68, 0.1);
}

/* Sidebar Collapsed items */
.sidebar--collapsed .nav-item {
  justify-content: center;
  padding: 0.75rem 0;
}

.sidebar--collapsed .sidebar__user {
  justify-content: center;
  padding: 0.5rem 0;
}
</style>


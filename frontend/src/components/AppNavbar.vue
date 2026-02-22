<template>
  <header class="navbar" :class="{ 'navbar--scrolled': isScrolled }">
    <div class="container navbar__inner">
      <!-- Logo -->
      <RouterLink to="/" class="navbar__logo" id="nav-logo">
        <div class="navbar__logo-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="url(#grad1)" stroke-width="2" stroke-linejoin="round"/>
            <path d="M2 17L12 22L22 17" stroke="url(#grad1)" stroke-width="2" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="url(#grad1)" stroke-width="2" stroke-linejoin="round"/>
            <defs>
              <linearGradient id="grad1" x1="2" y1="2" x2="22" y2="22" gradientUnits="userSpaceOnUse">
                <stop stop-color="#6366f1"/>
                <stop offset="0.5" stop-color="#8b5cf6"/>
                <stop offset="1" stop-color="#06b6d4"/>
              </linearGradient>
            </defs>
          </svg>
        </div>
        <span class="navbar__logo-text">Hire<span class="gradient-text">AI</span></span>
      </RouterLink>

      <!-- Desktop Nav Links -->
      <nav class="navbar__links" id="nav-links">
        <RouterLink
          v-for="link in navLinks"
          :key="link.name"
          :to="link.to"
          :id="`nav-link-${link.name.toLowerCase().replace(/\s/g,'-')}`"
          class="navbar__link"
          active-class="navbar__link--active"
        >
          <span class="navbar__link-icon" v-html="link.icon"></span>
          {{ link.name }}
        </RouterLink>
      </nav>

      <!-- CTA + Mobile Toggle -->
      <div class="navbar__actions">
        <RouterLink to="/resume-screening" class="btn btn-primary navbar__cta" id="nav-cta">
          Get Started
        </RouterLink>
        <button class="navbar__hamburger" :class="{ 'open': mobileOpen }" @click="mobileOpen = !mobileOpen" id="nav-hamburger" aria-label="Toggle menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <Transition name="mobile-menu">
      <div v-if="mobileOpen" class="navbar__mobile" id="nav-mobile-menu">
        <RouterLink
          v-for="link in navLinks"
          :key="link.name"
          :to="link.to"
          class="navbar__mobile-link"
          active-class="navbar__mobile-link--active"
          @click="mobileOpen = false"
        >
          <span v-html="link.icon"></span>
          {{ link.name }}
        </RouterLink>
        <RouterLink to="/resume-screening" class="btn btn-primary w-full" @click="mobileOpen = false">
          Get Started
        </RouterLink>
      </div>
    </Transition>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isScrolled = ref(false)
const mobileOpen = ref(false)

const navLinks = [
  {
    name: 'Dashboard',
    to: '/dashboard',
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>`,
  },
  {
    name: 'Resume Builder',
    to: '/resume-generation',
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>`,
  },
  {
    name: 'Resume Screening',
    to: '/resume-screening',
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="12" y2="17"/></svg>`,
  },
  {
    name: 'Candidates',
    to: '/candidates',
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`,
  },
  {
    name: 'Skill Assessment',
    to: '/skill-assessment',
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>`,
  },
]

function onScroll() {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  width: 100%;
  padding: 0.85rem 0;
  border-bottom: 1px solid transparent;
  transition: background var(--transition-base), border-color var(--transition-base), box-shadow var(--transition-base);
}

.navbar--scrolled {
  background: rgba(10, 13, 20, 0.9);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom-color: var(--clr-border);
  box-shadow: var(--shadow-sm);
}

.navbar__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-6);
}

/* Logo */
.navbar__logo {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  text-decoration: none;
  flex-shrink: 0;
}

.navbar__logo-icon {
  width: 36px;
  height: 36px;
  background: var(--clr-surface-2);
  border: 1px solid var(--clr-border-hover);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: border-color var(--transition-base);
}

.navbar__logo:hover .navbar__logo-icon {
  border-color: var(--clr-primary);
}

.navbar__logo-text {
  font-family: var(--font-heading);
  font-size: 1.3rem;
  font-weight: 800;
  color: var(--clr-text);
  letter-spacing: -0.02em;
}

/* Nav Links */
.navbar__links {
  display: flex;
  align-items: center;
  gap: var(--sp-1);
  flex: 1;
  justify-content: center;
}

.navbar__link {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  padding: 0.45rem 0.9rem;
  border-radius: var(--radius-full);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--clr-text-light);
  text-decoration: none;
  transition: all var(--transition-base);
  white-space: nowrap;
}

.navbar__link:hover {
  color: var(--clr-text);
  background: rgba(255,255,255,0.05);
}

.navbar__link--active {
  color: var(--clr-primary);
  background: rgba(99,102,241,0.1);
}

.navbar__link-icon {
  display: flex;
  align-items: center;
  opacity: 0.7;
}

/* Actions */
.navbar__actions {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  flex-shrink: 0;
}

.navbar__cta {
  font-size: 0.85rem;
  padding: 0.5rem 1.2rem;
}

/* Hamburger */
.navbar__hamburger {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--sp-2);
}

.navbar__hamburger span {
  display: block;
  width: 22px;
  height: 2px;
  background: var(--clr-text);
  border-radius: var(--radius-full);
  transition: all var(--transition-base);
}

.navbar__hamburger.open span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
.navbar__hamburger.open span:nth-child(2) { opacity: 0; }
.navbar__hamburger.open span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }

/* Mobile Menu */
.navbar__mobile {
  display: flex;
  flex-direction: column;
  gap: var(--sp-2);
  padding: var(--sp-4) var(--sp-6) var(--sp-6);
  background: rgba(10, 13, 20, 0.98);
  border-top: 1px solid var(--clr-border);
}

.navbar__mobile-link {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  padding: 0.7rem 1rem;
  border-radius: var(--radius-md);
  color: var(--clr-text-light);
  text-decoration: none;
  font-weight: 500;
  transition: all var(--transition-base);
}

.navbar__mobile-link:hover,
.navbar__mobile-link--active {
  color: var(--clr-primary);
  background: rgba(99,102,241,0.1);
}

.mobile-menu-enter-active, .mobile-menu-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.mobile-menu-enter-from, .mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* Responsive */
@media (max-width: 900px) {
  .navbar__links,
  .navbar__cta {
    display: none;
  }
  .navbar__hamburger {
    display: flex;
  }
}
</style>

<template>
  <div id="app-root" :class="{ 'has-sidebar': authStore.isAuthenticated, 'sidebar-collapsed': uiStore.isSidebarCollapsed }">
    <AppNavbar v-if="authStore.isAuthenticated" />

    <div class="main-wrapper">
      <header v-if="authStore.isAuthenticated" class="app-header">
        <div class="header-left">
          <h1 class="page-title">{{ currentPageTitle }}</h1>
        </div>

        <div class="header-right">
          <div class="search-bar">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            <input type="text" placeholder="Search for jobs, candidates...">
          </div>
          <div class="header-actions">
             <button @click="uiStore.toggleTheme" class="icon-btn theme-switch" :title="uiStore.isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'">
               <svg v-if="uiStore.isDarkMode" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="18.36" x2="5.64" y2="16.94"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
               <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
             </button>
             <button class="icon-btn"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path></svg></button>
          </div>
        </div>
      </header>

      <main class="main-content">
        <RouterView v-slot="{ Component }">
          <Transition name="page" mode="out-in">
            <div class="content-area" v-if="Component">
              <component :is="Component" />
            </div>
          </Transition>
        </RouterView>
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppNavbar from './components/AppNavbar.vue'
import { useAuthStore } from './stores/auth'
import { useUIStore } from './stores/ui'

const authStore = useAuthStore()
const uiStore = useUIStore()
const route = useRoute()

const currentPageTitle = computed(() => {
  // Prefer the human-readable meta.title, strip the " — HireAI" suffix
  if (route.meta?.title) {
    return route.meta.title.replace(/\s*—.*$/, '')
  }
  // Fall back to transforming the route name
  const name = route.name || 'Dashboard'
  return name.toString()
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
})
</script>

<style scoped>
#app-root {
  display: flex;
  min-height: 100vh;
  background-color: var(--clr-bg);
  color: var(--clr-text);
}

.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  transition: all 0.3s ease;
}

.app-header {
  height: 70px;
  background: var(--clr-surface);
  border-bottom: 1px solid var(--clr-border);
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 900;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.header-toggle-btn {
  background: transparent;
  border: none;
  color: var(--clr-text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
}

.header-toggle-btn:hover {
  background: var(--clr-surface-2);
  color: var(--clr-primary);
}

.page-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--clr-text);
  text-transform: capitalize;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--clr-surface-2);
  padding: 0.5rem 1rem;
  border-radius: 10px;
  width: 300px;
  color: var(--clr-text-muted);
}

.search-bar input {
  background: transparent;
  border: none;
  outline: none;
  font-size: 0.9rem;
  width: 100%;
  color: var(--clr-text);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.icon-btn {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  border: none;
  background: transparent;
  color: var(--clr-text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.icon-btn:hover {
  background: var(--clr-surface-2);
  color: var(--clr-primary);
}

.main-content {
  flex: 1;
  padding: 0;
  overflow-y: auto;
}

#app-root:not(.has-sidebar) {
  display: block;
}

#app-root:not(.has-sidebar) .main-wrapper {
  height: 100vh;
}

/* Transitions */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>


import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUIStore = defineStore('ui', () => {
  const isSidebarCollapsed = ref(localStorage.getItem('sidebar_collapsed') === 'true')
  const isDarkMode = ref(localStorage.getItem('theme') === 'dark' ||
    (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches))

  function toggleSidebar() {
    isSidebarCollapsed.value = !isSidebarCollapsed.value
    localStorage.setItem('sidebar_collapsed', isSidebarCollapsed.value)
  }

  function setSidebar(value) {
    isSidebarCollapsed.value = value
    localStorage.setItem('sidebar_collapsed', value)
  }

  function toggleTheme() {
    isDarkMode.value = !isDarkMode.value
    localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light')
    updateThemeClass()
  }

  function updateThemeClass() {
    if (isDarkMode.value) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  // Initialize theme on store creation
  updateThemeClass()

  return {
    isSidebarCollapsed,
    isDarkMode,
    toggleSidebar,
    setSidebar,
    toggleTheme
  }
})

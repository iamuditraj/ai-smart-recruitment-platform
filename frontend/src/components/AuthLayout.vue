<template>
  <div class="login-view section">
    <div class="container small-container">
      <div class="login-card card animate-fade-in-up">
        <div class="login-header text-center">
          <div class="login-logo-container">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="url(#grad-login)" stroke-width="2" stroke-linejoin="round"/>
              <path d="M2 17L12 22L22 17" stroke="url(#grad-login)" stroke-width="2" stroke-linejoin="round"/>
              <path d="M2 12L12 17L22 12" stroke="url(#grad-login)" stroke-width="2" stroke-linejoin="round"/>
              <defs>
                <linearGradient id="grad-login" x1="2" y1="2" x2="22" y2="22" gradientUnits="userSpaceOnUse">
                  <stop stop-color="#6366f1"/>
                  <stop offset="0.5" stop-color="#8b5cf6"/>
                  <stop offset="1" stop-color="#06b6d4"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <h1 class="login-title">
            <slot name="title">{{ title }}</slot>
          </h1>
          <p class="login-subtitle">
            <slot name="subtitle">{{ subtitle }}</slot>
          </p>
        </div>

        <slot></slot>

        <div v-if="$slots.footer" class="login-extra text-center mt-6">
          <slot name="footer"></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  subtitle: String
})
</script>

<style scoped>
.login-view {
  min-height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.small-container {
  max-width: 440px;
}

.login-card {
  padding: var(--sp-10);
  border: 1px solid var(--clr-border);
  box-shadow: var(--shadow-lg);
}

.login-header {
  margin-bottom: var(--sp-8);
}

.login-logo-container {
  margin-bottom: var(--sp-4);
  display: flex;
  justify-content: center;
}

.login-title {
  font-size: 1.75rem;
  font-weight: 800;
  margin-bottom: var(--sp-2);
}

.login-subtitle {
  color: var(--clr-text-muted);
  font-size: 0.95rem;
}

.mt-6 {
  margin-top: 1.5rem;
}
</style>

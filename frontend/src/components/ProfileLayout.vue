<template>
  <div>
    <PageHeader 
      :title="title" 
      :subtitle="subtitle"
    >
      <template #actions>
        <slot name="header-actions"></slot>
      </template>
    </PageHeader>

    <div class="profile-content grid">
      <!-- Left: Static Info -->
      <div class="profile-card card animate-fade-in-up" style="animation-delay: 0.1s">
         <slot name="left-pane"></slot>
      </div>

      <!-- Right: Edit Form -->
      <div class="profile-form card animate-fade-in-up" style="animation-delay: 0.2s">
        <form @submit.prevent="$emit('save')">
          <slot name="form-title">
              <h3 class="subsection-title" v-if="formTitle">{{ formTitle }}</h3>
          </slot>

          <AppAlert v-if="message" :message="message" :type="messageType" />

          <slot name="form-fields"></slot>

          <div class="profile-actions mt-8">
            <button type="submit" class="btn btn-primary" :disabled="isSaving">
              <span v-if="!isSaving">Save Changes</span>
              <AppSpinner v-else size="sm" />
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import PageHeader from '@/components/PageHeader.vue'
import AppAlert from '@/components/AppAlert.vue'
import AppSpinner from '@/components/AppSpinner.vue'

defineProps({
  title: String,
  subtitle: String,
  formTitle: String,
  message: String,
  messageType: String,
  isSaving: Boolean
})

defineEmits(['save'])
</script>

<style scoped>
.profile-content {
  grid-template-columns: 320px 1fr;
  align-items: start;
  gap: var(--sp-6);
  max-width: 100%;
}

.profile-card,
.profile-form {
  min-width: 0;
  overflow: hidden;
}

:global(.header-content) { display: flex; justify-content: space-between; align-items: center; }

:global(.profile-info-list) { margin-top: 2rem; display: flex; flex-direction: column; gap: 1.25rem; }
:global(.info-item) { display: flex; flex-direction: column; gap: 4px; }
:global(.info-item .label) { font-size: 0.75rem; color: var(--clr-text-muted); text-transform: uppercase; font-weight: 600; }
:global(.info-item .value) { font-weight: 600; color: var(--clr-text); }

:global(.form-grid) { display: grid; grid-template-columns: 1fr 1fr; gap: var(--sp-6); }
:global(.mx-auto) { margin-inline: auto; }

@media (max-width: 1000px) {
  .profile-content { grid-template-columns: 1fr; }
}

@media (max-width: 600px) {
  :global(.form-grid) { grid-template-columns: 1fr; }
  :global(.header-content) { flex-direction: column; align-items: flex-start; gap: 1rem; }
  .profile-card, .profile-form { padding: var(--sp-4) !important; }
  .profile-content { gap: var(--sp-4); }
}
</style>

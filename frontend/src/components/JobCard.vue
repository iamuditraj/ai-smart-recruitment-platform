<template>
  <div class="job-card card">
    <div class="job-card__header">
      <div v-if="job.company && showCompanyInfo" class="job-company-logo">
        {{ job.company[0] }}
      </div>
      <div class="job-meta">
        <h3 class="job-title">{{ job.title }}</h3>
        <p v-if="job.company && showCompanyInfo" class="job-company">{{ job.company }}</p>
      </div>
      <span v-if="job.type" class="job-type-badge">{{ job.type }}</span>
    </div>

    <div class="job-details">
      <div class="detail-item" v-if="job.location">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
        <span>{{ job.location }}</span>
      </div>
      <div class="detail-item" v-if="job.salary">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
        <span>{{ job.salary }}</span>
      </div>
    </div>

    <p class="job-description">{{ job.jobSummary || job.description }}</p>

    <div class="job-actions">
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  job: {
    type: Object,
    required: true
  },
  showCompanyInfo: {
    type: Boolean,
    default: true
  }
})
</script>

<style scoped>
.job-card {
  display: flex !important;
  flex-direction: column;
  gap: var(--sp-4);
  padding: var(--sp-6);
  height: 100%;
}

.job-card__header {
  display: flex;
  align-items: flex-start;
  gap: var(--sp-4);
}

.job-company-logo {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  background: var(--clr-surface-2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--clr-primary);
  flex-shrink: 0;
}

.job-meta {
  flex: 1;
}

.job-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--clr-text);
  margin-bottom: 0.2rem;
}

.job-company {
  font-size: 0.9rem;
  color: var(--clr-text-muted);
}

.job-type-badge {
  background: var(--gradient-brand);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 99px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.job-details {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sp-4);
  padding: var(--sp-4) 0;
  border-top: 1px solid var(--clr-border);
  border-bottom: 1px solid var(--clr-border);
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: var(--clr-text-muted);
}
.detail-item svg {
  color: var(--clr-primary);
  opacity: 0.8;
}

.job-description {
  font-size: 0.9rem;
  color: var(--clr-text-muted);
  line-height: 1.6;
  flex-grow: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.job-actions {
  display: flex;
  gap: var(--sp-3);
  margin-top: auto;
  padding-top: var(--sp-2);
}
.job-actions :deep(.btn) {
  flex: 1;
}
</style>

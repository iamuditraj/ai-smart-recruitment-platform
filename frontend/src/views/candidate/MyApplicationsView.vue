<template>
  <div class="my-apps">
    <div class="content-area">
      <!-- Header -->
      <PageHeader
        title="My Applications"
        subtitle="Track all jobs you've applied to and their current status">
        <template #actions>
          <div class="stats-row">
            <KpiCard
              label="Total"
              :value="applications.length"
              variant="simple"
              style="flex: 1;"
            />
            <KpiCard
              label="Shortlisted"
              :value="statusCounts.Shortlisted"
              variant="simple"
              style="flex: 1; --clr-text: #10b981;"
            />
            <KpiCard
              label="Pending"
              :value="statusCounts.Applied"
              variant="simple"
              style="flex: 1; --clr-text: #f59e0b;"
            />
            <KpiCard
              label="Rejected"
              :value="statusCounts.Rejected"
              variant="simple"
              style="flex: 1; --clr-text: #ef4444;"
            />
          </div>
        </template>
      </PageHeader>

      <!-- Filter Tabs -->
      <AppFilterTabs
        v-model="activeFilter"
        :tabs="['All', 'Applied', 'Shortlisted', 'Rejected']"
        :counts="statusCounts"
      />

      <!-- Loading State -->
      <div v-if="isLoading" class="loading-box card animate-fade-in">
        <AppSpinner size="md" />
        <p>Loading your applications...</p>
      </div>

      <!-- Applications List -->
      <div v-else-if="filteredApps.length > 0" class="apps-list animate-fade-in-up" style="animation-delay: 0.1s">
        <div v-for="app in filteredApps" :key="app.id" class="app-card card" :id="`app-${app.id}`">
          <div class="app-card__left">
            <div class="company-logo" :style="`background: ${avatarGrad(app.company)}`">
              {{ (app.company || '?')[0] }}
            </div>
            <div class="app-info">
              <h3 class="app-job-title">{{ app.job_title }}</h3>
              <p class="app-company">{{ app.company }}<span v-if="app.location"> · {{ app.location }}</span></p>
              <div class="app-meta">
                <span v-if="app.job_type" class="meta-tag">{{ app.job_type }}</span>
                <span class="meta-date">Applied {{ formatDate(app.applied_at) }}</span>
              </div>
            </div>
          </div>

          <div class="app-card__right">
            <!-- Recruiter Contact (Conditionally Visible) -->
            <div v-if="app.recruiter_email" class="recruiter-contact gap-row">
              <span class="contact-label">Recruiter Contact:</span>
              <a :href="`mailto:${app.recruiter_email}`" class="contact-link" title="Click to email">{{ app.recruiter_email }}</a>
            </div>

            <!-- ATS Score -->
            <div class="score-ring">
              <ScoreRing :score="app.ats_score || 0" :size="52" />
            </div>

            <!-- Status Badge -->
            <span class="status-badge" :class="getStatusClass(app.status)">
              <span class="status-dot"></span>
              {{ app.status }}
            </span>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <AppEmptyState
        v-else
        icon="📋"
        :title="activeFilter === 'All' ? 'No applications' : 'No applications with status \'' + activeFilter + '\''"
      >
        <p v-if="activeFilter === 'All'">You haven't applied to any jobs yet. <router-link to="/jobs" class="link-primary">Browse opportunities →</router-link></p>
        <p v-else>No applications match this filter.</p>
      </AppEmptyState>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { formatDate } from '@/utils/dateUtils'
import AppSpinner from '@/components/AppSpinner.vue'
import AppAlert from '@/components/AppAlert.vue'
import AppEmptyState from '@/components/AppEmptyState.vue'
import AppFilterTabs from '@/components/AppFilterTabs.vue'
import KpiCard from '@/components/KpiCard.vue'
import PageHeader from '@/components/PageHeader.vue'
import ScoreRing from '@/components/ScoreRing.vue'
import { getCandidateApplications } from '@/utils/api'
import { avatarGrad, getStatusClass } from '@/utils/uiHelpers'

const authStore = useAuthStore()

const applications = ref([])
const isLoading = ref(true)
const activeFilter = ref('All')

const statusCounts = computed(() => {
  const counts = { Applied: 0, Shortlisted: 0, Rejected: 0 }
  applications.value.forEach(a => {
    if (counts[a.status] !== undefined) counts[a.status]++
  })
  return counts
})

const filteredApps = computed(() => {
  if (activeFilter.value === 'All') return applications.value
  return applications.value.filter(a => a.status === activeFilter.value)
})

async function fetchApplications() {
  isLoading.value = true
  try {
    const email = authStore.user?.email
    if (!email) return
    const data = await getCandidateApplications(email)
    applications.value = data.applications
  } catch (err) {
    console.error('Fetch applications error:', err)
  } finally {
    isLoading.value = false
  }
}

function scoreClass(score) {
  if (score >= 80) return 'circle-high'
  if (score >= 50) return 'circle-mid'
  return 'circle-low'
}

onMounted(fetchApplications)
</script>

<style scoped>
/* Stats Row */
.stats-row { display: flex; gap: 0.75rem; flex-wrap: wrap; }





/* ═══ Application Cards ══════════════════════════════════════ */
.apps-list { display: flex; flex-direction: column; gap: var(--sp-3); }

.app-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.75rem;
  gap: 1.5rem;
  border: 1px solid var(--clr-border);
  background: var(--clr-surface);
}

.app-card__left { display: flex; align-items: center; gap: 1rem; flex: 1; min-width: 0; }

.company-logo {
  width: 48px; height: 48px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; color: white; font-size: 1.2rem; flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.app-info { min-width: 0; }
.app-job-title { font-size: 1.05rem; font-weight: 700; color: var(--clr-text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.app-company { font-size: 0.88rem; color: var(--clr-text-muted); margin-top: 2px; }
.app-meta { display: flex; align-items: center; gap: 0.75rem; margin-top: 0.4rem; flex-wrap: wrap; }
.meta-tag {
  background: var(--gradient-glow);
  color: var(--clr-primary);
  padding: 0.15rem 0.6rem;
  border-radius: 6px;
  font-size: 0.7rem;
  font-weight: 700;
  border: 1px solid rgba(99, 102, 241, 0.15);
}
.meta-date { font-size: 0.78rem; color: var(--clr-text-light); }

.app-card__right { display: flex; align-items: center; gap: 1.5rem; flex-shrink: 0; }

/* Recruiter Contact */
.recruiter-contact {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  margin-right: 0.5rem;
}
.contact-label { font-size: 0.65rem; font-weight: 700; text-transform: uppercase; color: var(--clr-text-muted); }
.contact-link { font-size: 0.85rem; font-weight: 600; color: var(--clr-primary); text-decoration: none; }
.contact-link:hover { text-decoration: underline; }

/* Status Badge */
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.35rem 0.85rem;
  border-radius: 99px;
  font-size: 0.78rem;
  font-weight: 700;
  white-space: nowrap;
}
.status-dot { width: 7px; height: 7px; border-radius: 50%; }

/* ═══ Loading & Empty ════════════════════════════════════════ */
.loading-box, .empty-box { text-align: center; padding: 4rem 2rem; }
.loading-box:hover, .empty-box:hover { transform: none; }

/* ═══ Responsive ═════════════════════════════════════════════ */
@media (max-width: 768px) {
  .page-header { flex-direction: column; }
  .page-title { font-size: 1.5rem; }
  .app-card { flex-direction: column; align-items: flex-start; }
  .app-card__right { width: 100%; justify-content: space-between; }
}
</style>

<template>
  <div class="my-apps">
    <div class="content-area">
      <!-- Header -->
      <PageHeader
        title="My Applications"
        subtitle="Track all jobs you've applied to and their pipeline status">
        <template #actions>
          <div class="stats-row">
            <KpiCard
              label="Total"
              :value="applications.length"
              variant="simple"
              style="flex: 1;"
            />
            <KpiCard
              label="Active"
              :value="statusCounts.Active"
              variant="simple"
              style="flex: 1; --clr-text: #10b981;"
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
        :tabs="['All', 'Active', 'Rejected', 'Hired']"
        :counts="statusCounts"
      />

      <!-- Loading State -->
      <div v-if="isLoading" class="loading-box card animate-fade-in">
        <AppSpinner size="md" />
        <p>Loading your applications...</p>
      </div>

      <!-- Applications List -->
      <div v-else-if="filteredApps.length > 0" class="apps-list animate-fade-in-up" style="animation-delay: 0.1s">
        <div v-for="app in filteredApps" :key="app.id" class="app-card card card--no-hover" :id="`app-${app.id}`">
          <!-- Top Row: Basic Info & Contact -->
          <div class="app-header">
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
              <div v-if="app.recruiter_email" class="recruiter-contact gap-row">
                <span class="contact-label">Recruiter Contact:</span>
                <a :href="`mailto:${app.recruiter_email}`" class="contact-link" title="Click to email">{{ app.recruiter_email }}</a>
              </div>
              <div class="score-ring" title="Your ATS Resume Match Score" v-if="app.ats_score !== undefined">
                <ScoreRing :score="app.ats_score || 0" :size="52" />
              </div>
            </div>
          </div>

          <!-- Mid Row: Pipeline Transparency Stepper -->
          <div class="app-pipeline" v-if="app.job_rounds && app.job_rounds.length > 0">
            <h4 class="pipeline-heading">Hiring Pipeline</h4>
            <div class="round-stepper">
              <div class="stepper-track">
                <div
                  v-for="(round, idx) in app.job_rounds"
                  :key="idx"
                  class="stepper-step"
                  :class="getStepClass(app, idx)"
                >
                  <div class="stepper-dot">
                    <svg v-if="getStepStatus(app, idx) === 'cleared'" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                    <svg v-else-if="getStepStatus(app, idx) === 'rejected'" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                    <span v-else>{{ idx + 1 }}</span>
                  </div>
                  <span class="stepper-label">{{ round }}</span>
                  <div v-if="idx < app.job_rounds.length - 1" class="stepper-connector" :class="{ 'stepper-connector--done': getStepStatus(app, idx) === 'cleared' }"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Bottom Row: Communications Log (Drawer) -->
          <details class="comms-drawer" v-if="app.communications_log && app.communications_log.length > 0">
            <summary class="comms-summary">
              <div class="comms-header-info">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                <span>Message History ({{ app.communications_log.length }})</span>
              </div>
              <svg class="chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
            </summary>
            
            <div class="comms-list">
              <div v-for="(msg, i) in app.communications_log.slice().reverse()" :key="i" class="comm-message">
                <div class="comm-meta">
                  <span class="comm-type" :class="`comm-type--${msg.type}`">{{ msg.type }}</span>
                  <span class="comm-date">{{ new Date(msg.sent_at).toLocaleString() }}</span>
                </div>
                <h5 class="comm-subject">{{ msg.subject }}</h5>
                <p class="comm-body">{{ msg.body }}</p>
              </div>
            </div>
          </details>
          
        </div>
      </div>

      <!-- Empty State -->
      <AppEmptyState
        v-else
        icon="📋"
        :title="activeFilter === 'All' ? 'No applications' : 'No applications match filter \'' + activeFilter + '\''"
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
import AppEmptyState from '@/components/AppEmptyState.vue'
import AppFilterTabs from '@/components/AppFilterTabs.vue'
import KpiCard from '@/components/KpiCard.vue'
import PageHeader from '@/components/PageHeader.vue'
import ScoreRing from '@/components/ScoreRing.vue'
import { getCandidateApplications } from '@/utils/api'
import { avatarGrad } from '@/utils/uiHelpers'

const authStore = useAuthStore()

const applications = ref([])
const isLoading = ref(true)
const activeFilter = ref('All')

// ── Status derivation ──────────────────────────────────────────
function isAppRejected(app) {
  return app.terminal_round_index !== null && app.terminal_round_index !== undefined;
}
function isAppHired(app) {
  // If it's cleared the final round, it should have status hired or terminal null but current_idx >= rounds
  return app.status === 'Hired' || (app.job_rounds && app.job_current_round_index >= app.job_rounds.length && !isAppRejected(app));
}
function getAppMacroStatus(app) {
  if (isAppRejected(app)) return 'Rejected';
  if (isAppHired(app)) return 'Hired';
  return 'Active';
}

const statusCounts = computed(() => {
  const counts = { All: applications.value.length, Active: 0, Rejected: 0, Hired: 0 }
  applications.value.forEach(a => {
    const s = getAppMacroStatus(a)
    if (counts[s] !== undefined) counts[s]++
  })
  return counts
})

const filteredApps = computed(() => {
  if (activeFilter.value === 'All') return applications.value
  return applications.value.filter(a => getAppMacroStatus(a) === activeFilter.value)
})

// ── Stepper logic ──────────────────────────────────────────────
function getStepStatus(app, nodeIndex) {
  const isRejected = isAppRejected(app);
  const currentIdx = app.job_current_round_index || 0;
  const terminalIdx = app.terminal_round_index;
  const roundStatus = app.round_status;

  if (isRejected) {
    if (nodeIndex < terminalIdx) return 'cleared';
    if (nodeIndex === terminalIdx) return 'rejected';
    return 'future';
  }

  // Active / Hired
  if (nodeIndex < currentIdx) return 'cleared';
  if (nodeIndex === currentIdx) {
    // If the pipeline is not complete, this round is active.
    // If the candidate is cleared but pipeline not finalized yet, it shows as pending from cand perspective until advance_round runs! 
    return 'active';
  }
  return 'future';
}

function getStepClass(app, nodeIndex) {
  const status = getStepStatus(app, nodeIndex);
  return {
    'stepper-step--completed': status === 'cleared',
    'stepper-step--active': status === 'active',
    'stepper-step--rejected': status === 'rejected',
    'stepper-step--future': status === 'future'
  };
}

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

onMounted(fetchApplications)
</script>

<style scoped>
/* Stats Row */
.stats-row { display: flex; gap: 0.75rem; flex-wrap: wrap; }

/* ═══ Application Cards ══════════════════════════════════════ */
.apps-list { display: flex; flex-direction: column; gap: var(--sp-4); }

.app-card {
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  gap: 1.25rem;
  border: 1px solid var(--clr-border);
  background: var(--clr-surface);
  overflow: hidden;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
}

.app-card__left { display: flex; align-items: center; gap: 1rem; flex: 1; min-width: 0; }

.company-logo {
  width: 48px; height: 48px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; color: white; font-size: 1.2rem; flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.app-info { min-width: 0; }
.app-job-title { font-size: 1.15rem; font-weight: 800; color: var(--clr-text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 0.15rem; }
.app-company { font-size: 0.88rem; font-weight: 600; color: var(--clr-text-muted); }
.app-meta { display: flex; align-items: center; gap: 0.75rem; margin-top: 0.5rem; flex-wrap: wrap; }
.meta-tag {
  background: var(--gradient-glow);
  color: var(--clr-primary);
  padding: 0.15rem 0.6rem;
  border-radius: 6px;
  font-size: 0.7rem;
  font-weight: 700;
  border: 1px solid rgba(99, 102, 241, 0.15);
}
.meta-date { font-size: 0.78rem; font-weight: 500; color: var(--clr-text-light); }

.app-card__right { display: flex; align-items: center; gap: 1.5rem; flex-shrink: 0; }

/* Recruiter Contact */
.recruiter-contact {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}
.contact-label { font-size: 0.65rem; font-weight: 800; text-transform: uppercase; color: var(--clr-text-muted); letter-spacing: 0.05em; }
.contact-link { font-size: 0.85rem; font-weight: 600; color: var(--clr-primary); text-decoration: none; margin-top: 0.15rem;}
.contact-link:hover { text-decoration: underline; }

/* ═══ Pipeline Stepper ═══════════════════════════════════════ */
.app-pipeline {
  padding-top: 1rem;
  border-top: 1px dashed var(--clr-border);
}
.pipeline-heading {
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--clr-text-muted);
  letter-spacing: 0.1em;
  margin-bottom: 1rem;
}

.round-stepper {
  overflow-x: auto;
  padding-bottom: 0.5rem;
}

.stepper-track {
  display: flex;
  align-items: flex-start;
  min-width: max-content;
}

.stepper-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  flex: 1;
  min-width: 90px;
}

.stepper-dot {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: 800;
  z-index: 1;
  transition: all 0.3s;
}

.stepper-step--completed .stepper-dot {
  background: #10b981;
  color: white;
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.15);
}

.stepper-step--active .stepper-dot {
  background: var(--clr-primary);
  color: white;
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
  animation: pulse-dot 2s infinite;
}

.stepper-step--rejected .stepper-dot {
  background: #ef4444;
  color: white;
  box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.15);
}

.stepper-step--future .stepper-dot {
  background: var(--clr-surface-2);
  color: var(--clr-text-muted);
  border: 2px solid var(--clr-border);
}

@keyframes pulse-dot {
  0%, 100% { box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2); }
  50% { box-shadow: 0 0 0 8px rgba(99, 102, 241, 0.08); }
}

.stepper-label {
  margin-top: 0.5rem;
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--clr-text-muted);
  text-align: center;
  white-space: nowrap;
}
.stepper-step--active .stepper-label { color: var(--clr-primary); font-weight: 800; }
.stepper-step--completed .stepper-label { color: #10b981; }
.stepper-step--rejected .stepper-label { color: #ef4444; }

.stepper-connector {
  position: absolute;
  top: 13px;
  left: calc(50% + 14px);
  width: calc(100% - 28px);
  height: 2px;
  background: var(--clr-border);
}
.stepper-connector--done { background: #10b981; }

/* ═══ Communications Drawer ══════════════════════════════════ */
.comms-drawer {
  background: var(--clr-surface-2);
  border-radius: 8px;
  border: 1px solid var(--clr-border);
  overflow: hidden;
}

.comms-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.85rem 1.25rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--clr-text);
  cursor: pointer;
  list-style: none;
  user-select: none;
}
.comms-summary::-webkit-details-marker { display: none; }
.comms-header-info {
  display: flex; align-items: center; gap: 0.5rem;
}
.chevron { transition: transform 0.2s; color: var(--clr-text-muted); }
details[open] .chevron { transform: rotate(180deg); }

.comms-list {
  display: flex;
  flex-direction: column;
  padding: 0;
  border-top: 1px solid var(--clr-border);
}

.comm-message {
  padding: 1.25rem;
  background: var(--clr-surface);
}
.comm-message:not(:last-child) {
  border-bottom: 1px solid var(--clr-border);
}

.comm-meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}
.comm-type {
  font-size: 0.65rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.15rem 0.5rem;
  border-radius: 99px;
  background: var(--clr-surface-2);
  color: var(--clr-text-muted);
}
.comm-type--advancement { background: rgba(99, 102, 241, 0.1); color: var(--clr-primary); }
.comm-type--offer { background: rgba(16, 185, 129, 0.1); color: #10b981; }
.comm-type--rejection { background: rgba(239, 68, 68, 0.1); color: #ef4444; }

.comm-date { font-size: 0.75rem; color: var(--clr-text-light); }
.comm-subject { font-size: 0.95rem; font-weight: 700; color: var(--clr-text); margin-bottom: 0.4rem; }
.comm-body { font-size: 0.85rem; color: var(--clr-text-muted); line-height: 1.6; white-space: pre-wrap; margin: 0;}

/* ═══ Loading & Empty ════════════════════════════════════════ */
.loading-box, .empty-box { text-align: center; padding: 4rem 2rem; }
.loading-box:hover, .empty-box:hover { transform: none; }

/* ═══ Responsive ═════════════════════════════════════════════ */
@media (max-width: 768px) {
  .page-header { flex-direction: column; }
  .page-title { font-size: 1.5rem; }
  .app-header { flex-direction: column; align-items: flex-start; }
  .app-card__right { width: 100%; justify-content: space-between; }
}
</style>

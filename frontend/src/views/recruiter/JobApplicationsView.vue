<template>
  <div class="job-apps">
    <div class="content-area">
      <!-- Back link + Header -->
      <PageHeader
        :title="jobTitle"
        :subtitle="isPipelineComplete ? `${activeApps.length} hired applicant${activeApps.length !== 1 ? 's' : ''}` : `${activeApps.length} active applicant${activeApps.length !== 1 ? 's' : ''} in round ${currentRoundIndex + 1} of ${rounds.length}`"
        backTo="/manage-jobs"
        backLabel="Back to Jobs"
      />

      <!-- ═══ Round Stepper ═══════════════════════════════════════ -->
      <div class="round-stepper card card--no-hover animate-fade-in-up" style="animation-delay:0.03s" id="round-stepper">
        <div class="stepper-track">
          <div
            v-for="(round, idx) in rounds"
            :key="idx"
            class="stepper-step"
            :class="{
              'stepper-step--completed': idx < currentRoundIndex,
              'stepper-step--active': idx === currentRoundIndex,
              'stepper-step--future': idx > currentRoundIndex,
            }"
          >
            <div class="stepper-dot">
              <svg v-if="idx < currentRoundIndex" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
              <span v-else>{{ idx + 1 }}</span>
            </div>
            <span class="stepper-label">{{ round }}</span>
            <div v-if="idx < rounds.length - 1" class="stepper-connector" :class="{ 'stepper-connector--done': idx < currentRoundIndex }"></div>
          </div>
        </div>
      </div>

      <!-- ═══ Cohort KPI Bar ══════════════════════════════════════ -->
      <div class="cohort-bar card card--no-hover animate-fade-in-up" style="animation-delay:0.06s" id="cohort-bar">
        <div class="cohort-stats">
          <div class="cohort-stat">
            <span class="cohort-stat__value">{{ activeApps.length }}</span>
            <span class="cohort-stat__label">Active</span>
          </div>
          <div class="cohort-stat cohort-stat--cleared">
            <span class="cohort-stat__value">{{ clearedCount }}</span>
            <span class="cohort-stat__label">Cleared</span>
          </div>
          <div class="cohort-stat cohort-stat--rejected">
            <span class="cohort-stat__value">{{ rejectedCount }}</span>
            <span class="cohort-stat__label">Rejected</span>
          </div>
          <div class="cohort-stat cohort-stat--pending">
            <span class="cohort-stat__value">{{ pendingCount }}</span>
            <span class="cohort-stat__label">Pending</span>
          </div>
        </div>
        <div class="cohort-actions">
          <button
            v-if="!isPipelineComplete"
            class="btn btn-finalize"
            :disabled="pendingCount > 0 || activeApps.length === 0 || isAdvancing"
            @click="handleFinalize"
            id="btn-finalize-round"
            :title="pendingCount > 0 ? `${pendingCount} candidate(s) still pending evaluation` : 'Finalize this round'"
          >
            <template v-if="isAdvancing">
              <AppSpinner size="sm" /> Advancing...
            </template>
            <template v-else>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
              Finalize Round
            </template>
          </button>
          <div v-else class="status-badge status-hired">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
            Pipeline Complete
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="loading-placeholder card animate-fade-in">
        <AppSpinner size="md" />
        <p>Loading applications...</p>
      </div>

      <!-- Applications Table -->
      <div v-else-if="activeApps.length > 0" class="apps-table-card card card--no-hover animate-fade-in-up" style="animation-delay:0.1s">
        <!-- Desktop Table -->
        <div class="table-container hide-mobile">
          <table class="apps-table" id="applications-table">
            <thead>
              <tr>
                <th width="70">Rank</th>
                <th>Candidate</th>
                <th>Matched Skills</th>
                <th style="white-space: nowrap; width: 180px;">ATS SCORE OUT OF 100</th>
                <th style="padding-left: 1.5rem;">Evaluation</th>
                <th width="100">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(app, i) in activeApps" :key="app.id" class="app-row" :id="`app-row-${app.id}`">
                <td>
                  <div class="rank-box" :class="{ 'top-rank': i < 3 }">
                    <span v-if="i === 0">🥇</span>
                    <span v-else-if="i === 1">🥈</span>
                    <span v-else-if="i === 2">🥉</span>
                    <span v-else>{{ i + 1 }}</span>
                  </div>
                </td>
                <td>
                  <div class="profile-cell">
                    <div class="profile-avatar" :style="`background: ${app._avatarGrad}`">{{ app._initials }}</div>
                    <div class="profile-info">
                      <span class="profile-name">{{ app.candidate_name || app.candidate_email }}</span>
                      <span class="profile-email">{{ app.candidate_email }}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <div class="skill-stack">
                    <span v-for="skill in (app.matched_skills || []).slice(0,3)" :key="skill" class="v-tag">{{ skill }}</span>
                    <span v-if="(app.matched_skills || []).length > 3" class="v-tag more">+{{ app.matched_skills.length - 3 }}</span>
                    <span v-if="!app.matched_skills || app.matched_skills.length === 0" class="v-tag dim">No data</span>
                  </div>
                </td>
                <td>
                  <div class="score-display">
                    <ScoreRing :score="app.ats_score || 0" :size="90" />
                  </div>
                </td>
                <!-- Tri-State Evaluation Toggle -->
                <td style="padding-left: 1.5rem;">
                  <div class="eval-toggle" :id="`eval-toggle-${app.id}`" v-if="!isPipelineComplete">
                    <button
                      class="eval-btn eval-btn--cleared"
                      :class="{ active: app.round_status === 'Cleared' }"
                      @click="setRoundStatus(app, 'Cleared')"
                      title="Clear candidate"
                    >
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                      Cleared
                    </button>
                    <button
                      class="eval-btn eval-btn--pending"
                      :class="{ active: app.round_status === 'Pending' }"
                      @click="setRoundStatus(app, 'Pending')"
                      title="Reset to pending"
                    >
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                      Pending
                    </button>
                    <button
                      class="eval-btn eval-btn--reject"
                      :class="{ active: app.round_status === 'Reject' }"
                      @click="setRoundStatus(app, 'Reject')"
                      title="Reject candidate"
                    >
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                      Reject
                    </button>
                  </div>
                  <span v-else class="status-badge status-hired">Hired</span>
                </td>
                <td>
                  <div class="action-group">
                    <button class="action-btn details" @click="selectedApp = app" title="View Details">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                      <span>Details</span>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Mobile Cards -->
        <div class="show-mobile apps-cards-mobile">
          <div v-for="(app, i) in activeApps" :key="app.id" class="app-card-mobile">
            <!-- Row 1: Rank + Profile + Score -->
            <div class="app-card-mobile__header">
              <div class="rank-box" :class="{ 'top-rank': i < 3 }">
                <span v-if="i === 0">🥇</span>
                <span v-else-if="i === 1">🥈</span>
                <span v-else-if="i === 2">🥉</span>
                <span v-else>{{ i + 1 }}</span>
              </div>
              <div class="profile-cell">
                <div class="profile-avatar" :style="`background: ${app._avatarGrad}`">{{ app._initials }}</div>
                <div class="profile-info">
                  <span class="profile-name">{{ app.candidate_name || app.candidate_email }}</span>
                  <span class="profile-email">{{ app.candidate_email }}</span>
                </div>
              </div>
              <div class="score-display">
                <ScoreRing :score="app.ats_score || 0" :size="48" />
              </div>
            </div>

            <!-- Row 2: Skills -->
            <div class="skill-stack mt-2">
              <span v-for="skill in (app.matched_skills || []).slice(0,3)" :key="skill" class="v-tag">{{ skill }}</span>
              <span v-if="(app.matched_skills || []).length > 3" class="v-tag more">+{{ app.matched_skills.length - 3 }}</span>
            </div>

            <!-- Row 3: Evaluation -->
            <div class="eval-toggle w-full mt-2" v-if="!isPipelineComplete">
              <button
                class="eval-btn eval-btn--cleared flex-1"
                :class="{ active: app.round_status === 'Cleared' }"
                @click="setRoundStatus(app, 'Cleared')"
              >Cleared</button>
              <button
                class="eval-btn eval-btn--pending flex-1"
                :class="{ active: app.round_status === 'Pending' }"
                @click="setRoundStatus(app, 'Pending')"
              >Pending</button>
              <button
                class="eval-btn eval-btn--reject flex-1"
                :class="{ active: app.round_status === 'Reject' }"
                @click="setRoundStatus(app, 'Reject')"
              >Reject</button>
            </div>

            <!-- Row 4: Actions -->
            <button class="action-btn details w-full justify-center mt-2" @click="selectedApp = app">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
              <span>View Full Profile</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Rejected Candidates (Collapsed) -->
      <details v-if="rejectedApps.length > 0" class="rejected-section animate-fade-in-up" style="animation-delay:0.15s">
        <summary class="rejected-summary card card--no-hover">
          <span>{{ rejectedApps.length }} rejected candidate{{ rejectedApps.length !== 1 ? 's' : '' }} from previous rounds</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </summary>
        <div class="rejected-list">
          <div v-for="app in rejectedApps" :key="app.id" class="rejected-card card card--no-hover">
            <div class="profile-cell">
              <div class="profile-avatar" :style="`background: ${app._avatarGrad}`">{{ app._initials }}</div>
              <div class="profile-info">
                <span class="profile-name">{{ app.candidate_name || app.candidate_email }}</span>
                <span class="profile-email">Rejected in Round {{ (app.terminal_round_index ?? 0) + 1 }}: {{ rounds[app.terminal_round_index] || '—' }}</span>
              </div>
            </div>
            <span class="status-badge status-rejected">Rejected</span>
          </div>
        </div>
      </details>

      <!-- Empty State -->
      <AppEmptyState
        v-if="!isLoading && activeApps.length === 0 && rejectedApps.length === 0"
        icon="📭"
        title="No applications yet"
        description="Candidates haven't applied for this job yet. Share the posting to attract talent!"
      />
    </div>

    <!-- ───── Candidate Detail Modal ───── -->
    <AppModal :show="!!selectedApp" @close="selectedApp = null">
      <div class="v-modal-header">
              <div class="v-modal-avatar" :style="`background: ${selectedApp._avatarGrad}`">
                {{ selectedApp._initials }}
              </div>
              <div class="v-modal-title-area">
                <h2 class="v-modal-name">{{ selectedApp.candidate_name || selectedApp.candidate_email }}</h2>
                <div class="v-modal-meta">
                  <span>{{ selectedApp.candidate_email }}</span>
                  <span class="dot-sep"></span>
                  <span class="eval-badge" :class="`eval-badge--${(selectedApp.round_status || 'Pending').toLowerCase()}`">{{ selectedApp.round_status || 'Pending' }}</span>
                </div>
              </div>
            </div>

          <div class="v-modal-contact-actions">
            <a target="_blank" rel="noopener noreferrer" :href="generateGmailLink(selectedApp)" class="btn btn-outline btn-sm">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
              Email Candidate
            </a>
            <a v-if="selectedApp.parsedResume?.phone" :href="`tel:${selectedApp.parsedResume.phone}`" class="btn btn-outline btn-sm">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
              Call Candidate
            </a>
          </div>

          <!-- ATS Score Section -->
          <div class="v-modal-section">
            <h4 class="section-label">ATS Analysis</h4>
            <AtsScorePanel
              :score="selectedApp.ats_score || 0"
              :breakdown="selectedApp.score_breakdown"
              :matchedSkills="selectedApp.matched_skills"
              :missingSkills="selectedApp.missing_skills"
            />
          </div>

          <!-- Parsed Resume Section -->
          <div v-if="selectedApp.parsedResume" class="v-modal-section">
            <ParsedResumeDisplay :parsedResume="selectedApp.parsedResume" />
          </div>
          <div v-else class="v-modal-section">
            <h4 class="section-label">Parsed Resume</h4>
            <p class="text-muted">No parsed resume data available for this candidate.</p>
          </div>

          <div class="v-modal-footer">
            <button class="btn btn-outline" @click="selectedApp = null">Close</button>
            <template v-if="!isPipelineComplete">
              <button
                v-if="selectedApp.round_status !== 'Cleared'"
                class="btn btn-cleared"
                @click="setRoundStatus(selectedApp, 'Cleared'); selectedApp = null"
              >Clear</button>
              <button
                v-if="selectedApp.round_status !== 'Reject'"
                class="btn btn-reject"
                @click="setRoundStatus(selectedApp, 'Reject'); selectedApp = null"
              >Reject</button>
            </template>
          </div>
    </AppModal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppModal from '@/components/AppModal.vue'
import { useRoute } from 'vue-router'
import { avatarGrad, initials } from '@/utils/uiHelpers'
import AppSpinner from '@/components/AppSpinner.vue'
import AppEmptyState from '@/components/AppEmptyState.vue'
import AtsScorePanel from '@/components/AtsScorePanel.vue'
import PageHeader from '@/components/PageHeader.vue'
import ScoreRing from '@/components/ScoreRing.vue'
import ParsedResumeDisplay from '@/components/ParsedResumeDisplay.vue'
import { getJobApplications, updateRoundStatus as updateRoundStatusApi, advanceRound as advanceRoundApi } from '@/utils/api'

const route = useRoute()
const jobId = route.params.jobId

const jobTitle = ref('Loading...')
const applications = ref([])
const rounds = ref([])
const currentRoundIndex = ref(0)
const isLoading = ref(true)
const isAdvancing = ref(false)
const selectedApp = ref(null)

// ── Computed: filter active vs rejected ────────────────────────
const activeApps = computed(() =>
  applications.value.filter(a => a.terminal_round_index == null)
)

const rejectedApps = computed(() =>
  applications.value.filter(a => a.terminal_round_index != null)
)

const clearedCount = computed(() => activeApps.value.filter(a => a.round_status === 'Cleared').length)
const rejectedCount = computed(() => activeApps.value.filter(a => a.round_status === 'Reject').length)
const pendingCount = computed(() => activeApps.value.filter(a => !a.round_status || a.round_status === 'Pending').length)

const isPipelineComplete = computed(() => rounds.value.length > 0 && currentRoundIndex.value >= rounds.value.length)

// ── Fetch ──────────────────────────────────────────────────────
async function fetchApplications() {
  isLoading.value = true
  try {
    const data = await getJobApplications(jobId)
    jobTitle.value = data.job_title
    rounds.value = data.rounds || []
    currentRoundIndex.value = data.current_round_index || 0
    applications.value = data.applications.map(app => ({
      ...app,
      round_status: app.round_status || 'Pending',
      _avatarGrad: avatarGrad(app.candidate_email),
      _initials: initials(app.candidate_name || app.candidate_email)
    }))
  } catch (err) {
    console.error('Fetch applications error:', err)
  } finally {
    isLoading.value = false
  }
}

// ── Tri-state evaluation ───────────────────────────────────────
async function setRoundStatus(app, newStatus) {
  const prev = app.round_status
  app.round_status = newStatus // optimistic
  try {
    await updateRoundStatusApi(jobId, app.id, newStatus)
  } catch (err) {
    console.error('Update round status error:', err)
    app.round_status = prev // rollback
  }
}

// ── Finalize round (calls advancement engine) ─────────────────
async function handleFinalize() {
  const nextRound = rounds.value[currentRoundIndex.value + 1] || 'Next Round'
  const msg = `Finalize this round?\n\n✅ ${clearedCount.value} candidate(s) will advance to "${nextRound}"\n❌ ${rejectedCount.value} candidate(s) will be permanently rejected\n\nThis action cannot be undone.`
  if (!confirm(msg)) return

  isAdvancing.value = true
  try {
    await advanceRoundApi(jobId, currentRoundIndex.value)
    await fetchApplications()
  } catch (err) {
    console.error('Advance round error:', err)
    alert('Failed to advance round: ' + (err.message || 'Unknown error'))
  } finally {
    isAdvancing.value = false
  }
}

function generateGmailLink(app) {
  if (!app) return '#'
  const candidateName = app.candidate_name || 'Candidate'
  const subject = `Regarding your application for ${jobTitle.value}`
  const body = `Hi ${candidateName},\n\nThank you for applying for the ${jobTitle.value} position. We have reviewed your application and would love to schedule a time to speak with you!\n\nPlease let me know what times work best for you this week.\n\nBest regards,`

  return `https://mail.google.com/mail/?view=cm&fs=1&to=${encodeURIComponent(app.candidate_email)}&su=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`
}

onMounted(fetchApplications)
</script>

<style scoped>
/* ═══ Round Stepper ═════════════════════════════════════════════ */
.round-stepper {
  margin-bottom: var(--sp-4);
  padding: 1.25rem 1.5rem;
  overflow-x: auto;
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
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
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

.stepper-connector {
  position: absolute;
  top: 15px;
  left: calc(50% + 18px);
  width: calc(100% - 36px);
  height: 2px;
  background: var(--clr-border);
}
.stepper-connector--done { background: #10b981; }

/* ═══ Cohort Bar ════════════════════════════════════════════════ */
.cohort-bar {
  margin-bottom: var(--sp-4);
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.cohort-stats {
  display: flex;
  gap: 2rem;
}

.cohort-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.cohort-stat__value {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--clr-text);
  line-height: 1;
}

.cohort-stat__label {
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--clr-text-muted);
  margin-top: 0.2rem;
}

.cohort-stat--cleared .cohort-stat__value { color: #10b981; }
.cohort-stat--rejected .cohort-stat__value { color: #ef4444; }
.cohort-stat--pending .cohort-stat__value { color: #f59e0b; }

.btn-finalize {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 1.5rem;
  border-radius: var(--radius-full);
  border: 1px solid var(--clr-primary);
  background: var(--clr-primary);
  color: white;
  font-weight: 700;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-finalize:hover:not(:disabled) {
  background: var(--clr-primary-hover, #5b5bd6);
  box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
}
.btn-finalize:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  background: var(--clr-surface-2);
  border-color: var(--clr-border);
  color: var(--clr-text-muted);
}

/* ═══ Evaluation Toggle ═════════════════════════════════════════ */
.eval-toggle {
  display: inline-flex;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--clr-border);
  background: var(--clr-surface-2);
}

.eval-btn {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.35rem 0.65rem;
  border: none;
  background: transparent;
  color: var(--clr-text-muted);
  font-size: 0.72rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}
.eval-btn:not(:last-child) { border-right: 1px solid var(--clr-border); }

.eval-btn--cleared.active { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.eval-btn--pending.active { background: rgba(245, 158, 11, 0.12); color: #f59e0b; }
.eval-btn--reject.active { background: rgba(239, 68, 68, 0.12); color: #ef4444; }

.eval-btn:hover:not(.active) { background: var(--clr-surface); }

/* Eval badge in modal */
.eval-badge {
  padding: 0.2rem 0.65rem;
  border-radius: 99px;
  font-size: 0.75rem;
  font-weight: 700;
}
.eval-badge--cleared { background: rgba(16, 185, 129, 0.12); color: #10b981; }
.eval-badge--pending { background: rgba(245, 158, 11, 0.1); color: #f59e0b; }
.eval-badge--reject { background: rgba(239, 68, 68, 0.1); color: #ef4444; }

/* ═══ Table ══════════════════════════════════════════════════ */
.apps-table-card {
  padding: 0;
  overflow: hidden;
  border: 1px solid var(--clr-border);
}

.table-container { overflow-x: auto; }

.apps-table { width: 100%; border-collapse: collapse; }

.apps-table thead th {
  background: var(--clr-surface-2);
  padding: 1.25rem 1.5rem;
  text-align: left;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--clr-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  border-bottom: 1px solid var(--clr-border);
}

.app-row td {
  padding: 1.15rem 1.5rem;
  vertical-align: middle;
  background: var(--clr-surface);
}
.app-row:not(:last-child) td { border-bottom: 1px solid var(--clr-border); }
.app-row:hover td { background: var(--clr-surface-2); }

/* Rank */
.rank-box {
  width: 36px;
  height: 36px;
  background: var(--clr-surface-2);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  color: var(--clr-text-muted);
  font-size: 0.9rem;
}
.top-rank {
  background: var(--gradient-brand);
  color: white;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
}

/* Profile */
.profile-cell { display: flex; align-items: center; gap: var(--sp-3); }
.profile-avatar {
  width: 40px; height: 40px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; color: white; font-size: 0.9rem; flex-shrink: 0;
}
.profile-info { display: flex; flex-direction: column; }
.profile-name { font-weight: 700; color: var(--clr-text); font-size: 0.95rem; }
.profile-email { font-size: 0.78rem; color: var(--clr-text-muted); }

/* Skills */
.skill-stack { display: flex; flex-wrap: wrap; gap: 0.35rem; }
.v-tag {
  background: var(--clr-surface-2);
  color: var(--clr-text-muted);
  padding: 0.2rem 0.6rem;
  border-radius: 6px;
  font-size: 0.72rem;
  font-weight: 600;
  border: 1px solid var(--clr-border);
}
.v-tag.more { color: var(--clr-primary); border-color: var(--clr-primary); opacity: 0.7; }
.v-tag.dim { opacity: 0.5; font-style: italic; }

/* Action Buttons */
.action-group { display: flex; align-items: center; gap: 0.4rem; justify-content: flex-end; }
.action-btn {
  display: flex; align-items: center; gap: 0.35rem;
  padding: 0.4rem 0.65rem;
  border-radius: 8px;
  border: 1px solid var(--clr-border);
  background: transparent;
  color: var(--clr-text-muted);
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.action-btn.details:hover { background: var(--clr-primary); color: white; border-color: var(--clr-primary); }

/* ═══ Rejected Section ═══════════════════════════════════════ */
.rejected-section { margin-top: var(--sp-4); }

.rejected-summary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.85rem 1.25rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--clr-text-muted);
  cursor: pointer;
  list-style: none;
  user-select: none;
}
.rejected-summary::-webkit-details-marker { display: none; }
.rejected-summary svg { transition: transform 0.2s; }
details[open] .rejected-summary svg { transform: rotate(180deg); }

.rejected-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.rejected-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.25rem;
  opacity: 0.6;
}

.status-rejected {
  padding: 0.2rem 0.65rem;
  border-radius: 99px;
  font-size: 0.72rem;
  font-weight: 700;
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.status-hired {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem 1rem;
  border-radius: 99px;
  font-size: 0.85rem;
  font-weight: 700;
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

/* ═══ Modal ══════════════════════════════════════════════════ */
.v-modal-header { display: flex; gap: var(--sp-4); margin-bottom: var(--sp-6); }
.v-modal-avatar {
  width: 64px; height: 64px; border-radius: 16px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.3rem; font-weight: 800; color: white;
  box-shadow: 0 8px 16px -4px rgba(0,0,0,0.1);
  flex-shrink: 0;
}
.v-modal-title-area { flex: 1; }
.v-modal-name { font-size: 1.5rem; font-weight: 800; margin-bottom: 0.25rem; }
.v-modal-meta { display: flex; align-items: center; gap: 0.75rem; color: var(--clr-text-muted); font-weight: 500; font-size: 0.9rem; flex-wrap: wrap; }
.dot-sep { width: 4px; height: 4px; background: var(--clr-border); border-radius: 50%; }
.v-modal-contact-actions { display: flex; gap: 0.5rem; margin-bottom: var(--sp-6); }
.section-label { font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; color: var(--clr-text-muted); margin-bottom: 0.75rem; }
.v-modal-section { margin-bottom: var(--sp-6); }

.v-modal-footer {
  margin-top: 1.5rem; display: flex; justify-content: flex-end; gap: 0.75rem;
}

/* Modal action buttons */
.btn-sm { padding: 0.4rem 0.9rem; font-size: 0.8rem; }

.btn-cleared {
  background: rgba(16, 185, 129, 0.12);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.25);
  font-weight: 600;
  display: inline-flex; align-items: center; gap: 0.35rem;
  padding: 0.4rem 0.9rem; border-radius: var(--radius-full);
  cursor: pointer; transition: all 0.2s;
}
.btn-cleared:hover { background: #10b981; color: white; }

.btn-reject {
  background: rgba(239, 68, 68, 0.12);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.25);
  font-weight: 600;
  display: inline-flex; align-items: center; gap: 0.35rem;
  padding: 0.4rem 0.9rem; border-radius: var(--radius-full);
  cursor: pointer; transition: all 0.2s;
}
.btn-reject:hover { background: #ef4444; color: white; }

/* ═══ Responsive ═════════════════════════════════════════════ */
@media (max-width: 1024px) {
  .cohort-bar { flex-direction: column; align-items: stretch; }
  .cohort-stats { justify-content: space-around; }
}

@media (max-width: 768px) {
  .v-modal-header { flex-direction: column; gap: var(--sp-3); }
  .stepper-step { min-width: 70px; }
  .eval-toggle { flex-direction: column; }
  .eval-btn { justify-content: center; }
  .eval-btn:not(:last-child) { border-right: none; border-bottom: 1px solid var(--clr-border); }

  .apps-cards-mobile {
    display: flex;
    flex-direction: column;
    padding: var(--sp-3);
  }

  .app-card-mobile {
    background: var(--clr-surface);
    border: 1px solid var(--clr-border);
    border-radius: var(--radius-md);
    padding: var(--sp-4);
    margin-bottom: var(--sp-3);
    display: flex;
    flex-direction: column;
    gap: var(--sp-2);
  }

  .app-card-mobile__header {
    display: flex;
    align-items: center;
    gap: var(--sp-3);
    border-bottom: 1px solid var(--clr-surface-2);
    padding-bottom: var(--sp-3);
    margin-bottom: var(--sp-1);
  }

  .app-card-mobile__header .profile-cell {
    flex: 1;
  }

  /* Evaluation buttons side-by-side on mobile card */
  .app-card-mobile .eval-toggle {
    flex-direction: row;
    width: 100%;
    margin-top: 0.5rem;
  }
  
  .app-card-mobile .eval-btn {
    flex: 1;
    border-bottom: none;
    border-right: 1px solid var(--clr-border);
  }
  
  .app-card-mobile .eval-btn:last-child {
    border-right: none;
  }
}
</style>

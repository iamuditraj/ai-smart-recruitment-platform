<template>
  <div class="job-apps">
    <div class="content-area">
      <!-- Back link + Header -->
      <PageHeader
        :title="jobTitle"
        :subtitle="`${applications.length} applicant${applications.length !== 1 ? 's' : ''} for this position`"
        backTo="/manage-jobs"
        backLabel="Back to Jobs"
      />

      <!-- Bulk Actions Toolbar -->
      <div class="bulk-toolbar card card--no-hover animate-fade-in-up" style="animation-delay:0.05s" id="bulk-actions">
        <div class="bulk-toolbar__section">
          <span class="bulk-label">Bulk Actions</span>
          <div class="bulk-action-group">
            <span class="bulk-action-text">Approve all with score ≥</span>
            <input v-model.number="approveThreshold" type="number" min="0" max="100" class="bulk-input" id="approve-threshold" />
            <button class="btn btn-approve btn-sm" @click="bulkAction('approve', approveThreshold, 'above')" id="btn-bulk-approve">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>
              Approve
            </button>
          </div>
          <div class="bulk-action-group">
            <span class="bulk-action-text">Reject all with score &lt;</span>
            <input v-model.number="rejectThreshold" type="number" min="0" max="100" class="bulk-input" id="reject-threshold" />
            <button class="btn btn-reject btn-sm" @click="bulkAction('reject', rejectThreshold, 'below')" id="btn-bulk-reject">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
              Reject
            </button>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="loading-placeholder card animate-fade-in">
        <AppSpinner size="md" />
        <p>Loading applications...</p>
      </div>

      <!-- Applications Table -->
      <div v-else-if="applications.length > 0" class="apps-table-card card card--no-hover animate-fade-in-up" style="animation-delay:0.1s">
        <div class="table-container">
          <table class="apps-table" id="applications-table">
            <thead>
              <tr>
                <th width="70">Rank</th>
                <th>Candidate</th>
                <th>Matched Skills</th>
                <th style="white-space: nowrap; width: 180px;">ATS SCORE OUT OF 100</th>
                <th style="padding-left: 1.5rem;">Status</th>
                <th width="200">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(app, i) in applications" :key="app.id" class="app-row" :id="`app-row-${app.id}`">
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
                <td style="padding-left: 1.5rem;">
                  <span class="status-badge" :class="getStatusClass(app.status)">{{ app.status }}</span>
                </td>
                <td>
                  <div class="action-group">
                    <button v-if="app.status !== 'Shortlisted'" class="action-btn approve" @click="updateStatus(app, 'Shortlisted')" title="Approve">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>
                    </button>
                    <button v-if="app.status !== 'Rejected'" class="action-btn reject" @click="updateStatus(app, 'Rejected')" title="Reject">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                    </button>
                    <button class="action-btn details" @click="selectedApp = app" title="View Details">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                      <span>Details</span>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Empty State -->
      <AppEmptyState
        v-else
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
                  <span class="status-badge" :class="getStatusClass(selectedApp.status)">{{ selectedApp.status }}</span>
                </div>
              </div>
            </div>

          <div class="v-modal-contact-actions">
            <a target="_blank" rel="noopener noreferrer" :href="generateGmailLink(selectedApp)" class="btn btn-outline btn-sm">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
              Email Candidate
            </a>
            <a v-if="selectedApp.parsedResume?.phone" :href="`tel:${selectedApp.parsedResume.phone}`" class="btn btn-outline btn-sm">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
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
            <button v-if="selectedApp.status !== 'Shortlisted'" class="btn btn-approve" @click="updateStatus(selectedApp, 'Shortlisted'); selectedApp = null">Approve</button>
            <button v-if="selectedApp.status !== 'Rejected'" class="btn btn-reject" @click="updateStatus(selectedApp, 'Rejected'); selectedApp = null">Reject</button>
          </div>
    </AppModal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppModal from '@/components/AppModal.vue'
import { useRoute } from 'vue-router'
import { avatarGrad, initials, getStatusClass } from '@/utils/uiHelpers'
import AppSpinner from '@/components/AppSpinner.vue'
import AppAlert from '@/components/AppAlert.vue'
import AppEmptyState from '@/components/AppEmptyState.vue'
import AtsScorePanel from '@/components/AtsScorePanel.vue'
import PageHeader from '@/components/PageHeader.vue'
import ScoreRing from '@/components/ScoreRing.vue'
import ParsedResumeDisplay from '@/components/ParsedResumeDisplay.vue'
import { getJobApplications, updateApplicationStatus as updateApplicationStatusApi, bulkUpdateStatus as bulkUpdateStatusApi } from '@/utils/api'

const route = useRoute()
const jobId = route.params.jobId

const jobTitle = ref('Loading...')
const applications = ref([])
const isLoading = ref(true)
const selectedApp = ref(null)
const approveThreshold = ref(80)
const rejectThreshold = ref(60)



async function fetchApplications() {
  isLoading.value = true
  try {
    const data = await getJobApplications(jobId)
    jobTitle.value = data.job_title
    applications.value = data.applications.map(app => ({
      ...app,
      _avatarGrad: avatarGrad(app.candidate_email),
      _initials: initials(app.candidate_name || app.candidate_email)
    }))
  } catch (err) {
    console.error('Fetch applications error:', err)
  } finally {
    isLoading.value = false
  }
}

async function updateStatus(app, newStatus) {
  try {
    await updateApplicationStatusApi(jobId, app.id, newStatus)
    app.status = newStatus
  } catch (err) {
    console.error('Update status error:', err)
  }
}

async function bulkAction(action, threshold, direction) {
  if (!threshold && threshold !== 0) return
  try {
    const data = await bulkUpdateStatusApi(jobId, action, threshold, direction)
    await fetchApplications()
    alert(`${data.updated_count} application(s) updated.`)
  } catch (err) {
    console.error('Bulk action error:', err)
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
/* ═══ Bulk Toolbar ═══════════════════════════════════════════ */
.bulk-toolbar {
  margin-bottom: var(--sp-4);
  padding: var(--sp-4) var(--sp-6);
}

.bulk-toolbar__section {
  display: flex;
  align-items: center;
  gap: var(--sp-6);
  flex-wrap: wrap;
}

.bulk-label {
  font-weight: 700;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--clr-text-muted);
}

.bulk-action-group {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
}

.bulk-action-text {
  font-size: 0.85rem;
  color: var(--clr-text-muted);
  font-weight: 500;
}

.bulk-input {
  width: 64px;
  height: 36px;
  text-align: center;
  border-radius: var(--radius-sm);
  border: 1px solid var(--clr-border);
  background: var(--clr-surface-2);
  color: var(--clr-text);
  font-size: 0.9rem;
  font-weight: 700;
  outline: none;
  transition: border-color 0.2s;
}
.bulk-input:focus { border-color: var(--clr-primary); }

/* ═══ Buttons ════════════════════════════════════════════════ */
.btn-sm { padding: 0.4rem 0.9rem; font-size: 0.8rem; }

.btn-approve {
  background: rgba(16, 185, 129, 0.12);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.25);
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.4rem 0.9rem;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all 0.2s;
}
.btn-approve:hover { background: #10b981; color: white; }

.btn-reject {
  background: rgba(239, 68, 68, 0.12);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.25);
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.4rem 0.9rem;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all 0.2s;
}
.btn-reject:hover { background: #ef4444; color: white; }

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
.v-tag.gap-tag { color: #ef4444; border-color: rgba(239, 68, 68, 0.3); background: rgba(239, 68, 68, 0.08); }

/* Status */
.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 99px;
  font-size: 0.75rem;
  font-weight: 700;
  white-space: nowrap;
}

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
.action-btn.approve:hover { background: #10b981; color: white; border-color: #10b981; }
.action-btn.reject:hover { background: #ef4444; color: white; border-color: #ef4444; }
.action-btn.details:hover { background: var(--clr-primary); color: white; border-color: var(--clr-primary); }

/* ═══ Loading & Empty ════════════════════════════════════════ */





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

/* Analysis Box */


/* Footer */
.v-modal-footer {
  margin-top: 1.5rem; display: flex; justify-content: flex-end; gap: 0.75rem;
}

/* Responsive ═════════════════════════════════════════════ */
@media (max-width: 1024px) {
  .bulk-toolbar__section { flex-direction: column; align-items: flex-start; gap: var(--sp-3); }
}

@media (max-width: 768px) {
  .page-title { font-size: 1.5rem; }
  .v-modal-header { flex-direction: column; gap: var(--sp-3); }
  .analysis-box { flex-direction: column; }
  .analysis-score { border-right: none; border-bottom: 1px solid var(--clr-border); padding-right: 0; padding-bottom: 1rem; }
  .parsed-resume-card { grid-template-columns: 1fr; }
}
</style>



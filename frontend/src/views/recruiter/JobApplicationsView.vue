<template>
  <div class="job-apps section">
    <div class="container--fluid">
      <!-- Back link + Header -->
      <div class="page-header animate-fade-in-up">
        <div>
          <router-link to="/manage-jobs" class="back-link" id="back-to-jobs">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg>
            Back to Jobs
          </router-link>
          <h1 class="page-title">{{ jobTitle }}</h1>
          <p class="page-subtitle">{{ applications.length }} applicant{{ applications.length !== 1 ? 's' : '' }} for this position</p>
        </div>
      </div>

      <!-- Bulk Actions Toolbar -->
      <div class="bulk-toolbar card animate-fade-in-up" style="animation-delay:0.05s" id="bulk-actions">
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
        <div class="spinner"></div>
        <p>Loading applications...</p>
      </div>

      <!-- Applications Table -->
      <div v-else-if="applications.length > 0" class="apps-table-card card animate-fade-in-up" style="animation-delay:0.1s">
        <div class="table-container">
          <table class="apps-table" id="applications-table">
            <thead>
              <tr>
                <th width="70">Rank</th>
                <th>Candidate</th>
                <th>Matched Skills</th>
                <th width="100">ATS Score</th>
                <th>Status</th>
                <th width="240">Actions</th>
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
                    <div class="score-radial">
                       <svg viewBox="0 0 36 36" class="circular-chart">
                         <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                         <path class="circle" :class="scoreColorClass(app.ats_score)" :style="`stroke-dasharray: ${app.ats_score || 0}, 100`" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                       </svg>
                       <span class="score-val">{{ app.ats_score || 0 }}%</span>
                    </div>
                  </div>
                </td>
                <td>
                  <span class="status-badge" :class="statusClass(app.status)">{{ app.status }}</span>
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
      <div v-else class="empty-placeholder card animate-fade-in">
        <div class="empty-icon">📭</div>
        <h3>No applications yet</h3>
        <p>Candidates haven't applied for this job yet. Share the posting to attract talent!</p>
      </div>
    </div>

    <!-- ───── Candidate Detail Modal ───── -->
    <Transition name="v-modal">
      <div v-if="selectedApp" class="v-modal-overlay" @click.self="selectedApp = null">
        <div class="v-modal-card card">
          <button class="v-modal-close" @click="selectedApp = null">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>

          <div class="v-modal-header">
            <div class="v-modal-avatar" :style="`background: ${selectedApp._avatarGrad}`">
              {{ selectedApp._initials }}
            </div>
            <div class="v-modal-title-area">
              <h2 class="v-modal-name">{{ selectedApp.candidate_name || selectedApp.candidate_email }}</h2>
              <div class="v-modal-meta">
                <span>{{ selectedApp.candidate_email }}</span>
                <span class="dot-sep"></span>
                <span class="status-badge" :class="statusClass(selectedApp.status)">{{ selectedApp.status }}</span>
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
            <div class="analysis-box">
              <div class="analysis-score">
                <span class="score-big">{{ selectedApp.ats_score || 0 }}%</span>
                <span class="score-small">Match Score</span>
              </div>
              <div class="analysis-details">
                <div v-if="selectedApp.matched_skills && selectedApp.matched_skills.length" class="detail-row">
                  <strong>Matched Skills:</strong>
                  <div class="skill-stack modal-skills">
                    <span v-for="skill in selectedApp.matched_skills" :key="skill" class="v-tag">{{ skill }}</span>
                  </div>
                </div>
                <div v-if="selectedApp.missing_skills && selectedApp.missing_skills.length" class="detail-row gap-row">
                  <strong>Missing Skills:</strong>
                  <div class="skill-stack modal-skills">
                    <span v-for="skill in selectedApp.missing_skills" :key="skill" class="v-tag gap-tag">{{ skill }}</span>
                  </div>
                </div>
                <div v-if="selectedApp.score_breakdown" class="detail-row">
                  <strong>Score Breakdown:</strong>
                  <div class="breakdown-grid">
                    <div v-for="(val, key) in selectedApp.score_breakdown" :key="key" class="breakdown-item">
                      <span class="breakdown-label">{{ formatBreakdownKey(key) }}</span>
                      <div class="breakdown-bar-wrap">
                        <div class="breakdown-bar" :style="`width: ${Math.min(val, 100)}%`"></div>
                      </div>
                      <span class="breakdown-val">{{ val }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Parsed Resume Section -->
          <div v-if="selectedApp.parsedResume" class="v-modal-section">
            <h4 class="section-label">Parsed Resume</h4>
            <div class="parsed-resume-card">
              <div v-if="selectedApp.parsedResume.name" class="resume-field">
                <span class="field-label">Name</span>
                <span class="field-value">{{ selectedApp.parsedResume.name }}</span>
              </div>
              <div v-if="selectedApp.parsedResume.email" class="resume-field">
                <span class="field-label">Email</span>
                <span class="field-value">{{ selectedApp.parsedResume.email }}</span>
              </div>
              <div v-if="selectedApp.parsedResume.phone" class="resume-field">
                <span class="field-label">Phone</span>
                <span class="field-value">{{ selectedApp.parsedResume.phone }}</span>
              </div>
              <div v-if="selectedApp.parsedResume.summary" class="resume-field full">
                <span class="field-label">Summary</span>
                <span class="field-value">{{ selectedApp.parsedResume.summary }}</span>
              </div>
              <div v-if="selectedApp.parsedResume.skills && selectedApp.parsedResume.skills.length" class="resume-field full">
                <span class="field-label">Skills</span>
                <div class="skill-stack modal-skills">
                  <span v-for="s in selectedApp.parsedResume.skills" :key="s" class="v-tag">{{ s }}</span>
                </div>
              </div>
              <div v-if="selectedApp.parsedResume.experience && selectedApp.parsedResume.experience.length" class="resume-field full">
                <span class="field-label">Experience</span>
                <div class="exp-list">
                  <div v-for="(exp, ei) in selectedApp.parsedResume.experience" :key="ei" class="exp-item">
                    <div class="exp-header">
                      <strong>{{ exp.title }}</strong>
                      <span v-if="exp.company"> — {{ exp.company }}</span>
                    </div>
                    <span v-if="exp.duration" class="exp-duration">{{ exp.duration }}</span>
                    <p v-if="exp.description" class="exp-desc">{{ exp.description }}</p>
                  </div>
                </div>
              </div>
              <div v-if="selectedApp.parsedResume.education && selectedApp.parsedResume.education.length" class="resume-field full">
                <span class="field-label">Education</span>
                <div class="exp-list">
                  <div v-for="(edu, ei) in selectedApp.parsedResume.education" :key="ei" class="exp-item">
                    <strong>{{ edu.degree }}</strong>
                    <span v-if="edu.institution"> — {{ edu.institution }}</span>
                    <span v-if="edu.year" class="exp-duration">{{ edu.year }}</span>
                  </div>
                </div>
              </div>
              <div v-if="selectedApp.parsedResume.certifications && selectedApp.parsedResume.certifications.length" class="resume-field full">
                <span class="field-label">Certifications</span>
                <div class="skill-stack modal-skills">
                  <span v-for="c in selectedApp.parsedResume.certifications" :key="c" class="v-tag">{{ c }}</span>
                </div>
              </div>
            </div>
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
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const jobId = route.params.jobId
const API = import.meta.env.VITE_API_URL || 'http://localhost:5001'

const jobTitle = ref('Loading...')
const applications = ref([])
const isLoading = ref(true)
const selectedApp = ref(null)
const approveThreshold = ref(80)
const rejectThreshold = ref(60)

function avatarGrad() {
  return `linear-gradient(135deg, #${Math.floor(Math.random()*16777215).toString(16).padStart(6,'0')}, #${Math.floor(Math.random()*16777215).toString(16).padStart(6,'0')})`
}

function initials(name) {
  return (name || '?').split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2)
}

async function fetchApplications() {
  isLoading.value = true
  try {
    const res = await fetch(`${API}/api/jobs/${jobId}/applications`)
    const data = await res.json()
    if (data.status === 'success') {
      jobTitle.value = data.job_title
      applications.value = data.applications.map(app => ({
        ...app,
        _avatarGrad: avatarGrad(),
        _initials: initials(app.candidate_name || app.candidate_email)
      }))
    }
  } catch (err) {
    console.error('Fetch applications error:', err)
  } finally {
    isLoading.value = false
  }
}

async function updateStatus(app, newStatus) {
  try {
    const res = await fetch(`${API}/api/jobs/${jobId}/applications/${app.id}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    })
    const data = await res.json()
    if (data.status === 'success') {
      app.status = newStatus
    }
  } catch (err) {
    console.error('Update status error:', err)
  }
}

async function bulkAction(action, threshold, direction) {
  if (!threshold && threshold !== 0) return
  try {
    const res = await fetch(`${API}/api/jobs/${jobId}/applications/bulk-status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, threshold, direction })
    })
    const data = await res.json()
    if (data.status === 'success') {
      // Re-fetch to get updated statuses
      await fetchApplications()
      alert(`${data.updated_count} application(s) updated.`)
    }
  } catch (err) {
    console.error('Bulk action error:', err)
  }
}

function statusClass(status) {
  if (status === 'Shortlisted') return 'status-approved'
  if (status === 'Rejected') return 'status-rejected'
  return 'status-applied'
}

function scoreColorClass(score) {
  if (score >= 80) return 'circle-high'
  if (score >= 50) return 'circle-mid'
  return 'circle-low'
}

function formatBreakdownKey(key) {
  return key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
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
/* ═══ Page Header ════════════════════════════════════════════ */
.page-header {
  margin-bottom: var(--sp-6);
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--clr-text-muted);
  margin-bottom: var(--sp-3);
  transition: color 0.2s;
}
.back-link:hover { color: var(--clr-primary); }

.page-title { font-size: 2.25rem; font-weight: 800; letter-spacing: -0.02em; color: var(--clr-text); font-family: var(--font-heading); }
.page-subtitle { color: var(--clr-text-muted); margin-top: 0.25rem; font-size: 1.05rem; }

/* ═══ Bulk Toolbar ═══════════════════════════════════════════ */
.bulk-toolbar {
  margin-bottom: var(--sp-4);
  padding: var(--sp-4) var(--sp-6);
}

.bulk-toolbar:hover { transform: none; }

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
.apps-table-card:hover { transform: none; }

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

/* Score */
.score-radial { position: relative; width: 44px; height: 44px; }
.circular-chart { display: block; max-width: 100%; max-height: 100%; }
.circle-bg { stroke: var(--clr-surface-3); fill: none; stroke-width: 3.5; }
.circle { fill: none; stroke-width: 3.5; stroke-linecap: round; transition: stroke-dasharray 1s ease 0.3s; }
.circle-high { stroke: #10b981; }
.circle-mid { stroke: #f59e0b; }
.circle-low { stroke: #ef4444; }
.score-val {
  position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.7rem; font-weight: 800; color: var(--clr-text);
}

/* Status */
.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 99px;
  font-size: 0.75rem;
  font-weight: 700;
  white-space: nowrap;
}
.status-applied { background: rgba(245, 158, 11, 0.1); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.2); }
.status-approved { background: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.2); }
.status-rejected { background: rgba(239, 68, 68, 0.1); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.2); }

/* Action Buttons */
.action-group { display: flex; align-items: center; gap: 0.4rem; }
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
.loading-placeholder, .empty-placeholder {
  text-align: center;
  padding: 4rem 2rem;
}
.loading-placeholder:hover, .empty-placeholder:hover { transform: none; }
.spinner {
  width: 36px; height: 36px;
  border: 3px solid var(--clr-surface-3);
  border-top-color: var(--clr-primary);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  margin: 0 auto 1rem;
}
@keyframes spin { to { transform: rotate(360deg); } }

.empty-icon { font-size: 3rem; margin-bottom: 1rem; }

/* ═══ Modal ══════════════════════════════════════════════════ */
.v-modal-overlay {
  position: fixed; inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  z-index: 2000;
  display: flex; align-items: center; justify-content: center;
  padding: 2rem;
}

.v-modal-card {
  width: 100%; max-width: 720px; max-height: 90vh; overflow-y: auto;
  background: var(--clr-surface);
  border-radius: var(--radius-xl);
  padding: var(--sp-8);
  position: relative;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}
.v-modal-card:hover { transform: none; }

.v-modal-close {
  position: absolute; top: 1.5rem; right: 1.5rem;
  background: var(--clr-surface-2); border: none;
  width: 36px; height: 36px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; color: var(--clr-text-muted);
}

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
.analysis-box {
  background: var(--clr-surface-2);
  border-radius: var(--radius-lg);
  padding: 1.25rem;
  display: flex;
  gap: 1.25rem;
  border: 1px solid var(--clr-border);
}
.analysis-score {
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  padding-right: 1.25rem;
  border-right: 1px solid var(--clr-border);
  min-width: 90px;
}
.score-big { font-size: 2rem; font-weight: 800; color: var(--clr-primary); line-height: 1; }
.score-small { font-size: 0.7rem; color: var(--clr-text-muted); text-transform: uppercase; margin-top: 4px; font-weight: 700; }

.analysis-details { flex: 1; display: flex; flex-direction: column; gap: 0.75rem; }
.detail-row strong { font-size: 0.82rem; color: var(--clr-text); display: block; margin-bottom: 0.35rem; }
.modal-skills { margin-top: 0.15rem; }

/* Breakdown Grid */
.breakdown-grid { display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.25rem; }
.breakdown-item { display: flex; align-items: center; gap: 0.75rem; }
.breakdown-label { font-size: 0.78rem; color: var(--clr-text-muted); width: 120px; flex-shrink: 0; text-transform: capitalize; }
.breakdown-bar-wrap { flex: 1; height: 6px; background: var(--clr-surface-3); border-radius: 99px; overflow: hidden; }
.breakdown-bar { height: 100%; background: var(--clr-primary); border-radius: 99px; transition: width 0.6s ease; }
.breakdown-val { font-size: 0.75rem; font-weight: 700; color: var(--clr-text); width: 30px; text-align: right; }

/* Parsed Resume Card */
.parsed-resume-card {
  background: var(--clr-surface-2);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-lg);
  padding: 1.25rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}
.resume-field.full { grid-column: 1 / -1; }
.field-label {
  font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.08em; color: var(--clr-text-muted); margin-bottom: 0.2rem; display: block;
}
.field-value { font-size: 0.9rem; color: var(--clr-text); line-height: 1.5; }

/* Experience items */
.exp-list { display: flex; flex-direction: column; gap: 0.75rem; }
.exp-item { padding: 0.75rem; background: var(--clr-surface); border-radius: var(--radius-md); border: 1px solid var(--clr-border); }
.exp-header { font-size: 0.9rem; color: var(--clr-text); }
.exp-duration { font-size: 0.78rem; color: var(--clr-text-muted); }
.exp-desc { font-size: 0.82rem; color: var(--clr-text-muted); margin-top: 0.25rem; line-height: 1.5; }

/* Footer */
.v-modal-footer {
  margin-top: 1.5rem; display: flex; justify-content: flex-end; gap: 0.75rem;
}

/* Animations */
.v-modal-enter-active, .v-modal-leave-active { transition: opacity 0.3s ease; }
.v-modal-enter-from, .v-modal-leave-to { opacity: 0; }
.v-modal-enter-from .v-modal-card { transform: scale(0.95) translateY(20px); }

/* ═══ Responsive ═════════════════════════════════════════════ */
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

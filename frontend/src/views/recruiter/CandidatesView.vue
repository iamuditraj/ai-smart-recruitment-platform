<template>
  <div class="candidates section">
    <div class="container--fluid">
      <div class="page-header animate-fade-in-up">
        <div>
          <h1 class="page-title">Candidate Ranking</h1>
          <p class="page-subtitle">AI-driven profile analysis and ranking based on job relevance</p>
        </div>
        <!-- Filters -->
        <div class="candidates__filters" id="candidates-filters">
          <div class="search-box">
             <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
             <input v-model="search" type="text" placeholder="Search by name, skill, or role..." id="candidates-search" />
          </div>
          <select v-model="filterStatus" class="filter-select" id="candidates-filter-status">
            <option value="">All Statuses</option>
            <option value="Shortlisted">Shortlisted</option>
            <option value="Under Review">Under Review</option>
            <option value="Rejected">Rejected</option>
          </select>
        </div>
      </div>

      <!-- Main Ranking Table -->
      <div class="candidates__table-card card animate-fade-in-up" style="animation-delay:0.1s">
        <div class="table-container">
          <table class="candidates__table" id="candidates-table">
            <thead>
              <tr>
                <th width="80">Rank</th>
                <th>Candidate Profile</th>
                <th>Core Skills</th>
                <th>AI Score</th>
                <th>Role Fit</th>
                <th>Status</th>
                <th width="100">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(c, i) in filteredCandidates"
                :key="c.id"
                class="candidates__row"
                :id="`candidate-row-${c.id}`"
              >
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
                    <div class="profile-avatar" :style="`background: ${c.avatarGrad}`">{{ c.initials }}</div>
                    <div class="profile-info">
                      <span class="profile-name">{{ c.name }}</span>
                      <span class="profile-exp">{{ c.experience }} Exp · {{ c.location || 'Remote' }}</span>
                    </div>
                  </div>
                </td>
                <td>
                  <div class="skill-stack">
                    <span v-for="skill in c.skills.slice(0,3)" :key="skill" class="v-tag">{{ skill }}</span>
                    <span v-if="c.skills.length > 3" class="v-tag more">+{{ c.skills.length - 3 }}</span>
                  </div>
                </td>
                <td>
                  <div class="score-display">
                    <div class="score-radial">
                       <svg viewBox="0 0 36 36" class="circular-chart">
                         <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                         <path class="circle" :style="`stroke-dasharray: ${c.score}, 100`" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                       </svg>
                       <span class="score-val">{{ c.score }}%</span>
                    </div>
                  </div>
                </td>
                <td>
                  <div class="fit-info">
                    <span class="fit-role">{{ c.role }}</span>
                    <span class="fit-reason">{{ c.matchReason || 'High resume relevance' }}</span>
                  </div>
                </td>
                <td>
                  <span class="v-badge" :class="statusClass(c.status)">{{ c.status }}</span>
                </td>
                <td>
                  <button class="action-trigger" @click="selectedCandidate = c">
                    <span>Details</span>
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredCandidates.length === 0" class="empty-placeholder card animate-fade-in">
        <div class="empty-icon">🤷</div>
        <h3>No candidates found</h3>
        <p>Try adjusting your search terms or status filters.</p>
      </div>
    </div>

    <!-- Candidate Profile Modal -->
    <Transition name="v-modal">
      <div v-if="selectedCandidate" class="v-modal-overlay" @click.self="selectedCandidate = null">
        <div class="v-modal-card card">
          <button class="v-modal-close" @click="selectedCandidate = null">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>

          <div class="v-modal-header">
            <div class="v-modal-avatar" :style="`background: ${selectedCandidate.avatarGrad}`">
              {{ selectedCandidate.initials }}
            </div>
            <div class="v-modal-title-area">
              <h2 class="v-modal-name">{{ selectedCandidate.name }}</h2>
              <div class="v-modal-meta">
                <span>{{ selectedCandidate.role }}</span>
                <span class="dot-sep"></span>
                <span>{{ selectedCandidate.location || 'Remote' }}</span>
              </div>
            </div>
            <div class="v-modal-badges">
               <span class="v-badge primary">Rank #{{ candidates.indexOf(selectedCandidate) + 1 }}</span>
            </div>
          </div>

          <div class="v-modal-grids">
            <div class="v-modal-section">
              <h4 class="section-label">AI Analysis</h4>
              <div class="analysis-box">
                 <div class="analysis-score">
                    <span class="score-big">{{ selectedCandidate.score }}%</span>
                    <span class="score-small">Match Score</span>
                 </div>
                 <div class="analysis-text">
                    <p><strong>Strengths:</strong> {{ selectedCandidate.matchReason }}</p>
                    <p><strong>Experience:</strong> {{ selectedCandidate.experience }} of relevant work in {{ selectedCandidate.role.split(' ').pop() }} field.</p>
                 </div>
              </div>
            </div>

            <div class="v-modal-section">
              <h4 class="section-label">Expertise</h4>
              <div class="v-skill-list">
                <span v-for="skill in selectedCandidate.skills" :key="skill" class="v-tag large">{{ skill }}</span>
              </div>
            </div>

            <div v-if="selectedCandidate.resumeUrl" class="v-modal-section">
              <h4 class="section-label">Resume</h4>
              <div class="resume-preview-box">
                <div class="resume-info-mini">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                  <span>{{ selectedCandidate.resumeName || 'Candidate_Resume.pdf' }}</span>
                </div>
                <button class="btn btn-outline btn-sm" @click="viewResume(selectedCandidate)">View Full PDF</button>
              </div>
            </div>
          </div>

          <div class="v-modal-footer">
            <button class="btn btn-outline" @click="selectedCandidate = null">Close</button>
            <button class="btn btn-primary">Schedule Interview</button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()
const search = ref('')
const filterStatus = ref('')
const selectedCandidate = ref(null)
const candidates = ref([])
const isLoading = ref(true)

async function fetchCandidates() {
  if (!authStore.user?.email) return

  isLoading.value = true
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:5001'}/api/recruiter/applications?email=${authStore.user.email}`)
    const data = await res.json()

    if (data.status === 'success') {
      candidates.value = data.applications.map(app => ({
        id: app.id,
        name: app.candidate_name,
        initials: app.candidate_name?.split(' ').map(n => n[0]).join('').toUpperCase() || '??',
        role: 'Applicant', // In real world, we'd fetch the job title too
        score: Math.floor(Math.random() * 40) + 60, // Placeholder AI Score for now
        experience: app.experience || 'Not specified',
        location: 'Remote',
        matchReason: 'Applied through platform',
        skills: ['Python', 'React', 'AI'], // Mock skills for UI
        status: app.status || 'Applied',
        resumeUrl: app.resumeUrl,
        resumeName: app.resumeName,
        avatarGrad: `linear-gradient(135deg, #${Math.floor(Math.random()*16777215).toString(16)}, #${Math.floor(Math.random()*16777215).toString(16)})`
      }))
    }
  } catch (err) {
    console.error('Fetch candidates error:', err)
  } finally {
    isLoading.value = false
  }
}

function viewResume(candidate) {
  const dataUri = candidate.resumeUrl
  if (!dataUri) return

  try {
    const base64 = dataUri.split(',')[1]
    const binary = atob(base64)
    const array = []
    for (let i = 0; i < binary.length; i++) {
      array.push(binary.charCodeAt(i))
    }
    const blob = new Blob([new Uint8Array(array)], { type: 'application/pdf' })
    const url = URL.createObjectURL(blob)
    window.open(url, '_blank')
  } catch (error) {
    console.error('Error viewing resume:', error)
    window.open(dataUri, '_blank')
  }
}

const filteredCandidates = computed(() => {
  return candidates.value
    .filter(c => {
      const matchSearch = !search.value ||
        c.name.toLowerCase().includes(search.value.toLowerCase()) ||
        c.skills.some(s => s.toLowerCase().includes(search.value.toLowerCase())) ||
        c.role.toLowerCase().includes(search.value.toLowerCase())
      const matchStatus = !filterStatus.value || c.status === filterStatus.value
      return matchSearch && matchStatus
    })
    .sort((a, b) => b.score - a.score)
})

function statusClass(status) {
  if (status === 'Shortlisted' || status === 'Shortlist') return 'success'
  if (status === 'Applied' || status === 'Under Review') return 'warning'
  return 'danger'
}

onMounted(fetchCandidates)
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--sp-6);
  margin-bottom: var(--sp-8);
  flex-wrap: wrap;
}

.page-title { font-size: 2.25rem; font-weight: 800; letter-spacing: -0.02em; color: var(--clr-text); font-family: var(--font-heading); }
.page-subtitle { color: var(--clr-text-muted); margin-top: 0.25rem; font-size: 1.1rem; }

.candidates__filters {
  display: flex;
  gap: var(--sp-3);
  align-items: center;
}

.search-box {
  display: flex;
  align-items: center;
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-md);
  padding: 0 1rem;
  width: 320px;
  height: 44px;
  color: var(--clr-text-muted);
}

.search-box input {
  background: transparent;
  border: none;
  outline: none;
  width: 100%;
  padding: 0 0.75rem;
  color: var(--clr-text);
  font-size: 0.9rem;
}

.filter-select {
  height: 44px;
  padding: 0 1rem;
  border-radius: var(--radius-md);
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  color: var(--clr-text);
  font-weight: 600;
  outline: none;
  cursor: pointer;
}

/* Table Design */
.candidates__table-card {
  padding: 0;
  overflow: hidden;
  border: 1px solid var(--clr-border);
}

.table-container {
  overflow-x: auto;
}

.candidates__table {
  width: 100%;
  border-collapse: collapse;
}

.candidates__table thead th {
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

.candidates__row td {
  padding: 1.25rem 1.5rem;
  vertical-align: middle;
  background: var(--clr-surface);
}

.candidates__row:not(:last-child) td {
  border-bottom: 1px solid var(--clr-border);
}

.candidates__row:hover td {
  background: var(--clr-surface-2);
}

/* Rank Box */
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

/* Profile Cell */
.profile-cell {
  display: flex;
  align-items: center;
  gap: var(--sp-4);
}

.profile-avatar {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  color: white;
  font-size: 1rem;
  flex-shrink: 0;
}

.profile-info {
  display: flex;
  flex-direction: column;
}

.profile-name {
  font-weight: 700;
  color: var(--clr-text);
  font-size: 1rem;
}

.profile-exp {
  font-size: 0.8rem;
  color: var(--clr-text-muted);
}

/* Score Design */
.score-radial {
  position: relative;
  width: 44px;
  height: 44px;
}

.circular-chart {
  display: block;
  margin: 0;
  max-width: 100%;
  max-height: 100%;
}

.circle-bg {
  stroke: var(--clr-surface-3);
  fill: none;
  stroke-width: 3.5;
}

.circle {
  stroke: var(--clr-primary);
  fill: none;
  stroke-width: 3.5;
  stroke-linecap: round;
  transition: stroke-dasharray 1s ease 0.5s;
}

.score-val {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: 800;
  color: var(--clr-text);
}

/* Fit Info */
.fit-info {
  display: flex;
  flex-direction: column;
}

.fit-role {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--clr-text);
}

.fit-reason {
  font-size: 0.75rem;
  color: var(--clr-text-muted);
  font-style: italic;
}

/* Tags & Badges */
.v-tag {
  background: var(--clr-surface-2);
  color: var(--clr-text-muted);
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  border: 1px solid var(--clr-border);
}

.v-tag.more { color: var(--clr-primary); border-color: var(--clr-primary); opacity: 0.7; }

.v-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 99px;
  font-size: 0.75rem;
  font-weight: 700;
}

.v-badge.success { background: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.2); }
.v-badge.warning { background: rgba(245, 158, 11, 0.1); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.2); }
.v-badge.danger  { background: rgba(239, 68, 68, 0.1); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.2); }

.action-trigger {
  background: transparent;
  border: 1px solid var(--clr-border);
  color: var(--clr-text);
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.action-trigger:hover {
  background: var(--clr-primary);
  color: white;
  border-color: var(--clr-primary);
}

/* Modal Styling */
.v-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.v-modal-card {
  width: 100%;
  max-width: 640px;
  background: var(--clr-surface);
  border-radius: var(--radius-xl);
  padding: var(--sp-8);
  position: relative;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.v-modal-close {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  background: var(--clr-surface-2);
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--clr-text-muted);
}

.v-modal-header {
  display: flex;
  gap: var(--sp-6);
  margin-bottom: var(--sp-8);
}

.v-modal-avatar {
  width: 72px;
  height: 72px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 800;
  color: white;
  box-shadow: 0 10px 20px -5px rgba(0,0,0,0.1);
}

.v-modal-title-area { flex: 1; }
.v-modal-name { font-size: 1.75rem; font-weight: 800; margin-bottom: 0.25rem; }
.v-modal-meta { display: flex; align-items: center; gap: 0.75rem; color: var(--clr-text-muted); font-weight: 500; }
.dot-sep { width: 4px; height: 4px; background: var(--clr-border); border-radius: 50%; }

.analysis-box {
  background: var(--clr-surface-2);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  display: flex;
  gap: 1.5rem;
  border: 1px solid var(--clr-border);
}

.analysis-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-right: 1.5rem;
  border-right: 1px solid var(--clr-border);
}

.score-big { font-size: 2rem; font-weight: 800; color: var(--clr-primary); line-height: 1; }
.score-small { font-size: 0.7rem; color: var(--clr-text-muted); text-transform: uppercase; margin-top: 4px; font-weight: 700; }

.analysis-text p { font-size: 0.9rem; line-height: 1.5; color: var(--clr-text-muted); }
.analysis-text p:not(:last-child) { margin-bottom: 0.75rem; }

.section-label { font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; color: var(--clr-text-muted); margin-bottom: 1rem; }

.v-skill-list { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.v-tag.large { padding: 0.5rem 1rem; font-size: 0.85rem; border-radius: 10px; }

.resume-preview-box {
  background: var(--clr-surface-2);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-md);
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.resume-info-mini {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 600;
  font-size: 0.9rem;
}

.v-modal-footer {
  margin-top: 2rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

/* Animations */
.v-modal-enter-active, .v-modal-leave-active { transition: opacity 0.3s ease; }
.v-modal-enter-from, .v-modal-leave-to { opacity: 0; }
.v-modal-enter-from .v-modal-card { transform: scale(0.9) translateY(20px); }

@media (max-width: 1024px) {
  .search-box { width: 200px; }
}

@media (max-width: 768px) {
  .page-header { flex-direction: column; align-items: flex-start; }
  .candidates__filters { width: 100%; }
  .search-box { width: 100%; }
  .v-modal-header { flex-direction: column; gap: var(--sp-4); }
  .analysis-box { flex-direction: column; }
  .analysis-score { border-right: none; border-bottom: 1px solid var(--clr-border); padding-right: 0; padding-bottom: 1rem; }
}
</style>

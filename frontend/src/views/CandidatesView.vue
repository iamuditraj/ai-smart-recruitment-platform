<template>
  <div class="candidates section">
    <div class="container">
      <div class="page-header animate-fade-in-up">
        <div>
          <h1 class="page-title">Candidates</h1>
          <p class="page-subtitle">Ranked list of all applicants powered by AI scoring</p>
        </div>
        <!-- Filters -->
        <div class="candidates__filters" id="candidates-filters">
          <input v-model="search" type="text" class="form-input search-input" placeholder="🔍  Search by name or skill..." id="candidates-search" />
          <select v-model="filterStatus" class="form-input filter-select" id="candidates-filter-status">
            <option value="">All Status</option>
            <option value="Shortlisted">Shortlisted</option>
            <option value="Under Review">Under Review</option>
            <option value="Rejected">Rejected</option>
          </select>
        </div>
      </div>

      <!-- Table -->
      <div class="candidates__table-wrap animate-fade-in-up" style="animation-delay:0.1s">
        <table class="candidates__table" id="candidates-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Candidate</th>
              <th>Role Applied</th>
              <th>AI Score</th>
              <th>Skills</th>
              <th>Status</th>
              <th>Action</th>
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
                <span class="rank-number" :class="i === 0 ? 'top' : ''">{{ i + 1 }}</span>
              </td>
              <td>
                <div class="candidate-cell">
                  <div class="candidate-avatar" :style="`background: ${c.avatarGrad}`">{{ c.initials }}</div>
                  <div class="candidate-info">
                    <span class="candidate-name">{{ c.name }}</span>
                    <span class="candidate-exp">{{ c.experience }}</span>
                  </div>
                </div>
              </td>
              <td><span class="candidate-role">{{ c.role }}</span></td>
              <td>
                <div class="score-bar">
                  <div class="score-bar__fill" :style="`width: ${c.score}%; background: ${c.score >= 80 ? '#10b981' : c.score >= 60 ? '#f59e0b' : '#ef4444'}`"></div>
                  <span class="score-bar__label" :class="c.score >= 80 ? 'high' : c.score >= 60 ? 'mid' : 'low'">{{ c.score }}%</span>
                </div>
              </td>
              <td>
                <div class="skill-list">
                  <span v-for="skill in c.skills.slice(0,3)" :key="skill" class="skill-tag">{{ skill }}</span>
                  <span v-if="c.skills.length > 3" class="skill-tag skill-tag--more">+{{ c.skills.length - 3 }}</span>
                </div>
              </td>
              <td>
                <span class="badge" :class="statusClass(c.status)">{{ c.status }}</span>
              </td>
              <td>
                <button class="btn btn-ghost btn-sm" :id="`view-candidate-${c.id}`" @click="selectedCandidate = c">View</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Empty State -->
      <div v-if="filteredCandidates.length === 0" class="empty-state card text-center animate-fade-in">
        <p style="font-size:2rem">🔍</p>
        <p>No candidates match your filter.</p>
      </div>
    </div>

    <!-- Candidate Detail Modal -->
    <Transition name="modal">
      <div v-if="selectedCandidate" class="modal-overlay" id="candidate-modal-overlay" @click.self="selectedCandidate = null">
        <div class="modal-box card" id="candidate-modal">
          <button class="modal-close btn btn-ghost" id="modal-close-btn" @click="selectedCandidate = null">✕</button>
          <div class="modal-header">
            <div class="modal-avatar" :style="`background: ${selectedCandidate.avatarGrad}`">{{ selectedCandidate.initials }}</div>
            <div>
              <h2 class="modal-name">{{ selectedCandidate.name }}</h2>
              <p class="modal-role">{{ selectedCandidate.role }}</p>
            </div>
          </div>
          <div class="modal-body">
            <div class="modal-stat">
              <span class="modal-stat__label">AI Score</span>
              <span class="modal-stat__value gradient-text">{{ selectedCandidate.score }}%</span>
            </div>
            <div class="modal-stat">
              <span class="modal-stat__label">Experience</span>
              <span class="modal-stat__value">{{ selectedCandidate.experience }}</span>
            </div>
            <div class="modal-stat">
              <span class="modal-stat__label">Status</span>
              <span class="badge" :class="statusClass(selectedCandidate.status)">{{ selectedCandidate.status }}</span>
            </div>
          </div>
          <div>
            <p class="modal-stat__label" style="margin-bottom:0.5rem">Skills</p>
            <div class="skill-list">
              <span v-for="skill in selectedCandidate.skills" :key="skill" class="skill-tag">{{ skill }}</span>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const search = ref('')
const filterStatus = ref('')
const selectedCandidate = ref(null)

const candidates = [
  { id: 1, name: 'Priya Sharma', initials: 'PS', role: 'Senior ML Engineer', score: 92, experience: '5 yrs', skills: ['Python', 'NLP', 'TensorFlow', 'BERT', 'MLOps'], status: 'Shortlisted', avatarGrad: 'linear-gradient(135deg,#6366f1,#8b5cf6)' },
  { id: 2, name: 'Riya Kapoor', initials: 'RK', role: 'ML Engineer', score: 85, experience: '4 yrs', skills: ['PyTorch', 'MLOps', 'Docker', 'AWS', 'Python'], status: 'Shortlisted', avatarGrad: 'linear-gradient(135deg,#10b981,#06b6d4)' },
  { id: 3, name: 'Arjun Mehta', initials: 'AM', role: 'Data Scientist', score: 78, experience: '3 yrs', skills: ['Python', 'Scikit-learn', 'SQL', 'Pandas'], status: 'Under Review', avatarGrad: 'linear-gradient(135deg,#f59e0b,#ef4444)' },
  { id: 4, name: 'Rahul Joshi', initials: 'RJ', role: 'DevOps Engineer', score: 95, experience: '6 yrs', skills: ['Kubernetes', 'Docker', 'CI/CD', 'Terraform', 'AWS'], status: 'Shortlisted', avatarGrad: 'linear-gradient(135deg,#06b6d4,#6366f1)' },
  { id: 5, name: 'Neha Singh', initials: 'NS', role: 'Full Stack Dev', score: 74, experience: '2 yrs', skills: ['React', 'Node.js', 'MongoDB'], status: 'Under Review', avatarGrad: 'linear-gradient(135deg,#8b5cf6,#ec4899)' },
  { id: 6, name: 'Vikram Nair', initials: 'VN', role: 'Data Scientist', score: 48, experience: '1 yr', skills: ['Excel', 'PowerBI'], status: 'Rejected', avatarGrad: 'linear-gradient(135deg,#64748b,#475569)' },
]

const filteredCandidates = computed(() => {
  return candidates
    .filter(c => {
      const matchSearch = !search.value || c.name.toLowerCase().includes(search.value.toLowerCase()) || c.skills.some(s => s.toLowerCase().includes(search.value.toLowerCase()))
      const matchStatus = !filterStatus.value || c.status === filterStatus.value
      return matchSearch && matchStatus
    })
    .sort((a, b) => b.score - a.score)
})

function statusClass(status) {
  if (status === 'Shortlisted') return 'badge-success'
  if (status === 'Under Review') return 'badge-warning'
  return 'badge-danger'
}
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--sp-4);
  margin-bottom: var(--sp-8);
  flex-wrap: wrap;
}

.page-title { font-size: 2rem; font-weight: 800; letter-spacing: -0.02em; }
.page-subtitle { color: var(--clr-text-muted); margin-top: var(--sp-1); }

.candidates__filters {
  display: flex;
  gap: var(--sp-3);
  flex-wrap: wrap;
}

.search-input { min-width: 220px; }
.filter-select { min-width: 150px; background: var(--clr-surface-2); }

/* Table */
.candidates__table-wrap {
  overflow-x: auto;
  border-radius: var(--radius-lg);
  border: 1px solid var(--clr-border);
}

.candidates__table {
  width: 100%;
  border-collapse: collapse;
}

.candidates__table thead th {
  background: var(--clr-surface-2);
  padding: 0.875rem 1.2rem;
  text-align: left;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--clr-text-muted);
  letter-spacing: 0.05em;
  text-transform: uppercase;
  white-space: nowrap;
}

.candidates__row td {
  padding: 0.875rem 1.2rem;
  border-top: 1px solid var(--clr-border);
  vertical-align: middle;
}

.candidates__row:hover td {
  background: rgba(255,255,255,0.02);
}

/* Rank */
.rank-number {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-full);
  font-weight: 700;
  font-size: 0.8rem;
  background: var(--clr-surface-3);
}

.rank-number.top {
  background: var(--gradient-brand);
  color: white;
}

/* Candidate Cell */
.candidate-cell {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
}

.candidate-avatar {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.candidate-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.candidate-name {
  font-weight: 600;
  font-size: 0.9rem;
  white-space: nowrap;
}

.candidate-exp {
  font-size: 0.75rem;
  color: var(--clr-text-muted);
}

.candidate-role {
  font-size: 0.85rem;
  color: var(--clr-text-light);
}

/* Score Bar */
.score-bar {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  min-width: 130px;
}

.score-bar__fill {
  height: 6px;
  border-radius: var(--radius-full);
  flex: 1;
  transition: width 0.8s ease;
}

.score-bar__label {
  font-size: 0.8rem;
  font-weight: 700;
  width: 36px;
  text-align: right;
}

.score-bar__label.high { color: #6ee7b7; }
.score-bar__label.mid  { color: #fcd34d; }
.score-bar__label.low  { color: #fca5a5; }

/* Skills */
.skill-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sp-1);
}

.skill-tag {
  background: var(--clr-surface-3);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-full);
  padding: 0.15rem 0.55rem;
  font-size: 0.72rem;
  font-weight: 500;
  color: var(--clr-text-light);
  white-space: nowrap;
}

.skill-tag--more {
  color: var(--clr-primary);
  border-color: rgba(99,102,241,0.3);
  background: rgba(99,102,241,0.08);
}

/* Badges */
.badge-success { background: rgba(16,185,129,0.12); color: #6ee7b7; border: 1px solid rgba(16,185,129,0.25); }
.badge-warning { background: rgba(245,158,11,0.12); color: #fcd34d; border: 1px solid rgba(245,158,11,0.25); }
.badge-danger  { background: rgba(239,68,68,0.12);  color: #fca5a5; border: 1px solid rgba(239,68,68,0.25); }

.btn-sm { padding: 0.35rem 0.8rem; font-size: 0.8rem; border-radius: var(--radius-md); }

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--sp-3);
  padding: var(--sp-12);
  margin-top: var(--sp-6);
  color: var(--clr-text-muted);
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.7);
  backdrop-filter: blur(4px);
  z-index: 200;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--sp-4);
}

.modal-box {
  width: 100%;
  max-width: 460px;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--sp-6);
}

.modal-close {
  position: absolute;
  top: var(--sp-4);
  right: var(--sp-4);
  font-size: 1rem;
}

.modal-header {
  display: flex;
  align-items: center;
  gap: var(--sp-4);
}

.modal-avatar {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: white;
  font-size: 1.1rem;
}

.modal-name { font-size: 1.2rem; font-weight: 700; }
.modal-role { color: var(--clr-text-muted); font-size: 0.875rem; margin-top: 2px; }

.modal-body {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--sp-4);
}

.modal-stat {
  display: flex;
  flex-direction: column;
  gap: var(--sp-1);
}

.modal-stat__label {
  font-size: 0.75rem;
  color: var(--clr-text-muted);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.modal-stat__value {
  font-size: 1rem;
  font-weight: 600;
}

.modal-enter-active, .modal-leave-active { transition: all 0.2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-from .modal-box, .modal-leave-to .modal-box { transform: scale(0.95) translateY(16px); }
</style>

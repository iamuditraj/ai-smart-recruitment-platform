<template>
  <div class="dashboard section">
    <div class="container">
      <!-- Header -->
      <div class="dashboard__header animate-fade-in-up">
        <div>
          <h1 class="dashboard__title">Dashboard</h1>
          <p class="dashboard__subtitle">Overview of your recruitment pipeline</p>
        </div>
        <RouterLink to="/resume-screening" class="btn btn-primary" id="dashboard-upload-btn">
          + Upload Resumes
        </RouterLink>
      </div>

      <!-- KPI Cards -->
      <div class="kpi-grid animate-fade-in-up" style="animation-delay:0.1s">
        <div v-for="kpi in kpis" :key="kpi.label" class="kpi-card card" :id="`kpi-${kpi.label.toLowerCase().replace(/\s/g,'-')}`">
          <div class="kpi-card__icon" :style="`background: ${kpi.gradient}`">
            <span v-html="kpi.icon"></span>
          </div>
          <div class="kpi-card__body">
            <span class="kpi-card__value">{{ kpi.value }}</span>
            <span class="kpi-card__label">{{ kpi.label }}</span>
          </div>
          <span class="kpi-card__change" :class="kpi.up ? 'up' : 'down'">
            {{ kpi.up ? '↑' : '↓' }} {{ kpi.change }}
          </span>
        </div>
      </div>

      <!-- Pipeline -->
      <div class="pipeline-section animate-fade-in-up" style="animation-delay:0.2s">
        <h2 class="subsection-title">Candidates Pipeline</h2>
        <div class="pipeline-stages">
          <div v-for="stage in pipeline" :key="stage.name" class="pipeline-stage card">
            <div class="pipeline-stage__header">
              <span class="pipeline-stage__name">{{ stage.name }}</span>
              <span class="badge" :class="stage.badgeClass">{{ stage.count }}</span>
            </div>
            <div v-for="candidate in stage.candidates" :key="candidate.name" class="pipeline-candidate">
              <div class="pipeline-candidate__avatar">{{ candidate.initials }}</div>
              <div class="pipeline-candidate__info">
                <span class="pipeline-candidate__name">{{ candidate.name }}</span>
                <span class="pipeline-candidate__role">{{ candidate.role }}</span>
              </div>
              <span class="pipeline-candidate__score" :class="candidate.scoreClass">{{ candidate.score }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="activity-section animate-fade-in-up" style="animation-delay:0.3s">
        <h2 class="subsection-title">Recent Activity</h2>
        <div class="activity-list card">
          <div v-for="(item, i) in activity" :key="i" class="activity-item" :id="`activity-item-${i}`">
            <div class="activity-item__dot" :style="`background: ${item.color}`"></div>
            <div class="activity-item__body">
              <span class="activity-item__text">{{ item.text }}</span>
              <span class="activity-item__time">{{ item.time }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const kpis = [
  { label: 'Total Applicants', value: '248', change: '12%', up: true,
    gradient: 'linear-gradient(135deg,#6366f1,#8b5cf6)',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>` },
  { label: 'Screened', value: '184', change: '8%', up: true,
    gradient: 'linear-gradient(135deg,#06b6d4,#6366f1)',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>` },
  { label: 'Shortlisted', value: '42', change: '5%', up: true,
    gradient: 'linear-gradient(135deg,#10b981,#06b6d4)',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>` },
  { label: 'Rejected', value: '22', change: '3%', up: false,
    gradient: 'linear-gradient(135deg,#ef4444,#f97316)',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>` },
]

const pipeline = [
  {
    name: 'Applied', count: '248', badgeClass: 'badge-primary',
    candidates: [
      { name: 'Priya Sharma', initials: 'PS', role: 'Frontend Dev', score: 88, scoreClass: 'high' },
      { name: 'Arjun Mehta', initials: 'AM', role: 'ML Engineer', score: 76, scoreClass: 'mid' },
    ],
  },
  {
    name: 'Screened', count: '184', badgeClass: 'badge-primary',
    candidates: [
      { name: 'Riya Kapoor', initials: 'RK', role: 'Backend Dev', score: 92, scoreClass: 'high' },
      { name: 'Vikram Nair', initials: 'VN', role: 'Data Scientist', score: 81, scoreClass: 'high' },
    ],
  },
  {
    name: 'Assessment', count: '42', badgeClass: 'badge-warning',
    candidates: [
      { name: 'Neha Singh', initials: 'NS', role: 'Full Stack', score: 74, scoreClass: 'mid' },
    ],
  },
  {
    name: 'Shortlisted', count: '12', badgeClass: 'badge-success',
    candidates: [
      { name: 'Rahul Joshi', initials: 'RJ', role: 'DevOps Eng.', score: 95, scoreClass: 'high' },
    ],
  },
]

const activity = [
  { text: '12 new resumes uploaded for "Senior ML Engineer"', time: '2 min ago', color: '#6366f1' },
  { text: 'Riya Kapoor scored 92% — moved to Shortlisted', time: '18 min ago', color: '#10b981' },
  { text: 'Skill assessment sent to 8 candidates', time: '1 hr ago', color: '#06b6d4' },
  { text: 'Arjun Mehta completed mock interview analysis', time: '3 hrs ago', color: '#8b5cf6' },
  { text: '22 candidates auto-rejected (score < 50%)', time: '5 hrs ago', color: '#ef4444' },
]
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
}

.dashboard__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--sp-4);
  margin-bottom: var(--sp-8);
  flex-wrap: wrap;
}

.dashboard__title {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.dashboard__subtitle {
  color: var(--clr-text-muted);
  margin-top: var(--sp-1);
}

/* KPIs */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--sp-4);
  margin-bottom: var(--sp-10);
}

.kpi-card {
  display: flex;
  align-items: center;
  gap: var(--sp-4);
  padding: var(--sp-4) var(--sp-6);
}

.kpi-card__icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.kpi-card__body {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.kpi-card__value {
  font-family: var(--font-heading);
  font-size: 1.6rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.kpi-card__label {
  font-size: 0.8rem;
  color: var(--clr-text-muted);
  font-weight: 500;
}

.kpi-card__change {
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.2rem 0.5rem;
  border-radius: var(--radius-full);
}

.kpi-card__change.up   { color: #6ee7b7; background: rgba(16,185,129,0.1); }
.kpi-card__change.down { color: #fca5a5; background: rgba(239,68,68,0.1); }

/* Pipeline */
.subsection-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: var(--sp-4);
}

.pipeline-section,
.activity-section {
  margin-bottom: var(--sp-10);
}

.pipeline-stages {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--sp-4);
}

.pipeline-stage {
  display: flex;
  flex-direction: column;
  gap: var(--sp-3);
}

.pipeline-stage__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--sp-2);
}

.pipeline-stage__name {
  font-weight: 700;
  font-size: 0.9rem;
}

.pipeline-candidate {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  padding: var(--sp-3);
  background: var(--clr-surface);
  border-radius: var(--radius-md);
  border: 1px solid var(--clr-border);
}

.pipeline-candidate__avatar {
  width: 34px;
  height: 34px;
  border-radius: var(--radius-full);
  background: var(--gradient-brand);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.pipeline-candidate__info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.pipeline-candidate__name {
  font-size: 0.85rem;
  font-weight: 600;
}

.pipeline-candidate__role {
  font-size: 0.75rem;
  color: var(--clr-text-muted);
}

.pipeline-candidate__score {
  font-size: 0.8rem;
  font-weight: 700;
}

.pipeline-candidate__score.high { color: #6ee7b7; }
.pipeline-candidate__score.mid  { color: #fcd34d; }
.pipeline-candidate__score.low  { color: #fca5a5; }

/* Activity */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 0;
  padding: 0;
  overflow: hidden;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: var(--sp-4);
  padding: var(--sp-4) var(--sp-6);
  border-bottom: 1px solid var(--clr-border);
  transition: background var(--transition-fast);
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-item:hover {
  background: rgba(255,255,255,0.02);
}

.activity-item__dot {
  width: 8px;
  height: 8px;
  border-radius: var(--radius-full);
  flex-shrink: 0;
}

.activity-item__body {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex: 1;
  gap: var(--sp-4);
  flex-wrap: wrap;
}

.activity-item__text {
  font-size: 0.875rem;
  color: var(--clr-text-light);
}

.activity-item__time {
  font-size: 0.78rem;
  color: var(--clr-text-muted);
  white-space: nowrap;
}
</style>

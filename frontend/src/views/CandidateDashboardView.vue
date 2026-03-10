<template>
  <div class="dashboard">
    <div class="content-area">
      <!-- Header -->
      <div class="dashboard__header animate-fade-in-up">
        <div>
          <h1 class="dashboard__title">Candidate Dashboard</h1>
          <p class="dashboard__subtitle">Track your job applications and improvements</p>
        </div>
        <RouterLink to="/resume-generation" class="btn btn-primary" id="dashboard-build-btn">
          Improve Your Resume
        </RouterLink>
      </div>

      <!-- KPI Cards -->
      <div class="kpi-grid animate-fade-in-up" style="animation-delay:0.1s">
        <div v-for="kpi in kpis" :key="kpi.label" class="kpi-card card">
          <div class="kpi-card__icon" :style="`background: ${kpi.gradient}`">
            <span v-html="kpi.icon"></span>
          </div>
          <div class="kpi-card__body">
            <span class="kpi-card__value">{{ kpi.value }}</span>
            <span class="kpi-card__label">{{ kpi.label }}</span>
          </div>
        </div>
      </div>

      <!-- Applications Section -->
      <div class="applications-section animate-fade-in-up" style="animation-delay:0.2s">
        <h2 class="subsection-title">Recent Applications</h2>
        <div class="applications-list grid">
          <div v-for="app in applications" :key="app.company" class="app-card card">
            <div class="app-card__header">
              <div class="app-card__company">
                <div class="app-card__logo">{{ app.company[0] }}</div>
                <div>
                  <h3 class="app-card__title">{{ app.role }}</h3>
                  <p class="app-card__subtitle">{{ app.company }}</p>
                </div>
              </div>
              <span class="badge" :class="app.statusClass">{{ app.status }}</span>
            </div>
            <div class="app-card__body">
              <div class="progress-bar">
                <div class="progress-bar__fill" :style="`width: ${app.progress}%`" :class="app.statusClass"></div>
              </div>
              <div class="app-card__footer">
                <span>Resume Match: <strong>{{ app.match }}%</strong></span>
                <span>Applied {{ app.date }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Preparation Section -->
      <div class="prep-section animate-fade-in-up" style="animation-delay:0.3s">
        <h2 class="subsection-title">Recommended Preparation</h2>
        <div class="prep-grid">
          <div class="card prep-card">
             <div class="prep-card__icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m16 6 4 14"/><path d="M12 6v14"/><path d="M8 8v12"/><path d="M4 4v16"/></svg></div>
             <h3>Skill Gap Analysis</h3>
             <p>AI analyzed your resume against "Senior Frontend Dev" roles. You should focus on: **React Query** and **Testing Libraries**.</p>
             <button class="btn btn-outline btn-sm">View Full Analysis</button>
          </div>
          <div class="card prep-card">
             <div class="prep-card__icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg></div>
             <h3>Mock Interview</h3>
             <p>Ready to practice? Let HireAI conduct a mock technical interview based on your applied roles.</p>
             <RouterLink to="/mock-interview" class="btn btn-outline btn-sm">Start Practice</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const kpis = [
  { label: 'Applications', value: '12', gradient: 'linear-gradient(135deg,#6366f1,#8b5cf6)', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>' },
  { label: 'Interviews', value: '3', gradient: 'linear-gradient(135deg,#06b6d4,#6366f1)', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>' },
  { label: 'Skill Score', value: '88%', gradient: 'linear-gradient(135deg,#10b981,#06b6d4)', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>' },
  { label: 'Offers', value: '1', gradient: 'linear-gradient(135deg,#f97316,#fbbf24)', icon: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M6 9a6 6 0 1 0 12 0"/><path d="M12 15V3"/><path d="m9 6 3-3 3 3"/></svg>' },
]

const applications = [
  { company: 'Google', role: 'Frontend Engineer', status: 'Interviewing', statusClass: 'badge-primary', progress: 60, match: 92, date: '2 days ago' },
  { company: 'Meta', role: 'React Developer', status: 'Applied', statusClass: 'badge-warning', progress: 20, match: 85, date: '5 days ago' },
  { company: 'Netflix', role: 'Senior UX Engineer', status: 'Screening', statusClass: 'badge-primary', progress: 40, match: 78, date: '1 week ago' },
]
</script>

<style scoped>
.dashboard { min-height: 100vh; background-color: var(--clr-bg); color: var(--clr-text); }
.dashboard__header { display: flex; align-items: flex-start; justify-content: space-between; gap: var(--sp-4); margin-bottom: var(--sp-8); flex-wrap: wrap; }
.dashboard__title { font-size: 2rem; font-weight: 800; color: var(--clr-text); }
.dashboard__subtitle { color: var(--clr-text-muted); margin-top: var(--sp-1); }

.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: var(--sp-4); margin-bottom: var(--sp-10); }
.kpi-card { display: flex; align-items: center; gap: var(--sp-4); padding: var(--sp-4) var(--sp-6); background: var(--clr-surface); border: 1px solid var(--clr-border); }
.kpi-card__icon { width: 44px; height: 44px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.kpi-card__body { display: flex; flex-direction: column; }
.kpi-card__value { font-size: 1.5rem; font-weight: 800; color: var(--clr-text); }
.kpi-card__label { font-size: 0.8rem; color: var(--clr-text-muted); }

.subsection-title { font-size: 1.25rem; font-weight: 700; margin-bottom: var(--sp-4); color: var(--clr-text); }

.applications-list { grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: var(--sp-6); margin-bottom: var(--sp-10); }
.app-card { padding: var(--sp-6); transition: transform 0.2s ease, border-color 0.2s ease; background: var(--clr-surface); border: 1px solid var(--clr-border); }
.app-card:hover { transform: translateY(-4px); border-color: var(--clr-primary); }
.app-card__header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: var(--sp-4); }
.app-card__company { display: flex; gap: var(--sp-3); align-items: center; }
.app-card__logo { width: 40px; height: 40px; border-radius: var(--radius-md); background: var(--clr-surface-2); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.2rem; border: 1px solid var(--clr-border); color: var(--clr-text); }
.app-card__title { font-size: 1rem; font-weight: 700; margin: 0; color: var(--clr-text); }
.app-card__subtitle { font-size: 0.85rem; color: var(--clr-text-muted); margin: 0; }

.progress-bar { width: 100%; height: 6px; background: var(--clr-surface-3); border-radius: 10px; margin-bottom: var(--sp-3); overflow: hidden; }
.progress-bar__fill { height: 100%; border-radius: 10px; transition: width 0.5s ease; }
.progress-bar__fill.badge-primary { background: var(--gradient-brand); }
.progress-bar__fill.badge-warning { background: var(--clr-warning); }

.app-card__footer { display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--clr-text-muted); }

.prep-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: var(--sp-6); }
.prep-card { padding: var(--sp-6); text-align: center; background: var(--clr-surface); border: 1px solid var(--clr-border); }
.prep-card__icon { width: 50px; height: 50px; border-radius: 50%; background: var(--gradient-glow); color: var(--clr-primary); display: flex; align-items: center; justify-content: center; margin: 0 auto var(--sp-4); }
.prep-card h3 { font-size: 1rem; font-weight: 700; margin-bottom: var(--sp-2); color: var(--clr-text); }
.prep-card p { font-size: 0.85rem; color: var(--clr-text-muted); margin-bottom: var(--sp-4); line-height: 1.5; }
</style>

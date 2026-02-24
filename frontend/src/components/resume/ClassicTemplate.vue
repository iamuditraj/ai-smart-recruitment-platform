<template>
  <div class="classic-resume" id="resume-classic">
    <!-- Sidebar -->
    <aside class="cr-sidebar">
      <!-- Name + Title -->
      <div class="cr-name-block">
        <div class="cr-avatar">{{ initials }}</div>
        <h1 class="cr-name">{{ d.personal.fullName || 'Your Name' }}</h1>
        <p class="cr-job-title">{{ d.personal.jobTitle || 'Job Title' }}</p>
      </div>

      <!-- Contact -->
      <div class="cr-section">
        <h3 class="cr-section-title">Contact</h3>
        <ul class="cr-contact-list">
          <li v-if="d.personal.email">
            <span class="cr-icon">✉</span>{{ d.personal.email }}
          </li>
          <li v-if="d.personal.phone">
            <span class="cr-icon">☎</span>{{ d.personal.phone }}
          </li>
          <li v-if="d.personal.location">
            <span class="cr-icon">📍</span>{{ d.personal.location }}
          </li>
          <li v-if="d.personal.linkedin">
            <span class="cr-icon">in</span>{{ d.personal.linkedin }}
          </li>
          <li v-if="d.personal.github">
            <span class="cr-icon">⌥</span>{{ d.personal.github }}
          </li>
          <li v-if="d.personal.website">
            <span class="cr-icon">🌐</span>{{ d.personal.website }}
          </li>
        </ul>
      </div>

      <!-- Technical Skills -->
      <div class="cr-section" v-if="d.skills.technical.length">
        <h3 class="cr-section-title">Technical Skills</h3>
        <div class="cr-tags">
          <span v-for="s in d.skills.technical" :key="s" class="cr-tag">{{ s }}</span>
        </div>
      </div>

      <!-- Soft Skills -->
      <div class="cr-section" v-if="d.skills.soft.length">
        <h3 class="cr-section-title">Soft Skills</h3>
        <div class="cr-tags">
          <span v-for="s in d.skills.soft" :key="s" class="cr-tag cr-tag--soft">{{ s }}</span>
        </div>
      </div>

      <!-- Certifications (sidebar) -->
      <div class="cr-section" v-if="d.certifications.length">
        <h3 class="cr-section-title">Certifications</h3>
        <ul class="cr-cert-list">
          <li v-for="cert in d.certifications" :key="cert.id">
            <strong>{{ cert.name }}</strong>
            <span v-if="cert.issuer"> — {{ cert.issuer }}</span>
            <span v-if="cert.year" class="cr-cert-year">{{ cert.year }}</span>
          </li>
        </ul>
      </div>
    </aside>

    <!-- Main Panel -->
    <main class="cr-main">
      <!-- Summary -->
      <section class="cr-main-section" v-if="d.summary">
        <h2 class="cr-main-title">Profile Summary</h2>
        <p class="cr-summary-text">{{ d.summary }}</p>
      </section>

      <!-- Experience -->
      <section class="cr-main-section" v-if="d.experience.length">
        <h2 class="cr-main-title">Work Experience</h2>
        <div v-for="exp in d.experience" :key="exp.id" class="cr-entry">
          <div class="cr-entry-header">
            <span class="cr-entry-role">{{ exp.title || 'Job Title' }}</span>
            <span class="cr-entry-date">{{ exp.startDate || 'Start' }} – {{ exp.current ? 'Present' : (exp.endDate || 'End') }}</span>
          </div>
          <p class="cr-entry-org">{{ exp.company || 'Company' }}<span v-if="exp.location"> · {{ exp.location }}</span></p>
          <p class="cr-entry-desc">{{ exp.description }}</p>
        </div>
      </section>

      <!-- Education -->
      <section class="cr-main-section" v-if="d.education.length">
        <h2 class="cr-main-title">Education</h2>
        <div v-for="edu in d.education" :key="edu.id" class="cr-entry">
          <div class="cr-entry-header">
            <span class="cr-entry-role">{{ edu.degree || 'Degree' }}</span>
            <span class="cr-entry-date">{{ edu.startYear || '' }} – {{ edu.endYear || '' }}</span>
          </div>
          <p class="cr-entry-org">{{ edu.institution || 'Institution' }}<span v-if="edu.location"> · {{ edu.location }}</span></p>
          <p v-if="edu.gpa" class="cr-entry-desc">GPA: {{ edu.gpa }}</p>
        </div>
      </section>

      <!-- Projects -->
      <section class="cr-main-section" v-if="d.projects.length">
        <h2 class="cr-main-title">Projects</h2>
        <div v-for="proj in d.projects" :key="proj.id" class="cr-entry">
          <div class="cr-entry-header">
            <span class="cr-entry-role">{{ proj.name || 'Project Name' }}</span>
            <a v-if="proj.link" :href="proj.link" class="cr-proj-link">{{ proj.link }}</a>
          </div>
          <p class="cr-entry-desc">{{ proj.description }}</p>
          <div v-if="proj.tech" class="cr-proj-techs">
            <span v-for="t in proj.tech.split(',')" :key="t" class="cr-proj-tech">{{ t.trim() }}</span>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: { type: Object, required: true },
})

const d = computed(() => props.data)

const initials = computed(() => {
  const name = d.value.personal.fullName || ''
  return name.split(' ').slice(0, 2).map(w => w[0] || '').join('').toUpperCase() || '?'
})
</script>

<style scoped>
.classic-resume {
  display: flex;
  font-family: 'Georgia', 'Times New Roman', serif;
  background: #fff;
  color: #1a1a2e;
  min-height: 1056px;
  width: 100%;
  font-size: 12px;
  line-height: 1.5;
}

/* Sidebar */
.cr-sidebar {
  width: 38%;
  background: #1e3a5f;
  color: #e8f0fe;
  padding: 28px 22px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  flex-shrink: 0;
}

.cr-name-block {
  text-align: center;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(255,255,255,0.15);
}

.cr-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4f9cf9, #6fcf97);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 700;
  color: white;
  margin: 0 auto 10px;
  font-family: 'Inter', sans-serif;
}

.cr-name {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  font-family: 'Inter', sans-serif;
  line-height: 1.2;
  margin: 0;
}

.cr-job-title {
  font-size: 11px;
  color: #93c5fd;
  margin-top: 4px;
  font-family: 'Inter', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.cr-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.cr-section-title {
  font-family: 'Inter', sans-serif;
  font-size: 9.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #93c5fd;
  padding-bottom: 4px;
  border-bottom: 1px solid rgba(255,255,255,0.15);
  margin: 0;
}

.cr-contact-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.cr-contact-list li {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 10px;
  color: #cbd5e1;
  word-break: break-all;
}

.cr-icon {
  font-size: 10px;
  flex-shrink: 0;
  margin-top: 1px;
}

.cr-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.cr-tag {
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 3px;
  padding: 2px 7px;
  font-size: 9.5px;
  color: #e2e8f0;
  font-family: 'Inter', sans-serif;
}

.cr-tag--soft {
  background: rgba(111, 207, 151, 0.15);
  border-color: rgba(111, 207, 151, 0.3);
  color: #6fcf97;
}

.cr-cert-list {
  padding: 0;
  margin: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 10px;
  color: #cbd5e1;
}

.cr-cert-year {
  display: block;
  color: #93c5fd;
  font-size: 9px;
}

/* Main Area */
.cr-main {
  flex: 1;
  padding: 28px 26px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.cr-main-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.cr-main-title {
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #1e3a5f;
  padding-bottom: 5px;
  border-bottom: 2px solid #1e3a5f;
  margin: 0;
}

.cr-summary-text {
  font-size: 11px;
  color: #374151;
  line-height: 1.7;
}

.cr-entry {
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f1f5f9;
}
.cr-entry:last-child { border-bottom: none; padding-bottom: 0; }

.cr-entry-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}

.cr-entry-role {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 11.5px;
  color: #1e3a5f;
}

.cr-entry-date {
  font-size: 9.5px;
  color: #64748b;
  white-space: nowrap;
  font-family: 'Inter', sans-serif;
}

.cr-entry-org {
  font-style: italic;
  font-size: 10.5px;
  color: #4f7aad;
}

.cr-entry-desc {
  font-size: 10.5px;
  color: #374151;
  line-height: 1.6;
  margin: 0;
}

.cr-proj-link {
  font-size: 9px;
  color: #4f7aad;
  text-decoration: none;
  word-break: break-all;
}

.cr-proj-techs {
  display: flex;
  flex-wrap: wrap;
  gap: 3px;
}

.cr-proj-tech {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 2px;
  padding: 1px 6px;
  font-size: 9px;
  color: #1d4ed8;
  font-family: 'Inter', sans-serif;
}
</style>

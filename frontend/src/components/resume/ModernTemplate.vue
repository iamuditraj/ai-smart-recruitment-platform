<template>
  <div class="modern-resume" id="resume-modern">
    <!-- Header -->
    <header class="mr-header">
      <div class="mr-header__left">
        <div class="mr-avatar">{{ initials }}</div>
        <div>
          <h1 class="mr-name">{{ d.personal.fullName || 'Your Name' }}</h1>
          <p class="mr-job-title">{{ d.personal.jobTitle || 'Job Title' }}</p>
          <div class="mr-contact-row">
            <span v-if="d.personal.email">✉ {{ d.personal.email }}</span>
            <span v-if="d.personal.phone">☎ {{ d.personal.phone }}</span>
            <span v-if="d.personal.location">📍 {{ d.personal.location }}</span>
            <span v-if="d.personal.linkedin">in {{ d.personal.linkedin }}</span>
            <span v-if="d.personal.github">⌥ {{ d.personal.github }}</span>
          </div>
        </div>
      </div>
    </header>

    <div class="mr-body">
      <!-- Left Column -->
      <div class="mr-left">
        <!-- Summary -->
        <section v-if="d.summary" class="mr-section">
          <h2 class="mr-section-title"><span class="mr-section-icon">◈</span> About Me</h2>
          <p class="mr-summary">{{ d.summary }}</p>
        </section>

        <!-- Technical Skills -->
        <section v-if="d.skills.technical.length" class="mr-section">
          <h2 class="mr-section-title"><span class="mr-section-icon">◈</span> Technical Skills</h2>
          <div class="mr-skill-bars">
            <div v-for="skill in d.skills.technical" :key="skill" class="mr-skill-bar">
              <span class="mr-skill-name">{{ skill }}</span>
              <div class="mr-skill-track">
                <div class="mr-skill-fill"></div>
              </div>
            </div>
          </div>
        </section>

        <!-- Soft Skills -->
        <section v-if="d.skills.soft.length" class="mr-section">
          <h2 class="mr-section-title"><span class="mr-section-icon">◈</span> Soft Skills</h2>
          <div class="mr-tags">
            <span v-for="s in d.skills.soft" :key="s" class="mr-tag">{{ s }}</span>
          </div>
        </section>

        <!-- Certifications -->
        <section v-if="d.certifications.length" class="mr-section">
          <h2 class="mr-section-title"><span class="mr-section-icon">◈</span> Certifications</h2>
          <div v-for="cert in d.certifications" :key="cert.id" class="mr-cert">
            <span class="mr-cert-name">{{ cert.name }}</span>
            <span class="mr-cert-meta">{{ cert.issuer }}<span v-if="cert.year"> · {{ cert.year }}</span></span>
          </div>
        </section>
      </div>

      <!-- Right Column -->
      <div class="mr-right">
        <!-- Experience -->
        <section v-if="d.experience.length" class="mr-section">
          <h2 class="mr-section-title"><span class="mr-section-icon">◈</span> Work Experience</h2>
          <div v-for="exp in d.experience" :key="exp.id" class="mr-timeline-entry">
            <div class="mr-timeline-dot"></div>
            <div class="mr-timeline-content">
              <div class="mr-entry-header">
                <span class="mr-entry-role">{{ exp.title || 'Job Title' }}</span>
                <span class="mr-entry-date">{{ exp.startDate }} – {{ exp.current ? 'Present' : exp.endDate }}</span>
              </div>
              <p class="mr-entry-org">{{ exp.company }}<span v-if="exp.location"> · {{ exp.location }}</span></p>
              <p class="mr-entry-desc">{{ exp.description }}</p>
            </div>
          </div>
        </section>

        <!-- Education -->
        <section v-if="d.education.length" class="mr-section">
          <h2 class="mr-section-title"><span class="mr-section-icon">◈</span> Education</h2>
          <div v-for="edu in d.education" :key="edu.id" class="mr-timeline-entry">
            <div class="mr-timeline-dot"></div>
            <div class="mr-timeline-content">
              <div class="mr-entry-header">
                <span class="mr-entry-role">{{ edu.degree || 'Degree' }}</span>
                <span class="mr-entry-date">{{ edu.startYear }} – {{ edu.endYear }}</span>
              </div>
              <p class="mr-entry-org">{{ edu.institution }}<span v-if="edu.location"> · {{ edu.location }}</span></p>
              <p v-if="edu.gpa" class="mr-entry-desc">GPA: {{ edu.gpa }}</p>
            </div>
          </div>
        </section>

        <!-- Projects -->
        <section v-if="d.projects.length" class="mr-section">
          <h2 class="mr-section-title"><span class="mr-section-icon">◈</span> Projects</h2>
          <div v-for="proj in d.projects" :key="proj.id" class="mr-project">
            <div class="mr-project-header">
              <span class="mr-project-name">{{ proj.name }}</span>
              <a v-if="proj.link" :href="proj.link" class="mr-project-link">{{ proj.link }}</a>
            </div>
            <p class="mr-entry-desc">{{ proj.description }}</p>
            <div v-if="proj.tech" class="mr-tags" style="margin-top:4px">
              <span v-for="t in proj.tech.split(',')" :key="t" class="mr-tag mr-tag--tech">{{ t.trim() }}</span>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ data: { type: Object, required: true } })
const d = computed(() => props.data)

const initials = computed(() => {
  const name = d.value.personal.fullName || ''
  return name.split(' ').slice(0, 2).map(w => w[0] || '').join('').toUpperCase() || '?'
})
</script>

<style scoped>
.modern-resume {
  font-family: 'Inter', 'Helvetica Neue', sans-serif;
  background: #fff;
  color: #1e293b;
  min-height: 1056px;
  font-size: 11.5px;
  line-height: 1.5;
}

/* Header */
.mr-header {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 60%, #0891b2 100%);
  padding: 28px 32px;
  color: white;
}

.mr-header__left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.mr-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(255,255,255,0.2);
  border: 2px solid rgba(255,255,255,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 800;
  color: white;
  flex-shrink: 0;
}

.mr-name {
  font-size: 22px;
  font-weight: 800;
  color: white;
  margin: 0;
  letter-spacing: -0.02em;
}

.mr-job-title {
  font-size: 11px;
  color: rgba(255,255,255,0.8);
  margin: 3px 0 8px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.mr-contact-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  font-size: 9.5px;
  color: rgba(255,255,255,0.85);
}

/* Body */
.mr-body {
  display: flex;
  min-height: calc(1056px - 110px);
}

.mr-left {
  width: 37%;
  background: #f8fafc;
  padding: 22px 18px;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.mr-right {
  flex: 1;
  padding: 22px 24px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

/* Sections */
.mr-section { display: flex; flex-direction: column; gap: 8px; }

.mr-section-title {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #4f46e5;
  display: flex;
  align-items: center;
  gap: 6px;
  padding-bottom: 4px;
  border-bottom: 1px solid #e0e7ff;
  margin: 0;
}

.mr-section-icon { font-size: 8px; }

.mr-summary {
  font-size: 10.5px;
  color: #475569;
  line-height: 1.7;
}

/* Skill Bars */
.mr-skill-bars { display: flex; flex-direction: column; gap: 5px; }

.mr-skill-bar {
  display: flex;
  align-items: center;
  gap: 8px;
}

.mr-skill-name {
  font-size: 10px;
  color: #334155;
  width: 90px;
  flex-shrink: 0;
  font-weight: 500;
}

.mr-skill-track {
  flex: 1;
  height: 4px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.mr-skill-fill {
  width: 75%;
  height: 100%;
  background: linear-gradient(90deg, #4f46e5, #7c3aed);
  border-radius: 4px;
}

/* Tags */
.mr-tags { display: flex; flex-wrap: wrap; gap: 4px; }

.mr-tag {
  background: #ede9fe;
  color: #5b21b6;
  border-radius: 3px;
  padding: 2px 7px;
  font-size: 9.5px;
  font-weight: 600;
}

.mr-tag--tech {
  background: #e0f2fe;
  color: #0369a1;
}

/* Certifications */
.mr-cert {
  display: flex;
  flex-direction: column;
  gap: 1px;
  padding: 5px 0;
  border-bottom: 1px solid #f1f5f9;
}
.mr-cert:last-child { border-bottom: none; }
.mr-cert-name { font-size: 10.5px; font-weight: 600; color: #1e293b; }
.mr-cert-meta { font-size: 9.5px; color: #64748b; }

/* Timeline */
.mr-timeline-entry {
  display: flex;
  gap: 10px;
  position: relative;
  padding-bottom: 10px;
  border-bottom: 1px dashed #e2e8f0;
}
.mr-timeline-entry:last-child { border-bottom: none; padding-bottom: 0; }

.mr-timeline-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #4f46e5;
  flex-shrink: 0;
  margin-top: 3px;
  box-shadow: 0 0 0 2px #e0e7ff;
}

.mr-timeline-content { flex: 1; display: flex; flex-direction: column; gap: 2px; }

.mr-entry-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}

.mr-entry-role {
  font-weight: 700;
  font-size: 11.5px;
  color: #1e293b;
}

.mr-entry-date {
  font-size: 9px;
  color: #94a3b8;
  white-space: nowrap;
}

.mr-entry-org {
  font-size: 10px;
  color: #4f46e5;
  font-style: italic;
}

.mr-entry-desc {
  font-size: 10.5px;
  color: #475569;
  line-height: 1.6;
  margin: 2px 0 0;
}

/* Projects */
.mr-project { display: flex; flex-direction: column; gap: 3px; padding-bottom: 8px; border-bottom: 1px dashed #e2e8f0; }
.mr-project:last-child { border-bottom: none; }
.mr-project-header { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
.mr-project-name { font-weight: 700; font-size: 11px; color: #1e293b; }
.mr-project-link { font-size: 9px; color: #4f46e5; word-break: break-all; }
</style>

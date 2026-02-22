<template>
  <div class="minimal-resume" id="resume-minimal">
    <!-- Header -->
    <header class="mn-header">
      <div>
        <h1 class="mn-name">{{ d.personal.fullName || 'Your Name' }}</h1>
        <p class="mn-job-title">{{ d.personal.jobTitle || 'Job Title' }}</p>
      </div>
      <div class="mn-contact">
        <span v-if="d.personal.email">{{ d.personal.email }}</span>
        <span class="mn-sep" v-if="d.personal.email && d.personal.phone">|</span>
        <span v-if="d.personal.phone">{{ d.personal.phone }}</span>
        <span class="mn-sep" v-if="d.personal.phone && d.personal.location">|</span>
        <span v-if="d.personal.location">{{ d.personal.location }}</span>
        <span class="mn-sep" v-if="d.personal.location && d.personal.linkedin">|</span>
        <span v-if="d.personal.linkedin">{{ d.personal.linkedin }}</span>
        <span class="mn-sep" v-if="d.personal.linkedin && d.personal.github">|</span>
        <span v-if="d.personal.github">{{ d.personal.github }}</span>
      </div>
    </header>

    <div class="mn-body">
      <!-- Summary -->
      <section v-if="d.summary" class="mn-section">
        <h2 class="mn-section-title">Summary</h2>
        <p class="mn-para">{{ d.summary }}</p>
      </section>

      <!-- Experience -->
      <section v-if="d.experience.length" class="mn-section">
        <h2 class="mn-section-title">Experience</h2>
        <div v-for="exp in d.experience" :key="exp.id" class="mn-entry">
          <div class="mn-entry-top">
            <div>
              <span class="mn-entry-role">{{ exp.title || 'Job Title' }}</span>
              <span class="mn-entry-at"> at </span>
              <span class="mn-entry-org">{{ exp.company || 'Company' }}</span>
              <span v-if="exp.location" class="mn-entry-loc">, {{ exp.location }}</span>
            </div>
            <span class="mn-entry-date">{{ exp.startDate }} – {{ exp.current ? 'Present' : exp.endDate }}</span>
          </div>
          <p class="mn-entry-desc">{{ exp.description }}</p>
        </div>
      </section>

      <!-- Education -->
      <section v-if="d.education.length" class="mn-section">
        <h2 class="mn-section-title">Education</h2>
        <div v-for="edu in d.education" :key="edu.id" class="mn-entry">
          <div class="mn-entry-top">
            <div>
              <span class="mn-entry-role">{{ edu.degree || 'Degree' }}</span>
              <span class="mn-entry-at"> — </span>
              <span class="mn-entry-org">{{ edu.institution || 'Institution' }}</span>
              <span v-if="edu.location" class="mn-entry-loc">, {{ edu.location }}</span>
            </div>
            <span class="mn-entry-date">{{ edu.startYear }} – {{ edu.endYear }}</span>
          </div>
          <p v-if="edu.gpa" class="mn-entry-desc">GPA: {{ edu.gpa }}</p>
        </div>
      </section>

      <!-- Skills -->
      <section v-if="d.skills.technical.length || d.skills.soft.length" class="mn-section">
        <h2 class="mn-section-title">Skills</h2>
        <div class="mn-skills-row">
          <div v-if="d.skills.technical.length">
            <span class="mn-skills-label">Technical: </span>
            <span class="mn-skills-list">{{ d.skills.technical.join(' · ') }}</span>
          </div>
          <div v-if="d.skills.soft.length">
            <span class="mn-skills-label">Soft: </span>
            <span class="mn-skills-list">{{ d.skills.soft.join(' · ') }}</span>
          </div>
        </div>
      </section>

      <!-- Projects -->
      <section v-if="d.projects.length" class="mn-section">
        <h2 class="mn-section-title">Projects</h2>
        <div v-for="proj in d.projects" :key="proj.id" class="mn-entry">
          <div class="mn-entry-top">
            <span class="mn-entry-role">{{ proj.name }}</span>
            <a v-if="proj.link" :href="proj.link" class="mn-proj-link">{{ proj.link }}</a>
          </div>
          <p class="mn-entry-desc">{{ proj.description }}</p>
          <p v-if="proj.tech" class="mn-entry-tech">
            <span class="mn-skills-label">Stack: </span>{{ proj.tech }}
          </p>
        </div>
      </section>

      <!-- Certifications -->
      <section v-if="d.certifications.length" class="mn-section">
        <h2 class="mn-section-title">Certifications</h2>
        <div v-for="cert in d.certifications" :key="cert.id" class="mn-entry mn-cert-entry">
          <span class="mn-entry-role">{{ cert.name }}</span>
          <span class="mn-entry-loc" v-if="cert.issuer"> — {{ cert.issuer }}</span>
          <span class="mn-entry-date mn-cert-year" v-if="cert.year">, {{ cert.year }}</span>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ data: { type: Object, required: true } })
const d = computed(() => props.data)
</script>

<style scoped>
.minimal-resume {
  font-family: 'Georgia', 'Times New Roman', serif;
  background: #ffffff;
  color: #111827;
  min-height: 1056px;
  font-size: 11.5px;
  line-height: 1.6;
  padding: 48px 52px;
}

/* Header */
.mn-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid #111827;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.mn-name {
  font-size: 26px;
  font-weight: 700;
  font-family: 'Georgia', serif;
  color: #111827;
  margin: 0;
  letter-spacing: -0.01em;
}

.mn-job-title {
  font-size: 11px;
  color: #6b7280;
  margin: 3px 0 0;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-family: 'Inter', sans-serif;
}

.mn-contact {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  font-size: 9.5px;
  color: #374151;
  font-family: 'Inter', sans-serif;
  text-align: right;
  justify-content: flex-end;
}

.mn-sep { color: #9ca3af; }

.mn-body { display: flex; flex-direction: column; gap: 20px; }

/* Section */
.mn-section { display: flex; flex-direction: column; gap: 8px; }

.mn-section-title {
  font-family: 'Inter', sans-serif;
  font-size: 9.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: #374151;
  padding-bottom: 3px;
  border-bottom: 1px solid #d1d5db;
  margin: 0;
}

.mn-para {
  font-size: 11px;
  color: #374151;
  line-height: 1.7;
}

/* Entry */
.mn-entry {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f3f4f6;
}
.mn-entry:last-child { border-bottom: none; padding-bottom: 0; }

.mn-entry-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
  flex-wrap: wrap;
}

.mn-entry-role { font-weight: 700; font-size: 11.5px; font-family: 'Inter', sans-serif; }
.mn-entry-at   { font-style: italic; color: #6b7280; }
.mn-entry-org  { font-style: italic; }
.mn-entry-loc  { color: #6b7280; }
.mn-entry-date { font-size: 9.5px; color: #6b7280; white-space: nowrap; font-family: 'Inter', sans-serif; }

.mn-entry-desc {
  font-size: 10.5px;
  color: #374151;
  line-height: 1.65;
}

.mn-entry-tech { font-size: 10px; color: #4b5563; margin: 0; }

/* Skills */
.mn-skills-row { display: flex; flex-direction: column; gap: 4px; }
.mn-skills-label { font-weight: 700; font-family: 'Inter', sans-serif; font-size: 10px; }
.mn-skills-list { color: #374151; }

/* Links */
.mn-proj-link { font-size: 9px; color: #2563eb; }

/* Cert */
.mn-cert-entry { flex-direction: row; flex-wrap: wrap; align-items: center; gap: 4px; }
.mn-cert-year { color: #6b7280; }
</style>

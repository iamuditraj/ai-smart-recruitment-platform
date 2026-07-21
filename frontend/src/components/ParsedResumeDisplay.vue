<template>
  <div class="parsed-resume-section animate-fade-in-up">
    <div class="parsed-resume-header">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/></svg>
      <h3 class="subsection-title" style="margin:0">AI Parsed Resume</h3>
      <span class="ai-badge">✦ Gemini</span>
    </div>

    <!-- Summary -->
    <div v-if="parsedResume.summary" class="parsed-block">
      <h4 class="parsed-label">Summary</h4>
      <p class="parsed-summary">{{ parsedResume.summary }}</p>
    </div>

    <!-- Skills -->
    <div v-if="parsedResume.skills?.length" class="parsed-block">
      <h4 class="parsed-label">Skills</h4>
      <div class="skills-chip-row">
        <span v-for="skill in parsedResume.skills" :key="skill" class="skill-chip">{{ skill }}</span>
      </div>
    </div>

    <!-- Experience -->
    <div v-if="parsedResume.experience?.length" class="parsed-block">
      <h4 class="parsed-label">Experience</h4>
      <div class="timeline">
        <div v-for="(exp, i) in parsedResume.experience" :key="i" class="timeline-item">
          <div class="timeline-dot"></div>
          <div class="timeline-content">
            <div class="timeline-title">{{ exp.title }}</div>
            <div class="timeline-meta">{{ exp.company }} <span v-if="exp.duration">· {{ exp.duration }}</span></div>
            <p v-if="exp.description" class="timeline-desc">{{ exp.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Education -->
    <div v-if="parsedResume.education?.length" class="parsed-block">
      <h4 class="parsed-label">Education</h4>
      <div class="edu-list">
        <div v-for="(edu, i) in parsedResume.education" :key="i" class="edu-item">
          <span class="edu-degree">{{ edu.degree }}</span>
          <span class="edu-meta">{{ edu.institution }}<span v-if="edu.year">, {{ edu.year }}</span></span>
        </div>
      </div>
    </div>

    <!-- Certifications -->
    <div v-if="parsedResume.certifications?.length" class="parsed-block">
      <h4 class="parsed-label">Certifications</h4>
      <ul class="cert-list">
        <li v-for="cert in parsedResume.certifications" :key="cert">{{ cert }}</li>
      </ul>
    </div>

    <!-- Languages -->
    <div v-if="parsedResume.languages?.length" class="parsed-block">
      <h4 class="parsed-label">Languages</h4>
      <div class="skills-chip-row">
        <span v-for="lang in parsedResume.languages" :key="lang" class="skill-chip skill-chip--lang">{{ lang }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  parsedResume: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.parsed-resume-section {
  background: linear-gradient(135deg, rgba(99,102,241,0.05), rgba(139,92,246,0.05));
  border: 1px solid rgba(99,102,241,0.15);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.parsed-resume-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--clr-primary);
}
.subsection-title {
  font-size: 1.2rem;
  font-weight: 700;
}
.ai-badge {
  margin-left: auto;
  background: var(--gradient-brand);
  color: #fff;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  padding: 3px 10px;
  border-radius: 999px;
}
.parsed-block {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.parsed-label {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--clr-primary);
  margin: 0;
}
.parsed-summary {
  font-size: 0.9rem;
  color: var(--clr-text);
  line-height: 1.6;
  margin: 0;
}
.skills-chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.skill-chip {
  background: rgba(99,102,241,0.1);
  color: var(--clr-primary);
  border: 1px solid rgba(99,102,241,0.2);
  border-radius: 999px;
  padding: 4px 12px;
  font-size: 0.8rem;
  font-weight: 600;
  white-space: nowrap;
}
.skill-chip--lang {
  background: rgba(16,185,129,0.08);
  color: var(--clr-success);
  border-color: rgba(16,185,129,0.2);
}
.timeline {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  padding-left: 1rem;
  border-left: 2px solid rgba(99,102,241,0.2);
}
.timeline-item {
  position: relative;
  display: flex;
  gap: 1rem;
}
.timeline-dot {
  position: absolute;
  left: -1.4rem;
  top: 4px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--clr-primary);
  border: 2px solid white;
  box-shadow: 0 0 0 2px rgba(99,102,241,0.3);
}
.timeline-content { flex: 1; }
.timeline-title {
  font-weight: 700;
  font-size: 0.9rem;
  color: var(--clr-text);
}
.timeline-meta {
  font-size: 0.8rem;
  color: var(--clr-text-muted);
  margin-top: 2px;
}
.timeline-desc {
  font-size: 0.85rem;
  color: var(--clr-text);
  margin: 4px 0 0;
  line-height: 1.5;
}
.edu-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.edu-item {
  display: flex;
  flex-direction: column;
  background: rgba(255,255,255,0.6);
  border: 1px solid rgba(99,102,241,0.1);
  border-radius: var(--radius-md);
  padding: 0.75rem 1rem;
}
.edu-degree {
  font-weight: 700;
  font-size: 0.9rem;
  color: var(--clr-text);
}
.edu-meta {
  font-size: 0.8rem;
  color: var(--clr-text-muted);
  margin-top: 2px;
}
.cert-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.cert-list li {
  font-size: 0.88rem;
  color: var(--clr-text);
  padding-left: 1rem;
  position: relative;
}
.cert-list li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: var(--clr-success);
  font-weight: 700;
}
</style>

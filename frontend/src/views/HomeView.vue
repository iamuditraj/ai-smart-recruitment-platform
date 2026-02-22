<template>
  <div class="home">
    <!-- Hero -->
    <section class="hero section">
      <div class="hero__bg-orb hero__bg-orb--1"></div>
      <div class="hero__bg-orb hero__bg-orb--2"></div>
      <div class="container hero__inner">
        <div class="hero__badge animate-fade-in-up">
          <span class="badge badge-primary">✨ AI-Powered Recruitment</span>
        </div>
        <h1 class="hero__title animate-fade-in-up" style="animation-delay:0.1s">
          Hire Smarter With<br />
          <span class="gradient-text">Artificial Intelligence</span>
        </h1>
        <p class="hero__subtitle animate-fade-in-up" style="animation-delay:0.2s">
          Automate resume screening, rank candidates using NLP, assess skills early,
          and analyze mock interviews — all in one intelligent platform.
        </p>
        <div class="hero__actions animate-fade-in-up" style="animation-delay:0.3s">
          <RouterLink to="/resume-screening" class="btn btn-primary" id="hero-cta-primary">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
            Upload Resume
          </RouterLink>
          <RouterLink to="/dashboard" class="btn btn-outline" id="hero-cta-secondary">
            View Dashboard
          </RouterLink>
        </div>
        <!-- Stats -->
        <div class="hero__stats animate-fade-in-up" style="animation-delay:0.4s">
          <div v-for="s in stats" :key="s.label" class="hero__stat">
            <span class="hero__stat-value gradient-text">{{ s.value }}</span>
            <span class="hero__stat-label">{{ s.label }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="features section">
      <div class="container">
        <div class="section-header text-center">
          <span class="badge badge-primary">Core Modules</span>
          <h2 class="section-title">Everything You Need to Hire Better</h2>
          <p class="section-subtitle">
            Our end-to-end platform handles every stage of the recruitment pipeline.
          </p>
        </div>
        <div class="features__grid">
          <div v-for="(feature, i) in features" :key="feature.title" class="feature-card card" :style="`animation-delay:${i * 0.08}s`">
            <div class="feature-card__icon" :style="`background: ${feature.gradient}`">
              <span v-html="feature.icon"></span>
            </div>
            <h3 class="feature-card__title">{{ feature.title }}</h3>
            <p class="feature-card__desc">{{ feature.desc }}</p>
            <RouterLink :to="feature.link" class="feature-card__link" :id="`feature-link-${i}`">
              Explore →
            </RouterLink>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works -->
    <section class="how-it-works section">
      <div class="container">
        <div class="section-header text-center">
          <span class="badge badge-primary">Process</span>
          <h2 class="section-title">How HireAI Works</h2>
        </div>
        <div class="steps">
          <div v-for="(step, i) in steps" :key="step.title" class="step">
            <div class="step__connector" v-if="i < steps.length - 1"></div>
            <div class="step__number">{{ i + 1 }}</div>
            <h3 class="step__title">{{ step.title }}</h3>
            <p class="step__desc">{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Banner -->
    <section class="cta-banner section">
      <div class="container">
        <div class="cta-banner__inner">
          <div class="cta-banner__bg-orb"></div>
          <h2 class="cta-banner__title">Ready to Transform Your Hiring?</h2>
          <p class="cta-banner__subtitle">Start screening smarter — upload your first resume in seconds.</p>
          <RouterLink to="/resume-screening" class="btn btn-primary" id="cta-banner-btn">
            Start for Free
          </RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
const stats = [
  { value: '10×', label: 'Faster Screening' },
  { value: '95%', label: 'Match Accuracy' },
  { value: '3 Modules', label: 'AI-Powered' },
]

const features = [
  {
    title: 'Resume Screening',
    desc: 'Upload resumes in bulk. Our NLP engine parses, extracts skills, and scores candidates against your job description instantly.',
    icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="13" x2="15" y2="13"/><line x1="9" y1="17" x2="12" y2="17"/></svg>`,
    gradient: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
    link: '/resume-screening',
  },
  {
    title: 'Candidate Ranking',
    desc: 'AI-driven scoring ranks candidates by skill relevance, experience match, and profile completeness — removing human bias.',
    icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><polyline points="18 15 12 9 6 15"/><line x1="12" y1="9" x2="12" y2="22"/><path d="M3 4h18"/></svg>`,
    gradient: 'linear-gradient(135deg, #8b5cf6, #ec4899)',
    link: '/candidates',
  },
  {
    title: 'Skill Assessment',
    desc: 'Automatically generate role-specific technical tests. Evaluate skills early in the pipeline to save interviewer time and cost.',
    icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>`,
    gradient: 'linear-gradient(135deg, #06b6d4, #6366f1)',
    link: '/skill-assessment',
  },
  {
    title: 'Mock Interview Analysis',
    desc: 'Camera-based AI analysis evaluates body language, speech clarity, and confidence during mock interviews to prepare candidates.',
    icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>`,
    gradient: 'linear-gradient(135deg, #10b981, #06b6d4)',
    link: '/dashboard',
  },
]

const steps = [
  { title: 'Upload Resumes', desc: 'Upload candidate resumes in PDF or DOCX format. Supports bulk uploads.' },
  { title: 'AI Parsing & Scoring', desc: 'NLP engine extracts skills, experience, and education. Scores against the job description.' },
  { title: 'Rank & Filter', desc: 'View ranked candidates on the dashboard. Filter by score, skills, or assessment results.' },
  { title: 'Assess & Interview', desc: 'Shortlisted candidates take skill assessments and mock interviews before final rounds.' },
]
</script>

<style scoped>
/* Hero */
.hero {
  position: relative;
  overflow: hidden;
  padding-top: var(--sp-20);
  padding-bottom: var(--sp-20);
}

.hero__bg-orb {
  position: absolute;
  border-radius: var(--radius-full);
  filter: blur(80px);
  pointer-events: none;
  z-index: 0;
}

.hero__bg-orb--1 {
  width: 500px;
  height: 500px;
  background: rgba(99, 102, 241, 0.15);
  top: -150px;
  left: -100px;
}

.hero__bg-orb--2 {
  width: 400px;
  height: 400px;
  background: rgba(6, 182, 212, 0.1);
  bottom: -100px;
  right: -100px;
}

.hero__inner {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--sp-6);
}

.hero__title {
  font-size: clamp(2.5rem, 6vw, 4.5rem);
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.1;
  max-width: 800px;
}

.hero__subtitle {
  font-size: clamp(1rem, 2vw, 1.2rem);
  color: var(--clr-text-light);
  max-width: 600px;
  line-height: 1.7;
}

.hero__actions {
  display: flex;
  gap: var(--sp-4);
  flex-wrap: wrap;
  justify-content: center;
}

.hero__stats {
  display: flex;
  gap: var(--sp-12);
  margin-top: var(--sp-4);
  flex-wrap: wrap;
  justify-content: center;
}

.hero__stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--sp-1);
}

.hero__stat-value {
  font-family: var(--font-heading);
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.hero__stat-label {
  font-size: 0.85rem;
  color: var(--clr-text-muted);
  font-weight: 500;
}

/* Section Header */
.section-header {
  margin-bottom: var(--sp-12);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--sp-4);
}

.section-title {
  font-size: clamp(1.8rem, 4vw, 2.8rem);
  letter-spacing: -0.02em;
  max-width: 600px;
}

.section-subtitle {
  color: var(--clr-text-light);
  font-size: 1.05rem;
  max-width: 500px;
  line-height: 1.7;
}

/* Features */
.features {
  background: linear-gradient(180deg, transparent, rgba(16,20,31,0.8), transparent);
}

.features__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: var(--sp-6);
}

.feature-card {
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
  animation: fade-in-up 0.6s ease both;
}

.feature-card__icon {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.feature-card__title {
  font-size: 1.1rem;
  font-weight: 700;
}

.feature-card__desc {
  color: var(--clr-text-light);
  font-size: 0.9rem;
  line-height: 1.7;
  flex: 1;
}

.feature-card__link {
  color: var(--clr-primary);
  font-size: 0.9rem;
  font-weight: 600;
  transition: gap var(--transition-fast);
}

.feature-card__link:hover {
  color: var(--clr-accent);
}

/* How It Works */
.how-it-works {
  position: relative;
}

.steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--sp-8);
  position: relative;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--sp-4);
  position: relative;
}

.step__number {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-full);
  background: var(--gradient-brand);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-heading);
  font-size: 1.2rem;
  font-weight: 800;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 0 24px rgba(99,102,241,0.4);
}

.step__title {
  font-size: 1rem;
  font-weight: 700;
}

.step__desc {
  color: var(--clr-text-light);
  font-size: 0.875rem;
  line-height: 1.7;
}

/* CTA Banner */
.cta-banner__inner {
  position: relative;
  background: var(--clr-surface-2);
  border: 1px solid var(--clr-border-hover);
  border-radius: var(--radius-xl);
  padding: var(--sp-16) var(--sp-8);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--sp-6);
  overflow: hidden;
}

.cta-banner__bg-orb {
  position: absolute;
  width: 400px;
  height: 400px;
  background: var(--gradient-glow);
  border-radius: var(--radius-full);
  filter: blur(60px);
  pointer-events: none;
}

.cta-banner__title {
  font-size: clamp(1.6rem, 3.5vw, 2.5rem);
  letter-spacing: -0.02em;
  position: relative;
}

.cta-banner__subtitle {
  color: var(--clr-text-light);
  font-size: 1.05rem;
  position: relative;
}

@media (max-width: 600px) {
  .hero__stats {
    gap: var(--sp-8);
  }
  .steps {
    grid-template-columns: 1fr;
  }
}
</style>

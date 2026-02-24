<template>
  <div class="review-step" id="review-step">

    <!-- ── Header ─────────────────────────────────────────────────── -->
    <div class="rs-header">
      <div>
        <h2 class="step-title">Review &amp; Export</h2>
        <p class="step-desc">Verify your structured data before exporting or submitting to AI modules.</p>
      </div>
    </div>

    <!-- ── Completeness Gauge ──────────────────────────────────────── -->
    <div class="rs-gauge-row" id="rs-completeness-panel">
      <div class="rs-gauge-circle" :class="gaugeClass">
        <svg viewBox="0 0 100 100" width="90" height="90">
          <circle cx="50" cy="50" r="42" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="10"/>
          <circle
            cx="50" cy="50" r="42"
            fill="none"
            :stroke="gaugeColor"
            stroke-width="10"
            stroke-linecap="round"
            :stroke-dasharray="`${circumference}`"
            :stroke-dashoffset="dashOffset"
            transform="rotate(-90 50 50)"
            style="transition: stroke-dashoffset 0.7s ease;"
          />
        </svg>
        <div class="rs-gauge-inner">
          <span class="rs-gauge-score">{{ score }}</span>
          <span class="rs-gauge-label">/ 100</span>
        </div>
      </div>

      <div class="rs-breakdown-grid">
        <div
          v-for="(sec, key) in breakdown"
          :key="key"
          class="rs-breakdown-item"
          :id="`rs-breakdown-${key}`"
        >
          <div class="rs-bd-top">
            <span class="rs-bd-icon">{{ sec.icon }}</span>
            <span class="rs-bd-label">{{ sec.label }}</span>
            <span class="rs-bd-pts">{{ sec.score }}/{{ sec.max }}</span>
          </div>
          <div class="rs-bd-bar">
            <div
              class="rs-bd-fill"
              :style="{ width: `${(sec.score / sec.max) * 100}%`, background: sectionColor(sec.score, sec.max) }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Validation ─────────────────────────────────────────────── -->
    <div v-if="validation.errors.length || validation.warnings.length" class="rs-validation">
      <!-- Errors -->
      <div v-if="validation.errors.length" class="rs-issue-group" id="rs-errors-panel">
        <div class="rs-issue-group__title rs-error-title">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          {{ validation.errors.length }} Error{{ validation.errors.length > 1 ? 's' : '' }} — must fix before export
        </div>
        <ul class="rs-issue-list">
          <li v-for="err in validation.errors" :key="err.field" class="rs-issue rs-issue--error">
            <code class="rs-field-tag">{{ err.field }}</code>
            <span>{{ err.message }}</span>
          </li>
        </ul>
      </div>

      <!-- Warnings -->
      <div v-if="validation.warnings.length" class="rs-issue-group" id="rs-warnings-panel">
        <div class="rs-issue-group__title rs-warn-title">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          {{ validation.warnings.length }} Suggestion{{ validation.warnings.length > 1 ? 's' : '' }}
        </div>
        <ul class="rs-issue-list">
          <li v-for="warn in validation.warnings" :key="warn.field" class="rs-issue rs-issue--warn">
            <code class="rs-field-tag rs-field-tag--warn">{{ warn.field }}</code>
            <span>{{ warn.message }}</span>
          </li>
        </ul>
      </div>
    </div>

    <div v-else class="rs-all-good" id="rs-all-good">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
      No validation errors. Your resume is ready to export.
    </div>

    <!-- ── Module Readiness ────────────────────────────────────────── -->
    <div class="rs-modules" id="rs-module-readiness">
      <p class="rs-modules__label">Ready for Platform Modules</p>
      <div class="rs-modules__badges">
        <span
          v-for="label in validation.readyForLabels"
          :key="label"
          class="rs-module-badge"
        >
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
          {{ label }}
        </span>
        <span
          v-if="!validation.readyForLabels?.length"
          class="rs-module-badge rs-module-badge--none"
        >
          Complete required fields to enable modules
        </span>
      </div>
    </div>

    <!-- ── Computed Highlights ────────────────────────────────────── -->
    <div class="rs-computed-grid" id="rs-computed-highlights">
      <div class="rs-computed-card">
        <span class="rs-computed-icon">⏱</span>
        <div>
          <span class="rs-computed-value">{{ structured.computed.total_experience_years }} yrs</span>
          <span class="rs-computed-meta">Total Experience</span>
        </div>
      </div>
      <div class="rs-computed-card">
        <span class="rs-computed-icon">🎓</span>
        <div>
          <span class="rs-computed-value rs-computed-value--cap">{{ structured.computed.education_level }}</span>
          <span class="rs-computed-meta">Highest Degree</span>
        </div>
      </div>
      <div class="rs-computed-card">
        <span class="rs-computed-icon">⚡</span>
        <div>
          <span class="rs-computed-value">{{ structured.computed.all_tech_stack.length }}</span>
          <span class="rs-computed-meta">Tech Skills</span>
        </div>
      </div>
      <div class="rs-computed-card">
        <span class="rs-computed-icon">🆔</span>
        <div>
          <span class="rs-computed-value rs-id-value">{{ structured.metadata.resume_id }}</span>
          <span class="rs-computed-meta">Resume ID</span>
        </div>
      </div>
    </div>

    <!-- ── Export Actions ──────────────────────────────────────────── -->
    <div class="rs-export-panel" id="rs-export-panel">
      <div class="rs-export-title">Export Structured Data</div>
      <div class="rs-export-actions">
        <button class="btn btn-primary rs-export-btn" id="rs-btn-download-json" @click="onDownloadJSON">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          Download JSON
        </button>
        <button
          class="btn rs-copy-btn"
          :class="clipboardStatus === 'copied' ? 'btn-success' : 'btn-outline'"
          id="rs-btn-copy-json"
          @click="onCopyJSON"
        >
          <svg v-if="clipboardStatus !== 'copied'" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
          <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
          {{ clipboardStatus === 'copied' ? 'Copied!' : clipboardStatus === 'error' ? 'Error' : 'Copy JSON' }}
        </button>
        <button class="btn btn-outline rs-export-btn" id="rs-btn-download-pdf" @click="$emit('print')">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
          Download PDF
        </button>
      </div>
    </div>

    <!-- ── JSON Preview (collapsible) ─────────────────────────────── -->
    <div class="rs-json-panel" id="rs-json-preview">
      <button class="rs-json-toggle" @click="showJSON = !showJSON" id="rs-json-toggle-btn">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
          :style="{ transform: showJSON ? 'rotate(90deg)' : 'rotate(0deg)', transition: 'transform 0.2s' }">
          <polyline points="9 18 15 12 9 6"/>
        </svg>
        <span>{{ showJSON ? 'Hide' : 'View' }} Structured JSON</span>
        <span class="rs-json-meta">schema v{{ structured.schema_version }}</span>
      </button>

      <Transition name="rs-collapse">
        <div v-if="showJSON" class="rs-json-body">
          <pre class="rs-json-code" id="rs-json-content">{{ prettyJSON }}</pre>
        </div>
      </Transition>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useResumeExport } from '../../composables/useResumeExport.js'

const props = defineProps({
  structured:  { type: Object, required: true },
  validation:  { type: Object, required: true },
  breakdown:   { type: Object, required: true },
  score:       { type: Number, required: true },
})

const emit = defineEmits(['print'])

const { clipboardStatus, downloadJSON, copyToClipboard } = useResumeExport()
const showJSON = ref(false)

// ── SVG gauge ──────────────────────────────────────────────────────────────
const circumference = Math.round(2 * Math.PI * 42)  // ≈ 264px
const dashOffset = computed(() =>
  circumference - (props.score / 100) * circumference
)
const gaugeColor = computed(() => {
  if (props.score >= 80) return '#10b981'
  if (props.score >= 50) return '#f59e0b'
  return '#ef4444'
})
const gaugeClass = computed(() => ({
  'rs-gauge--good': props.score >= 80,
  'rs-gauge--mid':  props.score >= 50 && props.score < 80,
  'rs-gauge--low':  props.score < 50,
}))

// ── Section bar colours ──────────────────────────────────────────────────────
function sectionColor(score, max) {
  const pct = score / max
  if (pct >= 0.8) return 'var(--clr-success)'
  if (pct >= 0.5) return '#f59e0b'
  if (pct >  0)   return '#f97316'
  return 'rgba(255,255,255,0.1)'
}

// ── Export handlers ──────────────────────────────────────────────────────────
function onDownloadJSON() { downloadJSON(props.structured) }
function onCopyJSON()     { copyToClipboard(props.structured) }

// ── JSON preview ─────────────────────────────────────────────────────────────
const prettyJSON = computed(() =>
  JSON.stringify(props.structured, null, 2)
)
</script>

<style scoped>
.review-step {
  display: flex;
  flex-direction: column;
  gap: var(--sp-5);
}

.rs-header { display: flex; align-items: flex-start; justify-content: space-between; flex-wrap: wrap; gap: var(--sp-3); }

/* ── Gauge ── */
.rs-gauge-row {
  display: flex;
  align-items: center;
  gap: var(--sp-6);
  flex-wrap: wrap;
}

.rs-gauge-circle {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.rs-gauge-inner {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.rs-gauge-score {
  font-size: 1.4rem;
  font-weight: 800;
  line-height: 1;
}

.rs-gauge-label {
  font-size: 0.7rem;
  color: var(--clr-text-muted);
}

.rs-gauge--good .rs-gauge-score { color: #10b981; }
.rs-gauge--mid  .rs-gauge-score { color: #f59e0b; }
.rs-gauge--low  .rs-gauge-score { color: #ef4444; }

/* Breakdown grid */
.rs-breakdown-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--sp-2) var(--sp-4);
  flex: 1;
  min-width: 220px;
}

.rs-breakdown-item { display: flex; flex-direction: column; gap: 4px; }

.rs-bd-top {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  font-size: 0.78rem;
}

.rs-bd-icon  { font-size: 0.9rem; }
.rs-bd-label { flex: 1; color: var(--clr-text-light); font-weight: 600; }
.rs-bd-pts   { color: var(--clr-text-muted); font-size: 0.72rem; font-weight: 700; }

.rs-bd-bar  {
  height: 5px;
  background: rgba(255,255,255,0.07);
  border-radius: var(--radius-full);
  overflow: hidden;
}
.rs-bd-fill {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width 0.6s ease;
}

/* ── Validation ── */
.rs-validation { display: flex; flex-direction: column; gap: var(--sp-3); }

.rs-issue-group {
  background: var(--clr-surface);
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--clr-border);
}

.rs-issue-group__title {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  padding: var(--sp-3) var(--sp-4);
  font-size: 0.8rem;
  font-weight: 700;
}

.rs-error-title { background: rgba(239,68,68,0.08); color: #f87171; border-bottom: 1px solid rgba(239,68,68,0.15); }
.rs-warn-title  { background: rgba(245,158,11,0.08); color: #fbbf24; border-bottom: 1px solid rgba(245,158,11,0.15); }

.rs-issue-list {
  list-style: none;
  margin: 0;
  padding: var(--sp-3) var(--sp-4);
  display: flex;
  flex-direction: column;
  gap: var(--sp-2);
}

.rs-issue {
  display: flex;
  align-items: flex-start;
  gap: var(--sp-2);
  font-size: 0.82rem;
  color: var(--clr-text-light);
  line-height: 1.5;
}

.rs-field-tag {
  font-family: 'Fira Code', monospace, monospace;
  font-size: 0.72rem;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
  background: rgba(239,68,68,0.12);
  color: #fca5a5;
  white-space: nowrap;
  flex-shrink: 0;
}

.rs-field-tag--warn {
  background: rgba(245,158,11,0.12);
  color: #fcd34d;
}

.rs-all-good {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  background: rgba(16,185,129,0.08);
  border: 1px solid rgba(16,185,129,0.2);
  border-radius: var(--radius-md);
  padding: var(--sp-3) var(--sp-4);
  font-size: 0.85rem;
  color: #34d399;
  font-weight: 600;
}

/* ── Module Readiness ── */
.rs-modules {
  display: flex;
  flex-direction: column;
  gap: var(--sp-2);
}

.rs-modules__label {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--clr-text-muted);
}

.rs-modules__badges {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sp-2);
}

.rs-module-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(99,102,241,0.1);
  border: 1px solid rgba(99,102,241,0.25);
  border-radius: var(--radius-full);
  padding: 0.25rem 0.7rem;
  font-size: 0.78rem;
  font-weight: 600;
  color: #a5b4fc;
}

.rs-module-badge--none {
  background: rgba(255,255,255,0.04);
  border-color: var(--clr-border);
  color: var(--clr-text-muted);
}

/* ── Computed Highlights ── */
.rs-computed-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--sp-3);
}

@media (max-width: 700px) {
  .rs-computed-grid { grid-template-columns: repeat(2, 1fr); }
  .rs-breakdown-grid { grid-template-columns: 1fr; }
}

.rs-computed-card {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-md);
  padding: var(--sp-3) var(--sp-4);
}

.rs-computed-icon { font-size: 1.4rem; flex-shrink: 0; }

.rs-computed-card > div {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.rs-computed-value {
  font-size: 1rem;
  font-weight: 800;
  line-height: 1.2;
  color: var(--clr-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.rs-computed-value--cap { text-transform: capitalize; }

.rs-id-value {
  font-family: 'Fira Code', monospace, monospace;
  font-size: 0.65rem;
  color: #a5b4fc;
  letter-spacing: 0.02em;
}

.rs-computed-meta {
  font-size: 0.7rem;
  color: var(--clr-text-muted);
  margin-top: 2px;
}

/* ── Export Panel ── */
.rs-export-panel {
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-md);
  padding: var(--sp-4) var(--sp-5);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-4);
  flex-wrap: wrap;
}

.rs-export-title {
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--clr-text-light);
}

.rs-export-actions {
  display: flex;
  gap: var(--sp-2);
  flex-wrap: wrap;
}

.rs-export-btn, .rs-copy-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.82rem;
}

.btn-success {
  background: var(--clr-success);
  color: white;
  border: 1px solid transparent;
}

/* ── JSON Preview ── */
.rs-json-panel {
  background: var(--clr-surface);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.rs-json-toggle {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  width: 100%;
  padding: var(--sp-3) var(--sp-4);
  background: none;
  border: none;
  cursor: pointer;
  font-family: var(--font-body);
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--clr-text-muted);
  text-align: left;
  transition: color var(--transition-fast);
}

.rs-json-toggle:hover { color: var(--clr-text); }

.rs-json-meta {
  margin-left: auto;
  font-size: 0.7rem;
  font-family: 'Fira Code', monospace;
  background: rgba(99,102,241,0.1);
  border: 1px solid rgba(99,102,241,0.2);
  border-radius: 4px;
  padding: 0.1rem 0.4rem;
  color: #a5b4fc;
}

.rs-json-body {
  border-top: 1px solid var(--clr-border);
  max-height: 360px;
  overflow-y: auto;
}

.rs-json-code {
  font-family: 'Fira Code', 'Consolas', monospace;
  font-size: 0.72rem;
  line-height: 1.6;
  color: #a5f3fc;
  padding: var(--sp-4);
  margin: 0;
  white-space: pre;
  background: rgba(6,12,27,0.5);
}

/* Collapse transition */
.rs-collapse-enter-active, .rs-collapse-leave-active {
  overflow: hidden;
  transition: max-height 0.28s ease, opacity 0.25s;
}
.rs-collapse-enter-from, .rs-collapse-leave-to {
  max-height: 0;
  opacity: 0;
}
.rs-collapse-enter-to, .rs-collapse-leave-from {
  max-height: 400px;
  opacity: 1;
}
</style>

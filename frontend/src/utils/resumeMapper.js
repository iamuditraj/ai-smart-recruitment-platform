/**
 * resumeMapper.js
 *
 * Transforms raw Pinia formData (user input) into the canonical
 * structured resume format defined in resumeSchema.js.
 *
 * This is the single transformation boundary — no other module
 * should read formData directly for processing purposes.
 */

import { SCHEMA_VERSION, COMPLETENESS_WEIGHTS } from '../schemas/resumeSchema.js'

// ─── Tech Keyword Dictionary ─────────────────────────────────────────────────
// Used for lightweight client-side keyword extraction from free-text fields.
const TECH_KEYWORDS = new Set([
    // Languages
    'python', 'javascript', 'typescript', 'java', 'kotlin', 'swift', 'go', 'rust', 'c', 'c++', 'c#',
    'ruby', 'php', 'scala', 'r', 'matlab', 'perl', 'dart', 'elixir', 'clojure', 'haskell',
    // Web
    'react', 'vue', 'angular', 'svelte', 'html', 'css', 'sass', 'tailwind', 'bootstrap', 'jquery',
    'nextjs', 'nuxt', 'gatsby', 'remix', 'astro', 'vite', 'webpack', 'vite',
    // Backend
    'nodejs', 'node.js', 'fastapi', 'flask', 'django', 'spring', 'express', 'rails', 'laravel',
    'nestjs', 'graphql', 'rest', 'grpc', 'websocket',
    // ML / AI
    'tensorflow', 'pytorch', 'keras', 'sklearn', 'scikit-learn', 'huggingface', 'transformers',
    'bert', 'gpt', 'llm', 'nlp', 'opencv', 'spacy', 'nltk', 'pandas', 'numpy', 'scipy',
    'xgboost', 'lightgbm', 'rapids', 'onnx', 'mlflow', 'kubeflow', 'wandb',
    // Data
    'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'sqlite', 'cassandra',
    'bigquery', 'spark', 'hadoop', 'kafka', 'airflow', 'dbt', 'snowflake', 'databricks',
    // Cloud / DevOps
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'ansible', 'jenkins', 'github',
    'gitlab', 'ci/cd', 'linux', 'bash', 'nginx', 'prometheus', 'grafana',
    // Mobile
    'android', 'ios', 'flutter', 'react native', 'xamarin',
])

// ─── Helpers ─────────────────────────────────────────────────────────────────

/** Generate a UUID-like unique ID */
function generateResumeId() {
    const hex = () => Math.floor(Math.random() * 0xffff).toString(16).padStart(4, '0')
    return `rsm-${hex()}-${hex()}-${hex()}-${hex()}`
}

/**
 * Compute duration in months between two YYYY-MM strings.
 * If endDate is null/empty and isCurrent is true, uses today.
 *
 * @param {string}  startDate - 'YYYY-MM'
 * @param {string}  endDate   - 'YYYY-MM' or ''
 * @param {boolean} isCurrent
 * @returns {number} months (≥ 0)
 */
function computeDurationMonths(startDate, endDate, isCurrent) {
    if (!startDate) return 0
    const start = new Date(startDate + '-01')
    const end = (isCurrent || !endDate)
        ? new Date()
        : new Date(endDate + '-01')
    const months = (end.getFullYear() - start.getFullYear()) * 12
        + (end.getMonth() - start.getMonth())
    return Math.max(0, months)
}

/**
 * Infer education level from a degree string.
 *
 * @param {string} degree
 * @returns {'phd'|'master'|'bachelor'|'diploma'|'high_school'|'other'}
 */
function inferEducationLevel(degree) {
    const d = (degree || '').toLowerCase()
    if (/\b(phd|ph\.d|doctorate|doctor of)\b/.test(d)) return 'phd'
    if (/\b(master|m\.tech|mtech|msc|m\.sc|mba|mca|m\.e\b|m\.s\b|ms\b)\b/.test(d)) return 'master'
    if (/\b(bachelor|b\.tech|btech|bsc|b\.sc|be\b|b\.e\b|ba\b|bca|bcom|engineering|b\.eng)\b/.test(d)) return 'bachelor'
    if (/\b(diploma|certificate course|pgdip|pgd)\b/.test(d)) return 'diploma'
    if (/\b(12th|hsc|10\+2|intermediate|a-level|high school)\b/.test(d)) return 'high_school'
    return 'other'
}

/**
 * Extract technology keywords from a block of free text.
 * Returns an array of matched keywords (lowercase, deduplicated).
 *
 * @param {string} text
 * @returns {string[]}
 */
function extractKeywords(text) {
    if (!text) return []
    const tokens = text
        .toLowerCase()
        .replace(/[^a-z0-9+#./\s-]/g, ' ')
        .split(/\s+/)
    const found = new Set()
    for (const token of tokens) {
        if (TECH_KEYWORDS.has(token)) found.add(token)
        // Also try multi-word: check pairs
    }
    // Check bigrams for things like "react native", "ci/cd", "node.js"
    const words = text.toLowerCase().split(/\s+/)
    for (let i = 0; i < words.length - 1; i++) {
        const bigram = words[i] + ' ' + words[i + 1]
        if (TECH_KEYWORDS.has(bigram)) found.add(bigram)
    }
    return Array.from(found)
}

/**
 * Parse a comma-separated tech string into a clean array.
 *
 * @param {string} techStr
 * @returns {string[]}
 */
function parseTechStack(techStr) {
    if (!techStr) return []
    return techStr
        .split(',')
        .map(t => t.trim())
        .filter(Boolean)
}

// ─── Completeness Scoring ─────────────────────────────────────────────────────

/**
 * Compute per-section completeness scores and overall weighted total.
 *
 * Scoring strategy:
 *  • personal  (20 pts): name + jobtitle = 10, email = 5, phone/location = 5
 *  • summary   (15 pts): present & ≥ 50 chars = 15, present < 50 = 7
 *  • experience(25 pts): 1 entry = 15, 2+ entries with description = 25
 *  • education (15 pts): 1 entry with degree + institution = 15
 *  • skills    (15 pts): ≥ 5 tech skills = 15, 1–4 = 8
 *  • projects  (10 pts): 1 project or 1 cert = 5, both or 2+ = 10
 *
 * @param {Object} d - raw formData
 * @returns {{ breakdown: Object, total: number }}
 */
function computeCompleteness(d) {
    const breakdown = {}

    // Personal (20)
    let personal = 0
    if (d.personal.fullName?.trim() && d.personal.jobTitle?.trim()) personal += 10
    else if (d.personal.fullName?.trim() || d.personal.jobTitle?.trim()) personal += 5
    if (d.personal.email?.trim()) personal += 5
    if (d.personal.phone?.trim() || d.personal.location?.trim()) personal += 5
    breakdown.personal = { score: personal, max: COMPLETENESS_WEIGHTS.personal.weight, ...COMPLETENESS_WEIGHTS.personal }

    // Summary (15)
    let summary = 0
    const summaryLen = (d.summary || '').trim().length
    if (summaryLen >= 100) summary = 15
    else if (summaryLen >= 50) summary = 10
    else if (summaryLen > 0) summary = 5
    breakdown.summary = { score: summary, max: COMPLETENESS_WEIGHTS.summary.weight, ...COMPLETENESS_WEIGHTS.summary }

    // Experience (25)
    let experience = 0
    const expFull = d.experience.filter(e => e.title?.trim() && e.company?.trim())
    if (expFull.length >= 2 && expFull.some(e => e.description?.trim())) experience = 25
    else if (expFull.length >= 1 && expFull[0].description?.trim()) experience = 20
    else if (expFull.length >= 1) experience = 12
    breakdown.experience = { score: experience, max: COMPLETENESS_WEIGHTS.experience.weight, ...COMPLETENESS_WEIGHTS.experience }

    // Education (15)
    let education = 0
    const eduFull = d.education.filter(e => e.degree?.trim() && e.institution?.trim())
    if (eduFull.length >= 1) education = 15
    breakdown.education = { score: education, max: COMPLETENESS_WEIGHTS.education.weight, ...COMPLETENESS_WEIGHTS.education }

    // Skills (15)
    let skills = 0
    const techCount = d.skills.technical.length
    if (techCount >= 8) skills = 15
    else if (techCount >= 5) skills = 12
    else if (techCount >= 3) skills = 8
    else if (techCount >= 1) skills = 4
    breakdown.skills = { score: skills, max: COMPLETENESS_WEIGHTS.skills.weight, ...COMPLETENESS_WEIGHTS.skills }

    // Projects + Certifications (10)
    let projects = 0
    const projFull = d.projects.filter(p => p.name?.trim())
    const certFull = d.certifications.filter(c => c.name?.trim())
    if (projFull.length >= 2 || (projFull.length >= 1 && certFull.length >= 1)) projects = 10
    else if (projFull.length >= 1 || certFull.length >= 1) projects = 5
    breakdown.projects = { score: projects, max: COMPLETENESS_WEIGHTS.projects.weight, ...COMPLETENESS_WEIGHTS.projects }

    const total = Object.values(breakdown).reduce((sum, s) => sum + s.score, 0)
    return { breakdown, total }
}

// ─── Main Mapper ──────────────────────────────────────────────────────────────

/**
 * mapToStructuredResume
 *
 * Transforms raw Pinia formData into the canonical structured resume object.
 * This is the primary function consumed by the store, export utilities, and
 * downstream processing modules (screening, ranking, assessment).
 *
 * @param {Object} formData - raw reactive formData from useResumeStore
 * @param {string} [existingId] - preserve existing resume_id on updates
 * @returns {Object} Canonical structured resume (matches ResumeSchema)
 */
export function mapToStructuredResume(formData, existingId = null) {
    const now = new Date().toISOString()

    // ── Experience ──────────────────────────────────────────────────────────
    const experience = formData.experience
        .filter(e => e.title?.trim() || e.company?.trim())
        .map(e => {
            const duration = computeDurationMonths(e.startDate, e.endDate, e.current)
            return {
                id: e.id,
                title: e.title?.trim() || '',
                company: e.company?.trim() || '',
                location: e.location?.trim() || '',
                start_date: e.startDate || null,
                end_date: e.current ? null : (e.endDate || null),
                is_current: Boolean(e.current),
                duration_months: duration,
                description: e.description?.trim() || '',
                keywords: extractKeywords(e.description),
            }
        })

    // ── Education ───────────────────────────────────────────────────────────
    const education = formData.education
        .filter(e => e.degree?.trim() || e.institution?.trim())
        .map(e => ({
            id: e.id,
            degree: e.degree?.trim() || '',
            institution: e.institution?.trim() || '',
            location: e.location?.trim() || '',
            start_year: e.startYear ? Number(e.startYear) : null,
            end_year: e.endYear ? Number(e.endYear) : null,
            gpa: e.gpa?.trim() || null,
        }))

    // ── Projects ────────────────────────────────────────────────────────────
    const projects = formData.projects
        .filter(p => p.name?.trim())
        .map(p => ({
            id: p.id,
            name: p.name?.trim() || '',
            description: p.description?.trim() || '',
            tech_stack: parseTechStack(p.tech),
            link: p.link?.trim() || null,
        }))

    // ── Certifications ──────────────────────────────────────────────────────
    const certifications = formData.certifications
        .filter(c => c.name?.trim())
        .map(c => ({
            id: c.id,
            name: c.name?.trim() || '',
            issuer: c.issuer?.trim() || null,
            year: c.year ? Number(c.year) : null,
        }))

    // ── Skills ──────────────────────────────────────────────────────────────
    const allSkills = Array.from(new Set([
        ...formData.skills.technical,
        ...formData.skills.soft,
    ]))

    // ── Computed fields ─────────────────────────────────────────────────────
    const totalExpMonths = experience.reduce((sum, e) => sum + e.duration_months, 0)

    // Highest education level across all entries
    const educationLevelPriority = ['phd', 'master', 'bachelor', 'diploma', 'high_school', 'other']
    const educationLevel = education.reduce((best, e) => {
        const level = inferEducationLevel(e.degree)
        return educationLevelPriority.indexOf(level) < educationLevelPriority.indexOf(best)
            ? level
            : best
    }, 'other')

    // All unique technologies across skills + projects
    const allTechStack = Array.from(new Set([
        ...formData.skills.technical,
        ...projects.flatMap(p => p.tech_stack),
    ])).filter(Boolean)

    const latestRole = experience.find(e => e.is_current)?.title
        || experience[0]?.title
        || formData.personal.jobTitle?.trim()
        || ''

    const { breakdown, total: completenessScore } = computeCompleteness(formData)

    // ── Assemble ─────────────────────────────────────────────────────────────
    return {
        schema_version: SCHEMA_VERSION,

        metadata: {
            resume_id: existingId || generateResumeId(),
            schema_version: SCHEMA_VERSION,
            created_at: existingId ? undefined : now,  // preserved on update
            updated_at: now,
        },

        profile: {
            full_name: formData.personal.fullName?.trim() || '',
            job_title: formData.personal.jobTitle?.trim() || '',
            contact: {
                email: formData.personal.email?.trim() || null,
                phone: formData.personal.phone?.trim() || null,
                location: formData.personal.location?.trim() || null,
                linkedin: formData.personal.linkedin?.trim() || null,
                github: formData.personal.github?.trim() || null,
                website: formData.personal.website?.trim() || null,
            },
        },

        summary: formData.summary?.trim() || null,

        experience,
        education,

        skills: {
            technical: [...formData.skills.technical],
            soft: [...formData.skills.soft],
            all: allSkills,
        },

        projects,
        certifications,

        computed: {
            total_experience_months: totalExpMonths,
            total_experience_years: Math.round((totalExpMonths / 12) * 10) / 10,
            education_level: educationLevel,
            latest_role: latestRole,
            all_tech_stack: allTechStack,
            completeness_score: completenessScore,
            completeness_breakdown: breakdown,
        },
    }
}

/**
 * Utility: extract a flat keyword list from a structured resume
 * for fast full-text search or JD matching.
 *
 * @param {Object} structured - result of mapToStructuredResume
 * @returns {string[]}
 */
export function extractSearchableKeywords(structured) {
    const keywords = new Set()

    // Profile signals
    if (structured.profile.full_name) keywords.add(structured.profile.full_name.toLowerCase())
    if (structured.profile.job_title) keywords.add(structured.profile.job_title.toLowerCase())

    // All skills
    structured.skills.all.forEach(s => keywords.add(s.toLowerCase()))

    // All tech stack
    structured.computed.all_tech_stack.forEach(t => keywords.add(t.toLowerCase()))

    // Experience keywords
    structured.experience.forEach(e => {
        e.keywords.forEach(k => keywords.add(k))
        if (e.title) keywords.add(e.title.toLowerCase())
    })

    // Certification names
    structured.certifications.forEach(c => {
        if (c.name) keywords.add(c.name.toLowerCase())
    })

    return Array.from(keywords)
}

/**
 * Resume Schema v1.0.0
 *
 * Single source of truth for the canonical resume data structure.
 * Every field is annotated with:
 *  - type        : expected JS type / value set
 *  - required    : whether absence triggers a validation error
 *  - description : human-readable purpose
 *  - used_by     : modules that consume this field
 *
 * The SCHEMA_VERSION must be bumped on any breaking change to the shape.
 */

export const SCHEMA_VERSION = '1.0.0'

/**
 * @typedef {Object} ResumeSchema
 *
 * @property {string}  schema_version
 * @property {Object}  metadata
 * @property {Object}  profile
 * @property {string}  summary
 * @property {Array}   experience
 * @property {Array}   education
 * @property {Object}  skills
 * @property {Array}   projects
 * @property {Array}   certifications
 * @property {Object}  computed
 */

export const FIELD_DESCRIPTORS = {
    // ── Metadata ────────────────────────────────────────────────────────────
    'metadata.resume_id': { type: 'string', required: true, used_by: ['all'], description: 'Unique identifier for this resume snapshot' },
    'metadata.schema_version': { type: 'string', required: true, used_by: ['all'], description: 'Schema version string for forward compatibility' },
    'metadata.created_at': { type: 'string', required: true, used_by: ['all'], description: 'ISO 8601 timestamp of first creation' },
    'metadata.updated_at': { type: 'string', required: true, used_by: ['all'], description: 'ISO 8601 timestamp of last modification' },

    // ── Profile ─────────────────────────────────────────────────────────────
    'profile.full_name': { type: 'string', required: true, used_by: ['screening', 'ranking', 'interview'], description: 'Candidate full legal name' },
    'profile.job_title': { type: 'string', required: true, used_by: ['screening', 'ranking'], description: 'Desired or current job title' },
    'profile.contact.email': { type: 'string', required: true, used_by: ['screening'], description: 'Primary contact email (validated format)' },
    'profile.contact.phone': { type: 'string', required: false, used_by: ['screening'], description: 'Contact phone number' },
    'profile.contact.location': { type: 'string', required: false, used_by: ['screening', 'ranking'], description: 'City, State/Country' },
    'profile.contact.linkedin': { type: 'string', required: false, used_by: ['screening'], description: 'LinkedIn profile URL' },
    'profile.contact.github': { type: 'string', required: false, used_by: ['screening'], description: 'GitHub profile URL' },
    'profile.contact.website': { type: 'string', required: false, used_by: ['screening'], description: 'Personal portfolio / website URL' },

    // ── Summary ─────────────────────────────────────────────────────────────
    'summary': { type: 'string', required: false, used_by: ['screening', 'ranking'], description: 'Professional summary text for NLP keyword extraction' },

    // ── Experience ──────────────────────────────────────────────────────────
    'experience[].id': { type: 'string', required: true, used_by: ['all'], description: 'Unique entry ID' },
    'experience[].title': { type: 'string', required: true, used_by: ['screening', 'ranking'], description: 'Job title / role' },
    'experience[].company': { type: 'string', required: true, used_by: ['screening'], description: 'Employer name' },
    'experience[].location': { type: 'string', required: false, used_by: ['screening'], description: 'Work location' },
    'experience[].start_date': { type: 'string', required: false, used_by: ['ranking'], description: 'Start date in YYYY-MM format' },
    'experience[].end_date': { type: 'string|null', required: false, used_by: ['ranking'], description: 'End date in YYYY-MM format, null if current' },
    'experience[].is_current': { type: 'boolean', required: true, used_by: ['ranking'], description: 'Whether this is the active role' },
    'experience[].duration_months': { type: 'number', required: true, used_by: ['ranking'], description: 'Computed duration in months' },
    'experience[].description': { type: 'string', required: false, used_by: ['screening', 'ranking'], description: 'Role description and achievements' },
    'experience[].keywords': { type: 'string[]', required: true, used_by: ['screening', 'ranking'], description: 'Extracted tech keywords from description' },

    // ── Education ───────────────────────────────────────────────────────────
    'education[].id': { type: 'string', required: true, used_by: ['all'], description: 'Unique entry ID' },
    'education[].degree': { type: 'string', required: true, used_by: ['screening', 'ranking'], description: 'Degree / qualification name' },
    'education[].institution': { type: 'string', required: true, used_by: ['screening'], description: 'Educational institution name' },
    'education[].location': { type: 'string', required: false, used_by: ['screening'], description: 'Institution location' },
    'education[].start_year': { type: 'number', required: false, used_by: ['ranking'], description: 'Year started (YYYY)' },
    'education[].end_year': { type: 'number', required: false, used_by: ['ranking'], description: 'Year completed (YYYY)' },
    'education[].gpa': { type: 'string', required: false, used_by: ['ranking'], description: 'GPA / CGPA string' },

    // ── Skills ──────────────────────────────────────────────────────────────
    'skills.technical': { type: 'string[]', required: false, used_by: ['screening', 'ranking', 'assessment'], description: 'Array of technical skill strings' },
    'skills.soft': { type: 'string[]', required: false, used_by: ['screening', 'interview'], description: 'Array of soft skill strings' },
    'skills.all': { type: 'string[]', required: true, used_by: ['screening', 'ranking'], description: 'Merged deduplicated skill list for fast search' },

    // ── Projects ────────────────────────────────────────────────────────────
    'projects[].id': { type: 'string', required: true, used_by: ['screening'], description: 'Unique entry ID' },
    'projects[].name': { type: 'string', required: true, used_by: ['screening'], description: 'Project name' },
    'projects[].description': { type: 'string', required: false, used_by: ['screening'], description: 'Project description' },
    'projects[].tech_stack': { type: 'string[]', required: false, used_by: ['screening', 'ranking', 'assessment'], description: 'Technologies used (parsed from comma string)' },
    'projects[].link': { type: 'string', required: false, used_by: ['screening'], description: 'Project URL or repository link' },

    // ── Certifications ──────────────────────────────────────────────────────
    'certifications[].id': { type: 'string', required: true, used_by: ['screening'], description: 'Unique entry ID' },
    'certifications[].name': { type: 'string', required: true, used_by: ['screening'], description: 'Certification name' },
    'certifications[].issuer': { type: 'string', required: false, used_by: ['screening'], description: 'Issuing organization' },
    'certifications[].year': { type: 'number', required: false, used_by: ['screening'], description: 'Year awarded' },

    // ── Computed (derived, not entered by user) ──────────────────────────────
    'computed.total_experience_months': { type: 'number', required: true, used_by: ['ranking'], description: 'Sum of all experience durations in months' },
    'computed.total_experience_years': { type: 'number', required: true, used_by: ['ranking'], description: 'total_experience_months / 12, rounded to 1 decimal' },
    'computed.education_level': { type: 'string', required: true, used_by: ['ranking'], description: 'Inferred: phd | master | bachelor | diploma | high_school | other' },
    'computed.latest_role': { type: 'string', required: true, used_by: ['ranking', 'screening'], description: 'Most recent job title' },
    'computed.all_tech_stack': { type: 'string[]', required: true, used_by: ['ranking', 'screening', 'assessment'], description: 'Deduplicated union of skills.technical + all project tech_stacks' },
    'computed.completeness_score': { type: 'number', required: true, used_by: ['all'], description: 'Resume completeness 0–100 (weighted across sections)' },
    'computed.completeness_breakdown': { type: 'Object', required: true, used_by: ['all'], description: 'Per-section completeness scores used in UI feedback' },
}

/**
 * Completeness scoring weights (must sum to 100).
 * Used by both the mapper (to compute the score) and
 * the UI (to display section-level breakdowns).
 */
export const COMPLETENESS_WEIGHTS = {
    personal: { weight: 20, label: 'Personal Info', icon: '👤' },
    summary: { weight: 15, label: 'Summary', icon: '📝' },
    experience: { weight: 25, label: 'Work Experience', icon: '💼' },
    education: { weight: 15, label: 'Education', icon: '🎓' },
    skills: { weight: 15, label: 'Skills', icon: '⚡' },
    projects: { weight: 10, label: 'Projects / Certs', icon: '🚀' },
}

/**
 * Modules that consume structured resume data.
 * Used for documentation and future dependency tracking.
 */
export const CONSUMING_MODULES = {
    screening: {
        label: 'Resume Screening',
        fields: ['profile', 'summary', 'experience', 'skills', 'computed.all_tech_stack'],
    },
    ranking: {
        label: 'Candidate Ranking',
        fields: ['computed.total_experience_years', 'computed.education_level', 'skills.technical', 'experience[].keywords'],
    },
    assessment: {
        label: 'Skill Assessment',
        fields: ['skills.technical', 'computed.all_tech_stack', 'computed.education_level'],
    },
    interview: {
        label: 'Mock Interview Analysis',
        fields: ['profile.full_name', 'profile.job_title', 'computed.latest_role', 'summary'],
    },
}

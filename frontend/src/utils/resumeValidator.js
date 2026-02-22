/**
 * resumeValidator.js
 *
 * Validates a structured resume object (output of mapToStructuredResume)
 * against business rules and schema requirements.
 *
 * Returns a ValidationResult with:
 *  - isValid     : boolean — true only if no errors exist
 *  - errors      : Array<{ field, message }> — blocking issues
 *  - warnings    : Array<{ field, message }> — non-blocking suggestions
 *  - score       : number 0–100 — completeness score (mirrors computed field)
 *  - readyFor    : string[] — modules this resume is ready to be consumed by
 */

// ─── Helpers ─────────────────────────────────────────────────────────────────

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function isPresent(val) {
    if (val === null || val === undefined) return false
    if (typeof val === 'string') return val.trim().length > 0
    if (Array.isArray(val)) return val.length > 0
    return true
}

// ─── Module Readiness Thresholds ─────────────────────────────────────────────

/**
 * Minimum field requirements for each consuming module.
 * A module is "ready" only if all its required conditions pass.
 */
const MODULE_REQUIREMENTS = {
    screening: {
        label: 'Resume Screening',
        check: (s) =>
            isPresent(s.profile.full_name) &&
            isPresent(s.profile.contact?.email) &&
            (isPresent(s.skills.technical) || isPresent(s.summary)),
    },
    ranking: {
        label: 'Candidate Ranking',
        check: (s) =>
            s.computed.total_experience_months >= 0 &&
            isPresent(s.computed.education_level) &&
            isPresent(s.skills.all),
    },
    assessment: {
        label: 'Skill Assessment',
        check: (s) =>
            isPresent(s.skills.technical) && s.skills.technical.length >= 2,
    },
    interview: {
        label: 'Mock Interview Analysis',
        check: (s) =>
            isPresent(s.profile.full_name) &&
            isPresent(s.computed.latest_role),
    },
}

// ─── Main Validator ───────────────────────────────────────────────────────────

/**
 * validateStructuredResume
 *
 * Validates a canonical structured resume against schema rules.
 *
 * @param {Object} structured - result of mapToStructuredResume
 * @returns {{
 *   isValid: boolean,
 *   errors:  Array<{field: string, message: string}>,
 *   warnings:Array<{field: string, message: string}>,
 *   score:   number,
 *   readyFor:string[],
 *   readyForLabels: string[],
 * }}
 */
export function validateStructuredResume(structured) {
    const errors = []
    const warnings = []

    // ── Required field checks (errors) ───────────────────────────────────────

    if (!isPresent(structured.profile?.full_name)) {
        errors.push({ field: 'profile.full_name', message: 'Full name is required.' })
    }

    if (!isPresent(structured.profile?.job_title)) {
        errors.push({ field: 'profile.job_title', message: 'Job title is required.' })
    }

    if (!isPresent(structured.profile?.contact?.email)) {
        errors.push({ field: 'profile.contact.email', message: 'Email address is required.' })
    } else if (!EMAIL_RE.test(structured.profile.contact.email)) {
        errors.push({ field: 'profile.contact.email', message: 'Email address format is invalid.' })
    }

    // ── Quality warnings (non-blocking) ──────────────────────────────────────

    if (!isPresent(structured.summary) || structured.summary.length < 50) {
        warnings.push({
            field: 'summary',
            message: 'A professional summary of ≥ 50 characters significantly improves screening accuracy.',
        })
    }

    if (structured.experience.length === 0) {
        warnings.push({
            field: 'experience',
            message: 'No work experience listed. Add at least one role for better ranking results.',
        })
    } else {
        const missingDesc = structured.experience.filter(e => !isPresent(e.description))
        if (missingDesc.length > 0) {
            warnings.push({
                field: 'experience[].description',
                message: `${missingDesc.length} experience ${missingDesc.length === 1 ? 'entry is' : 'entries are'} missing descriptions. Descriptions improve keyword extraction.`,
            })
        }
        const missingDates = structured.experience.filter(e => !e.start_date)
        if (missingDates.length > 0) {
            warnings.push({
                field: 'experience[].start_date',
                message: `${missingDates.length} experience ${missingDates.length === 1 ? 'entry is' : 'entries are'} missing start dates. Dates are required for experience calculation.`,
            })
        }
    }

    if (structured.education.length === 0) {
        warnings.push({
            field: 'education',
            message: 'No education listed. Add your highest qualification.',
        })
    }

    if (structured.skills.technical.length < 3) {
        warnings.push({
            field: 'skills.technical',
            message: `Only ${structured.skills.technical.length} technical skill(s) listed. Add at least 5 for effective matching against job descriptions.`,
        })
    }

    if (structured.projects.length === 0 && structured.certifications.length === 0) {
        warnings.push({
            field: 'projects',
            message: 'Adding projects or certifications strengthens your profile and improves assessment module accuracy.',
        })
    }

    if (structured.computed.all_tech_stack.length === 0) {
        warnings.push({
            field: 'computed.all_tech_stack',
            message: 'No tech stack could be extracted. Add technical skills or project technologies for AI matching.',
        })
    }

    // ── Module readiness ─────────────────────────────────────────────────────
    const readyFor = []
    const readyForLabels = []
    for (const [moduleKey, module] of Object.entries(MODULE_REQUIREMENTS)) {
        if (module.check(structured)) {
            readyFor.push(moduleKey)
            readyForLabels.push(module.label)
        }
    }

    return {
        isValid: errors.length === 0,
        errors,
        warnings,
        score: structured.computed?.completeness_score ?? 0,
        readyFor,
        readyForLabels,
    }
}

/**
 * validateFormData (convenience wrapper)
 *
 * Accepts raw formData directly (runs mapper internally).
 * Useful for real-time validation in the UI before building
 * the full structured resume.
 *
 * @param {Object} formData - raw Pinia formData
 * @returns {Object} ValidationResult
 */
export async function validateFormData(formData) {
    const { mapToStructuredResume } = await import('./resumeMapper.js')
    const structured = mapToStructuredResume(formData)
    return validateStructuredResume(structured)
}

import { reactive, ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { mapToStructuredResume } from '../utils/resumeMapper.js'
import { validateStructuredResume } from '../utils/resumeValidator.js'

export const useResumeStore = defineStore('resume', () => {
    // --- Selected Template ---
    const selectedTemplate = ref('classic')

    // --- Raw Form Data (user input) ---
    const formData = reactive({
        personal: {
            fullName: '',
            jobTitle: '',
            email: '',
            phone: '',
            location: '',
            linkedin: '',
            github: '',
            website: '',
        },

        summary: '',

        experience: [],
        // Shape: { id, title, company, location, startDate, endDate, current, description }

        education: [],
        // Shape: { id, degree, institution, location, startYear, endYear, gpa }

        skills: {
            technical: [],  // Array of strings
            soft: [],       // Array of strings
        },

        projects: [],
        // Shape: { id, name, description, tech, link }

        certifications: [],
        // Shape: { id, name, issuer, year }
    })

    // --- Persistent resume ID (preserved across re-builds) ---
    const _resumeId = ref(null)

    // ─── Structured Resume (derived + stored) ────────────────────────────────
    /**
     * The canonical structured resume computed from formData.
     * This is live-reactive — updates automatically as the user types.
     * Consume this in place of formData in all processing / export logic.
     */
    const structuredResume = computed(() =>
        mapToStructuredResume(formData, _resumeId.value)
    )

    /**
     * Validation result computed from the current structured resume.
     * Provides errors, warnings, completeness score, and module readiness.
     */
    const validationResult = computed(() =>
        validateStructuredResume(structuredResume.value)
    )

    /**
     * Completeness score (0–100) shorthand.
     */
    const completenessScore = computed(() =>
        structuredResume.value.computed.completeness_score
    )

    /**
     * Per-section completeness breakdown shorthand.
     */
    const completenessBreakdown = computed(() =>
        structuredResume.value.computed.completeness_breakdown
    )

    // ─── Save Snapshot ──────────────────────────────────────────────────────
    /**
     * Persist the current structured resume to localStorage as a snapshot.
     * Called when the user explicitly finalises / exports.
     *
     * @returns {Object} the structured resume that was saved
     */
    function saveSnapshot() {
        const snapshot = structuredResume.value
        _resumeId.value = snapshot.metadata.resume_id
        try {
            localStorage.setItem(
                `hireai_resume_${snapshot.metadata.resume_id}`,
                JSON.stringify(snapshot)
            )
            localStorage.setItem('hireai_resume_latest_id', snapshot.metadata.resume_id)
        } catch (e) {
            console.warn('[ResumeStore] localStorage unavailable:', e)
        }
        return snapshot
    }

    /**
     * Restore the latest saved snapshot from localStorage (if any).
     * Maps structured fields back into formData.
     */
    function restoreLatestSnapshot() {
        try {
            const latestId = localStorage.getItem('hireai_resume_latest_id')
            if (!latestId) return false
            const raw = localStorage.getItem(`hireai_resume_${latestId}`)
            if (!raw) return false
            const snapshot = JSON.parse(raw)
            _fillFormDataFromSnapshot(snapshot)
            _resumeId.value = latestId
            return true
        } catch {
            return false
        }
    }

    // ─── Helpers ─────────────────────────────────────────────────────────────
    function uid() {
        return Date.now().toString(36) + Math.random().toString(36).slice(2)
    }

    function _fillFormDataFromSnapshot(s) {
        // Personal
        Object.assign(formData.personal, {
            fullName: s.profile?.full_name || '',
            jobTitle: s.profile?.job_title || '',
            email: s.profile?.contact?.email || '',
            phone: s.profile?.contact?.phone || '',
            location: s.profile?.contact?.location || '',
            linkedin: s.profile?.contact?.linkedin || '',
            github: s.profile?.contact?.github || '',
            website: s.profile?.contact?.website || '',
        })
        formData.summary = s.summary || ''

        // Experience
        formData.experience.splice(0, formData.experience.length,
            ...(s.experience || []).map(e => ({
                id: e.id || uid(),
                title: e.title || '',
                company: e.company || '',
                location: e.location || '',
                startDate: e.start_date || '',
                endDate: e.end_date || '',
                current: e.is_current || false,
                description: e.description || '',
            }))
        )

        // Education
        formData.education.splice(0, formData.education.length,
            ...(s.education || []).map(e => ({
                id: e.id || uid(),
                degree: e.degree || '',
                institution: e.institution || '',
                location: e.location || '',
                startYear: e.start_year || '',
                endYear: e.end_year || '',
                gpa: e.gpa || '',
            }))
        )

        // Skills
        formData.skills.technical.splice(0, formData.skills.technical.length, ...(s.skills?.technical || []))
        formData.skills.soft.splice(0, formData.skills.soft.length, ...(s.skills?.soft || []))

        // Projects
        formData.projects.splice(0, formData.projects.length,
            ...(s.projects || []).map(p => ({
                id: p.id || uid(),
                name: p.name || '',
                description: p.description || '',
                tech: (p.tech_stack || []).join(', '),
                link: p.link || '',
            }))
        )

        // Certifications
        formData.certifications.splice(0, formData.certifications.length,
            ...(s.certifications || []).map(c => ({
                id: c.id || uid(),
                name: c.name || '',
                issuer: c.issuer || '',
                year: c.year || '',
            }))
        )
    }

    // ─── Experience actions ──────────────────────────────────────────────────
    function addExperience() {
        formData.experience.push({
            id: uid(), title: '', company: '', location: '',
            startDate: '', endDate: '', current: false, description: '',
        })
    }
    function removeExperience(id) {
        const idx = formData.experience.findIndex(e => e.id === id)
        if (idx !== -1) formData.experience.splice(idx, 1)
    }

    // ─── Education actions ────────────────────────────────────────────────────
    function addEducation() {
        formData.education.push({
            id: uid(), degree: '', institution: '', location: '',
            startYear: '', endYear: '', gpa: '',
        })
    }
    function removeEducation(id) {
        const idx = formData.education.findIndex(e => e.id === id)
        if (idx !== -1) formData.education.splice(idx, 1)
    }

    // ─── Project actions ──────────────────────────────────────────────────────
    function addProject() {
        formData.projects.push({ id: uid(), name: '', description: '', tech: '', link: '' })
    }
    function removeProject(id) {
        const idx = formData.projects.findIndex(p => p.id === id)
        if (idx !== -1) formData.projects.splice(idx, 1)
    }

    // ─── Certification actions ────────────────────────────────────────────────
    function addCertification() {
        formData.certifications.push({ id: uid(), name: '', issuer: '', year: '' })
    }
    function removeCertification(id) {
        const idx = formData.certifications.findIndex(c => c.id === id)
        if (idx !== -1) formData.certifications.splice(idx, 1)
    }

    // ─── Skills actions ───────────────────────────────────────────────────────
    function addSkill(type, skill) {
        const s = skill.trim()
        if (s && !formData.skills[type].includes(s)) {
            formData.skills[type].push(s)
        }
    }
    function removeSkill(type, skill) {
        formData.skills[type] = formData.skills[type].filter(s => s !== skill)
    }

    // ─── Reset ────────────────────────────────────────────────────────────────
    function resetForm() {
        Object.assign(formData.personal, {
            fullName: '', jobTitle: '', email: '', phone: '',
            location: '', linkedin: '', github: '', website: '',
        })
        formData.summary = ''
        formData.experience.splice(0)
        formData.education.splice(0)
        formData.skills.technical.splice(0)
        formData.skills.soft.splice(0)
        formData.projects.splice(0)
        formData.certifications.splice(0)
        _resumeId.value = null
    }

    return {
        // Template
        selectedTemplate,

        // Raw form data (for form binding)
        formData,

        // Structured output (for processing / export)
        structuredResume,
        validationResult,
        completenessScore,
        completenessBreakdown,

        // Persistence
        saveSnapshot,
        restoreLatestSnapshot,

        // CRUD actions
        addExperience, removeExperience,
        addEducation, removeEducation,
        addProject, removeProject,
        addCertification, removeCertification,
        addSkill, removeSkill,
        resetForm,
    }
})

/**
 * useResumeExport.js
 *
 * Vue composable that provides export utilities for the structured resume.
 *
 * Exports:
 *  - downloadJSON(structured)       → triggers browser file download
 *  - copyToClipboard(structured)    → copies JSON to clipboard
 *  - clipboardStatus                → reactive feedback string
 */

import { ref } from 'vue'

export function useResumeExport() {
    const clipboardStatus = ref('idle')  // 'idle' | 'copied' | 'error'
    let clipboardTimer = null

    /**
     * Trigger a browser download of the structured resume as a .json file.
     *
     * @param {Object} structured  - canonical structured resume object
     * @param {string} [filename]  - override filename (auto-generated if omitted)
     */
    function downloadJSON(structured, filename) {
        const name = filename
            || `resume_${(structured.profile?.full_name || 'candidate')
                .toLowerCase().replace(/\s+/g, '_')}_${Date.now()}.json`

        const json = JSON.stringify(structured, null, 2)
        const blob = new Blob([json], { type: 'application/json' })
        const url = URL.createObjectURL(blob)

        const anchor = document.createElement('a')
        anchor.href = url
        anchor.download = name
        anchor.click()

        // Clean up object URL after download begins
        setTimeout(() => URL.revokeObjectURL(url), 1000)
    }

    /**
     * Copy the structured resume JSON to the system clipboard.
     *
     * Updates clipboardStatus reactively:
     *  'copied' for 2 seconds, then reverts to 'idle'.
     *
     * @param {Object} structured - canonical structured resume object
     */
    async function copyToClipboard(structured) {
        try {
            await navigator.clipboard.writeText(JSON.stringify(structured, null, 2))
            clipboardStatus.value = 'copied'
        } catch {
            clipboardStatus.value = 'error'
        } finally {
            if (clipboardTimer) clearTimeout(clipboardTimer)
            clipboardTimer = setTimeout(() => {
                clipboardStatus.value = 'idle'
            }, 2500)
        }
    }

    /**
     * Build a human-readable summary string of the structured resume
     * for quick display or clipboard sharing.
     *
     * @param {Object} structured
     * @returns {string}
     */
    function buildSummaryText(structured) {
        const s = structured
        const lines = [
            `=== Resume: ${s.profile.full_name} (${s.profile.job_title}) ===`,
            `Email: ${s.profile.contact?.email || 'N/A'}`,
            `Experience: ${s.computed.total_experience_years} years`,
            `Education: ${s.computed.education_level}`,
            `Tech Stack: ${s.computed.all_tech_stack.slice(0, 10).join(', ')}`,
            `Completeness: ${s.computed.completeness_score}%`,
            `Schema: ${s.schema_version} | ID: ${s.metadata.resume_id}`,
        ]
        return lines.join('\n')
    }

    return {
        clipboardStatus,
        downloadJSON,
        copyToClipboard,
        buildSummaryText,
    }
}

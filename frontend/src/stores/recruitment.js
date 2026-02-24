import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useRecruitmentStore = defineStore('recruitment', () => {
    // State
    const candidates = ref([])
    const totalUploaded = ref(0)
    const screeningInProgress = ref(false)

    // Getters
    const shortlisted = computed(() => candidates.value.filter(c => c.status === 'Shortlisted'))
    const rejected = computed(() => candidates.value.filter(c => c.status === 'Rejected'))
    const underReview = computed(() => candidates.value.filter(c => c.status === 'Under Review'))

    // Actions
    function addCandidates(newCandidates) {
        candidates.value.push(...newCandidates)
        totalUploaded.value += newCandidates.length
    }

    function updateCandidateStatus(id, status) {
        const candidate = candidates.value.find(c => c.id === id)
        if (candidate) candidate.status = status
    }

    function clearCandidates() {
        candidates.value = []
        totalUploaded.value = 0
    }

    return {
        candidates,
        totalUploaded,
        screeningInProgress,
        shortlisted,
        rejected,
        underReview,
        addCandidates,
        updateCandidateStatus,
        clearCandidates,
    }
})

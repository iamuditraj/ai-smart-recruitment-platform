import { ref } from 'vue'

export function useResumeWizard() {
  const steps = [
    { id: 'personal', label: 'Personal' },
    { id: 'summary', label: 'Summary' },
    { id: 'experience', label: 'Experience' },
    { id: 'education', label: 'Education' },
    { id: 'skills', label: 'Skills' },
    { id: 'projects', label: 'Projects' },
    { id: 'review', label: 'Review' }
  ]

  const currentStep = ref(0)

  const isStepDone = (index, formData) => {
    if (!formData) return false

    switch (index) {
      case 0:
        return formData.personal && typeof formData.personal.fullName === 'string' && formData.personal.fullName.trim() !== '' &&
               typeof formData.personal.email === 'string' && formData.personal.email.trim() !== ''
      case 1:
        return typeof formData.summary === 'string' && formData.summary.trim().length >= 20
      case 2:
        if (!Array.isArray(formData.experience)) return false
        return formData.experience.some(exp => 
          exp && typeof exp.title === 'string' && exp.title.trim() !== '' &&
          typeof exp.company === 'string' && exp.company.trim() !== ''
        )
      case 3:
        if (!Array.isArray(formData.education)) return false
        return formData.education.some(edu => 
          edu && typeof edu.degree === 'string' && edu.degree.trim() !== '' &&
          typeof edu.institution === 'string' && edu.institution.trim() !== ''
        )
      case 4:
        const skillsArray = formData.skills && formData.skills.technical
        return Array.isArray(skillsArray) && skillsArray.length >= 2
      case 5:
        const hasProject = Array.isArray(formData.projects) && formData.projects.some(proj => proj && typeof proj.name === 'string' && proj.name.trim() !== '')
        const hasCert = Array.isArray(formData.certifications) && formData.certifications.some(cert => cert && typeof cert.name === 'string' && cert.name.trim() !== '')
        return hasProject || hasCert
      default:
        return false
    }
  }

  const goToStep = (i, saveSnapshotFn) => {
    if (i === steps.length - 1 && typeof saveSnapshotFn === 'function') {
      saveSnapshotFn()
    }
    currentStep.value = i
  }

  const nextStep = (saveSnapshotFn) => {
    if (currentStep.value === steps.length - 2 && typeof saveSnapshotFn === 'function') {
      saveSnapshotFn()
    }
    currentStep.value += 1
  }

  const prevStep = () => {
    if (currentStep.value > 0) {
      currentStep.value -= 1
    }
  }

  return {
    steps,
    currentStep,
    isStepDone,
    goToStep,
    nextStep,
    prevStep
  }
}

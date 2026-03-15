import { computed } from 'vue'
import { useResumeStore } from '../stores/resume.js'

export function useResumeAI() {
  const store = useResumeStore()

  const generateAISummary = async (formData) => {
    const prompt = `Write a professional 3-sentence resume summary for a ${formData.personal.jobTitle}. Key skills: ${formData.skills.technical.join(', ')}. Focus on high-impact results.`
    
    const result = await store.generateAIContent(prompt)
    if (result) {
      formData.summary = result.trim()
    }
  }

  const generateAIExperience = async (formData, index) => {
    const exp = formData.experience[index]
    const prompt = `Rewrite this job description to be more professional and impact-driven. Role: ${exp.title} at ${exp.company}. Current content: ${exp.description || 'N/A'}. Use strong action verbs and metrics-focused bullet points.`
    
    const result = await store.generateAIContent(prompt)
    if (result) {
      exp.description = result.trim()
    }
  }

  const handlePhotoUpload = (event, formData) => {
    const file = event.target.files[0]
    if (!file) return

    if (file.size > 2 * 1024 * 1024) {
      alert('Image size should be less than 2MB')
      return
    }

    const reader = new FileReader()
    reader.onload = (e) => {
      formData.personal.photo = e.target.result
    }
    reader.readAsDataURL(file)
  }

  return {
    generateAISummary,
    generateAIExperience,
    handlePhotoUpload,
    isGenerating: computed(() => store.isGenerating)
  }
}

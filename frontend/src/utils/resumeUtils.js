export function viewResume(dataUri) {
  if (!dataUri) return

  try {
    const base64 = dataUri.split(',')[1]
    const binary = atob(base64)
    const array = []
    for (let i = 0; i < binary.length; i++) {
      array.push(binary.charCodeAt(i))
    }
    const blob = new Blob([new Uint8Array(array)], { type: 'application/pdf' })
    const url = URL.createObjectURL(blob)
    window.open(url, '_blank')
  } catch (error) {
    console.error('Error viewing resume:', error)
    // Fallback: try opening the data URI directly if blob fails
    window.open(dataUri, '_blank')
  }
}

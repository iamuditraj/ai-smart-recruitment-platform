export const getScoreColor = (score) => {
  if (score >= 80) return '#10b981'
  if (score >= 60) return '#f59e0b'
  return '#ef4444'
}

export const getBreakdownColor = (score, max) => {
  const ratio = max > 0 ? score / max : 0
  if (ratio >= 0.75) return '#10b981'
  if (ratio >= 0.4)  return '#f59e0b'
  return '#ef4444'
}

export function avatarGrad(seed) {
  let hash = 0
  for (let i = 0; i < (seed || '').length; i++) hash = seed.charCodeAt(i) + ((hash << 5) - hash)
  const h1 = Math.abs(hash % 360)
  const h2 = (h1 + 40) % 360
  return `linear-gradient(135deg, hsl(${h1}, 70%, 55%), hsl(${h2}, 80%, 45%))`
}

export function initials(name) {
  return (name || '?').split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2)
}

export function getStatusClass(status) {
  if (status === 'Shortlisted' || status === 'Approved') return 'status-approved'
  if (status === 'Rejected') return 'status-rejected'
  if (status === 'Applied') return 'status-applied'
  return 'status-pending'
}

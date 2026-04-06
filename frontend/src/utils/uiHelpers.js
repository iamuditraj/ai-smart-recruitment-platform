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

export function avatarGrad() {
  return `linear-gradient(135deg, #${Math.floor(Math.random()*16777215).toString(16).padStart(6,'0')}, #${Math.floor(Math.random()*16777215).toString(16).padStart(6,'0')})`
}

export function initials(name) {
  return (name || '?').split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2)
}

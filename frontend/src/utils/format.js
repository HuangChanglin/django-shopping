export const formatPrice = (price) => {
  return `¥${Number(price).toFixed(2)}`
}

export const formatDate = (date) => {
  if (!date) return ''
  const d = new Date(date)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

export const formatDateTime = (datetime) => {
  if (!datetime) return ''
  const d = new Date(datetime)
  return `${formatDate(d)} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

export const getImageUrl = (url) => {
  if (!url) return '/placeholder.png'
  if (url.startsWith('http')) return url
  return `/api${url}`
}

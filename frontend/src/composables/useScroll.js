import { ref, computed, watch, onMounted, onUnmounted } from 'vue'

export function useInfiniteScroll(loadMore, options = {}) {
  const { distance = 100, disabled = ref(false) } = options
  
  const handleScroll = () => {
    if (disabled.value) return
    
    const scrollTop = window.scrollY || document.documentElement.scrollTop
    const scrollHeight = document.documentElement.scrollHeight
    const clientHeight = window.innerHeight
    
    if (scrollHeight - scrollTop - clientHeight < distance) {
      loadMore()
    }
  }

  onMounted(() => {
    window.addEventListener('scroll', handleScroll, { passive: true })
  })

  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll)
  })

  return { disabled }
}

export function useScrollPosition(key = 'scroll_position') {
  const position = ref(0)
  
  const savePosition = () => {
    position.value = window.scrollY
    sessionStorage.setItem(key, position.value.toString())
  }

  const restorePosition = () => {
    const saved = sessionStorage.getItem(key)
    if (saved) {
      window.scrollTo(0, parseInt(saved))
    }
  }

  onMounted(restorePosition)
  onUnmounted(savePosition)

  return { position }
}

export function useScrollToTop(options = {}) {
  const { threshold = 300, duration = 500 } = options
  const visible = ref(false)

  const handleScroll = () => {
    visible.value = window.scrollY > threshold
  }

  const scrollToTop = () => {
    const startY = window.scrollY
    const startTime = performance.now()
    
    const animate = (currentTime) => {
      const elapsed = currentTime - startTime
      const progress = Math.min(elapsed / duration, 1)
      const easeProgress = 1 - Math.pow(1 - progress, 3)
      
      window.scrollTo(0, startY * (1 - easeProgress))
      
      if (progress < 1) {
        requestAnimationFrame(animate)
      }
    }
    
    requestAnimationFrame(animate)
  }

  onMounted(() => {
    window.addEventListener('scroll', handleScroll, { passive: true })
  })

  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll)
  })

  return { visible, scrollToTop }
}

export function useScrollDirection() {
  const direction = ref('down')
  const lastScrollY = ref(0)

  const handleScroll = () => {
    const currentY = window.scrollY
    if (currentY > lastScrollY.value) {
      direction.value = 'down'
    } else {
      direction.value = 'up'
    }
    lastScrollY.value = currentY
  }

  onMounted(() => {
    window.addEventListener('scroll', handleScroll, { passive: true })
  })

  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll)
  })

  return { direction }
}

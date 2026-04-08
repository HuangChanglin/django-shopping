import { ref, computed } from 'vue'

export function useCountdown(initialTime = 60) {
  const time = ref(initialTime)
  const isCounting = ref(false)
  let timer = null

  const isDisabled = computed(() => isCounting.value || time.value <= 0)

  const start = (customTime = initialTime) => {
    if (isCounting.value) return
    
    time.value = customTime
    isCounting.value = true
    
    timer = setInterval(() => {
      time.value--
      if (time.value <= 0) {
        stop()
      }
    }, 1000)
  }

  const stop = () => {
    if (timer) {
      clearInterval(timer)
      timer = null
    }
    isCounting.value = false
  }

  const reset = (customTime = initialTime) => {
    stop()
    time.value = customTime
  }

  return {
    time,
    isCounting,
    isDisabled,
    start,
    stop,
    reset
  }
}

export function useCopy() {
  const copied = ref(false)
  
  const copy = async (text) => {
    try {
      await navigator.clipboard.writeText(text)
      copied.value = true
      setTimeout(() => {
        copied.value = false
      }, 2000)
      return true
    } catch (err) {
      console.error('复制失败:', err)
      return false
    }
  }

  return { copied, copy }
}

export function useDebounce(fn, delay = 300) {
  let timer = null
  
  const debounced = (...args) => {
    clearTimeout(timer)
    timer = setTimeout(() => {
      fn(...args)
    }, delay)
  }

  const cancel = () => {
    clearTimeout(timer)
  }

  return { debounced, cancel }
}

export function useThrottle(fn, delay = 300) {
  let lastTime = 0
  
  const throttled = (...args) => {
    const now = Date.now()
    if (now - lastTime >= delay) {
      lastTime = now
      fn(...args)
    }
  }

  return { throttled }
}

export function useLocalStorage(key, defaultValue) {
  const storedValue = localStorage.getItem(key)
  const data = ref(storedValue ? JSON.parse(storedValue) : defaultValue)

  const setValue = (value) => {
    data.value = value
    localStorage.setItem(key, JSON.stringify(value))
  }

  const removeValue = () => {
    data.value = defaultValue
    localStorage.removeItem(key)
  }

  return { data, setValue, removeValue }
}

export function useImagePreview() {
  const previewVisible = ref(false)
  const previewImage = ref('')
  const previewTitle = ref('')

  const openPreview = (imageUrl, title = '') => {
    previewImage.value = imageUrl
    previewTitle.value = title
    previewVisible.value = true
  }

  const closePreview = () => {
    previewVisible.value = false
    previewImage.value = ''
    previewTitle.value = ''
  }

  return {
    previewVisible,
    previewImage,
    previewTitle,
    openPreview,
    closePreview
  }
}

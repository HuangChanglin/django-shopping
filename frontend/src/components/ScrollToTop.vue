<template>
  <transition name="fade-slide" mode="out-in">
    <div v-if="visible" class="scroll-to-top" @click="scrollToTop">
      <el-icon><Top /></el-icon>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Top } from '@element-plus/icons-vue'

const visible = ref(false)
const threshold = 300

const handleScroll = () => {
  visible.value = window.scrollY > threshold
}

const scrollToTop = () => {
  const startY = window.scrollY
  const duration = 500
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
</script>

<style scoped lang="scss">
.scroll-to-top {
  position: fixed;
  right: 30px;
  bottom: 80px;
  width: 44px;
  height: 44px;
  background: rgba(64, 158, 255, 0.9);
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
  transition: all 0.3s ease;
  z-index: 1000;

  &:hover {
    background: #409EFF;
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(64, 158, 255, 0.5);
  }

  .el-icon {
    font-size: 20px;
  }
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>

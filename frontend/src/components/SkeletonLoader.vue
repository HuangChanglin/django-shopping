<template>
  <div v-if="loading && showSkeleton" class="skeleton-container">
    <template v-if="type === 'card'">
      <div class="skeleton-card">
        <div class="skeleton-image skeleton-pulse"></div>
        <div class="skeleton-content">
          <div class="skeleton-line skeleton-pulse" style="width: 80%"></div>
          <div class="skeleton-line skeleton-pulse" style="width: 60%"></div>
          <div class="skeleton-price skeleton-pulse"></div>
        </div>
      </div>
    </template>
    <template v-else-if="type === 'list'">
      <div v-for="i in count" :key="i" class="skeleton-list-item">
        <div class="skeleton-avatar skeleton-pulse"></div>
        <div class="skeleton-list-content">
          <div class="skeleton-line skeleton-pulse" style="width: 50%"></div>
          <div class="skeleton-line skeleton-pulse" style="width: 80%"></div>
        </div>
      </div>
    </template>
    <template v-else-if="type === 'detail'">
      <div class="skeleton-detail">
        <div class="skeleton-detail-left">
          <div class="skeleton-main-image skeleton-pulse"></div>
          <div class="skeleton-thumbnails">
            <div v-for="i in 4" :key="i" class="skeleton-thumb skeleton-pulse"></div>
          </div>
        </div>
        <div class="skeleton-detail-right">
          <div class="skeleton-line skeleton-pulse" style="width: 70%; height: 28px"></div>
          <div class="skeleton-line skeleton-pulse" style="width: 40%"></div>
          <div class="skeleton-price-large skeleton-pulse"></div>
          <div class="skeleton-line skeleton-pulse" style="width: 100%"></div>
          <div class="skeleton-line skeleton-pulse" style="width: 90%"></div>
          <div class="skeleton-line skeleton-pulse" style="width: 60%"></div>
        </div>
      </div>
    </template>
    <template v-else>
      <div v-for="i in count" :key="i" class="skeleton-item">
        <div class="skeleton-line skeleton-pulse" style="width: 30%"></div>
        <div class="skeleton-line skeleton-pulse" style="width: 70%"></div>
        <div class="skeleton-line skeleton-pulse" style="width: 50%"></div>
      </div>
    </template>
  </div>
</template>

<script setup>
defineProps({
  loading: {
    type: Boolean,
    default: true
  },
  type: {
    type: String,
    default: 'default',
    validator: (v) => ['default', 'card', 'list', 'detail'].includes(v)
  },
  count: {
    type: Number,
    default: 3
  },
  showSkeleton: {
    type: Boolean,
    default: true
  }
})
</script>

<style scoped lang="scss">
.skeleton-container {
  width: 100%;
}

.skeleton-pulse {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skeleton-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;

  .skeleton-image {
    width: 100%;
    height: 200px;
  }

  .skeleton-content {
    padding: 15px;
  }

  .skeleton-line {
    height: 14px;
    border-radius: 4px;
    margin-bottom: 10px;
  }

  .skeleton-price {
    height: 24px;
    width: 80px;
    border-radius: 4px;
    margin-top: 10px;
  }
}

.skeleton-list-item {
  display: flex;
  align-items: center;
  padding: 15px;
  background: #fff;
  margin-bottom: 10px;
  border-radius: 8px;

  .skeleton-avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin-right: 15px;
  }

  .skeleton-list-content {
    flex: 1;
  }

  .skeleton-line {
    height: 14px;
    border-radius: 4px;
    margin-bottom: 8px;
  }
}

.skeleton-detail {
  display: flex;
  gap: 40px;
  background: #fff;
  padding: 30px;
  border-radius: 8px;

  .skeleton-detail-left {
    width: 400px;
  }

  .skeleton-main-image {
    width: 100%;
    height: 400px;
    border-radius: 8px;
    margin-bottom: 15px;
  }

  .skeleton-thumbnails {
    display: flex;
    gap: 10px;
  }

  .skeleton-thumb {
    width: 60px;
    height: 60px;
    border-radius: 4px;
  }

  .skeleton-detail-right {
    flex: 1;
  }

  .skeleton-line {
    height: 14px;
    border-radius: 4px;
    margin-bottom: 15px;
  }

  .skeleton-price-large {
    height: 40px;
    width: 150px;
    border-radius: 4px;
    margin-bottom: 20px;
  }
}

.skeleton-item {
  padding: 15px;
  background: #fff;
  margin-bottom: 10px;
  border-radius: 8px;

  .skeleton-line {
    height: 14px;
    border-radius: 4px;
    margin-bottom: 10px;
  }
}
</style>

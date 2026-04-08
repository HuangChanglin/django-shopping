<template>
  <div class="product-card" :class="{ 'is-animated': animated }">
    <div class="image-wrapper" @click="$emit('click')">
      <el-image 
        :src="product.images?.[0] || '/placeholder.png'" 
        fit="cover" 
        class="product-image"
        :loading="lazy ? 'lazy' : 'eager'"
        @load="imageLoaded = true"
      >
        <template #placeholder>
          <div class="image-placeholder">
            <el-icon class="is-loading"><Loading /></el-icon>
          </div>
        </template>
      </el-image>
      
      <div v-if="product.is_hot || product.is_recommended || product.discount_rate" class="product-tags">
        <span v-if="product.is_hot" class="tag tag-hot">热销</span>
        <span v-if="product.is_recommended" class="tag tag-recommend">推荐</span>
        <span v-if="product.discount_rate" class="tag tag-discount">{{ product.discount_rate }}折</span>
      </div>

      <transition name="fade">
        <div v-if="showActions" class="product-actions">
          <el-button 
            type="warning" 
            size="small" 
            circle
            @click.stop="$emit('add-to-cart')"
          >
            <el-icon><ShoppingCart /></el-icon>
          </el-button>
          <el-button 
            type="danger" 
            size="small" 
            circle
            @click.stop="$emit('buy-now')"
          >
            <el-icon><ShoppingTrolley /></el-icon>
          </el-button>
        </div>
      </transition>
    </div>

    <div class="product-info" @click="$emit('click')">
      <h3 class="product-name">{{ product.name }}</h3>
      <div class="product-price">
        <span class="current-price text-price">{{ formatPrice(product.price) }}</span>
        <span v-if="product.original_price" class="original-price">¥{{ product.original_price }}</span>
      </div>
      <div class="product-meta">
        <span class="sales">销量 {{ product.sales || 0 }}</span>
        <span v-if="product.stock <= 10 && product.stock > 0" class="low-stock">仅剩{{ product.stock }}</span>
        <span v-else-if="product.stock === 0" class="out-stock">缺货</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Loading, ShoppingCart, ShoppingTrolley } from '@element-plus/icons-vue'
import { formatPrice } from '@/utils/format'

defineProps({
  product: {
    type: Object,
    required: true
  },
  lazy: {
    type: Boolean,
    default: true
  },
  animated: {
    type: Boolean,
    default: true
  }
})

defineEmits(['click', 'add-to-cart', 'buy-now'])

const imageLoaded = ref(false)
const showActions = ref(false)
</script>

<style scoped lang="scss">
.product-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid transparent;

  &:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
    border-color: #409EFF;
  }

  &.is-animated {
    animation: cardEnter 0.5s ease-out forwards;
    opacity: 0;
  }
}

@keyframes cardEnter {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.image-wrapper {
  position: relative;
  overflow: hidden;
  cursor: pointer;
}

.product-image {
  width: 100%;
  height: 220px;
  transition: transform 0.4s ease;

  .product-card:hover & {
    transform: scale(1.05);
  }
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
}

.product-tags {
  position: absolute;
  top: 10px;
  left: 10px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.tag {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.tag-hot { background: linear-gradient(135deg, #ff6b6b, #ee5a5a); color: #fff; }
.tag-recommend { background: linear-gradient(135deg, #f9ca24, #f0932b); color: #fff; }
.tag-discount { background: linear-gradient(135deg, #6ab04c, #22a6b3); color: #fff; }

.product-actions {
  position: absolute;
  bottom: 10px;
  right: 10px;
  display: flex;
  gap: 8px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.product-info {
  padding: 15px;
  cursor: pointer;
}

.product-name {
  margin: 0 0 10px;
  font-size: 15px;
  font-weight: 500;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  transition: color 0.2s;

  &:hover {
    color: #409EFF;
  }
}

.product-price {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 8px;
}

.current-price {
  font-size: 20px;
  font-weight: bold;
}

.original-price {
  color: #999;
  text-decoration: line-through;
  font-size: 13px;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
}

.low-stock {
  color: #e6a23c;
}

.out-stock {
  color: #f56c6c;
}
</style>

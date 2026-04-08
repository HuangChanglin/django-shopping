<template>
  <div class="product-detail container">
    <div v-if="loading" class="loading">
      <el-icon class="is-loading"><Loading /></el-icon>
    </div>
    <template v-else-if="product">
      <div class="product-main">
        <div class="product-images">
          <el-image :src="currentImage" fit="contain" class="main-image" />
          <div class="thumbnail-list">
            <div
              v-for="(img, index) in product.images"
              :key="index"
              class="thumbnail"
              :class="{ active: currentImageIndex === index }"
              @click="currentImageIndex = index"
            >
              <el-image :src="img" fit="cover" />
            </div>
          </div>
        </div>
        <div class="product-info">
          <h1 class="product-name">{{ product.name }}</h1>
          <div class="product-brief">
            <span v-if="product.is_hot" class="tag tag-hot">热销</span>
            <span v-if="product.is_recommended" class="tag tag-recommend">推荐</span>
            <span v-if="product.discount_rate" class="tag tag-discount">{{ product.discount_rate }}折</span>
          </div>
          <div class="product-price-box">
            <div class="price-row">
              <span class="label">价格</span>
              <span class="price text-price">{{ formatPrice(product.price) }}</span>
              <span v-if="product.original_price" class="original-price">¥{{ product.original_price }}</span>
            </div>
            <div class="stat-row">
              <span>销量 {{ product.sales }}</span>
              <span>库存 {{ product.stock }}</span>
              <span>评价 {{ product.review_count }}</span>
            </div>
          </div>
          <div class="product-specs">
            <div v-for="(value, key) in product.specs" :key="key" class="spec-item">
              <span class="spec-label">{{ key }}</span>
              <span class="spec-value">{{ value }}</span>
            </div>
          </div>
          <div class="product-actions">
            <div class="quantity-selector">
              <span>数量</span>
              <el-input-number v-model="quantity" :min="1" :max="product.stock" />
            </div>
            <div class="action-buttons">
              <el-button type="danger" size="large" @click="handleBuyNow">立即购买</el-button>
              <el-button type="warning" size="large" @click="handleAddToCart">加入购物车</el-button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="product-tabs">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="商品详情" name="detail">
            <div class="product-description" v-html="product.description"></div>
          </el-tab-pane>
          <el-tab-pane label="商品评价" name="reviews">
            <div v-if="reviews.length === 0" class="empty-reviews">
              <el-empty description="暂无评价" />
            </div>
            <div v-else class="review-list">
              <div v-for="review in reviews" :key="review.id" class="review-item">
                <div class="review-header">
                  <el-avatar :size="30">{{ review.user_name?.[0] }}</el-avatar>
                  <span class="user-name">{{ review.user_name }}</span>
                  <el-rate :model-value="review.rating" disabled />
                  <span class="review-date">{{ formatDate(review.created_at) }}</span>
                </div>
                <div class="review-content">{{ review.content }}</div>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { productApi } from '@/api'
import { useCartStore } from '@/stores/cart'
import { useUserStore } from '@/stores/user'
import { formatPrice, formatDate } from '@/utils/format'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()
const userStore = useUserStore()

const product = ref(null)
const reviews = ref([])
const loading = ref(false)
const quantity = ref(1)
const currentImageIndex = ref(0)
const activeTab = ref('detail')

const currentImage = computed(() => {
  return product.value?.images?.[currentImageIndex.value] || ''
})

const loadProduct = async () => {
  loading.value = true
  try {
    product.value = await productApi.getDetail(route.params.id)
    currentImageIndex.value = 0
  } catch (error) {
    console.error('Failed to load product:', error)
  } finally {
    loading.value = false
  }
}

const loadReviews = async () => {
  try {
    const res = await productApi.getReviews(route.params.id)
    reviews.value = res.results || res
  } catch (error) {
    console.error('Failed to load reviews:', error)
  }
}

const handleAddToCart = async () => {
  if (!userStore.isLoggedIn) {
    router.push({ name: 'Login', query: { redirect: route.fullPath } })
    return
  }
  try {
    await cartStore.addToCart(product.value.id, quantity.value)
    ElMessage.success('已加入购物车')
  } catch (error) {
    ElMessage.error('加入购物车失败')
  }
}

const handleBuyNow = async () => {
  if (!userStore.isLoggedIn) {
    router.push({ name: 'Login', query: { redirect: route.fullPath } })
    return
  }
  await handleAddToCart()
  router.push({ name: 'Cart' })
}

onMounted(() => {
  loadProduct()
  loadReviews()
})
</script>

<style scoped lang="scss">
.product-detail {
  padding-bottom: 40px;
}

.loading {
  text-align: center;
  padding: 100px;
}

.product-main {
  display: flex;
  gap: 40px;
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.product-images {
  width: 400px;
}

.main-image {
  width: 100%;
  height: 400px;
  border: 1px solid #eee;
  border-radius: 8px;
  margin-bottom: 15px;
}

.thumbnail-list {
  display: flex;
  gap: 10px;
}

.thumbnail {
  width: 60px;
  height: 60px;
  border: 2px solid #eee;
  border-radius: 4px;
  cursor: pointer;
  overflow: hidden;
  
  &.active {
    border-color: #409EFF;
  }
}

.product-info {
  flex: 1;
}

.product-name {
  font-size: 24px;
  margin: 0 0 15px;
}

.product-brief {
  margin-bottom: 20px;
}

.tag {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 12px;
  margin-right: 10px;
}

.tag-hot { background: #F56C6C; color: #fff; }
.tag-recommend { background: #E6A23C; color: #fff; }
.tag-discount { background: #409EFF; color: #fff; }

.product-price-box {
  background: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.price-row {
  display: flex;
  align-items: baseline;
  margin-bottom: 10px;
  
  .label { color: #909399; margin-right: 15px; }
  .price { font-size: 32px; }
  .original-price { color: #909399; text-decoration: line-through; margin-left: 10px; }
}

.stat-row {
  display: flex;
  gap: 30px;
  color: #909399;
  font-size: 14px;
}

.product-specs {
  margin-bottom: 30px;
}

.spec-item {
  display: flex;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
  
  .spec-label { width: 100px; color: #909399; }
  .spec-value { flex: 1; }
}

.product-actions {
  .quantity-selector {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 20px;
  }
  
  .action-buttons {
    display: flex;
    gap: 15px;
    
    .el-button {
      width: 150px;
    }
  }
}

.product-tabs {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
}

.product-description {
  line-height: 1.8;
}

.empty-reviews {
  padding: 50px;
}

.review-list {
  .review-item {
    padding: 20px 0;
    border-bottom: 1px solid #eee;
    
    &:last-child { border-bottom: none; }
  }
}

.review-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
  
  .user-name { font-weight: bold; }
  .review-date { color: #909399; margin-left: auto; }
}

.review-content {
  color: #606266;
  line-height: 1.6;
}
</style>

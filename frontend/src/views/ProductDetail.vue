<template>
  <div class="product-detail container">
    <transition name="fade" mode="out-in">
      <div v-if="loading" key="loading">
        <SkeletonLoader type="detail" />
      </div>
      
      <template v-else-if="product">
        <div key="content" class="product-main">
          <div class="product-images">
            <div class="main-image-container" @mouseenter="handleMouseEnter" @mouseleave="handleMouseLeave" @mousemove="handleMouseMove">
              <el-image 
                :src="currentImage" 
                fit="contain" 
                class="main-image"
                :class="{ 'is-zoomed': isZoomed }"
                preview-src-list=[]
              />
              <div 
                v-if="isZoomed"
                class="zoom-lens"
                :style="zoomLensStyle"
              ></div>
            </div>
            
            <transition name="thumbnail-fade">
              <div v-if="showThumbnails" class="thumbnail-list">
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
            </transition>
          </div>
          
          <div class="product-info">
            <h1 class="product-name">{{ product.name }}</h1>
            
            <div class="product-brief">
              <span v-if="product.is_hot" class="tag tag-hot">
                <el-icon><Fire /></el-icon> 热销
              </span>
              <span v-if="product.is_recommended" class="tag tag-recommend">
                <el-icon><Star /></el-icon> 推荐
              </span>
              <span v-if="product.discount_rate" class="tag tag-discount">
                {{ product.discount_rate }}折
              </span>
            </div>
            
            <div class="product-price-box">
              <div class="price-row">
                <span class="label">价格</span>
                <span class="price text-price">{{ formatPrice(product.price) }}</span>
                <span v-if="product.original_price" class="original-price">
                  ¥{{ product.original_price }}
                </span>
              </div>
              <div class="stat-row">
                <span><el-icon><Goods /></el-icon> 销量 {{ product.sales }}</span>
                <span><el-icon><Box /></el-icon> 库存 {{ product.stock }}</span>
                <span><el-icon><ChatLineSquare /></el-icon> 评价 {{ product.review_count }}</span>
                <span v-if="product.average_rating">
                  <el-icon><Star /></el-icon> {{ product.average_rating }}分
                </span>
              </div>
            </div>
            
            <div v-if="Object.keys(product.specs || {}).length > 0" class="product-specs">
              <div v-for="(value, key) in product.specs" :key="key" class="spec-item">
                <span class="spec-label">{{ key }}</span>
                <span class="spec-value">{{ value }}</span>
              </div>
            </div>
            
            <div class="product-shipping">
              <el-icon><Location /></el-icon>
              <span>配送至：全国大部分地区</span>
              <span class="freight">运费：{{ product.price >= 99 ? '免运费' : '¥10.00' }}</span>
            </div>
            
            <div class="product-actions">
              <div class="quantity-selector">
                <span class="label">数量</span>
                <el-input-number 
                  v-model="quantity" 
                  :min="1" 
                  :max="product.stock" 
                  size="large"
                />
                <span class="stock-tip" v-if="product.stock <= 10 && product.stock > 0">
                  仅剩 {{ product.stock }} 件
                </span>
              </div>
              
              <div class="action-buttons">
                <el-button type="danger" size="large" class="buy-btn" @click="handleBuyNow">
                  <el-icon><ShoppingTrolley /></el-icon>
                  立即购买
                </el-button>
                <el-button type="warning" size="large" class="cart-btn" @click="handleAddToCart">
                  <el-icon><ShoppingCart /></el-icon>
                  加入购物车
                </el-button>
              </div>
              
              <div class="action-tips">
                <span><el-icon><CircleCheck /></el-icon> 7天无理由退货</span>
                <span><el-icon><CircleCheck /></el-icon> 48小时发货</span>
                <span><el-icon><CircleCheck /></el-icon> 正品保障</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="product-tabs">
          <el-tabs v-model="activeTab" class="product-tabs-content">
            <el-tab-pane label="商品详情" name="detail">
              <div class="product-description" v-html="product.description || '<p>暂无商品描述</p>'"></div>
            </el-tab-pane>
            <el-tab-pane label="商品评价" name="reviews">
              <template #label>
                <span class="tab-label">
                  商品评价
                  <el-badge :value="product.review_count" type="primary" />
                </span>
              </template>
              
              <div v-if="reviews.length === 0" class="empty-reviews">
                <el-empty description="暂无评价，成为第一个评价的人吧！" />
              </div>
              <div v-else class="review-list">
                <div v-for="review in reviews" :key="review.id" class="review-item">
                  <div class="review-header">
                    <el-avatar :size="40">{{ review.user_name?.[0] }}</el-avatar>
                    <div class="review-user">
                      <span class="user-name">{{ review.user_name }}</span>
                      <el-rate :model-value="review.rating" disabled size="small" />
                    </div>
                    <span class="review-date">{{ formatDate(review.created_at) }}</span>
                  </div>
                  <div class="review-content">{{ review.content }}</div>
                  <div v-if="review.images?.length" class="review-images">
                    <el-image
                      v-for="(img, i) in review.images"
                      :key="i"
                      :src="img"
                      fit="cover"
                      class="review-image"
                      :preview-src-list="review.images"
                    />
                  </div>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </template>
    </transition>
    
    <ScrollToTop />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  Fire, Star, Goods, Box, ChatLineSquare, Location,
  ShoppingTrolley, ShoppingCart, CircleCheck 
} from '@element-plus/icons-vue'
import { productApi } from '@/api'
import { useCartStore } from '@/stores/cart'
import { useUserStore } from '@/stores/user'
import { formatPrice, formatDate } from '@/utils/format'
import SkeletonLoader from '@/components/SkeletonLoader.vue'
import ScrollToTop from '@/components/ScrollToTop.vue'

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
const isZoomed = ref(false)
const showThumbnails = ref(true)
const zoomLensStyle = ref({})

const currentImage = computed(() => product.value?.images?.[currentImageIndex.value] || '')

const handleMouseEnter = () => {
  isZoomed.value = true
}

const handleMouseLeave = () => {
  isZoomed.value = false
}

const handleMouseMove = (e) => {
  const rect = e.target.getBoundingClientRect()
  const x = ((e.clientX - rect.left) / rect.width) * 100
  const y = ((e.clientY - rect.top) / rect.height) * 100
  zoomLensStyle.value = {
    left: `${x}%`,
    top: `${y}%`
  }
}

const loadProduct = async () => {
  loading.value = true
  try {
    product.value = await productApi.getDetail(route.params.id)
    currentImageIndex.value = 0
    document.title = `${product.value.name} - 网上商城`
  } catch (error) {
    ElMessage.error('加载商品失败')
  } finally {
    setTimeout(() => { loading.value = false }, 300)
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
    ElMessage.success({ message: '已加入购物车', duration: 1500 })
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

.product-main {
  display: flex;
  gap: 40px;
  background: #fff;
  padding: 30px;
  border-radius: 16px;
  margin-bottom: 20px;
}

.product-images {
  width: 450px;
  flex-shrink: 0;
}

.main-image-container {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  background: #f5f5f5;
  cursor: zoom-in;
}

.main-image {
  width: 100%;
  height: 450px;
  transition: transform 0.3s ease;
  
  &.is-zoomed {
    transform: scale(1.2);
  }
}

.zoom-lens {
  position: absolute;
  width: 80px;
  height: 80px;
  background: rgba(64, 158, 255, 0.3);
  border: 2px solid #409EFF;
  border-radius: 50%;
  pointer-events: none;
  transform: translate(-50%, -50%);
}

.thumbnail-list {
  display: flex;
  gap: 10px;
  margin-top: 15px;
  justify-content: center;
}

.thumbnail {
  width: 70px;
  height: 70px;
  border: 2px solid #eee;
  border-radius: 8px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.2s;
  
  &:hover {
    border-color: #409EFF;
  }
  
  &.active {
    border-color: #409EFF;
    box-shadow: 0 0 10px rgba(64, 158, 255, 0.3);
  }
}

.thumbnail-fade-enter-active,
.thumbnail-fade-leave-active {
  transition: all 0.3s ease;
}

.thumbnail-fade-enter-from,
.thumbnail-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.product-info {
  flex: 1;
}

.product-name {
  font-size: 26px;
  font-weight: 600;
  margin: 0 0 15px;
  color: #333;
}

.product-brief {
  margin-bottom: 20px;
  
  .tag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    margin-right: 10px;
  }
  
  .tag-hot { background: linear-gradient(135deg, #ff6b6b, #ee5a5a); color: #fff; }
  .tag-recommend { background: linear-gradient(135deg, #f9ca24, #f0932b); color: #fff; }
  .tag-discount { background: linear-gradient(135deg, #6ab04c, #22a6b3); color: #fff; }
}

.product-price-box {
  background: linear-gradient(135deg, #fef5f5, #fff5f5);
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 20px;
}

.price-row {
  display: flex;
  align-items: baseline;
  gap: 15px;
  margin-bottom: 15px;
  
  .label { color: #666; }
  .price { font-size: 36px; font-weight: bold; }
  .original-price { color: #999; text-decoration: line-through; font-size: 16px; }
}

.stat-row {
  display: flex;
  gap: 25px;
  color: #666;
  font-size: 14px;
  
  .el-icon { margin-right: 4px; }
}

.product-specs {
  margin-bottom: 20px;
  
  .spec-item {
    display: flex;
    padding: 12px 0;
    border-bottom: 1px solid #f0f0f0;
    
    &:last-child { border-bottom: none; }
  }
  
  .spec-label { width: 100px; color: #999; }
  .spec-value { flex: 1; color: #333; }
}

.product-shipping {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 15px;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 25px;
  font-size: 14px;
  color: #666;
  
  .freight { margin-left: auto; color: #67C23A; }
}

.product-actions {
  .quantity-selector {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 20px;
    
    .label { color: #666; }
    .stock-tip { color: #e6a23c; font-size: 14px; }
  }
  
  .action-buttons {
    display: flex;
    gap: 15px;
    margin-bottom: 20px;
    
    .buy-btn, .cart-btn {
      flex: 1;
      height: 50px;
      font-size: 16px;
      
      .el-icon { margin-right: 8px; }
    }
  }
  
  .action-tips {
    display: flex;
    gap: 25px;
    color: #999;
    font-size: 13px;
    
    .el-icon { color: #67C23A; margin-right: 4px; }
  }
}

.product-tabs {
  background: #fff;
  padding: 20px;
  border-radius: 16px;
}

.product-tabs-content {
  :deep(.el-tabs__header) {
    margin-bottom: 20px;
  }
  
  :deep(.el-tabs__nav-wrap::after) {
    height: 1px;
  }
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.product-description {
  line-height: 1.8;
  color: #666;
  padding: 20px;
}

.empty-reviews {
  padding: 60px;
}

.review-list {
  .review-item {
    padding: 20px 0;
    border-bottom: 1px solid #f0f0f0;
    
    &:last-child { border-bottom: none; }
  }
}

.review-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.review-user {
  flex: 1;
  
  .user-name { display: block; margin-bottom: 4px; font-weight: 500; }
}

.review-date { color: #999; font-size: 13px; }

.review-content {
  color: #333;
  line-height: 1.6;
  margin-bottom: 10px;
}

.review-images {
  display: flex;
  gap: 10px;
}

.review-image {
  width: 80px;
  height: 80px;
  border-radius: 6px;
  cursor: pointer;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

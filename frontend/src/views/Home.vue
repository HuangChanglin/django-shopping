<template>
  <div class="home container">
    <transition name="fade" mode="out-in">
      <div v-if="loading" key="loading">
        <el-carousel height="400px" :interval="5000" class="banner-skeleton">
          <el-carousel-item v-for="i in 3" :key="i">
            <div class="skeleton-banner skeleton-pulse"></div>
          </el-carousel-item>
        </el-carousel>
      </div>
      <div v-else key="content">
        <el-carousel height="400px" :interval="5000" trigger="click" class="banner-carousel">
          <el-carousel-item v-for="(banner, index) in banners" :key="index">
            <div class="banner" :style="{ background: banner.color }">
              <div class="banner-content">
                <h2 class="banner-title">{{ banner.title }}</h2>
                <p class="banner-subtitle">{{ banner.subtitle }}</p>
                <el-button type="primary" size="large" round @click="handleBannerClick(banner)">
                  {{ banner.buttonText }}
                </el-button>
              </div>
            </div>
          </el-carousel-item>
        </el-carousel>
      </div>
    </transition>

    <section class="section">
      <div class="section-header">
        <div class="section-title">
          <el-icon><Fire /></el-icon>
          <h2>热门商品</h2>
        </div>
        <router-link to="/products?is_hot=1" class="more-link">
          查看更多 <el-icon><ArrowRight /></el-icon>
        </router-link>
      </div>
      <transition-group name="list" tag="div" class="product-grid">
        <ProductCard
          v-for="(product, index) in hotProducts"
          :key="product.id"
          :product="product"
          :style="{ '--delay': `${index * 0.1}s` }"
          @click="goDetail(product.id)"
          @add-to-cart="handleAddToCart(product)"
        />
      </transition-group>
    </section>

    <section class="section">
      <div class="section-header">
        <div class="section-title">
          <el-icon><Star /></el-icon>
          <h2>为你推荐</h2>
        </div>
        <router-link to="/products?is_recommended=1" class="more-link">
          查看更多 <el-icon><ArrowRight /></el-icon>
        </router-link>
      </div>
      <transition-group name="list" tag="div" class="product-grid">
        <ProductCard
          v-for="(product, index) in recommendedProducts"
          :key="product.id"
          :product="product"
          :style="{ '--delay': `${index * 0.1}s` }"
          @click="goDetail(product.id)"
          @add-to-cart="handleAddToCart(product)"
        />
      </transition-group>
    </section>

    <ScrollToTop />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Fire, Star, ArrowRight } from '@element-plus/icons-vue'
import { productApi } from '@/api'
import { useCartStore } from '@/stores/cart'
import { useUserStore } from '@/stores/user'
import ProductCard from '@/components/ProductCard.vue'
import ScrollToTop from '@/components/ScrollToTop.vue'

const router = useRouter()
const cartStore = useCartStore()
const userStore = useUserStore()

const loading = ref(true)
const hotProducts = ref([])
const recommendedProducts = ref([])

const banners = [
  { 
    title: '新人专享', 
    subtitle: '首单满100减20，优惠多多', 
    color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    buttonText: '立即领取',
    action: () => router.push('/register')
  },
  { 
    title: '限时秒杀', 
    subtitle: '每天10点准时开抢，优惠不容错过', 
    color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    buttonText: '立即抢购',
    action: () => router.push('/products')
  },
  { 
    title: '品质保障', 
    subtitle: '7天无理由退换货，放心购物', 
    color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    buttonText: '了解更多',
    action: () => {}
  }
]

const handleBannerClick = (banner) => {
  if (banner.action) banner.action()
}

const loadProducts = async () => {
  loading.value = true
  try {
    const [hotRes, recRes] = await Promise.all([
      productApi.getHot(),
      productApi.getRecommended()
    ])
    hotProducts.value = hotRes
    recommendedProducts.value = recRes
  } catch (error) {
    ElMessage.error('加载商品失败')
  } finally {
    setTimeout(() => { loading.value = false }, 300)
  }
}

const goDetail = (id) => {
  router.push({ name: 'ProductDetail', params: { id } })
}

const handleAddToCart = async (product) => {
  if (!userStore.isLoggedIn) {
    router.push({ name: 'Login' })
    return
  }
  try {
    await cartStore.addToCart(product.id, 1)
    ElMessage.success('已加入购物车')
  } catch (error) {
    ElMessage.error('加入购物车失败')
  }
}

onMounted(loadProducts)
</script>

<style scoped lang="scss">
.skeleton-banner {
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.banner-carousel {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.banner {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.banner-content {
  text-align: center;
  animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.banner-title {
  font-size: 56px;
  margin-bottom: 15px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.banner-subtitle {
  font-size: 22px;
  margin-bottom: 30px;
  opacity: 0.9;
}

.section {
  margin-top: 50px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;

  h2 {
    margin: 0;
    font-size: 24px;
  }

  .el-icon {
    font-size: 24px;
    color: #409EFF;
  }
}

.more-link {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #666;
  text-decoration: none;
  transition: color 0.2s;

  &:hover {
    color: #409EFF;
  }
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
}

.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.list-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.list-move {
  transition: transform 0.5s ease;
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

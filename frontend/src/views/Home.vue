<template>
  <div class="home container">
    <el-carousel height="400px" :interval="5000">
      <el-carousel-item v-for="(banner, index) in banners" :key="index">
        <div class="banner" :style="{ background: banner.color }">
          <h2>{{ banner.title }}</h2>
          <p>{{ banner.subtitle }}</p>
        </div>
      </el-carousel-item>
    </el-carousel>

    <section class="section">
      <div class="section-header">
        <h2>热门商品</h2>
        <router-link to="/products?is_hot=1">查看更多</router-link>
      </div>
      <div class="product-grid">
        <div v-for="product in hotProducts" :key="product.id" class="product-card goods-card" @click="goDetail(product.id)">
          <el-image :src="product.images[0]" fit="cover" class="product-image" />
          <div class="product-info">
            <h3 class="product-name">{{ product.name }}</h3>
            <div class="product-price">
              <span class="current-price text-price">{{ formatPrice(product.price) }}</span>
              <span v-if="product.original_price" class="original-price">¥{{ product.original_price }}</span>
            </div>
            <div class="product-meta">
              <span>销量 {{ product.sales }}</span>
              <span v-if="product.discount_rate">折扣 {{ product.discount_rate }}%</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-header">
        <h2>推荐商品</h2>
        <router-link to="/products?is_recommended=1">查看更多</router-link>
      </div>
      <div class="product-grid">
        <div v-for="product in recommendedProducts" :key="product.id" class="product-card goods-card" @click="goDetail(product.id)">
          <el-image :src="product.images[0]" fit="cover" class="product-image" />
          <div class="product-info">
            <h3 class="product-name">{{ product.name }}</h3>
            <div class="product-price">
              <span class="current-price text-price">{{ formatPrice(product.price) }}</span>
              <span v-if="product.original_price" class="original-price">¥{{ product.original_price }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { productApi } from '@/api'
import { formatPrice } from '@/utils/format'

const router = useRouter()
const hotProducts = ref([])
const recommendedProducts = ref([])

const banners = [
  { title: '新人专享', subtitle: '首单满100减20', color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
  { title: '限时秒杀', subtitle: '每天10点准时开抢', color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' },
  { title: '品质保障', subtitle: '7天无理由退换货', color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' }
]

const loadProducts = async () => {
  try {
    const [hotRes, recRes] = await Promise.all([
      productApi.getHot(),
      productApi.getRecommended()
    ])
    hotProducts.value = hotRes
    recommendedProducts.value = recRes
  } catch (error) {
    console.error('Failed to load products:', error)
  }
}

const goDetail = (id) => {
  router.push({ name: 'ProductDetail', params: { id } })
}

onMounted(loadProducts)
</script>

<style scoped lang="scss">
.home {
  padding-bottom: 40px;
}

.banner {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #fff;
  text-align: center;

  h2 {
    font-size: 48px;
    margin-bottom: 10px;
  }

  p {
    font-size: 20px;
  }
}

.section {
  margin-top: 40px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #409EFF;

  h2 {
    margin: 0;
  }

  a {
    color: #409EFF;
    text-decoration: none;
  }
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
}

.product-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
}

.product-image {
  width: 100%;
  height: 200px;
}

.product-info {
  padding: 15px;
}

.product-name {
  margin: 0 0 10px;
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-price {
  margin-bottom: 8px;
}

.current-price {
  font-size: 18px;
  margin-right: 10px;
}

.original-price {
  color: #909399;
  text-decoration: line-through;
  font-size: 12px;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #909399;
}
</style>

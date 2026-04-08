<template>
  <div class="products container">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h3>商品分类</h3>
      </div>
      <el-menu :default-active="categoryId" @select="handleCategoryChange" class="category-menu">
        <el-menu-item index="">
          <el-icon><Shop /></el-icon>
          <span>全部分类</span>
        </el-menu-item>
        <el-menu-item v-for="cat in categories" :key="cat.id" :index="String(cat.id)">
          <el-icon><Goods /></el-icon>
          <span>{{ cat.name }}</span>
          <span class="cat-count">{{ cat.product_count }}</span>
        </el-menu-item>
      </el-menu>
    </aside>
    
    <main class="content">
      <div class="toolbar">
        <div class="toolbar-left">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索商品..."
            class="search-input"
            clearable
            @keyup.enter="handleSearch"
            @clear="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
            <template #append>
              <el-button @click="handleSearch">搜索</el-button>
            </template>
          </el-input>
          
          <div class="filter-chips">
            <el-check-tag :checked="isHot" @change="toggleFilter('isHot')">热销</el-check-tag>
            <el-check-tag :checked="isRecommended" @change="toggleFilter('isRecommended')">推荐</el-check-tag>
          </div>
        </div>
        
        <div class="toolbar-right">
          <span class="total-count">共 {{ total }} 件商品</span>
          <el-select v-model="sortOrder" placeholder="排序" @change="handleSortChange">
            <el-option label="综合排序" value="" />
            <el-option label="价格从低到高" value="price" />
            <el-option label="价格从高到低" value="-price" />
            <el-option label="销量优先" value="-sales" />
            <el-option label="最新上架" value="-created_at" />
          </el-select>
        </div>
      </div>
      
      <div v-if="loading" class="loading-container">
        <div class="product-grid">
          <SkeletonLoader v-for="i in 8" :key="i" type="card" />
        </div>
      </div>
      
      <div v-else-if="products.length === 0" class="empty-container">
        <el-empty description="暂无商品" :image-size="200">
          <el-button type="primary" @click="resetFilters">重置筛选</el-button>
        </el-empty>
      </div>
      
      <transition-group
        v-else
        name="list"
        tag="div"
        class="product-grid"
        appear
      >
        <ProductCard
          v-for="(product, index) in products"
          :key="product.id"
          :product="product"
          :style="{ '--delay': `${index * 0.05}s` }"
          @click="goDetail(product.id)"
          @add-to-cart="handleAddToCart(product)"
        />
      </transition-group>
      
      <div v-if="total > pageSize && !loading" class="load-more">
        <el-button
          v-if="hasMore"
          :loading="loadingMore"
          @click="loadMore"
          class="load-more-btn"
        >
          加载更多
        </el-button>
        <span v-else class="no-more">没有更多了</span>
      </div>
    </main>
    
    <ScrollToTop />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, Shop, Goods } from '@element-plus/icons-vue'
import { productApi } from '@/api'
import { useCartStore } from '@/stores/cart'
import { useUserStore } from '@/stores/user'
import ProductCard from '@/components/ProductCard.vue'
import SkeletonLoader from '@/components/SkeletonLoader.vue'
import ScrollToTop from '@/components/ScrollToTop.vue'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()
const userStore = useUserStore()

const products = ref([])
const categories = ref([])
const loading = ref(false)
const loadingMore = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const categoryId = ref('')
const isHot = ref(false)
const isRecommended = ref(false)
const searchKeyword = ref('')
const sortOrder = ref('')

const hasMore = computed(() => products.value.length < total.value)

const loadCategories = async () => {
  try {
    categories.value = await productApi.getCategories()
  } catch (error) {
    console.error('Failed to load categories:', error)
  }
}

const loadProducts = async (append = false) => {
  if (append) {
    loadingMore.value = true
  } else {
    loading.value = true
  }
  
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchKeyword.value || undefined,
      category: categoryId.value || undefined,
      is_hot: isHot.value || undefined,
      is_recommended: isRecommended.value || undefined,
      ordering: sortOrder.value || undefined
    }
    
    const res = await productApi.getList(params)
    
    if (append) {
      products.value = [...products.value, ...(res.results || res)]
    } else {
      products.value = res.results || res
    }
    total.value = res.count || res.length || products.value.length
  } catch (error) {
    ElMessage.error('加载商品失败')
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

const loadMore = () => {
  if (hasMore.value && !loadingMore.value) {
    currentPage.value++
    loadProducts(true)
  }
}

const handleCategoryChange = (id) => {
  categoryId.value = id
  currentPage.value = 1
  loadProducts()
}

const handleSearch = () => {
  currentPage.value = 1
  loadProducts()
}

const toggleFilter = (filter) => {
  if (filter === 'isHot') isHot.value = !isHot.value
  if (filter === 'isRecommended') isRecommended.value = !isRecommended.value
  currentPage.value = 1
  loadProducts()
}

const handleSortChange = () => {
  currentPage.value = 1
  loadProducts()
}

const resetFilters = () => {
  categoryId.value = ''
  isHot.value = false
  isRecommended.value = false
  searchKeyword.value = ''
  sortOrder.value = ''
  currentPage.value = 1
  loadProducts()
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

const handleScroll = () => {
  if (!hasMore.value || loadingMore.value || loading.value) return
  
  const scrollTop = window.scrollY
  const scrollHeight = document.documentElement.scrollHeight
  const clientHeight = window.innerHeight
  
  if (scrollHeight - scrollTop - clientHeight < 300) {
    loadMore()
  }
}

watch(() => route.query, () => {
  searchKeyword.value = route.query.search || ''
  isHot.value = route.query.is_hot === 'true'
  isRecommended.value = route.query.is_recommended === 'true'
  categoryId.value = route.query.category || ''
  currentPage.value = 1
  loadProducts()
}, { immediate: true })

onMounted(() => {
  loadCategories()
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped lang="scss">
.products {
  display: flex;
  gap: 25px;
  padding-bottom: 40px;
}

.sidebar {
  width: 220px;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  flex-shrink: 0;
  position: sticky;
  top: 90px;
  height: fit-content;
  max-height: calc(100vh - 110px);
  overflow-y: auto;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
  
  h3 {
    margin: 0;
    font-size: 16px;
  }
}

.category-menu {
  border-right: none;
  
  .cat-count {
    margin-left: auto;
    font-size: 12px;
    color: #999;
  }
}

.content {
  flex: 1;
  min-width: 0;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  background: #fff;
  padding: 15px 20px;
  border-radius: 12px;
  flex-wrap: wrap;
  gap: 15px;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.search-input {
  width: 280px;
}

.filter-chips {
  display: flex;
  gap: 10px;
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.total-count {
  color: #999;
  font-size: 14px;
}

.loading-container,
.empty-container {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.list-move {
  transition: transform 0.5s ease;
}

.load-more {
  text-align: center;
  margin-top: 30px;
}

.load-more-btn {
  padding: 12px 60px;
}

.no-more {
  color: #999;
  font-size: 14px;
}
</style>

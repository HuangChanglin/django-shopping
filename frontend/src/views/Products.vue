<template>
  <div class="products container">
    <aside class="sidebar">
      <h3>商品分类</h3>
      <el-menu :default-active="categoryId" @select="handleCategoryChange">
        <el-menu-item index="">全部分类</el-menu-item>
        <el-menu-item v-for="cat in categories" :key="cat.id" :index="String(cat.id)">
          {{ cat.name }}
        </el-menu-item>
      </el-menu>
    </aside>
    <main class="content">
      <div class="toolbar">
        <div class="filter-group">
          <el-select v-model="isHot" placeholder="是否热销" clearable @change="loadProducts">
            <el-option label="热销" :value="true" />
          </el-select>
          <el-select v-model="isRecommended" placeholder="是否推荐" clearable @change="loadProducts">
            <el-option label="推荐" :value="true" />
          </el-select>
        </div>
        <el-input v-model="searchKeyword" placeholder="搜索商品" style="width: 200px;" @keyup.enter="loadProducts" />
      </div>
      
      <div v-if="loading" class="loading">
        <el-icon class="is-loading"><Loading /></el-icon>
      </div>
      
      <div v-else-if="products.length === 0" class="empty">
        <el-empty description="暂无商品" />
      </div>
      
      <div v-else class="product-grid">
        <div v-for="product in products" :key="product.id" class="product-card goods-card" @click="goDetail(product.id)">
          <el-image :src="product.images[0]" fit="cover" class="product-image" />
          <div class="product-info">
            <h3 class="product-name">{{ product.name }}</h3>
            <div class="product-price">
              <span class="current-price text-price">{{ formatPrice(product.price) }}</span>
              <span v-if="product.original_price" class="original-price">¥{{ product.original_price }}</span>
            </div>
            <div class="product-meta">
              <span>库存 {{ product.stock }}</span>
              <span>销量 {{ product.sales }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="loadProducts"
        />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productApi } from '@/api'
import { formatPrice } from '@/utils/format'

const route = useRoute()
const router = useRouter()

const products = ref([])
const categories = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const categoryId = ref('')
const isHot = ref(false)
const isRecommended = ref(false)
const searchKeyword = ref('')

const loadCategories = async () => {
  try {
    categories.value = await productApi.getCategories()
  } catch (error) {
    console.error('Failed to load categories:', error)
  }
}

const loadProducts = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      search: searchKeyword.value || undefined,
      category: categoryId.value || undefined,
      is_hot: isHot.value || undefined,
      is_recommended: isRecommended.value || undefined
    }
    const res = await productApi.getList(params)
    products.value = res.results || res
    total.value = res.count || res.length
  } catch (error) {
    console.error('Failed to load products:', error)
  } finally {
    loading.value = false
  }
}

const handleCategoryChange = (id) => {
  categoryId.value = id
  currentPage.value = 1
  loadProducts()
}

const goDetail = (id) => {
  router.push({ name: 'ProductDetail', params: { id } })
}

watch(() => route.query, () => {
  searchKeyword.value = route.query.search || ''
  isHot.value = route.query.is_hot === 'true'
  isRecommended.value = route.query.is_recommended === 'true'
  categoryId.value = route.query.category || ''
  loadProducts()
}, { immediate: true })

onMounted(() => {
  loadCategories()
})
</script>

<style scoped lang="scss">
.products {
  display: flex;
  gap: 20px;
}

.sidebar {
  width: 200px;
  background: #fff;
  padding: 20px;
  border-radius: 8px;

  h3 {
    margin: 0 0 15px;
  }
}

.content {
  flex: 1;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  background: #fff;
  padding: 15px;
  border-radius: 8px;
}

.loading {
  text-align: center;
  padding: 50px;
}

.empty {
  background: #fff;
  padding: 50px;
  border-radius: 8px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.product-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
}

.product-image {
  width: 100%;
  height: 180px;
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

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>

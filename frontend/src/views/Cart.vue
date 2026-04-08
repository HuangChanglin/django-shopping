<template>
  <div class="cart container">
    <h2 class="page-header">
      <el-icon><ShoppingCart /></el-icon>
      我的购物车
    </h2>
    
    <transition name="fade" mode="out-in">
      <div v-if="loading" key="loading" class="loading-container">
        <SkeletonLoader type="list" :count="3" />
      </div>
      
      <div v-else-if="cartStore.items.length === 0" key="empty" class="empty-cart">
        <div class="empty-content">
          <el-icon class="empty-icon"><ShoppingCart /></el-icon>
          <h3>购物车是空的</h3>
          <p>快去挑选心仪的商品吧！</p>
          <el-button type="primary" size="large" @click="$router.push('/products')">
            去逛逛
          </el-button>
        </div>
      </div>
      
      <template v-else key="content">
        <div class="cart-table">
          <div class="table-header">
            <el-checkbox 
              v-model="selectAll" 
              @change="handleSelectAll"
              class="select-all"
            >
              全选
            </el-checkbox>
            <span class="col-info">商品信息</span>
            <span class="col-price">单价</span>
            <span class="col-quantity">数量</span>
            <span class="col-subtotal">小计</span>
            <span class="col-action">操作</span>
          </div>
          
          <transition-group name="list" tag="div" class="cart-items">
            <div 
              v-for="item in cartStore.items" 
              :key="item.id" 
              class="table-row"
              :class="{ 'is-selected': isSelected(item.id) }"
            >
              <el-checkbox 
                :model-value="isSelected(item.id)" 
                @change="toggleSelect(item.id)"
              />
              <div class="col-info">
                <el-image 
                  :src="item.product_detail?.images?.[0]" 
                  fit="cover" 
                  class="product-image"
                  @click="$router.push(`/products/${item.product_detail?.id}`)"
                />
                <div class="product-info">
                  <h4 @click="$router.push(`/products/${item.product_detail?.id}`)">
                    {{ item.product_detail?.name }}
                  </h4>
                  <p v-if="item.selected_specs">
                    规格: {{ formatSpecs(item.selected_specs) }}
                  </p>
                </div>
              </div>
              <span class="col-price text-price">
                {{ formatPrice(item.product_detail?.price) }}
              </span>
              <div class="col-quantity">
                <el-input-number
                  v-model="item.quantity"
                  :min="1"
                  :max="item.product_detail?.stock"
                  size="small"
                  @change="handleQuantityChange(item)"
                />
              </div>
              <span class="col-subtotal text-price">
                {{ formatPrice(item.subtotal) }}
              </span>
              <div class="col-action">
                <el-button 
                  type="primary" 
                  text 
                  @click="handleAddToWishlist(item)"
                >
                  <el-icon><Star /></el-icon>
                </el-button>
                <el-button 
                  type="danger" 
                  text 
                  @click="handleRemove(item.id)"
                >
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
            </div>
          </transition-group>
        </div>
        
        <div class="cart-footer">
          <div class="footer-left">
            <el-checkbox v-model="selectAll" @change="handleSelectAll">全选</el-checkbox>
            <el-button 
              type="text" 
              :disabled="selectedIds.length === 0"
              @click="handleBatchDelete"
            >
              删除选中
            </el-button>
            <el-button type="text" @click="handleClearCart">清空购物车</el-button>
          </div>
          <div class="footer-right">
            <div class="summary-info">
              <p class="summary-count">
                已选 <span class="highlight">{{ selectedCount }}</span> 件商品，共 <span class="highlight">{{ selectedQuantity }}</span> 件
              </p>
              <div class="summary-amount">
                <span>合计：</span>
                <span class="total-price text-price">{{ formatPrice(selectedAmount) }}</span>
              </div>
            </div>
            <el-button 
              type="danger" 
              size="large" 
              :disabled="selectedCount === 0"
              @click="handleCheckout"
              class="checkout-btn"
            >
              结算 ({{ selectedCount }})
            </el-button>
          </div>
        </div>
      </template>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ShoppingCart, Star, Delete } from '@element-plus/icons-vue'
import { useCartStore } from '@/stores/cart'
import SkeletonLoader from '@/components/SkeletonLoader.vue'

const router = useRouter()
const cartStore = useCartStore()

const loading = ref(false)
const selectedIds = ref([])

const selectAll = computed({
  get: () => cartStore.items.length > 0 && selectedIds.value.length === cartStore.items.length,
  set: (val) => {
    selectedIds.value = val ? cartStore.items.map(i => i.id) : []
  }
})

const selectedItems = computed(() => 
  cartStore.items.filter(item => selectedIds.value.includes(item.id))
)

const selectedCount = computed(() => selectedItems.value.length)
const selectedQuantity = computed(() => 
  selectedItems.value.reduce((sum, i) => sum + i.quantity, 0)
)
const selectedAmount = computed(() => 
  selectedItems.value.reduce((sum, i) => sum + Number(i.subtotal), 0)
)

const isSelected = (id) => selectedIds.value.includes(id)
const toggleSelect = (id) => {
  const index = selectedIds.value.indexOf(id)
  if (index > -1) {
    selectedIds.value.splice(index, 1)
  } else {
    selectedIds.value.push(id)
  }
}

const formatSpecs = (specs) => {
  if (!specs) return ''
  if (typeof specs === 'string') return specs
  return Object.entries(specs).map(([k, v]) => `${k}: ${v}`).join(', ')
}

const formatPrice = (price) => {
  return `¥${Number(price || 0).toFixed(2)}`
}

const loadCart = async () => {
  loading.value = true
  try {
    await cartStore.getCartList()
    selectedIds.value = []
  } catch (error) {
    ElMessage.error('加载购物车失败')
  } finally {
    setTimeout(() => { loading.value = false }, 300)
  }
}

const handleQuantityChange = async (item) => {
  try {
    await cartStore.updateQuantity(item.id, item.quantity)
  } catch (error) {
    ElMessage.error('更新数量失败')
  }
}

const handleRemove = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该商品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await cartStore.removeItem(id)
    selectedIds.value = selectedIds.value.filter(i => i !== id)
    ElMessage.success({ message: '删除成功', duration: 1500 })
  } catch {}
}

const handleSelectAll = (val) => {
  selectedIds.value = val ? cartStore.items.map(i => i.id) : []
}

const handleBatchDelete = async () => {
  if (selectedIds.value.length === 0) {
    ElMessage.warning('请选择要删除的商品')
    return
  }
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 件商品吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await cartStore.batchDelete(selectedIds.value)
    selectedIds.value = []
    ElMessage.success({ message: '删除成功', duration: 1500 })
  } catch {}
}

const handleClearCart = async () => {
  try {
    await ElMessageBox.confirm('确定要清空购物车吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await cartStore.clearCart()
    ElMessage.success({ message: '购物车已清空', duration: 1500 })
  } catch {}
}

const handleAddToWishlist = (item) => {
  ElMessage.info('收藏功能开发中...')
}

const handleCheckout = () => {
  const ids = selectedIds.value.join(',')
  router.push({ name: 'Checkout', query: { ids } })
}

onMounted(loadCart)
</script>

<style scoped lang="scss">
.page-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 25px;
  
  .el-icon {
    font-size: 28px;
    color: #409EFF;
  }
}

.loading-container {
  background: #fff;
  padding: 20px;
  border-radius: 12px;
}

.empty-cart {
  background: #fff;
  border-radius: 12px;
  padding: 80px;
}

.empty-content {
  text-align: center;
  
  .empty-icon {
    font-size: 100px;
    color: #dcdfe6;
    margin-bottom: 20px;
  }
  
  h3 {
    margin: 0 0 10px;
    font-size: 20px;
  }
  
  p {
    color: #999;
    margin-bottom: 25px;
  }
}

.cart-table {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
}

.table-header {
  display: flex;
  align-items: center;
  padding: 18px 20px;
  background: #f5f7fa;
  font-weight: 500;
  color: #666;
  
  .select-all {
    width: 80px;
  }
}

.cart-items {
  position: relative;
}

.table-row {
  display: flex;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
  transition: all 0.3s ease;
  
  &:last-child { border-bottom: none; }
  
  &:hover {
    background: #fafafa;
  }
  
  &.is-selected {
    background: #f0f7ff;
  }
}

.col-info {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 15px;
}

.product-image {
  width: 90px;
  height: 90px;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s;
  
  &:hover {
    transform: scale(1.05);
  }
}

.product-info {
  flex: 1;
  
  h4 {
    margin: 0 0 8px;
    cursor: pointer;
    transition: color 0.2s;
    
    &:hover {
      color: #409EFF;
    }
  }
  
  p {
    margin: 0;
    color: #999;
    font-size: 13px;
  }
}

.col-price { width: 100px; text-align: center; font-size: 15px; }
.col-quantity { width: 130px; text-align: center; }
.col-subtotal { width: 100px; text-align: center; font-size: 16px; font-weight: bold; }
.col-action { width: 100px; text-align: center; }

.cart-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  padding: 20px 25px;
  background: #fff;
  border-radius: 12px;
}

.footer-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.footer-right {
  display: flex;
  align-items: center;
  gap: 30px;
}

.summary-info {
  text-align: right;
  
  .summary-count {
    color: #666;
    margin: 0 0 5px;
    
    .highlight {
      color: #409EFF;
      font-weight: bold;
    }
  }
  
  .summary-amount {
    font-size: 14px;
    
    .total-price {
      font-size: 24px;
      font-weight: bold;
    }
  }
}

.checkout-btn {
  padding: 15px 50px;
  font-size: 16px;
}

.list-enter-active,
.list-leave-active {
  transition: all 0.4s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

.list-move {
  transition: transform 0.4s ease;
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

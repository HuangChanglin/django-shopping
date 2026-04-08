<template>
  <div class="cart container">
    <h2 class="page-header">我的购物车</h2>
    
    <div v-if="loading" class="loading">
      <el-icon class="is-loading"><Loading /></el-icon>
    </div>
    
    <div v-else-if="cartStore.items.length === 0" class="empty-cart">
      <el-empty description="购物车是空的">
        <el-button type="primary" @click="$router.push('/products')">去逛逛</el-button>
      </el-empty>
    </div>
    
    <template v-else>
      <div class="cart-table">
        <div class="table-header">
          <el-checkbox v-model="selectAll" @change="handleSelectAll">全选</el-checkbox>
          <span class="col-info">商品信息</span>
          <span class="col-price">单价</span>
          <span class="col-quantity">数量</span>
          <span class="col-subtotal">小计</span>
          <span class="col-action">操作</span>
        </div>
        
        <div v-for="item in cartStore.items" :key="item.id" class="table-row">
          <el-checkbox v-model="selectedIds" :label="item.id" />
          <div class="col-info">
            <el-image :src="item.product_detail?.images?.[0]" fit="cover" class="product-image" />
            <div class="product-info">
              <h4>{{ item.product_detail?.name }}</h4>
              <p v-if="item.selected_specs">规格: {{ JSON.stringify(item.selected_specs) }}</p>
            </div>
          </div>
          <span class="col-price text-price">{{ formatPrice(item.product_detail?.price) }}</span>
          <div class="col-quantity">
            <el-input-number v-model="item.quantity" :min="1" :max="item.product_detail?.stock" size="small" @change="handleQuantityChange(item)" />
          </div>
          <span class="col-subtotal text-price">{{ formatPrice(item.subtotal) }}</span>
          <div class="col-action">
            <el-button type="danger" text @click="handleRemove(item.id)">删除</el-button>
          </div>
        </div>
      </div>
      
      <div class="cart-footer">
        <div class="footer-left">
          <el-button @click="handleBatchDelete">删除选中</el-button>
          <el-button @click="handleClearCart">清空购物车</el-button>
        </div>
        <div class="footer-right">
          <div class="summary">
            <p>已选 {{ selectedQuantity }} 件商品，总计 {{ selectedCount }} 件</p>
            <p class="total-amount">
              合计: <span class="text-price">{{ formatPrice(selectedAmount) }}</span>
            </p>
          </div>
          <el-button type="danger" size="large" :disabled="selectedCount === 0" @click="handleCheckout">
            结算 ({{ selectedCount }})
          </el-button>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useCartStore } from '@/stores/cart'

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

const selectedItems = computed(() => {
  return cartStore.items.filter(item => selectedIds.value.includes(item.id))
})

const selectedCount = computed(() => selectedItems.value.length)
const selectedQuantity = computed(() => selectedItems.value.reduce((sum, i) => sum + i.quantity, 0))
const selectedAmount = computed(() => selectedItems.value.reduce((sum, i) => sum + Number(i.subtotal), 0))

const loadCart = async () => {
  loading.value = true
  try {
    await cartStore.getCartList()
    selectedIds.value = []
  } catch (error) {
    console.error('Failed to load cart:', error)
  } finally {
    loading.value = false
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
    await ElMessageBox.confirm('确定要删除该商品吗？', '提示')
    await cartStore.removeItem(id)
    ElMessage.success('删除成功')
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
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 件商品吗？`, '提示')
    await cartStore.batchDelete(selectedIds.value)
    selectedIds.value = []
    ElMessage.success('删除成功')
  } catch {}
}

const handleClearCart = async () => {
  try {
    await ElMessageBox.confirm('确定要清空购物车吗？', '提示')
    await cartStore.clearCart()
    ElMessage.success('购物车已清空')
  } catch {}
}

const handleCheckout = () => {
  const ids = selectedIds.value.join(',')
  router.push({ name: 'Checkout', query: { ids } })
}

onMounted(loadCart)
</script>

<style scoped lang="scss">
.cart {
  padding-bottom: 40px;
}

.loading, .empty-cart {
  background: #fff;
  padding: 100px;
  border-radius: 8px;
}

.cart-table {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
}

.table-header {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  background: #f5f5f5;
  font-weight: bold;
}

.table-row {
  display: flex;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
  
  &:last-child { border-bottom: none; }
}

.col-info {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 15px;
}

.product-image {
  width: 80px;
  height: 80px;
  border-radius: 4px;
}

.product-info {
  h4 { margin: 0 0 5px; }
  p { margin: 0; color: #909399; font-size: 12px; }
}

.col-price { width: 100px; text-align: center; }
.col-quantity { width: 120px; text-align: center; }
.col-subtotal { width: 100px; text-align: center; font-weight: bold; }
.col-action { width: 80px; text-align: center; }

.cart-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
}

.footer-right {
  display: flex;
  align-items: center;
  gap: 30px;
}

.summary {
  text-align: right;
  
  .total-amount {
    font-size: 20px;
    margin-top: 10px;
  }
}
</style>

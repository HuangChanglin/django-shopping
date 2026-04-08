<template>
  <div class="orders container">
    <h2 class="page-header">我的订单</h2>
    
    <div class="toolbar">
      <el-tabs v-model="statusFilter" @tab-change="loadOrders">
        <el-tab-pane label="全部" name="" />
        <el-tab-pane label="待支付" name="pending" />
        <el-tab-pane label="已支付" name="paid" />
        <el-tab-pane label="已发货" name="shipped" />
        <el-tab-pane label="已完成" name="completed" />
        <el-tab-pane label="已取消" name="cancelled" />
      </el-tabs>
    </div>
    
    <div v-if="loading" class="loading">
      <el-icon class="is-loading"><Loading /></el-icon>
    </div>
    
    <div v-else-if="orders.length === 0" class="empty">
      <el-empty description="暂无订单">
        <el-button type="primary" @click="$router.push('/products')">去购物</el-button>
      </el-empty>
    </div>
    
    <div v-else class="order-list">
      <div v-for="order in orders" :key="order.id" class="order-card">
        <div class="order-header">
          <span class="order-no">订单号: {{ order.order_no }}</span>
          <span class="order-time">{{ formatDateTime(order.created_at) }}</span>
          <el-tag :type="getStatusType(order.status)">{{ getStatusText(order.status) }}</el-tag>
        </div>
        
        <div class="order-items">
          <div v-for="item in order.items" :key="item.id" class="order-item" @click="$router.push(`/orders/${order.id}`)">
            <el-image :src="item.product_image" fit="cover" class="item-image" />
            <div class="item-info">
              <h4>{{ item.product_name }}</h4>
              <p>{{ item.specs ? JSON.stringify(item.specs) : '' }}</p>
            </div>
            <div class="item-price">¥{{ item.price }} x {{ item.quantity }}</div>
          </div>
        </div>
        
        <div class="order-footer">
          <div class="order-amount">
            共 {{ order.items.length }} 件商品，实付款:
            <span class="text-price">{{ formatPrice(order.actual_amount) }}</span>
          </div>
          <div class="order-actions">
            <template v-if="order.status === 'pending'">
              <el-button type="primary" @click="handlePay(order)">支付</el-button>
              <el-button @click="handleCancel(order)">取消</el-button>
            </template>
            <template v-else-if="order.status === 'shipped'">
              <el-button type="primary" @click="handleConfirmReceive(order)">确认收货</el-button>
            </template>
            <template v-else-if="order.status === 'delivered'">
              <el-button type="success" @click="handleRefund(order)">申请退款</el-button>
            </template>
            <el-button @click="$router.push(`/orders/${order.id}`)">查看详情</el-button>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="total > 0" class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
        @current-change="loadOrders"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { orderApi } from '@/api'
import { formatPrice, formatDateTime } from '@/utils/format'

const orders = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const statusFilter = ref('')

const statusMap = {
  pending: { text: '待支付', type: 'warning' },
  paid: { text: '已支付', type: 'success' },
  shipped: { text: '已发货', type: 'primary' },
  delivered: { text: '已收货', type: 'success' },
  completed: { text: '已完成', type: 'success' },
  cancelled: { text: '已取消', type: 'info' },
  refunding: { text: '退款中', type: 'warning' },
  refunded: { text: '已退款', type: 'info' }
}

const getStatusText = (status) => statusMap[status]?.text || status
const getStatusType = (status) => statusMap[status]?.type || 'info'

const loadOrders = async () => {
  loading.value = true
  try {
    const params = { page: currentPage.value }
    if (statusFilter.value) params.status = statusFilter.value
    const res = await orderApi.getList(params)
    orders.value = res.results || res
    total.value = res.count || res.length
  } catch (error) {
    console.error('Failed to load orders:', error)
  } finally {
    loading.value = false
  }
}

const handlePay = async (order) => {
  try {
    await ElMessageBox.confirm('确认使用余额支付该订单吗？', '提示')
    await orderApi.pay(order.id, { payment_method: 'balance' })
    ElMessage.success('支付成功')
    loadOrders()
  } catch (error) {
    if (error !== 'cancel') ElMessage.error('支付失败')
  }
}

const handleCancel = async (order) => {
  try {
    await ElMessageBox.confirm('确定要取消该订单吗？', '提示')
    await orderApi.cancel(order.id)
    ElMessage.success('订单已取消')
    loadOrders()
  } catch (error) {
    if (error !== 'cancel') ElMessage.error('取消失败')
  }
}

const handleConfirmReceive = async (order) => {
  try {
    await ElMessageBox.confirm('确认已收到货物吗？', '提示')
    await orderApi.confirmReceive(order.id)
    ElMessage.success('已确认收货')
    loadOrders()
  } catch (error) {
    if (error !== 'cancel') ElMessage.error('操作失败')
  }
}

const handleRefund = async (order) => {
  try {
    await ElMessageBox.confirm('确定要申请退款吗？', '提示')
    await orderApi.refund(order.id)
    ElMessage.success('退款申请已提交')
    loadOrders()
  } catch (error) {
    if (error !== 'cancel') ElMessage.error('申请失败')
  }
}

onMounted(loadOrders)
</script>

<style scoped lang="scss">
.toolbar {
  background: #fff;
  padding: 0 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.loading, .empty {
  background: #fff;
  padding: 100px;
  border-radius: 8px;
}

.order-list {
  .order-card {
    background: #fff;
    border-radius: 8px;
    margin-bottom: 20px;
    overflow: hidden;
  }
}

.order-header {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 15px 20px;
  background: #f5f7fa;
  
  .order-no { font-weight: bold; }
  .order-time { color: #909399; }
}

.order-items {
  padding: 15px 20px;
}

.order-item {
  display: flex;
  align-items: center;
  padding: 10px 0;
  cursor: pointer;
  
  &:hover { background: #f5f7fa; }
}

.item-image {
  width: 60px;
  height: 60px;
  border-radius: 4px;
  margin-right: 15px;
}

.item-info {
  flex: 1;
  h4 { margin: 0 0 5px; font-size: 14px; }
  p { margin: 0; color: #909399; font-size: 12px; }
}

.item-price {
  color: #909399;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-top: 1px solid #eee;
}

.order-amount {
  font-size: 14px;
}

.order-actions {
  display: flex;
  gap: 10px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>

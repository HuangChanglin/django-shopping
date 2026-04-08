<template>
  <div class="order-detail container">
    <div v-if="loading" class="loading">
      <el-icon class="is-loading"><Loading /></el-icon>
    </div>
    
    <template v-else-if="order">
      <div class="order-status-card">
        <div class="status-icon">
          <el-icon v-if="order.status === 'completed'" :size="60" color="#67C23A"><CircleCheck /></el-icon>
          <el-icon v-else-if="order.status === 'cancelled'" :size="60" color="#909399"><CircleClose /></el-icon>
          <el-icon v-else :size="60" color="#409EFF"><Clock /></el-icon>
        </div>
        <div class="status-info">
          <h2>{{ getStatusText(order.status) }}</h2>
          <p v-if="order.status === 'shipped'">快递公司: {{ order.express_company }} 单号: {{ order.express_no }}</p>
        </div>
      </div>
      
      <div class="order-info-card">
        <h3>订单信息</h3>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">订单编号</span>
            <span class="value">{{ order.order_no }}</span>
          </div>
          <div class="info-item">
            <span class="label">下单时间</span>
            <span class="value">{{ formatDateTime(order.created_at) }}</span>
          </div>
          <div class="info-item">
            <span class="label">支付方式</span>
            <span class="value">{{ getPaymentText(order.payment_method) }}</span>
          </div>
          <div v-if="order.paid_at" class="info-item">
            <span class="label">支付时间</span>
            <span class="value">{{ formatDateTime(order.paid_at) }}</span>
          </div>
        </div>
        
        <h3>收货信息</h3>
        <div class="info-grid">
          <div class="info-item">
            <span class="label">收货人</span>
            <span class="value">{{ order.receiver_name }}</span>
          </div>
          <div class="info-item">
            <span class="label">联系电话</span>
            <span class="value">{{ order.receiver_phone }}</span>
          </div>
          <div class="info-item full">
            <span class="label">收货地址</span>
            <span class="value">{{ order.receiver_address }}</span>
          </div>
        </div>
      </div>
      
      <div class="order-goods-card">
        <h3>商品清单</h3>
        <div class="goods-list">
          <div v-for="item in order.items" :key="item.id" class="goods-item">
            <el-image :src="item.product_image" fit="cover" class="goods-image" />
            <div class="goods-info">
              <h4>{{ item.product_name }}</h4>
              <p>{{ item.specs ? JSON.stringify(item.specs) : '' }}</p>
            </div>
            <div class="goods-price">¥{{ item.price }}</div>
            <div class="goods-quantity">x {{ item.quantity }}</div>
            <div class="goods-subtotal text-price">¥{{ item.subtotal }}</div>
          </div>
        </div>
        
        <div class="order-amount">
          <div class="amount-row">
            <span>商品总额</span>
            <span>{{ formatPrice(order.total_amount) }}</span>
          </div>
          <div class="amount-row">
            <span>运费</span>
            <span>{{ formatPrice(order.freight_amount) }}</span>
          </div>
          <div v-if="order.discount_amount > 0" class="amount-row discount">
            <span>优惠</span>
            <span>- {{ formatPrice(order.discount_amount) }}</span>
          </div>
          <el-divider />
          <div class="amount-row total">
            <span>实付款</span>
            <span class="text-price">{{ formatPrice(order.actual_amount) }}</span>
          </div>
        </div>
      </div>
      
      <div class="order-actions">
        <el-button @click="$router.push('/orders')">返回订单列表</el-button>
        <template v-if="order.status === 'pending'">
          <el-button type="primary" @click="handlePay">支付</el-button>
          <el-button @click="handleCancel">取消订单</el-button>
        </template>
        <template v-else-if="order.status === 'shipped'">
          <el-button type="primary" @click="handleConfirmReceive">确认收货</el-button>
        </template>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { orderApi } from '@/api'
import { formatPrice, formatDateTime } from '@/utils/format'

const route = useRoute()
const order = ref(null)
const loading = ref(false)

const statusMap = {
  pending: '待支付', paid: '已支付', shipped: '已发货',
  delivered: '已收货', completed: '已完成', cancelled: '已取消',
  refunding: '退款中', refunded: '已退款'
}

const paymentMap = { balance: '余额支付', alipay: '支付宝', wechat: '微信支付' }

const getStatusText = (status) => statusMap[status] || status
const getPaymentText = (method) => paymentMap[method] || method

const loadOrder = async () => {
  loading.value = true
  try {
    order.value = await orderApi.getDetail(route.params.id)
  } catch (error) {
    console.error('Failed to load order:', error)
  } finally {
    loading.value = false
  }
}

const handlePay = async () => {
  try {
    await ElMessageBox.confirm('确认使用余额支付吗？', '提示')
    await orderApi.pay(order.value.id, { payment_method: 'balance' })
    ElMessage.success('支付成功')
    loadOrder()
  } catch (error) {
    if (error !== 'cancel') ElMessage.error('支付失败')
  }
}

const handleCancel = async () => {
  try {
    await ElMessageBox.confirm('确定要取消订单吗？', '提示')
    await orderApi.cancel(order.value.id)
    ElMessage.success('订单已取消')
    loadOrder()
  } catch (error) {
    if (error !== 'cancel') ElMessage.error('取消失败')
  }
}

const handleConfirmReceive = async () => {
  try {
    await ElMessageBox.confirm('确认已收到货物吗？', '提示')
    await orderApi.confirmReceive(order.value.id)
    ElMessage.success('已确认收货')
    loadOrder()
  } catch (error) {
    if (error !== 'cancel') ElMessage.error('操作失败')
  }
}

onMounted(loadOrder)
</script>

<style scoped lang="scss">
.order-status-card {
  display: flex;
  align-items: center;
  gap: 20px;
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 20px;
  
  h2 { margin: 0 0 10px; }
  p { margin: 0; color: #909399; }
}

.order-info-card, .order-goods-card {
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 20px;
  
  h3 {
    margin: 0 0 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;
  }
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-bottom: 30px;
}

.info-item {
  &.full { grid-column: 1 / -1; }
  
  .label { display: block; color: #909399; margin-bottom: 5px; }
  .value { font-weight: bold; }
}

.goods-list {
  .goods-item {
    display: flex;
    align-items: center;
    padding: 15px 0;
    border-bottom: 1px solid #eee;
    
    &:last-child { border-bottom: none; }
  }
}

.goods-image {
  width: 80px;
  height: 80px;
  border-radius: 4px;
  margin-right: 15px;
}

.goods-info {
  flex: 1;
  h4 { margin: 0 0 5px; }
  p { margin: 0; color: #909399; font-size: 12px; }
}

.goods-price { width: 80px; }
.goods-quantity { width: 60px; color: #909399; }
.goods-subtotal { width: 80px; font-weight: bold; }

.order-amount {
  margin-top: 20px;
  padding-top: 20px;
  text-align: right;
  
  .amount-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
    
    &.discount { color: #67C23A; }
    &.total { font-size: 18px; font-weight: bold; }
  }
}

.order-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
}

.loading {
  text-align: center;
  padding: 100px;
}
</style>

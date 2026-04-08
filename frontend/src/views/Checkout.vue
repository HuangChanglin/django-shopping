<template>
  <div class="checkout container">
    <h2 class="page-header">确认订单</h2>
    
    <div class="checkout-main">
      <div class="checkout-form">
        <h3>收货地址</h3>
        <div v-if="addresses.length > 0" class="address-list">
          <div
            v-for="addr in addresses"
            :key="addr.id"
            class="address-item"
            :class="{ active: selectedAddressId === addr.id }"
            @click="selectedAddressId = addr.id"
          >
            <div class="address-info">
              <p><strong>{{ addr.name }}</strong> {{ addr.phone }}</p>
              <p>{{ addr.full_address }}</p>
            </div>
            <el-tag v-if="addr.is_default" type="success" size="small">默认</el-tag>
          </div>
        </div>
        <div v-else class="no-address">
          <el-button type="primary" @click="showAddressDialog = true">添加收货地址</el-button>
        </div>
        
        <h3>支付方式</h3>
        <el-radio-group v-model="paymentMethod">
          <el-radio label="balance">余额支付</el-radio>
          <el-radio label="alipay">支付宝</el-radio>
          <el-radio label="wechat">微信支付</el-radio>
        </el-radio-group>
        
        <h3>商品清单</h3>
        <div class="goods-list">
          <div v-for="item in selectedItems" :key="item.id" class="goods-item">
            <el-image :src="item.product_detail?.images?.[0]" fit="cover" class="goods-image" />
            <div class="goods-info">
              <h4>{{ item.product_detail?.name }}</h4>
              <p>数量: {{ item.quantity }}</p>
            </div>
            <span class="goods-price text-price">{{ formatPrice(item.subtotal) }}</span>
          </div>
        </div>
        
        <div class="remark">
          <span>订单备注:</span>
          <el-input v-model="remark" placeholder="选填，可备注特殊需求" />
        </div>
      </div>
      
      <div class="order-summary">
        <h3>订单金额</h3>
        <div class="summary-item">
          <span>商品总额</span>
          <span>{{ formatPrice(totalAmount) }}</span>
        </div>
        <div class="summary-item">
          <span>运费</span>
          <span>{{ formatPrice(freightAmount) }}</span>
        </div>
        <div class="summary-item discount">
          <span>优惠</span>
          <span>- {{ formatPrice(0) }}</span>
        </div>
        <el-divider />
        <div class="summary-item total">
          <span>应付总额</span>
          <span class="text-price">{{ formatPrice(actualAmount) }}</span>
        </div>
        <div class="balance-info">
          <span>余额: {{ formatPrice(userStore.userInfo?.balance || 0) }}</span>
          <span v-if="paymentMethod === 'balance' && userStore.userInfo?.balance < actualAmount" class="balance-warning">
            余额不足
          </span>
        </div>
        <el-button type="danger" size="large" class="submit-btn" @click="handleSubmit" :loading="submitting">
          提交订单
        </el-button>
      </div>
    </div>
    
    <el-dialog v-model="showAddressDialog" title="添加收货地址" width="500px">
      <el-form :model="addressForm" :rules="addressRules" ref="addressFormRef" label-width="80px">
        <el-form-item label="收货人" prop="name">
          <el-input v-model="addressForm.name" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="addressForm.phone" />
        </el-form-item>
        <el-form-item label="省份" prop="province">
          <el-input v-model="addressForm.province" />
        </el-form-item>
        <el-form-item label="城市" prop="city">
          <el-input v-model="addressForm.city" />
        </el-form-item>
        <el-form-item label="区县" prop="district">
          <el-input v-model="addressForm.district" />
        </el-form-item>
        <el-form-item label="详细地址" prop="address">
          <el-input v-model="addressForm.address" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddressDialog = false">取消</el-button>
        <el-button type="primary" @click="handleAddAddress">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { cartApi, orderApi, addressApi } from '@/api'
import { useUserStore } from '@/stores/user'
import { formatPrice } from '@/utils/format'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const addresses = ref([])
const selectedItems = ref([])
const selectedAddressId = ref(null)
const paymentMethod = ref('balance')
const remark = ref('')
const submitting = ref(false)
const showAddressDialog = ref(false)

const addressForm = ref({
  name: '', phone: '', province: '', city: '', district: '', address: ''
})

const addressRules = {
  name: [{ required: true, message: '请输入收货人', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }],
  province: [{ required: true, message: '请输入省份', trigger: 'blur' }],
  city: [{ required: true, message: '请输入城市', trigger: 'blur' }],
  district: [{ required: true, message: '请输入区县', trigger: 'blur' }],
  address: [{ required: true, message: '请输入详细地址', trigger: 'blur' }]
}

const totalAmount = computed(() => selectedItems.value.reduce((sum, i) => sum + Number(i.subtotal), 0))
const freightAmount = computed(() => totalAmount.value < 99 ? 10 : 0)
const actualAmount = computed(() => totalAmount.value + freightAmount.value)

const loadData = async () => {
  try {
    await userStore.getUserInfo()
    const [addrRes, cartRes] = await Promise.all([
      addressApi.getList(),
      cartApi.getList()
    ])
    addresses.value = addrRes
    const defaultAddr = addrRes.find(a => a.is_default) || addrRes[0]
    if (defaultAddr) selectedAddressId.value = defaultAddr.id
    
    const ids = route.query.ids?.split(',').map(Number) || []
    selectedItems.value = ids.length > 0
      ? cartRes.filter(i => ids.includes(i.id))
      : cartRes
    
    if (selectedItems.value.length === 0) {
      ElMessage.warning('请选择要结算的商品')
      router.push('/cart')
    }
  } catch (error) {
    console.error('Failed to load data:', error)
  }
}

const handleAddAddress = async () => {
  try {
    const res = await addressApi.create(addressForm.value)
    addresses.value.push(res)
    selectedAddressId.value = res.id
    showAddressDialog.value = false
    ElMessage.success('添加成功')
  } catch (error) {
    ElMessage.error('添加失败')
  }
}

const handleSubmit = async () => {
  if (!selectedAddressId.value && !addressForm.value.name) {
    ElMessage.warning('请选择或添加收货地址')
    return
  }
  
  submitting.value = true
  try {
    const data = {
      payment_method: paymentMethod.value,
      remark: remark.value,
      cart_item_ids: selectedItems.value.map(i => i.id)
    }
    
    const addr = addresses.value.find(a => a.id === selectedAddressId.value)
    if (addr) {
      data.address_id = addr.id
    } else {
      Object.assign(data, {
        receiver_name: addressForm.value.name,
        receiver_phone: addressForm.value.phone,
        receiver_address: `${addressForm.value.province} ${addressForm.value.city} ${addressForm.value.district} ${addressForm.value.address}`
      })
    }
    
    const order = await orderApi.create(data)
    
    if (paymentMethod.value === 'balance' && userStore.userInfo?.balance >= actualAmount.value) {
      await orderApi.pay(order.id, { payment_method: 'balance' })
    }
    
    ElMessage.success('订单提交成功')
    router.push({ name: 'OrderDetail', params: { id: order.id } })
  } catch (error) {
    ElMessage.error('订单提交失败')
  } finally {
    submitting.value = false
  }
}

onMounted(loadData)
</script>

<style scoped lang="scss">
.checkout {
  padding-bottom: 40px;
}

.checkout-main {
  display: flex;
  gap: 20px;
}

.checkout-form {
  flex: 1;
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  
  h3 {
    margin: 0 0 15px;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;
  }
}

.address-list {
  margin-bottom: 30px;
}

.address-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border: 2px solid #eee;
  border-radius: 8px;
  margin-bottom: 10px;
  cursor: pointer;
  
  &.active {
    border-color: #409EFF;
    background: #f0f7ff;
  }
}

.address-info {
  p { margin: 5px 0; color: #606266; }
}

.goods-list {
  margin-bottom: 20px;
}

.goods-item {
  display: flex;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
  
  &:last-child { border-bottom: none; }
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
  p { margin: 0; color: #909399; }
}

.goods-price {
  font-size: 18px;
  font-weight: bold;
}

.remark {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-top: 20px;
  
  .el-input { flex: 1; }
}

.order-summary {
  width: 350px;
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  height: fit-content;
  
  h3 { margin: 0 0 20px; }
}

.summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  
  &.discount { color: #67C23A; }
  &.total { font-size: 18px; font-weight: bold; }
}

.balance-info {
  display: flex;
  justify-content: space-between;
  margin: 15px 0;
  font-size: 14px;
  color: #909399;
}

.balance-warning {
  color: #F56C6C;
}

.submit-btn {
  width: 100%;
  margin-top: 20px;
}

.no-address {
  margin-bottom: 30px;
}
</style>

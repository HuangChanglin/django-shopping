<template>
  <div class="user-center container">
    <div class="user-sidebar">
      <div class="user-info-card">
        <el-avatar :size="80" :src="userStore.userInfo?.avatar">
          {{ userStore.userInfo?.username?.[0]?.toUpperCase() }}
        </el-avatar>
        <h3>{{ userStore.userInfo?.username }}</h3>
        <p>{{ userStore.userInfo?.email }}</p>
      </div>
      <el-menu :default-active="activeMenu" @select="handleMenuSelect">
        <el-menu-item index="profile">个人信息</el-menu-item>
        <el-menu-item index="addresses">收货地址</el-menu-item>
        <el-menu-item index="password">修改密码</el-menu-item>
      </el-menu>
    </div>
    
    <div class="user-content">
      <template v-if="activeMenu === 'profile'">
        <div class="content-card">
          <h3>个人信息</h3>
          <el-form :model="profileForm" label-width="100px">
            <el-form-item label="用户名">
              <el-input v-model="profileForm.username" disabled />
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="profileForm.email" />
            </el-form-item>
            <el-form-item label="手机号">
              <el-input v-model="profileForm.phone" />
            </el-form-item>
            <el-form-item label="性别">
              <el-radio-group v-model="profileForm.gender">
                <el-radio label="male">男</el-radio>
                <el-radio label="female">女</el-radio>
                <el-radio label="unknown">未知</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="生日">
              <el-date-picker v-model="profileForm.birthday" type="date" placeholder="选择生日" />
            </el-form-item>
            <el-form-item label="收货地址">
              <el-input v-model="profileForm.address" type="textarea" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleUpdateProfile">保存</el-button>
            </el-form-item>
          </el-form>
        </div>
      </template>
      
      <template v-else-if="activeMenu === 'addresses'">
        <div class="content-card">
          <div class="card-header">
            <h3>收货地址</h3>
            <el-button type="primary" @click="showAddressDialog = true">添加地址</el-button>
          </div>
          <div v-if="addresses.length === 0" class="empty">
            <el-empty description="暂无收货地址" />
          </div>
          <div v-else class="address-list">
            <div v-for="addr in addresses" :key="addr.id" class="address-item">
              <div class="address-content">
                <p><strong>{{ addr.name }}</strong> {{ addr.phone }}</p>
                <p>{{ addr.full_address }}</p>
              </div>
              <div class="address-actions">
                <el-tag v-if="addr.is_default" type="success">默认</el-tag>
                <el-button type="primary" text @click="handleSetDefault(addr)">设为默认</el-button>
                <el-button type="danger" text @click="handleDeleteAddress(addr)">删除</el-button>
              </div>
            </div>
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
      </template>
      
      <template v-else-if="activeMenu === 'password'">
        <div class="content-card">
          <h3>修改密码</h3>
          <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="120px">
            <el-form-item label="原密码" prop="old_password">
              <el-input v-model="passwordForm.old_password" type="password" show-password />
            </el-form-item>
            <el-form-item label="新密码" prop="new_password">
              <el-input v-model="passwordForm.new_password" type="password" show-password />
            </el-form-item>
            <el-form-item label="确认新密码" prop="new_password_confirm">
              <el-input v-model="passwordForm.new_password_confirm" type="password" show-password />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleChangePassword">修改</el-button>
            </el-form-item>
          </el-form>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { authApi, addressApi } from '@/api'

const userStore = useUserStore()
const activeMenu = ref('profile')
const addresses = ref([])
const showAddressDialog = ref(false)

const profileForm = reactive({
  username: '', email: '', phone: '', gender: 'unknown', birthday: '', address: ''
})

const addressForm = reactive({
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

const passwordForm = reactive({
  old_password: '', new_password: '', new_password_confirm: ''
})

const passwordRules = {
  old_password: [{ required: true, message: '请输入原密码', trigger: 'blur' }],
  new_password: [{ required: true, message: '请输入新密码', trigger: 'blur' }, { min: 6, message: '密码至少6位', trigger: 'blur' }],
  new_password_confirm: [{ required: true, message: '请确认新密码', trigger: 'blur' }]
}

const handleMenuSelect = (index) => {
  activeMenu.value = index
  if (index === 'addresses') loadAddresses()
}

const loadUserInfo = () => {
  Object.assign(profileForm, {
    username: userStore.userInfo?.username,
    email: userStore.userInfo?.email,
    phone: userStore.userInfo?.phone,
    gender: userStore.userInfo?.gender || 'unknown',
    birthday: userStore.userInfo?.birthday,
    address: userStore.userInfo?.address
  })
}

const loadAddresses = async () => {
  try {
    addresses.value = await addressApi.getList()
  } catch (error) {
    console.error('Failed to load addresses:', error)
  }
}

const handleUpdateProfile = async () => {
  try {
    await userStore.updateUserInfo(profileForm)
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const handleAddAddress = async () => {
  try {
    const res = await addressApi.create(addressForm)
    addresses.value.push(res)
    showAddressDialog.value = false
    Object.keys(addressForm).forEach(k => addressForm[k] = '')
    ElMessage.success('添加成功')
  } catch (error) {
    ElMessage.error('添加失败')
  }
}

const handleSetDefault = async (addr) => {
  try {
    await addressApi.setDefault(addr.id)
    addresses.value.forEach(a => a.is_default = false)
    addr.is_default = true
    ElMessage.success('设置成功')
  } catch (error) {
    ElMessage.error('设置失败')
  }
}

const handleDeleteAddress = async (addr) => {
  try {
    await addressApi.delete(addr.id)
    addresses.value = addresses.value.filter(a => a.id !== addr.id)
    ElMessage.success('删除成功')
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

const handleChangePassword = async () => {
  if (passwordForm.new_password !== passwordForm.new_password_confirm) {
    ElMessage.error('两次密码不一致')
    return
  }
  try {
    await authApi.changePassword(passwordForm)
    ElMessage.success('密码修改成功')
    Object.keys(passwordForm).forEach(k => passwordForm[k] = '')
  } catch (error) {
    ElMessage.error('修改失败')
  }
}

onMounted(() => {
  if (userStore.userInfo) {
    loadUserInfo()
  }
})
</script>

<style scoped lang="scss">
.user-center {
  display: flex;
  gap: 20px;
  padding-bottom: 40px;
}

.user-sidebar {
  width: 250px;
}

.user-info-card {
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  text-align: center;
  margin-bottom: 20px;
  
  h3 { margin: 15px 0 5px; }
  p { margin: 0; color: #909399; }
}

.user-content {
  flex: 1;
}

.content-card {
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  
  h3 {
    margin: 0 0 20px;
    padding-bottom: 15px;
    border-bottom: 1px solid #eee;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  
  h3 { margin: 0; border: none; padding: 0; }
}

.address-list {
  .address-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    border: 1px solid #eee;
    border-radius: 8px;
    margin-bottom: 15px;
  }
}

.address-content {
  p { margin: 5px 0; }
}

.address-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.empty {
  padding: 50px;
}
</style>

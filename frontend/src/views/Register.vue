<template>
  <div class="register-page">
    <div class="register-background">
      <div class="shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
    </div>
    
    <div class="register-card">
      <div class="card-header">
        <h2>创建账号</h2>
        <p>加入我们，开启购物之旅</p>
      </div>
      
      <el-steps :active="currentStep" finish-status="success" class="register-steps">
        <el-step title="填写信息" />
        <el-step title="验证" />
        <el-step title="完成" />
      </el-steps>
      
      <transition name="fade-slide" mode="out-in">
        <el-form
          v-if="currentStep === 0"
          key="step1"
          ref="formRef"
          :model="form"
          :rules="rules"
          @submit.prevent="handleNext"
          class="register-form"
        >
          <el-form-item prop="username" class="form-item">
            <el-input
              v-model="form.username"
              placeholder="设置用户名（3-20位）"
              size="large"
              :prefix-icon="User"
              clearable
            >
              <template #prefix><User /></template>
            </el-input>
          </el-form-item>
          
          <el-form-item prop="email" class="form-item">
            <el-input
              v-model="form.email"
              placeholder="请输入邮箱"
              size="large"
              clearable
            >
              <template #prefix><Message /></template>
            </el-input>
          </el-form-item>
          
          <el-form-item prop="phone" class="form-item">
            <el-input
              v-model="form.phone"
              placeholder="手机号（选填）"
              size="large"
              clearable
            >
              <template #prefix><Phone /></template>
            </el-input>
          </el-form-item>
          
          <el-form-item prop="password" class="form-item">
            <el-input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="设置密码（至少6位）"
              size="large"
              clearable
            >
              <template #prefix><Lock /></template>
              <template #suffix>
                <el-icon @click="showPassword = !showPassword">
                  <component :is="showPassword ? 'View' : 'Hide'" />
                </el-icon>
              </template>
            </el-input>
          </el-form-item>
          
          <el-form-item prop="password_confirm" class="form-item">
            <el-input
              v-model="form.password_confirm"
              :type="showPassword ? 'text' : 'password'"
              placeholder="确认密码"
              size="large"
              @keyup.enter="handleNext"
              clearable
            >
              <template #prefix><Lock /></template>
            </el-input>
          </el-form-item>
          
          <el-button
            type="primary"
            size="large"
            class="submit-btn"
            @click="handleNext"
          >
            下一步
          </el-button>
        </el-form>
        
        <div v-else-if="currentStep === 1" key="step2" class="verify-step">
          <div class="verify-icon">
            <el-icon><Message /></el-icon>
          </div>
          <p>验证码已发送至您的邮箱</p>
          <p class="email-display">{{ form.email }}</p>
          
          <el-input
            v-model="verifyCode"
            placeholder="请输入验证码"
            size="large"
            maxlength="6"
            class="verify-input"
          />
          
          <div class="verify-actions">
            <el-button @click="currentStep = 0">返回</el-button>
            <el-button type="primary" :loading="loading" @click="handleRegister">
              立即注册
            </el-button>
          </div>
        </div>
        
        <div v-else key="step3" class="success-step">
          <div class="success-icon">
            <el-icon><CircleCheck /></el-icon>
          </div>
          <h3>注册成功！</h3>
          <p>欢迎加入网上商城</p>
          <el-button type="primary" size="large" @click="$router.push('/login')">
            立即登录
          </el-button>
        </div>
      </transition>
      
      <div class="links">
        已有账号？<router-link to="/login">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, shallowRef } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Message, Phone, View, Hide, CircleCheck } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const currentStep = ref(0)
const loading = ref(false)
const showPassword = ref(false)
const verifyCode = ref('')

const formRef = ref()
const form = reactive({
  username: '',
  email: '',
  phone: '',
  password: '',
  password_confirm: ''
})

const validatePasswordConfirm = (rule, value, callback) => {
  if (value !== form.password) {
    callback(new Error('两次密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度为3-20位', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' }
  ],
  password_confirm: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validatePasswordConfirm, trigger: 'blur' }
  ]
}

const handleNext = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  
  currentStep.value = 1
  ElMessage.success('验证码已发送')
}

const handleRegister = async () => {
  if (!verifyCode.value || verifyCode.value.length < 4) {
    ElMessage.warning('请输入正确的验证码')
    return
  }
  
  loading.value = true
  try {
    await userStore.register(form)
    currentStep.value = 2
  } catch (error) {
    ElMessage.error('注册失败')
    currentStep.value = 0
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.register-page {
  min-height: calc(100vh - 70px);
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  position: relative;
  overflow: hidden;
}

.register-background {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.shapes {
  position: absolute;
  inset: 0;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
}

.shape-1 {
  width: 400px;
  height: 400px;
  top: -100px;
  left: -100px;
  animation: float 20s ease-in-out infinite;
}

.shape-2 {
  width: 300px;
  height: 300px;
  bottom: -50px;
  right: -50px;
  animation: float 15s ease-in-out infinite reverse;
}

.shape-3 {
  width: 200px;
  height: 200px;
  top: 50%;
  left: 80%;
  animation: float 18s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  50% { transform: translate(30px, -30px) rotate(180deg); }
}

.register-card {
  width: 440px;
  background: #fff;
  padding: 45px;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  position: relative;
  z-index: 1;
}

.card-header {
  text-align: center;
  margin-bottom: 30px;
  
  h2 {
    margin: 0 0 10px;
    font-size: 26px;
    color: #333;
  }
  
  p {
    margin: 0;
    color: #909399;
  }
}

.register-steps {
  margin-bottom: 35px;
}

.register-form {
  .form-item {
    margin-bottom: 18px;
    
    :deep(.el-input__wrapper) {
      padding: 4px 15px;
      border-radius: 25px;
      transition: all 0.3s;
      
      &:hover, &.is-focus {
        box-shadow: 0 0 0 2px #11998e inset;
      }
    }
  }
}

.submit-btn {
  width: 100%;
  height: 48px;
  border-radius: 24px;
  font-size: 16px;
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  border: none;
  margin-top: 10px;
  transition: all 0.3s;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(17, 153, 142, 0.4);
  }
}

.verify-step {
  text-align: center;
  padding: 20px 0;
}

.verify-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  
  .el-icon {
    font-size: 40px;
    color: #fff;
  }
}

.email-display {
  color: #11998e;
  font-weight: 500;
  margin-bottom: 25px;
}

.verify-input {
  margin-bottom: 25px;
  
  :deep(.el-input__wrapper) {
    padding: 4px 20px;
    border-radius: 25px;
    font-size: 18px;
    letter-spacing: 8px;
    text-align: center;
  }
}

.verify-actions {
  display: flex;
  gap: 15px;
  
  .el-button {
    flex: 1;
    height: 44px;
    border-radius: 22px;
  }
}

.success-step {
  text-align: center;
  padding: 30px 0;
}

.success-icon {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 25px;
  animation: scaleIn 0.5s ease-out;
}

@keyframes scaleIn {
  from {
    transform: scale(0);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.success-icon .el-icon {
  font-size: 50px;
  color: #fff;
}

.success-step h3 {
  margin: 0 0 10px;
  font-size: 24px;
  color: #333;
}

.success-step p {
  color: #909399;
  margin-bottom: 30px;
}

.success-step .el-button {
  width: 100%;
  height: 48px;
  border-radius: 24px;
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  border: none;
}

.links {
  text-align: center;
  margin-top: 25px;
  color: #909399;
  
  a {
    color: #11998e;
    text-decoration: none;
    font-weight: 500;
    
    &:hover {
      text-decoration: underline;
    }
  }
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.4s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}
</style>

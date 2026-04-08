<template>
  <div class="login-page">
    <div class="login-background">
      <div class="particles">
        <div v-for="i in 20" :key="i" class="particle" :style="getParticleStyle(i)"></div>
      </div>
    </div>
    
    <div class="login-card">
      <div class="card-header">
        <h2>欢迎回来</h2>
        <p>登录您的账户继续购物</p>
      </div>
      
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        @submit.prevent="handleSubmit"
        class="login-form"
        :class="{ 'is-loading': loading }"
      >
        <el-form-item prop="username" class="form-item">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名/手机号/邮箱"
            size="large"
            :prefix-icon="User"
            clearable
          />
        </el-form-item>
        
        <el-form-item prop="password" class="form-item">
          <el-input
            v-model="form.password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="请输入密码"
            size="large"
            :prefix-icon="Lock"
            :suffix-icon="showPassword ? View : Hide"
            @click:suffix="showPassword = !showPassword"
            class="password-input"
            clearable
          />
        </el-form-item>
        
        <div class="form-options">
          <el-checkbox v-model="rememberMe">记住我</el-checkbox>
          <a href="#" class="forgot-link">忘记密码？</a>
        </div>
        
        <el-button
          type="primary"
          size="large"
          class="submit-btn"
          :loading="loading"
          @click="handleSubmit"
        >
          <span v-if="!loading">登 录</span>
        </el-button>
      </el-form>
      
      <div class="social-login">
        <span>其他登录方式</span>
        <div class="social-icons">
          <div class="social-icon" @click="handleSocialLogin('wechat')">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M8.691 2.188C3.891 2.188 0 5.476 0 9.53c0 2.212 1.17 4.203 3.002 5.55a.59.59 0 0 1 .213.665l-.39 1.48c-.019.07-.048.141-.048.213 0 .163.13.295.29.295a.326.326 0 0 0 .167-.054l1.903-1.114a.864.864 0 0 1 .717-.098 10.16 10.16 0 0 0 2.837.403c.276 0 .543-.027.811-.05-.857-2.578.157-4.972 1.932-6.446 1.703-1.415 3.882-1.98 5.853-1.838-.576-3.583-4.196-6.348-8.596-6.348zM5.785 5.991c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 0 1-1.162 1.178A1.17 1.17 0 0 1 4.623 7.17c0-.651.52-1.18 1.162-1.18zm5.813 0c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 0 1-1.162 1.178 1.17 1.17 0 0 1-1.162-1.178c0-.651.52-1.18 1.162-1.18zm5.34 2.867c-1.797-.052-3.746.512-5.28 1.786-1.72 1.428-2.687 3.72-1.78 6.22.942 2.453 3.666 4.229 6.884 4.229.826 0 1.622-.12 2.361-.336a.722.722 0 0 1 .598.082l1.584.926a.272.272 0 0 0 .14.045c.134 0 .24-.111.24-.247 0-.06-.023-.12-.038-.177l-.327-1.233a.582.582 0 0 1-.023-.156.49.49 0 0 1 .201-.398C23.024 18.48 24 16.82 24 14.98c0-3.21-2.931-5.837-6.656-6.088V8.89c-.135-.01-.269-.03-.406-.03zm-2.53 3.274c.535 0 .969.44.969.982a.976.976 0 0 1-.969.983.976.976 0 0 1-.969-.983c0-.542.434-.982.97-.982zm4.844 0c.535 0 .969.44.969.982a.976.976 0 0 1-.969.983.976.976 0 0 1-.969-.983c0-.542.434-.982.969-.982z"/>
            </svg>
          </div>
          <div class="social-icon" @click="handleSocialLogin('qq')">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M12.003 2c-2.265 0-6.52.587-6.52 5.594 0 1.932 1.183 4.914 5.164 7.62.528.38.916.994.916 1.657v2.766c0 .627.16 1.142.48 1.54.384.48.903.72 1.553.72.65 0 1.17-.24 1.553-.72.32-.398.48-.913.48-1.54V17.87c0-.663.388-1.277.916-1.657 3.98-2.705 5.164-5.687 5.164-7.62 0-5.007-4.242-5.594-6.502-5.594h-.704zm-.69 3.005c.828 0 1.5.72 1.5 1.608 0 .888-.672 1.604-1.5 1.604s-1.5-.716-1.5-1.604c0-.888.672-1.608 1.5-1.608zm6.31 0c.828 0 1.5.72 1.5 1.608 0 .888-.672 1.604-1.5 1.604s-1.5-.716-1.5-1.604c0-.888.672-1.608 1.5-1.608z"/>
            </svg>
          </div>
        </div>
      </div>
      
      <div class="links">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, shallowRef } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, View, Hide } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { useCartStore } from '@/stores/cart'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const cartStore = useCartStore()

const formRef = ref()
const loading = ref(false)
const showPassword = ref(false)
const rememberMe = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const getParticleStyle = (index) => {
  const size = Math.random() * 10 + 5
  const left = Math.random() * 100
  const delay = Math.random() * 5
  const duration = Math.random() * 10 + 10
  
  return {
    width: `${size}px`,
    height: `${size}px`,
    left: `${left}%`,
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`
  }
}

const handleSubmit = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  
  loading.value = true
  try {
    await userStore.login(form)
    await cartStore.getCartList()
    ElMessage.success({ message: '登录成功！', duration: 1500 })
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } catch (error) {
    ElMessage.error({ message: '用户名或密码错误', duration: 2000 })
  } finally {
    loading.value = false
  }
}

const handleSocialLogin = (type) => {
  ElMessage.info(`${type === 'wechat' ? '微信' : 'QQ'}登录开发中...`)
}
</script>

<style scoped lang="scss">
.login-page {
  min-height: calc(100vh - 70px);
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.login-background {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.particles {
  position: absolute;
  inset: 0;
}

.particle {
  position: absolute;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  animation: float 15s infinite ease-in-out;
}

@keyframes float {
  0%, 100% {
    transform: translateY(100vh) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100vh) rotate(720deg);
    opacity: 0;
  }
}

.login-card {
  width: 420px;
  background: #fff;
  padding: 45px;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  position: relative;
  z-index: 1;
  animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-header {
  text-align: center;
  margin-bottom: 35px;
  
  h2 {
    margin: 0 0 10px;
    font-size: 28px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  p {
    margin: 0;
    color: #909399;
  }
}

.login-form {
  .form-item {
    margin-bottom: 20px;
    
    :deep(.el-input__wrapper) {
      padding: 4px 15px;
      border-radius: 25px;
      box-shadow: 0 0 0 1px #dcdfe6 inset;
      transition: all 0.3s;
      
      &:hover, &.is-focus {
        box-shadow: 0 0 0 2px #667eea inset;
      }
    }
  }
}

.password-input {
  :deep(.el-input__suffix) {
    cursor: pointer;
  }
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.forgot-link {
  color: #667eea;
  text-decoration: none;
  font-size: 14px;
  
  &:hover {
    text-decoration: underline;
  }
}

.submit-btn {
  width: 100%;
  height: 50px;
  border-radius: 25px;
  font-size: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
  }
  
  &.is-loading {
    pointer-events: none;
  }
}

.social-login {
  margin-top: 30px;
  padding-top: 25px;
  border-top: 1px solid #eee;
  text-align: center;
  
  > span {
    display: block;
    color: #909399;
    margin-bottom: 15px;
    font-size: 14px;
  }
}

.social-icons {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.social-icon {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  
  svg {
    width: 24px;
    height: 24px;
  }
  
  &:first-child svg {
    color: #07c160;
  }
  
  &:last-child svg {
    color: #12b7f5;
  }
  
  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  }
}

.links {
  text-align: center;
  margin-top: 25px;
  color: #909399;
  
  a {
    color: #667eea;
    text-decoration: none;
    font-weight: 500;
    
    &:hover {
      text-decoration: underline;
    }
  }
}
</style>

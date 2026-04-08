<template>
  <div class="layout">
    <header class="header" :class="{ 'is-fixed': scrolled }">
      <div class="container header-content">
        <router-link to="/" class="logo">
          <el-icon class="logo-icon"><Shop /></el-icon>
          <span>网上商城</span>
        </router-link>
        
        <div class="search-box">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索商品..."
            @keyup.enter="handleSearch"
            class="search-input"
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
            <template #append>
              <el-button @click="handleSearch">搜索</el-button>
            </template>
          </el-input>
        </div>
        
        <nav class="nav">
          <router-link to="/products" class="nav-item">
            <el-icon><Goods /></el-icon>
            <span>全部商品</span>
          </router-link>
          
          <router-link to="/cart" class="nav-item cart-link">
            <el-badge :value="cartStore.totalCount" :hidden="cartStore.totalCount === 0" :max="99">
              <el-icon><ShoppingCart /></el-icon>
            </el-badge>
            <span>购物车</span>
          </router-link>
          
          <template v-if="userStore.isLoggedIn">
            <el-dropdown @command="handleUserCommand" trigger="click" class="user-dropdown">
              <div class="user-info">
                <el-avatar :size="36" :src="userStore.userInfo?.avatar" class="user-avatar">
                  {{ userStore.userInfo?.username?.[0]?.toUpperCase() }}
                </el-avatar>
                <span class="username">{{ userStore.userInfo?.username }}</span>
                <el-icon class="arrow"><ArrowDown /></el-icon>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="user">
                    <el-icon><User /></el-icon> 个人中心
                  </el-dropdown-item>
                  <el-dropdown-item command="orders">
                    <el-icon><List /></el-icon> 我的订单
                  </el-dropdown-item>
                  <el-dropdown-item divided command="logout">
                    <el-icon><SwitchButton /></el-icon> 退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <router-link to="/login" class="nav-item">
              <el-icon><User /></el-icon>
              <span>登录</span>
            </router-link>
            <router-link to="/register" class="nav-item register-btn">
              <el-icon><Plus /></el-icon>
              <span>注册</span>
            </router-link>
          </template>
        </nav>
      </div>
    </header>
    
    <main class="main" :class="{ 'has-header': scrolled }">
      <transition name="page" mode="out-in">
        <router-view :key="route.fullPath" />
      </transition>
    </main>
    
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-links">
            <div class="link-group">
              <h4>新手指南</h4>
              <a href="#">购物流程</a>
              <a href="#">会员制度</a>
              <a href="#">订单说明</a>
            </div>
            <div class="link-group">
              <h4>配送方式</h4>
              <a href="#">配送说明</a>
              <a href="#">签收须知</a>
              <a href="#">配送费用</a>
            </div>
            <div class="link-group">
              <h4>支付方式</h4>
              <a href="#">在线支付</a>
              <a href="#">余额支付</a>
              <a href="#">货到付款</a>
            </div>
            <div class="link-group">
              <h4>售后服务</h4>
              <a href="#">退换货政策</a>
              <a href="#">退款说明</a>
              <a href="#">联系客服</a>
            </div>
          </div>
          <div class="footer-info">
            <p>&copy; 2024 网上商城 - All Rights Reserved</p>
          </div>
        </div>
      </div>
    </footer>
    
    <ScrollToTop />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Shop, Search, Goods, ShoppingCart, User, List, 
  SwitchButton, Plus, ArrowDown
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { useCartStore } from '@/stores/cart'
import ScrollToTop from '@/components/ScrollToTop.vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const cartStore = useCartStore()

const searchKeyword = ref('')
const scrolled = ref(false)

const handleSearch = () => {
  router.push({ name: 'Products', query: { search: searchKeyword.value } })
}

const handleUserCommand = (command) => {
  switch (command) {
    case 'user':
      router.push({ name: 'User' })
      break
    case 'orders':
      router.push({ name: 'Orders' })
      break
    case 'logout':
      userStore.logout()
      ElMessage.success('已退出登录')
      router.push('/')
      break
  }
}

const handleScroll = () => {
  scrolled.value = window.scrollY > 70
}

if (userStore.isLoggedIn && !userStore.userInfo) {
  userStore.getUserInfo()
}

if (userStore.isLoggedIn) {
  cartStore.getSummary()
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped lang="scss">
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 100;
  transition: all 0.3s ease;
  
  &.is-fixed {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  }
}

.header-content {
  display: flex;
  align-items: center;
  height: 70px;
  gap: 40px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: #409EFF;
  transition: transform 0.2s;
  
  &:hover {
    transform: scale(1.05);
  }
  
  .logo-icon {
    font-size: 32px;
  }
  
  span {
    font-size: 22px;
    font-weight: bold;
  }
}

.search-box {
  flex: 1;
  max-width: 550px;
  
  .search-input {
    :deep(.el-input__wrapper) {
      border-radius: 20px 0 0 20px;
    }
  }
  
  :deep(.el-input-group__append) {
    border-radius: 0 20px 20px 0;
    background: #409EFF;
    color: #fff;
    border: none;
    
    .el-button {
      color: #fff;
    }
  }
}

.nav {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 18px;
  color: #606266;
  text-decoration: none;
  border-radius: 20px;
  transition: all 0.2s;
  
  &:hover {
    color: #409EFF;
    background: #f0f7ff;
  }
  
  &.router-link-active {
    color: #409EFF;
    background: #ecf5ff;
  }
}

.register-btn {
  background: linear-gradient(135deg, #409EFF, #66b1ff);
  color: #fff !important;
  
  &:hover {
    background: linear-gradient(135deg, #66b1ff, #79bbff);
    transform: translateY(-2px);
  }
}

.cart-link {
  position: relative;
  
  .el-badge {
    :deep(.el-badge__content) {
      background: #f56c6c;
    }
  }
}

.user-dropdown {
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 10px;
  border-radius: 20px;
  transition: background 0.2s;
  
  &:hover {
    background: #f5f7fa;
  }
}

.user-avatar {
  border: 2px solid #409EFF;
}

.username {
  color: #303133;
  font-weight: 500;
}

.arrow {
  font-size: 12px;
  color: #909399;
  transition: transform 0.2s;
  
  .user-dropdown:hover & {
    transform: rotate(180deg);
  }
}

.main {
  flex: 1;
  padding: 25px 0;
  
  &.has-header {
    padding-top: 25px;
  }
}

.footer {
  background: #2c3e50;
  color: #ecf0f1;
  padding: 50px 0 30px;
  margin-top: auto;
}

.footer-content {
  .footer-links {
    display: flex;
    justify-content: center;
    gap: 80px;
    margin-bottom: 40px;
    padding-bottom: 40px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
}

.link-group {
  h4 {
    margin: 0 0 15px;
    font-size: 16px;
    color: #fff;
  }
  
  a {
    display: block;
    color: #95a5a6;
    text-decoration: none;
    margin-bottom: 10px;
    transition: color 0.2s;
    
    &:hover {
      color: #409EFF;
    }
  }
}

.footer-info {
  text-align: center;
  color: #7f8c8d;
  font-size: 14px;
}

.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>

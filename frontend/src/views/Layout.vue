<template>
  <div class="layout">
    <header class="header">
      <div class="container header-content">
        <router-link to="/" class="logo">网上商城</router-link>
        <div class="search-box">
          <el-input v-model="searchKeyword" placeholder="搜索商品" @keyup.enter="handleSearch" />
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </div>
        <nav class="nav">
          <router-link to="/products">全部商品</router-link>
          <router-link to="/cart">
            <el-badge :value="cartStore.totalCount" :hidden="cartStore.totalCount === 0">
              <span>购物车</span>
            </el-badge>
          </router-link>
          <template v-if="userStore.isLoggedIn">
            <el-dropdown @command="handleUserCommand">
              <span class="user-info">
                <el-avatar :size="30" :src="userStore.userInfo?.avatar">
                  {{ userStore.userInfo?.username?.[0]?.toUpperCase() }}
                </el-avatar>
                <span>{{ userStore.userInfo?.username }}</span>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="user">个人中心</el-dropdown-item>
                  <el-dropdown-item command="orders">我的订单</el-dropdown-item>
                  <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <router-link to="/login">登录</router-link>
            <router-link to="/register">注册</router-link>
          </template>
        </nav>
      </div>
    </header>
    <main class="main">
      <router-view />
    </main>
    <footer class="footer">
      <div class="container">
        <p>&copy; 2024 网上商城 - All Rights Reserved</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useCartStore } from '@/stores/cart'

const router = useRouter()
const userStore = useUserStore()
const cartStore = useCartStore()

const searchKeyword = ref('')

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
      router.push('/')
      break
  }
}

if (userStore.isLoggedIn && !userStore.userInfo) {
  userStore.getUserInfo()
}

if (userStore.isLoggedIn) {
  cartStore.getSummary()
}
</script>

<style scoped lang="scss">
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: #fff;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  align-items: center;
  height: 70px;
  gap: 40px;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  text-decoration: none;
}

.search-box {
  flex: 1;
  max-width: 500px;
  display: flex;
  gap: 10px;
}

.nav {
  display: flex;
  align-items: center;
  gap: 25px;

  a {
    color: #606266;
    text-decoration: none;
    transition: color 0.2s;

    &:hover {
      color: #409EFF;
    }
  }
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.main {
  flex: 1;
  padding: 20px 0;
}

.footer {
  background: #f5f5f5;
  padding: 30px 0;
  text-align: center;
  color: #909399;
  margin-top: 40px;
}
</style>

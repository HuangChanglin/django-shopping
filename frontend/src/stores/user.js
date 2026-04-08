import { defineStore } from 'pinia'
import { authApi } from '@/api'
import { ElMessage } from 'element-plus'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    refreshToken: localStorage.getItem('refreshToken') || '',
    userInfo: null
  }),

  getters: {
    isLoggedIn: (state) => !!state.token
  },

  actions: {
    async login(credentials) {
      const res = await authApi.login(credentials)
      this.token = res.access
      this.refreshToken = res.refresh
      localStorage.setItem('token', this.token)
      localStorage.setItem('refreshToken', this.refreshToken)
      this.userInfo = res.user
      return res
    },

    async getUserInfo() {
      try {
        const res = await authApi.getUserInfo()
        this.userInfo = res
        return res
      } catch (error) {
        this.logout()
        throw error
      }
    },

    async updateUserInfo(data) {
      const res = await authApi.updateUserInfo(data)
      this.userInfo = { ...this.userInfo, ...res }
      return res
    },

    logout() {
      this.token = ''
      this.refreshToken = ''
      this.userInfo = null
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
    },

    async register(data) {
      const res = await authApi.register(data)
      ElMessage.success('注册成功，请登录')
      return res
    }
  }
})

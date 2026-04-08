import { defineStore } from 'pinia'
import { cartApi } from '@/api'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
    summary: {
      total_count: 0,
      total_quantity: 0,
      total_amount: 0
    }
  }),

  getters: {
    totalCount: (state) => state.summary.total_count,
    totalQuantity: (state) => state.summary.total_quantity,
    totalAmount: (state) => state.summary.total_amount
  },

  actions: {
    async getCartList() {
      const res = await cartApi.getList()
      this.items = res.results || res
      await this.getSummary()
      return this.items
    },

    async addToCart(productId, quantity = 1, selectedSpecs = {}) {
      await cartApi.add({
        product: productId,
        quantity,
        selected_specs: selectedSpecs
      })
      await this.getCartList()
    },

    async updateQuantity(id, quantity) {
      await cartApi.update(id, { quantity })
      await this.getCartList()
    },

    async removeItem(id) {
      await cartApi.delete(id)
      await this.getCartList()
    },

    async batchDelete(ids) {
      await cartApi.batchDelete(ids)
      await this.getCartList()
    },

    async clearCart() {
      await cartApi.clear()
      this.items = []
      this.summary = { total_count: 0, total_quantity: 0, total_amount: 0 }
    },

    async getSummary() {
      try {
        const res = await cartApi.getSummary()
        this.summary = res
      } catch (error) {
        console.error('Failed to get cart summary:', error)
      }
    }
  }
})

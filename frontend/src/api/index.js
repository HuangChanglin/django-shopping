import request from './request'

export const authApi = {
  register(data) {
    return request.post('/users/register/', data)
  },
  login(data) {
    return request.post('/users/login/', data)
  },
  refreshToken(refresh) {
    return request.post('/users/token/refresh/', { refresh })
  },
  getUserInfo() {
    return request.get('/users/me/')
  },
  updateUserInfo(data) {
    return request.patch('/users/', data)
  },
  changePassword(data) {
    return request.post('/users/change_password/', data)
  }
}

export const productApi = {
  getList(params) {
    return request.get('/products/', { params })
  },
  getDetail(id) {
    return request.get(`/products/${id}/`)
  },
  getHot() {
    return request.get('/products/hot/')
  },
  getRecommended() {
    return request.get('/products/recommended/')
  },
  getCategories() {
    return request.get('/products/categories/')
  },
  getReviews(id, params) {
    return request.get(`/products/${id}/reviews/`, { params })
  }
}

export const cartApi = {
  getList() {
    return request.get('/cart/')
  },
  add(data) {
    return request.post('/cart/', data)
  },
  update(id, data) {
    return request.patch(`/cart/${id}/`, data)
  },
  delete(id) {
    return request.delete(`/cart/${id}/`)
  },
  batchDelete(ids) {
    return request.post('/cart/batch_delete/', { ids })
  },
  clear() {
    return request.post('/cart/clear/')
  },
  getSummary() {
    return request.get('/cart/summary/')
  }
}

export const orderApi = {
  create(data) {
    return request.post('/orders/', data)
  },
  getList(params) {
    return request.get('/orders/', { params })
  },
  getDetail(id) {
    return request.get(`/orders/${id}/`)
  },
  cancel(id) {
    return request.post(`/orders/${id}/cancel/`)
  },
  pay(id, data) {
    return request.post(`/orders/${id}/pay/`, data)
  },
  confirmReceive(id) {
    return request.post(`/orders/${id}/confirm_receive/`)
  },
  refund(id) {
    return request.post(`/orders/${id}/refund/`)
  },
  getStatistics() {
    return request.get('/orders/statistics/')
  }
}

export const addressApi = {
  getList() {
    return request.get('/orders/addresses/')
  },
  create(data) {
    return request.post('/orders/addresses/', data)
  },
  update(id, data) {
    return request.patch(`/orders/addresses/${id}/`, data)
  },
  delete(id) {
    return request.delete(`/orders/addresses/${id}/`)
  },
  setDefault(id) {
    return request.post('/orders/addresses/set_default/', { address_id: id })
  }
}

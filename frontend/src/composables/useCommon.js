import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

export function usePagination(apiFunc, immediate = true) {
  const items = ref([])
  const loading = ref(false)
  const currentPage = ref(1)
  const pageSize = ref(20)
  const total = ref(0)
  const error = ref(null)

  const totalPages = computed(() => Math.ceil(total.value / pageSize.value))
  const hasMore = computed(() => currentPage.value < totalPages.value)

  const loadData = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const res = await apiFunc({ page: currentPage.value, page_size: pageSize.value, ...params })
      if (currentPage.value === 1) {
        items.value = res.results || res
      } else {
        items.value = [...items.value, ...(res.results || res)]
      }
      total.value = res.count || res.length || items.value.length
    } catch (e) {
      error.value = e
      ElMessage.error(e.message || '加载数据失败')
    } finally {
      loading.value = false
    }
  }

  const loadMore = () => {
    if (hasMore.value && !loading.value) {
      currentPage.value++
      loadData()
    }
  }

  const reset = () => {
    currentPage.value = 1
    items.value = []
    total.value = 0
  }

  const refresh = () => {
    reset()
    loadData()
  }

  if (immediate) {
    loadData()
  }

  return {
    items,
    loading,
    currentPage,
    pageSize,
    total,
    error,
    totalPages,
    hasMore,
    loadData,
    loadMore,
    reset,
    refresh
  }
}

export function useSearch(apiFunc, debounceMs = 300) {
  const keyword = ref('')
  const results = ref([])
  const loading = ref(false)
  let debounceTimer = null

  const search = async () => {
    if (!keyword.value.trim()) {
      results.value = []
      return
    }
    loading.value = true
    try {
      const res = await apiFunc({ search: keyword.value })
      results.value = res.results || res
    } catch (e) {
      ElMessage.error('搜索失败')
    } finally {
      loading.value = false
    }
  }

  const debouncedSearch = () => {
    clearTimeout(debounceTimer)
    debounceTimer = setTimeout(search, debounceMs)
  }

  watch(keyword, debouncedSearch)

  const clear = () => {
    keyword.value = ''
    results.value = []
  }

  return {
    keyword,
    results,
    loading,
    search,
    clear
  }
}

export function useSelection(initialSelected = []) {
  const selectedIds = ref([...initialSelected])

  const isSelected = (id) => selectedIds.value.includes(id)
  
  const toggleSelect = (id) => {
    const index = selectedIds.value.indexOf(id)
    if (index > -1) {
      selectedIds.value.splice(index, 1)
    } else {
      selectedIds.value.push(id)
    }
  }

  const selectAll = (ids) => {
    selectedIds.value = [...ids]
  }

  const clearSelection = () => {
    selectedIds.value = []
  }

  const selectMultiple = (ids) => {
    ids.forEach(id => {
      if (!selectedIds.value.includes(id)) {
        selectedIds.value.push(id)
      }
    })
  }

  return {
    selectedIds,
    isSelected,
    toggleSelect,
    selectAll,
    clearSelection,
    selectMultiple
  }
}

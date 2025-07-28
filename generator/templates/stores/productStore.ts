import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface Product {
  id: string | number
  name: string
  description: string
  price: number
  sale_price?: number
  image?: string
  images?: string[]
  category: string
  sku: string
  in_stock: boolean
  stock_quantity: number
  rating?: number
  review_count?: number
  tags?: string[]
  variants?: ProductVariant[]
  created_at: string
  updated_at: string
}

export interface ProductVariant {
  id: string | number
  name: string
  value: string
  price_modifier?: number
  stock_quantity: number
}

export interface ProductFilter {
  category?: string
  price_min?: number
  price_max?: number
  in_stock?: boolean
  tags?: string[]
  rating_min?: number
  search?: string
}

export interface ProductSort {
  field: 'name' | 'price' | 'rating' | 'created_at'
  direction: 'asc' | 'desc'
}

export const useProductStore = defineStore('product', () => {
  // State
  const products = ref<Product[]>([])
  const categories = ref<string[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const currentProduct = ref<Product | null>(null)
  
  // Filters and pagination
  const filters = ref<ProductFilter>({})
  const sort = ref<ProductSort>({ field: 'name', direction: 'asc' })
  const currentPage = ref(1)
  const pageSize = ref(12)
  
  // Getters
  const filteredProducts = computed(() => {
    let result = [...products.value]
    
    // Apply filters
    if (filters.value.category) {
      result = result.filter(p => p.category === filters.value.category)
    }
    
    if (filters.value.price_min !== undefined) {
      result = result.filter(p => (p.sale_price || p.price) >= filters.value.price_min!)
    }
    
    if (filters.value.price_max !== undefined) {
      result = result.filter(p => (p.sale_price || p.price) <= filters.value.price_max!)
    }
    
    if (filters.value.in_stock !== undefined) {
      result = result.filter(p => p.in_stock === filters.value.in_stock)
    }
    
    if (filters.value.rating_min !== undefined) {
      result = result.filter(p => (p.rating || 0) >= filters.value.rating_min!)
    }
    
    if (filters.value.search) {
      const searchTerm = filters.value.search.toLowerCase()
      result = result.filter(p => 
        p.name.toLowerCase().includes(searchTerm) ||
        p.description.toLowerCase().includes(searchTerm) ||
        p.tags?.some(tag => tag.toLowerCase().includes(searchTerm))
      )
    }
    
    if (filters.value.tags && filters.value.tags.length > 0) {
      result = result.filter(p => 
        p.tags?.some(tag => filters.value.tags!.includes(tag))
      )
    }
    
    // Apply sorting
    result.sort((a, b) => {
      const direction = sort.value.direction === 'asc' ? 1 : -1
      
      switch (sort.value.field) {
        case 'name':
          return a.name.localeCompare(b.name) * direction
        case 'price':
          const priceA = a.sale_price || a.price
          const priceB = b.sale_price || b.price
          return (priceA - priceB) * direction
        case 'rating':
          return ((a.rating || 0) - (b.rating || 0)) * direction
        case 'created_at':
          return (new Date(a.created_at).getTime() - new Date(b.created_at).getTime()) * direction
        default:
          return 0
      }
    })
    
    return result
  })
  
  const paginatedProducts = computed(() => {
    const start = (currentPage.value - 1) * pageSize.value
    const end = start + pageSize.value
    return filteredProducts.value.slice(start, end)
  })
  
  const totalPages = computed(() => {
    return Math.ceil(filteredProducts.value.length / pageSize.value)
  })
  
  const featuredProducts = computed(() => {
    return products.value
      .filter(p => p.tags?.includes('featured'))
      .slice(0, 8)
  })
  
  const onSaleProducts = computed(() => {
    return products.value
      .filter(p => p.sale_price && p.sale_price < p.price)
      .slice(0, 8)
  })
  
  const productsByCategory = computed(() => {
    const grouped: Record<string, Product[]> = {}
    products.value.forEach(product => {
      if (!grouped[product.category]) {
        grouped[product.category] = []
      }
      grouped[product.category].push(product)
    })
    return grouped
  })
  
  const priceRange = computed(() => {
    if (products.value.length === 0) return { min: 0, max: 100 }
    
    const prices = products.value.map(p => p.sale_price || p.price)
    return {
      min: Math.min(...prices),
      max: Math.max(...prices)
    }
  })
  
  // Actions
  const fetchProducts = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch('/api/products')
      if (!response.ok) throw new Error('Failed to fetch products')
      
      const data = await response.json()
      products.value = data
      
      // Extract unique categories
      const uniqueCategories = [...new Set(data.map((p: Product) => p.category))]
      categories.value = uniqueCategories.sort()
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error occurred'
    } finally {
      loading.value = false
    }
  }
  
  const fetchProduct = async (id: string | number) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch(`/api/products/${id}`)
      if (!response.ok) throw new Error('Product not found')
      
      const product = await response.json()
      currentProduct.value = product
      return product
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error occurred'
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const searchProducts = async (query: string) => {
    setFilter('search', query)
    currentPage.value = 1
  }
  
  const setFilter = (key: keyof ProductFilter, value: any) => {
    filters.value = { ...filters.value, [key]: value }
    currentPage.value = 1
  }
  
  const clearFilters = () => {
    filters.value = {}
    currentPage.value = 1
  }
  
  const setSort = (field: ProductSort['field'], direction: ProductSort['direction']) => {
    sort.value = { field, direction }
  }
  
  const setPage = (page: number) => {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page
    }
  }
  
  const setPageSize = (size: number) => {
    pageSize.value = size
    currentPage.value = 1
  }
  
  const getProductById = (id: string | number): Product | undefined => {
    return products.value.find(p => p.id === id)
  }
  
  const getProductsByCategory = (category: string): Product[] => {
    return products.value.filter(p => p.category === category)
  }
  
  const getRelatedProducts = (productId: string | number, limit = 4): Product[] => {
    const product = getProductById(productId)
    if (!product) return []
    
    return products.value
      .filter(p => p.id !== productId && p.category === product.category)
      .slice(0, limit)
  }
  
  const isProductInStock = (id: string | number): boolean => {
    const product = getProductById(id)
    return product ? product.in_stock && product.stock_quantity > 0 : false
  }
  
  const getProductPrice = (id: string | number): number => {
    const product = getProductById(id)
    if (!product) return 0
    return product.sale_price || product.price
  }
  
  const formatPrice = (price: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price)
  }
  
  // Admin actions (if needed)
  const createProduct = async (productData: Omit<Product, 'id' | 'created_at' | 'updated_at'>) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch('/api/products', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(productData)
      })
      
      if (!response.ok) throw new Error('Failed to create product')
      
      const newProduct = await response.json()
      products.value.push(newProduct)
      return newProduct
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error occurred'
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const updateProduct = async (id: string | number, updates: Partial<Product>) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch(`/api/products/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates)
      })
      
      if (!response.ok) throw new Error('Failed to update product')
      
      const updatedProduct = await response.json()
      const index = products.value.findIndex(p => p.id === id)
      if (index !== -1) {
        products.value[index] = updatedProduct
      }
      
      return updatedProduct
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error occurred'
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const deleteProduct = async (id: string | number) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch(`/api/products/${id}`, {
        method: 'DELETE'
      })
      
      if (!response.ok) throw new Error('Failed to delete product')
      
      products.value = products.value.filter(p => p.id !== id)
      
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error occurred'
      throw err
    } finally {
      loading.value = false
    }
  }
  
  return {
    // State
    products,
    categories,
    loading,
    error,
    currentProduct,
    filters,
    sort,
    currentPage,
    pageSize,
    
    // Getters
    filteredProducts,
    paginatedProducts,
    totalPages,
    featuredProducts,
    onSaleProducts,
    productsByCategory,
    priceRange,
    
    // Actions
    fetchProducts,
    fetchProduct,
    searchProducts,
    setFilter,
    clearFilters,
    setSort,
    setPage,
    setPageSize,
    getProductById,
    getProductsByCategory,
    getRelatedProducts,
    isProductInStock,
    getProductPrice,
    formatPrice,
    createProduct,
    updateProduct,
    deleteProduct
  }
}) 
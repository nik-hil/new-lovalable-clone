import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface CartItem {
  id: string | number
  productId: string | number
  name: string
  price: number
  sale_price?: number
  quantity: number
  image?: string
  variant?: string
  sku: string
  max_quantity?: number
  in_stock: boolean
}

export interface ShippingMethod {
  id: string
  name: string
  price: number
  estimatedDays: number
}

export interface Coupon {
  code: string
  type: 'percentage' | 'fixed'
  value: number
  minimum_order?: number
  expires_at?: string
}

export const useCartStore = defineStore('cart', () => {
  // State
  const items = ref<CartItem[]>([])
  const appliedCoupon = ref<Coupon | null>(null)
  const selectedShippingMethod = ref<ShippingMethod | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Available shipping methods
  const shippingMethods = ref<ShippingMethod[]>([
    { id: 'standard', name: 'Standard Shipping', price: 5.99, estimatedDays: 7 },
    { id: 'express', name: 'Express Shipping', price: 12.99, estimatedDays: 3 },
    { id: 'overnight', name: 'Overnight Shipping', price: 24.99, estimatedDays: 1 }
  ])

  // Getters
  const itemCount = computed(() => {
    return items.value.reduce((total, item) => total + item.quantity, 0)
  })

  const subtotal = computed(() => {
    return items.value.reduce((total, item) => {
      const price = item.sale_price || item.price
      return total + (price * item.quantity)
    }, 0)
  })

  const discountAmount = computed(() => {
    if (!appliedCoupon.value) return 0
    
    const coupon = appliedCoupon.value
    if (coupon.minimum_order && subtotal.value < coupon.minimum_order) return 0
    
    if (coupon.type === 'percentage') {
      return subtotal.value * (coupon.value / 100)
    } else {
      return Math.min(coupon.value, subtotal.value)
    }
  })

  const shippingCost = computed(() => {
    return selectedShippingMethod.value?.price || 0
  })

  const tax = computed(() => {
    // 8.5% tax rate (configurable)
    const taxRate = 0.085
    return (subtotal.value - discountAmount.value) * taxRate
  })

  const total = computed(() => {
    return subtotal.value - discountAmount.value + shippingCost.value + tax.value
  })

  const isEmpty = computed(() => items.value.length === 0)

  const isValidForCheckout = computed(() => {
    return !isEmpty.value && 
           items.value.every(item => item.in_stock) &&
           selectedShippingMethod.value !== null
  })

  // Actions
  const addItem = async (product: any, quantity = 1, variant?: string) => {
    const existingItemIndex = items.value.findIndex(
      item => item.productId === product.id && item.variant === variant
    )

    if (existingItemIndex !== -1) {
      // Update existing item quantity
      const existingItem = items.value[existingItemIndex]
      const newQuantity = existingItem.quantity + quantity
      const maxQty = existingItem.max_quantity || 999
      
      if (newQuantity <= maxQty) {
        existingItem.quantity = newQuantity
        await persistCart()
      } else {
        throw new Error(`Cannot add more than ${maxQty} of this item`)
      }
    } else {
      // Add new item
      const cartItem: CartItem = {
        id: `${product.id}-${variant || 'default'}-${Date.now()}`,
        productId: product.id,
        name: product.name,
        price: product.price,
        sale_price: product.sale_price,
        quantity,
        image: product.image,
        variant,
        sku: product.sku,
        max_quantity: product.max_quantity,
        in_stock: product.in_stock
      }

      items.value.push(cartItem)
      await persistCart()
    }
  }

  const updateQuantity = async (itemId: string | number, quantity: number) => {
    const item = items.value.find(i => i.id === itemId)
    if (!item) return

    if (quantity <= 0) {
      await removeItem(itemId)
      return
    }

    const maxQty = item.max_quantity || 999
    if (quantity > maxQty) {
      throw new Error(`Cannot add more than ${maxQty} of this item`)
    }

    item.quantity = quantity
    await persistCart()
  }

  const removeItem = async (itemId: string | number) => {
    const index = items.value.findIndex(i => i.id === itemId)
    if (index !== -1) {
      items.value.splice(index, 1)
      await persistCart()
    }
  }

  const clearCart = async () => {
    items.value = []
    appliedCoupon.value = null
    selectedShippingMethod.value = null
    await persistCart()
  }

  const applyCoupon = async (couponCode: string) => {
    loading.value = true
    error.value = null

    try {
      const response = await fetch('/api/coupons/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: couponCode, subtotal: subtotal.value })
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.message || 'Invalid coupon code')
      }

      const coupon = await response.json()
      appliedCoupon.value = coupon
      await persistCart()

    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to apply coupon'
      throw err
    } finally {
      loading.value = false
    }
  }

  const removeCoupon = async () => {
    appliedCoupon.value = null
    await persistCart()
  }

  const setShippingMethod = async (methodId: string) => {
    const method = shippingMethods.value.find(m => m.id === methodId)
    if (method) {
      selectedShippingMethod.value = method
      await persistCart()
    }
  }

  const getItemById = (itemId: string | number): CartItem | undefined => {
    return items.value.find(item => item.id === itemId)
  }

  const getItemsByProduct = (productId: string | number): CartItem[] => {
    return items.value.filter(item => item.productId === productId)
  }

  const hasProduct = (productId: string | number, variant?: string): boolean => {
    return items.value.some(
      item => item.productId === productId && item.variant === variant
    )
  }

  const getProductQuantity = (productId: string | number, variant?: string): number => {
    const item = items.value.find(
      item => item.productId === productId && item.variant === variant
    )
    return item ? item.quantity : 0
  }

  // Persistence
  const persistCart = async () => {
    try {
      const cartData = {
        items: items.value,
        appliedCoupon: appliedCoupon.value,
        selectedShippingMethod: selectedShippingMethod.value
      }

      // Save to localStorage for offline persistence
      localStorage.setItem('cart', JSON.stringify(cartData))

      // Save to server if user is logged in
      const response = await fetch('/api/cart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(cartData)
      })

      if (!response.ok && response.status !== 401) {
        console.warn('Failed to sync cart with server')
      }
    } catch (err) {
      console.warn('Failed to persist cart:', err)
    }
  }

  const loadCart = async () => {
    loading.value = true

    try {
      // Try to load from server first
      const response = await fetch('/api/cart')
      
      if (response.ok) {
        const serverCart = await response.json()
        items.value = serverCart.items || []
        appliedCoupon.value = serverCart.appliedCoupon || null
        selectedShippingMethod.value = serverCart.selectedShippingMethod || null
      } else {
        // Fallback to localStorage
        const localCart = localStorage.getItem('cart')
        if (localCart) {
          const cartData = JSON.parse(localCart)
          items.value = cartData.items || []
          appliedCoupon.value = cartData.appliedCoupon || null
          selectedShippingMethod.value = cartData.selectedShippingMethod || null
        }
      }

      // Validate item availability
      await validateCartItems()

    } catch (err) {
      console.warn('Failed to load cart:', err)
      
      // Try localStorage as last resort
      try {
        const localCart = localStorage.getItem('cart')
        if (localCart) {
          const cartData = JSON.parse(localCart)
          items.value = cartData.items || []
        }
      } catch (localErr) {
        console.error('Failed to load cart from localStorage:', localErr)
      }
    } finally {
      loading.value = false
    }
  }

  const validateCartItems = async () => {
    if (items.value.length === 0) return

    try {
      const productIds = items.value.map(item => item.productId)
      const response = await fetch('/api/products/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ productIds })
      })

      if (response.ok) {
        const validationData = await response.json()
        
        // Update cart items with current product data
        items.value = items.value.filter(item => {
          const productData = validationData.products[item.productId]
          if (!productData) return false // Remove unavailable products
          
          // Update item with current product info
          item.name = productData.name
          item.price = productData.price
          item.sale_price = productData.sale_price
          item.in_stock = productData.in_stock
          item.max_quantity = productData.max_quantity
          
          return true
        })

        await persistCart()
      }
    } catch (err) {
      console.warn('Failed to validate cart items:', err)
    }
  }

  // Checkout
  const prepareCheckout = () => {
    return {
      items: items.value,
      subtotal: subtotal.value,
      discount: discountAmount.value,
      shipping: shippingCost.value,
      tax: tax.value,
      total: total.value,
      coupon: appliedCoupon.value,
      shippingMethod: selectedShippingMethod.value
    }
  }

  // Utility functions
  const formatPrice = (price: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price)
  }

  const exportCart = () => {
    return {
      items: items.value,
      appliedCoupon: appliedCoupon.value,
      selectedShippingMethod: selectedShippingMethod.value,
      totals: {
        subtotal: subtotal.value,
        discount: discountAmount.value,
        shipping: shippingCost.value,
        tax: tax.value,
        total: total.value
      }
    }
  }

  return {
    // State
    items,
    appliedCoupon,
    selectedShippingMethod,
    shippingMethods,
    loading,
    error,

    // Getters
    itemCount,
    subtotal,
    discountAmount,
    shippingCost,
    tax,
    total,
    isEmpty,
    isValidForCheckout,

    // Actions
    addItem,
    updateQuantity,
    removeItem,
    clearCart,
    applyCoupon,
    removeCoupon,
    setShippingMethod,
    getItemById,
    getItemsByProduct,
    hasProduct,
    getProductQuantity,
    loadCart,
    validateCartItems,
    prepareCheckout,
    formatPrice,
    exportCart
  }
}) 
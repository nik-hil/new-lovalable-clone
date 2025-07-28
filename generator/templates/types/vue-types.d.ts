// TypeScript declarations for Vue template components
// This file resolves import errors in template files during development

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

declare module 'vue' {
  export * from '@vue/runtime-core'
  export * from '@vue/runtime-dom'
  export * from '@vue/reactivity'
  export * from '@vue/shared'
}

declare module 'vue-router' {
  export interface RouteLocationNormalized {
    query: Record<string, string | string[]>
  }
  
  export interface Router {
    push(to: string | object): void
    replace(to: object): void
  }
  
  export function useRoute(): RouteLocationNormalized
  export function useRouter(): Router
}

declare module 'pinia' {
  export function defineStore<T>(id: string, setup: () => T): () => T
}

declare module '@heroicons/vue/24/outline' {
  import type { DefineComponent } from 'vue'
  
  export const MapPinIcon: DefineComponent
  export const PhoneIcon: DefineComponent
  export const EnvelopeIcon: DefineComponent
  export const ClockIcon: DefineComponent
  export const ShoppingCartIcon: DefineComponent
  export const UserIcon: DefineComponent
  export const MagnifyingGlassIcon: DefineComponent
  export const Bars3Icon: DefineComponent
  export const XMarkIcon: DefineComponent
  export const StarIcon: DefineComponent
  export const EyeIcon: DefineComponent
  export const MinusIcon: DefineComponent
  export const PlusIcon: DefineComponent
  export const TrashIcon: DefineComponent
}

// Store types for templates
declare interface Product {
  id: number
  name: string
  description: string
  price: number
  sale_price?: number
  image: string
  in_stock: boolean
  rating: number
  review_count: number
  category?: string
}

declare interface CartItem {
  id: string
  product: Product
  quantity: number
  variant?: string
  total: number
}

declare interface ProductStore {
  products: Product[]
  categories: string[]
  filteredProducts: Product[]
  paginatedProducts: Product[]
  currentPage: number
  totalPages: number
  priceRange: { min: number; max: number }
  fetchProducts(): Promise<void>
  searchProducts(query: string): void
  setFilter(key: string, value: any): void
  clearFilters(): void
  setSort(field: string, direction: 'asc' | 'desc'): void
  setPage(page: number): void
  formatPrice(price: number): string
}

declare interface CartStore {
  items: CartItem[]
  itemCount: number
  subtotal: number
  total: number
  addItem(product: Product, quantity?: number): Promise<void>
}

// Global functions for templates
declare function useProductStore(): ProductStore
declare function useCartStore(): CartStore 
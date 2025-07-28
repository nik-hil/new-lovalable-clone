<template>
  <div class="product-card group relative overflow-hidden rounded-xl bg-white shadow-md transition-all duration-300 hover:shadow-xl">
    <!-- Product Image -->
    <div class="aspect-square overflow-hidden">
      <img 
        :src="product.image || '/api/placeholder/300/300'"
        :alt="product.name"
        class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
        loading="lazy"
      />
      
      <!-- Quick Actions Overlay -->
      <div class="absolute inset-0 flex items-center justify-center bg-black/50 opacity-0 transition-opacity duration-300 group-hover:opacity-100">
        <div class="flex gap-2">
          <button 
            @click="addToCart"
            class="rounded-full bg-white p-2 text-gray-800 shadow-lg transition-transform hover:scale-110"
            :disabled="!product.in_stock"
          >
            <ShoppingCartIcon class="h-5 w-5" />
          </button>
          <button 
            @click="viewDetails"
            class="rounded-full bg-white p-2 text-gray-800 shadow-lg transition-transform hover:scale-110"
          >
            <EyeIcon class="h-5 w-5" />
          </button>
        </div>
      </div>
      
      <!-- Stock Badge -->
      <div v-if="!product.in_stock" class="absolute top-2 left-2">
        <span class="rounded-full bg-red-500 px-2 py-1 text-xs font-medium text-white">
          Out of Stock
        </span>
      </div>
      
      <!-- Sale Badge -->
      <div v-if="product.sale_price" class="absolute top-2 right-2">
        <span class="rounded-full bg-red-500 px-2 py-1 text-xs font-medium text-white">
          Sale
        </span>
      </div>
    </div>
    
    <!-- Product Info -->
    <div class="p-4">
      <!-- Category -->
      <p v-if="product.category" class="text-xs font-medium uppercase tracking-wide text-gray-500 mb-1">
        {{ product.category }}
      </p>
      
      <!-- Product Name -->
      <h3 class="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
        {{ product.name }}
      </h3>
      
      <!-- Product Description -->
      <p v-if="product.description" class="text-sm text-gray-600 mb-3 line-clamp-2">
        {{ product.description }}
      </p>
      
      <!-- Rating -->
      <div v-if="product.rating" class="flex items-center gap-1 mb-3">
        <div class="flex">
          <StarIcon 
            v-for="i in 5" 
            :key="i"
            class="h-4 w-4"
            :class="i <= product.rating ? 'text-yellow-400' : 'text-gray-300'"
          />
        </div>
        <span class="text-sm text-gray-600">({{ product.review_count || 0 }})</span>
      </div>
      
      <!-- Price -->
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span 
            v-if="product.sale_price"
            class="text-lg font-bold text-red-600"
          >
            {{ formatPrice(product.sale_price) }}
          </span>
          <span 
            :class="[
              'font-semibold',
              product.sale_price 
                ? 'text-sm text-gray-500 line-through' 
                : 'text-lg text-gray-900'
            ]"
          >
            {{ formatPrice(product.price) }}
          </span>
        </div>
        
        <!-- Add to Cart Button -->
        <button
          @click="addToCart"
          :disabled="!product.in_stock"
          class="rounded-lg bg-primary-500 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-primary-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          {{ product.in_stock ? 'Add to Cart' : 'Sold Out' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ShoppingCartIcon, EyeIcon, StarIcon } from '@heroicons/vue/24/outline'

interface Product {
  id: string | number
  name: string
  description?: string
  price: number
  sale_price?: number
  image?: string
  category?: string
  in_stock: boolean
  rating?: number
  review_count?: number
}

interface Props {
  product: Product
}

interface Emits {
  (e: 'add-to-cart', product: Product): void
  (e: 'view-details', product: Product): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const formatPrice = (price: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(price)
}

const addToCart = () => {
  if (props.product.in_stock) {
    emit('add-to-cart', props.product)
  }
}

const viewDetails = () => {
  emit('view-details', props.product)
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 
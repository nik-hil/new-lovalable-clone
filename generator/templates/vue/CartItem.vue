<template>
  <div class="cart-item bg-white rounded-lg shadow-sm border border-gray-200 p-4">
    <div class="flex items-center space-x-4">
      <!-- Product Image -->
      <div class="w-16 h-16 sm:w-20 sm:h-20 flex-shrink-0">
        <img
          :src="item.image || '/api/placeholder/80/80'"
          :alt="item.name"
          class="w-full h-full object-cover rounded-lg"
          loading="lazy"
        />
      </div>

      <!-- Product Details -->
      <div class="flex-1 min-w-0">
        <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between">
          <div class="flex-1 pr-4">
            <h3 class="text-sm font-medium text-gray-900 truncate">
              {{ item.name }}
            </h3>
            
            <p v-if="item.variant" class="text-xs text-gray-500 mt-1">
              {{ item.variant }}
            </p>
            
            <div class="flex items-center mt-2 space-x-2">
              <!-- Price -->
              <div class="flex items-center space-x-1">
                <span 
                  v-if="item.sale_price"
                  class="text-sm font-medium text-red-600"
                >
                  {{ formatPrice(item.sale_price) }}
                </span>
                <span 
                  :class="[
                    'text-sm font-medium',
                    item.sale_price 
                      ? 'text-gray-500 line-through text-xs' 
                      : 'text-gray-900'
                  ]"
                >
                  {{ formatPrice(item.price) }}
                </span>
              </div>

              <!-- Stock Status -->
              <span 
                v-if="!item.in_stock"
                class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800"
              >
                Out of Stock
              </span>
              <span 
                v-else-if="item.low_stock"
                class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800"
              >
                Low Stock
              </span>
            </div>
          </div>

          <!-- Quantity Controls -->
          <div class="flex items-center mt-3 sm:mt-0">
            <div class="flex items-center border border-gray-300 rounded-lg">
              <button
                @click="decrementQuantity"
                :disabled="item.quantity <= 1 || updating"
                class="p-1 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                aria-label="Decrease quantity"
              >
                <MinusIcon class="h-4 w-4 text-gray-600" />
              </button>
              
              <input
                :value="item.quantity"
                @input="updateQuantity"
                @blur="validateQuantity"
                type="number"
                min="1"
                :max="item.max_quantity || 999"
                class="w-12 text-center border-0 text-sm font-medium text-gray-900 focus:ring-0 focus:outline-none"
                :disabled="updating"
              />
              
              <button
                @click="incrementQuantity"
                :disabled="item.quantity >= (item.max_quantity || 999) || updating"
                class="p-1 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                aria-label="Increase quantity"
              >
                <PlusIcon class="h-4 w-4 text-gray-600" />
              </button>
            </div>
          </div>
        </div>

        <!-- Item Total and Actions -->
        <div class="flex items-center justify-between mt-4">
          <div class="text-sm font-medium text-gray-900">
            Total: {{ formatPrice(itemTotal) }}
          </div>
          
          <div class="flex items-center space-x-2">
            <!-- Save for Later Button -->
            <button
              v-if="showSaveForLater"
              @click="saveForLater"
              :disabled="updating"
              class="text-xs text-primary-600 hover:text-primary-500 disabled:opacity-50 transition-colors"
            >
              Save for Later
            </button>
            
            <!-- Remove Button -->
            <button
              @click="removeItem"
              :disabled="updating"
              class="text-xs text-red-600 hover:text-red-500 disabled:opacity-50 transition-colors flex items-center space-x-1"
            >
              <TrashIcon class="h-3 w-3" />
              <span>Remove</span>
            </button>
          </div>
        </div>

        <!-- Loading Overlay -->
        <div v-if="updating" class="absolute inset-0 bg-white bg-opacity-50 flex items-center justify-center rounded-lg">
          <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-500"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  MinusIcon,
  PlusIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'

interface CartItem {
  id: string | number
  name: string
  price: number
  sale_price?: number
  quantity: number
  image?: string
  variant?: string
  in_stock: boolean
  low_stock?: boolean
  max_quantity?: number
}

interface Props {
  item: CartItem
  showSaveForLater?: boolean
  updating?: boolean
}

interface Emits {
  (e: 'update-quantity', itemId: string | number, quantity: number): void
  (e: 'remove-item', itemId: string | number): void
  (e: 'save-for-later', itemId: string | number): void
}

const props = withDefaults(defineProps<Props>(), {
  showSaveForLater: true,
  updating: false
})

const emit = defineEmits<Emits>()

// State
const localQuantity = ref(props.item.quantity)

// Computed
const itemTotal = computed(() => {
  const price = props.item.sale_price || props.item.price
  return price * props.item.quantity
})

// Methods
const formatPrice = (price: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(price)
}

const decrementQuantity = () => {
  if (props.item.quantity > 1) {
    emit('update-quantity', props.item.id, props.item.quantity - 1)
  }
}

const incrementQuantity = () => {
  const maxQty = props.item.max_quantity || 999
  if (props.item.quantity < maxQty) {
    emit('update-quantity', props.item.id, props.item.quantity + 1)
  }
}

const updateQuantity = (event: Event) => {
  const target = event.target as HTMLInputElement
  const newQuantity = parseInt(target.value) || 1
  localQuantity.value = newQuantity
}

const validateQuantity = () => {
  const minQty = 1
  const maxQty = props.item.max_quantity || 999
  
  if (localQuantity.value < minQty) {
    localQuantity.value = minQty
  } else if (localQuantity.value > maxQty) {
    localQuantity.value = maxQty
  }
  
  if (localQuantity.value !== props.item.quantity) {
    emit('update-quantity', props.item.id, localQuantity.value)
  }
}

const removeItem = () => {
  if (confirm('Are you sure you want to remove this item from your cart?')) {
    emit('remove-item', props.item.id)
  }
}

const saveForLater = () => {
  emit('save-for-later', props.item.id)
}
</script>

<style scoped>
.cart-item {
  position: relative;
}

/* Custom number input styling */
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type="number"] {
  -moz-appearance: textfield;
}
</style> 
<template>
  <div class="products-page">
    <!-- Page Header -->
    <div class="bg-gray-50 py-12">
      <div class="container mx-auto px-4">
        <div class="max-w-3xl">
          <h1 class="text-4xl font-bold text-gray-900 mb-4">
            {{ pageTitle }}
          </h1>
          <p class="text-lg text-gray-600">
            {{ pageDescription }}
          </p>
        </div>
      </div>
    </div>

    <div class="container mx-auto px-4 py-12">
      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Filters Sidebar -->
        <aside class="lg:w-64 space-y-6">
          <!-- Search -->
          <div class="bg-white p-6 rounded-lg shadow-sm border">
            <h3 class="font-semibold text-gray-900 mb-4">Search</h3>
            <Input
              v-model="searchQuery"
              type="search"
              placeholder="Search products..."
              @input="handleSearch"
              clearable
            />
          </div>

          <!-- Categories -->
          <div class="bg-white p-6 rounded-lg shadow-sm border">
            <h3 class="font-semibold text-gray-900 mb-4">Categories</h3>
            <div class="space-y-2">
              <label
                v-for="category in categories"
                :key="category"
                class="flex items-center cursor-pointer"
              >
                <input
                  :value="category"
                  :checked="selectedCategory === category"
                  @change="handleCategoryChange"
                  type="radio"
                  name="category"
                  class="text-primary-600 focus:ring-primary-500"
                />
                <span class="ml-2 text-gray-700">{{ category }}</span>
              </label>
              <label class="flex items-center cursor-pointer">
                <input
                  value=""
                  :checked="selectedCategory === ''"
                  @change="handleCategoryChange"
                  type="radio"
                  name="category"
                  class="text-primary-600 focus:ring-primary-500"
                />
                <span class="ml-2 text-gray-700">All Categories</span>
              </label>
            </div>
          </div>

          <!-- Price Range -->
          <div class="bg-white p-6 rounded-lg shadow-sm border">
            <h3 class="font-semibold text-gray-900 mb-4">Price Range</h3>
            <div class="space-y-4">
              <div class="flex items-center space-x-2">
                <Input
                  v-model.number="priceRange.min"
                  type="number"
                  placeholder="Min"
                  size="sm"
                  @blur="handlePriceChange"
                />
                <span class="text-gray-500">-</span>
                <Input
                  v-model.number="priceRange.max"
                  type="number"
                  placeholder="Max"
                  size="sm"
                  @blur="handlePriceChange"
                />
              </div>
              <div class="text-sm text-gray-500">
                Range: {{ formatPrice(productStore.priceRange.min) }} - {{ formatPrice(productStore.priceRange.max) }}
              </div>
            </div>
          </div>

          <!-- Availability -->
          <div class="bg-white p-6 rounded-lg shadow-sm border">
            <h3 class="font-semibold text-gray-900 mb-4">Availability</h3>
            <div class="space-y-2">
              <label class="flex items-center cursor-pointer">
                <input
                  v-model="inStockOnly"
                  type="checkbox"
                  class="text-primary-600 focus:ring-primary-500"
                  @change="handleAvailabilityChange"
                />
                <span class="ml-2 text-gray-700">In Stock Only</span>
              </label>
            </div>
          </div>

          <!-- Clear Filters -->
          <Button
            variant="outline"
            size="sm"
            full-width
            @click="clearAllFilters"
          >
            Clear All Filters
          </Button>
        </aside>

        <!-- Main Content -->
        <main class="flex-1">
          <!-- Results Header -->
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
            <div>
              <p class="text-gray-600">
                Showing {{ paginatedProducts.length }} of {{ filteredProducts.length }} products
                <span v-if="selectedCategory"> in "{{ selectedCategory }}"</span>
              </p>
            </div>
            
            <!-- Sort Options -->
            <div class="flex items-center space-x-4 mt-4 sm:mt-0">
              <label class="text-sm font-medium text-gray-700">Sort by:</label>
              <select
                v-model="sortOption"
                @change="handleSortChange"
                class="rounded-lg border-gray-300 text-sm focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="name-asc">Name (A-Z)</option>
                <option value="name-desc">Name (Z-A)</option>
                <option value="price-asc">Price (Low to High)</option>
                <option value="price-desc">Price (High to Low)</option>
                <option value="rating-desc">Rating (High to Low)</option>
                <option value="created_at-desc">Newest First</option>
              </select>
            </div>
          </div>

          <!-- Products Grid -->
          <div v-if="paginatedProducts.length > 0" class="space-y-8">
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              <ProductCard
                v-for="product in paginatedProducts"
                :key="product.id"
                :product="product"
                @add-to-cart="handleAddToCart"
                @view-details="handleViewProduct"
              />
            </div>

            <!-- Pagination -->
            <div v-if="totalPages > 1" class="flex justify-center">
              <nav class="flex items-center space-x-2">
                <Button
                  variant="outline"
                  size="sm"
                  :disabled="currentPage === 1"
                  @click="goToPage(currentPage - 1)"
                >
                  Previous
                </Button>
                
                <div class="flex items-center space-x-1">
                  <Button
                    v-for="page in visiblePages"
                    :key="page"
                    :variant="page === currentPage ? 'primary' : 'outline'"
                    size="sm"
                    @click="goToPage(page)"
                  >
                    {{ page }}
                  </Button>
                </div>
                
                <Button
                  variant="outline"
                  size="sm"
                  :disabled="currentPage === totalPages"
                  @click="goToPage(currentPage + 1)"
                >
                  Next
                </Button>
              </nav>
            </div>
          </div>

          <!-- No Results -->
          <div v-else class="text-center py-12">
            <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span class="text-4xl text-gray-400">🔍</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">
              No products found
            </h3>
            <p class="text-gray-600 mb-6">
              Try adjusting your filters or search terms
            </p>
            <Button
              variant="primary"
              @click="clearAllFilters"
            >
              Clear Filters
            </Button>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ProductCard from '../components/ProductCard.vue'
import Button from '../components/Button.vue'
import Input from '../components/Input.vue'
import { useProductStore } from '../stores/productStore'
import { useCartStore } from '../stores/cartStore'

interface Props {
  pageTitle?: string
  pageDescription?: string
}

const props = withDefaults(defineProps<Props>(), {
  pageTitle: 'Our Products',
  pageDescription: 'Discover our complete collection of high-quality products'
})

// Stores
const productStore = useProductStore()
const cartStore = useCartStore()

// Router
const route = useRoute()
const router = useRouter()

// State
const searchQuery = ref('')
const selectedCategory = ref('')
const priceRange = ref({ min: 0, max: 1000 })
const inStockOnly = ref(false)
const sortOption = ref('name-asc')

// Computed
const categories = computed(() => productStore.categories)
const filteredProducts = computed(() => productStore.filteredProducts)
const paginatedProducts = computed(() => productStore.paginatedProducts)
const currentPage = computed(() => productStore.currentPage)
const totalPages = computed(() => productStore.totalPages)

const visiblePages = computed(() => {
  const pages: number[] = []
  const current = currentPage.value
  const total = totalPages.value
  
  // Show up to 5 pages around current page
  const start = Math.max(1, current - 2)
  const end = Math.min(total, current + 2)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

// Methods
const handleSearch = (event: Event) => {
  const target = event.target as HTMLInputElement
  productStore.searchProducts(target.value)
  updateURL()
}

const handleCategoryChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  selectedCategory.value = target.value
  productStore.setFilter('category', target.value || undefined)
  updateURL()
}

const handlePriceChange = () => {
  if (priceRange.value.min >= 0) {
    productStore.setFilter('price_min', priceRange.value.min || undefined)
  }
  if (priceRange.value.max > 0) {
    productStore.setFilter('price_max', priceRange.value.max || undefined)
  }
  updateURL()
}

const handleAvailabilityChange = () => {
  productStore.setFilter('in_stock', inStockOnly.value || undefined)
  updateURL()
}

const handleSortChange = () => {
  const [field, direction] = sortOption.value.split('-')
  productStore.setSort(field as any, direction as 'asc' | 'desc')
  updateURL()
}

const clearAllFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = ''
  priceRange.value = { min: 0, max: 1000 }
  inStockOnly.value = false
  sortOption.value = 'name-asc'
  
  productStore.clearFilters()
  productStore.setSort('name', 'asc')
  
  updateURL()
}

const goToPage = (page: number) => {
  productStore.setPage(page)
  updateURL()
  
  // Scroll to top of products section
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const handleAddToCart = async (product: any) => {
  try {
    await cartStore.addItem(product)
    // Show success notification
  } catch (error) {
    console.error('Failed to add to cart:', error)
    // Show error notification
  }
}

const handleViewProduct = (product: any) => {
  router.push(`/products/${product.id}`)
}

const formatPrice = (price: number): string => {
  return productStore.formatPrice(price)
}

const updateURL = () => {
  // Update URL with current filters for bookmarking/sharing
  const query: any = {}
  
  if (searchQuery.value) query.search = searchQuery.value
  if (selectedCategory.value) query.category = selectedCategory.value
  if (priceRange.value.min > 0) query.price_min = priceRange.value.min
  if (priceRange.value.max < 1000) query.price_max = priceRange.value.max
  if (inStockOnly.value) query.in_stock = 'true'
  if (sortOption.value !== 'name-asc') query.sort = sortOption.value
  if (currentPage.value > 1) query.page = currentPage.value
  
  router.replace({ query })
}

const loadFiltersFromURL = () => {
  // Load filters from URL query parameters
  const query = route.query
  
  if (query.search) {
    searchQuery.value = query.search as string
    productStore.setFilter('search', query.search as string)
  }
  
  if (query.category) {
    selectedCategory.value = query.category as string
    productStore.setFilter('category', query.category as string)
  }
  
  if (query.price_min) {
    priceRange.value.min = parseInt(query.price_min as string)
    productStore.setFilter('price_min', priceRange.value.min)
  }
  
  if (query.price_max) {
    priceRange.value.max = parseInt(query.price_max as string)
    productStore.setFilter('price_max', priceRange.value.max)
  }
  
  if (query.in_stock === 'true') {
    inStockOnly.value = true
    productStore.setFilter('in_stock', true)
  }
  
  if (query.sort) {
    sortOption.value = query.sort as string
    const [field, direction] = sortOption.value.split('-')
    productStore.setSort(field as any, direction as 'asc' | 'desc')
  }
  
  if (query.page) {
    productStore.setPage(parseInt(query.page as string))
  }
}

// Lifecycle
onMounted(async () => {
  // Load products if not already loaded
  if (productStore.products.length === 0) {
    await productStore.fetchProducts()
  }
  
  // Load filters from URL
  loadFiltersFromURL()
})

// Watch for route changes (e.g., when navigating with browser back/forward)
watch(() => route.query, () => {
  loadFiltersFromURL()
}, { deep: true })
</script>

<style scoped>
/* Custom styles for better filter UI */
.products-page input[type="checkbox"],
.products-page input[type="radio"] {
  @apply rounded border-gray-300 text-primary-600 focus:ring-primary-500 focus:ring-offset-0;
}

.products-page select {
  @apply rounded-lg border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500;
}

/* Pagination styles */
.products-page nav button {
  @apply min-w-[2.5rem] h-10 flex items-center justify-center;
}
</style> 
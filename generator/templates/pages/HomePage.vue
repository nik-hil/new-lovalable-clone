<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section relative overflow-hidden bg-gradient-to-br from-primary-50 to-primary-100 py-20 lg:py-32">
      <div class="container mx-auto px-4 relative z-10">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div class="space-y-8">
            <div class="space-y-4">
              <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 leading-tight">
                {{ heroTitle }}
              </h1>
              <p class="text-xl text-gray-600 leading-relaxed">
                {{ heroSubtitle }}
              </p>
            </div>
            
            <div class="flex flex-col sm:flex-row gap-4">
              <Button
                variant="primary"
                size="lg"
                :to="ctaButtonLink"
                class="text-center"
              >
                {{ ctaButtonText }}
              </Button>
              <Button
                variant="outline"
                size="lg"
                :to="secondaryButtonLink"
                class="text-center"
              >
                {{ secondaryButtonText }}
              </Button>
            </div>
            
            <!-- Trust Indicators -->
            <div v-if="trustIndicators.length > 0" class="flex items-center space-x-8 pt-8">
              <span class="text-sm text-gray-500">Trusted by:</span>
              <div class="flex items-center space-x-6">
                <div
                  v-for="indicator in trustIndicators"
                  :key="indicator.name"
                  class="text-gray-400 text-sm font-medium"
                >
                  {{ indicator.name }}
                </div>
              </div>
            </div>
          </div>
          
          <div class="relative">
            <div class="aspect-square rounded-2xl overflow-hidden shadow-2xl">
              <img
                :src="heroImage"
                :alt="heroImageAlt"
                class="w-full h-full object-cover"
                loading="eager"
              />
            </div>
            <!-- Floating elements for visual interest -->
            <div class="absolute -top-4 -left-4 w-24 h-24 bg-primary-200 rounded-full opacity-20"></div>
            <div class="absolute -bottom-6 -right-6 w-32 h-32 bg-secondary-200 rounded-full opacity-20"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Products -->
    <section v-if="featuredProducts.length > 0" class="py-16 bg-white">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Featured Products
          </h2>
          <p class="text-lg text-gray-600 max-w-2xl mx-auto">
            Discover our most popular and highly-rated products
          </p>
        </div>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <ProductCard
            v-for="product in featuredProducts"
            :key="product.id"
            :product="product"
            @add-to-cart="handleAddToCart"
            @view-details="handleViewProduct"
          />
        </div>
        
        <div class="text-center mt-12">
          <Button
            variant="outline"
            size="lg"
            to="/products"
          >
            View All Products
          </Button>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-16 bg-gray-50">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Why Choose Us
          </h2>
          <p class="text-lg text-gray-600 max-w-2xl mx-auto">
            We're committed to providing the best products and service
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div
            v-for="feature in features"
            :key="feature.title"
            class="text-center space-y-4"
          >
            <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto">
              <span class="text-2xl">{{ feature.icon }}</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900">
              {{ feature.title }}
            </h3>
            <p class="text-gray-600">
              {{ feature.description }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Categories Section -->
    <section v-if="categories.length > 0" class="py-16 bg-white">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Shop by Category
          </h2>
          <p class="text-lg text-gray-600 max-w-2xl mx-auto">
            Find exactly what you're looking for
          </p>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          <router-link
            v-for="category in categories"
            :key="category.name"
            :to="`/products?category=${encodeURIComponent(category.name)}`"
            class="group relative overflow-hidden rounded-lg aspect-square hover:shadow-lg transition-all duration-300"
          >
            <img
              :src="category.image"
              :alt="category.name"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
            <div class="absolute inset-0 bg-black bg-opacity-40 group-hover:bg-opacity-50 transition-colors duration-300"></div>
            <div class="absolute inset-0 flex items-center justify-center">
              <h3 class="text-white text-lg font-semibold text-center px-4">
                {{ category.name }}
              </h3>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Newsletter Section -->
    <section class="py-16 bg-primary-600">
      <div class="container mx-auto px-4">
        <div class="max-w-2xl mx-auto text-center">
          <h2 class="text-3xl md:text-4xl font-bold text-white mb-4">
            Stay in the Loop
          </h2>
          <p class="text-primary-100 text-lg mb-8">
            Get the latest updates on new products, exclusive offers, and store news.
          </p>
          
          <form @submit.prevent="handleNewsletterSignup" class="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
            <Input
              v-model="newsletterEmail"
              type="email"
              placeholder="Enter your email"
              required
              class="flex-1"
              :class="{ 'bg-white': true }"
            />
            <Button
              type="submit"
              variant="secondary"
              size="lg"
              :loading="newsletterLoading"
              :disabled="!newsletterEmail.trim()"
            >
              {{ newsletterLoading ? 'Subscribing...' : 'Subscribe' }}
            </Button>
          </form>
          
          <p class="text-primary-200 text-sm mt-4">
            We respect your privacy. Unsubscribe at any time.
          </p>
        </div>
      </div>
    </section>

    <!-- Testimonials Section -->
    <section v-if="testimonials.length > 0" class="py-16 bg-gray-50">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            What Our Customers Say
          </h2>
          <p class="text-lg text-gray-600 max-w-2xl mx-auto">
            Real feedback from real customers
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div
            v-for="testimonial in testimonials"
            :key="testimonial.name"
            class="bg-white p-6 rounded-lg shadow-sm"
          >
            <div class="flex items-center mb-4">
              <div class="flex text-yellow-400">
                <span v-for="i in 5" :key="i" class="text-lg">
                  {{ i <= testimonial.rating ? '★' : '☆' }}
                </span>
              </div>
            </div>
            <blockquote class="text-gray-600 mb-4">
              "{{ testimonial.quote }}"
            </blockquote>
            <cite class="font-medium text-gray-900">
              {{ testimonial.name }}
            </cite>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import ProductCard from '../components/ProductCard.vue'
import Button from '../components/Button.vue'
import Input from '../components/Input.vue'
import { useProductStore } from '../stores/productStore'
import { useCartStore } from '../stores/cartStore'

interface Feature {
  icon: string
  title: string
  description: string
}

interface Category {
  name: string
  image: string
}

interface Testimonial {
  name: string
  quote: string
  rating: number
}

interface TrustIndicator {
  name: string
}

interface Props {
  heroTitle?: string
  heroSubtitle?: string
  heroImage?: string
  heroImageAlt?: string
  ctaButtonText?: string
  ctaButtonLink?: string
  secondaryButtonText?: string
  secondaryButtonLink?: string
  features?: Feature[]
  categories?: Category[]
  testimonials?: Testimonial[]
  trustIndicators?: TrustIndicator[]
}

const props = withDefaults(defineProps<Props>(), {
  heroTitle: 'Welcome to Our Store',
  heroSubtitle: 'Discover amazing products at unbeatable prices. Quality you can trust, service you can count on.',
  heroImage: '/api/placeholder/600/600',
  heroImageAlt: 'Store hero image',
  ctaButtonText: 'Shop Now',
  ctaButtonLink: '/products',
  secondaryButtonText: 'Learn More',
  secondaryButtonLink: '/about',
  features: () => [
    {
      icon: '🚚',
      title: 'Free Shipping',
      description: 'Free shipping on orders over $50. Fast and reliable delivery.'
    },
    {
      icon: '💎',
      title: 'Premium Quality',
      description: 'Only the finest products make it to our store. Quality guaranteed.'
    },
    {
      icon: '🔒',
      title: 'Secure Payment',
      description: 'Your payment information is always safe and secure with us.'
    },
    {
      icon: '📞',
      title: '24/7 Support',
      description: 'Our friendly support team is here to help you anytime.'
    },
    {
      icon: '↩️',
      title: 'Easy Returns',
      description: 'Not satisfied? Return your purchase within 30 days.'
    },
    {
      icon: '⭐',
      title: 'Trusted Brand',
      description: 'Join thousands of satisfied customers who trust our brand.'
    }
  ],
  categories: () => [],
  testimonials: () => [
    {
      name: 'Sarah Johnson',
      quote: 'Amazing quality and fast shipping! I\'ll definitely be shopping here again.',
      rating: 5
    },
    {
      name: 'Mike Chen',
      quote: 'Great customer service and exactly what I was looking for. Highly recommended.',
      rating: 5
    },
    {
      name: 'Emily Davis',
      quote: 'Love the variety of products and the website is so easy to use!',
      rating: 5
    }
  ],
  trustIndicators: () => []
})

// Stores
const productStore = useProductStore()
const cartStore = useCartStore()

// State
const newsletterEmail = ref('')
const newsletterLoading = ref(false)

// Computed
const featuredProducts = computed(() => productStore.featuredProducts)

// Methods
const handleAddToCart = async (product: any) => {
  try {
    await cartStore.addItem(product)
    // Show success notification (could emit event or use toast)
  } catch (error) {
    console.error('Failed to add to cart:', error)
    // Show error notification
  }
}

const handleViewProduct = (product: any) => {
  // Navigate to product detail page
  router.push(`/products/${product.id}`)
}

const handleNewsletterSignup = async () => {
  if (!newsletterEmail.value.trim()) return
  
  newsletterLoading.value = true
  
  try {
    const response = await fetch('/api/newsletter/subscribe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: newsletterEmail.value.trim() })
    })
    
    if (response.ok) {
      newsletterEmail.value = ''
      // Show success message
    } else {
      throw new Error('Subscription failed')
    }
  } catch (error) {
    console.error('Newsletter signup failed:', error)
    // Show error message
  } finally {
    newsletterLoading.value = false
  }
}

// Lifecycle
onMounted(async () => {
  // Load featured products
  if (productStore.products.length === 0) {
    await productStore.fetchProducts()
  }
})
</script>

<style scoped>
.hero-section {
  background-image: 
    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%);
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23000000' fill-opacity='0.02'%3E%3Ccircle cx='30' cy='30' r='4'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  pointer-events: none;
}
</style> 
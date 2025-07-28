<template>
  <footer class="bg-gray-900 text-white">
    <div class="container mx-auto px-4 py-12">
      <!-- Main Footer Content -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <!-- Store Info -->
        <div class="space-y-4">
          <div class="flex items-center space-x-2">
            <div class="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-lg">{{ logoText }}</span>
            </div>
            <span class="text-xl font-bold">{{ storeName }}</span>
          </div>
          <p class="text-gray-300 text-sm leading-relaxed">
            {{ storeDescription }}
          </p>
          <div v-if="socialLinks.length > 0" class="flex space-x-4">
            <a
              v-for="social in socialLinks"
              :key="social.platform"
              :href="social.url"
              class="text-gray-400 hover:text-primary-400 transition-colors"
              :aria-label="social.platform"
            >
              <component :is="social.icon" class="h-5 w-5" />
            </a>
          </div>
        </div>

        <!-- Quick Links -->
        <div class="space-y-4">
          <h3 class="text-lg font-semibold">Quick Links</h3>
          <ul class="space-y-2">
            <li v-for="link in quickLinks" :key="link.path">
              <router-link
                :to="link.path"
                class="text-gray-300 hover:text-white transition-colors text-sm"
              >
                {{ link.name }}
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Customer Service -->
        <div class="space-y-4">
          <h3 class="text-lg font-semibold">Customer Service</h3>
          <ul class="space-y-2">
            <li v-for="item in customerServiceLinks" :key="item.path">
              <router-link
                :to="item.path"
                class="text-gray-300 hover:text-white transition-colors text-sm"
              >
                {{ item.name }}
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Contact Info -->
        <div class="space-y-4">
          <h3 class="text-lg font-semibold">Contact Us</h3>
          <div class="space-y-3">
            <div v-if="contactInfo.address" class="flex items-start space-x-2">
              <MapPinIcon class="h-4 w-4 text-gray-400 mt-0.5 flex-shrink-0" />
              <span class="text-gray-300 text-sm">{{ contactInfo.address }}</span>
            </div>
            <div v-if="contactInfo.phone" class="flex items-center space-x-2">
              <PhoneIcon class="h-4 w-4 text-gray-400 flex-shrink-0" />
              <a 
                :href="`tel:${contactInfo.phone}`"
                class="text-gray-300 hover:text-white transition-colors text-sm"
              >
                {{ contactInfo.phone }}
              </a>
            </div>
            <div v-if="contactInfo.email" class="flex items-center space-x-2">
              <EnvelopeIcon class="h-4 w-4 text-gray-400 flex-shrink-0" />
              <a 
                :href="`mailto:${contactInfo.email}`"
                class="text-gray-300 hover:text-white transition-colors text-sm"
              >
                {{ contactInfo.email }}
              </a>
            </div>
            <div v-if="businessHours" class="flex items-start space-x-2">
              <ClockIcon class="h-4 w-4 text-gray-400 mt-0.5 flex-shrink-0" />
              <div class="text-gray-300 text-sm">
                <div v-for="hours in businessHours" :key="hours.days">
                  <span class="font-medium">{{ hours.days }}:</span> {{ hours.hours }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Newsletter Signup -->
      <div v-if="showNewsletter" class="mt-12 pt-8 border-t border-gray-700">
        <div class="max-w-md mx-auto text-center">
          <h3 class="text-lg font-semibold mb-2">Stay Updated</h3>
          <p class="text-gray-300 text-sm mb-4">
            Get the latest updates on new products and exclusive offers.
          </p>
          <form @submit.prevent="handleNewsletterSignup" class="flex space-x-2">
            <input
              v-model="newsletterEmail"
              type="email"
              placeholder="Enter your email"
              class="flex-1 px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              required
            />
            <button
              type="submit"
              :disabled="newsletterLoading"
              class="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors disabled:opacity-50"
            >
              {{ newsletterLoading ? 'Subscribing...' : 'Subscribe' }}
            </button>
          </form>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="mt-12 pt-8 border-t border-gray-700 flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
        <div class="text-gray-400 text-sm">
          © {{ currentYear }} {{ storeName }}. All rights reserved.
        </div>
        <div class="flex space-x-6">
          <router-link
            v-for="legal in legalLinks"
            :key="legal.path"
            :to="legal.path"
            class="text-gray-400 hover:text-white transition-colors text-sm"
          >
            {{ legal.name }}
          </router-link>
        </div>
        <div v-if="paymentMethods.length > 0" class="flex items-center space-x-2">
          <span class="text-gray-400 text-sm">We accept:</span>
          <div class="flex space-x-2">
            <div
              v-for="method in paymentMethods"
              :key="method"
              class="w-8 h-6 bg-gray-700 rounded flex items-center justify-center"
            >
              <span class="text-xs text-gray-300">{{ method.toUpperCase() }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  MapPinIcon,
  PhoneIcon,
  EnvelopeIcon,
  ClockIcon
} from '@heroicons/vue/24/outline'

interface NavigationLink {
  name: string
  path: string
}

interface SocialLink {
  platform: string
  url: string
  icon: string
}

interface ContactInfo {
  address?: string
  phone?: string
  email?: string
}

interface BusinessHours {
  days: string
  hours: string
}

interface Props {
  storeName?: string
  logoText?: string
  storeDescription?: string
  quickLinks?: NavigationLink[]
  customerServiceLinks?: NavigationLink[]
  legalLinks?: NavigationLink[]
  socialLinks?: SocialLink[]
  contactInfo?: ContactInfo
  businessHours?: BusinessHours[]
  showNewsletter?: boolean
  paymentMethods?: string[]
}

interface Emits {
  (e: 'newsletter-signup', email: string): void
}

const props = withDefaults(defineProps<Props>(), {
  storeName: 'Local Store',
  logoText: 'LS',
  storeDescription: 'Your trusted local store for quality products and exceptional service.',
  quickLinks: () => [
    { name: 'Home', path: '/' },
    { name: 'Products', path: '/products' },
    { name: 'About Us', path: '/about' },
    { name: 'Contact', path: '/contact' }
  ],
  customerServiceLinks: () => [
    { name: 'Help Center', path: '/help' },
    { name: 'Shipping Info', path: '/shipping' },
    { name: 'Returns', path: '/returns' },
    { name: 'Size Guide', path: '/size-guide' }
  ],
  legalLinks: () => [
    { name: 'Privacy Policy', path: '/privacy' },
    { name: 'Terms of Service', path: '/terms' },
    { name: 'Cookie Policy', path: '/cookies' }
  ],
  socialLinks: () => [],
  contactInfo: () => ({}),
  businessHours: () => [
    { days: 'Mon - Fri', hours: '9:00 AM - 6:00 PM' },
    { days: 'Saturday', hours: '10:00 AM - 4:00 PM' },
    { days: 'Sunday', hours: 'Closed' }
  ],
  showNewsletter: true,
  paymentMethods: () => ['visa', 'mc', 'amex', 'paypal']
})

const emit = defineEmits<Emits>()

// State
const newsletterEmail = ref('')
const newsletterLoading = ref(false)

// Computed
const currentYear = computed(() => new Date().getFullYear())

// Methods
const handleNewsletterSignup = async () => {
  if (!newsletterEmail.value.trim()) return
  
  newsletterLoading.value = true
  
  try {
    emit('newsletter-signup', newsletterEmail.value.trim())
    newsletterEmail.value = ''
    // Show success message (could be handled by parent component)
  } catch (error) {
    console.error('Newsletter signup failed:', error)
  } finally {
    newsletterLoading.value = false
  }
}
</script> 
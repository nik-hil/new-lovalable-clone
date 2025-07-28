<template>
  <header class="sticky top-0 z-50 bg-white shadow-sm border-b border-gray-200">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <div class="flex items-center">
          <router-link to="/" class="flex items-center space-x-2">
            <div class="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-lg">{{ logoText }}</span>
            </div>
            <span class="text-xl font-bold text-gray-900 hidden sm:block">
              {{ storeName }}
            </span>
          </router-link>
        </div>

        <!-- Desktop Navigation -->
        <nav class="hidden md:flex items-center space-x-8">
          <router-link
            v-for="item in navigationItems"
            :key="item.path"
            :to="item.path"
            class="text-gray-600 hover:text-primary-500 font-medium transition-colors"
            active-class="text-primary-500"
          >
            {{ item.name }}
          </router-link>
        </nav>

        <!-- Right Side Actions -->
        <div class="flex items-center space-x-4">
          <!-- Search -->
          <div v-if="showSearch" class="hidden sm:block relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search products..."
              class="w-64 pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              @keydown.enter="handleSearch"
            />
            <MagnifyingGlassIcon class="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
          </div>

          <!-- Cart Button -->
          <button
            v-if="showCart"
            @click="toggleCart"
            class="relative p-2 text-gray-600 hover:text-primary-500 transition-colors"
          >
            <ShoppingCartIcon class="h-6 w-6" />
            <span
              v-if="cartItemCount > 0"
              class="absolute -top-1 -right-1 bg-primary-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center"
            >
              {{ cartItemCount }}
            </span>
          </button>

          <!-- User Menu -->
          <div class="relative" ref="userMenuRef">
            <button
              @click="toggleUserMenu"
              class="flex items-center space-x-2 text-gray-600 hover:text-primary-500 transition-colors"
            >
              <UserIcon class="h-6 w-6" />
              <span class="hidden sm:block">Account</span>
            </button>

            <!-- User Dropdown -->
            <transition
              enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <div
                v-if="showUserMenu"
                class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1"
              >
                <a
                  v-for="item in userMenuItems"
                  :key="item.name"
                  :href="item.href"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  @click="item.action && item.action()"
                >
                  {{ item.name }}
                </a>
              </div>
            </transition>
          </div>

          <!-- Mobile Menu Button -->
          <button
            @click="toggleMobileMenu"
            class="md:hidden p-2 text-gray-600 hover:text-primary-500 transition-colors"
          >
            <Bars3Icon v-if="!showMobileMenu" class="h-6 w-6" />
            <XMarkIcon v-else class="h-6 w-6" />
          </button>
        </div>
      </div>

      <!-- Mobile Navigation -->
      <transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="transform opacity-100 scale-100"
        leave-to-class="transform opacity-0 scale-95"
      >
        <div v-if="showMobileMenu" class="md:hidden py-4 border-t border-gray-200">
          <!-- Mobile Search -->
          <div v-if="showSearch" class="px-4 mb-4">
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search products..."
                class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                @keydown.enter="handleSearch"
              />
              <MagnifyingGlassIcon class="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
            </div>
          </div>

          <!-- Mobile Navigation Links -->
          <nav class="space-y-1">
            <router-link
              v-for="item in navigationItems"
              :key="item.path"
              :to="item.path"
              class="block px-4 py-2 text-gray-600 hover:text-primary-500 hover:bg-gray-50 font-medium transition-colors"
              active-class="text-primary-500 bg-primary-50"
              @click="showMobileMenu = false"
            >
              {{ item.name }}
            </router-link>
          </nav>
        </div>
      </transition>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  ShoppingCartIcon,
  UserIcon,
  MagnifyingGlassIcon,
  Bars3Icon,
  XMarkIcon
} from '@heroicons/vue/24/outline'

interface NavigationItem {
  name: string
  path: string
}

interface UserMenuItem {
  name: string
  href?: string
  action?: () => void
}

interface Props {
  storeName?: string
  logoText?: string
  navigationItems?: NavigationItem[]
  showSearch?: boolean
  showCart?: boolean
  cartItemCount?: number
}

const props = withDefaults(defineProps<Props>(), {
  storeName: 'Local Store',
  logoText: 'LS',
  navigationItems: () => [
    { name: 'Home', path: '/' },
    { name: 'Products', path: '/products' },
    { name: 'About', path: '/about' },
    { name: 'Contact', path: '/contact' }
  ],
  showSearch: true,
  showCart: true,
  cartItemCount: 0
})

interface Emits {
  (e: 'toggle-cart'): void
  (e: 'search', query: string): void
}

const emit = defineEmits<Emits>()

const router = useRouter()

// State
const searchQuery = ref('')
const showMobileMenu = ref(false)
const showUserMenu = ref(false)
const userMenuRef = ref<HTMLElement>()

// User menu items
const userMenuItems = computed<UserMenuItem[]>(() => [
  { name: 'Profile', href: '/profile' },
  { name: 'Orders', href: '/orders' },
  { name: 'Settings', href: '/settings' },
  { name: 'Sign Out', action: handleSignOut }
])

// Methods
const toggleCart = () => {
  emit('toggle-cart')
}

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    emit('search', searchQuery.value.trim())
    router.push(`/search?q=${encodeURIComponent(searchQuery.value.trim())}`)
  }
}

const handleSignOut = () => {
  // TODO: Implement sign out logic
  console.log('Sign out clicked')
  showUserMenu.value = false
}

// Close dropdowns when clicking outside
const handleClickOutside = (event: MouseEvent) => {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target as Node)) {
    showUserMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// Close mobile menu on route change
router.afterEach(() => {
  showMobileMenu.value = false
})
</script> 
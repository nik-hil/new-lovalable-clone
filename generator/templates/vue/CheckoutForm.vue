<template>
  <form @submit.prevent="handleSubmit" class="checkout-form space-y-6">
    <!-- Customer Information -->
    <div class="section">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Customer Information</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          v-model="form.firstName"
          label="First Name"
          name="firstName"
          required
          :error-message="errors.firstName"
        />
        <Input
          v-model="form.lastName"
          label="Last Name"
          name="lastName"
          required
          :error-message="errors.lastName"
        />
        <Input
          v-model="form.email"
          type="email"
          label="Email Address"
          name="email"
          required
          :error-message="errors.email"
          class="md:col-span-2"
        />
        <Input
          v-model="form.phone"
          type="tel"
          label="Phone Number"
          name="phone"
          :error-message="errors.phone"
        />
      </div>
    </div>

    <!-- Shipping Address -->
    <div class="section">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Shipping Address</h3>
      <div class="space-y-4">
        <Input
          v-model="form.shippingAddress.street"
          label="Street Address"
          name="street"
          required
          :error-message="errors['shippingAddress.street']"
        />
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Input
            v-model="form.shippingAddress.city"
            label="City"
            name="city"
            required
            :error-message="errors['shippingAddress.city']"
          />
          <Input
            v-model="form.shippingAddress.state"
            type="select"
            label="State/Province"
            name="state"
            required
            :options="stateOptions"
            :error-message="errors['shippingAddress.state']"
          />
          <Input
            v-model="form.shippingAddress.zipCode"
            label="ZIP/Postal Code"
            name="zipCode"
            required
            :error-message="errors['shippingAddress.zipCode']"
          />
        </div>
        <Input
          v-model="form.shippingAddress.country"
          type="select"
          label="Country"
          name="country"
          required
          :options="countryOptions"
          :error-message="errors['shippingAddress.country']"
        />
      </div>
    </div>

    <!-- Billing Address -->
    <div class="section">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-900">Billing Address</h3>
        <label class="flex items-center">
          <input
            v-model="sameAsShipping"
            type="checkbox"
            class="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
          />
          <span class="ml-2 text-sm text-gray-700">Same as shipping address</span>
        </label>
      </div>
      
      <div v-if="!sameAsShipping" class="space-y-4">
        <Input
          v-model="form.billingAddress.street"
          label="Street Address"
          name="billingStreet"
          required
          :error-message="errors['billingAddress.street']"
        />
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Input
            v-model="form.billingAddress.city"
            label="City"
            name="billingCity"
            required
            :error-message="errors['billingAddress.city']"
          />
          <Input
            v-model="form.billingAddress.state"
            type="select"
            label="State/Province"
            name="billingState"
            required
            :options="stateOptions"
            :error-message="errors['billingAddress.state']"
          />
          <Input
            v-model="form.billingAddress.zipCode"
            label="ZIP/Postal Code"
            name="billingZipCode"
            required
            :error-message="errors['billingAddress.zipCode']"
          />
        </div>
        <Input
          v-model="form.billingAddress.country"
          type="select"
          label="Country"
          name="billingCountry"
          required
          :options="countryOptions"
          :error-message="errors['billingAddress.country']"
        />
      </div>
    </div>

    <!-- Shipping Method -->
    <div class="section">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Shipping Method</h3>
      <div class="space-y-3">
        <div
          v-for="method in shippingMethods"
          :key="method.id"
          class="flex items-center justify-between p-4 border border-gray-200 rounded-lg cursor-pointer hover:border-primary-300 transition-colors"
          :class="{ 'border-primary-500 bg-primary-50': form.shippingMethod === method.id }"
          @click="form.shippingMethod = method.id"
        >
          <div class="flex items-center">
            <input
              :id="`shipping-${method.id}`"
              v-model="form.shippingMethod"
              :value="method.id"
              type="radio"
              name="shippingMethod"
              class="text-primary-600 focus:ring-primary-500"
            />
            <label :for="`shipping-${method.id}`" class="ml-3 cursor-pointer">
              <div class="font-medium text-gray-900">{{ method.name }}</div>
              <div class="text-sm text-gray-600">{{ method.description }}</div>
              <div class="text-xs text-gray-500">{{ method.estimatedDelivery }}</div>
            </label>
          </div>
          <div class="font-semibold text-gray-900">
            {{ method.price === 0 ? 'Free' : formatPrice(method.price) }}
          </div>
        </div>
      </div>
    </div>

    <!-- Payment Information -->
    <div class="section">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Payment Information</h3>
      
      <!-- Payment Method Selection -->
      <div class="mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div
            v-for="method in paymentMethods"
            :key="method.id"
            class="payment-method-card p-3 border border-gray-200 rounded-lg cursor-pointer hover:border-primary-300 transition-colors"
            :class="{ 'border-primary-500 bg-primary-50': form.paymentMethod === method.id }"
            @click="form.paymentMethod = method.id"
          >
            <div class="flex items-center justify-center">
              <input
                :id="`payment-${method.id}`"
                v-model="form.paymentMethod"
                :value="method.id"
                type="radio"
                name="paymentMethod"
                class="sr-only"
              />
              <label :for="`payment-${method.id}`" class="text-center cursor-pointer">
                <div class="text-2xl mb-1">{{ method.icon }}</div>
                <div class="text-sm font-medium">{{ method.name }}</div>
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- Credit Card Form -->
      <div v-if="form.paymentMethod === 'card'" class="space-y-4">
        <Input
          v-model="form.cardNumber"
          label="Card Number"
          name="cardNumber"
          placeholder="1234 5678 9012 3456"
          required
          :error-message="errors.cardNumber"
          maxLength="19"
        />
        <div class="grid grid-cols-2 gap-4">
          <Input
            v-model="form.expiryDate"
            label="Expiry Date"
            name="expiryDate"
            placeholder="MM/YY"
            required
            :error-message="errors.expiryDate"
            maxLength="5"
          />
          <Input
            v-model="form.cvv"
            label="CVV"
            name="cvv"
            placeholder="123"
            required
            :error-message="errors.cvv"
            maxLength="4"
          />
        </div>
        <Input
          v-model="form.cardName"
          label="Name on Card"
          name="cardName"
          required
          :error-message="errors.cardName"
        />
      </div>
    </div>

    <!-- Order Notes -->
    <div class="section">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Order Notes (Optional)</h3>
      <Input
        v-model="form.notes"
        type="textarea"
        name="notes"
        placeholder="Special delivery instructions, gift message, etc."
        :rows="3"
        :max-length="500"
        :show-char-count="true"
      />
    </div>

    <!-- Terms and Conditions -->
    <div class="section">
      <label class="flex items-start">
        <input
          v-model="form.agreeToTerms"
          type="checkbox"
          required
          class="mt-1 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
        />
        <span class="ml-2 text-sm text-gray-700">
          I agree to the 
          <router-link to="/terms" class="text-primary-600 hover:text-primary-500">
            Terms of Service
          </router-link>
          and 
          <router-link to="/privacy" class="text-primary-600 hover:text-primary-500">
            Privacy Policy
          </router-link>
        </span>
      </label>
      <p v-if="errors.agreeToTerms" class="mt-1 text-sm text-red-600">
        {{ errors.agreeToTerms }}
      </p>
    </div>

    <!-- Submit Button -->
    <div class="pt-6 border-t border-gray-200">
      <Button
        type="submit"
        variant="primary"
        size="lg"
        :loading="submitting"
        :disabled="!form.agreeToTerms"
        full-width
      >
        {{ submitting ? 'Processing...' : `Place Order - ${formatPrice(totalAmount)}` }}
      </Button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import Input from './Input.vue'
import Button from './Button.vue'

interface Address {
  street: string
  city: string
  state: string
  zipCode: string
  country: string
}

interface ShippingMethod {
  id: string
  name: string
  description: string
  price: number
  estimatedDelivery: string
}

interface PaymentMethod {
  id: string
  name: string
  icon: string
}

interface Props {
  shippingMethods?: ShippingMethod[]
  paymentMethods?: PaymentMethod[]
  totalAmount: number
}

interface Emits {
  (e: 'submit', formData: any): void
}

const props = withDefaults(defineProps<Props>(), {
  shippingMethods: () => [
    {
      id: 'standard',
      name: 'Standard Shipping',
      description: 'Ships within 5-7 business days',
      price: 5.99,
      estimatedDelivery: 'Dec 20-25'
    },
    {
      id: 'express',
      name: 'Express Shipping',
      description: 'Ships within 2-3 business days',
      price: 12.99,
      estimatedDelivery: 'Dec 18-20'
    },
    {
      id: 'overnight',
      name: 'Overnight Shipping',
      description: 'Ships next business day',
      price: 24.99,
      estimatedDelivery: 'Dec 17'
    }
  ],
  paymentMethods: () => [
    { id: 'card', name: 'Credit Card', icon: '💳' },
    { id: 'paypal', name: 'PayPal', icon: '🔵' },
    { id: 'apple', name: 'Apple Pay', icon: '🍎' }
  ]
})

const emit = defineEmits<Emits>()

// Form data
const form = reactive({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  shippingAddress: {
    street: '',
    city: '',
    state: '',
    zipCode: '',
    country: 'US'
  } as Address,
  billingAddress: {
    street: '',
    city: '',
    state: '',
    zipCode: '',
    country: 'US'
  } as Address,
  shippingMethod: 'standard',
  paymentMethod: 'card',
  cardNumber: '',
  expiryDate: '',
  cvv: '',
  cardName: '',
  notes: '',
  agreeToTerms: false
})

// State
const submitting = ref(false)
const sameAsShipping = ref(true)
const errors = ref<Record<string, string>>({})

// Options
const stateOptions = [
  { value: 'AL', label: 'Alabama' },
  { value: 'CA', label: 'California' },
  { value: 'NY', label: 'New York' },
  { value: 'TX', label: 'Texas' },
  // Add more states...
]

const countryOptions = [
  { value: 'US', label: 'United States' },
  { value: 'CA', label: 'Canada' },
  { value: 'UK', label: 'United Kingdom' },
  // Add more countries...
]

// Methods
const formatPrice = (price: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(price)
}

const validateForm = (): boolean => {
  errors.value = {}

  // Required field validation
  if (!form.firstName.trim()) errors.value.firstName = 'First name is required'
  if (!form.lastName.trim()) errors.value.lastName = 'Last name is required'
  if (!form.email.trim()) errors.value.email = 'Email is required'
  if (!form.shippingAddress.street.trim()) errors.value['shippingAddress.street'] = 'Street address is required'
  if (!form.shippingAddress.city.trim()) errors.value['shippingAddress.city'] = 'City is required'
  if (!form.shippingAddress.state.trim()) errors.value['shippingAddress.state'] = 'State is required'
  if (!form.shippingAddress.zipCode.trim()) errors.value['shippingAddress.zipCode'] = 'ZIP code is required'

  // Email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (form.email && !emailRegex.test(form.email)) {
    errors.value.email = 'Please enter a valid email address'
  }

  // Payment validation
  if (form.paymentMethod === 'card') {
    if (!form.cardNumber.trim()) errors.value.cardNumber = 'Card number is required'
    if (!form.expiryDate.trim()) errors.value.expiryDate = 'Expiry date is required'
    if (!form.cvv.trim()) errors.value.cvv = 'CVV is required'
    if (!form.cardName.trim()) errors.value.cardName = 'Name on card is required'
  }

  // Terms validation
  if (!form.agreeToTerms) {
    errors.value.agreeToTerms = 'You must agree to the terms and conditions'
  }

  return Object.keys(errors.value).length === 0
}

const handleSubmit = async () => {
  if (!validateForm()) return

  submitting.value = true

  try {
    // Copy billing address from shipping if same
    const formData = { ...form }
    if (sameAsShipping.value) {
      formData.billingAddress = { ...form.shippingAddress }
    }

    emit('submit', formData)
  } catch (error) {
    console.error('Checkout submission failed:', error)
  } finally {
    submitting.value = false
  }
}

// Watch for same as shipping checkbox
watch(sameAsShipping, (newValue) => {
  if (newValue) {
    form.billingAddress = { ...form.shippingAddress }
  }
})

// Format card number input
watch(() => form.cardNumber, (newValue) => {
  // Remove all non-digits
  const digitsOnly = newValue.replace(/\D/g, '')
  // Add spaces every 4 digits
  const formatted = digitsOnly.replace(/(\d{4})(?=\d)/g, '$1 ')
  if (formatted !== newValue) {
    form.cardNumber = formatted
  }
})

// Format expiry date input
watch(() => form.expiryDate, (newValue) => {
  const digitsOnly = newValue.replace(/\D/g, '')
  let formatted = digitsOnly
  if (digitsOnly.length >= 2) {
    formatted = `${digitsOnly.slice(0, 2)}/${digitsOnly.slice(2, 4)}`
  }
  if (formatted !== newValue) {
    form.expiryDate = formatted
  }
})
</script>

<style scoped>
.checkout-form .section {
  @apply bg-white p-6 rounded-lg border border-gray-200;
}

.payment-method-card {
  @apply transition-all duration-200;
}

.payment-method-card:hover {
  @apply shadow-md;
}
</style> 
<template>
  <div class="input-wrapper">
    <label 
      v-if="label"
      :for="inputId"
      class="block text-sm font-medium text-gray-700 mb-1"
      :class="{ 'text-red-700': hasError }"
    >
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1">*</span>
    </label>
    
    <div class="relative">
      <!-- Text Input -->
      <input
        v-if="type !== 'textarea' && type !== 'select'"
        :id="inputId"
        :type="type"
        :name="name"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :min="min"
        :max="max"
        :step="step"
        :pattern="pattern"
        :autocomplete="autocomplete"
        :class="inputClasses"
        @input="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
      />
      
      <!-- Textarea -->
      <textarea
        v-else-if="type === 'textarea'"
        :id="inputId"
        :name="name"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :rows="rows"
        :class="textareaClasses"
        @input="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
      ></textarea>
      
      <!-- Select -->
      <select
        v-else-if="type === 'select'"
        :id="inputId"
        :name="name"
        :value="modelValue"
        :disabled="disabled"
        :required="required"
        :class="selectClasses"
        @change="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
      >
        <option value="" disabled>{{ placeholder || 'Select an option' }}</option>
        <option
          v-for="option in options"
          :key="getOptionValue(option)"
          :value="getOptionValue(option)"
        >
          {{ getOptionLabel(option) }}
        </option>
      </select>
      
      <!-- Prefix Icon -->
      <div 
        v-if="prefixIcon"
        class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
      >
        <component :is="prefixIcon" class="h-5 w-5 text-gray-400" />
      </div>
      
      <!-- Suffix Icon -->
      <div 
        v-if="suffixIcon"
        class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none"
      >
        <component :is="suffixIcon" class="h-5 w-5 text-gray-400" />
      </div>
      
      <!-- Clear Button -->
      <button
        v-if="clearable && modelValue && !disabled"
        @click="clearInput"
        type="button"
        class="absolute inset-y-0 right-0 pr-3 flex items-center"
      >
        <XMarkIcon class="h-4 w-4 text-gray-400 hover:text-gray-600" />
      </button>
    </div>
    
    <!-- Help Text -->
    <p 
      v-if="helpText && !hasError"
      class="mt-1 text-sm text-gray-500"
    >
      {{ helpText }}
    </p>
    
    <!-- Error Message -->
    <p 
      v-if="hasError"
      class="mt-1 text-sm text-red-600"
      role="alert"
    >
      {{ errorMessage }}
    </p>
    
    <!-- Character Count -->
    <p 
      v-if="showCharCount && maxLength"
      class="mt-1 text-xs text-gray-500 text-right"
    >
      {{ characterCount }}/{{ maxLength }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'

type InputType = 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search' | 'textarea' | 'select'

interface Option {
  label: string
  value: string | number
}

interface Props {
  modelValue?: string | number
  type?: InputType
  name?: string
  label?: string
  placeholder?: string
  helpText?: string
  errorMessage?: string
  disabled?: boolean
  readonly?: boolean
  required?: boolean
  clearable?: boolean
  size?: 'sm' | 'md' | 'lg'
  variant?: 'default' | 'filled' | 'outlined'
  prefixIcon?: any
  suffixIcon?: any
  // Number inputs
  min?: number
  max?: number
  step?: number
  // Text inputs
  pattern?: string
  maxLength?: number
  showCharCount?: boolean
  autocomplete?: string
  // Textarea
  rows?: number
  // Select
  options?: (Option | string)[]
}

interface Emits {
  (e: 'update:modelValue', value: string | number): void
  (e: 'blur', event: FocusEvent): void
  (e: 'focus', event: FocusEvent): void
  (e: 'clear'): void
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  size: 'md',
  variant: 'default',
  rows: 3,
  options: () => []
})

const emit = defineEmits<Emits>()

// State
const inputId = ref(`input-${Math.random().toString(36).substr(2, 9)}`)
const isFocused = ref(false)

// Computed
const hasError = computed(() => Boolean(props.errorMessage))

const characterCount = computed(() => {
  return String(props.modelValue || '').length
})

const baseInputClasses = computed(() => {
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-3 py-2 text-base',
    lg: 'px-4 py-3 text-lg'
  }
  
  const variantClasses = {
    default: 'border border-gray-300 bg-white',
    filled: 'border-0 bg-gray-100',
    outlined: 'border-2 border-gray-300 bg-transparent'
  }
  
  const stateClasses = hasError.value
    ? 'border-red-300 text-red-900 placeholder-red-300 focus:outline-none focus:ring-red-500 focus:border-red-500'
    : 'border-gray-300 placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500'
    
  const disabledClasses = props.disabled
    ? 'bg-gray-50 text-gray-500 cursor-not-allowed'
    : ''
    
  const paddingClasses = props.prefixIcon ? 'pl-10' : props.suffixIcon || props.clearable ? 'pr-10' : ''
  
  return [
    'block w-full rounded-lg shadow-sm transition-colors',
    sizeClasses[props.size],
    variantClasses[props.variant],
    stateClasses,
    disabledClasses,
    paddingClasses
  ].join(' ')
})

const inputClasses = computed(() => baseInputClasses.value)
const textareaClasses = computed(() => `${baseInputClasses.value} resize-vertical`)
const selectClasses = computed(() => `${baseInputClasses.value} pr-10`)

// Methods
const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
  let value: string | number = target.value
  
  // Convert to number for number inputs
  if (props.type === 'number' && value !== '') {
    value = Number(value)
  }
  
  emit('update:modelValue', value)
}

const handleBlur = (event: FocusEvent) => {
  isFocused.value = false
  emit('blur', event)
}

const handleFocus = (event: FocusEvent) => {
  isFocused.value = true
  emit('focus', event)
}

const clearInput = () => {
  emit('update:modelValue', '')
  emit('clear')
}

const getOptionValue = (option: Option | string): string | number => {
  return typeof option === 'string' ? option : option.value
}

const getOptionLabel = (option: Option | string): string => {
  return typeof option === 'string' ? option : option.label
}

// Watch for character limit
watch(() => props.modelValue, (newValue) => {
  if (props.maxLength && String(newValue || '').length > props.maxLength) {
    const truncated = String(newValue || '').slice(0, props.maxLength)
    emit('update:modelValue', truncated)
  }
})
</script>

<style scoped>
/* Remove default select arrow in favor of custom styling */
select {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

/* Custom focus styles */
.input-wrapper:focus-within label {
  @apply text-primary-700;
}
</style> 
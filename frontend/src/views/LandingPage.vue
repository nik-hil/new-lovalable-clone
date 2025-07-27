<template>
  <div class="landing-page">
    <!-- Animated background particles -->
    <div class="particles">
      <div v-for="i in 6" :key="i" class="particle" :style="getParticleStyle(i)"></div>
    </div>

    <!-- Main content -->
    <div class="container">
      <!-- Hero section -->
      <div class="hero-section animate-slide-up">
        <h1 class="hero-title">
          Craft extraordinary websites.<br>
          <span class="gradient-text">One thought. Infinite possibilities.</span>
        </h1>
        
        <p class="hero-subtitle animate-fade-in">
          Transform your vision into stunning, modern web experiences with AI-powered design
        </p>
      </div>

      <!-- Generation form -->
      <div class="generation-form glass-effect modern-shadow animate-slide-up">
        <form @submit.prevent="generateWebsite">
          <div class="input-group">
            <textarea
              v-model="prompt"
              class="prompt-input"
              rows="3"
              placeholder="Describe your vision — a revolutionary fintech platform, an immersive portfolio experience, or a premium e-commerce destination"
              required
              :disabled="isGenerating"
            ></textarea>
          </div>
          
          <button 
            type="submit" 
            class="generate-btn modern-shadow"
            :disabled="isGenerating || !prompt.trim()"
            :class="{ generating: isGenerating }"
          >
            <span v-if="!isGenerating" class="btn-text">
              ✨ Create
            </span>
            <span v-else class="generating-content">
              <span class="hourglass animate-spin">⌛</span>
              <span class="generating-text">Creating magic...</span>
            </span>
          </button>
        </form>

        <!-- Pro tip -->
        <div class="pro-tip">
          <span class="tip-icon">💡</span>
          <div class="tip-content">
            <strong>Pro tip:</strong> Create full-stack applications! For data-driven sites (e.g., "flower shop with orders", "blog with posts", "booking system"), I'll generate complete Vue.js frontends with backend APIs. For refinements, simply describe your vision — "embrace minimalism", or "add new features"
          </div>
        </div>
      </div>

      <!-- Clear all button -->
      <div class="actions-section animate-fade-in">
        <button @click="clearAll" class="clear-btn" :disabled="isGenerating">
          🗑️ Clear All & Start New
        </button>
      </div>

      <!-- Preview section -->
      <div v-if="previewUrl" class="preview-section glass-effect modern-shadow animate-slide-up">
        <div class="preview-header">
          <h3>Live Preview</h3>
          <div class="preview-actions">
            <button @click="refineWebsite" class="action-btn secondary" :disabled="isGenerating">
              ✨ Refine Experience
            </button>
            <button @click="downloadZip" class="action-btn success">
              📦 Export Project
            </button>
            <a :href="newTabUrl" target="_blank" class="action-btn primary">
              🚀 Launch Experience
            </a>
          </div>
        </div>
        <iframe 
          :src="previewUrl" 
          class="preview-iframe"
          @load="onPreviewLoad"
        ></iframe>
      </div>

      <!-- Error message -->
      <div v-if="errorMessage" class="error-message animate-slide-up">
        <span class="error-icon">❌</span>
        {{ errorMessage }}
      </div>

      <!-- Success message -->
      <div v-if="successMessage" class="success-message animate-slide-up">
        <span class="success-icon">✅</span>
        {{ successMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'LandingPage',
  setup() {
    const prompt = ref('')
    const isGenerating = ref(false)
    const previewUrl = ref('')
    const newTabUrl = ref('')
    const errorMessage = ref('')
    const successMessage = ref('')
    const filesGenerated = ref([])

    const generateWebsite = async () => {
      if (!prompt.value.trim()) return

      isGenerating.value = true
      errorMessage.value = ''
      successMessage.value = ''

      try {
        const formData = new FormData()
        formData.append('prompt', prompt.value)

        const response = await axios.post('/api/generate', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })

        if (response.data.preview_url) {
          previewUrl.value = `/api${response.data.preview_url}`
          newTabUrl.value = response.data.new_tab_url || previewUrl.value
          filesGenerated.value = response.data.files_generated || []
          
          successMessage.value = `Successfully generated ${filesGenerated.value.length} files`
          
          // Clear the textarea for next prompt
          prompt.value = ''
          
          // Show success message temporarily
          setTimeout(() => {
            successMessage.value = ''
          }, 3000)
        } else {
          errorMessage.value = response.data.error || 'Something went wrong.'
        }
      } catch (error) {
        console.error('Generation error:', error)
        errorMessage.value = error.response?.data?.error || 'Connection interrupted. Please try again.'
      } finally {
        isGenerating.value = false
      }
    }

    const clearAll = async () => {
      if (!confirm('This will clear all generated files and start a new project. Are you sure?')) {
        return
      }

      try {
        const response = await axios.post('/api/clear-all')
        
        if (response.data.success) {
          previewUrl.value = ''
          newTabUrl.value = ''
          prompt.value = ''
          errorMessage.value = ''
          filesGenerated.value = []
          
          successMessage.value = '✅ Project cleared successfully!'
          setTimeout(() => {
            successMessage.value = ''
          }, 3000)
        } else {
          errorMessage.value = 'Error clearing project: ' + (response.data.error || 'Unknown error')
        }
      } catch (error) {
        console.error('Clear error:', error)
        errorMessage.value = 'Error clearing project: ' + error.message
      }
    }

    const refineWebsite = () => {
      const textarea = document.querySelector('.prompt-input')
      if (textarea) {
        textarea.focus()
        prompt.value = 'Make it more modern and beautiful with better animations and colors'
      }
    }

    const downloadZip = async () => {
      if (!previewUrl.value) {
        errorMessage.value = 'Please generate a website first before exporting.'
        return
      }

      try {
        const response = await axios.get('/api/download-zip', {
          responseType: 'blob'
        })

        if (response.data) {
          const url = window.URL.createObjectURL(new Blob([response.data]))
          const link = document.createElement('a')
          link.href = url
          link.download = 'website.zip'
          document.body.appendChild(link)
          link.click()
          window.URL.revokeObjectURL(url)
          document.body.removeChild(link)
          
          successMessage.value = '📦 Project exported successfully!'
          setTimeout(() => {
            successMessage.value = ''
          }, 3000)
        }
      } catch (error) {
        console.error('Download error:', error)
        errorMessage.value = 'Export failed. Please try again.'
      }
    }

    const onPreviewLoad = () => {
      console.log('Preview loaded successfully')
    }

    const getParticleStyle = (index) => {
      const colors = [
        'rgba(102, 126, 234, 0.1)',
        'rgba(118, 75, 162, 0.1)',
        'rgba(255, 119, 198, 0.1)',
        'rgba(255, 177, 153, 0.1)',
        'rgba(158, 90, 243, 0.1)',
        'rgba(255, 145, 77, 0.1)'
      ]
      
      return {
        background: colors[index - 1],
        left: `${10 + (index * 15)}%`,
        top: `${5 + (index * 10)}%`,
        animationDelay: `${index * 0.5}s`,
        animationDuration: `${6 + index}s`
      }
    }

    onMounted(() => {
      // Add staggered animation to elements
      const elements = document.querySelectorAll('.animate-slide-up')
      elements.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.1}s`
      })
    })

    return {
      prompt,
      isGenerating,
      previewUrl,
      newTabUrl,
      errorMessage,
      successMessage,
      filesGenerated,
      generateWebsite,
      clearAll,
      refineWebsite,
      downloadZip,
      onPreviewLoad,
      getParticleStyle
    }
  }
}
</script>

<style scoped>
.landing-page {
  min-height: 100vh;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  overflow: hidden;
}

.particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.particle {
  position: absolute;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;
}

.container {
  position: relative;
  z-index: 2;
  max-width: 1000px;
  width: 100%;
  text-align: center;
}

.hero-section {
  margin-bottom: 3rem;
}

.hero-title {
  font-size: clamp(2.5rem, 6vw, 4rem);
  font-weight: 700;
  color: white;
  margin-bottom: 1.5rem;
  line-height: 1.2;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.hero-subtitle {
  font-size: clamp(1.1rem, 2.5vw, 1.3rem);
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 2rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.6;
}

.generation-form {
  padding: 2.5rem;
  margin-bottom: 2rem;
  transition: all 0.3s ease;
}

.generation-form:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.input-group {
  margin-bottom: 1.5rem;
}

.prompt-input {
  width: 100%;
  padding: 1.5rem;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 1.1rem;
  font-family: inherit;
  resize: vertical;
  min-height: 120px;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.prompt-input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.prompt-input:focus {
  outline: none;
  border-color: rgba(255, 255, 255, 0.5);
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.1);
}

.generate-btn {
  padding: 1.2rem 3rem;
  border: none;
  border-radius: 50px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  color: white;
  font-size: 1.2rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 200px;
  position: relative;
  overflow: hidden;
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
}

.generate-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.generate-btn.generating {
  background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
}

.generating-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.hourglass {
  font-size: 1.2rem;
  display: inline-block;
}

.generating-text {
  font-size: 1rem;
}

.pro-tip {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  margin-top: 1.5rem;
  text-align: left;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.tip-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.tip-content {
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
  font-size: 0.95rem;
}

.actions-section {
  margin-bottom: 2rem;
}

.clear-btn {
  padding: 0.8rem 1.5rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50px;
  background: transparent;
  color: white;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.clear-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
}

.preview-section {
  padding: 2rem;
  margin-bottom: 2rem;
  text-align: left;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.preview-header h3 {
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
}

.preview-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.7rem 1.2rem;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.action-btn.secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.action-btn.success {
  background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.preview-iframe {
  width: 100%;
  height: 600px;
  border: none;
  border-radius: 12px;
  background: white;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.error-message,
.success-message {
  padding: 1.2rem 1.5rem;
  border-radius: 12px;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  font-weight: 500;
}

.error-message {
  background: rgba(255, 69, 58, 0.15);
  border: 1px solid rgba(255, 69, 58, 0.3);
  color: #ff6b6b;
}

.success-message {
  background: rgba(52, 199, 89, 0.15);
  border: 1px solid rgba(52, 199, 89, 0.3);
  color: #2ecc71;
}

.error-icon,
.success-icon {
  font-size: 1.2rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .landing-page {
    padding: 1rem;
  }

  .generation-form {
    padding: 1.5rem;
  }

  .preview-header {
    flex-direction: column;
    align-items: stretch;
    text-align: center;
  }

  .preview-actions {
    justify-content: center;
  }

  .preview-iframe {
    height: 400px;
  }

  .pro-tip {
    flex-direction: column;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2rem;
  }

  .generate-btn {
    width: 100%;
    padding: 1rem;
  }

  .action-btn {
    flex: 1;
    text-align: center;
  }
}
</style> 
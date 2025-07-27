import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def is_data_driven_request(prompt: str) -> bool:
    """
    Detect if the request requires backend/database functionality
    """
    prompt_lower = prompt.lower()
    
    # Strong indicators that backend is needed (data management)
    strong_backend_keywords = [
        'order', 'orders', 'ordering', 'purchase', 'buy', 'cart', 'checkout',
        'user account', 'login', 'register', 'registration', 'signup', 'authentication',
        'booking', 'reservation', 'appointment', 'schedule',
        'inventory', 'manage products', 'admin panel', 'dashboard',
        'contact form', 'form submission', 'submit data',
        'crud', 'database', 'store data', 'save data',
        'user management', 'payment', 'subscription'
    ]
    
    # Weaker indicators that might not need backend (static content)
    weak_backend_keywords = [
        'blog', 'post', 'posts', 'article', 'comment',
        'portfolio', 'gallery', 'showcase',
        'product catalog', 'product list'
    ]
    
    # Static website indicators
    static_indicators = [
        'static', 'simple', 'landing page', 'brochure',
        'informational', 'about', 'showcase', 'display'
    ]
    
    # Check for strong backend indicators
    if any(keyword in prompt_lower for keyword in strong_backend_keywords):
        return True
    
    # If it's explicitly static, return false
    if any(indicator in prompt_lower for indicator in static_indicators):
        return False
    
    # For weak indicators, check context
    weak_matches = [keyword for keyword in weak_backend_keywords if keyword in prompt_lower]
    if weak_matches:
        # If it mentions user interaction, commenting, or management, then backend needed
        interaction_keywords = ['comment', 'user', 'manage', 'add', 'edit', 'delete', 'submit']
        if any(keyword in prompt_lower for keyword in interaction_keywords):
            return True
        # Otherwise, assume static blog/portfolio
        return False
    
    return False

def validate_generated_files(files: dict, is_backend_required: bool) -> tuple[bool, list]:
    """
    Validate that all required files were generated
    """
    missing_files = []
    
    # Check for essential frontend files (Vue.js or traditional)
    has_html = any('html' in filename.lower() for filename in files.keys())
    has_vue = any('vue' in filename.lower() for filename in files.keys())
    has_main_js = any('main.js' in filename for filename in files.keys())
    has_css = any('css' in filename.lower() for filename in files.keys())
    
    if not has_html:
        missing_files.append('HTML file')
    if not has_vue and not has_main_js:
        missing_files.append('Vue.js component (App.vue) or main.js')
    if not has_css:
        missing_files.append('CSS file')
    
    # Only check for backend files if explicitly required
    if is_backend_required:
        has_flask = any(
            'app.py' in filename or 
            ('flask' in content.lower() and 'from flask import' in content) 
            for filename, content in files.items()
        )
        has_schema = any('schema.sql' in filename for filename in files.keys())
        has_database = any('database.py' in filename for filename in files.keys())
        
        if not has_flask:
            missing_files.append('Flask backend (app.py)')
        if not (has_schema or has_database):
            missing_files.append('Database files (database.py or schema.sql)')
    
    return len(missing_files) == 0, missing_files

def generate_missing_files(prompt: str, existing_files: dict, missing_files: list, model) -> dict:
    """
    Generate specific missing files with targeted prompts
    """
    generated_files = {}
    
    for missing_file_type in missing_files:
        try:
            if "Flask backend" in missing_file_type:
                # Generate Flask app.py
                flask_prompt = f"""
Create a complete Flask backend for: {prompt}

Generate ONLY the app.py file with:
- Flask application with all necessary imports
- CORS configuration
- API endpoints for CRUD operations
- Database integration using database.py
- Error handling and validation

Format your response as:
**app.py:**
```python
[Complete Flask code here]
```
"""
                response = model.generate_content(flask_prompt)
                files = parse_gemini_response(response.text)
                if 'app.py' in files:
                    generated_files['app.py'] = files['app.py']
                    print(f"Debug: Generated Flask app.py ({len(files['app.py'])} chars)")
            
            elif "Database files" in missing_file_type:
                # Generate database.py and schema.sql
                db_prompt = f"""
Create database files for: {prompt}

Generate these files:
1. database.py - MySQL connection and helper functions
2. schema.sql - Complete database schema

Use MySQL settings: host='mysql', user='lovable_user', password='lovable_password', database='lovable_db'

Format your response as:
**database.py:**
```python
[Database connection code here]
```

**schema.sql:**
```sql
[Database schema here]
```
"""
                response = model.generate_content(db_prompt)
                files = parse_gemini_response(response.text)
                generated_files.update(files)
                print(f"Debug: Generated database files: {list(files.keys())}")
            
            elif "script.js" in missing_file_type or "JavaScript" in missing_file_type:
                # Generate JavaScript file
                js_prompt = f"""
Create a comprehensive JavaScript file for: {prompt}

The script MUST include:
- DOM event listeners for all forms and buttons
- Form validation and submission handling
- Fetch API calls to backend endpoints (if backend exists)
- Interactive features like animations, modal dialogs, image galleries
- Error handling and user feedback messages
- Smooth scrolling and navigation
- Dynamic content updates
- Modern ES6+ features where appropriate
- Mobile-responsive touch interactions
- Accessibility enhancements

Generate practical, working JavaScript code that enhances the user experience. Make it substantial (minimum 100+ lines) with proper functionality.

Format your response as:
**script.js:**
```javascript
[Complete functional JavaScript code here - minimum 100 lines with comprehensive features]
```
"""
                response = model.generate_content(js_prompt)
                files = parse_gemini_response(response.text)
                if 'script.js' in files and len(files['script.js']) > 200:  # Ensure substantial content
                    generated_files['script.js'] = files['script.js']
                    print(f"Debug: Generated script.js ({len(files['script.js'])} chars)")
                else:
                    # Fallback: create a robust interactive script
                    generated_files['script.js'] = """// Enhanced interactivity and modern features for the website
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize modern interaction features
    initializeAnimations();
    initializeFormHandling();
    initializeNavigation();
    initializeModals();
    initializeAccessibility();
    initializeMobileFeatures();
    
    // Modern animations with intersection observer
    function initializeAnimations() {
        const animatedElements = document.querySelectorAll('.animate-on-scroll, .card, .product-item, .service-item, .feature, .hero');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        });
        
        animatedElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        });
        
        // Enhanced button hover effects
        const buttons = document.querySelectorAll('button, .btn, .cta-button, .submit-btn');
        buttons.forEach(btn => {
            btn.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-3px) scale(1.02)';
                this.style.boxShadow = '0 10px 30px rgba(0,0,0,0.2)';
            });
            btn.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
                this.style.boxShadow = '0 4px 15px rgba(0,0,0,0.1)';
            });
        });
    }
}"""
                    print("Debug: Generated fallback script.js")
            
            elif ".env.example" in missing_file_type:
                # Generate environment variables template
                generated_files['.env.example'] = """# Database Configuration
DB_HOST=mysql
DB_USER=lovable_user
DB_PASSWORD=lovable_password
DB_NAME=lovable_db

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key-here
"""
                print("Debug: Generated .env.example")
                
        except Exception as e:
            print(f"Debug: Error generating {missing_file_type}: {e}")
            continue
    
    return generated_files

def create_website(prompt: str):
    """
    This function takes a prompt and creates or modifies a website based on it.
    Uses an iterative approach to generate all required files.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"error": "GEMINI_API_KEY not found. Please create a .env file with your Gemini API key."}
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
    except Exception as e:
        return {"error": f"Failed to initialize Gemini AI: {str(e)}"}

    # Check for existing files in the output directory
    existing_files = {}
    output_dir = "../output"
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            filepath = os.path.join(output_dir, filename)
            if os.path.isfile(filepath):
                with open(filepath, "r", encoding='utf-8') as f:
                    existing_files[filename] = f.read()

    # Determine if this is a data-driven request
    requires_backend = is_data_driven_request(prompt)
    print(f"Debug: Prompt '{prompt}' requires backend: {requires_backend}")

    if existing_files:
        prompt_with_context = (
            "You are a professional web developer and UI/UX designer. Here are the existing files for a website:\n\n"
        )
        for filename, content in existing_files.items():
            prompt_with_context += f"**{filename}**:\n```\n{content}\n```\n\n"
        prompt_with_context += (
            f"Please improve and modify this website based on this request: '{prompt}'\n\n"
            "IMPORTANT DESIGN REQUIREMENTS:\n"
            "- Make the website MODERN, BEAUTIFUL, and VISUALLY APPEALING\n"
            "- Use modern CSS techniques (flexbox, grid, smooth animations, gradients)\n"
            "- Apply attractive color schemes and typography\n"
            "- Ensure responsive design for all devices\n"
            "- Add subtle animations and hover effects\n"
            "- Use proper spacing, shadows, and visual hierarchy\n"
            "- Make it look professional and polished\n\n"
            "Provide the complete, updated code for ALL files (even if only some changed).\n"
            "Format your response exactly like this:\n\n"
            "**index.html**:\n"
            "```html\n"
            "[complete HTML code here]\n"
            "```\n\n"
            "**style.css**:\n"
            "```css\n"
            "[complete CSS code here]\n"
            "```\n\n"
            "If you need JavaScript for interactions, add:\n"
            "**script.js**:\n"
            "```javascript\n"
            "[complete JavaScript code here]\n"
            "```"
        )
    else:
        # Enhanced prompt for new website generation
        if requires_backend:
            backend_instruction = """
⚠️  CRITICAL: This request involves data management and REQUIRES a complete backend system.

🔴 YOU MUST GENERATE EXACTLY THESE FILES (or the system will fail):
1. **index.html** - Frontend with forms connected to APIs
2. **style.css** - Modern styling 
3. **app.py** - Complete Flask application with all API endpoints
4. **database.py** - Database connection and helper functions  
5. **schema.sql** - Complete database schema with all tables
6. **script.js** - Frontend JavaScript for API integration
7. **.env.example** - Environment variables template

🔴 IMPORTANT: The Flask app.py MUST include:
- from flask import Flask, request, jsonify, render_template
- All CRUD API endpoints (GET, POST, PUT, DELETE)
- CORS configuration: from flask_cors import CORS
- Database integration using the database.py file

🔴 IMPORTANT: The database.py MUST include:
- MySQL connection using: host='mysql', user='lovable_user', password='lovable_password', database='lovable_db'
- Helper functions for database operations

🔴 IMPORTANT: The frontend MUST include:
- Forms that submit to the Flask API endpoints
- JavaScript fetch() calls to connect to backend
- Error handling and success messages
            """
        else:
            backend_instruction = ""
        
        prompt_with_context = (
            f"You are a professional full-stack web developer. Create a modern, responsive website based on the following user request: '{prompt}'.\n\n"
            f"{backend_instruction}\n\n"
            "IMPORTANT REQUIREMENTS:\n\n"
            "If the user request involves storing or managing data (e.g., orders, user accounts, blog posts, inventory, bookings), generate a backend using Flask with MySQL as the database.\n"
            "Include the necessary database schema and API endpoints for CRUD operations.\n"
            "Ensure the generated frontend integrates seamlessly with the backend using AJAX or Fetch API.\n"
            "Make the website visually appealing, responsive, and user-friendly.\n"
            "Use contemporary design trends (clean layouts, attractive colors, modern typography).\n"
            "Apply CSS techniques like flexbox, grid, smooth animations, gradients, and shadows.\n"
            "Add subtle animations, hover effects, and micro-interactions.\n"
            "Ensure proper spacing, visual hierarchy, and professional aesthetics.\n"
            "Provide the complete, updated code for ALL files (frontend and backend).\n\n"
            "Format your response exactly like this:\n\n"
            "**index.html:**\n"
            "```html\n"
            "[HTML code here]\n"
            "```\n\n"
            "**style.css:**\n"
            "```css\n"
            "[CSS code here]\n"
            "```\n\n"
            "**app.py:** (if backend is needed)\n"
            "```python\n"
            "[Flask application code here]\n"
            "```\n\n"
            "**database.py:** (if backend is needed)\n"
            "```python\n"
            "[Database connection and models code here]\n"
            "```\n\n"
            "**schema.sql:** (if backend is needed)\n"
            "```sql\n"
            "[Database schema here]\n"
            "```\n\n"
            "**script.js:** (if needed)\n"
            "```javascript\n"
            "[JavaScript code here]\n"
            "```\n\n"
            "**.env.example:** (if backend is needed)\n"
            "```\n"
            "[Environment variables template]\n"
            "```\n\n"
            "CONTENT GUIDELINES:\n"
            "- Include realistic, relevant content (avoid Lorem Ipsum)\n"
            "- Add appropriate headings, descriptions, and calls-to-action\n"
            "- Use semantic HTML structure for accessibility\n"
            "- For backend applications, use MySQL connection settings: host='mysql', user='lovable_user', password='lovable_password', database='lovable_db'\n"
            "- Ensure frontend forms connect to backend APIs using fetch() or AJAX\n"
            "- Include proper error handling and user feedback\n"
            "- Make APIs RESTful with proper HTTP methods (GET, POST, PUT, DELETE)"
        )

    # Generate website with iterative approach
    all_generated_files = {}
    
    # Step 1: Generate initial website (frontend focus)
    initial_prompt = f"""
Create a stunning, modern, FULLY FUNCTIONAL website for: {prompt}

🎨 DESIGN REQUIREMENTS - MAKE IT STUNNING & MODERN:
- Use VIBRANT, eye-catching color palettes with rich gradients and depth
- Implement cutting-edge design trends: glassmorphism, neumorphism, gradient overlays
- Add bold, colorful gradients with multiple color stops and dynamic effects
- Use modern typography (Inter, Poppins, Outfit, Space Grotesk)
- Create strong visual hierarchy with generous whitespace and perfect spacing
- Add dynamic background effects, animated gradients, and modern textures
- Ensure the design looks premium, polished, and contemporary (2024+ aesthetic)
- Use modern CSS features: CSS Grid, Flexbox, custom properties, backdrop-filter
- Implement smooth micro-interactions and delightful hover states
- Make it responsive with mobile-first approach
- Use RICH, SATURATED colors - avoid bland, washed-out palettes
- Implement color-shifting gradients and dynamic color schemes
- Add depth with layered shadows and vibrant highlights

⚠️ CRITICAL TECHNICAL REQUIREMENTS:
- Create a WORKING website using vanilla HTML/CSS/JavaScript ONLY
- NO framework imports (no Vue.js, React, Angular, etc.)
- NO "import" statements or ES6 modules in JavaScript
- Use standard HTML with full content visible immediately
- Use vanilla JavaScript with document.addEventListener('DOMContentLoaded', ...)
- All functionality must work without any framework dependencies

Generate these core files (ALL are required):
- **index.html** - Complete HTML with ALL content (no empty divs)
- **style.css** - Beautiful, vibrant styling with bold colors and animations
- **script.js** - Interactive vanilla JavaScript (minimum 100+ lines)

For the HTML file:
- Include complete page structure with actual content
- All content must be in HTML, not loaded by JavaScript
- Use semantic HTML5 elements (header, main, section, footer)
- Include all text, headings, and content relevant to: {prompt}
- Reference only style.css and script.js files

For the CSS file:
- VIBRANT color schemes with rich, saturated colors
- Multiple gradient overlays with color-shifting effects
- Dynamic shadows with colored shadows and depth
- Smooth transitions, transforms, and modern hover interactions
- CSS Grid and Flexbox for perfect responsive layouts
- Custom CSS animations and keyframes
- Modern button designs with colorful glass/neumorphic effects
- Contemporary typography and professional spacing

For the JavaScript file:
- Use vanilla JavaScript only (no frameworks)
- DOM event listeners and interactive features
- Smooth animations and transitions
- Form handling and validation (if applicable)
- Dynamic content updates and user interactions
- Modern ES6+ features (but NO imports/modules)
- Comprehensive functionality (minimum 100+ lines)

Make it a premium, visually striking website that WORKS immediately when opened!

Format your response as:
**index.html:**
```html
[Complete HTML with all content - NO framework dependencies]
```

**style.css:**
```css
[Vibrant, modern CSS with bold colors]
```

**script.js:**
```javascript
[Comprehensive vanilla JavaScript - minimum 100 lines]
```
"""

    try:
        print("Debug: Generating initial website files...")
        response = model.generate_content(initial_prompt)
        if not response or not response.text:
            return {"error": "No response received from Gemini AI. Please try again."}
        
        initial_files = parse_gemini_response(response.text)
        print(f"Debug: Generated initial files: {list(initial_files.keys())}")
        all_generated_files.update(initial_files)
        
    except Exception as e:
        return {"error": f"Gemini AI generation failed: {str(e)}"}

    # Step 2: Check what's missing and generate additional files
    if requires_backend:
        max_iterations = 3
        for iteration in range(max_iterations):
            is_valid, missing_files = validate_generated_files(all_generated_files, requires_backend)
            
            if is_valid:
                print(f"Debug: All required files generated after {iteration + 1} iterations")
                break
            
            print(f"Debug: Iteration {iteration + 1}, missing: {missing_files}")
            
            # Generate missing files
            additional_files = generate_missing_files(prompt, all_generated_files, missing_files, model)
            if additional_files:
                all_generated_files.update(additional_files)
                print(f"Debug: Added files: {list(additional_files.keys())}")
            else:
                print("Debug: No additional files generated")
                break
    
    # Final validation and quality check
    is_valid, missing_files = validate_generated_files(all_generated_files, requires_backend)
    
    if not is_valid and requires_backend:
        print(f"Debug: Still missing files after all iterations: {missing_files}")
        # Continue anyway with a warning
    
    # Check if we have Vue.js artifacts that will cause blank pages
    has_broken_vue = (
        ('main.js' in all_generated_files and ('createApp' in all_generated_files.get('main.js', '') or 'Vue' in all_generated_files.get('main.js', ''))) or
        'App.vue' in all_generated_files or
        ('<div id="app"></div>' in all_generated_files.get('index.html', '') and len(all_generated_files.get('index.html', '')) < 1000)
    )
    
    if has_broken_vue or 'script.js' not in all_generated_files or len(all_generated_files.get('script.js', '')) < 200:
        print("Debug: Replacing broken Vue.js with working vanilla HTML for prompt:", prompt)
        
        # Create a working flower shop website
        if 'flower' in prompt.lower() or 'shop' in prompt.lower():
            title = "Bloom & Petals - Premium Flower Shop"
            hero_text = "Beautiful Flowers for Every Occasion"
            content_body = '''
    <section class="featured-flowers">
        <div class="container">
            <h2 class="section-title">Featured Flowers</h2>
            <div class="flower-grid">
                <div class="flower-card glass-effect">
                    <div class="flower-image">🌹</div>
                    <h3>Premium Roses</h3>
                    <p class="price">$25.99</p>
                    <button class="add-to-cart-btn" onclick="addToCart('roses', 25.99)">Add to Cart</button>
                </div>
                <div class="flower-card glass-effect">
                    <div class="flower-image">🌷</div>
                    <h3>Fresh Tulips</h3>
                    <p class="price">$18.99</p>
                    <button class="add-to-cart-btn" onclick="addToCart('tulips', 18.99)">Add to Cart</button>
                </div>
                <div class="flower-card glass-effect">
                    <div class="flower-image">🌺</div>
                    <h3>Exotic Lilies</h3>
                    <p class="price">$32.99</p>
                    <button class="add-to-cart-btn" onclick="addToCart('lilies', 32.99)">Add to Cart</button>
                </div>
            </div>
        </div>
    </section>
    
    <section class="order-section">
        <div class="container">
            <h2 class="section-title">Your Order</h2>
            <div class="order-container">
                <div class="cart-display glass-effect">
                    <h3>Shopping Cart</h3>
                    <div id="cartItems" class="cart-items">
                        <p class="empty-cart">Your cart is empty</p>
                    </div>
                    <div id="cartTotal" class="cart-total">Total: $0.00</div>
                </div>
                
                <form class="order-form glass-effect" id="orderForm">
                    <h3>Customer Information</h3>
                    <div class="form-group">
                        <label for="customerName">Full Name</label>
                        <input type="text" id="customerName" name="customerName" required>
                    </div>
                    <div class="form-group">
                        <label for="customerEmail">Email</label>
                        <input type="email" id="customerEmail" name="customerEmail" required>
                    </div>
                    <div class="form-group">
                        <label for="deliveryAddress">Delivery Address</label>
                        <textarea id="deliveryAddress" name="deliveryAddress" rows="3" required></textarea>
                    </div>
                    <button type="submit" class="submit-btn" id="submitOrder" disabled>Place Order</button>
                </form>
            </div>
        </div>
    </section>'''
        else:
            title = "Modern Website"
            hero_text = "Welcome to Our Amazing Website"
            content_body = '''
    <section class="features-section">
        <div class="container">
            <h2 class="section-title">Amazing Features</h2>
            <div class="features-grid">
                <div class="feature-card glass-effect">
                    <div class="feature-icon">🚀</div>
                    <h3>Lightning Fast</h3>
                    <p>Built with modern technology</p>
                </div>
                <div class="feature-card glass-effect">
                    <div class="feature-icon">🎨</div>
                    <h3>Beautiful Design</h3>
                    <p>Modern aesthetics with vibrant gradients</p>
                </div>
            </div>
        </div>
    </section>'''
        
        all_generated_files['index.html'] = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="hero-section">
        <h1 class="hero-title gradient-text">{hero_text}</h1>
        <p class="hero-subtitle">Premium fresh flowers delivered with love</p>
        <button class="cta-button" onclick="showWelcome()">Explore Our Shop</button>
    </header>

    <main class="main-content">
        {content_body}
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 {title}. All rights reserved.</p>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>"""

        all_generated_files['App.vue'] = """<template>
  <div id="app" class="app-container">
    <!-- Dynamic background -->
    <div class="animated-bg">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
    </div>

    <!-- Main content -->
    <div class="content-wrapper">
      <header class="hero-section">
        <h1 class="hero-title gradient-text animate-slide-up">
          {{ title }}
        </h1>
        <p class="hero-subtitle animate-fade-in">
          {{ subtitle }}
        </p>
        <button 
          @click="toggleMode" 
          class="cta-button animate-bounce"
          :class="{ active: isActive }"
        >
          <span class="button-content">
            <span class="icon">{{ isActive ? '🌙' : '🌟' }}</span>
            {{ buttonText }}
          </span>
        </button>
      </header>

      <!-- Feature cards -->
      <section class="features-grid">
        <div 
          v-for="(feature, index) in features" 
          :key="index"
          class="feature-card glass-effect"
          :style="{ animationDelay: index * 0.1 + 's' }"
          @mouseenter="onCardHover(index)"
          @mouseleave="onCardLeave(index)"
        >
          <div class="card-icon">{{ feature.icon }}</div>
          <h3 class="card-title">{{ feature.title }}</h3>
          <p class="card-description">{{ feature.description }}</p>
          <div class="card-accent" :class="`accent-${index + 1}`"></div>
        </div>
      </section>

      <!-- Interactive counter -->
      <section class="interactive-section">
        <div class="counter-container glass-effect">
          <h3>Interactive Counter</h3>
          <div class="counter-display">
            <span class="counter-number gradient-text">{{ counter }}</span>
          </div>
          <div class="counter-controls">
            <button @click="decrement" class="counter-btn minus">-</button>
            <button @click="increment" class="counter-btn plus">+</button>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'App',
  setup() {
    const title = ref('Welcome to the Future')
    const subtitle = ref('Experience cutting-edge design with vibrant colors and smooth animations')
    const isActive = ref(false)
    const counter = ref(0)
    
    const features = ref([
      {
        icon: '🚀',
        title: 'Lightning Fast',
        description: 'Built with Vue 3 for optimal performance'
      },
      {
        icon: '🎨',
        title: 'Beautiful Design',
        description: 'Modern aesthetics with vibrant gradients'
      },
      {
        icon: '📱',
        title: 'Responsive',
        description: 'Perfect on every device and screen size'
      },
      {
        icon: '⚡',
        title: 'Interactive',
        description: 'Engaging animations and smooth transitions'
      }
    ])

    const buttonText = computed(() => {
      return isActive.value ? 'Night Mode' : 'Bright Mode'
    })

    const toggleMode = () => {
      isActive.value = !isActive.value
      document.body.classList.toggle('dark-mode')
    }

    const increment = () => {
      counter.value++
    }

    const decrement = () => {
      if (counter.value > 0) counter.value--
    }

    const onCardHover = (index) => {
      console.log(`Hovering card ${index}`)
    }

    const onCardLeave = (index) => {
      console.log(`Left card ${index}`)
    }

    onMounted(() => {
      // Add entrance animations
      const cards = document.querySelectorAll('.feature-card')
      cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.2}s`
      })
    })

    return {
      title,
      subtitle,
      isActive,
      counter,
      features,
      buttonText,
      toggleMode,
      increment,
      decrement,
      onCardHover,
      onCardLeave
    }
  }
}
</script>

<style scoped>
/* Import global animations */
@import url('./style.css');

.app-container {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.animated-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  opacity: 0.6;
  animation: float 8s ease-in-out infinite;
}

.orb-1 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, #ff6b6b, #ee5a24);
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.orb-2 {
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, #4ecdc4, #44a08d);
  top: 50%;
  right: 10%;
  animation-delay: 2s;
}

.orb-3 {
  width: 250px;
  height: 250px;
  background: radial-gradient(circle, #ffa726, #fb8c00);
  bottom: 10%;
  left: 50%;
  animation-delay: 4s;
}

.content-wrapper {
  position: relative;
  z-index: 2;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  text-align: center;
  padding: 4rem 0;
}

.hero-title {
  font-size: clamp(3rem, 8vw, 5rem);
  font-weight: 700;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.gradient-text {
  background: linear-gradient(135deg, #ff6b6b, #ffa726, #4ecdc4, #667eea);
  background-size: 400% 400%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradient-shift 3s ease infinite;
}

.hero-subtitle {
  font-size: 1.3rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 3rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.cta-button {
  padding: 1.2rem 3rem;
  border: none;
  border-radius: 50px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  color: white;
  font-size: 1.2rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.cta-button:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 15px 35px rgba(255, 107, 107, 0.4);
}

.cta-button.active {
  background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
}

.button-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin: 4rem 0;
}

.feature-card {
  padding: 2rem;
  border-radius: 20px;
  backdrop-filter: blur(20px);
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
  transition: all 0.3s ease;
  animation: slide-up 0.8s ease forwards;
  opacity: 0;
  transform: translateY(30px);
}

.feature-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: white;
  margin-bottom: 1rem;
}

.card-description {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
}

.card-accent {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 4px;
  border-radius: 0 0 20px 20px;
}

.accent-1 { background: linear-gradient(90deg, #ff6b6b, #ee5a24); }
.accent-2 { background: linear-gradient(90deg, #4ecdc4, #44a08d); }
.accent-3 { background: linear-gradient(90deg, #ffa726, #fb8c00); }
.accent-4 { background: linear-gradient(90deg, #667eea, #764ba2); }

.interactive-section {
  display: flex;
  justify-content: center;
  margin: 4rem 0;
}

.counter-container {
  padding: 3rem;
  border-radius: 20px;
  text-align: center;
  backdrop-filter: blur(20px);
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.counter-container h3 {
  color: white;
  font-size: 1.5rem;
  margin-bottom: 2rem;
}

.counter-display {
  margin: 2rem 0;
}

.counter-number {
  font-size: 4rem;
  font-weight: 700;
}

.counter-controls {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.counter-btn {
  width: 60px;
  height: 60px;
  border: none;
  border-radius: 50%;
  font-size: 2rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
}

.counter-btn.plus {
  background: linear-gradient(135deg, #4ecdc4, #44a08d);
}

.counter-btn.minus {
  background: linear-gradient(135deg, #ff6b6b, #ee5a24);
}

.counter-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

/* Animations */
@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  33% { transform: translateY(-30px) rotate(5deg); }
  66% { transform: translateY(-20px) rotate(-5deg); }
}

@keyframes gradient-shift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

@keyframes slide-up {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .content-wrapper {
    padding: 1rem;
  }
  
  .hero-section {
    padding: 2rem 0;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .counter-container {
    padding: 2rem;
  }
}
</style>"""

        all_generated_files['main.js'] = """const { createApp } = Vue

createApp({
  data() {
    return {
      title: 'Welcome to the Future',
      subtitle: 'Experience cutting-edge design with vibrant colors and smooth animations',
      isActive: false,
      counter: 0,
      features: [
        {
          icon: '🚀',
          title: 'Lightning Fast',
          description: 'Built with Vue 3 for optimal performance'
        },
        {
          icon: '🎨',
          title: 'Beautiful Design',
          description: 'Modern aesthetics with vibrant gradients'
        },
        {
          icon: '📱',
          title: 'Responsive',
          description: 'Perfect on every device and screen size'
        },
        {
          icon: '⚡',
          title: 'Interactive',
          description: 'Engaging animations and smooth transitions'
        }
      ]
    }
  },
  computed: {
    buttonText() {
      return this.isActive ? 'Night Mode' : 'Bright Mode'
    }
  },
  methods: {
    toggleMode() {
      this.isActive = !this.isActive
      document.body.classList.toggle('dark-mode')
    },
    increment() {
      this.counter++
    },
    decrement() {
      if (this.counter > 0) this.counter--
    },
    onCardHover(index) {
      console.log(`Hovering card ${index}`)
    },
    onCardLeave(index) {
      console.log(`Left card ${index}`)
    }
  },
  mounted() {
    // Add entrance animations
    const cards = document.querySelectorAll('.feature-card')
    cards.forEach((card, index) => {
      card.style.animationDelay = `${index * 0.2}s`
    })
  }
}).mount('#app')"""

    elif 'script.js' in all_generated_files and len(all_generated_files['script.js']) < 200:
        print("Debug: script.js too short, using enhanced fallback")
        all_generated_files['script.js'] = """// Enhanced interactivity and modern features for the website
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize modern interaction features
    initializeAnimations();
    initializeFormHandling();
    initializeNavigation();
    initializeModals();
    initializeAccessibility();
    initializeMobileFeatures();
    
    // Modern animations with intersection observer
    function initializeAnimations() {
        const animatedElements = document.querySelectorAll('.animate-on-scroll, .card, .product-item, .service-item, .feature, .hero');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        });
        
        animatedElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        });
        
        // Enhanced button hover effects
        const buttons = document.querySelectorAll('button, .btn, .cta-button, .submit-btn');
        buttons.forEach(btn => {
            btn.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-3px) scale(1.02)';
                this.style.boxShadow = '0 10px 30px rgba(0,0,0,0.2)';
            });
            btn.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
                this.style.boxShadow = '0 4px 15px rgba(0,0,0,0.1)';
            });
        });
    }
}"""
    
    if not all_generated_files:
        return {"error": "Could not generate any files. Please try again."}

    # Write all generated files
    try:
        # Ensure the output directory exists - handle both relative and absolute paths
        output_dir = "../output"
        if not os.path.exists(output_dir):
            # Try relative to current working directory
            output_dir = "output"
        if not os.path.exists(output_dir):
            # Create the directory
            os.makedirs(output_dir, exist_ok=True)
        
        created_files = []
        for filename, content in all_generated_files.items():
            file_path = os.path.join(output_dir, filename)
            print(f"Debug: Writing file to {file_path}")
            with open(file_path, "w", encoding='utf-8') as f:
                f.write(content)
            created_files.append(filename)
            print(f"Debug: Successfully wrote {filename} ({len(content)} chars)")
        
        return {"files": created_files}
    except Exception as e:
        print(f"Debug: Error writing files: {str(e)}")
        return {"error": f"Failed to write files: {str(e)}"}

def parse_gemini_response(response_text):
    """
    Parses the Gemini API response to extract file names and their content.
    Enhanced for Vue.js and modern web development files.
    """
    files = {}
    
    # Enhanced pattern to match various filename formats including Vue.js files
    patterns = [
        # **filename.ext:** or **filename.ext**:
        re.compile(r"\*\*([\w.-]+)\*\*:?\s*\n+```(?:\w+)?\n(.*?)\n```", re.DOTALL),
        # **filename.ext**
        re.compile(r"\*\*([\w.-]+)\*\*\s*\n+```(?:\w+)?\n(.*?)\n```", re.DOTALL),
        # ### filename.ext or ## filename.ext
        re.compile(r"#{2,3}\s*([\w.-]+)\s*\n+```(?:\w+)?\n(.*?)\n```", re.DOTALL),
        # filename.ext: (without asterisks)
        re.compile(r"^([\w.-]+):\s*\n+```(?:\w+)?\n(.*?)\n```", re.DOTALL | re.MULTILINE),
    ]
    
    for pattern in patterns:
        matches = pattern.findall(response_text)
        if matches:
            for filename, content in matches:
                if filename and content.strip():
                    files[filename.strip()] = content.strip()
            break
    
    # If still no files found, try a more flexible approach
    if not files:
        # Look for common file extensions in the text
        sections = re.split(r'\n(?=\*\*|\#\#|\w+\.(?:html|css|js|py|sql))', response_text)
        for section in sections:
            # Extract filename from start of section
            filename_match = re.search(r'([\w.-]+\.(?:html|css|js|py|sql|env))', section[:50])
            if filename_match:
                filename = filename_match.group(1)
                # Extract code from code blocks
                code_match = re.search(r'```(?:\w+)?\n(.*?)\n```', section, re.DOTALL)
                if code_match:
                    files[filename] = code_match.group(1).strip()

    # Fallback for cases where the filename is not explicitly marked
    if not files:
        print("Debug: No files found with patterns, trying content-based detection")
        # Find all code blocks
        code_blocks = re.findall(r"```(?:\w+)?\n([\s\S]*?)\n```", response_text)
        print(f"Debug: Found {len(code_blocks)} code blocks")
        
        if len(code_blocks) >= 1:
            # Try to infer filenames based on content for Vue.js and modern web apps
            for i, content in enumerate(code_blocks):
                content = content.strip()
                if "<!DOCTYPE html>" in content or "<html>" in content:
                    files["index.html"] = content
                elif "<template>" in content and "<script>" in content and content.count("<") > 5:
                    files["App.vue"] = content
                elif "createApp" in content or "import { createApp }" in content:
                    files["main.js"] = content
                elif re.search(r"body\s*{", content) or re.search(r"[.#]\w+\s*{", content):
                    files["style.css"] = content
                elif "from flask import" in content or "app = Flask" in content:
                    files["app.py"] = content
                elif "CREATE TABLE" in content.upper() or "INSERT INTO" in content.upper():
                    files["schema.sql"] = content
                elif "import pymysql" in content or "def get_connection" in content:
                    files["database.py"] = content
                elif ("function" in content or "const" in content or "var" in content) and "flask" not in content.lower() and "createApp" not in content:
                    files["script.js"] = content
                elif content.startswith("#") or ("=" in content and not content.startswith("<")):
                    files[".env.example"] = content
                else:
                    # Generic filename if we can't determine
                    files[f"file_{i+1}.txt"] = content
    
    print(f"Debug: Final parsed files: {list(files.keys())}")
    return files


if __name__ == "__main__":
    # This block is for testing purposes only
    # To run, use the server.py file
    pass


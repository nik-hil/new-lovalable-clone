
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
    
    # Check for essential frontend files
    has_html = any('html' in filename.lower() for filename in files.keys())
    has_css = any('css' in filename.lower() for filename in files.keys())
    
    if not has_html:
        missing_files.append('HTML file')
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

Generate practical, working JavaScript code that enhances the user experience.

Format your response as:
**script.js:**
```javascript
[Complete functional JavaScript code here - minimum 50 lines]
```
"""
                response = model.generate_content(js_prompt)
                files = parse_gemini_response(response.text)
                if 'script.js' in files and len(files['script.js']) > 100:  # Ensure substantial content
                    generated_files['script.js'] = files['script.js']
                    print(f"Debug: Generated script.js ({len(files['script.js'])} chars)")
                else:
                    # Fallback: create a basic interactive script
                    generated_files['script.js'] = """// Enhanced interactivity for the website
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Form handling
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show loading state
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Processing...';
            submitBtn.disabled = true;
            
            // Simulate form submission
            setTimeout(() => {
                alert('Thank you! Your request has been submitted.');
                form.reset();
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }, 1500);
        });
    });

    // Add hover animations
    const buttons = document.querySelectorAll('button, .btn');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Image lazy loading and modal
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('click', function() {
            if (this.dataset.modal !== 'false') {
                showImageModal(this.src, this.alt);
            }
        });
    });

    function showImageModal(src, alt) {
        const modal = document.createElement('div');
        modal.className = 'image-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <span class="close">&times;</span>
                <img src="${src}" alt="${alt}">
            </div>
        `;
        
        document.body.appendChild(modal);
        
        modal.querySelector('.close').addEventListener('click', () => {
            document.body.removeChild(modal);
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                document.body.removeChild(modal);
            }
        });
    }
});"""
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
Create a stunning, modern, visually appealing website for: {prompt}

🎨 DESIGN REQUIREMENTS - MAKE IT BEAUTIFUL:
- Use vibrant, attractive color schemes that match the theme
- Add gradients, shadows, and modern visual effects
- Implement smooth animations and hover effects
- Use modern typography with proper font pairings
- Create visual hierarchy with proper spacing
- Add background patterns, images, or subtle textures
- Ensure the design is eye-catching and professional

Generate these core files:
- **index.html** - Complete HTML with rich content and proper structure
- **style.css** - Beautiful, modern styling with animations and visual effects
- **script.js** - Interactive features and smooth user experience

For the CSS, include:
- Modern color palettes (gradients, vibrant colors)
- Box shadows and border radius for depth
- Smooth transitions and hover effects
- Flexbox/Grid layouts for responsiveness
- Custom animations and keyframes
- Modern button designs with hover states
- Beautiful typography and spacing

Make it look like a premium, professional website that users would love to visit!

Format your response as:
**index.html:**
```html
[HTML code here]
```

**style.css:**
```css
[CSS code here with beautiful, modern styling]
```

**script.js:** (if needed)
```javascript
[JavaScript code here]
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
    
    # Final validation
    is_valid, missing_files = validate_generated_files(all_generated_files, requires_backend)
    
    if not is_valid and requires_backend:
        print(f"Debug: Still missing files after all iterations: {missing_files}")
        # Continue anyway with a warning
    
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
    This version is more robust to variations in filename markers.
    """
    files = {}
    
    # Enhanced pattern to match various filename formats
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
            # Try to infer filenames based on content
            for i, content in enumerate(code_blocks):
                content = content.strip()
                if "<!DOCTYPE html>" in content or "<html>" in content:
                    files["index.html"] = content
                elif re.search(r"body\s*{", content) or re.search(r"[.#]\w+\s*{", content):
                    files["style.css"] = content
                elif "from flask import" in content or "app = Flask" in content:
                    files["app.py"] = content
                elif "CREATE TABLE" in content.upper() or "INSERT INTO" in content.upper():
                    files["schema.sql"] = content
                elif "import pymysql" in content or "def get_connection" in content:
                    files["database.py"] = content
                elif ("function" in content or "const" in content or "var" in content) and "flask" not in content.lower():
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


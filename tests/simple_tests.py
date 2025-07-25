#!/usr/bin/env python3
"""
Simple test runner without pytest dependency or Gemini API
"""
import sys
import os

# Define the functions locally to avoid importing Gemini dependencies
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

def test_backend_detection():
    """Test the backend detection logic"""
    print("Testing backend detection...")
    
    # Should require backend
    test_cases = [
        ("flower shop with orders", True),
        ("e-commerce site with cart", True),
        ("blog with user comments", True),
        ("booking system for appointments", True),
        ("user registration system", True),
        ("simple landing page", False),
        ("static portfolio website", False),
        ("informational brochure site", False),
        ("company about page", False)
    ]
    
    for prompt, expected in test_cases:
        result = is_data_driven_request(prompt)
        print(f"  '{prompt}' -> {result} (expected {expected})")
        if result != expected:
            raise AssertionError(f"Backend detection failed for '{prompt}': got {result}, expected {expected}")
    
    print("✅ Backend detection tests passed!")

def test_file_validation():
    """Test the file validation logic"""
    print("Testing file validation...")
    
    # Test frontend-only validation
    frontend_files = {
        "index.html": "<!DOCTYPE html><html></html>",
        "style.css": "body { margin: 0; }"
    }
    is_valid, missing = validate_generated_files(frontend_files, False)
    assert is_valid == True
    assert len(missing) == 0
    
    # Test missing frontend files
    incomplete_files = {
        "style.css": "body { margin: 0; }"
    }
    is_valid, missing = validate_generated_files(incomplete_files, False)
    assert is_valid == False
    assert "HTML file" in missing
    
    # Test backend validation
    backend_files = {
        "index.html": "<!DOCTYPE html><html></html>",
        "style.css": "body { margin: 0; }",
        "app.py": "from flask import Flask\napp = Flask(__name__)",
        "database.py": "import pymysql",
        "schema.sql": "CREATE TABLE users (id INT);"
    }
    is_valid, missing = validate_generated_files(backend_files, True)
    assert is_valid == True
    assert len(missing) == 0
    
    # Test missing backend files
    incomplete_backend = {
        "index.html": "<!DOCTYPE html><html></html>",
        "style.css": "body { margin: 0; }"
    }
    is_valid, missing = validate_generated_files(incomplete_backend, True)
    assert is_valid == False
    assert any("Flask backend" in m for m in missing)
    assert any("Database files" in m for m in missing)
    
    print("✅ File validation tests passed!")

if __name__ == "__main__":
    try:
        test_backend_detection()
        test_file_validation()
        print("\n🎉 All tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

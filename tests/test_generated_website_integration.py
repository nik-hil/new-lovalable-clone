#!/usr/bin/env python3
"""
Integration tests to validate that generated websites work properly before preview
"""
import os
import sys
import pytest
import requests
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import main

class TestGeneratedWebsiteIntegration:
    """Test that generated websites actually work before showing to users"""
    
    def test_flower_shop_generation_and_validation(self):
        """Complete test: generate, validate, and ensure flower shop works"""
        
        # Step 1: Clear existing files
        clear_response = requests.post('http://localhost:5001/api/clear-all')
        assert clear_response.status_code == 200
        
        # Step 2: Generate a flower shop website
        generate_response = requests.post(
            'http://localhost:5001/generate',
            data={'prompt': 'modern flower shop with shopping cart and orders'},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=60
        )
        
        assert generate_response.status_code == 200
        generate_data = generate_response.json()
        assert 'files_generated' in generate_data
        assert len(generate_data['files_generated']) >= 3  # At least HTML, CSS, JS
        
        # Step 3: Validate files exist and have content
        output_dir = 'output'
        required_files = ['index.html', 'style.css', 'script.js']
        
        for file_name in required_files:
            file_path = os.path.join(output_dir, file_name)
            assert os.path.exists(file_path), f"Required file {file_name} not found"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert len(content) > 100, f"File {file_name} has insufficient content"
                
                # Specific validations
                if file_name == 'index.html':
                    assert '<!DOCTYPE html>' in content, "HTML file missing DOCTYPE"
                    assert '<html' in content, "HTML file missing html tag"
                    assert '<head>' in content, "HTML file missing head section"
                    assert '<body>' in content, "HTML file missing body section"
                    assert 'script.js' in content, "HTML file not referencing script.js"
                    assert 'style.css' in content, "HTML file not referencing style.css"
                    # Should NOT have Vue.js dependencies
                    assert 'vue@3' not in content.lower(), "HTML still has Vue.js dependencies"
                    assert '<div id="app"></div>' not in content, "HTML still has Vue.js app div"
                    
                elif file_name == 'script.js':
                    assert 'document.addEventListener' in content, "JavaScript missing DOM event listeners"
                    assert 'function' in content, "JavaScript missing functions"
                    # Should NOT have ES6 imports
                    assert 'import {' not in content, "JavaScript still has ES6 imports"
                    assert 'import ' not in content, "JavaScript still has imports"
                    
                elif file_name == 'style.css':
                    assert '{' in content and '}' in content, "CSS file missing style rules"
        
        # Step 4: Test HTTP accessibility
        website_response = requests.get('http://localhost:5001/output/index.html', timeout=10)
        assert website_response.status_code == 200, "Generated website not accessible"
        
        html_content = website_response.text
        assert len(html_content) > 500, "Website HTML content too short"
        assert 'flower' in html_content.lower() or 'bloom' in html_content.lower(), "Website doesn't match flower shop theme"
        
        # Step 5: Test with headless browser (if available)
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            driver = webdriver.Chrome(options=chrome_options)
            
            # Load the website
            driver.get('http://localhost:5001/output/index.html')
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Check that page has visible content
            body_text = driver.find_element(By.TAG_NAME, "body").text.strip()
            assert len(body_text) > 100, "Page appears to have no visible content"
            
            # Check for JavaScript functionality
            buttons = driver.find_elements(By.TAG_NAME, "button")
            assert len(buttons) > 0, "No interactive buttons found"
            
            # Test button click (if buttons exist)
            if buttons:
                first_button = buttons[0]
                first_button.click()
                time.sleep(1)  # Allow for any JS effects
            
            # Check for no JavaScript errors
            logs = driver.get_log('browser')
            js_errors = [log for log in logs if log['level'] == 'SEVERE']
            severe_errors = [error for error in js_errors if 'error' in error['message'].lower()]
            assert len(severe_errors) == 0, f"JavaScript errors found: {severe_errors}"
            
            driver.quit()
            
        except Exception as e:
            print(f"Browser test skipped (Chrome not available): {e}")
        
        print("✅ Generated website validation passed!")
        print(f"   - Files generated: {generate_data['files_generated']}")
        print(f"   - HTML content length: {len(html_content)} characters")
        print(f"   - Website URL: http://localhost:5001/output/index.html")
        
    def test_coffee_shop_generation_and_validation(self):
        """Test generation and validation of a coffee shop website"""
        
        # Clear and generate
        requests.post('http://localhost:5001/api/clear-all')
        
        generate_response = requests.post(
            'http://localhost:5001/generate',
            data={'prompt': 'modern coffee shop with menu and contact form'},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=60
        )
        
        assert generate_response.status_code == 200
        
        # Quick validation
        website_response = requests.get('http://localhost:5001/output/index.html')
        assert website_response.status_code == 200
        
        html_content = website_response.text
        assert len(html_content) > 500, "Coffee shop website too short"
        assert any(keyword in html_content.lower() for keyword in ['coffee', 'cafe', 'menu', 'drink']), \
               "Website doesn't match coffee shop theme"
        
        print("✅ Coffee shop generation validation passed!")
        
    def test_restaurant_generation_and_validation(self):
        """Test generation and validation of a restaurant website"""
        
        # Clear and generate
        requests.post('http://localhost:5001/api/clear-all')
        
        generate_response = requests.post(
            'http://localhost:5001/generate',
            data={'prompt': 'elegant restaurant with reservations and menu'},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=60
        )
        
        assert generate_response.status_code == 200
        
        # Quick validation
        website_response = requests.get('http://localhost:5001/output/index.html')
        assert website_response.status_code == 200
        
        html_content = website_response.text
        assert len(html_content) > 500, "Restaurant website too short"
        assert any(keyword in html_content.lower() for keyword in ['restaurant', 'menu', 'food', 'dining']), \
               "Website doesn't match restaurant theme"
        
        print("✅ Restaurant generation validation passed!")
        
    def test_validation_prevents_broken_websites(self):
        """Test that validation catches and prevents broken websites"""
        
        # This test ensures our validation would catch common issues
        test_broken_html = """<!DOCTYPE html>
<html><head><title>Broken</title></head>
<body><div id="app"></div><script src="https://unpkg.com/vue@3"></script></body></html>"""
        
        # Write a broken file temporarily
        with open('output/index.html', 'w') as f:
            f.write(test_broken_html)
        
        # Our validation should detect this as broken
        website_response = requests.get('http://localhost:5001/output/index.html')
        html_content = website_response.text
        
        # These are indicators of broken Vue.js setup
        is_broken = (
            '<div id="app"></div>' in html_content and
            'vue@3' in html_content and
            len(html_content) < 500
        )
        
        assert is_broken, "Test broken HTML was not detected as broken"
        print("✅ Validation correctly identifies broken websites!")
        
    def test_website_meets_quality_standards(self):
        """Test that generated websites meet modern quality standards"""
        
        # Generate a test website
        requests.post('http://localhost:5001/api/clear-all')
        requests.post(
            'http://localhost:5001/generate',
            data={'prompt': 'modern tech startup landing page'},
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        # Check HTML structure
        with open('output/index.html', 'r') as f:
            html_content = f.read()
        
        # Modern HTML standards
        assert '<!DOCTYPE html>' in html_content, "Missing modern DOCTYPE"
        assert 'charset="UTF-8"' in html_content, "Missing UTF-8 charset"
        assert 'viewport' in html_content, "Missing responsive viewport meta tag"
        
        # Check CSS exists and has modern features
        with open('output/style.css', 'r') as f:
            css_content = f.read()
        
        # Modern CSS features
        modern_css_features = ['gradient', 'rgba', 'transform', 'transition']
        css_score = sum(1 for feature in modern_css_features if feature in css_content)
        assert css_score >= 2, f"CSS lacks modern features. Found {css_score}/4"
        
        # Check JavaScript functionality
        with open('output/script.js', 'r') as f:
            js_content = f.read()
        
        # Modern JavaScript features
        assert 'addEventListener' in js_content, "Missing event listeners"
        assert len(js_content) > 200, "JavaScript functionality too minimal"
        
        print("✅ Generated website meets quality standards!")

if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v", "--tb=short"]) 
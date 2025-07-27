#!/usr/bin/env python3
"""
Website validation tests to ensure generated sites actually work
"""
import os
import sys
import pytest
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import subprocess
import signal

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestWebsiteValidation:
    """Test that generated websites actually work and display content"""
    
    @pytest.fixture(scope="class")
    def chrome_driver(self):
        """Set up Chrome driver for testing"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            yield driver
            driver.quit()
        except Exception as e:
            pytest.skip(f"Chrome driver not available: {e}")
    
    @pytest.fixture
    def test_server_process(self):
        """Start a simple HTTP server for testing generated websites"""
        output_dir = os.path.abspath('output')
        if not os.path.exists(output_dir):
            pytest.skip("No output directory found")
        
        # Start HTTP server in output directory
        process = subprocess.Popen([
            'python3', '-m', 'http.server', '8000'
        ], cwd=output_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(2)
        
        yield process
        
        # Clean up
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

    def test_generate_and_validate_website(self, chrome_driver, test_server_process):
        """Generate a website and validate it works properly"""
        
        # First, generate a website
        generate_response = requests.post(
            'http://localhost:5001/generate',
            data={'prompt': 'modern coffee shop website with menu and contact form'},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=30
        )
        
        assert generate_response.status_code == 200
        generate_data = generate_response.json()
        assert 'files_generated' in generate_data
        assert len(generate_data['files_generated']) >= 3  # At least HTML, CSS, JS
        
        # Wait a moment for files to be written
        time.sleep(1)
        
        # Test the generated website
        try:
            chrome_driver.get('http://localhost:8000')
            
            # Wait for page to load
            WebDriverWait(chrome_driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Check that page has content (not blank)
            body_text = chrome_driver.find_element(By.TAG_NAME, "body").text.strip()
            assert len(body_text) > 50, "Page appears to be mostly empty"
            
            # Check that CSS is loaded (page should have styling)
            body_element = chrome_driver.find_element(By.TAG_NAME, "body")
            computed_styles = chrome_driver.execute_script(
                "return window.getComputedStyle(arguments[0]);", body_element
            )
            
            # Basic checks for styling
            background_color = computed_styles.get('background-color', 'rgba(0, 0, 0, 0)')
            assert background_color != 'rgba(0, 0, 0, 0)', "No background styling detected"
            
            # Check that JavaScript is working (look for interactive elements)
            buttons = chrome_driver.find_elements(By.TAG_NAME, "button")
            if buttons:
                # Test button interaction
                button = buttons[0]
                button.click()
                time.sleep(1)  # Allow for any JS effects
            
            # Check for modern CSS features
            elements_with_gradients = chrome_driver.execute_script("""
                const elements = document.querySelectorAll('*');
                let gradientCount = 0;
                elements.forEach(el => {
                    const style = window.getComputedStyle(el);
                    if (style.background.includes('gradient') || 
                        style.backgroundImage.includes('gradient')) {
                        gradientCount++;
                    }
                });
                return gradientCount;
            """)
            
            assert elements_with_gradients > 0, "No gradient styling detected (not modern enough)"
            
            print(f"✅ Website validation passed!")
            print(f"   - Page content length: {len(body_text)} characters")
            print(f"   - Has styling: {background_color}")
            print(f"   - Gradient elements: {elements_with_gradients}")
            print(f"   - Interactive buttons: {len(buttons)}")
            
        except TimeoutException:
            pytest.fail("Website failed to load within timeout period")

    def test_website_responsive_design(self, chrome_driver, test_server_process):
        """Test that generated website is responsive"""
        try:
            chrome_driver.get('http://localhost:8000')
            
            # Test desktop viewport
            chrome_driver.set_window_size(1920, 1080)
            time.sleep(1)
            
            desktop_width = chrome_driver.execute_script("return document.body.scrollWidth;")
            
            # Test mobile viewport
            chrome_driver.set_window_size(375, 667)
            time.sleep(1)
            
            mobile_width = chrome_driver.execute_script("return document.body.scrollWidth;")
            
            # Website should adapt to different screen sizes
            assert mobile_width <= 400, f"Website not responsive - mobile width: {mobile_width}px"
            assert desktop_width >= 375, f"Website too narrow on desktop - width: {desktop_width}px"
            
            print(f"✅ Responsive design test passed!")
            print(f"   - Desktop width: {desktop_width}px")
            print(f"   - Mobile width: {mobile_width}px")
            
        except Exception as e:
            pytest.fail(f"Responsive design test failed: {e}")

    def test_website_accessibility_basics(self, chrome_driver, test_server_process):
        """Test basic accessibility features"""
        try:
            chrome_driver.get('http://localhost:8000')
            
            # Check for alt text on images
            images = chrome_driver.find_elements(By.TAG_NAME, "img")
            images_with_alt = [img for img in images if img.get_attribute("alt")]
            
            if images:
                alt_percentage = len(images_with_alt) / len(images) * 100
                assert alt_percentage >= 50, f"Only {alt_percentage:.1f}% of images have alt text"
            
            # Check for proper heading structure
            headings = chrome_driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6")
            assert len(headings) > 0, "No heading elements found"
            
            # Check for semantic HTML elements
            semantic_elements = chrome_driver.find_elements(By.CSS_SELECTOR, 
                "header, nav, main, section, article, aside, footer")
            assert len(semantic_elements) > 0, "No semantic HTML5 elements found"
            
            print(f"✅ Basic accessibility test passed!")
            print(f"   - Images with alt text: {len(images_with_alt)}/{len(images)}")
            print(f"   - Heading elements: {len(headings)}")
            print(f"   - Semantic elements: {len(semantic_elements)}")
            
        except Exception as e:
            pytest.fail(f"Accessibility test failed: {e}")

    def test_website_performance_basics(self, chrome_driver, test_server_process):
        """Test basic performance metrics"""
        try:
            start_time = time.time()
            chrome_driver.get('http://localhost:8000')
            
            # Wait for page to fully load
            WebDriverWait(chrome_driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            load_time = time.time() - start_time
            
            # Check load time (should be reasonable for local serving)
            assert load_time < 5.0, f"Page took too long to load: {load_time:.2f}s"
            
            # Check that CSS and JS files are loaded
            css_files = chrome_driver.execute_script("""
                return Array.from(document.styleSheets).length;
            """)
            
            js_files = chrome_driver.execute_script("""
                return Array.from(document.scripts).length;
            """)
            
            assert css_files > 0, "No CSS files loaded"
            assert js_files > 0, "No JavaScript files loaded"
            
            print(f"✅ Performance test passed!")
            print(f"   - Load time: {load_time:.2f}s")
            print(f"   - CSS files: {css_files}")
            print(f"   - JS files: {js_files}")
            
        except Exception as e:
            pytest.fail(f"Performance test failed: {e}")

    def test_javascript_functionality(self, chrome_driver, test_server_process):
        """Test that JavaScript functionality works"""
        try:
            chrome_driver.get('http://localhost:8000')
            
            # Check for JavaScript errors
            logs = chrome_driver.get_log('browser')
            js_errors = [log for log in logs if log['level'] == 'SEVERE']
            
            # Allow minor warnings but no severe errors
            severe_errors = [error for error in js_errors if 'error' in error['message'].lower()]
            assert len(severe_errors) == 0, f"JavaScript errors found: {severe_errors}"
            
            # Test if JavaScript functions are available
            js_functions_available = chrome_driver.execute_script("""
                return typeof window.showNotification === 'function' ||
                       typeof window.incrementCounter === 'function' ||
                       document.querySelectorAll('[onclick]').length > 0;
            """)
            
            assert js_functions_available, "No JavaScript interactivity detected"
            
            # Test event listeners
            elements_with_events = chrome_driver.execute_script("""
                const elements = document.querySelectorAll('*');
                let eventCount = 0;
                elements.forEach(el => {
                    if (el.onclick || el.onmouseenter || el.onmouseleave) {
                        eventCount++;
                    }
                });
                return eventCount;
            """)
            
            assert elements_with_events > 0, "No interactive elements with event handlers found"
            
            print(f"✅ JavaScript functionality test passed!")
            print(f"   - Severe JS errors: {len(severe_errors)}")
            print(f"   - Interactive elements: {elements_with_events}")
            
        except Exception as e:
            pytest.fail(f"JavaScript functionality test failed: {e}")

if __name__ == "__main__":
    # Run website validation tests directly
    pytest.main([__file__, "-v", "--tb=short"]) 
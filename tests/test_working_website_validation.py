#!/usr/bin/env python3
"""
Simple tests to validate that generated websites work properly (no browser automation)
"""
import os
import pytest
import requests
import json

class TestWorkingWebsiteValidation:
    """Test that generated websites actually work and have proper content"""
    
    def test_flower_shop_generation_works(self):
        """Test generating and validating a flower shop website"""
        
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
        
        print(f"✅ Generated {len(generate_data['files_generated'])} files: {generate_data['files_generated']}")
        
        # Step 3: Validate files exist and have content
        output_dir = 'output'
        required_files = ['index.html', 'style.css', 'script.js']
        
        for file_name in required_files:
            file_path = os.path.join(output_dir, file_name)
            assert os.path.exists(file_path), f"Required file {file_name} not found"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert len(content) > 100, f"File {file_name} has insufficient content ({len(content)} chars)"
                
                # Specific validations
                if file_name == 'index.html':
                    assert '<!DOCTYPE html>' in content, "HTML file missing DOCTYPE"
                    assert '<html' in content, "HTML file missing html tag"
                    assert '<head>' in content, "HTML file missing head section"
                    assert '<body>' in content, "HTML file missing body section"
                    assert 'script.js' in content, "HTML file not referencing script.js"
                    assert 'style.css' in content, "HTML file not referencing style.css"
                    
                    # Validate it's NOT broken Vue.js (should be vanilla HTML)
                    is_broken_vue = (
                        '<div id="app"></div>' in content and 
                        len([line for line in content.split('\n') if line.strip()]) < 20
                    )
                    assert not is_broken_vue, "HTML appears to be broken Vue.js template"
                    
                    # Should have actual content
                    content_indicators = ['flower', 'bloom', 'shop', 'cart', 'order', 'buy']
                    has_relevant_content = any(indicator in content.lower() for indicator in content_indicators)
                    assert has_relevant_content, "HTML doesn't contain flower shop related content"
                    
                elif file_name == 'script.js':
                    assert 'document.addEventListener' in content, "JavaScript missing DOM event listeners"
                    assert 'function' in content, "JavaScript missing functions"
                    
                    # Should NOT have broken ES6 imports
                    broken_imports = [
                        'import { createApp } from',
                        'import App from',
                        'import {' 
                    ]
                    has_broken_imports = any(imp in content for imp in broken_imports)
                    assert not has_broken_imports, "JavaScript still has broken framework imports"
                    
                elif file_name == 'style.css':
                    assert '{' in content and '}' in content, "CSS file missing style rules"
                    assert len(content) > 500, f"CSS file too minimal ({len(content)} chars)"
        
        # Step 4: Test HTTP accessibility
        website_response = requests.get('http://localhost:5001/output/index.html', timeout=10)
        assert website_response.status_code == 200, "Generated website not accessible"
        
        html_content = website_response.text
        assert len(html_content) > 1000, f"Website HTML content too short ({len(html_content)} chars)"
        
        # Verify it matches the flower shop theme
        theme_keywords = ['flower', 'bloom', 'petals', 'shop', 'cart', 'order']
        theme_matches = sum(1 for keyword in theme_keywords if keyword in html_content.lower())
        assert theme_matches >= 3, f"Website doesn't match flower shop theme (only {theme_matches} matches)"
        
        print(f"✅ Website validation passed!")
        print(f"   - HTML content: {len(html_content)} characters")
        print(f"   - Theme matches: {theme_matches}/6 keywords")
        print(f"   - Files validated: {required_files}")
        print(f"   - Preview URL: http://localhost:5001/output/index.html")
        
    def test_website_has_interactive_features(self):
        """Test that the website has proper interactive JavaScript"""
        
        # Check that script.js has substantial interactive content
        with open('output/script.js', 'r') as f:
            js_content = f.read()
        
        # Look for interactive features
        interactive_features = [
            'addEventListener',
            'onclick',
            'function',
            'const ',
            'let ',
            'getElementById',
            'querySelector'
        ]
        
        feature_count = sum(1 for feature in interactive_features if feature in js_content)
        assert feature_count >= 4, f"JavaScript lacks interactive features (found {feature_count}/7)"
        
        # Should be substantial (not minimal)
        assert len(js_content) > 1000, f"JavaScript too minimal ({len(js_content)} chars)"
        
        print(f"✅ Interactive features validation passed!")
        print(f"   - JavaScript size: {len(js_content)} characters")
        print(f"   - Interactive features: {feature_count}/7")
        
    def test_website_has_modern_styling(self):
        """Test that the CSS includes modern styling features"""
        
        with open('output/style.css', 'r') as f:
            css_content = f.read()
        
        # Look for modern CSS features
        modern_features = [
            'gradient',
            'rgba',
            'transform',
            'transition',
            'box-shadow',
            'border-radius',
            'flexbox',
            'grid'
        ]
        
        feature_count = sum(1 for feature in modern_features if feature in css_content.lower())
        assert feature_count >= 3, f"CSS lacks modern features (found {feature_count}/8)"
        
        # Should be substantial
        assert len(css_content) > 1000, f"CSS too minimal ({len(css_content)} chars)"
        
        print(f"✅ Modern styling validation passed!")
        print(f"   - CSS size: {len(css_content)} characters")  
        print(f"   - Modern features: {feature_count}/8")
        
    def test_no_broken_vue_artifacts(self):
        """Ensure there are no broken Vue.js artifacts that cause blank pages"""
        
        with open('output/index.html', 'r') as f:
            html_content = f.read()
        
        # Check for broken Vue.js patterns
        broken_patterns = [
            ('<div id="app"></div>', 'Empty Vue.js app div'),
            ('vue@3', 'Vue.js CDN reference'),
            ('import { createApp }', 'ES6 Vue.js imports'),
            ('main.js', 'Vue.js main.js reference')
        ]
        
        issues_found = []
        for pattern, description in broken_patterns:
            if pattern in html_content:
                # Only consider it broken if it's the minimal Vue.js template
                if pattern == '<div id="app"></div>' and len(html_content) < 1000:
                    issues_found.append(description)
                elif pattern != '<div id="app"></div>':
                    issues_found.append(description)
        
        assert len(issues_found) == 0, f"Found broken Vue.js artifacts: {issues_found}"
        
        print(f"✅ No broken Vue.js artifacts found!")
        
    def test_coffee_shop_theme_validation(self):
        """Test generating a different theme to ensure system works generally"""
        
        # Clear and generate coffee shop
        requests.post('http://localhost:5001/api/clear-all')
        
        generate_response = requests.post(
            'http://localhost:5001/generate',
            data={'prompt': 'modern coffee shop with menu'},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=60
        )
        
        assert generate_response.status_code == 200
        
        # Quick validation
        website_response = requests.get('http://localhost:5001/output/index.html')
        assert website_response.status_code == 200
        
        html_content = website_response.text
        assert len(html_content) > 1000, "Coffee shop website too short"
        
        # Check for coffee-related content
        coffee_keywords = ['coffee', 'cafe', 'menu', 'espresso', 'latte', 'drink']
        coffee_matches = sum(1 for keyword in coffee_keywords if keyword in html_content.lower())
        assert coffee_matches >= 2, f"Website doesn't match coffee shop theme (only {coffee_matches} matches)"
        
        print(f"✅ Coffee shop generation validation passed!")
        print(f"   - Theme matches: {coffee_matches}/6 keywords")

if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"]) 
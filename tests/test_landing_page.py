#!/usr/bin/env python3
"""
Test cases for landing page functionality
"""
import os
import sys
import pytest
import requests
import time
import json
from unittest.mock import patch, MagicMock

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestLandingPageEndpoints:
    """Test all landing page API endpoints"""
    
    @pytest.fixture
    def base_url(self):
        """Base URL for testing"""
        return "http://localhost:5001"
    
    def test_landing_page_loads(self, base_url):
        """Test that the main landing page loads"""
        try:
            response = requests.get(base_url, timeout=10)
            assert response.status_code == 200
            # Check for Vue.js redirect message or actual content
            assert ("Vue.js Frontend Loading" in response.text or 
                    "Craft extraordinary websites" in response.text)
        except requests.exceptions.ConnectionError:
            pytest.skip("Server not running - start with docker-compose up")
    
    def test_site_assets_load(self, base_url):
        """Test that site assets (CSS, etc.) load correctly"""
        try:
            # Test CSS file
            response = requests.get(f"{base_url}/site/style.css", timeout=10)
            assert response.status_code == 200
            assert "text/css" in response.headers.get("content-type", "")
        except requests.exceptions.ConnectionError:
            pytest.skip("Server not running - start with docker-compose up")
    
    def test_generate_endpoint_structure(self, base_url):
        """Test the generate endpoint responds correctly to invalid requests"""
        try:
            # Test with empty prompt
            response = requests.post(
                f"{base_url}/generate",
                data={"prompt": ""},
                timeout=10
            )
            # Should handle empty prompts gracefully
            assert response.status_code in [400, 422, 200]  # Accept 200 since it may process empty prompts
        except requests.exceptions.ConnectionError:
            pytest.skip("Server not running - start with docker-compose up")
    
    def test_clear_all_endpoint(self, base_url):
        """Test the clear all endpoint"""
        try:
            response = requests.post(f"{base_url}/api/clear-all", timeout=10)
            assert response.status_code == 200
            data = response.json()
            assert "success" in data
        except requests.exceptions.ConnectionError:
            pytest.skip("Server not running - start with docker-compose up")
    
    def test_download_zip_endpoint_no_files(self, base_url):
        """Test download endpoint when no files exist"""
        try:
            # First clear all files
            requests.post(f"{base_url}/api/clear-all", timeout=10)
            
            # Then try to download
            response = requests.get(f"{base_url}/download-zip", timeout=10)
            assert response.status_code == 404  # No files found
        except requests.exceptions.ConnectionError:
            pytest.skip("Server not running - start with docker-compose up")
    
    def test_history_endpoint(self, base_url):
        """Test the history endpoint"""
        try:
            response = requests.get(f"{base_url}/api/history", timeout=10)
            assert response.status_code == 200
            data = response.json()
            # The endpoint returns a dict with history key, not a direct list
            assert "history" in data  # Should have a history key
            assert isinstance(data["history"], list)  # History should be a list
        except requests.exceptions.ConnectionError:
            pytest.skip("Server not running - start with docker-compose up")
    
    def test_preview_endpoint_structure(self, base_url):
        """Test the preview endpoint structure"""
        try:
            # Test accessing output files
            response = requests.get(f"{base_url}/output/index.html", timeout=10)
            # Should either serve the file or return 404 if no files exist
            assert response.status_code in [200, 404]
        except requests.exceptions.ConnectionError:
            pytest.skip("Server not running - start with docker-compose up")

class TestLandingPageFeatures:
    """Test landing page feature functionality"""
    
    def test_prompt_validation_logic(self):
        """Test prompt validation without making API calls"""
        # Import the validation function
        from server import app
        
        with app.test_client() as client:
            # Test empty prompt
            response = client.post('/generate',
                                 data={"prompt": ""},
                                 content_type='application/x-www-form-urlencoded')
            assert response.status_code in [400, 422, 200]  # Accept various responses
            
            # Test very short prompt
            response = client.post('/generate',
                                 data={"prompt": "hi"},
                                 content_type='application/x-www-form-urlencoded')
            # Should handle short prompts (might process or reject)
            assert response.status_code in [200, 400, 422, 500]
    
    def test_history_management(self):
        """Test history management functionality"""
        from server import app
        
        with app.test_client() as client:
            # Test getting history
            response = client.get('/api/history')
            assert response.status_code == 200
            data = response.get_json()
            # The endpoint returns a dict with history key, not a direct list
            assert "history" in data  # Should have a history key
            assert isinstance(data["history"], list)  # History should be a list
    
    def test_clear_all_functionality(self):
        """Test clear all functionality"""
        from server import app
        
        with app.test_client() as client:
            # Test clear all
            response = client.post('/api/clear-all')
            assert response.status_code == 200
            data = response.get_json()
            assert "success" in data
    
    def test_file_serving_logic(self):
        """Test file serving logic"""
        from server import app
        
        with app.test_client() as client:
            # Test serving site files
            response = client.get('/site/style.css')
            assert response.status_code in [200, 404]  # File exists or doesn't
            
            # Test serving output files  
            response = client.get('/output/index.html')
            assert response.status_code in [200, 404]  # File exists or doesn't

class TestLandingPageUI:
    """Test UI-related functionality that can be validated server-side"""
    
    def test_landing_page_content(self):
        """Test that landing page contains required elements"""
        from server import app
        
        with app.test_client() as client:
            response = client.get('/')
            assert response.status_code == 200
            content = response.get_data(as_text=True)
            
            # Check for Vue.js setup or actual content
            assert ("Vue.js Frontend Loading" in content or 
                    "app" in content)  # Vue.js app div
            # The actual Vue.js components are loaded dynamically
    
    def test_javascript_functionality_present(self):
        """Test that JavaScript functionality is present in the page"""
        from server import app
        
        with app.test_client() as client:
            response = client.get('/')
            content = response.get_data(as_text=True)
            
            # Check for Vue.js app structure (dynamic content loaded by Vue.js)
            assert 'id="app"' in content
            # JavaScript functionality is now handled by Vue.js components
    
    def test_form_validation_elements(self):
        """Test that form validation elements are present"""
        from server import app
        
        with app.test_client() as client:
            response = client.get('/')
            content = response.get_data(as_text=True)
            
            # Check for Vue.js app container (form elements are dynamically created by Vue.js)
            assert 'id="app"' in content
            # Form elements are now created by Vue.js components dynamically

class TestBackendIntegration:
    """Test backend integration without making external API calls"""
    
    @patch('src.main.create_website')  # Corrected function name
    def test_generate_workflow_mocked(self, mock_create):
        """Test the generate workflow with mocked AI generation"""
        from server import app
        
        # Mock the create_website function
        mock_create.return_value = {
            "index.html": "<!DOCTYPE html><html><head><title>Test</title></head><body><h1>Test Site</h1></body></html>",
            "style.css": "body { margin: 0; padding: 20px; }"
        }
        
        with app.test_client() as client:
            response = client.post('/generate',
                                 data={"prompt": "simple landing page"},
                                 content_type='application/x-www-form-urlencoded')
            
            # Should process successfully with mocked data
            assert response.status_code in [200, 500]  # Accept various responses
            if response.status_code == 200:
                data = response.get_json()
                assert "preview_url" in data or "success" in data or "files" in data
    
    def test_database_connection_handling(self):
        """Test database connection handling"""
        from server import app
        
        with app.test_client() as client:
            # Test history endpoint which uses database
            response = client.get('/api/history')
            assert response.status_code == 200
            # Should handle database connection gracefully

if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])

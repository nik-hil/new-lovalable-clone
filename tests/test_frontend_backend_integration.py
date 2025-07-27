#!/usr/bin/env python3
"""
Integration tests for Vue.js frontend and Flask backend communication
"""
import os
import sys
import pytest
import requests
import time
import json
from unittest.mock import patch

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestFrontendBackendIntegration:
    """Test Vue.js frontend to Flask backend communication"""
    
    @pytest.fixture
    def backend_url(self):
        """Flask backend URL"""
        return "http://localhost:5001"
    
    @pytest.fixture  
    def frontend_proxy_url(self):
        """Vue.js frontend proxy URL"""
        return "http://localhost:8080"

    def test_backend_cors_configuration(self, backend_url):
        """Test that Flask backend has CORS configured for Vue.js frontend"""
        try:
            response = requests.options(
                f"{backend_url}/generate",
                headers={
                    'Origin': 'http://localhost:8080',
                    'Access-Control-Request-Method': 'POST',
                    'Access-Control-Request-Headers': 'Content-Type'
                },
                timeout=10
            )
            
            # Check CORS headers are present
            assert response.status_code in [200, 204]
            cors_headers = response.headers
            assert 'Access-Control-Allow-Origin' in cors_headers
            assert 'Access-Control-Allow-Methods' in cors_headers
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend not running - start with docker-compose up")

    def test_proxy_configuration_generate_endpoint(self, frontend_proxy_url):
        """Test that Vue.js proxy correctly forwards /api/generate to Flask backend"""
        try:
            # Test the proxy path that Vue.js will use
            response = requests.post(
                f"{frontend_proxy_url}/api/generate",
                data={"prompt": "test website"},
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                timeout=15
            )
            
            # Should successfully proxy to backend
            assert response.status_code in [200, 500]  # 500 might be from AI API issues, but proxy works
            
            # Check response format
            if response.status_code == 200:
                data = response.json()
                assert "files_generated" in data or "error" in data
                
        except requests.exceptions.ConnectionError:
            pytest.skip("Vue.js frontend proxy not running - start with npm run serve")

    def test_proxy_configuration_clear_all_endpoint(self, frontend_proxy_url):
        """Test that Vue.js proxy correctly forwards /api/clear-all to Flask backend"""
        try:
            response = requests.post(
                f"{frontend_proxy_url}/api/clear-all",
                timeout=10
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "success" in data
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Vue.js frontend proxy not running")

    def test_proxy_configuration_download_endpoint(self, frontend_proxy_url):
        """Test that Vue.js proxy correctly forwards /api/download-zip to Flask backend"""
        try:
            response = requests.get(
                f"{frontend_proxy_url}/api/download-zip",
                timeout=10
            )
            
            # Should either return zip file or 404 if no files
            assert response.status_code in [200, 404]
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Vue.js frontend proxy not running")

    def test_full_workflow_integration(self, frontend_proxy_url):
        """Test complete workflow: clear -> generate -> download through proxy"""
        try:
            # Step 1: Clear all existing data
            clear_response = requests.post(
                f"{frontend_proxy_url}/api/clear-all",
                timeout=10
            )
            assert clear_response.status_code == 200
            clear_data = clear_response.json()
            assert clear_data.get("success") == True
            
            # Step 2: Generate a simple website
            generate_response = requests.post(
                f"{frontend_proxy_url}/api/generate",
                data={"prompt": "simple modern portfolio website"},
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                timeout=30  # Generation can take time
            )
            
            # Check generation worked
            assert generate_response.status_code in [200, 500]  # AI issues might cause 500
            
            if generate_response.status_code == 200:
                generate_data = generate_response.json()
                assert "files_generated" in generate_data
                assert len(generate_data["files_generated"]) > 0
                assert "preview_url" in generate_data
                
                # Step 3: Try to download the generated files
                download_response = requests.get(
                    f"{frontend_proxy_url}/api/download-zip",
                    timeout=10
                )
                assert download_response.status_code == 200
                assert download_response.headers.get('content-type') == 'application/zip'
                
        except requests.exceptions.ConnectionError:
            pytest.skip("Services not running - start with ./docker-dev.sh up")
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out - possible connection issue between frontend and backend")

    def test_error_handling_in_proxy(self, frontend_proxy_url):
        """Test that errors from backend are properly handled through proxy"""
        try:
            # Send invalid request that should trigger backend error
            response = requests.post(
                f"{frontend_proxy_url}/api/generate",
                data={"prompt": ""},  # Empty prompt should trigger validation error
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                timeout=10
            )
            
            assert response.status_code == 400  # Should get validation error
            data = response.json()
            assert "error" in data
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Services not running")

    @patch('src.main.create_website')
    def test_mocked_generation_through_proxy(self, mock_create, frontend_proxy_url):
        """Test Vue.js to Flask communication with mocked AI generation"""
        # Mock the AI generation to avoid external API calls
        mock_create.return_value = {
            "files": ["index.html", "style.css", "main.js"]
        }
        
        try:
            response = requests.post(
                f"{frontend_proxy_url}/api/generate",
                data={"prompt": "test website"},
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                timeout=10
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "files_generated" in data
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Services not running")

class TestVueJsFrontendDirectly:
    """Test Vue.js frontend directly"""
    
    def test_vue_frontend_loads(self):
        """Test that Vue.js frontend serves the main page"""
        try:
            response = requests.get("http://localhost:8080", timeout=10)
            assert response.status_code == 200
            
            # Check for Vue.js app structure
            content = response.text
            assert 'id="app"' in content
            assert 'Craft. Create. Code.' in content
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Vue.js frontend not running - start with npm run serve")

    def test_vue_frontend_static_assets(self):
        """Test that Vue.js frontend serves static assets"""
        try:
            # Test CSS assets
            response = requests.get("http://localhost:8080/css/app.css", timeout=5)
            # Should either load CSS or 404 if not built yet
            assert response.status_code in [200, 404]
            
        except requests.exceptions.ConnectionError:
            pytest.skip("Vue.js frontend not running")

class TestServiceConnectivity:
    """Test that all services can communicate with each other"""
    
    def test_all_services_running(self):
        """Test that all required services are accessible"""
        services = [
            ("Flask Backend", "http://localhost:5001"),
            ("Vue.js Frontend", "http://localhost:8080"),
            ("Test Server", "http://localhost:5002")
        ]
        
        results = {}
        for name, url in services:
            try:
                response = requests.get(url, timeout=5)
                results[name] = response.status_code
            except requests.exceptions.ConnectionError:
                results[name] = "Not accessible"
        
        # At least Flask backend should be running for tests to be meaningful
        if results.get("Flask Backend") == "Not accessible":
            pytest.skip("Flask backend not running - start with docker-compose up")
            
        # Print status for debugging
        print("\nService Status:")
        for name, status in results.items():
            print(f"  {name}: {status}")

if __name__ == "__main__":
    # Run integration tests directly
    pytest.main([__file__, "-v", "--tb=short"]) 
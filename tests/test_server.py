import os
import pytest
import sys
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.server import app
from src.main import create_website, is_data_driven_request, validate_generated_files

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def temp_output_dir():
    """Create a temporary output directory for testing"""
    temp_dir = tempfile.mkdtemp()
    original_output = '../output'
    
    # Mock the output directory path in main.py
    with patch('src.main.os.path.exists') as mock_exists, \
         patch('src.main.os.makedirs') as mock_makedirs, \
         patch('src.main.open', create=True) as mock_open:
        
        mock_exists.return_value = True
        yield temp_dir
    
    # Cleanup
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

def test_generate_endpoint(client, monkeypatch):
    """
    Test the /generate endpoint to ensure it returns a JSON response
    with a preview URL and creates the files.
    """
    # Mock the create_website function to avoid actual API calls
    def mock_create_website(prompt):
        # Simulate creating files and returning the new format
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        files = ["index.html", "style.css"]
        with open(os.path.join(output_dir, files[0]), "w") as f:
            f.write("<h1>Test Website</h1>")
        with open(os.path.join(output_dir, files[1]), "w") as f:
            f.write("body { color: red; }")
        return {"files": files}

    monkeypatch.setattr("src.server.create_website", mock_create_website)

    # Clear the output directory before the test
    output_dir = "output"
    if os.path.exists(output_dir):
        for file in os.listdir(output_dir):
            os.remove(os.path.join(output_dir, file))

    response = client.post('/generate', data={'prompt': 'a test prompt'})
    
    assert response.status_code == 200
    assert response.is_json
    json_data = response.get_json()
    assert 'preview_url' in json_data
    assert json_data['preview_url'] == '/output/index.html'

    # Check that the files were actually created
    assert os.path.exists(os.path.join(output_dir, "index.html"))
    assert os.path.exists(os.path.join(output_dir, "style.css"))

def test_generate_endpoint_empty_prompt(client):
    """Test that empty prompts return an error"""
    response = client.post('/generate', data={'prompt': ''})
    assert response.status_code == 400
    json_data = response.get_json()
    assert 'error' in json_data

def test_generate_endpoint_long_prompt(client):
    """Test that overly long prompts return an error"""
    long_prompt = 'a' * 1001  # Over the 1000 character limit
    response = client.post('/generate', data={'prompt': long_prompt})
    assert response.status_code == 400
    json_data = response.get_json()
    assert 'error' in json_data

def test_backend_detection():
    """Test the backend detection logic"""
    # Should require backend
    assert is_data_driven_request("flower shop with orders") == True
    assert is_data_driven_request("e-commerce site with cart") == True
    assert is_data_driven_request("blog with user comments") == True
    assert is_data_driven_request("booking system for appointments") == True
    assert is_data_driven_request("user registration system") == True
    
    # Should not require backend
    assert is_data_driven_request("simple landing page") == False
    assert is_data_driven_request("static portfolio website") == False
    assert is_data_driven_request("informational brochure site") == False
    assert is_data_driven_request("company about page") == False

def test_file_validation():
    """Test the file validation logic"""
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

def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code in [200, 500]  # May fail if no database
    json_data = response.get_json()
    assert 'status' in json_data

def test_clear_all_endpoint(client, monkeypatch):
    """Test the clear all functionality"""
    # Mock database operations
    mock_db = MagicMock()
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    
    mock_db.get_connection.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    
    monkeypatch.setattr("src.server.db", mock_db)
    
    # Create some test files
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    test_file = os.path.join(output_dir, "test.html")
    with open(test_file, "w") as f:
        f.write("<h1>Test</h1>")
    
    response = client.post('/api/clear-all')
    
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data.get('success') == True
    
    # Verify file was deleted
    assert not os.path.exists(test_file)

def test_download_zip_endpoint(client):
    """Test the ZIP download functionality"""
    # Create some test files
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "index.html"), "w") as f:
        f.write("<h1>Test</h1>")
    with open(os.path.join(output_dir, "style.css"), "w") as f:
        f.write("body { margin: 0; }")
    
    response = client.get('/download-zip')
    
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/zip'
    
    # Test with no files
    shutil.rmtree(output_dir)
    response = client.get('/download-zip')
    assert response.status_code == 404

def test_api_reset_endpoint(client):
    """Test the API reset functionality"""
    response = client.get('/api/reset')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data.get('status') == 'reset'

def test_serve_output_files(client):
    """
    Test that the server can serve the generated files.
    """
    # Create dummy files to serve
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "test.html"), "w") as f:
        f.write("<h1>Test</h1>")

    response = client.get('/output/test.html')
    assert response.status_code == 200
    assert b"<h1>Test</h1>" in response.data

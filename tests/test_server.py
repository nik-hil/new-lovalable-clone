import os
import pytest
import sys
# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.server import app
from src.main import create_website

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

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

    monkeypatch.setattr("server.create_website", mock_create_website)

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

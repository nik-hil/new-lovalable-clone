#!/usr/bin/env python3
"""
Test cases for validating generated website files in the output folder
"""
import os
import sys
import pytest
import subprocess
import tempfile
import shutil
from pathlib import Path

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestOutputValidation:
    """Test cases for validating generated output files"""
    
    @pytest.fixture
    def output_dir(self):
        """Get the output directory path"""
        return os.path.join(os.path.dirname(__file__), '..', 'output')
    
    def test_output_directory_exists(self, output_dir):
        """Test that output directory exists"""
        assert os.path.exists(output_dir), "Output directory should exist"
    
    def test_has_html_files(self, output_dir):
        """Test that output contains HTML files"""
        if not os.listdir(output_dir):
            pytest.skip("No files in output directory")
        
        html_files = [f for f in os.listdir(output_dir) if f.endswith('.html')]
        assert len(html_files) > 0, "Should have at least one HTML file"
    
    def test_has_css_files(self, output_dir):
        """Test that output contains CSS files"""
        if not os.listdir(output_dir):
            pytest.skip("No files in output directory")
        
        css_files = [f for f in os.listdir(output_dir) if f.endswith('.css')]
        assert len(css_files) > 0, "Should have at least one CSS file"
    
    def test_html_files_are_valid(self, output_dir):
        """Test that HTML files are valid"""
        if not os.listdir(output_dir):
            pytest.skip("No files in output directory")
        
        html_files = [f for f in os.listdir(output_dir) if f.endswith('.html')]
        for html_file in html_files:
            file_path = os.path.join(output_dir, html_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert '<!DOCTYPE html>' in content or '<html' in content, f"{html_file} should be valid HTML"
                assert '</html>' in content, f"{html_file} should have closing html tag"
    
    def test_css_files_are_valid(self, output_dir):
        """Test that CSS files contain valid CSS"""
        if not os.listdir(output_dir):
            pytest.skip("No files in output directory")
        
        css_files = [f for f in os.listdir(output_dir) if f.endswith('.css')]
        for css_file in css_files:
            file_path = os.path.join(output_dir, css_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Basic CSS validation - should have some selectors or properties
                assert '{' in content and '}' in content, f"{css_file} should contain CSS rules"
    
    def test_python_files_syntax(self, output_dir):
        """Test that any Python files have valid syntax"""
        if not os.listdir(output_dir):
            pytest.skip("No files in output directory")
        
        python_files = [f for f in os.listdir(output_dir) if f.endswith('.py')]
        for python_file in python_files:
            file_path = os.path.join(output_dir, python_file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                compile(code, python_file, 'exec')
            except SyntaxError as e:
                pytest.fail(f"Python file {python_file} has syntax error: {e}")
    
    def test_flask_app_structure(self, output_dir):
        """Test Flask app files if they exist"""
        if not os.listdir(output_dir):
            pytest.skip("No files in output directory")
        
        flask_files = [f for f in os.listdir(output_dir) if f.endswith('.py') and ('app' in f.lower() or 'main' in f.lower())]
        
        for flask_file in flask_files:
            file_path = os.path.join(output_dir, flask_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'flask' in content.lower():
                    assert 'from flask import' in content, f"{flask_file} should import Flask"
                    assert 'app = Flask(' in content or 'Flask(__name__)' in content, f"{flask_file} should create Flask app"
    
    def test_database_files_structure(self, output_dir):
        """Test database files if they exist"""
        if not os.listdir(output_dir):
            pytest.skip("No files in output directory")
        
        sql_files = [f for f in os.listdir(output_dir) if f.endswith('.sql')]
        for sql_file in sql_files:
            file_path = os.path.join(output_dir, sql_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().upper()
                # Basic SQL validation
                assert any(keyword in content for keyword in ['CREATE', 'INSERT', 'SELECT', 'UPDATE']), f"{sql_file} should contain SQL statements"
    
    def test_files_are_not_empty(self, output_dir):
        """Test that generated files are not empty"""
        if not os.listdir(output_dir):
            pytest.skip("No files in output directory")
        
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                assert file_size > 0, f"File {filename} should not be empty"
    
    def test_can_serve_html_files(self, output_dir):
        """Test that HTML files can be served (basic content validation)"""
        if not os.listdir(output_dir):
            pytest.skip("No files in output directory")
        
        html_files = [f for f in os.listdir(output_dir) if f.endswith('.html')]
        for html_file in html_files:
            file_path = os.path.join(output_dir, html_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Check for basic web content
                assert len(content.strip()) > 100, f"{html_file} should have substantial content"
                # Should have some common HTML elements
                common_elements = ['<title', '<body', '<head', '<div', '<p', '<h1', '<h2', '<style', '<script']
                has_elements = any(element in content.lower() for element in common_elements)
                assert has_elements, f"{html_file} should contain common HTML elements"

class TestOutputScriptExecution:
    """Test cases for executing Python scripts in output folder"""
    
    @pytest.fixture
    def output_dir(self):
        """Get the output directory path"""
        return os.path.join(os.path.dirname(__file__), '..', 'output')
    
    def test_python_scripts_import_correctly(self, output_dir):
        """Test that Python scripts can be imported without errors"""
        if not os.listdir(output_dir):
            pytest.skip("No files in output directory")
        
        python_files = [f for f in os.listdir(output_dir) if f.endswith('.py')]
        
        # Create a temporary directory and copy files there for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            for python_file in python_files:
                src_path = os.path.join(output_dir, python_file)
                dst_path = os.path.join(temp_dir, python_file)
                shutil.copy2(src_path, dst_path)
            
            # Try to check syntax of each Python file
            for python_file in python_files:
                file_path = os.path.join(temp_dir, python_file)
                try:
                    result = subprocess.run(
                        [sys.executable, '-m', 'py_compile', file_path],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    assert result.returncode == 0, f"Python file {python_file} failed compilation: {result.stderr}"
                except subprocess.TimeoutExpired:
                    pytest.fail(f"Python file {python_file} compilation timed out")
                except Exception as e:
                    pytest.fail(f"Error testing Python file {python_file}: {e}")
    
    def test_flask_app_can_start_dry_run(self, output_dir):
        """Test that Flask apps can be validated without actually starting the server"""
        if not os.listdir(output_dir):
            pytest.skip("No files in output directory")
        
        python_files = [f for f in os.listdir(output_dir) if f.endswith('.py')]
        
        for python_file in python_files:
            file_path = os.path.join(output_dir, python_file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # If it's a Flask app, check basic structure
            if 'from flask import' in content.lower():
                # Check for required Flask patterns
                assert 'app = Flask(' in content or 'Flask(__name__)' in content, f"{python_file} should create Flask app"
                assert '@app.route' in content, f"{python_file} should have route definitions"
                
                # Check if it has a proper main block
                if "if __name__ == '__main__':" in content:
                    assert 'app.run(' in content, f"{python_file} should have app.run() in main block"

if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])

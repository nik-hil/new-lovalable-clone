from flask import Flask, request, render_template, send_from_directory, jsonify
from src.main import create_website
import os
import re

app = Flask(__name__, template_folder='site', static_folder=None)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        prompt = request.form.get('prompt', '').strip()
        if not prompt:
            return jsonify({"error": "Please provide a prompt to generate your website."}), 400
        
        result = create_website(prompt)
        
        if "error" in result:
            return jsonify({"error": result["error"]}), 500

        # Find the main HTML file in the list of generated files
        main_file = next((f for f in result.get("files", []) if f.endswith('.html')), None)

        if main_file:
            preview_url = f"/output/{main_file}"
            return jsonify({
                "preview_url": preview_url,
                "files_created": result.get("files", [])
            })
        else:
            return jsonify({"error": "Could not determine the main file for preview."}), 500
    
    except ValueError as e:
        return jsonify({"error": f"Configuration error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/site/<path:path>')
def serve_site(path):
    return send_from_directory('site', path)

@app.route('/output/<path:path>')
def serve_output(path):
    return send_from_directory('output', path)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

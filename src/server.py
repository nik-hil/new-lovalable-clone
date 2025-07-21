from flask import Flask, request, render_template, send_from_directory, jsonify, send_file
from .main import create_website
import os
import zipfile
from io import BytesIO

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

@app.route('/download-zip')
def download_zip():
    """Generate and download a ZIP file containing all generated website files."""
    try:
        output_dir = 'output'
        
        if not os.path.exists(output_dir) or not os.listdir(output_dir):
            return jsonify({"error": "No website files found. Please generate a website first."}), 404
        
        # Create a BytesIO object to hold the ZIP file in memory
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for filename in os.listdir(output_dir):
                file_path = os.path.join(output_dir, filename)
                if os.path.isfile(file_path):
                    zip_file.write(file_path, filename)
        
        zip_buffer.seek(0)
        
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='website.zip'
        )
        
    except Exception as e:
        app.logger.error(f"Error creating ZIP file: {str(e)}")
        return jsonify({"error": "Failed to create ZIP file."}), 500

@app.route('/site/<path:path>')
def serve_site(path):
    return send_from_directory('site', path)

@app.route('/output/<path:path>')
def serve_output(path):
    return send_from_directory('output', path)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

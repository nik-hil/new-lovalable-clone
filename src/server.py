from flask import Flask, request, render_template, send_from_directory, jsonify, send_file
from main import create_website
from database import DatabaseManager
import os
import re
import zipfile
import tempfile
from io import BytesIO

app = Flask(__name__, template_folder='../site', static_folder=None)

# Initialize database manager
db = DatabaseManager()
current_website_id = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    global current_website_id
    try:
        prompt = request.form.get('prompt', '').strip()
        
        if not prompt:
            return jsonify({"error": "Please provide a prompt to generate your website."}), 400
        
        if len(prompt) > 1000:
            return jsonify({"error": "Prompt is too long. Please keep it under 1000 characters."}), 400
        
        result = create_website(prompt)
        
        if "error" in result:
            return jsonify({"error": result["error"]}), 500

        # Find the main HTML file in the list of generated files
        main_file = next((f for f in result.get("files", []) if f.endswith('.html')), None)

        if main_file:
            # Save to database
            files_generated = result.get("files", [])
            
            # Determine if this is a new website or refinement
            try:
                if current_website_id is None:
                    # New website
                    website_id = db.create_website(prompt, files_generated)
                    if website_id:
                        current_website_id = website_id
                        success = db.add_prompt_history(website_id, prompt, 'initial')
                        print(f"Database save - New website ID: {website_id}, History saved: {success}")
                    else:
                        print("Failed to create website in database")
                else:
                    # Refinement of existing website
                    success = db.update_website_files(current_website_id, files_generated)
                    history_success = db.add_prompt_history(current_website_id, prompt, 'refinement')
                    print(f"Database save - Updated website ID: {current_website_id}, Files: {success}, History: {history_success}")
            except Exception as e:
                print(f"Database error: {e}")
                # Continue even if database fails
            
            preview_url = f"/output/{main_file}"
            # Create the full URL for the new tab - this was the issue!
            new_tab_url = f"{request.url_root}output/{main_file}"
            return jsonify({
                "preview_url": preview_url,
                "new_tab_url": new_tab_url,  # Add full URL for new tab
                "files_generated": result.get("files", []),
                "message": f"Successfully generated {len(result.get('files', []))} files"
            })
        else:
            return jsonify({"error": "No HTML file was generated. Please try a different prompt."}), 500
            
    except Exception as e:
        app.logger.error(f"Error in generate endpoint: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again."}), 500

@app.route('/api/health')
def health_check():
    try:
        # Test database connection
        db.get_connection()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": f"error: {str(e)}"}, 500

@app.route('/api/history')
def get_history():
    """Get prompt history and latest website data"""
    try:
        latest_website = db.get_latest_website()
        if latest_website:
            global current_website_id
            current_website_id = latest_website['id']
            
            return jsonify({
                "success": True,
                "website": {
                    "id": latest_website['id'],
                    "files": latest_website['files_generated'],
                    "created_at": latest_website['created_at'].isoformat()
                },
                "history": [
                    {
                        "prompt": h['prompt_text'],
                        "prompt_type": h['prompt_type'],
                        "created_at": h['created_at'].isoformat()
                    }
                    for h in latest_website['history']
                ]
            })
        else:
            return jsonify({"success": True, "website": None, "history": []})
    except Exception as e:
        print(f"Error getting history: {e}")
        return jsonify({"success": False, "website": None, "history": [], "error": str(e)})

@app.route('/api/reset')
def reset_session():
    """Reset current session to start a new website"""
    global current_website_id
    current_website_id = None
    return jsonify({"status": "reset"})

@app.route('/download-zip')
def download_zip():
    """Generate and download a ZIP file containing all generated website files."""
    try:
        output_dir = '../output'
        
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
    return send_from_directory('../site', path)

@app.route('/output/<path:path>')
def serve_output(path):
    try:
        return send_from_directory('../output', path)
    except FileNotFoundError:
        return "File not found", 404

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Page not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    # Listen on all interfaces for Docker compatibility
    app.run(debug=True, host='0.0.0.0', port=5001)

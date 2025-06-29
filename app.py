import os
from flask import Flask, request, render_template, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import uuid
from processor import blur_faces

app = Flask(__name__)

# Configuration
# Use environment variables for flexibility across deployment environments
UPLOAD_FOLDER = os.path.join('static', 'uploads')
PROCESSED_FOLDER = os.path.join('static', 'processed')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    files = request.files.getlist('file')
    results = []

    for file in files:
        if file and allowed_file(file.filename):
            try:
                # Generate unique filenames
                unique_id = str(uuid.uuid4())
                original_filename = secure_filename(file.filename)
                filename_parts = original_filename.rsplit('.', 1)
                
                # Create secure filenames with unique ID
                original_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                            f"{filename_parts[0]}_{unique_id}.{filename_parts[1]}")
                processed_path = os.path.join(app.config['PROCESSED_FOLDER'],
                                            f"{filename_parts[0]}_{unique_id}.{filename_parts[1]}")
                
                # Save the uploaded file
                file.save(original_path)
                
                # Process the image
                success, result = blur_faces(original_path, processed_path)
                
                if not success:
                    results.append({'error': result, 'filename': original_filename})
                    continue
                
                # Get filenames for URLs
                original_filename_url = os.path.basename(original_path)
                processed_filename_url = os.path.basename(processed_path)
                
                results.append({
                    'success': True,
                    'message': f"Processed successfully. Detected and blurred {result} faces." if result > 0 else "No faces detected in the image.",
                    'original_image': f"/uploads/{original_filename_url}",
                    'processed_image': f"/processed/{processed_filename_url}",
                    'filename': original_filename
                })
            except Exception as e:
                print(f"Error in upload: {str(e)}")
                results.append({'error': f"Server error: {str(e)}", 'filename': original_filename})
        else:
            results.append({'error': 'File type not allowed', 'filename': file.filename})

    return jsonify(results)


# For Vercel: add a health check endpoint
@app.route('/health')
def health_check():
    return jsonify({'status': 'ok'})

# For API usage
@app.route('/api/upload', methods=['POST'])
def api_upload_file():
    # Same functionality as upload_file, just a different endpoint
    return upload_file()

# Initialize application
if __name__ == '__main__':
    # Get port from environment variable or use 8080 as default
    port = int(os.environ.get('PORT', 8080))
    # In production, set debug to False
    debug = os.environ.get('FLASK_ENV', 'production') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
from flask import Flask, request, jsonify, send_from_directory, abort
from werkzeug.utils import secure_filename
import os
import logging
from functools import wraps
from config import Config
import uuid

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class FileServiceApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)  # Load configuration from Config class

        # Ensure storage path exists
        if not os.path.exists(self.app.config['STORAGE_PATH']):
            os.makedirs(self.app.config['STORAGE_PATH'])

        # Configure logging
        logging.basicConfig(level=logging.INFO)

        self.add_routes()
        self.register_error_handlers()

    def check_auth(self, username: str, password: str) -> bool:
        """Check if a username/password combination is valid."""
        return username == self.app.config['USERNAME'] and password == self.app.config['PASSWORD']

    def authenticate(self):
        """Sends a 401 response that enables basic auth."""
        return jsonify({'message': 'Authentication required'}), 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}

    def requires_auth(self, f):
        """Decorator to require authentication for a route."""
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not self.check_auth(auth.username, auth.password):
                return self.authenticate()
            return f(*args, **kwargs)
        return decorated

    def allowed_file(self, filename: str) -> bool:
        """Check if the file has an allowed extension."""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def add_routes(self):
        @self.app.route('/upload', methods=['POST'])
        @self.requires_auth
        def upload_file():
            """Endpoint to upload a file."""
            if 'file' not in request.files:
                return jsonify({'message': 'No file part'}), 400
            file = request.files['file']
            if file.filename == '':
                return jsonify({'message': 'No selected file'}), 400
            if file and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower()
                new_filename = f"{uuid.uuid4().hex}.{file_ext}"
                file_path = os.path.join(self.app.config['STORAGE_PATH'], new_filename)
                file.save(file_path)
                logging.info(f"File {filename} uploaded by {request.authorization.username} as {new_filename}")
                return jsonify({'message': 'File uploaded successfully', 'filename': new_filename}), 201
            else:
                return jsonify({'message': 'File type not allowed'}), 400

        @self.app.route('/files', methods=['GET'])
        @self.requires_auth
        def list_files():
            """Endpoint to list all uploaded files."""
            try:
                files = []
                for filename in os.listdir(self.app.config['STORAGE_PATH']):
                    path = os.path.join(self.app.config['STORAGE_PATH'], filename)
                    if os.path.isfile(path):
                        files.append({
                            'name': filename,
                            'size': os.path.getsize(path),
                            'date': os.path.getmtime(path)
                        })
                logging.info(f"Files listed by {request.authorization.username}")
                return jsonify(files)
            except Exception as e:
                logging.error(f"Error listing files: {e}")
                return jsonify({'message': 'Error listing files'}), 500

        @self.app.route('/files/<filename>', methods=['GET'])
        @self.requires_auth
        def get_file(filename: str):
            """Endpoint to download a file."""
            try:
                logging.info(f"File {filename} downloaded by {request.authorization.username}")
                return send_from_directory(self.app.config['STORAGE_PATH'], filename)
            except FileNotFoundError:
                logging.warning(f"File {filename} not found")
                abort(404)
            except Exception as e:
                logging.error(f"Error downloading file {filename}: {e}")
                abort(500)

        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Endpoint to check the health of the service."""
            return jsonify({'status': 'OK'})

    def register_error_handlers(self):
        """Register error handlers for the application."""
        @self.app.errorhandler(404)
        def not_found_error(error):
            return jsonify({'message': 'Resource not found'}), 404

        @self.app.errorhandler(500)
        def internal_error(error):
            return jsonify({'message': 'Internal server error'}), 500

    def run(self):
        self.app.run(port=self.app.config['PORT'])

# Create an instance of the app
app_instance = FileServiceApp()
app = app_instance.app

if __name__ == '__main__':
    app_instance.run()

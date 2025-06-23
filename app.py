import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from dotenv import load_dotenv

# Import services
from services.auth_service import AuthService
from services.analysis_service import AnalysisService
from services.storage_service import StorageService
from services.notification_service import NotificationService

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour
jwt = JWTManager(app)

# Initialize services
auth_service = AuthService()
analysis_service = AnalysisService()
storage_service = StorageService()
notification_service = NotificationService()

# Authentication routes
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Authenticate user
    user = auth_service.authenticate(email, password)
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Create access token
    access_token = create_access_token(identity=user['id'])
    return jsonify({'token': access_token, 'user': user}), 200

@app.route('/api/auth/logout', methods=['GET'])
@jwt_required()
def logout():
    # JWT blacklisting would be implemented here in a production system
    return jsonify({'message': 'Logout successful'}), 200

# Project routes
@app.route('/api/projects', methods=['GET'])
@jwt_required()
def get_projects():
    user_id = get_jwt_identity()
    projects = storage_service.get_user_projects(user_id)
    return jsonify({'projects': projects}), 200

@app.route('/api/projects', methods=['POST'])
@jwt_required()
def create_project():
    user_id = get_jwt_identity()
    data = request.get_json()
    project = storage_service.create_project(user_id, data)
    return jsonify({'project': project}), 201

@app.route('/api/projects/<project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    user_id = get_jwt_identity()
    project = storage_service.get_project(project_id, user_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    return jsonify({'project': project}), 200

# Asset routes
@app.route('/api/projects/<project_id>/assets', methods=['POST'])
@jwt_required()
def upload_asset(project_id):
    user_id = get_jwt_identity()
    
    # Check if project exists and user has access
    project = storage_service.get_project(project_id, user_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    # Handle file upload
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    metadata = request.form.get('metadata', '{}')
    asset = storage_service.upload_asset(project_id, file, metadata)
    return jsonify({'asset': asset}), 201

@app.route('/api/projects/<project_id>/assets', methods=['GET'])
@jwt_required()
def get_assets(project_id):
    user_id = get_jwt_identity()
    
    # Check if project exists and user has access
    project = storage_service.get_project(project_id, user_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
        
    assets = storage_service.get_project_assets(project_id)
    return jsonify({'assets': assets}), 200

# Analysis routes
@app.route('/api/projects/<project_id>/analyze', methods=['POST'])
@jwt_required()
def analyze_project(project_id):
    user_id = get_jwt_identity()
    
    # Check if project exists and user has access
    project = storage_service.get_project(project_id, user_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
        
    data = request.get_json()
    analysis_id = analysis_service.create_analysis_job(project_id, data)
    
    # In a real implementation, this would be a background job
    # For now, we'll run it synchronously
    result = analysis_service.run_analysis(analysis_id)
    
    # Send notification
    notification_service.send_analysis_complete(user_id, project_id, analysis_id)
    
    return jsonify({'analysis_id': analysis_id, 'result': result}), 200

@app.route('/api/projects/<project_id>/analysis', methods=['GET'])
@jwt_required()
def get_analyses(project_id):
    user_id = get_jwt_identity()
    
    # Check if project exists and user has access
    project = storage_service.get_project(project_id, user_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
        
    analyses = analysis_service.get_project_analyses(project_id)
    return jsonify({'analyses': analyses}), 200

@app.route('/api/projects/<project_id>/analysis/<analysis_id>', methods=['GET'])
@jwt_required()
def get_analysis(project_id, analysis_id):
    user_id = get_jwt_identity()
    
    # Check if project exists and user has access
    project = storage_service.get_project(project_id, user_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
        
    analysis = analysis_service.get_analysis(analysis_id)
    if not analysis or analysis['project_id'] != project_id:
        return jsonify({'error': 'Analysis not found'}), 404
        
    return jsonify({'analysis': analysis}), 200

# Continuity rule routes
@app.route('/api/rules', methods=['GET'])
@jwt_required()
def get_rules():
    user_id = get_jwt_identity()
    rules = storage_service.get_user_rules(user_id)
    return jsonify({'rules': rules}), 200

@app.route('/api/rules', methods=['POST'])
@jwt_required()
def create_rule():
    user_id = get_jwt_identity()
    data = request.get_json()
    rule = storage_service.create_rule(user_id, data)
    return jsonify({'rule': rule}), 201

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
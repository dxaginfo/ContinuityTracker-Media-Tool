import os
import uuid
from datetime import datetime
from firebase_admin import firestore, storage

class StorageService:
    def __init__(self):
        self.db = firestore.client()
        self.bucket = storage.bucket()
    
    def create_project(self, user_id, data):
        """Create a new project"""
        project_id = str(uuid.uuid4())
        
        # Prepare project data
        project_data = {
            'id': project_id,
            'name': data.get('name', 'Untitled Project'),
            'description': data.get('description', ''),
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP,
            'created_by': user_id,
            'members': [user_id],
            'settings': data.get('settings', {})
        }
        
        # Store in Firestore
        self.db.collection('projects').document(project_id).set(project_data)
        
        return project_data
    
    def get_project(self, project_id, user_id):
        """Get project details, ensuring user has access"""
        try:
            project_ref = self.db.collection('projects').document(project_id).get()
            if not project_ref.exists:
                return None
                
            project = project_ref.to_dict()
            
            # Check if user has access
            if user_id not in project.get('members', []):
                return None
                
            return project
        except Exception as e:
            print(f"Error getting project: {str(e)}")
            return None
    
    def get_user_projects(self, user_id):
        """Get all projects for a user"""
        projects = []
        
        try:
            project_docs = self.db.collection('projects').where('members', 'array_contains', user_id).stream()
            for doc in project_docs:
                project = doc.to_dict()
                projects.append(project)
            
            return projects
        except Exception as e:
            print(f"Error getting projects: {str(e)}")
            return []
    
    def upload_asset(self, project_id, file, metadata_json):
        """Upload a media asset"""
        try:
            # Parse metadata
            metadata = {}
            if metadata_json:
                metadata = json.loads(metadata_json)
            
            # Generate asset ID
            asset_id = str(uuid.uuid4())
            
            # Determine file type
            filename = file.filename
            file_extension = os.path.splitext(filename)[1].lower()
            
            # Set content type
            content_type = 'application/octet-stream'  # Default
            if file_extension in ['.mp4', '.mov']:
                content_type = 'video/mp4'
            elif file_extension in ['.jpg', '.jpeg']:
                content_type = 'image/jpeg'
            elif file_extension in ['.png']:
                content_type = 'image/png'
            
            # Create storage path
            storage_path = f"projects/{project_id}/assets/{asset_id}{file_extension}"
            
            # Upload to Cloud Storage
            blob = self.bucket.blob(storage_path)
            blob.upload_from_file(file, content_type=content_type)
            
            # Generate public URL
            url = blob.public_url
            
            # Prepare asset data
            asset_data = {
                'asset_id': asset_id,
                'project_id': project_id,
                'filename': filename,
                'storage_path': storage_path,
                'url': url,
                'content_type': content_type,
                'type': 'video' if content_type.startswith('video') else 'image',
                'uploaded_at': firestore.SERVER_TIMESTAMP,
                'metadata': metadata,
                'scene_info': metadata.get('scene_info', {})
            }
            
            # Store in Firestore
            self.db.collection('assets').document(asset_id).set(asset_data)
            
            return asset_data
        except Exception as e:
            print(f"Error uploading asset: {str(e)}")
            return None
    
    def get_project_assets(self, project_id):
        """Get all assets for a project"""
        assets = []
        
        try:
            asset_docs = self.db.collection('assets').where('project_id', '==', project_id).stream()
            for doc in asset_docs:
                asset = doc.to_dict()
                assets.append(asset)
            
            return assets
        except Exception as e:
            print(f"Error getting assets: {str(e)}")
            return []
    
    def create_rule(self, user_id, data):
        """Create a continuity rule"""
        rule_id = str(uuid.uuid4())
        
        # Prepare rule data
        rule_data = {
            'id': rule_id,
            'rule_type': data.get('rule_type', 'object_tracking'),
            'name': data.get('name', 'Untitled Rule'),
            'description': data.get('description', ''),
            'priority': data.get('priority', 'medium'),
            'created_at': firestore.SERVER_TIMESTAMP,
            'created_by': user_id,
            'parameters': data.get('parameters', {}),
            'is_global': data.get('is_global', False),
            'project_id': data.get('project_id')  # Optional, if rule is project-specific
        }
        
        # Store in Firestore
        self.db.collection('rules').document(rule_id).set(rule_data)
        
        return rule_data
    
    def get_user_rules(self, user_id):
        """Get all rules created by or accessible to a user"""
        rules = []
        
        try:
            # Get user-created rules
            rule_docs = self.db.collection('rules').where('created_by', '==', user_id).stream()
            for doc in rule_docs:
                rule = doc.to_dict()
                rules.append(rule)
            
            # Get global rules
            global_docs = self.db.collection('rules').where('is_global', '==', True).stream()
            for doc in global_docs:
                rule = doc.to_dict()
                if rule.get('id') not in [r.get('id') for r in rules]:  # Avoid duplicates
                    rules.append(rule)
            
            # Get project-specific rules for projects the user is a member of
            user_projects = self.get_user_projects(user_id)
            project_ids = [p.get('id') for p in user_projects]
            
            for project_id in project_ids:
                project_docs = self.db.collection('rules').where('project_id', '==', project_id).stream()
                for doc in project_docs:
                    rule = doc.to_dict()
                    if rule.get('id') not in [r.get('id') for r in rules]:  # Avoid duplicates
                        rules.append(rule)
            
            return rules
        except Exception as e:
            print(f"Error getting rules: {str(e)}")
            return []
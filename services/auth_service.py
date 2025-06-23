import os
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore

class AuthService:
    def __init__(self):
        # Initialize Firebase Admin SDK
        # In a real application, this would use environment variables or secure secrets
        # For demo purposes, we're just initializing with default settings
        try:
            firebase_admin.get_app()
        except ValueError:
            # Use application default credentials or service account
            if os.path.exists('firebase-credentials.json'):
                cred = credentials.Certificate('firebase-credentials.json')
                firebase_admin.initialize_app(cred)
            else:
                firebase_admin.initialize_app()
        
        self.db = firestore.client()
    
    def authenticate(self, email, password):
        """Authenticate a user with email and password
        
        In a real application, this would verify credentials with Firebase Auth
        For demo purposes, we're simulating the authentication flow
        """
        try:
            # This is a mock implementation
            # In production, you would use Firebase Auth methods
            if email == 'demo@example.com' and password == 'password':
                # Return a mock user object
                return {
                    'id': 'user123',
                    'email': email,
                    'name': 'Demo User'
                }
            return None
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return None
    
    def get_user(self, user_id):
        """Get user details by ID"""
        try:
            user_ref = self.db.collection('users').document(user_id).get()
            if user_ref.exists:
                return user_ref.to_dict()
            return None
        except Exception as e:
            print(f"Error getting user: {str(e)}")
            return None
    
    def create_user(self, email, password, name):
        """Create a new user account"""
        try:
            # Create user in Firebase Auth
            user = auth.create_user(
                email=email,
                password=password,
                display_name=name
            )
            
            # Store additional user data in Firestore
            user_data = {
                'id': user.uid,
                'email': email,
                'name': name,
                'created_at': firestore.SERVER_TIMESTAMP
            }
            
            self.db.collection('users').document(user.uid).set(user_data)
            return user_data
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return None
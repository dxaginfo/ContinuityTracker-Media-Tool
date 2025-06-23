import os
import json
import requests
from firebase_admin import firestore
from datetime import datetime

class NotificationService:
    def __init__(self):
        self.db = firestore.client()
    
    def send_analysis_complete(self, user_id, project_id, analysis_id):
        """Send notification when analysis is complete"""
        try:
            # Get user details
            user_ref = self.db.collection('users').document(user_id).get()
            if not user_ref.exists:
                print(f"User {user_id} not found")
                return False
                
            user = user_ref.to_dict()
            
            # Get project details
            project_ref = self.db.collection('projects').document(project_id).get()
            if not project_ref.exists:
                print(f"Project {project_id} not found")
                return False
                
            project = project_ref.to_dict()
            
            # Create notification
            notification_id = self.db.collection('notifications').document().id
            notification = {
                'id': notification_id,
                'user_id': user_id,
                'project_id': project_id,
                'analysis_id': analysis_id,
                'type': 'analysis_complete',
                'title': 'Analysis Complete',
                'message': f"Continuity analysis for project '{project.get('name')}' is complete.",
                'timestamp': firestore.SERVER_TIMESTAMP,
                'read': False,
                'data': {
                    'project_id': project_id,
                    'analysis_id': analysis_id
                }
            }
            
            # Store in Firestore
            self.db.collection('notifications').document(notification_id).set(notification)
            
            # Send email notification if configured
            if 'email' in user and os.getenv('ENABLE_EMAIL_NOTIFICATIONS') == 'true':
                self._send_email_notification(user['email'], notification)
            
            # Send Slack notification if configured
            if os.getenv('ENABLE_SLACK_NOTIFICATIONS') == 'true':
                self._send_slack_notification(notification)
            
            return True
        except Exception as e:
            print(f"Error sending notification: {str(e)}")
            return False
    
    def _send_email_notification(self, email, notification):
        """Send email notification"""
        # This is a placeholder
        # In a real implementation, you would use an email service
        print(f"Sending email notification to {email}: {notification['title']}")
    
    def _send_slack_notification(self, notification):
        """Send Slack notification"""
        try:
            slack_webhook = os.getenv('SLACK_WEBHOOK_URL')
            if not slack_webhook:
                print("Slack webhook URL not configured")
                return False
            
            # Prepare message payload
            payload = {
                "text": notification['title'],
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": notification['title']
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": notification['message']
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*View Results*"
                        },
                        "accessory": {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Open Analysis"
                            },
                            "url": f"https://continuity-tracker-app.example.com/projects/{notification['data']['project_id']}/analysis/{notification['data']['analysis_id']}"
                        }
                    }
                ]
            }
            
            # Send to Slack
            response = requests.post(
                slack_webhook,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                print(f"Error sending Slack notification: {response.status_code} {response.text}")
                return False
                
            return True
        except Exception as e:
            print(f"Error sending Slack notification: {str(e)}")
            return False
    
    def get_user_notifications(self, user_id, limit=10, offset=0):
        """Get notifications for a user"""
        notifications = []
        
        try:
            # Query notifications for user, ordered by timestamp
            query = self.db.collection('notifications') \
                .where('user_id', '==', user_id) \
                .order_by('timestamp', direction='DESCENDING') \
                .limit(limit) \
                .offset(offset)
                
            notification_docs = query.stream()
            for doc in notification_docs:
                notification = doc.to_dict()
                notifications.append(notification)
            
            return notifications
        except Exception as e:
            print(f"Error getting notifications: {str(e)}")
            return []
    
    def mark_notification_read(self, notification_id, user_id):
        """Mark a notification as read"""
        try:
            # Get notification
            notification_ref = self.db.collection('notifications').document(notification_id).get()
            if not notification_ref.exists:
                return False
                
            notification = notification_ref.to_dict()
            
            # Verify user owns this notification
            if notification.get('user_id') != user_id:
                return False
            
            # Update notification
            self.db.collection('notifications').document(notification_id).update({
                'read': True,
                'read_at': firestore.SERVER_TIMESTAMP
            })
            
            return True
        except Exception as e:
            print(f"Error marking notification read: {str(e)}")
            return False
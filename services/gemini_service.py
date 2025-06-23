import os
import json
import requests
from dotenv import load_dotenv

class GeminiService:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize Gemini API settings
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent"
        
        # Check if API key is available
        if not self.api_key:
            print("Warning: GEMINI_API_KEY not found in environment variables")
    
    def identify_objects(self, image_url):
        """Identify objects in an image using Gemini API"""
        # This is a placeholder implementation
        # In a real application, you would call the Gemini API
        if not self.api_key:
            return self._mock_identify_objects(image_url)
        
        try:
            # Prepare request payload
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": "Identify all key objects in this media scene. Focus on props, clothing, and set elements. Provide a detailed list with descriptions and positions."},
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": self._get_base64_image(image_url)
                                }
                            }
                        ]
                    }
                ],
                "generation_config": {
                    "temperature": 0.4,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
            }
            
            # Send request to Gemini API
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                # Extract the text from the response
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                # Process the text to extract object information
                return self._parse_object_text(text)
            else:
                print(f"Error calling Gemini API: {response.status_code} {response.text}")
                return self._mock_identify_objects(image_url)
                
        except Exception as e:
            print(f"Error in identify_objects: {str(e)}")
            return self._mock_identify_objects(image_url)
    
    def compare_scenes(self, image_url1, image_url2):
        """Compare two scenes for continuity issues"""
        # This is a placeholder implementation
        # In a real application, you would call the Gemini API
        if not self.api_key:
            return self._mock_compare_scenes(image_url1, image_url2)
        
        try:
            # Prepare request payload
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": "Compare these two media scenes for continuity issues. Focus on props, clothing, set arrangement, lighting, and any other visual elements that should remain consistent between shots. Provide a detailed analysis of any inconsistencies found."},
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": self._get_base64_image(image_url1)
                                }
                            },
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": self._get_base64_image(image_url2)
                                }
                            }
                        ]
                    }
                ],
                "generation_config": {
                    "temperature": 0.4,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
            }
            
            # Send request to Gemini API
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                # Extract the text from the response
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                # Process the text to extract continuity issues
                return self._parse_comparison_text(text)
            else:
                print(f"Error calling Gemini API: {response.status_code} {response.text}")
                return self._mock_compare_scenes(image_url1, image_url2)
                
        except Exception as e:
            print(f"Error in compare_scenes: {str(e)}")
            return self._mock_compare_scenes(image_url1, image_url2)
    
    def _get_base64_image(self, image_url):
        """Convert image URL to base64 encoding"""
        # In a real implementation, this would download and encode the image
        # For this placeholder, we'll return a mock value
        return "base64_encoded_image_data"
    
    def _parse_object_text(self, text):
        """Parse the Gemini API text response to extract object information"""
        # In a real implementation, this would parse the text to extract structured data
        # For this placeholder, we'll return a mock value
        return ["chair", "table", "lamp", "book", "person"]
    
    def _parse_comparison_text(self, text):
        """Parse the Gemini API text response to extract continuity issues"""
        # In a real implementation, this would parse the text to extract structured data
        # For this placeholder, we'll return a mock value
        return {
            "issues": [
                {
                    "type": "prop_inconsistency",
                    "description": "Coffee mug changed color between scenes",
                    "confidence": 0.92
                },
                {
                    "type": "lighting_shift",
                    "description": "Lighting direction changed between scenes",
                    "confidence": 0.78
                }
            ]
        }
    
    def _mock_identify_objects(self, image_url):
        """Generate mock object identification results"""
        # This is used when the API key is not available or for testing
        return ["chair", "table", "lamp", "book", "person"]
    
    def _mock_compare_scenes(self, image_url1, image_url2):
        """Generate mock scene comparison results"""
        # This is used when the API key is not available or for testing
        return {
            "issues": [
                {
                    "type": "prop_inconsistency",
                    "description": "Coffee mug changed color between scenes",
                    "confidence": 0.92
                },
                {
                    "type": "lighting_shift",
                    "description": "Lighting direction changed between scenes",
                    "confidence": 0.78
                }
            ]
        }
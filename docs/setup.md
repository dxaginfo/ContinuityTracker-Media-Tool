# ContinuityTracker Setup Guide

## Prerequisites

- Python 3.10 or higher
- Firebase account
- Google Cloud Platform account with Gemini API access
- Node.js and npm (for frontend development)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/dxaginfo/ContinuityTracker-Media-Tool.git
cd ContinuityTracker-Media-Tool
```

### 2. Set Up Python Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Firebase

1. Create a new Firebase project at [https://console.firebase.google.com/](https://console.firebase.google.com/)
2. Set up Firestore Database
3. Set up Storage
4. Set up Authentication (with Email/Password provider)
5. Download your Firebase service account key
6. Save the key as `firebase-credentials.json` in the project root

### 4. Set Up Google Cloud and Gemini API

1. Ensure your Google Cloud project has the Gemini API enabled
2. Create an API key for Gemini API access

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```
# Server configuration
PORT=5000

# Firebase config
FIREBASE_PROJECT_ID=your-project-id

# JWT configuration
JWT_SECRET_KEY=your-jwt-secret

# Gemini API configuration
GEMINI_API_KEY=your-gemini-api-key

# Notification settings
ENABLE_EMAIL_NOTIFICATIONS=false
ENABLE_SLACK_NOTIFICATIONS=false
SLACK_WEBHOOK_URL=your-slack-webhook-url
```

### 6. Initialize the Database

```bash
python setup.py
```

### 7. Start the Server

```bash
python app.py
```

The server will start on http://localhost:5000

## Running in Production

For production deployment, we recommend using Gunicorn with a reverse proxy like Nginx:

```bash
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

### Docker Deployment

A Dockerfile is included for containerized deployment:

```bash
# Build the Docker image
docker build -t continuity-tracker .

# Run the container
docker run -p 5000:5000 --env-file .env continuity-tracker
```

## Frontend Development

The frontend is built with React and is located in the `/frontend` directory:

```bash
cd frontend
npm install
npm start
```

This will start the development server on http://localhost:3000

## Troubleshooting

### Firebase Connection Issues

If you encounter issues connecting to Firebase:

- Verify that your `firebase-credentials.json` file is in the project root
- Check that your Firebase project has the necessary services enabled
- Ensure your IP address is allowed in Firebase Security Rules

### Gemini API Issues

If the Gemini API integration isn't working:

- Verify your API key is correct
- Check that the Gemini API is enabled in your Google Cloud project
- Ensure you have proper quota and billing set up

### For Additional Help

Open an issue on GitHub or contact the development team at support@example.com
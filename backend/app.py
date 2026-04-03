import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import external services
from services.firebase_service import init_firebase
from services.ai_service import init_ai

# Import blueprints
from routes.api_routes import api_bp

app = Flask(__name__)
CORS(app)

# 1. Initialize Firebase
init_firebase()

# 2. Initialize Groq AI
init_ai()

# Register routes
app.register_blueprint(api_bp)

if __name__ == '__main__':
    # Use port from .env or default to 5001
    port = int(os.getenv("PORT", 5001))
    app.run(debug=True, port=port)


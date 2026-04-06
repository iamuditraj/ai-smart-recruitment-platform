import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import external services
from services.firebase_service import init_firebase
from services.ai_service import init_ai

# Import blueprints
from routes.auth_routes import auth_bp
from routes.profile_routes import profile_bp
from routes.job_routes import job_bp
from routes.candidate_routes import candidate_bp
from routes.recruiter_routes import recruiter_bp
from routes.ai_routes import ai_bp

app = Flask(__name__)
CORS(app)

# 1. Initialize Firebase
init_firebase()

# 2. Initialize Groq AI
init_ai()

# Register routes
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(job_bp)
app.register_blueprint(candidate_bp)
app.register_blueprint(recruiter_bp)
app.register_blueprint(ai_bp)

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "project": "HireAI",
        "message": "Flask is integrated correctly!"
    })

@app.route('/api/check-db')
def check_db():
    try:
        from services.firebase_service import get_db
        db = get_db()
        if not db:
            return jsonify({"status": "error", "message": "Firebase not initialized. Did you add serviceAccountKey.json?"})
        # Simple test to see if we can talk to Firestore
        db.collection('user_index').limit(1).get()
        return jsonify({"status": "success", "message": "Connected to Firestore!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == '__main__':
    # Use port from .env or default to 5001
    port = int(os.getenv("PORT", 5001))
    app.run(debug=True, port=port)

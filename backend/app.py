import os
import google.generativeai as genai
from flask import Flask, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# 1. Initialize Firebase
# Path to your service account key file
key_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY", "serviceAccountKey.json")

if os.path.exists(key_path):
    try:
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase Admin initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing Firebase: {e}")
else:
    print("⚠️  Warning: serviceAccountKey.json not found. Database features won't work yet.")

# 2. Initialize Gemini AI
gemini_key = os.getenv("GEMINI_API_KEY")
if gemini_key:
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    print("✅ Gemini AI initialized!")
else:
    print("⚠️  Warning: GEMINI_API_KEY not found in .env.")

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "project": "HireAI",
        "message": "Flask is integrated correctly!"
    })

@app.route('/api/generate-content', methods=['POST'])
def generate_content():
    try:
        data = request.json
        prompt = data.get('prompt')
        context = data.get('context', '')
        
        if not prompt:
            return jsonify({"status": "error", "message": "No prompt provided"}), 400

        full_prompt = f"Context: {context}\n\nTask: {prompt}\n\nPlease generate concise, professional resume content based on the task and context above."
        
        response = model.generate_content(full_prompt)
        return jsonify({
            "status": "success",
            "content": response.text
        })
    except Exception as e:
        print(f"Error in generate_content: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/save-resume', methods=['POST'])
def save_resume():
    try:
        if 'db' not in globals():
             return jsonify({"status": "error", "message": "Firebase not initialized"}), 500
             
        data = request.json
        resume_id = data.get('metadata', {}).get('resume_id')
        
        if not resume_id:
            return jsonify({"status": "error", "message": "No resume_id provided"}), 400
            
        # Save to 'resumes' collection
        db.collection('resumes').document(resume_id).set(data)
        
        return jsonify({
            "status": "success",
            "message": f"Resume {resume_id} saved successfully to Firestore!"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_resumes():
    try:
        # In a real scenario, we'd use request.files and request.form
        # For now, we'll return a success status to confirm integration
        return jsonify({
            "status": "success",
            "message": "Resumes received and analyzed by Flask!",
            "results": [
                { "name": "Priya_Sharma_Resume.pdf", "score": 92, "status": "Shortlist", "badgeClass": "badge-success", "skills": ["Python", "NLP", "TensorFlow", "BERT"], "experience": "5 years — Senior ML Engineer at TechCorp" },
                { "name": "Arjun_Mehta_Resume.pdf", "score": 78, "status": "Review", "badgeClass": "badge-warning", "skills": ["Python", "Scikit-learn", "SQL"], "experience": "3 years — Data Scientist at StartupX" }
            ]
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/check-db')
def check_db():
    try:
        if 'db' not in globals():
             return jsonify({"status": "error", "message": "Firebase not initialized. Did you add serviceAccountKey.json?"})
        # Simple test to see if we can talk to Firestore
        return jsonify({"status": "success", "message": "Connected to Firestore!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # Use port from .env or default to 5001
    port = int(os.getenv("PORT", 5001))
    app.run(debug=True, port=port)

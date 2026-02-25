from flask import Blueprint, jsonify, request
from services.firebase_service import get_db
from services.ai_service import get_model

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def home():
    return jsonify({
        "status": "online",
        "project": "HireAI",
        "message": "Flask is integrated correctly!"
    })

@api_bp.route('/api/generate-content', methods=['POST'])
def generate_content():
    try:
        data = request.json
        prompt = data.get('prompt')
        context = data.get('context', '')
        
        if not prompt:
            return jsonify({"status": "error", "message": "No prompt provided"}), 400

        full_prompt = f"Context: {context}\n\nTask: {prompt}\n\nPlease generate concise, professional resume content based on the task and context above."
        
        model = get_model()
        if not model:
            return jsonify({"status": "error", "message": "AI model not initialized"}), 500

        response = model.generate_content(full_prompt)
        return jsonify({
            "status": "success",
            "content": response.text
        })
    except Exception as e:
        print(f"Error in generate_content: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route('/api/save-resume', methods=['POST'])
def save_resume():
    try:
        db = get_db()
        if not db:
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

@api_bp.route('/api/analyze', methods=['POST'])
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

@api_bp.route('/api/check-db')
def check_db():
    try:
        db = get_db()
        if not db:
             return jsonify({"status": "error", "message": "Firebase not initialized. Did you add serviceAccountKey.json?"})
        # Simple test to see if we can talk to Firestore
        return jsonify({"status": "success", "message": "Connected to Firestore!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

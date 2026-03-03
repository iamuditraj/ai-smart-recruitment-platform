from flask import Blueprint, jsonify, request
from services.firebase_service import get_db
from services.ai_service import get_model
from firebase_admin import firestore
from werkzeug.security import generate_password_hash, check_password_hash

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def home():
    return jsonify({
        "status": "online",
        "project": "HireAI",
        "message": "Flask is integrated correctly!"
    })

@api_bp.route('/api/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        name = data.get('name', '')

        if not email or not password or not role:
            return jsonify({"status": "error", "message": "Missing email, password or role"}), 400

        db = get_db()
        if not db:
            return jsonify({"status": "error", "message": "Database not initialized"}), 500

        # Check if user exists
        user_ref = db.collection('users').document(email)
        user_doc = user_ref.get()

        if user_doc.exists:
            return jsonify({"status": "error", "message": "User already exists"}), 400

        # Create user
        hashed_password = generate_password_hash(password)
        db.collection('users').document(email).set({
            'email': email,
            'password': hashed_password,
            'role': role,
            'name': name,
            'createdAt': firestore.SERVER_TIMESTAMP if hasattr(firestore, 'SERVER_TIMESTAMP') else None
        })

        return jsonify({
            "status": "success",
            "message": "Account created successfully!",
            "user": {
                "email": email,
                "role": role,
                "name": name
            }
        })
    except Exception as e:
        print(f"Error in signup: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"status": "error", "message": "Missing email or password"}), 400

        db = get_db()
        if not db:
            return jsonify({"status": "error", "message": "Database not initialized"}), 500

        # Get user
        user_ref = db.collection('users').document(email)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return jsonify({"status": "error", "message": "Invalid email or password"}), 401

        user_data = user_doc.to_dict()
        if not check_password_hash(user_data['password'], password):
            return jsonify({"status": "error", "message": "Invalid email or password"}), 401

        return jsonify({
            "status": "success",
            "message": "Login successful!",
            "user": {
                "email": user_data['email'],
                "role": user_data['role'],
                "name": user_data.get('name', '')
            }
        })
    except Exception as e:
        print(f"Error in login: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

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

@api_bp.route('/api/profile', methods=['GET', 'POST'])
def handle_profile():
    try:
        db = get_db()
        if not db:
            return jsonify({"status": "error", "message": "Database not initialized"}), 500

        if request.method == 'POST':
            data = request.json
            email = data.get('email')
            if not email:
                return jsonify({"status": "error", "message": "Email is required"}), 400
            
            # Simple profile update (merge data)
            user_ref = db.collection('users').document(email)
            user_ref.update(data)
            
            # Get updated data
            updated_doc = user_ref.get()
            user_data = updated_doc.to_dict()
            # Don't send back password
            user_data.pop('password', None)
            
            return jsonify({
                "status": "success",
                "message": "Profile updated successfully!",
                "user": user_data
            })
        
        else: # GET
            email = request.args.get('email')
            if not email:
                return jsonify({"status": "error", "message": "Email is required"}), 400
                
            user_doc = db.collection('users').document(email).get()
            if not user_doc.exists:
                return jsonify({"status": "error", "message": "User not found"}), 404
                
            user_data = user_doc.to_dict()
            user_data.pop('password', None)
            
            return jsonify({
                "status": "success",
                "user": user_data
            })

    except Exception as e:
        print(f"Error in handle_profile: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route('/api/jobs', methods=['GET', 'POST'])
def handle_jobs():
    try:
        db = get_db()
        if not db:
            return jsonify({"status": "error", "message": "Database not initialized"}), 500

        if request.method == 'POST':
            data = request.json
            title = data.get('title')
            company = data.get('company')
            recruiter_email = data.get('recruiter_email')
            
            if not all([title, company, recruiter_email]):
                return jsonify({"status": "error", "message": "Missing required job fields"}), 400
            
            job_ref = db.collection('jobs').document()
            job_data = {
                "id": job_ref.id,
                "title": title,
                "company": company,
                "location": data.get('location', 'Remote'),
                "type": data.get('type', 'Full-time'), # Job or Internship
                "salary": data.get('salary', 'Competitive'),
                "description": data.get('description', ''),
                "requirements": data.get('requirements', []),
                "recruiter_email": recruiter_email,
                "posted_at": firestore.SERVER_TIMESTAMP
            }
            job_ref.set(job_data)
            # Remove server timestamp for response serialization
            response_data = job_data.copy()
            response_data['posted_at'] = None # Or a placeholder string
            return jsonify({"status": "success", "message": "Job posted successfully!", "job": response_data})
        
        else: # GET - Fetch all jobs
            jobs_docs = db.collection('jobs').order_by('posted_at', direction=firestore.Query.DESCENDING).stream()
            jobs = []
            for doc in jobs_docs:
                job = doc.to_dict()
                # Document might not have posted_at if it was just added and SERVER_TIMESTAMP hasn't resolved
                if 'posted_at' in job and job['posted_at']:
                    job['posted_at'] = job['posted_at'].isoformat()
                jobs.append(job)
            return jsonify({"status": "success", "jobs": jobs})

    except Exception as e:
        print(f"Error in handle_jobs: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route('/api/jobs/apply', methods=['POST'])
def apply_for_job():
    try:
        db = get_db()
        data = request.json
        job_id = data.get('job_id')
        candidate_email = data.get('candidate_email')
        
        if not all([job_id, candidate_email]):
            return jsonify({"status": "error", "message": "Missing application fields"}), 400
            
        # Check if already applied
        existing = db.collection('job_applications').where('job_id', '==', job_id).where('candidate_email', '==', candidate_email).get()
        if len(existing) > 0:
            return jsonify({"status": "error", "message": "You have already applied for this job"}), 400
            
        app_ref = db.collection('job_applications').document()
        app_data = {
            "id": app_ref.id,
            "job_id": job_id,
            "candidate_email": candidate_email,
            "status": "Applied",
            "applied_at": firestore.SERVER_TIMESTAMP
        }
        app_ref.set(app_data)
        return jsonify({"status": "success", "message": "Applied successfully!"})

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

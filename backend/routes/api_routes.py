from flask import Blueprint, jsonify, request
from services.firebase_service import get_db
from services.ai_service import get_model
from services.parser_service import extract_text
from firebase_admin import firestore
from werkzeug.security import generate_password_hash, check_password_hash
import io
import json
import re
import datetime

api_bp = Blueprint('api', __name__)

def _clean_json_response(text):
    """Helper to extract and parse JSON from Gemini markdown output."""
    try:
        # Match anything between triple backticks (```json or ```) or the whole text if no backticks
        match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
        if match:
            text = match.group(1)
        # Remove any leading/trailing whitespace
        text = text.strip()
        return json.loads(text)
    except Exception as e:
        print(f"Error parsing Gemini JSON: {e}\nRaw text: {text}")
        return None

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
        db = get_db() # Added to get Firestore access if needed
        model = get_model()
        if not model:
            return jsonify({"status": "error", "message": "AI model not initialized"}), 500

        # 1. Get Job Description and Resumes
        job_description = request.form.get('jobDescription', 'No JD provided')
        resumes = request.files.getlist('resumes')

        if not resumes:
            return jsonify({"status": "error", "message": "No resumes uploaded"}), 400

        parsed_results = []
        
        for file in resumes:
            # 2. Extract Text from file
            # Read into memory first to avoid file-system issues
            file_stream = io.BytesIO(file.read())
            extracted_text = extract_text(file_stream, file.filename)
            
            # 3. Prompt Gemini for matching
            prompt = f"""
            Task: Compare the following resume text against the Job Description (JD).
            
            JD: {job_description}
            
            Resume Text: {extracted_text}
            
            Respond STRICTLY with a JSON object containing:
            - name: The candidate's name (found in resume, if not found use filename: {file.filename})
            - score: A match percentage (0-100) based on JD requirements
            - status: One of "Shortlist" (score >= 80), "Review" (60-79), or "Reject" (<60)
            - badgeClass: One of "badge-success", "badge-warning", or "badge-danger" corresponding to status
            - skills: Top 4 technical skills found in resume
            - experience: A one-sentence summary (e.g., "5 years - Senior Dev at Google")
            - category: The most fitting job domain for this resume, one of: INFORMATION-TECHNOLOGY, FINANCE, HEALTHCARE, ENGINEERING, BUSINESS-DEVELOPMENT, HR, SALES, MARKETING, EDUCATION, LEGAL, or OTHER
            
            JSON only, no additional talk.
            """
            
            response = model.generate_content(prompt)
            data = _clean_json_response(response.text)
            
            if data:
                parsed_results.append(data)

                # 4. Auto-save to Firestore candidate_profiles collection
                if db:
                    try:
                        # Use sanitized filename as document ID
                        doc_id = re.sub(r'[^\w]', '_', file.filename)
                        db.collection('candidate_profiles').document(doc_id).set({
                            **data,
                            "source_file": file.filename,
                            "job_description": job_description[:300],  # store first 300 chars of JD
                            "analyzed_at": firestore.SERVER_TIMESTAMP
                        })
                    except Exception as save_err:
                        print(f"Warning: Could not save to Firestore: {save_err}")
            else:
                # Fallback if AI fails to format JSON correctly
                parsed_results.append({
                    "name": file.filename,
                    "score": 0,
                    "status": "Error",
                    "badgeClass": "badge-danger",
                    "skills": [],
                    "experience": "Could not parse analysis",
                    "category": "OTHER"
                })

        # 4. Sort by score descending
        parsed_results.sort(key=lambda x: x.get('score', 0), reverse=True)

        return jsonify({
            "status": "success",
            "message": f"Successfully analyzed {len(parsed_results)} resumes!",
            "results": parsed_results
        })
    except Exception as e:
        print(f"Error in analyze_resumes: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route('/api/generate-assessment', methods=['POST'])
def generate_assessment():
    try:
        model = get_model()
        if not model:
            return jsonify({"status": "error", "message": "AI model not initialized"}), 500

        data = request.json
        role_label = data.get('role', 'Generic Developer')
        
        prompt = f"""
        Generate a professional technical skill assessment for the role: {role_label}.
        
        Requirements:
        1. Create exactly 5 multiple-choice questions.
        2. Questions should range from basic to intermediate difficulty.
        3. Respond ONLY with a JSON array of objects, with this structure:
           [
             {{
               "text": "The question text?",
               "options": ["Option A", "Option B", "Option C", "Option D"],
               "correct": 1  // index of the correct option (0-3)
             }}
           ]
        
        JSON only. No Markdown, no explanations.
        """
        
        response = model.generate_content(prompt)
        questions = _clean_json_response(response.text)
        
        if not questions:
            return jsonify({"status": "error", "message": "Failed to generate AI questions"}), 500
            
        return jsonify({
            "status": "success",
            "questions": questions
        })
    except Exception as e:
        print(f"Error in generate_assessment: {e}")
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

@api_bp.route('/api/profile/upload-resume', methods=['POST'])
def upload_resume():
    try:
        import base64
        db = get_db()
        if not db:
            return jsonify({"status": "error", "message": "Firebase not initialized"}), 500

        email = request.form.get('email')
        if not email:
            return jsonify({"status": "error", "message": "Email is required"}), 400

        if 'resume' not in request.files:
            return jsonify({"status": "error", "message": "No resume file provided"}), 400

        file = request.files['resume']
        if file.filename == '':
            return jsonify({"status": "error", "message": "No selected file"}), 400

        if not file.filename.lower().endswith('.pdf'):
            return jsonify({"status": "error", "message": "Only PDF files are allowed"}), 400

        # Read file and convert to Base64
        file_bytes = file.read()
        
        # Check size limit for Firestore (1MB limit per document)
        # We leave some room for other metadata (max 900KB)
        if len(file_bytes) > 900 * 1024:
            return jsonify({
                "status": "error", 
                "message": "File too large for free tier storage (Max 900KB). Please compress your PDF or use a smaller file."
            }), 400

        encoded_string = base64.b64encode(file_bytes).decode('utf-8')
        resume_data_uri = f"data:application/pdf;base64,{encoded_string}"

        # --- Extract text and parse with Gemini ---
        parsed_resume = None
        try:
            file_stream = io.BytesIO(file_bytes)
            raw_text = extract_text(file_stream, file.filename)

            model = get_model()
            if model and raw_text:
                prompt = f"""
You are a resume parser. Extract all structured information from the resume text below.
Respond STRICTLY with a single JSON object (no markdown fences, no extra text) with these fields:
- name: string
- email: string
- phone: string
- summary: string (professional summary or objective)
- skills: array of strings
- experience: array of objects with keys: title, company, duration, description
- education: array of objects with keys: degree, institution, year
- certifications: array of strings
- languages: array of strings

If a field is not found, use an empty string or empty array as appropriate.

Resume Text:
{raw_text}
"""
                response = model.generate_content(prompt)
                parsed_resume = _clean_json_response(response.text)
                print(f"✅ Resume parsed successfully for {email}")
            else:
                print("⚠️  Skipping Gemini parse: model not ready or no text extracted.")
        except Exception as parse_err:
            print(f"⚠️  Could not parse resume with Gemini: {parse_err}")
            parsed_resume = None
        # --- End parse ---

        # Update user profile in Firestore
        user_ref = db.collection('users').document(email)
        user_ref.update({
            'resumeUrl': resume_data_uri,
            'resumeName': file.filename,
            'parsedResume': parsed_resume,
            'updatedAt': firestore.SERVER_TIMESTAMP
        })

        return jsonify({
            "status": "success",
            "message": "Resume saved successfully to profile!",
            "resumeUrl": resume_data_uri,
            "resumeName": file.filename,
            "parsedResume": parsed_resume
        })

    except Exception as e:
        import traceback
        print(f"Error in upload_resume: {e}")
        traceback.print_exc()
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
                return jsonify({"status": "error", "message": "Missing required job fields: title, company, or recruiter_email"}), 400
            
            job_ref = db.collection('jobs').document()
            job_data = {
                "id": job_ref.id,
                "title": title,
                "company": company,
                "department": data.get('department', ''),
                "location": data.get('location', 'Remote'),
                "workArrangement": data.get('workArrangement', 'Remote'),
                "type": data.get('type', 'Full-time'),
                "experienceLevel": data.get('experienceLevel', 'Mid-Level'),
                "salary": data.get('salary', 'Competitive'),
                "companyOverview": data.get('companyOverview', ''),
                "jobSummary": data.get('jobSummary', ''),
                "keyResponsibilities": data.get('keyResponsibilities', ''),
                "requiredSkills": data.get('requiredSkills', ''),
                "softSkills": data.get('softSkills', ''),
                "educationalBackground": data.get('educationalBackground', ''),
                "preferredQualifications": data.get('preferredQualifications', ''),
                "applicationDeadline": data.get('applicationDeadline', ''),
                "requiredDocumentsList": data.get('requiredDocumentsList', []),
                "recruiter_email": recruiter_email,
                "posted_at": firestore.SERVER_TIMESTAMP
            }
            job_ref.set(job_data)
            # Remove server timestamp for response serialization
            response_data = job_data.copy()
            response_data['posted_at'] = None # Or a placeholder string
            return jsonify({"status": "success", "message": "Job posted successfully!", "job": response_data})
        
        else: # GET - Fetch jobs
            recruiter_email = request.args.get('recruiter_email')
            if recruiter_email:
                # Removed order_by here to avoid requiring a composite index in Firestore
                jobs_docs = db.collection('jobs').where('recruiter_email', '==', recruiter_email).stream()
            else:
                jobs_docs = db.collection('jobs').order_by('posted_at', direction=firestore.Query.DESCENDING).stream()
                
            jobs = []
            for doc in jobs_docs:
                job = doc.to_dict()
                # Document might not have posted_at if it was just added and SERVER_TIMESTAMP hasn't resolved
                if 'posted_at' in job and job['posted_at']:
                    job['posted_at'] = job['posted_at'].isoformat()
                jobs.append(job)
                
            # Sort manually if we didn't use Native Firestore sorting
            if recruiter_email:
                jobs.sort(key=lambda x: x.get('posted_at') or '', reverse=True)
                
            return jsonify({"status": "success", "jobs": jobs})

    except Exception as e:
        print(f"Error in handle_jobs: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route('/api/jobs/<job_id>', methods=['PUT', 'DELETE', 'GET'])
def handle_specific_job(job_id):
    try:
        db = get_db()
        if not db:
            return jsonify({"status": "error", "message": "Database not initialized"}), 500

        job_ref = db.collection('jobs').document(job_id)
        job_doc = job_ref.get()

        if not job_doc.exists:
            return jsonify({"status": "error", "message": "Job not found"}), 404

        if request.method == 'GET':
            job = job_doc.to_dict()
            if 'posted_at' in job and job['posted_at']:
                job['posted_at'] = job['posted_at'].isoformat()
            return jsonify({"status": "success", "job": job})

        if request.method == 'DELETE':
            # Also optionally check if recruiter owns the job here
            # recruiter_email = request.args.get('recruiter_email')
            job_ref.delete()
            return jsonify({"status": "success", "message": "Job deleted successfully"})

        if request.method == 'PUT':
            data = request.json
            
            # Fields that can be updated
            update_data = {
                "title": data.get('title'),
                "company": data.get('company'),
                "department": data.get('department'),
                "location": data.get('location'),
                "workArrangement": data.get('workArrangement'),
                "type": data.get('type'),
                "experienceLevel": data.get('experienceLevel'),
                "salary": data.get('salary'),
                "companyOverview": data.get('companyOverview'),
                "jobSummary": data.get('jobSummary'),
                "keyResponsibilities": data.get('keyResponsibilities'),
                "requiredSkills": data.get('requiredSkills'),
                "softSkills": data.get('softSkills'),
                "educationalBackground": data.get('educationalBackground'),
                "preferredQualifications": data.get('preferredQualifications'),
                "applicationDeadline": data.get('applicationDeadline'),
                "requiredDocumentsList": data.get('requiredDocumentsList'),
            }
            # Remove None values so we don't overwrite with nulls if a field is omitted
            update_data = {k: v for k, v in update_data.items() if v is not None}
            update_data['updated_at'] = firestore.SERVER_TIMESTAMP

            job_ref.update(update_data)
            return jsonify({"status": "success", "message": "Job updated successfully"})

    except Exception as e:
        print(f"Error in handle_specific_job: {e}")
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

@api_bp.route('/api/recruiter/applications', methods=['GET'])
def get_recruiter_applications():
    try:
        db = get_db()
        recruiter_email = request.args.get('email')
        if not recruiter_email:
            return jsonify({"status": "error", "message": "Recruiter email is required"}), 400

        # 1. Get all job IDs belonging to this recruiter
        jobs_docs = db.collection('jobs').where('recruiter_email', '==', recruiter_email).get()
        job_ids = [doc.id for doc in jobs_docs]

        if not job_ids:
            return jsonify({"status": "success", "applications": []})

        # 2. Get all applications for these jobs
        # Firestore 'in' query has a limit of 10 items. For simplicity, we fetch all and filter or loop.
        # Here we loop through job_ids since it's likely small for a MVP
        all_apps = []
        for j_id in job_ids:
            apps = db.collection('job_applications').where('job_id', '==', j_id).get()
            for app_doc in apps:
                app_data = app_doc.to_dict()
                
                # Fetch candidate profile to get name and resume
                c_email = app_data.get('candidate_email')
                user_doc = db.collection('users').document(c_email).get()
                if user_doc.exists:
                    user_data = user_doc.to_dict()
                    app_data['candidate_name'] = user_data.get('name', 'Unknown')
                    app_data['resumeUrl'] = user_data.get('resumeUrl')
                    app_data['resumeName'] = user_data.get('resumeName')
                    app_data['experience'] = user_data.get('bio', '') # Using bio as teaser experience
                
                if 'applied_at' in app_data and app_data['applied_at']:
                    app_data['applied_at'] = app_data['applied_at'].isoformat()
                
                all_apps.append(app_data)

        return jsonify({
            "status": "success",
            "applications": all_apps
        })

    except Exception as e:
        print(f"Error in get_recruiter_applications: {e}")
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

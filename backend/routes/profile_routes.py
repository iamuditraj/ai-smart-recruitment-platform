from flask import Blueprint, jsonify, request
from services.firebase_service import get_db
from firebase_admin import firestore
import datetime
import base64
import io
import json

from services.db_helpers import get_user_collection, serialize_timestamps
from services.ai_service import get_model, MODEL
from services.parser_service import extract_text

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/api/profile', methods=['GET', 'POST'])
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
            
            user_role, collection_name = get_user_collection(db, email)
            if not user_role:
                return jsonify({"status": "error", "message": "User not found"}), 404
                
            user_ref = db.collection(collection_name).document(email)
            user_ref.update(data)
            
            updated_doc = user_ref.get()
            user_data = updated_doc.to_dict()
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
                
            user_role, collection_name = get_user_collection(db, email)
            if not user_role:
                return jsonify({"status": "error", "message": "User not found"}), 404
                
            user_doc = db.collection(collection_name).document(email).get()
                
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

@profile_bp.route('/api/profile/upload-resume', methods=['POST'])
def upload_resume():
    try:
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

        file_bytes = file.read()
        
        if len(file_bytes) > 900 * 1024:
            return jsonify({
                "status": "error", 
                "message": "File too large for free tier storage (Max 900KB). Please compress your PDF or use a smaller file."
            }), 400

        encoded_string = base64.b64encode(file_bytes).decode('utf-8')
        resume_data_uri = f"data:application/pdf;base64,{encoded_string}"

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
                response = model.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    response_format={"type": "json_object"}
                )
                parsed_resume = json.loads(response.choices[0].message.content)
                print(f"✅ Resume parsed successfully for {email}")
            else:
                print("⚠️  Skipping Groq parse: model not ready or no text extracted.")
        except Exception as parse_err:
            print(f"⚠️  Could not parse resume with Groq: {parse_err}")
            parsed_resume = None

        user_ref = db.collection('candidates').document(email)
        
        is_default = len(list(user_ref.collection('resumes').stream())) == 0
        resume_id = str(datetime.datetime.utcnow().timestamp()).replace('.', '')
        
        new_resume = {
            'id': resume_id,
            'resumeUrl': resume_data_uri,
            'resumeName': file.filename,
            'type': 'uploaded',
            'parsedResume': parsed_resume,
            'isDefault': is_default,
            'uploadedAt': datetime.datetime.utcnow().isoformat()
        }
        
        user_ref.collection('resumes').document(resume_id).set(new_resume)
        
        if is_default:
            update_data = {
                'defaultResumeId': resume_id,
                'resumeUrl': resume_data_uri,
                'resumeName': file.filename,
                'updatedAt': firestore.SERVER_TIMESTAMP
            }
            if parsed_resume:
                update_data['parsedResume'] = parsed_resume
            user_ref.update(update_data)

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

@profile_bp.route('/api/profile/set-default-resume', methods=['POST'])
def set_default_resume():
    try:
        db = get_db()
        data = request.json
        email = data.get('email')
        resume_id = data.get('resume_id')
        
        if not email or not resume_id:
            return jsonify({"status": "error", "message": "Email and resume_id are required"}), 400
            
        user_ref = db.collection('candidates').document(email)
        doc = user_ref.get()
        
        if not doc.exists:
            return jsonify({"status": "error", "message": "User not found"}), 404
            
        all_resumes = list(user_ref.collection('resumes').stream())
        matched_resume = None
        
        for r_doc in all_resumes:
            r_data = r_doc.to_dict()
            is_match = (
                str(r_doc.id) == str(resume_id) or
                str(r_data.get('resume_id', '')) == str(resume_id) or
                str(r_data.get('uploadedAt', '')) == str(resume_id)
            )
            r_doc.reference.update({'isDefault': is_match})
            if is_match:
                matched_resume = r_data

        if not matched_resume:
            return jsonify({"status": "error", "message": "Resume not found in your profile"}), 404

        update_data = {
            'defaultResumeId': resume_id,
            'resumeName': matched_resume.get('resumeName', 'Default Resume'),
            'updatedAt': firestore.SERVER_TIMESTAMP
        }

        resume_url = matched_resume.get('resumeUrl')
        if resume_url:
            update_data['resumeUrl'] = resume_url

        parsed = matched_resume.get('parsedResume')
        if parsed:
            update_data['parsedResume'] = parsed

        user_ref.update(update_data)

        return jsonify({"status": "success", "message": "Default resume updated successfully!"})
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error in set_default_resume: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@profile_bp.route('/api/profile/resumes', methods=['GET'])
def get_resumes():
    try:
        db = get_db()
        email = request.args.get('email')
        if not email:
            return jsonify({"status": "error", "message": "Email is required"}), 400
        resumes_ref = db.collection('candidates').document(email).collection('resumes').stream()
        resumes = []
        for doc in resumes_ref:
            r = doc.to_dict()
            r['id'] = doc.id
            r = serialize_timestamps(r)
            resumes.append(r)
        resumes.sort(key=lambda x: x.get('uploadedAt', ''), reverse=True)
        return jsonify({"status": "success", "resumes": resumes})
    except Exception as e:
        print(f"Error in get_resumes: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

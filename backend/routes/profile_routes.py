from flask import Blueprint, g, jsonify, request
import datetime
import base64
import io

from routes.decorators import handle_route_errors, require_db
from services.db_helpers import get_user_collection, serialize_timestamps, save_resume_to_profile
from services.ai_service import parse_resume
from services.parser_service import extract_text

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/api/profile', methods=['GET', 'POST'])
@handle_route_errors
@require_db
def handle_profile():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        if not email:
            return jsonify({"status": "error", "message": "Email is required"}), 400
        
        user_role, collection_name = get_user_collection(g.db, email)
        if not user_role:
            return jsonify({"status": "error", "message": "User not found"}), 404
            
        user_ref = g.db.collection(collection_name).document(email)
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
            
        user_role, collection_name = get_user_collection(g.db, email)
        if not user_role:
            return jsonify({"status": "error", "message": "User not found"}), 404
            
        user_doc = g.db.collection(collection_name).document(email).get()
            
        if not user_doc.exists:
            return jsonify({"status": "error", "message": "User not found"}), 404
            
        user_data = user_doc.to_dict()
        user_data.pop('password', None)
        
        return jsonify({
            "status": "success",
            "user": user_data
        })

@profile_bp.route('/api/profile/upload-resume', methods=['POST'])
@handle_route_errors
@require_db
def upload_resume():
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

    # --- HP-3: Parse resume via centralised AI service ---
    parsed_resume = None
    try:
        file_stream = io.BytesIO(file_bytes)
        raw_text = extract_text(file_stream, file.filename)
        if raw_text:
            result = parse_resume(raw_text)
            # _run_inference returns a fallback dict when AI is unavailable;
            # only keep the result if it looks like a real parse
            if result.get('name') or result.get('skills'):
                parsed_resume = result
                print(f"✅ Resume parsed successfully for {email}")
            else:
                print("⚠️  AI returned empty result — skipping parsed resume.")
        else:
            print("⚠️  No text extracted from resume.")
    except Exception as parse_err:
        print(f"⚠️  Could not parse resume: {parse_err}")
        parsed_resume = None

    # --- HP-4: Save resume via centralised helper ---
    resume_id = str(datetime.datetime.utcnow().timestamp()).replace('.', '')
    resume_doc = {
        'id': resume_id,
        'resumeUrl': resume_data_uri,
        'resumeName': file.filename,
        'type': 'uploaded',
        'parsedResume': parsed_resume,
    }
    parent_extras = {
        'resumeUrl': resume_data_uri,
        'resumeName': file.filename,
    }
    if parsed_resume:
        parent_extras['parsedResume'] = parsed_resume

    save_resume_to_profile(g.db, email, resume_id, resume_doc, parent_extras)

    return jsonify({
        "status": "success",
        "message": "Resume saved successfully to profile!",
        "resumeUrl": resume_data_uri,
        "resumeName": file.filename,
        "parsedResume": parsed_resume
    })

@profile_bp.route('/api/profile/set-default-resume', methods=['POST'])
@handle_route_errors
@require_db
def set_default_resume():
    data = request.json
    email = data.get('email')
    resume_id = data.get('resume_id')
    
    if not email or not resume_id:
        return jsonify({"status": "error", "message": "Email and resume_id are required"}), 400
        
    user_ref = g.db.collection('candidates').document(email)
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

@profile_bp.route('/api/profile/resumes', methods=['GET'])
@handle_route_errors
@require_db
def get_resumes():
    email = request.args.get('email')
    if not email:
        return jsonify({"status": "error", "message": "Email is required"}), 400
    resumes_ref = g.db.collection('candidates').document(email).collection('resumes').stream()
    resumes = []
    for doc in resumes_ref:
        r = doc.to_dict()
        r['id'] = doc.id
        r = serialize_timestamps(r)
        resumes.append(r)
    resumes.sort(key=lambda x: x.get('uploadedAt', ''), reverse=True)
    return jsonify({"status": "success", "resumes": resumes})

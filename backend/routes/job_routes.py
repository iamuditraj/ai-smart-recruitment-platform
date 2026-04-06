from flask import Blueprint, jsonify, request
from services.firebase_service import get_db
from firebase_admin import firestore
import json
import io

from services.db_helpers import serialize_timestamps, build_ats_pipeline
from services.ai_service import parse_job_description

job_bp = Blueprint('job', __name__)

def _build_jd_from_job(job_data: dict) -> tuple:
    """Build full JD text from a Firestore job document and parse it with Groq.
    
    Returns (jd_text, parsed_jd) where parsed_jd is the LLM-structured dict
    """
    parts = []
    for field in ['title', 'jobSummary', 'description', 'keyResponsibilities',
                  'requiredSkills', 'softSkills', 'preferredQualifications',
                  'educationalBackground', 'experienceLevel', 'companyOverview']:
        val = job_data.get(field, '')
        if val:
            parts.append(f"{field}: {val}")
    jd_text = "\n".join(parts)

    parsed_jd = parse_job_description(jd_text)
    return jd_text, parsed_jd

@job_bp.route('/api/jobs', methods=['GET', 'POST'])
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
            response_data = job_data.copy()
            response_data['posted_at'] = None 
            return jsonify({"status": "success", "message": "Job posted successfully!", "job": response_data})
        
        else: # GET
            recruiter_email = request.args.get('recruiter_email')
            if recruiter_email:
                jobs_docs = db.collection('jobs').where('recruiter_email', '==', recruiter_email).stream()
            else:
                jobs_docs = db.collection('jobs').order_by('posted_at', direction=firestore.Query.DESCENDING).stream()
                
            jobs = []
            for doc in jobs_docs:
                job = doc.to_dict()
                job = serialize_timestamps(job)
                jobs.append(job)
                
            if recruiter_email:
                jobs.sort(key=lambda x: x.get('posted_at') or '', reverse=True)
                
            return jsonify({"status": "success", "jobs": jobs})

    except Exception as e:
        print(f"Error in handle_jobs: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@job_bp.route('/api/jobs/<job_id>', methods=['PUT', 'DELETE', 'GET'])
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
            job = serialize_timestamps(job)
            return jsonify({"status": "success", "job": job})

        if request.method == 'DELETE':
            job_ref.delete()
            return jsonify({"status": "success", "message": "Job deleted successfully"})

        if request.method == 'PUT':
            data = request.json
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
            update_data = {k: v for k, v in update_data.items() if v is not None}
            update_data['updated_at'] = firestore.SERVER_TIMESTAMP

            job_ref.update(update_data)
            return jsonify({"status": "success", "message": "Job updated successfully"})

    except Exception as e:
        print(f"Error in handle_specific_job: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@job_bp.route('/api/jobs/preview_score', methods=['POST'])
def preview_score():
    try:
        db = get_db()
        job_id = request.form.get('job_id')
        resume_file = request.files.get('resume')
        
        if not all([job_id, resume_file]):
            return jsonify({"status": "error", "message": "Missing job_id or resume file"}), 400
            
        job_doc = db.collection('jobs').document(job_id).get()
        if not job_doc.exists:
            return jsonify({"status": "error", "message": "Job not found"}), 404
            
        job_data = job_doc.to_dict()
        jd_text, parsed_jd = _build_jd_from_job(job_data)
        
        ats_result, llm_parsed_resume = build_ats_pipeline(resume_file, jd_text, parsed_jd)
        
        return jsonify({
            "status": "success",
            "message": "Preview generated successfully!",
            "ats_result": ats_result,
            "llm_parsed_resume": llm_parsed_resume
        })
    except Exception as e:
        print(f"Error previewing score: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@job_bp.route('/api/jobs/apply', methods=['POST'])
def apply_for_job():
    try:
        db = get_db()
        job_id = request.form.get('job_id')
        candidate_email = request.form.get('candidate_email')
        resume_file = request.files.get('resume')
        
        if not all([job_id, candidate_email, resume_file]):
            return jsonify({"status": "error", "message": "Missing application fields or resume file"}), 400
            
        existing = db.collection('jobs').document(job_id).collection('applications').where('candidate_email', '==', candidate_email).get()
        if len(existing) > 0:
            return jsonify({"status": "error", "message": "You have already applied for this job"}), 400
            
        job_doc = db.collection('jobs').document(job_id).get()
        if not job_doc.exists:
            return jsonify({"status": "error", "message": "Job not found"}), 404
            
        job_data = job_doc.to_dict()
        jd_text, parsed_jd = _build_jd_from_job(job_data)
        
        pre_ats_result_raw = request.form.get('ats_result')
        pre_parsed_resume_raw = request.form.get('llm_parsed_resume')
        
        ats_result = None
        llm_parsed_resume = None
        
        if pre_ats_result_raw:
            try:
                ats_result = json.loads(pre_ats_result_raw)
            except Exception as parse_e:
                print(f"Error parsing precomputed ATS data: {parse_e}")
                
        if pre_parsed_resume_raw:
            try:
                llm_parsed_resume = json.loads(pre_parsed_resume_raw)
            except Exception as parse_e:
                print(f"Error parsing precomputed resume data: {parse_e}")

        if not ats_result or not llm_parsed_resume:
            # Dual-path behavior: The Vue frontend sends precomputed values to save processing time.
            # However, test scripts (like apply_candidates.py) and external API calls might not.
            # If missing, we fallback to running the ATS pipeline locally here.
            ats_result, llm_parsed_resume = build_ats_pipeline(resume_file, jd_text, parsed_jd)
            
        app_ref = db.collection('jobs').document(job_id).collection('applications').document()
        app_data = {
            "id": app_ref.id,
            "job_id": job_id,
            "candidate_email": candidate_email,
            "status": "Applied",
            "applied_at": firestore.SERVER_TIMESTAMP,
            "ats_score": ats_result.get("score", 0),
            "ats_badge": ats_result.get("badgeClass", "badge-warning"),
            "score_breakdown": ats_result.get("score_breakdown", {}),
            "matched_skills": ats_result.get("matched_skills", []),
            "missing_skills": ats_result.get("key_gaps", []),
            "resume_filename": resume_file.filename,
            "parsedResume": llm_parsed_resume 
        }
        app_ref.set(app_data)

        try:
            db.collection('candidates').document(candidate_email).update({
                "parsedResume": llm_parsed_resume,
                "resumeName": resume_file.filename,
                "updatedAt": firestore.SERVER_TIMESTAMP
            })
        except Exception as update_e:
            print(f"Non-critical error updating candidate profile: {update_e}")
        
        return jsonify({
            "status": "success", 
            "message": "Applied successfully!",
            "ats_score": app_data["ats_score"]
        })

    except Exception as e:
        print(f"Error applying for job: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@job_bp.route('/api/jobs/<job_id>/applications', methods=['GET'])
def get_job_applications(job_id):
    try:
        db = get_db()
        if not db:
            return jsonify({"status": "error", "message": "Database not initialized"}), 500

        job_doc = db.collection('jobs').document(job_id).get()
        if not job_doc.exists:
            return jsonify({"status": "error", "message": "Job not found"}), 404

        job_data = job_doc.to_dict()

        apps = db.collection('jobs').document(job_id).collection('applications').stream()
        all_apps = []
        for app_doc in apps:
            app_data = app_doc.to_dict()

            c_email = app_data.get('candidate_email')
            if c_email:
                user_doc = db.collection('candidates').document(c_email).get()
                if user_doc.exists:
                    user_data = user_doc.to_dict()
                    app_data['candidate_name'] = user_data.get('name', c_email.split('@')[0])
                    if not app_data.get('parsedResume'):
                        app_data['parsedResume'] = user_data.get('parsedResume')
                else:
                    if not app_data.get('candidate_name'):
                        app_data['candidate_name'] = c_email.split('@')[0]

            app_data = serialize_timestamps(app_data)
            all_apps.append(app_data)

        all_apps.sort(key=lambda x: x.get('ats_score', 0), reverse=True)

        return jsonify({
            "status": "success",
            "job_title": job_data.get('title', 'Unknown Job'),
            "job_id": job_id,
            "applications": all_apps
        })

    except Exception as e:
        print(f"Error in get_job_applications: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@job_bp.route('/api/jobs/<job_id>/applications/<app_id>/status', methods=['PATCH'])
def update_application_status(job_id, app_id):
    try:
        db = get_db()
        if not db:
            return jsonify({"status": "error", "message": "Database not initialized"}), 500

        data = request.json
        new_status = data.get('status')
        if new_status not in ('Shortlisted', 'Rejected', 'Applied'):
            return jsonify({"status": "error", "message": "Invalid status. Use Shortlisted, Rejected, or Applied."}), 400

        app_ref = db.collection('jobs').document(job_id).collection('applications').document(app_id)
        app_doc = app_ref.get()
        if not app_doc.exists:
            return jsonify({"status": "error", "message": "Application not found"}), 404

        app_ref.update({"status": new_status})

        return jsonify({
            "status": "success",
            "message": f"Application status updated to {new_status}",
            "new_status": new_status
        })

    except Exception as e:
        print(f"Error in update_application_status: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@job_bp.route('/api/jobs/<job_id>/applications/bulk-status', methods=['PATCH'])
def bulk_update_application_status(job_id):
    try:
        db = get_db()
        if not db:
            return jsonify({"status": "error", "message": "Database not initialized"}), 500

        data = request.json
        action = data.get('action')       
        threshold = data.get('threshold')  
        direction = data.get('direction')  

        if action not in ('approve', 'reject'):
            return jsonify({"status": "error", "message": "action must be 'approve' or 'reject'"}), 400
        if direction not in ('above', 'below'):
            return jsonify({"status": "error", "message": "direction must be 'above' or 'below'"}), 400
        if threshold is None or not isinstance(threshold, (int, float)):
            return jsonify({"status": "error", "message": "threshold must be a number"}), 400

        new_status = 'Shortlisted' if action == 'approve' else 'Rejected'

        apps = db.collection('jobs').document(job_id).collection('applications').stream()
        updated_count = 0
        for app_doc in apps:
            app_data = app_doc.to_dict()
            score = app_data.get('ats_score', 0)

            matches = (direction == 'above' and score >= threshold) or \
                      (direction == 'below' and score < threshold)

            if matches:
                app_doc.reference.update({"status": new_status})
                updated_count += 1

        return jsonify({
            "status": "success",
            "message": f"{updated_count} applications updated to {new_status}",
            "updated_count": updated_count
        })

    except Exception as e:
        print(f"Error in bulk_update_application_status: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

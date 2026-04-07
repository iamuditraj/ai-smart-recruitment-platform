from flask import Blueprint, g, jsonify, request
from firebase_admin import firestore
import json

from routes.decorators import handle_route_errors, require_db
from services.db_helpers import (
    serialize_timestamps, build_ats_pipeline,
    get_job_with_parsed_jd, enrich_app_with_candidate,
)

job_bp = Blueprint('job', __name__)

# ── MP-4: Single source of truth for editable job fields ──────────────────
_JOB_EDITABLE_FIELDS = [
    'title', 'company', 'department', 'location', 'workArrangement', 'type',
    'experienceLevel', 'salary', 'companyOverview', 'jobSummary',
    'keyResponsibilities', 'requiredSkills', 'softSkills',
    'educationalBackground', 'preferredQualifications',
    'applicationDeadline', 'requiredDocumentsList',
]

_JOB_DEFAULTS = {
    'department': '', 'location': 'Remote', 'workArrangement': 'Remote',
    'type': 'Full-time', 'experienceLevel': 'Mid-Level', 'salary': 'Competitive',
    'companyOverview': '', 'jobSummary': '', 'keyResponsibilities': '',
    'requiredSkills': '', 'softSkills': '', 'educationalBackground': '',
    'preferredQualifications': '', 'applicationDeadline': '',
    'requiredDocumentsList': [],
}

@job_bp.route('/api/jobs', methods=['GET', 'POST'])
@handle_route_errors
@require_db
def handle_jobs():
    if request.method == 'POST':
        data = request.json
        title = data.get('title')
        company = data.get('company')
        recruiter_email = data.get('recruiter_email')
        
        if not all([title, company, recruiter_email]):
            return jsonify({"status": "error", "message": "Missing required job fields: title, company, or recruiter_email"}), 400
        
        job_ref = g.db.collection('jobs').document()
        job_data = {"id": job_ref.id, "recruiter_email": recruiter_email, "posted_at": firestore.SERVER_TIMESTAMP}
        for field in _JOB_EDITABLE_FIELDS:
            job_data[field] = data.get(field, _JOB_DEFAULTS.get(field))

        job_ref.set(job_data)
        response_data = job_data.copy()
        response_data['posted_at'] = None 
        return jsonify({"status": "success", "message": "Job posted successfully!", "job": response_data})
    
    else: # GET
        recruiter_email = request.args.get('recruiter_email')
        if recruiter_email:
            jobs_docs = g.db.collection('jobs').where('recruiter_email', '==', recruiter_email).stream()
        else:
            jobs_docs = g.db.collection('jobs').order_by('posted_at', direction=firestore.Query.DESCENDING).stream()
            
        jobs = []
        for doc in jobs_docs:
            job = doc.to_dict()
            job = serialize_timestamps(job)
            jobs.append(job)
            
        if recruiter_email:
            jobs.sort(key=lambda x: x.get('posted_at') or '', reverse=True)
            
        return jsonify({"status": "success", "jobs": jobs})

@job_bp.route('/api/jobs/<job_id>', methods=['PUT', 'DELETE', 'GET'])
@handle_route_errors
@require_db
def handle_specific_job(job_id):
    job_ref = g.db.collection('jobs').document(job_id)
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
        update_data = {field: data.get(field) for field in _JOB_EDITABLE_FIELDS}
        update_data = {k: v for k, v in update_data.items() if v is not None}
        update_data['updated_at'] = firestore.SERVER_TIMESTAMP

        job_ref.update(update_data)
        return jsonify({"status": "success", "message": "Job updated successfully"})

@job_bp.route('/api/jobs/preview_score', methods=['POST'])
@handle_route_errors
@require_db
def preview_score():
    job_id = request.form.get('job_id')
    resume_file = request.files.get('resume')
    
    if not all([job_id, resume_file]):
        return jsonify({"status": "error", "message": "Missing job_id or resume file"}), 400

    job_data, jd_text, parsed_jd = get_job_with_parsed_jd(g.db, job_id)
    if not job_data:
        return jsonify({"status": "error", "message": "Job not found"}), 404
    
    ats_result, llm_parsed_resume = build_ats_pipeline(resume_file, jd_text, parsed_jd)
    
    return jsonify({
        "status": "success",
        "message": "Preview generated successfully!",
        "ats_result": ats_result,
        "llm_parsed_resume": llm_parsed_resume
    })

@job_bp.route('/api/jobs/apply', methods=['POST'])
@handle_route_errors
@require_db
def apply_for_job():
    job_id = request.form.get('job_id')
    candidate_email = request.form.get('candidate_email')
    resume_file = request.files.get('resume')
    
    if not all([job_id, candidate_email, resume_file]):
        return jsonify({"status": "error", "message": "Missing application fields or resume file"}), 400
        
    existing = g.db.collection('jobs').document(job_id).collection('applications').where('candidate_email', '==', candidate_email).get()
    if len(existing) > 0:
        return jsonify({"status": "error", "message": "You have already applied for this job"}), 400

    job_data, jd_text, parsed_jd = get_job_with_parsed_jd(g.db, job_id)
    if not job_data:
        return jsonify({"status": "error", "message": "Job not found"}), 404
    
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
        
    app_ref = g.db.collection('jobs').document(job_id).collection('applications').document()
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
        g.db.collection('candidates').document(candidate_email).update({
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

@job_bp.route('/api/jobs/<job_id>/applications', methods=['GET'])
@handle_route_errors
@require_db
def get_job_applications(job_id):
    job_doc = g.db.collection('jobs').document(job_id).get()
    if not job_doc.exists:
        return jsonify({"status": "error", "message": "Job not found"}), 404

    job_data = job_doc.to_dict()

    apps = g.db.collection('jobs').document(job_id).collection('applications').stream()
    all_apps = []
    for app_doc in apps:
        app_data = app_doc.to_dict()
        enrich_app_with_candidate(g.db, app_data)
        app_data = serialize_timestamps(app_data)
        all_apps.append(app_data)

    all_apps.sort(key=lambda x: x.get('ats_score', 0), reverse=True)

    return jsonify({
        "status": "success",
        "job_title": job_data.get('title', 'Unknown Job'),
        "job_id": job_id,
        "applications": all_apps
    })

@job_bp.route('/api/jobs/<job_id>/applications/<app_id>/status', methods=['PATCH'])
@handle_route_errors
@require_db
def update_application_status(job_id, app_id):
    data = request.json
    new_status = data.get('status')
    if new_status not in ('Shortlisted', 'Rejected', 'Applied'):
        return jsonify({"status": "error", "message": "Invalid status. Use Shortlisted, Rejected, or Applied."}), 400

    app_ref = g.db.collection('jobs').document(job_id).collection('applications').document(app_id)
    app_doc = app_ref.get()
    if not app_doc.exists:
        return jsonify({"status": "error", "message": "Application not found"}), 404

    app_ref.update({"status": new_status})

    return jsonify({
        "status": "success",
        "message": f"Application status updated to {new_status}",
        "new_status": new_status
    })

@job_bp.route('/api/jobs/<job_id>/applications/bulk-status', methods=['PATCH'])
@handle_route_errors
@require_db
def bulk_update_application_status(job_id):
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

    apps = g.db.collection('jobs').document(job_id).collection('applications').stream()
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

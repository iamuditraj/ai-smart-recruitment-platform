from flask import Blueprint, g, jsonify, request
from routes.decorators import handle_route_errors, require_db
from services.db_helpers import serialize_timestamps

candidate_bp = Blueprint('candidate', __name__)

@candidate_bp.route('/api/candidate/applications', methods=['GET'])
@handle_route_errors
@require_db
def get_candidate_applications():
    """Return every application a candidate has submitted, enriched with job info."""
    candidate_email = request.args.get('email')
    if not candidate_email:
        return jsonify({"status": "error", "message": "Candidate email is required"}), 400

    # We need to scan all jobs for applications by this candidate.
    # For MVP scale this is acceptable; at scale use a top-level applications collection.
    jobs_stream = g.db.collection('jobs').stream()
    all_apps = []

    for job_doc in jobs_stream:
        job_data = job_doc.to_dict()
        apps = (g.db.collection('jobs').document(job_doc.id)
                  .collection('applications')
                  .where('candidate_email', '==', candidate_email)
                  .stream())

        for app_doc in apps:
            app_data = app_doc.to_dict()
            # Enrich with job metadata
            app_data['job_title'] = job_data.get('title', 'Unknown')
            app_data['company'] = job_data.get('company', '')
            app_data['location'] = job_data.get('location', '')
            app_data['job_type'] = job_data.get('type', '')
            app_data['job_rounds'] = job_data.get('rounds', [])
            app_data['job_current_round_index'] = job_data.get('current_round_index', 0)

            if app_data.get('status') in ['Shortlisted', 'Hired']:
                app_data['recruiter_email'] = job_data.get('recruiter_email', '')

            app_data = serialize_timestamps(app_data)
            all_apps.append(app_data)

    # Sort newest first
    all_apps.sort(key=lambda x: x.get('applied_at', ''), reverse=True)

    return jsonify({"status": "success", "applications": all_apps})

@candidate_bp.route('/api/candidate/applied-jobs', methods=['GET'])
@handle_route_errors
@require_db
def get_candidate_applied_jobs():
    """Return the set of job IDs a candidate has already applied to (for quick UI checks)."""
    candidate_email = request.args.get('email')
    if not candidate_email:
        return jsonify({"status": "error", "message": "Candidate email is required"}), 400

    jobs_stream = g.db.collection('jobs').stream()
    applied_job_ids = []

    for job_doc in jobs_stream:
        apps = (g.db.collection('jobs').document(job_doc.id)
                  .collection('applications')
                  .where('candidate_email', '==', candidate_email)
                  .limit(1)
                  .stream())
        if any(True for _ in apps):
            applied_job_ids.append(job_doc.id)

    return jsonify({"status": "success", "applied_job_ids": applied_job_ids})

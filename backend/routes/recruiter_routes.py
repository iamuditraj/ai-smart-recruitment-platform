from flask import Blueprint, g, jsonify, request
from routes.decorators import handle_route_errors, require_db
from services.db_helpers import serialize_timestamps, enrich_app_with_candidate

recruiter_bp = Blueprint('recruiter', __name__)

@recruiter_bp.route('/api/recruiter/applications', methods=['GET'])
@handle_route_errors
@require_db
def get_recruiter_applications():
    recruiter_email = request.args.get('email')
    if not recruiter_email:
        return jsonify({"status": "error", "message": "Recruiter email is required"}), 400

    # 1. Get all job IDs belonging to this recruiter
    jobs_docs = g.db.collection('jobs').where('recruiter_email', '==', recruiter_email).get()
    job_ids = [doc.id for doc in jobs_docs]

    if not job_ids:
        return jsonify({"status": "success", "applications": []})

    # 2. Get all applications for these jobs
    all_apps = []
    for j_id in job_ids:
        apps = g.db.collection('jobs').document(j_id).collection('applications').stream()
        for app_doc in apps:
            app_data = app_doc.to_dict()
            enrich_app_with_candidate(g.db, app_data)
            app_data = serialize_timestamps(app_data)
            all_apps.append(app_data)

    return jsonify({
        "status": "success",
        "applications": all_apps
    })


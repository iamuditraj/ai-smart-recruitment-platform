from flask import Blueprint, jsonify, request
from services.firebase_service import get_db
from services.db_helpers import serialize_timestamps

recruiter_bp = Blueprint('recruiter', __name__)

@recruiter_bp.route('/api/recruiter/applications', methods=['GET'])
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
        all_apps = []
        for j_id in job_ids:
            apps = db.collection('jobs').document(j_id).collection('applications').stream()
            for app_doc in apps:
                app_data = app_doc.to_dict()
                
                # Fetch candidate profile to get name and resume
                c_email = app_data.get('candidate_email')
                user_doc = db.collection('candidates').document(c_email).get()
                if user_doc.exists:
                    user_data = user_doc.to_dict()
                    app_data['candidate_name'] = user_data.get('name', 'Unknown')
                    app_data['resumeUrl'] = user_data.get('resumeUrl')
                    app_data['resumeName'] = user_data.get('resumeName')
                    app_data['experience'] = user_data.get('bio', '') # Using bio as teaser experience
                
                app_data = serialize_timestamps(app_data)
                all_apps.append(app_data)

        return jsonify({
            "status": "success",
            "applications": all_apps
        })

    except Exception as e:
        print(f"Error in get_recruiter_applications: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

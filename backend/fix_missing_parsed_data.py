import os
import sys
import io
import json

# Ensure the backend directory is in the Python path
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
if BACKEND_DIR not in sys.path:
    sys.path.append(BACKEND_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(BACKEND_DIR, '.env'))

from firebase_admin import firestore
from services.firebase_service import init_firebase, get_db
from services.parser_service import extract_text
from services.ai_service import init_ai, parse_resume_against_jd, parse_job_description

def _build_jd_from_job(job_data):
    """Reconstruct JD text from job data (similar to api_routes utility)"""
    title = job_data.get('title', '')
    desc = job_data.get('description', '')
    reqs = job_data.get('requirements', [])
    text = f"Title: {title}\nDescription: {desc}\nRequirements: {', '.join(reqs)}"
    
    parsed_jd = {
        "required_skills": reqs,
        "min_exp_years": 0,
        "education_level": 1
    }
    return text, parsed_jd

def fix_all_applications():
    # Initialize services
    init_firebase()
    init_ai()
    db = get_db()
    if not db:
        print("❌ Firebase error")
        return

    print("🚀 Fixing missing parsed resume data for all applications...")
    
    resumes_dir = os.path.join(BACKEND_DIR, "Test_scripts", "Test resume")

    # 1. Get all jobs
    jobs = db.collection('jobs').stream()
    for job_doc in jobs:
        job_id = job_doc.id
        job_data = job_doc.to_dict()
        jd_text, _ = _build_jd_from_job(job_data)
        
        # 2. Get applications for this job
        apps = db.collection('jobs').document(job_id).collection('applications').stream()
        for app_doc in apps:
            app_data = app_doc.to_dict()
            
            # If parsedResume is missing, attempt to fix it
            if 'parsedResume' not in app_data or not app_data['parsedResume']:
                email = app_data.get('candidate_email')
                filename = app_data.get('resume_filename')
                
                print(f"  Fixing app {app_doc.id} for {email}...")
                
                if filename:
                    resume_path = os.path.join(resumes_dir, filename)
                    if os.path.exists(resume_path):
                        try:
                            # Re-parse
                            with open(resume_path, 'rb') as f:
                                file_stream = io.BytesIO(f.read())
                                resume_text = extract_text(file_stream, filename)
                                parsed_res = parse_resume_against_jd(resume_text, jd_text)
                                
                                # Update application
                                app_doc.reference.update({"parsedResume": parsed_res})
                                
                                # Update candidate profile too
                                db.collection('candidates').document(email).update({"parsedResume": parsed_res})
                                
                                print(f"    ✅ Resaved parsedResume for {email}")
                                continue
                        except Exception as e:
                            print(f"    ❌ Error parsing {filename}: {e}")
                
                print(f"    ⚠️ No resume file found for local re-parsing of {email}")

    print("\n✨ Fix process completed.")

if __name__ == "__main__":
    fix_all_applications()

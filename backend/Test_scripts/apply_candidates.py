import os
import sys
import time
import requests
from werkzeug.security import generate_password_hash
from test_utils import setup_backend_path, get_firebase_db

setup_backend_path()
from firebase_admin import firestore

BASE_URL = "http://127.0.0.1:5001"
JOB_ID = "4t1pRjLsLcC230Ki6FKf"
TEST_RESUMES_DIR = os.path.join(os.path.dirname(__file__), "Test resume")

def ensure_candidate1_exists():
    """Ensure candidate1 exists in the database as requested."""
    print("Checking if candidate1 exists...")
    db = get_firebase_db()
    if not db:
        print("❌ Could not initialize Firebase.")
        return
        
    email = "candidate1@test.com"
    doc = db.collection('candidates').document(email).get()
    if not doc.exists:
        print(f"Creating missing {email}...")
        password = "12345678"
        hashed_password = generate_password_hash(password)
        db.collection('user_index').document(email).set({'role': 'candidate'})
        db.collection('candidates').document(email).set({
            'email': email,
            'password': hashed_password,
            'role': 'candidate',
            'name': 'candidate1',
            'createdAt': firestore.SERVER_TIMESTAMP
        })
        print("✅ Created candidate1")
    else:
        print("✅ candidate1 already exists.")

def apply_for_candidate(candidate_id):
    email = f"candidate{candidate_id}@test.com"
    resume_filename = f"ATSTestResumes-{candidate_id}.pdf"
    resume_path = os.path.join(TEST_RESUMES_DIR, resume_filename)
    
    if not os.path.exists(resume_path):
        print(f"❌ Resume not found for {email}: {resume_path}")
        return False
        
    print(f"\n🚀 Candidate {candidate_id} ({email}) is applying for job {JOB_ID}...")
    
    try:
        with open(resume_path, 'rb') as f:
            files = {
                'resume': (resume_filename, f, 'application/pdf')
            }
            data = {
                'job_id': JOB_ID,
                'candidate_email': email
            }
            
            response = requests.post(f"{BASE_URL}/api/jobs/apply", data=data, files=files, timeout=90)
            
            if response.status_code == 200:
                print(f"✅ Successfully applied for {email}")
                print(f"   ATS Score: {response.json().get('ats_score')}")
                return True
            else:
                print(f"❌ Failed to apply for {email}. Status: {response.status_code}")
                # Don't print the whole html if it's a 500 error page
                text = response.text
                if len(text) > 200:
                    text = text[:200] + "..."
                print(f"   Response: {text}")
                return False
    except Exception as e:
        print(f"❌ Error during application for {email}: {e}")
        return False

if __name__ == "__main__":
    ensure_candidate1_exists()
    
    print("=" * 60)
    print("Starting sequential job applications using local API...")
    print("=" * 60)
    
    for i in range(1, 16):
        success = apply_for_candidate(i)
        if success:
            # 2 second delay to ease load on the LLM API / Local server
            time.sleep(2)
        else:
            time.sleep(1)
            
    print("=" * 60)
    print("✨ Finished processing all candidate applications.")

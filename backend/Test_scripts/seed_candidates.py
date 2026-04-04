import os
import sys
from werkzeug.security import generate_password_hash

# Ensure the backend directory is in the Python path
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_DIR not in sys.path:
    sys.path.append(BACKEND_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(BACKEND_DIR, '.env'))

from firebase_admin import firestore
from services.firebase_service import init_firebase, get_db

def seed_candidates():
    # Initialize Firebase using your existing service
    init_firebase()
    db = get_db()
    if not db:
        print("❌ Failed to initialize Firebase. Make sure 'serviceAccountKey.json' is present.")
        return

    password = "12345678"
    hashed_password = generate_password_hash(password)
    
    print(f"🚀 Starting seeding of 14 candidates (candidate2 to candidate15)...")

    for i in range(2, 16):
        email = f"candidate{i}@test.com"
        name = f"candidate{i}"
        role = "candidate"
        
        try:
            # 1. Write the role-lookup doc to 'user_index'
            db.collection('user_index').document(email).set({
                'role': role
            })
            
            # 2. Write the candidate profile to 'candidates'
            db.collection('candidates').document(email).set({
                'email': email,
                'password': hashed_password,
                'role': role,
                'name': name,
                'createdAt': firestore.SERVER_TIMESTAMP
            })
            
            print(f"✅ Successfully created: {email}")
            
        except Exception as e:
            print(f"❌ Error creating {email}: {e}")

    print("✨ Seeding process finished.")

if __name__ == "__main__":
    seed_candidates()

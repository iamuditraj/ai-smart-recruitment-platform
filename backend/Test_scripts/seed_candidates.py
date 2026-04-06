import os
import sys
from werkzeug.security import generate_password_hash

from test_utils import setup_backend_path, get_firebase_db
setup_backend_path()

from firebase_admin import firestore

def seed_candidates():
    db = get_firebase_db()
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

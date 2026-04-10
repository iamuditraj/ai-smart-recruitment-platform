import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

db = None

def init_firebase():
    global db
    
    # Priority 1: JSON string from ENV (Best for Render/Heroku)
    key_json = os.getenv("FIREBASE_KEY_JSON")
    # Priority 2: File path from ENV or default
    key_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY", "serviceAccountKey.json")
    
    try:
        if key_json:
            # Parse JSON string into a dict and initialize
            key_dict = json.loads(key_json)
            cred = credentials.Certificate(key_dict)
            print("✅ Firebase initialized from FIREBASE_KEY_JSON!")
        elif os.path.exists(key_path):
            cred = credentials.Certificate(key_path)
            print(f"✅ Firebase initialized from file: {key_path}")
        else:
            print("⚠️  Warning: Firebase credentials not found (Checked FIREBASE_KEY_JSON and serviceAccountKey.json).")
            return

        # Only initialize if it hasn't been already
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        db = firestore.client()
    except Exception as e:
        print(f"❌ Error initializing Firebase: {e}")


def get_db():
    return db

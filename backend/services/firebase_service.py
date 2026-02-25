import os
import firebase_admin
from firebase_admin import credentials, firestore

db = None

def init_firebase():
    global db
    key_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY", "serviceAccountKey.json")
    
    if os.path.exists(key_path):
        try:
            cred = credentials.Certificate(key_path)
            # Only initialize if it hasn't been already
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            db = firestore.client()
            print("✅ Firebase Admin initialized successfully!")
        except Exception as e:
            print(f"❌ Error initializing Firebase: {e}")
    else:
        print("⚠️  Warning: serviceAccountKey.json not found. Database features won't work yet.")

def get_db():
    return db

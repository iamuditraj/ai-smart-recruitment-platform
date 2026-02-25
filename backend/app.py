from flask import Flask, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import os

app = Flask(__name__)
CORS(app)

# 1. Initialize Firebase
# Path to your service account key file
key_path = "serviceAccountKey.json"

if os.path.exists(key_path):
    try:
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase Admin initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing Firebase: {e}")
else:
    print("⚠️  Warning: serviceAccountKey.json not found. Database features won't work yet.")

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "project": "HireAI",
        "message": "Flask is integrated correctly!"
    })

@app.route('/api/check-db')
def check_db():
    try:
        if 'db' not in globals():
             return jsonify({"status": "error", "message": "Firebase not initialized. Did you add serviceAccountKey.json?"})
        return jsonify({"status": "success", "message": "Connected to Firestore!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # Use port 5001 to avoid conflicts with common services or your frontend
    app.run(debug=True, port=5001)

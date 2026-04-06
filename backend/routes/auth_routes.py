from flask import Blueprint, jsonify, request
from services.firebase_service import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from firebase_admin import firestore

from services.db_helpers import get_user_collection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        name = data.get('name', '')

        if not email or not password or not role:
            return jsonify({"status": "error", "message": "Missing email, password or role"}), 400

        db = get_db()
        if not db:
            return jsonify({"status": "error", "message": "Database not initialized"}), 500

        # Check if user exists in the user_index collection
        index_doc = db.collection('user_index').document(email).get()

        if index_doc.exists:
            return jsonify({"status": "error", "message": "User already exists"}), 400

        # Write the role-lookup doc
        db.collection('user_index').document(email).set({'role': role})

        # Create user in the appropriate collection
        hashed_password = generate_password_hash(password)
        collection_name = 'recruiters' if role == 'recruiter' else 'candidates'
        
        db.collection(collection_name).document(email).set({
            'email': email,
            'password': hashed_password,
            'role': role,
            'name': name,
            'createdAt': firestore.SERVER_TIMESTAMP if hasattr(firestore, 'SERVER_TIMESTAMP') else None
        })

        return jsonify({
            "status": "success",
            "message": "Account created successfully!",
            "user": {
                "email": email,
                "role": role,
                "name": name
            }
        })
    except Exception as e:
        print(f"Error in signup: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@auth_bp.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"status": "error", "message": "Missing email or password"}), 400

        db = get_db()
        if not db:
            return jsonify({"status": "error", "message": "Database not initialized"}), 500

        # Check user_index to get role
        user_role, collection_name = get_user_collection(db, email)

        if not user_role:
            return jsonify({"status": "error", "message": "Invalid email or password"}), 401
        
        # Get user from correct collection
        user_doc = db.collection(collection_name).document(email).get()

        if not user_doc.exists:
            return jsonify({"status": "error", "message": "Invalid email or password"}), 401

        user_data = user_doc.to_dict()
        if not check_password_hash(user_data['password'], password):
            return jsonify({"status": "error", "message": "Invalid email or password"}), 401

        return jsonify({
            "status": "success",
            "message": "Login successful!",
            "user": {
                "email": user_data['email'],
                "role": user_data['role'],
                "name": user_data.get('name', '')
            }
        })
    except Exception as e:
        print(f"Error in login: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

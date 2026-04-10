from flask import Blueprint, g, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from firebase_admin import firestore, auth as firebase_auth

from routes.decorators import handle_route_errors, require_db
from services.db_helpers import get_user_collection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/signup', methods=['POST'])
@handle_route_errors
@require_db
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    name = data.get('name', '')

    if not email or not password or not role:
        return jsonify({"status": "error", "message": "Missing email, password or role"}), 400

    # Check if user exists in the user_index collection
    index_doc = g.db.collection('user_index').document(email).get()

    if index_doc.exists:
        return jsonify({"status": "error", "message": "User already exists"}), 400

    # Write the role-lookup doc
    g.db.collection('user_index').document(email).set({'role': role})

    # Create user in the appropriate collection
    hashed_password = generate_password_hash(password)
    collection_name = 'recruiters' if role == 'recruiter' else 'candidates'
    
    g.db.collection(collection_name).document(email).set({
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

@auth_bp.route('/api/login', methods=['POST'])
@handle_route_errors
@require_db
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"status": "error", "message": "Missing email or password"}), 400

    # Check user_index to get role
    user_role, collection_name = get_user_collection(g.db, email)

    if not user_role:
        return jsonify({"status": "error", "message": "Invalid email or password"}), 401
    
    # Get user from correct collection
    user_doc = g.db.collection(collection_name).document(email).get()

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

@auth_bp.route('/api/google-auth', methods=['POST'])
@handle_route_errors
@require_db
def google_auth():
    data = request.json
    id_token = data.get('idToken')
    role = data.get('role')

    if not id_token:
        return jsonify({"status": "error", "message": "Missing ID token"}), 400

    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        email = decoded_token.get('email')
        name = decoded_token.get('name', '')
    except Exception as e:
        return jsonify({"status": "error", "message": "Invalid Google token"}), 401

    if not email:
        return jsonify({"status": "error", "message": "No email in token"}), 400

    # Check if user exists
    user_role, collection_name = get_user_collection(g.db, email)

    if user_role:
        # Existing user - log them in
        user_doc = g.db.collection(collection_name).document(email).get()
        user_data = user_doc.to_dict() if user_doc.exists else {}
        
        return jsonify({
            "status": "success",
            "message": "Login successful!",
            "user": {
                "email": email,
                "role": user_role,
                "name": user_data.get('name', name)
            }
        })
    else:
        # New Google user - need a role
        if not role or role not in ['candidate', 'recruiter']:
            # Default to candidate if none provided and it's a new user
            role = 'candidate'

        # Write the role-lookup doc
        g.db.collection('user_index').document(email).set({'role': role})

        # Create user in the appropriate collection
        collection_name = 'recruiters' if role == 'recruiter' else 'candidates'
        
        g.db.collection(collection_name).document(email).set({
            'email': email,
            'password': None, # No password for Google authenticated users
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

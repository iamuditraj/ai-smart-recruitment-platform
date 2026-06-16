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
    uid = data.get('uid')
    email = data.get('email')
    role = data.get('role')
    name = data.get('name', '')
    tenant_id = data.get('tenant_id')

    if not uid or not email or not role:
        if uid:
            try:
                firebase_auth.delete_user(uid)
            except Exception as e:
                print(f"Auth rollback failed: {e}")
        return jsonify({"status": "error", "message": "Missing uid, email or role"}), 400

    try:
        batch = g.db.batch()

        user_index_ref = g.db.collection('user_index').document(uid)
        
        if role == 'recruiter':
            collection_name = 'recruiters'
        elif role == 'candidate':
            collection_name = 'candidates'
        elif role == 'college':
            collection_name = 'colleges'
        elif role == 'company':
            collection_name = 'companies'
        else:
            raise ValueError("Invalid role")
            
        profile_ref = g.db.collection(collection_name).document(uid)

        batch.set(user_index_ref, {'role': role, 'email': email})

        profile_data = {
            'uid': uid,
            'email': email,
            'role': role,
            'name': name,
            'createdAt': firestore.SERVER_TIMESTAMP if hasattr(firestore, 'SERVER_TIMESTAMP') else None
        }
        
        if role in ('recruiter', 'company') and tenant_id:
            profile_data['company_id'] = tenant_id
        elif role in ('candidate', 'college') and tenant_id:
            profile_data['college_id'] = tenant_id

        batch.set(profile_ref, profile_data)
        
        batch.commit()

        return jsonify({
            "status": "success",
            "message": "Account created successfully!",
            "user": {
                "uid": uid,
                "email": email,
                "role": role,
                "name": name,
                "tenant_id": tenant_id
            }
        })
    except Exception as e:
        # Rollback Firebase Auth user
        try:
            firebase_auth.delete_user(uid)
            print(f"Rolled back Firebase Auth user: {uid}")
        except Exception as rollback_e:
            print(f"Rollback failed for {uid}: {rollback_e}")
            
        return jsonify({"status": "error", "message": f"Signup failed: {str(e)}"}), 500



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
        # User not found
        if not role:
            # Login attempt but no account found
            return jsonify({"status": "error", "code": "USER_NOT_FOUND", "message": "Account not found. Please sign up."}), 404

        # New Google user - need a role
        if role not in ['candidate', 'recruiter']:
            return jsonify({"status": "error", "message": "Invalid role specified."}), 400

        # Write the role-lookup doc
        g.db.collection('user_index').document(email).set({'role': role})

        # Create user in the appropriate collection
        collection_name = 'recruiters' if role == 'recruiter' else 'candidates'
        
        g.db.collection(collection_name).document(email).set({
            'email': email,
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

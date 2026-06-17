"""
Route decorators for cross-cutting concerns (error handling, auth guards, etc.)
"""
import logging
from functools import wraps
from flask import g, jsonify, request
import firebase_admin.auth

from services.firebase_service import get_db
from services.ai_service import get_model

logger = logging.getLogger(__name__)


def handle_route_errors(f):
    """
    Decorator that wraps a Flask route handler in a standardized try/except.
    Logs the full traceback via `logging.exception` and returns a consistent
    JSON error envelope so individual routes don't need their own try/except.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.exception("Error in %s", f.__name__)
            return jsonify({"status": "error", "message": str(e)}), 500
    return decorated_function


def require_db(f):
    """
    Decorator that ensures the Firestore client is available before the
    handler runs.  Sets ``g.db`` for the handler to use.
    Returns a 500 JSON response if Firebase is not initialized.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        db = get_db()
        if not db:
            return jsonify({"status": "error", "message": "Database not initialized"}), 500
        g.db = db
        return f(*args, **kwargs)
    return decorated_function


def require_ai_model(f):
    """
    Decorator that ensures the Groq AI client is available before the
    handler runs.  Sets ``g.model`` for the handler to use.
    Returns a 500 JSON response if the AI model is not initialized.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        model = get_model()
        if not model:
            return jsonify({"status": "error", "message": "AI model not initialized"}), 500
        g.model = model
        return f(*args, **kwargs)
    return decorated_function


def require_role(allowed_roles):
    """
    Decorator for RBAC. Expects an Authorization: Bearer <token> header.
    Verifies the token via Firebase Admin, checks if the user's role is in 
    `allowed_roles`, and attaches the decoded token to `g.user`.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"status": "error", "message": "Missing or invalid Authorization header"}), 401
            
            token = auth_header.split(" ")[1]
            try:
                decoded_token = firebase_admin.auth.verify_id_token(token)
            except Exception as e:
                logger.exception("Token verification failed")
                return jsonify({"status": "error", "message": "Invalid token"}), 401
            
            user_role = decoded_token.get("role")
            if not user_role or user_role not in allowed_roles:
                return jsonify({"status": "error", "message": "Forbidden: Insufficient permissions"}), 403
            
            g.user = decoded_token
            return f(*args, **kwargs)
        return decorated_function
    return decorator

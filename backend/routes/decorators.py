"""
Route decorators for cross-cutting concerns (error handling, auth guards, etc.)
"""
import logging
from functools import wraps
from flask import g, jsonify

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

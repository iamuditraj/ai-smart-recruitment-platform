import os
import sys

def setup_backend_path():
    """Ensure the backend directory is in the Python path and load .env"""
    BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if BACKEND_DIR not in sys.path:
        sys.path.append(BACKEND_DIR)
    
    from dotenv import load_dotenv
    load_dotenv(os.path.join(BACKEND_DIR, '.env'))
    return BACKEND_DIR

def get_firebase_db():
    """Initialize Firebase and return the database client"""
    from services.firebase_service import init_firebase, get_db
    init_firebase()
    return get_db()

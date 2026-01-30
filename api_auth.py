"""
API Authentication.
"""
from functools import wraps
from flask import request, jsonify
from config import API_KEY

def require_api_key(f):
    """Decorator to require X-API-Key header."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        key = request.headers.get('X-API-Key')
        if key and key == API_KEY:
            return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized", "message": "Invalid or missing API Key"}), 401
    return decorated_function

"""
Simple Authentication Logic.
"""
from functools import wraps
from flask import session, redirect, url_for, flash, request
from config import DEBUG

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """Wrapper to check session."""
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

"""
Admin Dashboard Routes.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from auth import login_required
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def dashboard():
    """Render admin dashboard."""
    return render_template('admin/dashboard.html')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle admin login."""
    if request.method == 'POST':
        password = request.form.get('password')
        # In real app, check env var. For demo: 'admin'
        if password == 'admin':
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid password')
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    """Handle admin logout."""
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))

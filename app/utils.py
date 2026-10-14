"""
Utility functions and decorators for Online Complaint Management System (OCMS).
Includes role-based access decorators, tracking number generation, secure uploads,
and audit logging.
"""

import os
import uuid
from datetime import datetime, timedelta
from functools import wraps
from flask import abort, flash, redirect, url_for, request, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename
from app.models import db, Complaint, Notification, AuditLog


def admin_required(f):
    """Decorator to restrict route access strictly to users with 'admin' role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please sign in to access the administrator portal.", "warning")
            return redirect(url_for('auth.login', next=request.url))
        if current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def staff_required(f):
    """Decorator to restrict route access to Staff officers and Administrators."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please sign in to access the staff workspace.", "warning")
            return redirect(url_for('auth.login', next=request.url))
        if current_user.role not in ['staff', 'admin']:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def generate_tracking_number():
    """
    Generate unique complaint tracking number in format OCMS-2026-XXXX.
    Guarantees sequential uniqueness across concurrent transactions.
    """
    year = datetime.utcnow().year
    # Find highest number for current year
    prefix = f"OCMS-{year}-"
    last_comp = Complaint.query.filter(Complaint.tracking_number.like(f"{prefix}%"))\
        .order_by(Complaint.id.desc()).first()
    
    if last_comp:
        try:
            seq = int(last_comp.tracking_number.split('-')[-1]) + 1
        except Exception:
            seq = Complaint.query.count() + 1
    else:
        seq = 1

    tracking_no = f"{prefix}{seq:04d}"
    # Double check uniqueness
    while Complaint.query.filter_by(tracking_number=tracking_no).first() is not None:
        seq += 1
        tracking_no = f"{prefix}{seq:04d}"
    return tracking_no


def allowed_file(filename):
    """Check if uploaded file has an allowed extension (png, jpg, jpeg, pdf)."""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'pdf'})


def save_attachment(file_storage):
    """
    Validate, securely rename, and save an uploaded file.
    Returns the saved filename or None if invalid.
    """
    if not file_storage or not file_storage.filename:
        return None
    
    if not allowed_file(file_storage.filename):
        return None
    
    filename = secure_filename(file_storage.filename)
    unique_name = f"{uuid.uuid4().hex[:12]}_{filename}"
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    destination = os.path.join(upload_folder, unique_name)
    file_storage.save(destination)
    return unique_name


def calculate_due_date(category, priority='Medium'):
    """
    Compute SLA target deadline based on Category SLA and Priority weighting.
    Priority multipliers: Urgent=0.25x, High=0.5x, Medium=1.0x, Low=1.5x.
    """
    base_hours = category.sla_hours if category else 48
    multipliers = {
        'Urgent': 0.25,
        'High': 0.5,
        'Medium': 1.0,
        'Low': 1.5
    }
    hours = int(base_hours * multipliers.get(priority, 1.0))
    if hours < 4:
        hours = 4  # Minimum SLA 4 hours
    return datetime.utcnow() + timedelta(hours=hours)


def send_notification(user_id, message, complaint_id=None):
    """Create in-app notification record (FR-5.3)."""
    try:
        notif = Notification(
            user_id=user_id,
            complaint_id=complaint_id,
            message=message
        )
        db.session.add(notif)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Failed to create notification: {e}")


def record_audit(action, target_id=None, details=None):
    """Record an administrative audit log entry (FR-3.10)."""
    try:
        user_id = current_user.id if (current_user and current_user.is_authenticated) else None
        ip_addr = request.remote_addr if request else "127.0.0.1"
        log = AuditLog(
            user_id=user_id,
            action=action,
            target_id=str(target_id) if target_id else None,
            details=details,
            ip_address=ip_addr
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Failed to record audit log: {e}")

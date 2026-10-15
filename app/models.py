"""
SQLAlchemy Database Models for Online Complaint Management System (OCMS).
Normalized tables conforming to IEEE Std 830-1998 SRS Specification.
"""

import os
from datetime import datetime, timedelta
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import TypeDecorator, DateTime

db = SQLAlchemy()


class SliceableDateTime(datetime):
    """
    Datetime subclass that supports slice notation (e.g. dt[:10])
    for seamless compatibility with Jinja2 string-slicing templates.
    """
    def __getitem__(self, item):
        return self.strftime("%Y-%m-%d %H:%M:%S")[item]


class SliceableDateTimeType(TypeDecorator):
    """Custom SQLAlchemy type decorator returning SliceableDateTime objects."""
    impl = DateTime
    cache_ok = True

    def process_result_value(self, value, dialect):
        if value is not None:
            return SliceableDateTime(
                value.year, value.month, value.day,
                value.hour, value.minute, value.second,
                value.microsecond, value.tzinfo
            )
        return value


class User(UserMixin, db.Model):
    """
    User Account Model.
    Actors: Complainant ('user'), Technician ('staff'), Administrator ('admin').
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False, index=True)  # 'user', 'staff', 'admin'
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    department = db.Column(db.String(100), nullable=True)
    failed_attempts = db.Column(db.Integer, default=0, nullable=False)
    locked_until = db.Column(SliceableDateTimeType, nullable=True)
    created_at = db.Column(SliceableDateTimeType, default=datetime.utcnow, nullable=False)

    # Relationships
    complaints = db.relationship('Complaint', foreign_keys='Complaint.user_id', backref='user', lazy=True)
    assigned_complaints = db.relationship('Complaint', foreign_keys='Complaint.assigned_to', backref='assignee', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and store password with Werkzeug salt."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password against stored salt and hash."""
        return check_password_hash(self.password_hash, password)

    def is_locked(self):
        """Check if account is temporarily locked due to failed login attempts (FR-1.8)."""
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False

    def record_failed_login(self):
        """Increment failed attempts; lock for 15 minutes after 5 consecutive failures."""
        self.failed_attempts += 1
        if self.failed_attempts >= 5:
            self.locked_until = datetime.utcnow() + timedelta(minutes=15)

    def reset_failed_logins(self):
        """Reset failed attempt counter and unlock on successful login."""
        self.failed_attempts = 0
        self.locked_until = None

    def get_reset_token(self):
        """Generate a time-limited secure token for password recovery (FR-1.6)."""
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}, salt='ocms-password-reset')

    @staticmethod
    def verify_reset_token(token, expires_sec=900):
        """Verify password reset token within expiration window (default 15 mins)."""
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, salt='ocms-password-reset', max_age=expires_sec)
        except Exception:
            return None
        return User.query.get(data.get('user_id'))

    @property
    def user_id(self):
        """Compatibility property for templates expecting user.user_id."""
        return self.id

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


class Department(db.Model):
    """Department / Section lookup table."""
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Department {self.name}>"


class Category(db.Model):
    """
    Complaint Category with target Service Level Agreement (SLA).
    Managed by Administrator (FR-3.4).
    """
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    sla_hours = db.Column(db.Integer, default=48, nullable=False)
    icon = db.Column(db.String(50), default='bi-tag', nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    default_priority = db.Column(db.String(20), default='Medium', nullable=False)

    complaints = db.relationship('Complaint', backref='category', lazy=True)

    @property
    def category_id(self):
        """Compatibility property for templates."""
        return self.id

    @property
    def complaint_count(self):
        """Total count of complaints under this category."""
        return len(self.complaints)

    def __repr__(self):
        return f"<Category {self.name}>"


class Complaint(db.Model):
    """
    Central Complaint / Grievance Entity.
    Tracks lifecycle from Submitted -> Assigned -> In Progress -> Resolved -> Closed.
    """
    __tablename__ = 'complaints'

    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=True)
    priority = db.Column(db.String(20), default='Medium', nullable=False)  # Low, Medium, High, Urgent
    status = db.Column(db.String(30), default='Submitted', nullable=False, index=True)
    attachment_path = db.Column(db.String(255), nullable=True)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    is_anonymous = db.Column(db.Boolean, default=False, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('complaints.id'), nullable=True)
    created_at = db.Column(SliceableDateTimeType, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(SliceableDateTimeType, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    due_at = db.Column(SliceableDateTimeType, nullable=True)
    resolved_at = db.Column(SliceableDateTimeType, nullable=True)

    # Relationships
    department = db.relationship('Department', backref='complaints', lazy=True)
    updates = db.relationship('ComplaintUpdate', backref='complaint', lazy=True, order_by='ComplaintUpdate.created_at.asc()', cascade='all, delete-orphan')
    feedback = db.relationship('Feedback', backref='complaint', uselist=False, lazy=True, cascade='all, delete-orphan')

    # Compatibility Properties for Jinja2 Templates
    @property
    def complaint_id(self):
        return self.id

    @property
    def complaint_no(self):
        return self.tracking_number

    @property
    def subject(self):
        return self.title

    @subject.setter
    def subject(self, val):
        self.title = val

    @property
    def category_name(self):
        return self.category.name if self.category else 'General'

    @property
    def assigned_name(self):
        return self.assignee.name if self.assignee else 'Unassigned'

    @property
    def user_name(self):
        return 'Anonymous' if self.is_anonymous else (self.user.name if self.user else 'Unknown')

    @property
    def user_email(self):
        return 'Hidden' if self.is_anonymous else (self.user.email if self.user else '')

    @property
    def user_phone(self):
        return 'Hidden' if self.is_anonymous else (self.user.phone if self.user else '')

    @property
    def comments(self):
        """Timeline updates matching the template comment list structure."""
        return self.updates

    @property
    def attachments(self):
        """List of attachment metadata dicts for template rendering."""
        if not self.attachment_path:
            return []
        fname = os.path.basename(self.attachment_path)
        is_img = fname.lower().endswith(('.png', '.jpg', '.jpeg'))
        return [{
            'file_name': fname,
            'url': f"/static/uploads/{fname}",
            'file_type': 'image' if is_img else 'application/pdf'
        }]

    @property
    def is_overdue(self):
        """Returns True if SLA deadline has passed and complaint is still open."""
        if self.due_at and datetime.utcnow() > self.due_at and self.status not in ['Resolved', 'Closed']:
            return True
        return False

    def __repr__(self):
        return f"<Complaint {self.tracking_number} [{self.status}]>"


class ComplaintUpdate(db.Model):
    """
    Status change history and remarks timeline entries.
    Every status progression or admin/staff note logs here.
    """
    __tablename__ = 'complaint_updates'

    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'), nullable=False, index=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    old_status = db.Column(db.String(30), nullable=True)
    new_status = db.Column(db.String(30), nullable=True)
    remark = db.Column(db.Text, nullable=False)
    created_at = db.Column(SliceableDateTimeType, default=datetime.utcnow, nullable=False)

    updater = db.relationship('User', lazy=True)

    @property
    def comment_id(self):
        return self.id

    @property
    def message(self):
        return self.remark

    @property
    def user_name(self):
        if self.updater:
            role_label = f" ({self.updater.role.title()})" if self.updater.role != 'user' else ""
            return f"{self.updater.name}{role_label}"
        return 'System Notification'

    @property
    def user_role(self):
        return self.updater.role if self.updater else 'system'

    @property
    def is_status_change(self):
        return bool(self.new_status and self.new_status != self.old_status)

    def __repr__(self):
        return f"<ComplaintUpdate {self.id} on {self.complaint_id}>"


class Feedback(db.Model):
    """
    Post-resolution satisfaction rating (1-5 stars) and review.
    Can only be submitted once per resolved complaint (FR-6.1).
    """
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1 to 5
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(SliceableDateTimeType, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', lazy=True)

    @property
    def feedback_id(self):
        return self.id

    @property
    def comments(self):
        return self.comment

    def __repr__(self):
        return f"<Feedback {self.rating}* for Complaint {self.complaint_id}>"


class Notification(db.Model):
    """
    In-App alerts and notifications for status progressions (FR-5.3).
    """
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'), nullable=True)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(SliceableDateTimeType, default=datetime.utcnow, nullable=False)

    complaint = db.relationship('Complaint', lazy=True)

    @property
    def notification_id(self):
        return self.id

    @property
    def complaint_no(self):
        return self.complaint.tracking_number if self.complaint else None

    @property
    def title(self):
        return "Complaint Update"

    @property
    def icon(self):
        return "bi-bell"

    @property
    def time_ago(self):
        return "Recently"

    def __repr__(self):
        return f"<Notification for User {self.user_id}>"


class AuditLog(db.Model):
    """
    Administrative and security audit trail (FR-3.10).
    """
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    target_id = db.Column(db.String(50), nullable=True)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    created_at = db.Column(SliceableDateTimeType, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', lazy=True)

    @property
    def log_id(self):
        return self.id

    @property
    def user_name(self):
        return self.user.name if self.user else 'System'

    @property
    def user_role(self):
        return self.user.role if self.user else 'System'

    @property
    def timestamp(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return f"<AuditLog {self.action} by User {self.user_id}>"

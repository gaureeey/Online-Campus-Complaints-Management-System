"""
Ancillary Feature Tests (SRS Sections 3.6, 3.7, 4.0).
Tests satisfaction ratings (FR-6.1), file upload constraints (FR-2.3),
notification center (FR-5.3), CSV reports (FR-7.3), and audit logging (FR-3.10).
"""

import io
from datetime import datetime, timedelta
from app.models import db, Complaint, Feedback, Notification, AuditLog, User, Category


def test_feedback_submission_on_resolved_complaint(auth, client):
    """FR-6.1: Submitting 1-5 star rating and comment on resolved complaint."""
    auth.login_user()
    user = User.query.filter_by(email='user@example.com').first()
    cat = Category.query.first()

    comp = Complaint(
        tracking_number="OCMS-2026-7001",
        user_id=user.id,
        category_id=cat.id,
        title="Repaired issue",
        description="Completed task",
        status="Resolved",
        priority="Medium",
        resolved_at=datetime.utcnow() - timedelta(days=1)
    )
    db.session.add(comp)
    db.session.commit()

    response = client.post(f'/complaint/{comp.tracking_number}/feedback', data={
        'rating': '5',
        'comments': 'Excellent rapid assistance.'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Thank you for rating our service' in response.data

    fb = Feedback.query.filter_by(complaint_id=comp.id).first()
    assert fb is not None
    assert fb.rating == 5
    assert fb.comment == 'Excellent rapid assistance.'


def test_duplicate_feedback_prevented(auth, client):
    """FR-6.1: Feedback can only be submitted once per resolved complaint."""
    auth.login_user()
    user = User.query.filter_by(email='user@example.com').first()
    cat = Category.query.first()

    comp = Complaint(
        tracking_number="OCMS-2026-7002",
        user_id=user.id,
        category_id=cat.id,
        title="Rated issue",
        description="Already rated",
        status="Resolved",
        priority="Low",
        resolved_at=datetime.utcnow()
    )
    db.session.add(comp)
    db.session.commit()

    # 1st feedback
    client.post(f'/complaint/{comp.tracking_number}/feedback', data={
        'rating': '4',
        'comments': 'Good fix.'
    }, follow_redirects=True)

    # 2nd feedback attempt
    client.post(f'/complaint/{comp.tracking_number}/feedback', data={
        'rating': '1',
        'comments': 'Changed my mind.'
    }, follow_redirects=True)

    # Rating should remain 4
    fb = Feedback.query.filter_by(complaint_id=comp.id).first()
    assert fb.rating == 4


def test_file_attachment_upload_valid(auth, client):
    """FR-2.3 & TC-3: Upload valid image file attachment."""
    auth.login_user()
    category = Category.query.first()

    file_data = (io.BytesIO(b"fake image data"), "evidence.png")

    response = client.post('/complaint/new', data={
        'subject': 'Damaged projector ceiling cord',
        'category_id': category.id,
        'priority': 'Medium',
        'location': 'Lab 2',
        'description': 'See attached photo of frayed cable.',
        'attachments': [file_data]
    }, content_type='multipart/form-data', follow_redirects=True)

    assert response.status_code == 200
    comp = Complaint.query.filter_by(title='Damaged projector ceiling cord').first()
    assert comp is not None
    assert comp.attachment_path is not None
    assert comp.attachment_path.endswith('.png')


def test_file_attachment_upload_invalid_extension(auth, client):
    """FR-2.3: Disallow unapproved file extensions (e.g. .exe)."""
    auth.login_user()
    category = Category.query.first()

    file_data = (io.BytesIO(b"malicious executable"), "virus.exe")

    response = client.post('/complaint/new', data={
        'subject': 'Invalid attachment test',
        'category_id': category.id,
        'priority': 'Low',
        'location': 'Lab 1',
        'description': 'Attempting to attach .exe file.',
        'attachments': [file_data]
    }, content_type='multipart/form-data', follow_redirects=True)

    assert b'Invalid file format' in response.data or b'Only JPG' in response.data


def test_mark_notifications_as_read(auth, client):
    """FR-5.3: User marks unread in-app notifications as read."""
    auth.login_user()
    user = User.query.filter_by(email='user@example.com').first()

    n1 = Notification(user_id=user.id, message="Notice 1", is_read=False)
    n2 = Notification(user_id=user.id, message="Notice 2", is_read=False)
    db.session.add_all([n1, n2])
    db.session.commit()

    response = client.post('/notifications/mark-read', follow_redirects=True)
    assert response.status_code == 200
    assert b'marked as read' in response.data

    db.session.refresh(n1)
    db.session.refresh(n2)
    assert n1.is_read is True
    assert n2.is_read is True


def test_admin_csv_export_report(auth, client):
    """FR-7.3: Administrator downloads grievance report as formatted CSV."""
    auth.login_admin()
    user = User.query.filter_by(email='user@example.com').first()
    cat = Category.query.first()

    comp = Complaint(
        tracking_number="OCMS-2026-7003",
        user_id=user.id,
        category_id=cat.id,
        title="CSV Export Case",
        description="Export to CSV test",
        status="Submitted",
        priority="High"
    )
    db.session.add(comp)
    db.session.commit()

    response = client.get('/admin/reports?export=csv')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'
    assert b'Tracking Number,Title,Category,Priority,Status' in response.data
    assert b'OCMS-2026-7003' in response.data


def test_audit_trail_recorded_on_admin_action(auth, client):
    """FR-3.10: Admin actions record security audit log entries."""
    auth.login_admin()

    # Trigger admin category creation which creates an audit record
    client.post('/admin/categories/add', data={
        'name': 'Audited Category',
        'description': 'Checking audit log creation',
        'sla_hours': '12'
    }, follow_redirects=True)

    log_entry = AuditLog.query.filter_by(target_id='Audited Category').first()
    assert log_entry is not None
    assert 'Created category' in log_entry.action

"""
Complaint Lifecycle Tests (SRS Section 3.2, 3.5, 3.6).
Tests complaint submission, reference tokens (FR-2.2), withdrawal (FR-2.9),
reopening (FR-2.10), access isolation, and public tracking privacy.
"""

from datetime import datetime, timedelta
from app.models import db, Complaint, ComplaintUpdate, User, Category


def test_submit_complaint_generates_tracking_number(auth, client):
    """FR-2.1 & FR-2.2: Submit complaint creates unique reference number & SLA due date."""
    auth.login_user()
    category = Category.query.filter_by(name="IT & Network Infrastructure").first()

    response = client.post('/complaint/new', data={
        'subject': 'Slow campus Wi-Fi in Hostel Room 101',
        'category_id': category.id,
        'priority': 'High',
        'location': 'Hostel Block B, Room 101',
        'description': 'Speed test shows under 50 Kbps throughout the morning.'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'successfully filed' in response.data or b'Complaint' in response.data

    complaint = Complaint.query.filter_by(title='Slow campus Wi-Fi in Hostel Room 101').first()
    assert complaint is not None
    assert complaint.status == 'Submitted'
    assert complaint.tracking_number.startswith('OCMS-')
    assert complaint.category_id == category.id
    # SLA due date computed (12 hours * 0.5 priority multiplier = 6 hours)
    expected_due = complaint.created_at + timedelta(hours=6)
    assert abs((complaint.due_at - expected_due).total_seconds()) < 60



def test_my_complaints_list_and_status_filtering(auth, client):
    """FR-2.5 & FR-2.6: Complainant views their complaints and filters by status."""
    auth.login_user()
    user = User.query.filter_by(email='user@example.com').first()
    cat = Category.query.first()

    # Create 2 complaints
    c1 = Complaint(
        tracking_number="OCMS-2026-9001",
        user_id=user.id,
        category_id=cat.id,
        title="Issue Alpha",
        description="First issue",
        status="Submitted",
        priority="Medium"
    )
    c2 = Complaint(
        tracking_number="OCMS-2026-9002",
        user_id=user.id,
        category_id=cat.id,
        title="Issue Beta",
        description="Second issue",
        status="Resolved",
        priority="High"
    )
    db.session.add_all([c1, c2])
    db.session.commit()

    # View all
    res_all = client.get('/complaints/my')
    assert b'OCMS-2026-9001' in res_all.data
    assert b'OCMS-2026-9002' in res_all.data

    # Filter by status=Resolved
    res_resolved = client.get('/complaints/my?status=Resolved')
    assert b'OCMS-2026-9002' in res_resolved.data
    assert b'OCMS-2026-9001' not in res_resolved.data


def test_access_isolation_user_cannot_view_others_complaint(auth, client):
    """NFR-4: Complainant cannot view another user's complaint details (403 Forbidden)."""
    user1 = User.query.filter_by(email='user@example.com').first()
    cat = Category.query.first()

    c1 = Complaint(
        tracking_number="OCMS-2026-9003",
        user_id=user1.id,
        category_id=cat.id,
        title="Private Issue",
        description="Confidential data",
        status="Submitted",
        priority="Medium"
    )
    db.session.add(c1)
    db.session.commit()

    # Log in as user2
    auth.login_user2()
    response = client.get('/complaint/OCMS-2026-9003')
    assert response.status_code == 403


def test_withdraw_complaint_when_submitted(auth, client):
    """FR-2.9: Complainant can withdraw complaint before assignment."""
    auth.login_user()
    user = User.query.filter_by(email='user@example.com').first()
    cat = Category.query.first()

    c = Complaint(
        tracking_number="OCMS-2026-9004",
        user_id=user.id,
        category_id=cat.id,
        title="Fixed myself",
        description="Withdraw this",
        status="Submitted",
        priority="Low"
    )
    db.session.add(c)
    db.session.commit()

    response = client.post('/complaint/OCMS-2026-9004/withdraw', follow_redirects=True)
    assert response.status_code == 200
    assert b'withdrawn' in response.data.lower()

    db.session.refresh(c)
    assert c.status == 'Withdrawn'


def test_withdraw_complaint_blocked_when_assigned(auth, client):
    """FR-2.9: Cannot withdraw after technician is assigned."""
    auth.login_user()
    user = User.query.filter_by(email='user@example.com').first()
    staff = User.query.filter_by(email='staff@example.com').first()
    cat = Category.query.first()

    c = Complaint(
        tracking_number="OCMS-2026-9005",
        user_id=user.id,
        category_id=cat.id,
        assigned_to=staff.id,
        title="Already being fixed",
        description="Cannot withdraw",
        status="Assigned",
        priority="High"
    )
    db.session.add(c)
    db.session.commit()

    response = client.post('/complaint/OCMS-2026-9005/withdraw', follow_redirects=True)
    assert b'Submitted' in response.data and b'withdrawn' in response.data

    db.session.refresh(c)
    assert c.status == 'Assigned'


def test_add_comment_to_conversation_thread(auth, client):
    """FR-2.8: Complainant posts message into conversation timeline."""
    auth.login_user()
    user = User.query.filter_by(email='user@example.com').first()
    cat = Category.query.first()

    c = Complaint(
        tracking_number="OCMS-2026-9006",
        user_id=user.id,
        category_id=cat.id,
        title="Router issue",
        description="Check router",
        status="Submitted",
        priority="Medium"
    )
    db.session.add(c)
    db.session.commit()

    response = client.post('/complaint/OCMS-2026-9006/comment', data={
        'message': 'I will be in the hostel room after 4 PM.'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'comment was added' in response.data

    update = ComplaintUpdate.query.filter_by(complaint_id=c.id).first()
    assert update is not None
    assert 'after 4 PM' in update.remark


def test_reopen_resolved_complaint_within_window(auth, client):
    """FR-2.10: Reopen a resolved complaint within 7 days with mandatory reason."""
    auth.login_user()
    user = User.query.filter_by(email='user@example.com').first()
    cat = Category.query.first()

    c = Complaint(
        tracking_number="OCMS-2026-9007",
        user_id=user.id,
        category_id=cat.id,
        title="AC repair",
        description="AC blowing warm air",
        status="Resolved",
        priority="Medium",
        resolved_at=datetime.utcnow() - timedelta(days=2)
    )
    db.session.add(c)
    db.session.commit()

    response = client.post('/complaint/OCMS-2026-9007/reopen', data={
        'reopen_reason': 'The cooling stopped working again this morning.'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'reopened' in response.data.lower()

    db.session.refresh(c)
    assert c.status == 'Reopened'


def test_public_tracking_privacy(client):
    """FR-2.7 & Privacy Rule: Public tracker shows status and timeline, but hides phone/email."""
    user = User.query.filter_by(email='user@example.com').first()
    cat = Category.query.first()

    c = Complaint(
        tracking_number="OCMS-2026-9008",
        user_id=user.id,
        category_id=cat.id,
        title="Publicly Trackable",
        description="Public tracking description details",
        location="Room 204",
        status="In Progress",
        priority="Medium"
    )
    db.session.add(c)
    db.session.commit()

    response = client.get('/track?complaint_no=OCMS-2026-9008')
    assert response.status_code == 200
    assert b'In Progress' in response.data
    assert b'Public tracking description details' in response.data

    # Privacy verification: user's personal phone and email must NOT be revealed publicly
    assert user.email.encode() not in response.data
    assert user.phone.encode() not in response.data

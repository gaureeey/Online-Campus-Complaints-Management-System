"""
Administrator & Staff Workflow Tests (SRS Section 3.3, 3.4, 3.7).
Tests triage, technician assignment (FR-3.3), staff resolution (FR-4.2),
mandatory rejection reasons (FR-4.3), category management & foreign key integrity.
"""

from app.models import db, Complaint, ComplaintUpdate, User, Category


def test_user_blocked_from_admin_dashboard(auth, client):
    """NFR-4: Complainant cannot access administrator dashboard (403 Forbidden)."""
    auth.login_user()
    response = client.get('/admin/dashboard')
    assert response.status_code == 403


def test_user_blocked_from_staff_dashboard(auth, client):
    """NFR-4: Complainant cannot access staff workspace (403 Forbidden)."""
    auth.login_user()
    response = client.get('/staff/dashboard')
    assert response.status_code == 403


def test_admin_assign_staff(auth, client):
    """FR-3.3: Administrator allocates complaint to staff technician."""
    auth.login_admin()
    user = User.query.filter_by(email='user@example.com').first()
    staff = User.query.filter_by(email='staff@example.com').first()
    cat = Category.query.first()

    comp = Complaint(
        tracking_number="OCMS-2026-8001",
        user_id=user.id,
        category_id=cat.id,
        title="Unassigned ticket",
        description="Needs technician",
        status="Submitted",
        priority="Medium"
    )
    db.session.add(comp)
    db.session.commit()

    response = client.post(f'/admin/complaint/{comp.tracking_number}/assign', data={
        'staff_id': staff.id,
        'admin_note': 'High priority triage.'
    }, follow_redirects=True)

    assert response.status_code == 200
    db.session.refresh(comp)
    assert comp.assigned_to == staff.id
    assert comp.status == 'Assigned'


def test_admin_update_status_and_priority(auth, client):
    """FR-3.2 & FR-3.7: Administrator updates priority and adds remark."""
    auth.login_admin()
    user = User.query.filter_by(email='user@example.com').first()
    cat = Category.query.first()

    comp = Complaint(
        tracking_number="OCMS-2026-8002",
        user_id=user.id,
        category_id=cat.id,
        title="Priority review",
        description="Review needed",
        status="Submitted",
        priority="Low"
    )
    db.session.add(comp)
    db.session.commit()

    response = client.post(f'/admin/complaint/{comp.tracking_number}/update-status', data={
        'priority': 'Urgent',
        'status': 'In Progress',
        'admin_remark': 'Escalated due to exam schedule.'
    }, follow_redirects=True)

    assert response.status_code == 200
    db.session.refresh(comp)
    assert comp.priority == 'Urgent'
    assert comp.status == 'In Progress'


def test_staff_assigned_queue(auth, client):
    """FR-4.1: Staff technician dashboard displays assigned complaints."""
    user = User.query.filter_by(email='user@example.com').first()
    staff = User.query.filter_by(email='staff@example.com').first()
    cat = Category.query.first()

    c_assigned = Complaint(
        tracking_number="OCMS-2026-8003",
        user_id=user.id,
        category_id=cat.id,
        assigned_to=staff.id,
        title="Assigned to Staff Priya",
        description="Priya's work queue",
        status="Assigned",
        priority="Medium"
    )
    c_unassigned = Complaint(
        tracking_number="OCMS-2026-8004",
        user_id=user.id,
        category_id=cat.id,
        assigned_to=None,
        title="Not Assigned",
        description="Not for Priya",
        status="Submitted",
        priority="Medium"
    )
    db.session.add_all([c_assigned, c_unassigned])
    db.session.commit()

    auth.login_staff()
    response = client.get('/staff/complaints')
    assert response.status_code == 200
    assert b'OCMS-2026-8003' in response.data
    assert b'OCMS-2026-8004' not in response.data


def test_staff_update_status_to_resolved(auth, client):
    """FR-4.2: Staff member resolves assigned complaint with resolution notes."""
    user = User.query.filter_by(email='user@example.com').first()
    staff = User.query.filter_by(email='staff@example.com').first()
    cat = Category.query.first()

    comp = Complaint(
        tracking_number="OCMS-2026-8005",
        user_id=user.id,
        category_id=cat.id,
        assigned_to=staff.id,
        title="Ethernet cable broken",
        description="Replace patch cord",
        status="In Progress",
        priority="Medium"
    )
    db.session.add(comp)
    db.session.commit()

    auth.login_staff()
    response = client.post(f'/staff/complaint/{comp.tracking_number}/update-status', data={
        'status': 'Resolved',
        'resolution_notes': 'New Cat-6 patch cord installed and verified.'
    }, follow_redirects=True)

    assert response.status_code == 200
    db.session.refresh(comp)
    assert comp.status == 'Resolved'
    assert comp.resolved_at is not None


def test_staff_reject_requires_reason(auth, client):
    """FR-4.3: Rejecting a complaint requires mandatory explanation."""
    user = User.query.filter_by(email='user@example.com').first()
    staff = User.query.filter_by(email='staff@example.com').first()
    cat = Category.query.first()

    comp = Complaint(
        tracking_number="OCMS-2026-8006",
        user_id=user.id,
        category_id=cat.id,
        assigned_to=staff.id,
        title="Invalid request",
        description="Duplicate",
        status="In Progress",
        priority="Low"
    )
    db.session.add(comp)
    db.session.commit()

    auth.login_staff()

    # Attempt to reject with empty reason
    response = client.post(f'/staff/complaint/{comp.tracking_number}/update-status', data={
        'status': 'Rejected',
        'rejection_reason': '',
        'resolution_notes': ''
    }, follow_redirects=True)

    assert b'mandatory written reason' in response.data
    db.session.refresh(comp)
    assert comp.status != 'Rejected'  # Rejected was blocked

    # Now reject with valid reason
    response2 = client.post(f'/staff/complaint/{comp.tracking_number}/update-status', data={
        'status': 'Rejected',
        'rejection_reason': 'Out of scope: Personal laptop hardware fault.'
    }, follow_redirects=True)

    db.session.refresh(comp)
    assert comp.status == 'Rejected'
    assert 'Personal laptop hardware' in comp.rejection_reason


def test_admin_category_crud_and_delete_protection(auth, client):
    """FR-3.4 & DB Integrity: Admin creates, edits, and verifies delete constraint."""
    auth.login_admin()

    # 1. Create Category
    client.post('/admin/categories/add', data={
        'name': 'Gymnasium & Sports',
        'description': 'Gym equipment and court maintenance',
        'sla_hours': '36'
    }, follow_redirects=True)

    cat = Category.query.filter_by(name='Gymnasium & Sports').first()
    assert cat is not None
    assert cat.sla_hours == 36

    # 2. Edit Category
    client.post(f'/admin/categories/{cat.id}/edit', data={
        'name': 'Gymnasium & Sports Updated',
        'description': 'Updated scope',
        'sla_hours': '48',
        'icon': 'bi-trophy'
    }, follow_redirects=True)

    db.session.refresh(cat)
    assert cat.name == 'Gymnasium & Sports Updated'
    assert cat.sla_hours == 48

    # 3. Safe Delete: When no complaints are attached, deletion succeeds
    del_res = client.post(f'/admin/categories/{cat.id}/delete', follow_redirects=True)
    assert b'has been deleted' in del_res.data
    assert Category.query.get(cat.id) is None

    # 4. Integrity Protection: Category with attached complaints cannot be deleted
    cat_with_complaint = Category.query.filter_by(name="IT & Network Infrastructure").first()
    user = User.query.first()
    comp = Complaint(
        tracking_number="OCMS-2026-8007",
        user_id=user.id,
        category_id=cat_with_complaint.id,
        title="Attached ticket",
        description="Blocks deletion",
        status="Submitted",
        priority="Medium"
    )
    db.session.add(comp)
    db.session.commit()

    del_blocked = client.post(f'/admin/categories/{cat_with_complaint.id}/delete', follow_redirects=True)
    assert b'Cannot delete category' in del_blocked.data
    assert Category.query.get(cat_with_complaint.id) is not None

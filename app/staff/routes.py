"""
Staff / Technician Blueprint Routes (SRS Section 3.4).
Restricted to staff officers and administrators (@staff_required).
Implements assigned tasks workspace, progress updates, resolution notes (FR-4.2),
and mandatory rejection reason logging (FR-4.3).
"""

from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import or_

from app.staff import staff_bp
from app.models import db, Complaint, ComplaintUpdate
from app.utils import staff_required, send_notification, record_audit


@staff_bp.route('/staff/dashboard')
@login_required
@staff_required
def staff_dashboard():
    """
    Technician Overview dashboard showing allocated tasks, in-progress queue,
    and completion statistics (FR-4.4).
    """
    staff_id = current_user.id

    # If admin views staff dashboard, show all or their assigned
    if current_user.role == 'admin':
        base_query = Complaint.query
    else:
        base_query = Complaint.query.filter_by(assigned_to=staff_id)

    total_assigned = base_query.count()
    pending_action = base_query.filter(Complaint.status.in_(['Assigned', 'In Progress', 'Under Review'])).count()
    resolved = base_query.filter(Complaint.status.in_(['Resolved', 'Closed'])).count()

    assigned_complaints = base_query.order_by(Complaint.created_at.desc()).limit(10).all()

    stats = {
        'total_assigned': total_assigned,
        'pending_action': pending_action,
        'resolved': resolved,
        'assigned_complaints': assigned_complaints
    }

    return render_template(
        'staff/dashboard.html',
        is_dashboard=True,
        active_page='staff_dashboard',
        stats=stats
    )


@staff_bp.route('/staff/complaints')
@login_required
@staff_required
def staff_complaints():
    """
    Manage assigned grievance tasks with status filtering and search (FR-4.1).
    """
    staff_id = current_user.id
    status_filter = request.args.get('status', 'all').strip()
    search_term = request.args.get('search', '').strip()

    if current_user.role == 'admin':
        query = Complaint.query
    else:
        query = Complaint.query.filter_by(assigned_to=staff_id)

    if status_filter and status_filter != 'all':
        query = query.filter_by(status=status_filter)

    if search_term:
        query = query.filter(
            or_(
                Complaint.tracking_number.ilike(f"%{search_term}%"),
                Complaint.title.ilike(f"%{search_term}%"),
                Complaint.description.ilike(f"%{search_term}%")
            )
        )

    complaints = query.order_by(Complaint.created_at.desc()).all()

    return render_template(
        'staff/complaints.html',
        is_dashboard=True,
        active_page='staff_complaints',
        complaints=complaints,
        current_status=status_filter,
        current_search=search_term
    )


@staff_bp.route('/staff/complaint/<complaint_no>')
@login_required
@staff_required
def staff_complaint_detail(complaint_no):
    """
    Technician resolution workspace for a specific grievance.
    """
    complaint = Complaint.query.filter_by(tracking_number=complaint_no).first_or_404()

    return render_template(
        'staff/complaint_detail.html',
        is_dashboard=True,
        active_page='staff_complaints',
        complaint=complaint
    )


@staff_bp.route('/staff/complaint/<complaint_no>/update-status', methods=['POST'])
@login_required
@staff_required
def staff_update_status(complaint_no):
    """
    Update Status (In Progress, Resolved, Rejected) with Resolution Notes (FR-4.2 & FR-4.3).
    Enforces mandatory rejection explanation if rejected.
    """
    complaint = Complaint.query.filter_by(tracking_number=complaint_no).first_or_404()

    status = request.form.get('status')
    resolution_notes = request.form.get('resolution_notes', '').strip()
    rejection_reason = request.form.get('rejection_reason', '').strip()

    # Mandatory rejection reason validation (FR-4.3)
    if status == 'Rejected' and not (rejection_reason or resolution_notes):
        flash('Rejection requires a mandatory written reason for the citizen (FR-4.3).', 'danger')
        return redirect(url_for('staff.staff_complaint_detail', complaint_no=complaint_no))

    old_status = complaint.status
    complaint.status = status

    if status == 'Rejected':
        complaint.rejection_reason = rejection_reason or resolution_notes
        remark = f"Rejected by technician: {complaint.rejection_reason}"
    elif status == 'Resolved':
        complaint.resolved_at = datetime.utcnow()
        remark = resolution_notes or "Problem resolved on-site by technician."
    else:
        remark = resolution_notes or f"Status changed to {status}."

    # Record in complaint_updates history
    update = ComplaintUpdate(
        complaint_id=complaint.id,
        updated_by=current_user.id,
        old_status=old_status,
        new_status=status,
        remark=remark
    )
    db.session.add(update)

    # In-app notification for the citizen (FR-5.1, FR-5.3)
    send_notification(
        user_id=complaint.user_id,
        message=f"Complaint {complaint.tracking_number} updated to {status}: {remark}",
        complaint_id=complaint.id
    )

    # Security audit trail (FR-3.10)
    record_audit(
        action=f"Staff updated status to {status}",
        target_id=complaint.tracking_number,
        details=remark
    )

    db.session.commit()
    flash(f"Complaint {complaint_no} updated to '{status}'.", "success")
    return redirect(url_for('staff.staff_complaint_detail', complaint_no=complaint_no))

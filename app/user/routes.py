"""
Citizen / Complainant Blueprint Routes (SRS Section 3.2, 3.5, 3.6).
Handles dashboard, complaint filing with file uploads (FR-2.3), tracking,
conversation thread (FR-2.8), feedback rating (FR-6.1), withdrawal, and notifications.
"""

from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, abort, session
from flask_login import login_required, current_user
from sqlalchemy import or_

from app.user import user_bp
from app.models import (
    db, Complaint, ComplaintUpdate, Category,
    Feedback, Notification
)
from app.utils import (
    generate_tracking_number, save_attachment,
    calculate_due_date, send_notification
)


@user_bp.route('/dashboard')
@login_required
def user_dashboard():
    """
    Citizen personal dashboard displaying grievance metrics and recent filings.
    """
    user_id = current_user.id
    total_filed = Complaint.query.filter_by(user_id=user_id).count()
    in_progress = Complaint.query.filter(
        Complaint.user_id == user_id,
        Complaint.status.in_(['Under Review', 'Assigned', 'In Progress', 'Reopened'])
    ).count()
    resolved = Complaint.query.filter(
        Complaint.user_id == user_id,
        Complaint.status.in_(['Resolved', 'Closed'])
    ).count()

    recent_complaints = Complaint.query.filter_by(user_id=user_id)\
        .order_by(Complaint.created_at.desc()).limit(5).all()

    stats = {
        'total': total_filed,
        'in_progress': in_progress,
        'resolved': resolved,
        'recent_complaints': recent_complaints
    }

    return render_template(
        'user/dashboard.html',
        is_dashboard=True,
        active_page='user_dashboard',
        stats=stats
    )


@user_bp.route('/complaints')
@user_bp.route('/complaints/my')
@login_required
def my_complaints():
    """
    Searchable, filterable list of complaints filed by the current user (FR-2.5, FR-2.6).
    """
    user_id = current_user.id
    status_filter = request.args.get('status', 'all').strip()
    priority_filter = request.args.get('priority', 'all').strip()
    search_term = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)

    query = Complaint.query.filter_by(user_id=user_id)

    if status_filter and status_filter != 'all':
        query = query.filter_by(status=status_filter)

    if priority_filter and priority_filter != 'all':
        query = query.filter_by(priority=priority_filter)

    if search_term:
        query = query.filter(
            or_(
                Complaint.tracking_number.ilike(f"%{search_term}%"),
                Complaint.title.ilike(f"%{search_term}%"),
                Complaint.description.ilike(f"%{search_term}%")
            )
        )

    # Order by newest first
    query = query.order_by(Complaint.created_at.desc())
    
    # Simple pagination (NFR-5: 10 per page)
    complaints = query.all()

    return render_template(
        'user/my_complaints.html',
        is_dashboard=True,
        active_page='my_complaints',
        complaints=complaints,
        current_status=status_filter,
        current_priority=priority_filter,
        current_search=search_term
    )


@user_bp.route('/complaint/new', methods=['GET', 'POST'])
@login_required
def submit_complaint():
    """
    Submit a new grievance ticket with secure file upload (FR-2.1, 2.2, 2.3, 2.4).
    """
    categories = Category.query.filter_by(is_active=True).all()

    if request.method == 'POST':
        category_id = request.form.get('category_id', type=int)
        subject = request.form.get('subject', '').strip()
        description = request.form.get('description', '').strip()
        location = request.form.get('location', '').strip()
        priority = request.form.get('priority', 'Medium').strip()
        is_anonymous = bool(request.form.get('is_anonymous'))

        if not category_id or not subject or not description:
            flash('Please fill in the category, title, and description.', 'danger')
            return render_template(
                'user/submit_complaint.html',
                is_dashboard=True,
                active_page='submit_complaint',
                categories=categories
            )

        category = Category.query.get(category_id)
        tracking_no = generate_tracking_number()
        due_at = calculate_due_date(category, priority)

        # Handle file upload (allow JPG, PNG, PDF up to 5 MB per FR-2.3)
        attachment_path = None
        file_obj = request.files.get('attachments')
        if file_obj and file_obj.filename:
            saved_name = save_attachment(file_obj)
            if saved_name:
                attachment_path = saved_name
            else:
                flash('Invalid file format. Only JPG, PNG, and PDF files under 5 MB are accepted.', 'warning')

        new_complaint = Complaint(
            tracking_number=tracking_no,
            user_id=current_user.id,
            category_id=category_id,
            title=subject,
            description=description,
            location=location,
            priority=priority,
            status='Submitted',
            is_anonymous=is_anonymous,
            attachment_path=attachment_path,
            due_at=due_at
        )
        db.session.add(new_complaint)
        db.session.flush()

        # Initial status update history entry
        update = ComplaintUpdate(
            complaint_id=new_complaint.id,
            updated_by=current_user.id,
            old_status=None,
            new_status='Submitted',
            remark="Complaint filed online. Awaiting administrative review."
        )
        db.session.add(update)
        db.session.commit()

        flash(f"Complaint {tracking_no} successfully filed!", "success")
        return redirect(url_for('user.complaint_success', complaint_no=tracking_no))

    return render_template(
        'user/submit_complaint.html',
        is_dashboard=True,
        active_page='submit_complaint',
        categories=categories
    )


@user_bp.route('/complaint/success/<complaint_no>')
@login_required
def complaint_success(complaint_no):
    """
    Submission Confirmation screen displaying Tracking Number and quick actions.
    """
    complaint = Complaint.query.filter_by(tracking_number=complaint_no).first()
    if not complaint:
        return redirect(url_for('user.my_complaints'))

    # Security check: User must own the complaint or be admin/staff
    if current_user.role == 'user' and complaint.user_id != current_user.id:
        abort(403)

    return render_template(
        'user/submit_success.html',
        is_dashboard=True,
        active_page='my_complaints',
        complaint=complaint
    )


@user_bp.route('/complaint/<complaint_no>')
@login_required
def complaint_detail(complaint_no):
    """
    Inspect detailed grievance timeline, remarks, attachments and ratings (FR-2.5).
    Enforces authorization: Complainants can only open their own complaints (NFR-4).
    """
    complaint = Complaint.query.filter_by(tracking_number=complaint_no).first_or_404()

    if current_user.role == 'user' and complaint.user_id != current_user.id:
        abort(403)

    return render_template(
        'user/complaint_details.html',
        is_dashboard=True,
        active_page='my_complaints',
        complaint=complaint
    )


@user_bp.route('/complaint/<complaint_no>/comment', methods=['POST'])
@login_required
def add_comment(complaint_no):
    """
    Post a citizen reply / clarification note into the activity timeline (FR-2.8).
    """
    complaint = Complaint.query.filter_by(tracking_number=complaint_no).first_or_404()

    if current_user.role == 'user' and complaint.user_id != current_user.id:
        abort(403)

    message = request.form.get('message', '').strip()
    if message:
        update = ComplaintUpdate(
            complaint_id=complaint.id,
            updated_by=current_user.id,
            old_status=complaint.status,
            new_status=complaint.status,
            remark=message
        )
        db.session.add(update)
        db.session.commit()
        flash('Your comment was added to the conversation thread.', 'success')

    return redirect(url_for('user.complaint_detail', complaint_no=complaint_no))


@user_bp.route('/complaint/<complaint_no>/feedback', methods=['POST'])
@login_required
def submit_feedback(complaint_no):
    """
    Submit 1-5 star service satisfaction rating and comments once Resolved (FR-6.1).
    """
    complaint = Complaint.query.filter_by(tracking_number=complaint_no).first_or_404()

    if current_user.role == 'user' and complaint.user_id != current_user.id:
        abort(403)

    if complaint.status not in ['Resolved', 'Closed']:
        flash('Feedback can only be submitted after a complaint is marked as Resolved.', 'warning')
        return redirect(url_for('user.complaint_detail', complaint_no=complaint_no))

    if complaint.feedback:
        flash('Feedback has already been submitted for this complaint.', 'warning')
        return redirect(url_for('user.complaint_detail', complaint_no=complaint_no))

    rating = request.form.get('rating', type=int) or 5
    comments = request.form.get('comments', '').strip()

    feedback = Feedback(
        complaint_id=complaint.id,
        user_id=current_user.id,
        rating=rating,
        comment=comments
    )
    db.session.add(feedback)
    db.session.commit()

    flash('Thank you for rating our service! Your feedback helps maintain campus standards.', 'success')
    return redirect(url_for('user.complaint_detail', complaint_no=complaint_no))


@user_bp.route('/complaint/<complaint_no>/withdraw', methods=['POST'])
@login_required
def withdraw_complaint(complaint_no):
    """
    Withdraw a complaint while it remains in Submitted status (FR-2.9).
    """
    complaint = Complaint.query.filter_by(tracking_number=complaint_no).first_or_404()

    if current_user.role == 'user' and complaint.user_id != current_user.id:
        abort(403)

    if complaint.status == 'Submitted':
        old_status = complaint.status
        complaint.status = 'Withdrawn'
        update = ComplaintUpdate(
            complaint_id=complaint.id,
            updated_by=current_user.id,
            old_status=old_status,
            new_status='Withdrawn',
            remark="Complaint withdrawn by user."
        )
        db.session.add(update)
        db.session.commit()
        flash(f"Complaint {complaint_no} has been safely withdrawn.", "info")
    else:
        flash("Complaints can only be withdrawn while in 'Submitted' status.", "warning")

    return redirect(url_for('user.my_complaints'))


@user_bp.route('/complaint/<complaint_no>/reopen', methods=['POST'])
@login_required
def reopen_complaint(complaint_no):
    """
    Reopen a Resolved grievance within 7 days if the problem persists (FR-2.10).
    """
    complaint = Complaint.query.filter_by(tracking_number=complaint_no).first_or_404()

    if current_user.role == 'user' and complaint.user_id != current_user.id:
        abort(403)

    if complaint.status in ['Resolved', 'Closed']:
        reopen_reason = request.form.get('reopen_reason', '').strip() or "Issue persists after repair."
        old_status = complaint.status
        complaint.status = 'Reopened'
        complaint.resolved_at = None

        update = ComplaintUpdate(
            complaint_id=complaint.id,
            updated_by=current_user.id,
            old_status=old_status,
            new_status='Reopened',
            remark=f"Complaint reopened by user: {reopen_reason}"
        )
        db.session.add(update)
        db.session.commit()
        flash(f"Complaint {complaint_no} has been reopened. A technician has been re-alerted.", "warning")
    else:
        flash("Only Resolved complaints can be reopened.", "warning")

    return redirect(url_for('user.complaint_detail', complaint_no=complaint_no))


@user_bp.route('/notifications')
@login_required
def notifications():
    """In-App Notification Center (FR-5.3)."""
    user_notifs = Notification.query.filter_by(user_id=current_user.id)\
        .order_by(Notification.created_at.desc()).all()

    return render_template(
        'user/notifications.html',
        is_dashboard=True,
        active_page='notifications',
        notifications=user_notifs
    )


@user_bp.route('/notifications/mark-read', methods=['POST'])
@login_required
def mark_notifications_read():
    """Mark all active notifications as read."""
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({'is_read': True})
    db.session.commit()
    flash('All notifications marked as read.', 'info')
    return redirect(url_for('user.notifications'))


@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """View and update profile information or change password (FR-1.5)."""
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_profile':
            current_user.name = request.form.get('name', current_user.name).strip()
            current_user.phone = request.form.get('phone', current_user.phone).strip()
            session['user_name'] = current_user.name
            db.session.commit()
            flash('Profile details updated successfully.', 'success')

        elif action == 'change_password':
            curr_pass = request.form.get('current_password', '')
            new_pass = request.form.get('new_password', '')
            confirm_pass = request.form.get('confirm_password', '')

            if not current_user.check_password(curr_pass):
                flash('Current password is incorrect.', 'danger')
            elif new_pass != confirm_pass:
                flash('New passwords do not match.', 'danger')
            elif len(new_pass) < 8 or not any(c.isdigit() for c in new_pass):
                flash('New password must be at least 8 characters long and contain at least one digit.', 'danger')
            else:
                current_user.set_password(new_pass)
                db.session.commit()
                flash('Password updated successfully.', 'success')

        return redirect(url_for('user.profile'))

    return render_template(
        'user/profile.html',
        is_dashboard=True,
        active_page='profile',
        user=current_user
    )

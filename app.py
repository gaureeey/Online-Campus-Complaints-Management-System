"""
Online Complaint Management System (OCMS) - Flask Web Application
Final Year BCA Capstone Project
Conforming to IEEE Std 830-1998 Software Requirements Specification (docs/SRS.pdf)

Frontend Prototype with Mock Data Engine.
Every route includes explicit TODO comments indicating where backend ORM/SQLAlchemy
models, database transactions, bcrypt hashing, and email dispatchers plug in.
"""

import os
from datetime import datetime
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, jsonify
)

import mock_data

app = Flask(__name__)
# Secret key for sessions & flash messages (In production, load from os.environ)
app.secret_key = os.environ.get('SECRET_KEY', 'ocms-capstone-bca-secret-2026-key')

# -------------------------------------------------------------------------
# Template Context Processors
# -------------------------------------------------------------------------
@app.context_processor
def inject_global_template_vars():
    """Make common variables available across all templates automatically."""
    active_role = session.get('role', None)
    return {
        'current_year': 2026,
        'active_role': active_role,
        'categories': mock_data.MOCK_CATEGORIES,
        'unread_notifications_count': 3
    }

# -------------------------------------------------------------------------
# Demo Role Switcher Route (For Project Evaluation & Viva Demo)
# -------------------------------------------------------------------------
@app.route('/switch-role/<role>')
def switch_role(role):
    """
    Demo helper: Quickly toggle the mock session role between:
    - 'guest' (Logged out public visitor)
    - 'user' (Citizen / Complainant: Rahul Sharma)
    - 'staff' (Technician / Field Officer: Priya Nair)
    - 'admin' (System Administrator: Dr. Arvind Mehta)
    """
    if role == 'guest':
        session.clear()
        flash('Switched to Guest (Public Visitor) view.', 'info')
        return redirect(url_for('index'))
    elif role == 'user':
        session['role'] = 'user'
        session['user_id'] = 1
        session['user_name'] = 'Rahul Sharma'
        flash('Switched to Complainant / Citizen persona: Rahul Sharma (Computer Science Student).', 'success')
        return redirect(url_for('user_dashboard'))
    elif role == 'staff':
        session['role'] = 'staff'
        session['user_id'] = 2
        session['user_name'] = 'Priya Nair'
        flash('Switched to Staff Officer persona: Priya Nair (Senior IT & Network Technician).', 'info')
        return redirect(url_for('staff_dashboard'))
    elif role == 'admin':
        session['role'] = 'admin'
        session['user_id'] = 4
        session['user_name'] = 'Dr. Arvind Mehta'
        flash('Switched to Administrator persona: Dr. Arvind Mehta (Chief Administrative Officer).', 'warning')
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('index'))

# =========================================================================
# PUBLIC / VISITOR MODULE (SRS Section 3.1 & 3.2)
# =========================================================================

@app.route('/')
def index():
    """Landing Page (Hero, 4-step workflow, categories, stats counters, CTA)."""
    # TODO Backend: Query dynamic active categories and real aggregate counts from database
    return render_template(
        'public/index.html',
        is_dashboard=False,
        categories=mock_data.MOCK_CATEGORIES
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User / Staff / Admin Login (SRS FR-1.3, FR-1.8 lockout)."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        # TODO Backend:
        # 1. user = User.query.filter_by(email=email).first()
        # 2. Check if user is locked out: user.locked_until > datetime.utcnow() (FR-1.8)
        # 3. Check password: if not bcrypt.check_password_hash(user.password_hash, password):
        #        user.failed_attempts += 1; if >= 5: lock for 15 mins (FR-1.8)
        # 4. login_user(user)

        # Mock authentication logic:
        if 'admin' in email:
            session['role'] = 'admin'
            session['user_id'] = 4
            session['user_name'] = 'Dr. Arvind Mehta'
            flash('Welcome back, Dr. Arvind Mehta (Administrator).', 'success')
            return redirect(url_for('admin_dashboard'))
        elif 'staff' in email or 'priya' in email or 'rajesh' in email:
            session['role'] = 'staff'
            session['user_id'] = 2
            session['user_name'] = 'Priya Nair'
            flash('Welcome back, Priya Nair (Staff Officer).', 'success')
            return redirect(url_for('staff_dashboard'))
        else:
            session['role'] = 'user'
            session['user_id'] = 1
            session['user_name'] = 'Rahul Sharma'
            flash('Welcome back, Rahul Sharma!', 'success')
            return redirect(url_for('user_dashboard'))

    return render_template('public/login.html', is_dashboard=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Complainant Registration (SRS FR-1.1 & FR-1.2 password check)."""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # TODO Backend:
        # 1. Reject duplicate email: if User.query.filter_by(email=email).first(): flash error (TC-1)
        # 2. Check password strength: length >= 8, has digit (FR-1.2)
        # 3. Hash password: pwd_hash = bcrypt.generate_password_hash(password) (FR-1.4)
        # 4. new_user = User(name=name, email=email, phone=phone, password_hash=pwd_hash, role='user')
        # 5. db.session.add(new_user); db.session.commit()

        flash('Registration successful! You can now log in with your credentials.', 'success')
        return redirect(url_for('login'))

    return render_template('public/register.html', is_dashboard=False)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Password Recovery (SRS FR-1.6 time-limited token)."""
    if request.method == 'POST':
        email = request.form.get('email')
        # TODO Backend:
        # 1. user = User.query.filter_by(email=email).first()
        # 2. token = generate_timed_reset_token(user.id, expires_sec=900)
        # 3. send_reset_email(email, token) in background thread (FR-5.4)
        flash(f'A secure password reset link has been dispatched to {email}. Valid for 15 minutes.', 'info')
        return redirect(url_for('login'))

    return render_template('public/forgot_password.html', is_dashboard=False)

@app.route('/track', methods=['GET'])
def track_public():
    """Public Grievance Tracker by Complaint Number."""
    query_no = request.args.get('complaint_no', '').strip()
    complaint = None
    if query_no:
        # TODO Backend: complaint = Complaint.query.filter_by(complaint_no=query_no).first()
        complaint = mock_data.get_complaint_by_no(query_no)

    return render_template(
        'public/track_public.html',
        is_dashboard=False,
        complaint=complaint,
        query_no=query_no
    )

@app.route('/logout')
def logout():
    """User Logout and Session Clear."""
    session.clear()
    flash('You have been safely logged out of your session.', 'info')
    return redirect(url_for('login'))

# =========================================================================
# CITIZEN / USER MODULE (SRS Section 3.2, 3.5, 3.6)
# =========================================================================

@app.route('/dashboard')
def user_dashboard():
    """Citizen Dashboard with aggregate status cards and recent complaints."""
    # Ensure role is set for mock preview
    if not session.get('role'):
        session['role'] = 'user'
        session['user_id'] = 1
        session['user_name'] = 'Rahul Sharma'

    # TODO Backend: Query Complaint counts where user_id == current_user.id
    stats = mock_data.get_user_dashboard_stats(user_id=session.get('user_id', 1))

    return render_template(
        'user/dashboard.html',
        is_dashboard=True,
        active_page='user_dashboard',
        stats=stats
    )

@app.route('/complaints')
@app.route('/complaints/my')
def my_complaints():
    """List Citizen's Complaints with Search & Status Filters (SRS FR-2.5 & FR-2.6)."""
    if not session.get('role'):
        session['role'] = 'user'

    status_filter = request.args.get('status', 'all')
    priority_filter = request.args.get('priority', 'all')
    search_term = request.args.get('search', '').strip()

    # TODO Backend:
    # query = Complaint.query.filter_by(user_id=current_user.id)
    # Apply filters & paginate (10-20 per page per NFR-5)
    complaints = mock_data.get_user_complaints(
        user_id=session.get('user_id', 1),
        status_filter=status_filter,
        priority_filter=priority_filter,
        search_term=search_term
    )

    return render_template(
        'user/my_complaints.html',
        is_dashboard=True,
        active_page='my_complaints',
        complaints=complaints,
        current_status=status_filter,
        current_priority=priority_filter,
        current_search=search_term
    )

@app.route('/complaint/new', methods=['GET', 'POST'])
def submit_complaint():
    """Submit New Complaint with Attachments (SRS FR-2.1, 2.2, 2.3, 2.7, 2.11)."""
    if not session.get('role'):
        session['role'] = 'user'

    if request.method == 'POST':
        subject = request.form.get('subject')
        category_id = request.form.get('category_id')
        priority = request.form.get('priority', 'Medium')
        location = request.form.get('location')
        description = request.form.get('description')
        is_anonymous = bool(request.form.get('is_anonymous'))

        # Generate unique reference token (FR-2.2 e.g. OCMS-2026-0010)
        next_id = len(mock_data.MOCK_COMPLAINTS) + 1
        new_complaint_no = f"OCMS-2026-{next_id:04d}"

        # Category Lookup
        category_name = "General Infrastructure"
        for cat in mock_data.MOCK_CATEGORIES:
            if str(cat["category_id"]) == str(category_id):
                category_name = cat["name"]
                break

        # TODO Backend:
        # 1. Validate file attachments: max 3 files, <= 5MB, JPG/PNG/PDF (FR-2.3 & TC-3)
        # 2. Rename files with uuid4 hash and save in upload_folder (NFR-3)
        # 3. Compute SLA due_at based on Category / Priority (FR-3.7)
        # 4. Insert into complaints table with status='Submitted' (FR-2.4)
        # 5. Dispatch confirmation email (FR-5.1)

        # Append to mock records for immediate testability
        new_comp = {
            "complaint_id": next_id,
            "complaint_no": new_complaint_no,
            "user_id": session.get('user_id', 1),
            "user_name": session.get('user_name', 'Rahul Sharma'),
            "user_email": "rahul.sharma@example.com",
            "user_phone": "+91 98765 43210",
            "category_id": int(category_id) if category_id else 1,
            "category_name": category_name,
            "assigned_to": None,
            "assigned_name": "Unassigned",
            "subject": subject,
            "description": description,
            "location": location,
            "priority": priority,
            "status": "Submitted",
            "is_anonymous": is_anonymous,
            "is_overdue": False,
            "parent_id": None,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "due_at": (datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
            "resolved_at": None,
            "rejection_reason": None,
            "attachments": [],
            "comments": [
                {
                    "comment_id": 99,
                    "user_name": session.get('user_name', 'Rahul Sharma'),
                    "user_role": "user",
                    "message": "Complaint filed online. Awaiting administrative review.",
                    "is_status_change": True,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            ],
            "feedback": None
        }
        mock_data.MOCK_COMPLAINTS.insert(0, new_comp)

        flash(f'Complaint {new_complaint_no} successfully filed!', 'success')
        return redirect(url_for('complaint_success', complaint_no=new_complaint_no))

    return render_template(
        'user/submit_complaint.html',
        is_dashboard=True,
        active_page='submit_complaint',
        categories=mock_data.MOCK_CATEGORIES
    )

@app.route('/complaint/success/<complaint_no>')
def complaint_success(complaint_no):
    """Success Screen displaying Big Tracking Number, Copy button, and Track button."""
    complaint = mock_data.get_complaint_by_no(complaint_no)
    if not complaint:
        return redirect(url_for('my_complaints'))
    return render_template(
        'user/submit_success.html',
        is_dashboard=True,
        active_page='my_complaints',
        complaint=complaint
    )

@app.route('/complaint/<complaint_no>')
def complaint_detail(complaint_no):
    """View Complaint Details, Milestones & Activity Thread (SRS FR-2.5 & 2.8)."""
    complaint = mock_data.get_complaint_by_no(complaint_no)
    if not complaint:
        flash(f'Complaint {complaint_no} was not found.', 'danger')
        return redirect(url_for('my_complaints'))

    # TODO Backend: Verify authorization: current_user.id == complaint.user_id or role in ['admin', 'staff'] (NFR-4)
    return render_template(
        'user/complaint_details.html',
        is_dashboard=True,
        active_page='my_complaints',
        complaint=complaint
    )

@app.route('/complaint/<complaint_no>/comment', methods=['POST'])
def add_comment(complaint_no):
    """Post Reply Comment into Complaint Conversation Thread (SRS FR-2.8)."""
    message = request.form.get('message', '').strip()
    complaint = mock_data.get_complaint_by_no(complaint_no)

    if complaint and message:
        # TODO Backend:
        # comment = Comment(complaint_id=complaint.id, user_id=current_user.id, message=message, is_status_change=False)
        # db.session.add(comment); db.session.commit()
        complaint['comments'].append({
            "comment_id": len(complaint['comments']) + 1,
            "user_name": session.get('user_name', 'Rahul Sharma'),
            "user_role": session.get('role', 'user'),
            "message": message,
            "is_status_change": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        flash('Your comment was added to the conversation thread.', 'success')

    return redirect(url_for('complaint_detail', complaint_no=complaint_no))

@app.route('/complaint/<complaint_no>/feedback', methods=['POST'])
def submit_feedback(complaint_no):
    """Submit 1-5 Star Rating & Review for Resolved Grievance (SRS FR-6.1)."""
    rating = request.form.get('rating')
    comments = request.form.get('comments', '').strip()
    complaint = mock_data.get_complaint_by_no(complaint_no)

    if complaint:
        # TODO Backend:
        # feedback = Feedback(complaint_id=complaint.id, rating=int(rating), comments=comments)
        # db.session.add(feedback); db.session.commit()
        complaint['feedback'] = {
            "feedback_id": 99,
            "rating": int(rating) if rating else 5,
            "comments": comments,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        flash('Thank you for rating our service! Your feedback helps maintain campus standards.', 'success')

    return redirect(url_for('complaint_detail', complaint_no=complaint_no))

@app.route('/complaint/<complaint_no>/withdraw', methods=['POST'])
def withdraw_complaint(complaint_no):
    """Withdraw Complaint before Staff Assignment (SRS FR-2.9)."""
    complaint = mock_data.get_complaint_by_no(complaint_no)
    if complaint and complaint['status'] == 'Submitted':
        # TODO Backend:
        # complaint.status = 'Withdrawn'
        # db.session.commit()
        complaint['status'] = 'Withdrawn'
        complaint['comments'].append({
            "comment_id": len(complaint['comments']) + 1,
            "user_name": session.get('user_name', 'Rahul Sharma'),
            "user_role": "user",
            "message": "Complaint withdrawn by user before assignment.",
            "is_status_change": True,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        flash(f'Complaint {complaint_no} has been withdrawn.', 'info')
    else:
        flash('Complaints can only be withdrawn while in Submitted status.', 'warning')

    return redirect(url_for('my_complaints'))

@app.route('/complaint/<complaint_no>/reopen', methods=['POST'])
def reopen_complaint(complaint_no):
    """Reopen a Resolved Grievance within 7 Days (SRS FR-2.10)."""
    reopen_reason = request.form.get('reopen_reason', '').strip()
    complaint = mock_data.get_complaint_by_no(complaint_no)

    if complaint and complaint['status'] == 'Resolved':
        # TODO Backend:
        # Check if resolved_at is within 7 days
        # complaint.status = 'Reopened'
        # db.session.commit()
        complaint['status'] = 'Reopened'
        complaint['comments'].append({
            "comment_id": len(complaint['comments']) + 1,
            "user_name": session.get('user_name', 'Rahul Sharma'),
            "user_role": "user",
            "message": f"Complaint reopened by user: {reopen_reason}",
            "is_status_change": True,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        flash(f'Complaint {complaint_no} has been reopened. A technician has been re-alerted.', 'warning')
    else:
        flash('Only Resolved complaints within 7 days can be reopened.', 'warning')

    return redirect(url_for('complaint_detail', complaint_no=complaint_no))

@app.route('/notifications')
def notifications():
    """In-App Notification Center (SRS FR-5.3)."""
    role = session.get('role', 'user')
    notifs = mock_data.get_notifications_for_role(role=role)
    return render_template(
        'user/notifications.html',
        is_dashboard=True,
        active_page='notifications',
        notifications=notifs
    )

@app.route('/notifications/mark-read', methods=['POST'])
def mark_notifications_read():
    """Mark all notifications as read."""
    for n in mock_data.MOCK_NOTIFICATIONS:
        n['is_read'] = True
    flash('All notifications marked as read.', 'info')
    return redirect(url_for('notifications'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """View and Edit User Profile / Change Password (SRS FR-1.5)."""
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_profile':
            name = request.form.get('name')
            session['user_name'] = name
            # TODO Backend: update User record in database
            flash('Profile details updated successfully.', 'success')
        elif action == 'change_password':
            # TODO Backend: verify current password hash and update to new salted hash (FR-1.4)
            flash('Password updated successfully.', 'success')
        return redirect(url_for('profile'))

    return render_template(
        'user/profile.html',
        is_dashboard=True,
        active_page='profile'
    )

# =========================================================================
# STAFF / OFFICER MODULE (SRS Section 3.4)
# =========================================================================

@app.route('/staff/dashboard')
def staff_dashboard():
    """Technician Dashboard showing allocated queue and workload metrics (SRS FR-4.4)."""
    if not session.get('role'):
        session['role'] = 'staff'
        session['user_id'] = 2
        session['user_name'] = 'Priya Nair'

    stats = mock_data.get_staff_dashboard_stats(staff_id=session.get('user_id', 2))
    return render_template(
        'staff/dashboard.html',
        is_dashboard=True,
        active_page='staff_dashboard',
        stats=stats
    )

@app.route('/staff/complaints')
def staff_complaints():
    """Staff Assigned Complaints List (SRS FR-4.1)."""
    if not session.get('role'):
        session['role'] = 'staff'
        session['user_id'] = 2

    status_filter = request.args.get('status', 'all')
    search_term = request.args.get('search', '').strip()

    complaints = mock_data.get_staff_complaints(
        staff_id=session.get('user_id', 2),
        status_filter=status_filter,
        search_term=search_term
    )

    return render_template(
        'staff/complaints.html',
        is_dashboard=True,
        active_page='staff_complaints',
        complaints=complaints,
        current_status=status_filter,
        current_search=search_term
    )

@app.route('/staff/complaint/<complaint_no>')
def staff_complaint_detail(complaint_no):
    """Staff Resolution Workspace for a specific complaint."""
    complaint = mock_data.get_complaint_by_no(complaint_no)
    if not complaint:
        flash('Complaint not found.', 'danger')
        return redirect(url_for('staff_complaints'))

    return render_template(
        'staff/complaint_detail.html',
        is_dashboard=True,
        active_page='staff_complaints',
        complaint=complaint
    )

@app.route('/staff/complaint/<complaint_no>/update-status', methods=['POST'])
def staff_update_status(complaint_no):
    """Update Status (In Progress, Resolved, Rejected) & Resolution Notes (SRS FR-4.2 & 4.3)."""
    status = request.form.get('status')
    resolution_notes = request.form.get('resolution_notes', '').strip()
    rejection_reason = request.form.get('rejection_reason', '').strip()

    complaint = mock_data.get_complaint_by_no(complaint_no)
    if complaint:
        # Mandatory rejection reason validation (FR-4.3)
        if status == 'Rejected' and not rejection_reason:
            flash('Rejection requires a mandatory written reason (FR-4.3).', 'danger')
            return redirect(url_for('staff_complaint_detail', complaint_no=complaint_no))

        complaint['status'] = status
        if status == 'Rejected':
            complaint['rejection_reason'] = rejection_reason
        elif status == 'Resolved':
            complaint['resolved_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Record timeline remark
        remark = resolution_notes or f"Status changed to {status}."
        if status == 'Rejected':
            remark = f"Rejected: {rejection_reason}. Notes: {resolution_notes}"

        complaint['comments'].append({
            "comment_id": len(complaint['comments']) + 1,
            "user_name": session.get('user_name', 'Priya Nair (Staff)'),
            "user_role": "staff",
            "message": remark,
            "is_status_change": True,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # TODO Backend:
        # 1. Update Complaint record in db
        # 2. Email user regarding progress / resolution (FR-5.1)
        # 3. Create AuditLog entry (FR-3.10)

        flash(f'Complaint {complaint_no} updated to {status}.', 'success')

    return redirect(url_for('staff_complaint_detail', complaint_no=complaint_no))

# =========================================================================
# ADMINISTRATOR MODULE (SRS Section 3.3 & 3.7)
# =========================================================================

@app.route('/admin/dashboard')
def admin_dashboard():
    """Executive Dashboard with Chart.js Trends & SLA Rates (SRS FR-7.1, 7.4, 7.5)."""
    if not session.get('role'):
        session['role'] = 'admin'
        session['user_id'] = 4
        session['user_name'] = 'Dr. Arvind Mehta'

    admin_stats = mock_data.get_admin_dashboard_stats()
    return render_template(
        'admin/dashboard.html',
        is_dashboard=True,
        active_page='admin_dashboard',
        admin_stats=admin_stats
    )

@app.route('/admin/complaints')
def admin_complaints():
    """Manage All System Grievances with Search & Multi-Filters (SRS FR-3.1)."""
    if not session.get('role'):
        session['role'] = 'admin'

    status_filter = request.args.get('status', 'all')
    category_filter = request.args.get('category', 'all')
    priority_filter = request.args.get('priority', 'all')
    staff_filter = request.args.get('staff', 'all')
    search_term = request.args.get('search', '').strip()

    complaints = mock_data.get_all_complaints(
        status_filter=status_filter,
        category_filter=category_filter,
        priority_filter=priority_filter,
        staff_filter=staff_filter,
        search_term=search_term
    )

    staff_users = [u for u in mock_data.MOCK_USERS if u['role'] == 'staff']

    return render_template(
        'admin/complaints.html',
        is_dashboard=True,
        active_page='admin_complaints',
        complaints=complaints,
        categories=mock_data.MOCK_CATEGORIES,
        staff_users=staff_users,
        current_status=status_filter,
        current_category=category_filter,
        current_priority=priority_filter,
        current_staff=staff_filter,
        current_search=search_term
    )

@app.route('/admin/complaint/<complaint_no>')
def admin_complaint_detail(complaint_no):
    """Admin Master Review & Action View for Complaint (SRS FR-3.2)."""
    complaint = mock_data.get_complaint_by_no(complaint_no)
    if not complaint:
        flash('Complaint not found.', 'danger')
        return redirect(url_for('admin_complaints'))

    staff_users = [u for u in mock_data.MOCK_USERS if u['role'] == 'staff']

    return render_template(
        'admin/complaint_detail.html',
        is_dashboard=True,
        active_page='admin_complaints',
        complaint=complaint,
        staff_users=staff_users
    )

@app.route('/admin/complaint/<complaint_no>/assign', methods=['POST'])
def admin_assign_staff(complaint_no):
    """Assign or Reassign Complaint to Staff Technician (SRS FR-3.3)."""
    staff_id = request.form.get('staff_id')
    admin_note = request.form.get('admin_note', '').strip()
    complaint = mock_data.get_complaint_by_no(complaint_no)

    if complaint and staff_id:
        staff_member = next((u for u in mock_data.MOCK_USERS if str(u['user_id']) == str(staff_id)), None)
        if staff_member:
            complaint['assigned_to'] = int(staff_id)
            complaint['assigned_name'] = staff_member['name']
            if complaint['status'] == 'Submitted':
                complaint['status'] = 'Assigned'

            msg = f"Assigned to {staff_member['name']} ({staff_member['department']})."
            if admin_note:
                msg += f" Note: {admin_note}"

            complaint['comments'].append({
                "comment_id": len(complaint['comments']) + 1,
                "user_name": session.get('user_name', 'Dr. Arvind Mehta (Admin)'),
                "user_role": "admin",
                "message": msg,
                "is_status_change": True,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            # Record Audit Log (FR-3.10)
            mock_data.MOCK_AUDIT_LOGS.insert(0, {
                "log_id": len(mock_data.MOCK_AUDIT_LOGS) + 101,
                "user_name": session.get('user_name', 'Dr. Arvind Mehta'),
                "user_role": "Admin",
                "action": "Assigned Complaint",
                "target_id": complaint_no,
                "details": f"Allocated to {staff_member['name']}",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ip_address": request.remote_addr or "127.0.0.1"
            })

            flash(f'Complaint {complaint_no} assigned to {staff_member["name"]}.', 'success')

    return redirect(url_for('admin_complaint_detail', complaint_no=complaint_no))

@app.route('/admin/complaint/<complaint_no>/update-status', methods=['POST'])
def admin_update_status(complaint_no):
    """Admin Update Status, Priority & Administrative Remark (SRS FR-3.2, 3.6, 3.7)."""
    status = request.form.get('status')
    priority = request.form.get('priority')
    admin_remark = request.form.get('admin_remark', '').strip()
    rejection_reason = request.form.get('rejection_reason', '').strip()
    staff_id = request.form.get('staff_id')

    complaint = mock_data.get_complaint_by_no(complaint_no)
    if complaint:
        if status:
            complaint['status'] = status
        if priority:
            complaint['priority'] = priority
        if status == 'Rejected' and rejection_reason:
            complaint['rejection_reason'] = rejection_reason

        if staff_id:
            staff_member = next((u for u in mock_data.MOCK_USERS if str(u['user_id']) == str(staff_id)), None)
            if staff_member:
                complaint['assigned_to'] = int(staff_id)
                complaint['assigned_name'] = staff_member['name']

        if admin_remark:
            complaint['comments'].append({
                "comment_id": len(complaint['comments']) + 1,
                "user_name": session.get('user_name', 'Dr. Arvind Mehta (Admin)'),
                "user_role": "admin",
                "message": admin_remark,
                "is_status_change": True,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        flash(f'Complaint {complaint_no} successfully updated.', 'success')

    return redirect(url_for('admin_complaint_detail', complaint_no=complaint_no))

@app.route('/admin/complaint/<complaint_no>/merge', methods=['POST'])
def admin_merge_complaint(complaint_no):
    """Merge Duplicate Complaint into Master Ticket (SRS FR-3.9)."""
    parent_complaint_no = request.form.get('parent_complaint_no', '').strip()
    complaint = mock_data.get_complaint_by_no(complaint_no)

    if complaint and parent_complaint_no:
        complaint['status'] = 'Closed'
        complaint['comments'].append({
            "comment_id": len(complaint['comments']) + 1,
            "user_name": session.get('user_name', 'Dr. Arvind Mehta (Admin)'),
            "user_role": "admin",
            "message": f"Merged as duplicate into parent master ticket {parent_complaint_no} (FR-3.9).",
            "is_status_change": True,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        flash(f'Complaint {complaint_no} merged into {parent_complaint_no}.', 'info')

    return redirect(url_for('admin_complaints'))

@app.route('/admin/users')
def admin_users():
    """Manage Users & Staff Accounts (SRS FR-3.5)."""
    return render_template(
        'admin/users.html',
        is_dashboard=True,
        active_page='admin_users',
        users=mock_data.MOCK_USERS
    )

@app.route('/admin/users/add', methods=['POST'])
def admin_add_user():
    """Create New User / Staff Account (SRS FR-3.5)."""
    name = request.form.get('name')
    email = request.form.get('email')
    role = request.form.get('role', 'user')
    department = request.form.get('department')
    phone = request.form.get('phone')

    # Append to mock users list
    new_user = {
        "user_id": len(mock_data.MOCK_USERS) + 1,
        "name": name,
        "email": email,
        "phone": phone,
        "role": role,
        "department": department,
        "is_active": True,
        "avatar": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    mock_data.MOCK_USERS.append(new_user)
    flash(f'Account created for {name} with role {role.upper()}.', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/users/<int:user_id>/edit', methods=['POST'])
def admin_edit_user(user_id):
    """Edit User / Staff Account Details (SRS FR-3.5)."""
    user = next((u for u in mock_data.MOCK_USERS if u['user_id'] == user_id), None)
    if user:
        user['name'] = request.form.get('name')
        user['role'] = request.form.get('role')
        user['department'] = request.form.get('department')
        user['phone'] = request.form.get('phone')
        flash(f'Account details updated for {user["name"]}.', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/users/<int:user_id>/toggle', methods=['POST'])
def admin_toggle_user(user_id):
    """Activate / Deactivate User Account (SRS FR-3.5)."""
    user = next((u for u in mock_data.MOCK_USERS if u['user_id'] == user_id), None)
    if user:
        user['is_active'] = not user['is_active']
        state = "activated" if user['is_active'] else "deactivated"
        flash(f'User {user["name"]} has been {state}.', 'warning')
    return redirect(url_for('admin_users'))

@app.route('/admin/categories')
def admin_categories():
    """Manage Categories & SLA Configuration (SRS FR-3.4 & FR-3.7)."""
    return render_template(
        'admin/categories.html',
        is_dashboard=True,
        active_page='admin_categories',
        categories=mock_data.MOCK_CATEGORIES
    )

@app.route('/admin/categories/add', methods=['POST'])
def admin_add_category():
    """Add Complaint Category with Target SLA (SRS FR-3.4)."""
    name = request.form.get('name')
    description = request.form.get('description')
    sla_hours = int(request.form.get('sla_hours', 24))
    icon = request.form.get('icon', 'bi-gear')

    new_cat = {
        "category_id": len(mock_data.MOCK_CATEGORIES) + 1,
        "name": name,
        "description": description,
        "icon": icon,
        "sla_hours": sla_hours,
        "default_priority": "Medium",
        "is_active": True,
        "complaint_count": 0
    }
    mock_data.MOCK_CATEGORIES.append(new_cat)
    flash(f'Category "{name}" created with {sla_hours}h SLA.', 'success')
    return redirect(url_for('admin_categories'))

@app.route('/admin/categories/<int:category_id>/edit', methods=['POST'])
def admin_edit_category(category_id):
    """Edit Category Details and SLA (SRS FR-3.4)."""
    cat = next((c for c in mock_data.MOCK_CATEGORIES if c['category_id'] == category_id), None)
    if cat:
        cat['name'] = request.form.get('name')
        cat['description'] = request.form.get('description')
        cat['sla_hours'] = int(request.form.get('sla_hours', 24))
        cat['icon'] = request.form.get('icon', 'bi-gear')
        flash(f'Category "{cat["name"]}" updated.', 'success')
    return redirect(url_for('admin_categories'))

@app.route('/admin/categories/<int:category_id>/toggle', methods=['POST'])
def admin_toggle_category(category_id):
    """Toggle Category Active / Inactive (SRS FR-3.4)."""
    cat = next((c for c in mock_data.MOCK_CATEGORIES if c['category_id'] == category_id), None)
    if cat:
        cat['is_active'] = not cat['is_active']
        state = "activated" if cat['is_active'] else "deactivated"
        flash(f'Category "{cat["name"]}" {state}.', 'info')
    return redirect(url_for('admin_categories'))

@app.route('/admin/reports')
def admin_reports():
    """Date-Range Filtered Reports & Export to CSV/PDF (SRS FR-7.2 & FR-7.3)."""
    category_filter = request.args.get('category', 'all')
    status_filter = request.args.get('status', 'all')

    complaints = mock_data.get_all_complaints(
        status_filter=status_filter,
        category_filter=category_filter
    )

    return render_template(
        'admin/reports.html',
        is_dashboard=True,
        active_page='admin_reports',
        complaints=complaints,
        categories=mock_data.MOCK_CATEGORIES,
        current_category=category_filter,
        current_status=status_filter
    )

@app.route('/admin/audit-log')
def admin_audit_log():
    """Security Audit Trail of Administrative Actions (SRS FR-3.10)."""
    return render_template(
        'admin/audit_log.html',
        is_dashboard=True,
        active_page='admin_audit_log',
        audit_logs=mock_data.MOCK_AUDIT_LOGS
    )

# -------------------------------------------------------------------------
# Application Entry Point
# -------------------------------------------------------------------------
def get_available_port(default_port=5000):
    """Check if default port is free, otherwise select 5050 or fallback."""
    import socket
    target_port = int(os.environ.get('PORT', default_port))
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex(('127.0.0.1', target_port)) != 0:
                return target_port
    except Exception:
        pass
    return 5050

if __name__ == '__main__':
    port = get_available_port(5000)
    print("=" * 70)
    print("Online Complaint Management System (OCMS)")
    print("Final Year BCA Capstone Project - Frontend Server")
    print(f"Starting server at: http://127.0.0.1:{port}")
    print("=" * 70)
    app.run(host='127.0.0.1', port=port, debug=False)


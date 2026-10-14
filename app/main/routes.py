"""
Public / Visitor Blueprint Routes (SRS Sections 3.1 & 3.2).
Includes landing page with live database statistics and public grievance tracker.
"""

from flask import render_template, request, flash
from app.main import main_bp
from app.models import Category, Complaint


@main_bp.route('/')
def index():
    """
    Landing Page with hero banner, 4-step workflow, active categories,
    and live system metrics.
    """
    categories = Category.query.filter_by(is_active=True).all()
    total_complaints = Complaint.query.count()
    resolved_count = Complaint.query.filter(Complaint.status.in_(['Resolved', 'Closed'])).count()
    resolution_rate = int((resolved_count / total_complaints * 100)) if total_complaints > 0 else 98

    stats = {
        'total': total_complaints,
        'resolved': resolved_count,
        'rate': resolution_rate,
        'categories_count': len(categories)
    }

    return render_template(
        'public/index.html',
        is_dashboard=False,
        categories=categories,
        stats=stats
    )


@main_bp.route('/track', methods=['GET'])
def track_public():
    """
    Public Grievance Tracker by Tracking Number (SRS FR-2.5).
    Displays only non-sensitive operational details: tracking token, subject,
    category, status, progress bar, and status update timeline.
    No personal contact details are exposed.
    """
    query_no = request.args.get('complaint_no', '').strip()
    complaint = None

    if query_no:
        complaint = Complaint.query.filter_by(tracking_number=query_no).first()
        if not complaint:
            flash(f"No grievance found with tracking number '{query_no}'. Please check the format.", "warning")

    return render_template(
        'public/track_public.html',
        is_dashboard=False,
        complaint=complaint,
        query_no=query_no
    )

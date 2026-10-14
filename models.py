"""
Re-export SQLAlchemy database models from app.models for top-level convenience.
"""

from app.models import (
    db,
    SliceableDateTime,
    SliceableDateTimeType,
    User,
    Department,
    Category,
    Complaint,
    ComplaintUpdate,
    Feedback,
    Notification,
    AuditLog
)

__all__ = [
    'db',
    'SliceableDateTime',
    'SliceableDateTimeType',
    'User',
    'Department',
    'Category',
    'Complaint',
    'ComplaintUpdate',
    'Feedback',
    'Notification',
    'AuditLog'
]

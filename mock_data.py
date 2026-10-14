"""
Mock Data Module for Online Complaint Management System (OCMS)
Based on SRS specifications (IEEE 830-1998 aligned)
Provides rich mock datasets for frontend UI testing and prototyping
prior to database integration.
"""

from datetime import datetime, timedelta

# Mock Users adhering to SRS Table: users
MOCK_USERS = [
    {
        "user_id": 1,
        "name": "Rahul Sharma",
        "email": "rahul.sharma@example.com",
        "phone": "+91 98765 43210",
        "role": "user",
        "department": "Computer Science (Student)",
        "is_active": True,
        "avatar": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80",
        "created_at": "2026-08-15 10:30:00"
    },
    {
        "user_id": 2,
        "name": "Priya Nair",
        "email": "priya.nair@campus.edu",
        "phone": "+91 98111 22334",
        "role": "staff",
        "department": "IT & Network Infrastructure",
        "is_active": True,
        "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=150&q=80",
        "created_at": "2026-07-10 09:00:00"
    },
    {
        "user_id": 3,
        "name": "Rajesh Kumar",
        "email": "rajesh.kumar@campus.edu",
        "phone": "+91 98222 33445",
        "role": "staff",
        "department": "Hostel & Maintenance Civil Works",
        "is_active": True,
        "avatar": "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?auto=format&fit=crop&w=150&q=80",
        "created_at": "2026-07-12 11:15:00"
    },
    {
        "user_id": 4,
        "name": "Dr. Arvind Mehta",
        "email": "admin@campus.edu",
        "phone": "+91 98999 88776",
        "role": "admin",
        "department": "Campus Administration & Grievance Cell",
        "is_active": True,
        "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=150&q=80",
        "created_at": "2026-06-01 08:30:00"
    },
    {
        "user_id": 5,
        "name": "Ananya Sen",
        "email": "ananya.sen@example.com",
        "phone": "+91 97333 44556",
        "role": "user",
        "department": "BCA 3rd Year (Resident Block B)",
        "is_active": True,
        "avatar": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&w=150&q=80",
        "created_at": "2026-09-02 14:20:00"
    },
    {
        "user_id": 6,
        "name": "Suresh Verma",
        "email": "suresh.verma@campus.edu",
        "phone": "+91 97444 55667",
        "role": "staff",
        "department": "Electrical & Power Systems",
        "is_active": False,
        "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=150&q=80",
        "created_at": "2026-07-20 16:45:00"
    }
]

# Mock Categories adhering to SRS Table: categories with SLA rules
MOCK_CATEGORIES = [
    {
        "category_id": 1,
        "name": "IT & Network Infrastructure",
        "description": "Wi-Fi connectivity, LAN ports, router issues, laboratory computing, lab projectors, and portal access.",
        "icon": "bi-wifi",
        "sla_hours": 24,
        "default_priority": "High",
        "is_active": True,
        "complaint_count": 14
    },
    {
        "category_id": 2,
        "name": "Hostels & Accommodation",
        "description": "Room amenities, furniture damage, room locks, hygiene, corridor lighting, and hostel warden issues.",
        "icon": "bi-building",
        "sla_hours": 48,
        "default_priority": "Medium",
        "is_active": True,
        "complaint_count": 22
    },
    {
        "category_id": 3,
        "name": "Electrical & Power Supply",
        "description": "Power outages, switchboard repairs, ceiling fans, street lights, voltage fluctuations, generator backups.",
        "icon": "bi-lightning-charge",
        "sla_hours": 12,
        "default_priority": "Urgent",
        "is_active": True,
        "complaint_count": 18
    },
    {
        "category_id": 4,
        "name": "Water Supply & Sanitation",
        "description": "Plumbing, drinking water purifiers, washroom hygiene, water shortages, leakage, drainage blockages.",
        "icon": "bi-droplet-half",
        "sla_hours": 24,
        "default_priority": "High",
        "is_active": True,
        "complaint_count": 19
    },
    {
        "category_id": 5,
        "name": "Academic & Library Facilities",
        "description": "Classroom seating, audio/visual podiums, digital library access, library books, exam hall facilities.",
        "icon": "bi-book",
        "sla_hours": 72,
        "default_priority": "Low",
        "is_active": True,
        "complaint_count": 9
    },
    {
        "category_id": 6,
        "name": "Transport & Parking",
        "description": "Campus shuttle routes, vehicle parking permits, bicycle stands, and security barrier malfunctions.",
        "icon": "bi-bus-front",
        "sla_hours": 96,
        "default_priority": "Low",
        "is_active": True,
        "complaint_count": 7
    },
    {
        "category_id": 7,
        "name": "Canteen & Food Quality",
        "description": "Mess food hygiene, pricing complaints, drinking water cleanliness, and meal timings.",
        "icon": "bi-cup-hot",
        "sla_hours": 24,
        "default_priority": "High",
        "is_active": True,
        "complaint_count": 11
    }
]

# Mock Complaints covering all 8 states in SRS Section 6.3 & Appendix A:
# Submitted, Assigned, In Progress, Resolved, Closed, Rejected, Withdrawn, Reopened + Overdue
MOCK_COMPLAINTS = [
    {
        "complaint_id": 1,
        "complaint_no": "OCMS-2026-0001",
        "user_id": 1,
        "user_name": "Rahul Sharma",
        "user_email": "rahul.sharma@example.com",
        "user_phone": "+91 98765 43210",
        "category_id": 1,
        "category_name": "IT & Network Infrastructure",
        "assigned_to": 2,
        "assigned_name": "Priya Nair",
        "subject": "CS Lab 3 High-Speed Wi-Fi Router Down",
        "description": "The primary wireless access point in CS Lab 3 (Block A, 2nd Floor) has been unreachable since this morning. Over 45 students working on final semester lab practicals cannot connect to the internal network repository. Amber light blinking continuously on the Cisco AP.",
        "location": "Block A, 2nd Floor, Room CS-204",
        "priority": "Urgent",
        "status": "In Progress",
        "is_anonymous": False,
        "is_overdue": False,
        "parent_id": None,
        "created_at": "2026-10-14 09:15:00",
        "due_at": "2026-10-15 09:15:00",
        "resolved_at": None,
        "rejection_reason": None,
        "attachments": [
            {
                "attachment_id": 101,
                "file_name": "router_error_light.jpg",
                "file_size": "2.1 MB",
                "file_type": "image/jpeg",
                "url": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=600&q=80"
            },
            {
                "attachment_id": 102,
                "file_name": "ping_timeout_logs.png",
                "file_size": "480 KB",
                "file_type": "image/png",
                "url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=600&q=80"
            }
        ],
        "comments": [
            {
                "comment_id": 1,
                "user_name": "Rahul Sharma",
                "user_role": "user",
                "message": "Complaint filed with system diagnostic logs attached.",
                "is_status_change": True,
                "created_at": "2026-10-14 09:15:00"
            },
            {
                "comment_id": 2,
                "user_name": "Dr. Arvind Mehta (Admin)",
                "user_role": "admin",
                "message": "Reviewed. Priority set to Urgent due to pending exam practicals. Assigned to Priya Nair (Senior Network Tech).",
                "is_status_change": True,
                "created_at": "2026-10-14 09:40:00"
            },
            {
                "comment_id": 3,
                "user_name": "Priya Nair (Staff)",
                "user_role": "staff",
                "message": "Inspected the switch rack. The uplink PoE injector failed. Replacement unit requested from inventory. Estimated fix time: 2 hours.",
                "is_status_change": False,
                "created_at": "2026-10-14 11:20:00"
            }
        ],
        "feedback": None
    },
    {
        "complaint_id": 2,
        "complaint_no": "OCMS-2026-0002",
        "user_id": 1,
        "user_name": "Rahul Sharma",
        "user_email": "rahul.sharma@example.com",
        "user_phone": "+91 98765 43210",
        "category_id": 4,
        "category_name": "Water Supply & Sanitation",
        "assigned_to": None,
        "assigned_name": "Unassigned",
        "subject": "Severe Water Pipe Leakage in Hostel B Washroom",
        "description": "Continuous water leakage from the main overhead pipe junction in the 1st floor bathroom of Hostel Block B. Water is overflowing into the corridor creating slippery hazard for residents.",
        "location": "Hostel Block B, 1st Floor East Wing Washroom",
        "priority": "High",
        "status": "Submitted",
        "is_anonymous": False,
        "is_overdue": False,
        "parent_id": None,
        "created_at": "2026-10-14 14:00:00",
        "due_at": "2026-10-16 14:00:00",
        "resolved_at": None,
        "rejection_reason": None,
        "attachments": [
            {
                "attachment_id": 103,
                "file_name": "pipe_burst_photo.jpg",
                "file_size": "3.4 MB",
                "file_type": "image/jpeg",
                "url": "https://images.unsplash.com/photo-1585704032915-c3400ca199e7?auto=format&fit=crop&w=600&q=80"
            }
        ],
        "comments": [
            {
                "comment_id": 4,
                "user_name": "Rahul Sharma",
                "user_role": "user",
                "message": "Complaint submitted online. Awaiting admin review.",
                "is_status_change": True,
                "created_at": "2026-10-14 14:00:00"
            }
        ],
        "feedback": None
    },
    {
        "complaint_id": 3,
        "complaint_no": "OCMS-2026-0003",
        "user_id": 1,
        "user_name": "Rahul Sharma",
        "user_email": "rahul.sharma@example.com",
        "user_phone": "+91 98765 43210",
        "category_id": 3,
        "category_name": "Electrical & Power Supply",
        "assigned_to": 3,
        "assigned_name": "Rajesh Kumar",
        "subject": "Seminar Hall 1 Projector Bulb Replacement",
        "description": "Seminar Hall projector lamp has reached end of life and shuts down every 10 minutes with an overheating warning buzzer during presentations.",
        "location": "Main Administrative Block, Seminar Hall 1",
        "priority": "Medium",
        "status": "Resolved",
        "is_anonymous": False,
        "is_overdue": False,
        "parent_id": None,
        "created_at": "2026-10-10 11:00:00",
        "due_at": "2026-10-12 11:00:00",
        "resolved_at": "2026-10-11 16:30:00",
        "rejection_reason": None,
        "attachments": [],
        "comments": [
            {
                "comment_id": 5,
                "user_name": "Rahul Sharma",
                "user_role": "user",
                "message": "Complaint logged for AV maintenance.",
                "is_status_change": True,
                "created_at": "2026-10-10 11:00:00"
            },
            {
                "comment_id": 6,
                "user_name": "Rajesh Kumar (Staff)",
                "user_role": "staff",
                "message": "Assigned and inspected. Replaced projector halogen lamp assembly with OEM module. Tested continuous projection for 45 mins without issues.",
                "is_status_change": True,
                "created_at": "2026-10-11 16:30:00"
            }
        ],
        "feedback": {
            "feedback_id": 1,
            "rating": 5,
            "comments": "Prompt and excellent service! Replaced before our seminar.",
            "created_at": "2026-10-12 09:30:00"
        }
    },
    {
        "complaint_id": 4,
        "complaint_no": "OCMS-2026-0004",
        "user_id": 5,
        "user_name": "Ananya Sen",
        "user_email": "ananya.sen@example.com",
        "user_phone": "+91 97333 44556",
        "category_id": 3,
        "category_name": "Electrical & Power Supply",
        "assigned_to": 3,
        "assigned_name": "Rajesh Kumar",
        "subject": "Campus Perimeter Streetlights Dark Near Gate 2",
        "description": "Five consecutive street solar light poles between Girl's Hostel B and Gate 2 are completely dead for 3 nights. Poses severe safety hazard for students walking back from late library hours.",
        "location": "South Perimeter Pathway, between Gate 2 & Hostel B",
        "priority": "Urgent",
        "status": "In Progress",
        "is_anonymous": False,
        "is_overdue": True,  # Overdue flag set! SLA deadline passed
        "parent_id": None,
        "created_at": "2026-10-11 08:00:00",
        "due_at": "2026-10-12 08:00:00",  # Passed
        "resolved_at": None,
        "rejection_reason": None,
        "attachments": [],
        "comments": [
            {
                "comment_id": 7,
                "user_name": "System Scheduler",
                "user_role": "system",
                "message": "ALERT: Complaint has breached its 24h Urgent SLA deadline. Escalated to Chief Administrator.",
                "is_status_change": True,
                "created_at": "2026-10-12 08:00:00"
            },
            {
                "comment_id": 8,
                "user_name": "Rajesh Kumar (Staff)",
                "user_role": "staff",
                "message": "Underground cable fault identified near drainage trench. PWD digging crew arranged for tomorrow morning.",
                "is_status_change": False,
                "created_at": "2026-10-13 14:10:00"
            }
        ],
        "feedback": None
    },
    {
        "complaint_id": 5,
        "complaint_no": "OCMS-2026-0005",
        "user_id": 5,
        "user_name": "Ananya Sen",
        "user_email": "ananya.sen@example.com",
        "user_phone": "+91 97333 44556",
        "category_id": 2,
        "category_name": "Hostels & Accommodation",
        "assigned_to": 3,
        "assigned_name": "Rajesh Kumar",
        "subject": "Room 304 Window Glass Shuttered by Storm",
        "description": "Heavy gale storm cracked the outer window pane in Room 304. Rainwater enters the study table area.",
        "location": "Hostel B, Room 304",
        "priority": "Medium",
        "status": "Assigned",
        "is_anonymous": False,
        "is_overdue": False,
        "parent_id": None,
        "created_at": "2026-10-13 16:30:00",
        "due_at": "2026-10-15 16:30:00",
        "resolved_at": None,
        "rejection_reason": None,
        "attachments": [],
        "comments": [
            {
                "comment_id": 9,
                "user_name": "Dr. Arvind Mehta (Admin)",
                "user_role": "admin",
                "message": "Assigned to Carpentry & Glazing team (Rajesh Kumar).",
                "is_status_change": True,
                "created_at": "2026-10-13 17:00:00"
            }
        ],
        "feedback": None
    },
    {
        "complaint_id": 6,
        "complaint_no": "OCMS-2026-0006",
        "user_id": 1,
        "user_name": "Rahul Sharma",
        "user_email": "rahul.sharma@example.com",
        "user_phone": "+91 98765 43210",
        "category_id": 1,
        "category_name": "IT & Network Infrastructure",
        "assigned_to": 2,
        "assigned_name": "Priya Nair",
        "subject": "Request for personal laptop operating system re-installation",
        "description": "My personal MacBook laptop is running slow and needs Windows dual-boot configuration.",
        "location": "Student Personal Device",
        "priority": "Low",
        "status": "Rejected",
        "is_anonymous": False,
        "is_overdue": False,
        "parent_id": None,
        "created_at": "2026-10-09 10:00:00",
        "due_at": "2026-10-13 10:00:00",
        "resolved_at": "2026-10-09 12:15:00",
        "rejection_reason": "Out of Scope (SRS Section 1.2): Campus IT department provides maintenance exclusively for college-owned equipment and lab infrastructure, not private student devices.",
        "attachments": [],
        "comments": [
            {
                "comment_id": 10,
                "user_name": "Priya Nair (Staff)",
                "user_role": "staff",
                "message": "Complaint rejected: Out of Scope. Private equipment servicing is not permitted under university IT policy.",
                "is_status_change": True,
                "created_at": "2026-10-09 12:15:00"
            }
        ],
        "feedback": None
    },
    {
        "complaint_id": 7,
        "complaint_no": "OCMS-2026-0007",
        "user_id": 1,
        "user_name": "Rahul Sharma",
        "user_email": "rahul.sharma@example.com",
        "user_phone": "+91 98765 43210",
        "category_id": 4,
        "category_name": "Water Supply & Sanitation",
        "assigned_to": 3,
        "assigned_name": "Rajesh Kumar",
        "subject": "Hostel A Water Cooler RO Filter Replacement",
        "description": "TDS reading on the drinking water purifier in Hostel A Ground Floor is 480 PPM. Carbon cartridge requires routine replacement.",
        "location": "Hostel A, Ground Floor Mess Entrance",
        "priority": "Low",
        "status": "Closed",
        "is_anonymous": False,
        "is_overdue": False,
        "parent_id": None,
        "created_at": "2026-09-25 10:00:00",
        "due_at": "2026-09-29 10:00:00",
        "resolved_at": "2026-09-27 15:00:00",
        "rejection_reason": None,
        "attachments": [],
        "comments": [
            {
                "comment_id": 11,
                "user_name": "Rajesh Kumar (Staff)",
                "user_role": "staff",
                "message": "Replaced both sediment and active carbon candle filters. TDS calibrated to 110 PPM.",
                "is_status_change": True,
                "created_at": "2026-09-27 15:00:00"
            },
            {
                "comment_id": 12,
                "user_name": "System Scheduler",
                "user_role": "system",
                "message": "Complaint automatically marked Closed after 7 days of successful resolution (FR-6.2).",
                "is_status_change": True,
                "created_at": "2026-10-04 15:00:00"
            }
        ],
        "feedback": {
            "feedback_id": 2,
            "rating": 4,
            "comments": "Water tastes much better now. Thank you.",
            "created_at": "2026-09-28 11:20:00"
        }
    },
    {
        "complaint_id": 8,
        "complaint_no": "OCMS-2026-0008",
        "user_id": 1,
        "user_name": "Rahul Sharma",
        "user_email": "rahul.sharma@example.com",
        "user_phone": "+91 98765 43210",
        "category_id": 7,
        "category_name": "Canteen & Food Quality",
        "assigned_to": 2,
        "assigned_name": "Priya Nair",
        "subject": "Mess Dining Hall Hygiene & Cold Food Service",
        "description": "Evening snacks served cold and water glasses were unwashed during dinner. Issue previously marked resolved but recurred on Tuesday.",
        "location": "Central Dining Hall, Block 2",
        "priority": "High",
        "status": "Reopened",
        "is_anonymous": True,  # Anonymous complaint (FR-2.11)
        "is_overdue": False,
        "parent_id": None,
        "created_at": "2026-10-08 19:30:00",
        "due_at": "2026-10-15 19:30:00",
        "resolved_at": None,
        "rejection_reason": None,
        "attachments": [],
        "comments": [
            {
                "comment_id": 13,
                "user_name": "Anonymous User",
                "user_role": "user",
                "message": "Reopened within 7 days per FR-2.10: Sanitation issues noticed again on Oct 12 dinner shift.",
                "is_status_change": True,
                "created_at": "2026-10-13 08:30:00"
            }
        ],
        "feedback": None
    },
    {
        "complaint_id": 9,
        "complaint_no": "OCMS-2026-0009",
        "user_id": 1,
        "user_name": "Rahul Sharma",
        "user_email": "rahul.sharma@example.com",
        "user_phone": "+91 98765 43210",
        "category_id": 5,
        "category_name": "Academic & Library Facilities",
        "assigned_to": None,
        "assigned_name": "Unassigned",
        "subject": "Duplicate request: Library book return scanner",
        "description": "Scanner wasn't reading barcode. Realized librarian had already reset the scanner. Withdrawing complaint.",
        "location": "Central Library, Ground Floor",
        "priority": "Low",
        "status": "Withdrawn",
        "is_anonymous": False,
        "is_overdue": False,
        "parent_id": None,
        "created_at": "2026-10-14 11:00:00",
        "due_at": "2026-10-18 11:00:00",
        "resolved_at": None,
        "rejection_reason": None,
        "attachments": [],
        "comments": [
            {
                "comment_id": 14,
                "user_name": "Rahul Sharma",
                "user_role": "user",
                "message": "Complaint withdrawn by user before assignment (FR-2.9).",
                "is_status_change": True,
                "created_at": "2026-10-14 11:15:00"
            }
        ],
        "feedback": None
    }
]

# Mock Notifications adhering to SRS FR-5.3
MOCK_NOTIFICATIONS = [
    {
        "notification_id": 1,
        "user_id": 1,
        "role": "user",
        "complaint_no": "OCMS-2026-0001",
        "title": "Status Updated: In Progress",
        "message": "Staff Priya Nair began working on 'CS Lab 3 High-Speed Wi-Fi Router Down'.",
        "time_ago": "2 hours ago",
        "is_read": False,
        "icon": "bi-arrow-repeat",
        "badge": "primary"
    },
    {
        "notification_id": 2,
        "user_id": 1,
        "role": "user",
        "complaint_no": "OCMS-2026-0002",
        "title": "Complaint Submitted",
        "message": "Your complaint OCMS-2026-0002 was recorded. Expected response within 48 hours.",
        "time_ago": "3 hours ago",
        "is_read": False,
        "icon": "bi-check2-circle",
        "badge": "success"
    },
    {
        "notification_id": 3,
        "user_id": 1,
        "role": "user",
        "complaint_no": "OCMS-2026-0003",
        "title": "Feedback Requested",
        "message": "OCMS-2026-0003 has been marked Resolved. Please rate our service.",
        "time_ago": "2 days ago",
        "is_read": True,
        "icon": "bi-star-fill",
        "badge": "warning"
    },
    {
        "notification_id": 4,
        "user_id": 2,
        "role": "staff",
        "complaint_no": "OCMS-2026-0001",
        "title": "New Assignment: Urgent",
        "message": "Admin assigned you complaint OCMS-2026-0001. SLA: 24 Hours.",
        "time_ago": "4 hours ago",
        "is_read": False,
        "icon": "bi-person-check",
        "badge": "danger"
    },
    {
        "notification_id": 5,
        "user_id": 4,
        "role": "admin",
        "complaint_no": "OCMS-2026-0004",
        "title": "SLA Escalation Alert",
        "message": "Complaint OCMS-2026-0004 has breached SLA. Marked as Overdue.",
        "time_ago": "1 day ago",
        "is_read": False,
        "icon": "bi-exclamation-triangle-fill",
        "badge": "danger"
    }
]

# Mock Audit Log adhering to SRS FR-3.10
MOCK_AUDIT_LOGS = [
    {
        "log_id": 101,
        "user_name": "Dr. Arvind Mehta",
        "user_role": "Admin",
        "action": "Assigned Complaint",
        "target_id": "OCMS-2026-0001",
        "details": "Assigned to staff Priya Nair with priority 'Urgent'",
        "timestamp": "2026-10-14 09:40:00",
        "ip_address": "192.168.1.15"
    },
    {
        "log_id": 102,
        "user_name": "Priya Nair",
        "user_role": "Staff",
        "action": "Updated Status",
        "target_id": "OCMS-2026-0001",
        "details": "Changed status from 'Assigned' to 'In Progress'",
        "timestamp": "2026-10-14 11:20:00",
        "ip_address": "192.168.1.42"
    },
    {
        "log_id": 103,
        "user_name": "Dr. Arvind Mehta",
        "user_role": "Admin",
        "action": "Updated Category",
        "target_id": "CAT-001",
        "details": "Adjusted default SLA to 24 hours for IT & Network",
        "timestamp": "2026-10-13 15:10:00",
        "ip_address": "192.168.1.15"
    },
    {
        "log_id": 104,
        "user_name": "Rajesh Kumar",
        "user_role": "Staff",
        "action": "Resolved Complaint",
        "target_id": "OCMS-2026-0003",
        "details": "Replaced bulb module. Verified operations.",
        "timestamp": "2026-10-11 16:30:00",
        "ip_address": "192.168.1.88"
    },
    {
        "log_id": 105,
        "user_name": "Priya Nair",
        "user_role": "Staff",
        "action": "Rejected Complaint",
        "target_id": "OCMS-2026-0006",
        "details": "Reason: Out of scope (personal MacBook servicing)",
        "timestamp": "2026-10-09 12:15:00",
        "ip_address": "192.168.1.42"
    }
]

# Helper query functions

def get_complaint_by_no(complaint_no):
    """Retrieve single complaint dictionary by complaint number"""
    for comp in MOCK_COMPLAINTS:
        if comp["complaint_no"].lower() == complaint_no.lower():
            return comp
    return None

def get_user_complaints(user_id=1, status_filter=None, priority_filter=None, search_term=None):
    """Filter complaints for a specific user/citizen"""
    results = [c for c in MOCK_COMPLAINTS if c["user_id"] == user_id]
    if status_filter and status_filter != 'all':
        results = [c for c in results if c["status"].lower() == status_filter.lower()]
    if priority_filter and priority_filter != 'all':
        results = [c for c in results if c["priority"].lower() == priority_filter.lower()]
    if search_term:
        term = search_term.lower()
        results = [c for c in results if term in c["subject"].lower() or term in c["complaint_no"].lower() or term in c["location"].lower()]
    return results

def get_staff_complaints(staff_id=2, status_filter=None, search_term=None):
    """Filter complaints assigned to a staff technician"""
    results = [c for c in MOCK_COMPLAINTS if c["assigned_to"] == staff_id]
    if status_filter and status_filter != 'all':
        if status_filter == 'Overdue':
            results = [c for c in results if c["is_overdue"]]
        else:
            results = [c for c in results if c["status"].lower() == status_filter.lower()]
    if search_term:
        term = search_term.lower()
        results = [c for c in results if term in c["subject"].lower() or term in c["complaint_no"].lower() or term in c["location"].lower()]
    return results

def get_all_complaints(status_filter=None, category_filter=None, priority_filter=None, staff_filter=None, search_term=None):
    """Filter all complaints for Admin view"""
    results = list(MOCK_COMPLAINTS)
    if status_filter and status_filter != 'all':
        if status_filter == 'Overdue':
            results = [c for c in results if c["is_overdue"]]
        else:
            results = [c for c in results if c["status"].lower() == status_filter.lower()]
    if category_filter and category_filter != 'all':
        results = [c for c in results if str(c["category_id"]) == str(category_filter)]
    if priority_filter and priority_filter != 'all':
        results = [c for c in results if c["priority"].lower() == priority_filter.lower()]
    if staff_filter and staff_filter != 'all':
        results = [c for c in results if str(c["assigned_to"]) == str(staff_filter)]
    if search_term:
        term = search_term.lower()
        results = [c for c in results if term in c["subject"].lower() or term in c["complaint_no"].lower() or term in c["user_name"].lower()]
    return results

def get_user_dashboard_stats(user_id=1):
    """Compute aggregate counts for Citizen dashboard"""
    user_comps = [c for c in MOCK_COMPLAINTS if c["user_id"] == user_id]
    total = len(user_comps)
    pending = len([c for c in user_comps if c["status"] in ["Submitted", "Assigned"]])
    in_progress = len([c for c in user_comps if c["status"] in ["In Progress", "Reopened"]])
    resolved = len([c for c in user_comps if c["status"] in ["Resolved", "Closed"]])
    rejected = len([c for c in user_comps if c["status"] == "Rejected"])
    return {
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "resolved": resolved,
        "rejected": rejected,
        "recent_complaints": sorted(user_comps, key=lambda x: x["created_at"], reverse=True)[:5]
    }

def get_staff_dashboard_stats(staff_id=2):
    """Compute aggregate counts for Staff officer dashboard"""
    staff_comps = [c for c in MOCK_COMPLAINTS if c["assigned_to"] == staff_id]
    total_assigned = len(staff_comps)
    pending_action = len([c for c in staff_comps if c["status"] in ["Assigned", "In Progress", "Reopened"]])
    resolved = len([c for c in staff_comps if c["status"] in ["Resolved", "Closed"]])
    overdue = len([c for c in staff_comps if c["is_overdue"]])
    return {
        "total_assigned": total_assigned,
        "pending_action": pending_action,
        "resolved": resolved,
        "overdue": overdue,
        "assigned_complaints": sorted(staff_comps, key=lambda x: x["created_at"], reverse=True)
    }

def get_admin_dashboard_stats():
    """Compute executive aggregate counts for Admin dashboard (FR-7.1)"""
    total = len(MOCK_COMPLAINTS)
    submitted = len([c for c in MOCK_COMPLAINTS if c["status"] == "Submitted"])
    assigned = len([c for c in MOCK_COMPLAINTS if c["status"] == "Assigned"])
    in_progress = len([c for c in MOCK_COMPLAINTS if c["status"] in ["In Progress", "Reopened"]])
    resolved = len([c for c in MOCK_COMPLAINTS if c["status"] in ["Resolved", "Closed"]])
    rejected = len([c for c in MOCK_COMPLAINTS if c["status"] == "Rejected"])
    overdue = len([c for c in MOCK_COMPLAINTS if c["is_overdue"]])
    
    # SLA metrics (FR-7.5)
    sla_compliance_pct = 88.5
    avg_resolution_hours = 28.4
    
    return {
        "total": total,
        "submitted": submitted,
        "assigned": assigned,
        "in_progress": in_progress,
        "resolved": resolved,
        "rejected": rejected,
        "overdue": overdue,
        "sla_compliance_pct": sla_compliance_pct,
        "avg_resolution_hours": avg_resolution_hours,
        "recent_complaints": sorted(MOCK_COMPLAINTS, key=lambda x: x["created_at"], reverse=True)[:6]
    }

def get_notifications_for_role(role="user"):
    """Retrieve notification items filtered by current session role"""
    return [n for n in MOCK_NOTIFICATIONS if n["role"] == role or n["role"] == "all"]

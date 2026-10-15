"""
Online Complaint Management System (OCMS) - Database Seeder
Seeds default departments, categories, users, complaints, status histories,
feedback ratings, and notifications conforming to SRS IEEE Std 830-1998.

Default Credentials:
- Admin:  admin@example.com  / Admin@123
- Staff:  staff@example.com  / Staff@123
- User 1: user@example.com   / User@123
- User 2: user2@example.com  / User@123
"""

import os
from datetime import datetime, timedelta
from app import create_app
from app.models import (
    db, User, Department, Category, Complaint,
    ComplaintUpdate, Feedback, Notification, AuditLog
)

def seed_database():
    app = create_app('default')
    with app.app_context():
        print(" [1/6] Creating database tables...")
        db.create_all()

        print(" [2/6] Seeding departments...")
        depts_data = [
            "IT & Networking",
            "Electrical Maintenance",
            "Civil & Infrastructure",
            "Sanitation & Housekeeping"
        ]
        dept_map = {}
        for name in depts_data:
            dept = Department.query.filter_by(name=name).first()
            if not dept:
                dept = Department(name=name)
                db.session.add(dept)
                db.session.flush()
            dept_map[name] = dept

        print(" [3/6] Seeding standard categories...")
        categories_data = [
            ("Hostel & Accommodation", "Plumbing, electrical fixtures, furniture, room maintenance in campus hostels.", 24, "bi-building"),
            ("IT & Network Infrastructure", "Campus Wi-Fi, Ethernet ports, lab systems, printer access.", 12, "bi-wifi"),
            ("Classrooms & Labs", "Projectors, audio systems, air conditioning, smart boards, lab equipment.", 18, "bi-mortarboard"),
            ("Electrical & Power", "Power cuts, switchboards, wiring faults, corridor lighting, UPS issues.", 8, "bi-lightning-charge"),
            ("Sanitation & Water", "Restroom cleanliness, water cooler filters, tap leaks, hygiene.", 12, "bi-droplet"),
            ("Security & General", "Campus lighting, lost-and-found items, noise pollution, perimeter safety.", 24, "bi-shield-check")
        ]
        cat_map = {}
        for name, desc, sla, icon in categories_data:
            cat = Category.query.filter_by(name=name).first()
            if not cat:
                cat = Category(name=name, description=desc, sla_hours=sla, icon=icon, is_active=True)
                db.session.add(cat)
                db.session.flush()
            else:
                cat.sla_hours = sla
                cat.icon = icon
            cat_map[name] = cat

        print(" [4/6] Seeding users with secure password hashing...")
        users_data = [
            {
                "email": "admin@example.com",
                "password": "Admin@123",
                "name": "Dr. Arvind Mehta",
                "role": "admin",
                "phone": "+91 98111 22334",
                "department": "Campus Administration"
            },
            {
                "email": "staff@example.com",
                "password": "Staff@123",
                "name": "Priya Nair",
                "role": "staff",
                "phone": "+91 98222 33445",
                "department": "IT & Networking"
            },
            {
                "email": "user@example.com",
                "password": "User@123",
                "name": "Rahul Sharma",
                "role": "user",
                "phone": "+91 98765 43210",
                "department": "Computer Science (Student)"
            },
            {
                "email": "user2@example.com",
                "password": "User@123",
                "name": "Ananya Iyer",
                "role": "user",
                "phone": "+91 98333 44556",
                "department": "Electronics Engineering (Student)"
            }
        ]

        user_map = {}
        for u in users_data:
            existing = User.query.filter_by(email=u["email"]).first()
            if not existing:
                new_u = User(
                    email=u["email"],
                    name=u["name"],
                    role=u["role"],
                    phone=u["phone"],
                    department=u["department"],
                    is_active=True
                )
                new_u.set_password(u["password"])
                db.session.add(new_u)
                db.session.flush()
                user_map[u["email"]] = new_u
            else:
                existing.name = u["name"]
                existing.role = u["role"]
                existing.phone = u["phone"]
                existing.department = u["department"]
                existing.set_password(u["password"])
                existing.is_active = True
                user_map[u["email"]] = existing

        admin_user = user_map["admin@example.com"]
        staff_user = user_map["staff@example.com"]
        user_1 = user_map["user@example.com"]
        user_2 = user_map["user2@example.com"]

        print(" [5/6] Seeding 14 realistic sample complaints with lifecycle history...")
        now = datetime.utcnow()

        sample_cases = [
            {
                "no": "OCMS-2026-0001",
                "user": user_1,
                "cat": cat_map["Hostel & Accommodation"],
                "subject": "Ceiling fan regulator sparking in Room 204",
                "desc": "The ceiling fan regulator sparks violently when rotated past speed 2. Possibility of electrical short circuit.",
                "loc": "Hostel Block B, 2nd Floor, Room 204",
                "priority": "Urgent",
                "status": "Resolved",
                "assigned": staff_user,
                "days_ago": 6,
                "resolved_days_ago": 5,
                "history": [
                    ("Submitted", "Complaint registered via online student portal.", user_1, 6),
                    ("Assigned", "Triaged by Administration. Priority set to Urgent due to safety risk.", admin_user, 5.8),
                    ("In Progress", "Technician dispatched with replacement modular regulator unit.", staff_user, 5.5),
                    ("Resolved", "Sparking regulator replaced with brand new Havells 100W step regulator. Tested safely.", staff_user, 5)
                ],
                "feedback": (5, "Very fast turnaround! Technician arrived within 3 hours and replaced the faulty switch safely.")
            },
            {
                "no": "OCMS-2026-0002",
                "user": user_1,
                "cat": cat_map["IT & Network Infrastructure"],
                "subject": "Access Point AP-04 dropping connections in CS Lab 3",
                "desc": "Students working on cloud computing practicals get disconnected every 10 minutes. DHCP error.",
                "loc": "Academic Block A, CS Lab 3, 3rd Floor",
                "priority": "High",
                "status": "In Progress",
                "assigned": staff_user,
                "days_ago": 3,
                "resolved_days_ago": None,
                "history": [
                    ("Submitted", "Complaint submitted by student representative.", user_1, 3),
                    ("Assigned", "Assigned to Senior IT Technician Priya Nair.", admin_user, 2.9),
                    ("In Progress", "Firmware upgrade initiated on Cisco AP-04; monitoring packet loss logs.", staff_user, 1.5)
                ],
                "feedback": None
            },
            {
                "no": "OCMS-2026-0003",
                "user": user_2,
                "cat": cat_map["Classrooms & Labs"],
                "subject": "Overhead HDMI Projector lamp dim and flickering",
                "desc": "Lecture Hall 102 projector lamp is flickering during lectures. Slides are barely visible in daylight.",
                "loc": "Lecture Hall Complex, Room LH-102",
                "priority": "Medium",
                "status": "Assigned",
                "assigned": staff_user,
                "days_ago": 2,
                "resolved_days_ago": None,
                "history": [
                    ("Submitted", "Filed by class coordinator.", user_2, 2),
                    ("Assigned", "Allocated to Audio-Visual support technician for lamp bulb replacement.", admin_user, 1.8)
                ],
                "feedback": None
            },
            {
                "no": "OCMS-2026-0004",
                "user": user_1,
                "cat": cat_map["Sanitation & Water"],
                "subject": "Water cooler on 1st floor dispensing warm, cloudy water",
                "desc": "The UV filter indicator light is red and the cooling compressor is not engaging.",
                "loc": "Library Building, 1st Floor Corridor",
                "priority": "Medium",
                "status": "Submitted",
                "assigned": None,
                "days_ago": 1,
                "resolved_days_ago": None,
                "history": [
                    ("Submitted", "Complaint received online. Awaiting administrative triage.", user_1, 1)
                ],
                "feedback": None
            },
            {
                "no": "OCMS-2026-0005",
                "user": user_2,
                "cat": cat_map["Electrical & Power"],
                "subject": "Corridor security floodlights inactive after 8 PM",
                "desc": "Path from Girls Hostel to Library is completely dark after sunset. High security concern.",
                "loc": "Pathway between Hostel Block C and Central Library",
                "priority": "Urgent",
                "status": "In Progress",
                "assigned": staff_user,
                "days_ago": 2,
                "resolved_days_ago": None,
                "history": [
                    ("Submitted", "Complaint filed for student safety.", user_2, 2),
                    ("Assigned", "Marked Urgent. Assigned to electrical department.", admin_user, 1.9),
                    ("In Progress", "Timer relay switch on pole 14 failed; procurement of industrial timer in progress.", staff_user, 0.8)
                ],
                "feedback": None
            },
            {
                "no": "OCMS-2026-0006",
                "user": user_1,
                "cat": cat_map["Security & General"],
                "subject": "Bicycle parking rack damaged near sports complex",
                "desc": "The steel stand is unbolted from the ground and tilts dangerously against locked bikes.",
                "loc": "Sports Complex South Gate",
                "priority": "Low",
                "status": "Rejected",
                "assigned": staff_user,
                "days_ago": 5,
                "resolved_days_ago": None,
                "history": [
                    ("Submitted", "Complaint filed regarding parking stand.", user_1, 5),
                    ("Assigned", "Assigned for campus inspection.", admin_user, 4.8),
                    ("Rejected", "Inspected on site: Area is currently scheduled for major paving renovation under Master Plan 2026. Stand will be relocated permanently next week.", staff_user, 4)
                ],
                "feedback": None
            },
            {
                "no": "OCMS-2026-0007",
                "user": user_2,
                "cat": cat_map["Hostel & Accommodation"],
                "subject": "Washbasin tap leaking continuously in 3rd Floor washroom",
                "desc": "Tap valve worn out, water is leaking continuously wasting water.",
                "loc": "Hostel Block C, Wing 1, 3rd Floor Washroom",
                "priority": "Medium",
                "status": "Resolved",
                "assigned": staff_user,
                "days_ago": 8,
                "resolved_days_ago": 6,
                "history": [
                    ("Submitted", "Complaint submitted.", user_2, 8),
                    ("Assigned", "Assigned to civil plumbing squad.", admin_user, 7.8),
                    ("In Progress", "Plumber on site repairing washer valve.", staff_user, 6.5),
                    ("Resolved", "Brass ceramic disc valve replaced. No leaks detected.", staff_user, 6)
                ],
                "feedback": (4, "Fixed properly, though took a day longer than expected.")
            },
            {
                "no": "OCMS-2026-0008",
                "user": user_1,
                "cat": cat_map["Classrooms & Labs"],
                "subject": "AC unit in Server Room leaking condensation on rack",
                "desc": "Drain pipe blocked, water pooling near networking switches. Requires immediate attention.",
                "loc": "Data Center, Ground Floor, Admin Block",
                "priority": "Urgent",
                "status": "Closed",
                "assigned": staff_user,
                "days_ago": 12,
                "resolved_days_ago": 11,
                "history": [
                    ("Submitted", "Critical alert filed by lab technician.", user_1, 12),
                    ("Assigned", "Immediate triage. Assigned to HVAC specialist.", admin_user, 11.9),
                    ("In Progress", "Drain line cleared and insulation repaired.", staff_user, 11.5),
                    ("Resolved", "AC drip tray unclogged, test run 4 hours verified dry.", staff_user, 11),
                    ("Closed", "Ticket confirmed and closed after 48h observation period.", admin_user, 9)
                ],
                "feedback": (5, "Outstanding rapid emergency response prevented equipment damage.")
            },
            {
                "no": "OCMS-2026-0009",
                "user": user_2,
                "cat": cat_map["IT & Network Infrastructure"],
                "subject": "Lab 105 Printer paper jam mechanism broken",
                "desc": "Network printer HP LaserJet 404 tray 2 roller is jammed with torn paper.",
                "loc": "MCA Computer Lab 105",
                "priority": "Low",
                "status": "Submitted",
                "assigned": None,
                "days_ago": 0.5,
                "resolved_days_ago": None,
                "history": [
                    ("Submitted", "Filed by MCA student.", user_2, 0.5)
                ],
                "feedback": None
            },
            {
                "no": "OCMS-2026-00010",
                "user": user_1,
                "cat": cat_map["Sanitation & Water"],
                "subject": "Cafeteria handwash soap dispensers empty",
                "desc": "All three liquid soap dispensers in the main student dining hall are empty.",
                "loc": "Main Campus Cafeteria, Dining Hall B",
                "priority": "Medium",
                "status": "Resolved",
                "assigned": staff_user,
                "days_ago": 4,
                "resolved_days_ago": 3,
                "history": [
                    ("Submitted", "Complaint registered for hygiene compliance.", user_1, 4),
                    ("Assigned", "Forwarded to housekeeping contractor supervisor.", admin_user, 3.8),
                    ("Resolved", "All soap dispensers refilled and backup bottles stocked in cleaning closet.", staff_user, 3)
                ],
                "feedback": (5, "Prompt refill, thank you.")
            },
            {
                "no": "OCMS-2026-00011",
                "user": user_2,
                "cat": cat_map["Electrical & Power"],
                "subject": "Chemistry lab fume hood exhaust motor making loud grinding noise",
                "desc": "Exhaust fan bearing seems worn out; fumes not evacuating effectively.",
                "loc": "Science Block, Chemistry Lab 201",
                "priority": "High",
                "status": "Assigned",
                "assigned": staff_user,
                "days_ago": 1.2,
                "resolved_days_ago": None,
                "history": [
                    ("Submitted", "Reported by Lab Assistant.", user_2, 1.2),
                    ("Assigned", "Assigned to mechanical maintenance team.", admin_user, 1.0)
                ],
                "feedback": None
            },
            {
                "no": "OCMS-2026-00012",
                "user": user_1,
                "cat": cat_map["Security & General"],
                "subject": "Fire extinguisher inspection tag expired in Seminar Hall",
                "desc": "CO2 extinguisher last inspected in 2024. Needs pressure testing and certified refilling.",
                "loc": "Management Block, Main Seminar Hall",
                "priority": "High",
                "status": "In Progress",
                "assigned": staff_user,
                "days_ago": 2.5,
                "resolved_days_ago": None,
                "history": [
                    ("Submitted", "Reported during student council safety audit.", user_1, 2.5),
                    ("Assigned", "Assigned to Safety Officer.", admin_user, 2.2),
                    ("In Progress", "Fire safety vendor contacted for campus-wide extinguisher audit.", staff_user, 1.1)
                ],
                "feedback": None
            },
            {
                "no": "OCMS-2026-00013",
                "user": user_2,
                "cat": cat_map["Hostel & Accommodation"],
                "subject": "Door latch stuck from outside in Room 112",
                "desc": "The brass cylinder latch is jammed and difficult to unlock with room key.",
                "loc": "Hostel Block A, Ground Floor, Room 112",
                "priority": "Low",
                "status": "Submitted",
                "assigned": None,
                "days_ago": 0.8,
                "resolved_days_ago": None,
                "history": [
                    ("Submitted", "Filed by student occupant.", user_2, 0.8)
                ],
                "feedback": None
            },
            {
                "no": "OCMS-2026-00014",
                "user": user_1,
                "cat": cat_map["Classrooms & Labs"],
                "subject": "Audio microphone cordless system battery died during keynote",
                "desc": "Rechargeable dock does not charge the wireless handheld mic unit.",
                "loc": "Auditorium Control Room",
                "priority": "Low",
                "status": "Resolved",
                "assigned": staff_user,
                "days_ago": 5,
                "resolved_days_ago": 4,
                "history": [
                    ("Submitted", "Filed following technical symposium.", user_1, 5),
                    ("Assigned", "Assigned to AV tech.", admin_user, 4.8),
                    ("Resolved", "Charging dock power adapter replaced and fresh NiMH cells installed.", staff_user, 4)
                ],
                "feedback": (5, "Good service, testing went smooth.")
            }
        ]

        for case in sample_cases:
            existing_comp = Complaint.query.filter_by(tracking_number=case["no"]).first()
            created_dt = now - timedelta(days=case["days_ago"])
            due_dt = created_dt + timedelta(hours=case["cat"].sla_hours)
            resolved_dt = (now - timedelta(days=case["resolved_days_ago"])) if case["resolved_days_ago"] else None

            if not existing_comp:
                comp = Complaint(
                    tracking_number=case["no"],
                    user_id=case["user"].id,
                    category_id=case["cat"].id,
                    assigned_to=case["assigned"].id if case["assigned"] else None,
                    title=case["subject"],
                    description=case["desc"],
                    location=case["loc"],
                    priority=case["priority"],
                    status=case["status"],
                    created_at=created_dt,
                    due_at=due_dt,
                    resolved_at=resolved_dt,
                    rejection_reason=case["history"][-1][1] if case["status"] == "Rejected" else None
                )
                db.session.add(comp)
                db.session.flush()

                # Add updates / comments history
                for st, msg, author, days_back in case["history"]:
                    up_dt = now - timedelta(days=days_back)
                    update = ComplaintUpdate(
                        complaint_id=comp.id,
                        updated_by=author.id,
                        old_status=None,
                        new_status=st,
                        remark=msg,
                        created_at=up_dt
                    )
                    db.session.add(update)

                # Add feedback if applicable
                if case["feedback"]:
                    rating_val, comment_text = case["feedback"]
                    fb = Feedback(
                        complaint_id=comp.id,
                        user_id=case["user"].id,
                        rating=rating_val,
                        comment=comment_text,
                        created_at=resolved_dt + timedelta(minutes=30) if resolved_dt else now
                    )
                    db.session.add(fb)

        print(" [6/6] Seeding sample notifications and security audit logs...")
        sample_notifs = [
            (user_1.id, "OCMS-2026-0001", "Grievance Resolved: Your complaint regarding sparking ceiling fan regulator was fixed."),
            (user_1.id, "OCMS-2026-0002", "Technician Dispatched: Senior IT Technician Priya Nair started work on your complaint."),
            (user_2.id, "OCMS-2026-0003", "Staff Assigned: Dr. Arvind Mehta assigned your complaint to technician Priya Nair."),
            (user_1.id, "OCMS-2026-0006", "Notice of Rejection: Your complaint was reviewed and marked as scheduled under Campus Master Plan.")
        ]
        for uid, cno, msg in sample_notifs:
            comp_obj = Complaint.query.filter_by(tracking_number=cno).first()
            notif = Notification(
                user_id=uid,
                complaint_id=comp_obj.id if comp_obj else None,
                message=msg,
                is_read=False
            )
            db.session.add(notif)

        # Audit logs
        sample_audits = [
            ("Created category", "IT & Network Infrastructure", "System setup"),
            ("Assigned Complaint", "OCMS-2026-0001", "Allocated to Priya Nair"),
            ("Updated status", "OCMS-2026-0001", "Status changed to Resolved"),
            ("Assigned Complaint", "OCMS-2026-0002", "Allocated to Priya Nair")
        ]
        for action, target, details in sample_audits:
            audit = AuditLog(
                user_id=admin_user.id,
                action=action,
                target_id=target,
                details=details,
                ip_address="127.0.0.1"
            )
            db.session.add(audit)

        db.session.commit()
        print("\n [SUCCESS] Database seeded successfully!")
        print(" SQLite database initialized at:", app.config['SQLALCHEMY_DATABASE_URI'])
        print("\n Demo Credentials:")
        print("  - Admin: admin@example.com  | Admin@123")
        print("  - Staff: staff@example.com  | Staff@123")
        print("  - User1: user@example.com   | User@123")
        print("  - User2: user2@example.com  | User@123")

if __name__ == '__main__':
    seed_database()

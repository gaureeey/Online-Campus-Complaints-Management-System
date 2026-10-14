# Online Complaint Management System (OCMS)
**Final Year BCA Capstone Project &bull; Python Web Application**

Conforming strictly to the Software Requirements Specification ([docs/SRS.pdf](file:///c:/Users/Gauri%20Rajesh/Desktop/OCMS/docs/SRS.pdf)) based on **IEEE Std 830-1998**.

---

## 📌 Project Overview

The **Online Complaint Management System (OCMS)** replaces paper-based complaint registers, informal phone calls, and email threads with a centralized, automated web portal. It provides end-to-end transparency for filing, categorizing, prioritizing, assigning, resolving, and evaluating campus facility grievances across students, technicians, and administrators.

This repository contains the **complete, production-grade frontend prototype**, rendered server-side using **Python Flask + Jinja2 templates**, designed specifically so that SQLAlchemy ORM and SQLite/MySQL backends can be plugged directly into [app.py](file:///c:/Users/Gauri%20Rajesh/Desktop/OCMS/app.py) without altering any HTML or CSS layouts.

---

## 🛠️ Technology Stack

- **Back-end Server**: Python 3.10+ with [Flask 3.1.3](https://palletsprojects.com/p/flask/)
- **Templating Engine**: Jinja2 (Server-Rendered HTML5)
- **CSS Framework**: Bootstrap 5.3.3 (CDN) with Calm Modern Theme ([static/css/theme.css](file:///c:/Users/Gauri%20Rajesh/Desktop/OCMS/static/css/theme.css))
- **Iconography**: Bootstrap Icons 1.11.3 (CDN)
- **Data Visualizations**: Chart.js 4.4.3 (CDN)
- **Client Scripting**: Vanilla JavaScript ([static/js/main.js](file:///c:/Users/Gauri%20Rajesh/Desktop/OCMS/static/js/main.js)) &ndash; No Node.js / npm build step required

---

## 🚀 Quick Start Guide

### Step 1: Install Dependencies
Open PowerShell or your terminal in this directory and execute:
```powershell
pip install -r requirements.txt
```

### Step 2: Run the Application
Launch the Flask development server:
```powershell
python app.py
```

### Step 3: Open in Browser
Open your browser and navigate to:
```
http://127.0.0.1:5050
```
*(If port 5000 is free on your machine, it will use 5000; otherwise, it automatically uses 5050).*

---

## 🎭 Viva Evaluation Demo: Instant Role Switching

To make your **BCA final project presentation and viva evaluation seamless**, an interactive **Demo Role Switcher Bar** is pinned to the top of every screen:

| Role Persona | Mock User | Target Dashboard | 1-Click Route |
|:---|:---|:---|:---|
| **Public Visitor (Guest)** | Unauthenticated | Landing Page & Public Tracker | `/switch-role/guest` |
| **User (Student / Resident)** | Rahul Sharma | Citizen Grievance Portal | `/switch-role/user` |
| **Staff (Technician)** | Priya Nair | Field Officer Resolution Desk | `/switch-role/staff` |
| **Administrator** | Dr. Arvind Mehta | Executive Analytics & Governance | `/switch-role/admin` |

Alternatively, you can test traditional login at `/login` where one-click demo credentials are also provided.

---

## 📑 Complete Routes & Pages Directory

All 21 application pages are catalogued in detail with screenshot guidelines in [PAGES.md](file:///c:/Users/Gauri%20Rajesh/Desktop/OCMS/PAGES.md):

### 1. Public Pages
- `/` : Landing Page (Hero, 4-step workflow, categories, live statistics, quick tracker widget)
- `/login` : Authentication form with 30-min session security notice (NFR-1) and lockout alert (FR-1.8)
- `/register` : Complainant signup with real-time password strength meter (FR-1.1, FR-1.2)
- `/forgot-password` : Cryptographic 15-minute time-limited password recovery request (FR-1.6)
- `/track` : Public Grievance Tracker by Complaint Number (e.g. `OCMS-2026-0001`)

### 2. Complainant / Citizen Pages
- `/dashboard` : Citizen dashboard with total, pending, in-progress, and resolved metrics
- `/complaint/new` : Grievance submission form featuring:
  - Drag-and-drop file upload with preview (max 3 files, 5MB each, JPG/PNG/PDF &ndash; FR-2.3)
  - Real-time keyword auto-categorisation assistant (FR-8.1)
  - Duplicate complaint detection alert (FR-8.2)
  - Anonymous submission toggle (FR-2.11)
- `/complaints` : Searchable and filterable table of filed complaints with pagination (NFR-5)
- `/complaint/<complaint_no>` : Complaint details view with:
  - Resolution timeline & conversational reply box (FR-2.8)
  - Attached evidence viewer (FR-2.3)
  - 1-to-5 star interactive rating and feedback form upon resolution (FR-6.1)
  - Withdraw modal for unassigned complaints (FR-2.9)
  - Reopen issue modal within 7 days of resolution (FR-2.10)
- `/notifications` : In-app notification feed with unread counters (FR-5.3)
- `/profile` : User profile management and password change form (FR-1.5)

### 3. Staff / Field Officer Pages
- `/staff/dashboard` : Technician overview with assigned workload and SLA overdue alerts (FR-4.4)
- `/staff/complaints` : Filterable queue of complaints assigned only to the logged-in staff member (FR-4.1)
- `/staff/complaint/<complaint_no>` : Inspection workspace to:
  - Update progress status to *In Progress* or *Resolved* (FR-4.2)
  - Mark complaints *Rejected* with a mandatory written justification (FR-4.3)
  - Add resolution notes stored in the complaint timeline

### 4. Administrator Pages
- `/admin/dashboard` : Executive console with SLA compliance index (88.5%), resolution velocity, and Chart.js graphs (FR-7.1, 7.4, 7.5)
- `/admin/complaints` : Central management ledger with multi-criteria filters, staff assignment modal (FR-3.3), priority/SLA adjuster (FR-3.7), and duplicate merger (FR-3.9)
- `/admin/complaint/<complaint_no>` : Administrative master triage view revealing complainant identity (FR-2.11) and official response publishing (FR-3.6)
- `/admin/users` : User & staff account provisioning, role modifiers, and deactivation toggles (FR-3.5)
- `/admin/categories` : Category catalogue with configurable SLA target hours (FR-3.4)
- `/admin/reports` : Date-range filtered audit report ledger with **Export to CSV** and **Print/PDF** layout (FR-7.2, 7.3)
- `/admin/audit-log` : Tamper-evident administrative action log (FR-3.10)

---

## 🔌 Plugging in the Backend (Next Phase)

Each route in [app.py](file:///c:/Users/Gauri%20Rajesh/Desktop/OCMS/app.py) contains detailed `TODO Backend` comments indicating exactly how to replace the mock data functions with SQLAlchemy ORM models:

```python
# Example from app.py:
# TODO Backend:
# 1. user = User.query.filter_by(email=email).first()
# 2. Check password hash: bcrypt.check_password_hash(user.password_hash, password)
# 3. Handle session and redirect to role-specific dashboard
```

The database schema defined in the SRS (Section 7: `users`, `categories`, `complaints`, `attachments`, `comments`, `feedback`, `notifications`, `audit_log`) matches the dictionary structure in [mock_data.py](file:///c:/Users/Gauri%20Rajesh/Desktop/OCMS/mock_data.py) 1-to-1.

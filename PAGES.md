# Online Complaint Management System (OCMS)
## Chapter 6: Implementation & User Interface Directory (Simplified & Polished)

This document provides the formal numbered catalogue of all graphical user interfaces implemented in the **Online Complaint Management System (OCMS)**, aligned with the Software Requirements Specification (IEEE Std 830-1998 format).

Use this numbered reference to structure the **Chapter 6: System Implementation & Testing** screenshots and descriptions in your BCA project report.

---

### Part 1: Public & Visitor Interfaces

| Page # | Route | Page Title | Actor / Role | Description & Screenshot Focus |
|:---:|:---|:---|:---|:---|
| **01** | `/` | **Portal Landing Page** | Public Visitor | Clean hero banner with one-line subtitle, primary "Submit a Complaint" and "Track a Complaint" buttons, 3-step "How it works" strip, and common categories grid. |
| **02** | `/login` | **Authentication & Sign-in** | All Actors | Clean login form with email and password fields, and one-click Fast-Track Demo Logins for Citizen, Staff, and Admin evaluation. |
| **03** | `/register` | **Citizen Account Registration** | Visitor | Streamlined 4-field registration form (Full Name, Email, Mobile Phone, Password) with helpful inline guidance. |
| **04** | `/forgot-password` | **Password Help** | Visitor | Clean single-field password recovery screen dispatching time-limited reset links. |
| **05** | `/track` | **Track a Complaint** | Public / All | Public search by Tracking Number (e.g. `OCMS-2026-0001`), displaying 4-step progress tracker (`Submitted` &rarr; `Under Review` &rarr; `In Progress` &rarr; `Resolved`), status badges, and latest technician notes. |

---

### Part 2: Complainant / Citizen Interfaces

| Page # | Route | Page Title | Actor / Role | Description & Screenshot Focus |
|:---:|:---|:---|:---|:---|
| **06** | `/dashboard` | **Citizen Overview Dashboard** | Complainant | 3 clean summary cards (Total Filed, In Progress, Resolved), 3-step "How it works" strip, prominent "Submit a Complaint" button, and 5-column recent complaints table. |
| **07** | `/complaint/new` | **Submit Complaint (Simplified)** | Complainant | Cut to essential fields: Category, Title, Description, optional Location, optional Photo attachment. Plain language labels, kind helper text, and submit loading state. |
| **08** | `/complaint/success/<id>` | **Submission Success Screen** | Complainant | Prominent green checkmark confirmation displaying large Tracking Number, instant Copy to Clipboard button, "Track this Complaint" button, and next-step breakdown. |
| **09** | `/complaints` | **My Complaints** | Complainant | 5-column table (Tracking Number, Title, Category, Status, Action), search bar, clean status filter, friendly empty state, and simple pagination. |
| **10** | `/complaint/<complaint_no>` | **Complaint Details & Timeline** | Complainant | Back button, large Tracking Number with Copy button, 4-step visual tracker (`Submitted` &rarr; `Under Review` &rarr; `In Progress` &rarr; `Resolved`), remarks thread, reply box, and 1-5 star feedback rating widget upon resolution. |
| **11** | `/notifications` | **Notifications Center** | Complainant / All | Clean notification feed showing status updates and direct links to complaints. |
| **12** | `/profile` | **Profile & Security** | Complainant / All | Personal contact details form and password change screen. |

---

### Part 3: Field Staff / Technician Interfaces

| Page # | Route | Page Title | Actor / Role | Description & Screenshot Focus |
|:---:|:---|:---|:---|:---|
| **13** | `/staff/dashboard` | **Technician Overview** | Staff Officer | 3 workload metric cards (Assigned Tasks, In Progress, Resolved) and active task queue. |
| **14** | `/staff/complaints` | **My Assigned Tasks** | Staff Officer | Clean 4-column table of tasks allocated to the officer with fast status filter. |
| **15** | `/staff/complaint/<complaint_no>` | **Task Resolution Workspace** | Staff Officer | Progress status update desk (`In Progress`, `Resolved`, `Rejected`), resolution notes entry, and timeline remarks. |

---

### Part 4: System Administration & Governance Interfaces

| Page # | Route | Page Title | Actor / Role | Description & Screenshot Focus |
|:---:|:---|:---|:---|:---|
| **16** | `/admin/dashboard` | **Admin Overview** | Administrator | 4 clean cards (New, In Progress, Resolved, Needs Attention), single Monthly Resolution Trend chart (Chart.js), and recent complaints list. |
| **17** | `/admin/complaints` | **All Complaints** | Administrator | 5-column management table with search and status filter, quick Assign Staff modal, and update status controls. |
| **18** | `/admin/complaint/<complaint_no>` | **Admin Review & Triage** | Administrator | Detailed ticket review, complainant details, staff assignment dropdown, and official administrative remark publisher. |
| **19** | `/admin/users` | **Users & Staff** | Administrator | User directory table with Add Account modal and activate/deactivate toggles. |
| **20** | `/admin/categories` | **Complaint Categories** | Administrator | Service category cards with resolution target SLA hours and Add Category modal. |
| **21** | `/admin/reports` | **Reports & Data Export** | Administrator | Filterable complaint ledger with summary counts and one-click "Download CSV" exporter. |
| **22** | `/admin/audit-log` | **Security Audit Trail** | Administrator | Administrative activity log recording Actor, Action, Target Record, Timestamps, and IP addresses. |

---

### Part 5: Demo Utilities

| Page # | Route | Purpose | Description |
|:---:|:---|:---|:---|
| **23** | `/switch-role/<role>` | **Viva Demo Role Switcher** | Instantaneous persona switcher (`guest`, `user`, `staff`, `admin`) pinned to the top of every screen to demonstrate role-based access control. |

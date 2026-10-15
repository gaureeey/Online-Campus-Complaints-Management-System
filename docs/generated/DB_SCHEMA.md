# Database Schema Documentation

**System**: Online Complaint Management System (OCMS)  
**Standard**: IEEE Std 830-1998 Conforming  
**Engine**: SQLite 3 (`instance/complaints.db`)  
**ORM**: Flask-SQLAlchemy (SQLAlchemy 2.x)

---

## 1. Relational Tables Overview

| Table Name | Description | Key Relationships |
|:---|:---|:---|
| `users` | User accounts across Complainant (`user`), Staff (`staff`), and Admin (`admin`) roles | 1:N with `complaints`, `complaint_updates`, `feedback`, `notifications`, `audit_logs` |
| `departments` | Organizational units / sections for campus maintenance | Referenced by staff users |
| `categories` | Service complaint categories with SLA durations (FR-3.4) | 1:N with `complaints` |
| `complaints` | Master ticket records with status, priority, and timeline milestones | Belongs to `user` and `category`; assigned to `staff` |
| `complaint_updates` | Audit trail of status progressions and conversation remarks | Belongs to `complaint`; authored by `user` |
| `feedback` | Post-resolution 1-5 star ratings and reviews (FR-6.1) | 1:1 with `complaint`; submitted by `user` |
| `notifications` | In-app user notifications for ticket milestones (FR-5.3) | Belongs to `user` and optional `complaint` |
| `audit_logs` | Administrative and security action log (FR-3.10) | Recorded by `user` (Admin) |

---

## 2. Table Specifications

### 2.1 Table: `users`
| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique user identifier |
| `email` | VARCHAR(120) | UNIQUE, NOT NULL, INDEX | Campus email address |
| `name` | VARCHAR(120) | NOT NULL | Full name of user |
| `role` | VARCHAR(20) | NOT NULL, DEFAULT 'user' | Access role: `'user'`, `'staff'`, `'admin'` |
| `phone` | VARCHAR(20) | NULLABLE | Mobile phone number |
| `department` | VARCHAR(100) | NULLABLE | Department name for staff / students |
| `password_hash` | VARCHAR(255) | NOT NULL | Werkzeug scrypt salted password hash |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT 1 | Account activation status |
| `failed_attempts` | INTEGER | NOT NULL, DEFAULT 0 | Failed login attempt counter (FR-1.8) |
| `locked_until` | DATETIME | NULLABLE | Lockout expiration timestamp (FR-1.8) |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |

### 2.2 Table: `departments`
| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique department identifier |
| `name` | VARCHAR(100) | UNIQUE, NOT NULL | Department name |

### 2.3 Table: `categories`
| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique category identifier |
| `name` | VARCHAR(100) | UNIQUE, NOT NULL | Category name |
| `description` | TEXT | NULLABLE | Scope and guidelines for complaints |
| `sla_hours` | INTEGER | NOT NULL, DEFAULT 48 | Target resolution SLA in hours (FR-3.4) |
| `icon` | VARCHAR(50) | NOT NULL, DEFAULT 'bi-tag' | Bootstrap Icons CSS class |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT 1 | Active state flag |
| `default_priority` | VARCHAR(20) | NOT NULL, DEFAULT 'Medium' | Default triage priority |

### 2.4 Table: `complaints`
| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Internal primary key |
| `tracking_number` | VARCHAR(30) | UNIQUE, NOT NULL, INDEX | Tracking token (e.g. `OCMS-2026-0001`) |
| `user_id` | INTEGER | NOT NULL, FK `users(id)` | Author complainant identifier |
| `category_id` | INTEGER | NOT NULL, FK `categories(id)` | Linked category identifier |
| `assigned_to` | INTEGER | NULLABLE, FK `users(id)` | Assigned technician staff identifier |
| `title` | VARCHAR(150) | NOT NULL | Short issue summary (subject) |
| `description` | TEXT | NOT NULL | Full issue explanation |
| `location` | VARCHAR(150) | NULLABLE | Campus building / room location |
| `priority` | VARCHAR(20) | NOT NULL, DEFAULT 'Medium' | `'Low'`, `'Medium'`, `'High'`, `'Urgent'` |
| `status` | VARCHAR(30) | NOT NULL, DEFAULT 'Submitted' | Lifecycle progression state |
| `attachment_path` | VARCHAR(255) | NULLABLE | Relative path to uploaded file (FR-2.3) |
| `is_anonymous` | BOOLEAN | NOT NULL, DEFAULT 0 | Anonymous submission flag (FR-2.11) |
| `parent_id` | INTEGER | NULLABLE, FK `complaints(id)` | Parent ticket for merged duplicates (FR-3.9) |
| `rejection_reason`| TEXT | NULLABLE | Mandatory reason if rejected (FR-4.3) |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Submission timestamp |
| `due_at` | DATETIME | NULLABLE | Computed SLA target deadline (FR-3.7) |
| `resolved_at` | DATETIME | NULLABLE | Final resolution timestamp (FR-4.2) |

### 2.5 Table: `complaint_updates`
| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique update identifier |
| `complaint_id` | INTEGER | NOT NULL, FK `complaints(id)` | Target complaint reference |
| `updated_by` | INTEGER | NULLABLE, FK `users(id)` | Author of the remark or status change |
| `old_status` | VARCHAR(30) | NULLABLE | Status before this update |
| `new_status` | VARCHAR(30) | NULLABLE | Status after this update |
| `remark` | TEXT | NOT NULL | Progress note or discussion message |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Remark timestamp |

### 2.6 Table: `feedback`
| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique feedback identifier |
| `complaint_id` | INTEGER | UNIQUE, NOT NULL, FK `complaints(id)` | Only 1 feedback per ticket (FR-6.1) |
| `user_id` | INTEGER | NOT NULL, FK `users(id)` | Complainant submitting feedback |
| `rating` | INTEGER | NOT NULL, CHECK (1 <= rating <= 5) | Satisfaction star rating |
| `comment` | TEXT | NULLABLE | Qualitative review note |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Feedback timestamp |

### 2.7 Table: `notifications`
| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique notification identifier |
| `user_id` | INTEGER | NOT NULL, FK `users(id)` | Recipient user identifier |
| `complaint_id` | INTEGER | NULLABLE, FK `complaints(id)` | Related grievance ticket |
| `message` | VARCHAR(255) | NOT NULL | Brief alert message |
| `is_read` | BOOLEAN | NOT NULL, DEFAULT 0 | Read flag |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Notification timestamp |

### 2.8 Table: `audit_logs`
| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique audit entry identifier |
| `user_id` | INTEGER | NULLABLE, FK `users(id)` | Administrative user performing action |
| `action` | VARCHAR(100) | NOT NULL | Action description (e.g. Assigned, Created) |
| `target_id` | VARCHAR(50) | NULLABLE | Target identifier or category name |
| `details` | TEXT | NULLABLE | Contextual details and changes |
| `ip_address` | VARCHAR(50) | NULLABLE | Client IP address for audit compliance |
| `created_at` | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Timestamp of action |

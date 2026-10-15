# System Modules & Code Architecture

**Project**: Online Complaint Management System (OCMS)  
**Standard**: IEEE Std 830-1998 Conforming  
**Architecture**: Flask Application Factory Pattern with Domain Blueprints

---

## 1. Directory & Package Structure

```
OCMS/
├── app/                        # Application Package
│   ├── __init__.py             # Application factory, extensions, and error handlers
│   ├── models.py               # Normalized SQLAlchemy ORM models
│   ├── forms.py                # Flask-WTF validation forms
│   ├── utils.py                # Security decorators, SLA calculator, file handlers
│   ├── auth/                   # Authentication Blueprint
│   │   ├── __init__.py
│   │   └── routes.py           # Login, registration, lockout, password reset
│   ├── main/                   # Public Visitor Blueprint
│   │   ├── __init__.py
│   │   └── routes.py           # Landing page, public tracker
│   ├── user/                   # Citizen / Complainant Blueprint
│   │   ├── __init__.py
│   │   └── routes.py           # Filing, tracking, conversation, feedback, reopen
│   ├── staff/                  # Field Technician Blueprint
│   │   ├── __init__.py
│   │   └── routes.py           # Assigned queue, status progression, resolution
│   └── admin/                  # System Administrator Blueprint
│       ├── __init__.py
│       └── routes.py           # Executive dashboard, triage, users, categories, reports
├── config.py                   # Environment configurations (Dev, Test, Prod)
├── seed.py                     # Realistic database seeder
├── app.py                      # Root execution runner
├── requirements.txt            # Python dependencies
├── static/                     # CSS, JavaScript, and user uploads
│   ├── css/theme.css           # Styling
│   ├── js/main.js              # Client interactions
│   ├── js/charts.js            # Dynamic Chart.js dashboard integration
│   └── uploads/                # Secured file attachments
├── templates/                  # Jinja2 HTML templates
│   ├── base.html               # Master layout wrapper
│   ├── errors/                 # 403, 404, 500 custom error pages
│   ├── partials/               # Navbar, sidebar, role switcher, flash messages
│   ├── public/                 # Landing, login, register, forgot password, tracker
│   ├── user/                   # Complainant dashboard, my complaints, submit, details
│   ├── staff/                  # Technician dashboard, assigned tasks, resolution desk
│   └── admin/                  # Admin dashboard, complaints, users, categories, reports
├── tests/                      # pytest test suite
│   ├── conftest.py             # Fixtures and test helpers
│   ├── test_auth.py            # Registration, lockout, password security tests
│   ├── test_complaints.py      # Lifecycle, isolation, privacy, reopen tests
│   ├── test_admin_staff.py     # Access control, triage, resolution, category CRUD
│   └── test_features.py        # Feedback, notifications, attachments, CSV export
└── docs/                       # Specifications and generated documentation
    ├── SRS.pdf                 # IEEE Std 830-1998 Specification
    └── generated/              # Auto-generated schemas, catalogs, and test matrices
```

---

## 2. Core Modules & Responsibilities

### 2.1 `app/__init__.py` (Application Factory)
- Instantiates Flask application via `create_app(config_name)`.
- Configures extensions: `Flask-SQLAlchemy` (`db`), `Flask-Login` (`login_manager`), `Flask-WTF` (`csrf`).
- Implements `smart_url_for` global helper supporting both blueprint-prefixed and root endpoints seamlessly in Jinja2 templates.
- Injects global context processors (`active_role`, `categories`, `unread_notifications_count`).
- Registers custom error handlers for HTTP 403 (Forbidden), HTTP 404 (Not Found), and HTTP 500 (Internal Server Error).
- Provides instant viva demo role switcher `/switch-role/<role>` (`guest`, `user`, `staff`, `admin`).

### 2.2 `app/models.py` (Domain Data Layer)
- Defines 8 normalized tables with foreign keys and cascade rules.
- Implements `SliceableDateTimeType` and `SliceableDateTime` enabling string-slicing (e.g. `c.created_at[:10]`) in legacy Jinja2 templates while preserving native datetime operations in Python.
- Provides helper properties (`user_name`, `user_email`, `user_phone`, `assigned_name`, `category_name`, `complaint_no`, `comments`, `attachments`, `is_overdue`) ensuring backwards compatibility with templates.
- Includes password hashing methods (`set_password`, `check_password`) and account lockout tracking (`record_failed_login`, `reset_failed_logins`, `is_locked`).
- Includes secure password reset token generation using `URLSafeTimedSerializer`.

### 2.3 `app/forms.py` (WTF Form Validations)
- `LoginForm`: email and password validation.
- `RegistrationForm`: name, email, phone, password length (>=8), digit check, and confirmation matching.
- `ComplaintForm`: category, title, description, location, priority, and file uploads.
- `CategoryForm`: category name, description, SLA hours.
- `FeedbackForm`: 1-5 star rating and review comment.

### 2.4 `app/utils.py` (Security & Utility Functions)
- `@admin_required`: Enforces administrator-only route protection with HTTP 403 abort.
- `@staff_required`: Enforces staff or admin access with HTTP 403 abort.
- `generate_tracking_number()`: Generates unique format `OCMS-YYYY-XXXX`.
- `calculate_due_date(category, priority)`: Priority-weighted SLA calculation (`Urgent`=0.25x, `High`=0.5x, `Medium`=1.0x, `Low`=1.5x) enforcing minimum 4h floor (FR-3.7).
- `save_attachment(file_obj)`: Validates file extensions (`.png`, `.jpg`, `.jpeg`, `.pdf`), enforces 5MB limit, hashes filename with `uuid4`, and saves to uploads directory.
- `send_notification(user_id, message)`: Records in-app alerts.
- `record_audit(action, target_id, details)`: Appends to security audit log.

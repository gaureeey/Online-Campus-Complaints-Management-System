# Test Suite & Verification Matrix

**System**: Online Complaint Management System (OCMS)  
**Standard**: IEEE Std 830-1998 Conforming  
**Test Framework**: pytest 9.x  
**Results**: **35 Passed, 0 Failed, 0 Errors** (100% Pass Rate)

---

## 1. Test Execution Summary

| Test Module | Total Tests | Passed | Failed | Areas Covered |
|:---|:---:|:---:|:---:|:---|
| `tests/test_auth.py` | 12 | 12 | 0 | Registration, duplicate check, password strength, account lockout, login, logout, password reset tokens, viva role switcher |
| `tests/test_complaints.py` | 8 | 8 | 0 | Filing, tracking tokens, status filtering, access isolation, withdrawal rules, discussion comments, 7-day reopening, public privacy |
| `tests/test_admin_staff.py` | 8 | 8 | 0 | Role-based 403 access control, staff allocation, admin status/priority override, staff queue isolation, resolution notes, rejection reason check, category CRUD & delete integrity |
| `tests/test_features.py` | 7 | 7 | 0 | 1-5 star feedback, duplicate feedback rejection, file attachment validation, notification center, CSV report export, audit log recording |
| **Total** | **35** | **35** | **0** | **Complete SRS Functional Coverage** |

---

## 2. Comprehensive Test Case Mapping

### 2.1 Authentication & Security (`tests/test_auth.py`)

| Test Function | SRS Requirements | Precondition | Test Input | Expected Result | Status |
|:---|:---|:---|:---|:---|:---:|
| `test_registration_success` | FR-1.1, FR-1.4, TC-1 | User does not exist | Valid name, unique email, phone, strong password | Account created, password hashed with scrypt, 200 OK | **PASSED** |
| `test_registration_duplicate_email` | FR-1.1, TC-1 | Email already registered | Registration with existing email | Error message displayed; duplicate blocked | **PASSED** |
| `test_registration_weak_password` | FR-1.2 | N/A | Password <8 chars or missing digits | Registration rejected; policy message shown | **PASSED** |
| `test_registration_password_mismatch` | FR-1.1 | N/A | `password != confirm_password` | Form rejected with mismatch notification | **PASSED** |
| `test_login_user_success` | FR-1.3 | Registered student | Correct email & password | Authenticated; redirected to `/dashboard` | **PASSED** |
| `test_login_staff_success` | FR-1.3 | Registered staff | Correct email & password | Authenticated; redirected to `/staff/dashboard` | **PASSED** |
| `test_login_admin_success` | FR-1.3 | Registered admin | Correct email & password | Authenticated; redirected to `/admin/dashboard` | **PASSED** |
| `test_login_invalid_password_and_failed_attempts` | FR-1.8 | Registered user | Incorrect password | `failed_attempts` incremented; warning shown | **PASSED** |
| `test_account_lockout_after_five_failed_attempts` | FR-1.8 | Registered user | 5 consecutive bad passwords | Account locked for 15 minutes; subsequent logins blocked | **PASSED** |
| `test_logout` | FR-1.3 | Logged in session | Click logout | Session cleared; redirected to login with flash notice | **PASSED** |
| `test_password_recovery_token` | FR-1.6 | Registered user | Forgot password token | Secure token generated; verifies within 15 mins; password updated | **PASSED** |
| `test_switch_role_personas` | Evaluation Demo | Database seeded | Switch to `user`, `staff`, `admin`, `guest` | Instant session toggle to target persona without errors | **PASSED** |

### 2.2 Complaint Lifecycle (`tests/test_complaints.py`)

| Test Function | SRS Requirements | Precondition | Test Input | Expected Result | Status |
|:---|:---|:---|:---|:---|:---:|
| `test_submit_complaint_generates_tracking_number` | FR-2.1, FR-2.2, FR-3.7 | Logged in as User | Valid subject, category, description, priority | Ticket created with format `OCMS-YYYY-XXXX`; SLA due date computed | **PASSED** |
| `test_my_complaints_list_and_status_filtering` | FR-2.5, FR-2.6 | User with complaints | Query with `?status=Resolved` | Returns only complaints matching filter | **PASSED** |
| `test_access_isolation_user_cannot_view_others_complaint` | NFR-4 | Complaint by User 1 | User 2 accesses ticket detail URL | HTTP 403 Forbidden; access denied | **PASSED** |
| `test_withdraw_complaint_when_submitted` | FR-2.9 | Ticket in `Submitted` status | Post withdraw | Status changes to `Withdrawn`; history update logged | **PASSED** |
| `test_withdraw_complaint_blocked_when_assigned` | FR-2.9 | Ticket in `Assigned` status | Post withdraw | Withdrawal rejected; status remains `Assigned` | **PASSED** |
| `test_add_comment_to_conversation_thread` | FR-2.8 | Active complaint | User submits remark text | Comment appended to timeline history | **PASSED** |
| `test_reopen_resolved_complaint_within_window` | FR-2.10 | Ticket resolved 2 days ago | User submits reopen reason | Status updated to `Reopened`; notification dispatched | **PASSED** |
| `test_public_tracking_privacy` | FR-2.7, Privacy | Active complaint | Public query `/track?complaint_no=...` | Displays status and timeline; conceals email and phone | **PASSED** |

### 2.3 Administrative & Staff Workflows (`tests/test_admin_staff.py`)

| Test Function | SRS Requirements | Precondition | Test Input | Expected Result | Status |
|:---|:---|:---|:---|:---|:---:|
| `test_user_blocked_from_admin_dashboard` | NFR-4 | Logged in as User | Access `/admin/dashboard` | HTTP 403 Forbidden | **PASSED** |
| `test_user_blocked_from_staff_dashboard` | NFR-4 | Logged in as User | Access `/staff/dashboard` | HTTP 403 Forbidden | **PASSED** |
| `test_admin_assign_staff` | FR-3.3 | Unassigned complaint | Admin assigns to Staff ID | Status becomes `Assigned`; technician assigned; update logged | **PASSED** |
| `test_admin_update_status_and_priority` | FR-3.2, FR-3.7 | Active complaint | Admin updates priority & remark | Priority updated; remarks logged in timeline | **PASSED** |
| `test_staff_assigned_queue` | FR-4.1 | Multiple complaints in DB | Staff logs into workspace | Staff only sees tickets allocated to their ID | **PASSED** |
| `test_staff_update_status_to_resolved` | FR-4.2 | In-progress ticket | Staff marks `Resolved` with note | Status becomes `Resolved`; `resolved_at` recorded | **PASSED** |
| `test_staff_reject_requires_reason` | FR-4.3 | Active ticket | Staff marks `Rejected` without note | Rejection blocked; mandatory reason enforced | **PASSED** |
| `test_admin_category_crud_and_delete_protection` | FR-3.4, DB Integrity | Category with complaints | Attempt category delete | Delete blocked when complaints attached; succeeds when clean | **PASSED** |

### 2.4 Ancillary Features & Reports (`tests/test_features.py`)

| Test Function | SRS Requirements | Precondition | Test Input | Expected Result | Status |
|:---|:---|:---|:---|:---|:---:|
| `test_feedback_submission_on_resolved_complaint` | FR-6.1 | Resolved ticket | 5-star rating and comment | Rating stored in database; review displayed | **PASSED** |
| `test_duplicate_feedback_prevented` | FR-6.1 | Ticket already rated | Second feedback submission | Blocked; original feedback preserved intact | **PASSED** |
| `test_file_attachment_upload_valid` | FR-2.3, TC-3 | Logged in as User | PNG file attached | File saved to `static/uploads/` with UUID filename | **PASSED** |
| `test_file_attachment_upload_invalid_extension` | FR-2.3 | Logged in as User | `.exe` file attached | Rejected with invalid format warning | **PASSED** |
| `test_mark_notifications_as_read` | FR-5.3 | Unread notifications | Post `/notifications/mark-read` | All user notifications flagged `is_read=True` | **PASSED** |
| `test_admin_csv_export_report` | FR-7.3 | Database with complaints | Get `/admin/reports?export=csv` | HTTP 200 with `text/csv` header and CSV payload | **PASSED** |
| `test_audit_trail_recorded_on_admin_action` | FR-3.10 | Admin session | Admin category modification | Audit entry logged with user, action, target, IP | **PASSED** |

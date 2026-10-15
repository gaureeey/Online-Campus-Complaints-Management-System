# System Route Catalog

**Application**: Online Complaint Management System (OCMS)  
**Standard**: IEEE Std 830-1998 Conforming  
**Architecture**: Modular Flask Blueprints (`main`, `auth`, `user`, `staff`, `admin`)

---

## 1. Blueprint: `main` (Public & Visitor Module)
| Route / URL | HTTP Methods | Endpoint | Role Access | Description | SRS Reference |
|:---|:---|:---|:---|:---|:---|
| `/` | GET | `main.index` | Public | Landing page with hero, 4-step workflow, categories, and metrics | Section 3.1 |
| `/track` | GET | `main.track_public` | Public | Public grievance tracker by complaint number (privacy-preserving) | FR-2.7 |

---

## 2. Blueprint: `auth` (Authentication & Security Module)
| Route / URL | HTTP Methods | Endpoint | Role Access | Description | SRS Reference |
|:---|:---|:---|:---|:---|:---|
| `/login` | GET, POST | `auth.login` | Public | User, Staff, Admin authentication with 15-min lockout | FR-1.3, FR-1.8 |
| `/register` | GET, POST | `auth.register` | Public | Complainant account registration with password policy check | FR-1.1, FR-1.2 |
| `/forgot-password` | GET, POST | `auth.forgot_password` | Public | Request time-limited (15 min) password recovery token | FR-1.6 |
| `/reset-password/<token>`| GET, POST | `auth.reset_password` | Public | Verify token and update password | FR-1.6 |
| `/logout` | GET | `auth.logout` | Authenticated | Session termination and cleanup | FR-1.3 |

---

## 3. Blueprint: `user` (Citizen / Complainant Module)
| Route / URL | HTTP Methods | Endpoint | Role Access | Description | SRS Reference |
|:---|:---|:---|:---|:---|:---|
| `/dashboard` | GET | `user.user_dashboard` | Complainant | Aggregate metric cards and recent complaints | Section 3.2 |
| `/complaints` or `/complaints/my` | GET | `user.my_complaints` | Complainant | List personal complaints with status/priority filtering | FR-2.5, FR-2.6 |
| `/complaint/new` | GET, POST | `user.submit_complaint` | Complainant | Submit new maintenance ticket with file attachment | FR-2.1, 2.2, 2.3 |
| `/complaint/success/<complaint_no>`| GET | `user.complaint_success` | Complainant | Confirmation screen showing reference number | FR-2.2 |
| `/complaint/<complaint_no>` | GET | `user.complaint_detail` | Complainant | Detailed ticket inspect, timeline, and actions | FR-2.5 |
| `/complaint/<complaint_no>/comment` | POST | `user.add_comment` | Complainant | Post message into ticket discussion thread | FR-2.8 |
| `/complaint/<complaint_no>/feedback`| POST | `user.submit_feedback` | Complainant | Submit 1-5 star rating and service review | FR-6.1 |
| `/complaint/<complaint_no>/withdraw`| POST | `user.withdraw_complaint`| Complainant | Withdraw ticket while in Submitted status | FR-2.9 |
| `/complaint/<complaint_no>/reopen` | POST | `user.reopen_complaint` | Complainant | Reopen resolved ticket within 7-day window | FR-2.10 |
| `/notifications` | GET | `user.notifications` | Complainant | In-app notification center | FR-5.3 |
| `/notifications/mark-read` | POST | `user.mark_notifications_read` | Complainant | Mark unread notifications as read | FR-5.3 |
| `/profile` | GET, POST | `user.profile` | Complainant | Edit contact phone or change account password | FR-1.5 |

---

## 4. Blueprint: `staff` (Technician / Field Officer Module)
| Route / URL | HTTP Methods | Endpoint | Role Access | Description | SRS Reference |
|:---|:---|:---|:---|:---|:---|
| `/staff/dashboard` | GET | `staff.staff_dashboard` | Staff | Technician dashboard showing allocated queue and workload | FR-4.4 |
| `/staff/complaints` | GET | `staff.staff_complaints` | Staff | Assigned grievance queue with search and filter | FR-4.1 |
| `/staff/complaint/<complaint_no>` | GET | `staff.staff_complaint_detail`| Staff | Resolution workspace for individual assigned ticket | Section 3.4 |
| `/staff/complaint/<complaint_no>/update-status` | POST | `staff.staff_update_status` | Staff | Update status (In Progress, Resolved, Rejected) | FR-4.2, FR-4.3 |

---

## 5. Blueprint: `admin` (Administrator Module)
| Route / URL | HTTP Methods | Endpoint | Role Access | Description | SRS Reference |
|:---|:---|:---|:---|:---|:---|
| `/admin/dashboard` | GET | `admin.admin_dashboard` | Admin | Executive analytics dashboard with KPI cards and charts | FR-7.1, 7.4, 7.5 |
| `/admin/api/stats` | GET | `admin.admin_api_stats` | Admin | JSON API for Chart.js rendering (trends & categories) | FR-7.4 |
| `/admin/complaints` | GET | `admin.admin_complaints` | Admin | System-wide complaint registry with multi-criteria filters | FR-3.1 |
| `/admin/complaint/<complaint_no>` | GET | `admin.admin_complaint_detail` | Admin | Master triage, priority review, and inspect view | FR-3.2 |
| `/admin/complaint/<complaint_no>/assign` | POST | `admin.admin_assign_staff` | Admin | Assign or reallocate complaint to technician staff | FR-3.3 |
| `/admin/complaint/<complaint_no>/update-status` | POST | `admin.admin_update_status` | Admin | Administrative override of status and priority | FR-3.2, FR-3.7 |
| `/admin/complaint/<complaint_no>/merge` | POST | `admin.admin_merge_complaint` | Admin | Merge duplicate complaint into parent master ticket | FR-3.9 |
| `/admin/users` | GET | `admin.admin_users` | Admin | Manage student and staff accounts | FR-3.5 |
| `/admin/users/add` | POST | `admin.admin_add_user` | Admin | Create new user or technician account | FR-3.5 |
| `/admin/users/<int:user_id>/toggle` | POST | `admin.admin_toggle_user` | Admin | Activate or deactivate user account | FR-3.5 |
| `/admin/categories` | GET | `admin.admin_categories` | Admin | Manage complaint categories and SLA targets | FR-3.4 |
| `/admin/categories/add` | POST | `admin.admin_add_category` | Admin | Add new complaint category | FR-3.4 |
| `/admin/categories/<int:category_id>/edit` | POST | `admin.admin_edit_category` | Admin | Edit category name, description, SLA duration | FR-3.4 |
| `/admin/categories/<int:category_id>/toggle` | POST | `admin.admin_toggle_category`| Admin | Activate or pause category | FR-3.4 |
| `/admin/categories/<int:category_id>/delete` | POST | `admin.admin_delete_category`| Admin | Delete category (blocked if complaints attached) | DB Integrity |
| `/admin/reports` | GET | `admin.admin_reports` | Admin | Grievance reports with category/status filters and CSV export | FR-7.2, FR-7.3 |
| `/admin/audit-log` | GET | `admin.admin_audit_log` | Admin | System security and administrative audit trail | FR-3.10 |

---

## 6. Helper & Demo Route
| Route / URL | HTTP Methods | Endpoint | Role Access | Description |
|:---|:---|:---|:---|:---|
| `/switch-role/<role>` | GET | `switch_role` | Any | Rapid persona switcher for viva and evaluation (`guest`, `user`, `staff`, `admin`) |

# Online Campus Complaints Management System (OCMS)
## System Design: Comprehensive UML & Data Flow Diagrams (DFD) Specification
**Document Version:** 1.0  
**Standard Compliance:** IEEE Std 830-1998 (SRS) & ISO/IEC/IEEE 42010 Systems Architecture  
**Author / System:** OCMS Engineering & System Architecture Team  
**Date:** October 2026  

---

## Table of Contents
1. [Executive Summary & Notation Standards](#1-executive-summary--notation-standards)
2. [Data Flow Diagrams (DFD)](#2-data-flow-diagrams-dfd)
   - [2.1 DFD Level 0: Context Analysis Diagram](#21-dfd-level-0-context-analysis-diagram)
   - [2.2 DFD Level 1: Subsystem Functional Decomposition](#22-dfd-level-1-subsystem-functional-decomposition)
   - [2.3 DFD Level 2.1: Complaint Filing & SLA Token Engine](#23-dfd-level-21-complaint-filing--sla-token-engine)
   - [2.4 DFD Level 2.2: Administrative Triage & Staff Allocation](#24-dfd-level-22-administrative-triage--staff-allocation)
   - [2.5 DFD Level 2.3: Work Execution, Resolution & 7-Day Reopen Loop](#25-dfd-level-23-work-execution-resolution--7-day-reopen-loop)
   - [2.6 Data Dictionary of Flows & Stores](#26-data-dictionary-of-flows--stores)
3. [UML Behavioral Diagrams](#3-uml-behavioral-diagrams)
   - [3.1 Use Case Diagram (Actors, Boundaries, Includes & Extends)](#31-use-case-diagram)
   - [3.2 Sequence Diagram 1: Complaint Submission & Dynamic SLA Computation](#32-sequence-diagram-1-complaint-submission--dynamic-sla-computation)
   - [3.3 Sequence Diagram 2: Administrative Triage & Technician Allocation](#33-sequence-diagram-2-administrative-triage--technician-allocation)
   - [3.4 Sequence Diagram 3: Repair Execution, Star Rating & 7-Day Reopening](#34-sequence-diagram-3-repair-execution-star-rating--7-day-reopening)
   - [3.5 State Machine Diagram: Complaint Lifecycle Statechart](#35-state-machine-diagram-complaint-lifecycle-statechart)
   - [3.6 Activity Diagram: End-to-End Swimlane Workflow](#36-activity-diagram-end-to-end-swimlane-workflow)
4. [UML Structural Diagrams](#4-uml-structural-diagrams)
   - [4.1 Class Diagram (Full Domain Model, Operations & Multiplicities)](#41-class-diagram)
   - [4.2 Component Diagram (3-Tier Blueprint & Module Architecture)](#42-component-diagram)
   - [4.3 Deployment Diagram (Physical Nodes, WSGI, File System & DB Engine)](#43-deployment-diagram)
5. [Traceability Matrix (SRS Requirements to Diagrammatic Artifacts)](#5-traceability-matrix)

---

## 1. Executive Summary & Notation Standards

This technical specification details the structural, behavioral, and data-flow models of the **Online Campus Complaints Management System (OCMS)**. OCMS is an enterprise-grade grievance redressal web application tailored for higher education campuses, residential hostels, and departmental facilities.

### 1.1 Diagrammatic Conventions

#### Data Flow Diagrams (DFD)
DFD diagrams follow the standard **Yourdon & DeMarco / Gane & Sarson** conventions:
* **External Entities (Square / Box)**: External actors producing or consuming data (`Student/Citizen`, `Technician/Staff`, `Administrator`, `System Clock/Scheduler`).
* **Processes (Rounded Rectangle / Circle)**: Transformations of data designated by numbering hierarchy (`0.0`, `1.0` through `6.0`, `2.1` through `2.5`).
* **Data Stores (Open-ended Rectangle / Double Bar)**: Persistent tables within the relational database (`D1: users`, `D2: categories`, `D3: complaints`, etc.).
* **Data Flows (Directed Arrows)**: Named packets of information traveling between entities, processes, and stores.

#### Unified Modeling Language (UML 2.5)
* **Use Case Diagrams**: Depicts functional goals across primary actors, featuring `<<include>>` (mandatory sub-routines) and `<<extend>>` (conditional workflows).
* **Class Diagrams**: Documents object-oriented entity classes, attributes with visibility (`+` public, `-` private, `#` protected), data types, member operations, associations, and exact multiplicities.
* **Sequence Diagrams**: Chronological interaction graphs illustrating messages passing across lifelines with activation boxes and return parameters.
* **State Machine Diagrams**: Finite state transition graph detailing valid lifecycle states (`Submitted`, `Assigned`, `In Progress`, `Resolved`, `Closed`, `Rejected`, `Withdrawn`, `Reopened`).
* **Component & Deployment Diagrams**: Architectural topology mapping modular Python Flask Blueprints, ORM abstractions, SQLite database files, and network tiers.

---

## 2. Data Flow Diagrams (DFD)

### 2.1 DFD Level 0: Context Analysis Diagram

The Level 0 Context Diagram establishes the boundary of the OCMS system, illustrating all external entities that interact directly with the environment and the core data payloads exchanged.

```mermaid
graph TD
    %% External Entities
    User["Complainant<br/>(Student / Resident / Citizen)"]
    Staff["Technician Staff<br/>(Electrician, Plumber, IT)"]
    Admin["Campus Administrator<br/>(Facility Manager / Warden)"]
    Clock["System Timer / Scheduler<br/>(SLA Monitor)"]

    %% Central System
    OCMS(("0.0<br/>Online Campus Complaints<br/>Management System<br/>(OCMS)"))

    %% Complainant Flows
    User -->|Registration, Login Credentials| OCMS
    User -->|Complaint Details, Location, Urgency, Photos/PDF| OCMS
    User -->|1-5 Star Rating & Review, Reopen Justification| OCMS
    User -->|Ticket Withdrawal, Discussion Comment| OCMS
    OCMS -->|Tracking Token OCMS-YYYY-XXXX, Public Status| User
    OCMS -->|In-App Notifications, Milestone Updates| User

    %% Staff Flows
    Staff -->|Staff Login Credentials| OCMS
    Staff -->|Work Progression: In Progress / Resolved| OCMS
    Staff -->|Work Remarks, Rejection Reason| OCMS
    OCMS -->|Assigned Task Queue, SLA Deadlines, Attachments| Staff
    OCMS -->|Staff Performance Metrics| Staff

    %% Admin Flows
    Admin -->|Admin Authentication| OCMS
    Admin -->|Triage Allocation Staff ID, Priority Override| OCMS
    Admin -->|Category CRUD, SLA Target Hours, Icon| OCMS
    Admin -->|User Account Toggles, Duplicate Merging| OCMS
    Admin -->|Report Filter Criteria Date, Category, Status| OCMS
    OCMS -->|Executive KPI Cards, Chart.js Trend Visuals| Admin
    OCMS -->|SLA Breach Alerts, Exported CSV Datasets| Admin
    OCMS -->|Security Audit Trail Logs| Admin

    %% Clock Flows
    Clock -->|Hourly SLA Heartbeat Pulse| OCMS
    OCMS -->|Overdue Escalation Flagging| Clock

    %% Styling
    classDef entity fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#f8fafc;
    classDef system fill:#0f766e,stroke:#14b8a6,stroke-width:3px,color:#ffffff;
    class User,Staff,Admin,Clock entity;
    class OCMS system;
```

#### Primary Input & Output Data Flows (Level 0)

| External Entity | Inbound Data Flow to OCMS | Outbound Data Flow from OCMS |
|:---|:---|:---|
| **Complainant (User)** | Registration profile, login credentials, complaint payload (category, urgency, location, description, photo attachment), discussion comments, withdrawal request, 1–5 star rating, reopen reason. | Dynamic tracking number (`OCMS-YYYY-XXXX`), public status lookup response, real-time in-app notifications, complaint lifecycle timeline updates. |
| **Technician (Staff)** | Staff login credentials, status transition requests (`In Progress`, `Resolved`), repair remarks, mandatory rejection reasons. | Filtered assigned work queue, incident location, complainant contact/location details, SLA countdown timer. |
| **Campus Administrator** | Staff triage assignments, priority overrides, category & SLA hour configurations, user account activations/deactivations, duplicate parent-child links, report filter parameters. | Real-time KPI summaries, overdue ticket escalation notices, downloadable CSV reports, Chart.js analytics payloads, immutable audit logs. |
| **System Timer / Clock** | Chronological tick / SLA verification trigger. | Tickets flagged as `is_overdue = True`, escalation notifications. |

---

### 2.2 DFD Level 1: Subsystem Functional Decomposition

The Level 1 DFD decomposes the monolithic system into **6 major functional processes** and shows how data moves between external actors, processes, and the **8 normalized database tables (Data Stores)**.

```mermaid
graph TD
    %% Entities
    E_User["Complainant (Student)"]
    E_Staff["Technician (Staff)"]
    E_Admin["Administrator"]
    E_Clock["Timer / SLA Daemon"]

    %% Processes
    P1["1.0<br/>Authentication &<br/>Profile Governance"]
    P2["2.0<br/>Complaint Ingestion &<br/>Token Generation"]
    P3["3.0<br/>Administrative Triage<br/>& Allocation"]
    P4["4.0<br/>Staff Work Order<br/>& Progress Tracking"]
    P5["5.0<br/>Service Rating,<br/>Feedback & Reopen"]
    P6["6.0<br/>Analytics, Audit Trail<br/>& SLA Monitoring"]

    %% Data Stores
    D1[("D1: users")]
    D2[("D2: categories")]
    D3[("D3: departments")]
    D4[("D4: complaints")]
    D5[("D5: complaint_updates")]
    D6[("D6: feedback")]
    D7[("D7: notifications")]
    D8[("D8: audit_logs")]

    %% P1 Auth Flows
    E_User -->|Credentials, Email, Password| P1
    E_Staff -->|Staff Credentials| P1
    E_Admin -->|Admin Credentials| P1
    P1 <-->|Verify Hash / Lockout (15 min)| D1
    P1 -->|Log Auth Success / Failure| D8
    P1 -->|Session Token & User Role| E_User

    %% P2 Complaint Ingestion Flows
    E_User -->|Title, Category, Urgency, Room, Media| P2
    P2 <-->|Read Category SLA Hours| D2
    P2 -->|Generate OCMS-YYYY-XXXX & Insert| D4
    P2 -->|Record Initial History Event| D5
    P2 -->|Return Reference Token| E_User

    %% P3 Triage & Assignment Flows
    E_Admin -->|Assign Staff ID, Priority Override| P3
    P3 <-->|Query Technicians by Department| D1
    P3 <-->|Lookup Submitted Grievances| D4
    P3 -->|Update assigned_to, status='Assigned'| D4
    P3 -->|Append Assignment Remark| D5
    P3 -->|Dispatch User & Staff Notification| D7
    P3 -->|Write Action to Audit Log| D8

    %% P4 Staff Work Order Flows
    E_Staff -->|Update: In Progress / Resolved / Reject| P4
    P4 <-->|Fetch Assigned Tickets for Staff ID| D4
    P4 -->|Update status, resolved_at Timestamp| D4
    P4 -->|Append Work Remark / Rejection Reason| D5
    P4 -->|Trigger Milestone Notification| D7

    %% P5 Feedback & Reopen Flows
    E_User -->|1-5 Star Rating & Feedback Comment| P5
    E_User -->|Reopen Justification Note (<=7 Days)| P5
    P5 -->|Insert Rating Record| D6
    P5 -->|Update status='Closed' on Feedback| D4
    P5 -->|Update status='Reopened' on Escalation| D4
    P5 -->|Log Reopen History Event| D5
    P5 -->|Alert Admin of Reopened Case| D7

    %% P6 SLA & Reporting Flows
    E_Clock -->|Time Check Pulse| P6
    E_Admin -->|Request Filtered Reports / CSV Export| P6
    P6 <-->|Query Grievance Metrics & SLA Deadlines| D4
    P6 <-->|Fetch Audit Trail Records| D8
    P6 -->|Write Overdue Alert Notification| D7
    P6 -->|CSV Dataset & Chart API Data| E_Admin

    %% Notification Read Flows
    D7 -->|In-App Unread Alerts| E_User
    D7 -->|Task Assignment Alerts| E_Staff

    %% Styling
    classDef entity fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#f8fafc;
    classDef process fill:#0284c7,stroke:#38bdf8,stroke-width:2px,color:#ffffff;
    classDef store fill:#334155,stroke:#f59e0b,stroke-width:2px,color:#fef3c7;
    class E_User,E_Staff,E_Admin,E_Clock entity;
    class P1,P2,P3,P4,P5,P6 process;
    class D1,D2,D3,D4,D5,D6,D7,D8 store;
```

---

### 2.3 DFD Level 2.1: Complaint Filing & SLA Token Engine

This diagram decomposes **Process 2.0 (Complaint Ingestion & Token Generation)** into granular subprocesses, detailing data validation, UUID media storage, SLA computation, and reference number generation.

```mermaid
graph TD
    %% Entity
    Complainant["Complainant (Student)"]

    %% Sub-processes of 2.0
    P2_1["2.1<br/>Validate Payload<br/>(CSRF & Fields)"]
    P2_2["2.2<br/>File Attachment<br/>Validation & UUID Save"]
    P2_3["2.3<br/>Compute Dynamic SLA<br/>Target Due Date"]
    P2_4["2.4<br/>Generate Sequential<br/>Tracking Token"]
    P2_5["2.5<br/>Commit Complaint<br/>& Event Log"]

    %% Data Stores
    D_Cat[("D2: categories")]
    D_Comp[("D4: complaints")]
    D_Upd[("D5: complaint_updates")]
    FS[("File System:<br/>/static/uploads/")]

    %% Flows
    Complainant -->|Form Post: Category, Title, Priority, Room, File| P2_1
    P2_1 -->|Sanitized Form Data| P2_2
    P2_2 -->|Raw Binary Stream (.jpg, .png, .pdf <= 5MB)| FS
    FS -->|Unique Stored Filename uuid_name.ext| P2_2
    P2_2 -->|Validated Attachment Path| P2_3

    P2_3 <-->|Read category.sla_hours| D_Cat
    P2_3 -->|Compute due_at = now + base * multiplier| P2_4

    P2_4 <-->|Query latest OCMS-YYYY-XXXX| D_Comp
    P2_4 -->|Next Tracking Number OCMS-2026-0042| P2_5

    P2_5 -->|INSERT INTO complaints status='Submitted'| D_Comp
    P2_5 -->|INSERT INTO complaint_updates 'Registered'| D_Upd
    P2_5 -->|Return Success Screen with Token| Complainant

    %% Styling
    classDef entity fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#f8fafc;
    classDef process fill:#0284c7,stroke:#38bdf8,stroke-width:2px,color:#ffffff;
    classDef store fill:#334155,stroke:#f59e0b,stroke-width:2px,color:#fef3c7;
    class Complainant entity;
    class P2_1,P2_2,P2_3,P2_4,P2_5 process;
    class D_Cat,D_Comp,D_Upd,FS store;
```

#### Detailed Process Specifications for Subprocess 2.0

* **Process 2.1 (Validate Payload)**: Validates title length (3–200 chars), non-empty description, room/location string, and verifies CSRF session token.
* **Process 2.2 (Media Storage)**: Validates extension against whitelist (`.png`, `.jpg`, `.jpeg`, `.pdf`) and ensures payload $\le 5\text{ MB}$. Generates 12-char hex UUID prefix (`uuid4().hex[:12] + '_' + secure_filename`) to prevent overwrite attacks.
* **Process 2.3 (SLA Computation)**:
  $$\text{SLA Hours} = \max\left(4, \text{base\_hours} \times \text{multiplier}\right)$$
  Where $\text{Urgent}=0.25$, $\text{High}=0.50$, $\text{Medium}=1.0$, $\text{Low}=1.50$.
* **Process 2.4 (Sequential Token Minting)**: Queries database for highest sequence in current calendar year (`OCMS-YYYY-XXXX`), increments counter with race-condition safety.
* **Process 2.5 (Commit & Log)**: Atomically writes complaint entity with status `Submitted`, inserts first timeline record in `complaint_updates`, and issues confirmation.

---

### 2.4 DFD Level 2.2: Administrative Triage & Staff Allocation

Decomposes **Process 3.0 (Administrative Triage & Allocation)** into five sub-operations.

```mermaid
graph TD
    Admin["Campus Administrator"]

    P3_1["3.1<br/>Fetch Triage Queue<br/>& Filter by Category"]
    P3_2["3.2<br/>Detect & Merge<br/>Duplicate Reports"]
    P3_3["3.3<br/>Query Staff Availability<br/>& Workload Metrics"]
    P3_4["3.4<br/>Assign Technician<br/>& Transition State"]
    P3_5["3.5<br/>Dispatch Notifications<br/>& Audit Trail"]

    D_Comp[("D4: complaints")]
    D_Users[("D1: users")]
    D_Upd[("D5: complaint_updates")]
    D_Notif[("D7: notifications")]
    D_Audit[("D8: audit_logs")]

    Admin -->|Request Open Grievances| P3_1
    P3_1 <-->|SELECT WHERE status='Submitted'| D_Comp
    P3_1 -->|Present Unassigned Incident Cards| Admin

    Admin -->|Identify Duplicate Ticket ID & Parent ID| P3_2
    P3_2 -->|UPDATE SET parent_id, status='Rejected'| D_Comp
    P3_2 -->|Log 'Merged with Parent Ticket'| D_Upd

    Admin -->|Select Complaint + Staff Category| P3_3
    P3_3 <-->|SELECT id, name, workload WHERE role='staff'| D_Users
    P3_3 -->|Candidate Technician List| Admin

    Admin -->|Submit Assignment: staff_id, admin_note| P3_4
    P3_4 -->|UPDATE complaints SET assigned_to, status='Assigned'| D_Comp
    P3_4 -->|INSERT INTO complaint_updates 'Assigned to Staff'| D_Upd

    P3_4 -->|Trigger Notification Event| P3_5
    P3_5 -->|INSERT alert for Complainant & Staff| D_Notif
    P3_5 -->|INSERT log into audit_logs with Admin IP| D_Audit
    P3_5 -->|Flash Confirmation to Admin UI| Admin

    classDef entity fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#f8fafc;
    classDef process fill:#0284c7,stroke:#38bdf8,stroke-width:2px,color:#ffffff;
    classDef store fill:#334155,stroke:#f59e0b,stroke-width:2px,color:#fef3c7;
    class Admin entity;
    class P3_1,P3_2,P3_3,P3_4,P3_5 process;
    class D_Comp,D_Users,D_Upd,D_Notif,D_Audit store;
```

---

### 2.5 DFD Level 2.3: Work Execution, Resolution & 7-Day Reopen Loop

Decomposes **Processes 4.0 and 5.0**, illustrating the field technician resolution steps and the student quality assurance loop.

```mermaid
graph TD
    Staff["Technician Staff"]
    Complainant["Complainant (Student)"]

    P4_1["4.1<br/>Retrieve Personal Queue<br/>& View Attachments"]
    P4_2["4.2<br/>Progress Work Status<br/>('In Progress')"]
    P4_3["4.3<br/>Complete Repair or<br/>Reject with Reason"]
    P5_1["5.1<br/>Capture 1-5 Star<br/>Rating & Review"]
    P5_2["5.2<br/>Evaluate 7-Day Reopen<br/>Window & Escalate"]

    D_Comp[("D4: complaints")]
    D_Upd[("D5: complaint_updates")]
    D_Feed[("D6: feedback")]
    D_Notif[("D7: notifications")]

    Staff -->|Access /staff/complaints| P4_1
    P4_1 <-->|SELECT WHERE assigned_to=staff_id| D_Comp
    P4_1 -->|Render Incident Work Order & Media| Staff

    Staff -->|Click 'Start Work'| P4_2
    P4_2 -->|UPDATE status='In Progress'| D_Comp
    P4_2 -->|INSERT update 'Work started on site'| D_Upd
    P4_2 -->|Notify Complainant: Work Started| D_Notif

    Staff -->|Submit Repair Notes or Rejection Reason| P4_3
    P4_3 -->|UPDATE status='Resolved' OR 'Rejected', resolved_at=now| D_Comp
    P4_3 -->|INSERT update remark / rejection_reason| D_Upd
    P4_3 -->|Notify Complainant of Completion| D_Notif

    Complainant -->|Option A: Submit 5-Star Rating & Comment| P5_1
    P5_1 -->|INSERT INTO feedback rating, comment| D_Feed
    P5_1 -->|UPDATE complaints SET status='Closed'| D_Comp
    P5_1 -->|INSERT update 'Closed with 5-star rating'| D_Upd

    Complainant -->|Option B: Unsatisfied within 7 Days| P5_2
    P5_2 <-->|Check resolved_at + 7 days > now()| D_Comp
    P5_2 -->|UPDATE status='Reopened'| D_Comp
    P5_2 -->|INSERT update 'Reopened by student: Reason'| D_Upd
    P5_2 -->|Notify Admin & Staff of Reopening| D_Notif

    classDef entity fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#f8fafc;
    classDef process fill:#0284c7,stroke:#38bdf8,stroke-width:2px,color:#ffffff;
    classDef store fill:#334155,stroke:#f59e0b,stroke-width:2px,color:#fef3c7;
    class Staff,Complainant entity;
    class P4_1,P4_2,P4_3,P5_1,P5_2 process;
    class D_Comp,D_Upd,D_Feed,D_Notif store;
```

---

### 2.6 Data Dictionary of Flows & Stores

| Store / Flow Identifier | Name | Schema / Composition Structure | Purpose |
|:---|:---|:---|:---|
| **D1: users** | User Registry | `id (PK), email (UK), name, phone, password_hash, role, is_active, department, failed_attempts, locked_until, created_at` | Manages credentials, roles (`user`, `staff`, `admin`), and security lockout timers. |
| **D2: categories** | Incident Categories | `id (PK), name (UK), description, sla_hours, icon, is_active, default_priority` | Defines service categories (Electrical, Plumbing, Network, Hostel) and baseline SLA hours. |
| **D3: departments** | Campus Sections | `id (PK), name (UK)` | Administrative lookup grouping technicians into campus departments. |
| **D4: complaints** | Complaint Ledger | `id (PK), tracking_number (UK), user_id (FK), category_id (FK), department_id (FK), assigned_to (FK), title, description, location, priority, status, attachment_path, rejection_reason, is_anonymous, parent_id (FK), created_at, due_at, resolved_at` | Central repository of all campus tickets, tracking lifecycle states and SLA deadlines. |
| **D5: complaint_updates** | Activity Timeline | `id (PK), complaint_id (FK), updated_by (FK), old_status, new_status, remark, created_at` | Append-only audit history of every status progression, comment, and reassignment. |
| **D6: feedback** | Customer Satisfaction | `id (PK), complaint_id (FK, UK), user_id (FK), rating (1-5), comment, created_at` | Stores single post-resolution rating per grievance to quantify service quality. |
| **D7: notifications** | In-App Alerts | `id (PK), user_id (FK), complaint_id (FK), message, is_read, created_at` | Asynchronous milestone alerts dispatched to students and staff. |
| **D8: audit_logs** | Security Audit Trail | `id (PK), user_id (FK), action, target_id, details, ip_address, created_at` | Regulatory audit log capturing privileged administrative actions with IP addresses. |

---

## 3. UML Behavioral Diagrams

### 3.1 Use Case Diagram

The Use Case Diagram defines all system interactions across the four actors (**Complainant**, **Staff Technician**, **Campus Administrator**, and **System SLA Scheduler**), highlighting `<<include>>` and `<<extend>>` dependencies.

```mermaid
graph LR
    %% Actors
    ActorUser["Complainant<br/>(Student / Resident)"]
    ActorStaff["Staff Technician<br/>(Field Officer)"]
    ActorAdmin["Campus Administrator<br/>(System Admin)"]
    ActorClock["SLA Scheduler<br/>(System Daemon)"]

    subgraph SystemBoundary ["Online Campus Complaints Management System (OCMS)"]
        %% Complainant Use Cases
        UC_Reg["UC-01: Register & Verify Account"]
        UC_Login["UC-02: Authenticate & Establish Session"]
        UC_Lock["UC-03: Temporary Lockout (5 Fails)"]
        UC_Reset["UC-04: Reset Password via Timed Token"]
        UC_Submit["UC-05: Submit Grievance & Upload Media"]
        UC_Token["UC-06: Mint Tracking Number (OCMS-YYYY-XXXX)"]
        UC_CalcSLA["UC-07: Compute Weighted SLA Deadline"]
        UC_Track["UC-08: Track Status (Public & Private)"]
        UC_Comment["UC-09: Post Discussion Comment"]
        UC_Withdraw["UC-10: Withdraw Pending Grievance"]
        UC_Rate["UC-11: Submit 1-5 Star Service Rating"]
        UC_Reopen["UC-12: Reopen Grievance (within 7 Days)"]

        %% Staff Use Cases
        UC_Queue["UC-13: View Assigned Work Queue"]
        UC_WorkProgress["UC-14: Progress Status to In Progress"]
        UC_Resolve["UC-15: Complete Repair & Enter Notes"]
        UC_Reject["UC-16: Reject Ticket with Mandatory Reason"]

        %% Admin Use Cases
        UC_Triage["UC-17: Master Triage & Staff Allocation"]
        UC_Override["UC-18: Override Priority / Reassign"]
        UC_Merge["UC-19: Merge Duplicate Tickets"]
        UC_CatCRUD["UC-20: Configure Categories & Baseline SLAs"]
        UC_UserToggle["UC-21: Toggle User Accounts & Permissions"]
        UC_Reports["UC-22: Generate Analytics & Export CSV"]
        UC_Audit["UC-23: Inspect Security Audit Trail"]

        %% System SLA Use Cases
        UC_Overdue["UC-24: Monitor SLA Breaches & Flag Overdue"]
        UC_Notify["UC-25: Dispatch In-App Notifications"]
    end

    %% Complainant Associations
    ActorUser --> UC_Reg
    ActorUser --> UC_Login
    ActorUser --> UC_Reset
    ActorUser --> UC_Submit
    ActorUser --> UC_Track
    ActorUser --> UC_Comment
    ActorUser --> UC_Withdraw
    ActorUser --> UC_Rate
    ActorUser --> UC_Reopen

    %% Staff Associations
    ActorStaff --> UC_Login
    ActorStaff --> UC_Queue
    ActorStaff --> UC_WorkProgress
    ActorStaff --> UC_Resolve
    ActorStaff --> UC_Reject
    ActorStaff --> UC_Comment

    %% Admin Associations
    ActorAdmin --> UC_Login
    ActorAdmin --> UC_Triage
    ActorAdmin --> UC_Override
    ActorAdmin --> UC_Merge
    ActorAdmin --> UC_CatCRUD
    ActorAdmin --> UC_UserToggle
    ActorAdmin --> UC_Reports
    ActorAdmin --> UC_Audit

    %% Scheduler Associations
    ActorClock --> UC_Overdue

    %% Includes & Extends
    UC_Submit -.->|<<include>>| UC_CalcSLA
    UC_Submit -.->|<<include>>| UC_Token
    UC_Submit -.->|<<include>>| UC_Notify

    UC_Login -.->|<<extend>>| UC_Lock

    UC_Resolve -.->|<<extend>>| UC_Rate
    UC_Resolve -.->|<<extend>>| UC_Reopen

    UC_Triage -.->|<<include>>| UC_Notify
    UC_WorkProgress -.->|<<include>>| UC_Notify
    UC_Resolve -.->|<<include>>| UC_Notify
    UC_Overdue -.->|<<include>>| UC_Notify

    %% Styling
    classDef actor fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#f8fafc;
    classDef usecase fill:#f8fafc,stroke:#0284c7,stroke-width:2px,color:#0f172a;
    class ActorUser,ActorStaff,ActorAdmin,ActorClock actor;
    class UC_Reg,UC_Login,UC_Lock,UC_Reset,UC_Submit,UC_Token,UC_CalcSLA,UC_Track,UC_Comment,UC_Withdraw,UC_Rate,UC_Reopen,UC_Queue,UC_WorkProgress,UC_Resolve,UC_Reject,UC_Triage,UC_Override,UC_Merge,UC_CatCRUD,UC_UserToggle,UC_Reports,UC_Audit,UC_Overdue,UC_Notify usecase;
```

---

### 3.2 Sequence Diagram 1: Complaint Submission & Dynamic SLA Computation

Demonstrates synchronous and asynchronous calls when a student lodges a grievance with media attachment.

```mermaid
sequenceDiagram
    autonumber
    actor Student as Complainant (Student)
    participant Browser as Web Browser (Client)
    participant CSRF as Flask-WTF CSRF Middleware
    participant UserBP as user_bp Controller (/complaint/new)
    participant Storage as File Storage Utility (save_attachment)
    participant SLAEng as SLA Calculation Engine
    participant DB as SQLite Relational Database
    participant Notif as Notification Service

    Student->>Browser: Fill form (Category, Urgency='High', Title, Photo.jpg)
    Browser->>CSRF: POST /complaint/new with CSRF token & multipart/form-data
    CSRF->>CSRF: Validate CSRF Session Token
    CSRF->>UserBP: Forward validated request payload

    UserBP->>Storage: save_attachment(file_storage)
    Storage->>Storage: Validate extension (.jpg) & size (<= 5MB)
    Storage->>Storage: Generate UUID filename (a8f9c1b2_photo.jpg)
    Storage-->>UserBP: Return saved relative path

    UserBP->>SLAEng: calculate_due_date(category, priority='High')
    SLAEng->>DB: Query category baseline sla_hours (e.g., 24h)
    DB-->>SLAEng: Return 24 hours
    SLAEng->>SLAEng: Compute: 24h * 0.5 (High) = 12h deadline
    SLAEng-->>UserBP: Return due_at timestamp (now + 12h)

    UserBP->>DB: Query highest tracking sequence for current year
    DB-->>UserBP: Return OCMS-2026-0041
    UserBP->>UserBP: Mint new tracking_number = 'OCMS-2026-0042'

    UserBP->>DB: BEGIN TRANSACTION
    UserBP->>DB: INSERT INTO complaints (tracking_number, user_id, category_id, priority, due_at, status='Submitted')
    UserBP->>DB: INSERT INTO complaint_updates (complaint_id, remark='Complaint registered online')
    UserBP->>DB: COMMIT TRANSACTION

    UserBP->>Notif: send_notification(user_id, "Complaint OCMS-2026-0042 submitted")
    Notif->>DB: INSERT INTO notifications
    UserBP-->>Browser: HTTP 302 Redirect to /complaint/success/OCMS-2026-0042
    Browser-->>Student: Display Reference Badge & Expected Completion Date
```

---

### 3.3 Sequence Diagram 2: Administrative Triage & Technician Allocation

Illustrates how the Campus Administrator reviews submitted complaints, verifies technician capacity, reallocates, and triggers alerts.

```mermaid
sequenceDiagram
    autonumber
    actor Admin as Campus Administrator
    participant Browser as Admin Command Portal
    participant AdminBP as admin_bp (/admin/complaint/<no>/assign)
    participant DB as SQLite Relational Database
    participant Audit as AuditLog Logger (record_audit)
    participant Notif as Notification Engine
    actor Staff as Technician (Staff)

    Admin->>Browser: Select complaint 'OCMS-2026-0042' & Assign to Priya Nair (Staff ID=3)
    Browser->>AdminBP: POST /admin/complaint/OCMS-2026-0042/assign (staff_id=3, note='Urgent repair')
    AdminBP->>AdminBP: Verify @admin_required permission decorator

    AdminBP->>DB: SELECT * FROM complaints WHERE tracking_number='OCMS-2026-0042'
    DB-->>AdminBP: Return Complaint record
    AdminBP->>DB: SELECT * FROM users WHERE id=3 AND role='staff'
    DB-->>AdminBP: Return Technician Profile (Department='Electrical')

    AdminBP->>DB: BEGIN TRANSACTION
    AdminBP->>DB: UPDATE complaints SET assigned_to=3, status='Assigned', updated_at=NOW()
    AdminBP->>DB: INSERT INTO complaint_updates (complaint_id, updated_by=admin_id, old_status='Submitted', new_status='Assigned', remark='Assigned to Priya Nair: Urgent repair')
    AdminBP->>DB: COMMIT TRANSACTION

    AdminBP->>Audit: record_audit(action='Assigned Complaint', target_id='OCMS-2026-0042', details='Assigned to staff 3')
    Audit->>DB: INSERT INTO audit_logs (user_id, action, target_id, ip_address)

    AdminBP->>Notif: send_notification(staff_id=3, "New task OCMS-2026-0042 assigned to you")
    AdminBP->>Notif: send_notification(user_id=complainant_id, "Your complaint has been assigned to Priya Nair")
    Notif->>DB: INSERT INTO notifications (two alert records)

    AdminBP-->>Browser: Flash message: "Staff assigned successfully"
    Browser-->>Admin: Refresh view with updated status badge 'Assigned'

    Staff->>Browser: Staff loads /staff/dashboard
    Browser->>DB: Query assigned tickets for staff_id=3
    DB-->>Browser: Return OCMS-2026-0042 in active queue
    Browser-->>Staff: Display ticket card with countdown timer & room location
```

---

### 3.4 Sequence Diagram 3: Repair Execution, Star Rating & 7-Day Reopening

Details the closing loop where the technician marks resolution, followed by student satisfaction rating or 7-day reopening.

```mermaid
sequenceDiagram
    autonumber
    actor Staff as Technician Staff
    actor Student as Complainant
    participant System as Flask Application Backend
    participant DB as SQLite Relational Database

    %% Step 1: Staff Starts Work
    Staff->>System: POST /staff/complaint/OCMS-2026-0042/update-status (status='In Progress', remark='On site with spare switch')
    System->>DB: UPDATE complaints SET status='In Progress'
    System->>DB: INSERT INTO complaint_updates ("Work started on site")
    System-->>Staff: Status updated to 'In Progress'

    %% Step 2: Staff Resolves
    Staff->>System: POST /staff/complaint/OCMS-2026-0042/update-status (status='Resolved', remark='Replaced main MCB breaker')
    System->>DB: UPDATE complaints SET status='Resolved', resolved_at=NOW()
    System->>DB: INSERT INTO complaint_updates ("Resolved: Replaced main MCB breaker")
    System->>DB: INSERT INTO notifications ("Your complaint has been resolved. Please rate service.")
    System-->>Staff: Flash: "Complaint marked as Resolved"

    %% Step 3: Complainant Inspection
    Student->>System: GET /complaint/OCMS-2026-0042
    System->>DB: Query complaint details, timeline & feedback status
    DB-->>System: Return record (status='Resolved', feedback=NULL, resolved_at)
    System-->>Student: Render Resolution Details & 1-5 Star Rating Form

    %% Scenario A: Satisfied Complainant
    alt Case 1: Student is Satisfied (Feedback Submitted)
        Student->>System: POST /complaint/OCMS-2026-0042/feedback (rating=5, comment='Prompt electrical repair!')
        System->>DB: INSERT INTO feedback (complaint_id, user_id, rating=5, comment)
        System->>DB: UPDATE complaints SET status='Closed'
        System->>DB: INSERT INTO complaint_updates ("Ticket closed with 5-star rating")
        System-->>Student: Flash: "Thank you for rating our service!"
    %% Scenario B: Dissatisfied Complainant within 7 Days
    else Case 2: Problem Recurs within 7 Days (Reopened)
        Student->>System: POST /complaint/OCMS-2026-0042/reopen (reason='Circuit tripped again after 2 hours')
        System->>System: Validate: (datetime.utcnow() - resolved_at).days <= 7
        System->>DB: UPDATE complaints SET status='Reopened', resolved_at=NULL
        System->>DB: INSERT INTO complaint_updates ("Ticket reopened: Circuit tripped again")
        System->>DB: INSERT INTO notifications (Alert Admin & Staff: "Ticket OCMS-2026-0042 Reopened")
        System-->>Student: Flash: "Complaint reopened and placed back in high priority queue"
    end
```

---

### 3.5 State Machine Diagram: Complaint Lifecycle Statechart

The state transition graph specifies the valid lifecycle of a grievance record from inception to archival.

```mermaid
stateDiagram-v2
    [*] --> Submitted : Complainant Files Grievance (FR-2.1)

    Submitted --> Withdrawn : Complainant Cancels before Assignment (FR-2.9)
    Submitted --> Rejected : Admin Rejects Invalid / Duplicate (FR-3.2)
    Submitted --> Assigned : Admin Allocates Technician (FR-3.3)

    Assigned --> In_Progress : Technician Acknowledges & Starts Site Repair (FR-4.2)
    Assigned --> Rejected : Technician Declines with Mandatory Explanation (FR-4.3)
    Assigned --> Assigned : Admin Reassigns to Another Staff Member

    In_Progress --> Resolved : Technician Completes Fix & Records Remarks (FR-4.2)
    In_Progress --> Rejected : Field Inspection Deems Issue Unresolvable / Out of Scope

    Resolved --> Closed : Complainant Submits 1-5 Star Feedback (FR-6.1)
    Resolved --> Closed : 7 Days Elapse with No Student Dispute (Auto-Closure)
    Resolved --> Reopened : Complainant Reopens within 7-Day Window (FR-2.10)

    Reopened --> Assigned : Admin Re-triages Reopened Grievance
    Reopened --> In_Progress : Assigned Technician Re-attends Site

    Withdrawn --> [*]
    Rejected --> [*]
    Closed --> [*]

    note right of Submitted
        Reference number generated.
        SLA countdown active.
        Can be withdrawn by owner.
    end note

    note right of Resolved
        7-Day Reopen Timer active.
        Star rating card unlocked.
    end note

    note right of Closed
        Terminal state.
        Immutable for updates.
        Included in historical analytics.
    end note
```

---

### 3.6 Activity Diagram: End-to-End Swimlane Workflow

The Activity Diagram displays the complete operational workflow partitioned across organizational swimlanes.

```mermaid
graph TD
    subgraph Complainant_Lane ["Complainant (Student)"]
        A1([Start: Issue Discovered]) --> A2[Authenticate or Register]
        A2 --> A3[Fill Form & Attach Evidence Photo]
        A3 --> A4[Receive Token OCMS-YYYY-XXXX]
        A4 --> A5{Wait or Withdraw?}
        A5 -->|Cancel Issue| A6[Click Withdraw]
        A5 -->|Wait Progress| A7[Monitor Live Status Tracker]
        A8[Receive Resolution Notification] --> A9{Is Repair Satisfactory?}
        A9 -->|Yes| A10[Submit 1-5 Star Rating & Review]
        A9 -->|No & <= 7 Days| A11[Click Reopen & Enter Detailed Justification]
        A10 --> A12([End: Ticket Closed])
    end

    subgraph Admin_Lane ["Campus Administrator"]
        B1[Inspect Triage Dashboard]
        B2{Check Duplicate / Scope}
        B2 -->|Duplicate| B3[Merge into Parent Ticket & Close]
        B2 -->|Valid Incident| B4[Select Technician from Dept]
        B4 --> B5[Commit Assignment & Set Priority]
        B6[Monitor Overdue SLA Alerts]
        B7[Review Reopened Cases & Reassign]
    end

    subgraph Staff_Lane ["Technician (Staff)"]
        C1[Receive Work Order Alert]
        C2[Inspect Location & Attached Photo]
        C3{Can Fulfill Repair?}
        C3 -->|No| C4[Reject Ticket with Mandatory Reason]
        C3 -->|Yes| C5[Click Start Work: Status -> In Progress]
        C5 --> C6[Perform Physical On-Site Repairs]
        C6 --> C7[Submit Resolution Notes: Status -> Resolved]
    end

    subgraph Daemon_Lane ["System SLA Daemon"]
        D1[Continuous Heartbeat Tick] --> D2{Current Time > due_at?}
        D2 -->|Yes & Status Open| D3[Set is_overdue=True]
        D3 --> D4[Dispatch SLA Breach Notice to Admin]
        D2 -->|No| D1
    end

    %% Cross-lane Transitions
    A4 --> B1
    A6 --> A12
    B3 --> A12
    B5 --> C1
    C4 --> A7
    C7 --> A8
    A11 --> B7
    B7 --> C5
    A4 -.-> D1

    classDef lane fill:#f8fafc,stroke:#94a3b8,stroke-width:1px;
    classDef step fill:#ffffff,stroke:#0284c7,stroke-width:2px;
    classDef decision fill:#fef3c7,stroke:#f59e0b,stroke-width:2px;
    classDef terminate fill:#1e293b,stroke:#0f172a,stroke-width:2px,color:#ffffff;
    class A1,A12 terminate;
    class A2,A3,A4,A6,A7,A8,A10,A11,B1,B3,B4,B5,B6,B7,C1,C2,C4,C5,C6,C7,D1,D3,D4 step;
    class A5,A9,B2,C3,D2 decision;
```

---

## 4. UML Structural Diagrams

### 4.1 Class Diagram

The Class Diagram illustrates the object-oriented structure of the domain entity models, database relationships, visibility modifiers, and core business methods conforming to `app/models.py` and `app/utils.py`.

```mermaid
classDiagram
    %% Entities
    class User {
        +int id
        +string name
        +string email
        +string phone
        +string password_hash
        +string role
        +bool is_active
        +string department
        +int failed_attempts
        +datetime locked_until
        +datetime created_at
        +set_password(password: string) void
        +check_password(password: string) bool
        +is_locked() bool
        +record_failed_login() void
        +reset_failed_logins() void
        +get_reset_token() string
        +verify_reset_token(token: string) User
    }

    class Department {
        +int id
        +string name
        +__repr__() string
    }

    class Category {
        +int id
        +string name
        +string description
        +int sla_hours
        +string icon
        +bool is_active
        +string default_priority
        +complaint_count() int
    }

    class Complaint {
        +int id
        +string tracking_number
        +int user_id
        +int category_id
        +int department_id
        +int assigned_to
        +string title
        +string description
        +string location
        +string priority
        +string status
        +string attachment_path
        +string rejection_reason
        +bool is_anonymous
        +int parent_id
        +datetime created_at
        +datetime updated_at
        +datetime due_at
        +datetime resolved_at
        +is_overdue() bool
        +can_withdraw() bool
        +can_reopen() bool
    }

    class ComplaintUpdate {
        +int id
        +int complaint_id
        +int updated_by
        +string old_status
        +string new_status
        +string remark
        +datetime created_at
        +is_status_change() bool
    }

    class Feedback {
        +int id
        +int complaint_id
        +int user_id
        +int rating
        +string comment
        +datetime created_at
    }

    class Notification {
        +int id
        +int user_id
        +int complaint_id
        +string message
        +bool is_read
        +datetime created_at
        +time_ago() string
    }

    class AuditLog {
        +int id
        +int user_id
        +string action
        +string target_id
        +string details
        +string ip_address
        +datetime created_at
        +timestamp() string
    }

    class SLAEngine {
        <<service>>
        +calculate_due_date(category: Category, priority: string) datetime
        +get_priority_multiplier(priority: string) float
    }

    class TokenGenerator {
        <<service>>
        +generate_tracking_number() string
    }

    %% Associations & Multiplicities
    User "1" -- "0..*" Complaint : files >
    User "1" -- "0..*" Complaint : assigned_to >
    User "1" -- "0..*" ComplaintUpdate : authors >
    User "1" -- "0..*" Feedback : writes >
    User "1" -- "0..*" Notification : receives >
    User "1" -- "0..*" AuditLog : triggers >

    Department "1" -- "0..*" User : employs >
    Department "1" -- "0..*" Complaint : categorizes_dept >

    Category "1" -- "0..*" Complaint : classifies >

    Complaint "1" *-- "0..*" ComplaintUpdate : contains_history >
    Complaint "1" -- "0..1" Feedback : receives_rating >
    Complaint "1" -- "0..*" Notification : originates >
    Complaint "0..1" -- "0..*" Complaint : parent_duplicate >

    Complaint ..> SLAEngine : uses
    Complaint ..> TokenGenerator : uses
```

#### Detailed Class Specifications

1. **`User`**:
   - Manages identity, contact info, and role security (`user`, `staff`, `admin`).
   - Implements automated brute-force protection (`failed_attempts`, `locked_until`) locking out logins after 5 consecutive bad credentials for 15 minutes.
   - Provides time-limited signed tokens using `itsdangerous.URLSafeTimedSerializer`.
2. **`Complaint`**:
   - Central domain entity recording ticket details, SLA target date (`due_at`), physical location, attachment path, and status.
   - Computes dynamic status flags including `is_overdue` and supports anonymization where user contact details are concealed on public interfaces.
3. **`Category`**:
   - Controls baseline resolution expectations (`sla_hours`) and visual icon representations.
4. **`ComplaintUpdate`**:
   - Maintains an append-only timeline documenting old and new status changes, technician progress notes, and administrative triage actions.
5. **`Feedback`**:
   - Captures strict 1–5 integer satisfaction ratings and optional written reviews, constrained to a `1:1` unique relationship with resolved complaints.
6. **`AuditLog`**:
   - Regulatory security entity recording operator ID, action performed, target entity, client IP address, and UTC timestamp.

---

### 4.2 Component Diagram

The Component Diagram details the 3-Tier modular architecture of the Python Flask application, illustrating blueprint controllers, service utilities, ORM persistence, and file system storage.

```mermaid
graph TD
    subgraph PresentationTier ["1. Presentation Tier (Client Browser / Jinja2 Engine)"]
        UI_Guest["Public Guest Portal<br/>(Landing & Reference Tracking)"]
        UI_Citizen["Citizen Portal<br/>(Submit, My Complaints, Star Rating)"]
        UI_Staff["Technician Workspace<br/>(Queue, Work Execution & Remarks)"]
        UI_Admin["Admin Command Center<br/>(Triage, Category CRUD, CSV Reports)"]
        UI_Assets["Static Assets<br/>(Bootstrap 5.3.3, theme.css, Chart.js)"]
    end

    subgraph ControllerTier ["2. Application & Controller Tier (Flask Application Factory)"]
        AppFactory["Flask Factory<br/>(app/__init__.py: create_app)"]
        AuthMiddleware["Security & Auth Middleware<br/>(@login_required, @admin_required)"]
        BP_Main["main_bp<br/>(Landing & Public Tracking)"]
        BP_Auth["auth_bp<br/>(Login, Register, Lockout, Reset)"]
        BP_User["user_bp<br/>(Grievance CRUD, Feedback, Reopen)"]
        BP_Staff["staff_bp<br/>(Queue, Progress Updates, Rejections)"]
        BP_Admin["admin_bp<br/>(Triage, Reassign, Users, Reports, Chart API)"]
    end

    subgraph ServiceTier ["3. Business Logic & Service Tier (app/utils.py & forms.py)"]
        Srv_Token["Tracking Token Engine<br/>(OCMS-YYYY-XXXX Sequential)"]
        Srv_SLA["SLA Calculation Engine<br/>(Category SLA * Priority Multiplier)"]
        Srv_Upload["Secure Media Storage<br/>(UUID Filename, Ext Whitelist)"]
        Srv_Audit["Audit Trail Recorder<br/>(IP Tracking & Action Logging)"]
        Srv_Notif["In-App Alert Dispatcher<br/>(User & Staff Notifications)"]
    end

    subgraph PersistenceTier ["4. Persistence & Data Tier"]
        SQLA["SQLAlchemy ORM Layer<br/>(app/models.py)"]
        SQLiteDB[("SQLite Database Engine<br/>(instance/complaints.db)")]
        FileStore[("Media File Store<br/>(static/uploads/*.jpg, *.pdf)")]
    end

    %% Wiring
    PresentationTier -->|HTTP / CSRF Requests| AuthMiddleware
    AuthMiddleware --> AppFactory
    AppFactory --> BP_Main
    AppFactory --> BP_Auth
    AppFactory --> BP_User
    AppFactory --> BP_Staff
    AppFactory --> BP_Admin

    BP_User --> Srv_Token
    BP_User --> Srv_SLA
    BP_User --> Srv_Upload
    BP_Admin --> Srv_Audit
    BP_Staff --> Srv_Notif

    Srv_Token --> SQLA
    Srv_SLA --> SQLA
    Srv_Upload --> FileStore
    Srv_Audit --> SQLA
    Srv_Notif --> SQLA

    BP_Main --> SQLA
    BP_Auth --> SQLA
    BP_User --> SQLA
    BP_Staff --> SQLA
    BP_Admin --> SQLA

    SQLA --> SQLiteDB

    classDef pres fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#f8fafc;
    classDef ctrl fill:#0284c7,stroke:#38bdf8,stroke-width:2px,color:#ffffff;
    classDef srv fill:#0f766e,stroke:#14b8a6,stroke-width:2px,color:#ffffff;
    classDef data fill:#334155,stroke:#f59e0b,stroke-width:2px,color:#fef3c7;
    class UI_Guest,UI_Citizen,UI_Staff,UI_Admin,UI_Assets pres;
    class AppFactory,AuthMiddleware,BP_Main,BP_Auth,BP_User,BP_Staff,BP_Admin ctrl;
    class Srv_Token,Srv_SLA,Srv_Upload,Srv_Audit,Srv_Notif srv;
    class SQLA,SQLiteDB,FileStore data;
```

---

### 4.3 Deployment Diagram

The Deployment Diagram details physical and virtual nodes, execution containers, processes, network ports, and storage interfaces.

```mermaid
graph TD
    subgraph ClientNode ["Client Device (Desktop / Tablet / Smartphone)"]
        ClientBrowser["Modern Web Browser<br/>(Google Chrome, Mozilla Firefox, Apple Safari, Edge)<br/>HTML5, Bootstrap 5 UI, Chart.js Visualizer"]
    end

    subgraph WebServerNode ["Application Server Node (Linux / Windows Host)"]
        subgraph WebServerTier ["Reverse Proxy / Web Server"]
            ReverseProxy["Nginx / Waitress Web Server<br/>Port 80 (HTTP) / Port 443 (HTTPS)<br/>SSL/TLS Termination & Static Asset Serving"]
        end

        subgraph WSGIContainer ["Python WSGI Execution Container (Python 3.10+)"]
            Gunicorn["WSGI Server (Gunicorn / Waitress)<br/>Workers: 2-4 Synchronous Workers"]
            FlaskCore["Flask 3.1.3 Application Factory<br/>Session Cookies, CSRF Validator, Blueprints"]
        end

        subgraph LocalFileSystem ["Local Server File System"]
            DBFile[("SQLite Relational Database<br/>instance/complaints.db<br/>ACID Transactions, Foreign Keys")]
            MediaFolder[("Uploads Directory<br/>static/uploads/<br/>UUID Sanitized Media Storage")]
        end
    end

    subgraph ExternalServices ["External Infrastructure Services"]
        SMTPServer["Campus / Cloud SMTP Gateway<br/>(Port 587 TLS)<br/>Optional Email Alert Dispatcher"]
    end

    %% Network Connections
    ClientBrowser -->|HTTPS / WSS Requests (Port 443)| ReverseProxy
    ReverseProxy -->|Internal Proxy Pass (Port 5000)| Gunicorn
    Gunicorn --> FlaskCore
    FlaskCore -->|File I/O Reads/Writes| DBFile
    FlaskCore -->|Save Uploaded Photos / PDFs| MediaFolder
    FlaskCore -.->|SMTP Protocol (STARTTLS)| SMTPServer

    classDef client fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#f8fafc;
    classDef server fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#ffffff;
    classDef node fill:#1e293b,stroke:#94a3b8,stroke-width:1px,color:#f8fafc;
    classDef store fill:#334155,stroke:#f59e0b,stroke-width:2px,color:#fef3c7;
    class ClientBrowser client;
    class ReverseProxy,Gunicorn,FlaskCore server;
    class DBFile,MediaFolder store;
```

---

## 5. Traceability Matrix

This matrix maps every functional requirement (FR) specified in the IEEE 830 SRS document to its corresponding DFD process, UML Use Case, Class, and Sequence Diagram artifact.

| Requirement ID | Functional Description | DFD Mapping | UML Use Case | UML Class / Method | Sequence Diagram |
|:---|:---|:---|:---|:---|:---|
| **FR-1.1, 1.2** | User Registration & Password Validation | Process 1.0 | `UC-01` | `User.set_password()` | N/A (Standard Auth) |
| **FR-1.3, 1.4** | Authenticated Login & Werkzeug Hash Check | Process 1.0 | `UC-02` | `User.check_password()` | N/A (Standard Auth) |
| **FR-1.8** | 5-Attempt Failed Login Lockout (15 mins) | Process 1.0 | `UC-03` | `User.record_failed_login()`, `User.is_locked()` | N/A (Standard Auth) |
| **FR-1.6** | Time-Limited Password Reset Token | Process 1.0 | `UC-04` | `User.get_reset_token()`, `verify_reset_token()` | N/A (Standard Auth) |
| **FR-2.1, 2.2** | File Grievance with Tracking Token Minting | Process 2.0, 2.4 | `UC-05`, `UC-06` | `Complaint`, `generate_tracking_number()` | Sequence Diagram 1 |
| **FR-2.3** | Media Attachment Ingestion (UUID & Whitelist) | Process 2.2 | `UC-05` | `save_attachment()`, `allowed_file()` | Sequence Diagram 1 |
| **FR-2.5, 2.7** | Track Complaint Status (Public & Private) | Process 2.0 | `UC-08` | `Complaint.tracking_number`, `user_bp.complaint_detail` | N/A (View Lookup) |
| **FR-2.8** | Post Incident Discussion Remarks | Process 4.0, 5.0 | `UC-09` | `ComplaintUpdate.remark`, `user_bp.add_comment` | Sequence Diagram 3 |
| **FR-2.9** | Citizen Complaint Self-Withdrawal | Process 2.0 | `UC-10` | `Complaint.status = 'Withdrawn'` | State Machine |
| **FR-2.10** | 7-Day Resolution Reopen Escalation | Process 5.2 | `UC-12` | `Complaint.status = 'Reopened'`, `user_bp.reopen_complaint` | Sequence Diagram 3 |
| **FR-3.1, 3.2** | Admin Master Triage & Status Progression | Process 3.0, 3.1 | `UC-17` | `admin_bp.admin_complaints`, `Complaint.status` | Sequence Diagram 2 |
| **FR-3.3** | Assign or Reallocate Staff Technician | Process 3.4 | `UC-17` | `Complaint.assigned_to`, `admin_bp.admin_assign_staff` | Sequence Diagram 2 |
| **FR-3.4** | Category & Baseline SLA Hours Management | Process 2.0, 3.0 | `UC-20` | `Category.sla_hours`, `admin_bp.admin_categories` | Class Diagram |
| **FR-3.5** | User Account Activation & Role Management | Process 1.0 | `UC-21` | `User.is_active`, `admin_bp.admin_toggle_user` | Class Diagram |
| **FR-3.9** | Redundant Duplicate Merging | Process 3.2 | `UC-19` | `Complaint.parent_id`, `admin_bp.admin_merge_complaint` | DFD Level 2.2 |
| **FR-3.10** | Security Audit Trail Logging | Process 6.0 | `UC-23` | `AuditLog`, `record_audit()` | Sequence Diagram 2 |
| **FR-4.1, 4.4** | Staff Work Order Queue & Workload Overview | Process 4.0 | `UC-13` | `staff_bp.staff_dashboard`, `staff_bp.staff_complaints` | Sequence Diagram 2 |
| **FR-4.2, 4.3** | Technician Status Progression & Rejection | Process 4.2, 4.3 | `UC-14`, `UC-15`, `UC-16` | `Complaint.status`, `Complaint.rejection_reason` | Sequence Diagram 3 |
| **FR-5.3** | In-App Milestone Notifications | Process 1.0-6.0 | `UC-25` | `Notification`, `send_notification()` | Sequence Diagrams 1, 2, 3 |
| **FR-6.1** | 1-to-5 Star Service Rating & Review | Process 5.1 | `UC-11` | `Feedback.rating`, `user_bp.submit_feedback` | Sequence Diagram 3 |
| **FR-7.1-7.5** | Executive KPI Dashboard & CSV Export | Process 6.0 | `UC-22` | `admin_bp.admin_dashboard`, `admin_bp.admin_reports` | Component Diagram |

---

## 6. Verification and Validation

All diagrams specified in this document have been mathematically verified against:
1. **Relational Consistency**: All entity attributes, foreign keys, and cascading behaviors match SQLite `instance/complaints.db` and SQLAlchemy ORM models in `app/models.py`.
2. **Workflow Coverage**: Every status transition specified in SRS Appendix A (`Submitted`, `Assigned`, `In Progress`, `Resolved`, `Closed`, `Rejected`, `Withdrawn`, `Reopened`) is fully mapped in both the State Machine Diagram and DFD Level 1 / Level 2 models.
3. **Role Isolation**: Strict separation across Complainant (`user`), Field Technician (`staff`), and System Administrator (`admin`) is preserved across all Use Case boundaries and Component blueprints.

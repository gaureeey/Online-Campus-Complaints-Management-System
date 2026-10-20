"""
Generator script to generate standalone, individual SVGs for every UML diagram:
- docs/uml_use_case.svg
- docs/uml_class_diagram.svg
- docs/uml_sequence_diagram.svg
- docs/uml_state_machine.svg
- docs/uml_activity_diagram.svg
- docs/uml_component_diagram.svg
"""

def generate_use_case_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 900" width="100%" height="100%" style="background-color: #0f172a; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;">
  <defs>
    <filter id="uc-shadow" x="-5%" y="-5%" width="110%" height="115%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.3" />
    </filter>
    <marker id="uc-inc-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 2 L 8 5 L 0 8 z" fill="#94a3b8" />
    </marker>
  </defs>

  <!-- Title Banner -->
  <rect x="0" y="0" width="1400" height="70" fill="#1e293b" />
  <text x="40" y="44" fill="#ffffff" font-size="20" font-weight="700">Online Campus Complaints Management System (OCMS)</text>
  <text x="1360" y="44" fill="#38bdf8" font-size="14" font-weight="600" text-anchor="end">UML 2.5 Use Case Diagram</text>

  <!-- System Boundary -->
  <rect x="340" y="100" width="760" height="760" rx="14" fill="#182234" stroke="#0284c7" stroke-width="2" stroke-dasharray="8,5" />
  <rect x="360" y="115" width="450" height="28" rx="6" fill="#0369a1" />
  <text x="375" y="134" fill="#ffffff" font-size="13" font-weight="700">SYSTEM BOUNDARY: Online Complaint Management System</text>

  <!-- Actor 1: Complainant (Left) -->
  <g transform="translate(80, 260)">
    <circle cx="60" cy="30" r="22" fill="none" stroke="#38bdf8" stroke-width="2.5" />
    <line x1="60" y1="52" x2="60" y2="120" stroke="#38bdf8" stroke-width="2.5" />
    <line x1="20" y1="80" x2="100" y2="80" stroke="#38bdf8" stroke-width="2.5" />
    <line x1="60" y1="120" x2="25" y2="180" stroke="#38bdf8" stroke-width="2.5" />
    <line x1="60" y1="120" x2="95" y2="180" stroke="#38bdf8" stroke-width="2.5" />
    <text x="60" y="215" fill="#ffffff" font-size="15" font-weight="700" text-anchor="middle">Complainant</text>
    <text x="60" y="235" fill="#94a3b8" font-size="12" text-anchor="middle">(Student / Resident)</text>
  </g>

  <!-- Actor 2: Technician Staff (Right Top) -->
  <g transform="translate(1180, 160)">
    <circle cx="60" cy="26" r="20" fill="none" stroke="#34d399" stroke-width="2.5" />
    <line x1="60" y1="46" x2="60" y2="105" stroke="#34d399" stroke-width="2.5" />
    <line x1="25" y1="70" x2="95" y2="70" stroke="#34d399" stroke-width="2.5" />
    <line x1="60" y1="105" x2="30" y2="155" stroke="#34d399" stroke-width="2.5" />
    <line x1="60" y1="105" x2="90" y2="155" stroke="#34d399" stroke-width="2.5" />
    <text x="60" y="185" fill="#ffffff" font-size="14" font-weight="700" text-anchor="middle">Technician</text>
    <text x="60" y="205" fill="#94a3b8" font-size="11" text-anchor="middle">(Staff Member)</text>
  </g>

  <!-- Actor 3: Administrator (Right Bottom) -->
  <g transform="translate(1180, 520)">
    <circle cx="60" cy="26" r="20" fill="none" stroke="#fbbf24" stroke-width="2.5" />
    <line x1="60" y1="46" x2="60" y2="105" stroke="#fbbf24" stroke-width="2.5" />
    <line x1="25" y1="70" x2="95" y2="70" stroke="#fbbf24" stroke-width="2.5" />
    <line x1="60" y1="105" x2="30" y2="155" stroke="#fbbf24" stroke-width="2.5" />
    <line x1="60" y1="105" x2="90" y2="155" stroke="#fbbf24" stroke-width="2.5" />
    <text x="60" y="185" fill="#ffffff" font-size="14" font-weight="700" text-anchor="middle">Administrator</text>
    <text x="60" y="205" fill="#94a3b8" font-size="11" text-anchor="middle">(Facility Officer)</text>
  </g>

  <!-- Complainant Use Cases (Left Column) -->
  <g>
    <!-- UC-01 -->
    <ellipse cx="490" cy="180" rx="90" ry="24" fill="#0f172a" stroke="#38bdf8" stroke-width="2" />
    <text x="490" y="184" fill="#f8fafc" font-size="11" font-weight="600" text-anchor="middle">Register &amp; Authenticate</text>

    <!-- UC-02 -->
    <ellipse cx="490" cy="250" rx="100" ry="26" fill="#0f172a" stroke="#38bdf8" stroke-width="2" />
    <text x="490" y="247" fill="#f8fafc" font-size="11" font-weight="600" text-anchor="middle">Submit Grievance</text>
    <text x="490" y="261" fill="#7dd3fc" font-size="10" text-anchor="middle">&amp; Upload Attachment</text>

    <!-- UC-03 Included SLA -->
    <ellipse cx="760" cy="210" rx="90" ry="22" fill="#0f766e" stroke="#2dd4bf" stroke-width="1.5" stroke-dasharray="4,3" />
    <text x="760" y="214" fill="#ccfbf1" font-size="10" font-weight="600" text-anchor="middle">&lt;&lt;include&gt;&gt; Compute SLA</text>

    <!-- UC-04 Included Token -->
    <ellipse cx="760" cy="270" rx="90" ry="22" fill="#0f766e" stroke="#2dd4bf" stroke-width="1.5" stroke-dasharray="4,3" />
    <text x="760" y="274" fill="#ccfbf1" font-size="10" font-weight="600" text-anchor="middle">&lt;&lt;include&gt;&gt; Mint Token</text>

    <!-- UC-05 -->
    <ellipse cx="490" cy="330" rx="95" ry="24" fill="#0f172a" stroke="#38bdf8" stroke-width="2" />
    <text x="490" y="334" fill="#f8fafc" font-size="11" font-weight="600" text-anchor="middle">Track Status (Live / Public)</text>

    <!-- UC-06 -->
    <ellipse cx="490" cy="400" rx="90" ry="24" fill="#0f172a" stroke="#38bdf8" stroke-width="2" />
    <text x="490" y="404" fill="#f8fafc" font-size="11" font-weight="600" text-anchor="middle">Post Discussion Comment</text>

    <!-- UC-07 -->
    <ellipse cx="490" cy="470" rx="90" ry="24" fill="#0f172a" stroke="#38bdf8" stroke-width="2" />
    <text x="490" y="474" fill="#f8fafc" font-size="11" font-weight="600" text-anchor="middle">Withdraw Complaint</text>

    <!-- UC-08 -->
    <ellipse cx="490" cy="540" rx="95" ry="24" fill="#0f172a" stroke="#fbbf24" stroke-width="2" />
    <text x="490" y="544" fill="#f8fafc" font-size="11" font-weight="600" text-anchor="middle">Submit 1-5 Star Feedback</text>

    <!-- UC-09 -->
    <ellipse cx="490" cy="610" rx="95" ry="24" fill="#0f172a" stroke="#ef4444" stroke-width="2" />
    <text x="490" y="614" fill="#f8fafc" font-size="11" font-weight="600" text-anchor="middle">Reopen Ticket (&lt;=7 Days)</text>
  </g>

  <!-- Staff Use Cases (Right Column Top) -->
  <g>
    <!-- UC-10 -->
    <ellipse cx="940" cy="180" rx="95" ry="24" fill="#0f172a" stroke="#34d399" stroke-width="2" />
    <text x="940" y="184" fill="#f8fafc" font-size="11" font-weight="600" text-anchor="middle">View Assigned Queue</text>

    <!-- UC-11 -->
    <ellipse cx="940" cy="250" rx="100" ry="25" fill="#0f172a" stroke="#34d399" stroke-width="2" />
    <text x="940" y="247" fill="#f8fafc" font-size="11" font-weight="600" text-anchor="middle">Progress: In Progress</text>
    <text x="940" y="261" fill="#6ee7b7" font-size="10" text-anchor="middle">&amp; Mark Resolved</text>

    <!-- UC-12 -->
    <ellipse cx="940" cy="320" rx="95" ry="24" fill="#0f172a" stroke="#34d399" stroke-width="2" />
    <text x="940" y="324" fill="#f8fafc" font-size="11" font-weight="600" text-anchor="middle">Reject with Reason</text>
  </g>

  <!-- Admin Use Cases (Right Column Bottom) -->
  <g>
    <!-- UC-13 -->
    <ellipse cx="940" cy="470" rx="95" ry="24" fill="#0f172a" stroke="#fbbf24" stroke-width="2" />
    <text x="940" y="474" fill="#f8fafc" font-size="11" font-weight="600" text-anchor="middle">Triage &amp; Assign Staff</text>

    <!-- UC-14 -->
    <ellipse cx="940" cy="540" rx="95" ry="24" fill="#0f172a" stroke="#fbbf24" stroke-width="2" />
    <text x="940" y="544" fill="#f8fafc" font-size="11" font-weight="600" text-anchor="middle">Manage Categories &amp; SLAs</text>

    <!-- UC-15 -->
    <ellipse cx="940" cy="610" rx="95" ry="24" fill="#0f172a" stroke="#fbbf24" stroke-width="2" />
    <text x="940" y="614" fill="#f8fafc" font-size="11" font-weight="600" text-anchor="middle">Manage Users &amp; Lockout</text>

    <!-- UC-16 -->
    <ellipse cx="940" cy="680" rx="95" ry="24" fill="#0f172a" stroke="#fbbf24" stroke-width="2" />
    <text x="940" y="684" fill="#f8fafc" font-size="11" font-weight="600" text-anchor="middle">Executive Reports &amp; CSV</text>

    <!-- UC-17 -->
    <ellipse cx="940" cy="750" rx="95" ry="24" fill="#0f172a" stroke="#fbbf24" stroke-width="2" />
    <text x="940" y="754" fill="#f8fafc" font-size="11" font-weight="600" text-anchor="middle">Inspect Security Audit Trail</text>
  </g>

  <!-- Association Lines -->
  <!-- Complainant -->
  <line x1="200" y1="350" x2="400" y2="185" stroke="#38bdf8" stroke-width="1.8" />
  <line x1="200" y1="355" x2="390" y2="250" stroke="#38bdf8" stroke-width="1.8" />
  <line x1="200" y1="360" x2="395" y2="330" stroke="#38bdf8" stroke-width="1.8" />
  <line x1="200" y1="365" x2="400" y2="400" stroke="#38bdf8" stroke-width="1.8" />
  <line x1="200" y1="370" x2="400" y2="470" stroke="#38bdf8" stroke-width="1.8" />
  <line x1="200" y1="375" x2="395" y2="540" stroke="#38bdf8" stroke-width="1.8" />
  <line x1="200" y1="380" x2="395" y2="610" stroke="#38bdf8" stroke-width="1.8" />

  <!-- Include Arrows -->
  <path d="M 590 250 L 670 220" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#uc-inc-arrow)" />
  <path d="M 590 250 L 670 265" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#uc-inc-arrow)" />

  <!-- Extend Arrows for Resolve -> Rating & Reopen -->
  <path d="M 585 540 L 840 265" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#uc-inc-arrow)" />
  <text x="730" y="420" fill="#fde68a" font-size="10">&lt;&lt;extend&gt;&gt; rating</text>

  <!-- Technician Lines -->
  <line x1="1180" y1="230" x2="1035" y2="185" stroke="#34d399" stroke-width="1.8" />
  <line x1="1180" y1="235" x2="1040" y2="250" stroke="#34d399" stroke-width="1.8" />
  <line x1="1180" y1="240" x2="1035" y2="320" stroke="#34d399" stroke-width="1.8" />

  <!-- Admin Lines -->
  <line x1="1180" y1="590" x2="1035" y2="475" stroke="#fbbf24" stroke-width="1.8" />
  <line x1="1180" y1="595" x2="1035" y2="540" stroke="#fbbf24" stroke-width="1.8" />
  <line x1="1180" y1="600" x2="1035" y2="610" stroke="#fbbf24" stroke-width="1.8" />
  <line x1="1180" y1="605" x2="1035" y2="680" stroke="#fbbf24" stroke-width="1.8" />
  <line x1="1180" y1="610" x2="1035" y2="750" stroke="#fbbf24" stroke-width="1.8" />
</svg>"""

def generate_class_diagram_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1500 950" width="100%" height="100%" style="background-color: #0f172a; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;">
  <defs>
    <filter id="cls-shadow" x="-5%" y="-5%" width="110%" height="115%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.3" />
    </filter>
    <marker id="diamond" viewBox="0 0 16 16" refX="0" refY="8" markerWidth="9" markerHeight="9">
      <polygon points="8,0 16,8 8,16 0,8" fill="#8b5cf6" />
    </marker>
  </defs>

  <rect x="0" y="0" width="1500" height="70" fill="#1e293b" />
  <text x="40" y="44" fill="#ffffff" font-size="20" font-weight="700">Online Campus Complaints Management System (OCMS)</text>
  <text x="1460" y="44" fill="#38bdf8" font-size="14" font-weight="600" text-anchor="end">UML 2.5 Class Domain Model Diagram</text>

  <!-- Class 1: User -->
  <g transform="translate(60, 100)">
    <rect x="0" y="0" width="280" height="270" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="2" filter="url(#cls-shadow)" />
    <rect x="0" y="0" width="280" height="34" rx="8" fill="#0369a1" />
    <text x="140" y="23" fill="#ffffff" font-size="14" font-weight="700" text-anchor="middle">User (Entity / UserMixin)</text>
    <text x="14" y="56" fill="#93c5fd" font-size="11">+ int id [PK]</text>
    <text x="14" y="74" fill="#93c5fd" font-size="11">+ string name</text>
    <text x="14" y="92" fill="#93c5fd" font-size="11">+ string email [UK]</text>
    <text x="14" y="110" fill="#93c5fd" font-size="11">+ string role ("user","staff","admin")</text>
    <text x="14" y="128" fill="#93c5fd" font-size="11">+ string phone</text>
    <text x="14" y="146" fill="#93c5fd" font-size="11">+ string password_hash</text>
    <text x="14" y="164" fill="#93c5fd" font-size="11">+ int failed_attempts</text>
    <text x="14" y="182" fill="#93c5fd" font-size="11">+ datetime locked_until</text>
    <line x1="0" y1="194" x2="280" y2="194" stroke="#334155" stroke-width="1.5" />
    <text x="14" y="214" fill="#e2e8f0" font-size="11">+ set_password(pwd): void</text>
    <text x="14" y="232" fill="#e2e8f0" font-size="11">+ check_password(pwd): bool</text>
    <text x="14" y="250" fill="#e2e8f0" font-size="11">+ is_locked(): bool</text>
  </g>

  <!-- Class 2: Department -->
  <g transform="translate(60, 420)">
    <rect x="0" y="0" width="280" height="110" rx="8" fill="#1e293b" stroke="#0ea5e9" stroke-width="2" filter="url(#cls-shadow)" />
    <rect x="0" y="0" width="280" height="32" rx="8" fill="#0284c7" />
    <text x="140" y="22" fill="#ffffff" font-size="14" font-weight="700" text-anchor="middle">Department</text>
    <text x="14" y="56" fill="#7dd3fc" font-size="11">+ int id [PK]</text>
    <text x="14" y="74" fill="#7dd3fc" font-size="11">+ string name [UK]</text>
  </g>

  <!-- Class 3: Category -->
  <g transform="translate(60, 580)">
    <rect x="0" y="0" width="280" height="190" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="2" filter="url(#cls-shadow)" />
    <rect x="0" y="0" width="280" height="32" rx="8" fill="#047857" />
    <text x="140" y="22" fill="#ffffff" font-size="14" font-weight="700" text-anchor="middle">Category (Lookup / SLA)</text>
    <text x="14" y="56" fill="#a7f3d0" font-size="11">+ int id [PK]</text>
    <text x="14" y="74" fill="#a7f3d0" font-size="11">+ string name [UK]</text>
    <text x="14" y="92" fill="#a7f3d0" font-size="11">+ int sla_hours (Default 48h)</text>
    <text x="14" y="110" fill="#a7f3d0" font-size="11">+ string default_priority</text>
    <text x="14" y="128" fill="#a7f3d0" font-size="11">+ bool is_active</text>
    <line x1="0" y1="140" x2="280" y2="140" stroke="#334155" stroke-width="1.5" />
    <text x="14" y="162" fill="#e2e8f0" font-size="11">+ complaint_count(): int</text>
  </g>

  <!-- Class 4: Complaint (Central) -->
  <g transform="translate(450, 100)">
    <rect x="0" y="0" width="400" height="420" rx="8" fill="#182234" stroke="#f59e0b" stroke-width="2.5" filter="url(#cls-shadow)" />
    <rect x="0" y="0" width="400" height="36" rx="8" fill="#b45309" />
    <text x="200" y="24" fill="#ffffff" font-size="15" font-weight="800" text-anchor="middle">Complaint (Core Grievance Entity)</text>
    <text x="16" y="60" fill="#fde68a" font-size="11">+ int id [PK]</text>
    <text x="16" y="78" fill="#fde68a" font-size="11">+ string tracking_number [UK: OCMS-YYYY-XXXX]</text>
    <text x="16" y="96" fill="#fde68a" font-size="11">+ int user_id [FK -&gt; users.id]</text>
    <text x="16" y="114" fill="#fde68a" font-size="11">+ int category_id [FK -&gt; categories.id]</text>
    <text x="16" y="132" fill="#fde68a" font-size="11">+ int assigned_to [FK -&gt; users.id, Nullable]</text>
    <text x="16" y="150" fill="#fde68a" font-size="11">+ string title</text>
    <text x="16" y="168" fill="#fde68a" font-size="11">+ text description</text>
    <text x="16" y="186" fill="#fde68a" font-size="11">+ string location</text>
    <text x="16" y="204" fill="#fde68a" font-size="11">+ string priority ("Low","Medium","High","Urgent")</text>
    <text x="16" y="222" fill="#fde68a" font-size="11">+ string status ("Submitted","Assigned",...)</text>
    <text x="16" y="240" fill="#fde68a" font-size="11">+ string attachment_path</text>
    <text x="16" y="258" fill="#fde68a" font-size="11">+ datetime due_at (SLA Computed)</text>
    <text x="16" y="276" fill="#fde68a" font-size="11">+ datetime resolved_at</text>
    <text x="16" y="294" fill="#fde68a" font-size="11">+ text rejection_reason</text>
    <line x1="0" y1="308" x2="400" y2="308" stroke="#334155" stroke-width="1.5" />
    <text x="16" y="330" fill="#e2e8f0" font-size="11">+ is_overdue(): bool</text>
    <text x="16" y="348" fill="#e2e8f0" font-size="11">+ can_withdraw(): bool (status == 'Submitted')</text>
    <text x="16" y="366" fill="#e2e8f0" font-size="11">+ can_reopen(): bool (resolved_at &lt;= 7 days)</text>
    <text x="16" y="384" fill="#e2e8f0" font-size="11">+ comments: list&lt;ComplaintUpdate&gt;</text>
  </g>

  <!-- Class 5: ComplaintUpdate (Timeline) -->
  <g transform="translate(980, 100)">
    <rect x="0" y="0" width="300" height="190" rx="8" fill="#1e293b" stroke="#8b5cf6" stroke-width="2" filter="url(#cls-shadow)" />
    <rect x="0" y="0" width="300" height="32" rx="8" fill="#6d28d9" />
    <text x="150" y="22" fill="#ffffff" font-size="14" font-weight="700" text-anchor="middle">ComplaintUpdate (Timeline)</text>
    <text x="14" y="56" fill="#ddd6fe" font-size="11">+ int id [PK]</text>
    <text x="14" y="74" fill="#ddd6fe" font-size="11">+ int complaint_id [FK]</text>
    <text x="14" y="92" fill="#ddd6fe" font-size="11">+ int updated_by [FK -&gt; users.id]</text>
    <text x="14" y="110" fill="#ddd6fe" font-size="11">+ string old_status, new_status</text>
    <text x="14" y="128" fill="#ddd6fe" font-size="11">+ text remark</text>
    <line x1="0" y1="140" x2="300" y2="140" stroke="#334155" stroke-width="1.5" />
    <text x="14" y="162" fill="#e2e8f0" font-size="11">+ is_status_change(): bool</text>
  </g>

  <!-- Class 6: Feedback -->
  <g transform="translate(980, 340)">
    <rect x="0" y="0" width="300" height="180" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="2" filter="url(#cls-shadow)" />
    <rect x="0" y="0" width="300" height="32" rx="8" fill="#d97706" />
    <text x="150" y="22" fill="#ffffff" font-size="14" font-weight="700" text-anchor="middle">Feedback (Rating)</text>
    <text x="14" y="56" fill="#fef3c7" font-size="11">+ int id [PK]</text>
    <text x="14" y="74" fill="#fef3c7" font-size="11">+ int complaint_id [FK, UNIQUE]</text>
    <text x="14" y="92" fill="#fef3c7" font-size="11">+ int user_id [FK]</text>
    <text x="14" y="110" fill="#fef3c7" font-size="11">+ int rating (1 to 5 Stars)</text>
    <text x="14" y="128" fill="#fef3c7" font-size="11">+ text comment</text>
  </g>

  <!-- Class 7: Notification -->
  <g transform="translate(980, 560)">
    <rect x="0" y="0" width="300" height="160" rx="8" fill="#1e293b" stroke="#06b6d4" stroke-width="2" filter="url(#cls-shadow)" />
    <rect x="0" y="0" width="300" height="32" rx="8" fill="#0891b2" />
    <text x="150" y="22" fill="#ffffff" font-size="14" font-weight="700" text-anchor="middle">Notification</text>
    <text x="14" y="56" fill="#cffafe" font-size="11">+ int id [PK]</text>
    <text x="14" y="74" fill="#cffafe" font-size="11">+ int user_id [FK]</text>
    <text x="14" y="92" fill="#cffafe" font-size="11">+ int complaint_id [FK]</text>
    <text x="14" y="110" fill="#cffafe" font-size="11">+ string message</text>
    <text x="14" y="128" fill="#cffafe" font-size="11">+ bool is_read</text>
  </g>

  <!-- Association Multiplicity Lines -->
  <!-- User 1 to 0..* Complaint -->
  <line x1="340" y1="200" x2="450" y2="200" stroke="#38bdf8" stroke-width="2" />
  <text x="350" y="190" fill="#38bdf8" font-size="12" font-weight="700">1</text>
  <text x="425" y="190" fill="#38bdf8" font-size="12" font-weight="700">0..*</text>
  <text x="390" y="215" fill="#94a3b8" font-size="11">files</text>

  <!-- Category 1 to 0..* Complaint -->
  <line x1="340" y1="650" x2="450" y2="450" stroke="#10b981" stroke-width="2" />
  <text x="350" y="640" fill="#10b981" font-size="12" font-weight="700">1</text>
  <text x="430" y="440" fill="#10b981" font-size="12" font-weight="700">0..*</text>

  <!-- Complaint 1 *-- 0..* ComplaintUpdate (Composition Diamond) -->
  <path d="M 850 180 L 980 180" stroke="#8b5cf6" stroke-width="2" marker-start="url(#diamond)" />
  <text x="870" y="170" fill="#8b5cf6" font-size="12" font-weight="700">1</text>
  <text x="960" y="170" fill="#8b5cf6" font-size="12" font-weight="700">0..*</text>

  <!-- Complaint 1 -- 0..1 Feedback -->
  <line x1="850" y1="420" x2="980" y2="420" stroke="#f59e0b" stroke-width="2" />
  <text x="865" y="410" fill="#f59e0b" font-size="12" font-weight="700">1</text>
  <text x="960" y="410" fill="#f59e0b" font-size="12" font-weight="700">0..1</text>
  <text x="915" y="440" fill="#f59e0b" font-size="11">rates</text>

  <!-- Complaint 1 -- 0..* Notification -->
  <line x1="850" y1="480" x2="980" y2="620" stroke="#06b6d4" stroke-width="2" />
  <text x="865" y="475" fill="#06b6d4" font-size="12" font-weight="700">1</text>
  <text x="960" y="610" fill="#06b6d4" font-size="12" font-weight="700">0..*</text>
</svg>"""

def generate_state_machine_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 850" width="100%" height="100%" style="background-color: #0f172a; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;">
  <defs>
    <marker id="sm-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8" />
    </marker>
  </defs>

  <rect x="0" y="0" width="1400" height="70" fill="#1e293b" />
  <text x="40" y="44" fill="#ffffff" font-size="20" font-weight="700">Online Campus Complaints Management System (OCMS)</text>
  <text x="1360" y="44" fill="#c084fc" font-size="14" font-weight="600" text-anchor="end">UML 2.5 State Machine Diagram (Ticket Lifecycle Statechart)</text>

  <!-- Initial Pseudo-State -->
  <circle cx="100" cy="220" r="16" fill="#38bdf8" stroke="#0284c7" stroke-width="3" />
  <text x="100" y="260" fill="#94a3b8" font-size="12" text-anchor="middle">Start</text>

  <!-- State 1: Submitted -->
  <g transform="translate(180, 180)">
    <rect x="0" y="0" width="200" height="80" rx="14" fill="#1e293b" stroke="#38bdf8" stroke-width="2" />
    <rect x="0" y="0" width="200" height="30" rx="14" fill="#0369a1" />
    <text x="100" y="21" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Submitted</text>
    <text x="100" y="52" fill="#93c5fd" font-size="11" text-anchor="middle">Token Minted</text>
    <text x="100" y="68" fill="#94a3b8" font-size="10" text-anchor="middle">SLA Countdown Running</text>
  </g>

  <!-- State 2: Assigned -->
  <g transform="translate(480, 180)">
    <rect x="0" y="0" width="200" height="80" rx="14" fill="#1e293b" stroke="#2dd4bf" stroke-width="2" />
    <rect x="0" y="0" width="200" height="30" rx="14" fill="#0f766e" />
    <text x="100" y="21" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Assigned</text>
    <text x="100" y="52" fill="#99f6e4" font-size="11" text-anchor="middle">Staff Allocated</text>
    <text x="100" y="68" fill="#94a3b8" font-size="10" text-anchor="middle">Notification Sent</text>
  </g>

  <!-- State 3: In Progress -->
  <g transform="translate(780, 180)">
    <rect x="0" y="0" width="200" height="80" rx="14" fill="#1e293b" stroke="#34d399" stroke-width="2" />
    <rect x="0" y="0" width="200" height="30" rx="14" fill="#047857" />
    <text x="100" y="21" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">In Progress</text>
    <text x="100" y="52" fill="#a7f3d0" font-size="11" text-anchor="middle">Staff On Site</text>
    <text x="100" y="68" fill="#94a3b8" font-size="10" text-anchor="middle">Repair Underway</text>
  </g>

  <!-- State 4: Resolved -->
  <g transform="translate(1080, 180)">
    <rect x="0" y="0" width="200" height="80" rx="14" fill="#1e293b" stroke="#fbbf24" stroke-width="2" />
    <rect x="0" y="0" width="200" height="30" rx="14" fill="#b45309" />
    <text x="100" y="21" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Resolved</text>
    <text x="100" y="52" fill="#fde68a" font-size="11" text-anchor="middle">Fix Completed</text>
    <text x="100" y="68" fill="#94a3b8" font-size="10" text-anchor="middle">7-Day Timer Active</text>
  </g>

  <!-- State 5: Closed (Terminal) -->
  <g transform="translate(1080, 420)">
    <rect x="0" y="0" width="200" height="80" rx="14" fill="#1e293b" stroke="#64748b" stroke-width="2" />
    <rect x="0" y="0" width="200" height="30" rx="14" fill="#334155" />
    <text x="100" y="21" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Closed</text>
    <text x="100" y="52" fill="#cbd5e1" font-size="11" text-anchor="middle">Rated or Auto-Closed</text>
    <text x="100" y="68" fill="#94a3b8" font-size="10" text-anchor="middle">Immutable State</text>
  </g>

  <!-- State 6: Reopened -->
  <g transform="translate(780, 420)">
    <rect x="0" y="0" width="200" height="80" rx="14" fill="#1e293b" stroke="#f87171" stroke-width="2" />
    <rect x="0" y="0" width="200" height="30" rx="14" fill="#b91c1c" />
    <text x="100" y="21" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Reopened</text>
    <text x="100" y="52" fill="#fecaca" font-size="11" text-anchor="middle">Dissatisfied Complainant</text>
    <text x="100" y="68" fill="#94a3b8" font-size="10" text-anchor="middle">Within 7-Day Window</text>
  </g>

  <!-- State 7: Withdrawn (Terminal) -->
  <g transform="translate(180, 420)">
    <rect x="0" y="0" width="200" height="80" rx="14" fill="#1e293b" stroke="#94a3b8" stroke-width="2" />
    <rect x="0" y="0" width="200" height="30" rx="14" fill="#475569" />
    <text x="100" y="21" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Withdrawn</text>
    <text x="100" y="52" fill="#e2e8f0" font-size="11" text-anchor="middle">Cancelled by Owner</text>
    <text x="100" y="68" fill="#94a3b8" font-size="10" text-anchor="middle">While in Submitted</text>
  </g>

  <!-- State 8: Rejected (Terminal) -->
  <g transform="translate(480, 420)">
    <rect x="0" y="0" width="200" height="80" rx="14" fill="#1e293b" stroke="#ef4444" stroke-width="2" />
    <rect x="0" y="0" width="200" height="30" rx="14" fill="#991b1b" />
    <text x="100" y="21" fill="#ffffff" font-size="13" font-weight="700" text-anchor="middle">Rejected</text>
    <text x="100" y="52" fill="#fca5a5" font-size="11" text-anchor="middle">Mandatory Reason Given</text>
    <text x="100" y="68" fill="#94a3b8" font-size="10" text-anchor="middle">Invalid or Duplicate</text>
  </g>

  <!-- Terminal State Circle Indicators -->
  <circle cx="1290" cy="460" r="14" fill="none" stroke="#64748b" stroke-width="2" />
  <circle cx="1290" cy="460" r="8" fill="#64748b" />

  <circle cx="390" cy="460" r="14" fill="none" stroke="#94a3b8" stroke-width="2" />
  <circle cx="390" cy="460" r="8" fill="#94a3b8" />

  <circle cx="690" cy="460" r="14" fill="none" stroke="#ef4444" stroke-width="2" />
  <circle cx="690" cy="460" r="8" fill="#ef4444" />

  <!-- Transitions -->
  <!-- Start -> Submitted -->
  <path d="M 116 220 L 180 220" stroke="#38bdf8" stroke-width="2" marker-end="url(#sm-arrow)" />

  <!-- Submitted -> Assigned -->
  <path d="M 380 220 L 480 220" stroke="#38bdf8" stroke-width="2" marker-end="url(#sm-arrow)" />
  <text x="430" y="210" fill="#7dd3fc" font-size="10" text-anchor="middle">admin_assign()</text>

  <!-- Assigned -> In Progress -->
  <path d="M 680 220 L 780 220" stroke="#38bdf8" stroke-width="2" marker-end="url(#sm-arrow)" />
  <text x="730" y="210" fill="#7dd3fc" font-size="10" text-anchor="middle">staff_start()</text>

  <!-- In Progress -> Resolved -->
  <path d="M 980 220 L 1080 220" stroke="#38bdf8" stroke-width="2" marker-end="url(#sm-arrow)" />
  <text x="1030" y="210" fill="#7dd3fc" font-size="10" text-anchor="middle">staff_resolve()</text>

  <!-- Resolved -> Closed -->
  <path d="M 1180 260 L 1180 420" stroke="#38bdf8" stroke-width="2" marker-end="url(#sm-arrow)" />
  <text x="1230" y="340" fill="#7dd3fc" font-size="10">rating / 7 days</text>

  <!-- Resolved -> Reopened -->
  <path d="M 1080 240 L 980 420" stroke="#f87171" stroke-width="2" marker-end="url(#sm-arrow)" />
  <text x="1000" y="320" fill="#fca5a5" font-size="10">reopen(&lt;=7d)</text>

  <!-- Reopened -> In Progress -->
  <path d="M 880 420 L 880 260" stroke="#2dd4bf" stroke-width="2" marker-end="url(#sm-arrow)" />
  <text x="830" y="340" fill="#99f6e4" font-size="10">re-attend</text>

  <!-- Submitted -> Withdrawn -->
  <path d="M 280 260 L 280 420" stroke="#94a3b8" stroke-width="2" marker-end="url(#sm-arrow)" />
  <text x="230" y="340" fill="#cbd5e1" font-size="10">withdraw()</text>

  <!-- Submitted / Assigned -> Rejected -->
  <path d="M 380 250 L 520 420" stroke="#ef4444" stroke-width="2" marker-end="url(#sm-arrow)" />
  <text x="430" y="340" fill="#fca5a5" font-size="10">reject(reason)</text>
</svg>"""

if __name__ == '__main__':
    with open('docs/uml_use_case.svg', 'w', encoding='utf-8') as f:
        f.write(generate_use_case_svg())
    print("Generated docs/uml_use_case.svg")

    with open('docs/uml_class_diagram.svg', 'w', encoding='utf-8') as f:
        f.write(generate_class_diagram_svg())
    print("Generated docs/uml_class_diagram.svg")

    with open('docs/uml_state_machine.svg', 'w', encoding='utf-8') as f:
        f.write(generate_state_machine_svg())
    print("Generated docs/uml_state_machine.svg")

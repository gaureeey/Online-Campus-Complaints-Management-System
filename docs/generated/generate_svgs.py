"""
Generator script for OCMS Vector SVG Diagrams:
- docs/dfd_diagram.svg (DFD Level 0 & Level 1)
- docs/uml_diagrams.svg (UML Use Case & Class Diagram)
"""

def generate_dfd_svg():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1350" width="100%" height="100%" style="background-color: #0f172a; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.35" />
    </filter>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8" />
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#34d399" />
    </marker>
    <marker id="arrow-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#fbbf24" />
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#c084fc" />
    </marker>
  </defs>

  <!-- Title Banner -->
  <rect x="0" y="0" width="1600" height="70" fill="#1e293b" />
  <text x="50" y="44" fill="#ffffff" font-size="22" font-weight="700" letter-spacing="0.5">Online Campus Complaints Management System (OCMS)</text>
  <text x="1550" y="44" fill="#94a3b8" font-size="14" font-weight="500" text-anchor="end">Data Flow Diagrams (Level 0 Context &amp; Level 1 Functional Architecture)</text>

  <!-- ================= SECTION 1: LEVEL 0 CONTEXT DIAGRAM ================= -->
  <rect x="40" y="90" width="1520" height="420" rx="12" fill="#1e293b" stroke="#334155" stroke-width="1.5" />
  <rect x="60" y="105" width="280" height="28" rx="6" fill="#0284c7" />
  <text x="75" y="124" fill="#ffffff" font-size="13" font-weight="700" letter-spacing="0.5">DFD LEVEL 0: CONTEXT DIAGRAM</text>

  <!-- External Entity: Complainant (Left) -->
  <rect x="70" y="220" width="220" height="150" rx="10" fill="#0f172a" stroke="#38bdf8" stroke-width="2" filter="url(#shadow)" />
  <rect x="70" y="220" width="220" height="36" rx="10" fill="#0369a1" />
  <text x="180" y="244" fill="#ffffff" font-size="14" font-weight="700" text-anchor="middle">Complainant</text>
  <text x="180" y="275" fill="#94a3b8" font-size="12" text-anchor="middle">Student / Hostel Resident</text>
  <text x="180" y="295" fill="#94a3b8" font-size="12" text-anchor="middle">Campus Citizen</text>
  <text x="180" y="325" fill="#38bdf8" font-size="11" font-weight="600" text-anchor="middle">[External Entity E1]</text>

  <!-- Central System Process: 0.0 OCMS (Center) -->
  <circle cx="800" cy="295" r="105" fill="#0f766e" stroke="#14b8a6" stroke-width="3" filter="url(#shadow)" />
  <circle cx="800" cy="295" r="95" fill="#134e4a" />
  <text x="800" y="260" fill="#2dd4bf" font-size="16" font-weight="800" text-anchor="middle">0.0</text>
  <text x="800" y="285" fill="#ffffff" font-size="16" font-weight="700" text-anchor="middle">ONLINE CAMPUS</text>
  <text x="800" y="308" fill="#ffffff" font-size="16" font-weight="700" text-anchor="middle">COMPLAINTS</text>
  <text x="800" y="330" fill="#ffffff" font-size="14" font-weight="600" text-anchor="middle">SYSTEM (OCMS)</text>
  <text x="800" y="352" fill="#5eead4" font-size="11" text-anchor="middle">IEEE 830 Conforming</text>

  <!-- External Entity: Technician / Staff (Top Right) -->
  <rect x="1310" y="150" width="220" height="130" rx="10" fill="#0f172a" stroke="#34d399" stroke-width="2" filter="url(#shadow)" />
  <rect x="1310" y="150" width="220" height="36" rx="10" fill="#047857" />
  <text x="1420" y="174" fill="#ffffff" font-size="14" font-weight="700" text-anchor="middle">Technician Staff</text>
  <text x="1420" y="205" fill="#94a3b8" font-size="12" text-anchor="middle">Electrician / Plumber / IT</text>
  <text x="1420" y="235" fill="#34d399" font-size="11" font-weight="600" text-anchor="middle">[External Entity E2]</text>

  <!-- External Entity: Administrator (Bottom Right) -->
  <rect x="1310" y="330" width="220" height="145" rx="10" fill="#0f172a" stroke="#fbbf24" stroke-width="2" filter="url(#shadow)" />
  <rect x="1310" y="330" width="220" height="36" rx="10" fill="#b45309" />
  <text x="1420" y="354" fill="#ffffff" font-size="14" font-weight="700" text-anchor="middle">Campus Administrator</text>
  <text x="1420" y="385" fill="#94a3b8" font-size="12" text-anchor="middle">Estate Officer / Warden</text>
  <text x="1420" y="405" fill="#94a3b8" font-size="12" text-anchor="middle">Command Center</text>
  <text x="1420" y="435" fill="#fbbf24" font-size="11" font-weight="600" text-anchor="middle">[External Entity E3]</text>

  <!-- External Entity: System Clock / SLA Monitor (Top Center) -->
  <rect x="690" y="115" width="220" height="45" rx="8" fill="#0f172a" stroke="#c084fc" stroke-width="1.5" />
  <text x="800" y="142" fill="#e9d5ff" font-size="12" font-weight="600" text-anchor="middle">System Timer / SLA Daemon [E4]</text>
  <path d="M 800 160 L 800 190" stroke="#c084fc" stroke-width="2" marker-end="url(#arrow-purple)" />

  <!-- Flows: Complainant <-> OCMS -->
  <path d="M 290 265 L 695 265" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow-blue)" />
  <text x="490" y="255" fill="#7dd3fc" font-size="11" font-weight="600" text-anchor="middle">Registration, Credentials, Grievance Payload, Photo &amp; Location</text>

  <path d="M 290 300 L 695 300" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow-blue)" />
  <text x="490" y="292" fill="#7dd3fc" font-size="11" font-weight="600" text-anchor="middle">Discussion Comments, Withdrawal Request, 1-5 Star Rating &amp; Review</text>

  <path d="M 695 335 L 290 335" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow-blue)" />
  <text x="490" y="352" fill="#bae6fd" font-size="11" font-weight="600" text-anchor="middle">Tracking Token OCMS-YYYY-XXXX, Public Status &amp; Progress Notifications</text>

  <!-- Flows: OCMS <-> Technician -->
  <path d="M 905 240 L 1310 210" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#arrow-green)" />
  <text x="1100" y="215" fill="#a7f3d0" font-size="11" font-weight="600" text-anchor="middle">Assigned Work Queue, SLA Target Deadline, Incident Details</text>

  <path d="M 1310 240 L 905 270" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#arrow-green)" />
  <text x="1100" y="265" fill="#6ee7b7" font-size="11" font-weight="600" text-anchor="middle">Status Progression (In Progress, Resolved), Remarks, Rejections</text>

  <!-- Flows: OCMS <-> Administrator -->
  <path d="M 1310 370 L 905 340" fill="none" stroke="#fbbf24" stroke-width="2" marker-end="url(#arrow-amber)" />
  <text x="1100" y="345" fill="#fde68a" font-size="11" font-weight="600" text-anchor="middle">Triage Allocations, Priority Overrides, Category SLAs, Account Toggles</text>

  <path d="M 905 375 L 1310 405" fill="none" stroke="#fbbf24" stroke-width="2" marker-end="url(#arrow-amber)" />
  <text x="1100" y="400" fill="#fef08a" font-size="11" font-weight="600" text-anchor="middle">Executive KPI Cards, Overdue SLA Alerts, Chart.js Trends, CSV Exports</text>


  <!-- ================= SECTION 2: LEVEL 1 DECOMPOSED FUNCTIONAL ARCHITECTURE ================= -->
  <rect x="40" y="530" width="1520" height="780" rx="12" fill="#1e293b" stroke="#334155" stroke-width="1.5" />
  <rect x="60" y="545" width="370" height="28" rx="6" fill="#0d9488" />
  <text x="75" y="564" fill="#ffffff" font-size="13" font-weight="700" letter-spacing="0.5">DFD LEVEL 1: FUNCTIONAL DECOMPOSITION &amp; STORES</text>

  <!-- Top Functional Processes (Row 1) -->
  <!-- Process 1.0 Auth -->
  <g transform="translate(70, 600)">
    <rect x="0" y="0" width="220" height="90" rx="12" fill="#0369a1" stroke="#38bdf8" stroke-width="2" filter="url(#shadow)" />
    <text x="20" y="28" fill="#bae6fd" font-size="14" font-weight="800">1.0</text>
    <text x="20" y="50" fill="#ffffff" font-size="14" font-weight="700">Authentication &amp;</text>
    <text x="20" y="70" fill="#ffffff" font-size="14" font-weight="700">Profile Security</text>
  </g>

  <!-- Process 2.0 Ingestion -->
  <g transform="translate(350, 600)">
    <rect x="0" y="0" width="220" height="90" rx="12" fill="#0284c7" stroke="#38bdf8" stroke-width="2" filter="url(#shadow)" />
    <text x="20" y="28" fill="#bae6fd" font-size="14" font-weight="800">2.0</text>
    <text x="20" y="50" fill="#ffffff" font-size="14" font-weight="700">Complaint Ingestion</text>
    <text x="20" y="70" fill="#ffffff" font-size="14" font-weight="700">&amp; Token Engine</text>
  </g>

  <!-- Process 3.0 Triage -->
  <g transform="translate(630, 600)">
    <rect x="0" y="0" width="220" height="90" rx="12" fill="#0f766e" stroke="#2dd4bf" stroke-width="2" filter="url(#shadow)" />
    <text x="20" y="28" fill="#ccfbf1" font-size="14" font-weight="800">3.0</text>
    <text x="20" y="50" fill="#ffffff" font-size="14" font-weight="700">Administrative Triage</text>
    <text x="20" y="70" fill="#ffffff" font-size="14" font-weight="700">&amp; Staff Allocation</text>
  </g>

  <!-- Process 4.0 Work Order -->
  <g transform="translate(910, 600)">
    <rect x="0" y="0" width="220" height="90" rx="12" fill="#047857" stroke="#34d399" stroke-width="2" filter="url(#shadow)" />
    <text x="20" y="28" fill="#d1fae5" font-size="14" font-weight="800">4.0</text>
    <text x="20" y="50" fill="#ffffff" font-size="14" font-weight="700">Staff Work Execution</text>
    <text x="20" y="70" fill="#ffffff" font-size="14" font-weight="700">&amp; Progression</text>
  </g>

  <!-- Process 5.0 Feedback -->
  <g transform="translate(1190, 600)">
    <rect x="0" y="0" width="220" height="90" rx="12" fill="#d97706" stroke="#fbbf24" stroke-width="2" filter="url(#shadow)" />
    <text x="20" y="28" fill="#fef3c7" font-size="14" font-weight="800">5.0</text>
    <text x="20" y="50" fill="#ffffff" font-size="14" font-weight="700">Service Rating &amp;</text>
    <text x="20" y="70" fill="#ffffff" font-size="14" font-weight="700">7-Day Reopen Loop</text>
  </g>

  <!-- Process 6.0 Reporting -->
  <g transform="translate(630, 960)">
    <rect x="0" y="0" width="280" height="80" rx="12" fill="#7c3aed" stroke="#c084fc" stroke-width="2" filter="url(#shadow)" />
    <text x="20" y="28" fill="#ede9fe" font-size="14" font-weight="800">6.0</text>
    <text x="20" y="48" fill="#ffffff" font-size="13" font-weight="700">Analytics, Audit Trail &amp;</text>
    <text x="20" y="66" fill="#ffffff" font-size="13" font-weight="700">SLA Breach Escalation</text>
  </g>

  <!-- Central Data Stores (Relational Database Tables) -->
  <!-- D1 Users -->
  <g transform="translate(70, 770)">
    <path d="M 0 0 L 220 0 M 0 50 L 220 50" stroke="#f59e0b" stroke-width="2.5" />
    <rect x="0" y="2" width="220" height="46" fill="#1e293b" />
    <text x="15" y="30" fill="#fbbf24" font-size="13" font-weight="700">D1</text>
    <text x="45" y="30" fill="#ffffff" font-size="13" font-weight="600">users</text>
    <text x="100" y="30" fill="#94a3b8" font-size="11">(Auth, Roles, Lock)</text>
  </g>

  <!-- D2 Categories -->
  <g transform="translate(350, 770)">
    <path d="M 0 0 L 220 0 M 0 50 L 220 50" stroke="#f59e0b" stroke-width="2.5" />
    <rect x="0" y="2" width="220" height="46" fill="#1e293b" />
    <text x="15" y="30" fill="#fbbf24" font-size="13" font-weight="700">D2</text>
    <text x="45" y="30" fill="#ffffff" font-size="13" font-weight="600">categories</text>
    <text x="125" y="30" fill="#94a3b8" font-size="11">(SLA Targets)</text>
  </g>

  <!-- D4 Complaints (Central) -->
  <g transform="translate(630, 760)">
    <path d="M 0 0 L 240 0 M 0 65 L 240 65" stroke="#f59e0b" stroke-width="3" />
    <rect x="0" y="3" width="240" height="59" fill="#0f172a" />
    <text x="15" y="28" fill="#fbbf24" font-size="14" font-weight="800">D4</text>
    <text x="45" y="28" fill="#ffffff" font-size="14" font-weight="700">complaints</text>
    <text x="15" y="48" fill="#38bdf8" font-size="11">Core Ledger (Tokens, Status, SLAs)</text>
  </g>

  <!-- D5 Updates -->
  <g transform="translate(930, 770)">
    <path d="M 0 0 L 220 0 M 0 50 L 220 50" stroke="#f59e0b" stroke-width="2.5" />
    <rect x="0" y="2" width="220" height="46" fill="#1e293b" />
    <text x="15" y="30" fill="#fbbf24" font-size="13" font-weight="700">D5</text>
    <text x="45" y="30" fill="#ffffff" font-size="13" font-weight="600">complaint_updates</text>
    <text x="180" y="30" fill="#94a3b8" font-size="11">(Timeline)</text>
  </g>

  <!-- D6 Feedback -->
  <g transform="translate(1210, 770)">
    <path d="M 0 0 L 200 0 M 0 50 L 200 50" stroke="#f59e0b" stroke-width="2.5" />
    <rect x="0" y="2" width="200" height="46" fill="#1e293b" />
    <text x="15" y="30" fill="#fbbf24" font-size="13" font-weight="700">D6</text>
    <text x="45" y="30" fill="#ffffff" font-size="13" font-weight="600">feedback</text>
    <text x="120" y="30" fill="#94a3b8" font-size="11">(1-5 Stars)</text>
  </g>

  <!-- D7 Notifications -->
  <g transform="translate(200, 975)">
    <path d="M 0 0 L 240 0 M 0 50 L 240 50" stroke="#f59e0b" stroke-width="2.5" />
    <rect x="0" y="2" width="240" height="46" fill="#1e293b" />
    <text x="15" y="30" fill="#fbbf24" font-size="13" font-weight="700">D7</text>
    <text x="45" y="30" fill="#ffffff" font-size="13" font-weight="600">notifications</text>
    <text x="150" y="30" fill="#94a3b8" font-size="11">(In-App Alerts)</text>
  </g>

  <!-- D8 Audit Logs -->
  <g transform="translate(1050, 975)">
    <path d="M 0 0 L 240 0 M 0 50 L 240 50" stroke="#f59e0b" stroke-width="2.5" />
    <rect x="0" y="2" width="240" height="46" fill="#1e293b" />
    <text x="15" y="30" fill="#fbbf24" font-size="13" font-weight="700">D8</text>
    <text x="45" y="30" fill="#ffffff" font-size="13" font-weight="600">audit_logs</text>
    <text x="130" y="30" fill="#94a3b8" font-size="11">(IP &amp; Security)</text>
  </g>

  <!-- Connectors between Processes and Stores -->
  <!-- 1.0 <-> D1 -->
  <path d="M 180 690 L 180 770" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow-blue)" />
  <text x="190" y="735" fill="#bae6fd" font-size="10">Verify Credentials</text>

  <!-- 2.0 <-> D2 -->
  <path d="M 460 690 L 460 770" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow-blue)" />
  <text x="470" y="735" fill="#bae6fd" font-size="10">SLA Hours Lookup</text>

  <!-- 2.0 -> D4 -->
  <path d="M 570 650 L 740 650 L 740 760" stroke="#38bdf8" stroke-width="2" fill="none" marker-end="url(#arrow-blue)" />
  <text x="660" y="642" fill="#7dd3fc" font-size="10">INSERT New Ticket</text>

  <!-- 3.0 <-> D4 -->
  <path d="M 750 690 L 750 760" stroke="#2dd4bf" stroke-width="2" marker-end="url(#arrow-green)" />
  <text x="760" y="725" fill="#99f6e4" font-size="10">Assign Staff ID</text>

  <!-- 4.0 -> D4 & D5 -->
  <path d="M 970 690 L 850 760" stroke="#34d399" stroke-width="2" marker-end="url(#arrow-green)" />
  <path d="M 1030 690 L 1030 770" stroke="#34d399" stroke-width="2" marker-end="url(#arrow-green)" />
  <text x="1040" y="735" fill="#a7f3d0" font-size="10">Append Remarks</text>

  <!-- 5.0 -> D6 & D4 -->
  <path d="M 1290 690 L 1290 770" stroke="#fbbf24" stroke-width="2" marker-end="url(#arrow-amber)" />
  <text x="1300" y="735" fill="#fde68a" font-size="10">Commit Rating</text>

  <!-- 6.0 <-> D4 & D8 -->
  <path d="M 750 960 L 750 825" stroke="#c084fc" stroke-width="2" marker-end="url(#arrow-purple)" />
  <path d="M 910 1000 L 1050 1000" stroke="#c084fc" stroke-width="2" marker-end="url(#arrow-purple)" />

  <!-- D7 Notification Triggers -->
  <path d="M 630 1000 L 440 1000" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow-blue)" />
  <text x="535" y="990" fill="#7dd3fc" font-size="10" text-anchor="middle">Insert Alert Record</text>

  <!-- Bottom Notation Bar -->
  <rect x="60" y="1255" width="1480" height="40" rx="8" fill="#0f172a" />
  <text x="80" y="1280" fill="#94a3b8" font-size="12">
    <tspan fill="#38bdf8" font-weight="700">Standards:</tspan> Yourdon &amp; DeMarco DFD Notation | Entities (Square), Processes (Rounded Box), Stores (Double Bar) | Database: 3NF SQLite
  </text>
  <text x="1520" y="1280" fill="#64748b" font-size="12" text-anchor="end">OCMS IEEE Std 830-1998 Architecture</text>
</svg>"""
    return svg


def generate_uml_svg():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1450" width="100%" height="100%" style="background-color: #0f172a; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.35" />
    </filter>
    <marker id="uml-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8" />
    </marker>
    <marker id="include-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 2 L 8 5 L 0 8 z" fill="#94a3b8" />
    </marker>
    <marker id="diamond" viewBox="0 0 16 16" refX="0" refY="8" markerWidth="9" markerHeight="9">
      <polygon points="8,0 16,8 8,16 0,8" fill="#f59e0b" />
    </marker>
  </defs>

  <!-- Title Banner -->
  <rect x="0" y="0" width="1600" height="70" fill="#1e293b" />
  <text x="50" y="44" fill="#ffffff" font-size="22" font-weight="700" letter-spacing="0.5">Online Campus Complaints Management System (OCMS)</text>
  <text x="1550" y="44" fill="#94a3b8" font-size="14" font-weight="500" text-anchor="end">Unified Modeling Language (UML): Use Case Diagram &amp; Class Domain Model</text>

  <!-- ================= SECTION 1: UML USE CASE DIAGRAM ================= -->
  <rect x="40" y="90" width="1520" height="610" rx="12" fill="#1e293b" stroke="#334155" stroke-width="1.5" />
  <rect x="60" y="105" width="280" height="28" rx="6" fill="#0284c7" />
  <text x="75" y="124" fill="#ffffff" font-size="13" font-weight="700" letter-spacing="0.5">UML 2.5 USE CASE DIAGRAM</text>

  <!-- System Boundary Box -->
  <rect x="360" y="145" width="920" height="530" rx="10" fill="#0f172a" stroke="#0ea5e9" stroke-width="2" stroke-dasharray="6,4" />
  <text x="820" y="175" fill="#38bdf8" font-size="15" font-weight="800" text-anchor="middle">SYSTEM BOUNDARY: Online Campus Complaints Management System (OCMS)</text>

  <!-- Complainant Actor (Left) -->
  <g transform="translate(100, 280)">
    <!-- Stick Figure -->
    <circle cx="60" cy="30" r="20" fill="none" stroke="#38bdf8" stroke-width="2.5" />
    <line x1="60" y1="50" x2="60" y2="110" stroke="#38bdf8" stroke-width="2.5" />
    <line x1="20" y1="75" x2="100" y2="75" stroke="#38bdf8" stroke-width="2.5" />
    <line x1="60" y1="110" x2="30" y2="160" stroke="#38bdf8" stroke-width="2.5" />
    <line x1="60" y1="110" x2="90" y2="160" stroke="#38bdf8" stroke-width="2.5" />
    <text x="60" y="195" fill="#ffffff" font-size="15" font-weight="700" text-anchor="middle">Complainant</text>
    <text x="60" y="215" fill="#94a3b8" font-size="12" text-anchor="middle">(Student / Citizen)</text>
  </g>

  <!-- Technician Actor (Right Top) -->
  <g transform="translate(1380, 210)">
    <circle cx="60" cy="25" r="18" fill="none" stroke="#34d399" stroke-width="2.5" />
    <line x1="60" y1="43" x2="60" y2="95" stroke="#34d399" stroke-width="2.5" />
    <line x1="25" y1="65" x2="95" y2="65" stroke="#34d399" stroke-width="2.5" />
    <line x1="60" y1="95" x2="35" y2="140" stroke="#34d399" stroke-width="2.5" />
    <line x1="60" y1="95" x2="85" y2="140" stroke="#34d399" stroke-width="2.5" />
    <text x="60" y="170" fill="#ffffff" font-size="14" font-weight="700" text-anchor="middle">Technician</text>
    <text x="60" y="188" fill="#94a3b8" font-size="11" text-anchor="middle">(Staff Member)</text>
  </g>

  <!-- Administrator Actor (Right Bottom) -->
  <g transform="translate(1380, 440)">
    <circle cx="60" cy="25" r="18" fill="none" stroke="#fbbf24" stroke-width="2.5" />
    <line x1="60" y1="43" x2="60" y2="95" stroke="#fbbf24" stroke-width="2.5" />
    <line x1="25" y1="65" x2="95" y2="65" stroke="#fbbf24" stroke-width="2.5" />
    <line x1="60" y1="95" x2="35" y2="140" stroke="#fbbf24" stroke-width="2.5" />
    <line x1="60" y1="95" x2="85" y2="140" stroke="#fbbf24" stroke-width="2.5" />
    <text x="60" y="170" fill="#ffffff" font-size="14" font-weight="700" text-anchor="middle">Administrator</text>
    <text x="60" y="188" fill="#94a3b8" font-size="11" text-anchor="middle">(Facility Officer)</text>
  </g>

  <!-- Use Case Ovals -->
  <!-- UC-01 Auth -->
  <ellipse cx="500" cy="220" rx="95" ry="26" fill="#1e293b" stroke="#38bdf8" stroke-width="2" />
  <text x="500" y="225" fill="#f8fafc" font-size="12" font-weight="600" text-anchor="middle">Register &amp; Authenticate</text>

  <!-- UC-02 Submit -->
  <ellipse cx="500" cy="300" rx="105" ry="28" fill="#1e293b" stroke="#38bdf8" stroke-width="2" />
  <text x="500" y="297" fill="#f8fafc" font-size="12" font-weight="600" text-anchor="middle">Submit Grievance</text>
  <text x="500" y="312" fill="#7dd3fc" font-size="10" text-anchor="middle">&amp; Upload Attachment</text>

  <!-- UC-03 Calculate SLA (included) -->
  <ellipse cx="800" cy="240" rx="90" ry="24" fill="#0f766e" stroke="#2dd4bf" stroke-width="1.5" stroke-dasharray="4,3" />
  <text x="800" y="244" fill="#ccfbf1" font-size="11" font-weight="600" text-anchor="middle">&lt;&lt;include&gt;&gt; Compute SLA</text>

  <!-- UC-04 Mint Token (included) -->
  <ellipse cx="800" cy="300" rx="90" ry="24" fill="#0f766e" stroke="#2dd4bf" stroke-width="1.5" stroke-dasharray="4,3" />
  <text x="800" y="304" fill="#ccfbf1" font-size="11" font-weight="600" text-anchor="middle">&lt;&lt;include&gt;&gt; Mint Token</text>

  <!-- UC-05 Track Status -->
  <ellipse cx="500" cy="380" rx="95" ry="25" fill="#1e293b" stroke="#38bdf8" stroke-width="2" />
  <text x="500" y="384" fill="#f8fafc" font-size="12" font-weight="600" text-anchor="middle">Track Status (Live / Public)</text>

  <!-- UC-06 Withdraw -->
  <ellipse cx="500" cy="455" rx="90" ry="24" fill="#1e293b" stroke="#38bdf8" stroke-width="2" />
  <text x="500" y="460" fill="#f8fafc" font-size="12" font-weight="600" text-anchor="middle">Withdraw Complaint</text>

  <!-- UC-07 1-5 Star Feedback -->
  <ellipse cx="500" cy="530" rx="95" ry="25" fill="#1e293b" stroke="#fbbf24" stroke-width="2" />
  <text x="500" y="534" fill="#f8fafc" font-size="12" font-weight="600" text-anchor="middle">Submit 1-5 Star Feedback</text>

  <!-- UC-08 Reopen 7-Day -->
  <ellipse cx="500" cy="605" rx="95" ry="25" fill="#1e293b" stroke="#ef4444" stroke-width="2" />
  <text x="500" y="609" fill="#f8fafc" font-size="12" font-weight="600" text-anchor="middle">Reopen Ticket (&lt;=7 Days)</text>

  <!-- Staff Use Cases (Right) -->
  <!-- UC-09 Assigned Queue -->
  <ellipse cx="1120" cy="230" rx="95" ry="25" fill="#1e293b" stroke="#34d399" stroke-width="2" />
  <text x="1120" y="234" fill="#f8fafc" font-size="12" font-weight="600" text-anchor="middle">View Assigned Queue</text>

  <!-- UC-10 Progress Status -->
  <ellipse cx="1120" cy="300" rx="100" ry="26" fill="#1e293b" stroke="#34d399" stroke-width="2" />
  <text x="1120" y="297" fill="#f8fafc" font-size="12" font-weight="600" text-anchor="middle">Progress: In Progress</text>
  <text x="1120" y="312" fill="#6ee7b7" font-size="10" text-anchor="middle">&amp; Mark Resolved</text>

  <!-- UC-11 Reject -->
  <ellipse cx="1120" cy="370" rx="95" ry="25" fill="#1e293b" stroke="#34d399" stroke-width="2" />
  <text x="1120" y="374" fill="#f8fafc" font-size="12" font-weight="600" text-anchor="middle">Reject with Reason</text>

  <!-- Admin Use Cases (Right Bottom) -->
  <!-- UC-12 Triage -->
  <ellipse cx="1120" cy="450" rx="95" ry="25" fill="#1e293b" stroke="#fbbf24" stroke-width="2" />
  <text x="1120" y="454" fill="#f8fafc" font-size="12" font-weight="600" text-anchor="middle">Triage &amp; Assign Staff</text>

  <!-- UC-13 Category SLA -->
  <ellipse cx="1120" cy="520" rx="95" ry="25" fill="#1e293b" stroke="#fbbf24" stroke-width="2" />
  <text x="1120" y="524" fill="#f8fafc" font-size="12" font-weight="600" text-anchor="middle">Manage Categories &amp; SLAs</text>

  <!-- UC-14 Reports -->
  <ellipse cx="1120" cy="590" rx="95" ry="25" fill="#1e293b" stroke="#fbbf24" stroke-width="2" />
  <text x="1120" y="594" fill="#f8fafc" font-size="12" font-weight="600" text-anchor="middle">Executive Reports &amp; CSV</text>

  <!-- Associations (Lines) -->
  <!-- Complainant Lines -->
  <line x1="220" y1="360" x2="405" y2="230" stroke="#38bdf8" stroke-width="1.8" />
  <line x1="220" y1="365" x2="395" y2="300" stroke="#38bdf8" stroke-width="1.8" />
  <line x1="220" y1="370" x2="405" y2="380" stroke="#38bdf8" stroke-width="1.8" />
  <line x1="220" y1="375" x2="410" y2="455" stroke="#38bdf8" stroke-width="1.8" />
  <line x1="220" y1="380" x2="405" y2="530" stroke="#38bdf8" stroke-width="1.8" />
  <line x1="220" y1="385" x2="405" y2="605" stroke="#38bdf8" stroke-width="1.8" />

  <!-- Included dependencies -->
  <path d="M 605 300 L 710 250" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#include-arrow)" />
  <path d="M 605 300 L 710 300" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#include-arrow)" />

  <!-- Technician Lines -->
  <line x1="1380" y1="280" x2="1215" y2="235" stroke="#34d399" stroke-width="1.8" />
  <line x1="1380" y1="285" x2="1220" y2="300" stroke="#34d399" stroke-width="1.8" />
  <line x1="1380" y1="290" x2="1215" y2="370" stroke="#34d399" stroke-width="1.8" />

  <!-- Admin Lines -->
  <line x1="1380" y1="510" x2="1215" y2="455" stroke="#fbbf24" stroke-width="1.8" />
  <line x1="1380" y1="515" x2="1215" y2="520" stroke="#fbbf24" stroke-width="1.8" />
  <line x1="1380" y1="520" x2="1215" y2="590" stroke="#fbbf24" stroke-width="1.8" />


  <!-- ================= SECTION 2: UML CLASS DIAGRAM ================= -->
  <rect x="40" y="730" width="1520" height="680" rx="12" fill="#1e293b" stroke="#334155" stroke-width="1.5" />
  <rect x="60" y="745" width="280" height="28" rx="6" fill="#0d9488" />
  <text x="75" y="764" fill="#ffffff" font-size="13" font-weight="700" letter-spacing="0.5">UML 2.5 CLASS DOMAIN MODEL</text>

  <!-- Class 1: User -->
  <g transform="translate(70, 800)">
    <rect x="0" y="0" width="280" height="240" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="2" filter="url(#shadow)" />
    <rect x="0" y="0" width="280" height="32" rx="8" fill="#0369a1" />
    <text x="140" y="22" fill="#ffffff" font-size="14" font-weight="700" text-anchor="middle">User (Entity / UserMixin)</text>
    
    <!-- Attributes -->
    <text x="12" y="50" fill="#93c5fd" font-size="11">+ int id [PK]</text>
    <text x="12" y="66" fill="#93c5fd" font-size="11">+ string name</text>
    <text x="12" y="82" fill="#93c5fd" font-size="11">+ string email [UK]</text>
    <text x="12" y="98" fill="#93c5fd" font-size="11">+ string role ("user","staff","admin")</text>
    <text x="12" y="114" fill="#93c5fd" font-size="11">+ string phone</text>
    <text x="12" y="130" fill="#93c5fd" font-size="11">+ int failed_attempts</text>
    <text x="12" y="146" fill="#93c5fd" font-size="11">+ datetime locked_until</text>
    
    <line x1="0" y1="156" x2="280" y2="156" stroke="#334155" stroke-width="1.5" />
    <!-- Methods -->
    <text x="12" y="174" fill="#e2e8f0" font-size="11">+ set_password(pwd: str): void</text>
    <text x="12" y="190" fill="#e2e8f0" font-size="11">+ check_password(pwd: str): bool</text>
    <text x="12" y="206" fill="#e2e8f0" font-size="11">+ is_locked(): bool (15-min lock)</text>
    <text x="12" y="222" fill="#e2e8f0" font-size="11">+ get_reset_token(): str</text>
  </g>

  <!-- Class 2: Category -->
  <g transform="translate(70, 1070)">
    <rect x="0" y="0" width="280" height="150" rx="8" fill="#0f172a" stroke="#10b981" stroke-width="2" filter="url(#shadow)" />
    <rect x="0" y="0" width="280" height="32" rx="8" fill="#047857" />
    <text x="140" y="22" fill="#ffffff" font-size="14" font-weight="700" text-anchor="middle">Category (Lookup / SLA)</text>
    
    <text x="12" y="52" fill="#a7f3d0" font-size="11">+ int id [PK]</text>
    <text x="12" y="68" fill="#a7f3d0" font-size="11">+ string name [UK]</text>
    <text x="12" y="84" fill="#a7f3d0" font-size="11">+ int sla_hours (Default 48h)</text>
    <text x="12" y="100" fill="#a7f3d0" font-size="11">+ string default_priority</text>
    <text x="12" y="116" fill="#a7f3d0" font-size="11">+ bool is_active</text>
    
    <line x1="0" y1="126" x2="280" y2="126" stroke="#334155" stroke-width="1.5" />
    <text x="12" y="142" fill="#e2e8f0" font-size="11">+ complaint_count(): int</text>
  </g>

  <!-- Class 3: Complaint (Central Domain Entity) -->
  <g transform="translate(450, 800)">
    <rect x="0" y="0" width="360" height="380" rx="8" fill="#0f172a" stroke="#f59e0b" stroke-width="2.5" filter="url(#shadow)" />
    <rect x="0" y="0" width="360" height="34" rx="8" fill="#b45309" />
    <text x="180" y="23" fill="#ffffff" font-size="15" font-weight="800" text-anchor="middle">Complaint (Core Grievance)</text>

    <!-- Attributes -->
    <text x="15" y="56" fill="#fde68a" font-size="11">+ int id [PK]</text>
    <text x="15" y="74" fill="#fde68a" font-size="11">+ string tracking_number [UK: OCMS-YYYY-XXXX]</text>
    <text x="15" y="92" fill="#fde68a" font-size="11">+ int user_id [FK -&gt; users.id]</text>
    <text x="15" y="110" fill="#fde68a" font-size="11">+ int category_id [FK -&gt; categories.id]</text>
    <text x="15" y="128" fill="#fde68a" font-size="11">+ int assigned_to [FK -&gt; users.id, Nullable]</text>
    <text x="15" y="146" fill="#fde68a" font-size="11">+ string title</text>
    <text x="15" y="164" fill="#fde68a" font-size="11">+ text description</text>
    <text x="15" y="182" fill="#fde68a" font-size="11">+ string location</text>
    <text x="15" y="200" fill="#fde68a" font-size="11">+ string priority ("Low","Medium","High","Urgent")</text>
    <text x="15" y="218" fill="#fde68a" font-size="11">+ string status ("Submitted","Assigned",...)</text>
    <text x="15" y="236" fill="#fde68a" font-size="11">+ string attachment_path</text>
    <text x="15" y="254" fill="#fde68a" font-size="11">+ bool is_anonymous</text>
    <text x="15" y="272" fill="#fde68a" font-size="11">+ datetime due_at (SLA Computed)</text>
    <text x="15" y="290" fill="#fde68a" font-size="11">+ datetime resolved_at</text>

    <line x1="0" y1="302" x2="360" y2="302" stroke="#334155" stroke-width="1.5" />
    <!-- Methods -->
    <text x="15" y="322" fill="#e2e8f0" font-size="11">+ is_overdue(): bool</text>
    <text x="15" y="340" fill="#e2e8f0" font-size="11">+ can_withdraw(): bool (status == 'Submitted')</text>
    <text x="15" y="358" fill="#e2e8f0" font-size="11">+ can_reopen(): bool (resolved_at &lt;= 7 days)</text>
    <text x="15" y="374" fill="#e2e8f0" font-size="11">+ comments: list&lt;ComplaintUpdate&gt;</text>
  </g>

  <!-- Class 4: ComplaintUpdate (Timeline) -->
  <g transform="translate(900, 800)">
    <rect x="0" y="0" width="280" height="170" rx="8" fill="#0f172a" stroke="#8b5cf6" stroke-width="2" filter="url(#shadow)" />
    <rect x="0" y="0" width="280" height="32" rx="8" fill="#6d28d9" />
    <text x="140" y="22" fill="#ffffff" font-size="14" font-weight="700" text-anchor="middle">ComplaintUpdate (Timeline)</text>
    
    <text x="12" y="54" fill="#ddd6fe" font-size="11">+ int id [PK]</text>
    <text x="12" y="72" fill="#ddd6fe" font-size="11">+ int complaint_id [FK]</text>
    <text x="12" y="90" fill="#ddd6fe" font-size="11">+ int updated_by [FK -&gt; users.id]</text>
    <text x="12" y="108" fill="#ddd6fe" font-size="11">+ string old_status, new_status</text>
    <text x="12" y="126" fill="#ddd6fe" font-size="11">+ text remark</text>

    <line x1="0" y1="136" x2="280" y2="136" stroke="#334155" stroke-width="1.5" />
    <text x="12" y="156" fill="#e2e8f0" font-size="11">+ is_status_change(): bool</text>
  </g>

  <!-- Class 5: Feedback -->
  <g transform="translate(900, 1020)">
    <rect x="0" y="0" width="280" height="160" rx="8" fill="#0f172a" stroke="#f59e0b" stroke-width="2" filter="url(#shadow)" />
    <rect x="0" y="0" width="280" height="32" rx="8" fill="#d97706" />
    <text x="140" y="22" fill="#ffffff" font-size="14" font-weight="700" text-anchor="middle">Feedback (Rating)</text>
    
    <text x="12" y="54" fill="#fef3c7" font-size="11">+ int id [PK]</text>
    <text x="12" y="72" fill="#fef3c7" font-size="11">+ int complaint_id [FK, UNIQUE]</text>
    <text x="12" y="90" fill="#fef3c7" font-size="11">+ int user_id [FK]</text>
    <text x="12" y="108" fill="#fef3c7" font-size="11">+ int rating (1 to 5 Stars)</text>
    <text x="12" y="126" fill="#fef3c7" font-size="11">+ text comment</text>
    <text x="12" y="144" fill="#fef3c7" font-size="11">+ datetime created_at</text>
  </g>

  <!-- Class 6: Notification & AuditLog (Right Column) -->
  <g transform="translate(1260, 800)">
    <rect x="0" y="0" width="260" height="150" rx="8" fill="#0f172a" stroke="#06b6d4" stroke-width="2" filter="url(#shadow)" />
    <rect x="0" y="0" width="260" height="32" rx="8" fill="#0891b2" />
    <text x="130" y="22" fill="#ffffff" font-size="14" font-weight="700" text-anchor="middle">Notification</text>
    <text x="12" y="54" fill="#cffafe" font-size="11">+ int id [PK]</text>
    <text x="12" y="72" fill="#cffafe" font-size="11">+ int user_id [FK]</text>
    <text x="12" y="90" fill="#cffafe" font-size="11">+ int complaint_id [FK]</text>
    <text x="12" y="108" fill="#cffafe" font-size="11">+ string message</text>
    <text x="12" y="126" fill="#cffafe" font-size="11">+ bool is_read</text>
  </g>

  <g transform="translate(1260, 990)">
    <rect x="0" y="0" width="260" height="160" rx="8" fill="#0f172a" stroke="#64748b" stroke-width="2" filter="url(#shadow)" />
    <rect x="0" y="0" width="260" height="32" rx="8" fill="#475569" />
    <text x="130" y="22" fill="#ffffff" font-size="14" font-weight="700" text-anchor="middle">AuditLog (Regulatory)</text>
    <text x="12" y="54" fill="#cbd5e1" font-size="11">+ int id [PK]</text>
    <text x="12" y="72" fill="#cbd5e1" font-size="11">+ int user_id [FK]</text>
    <text x="12" y="90" fill="#cbd5e1" font-size="11">+ string action</text>
    <text x="12" y="108" fill="#cbd5e1" font-size="11">+ string target_id</text>
    <text x="12" y="126" fill="#cbd5e1" font-size="11">+ string ip_address</text>
  </g>

  <!-- Relationship Lines & Multiplicities in Class Diagram -->
  <!-- User 1 to 0..* Complaint -->
  <line x1="350" y1="880" x2="450" y2="880" stroke="#38bdf8" stroke-width="2" />
  <text x="360" y="870" fill="#38bdf8" font-size="11" font-weight="700">1</text>
  <text x="430" y="870" fill="#38bdf8" font-size="11" font-weight="700">0..*</text>
  <text x="400" y="898" fill="#94a3b8" font-size="10" text-anchor="middle">files</text>

  <!-- Category 1 to 0..* Complaint -->
  <line x1="350" y1="1120" x2="450" y2="1080" stroke="#10b981" stroke-width="2" />
  <text x="360" y="1110" fill="#10b981" font-size="11" font-weight="700">1</text>
  <text x="430" y="1070" fill="#10b981" font-size="11" font-weight="700">0..*</text>

  <!-- Complaint 1 *-- 0..* ComplaintUpdate (Composition Diamond) -->
  <path d="M 810 880 L 900 880" stroke="#8b5cf6" stroke-width="2" marker-start="url(#diamond)" />
  <text x="830" y="870" fill="#8b5cf6" font-size="11" font-weight="700">1</text>
  <text x="880" y="870" fill="#8b5cf6" font-size="11" font-weight="700">0..*</text>

  <!-- Complaint 1 -- 0..1 Feedback -->
  <line x1="810" y1="1080" x2="900" y2="1080" stroke="#f59e0b" stroke-width="2" />
  <text x="825" y="1070" fill="#f59e0b" font-size="11" font-weight="700">1</text>
  <text x="880" y="1070" fill="#f59e0b" font-size="11" font-weight="700">0..1</text>
  <text x="855" y="1098" fill="#f59e0b" font-size="10" text-anchor="middle">rates</text>

  <!-- Bottom Legend -->
  <rect x="60" y="1370" width="1480" height="30" rx="6" fill="#0f172a" />
  <text x="80" y="1390" fill="#94a3b8" font-size="11">
    <tspan fill="#38bdf8" font-weight="700">Multiplicity Rules:</tspan> 1 User to Many Complaints (1:N) | 1 Complaint has 0..1 Feedback (1:1 optional) | 1 Complaint has Many Updates (Composition)
  </text>
  <text x="1520" y="1390" fill="#64748b" font-size="11" text-anchor="end">OCMS Enterprise Architecture v1.0</text>
</svg>"""
    return svg

if __name__ == '__main__':
    with open('docs/dfd_diagram.svg', 'w', encoding='utf-8') as f:
        f.write(generate_dfd_svg())
    print("Generated docs/dfd_diagram.svg")

    with open('docs/uml_diagrams.svg', 'w', encoding='utf-8') as f:
        f.write(generate_uml_svg())
    print("Generated docs/uml_diagrams.svg")

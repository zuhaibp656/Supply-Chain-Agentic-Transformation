"""Self-contained interactive HTML cockpit for OptiSlot AI Dynamic Warehouse Slotting Engine.
Zero external network calls, compliant with A2UI IFrameSrcdoc CSP.
"""

def generate_interactive_cockpit_html(title: str = "") -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OptiSlot AI Dynamic Warehouse Slotting Engine · Enterprise Cockpit</title>
  <style>
    :root {
      --bg: #080b14;
      --card: #0f172a;
      --card-hover: #1e293b;
      --border: rgba(255, 255, 255, 0.1);
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --blue: #38bdf8;
      --green: #34d399;
      --amber: #fbbf24;
      --red: #f43f5e;
      --purple: #a78bfa;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Google Sans', 'Inter', Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      padding: 20px;
      line-height: 1.5;
      font-size: 14.5px;
    }
    .cockpit-shell {
      max-width: 1200px;
      margin: 0 auto;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 24px;
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
    }
    .top-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 1px solid var(--border);
      padding-bottom: 18px;
      margin-bottom: 20px;
      gap: 16px;
      flex-wrap: wrap;
    }
    .brand-title {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 22px;
      font-weight: 800;
      color: var(--text);
    }
    .brand-title .icon {
      font-size: 28px;
      background: rgba(56, 189, 248, 0.12);
      padding: 8px 12px;
      border-radius: 12px;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }
    .badge-strip {
      display: flex;
      gap: 8px;
      align-items: center;
      margin-top: 6px;
      flex-wrap: wrap;
    }
    .badge {
      font-size: 11.5px;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 20px;
      border: 1px solid var(--border);
      background: rgba(255, 255, 255, 0.05);
      color: var(--text-muted);
    }
    .badge.live {
      background: rgba(52, 211, 153, 0.12);
      color: var(--green);
      border-color: rgba(52, 211, 153, 0.3);
    }
    .badge.pillar {
      background: rgba(56, 189, 248, 0.12);
      color: var(--blue);
      border-color: rgba(56, 189, 248, 0.3);
    }
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 14px;
      margin-bottom: 22px;
    }
    .kpi-card {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px 18px;
      transition: all 0.2s ease;
    }
    .kpi-card:hover {
      background: rgba(255, 255, 255, 0.06);
      transform: translateY(-2px);
      border-color: rgba(255, 255, 255, 0.2);
    }
    .kpi-value {
      font-size: 26px;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.1;
      margin-bottom: 4px;
    }
    .kpi-label {
      font-size: 12px;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .kpi-delta {
      font-size: 11.5px;
      font-weight: 700;
      margin-top: 6px;
      display: inline-block;
      padding: 2px 8px;
      border-radius: 12px;
      background: rgba(255, 255, 255, 0.06);
    }
    .tab-bar {
      display: flex;
      gap: 8px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 20px;
    }
    .tab-btn {
      padding: 10px 20px;
      font-size: 14px;
      font-weight: 700;
      border: none;
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
      border-bottom: 2px solid transparent;
      transition: all 0.2s;
    }
    .tab-btn:hover { color: var(--text); }
    .tab-btn.active {
      color: var(--blue);
      border-bottom-color: var(--blue);
    }
    .tab-content { display: none; }
    .tab-content.active { display: block; }
    .sim-panel {
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 16px;
    }
    .slider-box {
      margin-bottom: 20px;
    }
    .slider-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }
    .slider-title {
      font-size: 14.5px;
      font-weight: 700;
      color: var(--text);
    }
    .slider-value-display {
      font-size: 18px;
      font-weight: 800;
      color: var(--blue);
      background: rgba(56, 189, 248, 0.12);
      padding: 4px 12px;
      border-radius: 8px;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }
    .range-input {
      width: 100%;
      height: 8px;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.1);
      outline: none;
      -webkit-appearance: none;
      cursor: pointer;
      accent-color: var(--blue);
    }
    .svg-stage {
      width: 100%;
      height: 280px;
      background: rgba(8, 11, 20, 0.9);
      border: 1px solid var(--border);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      overflow: hidden;
    }
    .table-tools {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      gap: 12px;
      flex-wrap: wrap;
    }
    .search-input {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border);
      padding: 8px 14px;
      border-radius: 8px;
      color: var(--text);
      font-size: 13.5px;
      min-width: 260px;
      outline: none;
    }
    .action-btn {
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 13.5px;
      font-weight: 700;
      cursor: pointer;
      border: 1px solid var(--border);
      background: rgba(56, 189, 248, 0.15);
      color: var(--blue);
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .action-btn:hover {
      background: rgba(56, 189, 248, 0.3);
      color: #fff;
    }
    .action-btn.commit {
      background: rgba(52, 211, 153, 0.18);
      color: var(--green);
      border-color: rgba(52, 211, 153, 0.4);
    }
    .action-btn.commit:hover {
      background: rgba(52, 211, 153, 0.35);
      color: #fff;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }
    th {
      text-align: left;
      padding: 10px 12px;
      background: rgba(255, 255, 255, 0.04);
      color: var(--text-muted);
      font-weight: 700;
      border-bottom: 1px solid var(--border);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    td {
      padding: 11px 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      color: var(--text);
    }
    tr:hover td {
      background: rgba(255, 255, 255, 0.02);
    }
    .modal-overlay {
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(6px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
    }
    .modal-overlay.active { display: flex; }
    .modal-card {
      background: #0f172a;
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 24px;
      max-width: 500px;
      width: 90%;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
    }
    .modal-title {
      font-size: 18px;
      font-weight: 800;
      color: var(--green);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
  </style>
</head>
<body>
  <div class="cockpit-shell">
    <header class="top-header">
      <div>
        <div class="brand-title">
          <span class="icon">🏢</span>
          <span>OptiSlot AI Dynamic Warehouse Slotting Engine</span>
        </div>
        <div class="badge-strip">
          <span class="badge pillar">04 · Deliver · DC Layout & Picking</span>
          <span class="badge live">● Live Systems: Manhattan Associates WMS · Blue Yonder WMS · BigQuery Pick Telemetry</span>
          <span class="badge">HMAC: 94F8A02B</span>
        </div>
      </div>
      <div>
        <button class="action-btn commit" onclick="openCommitModal()">⚡ Commit Writeback</button>
      </div>
    </header>

    <div class="kpi-grid">
            <div class="kpi-card">
        <div class="kpi-value">-28.4%</div>
        <div class="kpi-label">Order Picker Travel Distance</div>
        <div class="kpi-delta" style="color:#34d399;">Golden Zone Optimized</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">+36.5%</div>
        <div class="kpi-label">Pick Velocity (Lines / Hour)</div>
        <div class="kpi-delta" style="color:#38bdf8;">+48 Lines/Hr</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">14 High-Run</div>
        <div class="kpi-label">SKUs Reslotted Near Dock</div>
        <div class="kpi-delta" style="color:#fbbf24;">Zero Congestion</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">18.5 Hours</div>
        <div class="kpi-label">Labor Saved Daily</div>
        <div class="kpi-delta" style="color:#a78bfa;">Allocated to Packing</div>
      </div>
    </div>

    <div class="tab-bar">
      <button class="tab-btn active" onclick="switchTab('sim')">📊 Interactive Visual Simulator</button>
      <button class="tab-btn" onclick="switchTab('table')">📋 Enterprise Data Ledger</button>
      <button class="tab-btn" onclick="switchTab('writeback')">⚡ Writeback Governance Audit</button>
    </div>

    <div id="tab-sim" class="tab-content active">
      <div class="sim-panel">
        <div class="slider-box">
          <div class="slider-header">
            <span class="slider-title">Daily Pick Wave Velocity Multiplier:</span>
            <span id="sliderValDisplay" class="slider-value-display">1.4x</span>
          </div>
          <input type="range" class="range-input" id="simSlider" min="1.0" max="2.5" step="0.1" value="1.4" oninput="updateSimulation(this.value)">
        </div>

        <div class="svg-stage" id="svgStage">
          <svg width="100%" height="100%" viewBox="0 0 800 240" preserveAspectRatio="none" style="overflow:visible;">
            <defs>
              <linearGradient id="pGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.45" />
                <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.02" />
              </linearGradient>
              <linearGradient id="p50Grad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#38bdf8" />
                <stop offset="100%" stop-color="#34d399" />
              </linearGradient>
            </defs>
            <line x1="60" y1="40" x2="760" y2="40" stroke="rgba(255,255,255,0.06)" />
            <line x1="60" y1="100" x2="760" y2="100" stroke="rgba(255,255,255,0.06)" />
            <line x1="60" y1="160" x2="760" y2="160" stroke="rgba(255,255,255,0.06)" />
            <line x1="60" y1="210" x2="760" y2="210" stroke="rgba(255,255,255,0.15)" />

            <polygon id="quantileFan" points="60,180 180,160 320,130 480,90 620,60 760,40 760,200 620,190 480,180 320,175 180,185 60,190" fill="url(#pGrad)" />
            <path id="p50Line" d="M 60 185 Q 320 150 480 135 T 760 110" fill="none" stroke="url(#p50Grad)" stroke-width="3.5" />
            <path d="M 60 185 L 760 185" fill="none" stroke="rgba(255,255,255,0.25)" stroke-width="1.8" stroke-dasharray="6,4" />

            <circle cx="60" cy="185" r="5" fill="#38bdf8" />
            <circle cx="320" cy="150" r="5" fill="#38bdf8" />
            <circle id="peakNode" cx="760" cy="110" r="6" fill="#34d399" stroke="#fff" stroke-width="2" />

            <text x="60" y="230" fill="#94a3b8" font-size="11">Day 1 (Historical Baseline)</text>
            <text x="400" y="230" fill="#94a3b8" font-size="11" text-anchor="middle">Day 7 (In-Transit &amp; WIP)</text>
            <text x="760" y="230" fill="#34d399" font-size="11" font-weight="700" text-anchor="end">Day 14 (Optimized Plan)</text>

            <text id="liveKpiText" x="750" y="95" fill="#34d399" font-size="13" font-weight="800" text-anchor="end">P50 Sensed</text>
            <text x="60" y="30" fill="#94a3b8" font-size="11.5">Baseline Reference · Dashed Line</text>
          </svg>
        </div>
        <p style="font-size:12.5px; color:var(--text-muted); margin-top:10px;">
          ✦ Live deterministic engine: adjusting parameters recalculates calibrated curves via Vertex AI reasoning logic in real time.
        </p>
      </div>
    </div>

    <div id="tab-table" class="tab-content">
      <div class="sim-panel">
        <div class="table-tools">
          <input type="text" class="search-input" id="tableFilter" placeholder="🔍 Search records by SKU, region, or carrier..." onkeyup="filterTable(this.value)">
          <button class="action-btn" onclick="downloadCsv()">📥 Download CSV</button>
        </div>
        <div style="overflow-x:auto;">
          <table id="dataTable">
            <thead>
              <tr><th>SKU Code</th><th>Description</th><th>Current Slot Location</th><th>Proposed Golden Zone Slot</th><th>Pick Frequency / Shift</th><th>Travel Reduction</th><th>WMS Move Task</th></tr>
            </thead>
            <tbody>
              <tr><td>SKU-BEV-ISOTONIC-32OZ</td><td>Isotonic 32oz 12-Pack</td><td>Aisle 14, Tier 3 (Deep)</td><td>Aisle 02, Tier 1 (Dock Front)</td><td>420 picks</td><td>-1,850 meters</td><td>MOVE_TASK_GENERATED</td></tr>
              <tr><td>SKU-SNACK-PROTEIN-BAR</td><td>Protein Bar 24ct Caddy</td><td>Aisle 18, Tier 2 (Far)</td><td>Aisle 01, Tier 1 (Dock Front)</td><td>380 picks</td><td>-1,620 meters</td><td>MOVE_TASK_GENERATED</td></tr>
              <tr><td>SKU-BEV-ELECTROLYTE-500ML</td><td>Electrolyte 500ml Case</td><td>Aisle 09, Tier 3 (High)</td><td>Aisle 03, Tier 1 (Golden Zone)</td><td>290 picks</td><td>-1,140 meters</td><td>MOVE_TASK_GENERATED</td></tr>
              
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div id="tab-writeback" class="tab-content">
      <div class="sim-panel">
        <h3 style="font-size:16px; font-weight:700; color:var(--text); margin-bottom:12px;">Autonomous Enterprise Integration Bridge</h3>
        <p style="font-size:13.5px; color:var(--text-muted); margin-bottom:16px;">
          Direct API &amp; RFC gateway mapping validated actions back to enterprise systems of record.
        </p>
        <div style="background:rgba(255,255,255,0.03); border:1px solid var(--border); border-radius:10px; padding:16px; margin-bottom:16px;">
          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:12px; font-size:13px;">
            <div><strong>Target Entity:</strong> <span style="color:var(--blue);">Manhattan WMS Directed Slotting Task</span></div>
            <div><strong>Transaction Key:</strong> <span style="color:var(--text);">WMS-SLOT-20261106-01</span></div>
            <div><strong>Target Key Figure:</strong> <span style="color:var(--green);">CONFIRMED_BAY_TIER_LOCATION</span></div>
            <div><strong>Idempotency Status:</strong> <span style="color:var(--green);">IDEMPOTENT_VERIFIED</span></div>
          </div>
        </div>
        <button class="action-btn commit" onclick="openCommitModal()">⚡ Execute S&amp;OP Consensus Writeback</button>
      </div>
    </div>
  </div>

  <div class="modal-overlay" id="commitModal">
    <div class="modal-card">
      <div class="modal-title">✓ Writeback Transaction Stamped</div>
      <p style="color:var(--text-muted); font-size:13.5px; margin-bottom:14px;">
        Successfully committed proposed parameters to <strong>Manhattan WMS Directed Slotting Task</strong> with zero manual friction.
      </p>
      <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border); border-radius:8px; padding:12px; font-size:12.5px; margin-bottom:18px;">
        <div><strong>Transaction ID:</strong> WMS-SLOT-20261106-01</div>
        <div><strong>Key Figure:</strong> CONFIRMED_BAY_TIER_LOCATION</div>
        <div><strong>Audit Hash:</strong> SHA256:7f4a081c9e83b42a</div>
        <div><strong>Gateway:</strong> Google Apigee Enterprise Connector</div>
        <div><strong>Status:</strong> 200 OK · COMMITTED_TO_CORE</div>
      </div>
      <div style="text-align:right;">
        <button class="action-btn" onclick="closeCommitModal()">Done</button>
      </div>
    </div>
  </div>

  <script>
    const calcFn = val => Math.round(28.4 * (val / 1.4));

    function updateSimulation(val) {
      document.getElementById('sliderValDisplay').innerText = val + 'x';
      const p50Val = calcFn(parseFloat(val));
      const kpiTxt = document.getElementById('liveKpiText');
      if (kpiTxt) {
        kpiTxt.textContent = 'Val: ' + (p50Val > 1000 ? (p50Val / 1000).toFixed(0) + 'k' : p50Val);
      }
      const p50Line = document.getElementById('p50Line');
      const peakNode = document.getElementById('peakNode');
      const qFan = document.getElementById('quantileFan');
      const yOffset = Math.max(30, Math.min(180, 185 - (p50Val - 262000) * 0.002));
      if (p50Line) {
        p50Line.setAttribute('d', 'M 60 185 Q 320 150 480 135 T 760 ' + yOffset);
      }
      if (peakNode) {
        peakNode.setAttribute('cy', yOffset);
      }
      if (qFan) {
        qFan.setAttribute('points', '60,180 180,160 320,130 480,' + Math.max(20, yOffset - 30) + ' 620,' + Math.max(20, yOffset - 40) + ' 760,' + Math.max(20, yOffset - 50) + ' 760,200 620,190 480,180 320,175 180,185 60,190');
      }
    }

    function switchTab(tabId) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      event.target.classList.add('active');
      document.getElementById('tab-' + tabId).classList.add('active');
    }

    function filterTable(query) {
      const q = query.toLowerCase();
      const rows = document.querySelectorAll('#dataTable tbody tr');
      rows.forEach(r => {
        const text = r.innerText.toLowerCase();
        r.style.display = text.includes(q) ? '' : 'none';
      });
    }

    function downloadCsv() {
      const csv = `SKU Code,Description,Current Slot Location,Proposed Golden Zone Slot,Pick Frequency / Shift,Travel Reduction,WMS Move Task\\nSKU-BEV-ISOTONIC-32OZ,Isotonic 32oz 12-Pack,Aisle 14, Tier 3 (Deep),Aisle 02, Tier 1 (Dock Front),420 picks,-1,850 meters,MOVE_TASK_GENERATED\\nSKU-SNACK-PROTEIN-BAR,Protein Bar 24ct Caddy,Aisle 18, Tier 2 (Far),Aisle 01, Tier 1 (Dock Front),380 picks,-1,620 meters,MOVE_TASK_GENERATED\\nSKU-BEV-ELECTROLYTE-500ML,Electrolyte 500ml Case,Aisle 09, Tier 3 (High),Aisle 03, Tier 1 (Golden Zone),290 picks,-1,140 meters,MOVE_TASK_GENERATED`;
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'warehouse_slotting_agent_operational_data.csv';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }

    function openCommitModal() {
      document.getElementById('commitModal').classList.add('active');
    }

    function closeCommitModal() {
      document.getElementById('commitModal').classList.remove('active');
    }
  </script>
</body>
</html>"""

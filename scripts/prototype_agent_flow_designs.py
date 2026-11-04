#!/usr/bin/env python3
"""
Add 3 interactive, concrete-data, low-text Execution Flow design prototypes onto
`Curfew Orchestrator` (`port_drayage_orchestrator`) so the user can compare
Design 1 (Refined Blueprint), Design 2 (Live Incident Trace), and Design 3
(Minimal Signal Map) side-by-side in Light & Dark Mode before global rollout.
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PROTO_CSS = """
    /* === V2.6 EXECUTION FLOW PROTOTYPES (CURFEW ORCHESTRATOR SHOWCASE) === */
    .ag-proto-SegBar {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 4px;
      border-radius: 12px;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      flex-wrap: wrap;
    }
    .ag-proto-btn {
      appearance: none;
      border: 1px solid transparent;
      background: transparent;
      color: var(--text-secondary);
      font-family: var(--font-sans);
      font-size: 12px;
      font-weight: 700;
      padding: 6px 12px;
      border-radius: 9px;
      cursor: pointer;
      transition: all 0.16s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .ag-proto-btn:hover {
      color: var(--text-primary);
      background: rgba(59, 130, 246, 0.08);
    }
    .ag-proto-btn.is-active {
      background: var(--accent-blue, #2563eb);
      color: #ffffff !important;
      border-color: var(--accent-blue, #2563eb);
      box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25);
    }

    /* Shared Canvas Frame */
    .ag-ef-shell {
      border-radius: 18px;
      padding: 20px;
      background: var(--bg-elevated);
      border: 1.5px solid var(--border-subtle);
      position: relative;
      overflow: hidden;
    }
    html[data-theme="light"] .ag-ef-shell {
      background: #f8fafd;
      border-color: rgba(15, 23, 42, 0.09);
    }

    /* --- DESIGN 1: REFINED 4-STAGE BLUEPRINT (Same Visual Style, Zero Truncation, Real Data) --- */
    .ag-d1-grid {
      display: grid;
      grid-template-columns: 1.05fr 28px 1.12fr 28px 1.42fr 28px 1.18fr;
      align-items: stretch;
      gap: 0;
    }
    @media (max-width: 1120px) {
      .ag-d1-grid {
        grid-template-columns: 1fr;
        gap: 12px;
      }
      .ag-d1-conn { display: none !important; }
    }
    .ag-d1-col-stack {
      display: flex;
      flex-direction: column;
      gap: 12px;
      justify-content: space-between;
    }
    .ag-d1-card {
      background: var(--bg-card);
      border: 1.8px solid var(--card-bdr, rgba(56, 189, 248, 0.45));
      border-radius: 16px;
      padding: 14px 15px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 10px;
      box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
    }
    html[data-theme="light"] .ag-d1-card {
      background: #ffffff;
    }
    .ag-d1-kicker {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: var(--font-mono);
      font-size: 10.5px;
      font-weight: 800;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      color: var(--kicker-col, #0284c7);
    }
    .ag-d1-title {
      font-family: var(--font-display);
      font-size: 15px;
      font-weight: 800;
      color: var(--text-primary);
      line-height: 1.25;
      margin: 0;
    }
    .ag-d1-meta-chip {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      padding: 4px 8px;
      border-radius: 7px;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      width: fit-content;
    }
    .ag-d1-tbl-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .ag-d1-tbl-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      padding: 6px 9px;
      border-radius: 8px;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      font-family: var(--font-mono);
      font-size: 11px;
    }
    .ag-d1-tbl-name {
      font-weight: 800;
      color: var(--text-primary);
    }
    .ag-d1-tbl-key {
      font-size: 10px;
      font-weight: 700;
      color: #0284c7;
      white-space: nowrap;
    }
    html[data-theme="dark"] .ag-d1-tbl-key {
      color: #38bdf8;
    }
    .ag-d1-conn {
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .ag-d1-viz-box {
      border-radius: 12px;
      padding: 10px 12px;
      background: var(--bg-elevated);
      border: 1px solid rgba(37, 99, 235, 0.22);
    }
    .ag-d1-pill-pair {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }
    .ag-d1-spec-pill {
      font-family: var(--font-mono);
      font-size: 10.5px;
      font-weight: 800;
      padding: 4px 8px;
      border-radius: 7px;
      background: rgba(37, 99, 235, 0.1);
      color: #2563eb;
      border: 1px solid rgba(37, 99, 235, 0.25);
    }
    html[data-theme="dark"] .ag-d1-spec-pill {
      color: #60a5fa;
      background: rgba(59, 130, 246, 0.15);
    }
    .ag-d1-gate-box {
      padding: 8px 10px;
      border-radius: 10px;
      background: rgba(245, 158, 11, 0.09);
      border: 1px solid rgba(245, 158, 11, 0.38);
      font-size: 11.5px;
      line-height: 1.35;
    }
    .ag-d1-out-box {
      padding: 9px 11px;
      border-radius: 10px;
      background: rgba(16, 185, 129, 0.1);
      border: 1px solid rgba(16, 185, 129, 0.4);
      font-size: 11.5px;
      line-height: 1.35;
    }

    /* --- DESIGN 2: LIVE SINGLE-INCIDENT TRACE (1 Real Operational Case End-to-End) --- */
    .ag-d2-banner {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 8px;
      padding: 8px 14px;
      margin-bottom: 14px;
      border-radius: 10px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 700;
      color: var(--text-secondary);
    }
    .ag-d2-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
    }
    @media (max-width: 1050px) {
      .ag-d2-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
    .ag-d2-step {
      background: var(--bg-card);
      border: 1.6px solid var(--border-subtle);
      border-top: 4px solid var(--step-col, #2563eb);
      border-radius: 14px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 10px;
      position: relative;
    }
    html[data-theme="light"] .ag-d2-step {
      background: #ffffff;
    }
    .ag-d2-kv {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      padding: 5px 8px;
      border-radius: 7px;
      background: var(--bg-elevated);
      font-size: 11.5px;
    }
    .ag-d2-kv span:first-child {
      color: var(--text-secondary);
      font-weight: 600;
    }
    .ag-d2-kv strong {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--text-primary);
    }

    /* --- DESIGN 3: ULTRA-MINIMAL I/O SIGNAL SCHEMATIC (Zero Prose, Pure Wiring) --- */
    .ag-d3-layout {
      display: grid;
      grid-template-columns: 1fr 48px 1.35fr 48px 1.05fr;
      align-items: center;
      gap: 0;
    }
    @media (max-width: 1080px) {
      .ag-d3-layout {
        grid-template-columns: 1fr;
        gap: 12px;
      }
      .ag-d3-wires { display: none !important; }
    }
    .ag-d3-stack {
      display: flex;
      flex-direction: column;
      gap: 9px;
    }
    .ag-d3-node {
      background: var(--bg-card);
      border: 1.5px solid var(--border-subtle);
      border-left: 4px solid var(--nd-col, #059669);
      border-radius: 11px;
      padding: 10px 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }
    html[data-theme="light"] .ag-d3-node {
      background: #ffffff;
    }
    .ag-d3-hub {
      background: var(--bg-card);
      border: 2px solid #2563eb;
      border-radius: 18px;
      padding: 16px;
      box-shadow: 0 8px 24px rgba(37, 99, 235, 0.08);
    }
    html[data-theme="light"] .ag-d3-hub {
      background: #ffffff;
    }
    .ag-d3-stage-pill {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 11px;
      border-radius: 10px;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      font-size: 12px;
      font-weight: 700;
      color: var(--text-primary);
    }
"""

PROTO_JS = """
    window.agentFlowProtoMode = window.agentFlowProtoMode || 'd1';

    window.setAgentFlowProtoMode = function(mode, agentId) {
      window.agentFlowProtoMode = mode;
      openAgentPage(agentId || 'port_drayage_orchestrator', false);
    };

    function renderCurfewFlowPrototype(ag, dept, legacySvgHtml) {
      const mode = window.agentFlowProtoMode || 'd1';
      const cleanName = cleanAgentName(ag.name);

      const switcherHtml = `
        <div class="ag-proto-SegBar" role="tablist" aria-label="Execution Flow Design Options">
          <button type="button" class="ag-proto-btn ${mode === 'd1' ? 'is-active' : ''}" onclick="setAgentFlowProtoMode('d1', '${ag.id}')">
            1 · Refined Blueprint
          </button>
          <button type="button" class="ag-proto-btn ${mode === 'd2' ? 'is-active' : ''}" onclick="setAgentFlowProtoMode('d2', '${ag.id}')">
            2 · Live Data Trace
          </button>
          <button type="button" class="ag-proto-btn ${mode === 'd3' ? 'is-active' : ''}" onclick="setAgentFlowProtoMode('d3', '${ag.id}')">
            3 · Minimal Signal Map
          </button>
          <button type="button" class="ag-proto-btn ${mode === 'legacy' ? 'is-active' : ''}" onclick="setAgentFlowProtoMode('legacy', '${ag.id}')">
            Original (Before)
          </button>
        </div>
      `;

      const arrowSvg = (col) => `
        <div class="ag-d1-conn">
          <svg viewBox="0 0 28 60" width="28" height="60" fill="none">
            <line x1="2" y1="30" x2="22" y2="30" stroke="${col}" stroke-width="2.2" stroke-dasharray="4 3"/>
            <path d="M18 24L25 30L18 36" stroke="${col}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
      `;

      let bodyHtml = '';

      if (mode === 'd1') {
        // DESIGN 1: Keeps the exact 4-column visual DNA the user liked, zero truncation, real system & table names!
        bodyHtml = `
          <div class="ag-ef-shell">
            <div class="ag-d1-grid">
              <!-- COL 1: 2 Concrete Input Systems -->
              <div class="ag-d1-col-stack">
                <div class="ag-d1-card" style="--card-bdr:#05966988; flex:1;">
                  <div class="ag-d1-kicker" style="--kicker-col:#059669;">
                    <svg viewBox="0 0 20 20" width="14" height="14" fill="none"><circle cx="10" cy="10" r="3" fill="currentColor"/><path d="M4.5 10a5.5 5.5 0 0 1 11 0M2 10a8 8 0 0 1 16 0" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
                    1A · LIVE FLEET &amp; CITY RULES
                  </div>
                  <div class="ag-d1-title">Samsara GPS + City Curfew GIS</div>
                  <div style="display:flex; flex-wrap:wrap; gap:5px;">
                    <span class="ag-d1-meta-chip">truck_eta: 5m stream</span>
                    <span class="ag-d1-meta-chip">quiet_zone: 22:00–06:00</span>
                  </div>
                </div>

                <div class="ag-d1-card" style="--card-bdr:#0284c788; flex:1;">
                  <div class="ag-d1-kicker" style="--kicker-col:#0284c7;">
                    <svg viewBox="0 0 20 20" width="14" height="14" fill="none"><rect x="3" y="4" width="14" height="12" rx="2" stroke="currentColor" stroke-width="1.7"/><path d="M3 8.5h14M8 8.5V16" stroke="currentColor" stroke-width="1.5"/></svg>
                    1B · TMS &amp; STORE DOCK ERP
                  </div>
                  <div class="ag-d1-title">Blue Yonder TMS + Manhattan WMS</div>
                  <div style="display:flex; flex-wrap:wrap; gap:5px;">
                    <span class="ag-d1-meta-chip">bay_doors</span>
                    <span class="ag-d1-meta-chip">store_crew_shifts</span>
                  </div>
                </div>
              </div>

              ${arrowSvg('#0284c7')}

              <!-- COL 2: Actual Connected Tables & Keys (Zero Boilerplate Prose) -->
              <div class="ag-d1-card" style="--card-bdr:#0284c7;">
                <div>
                  <div class="ag-d1-kicker" style="--kicker-col:#0284c7; margin-bottom:6px;">
                    <svg viewBox="0 0 20 20" width="14" height="14" fill="none"><ellipse cx="10" cy="5" rx="6.5" ry="2.5" stroke="currentColor" stroke-width="1.7"/><path d="M3.5 5v10c0 1.4 2.9 2.5 6.5 2.5s6.5-1.1 6.5-2.5V5M3.5 10c0 1.4 2.9 2.5 6.5 2.5s6.5-1.1 6.5-2.5" stroke="currentColor" stroke-width="1.7"/></svg>
                    2 · LIVE DATA JOIN (4 TABLES)
                  </div>
                  <div class="ag-d1-title">Curfew &amp; Dock State Correlator</div>
                </div>

                <div class="ag-d1-tbl-list">
                  <div class="ag-d1-tbl-row">
                    <span class="ag-d1-tbl-name">store_curfew_rules</span>
                    <span class="ag-d1-tbl-key">max_dB · fine_$</span>
                  </div>
                  <div class="ag-d1-tbl-row">
                    <span class="ag-d1-tbl-name">dock_shift_rosters</span>
                    <span class="ag-d1-tbl-key">bay_id · crew_out</span>
                  </div>
                  <div class="ag-d1-tbl-row">
                    <span class="ag-d1-tbl-name">fleet_tractor_etas</span>
                    <span class="ag-d1-tbl-key">ev_quiet · eta_utc</span>
                  </div>
                  <div class="ag-d1-tbl-row">
                    <span class="ag-d1-tbl-name">backroom_pallet_cap</span>
                    <span class="ag-d1-tbl-key">free_slots · risk</span>
                  </div>
                </div>

                <div class="ag-d1-meta-chip" style="width:100%; justify-content:center; color:#059669; border-color:rgba(5,150,105,0.3);">
                  ✓ Deterministic SQL Join · 0 Hallucination
                </div>
              </div>

              ${arrowSvg('#2563eb')}

              <!-- COL 3: Domain-Accurate Visual Solver Card -->
              <div class="ag-d1-card" style="--card-bdr:#2563eb;">
                <div>
                  <div class="ag-d1-kicker" style="--kicker-col:#2563eb; margin-bottom:5px;">
                    <svg viewBox="0 0 20 20" width="14" height="14" fill="none"><rect x="3" y="3" width="14" height="14" rx="3.5" stroke="currentColor" stroke-width="1.7"/><circle cx="10" cy="10" r="2.5" fill="currentColor"/></svg>
                    3 · CURFEW &amp; DOCK WINDOW SOLVER
                  </div>
                  <div class="ag-d1-title">Quiet-Tractor &amp; Slot Re-Sequencer</div>
                </div>

                <!-- Clean Domain Graphic: Diesel Blocked at 22:00 Quiet Zone -> Swapped to Quiet EV Tractor -->
                <div class="ag-d1-viz-box">
                  <svg viewBox="0 0 300 104" width="100%" height="104" style="display:block;">
                    <!-- Timeline Header -->
                    <line x1="10" y1="18" x2="290" y2="18" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="3 2"/>
                    <text x="12" y="12" fill="#64748b" font-size="9.5" font-weight="800" font-family="var(--font-mono)">20:30</text>
                    <text x="166" y="12" fill="#e11d48" font-size="9.5" font-weight="800" font-family="var(--font-mono)">22:00 CURFEW (&gt;65dB)</text>
                    <line x1="162" y1="18" x2="162" y2="98" stroke="#e11d48" stroke-width="1.5" stroke-dasharray="3 2"/>

                    <!-- Row 1: Diesel Blocked -->
                    <rect x="12" y="27" width="142" height="26" rx="6" fill="rgba(225,29,72,0.10)" stroke="#e11d48" stroke-width="1.3"/>
                    <text x="83" y="44" text-anchor="middle" fill="#e11d48" font-size="9.5" font-weight="800" font-family="var(--font-mono)">✕ Diesel #TR-409 (22:18)</text>
                    <rect x="168" y="27" width="120" height="26" rx="6" fill="rgba(225,29,72,0.06)" stroke="rgba(225,29,72,0.45)" stroke-width="1.1" stroke-dasharray="3 2"/>
                    <text x="228" y="44" text-anchor="middle" fill="#e11d48" font-size="9" font-weight="800" font-family="var(--font-mono)">$2,500 FINE ZONE</text>

                    <!-- Row 2: Legal EV Swap -->
                    <path d="M 83 53 L 83 75 L 116 75" fill="none" stroke="#059669" stroke-width="2" stroke-linecap="round"/>
                    <rect x="116" y="62" width="172" height="28" rx="6" fill="rgba(16,185,129,0.14)" stroke="#059669" stroke-width="1.5"/>
                    <text x="202" y="80" text-anchor="middle" fill="#059669" font-size="9.5" font-weight="800" font-family="var(--font-mono)">✓ EV #112 (&lt;58dB) · Bay #2</text>
                  </svg>
                </div>

                <div class="ag-d1-pill-pair">
                  <span class="ag-d1-spec-pill">OR-Tools CP-SAT</span>
                  <span class="ag-d1-spec-pill">Gemini 3.8 Flash · 3.1 Pro</span>
                </div>
              </div>

              ${arrowSvg('#059669')}

              <!-- COL 4: Policy Gate + Concrete Write-Back + KPI -->
              <div class="ag-d1-card" style="--card-bdr:#059669;">
                <div>
                  <div class="ag-d1-kicker" style="--kicker-col:#059669; margin-bottom:5px;">
                    <svg viewBox="0 0 20 20" width="14" height="14" fill="none"><path d="M11 2.5L4.5 11h5l-.7 6.5L15.5 9h-5l.5-6.5z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>
                    4 · GOVERNED WRITE-BACK
                  </div>
                  <div class="ag-d1-title">Blue Yonder TMS &amp; Store Dock</div>
                  <div style="font-size:11.5px; color:var(--text-secondary); font-weight:600; margin-top:2px;">
                    Owner: Retail Logistics Dispatcher
                  </div>
                </div>

                <div class="ag-d1-gate-box">
                  <div style="font-family:var(--font-mono); font-size:10.5px; font-weight:800; color:#d97706;">POLICY GATE</div>
                  <div style="color:var(--text-primary); font-weight:700; margin-top:2px;">Auto ≤30m shift · Escalate &gt;$500</div>
                </div>

                <div class="ag-d1-out-box">
                  <div style="font-family:var(--font-mono); font-size:10.5px; font-weight:800; color:#059669;">action_rebook_store_slot()</div>
                  <div style="font-weight:800; color:var(--text-primary); font-size:13px; margin-top:2px;">-80% Curfew &amp; Slot Penalties</div>
                  <div style="font-size:11px; color:var(--text-secondary); margin-top:2px;">98.4% On-Time Window · A2UI Chart</div>
                </div>
              </div>
            </div>
          </div>
        `;
      } else if (mode === 'd2') {
        // DESIGN 2: Live Single-Case Operational Storyboard (Concrete IDs & Numbers, Zero Abstract Jargon)
        bodyHtml = `
          <div class="ag-ef-shell">
            <div class="ag-d2-banner">
              <span>LIVE SAMPLE RUN · <strong style="color:var(--text-primary);">Store #104 (Urban Quiet Zone)</strong> · Load <strong style="color:var(--text-primary);">#STO-88412</strong></span>
              <span style="color:#059669;">End-to-End Resolution: 1.4 sec</span>
            </div>

            <div class="ag-d2-grid">
              <!-- Step 1: Real Trigger -->
              <div class="ag-d2-step" style="--step-col:#e11d48;">
                <div>
                  <div class="ag-d1-kicker" style="--kicker-col:#e11d48; margin-bottom:6px;">01 · LIVE EXCEPTION DETECTED</div>
                  <div class="ag-d1-title">Curfew Breach in 42 Mins</div>
                </div>
                <div style="display:flex; flex-direction:column; gap:6px;">
                  <div class="ag-d2-kv"><span>Source</span><strong>Samsara GPS</strong></div>
                  <div class="ag-d2-kv"><span>Tractor #TR-409</span><strong style="color:#e11d48;">ETA 22:18 (+38m)</strong></div>
                  <div class="ag-d2-kv"><span>City Curfew</span><strong>22:00 (&gt;65 dB Ban)</strong></div>
                  <div class="ag-d2-kv"><span>Penalty Risk</span><strong style="color:#e11d48;">$2,500 + Refused</strong></div>
                </div>
              </div>

              <!-- Step 2: Real Table Lookup -->
              <div class="ag-d2-step" style="--step-col:#0284c7;">
                <div>
                  <div class="ag-d1-kicker" style="--kicker-col:#0284c7; margin-bottom:6px;">02 · TABLES QUERIED</div>
                  <div class="ag-d1-title">Dock &amp; Quiet-Fleet Check</div>
                </div>
                <div style="display:flex; flex-direction:column; gap:6px;">
                  <div class="ag-d2-kv"><span>dock_shift_rosters</span><strong>Bay #2 till 23:00</strong></div>
                  <div class="ag-d2-kv"><span>store_curfew_rules</span><strong>EV &lt;58 dB Exempt</strong></div>
                  <div class="ag-d2-kv"><span>fleet_tractor_etas</span><strong style="color:#0284c7;">#EV-112 (9 km out)</strong></div>
                  <div class="ag-d2-kv"><span>backroom_pallet_cap</span><strong>18 Pallets Free</strong></div>
                </div>
              </div>

              <!-- Step 3: Solver Trade-Off -->
              <div class="ag-d2-step" style="--step-col:#2563eb;">
                <div>
                  <div class="ag-d1-kicker" style="--kicker-col:#2563eb; margin-bottom:6px;">03 · CP-SAT + GEMINI SOLVE</div>
                  <div class="ag-d1-title">Optimal Swap Selected</div>
                </div>
                <div style="display:flex; flex-direction:column; gap:6px;">
                  <div class="ag-d2-kv" style="opacity:0.7;"><span>Option A · Hold AM</span><strong>Stockout -$4.2K</strong></div>
                  <div class="ag-d2-kv" style="border:1.5px solid #059669; background:rgba(16,185,129,0.08);">
                    <span style="color:#059669; font-weight:800;">✓ Option B · EV Swap</span>
                    <strong style="color:#059669;">+$140 · $0 Fine</strong>
                  </div>
                  <div class="ag-d2-kv"><span>Solver</span><strong>OR-Tools CP-SAT</strong></div>
                  <div class="ag-d2-kv"><span>Reasoning</span><strong>Gemini 3.8 Flash</strong></div>
                </div>
              </div>

              <!-- Step 4: Write-Back Receipt -->
              <div class="ag-d2-step" style="--step-col:#059669;">
                <div>
                  <div class="ag-d1-kicker" style="--kicker-col:#059669; margin-bottom:6px;">04 · AUTO-COMMITTED</div>
                  <div class="ag-d1-title">TMS &amp; Store Bay Updated</div>
                </div>
                <div style="display:flex; flex-direction:column; gap:6px;">
                  <div class="ag-d2-kv"><span>Policy Gate</span><strong style="color:#d97706;">$140 &lt; $500 Limit</strong></div>
                  <div class="ag-d2-kv"><span>Blue Yonder TMS</span><strong>#DSP-9921 Swapped</strong></div>
                  <div class="ag-d2-kv"><span>Store #104 WMS</span><strong>Bay #2 · 22:10 EV</strong></div>
                  <div class="ag-d2-kv"><span>Verified Impact</span><strong style="color:#059669;">$2,500 Fine Saved</strong></div>
                </div>
              </div>
            </div>
          </div>
        `;
      } else if (mode === 'd3') {
        // DESIGN 3: Ultra-Minimal Technical I/O Signal Map (Zero Sentences, Labeled Data Wires)
        bodyHtml = `
          <div class="ag-ef-shell">
            <div class="ag-d3-layout">
              <!-- Left: Concrete Input Feeds -->
              <div class="ag-d3-stack">
                <div class="ag-d1-kicker" style="--kicker-col:#64748b; padding-left:4px;">INPUT FEEDS (MCP / API)</div>
                <div class="ag-d3-node" style="--nd-col:#059669;">
                  <div>
                    <div style="font-weight:800; font-size:13px; color:var(--text-primary);">Samsara Fleet GPS</div>
                    <div style="font-family:var(--font-mono); font-size:10.5px; color:var(--text-secondary);">tractor_id · eta_utc · dB_rating</div>
                  </div>
                  <span class="ag-d1-meta-chip">gRPC</span>
                </div>
                <div class="ag-d3-node" style="--nd-col:#0284c7;">
                  <div>
                    <div style="font-weight:800; font-size:13px; color:var(--text-primary);">City Curfew GIS</div>
                    <div style="font-family:var(--font-mono); font-size:10.5px; color:var(--text-secondary);">zone_ordinance · quiet_hours</div>
                  </div>
                  <span class="ag-d1-meta-chip">REST</span>
                </div>
                <div class="ag-d3-node" style="--nd-col:#7c3aed;">
                  <div>
                    <div style="font-weight:800; font-size:13px; color:var(--text-primary);">Manhattan Store WMS</div>
                    <div style="font-family:var(--font-mono); font-size:10.5px; color:var(--text-secondary);">bay_availability · crew_shift</div>
                  </div>
                  <span class="ag-d1-meta-chip">CDC</span>
                </div>
              </div>

              <!-- Left Wires -->
              <div class="ag-d3-wires" style="display:flex; justify-content:center;">
                <svg viewBox="0 0 48 170" width="48" height="170" fill="none">
                  <path d="M2 34 C 24 34, 24 85, 44 85" stroke="#059669" stroke-width="2" stroke-dasharray="4 3"/>
                  <path d="M2 85 L 44 85" stroke="#0284c7" stroke-width="2" stroke-dasharray="4 3"/>
                  <path d="M2 136 C 24 136, 24 85, 44 85" stroke="#7c3aed" stroke-width="2" stroke-dasharray="4 3"/>
                  <circle cx="44" cy="85" r="3.5" fill="#2563eb"/>
                </svg>
              </div>

              <!-- Center: 3-Sub-Agent Brain -->
              <div class="ag-d3-hub">
                <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:10px;">
                  <span class="ag-d1-kicker" style="--kicker-col:#2563eb;">AGENTIC CORE · ADK + A2A</span>
                  <span class="ag-d1-spec-pill">Gemini 3.8 Flash + OR-Tools</span>
                </div>
                <div style="display:flex; flex-direction:column; gap:8px;">
                  <div class="ag-d3-stage-pill">
                    <span>1. Curfew Conflict Detector</span>
                    <span style="font-family:var(--font-mono); font-size:10.5px; color:#0284c7;">4 BQ Tables</span>
                  </div>
                  <div class="ag-d3-stage-pill" style="border-color:rgba(37,99,235,0.4);">
                    <span>2. Quiet-Fleet &amp; Bay CP-SAT Solver</span>
                    <span style="font-family:var(--font-mono); font-size:10.5px; color:#2563eb;">Optimal Slot</span>
                  </div>
                  <div class="ag-d3-stage-pill" style="border-color:rgba(245,158,11,0.4);">
                    <span>3. Policy Gate Verifier</span>
                    <span style="font-family:var(--font-mono); font-size:10.5px; color:#d97706;">Auto ≤$500</span>
                  </div>
                </div>
              </div>

              <!-- Right Wires -->
              <div class="ag-d3-wires" style="display:flex; justify-content:center;">
                <svg viewBox="0 0 48 140" width="48" height="140" fill="none">
                  <path d="M4 70 C 24 70, 24 40, 44 40" stroke="#059669" stroke-width="2.2"/>
                  <path d="M4 70 C 24 70, 24 102, 44 102" stroke="#0284c7" stroke-width="2.2"/>
                  <polygon points="44,40 38,36 38,44" fill="#059669"/>
                  <polygon points="44,102 38,98 38,106" fill="#0284c7"/>
                </svg>
              </div>

              <!-- Right: Concrete Write-Backs & KPI -->
              <div class="ag-d3-stack">
                <div class="ag-d1-kicker" style="--kicker-col:#059669; padding-left:4px;">WRITE-BACK &amp; KPI</div>
                <div class="ag-d3-node" style="--nd-col:#059669;">
                  <div>
                    <div style="font-weight:800; font-size:13px; color:var(--text-primary);">Blue Yonder TMS</div>
                    <div style="font-family:var(--font-mono); font-size:10.5px; color:#059669;">action_rebook_store_slot()</div>
                  </div>
                  <span class="ag-d1-meta-chip">EDI 204</span>
                </div>
                <div class="ag-d3-node" style="--nd-col:#0284c7;">
                  <div>
                    <div style="font-weight:800; font-size:13px; color:var(--text-primary);">Retail Dispatcher Console</div>
                    <div style="font-family:var(--font-mono); font-size:10.5px; color:var(--text-secondary);">A2UI VegaChart + Dock Alert</div>
                  </div>
                  <span class="ag-d1-meta-chip">A2UI</span>
                </div>
                <div style="padding:9px 12px; border-radius:11px; background:rgba(16,185,129,0.12); border:1px solid rgba(16,185,129,0.4); display:flex; align-items:center; justify-content:space-between;">
                  <span style="font-size:11.5px; font-weight:800; color:#059669;">VERIFIED OUTCOME</span>
                  <span style="font-family:var(--font-mono); font-size:12px; font-weight:800; color:var(--text-primary);">-80% Curfew Penalties</span>
                </div>
              </div>
            </div>
          </div>
        `;
      } else {
        bodyHtml = legacySvgHtml;
      }

      return `
        <div class="simple-arch-card">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:14px;">
            <div>
              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:4px;">
                <span style="font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color};">
                  05 · Store Replenishment · Event-Driven + 5-Min GPS
                </span>
              </div>
              <h2 style="font-family:var(--font-display); font-size:24px; font-weight:800; color:var(--text-primary); margin:0;">
                Execution Flow — ${cleanName}
              </h2>
            </div>
            ${switcherHtml}
          </div>
          ${bodyHtml}
        </div>
      `;
    }
"""


def main() -> None:
    idx_path = ROOT / "index.html"
    html = idx_path.read_text(encoding="utf-8")

    # Idempotently strip prior v2.6 injection if re-run
    if "/* === V2.6 EXECUTION FLOW PROTOTYPES" in html:
        s = html.index("/* === V2.6 EXECUTION FLOW PROTOTYPES")
        e = html.index("</style>", s)
        html = html[:s] + html[e:]

    if "window.agentFlowProtoMode =" in html:
        s = html.index("window.agentFlowProtoMode =")
        e = html.index("function renderSimpleAgentArchitectureDiagram(ag, dept)", s)
        html = html[:s] + html[e:]

    # 1. Inject CSS before closing </style>
    first_style_close = html.index("</style>")
    html = html[:first_style_close] + PROTO_CSS + "\n  " + html[first_style_close:]

    # 2. Inject JS helper right before renderSimpleAgentArchitectureDiagram
    target_fn = "    function renderSimpleAgentArchitectureDiagram(ag, dept) {"
    assert target_fn in html, "renderSimpleAgentArchitectureDiagram not found!"
    html = html.replace(target_fn, PROTO_JS + "\n" + target_fn, 1)

    # 3. Hook Curfew Orchestrator (`port_drayage_orchestrator`) inside renderSimpleAgentArchitectureDiagram
    old_return = """      return `
        <div class="simple-arch-card">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:14px;">
            <div>
              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:4px;">
                <span style="font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color};">
                  ${tMeta.badge}
                </span>
                <span class="sc-spec-count-badge" style="font-size:11px;">
                  ⏱️ ${cadence}
                </span>
              </div>
              <h2 style="font-family:var(--font-display); font-size:24px; font-weight:800; color:var(--text-primary); margin:0;">
                Execution Flow — ${cleanName}
              </h2>
            </div>

            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="sc-spec-count-badge" style="color:#10b981; border-color:rgba(16,185,129,0.35);">
                🔌 BigQuery · On-Prem DBs · 3rd-Party MCPs · REST/EDI
              </span>
            </div>
          </div>

          <!-- Custom Agent-Specific Animated Full-Canvas SVG Flow Diagram -->
          <div class="ag-flow-canvas-wrap">
            <svg class="ag-flow-svg" viewBox="0 0 1120 288">
              <defs>
                <marker id="arrowAccent_${ag.id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 1 L 10 5 L 0 9 z" fill="${dept.color}" />
                </marker>
                <marker id="arrowGreen_${ag.id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 1 L 10 5 L 0 9 z" fill="#10b981" />
                </marker>
                <marker id="arrowCyan_${ag.id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8" />
                </marker>
              </defs>
              ${svgBody}
            </svg>
          </div>

        </div>
      `;"""

    new_return = """      const legacySvgWrap = `
          <div class="ag-flow-canvas-wrap">
            <svg class="ag-flow-svg" viewBox="0 0 1120 288">
              <defs>
                <marker id="arrowAccent_${ag.id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 1 L 10 5 L 0 9 z" fill="${dept.color}" />
                </marker>
                <marker id="arrowGreen_${ag.id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 1 L 10 5 L 0 9 z" fill="#10b981" />
                </marker>
                <marker id="arrowCyan_${ag.id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8" />
                </marker>
              </defs>
              ${svgBody}
            </svg>
          </div>
      `;

      if (ag.id === 'port_drayage_orchestrator') {
        return renderCurfewFlowPrototype(ag, dept, legacySvgWrap);
      }

      return `
        <div class="simple-arch-card">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:14px;">
            <div>
              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:4px;">
                <span style="font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color};">
                  ${tMeta.badge}
                </span>
                <span class="sc-spec-count-badge" style="font-size:11px;">
                  ⏱️ ${cadence}
                </span>
              </div>
              <h2 style="font-family:var(--font-display); font-size:24px; font-weight:800; color:var(--text-primary); margin:0;">
                Execution Flow — ${cleanName}
              </h2>
            </div>

            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="sc-spec-count-badge" style="color:#10b981; border-color:rgba(16,185,129,0.35);">
                🔌 BigQuery · On-Prem DBs · 3rd-Party MCPs · REST/EDI
              </span>
            </div>
          </div>

          ${legacySvgWrap}

        </div>
      `;"""

    if old_return in html:
        html = html.replace(old_return, new_return, 1)

    idx_path.write_text(html, encoding="utf-8")

    # Sync derived HTML files
    pt_boot = """
  <script>
    window.addEventListener('DOMContentLoaded', function() {
      if (!window.location.hash || window.location.hash === '#home') {
        if (typeof openPeriodicTablePage === 'function') openPeriodicTablePage('all', null, false);
      }
    });
  </script>
</body>"""
    mm_boot = """
  <script>
    window.addEventListener('DOMContentLoaded', function() {
      if (!window.location.hash || window.location.hash === '#home') {
        if (typeof openMindMapPage === 'function') openMindMapPage('mindmap', null, null, false);
      }
    });
  </script>
</body>"""
    (ROOT / "periodic_table.html").write_text(html.replace("</body>", pt_boot, 1), encoding="utf-8")
    (ROOT / "mind_map.html").write_text(html.replace("</body>", mm_boot, 1), encoding="utf-8")

    for target_dir in [ROOT / "docs", ROOT / "zipline_dist"]:
        if target_dir.exists():
            for fname in ["index.html", "periodic_table.html", "mind_map.html"]:
                shutil.copy2(ROOT / fname, target_dir / fname)

    print("✅ Injected 3 Execution Flow design prototypes onto Curfew Orchestrator (`port_drayage_orchestrator`)!")


if __name__ == "__main__":
    main()

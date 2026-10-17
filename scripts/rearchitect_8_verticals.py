#!/usr/bin/env python3
"""
Rearchitect build_site.py to implement:
1. The 8 Operational Verticals (Level-1 to Level-3 decomposition)
2. High-contrast, responsive front-page tabs to see and filter all 8 verticals
3. Three Rivers Flow banner
4. Live Interactive Safety Stock & ROP Calculator
5. 5-Step S&OP Cadence Timeline
6. Updated Architecture, Directory, Periodic Table & Mind Map views
"""
import re
import sys
from pathlib import Path

ROOT = Path("/usr/local/google/home/zuhaibp/Supply_chain_Agentic_Transformation")
BUILD_SITE_PATH = ROOT / "build_site.py"

def main():
    content = BUILD_SITE_PATH.read_text(encoding="utf-8")

    # 1. Update CSS: .dept-row grid-template-columns and animation delays
    old_dept_row_css = """    .dept-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      width: 100%;
    }

    @media (max-width: 980px) {
      .dept-row { grid-template-columns: repeat(2, 1fr); }
      .org-connectors { display: none; }
      .cfo-box { margin-bottom: 28px; }
    }
    @media (max-width: 600px) {
      .dept-row { grid-template-columns: 1fr; }
    }"""

    new_dept_row_css = """    .dept-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
      width: 100%;
    }

    @media (max-width: 1280px) {
      .dept-row { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 680px) {
      .dept-row { grid-template-columns: 1fr; }
      .org-connectors { display: none; }
      .cfo-box { margin-bottom: 28px; }
    }

    /* Three Rivers Flow Architecture Banner */
    .rivers-banner {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin: 28px 0 32px;
      width: 100%;
    }
    @media (max-width: 900px) {
      .rivers-banner { grid-template-columns: 1fr; }
    }
    .river-box {
      background: linear-gradient(165deg, rgba(16, 26, 46, 0.88) 0%, rgba(9, 14, 26, 0.94) 100%);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 14px;
      padding: 18px 20px;
      border-left: 4px solid #38bdf8;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
      position: relative;
      overflow: hidden;
      transition: transform 0.25s ease, border-color 0.25s ease;
    }
    .river-box:hover {
      transform: translateY(-2px);
      border-color: rgba(255, 255, 255, 0.22);
    }
    .river-box.signal { border-left-color: #f472b6; }
    .river-box.cash { border-left-color: #10b981; }
    .river-box h4 {
      font-size: 14.5px;
      font-weight: 800;
      color: #fff;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .river-box p {
      font-size: 13px;
      color: #94a3b8;
      line-height: 1.58;
    }

    /* 8-Vertical Interactive Master Navigation Tab Bar on Front Page */
    .vertical-tabs-nav-bar {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 10px;
      padding: 14px 18px;
      background: rgba(9, 14, 25, 0.92);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 20px;
      margin: 18px 0 34px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.45);
      position: sticky;
      top: 68px;
      z-index: 95;
    }
    .v-tab-btn {
      background: rgba(18, 28, 48, 0.85);
      color: #94a3b8;
      border: 1.5px solid rgba(255, 255, 255, 0.1);
      padding: 10px 16px;
      border-radius: 12px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.26s var(--ease-spring);
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 3px;
      text-align: left;
      min-width: 140px;
      position: relative;
    }
    .v-tab-btn:hover {
      background: rgba(28, 44, 72, 0.95);
      color: #fff;
      border-color: var(--v-accent, #38bdf8);
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
    }
    .v-tab-btn.active {
      background: linear-gradient(145deg, rgba(22, 38, 64, 0.98), rgba(12, 20, 36, 0.98));
      color: #fff;
      border-color: var(--v-accent, #38bdf8);
      box-shadow: 0 0 22px rgba(56, 189, 248, 0.28), inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    .v-tab-btn .v-tab-num {
      font-size: 10.5px;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--v-accent, #38bdf8);
    }
    .v-tab-btn .v-tab-title {
      font-size: 13px;
      font-weight: 800;
      color: #fff;
      white-space: nowrap;
    }
    .v-tab-btn .v-tab-tag {
      font-size: 11px;
      font-weight: 500;
      color: #94a3b8;
    }
    .v-tab-btn.active .v-tab-tag {
      color: #cbd5e1;
    }
    .v-tab-btn .v-tab-badge {
      font-size: 10px;
      font-weight: 600;
      color: #64748b;
      margin-top: 2px;
    }

    /* 4-Quadrant Level-1 to Level-3 Decomposition Grid inside Showcase */
    .quad-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
      margin: 20px 0;
      width: 100%;
    }
    .quad-card {
      background: rgba(14, 22, 38, 0.95);
      border: 1px solid rgba(255, 255, 255, 0.09);
      border-radius: 14px;
      padding: 18px 20px;
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
    }
    .quad-card h5 {
      font-size: 12.5px;
      font-weight: 800;
      color: var(--dept-accent, #38bdf8);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .quad-card ul {
      list-style: none;
      padding: 0;
      margin: 0;
    }
    .quad-card li {
      font-size: 13px;
      color: #cbd5e1;
      margin-bottom: 8px;
      padding-left: 16px;
      position: relative;
      line-height: 1.52;
    }
    .quad-card li::before {
      content: "▸";
      position: absolute;
      left: 0;
      color: var(--dept-accent, #38bdf8);
      font-weight: 700;
    }

    /* Interactive Multi-Echelon Safety Stock & ROP Calculator */
    .ss-calc-card {
      background: linear-gradient(165deg, rgba(14, 24, 42, 0.96) 0%, rgba(8, 14, 26, 0.98) 100%);
      border: 1px solid rgba(56, 189, 248, 0.28);
      border-radius: 20px;
      padding: 28px;
      margin: 36px 0 20px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
    }
    .ss-calc-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 20px;
    }
    .ss-calc-title {
      font-size: 20px;
      font-weight: 800;
      color: #fff;
    }
    .ss-calc-sub {
      font-size: 13.5px;
      color: #94a3b8;
      margin-top: 4px;
    }
    .control-row {
      display: flex;
      align-items: center;
      gap: 24px;
      flex-wrap: wrap;
      margin: 20px 0;
    }
    .control-field {
      flex: 1;
      min-width: 240px;
    }
    .control-field label {
      display: block;
      font-size: 12.5px;
      font-weight: 600;
      color: #94a3b8;
      margin-bottom: 6px;
    }
    .control-field input[type="range"] {
      width: 100%;
      accent-color: #38bdf8;
      cursor: pointer;
    }
    .ss-output-box {
      background: #060a12;
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 14px;
      padding: 20px;
      font-size: 14px;
      margin-top: 14px;
    }
    .bar-line { margin: 14px 0 6px; }
    .bar-meta { display: flex; justify-content: space-between; font-size: 12.5px; margin-bottom: 6px; color: #94a3b8; }
    .bar-outer {
      width: 100%;
      height: 24px;
      background: #090e17;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.1);
      overflow: hidden;
    }
    .bar-inner {
      height: 100%;
      background: linear-gradient(90deg, #38bdf8, #ec4899);
      transition: width 0.35s ease;
    }

    /* 5-Step S&OP Cadence Table */
    .sop-table-wrap {
      width: 100%;
      overflow-x: auto;
      margin: 24px 0;
      border-radius: 14px;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .sop-cadence-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13.5px;
      background: rgba(10, 16, 28, 0.95);
    }
    .sop-cadence-table th {
      background: #080d18;
      color: #38bdf8;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 12px 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      text-align: left;
    }
    .sop-cadence-table td {
      padding: 12px 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.07);
      color: #cbd5e1;
    }
    .sop-cadence-table tr:hover td {
      background: rgba(255, 255, 255, 0.03);
    }"""

    if old_dept_row_css in content:
        content = content.replace(old_dept_row_css, new_dept_row_css, 1)
        print("Updated .dept-row CSS & added Three Rivers banner, tabs, quad-grid & calculator CSS.")
    else:
        print("Warning: old_dept_row_css not matched verbatim, skipping CSS replace")

    # Add animation delays for nth-child(7) and nth-child(8) in .dept-row
    old_nth6 = ".dept-row > :nth-child(6), .catalog-grid > :nth-child(6), .dir-persona-grid > :nth-child(6), .day-schedule > :nth-child(6) { animation-delay: 0.22s; }"
    new_nth = old_nth6 + "\n    .dept-row > :nth-child(7) { animation-delay: 0.25s; }\n    .dept-row > :nth-child(8) { animation-delay: 0.28s; }"
    if old_nth6 in content:
        content = content.replace(old_nth6, new_nth, 1)
        print("Added animation delays for children 7 and 8.")

    # 2. Update HTML of #orgChartSection
    old_org_section_header = """    <!-- 2. CSCO ORG CHART (PROGRESSIVE ONE-BY-ONE EXPLORATION ACROSS 6 SCOR VERTICALS) -->
    <section id="orgChartSection" class="org-section">
      <div class="section-header">
        <h2 class="section-title">Office of the CSCO — 6 SCOR Supply Chain Verticals</h2>
        <p class="section-subtitle">Aligned to the global <span class="sc-hl-underline">ASCM SCOR DS</span> taxonomy (<strong class="sc-hl-bold">Plan · Source · Make · Fulfill: Warehouse · Deliver: Ocean/Air/Rail/Road Fleet · Return &amp; Enable</strong>) — delivering <span class="sc-hl-metric">zero-toil execution</span>, <span class="sc-hl-underline">deterministic math optimization</span>, and verified <strong class="sc-hl-bold">bottom-line ROI</strong> across <span class="sc-hl-metric">26 roles</span>.</p>
      </div>"""

    new_org_section_header = """    <!-- 2. CSCO ORG CHART (PROGRESSIVE EXPLORATION ACROSS THE 8 OPERATIONAL VERTICALS) -->
    <section id="orgChartSection" class="org-section">
      <div class="section-header">
        <h2 class="section-title">Office of the CSCO — The 8 Operational Verticals</h2>
        <p class="section-subtitle">The End-to-End Operating Topology decomposed from <span class="sc-hl-underline">Level-1 to Level-3</span> across the <strong class="sc-hl-bold">Three Rivers Flow</strong> (Physical Material Flow, Demand/Information Flow, Cash/Working Capital Flow) — powered by deterministic math solvers and Gemini Enterprise agentic orchestration.</p>
      </div>

      <!-- Three Rivers Flow Architecture Banner -->
      <div class="rivers-banner">
        <div class="river-box">
          <h4>🌊 River 1: Physical Material Flow (Downstream ──▶)</h4>
          <p>Raw Materials / Agri Nodes ──▶ Factory WIP ──▶ Mother Warehouses ──▶ Regional Depots ──▶ Distributors ──▶ Retail Shelf / Kirana.</p>
        </div>
        <div class="river-box signal">
          <h4>📡 River 2: Demand &amp; Information Flow (◀── Upstream)</h4>
          <p>Consumer POS Scans ◀── FSO Beat Orders ◀── DMS Inventory ◀── S&amp;OP Consensus Forecast ◀── MRP BOM Explosion ◀── Vendor POs.</p>
        </div>
        <div class="river-box cash">
          <h4>💰 River 3: Cash &amp; Working Capital Flow (◀──▶ Cyclic)</h4>
          <p>Cash Conversion Cycle = Days Inventory (DIO) + Receivables (DSO) − Payables (DPO). Every excess day of dead stock locks corporate liquidity.</p>
        </div>
      </div>

      <!-- 8-Vertical Interactive Master Navigation Tab Bar on the Front Page -->
      <div class="vertical-tabs-nav-bar" id="verticalTabsNavBar">
        <button type="button" class="v-tab-btn active" data-vtab="all" onclick="switchVerticalTab('all', this)">
          <span class="v-tab-num" style="color:#38bdf8;">ALL 8</span>
          <span class="v-tab-title">All Verticals</span>
          <span class="v-tab-tag">End-to-End Network</span>
          <span class="v-tab-badge">26 Roles · 32 Agents</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="demand_sop" onclick="switchVerticalTab('demand_sop', this)" style="--v-accent: #10b981;">
          <span class="v-tab-num">V1 · PLAN</span>
          <span class="v-tab-title">Demand &amp; S&amp;OP</span>
          <span class="v-tab-tag">The Forecasters</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="sourcing_procurement" onclick="switchVerticalTab('sourcing_procurement', this)" style="--v-accent: #a142f4;">
          <span class="v-tab-num">V2 · SOURCE</span>
          <span class="v-tab-title">Sourcing &amp; Procurement</span>
          <span class="v-tab-tag">The Buyers</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="manufacturing_prod" onclick="switchVerticalTab('manufacturing_prod', this)" style="--v-accent: #3b82f6;">
          <span class="v-tab-num">V3 · MAKE</span>
          <span class="v-tab-title">Manufacturing &amp; MPS</span>
          <span class="v-tab-tag">The Makers</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="inventory_meio" onclick="switchVerticalTab('inventory_meio', this)" style="--v-accent: #06b6d4;">
          <span class="v-tab-num">V4 · BUFFER</span>
          <span class="v-tab-title">Inventory &amp; MEIO</span>
          <span class="v-tab-tag">The Buffers</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="warehousing_qa" onclick="switchVerticalTab('warehousing_qa', this)" style="--v-accent: #00d2ff;">
          <span class="v-tab-num">V5 · WMS &amp; QA</span>
          <span class="v-tab-title">Warehousing &amp; QA</span>
          <span class="v-tab-tag">The Custodians</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="logistics_fleet" onclick="switchVerticalTab('logistics_fleet', this)" style="--v-accent: #ff8c00;">
          <span class="v-tab-num">V6 · LOGISTICS</span>
          <span class="v-tab-title">Logistics &amp; Fleet</span>
          <span class="v-tab-tag">The Movers</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="trade_mkt_dist" onclick="switchVerticalTab('trade_mkt_dist', this)" style="--v-accent: #f59e0b;">
          <span class="v-tab-num">V7 · TM&amp;D</span>
          <span class="v-tab-title">TM&amp;D Last-Mile</span>
          <span class="v-tab-tag">The Last-Mile Push</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="reverse_risk_esg" onclick="switchVerticalTab('reverse_risk_esg', this)" style="--v-accent: #ec4899;">
          <span class="v-tab-num">V8 · GUARDIAN</span>
          <span class="v-tab-title">Reverse &amp; Risk ESG</span>
          <span class="v-tab-tag">The Guardians</span>
        </button>
      </div>"""

    if old_org_section_header in content:
        content = content.replace(old_org_section_header, new_org_section_header, 1)
        print("Updated #orgChartSection header and inserted Three Rivers banner + 8-vertical tab bar.")
    else:
        print("Warning: old_org_section_header not found")

    # Update CSCO subtext
    old_cfo_sub = '<div class="cfo-box-sub"><span class="sc-hl-metric">6 SCOR Verticals</span> · <span class="sc-hl-metric">26 Personas</span> · <span class="sc-hl-metric">28 Domain Agents</span> + <span class="sc-hl-metric">4 Universal Cross-Persona Agents</span></div>'
    new_cfo_sub = '<div class="cfo-box-sub"><span class="sc-hl-metric">8 Operational Verticals</span> · <span class="sc-hl-metric">26 Personas</span> · <span class="sc-hl-metric">28 Domain Agents</span> + <span class="sc-hl-metric">4 Universal Cross-Persona Agents</span></div>'
    content = content.replace(old_cfo_sub, new_cfo_sub)

    # Update SVG connectors for 4 columns
    old_svg_connectors = """        <!-- SVG Tree Lines to 6 Supply Chain Verticals (3x2 Grid) with Animated Telemetry Packets -->
        <svg class="org-connectors" viewBox="0 0 1000 56" preserveAspectRatio="none">
          <defs>
            <linearGradient id="orgLineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#10b981" stop-opacity="0.55" />
              <stop offset="50%" stop-color="#00d2ff" stop-opacity="0.85" />
              <stop offset="100%" stop-color="#ec4899" stop-opacity="0.55" />
            </linearGradient>
          </defs>
          <path d="M500,0 L500,24 M166,24 L834,24 M166,24 L166,56 M500,24 L500,56 M834,24 L834,56" />
          <path d="M500,0 L500,24 M166,24 L834,24 M166,24 L166,56 M500,24 L500,56 M834,24 L834,56"
                stroke="url(#orgLineGrad)" stroke-width="2.2" stroke-dasharray="8 10" fill="none"
                style="animation: scDashFlow 2.4s linear infinite;" />
          <circle r="3.5" fill="#00d2ff">
            <animateMotion dur="2.6s" repeatCount="indefinite" path="M500,0 L500,24 L166,24 L166,56" />
          </circle>
          <circle r="3.5" fill="#38bdf8">
            <animateMotion dur="2.0s" repeatCount="indefinite" path="M500,0 L500,56" />
          </circle>
          <circle r="3.5" fill="#a855f7">
            <animateMotion dur="2.6s" repeatCount="indefinite" path="M500,0 L500,24 L834,24 L834,56" />
          </circle>
        </svg>"""

    new_svg_connectors = """        <!-- SVG Tree Lines to 8 Supply Chain Verticals (4x2 Grid) with Animated Telemetry Packets -->
        <svg class="org-connectors" viewBox="0 0 1000 56" preserveAspectRatio="none">
          <defs>
            <linearGradient id="orgLineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#10b981" stop-opacity="0.55" />
              <stop offset="33%" stop-color="#3b82f6" stop-opacity="0.75" />
              <stop offset="66%" stop-color="#ff8c00" stop-opacity="0.75" />
              <stop offset="100%" stop-color="#ec4899" stop-opacity="0.55" />
            </linearGradient>
          </defs>
          <path d="M500,0 L500,24 M125,24 L875,24 M125,24 L125,56 M375,24 L375,56 M625,24 L625,56 M875,24 L875,56" />
          <path d="M500,0 L500,24 M125,24 L875,24 M125,24 L125,56 M375,24 L375,56 M625,24 L625,56 M875,24 L875,56"
                stroke="url(#orgLineGrad)" stroke-width="2.2" stroke-dasharray="8 10" fill="none"
                style="animation: scDashFlow 2.4s linear infinite;" />
          <circle r="3.5" fill="#10b981">
            <animateMotion dur="2.4s" repeatCount="indefinite" path="M500,0 L500,24 L125,24 L125,56" />
          </circle>
          <circle r="3.5" fill="#3b82f6">
            <animateMotion dur="2.0s" repeatCount="indefinite" path="M500,0 L500,24 L375,24 L375,56" />
          </circle>
          <circle r="3.5" fill="#ff8c00">
            <animateMotion dur="2.2s" repeatCount="indefinite" path="M500,0 L500,24 L625,24 L625,56" />
          </circle>
          <circle r="3.5" fill="#ec4899">
            <animateMotion dur="2.6s" repeatCount="indefinite" path="M500,0 L500,24 L875,24 L875,56" />
          </circle>
        </svg>"""

    if old_svg_connectors in content:
        content = content.replace(old_svg_connectors, new_svg_connectors, 1)
        print("Updated SVG connectors for 4-column 8-vertical grid.")

    # Also add the Interactive Safety Stock & ROP Calculator right below Universal Agents
    old_univ_home = """      <!-- Cross-Persona Universal Supply Chain Agents (Used by All 26 Personas) -->
      <div id="universalAgentsHomeContainer"></div>"""

    new_univ_home = """      <!-- Cross-Persona Universal Supply Chain Agents (Used by All 26 Personas) -->
      <div id="universalAgentsHomeContainer"></div>

      <!-- Interactive Multi-Echelon Safety Stock & ROP Calculator -->
      <div class="ss-calc-card">
        <div class="ss-calc-header">
          <div>
            <div class="ss-calc-title">🧮 Interactive Multi-Echelon Safety Stock &amp; Reorder Point (ROP) Calculator</div>
            <div class="ss-calc-sub">See in real time why supplier lead-time volatility (σ_LT) exponentially inflates required buffer stock compared to pure demand fluctuations:</div>
          </div>
          <div style="font-size:12px; color:var(--text-muted); background:rgba(56,189,248,0.1); border:1px solid rgba(56,189,248,0.3); padding:4px 12px; border-radius:999px;">
            Service Level Z = 2.05 (98.0% Cycle Service)
          </div>
        </div>

        <div class="control-row">
          <div class="control-field">
            <label>Average Daily Demand (Cases/Day): <strong id="lblD" style="color:#fff;">600</strong></label>
            <input type="range" id="rngD" min="100" max="2500" step="50" value="600" oninput="runSSCalc()"/>
          </div>
          <div class="control-field">
            <label>Supplier Lead Time (Days): <strong id="lblLT" style="color:#fff;">8</strong></label>
            <input type="range" id="rngLT" min="1" max="45" step="1" value="8" oninput="runSSCalc()"/>
          </div>
          <div class="control-field">
            <label>Lead-Time Std Dev σ_LT (Days): <strong id="lblSLT" style="color:#fff;">3.0</strong></label>
            <input type="range" id="rngSLT" min="0" max="15" step="0.5" value="3.0" oninput="runSSCalc()"/>
          </div>
        </div>

        <div id="ssOutput" class="ss-output-box"></div>
      </div>"""

    if old_univ_home in content:
        content = content.replace(old_univ_home, new_univ_home, 1)
        print("Inserted live Safety Stock & ROP Calculator card into front page.")

    # 3. Replace const DEPARTMENTS block
    # Locate from `/* 1. SIX UNIVERSAL SCOR` to `/* Metadata helper for the 4 Universal`
    dept_block_regex = re.compile(r"/\* 1\. SIX UNIVERSAL SCOR SUPPLY CHAIN VERTICALS.*?(?=const UNIVERSAL_CSCO_DEPT =)", re.DOTALL)
    
    new_dept_block = """/* 1. EIGHT CANONICAL OPERATIONAL VERTICALS UNDER THE CSCO (LEVEL-1 TO LEVEL-3 DECOMPOSITION) */
    const DEPARTMENTS = {
      demand_sop: {
        id: 'demand_sop',
        vNum: 'V1',
        scorBadge: 'VERTICAL 01 · DEMAND & S&OP',
        name: 'Demand Planning, Sensing & S&OP',
        fullName: 'Vertical 1: Demand Planning, Sensing & S&OP (The Forecasters)',
        tagline: 'The Forecasters',
        subtitle: 'Demand sensing, 45-min S&OP consensus, promo elasticity & retail CPFR',
        color: '#10b981',
        watermarkType: 'demand_wave',
        horizon: 'Tactical Horizon (Weekly – 18 Months)',
        coreQuestion: 'What, how much, when, and where will customers buy—and can our network supply it?',
        river: 'River 2: Demand & Information Flow (◀── Upstream)',
        systems: 'SAP IBP · SAP S/4HANA · Kinaxis · o9 Solutions · EDI 852/830 POS · BigQuery · AlloyDB · Cloud Spanner · Vertex AI TimesFM · Google WeatherNext 3 · Google Maps Places · Apigee',
        solverSummary: 'Vertex AI TimesFM Zero-Shot Foundation Forecasting + Hierarchical Bayesian Reconciliation + Google OR-Tools MILP S&OP Capacity & Margin Solver on BigQuery & AlloyDB',
        toilMetric: '65% of planning time lost',
        toilBullets: [
          'Stitching 15+ disconnected sales, POS, distributor EDI 852, and marketing spreadsheets every cycle',
          'Order-history forecasts lag real-time customer sell-through by 2 to 4 weeks and ignore stockout censorship',
          'Promotions silently cannibalize 30%+ of sister SKUs while 21-day sequential S&OP cycles stall decisions'
        ],
        impactMetric: '45-Min S&OP & +24% Forecast Accuracy',
        impactBullets: [
          'Cuts demand forecast error by 24% ($14M+ saved in excess buffer stock & prevented stockouts; secondary KPI: -6.4% WAPE)',
          'Compresses S&OP planning cycles from 21 days to a live 45-minute executive review (-85% manual planner effort)',
          'Eliminates 30%+ promo cannibalization to boost net promotional return by +22% ($8M+ saved trade spend)'
        ],
        l1toL3: {
          mandate: 'Transforms market demand signals into a single consensus operational plan. Operates 5-stage monthly S&OP cadence reconciling Sales with Manufacturing. Utilizes statistical baseline models augmented by short-term AI demand sensing.',
          mtoVsMts: 'Make-to-Stock across 5,000+ regional SKUs vs. Make-to-Order customized packs; solves festival demand spikes (e.g. Durga Puja, Diwali) while preventing Bullwhip amplification upstream.',
          battleground: 'Finance plans in quarterly currency; Demand Planning must forecast cases per SKU per depot per week. Reconciles promotional lift with depot buffers.',
          dataObjects: 'POS Scanner Streams · EDI 852 Feeds · TimesFM Forecast Curves · Promotional Lift Elasticity Coefficients · Consensus S&OP Master Sheets'
        },
        kpis: 'Forecast Accuracy (1 - WMAPE) | Mean Absolute Percentage Error (MAPE) | Forecast Bias (%)',
        personaIds: ['demand_planning_dir', 'sop_ibp_lead', 'promo_launch_planner', 'cpfr_channel_mgr'],
        agentIds: ['demand_sensing_agent', 'sop_scenario_weaver', 'promo_lift_simulator', 'cpfr_sync_agent']
      },
      sourcing_procurement: {
        id: 'sourcing_procurement',
        vNum: 'V2',
        scorBadge: 'VERTICAL 02 · SOURCING & PROCUREMENT',
        name: 'Strategic Sourcing & Category Procurement',
        fullName: 'Vertical 2: Strategic Sourcing & Category Procurement (The Buyers)',
        tagline: 'The Buyers',
        subtitle: 'Parametric should-cost RFQ, Tier-N Spanner graph, contract SLAs & inbound AQL QA',
        color: '#a142f4',
        watermarkType: 'supplier_graph',
        horizon: 'Strategic & Operational Horizon',
        coreQuestion: 'Where do we procure raw materials & packaging at optimal total cost, lead time, and AQL quality?',
        river: 'Bridges River 1 (Inbound Material) and River 3 (Cash Outflows / DPO)',
        systems: 'SAP Ariba · SAP S/4HANA MM/QM/GTS · Coupa · Siemens Teamcenter BOM · Cloud Spanner Graph · BigQuery · AlloyDB · Google Maps Geocoding · Document AI · OR-Tools · Apigee',
        solverSummary: 'Cloud Spanner Tier-N Graph Neural Propagation + Parametric BOM Should-Cost + Google OR-Tools Combinatorial MILP Award Split + Document AI COA/Contract Parser',
        toilMetric: 'Zero visibility past Tier-1',
        toilBullets: [
          'Weeks spent normalizing inconsistent supplier PDF and Excel RFQ quotes without bottom-up should-costs',
          'Sub-tier (Tier-2 / Tier-3) disruptions and lot quality defects stay hidden until factory lines stop',
          'Volume rebates, commodity index caps, and Free Trade Agreement (FTA) tariff savings leak unnoticed'
        ],
        impactMetric: '-6.8% Spend & 11-Day Early Warning',
        impactBullets: [
          'Parametric BOM should-cost decomposition & combinatorial multi-supplier RFQ award solver ($100M+ Unilever benchmark)',
          'Multi-tier (Tier-1 to Tier-4) Spanner dependency graph, predictive quality COA screening & backup PO routing (9 mos → hours)',
          'Continuous contract rebate recovery, HS tariff engineering & multi-tier provenance ledger'
        ],
        l1toL3: {
          mandate: 'Manages all external supplier expenditure across Direct Procurement (agricultural crops, chemicals, packaging laminates) and Indirect Procurement (MRO spare parts, logistics services). Governs vendor RFPs, should-cost models, contract SLAs, and Delegation of Authority (DOA).',
          mtoVsMts: 'Dual-sourcing strategies balancing committed long-term vendor allocations with dynamic spot-buy hedging across volatile commodity markets.',
          battleground: 'Ensuring defective materials are rejected or penalized at the gate (AQL moisture/defect audits) before Accounts Payable pays the vendor.',
          dataObjects: 'SAP Purchase Orders (ME21N) · Inwarding Gate Entries (MIGO) · Vendor Quality Defect Logs · Should-Cost Decomposition Tables · DOA Matrix'
        },
        kpis: 'Purchase Price Variance (PPV) | Supplier OTIF % | Lead-Time Std Dev (σ_LT) | Cost Savings ($/₹)',
        personaIds: ['category_sourcing_mgr', 'supplier_risk_lead', 'tariff_compliance_spec', 'supplier_quality_lead'],
        agentIds: ['rfq_should_cost_agent', 'tier_n_risk_sentinel', 'tariff_esg_agent', 'supplier_quality_sentinel']
      },
      manufacturing_prod: {
        id: 'manufacturing_prod',
        vNum: 'V3',
        scorBadge: 'VERTICAL 03 · MANUFACTURING & MPS',
        name: 'Production Planning & Manufacturing / MPS',
        fullName: 'Vertical 3: Production Planning & Manufacturing / MPS (The Makers)',
        tagline: 'The Makers',
        subtitle: 'Finite MPS line scheduling, predictive spindle OEE, inline SPC yield & ECO cutover',
        color: '#3b82f6',
        watermarkType: 'plant_oee',
        horizon: 'Tactical to Shift-Level Execution',
        coreQuestion: 'How do we sequence factory lines and synchronize BOM inputs for zero unplanned downtime?',
        river: 'River 1: Physical Material Flow (Factory WIP & Transformation)',
        systems: 'SAP S/4HANA PP/DS & PM · Siemens Opcenter MES · Rockwell Plex · OSIsoft PI Historian · Teamcenter PLM · BigQuery · AlloyDB · Cloud Spanner · OR-Tools CP-SAT · Pub/Sub & Dataflow',
        solverSummary: 'Google OR-Tools CP-SAT Sequence-Dependent Setup & Finite Capacity Job-Shop Scheduler + Vertex AI Multimodal Vibration/Thermal OEE Anomaly Model + Closed-Loop SPC',
        toilMetric: '19% capacity lost to changeovers & stops',
        toilBullets: [
          'Infinite-capacity ERP MRP schedules ignore sequence-dependent coil/paint/mold changeovers and line starvation',
          'Unplanned spindle, press, and robotics breakdowns halt high-margin production runs and trigger backorders',
          'Inline process parameter drift and uncoordinated Engineering Change Orders (ECOs) generate scrap and obsolete WIP'
        ],
        impactMetric: '-48% Unplanned Downtime & -25% Backorders',
        impactBullets: [
          'Autonomous OR-Tools CP-SAT finite capacity scheduling cuts line changeover time by 32% (-25% customer backorders)',
          'Predictive PLC/historian telemetry prevents 48% of unplanned stops (+14.2% productive machine uptime / OEE)',
          'Closed-loop inline SPC vision quality cuts scrap by 44% and speeds batch release from 48 hours to 5 minutes'
        ],
        l1toL3: {
          mandate: 'Converts constrained S&OP plan into plant-level Master Production Schedules (MPS) and executes Material Requirements Planning (MRP) BOM explosions. Coordinates multi-component packaging synchronization (e.g. noodle cake + seasoning sachet) and drives shop-floor OEE.',
          mtoVsMts: 'Balancing long efficient production runs with agility; minimizing sequence-dependent setup losses while holding line changeovers under strict limits.',
          battleground: 'Short production runs increase changeover downtime costs; excessively long runs build surplus finished goods inventory.',
          dataObjects: 'Production Orders (CO01) · Multi-Level BOMs · SCADA Historian High-Frequency Telemetry · Tooling Wear Indices · Shift Maintenance Schedules'
        },
        kpis: 'Schedule Adherence (%) | Overall Equipment Effectiveness (OEE) | Changeover Downtime Hours',
        personaIds: ['mps_scheduling_lead', 'plant_oee_maintenance_mgr', 'manufacturing_quality_eng', 'bom_change_launch_lead'],
        agentIds: ['line_schedule_optimizer', 'predictive_oee_sentinel', 'inline_yield_guardian', 'eco_cutover_orchestrator']
      },
      inventory_meio: {
        id: 'inventory_meio',
        vNum: 'V4',
        scorBadge: 'VERTICAL 04 · INVENTORY & MEIO',
        name: 'Inventory & Network Optimization / MEIO',
        fullName: 'Vertical 4: Inventory & Network Optimization / MEIO (The Buffers)',
        tagline: 'The Buffers',
        subtitle: 'Multi-echelon safety stock, dynamic STO rebalancing, sub-50ms ATP & cost-to-serve',
        color: '#06b6d4',
        watermarkType: 'demand_wave',
        horizon: 'Tactical Horizon (Weekly – Monthly)',
        coreQuestion: 'How much buffer stock should be placed at each echelon to guarantee 99%+ fill rate at minimum working capital?',
        river: 'River 3: Cash & Working Capital Flow (DIO Optimization)',
        systems: 'SAP IBP/MM · Blue Yonder MEIO · BigQuery · AlloyDB · Cloud Spanner · Google OR-Tools · Google Maps Distance Matrix',
        solverSummary: 'Coupled Stochastic Multi-Echelon (MEIO) + Dynamic Lateral STO Rebalancing MILP + Sub-50ms AlloyDB/Spanner Real-Time ATP Order Promising + Network Cost-to-Serve Twin',
        toilMetric: '24% excess buffer cash trapped',
        toilBullets: [
          'Static single-echelon ERP rules hoard redundant safety stocks upstream while edge regional depots stock out',
          'Manual spreadsheet rebalancing moves stock too late—leaving festival markets dry while sister depots sit on dead inventory',
          'Rigid FIFO order promising splits customer orders across distant depots, inflating secondary freight and late arrivals'
        ],
        impactMetric: '-18% Working Capital @ 99.4% Fill',
        impactBullets: [
          'Stochastic Multi-Echelon Inventory Optimization (MEIO) & lateral hub-to-hub rebalancing unlocks $28M+ liquidity',
          'Dynamic Stock Transfer Order (STO) orchestrator prevents regional stockouts with zero manual planner intervention',
          'Margin-aware real-time ATP order promising with Google Maps Distance Matrix cuts split shipments by 34%'
        ],
        l1toL3: {
          mandate: 'Acts as the physical treasury of the enterprise. Segments SKUs via ABC-XYZ matrices, calculates mathematically optimal Safety Stock buffers across central hubs and regional depots, and initiates dynamic Stock Transfer Orders (STOs) to prevent regional stockouts without bloating DIO.',
          mtoVsMts: 'Decoupling points placement; holding generic WIP upstream and postponing final regional pack customization until local demand signals crystallize.',
          battleground: 'CFO wants lean stock to free corporate cash; Sales wants safety buffers to prevent festival stockouts.',
          dataObjects: 'Multi-Echelon Stock Ledgers · Safety Stock Targets (SS) · Reorder Points (ROP) · Inter-Depot Stock Transfer Orders (STOs) · ABC-XYZ Velocity Matrix'
        },
        kpis: 'Days Inventory Outstanding (DIO) | Inventory Turns | Slow-Moving / Dead Stock (SLOB) %',
        personaIds: ['meio_inventory_mgr', 'atp_fulfillment_spec', 'sc_finops_network_architect'],
        agentIds: ['meio_safety_stock_agent', 'atp_order_promising_agent', 'network_twin_architect']
      },
      warehousing_qa: {
        id: 'warehousing_qa',
        vNum: 'V5',
        scorBadge: 'VERTICAL 05 · WAREHOUSING & QA',
        name: 'Warehousing, Inwarding QA & Intralogistics',
        fullName: 'Vertical 5: Warehousing, Inwarding QA & Intralogistics (The Custodians)',
        tagline: 'The Custodians',
        subtitle: 'Dock-to-stock <4h, inbound AQL quality, 3D Golden-Zone slotting & yard sequencing',
        color: '#00d2ff',
        watermarkType: 'conveyor_rack',
        horizon: 'Real-Time Daily Execution',
        coreQuestion: 'How do we receive, inspect, putaway, and wave-pick goods inside facilities with zero congestion and <4h dock-to-stock?',
        river: 'Node Custodians along River 1: Physical Material Flow',
        systems: 'Manhattan Active WMS · SAP EWM · Dematic AS/RS WCS · ICML Quality SOP Manuals · Handheld RF Scanners · Yard Management',
        solverSummary: '3D Spatial Affinity Slotting Twin + Inbound AQL Defect Classifier + Port/Air/Rail Cross-Dock Flow-Through MILP + Dynamic Yard Door Sequencer',
        toilMetric: 'Dock congestion & 34% pick travel waste',
        toilBullets: [
          'When incoming deliveries breach AQL moisture or defect limits, supervisors waste hours flipping through SOP binders and contracts',
          'Static annual warehouse slotting forces pickers to walk miles through congested aisles for high-velocity SKUs',
          'Uncoordinated trailer yard arrivals cause dock gridlock while cross-dock transloads sit waiting for bay doors'
        ],
        impactMetric: '-28% Picker Travel & <2.5h Dock-to-Stock',
        impactBullets: [
          'Automated AQL defect auditing and instant PDF dispute memo generation with contract-backed penalty debit notes',
          '3D Golden-Zone spatial affinity slotting cuts picker travel distance by 28% and boosts storage density by 31%',
          'Autonomous trailer yard and dock door sequencing slashes gate dwell by 41% and speeds cross-dock flow-through'
        ],
        l1toL3: {
          mandate: 'Manages all physical movements inside factory warehouses and regional C&F depots: gate entry, inbound AQL quality sampling (moisture, visual defects), GRN posting, directed putaway, FEFO/FIFO wave picking, cross-docking, and physical-to-book stock cycle counting.',
          mtoVsMts: 'Fast-moving consumer products require high-velocity cross-dock flow-through; high-value discrete parts require secure AS/RS high-bay quarantine.',
          battleground: 'Dock congestion vs. turnaround speed; ensuring defective incoming batches do not contaminate clean stock.',
          dataObjects: 'Goods Receipt Notes (MIGO/GRN) · Bin-Level Storage Locations · Wave-Pick Work Orders · RF Scan Timestamps · Yard Bay Schedules'
        },
        kpis: 'Dock-to-Stock Cycle Time (<4h) | Inbound AQL Defect Rate (%) | Warehouse Pick Accuracy (%)',
        personaIds: ['warehouse_slotting_lead', 'dock_yard_supervisor'],
        agentIds: ['warehouse_slotting_agent', 'yard_dock_sequencer', 'crossdock_transfer_orchestrator']
      },
      logistics_fleet: {
        id: 'logistics_fleet',
        vNum: 'V6',
        scorBadge: 'VERTICAL 06 · LOGISTICS & FLEET',
        name: 'Logistics, Fleet & Transportation Management',
        fullName: 'Vertical 6: Logistics, Fleet & Transportation Management (The Movers)',
        tagline: 'The Movers',
        subtitle: 'Ocean vessel AIS, air cargo charter/ULD, rail siding free-time & 3D LIFO loading',
        color: '#ff8c00',
        watermarkType: 'corridor_lifo',
        horizon: 'Real-Time Multi-Modal Daily Execution',
        coreQuestion: 'How do we move freight across ocean vessels, cargo aircraft, intermodal rail rakes, and linehaul trailers at minimum cost and 98%+ OTIF?',
        river: 'Arteries of River 1: Physical Material Flow',
        systems: 'SAP TM · Blue Yonder TMS · Oracle OTM · CargoWise One · Spire AIS · IATA Cargo-XML · Railinc EDI 404 · Indian Railways FOIS · Google Maps Routes API · Google OR-Tools',
        solverSummary: 'End-to-End Multi-Modal Mode-Shift MILP (Factory→Ship→Air→Rail→Truck) + 3D Aircraft ULD & Trailer LIFO Guillotine Bin-Packing + Rail Siding Free-Time & Demurrage Sentinel',
        toilMetric: '22% multi-modal freight waste & demurrage',
        toilBullets: [
          'Siloed ocean container booking, panic air freight charters, slow rail handoffs, and unclustered linehaul routes',
          '2D paper load sheets ignore 3D aircraft ULD contours, container cube, highway axle limits, and strict reverse-stop LIFO order',
          'Indian Railways siding demurrage and carrier detention fees leak millions due to unmonitored turnaround timestamps'
        ],
        impactMetric: '-22.4% Multi-Modal Cost & Zero Demurrage',
        impactBullets: [
          'End-to-end multi-modal corridor orchestration from Factory Gate to Ocean Ships, Airplanes, Rail Rakes & Road Trucks',
          '3D guillotine bin-packing for 53ft trailers (reverse-stop LIFO), 40ft ocean containers & contoured aircraft ULDs (LD3/PMC)',
          'Continuous railway rake siding turnaround monitoring and automated carrier freight invoice fuel surcharge auditing'
        ],
        l1toL3: {
          mandate: 'Manages Primary Freight (plant-to-depot via rail rakes, coastal shipping, and heavy multi-axle trucks) and Secondary Linehaul. Optimizes truck cube/weight fill, tracks railway rake placement to prevent demurrage/wharfage fines, and audits carrier freight/fuel invoices.',
          mtoVsMts: 'Heavy industrial (cement/metals) relies on 58-wagon rail rakes where freight is 30% of COGS; CPG relies on multi-axle road fleet for agility.',
          battleground: 'Unplanned rake demurrage penalties and freight invoice fuel surcharge creep eroding operating margins.',
          dataObjects: 'Railway FOIS Timestamps · GPS Satellite AIS Pings · Electronic Bills of Lading (e-BOL) · 3D Load Plans (Cube/Axle) · Carrier Rate Cards'
        },
        kpis: 'Freight Cost per Ton-Km (₹/PTPK) | Truck Cube Fill % | Railway Demurrage & Wharfage (₹)',
        personaIds: ['global_trade_port_mgr', 'air_cargo_charter_lead', 'intermodal_rail_linehaul_lead', 'network_logistics_lead', 'freight_claims_analyst'],
        agentIds: ['port_drayage_orchestrator', 'air_cargo_uld_optimizer', 'intermodal_rail_linehaul_agent', 'multimodal_mode_shift_agent', 'load_consolidation_agent', 'freight_control_tower']
      },
      trade_mkt_dist: {
        id: 'trade_mkt_dist',
        vNum: 'V7',
        scorBadge: 'VERTICAL 07 · TM&D & LAST-MILE',
        name: 'Trade Marketing & Distribution / TM&D',
        fullName: 'Vertical 7: Trade Marketing & Distribution / TM&D (The Last-Mile Push)',
        tagline: 'The Last-Mile Push',
        subtitle: 'Secondary distribution, FSO beat planning, distributor live stock & planogram audits',
        color: '#f59e0b',
        watermarkType: 'corridor_lifo',
        horizon: 'Daily Field Execution',
        coreQuestion: 'How do we push inventory through distributors to millions of retail counters, optimize FSO beats, and prevent stockout pitches?',
        river: 'Terminal Interface of River 1 (Retail Shelf) and River 2 (Consumer POS / Sell-Through)',
        systems: 'DMS (Distributor Management Systems) · SFA Mobile Handhelds · Google Maps Platform · Store Visibility Sheets · Quick-Commerce Portals (Blinkit/Zepto)',
        solverSummary: 'Google Maps Routes Preferred CVRPTW Beat Sequencer + Live DMS Inventory Stock-Reconciliation Broker + Planogram Vision Auditor + Secondary Trade Scheme Reconciler',
        toilMetric: 'Field sales pitching out-of-stock SKUs',
        toilBullets: [
          'Field Sales Officers (FSOs) waste retail counter visits booking orders for SKUs that are currently out of stock at the distributor',
          'Manual store visibility audits rely on unverified photos, allowing retailer planogram violations and unearned scheme payouts',
          'Sub-optimal distributor beat routes cause delayed delivery to high-velocity kirana stores, causing retail stockouts'
        ],
        impactMetric: '+18% Distributor Case Fill & Zero Lost Visits',
        impactBullets: [
          'Real-time reconciliation of FSO focus target SKUs with live distributor stock, automatically substituting available variants',
          'Multimodal vision auditing of retail shelf photos verifies planogram compliance and automates scheme discount approvals',
          'Google Maps Fleet Engine beat routing ensures 100% scheduled store coverage and accelerates secondary reorders'
        ],
        l1toL3: {
          mandate: 'Orchestrates the commercial flow from Authorized Distributors to millions of General Trade (kirana) counters, Modern Trade, and Quick-Commerce dark stores. Optimizes Field Sales Officer (FSO) beat plans, audits live distributor stock, and verifies retail planogram visibility.',
          mtoVsMts: 'Synchronizing distributor daily replenishment with ultra-fast quick-commerce dark store inventory feeds and daily kirana shop beats.',
          battleground: 'Incomplete store deliveries and planogram compliance gaps delaying invoice acceptance and leaking trade spend.',
          dataObjects: 'DMS Inventory Ledgers · FSO Beat Itineraries · Retail Shelf Visibility Photos · Secondary Trade Scheme Agreements · Store POS Feeds'
        },
        kpis: 'Effective Store Coverage % | Distributor Case Fill Rate % | Retail Planogram Compliance %',
        personaIds: ['fleet_dispatch_mgr'],
        agentIds: ['fleetflow_dispatch']
      },
      reverse_risk_esg: {
        id: 'reverse_risk_esg',
        vNum: 'V8',
        scorBadge: 'VERTICAL 08 · REVERSE & RISK TOWER',
        name: 'Reverse Logistics, Risk Control Tower & ESG',
        fullName: 'Vertical 8: Reverse Logistics, Risk Control Tower & ESG (The Guardians)',
        tagline: 'The Guardians',
        subtitle: 'Retail OTIF chargeback defense, circular RMA backhaul, Scope-3 ESG & macro resilience',
        color: '#ec4899',
        watermarkType: 'circular_loop',
        horizon: 'Continuous Strategic Horizon',
        coreQuestion: 'How do we recover value from damaged/expired stock, defend against unearned chargebacks, and govern Scope-3 carbon & supply risks?',
        river: 'Circular Loop closing River 1 (Reversals/Recycling) and shielding River 3 (Chargeback Protection)',
        systems: 'SAP Claims & Returns Management · Retail OTIF Portals · Loop RMA · Google Earth Engine · ISO-14083 Carbon Engine · BigQuery Omni · Cloud Spanner · Live Commodity Feeds',
        solverSummary: 'Retail Chargeback Risk Classifier + Vision RMA Backhaul CVRPTW + Google Earth Engine & Maps ISO-14083 Carbon Engine + RCSA Governance Auditor',
        toilMetric: '3.5% revenue lost to OTIF fines & returns',
        toilBullets: [
          'Retailer On-Time In-Full (OTIF) penalty deductions and shortage chargebacks are discovered weeks after payment with no easy dispute path',
          'Customer returns ship via costly third-party LTL to central depots while outbound fleet trucks return backhaul empty',
          'Shipment-level Scope-3 carbon accounting (CBAM/EUDR) and enterprise RCSA risk assessments rely on static annual guesswork'
        ],
        impactMetric: '-78% OTIF Fines & +31% Return Margin',
        impactBullets: [
          'Predicts retailer OTIF breaches 72 hours early to reallocate stock and auto-generates contract-backed dispute evidence',
          'Multimodal edge RMA grading and Google Maps fleet backhaul insertion boost net return recovery margin by 31%',
          'Automated ISO-14083 compliant shipment-level Scope-3 carbon ledger and continuous supply chain RCSA risk auditing'
        ],
        l1toL3: {
          mandate: 'Manages Return-to-Vendor (RTV) chargebacks, customer returns, farm-to-fork ESG traceability (e.g. carbon and water metrics), macro commodity stress testing, and internal RCSA risk and control compliance registers.',
          mtoVsMts: 'Closed-loop circularity; recovering value from returned assets, packaging drums, pallets, and re-certifying refurbished stock.',
          battleground: 'Preventing fraudulent distributor breakage claims that leak 1–2% of EBITDA margin and fighting invalid retailer deductions.',
          dataObjects: 'Customer Return Authorizations (RMA) · Retailer OTIF Scorecards · Vendor Debit Notes · Scope 1/2/3 Carbon Emissions Ledgers · RCSA Matrix'
        },
        kpis: 'Return Processing Time | Unearned Claim Leakage % | Scope-3 Carbon Intensity | RCSA Audit Score',
        personaIds: ['otif_customer_service_lead', 'reverse_logistics_mgr', 'sc_sustainability_esg_lead'],
        agentIds: ['reverse_rma_optimizer', 'otif_penalty_shield', 'carbon_scope3_ledger']
      }
    };

    /* Backward compatibility aliases */
    DEPARTMENTS['sourcing_risk'] = DEPARTMENTS['sourcing_procurement'];
    DEPARTMENTS['inventory_warehouse'] = DEPARTMENTS['warehousing_qa'];
    DEPARTMENTS['circular_enable'] = DEPARTMENTS['reverse_risk_esg'];

    """

    content, n_subs = dept_block_regex.subn(new_dept_block, content, count=1)
    if n_subs > 0:
        print("Successfully replaced const DEPARTMENTS with the 8 Operational Verticals & aliases.")
    else:
        print("Error: Could not match const DEPARTMENTS block for replacement!")
        sys.exit(1)

    # 4. Update deptId in PERSONAS
    persona_dept_updates = {
        "meio_inventory_mgr": "inventory_meio",
        "warehouse_slotting_lead": "warehousing_qa",
        "atp_fulfillment_spec": "inventory_meio",
        "fleet_dispatch_mgr": "trade_mkt_dist",
        "category_sourcing_mgr": "sourcing_procurement",
        "supplier_risk_lead": "sourcing_procurement",
        "tariff_compliance_spec": "sourcing_procurement",
        "supplier_quality_lead": "sourcing_procurement",
        "dock_yard_supervisor": "warehousing_qa",
        "reverse_logistics_mgr": "reverse_risk_esg",
        "otif_customer_service_lead": "reverse_risk_esg",
        "sc_sustainability_esg_lead": "reverse_risk_esg",
        "sc_finops_network_architect": "inventory_meio",
    }

    for pid, new_dept in persona_dept_updates.items():
        # Match pattern: pid: {\n        id: 'pid',\n        deptId: '...',
        pat = re.compile(rf"({pid}:\s*\{{\s*id:\s*'{pid}',\s*deptId:\s*)'[a-zA-Z0-9_]+'", re.MULTILINE)
        content, count = pat.subn(rf"\1'{new_dept}'", content, count=1)
        if count > 0:
            print(f"Updated persona {pid} -> deptId: {new_dept}")

    # 5. Update deptId in AGENTS
    agent_dept_updates = {
        "rfq_should_cost_agent": "sourcing_procurement",
        "tier_n_risk_sentinel": "sourcing_procurement",
        "tariff_esg_agent": "sourcing_procurement",
        "supplier_quality_sentinel": "sourcing_procurement",
        "meio_safety_stock_agent": "inventory_meio",
        "warehouse_slotting_agent": "warehousing_qa",
        "atp_order_promising_agent": "inventory_meio",
        "yard_dock_sequencer": "warehousing_qa",
        "crossdock_transfer_orchestrator": "warehousing_qa",
        "fleetflow_dispatch": "trade_mkt_dist",
        "reverse_rma_optimizer": "reverse_risk_esg",
        "otif_penalty_shield": "reverse_risk_esg",
        "carbon_scope3_ledger": "reverse_risk_esg",
        "network_twin_architect": "inventory_meio"
    }

    for aid, new_dept in agent_dept_updates.items():
        pat = re.compile(rf"({aid}:\s*\{{\s*id:\s*'{aid}',\s*deptId:\s*)'[a-zA-Z0-9_]+'", re.MULTILINE)
        content, count = pat.subn(rf"\1'{new_dept}'", content, count=1)
        if count > 0:
            print(f"Updated agent {aid} -> deptId: {new_dept}")

    # 6. Update PERIODIC_AGENT_META and PERIODIC_GROUPS
    old_periodic_groups_pat = re.compile(r"const PERIODIC_GROUPS = \[.*?\];", re.DOTALL)
    new_periodic_groups = """const PERIODIC_GROUPS = [
      { id: 'demand_sop',          shortTab: 'Plan (V1)',            title: '01 · PLAN — DEMAND PLANNING, SENSING & S&OP (V1)',          color: '#10b981', count: 4 },
      { id: 'sourcing_procurement', shortTab: 'Source (V2)',          title: '02 · SOURCE — STRATEGIC SOURCING & PROCUREMENT (V2)',        color: '#a142f4', count: 4 },
      { id: 'manufacturing_prod',  shortTab: 'Make (V3)',            title: '03 · MAKE — PRODUCTION PLANNING & MANUFACTURING (V3)',       color: '#3b82f6', count: 4 },
      { id: 'inventory_meio',      shortTab: 'Inventory (V4)',       title: '04 · INVENTORY — MULTI-ECHELON BUFFER & MEIO (V4)',          color: '#06b6d4', count: 3 },
      { id: 'warehousing_qa',      shortTab: 'Warehouse (V5)',       title: '05 · WAREHOUSING — INWARDING QA & INTRALOGISTICS (V5)',      color: '#00d2ff', count: 3 },
      { id: 'logistics_fleet',     shortTab: 'Logistics (V6)',       title: '06 · LOGISTICS — MULTI-MODAL FLEET & TRANSIT (V6)',          color: '#ff8c00', count: 6 },
      { id: 'trade_mkt_dist',      shortTab: 'TM&D (V7)',            title: '07 · TM&D — TRADE MARKETING & DISTRIBUTION LAST-MILE (V7)',   color: '#f59e0b', count: 1 },
      { id: 'reverse_risk_esg',    shortTab: 'Reverse & ESG (V8)',   title: '08 · REVERSE & RISK — CIRCULAR RMA, OTIF & ESG (V8)',        color: '#ec4899', count: 3 },
      { id: 'universal_csco',      shortTab: 'Universal Core',       title: '00 · UNIVERSAL CROSS-PERSONA CSCO CONTROL TOWER CORE',       color: '#38bdf8', count: 4 }
    ];"""

    content, n_pg = old_periodic_groups_pat.subn(new_periodic_groups, content, count=1)
    if n_pg > 0:
        print("Updated PERIODIC_GROUPS with all 8 verticals + universal core.")

    # Update groups in PERIODIC_AGENT_META
    content = content.replace("group: 'sourcing_risk'", "group: 'sourcing_procurement'")
    content = content.replace("meio_safety_stock_agent:         { code: '401', sym: 'Ef', short: 'EchelonFlow',     group: 'inventory_warehouse'", "meio_safety_stock_agent:         { code: '401', sym: 'Ef', short: 'EchelonFlow',     group: 'inventory_meio'")
    content = content.replace("atp_order_promising_agent:       { code: '403', sym: 'Pg', short: 'PromiseGuard',    group: 'inventory_warehouse'", "atp_order_promising_agent:       { code: '402', sym: 'Pg', short: 'PromiseGuard',    group: 'inventory_meio'")
    content = content.replace("network_twin_architect:          { code: '604', sym: 'Td', short: 'TwinDesign',      group: 'circular_enable'", "network_twin_architect:          { code: '403', sym: 'Td', short: 'TwinDesign',      group: 'inventory_meio'")
    content = content.replace("warehouse_slotting_agent:        { code: '402', sym: 'Sm', short: 'SlotMaster 3D',   group: 'inventory_warehouse'", "warehouse_slotting_agent:        { code: '501', sym: 'Sm', short: 'SlotMaster 3D',   group: 'warehousing_qa'")
    content = content.replace("yard_dock_sequencer:             { code: '404', sym: 'Yp', short: 'YardPulse',       group: 'inventory_warehouse'", "yard_dock_sequencer:             { code: '502', sym: 'Yp', short: 'YardPulse',       group: 'warehousing_qa'")
    content = content.replace("crossdock_transfer_orchestrator: { code: '405', sym: 'Xd', short: 'CrossDockFlow',   group: 'inventory_warehouse'", "crossdock_transfer_orchestrator: { code: '503', sym: 'Xd', short: 'CrossDockFlow',   group: 'warehousing_qa'")
    content = content.replace("fleetflow_dispatch:              { code: '502', sym: 'Ff', short: 'FleetFlow Maps',  group: 'logistics_fleet'", "fleetflow_dispatch:              { code: '701', sym: 'Ff', short: 'FleetFlow Maps',  group: 'trade_mkt_dist'")
    content = content.replace("group: 'circular_enable'", "group: 'reverse_risk_esg'")

    # 7. Update getAgentSellingMeta proofs and savings
    content = content.replace(
        "sourcing_risk: 'Unilever ($100M+ productivity savings · 9 months → hours Tier-N supplier mapping across 60,000+ suppliers) & SAP Ariba / BigQuery Supply Chain Twin.',",
        "sourcing_procurement: 'Unilever ($100M+ productivity savings · 9 months → hours Tier-N supplier mapping across 60,000+ suppliers) & SAP Ariba / BigQuery Supply Chain Twin.',\n        sourcing_risk: 'Unilever ($100M+ productivity savings · 9 months → hours Tier-N supplier mapping across 60,000+ suppliers) & SAP Ariba / BigQuery Supply Chain Twin.',"
    )
    content = content.replace(
        "inventory_warehouse: 'FM Logistic (Google DeepMind AlphaEvolve + Vertex AI · -10% picker travel · +31% storage density) & Manhattan Active WMS.',",
        "inventory_meio: 'Multi-Echelon Network Deployments on BigQuery + Spanner (-18% working capital · $28M+ liquidity unlocked · 99.4% customer line fill).',\n        warehousing_qa: 'FM Logistic & Global High-Bay Deployments (AlphaEvolve + Vertex AI · -28% picker travel · <2.5h dock-to-stock · 99.8% pick accuracy).',\n        inventory_warehouse: 'FM Logistic (Google DeepMind AlphaEvolve + Vertex AI · -28% picker travel · <2.5h dock-to-stock) & Manhattan Active WMS.',"
    )
    content = content.replace(
        "circular_enable: 'CSCO Circular & ESG Operations on BigQuery + Cloud Spanner (+31% net RMA margin recovery, 99.6% audit-ready Scope 3 primary telemetry).'",
        "trade_mkt_dist: 'ITC Foods & FMCG Field Operations (Google Maps Platform + BigQuery · +18% distributor case fill rate · zero stockout pitch waste · 100% automated planogram audits).',\n        reverse_risk_esg: 'CSCO Circular & ESG Operations on BigQuery + Cloud Spanner (+31% net RMA margin recovery, 99.6% audit-ready Scope 3 primary telemetry).',\n        circular_enable: 'CSCO Circular & ESG Operations on BigQuery + Cloud Spanner (+31% net RMA margin recovery, 99.6% audit-ready Scope 3 primary telemetry).'"
    )

    # Update savingsByDept
    content = content.replace(
        "sourcing_risk: { val: '-6.8% ($18M+)', label: 'Direct Spend & Risk Savings', sub: 'Parametric should-cost negotiation & avoided line-down stops' },",
        "sourcing_procurement: { val: '-6.8% ($18M+)', label: 'Direct Spend & Risk Savings', sub: 'Parametric should-cost negotiation & avoided line-down stops' },\n        sourcing_risk: { val: '-6.8% ($18M+)', label: 'Direct Spend & Risk Savings', sub: 'Parametric should-cost negotiation & avoided line-down stops' },"
    )
    content = content.replace(
        "inventory_warehouse: { val: '-18% ($35M+)', label: 'Working Capital Cash Released', sub: 'Frees trapped safety stock while holding 99.4% customer fill rate' },",
        "inventory_meio: { val: '-18% ($28M+)', label: 'Working Capital Cash Released', sub: 'Frees trapped safety stock while holding 99.4% customer fill rate' },\n        warehousing_qa: { val: '-28% Travel', label: 'Dock & Pick Labor Productivity', sub: 'Cuts picker walking by 28% and speeds dock-to-stock from 14h to <2.5h' },\n        inventory_warehouse: { val: '-18% ($28M+)', label: 'Working Capital Cash Released', sub: 'Frees trapped safety stock while holding 99.4% customer fill rate' },"
    )
    content = content.replace(
        "circular_enable: { val: '-78% ($9M+)', label: 'OTIF Fines & Logistics Cost Saved', sub: 'Prevents retailer chargebacks & recovers +31% return margin' },",
        "trade_mkt_dist: { val: '+18% Fill Rate', label: 'Secondary Case Fill & Coverage', sub: 'Reconciles FSO beats with live distributor stock & cuts stockouts' },\n        reverse_risk_esg: { val: '-78% ($9M+)', label: 'OTIF Fines & Logistics Cost Saved', sub: 'Prevents retailer chargebacks & recovers +31% return margin' },\n        circular_enable: { val: '-78% ($9M+)', label: 'OTIF Fines & Logistics Cost Saved', sub: 'Prevents retailer chargebacks & recovers +31% return margin' },"
    )

    # 8. Add switchVerticalTab and runSSCalc in JS
    js_functions_to_insert = """
    /* 8-Vertical Interactive Master Navigation & Tab Controller */
    let currentFrontPageVerticalTab = 'all';

    function switchVerticalTab(vId, btnEl) {
      currentFrontPageVerticalTab = vId;
      document.querySelectorAll('#verticalTabsNavBar .v-tab-btn').forEach(b => {
        const isTarget = b.getAttribute('data-vtab') === vId;
        b.classList.toggle('active', isTarget);
      });

      if (vId === 'all') {
        selectedDeptId = null;
        document.querySelectorAll('#deptRowContainer .dept-node').forEach(node => {
          node.classList.remove('active');
          node.style.display = 'flex';
        });
        renderDepartmentShowcaseBox();
        const row = document.getElementById('deptRowContainer');
        if (row) row.scrollIntoView({ behavior: 'smooth', block: 'start' });
      } else {
        selectedDeptId = vId;
        document.querySelectorAll('#deptRowContainer .dept-node').forEach(node => {
          const nid = node.getAttribute('data-dept-id');
          const isTarget = nid === vId;
          node.classList.toggle('active', isTarget);
          node.style.display = 'flex'; // keep visible in 4x2 grid
        });
        renderDepartmentShowcaseBox();
        hydrateAssets();
        setTimeout(() => {
          const showcase = document.getElementById('deptShowcaseBoxEl');
          if (showcase) showcase.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 80);
      }
    }

    /* Live Interactive Safety Stock & ROP Calculator */
    function runSSCalc() {
      const elD = document.getElementById('rngD');
      const elLT = document.getElementById('rngLT');
      const elSLT = document.getElementById('rngSLT');
      if (!elD || !elLT || !elSLT) return;

      const D = parseFloat(elD.value);
      const LT = parseFloat(elLT.value);
      const sLT = parseFloat(elSLT.value);

      document.getElementById('lblD').innerText = D.toLocaleString();
      document.getElementById('lblLT').innerText = LT.toString();
      document.getElementById('lblSLT').innerText = sLT.toFixed(1);

      // Assume demand volatility is 15% of daily demand
      const sD = D * 0.15;
      const Z = 2.05; // 98% service level

      // Safety Stock formula: Z * sqrt( L * sD^2 + D^2 * sLT^2 )
      const varDemand = LT * Math.pow(sD, 2);
      const varLeadTime = Math.pow(D, 2) * Math.pow(sLT, 2);
      const ssUnits = Math.round(Z * Math.sqrt(varDemand + varLeadTime));
      const cycleStock = Math.round((D * LT) / 2);
      const ropUnits = Math.round(D * LT + ssUnits);

      // Percent driven by lead time volatility
      const pctLeadTimeRisk = Math.round((varLeadTime / (varDemand + varLeadTime)) * 100);

      const outEl = document.getElementById('ssOutput');
      if (outEl) {
        outEl.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:14px; margin-bottom:12px;">
            <div>
              <span style="color:#94a3b8; font-size:12px; text-transform:uppercase; letter-spacing:0.06em; font-weight:700;">Optimal Safety Stock (SS)</span>
              <div style="font-size:26px; font-weight:900; color:#38bdf8;">${ssUnits.toLocaleString()} Cases</div>
            </div>
            <div>
              <span style="color:#94a3b8; font-size:12px; text-transform:uppercase; letter-spacing:0.06em; font-weight:700;">Reorder Point (ROP)</span>
              <div style="font-size:26px; font-weight:900; color:#10b981;">${ropUnits.toLocaleString()} Cases</div>
            </div>
            <div>
              <span style="color:#94a3b8; font-size:12px; text-transform:uppercase; letter-spacing:0.06em; font-weight:700;">Working Capital Locked</span>
              <div style="font-size:26px; font-weight:900; color:#f59e0b;">$${Math.round((ssUnits * 42) / 1000).toLocaleString()}K</div>
            </div>
          </div>
          <div class="bar-line">
            <div class="bar-meta">
              <span>Lead-Time Volatility Risk Share: <strong style="color:#ec4899;">${pctLeadTimeRisk}%</strong></span>
              <span>Demand Volatility Share: <strong>${100 - pctLeadTimeRisk}%</strong></span>
            </div>
            <div class="bar-outer">
              <div class="bar-inner" style="width: ${pctLeadTimeRisk}%;"></div>
            </div>
          </div>
          <p style="color:#94a3b8; font-size:12px; margin-top:8px; line-height:1.5;">
            💡 <em>Executive Insight:</em> When supplier delivery dates drift by ±${sLT.toFixed(1)} days, lead-time uncertainty drives <strong>${pctLeadTimeRisk}%</strong> of your required buffer stock. Tightening vendor delivery variance via agentic PO monitoring cuts working capital far faster than forecasting tweaks.
          </p>
        `;
      }
    }
"""

    # Insert switchVerticalTab and runSSCalc right before renderOrgChart
    if "function renderOrgChart()" in content:
        content = content.replace("function renderOrgChart()", js_functions_to_insert + "\n    function renderOrgChart()", 1)
        print("Inserted switchVerticalTab and runSSCalc functions.")

    # 9. Update renderDepartmentShowcaseBox to render the 4-Quadrant Level-1 to Level-3 Decomposition Grid
    old_showcase_quad_target = """            <!-- Column 1: Problem / Manual Toil -->"""
    new_showcase_quad = """          <!-- 4-Quadrant Level-1 to Level-3 Process Decomposition Grid -->
          <div style="margin: 20px 0 14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
              <div style="font-size:16px; font-weight:800; color:#fff;">
                📑 Level-1 to Level-3 Operational Process Architecture &amp; Mandate
              </div>
              <div style="font-size:12px; color:var(--text-muted);">
                ${dept.horizon} · ${dept.river}
              </div>
            </div>
            <div class="quad-grid">
              <div class="quad-card">
                <h5>1. Operational Mandate</h5>
                <p style="font-size:13px; color:#cbd5e1; line-height:1.52;">${dept.l1toL3 ? dept.l1toL3.mandate : dept.subtitle}</p>
              </div>
              <div class="quad-card">
                <h5>2. Make-to-Stock vs. MTO Nuances</h5>
                <p style="font-size:13px; color:#cbd5e1; line-height:1.52;">${dept.l1toL3 ? dept.l1toL3.mtoVsMts : 'Postponement & multi-echelon buffering across regional distribution nodes.'}</p>
              </div>
              <div class="quad-card">
                <h5>3. Operational Battleground</h5>
                <p style="font-size:13px; color:#cbd5e1; line-height:1.52;">${dept.l1toL3 ? dept.l1toL3.battleground : 'Balancing operational uptime and service levels with lean working capital.'}</p>
              </div>
              <div class="quad-card">
                <h5>4. Core Enterprise Data Objects</h5>
                <p style="font-size:13px; color:#cbd5e1; line-height:1.52;">${dept.l1toL3 ? dept.l1toL3.dataObjects : dept.systems}</p>
              </div>
            </div>
          </div>

          <!-- Column 1: Problem / Manual Toil -->"""

    if old_showcase_quad_target in content:
        content = content.replace(old_showcase_quad_target, new_showcase_quad, 1)
        print("Updated renderDepartmentShowcaseBox with 4-Quadrant L1-L3 Process Decomposition Grid.")

    # 10. Update window onload to initialize runSSCalc
    if "hydrateAssets();" in content:
        content = content.replace("hydrateAssets();", "hydrateAssets();\n      runSSCalc();", 1)
        print("Hooked runSSCalc into asset hydration.")

    # Write updated file
    BUILD_SITE_PATH.write_text(content, encoding="utf-8")
    print(f"Successfully updated {BUILD_SITE_PATH}")

if __name__ == "__main__":
    main()

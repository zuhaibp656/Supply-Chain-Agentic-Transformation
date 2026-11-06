#!/usr/bin/env python3
"""Generates the Simplified, Human-Understandable Supply Chain Agent Playbook:
1. AGENT_TESTING_AND_VIDEO_PLAYBOOK.md (Root & docs/)
2. agent_testing_and_video_playbook.html (Root, docs/, zipline_dist/)

Design Principles requested by user & manager (Kiran):
- Simple, clear, human-understandable flow for every one of the 60 agents.
- Real-world business use cases (plain English, no developer jargon).
- Connected Enterprise Systems & Connectors (SAP, BigQuery, Manhattan WMS, Oracle OTM, Siemens MES) — ZERO messy database table name dumps.
- 3 Realistic, high-impact business prompts per agent (Operational Diagnostic, Visual Analytics, Executive Decision Brief) tailored to authentic Indian enterprise supply chain networks (DMart, Reliance, Blinkit, Bhiwandi Mega DC, Chakan Auto Plant, Nelamangala RDC, Mundra Port, JNPT).
"""

import json
import html
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "data" / "supply_chain_catalog.json"

PILLAR_METAS = [
    ("demand_sop", "01 · Planning & Strategy", "#3b82f6", "Demand Forecasting, Trade Promotion, S&OP / IBP, Portfolio & SKU"),
    ("sourcing_procurement", "02 · Sourcing & Procurement", "#f59e0b", "Supplier Network, Material & Packaging, Contract & PO Management"),
    ("manufacturing_prod", "03 · Manufacturing & Production", "#8b5cf6", "Production Scheduling, Capacity Planning, Quality & Compliance"),
    ("inventory_warehouse", "04 · Inventory & Warehousing", "#10b981", "Positioning & Optimization (MEIO), 3D Warehouse Operations, Omnichannel ATP"),
    ("logistics_fleet", "05 · Distribution & Logistics", "#06b6d4", "First & Mid-Mile, Store Replenishment, Last-Mile Delivery, Route & Carrier"),
    ("circular_enable", "06 · Returns & Reverse Logistics", "#f43f5e", "Returns & Claims Management, Expiry & Markdowns, Pallet & Tote Reclamation"),
]

def load_catalog():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# High-level system connector mapping per pillar / domain
PILLAR_CONNECTORS = {
    "demand_sop": [
        ("🛒 SAP S/4HANA (SD/MM)", "Pulls daily store checkout scans (EDI 852), open customer orders, and baseline ERP demand forecasts."),
        ("☁️ BigQuery Demand Lake", "Streams real-time weather anomalies (Google DeepMind WeatherNext), foot-traffic indices, and channel sales."),
        ("🧠 Vertex AI TimesFM", "Foundation time-series forecasting model generating probabilistic P10/P50/P90 demand envelopes."),
        ("📊 SAP IBP", "Reconciles unconstrained commercial plans and publishes approved consensus forecast key figures."),
    ],
    "sourcing_procurement": [
        ("🤝 SAP Ariba", "Manages supplier master agreements, active RFQ bid sheets, and multi-tier vendor compliance records."),
        ("📈 Commodity Indices (LME/ICIS)", "Live spot and futures market benchmarks for aluminum, steel, polymer resins, and corrugated packaging."),
        ("🕸️ Cloud Spanner Graph", "Multi-tier supply chain graph tracing Tier-1 to Tier-3 component lineage and sole-source bottlenecks."),
        ("📑 Accounts Payable OCR / EDI 810", "Automated 3-way matching across purchase orders, receiving dock receipts, and vendor invoices."),
    ],
    "manufacturing_prod": [
        ("⚙️ Siemens Opcenter MES", "Live plant machine work center status, run rates, job dispatch queues, and maintenance schedules."),
        ("🏭 SAP PP/DS", "Planned production orders, bill of material routings, and plant line capacity envelopes."),
        ("📡 SCADA / IoT Vibration Telemetry", "Industrial vibration FFT spectrograms, bearing temperatures, and predictive failure alarms."),
        ("🎯 Google OR-Tools CP-SAT", "Finite capacity constraint solver minimizing sequence-dependent wash and changeover downtime."),
    ],
    "inventory_warehouse": [
        ("📦 Manhattan Active WMS", "Real-time bin/aisle slotting, picker travel telemetry, wave release queues, and dock door schedules."),
        ("🌐 Cloud Spanner ATP", "Sub-50ms distributed transactional ledger maintaining committed customer orders and available inventory."),
        ("⚖️ Clark-Scarf MEIO Optimizer", "Coupled stochastic inventory solver balancing safety stock across Plants, RDCs, and Dark Stores."),
        ("🏢 SAP EWM", "Plant-to-warehouse stock transfer orders, pallet serialization, and inventory reconciliation."),
    ],
    "logistics_fleet": [
        ("🚚 Oracle OTM", "Outbound freight shipment orders, load tenders, rate tariffs, and carrier contractual commitments."),
        ("🗺️ Google Maps Routes Preferred", "Real-time highway traffic matrix, bridge height clearances, and dynamic corridor routing."),
        ("🛰️ Samsara ELD & IoT Telematics", "Live GPS truck tracking, driver Hours-of-Service (HOS) clocks, and continuous reefer temperature probes."),
        ("🚛 Google OR-Tools VRPTW", "Capacitated Vehicle Routing Problem solver with strict customer delivery time windows."),
    ],
    "circular_enable": [
        ("🔄 SAP Customer Returns (SD/LE)", "Automated customer RMA intake, warranty claims, and credit memo release processing."),
        ("🏷️ Zebra RFID Dock Portals", "High-speed dock door RFID scanners tracking reusable transport items (pallets, totes, and cages)."),
        ("🌱 BigQuery Scope-3 ESG Ledger", "GLEC-compliant carbon emission accounting, CBAM embedded carbon, and EUDR deforestation audits."),
        ("💰 Dynamic Markdown Optimizer", "Price elasticity model balancing clearance markdown depth against charitable food bank tax deductions."),
    ]
}

def get_re_id(ag_id, cat):
    ag = cat.get("agents", {}).get(ag_id, {})
    return ag.get("reasoningEngineId") or ag.get("adkImplementation", {}).get("reasoningEngineId", "")

def generate_playbook():
    cat = load_catalog()
    agents = cat.get("agents", {})

    try:
        from human_plain_english_prompts import HUMAN_AGENT_PROMPTS
    except ImportError:
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        from human_plain_english_prompts import HUMAN_AGENT_PROMPTS

    md_lines = [
        "# 🎬 Supply Chain AI Agents — Complete Testing, Demo Data & Video Recording Playbook",
        "",
        "> **Executive Summary for Leadership & Evaluators**:",
        "> This Playbook provides a clear, human-understandable walkthrough for all **60 Supply Chain AI Agents** spanning the 6 ASCM SCOR Operating Pillars.",
        "> For each agent, you will find:",
        "> 1. **The Real-World Business Use Case**: What specific operational problem it solves in plain English.",
        "> 2. **Connected Enterprise Systems & Data Sources**: Simple enterprise connectors (SAP, BigQuery, Manhattan WMS, Oracle OTM, Siemens MES) — zero raw SQL table clutter.",
        "> 3. **The 3-Step Execution Flow**: How the agent ingests data, solves constraints, and executes safe writebacks.",
        "> 4. **3 Realistic High-Impact Business Prompts**: Authentic plain-English questions you can paste directly into Gemini Enterprise or the local ADK chat.",
        "",
        "---",
        ""
    ]

    html_cards = []
    agent_idx = 0

    for dept_id, pillar_title, pillar_color, pillar_subtext in PILLAR_METAS:
        pillar_agents = [ag for ag in agents.values() if ag.get("deptId") == dept_id]
        md_lines.append(f"## {pillar_title} ({len(pillar_agents)} Agents)")
        md_lines.append(f"*{pillar_subtext}*")
        md_lines.append("")

        for ag in pillar_agents:
            agent_idx += 1
            ag_id = ag["id"]
            name = ag.get("name", ag_id)
            sub_pillar = ag.get("subPillarName") or "General"
            persona = ag.get("primaryPersonaName") or "Supply Chain Lead"
            roi_badge = ag.get("badge") or "Verified ROI"
            re_id = get_re_id(ag_id, cat)

            # Problems and solutions
            problem = ag.get("problem") or "Disconnected enterprise systems and manual spreadsheet analysis cause operational delays, stockouts, or cost overruns."
            solution = ag.get("solution") or "Autonomously synthesizes real-time enterprise signals, applies mathematical solvers, and executes governed write-backs."
            outcome = ag.get("outcome") or "Delivers measurable cost savings, protects revenue, and eliminates manual toil."

            # Prompts
            prompts = HUMAN_AGENT_PROMPTS.get(ag_id, {})
            q1 = prompts.get("q1") or f"Audit active operational records for {name} across our primary regional hubs, detect discrepancies, and output a copy-ready CSV schedule."
            q2 = prompts.get("q2") or f"Generate an interactive visual comparison chart for {name} illustrating key variances, bottlenecks, and optimization recommendations."
            q3 = prompts.get("q3") or f"Draft an executive briefing memorandum and interactive HTML cockpit for supply chain leadership detailing financial impact and recommended decisions."

            connectors = PILLAR_CONNECTORS.get(dept_id, PILLAR_CONNECTORS["demand_sop"])

            # Build Markdown
            cloud_badge = f" · 🟢 **Cloud-Deployed (RE: `{re_id.split('/')[-1][:12]}...`)**" if re_id else " · 📦 **High-Code ADK Package**"
            md_lines.extend([
                f"### #{agent_idx:02d} · {name} (`{ag_id}`)",
                f"- **Sub-Pillar**: {sub_pillar} | **Pillar**: {pillar_title}",
                f"- **Primary Human Persona**: {persona} · **ROI Benchmark**: `{roi_badge}`{cloud_badge}",
                "",
                "#### 🎯 1. Real-World Business Use Case",
                f"- **The Business Problem**: {problem}",
                f"- **The AI Solution**: {solution}",
                f"- **Quantified Outcome**: {outcome}",
                "",
                "#### 🔌 2. Connected Enterprise Systems & Data Sources",
            ])
            for sys_icon, sys_desc in connectors:
                md_lines.append(f"- **{sys_icon}**: {sys_desc}")

            md_lines.extend([
                "",
                "#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)",
                f"1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors ({connectors[0][0].split()[1]} and {connectors[1][0].split()[1]}) without asking the user for technical table names or SQL parameters.",
                f"2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers ({connectors[2][0].split()[1]}) to identify the optimal action plan.",
                f"3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback ({connectors[3][0].split()[1]}).",
                "",
                "#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)",
                f"- **Prompt 1 · Operational Diagnostic & Reconciliation**:",
                f"  > `{q1}`",
                f"- **Prompt 2 · Visual Analytics & Comparison Chart**:",
                f"  > `{q2}`",
                f"- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:",
                f"  > `{q3}`",
                "",
                "```bash",
                f"# Run full autonomous scenario & print copy-ready table:",
                f"python3 scripts/test_agent_demo.py {ag_id}",
                "```",
                "",
                "---",
                ""
            ])

            # Build HTML Card
            connectors_html = "".join([f"""
              <div class="pb-conn-item">
                <span class="pb-conn-tag">{html.escape(c[0])}</span>
                <span class="pb-conn-desc">{html.escape(c[1])}</span>
              </div>
            """ for c in connectors])

            cloud_pill = (
                f'<span class="pb-badge" style="background:rgba(16,185,129,0.16); color:#10b981; border-color:rgba(16,185,129,0.4);">🟢 Cloud Deployed</span>'
                if re_id else
                '<span class="pb-badge">📦 Local ADK Package Ready</span>'
            )

            html_cards.append(f"""
              <article class="pb-agent-card" id="agent-{ag_id}" data-pillar="{dept_id}" data-cloud="{'true' if re_id else 'false'}" style="--pillar-color:{pillar_color};">
                <div class="pb-card-header">
                  <div>
                    <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:6px;">
                      <span class="pb-badge" style="color:{pillar_color}; border-color:{pillar_color}55;">#{agent_idx:02d} · {html.escape(pillar_title)}</span>
                      <span class="pb-badge">{html.escape(sub_pillar)}</span>
                      <span class="pb-badge">👤 {html.escape(persona)}</span>
                      {cloud_pill}
                    </div>
                    <h2 class="pb-agent-title">{html.escape(name)} <code style="font-size:14px; color:var(--text-secondary); font-weight:600;">({ag_id})</code></h2>
                  </div>
                  <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                    <span class="pb-roi-pill">🚀 {html.escape(roi_badge)}</span>
                    <a href="index.html#agent/{ag_id}" class="pb-link-btn">Open Agent Page ↗</a>
                  </div>
                </div>

                <!-- 1. Real-World Business Use Case -->
                <div class="pb-what-box">
                  <div class="pb-section-kicker">🎯 1 · REAL-WORLD BUSINESS USE CASE</div>
                  <div class="pb-what-grid">
                    <div class="pb-what-item">
                      <span class="pb-what-label" style="color:#fb7185;">✕ The Business Problem</span>
                      <p>{html.escape(problem)}</p>
                    </div>
                    <div class="pb-what-item">
                      <span class="pb-what-label" style="color:#38bdf8;">✦ How the Agent Works</span>
                      <p>{html.escape(solution)}</p>
                    </div>
                    <div class="pb-what-item">
                      <span class="pb-what-label" style="color:#10b981;">🚀 Quantified Outcome</span>
                      <p>{html.escape(outcome)}</p>
                    </div>
                  </div>
                </div>

                <div class="pb-two-col">
                  <!-- 2. Connected Enterprise Systems -->
                  <div class="pb-panel">
                    <div class="pb-section-kicker">🔌 2 · CONNECTED ENTERPRISE SYSTEMS &amp; DATA SOURCES</div>
                    <div style="display:flex; flex-direction:column; gap:8px;">
                      {connectors_html}
                    </div>

                    <div style="margin-top:14px; padding:12px; border-radius:8px; background:rgba(56,189,248,0.06); border:1px solid rgba(56,189,248,0.2);">
                      <div style="font-size:11.5px; font-weight:800; color:#38bdf8; text-transform:uppercase; margin-bottom:4px; font-family:var(--font-mono);">🔄 3-Step Execution Flow</div>
                      <div style="font-size:13px; color:var(--text-secondary); line-height:1.5;">
                        <strong>1. Ingest:</strong> Checks live ERP/WMS transactions &rarr; 
                        <strong>2. Optimize:</strong> Solves constraints with zero human toil &rarr; 
                        <strong>3. Action:</strong> Generates visual charts, copy-ready CSVs &amp; verified ERP write-backs.
                      </div>
                    </div>
                  </div>

                  <!-- 3. Realistic High-Impact Business Prompts -->
                  <div class="pb-panel">
                    <div class="pb-section-kicker">💬 3 · REALISTIC HIGH-IMPACT BUSINESS PROMPTS (ACTUAL USE CASES)</div>
                    
                    <div class="pb-prompt-block">
                      <div class="pb-prompt-head">
                        <span class="pb-prompt-tag">Mode 1 · Operational Diagnostic</span>
                        <button type="button" class="pb-copy-btn" data-copy="{html.escape(q1)}" onclick="copyPlaybookText(this)">📋 Copy Prompt</button>
                      </div>
                      <div class="pb-prompt-text">“{html.escape(q1)}”</div>
                    </div>

                    <div class="pb-prompt-block">
                      <div class="pb-prompt-head">
                        <span class="pb-prompt-tag">Mode 2 · Visual Analytics &amp; Chart</span>
                        <button type="button" class="pb-copy-btn" data-copy="{html.escape(q2)}" onclick="copyPlaybookText(this)">📋 Copy Prompt</button>
                      </div>
                      <div class="pb-prompt-text">“{html.escape(q2)}”</div>
                    </div>

                    <div class="pb-prompt-block">
                      <div class="pb-prompt-head">
                        <span class="pb-prompt-tag">Mode 3 · Executive Decision Brief</span>
                        <button type="button" class="pb-copy-btn" data-copy="{html.escape(q3)}" onclick="copyPlaybookText(this)">📋 Copy Prompt</button>
                      </div>
                      <div class="pb-prompt-text">“{html.escape(q3)}”</div>
                    </div>

                    <div style="margin-top:10px;">
                      <button type="button" class="pb-copy-btn" style="width:100%; text-align:center;" data-copy="python3 scripts/test_agent_demo.py {ag_id}" onclick="copyPlaybookText(this)">
                        💻 Copy CLI Run Command: <code>python3 scripts/test_agent_demo.py {ag_id}</code>
                      </button>
                    </div>
                  </div>
                </div>
              </article>
            """)

    # Write Markdown Playbook
    md_content = "\n".join(md_lines)
    (ROOT / "AGENT_TESTING_AND_VIDEO_PLAYBOOK.md").write_text(md_content, encoding="utf-8")
    (ROOT / "docs" / "AGENT_TESTING_AND_VIDEO_PLAYBOOK.md").write_text(md_content, encoding="utf-8")
    print("✅ Wrote simplified AGENT_TESTING_AND_VIDEO_PLAYBOOK.md (root & docs/)")

    # Build Complete HTML Playbook
    playbook_html = f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Supply Chain AI Agents — Executive Playbook &amp; Use-Case Guide</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Google+Sans+Display:wght@500;700;800&family=Google+Sans+Text:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-base: #060911;
      --bg-surface: #0c1220;
      --bg-card: #131b2e;
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-strong: rgba(255, 255, 255, 0.16);
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --font-display: 'Google Sans Display', -apple-system, sans-serif;
      --font-body: 'Google Sans Text', -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}
    html[data-theme="light"] {{
      --bg-base: #f0f4fa;
      --bg-surface: #ffffff;
      --bg-card: #ffffff;
      --border-subtle: rgba(0, 0, 0, 0.08);
      --border-strong: rgba(0, 0, 0, 0.16);
      --text-primary: #0f172a;
      --text-secondary: #475569;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      background: var(--bg-base);
      color: var(--text-primary);
      font-family: var(--font-body);
      line-height: 1.5;
    }}
    .pb-navbar {{
      position: sticky;
      top: 0;
      z-index: 100;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 14px 28px;
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-subtle);
      backdrop-filter: blur(12px);
    }}
    .pb-container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 32px 24px 60px;
    }}
    .pb-hero {{
      margin-bottom: 28px;
      padding: 28px 32px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
    }}
    .pb-badge {{
      display: inline-flex;
      align-items: center;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      font-family: var(--font-mono);
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border-subtle);
    }}
    .pb-filter-bar {{
      position: sticky;
      top: 65px;
      z-index: 90;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
      padding: 12px 18px;
      margin-bottom: 24px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
    }}
    .pb-filter-btn {{
      padding: 8px 14px;
      border-radius: 8px;
      border: 1px solid var(--border-subtle);
      background: transparent;
      color: var(--text-secondary);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .pb-filter-btn:hover, .pb-filter-btn.active {{
      background: #38bdf8;
      color: #060911;
      border-color: #38bdf8;
    }}
    .pb-agent-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-left: 5px solid var(--pillar-color, #38bdf8);
      border-radius: 14px;
      padding: 24px;
      margin-bottom: 24px;
    }}
    .pb-card-header {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
      margin-bottom: 18px;
    }}
    .pb-agent-title {{
      font-family: var(--font-display);
      font-size: 22px;
      font-weight: 700;
      margin: 0;
    }}
    .pb-roi-pill {{
      padding: 5px 12px;
      border-radius: 20px;
      background: rgba(16, 185, 129, 0.14);
      color: #10b981;
      border: 1px solid rgba(16, 185, 129, 0.35);
      font-weight: 700;
      font-size: 13px;
    }}
    .pb-link-btn {{
      padding: 6px 12px;
      border-radius: 8px;
      background: rgba(56, 189, 248, 0.12);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.3);
      font-size: 12.5px;
      font-weight: 700;
      text-decoration: none;
    }}
    .pb-section-kicker {{
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 800;
      color: var(--text-secondary);
      letter-spacing: 0.08em;
      margin-bottom: 10px;
    }}
    .pb-what-box {{
      padding: 16px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      margin-bottom: 16px;
    }}
    .pb-what-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 14px;
    }}
    .pb-what-item p {{
      margin: 4px 0 0;
      font-size: 14px;
      color: var(--text-primary);
      line-height: 1.45;
    }}
    .pb-what-label {{
      font-size: 11.5px;
      font-weight: 800;
      text-transform: uppercase;
      font-family: var(--font-mono);
    }}
    .pb-two-col {{
      display: grid;
      grid-template-columns: 1fr 1.2fr;
      gap: 16px;
    }}
    @media (max-width: 980px) {{
      .pb-two-col {{ grid-template-columns: 1fr; }}
    }}
    .pb-panel {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 16px;
    }}
    .pb-conn-item {{
      display: flex;
      flex-direction: column;
      gap: 2px;
      padding: 6px 8px;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.03);
    }}
    .pb-conn-tag {{
      font-size: 12.5px;
      font-weight: 700;
      color: #38bdf8;
    }}
    .pb-conn-desc {{
      font-size: 12.5px;
      color: var(--text-secondary);
    }}
    .pb-prompt-block {{
      margin-bottom: 10px;
      padding: 10px 12px;
      border-radius: 8px;
      background: rgba(0, 0, 0, 0.2);
      border: 1px solid var(--border-subtle);
    }}
    .pb-prompt-head {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      margin-bottom: 4px;
    }}
    .pb-prompt-tag {{
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      color: #fbbf24;
      font-family: var(--font-mono);
    }}
    .pb-prompt-text {{
      font-size: 13.5px;
      font-weight: 500;
      color: var(--text-primary);
      line-height: 1.45;
    }}
    .pb-copy-btn {{
      padding: 4px 8px;
      border-radius: 5px;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
      font-size: 11.5px;
      font-weight: 700;
      cursor: pointer;
      transition: background 0.15s;
    }}
    .pb-copy-btn:hover {{
      background: #38bdf8;
      color: #060911;
    }}
  </style>
</head>
<body>
  <header class="pb-navbar">
    <div style="display:flex; align-items:center; gap:14px;">
      <a href="index.html" style="text-decoration:none; color:var(--text-primary); font-family:var(--font-display); font-size:20px; font-weight:800;">
        &larr; Back to Supply Chain Portal
      </a>
      <span class="pb-badge" style="color:#38bdf8; border-color:rgba(56,189,248,0.4);">🎬 60-Agent Executive Playbook</span>
    </div>
    <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
      <a href="periodic_table.html" class="pb-filter-btn" style="text-decoration:none;">Periodic Table</a>
      <a href="mind_map.html" class="pb-filter-btn" style="text-decoration:none;">Neural Mind Map</a>
      <button type="button" class="pb-filter-btn" onclick="document.documentElement.setAttribute('data-theme', document.documentElement.getAttribute('data-theme')==='light'?'dark':'light')">
        🌗 Theme
      </button>
    </div>
  </header>

  <main class="pb-container">
    <section class="pb-hero">
      <div style="font-family:var(--font-mono); font-size:12px; font-weight:800; color:#38bdf8; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">
        EXECUTIVE USE-CASE &amp; PROMPT TESTING PLAYBOOK
      </div>
      <h1 style="font-family:var(--font-display); font-size:clamp(26px, 3vw, 36px); margin:0 0 10px;">
        The 60 Supply Chain AI Agents: Plain-English Flow &amp; Testing Guide
      </h1>
      <p style="font-size:15px; color:var(--text-secondary); margin:0; max-width:1100px;">
        Designed for leadership, business teams, and evaluators. For every agent, this guide presents: 
        <strong>(1) The Business Use Case</strong> in plain English, 
        <strong>(2) Connected Enterprise Systems</strong> (SAP, BigQuery, Manhattan WMS, Oracle OTM, Siemens MES) without database clutter, 
        <strong>(3) The 3-Step Execution Flow</strong>, and 
        <strong>(4) 3 Realistic High-Impact Business Prompts</strong> ready to copy and run.
      </p>
    </section>

    <div class="pb-filter-bar">
      <div style="display:flex; gap:8px; flex-wrap:wrap;">
        <button type="button" class="pb-filter-btn active" onclick="filterPlaybook('all', this)">All 60 Agents</button>
        <button type="button" class="pb-filter-btn" onclick="filterPlaybook('demand_sop', this)">01 · Plan</button>
        <button type="button" class="pb-filter-btn" onclick="filterPlaybook('sourcing_procurement', this)">02 · Source</button>
        <button type="button" class="pb-filter-btn" onclick="filterPlaybook('manufacturing_prod', this)">03 · Make</button>
        <button type="button" class="pb-filter-btn" onclick="filterPlaybook('inventory_warehouse', this)">04 · Inventory &amp; DC</button>
        <button type="button" class="pb-filter-btn" onclick="filterPlaybook('logistics_fleet', this)">05 · Logistics</button>
        <button type="button" class="pb-filter-btn" onclick="filterPlaybook('circular_enable', this)">06 · Returns &amp; ESG</button>
      </div>
      <input type="search" id="pbSearchInput" style="padding:8px 12px; border-radius:8px; background:var(--bg-card); border:1px solid var(--border-subtle); color:var(--text-primary); width:280px;" placeholder="🔍 Filter by agent or persona…" oninput="filterPlaybookSearch()" />
    </div>

    <div id="pbCardsContainer">
      {''.join(html_cards)}
    </div>
  </main>

  <script>
    let currentPillar = 'all';
    function copyPlaybookText(btn) {{
      const txt = btn.getAttribute('data-copy') || '';
      navigator.clipboard.writeText(txt);
      const orig = btn.innerHTML;
      btn.innerHTML = '✅ Copied!';
      setTimeout(() => {{ btn.innerHTML = orig; }}, 1400);
    }}
    function filterPlaybook(p, btn) {{
      currentPillar = p;
      document.querySelectorAll('.pb-filter-bar .pb-filter-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      applyFilter();
    }}
    function filterPlaybookSearch() {{
      applyFilter();
    }}
    function applyFilter() {{
      const q = (document.getElementById('pbSearchInput').value || '').toLowerCase().trim();
      document.querySelectorAll('.pb-agent-card').forEach(card => {{
        const pillMatch = (currentPillar === 'all' || card.getAttribute('data-pillar') === currentPillar);
        const textMatch = !q || card.textContent.toLowerCase().includes(q);
        card.style.display = (pillMatch && textMatch) ? 'block' : 'none';
      }});
    }}
  </script>
</body>
</html>
"""
    (ROOT / "agent_testing_and_video_playbook.html").write_text(playbook_html, encoding="utf-8")
    for sub in ["docs", "zipline_dist"]:
        d = ROOT / sub
        if d.exists():
            (d / "agent_testing_and_video_playbook.html").write_text(playbook_html, encoding="utf-8")
    print("✅ Wrote simplified agent_testing_and_video_playbook.html (root, docs/, zipline_dist/)")

if __name__ == "__main__":
    generate_playbook()

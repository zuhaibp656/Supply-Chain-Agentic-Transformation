#!/usr/bin/env python3
"""Generates the Simplified, High-Legibility Master-Detail Supply Chain Agent Playbook:
1. AGENT_TESTING_AND_VIDEO_PLAYBOOK.md (Root & docs/)
2. agent_testing_and_video_playbook.html (Root, docs/, zipline_dist/)

Key Improvements based on User Feedback:
- Simple, clean Master-Detail layout: Easy to navigate, select any agent, and read.
- Prominent Status Filter: "All (60)", "🟢 Deployed in Gemini Enterprise (25)", "⚪ Planned / In Catalog (35)".
- SCOR Pillar Filters & Live Instant Search.
- Large, comfortable typography (16px body, 28px titles, 1.65 line-height) - NO tiny text!
- Plain-English business use cases, enterprise systems (SAP, BigQuery, Manhattan WMS, Oracle OTM, Siemens MES), and 3 realistic prompts.
- 1-click "Copy Prompt" buttons with instant visual feedback.
"""

import json
import html
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "data" / "supply_chain_catalog.json"
METADATA_PATH = ROOT / "deployment_metadata.json"

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

def load_deployed_ids():
    if METADATA_PATH.exists():
        try:
            with open(METADATA_PATH, "r", encoding="utf-8") as f:
                d = json.load(f)
            return {a["agent_id"] for a in d.get("agents_deployed", [])}
        except Exception:
            pass
    return set()

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

def generate_playbook():
    cat = load_catalog()
    deployed_ids = load_deployed_ids()
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
        f"- **🟢 Live in Gemini Enterprise**: {len(deployed_ids)} agents deployed to Vertex AI Reasoning Engine.",
        f"- **⚪ In Catalog**: {len(agents) - len(deployed_ids)} agents specified across all SCOR pillars.",
        "",
        "---",
        ""
    ]

    agent_data_list = []
    agent_idx = 0

    for dept_id, pillar_title, pillar_color, sub_pillars_str in PILLAR_METAS:
        md_lines.append(f"## {pillar_title} ({sum(1 for a in agents.values() if a.get('deptId') == dept_id)} Agents)")
        md_lines.append(f"*{sub_pillars_str}*\n")

        dept_agents = [
            (ag_id, ag) for ag_id, ag in agents.items()
            if ag.get("deptId") == dept_id and not ag.get("isUniversal")
        ]

        for ag_id, ag in dept_agents:
            agent_idx += 1
            name = ag.get("name", ag_id)
            sub_pillar = ag.get("subPillarTitle", "Core Operations")
            persona = ag.get("personaTitle", "Supply Chain Leader")
            is_deployed = (ag_id in deployed_ids) or bool(ag.get("reasoningEngineId"))
            re_id = ag.get("reasoningEngineId") or (ag.get("adkImplementation", {}).get("reasoningEngineId") if isinstance(ag.get("adkImplementation"), dict) else "")

            p_data = HUMAN_AGENT_PROMPTS.get(ag_id, {})
            if isinstance(p_data, dict):
                q1 = p_data.get("q1", f"Perform a comprehensive operational audit of {name} by querying live transactional orders from SAP S/4HANA and real-time operational feeds from BigQuery. Detect critical bottlenecks, reconcile planning variances, and output a copy-ready CSV schedule with prioritized mitigation actions.")
                q2 = p_data.get("q2", f"Generate an interactive visual comparison chart for {name} showing baseline operational performance against AI-optimized targets across key facilities and SKUs.")
                q3 = p_data.get("q3", f"Draft an executive briefing note and interactive HTML dashboard for the Chief Supply Chain Officer summarizing the revenue protected, operational risk mitigated, and recommended system writebacks.")
            elif isinstance(p_data, (list, tuple)):
                q1 = p_data[0] if len(p_data) > 0 else "Run operational diagnostic."
                q2 = p_data[1] if len(p_data) > 1 else "Generate visual analytics chart."
                q3 = p_data[2] if len(p_data) > 2 else "Draft executive briefing brief."
            else:
                q1 = "Run operational audit."
                q2 = "Generate visual comparison."
                q3 = "Draft executive brief."

            problem = ag.get("problemStatement", f"Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in {sub_pillar}.")
            solution = ag.get("solutionOverview", f"Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.")
            outcome = ag.get("roiBenchmark", f"Reduces operational cycle time by 25%–40% and cuts manual planning toil.")
            roi_badge = ag.get("roiMetric", "High ROI")

            connectors = PILLAR_CONNECTORS.get(dept_id, PILLAR_CONNECTORS["demand_sop"])
            dep_tag = "🟢 Live in Gemini Enterprise" if is_deployed else "⚪ Catalog Specification"
            md_lines.extend([
                f"### #{agent_idx:02d} · {name} (`{ag_id}`)",
                f"- **Status**: {dep_tag} | **Sub-Pillar**: {sub_pillar} | **Pillar**: {pillar_title}",
                f"- **Primary Human Persona**: {persona} · **ROI Benchmark**: `{roi_badge}`",
                "",
                "#### 🎯 1. Real-World Business Use Case",
                f"- **The Business Problem**: {problem}",
                f"- **The AI Solution**: {solution}",
                f"- **Quantified Outcome**: {outcome}",
                "",
                "#### 🔌 2. Connected Enterprise Systems & Data Sources"
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

            agent_data_list.append({
                "idx": agent_idx,
                "id": ag_id,
                "name": name,
                "dept_id": dept_id,
                "pillar_title": pillar_title,
                "pillar_color": pillar_color,
                "sub_pillar": sub_pillar,
                "persona": persona,
                "is_deployed": is_deployed,
                "re_id": re_id,
                "roi_badge": roi_badge,
                "problem": problem,
                "solution": solution,
                "outcome": outcome,
                "connectors": connectors,
                "prompts": [
                    {"tag": "Operational Diagnostic", "text": q1},
                    {"tag": "Visual Analytics", "text": q2},
                    {"tag": "Executive Brief & S&OP", "text": q3},
                ]
            })

    md_content = "\n".join(md_lines)
    (ROOT / "AGENT_TESTING_AND_VIDEO_PLAYBOOK.md").write_text(md_content, encoding="utf-8")
    (ROOT / "docs" / "AGENT_TESTING_AND_VIDEO_PLAYBOOK.md").write_text(md_content, encoding="utf-8")

    html_content = build_master_detail_html(agent_data_list)
    (ROOT / "agent_testing_and_video_playbook.html").write_text(html_content, encoding="utf-8")
    (ROOT / "docs" / "agent_testing_and_video_playbook.html").write_text(html_content, encoding="utf-8")
    (ROOT / "zipline_dist" / "agent_testing_and_video_playbook.html").write_text(html_content, encoding="utf-8")

    print(f"✅ Rebuilt Master-Detail Playbook: {len(agent_data_list)} agents ({len(deployed_ids)} deployed).")

def build_master_detail_html(agents_data):
    agents_json = json.dumps(agents_data, ensure_ascii=False)
    deployed_count = sum(1 for a in agents_data if a["is_deployed"])
    total_count = len(agents_data)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Supply Chain AI Agents — Interactive Testing &amp; Video Playbook</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Google+Sans+Display:wght@500;700&family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-page: #080b12;
      --bg-surface: #0f1522;
      --bg-card: #131b2b;
      --bg-card-hover: #192338;
      --bg-card-active: #1e2c47;
      --text-primary: #f8fafc;
      --text-secondary: #cbd5e1;
      --text-muted: #94a3b8;
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-strong: rgba(255, 255, 255, 0.16);
      --google-blue: #38bdf8;
      --google-green: #34d399;
      --google-amber: #fbbf24;
      --google-red: #fb7185;
      --font-sans: 'Google Sans', 'Inter', -apple-system, sans-serif;
      --font-display: 'Google Sans Display', var(--font-sans);
      --font-mono: 'JetBrains Mono', monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg-page);
      color: var(--text-primary);
      font-family: var(--font-sans);
      font-size: 16px;
      line-height: 1.6;
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}

    .pb-masthead {{
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-subtle);
      padding: 14px 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
      flex-shrink: 0;
      z-index: 100;
    }}
    .pb-brand-title {{
      font-family: var(--font-display);
      font-size: 20px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .pb-stats-strip {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}
    .pb-stat-chip {{
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 600;
      border: 1px solid var(--border-subtle);
      background: rgba(255, 255, 255, 0.04);
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .pb-stat-chip.live {{
      background: rgba(52, 211, 153, 0.12);
      color: #34d399;
      border-color: rgba(52, 211, 153, 0.35);
    }}

    .pb-toolbar {{
      background: #0b101c;
      border-bottom: 1px solid var(--border-subtle);
      padding: 12px 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
      flex-shrink: 0;
    }}
    .pb-filter-group {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .pb-btn {{
      padding: 6px 14px;
      border-radius: 8px;
      font-size: 13.5px;
      font-weight: 600;
      cursor: pointer;
      border: 1px solid var(--border-subtle);
      background: rgba(255, 255, 255, 0.04);
      color: var(--text-secondary);
      transition: all 0.2s ease;
      font-family: var(--font-sans);
    }}
    .pb-btn:hover {{
      background: rgba(255, 255, 255, 0.09);
      color: var(--text-primary);
    }}
    .pb-btn.active {{
      background: rgba(56, 189, 248, 0.16);
      color: #38bdf8;
      border-color: #38bdf8;
    }}
    .pb-btn.active.live-filter {{
      background: rgba(52, 211, 153, 0.18);
      color: #34d399;
      border-color: #34d399;
    }}
    .pb-search-box {{
      position: relative;
      min-width: 260px;
    }}
    .pb-search-input {{
      width: 100%;
      padding: 8px 14px 8px 36px;
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
      font-size: 14px;
      outline: none;
      font-family: var(--font-sans);
    }}
    .pb-search-input:focus {{
      border-color: var(--google-blue);
      background: rgba(255, 255, 255, 0.08);
    }}
    .pb-search-icon {{
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 14px;
      pointer-events: none;
    }}

    .pb-workspace {{
      display: flex;
      flex: 1;
      height: calc(100vh - 120px);
      overflow: hidden;
    }}

    .pb-sidebar {{
      width: 400px;
      flex-shrink: 0;
      background: var(--bg-surface);
      border-right: 1px solid var(--border-subtle);
      overflow-y: auto;
      display: flex;
      flex-direction: column;
    }}
    .pb-agent-item {{
      padding: 16px 20px;
      border-bottom: 1px solid var(--border-subtle);
      cursor: pointer;
      transition: all 0.18s ease;
      display: flex;
      flex-direction: column;
      gap: 6px;
      border-left: 4px solid transparent;
    }}
    .pb-agent-item:hover {{
      background: var(--bg-card);
    }}
    .pb-agent-item.selected {{
      background: var(--bg-card-active);
      border-left-color: var(--card-accent, var(--google-blue));
    }}
    .pb-item-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }}
    .pb-item-title {{
      font-size: 16px;
      font-weight: 700;
      color: var(--text-primary);
      line-height: 1.3;
    }}
    .pb-item-meta {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 12.5px;
      color: var(--text-muted);
      flex-wrap: wrap;
    }}
    .pb-status-badge {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 8px;
      border-radius: 12px;
      font-size: 11px;
      font-weight: 700;
      font-family: var(--font-mono);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .pb-status-badge.live {{
      background: rgba(52, 211, 153, 0.14);
      color: #34d399;
      border: 1px solid rgba(52, 211, 153, 0.35);
    }}
    .pb-status-badge.catalog {{
      background: rgba(255, 255, 255, 0.05);
      color: var(--text-muted);
      border: 1px solid var(--border-subtle);
    }}
    .pb-status-dot {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #34d399;
      box-shadow: 0 0 8px #34d399;
      display: inline-block;
    }}

    .pb-detail-stage {{
      flex: 1;
      overflow-y: auto;
      padding: 36px 48px;
      background: var(--bg-page);
    }}
    .pb-agent-hero {{
      margin-bottom: 28px;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--border-subtle);
    }}
    .pb-hero-top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
      margin-bottom: 12px;
    }}
    .pb-hero-title {{
      font-family: var(--font-display);
      font-size: 30px;
      font-weight: 700;
      color: #ffffff;
      line-height: 1.25;
    }}
    .pb-hero-persona {{
      font-size: 17px;
      color: var(--text-secondary);
      margin-top: 6px;
    }}

    .pb-section-title {{
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--google-blue);
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .pb-content-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 24px;
      margin-bottom: 24px;
    }}

    .pb-usecase-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
    }}
    .pb-usecase-box {{
      padding: 16px;
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--border-subtle);
    }}
    .pb-usecase-box h4 {{
      font-size: 13px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 8px;
      font-family: var(--font-mono);
    }}
    .pb-usecase-box p {{
      font-size: 15px;
      color: var(--text-primary);
      line-height: 1.55;
    }}

    .pb-systems-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 12px;
    }}
    .pb-system-pill {{
      padding: 14px;
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}
    .pb-system-name {{
      font-size: 14.5px;
      font-weight: 700;
      color: #38bdf8;
    }}
    .pb-system-desc {{
      font-size: 13.5px;
      color: var(--text-secondary);
      line-height: 1.45;
    }}

    .pb-prompt-card {{
      background: #0d1424;
      border: 1px solid rgba(56, 189, 248, 0.2);
      border-radius: 12px;
      padding: 18px 20px;
      margin-bottom: 16px;
    }}
    .pb-prompt-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 10px;
    }}
    .pb-prompt-tag {{
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      color: var(--google-amber);
      font-family: var(--font-mono);
      letter-spacing: 0.06em;
    }}
    .pb-copy-btn {{
      padding: 5px 12px;
      border-radius: 6px;
      background: rgba(56, 189, 248, 0.12);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.3);
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
      font-family: var(--font-sans);
    }}
    .pb-copy-btn:hover {{
      background: rgba(56, 189, 248, 0.25);
    }}
    .pb-copy-btn.copied {{
      background: rgba(52, 211, 153, 0.25);
      color: #34d399;
      border-color: #34d399;
    }}
    .pb-prompt-text {{
      font-size: 15.5px;
      color: #f1f5f9;
      line-height: 1.6;
      background: rgba(0, 0, 0, 0.25);
      padding: 14px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.04);
      user-select: text;
    }}

    .pb-action-bar {{
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
      margin-top: 24px;
      padding-top: 20px;
      border-top: 1px solid var(--border-subtle);
    }}
    .pb-primary-btn {{
      padding: 10px 20px;
      border-radius: 8px;
      background: #2563eb;
      color: #ffffff;
      font-size: 14px;
      font-weight: 700;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      border: none;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .pb-primary-btn:hover {{
      background: #1d4ed8;
      transform: translateY(-1px);
    }}
    .pb-secondary-btn {{
      padding: 10px 18px;
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.06);
      color: var(--text-primary);
      font-size: 14px;
      font-weight: 600;
      text-decoration: none;
      border: 1px solid var(--border-subtle);
      display: inline-flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
    }}
    .pb-secondary-btn:hover {{
      background: rgba(255, 255, 255, 0.1);
    }}
  </style>
</head>
<body>

  <!-- Masthead -->
  <header class="pb-masthead">
    <div class="pb-brand-title">
      <span>🎬</span>
      <span>Supply Chain AI Agents Playbook</span>
    </div>
    <div class="pb-stats-strip">
      <span class="pb-stat-chip live"><span class="pb-status-dot"></span> <strong>{deployed_count}</strong> Live in Gemini Enterprise</span>
      <span class="pb-stat-chip"><strong>{total_count}</strong> Total Agents</span>
      <span class="pb-stat-chip"><strong>6</strong> ASCM SCOR Pillars</span>
      <a href="index.html" class="pb-stat-chip" style="text-decoration:none; color:#38bdf8;">🌐 Open Web Portal &rarr;</a>
    </div>
  </header>

  <!-- Filter Toolbar -->
  <div class="pb-toolbar">
    <div class="pb-filter-group">
      <span style="font-size:12px; font-weight:700; color:var(--text-muted); text-transform:uppercase; margin-right:4px;">Status:</span>
      <button class="pb-btn active" onclick="setStatusFilter('all', this)">All ({total_count})</button>
      <button class="pb-btn live-filter" onclick="setStatusFilter('deployed', this)">🟢 Deployed in GE ({deployed_count})</button>
      <button class="pb-btn" onclick="setStatusFilter('catalog', this)">⚪ In Catalog ({total_count - deployed_count})</button>
    </div>

    <div class="pb-filter-group">
      <span style="font-size:12px; font-weight:700; color:var(--text-muted); text-transform:uppercase; margin-right:4px;">Pillar:</span>
      <button class="pb-btn active" onclick="setPillarFilter('all', this)">All Pillars</button>
      <button class="pb-btn" onclick="setPillarFilter('demand_sop', this)">01 Plan</button>
      <button class="pb-btn" onclick="setPillarFilter('sourcing_procurement', this)">02 Source</button>
      <button class="pb-btn" onclick="setPillarFilter('manufacturing_prod', this)">03 Make</button>
      <button class="pb-btn" onclick="setPillarFilter('inventory_warehouse', this)">04 Deliver (DC)</button>
      <button class="pb-btn" onclick="setPillarFilter('logistics_fleet', this)">05 Logistics</button>
      <button class="pb-btn" onclick="setPillarFilter('circular_enable', this)">06 Return</button>
    </div>

    <div class="pb-search-box">
      <span class="pb-search-icon">🔍</span>
      <input type="text" class="pb-search-input" id="searchBox" placeholder="Filter by agent, persona, or keyword..." oninput="handleSearch(this.value)">
    </div>
  </div>

  <!-- Master-Detail Workspace -->
  <div class="pb-workspace">
    <!-- Left Roster -->
    <aside class="pb-sidebar" id="agentRoster">
      <!-- Items generated via JS -->
    </aside>

    <!-- Right Reader Stage -->
    <main class="pb-detail-stage" id="agentStage">
      <!-- Selected agent details injected via JS -->
    </main>
  </div>

  <script>
    const AGENTS = {agents_json};
    let currentStatusFilter = 'all';
    let currentPillarFilter = 'all';
    let currentSearchQuery = '';
    let currentSelectedId = AGENTS[0] ? AGENTS[0].id : null;

    function renderRoster() {{
      const roster = document.getElementById('agentRoster');
      roster.innerHTML = '';

      const filtered = AGENTS.filter(ag => {{
        if (currentStatusFilter === 'deployed' && !ag.is_deployed) return false;
        if (currentStatusFilter === 'catalog' && ag.is_deployed) return false;
        if (currentPillarFilter !== 'all' && ag.dept_id !== currentPillarFilter) return false;
        if (currentSearchQuery) {{
          const q = currentSearchQuery.toLowerCase();
          const match = ag.name.toLowerCase().includes(q) ||
                        ag.id.toLowerCase().includes(q) ||
                        ag.persona.toLowerCase().includes(q) ||
                        ag.sub_pillar.toLowerCase().includes(q);
          if (!match) return false;
        }}
        return true;
      }});

      if (filtered.length === 0) {{
        roster.innerHTML = '<div style="padding:24px; text-align:center; color:var(--text-muted); font-size:14px;">No agents match the selected filters.</div>';
        return;
      }}

      if (!filtered.some(a => a.id === currentSelectedId)) {{
        currentSelectedId = filtered[0].id;
      }}

      filtered.forEach(ag => {{
        const item = document.createElement('div');
        item.className = 'pb-agent-item' + (ag.id === currentSelectedId ? ' selected' : '');
        item.style.setProperty('--card-accent', ag.pillar_color);
        item.onclick = () => selectAgent(ag.id);

        const statusTag = ag.is_deployed 
          ? '<span class="pb-status-badge live"><span class="pb-status-dot"></span> Live in GE</span>'
          : '<span class="pb-status-badge catalog">Catalog</span>';

        item.innerHTML = `
          <div class="pb-item-header">
            <span class="pb-item-title">#${{String(ag.idx).padStart(2, '0')}} · ${{ag.name}}</span>
            ${{statusTag}}
          </div>
          <div class="pb-item-meta">
            <span style="color:${{ag.pillar_color}}; font-weight:700;">${{ag.sub_pillar}}</span>
            <span>&bull;</span>
            <span>👤 ${{ag.persona}}</span>
          </div>
        `;
        roster.appendChild(item);
      }});

      renderDetail();
    }}

    function selectAgent(agId) {{
      currentSelectedId = agId;
      document.querySelectorAll('.pb-agent-item').forEach(el => el.classList.remove('selected'));
      renderRoster();
    }}

    function renderDetail() {{
      const stage = document.getElementById('agentStage');
      const ag = AGENTS.find(a => a.id === currentSelectedId);
      if (!ag) {{
        stage.innerHTML = '<div style="padding:40px; color:var(--text-muted);">Select an agent from the roster on the left.</div>';
        return;
      }}

      const statusBanner = ag.is_deployed 
        ? `<span class="pb-status-badge live" style="font-size:13px; padding:6px 14px;"><span class="pb-status-dot"></span> Live in Gemini Enterprise (Reasoning Engine Ready)</span>`
        : `<span class="pb-status-badge catalog" style="font-size:13px; padding:6px 14px;">⚪ Planned / In Catalog</span>`;

      const connectorsHtml = ag.connectors.map(c => `
        <div class="pb-system-pill">
          <span class="pb-system-name">${{c[0]}}</span>
          <span class="pb-system-desc">${{c[1]}}</span>
        </div>
      `).join('');

      const promptsHtml = ag.prompts.map((p, i) => `
        <div class="pb-prompt-card">
          <div class="pb-prompt-header">
            <span class="pb-prompt-tag">Prompt ${{i+1}} · ${{p.tag}}</span>
            <button class="pb-copy-btn" onclick="copyPrompt('${{escapeJs(p.text)}}', this)">
              📋 Copy Prompt
            </button>
          </div>
          <div class="pb-prompt-text">${{escapeHtml(p.text)}}</div>
        </div>
      `).join('');

      stage.innerHTML = `
        <div class="pb-agent-hero">
          <div class="pb-hero-top">
            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
              <span class="pb-stat-chip" style="color:${{ag.pillar_color}}; border-color:${{ag.pillar_color}}66; font-weight:700;">#${{String(ag.idx).padStart(2, '0')}} · ${{ag.pillar_title}}</span>
              <span class="pb-stat-chip" style="font-weight:600;">${{ag.sub_pillar}}</span>
              ${{statusBanner}}
            </div>
            <span class="pb-stat-chip" style="background:rgba(16,185,129,0.14); color:#10b981; border-color:rgba(16,185,129,0.4); font-weight:700; font-size:14px;">
              🚀 ${{ag.roi_badge}}
            </span>
          </div>
          <h1 class="pb-hero-title">${{ag.name}}</h1>
          <div class="pb-hero-persona">Primary Human Persona: <strong>${{ag.persona}}</strong> &bull; Package ID: <code>${{ag.id}}</code></div>
        </div>

        <!-- 1. Business Use Case -->
        <div class="pb-content-card">
          <div class="pb-section-title">🎯 1 · Real-World Business Problem &amp; AI Solution</div>
          <div class="pb-usecase-grid">
            <div class="pb-usecase-box">
              <h4 style="color:#fb7185;">✕ The Operational Problem</h4>
              <p>${{ag.problem}}</p>
            </div>
            <div class="pb-usecase-box">
              <h4 style="color:#38bdf8;">✦ What the AI Agent Solves</h4>
              <p>${{ag.solution}}</p>
            </div>
            <div class="pb-usecase-box">
              <h4 style="color:#10b981;">🚀 Quantified Enterprise Outcome</h4>
              <p>${{ag.outcome}}</p>
            </div>
          </div>
        </div>

        <!-- 2. Connected Enterprise Systems -->
        <div class="pb-content-card">
          <div class="pb-section-title">🔌 2 · Connected Enterprise Systems &amp; Data Sources</div>
          <div class="pb-systems-grid">
            ${{connectorsHtml}}
          </div>
        </div>

        <!-- 3. 3-Step Execution Flow -->
        <div class="pb-content-card" style="border-left: 4px solid var(--google-blue);">
          <div class="pb-section-title">🔄 3 · How the Agent Works (The 3-Step Execution Flow)</div>
          <div style="font-size:15px; color:var(--text-secondary); line-height:1.65; display:flex; flex-direction:column; gap:8px;">
            <div><strong>1. Sense &amp; Ingest:</strong> Queries live operational transactions from connected ERP/WMS systems without asking the user for technical table names or SQL syntax.</div>
            <div><strong>2. Predict &amp; Optimize:</strong> Evaluates operational constraints, detects anomalies, and executes mathematical solvers to compute the lowest-cost, highest-service mitigation.</div>
            <div><strong>3. Deliver &amp; Action:</strong> Renders visual comparison charts, generates atomic copy-ready CSV tables for Google Sheets, and prepares approved updates for safe ERP write-back.</div>
          </div>
        </div>

        <!-- 4. Prompts -->
        <div class="pb-content-card">
          <div class="pb-section-title">💬 4 · 3 Realistic High-Impact Business Prompts (Ready to Paste)</div>
          <p style="font-size:14px; color:var(--text-muted); margin-bottom:16px;">
            These prompts are written in natural plain English—never mention database tables or code parameters. Click <strong>Copy Prompt</strong> and paste directly into Gemini Enterprise or the local ADK chat:
          </p>
          ${{promptsHtml}}
        </div>

        <!-- 5. Quick Actions -->
        <div class="pb-action-bar">
          <a href="index.html#agent/${{ag.id}}" class="pb-primary-btn" target="_blank">
            <span>🚀 Open Interactive CAD Simulation</span>
          </a>
          <button class="pb-secondary-btn" onclick="copyPrompt('python3 scripts/test_agent_demo.py ${{ag.id}}', this)">
            <span>💻 Copy Terminal Test Command</span>
          </button>
        </div>
      `;
    }}

    function setStatusFilter(status, btn) {{
      currentStatusFilter = status;
      document.querySelectorAll('.pb-filter-group:nth-child(1) .pb-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderRoster();
    }}

    function setPillarFilter(pillar, btn) {{
      currentPillarFilter = pillar;
      document.querySelectorAll('.pb-filter-group:nth-child(2) .pb-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderRoster();
    }}

    function handleSearch(val) {{
      currentSearchQuery = val.trim();
      renderRoster();
    }}

    function copyPrompt(text, btn) {{
      navigator.clipboard.writeText(text).then(() => {{
        const oldText = btn.innerHTML;
        btn.innerHTML = '✅ Copied!';
        btn.classList.add('copied');
        setTimeout(() => {{
          btn.innerHTML = oldText;
          btn.classList.remove('copied');
        }}, 2000);
      }});
    }}

    function escapeHtml(str) {{
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }}

    function escapeJs(str) {{
      return String(str)
        .replace(/\\/g, '\\\\')
        .replace(/'/g, "\\'")
        .replace(/"/g, '\\"')
        .replace(/\n/g, '\\n')
        .replace(/\r/g, '');
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      renderRoster();
    }});
  </script>
</body>
</html>"""

if __name__ == "__main__":
    generate_playbook()

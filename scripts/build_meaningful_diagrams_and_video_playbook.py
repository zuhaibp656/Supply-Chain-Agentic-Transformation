#!/usr/bin/env python3
"""Builds:
1. Simpler, meaningful 4-Stage Agent Flow SVG Diagrams across all 8 topologies (keeping the signature domain graphics while replacing tiny code/table clutter with clear, larger plain-English labels).
2. Clear 'What This Agent Does' few-liner explanation box on every Agent & Blueprint page + 1-line previews on the front of the 3 Flippable Cards + direct link to the Agent's Playbook entry.
3. Comprehensive Agent Testing, Demo Data & Video Recording Playbook:
   - AGENT_TESTING_AND_VIDEO_PLAYBOOK.md (and docs/AGENT_TESTING_AND_VIDEO_PLAYBOOK.md)
   - Interactive agent_testing_and_video_playbook.html (linked in top navbar across all pages)
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "data" / "supply_chain_catalog.json"
HTML_FILES = [
    ROOT / "index.html",
    ROOT / "periodic_table.html",
    ROOT / "mind_map.html",
]

PILLAR_ORDER = [
    ("demand_sop", "01 · Planning & Strategy", "#3b82f6"),
    ("sourcing_procurement", "02 · Sourcing & Procurement", "#f59e0b"),
    ("manufacturing_prod", "03 · Manufacturing & Operations", "#8b5cf6"),
    ("logistics_fleet", "04 · Logistics & Distribution", "#06b6d4"),
    ("inventory_warehouse", "05 · Inventory & Warehousing", "#10b981"),
    ("circular_enable", "06 · Control Tower & Governance", "#f43f5e"),
]


def clean_agent_name(raw_name: str) -> str:
    s = str(raw_name or "").strip()
    s = re.sub(r"^\[[^\]]+\]\s*", "", s)
    return s


def to_open_tech_label(raw: str) -> str:
    s = str(raw or "")
    replacements = [
        (r"AlloyDB\s*AI\s*\(\s*pgvector\s*\)", "Vector Search & Semantic Index (DB / MCP)"),
        (r"AlloyDB\s*pgvector", "Vector Search & Semantic Index (DB / MCP)"),
        (r"AlloyDB\s*AI", "Vector Search & Transactional DB"),
        (r"AlloyDB", "Transactional & Vector DB (On-Prem / Cloud)"),
        (r"Cloud\s*Spanner\s*Graph", "Multi-Hop Graph Database (Cloud / On-Prem)"),
        (r"Spanner\s*Graph", "Multi-Hop Supply Graph DB"),
        (r"Cloud\s*Spanner", "Low-Latency Transactional State DB"),
        (r"Spanner", "Low-Latency Transactional DB"),
        (r"Google\s*DeepMind\s*WeatherNext\s*3", "Weather & Climate Ensemble Feed (API / MCP)"),
        (r"WeatherNext\s*3", "Weather Ensemble Feed"),
        (r"Google\s*Earth\s*Engine", "Satellite & Geospatial Imagery API"),
        (r"Google\s*Maps\s*Routes\s*Preferred\s*API", "Geospatial Routing & Traffic API"),
        (r"Google\s*Maps\s*Routes\s*API", "Geospatial Routing & Traffic API"),
        (r"Google\s*Maps\s*Fleet\s*Engine", "Fleet & Yard Geofencing API"),
        (r"Google\s*Maps\s*Platform", "Geospatial Routing & ETA API"),
        (r"Vertex\s*AI\s*TimesFM\s*Foundation\s*Model", "Time-Series Forecasting Foundation Model"),
        (r"Vertex\s*AI\s*TimesFM", "Time-Series Forecasting Model"),
        (r"TimesFM", "Time-Series Forecasting Model"),
        (r"Google\s*OR-Tools", "Mathematical Optimization Solver (MILP / CP-SAT)"),
        (r"OR-Tools", "Constraint Optimization Solver (MILP)"),
        (r"SAP\s*IBP\s*&\s*S/4HANA", "Enterprise ERP & Supply Planning (MCP / On-Prem)"),
        (r"SAP\s*IBP", "Supply Planning System (MCP / API)"),
        (r"SAP\s*S/4HANA", "Enterprise ERP (MCP / On-Prem DB)"),
        (r"SAP\s*EWM", "Warehouse Management System (WMS / MCP)"),
        (r"SAP\s*QM", "Quality Management System (QMS / ERP)"),
        (r"SAP\s*PM", "Plant Maintenance System (EAM / ERP)"),
        (r"SAP\s*TM", "Transportation Management System (TMS)"),
        (r"SAP\s*GTS", "Global Trade & Tariff System (MCP / API)"),
        (r"SAP\s*Ariba", "e-Procurement & Sourcing Portal (MCP / API)"),
        (r"Manhattan\s*Active\s*WMS", "Warehouse Management System (WMS / API)"),
        (r"Blue\s*Yonder\s*TMS", "Transportation Management System (TMS / API)"),
        (r"Oracle\s*OTM", "Transportation Management System (TMS / API)"),
        (r"Apigee", "MCP / REST API Gateway"),
    ]
    for pattern, rep in replacements:
        s = re.sub(pattern, rep, s, flags=re.IGNORECASE)
    return s


def get_re_id(agent_id: str) -> str | None:
    p = ROOT / "agents" / agent_id / ".reasoning_engine_id"
    if p.exists():
        return p.read_text(encoding="utf-8").strip()
    return None


def build_playbooks() -> None:
    cat = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    agents_dict = cat.get("agents", {})
    personas_dict = cat.get("personas", {})

    # Group agents by deptId
    by_dept: dict[str, list[dict]] = {pid: [] for pid, _, _ in PILLAR_ORDER}
    for ag in agents_dict.values():
        did = ag.get("deptId", "demand_sop")
        by_dept.setdefault(did, []).append(ag)

    # -------------------------------------------------------------------------
    # 1. BUILD MARKDOWN PLAYBOOK (AGENT_TESTING_AND_VIDEO_PLAYBOOK.md)
    # -------------------------------------------------------------------------
    md_lines = [
        "# 🎬 Supply Chain AI Agents — Complete Testing, Demo Data & Video Recording Playbook",
        "",
        "> **Purpose of This Playbook**: A clear, step-by-step reference for all **60 Built Supply Chain AI Agents** across the 6 SCOR Operating Pillars. For every agent, this document explains:",
        "> 1. **What the Agent Does** (simple 3-line explanation ready for your video voiceover).",
        "> 2. **What Demo Data It Uses** (exact fixture tables, sample SKUs/Orders/Plants, and seeded anomalies).",
        "> 3. **What the Agent Will Do During the Test** (which read tools it calls, how it solves the problem, what safety gate it checks, and what ERP/WMS write-back + visual `VegaChart` it produces).",
        "> 4. **How to Test It Immediately** (1-click copy-paste prompts and terminal commands).",
        "",
        "---",
        "",
        "## 🚀 Quick-Start: 4 Ways to Run & Record Any Agent Tomorrow",
        "",
        "### Method 1: Instant 1-Line CLI Demo Runner (Recommended for Quick Verification & Terminal Demos)",
        "We built a dedicated CLI helper (`scripts/test_agent_demo.py`) that runs any of the 60 agents end-to-end, prints the executed ERP/WMS write-back receipts, shows the A2UI `VegaChart` metadata, and outputs the formatted Markdown report & copy-ready table:",
        "```bash",
        "# 1. Run an agent's full autonomous scenario (Read -> Solve -> Safety Gate -> Write-Back + Markdown Report):",
        "python3 scripts/test_agent_demo.py demand_sensing_agent",
        "",
        "# 2. Inspect the agent's Demo Data tables and sample rows before recording:",
        "python3 scripts/test_agent_demo.py demand_sensing_agent --show-data",
        "",
        "# 3. Test the Pre-Execution Governance / Safety Gate (shows how missing idempotency_key is blocked):",
        "python3 scripts/test_agent_demo.py demand_sensing_agent --test-guardrail",
        "",
        "# 4. List all 60 built agents grouped by SCOR Pillar:",
        "python3 scripts/test_agent_demo.py --list",
        "```",
        "",
        "### Method 2: Interactive Local Google ADK Web UI (Best for Browser Screen Recording)",
        "Launch the Google ADK Web UI locally to chat with any of the 60 agents, watch live tool calls (`query_*` and `action_*`), and record the interactive session:",
        "```bash",
        "adk web agents --port 8080",
        "# Then open http://localhost:8080 in Chrome, select the agent from the top-left dropdown, and paste the Demo Prompt from below!",
        "```",
        "",
        "### Method 3: Automated Pytest Smoke Test Suite (Verifies All 7 Unit & Governance Tests per Agent)",
        "```bash",
        "# Test a single agent:",
        "pytest agents/demand_sensing_agent/tests/test_smoke.py -v",
        "",
        "# Or run all 60 agent smoke test suites (420+ tests):",
        "pytest agents/*/tests/test_smoke.py -v",
        "```",
        "",
        "### Method 4: Gemini Enterprise Web UI (For the 14 Cloud-Deployed Flagship Agents in `zuhaibp-ai`)",
        "- **GCP Project**: `zuhaibp-ai` (`632239123109`, Region: `us-central1`)",
        "- **Gemini Enterprise App Engine**: `gemini-enterprise-zuhaibp_1784012666241`",
        "- **Dynamic Orchestrator Model Routing**: Every agent automatically routes high-speed telemetry/lookup queries to **`Gemini 3.8 Flash` (`gemini-3.8-flash`)** and escalates complex multi-echelon optimization/trade-offs to **`Gemini 3.1 Pro / 4 Argon` (`gemini-3.1-pro` / `gemini-4-argon`, subject to availability)**.",
        "",
        "---",
        "",
        "## 🗄️ Shared Enterprise Demo Data Universe (`XYZ Global Industries Corp. — XYZ-CORP-01`)",
        "",
        "All 60 agents are grounded on deterministic, interconnected enterprise demo data so you never get empty results or hallucinated numbers:",
        "",
        "| Data Asset Layer | Location in Repository / Cloud | Count | Key Shared Entity IDs You Can Mention in Prompts |",
        "|:---|:---|---:|:---|",
        "| **Per-Agent Fixture Tables (`.json`)** | `agents/<agent_id>/fixtures/tables/*.json` | **245 Tables** | `SKU-BEV-ISOTONIC-32OZ`, `SKU-SEMI-9900-X1`, `SKU-CRYO-4410-BIO` |",
        "| **Exported CSV & JSON Tables** | `demo_data/tables/*.csv` & `*.json` | **245 Tables** | `ORD-XYZ-2026-99401`, `SHP-XYZ-90884`, `RMA-2026-7741` |",
        "| **BigQuery Digital Twin Dataset** | `zuhaibp-ai:supply_chain_twin` | **149 Tables** | `FAC-PLANT-US-AUS01`, `DC-DALLAS-CENTRAL`, `VND-T1-TSMC-TW01` |",
        "| **Multi-Tab Excel Workbooks (`.xlsx`)** | `demo_data/xyz_corporation/excel/` | **7 Workbooks (43 Tabs)** | `XYZ_Corp_00_Global_ERP_Master_and_Org_Data.xlsx` – `06_Return_RMA...xlsx` |",
        "| **Corporate PDFs (`.pdf`)** | `demo_data/xyz_corporation/pdfs/` | **7 Multi-Page PDFs** | Master Supplier MSA, Lab COA, Commercial Invoice & BOL, EU CBAM Cert |",
        "| **Computer Vision PNG Feeds (`.png`)** | `demo_data/xyz_corporation/images/` | **8 HD Vision Frames** | Dock Door #14 QR Scan, VisionInspect Seal Defect, ShelfVision Planogram |",
        "| **SOPs, Emails & X12 EDI Streams** | `demo_data/xyz_corporation/docs/` | **6 Docs/EDI Files** | ANSI X12 852 POS, 856 ASN, 204 Motor Carrier Load Tender, 214 Status |",
        "",
        "---",
        "",
    ]

    # HTML Playbook Cards collector
    html_cards: list[str] = []
    total_idx = 0

    for dept_id, pillar_title, pillar_color in PILLAR_ORDER:
        dept_agents = by_dept.get(dept_id, [])
        md_lines.append(f"## {pillar_title} ({len(dept_agents)} Agents)")
        md_lines.append("")

        for ag in dept_agents:
            total_idx += 1
            ag_id = ag["id"]
            c_name = clean_agent_name(ag.get("name", ag_id))
            sub_pillar = ag.get("subPillarName") or pillar_title
            persona_name = ag.get("primaryPersonaName") or personas_dict.get(ag.get("primaryPersonaId", ""), {}).get("name", "Supply Chain Lead")
            re_id = get_re_id(ag_id)
            adk = ag.get("adkImplementation", {})
            spec = ag.get("adkSpec", {})
            eval_obj = spec.get("evalScenario", {})
            tables = adk.get("fixtureTables", [])
            tools_meta = spec.get("toolsMeta", [])
            read_tools = [t["name"] for t in tools_meta if t.get("kind") != "action"] or [t for t in adk.get("tools", []) if not t.startswith("action_") and t != "list_systems"]
            write_tools = [t["name"] for t in tools_meta if t.get("kind") == "action"] or [t for t in adk.get("tools", []) if t.startswith("action_")]

            demo_prompt = eval_obj.get("query") or f"Analyze live {sub_pillar} signals for {c_name}, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'."
            guardrail_prompt = f"Call {write_tools[0] if write_tools else 'the write-back tool'} immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate."
            solver_open = to_open_tech_label(ag.get("solverStack") or "AI & Mathematical Optimization Solver")
            writeback_open = to_open_tech_label(ag.get("apiWriteback") or "Enterprise ERP / WMS Write-Back via MCP")
            anomalies = spec.get("anomalies", [])

            # Build Markdown section for this agent
            cloud_badge_md = f" · 🟢 **Live Vertex AI RE**: `{re_id.split('/')[-1]}`" if re_id else ""
            md_lines.extend([
                f"### {total_idx}. {c_name} (`{ag_id}`)",
                f"- **Pillar / Sub-Pillar**: {pillar_title} — **{sub_pillar}**",
                f"- **Primary Human Persona**: {persona_name} · **ROI Badge**: `{ag.get('badge', 'Verified ROI')}`{cloud_badge_md}",
                "",
                "#### 🎯 What This Agent Does (Simple Voiceover Summary)",
                f"1. **The Problem It Solves**: {ag.get('problem', '')}",
                f"2. **What the Agent Does**: {ag.get('solution', '')}",
                f"3. **Expected Outcome**: {ag.get('outcome', '')} (**{ag.get('badge', '')}**).",
                "",
                "#### 🗄️ Demo Data Details (`agents/" + ag_id + "/fixtures/tables/`)",
            ])

            sample_kv_Chips = []
            for t in tables:
                tname = t.get("table_name", "")
                cols = t.get("columns", [])
                rows = t.get("rows", [])
                sample_pairs = []
                if rows and isinstance(rows[0], dict):
                    for k, v in list(rows[0].items())[:4]:
                        sample_pairs.append(f"`{k}={v}`")
                        if len(sample_kv_Chips) < 4 and isinstance(v, (str, int, float)) and len(str(v)) < 28:
                            sample_kv_Chips.append(f"{k}: {v}")
                sample_str = ", ".join(sample_pairs) if sample_pairs else "Deterministic fixture records"
                md_lines.append(f"- **`{tname}.json`** ({t.get('row_count', len(rows))} rows) — Columns: `{', '.join(cols[:6])}` · Sample Record: {sample_str}")

            if anomalies:
                md_lines.append(f"- **Seeded Anomalies in Demo Data**: {' | '.join(anomalies[:2])}")

            md_lines.extend([
                "",
                "#### ⚙️ What Happens When You Test It (Step-by-Step Flow)",
                f"1. **Reads Live Demo Tables**: Calls `{', '.join(read_tools[:3])}` across the {len(tables)} fixture tables above.",
                f"2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **{solver_open}**.",
                f"3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.",
                f"4. **Executes Write-Back & Visual**: Calls `{', '.join(write_tools) or 'action_commit'}` ({writeback_open}) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.",
                "",
                "#### 🧪 How to Test It (Copy-Paste Prompts & Commands)",
                "- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:",
                f"  > `{demo_prompt}`",
                "- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:",
                f"  > `{guardrail_prompt}`",
                "- **Terminal Commands**:",
                "```bash",
                f"# Run full scenario & print Markdown report + write-back receipts:",
                f"python3 scripts/test_agent_demo.py {ag_id}",
                f"",
                f"# Inspect demo data tables & sample rows:",
                f"python3 scripts/test_agent_demo.py {ag_id} --show-data",
                f"",
                f"# Test pre-execution safety gate:",
                f"python3 scripts/test_agent_demo.py {ag_id} --test-guardrail",
                f"",
                f"# Run unit smoke tests:",
                f"pytest agents/{ag_id}/tests/test_smoke.py -v",
                "```",
                "",
                "---",
                "",
            ])

            # Build HTML Card for agent_testing_and_video_playbook.html
            tables_html = []
            for t in tables:
                tname = html.escape(str(t.get("table_name", "")))
                cols = t.get("columns", [])
                rows = t.get("rows", [])
                first_row_json = html.escape(json.dumps(rows[0], indent=2, ensure_ascii=False)) if rows else "{}"
                tables_html.append(f"""
                  <div class="pb-table-item">
                    <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; flex-wrap:wrap;">
                      <code class="pb-code-pill">🗄️ {tname}.json</code>
                      <span style="font-size:12px; color:var(--text-secondary); font-family:var(--font-mono);">{len(rows)} rows · {len(cols)} cols</span>
                    </div>
                    <div style="font-size:12.5px; color:var(--text-secondary); margin-top:6px;">
                      <strong>Fields:</strong> {html.escape(', '.join(cols[:7]))}
                    </div>
                    <details style="margin-top:8px;">
                      <summary style="cursor:pointer; font-size:12px; font-weight:700; color:#38bdf8;">▾ View Sample Demo Row</summary>
                      <pre class="pb-json-pre">{first_row_json}</pre>
                    </details>
                  </div>
                """)

            cmd_run = f"python3 scripts/test_agent_demo.py {ag_id}"
            cmd_data = f"python3 scripts/test_agent_demo.py {ag_id} --show-data"
            cmd_gate = f"python3 scripts/test_agent_demo.py {ag_id} --test-guardrail"
            cmd_pytest = f"pytest agents/{ag_id}/tests/test_smoke.py -v"

            cloud_pill_html = (
                f'<span class="pb-badge" style="background:rgba(16,185,129,0.16); color:#10b981; border-color:rgba(16,185,129,0.4);">🟢 Cloud Deployed (RE {re_id.split("/")[-1][:8]}…)</span>'
                if re_id else
                '<span class="pb-badge">📦 Local ADK Package Ready</span>'
            )

            html_cards.append(f"""
              <article class="pb-agent-card" id="agent-{ag_id}" data-pillar="{dept_id}" data-cloud="{'true' if re_id else 'false'}" data-search="{html.escape((c_name + ' ' + ag_id + ' ' + sub_pillar + ' ' + persona_name + ' ' + ag.get('solution', '')).lower())}" style="--pillar-color:{pillar_color};">
                <div class="pb-card-header">
                  <div>
                    <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:6px;">
                      <span class="pb-badge" style="color:{pillar_color}; border-color:{pillar_color}55;">#{total_idx:02d} · {html.escape(pillar_title)}</span>
                      <span class="pb-badge">{html.escape(sub_pillar)}</span>
                      <span class="pb-badge">👤 {html.escape(persona_name)}</span>
                      {cloud_pill_html}
                    </div>
                    <h2 class="pb-agent-title">{html.escape(c_name)} <code style="font-size:14px; color:var(--text-secondary); font-weight:600;">({ag_id})</code></h2>
                  </div>
                  <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                    <span class="pb-roi-pill">🚀 {html.escape(ag.get('badge', 'Verified ROI'))}</span>
                    <a href="index.html#agent/{ag_id}" class="pb-link-btn">Open Agent Page ↗</a>
                  </div>
                </div>

                <!-- 1. What This Agent Does (Simple 3-Line Explanation for Video Voiceover) -->
                <div class="pb-what-box">
                  <div class="pb-section-kicker">🎯 1 · WHAT THIS AGENT DOES (VOICEOVER SUMMARY)</div>
                  <div class="pb-what-grid">
                    <div class="pb-what-item">
                      <span class="pb-what-label" style="color:#fb7185;">✕ Problem It Solves</span>
                      <p>{html.escape(ag.get('problem', ''))}</p>
                    </div>
                    <div class="pb-what-item">
                      <span class="pb-what-label" style="color:#38bdf8;">✦ How the Agent Works</span>
                      <p>{html.escape(ag.get('solution', ''))}</p>
                    </div>
                    <div class="pb-what-item">
                      <span class="pb-what-label" style="color:#10b981;">🚀 Expected Outcome</span>
                      <p>{html.escape(ag.get('outcome', ''))}</p>
                    </div>
                  </div>
                </div>

                <!-- 2. What Happens During the Demo & Demo Data Tables -->
                <div class="pb-two-col">
                  <div class="pb-panel">
                    <div class="pb-section-kicker">🗄️ 2 · DEMO DATA TABLES & SAMPLE RECORDS ({len(tables)} TABLES)</div>
                    <div style="display:flex; flex-direction:column; gap:10px;">
                      {''.join(tables_html)}
                    </div>
                    {f'<div style="margin-top:10px; padding:10px 12px; border-radius:10px; background:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.3); font-size:13px; color:var(--text-primary);"><strong>⚠️ Seeded Anomaly to Highlight:</strong> {html.escape(anomalies[0])}</div>' if anomalies else ''}
                  </div>

                  <div class="pb-panel">
                    <div class="pb-section-kicker">⚙️ 3 · WHAT THE AGENT WILL DO & HOW TO TEST IT</div>
                    <ol class="pb-steps-list">
                      <li><strong>Reads Demo Data:</strong> Calls <code>{html.escape(', '.join(read_tools[:3]))}</code> to pull live records & detect anomalies.</li>
                      <li><strong>Runs AI & Math Solver:</strong> Uses <strong>{html.escape(solver_open)}</strong> (<code>Gemini 3.8 Flash</code> ↔ <code>Gemini 3.1 Pro / 4 Argon</code>).</li>
                      <li><strong>Enforces Safety Gate:</strong> Verifies contract parameters & <code>idempotency_key</code> via <code>enforce_tool_contract()</code>.</li>
                      <li><strong>Writes Back & Renders Visual:</strong> Calls <code>{html.escape(', '.join(write_tools) or 'action_commit')}</code> and outputs an interactive <strong>VegaChart</strong> + <strong>Copy-Ready Table</strong>.</li>
                    </ol>

                    <div class="pb-prompt-box">
                      <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; margin-bottom:6px;">
                        <span style="font-size:11.5px; font-weight:800; text-transform:uppercase; color:#38bdf8; font-family:var(--font-mono);">💬 Primary Video Demo Prompt</span>
                        <button type="button" class="pb-copy-btn" data-copy="{html.escape(demo_prompt)}" onclick="copyPlaybookText(this)">📋 Copy Prompt</button>
                      </div>
                      <div style="font-size:14.5px; color:var(--text-primary); line-height:1.55; font-weight:600;">“{html.escape(demo_prompt)}”</div>
                    </div>

                    <div class="pb-cmd-grid">
                      <button type="button" class="pb-copy-btn" data-copy="{html.escape(cmd_run)}" onclick="copyPlaybookText(this)">💻 Copy CLI Run: <code>{ag_id}</code></button>
                      <button type="button" class="pb-copy-btn" data-copy="{html.escape(cmd_data)}" onclick="copyPlaybookText(this)">🗄️ Copy Show-Data Command</button>
                      <button type="button" class="pb-copy-btn" data-copy="{html.escape(cmd_gate)}" onclick="copyPlaybookText(this)">🛡️ Copy Safety-Gate Test</button>
                      <button type="button" class="pb-copy-btn" data-copy="{html.escape(cmd_pytest)}" onclick="copyPlaybookText(this)">🧪 Copy Pytest Command</button>
                    </div>
                  </div>
                </div>
              </article>
            """)

    md_content = "\n".join(md_lines)
    (ROOT / "AGENT_TESTING_AND_VIDEO_PLAYBOOK.md").write_text(md_content, encoding="utf-8")
    (ROOT / "docs" / "AGENT_TESTING_AND_VIDEO_PLAYBOOK.md").write_text(md_content, encoding="utf-8")
    print("Wrote AGENT_TESTING_AND_VIDEO_PLAYBOOK.md")

    # -------------------------------------------------------------------------
    # 2. BUILD INTERACTIVE HTML PLAYBOOK (agent_testing_and_video_playbook.html)
    # -------------------------------------------------------------------------
    playbook_html = f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Agent Testing, Demo Data &amp; Video Playbook — 60 Supply Chain AI Agents</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Google+Sans+Display:wght@500;700;800&family=Google+Sans+Text:wght@400;500;700&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-canvas: #070b14;
      --bg-card: #0f172a;
      --bg-elevated: #162033;
      --text-primary: #f8fafc;
      --text-secondary: #cbd5e1;
      --border-subtle: rgba(148, 163, 184, 0.18);
      --font-display: 'Google Sans Display', 'Inter', sans-serif;
      --font-sans: 'Google Sans Text', 'Inter', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}
    html[data-theme="light"] {{
      --bg-canvas: #f1f5f9;
      --bg-card: #ffffff;
      --bg-elevated: #f8fafc;
      --text-primary: #0f172a;
      --text-secondary: #334155;
      --border-subtle: rgba(15, 23, 42, 0.12);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: var(--font-sans);
      background: var(--bg-canvas);
      color: var(--text-primary);
      line-height: 1.6;
    }}
    .pb-navbar {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(15, 23, 42, 0.9);
      backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border-subtle);
      padding: 14px 4vw;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }}
    html[data-theme="light"] .pb-navbar {{
      background: rgba(255, 255, 255, 0.92);
    }}
    .pb-container {{
      max-width: 1540px;
      width: 92vw;
      margin: 0 auto;
      padding: 32px 0 80px;
    }}
    .pb-hero {{
      background: var(--bg-card);
      border: 1.5px solid var(--border-subtle);
      border-top: 4px solid #38bdf8;
      border-radius: 20px;
      padding: 28px 32px;
      margin-bottom: 24px;
    }}
    .pb-quick-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 16px;
      margin-top: 20px;
    }}
    .pb-quick-card {{
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 16px 20px;
    }}
    .pb-filter-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 24px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      padding: 14px 18px;
      border-radius: 16px;
    }}
    .pb-filter-btn {{
      font-family: var(--font-sans);
      font-size: 13.5px;
      font-weight: 700;
      padding: 8px 15px;
      border-radius: 999px;
      border: 1px solid var(--border-subtle);
      background: var(--bg-elevated);
      color: var(--text-primary);
      cursor: pointer;
      transition: all 0.18s ease;
    }}
    .pb-filter-btn.active, .pb-filter-btn:hover {{
      background: #2563eb;
      color: #ffffff;
      border-color: #38bdf8;
    }}
    .pb-search-input {{
      font-family: var(--font-sans);
      font-size: 14.5px;
      padding: 9px 16px;
      border-radius: 999px;
      border: 1.5px solid var(--border-subtle);
      background: var(--bg-elevated);
      color: var(--text-primary);
      min-width: 280px;
    }}
    .pb-agent-card {{
      background: var(--bg-card);
      border: 1.5px solid var(--border-subtle);
      border-top: 4px solid var(--pillar-color, #38bdf8);
      border-radius: 20px;
      padding: 26px 30px;
      margin-bottom: 24px;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.18);
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
      font-size: 24px;
      font-weight: 800;
      margin: 0;
    }}
    .pb-badge {{
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 700;
      padding: 4px 11px;
      border-radius: 999px;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
    }}
    .pb-roi-pill {{
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 800;
      padding: 7px 14px;
      border-radius: 999px;
      background: rgba(16, 185, 129, 0.14);
      color: #10b981;
      border: 1px solid rgba(16, 185, 129, 0.35);
    }}
    .pb-link-btn {{
      text-decoration: none;
      font-size: 13.5px;
      font-weight: 700;
      padding: 8px 16px;
      border-radius: 12px;
      background: #2563eb;
      color: #ffffff;
      transition: transform 0.15s ease;
    }}
    .pb-link-btn:hover {{
      transform: translateY(-2px);
    }}
    .pb-what-box {{
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 18px 22px;
      margin-bottom: 18px;
    }}
    .pb-section-kicker {{
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      color: #38bdf8;
      margin-bottom: 12px;
    }}
    .pb-what-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
    }}
    .pb-what-item {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 14px 16px;
    }}
    .pb-what-label {{
      display: block;
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 800;
      text-transform: uppercase;
      margin-bottom: 6px;
    }}
    .pb-what-item p {{
      margin: 0;
      font-size: 15px;
      line-height: 1.6;
      color: var(--text-primary);
    }}
    .pb-two-col {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
      gap: 18px;
    }}
    .pb-panel {{
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 18px 22px;
    }}
    .pb-table-item {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 12px 14px;
    }}
    .pb-code-pill {{
      font-family: var(--font-mono);
      font-size: 12.5px;
      font-weight: 700;
      color: #38bdf8;
    }}
    .pb-json-pre {{
      margin: 8px 0 0;
      padding: 10px 12px;
      border-radius: 8px;
      background: rgba(15, 23, 42, 0.75);
      color: #e2e8f0;
      font-family: var(--font-mono);
      font-size: 11.5px;
      overflow-x: auto;
    }}
    .pb-steps-list {{
      margin: 0 0 16px;
      padding-left: 20px;
      font-size: 14.5px;
      line-height: 1.65;
    }}
    .pb-steps-list li {{
      margin-bottom: 6px;
    }}
    .pb-prompt-box {{
      background: var(--bg-card);
      border: 1.5px solid rgba(56, 189, 248, 0.35);
      border-radius: 14px;
      padding: 14px 16px;
      margin-bottom: 14px;
    }}
    .pb-cmd-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 10px;
    }}
    .pb-copy-btn {{
      font-family: var(--font-sans);
      font-size: 13px;
      font-weight: 700;
      padding: 9px 14px;
      border-radius: 10px;
      border: 1px solid var(--border-subtle);
      background: var(--bg-card);
      color: var(--text-primary);
      cursor: pointer;
      text-align: left;
      transition: all 0.15s ease;
    }}
    .pb-copy-btn:hover {{
      border-color: #38bdf8;
      background: rgba(56, 189, 248, 0.12);
    }}
  </style>
</head>
<body>
  <header class="pb-navbar">
    <div style="display:flex; align-items:center; gap:14px;">
      <a href="index.html" style="text-decoration:none; color:var(--text-primary); font-family:var(--font-display); font-size:20px; font-weight:800;">
        &larr; Back to Supply Chain Portal
      </a>
      <span class="pb-badge" style="color:#38bdf8; border-color:rgba(56,189,248,0.4);">🎬 60-Agent Video &amp; Testing Playbook</span>
    </div>
    <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
      <a href="periodic_table.html" class="pb-filter-btn" style="text-decoration:none;">Periodic Table</a>
      <a href="mind_map.html" class="pb-filter-btn" style="text-decoration:none;">Neural Mind Map</a>
      <a href="cost_analysis_presentation.html" class="pb-filter-btn" style="text-decoration:none;">FinOps Deck</a>
      <button type="button" class="pb-filter-btn" onclick="document.documentElement.setAttribute('data-theme', document.documentElement.getAttribute('data-theme')==='light'?'dark':'light')">
        🌗 Theme
      </button>
    </div>
  </header>

  <main class="pb-container">
    <section class="pb-hero">
      <div style="font-family:var(--font-mono); font-size:12px; font-weight:800; color:#38bdf8; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">
        COMPLETE DEMO DATA, VOICEOVER SCRIPT &amp; TEST COMMAND PLAYBOOK
      </div>
      <h1 style="font-family:var(--font-display); font-size:clamp(26px, 3vw, 38px); margin:0 0 10px;">
        How to Test &amp; Record All 60 Supply Chain AI Agents
      </h1>
      <p style="font-size:16px; color:var(--text-secondary); margin:0; max-width:1100px;">
        Every card below gives you: <strong>(1) A simple 3-line explanation</strong> of what the agent does for your video voiceover, <strong>(2) Exact Demo Data tables &amp; sample rows</strong>, <strong>(3) What the agent will execute</strong>, and <strong>(4) 1-Click Copy buttons</strong> for the Demo Prompt and CLI commands.
      </p>

      <div class="pb-quick-grid">
        <div class="pb-quick-card">
          <div style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; color:#10b981; margin-bottom:6px;">OPTION A · 1-LINE TERMINAL DEMO RUNNER</div>
          <div style="font-size:13.5px; color:var(--text-secondary); margin-bottom:8px;">Runs the agent on its demo data, executes ERP write-backs, and prints the Markdown table:</div>
          <code style="display:block; padding:8px 10px; border-radius:8px; background:var(--bg-card); font-family:var(--font-mono); font-size:12px; color:#38bdf8;">python3 scripts/test_agent_demo.py &lt;agent_id&gt;</code>
        </div>
        <div class="pb-quick-card">
          <div style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; color:#38bdf8; margin-bottom:6px;">OPTION B · INTERACTIVE ADK WEB UI (FOR VIDEO)</div>
          <div style="font-size:13.5px; color:var(--text-secondary); margin-bottom:8px;">Launches the local browser chat UI for all 60 agents at <code>http://localhost:8080</code>:</div>
          <code style="display:block; padding:8px 10px; border-radius:8px; background:var(--bg-card); font-family:var(--font-mono); font-size:12px; color:#38bdf8;">adk web agents --port 8080</code>
        </div>
        <div class="pb-quick-card">
          <div style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; color:#f59e0b; margin-bottom:6px;">OPTION C · SHARED MULTI-MODAL DEMO DATA</div>
          <div style="font-size:13.5px; color:var(--text-secondary); margin-bottom:8px;">245 JSON/CSV tables + 7 Excel workbooks + 7 PDFs + 8 Vision PNGs in:</div>
          <code style="display:block; padding:8px 10px; border-radius:8px; background:var(--bg-card); font-family:var(--font-mono); font-size:12px; color:#fbbf24;">demo_data/xyz_corporation/ &amp; demo_data/tables/</code>
        </div>
      </div>
    </section>

    <div class="pb-filter-bar">
      <div style="display:flex; gap:8px; flex-wrap:wrap;">
        <button type="button" class="pb-filter-btn active" onclick="filterPlaybook('all', this)">All 60 Agents</button>
        <button type="button" class="pb-filter-btn" onclick="filterPlaybook('demand_sop', this)">01 · Plan (9)</button>
        <button type="button" class="pb-filter-btn" onclick="filterPlaybook('sourcing_procurement', this)">02 · Source (9)</button>
        <button type="button" class="pb-filter-btn" onclick="filterPlaybook('manufacturing_prod', this)">03 · Make (9)</button>
        <button type="button" class="pb-filter-btn" onclick="filterPlaybook('logistics_fleet', this)">04 · Logistics (12)</button>
        <button type="button" class="pb-filter-btn" onclick="filterPlaybook('inventory_warehouse', this)">05 · Inventory (12)</button>
        <button type="button" class="pb-filter-btn" onclick="filterPlaybook('circular_enable', this)">06 · Control Tower (9)</button>
        <button type="button" class="pb-filter-btn" onclick="filterPlaybook('cloud', this)">🟢 Cloud-Deployed</button>
      </div>
      <input type="search" id="pbSearchInput" class="pb-search-input" placeholder="🔍 Search agent name, ID, SKU, or persona…" oninput="filterPlaybookSearch()" />
    </div>

    <div id="pbCardsContainer">
      {''.join(html_cards)}
    </div>
  </main>

  <script>
    let currentPillarFilter = 'all';
    function copyPlaybookText(btn) {{
      const txt = btn.getAttribute('data-copy') || '';
      navigator.clipboard.writeText(txt);
      const orig = btn.innerHTML;
      btn.innerHTML = '✅ Copied!';
      setTimeout(() => {{ btn.innerHTML = orig; }}, 1400);
    }}
    function filterPlaybook(pillar, btn) {{
      currentPillarFilter = pillar;
      document.querySelectorAll('.pb-filter-bar .pb-filter-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      applyPlaybookFilters();
    }}
    function filterPlaybookSearch() {{
      applyPlaybookFilters();
    }}
    function applyPlaybookFilters() {{
      const q = (document.getElementById('pbSearchInput').value || '').toLowerCase().trim();
      document.querySelectorAll('.pb-agent-card').forEach(card => {{
        const p = card.getAttribute('data-pillar');
        const c = card.getAttribute('data-cloud');
        const s = card.getAttribute('data-search') || '';
        const matchPillar = (currentPillarFilter === 'all') ||
                            (currentPillarFilter === 'cloud' && c === 'true') ||
                            (p === currentPillarFilter);
        const matchSearch = !q || s.includes(q);
        card.style.display = (matchPillar && matchSearch) ? 'block' : 'none';
      }});
    }}
  </script>
</body>
</html>
"""
    (ROOT / "agent_testing_and_video_playbook.html").write_text(playbook_html, encoding="utf-8")
    for sub in ["docs", "zipline_dist", "dist/itc_limited"]:
        d = ROOT / sub
        if d.exists():
            (d / "agent_testing_and_video_playbook.html").write_text(playbook_html, encoding="utf-8")
    print("Wrote agent_testing_and_video_playbook.html")


# -----------------------------------------------------------------------------
# 3. SIMPLER, MORE MEANINGFUL 4-STAGE SVG FLOW DIAGRAMS + CLEAR AGENT DETAILS
# -----------------------------------------------------------------------------
NEW_RENDER_FULL_TOPOLOGY_SVG = """    function renderFullTopologySvg(topology, ctx) {
      const {
        ag, dept, cls, cleanName, trunc,
        sys1, sys2, sys3, ic1, ic2, ic3,
        tbl1, tbl2, tbl3, tablesCount,
        q1, q2, a1, subs, solverLabel, writebackLabel
      } = ctx;

      const uid = ag.id;
      const role1 = trunc(subs[0].role || 'Validates & correlates live operational signals', 32);
      const role2 = trunc(subs[1].role || 'Computes optimal plan across constraints', 36);
      const badgeLabel = trunc(ag.badge || 'Verified ROI Impact', 24);
      const personaShort = trunc(ag.primaryPersonaName || 'Supply Chain Lead', 24);

      // Common center visual graphic selector for Stage 3 based on the 8 topologies
      let centerGraphic = '';
      let stage3Kicker = '3 · AI & MATH OPTIMIZER';
      let stage2Kicker = '2 · SIGNAL & DATA CHECK';
      let stage4Kicker = '4 · ACTION & OUTCOME';

      if (topology === 'sensing_fan') {
        stage2Kicker = '2 · CLEAN & IMPUTE DATA';
        stage3Kicker = '3 · DEMAND FORECAST ENGINE';
        centerGraphic = `
          <rect class="svg-viz-well" width="248" height="106" rx="10" stroke="${dept.color}66" stroke-width="1.2" />
          <path d="M 88 58 C 132 42, 182 22, 232 14 L 232 94 C 182 84, 132 72, 88 58 Z" fill="${dept.color}38" />
          <path d="M 16 76 Q 44 64, 66 68 T 88 58" fill="none" stroke="#94a3b8" stroke-width="2.4" />
          <path d="M 88 58 C 132 42, 182 22, 232 14" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4 2" />
          <path d="M 88 58 C 136 52, 184 48, 232 44" fill="none" stroke="${dept.color}" stroke-width="2.8" />
          <path d="M 88 58 C 132 72, 182 84, 232 94" fill="none" stroke="#fbbf24" stroke-width="2" stroke-dasharray="4 2" />
          <circle cx="88" cy="58" r="5" fill="#ffffff" stroke="${dept.color}" stroke-width="2" />
          <text x="16" y="24" class="svg-text-mono" font-size="10" font-weight="700">HISTORY</text>
          <text x="168" y="18" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">P90 HIGH</text>
          <text x="168" y="41" fill="${dept.color}" font-size="9.5" font-weight="800" font-family="var(--font-mono)">P50 PLAN</text>
          <text x="168" y="92" fill="#fbbf24" font-size="9.5" font-weight="800" font-family="var(--font-mono)">P10 LOW</text>
        `;
      } else if (topology === 'elasticity_curve') {
        stage2Kicker = '2 · STRIP BASELINE TREND';
        stage3Kicker = '3 · PRICE & PROMO SIMULATOR';
        centerGraphic = `
          <rect class="svg-viz-well" width="248" height="106" rx="10" stroke="#10b98166" stroke-width="1.2" />
          <rect x="22" y="42" width="24" height="44" rx="4" fill="#38bdf8" />
          <rect x="58" y="18" width="24" height="32" rx="4" fill="#10b981" />
          <rect x="94" y="28" width="24" height="24" rx="4" fill="#f43f5e" />
          <rect x="130" y="22" width="24" height="64" rx="4" fill="#fbbf24" />
          <text x="34" y="99" text-anchor="middle" class="svg-text-mono" font-size="9">BASE</text>
          <text x="70" y="99" text-anchor="middle" fill="#10b981" font-size="9" font-weight="800">+LIFT</text>
          <text x="106" y="99" text-anchor="middle" fill="#fb7185" font-size="9" font-weight="800">-DRAG</text>
          <text x="142" y="99" text-anchor="middle" fill="#fbbf24" font-size="9" font-weight="800">NET $</text>
          <path d="M 168 82 C 184 76, 198 24, 232 18" fill="none" stroke="#38bdf8" stroke-width="2.4" />
          <circle cx="202" cy="34" r="5" fill="#10b981" stroke="#ffffff" stroke-width="1.5" />
          <text x="172" y="20" fill="#10b981" font-size="9.5" font-weight="800" font-family="var(--font-mono)">BEST ROI</text>
        `;
      } else if (topology === 'graph_contract_audit') {
        stage2Kicker = '2 · MAP SUPPLIERS & DOCS';
        stage3Kicker = '3 · AI RISK & CLAUSE AUDITOR';
        centerGraphic = `
          <rect class="svg-viz-well" width="248" height="106" rx="10" stroke="#38bdf866" stroke-width="1.2" />
          <line x1="42" y1="53" x2="112" y2="26" stroke="#38bdf8" stroke-width="2" />
          <line x1="42" y1="53" x2="112" y2="80" stroke="#38bdf8" stroke-width="2" />
          <line x1="112" y1="26" x2="196" y2="34" stroke="#f43f5e" stroke-width="2.2" stroke-dasharray="4 2" />
          <line x1="112" y1="80" x2="196" y2="74" stroke="#10b981" stroke-width="2" />
          <circle cx="42" cy="53" r="14" fill="#0f172a" stroke="#38bdf8" stroke-width="2" />
          <text x="42" y="57" text-anchor="middle" fill="#38bdf8" font-size="9.5" font-weight="800">SKU</text>
          <circle cx="112" cy="26" r="14" fill="#0f172a" stroke="#fbbf24" stroke-width="2" />
          <text x="112" y="30" text-anchor="middle" fill="#fbbf24" font-size="9.5" font-weight="800">T-1</text>
          <circle cx="112" cy="80" r="14" fill="#0f172a" stroke="#10b981" stroke-width="2" />
          <text x="112" y="84" text-anchor="middle" fill="#10b981" font-size="9.5" font-weight="800">DOC</text>
          <circle cx="196" cy="34" r="15" fill="rgba(244,63,94,0.25)" stroke="#f43f5e" stroke-width="2.2" />
          <text x="196" y="38" text-anchor="middle" fill="#fb7185" font-size="9.5" font-weight="800">GAP</text>
          <circle cx="196" cy="74" r="14" fill="#0f172a" stroke="#10b981" stroke-width="2" />
          <text x="196" y="78" text-anchor="middle" fill="#10b981" font-size="9.5" font-weight="800">OK</text>
        `;
      } else if (topology === 'edge_vision_iot') {
        stage2Kicker = '2 · SYNC SENSOR STREAMS';
        stage3Kicker = '3 · VISION & SENSOR AI ENGINE';
        centerGraphic = `
          <rect class="svg-viz-well" width="248" height="106" rx="10" stroke="#f59e0b66" stroke-width="1.2" />
          <path d="M 14 56 L 30 56 L 38 22 L 46 86 L 54 16 L 62 80 L 70 38 L 78 66 L 88 56 L 112 56" fill="none" stroke="#fbbf24" stroke-width="2.2" />
          <text x="16" y="96" class="svg-text-mono" font-size="9" font-weight="700">SENSOR WAVE</text>
          <rect x="126" y="14" width="108" height="78" rx="6" fill="rgba(15,23,42,0.78)" stroke="#38bdf8" stroke-width="1.5" />
          <rect x="148" y="28" width="64" height="40" rx="4" fill="rgba(244,63,94,0.2)" stroke="#f43f5e" stroke-width="1.8" stroke-dasharray="4 2" />
          <circle cx="180" cy="48" r="8" fill="rgba(244,63,94,0.48)" stroke="#f43f5e" stroke-width="1.5" />
          <text x="180" y="84" text-anchor="middle" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">DEFECT CAUGHT</text>
        `;
      } else if (topology === 'spatial_wms_atp') {
        stage2Kicker = '2 · CHECK REAL-TIME STOCK';
        stage3Kicker = '3 · 3D WAREHOUSE & ATP ENGINE';
        centerGraphic = `
          <rect class="svg-viz-well" width="248" height="106" rx="10" stroke="#10b98166" stroke-width="1.2" />
          <rect x="18" y="16" width="28" height="20" rx="3" fill="#334155" stroke="#64748b" />
          <rect x="52" y="16" width="28" height="20" rx="3" fill="#38bdf8" />
          <rect x="86" y="16" width="28" height="20" rx="3" fill="#334155" stroke="#64748b" />
          <rect x="18" y="42" width="28" height="20" rx="3" fill="#10b981" stroke="#ffffff" stroke-width="1.2" />
          <rect x="52" y="42" width="28" height="20" rx="3" fill="#10b981" stroke="#ffffff" stroke-width="1.2" />
          <rect x="86" y="42" width="28" height="20" rx="3" fill="#fbbf24" />
          <rect x="18" y="68" width="28" height="20" rx="3" fill="#38bdf8" />
          <rect x="52" y="68" width="28" height="20" rx="3" fill="#10b981" />
          <rect x="86" y="68" width="28" height="20" rx="3" fill="#334155" stroke="#64748b" />
          <path d="M 140 82 L 140 22 L 182 22 L 182 82 L 224 82 L 224 22" fill="none" stroke="#38bdf8" stroke-width="2.2" stroke-dasharray="4 2" />
          <circle cx="140" cy="52" r="5" fill="#10b981" />
          <circle cx="182" cy="38" r="5" fill="#fbbf24" />
          <circle cx="224" cy="22" r="5.5" fill="#38bdf8" />
          <text x="182" y="98" text-anchor="middle" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">FAST PICK &amp; ATP</text>
        `;
      } else if (topology === 'multimodal_corridor_vrp') {
        stage2Kicker = '2 · TRACK LANES & LOADS';
        stage3Kicker = '3 · ROUTE & 3D LOAD OPTIMIZER';
        centerGraphic = `
          <rect class="svg-viz-well" width="248" height="106" rx="10" stroke="#38bdf866" stroke-width="1.2" />
          <path d="M 22 38 Q 76 10, 130 30 T 226 18" fill="none" stroke="#38bdf8" stroke-width="2.4" stroke-dasharray="4 2" />
          <circle cx="22" cy="38" r="5.5" fill="#f59e0b" />
          <circle cx="130" cy="30" r="5.5" fill="#38bdf8" />
          <circle cx="226" cy="18" r="6" fill="#10b981" />
          <rect x="22" y="56" width="154" height="32" rx="4" fill="rgba(15,23,42,0.85)" stroke="#94a3b8" stroke-width="1.4" />
          <rect x="26" y="60" width="36" height="24" rx="2" fill="#10b981" />
          <rect x="66" y="60" width="36" height="24" rx="2" fill="#38bdf8" />
          <rect x="106" y="60" width="36" height="24" rx="2" fill="#fbbf24" />
          <text x="184" y="72" fill="#10b981" font-size="9.5" font-weight="800" font-family="var(--font-mono)">94% CUBE</text>
          <text x="184" y="86" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">BEST ROUTE</text>
        `;
      } else if (topology === 'circular_warroom_triage') {
        stage2Kicker = '2 · ASSESS RISK & IMPACT';
        stage3Kicker = '3 · 3-OPTION DECISION ENGINE';
        centerGraphic = `
          <rect class="svg-viz-well" width="248" height="106" rx="10" stroke="#fb718566" stroke-width="1.2" />
          <path d="M 34 53 L 84 22 M 34 53 L 84 53 M 34 53 L 84 84" stroke="#94a3b8" stroke-width="2.2" />
          <circle cx="34" cy="53" r="13" fill="#f43f5e" />
          <text x="34" y="57" text-anchor="middle" fill="#ffffff" font-size="9" font-weight="800">AI</text>
          <rect x="84" y="10" width="148" height="24" rx="5" fill="rgba(16,185,129,0.18)" stroke="#10b981" stroke-width="1.4" />
          <text x="92" y="26" fill="#10b981" font-size="9.5" font-weight="800" font-family="var(--font-mono)">✓ OPTION A · BEST ROI</text>
          <rect x="84" y="41" width="148" height="24" rx="5" fill="rgba(56,189,248,0.16)" stroke="#38bdf8" stroke-width="1.4" />
          <text x="92" y="57" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">• OPTION B · BACKUP</text>
          <rect x="84" y="72" width="148" height="24" rx="5" fill="rgba(245,158,11,0.16)" stroke="#f59e0b" stroke-width="1.4" />
          <text x="92" y="88" fill="#fbbf24" font-size="9.5" font-weight="800" font-family="var(--font-mono)">• OPTION C · ESCALATE</text>
        `;
      } else {
        // Default: milp_pareto_loop
        stage2Kicker = '2 · CHECK CONSTRAINTS';
        stage3Kicker = '3 · AI & MATH OPTIMIZER';
        centerGraphic = `
          <rect class="svg-viz-well" width="248" height="106" rx="10" stroke="${cls.color}66" stroke-width="1.2" />
          <path d="M 24 20 C 30 72, 72 88, 134 92" fill="none" stroke="${cls.color}" stroke-width="2.6" />
          <circle cx="36" cy="46" r="5" fill="#38bdf8" />
          <circle cx="68" cy="74" r="6" fill="#10b981" stroke="#ffffff" stroke-width="1.6" />
          <circle cx="110" cy="88" r="5" fill="#fbbf24" />
          <text x="80" y="74" fill="#10b981" font-size="9.5" font-weight="800" font-family="var(--font-mono)">★ OPTIMAL PLAN</text>
          <circle cx="196" cy="53" r="28" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="6 3" />
          <circle r="4" fill="#10b981">
            <animateMotion dur="2.2s" repeatCount="indefinite" path="M 196 25 A 28 28 0 1 1 195.9 25" />
          </circle>
          <text x="196" y="57" text-anchor="middle" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">SOLVER</text>
        `;
      }

      return `
        <!-- Animated Connection Arrows Across the 4 Simple, Meaningful Stages -->
        <path d="M 232 90 C 254 90, 254 132, 272 132" fill="none" stroke="${dept.color}" stroke-width="2.4" stroke-dasharray="5 3" />
        <path d="M 232 206 C 254 206, 254 164, 272 164" fill="none" stroke="#38bdf8" stroke-width="2.4" stroke-dasharray="5 3" />
        <circle r="4" fill="${dept.color}"><animateMotion dur="1.6s" repeatCount="indefinite" path="M 232 90 C 254 90, 254 132, 272 132" /></circle>
        <circle r="4" fill="#38bdf8"><animateMotion dur="1.9s" repeatCount="indefinite" path="M 232 206 C 254 206, 254 164, 272 164" /></circle>

        <path d="M 488 148 L 524 148" fill="none" stroke="#38bdf8" stroke-width="2.8" marker-end="url(#arrowCyan_${uid})" />
        <circle r="4" fill="#38bdf8"><animateMotion dur="1.4s" repeatCount="indefinite" path="M 488 148 L 524 148" /></circle>

        <path d="M 808 148 L 844 148" fill="none" stroke="#10b981" stroke-width="2.8" marker-end="url(#arrowGreen_${uid})" />
        <circle r="4" fill="#10b981"><animateMotion dur="1.4s" repeatCount="indefinite" path="M 808 148 L 844 148" /></circle>

        <!-- STAGE 1: LIVE DATA INPUTS (2 Clean, Readable Source Cards) -->
        <g transform="translate(12, 32)">
          <rect class="svg-node-box" width="220" height="106" rx="16" stroke="${dept.color}" stroke-width="2" />
          <text x="16" y="28" font-size="18">${ic1}</text>
          <text x="42" y="26" fill="${dept.color}" font-size="10.5" font-weight="800" font-family="var(--font-mono)">1A · LIVE INPUT SOURCE</text>
          <text x="16" y="54" class="svg-text-main" font-size="14" font-weight="800">${trunc(sys1, 23)}</text>
          <text x="16" y="78" class="svg-text-sub" font-size="11.5">Real-time operational feed</text>
        </g>

        <g transform="translate(12, 156)">
          <rect class="svg-node-box" width="220" height="106" rx="16" stroke="#38bdf8" stroke-width="2" />
          <text x="16" y="28" font-size="18">${ic2}</text>
          <text x="42" y="26" fill="#38bdf8" font-size="10.5" font-weight="800" font-family="var(--font-mono)">1B · DIGITAL TWIN &amp; ERP</text>
          <text x="16" y="54" class="svg-text-main" font-size="14" font-weight="800">${trunc(sys2, 23)}</text>
          <text x="16" y="78" class="svg-text-sub" font-size="11.5">+ ${trunc(sys3, 22)}</text>
        </g>

        <!-- STAGE 2: WHAT THE AGENT CHECKS & CORRELATES -->
        <g transform="translate(272, 32)">
          <rect class="svg-node-box-alt" width="216" height="230" rx="16" stroke="#38bdf8" stroke-width="2.2" />
          <text x="16" y="28" fill="#38bdf8" font-size="10.5" font-weight="800" font-family="var(--font-mono)">🔍 ${stage2Kicker}</text>
          <text x="16" y="54" class="svg-text-main" font-size="14.5" font-weight="800">${trunc(subs[0].name, 22)}</text>
          <text x="16" y="76" class="svg-text-sub" font-size="11.5">${role1}</text>

          <rect class="svg-pill-bg" x="14" y="96" width="188" height="46" rx="10" stroke="rgba(56,189,248,0.4)" />
          <text x="24" y="116" fill="#38bdf8" font-size="11" font-weight="800">✓ Reads ${tablesCount} Live Data Tables</text>
          <text x="24" y="133" class="svg-text-sub" font-size="10.5">Spots gaps, stockouts &amp; risks</text>

          <rect class="svg-pill-bg" x="14" y="152" width="188" height="46" rx="10" stroke="rgba(16,185,129,0.4)" />
          <text x="24" y="172" fill="#10b981" font-size="11" font-weight="800">✓ Zero-Hallucination Grounding</text>
          <text x="24" y="189" class="svg-text-sub" font-size="10.5">Every number tied to live rows</text>
        </g>

        <!-- STAGE 3: HOW AI & MATH SOLVE IT (With Meaningful Visual Graphic) -->
        <g transform="translate(524, 18)">
          <rect class="svg-node-box-alt" width="284" height="258" rx="18" stroke="${cls.color}" stroke-width="2.5" />
          <rect x="16" y="14" width="252" height="26" rx="8" fill="${cls.color}26" stroke="${cls.color}" />
          <text x="142" y="31" text-anchor="middle" class="svg-text-main" font-size="10.5" font-weight="800" font-family="var(--font-mono)">🧠 ${stage3Kicker}</text>
          <text x="18" y="60" class="svg-text-main" font-size="15" font-weight="800">${trunc(subs[1].name, 26)}</text>
          <text x="18" y="80" fill="${cls.color}" font-size="11.5" font-weight="700">${trunc(solverLabel, 34)}</text>

          <g transform="translate(18, 92)">
            ${centerGraphic}
          </g>

          <text x="18" y="220" class="svg-text-main" font-size="11.5" font-weight="700">• ${role2}</text>
          <text x="18" y="240" fill="#10b981" font-size="11.5" font-weight="800">• Models: Gemini 3.8 Flash ↔ Gemini 3.1 Pro / 4 Argon</text>
        </g>

        <!-- STAGE 4: SAFETY CHECK, AUTOMATED ACTION & BUSINESS RESULT -->
        <g transform="translate(844, 32)">
          <rect class="svg-node-box-out" width="264" height="230" rx="16" stroke="#10b981" stroke-width="2.2" />
          <text x="16" y="28" fill="#10b981" font-size="10.5" font-weight="800" font-family="var(--font-mono)">⚡ ${stage4Kicker}</text>
          <text x="16" y="54" class="svg-text-main" font-size="14.5" font-weight="800">${writebackLabel}</text>
          <text x="16" y="75" class="svg-text-sub" font-size="11.5">Owner: ${personaShort}</text>

          <rect class="svg-pill-bg" x="14" y="92" width="236" height="44" rx="10" stroke="#f59e0b66" />
          <text x="24" y="111" fill="#fbbf24" font-size="11" font-weight="800">🛡️ Safety &amp; Policy Gate First</text>
          <text x="24" y="127" class="svg-text-sub" font-size="10.5">Auto-commits in bounds; escalates &gt;20% shift</text>

          <rect class="svg-pill-bg" x="14" y="146" width="236" height="68" rx="10" stroke="#10b98166" />
          <text x="24" y="168" fill="#10b981" font-size="12.5" font-weight="800">🚀 Result: ${badgeLabel}</text>
          <text x="24" y="186" class="svg-text-sub" font-size="11">Writes back to ERP/WMS + renders</text>
          <text x="24" y="202" fill="#38bdf8" font-size="11" font-weight="700">✦ Interactive A2UI VegaChart &amp; Table</text>
        </g>
      `;
    }"""


def update_html_files() -> None:
    for path in HTML_FILES:
        text = path.read_text(encoding="utf-8")

        # 1. Add CSS for .agent-what-it-does-box right before .sc-flip-card
        what_css = """    .agent-what-it-does-box {
      background: var(--bg-elevated);
      border: 1.5px solid var(--border-subtle);
      border-left: 5px solid var(--what-accent, #38bdf8);
      border-radius: 16px;
      padding: 20px 24px;
      margin-bottom: 20px;
    }
    html[data-theme="light"] .agent-what-it-does-box {
      background: #f8fafc;
      border-color: rgba(15, 23, 42, 0.12);
      border-left: 5px solid var(--what-accent, #2563eb);
    }
    .agent-what-summary {
      font-size: 16.5px;
      font-weight: 600;
      color: var(--text-primary);
      line-height: 1.65;
      margin: 0 0 14px;
    }
    .agent-what-bullets {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 12px;
      margin: 0;
      padding: 0;
      list-style: none;
    }
    .agent-what-bullets li {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 12px 15px;
      font-size: 14.5px;
      line-height: 1.55;
      color: var(--text-secondary);
    }
    .agent-what-bullets li strong {
      display: block;
      font-size: 12px;
      font-family: var(--font-mono);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-primary);
      margin-bottom: 4px;
    }
"""
        if ".agent-what-it-does-box {" not in text:
            text = text.replace("    .sc-flip-card {", what_css + "    .sc-flip-card {", 1)

        # 2. Replace renderFullTopologySvg with our simpler, larger-text, meaningful 4-stage diagram
        start_marker = "    function renderFullTopologySvg(topology, ctx) {"
        end_marker = "    function shortStepHeading(rawTitle, fallback) {"
        assert start_marker in text and end_marker in text, f"Topology markers missing in {path}"
        s_idx = text.index(start_marker)
        e_idx = text.index(end_marker)
        text = text[:s_idx] + NEW_RENDER_FULL_TOPOLOGY_SVG + "\n\n" + text[e_idx:]

        # Adjust SVG viewBox height from 326 to 288 for cleaner aspect ratio
        text = text.replace('<svg class="ag-flow-svg" viewBox="0 0 1120 326">', '<svg class="ag-flow-svg" viewBox="0 0 1120 288">')

        # 3. Add the clear "What This Agent Does" few-liner box + Playbook button inside openAgentPage
        old_hero_top = """              <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                <span class="build-tier-badge ${cls.cssClass}">${cls.label}</span>
              </div>
            </div>

            <!-- 3 Big-Heading Flippable Summary Cards -->"""

        new_hero_top = """              <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                <a href="agent_testing_and_video_playbook.html#agent-${ag.id}"
                   style="text-decoration:none; font-size:13.5px; font-weight:700; padding:8px 16px; border-radius:999px; background:rgba(56,189,248,0.14); color:#38bdf8; border:1.5px solid rgba(56,189,248,0.4);">
                  📋 Demo Data &amp; Test Playbook &rarr;
                </a>
                <span class="build-tier-badge ${cls.cssClass}">${cls.label}</span>
              </div>
            </div>

            <!-- Simple, Clear Few-Liner Explanation of What This Agent Is Supposed to Do -->
            <div class="agent-what-it-does-box" style="--what-accent:${dept.color};">
              <div style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.07em; color:${dept.color}; margin-bottom:6px;">
                ✦ WHAT THIS AGENT DOES AT A GLANCE
              </div>
              <p class="agent-what-summary">
                ${ag.solution}
              </p>
              <ul class="agent-what-bullets">
                <li>
                  <strong style="color:#fb7185;">✕ When &amp; Why It Runs</strong>
                  ${shortSentence(ag.problem, 135)}
                </li>
                <li>
                  <strong style="color:#38bdf8;">🧠 How It Works</strong>
                  Combines <b>${toOpenTechLabel(ag.solverStack || 'AI & Mathematical Optimization')}</b> with live enterprise tables to find the best decision.
                </li>
                <li>
                  <strong style="color:#10b981;">⚡ What Action It Takes</strong>
                  Executes <b>${toOpenTechLabel(ag.apiWriteback || 'Governed ERP / WMS Write-Back')}</b> within safety limits to deliver <b>${ag.badge || 'Verified ROI'}</b>.
                </li>
              </ul>
            </div>

            <!-- 3 Big-Heading Flippable Summary Cards -->"""

        if old_hero_top in text:
            text = text.replace(old_hero_top, new_hero_top, 1)

        # Also make the front of the 3 Flippable Summary Cards show a meaningful 1-line preview instead of generic "Click to read problem"
        text = text.replace(
            '<span class="sc-flip-pill">Click to read problem</span>',
            '<span class="sc-flip-pill">${shortSentence(ag.problem, 68)}</span>'
        )
        text = text.replace(
            '<span class="sc-flip-pill">Click to read solution</span>',
            '<span class="sc-flip-pill">${shortSentence(ag.solution, 68)}</span>'
        )
        text = text.replace(
            '<span class="sc-flip-pill">Click to read outcome</span>',
            '<span class="sc-flip-pill">${shortSentence(ag.outcome, 68)}</span>'
        )

        # 4. Add a link to agent_testing_and_video_playbook.html in the top navbar right next to FinOps Deck
        old_nav_link = '<a href="cost_analysis_presentation.html" class="nav-link"'
        new_nav_link = '<a href="agent_testing_and_video_playbook.html" class="nav-link" style="color:#10b981; font-weight:700;">📋 Demo Playbook</a>\n        <a href="cost_analysis_presentation.html" class="nav-link"'
        if 'href="agent_testing_and_video_playbook.html"' not in text and old_nav_link in text:
            text = text.replace(old_nav_link, new_nav_link, 1)

        path.write_text(text, encoding="utf-8")
        print(f"Updated {path.name}")


if __name__ == "__main__":
    build_playbooks()
    update_html_files()

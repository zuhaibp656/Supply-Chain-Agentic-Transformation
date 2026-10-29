#!/usr/bin/env python3
"""Builds:
1. Upgraded Manual Verification & Customer Demo Playbook (`agent_testing_and_video_playbook.html` & `AGENT_TESTING_AND_VIDEO_PLAYBOOK.md`):
   - Runs `extract_normalized_scenario(agent_id)` across all 60 agents so every single agent card contains:
     a) Plain-English Customer Pitch & Problem Explanation (with all abbreviations spelled out inline).
     b) "Assuming You Give This Input -> Here Is the Exact Output You Should Receive" side-by-side verification panel.
     c) Real rendered Markdown output & table, expected A2UI VegaChart title/type/axes, and expected Write-Back JSON receipt.
     d) Interactive 5-checkbox Manual Testing Checklist (saved in localStorage) to verify the agent uses all resources, renders A2UI graphics, and replies accurately.
2. Separate Interactive Visual Learning Asset (`supply_chain_101_interactive_academy.html` & `SUPPLY_CHAIN_101_MASTER_GUIDE.md`):
   - Visual, interactive "Learn Supply Chain From Zero" Academy with:
     - Module 1: Interactive 6-Stage Product Journey + 3 Flows Visualizer + Interactive Bullwhip Effect Slider Simulator
     - Module 2: Interactive 6 Pillars & 20 Sub-Pillars Visual Process Map (explained in plain everyday words)
     - Module 3: 56 Interactive 3D Flip-Flashcards decoding every Supply Chain abbreviation (OTIF, S&OP, WAPE, FVA, SKU, BOM, RFQ, 3-Way Match, OEE, MEIO, ATP, WMS, TMS,ERP, MES, FEFO/LIFO, FTL/LTL, Demurrage, BOL/ASN/POD, RMA, CCC, Scope 3/CBAM, etc.) with real-world number examples and customer talking points
     - Module 4: 4 Step-by-Step Interactive Workflow Simulators (Forecast-to-Plan, Source-to-Pay, Order-to-Delivery, Disruption-to-Recovery)
     - Module 5: Customer Conversation Decoder ("When Customer Says X -> What It Means -> Which Agent to Demo")
     - Module 6: 12-Question Interactive Self-Quiz with instant feedback
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from test_agent_demo import extract_normalized_scenario, load_catalog
from svg_infographics_helper import render_agent_flow_svg, render_vega_svg_preview


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

# Glossary of common abbreviations to automatically spell out the first time they appear in customer explanations
ACRONYM_EXPANSIONS = [
    (r"\bPOS\b", "POS (Point of Sale — cash-register store scans)"),
    (r"\bS&OP\b", "S&OP (Sales & Operations Planning — monthly alignment meeting)"),
    (r"\bIBP\b", "IBP (Integrated Business Planning software)"),
    (r"\bCPFR\b", "CPFR (Collaborative Planning, Forecasting & Replenishment with retailers)"),
    (r"\bWAPE\b", "WAPE (Weighted Absolute Percentage Error — forecast error %)"),
    (r"\bFVA\b", "FVA (Forecast Value Added — whether human edits improved or hurt the forecast)"),
    (r"\bNPI\b", "NPI (New Product Introduction — launching a new item)"),
    (r"\bPIR\b", "PIR (Planned Independent Requirements — target forecast quantity in ERP)"),
    (r"\bSKU\b", "SKU (Stock Keeping Unit — a specific product code)"),
    (r"\bBOM\b", "BOM (Bill of Materials — the recipe/parts list to build a product)"),
    (r"\bRFQ\b", "RFQ (Request for Quotation — asking suppliers for price bids)"),
    (r"\bNCR\b", "NCR (Non-Conformance Report — defective supplier batch alert)"),
    (r"\bCOPQ\b", "COPQ (Cost of Poor Quality — money lost from defects)"),
    (r"\bOEE\b", "OEE (Overall Equipment Effectiveness — factory machine uptime & efficiency %)"),
    (r"\bMPS\b", "MPS (Master Production Schedule — factory build plan)"),
    (r"\bMES\b", "MES (Manufacturing Execution System — factory floor software)"),
    (r"\bPLC\b", "PLC (Programmable Logic Controller — machine hardware controller)"),
    (r"\beBHR\b", "eBHR (Electronic Batch History Record — FDA quality log)"),
    (r"\bCapEx\b", "CapEx (Capital Expenditure — buying heavy equipment)"),
    (r"\bMEIO\b", "MEIO (Multi-Echelon Inventory Optimization — balancing stock across Plant, Regional DC, Local DC & Store)"),
    (r"\bWMS\b", "WMS (Warehouse Management System — software running the warehouse)"),
    (r"\bTMS\b", "TMS (Transportation Management System — software managing trucks & carriers)"),
    (r"\bATP\b", "ATP (Available-to-Promise — uncommitted stock ready to sell right now)"),
    (r"\bSLOB\b", "SLOB (Slow-Moving & Obsolete inventory sitting unsold)"),
    (r"\bFEFO\b", "FEFO (First-Expired, First-Out — shipping oldest expiry dates first)"),
    (r"\bLIFO\b", "LIFO (Last-In, First-Out — loading the truck so the first delivery stop is right at the back door)"),
    (r"\bVRP\b", "VRP (Vehicle Routing Problem — math solver for multi-stop truck routes)"),
    (r"\bCVRPTW\b", "CVRPTW (Capacitated Vehicle Routing with Time Windows)"),
    (r"\bHOS\b", "HOS (Hours of Service — legal driving-hour limits for truck drivers)"),
    (r"\bELD\b", "ELD (Electronic Logging Device — truck cab GPS & hours tracker)"),
    (r"\bULD\b", "ULD (Unit Load Device — contoured aviation cargo container)"),
    (r"\bASN\b", "ASN (Advance Shipping Notice — EDI 856 pre-arrival manifest)"),
    (r"\bBOL\b", "BOL (Bill of Lading — legal freight shipping contract)"),
    (r"\bePOD\b", "ePOD (Electronic Proof of Delivery)"),
    (r"\bOS&D\b", "OS&D (Over, Short & Damaged freight claims)"),
    (r"\bOTIF\b", "OTIF (On-Time In-Full — delivering 100% of ordered units before the deadline)"),
    (r"\bRMA\b", "RMA (Return Merchandise Authorization — customer return approval)"),
    (r"\bCBAM\b", "CBAM (Carbon Border Adjustment Mechanism — EU carbon import tax)"),
    (r"\bEUDR\b", "EUDR (EU Deforestation Regulation)"),
    (r"\bRTI\b", "RTI (Returnable Transport Items — reusable plastic crates, kegs & pallets)"),
    (r"\bCCC\b", "CCC (Cash Conversion Cycle — days cash is tied up in inventory & invoices)"),
    (r"\bMILP\b", "MILP (Mixed-Integer Linear Programming — mathematical optimization solver)"),
]


def expand_acronyms_once(text: str) -> str:
    """Expands supply chain abbreviations the first time they appear in a text block."""
    out = str(text or "")
    for pattern, replacement in ACRONYM_EXPANSIONS:
        if re.search(pattern, out):
            # Avoid double-expanding if already followed by '('
            out = re.sub(pattern + r"(?!\s*\()", replacement, out, count=1)
    return out


def clean_agent_name(raw_name: str) -> str:
    s = str(raw_name or "").strip()
    s = re.sub(r"^\[[^\]]+\]\s*", "", s)
    return s


def get_re_id(agent_id: str) -> str | None:
    p = ROOT / "agents" / agent_id / ".reasoning_engine_id"
    if p.exists():
        return p.read_text(encoding="utf-8").strip()
    return None


def md_to_simple_html(md_text: str) -> str:
    """Converts agent markdown output (headings, blockquotes, tables, bullets) into clean styled HTML."""
    lines = [line.rstrip() for line in str(md_text or "").splitlines()]
    out_html: list[str] = []
    in_table = False
    in_list = False

    def format_inline(s: str) -> str:
        s = html.escape(s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"`([^`]+)`", r'<code class="pb-inline-code">\1</code>', s)
        return s

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_table:
                out_html.append("</tbody></table></div>")
                in_table = False
            if in_list:
                out_html.append("</ul>")
                in_list = False
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if all(re.match(r"^:?-{2,}:?$", c) for c in cells):
                continue
            if not in_table:
                out_html.append('<div class="pb-md-table-wrap"><table class="pb-md-table"><thead><tr>')
                for c in cells:
                    out_html.append(f"<th>{format_inline(c)}</th>")
                out_html.append("</tr></thead><tbody>")
                in_table = True
            else:
                out_html.append("<tr>")
                for c in cells:
                    out_html.append(f"<td>{format_inline(c)}</td>")
                out_html.append("</tr>")
            continue

        if in_table:
            out_html.append("</tbody></table></div>")
            in_table = False

        if stripped.startswith("### "):
            if in_list:
                out_html.append("</ul>")
                in_list = False
            out_html.append(f'<h4 class="pb-md-h3">{format_inline(stripped[4:])}</h4>')
        elif stripped.startswith("#### "):
            if in_list:
                out_html.append("</ul>")
                in_list = False
            out_html.append(f'<h5 class="pb-md-h4">{format_inline(stripped[5:])}</h5>')
        elif stripped.startswith("> "):
            if in_list:
                out_html.append("</ul>")
                in_list = False
            out_html.append(f'<blockquote class="pb-md-quote">{format_inline(stripped[2:])}</blockquote>')
        elif stripped.startswith("- "):
            if not in_list:
                out_html.append('<ul class="pb-md-ul">')
                in_list = True
            out_html.append(f"<li>{format_inline(stripped[2:])}</li>")
        else:
            if in_list:
                out_html.append("</ul>")
                in_list = False
            out_html.append(f'<p class="pb-md-p">{format_inline(stripped)}</p>')

    if in_table:
        out_html.append("</tbody></table></div>")
    if in_list:
        out_html.append("</ul>")
    return "\n".join(out_html)


def describe_vega_spec(vega: dict) -> dict:
    """Extracts human-readable chart title, mark type, and sample data points from a Vega-Lite spec."""
    title = vega.get("title", "Operational A2UI Visual Surface")
    if isinstance(title, dict):
        title = title.get("text", "Operational A2UI Visual Surface")

    mark = vega.get("mark")
    if isinstance(mark, dict):
        mark_type = mark.get("type", "bar")
    elif isinstance(mark, str):
        mark_type = mark
    elif "layer" in vega:
        marks = []
        for lyr in vega.get("layer", []):
            m = lyr.get("mark")
            marks.append(m.get("type", "line") if isinstance(m, dict) else str(m or "line"))
        mark_type = " + ".join(dict.fromkeys(marks))
    else:
        mark_type = "bar / line"

    values = vega.get("data", {}).get("values", [])
    sample_points = []
    for row in values[:3]:
        if isinstance(row, dict):
            kv = [f"{k}={v}" for k, v in list(row.items())[:3]]
            sample_points.append(", ".join(kv))

    return {
        "title": str(title),
        "mark_type": str(mark_type).upper(),
        "data_rows": len(values),
        "sample_points": " | ".join(sample_points) if sample_points else "Live fixture series",
    }


def build_upgraded_playbook() -> None:
    cat = load_catalog()
    agents_dict = cat.get("agents", {})
    personas_dict = cat.get("personas", {})

    by_dept: dict[str, list[dict]] = {pid: [] for pid, _, _ in PILLAR_ORDER}
    for ag in agents_dict.values():
        did = ag.get("deptId", "demand_sop")
        by_dept.setdefault(did, []).append(ag)

    md_lines = [
        "# 🎬 Supply Chain AI Agents — Manual Testing, Expected Output & Customer Explanation Playbook",
        "",
        "> **Built for Manual Verification & Customer Demos**: For all **60 Supply Chain AI Agents**, this playbook gives you:",
        "> 1. **Plain-English Customer Explanation (Zero Unexplained Abbreviations)**: What problem the customer has, why it matters, and how this agent solves it — with every acronym (`OTIF`, `WAPE`, `S&OP`, `ATP`, `MEIO`, etc.) spelled out and explained.",
        "> 2. **Exact Input Data -> Exact Expected Output**: What input prompt you give, which demo data tables & resources the agent must read, the **exact Markdown table & numbers** it must reply with, the **exact A2UI `VegaChart` graphic** it must render, and the **exact ERP/WMS Write-Back receipt** it must return.",
        "> 3. **5-Point Manual Verification Checklist**: So you can verify manually that every agent does what it says, uses all its resources, and renders its A2UI graphics.",
        "",
        "> 💡 **New to Supply Chain?** Open the companion **[🎓 Supply Chain 101 Interactive Academy (`supply_chain_101_interactive_academy.html`)](supply_chain_101_interactive_academy.html)** (or **[`SUPPLY_CHAIN_101_MASTER_GUIDE.md`](SUPPLY_CHAIN_101_MASTER_GUIDE.md)**) to learn Supply Chain from scratch with visual diagrams, 56 3D flip-flashcards, and a Customer Conversation Decoder!",
        "",
        "---",
        "",
    ]

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
            tables = adk.get("fixtureTables", [])
            tools_meta = spec.get("toolsMeta", [])
            read_tools = [t["name"] for t in tools_meta if t.get("kind") != "action"] or [t for t in adk.get("tools", []) if not t.startswith("action_") and t != "list_systems"]
            write_tools = [t["name"] for t in tools_meta if t.get("kind") == "action"] or [t for t in adk.get("tools", []) if t.startswith("action_")]

            # Run the real agent scenario to capture exact expected output!
            norm = extract_normalized_scenario(ag_id)
            demo_prompt = norm["query"]
            vega_info = describe_vega_spec(norm["vega_spec"])
            actions_list = norm["actions"]
            expected_md = norm["markdown"]

            # Expand abbreviations in Problem, Solution, and Outcome for easy customer explanation
            prob_explained = expand_acronyms_once(ag.get("problem", ""))
            sol_explained = expand_acronyms_once(ag.get("solution", ""))
            out_explained = expand_acronyms_once(ag.get("outcome", ""))

            # Summarize concrete input data values from the first 2 fixture tables
            input_data_bullets_md = []
            input_data_bullets_html = []
            for t in tables:
                tname = t.get("table_name", "")
                rows = t.get("rows", [])
                cols = t.get("columns", [])
                if rows and isinstance(rows[0], dict):
                    r0 = rows[0]
                    kv_str = ", ".join(f"{k}={v}" for k, v in list(r0.items())[:5])
                    input_data_bullets_md.append(f"  - Table `{tname}.json` ({len(rows)} rows): Sample input record has `{kv_str}`")
                    first_row_pretty = html.escape(json.dumps(r0, indent=2, ensure_ascii=False))
                    input_data_bullets_html.append(f"""
                      <div class="pb-table-item">
                        <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; flex-wrap:wrap;">
                          <code class="pb-code-pill">🗄️ {html.escape(tname)}.json</code>
                          <span style="font-size:12px; color:var(--text-secondary); font-family:var(--font-mono);">{len(rows)} rows · {len(cols)} cols</span>
                        </div>
                        <div style="font-size:13px; color:var(--text-primary); margin-top:6px; line-height:1.5;">
                          <strong>Sample Input Values:</strong> <code style="font-size:12px; color:#cbd5e1;">{html.escape(kv_str)}</code>
                        </div>
                        <details style="margin-top:6px;">
                          <summary style="cursor:pointer; font-size:12px; font-weight:700; color:#38bdf8;">▾ View Full JSON Input Record</summary>
                          <pre class="pb-json-pre">{first_row_pretty}</pre>
                        </details>
                      </div>
                    """)

            receipt_str = json.dumps(actions_list[0], ensure_ascii=False) if actions_list else '{"status": "COMMITTED"}'
            receipt_pretty = html.escape(json.dumps(actions_list, indent=2, ensure_ascii=False))

            # Append to Markdown Playbook
            md_lines.extend([
                f"### {total_idx}. {c_name} (`{ag_id}`)",
                f"- **Pillar / Sub-Pillar**: {pillar_title} — **{sub_pillar}** · **Persona**: {persona_name} · **ROI**: `{ag.get('badge', '')}`",
                "",
                "#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)",
                f"- **The Customer Problem**: {prob_explained}",
                f"- **What This Agent Does**: {sol_explained}",
                f"- **Business Result**: {out_explained} (**{ag.get('badge', '')}**).",
                "",
                "#### 📥 1. Input You Give & Demo Data Resources Used",
                f"- **Prompt to Type / Paste**:",
                f"  > `{demo_prompt}`",
                f"- **Read Tools It Must Call**: `{', '.join(read_tools)}`",
                f"- **Write-Back Tools It Must Call**: `{', '.join(write_tools)}`",
                "- **Demo Data Input Values It Reads**:",
                *input_data_bullets_md,
                "",
                "#### 📤 2. Exact Output You Must Receive When Testing Manually",
                f"- **Expected A2UI Visual Card (`VegaChart`)**:",
                f"  - **Chart Title**: `{vega_info['title']}`",
                f"  - **Visual Mark Type**: `{vega_info['mark_type']}` ({vega_info['data_rows']} data points: `{vega_info['sample_points']}`)",
                f"- **Expected Write-Back Receipt**: `{receipt_str}`",
                "- **Expected Markdown Report & Table**:",
                "",
                expected_md,
                "",
                "#### ✅ 3. Manual Verification Checklist",
                f"- [ ] **Resource Check**: Agent invoked `{', '.join(read_tools[:2])}` against its `{len(tables)}` fixture tables.",
                f"- [ ] **A2UI Graphic Check**: Agent rendered the `{vega_info['title']}` (`{vega_info['mark_type']}`) visual surface.",
                "- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.",
                f"- [ ] **Governance Gate Check**: Calling `{write_tools[0] if write_tools else 'action_commit'}` without `idempotency_key` triggers `missing_idempotency_key`.",
                "",
                "---",
                "",
            ])

            # Build HTML Card for agent_testing_and_video_playbook.html
            rendered_expected_md_html = md_to_simple_html(expected_md)
            cmd_run = f"python3 scripts/test_agent_demo.py {ag_id}"
            cmd_data = f"python3 scripts/test_agent_demo.py {ag_id} --show-data"
            cmd_gate = f"python3 scripts/test_agent_demo.py {ag_id} --test-guardrail"

            cloud_pill_html = (
                f'<span class="pb-badge" style="background:rgba(16,185,129,0.16); color:#10b981; border-color:rgba(16,185,129,0.4);">🟢 Cloud Deployed (RE {re_id.split("/")[-1][:8]}…)</span>'
                if re_id else
                '<span class="pb-badge">📦 Local ADK Package Ready</span>'
            )

            html_cards.append(f"""
              <article class="pb-agent-card" id="agent-{ag_id}" data-pillar="{dept_id}" data-cloud="{'true' if re_id else 'false'}" data-search="{html.escape((c_name + ' ' + ag_id + ' ' + sub_pillar + ' ' + persona_name + ' ' + prob_explained + ' ' + sol_explained).lower())}" style="--pillar-color:{pillar_color};">
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

                <!-- 1. Plain-English Customer Pitch & Problem Explanation (With Abbreviations Spelled Out) -->
                <div class="pb-what-box">
                  <div class="pb-section-kicker">🗣️ 1 · HOW TO EXPLAIN THIS AGENT TO A CUSTOMER (PLAIN ENGLISH, ABBREVIATIONS DECODED)</div>
                  <div class="pb-what-grid">
                    <div class="pb-what-item">
                      <span class="pb-what-label" style="color:#fb7185;">✕ The Problem in Plain Words</span>
                      <p>{html.escape(prob_explained)}</p>
                    </div>
                    <div class="pb-what-item">
                      <span class="pb-what-label" style="color:#38bdf8;">✦ What This Agent Does</span>
                      <p>{html.escape(sol_explained)}</p>
                    </div>
                    <div class="pb-what-item">
                      <span class="pb-what-label" style="color:#10b981;">🚀 Business Outcome to Promise</span>
                      <p>{html.escape(out_explained)}</p>
                    </div>
                  </div>
                </div>

                <!-- 1B. Visual 4-Stage Agent Execution Diagram -->
                {render_agent_flow_svg(c_name, tables, read_tools, write_tools, vega_info['title'], pillar_color)}

                <!-- 2. Side-by-Side: Input You Give & Resources Used vs. Exact Expected Output -->
                <div class="pb-two-col">
                  <!-- LEFT: Input Prompt, Demo Data Values & Manual Testing Checklist -->
                  <div class="pb-panel">
                    <div class="pb-section-kicker">📥 2 · INPUT YOU GIVE, DEMO DATA VALUES &amp; MANUAL CHECKLIST</div>

                    <div class="pb-prompt-box">
                      <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; margin-bottom:6px;">
                        <span style="font-size:11.5px; font-weight:800; text-transform:uppercase; color:#38bdf8; font-family:var(--font-mono);">💬 Step 1: Type / Paste This Input Prompt</span>
                        <button type="button" class="pb-copy-btn" data-copy="{html.escape(demo_prompt)}" onclick="copyPlaybookText(this)">📋 Copy Prompt</button>
                      </div>
                      <div style="font-size:14.5px; color:var(--text-primary); line-height:1.58; font-weight:600;">“{html.escape(demo_prompt)}”</div>
                    </div>

                    <div style="margin-bottom:14px;">
                      <div style="font-size:12px; font-weight:800; text-transform:uppercase; color:var(--text-secondary); font-family:var(--font-mono); margin-bottom:8px;">
                        🗄️ Step 2: Demo Data Tables &amp; Input Values It Reads ({len(tables)} Tables)
                      </div>
                      <div style="display:flex; flex-direction:column; gap:8px;">
                        {''.join(input_data_bullets_html)}
                      </div>
                    </div>

                    <!-- Interactive 5-Point Manual Verification Checklist -->
                    <div class="pb-checklist-box">
                      <div style="font-size:12px; font-weight:800; text-transform:uppercase; color:#10b981; font-family:var(--font-mono); margin-bottom:8px;">
                        ✅ Step 3: Manual Testing Verification Checklist (Click to Tick)
                      </div>
                      <label class="pb-check-row">
                        <input type="checkbox" onchange="saveCheckState('{ag_id}_1', this.checked)" id="chk_{ag_id}_1" />
                        <span><strong>Used All Data Resources:</strong> Called read tools (<code>{html.escape(', '.join(read_tools[:3]))}</code>) on the {len(tables)} demo tables above.</span>
                      </label>
                      <label class="pb-check-row">
                        <input type="checkbox" onchange="saveCheckState('{ag_id}_2', this.checked)" id="chk_{ag_id}_2" />
                        <span><strong>Rendered A2UI Visual Graphic:</strong> Displayed the <strong>{html.escape(vega_info['title'])}</strong> (<code>{html.escape(vega_info['mark_type'])}</code> chart) inside the visual card.</span>
                      </label>
                      <label class="pb-check-row">
                        <input type="checkbox" onchange="saveCheckState('{ag_id}_3', this.checked)" id="chk_{ag_id}_3" />
                        <span><strong>Accurate Output Numbers:</strong> Replied with the exact SKU/Facility/Order table and numbers shown on the right.</span>
                      </label>
                      <label class="pb-check-row">
                        <input type="checkbox" onchange="saveCheckState('{ag_id}_4', this.checked)" id="chk_{ag_id}_4" />
                        <span><strong>Executed Write-Back Tool:</strong> Invoked <code>{html.escape(', '.join(write_tools) or 'action_commit')}</code> and returned a signed confirmation ID.</span>
                      </label>
                      <label class="pb-check-row">
                        <input type="checkbox" onchange="saveCheckState('{ag_id}_5', this.checked)" id="chk_{ag_id}_5" />
                        <span><strong>Safety Gate Works:</strong> Blocks unapproved mutations when <code>idempotency_key</code> is missing.</span>
                      </label>
                    </div>

                    <div class="pb-cmd-grid" style="margin-top:12px;">
                      <button type="button" class="pb-copy-btn" data-copy="{html.escape(cmd_run)}" onclick="copyPlaybookText(this)">💻 Copy CLI Run</button>
                      <button type="button" class="pb-copy-btn" data-copy="{html.escape(cmd_data)}" onclick="copyPlaybookText(this)">🗄️ Copy Show-Data</button>
                      <button type="button" class="pb-copy-btn" data-copy="{html.escape(cmd_gate)}" onclick="copyPlaybookText(this)">🛡️ Copy Gate Test</button>
                    </div>
                  </div>

                  <!-- RIGHT: Exact Expected Output (A2UI Graphic Preview + Rendered Markdown Table + Write-Back Receipt) -->
                  <div class="pb-panel">
                    <div class="pb-section-kicker" style="color:#10b981;">📤 3 · EXACT OUTPUT YOU SHOULD RECEIVE (A2UI GRAPHIC + TABLE + WRITE-BACK)</div>

                    <!-- Expected A2UI Graphic Banner + Rendered SVG Infographic Preview -->
                    <div class="pb-a2ui-preview-box">
                      <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; flex-wrap:wrap; margin-bottom:6px;">
                        <span style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; color:#38bdf8;">📊 EXPECTED A2UI VISUAL CARD (VegaChart INFOGRAPHIC PREVIEW)</span>
                        <span class="pb-badge" style="color:#10b981; border-color:rgba(16,185,129,0.4);">Chart Type: {html.escape(vega_info['mark_type'])}</span>
                      </div>
                      <div style="font-size:15px; font-weight:800; color:var(--text-primary); margin-bottom:4px;">
                        {html.escape(vega_info['title'])}
                      </div>
                      <div style="font-size:12.5px; color:var(--text-secondary); font-family:var(--font-mono);">
                        Plotted Series ({vega_info['data_rows']} pts): {html.escape(vega_info['sample_points'])}
                      </div>
                      {render_vega_svg_preview(norm["vega_spec"], pillar_color)}
                    </div>


                    <!-- Expected Rendered Markdown Report & Copy-Ready Table -->
                    <div class="pb-expected-md-box">
                      <div style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; color:#a855f7; text-transform:uppercase; margin-bottom:8px;">
                        📋 EXPECTED MARKDOWN REPLY &amp; ATOMIC TABLE
                      </div>
                      {rendered_expected_md_html}
                    </div>

                    <!-- Expected Write-Back Receipt -->
                    <details style="margin-top:12px;">
                      <summary style="cursor:pointer; font-size:12.5px; font-weight:800; color:#10b981; font-family:var(--font-mono);">
                        ⚡ View Exact Expected ERP/WMS Write-Back JSON Receipt ({len(actions_list)} Action{'' if len(actions_list)==1 else 's'})
                      </summary>
                      <pre class="pb-json-pre" style="margin-top:8px;">{receipt_pretty}</pre>
                    </details>
                  </div>
                </div>
              </article>
            """)

    md_content = "\n".join(md_lines)
    (ROOT / "AGENT_TESTING_AND_VIDEO_PLAYBOOK.md").write_text(md_content, encoding="utf-8")
    (ROOT / "docs" / "AGENT_TESTING_AND_VIDEO_PLAYBOOK.md").write_text(md_content, encoding="utf-8")
    print("Updated AGENT_TESTING_AND_VIDEO_PLAYBOOK.md with real input->output walkthroughs for all 60 agents")

    playbook_html = f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Manual Testing, Expected Output &amp; Customer Playbook — 60 Supply Chain AI Agents</title>
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
      background: rgba(15, 23, 42, 0.92);
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
      background: rgba(255, 255, 255, 0.94);
    }}
    .pb-container {{
      max-width: 1580px;
      width: 93vw;
      margin: 0 auto;
      padding: 28px 0 80px;
    }}
    .pb-hero {{
      background: var(--bg-card);
      border: 1.5px solid var(--border-subtle);
      border-top: 4px solid #38bdf8;
      border-radius: 20px;
      padding: 26px 32px;
      margin-bottom: 24px;
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
      margin-bottom: 26px;
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
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
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
      line-height: 1.64;
      color: var(--text-primary);
    }}
    .pb-two-col {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(460px, 1fr));
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
      padding: 11px 14px;
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
      background: rgba(15, 23, 42, 0.85);
      color: #e2e8f0;
      font-family: var(--font-mono);
      font-size: 11.5px;
      overflow-x: auto;
    }}
    .pb-prompt-box {{
      background: var(--bg-card);
      border: 1.5px solid rgba(56, 189, 248, 0.35);
      border-radius: 14px;
      padding: 14px 16px;
      margin-bottom: 14px;
    }}
    .pb-checklist-box {{
      background: var(--bg-card);
      border: 1px solid rgba(16, 185, 129, 0.32);
      border-radius: 14px;
      padding: 14px 16px;
    }}
    .pb-check-row {{
      display: flex;
      align-items: flex-start;
      gap: 10px;
      font-size: 13.5px;
      line-height: 1.5;
      color: var(--text-primary);
      margin-bottom: 8px;
      cursor: pointer;
    }}
    .pb-check-row input[type="checkbox"] {{
      margin-top: 3px;
      width: 16px;
      height: 16px;
      accent-color: #10b981;
      cursor: pointer;
    }}
    .pb-a2ui-preview-box {{
      background: var(--bg-card);
      border: 1.5px solid rgba(56, 189, 248, 0.38);
      border-left: 5px solid #38bdf8;
      border-radius: 14px;
      padding: 14px 16px;
      margin-bottom: 14px;
    }}
    .pb-expected-md-box {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 16px 18px;
    }}
    .pb-md-h3 {{
      font-family: var(--font-display);
      font-size: 17px;
      font-weight: 800;
      margin: 0 0 10px;
      color: var(--text-primary);
    }}
    .pb-md-h4 {{
      font-family: var(--font-display);
      font-size: 14.5px;
      font-weight: 800;
      margin: 14px 0 8px;
      color: #38bdf8;
    }}
    .pb-md-quote {{
      margin: 0 0 12px;
      padding: 10px 14px;
      border-left: 4px solid #38bdf8;
      background: rgba(56, 189, 248, 0.08);
      border-radius: 8px;
      font-size: 13.5px;
      line-height: 1.58;
      color: var(--text-primary);
    }}
    .pb-md-p {{
      font-size: 13.5px;
      line-height: 1.58;
      margin: 0 0 8px;
    }}
    .pb-md-ul {{
      margin: 0 0 10px;
      padding-left: 18px;
      font-size: 13px;
      line-height: 1.55;
    }}
    .pb-md-table-wrap {{
      overflow-x: auto;
      margin: 8px 0 12px;
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
    }}
    .pb-md-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 12.5px;
    }}
    .pb-md-table th {{
      background: rgba(56, 189, 248, 0.12);
      color: #38bdf8;
      font-family: var(--font-mono);
      font-size: 11.5px;
      text-align: left;
      padding: 8px 10px;
      border-bottom: 1px solid var(--border-subtle);
    }}
    .pb-md-table td {{
      padding: 8px 10px;
      border-bottom: 1px solid var(--border-subtle);
      color: var(--text-primary);
    }}
    .pb-inline-code {{
      font-family: var(--font-mono);
      font-size: 12px;
      padding: 2px 6px;
      border-radius: 5px;
      background: rgba(148, 163, 184, 0.15);
      color: #38bdf8;
    }}
    .pb-cmd-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 8px;
    }}
    .pb-copy-btn {{
      font-family: var(--font-sans);
      font-size: 12.5px;
      font-weight: 700;
      padding: 8px 12px;
      border-radius: 10px;
      border: 1px solid var(--border-subtle);
      background: var(--bg-card);
      color: var(--text-primary);
      cursor: pointer;
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
    <div style="display:flex; align-items:center; gap:14px; flex-wrap:wrap;">
      <a href="index.html" style="text-decoration:none; color:var(--text-primary); font-family:var(--font-display); font-size:20px; font-weight:800;">
        &larr; Supply Chain Portal
      </a>
      <span class="pb-badge" style="color:#38bdf8; border-color:rgba(56,189,248,0.4);">🎬 60-Agent Manual Testing &amp; Expected Output Playbook</span>
    </div>
    <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
      <a href="supply_chain_101_interactive_academy.html" class="pb-filter-btn" style="text-decoration:none; background:rgba(16,185,129,0.16); color:#10b981; border-color:rgba(16,185,129,0.45);">🎓 Supply Chain 101 Academy (Learn From Zero)</a>
      <a href="periodic_table.html" class="pb-filter-btn" style="text-decoration:none;">Periodic Table</a>
      <a href="mind_map.html" class="pb-filter-btn" style="text-decoration:none;">Neural Mind Map</a>
      <button type="button" class="pb-filter-btn" onclick="document.documentElement.setAttribute('data-theme', document.documentElement.getAttribute('data-theme')==='light'?'dark':'light')">
        🌗 Theme
      </button>
    </div>
  </header>

  <main class="pb-container">
    <section class="pb-hero">
      <div style="display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap;">
        <div>
          <div style="font-family:var(--font-mono); font-size:12px; font-weight:800; color:#38bdf8; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">
            MANUAL VERIFICATION PLAYBOOK · INPUT PROMPT &rarr; EXACT EXPECTED OUTPUT &amp; A2UI GRAPHICS
          </div>
          <h1 style="font-family:var(--font-display); font-size:clamp(25px, 2.8vw, 36px); margin:0 0 8px;">
            Test Every Agent Manually &amp; Explain the Problem to Any Customer
          </h1>
          <p style="font-size:15.5px; color:var(--text-secondary); margin:0; max-width:1080px;">
            Every agent below shows: <strong>(1) Plain-English Customer Explanation</strong> (with all abbreviations spelled out), <strong>(2) The Exact Input Prompt &amp; Demo Data Values</strong>, <strong>(3) The Exact Output Table, Numbers, A2UI <code>VegaChart</code> &amp; Write-Back Receipt You Must Receive</strong>, and <strong>(4) A 5-Point Manual Verification Checklist</strong>.
          </p>
        </div>
        <a href="supply_chain_101_interactive_academy.html" style="text-decoration:none; padding:14px 22px; border-radius:16px; background:linear-gradient(135deg, #10b981, #0284c7); color:#ffffff; font-weight:800; font-size:15px; box-shadow:0 10px 24px rgba(16,185,129,0.25);">
          🎓 Open Supply Chain 101 Academy &rarr;
        </a>
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
        <button type="button" class="pb-filter-btn" onclick="filterPlaybook('cloud', this)">🟢 Cloud-Deployed (14)</button>
      </div>
      <input type="search" id="pbSearchInput" class="pb-search-input" placeholder="🔍 Search agent name, SKU, term, or persona…" oninput="filterPlaybookSearch()" />
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
    function saveCheckState(key, checked) {{
      try {{ localStorage.setItem('pb_chk_' + key, checked ? '1' : '0'); }} catch(e) {{}}
    }}
    function loadCheckStates() {{
      try {{
        document.querySelectorAll('input[type="checkbox"][id^="chk_"]').forEach(el => {{
          const key = el.id.replace(/^chk_/, '');
          if (localStorage.getItem('pb_chk_' + key) === '1') el.checked = true;
        }});
      }} catch(e) {{}}
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
    window.addEventListener('DOMContentLoaded', loadCheckStates);
  </script>
</body>
</html>
"""
    (ROOT / "agent_testing_and_video_playbook.html").write_text(playbook_html, encoding="utf-8")
    for sub in ["docs", "zipline_dist", "dist/itc_limited"]:
        d = ROOT / sub
        if d.exists():
            (d / "agent_testing_and_video_playbook.html").write_text(playbook_html, encoding="utf-8")
    print("Updated agent_testing_and_video_playbook.html with full expected outputs and manual checklists")


if __name__ == "__main__":
    build_upgraded_playbook()

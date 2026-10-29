#!/usr/bin/env python3
"""Rebuilds BOTH:
1. `agent_testing_and_video_playbook.html` — One-by-One Linear, Spacious, Tabular, Button-Wise Google Design Language Playbook:
   - Bright Google Material Design 3 theme (#FFFFFF cards on #F8F9FA background, Google Blue #1A73E8, Green #1E8E3E, Yellow #F9AB00, Red #D93025).
   - Test ONE AGENT AT A TIME ("Agent 1 of 60") with Pillar Buttons, Agent Pill Buttons, Search/Dropdown, and Previous/Next Agent buttons.
   - Linear, spacious, single-column flow with clean HTML tables (no raw JSON dumps by default, no cramped side-by-side columns):
     * Section 1: Plain-English Overview Table (Problem | What the Agent Does | Business Result — all abbreviations spelled out).
     * Section 2: Spacious Visual 4-Step Flow Diagram (Bright Google SVG).
     * Section 3: Input Prompt (Big 1-click Copy Box) + Clean Tabular Demo Input Data (real HTML tables of the fixture rows).
     * Section 4: Exact Expected Output (Bright Google SVG Chart + Clean Expected Output Table + Clean Action Receipt Table).
     * Section 5: 5-Row Tabular Manual Verification Checklist + "Mark All Verified & Next Agent ->" button.

2. `supply_chain_101_interactive_academy.html` — Bright Google-Colored, Linear, Spacious, Button-Wise & Tabular Supply Chain 101 Academy:
   - Chapter 1: What Is a Supply Chain? (Bright Google SVG 6-Stage Relay Race + Click 1 Stage at a Time + Clean 3-Flows Table + Clean 4-Software-Systems Table).
   - Chapter 2: Bullwhip Simulator & 4 Core Visual Diagrams (Button-Wise: click 1 diagram at a time with bright SVG + simple comparison table).
   - Chapter 3: 4 Core Supply Chain Workflows (Button-Wise + Stepper + Clean Before-vs-After Comparison Table).
   - Chapter 4: All 56 Supply Chain Terms Spelled Out (Switch between One-by-One Big Flashcard Mode & Clean Tabular Dictionary Mode).
   - Chapter 5: Customer Problem -> AI Agent Table (20 Scenarios with Pillar Filter Buttons in a spacious table).
   - Chapter 6: One-by-One Practice Quiz (Question 1 of 12, one question at a time).
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from test_agent_demo import extract_normalized_scenario, load_catalog
from build_manual_verification_playbook_and_supply_chain_academy import (
    PILLAR_ORDER,
    clean_agent_name,
    describe_vega_spec,
    expand_acronyms_once,
    get_re_id,
    md_to_simple_html,
)
from build_supply_chain_101_academy import (
    CUSTOMER_DECODER,
    FLASHCARDS,
    QUIZ_QUESTIONS,
)

WORKFLOW_SIMULATORS = {
    "sop": {
        "title": "1 · Monthly S&OP (Sales & Operations Planning — 5 Steps)",
        "subtitle": "How a company aligns Sales forecasts, Factory capacity, and Finance budgets every month:",
        "steps": [
            {"badge": "Step 1 · Data Gathering", "title": "Pull Past Sales, POS Checkout Scans & Weather", "plain": "Collect what stores actually sold last month plus upcoming promotions and weather.", "manual": "Analysts spend 5 days downloading CSVs and fixing broken Excel formulas.", "ai": "Demand Sensing Agent pulls live POS scans & weather automatically in seconds."},
            {"badge": "Step 2 · Demand Plan", "title": "Agree on What Customers Will Buy", "plain": "Create a statistical baseline forecast and check if salesperson overrides help or hurt (FVA).", "manual": "Sales reps pad forecasts by +20% 'just in case', creating negative Forecast Value Added.", "ai": "Flags biased manual overrides and harmonies retailer CPFR forecasts."},
            {"badge": "Step 3 · Supply & Factory Check", "title": "Check If Factories & Suppliers Can Build It", "plain": "Compare the demand forecast against real factory line hours, machine OEE, and supplier stock.", "manual": "Planners discover 2 weeks too late that a line is booked or a supplier is short.", "ai": "Finite Scheduler & Tier-N Sentinel flag capacity and component bottlenecks early."},
            {"badge": "Step 4 · Pre-S&OP Trade-Offs", "title": "Solve Gaps (Overtime vs. Air Freight vs. Margin)", "plain": "When demand beats capacity, simulate options: run weekend overtime, use co-packers, or shift stock.", "manual": "Teams argue in meetings with no live math on profit margin vs. OTIF service impact.", "ai": "S&OP Scenario Weaver simulates 3 cost/margin/service options in 10 seconds."},
            {"badge": "Step 5 · Executive Sign-Off", "title": "Lock the One-Number Plan into ERP", "plain": "Leadership approves the final plan and publishes firm production & procurement targets.", "manual": "Manual re-keying into ERP takes days; plan is stale before execution starts.", "ai": "1-click governed write-back locks the consensus plan across ERP, MES, and WMS."},
        ],
    },
    "match3": {
        "title": "2 · Paying Suppliers: The 3-Way Invoice Match (4 Steps)",
        "subtitle": "How Procurement & Accounts Payable make sure the company never overpays a supplier invoice:",
        "steps": [
            {"badge": "Step 1 · Document #1 (PO)", "title": "Check the Original Purchase Order (PO)", "plain": "Look up what price and quantity our buyer officially agreed to pay (e.g., 1,000 units @ $10 = $10,000).", "manual": "AP clerk manually searches SAP for the PO number typed on a PDF invoice.", "ai": "Three-Way Match Agent extracts the PO line items automatically."},
            {"badge": "Step 2 · Document #2 (GRN)", "title": "Check the Warehouse Goods Receipt Note (GRN)", "plain": "Check what the receiving dock actually unloaded and scanned (e.g., only 960 units arrived; 40 were missing).", "manual": "Clerk emails the warehouse manager waiting 3 days to confirm dock count.", "ai": "Instantly cross-checks WMS dock barcode scans (GRN) against the PO."},
            {"badge": "Step 3 · Document #3 (Invoice)", "title": "Compare Supplier Invoice Against PO & GRN", "plain": "The vendor billed $10,500 (1,000 units @ $10.50) — both unit price and quantity are wrong!", "manual": "Invoice sits blocked in a queue for weeks while teams argue over email.", "ai": "Pinpoints the exact $500 price variance + $400 short-shipment discrepancy."},
            {"badge": "Step 4 · Auto-Debit & Release", "title": "Issue Debit Memo & Release Exact Approved Payment", "plain": "Block the $900 overcharge, send an automated debit memo with dock proof, and pay the valid $9,600.", "manual": "Late payment causes supplier credit hold or accidental overpayment.", "ai": "Issues signed debit memo and releases the exact verified amount on time."},
        ],
    },
    "wms_flow": {
        "title": "3 · Inside the Warehouse: Inbound Dock to Outbound Truck (5 Steps)",
        "subtitle": "How pallets move through the 4 walls of a Distribution Center (WMS):",
        "steps": [
            {"badge": "Step 1 · Yard & Dock Arrival", "title": "Assign Incoming Truck to the Best Dock Door", "plain": "A supplier truck arrives at the gate and needs an open unloading door.", "manual": "Trucks wait 3 hours in line, triggering $150/hr carrier detention penalties.", "ai": "Yard & Dock Sequencer assigns the optimal door dynamically from live GPS ETA."},
            {"badge": "Step 2 · Dock-to-Stock & QA", "title": "Scan Pallets (GRN) & Check Quality / Cold-Chain", "plain": "Unload pallets, scan barcodes, and verify temperature logs before releasing stock for sale.", "manual": "Pallets sit on the dock floor for 28 hours waiting for manual clipboards.", "ai": "Dock-to-Stock & Cold-Chain Auditors clear good pallets in under 2 hours."},
            {"badge": "Step 3 · Dynamic Slotting", "title": "Put Fast-Selling Items in Golden-Zone Bins", "plain": "Store high-velocity SKUs at waist height near shipping doors to minimize forklift travel.", "manual": "Static bin maps leave workers walking 8 extra miles a day in congested aisles.", "ai": "Warehouse Slotting Optimizer re-slots fast movers before peak waves."},
            {"badge": "Step 4 · Wave Picking (FEFO)", "title": "Batch Customer Orders & Pick Earliest-Expiring Stock", "plain": "Release picking waves to handheld scanners enforcing First-Expired, First-Out (FEFO).", "manual": "One zone gets swamped while packing stations sit idle waiting for carts.", "ai": "Wave Fulfillment Copilot balances zone labor and enforces strict FEFO."},
            {"badge": "Step 5 · 3D LIFO Truck Loading", "title": "Pack the Outbound 53-Foot Trailer in Stop Order", "plain": "Stack pallets safely by crush resistance, axle weight, and Last-In First-Out (LIFO) delivery sequence.", "manual": "Trailers leave 25% empty or drivers have to dig behind pallets at Stop #1.", "ai": "3D Load Consolidation Studio builds axle-legal LIFO load blueprints."},
        ],
    },
    "otif_flow": {
        "title": "4 · Customer Order to On-Time In-Full (OTIF) Delivery (5 Steps)",
        "subtitle": "How a customer order is promised, routed, tracked, and protected from retailer fines:",
        "steps": [
            {"badge": "Step 1 · Order Promising (ATP)", "title": "Promise an Accurate Delivery Date & Protect VIP Stock", "plain": "Check real-time Available-to-Promise (ATP) stock and reserve inventory for high-priority orders.", "manual": "First-come-first-served rules let low-margin orders drain VIP stock.", "ai": "ATP Order Promising Agent allocates stock from the best node in <50ms."},
            {"badge": "Step 2 · Mode & Carrier Selection", "title": "Choose Full Truckload (FTL), Rail, or Expedite", "plain": "Pick the lowest-cost transport mode that still meets the customer's exact delivery window.", "manual": "Planners book expensive last-minute air freight or LTL out of habit.", "ai": "Multimodal Mode-Shift & FleetFlow optimize multi-stop routes."},
            {"badge": "Step 3 · In-Transit Tracking", "title": "Watch Live GPS, Weather & Driver Hours (ELD/HOS)", "plain": "Track the truck along the highway and predict if weather or driver hours will cause a delay.", "manual": "Nobody knows a shipment is stuck until the customer calls angry.", "ai": "Freight Control Tower & OTIF Shield flag at-risk loads 48 hours early."},
            {"badge": "Step 4 · Delivery & ePOD", "title": "Arrive Inside Appointment Window & Capture ePOD", "plain": "Deliver 100% of cases on time and capture timestamped GPS + Electronic Proof of Delivery (ePOD).", "manual": "Paper delivery slips get lost, leaving no proof when retailers claim late arrival.", "ai": "Automatically archives signed ePOD, BOL, and geofence arrival timestamps."},
            {"badge": "Step 5 · Freight Audit & Claims", "title": "Audit Carrier Freight Bill & Dispute Unfair Fines", "plain": "Verify carrier freight rates against contract tables and auto-dispute invalid retailer OTIF fines.", "manual": "Companies lose 3% revenue to unchallenged chargebacks and billing errors.", "ai": "Freight Bill Audit & OTIF Shield recover overcharges automatically."},
        ],
    },
}


# Google Brand Colors mapped to the 6 Pillars
GOOGLE_PILLAR_META = [
    ("demand_sop", "01 · Planning & Forecasting", "#1A73E8", "#E8F0FE"),          # Google Blue
    ("sourcing_procurement", "02 · Sourcing & Suppliers", "#E8710A", "#FEF7E0"),  # Google Amber/Orange
    ("manufacturing_prod", "03 · Factory & Manufacturing", "#9334E6", "#F3E8FD"), # Google Purple
    ("logistics_fleet", "04 · Logistics & Trucking", "#007B83", "#E4F7FB"),       # Google Teal
    ("inventory_warehouse", "05 · Inventory & Warehouse", "#1E8E3E", "#E6F4EA"),  # Google Green
    ("circular_enable", "06 · Control Tower, Returns & ESG", "#D93025", "#FCE8E6"), # Google Red
]


def _num(val: Any) -> float | None:
    if isinstance(val, (int, float)) and not isinstance(val, bool):
        return float(val)
    if isinstance(val, str):
        s = val.replace(",", "").replace("$", "").replace("%", "").strip()
        try:
            return float(s)
        except ValueError:
            return None
    return None


def render_bright_google_chart_svg(vega: dict, accent: str = "#1A73E8") -> str:
    """Renders a clean, bright, spacious Google-styled SVG chart from Vega-Lite data.values."""
    values = vega.get("data", {}).get("values", [])
    mark_raw = vega.get("mark")
    if isinstance(mark_raw, dict):
        mark_type = str(mark_raw.get("type", "bar")).lower()
    elif isinstance(mark_raw, str):
        mark_type = mark_raw.lower()
    elif "layer" in vega:
        mark_type = "line"
    else:
        mark_type = "bar"

    rows = [r for r in values if isinstance(r, dict)][:6]
    if not rows:
        rows = [
            {"Metric": "Before AI", "Value": 62},
            {"Metric": "With AI Agent", "Value": 94},
            {"Metric": "Target SLA", "Value": 90},
        ]

    keys = list(rows[0].keys())
    label_key = keys[0]
    num_key = None
    for k in keys:
        if _num(rows[0].get(k)) is not None and k != label_key:
            num_key = k
            break
    if num_key is None:
        for k in keys:
            if _num(rows[0].get(k)) is not None:
                num_key = k
                break

    points: list[tuple[str, float]] = []
    for idx, r in enumerate(rows):
        lbl = str(r.get(label_key, f"Item {idx+1}"))
        if len(lbl) > 18:
            lbl = lbl[:17] + "…"
        v = _num(r.get(num_key)) if num_key else None
        if v is None:
            v = float((idx + 1) * 20)
        points.append((lbl, v))

    max_v = max([abs(p[1]) for p in points] + [1.0])
    google_palette = ["#4285F4", "#34A853", "#FBBC04", "#EA4335", "#9334E6", "#00ACC1"]

    if "line" in mark_type or "area" in mark_type:
        w, h = 760, 220
        left, right, top, bottom = 64, 720, 36, 174
        n = max(len(points), 2)
        step_x = (right - left) / max(n - 1, 1)
        coords = []
        dots = []
        for idx, (lbl, val) in enumerate(points):
            x = left + idx * step_x
            y = bottom - (abs(val) / max_v) * (bottom - top)
            coords.append(f"{x:.1f},{y:.1f}")
            dots.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{accent}" stroke="#FFFFFF" stroke-width="2.5"/>'
                f'<text x="{x:.1f}" y="{max(y - 12, 18):.1f}" text-anchor="middle" fill="#202124" font-size="13" font-weight="700" font-family="Google Sans, Inter, sans-serif">{val:,.1f}</text>'
                f'<text x="{x:.1f}" y="202" text-anchor="middle" fill="#5F6368" font-size="12.5" font-weight="600" font-family="Google Sans, Inter, sans-serif">{html.escape(lbl)}</text>'
            )
        poly = " ".join(coords)
        area = f"{left},{bottom} " + poly + f" {left + (n-1)*step_x:.1f},{bottom}"
        return f"""
        <svg viewBox="0 0 {w} {h}" style="width:100%; max-width:760px; height:auto; display:block; background:#FFFFFF; border-radius:14px; border:1px solid #DADCE0;">
          <line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#DADCE0" stroke-width="1.5"/>
          <line x1="{left}" y1="{(top+bottom)/2:.1f}" x2="{right}" y2="{(top+bottom)/2:.1f}" stroke="#F1F3F4" stroke-width="1.5" stroke-dasharray="5 5"/>
          <polygon points="{area}" fill="{accent}" fill-opacity="0.12"/>
          <polyline fill="none" stroke="{accent}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" points="{poly}"/>
          {''.join(dots)}
        </svg>
        """

    # Clean Spacious Google Bar Chart
    w, h = 760, 220
    left, right, top, bottom = 64, 720, 36, 174
    n = len(points)
    slot_w = (right - left) / max(n, 1)
    bar_w = min(68.0, slot_w * 0.55)
    bars = []
    for idx, (lbl, val) in enumerate(points):
        bh = max(12.0, (abs(val) / max_v) * (bottom - top))
        x = left + idx * slot_w + (slot_w - bar_w) / 2
        y = bottom - bh
        c = google_palette[idx % len(google_palette)]
        bars.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" rx="8" fill="{c}"/>'
            f'<text x="{x + bar_w/2:.1f}" y="{max(y - 10, 18):.1f}" text-anchor="middle" fill="#202124" font-size="13" font-weight="700" font-family="Google Sans, Inter, sans-serif">{val:,.1f}</text>'
            f'<text x="{x + bar_w/2:.1f}" y="202" text-anchor="middle" fill="#5F6368" font-size="12.5" font-weight="600" font-family="Google Sans, Inter, sans-serif">{html.escape(lbl)}</text>'
        )
    return f"""
    <svg viewBox="0 0 {w} {h}" style="width:100%; max-width:760px; height:auto; display:block; background:#FFFFFF; border-radius:14px; border:1px solid #DADCE0;">
      <line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#DADCE0" stroke-width="1.5"/>
      <line x1="{left}" y1="{(top+bottom)/2:.1f}" x2="{right}" y2="{(top+bottom)/2:.1f}" stroke="#F1F3F4" stroke-width="1.5" stroke-dasharray="5 5"/>
      {''.join(bars)}
    </svg>
    """


def render_bright_agent_flow_svg(
    t1: str,
    t2: str,
    r1: str,
    w1: str,
    chart_title: str,
) -> str:
    """Renders a spacious, bright Google-colored 4-step SVG diagram for an agent."""
    return f"""
    <svg viewBox="0 0 980 136" style="width:100%; height:auto; display:block; background:#FFFFFF; border-radius:16px; border:1px solid #DADCE0; padding:6px;">
      <!-- Step 1: Google Blue -->
      <rect x="14" y="16" width="210" height="104" rx="14" fill="#E8F0FE" stroke="#4285F4" stroke-width="2"/>
      <text x="119" y="40" text-anchor="middle" fill="#1A73E8" font-size="11.5" font-weight="800" font-family="Google Sans, Inter, sans-serif">STEP 1 · DEMO DATA READ</text>
      <text x="119" y="66" text-anchor="middle" fill="#202124" font-size="13" font-weight="700" font-family="JetBrains Mono, monospace">🗄️ {html.escape(t1[:20])}</text>
      <text x="119" y="88" text-anchor="middle" fill="#3C4043" font-size="12.5" font-weight="600" font-family="JetBrains Mono, monospace">🗄️ {html.escape(t2[:20])}</text>
      <text x="119" y="108" text-anchor="middle" fill="#5F6368" font-size="11.5" font-family="Inter, sans-serif">Live Input Tables</text>

      <!-- Arrow 1->2 -->
      <line x1="224" y1="68" x2="256" y2="68" stroke="#4285F4" stroke-width="2.5"/>
      <polygon points="256,62 268,68 256,74" fill="#4285F4"/>

      <!-- Step 2: Google Yellow/Amber -->
      <rect x="270" y="16" width="210" height="104" rx="14" fill="#FEF7E0" stroke="#FBBC04" stroke-width="2"/>
      <text x="375" y="40" text-anchor="middle" fill="#B06000" font-size="11.5" font-weight="800" font-family="Google Sans, Inter, sans-serif">STEP 2 · CHECK &amp; DETECT</text>
      <text x="375" y="66" text-anchor="middle" fill="#202124" font-size="13" font-weight="700" font-family="JetBrains Mono, monospace">🔎 {html.escape(r1[:21])}</text>
      <text x="375" y="88" text-anchor="middle" fill="#3C4043" font-size="12.5" font-weight="600" font-family="Inter, sans-serif">Finds gap or risk breach</text>
      <text x="375" y="108" text-anchor="middle" fill="#5F6368" font-size="11.5" font-family="Inter, sans-serif">Reads all table rows</text>

      <!-- Arrow 2->3 -->
      <line x1="480" y1="68" x2="512" y2="68" stroke="#FBBC04" stroke-width="2.5"/>
      <polygon points="512,62 524,68 512,74" fill="#FBBC04"/>

      <!-- Step 3: Google Red / Purple -->
      <rect x="526" y="16" width="205" height="104" rx="14" fill="#FCE8E6" stroke="#EA4335" stroke-width="2"/>
      <text x="628" y="40" text-anchor="middle" fill="#C5221F" font-size="11.5" font-weight="800" font-family="Google Sans, Inter, sans-serif">STEP 3 · AI &amp; MATH SOLVER</text>
      <text x="628" y="66" text-anchor="middle" fill="#202124" font-size="13.5" font-weight="800" font-family="Google Sans, Inter, sans-serif">✦ Gemini 3.8 / 3.1 Pro</text>
      <text x="628" y="88" text-anchor="middle" fill="#3C4043" font-size="12.5" font-weight="600" font-family="Inter, sans-serif">Calculates best option</text>
      <text x="628" y="108" text-anchor="middle" fill="#5F6368" font-size="11.5" font-family="Inter, sans-serif">Checks safety gate</text>

      <!-- Arrow 3->4 -->
      <line x1="731" y1="68" x2="763" y2="68" stroke="#34A853" stroke-width="2.5"/>
      <polygon points="763,62 775,68 763,74" fill="#34A853"/>

      <!-- Step 4: Google Green -->
      <rect x="777" y="16" width="189" height="104" rx="14" fill="#E6F4EA" stroke="#34A853" stroke-width="2"/>
      <text x="871" y="40" text-anchor="middle" fill="#137333" font-size="11.5" font-weight="800" font-family="Google Sans, Inter, sans-serif">STEP 4 · RESULT &amp; ACTION</text>
      <text x="871" y="66" text-anchor="middle" fill="#202124" font-size="12.5" font-weight="700" font-family="Inter, sans-serif">📊 {html.escape(chart_title[:20])}</text>
      <text x="871" y="88" text-anchor="middle" fill="#137333" font-size="12.5" font-weight="700" font-family="JetBrains Mono, monospace">⚡ {html.escape(w1[:19])}</text>
      <text x="871" y="108" text-anchor="middle" fill="#5F6368" font-size="11.5" font-family="Inter, sans-serif">Table + Signed Receipt</text>
    </svg>
    """


def build_tabular_input_tables_html(tables: list[dict]) -> str:
    """Renders each fixture table as a clean, readable HTML table instead of raw JSON code."""
    if not tables:
        return "<p>No fixture tables required.</p>"
    blocks = []
    for idx, t in enumerate(tables):
        tname = t.get("table_name", f"table_{idx+1}")
        rows = t.get("rows", [])
        if not rows or not isinstance(rows[0], dict):
            continue
        cols = list(rows[0].keys())[:6]
        th_html = "".join(f"<th>{html.escape(str(c))}</th>" for c in cols)
        tr_html = []
        for r in rows[:3]:
            tds = "".join(f"<td>{html.escape(str(r.get(c, '')))}</td>" for c in cols)
            tr_html.append(f"<tr>{tds}</tr>")
        blocks.append(f"""
        <div class="g-subcard" style="margin-bottom:16px;">
          <div style="display:flex; align-items:center; justify-content:space-between; gap:10px; flex-wrap:wrap; margin-bottom:10px;">
            <span style="font-weight:700; font-size:15px; color:#1A73E8;">🗄️ Table {idx+1}: <code>{html.escape(tname)}.json</code></span>
            <span class="g-chip" style="background:#E8F0FE; color:#1A73E8;">{len(rows)} demo rows · showing top {min(len(rows), 3)}</span>
          </div>
          <div class="g-table-wrap">
            <table class="g-table">
              <thead><tr>{th_html}</tr></thead>
              <tbody>{''.join(tr_html)}</tbody>
            </table>
          </div>
        </div>
        """)
    return "\n".join(blocks)


def build_tabular_receipt_html(actions_list: list[dict]) -> str:
    """Renders the expected write-back receipt as a clean, human-readable HTML table."""
    if not actions_list or not isinstance(actions_list[0], dict):
        return "<p>Action committed with signed receipt.</p>"
    act = actions_list[0]
    rows_html = []
    for k, v in act.items():
        val_str = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)
        rows_html.append(f"<tr><th style='width:240px;'><code>{html.escape(str(k))}</code></th><td>{html.escape(val_str)}</td></tr>")
    return f"""
    <div class="g-table-wrap">
      <table class="g-table">
        <tbody>
          {''.join(rows_html)}
        </tbody>
      </table>
    </div>
    """


def build_google_linear_playbook() -> None:
    cat = load_catalog()
    agents_dict = cat.get("agents", {})
    personas_dict = cat.get("personas", {})

    by_dept: dict[str, list[dict]] = {pid: [] for pid, _, _, _ in GOOGLE_PILLAR_META}
    for ag in agents_dict.values():
        did = ag.get("deptId", "demand_sop")
        by_dept.setdefault(did, []).append(ag)

    all_agents_payload = []
    total_idx = 0

    for dept_id, pillar_title, pillar_color, pillar_bg in GOOGLE_PILLAR_META:
        for ag in by_dept.get(dept_id, []):
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

            norm = extract_normalized_scenario(ag_id)
            demo_prompt = norm["query"]
            vega_info = describe_vega_spec(norm["vega_spec"])
            actions_list = norm["actions"]
            expected_md = norm["markdown"]

            prob_explained = expand_acronyms_once(ag.get("problem", ""))
            sol_explained = expand_acronyms_once(ag.get("solution", ""))
            out_explained = expand_acronyms_once(ag.get("outcome", ""))

            t1 = tables[0].get("table_name", "fixture_table_1") if len(tables) > 0 else "erp_live_feed"
            t2 = tables[1].get("table_name", "fixture_table_2") if len(tables) > 1 else "iot_twin_state"
            r1 = read_tools[0] if read_tools else "query_records"
            w1 = write_tools[0] if write_tools else "action_commit"

            all_agents_payload.append({
                "num": total_idx,
                "id": ag_id,
                "name": c_name,
                "deptId": dept_id,
                "pillarTitle": pillar_title,
                "pillarColor": pillar_color,
                "pillarBg": pillar_bg,
                "subPillar": sub_pillar,
                "persona": persona_name,
                "roiBadge": ag.get("badge", "Verified ROI"),
                "cloudRe": re_id.split("/")[-1] if re_id else "",
                "problem": prob_explained,
                "solution": sol_explained,
                "outcome": out_explained,
                "prompt": demo_prompt,
                "readTools": read_tools,
                "writeTools": write_tools,
                "tableCount": len(tables),
                "flowSvg": render_bright_agent_flow_svg(t1, t2, r1, w1, vega_info["title"]),
                "inputTablesHtml": build_tabular_input_tables_html(tables),
                "chartTitle": vega_info["title"],
                "chartType": vega_info["mark_type"],
                "chartSeries": vega_info["sample_points"],
                "chartSvg": render_bright_google_chart_svg(norm["vega_spec"], pillar_color),
                "expectedMdHtml": md_to_simple_html(expected_md),
                "receiptTableHtml": build_tabular_receipt_html(actions_list),
                "cmdRun": f"python3 scripts/test_agent_demo.py {ag_id}",
                "cmdGate": f"python3 scripts/test_agent_demo.py {ag_id} --test-guardrail",
            })

    pillar_buttons_html = []
    for idx, (pid, ptitle, pcol, pbg) in enumerate(GOOGLE_PILLAR_META):
        active_cls = "active" if idx == 0 else ""
        pillar_buttons_html.append(
            f'<button type="button" class="g-pillar-btn {active_cls}" data-dept="{pid}" '
            f'style="--pcol:{pcol}; --pbg:{pbg};" onclick="selectPillar(\'{pid}\')">'
            f'{html.escape(ptitle)} <span class="g-count-pill">10</span></button>'
        )

    agents_json = json.dumps(all_agents_payload, ensure_ascii=False)

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>One-by-One Agent Testing &amp; Video Playbook — Google Clean Edition</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Google+Sans+Display:wght@500;700&family=Google+Sans:wght@400;500;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --g-blue: #1A73E8;
      --g-blue-bg: #E8F0FE;
      --g-red: #D93025;
      --g-red-bg: #FCE8E6;
      --g-yellow: #F9AB00;
      --g-yellow-bg: #FEF7E0;
      --g-green: #1E8E3E;
      --g-green-bg: #E6F4EA;
      --bg-page: #F8F9FA;
      --bg-card: #FFFFFF;
      --text-main: #202124;
      --text-sub: #5F6368;
      --border-light: #DADCE0;
      --font-display: 'Google Sans Display', 'Google Sans', 'Inter', sans-serif;
      --font-sans: 'Google Sans', 'Inter', -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      background: var(--bg-page);
      color: var(--text-main);
      font-family: var(--font-sans);
      font-size: 17px;
      line-height: 1.7;
    }}
    /* Google 4-Color Top Bar */
    .g-color-strip {{
      height: 5px;
      background: linear-gradient(90deg, #4285F4 0% 25%, #EA4335 25% 50%, #FBBC04 50% 75%, #34A853 75% 100%);
      position: sticky;
      top: 0;
      z-index: 200;
    }}
    .g-header {{
      position: sticky;
      top: 5px;
      z-index: 190;
      background: rgba(255, 255, 255, 0.96);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-light);
      padding: 14px 32px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }}
    .g-container {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 32px 24px 96px;
    }}
    .g-btn {{
      font-family: var(--font-sans);
      font-size: 15px;
      font-weight: 600;
      padding: 10px 20px;
      border-radius: 999px;
      border: 1.5px solid var(--border-light);
      background: #FFFFFF;
      color: var(--text-main);
      cursor: pointer;
      transition: all 0.18s ease;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }}
    .g-btn:hover {{
      border-color: var(--g-blue);
      color: var(--g-blue);
      background: var(--g-blue-bg);
    }}
    .g-btn-primary {{
      background: var(--g-blue);
      color: #FFFFFF;
      border-color: var(--g-blue);
    }}
    .g-btn-primary:hover {{
      background: #1557B0;
      color: #FFFFFF;
    }}
    .g-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-light);
      border-radius: 20px;
      padding: 32px 36px;
      margin-bottom: 28px;
      box-shadow: 0 2px 10px rgba(60, 64, 67, 0.06);
    }}
    .g-subcard {{
      background: #F8F9FA;
      border: 1px solid var(--border-light);
      border-radius: 16px;
      padding: 20px 24px;
    }}
    .g-step-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 6px 14px;
      border-radius: 999px;
      margin-bottom: 12px;
    }}
    .g-chip {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 13.5px;
      font-weight: 600;
      padding: 5px 14px;
      border-radius: 999px;
      border: 1px solid transparent;
    }}
    /* Step 1: Pillar Selector Buttons */
    .g-pillar-bar {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }}
    @media (max-width: 820px) {{
      .g-pillar-bar {{ grid-template-columns: 1fr; }}
    }}
    .g-pillar-btn {{
      font-family: var(--font-sans);
      font-size: 15px;
      font-weight: 700;
      padding: 14px 18px;
      border-radius: 14px;
      border: 2px solid var(--border-light);
      background: #FFFFFF;
      color: var(--text-main);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: all 0.16s ease;
      text-align: left;
    }}
    .g-pillar-btn:hover {{
      border-color: var(--pcol);
      background: var(--pbg);
    }}
    .g-pillar-btn.active {{
      border-color: var(--pcol);
      background: var(--pbg);
      color: var(--pcol);
      box-shadow: 0 3px 10px rgba(0,0,0,0.06);
    }}
    .g-count-pill {{
      font-size: 12.5px;
      padding: 2px 10px;
      border-radius: 999px;
      background: rgba(0,0,0,0.07);
    }}
    /* Step 2: 10 Agent Buttons inside selected Pillar */
    .g-agent-pills {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }}
    @media (max-width: 720px) {{
      .g-agent-pills {{ grid-template-columns: 1fr; }}
    }}
    .g-agent-pill {{
      font-family: var(--font-sans);
      font-size: 15px;
      font-weight: 600;
      padding: 12px 16px;
      border-radius: 12px;
      border: 1.5px solid var(--border-light);
      background: #FFFFFF;
      color: var(--text-main);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      text-align: left;
      transition: all 0.15s ease;
    }}
    .g-agent-pill:hover {{
      border-color: var(--g-blue);
      background: var(--g-blue-bg);
    }}
    .g-agent-pill.active {{
      background: var(--g-blue);
      color: #FFFFFF;
      border-color: var(--g-blue);
      font-weight: 700;
    }}
    /* Spacious Google Tables */
    .g-table-wrap {{
      overflow-x: auto;
      border-radius: 14px;
      border: 1px solid var(--border-light);
      background: #FFFFFF;
    }}
    .g-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 16px;
    }}
    .g-table th, .g-table td {{
      padding: 16px 20px;
      text-align: left;
      border-bottom: 1px solid #E8EAED;
      vertical-align: top;
      line-height: 1.65;
    }}
    .g-table th {{
      background: #F1F3F4;
      color: #202124;
      font-weight: 700;
      font-size: 14px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .g-table tr:last-child td, .g-table tr:last-child th {{
      border-bottom: none;
    }}
    .g-table tr:hover td {{
      background: #F8FAFD;
    }}
    /* Rendered Expected Markdown Table overrides */
    .pb-table-wrap {{
      overflow-x: auto;
      margin: 14px 0;
      border-radius: 12px;
      border: 1px solid var(--border-light);
    }}
    .pb-md-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 15.5px;
      background: #FFFFFF;
    }}
    .pb-md-table th, .pb-md-table td {{
      padding: 14px 18px;
      border-bottom: 1px solid #E8EAED;
      text-align: left;
    }}
    .pb-md-table th {{
      background: #E8F0FE;
      color: #1A73E8;
      font-weight: 700;
    }}
    .pb-md-h3, .pb-md-h4 {{
      margin: 16px 0 8px;
      color: #202124;
      font-family: var(--font-display);
    }}
    .pb-md-p, .pb-md-ul {{
      margin: 8px 0;
      color: #3C4043;
      font-size: 16px;
    }}
    .pb-md-quote {{
      margin: 12px 0;
      padding: 12px 18px;
      background: #E6F4EA;
      border-left: 4px solid #1E8E3E;
      border-radius: 8px;
      color: #137333;
      font-weight: 600;
    }}
    code {{
      font-family: var(--font-mono);
      font-size: 14px;
      background: #F1F3F4;
      color: #1A73E8;
      padding: 2px 7px;
      border-radius: 6px;
    }}
    .g-check-box {{
      width: 22px;
      height: 22px;
      accent-color: var(--g-green);
      cursor: pointer;
    }}
  </style>
</head>
<body>
  <div class="g-color-strip"></div>
  <header class="g-header">
    <div style="display:flex; align-items:center; gap:14px; flex-wrap:wrap;">
      <a href="index.html" class="g-btn">&larr; Main Portal</a>
      <span style="font-family:var(--font-display); font-size:20px; font-weight:700; color:#202124;">
        📋 One-by-One Agent Testing &amp; Video Playbook
      </span>
    </div>
    <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
      <span id="globalProgressBadge" class="g-chip" style="background:var(--g-green-bg); color:var(--g-green); font-weight:700;">
        ✓ 0 / 60 Agents Tested
      </span>
      <a href="supply_chain_101_interactive_academy.html" class="g-btn" style="border-color:var(--g-green); color:var(--g-green);">
        🎓 Open Supply Chain 101 Guide &rarr;
      </a>
    </div>
  </header>

  <main class="g-container">
    <!-- TOP SELECTOR CARD: PICK PILLAR -> PICK 1 AGENT -->
    <section class="g-card" style="padding:28px 32px;">
      <div style="display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap; margin-bottom:16px;">
        <div>
          <span class="g-step-badge" style="background:var(--g-blue-bg); color:var(--g-blue); margin-bottom:6px;">
            STEP 1 · PICK A PILLAR, THEN CLICK ONE AGENT TO TEST
          </span>
          <h1 style="font-family:var(--font-display); font-size:28px; margin:0;">
            Test Each Agent One-by-One (Simple, Linear &amp; Tabular)
          </h1>
        </div>
        <!-- Quick Jump Dropdown & Search -->
        <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
          <select id="agentQuickSelect" onchange="selectAgentByIndex(Number(this.value))" style="font-family:var(--font-sans); font-size:15px; padding:10px 14px; border-radius:12px; border:1.5px solid var(--border-light); background:#FFFFFF; color:#202124; font-weight:600; cursor:pointer;">
          </select>
        </div>
      </div>

      <!-- 6 Google-Colored Pillar Buttons -->
      <div class="g-pillar-bar" id="pillarButtonsBar">
        {''.join(pillar_buttons_html)}
      </div>

      <!-- 10 Agent Pill Buttons in Current Pillar -->
      <div style="margin-top:16px;">
        <div style="font-size:13.5px; font-weight:700; color:var(--text-sub); text-transform:uppercase; margin-bottom:10px;">
          Click Any Agent in This Pillar (10 Agents):
        </div>
        <div class="g-agent-pills" id="agentPillsContainer"></div>
      </div>
    </section>

    <!-- PREVIOUS / CURRENT / NEXT AGENT BAR -->
    <div style="display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap; margin-bottom:24px;">
      <button type="button" class="g-btn" onclick="stepAgent(-1)">&larr; Previous Agent</button>
      <div id="agentCounterLabel" style="font-family:var(--font-display); font-size:19px; font-weight:700; color:var(--g-blue);">
        Agent 1 of 60
      </div>
      <button type="button" class="g-btn g-btn-primary" onclick="stepAgent(1)">Next Agent &rarr;</button>
    </div>

    <!-- SINGLE AGENT LINEAR VIEW -->
    <div id="singleAgentMount"></div>
  </main>

  <script>
    const AGENTS = {agents_json};
    let currentIdx = 0;

    function getChecked(key) {{
      return localStorage.getItem('g_pb_' + key) === '1';
    }}
    function setChecked(key, val) {{
      if (val) localStorage.setItem('g_pb_' + key, '1');
      else localStorage.removeItem('g_pb_' + key);
      updateGlobalProgress();
      renderAgentPills(AGENTS[currentIdx].deptId);
    }}
    function isAgentFullyVerified(agId) {{
      for (let i = 1; i <= 5; i++) {{
        if (!getChecked(agId + '_' + i)) return false;
      }}
      return true;
    }}
    function markAllCurrentAgentVerified() {{
      const ag = AGENTS[currentIdx];
      for (let i = 1; i <= 5; i++) {{
        localStorage.setItem('g_pb_' + ag.id + '_' + i, '1');
      }}
      updateGlobalProgress();
      renderSingleAgent();
      renderAgentPills(ag.deptId);
    }}
    function updateGlobalProgress() {{
      let done = 0;
      AGENTS.forEach(ag => {{
        if (isAgentFullyVerified(ag.id)) done++;
      }});
      const badge = document.getElementById('globalProgressBadge');
      if (badge) badge.textContent = `✓ ${{done}} / 60 Agents Tested`;
    }}

    function populateDropdown() {{
      const sel = document.getElementById('agentQuickSelect');
      sel.innerHTML = AGENTS.map((ag, idx) =>
        `<option value="${{idx}}">#${{String(ag.num).padStart(2, '0')}} · ${{ag.name}} (${{ag.subPillar}})</option>`
      ).join('');
    }}

    function selectPillar(deptId) {{
      document.querySelectorAll('.g-pillar-btn').forEach(b => {{
        b.classList.toggle('active', b.getAttribute('data-dept') === deptId);
      }});
      const firstIdx = AGENTS.findIndex(a => a.deptId === deptId);
      if (firstIdx >= 0) {{
        currentIdx = firstIdx;
        renderAgentPills(deptId);
        renderSingleAgent();
      }}
    }}

    function renderAgentPills(deptId) {{
      const container = document.getElementById('agentPillsContainer');
      const list = AGENTS.map((a, idx) => ({{ ...a, idx }})).filter(a => a.deptId === deptId);
      container.innerHTML = list.map(a => {{
        const done = isAgentFullyVerified(a.id);
        const active = a.idx === currentIdx ? 'active' : '';
        return `<button type="button" class="g-agent-pill ${{active}}" onclick="selectAgentByIndex(${{a.idx}})">
          <span>#${{String(a.num).padStart(2, '0')}} · ${{a.name}}</span>
          <span>${{done ? '✅' : (a.cloudRe ? '🟢' : '📦')}}</span>
        </button>`;
      }}).join('');
    }}

    function selectAgentByIndex(idx) {{
      if (idx < 0) idx = AGENTS.length - 1;
      if (idx >= AGENTS.length) idx = 0;
      currentIdx = idx;
      const ag = AGENTS[currentIdx];
      document.querySelectorAll('.g-pillar-btn').forEach(b => {{
        b.classList.toggle('active', b.getAttribute('data-dept') === ag.deptId);
      }});
      renderAgentPills(ag.deptId);
      renderSingleAgent();
      const sel = document.getElementById('agentQuickSelect');
      if (sel) sel.value = String(currentIdx);
    }}

    function stepAgent(delta) {{
      selectAgentByIndex(currentIdx + delta);
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function copyTextBtn(btn, text) {{
      navigator.clipboard.writeText(text).then(() => {{
        const orig = btn.innerHTML;
        btn.innerHTML = '✓ Copied!';
        setTimeout(() => {{ btn.innerHTML = orig; }}, 1400);
      }});
    }}

    function renderSingleAgent() {{
      const ag = AGENTS[currentIdx];
      document.getElementById('agentCounterLabel').textContent =
        `Agent ${{ag.num}} of 60 — ${{ag.name}}`;

      const c1 = getChecked(ag.id + '_1') ? 'checked' : '';
      const c2 = getChecked(ag.id + '_2') ? 'checked' : '';
      const c3 = getChecked(ag.id + '_3') ? 'checked' : '';
      const c4 = getChecked(ag.id + '_4') ? 'checked' : '';
      const c5 = getChecked(ag.id + '_5') ? 'checked' : '';

      const mount = document.getElementById('singleAgentMount');
      mount.innerHTML = `
        <!-- CARD 1: AGENT HEADER & PLAIN-ENGLISH TABLE -->
        <section class="g-card" style="border-top: 6px solid ${{ag.pillarColor}};">
          <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:16px; flex-wrap:wrap; margin-bottom:20px;">
            <div>
              <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:10px;">
                <span class="g-chip" style="background:${{ag.pillarBg}}; color:${{ag.pillarColor}}; font-weight:700;">
                  ${{ag.pillarTitle}}
                </span>
                <span class="g-chip" style="background:#F1F3F4; color:#3C4043;">
                  Sub-Pillar: ${{ag.subPillar}}
                </span>
                <span class="g-chip" style="background:#FEF7E0; color:#B06000;">
                  👤 Persona: ${{ag.persona}}
                </span>
                ${{ag.cloudRe
                  ? `<span class="g-chip" style="background:#E6F4EA; color:#1E8E3E;">🟢 Live in Gemini Enterprise (RE ${{ag.cloudRe.slice(0,8)}}…)</span>`
                  : `<span class="g-chip" style="background:#E8F0FE; color:#1A73E8;">📦 Local ADK Ready</span>`
                }}
              </div>
              <h2 style="font-family:var(--font-display); font-size:32px; margin:0;">
                #${{String(ag.num).padStart(2, '0')}} · ${{ag.name}}
              </h2>
              <div style="font-family:var(--font-mono); font-size:14px; color:var(--text-sub); margin-top:4px;">
                Agent ID: <code>${{ag.id}}</code>
              </div>
            </div>
            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
              <span class="g-chip" style="background:#E6F4EA; color:#1E8E3E; font-size:15px; font-weight:700; padding:8px 16px;">
                🚀 ${{ag.roiBadge}}
              </span>
              <a href="index.html#agent/${{ag.id}}" class="g-btn">Open in Portal &rarr;</a>
            </div>
          </div>

          <div class="g-step-badge" style="background:#E8F0FE; color:#1A73E8;">
            🗣️ PART 1 · HOW TO EXPLAIN THIS AGENT TO A CUSTOMER (PLAIN ENGLISH TABLE)
          </div>
          <div class="g-table-wrap">
            <table class="g-table">
              <thead>
                <tr>
                  <th style="width:220px;">Question</th>
                  <th>Plain-English Answer (All Abbreviations Spelled Out)</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td style="font-weight:700; color:#D93025;">✕ 1. What Problem Does the Customer Have Today?</td>
                  <td>${{ag.problem}}</td>
                </tr>
                <tr>
                  <td style="font-weight:700; color:#1A73E8;">✦ 2. What Does This AI Agent Do?</td>
                  <td>${{ag.solution}}</td>
                </tr>
                <tr>
                  <td style="font-weight:700; color:#1E8E3E;">🚀 3. What Business Result Does It Deliver?</td>
                  <td><strong>${{ag.outcome}}</strong> (${{ag.roiBadge}})</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- CARD 2: VISUAL 4-STEP DIAGRAM -->
        <section class="g-card">
          <div class="g-step-badge" style="background:#FEF7E0; color:#B06000;">
            🗺️ PART 2 · VISUAL 4-STEP FLOW DIAGRAM
          </div>
          <h3 style="font-family:var(--font-display); font-size:22px; margin:0 0 14px;">
            How <strong>${{ag.name}}</strong> Works in 4 Simple Steps
          </h3>
          ${{ag.flowSvg}}
        </section>

        <!-- CARD 3: INPUT PROMPT & DEMO DATA TABLES -->
        <section class="g-card">
          <div class="g-step-badge" style="background:#E8F0FE; color:#1A73E8;">
            📥 PART 3 · INPUT YOU GIVE &amp; DEMO DATA TABLES IT READS
          </div>
          <h3 style="font-family:var(--font-display); font-size:22px; margin:0 0 12px;">
            Step 3A · Copy &amp; Paste This Input Prompt to Test the Agent
          </h3>
          <div style="background:#E8F0FE; border:2px solid #4285F4; border-radius:16px; padding:22px 26px; margin-bottom:28px; display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap;">
            <div style="font-size:19px; font-weight:700; color:#174EA6; flex:1; min-width:260px;">
              “${{ag.prompt}}”
            </div>
            <button type="button" class="g-btn g-btn-primary" onclick='copyTextBtn(this, ${{JSON.stringify(ag.prompt)}})'>
              📋 Copy Input Prompt
            </button>
          </div>

          <h3 style="font-family:var(--font-display); font-size:22px; margin:0 0 8px;">
            Step 3B · Demo Data Tables the Agent Reads Automatically (${{ag.tableCount}} Tables)
          </h3>
          <p style="color:var(--text-sub); margin:0 0 16px;">
            When you give the prompt above, the agent calls <code>${{ag.readTools.join('</code>, <code>')}}</code> to read these exact demo data records:
          </p>
          ${{ag.inputTablesHtml}}
        </section>

        <!-- CARD 4: EXACT EXPECTED OUTPUT (CHART + TABLE + ACTION RECEIPT) -->
        <section class="g-card" style="border-top: 6px solid #1E8E3E;">
          <div class="g-step-badge" style="background:#E6F4EA; color:#1E8E3E;">
            📤 PART 4 · EXACT EXPECTED OUTPUT YOU MUST RECEIVE BACK
          </div>

          <h3 style="font-family:var(--font-display); font-size:22px; margin:0 0 10px;">
            Output 4A · Expected Visual Graphic Card (A2UI <code>VegaChart</code>)
          </h3>
          <p style="color:var(--text-sub); margin:0 0 14px;">
            Verify that the agent renders the <strong>${{ag.chartTitle}}</strong> (<code>${{ag.chartType}}</code>) chart with these values:
          </p>
          <div class="g-subcard" style="margin-bottom:28px;">
            <div style="display:flex; align-items:center; justify-content:space-between; gap:10px; flex-wrap:wrap; margin-bottom:12px;">
              <strong style="font-size:17px; color:#202124;">📊 ${{ag.chartTitle}}</strong>
              <span class="g-chip" style="background:#E6F4EA; color:#1E8E3E;">Chart Type: ${{ag.chartType}}</span>
            </div>
            ${{ag.chartSvg}}
          </div>

          <h3 style="font-family:var(--font-display); font-size:22px; margin:0 0 10px;">
            Output 4B · Expected Written Reply &amp; Numbers Table
          </h3>
          <p style="color:var(--text-sub); margin:0 0 14px;">
            Verify that the agent's text response and table match these exact numbers:
          </p>
          <div class="g-subcard" style="background:#FFFFFF; margin-bottom:28px;">
            ${{ag.expectedMdHtml}}
          </div>

          <h3 style="font-family:var(--font-display); font-size:22px; margin:0 0 10px;">
            Output 4C · Expected Action Receipt Table (Tool: <code>${{ag.writeTools.join(', ') || 'action_commit'}}</code>)
          </h3>
          ${{ag.receiptTableHtml}}
        </section>

        <!-- CARD 5: 5-ROW TABULAR VERIFICATION CHECKLIST -->
        <section class="g-card">
          <div style="display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap; margin-bottom:16px;">
            <div>
              <div class="g-step-badge" style="background:#E6F4EA; color:#1E8E3E;">
                ✅ PART 5 · 5-POINT MANUAL TESTING CHECKLIST
              </div>
              <h3 style="font-family:var(--font-display); font-size:24px; margin:0;">
                Tick Each Box as You Verify <strong>${{ag.name}}</strong>
              </h3>
            </div>
            <button type="button" class="g-btn g-btn-primary" style="background:#1E8E3E; border-color:#1E8E3E;" onclick="markAllCurrentAgentVerified()">
              ✓ Mark All 5 Verified
            </button>
          </div>

          <div class="g-table-wrap" style="margin-bottom:24px;">
            <table class="g-table">
              <thead>
                <tr>
                  <th style="width:70px; text-align:center;">Done</th>
                  <th style="width:240px;">Check Step</th>
                  <th>What to Confirm</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td style="text-align:center;"><input type="checkbox" class="g-check-box" ${{c1}} onchange="setChecked('${{ag.id}}_1', this.checked)" /></td>
                  <td style="font-weight:700;">1. Read Demo Data</td>
                  <td>Agent called <code>${{ag.readTools.slice(0,3).join(', ')}}</code> across its ${{ag.tableCount}} input tables.</td>
                </tr>
                <tr>
                  <td style="text-align:center;"><input type="checkbox" class="g-check-box" ${{c2}} onchange="setChecked('${{ag.id}}_2', this.checked)" /></td>
                  <td style="font-weight:700;">2. Rendered Visual Chart</td>
                  <td>Agent displayed the <strong>${{ag.chartTitle}}</strong> (<code>${{ag.chartType}}</code>) graphic card.</td>
                </tr>
                <tr>
                  <td style="text-align:center;"><input type="checkbox" class="g-check-box" ${{c3}} onchange="setChecked('${{ag.id}}_3', this.checked)" /></td>
                  <td style="font-weight:700;">3. Accurate Table Numbers</td>
                  <td>Output table matches the exact SKU / Facility / Order numbers in Output 4B above.</td>
                </tr>
                <tr>
                  <td style="text-align:center;"><input type="checkbox" class="g-check-box" ${{c4}} onchange="setChecked('${{ag.id}}_4', this.checked)" /></td>
                  <td style="font-weight:700;">4. Executed Action Tool</td>
                  <td>Agent called <code>${{ag.writeTools.join(', ') || 'action_commit'}}</code> and returned the signed receipt in Output 4C.</td>
                </tr>
                <tr>
                  <td style="text-align:center;"><input type="checkbox" class="g-check-box" ${{c5}} onchange="setChecked('${{ag.id}}_5', this.checked)" /></td>
                  <td style="font-weight:700;">5. Safety Gate Works</td>
                  <td>Blocks unapproved write-back if <code>idempotency_key</code> is missing.</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div style="display:flex; align-items:center; justify-content:space-between; gap:14px; flex-wrap:wrap;">
            <div style="display:flex; gap:10px; flex-wrap:wrap;">
              <button type="button" class="g-btn" onclick='copyTextBtn(this, ${{JSON.stringify(ag.cmdRun)}})'>💻 Copy CLI Run Command</button>
              <button type="button" class="g-btn" onclick='copyTextBtn(this, ${{JSON.stringify(ag.cmdGate)}})'>🛡️ Copy Safety Gate Test</button>
            </div>
            <button type="button" class="g-btn g-btn-primary" style="font-size:16px; padding:12px 26px;" onclick="stepAgent(1)">
              Next Agent (#${{String((currentIdx + 1) % AGENTS.length + 1).padStart(2, '0')}}) &rarr;
            </button>
          </div>
        </section>
      `;
    }}

    populateDropdown();
    updateGlobalProgress();
    selectAgentByIndex(0);
  </script>
</body>
</html>
"""
    out_path = ROOT / "agent_testing_and_video_playbook.html"
    out_path.write_text(html_doc, encoding="utf-8")
    print(f"Rebuilt one-by-one Google clean {out_path.name} ({len(html_doc)//1024} KB)")


def build_google_linear_academy() -> None:
    """Rebuilds supply_chain_101_interactive_academy.html in Google's bright, spacious, linear, button-wise & tabular design language."""
    fc_json = json.dumps(FLASHCARDS, ensure_ascii=False)
    wf_json = json.dumps(WORKFLOW_SIMULATORS, ensure_ascii=False)
    dec_json = json.dumps(CUSTOMER_DECODER, ensure_ascii=False)
    quiz_json = json.dumps(QUIZ_QUESTIONS, ensure_ascii=False)

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Supply Chain 101 — Simple, Spacious, Button-Wise &amp; Tabular Google Guide</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Google+Sans+Display:wght@500;700&family=Google+Sans:wght@400;500;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --g-blue: #1A73E8;
      --g-blue-bg: #E8F0FE;
      --g-red: #D93025;
      --g-red-bg: #FCE8E6;
      --g-yellow: #F9AB00;
      --g-yellow-bg: #FEF7E0;
      --g-green: #1E8E3E;
      --g-green-bg: #E6F4EA;
      --bg-page: #F8F9FA;
      --bg-card: #FFFFFF;
      --text-main: #202124;
      --text-sub: #5F6368;
      --border-light: #DADCE0;
      --font-display: 'Google Sans Display', 'Google Sans', 'Inter', sans-serif;
      --font-sans: 'Google Sans', 'Inter', -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      background: var(--bg-page);
      color: var(--text-main);
      font-family: var(--font-sans);
      font-size: 17.5px;
      line-height: 1.72;
    }}
    .g-color-strip {{
      height: 5px;
      background: linear-gradient(90deg, #4285F4 0% 25%, #EA4335 25% 50%, #FBBC04 50% 75%, #34A853 75% 100%);
      position: sticky;
      top: 0;
      z-index: 200;
    }}
    .g-header {{
      position: sticky;
      top: 5px;
      z-index: 190;
      background: rgba(255, 255, 255, 0.96);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-light);
      padding: 14px 32px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }}
    .g-container {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 32px 24px 96px;
    }}
    .g-btn {{
      font-family: var(--font-sans);
      font-size: 15px;
      font-weight: 600;
      padding: 10px 20px;
      border-radius: 999px;
      border: 1.5px solid var(--border-light);
      background: #FFFFFF;
      color: var(--text-main);
      cursor: pointer;
      transition: all 0.18s ease;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }}
    .g-btn:hover {{
      border-color: var(--g-blue);
      color: var(--g-blue);
      background: var(--g-blue-bg);
    }}
    .g-btn.active, .g-btn-primary {{
      background: var(--g-blue);
      color: #FFFFFF;
      border-color: var(--g-blue);
    }}
    .g-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-light);
      border-radius: 20px;
      padding: 34px 38px;
      margin-bottom: 28px;
      box-shadow: 0 2px 10px rgba(60, 64, 67, 0.06);
    }}
    .g-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 6px 14px;
      border-radius: 999px;
      margin-bottom: 12px;
    }}
    /* Chapter Navigation Bar */
    .g-chapter-bar {{
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 28px;
    }}
    @media (max-width: 900px) {{
      .g-chapter-bar {{ grid-template-columns: 1fr 1fr; }}
    }}
    .g-chap-btn {{
      font-family: var(--font-sans);
      font-size: 15px;
      font-weight: 700;
      padding: 16px 14px;
      border-radius: 16px;
      border: 2px solid var(--border-light);
      background: #FFFFFF;
      color: var(--text-main);
      cursor: pointer;
      text-align: center;
      transition: all 0.18s ease;
    }}
    .g-chap-btn:hover {{
      border-color: var(--g-blue);
      background: var(--g-blue-bg);
    }}
    .g-chap-btn.active {{
      background: var(--g-blue);
      color: #FFFFFF;
      border-color: var(--g-blue);
      box-shadow: 0 4px 12px rgba(26, 115, 232, 0.22);
    }}
    .g-pane {{ display: none; }}
    .g-pane.active {{ display: block; }}

    /* Spacious Google Tables */
    .g-table-wrap {{
      overflow-x: auto;
      border-radius: 14px;
      border: 1px solid var(--border-light);
      background: #FFFFFF;
    }}
    .g-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 16.5px;
    }}
    .g-table th, .g-table td {{
      padding: 18px 22px;
      text-align: left;
      border-bottom: 1px solid #E8EAED;
      vertical-align: top;
      line-height: 1.68;
    }}
    .g-table th {{
      background: #F1F3F4;
      color: #202124;
      font-weight: 700;
      font-size: 14px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .g-table tr:last-child td, .g-table tr:last-child th {{
      border-bottom: none;
    }}
    .g-table tr:hover td {{
      background: #F8FAFD;
    }}
    code {{
      font-family: var(--font-mono);
      font-size: 14.5px;
      background: #F1F3F4;
      color: #1A73E8;
      padding: 2px 7px;
      border-radius: 6px;
    }}
  </style>
</head>
<body>
  <div class="g-color-strip"></div>
  <header class="g-header">
    <div style="display:flex; align-items:center; gap:14px; flex-wrap:wrap;">
      <a href="index.html" class="g-btn">&larr; Main Portal</a>
      <span style="font-family:var(--font-display); font-size:20px; font-weight:700; color:#202124;">
        🎓 Supply Chain 101 — Simple, Linear &amp; Tabular Guide
      </span>
    </div>
    <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
      <a href="agent_testing_and_video_playbook.html" class="g-btn g-btn-primary">
        📋 Open One-by-One Agent Testing Playbook &rarr;
      </a>
    </div>
  </header>

  <main class="g-container">
    <!-- SIMPLE HERO -->
    <section class="g-card" style="padding:28px 34px; background:linear-gradient(135deg, #E8F0FE 0%, #FFFFFF 65%, #E6F4EA 100%);">
      <span class="g-badge" style="background:#FFFFFF; color:var(--g-blue); border:1px solid #DADCE0;">
        ZERO UNEXPLAINED JARGON · ONE STEP AT A TIME
      </span>
      <h1 style="font-family:var(--font-display); font-size:34px; margin:0 0 8px;">
        Learn Supply Chain From Scratch (Button-by-Button &amp; Tabular)
      </h1>
      <p style="margin:0; color:var(--text-sub); font-size:18px; max-width:920px;">
        Click through the <strong>5 simple chapters</strong> below one at a time. Every concept is explained in everyday words using clean tables, bright Google diagrams, and one-by-one interactive cards.
      </p>
    </section>

    <!-- 5 CHAPTER BUTTONS -->
    <nav class="g-chapter-bar">
      <button type="button" class="g-chap-btn active" onclick="switchChapter('chap1', this)">
        1 · Intro to Supply Chain &amp; The 7 Stages
      </button>
      <button type="button" class="g-chap-btn" onclick="switchChapter('chap2', this)">
        2 · Bullwhip &amp; 4 Core Diagrams
      </button>
      <button type="button" class="g-chap-btn" onclick="switchChapter('chap3', this)">
        3 · 4 Step-by-Step Processes
      </button>
      <button type="button" class="g-chap-btn" onclick="switchChapter('chap4', this)">
        4 · All 56 Terms (1-by-1 or Table)
      </button>
      <button type="button" class="g-chap-btn" onclick="switchChapter('chap5', this)">
        5 · Customer Decoder &amp; Quiz
      </button>
    </nav>

    <!-- ===================================================================
         CHAPTER 1: INTRODUCTION TO SUPPLY CHAIN, WHERE IT FITS & THE 7 STAGES
         =================================================================== -->
    <div id="chap1" class="g-pane active">
      <!-- SECTION 1A: WHAT IS A SUPPLY CHAIN & WHERE DOES IT COME INTO THE PICTURE? -->
      <section class="g-card" style="border-top: 6px solid var(--g-blue);">
        <span class="g-badge" style="background:var(--g-blue-bg); color:var(--g-blue);">
          PART 1A · INTRODUCTION — WHAT IS A SUPPLY CHAIN ALL ABOUT?
        </span>
        <h2 style="font-family:var(--font-display); font-size:30px; margin:0 0 12px;">
          What Is a Supply Chain, and Where Does It Come Into the Picture?
        </h2>
        <p style="font-size:18px; color:var(--text-main); margin:0 0 16px;">
          Look at any physical item around you right now — a <strong>jar of coffee</strong>, a <strong>smartphone</strong>, a <strong>pair of running shoes</strong>, or <strong>medicine at a pharmacy</strong>. None of those products magically appeared on a shelf. Every single one started as raw materials in the ground (coffee beans on a farm, silica sand for microchips, rubber and cotton, chemical compounds) and had to be <strong>planned, bought, manufactured, packed, stored in warehouses, shipped across oceans and highways, and placed on a shelf</strong> at the exact moment you wanted to buy it.
        </p>
        <div style="background:#E8F0FE; border-left:5px solid #1A73E8; border-radius:12px; padding:18px 22px; margin-bottom:26px; font-size:18px; font-weight:600; color:#174EA6;">
          💡 <strong>In one simple sentence:</strong> The <strong>Supply Chain</strong> is the entire end-to-end system of people, factories, suppliers, warehouses, trucks, and software that turns raw ingredients into a finished product in the customer’s hands — and it accounts for <strong>60% to 80% of a product company’s total cost!</strong>
        </div>

        <h3 style="font-family:var(--font-display); font-size:23px; margin:0 0 12px;">
          Where Does Supply Chain Come Into the Picture Inside a Company?
        </h3>
        <p style="color:var(--text-sub); margin:0 0 16px;">
          Every product company has 4 main parts. Here is how they hand the baton to each other, and where Supply Chain takes over:
        </p>

        <!-- Bright Google SVG: Where Supply Chain Fits in the Enterprise -->
        <svg viewBox="0 0 1020 126" style="width:100%; height:auto; display:block; margin-bottom:20px; background:#F8F9FA; border-radius:16px; border:1px solid #DADCE0; padding:8px;">
          <g transform="translate(14,16)">
            <rect width="205" height="94" rx="14" fill="#FFFFFF" stroke="#DADCE0" stroke-width="2"/>
            <text x="102" y="30" text-anchor="middle" fill="#5F6368" font-size="11.5" font-weight="800">1 · R&amp;D / PRODUCT</text>
            <text x="102" y="54" text-anchor="middle" fill="#202124" font-size="14.5" font-weight="700">🧪 Designs Product</text>
            <text x="102" y="76" text-anchor="middle" fill="#5F6368" font-size="11.5">Creates recipe (BOM)</text>
          </g>
          <text x="230" y="68" fill="#5F6368" font-size="20" font-weight="700">&rarr;</text>
          <g transform="translate(248,16)">
            <rect width="205" height="94" rx="14" fill="#FFFFFF" stroke="#DADCE0" stroke-width="2"/>
            <text x="102" y="30" text-anchor="middle" fill="#5F6368" font-size="11.5" font-weight="800">2 · MARKETING &amp; SALES</text>
            <text x="102" y="54" text-anchor="middle" fill="#202124" font-size="14.5" font-weight="700">📣 Creates Demand</text>
            <text x="102" y="76" text-anchor="middle" fill="#5F6368" font-size="11.5">Runs promos &amp; takes orders</text>
          </g>
          <text x="464" y="68" fill="#1A73E8" font-size="20" font-weight="700">&rarr;</text>
          <g transform="translate(482,12)">
            <rect width="300" height="102" rx="16" fill="#E8F0FE" stroke="#1A73E8" stroke-width="3"/>
            <text x="150" y="28" text-anchor="middle" fill="#1A73E8" font-size="12" font-weight="800">3 · 🎯 THE SUPPLY CHAIN (ENGINE ROOM)</text>
            <text x="150" y="54" text-anchor="middle" fill="#202124" font-size="15.5" font-weight="800">⚙️ Plans · Buys · Makes · Stores · Ships</text>
            <text x="150" y="76" text-anchor="middle" fill="#174EA6" font-size="12" font-weight="700">60%–80% of Company Cost &amp; Cash!</text>
            <text x="150" y="94" text-anchor="middle" fill="#5F6368" font-size="11">Led by Chief Supply Chain Officer (CSCO)</text>
          </g>
          <text x="794" y="68" fill="#1E8E3E" font-size="20" font-weight="700">&rarr;</text>
          <g transform="translate(812,16)">
            <rect width="194" height="94" rx="14" fill="#E6F4EA" stroke="#1E8E3E" stroke-width="2"/>
            <text x="97" y="30" text-anchor="middle" fill="#1E8E3E" font-size="11.5" font-weight="800">4 · FINANCE &amp; CFO</text>
            <text x="97" y="54" text-anchor="middle" fill="#202124" font-size="14.5" font-weight="700">💰 Collects Cash</text>
            <text x="97" y="76" text-anchor="middle" fill="#137333" font-size="11.5">Pays vendors &amp; books profit</text>
          </g>
        </svg>

        <div class="g-table-wrap" style="margin-bottom:28px;">
          <table class="g-table">
            <thead>
              <tr>
                <th style="width:230px;">Company Function</th>
                <th style="width:260px;">What They Do</th>
                <th>How Supply Chain Connects to Them</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="font-weight:700;">🧪 1. Product / R&amp;D</td>
                <td>Invents the product and defines its recipe of parts (<strong>BOM — Bill of Materials</strong>).</td>
                <td>Hands the recipe to Supply Chain so buyers can find suppliers for every screw, chip, bottle, and label before launch (<strong>NPI — New Product Introduction</strong>).</td>
              </tr>
              <tr>
                <td style="font-weight:700;">📣 2. Sales &amp; Marketing</td>
                <td>Runs price promotions, signs retail deals (Walmart, Amazon), and promises delivery dates.</td>
                <td>If Sales runs a 20%-off promotion without telling Supply Chain, stores run out of stock! Supply Chain works with Sales every month (<strong>S&amp;OP</strong>) to match supply with demand.</td>
              </tr>
              <tr style="background:#F8FAFD;">
                <td style="font-weight:800; color:#1A73E8;">⚙️ 3. THE SUPPLY CHAIN<br/><span style="font-size:13px; color:#5F6368;">(Office of the CSCO)</span></td>
                <td><strong>Forecasts demand, buys raw materials, runs factories, manages warehouses, and dispatches trucks/ships.</strong></td>
                <td><strong>The physical execution engine of the business.</strong> If Supply Chain fails, factories stop, shelves go empty, or millions of dollars get trapped in unsold warehouse inventory.</td>
              </tr>
              <tr>
                <td style="font-weight:700;">💰 4. Finance (The CFO)</td>
                <td>Manages company cash flow, profit margins, and supplier/customer payments.</td>
                <td>The CFO relies on Supply Chain to keep <strong>Inventory Cash (DIO)</strong> low, avoid expensive emergency air freight, and verify every supplier bill before paying (<strong>3-Way Match</strong>).</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3 style="font-family:var(--font-display); font-size:23px; margin:0 0 10px;">
          Why Is Supply Chain So Hard? (The 3-Way Tug-of-War)
        </h3>
        <p style="color:var(--text-sub); margin:0 0 14px;">
          Running a supply chain is difficult because every decision pulls in <strong>3 opposite directions</strong> at once:
        </p>
        <div class="g-table-wrap">
          <table class="g-table">
            <thead>
              <tr>
                <th style="width:220px;">Goal</th>
                <th style="width:200px;">Who Demands It</th>
                <th>What Happens If You Push Too Far</th>
                <th style="width:270px;">How Our AI Agents Solve It</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="font-weight:800; color:#1E8E3E;">🎯 1. High Service<br/>(Never Run Out)</td>
                <td><strong>Sales &amp; Retail Customers</strong><br/>(Want 99% <code>OTIF</code>)</td>
                <td>To never run out, you pile up mountains of extra backup stock in every warehouse — tying up tens of millions in cash!</td>
                <td><strong>Demand Sensing &amp; ATP Agents</strong> predict exact local demand and protect VIP stock.</td>
              </tr>
              <tr>
                <td style="font-weight:800; color:#1A73E8;">💵 2. Low Inventory Cash<br/>(Lean Warehouses)</td>
                <td><strong>Chief Financial Officer (CFO)</strong><br/>(Wants low <code>DIO</code> / <code>CCC</code>)</td>
                <td>If you slash warehouse stock too aggressively, a single supplier delay or warm weekend causes immediate store stockouts!</td>
                <td><strong>MEIO Safety Stock Agent</strong> mathematically places smaller, smarter buffers across hubs.</td>
              </tr>
              <tr>
                <td style="font-weight:800; color:#E8710A;">🚚 3. Low Operating Cost<br/>(Cheap Production &amp; Freight)</td>
                <td><strong>Factory &amp; Logistics Heads</strong><br/>(Want full lines &amp; full trucks)</td>
                <td>Waiting to fill a 53-foot truck or running huge factory batches saves unit cost, but makes reaction time slow when demand shifts.</td>
                <td><strong>Finite Scheduler &amp; 3D Load Studio</strong> cut changeover waste and pack multi-stop trucks.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- SECTION 1B: THE 7 STAGES OF THE SUPPLY CHAIN PROCESS (DETAILED WALKTHROUGH) -->
      <section class="g-card">
        <span class="g-badge" style="background:var(--g-blue-bg); color:var(--g-blue);">
          PART 1B · THE 7 STAGES OF THE SUPPLY CHAIN PROCESS (CLICK EACH STAGE IN ORDER)
        </span>
        <h2 style="font-family:var(--font-display); font-size:28px; margin:0 0 10px;">
          Step-by-Step: How the Supply Chain Process Works From Beginning to End
        </h2>
        <p style="color:var(--text-sub); margin:0 0 20px;">
          Notice that before a single physical box moves, the process starts with <strong>Stage 0 · Planning &amp; Forecasting</strong> (the brain), followed by the <strong>6 physical stages</strong>. Click each of the 7 stage buttons below in order (or use <code>Next Stage &rarr;</code>) for a deep, plain-English walkthrough:
        </p>

        <!-- Bright Google SVG 7-Stage Relay Diagram -->
        <svg viewBox="0 0 1060 124" style="width:100%; height:auto; display:block; margin-bottom:22px; background:#F8F9FA; border-radius:16px; border:1px solid #DADCE0; padding:8px;">
          <g transform="translate(8,18)">
            <rect width="132" height="88" rx="12" fill="#E8F0FE" stroke="#1A73E8" stroke-width="2.5"/>
            <text x="66" y="28" text-anchor="middle" fill="#1A73E8" font-size="11" font-weight="800">STAGE 0 (BRAIN)</text>
            <text x="66" y="52" text-anchor="middle" fill="#202124" font-size="13.5" font-weight="700">📈 Plan &amp; S&amp;OP</text>
            <text x="66" y="72" text-anchor="middle" fill="#5F6368" font-size="10.5">Forecast Demand</text>
          </g>
          <text x="145" y="65" fill="#1A73E8" font-size="16" font-weight="700">&rarr;</text>
          <g transform="translate(158,18)">
            <rect width="132" height="88" rx="12" fill="#FEF7E0" stroke="#F9AB00" stroke-width="2"/>
            <text x="66" y="28" text-anchor="middle" fill="#B06000" font-size="11" font-weight="800">STAGE 1 · SOURCE</text>
            <text x="66" y="52" text-anchor="middle" fill="#202124" font-size="13.5" font-weight="700">⛏️ Suppliers</text>
            <text x="66" y="72" text-anchor="middle" fill="#5F6368" font-size="10.5">Buy Raw Parts</text>
          </g>
          <text x="295" y="65" fill="#5F6368" font-size="16" font-weight="700">&rarr;</text>
          <g transform="translate(308,18)">
            <rect width="132" height="88" rx="12" fill="#F3E8FD" stroke="#9334E6" stroke-width="2"/>
            <text x="66" y="28" text-anchor="middle" fill="#9334E6" font-size="11" font-weight="800">STAGE 2 · MAKE</text>
            <text x="66" y="52" text-anchor="middle" fill="#202124" font-size="13.5" font-weight="700">🏭 Factory</text>
            <text x="66" y="72" text-anchor="middle" fill="#5F6368" font-size="10.5">Build &amp; QA Test</text>
          </g>
          <text x="445" y="65" fill="#5F6368" font-size="16" font-weight="700">&rarr;</text>
          <g transform="translate(458,18)">
            <rect width="132" height="88" rx="12" fill="#E6F4EA" stroke="#1E8E3E" stroke-width="2"/>
            <text x="66" y="28" text-anchor="middle" fill="#1E8E3E" font-size="11" font-weight="800">STAGE 3 · RDC</text>
            <text x="66" y="52" text-anchor="middle" fill="#202124" font-size="13.5" font-weight="700">🏢 Regional DC</text>
            <text x="66" y="72" text-anchor="middle" fill="#5F6368" font-size="10.5">Central Buffer</text>
          </g>
          <text x="595" y="65" fill="#5F6368" font-size="16" font-weight="700">&rarr;</text>
          <g transform="translate(608,18)">
            <rect width="132" height="88" rx="12" fill="#E8F0FE" stroke="#1A73E8" stroke-width="2"/>
            <text x="66" y="28" text-anchor="middle" fill="#1A73E8" font-size="11" font-weight="800">STAGE 4 · FDC</text>
            <text x="66" y="52" text-anchor="middle" fill="#202124" font-size="13.5" font-weight="700">📦 Local DC</text>
            <text x="66" y="72" text-anchor="middle" fill="#5F6368" font-size="10.5">Pick, Pack &amp; ATP</text>
          </g>
          <text x="745" y="65" fill="#5F6368" font-size="16" font-weight="700">&rarr;</text>
          <g transform="translate(758,18)">
            <rect width="132" height="88" rx="12" fill="#E4F7FB" stroke="#007B83" stroke-width="2"/>
            <text x="66" y="28" text-anchor="middle" fill="#007B83" font-size="11" font-weight="800">STAGE 5 · MOVE</text>
            <text x="66" y="52" text-anchor="middle" fill="#202124" font-size="13.5" font-weight="700">🚚 Fleet Transit</text>
            <text x="66" y="72" text-anchor="middle" fill="#5F6368" font-size="10.5">Ocean / Air / Truck</text>
          </g>
          <text x="895" y="65" fill="#5F6368" font-size="16" font-weight="700">&rarr;</text>
          <g transform="translate(908,18)">
            <rect width="142" height="88" rx="12" fill="#FCE8E6" stroke="#D93025" stroke-width="2"/>
            <text x="71" y="28" text-anchor="middle" fill="#D93025" font-size="11" font-weight="800">STAGE 6 · DELIVER</text>
            <text x="71" y="52" text-anchor="middle" fill="#202124" font-size="13.5" font-weight="700">🛒 Store &amp; RMA</text>
            <text x="71" y="72" text-anchor="middle" fill="#5F6368" font-size="10.5">OTIF, POS &amp; ESG</text>
          </g>
        </svg>

        <!-- 7 Stage Selector Buttons -->
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:20px;" id="stageBtnRow">
          <button type="button" class="g-btn active" onclick="showStageTable(0, this)">0 · 📈 Plan &amp; Forecast (The Brain)</button>
          <button type="button" class="g-btn" onclick="showStageTable(1, this)">1 · ⛏️ Source (Suppliers)</button>
          <button type="button" class="g-btn" onclick="showStageTable(2, this)">2 · 🏭 Make (Factory)</button>
          <button type="button" class="g-btn" onclick="showStageTable(3, this)">3 · 🏢 Central Store (RDC)</button>
          <button type="button" class="g-btn" onclick="showStageTable(4, this)">4 · 📦 Local Store (FDC)</button>
          <button type="button" class="g-btn" onclick="showStageTable(5, this)">5 · 🚚 Move (Fleet &amp; Transit)</button>
          <button type="button" class="g-btn" onclick="showStageTable(6, this)">6 · 🛒 Customer, OTIF &amp; Returns</button>
        </div>

        <div id="stageTableMount"></div>
      </section>

      <!-- THE 3 FLOWS TABLE -->
      <section class="g-card">
        <span class="g-badge" style="background:var(--g-green-bg); color:var(--g-green);">
          PART 1C · THE 3 FLOWS TABLE
        </span>
        <h2 style="font-family:var(--font-display); font-size:26px; margin:0 0 14px;">
          The 3 Things Moving Through Every Supply Chain at the Same Time
        </h2>
        <div class="g-table-wrap">
          <table class="g-table">
            <thead>
              <tr>
                <th style="width:230px;">Flow Name</th>
                <th style="width:180px;">Direction</th>
                <th>What Moves &amp; Why It Matters in Plain English</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="font-weight:700; color:#1E8E3E;">📦 1. Physical Goods Flow</td>
                <td><strong>Downstream (&rarr;)</strong><br/>Supplier &rarr; Customer</td>
                <td>Raw materials, parts, pallets, and finished boxes moving toward the customer. If this stops, store shelves go empty (<strong>Stockout</strong>).</td>
              </tr>
              <tr>
                <td style="font-weight:700; color:#1A73E8;">📡 2. Information Signal Flow</td>
                <td><strong>Upstream (&larr;)</strong><br/>Customer &rarr; Supplier</td>
                <td>Store checkout barcode scans (<strong>POS — Point of Sale</strong>), customer orders, and forecasts moving backward to tell factories what to make next.</td>
              </tr>
              <tr>
                <td style="font-weight:700; color:#E8710A;">💰 3. Money &amp; Cash Flow</td>
                <td><strong>Both Ways (&harr;)</strong><br/>Customer &harr; Company &harr; Vendor</td>
                <td>Customers pay invoices (<strong>DSO — Days Sales Outstanding</strong>), while the company pays suppliers after checking the invoice (<strong>3-Way Match</strong>).</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- THE 4 ENTERPRISE SOFTWARE SYSTEMS TABLE -->
      <section class="g-card">
        <span class="g-badge" style="background:#F3E8FD; color:#9334E6;">
          PART 1D · THE 4 SOFTWARE SYSTEMS TABLE
        </span>
        <h2 style="font-family:var(--font-display); font-size:26px; margin:0 0 14px;">
          ERP vs. MES vs. WMS vs. TMS — What Software Runs Which Building?
        </h2>
        <div class="g-table-wrap">
          <table class="g-table">
            <thead>
              <tr>
                <th style="width:140px;">Acronym</th>
                <th style="width:240px;">Full Name Spelled Out</th>
                <th style="width:200px;">Where It Lives</th>
                <th>What It Does in Plain Words (With Brand Examples)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong style="font-size:18px; color:#1A73E8;">ERP</strong></td>
                <td><strong>Enterprise Resource Planning</strong></td>
                <td>🏢 Corporate Head Office &amp; Finance</td>
                <td>The company’s financial brain. Holds customer orders, product part numbers (<strong>SKUs</strong>), supplier <strong>Purchase Orders (POs)</strong>, and accounting invoices. <em>(Examples: SAP S/4HANA, Oracle Cloud ERP)</em></td>
              </tr>
              <tr>
                <td><strong style="font-size:18px; color:#9334E6;">MES</strong></td>
                <td><strong>Manufacturing Execution System</strong></td>
                <td>🏭 Inside the Factory Floor</td>
                <td>Runs the factory machines and assembly lines. Tracks machine health (<strong>OEE</strong>), production schedules, and quality batch logs (<strong>eBHR</strong>). <em>(Examples: Siemens Opcenter, Rockwell)</em></td>
              </tr>
              <tr>
                <td><strong style="font-size:18px; color:#1E8E3E;">WMS</strong></td>
                <td><strong>Warehouse Management System</strong></td>
                <td>📦 Inside the 4 Walls of the Warehouse</td>
                <td>Tracks exactly which shelf bin every pallet sits in (<strong>Slotting</strong>) and guides workers with barcode scanners to pick and pack orders (<strong>Wave Picking</strong>). <em>(Examples: Manhattan Active, SAP EWM)</em></td>
              </tr>
              <tr>
                <td><strong style="font-size:18px; color:#007B83;">TMS</strong></td>
                <td><strong>Transportation Management System</strong></td>
                <td>🚚 Outside on the Road, Ocean &amp; Air</td>
                <td>Books trucking and shipping carriers, plans delivery routes, tracks live truck GPS, and audits freight bills. <em>(Examples: Oracle OTM, Blue Yonder TMS)</em></td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>

    <!-- ===================================================================
         CHAPTER 2: BULLWHIP SIMULATOR & 4 CORE VISUAL DIAGRAMS (ONE BY ONE)
         =================================================================== -->
    <div id="chap2" class="g-pane">
      <section class="g-card">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap; margin-bottom:14px;">
          <div>
            <span class="g-badge" style="background:var(--g-yellow-bg); color:#B06000;">
              CHAPTER 2A · INTERACTIVE BULLWHIP SIMULATOR
            </span>
            <h2 style="font-family:var(--font-display); font-size:28px; margin:0;">
              Why Small Store Changes Cause Giant Factory Panic (“The Bullwhip Effect”)
            </h2>
          </div>
          <button type="button" id="bwAiBtn" class="g-btn" style="border-color:var(--g-green); color:var(--g-green); font-weight:700;" onclick="toggleBwAi()">
            ✨ Turn On AI Demand Sensing: OFF
          </button>
        </div>
        <p style="color:var(--text-sub); margin:0 0 18px;">
          Drag the slider below to change how much extra customers buy at the store checkout, and see what happens to orders at each stage upstream in the table below:
        </p>

        <div style="background:#F8F9FA; border:1px solid var(--border-light); border-radius:16px; padding:20px 24px; margin-bottom:20px;">
          <label style="font-weight:700; font-size:18px; display:flex; justify-content:space-between;">
            <span>🛒 Customer Checkout Surge at the Store (POS):</span>
            <span id="bwValLabel" style="color:var(--g-blue); font-weight:800;">+10%</span>
          </label>
          <input type="range" id="bwRange" min="5" max="25" value="10" style="width:100%; margin-top:12px; accent-color:var(--g-blue);" oninput="renderBwTable()" />
        </div>

        <div id="bwTableMount"></div>
      </section>

      <!-- 4 CORE VISUAL DIAGRAMS (CLICK 1 BUTTON AT A TIME) -->
      <section class="g-card">
        <span class="g-badge" style="background:var(--g-blue-bg); color:var(--g-blue);">
          CHAPTER 2B · 4 ESSENTIAL VISUAL DIAGRAMS (CLICK ONE BUTTON AT A TIME)
        </span>
        <h2 style="font-family:var(--font-display); font-size:28px; margin:0 0 16px;">
          Click Any Concept Below to View Its Diagram &amp; Simple Comparison Table
        </h2>
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:24px;">
          <button type="button" class="g-btn active" onclick="showConceptDiagram(0, this)">1 · Make-to-Stock (MTS) vs. Make-to-Order (MTO)</button>
          <button type="button" class="g-btn" onclick="showConceptDiagram(1, this)">2 · Warehouse Rules: FEFO vs. FIFO vs. LIFO</button>
          <button type="button" class="g-btn" onclick="showConceptDiagram(2, this)">3 · Cash Cycle: CCC = DIO + DSO − DPO</button>
          <button type="button" class="g-btn" onclick="showConceptDiagram(3, this)">4 · Carbon Footprint: Scope 1, 2 &amp; 3</button>
        </div>

        <div id="conceptDiagramMount"></div>
      </section>
    </div>

    <!-- ===================================================================
         CHAPTER 3: 4 STEP-BY-STEP SUPPLY CHAIN PROCESSES (TABULAR)
         =================================================================== -->
    <div id="chap3" class="g-pane">
      <section class="g-card">
        <span class="g-badge" style="background:var(--g-green-bg); color:var(--g-green);">
          CHAPTER 3 · 4 CORE SUPPLY CHAIN WORKFLOWS (BUTTON-BY-BUTTON &amp; TABULAR)
        </span>
        <h2 style="font-family:var(--font-display); font-size:28px; margin:0 0 12px;">
          How Supply Chain Teams Actually Work Day-to-Day
        </h2>
        <p style="color:var(--text-sub); margin:0 0 20px;">
          Click any of the 4 core processes below to see every step in a clean, spacious table comparing the <strong>Old Manual Way</strong> vs. the <strong>New AI Agent Way</strong>:
        </p>

        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:24px;">
          <button type="button" class="g-btn active" onclick="selectWorkflow('sop', this)">1 · 📅 Monthly Planning (S&amp;OP)</button>
          <button type="button" class="g-btn" onclick="selectWorkflow('match3', this)">2 · 🧾 Paying Suppliers (3-Way Match)</button>
          <button type="button" class="g-btn" onclick="selectWorkflow('wms_flow', this)">3 · 📦 Warehouse Flow (Inbound to Ship)</button>
          <button type="button" class="g-btn" onclick="selectWorkflow('otif_flow', this)">4 · 🚚 Customer Order to Delivery (OTIF)</button>
        </div>

        <div id="workflowMount"></div>
      </section>
    </div>

    <!-- ===================================================================
         CHAPTER 4: ALL 56 SUPPLY CHAIN TERMS (1-BY-1 CARD OR CLEAN TABLE)
         =================================================================== -->
    <div id="chap4" class="g-pane">
      <section class="g-card">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap; margin-bottom:18px;">
          <div>
            <span class="g-badge" style="background:var(--g-blue-bg); color:var(--g-blue);">
              CHAPTER 4 · ALL 56 TERMS SPELLED OUT &amp; EXPLAINED SIMPLY
            </span>
            <h2 style="font-family:var(--font-display); font-size:28px; margin:0;">
              Learn One Term at a Time — Or Browse the Clean Table
            </h2>
          </div>
          <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <button type="button" id="modeOneBtn" class="g-btn active" onclick="setTermsMode('one')">🎯 One-by-One Card View</button>
            <button type="button" id="modeTableBtn" class="g-btn" onclick="setTermsMode('table')">📋 Clean Table View</button>
          </div>
        </div>

        <!-- Topic Filter Buttons -->
        <div style="display:flex; gap:8px; flex-wrap:wrap; margin-bottom:22px;">
          <button type="button" class="g-btn active" onclick="filterTerms('all', this)">All 56 Terms</button>
          <button type="button" class="g-btn" onclick="filterTerms('top15', this)">⭐ Top 15 Must-Know</button>
          <button type="button" class="g-btn" onclick="filterTerms('planning', this)">01 · Planning</button>
          <button type="button" class="g-btn" onclick="filterTerms('sourcing', this)">02 · Sourcing</button>
          <button type="button" class="g-btn" onclick="filterTerms('manufacturing', this)">03 · Factory</button>
          <button type="button" class="g-btn" onclick="filterTerms('inventory', this)">04 · Warehouse</button>
          <button type="button" class="g-btn" onclick="filterTerms('logistics', this)">05 · Logistics</button>
          <button type="button" class="g-btn" onclick="filterTerms('finance_esg', this)">06 · Finance &amp; ESG</button>
        </div>

        <div id="termsMount"></div>
      </section>
    </div>

    <!-- ===================================================================
         CHAPTER 5: CUSTOMER CONVERSATION DECODER TABLE & 1-BY-1 QUIZ
         =================================================================== -->
    <div id="chap5" class="g-pane">
      <section class="g-card">
        <span class="g-badge" style="background:var(--g-red-bg); color:var(--g-red);">
          CHAPTER 5A · CUSTOMER CONVERSATION DECODER TABLE
        </span>
        <h2 style="font-family:var(--font-display); font-size:28px; margin:0 0 12px;">
          When a Customer Complains About “X” &rarr; What It Means &amp; Which Agent to Demo
        </h2>
        <div class="g-table-wrap">
          <table class="g-table" id="decoderTableMount"></table>
        </div>
      </section>

      <section class="g-card">
        <span class="g-badge" style="background:var(--g-green-bg); color:var(--g-green);">
          CHAPTER 5B · ONE-BY-ONE PRACTICE QUIZ
        </span>
        <div id="quizOneMount"></div>
      </section>
    </div>
  </main>

  <script>
    const FLASHCARDS = {fc_json};
    const WORKFLOWS = {wf_json};
    const DECODER = {dec_json};
    const QUIZ = {quiz_json};

    const STAGES = [
      {{
        title: "Stage 0 · 📈 Demand Planning, Sensing & S&OP (The Brain of the Supply Chain)",
        whyExists: "Because buying raw materials and running factories takes weeks or months (Lead Time), a company cannot wait until you walk into a store to start making a product. Planning is the 'brain' that predicts what customers will buy, where, and when — and aligns Sales, Factories, Warehouses, and Finance around a single plan.",
        analogy: "🍽️ Everyday Analogy: Like a restaurant chef checking Friday reservation bookings, local weather, and last month's popular dishes before deciding how much fish and produce to order for the weekend.",
        story: "1. Forecasters pull historical sales, daily store checkout scans (POS), weather forecasts, and upcoming promotions.<br/>2. They generate a baseline demand forecast for each product (SKU) and measure forecast error (WAPE) and human bias (FVA).<br/>3. In the monthly S&OP (Sales & Operations Planning) cycle, Sales, Operations, and Finance resolve capacity gaps and lock a 'One-Number Plan'.",
        personas: "Demand Planner / Forecaster, S&OP / IBP Director, Trade Promotion Manager, New Product (NPI) Planner",
        docs: "Baseline Statistical Forecast, Consensus Demand Plan, Promotion Lift Calendar, Retailer CPFR Forecast",
        software: "IBP & Demand Planning Systems (SAP IBP, Kinaxis RapidResponse, o9 Solutions, Blue Yonder)",
        breaks: "Forecasts rely on 30-day-old ERP shipments instead of daily store checkout scans; sales reps manually inflate forecasts by +20% 'just in case' (Negative FVA), triggering the Bullwhip Effect.",
        agents: "Demand Sensing Agent (`demand_sensing_agent`), S&OP Scenario Weaver (`sop_scenario_weaver`), Promo Lift Simulator (`promo_lift_simulator`), CPFR Sync (`cpfr_sync_agent`), NPI Profiler (`npi_demand_profiler`)",
        terms: "SKU (Stock Keeping Unit), WAPE (Weighted Absolute Percentage Error), Bias, FVA (Forecast Value Added), S&OP (Sales & Operations Planning), IBP (Integrated Business Planning), CPFR, POS (Point of Sale)"
      }},
      {{
        title: "Stage 1 · ⛏️ Strategic Sourcing & Tier-N Suppliers (Buying Raw Materials & Packaging)",
        whyExists: "Once the Demand Plan says we need 500,000 jars of coffee next month, the factory cannot build anything without coffee beans, glass jars, metal lids, and paper labels. Sourcing finds qualified suppliers, negotiates fair prices, tracks multi-tier supply risks, and issues official Purchase Orders (POs).",
        analogy: "🥣 Everyday Analogy: Like a bakery checking its recipe card (Bill of Materials), comparing flour mill prices against wheat market prices, ordering 50 sacks of flour, and checking the bill before paying.",
        story: "1. ERP explodes the finished product forecast into raw component quantities using the Bill of Materials (BOM).<br/>2. Category Buyers send out Requests for Quotations (RFQs) and compare vendor bids against a bottom-up Should-Cost model tied to live commodity indices (steel, resin, coffee, energy).<br/>3. Buyers check Tier-2 and Tier-3 sub-suppliers for disruptions or tariff/ESG risks, then issue a binding Purchase Order (PO).<br/>4. When the supplier sends an invoice, Accounts Payable verifies the 3-Way Match (PO vs. Warehouse Goods Receipt vs. Invoice) before paying.",
        personas: "Category Procurement Manager, Supplier Risk Manager, Accounts Payable / 3-Way Match Specialist, Packaging Sustainability Lead",
        docs: "BOM (Bill of Materials), RFQ (Request for Quotation), Should-Cost Model, PO (Purchase Order), 3-Way Match Packet, NCR (Non-Conformance Report)",
        software: "ERP & Source-to-Pay Portals (SAP Ariba, Coupa, SAP S/4HANA MM, Oracle Procurement)",
        breaks: "A Tier-2 sub-supplier has a factory fire that nobody knew about; suppliers pad quotes by +15% when commodity prices actually dropped; or 20% of invoices fail 3-Way Match due to price/quantity errors.",
        agents: "RFQ Should-Cost Agent (`rfq_should_cost_agent`), Tier-N Risk Sentinel (`tier_n_risk_sentinel`), Three-Way Match Dispute Agent (`three_way_match_dispute`), Supplier Quality Sentinel (`supplier_quality_sentinel`), Commodity Index Advisor (`commodity_index_advisor`)",
        terms: "BOM (Bill of Materials), RFQ (Request for Quotation), Should-Cost, Tier-1 / Tier-2 / Tier-3 Supplier, PO (Purchase Order), GRN (Goods Receipt Note), 3-Way Match, MOQ (Minimum Order Quantity), Lead Time, NCR & COPQ"
      }},
      {{
        title: "Stage 2 · 🏭 Manufacturing & Plant Operations (Making & Testing the Product)",
        whyExists: "This is where raw ingredients and components are physically transformed, mixed, assembled, filled, and quality-tested on high-speed production lines to become finished goods ready for sale.",
        analogy: "👩‍🍳 Everyday Analogy: Like a commercial kitchen scheduling which oven bakes bread vs. pastries, cleaning mixers between allergen batches, monitoring oven temperatures, and tasting every batch before boxing.",
        story: "1. Production Planners sequence jobs across factory lines (Finite Capacity Scheduling) to minimize wash-down and changeover downtime between flavors or sizes.<br/>2. Plant Engineers monitor machine health — Availability × Performance × Quality (OEE — Overall Equipment Effectiveness) — using vibration and temperature sensors.<br/>3. Cameras and sensors inspect products inline for defects, and Quality Assurance (QA) audits the Electronic Batch History Record (eBHR) and Certificate of Analysis (COA) to release the batch.",
        personas: "Master Production Scheduler, Plant Manager / OEE Lead, Quality Assurance (QA) Auditor, Line Labor Supervisor, Co-Packer Manager",
        docs: "Master Production Schedule (MPS), Work Order, eBHR (Electronic Batch History Record), COA (Certificate of Analysis), CIP (Clean-in-Place) Log",
        software: "MES — Manufacturing Execution System & SCADA/PLC Sensors (Siemens Opcenter, Rockwell FactoryTalk, SAP DMC)",
        breaks: "A critical motor bearing fails mid-shift causing $50,000/hr unplanned downtime; poor sequencing wastes 18 hours a week on line changeovers; or finished pallets sit quarantined for 6 days waiting for manual paper batch record review.",
        agents: "Predictive OEE Maintenance Sentinel (`predictive_oee_sentinel`), Finite Production Scheduler (`line_schedule_optimizer`), Inline Vision & Yield Guardian (`inline_yield_guardian`), Batch Record Auditor (`batch_record_auditor`), Labor Line Balancing (`labor_line_balancing_agent`)",
        terms: "OEE (Overall Equipment Effectiveness), MTS (Make-to-Stock) vs. MTO (Make-to-Order), Finite Scheduling, Changeover / Setup Time, eBHR (Electronic Batch Record), COA (Certificate of Analysis), CIP (Clean-in-Place)"
      }},
      {{
        title: "Stage 3 · 🏢 Regional Distribution Center — RDC (Central Network Inventory & Buffers)",
        whyExists: "Factories produce in large batches, but thousands of local stores need small replenishments every day. Regional Distribution Centers (RDCs) act as the central shock absorber — holding strategic safety stock buffers and distributing inventory across the country.",
        analogy: "🏦 Everyday Analogy: Like a central Federal Reserve vault that holds bulk cash reserves and replenishes local neighborhood bank branches whenever a branch runs low.",
        story: "1. Full truckloads of finished pallets arrive from factories at 3 to 5 huge Regional Distribution Centers (RDCs).<br/>2. Inventory Optimizers use Multi-Echelon Inventory Optimization (MEIO) math to decide how much Safety Stock and Reorder Point (ROP) buffer to hold centrally at the RDC vs. pushing forward to local warehouses.<br/>3. Planners monitor Slow-Moving & Obsolete stock (SLOB) and short-dated perishable batches so inventory doesn't expire or become dead cash.",
        personas: "Multi-Echelon Inventory Planner (MEIO), Network Allocation Lead, Inventory Health / SLOB Analyst, Cold-Chain Inventory Steward",
        docs: "Network Safety Stock Policy, Stock Transfer Order (STO), Inventory Aging / SLOB Report",
        software: "Enterprise Inventory & Supply Planning (SAP IBP Inventory, Kinaxis, Manhattan, ERP MM)",
        breaks: "Each warehouse manager hoards extra 'just-in-case' buffer in silos — locking up $40M in excess working capital while other regions simultaneously suffer stockouts!",
        agents: "MEIO Safety Stock Agent (`meio_safety_stock_agent`), SLOB Disposition Agent (`slob_disposition_agent`), Short-Dated Redistributor (`short_dated_redistributor`), Dynamic Markdown Agent (`dynamic_markdown_agent`)",
        terms: "RDC (Regional Distribution Center), MEIO (Multi-Echelon Inventory Optimization), Safety Stock, ROP (Reorder Point), SLOB (Slow-Moving & Obsolete Stock), DIO (Days Inventory Outstanding)"
      }},
      {{
        title: "Stage 4 · 📦 Local Fulfillment Center — FDC (Inside the 4 Walls of the Warehouse)",
        whyExists: "When a retail store or online shopper places an order, boxes must be unloaded, put away in rack bins, picked accurately, packed onto store-friendly pallets, and staged at outbound dock doors within hours.",
        analogy: "🛒 Everyday Analogy: Like organizing a giant supermarket backroom so fast-selling drinks sit right by the door at waist height, oldest milk is grabbed first, and outgoing carts are lined up by delivery route.",
        story: "1. Inbound trucks are sequenced to unloading doors (Yard & Dock Management) and pallets are scanned into inventory (Dock-to-Stock).<br/>2. The Warehouse Management System (WMS) assigns each product to an optimal rack bin (Slotting) and groups customer orders into picking waves (Wave Picking) following First-Expired, First-Out (FEFO).<br/>3. Or, if demand is urgent, incoming pallets bypass storage racks completely and roll straight across the floor to an outbound truck (Cross-Docking).<br/>4. Meanwhile, the Available-to-Promise (ATP) engine commits exact delivery dates to customer orders in milliseconds.",
        personas: "Warehouse Operations Manager, Slotting & Wave Supervisor, Order Promising (ATP) Specialist, Yard & Dock Coordinator",
        docs: "GRN (Goods Receipt Note), Putaway & Pick Wave List, Cross-Dock Flow Manifest, ATP Order Confirmation",
        software: "WMS — Warehouse Management System (Manhattan Active WMS, Blue Yonder WMS, SAP EWM)",
        breaks: "Trucks wait 4 hours at congested yard gates; pickers walk 9 miles a day because fast-moving items are slotted in high back aisles; or low-margin orders steal stock needed for VIP retail accounts.",
        agents: "Warehouse Slotting Optimizer (`warehouse_slotting_agent`), Wave Fulfillment Copilot (`wave_fulfillment_copilot`), ATP Order Promising Agent (`atp_order_promising_agent`), Cross-Dock Orchestrator (`crossdock_transfer_orchestrator`), Yard & Dock Sequencer (`yard_dock_sequencer`), Dock-to-Stock Agent (`dock_to_stock_agent`)",
        terms: "FDC (Fulfillment Distribution Center), WMS (Warehouse Management System), Dock-to-Stock, Slotting, Wave Picking, Cross-Docking, FEFO / FIFO, ATP (Available-to-Promise)"
      }},
      {{
        title: "Stage 5 · 🚚 Multi-Modal Fleet & Global Transit (Ocean Ships, Airplanes, Rail & Road Trucks)",
        whyExists: "Inventory sitting in a warehouse has zero value until it physically travels across oceans, railroads, and highways to reach the customer safely, legally, and at the lowest freight cost.",
        analogy: "✈️ Everyday Analogy: Like planning a cross-country move — choosing between ocean container ships, freight trains, or 53-foot highway trucks, packing boxes tightly to the roof in reverse stop order, and tracking live traffic.",
        story: "1. Load Planners pack orders into 3D trailer/container blueprints (Cube Utilization), putting Stop #1 last at the rear doors (LIFO — Last-In, First-Out) while respecting highway axle weight limits.<br/>2. Port Coordinators pull ocean containers from marine terminals before free days expire (Drayage) to avoid $300/day Demurrage & Detention fines.<br/>3. Dispatchers route trucks using live traffic, weather, and driver Electronic Logging Device (ELD / Hours of Service) limits, sending an Advance Ship Notice (ASN) and Bill of Lading (BOL) ahead of the truck.",
        personas: "Fleet & Route Dispatch Manager, Ocean Port & Drayage Lead, Air Cargo & Intermodal Planner, Freight Bill Audit Specialist",
        docs: "BOL (Bill of Lading), ASN (Advance Ship Notice / EDI 856), 3D LIFO Load Plan, Carrier Freight Invoice",
        software: "TMS — Transportation Management System & Telematics (Oracle OTM, Blue Yonder TMS, Project44, Samsara ELD)",
        breaks: "Trailers leave 28% empty shipping expensive Less-Than-Truckload (LTL) pallets; containers rack up port Demurrage fees; or carriers overbill fuel surcharges and accessorial fees by 6%.",
        agents: "FleetFlow Route & Dispatch (`fleetflow_dispatch`), 3D Load Consolidation Studio (`load_consolidation_agent`), Ocean Port Drayage Orchestrator (`port_drayage_orchestrator`), Multimodal Mode-Shift (`multimodal_mode_shift_agent`), Freight Bill Audit (`freight_bill_audit_agent`), Cold-Chain Auditor (`cold_chain_auditor`)",
        terms: "TMS (Transportation Management System), FTL (Full Truckload) vs. LTL (Less-Than-Truckload), 3D Cube Utilization, LIFO (Last-In, First-Out), Drayage, Demurrage & Detention, BOL (Bill of Lading), ASN (Advance Ship Notice), ELD & HOS"
      }},
      {{
        title: "Stage 6 · 🛒 Customer Delivery (OTIF), Retail Execution, Reverse Returns (RMA) & ESG",
        whyExists: "The final mile — and the reverse loop back! Products must arrive On-Time In-Full (OTIF), get stocked properly on store shelves, handle customer returns (RMA) profitably when items come back, and report carbon emissions (Scope 3) and working capital to leadership.",
        analogy: "🔄 Everyday Analogy: Like delivering an online grocery order inside the exact 1-hour window with a photo receipt — and handling refunds or bottle recycling afterward.",
        story: "1. The truck arrives at the customer dock within the scheduled window, delivers 100% of ordered cases (OTIF — On-Time In-Full), and captures a signed Electronic Proof of Delivery (ePOD).<br/>2. If a retailer unfairly deducts a 3% OTIF penalty or claims OS&D (Over, Short & Damaged), the team uses GPS + ePOD + dock photos to win back the chargeback.<br/>3. Field sales vans replenish local stores (TM&D) and audit shelf compliance (Planogram).<br/>4. When customers initiate a return (RMA), AI calculates whether to refund without return ('Keep-It') or route to refurbishment, while the Control Tower tracks Scope 3 carbon (CBAM/EUDR) and Cash Conversion Cycle (CCC).",
        personas: "Customer OTIF & Chargeback Lead, Reverse Logistics / RMA Manager, Trade Marketing (TM&D) Lead, Chief Supply Chain Officer (CSCO), Sustainability & ESG Officer",
        docs: "ePOD (Electronic Proof of Delivery), OTIF Dispute Dossier, RMA (Return Merchandise Authorization), Scope 3 Carbon & CBAM Certificate",
        software: "Enterprise Control Tower, Retail Execution & Returns Systems (SAP GTS, Loop Returns, Looker / BigQuery Twin)",
        breaks: "Retailers deduct millions in unchallenged OTIF penalties; companies spend $15 in return shipping to take back a $10 item; or sudden port strikes paralyze multiple pillars at once.",
        agents: "CSCO Control Tower Copilot (`csco_control_tower_copilot`), Disruption War-Room (`disruption_war_room_orchestrator`), OTIF Penalty Shield (`otif_penalty_shield`), Keep-It vs. Return Advisor (`keep_it_routing_advisor`), Returns Triage (`returns_triage_agent`), Scope 3 Carbon Ledger (`carbon_scope3_ledger`), Working Capital Cash Bridge (`working_capital_cash_bridge`)",
        terms: "OTIF (On-Time In-Full), ePOD (Electronic Proof of Delivery), OS&D (Over, Short & Damaged), TM&D & Planogram, RMA (Return Merchandise Authorization), Keep-It vs. Return-It, CCC (Cash Conversion Cycle), Scope 1/2/3, CBAM & EUDR"
      }}
    ];

    let currentStageIdx = 0;

    function switchChapter(id, btn) {{
      document.querySelectorAll('.g-pane').forEach(p => p.classList.remove('active'));
      document.querySelectorAll('.g-chap-btn').forEach(b => b.classList.remove('active'));
      document.getElementById(id).classList.add('active');
      if (btn) btn.classList.add('active');
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function stepStage(delta) {{
      const next = (currentStageIdx + delta + STAGES.length) % STAGES.length;
      const btns = document.querySelectorAll('#stageBtnRow .g-btn');
      showStageTable(next, btns[next]);
    }}

    function showStageTable(idx, btn) {{
      currentStageIdx = idx;
      if (btn) {{
        document.querySelectorAll('#stageBtnRow .g-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
      }}
      const s = STAGES[idx];
      document.getElementById('stageTableMount').innerHTML = `
        <div style="display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:14px;">
          <button type="button" class="g-btn" onclick="stepStage(-1)">&larr; Previous Stage</button>
          <strong style="color:#1A73E8; font-size:18px;">Viewing Stage ${{idx}} of 6 (${{idx + 1}} of 7 Total Steps)</strong>
          <button type="button" class="g-btn g-btn-primary" onclick="stepStage(1)">Next Stage &rarr;</button>
        </div>
        <div class="g-table-wrap">
          <table class="g-table">
            <thead>
              <tr>
                <th colspan="2" style="background:#E8F0FE; color:#1A73E8; font-size:18px; padding:18px 22px;">${{s.title}}</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="width:260px; font-weight:700; color:#1A73E8;">🎯 1. What This Stage Is &amp; Why It Exists</td>
                <td style="font-size:17px; font-weight:500;">${{s.whyExists}}</td>
              </tr>
              <tr>
                <td style="font-weight:700; color:#B06000;">💡 2. Everyday Real-Life Analogy</td>
                <td style="font-weight:600; background:#FEF7E0;">${{s.analogy}}</td>
              </tr>
              <tr>
                <td style="font-weight:700; color:#1E8E3E;">📦 3. Step-by-Step What Actually Happens Here</td>
                <td>${{s.story}}</td>
              </tr>
              <tr>
                <td style="font-weight:700; color:#202124;">👥 4. Who Works Here (Human Roles)</td>
                <td>${{s.personas}}</td>
              </tr>
              <tr>
                <td style="font-weight:700; color:#007B83;">📄 5. Key Documents &amp; Data Passed Forward</td>
                <td><strong>${{s.docs}}</strong></td>
              </tr>
              <tr>
                <td style="font-weight:700; color:#9334E6;">💻 6. Software Systems Used</td>
                <td><strong>${{s.software}}</strong></td>
              </tr>
              <tr>
                <td style="font-weight:700; color:#D93025;">⚠️ 7. What Goes Wrong &amp; Why It Costs Millions</td>
                <td style="background:#FCE8E6; color:#C5221F; font-weight:500;">${{s.breaks}}</td>
              </tr>
              <tr>
                <td style="font-weight:700; color:#1E8E3E;">🤖 8. How Our AI Agents Solve It</td>
                <td style="background:#E6F4EA; color:#137333; font-weight:600;">${{s.agents}}</td>
              </tr>
              <tr>
                <td style="font-weight:700; color:#5F6368;">🔤 9. Key Abbreviations in This Stage</td>
                <td><code>${{s.terms}}</code></td>
              </tr>
            </tbody>
          </table>
        </div>
      `;
    }}

    // Bullwhip Table
    let bwAi = false;
    function toggleBwAi() {{
      bwAi = !bwAi;
      const btn = document.getElementById('bwAiBtn');
      btn.textContent = bwAi ? '✨ AI Demand Sensing: ON (Synchronized!)' : '✨ Turn On AI Demand Sensing: OFF';
      btn.style.background = bwAi ? '#E6F4EA' : '#FFFFFF';
      renderBwTable();
    }}
    function renderBwTable() {{
      const pos = Number(document.getElementById('bwRange').value);
      document.getElementById('bwValLabel').textContent = `+${{pos}}%`;
      const mults = bwAi ? [1.0, 1.08, 1.15, 1.22, 1.28] : [1.0, 1.8, 3.2, 5.2, 7.5];
      const names = [
        ["1. Store Checkout (POS)", "Customers buy slightly more on a warm weekend."],
        ["2. Store Manager Order", bwAi ? "Shared live via CPFR — no panic padding." : "Manager panics and pads order to avoid running out."],
        ["3. Local Warehouse (FDC)", bwAi ? "MEIO adjusts buffer smoothly." : "Sees spiky store orders and doubles safety buffer."],
        ["4. Factory Production Line", bwAi ? "Runs steady shift schedule." : "Turns on expensive weekend overtime shifts."],
        ["5. Raw Material Supplier", bwAi ? "Steady raw material pulls." : "Sees massive fake boom, followed by order cancellations!"]
      ];
      const rows = names.map((n, i) => {{
        const val = Math.round(pos * mults[i]);
        const barW = Math.min(100, Math.round(val / 1.8));
        const col = bwAi ? '#1E8E3E' : (i >= 3 ? '#D93025' : (i >= 1 ? '#F9AB00' : '#1A73E8'));
        return `<tr>
          <td style="font-weight:700; width:230px;">${{n[0]}}</td>
          <td style="width:120px; font-weight:800; color:${{col}}; font-size:18px;">+${{val}}%</td>
          <td style="width:280px;">
            <div style="background:#F1F3F4; height:18px; border-radius:999px; overflow:hidden;">
              <div style="width:${{barW}}%; height:100%; background:${{col}}; border-radius:999px;"></div>
            </div>
          </td>
          <td>${{n[1]}}</td>
        </tr>`;
      }}).join('');
      document.getElementById('bwTableMount').innerHTML = `
        <div class="g-table-wrap">
          <table class="g-table">
            <thead><tr><th>Supply Chain Stage</th><th>Order Spike</th><th>Visual Wave Size</th><th>Why This Happens</th></tr></thead>
            <tbody>${{rows}}</tbody>
          </table>
        </div>
      `;
    }}

    // 4 Core Concept Diagrams (One at a Time)
    function showConceptDiagram(idx, btn) {{
      if (btn) {{
        btn.parentElement.querySelectorAll('.g-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
      }}
      const mount = document.getElementById('conceptDiagramMount');
      if (idx === 0) {{
        mount.innerHTML = `
          <svg viewBox="0 0 920 140" style="width:100%; height:auto; display:block; margin-bottom:20px; background:#F8F9FA; border-radius:16px; border:1px solid #DADCE0;">
            <rect x="20" y="20" width="420" height="100" rx="14" fill="#E8F0FE" stroke="#1A73E8" stroke-width="2"/>
            <text x="230" y="52" text-anchor="middle" fill="#1A73E8" font-size="15" font-weight="800">MAKE-TO-STOCK (MTS · PUSH STRATEGY)</text>
            <text x="230" y="80" text-anchor="middle" fill="#202124" font-size="14" font-weight="600">Forecast &rarr; Manufacture Early &rarr; Hold in Warehouse &rarr; Instant Ship</text>
            <text x="230" y="104" text-anchor="middle" fill="#5F6368" font-size="12.5">Examples: Toothpaste, Soda, AA Batteries</text>

            <rect x="480" y="20" width="420" height="100" rx="14" fill="#E6F4EA" stroke="#1E8E3E" stroke-width="2"/>
            <text x="690" y="52" text-anchor="middle" fill="#1E8E3E" font-size="15" font-weight="800">MAKE-TO-ORDER (MTO · PULL STRATEGY)</text>
            <text x="690" y="80" text-anchor="middle" fill="#202124" font-size="14" font-weight="600">Wait for Customer Order &rarr; Custom Build &rarr; Ship Direct</text>
            <text x="690" y="104" text-anchor="middle" fill="#5F6368" font-size="12.5">Examples: Custom Dell Server, Boeing Jet, Custom Suit</text>
          </svg>
          <div class="g-table-wrap">
            <table class="g-table">
              <thead><tr><th>Strategy</th><th>Full Name</th><th>How It Works</th><th>Biggest Risk</th></tr></thead>
              <tbody>
                <tr><td><strong style="color:#1A73E8;">MTS</strong></td><td>Make-to-Stock</td><td>Factory builds goods in advance based on a forecast and stacks them in warehouses.</td><td>If the forecast is wrong, you get stuck with unsold dead stock (<strong>SLOB</strong>).</td></tr>
                <tr><td><strong style="color:#1E8E3E;">MTO</strong></td><td>Make-to-Order</td><td>Factory waits until a customer actually places a firm order before building it.</td><td>Customer has to wait longer (lead time), and raw component shortages delay delivery.</td></tr>
              </tbody>
            </table>
          </div>
        `;
      }} else if (idx === 1) {{
        mount.innerHTML = `
          <svg viewBox="0 0 920 140" style="width:100%; height:auto; display:block; margin-bottom:20px; background:#F8F9FA; border-radius:16px; border:1px solid #DADCE0;">
            <rect x="20" y="20" width="280" height="100" rx="14" fill="#FCE8E6" stroke="#D93025" stroke-width="2"/>
            <text x="160" y="50" text-anchor="middle" fill="#D93025" font-size="15" font-weight="800">1. FEFO (First-Expired, First-Out)</text>
            <text x="160" y="78" text-anchor="middle" fill="#202124" font-size="13.5" font-weight="600">🥛 Ship batch expiring soonest first</text>
            <text x="160" y="102" text-anchor="middle" fill="#5F6368" font-size="12">Used for Food, Dairy, Vaccines, Pharma</text>

            <rect x="320" y="20" width="280" height="100" rx="14" fill="#E6F4EA" stroke="#1E8E3E" stroke-width="2"/>
            <text x="460" y="50" text-anchor="middle" fill="#1E8E3E" font-size="15" font-weight="800">2. FIFO (First-In, First-Out)</text>
            <text x="460" y="78" text-anchor="middle" fill="#202124" font-size="13.5" font-weight="600">📦 Ship oldest arrived pallet first</text>
            <text x="460" y="102" text-anchor="middle" fill="#5F6368" font-size="12">Used for Electronics, Apparel, Hardware</text>

            <rect x="620" y="20" width="280" height="100" rx="14" fill="#E8F0FE" stroke="#1A73E8" stroke-width="2"/>
            <text x="760" y="50" text-anchor="middle" fill="#1A73E8" font-size="15" font-weight="800">3. LIFO (Last-In, First-Out)</text>
            <text x="760" y="78" text-anchor="middle" fill="#202124" font-size="13.5" font-weight="600">🚚 Load Delivery Stop #1 LAST</text>
            <text x="760" y="102" text-anchor="middle" fill="#5F6368" font-size="12">So Stop #1 sits right at the rear truck doors!</text>
          </svg>
          <div class="g-table-wrap">
            <table class="g-table">
              <thead><tr><th>Rule</th><th>Full Name</th><th>Everyday Meaning</th><th>Which Agent Uses It</th></tr></thead>
              <tbody>
                <tr><td><strong style="color:#D93025;">FEFO</strong></td><td>First-Expired, First-Out</td><td>Always ship the batch whose expiration date is closest so nothing spoils in the warehouse.</td><td><code>short_dated_redistributor</code> &amp; <code>dynamic_markdown_agent</code></td></tr>
                <tr><td><strong style="color:#1E8E3E;">FIFO</strong></td><td>First-In, First-Out</td><td>Ship the pallet that arrived earliest so boxes don't gather dust in the back of the rack.</td><td><code>warehouse_slotting_agent</code></td></tr>
                <tr><td><strong style="color:#1A73E8;">LIFO</strong></td><td>Last-In, First-Out</td><td>When loading a multi-stop delivery truck, put Stop #3 in the nose first and Stop #1 in the tail last.</td><td><code>load_consolidation_agent</code> (CubeMaster 3D)</td></tr>
              </tbody>
            </table>
          </div>
        `;
      }} else if (idx === 2) {{
        mount.innerHTML = `
          <svg viewBox="0 0 920 140" style="width:100%; height:auto; display:block; margin-bottom:20px; background:#F8F9FA; border-radius:16px; border:1px solid #DADCE0;">
            <rect x="20" y="24" width="260" height="92" rx="14" fill="#E8F0FE" stroke="#1A73E8" stroke-width="2"/>
            <text x="150" y="56" text-anchor="middle" fill="#1A73E8" font-size="15" font-weight="800">+ DIO (55 Days)</text>
            <text x="150" y="82" text-anchor="middle" fill="#202124" font-size="13">Days Inventory sits in Warehouse</text>

            <rect x="300" y="24" width="260" height="92" rx="14" fill="#FEF7E0" stroke="#F9AB00" stroke-width="2"/>
            <text x="430" y="56" text-anchor="middle" fill="#B06000" font-size="15" font-weight="800">+ DSO (40 Days)</text>
            <text x="430" y="82" text-anchor="middle" fill="#202124" font-size="13">Days Customer takes to pay you</text>

            <rect x="580" y="24" width="320" height="92" rx="14" fill="#E6F4EA" stroke="#1E8E3E" stroke-width="2"/>
            <text x="740" y="56" text-anchor="middle" fill="#1E8E3E" font-size="15" font-weight="800">− DPO (45 Days) = 50 Days CCC</text>
            <text x="740" y="82" text-anchor="middle" fill="#202124" font-size="13">Minus Days you take to pay Suppliers</text>
          </svg>
          <div class="g-table-wrap">
            <table class="g-table">
              <thead><tr><th>Term</th><th>Full Name</th><th>Plain-English Meaning</th></tr></thead>
              <tbody>
                <tr><td><strong>DIO</strong></td><td>Days Inventory Outstanding</td><td>How many days cash sits tied up as physical boxes on warehouse shelves before being sold (lower is better).</td></tr>
                <tr><td><strong>DSO</strong></td><td>Days Sales Outstanding</td><td>How many days it takes to collect cash from customers after you ship their order (lower is better).</td></tr>
                <tr><td><strong>DPO</strong></td><td>Days Payable Outstanding</td><td>How many days you wait before paying your suppliers' invoices (higher keeps cash in your bank longer).</td></tr>
                <tr><td><strong style="color:#1A73E8;">CCC</strong></td><td>Cash Conversion Cycle (<code>DIO + DSO − DPO</code>)</td><td>Total days a dollar is trapped in your supply chain. Cutting CCC by 5 days frees tens of millions in cash!</td></tr>
              </tbody>
            </table>
          </div>
        `;
      }} else {{
        mount.innerHTML = `
          <svg viewBox="0 0 920 140" style="width:100%; height:auto; display:block; margin-bottom:20px; background:#F8F9FA; border-radius:16px; border:1px solid #DADCE0;">
            <rect x="20" y="24" width="210" height="92" rx="14" fill="#F1F3F4" stroke="#5F6368" stroke-width="2"/>
            <text x="125" y="56" text-anchor="middle" fill="#202124" font-size="15" font-weight="800">SCOPE 1 (~8%)</text>
            <text x="125" y="82" text-anchor="middle" fill="#5F6368" font-size="13">Your own factory boilers &amp; vans</text>

            <rect x="250" y="24" width="210" height="92" rx="14" fill="#E8F0FE" stroke="#1A73E8" stroke-width="2"/>
            <text x="355" y="56" text-anchor="middle" fill="#1A73E8" font-size="15" font-weight="800">SCOPE 2 (~7%)</text>
            <text x="355" y="82" text-anchor="middle" fill="#202124" font-size="13">Purchased grid electricity</text>

            <rect x="480" y="24" width="420" height="92" rx="14" fill="#E6F4EA" stroke="#1E8E3E" stroke-width="2"/>
            <text x="690" y="56" text-anchor="middle" fill="#1E8E3E" font-size="15" font-weight="800">SCOPE 3 · SUPPLY CHAIN (85% OF TOTAL!)</text>
            <text x="690" y="82" text-anchor="middle" fill="#202124" font-size="13">All upstream suppliers + ocean/air/truck freight (CBAM &amp; EUDR)</text>
          </svg>
          <div class="g-table-wrap">
            <table class="g-table">
              <thead><tr><th>Term</th><th>Full Name</th><th>Why Customers Care</th></tr></thead>
              <tbody>
                <tr><td><strong>Scope 1 &amp; 2</strong></td><td>Direct Fuel &amp; Purchased Electricity</td><td>Emissions from burning fuel in your own buildings/trucks (Scope 1) and buying utility power (Scope 2).</td></tr>
                <tr><td><strong style="color:#1E8E3E;">Scope 3</strong></td><td>Value Chain Emissions (Suppliers + Freight)</td><td>Makes up 80–90% of a company's carbon footprint! Tracked by our <code>carbon_scope3_ledger</code> agent.</td></tr>
                <tr><td><strong>CBAM &amp; EUDR</strong></td><td>Carbon Border Adjustment &amp; Deforestation Rules</td><td>European laws that tax carbon-heavy imports (CBAM) and block goods from deforested land (EUDR).</td></tr>
              </tbody>
            </table>
          </div>
        `;
      }}
    }}

    // Chapter 3: Workflows rendered as Clean Spacious Tables
    function selectWorkflow(wfKey, btn) {{
      if (btn) {{
        btn.parentElement.querySelectorAll('.g-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
      }}
      const wf = WORKFLOWS[wfKey];
      const rows = wf.steps.map(st => `
        <tr>
          <td style="font-weight:800; color:#1A73E8; width:210px;">${{st.badge}}<br/><span style="color:#202124; font-size:15.5px;">${{st.title}}</span></td>
          <td>${{st.plain}}</td>
          <td style="background:#FCE8E6; color:#C5221F; font-weight:500;">✕ ${{st.manual}}</td>
          <td style="background:#E6F4EA; color:#137333; font-weight:600;">✦ ${{st.ai}}</td>
        </tr>
      `).join('');
      document.getElementById('workflowMount').innerHTML = `
        <h3 style="font-family:var(--font-display); font-size:23px; margin:0 0 6px; color:#1A73E8;">${{wf.title}}</h3>
        <p style="color:var(--text-sub); margin:0 0 16px;">${{wf.subtitle}}</p>
        <div class="g-table-wrap">
          <table class="g-table">
            <thead>
              <tr>
                <th>Step</th>
                <th>What Happens in Plain English</th>
                <th>✕ Old Manual Bottleneck</th>
                <th>✦ With Our AI Agent</th>
              </tr>
            </thead>
            <tbody>${{rows}}</tbody>
          </table>
        </div>
      `;
    }}

    // Chapter 4: Terms (One-by-One Card Mode OR Clean Table Mode)
    let termsMode = 'one';
    let termsFilter = 'all';
    let termIdx = 0;

    function getFilteredTerms() {{
      return FLASHCARDS.filter(fc => {{
        if (termsFilter === 'all') return true;
        if (termsFilter === 'top15') return fc.top15;
        return fc.cat === termsFilter;
      }});
    }}

    function setTermsMode(m) {{
      termsMode = m;
      document.getElementById('modeOneBtn').classList.toggle('active', m === 'one');
      document.getElementById('modeTableBtn').classList.toggle('active', m === 'table');
      renderTerms();
    }}

    function filterTerms(cat, btn) {{
      termsFilter = cat;
      termIdx = 0;
      if (btn) {{
        btn.parentElement.querySelectorAll('.g-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
      }}
      renderTerms();
    }}

    function stepTerm(delta) {{
      const list = getFilteredTerms();
      termIdx = (termIdx + delta + list.length) % list.length;
      renderTerms();
    }}

    function renderTerms() {{
      const list = getFilteredTerms();
      const mount = document.getElementById('termsMount');
      if (termsMode === 'one') {{
        const fc = list[termIdx] || list[0];
        mount.innerHTML = `
          <div style="display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:18px;">
            <button type="button" class="g-btn" onclick="stepTerm(-1)">&larr; Previous Term</button>
            <div style="font-family:var(--font-display); font-size:19px; font-weight:700; color:#1A73E8;">
              Term ${{termIdx + 1}} of ${{list.length}}
            </div>
            <button type="button" class="g-btn g-btn-primary" onclick="stepTerm(1)">Next Term &rarr;</button>
          </div>

          <div style="background:#F8F9FA; border:2px solid #4285F4; border-radius:20px; padding:30px 34px;">
            <div style="display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap; margin-bottom:10px;">
              <span class="g-badge" style="background:#E8F0FE; color:#1A73E8; margin:0;">${{fc.catLabel}}</span>
              ${{fc.top15 ? '<span class="g-badge" style="background:#FEF7E0; color:#B06000; margin:0;">⭐ Top 15 Must-Know</span>' : ''}}
            </div>
            <h3 style="font-family:var(--font-display); font-size:34px; margin:6px 0 4px; color:#202124;">
              ${{fc.term}}
            </h3>
            <div style="font-size:19px; font-weight:700; color:#1E8E3E; margin-bottom:22px;">
              Full Name: ${{fc.full}}
            </div>

            <div class="g-table-wrap">
              <table class="g-table">
                <tbody>
                  <tr>
                    <th style="width:240px;">📖 Plain-English Meaning</th>
                    <td style="font-size:17.5px; font-weight:600;">${{fc.simple}}</td>
                  </tr>
                  <tr>
                    <th>💡 Concrete Real-World Example</th>
                    <td>${{fc.example}}</td>
                  </tr>
                  <tr>
                    <th>💰 Why Customers Care</th>
                    <td>${{fc.whyCare}}</td>
                  </tr>
                  <tr>
                    <th>🤖 Which AI Agent Uses It</th>
                    <td><strong style="color:#1A73E8;">${{fc.agent}}</strong></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        `;
      }} else {{
        const rows = list.map((fc, i) => `
          <tr>
            <td style="font-weight:800; color:#1A73E8; width:160px;">${{i+1}}. ${{fc.term}}</td>
            <td style="font-weight:700; color:#1E8E3E; width:220px;">${{fc.full}}</td>
            <td>${{fc.simple}}</td>
            <td>${{fc.example}}</td>
            <td style="font-weight:600; color:#9334E6; width:210px;">${{fc.agent}}</td>
          </tr>
        `).join('');
        mount.innerHTML = `
          <div class="g-table-wrap">
            <table class="g-table">
              <thead>
                <tr>
                  <th>Term</th>
                  <th>Full Spelled-Out Name</th>
                  <th>Simple Meaning</th>
                  <th>Real-World Example</th>
                  <th>AI Agent</th>
                </tr>
              </thead>
              <tbody>${{rows}}</tbody>
            </table>
          </div>
        `;
      }}
    }}

    // Chapter 5: Decoder Table & 1-by-1 Quiz
    function renderDecoderTable() {{
      const rows = DECODER.map((d, i) => `
        <tr>
          <td style="font-weight:700; color:#D93025; width:270px;">${{i+1}}. ${{d.complaint}}</td>
          <td>${{d.meaning}}</td>
          <td style="font-weight:700; color:#1E8E3E; width:230px;">${{d.agents}}</td>
          <td style="color:#1A73E8; font-weight:600;">${{d.question}}</td>
        </tr>
      `).join('');
      document.getElementById('decoderTableMount').innerHTML = `
        <thead>
          <tr>
            <th>When Customer Says…</th>
            <th>What It Means in Plain English</th>
            <th>Which AI Agent to Show</th>
            <th>Smart Follow-Up Question</th>
          </tr>
        </thead>
        <tbody>${{rows}}</tbody>
      `;
    }}

    let qIdx = 0;
    function stepQuiz(delta) {{
      qIdx = (qIdx + delta + QUIZ.length) % QUIZ.length;
      renderOneQuiz();
    }}
    function renderOneQuiz() {{
      const q = QUIZ[qIdx];
      const opts = q.options.map((o, oi) => `
        <button type="button" class="g-btn" style="width:100%; justify-content:flex-start; padding:16px 20px; border-radius:14px; margin-bottom:10px; font-size:16.5px; text-align:left;" onclick="answerOneQuiz(${{oi}}, this)">
          <strong>${{String.fromCharCode(65 + oi)}}.</strong> ${{o}}
        </button>
      `).join('');
      document.getElementById('quizOneMount').innerHTML = `
        <div style="display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:16px;">
          <button type="button" class="g-btn" onclick="stepQuiz(-1)">&larr; Previous Question</button>
          <strong style="color:#1A73E8; font-size:18px;">Question ${{qIdx + 1}} of ${{QUIZ.length}}</strong>
          <button type="button" class="g-btn g-btn-primary" onclick="stepQuiz(1)">Next Question &rarr;</button>
        </div>
        <h3 style="font-family:var(--font-display); font-size:22px; margin:0 0 16px;">${{q.q}}</h3>
        <div>${{opts}}</div>
        <div id="quizFeedbackBox" style="display:none; margin-top:16px; padding:18px 22px; border-radius:14px; font-weight:600;"></div>
      `;
    }}
    function answerOneQuiz(oi, btn) {{
      const q = QUIZ[qIdx];
      const fb = document.getElementById('quizFeedbackBox');
      fb.style.display = 'block';
      if (oi === q.correct) {{
        btn.style.background = '#E6F4EA';
        btn.style.borderColor = '#1E8E3E';
        btn.style.color = '#137333';
        fb.style.background = '#E6F4EA';
        fb.style.color = '#137333';
        fb.innerHTML = '✅ ' + q.explain;
      }} else {{
        btn.style.background = '#FCE8E6';
        btn.style.borderColor = '#D93025';
        btn.style.color = '#C5221F';
        fb.style.background = '#FCE8E6';
        fb.style.color = '#C5221F';
        fb.innerHTML = '✕ Not quite — try another option! (' + q.explain + ')';
      }}
    }}

    showStageTable(0);
    renderBwTable();
    showConceptDiagram(0);
    selectWorkflow('sop');
    renderTerms();
    renderDecoderTable();
    renderOneQuiz();
  </script>
</body>
</html>
"""
    out_path = ROOT / "supply_chain_101_interactive_academy.html"
    out_path.write_text(html_doc, encoding="utf-8")
    print(f"Rebuilt Google clean {out_path.name} ({len(html_doc)//1024} KB)")


if __name__ == "__main__":
    build_google_linear_playbook()
    build_google_linear_academy()

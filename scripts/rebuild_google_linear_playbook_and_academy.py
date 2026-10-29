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
        "subtitle": "How a company aligns Sales forecasts, Factory capacity, and Finance budgets every month so everyone works from one plan:",
        "company_case": "🌍 Real-World Company Spotlight: How Unilever, PepsiCo & Mondelēz Run Monthly S&OP Across 190+ Countries",
        "company_summary": "Every month, consumer giants like Unilever (Dove soap, Magnum ice cream) and PepsiCo align 100,000+ store checkout feeds with 300+ factories so a heatwave in Europe or a Super Bowl promotion in the US never leaves supermarket shelves empty.",
        "steps": [
            {
                "badge": "Step 1 · Data Gathering",
                "title": "Pull Past Sales, POS (Point of Sale — store checkout scans) & Weather",
                "plain": "Collect what retail stores actually sold at the cash register last month, plus upcoming price promotions and local weather forecasts.",
                "real_world": "PepsiCo & Unilever pull daily Point of Sale (POS) scanner data from Walmart, Tesco, and Carrefour plus 14-day weather forecasts (because a +5°C warmer weekend spikes cold beverage & ice cream sales by +28%).",
                "manual": "Analysts spend 5 days downloading CSV spreadsheets and fixing broken Excel formulas.",
                "ai": "Demand Sensing Agent pulls live POS (Point of Sale) scans & weather automatically in seconds.",
            },
            {
                "badge": "Step 2 · Demand Plan",
                "title": "Agree on What Customers Will Buy & Check FVA (Forecast Value Added)",
                "plain": "Create a statistical baseline forecast and check whether human salesperson edits actually improved accuracy or hurt it — called FVA (Forecast Value Added).",
                "real_world": "At Nestl\u00e9 & P&G, regional sales managers often pad forecasts by +20% before a holiday 'just in case'. Measuring FVA (Forecast Value Added) exposes which manual overrides add value vs. which ones create unsold warehouse clutter.",
                "manual": "Sales reps pad forecasts by +20% 'just in case', creating negative FVA (Forecast Value Added).",
                "ai": "Flags biased manual overrides and harmonizes joint retailer CPFR (Collaborative Planning, Forecasting & Replenishment) forecasts.",
            },
            {
                "badge": "Step 3 · Supply & Factory Check",
                "title": "Check If Factories & Suppliers Can Build It (Checking OEE — Machine Uptime)",
                "plain": "Compare the demand forecast against real factory line hours, machine OEE (Overall Equipment Effectiveness — uptime & speed %), and raw material supplier stock.",
                "real_world": "Before locking a summer beverage plan, Coca-Cola & ITC check if their high-speed bottling lines have enough OEE (Overall Equipment Effectiveness) capacity and whether aluminum can & sugar suppliers can deliver on time.",
                "manual": "Planners discover 2 weeks too late that a factory line is booked or a supplier is short.",
                "ai": "Finite Production Scheduler & Tier-N Risk Sentinel flag capacity and component bottlenecks weeks early.",
            },
            {
                "badge": "Step 4 · Pre-S&OP Trade-Offs",
                "title": "Solve Gaps (Overtime vs. Air Freight vs. Profit Margin vs. OTIF Service)",
                "plain": "When demand beats capacity, simulate options: run weekend factory overtime, hire contract packers, or shift stock while protecting OTIF (On-Time In-Full delivery).",
                "real_world": "When demand for Sony PlayStation or Apple AirPods spikes 35% above plan, executives compare the profit margin impact of chartering air cargo vs. running 3rd-shift factory overtime in a 30-minute trade-off review.",
                "manual": "Teams argue in meetings with no live math on profit margin vs. OTIF (On-Time In-Full) service impact.",
                "ai": "S&OP Scenario Weaver simulates 3 cost/margin/OTIF service options in 10 seconds.",
            },
            {
                "badge": "Step 5 · Executive Sign-Off",
                "title": "Lock the One-Number Plan into ERP (Enterprise Resource Planning)",
                "plain": "Leadership approves the final plan and publishes firm production & buying targets into ERP (Enterprise Resource Planning — corporate software like SAP).",
                "real_world": "Once the Chief Supply Chain Officer (CSCO) and Chief Financial Officer (CFO) sign off at Procter & Gamble, SAP ERP automatically releases raw material Purchase Orders (POs) and factory build schedules worldwide.",
                "manual": "Manual re-keying into ERP takes days; the plan is already stale before execution starts.",
                "ai": "1-click governed write-back locks the consensus plan across ERP (Head Office), MES (Factory), and WMS (Warehouse).",
            },
        ],
    },
    "match3": {
        "title": "2 · Paying Suppliers: The 3-Way Invoice Match (4 Steps)",
        "subtitle": "How Procurement & Accounts Payable make sure the company never overpays a supplier bill by matching 3 documents (PO + GRN + Invoice):",
        "company_case": "🌍 Real-World Company Spotlight: How Toyota, Target & Walmart Verify Millions of Supplier Invoices Without Overpaying",
        "company_summary": "Large manufacturers and retailers receive 50,000+ supplier invoices every week. By strictly matching Document #1 (Purchase Order / PO), Document #2 (Warehouse Goods Receipt Note / GRN), and Document #3 (Vendor Invoice), they prevent tens of millions in billing errors and short-shipments.",
        "steps": [
            {
                "badge": "Step 1 · Document #1 (PO)",
                "title": "Check the Original PO (Purchase Order — Our Official Buyer Contract)",
                "plain": "Look up what unit price and quantity our buyer officially agreed to pay on the PO (Purchase Order) — e.g., 1,000 units @ $10.00 = $10,000.",
                "real_world": "Toyota's procurement system issues a firm PO (Purchase Order) to a brake-pad supplier (e.g., Bosch or Denso) specifying 1,000 brake assemblies at an agreed contract price of $10.00 each.",
                "manual": "Accounts Payable clerk manually searches SAP ERP for the PO number typed on a PDF invoice.",
                "ai": "Three-Way Match Agent extracts the PO (Purchase Order) line items automatically.",
            },
            {
                "badge": "Step 2 · Document #2 (GRN)",
                "title": "Check the Warehouse GRN (Goods Receipt Note — What Actually Arrived at the Dock)",
                "plain": "Check what the warehouse receiving dock actually unloaded and scanned on the GRN (Goods Receipt Note) — e.g., only 960 units arrived; 40 were missing!",
                "real_world": "When the supplier's truck backs into Target's or Toyota's receiving dock, workers scan every pallet barcode into the WMS (Warehouse Management System), generating a GRN (Goods Receipt Note) showing only 960 units were physically inside the trailer.",
                "manual": "Clerk emails the warehouse manager and waits 3 days to confirm the physical dock count.",
                "ai": "Instantly cross-checks WMS (Warehouse Management System) dock barcode scans (GRN) against the PO.",
            },
            {
                "badge": "Step 3 · Document #3 (Invoice)",
                "title": "Compare Supplier Invoice Against PO (Purchase Order) & GRN (Goods Receipt Note)",
                "plain": "The vendor billed $10,500 (1,000 units @ $10.50) — both unit price (+$0.50 higher) and quantity (+40 missing units) are wrong!",
                "real_world": "In fast-moving consumer goods (Unilever / Kraft Heinz), resin or packaging vendors frequently bill outdated price tiers or full truckload quantities even when 2 pallets were left behind at the factory.",
                "manual": "Invoice sits blocked in an exception queue for weeks while teams argue over email.",
                "ai": "Pinpoints the exact $500 price variance + $400 short-shipment discrepancy ($900 total overcharge).",
            },
            {
                "badge": "Step 4 · Auto-Debit & Release",
                "title": "Issue Automated Debit Memo & Pay the Exact Verified Amount ($9,600)",
                "plain": "Block the $900 overcharge, send an automated debit memo with dock scan proof, and pay the valid $9,600 (960 units @ $10.00) on time.",
                "real_world": "Walmart and Amazon automatically deduct short-shipped quantities via an electronic Debit Memo with attached GRN (Goods Receipt Note) barcode logs and release the exact $9,600 payment on the agreed DPO (Days Payable Outstanding) date.",
                "manual": "Late payment causes supplier credit hold, or rubber-stamping causes a $900 cash loss.",
                "ai": "Issues a signed debit memo and releases the exact verified payment amount on time.",
            },
        ],
    },
    "wms_flow": {
        "title": "3 · Inside the Warehouse: Inbound Dock to Outbound Truck (5 Steps)",
        "subtitle": "How pallets move through the 4 walls of a Distribution Center using a WMS (Warehouse Management System):",
        "company_case": "🌍 Real-World Company Spotlight: Inside an Amazon Fulfillment Center, Sysco Food Hub & Pfizer Cold-Chain Depot",
        "company_summary": "A modern distribution center is like a high-speed airport for boxes. Companies like Amazon, Sysco (restaurant food distribution), and DHL process 100+ trucks a day — unloading, checking quality, slotting fast movers, picking by expiration date (FEFO), and packing outbound trailers in reverse stop order (LIFO).",
        "steps": [
            {
                "badge": "Step 1 · Yard & Dock Arrival",
                "title": "Assign Incoming Truck to the Best Unloading Dock Door",
                "plain": "A supplier truck arrives at the security gate and needs an open dock door near the rack zone where its goods belong.",
                "real_world": "At Walmart and DHL mega-hubs with 150+ dock doors, live GPS telematics assigns an incoming refrigerated dairy truck to Cold-Dock Door #14 zero minutes after arrival so the driver never waits in line.",
                "manual": "Trucks wait 3 hours in yard queues, triggering $150/hr carrier detention penalties.",
                "ai": "Yard & Dock Sequencer assigns the optimal door dynamically from live GPS arrival time.",
            },
            {
                "badge": "Step 2 · Dock-to-Stock & QA",
                "title": "Scan Pallets (GRN — Goods Receipt Note) & Check Quality / Cold-Chain",
                "plain": "Unload pallets, scan barcodes to create the GRN (Goods Receipt Note), and verify temperature logs before releasing stock for sale.",
                "real_world": "At Pfizer (vaccines) and Amul (chilled dairy), workers plug in the truck's digital temperature logger at the dock; if the trailer stayed between 2°C and 8°C for the entire trip, the batch is cleared into saleable stock in minutes.",
                "manual": "Pallets sit on the dock floor for 28 hours waiting for manual paper clipboard checks.",
                "ai": "Dock-to-Stock & Cold-Chain Auditors clear good pallets into active inventory in under 2 hours.",
            },
            {
                "badge": "Step 3 · Dynamic Slotting",
                "title": "Put Fast-Selling SKUs (Stock Keeping Units) in Golden-Zone Bins",
                "plain": "Store high-velocity SKUs (Stock Keeping Units — individual product items) at waist height right near the outbound shipping doors to minimize walking and forklift travel.",
                "real_world": "Before Prime Day or Black Friday, Amazon and Nike re-slot their top 500 fastest-selling items into 'Golden Zone' waist-high bins right next to packing stations, cutting picker walking distance by 40%.",
                "manual": "Static bin maps leave workers walking 8 extra miles a day into high back aisles.",
                "ai": "Warehouse Slotting Optimizer re-slots fast movers automatically before peak waves.",
            },
            {
                "badge": "Step 4 · Wave Picking (FEFO)",
                "title": "Batch Customer Orders & Pick Earliest-Expiring Stock (FEFO — First-Expired, First-Out)",
                "plain": "Release picking waves to handheld barcode scanners enforcing FEFO (First-Expired, First-Out — shipping the batch whose expiration date is closest first).",
                "real_world": "At Sysco, Nestlé, and grocery hubs, handheld WMS (Warehouse Management System) scanners force pickers to scan the yogurt pallet expiring May 12 before touching the pallet expiring May 25 (strict FEFO).",
                "manual": "Pickers grab whichever pallet is closest, leaving older batches in the back to expire.",
                "ai": "Wave Fulfillment Copilot balances zone labor and enforces strict FEFO (First-Expired, First-Out).",
            },
            {
                "badge": "Step 5 · 3D LIFO Truck Loading",
                "title": "Pack the Outbound 53-Foot Trailer in Stop Order (LIFO — Last-In, First-Out)",
                "plain": "Stack pallets safely by crush resistance, highway axle weight, and LIFO (Last-In, First-Out — loading Stop #1 last at the rear doors so it unloads first).",
                "real_world": "A Sysco or Coca-Cola delivery truck making 6 restaurant/store stops loads Stop #6 deep in the nose of the trailer first, and loads Stop #1 last right at the tail doors (LIFO) with heavy cans on the floor and fragile chips on top.",
                "manual": "Trailers leave 25% empty, or drivers have to dig behind 10 pallets at Stop #1.",
                "ai": "3D Load Consolidation Studio builds axle-legal LIFO (Last-In, First-Out) load blueprints.",
            },
        ],
    },
    "otif_flow": {
        "title": "4 · Customer Order to On-Time In-Full (OTIF) Delivery (5 Steps)",
        "subtitle": "How a customer order is promised, routed, tracked, and delivered On-Time In-Full (OTIF) without retailer penalty fines:",
        "company_case": "🌍 Real-World Company Spotlight: How P&G, Kraft Heinz & Unilever Hit Walmart's Strict 98% OTIF (On-Time In-Full) Mandate",
        "company_summary": "Big retailers like Walmart, Target, and Kroger fine suppliers 3% of the order value if a truck arrives outside its 2-hour appointment window or is missing even a few cases. Here is how top companies achieve 98%+ OTIF (On-Time In-Full):",
        "steps": [
            {
                "badge": "Step 1 · Order Promising (ATP)",
                "title": "Promise an Accurate Delivery Date Using ATP (Available-to-Promise)",
                "plain": "Check real-time ATP (Available-to-Promise — uncommitted sellable stock) across warehouses and reserve stock for high-priority orders.",
                "real_world": "When Walmart places a 5,000-case order with Procter & Gamble (Tide detergent), P&G's ATP (Available-to-Promise) rules protect strategic retail buffer so a small spot order doesn't accidentally drain Walmart's stock.",
                "manual": "First-come-first-served rules let low-margin orders drain VIP customer stock.",
                "ai": "ATP Order Promising Agent allocates stock from the best warehouse node in under 50 milliseconds.",
            },
            {
                "badge": "Step 2 · Mode & Carrier Selection",
                "title": "Choose FTL (Full Truckload), Intermodal Rail, or LTL (Less-Than-Truckload)",
                "plain": "Pick the lowest-cost transport mode — FTL (Full Truckload — full 53-ft truck), rail, or LTL (Less-Than-Truckload — shared pallet space) — that meets the delivery window.",
                "real_world": "Nike and Samsung combine multiple smaller LTL (Less-Than-Truckload) shipments heading to the same city into a single consolidated FTL (Full Truckload) or intermodal rail move, cutting freight cost by 22%.",
                "manual": "Planners book expensive last-minute air freight or LTL (Less-Than-Truckload) out of habit.",
                "ai": "Multimodal Mode-Shift & FleetFlow optimize multi-stop routes and mode choices.",
            },
            {
                "badge": "Step 3 · In-Transit Tracking",
                "title": "Watch Live GPS, Weather & Driver ELD / HOS (Electronic Logging / Hours of Service)",
                "plain": "Track the truck along the highway and check driver ELD (Electronic Logging Device) and HOS (Hours of Service — legal driving limits) to spot delays 48 hours early.",
                "real_world": "If a winter storm slows I-80 and the truck driver only has 2 hours left on their federal HOS (Hours of Service) clock on the cab's ELD (Electronic Logging Device), Nestlé's Control Tower swaps in a relay driver to save the appointment.",
                "manual": "Nobody knows a shipment is stuck on the highway until the customer calls angry.",
                "ai": "Freight Control Tower & OTIF Shield flag at-risk loads 48 hours early and re-route.",
            },
            {
                "badge": "Step 4 · Delivery & ePOD",
                "title": "Arrive Inside Appointment Window & Capture ePOD (Electronic Proof of Delivery)",
                "plain": "Deliver 100% of ordered cases on time — achieving OTIF (On-Time In-Full) — and capture timestamped GPS + ePOD (Electronic Proof of Delivery).",
                "real_world": "When a FedEx, UPS, or JB Hunt driver backs into a Kroger dock at 08:14 AM for an 08:00–10:00 AM window, geofence GPS + a tablet signature creates an tamper-proof ePOD (Electronic Proof of Delivery) and BOL (Bill of Lading) archive.",
                "manual": "Paper delivery slips get lost in truck cabs, leaving no proof when retailers claim late arrival.",
                "ai": "Automatically archives signed ePOD (Electronic Proof of Delivery), BOL (Bill of Lading), and GPS timestamps.",
            },
            {
                "badge": "Step 5 · Freight Audit & Claims",
                "title": "Audit Carrier Freight Bill & Dispute Unfair OTIF (On-Time In-Full) Fines",
                "plain": "Verify carrier freight bills against contract rate tables and automatically dispute invalid retailer OTIF (On-Time In-Full) chargeback fines.",
                "real_world": "When a retailer's automated system mistakenly deducts a $45,000 OTIF (On-Time In-Full) penalty even though the truck arrived at the gate on time, Kraft Heinz / Unilever submit the GPS + ASN (Advance Ship Notice) + ePOD dossier to recover 100% of the fine.",
                "manual": "Companies lose 2%–3% of revenue to unchallenged retail chargebacks and carrier billing errors.",
                "ai": "Freight Bill Audit & OTIF Penalty Shield recover overcharges and invalid fines automatically.",
            },
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

PILLAR_REAL_WORLD_EXAMPLES = {
    "demand_sop": (
        "<strong>Unilever, PepsiCo &amp; Zara:</strong> Unilever and PepsiCo ingest daily <strong>POS (Point of Sale — store checkout barcode scans)</strong> from Walmart and Tesco plus local weather forecasts to adjust production before weekend heatwaves hit, while Zara uses daily store checkout signals to update garment forecasts twice a week and avoid the Bullwhip Effect."
    ),
    "sourcing_procurement": (
        "<strong>Apple, Toyota &amp; Nestl\u00e9:</strong> Apple and Toyota map every <strong>BOM (Bill of Materials — product recipe)</strong> across Tier-1 (Foxconn/Denso) and Tier-2/3 raw wafer and lithium suppliers, benchmark supplier <strong>RFQ (Request for Quotation)</strong> bids against live commodity indices, and run automated <strong>3-Way Match</strong> (matching the <strong>PO — Purchase Order</strong>, <strong>GRN — Goods Receipt Note</strong>, and Invoice) before releasing cash."
    ),
    "manufacturing_prod": (
        "<strong>Tesla, Pfizer &amp; Amul Dairy:</strong> Tesla and Toyota track real-time factory machine <strong>OEE (Overall Equipment Effectiveness — uptime, speed &amp; quality %)</strong> via vibration sensors to stop unplanned line breakdowns; Pfizer audits digital <strong>eBHR (Electronic Batch History Records)</strong> and <strong>COA (Certificates of Analysis)</strong> for rapid vaccine release; and Amul optimizes <strong>CIP (Clean-in-Place)</strong> pipe washes between dairy batches."
    ),
    "logistics_fleet": (
        "<strong>Walmart, Maersk, Sysco &amp; FedEx:</strong> Sysco and Coca-Cola pack multi-stop delivery trailers in <strong>3D LIFO (Last-In, First-Out)</strong> stop sequence so Stop #1 sits right at the rear doors; Maersk and Nike orchestrate ocean port drayage to avoid daily container <strong>Demurrage</strong> fines; and Walmart tracks truck <strong>ELD (Electronic Logging Device)</strong> driving hours and <strong>ePOD (Electronic Proof of Delivery)</strong> to protect 98% <strong>OTIF (On-Time In-Full)</strong> delivery."
    ),
    "inventory_warehouse": (
        "<strong>Amazon, Target &amp; McKesson Pharma:</strong> Amazon and DHL dynamically re-slot fast-selling <strong>SKUs (Stock Keeping Units)</strong> into waist-high Golden-Zone bins inside their <strong>WMS (Warehouse Management System)</strong>; McKesson and Amul enforce strict <strong>FEFO (First-Expired, First-Out)</strong> wave picking so short-dated medicine and milk never expire in the warehouse; and Procter &amp; Gamble uses <strong>MEIO (Multi-Echelon Inventory Optimization)</strong> to cut <strong>DIO (Days Inventory Outstanding)</strong>."
    ),
    "circular_enable": (
        "<strong>Amazon, Apple, Unilever &amp; Tata Steel:</strong> Amazon uses <strong>Keep-It vs. Return-It</strong> math on low-price <strong>RMA (Return Merchandise Authorization)</strong> refunds when return shipping costs more than the item; Apple achieves a negative <strong>CCC (Cash Conversion Cycle = DIO + DSO &minus; DPO)</strong> by turning inventory in 9 days; and Unilever &amp; Tata Steel track supplier <strong>Scope 3 Carbon</strong> for European <strong>CBAM (Carbon Border Adjustment Mechanism)</strong> and <strong>EUDR (EU Deforestation Regulation)</strong> compliance."
    ),
}


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
            real_world_example = PILLAR_REAL_WORLD_EXAMPLES.get(
                dept_id,
                PILLAR_REAL_WORLD_EXAMPLES["demand_sop"],
            )

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
                "realWorld": real_world_example,
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
            🗣️ PART 1 · HOW TO EXPLAIN THIS AGENT TO A CUSTOMER (PLAIN ENGLISH TABLE + REAL-WORLD EXAMPLE)
          </div>
          <div class="g-table-wrap">
            <table class="g-table">
              <thead>
                <tr>
                  <th style="width:240px;">Question</th>
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
                <tr style="background:#FEF7E0;">
                  <td style="font-weight:700; color:#B06000;">🌍 4. Real-World Company Example</td>
                  <td>${{ag.realWorld}}</td>
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


def _convert_backticks(obj):
    """Recursively converts markdown `code` backticks into HTML <code>code</code> tags."""
    import re
    if isinstance(obj, str):
        return re.sub(r"`([^`]+)`", r"<code>\1</code>", obj)
    if isinstance(obj, list):
        return [_convert_backticks(x) for x in obj]
    if isinstance(obj, tuple):
        return tuple(_convert_backticks(x) for x in obj)
    if isinstance(obj, dict):
        return {k: _convert_backticks(v) for k, v in obj.items()}
    return obj


def build_google_linear_academy() -> None:
    """Rebuilds supply_chain_101_interactive_academy.html in Google's bright, spacious, linear, button-wise & tabular design language."""
    from supply_chain_real_world_sectors_data import (
        QUICK_ABBREVIATIONS_TABLE,
        SECTOR_CASE_STUDIES,
        STAGES_DATA,
    )

    fc_json = json.dumps(_convert_backticks(FLASHCARDS), ensure_ascii=False)
    wf_json = json.dumps(_convert_backticks(WORKFLOW_SIMULATORS), ensure_ascii=False)
    dec_json = json.dumps(_convert_backticks(CUSTOMER_DECODER), ensure_ascii=False)
    quiz_json = json.dumps(_convert_backticks(QUIZ_QUESTIONS), ensure_ascii=False)
    stages_json = json.dumps(_convert_backticks(STAGES_DATA), ensure_ascii=False)
    sectors_json = json.dumps(_convert_backticks(SECTOR_CASE_STUDIES), ensure_ascii=False)

    abbr_rows_html = "".join(
        f"""<tr>
          <td style="font-weight:800; color:#1A73E8; font-size:17px;"><code>{row["code"]}</code></td>
          <td style="font-weight:700; color:#1E8E3E;">{row["full"]}</td>
          <td>{row["simple"]}</td>
          <td style="background:#F8FAFD; color:#202124;">{row["example"]}</td>
        </tr>"""
        for row in QUICK_ABBREVIATIONS_TABLE
    )

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
      max-width: 1140px;
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
    /* Chapter Navigation Bar (6 Chapters) */
    .g-chapter-bar {{
      display: grid;
      grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 28px;
    }}
    @media (max-width: 1020px) {{
      .g-chapter-bar {{ grid-template-columns: repeat(2, 1fr); }}
    }}
    .g-chap-btn {{
      font-family: var(--font-sans);
      font-size: 14.5px;
      font-weight: 700;
      padding: 16px 12px;
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
        🎓 Supply Chain 101 — Zero Unexplained Abbreviations + Real-World Companies
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
        EVERY ABBREVIATION SPELLED OUT · REAL-WORLD EXAMPLES IN EVERY SECTION + 8 INDUSTRY SECTORS
      </span>
      <h1 style="font-family:var(--font-display); font-size:34px; margin:0 0 8px;">
        Learn Supply Chain From Scratch (Button-by-Button &amp; Tabular)
      </h1>
      <p style="margin:0; color:var(--text-sub); font-size:18px; max-width:980px;">
        Click through the <strong>6 simple chapters</strong> below one at a time. Every single abbreviation (like <strong>OTIF — On-Time In-Full</strong>, <strong>DIO — Days Inventory Outstanding</strong>, and <strong>CCC — Cash Conversion Cycle</strong>) is spelled out and explained right where it appears, with <strong>real-world company examples</strong> inside every section plus a dedicated <strong>Chapter 6 covering 8 major industry sectors</strong>.
      </p>
    </section>

    <!-- 6 CHAPTER BUTTONS -->
    <nav class="g-chapter-bar">
      <button type="button" class="g-chap-btn active" onclick="switchChapter('chap1', this)">
        1 · Intro, Abbreviations &amp; 7 Stages
      </button>
      <button type="button" class="g-chap-btn" onclick="switchChapter('chap2', this)">
        2 · Bullwhip &amp; 4 Core Diagrams
      </button>
      <button type="button" class="g-chap-btn" onclick="switchChapter('chap3', this)">
        3 · 4 Step-by-Step Workflows
      </button>
      <button type="button" class="g-chap-btn" onclick="switchChapter('chap4', this)">
        4 · All 56 Terms (1-by-1 or Table)
      </button>
      <button type="button" class="g-chap-btn" onclick="switchChapter('chap5', this)">
        5 · Customer Decoder &amp; Quiz
      </button>
      <button type="button" class="g-chap-btn" style="border-color:#1E8E3E;" onclick="switchChapter('chap6', this)">
        🌍 6 · Real-World Companies (8 Sectors)
      </button>
    </nav>

    <!-- ===================================================================
         CHAPTER 1: INTRODUCTION TO SUPPLY CHAIN, ABBREVIATIONS & THE 7 STAGES
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
          Look at any physical item around you right now — a <strong>jar of Nestlé coffee</strong>, an <strong>Apple iPhone</strong>, a <strong>pair of Nike running shoes</strong>, or <strong>Pfizer medicine at a pharmacy</strong>. None of those products magically appeared on a shelf. Every single one started as raw materials in the ground (coffee beans on a farm in Colombia, silica sand for microchips in Taiwan, rubber and cotton in Vietnam, chemical compounds in Germany) and had to be <strong>planned, bought, manufactured, packed, stored in warehouses, shipped across oceans and highways, and placed on a shelf</strong> at the exact moment you wanted to buy it.
        </p>
        <div style="background:#E8F0FE; border-left:5px solid #1A73E8; border-radius:12px; padding:18px 22px; margin-bottom:26px; font-size:18px; font-weight:600; color:#174EA6;">
          💡 <strong>In one simple sentence:</strong> The <strong>Supply Chain</strong> is the entire end-to-end system of people, factories, suppliers, warehouses, trucks, and software that turns raw ingredients into a finished product in the customer’s hands — and it accounts for <strong>60% to 80% of a product company’s total cost!</strong>
        </div>

        <h3 style="font-family:var(--font-display); font-size:23px; margin:0 0 12px;">
          Where Does Supply Chain Come Into the Picture Inside a Company?
        </h3>
        <p style="color:var(--text-sub); margin:0 0 16px;">
          Every product company has 4 main parts. Here is how they hand the baton to each other, where Supply Chain takes over, and how real companies do this every day:
        </p>

        <!-- Bright Google SVG: Where Supply Chain Fits in the Enterprise -->
        <svg viewBox="0 0 1020 126" style="width:100%; height:auto; display:block; margin-bottom:20px; background:#F8F9FA; border-radius:16px; border:1px solid #DADCE0; padding:8px;">
          <g transform="translate(14,16)">
            <rect width="205" height="94" rx="14" fill="#FFFFFF" stroke="#DADCE0" stroke-width="2"/>
            <text x="102" y="30" text-anchor="middle" fill="#5F6368" font-size="11" font-weight="800">1 · R&amp;D (RESEARCH &amp; DEV)</text>
            <text x="102" y="54" text-anchor="middle" fill="#202124" font-size="14.5" font-weight="700">🧪 Designs Product</text>
            <text x="102" y="76" text-anchor="middle" fill="#5F6368" font-size="11">Recipe: BOM (Bill of Materials)</text>
          </g>
          <text x="230" y="68" fill="#5F6368" font-size="20" font-weight="700">&rarr;</text>
          <g transform="translate(248,16)">
            <rect width="205" height="94" rx="14" fill="#FFFFFF" stroke="#DADCE0" stroke-width="2"/>
            <text x="102" y="30" text-anchor="middle" fill="#5F6368" font-size="11" font-weight="800">2 · MARKETING &amp; SALES</text>
            <text x="102" y="54" text-anchor="middle" fill="#202124" font-size="14.5" font-weight="700">📣 Creates Demand</text>
            <text x="102" y="76" text-anchor="middle" fill="#5F6368" font-size="11">Runs promos &amp; takes orders</text>
          </g>
          <text x="464" y="68" fill="#1A73E8" font-size="20" font-weight="700">&rarr;</text>
          <g transform="translate(482,12)">
            <rect width="300" height="102" rx="16" fill="#E8F0FE" stroke="#1A73E8" stroke-width="3"/>
            <text x="150" y="28" text-anchor="middle" fill="#1A73E8" font-size="12" font-weight="800">3 · 🎯 THE SUPPLY CHAIN (ENGINE ROOM)</text>
            <text x="150" y="54" text-anchor="middle" fill="#202124" font-size="15.5" font-weight="800">⚙️ Plans · Buys · Makes · Stores · Ships</text>
            <text x="150" y="76" text-anchor="middle" fill="#174EA6" font-size="12" font-weight="700">60%–80% of Company Cost &amp; Cash!</text>
            <text x="150" y="94" text-anchor="middle" fill="#5F6368" font-size="11">Led by CSCO (Chief Supply Chain Officer)</text>
          </g>
          <text x="794" y="68" fill="#1E8E3E" font-size="20" font-weight="700">&rarr;</text>
          <g transform="translate(812,16)">
            <rect width="194" height="94" rx="14" fill="#E6F4EA" stroke="#1E8E3E" stroke-width="2"/>
            <text x="97" y="30" text-anchor="middle" fill="#1E8E3E" font-size="11" font-weight="800">4 · FINANCE (THE CFO)</text>
            <text x="97" y="54" text-anchor="middle" fill="#202124" font-size="14.5" font-weight="700">💰 Collects Cash</text>
            <text x="97" y="76" text-anchor="middle" fill="#137333" font-size="11">Pays vendors &amp; books profit</text>
          </g>
        </svg>

        <div class="g-table-wrap" style="margin-bottom:32px;">
          <table class="g-table">
            <thead>
              <tr>
                <th style="width:210px;">Company Function</th>
                <th style="width:230px;">What They Do</th>
                <th>How Supply Chain Connects to Them</th>
                <th style="width:270px;">🌍 Real-World Company Example</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="font-weight:700;">🧪 1. Product / R&amp;D<br/><span style="font-size:13px; color:#5F6368;">(Research &amp; Development)</span></td>
                <td>Invents the product and defines its exact recipe of parts (<strong>BOM — Bill of Materials</strong>, the complete ingredients list).</td>
                <td>Hands the recipe to Supply Chain so buyers can qualify suppliers for every screw, microchip, bottle, and label months before launch (<strong>NPI — New Product Introduction</strong>).</td>
                <td style="background:#F8FAFD;"><strong>📱 Apple (Cupertino):</strong> Engineers design the iPhone in California, then hand the 1,500-part <strong>BOM (Bill of Materials)</strong> to Apple’s supply chain team to lock in Sony cameras, Samsung OLED screens, and TSMC chips 6 months before September launch.</td>
              </tr>
              <tr>
                <td style="font-weight:700;">📣 2. Sales &amp; Marketing</td>
                <td>Runs price promotions, signs retail deals (Walmart, Target, Amazon), and promises delivery dates.</td>
                <td>If Sales runs a 20%-off promotion without telling Supply Chain, stores run out of stock! Supply Chain meets with Sales every month in <strong>S&amp;OP (Sales &amp; Operations Planning)</strong> to match factory output with sales deals.</td>
                <td style="background:#F8FAFD;"><strong>🥔 PepsiCo (Frito-Lay):</strong> Before Super Bowl Sunday, Marketing plans a nationwide Doritos display at Walmart. Supply Chain ramps up potato &amp; corn frying lines 4 weeks early so 5,000 stores don’t run empty on game day.</td>
              </tr>
              <tr style="background:#E8F0FE;">
                <td style="font-weight:800; color:#1A73E8;">⚙️ 3. THE SUPPLY CHAIN<br/><span style="font-size:13px; color:#174EA6;">Led by CSCO (Chief Supply Chain Officer)</span></td>
                <td><strong>Forecasts demand, buys raw materials, runs factories, manages warehouses, and dispatches trucks/ships.</strong></td>
                <td><strong>The physical execution engine of the business.</strong> If Supply Chain fails, factories stop, store shelves go empty, or tens of millions of dollars get trapped in unsold warehouse boxes.</td>
                <td style="background:#FFFFFF;"><strong>🧴 Unilever &amp; Nestlé:</strong> Their supply chains coordinate 300+ factories and 50,000+ suppliers daily to deliver 2 billion Dove soaps, Maggi noodles, and Nescafé jars across 190 countries.</td>
              </tr>
              <tr>
                <td style="font-weight:700;">💰 4. Finance<br/><span style="font-size:13px; color:#5F6368;">Led by CFO (Chief Financial Officer)</span></td>
                <td>Manages company cash flow, profit margins, and supplier/customer payments.</td>
                <td>The CFO relies on Supply Chain to keep <strong>DIO (Days Inventory Outstanding — days cash sits in warehouse boxes)</strong> low, avoid expensive emergency air freight, and check every supplier bill before paying (<strong>3-Way Match</strong>).</td>
                <td style="background:#F8FAFD;"><strong>📦 Amazon &amp; P&amp;G:</strong> Finance tracks how fast warehouse inventory turns into cash (<strong>CCC — Cash Conversion Cycle</strong>) and blocks any supplier invoice that doesn’t match the original Purchase Order and warehouse receipt.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h3 style="font-family:var(--font-display); font-size:23px; margin:0 0 10px;">
          Why Is Supply Chain So Hard? (The 3-Way Tug-of-War — With Every Abbreviation Explained)
        </h3>
        <p style="color:var(--text-sub); margin:0 0 14px;">
          Running a supply chain is difficult because every decision pulls in <strong>3 opposite directions</strong> at once. Notice how every abbreviation below (<strong>OTIF</strong>, <strong>DIO</strong>, <strong>CCC</strong>) is spelled out right in the table:
        </p>
        <div class="g-table-wrap" style="margin-bottom:32px;">
          <table class="g-table">
            <thead>
              <tr>
                <th style="width:190px;">Goal</th>
                <th style="width:220px;">Who Demands It &amp; Key Metric Spelled Out</th>
                <th>What Happens If You Push Too Far</th>
                <th style="width:240px;">🌍 Real-World Example</th>
                <th style="width:220px;">How Our AI Agents Solve It</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="font-weight:800; color:#1E8E3E;">🎯 1. High Service<br/>(Never Run Out)</td>
                <td><strong>Sales &amp; Retail Customers</strong><br/>Demand 98%+ <strong>OTIF (On-Time In-Full — delivering the exact quantity ordered inside the exact time window)</strong>.</td>
                <td>To never run out, you pile up mountains of extra backup stock in every warehouse — tying up tens of millions of dollars in cash!</td>
                <td style="background:#F8FAFD;"><strong>🛒 Walmart &amp; Target</strong> fine suppliers like Kraft Heinz or Colgate <strong>3% of the invoice value</strong> whenever a truck arrives late or short on cases (an <strong>OTIF penalty</strong>).</td>
                <td><strong>Demand Sensing &amp; ATP (Available-to-Promise) Agents</strong> predict exact local demand and protect VIP stock.</td>
              </tr>
              <tr>
                <td style="font-weight:800; color:#1A73E8;">💵 2. Low Inventory Cash<br/>(Lean Warehouses)</td>
                <td><strong>CFO (Chief Financial Officer)</strong><br/>Wants low <strong>DIO (Days Inventory Outstanding — days cash is trapped in unsold boxes)</strong> and low <strong>CCC (Cash Conversion Cycle — total days a dollar stays stuck before turning back into cash)</strong>.</td>
                <td>If you slash warehouse stock too aggressively to save cash, a single supplier delay or warm weekend causes immediate empty shelves (<strong>Stockouts</strong>)!</td>
                <td style="background:#F8FAFD;"><strong>👟 Nike (2022–2023):</strong> When pandemic shipping delays cleared all at once, Nike’s <strong>DIO (Days Inventory Outstanding)</strong> ballooned to $9.7 Billion in unsold shoes, forcing margin-crushing clearance sales.</td>
                <td><strong>MEIO (Multi-Echelon Inventory Optimization) Agent</strong> mathematically places smaller, smarter buffers across hubs.</td>
              </tr>
              <tr>
                <td style="font-weight:800; color:#E8710A;">🚚 3. Low Operating Cost<br/>(Cheap Factory &amp; Freight)</td>
                <td><strong>Factory &amp; Logistics Heads</strong><br/>Want long factory runs and 100% full <strong>FTL (Full Truckload — 53-foot highway trailers)</strong>.</td>
                <td>Waiting to fill a 53-foot truck or running huge factory batches lowers cost per box, but makes reaction time slow when customer tastes shift.</td>
                <td style="background:#F8FAFD;"><strong>🥤 Coca-Cola:</strong> Running only classic red Coke cans all week maximizes factory speed, but stores also need Diet Coke, Sprite, and Fanta every 48 hours without shipping half-empty trucks.</td>
                <td><strong>Finite Scheduler &amp; 3D Load Studio</strong> cut line changeover waste and pack multi-stop full trucks.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- PART 1A-2: QUICK-DECODE TABLE OF THE 18 MOST COMMON ABBREVIATIONS -->
        <div style="background:#FEF7E0; border:2px solid #F9AB00; border-radius:16px; padding:22px 26px; margin-bottom:10px;">
          <span class="g-badge" style="background:#FFFFFF; color:#B06000; border:1px solid #F9AB00;">
            🔤 PART 1A-2 · QUICK-DECODE TABLE OF THE 18 MOST COMMON SUPPLY CHAIN ABBREVIATIONS
          </span>
          <h3 style="font-family:var(--font-display); font-size:24px; margin:0 0 8px; color:#202124;">
            Bookmark This Table: Every Major Acronym (<code>OTIF</code>, <code>DIO</code>, <code>DSO</code>, <code>DPO</code>, <code>CCC</code>, <code>BOM</code>, <code>S&amp;OP</code>, <code>MEIO</code>, <code>FEFO</code>, <code>ATP</code>, <code>ERP/MES/WMS/TMS</code>) Explained Simply
          </h3>
          <p style="margin:0 0 16px; color:#5F6368;">
            Whenever someone in a meeting drops a 3-letter or 4-letter supply chain acronym, here is what it stands for, what it means in everyday words, and how a real-world company uses it:
          </p>
          <div class="g-table-wrap">
            <table class="g-table">
              <thead>
                <tr>
                  <th style="width:110px;">Acronym</th>
                  <th style="width:230px;">Full Spelled-Out Name</th>
                  <th>Plain-English Meaning (Zero Jargon)</th>
                  <th style="width:310px;">🌍 Real-World Company Example</th>
                </tr>
              </thead>
              <tbody>
                {abbr_rows_html}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- SECTION 1B: THE 7 STAGES OF THE SUPPLY CHAIN PROCESS (DETAILED WALKTHROUGH) -->
      <section class="g-card">
        <span class="g-badge" style="background:var(--g-blue-bg); color:var(--g-blue);">
          PART 1B · THE 7 STAGES OF THE SUPPLY CHAIN PROCESS (WITH REAL-WORLD COMPANY EXAMPLES IN EVERY STAGE)
        </span>
        <h2 style="font-family:var(--font-display); font-size:28px; margin:0 0 10px;">
          Step-by-Step: How the Supply Chain Process Works From Beginning to End
        </h2>
        <p style="color:var(--text-sub); margin:0 0 20px;">
          Before a single physical box moves, the process starts with <strong>Stage 0 · Planning &amp; Forecasting</strong> (the brain), followed by the <strong>6 physical stages</strong>. Click each of the 7 stage buttons below in order (or use <code>Next Stage &rarr;</code>) to see what happens, <strong>how 3 real-world companies execute that stage</strong>, and every abbreviation spelled out in full:
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
            <text x="66" y="52" text-anchor="middle" fill="#202124" font-size="13.5" font-weight="700">🏢 Regional Hub</text>
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
            <text x="71" y="52" text-anchor="middle" fill="#202124" font-size="13.5" font-weight="700">🛒 Store &amp; Returns</text>
            <text x="71" y="72" text-anchor="middle" fill="#5F6368" font-size="10.5">On-Time In-Full</text>
          </g>
        </svg>

        <!-- 7 Stage Selector Buttons -->
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:20px;" id="stageBtnRow">
          <button type="button" class="g-btn active" onclick="showStageTable(0, this)">0 · 📈 Plan &amp; Forecast (The Brain)</button>
          <button type="button" class="g-btn" onclick="showStageTable(1, this)">1 · ⛏️ Source (Suppliers)</button>
          <button type="button" class="g-btn" onclick="showStageTable(2, this)">2 · 🏭 Make (Factory)</button>
          <button type="button" class="g-btn" onclick="showStageTable(3, this)">3 · 🏢 Central Hub (RDC)</button>
          <button type="button" class="g-btn" onclick="showStageTable(4, this)">4 · 📦 Local Warehouse (FDC)</button>
          <button type="button" class="g-btn" onclick="showStageTable(5, this)">5 · 🚚 Move (Fleet &amp; Transit)</button>
          <button type="button" class="g-btn" onclick="showStageTable(6, this)">6 · 🛒 Customer Delivery &amp; Returns</button>
        </div>

        <div id="stageTableMount"></div>
      </section>

      <!-- THE 3 FLOWS TABLE -->
      <section class="g-card">
        <span class="g-badge" style="background:var(--g-green-bg); color:var(--g-green);">
          PART 1C · THE 3 FLOWS TABLE (WITH REAL-WORLD COMPANY EXAMPLES)
        </span>
        <h2 style="font-family:var(--font-display); font-size:26px; margin:0 0 14px;">
          The 3 Things Moving Through Every Supply Chain at the Same Time
        </h2>
        <div class="g-table-wrap">
          <table class="g-table">
            <thead>
              <tr>
                <th style="width:210px;">Flow Name</th>
                <th style="width:170px;">Direction</th>
                <th>What Moves &amp; Why It Matters in Plain English</th>
                <th style="width:310px;">🌍 Real-World Company Example</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="font-weight:700; color:#1E8E3E;">📦 1. Physical Goods Flow</td>
                <td><strong>Downstream (&rarr;)</strong><br/>Supplier &rarr; Customer</td>
                <td>Raw materials, parts, pallets, and finished boxes moving toward the customer. If this stops, store shelves go empty (<strong>Stockout</strong>).</td>
                <td style="background:#F8FAFD;"><strong>☕ Starbucks:</strong> Arabica coffee beans travel from farms in Colombia &rarr; roasting plants in Nevada &rarr; regional hubs &rarr; 16,000 cafés every week.</td>
              </tr>
              <tr>
                <td style="font-weight:700; color:#1A73E8;">📡 2. Information Signal Flow</td>
                <td><strong>Upstream (&larr;)</strong><br/>Customer &rarr; Supplier</td>
                <td>Store checkout barcode scans (<strong>POS — Point of Sale</strong>), customer orders, and forecasts moving backward to tell factories what to make next.</td>
                <td style="background:#F8FAFD;"><strong>🛒 Walmart Retail Link:</strong> Every time a shopper scans a bottle of Tide detergent at checkout, Walmart’s computer sends that live <strong>POS (Point of Sale)</strong> signal straight back to Procter &amp; Gamble’s factory.</td>
              </tr>
              <tr>
                <td style="font-weight:700; color:#E8710A;">💰 3. Money &amp; Cash Flow</td>
                <td><strong>Both Ways (&harr;)</strong><br/>Customer &harr; Company &harr; Vendor</td>
                <td>Customers pay invoices (<strong>DSO — Days Sales Outstanding</strong>), while the company pays suppliers (<strong>DPO — Days Payable Outstanding</strong>) after checking the bill (<strong>3-Way Match</strong>). Together with inventory days (<strong>DIO</strong>), this sets your <strong>CCC (Cash Conversion Cycle)</strong>.</td>
                <td style="background:#F8FAFD;"><strong>📱 Apple &amp; 📦 Amazon:</strong> Shoppers pay Apple &amp; Amazon immediately by credit card (<strong>DSO = ~5 days</strong>), inventory sells out in 9–25 days (<strong>DIO</strong>), and Apple/Amazon pay their suppliers 60–90 days later (<strong>DPO</strong>) — giving them a <strong>negative Cash Conversion Cycle (CCC)</strong>!</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- THE 4 ENTERPRISE SOFTWARE SYSTEMS TABLE -->
      <section class="g-card">
        <span class="g-badge" style="background:#F3E8FD; color:#9334E6;">
          PART 1D · THE 4 SOFTWARE SYSTEMS TABLE (WITH REAL-WORLD COMPANY EXAMPLES)
        </span>
        <h2 style="font-family:var(--font-display); font-size:26px; margin:0 0 14px;">
          ERP vs. MES vs. WMS vs. TMS — What Software Runs Which Building?
        </h2>
        <div class="g-table-wrap">
          <table class="g-table">
            <thead>
              <tr>
                <th style="width:110px;">Acronym</th>
                <th style="width:210px;">Full Name Spelled Out</th>
                <th style="width:180px;">Where It Lives</th>
                <th>What It Does in Plain Words (With Brand Examples)</th>
                <th style="width:290px;">🌍 Real-World Company Example</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong style="font-size:18px; color:#1A73E8;">ERP</strong></td>
                <td><strong>Enterprise Resource Planning</strong></td>
                <td>🏢 Corporate Head Office &amp; Finance</td>
                <td>The company’s financial brain. Holds customer orders, product part numbers (<strong>SKUs — Stock Keeping Units</strong>), supplier <strong>POs (Purchase Orders)</strong>, and accounting invoices. <em>(SAP S/4HANA, Oracle Cloud ERP)</em></td>
                <td style="background:#F8FAFD;"><strong>🍫 Nestlé &amp; 🧴 Unilever</strong> run global <strong>SAP S/4HANA ERP</strong> to manage 100,000+ product SKUs, supplier Purchase Orders, and financial books across 190 countries.</td>
              </tr>
              <tr>
                <td><strong style="font-size:18px; color:#9334E6;">MES</strong></td>
                <td><strong>Manufacturing Execution System</strong></td>
                <td>🏭 Inside the Factory Floor</td>
                <td>Runs the factory machines and assembly lines. Tracks machine health (<strong>OEE — Overall Equipment Effectiveness</strong>), production schedules, and digital batch logs (<strong>eBHR — Electronic Batch History Record</strong>). <em>(Siemens Opcenter, Rockwell)</em></td>
                <td style="background:#F8FAFD;"><strong>🚗 Tesla &amp; BMW</strong> use factory-floor <strong>MES</strong> systems to guide every welding robot, torque wrench, and battery quality test on each car’s VIN number.</td>
              </tr>
              <tr>
                <td><strong style="font-size:18px; color:#1E8E3E;">WMS</strong></td>
                <td><strong>Warehouse Management System</strong></td>
                <td>📦 Inside the 4 Walls of the Warehouse</td>
                <td>Tracks exactly which shelf bin every pallet sits in (<strong>Slotting</strong>) and guides workers or robots with barcode scanners to pick and pack orders (<strong>Wave Picking</strong>). <em>(Manhattan Active WMS, SAP EWM)</em></td>
                <td style="background:#F8FAFD;"><strong>👟 Nike &amp; 📦 Amazon</strong> use <strong>WMS</strong> software to coordinate 750,000+ mobile warehouse robots and human pickers so an online order is packed in under 30 minutes.</td>
              </tr>
              <tr>
                <td><strong style="font-size:18px; color:#007B83;">TMS</strong></td>
                <td><strong>Transportation Management System</strong></td>
                <td>🚚 Outside on the Road, Ocean &amp; Air</td>
                <td>Books trucking and ocean carriers, plans multi-stop delivery routes, tracks live truck GPS, and audits freight bills. <em>(Oracle OTM, Blue Yonder TMS)</em></td>
                <td style="background:#F8FAFD;"><strong>🥤 PepsiCo &amp; 🛒 Walmart</strong> use <strong>TMS</strong> platforms to route 10,000+ highway trucks daily, consolidate loads, and track live GPS arrival times.</td>
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
              CHAPTER 2A · INTERACTIVE BULLWHIP SIMULATOR + REAL-WORLD CASE STUDIES
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
          Drag the slider below to change how much extra customers buy at the store checkout (<strong>POS — Point of Sale</strong>), and see what happens to orders at each stage upstream in the table below:
        </p>

        <div style="background:#F8F9FA; border:1px solid var(--border-light); border-radius:16px; padding:20px 24px; margin-bottom:20px;">
          <label style="font-weight:700; font-size:18px; display:flex; justify-content:space-between;">
            <span>🛒 Customer Checkout Surge at the Store (POS — Point of Sale):</span>
            <span id="bwValLabel" style="color:var(--g-blue); font-weight:800;">+10%</span>
          </label>
          <input type="range" id="bwRange" min="5" max="25" value="10" style="width:100%; margin-top:12px; accent-color:var(--g-blue);" oninput="renderBwTable()" />
        </div>

        <div id="bwTableMount" style="margin-bottom:26px;"></div>

        <h3 style="font-family:var(--font-display); font-size:22px; margin:0 0 12px;">
          🌍 3 Famous Real-World Company Examples of the Bullwhip Effect
        </h3>
        <div class="g-table-wrap">
          <table class="g-table">
            <thead>
              <tr>
                <th style="width:230px;">Real-World Company</th>
                <th style="width:240px;">What Customers Actually Did</th>
                <th>How the Bullwhip Panic Happened Upstream</th>
                <th style="width:260px;">How They Fixed It</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="font-weight:800; color:#1A73E8;">👶 1. Procter &amp; Gamble (Pampers Diapers)</td>
                <td>Babies used diapers at a steady, flat rate every single week (±2% variation at store checkouts).</td>
                <td>Store managers padded orders during promos &rarr; distributors doubled orders &rarr; P&amp;G’s diaper factories saw ±40% swings &rarr; 3M’s adhesive tape suppliers saw ±80% wild booms and crashes! (This is where P&amp;G executives coined the term <em>“Bullwhip Effect”</em>.)</td>
                <td style="background:#E6F4EA; color:#137333;">Connected live <strong>POS (Point of Sale)</strong> store scanner data directly to P&amp;G planners via <strong>CPFR (Collaborative Planning, Forecasting &amp; Replenishment)</strong>.</td>
              </tr>
              <tr>
                <td style="font-weight:800; color:#D93025;">🚗 2. Ford, GM &amp; TSMC (2020–2022 Chip Crisis)</td>
                <td>Car sales dipped briefly in Spring 2020, then rebounded by +15% as people bought cars.</td>
                <td>Automakers canceled all microchip orders in April 2020, then panic-ordered 3× their normal chip volume in late 2020. Taiwan Semiconductor (TSMC) lines jammed for 18 months, forcing Ford and GM to park 100,000 unfinished trucks in lots!</td>
                <td style="background:#E6F4EA; color:#137333;">Automakers now share 52-week rolling production schedules directly with Tier-2 wafer foundries (<strong>Tier-N Visibility</strong>).</td>
              </tr>
              <tr>
                <td style="font-weight:800; color:#B06000;">🍝 3. Barilla Pasta (Italy)</td>
                <td>Italians ate steady amounts of pasta every week all year round.</td>
                <td>Barilla’s sales reps offered end-of-quarter volume discounts, causing grocery distributors to buy 10 weeks of pasta at once and zero for the next two months — overwhelming Barilla’s pasta drying ovens and trucks.</td>
                <td style="background:#E6F4EA; color:#137333;">Barilla took over automatic warehouse replenishment based on actual daily grocery shelf sales.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- 4 CORE VISUAL DIAGRAMS (CLICK 1 BUTTON AT A TIME) -->
      <section class="g-card">
        <span class="g-badge" style="background:var(--g-blue-bg); color:var(--g-blue);">
          CHAPTER 2B · 4 ESSENTIAL VISUAL DIAGRAMS (WITH REAL-WORLD COMPANY EXAMPLES)
        </span>
        <h2 style="font-family:var(--font-display); font-size:28px; margin:0 0 16px;">
          Click Any Concept Below to View Its Diagram, Spelled-Out Abbreviations &amp; Real-World Company Examples
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
          CHAPTER 3 · 4 CORE SUPPLY CHAIN WORKFLOWS (WITH REAL-WORLD COMPANY SPOTLIGHTS)
        </span>
        <h2 style="font-family:var(--font-display); font-size:28px; margin:0 0 12px;">
          How Supply Chain Teams Actually Work Day-to-Day (With Real-World Examples at Every Step)
        </h2>
        <p style="color:var(--text-sub); margin:0 0 20px;">
          Click any of the 4 core processes below to see every step in a clean, spacious table comparing the <strong>Old Manual Way</strong> vs. the <strong>New AI Agent Way</strong>, plus how real companies execute each step:
        </p>

        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:24px;">
          <button type="button" class="g-btn active" onclick="selectWorkflow('sop', this)">1 · 📅 Monthly Planning (S&amp;OP — Sales &amp; Operations Planning)</button>
          <button type="button" class="g-btn" onclick="selectWorkflow('match3', this)">2 · 🧾 Paying Suppliers (3-Way Match: PO + GRN + Invoice)</button>
          <button type="button" class="g-btn" onclick="selectWorkflow('wms_flow', this)">3 · 📦 Warehouse Flow (Inbound Unload to Outbound Ship)</button>
          <button type="button" class="g-btn" onclick="selectWorkflow('otif_flow', this)">4 · 🚚 Customer Order to Delivery (OTIF — On-Time In-Full)</button>
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

    <!-- ===================================================================
         CHAPTER 6: REAL-WORLD COMPANIES ACROSS ALL 8 INDUSTRY SECTORS
         =================================================================== -->
    <div id="chap6" class="g-pane">
      <section class="g-card" style="border-top: 6px solid var(--g-green);">
        <span class="g-badge" style="background:var(--g-green-bg); color:var(--g-green);">
          CHAPTER 6 · REAL-WORLD SUPPLY CHAINS ACROSS ALL 8 MAJOR INDUSTRY SECTORS
        </span>
        <h2 style="font-family:var(--font-display); font-size:30px; margin:0 0 10px;">
          How Famous Companies Across Every Sector Actually Run Their Supply Chains End-to-End
        </h2>
        <p style="color:var(--text-sub); margin:0 0 20px;">
          A smartphone company (Apple), a fast-fashion retailer (Zara), a vaccine maker (Pfizer), and a dairy cooperative (Amul) all use the same 7 supply chain stages — but they configure them in completely different ways! Click any of the <strong>8 industry sectors</strong> below (or click <strong>📊 Compare All 8 Sectors in One Table</strong>) to see their end-to-end blueprint, metrics, secret weapon, and AI agents:
        </p>

        <!-- 8 Sector Selector Buttons + Master Comparison Button -->
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:24px;" id="sectorBtnRow">
          <button type="button" class="g-btn active" onclick="showSectorCase(0, this)">1 · 🛒 Consumer Goods (Unilever, Nestlé, ITC)</button>
          <button type="button" class="g-btn" onclick="showSectorCase(1, this)">2 · 📱 Smartphones &amp; Tech (Apple, Samsung)</button>
          <button type="button" class="g-btn" onclick="showSectorCase(2, this)">3 · 🚗 Automotive &amp; EVs (Toyota, Tesla)</button>
          <button type="button" class="g-btn" onclick="showSectorCase(3, this)">4 · 💊 Pharma &amp; Vaccines (Pfizer, Novo Nordisk)</button>
          <button type="button" class="g-btn" onclick="showSectorCase(4, this)">5 · 📦 Retail &amp; E-Commerce (Walmart, Amazon)</button>
          <button type="button" class="g-btn" onclick="showSectorCase(5, this)">6 · 👗 Fast Fashion &amp; Shoes (Zara, Nike)</button>
          <button type="button" class="g-btn" onclick="showSectorCase(6, this)">7 · 🥛 Fresh Dairy &amp; Food (Amul, McDonald's)</button>
          <button type="button" class="g-btn" onclick="showSectorCase(7, this)">8 · ⚙️ Industrial &amp; Heavy (Caterpillar, BASF)</button>
          <button type="button" class="g-btn" style="border-color:#1E8E3E; color:#1E8E3E; font-weight:700;" onclick="showAllSectorsComparison(this)">📊 Compare All 8 Sectors in One Table</button>
        </div>

        <div id="sectorCaseMount"></div>
      </section>
    </div>
  </main>

  <script>
    const FLASHCARDS = {fc_json};
    const WORKFLOWS = {wf_json};
    const DECODER = {dec_json};
    const QUIZ = {quiz_json};
    const STAGES = {stages_json};
    const SECTORS = {sectors_json};

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
                <td style="width:270px; font-weight:700; color:#1A73E8;">🎯 1. What This Stage Is &amp; Why It Exists</td>
                <td style="font-size:17px; font-weight:500;">${{s.whyExists}}</td>
              </tr>
              <tr>
                <td style="font-weight:700; color:#B06000;">💡 2. Everyday Real-Life Analogy</td>
                <td style="font-weight:600; background:#FEF7E0;">${{s.analogy}}</td>
              </tr>
              <tr>
                <td style="font-weight:800; color:#174EA6;">🌍 3. Real-World Company Examples at This Stage</td>
                <td style="background:#E8F0FE; color:#202124;">${{s.realWorld}}</td>
              </tr>
              <tr>
                <td style="font-weight:700; color:#1E8E3E;">📦 4. Step-by-Step What Actually Happens Here</td>
                <td>${{s.story}}</td>
              </tr>
              <tr>
                <td style="font-weight:700; color:#202124;">👥 5. Who Works Here (Human Roles)</td>
                <td>${{s.personas}}</td>
              </tr>
              <tr>
                <td style="font-weight:700; color:#007B83;">📄 6. Key Documents &amp; Data Passed Forward</td>
                <td><strong>${{s.docs}}</strong></td>
              </tr>
              <tr>
                <td style="font-weight:700; color:#9334E6;">💻 7. Software Systems Used</td>
                <td><strong>${{s.software}}</strong></td>
              </tr>
              <tr>
                <td style="font-weight:700; color:#D93025;">⚠️ 8. What Goes Wrong &amp; Why It Costs Millions</td>
                <td style="background:#FCE8E6; color:#C5221F; font-weight:500;">${{s.breaks}}</td>
              </tr>
              <tr>
                <td style="font-weight:700; color:#1E8E3E;">🤖 9. How Our AI Agents Solve It</td>
                <td style="background:#E6F4EA; color:#137333; font-weight:600;">${{s.agents}}</td>
              </tr>
              <tr>
                <td style="font-weight:800; color:#202124;">🔤 10. Every Abbreviation in This Stage Explained in Plain Words</td>
                <td style="background:#F8F9FA;">${{s.terms}}</td>
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
        ["1. Store Checkout (POS — Point of Sale)", "Customers buy slightly more on a warm weekend."],
        ["2. Store Manager Order", bwAi ? "Shared live via CPFR (Collaborative Planning, Forecasting & Replenishment) — no panic padding." : "Manager panics and pads order to avoid running out."],
        ["3. Local Warehouse (FDC — Fulfillment Distribution Center)", bwAi ? "MEIO (Multi-Echelon Inventory Optimization) adjusts buffer smoothly." : "Sees spiky store orders and doubles safety buffer."],
        ["4. Factory Production Line", bwAi ? "Runs steady shift schedule." : "Turns on expensive weekend overtime shifts."],
        ["5. Raw Material Supplier", bwAi ? "Steady raw material pulls." : "Sees massive fake boom, followed by order cancellations!"]
      ];
      const rows = names.map((n, i) => {{
        const val = Math.round(pos * mults[i]);
        const barW = Math.min(100, Math.round(val / 1.8));
        const col = bwAi ? '#1E8E3E' : (i >= 3 ? '#D93025' : (i >= 1 ? '#F9AB00' : '#1A73E8'));
        return `<tr>
          <td style="font-weight:700; width:260px;">${{n[0]}}</td>
          <td style="width:120px; font-weight:800; color:${{col}}; font-size:18px;">+${{val}}%</td>
          <td style="width:260px;">
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

    // 4 Core Concept Diagrams (One at a Time, with Real-World Company Examples)
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
            <text x="230" y="104" text-anchor="middle" fill="#5F6368" font-size="12.5">Examples: Colgate Toothpaste, Coca-Cola, Duracell Batteries</text>

            <rect x="480" y="20" width="420" height="100" rx="14" fill="#E6F4EA" stroke="#1E8E3E" stroke-width="2"/>
            <text x="690" y="52" text-anchor="middle" fill="#1E8E3E" font-size="15" font-weight="800">MAKE-TO-ORDER (MTO · PULL STRATEGY)</text>
            <text x="690" y="80" text-anchor="middle" fill="#202124" font-size="14" font-weight="600">Wait for Customer Order &rarr; Custom Build &rarr; Ship Direct</text>
            <text x="690" y="104" text-anchor="middle" fill="#5F6368" font-size="12.5">Examples: Custom Dell Server, Boeing 787 Jet, Custom Tesla</text>
          </svg>
          <div class="g-table-wrap">
            <table class="g-table">
              <thead><tr><th style="width:90px;">Acronym</th><th style="width:160px;">Full Name</th><th>How It Works &amp; Biggest Risk</th><th style="width:340px;">🌍 Real-World Company Examples</th></tr></thead>
              <tbody>
                <tr><td><strong style="color:#1A73E8;">MTS</strong></td><td><strong>Make-to-Stock</strong></td><td>Factory builds goods in advance based on a forecast and stacks them in warehouses so shoppers can grab them immediately. <em>Risk:</em> If the forecast is wrong, you get stuck with unsold dead stock (<strong>SLOB — Slow-Moving &amp; Obsolete Stock</strong>).</td><td style="background:#F8FAFD;"><strong>🧴 Procter &amp; Gamble (Tide) &amp; 🍫 Nestlé (KitKat):</strong> You will never wait 2 weeks for a factory to custom-make a KitKat bar — they are produced <strong>MTS (Make-to-Stock)</strong> millions at a time.</td></tr>
                <tr><td><strong style="color:#1E8E3E;">MTO</strong></td><td><strong>Make-to-Order</strong></td><td>Factory waits until a customer actually places a firm order before building the finished product. <em>Risk:</em> Customer has to wait longer (<strong>Lead Time</strong>), and raw part shortages delay delivery.</td><td style="background:#F8FAFD;"><strong>💻 Dell Custom Servers, ✈️ Boeing &amp; 👟 Nike By You:</strong> Boeing doesn’t build $250M airplanes and hope an airline buys them — every plane is built <strong>MTO (Make-to-Order)</strong> to the airline’s exact cabin blueprint.</td></tr>
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
            <text x="160" y="102" text-anchor="middle" fill="#5F6368" font-size="12">Amul Dairy, Pfizer Vaccines, Chobani</text>

            <rect x="320" y="20" width="280" height="100" rx="14" fill="#E6F4EA" stroke="#1E8E3E" stroke-width="2"/>
            <text x="460" y="50" text-anchor="middle" fill="#1E8E3E" font-size="15" font-weight="800">2. FIFO (First-In, First-Out)</text>
            <text x="460" y="78" text-anchor="middle" fill="#202124" font-size="13.5" font-weight="600">📦 Ship oldest arrived pallet first</text>
            <text x="460" y="102" text-anchor="middle" fill="#5F6368" font-size="12">Apple Electronics, IKEA, Nike Shoes</text>

            <rect x="620" y="20" width="280" height="100" rx="14" fill="#E8F0FE" stroke="#1A73E8" stroke-width="2"/>
            <text x="760" y="50" text-anchor="middle" fill="#1A73E8" font-size="15" font-weight="800">3. LIFO (Last-In, First-Out)</text>
            <text x="760" y="78" text-anchor="middle" fill="#202124" font-size="13.5" font-weight="600">🚚 Load Delivery Stop #1 LAST</text>
            <text x="760" y="102" text-anchor="middle" fill="#5F6368" font-size="12">Sysco Food Trucks, UPS, PepsiCo</text>
          </svg>
          <div class="g-table-wrap">
            <table class="g-table">
              <thead><tr><th style="width:90px;">Rule</th><th style="width:190px;">Full Name</th><th>Everyday Meaning</th><th style="width:330px;">🌍 Real-World Company Examples</th><th style="width:190px;">Which Agent Uses It</th></tr></thead>
              <tbody>
                <tr><td><strong style="color:#D93025;">FEFO</strong></td><td><strong>First-Expired, First-Out</strong></td><td>Always ship the batch whose expiration date is closest so nothing spoils in the warehouse.</td><td style="background:#F8FAFD;"><strong>🥛 Amul Dairy &amp; 💊 Pfizer:</strong> A yogurt pallet expiring May 10 is always shipped before a pallet expiring May 18, even if the May 10 pallet arrived later.</td><td><code>short_dated_redistributor</code> &amp; <code>dynamic_markdown_agent</code></td></tr>
                <tr><td><strong style="color:#1E8E3E;">FIFO</strong></td><td><strong>First-In, First-Out</strong></td><td>Ship the pallet that arrived earliest so boxes don’t gather dust or packaging wear in the back of the rack.</td><td style="background:#F8FAFD;"><strong>🛋️ IKEA &amp; 📱 Samsung:</strong> TVs and bookshelves don’t expire like milk, so warehouses ship the oldest arrived batch first so boxes stay fresh.</td><td><code>warehouse_slotting_agent</code></td></tr>
                <tr><td><strong style="color:#1A73E8;">LIFO</strong></td><td><strong>Last-In, First-Out</strong></td><td>When loading a multi-stop delivery truck, put Stop #3 in the nose first and Stop #1 at the rear doors last.</td><td style="background:#F8FAFD;"><strong>🚛 Sysco &amp; PepsiCo Route Trucks:</strong> If a truck delivers to 4 restaurants at 6 AM, 7 AM, 8 AM, and 9 AM, the 6 AM restaurant’s pallets are loaded <strong>LAST (LIFO)</strong> right against the rear doors.</td><td><code>load_consolidation_agent</code> (CubeMaster 3D)</td></tr>
              </tbody>
            </table>
          </div>
        `;
      }} else if (idx === 2) {{
        mount.innerHTML = `
          <svg viewBox="0 0 920 140" style="width:100%; height:auto; display:block; margin-bottom:20px; background:#F8F9FA; border-radius:16px; border:1px solid #DADCE0;">
            <rect x="20" y="24" width="260" height="92" rx="14" fill="#E8F0FE" stroke="#1A73E8" stroke-width="2"/>
            <text x="150" y="56" text-anchor="middle" fill="#1A73E8" font-size="15" font-weight="800">+ DIO (55 Days)</text>
            <text x="150" y="82" text-anchor="middle" fill="#202124" font-size="13">Days Inventory Outstanding</text>

            <rect x="300" y="24" width="260" height="92" rx="14" fill="#FEF7E0" stroke="#F9AB00" stroke-width="2"/>
            <text x="430" y="56" text-anchor="middle" fill="#B06000" font-size="15" font-weight="800">+ DSO (40 Days)</text>
            <text x="430" y="82" text-anchor="middle" fill="#202124" font-size="13">Days Sales Outstanding</text>

            <rect x="580" y="24" width="320" height="92" rx="14" fill="#E6F4EA" stroke="#1E8E3E" stroke-width="2"/>
            <text x="740" y="56" text-anchor="middle" fill="#1E8E3E" font-size="15" font-weight="800">− DPO (45 Days) = 50 Days CCC</text>
            <text x="740" y="82" text-anchor="middle" fill="#202124" font-size="13">Minus Days Payable Outstanding</text>
          </svg>
          <div class="g-table-wrap">
            <table class="g-table">
              <thead><tr><th style="width:90px;">Term</th><th style="width:210px;">Full Name Spelled Out</th><th>Plain-English Meaning</th><th style="width:360px;">🌍 Real-World Company Examples</th></tr></thead>
              <tbody>
                <tr><td><strong>DIO</strong></td><td><strong>Days Inventory Outstanding</strong></td><td>How many days cash sits tied up as physical boxes on warehouse shelves before being sold (lower is better).</td><td style="background:#F8FAFD;"><strong>📱 Apple holds only ~9 days of DIO</strong> (iPhones fly out of warehouses almost immediately), whereas a luxury watchmaker or heavy machinery company like <strong>Caterpillar holds 110+ days of DIO</strong>.</td></tr>
                <tr><td><strong>DSO</strong></td><td><strong>Days Sales Outstanding</strong></td><td>How many days it takes to collect cash from customers after you ship their order (lower is better).</td><td style="background:#F8FAFD;"><strong>📦 Amazon &amp; Zara have ~3–5 days DSO</strong> because shoppers pay immediately by credit card, whereas B2B suppliers selling to hospitals wait <strong>45–60 days (DSO)</strong> to get paid.</td></tr>
                <tr><td><strong>DPO</strong></td><td><strong>Days Payable Outstanding</strong></td><td>How many days you wait before paying your suppliers’ invoices (higher keeps cash in your bank longer).</td><td style="background:#F8FAFD;"><strong>🧴 Unilever, P&amp;G &amp; Apple</strong> negotiate <strong>60 to 95 days DPO</strong> with their raw material and component suppliers.</td></tr>
                <tr><td><strong style="color:#1A73E8;">CCC</strong></td><td><strong>Cash Conversion Cycle</strong><br/>(<code>DIO + DSO − DPO</code>)</td><td>Total days a dollar is trapped in your supply chain. Cutting CCC by 5 days frees tens of millions in cash!</td><td style="background:#E6F4EA; color:#137333;"><strong>🔥 How Apple &amp; Amazon Achieve a NEGATIVE CCC (-30 to -60 Days):</strong> Apple sells an iPhone in 9 days (<code>DIO=9</code>), collects credit card cash in 5 days (<code>DSO=5</code>), and pays Foxconn/suppliers 80 days later (<code>DPO=80</code>) &rarr; <code>9 + 5 − 80 = -66 days CCC</code>! Apple gets customer cash 2 months before paying suppliers!</td></tr>
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
              <thead><tr><th style="width:130px;">Term</th><th style="width:220px;">Full Name Spelled Out</th><th>Why Customers Care</th><th style="width:350px;">🌍 Real-World Company Examples</th></tr></thead>
              <tbody>
                <tr><td><strong>Scope 1 &amp; 2</strong></td><td><strong>Direct Fuel &amp; Purchased Electricity</strong></td><td>Emissions from burning fuel in your own buildings/trucks (Scope 1) and buying utility power (Scope 2).</td><td style="background:#F8FAFD;"><strong>📦 Amazon &amp; 🥤 PepsiCo</strong> deploy Rivian electric delivery vans and rooftop warehouse solar panels to cut Scope 1 and Scope 2 emissions.</td></tr>
                <tr><td><strong style="color:#1E8E3E;">Scope 3</strong></td><td><strong>Value Chain Emissions (Suppliers + Freight)</strong></td><td>Makes up 80–90% of a product company’s total carbon footprint! Tracked by our <code>carbon_scope3_ledger</code> agent.</td><td style="background:#F8FAFD;"><strong>🧴 Unilever &amp; 📱 Apple:</strong> Over 85% of an iPhone’s or Dove soap bar’s carbon comes from upstream raw material suppliers and cargo flights (<strong>Scope 3</strong>).</td></tr>
                <tr><td><strong>CBAM &amp; EUDR</strong></td><td><strong>Carbon Border Adjustment Mechanism &amp; EU Deforestation Regulation</strong></td><td>European laws that tax carbon-heavy steel/aluminum imports (<strong>CBAM</strong>) and block coffee, cocoa, palm oil, or paper from deforested land (<strong>EUDR</strong>).</td><td style="background:#F8FAFD;"><strong>🍫 Nestlé, Ferrero (Nutella) &amp; ⚙️ Tata Steel:</strong> Must provide satellite GPS farm polygons for every cocoa/coffee shipment entering Europe (<strong>EUDR</strong>) and verified steel furnace carbon certificates (<strong>CBAM</strong>).</td></tr>
              </tbody>
            </table>
          </div>
        `;
      }}
    }}

    // Chapter 3: Workflows rendered as Clean Spacious Tables with Real-World Company Spotlights
    function selectWorkflow(wfKey, btn) {{
      if (btn) {{
        btn.parentElement.querySelectorAll('.g-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
      }}
      const wf = WORKFLOWS[wfKey];
      const rows = wf.steps.map(st => `
        <tr>
          <td style="font-weight:800; color:#1A73E8; width:195px;">${{st.badge}}<br/><span style="color:#202124; font-size:15.5px;">${{st.title}}</span></td>
          <td>${{st.plain}}</td>
          <td style="background:#F8FAFD; color:#202124;">${{st.real_world || ''}}</td>
          <td style="background:#FCE8E6; color:#C5221F; font-weight:500;">✕ ${{st.manual}}</td>
          <td style="background:#E6F4EA; color:#137333; font-weight:600;">✦ ${{st.ai}}</td>
        </tr>
      `).join('');
      document.getElementById('workflowMount').innerHTML = `
        <h3 style="font-family:var(--font-display); font-size:23px; margin:0 0 6px; color:#1A73E8;">${{wf.title}}</h3>
        <p style="color:var(--text-sub); margin:0 0 14px;">${{wf.subtitle}}</p>
        <div style="background:#E8F0FE; border-left:5px solid #1A73E8; border-radius:12px; padding:16px 20px; margin-bottom:18px;">
          <div style="font-weight:800; color:#174EA6; font-size:16.5px; margin-bottom:4px;">${{wf.company_case || ''}}</div>
          <div style="color:#202124; font-size:16px;">${{wf.company_summary || ''}}</div>
        </div>
        <div class="g-table-wrap">
          <table class="g-table">
            <thead>
              <tr>
                <th>Step</th>
                <th>What Happens in Plain English</th>
                <th style="width:270px;">🌍 Real-World Company Example</th>
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

    // Chapter 6: 8 Real-World Industry Sector Case Studies + All-8-Sectors Master Comparison
    let currentSectorIdx = 0;
    function stepSector(delta) {{
      const next = (currentSectorIdx + delta + SECTORS.length) % SECTORS.length;
      const btns = document.querySelectorAll('#sectorBtnRow .g-btn');
      showSectorCase(next, btns[next]);
    }}

    function showSectorCase(idx, btn) {{
      currentSectorIdx = idx;
      if (btn) {{
        document.querySelectorAll('#sectorBtnRow .g-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
      }}
      const sec = SECTORS[idx];
      const nodeSvg = sec.svgNodes.map((nd, ni) => {{
        const x = 14 + ni * 202;
        const arrow = ni < 4 ? `<text x="${{x + 190}}" y="62" fill="${{sec.color}}" font-size="18" font-weight="800">&rarr;</text>` : '';
        return `
          <g transform="translate(${{x}}, 12)">
            <rect width="184" height="94" rx="12" fill="#FFFFFF" stroke="${{sec.color}}" stroke-width="2"/>
            <text x="92" y="30" text-anchor="middle" fill="${{sec.color}}" font-size="12" font-weight="800">${{nd[0]}}</text>
            <text x="92" y="54" text-anchor="middle" fill="#202124" font-size="12" font-weight="700">${{nd[1]}}</text>
            <text x="92" y="76" text-anchor="middle" fill="#5F6368" font-size="11">${{nd[2] || ''}}</text>
          </g>
          ${{arrow}}
        `;
      }}).join('');

      const stageRows = sec.stages.map(st => `
        <tr>
          <td style="width:270px; font-weight:800; color:${{sec.color}};">${{st[0]}}</td>
          <td>${{st[1]}}</td>
        </tr>
      `).join('');

      document.getElementById('sectorCaseMount').innerHTML = `
        <div style="display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:16px;">
          <button type="button" class="g-btn" onclick="stepSector(-1)">&larr; Previous Sector</button>
          <strong style="color:${{sec.color}}; font-size:18px;">Industry Sector ${{idx + 1}} of ${{SECTORS.length}} · ${{sec.sector}}</strong>
          <button type="button" class="g-btn g-btn-primary" onclick="stepSector(1)">Next Sector &rarr;</button>
        </div>

        <div style="background:#F8F9FA; border:2px solid ${{sec.color}}; border-radius:18px; padding:26px 30px; margin-bottom:22px;">
          <div style="display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap; margin-bottom:8px;">
            <span class="g-badge" style="background:${{sec.bg}}; color:${{sec.color}}; margin:0;">${{sec.sector}}</span>
            <span class="g-badge" style="background:#FFFFFF; color:#202124; border:1px solid #DADCE0; margin:0;">🏢 Companies: ${{sec.companies}}</span>
          </div>
          <h3 style="font-family:var(--font-display); font-size:26px; margin:6px 0 8px; color:#202124;">${{sec.headline}}</h3>
          <p style="margin:0 0 16px; color:#202124; font-size:17px;">${{sec.overview}}</p>

          <!-- Key Metrics Strip Banner -->
          <div style="background:#FFFFFF; border:1px solid #DADCE0; border-left:5px solid ${{sec.color}}; border-radius:12px; padding:14px 18px; margin-bottom:18px; font-size:15.5px;">
            📊 ${{sec.metrics}}
          </div>

          <!-- 5-Node End-to-End Physical Flow SVG -->
          <svg viewBox="0 0 1020 118" style="width:100%; height:auto; display:block; margin-bottom:20px; background:${{sec.bg}}; border-radius:14px; padding:4px;">
            ${{nodeSvg}}
          </svg>

          <!-- How This Sector Uses All 7 Supply Chain Stages -->
          <h4 style="font-family:var(--font-display); font-size:20px; margin:0 0 10px; color:${{sec.color}};">
            🔍 Step-by-Step: How ${{sec.companies}} Use Each Stage of the Supply Chain
          </h4>
          <div class="g-table-wrap">
            <table class="g-table">
              <thead>
                <tr>
                  <th>Supply Chain Stage</th>
                  <th>How Companies in This Sector Execute This Stage in the Real World</th>
                </tr>
              </thead>
              <tbody>
                ${{stageRows}}
                <tr>
                  <td style="font-weight:800; color:#1E8E3E;">🤖 Top AI Agents Used by This Sector</td>
                  <td style="background:#E6F4EA; color:#137333; font-weight:700;">${{sec.agents}}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      `;
    }}

    function showAllSectorsComparison(btn) {{
      if (btn) {{
        document.querySelectorAll('#sectorBtnRow .g-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
      }}
      const rows = SECTORS.map((s) => `
        <tr>
          <td style="font-weight:800; color:${{s.color}}; width:210px;">${{s.sector}}</td>
          <td style="font-weight:700; width:190px;">${{s.companies}}</td>
          <td><strong>${{s.headline}}</strong><br/><span style="color:#5F6368; font-size:15px;">${{s.overview}}</span></td>
          <td style="background:#F8FAFD; width:270px; font-size:15px;">${{s.metrics}}</td>
          <td style="background:#E6F4EA; color:#137333; font-weight:600; width:220px; font-size:14.5px;">${{s.agents}}</td>
        </tr>
      `).join('');
      document.getElementById('sectorCaseMount').innerHTML = `
        <h3 style="font-family:var(--font-display); font-size:24px; margin:0 0 12px; color:#1E8E3E;">
          📊 Master Side-by-Side Comparison: How All 8 Industry Sectors Run Their Supply Chains
        </h3>
        <div class="g-table-wrap">
          <table class="g-table">
            <thead>
              <tr>
                <th>Industry Sector</th>
                <th>Iconic Companies</th>
                <th>How Their Supply Chain Works End-to-End</th>
                <th>Key Metrics (DIO, DSO, DPO, CCC &amp; OTIF)</th>
                <th>Top AI Agents Used</th>
              </tr>
            </thead>
            <tbody>${{rows}}</tbody>
          </table>
        </div>
      `;
    }}

    showStageTable(0);
    renderBwTable();
    showConceptDiagram(0);
    selectWorkflow('sop');
    renderTerms();
    renderDecoderTable();
    renderOneQuiz();
    showSectorCase(0);
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

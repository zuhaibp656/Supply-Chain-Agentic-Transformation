#!/usr/bin/env python3
"""Enhance Vertical 7 (Trade Marketing & Distribution / TM&D) with dedicated,
industry-standard personas, agents, and unique SVG watermarks.

Restores FleetFlow & Fleet Dispatch Manager to Vertical 6 (Logistics & Fleet).
Ensures all 8 verticals have 100% unique watermark types, distinct personas,
and dedicated agentic solutions.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "data" / "supply_chain_catalog.json"
PERIODIC_PATH = ROOT / "data" / "periodic_table_elements.json"


def update_catalog():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        cat = json.load(f)

    # 1. Update Departments
    depts = cat["departments"]

    # V4: Inventory & MEIO -> unique watermark multi_echelon_buffer
    if "inventory_meio" in depts:
        depts["inventory_meio"]["watermarkType"] = "multi_echelon_buffer"

    # V6: Logistics & Fleet -> restore fleet_dispatch_mgr and fleetflow_dispatch
    if "logistics_fleet" in depts:
        v6 = depts["logistics_fleet"]
        if "fleet_dispatch_mgr" not in v6["personaIds"]:
            v6["personaIds"].insert(0, "fleet_dispatch_mgr")
        if "fleetflow_dispatch" not in v6["agentIds"]:
            v6["agentIds"].insert(0, "fleetflow_dispatch")

    # V7: Trade Marketing & Distribution -> Dedicated personas, agents & watermark
    tmd_persona_ids = [
        "tmd_merchandising_mgr",
        "area_sales_field_ops_lead",
        "distributor_claims_settlement_spec",
    ]
    tmd_agent_ids = [
        "field_beat_distributor_sync_agent",
        "planogram_merchandising_vision_auditor",
        "trade_scheme_claims_reconciler",
    ]

    depts["trade_mkt_dist"] = {
        "id": "trade_mkt_dist",
        "vNum": "V7",
        "scorBadge": "VERTICAL 07 · TM&D & LAST-MILE",
        "name": "Trade Marketing & Distribution / TM&D",
        "fullName": "Vertical 7: Trade Marketing & Distribution / TM&D (The Last-Mile Push)",
        "tagline": "The Last-Mile Push",
        "subtitle": "Secondary distribution, FSO beat planning, distributor live stock & planogram audits",
        "color": "#f59e0b",
        "watermarkType": "tmd_retail_network",
        "horizon": "Daily Field Execution",
        "coreQuestion": "How do we push inventory through distributors to millions of retail counters, optimize FSO beats, and prevent stockout pitches?",
        "river": "Terminal Interface of River 1 (Retail Shelf) and River 2 (Consumer POS / Sell-Through)",
        "systems": "DMS (Distributor Management Systems) · SFA Mobile Handhelds · Google Maps Platform Routes · Modern Trade JBP Portals · BigQuery · AlloyDB · Apigee",
        "solverSummary": "Google Maps Routes Preferred CVRPTW Beat Sequencer + Real-Time DMS Inventory Reconciliation Broker + Multimodal Vision Planogram Auditor + Secondary Sales Slab Reconciler",
        "toilMetric": "Field sales pitching out-of-stock SKUs",
        "toilBullets": [
            "Field Sales Officers (FSOs) waste 30%+ of store visits booking orders for SKUs currently out of stock at the distributor",
            "Manual store visibility audits rely on unverified photos, allowing retailer planogram violations and unearned trade payouts",
            "Sub-optimal distributor beat routes cause delayed delivery to high-velocity kirana stores, triggering retail stockouts"
        ],
        "impactMetric": "+18.4% Distributor Case Fill & Zero Lost Visits",
        "impactBullets": [
            "Real-time reconciliation of FSO focus target SKUs with live distributor stock, automatically substituting available variants",
            "Multimodal vision auditing of retail shelf photos verifies planogram compliance and automates scheme discount approvals",
            "Google Maps Fleet Engine beat routing ensures 100% scheduled store coverage and accelerates secondary reorders"
        ],
        "kpis": "Effective Store Coverage % | Distributor Case Fill Rate % | Retail Planogram Compliance %",
        "personaIds": tmd_persona_ids,
        "agentIds": tmd_agent_ids,
        "l1toL3": {
            "mandate": "Directs secondary distribution through authorized distributors and wholesalers to General Trade (kirana), Modern Trade, and Quick-Commerce dark stores.",
            "mtoVsMts": "High-velocity Make-to-Stock replenishment driven by daily store beat orders, distributor buffer norms, and localized trade promotion schemes.",
            "battleground": "Maximizing retailer on-shelf availability (OSA) and share-of-shelf (SOS) while preventing distributor stockouts and trade spend claim leakage.",
            "dataObjects": "Distributor Master, Retail Outlet Registry, Secondary Sales Orders, Beat Schedules, Scheme Slab Rate Cards, Shelf Images."
        }
    }

    # 2. Update Personas in Catalog
    personas = cat["personas"]

    # Ensure fleet_dispatch_mgr is mapped to logistics_fleet
    if "fleet_dispatch_mgr" in personas:
        personas["fleet_dispatch_mgr"]["deptId"] = "logistics_fleet"
        personas["fleet_dispatch_mgr"]["role"] = "Road Fleet & Primary/Secondary Linehaul Dispatch Manager"
        personas["fleet_dispatch_mgr"]["agentIds"] = ["fleetflow_dispatch", "load_consolidation_agent"]

    # Add 3 Dedicated TM&D Personas
    personas["tmd_merchandising_mgr"] = {
        "id": "tmd_merchandising_mgr",
        "deptId": "trade_mkt_dist",
        "icon": "🏪",
        "name": "Trade Marketing & Merchandising Manager",
        "role": "Retail Planograms, Share of Shelf (SOS) & Visibility Agreements",
        "summary": "Owns in-store visibility, brand planogram execution, Share-of-Shelf (SOS) targets, and modern trade key account visibility agreements across supermarket aisles, chillers, and quick-commerce dark stores.",
        "focusAreas": [
            "Planogram Compliance",
            "Share of Shelf (SOS) Auditing",
            "Modern Trade JBP Execution",
            "POS Merchandiser Deployment"
        ],
        "headlineStat": "98.7%",
        "headlineLabel": "Planogram Audit Compliance (vs. 61% Manual)",
        "toilHoursBefore": "6.0 hrs/day manual store photo review & dispute handling",
        "toilHoursAfter": "30 mins/day strategic visibility review",
        "agentIds": [
            "planogram_merchandising_vision_auditor",
            "trade_scheme_claims_reconciler"
        ],
        "dayInLife": [
            {
                "time": "8:30 AM",
                "task": "Overnight Retail Shelf Photo Intake & OCR Triage",
                "isToil": True,
                "toilTime": "2.0 hrs",
                "afterTime": "5 mins",
                "before": "Scrolls through hundreds of unorganized WhatsApp and field app photos trying to verify eye-level shelf facings.",
                "after": "ShelfVision multimodal agent auto-aligns, detects SKU facings, and scores planogram compliance with Gemini 3.8 Flash in seconds.",
                "agentId": "planogram_merchandising_vision_auditor"
            },
            {
                "time": "11:00 AM",
                "task": "Share-of-Shelf (SOS) vs. Competitor Encroachment Analysis",
                "isToil": True,
                "toilTime": "1.5 hrs",
                "afterTime": "10 mins",
                "before": "Manually counts competitor facings on paper sheets to determine if promotional end-caps breached contractual terms.",
                "after": "Reviews automated bounding-box heatmaps displaying exact Share-of-Shelf percentages and encroachment alerts.",
                "agentId": "planogram_merchandising_vision_auditor"
            },
            {
                "time": "2:30 PM",
                "task": "Retailer Visibility Scheme Incentive Reconciliation",
                "isToil": True,
                "toilTime": "2.0 hrs",
                "afterTime": "10 mins",
                "before": "Argues with modern trade key account managers over disputed visibility deductions and missing compliance proof.",
                "after": "SchemeGuard correlates verified shelf images with contractual payout slabs and issues audit-ready settlement credit notes.",
                "agentId": "trade_scheme_claims_reconciler"
            },
            {
                "time": "4:30 PM",
                "task": "Regional Planogram Optimization & Merchandiser Dispatch",
                "isToil": False,
                "activity": "Reallocates merchandiser routes to stores with persistent shelf execution gaps before weekend peak footfall.",
                "tag": "Execution Strategy"
            }
        ]
    }

    personas["area_sales_field_ops_lead"] = {
        "id": "area_sales_field_ops_lead",
        "deptId": "trade_mkt_dist",
        "icon": "🛵",
        "name": "Area Sales & Field Beat Operations Lead",
        "role": "FSO Beat Optimization, Store Coverage & Live Distributor Inventory Sync",
        "summary": "Manages distributor sales reps and Field Sales Officers (FSOs) across retail beats—reconciling daily store calls with live distributor stock so reps never pitch out-of-stock SKUs and maximize productive call strike rates.",
        "focusAreas": [
            "Daily FSO Beat Routing",
            "Live DMS Stock Reconciliation",
            "Zero Out-of-Stock Pitches",
            "Kirana Counter Coverage"
        ],
        "headlineStat": "+18.4%",
        "headlineLabel": "Distributor Case Fill Rate (Zero OOS Pitches)",
        "toilHoursBefore": "5.5 hrs/day handling stockout cancellations & manual beat planning",
        "toilHoursAfter": "40 mins/day high-value commercial steering",
        "agentIds": [
            "field_beat_distributor_sync_agent",
            "planogram_merchandising_vision_auditor"
        ],
        "dayInLife": [
            {
                "time": "7:30 AM",
                "task": "Daily FSO Beat Allocation & Route Sequencing",
                "isToil": True,
                "toilTime": "1.5 hrs",
                "afterTime": "5 mins",
                "before": "FSOs follow static paper beat sheets, hitting retail stores during peak unloading rush or when owners are away.",
                "after": "BeatSync dynamically sequences retail store beats with Google Maps Routes Preferred API based on traffic and owner availability.",
                "agentId": "field_beat_distributor_sync_agent"
            },
            {
                "time": "9:30 AM",
                "task": "Real-Time Distributor Stock Re-Check During Store Calls",
                "isToil": True,
                "toilTime": "2.5 hrs",
                "afterTime": "5 mins",
                "before": "FSOs pitch promotional SKUs only to discover at afternoon delivery that the distributor ran out, canceling 25% of lines.",
                "after": "BeatSync checks live DMS stock upon store check-in, swapping out-of-stock items with available high-margin sister SKUs.",
                "agentId": "field_beat_distributor_sync_agent"
            },
            {
                "time": "1:30 PM",
                "task": "Mid-Day Secondary Order Sync & Van Dispatch Handoff",
                "isToil": True,
                "toilTime": "1.5 hrs",
                "afterTime": "10 mins",
                "before": "Batches paper order forms at end of day, delaying picking and next-morning van loading.",
                "after": "Streams verified orders into distributor DMS instantly, generating pick-lists and van load sequences in real time.",
                "agentId": "field_beat_distributor_sync_agent"
            },
            {
                "time": "4:00 PM",
                "task": "Field Sales Strike Rate & Productive Call Coaching",
                "isToil": False,
                "activity": "Reviews rep performance dashboards, coaching FSOs on slow-moving line cross-selling and outlet expansion.",
                "tag": "Commercial Leadership"
            }
        ]
    }

    personas["distributor_claims_settlement_spec"] = {
        "id": "distributor_claims_settlement_spec",
        "deptId": "trade_mkt_dist",
        "icon": "📑",
        "name": "Distributor Commercial & Scheme Settlement Specialist",
        "role": "Secondary Sales Slabs, Trade Promotion Settlement & Claim Auditing",
        "summary": "Governs distributor commercial claims, secondary sales volume slabs, turnover incentives, and promotional discounts—eliminating phantom billing and automating credit note disbursements.",
        "focusAreas": [
            "Secondary Sales Verification",
            "Tiered Volume Slab Rebates",
            "Phantom Billing Detection",
            "SAP Credit Memo Lock"
        ],
        "headlineStat": "45d → <2h",
        "headlineLabel": "Claim Settlement Cycle Time & Zero Leakage",
        "toilHoursBefore": "6.5 hrs/day manual invoice reconciliation in Excel",
        "toilHoursAfter": "30 mins/day exception approval",
        "agentIds": [
            "trade_scheme_claims_reconciler",
            "field_beat_distributor_sync_agent"
        ],
        "dayInLife": [
            {
                "time": "8:30 AM",
                "task": "Distributor Secondary Sales & Tax Invoice Intake",
                "isToil": True,
                "toilTime": "2.0 hrs",
                "afterTime": "5 mins",
                "before": "Downloads hundreds of secondary sales CSVs and invoice scans from disparate distributor DMS databases.",
                "after": "SchemeGuard auto-ingests secondary sales records and reconciles them against distributor opening/closing stock.",
                "agentId": "trade_scheme_claims_reconciler"
            },
            {
                "time": "11:00 AM",
                "task": "Promotional Slab Verification & Phantom Claim Auditing",
                "isToil": True,
                "toilTime": "2.5 hrs",
                "afterTime": "10 mins",
                "before": "Manually validates whether each retailer reached volume slab thresholds; misses inflated quantities and duplicate claims.",
                "after": "Algorithms detect phantom billing anomalies, calculate exact slab discounts, and flag unearned claims.",
                "agentId": "trade_scheme_claims_reconciler"
            },
            {
                "time": "2:30 PM",
                "task": "Credit Memo Approval & SAP S/4HANA Write-Back",
                "isToil": True,
                "toilTime": "1.5 hrs",
                "afterTime": "5 mins",
                "before": "Enters manual debit/credit memos into SAP FI/SD one by one, creating a 45-day payment backlog for distributors.",
                "after": "Approved claims generate SAP credit notes automatically via Apigee, releasing funds to distributors in under 2 hours.",
                "agentId": "trade_scheme_claims_reconciler"
            },
            {
                "time": "4:00 PM",
                "task": "Distributor Working Capital Health Review",
                "isToil": False,
                "activity": "Meets with commercial finance to optimize distributor credit limits and seasonal trade incentive designs.",
                "tag": "Commercial Governance"
            }
        ]
    }

    # 3. Update Agents in Catalog
    agents = cat["agents"]

    # Ensure fleetflow_dispatch is mapped to logistics_fleet
    if "fleetflow_dispatch" in agents:
        agents["fleetflow_dispatch"]["deptId"] = "logistics_fleet"

    # Add 3 Dedicated TM&D Agents
    agents["field_beat_distributor_sync_agent"] = {
        "id": "field_beat_distributor_sync_agent",
        "deptId": "trade_mkt_dist",
        "name": "BeatSync — Field Sales & Distributor Inventory Harmonizer",
        "shortDesc": "Synchronizes daily FSO beat routes with live Distributor Management System (DMS) inventory in real time, auto-substituting in-stock promotional variants and optimizing store visit sequences.",
        "badge": "Zero OOS Pitches · +18% Fill",
        "cadType": "tmd_retail_network",
        "videoSrc": "videos/f2f_fleet_demo.mp4",
        "hasPreloadedVideo": True,
        "systems": "DMS (Distributor Management Systems) · SFA Mobile Handhelds · Google Maps Routes Preferred API · SAP SD · BigQuery · AlloyDB",
        "solverStack": "Google Maps Routes Preferred CVRPTW Beat Sequencer + Real-Time DMS Inventory Reconciliation Broker + Smart Variant Recommender",
        "apiWriteback": "Live Handheld SKU Catalog Override, Secondary Order Booking in DMS & Optimized Daily Route Sheet",
        "roiMetrics": [
            {
                "val": "+18.4%",
                "label": "Distributor Case Fill Rate",
                "sub": "Eliminates cancelled orders by checking live warehouse stock before rep pitch",
                "color": "#10b981"
            },
            {
                "val": "0%",
                "label": "Out-of-Stock Pitches",
                "sub": "Auto-suggests high-margin in-stock sister pack sizes upon store check-in",
                "color": "#f59e0b"
            },
            {
                "val": "+22%",
                "label": "Productive Calls / Day",
                "sub": "Sequences store visits via Google Maps Routes Preferred API to cut travel time",
                "color": "#38bdf8"
            },
            {
                "val": "<15s",
                "label": "Order-to-DMS Sync",
                "sub": "Streams booked secondary orders directly into distributor picking queue",
                "color": "#a855f7"
            }
        ],
        "customerProof": "ITC Foods & FMCG Field Operations (Google Maps Platform + BigQuery · +18.4% distributor case fill rate · zero stockout pitch waste · 22% increase in daily store calls).",
        "dataSegments": {
            "private": "Distributor Management System (DMS) inventory balances, retailer order history, credit limits & price lists in BigQuery & AlloyDB",
            "community": "Daily FSO GPS check-ins, store geo-coordinates, distributor delivery van schedules & order cutoffs",
            "public": "Google Maps Live Traffic, local market holiday calendars, festival demand surges & weather conditions"
        },
        "subAgents": [
            {
                "name": "Live DMS Stock Validator",
                "role": "Reconciles SKU catalog against real-time distributor warehouse inventory before each store call"
            },
            {
                "name": "Smart Variant Recommender",
                "role": "Dynamically swaps out-of-stock items with high-margin, in-stock promotional sister pack sizes"
            },
            {
                "name": "Dynamic Beat Route Optimizer",
                "role": "Re-sequences daily retail store calls with Google Maps Routes Preferred API to maximize productive strike rate"
            }
        ],
        "problem": "Field Sales Officers (FSOs) waste 30%+ of daily store visits booking orders for SKUs that are out-of-stock at the local distributor warehouse—causing delivery stockouts, wasted trips, and lost retailer trust.",
        "solution": "Synchronizes daily FSO beat routes with live Distributor Management System (DMS) inventory in real time. If a SKU is stocked out, BeatSync dynamically swaps it on the sales rep's mobile SFA app with available high-margin variants or promotional sister pack sizes, and sequences visits using Google Maps Routes Preferred API.",
        "advantage": "Drives +18.4% distributor case fill rate, eliminates out-of-stock pitches, and boosts daily productive store calls per FSO by 22%."
    }

    agents["planogram_merchandising_vision_auditor"] = {
        "id": "planogram_merchandising_vision_auditor",
        "deptId": "trade_mkt_dist",
        "name": "ShelfVision — Retail Planogram & Visibility Auditor",
        "shortDesc": "Multimodal vision agent powered by Gemini 3.8 Flash that inspects retail shelf and chiller photos captured by field reps, measuring brand facings, Share of Shelf (SOS), and competitor encroachment.",
        "badge": "98.7% Vision Audit · -85% Time",
        "cadType": "tmd_retail_network",
        "videoSrc": "videos/smart_warehouse_demo.mp4",
        "hasPreloadedVideo": True,
        "systems": "SFA Camera Uploads · Cloud Storage · Gemini 3.8 Flash Multimodal Vision · BigQuery · Planogram Master Repositories · AlloyDB pgvector",
        "solverStack": "Vertex AI Multimodal Vision Object & Facing Detection + Share-of-Shelf Planogram Compliance Classifier",
        "apiWriteback": "Store Planogram Audit Scorecard, Retailer Visibility Incentive Approval & Penalty Dispute Memo",
        "roiMetrics": [
            {
                "val": "98.7%",
                "label": "Planogram Audit Accuracy",
                "sub": "Detects brand facings, eye-level placement & competitor encroachment with Gemini 3.8 Flash",
                "color": "#10b981"
            },
            {
                "val": "-85%",
                "label": "Audit Cycle Time",
                "sub": "Compresses weeks of manual sampling into instant sub-second shelf classification",
                "color": "#38bdf8"
            },
            {
                "val": "$4.2M",
                "label": "Unearned Payouts Saved",
                "sub": "Prevents scheme payouts to non-compliant retail stores with verifiable photo audit evidence",
                "color": "#f59e0b"
            },
            {
                "val": "100%",
                "label": "Store Audit Coverage",
                "sub": "Evaluates 100% of store visibility photos rather than 5% sample audits",
                "color": "#a855f7"
            }
        ],
        "customerProof": "Global FMCG Retail Execution Benchmarks (Gemini 3.8 Flash Multimodal Vision · 98.7% planogram audit accuracy · weeks → sub-second audit cycle · $4.2M saved in unearned visibility payouts).",
        "dataSegments": {
            "private": "Official brand planogram CAD templates, store contract agreements & historical audit scorecards in AlloyDB & BigQuery",
            "community": "Store shelf photos taken by field reps, geo-tagged mobile uploads & retailer master registry",
            "public": "Competitor brand packaging catalogs & standard retail aisle lighting normalization models"
        },
        "subAgents": [
            {
                "name": "Multimodal Shelf Image Normalizer",
                "role": "Automatically cleans, de-skews, and aligns wide-angle shelf photos uploaded by field reps"
            },
            {
                "name": "SKU Facing & SOS Detector",
                "role": "Counts brand facings, detects eye-level placements, and calculates exact Share-of-Shelf vs. competitors"
            },
            {
                "name": "Payout Deduction Calculator",
                "role": "Compares detected facings against contractual retailer planogram terms and computes approved visibility payouts"
            }
        ],
        "problem": "FMCG brands spend millions on retailer visibility schemes, but manual audits of thousands of messy store photos take weeks, allowing widespread planogram violations and unearned payout leakages.",
        "solution": "Multimodal vision agent powered by Gemini 3.8 Flash that inspects retail shelf, chiller, and end-cap photos captured by field sales reps during store visits. Measures brand facings, Share of Shelf (SOS), and competitor encroachment against corporate planogram rules.",
        "advantage": "Delivers 98.7% planogram audit accuracy, compresses audit cycles from weeks to sub-seconds, and prevents $4.2M in unearned retailer visibility payouts."
    }

    agents["trade_scheme_claims_reconciler"] = {
        "id": "trade_scheme_claims_reconciler",
        "deptId": "trade_mkt_dist",
        "name": "SchemeGuard — Secondary Trade Payout & Claims Sentinel",
        "shortDesc": "Reconciles distributor secondary sales invoices against corporate trade promotion schemes, volume slabs, and seasonal incentive agreements to prevent phantom billing and issue instant credit notes.",
        "badge": "45 Days → <2 Hrs · Zero Leakage",
        "cadType": "tmd_retail_network",
        "videoSrc": "videos/demand_sensing_demo.mp4",
        "hasPreloadedVideo": True,
        "systems": "SAP S/4HANA SD/FI · Distributor DMS Portals · Secondary Sales Ledgers in BigQuery & AlloyDB · Apigee APIs · Document AI",
        "solverStack": "Deterministic Secondary Sales Volume Slab Engine + BigQuery Phantom Invoice Anomaly Classifier + ERP Credit Note Broker",
        "apiWriteback": "SAP S/4HANA Credit Memo (FB01/VF01), Distributor Statement Reconciliation & Instant Settlement Notice",
        "roiMetrics": [
            {
                "val": "<2 Hours",
                "label": "Claim Settlement Time",
                "sub": "Compresses 45-day manual spreadsheet reconciliation into instant automated validation",
                "color": "#10b981"
            },
            {
                "val": "99.8%",
                "label": "Dispute-Free Payouts",
                "sub": "Eliminates distributor deduction disputes with line-item mathematical proof",
                "color": "#38bdf8"
            },
            {
                "val": "$6.8M",
                "label": "Claim Leakage Prevented",
                "sub": "Detects phantom billing, duplicate invoices & unearned volume slab claims before payout",
                "color": "#f59e0b"
            },
            {
                "val": "100%",
                "label": "Audit-Ready Trail",
                "sub": "Links every credit note directly to verified secondary tax invoices and contract rate cards",
                "color": "#a855f7"
            }
        ],
        "customerProof": "Enterprise CPG Trade Spend Management (Claim settlement compressed from 45 days to <2 hours · 99.8% dispute-free payouts · $6.8M prevented claim leakage).",
        "dataSegments": {
            "private": "Approved corporate trade scheme agreements, volume slab tables, SAP credit memos & distributor ledgers in BigQuery",
            "community": "Distributor secondary sales tax invoices, retailer purchase receipts & DMS transaction logs",
            "public": "GST / tax compliance portals & banking disbursement API payment rails"
        },
        "subAgents": [
            {
                "name": "Secondary Invoice Validator",
                "role": "Verifies retailer tax invoices against distributor opening/closing stock to detect phantom billing"
            },
            {
                "name": "Tiered Slab Incentive Engine",
                "role": "Computes exact volume-based discounts and special promotional scheme credits per trade contract"
            },
            {
                "name": "Autonomous ERP Credit Broker",
                "role": "Drafts validated credit memos in SAP S/4HANA and posts instant settlement notifications to distributor portals"
            }
        ],
        "problem": "Distributor trade promotion claims and volume slabs are reconciled manually over 45-day cycles, tying up distributor working capital and leaking millions to phantom invoices and duplicate claims.",
        "solution": "Continuously reconciles distributor secondary sales invoices against corporate trade promotion schemes, volume slabs, and seasonal incentive agreements. Cross-references secondary sales data against opening/closing stock balances to detect phantom billing before payouts are released.",
        "advantage": "Compresses distributor claim settlement from 45 days to <2 hours with 99.8% dispute-free payouts, saving $6.8M in fraudulent or unearned claim leakages."
    }

    # 4. Update metadata counts
    cat["metadata"]["personasCount"] = len(personas)
    cat["metadata"]["agentsCount"] = len(agents)
    cat["metadata"]["domainAgentsCount"] = len(agents) - cat["metadata"]["universalAgentsCount"]
    cat["metadata"]["verticalsCount"] = 8
    cat["metadata"]["scorVerticalsCount"] = 8

    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(cat, f, indent=2, ensure_ascii=False)
    print(f"Updated {CATALOG_PATH}: {len(depts)} verticals, {len(personas)} personas, {len(agents)} agents.")


def update_periodic():
    with open(PERIODIC_PATH, "r", encoding="utf-8") as f:
        p_data = json.load(f)

    # Re-build elements list cleanly from catalog
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        cat = json.load(f)

    agents = cat["agents"]

    # Map groups in order: universal_csco, demand_sop, sourcing_procurement, manufacturing_prod, inventory_meio, warehousing_qa, logistics_fleet, trade_mkt_dist, reverse_risk_esg
    group_order = [
        "universal_csco",
        "demand_sop",
        "sourcing_procurement",
        "manufacturing_prod",
        "inventory_meio",
        "warehousing_qa",
        "logistics_fleet",
        "trade_mkt_dist",
        "reverse_risk_esg",
    ]

    elements = []
    idx = 1
    for grp in group_order:
        grp_agents = [a for a in agents.values() if a.get("deptId") == grp or (grp == "universal_csco" and a.get("isUniversal"))]
        for ag in grp_agents:
            # Determine code & symbol
            code = f"{idx:02d}"
            sym = ag["name"][:2].capitalize()
            short_name = ag["name"].split(" — ")[0]
            elem = {
                "atomicNumber": code,
                "symbol": sym,
                "shortName": short_name,
                "group": grp,
                "agentId": ag["id"],
                "fullName": ag["name"],
                "kpiBadge": ag["badge"],
                "problem": ag["problem"],
                "solution": ag["solution"],
                "solverStack": ag["solverStack"],
                "subAgents": ag.get("subAgents", [])
            }
            elements.append(elem)
            idx += 1

    p_data["elements"] = elements
    with open(PERIODIC_PATH, "w", encoding="utf-8") as f:
        json.dump(p_data, f, indent=2, ensure_ascii=False)
    print(f"Updated {PERIODIC_PATH}: {len(elements)} elements across 9 groups.")


if __name__ == "__main__":
    update_catalog()
    update_periodic()

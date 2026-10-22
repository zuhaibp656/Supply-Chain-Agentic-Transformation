#!/usr/bin/env python3
"""
Consolidates the supply chain suite catalog and periodic table back to the
canonical 6 ASCM SCOR Pillars while retaining all 29 personas and 35 agents.

Pillars:
  01 · PLAN (demand_sop)
  02 · SOURCE (sourcing_procurement)
  03 · MAKE (manufacturing_prod)
  04 · FULFILL (inventory_warehouse) - consolidates inventory_meio + warehousing_qa
  05 · DELIVER (logistics_fleet) - consolidates logistics_fleet + trade_mkt_dist
  06 · RETURN & ENABLE (circular_enable) - consolidates reverse_risk_esg
  Plus: Universal CSCO Core (4 flagship copilots)
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "data" / "supply_chain_catalog.json"
PERIODIC_PATH = ROOT / "data" / "periodic_table_elements.json"

def consolidate_catalog():
    print(f"Loading {CATALOG_PATH}...")
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        cat = json.load(f)

    # 1. Update metadata
    cat["metadata"]["scorVerticalsCount"] = 6
    cat["metadata"]["verticalsCount"] = 6
    cat["metadata"]["personasCount"] = 29
    cat["metadata"]["agentsCount"] = 35
    cat["metadata"]["universalAgentsCount"] = 4
    cat["metadata"]["domainAgentsCount"] = 31

    # 2. Consolidate departments
    departments = {
        "demand_sop": {
            "id": "demand_sop",
            "vNum": "01",
            "scorBadge": "SCOR 01 · PLAN",
            "name": "Plan (Demand Planning, Sensing & S&OP)",
            "fullName": "Pillar 1: Plan — Demand Planning, Sensing & S&OP (The Forecasters)",
            "tagline": "The Forecasters",
            "subtitle": "Demand sensing, 45-min S&OP consensus, promo elasticity & retail CPFR",
            "color": "#10b981",
            "watermarkType": "demand_wave",
            "horizon": "Tactical Horizon (Weekly – 18 Months)",
            "coreQuestion": "What, how much, when, and where will customers buy, and how do we align cross-functional capacity before spending capital?",
            "systems": "SAP IBP · Blue Yonder Demand · Anaplan · Vertex AI TimesFM · BigQuery · AlloyDB",
            "solverSummary": "Vertex AI TimesFM Foundation Model + BigQuery ML ARIMA-Plus + Optuna Hyperparameter Tuner + Bayesian Price Elasticity Solver + Gemini 3.1 Pro Multi-Agent Consensus Synthesizer",
            "toilMetric": "4 weeks of manual Excel rollups per S&OP cycle",
            "toilBullets": [
                "Planners burn 40+ hours per month chasing sales reps and marketing for offline promotional spreadsheets with conflicting numbers",
                "Statistical baseline models fail to capture real-time weather shocks, social sentiment, macro inflation, and localized demand swings",
                "Executive S&OP meetings debate whose numbers are correct rather than evaluating pre-computed, P&L-optimized scenario choices"
            ],
            "impactMetric": "+28% Forecast Accuracy & 45-Min S&OP Cycle",
            "impactBullets": [
                "Autonomous ingestion and reconciliation of 40+ external demand signals in BigQuery, slashing forecast WAPE by 28%",
                "Multi-agent S&OP scenario simulation evaluates Revenue, Margin, Service Level, and Working Capital trade-offs in 45 minutes",
                "Dynamic promotional lift modeling isolates cannibalization and halo effects, saving $14M annually in misallocated trade spend"
            ],
            "kpis": "Forecast Accuracy / WAPE | S&OP Cycle Time | Bias % | Promo ROI",
            "personaIds": [
                "demand_planning_dir",
                "sop_ibp_lead",
                "promo_launch_planner",
                "cpfr_channel_mgr"
            ],
            "agentIds": [
                "demand_sensing_agent",
                "sop_scenario_weaver",
                "promo_lift_simulator",
                "cpfr_sync_agent"
            ],
            "flow": "Demand & Information Signal Flow (Upstream ◀──)"
        },
        "sourcing_procurement": {
            "id": "sourcing_procurement",
            "vNum": "02",
            "scorBadge": "SCOR 02 · SOURCE",
            "name": "Source (Strategic Sourcing & Category Procurement)",
            "fullName": "Pillar 2: Source — Strategic Sourcing & Category Procurement (The Buyers)",
            "tagline": "The Buyers",
            "subtitle": "Parametric should-cost RFQ, Tier-N Spanner graph, contract SLAs & inbound AQL QA",
            "color": "#a142f4",
            "watermarkType": "supplier_graph",
            "horizon": "Strategic & Operational Horizon",
            "coreQuestion": "Who do we buy from at what cost, under what geopolitical and ESG risks, and how do we ensure component availability across Tier-N suppliers?",
            "systems": "SAP Ariba · Coupa · Cloud Spanner Graph · AlloyDB + pgvector · Dun & Bradstreet · Resilinc",
            "solverSummary": "Parametric Should-Cost Bottom-Up Breakdown Engine + Cloud Spanner Graph N-Tier Lineage Tracer + LLM Contract Clause Extractor (Gemini 3.1 Pro) + Supplier Risk Multi-Criteria Classifier",
            "toilMetric": "6 weeks of manual RFQ negotiation & blind Tier-N risk",
            "toilBullets": [
                "Buyers negotiate blind without bottom-up material should-cost models, overpaying suppliers 8–15% on custom fabricated parts",
                "Zero visibility past Tier-1 suppliers leaves companies blindsided when a single Tier-3 resin or chip supplier halts global production",
                "Contract compliance, ESG audits, and certificate of analysis (COA) verification require weeks of manual document review"
            ],
            "impactMetric": "-14.2% Procurement Cost & Zero Tier-N Blindspots",
            "impactBullets": [
                "Real-time parametric should-cost models dynamically recalculate fair prices against live raw material indices (LME, ICIS, energy)",
                "Graph neural network on Cloud Spanner maps 4 tiers of supplier dependencies, identifying single-source bottlenecks before disruptions strike",
                "Autonomous RFQ drafting, negotiation agent, and clause compliance verification reduce contracting cycle time by 72%"
            ],
            "kpis": "Purchase Price Variance (PPV) | Sourcing Cycle Time | Supplier OTIF % | Tier-N Risk Score",
            "personaIds": [
                "category_sourcing_mgr",
                "supplier_risk_lead",
                "tariff_compliance_spec",
                "supplier_quality_lead"
            ],
            "agentIds": [
                "rfq_should_cost_agent",
                "tier_n_risk_sentinel",
                "tariff_esg_agent",
                "supplier_quality_sentinel"
            ],
            "flow": "Physical Material Flow (Raw Materials Sourcing ──▶)"
        },
        "manufacturing_prod": {
            "id": "manufacturing_prod",
            "vNum": "03",
            "scorBadge": "SCOR 03 · MAKE",
            "name": "Make (Production Planning & Manufacturing / MPS)",
            "fullName": "Pillar 3: Make — Production Planning & Manufacturing / MPS (The Makers)",
            "tagline": "The Makers",
            "subtitle": "Finite MPS line scheduling, predictive spindle OEE, inline SPC yield & ECO cutover",
            "color": "#3b82f6",
            "watermarkType": "plant_oee",
            "horizon": "Tactical to Shift-Level Execution",
            "coreQuestion": "How do we manufacture the right products on the right lines at maximum OEE, minimal scrap, and zero unplanned downtime?",
            "systems": "Siemens Opcenter · Rockwell FactoryTalk · SAP PP/MES · BigQuery ML · Vertex AI AutoML",
            "solverSummary": "OR-Tools CP-SAT Finite Capacity Job Shop Scheduler + Vibration Spectral Predictive Maintenance (BigQuery ML) + Gemini 3.8 Flash Vision Inline QA Inspector + BOM Delta Topology Engine",
            "toilMetric": "18 hours of daily rescheduling & reactive machine downtime",
            "toilBullets": [
                "Production schedulers spend hours manually reshuffling line schedules on spreadsheets whenever emergency orders or breakdowns occur",
                "Unplanned machine breakdowns cost up to $260K/hour because maintenance teams react to failures rather than predicting bearing wear",
                "Inline scrap and defect root-cause analysis is performed days after production runs, leaving thousands of defective units produced"
            ],
            "impactMetric": "+22.5% Plant OEE & -34% Scrap Defects",
            "impactBullets": [
                "Constraint Programming (OR-Tools CP-SAT) sequences jobs in <30 seconds, minimizing changeovers, cleanings, and energy peaks",
                "Edge vibration and acoustic telemetry analysis predicts spindle/bearing failures 72 hours early, preventing line stoppages",
                "Gemini 3.8 Flash multimodal vision performs sub-second inline defect classification, triggering automated diverter gates"
            ],
            "kpis": "Overall Equipment Effectiveness (OEE) | Schedule Adherence % | Scrap Rate % | First Pass Yield (FPY)",
            "personaIds": [
                "mps_scheduling_lead",
                "plant_oee_maintenance_mgr",
                "manufacturing_quality_eng",
                "bom_change_launch_lead"
            ],
            "agentIds": [
                "line_schedule_optimizer",
                "predictive_oee_sentinel",
                "inline_yield_guardian",
                "eco_cutover_orchestrator"
            ],
            "flow": "Physical Material Flow (Manufacturing Transformation ──▶)"
        },
        "inventory_warehouse": {
            "id": "inventory_warehouse",
            "vNum": "04",
            "scorBadge": "SCOR 04 · FULFILL",
            "name": "Fulfill (Inventory, MEIO & Warehousing)",
            "fullName": "Pillar 4: Fulfill — Multi-Echelon Inventory Optimization & 3D Warehousing (The Buffers & Custodians)",
            "tagline": "The Buffers & Custodians",
            "subtitle": "Multi-echelon safety stock, dynamic ATP, Golden-Zone slotting, inwarding QA & dock-yard operations",
            "color": "#00d2ff",
            "watermarkType": "conveyor_rack",
            "horizon": "Tactical Horizon (Weekly) to Real-Time Daily Execution",
            "coreQuestion": "Where should inventory be buffered across the multi-echelon network, how do we promise orders in <50ms, and how do we run dock-to-stock in <4 hours?",
            "systems": "SAP IBP MEIO · Blue Yonder WMS · Manhattan Active · Cloud Spanner · Google OR-Tools · BigQuery",
            "solverSummary": "Clark-Scarf Multi-Echelon Stochastic Safety Stock Solver + Sub-50ms Spanner Strict Quota ATP Engine + 3D Golden-Zone High-Bay AS/RS Slotting IP + Google Maps Fleet Engine Dock Door Demurrage Shield",
            "toilMetric": "Trapped capital in wrong nodes & 14-hour dock-to-stock delays",
            "toilBullets": [
                "Each warehouse node buffers inventory independently, causing severe bullwhip magnification and $85M+ in trapped working capital",
                "Order promising takes hours of batch ATP runs, causing overselling, emergency stockouts, and cancelled high-margin customer orders",
                "Manual 2D warehouse slotting forces pickers to walk 12+ miles/shift, while inbound trailers queue in yards causing massive demurrage"
            ],
            "impactMetric": "-24.8% Trapped Working Capital & <4h Dock-to-Stock",
            "impactBullets": [
                "Multi-Echelon Inventory Optimization (MEIO) mathematically places decoupling buffers at central plants, freeing 24.8% working capital",
                "Sub-50ms real-time ATP on Cloud Spanner commits inventory across DCs with strategic quota reservation for Tier-1 accounts",
                "Dynamic 3D Golden-Zone slotting cuts picker travel time by 32%, and automated dock yard geofencing eliminates trailer demurrage"
            ],
            "kpis": "Days Inventory Outstanding (DIO) | Order Promise Latency (ms) | Dock-to-Stock Time (hrs) | Warehouse Pick Rate (lines/hr)",
            "personaIds": [
                "meio_inventory_mgr",
                "atp_fulfillment_spec",
                "sc_finops_network_architect",
                "warehouse_slotting_lead",
                "dock_yard_supervisor"
            ],
            "agentIds": [
                "meio_safety_stock_agent",
                "atp_order_promising_agent",
                "network_twin_architect",
                "warehouse_slotting_agent",
                "yard_dock_sequencer",
                "crossdock_transfer_orchestrator"
            ],
            "flow": "Physical Material Flow (Mother Warehouses & Cross-Dock Hubs ──▶)"
        },
        "logistics_fleet": {
            "id": "logistics_fleet",
            "vNum": "05",
            "scorBadge": "SCOR 05 · DELIVER",
            "name": "Deliver (Multi-Modal Logistics, Fleet & TM&D)",
            "fullName": "Pillar 5: Deliver — Multi-Modal Logistics, Fleet Management & Trade Distribution (The Movers & Distributors)",
            "tagline": "The Movers & Distributors",
            "subtitle": "Ocean AIS, air cargo ULD, rail sidings, 3D LIFO loading, FSO beat routes & retail planograms",
            "color": "#ff8c00",
            "watermarkType": "corridor_lifo",
            "horizon": "Real-Time Multi-Modal Daily Execution & Secondary Distribution",
            "coreQuestion": "How do we transport freight across Ocean, Air, Rail, and Road with maximum cube fill, zero demurrage, and execute secondary distribution to retail counters?",
            "systems": "Oracle OTM · Blue Yonder TMS · Google Maps Platform (Routes Preferred & Fleet Engine) · Spire Satellite AIS · FlightAware · DMS / SFA Mobile Handhelds",
            "solverSummary": "3D Bin-Packing LIFO Container/Trailer & Aircraft ULD Solver + Google Maps Routes Preferred CVRPTW Beat Engine + AIS/ADS-B Satellite Demurrage Sentinel + Multimodal Vision Planogram Auditor",
            "toilMetric": "22% multi-modal freight waste & field stockout pitches",
            "toilBullets": [
                "Siloed ocean container booking, panic air freight charters, slow rail handoffs, and sub-optimal 2D paper load sheets leak millions",
                "Field Sales Officers (FSOs) waste 30%+ of store visits booking orders for SKUs currently out of stock at distributors",
                "Unverified store photos allow retailer planogram violations and unearned trade payouts, while railway siding demurrage mounts"
            ],
            "impactMetric": "-22.4% Multi-Modal Cost & +18.4% Distributor Fill",
            "impactBullets": [
                "End-to-end multi-modal corridor orchestration from Factory Gate to Ocean Ships, Airplanes, Rail Rakes & Road Trucks with 3D LIFO packing",
                "Real-time reconciliation of FSO focus SKUs with live distributor stock prevents wasted visits and guarantees 100% fulfillable orders",
                "Gemini 3.8 Flash multimodal vision audits retail shelf photos for planogram compliance, automating verified trade scheme payouts"
            ],
            "kpis": "Freight Cost per Ton-Km (₹/PTPK) | Truck Cube Fill % | Railway Demurrage (₹) | Distributor Case Fill % | Planogram Compliance %",
            "personaIds": [
                "fleet_dispatch_mgr",
                "global_trade_port_mgr",
                "air_cargo_charter_lead",
                "intermodal_rail_linehaul_lead",
                "network_logistics_lead",
                "freight_claims_analyst",
                "tmd_merchandising_mgr",
                "area_sales_field_ops_lead",
                "distributor_claims_settlement_spec"
            ],
            "agentIds": [
                "fleetflow_dispatch",
                "port_drayage_orchestrator",
                "air_cargo_uld_optimizer",
                "intermodal_rail_linehaul_agent",
                "multimodal_mode_shift_agent",
                "load_consolidation_agent",
                "freight_control_tower",
                "field_beat_distributor_sync_agent",
                "planogram_merchandising_vision_auditor",
                "trade_scheme_claims_reconciler"
            ],
            "flow": "Physical Material Flow (Multi-Modal Arteries & Secondary Distribution ──▶)"
        },
        "circular_enable": {
            "id": "circular_enable",
            "vNum": "06",
            "scorBadge": "SCOR 06 · RETURN & ENABLE",
            "name": "Return & Enable (Customer OTIF, Circular RMA & ESG)",
            "fullName": "Pillar 6: Return & Enable — Customer OTIF Defense, Circular RMA & Scope-3 ESG (The Guardians)",
            "tagline": "The Guardians",
            "subtitle": "Retail OTIF chargeback defense, circular RMA backhaul, Scope-3 ESG & macro resilience",
            "color": "#ec4899",
            "watermarkType": "circular_loop",
            "horizon": "Continuous Strategic & Operational Horizon",
            "coreQuestion": "How do we recover value from damaged/expired returns, defend against retailer chargebacks, and govern Scope-3 carbon & supply risks?",
            "systems": "SAP Claims & Returns · Retail OTIF Portals · Loop RMA · Google Earth Engine · ISO-14083 Carbon Engine · BigQuery Omni",
            "solverSummary": "Retail OTIF Deduction Dispute Classifier + Gemini 3.8 Flash Edge RMA Grading + Google Maps Fleet Backhaul CVRPTW + ISO-14083 GEE Carbon Ledger",
            "toilMetric": "3.5% revenue lost to OTIF fines & unrecovered returns",
            "toilBullets": [
                "Retailer On-Time In-Full (OTIF) penalty deductions and shortage chargebacks are absorbed without automated dispute evidence",
                "Customer returns ship via costly third-party LTL to central depots while outbound fleet trucks return backhaul empty",
                "Shipment-level Scope-3 carbon accounting (CBAM/EUDR) and enterprise supply chain risk assessments rely on static annual guesswork"
            ],
            "impactMetric": "-78% OTIF Fines & +31% Return Margin Recovery",
            "impactBullets": [
                "Predicts retailer OTIF breaches 72 hours early to reallocate stock and auto-generates contract-backed dispute dossiers with digital PODs",
                "Multimodal edge RMA grading and Google Maps fleet backhaul insertion recover Grade-A stock locally, boosting margin by 31%",
                "Automated ISO-14083 compliant shipment-level Scope-3 carbon ledger provides verified audit trails for global regulatory reporting"
            ],
            "kpis": "OTIF Fine Deduction ($) | Return Processing Cycle (days) | Scope-3 Carbon Intensity (gCO2e/t-km) | Net Return Recovery %",
            "personaIds": [
                "otif_customer_service_lead",
                "reverse_logistics_mgr",
                "sc_sustainability_esg_lead"
            ],
            "agentIds": [
                "reverse_rma_optimizer",
                "otif_penalty_shield",
                "carbon_scope3_ledger"
            ],
            "flow": "End-to-End Enterprise Synchronized Flow & Circular Loop (◀──▶)"
        }
    }
    cat["departments"] = departments

    # 3. Update persona deptIds
    persona_dept_map = {
        "demand_planning_dir": "demand_sop",
        "sop_ibp_lead": "demand_sop",
        "promo_launch_planner": "demand_sop",
        "cpfr_channel_mgr": "demand_sop",
        "category_sourcing_mgr": "sourcing_procurement",
        "supplier_risk_lead": "sourcing_procurement",
        "tariff_compliance_spec": "sourcing_procurement",
        "supplier_quality_lead": "sourcing_procurement",
        "mps_scheduling_lead": "manufacturing_prod",
        "plant_oee_maintenance_mgr": "manufacturing_prod",
        "manufacturing_quality_eng": "manufacturing_prod",
        "bom_change_launch_lead": "manufacturing_prod",
        "meio_inventory_mgr": "inventory_warehouse",
        "atp_fulfillment_spec": "inventory_warehouse",
        "sc_finops_network_architect": "inventory_warehouse",
        "warehouse_slotting_lead": "inventory_warehouse",
        "dock_yard_supervisor": "inventory_warehouse",
        "fleet_dispatch_mgr": "logistics_fleet",
        "global_trade_port_mgr": "logistics_fleet",
        "air_cargo_charter_lead": "logistics_fleet",
        "intermodal_rail_linehaul_lead": "logistics_fleet",
        "network_logistics_lead": "logistics_fleet",
        "freight_claims_analyst": "logistics_fleet",
        "tmd_merchandising_mgr": "logistics_fleet",
        "area_sales_field_ops_lead": "logistics_fleet",
        "distributor_claims_settlement_spec": "logistics_fleet",
        "otif_customer_service_lead": "circular_enable",
        "reverse_logistics_mgr": "circular_enable",
        "sc_sustainability_esg_lead": "circular_enable"
    }

    for pid, p in cat["personas"].items():
        if pid in persona_dept_map:
            p["deptId"] = persona_dept_map[pid]

    # 4. Update agent deptIds
    agent_dept_map = {
        "csco_control_tower_copilot": "universal_csco",
        "disruption_war_room_orchestrator": "universal_csco",
        "master_data_leadtime_steward": "universal_csco",
        "working_capital_cash_bridge": "universal_csco",
        "demand_sensing_agent": "demand_sop",
        "sop_scenario_weaver": "demand_sop",
        "promo_lift_simulator": "demand_sop",
        "cpfr_sync_agent": "demand_sop",
        "rfq_should_cost_agent": "sourcing_procurement",
        "tier_n_risk_sentinel": "sourcing_procurement",
        "tariff_esg_agent": "sourcing_procurement",
        "supplier_quality_sentinel": "sourcing_procurement",
        "line_schedule_optimizer": "manufacturing_prod",
        "predictive_oee_sentinel": "manufacturing_prod",
        "inline_yield_guardian": "manufacturing_prod",
        "eco_cutover_orchestrator": "manufacturing_prod",
        "meio_safety_stock_agent": "inventory_warehouse",
        "atp_order_promising_agent": "inventory_warehouse",
        "network_twin_architect": "inventory_warehouse",
        "warehouse_slotting_agent": "inventory_warehouse",
        "yard_dock_sequencer": "inventory_warehouse",
        "crossdock_transfer_orchestrator": "inventory_warehouse",
        "fleetflow_dispatch": "logistics_fleet",
        "load_consolidation_agent": "logistics_fleet",
        "freight_control_tower": "logistics_fleet",
        "port_drayage_orchestrator": "logistics_fleet",
        "air_cargo_uld_optimizer": "logistics_fleet",
        "intermodal_rail_linehaul_agent": "logistics_fleet",
        "multimodal_mode_shift_agent": "logistics_fleet",
        "field_beat_distributor_sync_agent": "logistics_fleet",
        "planogram_merchandising_vision_auditor": "logistics_fleet",
        "trade_scheme_claims_reconciler": "logistics_fleet",
        "reverse_rma_optimizer": "circular_enable",
        "otif_penalty_shield": "circular_enable",
        "carbon_scope3_ledger": "circular_enable"
    }

    for aid, a in cat["agents"].items():
        if aid in agent_dept_map:
            a["deptId"] = agent_dept_map[aid]

    # 5. Update periodicGroups
    cat["periodicGroups"] = [
        {
            "id": "universal_csco",
            "code": "GROUP 0 · CORE",
            "title": "Universal CSCO Core (4)",
            "color": "#38bdf8",
            "glow": "rgba(56,189,248,0.35)"
        },
        {
            "id": "demand_sop",
            "code": "GROUP I · PLAN",
            "title": "01 · Plan: Demand & S&OP (4)",
            "color": "#10b981",
            "glow": "rgba(16,185,129,0.35)"
        },
        {
            "id": "sourcing_procurement",
            "code": "GROUP II · SOURCE",
            "title": "02 · Source: Procurement (4)",
            "color": "#a142f4",
            "glow": "rgba(161,66,244,0.35)"
        },
        {
            "id": "manufacturing_prod",
            "code": "GROUP III · MAKE",
            "title": "03 · Make: Manufacturing (4)",
            "color": "#3b82f6",
            "glow": "rgba(59,130,246,0.35)"
        },
        {
            "id": "inventory_warehouse",
            "code": "GROUP IV · FULFILL",
            "title": "04 · Fulfill: 3D WMS & MEIO (6)",
            "color": "#00d2ff",
            "glow": "rgba(0,210,255,0.35)"
        },
        {
            "id": "logistics_fleet",
            "code": "GROUP V · DELIVER",
            "title": "05 · Deliver: Ship/Air/Rail/Road/TM&D (10)",
            "color": "#ff8c00",
            "glow": "rgba(255,140,0,0.35)"
        },
        {
            "id": "circular_enable",
            "code": "GROUP VI · RETURN & ENABLE",
            "title": "06 · Return & Enable: OTIF & ESG (3)",
            "color": "#ec4899",
            "glow": "rgba(236,72,153,0.35)"
        }
    ]

    # 6. Update periodicAgentMeta
    for aid, meta in cat.get("periodicAgentMeta", {}).items():
        if aid in agent_dept_map:
            meta["group"] = agent_dept_map[aid]

    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(cat, f, indent=2, ensure_ascii=False)
    print(f"Successfully updated {CATALOG_PATH}.")


def consolidate_periodic_table():
    print(f"Loading {PERIODIC_PATH}...")
    with open(PERIODIC_PATH, "r", encoding="utf-8") as f:
        pt = json.load(f)

    pt["groups"] = [
        {
            "id": "universal_csco",
            "code": "GROUP 0 · CORE",
            "title": "Universal CSCO Core (4)",
            "color": "#38bdf8",
            "glow": "rgba(56,189,248,0.35)"
        },
        {
            "id": "demand_sop",
            "code": "GROUP I · PLAN",
            "title": "01 · Plan: Demand & S&OP (4)",
            "color": "#10b981",
            "glow": "rgba(16,185,129,0.35)"
        },
        {
            "id": "sourcing_procurement",
            "code": "GROUP II · SOURCE",
            "title": "02 · Source: Procurement (4)",
            "color": "#a142f4",
            "glow": "rgba(161,66,244,0.35)"
        },
        {
            "id": "manufacturing_prod",
            "code": "GROUP III · MAKE",
            "title": "03 · Make: Manufacturing (4)",
            "color": "#3b82f6",
            "glow": "rgba(59,130,246,0.35)"
        },
        {
            "id": "inventory_warehouse",
            "code": "GROUP IV · FULFILL",
            "title": "04 · Fulfill: 3D WMS & MEIO (6)",
            "color": "#00d2ff",
            "glow": "rgba(0,210,255,0.35)"
        },
        {
            "id": "logistics_fleet",
            "code": "GROUP V · DELIVER",
            "title": "05 · Deliver: Ship/Air/Rail/Road/TM&D (10)",
            "color": "#ff8c00",
            "glow": "rgba(255,140,0,0.35)"
        },
        {
            "id": "circular_enable",
            "code": "GROUP VI · RETURN & ENABLE",
            "title": "06 · Return & Enable: OTIF & ESG (3)",
            "color": "#ec4899",
            "glow": "rgba(236,72,153,0.35)"
        }
    ]

    agent_group_map = {
        "csco_control_tower_copilot": "universal_csco",
        "disruption_war_room_orchestrator": "universal_csco",
        "master_data_leadtime_steward": "universal_csco",
        "working_capital_cash_bridge": "universal_csco",
        "demand_sensing_agent": "demand_sop",
        "sop_scenario_weaver": "demand_sop",
        "promo_lift_simulator": "demand_sop",
        "cpfr_sync_agent": "demand_sop",
        "rfq_should_cost_agent": "sourcing_procurement",
        "tier_n_risk_sentinel": "sourcing_procurement",
        "tariff_esg_agent": "sourcing_procurement",
        "supplier_quality_sentinel": "sourcing_procurement",
        "line_schedule_optimizer": "manufacturing_prod",
        "predictive_oee_sentinel": "manufacturing_prod",
        "inline_yield_guardian": "manufacturing_prod",
        "eco_cutover_orchestrator": "manufacturing_prod",
        "meio_safety_stock_agent": "inventory_warehouse",
        "atp_order_promising_agent": "inventory_warehouse",
        "network_twin_architect": "inventory_warehouse",
        "warehouse_slotting_agent": "inventory_warehouse",
        "yard_dock_sequencer": "inventory_warehouse",
        "crossdock_transfer_orchestrator": "inventory_warehouse",
        "fleetflow_dispatch": "logistics_fleet",
        "load_consolidation_agent": "logistics_fleet",
        "freight_control_tower": "logistics_fleet",
        "port_drayage_orchestrator": "logistics_fleet",
        "air_cargo_uld_optimizer": "logistics_fleet",
        "intermodal_rail_linehaul_agent": "logistics_fleet",
        "multimodal_mode_shift_agent": "logistics_fleet",
        "field_beat_distributor_sync_agent": "logistics_fleet",
        "planogram_merchandising_vision_auditor": "logistics_fleet",
        "trade_scheme_claims_reconciler": "logistics_fleet",
        "reverse_rma_optimizer": "circular_enable",
        "otif_penalty_shield": "circular_enable",
        "carbon_scope3_ledger": "circular_enable"
    }

    for el in pt.get("elements", []):
        aid = el.get("agentId")
        if aid in agent_group_map:
            el["group"] = agent_group_map[aid]

    with open(PERIODIC_PATH, "w", encoding="utf-8") as f:
        json.dump(pt, f, indent=2, ensure_ascii=False)
    print(f"Successfully updated {PERIODIC_PATH}.")

if __name__ == "__main__":
    consolidate_catalog()
    consolidate_periodic_table()
    print("Done!")

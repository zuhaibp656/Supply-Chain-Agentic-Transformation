#!/usr/bin/env python3
"""
Applies the 7-Page Value Stream Presentation PDF Taxonomy across the entire
Supply Chain Agentic Transformation portal:
  - 6 Core Operating Pillars (01 through 06)
  - 20 Sub-Pillars (Lifecycle Spine Columns)
  - 60 AI Agents (3 per Sub-Pillar) with exact PDF names, 1-sentence descriptions,
    and quantified outcome badges
  - 60 Human Personas (1-to-1 mapped to the 60 AI Agents) with clean Daily Journeys
  - 4 End-to-End 6-Stage Value Chains (F2F, O2D, S2P, P2R) aligned to the PDF
  - Lifecycle Spine UI Drawer on #pageHome modeled directly on Slides 2-7 of the PDF
"""

import copy
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT, "index.html")
PERIODIC_HTML_PATH = os.path.join(ROOT, "periodic_table.html")
MINDMAP_HTML_PATH = os.path.join(ROOT, "mind_map.html")
CATALOG_JSON_PATH = os.path.join(ROOT, "data", "supply_chain_catalog.json")
PERIODIC_JSON_PATH = os.path.join(ROOT, "data", "periodic_table_elements.json")


# =============================================================================
# 1. COMPLETE 7-PAGE PDF TAXONOMY: 6 PILLARS, 20 SUB-PILLARS, 60 AGENTS/PERSONAS
# =============================================================================
PDF_PILLARS = [
    {
        "id": "demand_sop",
        "vNum": "01",
        "scorBadge": "01 · PLANNING & STRATEGY",
        "shortTab": "01 · Planning & Strategy",
        "name": "Planning & Strategy",
        "slideTitle": "Supply Chain Planning & Strategy",
        "fullName": "Pillar 01: Supply Chain Planning & Strategy",
        "spineTitle": "CORE PLANNING LIFECYCLE",
        "tagline": "Core Planning Lifecycle",
        "subtitle": "Demand signals and strategic S&OP alignment.",
        "slideSubtitle": "Agentic AI Value Stream: Autonomous sensing, promotional optimization, and executive consensus.",
        "color": "#2563eb",
        "watermarkType": "demand_wave",
        "horizon": "Tactical & Strategic Horizon (Weekly – 24 Months)",
        "coreQuestion": "How do we sense market shifts early, optimize trade spend, reconcile plant bottlenecks in S&OP, and rationalize SKU portfolios?",
        "systems": "SAP IBP · Blue Yonder Demand · Anaplan · Vertex AI TimesFM · BigQuery · AlloyDB",
        "solverSummary": "Vertex AI TimesFM Foundation Model + BigQuery ML Elasticity Solver + OR-Tools S&OP Consensus MILP + Gemini 3.1 Pro Executive Synthesis",
        "toilMetric": "Weeks of siloed forecast overrides & trade spend leakage",
        "impactMetric": "7–14d Earlier Demand Sensing & Rapid S&OP Consensus",
        "kpis": "Forecast Accuracy (WAPE) | Trade Promo ROI | S&OP Consensus Cycle | Portfolio Net Margin",
        "flow": "Demand Forecasting ──▶ Trade Promotion ──▶ S&OP / IBP ──▶ Portfolio & SKU",
        "vcId": "f2f",
        "vcLabel": "Open Forecast-to-Fulfill (F2F) Process →",
        "subPillars": [
            {
                "id": "demand_forecasting",
                "name": "Demand Forecasting",
                "color": "#2563eb",
                "icon": "📡",
                "items": [
                    {
                        "agentId": "demand_sensing_agent",
                        "seedAgentId": "demand_sensing_agent",
                        "agentName": "Demand Sensing Agent",
                        "sym": "Ds",
                        "code": "101",
                        "personaId": "demand_planner_forecaster",
                        "legacyPersonaId": "demand_planning_dir",
                        "personaName": "Demand Planner / Forecaster",
                        "personaIcon": "📈",
                        "desc": "Synthesizes POS velocity, weather anomalies, and macro trends.",
                        "outcome": "Detects demand shifts 7–14 days earlier",
                        "buildTier": "Hybrid",
                        "cadType": "demand_wave",
                    },
                    {
                        "agentId": "cpfr_sync_agent",
                        "seedAgentId": "cpfr_sync_agent",
                        "agentName": "Forecast Reconciliation",
                        "sym": "Fr",
                        "code": "102",
                        "personaId": "commercial_planning_lead",
                        "legacyPersonaId": "cpfr_channel_mgr",
                        "personaName": "Commercial Planning Lead",
                        "personaIcon": "🤝",
                        "desc": "Identifies unmodeled drivers across eCommerce and retail channels.",
                        "outcome": "Replaces black-box variance models",
                        "buildTier": "Low-Code",
                        "cadType": "demand_wave",
                    },
                    {
                        "agentId": "npi_demand_profiler",
                        "seedAgentId": "demand_sensing_agent",
                        "agentName": "NPI Demand Profiler",
                        "sym": "Np",
                        "code": "103",
                        "personaId": "brand_innovation_mgr",
                        "legacyPersonaId": None,
                        "personaName": "Brand & Innovation Manager",
                        "personaIcon": "🚀",
                        "desc": "Matches launch packaging and attributes to historical lookalikes.",
                        "outcome": "Cuts 90-day launch forecast errors",
                        "buildTier": "Hybrid",
                        "cadType": "demand_wave",
                    },
                ],
            },
            {
                "id": "trade_promotion",
                "name": "Trade Promotion",
                "color": "#ea580c",
                "icon": "🏷️",
                "items": [
                    {
                        "agentId": "promo_lift_simulator",
                        "seedAgentId": "promo_lift_simulator",
                        "agentName": "Promo ROI Simulator",
                        "sym": "Pr",
                        "code": "104",
                        "personaId": "trade_marketing_manager",
                        "legacyPersonaId": "promo_launch_planner",
                        "personaName": "Trade Marketing Manager",
                        "personaIcon": "🎯",
                        "desc": "Simulates price elasticity, shelf lift, and incremental spend return.",
                        "outcome": "Prevents break-even trade leakage",
                        "buildTier": "Hybrid",
                        "cadType": "demand_wave",
                    },
                    {
                        "agentId": "field_beat_distributor_sync_agent",
                        "seedAgentId": "field_beat_distributor_sync_agent",
                        "agentName": "JBP Negotiation Agent",
                        "sym": "Jb",
                        "code": "105",
                        "personaId": "key_account_manager",
                        "legacyPersonaId": "area_sales_field_ops_lead",
                        "personaName": "Key Account Manager (KAM)",
                        "personaIcon": "💼",
                        "desc": "Creates customized sell-in story decks and joint promotional calendars.",
                        "outcome": "Aligns buyer margins and volume goals",
                        "buildTier": "Low-Code",
                        "cadType": "demand_wave",
                    },
                    {
                        "agentId": "trade_scheme_claims_reconciler",
                        "seedAgentId": "trade_scheme_claims_reconciler",
                        "agentName": "Deduction Audit Agent",
                        "sym": "Da",
                        "code": "106",
                        "personaId": "revenue_trade_finance_lead",
                        "legacyPersonaId": "distributor_claims_settlement_spec",
                        "personaName": "Revenue / Trade Finance Lead",
                        "personaIcon": "🧾",
                        "desc": "Audits scanned proof-of-performance circulars and invoices via OCR.",
                        "outcome": "Resolves claim disputes in hours",
                        "buildTier": "Low-Code",
                        "cadType": "demand_wave",
                    },
                ],
            },
            {
                "id": "sop_ibp",
                "name": "S&OP / IBP",
                "color": "#4f46e5",
                "icon": "⚖️",
                "items": [
                    {
                        "agentId": "sop_scenario_weaver",
                        "seedAgentId": "sop_scenario_weaver",
                        "agentName": "Consensus & Gap Agent",
                        "sym": "Cg",
                        "code": "107",
                        "personaId": "sop_supply_planning_dir",
                        "legacyPersonaId": "sop_ibp_lead",
                        "personaName": "S&OP / Supply Planning Dir.",
                        "personaIcon": "🧭",
                        "desc": "Reconciles unconstrained demand with factory plant bottleneck limits.",
                        "outcome": "Highlights margin-dilutive imbalances",
                        "buildTier": "High-Code",
                        "cadType": "control_tower_twin",
                    },
                    {
                        "agentId": "disruption_war_room_orchestrator",
                        "seedAgentId": "disruption_war_room_orchestrator",
                        "agentName": "Digital War-Room Agent",
                        "sym": "Wr",
                        "code": "108",
                        "personaId": "supply_chain_vp_coo",
                        "legacyPersonaId": None,
                        "personaName": "Supply Chain VP / COO",
                        "personaIcon": "🛡️",
                        "desc": "Evaluates co-packer shifts and allocation trade-offs during supply outages.",
                        "outcome": "Rapid OTIF impact scenario brief",
                        "buildTier": "Hybrid",
                        "cadType": "control_tower_twin",
                    },
                    {
                        "agentId": "csco_control_tower_copilot",
                        "seedAgentId": "csco_control_tower_copilot",
                        "agentName": "Executive Copilot",
                        "sym": "Ec",
                        "code": "109",
                        "personaId": "ibp_lead_chief_planning_off",
                        "legacyPersonaId": None,
                        "personaName": "IBP Lead / Chief Planning Off.",
                        "personaIcon": "🏛️",
                        "desc": "Generates pre-read decks and tracks sign-offs across cross-functional leads.",
                        "outcome": "Reduces deck preparation by days",
                        "buildTier": "Low-Code",
                        "cadType": "control_tower_twin",
                    },
                ],
            },
            {
                "id": "portfolio_sku",
                "name": "Portfolio & SKU",
                "color": "#059669",
                "icon": "🧩",
                "items": [
                    {
                        "agentId": "working_capital_cash_bridge",
                        "seedAgentId": "working_capital_cash_bridge",
                        "agentName": "SKU Pruning Agent",
                        "sym": "Sp",
                        "code": "110",
                        "personaId": "category_manager_portfolio",
                        "legacyPersonaId": None,
                        "personaName": "Category Manager",
                        "personaIcon": "✂️",
                        "desc": "Scores velocity, plant changeover cost, and shelf revenue yield.",
                        "outcome": "Unlocks tail working capital",
                        "buildTier": "Low-Code",
                        "cadType": "demand_wave",
                    },
                    {
                        "agentId": "eco_cutover_orchestrator",
                        "seedAgentId": "eco_cutover_orchestrator",
                        "agentName": "PIPO Run-Out Agent",
                        "sym": "Pi",
                        "code": "111",
                        "personaId": "lifecycle_materials_mgr",
                        "legacyPersonaId": "bom_change_launch_lead",
                        "personaName": "Lifecycle / Materials Mgr",
                        "personaIcon": "🔄",
                        "desc": "Orchestrates transition buffers to sync packaging and formulation cuts.",
                        "outcome": "Eliminates stranded write-offs",
                        "buildTier": "High-Code",
                        "cadType": "plant_oee",
                    },
                    {
                        "agentId": "network_twin_architect",
                        "seedAgentId": "network_twin_architect",
                        "agentName": "Cost-to-Serve Diagnostic",
                        "sym": "Cs",
                        "code": "112",
                        "personaId": "commercial_finance_director",
                        "legacyPersonaId": "sc_finops_network_architect",
                        "personaName": "Commercial Finance Director",
                        "personaIcon": "💹",
                        "desc": "Calculates net-net margin across Club, Grocery, and eCommerce packs.",
                        "outcome": "Re-engineers MOQ and pack rules",
                        "buildTier": "High-Code",
                        "cadType": "control_tower_twin",
                    },
                ],
            },
        ],
    },
    {
        "id": "sourcing_procurement",
        "vNum": "02",
        "scorBadge": "02 · SOURCING & PROCUREMENT",
        "shortTab": "02 · Sourcing & Procurement",
        "name": "Sourcing & Procurement",
        "slideTitle": "Strategic Procurement",
        "fullName": "Pillar 02: Strategic Sourcing & Procurement",
        "spineTitle": "PROCUREMENT LIFECYCLE SPINE",
        "tagline": "Procurement Lifecycle Spine",
        "subtitle": "Tier vendor networks and EDI order routing.",
        "slideSubtitle": "Agentic AI Value Stream: Multi-tier risk sensing, dynamic should-costing, and autonomous PO execution.",
        "color": "#7c3aed",
        "watermarkType": "supplier_graph",
        "horizon": "Strategic & Operational Horizon",
        "coreQuestion": "How do we sense multi-tier vendor disruptions weeks ahead, negotiate with clean-sheet should-cost models, and automate PO & 3-way match execution?",
        "systems": "SAP Ariba · Coupa · Cloud Spanner Graph · AlloyDB + pgvector · CBOT / Platts · EDI 855/856",
        "solverSummary": "Cloud Spanner Multi-Tier Graph Sentinel + Parametric Clean-Sheet Should-Cost Engine + Gemini Document AI 3-Way Match Reconciler",
        "toilMetric": "Manual vendor onboarding, blind RFP pricing & PO delay chasing",
        "impactMetric": "2–3 Wk Early Risk Warning & ~70% Auto-Resolved PO Delays",
        "kpis": "Supplier OTIF % | Purchase Price Variance (PPV) | Onboarding Cycle (<48h) | Rebate Leakage Recovery",
        "flow": "Supplier Network ──▶ Material & Packaging ──▶ Contract & PO Mgmt",
        "vcId": "s2p",
        "vcLabel": "Open Source-to-Pay (S2P) Process →",
        "subPillars": [
            {
                "id": "supplier_network",
                "name": "Supplier Network",
                "color": "#0d9488",
                "icon": "🕸️",
                "items": [
                    {
                        "agentId": "tier_n_risk_sentinel",
                        "seedAgentId": "tier_n_risk_sentinel",
                        "agentName": "Disruption Sensing Agent",
                        "sym": "Sn",
                        "code": "201",
                        "personaId": "procurement_dir_risk_mgr",
                        "legacyPersonaId": "supplier_risk_lead",
                        "personaName": "Procurement Dir. / Risk Mgr",
                        "personaIcon": "🌐",
                        "desc": "Monitors multi-tier supply feeds, port delays, and vendor financials.",
                        "outcome": "2–3 week advance disruption warning",
                        "buildTier": "Hybrid",
                        "cadType": "supplier_graph",
                    },
                    {
                        "agentId": "supplier_quality_sentinel",
                        "seedAgentId": "supplier_quality_sentinel",
                        "agentName": "Onboarding & Qual. Agent",
                        "sym": "Oq",
                        "code": "202",
                        "personaId": "procurement_operations_lead",
                        "legacyPersonaId": "supplier_quality_lead",
                        "personaName": "Procurement Operations Lead",
                        "personaIcon": "📋",
                        "desc": "Parses BRC/ISO audits, food-safety filings, and tax registrations.",
                        "outcome": "Cuts onboarding from weeks to <48h",
                        "buildTier": "Low-Code",
                        "cadType": "supplier_graph",
                    },
                    {
                        "agentId": "carbon_scope3_ledger",
                        "seedAgentId": "carbon_scope3_ledger",
                        "agentName": "ESG & Scope 3 Auditor",
                        "sym": "Es",
                        "code": "203",
                        "personaId": "chief_sustainability_officer",
                        "legacyPersonaId": "sc_sustainability_esg_lead",
                        "personaName": "Chief Sustainability Officer",
                        "personaIcon": "🌿",
                        "desc": "Standardizes chain-of-custody certificates (RSPO/FSC) and packaging LCAs.",
                        "outcome": "Automates Scope 3 disclosure audits",
                        "buildTier": "Low-Code",
                        "cadType": "circular_loop",
                    },
                ],
            },
            {
                "id": "material_packaging",
                "name": "Material & Packaging",
                "color": "#d97706",
                "icon": "📦",
                "items": [
                    {
                        "agentId": "commodity_index_advisor",
                        "seedAgentId": "rfq_should_cost_agent",
                        "agentName": "Commodity Index Advisor",
                        "sym": "Ci",
                        "code": "204",
                        "personaId": "category_sourcing_mgr_direct",
                        "legacyPersonaId": "category_sourcing_mgr",
                        "personaName": "Category Sourcing Mgr (Direct)",
                        "personaIcon": "📊",
                        "desc": "Correlates CBOT/Platts feedstocks with depletion to advise hedging.",
                        "outcome": "Optimizes forward-contract windows",
                        "buildTier": "Hybrid",
                        "cadType": "supplier_graph",
                    },
                    {
                        "agentId": "rfq_should_cost_agent",
                        "seedAgentId": "rfq_should_cost_agent",
                        "agentName": "Dynamic Should-Cost Agent",
                        "sym": "Sc",
                        "code": "205",
                        "personaId": "strategic_sourcing_lead",
                        "legacyPersonaId": None,
                        "personaName": "Strategic Sourcing Lead",
                        "personaIcon": "🧮",
                        "desc": "Deconstructs packaging specs (resin weight, corrugate, conversion energy).",
                        "outcome": "Fact-based margin leverage in RFPs",
                        "buildTier": "High-Code",
                        "cadType": "supplier_graph",
                    },
                    {
                        "agentId": "sustainable_packaging_agent",
                        "seedAgentId": "carbon_scope3_ledger",
                        "agentName": "Sustainable Packaging Agent",
                        "sym": "Pk",
                        "code": "206",
                        "personaId": "packaging_rd_engineer",
                        "legacyPersonaId": None,
                        "personaName": "Packaging R&D Engineer",
                        "personaIcon": "🧪",
                        "desc": "Evaluates PCR resins and barrier materials against line runnability & taxes.",
                        "outcome": "Mitigates EPR and landfill taxation",
                        "buildTier": "Hybrid",
                        "cadType": "circular_loop",
                    },
                ],
            },
            {
                "id": "contract_po_mgmt",
                "name": "Contract & PO Mgmt",
                "color": "#4f46e5",
                "icon": "📜",
                "items": [
                    {
                        "agentId": "tariff_esg_agent",
                        "seedAgentId": "tariff_esg_agent",
                        "agentName": "Contract Leakage Agent",
                        "sym": "Cl",
                        "code": "207",
                        "personaId": "commercial_sourcing_legal",
                        "legacyPersonaId": "tariff_compliance_spec",
                        "personaName": "Commercial Sourcing / Legal",
                        "personaIcon": "⚖️",
                        "desc": "Reconciles live spend against negotiated rebate tiers and volume discount scales.",
                        "outcome": "Recovers missed rebates & surcharges",
                        "buildTier": "Low-Code",
                        "cadType": "supplier_graph",
                    },
                    {
                        "agentId": "master_data_leadtime_steward",
                        "seedAgentId": "master_data_leadtime_steward",
                        "agentName": "PO Expediting Agent",
                        "sym": "Pe",
                        "code": "208",
                        "personaId": "buyer_procurement_coord",
                        "legacyPersonaId": None,
                        "personaName": "Buyer / Procurement Coord.",
                        "personaIcon": "⚡",
                        "desc": "Monitors EDI 855/856 delay feeds and orchestrates supplier split-shipments.",
                        "outcome": "Resolves ~70% of standard PO delays",
                        "buildTier": "Low-Code",
                        "cadType": "supplier_graph",
                    },
                    {
                        "agentId": "three_way_match_dispute",
                        "seedAgentId": "tariff_esg_agent",
                        "agentName": "Three-Way Match Dispute",
                        "sym": "Tm",
                        "code": "209",
                        "personaId": "accounts_payable_lead",
                        "legacyPersonaId": None,
                        "personaName": "Accounts Payable Lead",
                        "personaIcon": "💳",
                        "desc": "Diagnoses price/quantity discrepancies across POs, GRNs, and carrier invoices.",
                        "outcome": "Prevents vendor holds & saves discounts",
                        "buildTier": "Low-Code",
                        "cadType": "supplier_graph",
                    },
                ],
            },
        ],
    },
    {
        "id": "manufacturing_prod",
        "vNum": "03",
        "scorBadge": "03 · MANUFACTURING & PRODUCTION",
        "shortTab": "03 · Manufacturing & Prod",
        "name": "Manufacturing & Production",
        "slideTitle": "Intelligent Shop Floor",
        "fullName": "Pillar 03: Intelligent Shop Floor — Manufacturing & Production",
        "spineTitle": "MANUFACTURING OPERATIONS LIFECYCLE",
        "tagline": "Manufacturing Operations Lifecycle",
        "subtitle": "Optimized runs and zero-defect QA protocols.",
        "slideSubtitle": "Agentic AI Value Stream: Autonomous scheduling, bottleneck diagnostics, and zero-defect QA.",
        "color": "#ea580c",
        "watermarkType": "plant_oee",
        "horizon": "Shift-Level Execution to Multi-Year CapEx Horizon",
        "coreQuestion": "How do we sequence runs to cut sanitation downtime, re-route WIP in under 3 minutes, balance co-packer margins, and release batches 60–80% faster?",
        "systems": "Siemens Opcenter · Rockwell FactoryTalk · SAP PP/QM · Google OR-Tools CP-SAT · Gemini Vision",
        "solverSummary": "OR-Tools CP-SAT Sequence & Washdown Minimizer + Real-Time WIP Disruption Re-Router + Gemini Multimodal Vision & Batch Record Auditor",
        "toilMetric": "Sanitation changeover losses, line halts & manual BPR review",
        "impactMetric": "-15–25% Sanitation Downtime & 60–80% Faster Batch Release",
        "kpis": "Plant OEE % | Sanitation Changeover Hrs | Batch Release Cycle | First-Pass Yield (FPY)",
        "flow": "Production Scheduling ──▶ Capacity Planning ──▶ Quality & Compliance",
        "vcId": "f2f",
        "vcLabel": "Open Forecast-to-Fulfill (F2F) Process →",
        "subPillars": [
            {
                "id": "production_scheduling",
                "name": "Production Scheduling",
                "color": "#ea580c",
                "icon": "🗓️",
                "items": [
                    {
                        "agentId": "finite_production_scheduler",
                        "seedAgentId": "line_schedule_optimizer",
                        "agentName": "Changeover Optimizer",
                        "sym": "Co",
                        "code": "301",
                        "personaId": "master_production_scheduler",
                        "legacyPersonaId": "mps_scheduling_lead",
                        "personaName": "Master Production Scheduler",
                        "personaIcon": "🗓️",
                        "desc": "Sequences allergen, kosher, and packaging runs to minimize washdowns.",
                        "outcome": "Cuts sanitation downtime by 15–25%",
                        "buildTier": "High-Code",
                        "cadType": "plant_oee",
                    },
                    {
                        "agentId": "line_schedule_optimizer",
                        "seedAgentId": "line_schedule_optimizer",
                        "agentName": "Disruption Re-sequencer",
                        "sym": "Dr",
                        "code": "302",
                        "personaId": "shop_floor_shift_lead",
                        "legacyPersonaId": None,
                        "personaName": "Shop Floor / Shift Lead",
                        "personaIcon": "⚙️",
                        "desc": "Detects machine halts and re-routes perishable WIP to alternate lines.",
                        "outcome": "Line reallocation in <3 minutes",
                        "buildTier": "High-Code",
                        "cadType": "plant_oee",
                    },
                    {
                        "agentId": "labor_line_balancing_agent",
                        "seedAgentId": "line_schedule_optimizer",
                        "agentName": "Labor & Line Balancing",
                        "sym": "Lb",
                        "code": "303",
                        "personaId": "plant_operations_manager",
                        "legacyPersonaId": None,
                        "personaName": "Plant Operations Manager",
                        "personaIcon": "👷",
                        "desc": "Maps shift skill certifications and fatigue constraints to line speeds.",
                        "outcome": "Prevents certified skill bottlenecks",
                        "buildTier": "High-Code",
                        "cadType": "plant_oee",
                    },
                ],
            },
            {
                "id": "capacity_planning",
                "name": "Capacity Planning",
                "color": "#2563eb",
                "icon": "🏭",
                "items": [
                    {
                        "agentId": "predictive_oee_sentinel",
                        "seedAgentId": "predictive_oee_sentinel",
                        "agentName": "Bottleneck Diagnostic",
                        "sym": "Bd",
                        "code": "304",
                        "personaId": "supply_chain_ops_director",
                        "legacyPersonaId": "plant_oee_maintenance_mgr",
                        "personaName": "Supply Chain Ops Director",
                        "personaIcon": "🔧",
                        "desc": "Assesses CIP utilities, boiler loads, and cold storage holding limits.",
                        "outcome": "Flags facility constraints 3–6 mos out",
                        "buildTier": "Hybrid",
                        "cadType": "plant_oee",
                    },
                    {
                        "agentId": "copacker_allocation_agent",
                        "seedAgentId": "sop_scenario_weaver",
                        "agentName": "Co-Packer Allocation",
                        "sym": "Cp",
                        "code": "305",
                        "personaId": "external_sourcing_cmo_lead",
                        "legacyPersonaId": None,
                        "personaName": "External Sourcing / CMO Lead",
                        "personaIcon": "🤝",
                        "desc": "Models internal conversion costs against co-packer tolling agreements.",
                        "outcome": "Optimizes net gross margin per case",
                        "buildTier": "High-Code",
                        "cadType": "plant_oee",
                    },
                    {
                        "agentId": "capex_simulator_agent",
                        "seedAgentId": "network_twin_architect",
                        "agentName": "CapEx Simulator",
                        "sym": "Cx",
                        "code": "306",
                        "personaId": "vp_manufacturing_engineering",
                        "legacyPersonaId": None,
                        "personaName": "VP Manufacturing Engineering",
                        "personaIcon": "🏗️",
                        "desc": "Simulates multi-year volume trends to test high-speed line expansions.",
                        "outcome": "Delivers defensible board CapEx ROI",
                        "buildTier": "High-Code",
                        "cadType": "plant_oee",
                    },
                ],
            },
            {
                "id": "quality_compliance",
                "name": "Quality & Compliance",
                "color": "#0d9488",
                "icon": "🔬",
                "items": [
                    {
                        "agentId": "inline_yield_guardian",
                        "seedAgentId": "inline_yield_guardian",
                        "agentName": "Visual Defect Triager",
                        "sym": "Vd",
                        "code": "307",
                        "personaId": "qa_manager_line_inspector",
                        "legacyPersonaId": "manufacturing_quality_eng",
                        "personaName": "QA Manager / Line Inspector",
                        "personaIcon": "📷",
                        "desc": "Inspects high-speed video frames for crimped seals, lot codes, and labels.",
                        "outcome": "Prevents full pallet scrap & holds",
                        "buildTier": "Hybrid",
                        "cadType": "plant_oee",
                    },
                    {
                        "agentId": "batch_record_auditor",
                        "seedAgentId": "inline_yield_guardian",
                        "agentName": "Batch Record Auditor",
                        "sym": "Br",
                        "code": "308",
                        "personaId": "regulatory_compliance_lead",
                        "legacyPersonaId": None,
                        "personaName": "Regulatory Compliance Lead",
                        "personaIcon": "📑",
                        "desc": "Parses BPR and COA documents to flag pasteurization & CCP deviations.",
                        "outcome": "60–80% faster batch release review",
                        "buildTier": "Low-Code",
                        "cadType": "plant_oee",
                    },
                    {
                        "agentId": "scrap_defect_root_cause_agent",
                        "seedAgentId": "inline_yield_guardian",
                        "agentName": "RCA & CAPA Copilot",
                        "sym": "Rc",
                        "code": "309",
                        "personaId": "continuous_improvement_lead",
                        "legacyPersonaId": None,
                        "personaName": "Continuous Improvement Lead",
                        "personaIcon": "🎯",
                        "desc": "Correlates consumer complaints with ingredient lots and machine telemetry.",
                        "outcome": "Speeds 5-Why investigation closures",
                        "buildTier": "Hybrid",
                        "cadType": "plant_oee",
                    },
                ],
            },
        ],
    },
    {
        "id": "inventory_warehouse",
        "vNum": "04",
        "scorBadge": "04 · INVENTORY & WAREHOUSING",
        "shortTab": "04 · Inventory & Warehousing",
        "name": "Inventory & Warehousing",
        "slideTitle": "Dynamic Fulfillment",
        "fullName": "Pillar 04: Dynamic Fulfillment — Inventory & Warehousing",
        "spineTitle": "INVENTORY & DC LIFECYCLE SPINE",
        "tagline": "Inventory & DC Lifecycle Spine",
        "subtitle": "Multi-node staging and enterprise visibility.",
        "slideSubtitle": "Agentic AI Value Stream: Multi-echelon positioning, automated DC execution, and omnichannel flow.",
        "color": "#0284c7",
        "watermarkType": "conveyor_rack",
        "horizon": "Weekly Multi-Echelon Positioning to Real-Time DC Floor Execution",
        "coreQuestion": "How do we cut working capital 10–18% across echelons, reduce DC picker transit time 15–30%, and eliminate phantom inventory & split shipments?",
        "systems": "SAP IBP MEIO · Manhattan Active WMS · Blue Yonder WMS · Cloud Spanner · Google OR-Tools",
        "solverSummary": "Stochastic Multi-Echelon Safety Stock Solver + Co-Pick Affinity 3D Slotting Optimizer + Sub-50ms Spanner SFS/BOPIS Order Sourcing Engine",
        "toilMetric": "Excess safety stock buffers, slow dock turnaround & phantom stock",
        "impactMetric": "-10–18% Working Capital & -15–30% Picker Transit Time",
        "kpis": "Days Inventory Outstanding (DIO) | Picker Transit Time | Dock-to-Stock Turnaround | SFS Split Rate",
        "flow": "Positioning & Optimization ──▶ Warehouse Operations ──▶ Omnichannel Visibility",
        "vcId": "p2r",
        "vcLabel": "Open Plan-to-Recovery (P2R) Process →",
        "subPillars": [
            {
                "id": "positioning_optimization",
                "name": "Positioning & Optimization",
                "color": "#0284c7",
                "icon": "🌐",
                "items": [
                    {
                        "agentId": "meio_safety_stock_agent",
                        "seedAgentId": "meio_safety_stock_agent",
                        "agentName": "Safety Stock Agent",
                        "sym": "Ss",
                        "code": "401",
                        "personaId": "inventory_optimization_lead",
                        "legacyPersonaId": "meio_inventory_mgr",
                        "personaName": "Inventory Optimization Lead",
                        "personaIcon": "📊",
                        "desc": "Recalibrates multi-echelon buffers using live lead-time and demand variance.",
                        "outcome": "Cuts working capital by 10–18%",
                        "buildTier": "High-Code",
                        "cadType": "conveyor_rack",
                    },
                    {
                        "agentId": "slob_disposition_agent",
                        "seedAgentId": "meio_safety_stock_agent",
                        "agentName": "SLOB Disposition Agent",
                        "sym": "Sl",
                        "code": "402",
                        "personaId": "inventory_controller_buyer",
                        "legacyPersonaId": None,
                        "personaName": "Inventory Controller / Buyer",
                        "personaIcon": "⏳",
                        "desc": "Analyzes shelf-life risk and triggers promotional bundles or liquidations.",
                        "outcome": "Prevents expired stock write-offs",
                        "buildTier": "Hybrid",
                        "cadType": "conveyor_rack",
                    },
                    {
                        "agentId": "crossdock_transfer_orchestrator",
                        "seedAgentId": "crossdock_transfer_orchestrator",
                        "agentName": "Inter-Facility Rebalancer",
                        "sym": "If",
                        "code": "403",
                        "personaId": "replenishment_planner",
                        "legacyPersonaId": None,
                        "personaName": "Replenishment Planner",
                        "personaIcon": "🔄",
                        "desc": "Generates automated inter-DC and store transfers to balance localized gluts.",
                        "outcome": "Eliminates regional out-of-stocks",
                        "buildTier": "High-Code",
                        "cadType": "conveyor_rack",
                    },
                ],
            },
            {
                "id": "warehouse_operations",
                "name": "Warehouse Operations",
                "color": "#d97706",
                "icon": "🏗️",
                "items": [
                    {
                        "agentId": "warehouse_slotting_agent",
                        "seedAgentId": "warehouse_slotting_agent",
                        "agentName": "Dynamic Slotting Agent",
                        "sym": "Ds",
                        "code": "404",
                        "personaId": "dc_operations_mgr",
                        "legacyPersonaId": "warehouse_slotting_lead",
                        "personaName": "DC Operations Mgr / IE Lead",
                        "personaIcon": "📦",
                        "desc": "Evaluates co-pick affinity matrices to recommend fast-pick zone re-slotting.",
                        "outcome": "Reduces picker transit time by 15–30%",
                        "buildTier": "High-Code",
                        "cadType": "conveyor_rack",
                    },
                    {
                        "agentId": "dock_to_stock_agent",
                        "seedAgentId": "yard_dock_sequencer",
                        "agentName": "Dock-to-Stock Agent",
                        "sym": "Dt",
                        "code": "405",
                        "personaId": "inbound_receiving_supervisor",
                        "legacyPersonaId": "dock_yard_supervisor",
                        "personaName": "Inbound Receiving Supervisor",
                        "personaIcon": "🚛",
                        "desc": "Parses scanned BOLs and pallet photos to reconcile open ASN variances.",
                        "outcome": "Dock turnaround in minutes vs. hours",
                        "buildTier": "Hybrid",
                        "cadType": "conveyor_rack",
                    },
                    {
                        "agentId": "wave_fulfillment_copilot",
                        "seedAgentId": "warehouse_slotting_agent",
                        "agentName": "Wave Fulfillment Copilot",
                        "sym": "Wf",
                        "code": "406",
                        "personaId": "dc_shift_floor_lead",
                        "legacyPersonaId": None,
                        "personaName": "DC Shift Floor Lead",
                        "personaIcon": "⚡",
                        "desc": "Balances picker lines dynamically to protect carrier pickup cutoff times.",
                        "outcome": "Prevents missed dispatch windows (OTIF)",
                        "buildTier": "High-Code",
                        "cadType": "conveyor_rack",
                    },
                ],
            },
            {
                "id": "omnichannel_visibility",
                "name": "Omnichannel Visibility",
                "color": "#4f46e5",
                "icon": "🏪",
                "items": [
                    {
                        "agentId": "planogram_merchandising_vision_auditor",
                        "seedAgentId": "planogram_merchandising_vision_auditor",
                        "agentName": "Phantom Inventory Sensor",
                        "sym": "Ph",
                        "code": "407",
                        "personaId": "store_operations_omni_lead",
                        "legacyPersonaId": "tmd_merchandising_mgr",
                        "personaName": "Store Operations / Omni Lead",
                        "personaIcon": "👁️",
                        "desc": "Identifies shrinkage anomalies when on-hand stock stops scanning at POS.",
                        "outcome": "Triggers targeted floor cycle counts",
                        "buildTier": "Hybrid",
                        "cadType": "conveyor_rack",
                    },
                    {
                        "agentId": "atp_order_promising_agent",
                        "seedAgentId": "atp_order_promising_agent",
                        "agentName": "SFS / BOPIS Sourcing",
                        "sym": "Sb",
                        "code": "408",
                        "personaId": "omnichannel_fulfillment_dir",
                        "legacyPersonaId": "atp_fulfillment_spec",
                        "personaName": "Omnichannel Fulfillment Dir.",
                        "personaIcon": "🛒",
                        "desc": "Selects lowest-cost fulfillment nodes based on store labor and parcel zones.",
                        "outcome": "Lowers parcel costs & split rates",
                        "buildTier": "Hybrid",
                        "cadType": "conveyor_rack",
                    },
                    {
                        "agentId": "returns_triage_agent",
                        "seedAgentId": "reverse_rma_optimizer",
                        "agentName": "Returns Triage Agent",
                        "sym": "Rt",
                        "code": "409",
                        "personaId": "reverse_logistics_lead_wh",
                        "legacyPersonaId": None,
                        "personaName": "Reverse Logistics Lead",
                        "personaIcon": "↩️",
                        "desc": "Evaluates item condition scans to triage restock, vendor return, or liquidation.",
                        "outcome": "Restocks sellable returns within 24h",
                        "buildTier": "Hybrid",
                        "cadType": "circular_loop",
                    },
                ],
            },
        ],
    },
    {
        "id": "logistics_fleet",
        "vNum": "05",
        "scorBadge": "05 · DISTRIBUTION & LOGISTICS",
        "shortTab": "05 · Distribution & Logistics",
        "name": "Distribution & Logistics",
        "slideTitle": "End-to-End Fulfillment",
        "fullName": "Pillar 05: End-to-End Fulfillment — Distribution & Logistics",
        "spineTitle": "LOGISTICS FULFILLMENT LIFECYCLE",
        "tagline": "Logistics Fulfillment Lifecycle",
        "subtitle": "Store replenishment and last-mile dispatch.",
        "slideSubtitle": "Agentic AI Value Stream: Freight consolidation, store-ready replenishment, and dynamic routing.",
        "color": "#059669",
        "watermarkType": "corridor_lifo",
        "horizon": "Real-Time Linehaul, Store Replenishment & Last-Mile Execution",
        "coreQuestion": "How do we consolidate LTLs into high-cube FTLs, build aisle-aligned store pallets, drop failed deliveries 30–45%, and audit freight bills automatically?",
        "systems": "Oracle OTM · Blue Yonder TMS · Google Maps Platform (Routes & Fleet Engine) · Reefer IoT · Carrier EDI 204/214/210",
        "solverSummary": "3D Cube & Axle-Weight Consolidation Solver + Planogram-Aligned Pallet Sequencer + Google Maps Dynamic Rerouter & Rate-Card Broker",
        "toilMetric": "Under-filled trailers, store backroom congestion & spot freight spikes",
        "impactMetric": "+12–18% Trailer Fill & -30–45% Failed Last-Mile Deliveries",
        "kpis": "Trailer Cube Fill % | Store Stocking Labor | On-Time Window Compliance (98%+) | Freight Bill Audit Savings",
        "flow": "First & Mid-Mile ──▶ Store Replenishment ──▶ Last-Mile Delivery ──▶ Route & Carrier",
        "vcId": "o2d",
        "vcLabel": "Open Order-to-Delivery (O2D) Process →",
        "subPillars": [
            {
                "id": "first_mid_mile",
                "name": "First & Mid-Mile",
                "color": "#2563eb",
                "icon": "🚛",
                "items": [
                    {
                        "agentId": "load_consolidation_agent",
                        "seedAgentId": "load_consolidation_agent",
                        "agentName": "Load Consolidation",
                        "sym": "Lc",
                        "code": "501",
                        "personaId": "transport_planner_inbound_mgr",
                        "legacyPersonaId": "network_logistics_lead",
                        "personaName": "Transport Planner / Inbound Mgr",
                        "personaIcon": "📐",
                        "desc": "Consolidates vendor LTLs into multi-stop FTL linehauls via cube & weight modeling.",
                        "outcome": "12–18% higher trailer fill rate",
                        "buildTier": "High-Code",
                        "cadType": "corridor_lifo",
                    },
                    {
                        "agentId": "yard_dock_sequencer",
                        "seedAgentId": "yard_dock_sequencer",
                        "agentName": "Yard Disruption Agent",
                        "sym": "Yd",
                        "code": "502",
                        "personaId": "yard_master_plant_logistics",
                        "legacyPersonaId": None,
                        "personaName": "Yard Master / Plant Logistics",
                        "personaIcon": "🚧",
                        "desc": "Parses GPS & gate feeds to flag delays and reassign dock staging doors dynamically.",
                        "outcome": "Eliminates demurrage & line starvation",
                        "buildTier": "Hybrid",
                        "cadType": "corridor_lifo",
                    },
                    {
                        "agentId": "cold_chain_auditor",
                        "seedAgentId": "freight_control_tower",
                        "agentName": "Cold-Chain Auditor",
                        "sym": "Cc",
                        "code": "503",
                        "personaId": "cold_chain_qa_logistics_dir",
                        "legacyPersonaId": None,
                        "personaName": "Cold Chain QA / Logistics Dir.",
                        "personaIcon": "❄️",
                        "desc": "Analyzes reefer IoT telemetry to flag thermal excursions and file carrier claims.",
                        "outcome": "Prevents perishable food spoilage",
                        "buildTier": "Hybrid",
                        "cadType": "corridor_lifo",
                    },
                ],
            },
            {
                "id": "store_replenishment",
                "name": "Store Replenishment",
                "color": "#d97706",
                "icon": "🏪",
                "items": [
                    {
                        "agentId": "aisle_aligned_pallet_agent",
                        "seedAgentId": "air_cargo_uld_optimizer",
                        "agentName": "Aisle-Aligned Pallet",
                        "sym": "Ap",
                        "code": "504",
                        "personaId": "outbound_lead_industrial_eng",
                        "legacyPersonaId": "air_cargo_charter_lead",
                        "personaName": "Outbound Lead / Industrial Eng.",
                        "personaIcon": "🧱",
                        "desc": "Sequences DC pick waves to match individual store planograms and shelf layouts.",
                        "outcome": "Cuts store stocking labor by 20–35%",
                        "buildTier": "High-Code",
                        "cadType": "corridor_lifo",
                    },
                    {
                        "agentId": "store_capacity_agent",
                        "seedAgentId": "meio_safety_stock_agent",
                        "agentName": "Store Capacity Agent",
                        "sym": "Sc",
                        "code": "505",
                        "personaId": "store_replenishment_lead",
                        "legacyPersonaId": None,
                        "personaName": "Store Replenishment Lead",
                        "personaIcon": "🏬",
                        "desc": "Throttles push replenishment based on store backroom limits and live POS velocity.",
                        "outcome": "Reduces backroom stock by 25%",
                        "buildTier": "High-Code",
                        "cadType": "conveyor_rack",
                    },
                    {
                        "agentId": "port_drayage_orchestrator",
                        "seedAgentId": "port_drayage_orchestrator",
                        "agentName": "Curfew Orchestrator",
                        "sym": "Cu",
                        "code": "506",
                        "personaId": "retail_logistics_dispatcher",
                        "legacyPersonaId": "global_trade_port_mgr",
                        "personaName": "Retail Logistics Dispatcher",
                        "personaIcon": "🕐",
                        "desc": "Coordinates municipal delivery curfews and store dock shift schedules dynamically.",
                        "outcome": "98%+ on-time store window compliance",
                        "buildTier": "Hybrid",
                        "cadType": "corridor_lifo",
                    },
                ],
            },
            {
                "id": "last_mile_delivery",
                "name": "Last-Mile Delivery",
                "color": "#059669",
                "icon": "📍",
                "items": [
                    {
                        "agentId": "geocoding_intelligence_agent",
                        "seedAgentId": "fleetflow_dispatch",
                        "agentName": "Geocoding Intelligence",
                        "sym": "Gi",
                        "code": "507",
                        "personaId": "last_mile_operations_lead",
                        "legacyPersonaId": None,
                        "personaName": "Last-Mile Operations Lead",
                        "personaIcon": "🗺️",
                        "desc": "Interprets gate codes, apartment delivery notes, and aerial imagery to guide drivers.",
                        "outcome": "Drops failed deliveries by 30–45%",
                        "buildTier": "Hybrid",
                        "cadType": "corridor_lifo",
                    },
                    {
                        "agentId": "multimodal_mode_shift_agent",
                        "seedAgentId": "multimodal_mode_shift_agent",
                        "agentName": "Courier Allocation",
                        "sym": "Ca",
                        "code": "508",
                        "personaId": "ecommerce_logistics_dir",
                        "legacyPersonaId": None,
                        "personaName": "E-Commerce Logistics Dir.",
                        "personaIcon": "📦",
                        "desc": "Routes parcels dynamically across internal fleet, 3PL, and gig couriers by rate card.",
                        "outcome": "Lowers last-mile cost by 8–14%",
                        "buildTier": "High-Code",
                        "cadType": "corridor_lifo",
                    },
                    {
                        "agentId": "otif_penalty_shield",
                        "seedAgentId": "otif_penalty_shield",
                        "agentName": "Delivery Exception Copilot",
                        "sym": "De",
                        "code": "509",
                        "personaId": "customer_support_ops_lead",
                        "legacyPersonaId": "otif_customer_service_lead",
                        "personaName": "Customer Support Ops Lead",
                        "personaIcon": "💬",
                        "desc": "Detects en-route exceptions and updates customers proactively with reschedule links.",
                        "outcome": "Decreases WISMO calls by up to 60%",
                        "buildTier": "Low-Code",
                        "cadType": "corridor_lifo",
                    },
                ],
            },
            {
                "id": "route_carrier",
                "name": "Route & Carrier",
                "color": "#4f46e5",
                "icon": "🧭",
                "items": [
                    {
                        "agentId": "fleetflow_dispatch",
                        "seedAgentId": "fleetflow_dispatch",
                        "agentName": "Dynamic Rerouter",
                        "sym": "Dr",
                        "code": "510",
                        "personaId": "fleet_dispatcher_central_ops",
                        "legacyPersonaId": "fleet_dispatch_mgr",
                        "personaName": "Fleet Dispatcher / Central Ops",
                        "personaIcon": "🚚",
                        "desc": "Recalculates multi-stop routes using live Google Maps traffic, radar, and bridge limits.",
                        "outcome": "Cuts fleet fuel usage by 6–10%",
                        "buildTier": "High-Code",
                        "cadType": "corridor_lifo",
                    },
                    {
                        "agentId": "freight_control_tower",
                        "seedAgentId": "freight_control_tower",
                        "agentName": "Routing Guide Compliance",
                        "sym": "Rg",
                        "code": "511",
                        "personaId": "transport_procurement_lead",
                        "legacyPersonaId": None,
                        "personaName": "Transport Procurement Lead",
                        "personaIcon": "📋",
                        "desc": "Tracks carrier tender acceptance & OTIF to reprioritize waterfall routing guides.",
                        "outcome": "Reduces spot freight by 15–20%",
                        "buildTier": "Low-Code",
                        "cadType": "corridor_lifo",
                    },
                    {
                        "agentId": "freight_bill_audit_agent",
                        "seedAgentId": "freight_control_tower",
                        "agentName": "Freight Bill Audit Agent",
                        "sym": "Fb",
                        "code": "512",
                        "personaId": "freight_controller_claims",
                        "legacyPersonaId": "freight_claims_analyst",
                        "personaName": "Freight Controller / Claims",
                        "personaIcon": "🧾",
                        "desc": "Extracts signed PODs and rate contracts via OCR to audit accessorial surcharges.",
                        "outcome": "Captures 3–7% in overbilled fees",
                        "buildTier": "Low-Code",
                        "cadType": "corridor_lifo",
                    },
                ],
            },
        ],
    },
    {
        "id": "circular_enable",
        "vNum": "06",
        "scorBadge": "06 · RETURNS & REVERSE LOGISTICS",
        "shortTab": "06 · Returns & Reverse",
        "name": "Returns & Reverse Logistics",
        "slideTitle": "Circularity & Value Recovery",
        "fullName": "Pillar 06: Circularity & Value Recovery — Returns & Reverse Logistics",
        "spineTitle": "REVERSE VALUE STREAM LIFECYCLE",
        "tagline": "Reverse Value Stream Lifecycle",
        "subtitle": "Triage inspection and upstream defect loops.",
        "slideSubtitle": "Agentic AI Value Stream: Smart return triage, markdown optimization, and asset reclamation.",
        "color": "#0d9488",
        "watermarkType": "circular_loop",
        "horizon": "Continuous Reverse Value Stream & Circularity Governance",
        "coreQuestion": "How do we stop returns fraud, optimize keep-it vs. reverse freight, prevent perishable expiry waste, and reclaim reusable pallets & totes?",
        "systems": "SAP Claims & Returns · Loop RMA · ESL Dynamic Pricing · RFID Portal Readers · CHEP/PECO Ledger · BigQuery",
        "solverSummary": "Gemini Vision Return Fraud & RTI Inspector + Keep-It Salvage Margin Solver + Dynamic DTE Markdown Engine + Milk-Run Backhaul CVRPTW",
        "toilMetric": "Return fraud abuse, perishable landfill scrap & lost pallet fines",
        "impactMetric": "-25–40% Return Fraud & -20–35% Perishable Scrap",
        "kpis": "Net Return Cost Reduction % | Perishable Scrap % | RTI Non-Return Fines | Backhaul Fill Rate %",
        "flow": "Returns & Claims Mgmt ──▶ Expiry & Markdowns ──▶ Pallet & Tote Reclamation",
        "vcId": "p2r",
        "vcLabel": "Open Plan-to-Recovery (P2R) Process →",
        "subPillars": [
            {
                "id": "returns_claims_mgmt",
                "name": "Returns & Claims Mgmt",
                "color": "#059669",
                "icon": "🛡️",
                "items": [
                    {
                        "agentId": "reverse_rma_optimizer",
                        "seedAgentId": "reverse_rma_optimizer",
                        "agentName": "Return Fraud Sentinel",
                        "sym": "Rf",
                        "code": "601",
                        "personaId": "reverse_logistics_fraud_lead",
                        "legacyPersonaId": "reverse_logistics_mgr",
                        "personaName": "Reverse Logistics / Fraud Lead",
                        "personaIcon": "🔍",
                        "desc": "Analyzes item photos and packaging video feeds to detect wear or swapped tags.",
                        "outcome": "Cuts returns fraud abuse by 25–40%",
                        "buildTier": "Hybrid",
                        "cadType": "circular_loop",
                    },
                    {
                        "agentId": "keep_it_routing_advisor",
                        "seedAgentId": "reverse_rma_optimizer",
                        "agentName": "Keep-It & Routing Advisor",
                        "sym": "Kr",
                        "code": "602",
                        "personaId": "customer_experience_cx_lead",
                        "legacyPersonaId": None,
                        "personaName": "Customer Experience (CX) Lead",
                        "personaIcon": "💝",
                        "desc": "Evaluates salvage margins vs reverse freight to determine keep-it instant refunds.",
                        "outcome": "Lowers net return costs by 15–22%",
                        "buildTier": "High-Code",
                        "cadType": "circular_loop",
                    },
                    {
                        "agentId": "osd_freight_claims_agent",
                        "seedAgentId": "otif_penalty_shield",
                        "agentName": "OS&D Freight Claims",
                        "sym": "Os",
                        "code": "603",
                        "personaId": "claims_specialist_controller",
                        "legacyPersonaId": None,
                        "personaName": "Claims Specialist / Controller",
                        "personaIcon": "📑",
                        "desc": "Reconciles eBOLs, dock damage logs, and carrier contracts to auto-file disputes.",
                        "outcome": "Resolves carrier claims in <72 hours",
                        "buildTier": "Low-Code",
                        "cadType": "circular_loop",
                    },
                ],
            },
            {
                "id": "expiry_markdowns",
                "name": "Expiry & Markdowns",
                "color": "#d97706",
                "icon": "🏷️",
                "items": [
                    {
                        "agentId": "dynamic_markdown_agent",
                        "seedAgentId": "promo_lift_simulator",
                        "agentName": "Dynamic Markdown Agent",
                        "sym": "Dm",
                        "code": "604",
                        "personaId": "merchandising_store_ops_mgr",
                        "legacyPersonaId": None,
                        "personaName": "Merchandising / Store Ops Mgr",
                        "personaIcon": "🏷️",
                        "desc": "Correlates days-to-expiry (DTE) with sales velocity to trigger ESL shelf price cuts.",
                        "outcome": "Cuts perishable scrap by 20–35%",
                        "buildTier": "Hybrid",
                        "cadType": "demand_wave",
                    },
                    {
                        "agentId": "short_dated_redistributor",
                        "seedAgentId": "crossdock_transfer_orchestrator",
                        "agentName": "Short-Dated Redistributor",
                        "sym": "Sd",
                        "code": "605",
                        "personaId": "inventory_disposition_lead",
                        "legacyPersonaId": None,
                        "personaName": "Inventory Disposition Lead",
                        "personaIcon": "📦",
                        "desc": "Matches near-date DC lots with discounters or food banks before acceptance cutoffs.",
                        "outcome": "Diverts bulk perishables from landfill",
                        "buildTier": "High-Code",
                        "cadType": "circular_loop",
                    },
                    {
                        "agentId": "food_waste_esg_copilot",
                        "seedAgentId": "carbon_scope3_ledger",
                        "agentName": "Food Waste & ESG Copilot",
                        "sym": "Fw",
                        "code": "606",
                        "personaId": "cso_circular_lead",
                        "legacyPersonaId": None,
                        "personaName": "Chief Sustainability Officer",
                        "personaIcon": "🌱",
                        "desc": "Aggregates store shrink and organic haul logs to generate audited GHG diversion filings.",
                        "outcome": "Automates annual circularity reporting",
                        "buildTier": "Low-Code",
                        "cadType": "circular_loop",
                    },
                ],
            },
            {
                "id": "pallet_tote_reclamation",
                "name": "Pallet & Tote Reclamation",
                "color": "#4f46e5",
                "icon": "♻️",
                "items": [
                    {
                        "agentId": "rti_balance_reconciler",
                        "seedAgentId": "master_data_leadtime_steward",
                        "agentName": "RTI Balance Reconciler",
                        "sym": "Rb",
                        "code": "607",
                        "personaId": "asset_recovery_rti_manager",
                        "legacyPersonaId": None,
                        "personaName": "Asset Recovery / RTI Manager",
                        "personaIcon": "🔄",
                        "desc": "Reconciles RFID portal scans with CHEP/PECO statements to detect hoarding nodes.",
                        "outcome": "Eliminates 30% in non-return fee fines",
                        "buildTier": "Low-Code",
                        "cadType": "circular_loop",
                    },
                    {
                        "agentId": "intermodal_rail_linehaul_agent",
                        "seedAgentId": "intermodal_rail_linehaul_agent",
                        "agentName": "Milk-Run Consolidation",
                        "sym": "Mr",
                        "code": "608",
                        "personaId": "reverse_transport_planner",
                        "legacyPersonaId": "intermodal_rail_linehaul_lead",
                        "personaName": "Reverse Transport Planner",
                        "personaIcon": "🚛",
                        "desc": "Schedules dynamic backhauls to collect empty roll cages and RPCs from retail stores.",
                        "outcome": "Boosts backhaul fill rate by 25–40%",
                        "buildTier": "High-Code",
                        "cadType": "corridor_lifo",
                    },
                    {
                        "agentId": "sanitation_health_agent",
                        "seedAgentId": "inline_yield_guardian",
                        "agentName": "Sanitation & Health Agent",
                        "sym": "Sh",
                        "code": "609",
                        "personaId": "packaging_qa_food_safety",
                        "legacyPersonaId": None,
                        "personaName": "Packaging QA / Food Safety",
                        "personaIcon": "🧼",
                        "desc": "Inspects return photos and wash logs for structural fatigue and chemical compliance.",
                        "outcome": "Extends reusable lifecycle by 15–20%",
                        "buildTier": "Hybrid",
                        "cadType": "circular_loop",
                    },
                ],
            },
        ],
    },
]


def build_datasets(existing_agents, existing_personas):
    departments = {}
    personas = {}
    agents = {}
    periodic_meta = {}
    periodic_groups = []
    persona_vc_map = {}
    legacy_persona_aliases = {}
    legacy_agent_aliases = {
        "air_cargo_uld_optimizer": "aisle_aligned_pallet_agent",
        "echelon_inventory_allocator": "meio_safety_stock_agent",
        "warehouse_slotting_optimizer": "warehouse_slotting_agent",
        "dynamic_order_promising_atp": "atp_order_promising_agent",
        "yard_dock_scheduling_agent": "yard_dock_sequencer",
        "plant_oee_maintenance_agent": "predictive_oee_sentinel",
        "inline_quality_inspection_agent": "inline_yield_guardian",
        "otif_chargeback_defender": "otif_penalty_shield",
        "circular_rma_orchestrator": "reverse_rma_optimizer",
        "esg_scope3_auditor": "carbon_scope3_ledger",
    }

    low_code_ids = []
    hybrid_ids = []
    high_code_ids = []

    for pillar in PDF_PILLARS:
        pid = pillar["id"]
        p_persona_ids = []
        p_agent_ids = []
        sub_pillars_meta = []

        for sp in pillar["subPillars"]:
            sp_id = sp["id"]
            sp_name = sp["name"]
            sp_color = sp["color"]
            sp_items_meta = []
            sp_agent_ids = [it["agentId"] for it in sp["items"]]

            for idx, item in enumerate(sp["items"]):
                ag_id = item["agentId"]
                per_id = item["personaId"]
                p_persona_ids.append(per_id)
                p_agent_ids.append(ag_id)
                persona_vc_map[per_id] = pillar["vcId"]

                if item["legacyPersonaId"]:
                    legacy_persona_aliases[item["legacyPersonaId"]] = per_id

                if item["buildTier"] == "Low-Code":
                    low_code_ids.append(ag_id)
                elif item["buildTier"] == "Hybrid":
                    hybrid_ids.append(ag_id)
                else:
                    high_code_ids.append(ag_id)

                # Seed from existing agent so ADK architecture & demo tables are always rich
                seed_ag = copy.deepcopy(
                    existing_agents.get(item["seedAgentId"])
                    or existing_agents.get("demand_sensing_agent")
                )

                sibling_ag_1 = sp_agent_ids[(idx + 1) % len(sp_agent_ids)]
                sibling_ag_2 = sp_agent_ids[(idx + 2) % len(sp_agent_ids)]

                # Update Agent fields to match the PDF 100%
                seed_ag["id"] = ag_id
                seed_ag["deptId"] = pid
                seed_ag["subPillarId"] = sp_id
                seed_ag["subPillarName"] = sp_name
                seed_ag["subPillarColor"] = sp_color
                seed_ag["isUniversal"] = False
                seed_ag["usedByPersonaIds"] = [per_id]
                seed_ag["primaryPersonaId"] = per_id
                seed_ag["primaryPersonaName"] = item["personaName"]
                seed_ag["name"] = item["agentName"]
                seed_ag["shortDesc"] = item["desc"]
                seed_ag["tagline"] = f"{sp_name} · {item['desc']}"
                seed_ag["badge"] = item["outcome"]
                seed_ag["cadType"] = item["cadType"]
                seed_ag["problem"] = (
                    f"In {sp_name}, {item['personaName']} teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before {item['agentName']} intervenes."
                )
                seed_ag["solution"] = item["desc"]
                seed_ag["outcome"] = f"{item['outcome']}."

                if "roiMetrics" in seed_ag and len(seed_ag["roiMetrics"]) >= 1:
                    seed_ag["roiMetrics"][0]["val"] = item["outcome"].split(" ")[0]
                    seed_ag["roiMetrics"][0]["label"] = item["outcome"]

                if "demoExecution" in seed_ag and isinstance(seed_ag["demoExecution"], dict):
                    seed_ag["demoExecution"]["agentName"] = item["agentName"]
                    if "sampleExecution" in seed_ag["demoExecution"]:
                        seed_ag["demoExecution"]["sampleExecution"]["vegaChartTitle"] = (
                            f"{item['agentName']} — {sp_name} Telemetry"
                        )

                agents[ag_id] = seed_ag

                # Build Persona object with clean, simple 4-step Daily Journey
                seed_per = copy.deepcopy(
                    existing_personas.get(item["legacyPersonaId"] or "")
                    or existing_personas.get("demand_planning_dir")
                )
                other_items = [x for x in sp["items"] if x["agentId"] != ag_id]
                other_1 = other_items[0] if len(other_items) > 0 else item
                other_2 = other_items[1] if len(other_items) > 1 else item

                personas[per_id] = {
                    "id": per_id,
                    "deptId": pid,
                    "subPillarId": sp_id,
                    "subPillarName": sp_name,
                    "subPillarColor": sp_color,
                    "icon": item["personaIcon"],
                    "name": item["personaName"],
                    "role": f"{sp_name} · {pillar['name']}",
                    "mandate": f"Leads {sp_name.lower()} across {pillar['name']}: {item['desc'].lower()}",
                    "summary": f"Owns {sp_name.lower()} execution within {pillar['slideTitle']}—partnering with {item['agentName']} to {item['outcome'].lower()}.",
                    "focusAreas": [
                        sp_name,
                        item["agentName"],
                        item["outcome"],
                        pillar["name"],
                    ],
                    "headlineStat": item["outcome"],
                    "headlineLabel": f"{sp_name} Impact",
                    "timeSaved": item["outcome"],
                    "toilHoursBefore": "5.5 hrs/day manual toil",
                    "toilHoursAfter": "45 mins/day exception review",
                    "primaryAgentId": ag_id,
                    "agentIds": [ag_id, sibling_ag_1, sibling_ag_2],
                    "dayInLife": [
                        {
                            "time": "8:30 AM",
                            "task": f"{sp_name}: Signal & Telemetry Triage",
                            "isToil": True,
                            "toilTime": "2.0 hrs",
                            "afterTime": "5 mins",
                            "before": f"Manually pulls ERP, WMS/TMS, and portal spreadsheets to diagnose {sp_name.lower()} variances and exceptions across regions.",
                            "after": f"{item['agentName']} automatically {item['desc'][0].lower() + item['desc'][1:]} — {item['outcome'].lower()}.",
                            "agentId": ag_id,
                        },
                        {
                            "time": "11:00 AM",
                            "task": f"Cross-Functional {other_1['agentName']} Alignment",
                            "isToil": True,
                            "toilTime": "1.8 hrs",
                            "afterTime": "10 mins",
                            "before": f"Chases email approvals and reconciles conflicting assumptions across adjacent {sp_name.lower()} teams.",
                            "after": f"{other_1['agentName']} {other_1['desc'][0].lower() + other_1['desc'][1:]} — {other_1['outcome'].lower()}.",
                            "agentId": other_1["agentId"],
                        },
                        {
                            "time": "2:00 PM",
                            "task": f"Exception Resolution & ERP Write-Back",
                            "isToil": True,
                            "toilTime": "1.7 hrs",
                            "afterTime": "10 mins",
                            "before": f"Manually keys line-by-line adjustments into {pillar['systems'].split('·')[0].strip()} after afternoon fire-drills.",
                            "after": f"{other_2['agentName']} {other_2['desc'][0].lower() + other_2['desc'][1:]} — {other_2['outcome'].lower()}.",
                            "agentId": other_2["agentId"],
                        },
                        {
                            "time": "4:30 PM",
                            "task": f"Executive {sp_name} Governance Review",
                            "isToil": False,
                            "activity": f"Reviews exception-only scorecards and locks decisions across {pillar['slideTitle']}.",
                            "tag": sp_name,
                        },
                    ],
                }

                # Periodic Table Element Metadata
                layer_map = {
                    "Low-Code": ("Gemini Enterprise Studio + RAG", "#10b981", "Chat-Initiated", "💬"),
                    "Hybrid": ("Vertex AI ADK + Cloud Run Tool", "#3b82f6", "Event-Driven", "⚡"),
                    "High-Code": ("OR-Tools + Vertex ADK", "#f59e0b", "Scheduled / Event", "🛡️"),
                }
                layer_name, layer_col, trig_name, trig_icon = layer_map.get(
                    item["buildTier"], ("Vertex AI ADK + A2A", "#3b82f6", "Event-Driven", "⚡")
                )
                periodic_meta[ag_id] = {
                    "code": item["code"],
                    "sym": item["sym"],
                    "short": item["agentName"],
                    "subPillar": sp_name,
                    "subPillarColor": sp_color,
                    "personaId": per_id,
                    "personaName": item["personaName"],
                    "group": pid,
                    "layer": layer_name,
                    "layerColor": layer_col,
                    "trigger": trig_name,
                    "trigIcon": trig_icon,
                }

                sp_items_meta.append(
                    {
                        "agentId": ag_id,
                        "agentName": item["agentName"],
                        "personaId": per_id,
                        "personaName": item["personaName"],
                        "personaIcon": item["personaIcon"],
                        "desc": item["desc"],
                        "outcome": item["outcome"],
                        "buildTier": item["buildTier"],
                    }
                )

            sub_pillars_meta.append(
                {
                    "id": sp_id,
                    "name": sp_name,
                    "color": sp_color,
                    "icon": sp["icon"],
                    "items": sp_items_meta,
                }
            )

        departments[pid] = {
            "id": pid,
            "vNum": pillar["vNum"],
            "scorBadge": pillar["scorBadge"],
            "name": pillar["name"],
            "slideTitle": pillar["slideTitle"],
            "fullName": pillar["fullName"],
            "spineTitle": pillar["spineTitle"],
            "tagline": pillar["tagline"],
            "subtitle": pillar["subtitle"],
            "slideSubtitle": pillar["slideSubtitle"],
            "color": pillar["color"],
            "watermarkType": pillar["watermarkType"],
            "horizon": pillar["horizon"],
            "coreQuestion": pillar["coreQuestion"],
            "systems": pillar["systems"],
            "solverSummary": pillar["solverSummary"],
            "toilMetric": pillar["toilMetric"],
            "toilBullets": [
                f"Fragmented workflows across {', '.join(sp['name'] for sp in pillar['subPillars'])}",
                "Delayed exception detection due to batch ERP exports and manual spreadsheet reconciliation",
                "High operational toil preventing planners and operators from focusing on strategic exceptions",
            ],
            "impactMetric": pillar["impactMetric"],
            "impactBullets": [
                f"{sp['name']}: {sp['items'][0]['outcome']} ({sp['items'][0]['agentName']})"
                for sp in pillar["subPillars"]
            ],
            "kpis": pillar["kpis"],
            "vcId": pillar["vcId"],
            "vcLabel": pillar["vcLabel"],
            "subPillars": sub_pillars_meta,
            "personaIds": p_persona_ids,
            "agentIds": p_agent_ids,
            "flow": pillar["flow"],
        }

        periodic_groups.append(
            {
                "id": pid,
                "shortTab": f"{pillar['name']} ({pillar['vNum']})",
                "title": f"{pillar['vNum']} · {pillar['slideTitle'].upper()} ({pillar['spineTitle']})",
                "color": pillar["color"],
                "count": len(p_agent_ids),
            }
        )

    return (
        departments,
        personas,
        agents,
        periodic_meta,
        periodic_groups,
        persona_vc_map,
        legacy_persona_aliases,
        legacy_agent_aliases,
        low_code_ids,
        hybrid_ids,
    )


def build_value_chains():
    return {
        "f2f": {
            "id": "f2f",
            "shortTitle": "Forecast-to-Fulfill (F2F)",
            "title": "Forecast-to-Fulfill (F2F) Value Stream Process",
            "flowBadge": "End-to-End Planning → Manufacturing → Inventory Pipeline",
            "cardSubtitle": "Connects Demand Forecasting, Trade Promotion, S&OP / IBP, Production Scheduling, Inventory Positioning & Warehouse Slotting.",
            "cardFooterLeft": "6 Stages · 6 Sub-Pillars · 6 Personas & Agents",
            "color": "#2563eb",
            "sculpture": "sculpture_emerald_ribbon.png",
            "animGif": "anim_genome_dark.gif",
            "cadType": "demand_wave",
            "headlineStat": "7–14d Earlier",
            "headlineLabel": "Demand Shift Detection to Synchronized DC Slotting",
            "toilHoursBefore": "21-day siloed spreadsheet planning cycle",
            "toilHoursAfter": "45-minute synchronized Golden Thread loop",
            "summary": "Unifies Core Planning Lifecycle (Pillar 01), Manufacturing Operations (Pillar 03), and Inventory & DC Spine (Pillar 04) into a single continuous flow.",
            "focusAreas": [
                "Demand Forecasting",
                "Trade Promotion",
                "S&OP / IBP",
                "Production Scheduling",
                "Positioning & Optimization",
                "Warehouse Operations",
            ],
            "videoSrc": "videos/demand_sensing_demo.mp4",
            "hasPreloadedVideo": True,
            "problem": "Demand forecasting, trade promotions, S&OP, plant scheduling, and DC inventory buffers operate in sequential spreadsheet silos.",
            "solution": "Six agents across Pillars 01, 03, and 04 pass demand shifts, promotional lift, capacity envelopes, changeover schedules, and safety stock targets along one Golden Thread.",
            "advantage": "Detects demand shifts 7–14 days earlier, prevents break-even trade leakage, cuts sanitation downtime 15–25%, and reduces working capital 10–18%.",
            "stages": [
                {
                    "num": "Stage 01",
                    "name": "Demand Forecasting · Demand Sensing",
                    "ownerPersonaId": "demand_planner_forecaster",
                    "ownerLabel": "Demand Planner / Forecaster",
                    "agentId": "demand_sensing_agent",
                    "modality": "TimesFM + Weather & POS",
                    "color": "#2563eb",
                    "systems": ["SAP IBP", "POS Velocity", "Weather Anomalies", "BigQuery"],
                    "toilTime": "6.5 hrs",
                    "afterTime": "8 mins",
                    "before": "Regional POS and macro trends arrive weeks late in disconnected spreadsheets.",
                    "after": "Demand Sensing Agent synthesizes POS velocity, weather anomalies, and macro trends to detect demand shifts 7–14 days earlier.",
                    "goldenThread": "Publishes P10/P50/P90 demand shift vectors to Trade Promotion & S&OP.",
                },
                {
                    "num": "Stage 02",
                    "name": "Trade Promotion · Promo ROI Simulation",
                    "ownerPersonaId": "trade_marketing_manager",
                    "ownerLabel": "Trade Marketing Manager",
                    "agentId": "promo_lift_simulator",
                    "modality": "Price Elasticity & Lift",
                    "color": "#ea580c",
                    "systems": ["TPM Portal", "Nielsen/Circana", "SAP IBP", "BigQuery ML"],
                    "toilTime": "18 hrs",
                    "afterTime": "12 mins",
                    "before": "Trade promotions are planned on flat historical averages without cannibalization checks.",
                    "after": "Promo ROI Simulator models price elasticity, shelf lift, and incremental spend return to prevent break-even trade leakage.",
                    "goldenThread": "Locks net incremental promo volume into Consensus S&OP.",
                },
                {
                    "num": "Stage 03",
                    "name": "S&OP / IBP · Consensus & Gap Alignment",
                    "ownerPersonaId": "sop_supply_planning_dir",
                    "ownerLabel": "S&OP / Supply Planning Dir.",
                    "agentId": "sop_scenario_weaver",
                    "modality": "OR-Tools Capacity MILP",
                    "color": "#4f46e5",
                    "systems": ["SAP IBP S&OP", "Plant RCCP", "Finance P&L", "Vertex AI"],
                    "toilTime": "14 days",
                    "afterTime": "45 mins",
                    "before": "Unconstrained commercial demand clashes with factory line bottlenecks in late-month meetings.",
                    "after": "Consensus & Gap Agent reconciles unconstrained demand with factory plant bottleneck limits and highlights margin-dilutive imbalances.",
                    "goldenThread": "Releases constrained master production targets to Plant Scheduling.",
                },
                {
                    "num": "Stage 04",
                    "name": "Production Scheduling · Changeover Optimizer",
                    "ownerPersonaId": "master_production_scheduler",
                    "ownerLabel": "Master Production Scheduler",
                    "agentId": "finite_production_scheduler",
                    "modality": "CP-SAT Allergen/Washdown",
                    "color": "#ea580c",
                    "systems": ["SAP PP/DS", "Siemens Opcenter", "OR-Tools CP-SAT"],
                    "toilTime": "5.0 hrs",
                    "afterTime": "3 mins",
                    "before": "Manual sequencing of allergen, kosher, and packaging runs causes excessive sanitation washdowns.",
                    "after": "Changeover Optimizer sequences allergen, kosher, and packaging runs to cut sanitation downtime by 15–25%.",
                    "goldenThread": "Streams finished-goods output timestamps to Multi-Echelon Inventory.",
                },
                {
                    "num": "Stage 05",
                    "name": "Positioning & Optimization · Safety Stock",
                    "ownerPersonaId": "inventory_optimization_lead",
                    "ownerLabel": "Inventory Optimization Lead",
                    "agentId": "meio_safety_stock_agent",
                    "modality": "Multi-Echelon Buffer Solver",
                    "color": "#0284c7",
                    "systems": ["SAP IBP MEIO", "Cloud Spanner", "BigQuery"],
                    "toilTime": "5.5 hrs",
                    "afterTime": "10 mins",
                    "before": "Static safety stock rules trap working capital in low-velocity regional DCs.",
                    "after": "Safety Stock Agent recalibrates multi-echelon buffers using live lead-time and demand variance, cutting working capital by 10–18%.",
                    "goldenThread": "Sends SKU velocity tiers to Warehouse Operations for zone slotting.",
                },
                {
                    "num": "Stage 06",
                    "name": "Warehouse Operations · Dynamic Slotting",
                    "ownerPersonaId": "dc_operations_mgr",
                    "ownerLabel": "DC Operations Mgr / IE Lead",
                    "agentId": "warehouse_slotting_agent",
                    "modality": "Co-Pick Affinity Matrix",
                    "color": "#d97706",
                    "systems": ["Manhattan Active WMS", "Blue Yonder WMS", "OR-Tools"],
                    "toilTime": "6.0 hrs",
                    "afterTime": "15 mins",
                    "before": "Quarterly manual slotting leaves high-affinity promotional SKUs far from golden pick zones.",
                    "after": "Dynamic Slotting Agent evaluates co-pick affinity matrices to recommend fast-pick zone re-slotting, reducing picker transit time by 15–30%.",
                    "goldenThread": "Closes the F2F loop with real-time DC pick-wave readiness.",
                },
            ],
        },
        "o2d": {
            "id": "o2d",
            "shortTitle": "Order-to-Delivery (O2D)",
            "title": "Order-to-Delivery (O2D) Value Stream Process",
            "flowBadge": "Omnichannel Order → DC Wave → Store & Last-Mile Dispatch",
            "cardSubtitle": "Connects SFS/BOPIS Sourcing, Wave Fulfillment, First/Mid-Mile Consolidation, Aisle-Aligned Pallets, Dynamic Rerouting & Exception Copilot.",
            "cardFooterLeft": "6 Stages · 6 Sub-Pillars · 6 Personas & Agents",
            "color": "#059669",
            "sculpture": "sculpture_cyan_helix.png",
            "animGif": "anim_Read_dark.gif",
            "cadType": "corridor_lifo",
            "headlineStat": "-30–45% Fails",
            "headlineLabel": "Failed Deliveries Cut & +12–18% Trailer Fill",
            "toilHoursBefore": "Fragmented WMS, TMS, store dock & courier handoffs",
            "toilHoursAfter": "Synchronized omnichannel & fleet execution spine",
            "summary": "Orchestrates Dynamic Fulfillment (Pillar 04) and End-to-End Logistics (Pillar 05) from order promising through store replenishment and last-mile delivery.",
            "focusAreas": [
                "Omnichannel Visibility",
                "Warehouse Operations",
                "First & Mid-Mile",
                "Store Replenishment",
                "Route & Carrier",
                "Last-Mile Delivery",
            ],
            "videoSrc": "videos/fleetflow_dispatch_demo.mp4",
            "hasPreloadedVideo": True,
            "problem": "Sub-optimal node selection splits parcels, under-filled LTLs waste freight spend, mixed pallets slow store stocking, and en-route traffic causes missed windows.",
            "solution": "Six agents synchronize SFS/BOPIS order sourcing, wave cutoff balancing, FTL load consolidation, aisle-aligned pallet building, live Google Maps rerouting, and proactive customer alerts.",
            "advantage": "Boosts trailer fill rate 12–18%, cuts store stocking labor 20–35%, cuts fleet fuel 6–10%, and drops WISMO support calls by up to 60%.",
            "stages": [
                {
                    "num": "Stage 01",
                    "name": "Omnichannel Visibility · SFS / BOPIS Sourcing",
                    "ownerPersonaId": "omnichannel_fulfillment_dir",
                    "ownerLabel": "Omnichannel Fulfillment Dir.",
                    "agentId": "atp_order_promising_agent",
                    "modality": "Sub-50ms Node Optimizer",
                    "color": "#4f46e5",
                    "systems": ["Cloud Spanner ATP", "OMS", "Parcel Rate Cards"],
                    "toilTime": "4.0 hrs",
                    "afterTime": "<50 ms",
                    "before": "Static DOM rules assign orders to congested stores or high-zone parcel lanes, inflating split shipments.",
                    "after": "SFS / BOPIS Sourcing selects lowest-cost fulfillment nodes based on store labor and parcel zones, lowering parcel costs & split rates.",
                    "goldenThread": "Releases node-allocated order waves to DC Floor Operations.",
                },
                {
                    "num": "Stage 02",
                    "name": "Warehouse Operations · Wave Fulfillment Copilot",
                    "ownerPersonaId": "dc_shift_floor_lead",
                    "ownerLabel": "DC Shift Floor Lead",
                    "agentId": "wave_fulfillment_copilot",
                    "modality": "Dynamic Cutoff Balancer",
                    "color": "#d97706",
                    "systems": ["Manhattan Active WMS", "WES Labor Feed", "Carrier Schedule"],
                    "toilTime": "3.5 hrs",
                    "afterTime": "2 mins",
                    "before": "Imbalanced pick zones bottleneck packing stations right before carrier pickup cutoffs.",
                    "after": "Wave Fulfillment Copilot balances picker lines dynamically to protect carrier pickup cutoff times and prevent missed OTIF windows.",
                    "goldenThread": "Hands staged outbound waves to First & Mid-Mile Consolidation.",
                },
                {
                    "num": "Stage 03",
                    "name": "First & Mid-Mile · Load Consolidation",
                    "ownerPersonaId": "transport_planner_inbound_mgr",
                    "ownerLabel": "Transport Planner / Inbound Mgr",
                    "agentId": "load_consolidation_agent",
                    "modality": "3D Cube & Weight Solver",
                    "color": "#2563eb",
                    "systems": ["Oracle OTM", "Blue Yonder TMS", "OR-Tools 3D Bin"],
                    "toilTime": "4.5 hrs",
                    "afterTime": "35 secs",
                    "before": "Planners ship partial LTL trailers because multi-stop cube and axle-weight limits are too complex to model manually.",
                    "after": "Load Consolidation merges vendor LTLs into multi-stop FTL linehauls via cube & weight modeling for 12–18% higher trailer fill.",
                    "goldenThread": "Transmits trailer manifests to Store Replenishment pallet builders.",
                },
                {
                    "num": "Stage 04",
                    "name": "Store Replenishment · Aisle-Aligned Pallet",
                    "ownerPersonaId": "outbound_lead_industrial_eng",
                    "ownerLabel": "Outbound Lead / Industrial Eng.",
                    "agentId": "aisle_aligned_pallet_agent",
                    "modality": "Planogram Wave Sequencer",
                    "color": "#d97706",
                    "systems": ["WMS Pick Wave", "Store Planogram DB", "Robotic Palletizer"],
                    "toilTime": "5.0 hrs",
                    "afterTime": "5 mins",
                    "before": "DC pallets arrive mixed across multiple store aisles, forcing store associates to sort cases in backrooms.",
                    "after": "Aisle-Aligned Pallet sequences DC pick waves to match individual store planograms, cutting store stocking labor by 20–35%.",
                    "goldenThread": "Dispatches store-ready trailers to Fleet & Route Operations.",
                },
                {
                    "num": "Stage 05",
                    "name": "Route & Carrier · Dynamic Rerouter",
                    "ownerPersonaId": "fleet_dispatcher_central_ops",
                    "ownerLabel": "Fleet Dispatcher / Central Ops",
                    "agentId": "fleetflow_dispatch",
                    "modality": "Google Maps Live CVRPTW",
                    "color": "#4f46e5",
                    "systems": ["Google Maps Routes API", "Fleet Engine", "Samsara ELD"],
                    "toilTime": "4.5 hrs",
                    "afterTime": "15 secs",
                    "before": "Static morning route sheets fail when highway accidents, weather radar, or bridge limits block corridors.",
                    "after": "Dynamic Rerouter recalculates multi-stop routes using live Google Maps traffic, radar, and bridge limits, cutting fleet fuel by 6–10%.",
                    "goldenThread": "Streams live stop ETAs to Last-Mile Delivery & Customer Support.",
                },
                {
                    "num": "Stage 06",
                    "name": "Last-Mile Delivery · Delivery Exception Copilot",
                    "ownerPersonaId": "customer_support_ops_lead",
                    "ownerLabel": "Customer Support Ops Lead",
                    "agentId": "otif_penalty_shield",
                    "modality": "Proactive WISMO & Reschedule",
                    "color": "#059669",
                    "systems": ["Courier Telemetry", "CRM / OMS", "Gemini Enterprise"],
                    "toilTime": "6.0 hrs",
                    "afterTime": "Instant",
                    "before": "Customers discover delivery delays after windows pass, flooding support centers with WISMO calls.",
                    "after": "Delivery Exception Copilot detects en-route exceptions and updates customers proactively with reschedule links, decreasing WISMO calls by up to 60%.",
                    "goldenThread": "Feeds verified POD and exception logs back to Carrier Compliance.",
                },
            ],
        },
        "s2p": {
            "id": "s2p",
            "shortTitle": "Source-to-Pay (S2P)",
            "title": "Source-to-Pay (S2P) Strategic Procurement Process",
            "flowBadge": "Supplier Network → Material Should-Cost → Contract & PO Spine",
            "cardSubtitle": "Connects Disruption Sensing, Commodity Hedging, Dynamic Should-Costing, Supplier Onboarding, PO Expediting & 3-Way Match.",
            "cardFooterLeft": "6 Stages · 3 Sub-Pillars · 6 Personas & Agents",
            "color": "#7c3aed",
            "sculpture": "sculpture_amber_Mobius.png",
            "animGif": "anim_Discuss_dark.gif",
            "cadType": "supplier_graph",
            "headlineStat": "<48h Onboard",
            "headlineLabel": "2–3 Wk Advance Risk Warning & ~70% PO Delays Resolved",
            "toilHoursBefore": "6-week manual onboarding, blind RFPs & AP invoice holds",
            "toilHoursAfter": "Autonomous Procurement Lifecycle Spine (Pillar 02)",
            "summary": "Executes the complete Pillar 02 Strategic Procurement Lifecycle Spine across Supplier Network, Material & Packaging, and Contract & PO Management.",
            "focusAreas": [
                "Supplier Network",
                "Material & Packaging",
                "Contract & PO Mgmt",
                "Clean-Sheet Should-Cost",
                "EDI 855/856 Expediting",
                "Three-Way Match",
            ],
            "videoSrc": "videos/rfq_should_cost_demo.mp4",
            "hasPreloadedVideo": True,
            "problem": "Procurement teams get blindsided by sub-tier disruptions, negotiate without feedstock should-cost models, spend weeks onboarding backup vendors, and suffer AP holds on invoice mismatches.",
            "solution": "Six agents across the Procurement Lifecycle Spine sense multi-tier risks 2–3 weeks early, advise commodity hedging, deconstruct packaging specs, qualify vendors in <48h, expedite EDI POs, and resolve 3-way match disputes.",
            "advantage": "Delivers 2–3 week advance disruption warnings, cuts onboarding to <48h, resolves ~70% of standard PO delays, and prevents vendor holds while capturing early-pay discounts.",
            "stages": [
                {
                    "num": "Stage 01",
                    "name": "Supplier Network · Disruption Sensing Agent",
                    "ownerPersonaId": "procurement_dir_risk_mgr",
                    "ownerLabel": "Procurement Dir. / Risk Mgr",
                    "agentId": "tier_n_risk_sentinel",
                    "modality": "Spanner Multi-Tier Graph",
                    "color": "#0d9488",
                    "systems": ["Cloud Spanner Graph", "Port AIS Feeds", "D&B Financials"],
                    "toilTime": "16 hrs",
                    "afterTime": "90 secs",
                    "before": "Sub-tier supplier insolvencies or port closures remain invisible until Tier-1 shipments fail to arrive.",
                    "after": "Disruption Sensing Agent monitors multi-tier supply feeds, port delays, and vendor financials for 2–3 week advance disruption warning.",
                    "goldenThread": "Flags affected raw materials and packaging categories for Hedging & Sourcing.",
                },
                {
                    "num": "Stage 02",
                    "name": "Material & Packaging · Commodity Index Advisor",
                    "ownerPersonaId": "category_sourcing_mgr_direct",
                    "ownerLabel": "Category Sourcing Mgr (Direct)",
                    "agentId": "commodity_index_advisor",
                    "modality": "CBOT/Platts Feedstock Model",
                    "color": "#d97706",
                    "systems": ["CBOT / Platts", "SAP Ariba", "BigQuery ML"],
                    "toilTime": "8.0 hrs",
                    "afterTime": "10 mins",
                    "before": "Category managers lock forward contracts without correlating feedstock indices against plant depletion rates.",
                    "after": "Commodity Index Advisor correlates CBOT/Platts feedstocks with depletion to advise hedging and optimize forward-contract windows.",
                    "goldenThread": "Feeds live feedstock index curves into Dynamic Should-Costing.",
                },
                {
                    "num": "Stage 03",
                    "name": "Material & Packaging · Dynamic Should-Cost Agent",
                    "ownerPersonaId": "strategic_sourcing_lead",
                    "ownerLabel": "Strategic Sourcing Lead",
                    "agentId": "rfq_should_cost_agent",
                    "modality": "Parametric Spec Teardown",
                    "color": "#d97706",
                    "systems": ["PLM Spec Sheets", "Resin/Corrugate Indices", "SAP Ariba RFQ"],
                    "toilTime": "12 hrs",
                    "afterTime": "4 mins",
                    "before": "Suppliers quote opaque bundled unit prices that hide resin weight and conversion energy margins.",
                    "after": "Dynamic Should-Cost Agent deconstructs packaging specs (resin weight, corrugate, conversion energy) for fact-based margin leverage in RFPs.",
                    "goldenThread": "Sends target award packages to Supplier Qualification & Onboarding.",
                },
                {
                    "num": "Stage 04",
                    "name": "Supplier Network · Onboarding & Qual. Agent",
                    "ownerPersonaId": "procurement_operations_lead",
                    "ownerLabel": "Procurement Operations Lead",
                    "agentId": "supplier_quality_sentinel",
                    "modality": "Document AI BRC/ISO Parser",
                    "color": "#0d9488",
                    "systems": ["Document AI", "BRC/ISO Registry", "SAP Business Partner"],
                    "toilTime": "3 weeks",
                    "afterTime": "<48 hrs",
                    "before": "Manual review of BRC/ISO certificates, food-safety filings, and tax forms delays vendor activation for weeks.",
                    "after": "Onboarding & Qual. Agent parses BRC/ISO audits, food-safety filings, and tax registrations, cutting onboarding from weeks to <48h.",
                    "goldenThread": "Activates approved vendor master records for Contract & PO Execution.",
                },
                {
                    "num": "Stage 05",
                    "name": "Contract & PO Mgmt · PO Expediting Agent",
                    "ownerPersonaId": "buyer_procurement_coord",
                    "ownerLabel": "Buyer / Procurement Coord.",
                    "agentId": "master_data_leadtime_steward",
                    "modality": "EDI 855/856 Split-Ship",
                    "color": "#4f46e5",
                    "systems": ["SAP MM POs", "EDI 855/856", "Supplier Portal"],
                    "toilTime": "5.0 hrs",
                    "afterTime": "3 mins",
                    "before": "Buyers chase late PO acknowledgments via email and discover shortages when lines are about to starve.",
                    "after": "PO Expediting Agent monitors EDI 855/856 delay feeds and orchestrates supplier split-shipments, resolving ~70% of standard PO delays.",
                    "goldenThread": "Streams verified ASN and GRN quantities to Accounts Payable.",
                },
                {
                    "num": "Stage 06",
                    "name": "Contract & PO Mgmt · Three-Way Match Dispute",
                    "ownerPersonaId": "accounts_payable_lead",
                    "ownerLabel": "Accounts Payable Lead",
                    "agentId": "three_way_match_dispute",
                    "modality": "PO / GRN / Invoice Reconciler",
                    "color": "#4f46e5",
                    "systems": ["SAP FI-AP", "Goods Receipt (MIGO)", "Carrier Invoices"],
                    "toilTime": "6.0 hrs",
                    "afterTime": "2 mins",
                    "before": "Price or quantity variances across POs, GRNs, and invoices trigger manual AP blocks and lost early-pay discounts.",
                    "after": "Three-Way Match Dispute diagnoses discrepancies across POs, GRNs, and carrier invoices, preventing vendor holds & saving discounts.",
                    "goldenThread": "Closes the S2P loop and posts Rebate Tier compliance back to Sourcing.",
                },
            ],
        },
        "p2r": {
            "id": "p2r",
            "shortTitle": "Plan-to-Recovery (P2R)",
            "title": "Plan-to-Recovery (P2R) Circular & Quality Value Stream",
            "flowBadge": "Dock Receiving → Inline QA → Expiry Markdown → Circular Recovery",
            "cardSubtitle": "Connects Dock-to-Stock, Visual Defect QA, Dynamic Markdowns, Return Fraud Sentinel, RTI Pallet Reclamation & Food Waste ESG.",
            "cardFooterLeft": "6 Stages · 5 Sub-Pillars · 6 Personas & Agents",
            "color": "#0d9488",
            "sculpture": "sculpture_violet_torus.png",
            "animGif": "anim_build_dark.gif",
            "cadType": "circular_loop",
            "headlineStat": "-25–40% Fraud",
            "headlineLabel": "Return Fraud Cut & -20–35% Perishable Scrap",
            "toilHoursBefore": "Dock bottlenecks, pallet holds, expiry write-offs & lost CHEP pallets",
            "toilHoursAfter": "Autonomous Circularity & Value Recovery Spine (Pillar 06)",
            "summary": "Links Inbound Receiving (Pillar 04) and Quality & Compliance (Pillar 03) with Returns, Expiry Markdowns, and Pallet Reclamation (Pillar 06).",
            "focusAreas": [
                "Warehouse Operations",
                "Quality & Compliance",
                "Expiry & Markdowns",
                "Returns & Claims Mgmt",
                "Pallet & Tote Reclamation",
                "Circular ESG Reporting",
            ],
            "videoSrc": "videos/reverse_rma_demo.mp4",
            "hasPreloadedVideo": True,
            "problem": "Slow dock receiving, undetected packaging defects, unpriced short-dated stock, fraudulent customer returns, and unreturned CHEP/PECO pallets drain millions in margin.",
            "solution": "Six agents reconcile dock BOLs in minutes, triage inline defects via vision, trigger dynamic ESL expiry markdowns, block return fraud, reconcile RFID pallet balances, and automate GHG circularity filings.",
            "advantage": "Cuts perishable scrap 20–35%, cuts return fraud 25–40%, eliminates 30% in non-return pallet fines, and automates annual circularity reporting.",
            "stages": [
                {
                    "num": "Stage 01",
                    "name": "Warehouse Operations · Dock-to-Stock Agent",
                    "ownerPersonaId": "inbound_receiving_supervisor",
                    "ownerLabel": "Inbound Receiving Supervisor",
                    "agentId": "dock_to_stock_agent",
                    "modality": "BOL OCR & Pallet Vision",
                    "color": "#d97706",
                    "systems": ["Manhattan WMS", "Dock Vision Portal", "EDI 856 ASN"],
                    "toilTime": "4.5 hrs",
                    "afterTime": "4 mins",
                    "before": "Manual paper BOL checks and ASN discrepancy hunts leave inbound pallets sitting on staging docks for hours.",
                    "after": "Dock-to-Stock Agent parses scanned BOLs and pallet photos to reconcile open ASN variances, cutting dock turnaround to minutes.",
                    "goldenThread": "Registers lot codes and shelf-life dates into Quality & Inventory.",
                },
                {
                    "num": "Stage 02",
                    "name": "Quality & Compliance · Visual Defect Triager",
                    "ownerPersonaId": "qa_manager_line_inspector",
                    "ownerLabel": "QA Manager / Line Inspector",
                    "agentId": "inline_yield_guardian",
                    "modality": "High-Speed Frame Vision",
                    "color": "#0d9488",
                    "systems": ["Line Cameras", "Gemini Flash Vision", "SAP QM"],
                    "toilTime": "4.0 hrs",
                    "afterTime": "<50 ms",
                    "before": "Crimped seals or misprinted lot codes go unnoticed until full pallets are quarantined at final inspection.",
                    "after": "Visual Defect Triager inspects high-speed video frames for crimped seals, lot codes, and labels, preventing full pallet scrap & holds.",
                    "goldenThread": "Certifies lot quality and passes DTE shelf-life tracking to Merchandising.",
                },
                {
                    "num": "Stage 03",
                    "name": "Expiry & Markdowns · Dynamic Markdown Agent",
                    "ownerPersonaId": "merchandising_store_ops_mgr",
                    "ownerLabel": "Merchandising / Store Ops Mgr",
                    "agentId": "dynamic_markdown_agent",
                    "modality": "DTE Velocity ESL Pricing",
                    "color": "#d97706",
                    "systems": ["ESL Electronic Shelf Labels", "POS Velocity", "Lot DTE Ledger"],
                    "toilTime": "5.0 hrs",
                    "afterTime": "5 mins",
                    "before": "Store associates apply flat manual markdown stickers too late, sending unsold perishables to landfill.",
                    "after": "Dynamic Markdown Agent correlates days-to-expiry (DTE) with sales velocity to trigger ESL shelf price cuts, cutting perishable scrap by 20–35%.",
                    "goldenThread": "Routes remaining near-date or returned stock to Reverse Logistics.",
                },
                {
                    "num": "Stage 04",
                    "name": "Returns & Claims · Return Fraud Sentinel",
                    "ownerPersonaId": "reverse_logistics_fraud_lead",
                    "ownerLabel": "Reverse Logistics / Fraud Lead",
                    "agentId": "reverse_rma_optimizer",
                    "modality": "Multimodal Return Inspection",
                    "color": "#059669",
                    "systems": ["Loop RMA Portal", "Return Bench Cameras", "SAP Returns"],
                    "toilTime": "5.5 hrs",
                    "afterTime": "12 secs",
                    "before": "Worn items and swapped barcode tags slip through manual return benches, eroding net recovery margins.",
                    "after": "Return Fraud Sentinel analyzes item photos and packaging video feeds to detect wear or swapped tags, cutting return fraud abuse by 25–40%.",
                    "goldenThread": "Releases verified reusable totes and pallets to Asset Recovery.",
                },
                {
                    "num": "Stage 05",
                    "name": "Pallet & Tote Reclamation · RTI Balance Reconciler",
                    "ownerPersonaId": "asset_recovery_rti_manager",
                    "ownerLabel": "Asset Recovery / RTI Manager",
                    "agentId": "rti_balance_reconciler",
                    "modality": "RFID & CHEP/PECO Audit",
                    "color": "#4f46e5",
                    "systems": ["RFID Dock Portals", "CHEP / PECO Statements", "BigQuery"],
                    "toilTime": "6.0 hrs",
                    "afterTime": "8 mins",
                    "before": "Unreconciled pallet pool statements and store hoarding result in steep CHEP/PECO non-return penalty fines.",
                    "after": "RTI Balance Reconciler reconciles RFID portal scans with CHEP/PECO statements to detect hoarding nodes, eliminating 30% in non-return fee fines.",
                    "goldenThread": "Streams asset reuse and waste diversion metrics to Sustainability.",
                },
                {
                    "num": "Stage 06",
                    "name": "Expiry & Markdowns · Food Waste & ESG Copilot",
                    "ownerPersonaId": "cso_circular_lead",
                    "ownerLabel": "Chief Sustainability Officer",
                    "agentId": "food_waste_esg_copilot",
                    "modality": "Audited GHG Diversion Ledger",
                    "color": "#0d9488",
                    "systems": ["Store Shrink Logs", "Organic Haul Manifests", "CSRD / SEC Ledger"],
                    "toilTime": "3 weeks",
                    "afterTime": "15 mins",
                    "before": "Sustainability teams spend weeks stitching store shrink and organic haul spreadsheets for annual ESG filings.",
                    "after": "Food Waste & ESG Copilot aggregates store shrink and organic haul logs to generate audited GHG diversion filings automatically.",
                    "goldenThread": "Completes the Circular Value Stream loop back to Executive Planning.",
                },
            ],
        },
    }


def main():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # Extract existing AGENTS and PERSONAS so we preserve ADK traces and demo tables
    m_ag = re.search(r"const AGENTS = (\{.*?\n\});", html, re.S)
    m_per = re.search(r"const PERSONAS = (\{.*?\n\});", html, re.S)
    if not m_ag or not m_per:
        raise RuntimeError("Could not locate AGENTS or PERSONAS in index.html")

    existing_agents = json.loads(m_ag.group(1))
    existing_personas = json.loads(m_per.group(1))

    (
        departments,
        personas,
        agents,
        periodic_meta,
        periodic_groups,
        persona_vc_map,
        legacy_persona_aliases,
        legacy_agent_aliases,
        low_code_ids,
        hybrid_ids,
    ) = build_datasets(existing_agents, existing_personas)

    value_chains = build_value_chains()

    print(
        f"Built PDF Taxonomy: {len(departments)} Pillars, "
        f"{sum(len(d['subPillars']) for d in departments.values())} Sub-Pillars, "
        f"{len(personas)} Personas, {len(agents)} Agents, {len(value_chains)} Value Chains."
    )

    # 1. Update data/supply_chain_catalog.json
    if os.path.exists(CATALOG_JSON_PATH):
        with open(CATALOG_JSON_PATH, "r", encoding="utf-8") as f:
            cat = json.load(f)
    else:
        cat = {}
    cat["departments"] = departments
    cat["personas"] = personas
    cat["agents"] = agents
    cat["valueChains"] = value_chains
    cat["universalAgentIds"] = [
        "csco_control_tower_copilot",
        "disruption_war_room_orchestrator",
        "master_data_leadtime_steward",
        "working_capital_cash_bridge",
    ]
    with open(CATALOG_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(cat, f, indent=2)
    print("Updated:", CATALOG_JSON_PATH)

    # 2. Update data/periodic_table_elements.json
    pt_json = {
        "groups": periodic_groups,
        "elements": periodic_meta,
        "totalAgents": len(agents),
        "totalPersonas": len(personas),
        "totalSubPillars": 20,
    }
    with open(PERIODIC_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(pt_json, f, indent=2)
    print("Updated:", PERIODIC_JSON_PATH)

    # 3. Replace DEPARTMENTS, PERSONAS, AGENTS, UNIVERSAL_AGENT_IDS, PERSONA_VALUE_CHAIN_MAP, VALUE_CHAINS in index.html
    dept_aliases_js = """
    Object.defineProperty(DEPARTMENTS, 'sourcing_risk', { get: () => DEPARTMENTS.sourcing_procurement, enumerable: false, configurable: true });
    Object.defineProperty(DEPARTMENTS, 'inventory_meio', { get: () => DEPARTMENTS.inventory_warehouse, enumerable: false, configurable: true });
    Object.defineProperty(DEPARTMENTS, 'warehousing_qa', { get: () => DEPARTMENTS.inventory_warehouse, enumerable: false, configurable: true });
    Object.defineProperty(DEPARTMENTS, 'warehouse_intralogistics', { get: () => DEPARTMENTS.inventory_warehouse, enumerable: false, configurable: true });
    Object.defineProperty(DEPARTMENTS, 'trade_mkt_dist', { get: () => DEPARTMENTS.logistics_fleet, enumerable: false, configurable: true });
    Object.defineProperty(DEPARTMENTS, 'reverse_risk_esg', { get: () => DEPARTMENTS.circular_enable, enumerable: false, configurable: true });
    Object.defineProperty(DEPARTMENTS, 'reverse_logistics_esg', { get: () => DEPARTMENTS.circular_enable, enumerable: false, configurable: true });
"""

    persona_aliases_lines = []
    for old_pid, new_pid in legacy_persona_aliases.items():
        if old_pid not in personas:
            persona_aliases_lines.append(
                f"    Object.defineProperty(PERSONAS, '{old_pid}', {{ get: () => PERSONAS['{new_pid}'], enumerable: false, configurable: true }});"
            )
    persona_aliases_js = "\n".join(persona_aliases_lines)

    agent_aliases_lines = []
    for old_aid, new_aid in legacy_agent_aliases.items():
        if old_aid not in agents:
            agent_aliases_lines.append(
                f"    Object.defineProperty(AGENTS, '{old_aid}', {{ get: () => AGENTS['{new_aid}'], enumerable: false, configurable: true }});"
            )
    agent_aliases_js = "\n".join(agent_aliases_lines)

    new_data_block = (
        "    /* 1. SIX CANONICAL VALUE STREAM PILLARS (20 SUB-PILLARS · 60 AGENTS · 60 PERSONAS) */\n"
        f"    const DEPARTMENTS = {json.dumps(departments, indent=2)};\n"
        f"{dept_aliases_js}\n"
        "    function getDeptMeta(deptId) {\n"
        "      if (DEPARTMENTS[deptId]) return DEPARTMENTS[deptId];\n"
        "      if (deptId === 'sourcing_risk') return DEPARTMENTS.sourcing_procurement;\n"
        "      if (deptId === 'inventory_warehouse') return DEPARTMENTS.inventory_warehouse;\n"
        "      if (deptId === 'circular_enable') return DEPARTMENTS.circular_enable;\n"
        "      return DEPARTMENTS.demand_sop;\n"
        "    }\n\n"
        "    /* 2. SUPPLY CHAIN PERSONAS ROSTER (60 ROLES ACROSS 6 PILLARS & 20 SUB-PILLARS) */\n"
        f"    const PERSONAS = {json.dumps(personas, indent=2)};\n"
        f"{persona_aliases_js}\n\n"
        "    /* 3. SUPPLY CHAIN AGENTS ROSTER (60 AGENTS ACROSS 6 PILLARS & 20 SUB-PILLARS) */\n"
        f"    const AGENTS = {json.dumps(agents, indent=2)};\n"
        f"{agent_aliases_js}\n\n"
        "    /* 4 CROSS-PILLAR EXECUTIVE COPILOTS */\n"
        "    const UNIVERSAL_AGENT_IDS = [\n"
        "      'csco_control_tower_copilot',\n"
        "      'disruption_war_room_orchestrator',\n"
        "      'master_data_leadtime_steward',\n"
        "      'working_capital_cash_bridge'\n"
        "    ];\n\n"
        "    /* 4. PERSONA -> VALUE CHAIN MAPPING (ALL 60 PERSONAS MAPPED ACROSS 4 SUITES) */\n"
        f"    const PERSONA_VALUE_CHAIN_MAP = {json.dumps(persona_vc_map, indent=2)};\n\n"
        "    /* 5. FOUR END-TO-END 6-STAGE AGENTIC VALUE CHAINS (F2F, O2D, S2P, P2R) */\n"
        f"    const VALUE_CHAINS = {json.dumps(value_chains, indent=2)};"
    )

    # Find exact span from `/* 1. SIX CANONICAL SCOR PILLARS UNDER THE CSCO */` to end of `VALUE_CHAINS`
    start_marker = "/* 1. SIX CANONICAL"
    start_idx = html.find(start_marker)
    if start_idx == -1:
        start_idx = html.find("const DEPARTMENTS = {")
    vc_end_match = re.search(
        r"const VALUE_CHAINS = \{.*?\n    \};\n", html[start_idx:], re.S
    )
    if not vc_end_match:
        raise RuntimeError("Could not find end of VALUE_CHAINS in index.html")
    end_idx = start_idx + vc_end_match.end()

    html = html[:start_idx] + new_data_block + "\n" + html[end_idx:]

    # 4. Update CSS for the new PDF Lifecycle Spine Board inside <style>
    spine_css = """
    /* =========================================================================
       7-PAGE PDF VALUE STREAM LIFECYCLE SPINE BOARD (PILLAR -> SUB-PILLAR -> 3 CARDS)
       ========================================================================= */
    .pdf-spine-banner {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      padding: 14px 20px;
      border-radius: 14px;
      background: #0f172a;
      border: 1px solid rgba(255, 255, 255, 0.14);
      margin: 16px 0 20px;
      box-shadow: 0 10px 26px rgba(0, 0, 0, 0.28);
    }

    .pdf-spine-label {
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #94a3b8;
    }

    .pdf-spine-steps {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }

    .pdf-spine-pill {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      padding: 7px 14px;
      border-radius: 9px;
      font-family: var(--font-display);
      font-size: 12.5px;
      font-weight: 800;
      color: #ffffff;
      background: var(--sp-color, #2563eb);
      border: 1.5px solid rgba(255, 255, 255, 0.22);
      cursor: pointer;
      transition: transform 0.18s ease, box-shadow 0.18s ease, opacity 0.18s ease;
    }

    .pdf-spine-pill:hover,
    .pdf-spine-pill.active {
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.35);
    }

    .pdf-spine-arrow {
      font-family: var(--font-mono);
      font-size: 14px;
      font-weight: 800;
      color: #64748b;
    }

    .pdf-subpillars-board {
      display: grid;
      grid-template-columns: repeat(var(--sp-cols, 3), minmax(0, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }

    @media (max-width: 1180px) {
      .pdf-subpillars-board {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }

    @media (max-width: 720px) {
      .pdf-subpillars-board {
        grid-template-columns: 1fr;
      }
    }

    .pdf-subpillar-col {
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 14px;
      border-radius: 16px;
      background: rgba(15, 23, 42, 0.55);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-top: 4px solid var(--sp-color, #2563eb);
    }

    .pdf-subpillar-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      padding: 10px 14px;
      border-radius: 10px;
      background: var(--sp-color, #2563eb);
      color: #ffffff;
      font-family: var(--font-display);
      font-size: 15px;
      font-weight: 800;
      letter-spacing: -0.01em;
    }

    .pdf-process-agent-card {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 10px;
      padding: 15px 16px;
      border-radius: 13px;
      background: var(--bg-card);
      border: 1px solid var(--border-strong);
      border-left: 4px solid var(--sp-color, #2563eb);
      transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }

    .pdf-process-agent-card:hover {
      transform: translateY(-3px);
      border-color: var(--sp-color, #2563eb);
      box-shadow: 0 12px 26px rgba(0, 0, 0, 0.28);
    }

    .pdf-card-agent-title {
      font-family: var(--font-display);
      font-size: 16px;
      font-weight: 800;
      color: var(--text-primary);
      line-height: 1.25;
      cursor: pointer;
    }

    .pdf-card-agent-title:hover {
      color: var(--sp-color, #2563eb);
    }

    .pdf-card-persona-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      align-self: flex-start;
      padding: 4px 10px;
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.15);
      font-size: 12px;
      font-weight: 700;
      color: var(--text-secondary);
      cursor: pointer;
      transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
    }

    .pdf-card-persona-btn:hover {
      background: var(--sp-color, #2563eb);
      border-color: var(--sp-color, #2563eb);
      color: #ffffff;
    }

    .pdf-card-desc {
      font-size: 13.5px;
      color: var(--text-secondary);
      line-height: 1.48;
    }

    .pdf-card-outcome-badge {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 7px 11px;
      border-radius: 8px;
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.35);
      color: #10b981;
      font-size: 12px;
      font-weight: 800;
      line-height: 1.3;
    }

    .pdf-card-actions {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      padding-top: 8px;
      border-top: 1px solid var(--border-subtle);
      font-size: 11.5px;
      font-weight: 800;
    }

    html[data-theme="light"] .pdf-subpillar-col {
      background: #f8fafc;
      border-color: #cbd5e1;
      border-top: 4px solid var(--sp-color, #2563eb);
    }

    html[data-theme="light"] .pdf-process-agent-card {
      background: #ffffff;
      border-color: #cbd5e1;
      border-left: 4px solid var(--sp-color, #2563eb);
      box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
    }

    html[data-theme="light"] .pdf-card-persona-btn {
      background: #f1f5f9;
      border-color: #cbd5e1;
      color: #1e293b;
    }

    html[data-theme="light"] .pdf-card-persona-btn:hover {
      background: var(--sp-color, #2563eb);
      border-color: var(--sp-color, #2563eb);
      color: #ffffff;
    }

    html[data-theme="light"] .pdf-card-outcome-badge {
      background: #ecfdf5;
      border-color: #6ee7b7;
      color: #047857;
    }
"""
    if ".pdf-spine-banner" not in html:
        html = html.replace("  </style>\n</head>", spine_css + "\n  </style>\n</head>", 1)

    # 5. Update Top Navbar & Master Tab Bar in HTML markup
    html = re.sub(
        r"6 SCOR Pillars ▾",
        "6 Pillars (20 Sub-Pillars) ▾",
        html,
    )
    html = re.sub(
        r"Personas \(\d+\) ▾",
        "Personas (60) ▾",
        html,
    )
    html = re.sub(
        r"Agents \(\d+\) ▾",
        "Agents (60) ▾",
        html,
    )
    html = re.sub(
        r"Explore 6 SCOR Pillars",
        "Explore 6 Value Stream Pillars",
        html,
    )
    html = re.sub(
        r"Office of the CSCO — The 6 ASCM SCOR Pillars",
        "Enterprise Supply Chain — 6 Core Operating Pillars",
        html,
    )
    html = re.sub(
        r"Select any pillar below to view what it means and explore its supply chain personas\.",
        "Click any of the 6 Core Operating Pillars below to expand its Sub-Pillar Lifecycle Spine, 60 Personas, and 60 AI Agents.",
        html,
    )

    # Replace #verticalTabsNavBar markup with the exact 6 PDF Pillars
    vtabs_html = """      <div class="vertical-tabs-nav-bar" id="verticalTabsNavBar">
        <button type="button" class="v-tab-btn active" data-vtab="all" onclick="switchVerticalTab('all', this)">
          <span class="v-tab-num" style="color:var(--g-blue);">ALL 6 PILLARS</span>
          <span class="v-tab-title">All 6 Pillars</span>
          <span class="v-tab-tag">20 Sub-Pillars · 60 Agents</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="demand_sop" onclick="switchVerticalTab('demand_sop', this)" style="--v-accent: #2563eb;">
          <span class="v-tab-num">01 · PLAN</span>
          <span class="v-tab-title">Planning &amp; Strategy</span>
          <span class="v-tab-tag">4 Sub-Pillars · 12 Agents</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="sourcing_procurement" onclick="switchVerticalTab('sourcing_procurement', this)" style="--v-accent: #7c3aed;">
          <span class="v-tab-num">02 · SOURCE</span>
          <span class="v-tab-title">Sourcing &amp; Procurement</span>
          <span class="v-tab-tag">3 Sub-Pillars · 9 Agents</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="manufacturing_prod" onclick="switchVerticalTab('manufacturing_prod', this)" style="--v-accent: #ea580c;">
          <span class="v-tab-num">03 · MAKE</span>
          <span class="v-tab-title">Manufacturing &amp; Prod</span>
          <span class="v-tab-tag">3 Sub-Pillars · 9 Agents</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="inventory_warehouse" onclick="switchVerticalTab('inventory_warehouse', this)" style="--v-accent: #0284c7;">
          <span class="v-tab-num">04 · FULFILL</span>
          <span class="v-tab-title">Inventory &amp; Warehousing</span>
          <span class="v-tab-tag">3 Sub-Pillars · 9 Agents</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="logistics_fleet" onclick="switchVerticalTab('logistics_fleet', this)" style="--v-accent: #059669;">
          <span class="v-tab-num">05 · DELIVER</span>
          <span class="v-tab-title">Distribution &amp; Logistics</span>
          <span class="v-tab-tag">4 Sub-Pillars · 12 Agents</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="circular_enable" onclick="switchVerticalTab('circular_enable', this)" style="--v-accent: #0d9488;">
          <span class="v-tab-num">06 · RETURN</span>
          <span class="v-tab-title">Returns &amp; Reverse Logistics</span>
          <span class="v-tab-tag">3 Sub-Pillars · 9 Agents</span>
        </button>
      </div>"""
    html = re.sub(
        r'<div class="vertical-tabs-nav-bar" id="verticalTabsNavBar">.*?</div>',
        vtabs_html,
        html,
        count=1,
        flags=re.S,
    )

    html = re.sub(
        r'<div class="cfo-box-sub">.*?</div>',
        '<div class="cfo-box-sub">6 Core Operating Pillars · 20 Sub-Pillars · 60 Personas · 60 AI Agents</div>',
        html,
        count=1,
    )
    html = re.sub(
        r"6 ASCM SCOR Verticals · 26 Enterprise Supply Chain Personas · 32 Agentic AI Systems \(4 Universal Core \+ 28 Domain Agents\) · 96 A2A Sub-Agents",
        "6 Core Operating Pillars · 20 Sub-Pillars · 60 Supply Chain Personas · 60 Agentic AI Systems · 180 A2A Sub-Agents",
        html,
    )

    # 6. Update renderOrgChart() so each of the 6 Pillar Cards displays its Sub-Pillars flow
    new_render_org_chart = """    function renderOrgChart() {
      const row = document.getElementById('deptRowContainer');
      if (!row) return;
      row.innerHTML = Object.values(DEPARTMENTS).map(dept => {
        const isActive = dept.id === selectedDeptId;
        const subPillars = dept.subPillars || [];
        const subPillarsHtml = subPillars.map((sp, idx) => `
          <span class="vc-mini-stage-pill" style="font-size:11px; padding:3px 8px;">
            <span class="st-idx" style="color:${sp.color};">0${idx + 1}</span>
            <span>${sp.name}</span>
          </span>
          ${idx < subPillars.length - 1 ? `<span class="vc-mini-arrow" style="color:${dept.color};">&rarr;</span>` : ''}
        `).join('');

        return `
          <div class="dept-node ${isActive ? 'active' : ''}"
               data-dept-id="${dept.id}"
               style="--dept-accent: ${dept.color};"
               onclick="selectDepartment('${dept.id}', event)">
            <div style="position:relative; z-index:2;">
              <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; margin-bottom:10px;">
                <div style="display:inline-flex; align-items:center; gap:6px; padding:4px 11px; border-radius:999px; font-size:11px; font-weight:800; letter-spacing:0.06em; text-transform:uppercase; background:${dept.color}18; color:${dept.color}; border:1px solid ${dept.color}40;">
                  <span>${dept.scorBadge || 'PILLAR'}</span>
                </div>
                <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:${dept.color};">
                  ${subPillars.length} Sub-Pillars
                </span>
              </div>
              <div class="dept-node-title">${dept.name}</div>
              <div class="dept-node-sub" style="margin-bottom:8px;">${dept.subtitle}</div>
              <div class="vc-mini-pipeline" style="margin-top:8px;">
                ${subPillarsHtml}
              </div>
            </div>
            <div class="dept-anim-stage">
              ${renderSupplyChainWatermarkSvg(dept.watermarkType, dept.color, 'dept-stage-svg')}
              <span class="dept-anim-meta">${subPillars.length} Sub-Pillars · ${dept.personaIds.length} Personas · ${dept.agentIds.length} Agents &rarr;</span>
            </div>
          </div>
        `;
      }).join('');

      renderDepartmentShowcaseBox();
    }"""

    html = re.sub(
        r"    function renderOrgChart\(\) \{.*?\n    \}",
        new_render_org_chart,
        html,
        count=1,
        flags=re.S,
    )

    # 7. Update getAgentBuildClassification() with the 60 PDF agents' build tiers
    new_build_cls_fn = f"""    function getAgentBuildClassification(ag) {{
      const lowCodeIds = new Set({json.dumps(low_code_ids)});
      const hybridIds = new Set({json.dumps(hybrid_ids)});

      const id = (ag && ag.id) ? ag.id : '';
      if (lowCodeIds.has(id)) {{
        return {{
          tier: 'Low-Code',
          label: '🟢 Low-Code · Gemini Enterprise Studio',
          shortLabel: '🟢 Low-Code Agent',
          platform: 'Gemini Enterprise No/Low-Code Builder + Grounded BigQuery RAG',
          engineTitle: 'Gemini Enterprise Studio',
          engineSub: 'Low-Code Prompt & Grounding',
          cssClass: 'build-tier-lowcode',
          color: '#34a853'
        }};
      }}
      if (hybridIds.has(id)) {{
        return {{
          tier: 'Hybrid',
          label: '🔵 Hybrid · Low-Code Agent + Cloud Run Tool',
          shortLabel: '🔵 Low-Code + Cloud Run',
          platform: 'Gemini Enterprise Conversational Flow + Cloud Run / Vision / Maps API Tool',
          engineTitle: 'Gemini Studio + Cloud Run',
          engineSub: 'Low-Code Flow + API Function',
          cssClass: 'build-tier-hybrid',
          color: '#4285f4'
        }};
      }}
      return {{
        tier: 'High-Code',
        label: '🟣 High-Code · Vertex ADK + OR-Tools Solver',
        shortLabel: '🟣 High-Code ADK + Solver',
        platform: 'Vertex AI ADK Multi-Agent + Google OR-Tools Deterministic Math Solver',
        engineTitle: 'Vertex ADK + OR-Tools',
        engineSub: 'High-Code Multi-Agent Solver',
        cssClass: 'build-tier-highcode',
        color: '#a142f4'
      }};
    }}"""

    html = re.sub(
        r"    function getAgentBuildClassification\(ag\) \{.*?\n    \}",
        new_build_cls_fn,
        html,
        count=1,
        flags=re.S,
    )

    # 8. Update populateNavbarQuickMenus() and renderDepartmentShowcaseBox() to show the PDF Lifecycle Spine Board
    new_nav_and_showcase = """    function populateNavbarQuickMenus() {
      const pillarsMenu = document.getElementById('navPillarsQuickMenu');
      const processesMenu = document.getElementById('navProcessesQuickMenu');
      const personasMenu = document.getElementById('navPersonasQuickMenu');
      const agentsMenu = document.getElementById('navAgentsQuickMenu');

      if (pillarsMenu) {
        pillarsMenu.innerHTML = Object.values(DEPARTMENTS).map(d => {
          const spCount = (d.subPillars || []).length;
          return `
            <button type="button" class="nav-quick-item" onclick="goHome(); setTimeout(() => switchVerticalTab('${d.id}'), 40);">
              <span style="display:flex; align-items:center; gap:8px;">
                <span style="width:8px; height:8px; border-radius:50%; background:${d.color};"></span>
                <span>${d.vNum} · ${d.name}</span>
              </span>
              <span style="font-size:11px; color:var(--text-secondary);">${spCount} Sub-Pillars · ${d.agentIds.length}A</span>
            </button>
          `;
        }).join('');
      }

      if (processesMenu) {
        processesMenu.innerHTML = `
          <button type="button" class="nav-quick-item" style="color:var(--g-blue); font-weight:800;" onclick="scrollToProcessJourneys()">
            <span>🔗 Open End-to-End Process Journeys (4)</span>
            <span>&rarr;</span>
          </button>
          <div class="nav-quick-group-title" style="color:#34a853;">Cross-Pillar End-to-End Value Streams (6 Stages Each)</div>
          ${Object.values(VALUE_CHAINS).map(vc => `
            <button type="button" class="nav-quick-item" onclick="openValueChainPage('${vc.id}', true, event)">
              <span style="display:flex; align-items:center; gap:8px;">
                <span style="width:8px; height:8px; border-radius:50%; background:${vc.color};"></span>
                <span>${vc.shortTitle}</span>
              </span>
              <span style="font-family:var(--font-mono); font-size:11px; color:${vc.color}; font-weight:700;">${vc.headlineStat}</span>
            </button>
          `).join('')}
        `;
      }

      if (personasMenu) {
        let html = `
          <button type="button" class="nav-quick-item" style="color:var(--g-blue); font-weight:800;" onclick="openPersonasDirectoryPage('all', '', true, 'personas')">
            <span>👥 Open Full Personas Directory (60)</span>
            <span>&rarr;</span>
          </button>
        `;
        Object.values(DEPARTMENTS).forEach(d => {
          html += `<div class="nav-quick-group-title" style="color:${d.color};">${d.vNum} · ${d.name} (${d.personaIds.length})</div>`;
          (d.personaIds || []).forEach(pid => {
            const p = PERSONAS[pid];
            if (!p) return;
            html += `
              <button type="button" class="nav-quick-item" onclick="openPersonaPage('${p.id}', true, event)">
                <span>${p.icon} ${p.name}</span>
                <span style="font-size:10.5px; color:${p.subPillarColor || d.color};">${p.subPillarName || ''} &rarr;</span>
              </button>
            `;
          });
        });
        personasMenu.innerHTML = html;
      }

      if (agentsMenu) {
        let html = `
          <button type="button" class="nav-quick-item" style="color:var(--g-blue); font-weight:800;" onclick="openPersonasDirectoryPage('all', '', true, 'agents')">
            <span>🤖 Open Full AI Agents Directory (60)</span>
            <span>&rarr;</span>
          </button>
        `;
        Object.values(DEPARTMENTS).forEach(d => {
          html += `<div class="nav-quick-group-title" style="color:${d.color};">${d.vNum} · ${d.name} (${d.agentIds.length})</div>`;
          (d.agentIds || []).forEach(aid => {
            const ag = AGENTS[aid];
            if (!ag) return;
            const cls = getAgentBuildClassification(ag);
            html += `
              <button type="button" class="nav-quick-item" onclick="openAgentPage('${ag.id}', true, event)">
                <span>${ag.name}</span>
                <span style="font-size:10.5px; color:${cls.color};">${ag.subPillarName || cls.tier}</span>
              </button>
            `;
          });
        });
        agentsMenu.innerHTML = html;
      }
    }

    let currentSelectedSubPillarId = 'all';

    function selectSubPillarFilter(spId) {
      currentSelectedSubPillarId = (currentSelectedSubPillarId === spId) ? 'all' : spId;
      renderDepartmentShowcaseBox();
    }

    function renderDepartmentShowcaseBox() {
      const container = document.getElementById('deptShowcaseContainer');
      if (!container) return;
      if (!selectedDeptId || !DEPARTMENTS[selectedDeptId]) {
        container.innerHTML = '';
        return;
      }
      const dept = DEPARTMENTS[selectedDeptId];
      const subPillars = dept.subPillars || [];
      if (currentSelectedSubPillarId !== 'all' && !subPillars.some(sp => sp.id === currentSelectedSubPillarId)) {
        currentSelectedSubPillarId = 'all';
      }
      const visibleSubPillars = currentSelectedSubPillarId === 'all'
        ? subPillars
        : subPillars.filter(sp => sp.id === currentSelectedSubPillarId);
      const colCount = visibleSubPillars.length;

      container.innerHTML = `
        <div id="deptShowcaseBoxEl" class="dept-showcase-box genie-enter" style="--dept-accent: ${dept.color};">
          <!-- Slide Header Row -->
          <div class="showcase-header" style="margin-bottom:14px;">
            <div>
              <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:4px;">
                <span style="padding:4px 10px; border-radius:8px; background:${dept.color}; color:#ffffff; font-family:var(--font-mono); font-size:11px; font-weight:800; letter-spacing:0.06em;">
                  PILLAR ${dept.vNum} · ${subPillars.length} SUB-PILLARS · ${dept.agentIds.length} AGENTS
                </span>
                <span style="font-size:13px; font-weight:700; color:${dept.color};">
                  ${dept.name}
                </span>
              </div>
              <div class="showcase-dept-name" style="font-size:clamp(22px, 2.4vw, 30px);">
                <span>${dept.slideTitle || dept.name}</span>
              </div>
              <div style="font-size:14.5px; color:var(--text-secondary); margin-top:2px;">
                ${dept.slideSubtitle || dept.subtitle}
              </div>
            </div>

            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <button type="button" class="switch-pill" style="border-color:${dept.color}; color:${dept.color}; font-weight:800;" onclick="openValueChainPage('${dept.vcId || 'f2f'}', true, event)">
                🔗 ${dept.vcLabel || 'Open End-to-End Process &rarr;'}
              </button>
              <button type="button" class="switch-pill" onclick="selectDepartment('${dept.id}')">
                ✕ Close
              </button>
            </div>
          </div>

          <!-- PDF Lifecycle Spine Navigation Bar (Pillar -> Sub-Pillars Connected by Arrows) -->
          <div class="pdf-spine-banner">
            <div style="display:flex; align-items:center; gap:10px;">
              <span style="width:10px; height:10px; border-radius:50%; background:${dept.color}; display:inline-block;"></span>
              <span class="pdf-spine-label">${dept.spineTitle || 'VALUE STREAM LIFECYCLE SPINE'}</span>
            </div>

            <div class="pdf-spine-steps">
              <button type="button"
                      class="pdf-spine-pill ${currentSelectedSubPillarId === 'all' ? 'active' : ''}"
                      style="--sp-color: #334155; opacity:${currentSelectedSubPillarId === 'all' ? '1' : '0.75'};"
                      onclick="selectSubPillarFilter('all')">
                <span>All ${subPillars.length} Sub-Pillars (${dept.agentIds.length})</span>
              </button>
              ${subPillars.map((sp, idx) => `
                <button type="button"
                        class="pdf-spine-pill ${currentSelectedSubPillarId === sp.id ? 'active' : ''}"
                        style="--sp-color: ${sp.color}; opacity:${currentSelectedSubPillarId === 'all' || currentSelectedSubPillarId === sp.id ? '1' : '0.55'};"
                        onclick="selectSubPillarFilter('${sp.id}')">
                  <span>${sp.icon} ${sp.name}</span>
                </button>
                ${idx < subPillars.length - 1 ? '<span class="pdf-spine-arrow">&rarr;</span>' : ''}
              `).join('')}
            </div>
          </div>

          <!-- PDF Slide Multi-Column Board: Sub-Pillar Columns -> 3 Process/Agent/Persona Cards Each -->
          <div class="pdf-subpillars-board" style="--sp-cols: ${colCount};">
            ${visibleSubPillars.map(sp => `
              <div class="pdf-subpillar-col" style="--sp-color: ${sp.color};">
                <div class="pdf-subpillar-header" style="--sp-color: ${sp.color};">
                  <span>${sp.icon} ${sp.name}</span>
                  <span style="font-family:var(--font-mono); font-size:11px; opacity:0.9;">3 Agents</span>
                </div>

                ${(sp.items || []).map(item => {
                  const ag = AGENTS[item.agentId];
                  const cls = getAgentBuildClassification(ag);
                  return `
                    <div class="pdf-process-agent-card" style="--sp-color: ${sp.color};">
                      <div>
                        <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:8px; margin-bottom:8px;">
                          <div class="pdf-card-agent-title" onclick="openAgentPage('${item.agentId}', true, event)">
                            ${item.agentName}
                          </div>
                          <span class="build-tier-badge ${cls.cssClass}" style="font-size:9.5px; padding:2px 7px; flex-shrink:0;">
                            ${cls.tier}
                          </span>
                        </div>

                        <button type="button"
                                class="pdf-card-persona-btn"
                                style="--sp-color: ${sp.color}; margin-bottom:10px;"
                                onclick="openPersonaPage('${item.personaId}', true, event)"
                                title="Open ${item.personaName} Daily Journey">
                          <span>👤 ${item.personaName}</span>
                          <span>&rarr;</span>
                        </button>

                        <div class="pdf-card-desc">
                          ${item.desc}
                        </div>
                      </div>

                      <div>
                        <div class="pdf-card-outcome-badge" style="margin-bottom:8px;">
                          <span>✓</span>
                          <span>${item.outcome}</span>
                        </div>

                        <div class="pdf-card-actions">
                          <button type="button"
                                  style="color:${sp.color}; font-weight:800; cursor:pointer;"
                                  onclick="openPersonaPage('${item.personaId}', true, event)">
                            👤 Persona Journey &rarr;
                          </button>
                          <button type="button"
                                  style="color:var(--g-blue); font-weight:800; cursor:pointer;"
                                  onclick="openAgentPage('${item.agentId}', true, event)">
                            ✦ Agent &amp; Demo &rarr;
                          </button>
                        </div>
                      </div>
                    </div>
                  `;
                }).join('')}
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }"""

    html = re.sub(
        r"    function populateNavbarQuickMenus\(\) \{.*?\n    function togglePersonaJourneyStep",
        new_nav_and_showcase + "\n\n    function togglePersonaJourneyStep",
        html,
        count=1,
        flags=re.S,
    )

    # 9. Update openPersonaPage so it shows the Sub-Pillar badge and only the Persona's Sub-Pillar Agents in the bottom dock
    html = html.replace(
        "${[...new Set([...(p.agentIds || []), ...UNIVERSAL_AGENT_IDS])].map(aid => {",
        "${[...new Set(p.agentIds || [])].map(aid => {",
    )
    html = html.replace(
        "${dept.scorBadge || ''} · ${dept.name}",
        "${dept.scorBadge || ''} · ${p.subPillarName || dept.name}",
    )

    # 10. Update Directory counts (29 -> 60 Personas, 35 -> 60 Agents, 32 -> 60)
    html = html.replace("👤 Human Personas (29)", "👤 Human Personas (60)")
    html = html.replace("✦ AI Agents (35)", "✦ AI Agents (60)")
    html = html.replace("✦ 35 Supply Chain AI Agents", "✦ 60 Supply Chain AI Agents")
    html = html.replace("👤 29 Supply Chain Human Personas", "👤 60 Supply Chain Human Personas")
    html = html.replace("All (${currentDirMode === 'agents' ? '35' : '29'})", "All (60)")
    html = re.sub(
        r"Object\.values\(AGENTS\)\.filter\(a => !a\.isUniversal && a\.deptId === d\.id\)\.length",
        "d.agentIds.length",
        html,
    )

    # 11. Replace PERIODIC_AGENT_META and PERIODIC_GROUPS and update counts in openPeriodicTablePage & openMindMapPage
    periodic_block = (
        f"    const PERIODIC_AGENT_META = {json.dumps(periodic_meta, indent=2)};\n\n"
        f"    const PERIODIC_GROUPS = {json.dumps(periodic_groups, indent=2)};"
    )
    html = re.sub(
        r"    const PERIODIC_AGENT_META = \{.*?\n    const PERIODIC_GROUPS = \[.*?\];",
        lambda _: periodic_block,
        html,
        count=1,
        flags=re.S,
    )

    html = html.replace(
        "Enterprise catalog of 32 autonomous AI agents across 7 SCOR domains and 26 personas.",
        "Enterprise catalog of 60 autonomous AI agents across 6 Value Stream Pillars, 20 Sub-Pillars, and 60 Personas.",
    )
    html = html.replace(
        '<span class="pt-tab-count">32</span>',
        '<span class="pt-tab-count">60</span>',
    )
    html = html.replace(
        '<span class="pt-tab-count">26</span>',
        '<span class="pt-tab-count">60</span>',
    )
    html = html.replace(
        "Persona-to-Agent Mapping (26 Supply Chain Roles)",
        "Persona-to-Agent Mapping (60 Supply Chain Roles)",
    )
    html = html.replace(
        "All 7 SCOR Domains &amp; Universal Core",
        "All 6 Operating Pillars &amp; 20 Sub-Pillars (60 AI Agents)",
    )
    html = html.replace(
        '<div class="pt-stat-badge"><strong>32</strong>agents</div>',
        '<div class="pt-stat-badge"><strong>60</strong>agents</div>',
    )
    html = html.replace(
        '<div class="pt-stat-badge"><strong>7</strong>domains</div>',
        '<div class="pt-stat-badge"><strong>20</strong>sub-pillars</div>',
    )
    html = html.replace(
        '<div class="pt-stat-badge"><strong>26</strong>personas</div>',
        '<div class="pt-stat-badge"><strong>60</strong>personas</div>',
    )
    html = html.replace(
        "const pAgents = [...(p.agentIds || []), ...UNIVERSAL_AGENT_IDS].map(id => AGENTS[id]).filter(Boolean);",
        "const pAgents = (p.agentIds || []).map(id => AGENTS[id]).filter(Boolean);",
    )
    html = html.replace(
        "let currentMindMapPersonaId = 'demand_planning_dir';",
        "let currentMindMapPersonaId = 'demand_planner_forecaster';",
    )
    html = html.replace(
        "End-to-end interactive topology mapping 6 SCOR domains, 26 personas, and 32 autonomous AI agents across the enterprise.",
        "End-to-end interactive topology mapping 6 Core Operating Pillars, 20 Sub-Pillars, 60 Personas, and 60 autonomous AI Agents.",
    )
    html = html.replace(
        '<span class="pt-tab-count">29 Personas &harr; 35 Agents</span>',
        '<span class="pt-tab-count">60 Personas &harr; 60 Agents</span>',
    )

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated:", INDEX_PATH)

    # 12. Sync periodic_table.html and mind_map.html from index.html
    pt_html = html.replace(
        "handleUrlHash();",
        "if (!window.location.hash) { window.location.hash = '#periodic'; } handleUrlHash();",
        1,
    )
    with open(PERIODIC_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(pt_html)
    print("Updated:", PERIODIC_HTML_PATH)

    mm_html = html.replace(
        "handleUrlHash();",
        "if (!window.location.hash) { window.location.hash = '#mindmap'; } handleUrlHash();",
        1,
    )
    with open(MINDMAP_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(mm_html)
    print("Updated:", MINDMAP_HTML_PATH)


if __name__ == "__main__":
    main()

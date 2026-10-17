#!/usr/bin/env python3
"""
Update data/supply_chain_catalog.json and data/periodic_table_elements.json
to reflect the canonical 8 Operational Verticals (Level-1 to Level-3 decomposition)
and the Three Rivers Flow architecture.
"""
import json
from pathlib import Path

ROOT = Path("/usr/local/google/home/zuhaibp/Supply_chain_Agentic_Transformation")
CATALOG_PATH = ROOT / "data" / "supply_chain_catalog.json"
PERIODIC_PATH = ROOT / "data" / "periodic_table_elements.json"

def update_catalog():
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        cat = json.load(f)

    # 1. Update metadata
    cat["metadata"]["scorVerticalsCount"] = 8
    cat["metadata"]["verticalsCount"] = 8

    # 2. Define the 8 Verticals
    verticals = {
        "demand_sop": {
            "id": "demand_sop",
            "vNum": "V1",
            "scorBadge": "VERTICAL 01 · DEMAND & S&OP",
            "name": "Demand Planning, Sensing & S&OP",
            "fullName": "Vertical 1: Demand Planning, Sensing & S&OP (The Forecasters)",
            "tagline": "The Forecasters",
            "subtitle": "Demand sensing, 45-min S&OP consensus, promo elasticity & retail CPFR",
            "color": "#10b981",
            "watermarkType": "demand_wave",
            "horizon": "Tactical Horizon (Weekly – 18 Months)",
            "coreQuestion": "What, how much, when, and where will customers buy—and can our network supply it?",
            "river": "River 2: Demand & Information Flow (◀── Upstream)",
            "systems": "SAP IBP · SAP S/4HANA · Kinaxis · o9 Solutions · EDI 852/830 POS · BigQuery · AlloyDB · Cloud Spanner · Vertex AI TimesFM · Google WeatherNext 3 · Google Maps Places · Apigee",
            "solverSummary": "Vertex AI TimesFM Zero-Shot Foundation Forecasting + Hierarchical Bayesian Reconciliation + Google OR-Tools MILP S&OP Capacity & Margin Solver on BigQuery & AlloyDB",
            "toilMetric": "65% of planning time lost",
            "toilBullets": [
                "Stitching 15+ disconnected sales, POS, distributor EDI 852, and marketing spreadsheets every cycle",
                "Order-history forecasts lag real-time customer sell-through by 2 to 4 weeks and ignore stockout censorship",
                "Promotions silently cannibalize 30%+ of sister SKUs while 21-day sequential S&OP cycles stall decisions"
            ],
            "impactMetric": "45-Min S&OP & +24% Forecast Accuracy",
            "impactBullets": [
                "Cuts demand forecast error by 24% ($14M+ saved in excess buffer stock & prevented stockouts; secondary KPI: -6.4% WAPE)",
                "Compresses S&OP planning cycles from 21 days to a live 45-minute executive review (-85% manual planner effort)",
                "Eliminates 30%+ promo cannibalization to boost net promotional return by +22% ($8M+ saved trade spend)"
            ],
            "kpis": "Forecast Accuracy (1 - WMAPE) | Mean Absolute Percentage Error (MAPE) | Forecast Bias (%)",
            "personaIds": ["demand_planning_dir", "sop_ibp_lead", "promo_launch_planner", "cpfr_channel_mgr"],
            "agentIds": ["demand_sensing_agent", "sop_scenario_weaver", "promo_lift_simulator", "cpfr_sync_agent"]
        },
        "sourcing_procurement": {
            "id": "sourcing_procurement",
            "vNum": "V2",
            "scorBadge": "VERTICAL 02 · SOURCING & PROCUREMENT",
            "name": "Strategic Sourcing & Category Procurement",
            "fullName": "Vertical 2: Strategic Sourcing & Category Procurement (The Buyers)",
            "tagline": "The Buyers",
            "subtitle": "Parametric should-cost RFQ, Tier-N Spanner graph, contract SLAs & inbound AQL QA",
            "color": "#a142f4",
            "watermarkType": "supplier_graph",
            "horizon": "Strategic & Operational Horizon",
            "coreQuestion": "Where do we procure raw materials & packaging at optimal total cost, lead time, and AQL quality?",
            "river": "Bridges River 1 (Inbound Material) and River 3 (Cash Outflows / DPO)",
            "systems": "SAP Ariba · SAP S/4HANA MM/QM/GTS · Coupa · Siemens Teamcenter BOM · Cloud Spanner Graph · BigQuery · AlloyDB · Google Maps Geocoding · Document AI · OR-Tools · Apigee",
            "solverSummary": "Cloud Spanner Tier-N Graph Neural Propagation + Parametric BOM Should-Cost + Google OR-Tools Combinatorial MILP Award Split + Document AI COA/Contract Parser",
            "toilMetric": "Zero visibility past Tier-1",
            "toilBullets": [
                "Weeks spent normalizing inconsistent supplier PDF and Excel RFQ quotes without bottom-up should-costs",
                "Sub-tier (Tier-2 / Tier-3) disruptions and lot quality defects stay hidden until factory lines stop",
                "Volume rebates, commodity index caps, and Free Trade Agreement (FTA) tariff savings leak unnoticed"
            ],
            "impactMetric": "-6.8% Spend & 11-Day Early Warning",
            "impactBullets": [
                "Parametric BOM should-cost decomposition & combinatorial multi-supplier RFQ award solver ($100M+ Unilever benchmark)",
                "Multi-tier (Tier-1 to Tier-4) Spanner dependency graph, predictive quality COA screening & backup PO routing (9 mos → hours)",
                "Continuous contract rebate recovery, HS tariff engineering & multi-tier provenance ledger"
            ],
            "kpis": "Purchase Price Variance (PPV) | Supplier OTIF % | Lead-Time Std Dev (σ_LT) | Cost Savings ($/₹)",
            "personaIds": ["category_sourcing_mgr", "supplier_risk_lead", "tariff_compliance_spec", "supplier_quality_lead"],
            "agentIds": ["rfq_should_cost_agent", "tier_n_risk_sentinel", "tariff_esg_agent", "supplier_quality_sentinel"]
        },
        "manufacturing_prod": {
            "id": "manufacturing_prod",
            "vNum": "V3",
            "scorBadge": "VERTICAL 03 · MANUFACTURING & MPS",
            "name": "Production Planning & Manufacturing / MPS",
            "fullName": "Vertical 3: Production Planning & Manufacturing / MPS (The Makers)",
            "tagline": "The Makers",
            "subtitle": "Finite MPS line scheduling, predictive spindle OEE, inline SPC yield & ECO cutover",
            "color": "#3b82f6",
            "watermarkType": "plant_oee",
            "horizon": "Tactical to Shift-Level Execution",
            "coreQuestion": "How do we sequence factory lines and synchronize BOM inputs for zero unplanned downtime?",
            "river": "River 1: Physical Material Flow (Factory WIP & Transformation)",
            "systems": "SAP S/4HANA PP/DS & PM · Siemens Opcenter MES · Rockwell Plex · OSIsoft PI Historian · Teamcenter PLM · BigQuery · AlloyDB · Cloud Spanner · OR-Tools CP-SAT · Pub/Sub & Dataflow",
            "solverSummary": "Google OR-Tools CP-SAT Sequence-Dependent Setup & Finite Capacity Job-Shop Scheduler + Vertex AI Multimodal Vibration/Thermal OEE Anomaly Model + Closed-Loop SPC",
            "toilMetric": "19% capacity lost to changeovers & stops",
            "toilBullets": [
                "Infinite-capacity ERP MRP schedules ignore sequence-dependent coil/paint/mold changeovers and line starvation",
                "Unplanned spindle, press, and robotics breakdowns halt high-margin production runs and trigger backorders",
                "Inline process parameter drift and uncoordinated Engineering Change Orders (ECOs) generate scrap and obsolete WIP"
            ],
            "impactMetric": "-48% Unplanned Downtime & -25% Backorders",
            "impactBullets": [
                "Autonomous OR-Tools CP-SAT finite capacity scheduling cuts line changeover time by 32% (-25% customer backorders)",
                "Predictive PLC/historian telemetry prevents 48% of unplanned stops (+14.2% productive machine uptime / OEE)",
                "Closed-loop inline SPC vision quality cuts scrap by 44% and speeds batch release from 48 hours to 5 minutes"
            ],
            "kpis": "Schedule Adherence (%) | Overall Equipment Effectiveness (OEE) | Changeover Downtime Hours",
            "personaIds": ["mps_scheduling_lead", "plant_oee_maintenance_mgr", "manufacturing_quality_eng", "bom_change_launch_lead"],
            "agentIds": ["line_schedule_optimizer", "predictive_oee_sentinel", "inline_yield_guardian", "eco_cutover_orchestrator"]
        },
        "inventory_meio": {
            "id": "inventory_meio",
            "vNum": "V4",
            "scorBadge": "VERTICAL 04 · INVENTORY & MEIO",
            "name": "Inventory & Network Optimization / MEIO",
            "fullName": "Vertical 4: Inventory & Network Optimization / MEIO (The Buffers)",
            "tagline": "The Buffers",
            "subtitle": "Multi-echelon safety stock, dynamic STO rebalancing, sub-50ms ATP & cost-to-serve",
            "color": "#06b6d4",
            "watermarkType": "demand_wave",
            "horizon": "Tactical Horizon (Weekly – Monthly)",
            "coreQuestion": "How much buffer stock should be placed at each echelon to guarantee 99%+ fill rate at minimum working capital?",
            "river": "River 3: Cash & Working Capital Flow (DIO Optimization)",
            "systems": "SAP IBP/MM · Blue Yonder MEIO · BigQuery · AlloyDB · Cloud Spanner · Google OR-Tools · Google Maps Distance Matrix",
            "solverSummary": "Coupled Stochastic Multi-Echelon (MEIO) + Dynamic Lateral STO Rebalancing MILP + Sub-50ms AlloyDB/Spanner Real-Time ATP Order Promising + Network Cost-to-Serve Twin",
            "toilMetric": "24% excess buffer cash trapped",
            "toilBullets": [
                "Static single-echelon ERP rules hoard redundant safety stocks upstream while edge regional depots stock out",
                "Manual spreadsheet rebalancing moves stock too late—leaving festival markets dry while sister depots sit on dead inventory",
                "Rigid FIFO order promising splits customer orders across distant depots, inflating secondary freight and late arrivals"
            ],
            "impactMetric": "-18% Working Capital @ 99.4% Fill",
            "impactBullets": [
                "Stochastic Multi-Echelon Inventory Optimization (MEIO) & lateral hub-to-hub rebalancing unlocks $28M+ liquidity",
                "Dynamic Stock Transfer Order (STO) orchestrator prevents regional stockouts with zero manual planner intervention",
                "Margin-aware real-time ATP order promising with Google Maps Distance Matrix cuts split shipments by 34%"
            ],
            "kpis": "Days Inventory Outstanding (DIO) | Inventory Turns | Slow-Moving / Dead Stock (SLOB) %",
            "personaIds": ["meio_inventory_mgr", "atp_fulfillment_spec", "sc_finops_network_architect"],
            "agentIds": ["meio_safety_stock_agent", "atp_order_promising_agent", "network_twin_architect"]
        },
        "warehousing_qa": {
            "id": "warehousing_qa",
            "vNum": "V5",
            "scorBadge": "VERTICAL 05 · WAREHOUSING & QA",
            "name": "Warehousing, Inwarding QA & Intralogistics",
            "fullName": "Vertical 5: Warehousing, Inwarding QA & Intralogistics (The Custodians)",
            "tagline": "The Custodians",
            "subtitle": "Dock-to-stock <4h, inbound AQL quality, 3D Golden-Zone slotting & yard sequencing",
            "color": "#00d2ff",
            "watermarkType": "conveyor_rack",
            "horizon": "Real-Time Daily Execution",
            "coreQuestion": "How do we receive, inspect, putaway, and wave-pick goods inside facilities with zero congestion and <4h dock-to-stock?",
            "river": "Node Custodians along River 1: Physical Material Flow",
            "systems": "Manhattan Active WMS · SAP EWM · Dematic AS/RS WCS · ICML Quality SOP Manuals · Handheld RF Scanners · Yard Management",
            "solverSummary": "3D Spatial Affinity Slotting Twin + Inbound AQL Defect Classifier + Port/Air/Rail Cross-Dock Flow-Through MILP + Dynamic Yard Door Sequencer",
            "toilMetric": "Dock congestion & 34% pick travel waste",
            "toilBullets": [
                "When incoming deliveries breach AQL moisture or defect limits, supervisors waste hours flipping through SOP binders and contracts",
                "Static annual warehouse slotting forces pickers to walk miles through congested aisles for high-velocity SKUs",
                "Uncoordinated trailer yard arrivals cause dock gridlock while cross-dock transloads sit waiting for bay doors"
            ],
            "impactMetric": "-28% Picker Travel & <2.5h Dock-to-Stock",
            "impactBullets": [
                "Automated AQL defect auditing and instant PDF dispute memo generation with contract-backed penalty debit notes",
                "3D Golden-Zone spatial affinity slotting cuts picker travel distance by 28% and boosts storage density by 31%",
                "Autonomous trailer yard and dock door sequencing slashes gate dwell by 41% and speeds cross-dock flow-through"
            ],
            "kpis": "Dock-to-Stock Cycle Time (<4h) | Inbound AQL Defect Rate (%) | Warehouse Pick Accuracy (%)",
            "personaIds": ["warehouse_slotting_lead", "dock_yard_supervisor"],
            "agentIds": ["warehouse_slotting_agent", "yard_dock_sequencer", "crossdock_transfer_orchestrator"]
        },
        "logistics_fleet": {
            "id": "logistics_fleet",
            "vNum": "V6",
            "scorBadge": "VERTICAL 06 · LOGISTICS & FLEET",
            "name": "Logistics, Fleet & Transportation Management",
            "fullName": "Vertical 6: Logistics, Fleet & Transportation Management (The Movers)",
            "tagline": "The Movers",
            "subtitle": "Ocean vessel AIS, air cargo charter/ULD, rail siding free-time & 3D LIFO loading",
            "color": "#ff8c00",
            "watermarkType": "corridor_lifo",
            "horizon": "Real-Time Multi-Modal Daily Execution",
            "coreQuestion": "How do we move freight across ocean vessels, cargo aircraft, intermodal rail rakes, and linehaul trailers at minimum cost and 98%+ OTIF?",
            "river": "Arteries of River 1: Physical Material Flow",
            "systems": "SAP TM · Blue Yonder TMS · Oracle OTM · CargoWise One · Spire AIS · IATA Cargo-XML · Railinc EDI 404 · Indian Railways FOIS · Google Maps Routes API · Google OR-Tools",
            "solverSummary": "End-to-End Multi-Modal Mode-Shift MILP (Factory→Ship→Air→Rail→Truck) + 3D Aircraft ULD & Trailer LIFO Guillotine Bin-Packing + Rail Siding Free-Time & Demurrage Sentinel",
            "toilMetric": "22% multi-modal freight waste & demurrage",
            "toilBullets": [
                "Siloed ocean container booking, panic air freight charters, slow rail handoffs, and unclustered linehaul routes",
                "2D paper load sheets ignore 3D aircraft ULD contours, container cube, highway axle limits, and strict reverse-stop LIFO order",
                "Indian Railways siding demurrage and carrier detention fees leak millions due to unmonitored turnaround timestamps"
            ],
            "impactMetric": "-22.4% Multi-Modal Cost & Zero Demurrage",
            "impactBullets": [
                "End-to-end multi-modal corridor orchestration from Factory Gate to Ocean Ships, Airplanes, Rail Rakes & Road Trucks",
                "3D guillotine bin-packing for 53ft trailers (reverse-stop LIFO), 40ft ocean containers & contoured aircraft ULDs (LD3/PMC)",
                "Continuous railway rake siding turnaround monitoring and automated carrier freight invoice fuel surcharge auditing"
            ],
            "kpis": "Freight Cost per Ton-Km (₹/PTPK) | Truck Cube Fill % | Railway Demurrage & Wharfage (₹)",
            "personaIds": ["global_trade_port_mgr", "air_cargo_charter_lead", "intermodal_rail_linehaul_lead", "network_logistics_lead", "freight_claims_analyst"],
            "agentIds": ["port_drayage_orchestrator", "air_cargo_uld_optimizer", "intermodal_rail_linehaul_agent", "multimodal_mode_shift_agent", "load_consolidation_agent", "freight_control_tower"]
        },
        "trade_mkt_dist": {
            "id": "trade_mkt_dist",
            "vNum": "V7",
            "scorBadge": "VERTICAL 07 · TM&D & LAST-MILE",
            "name": "Trade Marketing & Distribution / TM&D",
            "fullName": "Vertical 7: Trade Marketing & Distribution / TM&D (The Last-Mile Push)",
            "tagline": "The Last-Mile Push",
            "subtitle": "Secondary distribution, FSO beat planning, distributor live stock & planogram audits",
            "color": "#f59e0b",
            "watermarkType": "corridor_lifo",
            "horizon": "Daily Field Execution",
            "coreQuestion": "How do we push inventory through distributors to millions of retail counters, optimize FSO beats, and prevent stockout pitches?",
            "river": "Terminal Interface of River 1 (Retail Shelf) and River 2 (Consumer POS / Sell-Through)",
            "systems": "DMS (Distributor Management Systems) · SFA Mobile Handhelds · Google Maps Platform · Store Visibility Sheets · Quick-Commerce Portals (Blinkit/Zepto)",
            "solverSummary": "Google Maps Routes Preferred CVRPTW Beat Sequencer + Live DMS Inventory Stock-Reconciliation Broker + Planogram Vision Auditor + Secondary Trade Scheme Reconciler",
            "toilMetric": "Field sales pitching out-of-stock SKUs",
            "toilBullets": [
                "Field Sales Officers (FSOs) waste retail counter visits booking orders for SKUs that are currently out of stock at the distributor",
                "Manual store visibility audits rely on unverified photos, allowing retailer planogram violations and unearned scheme payouts",
                "Sub-optimal distributor beat routes cause delayed delivery to high-velocity kirana stores, causing retail stockouts"
            ],
            "impactMetric": "+18% Distributor Case Fill & Zero Lost Visits",
            "impactBullets": [
                "Real-time reconciliation of FSO focus target SKUs with live distributor stock, automatically substituting available variants",
                "Multimodal vision auditing of retail shelf photos verifies planogram compliance and automates scheme discount approvals",
                "Google Maps Fleet Engine beat routing ensures 100% scheduled store coverage and accelerates secondary reorders"
            ],
            "kpis": "Effective Store Coverage % | Distributor Case Fill Rate % | Retail Planogram Compliance %",
            "personaIds": ["fleet_dispatch_mgr"],
            "agentIds": ["fleetflow_dispatch"]
        },
        "reverse_risk_esg": {
            "id": "reverse_risk_esg",
            "vNum": "V8",
            "scorBadge": "VERTICAL 08 · REVERSE & RISK TOWER",
            "name": "Reverse Logistics, Risk Control Tower & ESG",
            "fullName": "Vertical 8: Reverse Logistics, Risk Control Tower & ESG (The Guardians)",
            "tagline": "The Guardians",
            "subtitle": "Retail OTIF chargeback defense, circular RMA backhaul, Scope-3 ESG & macro resilience",
            "color": "#ec4899",
            "watermarkType": "circular_loop",
            "horizon": "Continuous Strategic Horizon",
            "coreQuestion": "How do we recover value from damaged/expired stock, defend against unearned chargebacks, and govern Scope-3 carbon & supply risks?",
            "river": "Circular Loop closing River 1 (Reversals/Recycling) and shielding River 3 (Chargeback Protection)",
            "systems": "SAP Claims & Returns Management · Retail OTIF Portals · Loop RMA · Google Earth Engine · ISO-14083 Carbon Engine · BigQuery Omni · Cloud Spanner · Live Commodity Feeds",
            "solverSummary": "Retail Chargeback Risk Classifier + Vision RMA Backhaul CVRPTW + Google Earth Engine & Maps ISO-14083 Carbon Engine + RCSA Governance Auditor",
            "toilMetric": "3.5% revenue lost to OTIF fines & returns",
            "toilBullets": [
                "Retailer On-Time In-Full (OTIF) penalty deductions and shortage chargebacks are discovered weeks after payment with no easy dispute path",
                "Customer returns ship via costly third-party LTL to central depots while outbound fleet trucks return backhaul empty",
                "Shipment-level Scope-3 carbon accounting (CBAM/EUDR) and enterprise RCSA risk assessments rely on static annual guesswork"
            ],
            "impactMetric": "-78% OTIF Fines & +31% Return Margin",
            "impactBullets": [
                "Predicts retailer OTIF breaches 72 hours early to reallocate stock and auto-generates contract-backed dispute evidence",
                "Multimodal edge RMA grading and Google Maps fleet backhaul insertion boost net return recovery margin by 31%",
                "Automated ISO-14083 compliant shipment-level Scope-3 carbon ledger and continuous supply chain RCSA risk auditing"
            ],
            "kpis": "Return Processing Time | Unearned Claim Leakage % | Scope-3 Carbon Intensity | RCSA Audit Score",
            "personaIds": ["otif_customer_service_lead", "reverse_logistics_mgr", "sc_sustainability_esg_lead"],
            "agentIds": ["reverse_rma_optimizer", "otif_penalty_shield", "carbon_scope3_ledger"]
        }
    }

    cat["departments"] = verticals

    # 3. Update personas' deptId
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
        "meio_inventory_mgr": "inventory_meio",
        "atp_fulfillment_spec": "inventory_meio",
        "sc_finops_network_architect": "inventory_meio",
        "warehouse_slotting_lead": "warehousing_qa",
        "dock_yard_supervisor": "warehousing_qa",
        "global_trade_port_mgr": "logistics_fleet",
        "air_cargo_charter_lead": "logistics_fleet",
        "intermodal_rail_linehaul_lead": "logistics_fleet",
        "network_logistics_lead": "logistics_fleet",
        "freight_claims_analyst": "logistics_fleet",
        "fleet_dispatch_mgr": "trade_mkt_dist",
        "otif_customer_service_lead": "reverse_risk_esg",
        "reverse_logistics_mgr": "reverse_risk_esg",
        "sc_sustainability_esg_lead": "reverse_risk_esg"
    }

    for pid, dept in persona_dept_map.items():
        if pid in cat["personas"]:
            cat["personas"][pid]["deptId"] = dept

    # 4. Update agents' deptId and vertical mappings
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
        "meio_safety_stock_agent": "inventory_meio",
        "atp_order_promising_agent": "inventory_meio",
        "network_twin_architect": "inventory_meio",
        "warehouse_slotting_agent": "warehousing_qa",
        "yard_dock_sequencer": "warehousing_qa",
        "crossdock_transfer_orchestrator": "warehousing_qa",
        "port_drayage_orchestrator": "logistics_fleet",
        "air_cargo_uld_optimizer": "logistics_fleet",
        "intermodal_rail_linehaul_agent": "logistics_fleet",
        "multimodal_mode_shift_agent": "logistics_fleet",
        "load_consolidation_agent": "logistics_fleet",
        "freight_control_tower": "logistics_fleet",
        "fleetflow_dispatch": "trade_mkt_dist",
        "reverse_rma_optimizer": "reverse_risk_esg",
        "otif_penalty_shield": "reverse_risk_esg",
        "carbon_scope3_ledger": "reverse_risk_esg"
    }

    for aid, dept in agent_dept_map.items():
        if aid in cat["agents"]:
            cat["agents"][aid]["deptId"] = dept

    # 5. Update periodicGroups in catalog
    cat["periodicGroups"] = [
        {"id": "universal_csco", "code": "GROUP 0 · CORE", "title": "Universal CSCO Core (4)", "color": "#38bdf8"},
        {"id": "demand_sop", "code": "GROUP I · DEMAND & S&OP", "title": "01 · Demand & S&OP (4)", "color": "#10b981"},
        {"id": "sourcing_procurement", "code": "GROUP II · SOURCING", "title": "02 · Sourcing & Procurement (4)", "color": "#a142f4"},
        {"id": "manufacturing_prod", "code": "GROUP III · MAKE", "title": "03 · Manufacturing & MPS (4)", "color": "#3b82f6"},
        {"id": "inventory_meio", "code": "GROUP IV · INVENTORY", "title": "04 · Inventory & MEIO (3)", "color": "#06b6d4"},
        {"id": "warehousing_qa", "code": "GROUP V · WAREHOUSE", "title": "05 · Warehousing & QA (3)", "color": "#00d2ff"},
        {"id": "logistics_fleet", "code": "GROUP VI · LOGISTICS", "title": "06 · Logistics & Fleet (6)", "color": "#ff8c00"},
        {"id": "trade_mkt_dist", "code": "GROUP VII · TM&D", "title": "07 · TM&D & Last-Mile (1)", "color": "#f59e0b"},
        {"id": "reverse_risk_esg", "code": "GROUP VIII · REVERSE & ESG", "title": "08 · Reverse & Risk Tower (3)", "color": "#ec4899"}
    ]

    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(cat, f, indent=2, ensure_ascii=False)
    print(f"Successfully updated {CATALOG_PATH}")

def update_periodic_elements():
    with open(PERIODIC_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["groups"] = [
        {"id": "universal_csco", "code": "GROUP 0 · CORE", "title": "Universal CSCO Core (4)", "color": "#38bdf8", "glow": "rgba(56,189,248,0.35)"},
        {"id": "demand_sop", "code": "GROUP I · DEMAND & S&OP", "title": "01 · Demand & S&OP (4)", "color": "#10b981", "glow": "rgba(16,185,129,0.35)"},
        {"id": "sourcing_procurement", "code": "GROUP II · SOURCING", "title": "02 · Sourcing & Procurement (4)", "color": "#a142f4", "glow": "rgba(161,66,244,0.35)"},
        {"id": "manufacturing_prod", "code": "GROUP III · MAKE", "title": "03 · Manufacturing & MPS (4)", "color": "#3b82f6", "glow": "rgba(59,130,246,0.35)"},
        {"id": "inventory_meio", "code": "GROUP IV · INVENTORY", "title": "04 · Inventory & MEIO (3)", "color": "#06b6d4", "glow": "rgba(6,182,212,0.35)"},
        {"id": "warehousing_qa", "code": "GROUP V · WAREHOUSE", "title": "05 · Warehousing & QA (3)", "color": "#00d2ff", "glow": "rgba(0,210,255,0.35)"},
        {"id": "logistics_fleet", "code": "GROUP VI · LOGISTICS", "title": "06 · Logistics & Fleet (6)", "color": "#ff8c00", "glow": "rgba(255,140,0,0.35)"},
        {"id": "trade_mkt_dist", "code": "GROUP VII · TM&D", "title": "07 · TM&D & Last-Mile (1)", "color": "#f59e0b", "glow": "rgba(245,158,11,0.35)"},
        {"id": "reverse_risk_esg", "code": "GROUP VIII · REVERSE & ESG", "title": "08 · Reverse & Risk Tower (3)", "color": "#ec4899", "glow": "rgba(236,72,153,0.35)"}
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
        "meio_safety_stock_agent": "inventory_meio",
        "atp_order_promising_agent": "inventory_meio",
        "network_twin_architect": "inventory_meio",
        "warehouse_slotting_agent": "warehousing_qa",
        "yard_dock_sequencer": "warehousing_qa",
        "crossdock_transfer_orchestrator": "warehousing_qa",
        "port_drayage_orchestrator": "logistics_fleet",
        "air_cargo_uld_optimizer": "logistics_fleet",
        "intermodal_rail_linehaul_agent": "logistics_fleet",
        "multimodal_mode_shift_agent": "logistics_fleet",
        "load_consolidation_agent": "logistics_fleet",
        "freight_control_tower": "logistics_fleet",
        "fleetflow_dispatch": "trade_mkt_dist",
        "reverse_rma_optimizer": "reverse_risk_esg",
        "otif_penalty_shield": "reverse_risk_esg",
        "carbon_scope3_ledger": "reverse_risk_esg"
    }

    for el in data["elements"]:
        aid = el.get("agentId")
        if aid in agent_group_map:
            el["group"] = agent_group_map[aid]

    with open(PERIODIC_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Successfully updated {PERIODIC_PATH}")

if __name__ == "__main__":
    update_catalog()
    update_periodic_elements()

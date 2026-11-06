# Supply Chain High-Code ADK Agents Library

This directory houses the executable, high-code **Google Agent Development Kit (ADK)** implementations for all **60 High-ROI Supply Chain AI Agents** across the **6 ASCM SCOR Pillars** and **20 Sub-Pillars**.

Every agent directory (`agents/<agent_id>/`) is fully equipped with:
- **Dedicated Executive README**: Business problem, autonomous solution, technical architecture, connected BigQuery data lake, and 1-command deployment instructions.
- **Interactive HTML Cockpit**: Domain-tailored A2UI canvas dashboard (`app/render/interactive_html.py`) with zero CDN dependencies.
- **Deterministic Solvers & Tools**: High-code tools (`app/tools.py`) connecting to ERP, WMS, TMS, and OR-Tools solvers.
- **Realistic Data Fixtures**: Ground-truth JSON datasets (`fixtures/tables/*.json`) mirrored to BigQuery `zuhaibp-ai:supply_chain_twin`.
- **Smoke Tests**: Automated pytest suites (`tests/test_smoke.py`) validating tool execution and safety guardrails.

---

## 🏛️ Agent Portfolio by SCOR Pillar

## Pillar 01: Planning & Strategy (📡 39 Agents)

### [`Demand Sensing Agent`](./demand_sensing_agent/README.md)
- **Sub-Pillar**: `Demand Forecasting`
- **Target Persona**: Demand Planner / Forecaster
- **Value Metric**: `-20%–35% Short-Term WAPE`
- **Overview**: Synthesizes POS velocity, weather anomalies, and macro trends.
- **Systems**: Supply Planning System · Enterprise ERP (MCP / On-Prem DB) · BigQuery ML · Time-Series Forecasting Model · Weather & Climate Ensemble Feed (MCP / API) · Geospatial & Location Intelligence API · EDI 852 POS · Supply Planning Platform (MCP / API)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent demand_sensing_agent`

### [`Forecast Reconciliation`](./cpfr_sync_agent/README.md)
- **Sub-Pillar**: `Demand Forecasting`
- **Target Persona**: Commercial Planning Lead
- **Value Metric**: `-40%–55% CPFR Variance`
- **Overview**: Identifies unmodeled drivers across eCommerce and retail channels.
- **Systems**: EDI 852 / 830 / 855 · Retail Customer POS & e-Commerce Portals (EDI / MCP) · BigQuery · Cloud Dataflow · Geospatial & Location Intelligence API · Supply Planning System (MCP / API)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent cpfr_sync_agent`

### [`NPI Demand Profiler`](./npi_demand_profiler/README.md)
- **Sub-Pillar**: `Demand Forecasting`
- **Target Persona**: Brand & Innovation Manager
- **Value Metric**: `-30% Launch Forecast Error`
- **Overview**: Matches launch packaging and attributes to historical lookalikes.
- **Systems**: Supply Planning System · Enterprise ERP (MCP / On-Prem DB) · BigQuery ML · Time-Series Forecasting Model · Weather & Climate Ensemble Feed (MCP / API) · Geospatial & Location Intelligence API · EDI 852 POS · Supply Planning Platform (MCP / API)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent npi_demand_profiler`

### [`Promo ROI Simulator`](./promo_lift_simulator/README.md)
- **Sub-Pillar**: `Trade Promotion`
- **Target Persona**: Trade Marketing Manager
- **Value Metric**: `+15%–25% Promo Net ROI`
- **Overview**: Simulates price elasticity, shelf lift, and incremental spend return.
- **Systems**: Trade Promotion Management (TPM / CRM) · Commercial CRM & Trade Portal (MCP / API) · Supply Planning System (MCP / API) · BigQuery ML · Time-Series Forecasting Model · Operational SQL & Vector DB (On-Prem / Cloud) · Geospatial & Location Intelligence API
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent promo_lift_simulator`

### [`JBP Negotiation Agent`](./field_beat_distributor_sync_agent/README.md)
- **Sub-Pillar**: `Trade Promotion`
- **Target Persona**: Key Account Manager (KAM)
- **Value Metric**: `+2–4 pts JBP Margin`
- **Overview**: Creates customized sell-in story decks and joint promotional calendars.
- **Systems**: DMS (Distributor Management Systems) · SFA Mobile Handhelds · Geospatial Routing & Traffic Telemetry API · ERP Order Management (SD / MCP) · BigQuery · Operational SQL & Vector DB (On-Prem / Cloud)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent field_beat_distributor_sync_agent`

### [`Deduction Audit Agent`](./trade_scheme_claims_reconciler/README.md)
- **Sub-Pillar**: `Trade Promotion`
- **Target Persona**: Revenue / Trade Finance Lead
- **Value Metric**: `Recovers 1.5%–3% Trade Spend`
- **Overview**: Audits scanned proof-of-performance circulars and invoices via OCR.
- **Systems**: ERP Order & Finance Ledger (MCP / On-Prem DB) · Distributor DMS Portals · Secondary Sales Ledgers in BigQuery, On-Prem SQL & Vector DB · Enterprise API & MCP Gateways · Document AI
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent trade_scheme_claims_reconciler`

### [`Consensus & Gap Agent`](./sop_scenario_weaver/README.md)
- **Sub-Pillar**: `S&OP / IBP`
- **Target Persona**: S&OP / Supply Planning Dir.
- **Value Metric**: `+1.5–3 pts EBITDA Protection`
- **Overview**: Reconciles unconstrained demand with factory plant bottleneck limits.
- **Systems**: Production Planning & ERP (MCP / On-Prem DB) · Supply Planning System (MCP / API) · Concurrent Supply Planning Platform (MCP / API) · BigQuery · Multi-Hop Graph Database (Cloud / On-Prem) · Mathematical Optimization Solver (MILP / CP-SAT) · Enterprise FP&A & Financial Planning (MCP / API)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent sop_scenario_weaver`

### [`Digital War-Room Agent`](./disruption_war_room_orchestrator/README.md)
- **Sub-Pillar**: `S&OP / IBP`
- **Target Persona**: Supply Chain VP / COO
- **Value Metric**: `Protects 97%+ Strategic OTIF`
- **Overview**: Evaluates co-packer shifts and allocation trade-offs during supply outages.
- **Systems**: Weather & Climate Ensemble Feed (MCP / API) · Satellite & Geospatial Remote Sensing API · Geospatial Routing & ETA Telemetry API · BigQuery GIS · Multi-Hop Graph Database (Cloud / On-Prem) · Ocean Vessel AIS Telemetry (MCP / API) · Air Cargo Flight Telemetry (MCP / API) · Real-Time Carrier Visibility (MCP / API) · Enterprise ERP & Supply Planning (MCP / On-Prem / API) · Transportation Management System (TMS / API)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent disruption_war_room_orchestrator`

### [`Executive Copilot`](./csco_control_tower_copilot/README.md)
- **Sub-Pillar**: `S&OP / IBP`
- **Target Persona**: IBP Lead / Chief Planning Off.
- **Value Metric**: `-85% Executive Latency`
- **Overview**: Generates pre-read decks and tracks sign-offs across cross-functional leads.
- **Systems**: Gemini Enterprise · BigQuery Supply Chain Twin · Multi-Hop Graph Database (Cloud / On-Prem) · Operational SQL & Vector DB (On-Prem / Cloud) · Looker Semantic Layer · Geospatial Routing & ETA Telemetry API · Enterprise ERP (MCP / On-Prem DB) & IBP · Manhattan WMS · Transportation Management System (TMS / API) · CargoWise
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent csco_control_tower_copilot`

### [`SKU Pruning Agent`](./working_capital_cash_bridge/README.md)
- **Sub-Pillar**: `Portfolio & SKU`
- **Target Persona**: Category Manager
- **Value Metric**: `Frees 12%–20% Tail Capital`
- **Overview**: Scores velocity, plant changeover cost, and shelf revenue yield.
- **Systems**: Enterprise ERP (MCP / On-Prem DB) Finance (ACDOCA) · Supply Planning System (MCP / API) · BigQuery Cortex · Operational SQL & Vector DB (On-Prem / Cloud) · Low-Latency Transactional State DB · Enterprise FP&A & Financial Planning (MCP / API) · Looker · Enterprise API & MCP Gateway
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent working_capital_cash_bridge`

### [`PIPO Run-Out Agent`](./eco_cutover_orchestrator/README.md)
- **Sub-Pillar**: `Portfolio & SKU`
- **Target Persona**: Lifecycle / Materials Mgr
- **Value Metric**: `-60%–80% Obsolescence Scrap`
- **Overview**: Orchestrates transition buffers to sync packaging and formulation cuts.
- **Systems**: Siemens Teamcenter / PTC Windchill PLM · Enterprise ERP (MCP / On-Prem DB) BOM (CC02) · e-Procurement & Sourcing Portal (MCP / API) · Siemens MES · Multi-Hop Graph Database (Cloud / On-Prem) · Mathematical Optimization Solver (MILP / CP-SAT) · BigQuery
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent eco_cutover_orchestrator`

### [`Cost-to-Serve Diagnostic`](./network_twin_architect/README.md)
- **Sub-Pillar**: `Portfolio & SKU`
- **Target Persona**: Commercial Finance Director
- **Value Metric**: `-6%–11% Network Cost-to-Serve`
- **Overview**: Calculates net-net margin across Club, Grocery, and eCommerce packs.
- **Systems**: BigQuery Supply Chain Twin · Multi-Hop Graph Database (Cloud / On-Prem) · Google Maps Distance Matrix · Mathematical Optimization Solver (MILP / CP-SAT) · Enterprise ERP (MCP / On-Prem DB) CO-PA · Manhattan WMS · Transportation Management System (TMS / API) · Looker
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent network_twin_architect`

### [`Disruption Sensing Agent`](./tier_n_risk_sentinel/README.md)
- **Sub-Pillar**: `Supplier Network`
- **Target Persona**: Procurement Dir. / Risk Mgr
- **Value Metric**: `-55% Disruption Downtime`
- **Overview**: Monitors multi-tier supply feeds, port delays, and vendor financials.
- **Systems**: Multi-Hop Graph Database (Cloud / On-Prem) · BigQuery GIS · Weather & Climate Ensemble Feed (MCP / API) · Geospatial & Location Intelligence API · Resilinc / Everstream · Customs BOL Graph · Enterprise ERP (MCP / On-Prem DB) BOM · e-Procurement & Sourcing Portal (MCP / API)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent tier_n_risk_sentinel`

### [`Onboarding & Qual. Agent`](./supplier_quality_sentinel/README.md)
- **Sub-Pillar**: `Supplier Network`
- **Target Persona**: Procurement Operations Lead
- **Value Metric**: `-80% Onboarding Cycle Time`
- **Overview**: Parses BRC/ISO audits, food-safety filings, and tax registrations.
- **Systems**: Enterprise ERP (MCP / On-Prem DB) QM · TrackWise / Veeva QMS · Siemens Teamcenter CAD PMI · Document AI · Gemini 3.1 Pro Vision · BigQuery ML · Operational SQL & Vector DB (On-Prem / Cloud)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent supplier_quality_sentinel`

### [`ESG & Scope 3 Auditor`](./carbon_scope3_ledger/README.md)
- **Sub-Pillar**: `Supplier Network`
- **Target Persona**: Chief Sustainability Officer
- **Value Metric**: `100% Audit-Ready Scope 3`
- **Overview**: Standardizes chain-of-custody certificates (RSPO/FSC) and packaging LCAs.
- **Systems**: Satellite & Geospatial Remote Sensing API · Geospatial Routing & Traffic API · BigQuery GIS · Low-Latency Transactional State DB · SAP EHS & GTS · Transportation Management System (TMS / API) · CargoWise · ISO-14083 / GLEC Engine
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent carbon_scope3_ledger`

### [`Commodity Index Advisor`](./commodity_index_advisor/README.md)
- **Sub-Pillar**: `Material & Packaging`
- **Target Persona**: Category Sourcing Mgr (Direct)
- **Value Metric**: `-4%–8% Direct Material Spend`
- **Overview**: Correlates CBOT/Platts feedstocks with depletion to advise hedging.
- **Systems**: e-Procurement & Supplier Portals (MCP / REST API) · Enterprise ERP (MCP / On-Prem DB) MM · Siemens Teamcenter PLM · Document AI · BigQuery · Vector Search & Semantic Index (DB / MCP) · Mathematical Optimization Solver (MILP / CP-SAT) · LME/ICIS Feeds
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent commodity_index_advisor`

### [`Dynamic Should-Cost Agent`](./rfq_should_cost_agent/README.md)
- **Sub-Pillar**: `Material & Packaging`
- **Target Persona**: Strategic Sourcing Lead
- **Value Metric**: `5%–10% RFP Spend Savings`
- **Overview**: Deconstructs packaging specs (resin weight, corrugate, conversion energy).
- **Systems**: e-Procurement & Supplier Portals (MCP / REST API) · Enterprise ERP (MCP / On-Prem DB) MM · Siemens Teamcenter PLM · Document AI · BigQuery · Vector Search & Semantic Index (DB / MCP) · Mathematical Optimization Solver (MILP / CP-SAT) · LME/ICIS Feeds
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent rfq_should_cost_agent`

### [`Sustainable Packaging Agent`](./sustainable_packaging_agent/README.md)
- **Sub-Pillar**: `Material & Packaging`
- **Target Persona**: Packaging R&D Engineer
- **Value Metric**: `-15%–25% EPR & Spec Cost`
- **Overview**: Evaluates PCR resins and barrier materials against line runnability & taxes.
- **Systems**: Satellite & Geospatial Remote Sensing API · Geospatial Routing & Traffic API · BigQuery GIS · Low-Latency Transactional State DB · SAP EHS & GTS · Transportation Management System (TMS / API) · CargoWise · ISO-14083 / GLEC Engine
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent sustainable_packaging_agent`

### [`Contract Leakage Agent`](./tariff_esg_agent/README.md)
- **Sub-Pillar**: `Contract & PO Mgmt`
- **Target Persona**: Commercial Sourcing / Legal
- **Value Metric**: `Recovers 2%–4% Addressable Spend`
- **Overview**: Reconciles live spend against negotiated rebate tiers and volume discount scales.
- **Systems**: Global Trade & Tariff System (MCP / API) · e-Procurement & Sourcing Portal (MCP / API) CLM · Icertis · Document AI · Vector Search & Semantic Index (DB / MCP) · BigQuery · Satellite & Geospatial Remote Sensing API · USITC / EU TARIC Schedules
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent tariff_esg_agent`

### [`PO Expediting Agent`](./master_data_leadtime_steward/README.md)
- **Sub-Pillar**: `Contract & PO Mgmt`
- **Target Persona**: Buyer / Procurement Coord.
- **Value Metric**: `-35%–50% Expedite Freight`
- **Overview**: Monitors EDI 855/856 delay feeds and orchestrates supplier split-shipments.
- **Systems**: Enterprise ERP (MCP / On-Prem DB) MM/PP/SD · SAP MDG · BigQuery ML · Operational SQL & Vector DB (On-Prem / Cloud) · Low-Latency Transactional State DB · CubiScan 3D Dimensioners · Manhattan WMS · Transportation Management System (TMS / API) · Enterprise API & MCP Gateway
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent master_data_leadtime_steward`

### [`Three-Way Match Dispute`](./three_way_match_dispute/README.md)
- **Sub-Pillar**: `Contract & PO Mgmt`
- **Target Persona**: Accounts Payable Lead
- **Value Metric**: `-80% Invoice Exception Cost`
- **Overview**: Diagnoses price/quantity discrepancies across POs, GRNs, and carrier invoices.
- **Systems**: Global Trade & Tariff System (MCP / API) · e-Procurement & Sourcing Portal (MCP / API) CLM · Icertis · Document AI · Vector Search & Semantic Index (DB / MCP) · BigQuery · Satellite & Geospatial Remote Sensing API · USITC / EU TARIC Schedules
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent three_way_match_dispute`

### [`Changeover Optimizer`](./finite_production_scheduler/README.md)
- **Sub-Pillar**: `Production Scheduling`
- **Target Persona**: Master Production Scheduler
- **Value Metric**: `+4–7 pts Line OEE Lift`
- **Overview**: Sequences allergen, kosher, and packaging runs to minimize washdowns.
- **Systems**: Production Planning & ERP (MCP / On-Prem DB) · Siemens Opcenter MES · Rockwell FactoryTalk · Supply Planning Platform (MCP / API) · Constraint Programming Solver (CP-SAT) · Low-Latency Transactional State DB · Operational SQL & Vector DB (On-Prem / Cloud) · BigQuery
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent finite_production_scheduler`

### [`Disruption Re-sequencer`](./line_schedule_optimizer/README.md)
- **Sub-Pillar**: `Production Scheduling`
- **Target Persona**: Shop Floor / Shift Lead
- **Value Metric**: `-40% Disruption Output Loss`
- **Overview**: Detects machine halts and re-routes perishable WIP to alternate lines.
- **Systems**: Production Planning & ERP (MCP / On-Prem DB) · Siemens Opcenter MES · Rockwell FactoryTalk · Supply Planning Platform (MCP / API) · Constraint Programming Solver (CP-SAT) · Low-Latency Transactional State DB · Operational SQL & Vector DB (On-Prem / Cloud) · BigQuery
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent line_schedule_optimizer`

### [`Labor & Line Balancing`](./labor_line_balancing_agent/README.md)
- **Sub-Pillar**: `Production Scheduling`
- **Target Persona**: Plant Operations Manager
- **Value Metric**: `+8%–12% Direct Labor Output`
- **Overview**: Maps shift skill certifications and fatigue constraints to line speeds.
- **Systems**: Production Planning & ERP (MCP / On-Prem DB) · Siemens Opcenter MES · Rockwell FactoryTalk · Supply Planning Platform (MCP / API) · Constraint Programming Solver (CP-SAT) · Low-Latency Transactional State DB · Operational SQL & Vector DB (On-Prem / Cloud) · BigQuery
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent labor_line_balancing_agent`

### [`Bottleneck Diagnostic`](./predictive_oee_sentinel/README.md)
- **Sub-Pillar**: `Capacity Planning`
- **Target Persona**: Supply Chain Ops Director
- **Value Metric**: `-30%–45% Unplanned Stops`
- **Overview**: Assesses CIP utilities, boiler loads, and cold storage holding limits.
- **Systems**: Plant Process Historian (OPC-UA / On-Prem) / AVEVA Historian · Siemens / Allen-Bradley PLC · Enterprise ERP (MCP / On-Prem DB) PM & MM · Cloud Pub/Sub & Dataflow · BigQuery ML · Vertex AI · Mathematical Optimization Solver (MILP / CP-SAT)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent predictive_oee_sentinel`

### [`Co-Packer Allocation`](./copacker_allocation_agent/README.md)
- **Sub-Pillar**: `Capacity Planning`
- **Target Persona**: External Sourcing / CMO Lead
- **Value Metric**: `-8%–14% External Tolling Cost`
- **Overview**: Models internal conversion costs against co-packer tolling agreements.
- **Systems**: Production Planning & ERP (MCP / On-Prem DB) · Supply Planning System (MCP / API) · Concurrent Supply Planning Platform (MCP / API) · BigQuery · Multi-Hop Graph Database (Cloud / On-Prem) · Mathematical Optimization Solver (MILP / CP-SAT) · Enterprise FP&A & Financial Planning (MCP / API)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent copacker_allocation_agent`

### [`CapEx Simulator`](./capex_simulator_agent/README.md)
- **Sub-Pillar**: `Capacity Planning`
- **Target Persona**: VP Manufacturing Engineering
- **Value Metric**: `Avoids 15%–25% Idle CapEx`
- **Overview**: Simulates multi-year volume trends to test high-speed line expansions.
- **Systems**: BigQuery Supply Chain Twin · Multi-Hop Graph Database (Cloud / On-Prem) · Google Maps Distance Matrix · Mathematical Optimization Solver (MILP / CP-SAT) · Enterprise ERP (MCP / On-Prem DB) CO-PA · Manhattan WMS · Transportation Management System (TMS / API) · Looker
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent capex_simulator_agent`

### [`Visual Defect Triager`](./inline_yield_guardian/README.md)
- **Sub-Pillar**: `Quality & Compliance`
- **Target Persona**: QA Manager / Line Inspector
- **Value Metric**: `-35%–50% Quality Scrap`
- **Overview**: Inspects high-speed video frames for crimped seals, lot codes, and labels.
- **Systems**: Industrial Line Vision Cameras (RTSP / Edge) Inline Vision · Siemens PLC SCADA · Enterprise ERP (MCP / On-Prem DB) QM · Siemens Opcenter eBHR · Vertex AI Vision · BigQuery ML · Operational SQL & Vector DB (On-Prem / Cloud)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent inline_yield_guardian`

### [`Batch Record Auditor`](./batch_record_auditor/README.md)
- **Sub-Pillar**: `Quality & Compliance`
- **Target Persona**: Regulatory Compliance Lead
- **Value Metric**: `-70% Batch Release Lead Time`
- **Overview**: Parses BPR and COA documents to flag pasteurization & CCP deviations.
- **Systems**: Industrial Line Vision Cameras (RTSP / Edge) Inline Vision · Siemens PLC SCADA · Enterprise ERP (MCP / On-Prem DB) QM · Siemens Opcenter eBHR · Vertex AI Vision · BigQuery ML · Operational SQL & Vector DB (On-Prem / Cloud)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent batch_record_auditor`

### [`RCA & CAPA Copilot`](./scrap_defect_root_cause_agent/README.md)
- **Sub-Pillar**: `Quality & Compliance`
- **Target Persona**: Continuous Improvement Lead
- **Value Metric**: `-40%–55% Repeat Quality Loss`
- **Overview**: Correlates consumer complaints with ingredient lots and machine telemetry.
- **Systems**: Industrial Line Vision Cameras (RTSP / Edge) Inline Vision · Siemens PLC SCADA · Enterprise ERP (MCP / On-Prem DB) QM · Siemens Opcenter eBHR · Vertex AI Vision · BigQuery ML · Operational SQL & Vector DB (On-Prem / Cloud)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent scrap_defect_root_cause_agent`

### [`Return Fraud Sentinel`](./reverse_rma_optimizer/README.md)
- **Sub-Pillar**: `Returns & Claims Mgmt`
- **Target Persona**: Reverse Logistics / Fraud Lead
- **Value Metric**: `-25%–40% Return Fraud Loss`
- **Overview**: Analyzes item photos and packaging video feeds to detect wear or swapped tags.
- **Systems**: Loop / Narvar RMA · Transportation Management System (TMS / API) · Enterprise ERP (MCP / On-Prem DB) QM & EWM · Gemini 3.8 Flash Vision · Geospatial Routing & Traffic API · Mathematical Optimization Solver (MILP / CP-SAT) · Operational SQL & Vector DB (On-Prem / Cloud)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent reverse_rma_optimizer`

### [`Keep-It & Routing Advisor`](./keep_it_routing_advisor/README.md)
- **Sub-Pillar**: `Returns & Claims Mgmt`
- **Target Persona**: Customer Experience (CX) Lead
- **Value Metric**: `+15%–22% Net Return Margin`
- **Overview**: Evaluates salvage margins vs reverse freight to determine keep-it instant refunds.
- **Systems**: Loop / Narvar RMA · Transportation Management System (TMS / API) · Enterprise ERP (MCP / On-Prem DB) QM & EWM · Gemini 3.8 Flash Vision · Geospatial Routing & Traffic API · Mathematical Optimization Solver (MILP / CP-SAT) · Operational SQL & Vector DB (On-Prem / Cloud)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent keep_it_routing_advisor`

### [`OS&D Freight Claims`](./osd_freight_claims_agent/README.md)
- **Sub-Pillar**: `Returns & Claims Mgmt`
- **Target Persona**: Claims Specialist / Controller
- **Value Metric**: `2x Faster OS&D Cash Recovery`
- **Overview**: Reconciles eBOLs, dock damage logs, and carrier contracts to auto-file disputes.
- **Systems**: Retail Customer POS Portal (EDI / MCP) / Target / DMart (Avenue Supermarts) OTIF Portals · Enterprise ERP (MCP / On-Prem DB) SD & FI-AR · Real-Time Carrier Visibility (MCP / API) GPS · Google Maps Geofencing · Document AI · BigQuery · Operational SQL & Vector DB (On-Prem / Cloud)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent osd_freight_claims_agent`

### [`Dynamic Markdown Agent`](./dynamic_markdown_agent/README.md)
- **Sub-Pillar**: `Expiry & Markdowns`
- **Target Persona**: Merchandising / Store Ops Mgr
- **Value Metric**: `-22%–35% Expiry Shrink`
- **Overview**: Correlates days-to-expiry (DTE) with sales velocity to trigger ESL shelf price cuts.
- **Systems**: Trade Promotion Management (TPM / CRM) · Commercial CRM & Trade Portal (MCP / API) · Supply Planning System (MCP / API) · BigQuery ML · Time-Series Forecasting Model · Operational SQL & Vector DB (On-Prem / Cloud) · Geospatial & Location Intelligence API
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent dynamic_markdown_agent`

### [`Short-Dated Redistributor`](./short_dated_redistributor/README.md)
- **Sub-Pillar**: `Expiry & Markdowns`
- **Target Persona**: Inventory Disposition Lead
- **Value Metric**: `Diverts 30%–45% At-Risk Lots`
- **Overview**: Matches near-date DC lots with discounters or food banks before acceptance cutoffs.
- **Systems**: Warehouse Management System (WMS / MCP) · Warehouse Management System (WMS / On-Prem / API) · Transportation Management System (TMS / API) · Low-Latency Transactional State DB · Operational SQL & Vector DB (On-Prem / Cloud) · Mathematical Optimization Solver (MILP / CP-SAT) · Geospatial Routing & Traffic API · Dematic WCS
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent short_dated_redistributor`

### [`Food Waste & ESG Copilot`](./food_waste_esg_copilot/README.md)
- **Sub-Pillar**: `Expiry & Markdowns`
- **Target Persona**: Chief Sustainability Officer
- **Value Metric**: `-75% ESG Reporting Cost`
- **Overview**: Aggregates store shrink and organic haul logs to generate audited GHG diversion filings.
- **Systems**: Satellite & Geospatial Remote Sensing API · Geospatial Routing & Traffic API · BigQuery GIS · Low-Latency Transactional State DB · SAP EHS & GTS · Transportation Management System (TMS / API) · CargoWise · ISO-14083 / GLEC Engine
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent food_waste_esg_copilot`

### [`RTI Balance Reconciler`](./rti_balance_reconciler/README.md)
- **Sub-Pillar**: `Pallet & Tote Reclamation`
- **Target Persona**: Asset Recovery / RTI Manager
- **Value Metric**: `-25%–35% RTI Replacement Cost`
- **Overview**: Reconciles RFID portal scans with CHEP/PECO statements to detect hoarding nodes.
- **Systems**: Enterprise ERP (MCP / On-Prem DB) MM/PP/SD · SAP MDG · BigQuery ML · Operational SQL & Vector DB (On-Prem / Cloud) · Low-Latency Transactional State DB · CubiScan 3D Dimensioners · Manhattan WMS · Transportation Management System (TMS / API) · Enterprise API & MCP Gateway
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent rti_balance_reconciler`

### [`Milk-Run Consolidation`](./intermodal_rail_linehaul_agent/README.md)
- **Sub-Pillar**: `Pallet & Tote Reclamation`
- **Target Persona**: Reverse Transport Planner
- **Value Metric**: `-20%–30% Reverse Haul Cost`
- **Overview**: Schedules dynamic backhauls to collect empty roll cages and RPCs from retail stores.
- **Systems**: Railinc EDI 404 / 417 / 322 · Class-I Rail Portals (BNSF/UP/CSX/NS/CN) · Transportation Management System (TMS / API) · Transportation Management System (TMS / MCP) · Fleet & Yard Geofencing Telemetry API · Mathematical Optimization Solver (MILP / CP-SAT) · BigQuery GIS · Operational SQL & Vector DB (On-Prem / Cloud)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent intermodal_rail_linehaul_agent`

### [`Sanitation & Health Agent`](./sanitation_health_agent/README.md)
- **Sub-Pillar**: `Pallet & Tote Reclamation`
- **Target Persona**: Packaging QA / Food Safety
- **Value Metric**: `Zero Sanitation Recall Breaches`
- **Overview**: Inspects return photos and wash logs for structural fatigue and chemical compliance.
- **Systems**: Industrial Line Vision Cameras (RTSP / Edge) Inline Vision · Siemens PLC SCADA · Enterprise ERP (MCP / On-Prem DB) QM · Siemens Opcenter eBHR · Vertex AI Vision · BigQuery ML · Operational SQL & Vector DB (On-Prem / Cloud)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent sanitation_health_agent`


## Pillar 02: Sourcing & Procurement (🛡️ 0 Agents)



## Pillar 03: Manufacturing & Production (⚙️ 0 Agents)



## Pillar 04: Inventory & Warehousing (📦 9 Agents)

### [`Safety Stock Agent`](./meio_safety_stock_agent/README.md)
- **Sub-Pillar**: `Positioning & Optimization`
- **Target Persona**: Inventory Optimization Lead
- **Value Metric**: `-12%–22% Safety Stock Capital`
- **Overview**: Recalibrates multi-echelon buffers using live lead-time and demand variance.
- **Systems**: Enterprise ERP (MCP / On-Prem DB) MM · Supply Planning System (MCP / API) Inventory · Supply Planning Platform (MCP / API) · Warehouse Management System (WMS / On-Prem / API) · BigQuery Twin · Multi-Hop Graph Database (Cloud / On-Prem) · Mathematical Optimization Solver (MILP / CP-SAT) · Google Maps Distance Matrix
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent meio_safety_stock_agent`

### [`SLOB Disposition Agent`](./slob_disposition_agent/README.md)
- **Sub-Pillar**: `Positioning & Optimization`
- **Target Persona**: Inventory Controller / Buyer
- **Value Metric**: `+25%–40% Aged Stock Recovery`
- **Overview**: Analyzes shelf-life risk and triggers promotional bundles or liquidations.
- **Systems**: Enterprise ERP (MCP / On-Prem DB) MM · Supply Planning System (MCP / API) Inventory · Supply Planning Platform (MCP / API) · Warehouse Management System (WMS / On-Prem / API) · BigQuery Twin · Multi-Hop Graph Database (Cloud / On-Prem) · Mathematical Optimization Solver (MILP / CP-SAT) · Google Maps Distance Matrix
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent slob_disposition_agent`

### [`Inter-Facility Rebalancer`](./crossdock_transfer_orchestrator/README.md)
- **Sub-Pillar**: `Positioning & Optimization`
- **Target Persona**: Replenishment Planner
- **Value Metric**: `-35%–50% Lost-Sale Stockouts`
- **Overview**: Generates automated inter-DC and store transfers to balance localized gluts.
- **Systems**: Warehouse Management System (WMS / MCP) · Warehouse Management System (WMS / On-Prem / API) · Transportation Management System (TMS / API) · Low-Latency Transactional State DB · Operational SQL & Vector DB (On-Prem / Cloud) · Mathematical Optimization Solver (MILP / CP-SAT) · Geospatial Routing & Traffic API · Dematic WCS
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent crossdock_transfer_orchestrator`

### [`Dynamic Slotting Agent`](./warehouse_slotting_agent/README.md)
- **Sub-Pillar**: `Warehouse Operations`
- **Target Persona**: DC Operations Mgr / IE Lead
- **Value Metric**: `-15%–28% Picker Travel Time`
- **Overview**: Evaluates co-pick affinity matrices to recommend fast-pick zone re-slotting.
- **Systems**: Warehouse Management System (WMS / On-Prem / API) · Warehouse Management System (WMS / API) · Warehouse Management System (WMS / MCP) · Dematic / Knapp WCS · Operational SQL & Vector DB (On-Prem / Cloud) · BigQuery · Mathematical Optimization Solver (MILP / CP-SAT) · RF / AMR Telemetry
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent warehouse_slotting_agent`

### [`Dock-to-Stock Agent`](./dock_to_stock_agent/README.md)
- **Sub-Pillar**: `Warehouse Operations`
- **Target Persona**: Inbound Receiving Supervisor
- **Value Metric**: `-75% Dock-to-Stock Latency`
- **Overview**: Parses scanned BOLs and pallet photos to reconcile open ASN variances.
- **Systems**: Carrier Transit Telemetry (MCP / API) / Real-Time Carrier Visibility (MCP / API) Yard · Manhattan YMS · Warehouse Management System (WMS / MCP) · Fleet & Yard Geofencing Telemetry API & Geofencing · Vertex AI Vision ANPR · Operational SQL & Vector DB (On-Prem / Cloud) · Mathematical Optimization Solver (MILP / CP-SAT)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent dock_to_stock_agent`

### [`Wave Fulfillment Copilot`](./wave_fulfillment_copilot/README.md)
- **Sub-Pillar**: `Warehouse Operations`
- **Target Persona**: DC Shift Floor Lead
- **Value Metric**: `-30% DC Rush Overtime`
- **Overview**: Balances picker lines dynamically to protect carrier pickup cutoff times.
- **Systems**: Warehouse Management System (WMS / On-Prem / API) · Warehouse Management System (WMS / API) · Warehouse Management System (WMS / MCP) · Dematic / Knapp WCS · Operational SQL & Vector DB (On-Prem / Cloud) · BigQuery · Mathematical Optimization Solver (MILP / CP-SAT) · RF / AMR Telemetry
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent wave_fulfillment_copilot`

### [`Phantom Inventory Sensor`](./planogram_merchandising_vision_auditor/README.md)
- **Sub-Pillar**: `Omnichannel Visibility`
- **Target Persona**: Store Operations / Omni Lead
- **Value Metric**: `+2.5%–4% On-Shelf Sales Lift`
- **Overview**: Identifies shrinkage anomalies when on-hand stock stops scanning at POS.
- **Systems**: SFA Camera Uploads · Cloud Storage · Gemini 3.8 Flash Multimodal Vision · BigQuery · Planogram Master Repositories · Vector Search & Semantic Index (DB / MCP)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent planogram_merchandising_vision_auditor`

### [`SFS / BOPIS Sourcing`](./atp_order_promising_agent/README.md)
- **Sub-Pillar**: `Omnichannel Visibility`
- **Target Persona**: Omnichannel Fulfillment Dir.
- **Value Metric**: `-15%–25% Parcel & Split Cost`
- **Overview**: Selects lowest-cost fulfillment nodes based on store labor and parcel zones.
- **Systems**: Enterprise ERP (MCP / On-Prem DB) aATP · IBM Sterling OMS · Manhattan Active Omni · Low-Latency Transactional State DB · Operational SQL & Vector DB (On-Prem / Cloud) · Google Maps Routes & Distance Matrix · Mathematical Optimization Solver (MILP / CP-SAT)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent atp_order_promising_agent`

### [`Returns Triage Agent`](./returns_triage_agent/README.md)
- **Sub-Pillar**: `Omnichannel Visibility`
- **Target Persona**: Reverse Logistics Lead
- **Value Metric**: `+18%–30% Full-Price Recovery`
- **Overview**: Evaluates item condition scans to triage restock, vendor return, or liquidation.
- **Systems**: Loop / Narvar RMA · Transportation Management System (TMS / API) · Enterprise ERP (MCP / On-Prem DB) QM & EWM · Gemini 3.8 Flash Vision · Geospatial Routing & Traffic API · Mathematical Optimization Solver (MILP / CP-SAT) · Operational SQL & Vector DB (On-Prem / Cloud)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent returns_triage_agent`


## Pillar 05: Logistics & Transportation (🚚 12 Agents)

### [`Load Consolidation`](./load_consolidation_agent/README.md)
- **Sub-Pillar**: `First & Mid-Mile`
- **Target Persona**: Transport Planner / Inbound Mgr
- **Value Metric**: `+12%–18% Cube · -10% Trucks`
- **Overview**: Consolidates vendor LTLs into multi-stop FTL linehauls via cube & weight modeling.
- **Systems**: Warehouse Management System (WMS / MCP) / TM · Manhattan WMS Cartonization · Mathematical Optimization Solver (MILP / CP-SAT) 3D Bin Packing · Operational SQL & Vector DB (On-Prem / Cloud) · Cloud Run 3D Load Studio · Weighbridge IoT
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent load_consolidation_agent`

### [`Yard Disruption Agent`](./yard_dock_sequencer/README.md)
- **Sub-Pillar**: `First & Mid-Mile`
- **Target Persona**: Yard Master / Plant Logistics
- **Value Metric**: `-60%–75% Yard Demurrage`
- **Overview**: Parses GPS & gate feeds to flag delays and reassign dock staging doors dynamically.
- **Systems**: Carrier Transit Telemetry (MCP / API) / Real-Time Carrier Visibility (MCP / API) Yard · Manhattan YMS · Warehouse Management System (WMS / MCP) · Fleet & Yard Geofencing Telemetry API & Geofencing · Vertex AI Vision ANPR · Operational SQL & Vector DB (On-Prem / Cloud) · Mathematical Optimization Solver (MILP / CP-SAT)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent yard_dock_sequencer`

### [`Cold-Chain Auditor`](./cold_chain_auditor/README.md)
- **Sub-Pillar**: `First & Mid-Mile`
- **Target Persona**: Cold Chain QA / Logistics Dir.
- **Value Metric**: `-50%–70% Cold-Chain Claims`
- **Overview**: Analyzes reefer IoT telemetry to flag thermal excursions and file carrier claims.
- **Systems**: Real-Time Carrier Visibility (MCP / API) / Carrier Transit Telemetry (MCP / API) · Ocean Vessel AIS Telemetry (MCP / API) · Air Cargo Flight Telemetry (MCP / API) · Sensitech Cold-Chain IoT · Google Maps Geofencing · Document AI · BigQuery · Operational SQL & Vector DB (On-Prem / Cloud) · Enterprise ERP (MCP / On-Prem DB) TM/AP
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent cold_chain_auditor`

### [`Aisle-Aligned Pallet`](./aisle_aligned_pallet_agent/README.md)
- **Sub-Pillar**: `Store Replenishment`
- **Target Persona**: Outbound Lead / Industrial Eng.
- **Value Metric**: `-20%–35% Store Unload Labor`
- **Overview**: Sequences DC pick waves to match individual store planograms and shelf layouts.
- **Systems**: IATA ONE Record / Cargo-XML e-AWB · CargoWise One · Champ Cargospot · Air Cargo Flight Telemetry (MCP / API) · TAC Index · Transportation Management System (TMS / MCP) · Mathematical Optimization Solver (MILP / CP-SAT) · BigQuery · Low-Latency Transactional State DB · Google Maps
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent aisle_aligned_pallet_agent`

### [`Store Capacity Agent`](./store_capacity_agent/README.md)
- **Sub-Pillar**: `Store Replenishment`
- **Target Persona**: Store Replenishment Lead
- **Value Metric**: `-25% Backroom Congestion`
- **Overview**: Throttles push replenishment based on store backroom limits and live POS velocity.
- **Systems**: Enterprise ERP (MCP / On-Prem DB) MM · Supply Planning System (MCP / API) Inventory · Supply Planning Platform (MCP / API) · Warehouse Management System (WMS / On-Prem / API) · BigQuery Twin · Multi-Hop Graph Database (Cloud / On-Prem) · Mathematical Optimization Solver (MILP / CP-SAT) · Google Maps Distance Matrix
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent store_capacity_agent`

### [`Curfew Orchestrator`](./port_drayage_orchestrator/README.md)
- **Sub-Pillar**: `Store Replenishment`
- **Target Persona**: Retail Logistics Dispatcher
- **Value Metric**: `-80% Curfew & Slot Penalties`
- **Overview**: Coordinates municipal delivery curfews and store dock shift schedules dynamically.
- **Systems**: Spire / MarineTraffic Satellite AIS · CargoWise One · INTTRA · Real-Time Carrier Visibility (MCP / API) Ocean · Global Trade & Tariff System (MCP / API) & TM · Weather & Climate Ensemble Feed (MCP / API) Marine · Google Maps Routes · BigQuery GIS · Low-Latency Transactional State DB
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent port_drayage_orchestrator`

### [`Geocoding Intelligence`](./geocoding_intelligence_agent/README.md)
- **Sub-Pillar**: `Last-Mile Delivery`
- **Target Persona**: Last-Mile Operations Lead
- **Value Metric**: `-30%–45% Failed Deliveries`
- **Overview**: Interprets gate codes, apartment delivery notes, and aerial imagery to guide drivers.
- **Systems**: Geospatial Routing & Traffic Telemetry API · Fleet & Yard Geofencing Telemetry API · Mathematical Optimization Solver (MILP / CP-SAT) · Transportation Management System (TMS / API) · Transportation Management System (TMS / MCP) · Transportation Management System (TMS / API) · Samsara ELD · Operational SQL & Vector DB (On-Prem / Cloud) · BigQuery
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent geocoding_intelligence_agent`

### [`Courier Allocation`](./multimodal_mode_shift_agent/README.md)
- **Sub-Pillar**: `Last-Mile Delivery`
- **Target Persona**: E-Commerce Logistics Dir.
- **Value Metric**: `-8%–14% Parcel & Courier Spend`
- **Overview**: Routes parcels dynamically across internal fleet, 3PL, and gig couriers by rate card.
- **Systems**: Enterprise ERP (MCP / On-Prem DB) TM & aATP · Transportation Management System (TMS / API) · CargoWise · BigQuery Supply Chain Twin · Multi-Hop Graph Database (Cloud / On-Prem) · Mathematical Optimization Solver (MILP / CP-SAT) · Geospatial Routing & ETA Telemetry API · Weather & Climate Ensemble Feed (MCP / API)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent multimodal_mode_shift_agent`

### [`Delivery Exception Copilot`](./otif_penalty_shield/README.md)
- **Sub-Pillar**: `Last-Mile Delivery`
- **Target Persona**: Customer Support Ops Lead
- **Value Metric**: `-50%–65% WISMO & Chargebacks`
- **Overview**: Detects en-route exceptions and updates customers proactively with reschedule links.
- **Systems**: Retail Customer POS Portal (EDI / MCP) / Target / DMart (Avenue Supermarts) OTIF Portals · Enterprise ERP (MCP / On-Prem DB) SD & FI-AR · Real-Time Carrier Visibility (MCP / API) GPS · Google Maps Geofencing · Document AI · BigQuery · Operational SQL & Vector DB (On-Prem / Cloud)
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent otif_penalty_shield`

### [`Dynamic Rerouter`](./fleetflow_dispatch/README.md)
- **Sub-Pillar**: `Route & Carrier`
- **Target Persona**: Fleet Dispatcher / Central Ops
- **Value Metric**: `-6%–11% Fleet Miles & Fuel`
- **Overview**: Recalculates multi-stop routes using live Google Maps traffic, radar, and bridge limits.
- **Systems**: Geospatial Routing & Traffic Telemetry API · Fleet & Yard Geofencing Telemetry API · Mathematical Optimization Solver (MILP / CP-SAT) · Transportation Management System (TMS / API) · Transportation Management System (TMS / MCP) · Transportation Management System (TMS / API) · Samsara ELD · Operational SQL & Vector DB (On-Prem / Cloud) · BigQuery
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent fleetflow_dispatch`

### [`Routing Guide Compliance`](./freight_control_tower/README.md)
- **Sub-Pillar**: `Route & Carrier`
- **Target Persona**: Transport Procurement Lead
- **Value Metric**: `-15%–22% Spot Freight Spend`
- **Overview**: Tracks carrier tender acceptance & OTIF to reprioritize waterfall routing guides.
- **Systems**: Real-Time Carrier Visibility (MCP / API) / Carrier Transit Telemetry (MCP / API) · Ocean Vessel AIS Telemetry (MCP / API) · Air Cargo Flight Telemetry (MCP / API) · Sensitech Cold-Chain IoT · Google Maps Geofencing · Document AI · BigQuery · Operational SQL & Vector DB (On-Prem / Cloud) · Enterprise ERP (MCP / On-Prem DB) TM/AP
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent freight_control_tower`

### [`Freight Bill Audit Agent`](./freight_bill_audit_agent/README.md)
- **Sub-Pillar**: `Route & Carrier`
- **Target Persona**: Freight Controller / Claims
- **Value Metric**: `Recovers 3%–7% Freight Spend`
- **Overview**: Extracts signed PODs and rate contracts via OCR to audit accessorial surcharges.
- **Systems**: Real-Time Carrier Visibility (MCP / API) / Carrier Transit Telemetry (MCP / API) · Ocean Vessel AIS Telemetry (MCP / API) · Air Cargo Flight Telemetry (MCP / API) · Sensitech Cold-Chain IoT · Google Maps Geofencing · Document AI · BigQuery · Operational SQL & Vector DB (On-Prem / Cloud) · Enterprise ERP (MCP / On-Prem DB) TM/AP
- **1-Command Deploy**: `python3 scripts/deploy_to_gemini_enterprise.py --agent freight_bill_audit_agent`


## Pillar 06: Returns & Circularity (🔄 0 Agents)




---

## 🚀 1-Command Automated Deployments

### Deploy Any Single Agent:
```bash
python3 scripts/deploy_to_gemini_enterprise.py --agent <agent_id>
```

### Deploy 25 Curated Showcase Agents:
```bash
python3 scripts/deploy_to_gemini_enterprise.py --curated-showcase
```

### Deploy All 60 Agents:
```bash
python3 scripts/deploy_to_gemini_enterprise.py --all-60
```

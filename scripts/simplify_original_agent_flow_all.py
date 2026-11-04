#!/usr/bin/env python3
"""
Restore the Original 4-Stage SVG Execution Flow visual design across ALL 60 agents
(including `port_drayage_orchestrator` / Curfew Orchestrator) while making every
header and stage card's text simple, crisp, domain-relevant, and zero-overflow.
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NEW_FLOW_JS_BLOCK = r"""    const TOPOLOGY_META = {
      sensing_fan: {
        badge: 'Demand & Signal Forecasting',
        icons: ['📡', '🗄️', '📈', '🛡️', '🎯'],
        stageLabels: ['1 · Live Signals', '2 · Clean Data', '3 · Forecast Fan', '4 · Policy Gate', '5 · Update Plan']
      },
      elasticity_curve: {
        badge: 'Price & Promo Optimization',
        icons: ['🏷️', '📊', '🧮', '⚖️', '💰'],
        stageLabels: ['1 · Price & Sales', '2 · Strip Baseline', '3 · Uplift Curve', '4 · Margin Gate', '5 · Publish Price']
      },
      milp_pareto_loop: {
        badge: 'Constraint & Math Optimization',
        icons: ['📥', '🔗', '⚙️', '🛡️', '🚀'],
        stageLabels: ['1 · Live Inputs', '2 · Check Limits', '3 · Math Solver', '4 · Policy Gate', '5 · Commit Plan']
      },
      graph_contract_audit: {
        badge: 'Supplier Graph & Document Audit',
        icons: ['📄', '🕸️', '🔍', '🔒', '✅'],
        stageLabels: ['1 · Docs & Alerts', '2 · Map Graph', '3 · Risk & Audit', '4 · Policy Gate', '5 · ERP Action']
      },
      edge_vision_iot: {
        badge: 'Edge Vision & Sensor AI',
        icons: ['📷', '⚡', '🔬', '🚨', '🔧'],
        stageLabels: ['1 · Camera & IoT', '2 · Sync Stream', '3 · Vision & AI', '4 · Safety Gate', '5 · Line Action']
      },
      spatial_wms_atp: {
        badge: 'Warehouse & Order Promising',
        icons: ['🛒', '📐', '📦', '🚦', '🏢'],
        stageLabels: ['1 · Orders & Yard', '2 · Live Stock', '3 · 3D & Wave AI', '4 · Policy Gate', '5 · WMS Commit']
      },
      multimodal_corridor_vrp: {
        badge: 'Route & Load Optimization',
        icons: ['🚢', '🗺️', '🚚', '🛣️', '📍'],
        stageLabels: ['1 · Fleet & GPS', '2 · Lane Check', '3 · Route & Load', '4 · Safety Gate', '5 · TMS Dispatch']
      },
      circular_warroom_triage: {
        badge: 'Exception Triage & Recovery',
        icons: ['🚨', '🧭', '🔀', '🛡️', '⚡'],
        stageLabels: ['1 · Alert Intake', '2 · Gather Facts', '3 · Rank Options', '4 · Policy Gate', '5 · Auto-Resolve']
      }
    };

    /* Concise, plain-English, zero-overflow Execution Flow copy for all 60 agents */
    const AGENT_FLOW_BRIEFS = {
      demand_sensing_agent: {
        s1a: 'POS & Weather Feeds', s1aSub: 'Daily store scans + weather',
        s1b: 'SAP IBP & ERP Stock', s1bSub: 'On-hand units + open promos',
        s2Title: 'Clean & Match Signals', s2Sub: 'Fixes stockout gaps & bias',
        p1: 'pos_store_scans', p2: 'fva_sales_bias',
        s3Title: 'P10 / P50 / P90 Forecast', s3Tech: 'TimesFM + BigQuery ML',
        s4Title: 'Update Supply Plan', s4Gate: 'Auto ≤15% shift · Review >15%', s4Target: 'SAP IBP & ERP'
      },
      cpfr_sync_agent: {
        s1a: 'Retailer EDI 830 / POS', s1aSub: 'Buyer order forecasts',
        s1b: 'Internal Supply Plan', s1bSub: 'Baseline forecast + promos',
        s2Title: 'Spot Forecast Gaps', s2Sub: 'Flags buyer vs. plan drift',
        p1: 'retailer_edi830', p2: 'cpfr_consensus',
        s3Title: 'Consensus Forecast', s3Tech: 'TimesFM + Gemini Pro',
        s4Title: 'Sync Joint Plan', s4Gate: 'Auto ≤10% gap · Review >10%', s4Target: 'Retail Portal & IBP'
      },
      npi_demand_profiler: {
        s1a: 'Launch Brief & Orders', s1aSub: 'New SKU specs + pre-orders',
        s1b: 'Past Launch History', s1bSub: 'Lookalike SKU sales curves',
        s2Title: 'Match Lookalike SKUs', s2Sub: 'Finds closest past launches',
        p1: 'lookalike_skus', p2: 'npi_90day_plan',
        s3Title: '90-Day Launch Curve', s3Tech: 'TimesFM + Vector Match',
        s4Title: 'Set First Allocation', s4Gate: 'Auto Class-B · Review Hero', s4Target: 'SAP IBP & ERP'
      },
      promo_lift_simulator: {
        s1a: 'TPM Promo Calendar', s1aSub: 'Planned discounts + displays',
        s1b: 'POS & Margin Ledger', s1bSub: 'Historical lift + SKU COGS',
        s2Title: 'Strip Baseline Sales', s2Sub: 'Splits true lift vs. pull-fwd',
        p1: 'promo_elasticity', p2: 'sku_cannibalization',
        s3Title: 'Net Promo ROI Curve', s3Tech: 'Causal ML + OR-Tools',
        s4Title: 'Approve / Tune Promo', s4Gate: 'Block <0% ROI · Flag <10%', s4Target: 'TPM & Demand Plan'
      },
      field_beat_distributor_sync_agent: {
        s1a: 'Distributor Stock', s1aSub: 'Secondary sales + beat orders',
        s1b: 'JBP Terms & Targets', s1bSub: 'Rebate tiers + margin floors',
        s2Title: 'Audit Beat & Margin', s2Sub: 'Checks sell-out vs. rebates',
        p1: 'dms_live_stock', p2: 'beat_store_outlets',
        s3Title: 'JBP Scenario Solver', s3Tech: 'OR-Tools + Gemini Pro',
        s4Title: 'Publish JBP Offer', s4Gate: 'Auto in band · Review <floor', s4Target: 'CRM & DMS Portal'
      },
      trade_scheme_claims_reconciler: {
        s1a: 'Retailer Deductions', s1aSub: 'EDI 812 claims + debit notes',
        s1b: 'Signed Trade Schemes', s1bSub: 'Promo contracts + POS proof',
        s2Title: 'Match Claim to Proof', s2Sub: 'Checks scan volume & dates',
        p1: 'trade_schemes', p2: 'claim_audit_log',
        s3Title: 'Valid vs. Invalid Split', s3Tech: 'Document AI + Gemini',
        s4Title: 'Settle or Dispute', s4Gate: 'Auto-clear <$2K · Hold >$2K', s4Target: 'ERP AR & Portal'
      },
      sop_scenario_weaver: {
        s1a: 'Consensus Demand Plan', s1aSub: 'Upside / downside SKU demand',
        s1b: 'Plant & Supply Limits', s1bSub: 'Line hours, stock & COGS',
        s2Title: 'Map Bottlenecks', s2Sub: 'Finds capacity & stock gaps',
        p1: 'plant_capacities', p2: 'sop_tradeoffs',
        s3Title: 'EBITDA Trade-Off Plan', s3Tech: 'OR-Tools MILP + Gemini',
        s4Title: 'Publish S&OP Options', s4Gate: 'Exec sign-off on cap shifts', s4Target: 'SAP IBP & S&OP'
      },
      disruption_war_room_orchestrator: {
        s1a: 'AIS, Weather & News', s1aSub: 'Port closures & storm delays',
        s1b: 'Open Orders & Stock', s1bSub: 'At-risk loads + SLA value',
        s2Title: 'Score Orders at Risk', s2Sub: 'Links delays to customer SLA',
        p1: 'incident_war_rooms', p2: 'ais_vessel_etas',
        s3Title: '3-Option Recovery Plan', s3Tech: 'OR-Tools + Gemini Pro',
        s4Title: 'Reroute & Buffer', s4Gate: 'Auto <$5K · Exec >$5K', s4Target: 'TMS, ERP & Tower'
      },
      csco_control_tower_copilot: {
        s1a: 'Cross-Pillar KPIs', s1aSub: 'OTIF, stockouts, freight, OEE',
        s1b: 'ERP & Finance Ledger', s1bSub: 'Working capital + backlog $',
        s2Title: 'Find Root Exceptions', s2Sub: 'Ranks top margin & SLA risks',
        p1: 'order_backlog', p2: 'exec_playbooks',
        s3Title: 'Executive Action Rank', s3Tech: 'Gemini Pro + BigQuery',
        s4Title: 'Dispatch Playbook', s4Gate: 'Human sign-off on P&L shifts', s4Target: 'Control Tower'
      },
      working_capital_cash_bridge: {
        s1a: 'SKU Margin & Turns', s1aSub: '12-mo velocity & tail SKUs',
        s1b: 'Stock & AP/AR Terms', s1bSub: 'Holding cost + vendor terms',
        s2Title: 'Flag Cash-Trap SKUs', s2Sub: 'Finds low-margin slow movers',
        p1: 'inventory_ledger', p2: 'sku_margin_turns',
        s3Title: 'SKU Pruning Optimizer', s3Tech: 'OR-Tools MILP + Gemini',
        s4Title: 'Phase Out Tail SKUs', s4Gate: 'Commercial review on delist', s4Target: 'ERP & Portfolio'
      },
      eco_cutover_orchestrator: {
        s1a: 'PLM BOM Changes', s1aSub: 'New specs + target dates',
        s1b: 'Old Stock & Open POs', s1bSub: 'Plant stock + supplier WIP',
        s2Title: 'Find Run-Out Date', s2Sub: 'Matches old stock vs. burn',
        p1: 'bom_effectivity', p2: 'eco_cutover_plan',
        s3Title: 'Zero-Scrap Cutover', s3Tech: 'OR-Tools MILP + Gemini',
        s4Title: 'Sync ERP BOM & POs', s4Gate: 'QA + Eng cutover sign-off', s4Target: 'ERP BOM & POs'
      },
      network_twin_architect: {
        s1a: 'Shipment & Demand', s1aSub: 'Lane volumes, rates & SLAs',
        s1b: 'DC Leases & Capacity', s1bSub: 'Fixed costs, cube & labor',
        s2Title: 'Map Cost-to-Serve', s2Sub: 'Scores lane + node cost/unit',
        p1: 'network_facilities', p2: 'cog_milp_scenarios',
        s3Title: 'Optimal Node & Lanes', s3Tech: 'Center-of-Gravity MILP',
        s4Title: 'Publish Network Plan', s4Gate: 'CapEx board review required', s4Target: 'Network Twin'
      },
      tier_n_risk_sentinel: {
        s1a: 'Customs & Risk Feeds', s1aSub: 'Sub-tier alerts, weather, AIS',
        s1b: 'Multi-Tier BOM & POs', s1bSub: 'Supplier sites + customer SKU',
        s2Title: 'Trace Tier-N Impact', s2Sub: 'Maps disrupted site to orders',
        p1: 'disruption_threats', p2: 'bom_sku_lineage',
        s3Title: 'Dual-Source & Buffer', s3Tech: 'Graph AI + OR-Tools',
        s4Title: 'Split PO & Buffer', s4Gate: 'Auto buffer · Buyer ok on PO', s4Target: 'SAP Ariba & ERP'
      },
      supplier_quality_sentinel: {
        s1a: 'Vendor Certs & COAs', s1aSub: 'ISO certs, audits & lab specs',
        s1b: 'Defect & Audit Log', s1bSub: 'Lot rejections + compliance',
        s2Title: 'Check Certs & Specs', s2Sub: 'Flags expired docs & COA gaps',
        p1: 'quality_deviations', p2: 'copq_vendor_ledger',
        s3Title: 'Supplier QA Risk Score', s3Tech: 'Document AI + Gemini',
        s4Title: 'Approve or Hold Lot', s4Gate: 'Auto-hold on safety spec fail', s4Target: 'QMS & ERP Master'
      },
      carbon_scope3_ledger: {
        s1a: 'Vendor Declarations', s1aSub: 'CBAM carbon + EUDR geo-plots',
        s1b: 'Satellite & PO Data', s1bSub: 'Plot imagery + load weights',
        s2Title: 'Verify Plot & Carbon', s2Sub: 'Checks forest & CO2 math',
        p1: 'cbam_declarations', p2: 'eudr_plot_checks',
        s3Title: 'Scope 3 Audit Calc', s3Tech: 'Earth Engine + Gemini',
        s4Title: 'File ESG Certificate', s4Gate: 'Block non-compliant imports', s4Target: 'ESG & Customs'
      },
      commodity_index_advisor: {
        s1a: 'Commodity Futures', s1aSub: 'LME, CBOT, resin & FX feeds',
        s1b: 'Contracts & BOMs', s1bSub: 'Unhedged spend + index rules',
        s2Title: 'Measure Price Risk', s2Sub: 'Tracks index bands & collars',
        p1: 'futures_index_feed', p2: 'hedge_positions',
        s3Title: 'Buy Window & Collar', s3Tech: 'TimesFM + Quant Solver',
        s4Title: 'Lock Buy or Rebate', s4Gate: 'Treasury ok >$50K hedge', s4Target: 'Sourcing & ERP'
      },
      rfq_should_cost_agent: {
        s1a: 'Supplier RFQ Bids', s1aSub: 'Quoted unit rates + tooling',
        s1b: 'Material & Labor DB', s1bSub: 'BOM weights, cycle & rates',
        s2Title: 'Build Should-Cost', s2Sub: 'Material, labor & margin',
        p1: 'commodity_rates', p2: 'award_scenarios',
        s3Title: 'Optimal Award Split', s3Tech: 'OR-Tools MILP + Gemini',
        s4Title: 'Send Counter-Offer', s4Gate: 'Category lead approves award', s4Target: 'SAP Ariba'
      },
      sustainable_packaging_agent: {
        s1a: 'Packaging BOM Specs', s1aSub: 'Resin type, grams & PCR %',
        s1b: 'EPR Plastic Tax Rules', s1bSub: 'Country fees + crush limits',
        s2Title: 'Audit Tax & Weight', s2Sub: 'Spots heavy, high-tax packs',
        p1: 'packaging_bom', p2: 'epr_tax_ledger',
        s3Title: 'Low-Tax Pack Spec', s3Tech: 'OR-Tools + Gemini Pro',
        s4Title: 'Update Pack Spec', s4Gate: 'QA transit test before switch', s4Target: 'PLM & EPR Filing'
      },
      tariff_esg_agent: {
        s1a: 'Contracts & Tariffs', s1aSub: 'Rebate tiers, SLAs & HTS',
        s1b: 'AP Invoices & Duties', s1bSub: 'Billed prices + duty paid',
        s2Title: 'Spot Spend Leakage', s2Sub: 'Catches missed rebates & HTS',
        p1: 'contract_clauses', p2: 'duty_impact_log',
        s3Title: 'Rebate & Duty Claim', s3Tech: 'Document AI + Gemini',
        s4Title: 'Issue Debit / Reclass', s4Gate: 'Trade/Legal sign-off on HTS', s4Target: 'ERP AP & Trade'
      },
      master_data_leadtime_steward: {
        s1a: 'ASN & Receipt Logs', s1aSub: 'Actual transit + vendor days',
        s1b: 'ERP Master Lead Time', s1bSub: 'Static MRP days + open POs',
        s2Title: 'Spot Lead-Time Drift', s2Sub: 'Flags late POs & stale MRP',
        p1: 'bom_leadtimes', p2: 'late_po_tracker',
        s3Title: 'True Lead-Time & Chase', s3Tech: 'BigQuery ML + Gemini',
        s4Title: 'Sync MRP & Chase PO', s4Gate: 'Auto nudge · Buyer ok on air', s4Target: 'ERP & Vendor'
      },
      three_way_match_dispute: {
        s1a: 'Vendor Invoices', s1aSub: 'Billed qty, unit price & tax',
        s1b: 'ERP PO & Dock GRN', s1bSub: 'Contract price + received qty',
        s2Title: '3-Way Line Match', s2Sub: 'Finds price or short-ship gap',
        p1: 'ap_invoices', p2: 'po_schedules',
        s3Title: 'Auto-Clear vs Dispute', s3Tech: 'Document AI + Gemini',
        s4Title: 'Pay or Send Debit', s4Gate: 'Auto ≤$250 · Hold >$250', s4Target: 'SAP FI/AP'
      },
      finite_production_scheduler: {
        s1a: 'Firm Orders & WIP', s1aSub: 'Due dates, priorities & stock',
        s1b: 'Line & Clean Matrix', s1bSub: 'Allergen wash + setup mins',
        s2Title: 'Check Setup & Crew', s2Sub: 'Maps sequence wash penalties',
        p1: 'changeover_matrix', p2: 'line_schedule',
        s3Title: 'Min-Setup Sequence', s3Tech: 'OR-Tools CP-SAT',
        s4Title: 'Publish Shift Plan', s4Gate: 'Scheduler lock <24h window', s4Target: 'MES & SAP PP/DS'
      },
      line_schedule_optimizer: {
        s1a: 'Live Line Stop / Rush', s1aSub: 'Machine fault or hot order',
        s1b: 'Active Shift Plan', s1bSub: 'Alt lines + material WIP',
        s2Title: 'Check Delayed Orders', s2Sub: 'Scores SLA risk & alt lines',
        p1: 'active_line_state', p2: 'line_schedule',
        s3Title: 'Fast Re-Sequence', s3Tech: 'OR-Tools CP-SAT + Gemini',
        s4Title: 'Move Jobs to Alt Line', s4Gate: 'Shift lead 1-click confirm', s4Target: 'Plant MES'
      },
      labor_line_balancing_agent: {
        s1a: 'Shift Attendance', s1aSub: 'Certified skills + clock-ins',
        s1b: 'Line Takt & Fatigue', s1bSub: 'Station cycle + overtime cap',
        s2Title: 'Spot Line Bottleneck', s2Sub: 'Finds skill gaps & OT risk',
        p1: 'shift_rosters', p2: 'fatigue_overtime',
        s3Title: 'Balanced Crew Plan', s3Tech: 'OR-Tools CP-SAT',
        s4Title: 'Publish Crew Roster', s4Gate: 'Enforces union & safety rules', s4Target: 'Workforce & MES'
      },
      predictive_oee_sentinel: {
        s1a: 'PLC Vibration & Temp', s1aSub: '100Hz bearing, amp & heat IoT',
        s1b: 'CMMS Spares & Plan', s1bSub: 'Spare parts + planned stops',
        s2Title: 'Spot Early Faults', s2Sub: 'Detects wear days in advance',
        p1: 'machine_telemetry', p2: 'oee_breakdowns',
        s3Title: 'Failure & PM Window', s3Tech: 'FFT Anomaly + OR-Tools',
        s4Title: 'Book Maintenance Slot', s4Gate: 'Auto PM ticket · Safe stop', s4Target: 'SAP PM & PLC'
      },
      copacker_allocation_agent: {
        s1a: 'Overflow SKU Demand', s1aSub: 'Promo surge + pack formats',
        s1b: 'CMO Rates & Yields', s1bSub: 'Tolling tiers, freight & QA',
        s2Title: 'Compare Landed Cost', s2Sub: 'Checks CMO cap, yield & lane',
        p1: 'tolling_contracts', p2: 'cmo_allocations',
        s3Title: 'Optimal CMO Split', s3Tech: 'OR-Tools MILP',
        s4Title: 'Issue Tolling POs', s4Gate: 'Sourcing ok >$25K shift', s4Target: 'ERP Subcontract'
      },
      capex_simulator_agent: {
        s1a: 'CapEx Proposals', s1aSub: 'Line cost, speed & OEE lift',
        s1b: '5-Yr Demand & WACC', s1bSub: 'Volume scenarios + hurdle %',
        s2Title: 'Stress-Test Payback', s2Sub: 'Tests volume dips & limits',
        p1: 'capex_proposals', p2: 'npv_simulations',
        s3Title: 'Monte Carlo NPV Rank', s3Tech: 'Monte Carlo + OR-Tools',
        s4Title: 'Rank CapEx Projects', s4Gate: 'Finance board sign-off', s4Target: 'CapEx & FP&A'
      },
      inline_yield_guardian: {
        s1a: 'Line Vision Cameras', s1aSub: 'Seal, fill, label & surface',
        s1b: 'Batch & PLC Targets', s1bSub: 'Weight, temp & torque limits',
        s2Title: 'Catch Micro-Defects', s2Sub: 'Links flaw to machine drift',
        p1: 'vision_frames', p2: 'batch_deviations',
        s3Title: 'Defect & Setpoint Fix', s3Tech: 'Gemini Vision + Edge AI',
        s4Title: 'Eject & Tune Recipe', s4Gate: 'QA interlock on spec bounds', s4Target: 'Line PLC & eBHR'
      },
      batch_record_auditor: {
        s1a: 'Digital Batch Logs', s1aSub: 'MES steps, lab COAs & signs',
        s1b: 'GMP & 21 CFR Rules', s1bSub: 'SOP limits + deviation log',
        s2Title: 'Scan Batch Exceptions', s2Sub: 'Flags missing signs & OOS',
        p1: 'batch_capa_logs', p2: 'cfr11_signoffs',
        s3Title: 'Lot Release Verdict', s3Tech: 'Document AI + Gemini Pro',
        s4Title: 'Fast-Track QA Release', s4Gate: 'Qualified Person final sign', s4Target: 'QMS & SAP QM'
      },
      scrap_defect_root_cause_agent: {
        s1a: 'Scrap & Defect Logs', s1aSub: 'Reject codes, lots & shifts',
        s1b: 'SCADA & Lot History', s1bSub: 'Temp, humidity & vendor lots',
        s2Title: 'Correlate Drift', s2Sub: 'Finds variable driving scrap',
        p1: 'param_correlations', p2: 'scada_setpoints',
        s3Title: 'Root Cause & CAPA', s3Tech: 'Causal ML + Gemini Pro',
        s4Title: 'Send CAPA & Setpoint', s4Gate: 'Process eng approves recipe', s4Target: 'QMS & SCADA'
      },
      meio_safety_stock_agent: {
        s1a: 'Demand Volatility', s1aSub: 'Forecast error across DCs',
        s1b: 'Lead-Time Spread', s1bSub: 'Vendor variance + target SLA',
        s2Title: 'Audit Buffer Levels', s2Sub: 'Finds excess cash vs. risk',
        p1: 'echelon_balances', p2: 'sla_projections',
        s3Title: 'Multi-Node Buffer Opt', s3Tech: 'MEIO Solver + BigQuery',
        s4Title: 'Update Safety Stocks', s4Gate: 'Auto ≤20% · Planner >20%', s4Target: 'SAP IBP & ERP'
      },
      slob_disposition_agent: {
        s1a: 'Aging & Slow Stock', s1aSub: 'Days-on-supply + shelf life',
        s1b: 'Outlet & Liq Bids', s1bSub: 'Recovery rates + handling $',
        s2Title: 'Score Write-Off Risk', s2Sub: 'Flags lots near expiry cliff',
        p1: 'aging_dos_ledger', p2: 'recovery_rates',
        s3Title: 'Best Recovery Channel', s3Tech: 'OR-Tools MILP + Gemini',
        s4Title: 'Markdown or Transfer', s4Gate: 'Finance ok >30% discount', s4Target: 'ERP & Outlet'
      },
      crossdock_transfer_orchestrator: {
        s1a: 'Regional Stockouts', s1aSub: 'DC gaps + store demand spike',
        s1b: 'Inbound & Alt DCs', s1bSub: 'Truck ETAs + surplus stock',
        s2Title: 'Match Surplus to Gap', s2Sub: 'Transfer cost vs. lost sales',
        p1: 'crossdock_dwell', p2: 'inbound_etas',
        s3Title: 'Cross-Dock Rebalance', s3Tech: 'OR-Tools MILP',
        s4Title: 'Divert Load / STO', s4Gate: 'Auto when margin > freight $', s4Target: 'WMS & ERP STO'
      },
      warehouse_slotting_agent: {
        s1a: 'Pick Velocity & Pairs', s1aSub: 'Fast movers + co-picked SKUs',
        s1b: '3D Rack & Cube Map', s1bSub: 'Golden-zone bins + weight',
        s2Title: 'Spot Pick Congestion', s2Sub: 'Finds mis-slotted fast SKUs',
        p1: 'picker_telemetry', p2: 'slot_moves',
        s3Title: 'Golden-Zone Re-Slot', s3Tech: '3D Spatial CP-SAT',
        s4Title: 'Queue Re-Slot Moves', s4Gate: 'Heavy-on-bottom safety rule', s4Target: 'WMS / SAP EWM'
      },
      dock_to_stock_agent: {
        s1a: 'ASN & Pallet Scans', s1aSub: 'Gate camera + barcode scans',
        s1b: 'Open POs & Free Bins', s1bSub: 'Backorders + open rack slots',
        s2Title: 'Check Receipt & Need', s2Sub: 'Flags urgent backorder items',
        p1: 'pallet_scan_logs', p2: 'turnaround_log',
        s3Title: 'Direct Bin / Crossdock', s3Tech: 'Gemini Vision + WMS AI',
        s4Title: 'Dispatch Forklift', s4Gate: 'Auto-hold damaged pallets', s4Target: 'WMS RF & ERP'
      },
      wave_fulfillment_copilot: {
        s1a: 'Live Order Backlog', s1aSub: 'eComm + truck wave cutoffs',
        s1b: 'Zone Crew & Sorters', s1bSub: 'Picker count + chute load',
        s2Title: 'Spot Cutoff Bottleneck', s2Sub: 'Predicts zone jam 2h ahead',
        p1: 'carrier_cutoffs', p2: 'wave_directives',
        s3Title: 'Dynamic Wave & Crew', s3Tech: 'OR-Tools CP-SAT',
        s4Title: 'Rebalance Wave & Crew', s4Gate: 'DC lead confirms zone flex', s4Target: 'WMS Wave Engine'
      },
      planogram_merchandising_vision_auditor: {
        s1a: 'Shelf Photos & POS', s1aSub: 'Store snaps + zero-scan SKUs',
        s1b: 'Planogram & On-Hand', s1bSub: 'Shelf map + backroom units',
        s2Title: 'Spot Phantom Stock', s2Sub: 'In backroom, missing on shelf',
        p1: 'planogram_specs', p2: 'store_shelf_tasks',
        s3Title: 'Shelf Gap & Task AI', s3Tech: 'Gemini Vision + Anomaly',
        s4Title: 'Send Restock Alert', s4Gate: 'Auto-push to store handheld', s4Target: 'Store App & SFA'
      },
      atp_order_promising_agent: {
        s1a: 'Live Checkout Orders', s1aSub: 'Cart SKUs, ZIP & SLA promise',
        s1b: 'Store + DC ATP & Rate', s1bSub: 'Live stock + parcel tariffs',
        s2Title: 'Check Split-Box Cost', s2Sub: 'Avoids costly split shipments',
        p1: 'order_requests', p2: 'tier_sla_rules',
        s3Title: 'Best Node Sourcing', s3Tech: 'Low-Latency MILP',
        s4Title: 'Commit Node & ETA', s4Gate: 'Protects walk-in store stock', s4Target: 'OMS & Store App'
      },
      returns_triage_agent: {
        s1a: 'Return Scan & Photos', s1aSub: 'RMA reason + dock camera',
        s1b: 'Resale & Refurb Value', s1bSub: 'Channel price + refurb cost',
        s2Title: 'Grade Item Condition', s2Sub: 'Sorts Grade-A, refurb, scrap',
        p1: 'return_intake', p2: 'optical_grading',
        s3Title: 'Best-Margin Routing', s3Tech: 'Gemini Vision + MILP',
        s4Title: 'Route Restock / Refurb', s4Gate: 'QA check on sealed items', s4Target: 'WMS & RMA'
      },
      load_consolidation_agent: {
        s1a: 'Orders & Pallet Dims', s1aSub: 'Cube, weight & stop windows',
        s1b: 'Trailer & Axle Limits', s1bSub: '53ft cube, crush & DOT rules',
        s2Title: 'Group Matching Stops', s2Sub: 'Aligns corridor, temp & seq',
        p1: 'voxel_load_plans', p2: 'axle_crush_rules',
        s3Title: '3D LIFO Load Plan', s3Tech: '3D Bin-Pack + OR-Tools',
        s4Title: 'Build & Tender FTL', s4Gate: '100% DOT axle & crush safe', s4Target: 'TMS & Dock Map'
      },
      yard_dock_sequencer: {
        s1a: 'Gate Cam & Truck GPS', s1aSub: 'Live ETAs + yard queue',
        s1b: 'Dock Doors & Crew', s1bSub: 'Door specs + detention timer',
        s2Title: 'Spot Detention Risk', s2Sub: 'Flags reefers & demurrage',
        p1: 'detention_risk', p2: 'dock_schedules',
        s3Title: 'Door & Shunt Solver', s3Tech: 'OR-Tools CP-SAT',
        s4Title: 'Assign Door & SMS', s4Gate: 'Priority lock on cold loads', s4Target: 'YMS, WMS & SMS'
      },
      cold_chain_auditor: {
        s1a: 'Reefer IoT Loggers', s1aSub: 'Live °C + door-open events',
        s1b: 'SKU Stability Specs', s1bSub: 'Max degree-hrs + shelf life',
        s2Title: 'Check Thermal Budget', s2Sub: 'Calculates true potency left',
        p1: 'stability_specs', p2: 'qa_claims_ledger',
        s3Title: 'Release vs. Hold Call', s3Tech: 'Kinetic Decay + Gemini',
        s4Title: 'Release or File Claim', s4Gate: 'QA lock on safety excursion', s4Target: 'SAP QM & Claims'
      },
      aisle_aligned_pallet_agent: {
        s1a: 'Store Case Orders', s1aSub: 'Replenishment cases by store',
        s1b: 'Aisle Map & Crush DB', s1bSub: 'Store layout + box strength',
        s2Title: 'Group by Store Aisle', s2Sub: 'Matches aisle order & weight',
        p1: 'crush_physics', p2: 'pallet_sequences',
        s3Title: 'Aisle-Ready 3D Layer', s3Tech: '3D Stacking CP-SAT',
        s4Title: 'Send Pallet Build Seq', s4Gate: 'Zero crush weight violation', s4Target: 'WMS & Palletizer'
      },
      store_capacity_agent: {
        s1a: 'Store POS & On-Hand', s1aSub: 'Live sales + backroom count',
        s1b: 'Backroom Cap & Drops', s1bSub: 'Max pallets + store crew hrs',
        s2Title: 'Spot Backroom Jam', s2Sub: 'Flags drops over store room',
        p1: 'store_onhand', p2: 'scheduled_drops',
        s3Title: 'Smoothed Drop Plan', s3Tech: 'OR-Tools MILP + TimesFM',
        s4Title: 'Pace & Shift Drops', s4Gate: 'Protects promo & A-SKUs', s4Target: 'Replenish & WMS'
      },
      port_drayage_orchestrator: {
        s1a: 'Fleet GPS & Curfews', s1aSub: 'Live truck ETA + quiet zones',
        s1b: 'TMS & Dock Roster', s1bSub: 'Bay doors + crew shift hours',
        s2Title: 'Spot Curfew Clash', s2Sub: 'Flags diesel trucks > 22:00',
        p1: 'curfew_rules', p2: 'dock_rosters',
        s3Title: 'Quiet-EV & Slot Swap', s3Tech: 'OR-Tools CP-SAT + Gemini',
        s4Title: 'Swap EV & Rebook Bay', s4Gate: 'Auto ≤30m · Review >$500', s4Target: 'TMS & Store WMS'
      },
      geocoding_intelligence_agent: {
        s1a: 'Driver GPS & Scans', s1aSub: 'Actual drop pin + gate snaps',
        s1b: 'Stop Address Master', s1bSub: 'Rooftop coords + dock notes',
        s2Title: 'Find True Dock Pin', s2Sub: 'Fixes rooftop vs. bay error',
        p1: 'rooftop_coords', p2: 'driver_dwell_logs',
        s3Title: 'Verified Bay Geofence', s3Tech: 'Geo-Cluster + Vision AI',
        s4Title: 'Update Stop Master', s4Gate: 'Auto-save >95% confidence', s4Target: 'TMS & Nav App'
      },
      multimodal_mode_shift_agent: {
        s1a: 'Outbound Shipments', s1aSub: 'Weight, dims, zone & SLA',
        s1b: 'Courier & LTL Rates', s1bSub: 'DIM fees + lane on-time %',
        s2Title: 'Compare Mode & SLA', s2Sub: 'Weighs ground vs air cost',
        p1: 'outbound_orders', p2: 'mode_split_rates',
        s3Title: 'Lowest-Cost SLA Mode', s3Tech: 'OR-Tools Rate Solver',
        s4Title: 'Book Mode & Label', s4Gate: '100% promised SLA date kept', s4Target: 'TMS & Pack Line'
      },
      otif_penalty_shield: {
        s1a: 'Live Carrier GPS', s1aSub: 'Truck ETA vs. retail slot',
        s1b: 'Retailer OTIF Rules', s1bSub: 'MABD window + fine schedule',
        s2Title: 'Score OTIF Fine Risk', s2Sub: 'Flags late loads pre-arrival',
        p1: 'open_retail_slas', p2: 'edi856_dossiers',
        s3Title: 'Rebook vs. Expedite', s3Tech: 'OR-Tools + Gemini Pro',
        s4Title: 'Rebook / Fight Fine', s4Gate: 'Auto rebook · Dispute proof', s4Target: 'Retail & TMS'
      },
      fleetflow_dispatch: {
        s1a: 'Traffic, Weather, HOS', s1aSub: 'Road delays + driver hours',
        s1b: 'Active Fleet & Loads', s1bSub: 'Open stops + empty return',
        s2Title: 'Spot Delay & Deadhead', s2Sub: 'Finds detours & backhauls',
        p1: 'corridor_orders', p2: 'backhaul_matches',
        s3Title: 'Dynamic Route & Reload', s3Tech: 'OR-Tools VRP + Maps API',
        s4Title: 'Push New Route Live', s4Gate: '100% DOT HOS & weight legal', s4Target: 'Driver ELD & TMS'
      },
      freight_control_tower: {
        s1a: 'Rejects & Spot Bids', s1aSub: 'Tender drops + broker quotes',
        s1b: 'Contract Route Guide', s1bSub: 'Awarded rates + backup list',
        s2Title: 'Audit Spot Leakage', s2Sub: 'Flags off-guide rate spikes',
        p1: 'routing_guide', p2: 'spot_bid_quotes',
        s3Title: 'Best Backup Carrier', s3Tech: 'OR-Tools + Gemini',
        s4Title: 'Tender Backup Carrier', s4Gate: 'Auto ≤15% over contract', s4Target: 'TMS Tendering'
      },
      freight_bill_audit_agent: {
        s1a: 'EDI 210 Freight Bills', s1aSub: 'Linehaul, fuel & detention',
        s1b: 'Tariffs & GPS Proof', s1bSub: 'Signed rates + yard geofence',
        s2Title: 'Audit Rate & Dwell', s2Sub: 'Catches billing & dwell errs',
        p1: 'edi210_invoices', p2: 'lane_rate_tables',
        s3Title: 'Line Audit Verdict', s3Tech: 'Document AI + Rules',
        s4Title: 'Pay Exact or Dispute', s4Gate: 'Block unverified detention', s4Target: 'Freight Pay & AP'
      },
      reverse_rma_optimizer: {
        s1a: 'RMA & Return Photos', s1aSub: 'Serial #, snaps & history',
        s1b: 'Order & Fleet Routes', s1bSub: 'Original sale + nearby vans',
        s2Title: 'Screen Fraud Signals', s2Sub: 'Spots box-swap & wardrobing',
        p1: 'rma_requests', p2: 'vision_grading',
        s3Title: 'Fraud & Pickup Match', s3Tech: 'Gemini Vision + VRP',
        s4Title: 'Approve or Hold RMA', s4Gate: 'Human check before deny', s4Target: 'RMA & TMS'
      },
      keep_it_routing_advisor: {
        s1a: 'Return Request', s1aSub: 'Item price, weight & reason',
        s1b: 'Reverse & Refurb Cost', s1bSub: 'Return shipping + labor $',
        s2Title: 'Calc Net Recovery $', s2Sub: 'Resale value vs. return cost',
        p1: 'keep_it_rules', p2: 'ltv_fraud_scores',
        s3Title: 'Keep-It vs. Ship Back', s3Tech: 'Margin Solver + Gemini',
        s4Title: 'Refund or Send Label', s4Gate: 'Strict per-user abuse cap', s4Target: 'RMA & OMS'
      },
      osd_freight_claims_agent: {
        s1a: 'Damage Photos & BOL', s1aSub: 'OS&D scans + signed POD',
        s1b: 'Carrier Claim Rules', s1bSub: 'Liability caps + deadlines',
        s2Title: 'Build Claim Proof', s2Sub: 'Links seal, temp & dock pics',
        p1: 'osd_inspections', p2: 'carmack_rules',
        s3Title: 'Liability Dossier AI', s3Tech: 'Gemini Vision + Doc AI',
        s4Title: 'File Carrier Claim', s4Gate: 'Lead review on >$5K claim', s4Target: 'Carrier & AR'
      },
      dynamic_markdown_agent: {
        s1a: 'Lot Expiry & Stock', s1aSub: 'Days-to-expiry + shelf qty',
        s1b: 'Sell-Through & Tags', s1bSub: 'Elasticity + digital tags',
        s2Title: 'Spot Spoilage Risk', s2Sub: 'Predicts unsold units at end',
        p1: 'dte_elasticity', p2: 'esl_markdowns',
        s3Title: 'Optimal Markdown %', s3Tech: 'Elasticity ML + Solver',
        s4Title: 'Push New Shelf Price', s4Gate: 'Enforces brand floor price', s4Target: 'Store ESL & POS'
      },
      short_dated_redistributor: {
        s1a: 'Short-Dated DC Lots', s1aSub: 'FEFO lots near code cutoff',
        s1b: 'Fast Outlets & Buyers', s1bSub: 'High-turn stores & charity',
        s2Title: 'Match Life to Turn', s2Sub: 'Checks transit vs. days left',
        p1: 'lane_transit_days', p2: 'secondary_buyers',
        s3Title: 'Best Diversion Path', s3Tech: 'OR-Tools MILP',
        s4Title: 'Divert or Donate Lot', s4Gate: 'Enforces min customer code', s4Target: 'WMS, OMS & Tax'
      },
      food_waste_esg_copilot: {
        s1a: 'Unsellable Organics', s1aSub: 'Spoiled weight & food class',
        s1b: 'Digester & Tax Rules', s1bSub: 'Local haulers + tax credits',
        s2Title: 'Rank EPA Diversion', s2Sub: 'Feed & compost over landfill',
        p1: 'epa_partners', p2: 'digestion_rates',
        s3Title: 'Zero-Landfill Route', s3Tech: 'OR-Tools + Gemini',
        s4Title: 'Book Hauler & Credit', s4Gate: 'Safety lock on feed routing', s4Target: 'Hauler & ESG Log'
      },
      rti_balance_reconciler: {
        s1a: 'RFID & Barcode Scans', s1aSub: 'Pallets, totes & kegs moved',
        s1b: 'Pool Rental Tariffs', s1bSub: 'CHEP/PECO rent + lost fees',
        s2Title: 'Spot Hoarded Assets', s2Sub: 'Finds sites holding pallets',
        p1: 'rti_balances', p2: 'pool_fee_tariffs',
        s3Title: 'Sweep & Fee Audit', s3Tech: 'BigQuery + OR-Tools',
        s4Title: 'Book Sweep / Bill Fee', s4Gate: 'Verify POD before billing', s4Target: 'TMS & ERP AR'
      },
      intermodal_rail_linehaul_agent: {
        s1a: 'Empty Returns & Loads', s1aSub: 'Return stops & reload freight',
        s1b: 'Rail & Truck Lanes', s1bSub: 'Rail schedules + OTR rates',
        s2Title: 'Pair Outbound & Back', s2Sub: 'Cuts empty deadhead miles',
        p1: 'corridor_loads', p2: 'rail_conversions',
        s3Title: 'Milk-Run & Rail Loop', s3Tech: 'OR-Tools VRP + MILP',
        s4Title: 'Book Combined Loop', s4Gate: 'Transit buffer keeps SLA', s4Target: 'TMS & Rail EDI'
      },
      sanitation_health_agent: {
        s1a: 'Wash & Swab Sensors', s1aSub: 'Temp, caustic & ATP swabs',
        s1b: 'HACCP Hygiene Rules', s1bSub: 'FSMA & allergen wash limits',
        s2Title: 'Verify Clean Proof', s2Sub: 'Flags missed wash or swab',
        p1: 'rfid_wash_logs', p2: 'atp_swab_tests',
        s3Title: 'Hygiene Clearance AI', s3Tech: 'Anomaly AI + Interlock',
        s4Title: 'Clear or Lock Fill', s4Gate: 'Hard block on failed swab', s4Target: 'WMS, MES & QA'
      }
    };

    /* Clean short fallback helper for any dynamically synthesized Enterprise Twin agent */
    function buildCleanFlowBrief(ag, sysArr, tables, subs, solverLabel, writebackFull) {
      if (AGENT_FLOW_BRIEFS[ag.id]) {
        return AGENT_FLOW_BRIEFS[ag.id];
      }
      const shortClean = (str, max = 21) => {
        const s = String(str || '')
          .replace(/\(MCP[^)]*\)/gi, '')
          .replace(/\(On-Prem[^)]*\)/gi, '')
          .replace(/\(Cloud[^)]*\)/gi, '')
          .replace(/\(API[^)]*\)/gi, '')
          .replace(/Mathematical Optimization Solver/gi, 'OR-Tools Solver')
          .replace(/Time-Series Forecasting (Foundation )?Model/gi, 'TimesFM')
          .replace(/Operational SQL & Vector DB/gi, 'Vector & SQL DB')
          .replace(/Low-Latency Transactional State DB/gi, 'State DB')
          .replace(/Multi-Hop Graph Database/gi, 'Supply Graph DB')
          .replace(/\s+/g, ' ')
          .trim();
        if (!s) return 'Enterprise System';
        if (s.length <= max) return s;
        const words = s.split(' ');
        let out = '';
        for (const w of words) {
          if ((out ? out.length + 1 + w.length : w.length) <= max) {
            out = out ? out + ' ' + w : w;
          } else break;
        }
        return out || s.slice(0, max);
      };
      return {
        s1a: shortClean(sysArr[0] || 'Live Feed', 21),
        s1aSub: 'Real-time events & signals',
        s1b: shortClean(sysArr[1] || 'ERP & Twin', 21),
        s1bSub: 'Master data & inventory',
        s2Title: shortClean((subs[0] && subs[0].name) || 'Validate Data', 20),
        s2Sub: 'Matches signals & limits',
        p1: shortClean(tables[0] || 'live_signals', 19),
        p2: shortClean(tables[1] || 'system_rules', 19),
        s3Title: shortClean((subs[1] && subs[1].name) || 'Optimize Action', 22),
        s3Tech: shortClean(solverLabel || 'OR-Tools + Gemini', 25),
        s4Title: shortClean(writebackFull || 'Commit Update', 21),
        s4Gate: 'Auto in bounds · Human > cap',
        s4Target: 'ERP, WMS & TMS'
      };
    }

    /* Maps product-specific vendor strings to concise, clean labels */
    function toOpenTechLabel(rawStr) {
      if (!rawStr) return 'Enterprise System';
      let s = String(rawStr).trim();
      const replacements = [
        [/\(MCP\s*\/\s*On-Prem\s*DB\)/gi, ''],
        [/\(On-Prem\s*\/\s*Cloud\)/gi, ''],
        [/\(Cloud\s*\/\s*On-Prem\)/gi, ''],
        [/\(MCP\s*\/\s*API\)/gi, ''],
        [/\(EDI\s*\/\s*MCP\)/gi, ''],
        [/Mathematical Optimization Solver \(MILP \/ CP-SAT\)/gi, 'OR-Tools MILP / CP-SAT'],
        [/Time-Series Forecasting Foundation Model/gi, 'TimesFM Forecaster'],
        [/Low-Latency Transactional State DB/gi, 'State DB'],
        [/Operational SQL & Vector DB/gi, 'SQL & Vector DB'],
        [/\s+/g, ' ']
      ];
      for (const [regex, rep] of replacements) {
        s = s.replace(regex, rep);
      }
      return s.trim();
    }

    function pickSystemIcon(sysName) {
      const s = String(sysName || '').toLowerCase();
      if (s.includes('weather') || s.includes('climate') || s.includes('satellite')) return '🌦️';
      if (s.includes('geo') || s.includes('routing') || s.includes('gps') || s.includes('fleet') || s.includes('curfew') || s.includes('traffic')) return '🗺️';
      if (s.includes('pos') || s.includes('edi') || s.includes('retail') || s.includes('promo') || s.includes('store')) return '🛒';
      if (s.includes('vision') || s.includes('camera') || s.includes('photo') || s.includes('scan')) return '📷';
      if (s.includes('plc') || s.includes('scada') || s.includes('vibration') || s.includes('iot') || s.includes('reefer') || s.includes('sensor') || s.includes('swab')) return '📳';
      if (s.includes('ais') || s.includes('ocean') || s.includes('port') || s.includes('customs')) return '🚢';
      if (s.includes('air') || s.includes('flight') || s.includes('courier')) return '✈️';
      if (s.includes('rail') || s.includes('intermodal')) return '🚆';
      if (s.includes('wms') || s.includes('warehouse') || s.includes('yard') || s.includes('dock') || s.includes('rack')) return '🏢';
      if (s.includes('tms') || s.includes('carrier') || s.includes('freight') || s.includes('trailer')) return '🚚';
      if (s.includes('procurement') || s.includes('sourcing') || s.includes('supplier') || s.includes('contract') || s.includes('rfq') || s.includes('vendor')) return '🤝';
      if (s.includes('rma') || s.includes('return')) return '↩️';
      if (s.includes('erp') || s.includes('ibp') || s.includes('plan') || s.includes('finance') || s.includes('invoice')) return '🏦';
      return '🔌';
    }

    function renderFullTopologySvg(topology, ctx) {
      const {
        ag, dept, cls,
        sys1, sys2,
        tables, subs, solverLabel, writebackFull
      } = ctx;

      const uid = ag.id;
      const brief = buildCleanFlowBrief(ag, [sys1, sys2], tables || [], subs || [], solverLabel, writebackFull);
      const ic1 = pickSystemIcon(brief.s1a);
      const ic2 = pickSystemIcon(brief.s1b);
      const badgeLabel = String(ag.badge || 'Verified ROI').trim();
      const personaRaw = String(ag.primaryPersonaName || 'Operations Lead').trim();
      const personaShort = personaRaw.length > 24 ? personaRaw.split('/').shift().trim().slice(0, 24) : personaRaw;

      // Center visual graphic for Stage 3 based on the 8 topologies (Original visual design)
      let centerGraphic = '';
      let stage2Kicker = '2 · DATA CHECK';
      let stage3Kicker = '3 · AI & MATH SOLVER';

      if (topology === 'sensing_fan') {
        stage2Kicker = '2 · CLEAN & MATCH';
        stage3Kicker = '3 · FORECAST ENGINE';
        centerGraphic = `
          <rect class="svg-viz-well" width="248" height="108" rx="10" stroke="${dept.color}66" stroke-width="1.2" />
          <path d="M 88 58 C 132 42, 182 22, 232 14 L 232 94 C 182 84, 132 72, 88 58 Z" fill="${dept.color}38" />
          <path d="M 16 76 Q 44 64, 66 68 T 88 58" fill="none" stroke="#94a3b8" stroke-width="2.4" />
          <path d="M 88 58 C 132 42, 182 22, 232 14" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4 2" />
          <path d="M 88 58 C 136 52, 184 48, 232 44" fill="none" stroke="${dept.color}" stroke-width="2.8" />
          <path d="M 88 58 C 132 72, 182 84, 232 94" fill="none" stroke="#fbbf24" stroke-width="2" stroke-dasharray="4 2" />
          <circle cx="88" cy="58" r="5" fill="#ffffff" stroke="${dept.color}" stroke-width="2" />
          <text x="16" y="24" class="svg-text-mono" font-size="10" font-weight="700">ACTUALS</text>
          <text x="172" y="18" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">P90 HIGH</text>
          <text x="172" y="41" fill="${dept.color}" font-size="9.5" font-weight="800" font-family="var(--font-mono)">P50 PLAN</text>
          <text x="172" y="92" fill="#fbbf24" font-size="9.5" font-weight="800" font-family="var(--font-mono)">P10 LOW</text>
        `;
      } else if (topology === 'elasticity_curve') {
        stage2Kicker = '2 · BASELINE SPLIT';
        stage3Kicker = '3 · MARGIN SIMULATOR';
        centerGraphic = `
          <rect class="svg-viz-well" width="248" height="108" rx="10" stroke="#10b98166" stroke-width="1.2" />
          <rect x="22" y="42" width="24" height="44" rx="4" fill="#38bdf8" />
          <rect x="58" y="18" width="24" height="32" rx="4" fill="#10b981" />
          <rect x="94" y="28" width="24" height="24" rx="4" fill="#f43f5e" />
          <rect x="130" y="22" width="24" height="64" rx="4" fill="#fbbf24" />
          <text x="34" y="100" text-anchor="middle" class="svg-text-mono" font-size="9">BASE</text>
          <text x="70" y="100" text-anchor="middle" fill="#10b981" font-size="9" font-weight="800">+LIFT</text>
          <text x="106" y="100" text-anchor="middle" fill="#fb7185" font-size="9" font-weight="800">-COST</text>
          <text x="142" y="100" text-anchor="middle" fill="#fbbf24" font-size="9" font-weight="800">NET $</text>
          <path d="M 168 82 C 184 76, 198 24, 232 18" fill="none" stroke="#38bdf8" stroke-width="2.4" />
          <circle cx="202" cy="34" r="5" fill="#10b981" stroke="#ffffff" stroke-width="1.5" />
          <text x="172" y="20" fill="#10b981" font-size="9.5" font-weight="800" font-family="var(--font-mono)">BEST ROI</text>
        `;
      } else if (topology === 'graph_contract_audit') {
        stage2Kicker = '2 · GRAPH & DOC MATCH';
        stage3Kicker = '3 · RISK & AUDIT AI';
        centerGraphic = `
          <rect class="svg-viz-well" width="248" height="108" rx="10" stroke="#38bdf866" stroke-width="1.2" />
          <line x1="42" y1="54" x2="112" y2="27" stroke="#38bdf8" stroke-width="2" />
          <line x1="42" y1="54" x2="112" y2="81" stroke="#38bdf8" stroke-width="2" />
          <line x1="112" y1="27" x2="196" y2="35" stroke="#f43f5e" stroke-width="2.2" stroke-dasharray="4 2" />
          <line x1="112" y1="81" x2="196" y2="75" stroke="#10b981" stroke-width="2" />
          <circle cx="42" cy="54" r="14" fill="var(--svg-node-fill)" stroke="#38bdf8" stroke-width="2" />
          <text x="42" y="58" text-anchor="middle" fill="#38bdf8" font-size="9.5" font-weight="800">PO</text>
          <circle cx="112" cy="27" r="14" fill="var(--svg-node-fill)" stroke="#fbbf24" stroke-width="2" />
          <text x="112" y="31" text-anchor="middle" fill="#fbbf24" font-size="9.5" font-weight="800">T-N</text>
          <circle cx="112" cy="81" r="14" fill="var(--svg-node-fill)" stroke="#10b981" stroke-width="2" />
          <text x="112" y="85" text-anchor="middle" fill="#10b981" font-size="9.5" font-weight="800">DOC</text>
          <circle cx="196" cy="35" r="15" fill="rgba(244,63,94,0.22)" stroke="#f43f5e" stroke-width="2.2" />
          <text x="196" y="39" text-anchor="middle" fill="#fb7185" font-size="9.5" font-weight="800">FLAG</text>
          <circle cx="196" cy="75" r="14" fill="var(--svg-node-fill)" stroke="#10b981" stroke-width="2" />
          <text x="196" y="79" text-anchor="middle" fill="#10b981" font-size="9.5" font-weight="800">OK</text>
        `;
      } else if (topology === 'edge_vision_iot') {
        stage2Kicker = '2 · STREAM CHECK';
        stage3Kicker = '3 · VISION & SENSOR AI';
        centerGraphic = `
          <rect class="svg-viz-well" width="248" height="108" rx="10" stroke="#f59e0b66" stroke-width="1.2" />
          <path d="M 14 56 L 30 56 L 38 22 L 46 86 L 54 16 L 62 80 L 70 38 L 78 66 L 88 56 L 112 56" fill="none" stroke="#fbbf24" stroke-width="2.2" />
          <text x="16" y="97" class="svg-text-mono" font-size="9" font-weight="700">LIVE SIGNAL</text>
          <rect x="126" y="14" width="108" height="80" rx="6" fill="var(--svg-node-fill)" stroke="#38bdf8" stroke-width="1.5" />
          <rect x="148" y="28" width="64" height="40" rx="4" fill="rgba(244,63,94,0.2)" stroke="#f43f5e" stroke-width="1.8" stroke-dasharray="4 2" />
          <circle cx="180" cy="48" r="8" fill="rgba(244,63,94,0.48)" stroke="#f43f5e" stroke-width="1.5" />
          <text x="180" y="85" text-anchor="middle" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">CAUGHT LIVE</text>
        `;
      } else if (topology === 'spatial_wms_atp') {
        stage2Kicker = '2 · LIVE STOCK & BINS';
        stage3Kicker = '3 · 3D & ORDER SOLVER';
        centerGraphic = `
          <rect class="svg-viz-well" width="248" height="108" rx="10" stroke="#10b98166" stroke-width="1.2" />
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
          <text x="182" y="99" text-anchor="middle" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">OPTIMAL PATH</text>
        `;
      } else if (topology === 'multimodal_corridor_vrp') {
        stage2Kicker = '2 · LANE & SLOT CHECK';
        stage3Kicker = '3 · ROUTE & LOAD SOLVER';
        centerGraphic = `
          <rect class="svg-viz-well" width="248" height="108" rx="10" stroke="#38bdf866" stroke-width="1.2" />
          <path d="M 22 38 Q 76 10, 130 30 T 226 18" fill="none" stroke="#38bdf8" stroke-width="2.4" stroke-dasharray="4 2" />
          <circle cx="22" cy="38" r="5.5" fill="#f59e0b" />
          <circle cx="130" cy="30" r="5.5" fill="#38bdf8" />
          <circle cx="226" cy="18" r="6" fill="#10b981" />
          <rect x="22" y="56" width="150" height="32" rx="4" fill="var(--svg-node-fill)" stroke="#94a3b8" stroke-width="1.4" />
          <rect x="26" y="60" width="35" height="24" rx="2" fill="#10b981" />
          <rect x="65" y="60" width="35" height="24" rx="2" fill="#38bdf8" />
          <rect x="104" y="60" width="35" height="24" rx="2" fill="#fbbf24" />
          <text x="180" y="71" fill="#10b981" font-size="9.5" font-weight="800" font-family="var(--font-mono)">LEGAL SLOT</text>
          <text x="180" y="86" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">BEST ROUTE</text>
        `;
      } else if (topology === 'circular_warroom_triage') {
        stage2Kicker = '2 · EVIDENCE CHECK';
        stage3Kicker = '3 · DECISION ENGINE';
        centerGraphic = `
          <rect class="svg-viz-well" width="248" height="108" rx="10" stroke="#fb718566" stroke-width="1.2" />
          <path d="M 34 54 L 84 22 M 34 54 L 84 54 M 34 54 L 84 86" stroke="#94a3b8" stroke-width="2.2" />
          <circle cx="34" cy="54" r="13" fill="#f43f5e" />
          <text x="34" y="58" text-anchor="middle" fill="#ffffff" font-size="9" font-weight="800">AI</text>
          <rect x="84" y="10" width="148" height="24" rx="5" fill="rgba(16,185,129,0.18)" stroke="#10b981" stroke-width="1.4" />
          <text x="92" y="26" fill="#10b981" font-size="9.5" font-weight="800" font-family="var(--font-mono)">✓ BEST NET VALUE</text>
          <rect x="84" y="42" width="148" height="24" rx="5" fill="rgba(56,189,248,0.16)" stroke="#38bdf8" stroke-width="1.4" />
          <text x="92" y="58" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">• BACKUP PATH</text>
          <rect x="84" y="74" width="148" height="24" rx="5" fill="rgba(245,158,11,0.16)" stroke="#f59e0b" stroke-width="1.4" />
          <text x="92" y="90" fill="#fbbf24" font-size="9.5" font-weight="800" font-family="var(--font-mono)">• HUMAN REVIEW</text>
        `;
      } else {
        stage2Kicker = '2 · CHECK LIMITS';
        stage3Kicker = '3 · MATH OPTIMIZER';
        centerGraphic = `
          <rect class="svg-viz-well" width="248" height="108" rx="10" stroke="${cls.color}66" stroke-width="1.2" />
          <path d="M 24 20 C 30 72, 72 88, 134 92" fill="none" stroke="${cls.color}" stroke-width="2.6" />
          <circle cx="36" cy="46" r="5" fill="#38bdf8" />
          <circle cx="68" cy="74" r="6" fill="#10b981" stroke="#ffffff" stroke-width="1.6" />
          <circle cx="110" cy="88" r="5" fill="#fbbf24" />
          <text x="80" y="74" fill="#10b981" font-size="9.5" font-weight="800" font-family="var(--font-mono)">★ OPTIMAL</text>
          <circle cx="196" cy="54" r="28" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="6 3" />
          <circle r="4" fill="#10b981">
            <animateMotion dur="2.2s" repeatCount="indefinite" path="M 196 26 A 28 28 0 1 1 195.9 26" />
          </circle>
          <text x="196" y="58" text-anchor="middle" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">SOLVER</text>
        `;
      }

      return `
        <!-- Animated Connection Arrows Across the 4 Stages -->
        <path d="M 232 88 C 254 88, 254 132, 272 132" fill="none" stroke="${dept.color}" stroke-width="2.4" stroke-dasharray="5 3" />
        <path d="M 232 206 C 254 206, 254 164, 272 164" fill="none" stroke="#38bdf8" stroke-width="2.4" stroke-dasharray="5 3" />
        <circle r="4" fill="${dept.color}"><animateMotion dur="1.6s" repeatCount="indefinite" path="M 232 88 C 254 88, 254 132, 272 132" /></circle>
        <circle r="4" fill="#38bdf8"><animateMotion dur="1.9s" repeatCount="indefinite" path="M 232 206 C 254 206, 254 164, 272 164" /></circle>

        <path d="M 488 148 L 524 148" fill="none" stroke="#38bdf8" stroke-width="2.8" marker-end="url(#arrowCyan_${uid})" />
        <circle r="4" fill="#38bdf8"><animateMotion dur="1.4s" repeatCount="indefinite" path="M 488 148 L 524 148" /></circle>

        <path d="M 808 148 L 844 148" fill="none" stroke="#10b981" stroke-width="2.8" marker-end="url(#arrowGreen_${uid})" />
        <circle r="4" fill="#10b981"><animateMotion dur="1.4s" repeatCount="indefinite" path="M 808 148 L 844 148" /></circle>

        <!-- STAGE 1: TWO SIMPLE INPUT CARDS -->
        <g transform="translate(12, 32)">
          <rect class="svg-node-box" width="220" height="106" rx="16" stroke="${dept.color}" stroke-width="2" />
          <text x="16" y="28" font-size="16">${ic1}</text>
          <text x="40" y="26" fill="${dept.color}" font-size="10.5" font-weight="800" font-family="var(--font-mono)">1A · LIVE SIGNAL</text>
          <text x="16" y="56" class="svg-text-main" font-size="14" font-weight="800">${brief.s1a}</text>
          <text x="16" y="80" class="svg-text-sub" font-size="11.5">${brief.s1aSub}</text>
        </g>

        <g transform="translate(12, 156)">
          <rect class="svg-node-box" width="220" height="106" rx="16" stroke="#38bdf8" stroke-width="2" />
          <text x="16" y="28" font-size="16">${ic2}</text>
          <text x="40" y="26" fill="#38bdf8" font-size="10.5" font-weight="800" font-family="var(--font-mono)">1B · SYSTEM DATA</text>
          <text x="16" y="56" class="svg-text-main" font-size="14" font-weight="800">${brief.s1b}</text>
          <text x="16" y="80" class="svg-text-sub" font-size="11.5">${brief.s1bSub}</text>
        </g>

        <!-- STAGE 2: SIMPLE DATA CHECK + 2 ACTUAL TABLES -->
        <g transform="translate(272, 32)">
          <rect class="svg-node-box-alt" width="216" height="230" rx="16" stroke="#38bdf8" stroke-width="2.2" />
          <text x="16" y="28" fill="#38bdf8" font-size="10.5" font-weight="800" font-family="var(--font-mono)">🔍 ${stage2Kicker}</text>
          <text x="16" y="55" class="svg-text-main" font-size="14.5" font-weight="800">${brief.s2Title}</text>
          <text x="16" y="77" class="svg-text-sub" font-size="11.5">${brief.s2Sub}</text>

          <text x="16" y="106" class="svg-text-mono" font-size="9.5" font-weight="800">KEY TABLES JOINED</text>
          <rect class="svg-pill-bg" x="14" y="116" width="188" height="38" rx="9" stroke="rgba(56,189,248,0.4)" />
          <text x="24" y="140" fill="#38bdf8" font-size="11" font-weight="800" font-family="var(--font-mono)">🗄️ ${brief.p1}</text>

          <rect class="svg-pill-bg" x="14" y="164" width="188" height="38" rx="9" stroke="rgba(16,185,129,0.4)" />
          <text x="24" y="188" fill="#10b981" font-size="11" font-weight="800" font-family="var(--font-mono)">🗄️ ${brief.p2}</text>
        </g>

        <!-- STAGE 3: CORE AI & MATH ENGINE -->
        <g transform="translate(524, 18)">
          <rect class="svg-node-box-alt" width="284" height="258" rx="18" stroke="${cls.color}" stroke-width="2.5" />
          <rect x="16" y="14" width="252" height="26" rx="8" fill="${cls.color}22" stroke="${cls.color}" />
          <text x="142" y="31" text-anchor="middle" class="svg-text-main" font-size="10.5" font-weight="800" font-family="var(--font-mono)">🧠 ${stage3Kicker}</text>
          <text x="142" y="64" text-anchor="middle" class="svg-text-main" font-size="15" font-weight="800">${brief.s3Title}</text>

          <g transform="translate(18, 78)">
            ${centerGraphic}
          </g>

          <rect class="svg-pill-bg" x="18" y="202" width="248" height="36" rx="9" stroke="${cls.color}55" />
          <text x="142" y="225" text-anchor="middle" fill="${cls.color}" font-size="11.5" font-weight="800" font-family="var(--font-mono)">⚙️ ${brief.s3Tech}</text>
        </g>

        <!-- STAGE 4: GOVERNED ACTION & BUSINESS RESULT -->
        <g transform="translate(844, 32)">
          <rect class="svg-node-box-out" width="264" height="230" rx="16" stroke="#10b981" stroke-width="2.2" />
          <text x="16" y="28" fill="#10b981" font-size="10.5" font-weight="800" font-family="var(--font-mono)">⚡ 4 · ACTION &amp; RESULT</text>
          <text x="16" y="55" class="svg-text-main" font-size="14.5" font-weight="800">${brief.s4Title}</text>
          <text x="16" y="76" class="svg-text-sub" font-size="11.5">Owner: ${personaShort}</text>

          <rect class="svg-pill-bg" x="14" y="94" width="236" height="48" rx="10" stroke="#f59e0b66" />
          <text x="24" y="113" fill="#f59e0b" font-size="10" font-weight="800" font-family="var(--font-mono)">🛡️ POLICY GATE</text>
          <text x="24" y="131" class="svg-text-main" font-size="11" font-weight="700">${brief.s4Gate}</text>

          <rect class="svg-pill-bg" x="14" y="152" width="236" height="60" rx="10" stroke="#10b98166" />
          <text x="24" y="174" fill="#10b981" font-size="12.5" font-weight="800">🚀 ${badgeLabel}</text>
          <text x="24" y="196" class="svg-text-sub" font-size="11.5">Updates ${brief.s4Target}</text>
        </g>
      `;
    }

    function shortStepHeading(rawTitle, fallback) {
      const s = String(rawTitle || fallback || '').trim();
      const words = s.split(/\s+/).filter(Boolean);
      return words.length <= 4 ? s : words.slice(0, 4).join(' ');
    }

    function renderSimpleAgentArchitectureDiagram(ag, dept) {
      const adk = ag.adkImplementation || {};
      const spec = ag.adkSpec || {};
      const cls = getAgentBuildClassification(ag);
      const cleanName = cleanAgentName(ag.name);
      const topology = AGENT_TOPOLOGY_MAP[ag.id] || 'milp_pareto_loop';
      const tMeta = TOPOLOGY_META[topology] || TOPOLOGY_META.milp_pareto_loop;

      const rawSysArr = (spec.systems && spec.systems.length)
        ? spec.systems.map(s => s.name)
        : toSysArray(ag.systems);
      const sysArr = rawSysArr.map(s => toOpenTechLabel(s));
      const sys1 = sysArr[0] || 'Live Operational Feed';
      const sys2 = sysArr[1] || 'ERP & Digital Twin';

      const tables = (adk.fixtureTables || []).map(t => t.table_name);
      const rawSubs = (ag.subAgents && ag.subAgents.length >= 2)
        ? ag.subAgents.slice(0, 3)
        : [
            { name: 'Data Validator', role: 'Checks live signals' },
            { name: 'Optimization Engine', role: 'Selects best action' }
          ];
      const subs = rawSubs.map(sa => ({
        name: toOpenTechLabel(sa.name),
        role: toOpenTechLabel(sa.role)
      }));

      const rawCadence = (ag.costModel && ag.costModel.triggerCadence) || 'Live + 15-Min Sync';
      const shortCadence = String(rawCadence)
        .replace(/Event-Driven\s*\+\s*/i, 'Live + ')
        .replace(/Telemetry/i, 'Sync')
        .trim();
      const solverLabel = toOpenTechLabel(ag.solverStack || 'OR-Tools + Gemini');
      const writebackFull = toOpenTechLabel(ag.apiWriteback || 'ERP / WMS Update');

      const svgBody = renderFullTopologySvg(topology, {
        ag, dept, cls, cleanName,
        sys1, sys2,
        tables, subs, solverLabel, writebackFull
      });

      return `
        <div class="simple-arch-card">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
            <div>
              <div style="font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:3px;">
                ${tMeta.badge}
              </div>
              <h2 style="font-family:var(--font-display); font-size:23px; font-weight:800; color:var(--text-primary); margin:0;">
                Execution Flow — ${cleanName}
              </h2>
            </div>
            <span class="sc-spec-count-badge" style="font-size:11.5px;">
              ⏱️ ${shortCadence}
            </span>
          </div>

          <div class="ag-flow-canvas-wrap">
            <svg class="ag-flow-svg" viewBox="0 0 1120 288">
              <defs>
                <marker id="arrowAccent_${ag.id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 1 L 10 5 L 0 9 z" fill="${dept.color}" />
                </marker>
                <marker id="arrowGreen_${ag.id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 1 L 10 5 L 0 9 z" fill="#10b981" />
                </marker>
                <marker id="arrowCyan_${ag.id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8" />
                </marker>
              </defs>
              ${svgBody}
            </svg>
          </div>
        </div>
      `;
    }"""


def patch_html_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    # 1. Remove temporary prototype CSS block if present
    proto_css_start = "    /* === V2.6 EXECUTION FLOW PROTOTYPES (CURFEW ORCHESTRATOR SHOWCASE) === */"
    if proto_css_start in text:
        c_idx = text.index(proto_css_start)
        style_close = text.index("  </style>", c_idx)
        text = text[:c_idx] + text[style_close:]

    # 2. Replace from `const TOPOLOGY_META = {` through the end of `renderSimpleAgentArchitectureDiagram`
    start_marker = "    const TOPOLOGY_META = {"
    end_marker = "    function renderAgentFiveStepCards(ag, dept) {"
    if start_marker not in text or end_marker not in text:
        raise RuntimeError(f"Markers not found in {path}")

    s_idx = text.index(start_marker)
    e_idx = text.index(end_marker, s_idx)
    text = text[:s_idx] + NEW_FLOW_JS_BLOCK + "\n\n" + text[e_idx:]

    path.write_text(text, encoding="utf-8")


def validate_js_block() -> None:
    import json
    import subprocess

    catalog = json.loads((ROOT / "data" / "supply_chain_catalog.json").read_text(encoding="utf-8"))
    agent_ids = list(catalog["agents"].keys())
    js_check = (
        NEW_FLOW_JS_BLOCK
        + "\nconst ids = "
        + json.dumps(agent_ids)
        + ";\n"
        + """
const missing = ids.filter(id => !AGENT_FLOW_BRIEFS[id]);
if (missing.length) throw new Error("Missing briefs: " + missing.join(","));
const limits = { s1a: 23, s1aSub: 29, s1b: 23, s1bSub: 29, s2Title: 22, s2Sub: 29, p1: 20, p2: 20, s3Title: 26, s3Tech: 26, s4Title: 24, s4Gate: 33, s4Target: 23 };
for (const id of ids) {
  const b = AGENT_FLOW_BRIEFS[id];
  for (const [k, max] of Object.entries(limits)) {
    const v = String(b[k] || "").trim();
    if (!v || v.includes("…") || v.length > max) {
      throw new Error(`Length/ellipsis violation on ${id}.${k} (${v.length} > ${max}): "${v}"`);
    }
  }
}
console.log(`Validated ${ids.length}/60 agents: 0 JS syntax errors, 0 box overflows!`);
"""
    )
    subprocess.run(["node"], input=js_check, text=True, check=True)


def main() -> None:
    validate_js_block()
    index_path = ROOT / "index.html"
    patch_html_file(index_path)

    base = index_path.read_text(encoding="utf-8")
    for boot, fname in [
        ("window.__BOOT_PAGE__ = 'periodic';", "periodic_table.html"),
        ("window.__BOOT_PAGE__ = 'mindmap';", "mind_map.html"),
    ]:
        variant = base.replace("<script>", f"<script>\n    {boot}", 1)
        (ROOT / fname).write_text(variant, encoding="utf-8")

    for target_dir in [ROOT / "docs", ROOT / "zipline_dist"]:
        if target_dir.exists():
            for fname in ["index.html", "periodic_table.html", "mind_map.html"]:
                shutil.copy2(ROOT / fname, target_dir / fname)

    print("Updated index.html, periodic_table.html, mind_map.html, docs/*, and zipline_dist/* cleanly.")


if __name__ == "__main__":
    main()


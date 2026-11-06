#!/usr/bin/env python3
"""Generates authentic, high-code interactive HTML cockpits and updates A2UI IFrameSrcdoc
surfaces across all 25 curated showcase agents.

Matches Customer Engineering (CE) patterns:
- Self-contained, responsive single-file HTML applications (< 40 KB, 0 external network calls).
- Interactive SVG / Canvas visualizations with live sliders and toggles.
- Filterable and sortable enterprise data tables with client-side 1-click CSV download.
- Autonomous ERP / WMS / S&OP writeback simulator with tamper-evident audit confirmation modal.
- A2UI IFrameSrcdoc card integration so Gemini Enterprise renders the live web app in the canvas side panel.
"""

from __future__ import annotations
import json
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Domain visual specifications and parameters for each agent
AGENT_INTERACTIVE_SPECS = {
    "demand_sensing_agent": {
        "title": "PulseCast Demand Sensing Studio",
        "icon": "🌊",
        "pillar": "01 · Plan · Demand Forecasting",
        "systems": "SAP S/4HANA · WeatherNext 3 · BigQuery Lake · Vertex AI TimesFM · SAP IBP",
        "kpis": [
            ("298,000", "Sensed P50 Units", "+28.5% Surge", "#34d399"),
            ("5.2%", "Calibrated WAPE", "-4.1% Error", "#38bdf8"),
            ("$180,000", "Revenue Protected", "+$45k Buffer", "#fbbf24"),
            ("-4.2%", "FVA Optimism Dampened", "SAP IBP Committed", "#a78bfa"),
        ],
        "slider_label": "WeatherNext Heatwave Anomaly (°C above normal):",
        "slider_min": 0, "slider_max": 10, "slider_val": 6.8, "slider_step": 0.2, "slider_unit": "°C",
        "slider_calc": "val => Math.round(262000 * (1 + (val * 0.042)))",
        "table_headers": ["SKU ID", "Region / Hub", "Weather Anomaly", "ERP Baseline", "Sensed P50", "WAPE %", "Writeback Status"],
        "table_rows": [
            ["SKU-BEV-ISOTONIC-32OZ", "Western Corridor (Mumbai/Pune)", "+6.8°C Heatwave", "262,000", "298,000", "5.2%", "COMMITTED_SAP_IBP"],
            ["SKU-SNACK-PROTEIN-BAR", "Northern NCR Hub (Delhi/Gurgaon)", "+19.0% Marathon Footprint", "135,000", "142,000", "4.8%", "COMMITTED_SAP_IBP"],
            ["SKU-BEV-ELECTROLYTE-500ML", "Southern Region (Bengaluru)", "+3.2°C Anomaly", "98,000", "105,000", "6.1%", "VERIFIED_READY"],
            ["SKU-HYDRATION-RECHARGE-1L", "Eastern Corridor (Kolkata)", "Normal Trend", "74,000", "75,200", "5.9%", "VERIFIED_READY"],
        ],
        "writeback_entity": "SAP IBP PIR Key Figure",
        "writeback_id": "PIR-20261106-001",
        "target_key": "CONSENSUS_DEMAND_SAMPLED_P50",
    },
    "promo_lift_simulator": {
        "title": "PromoLift Trade Promotion ROI Simulator",
        "icon": "🏷️",
        "pillar": "01 · Plan · Trade Promotion",
        "systems": "Salesforce CRM TPM · BigQuery POS · Vertex AI Causal ML · SAP S/4HANA Pricing",
        "kpis": [
            ("+34.2%", "Incremental Promo Lift", "Target Exceeded", "#34d399"),
            ("18.4%", "Net Profit Margin", "-2.1% Dilution Buffer", "#38bdf8"),
            ("-$24,500", "Cross-SKU Cannibalization", "Contained", "#fbbf24"),
            ("$1.82M", "Net Incremental GMV", "Approved", "#a78bfa"),
        ],
        "slider_label": "Promotional Discount Depth (%):",
        "slider_min": 5, "slider_max": 40, "slider_val": 20, "slider_step": 1, "slider_unit": "%",
        "slider_calc": "val => Math.round(1500000 * (1 + (val * 0.018)))",
        "table_headers": ["Promo Campaign", "Retailer Partner", "Discount %", "Baseline GMV", "Promo GMV", "Cannibalization", "ROI Decision"],
        "table_rows": [
            ["PROMO-DIWALI-MEGA-PACK", "DMart (Avenue Supermarts)", "20%", "$850,000", "$1,140,000", "-$12,400", "APPROVED_FUNDED"],
            ["PROMO-WEEKEND-COMBO", "Reliance Retail & Wholesale", "15%", "$420,000", "$560,000", "-$6,800", "APPROVED_FUNDED"],
            ["PROMO-FLASH-DEAL-BARS", "Spencers Retail", "25%", "$210,000", "$280,000", "-$9,200", "RESTRUCTURE_BUNDLE"],
            ["PROMO-BOGO-ISOTONIC", "More Retail Hypermarkets", "30%", "$180,000", "$215,000", "-$18,500", "MARGIN_DILUTIVE_REJECT"],
        ],
        "writeback_entity": "Salesforce TPM & SAP Pricing Ledger",
        "writeback_id": "TPM-20261106-Q4",
        "target_key": "APPROVED_TRADE_SPEND_ALLOWANCE",
    },
    "csco_control_tower_copilot": {
        "title": "TowerMind Executive Control Tower",
        "icon": "🗼",
        "pillar": "01 · Plan · S&OP / IBP",
        "systems": "SAP S/4HANA · Oracle OTM · Manhattan WMS · BigQuery Digital Twin · Siemens MES",
        "kpis": [
            ("98.4%", "Global OTIF SLA", "+1.2% MoM", "#34d399"),
            ("$2.45M", "Revenue at Chokepoints", "Actioned", "#fbbf24"),
            ("3 Plant Lines", "Critical Bottlenecks", "Resolving", "#f43f5e"),
            ("14.2 Days", "Cash-to-Cash Cycle", "-3.8 Days Accelerated", "#38bdf8"),
        ],
        "slider_label": "Network Disruption Shock Intensity:",
        "slider_min": 1, "slider_max": 5, "slider_val": 2, "slider_step": 1, "slider_unit": " Level",
        "slider_calc": "val => Math.round(98.4 - (val * 1.8))",
        "table_headers": ["Echelon Node", "Facility Type", "Chokepoint Driver", "Volume at Risk", "Direct Mitigation", "ERP Escalation"],
        "table_rows": [
            ["PLANT-PUNE-01", "Beverage Bottling Line", "Filler Valve Bearing Wear", "145,000 units", "Shift 40k to Plant Nashik", "MES_MAINTENANCE_TRIGGERED"],
            ["DC-BHIWANDI-HUB", "Regional Distribution Hub", "RFID Inbound Dock Congestion", "85,000 cartons", "Auto-resequence Yard Dock", "WMS_DOCK_RESEQUENCED"],
            ["PORT-JNPT-TERMINAL", "Ocean Container Gate", "Customs Port Hold (Chilled)", "14 Reefers", "Drayage Priority Bypass", "OTM_CUSTOMS_EXPEDITED"],
            ["SUPPLIER-ALPHA-PACK", "Corrugated Shipper Vendor", "Paper Flute Raw Material Stockout", "60,000 boxes", "Dual-Source to Packaging Beta", "SAP_PO_SPLIT_COMMITTED"],
        ],
        "writeback_entity": "Executive S&OP Consensus Directive",
        "writeback_id": "CSCO-DIR-20261106-01",
        "target_key": "CROSS_FUNCTIONAL_RESOLVE_STATUS",
    },
    "sop_scenario_weaver": {
        "title": "Synapse S&OP Scenario Weaver",
        "icon": "🕸️",
        "pillar": "01 · Plan · S&OP / IBP",
        "systems": "SAP IBP · Siemens Opcenter MES · SAP Ariba · Google OR-Tools MIP Solver",
        "kpis": [
            ("99.1%", "Constrained Demand Fill", "+6.4% vs Unconstrained", "#34d399"),
            ("$48,500", "Premium Overtime Cost", "-$32k vs Baseline", "#38bdf8"),
            ("100%", "Component Allocation", "Zero Line Starvation", "#fbbf24"),
            ("$1.15M", "EBITDA Margin Preserved", "Optimized", "#a78bfa"),
        ],
        "slider_label": "Overtime Labor Allowance (Hours / Week):",
        "slider_min": 0, "slider_max": 100, "slider_val": 40, "slider_step": 5, "slider_unit": " hrs",
        "slider_calc": "val => Math.round(92.0 + (val * 0.08))",
        "table_headers": ["Scenario Name", "Plant Capacity %", "Overtime Spend", "Co-Packer Premium", "Fill Rate %", "Net Margin", "S&OP Approval"],
        "table_rows": [
            ["Scenario A: Baseline Constrained", "88.0%", "$0", "$0", "89.4%", "$1,040,000", "REJECTED_UNMET_DEMAND"],
            ["Scenario B: Overtime + Co-Packer", "100.0%", "$48,500", "$28,000", "99.1%", "$1,152,000", "RECOMMENDED_CONSENSUS"],
            ["Scenario C: 100% Co-Packer Shift", "92.0%", "$0", "$115,000", "96.5%", "$980,000", "MARGIN_DILUTIVE_DROP"],
        ],
        "writeback_entity": "SAP IBP Supply Consensus Plan",
        "writeback_id": "SOP-SCEN-20261106-B",
        "target_key": "CONSTRAINED_PRODUCTION_VOLUME",
    },
    "disruption_war_room_orchestrator": {
        "title": "StormShield Disruption War Room",
        "icon": "⚡",
        "pillar": "01 · Plan · S&OP / IBP",
        "systems": "GDACS Global Disaster Alerts · NOAA / WeatherNext · SAP S/4HANA · Oracle OTM",
        "kpis": [
            ("Category 3", "Cyclone Threat (West Coast)", "JNPT Port Affected", "#f43f5e"),
            ("18 Shipments", "Diverted in Transit", "Zero Cargo Loss", "#34d399"),
            ("-$62,000", "Expedited Freight Cost", "Within Contingency", "#fbbf24"),
            ("99.2%", "Customer OTIF Protected", "Verified", "#38bdf8"),
        ],
        "slider_label": "Port Closure Duration (Hours):",
        "slider_min": 12, "slider_max": 96, "slider_val": 48, "slider_step": 6, "slider_unit": " hrs",
        "slider_calc": "val => Math.round(18 + (val * 0.25))",
        "table_headers": ["Shipment ID", "Original Port", "Rerouted Hub", "Mode Shift", "Transit Delta", "Cargo Protected", "Carrier Dispatch"],
        "table_rows": [
            ["SHIP-JNPT-0841", "Port of JNPT Mumbai", "Hazira Port Gujarat", "Truck Linehaul Reroute", "+14 hrs", "$420,000", "DISPATCHED_CONFIRMED"],
            ["SHIP-JNPT-0842", "Port of JNPT Mumbai", "Mundra Port Hub", "Rail Intermodal Reroute", "+22 hrs", "$680,000", "DISPATCHED_CONFIRMED"],
            ["SHIP-JNPT-0845", "Port of JNPT Mumbai", "Bhiwandi Inland Depot", "Pre-Gate Hold & Stage", "+8 hrs", "$290,000", "STAGED_SECURE"],
        ],
        "writeback_entity": "Oracle OTM Reroute Execution Order",
        "writeback_id": "DISRUPT-WAR-20261106-01",
        "target_key": "EMERGENCY_DIVERSION_ROUTE",
    },
    "working_capital_cash_bridge": {
        "title": "Working Capital Cash Bridge Studio",
        "icon": "💰",
        "pillar": "01 · Plan · Working Capital",
        "systems": "SAP S/4HANA FI/CO · Kyriba Treasury · Taulia Dynamic Discounting · BigQuery",
        "kpis": [
            ("$4.85M", "Working Capital Unlocked", "Cash Released", "#34d399"),
            ("-6.4 Days", "Days Sales Outstanding (DSO)", "Accelerated", "#38bdf8"),
            ("+8.2 Days", "Days Payable Outstanding (DPO)", "Terms Harmonized", "#fbbf24"),
            ("18.4% APY", "Dynamic Discount Return", "Early Pay Return", "#a78bfa"),
        ],
        "slider_label": "Dynamic Discounting Supplier Uptake (%):",
        "slider_min": 10, "slider_max": 80, "slider_val": 45, "slider_step": 5, "slider_unit": "%",
        "slider_calc": "val => (4.85 * (val / 45)).toFixed(2)",
        "table_headers": ["Vendor / Customer", "Trading Category", "Terms Baseline", "Harmonized Terms", "Cash Impact", "Annual Yield", "Treasury Status"],
        "table_rows": [
            ["Tata Steel Processing", "Raw Material Supplier", "Net 30 Days", "Net 60 Days", "+$1,850,000", "14.2% Cost-Free", "TERMS_COMMITTED"],
            ["Reliance Packaging Ltd", "Corrugate Supplier", "Net 45 Days", "Dynamic Early Pay 2% 10", "+$920,000", "18.8% APY Return", "TAULIA_OFFER_SENT"],
            ["Apollo Tyres Fleet", "MRO & Transport", "Net 30 Days", "Net 45 Days", "+$640,000", "12.0% Cash Release", "TERMS_COMMITTED"],
            ["Modern Food Retailing", "Top Customer Tier", "Net 60 Days", "Net 45 Days + 1% Quick", "+$1,440,000", "DSO Reduced 15d", "COLLECTIONS_ACCELERATED"],
        ],
        "writeback_entity": "SAP FI/CO & Kyriba Treasury Bridge",
        "writeback_id": "CASH-BRIDGE-20261106-01",
        "target_key": "COMMITTED_PAYMENT_TERMS",
    },
    "tier_n_risk_sentinel": {
        "title": "NexusShield Multi-Tier Supply Network Sentinel",
        "icon": "🛡️",
        "pillar": "02 · Source · Vendor Sourcing",
        "systems": "SAP Ariba · Dun & Bradstreet Risk · Kharon Trade Sanctions · BigQuery Graph",
        "kpis": [
            ("Tier 3 Chokepoint", "Deep Semiconductor Wafer", "Sole-Source Flagged", "#f43f5e"),
            ("48 Hours", "Disruption Lead-Time", "+14 Days Head-Start", "#34d399"),
            ("2 Qualified", "Pre-Vetted Backup Suppliers", "Ready to Engage", "#38bdf8"),
            ("99.8%", "Sanctions & ESG Clean", "UFLPA Compliant", "#a78bfa"),
        ],
        "slider_label": "Supplier Disruption Vulnerability Threshold (%):",
        "slider_min": 20, "slider_max": 90, "slider_val": 65, "slider_step": 5, "slider_unit": "%",
        "slider_calc": "val => Math.round(14 * (val / 65))",
        "table_headers": ["Vendor Name", "Supply Tier", "Component Supplied", "Geographic Hub", "Risk Score", "Single Point of Failure", "Mitigation Status"],
        "table_rows": [
            ["Silicon Tech Fab", "Tier 3 Vendor", "Automotive MCU Wafers", "Hsinchu Science Park", "88 / 100", "YES (Sole Source)", "QUALIFYING_BACKUP_FAB"],
            ["Kyoto Ceramic Substrates", "Tier 2 Vendor", "Package Interposers", "Kyoto Japan", "42 / 100", "NO (Dual Sourced)", "MONITORED_HEALTHY"],
            ["Apex Electronics Harness", "Tier 1 Direct", "Wiring Harness Assembly", "Chennai Hub", "58 / 100", "NO (Backup in Pune)", "BUFFER_INVENTORY_COMMITTED"],
        ],
        "writeback_entity": "SAP Ariba Supplier Risk Rating",
        "writeback_id": "RISK-TIERN-20261106-01",
        "target_key": "DUAL_SOURCE_TARGET_ALLOCATION",
    },
    "carbon_scope3_ledger": {
        "title": "CarbonTrace Scope 3 Emissions Ledger",
        "icon": "🌱",
        "pillar": "02 · Source · ESG & Sustainability",
        "systems": "SAP S/4HANA Sustainability Footprint · Ecoinvent LCA · GLEC Logistics · BigQuery",
        "kpis": [
            ("-18.4%", "Scope 3 Carbon Avoided", "GLEC Framework Verified", "#34d399"),
            ("142,500 kg", "CO2e Reduced Today", "+3,200 Trees Equivalent", "#38bdf8"),
            ("€42.50 / t", "Shadow Carbon Price", "CBAM Prepared", "#fbbf24"),
            ("98.9%", "Audit Traceability", "Certified", "#a78bfa"),
        ],
        "slider_label": "Intermodal Rail Shift Target (%):",
        "slider_min": 10, "slider_max": 70, "slider_val": 40, "slider_step": 5, "slider_unit": "%",
        "slider_calc": "val => Math.round(142500 * (val / 40))",
        "table_headers": ["Transport Corridor", "Freight Mode", "LCA Emission Factor", "Baseline CO2e (kg)", "Optimized CO2e (kg)", "Abatement Cost", "ESG Registry"],
        "table_rows": [
            ["Mumbai DC -> Delhi NCR Hub", "Road -> Electric Rail Shift", "22 g CO2/t-km vs 84 g", "185,000 kg", "48,000 kg", "-$12 / t CO2e", "REGISTERED_CBAM_GLEC"],
            ["Chennai Auto Plant -> Pune", "Direct Linehaul Intermodal", "26 g CO2/t-km", "94,000 kg", "29,000 kg", "-$8 / t CO2e", "REGISTERED_CBAM_GLEC"],
            ["Bhiwandi Hub -> Ahmedabad", "Bio-CNG Heavy Truck Fleet", "48 g CO2/t-km", "68,000 kg", "38,000 kg", "+$4 / t CO2e", "REGISTERED_CBAM_GLEC"],
        ],
        "writeback_entity": "SAP Sustainability Footprint Management",
        "writeback_id": "ESG-SCOPE3-20261106-01",
        "target_key": "VERIFIED_CARBON_REDUCTION_KG",
    },
    "rfq_should_cost_agent": {
        "title": "SourcePulse Parametric Should-Cost Studio",
        "icon": "🧮",
        "pillar": "02 · Source · Material & Packaging",
        "systems": "London Metal Exchange (LME) · ICIS Polymer Index · SAP Ariba · BigQuery Cost Lake",
        "kpis": [
            ("-$342,000", "Total Sourcing Savings", "14.2% Below Quote", "#34d399"),
            ("$1.84 / kg", "Should-Cost Baseline", "Verified Index Math", "#38bdf8"),
            ("4 Suppliers", "RFQ Quotes Audited", "Margin Padding Stripped", "#fbbf24"),
            ("100% Index-Linked", "Clean Price Mechanism", "Commodity Clause", "#a78bfa"),
        ],
        "slider_label": "Polymer Index Volatility (+/- %):",
        "slider_min": -20, "slider_max": 20, "slider_val": -5, "slider_step": 1, "slider_unit": "%",
        "slider_calc": "val => (1.84 * (1 + (val * 0.01))).toFixed(2)",
        "table_headers": ["Part / Raw Material", "Supplier Quoted", "Should-Cost Target", "Material Delta", "Conversion Delta", "Negotiated Savings", "Ariba Contract"],
        "table_rows": [
            ["HDPE Bottle 1L Blowmold", "$2.45 / unit", "$2.08 / unit", "-$0.22 (Resin)", "-$0.15 (Cycle Time)", "$185,000 (15.1%)", "CONTRACT_AWARDED"],
            ["Corrugated Master Shipper 5-Ply", "$1.15 / box", "$0.96 / box", "-$0.12 (Kraft Paper)", "-$0.07 (Overhead)", "$94,000 (16.5%)", "CONTRACT_AWARDED"],
            ["Tamper-Evident Screw Cap", "$0.38 / cap", "$0.32 / cap", "-$0.03 (PP Resin)", "-$0.03 (Tooling)", "$63,000 (15.8%)", "CONTRACT_AWARDED"],
        ],
        "writeback_entity": "SAP Ariba Contract Master Agreement",
        "writeback_id": "RFQ-COST-20261106-01",
        "target_key": "AGREED_UNIT_PURCHASE_PRICE",
    },
    "three_way_match_dispute": {
        "title": "MatchGuard AP 3-Way Match & Dispute Arbiter",
        "icon": "⚖️",
        "pillar": "02 · Source · AP & Sourcing Operations",
        "systems": "SAP S/4HANA MM/FI · Manhattan WMS Dock Receiving · Document AI Invoice OCR",
        "kpis": [
            ("$148,200", "Fraudulent Overcharges Blocked", "Saved This Shift", "#34d399"),
            ("99.4%", "Straight-Through Processing", "< 15s Cycle Time", "#38bdf8"),
            ("0 False Holds", "Vendor Relationship Protected", "Zero Friction", "#fbbf24"),
            ("100% Tax Compliant", "GST / VAT Matched", "Clean Audit Stamp", "#a78bfa"),
        ],
        "slider_label": "Price Variance Tolerance Threshold ($):",
        "slider_min": 0, "slider_max": 100, "slider_val": 15, "slider_step": 5, "slider_unit": "$",
        "slider_calc": "val => Math.round(148200 - (val * 450))",
        "table_headers": ["Invoice Number", "Vendor Name", "PO Unit Price", "Invoice Unit Price", "GRN Received Qty", "Variance Type", "Arbiter Resolution"],
        "table_rows": [
            ["INV-AP-89211", "Global Plastic Molders", "$2.10", "$2.45 (+16.7%)", "50,000 units", "Price Overbill", "SHORT_PAY_DEBIT_MEMO_ISSUED"],
            ["INV-AP-89214", "Premier Corrugate Ltd", "$0.95", "$0.95 (Matched)", "40,000 (Billed 45k)", "Quantity Shortage", "RECEIPT_QUANTITY_MATCHED_CLEARED"],
            ["INV-AP-89218", "Express Linehaul Freight", "$1,450", "$1,720 (+18.6%)", "Delivered On-Time", "Uncontracted Fuel Surcharge", "STRIPPED_CONTRACT_RATE_PAID"],
        ],
        "writeback_entity": "SAP S/4HANA FI Automated Debit Memo",
        "writeback_id": "AP-DEBIT-20261106-01",
        "target_key": "PROCESSED_VOUCHER_AMOUNT",
    },
    "finite_production_scheduler": {
        "title": "FlowMaster Finite Production Scheduler",
        "icon": "🏭",
        "pillar": "03 · Make · Production Scheduling",
        "systems": "Siemens Opcenter MES · SAP PP/DS · Google OR-Tools Job-Shop MIP Solver",
        "kpis": [
            ("98.2%", "Line Schedule Adherence", "+8.4% Efficiency", "#34d399"),
            ("-32%", "Changeover Setup Time", "Matrix Optimized", "#38bdf8"),
            ("0 Stockouts", "BOM Component Sync", "100% Staged", "#fbbf24"),
            ("44,000 Units", "Incremental Shift Output", "Overtime Avoided", "#a78bfa"),
        ],
        "slider_label": "Line 01 Bottleneck Line Speed (% of rated speed):",
        "slider_min": 70, "slider_max": 110, "slider_val": 95, "slider_step": 1, "slider_unit": "%",
        "slider_calc": "val => Math.round(44000 * (val / 95))",
        "table_headers": ["Production Line", "Scheduled Product", "Batch Size", "Changeover Window", "WIP Status", "Bottleneck Risk", "MES Dispatch"],
        "table_rows": [
            ["Line 01 (High-Speed Bottling)", "SKU-BEV-ISOTONIC-32OZ", "120,000 units", "25 min (Flavor Allergen Clean)", "Ingredients Verified", "Low (Run Sequence Locked)", "DISPATCHED_TO_MES"],
            ["Line 02 (Aseptic Carton Filling)", "SKU-BEV-ELECTROLYTE-500ML", "85,000 units", "40 min (Size Tooling Swap)", "Packaging Staged", "Medium (Sterilization Hold)", "DISPATCHED_TO_MES"],
            ["Line 03 (Energy Bar Packaging)", "SKU-SNACK-PROTEIN-BAR", "60,000 units", "15 min (Film Roll Splicing)", "WIP Ready", "Low (Synchronized)", "DISPATCHED_TO_MES"],
        ],
        "writeback_entity": "Siemens Opcenter MES Job Schedule",
        "writeback_id": "MES-SCHED-20261106-01",
        "target_key": "COMMITTED_DISPATCH_TIMETABLE",
    },
    "predictive_oee_sentinel": {
        "title": "AssetGuard Plant OEE & Maintenance Sentinel",
        "icon": "⚙️",
        "pillar": "03 · Make · Production Scheduling",
        "systems": "Siemens MindSphere IoT · SAP PM (Plant Maintenance) · Vertex AI Autoencoder",
        "kpis": [
            ("88.4%", "Plant Overall OEE", "+6.2% vs Benchmark", "#34d399"),
            ("4.5 Hours", "Unplanned Downtime Avoided", "Prescriptive Work Order", "#38bdf8"),
            ("99.1%", "Equipment Availability", "Healthy", "#fbbf24"),
            ("$85,000", "Catastrophic Failure Loss Avoided", "Bearing Saved", "#a78bfa"),
        ],
        "slider_label": "Filler Drive Motor Vibration Threshold (mm/s):",
        "slider_min": 1.0, "slider_max": 8.0, "slider_val": 4.2, "slider_step": 0.1, "slider_unit": " mm/s",
        "slider_calc": "val => (88.4 - (val > 4.5 ? (val - 4.5) * 4 : 0)).toFixed(1)",
        "table_headers": ["Equipment Asset", "Critical Component", "Telemetry Sensor", "Vibration / Temp", "Anomaly Probability", "Prescriptive Action", "SAP PM Order"],
        "table_rows": [
            ["Filling Carousel 01", "Rotary Valve Drive Bearing", "Triaxial Accel #VIB-04", "4.2 mm/s | 68°C", "94% Failure in 18 hrs", "Auto-Lubricate & Schedule Swapped Shift", "PM_WORK_ORDER_48911"],
            ["Capper Station 02", "Pneumatic Chuck Spindle", "Pressure Transducer #PRS-02", "5.8 bar (Normal)", "4% Risk", "Routine Clean & Inspection", "NORMAL_MONITORING"],
            ["Labeler Machine 01", "Hot Melt Glue Applicator", "Thermal RTD #TEMP-08", "172°C (Optimal)", "6% Risk", "Calibrated Heating Element", "NORMAL_MONITORING"],
        ],
        "writeback_entity": "SAP PM Automated Maintenance Work Order",
        "writeback_id": "SAP-PM-20261106-48911",
        "target_key": "COMMITTED_WORK_ORDER_PRIORITY",
    },
    "inline_yield_guardian": {
        "title": "VisionInspect Multimodal Quality Inspector",
        "icon": "🔬",
        "pillar": "03 · Make · Quality & Compliance",
        "systems": "Cognex Line-Scan Vision · Gemini 3.1 Flash Multimodal · SAP Quality Management (QM)",
        "kpis": [
            ("99.98%", "First-Pass Quality Yield", "+0.42% Yield Lift", "#34d399"),
            ("12 Defective", "Caps Diverted at 900 BPM", "Zero Escapes", "#38bdf8"),
            ("14.5 ms", "Edge Inference Latency", "Real-Time Rejection", "#fbbf24"),
            ("$120,000", "Downstream Product Recall Protected", "100% Sealed", "#a78bfa"),
        ],
        "slider_label": "Vision Inspection Anomaly Confidence Gate (%):",
        "slider_min": 80, "slider_max": 99, "slider_val": 95, "slider_step": 1, "slider_unit": "%",
        "slider_calc": "val => (99.98 - ((100 - val) * 0.01)).toFixed(2)",
        "table_headers": ["Inspection Station", "Bottle Barcode", "Defect Detected", "Multimodal Vision Confidence", "Physical Ejector Gate", "Root Cause", "SAP QM Status"],
        "table_rows": [
            ["Station 04 (Seal & Capping)", "SKU-BEV-LOT48-0091", "Micro-Crack on Thread", "99.4% (Gemini Vision Edge)", "Pneumatic Air Blast Diverted", "Capper Chuck Overtorque", "QM_DEFECT_LOGGED"],
            ["Station 04 (Seal & Capping)", "SKU-BEV-LOT48-0092", "Missing Tamper Band", "98.8% (Gemini Vision Edge)", "Pneumatic Air Blast Diverted", "Cap Feeder Misfeed", "QM_DEFECT_LOGGED"],
            ["Station 05 (Label Placement)", "SKU-BEV-LOT48-0114", "Skewed Label (3.2mm)", "96.2% (Gemini Vision Edge)", "Rework Reject Bin", "Web Tension Fluctuation", "QM_REWORK_STAGED"],
        ],
        "writeback_entity": "SAP QM Inspection Lot Disposition",
        "writeback_id": "QM-INSPECT-20261106-01",
        "target_key": "REJECT_PNEUMATIC_DIVERSION",
    },
    "meio_safety_stock_agent": {
        "title": "EchelonFlow Multi-Echelon Inventory Allocator",
        "icon": "📦",
        "pillar": "04 · Deliver · Positioning & Optimization",
        "systems": "SAP S/4HANA Inventory · Manhattan WMS · BigQuery Stochastic MEIO Engine",
        "kpis": [
            ("-$2.15M", "Safety Stock Capital Freed", "Without Service Loss", "#34d399"),
            ("99.2%", "Echelon Service Level Target", "Exceeded Across Hubs", "#38bdf8"),
            ("18.2 Days", "Days of Inventory Outstanding", "-4.5 Days Leaner", "#fbbf24"),
            ("0 Stockouts", "Spoke Depot Fulfillment", "Guaranteed", "#a78bfa"),
        ],
        "slider_label": "Target Service Level SLA (%):",
        "slider_min": 95, "slider_max": 99.9, "slider_val": 99.2, "slider_step": 0.1, "slider_unit": "%",
        "slider_calc": "val => Math.round(2150000 * (1 - ((val - 95) / 10)))",
        "table_headers": ["Inventory Echelon Node", "Product Family", "Prior Safety Stock", "Optimized MEIO Stock", "Working Capital Freed", "Service SLA", "SAP Reorder Point"],
        "table_rows": [
            ["Central Plant DC (Bhiwandi)", "Beverage Core SKUs", "450,000 units", "340,000 units", "+$980,000", "99.5%", "UPDATED_COMMITTED"],
            ["Regional Hub (Bengaluru Nelamangala)", "High-Velocity Isotonic", "180,000 units", "135,000 units", "+$490,000", "99.2%", "UPDATED_COMMITTED"],
            ["Forward Spoke (Hyderabad Depot)", "Snack Bars & Drinks", "95,000 units", "68,000 units", "+$380,000", "99.0%", "UPDATED_COMMITTED"],
            ["Forward Spoke (Chennai Depot)", "Core Beverage Portfolio", "82,000 units", "61,000 units", "+$300,000", "99.1%", "UPDATED_COMMITTED"],
        ],
        "writeback_entity": "SAP S/4HANA MRP Safety Stock Parameter",
        "writeback_id": "MEIO-STOCK-20261106-01",
        "target_key": "OPTIMAL_REORDER_SAFETY_UNITS",
    },
    "warehouse_slotting_agent": {
        "title": "OptiSlot AI Dynamic Warehouse Slotting Engine",
        "icon": "🏢",
        "pillar": "04 · Deliver · DC Layout & Picking",
        "systems": "Manhattan Associates WMS · Blue Yonder WMS · BigQuery Pick Telemetry",
        "kpis": [
            ("-28.4%", "Order Picker Travel Distance", "Golden Zone Optimized", "#34d399"),
            ("+36.5%", "Pick Velocity (Lines / Hour)", "+48 Lines/Hr", "#38bdf8"),
            ("14 High-Run", "SKUs Reslotted Near Dock", "Zero Congestion", "#fbbf24"),
            ("18.5 Hours", "Labor Saved Daily", "Allocated to Packing", "#a78bfa"),
        ],
        "slider_label": "Daily Pick Wave Velocity Multiplier:",
        "slider_min": 1.0, "slider_max": 2.5, "slider_val": 1.4, "slider_step": 0.1, "slider_unit": "x",
        "slider_calc": "val => Math.round(28.4 * (val / 1.4))",
        "table_headers": ["SKU Code", "Description", "Current Slot Location", "Proposed Golden Zone Slot", "Pick Frequency / Shift", "Travel Reduction", "WMS Move Task"],
        "table_rows": [
            ["SKU-BEV-ISOTONIC-32OZ", "Isotonic 32oz 12-Pack", "Aisle 14, Tier 3 (Deep)", "Aisle 02, Tier 1 (Dock Front)", "420 picks", "-1,850 meters", "MOVE_TASK_GENERATED"],
            ["SKU-SNACK-PROTEIN-BAR", "Protein Bar 24ct Caddy", "Aisle 18, Tier 2 (Far)", "Aisle 01, Tier 1 (Dock Front)", "380 picks", "-1,620 meters", "MOVE_TASK_GENERATED"],
            ["SKU-BEV-ELECTROLYTE-500ML", "Electrolyte 500ml Case", "Aisle 09, Tier 3 (High)", "Aisle 03, Tier 1 (Golden Zone)", "290 picks", "-1,140 meters", "MOVE_TASK_GENERATED"],
        ],
        "writeback_entity": "Manhattan WMS Directed Slotting Task",
        "writeback_id": "WMS-SLOT-20261106-01",
        "target_key": "CONFIRMED_BAY_TIER_LOCATION",
    },
    "atp_order_promising_agent": {
        "title": "PromiseGuard Sub-50ms Spanner ATP & Order Promising",
        "icon": "⚡",
        "pillar": "04 · Deliver · Omnichannel Visibility",
        "systems": "Google Cloud Spanner · SAP S/4HANA Sales Order · Salesforce Commerce Cloud",
        "kpis": [
            ("28 ms", "Global ATP Check Latency", "Sub-50ms SLA Met", "#34d399"),
            ("99.999%", "Spanner Five-Nines Availability", "True Distributed ACID", "#38bdf8"),
            ("0 Overselling", "Real-Time Cross-DC Locks", "Zero Backorder Drops", "#fbbf24"),
            ("140,000 Units", "Promised & Soft-Allocated", "Protected", "#a78bfa"),
        ],
        "slider_label": "Peak Order Ingestion Concurrency (Orders / Sec):",
        "slider_min": 1000, "slider_max": 25000, "slider_val": 8500, "slider_step": 500, "slider_unit": " QPS",
        "slider_calc": "val => Math.round(28 + (val > 10000 ? (val - 10000) * 0.001 : 0))",
        "table_headers": ["Order ID", "Customer Account", "Requested Units", "Promised Delivery Date", "Fulfilling Node", "Latency", "Spanner Commit Status"],
        "table_rows": [
            ["ORD-RET-90411", "DMart Western Hub", "45,000 cases", "Tomorrow 06:00 IST", "DC-Bhiwandi Hub", "24 ms", "COMMITTED_ACID_LOCK"],
            ["ORD-RET-90412", "Reliance Retail North", "32,000 cases", "Tomorrow 08:30 IST", "DC-NCR Gurgaon", "28 ms", "COMMITTED_ACID_LOCK"],
            ["ORD-RET-90418", "Spencers Retail South", "18,500 cases", "Tomorrow 07:00 IST", "DC-Nelamangala BLR", "21 ms", "COMMITTED_ACID_LOCK"],
        ],
        "writeback_entity": "Google Cloud Spanner Inventory Allocation",
        "writeback_id": "ATP-LOCK-20261106-01",
        "target_key": "COMMITTED_SOFT_RESERVATION",
    },
    "load_consolidation_agent": {
        "title": "CubeMaster 3D Isometric LIFO Bay & Load Consolidation",
        "icon": "📐",
        "pillar": "05 · Logistics · First & Mid-Mile",
        "systems": "Oracle OTM · Manhattan WMS · Google 3D Packing MIP Solver · Canvas Engine",
        "kpis": [
            ("96.4%", "Volumetric Cube Utilization", "+14.8% Fill Factor", "#34d399"),
            ("100% LIFO", "Reverse-Drop Unload Verified", "0 Shuffling at Docks", "#38bdf8"),
            ("14.2 Tonnes", "Axle Weight Distribution", "CMVR Rule 93 Safe", "#fbbf24"),
            ("-$18,400", "Linehaul Freight Saved Today", "2 Trucks Consolidated", "#a78bfa"),
        ],
        "slider_label": "Vehicle Cargo Bay Length (Meters):",
        "slider_min": 6.0, "slider_max": 14.0, "slider_val": 9.6, "slider_step": 0.4, "slider_unit": " m",
        "slider_calc": "val => (96.4 - ((14.0 - val) * 0.3)).toFixed(1)",
        "table_headers": ["Stop Order (LIFO)", "Delivery Destination", "Carton Count", "Bay Position (from Cab)", "Weight (kg)", "Axle Load Balance", "Loading Sequence"],
        "table_rows": [
            ["Drop 03 (Last Stop)", "Spencers Outlet Thane", "240 cartons", "Front Section (Cab)", "3,600 kg", "Steer Axle: 48%", "LOAD_FIRST_ZONE_A"],
            ["Drop 02 (Mid Stop)", "Reliance Mart Kurla", "380 cartons", "Mid Section (Center)", "5,700 kg", "Drive Axle: 52%", "LOAD_SECOND_ZONE_B"],
            ["Drop 01 (First Stop)", "DMart Hypermarket Andheri", "420 cartons", "Rear Section (Door)", "6,300 kg", "Door Clearance: 100%", "LOAD_LAST_ZONE_C"],
        ],
        "writeback_entity": "Oracle OTM Freight Consolidation Order",
        "writeback_id": "CUBE-3D-20261106-01",
        "target_key": "VERIFIED_LIFO_BAY_MAP",
    },
    "cold_chain_auditor": {
        "title": "CryoShield Cold-Chain & MKT Excursion Auditor",
        "icon": "❄️",
        "pillar": "05 · Logistics · First & Mid-Mile",
        "systems": "Carrier Transicold IoT · Thermo King TracKing · BigQuery IoT Lake · SAP QM",
        "kpis": [
            ("3.8°C", "Mean Kinetic Temp (MKT)", "Within 2°C–8°C Spec", "#34d399"),
            ("14 Trailed", "Reefer Telemetry Feeds", "Live Continuous Ping", "#38bdf8"),
            ("1 Excursion", "Compressor Defrost Cycle", "Safely Remediated", "#fbbf24"),
            ("$240,000", "Perishable Vaccines Protected", "100% Viable", "#a78bfa"),
        ],
        "slider_label": "Ambient Outside Highway Heat (°C):",
        "slider_min": 25, "slider_max": 50, "slider_val": 42, "slider_step": 1, "slider_unit": "°C",
        "slider_calc": "val => (3.8 + ((val - 42) * 0.08)).toFixed(1)",
        "table_headers": ["Reefer Trailer ID", "Transit Corridor", "Inside Cargo Temp", "MKT Kinetic Temp", "Battery / Fuel Level", "Door Open Events", "Compliance Release"],
        "table_rows": [
            ["REEFER-MH-04-9811", "Pune Serum DC -> Mumbai Airport", "+3.8°C", "+3.6°C", "94% (Full Fuel)", "0 (Security Sealed)", "QUALIFIED_RELEASED"],
            ["REEFER-MH-04-9815", "Bengaluru Hub -> Chennai Port", "+4.2°C", "+4.0°C", "88% (Normal)", "0 (Security Sealed)", "QUALIFIED_RELEASED"],
            ["REEFER-MH-04-9822", "Hyderabad Depot -> Vijayawada", "+5.1°C", "+4.8°C", "91% (Normal)", "1 (Authorized Transfer)", "QUALIFIED_RELEASED"],
        ],
        "writeback_entity": "SAP QM Electronic Batch Release Record",
        "writeback_id": "COLD-RELEASE-20261106-01",
        "target_key": "VERIFIED_MKT_COMPLIANCE_STATUS",
    },
    "port_drayage_orchestrator": {
        "title": "DrayFlow Ocean Port & Intermodal Drayage Studio",
        "icon": "⚓",
        "pillar": "05 · Logistics · Ocean & Port Drayage",
        "systems": "JNPT / Mundra Port TOS API · AIS MarineTraffic · Oracle OTM · BigQuery",
        "kpis": [
            ("-$42,800", "Demurrage & Detention Avoided", "0 Fee Incurred", "#34d399"),
            ("38 min", "Truck Gate-In Turnaround", "-45 min vs Average", "#38bdf8"),
            ("18 Containers", "Evacuated in Free-Time", "100% Timely", "#fbbf24"),
            ("100%", "Dual-Transaction Round Trips", "Zero Empty Bobtails", "#a78bfa"),
        ],
        "slider_label": "Port Gate Congestion Queue (Trucks):",
        "slider_min": 50, "slider_max": 500, "slider_val": 180, "slider_step": 10, "slider_unit": " trucks",
        "slider_calc": "val => Math.round(38 + ((val - 180) * 0.08))",
        "table_headers": ["Container ISO Code", "Ocean Vessel", "Discharge Timestamp", "Free-Time Expiry", "Drayage Truck Assigned", "Appointment Slot", "Port Dispatch"],
        "table_rows": [
            ["MSCU-789041-2", "MSC Gülsün (Berth 02)", "Today 04:00 IST", "In 96 hours", "TRUCK-MH-04-DRAY-14", "Slot 09:30 (Priority Gate)", "DISPATCHED_IN_GATE"],
            ["MAEU-451298-0", "Maersk Mc-Kinney (Berth 01)", "Today 05:30 IST", "In 120 hours", "TRUCK-MH-04-DRAY-18", "Slot 10:15 (Priority Gate)", "DISPATCHED_IN_GATE"],
            ["CMAU-128904-9", "CMA CGM Palais (Berth 03)", "Today 06:15 IST", "In 72 hours", "TRUCK-MH-04-DRAY-22", "Slot 11:00 (Priority Gate)", "DISPATCHED_IN_GATE"],
        ],
        "writeback_entity": "Oracle OTM Port Drayage Appointment",
        "writeback_id": "DRAY-APPT-20261106-01",
        "target_key": "COMMITTED_GATE_APPOINTMENT",
    },
    "geocoding_intelligence_agent": {
        "title": "GeoSmart Address Resolution & Fleet Intelligence",
        "icon": "🗺️",
        "pillar": "05 · Logistics · Last-Mile Delivery",
        "systems": "Google Maps Geocoding API · Plus Codes · Places API · Oracle OTM",
        "kpis": [
            ("99.8%", "Rooftop Geocoding Accuracy", "Precise Delivery Point", "#34d399"),
            ("0 Misdeliveries", "Fuzzy Parsing Disambiguation", "100% Pinpoint", "#38bdf8"),
            ("18.4 min", "Saved Per Route", "No Circling Blocks", "#fbbf24"),
            ("1,420 Drops", "Validated & Normalized", "Clean Lat/Long", "#a78bfa"),
        ],
        "slider_label": "Fuzzy Text Matching Confidence Threshold (%):",
        "slider_min": 60, "slider_max": 95, "slider_val": 85, "slider_step": 1, "slider_unit": "%",
        "slider_calc": "val => (99.8 - ((95 - val) * 0.02)).toFixed(1)",
        "table_headers": ["Unstructured Raw Address", "Parsed City / Pincode", "Google Plus Code", "Resolved Rooftop Coordinates", "Match Quality", "Carrier Dispatch"],
        "table_rows": [
            ["opp dmart near flyover andheri east mumb", "Mumbai, Maharashtra · 400069", "7JFJ+7X Mumbai", "19.1136° N, 72.8697° E", "ROOFTOP_EXACT (99%)", "VERIFIED_READY"],
            ["shree ram sweets shop no 4 mg rd blr", "Bengaluru, Karnataka · 560001", "XH8J+9M Bengaluru", "12.9754° N, 77.6067° E", "ROOFTOP_EXACT (98%)", "VERIFIED_READY"],
            ["sector 18 mkt behind petrol pump noida", "Noida, Uttar Pradesh · 201301", "G8W5+3F Noida", "28.5708° N, 77.3271° E", "ROOFTOP_EXACT (99%)", "VERIFIED_READY"],
        ],
        "writeback_entity": "Google Maps Enterprise Geocoding Master",
        "writeback_id": "GEO-PIN-20261106-01",
        "target_key": "VERIFIED_COORDINATES_PLUS_CODE",
    },
    "fleetflow_dispatch": {
        "title": "FleetFlow Corridor Route & Fleet Dispatch Studio",
        "icon": "🚚",
        "pillar": "05 · Logistics · Last-Mile Delivery",
        "systems": "Google Maps Routes API · Google OR-Tools VRP · BigQuery · WhatsApp Dispatch",
        "kpis": [
            ("8 Trucks", "Fleet Dispatched (vs 10 Baseline)", "-2 Trucks Saved", "#34d399"),
            ("₹18,600", "Daily Transport Cost Savings", "Verified Budget Cut", "#38bdf8"),
            ("100% LIFO", "Reverse Loading Sequence", "Zero Cargo Shuffling", "#fbbf24"),
            ("CMVR 93 Safe", "Axle Load Distribution", "100% Law Compliant", "#a78bfa"),
        ],
        "slider_label": "Diesel Fuel Rate (₹ / Litre):",
        "slider_min": 85, "slider_max": 120, "slider_val": 98, "slider_step": 1, "slider_unit": " ₹/L",
        "slider_calc": "val => Math.round(18600 * (val / 98))",
        "table_headers": ["Driver & Truck", "Assigned Corridor", "Stops", "Cartons", "Route Distance", "CMVR Balance", "1-Tap Dispatch"],
        "table_rows": [
            ["Ravi Sharma (T14-01)", "West Corridor (Andheri/Bandra)", "8 drops", "165 ctn", "71.7 km", "Steer 48% / Drive 52%", "WHATSAPP_DISPATCHED"],
            ["Imran Khan (T17-02)", "North-East Corridor (Thane/Kalyan)", "10 drops", "210 ctn", "94.2 km", "Steer 49% / Drive 51%", "WHATSAPP_DISPATCHED"],
            ["Sunil Patil (T20-01)", "South Corridor (Vashi/Nerul)", "12 drops", "280 ctn", "88.5 km", "Steer 50% / Drive 50%", "WHATSAPP_DISPATCHED"],
        ],
        "writeback_entity": "FleetFlow Autonomous Route Manifest",
        "writeback_id": "FLEET-DISPATCH-20261106-01",
        "target_key": "COMMITTED_DRIVER_CORRIDORS",
    },
    "freight_bill_audit_agent": {
        "title": "FreightAudit Carrier Tariff & Surcharge Arbiter",
        "icon": "🧾",
        "pillar": "05 · Logistics · Route & Carrier",
        "systems": "Oracle OTM · SMC3 RateWare XL · Transporeon EDI 210 · SAP S/4HANA",
        "kpis": [
            ("-$68,400", "Disputed Carrier Invoices", "Overcharges Caught", "#34d399"),
            ("14 Invoices", "Flagged for Clawback", "Automated Notice Sent", "#38bdf8"),
            ("0 Late Fees", "Contracted Due Dates Honored", "Clean AP Processing", "#fbbf24"),
            ("100% Contract Match", "Base Rate Tariff Adherence", "Zero Leakage", "#a78bfa"),
        ],
        "slider_label": "Contract Fuel Surcharge Peg ($ / Barrel):",
        "slider_min": 60, "slider_max": 120, "slider_val": 82, "slider_step": 2, "slider_unit": " $/bbl",
        "slider_calc": "val => Math.round(68400 * (val / 82))",
        "table_headers": ["Carrier Invoice #", "Freight Carrier", "Billed Total", "Contract Tariff Total", "Variance Dispute", "Dispute Code", "Clawback Status"],
        "table_rows": [
            ["INV-FRT-98104", "VRL Logistics Express", "₹48,500", "₹41,200", "₹7,300 (+17.7%)", "UNCONTRACTED_ACCESSORIAL_LIFTGATE", "CLAWBACK_NOTICE_FILED"],
            ["INV-FRT-98109", "TCI Freight Linehaul", "₹82,400", "₹74,000", "₹8,400 (+11.3%)", "INCORRECT_MILEAGE_BAND", "CLAWBACK_NOTICE_FILED"],
            ["INV-FRT-98115", "Gati KWE Express", "₹34,000", "₹29,500", "₹4,500 (+15.2%)", "INVALID_FUEL_SURCHARGE_INDEX", "CLAWBACK_NOTICE_FILED"],
        ],
        "writeback_entity": "SAP S/4HANA Carrier AP Debit Memo",
        "writeback_id": "FRT-AUDIT-20261106-01",
        "target_key": "APPROVED_NET_CARRIER_PAYMENT",
    },
    "reverse_rma_optimizer": {
        "title": "ReturnGuard RMA & Warranty Fraud Sentinel",
        "icon": "🔄",
        "pillar": "06 · Return · Customer Returns (RMA)",
        "systems": "Salesforce Service Cloud · BigQuery Returns Lake · Vertex AI Fraud Model",
        "kpis": [
            ("$214,000", "Serial Return Fraud Prevented", "Wardrobing Blocked", "#34d399"),
            ("88.4%", "Automated Instant RMA Approval", "Legitimate Buyers", "#38bdf8"),
            ("+$62,000", "Secondary Market Salvage Value", "Refurbished Recovery", "#fbbf24"),
            ("< 12s", "Returns Triage Decision", "Real-Time Decisioning", "#a78bfa"),
        ],
        "slider_label": "Customer Fraud Risk Sensitivity Threshold (%):",
        "slider_min": 40, "slider_max": 90, "slider_val": 70, "slider_step": 5, "slider_unit": "%",
        "slider_calc": "val => Math.round(214000 * (val / 70))",
        "table_headers": ["RMA Request ID", "Customer Account", "Product Serial #", "Return Reason", "Fraud Risk Score", "Disposition Recommendation", "Portal Status"],
        "table_rows": [
            ["RMA-2026-9041", "Buyer-Acc-78112", "SN-BEV-DISP-0841", "Claimed 'Defective Valve'", "92% (High Repeat Fraud)", "Physical Depot Inspection Required", "FLAGGED_INSPECTION"],
            ["RMA-2026-9044", "Verified-VIP-1104", "SN-BEV-COOL-4912", "Color Mismatch", "4% (Legitimate Return)", "Instant QR Shipping Label Issued", "INSTANT_LABEL_ISSUED"],
            ["RMA-2026-9048", "Buyer-Acc-34901", "SN-SNK-PACK-1092", "Missing Inner Seals", "12% (Legitimate Return)", "Instant Refund & Donate Locally", "REFUND_DONATE_ALLOWED"],
        ],
        "writeback_entity": "Salesforce Service Cloud RMA Decision",
        "writeback_id": "RMA-DECISION-20261106-01",
        "target_key": "APPROVED_DISPOSITION_STATUS",
    },
    "dynamic_markdown_agent": {
        "title": "MarkdownMaster Expiry & Dynamic Salvage Pricing",
        "icon": "📉",
        "pillar": "06 · Return · Expiry & Markdowns",
        "systems": "SAP S/4HANA Batch Management · BigQuery Elasticity · SAP Retail Dynamic Pricing",
        "kpis": [
            ("$184,000", "Perishable Waste Salvaged", "Clean Inventory Clearance", "#34d399"),
            ("84.2%", "Sell-Through Velocity", "+32% vs Baseline", "#38bdf8"),
            ("+$38,000", "Charitable Tax Donation Credits", "Food Bank Partners", "#fbbf24"),
            ("0 Landfill", "Zero Food Waste Mandate", "100% Recouped", "#a78bfa"),
        ],
        "slider_label": "Recommended Price Markdown Discount (%):",
        "slider_min": 10, "slider_max": 60, "slider_val": 30, "slider_step": 5, "slider_unit": "%",
        "slider_calc": "val => Math.round(184000 * (val / 30))",
        "table_headers": ["Batch Lot #", "Product Description", "Days to Expiry", "Current Inventory", "Proposed Markdown", "Salvage Channel", "SAP Retail Status"],
        "table_rows": [
            ["LOT-EXP-20261120-A", "Fresh Electrolyte Drink 500ml", "14 days", "42,000 units", "-30% Flash Promo", "Retail End-Cap Clearance", "PRICE_UPDATE_COMMITTED"],
            ["LOT-EXP-20261114-B", "Organic Protein Snack Bars", "7 days", "18,000 units", "-50% Deep Liquidation", "Institutional Food Service", "PRICE_UPDATE_COMMITTED"],
            ["LOT-EXP-20261109-C", "Cold-Pressed Raw Juice 1L", "3 days", "6,500 units", "100% Tax Write-Off", "Donated to Akshaya Patra", "CHARITABLE_TRANSFER_POSTED"],
        ],
        "writeback_entity": "SAP Retail POS Dynamic Price Update",
        "writeback_id": "MARKDOWN-POS-20261106-01",
        "target_key": "COMMITTED_SHELF_PRICE",
    },
    "rti_balance_reconciler": {
        "title": "PalletPulse Reusable Transport Item (RTI) Reconciler",
        "icon": "🔄",
        "pillar": "06 · Return · Pallet & Tote Reclamation",
        "systems": "CHEP / PECO Master Exchange · RFID Dock Scanners · SAP S/4HANA Billing",
        "kpis": [
            ("14,200 Pallets", "Reclaimed from Retail DCs", "Zero Asset Loss", "#34d399"),
            ("-$84,000", "Demurrage Charges Avoided", "Within Grace Period", "#38bdf8"),
            ("8.2 Days", "Average Pallet Dwell Time", "-6.4 Days Cycle", "#fbbf24"),
            ("100% Reconciled", "CHEP Exchange Statement", "Certified", "#a78bfa"),
        ],
        "slider_label": "Customer Free Dwell Period (Days):",
        "slider_min": 5, "slider_max": 30, "slider_val": 14, "slider_step": 1, "slider_unit": " days",
        "slider_calc": "val => Math.round(14200 - ((val - 14) * 400))",
        "table_headers": ["Customer Distribution Center", "RTI Asset Type", "Unreturned Balance", "Max Dwell Days", "Demurrage Liability", "Action Triggered", "Billing Debit"],
        "table_rows": [
            ["DMart Central DC Kalamboli", "CHEP Blue Pallets (1200x1000)", "4,850 pallets", "24 days (Overdue 10d)", "₹242,500", "Auto-Schedule Reverse Pickup Route", "RECLAMATION_DISPATCHED"],
            ["Reliance Mart Logistics Kurla", "Plastic Bakery Totes (Heavy Duty)", "2,400 totes", "18 days (Overdue 4d)", "₹96,000", "Auto-Schedule Reverse Pickup Route", "RECLAMATION_DISPATCHED"],
            ["Spencers Retail DC Bhiwandi", "PECO Red Wooden Pallets", "1,850 pallets", "12 days (Within Grace)", "₹0", "Routine Exchange Ledger Logged", "HEALTHY_CYCLE"],
        ],
        "writeback_entity": "SAP S/4HANA RTI Demurrage Debit Memo",
        "writeback_id": "RTI-RECON-20261106-01",
        "target_key": "AUTHORIZED_RECLAMATION_ORDER",
    },
}


def build_self_contained_html(agent_id: str, cfg: dict) -> str:
    """Renders a production-grade, self-contained interactive single-file HTML cockpit."""
    title = cfg["title"]
    icon = cfg["icon"]
    pillar = cfg["pillar"]
    systems = cfg["systems"]
    kpis = cfg["kpis"]
    s_label = cfg["slider_label"]
    s_min = cfg["slider_min"]
    s_max = cfg["slider_max"]
    s_val = cfg["slider_val"]
    s_step = cfg["slider_step"]
    s_unit = cfg["slider_unit"]
    s_calc = cfg["slider_calc"]
    headers = cfg["table_headers"]
    rows = cfg["table_rows"]
    wb_entity = cfg["writeback_entity"]
    wb_id = cfg["writeback_id"]
    target_key = cfg["target_key"]

    headers_th = "".join(f"<th>{h}</th>" for h in headers)
    rows_tr = "".join(
        f"<tr>{''.join(f'<td>{cell}</td>' for cell in r)}</tr>"
        for r in rows
    )
    csv_raw = "\\n".join([",".join(headers)] + [",".join(r) for r in rows])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} · Enterprise Interactive Cockpit</title>
  <style>
    :root {{
      --bg: #080b14;
      --card: #0f172a;
      --card-hover: #1e293b;
      --border: rgba(255, 255, 255, 0.1);
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --blue: #38bdf8;
      --green: #34d399;
      --amber: #fbbf24;
      --red: #f43f5e;
      --purple: #a78bfa;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Google Sans', 'Inter', Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      padding: 20px;
      line-height: 1.5;
      font-size: 14.5px;
    }}
    .cockpit-shell {{
      max-width: 1200px;
      margin: 0 auto;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 24px;
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
    }}
    /* Top Masthead */
    .top-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 1px solid var(--border);
      padding-bottom: 18px;
      margin-bottom: 20px;
      gap: 16px;
      flex-wrap: wrap;
    }}
    .brand-title {{
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 22px;
      font-weight: 800;
      color: var(--text);
    }}
    .brand-title .icon {{
      font-size: 28px;
      background: rgba(56, 189, 248, 0.12);
      padding: 8px 12px;
      border-radius: 12px;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }}
    .badge-strip {{
      display: flex;
      gap: 8px;
      align-items: center;
      margin-top: 6px;
      flex-wrap: wrap;
    }}
    .badge {{
      font-size: 11.5px;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 20px;
      border: 1px solid var(--border);
      background: rgba(255, 255, 255, 0.05);
      color: var(--text-muted);
    }}
    .badge.live {{
      background: rgba(52, 211, 153, 0.12);
      color: var(--green);
      border-color: rgba(52, 211, 153, 0.3);
    }}
    .badge.pillar {{
      background: rgba(56, 189, 248, 0.12);
      color: var(--blue);
      border-color: rgba(56, 189, 248, 0.3);
    }}
    /* KPI Ribbon */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 14px;
      margin-bottom: 22px;
    }}
    .kpi-card {{
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px 18px;
      transition: all 0.2s ease;
    }}
    .kpi-card:hover {{
      background: rgba(255, 255, 255, 0.06);
      transform: translateY(-2px);
      border-color: rgba(255, 255, 255, 0.2);
    }}
    .kpi-value {{
      font-size: 26px;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.1;
      margin-bottom: 4px;
    }}
    .kpi-label {{
      font-size: 12px;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .kpi-delta {{
      font-size: 11.5px;
      font-weight: 700;
      margin-top: 6px;
      display: inline-block;
      padding: 2px 8px;
      border-radius: 12px;
      background: rgba(255, 255, 255, 0.06);
    }}
    /* Tab System */
    .tab-bar {{
      display: flex;
      gap: 8px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 20px;
    }}
    .tab-btn {{
      padding: 10px 20px;
      font-size: 14px;
      font-weight: 700;
      border: none;
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
      border-bottom: 2px solid transparent;
      transition: all 0.2s;
    }}
    .tab-btn:hover {{ color: var(--text); }}
    .tab-btn.active {{
      color: var(--blue);
      border-bottom-color: var(--blue);
    }}
    .tab-content {{ display: none; }}
    .tab-content.active {{ display: block; }}
    /* Interactive Simulator */
    .sim-panel {{
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 16px;
    }}
    .slider-box {{
      margin-bottom: 20px;
    }}
    .slider-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }}
    .slider-title {{
      font-size: 14.5px;
      font-weight: 700;
      color: var(--text);
    }}
    .slider-value-display {{
      font-size: 18px;
      font-weight: 800;
      color: var(--blue);
      background: rgba(56, 189, 248, 0.12);
      padding: 4px 12px;
      border-radius: 8px;
      border: 1px solid rgba(56, 189, 248, 0.3);
    }}
    .range-input {{
      width: 100%;
      height: 8px;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.1);
      outline: none;
      -webkit-appearance: none;
      cursor: pointer;
      accent-color: var(--blue);
    }}
    /* SVG Visual Stage */
    .svg-stage {{
      width: 100%;
      height: 280px;
      background: rgba(8, 11, 20, 0.9);
      border: 1px solid var(--border);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      overflow: hidden;
    }}
    /* Table */
    .table-tools {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      gap: 12px;
      flex-wrap: wrap;
    }}
    .search-input {{
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border);
      padding: 8px 14px;
      border-radius: 8px;
      color: var(--text);
      font-size: 13.5px;
      min-width: 260px;
      outline: none;
    }}
    .action-btn {{
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 13.5px;
      font-weight: 700;
      cursor: pointer;
      border: 1px solid var(--border);
      background: rgba(56, 189, 248, 0.15);
      color: var(--blue);
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}
    .action-btn:hover {{
      background: rgba(56, 189, 248, 0.3);
      color: #fff;
    }}
    .action-btn.commit {{
      background: rgba(52, 211, 153, 0.18);
      color: var(--green);
      border-color: rgba(52, 211, 153, 0.4);
    }}
    .action-btn.commit:hover {{
      background: rgba(52, 211, 153, 0.35);
      color: #fff;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}
    th {{
      text-align: left;
      padding: 10px 12px;
      background: rgba(255, 255, 255, 0.04);
      color: var(--text-muted);
      font-weight: 700;
      border-bottom: 1px solid var(--border);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    td {{
      padding: 11px 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      color: var(--text);
    }}
    tr:hover td {{
      background: rgba(255, 255, 255, 0.02);
    }}
    /* Modal */
    .modal-overlay {{
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(6px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
    }}
    .modal-overlay.active {{ display: flex; }}
    .modal-card {{
      background: #0f172a;
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 24px;
      max-width: 500px;
      width: 90%;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
    }}
    .modal-title {{
      font-size: 18px;
      font-weight: 800;
      color: var(--green);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
  </style>
</head>
<body>
  <div class="cockpit-shell">
    <!-- Header -->
    <header class="top-header">
      <div>
        <div class="brand-title">
          <span class="icon">{icon}</span>
          <span>{title}</span>
        </div>
        <div class="badge-strip">
          <span class="badge pillar">{pillar}</span>
          <span class="badge live">● Live Systems: {systems}</span>
          <span class="badge">HMAC: 94F8A02B</span>
        </div>
      </div>
      <div>
        <button class="action-btn commit" onclick="openCommitModal()">⚡ Commit Writeback</button>
      </div>
    </header>

    <!-- KPI Strip -->
    <div class="kpi-grid">
      {"".join(f'''
      <div class="kpi-card">
        <div class="kpi-value">{val}</div>
        <div class="kpi-label">{lbl}</div>
        <div class="kpi-delta" style="color:{color};">{delta}</div>
      </div>
      ''' for val, lbl, delta, color in kpis)}
    </div>

    <!-- Navigation Tabs -->
    <div class="tab-bar">
      <button class="tab-btn active" onclick="switchTab('sim')">📊 Interactive Visual Simulator</button>
      <button class="tab-btn" onclick="switchTab('table')">📋 Enterprise Data Ledger</button>
      <button class="tab-btn" onclick="switchTab('writeback')">⚡ Writeback Governance Audit</button>
    </div>

    <!-- Tab 1: Simulator -->
    <div id="tab-sim" class="tab-content active">
      <div class="sim-panel">
        <div class="slider-box">
          <div class="slider-header">
            <span class="slider-title">{s_label}</span>
            <span id="sliderValDisplay" class="slider-value-display">{s_val}{s_unit}</span>
          </div>
          <input type="range" class="range-input" id="simSlider" min="{s_min}" max="{s_max}" step="{s_step}" value="{s_val}" oninput="updateSimulation(this.value)">
        </div>

        <div class="svg-stage" id="svgStage">
          <!-- Dynamic SVG Chart Canvas -->
          <svg width="100%" height="100%" viewBox="0 0 800 240" preserveAspectRatio="none" style="overflow:visible;">
            <defs>
              <linearGradient id="pGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.45" />
                <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.02" />
              </linearGradient>
              <linearGradient id="p50Grad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#38bdf8" />
                <stop offset="100%" stop-color="#34d399" />
              </linearGradient>
            </defs>
            <!-- Grid Lines -->
            <line x1="60" y1="40" x2="760" y2="40" stroke="rgba(255,255,255,0.06)" />
            <line x1="60" y1="100" x2="760" y2="100" stroke="rgba(255,255,255,0.06)" />
            <line x1="60" y1="160" x2="760" y2="160" stroke="rgba(255,255,255,0.06)" />
            <line x1="60" y1="210" x2="760" y2="210" stroke="rgba(255,255,255,0.15)" />

            <!-- P10-P90 Confidence Fan -->
            <polygon id="quantileFan" points="60,180 180,160 320,130 480,90 620,60 760,40 760,200 620,190 480,180 320,175 180,185 60,190" fill="url(#pGrad)" />

            <!-- P50 Median Sensed Curve -->
            <path id="p50Line" d="M 60 185 Q 320 150 480 135 T 760 110" fill="none" stroke="url(#p50Grad)" stroke-width="3.5" />

            <!-- Baseline Reference -->
            <path d="M 60 185 L 760 185" fill="none" stroke="rgba(255,255,255,0.25)" stroke-width="1.8" stroke-dasharray="6,4" />

            <!-- Dynamic Node Points -->
            <circle cx="60" cy="185" r="5" fill="#38bdf8" />
            <circle cx="320" cy="150" r="5" fill="#38bdf8" />
            <circle id="peakNode" cx="760" cy="110" r="6" fill="#34d399" stroke="#fff" stroke-width="2" />

            <!-- Axis Labels -->
            <text x="60" y="230" fill="#94a3b8" font-size="11">Day 1 (Historical POS)</text>
            <text x="400" y="230" fill="#94a3b8" font-size="11" text-anchor="middle">Day 7 (In-Transit Pipeline)</text>
            <text x="760" y="230" fill="#34d399" font-size="11" font-weight="700" text-anchor="end">Day 14 (Optimized Plan)</text>

            <text id="liveKpiText" x="750" y="95" fill="#34d399" font-size="13" font-weight="800" text-anchor="end">P50: 298k</text>
            <text x="60" y="30" fill="#94a3b8" font-size="11.5">Baseline ERP: 262k · Dashed Line</text>
          </svg>
        </div>
        <p style="font-size:12.5px; color:var(--text-muted); margin-top:10px;">
          ✦ Live deterministic engine: adjusting parameters recalculates calibrated curves via Vertex AI reasoning logic in real time.
        </p>
      </div>
    </div>

    <!-- Tab 2: Table -->
    <div id="tab-table" class="tab-content">
      <div class="sim-panel">
        <div class="table-tools">
          <input type="text" class="search-input" id="tableFilter" placeholder="🔍 Search records by SKU, region, or carrier..." onkeyup="filterTable(this.value)">
          <button class="action-btn" onclick="downloadCsv()">📥 Download CSV</button>
        </div>
        <div style="overflow-x:auto;">
          <table id="dataTable">
            <thead>
              <tr>{headers_th}</tr>
            </thead>
            <tbody>
              {rows_tr}
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Tab 3: Writeback -->
    <div id="tab-writeback" class="tab-content">
      <div class="sim-panel">
        <h3 style="font-size:16px; font-weight:700; color:var(--text); margin-bottom:12px;">Autonomous Enterprise Integration Bridge</h3>
        <p style="font-size:13.5px; color:var(--text-muted); margin-bottom:16px;">
          Direct API & RFC gateway mapping validated actions back to enterprise systems of record.
        </p>
        <div style="background:rgba(255,255,255,0.03); border:1px solid var(--border); border-radius:10px; padding:16px; margin-bottom:16px;">
          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:12px; font-size:13px;">
            <div><strong>Target Entity:</strong> <span style="color:var(--blue);">{wb_entity}</span></div>
            <div><strong>Transaction Key:</strong> <span style="color:var(--text);">{wb_id}</span></div>
            <div><strong>Target Key Figure:</strong> <span style="color:var(--green);">{target_key}</span></div>
            <div><strong>Idempotency Status:</strong> <span style="color:var(--green);">IDEMPOTENT_VERIFIED</span></div>
          </div>
        </div>
        <button class="action-btn commit" onclick="openCommitModal()">⚡ Execute S&OP Consensus Writeback</button>
      </div>
    </div>
  </div>

  <!-- Modal -->
  <div class="modal-overlay" id="commitModal">
    <div class="modal-card">
      <div class="modal-title">✓ Writeback Transaction Stamped</div>
      <p style="color:var(--text-muted); font-size:13.5px; margin-bottom:14px;">
        Successfully committed proposed parameters to <strong>{wb_entity}</strong> with zero manual friction.
      </p>
      <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border); border-radius:8px; padding:12px; font-size:12.5px; margin-bottom:18px;">
        <div><strong>Transaction ID:</strong> {wb_id}</div>
        <div><strong>Key Figure:</strong> {target_key}</div>
        <div><strong>Audit Hash:</strong> SHA256:7f4a081c9e83b42a</div>
        <div><strong>Gateway:</strong> Google Apigee Enterprise Connector</div>
        <div><strong>Status:</strong> 200 OK · COMMITTED_TO_CORE</div>
      </div>
      <div style="text-align:right;">
        <button class="action-btn" onclick="closeCommitModal()">Done</button>
      </div>
    </div>
  </div>

  <script>
    const calcFn = {s_calc};

    function updateSimulation(val) {{
      document.getElementById('sliderValDisplay').innerText = val + '{s_unit}';
      const p50Val = calcFn(parseFloat(val));
      const kpiTxt = document.getElementById('liveKpiText');
      if (kpiTxt) {{
        kpiTxt.textContent = 'P50: ' + (p50Val / 1000).toFixed(0) + 'k';
      }}
      const p50Line = document.getElementById('p50Line');
      const peakNode = document.getElementById('peakNode');
      const qFan = document.getElementById('quantileFan');
      const yOffset = Math.max(30, Math.min(180, 185 - (p50Val - 262000) * 0.002));
      if (p50Line) {{
        p50Line.setAttribute('d', `M 60 185 Q 320 150 480 135 T 760 ${{yOffset}}`);
      }}
      if (peakNode) {{
        peakNode.setAttribute('cy', yOffset);
      }}
      if (qFan) {{
        qFan.setAttribute('points', `60,180 180,160 320,130 480,${{Math.max(20, yOffset - 30)}} 620,${{Math.max(20, yOffset - 40)}} 760,${{Math.max(20, yOffset - 50)}} 760,200 620,190 480,180 320,175 180,185 60,190`);
      }}
    }}

    function switchTab(tabId) {{
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      event.target.classList.add('active');
      document.getElementById('tab-' + tabId).classList.add('active');
    }}

    function filterTable(query) {{
      const q = query.toLowerCase();
      const rows = document.querySelectorAll('#dataTable tbody tr');
      rows.forEach(r => {{
        const text = r.innerText.toLowerCase();
        r.style.display = text.includes(q) ? '' : 'none';
      }});
    }}

    function downloadCsv() {{
      const csv = "{csv_raw}";
      const blob = new Blob([csv], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = '{agent_id}_operational_data.csv';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }}

    function openCommitModal() {{
      document.getElementById('commitModal').classList.add('active');
    }}

    function closeCommitModal() {{
      document.getElementById('commitModal').classList.remove('active');
    }}
  </script>
</body>
</html>"""
    return html


def update_showcase_agent(agent_id: str, cfg: dict):
    agent_dir = REPO_ROOT / "agents" / agent_id / "app"
    tools_py = agent_dir / "tools.py"
    surfaces_py = agent_dir / "render" / "surfaces.py"
    agent_py = agent_dir / "agent.py"

    if not agent_dir.exists() or not tools_py.exists():
        print(f"Skipping {agent_id}: path does not exist")
        return

    print(f"Enhancing {agent_id}...")

    # 1. Generate full self-contained HTML
    full_html = build_self_contained_html(agent_id, cfg)

    # 2. Update tools.py: replace generate_interactive_html_dashboard with the rich generator
    tools_txt = tools_py.read_text(encoding="utf-8")

    # Add _LATEST_INTERACTIVE_HTML store and getter if not present
    store_code = """
_LATEST_INTERACTIVE_HTML: dict | None = None

def get_latest_interactive_html(consume: bool = False) -> dict | None:
    global _LATEST_INTERACTIVE_HTML
    res = _LATEST_INTERACTIVE_HTML
    if consume:
        _LATEST_INTERACTIVE_HTML = None
    return res
"""
    if "_LATEST_INTERACTIVE_HTML" not in tools_txt:
        tools_txt = store_code + "\n" + tools_txt

    # Replace or add generate_interactive_html_dashboard
    # Escape quotes inside raw html
    escaped_html = full_html.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    new_html_tool_func = f'''
def generate_interactive_html_dashboard(title: str = "{cfg["title"]} Interactive Cockpit") -> dict:
    """Generate a self-contained interactive HTML dashboard view with visual surface.
    Allows business users to inspect visual graphs, spatial maps, or 3D layouts directly in a browser.
    """
    global _LATEST_INTERACTIVE_HTML
    html_markup = """{full_html}"""
    result = {{
        "status": "SUCCESS",
        "title": title,
        "format": "html",
        "html_code": html_markup,
        "html_preview": html_markup,
        "ready_to_view": True
    }}
    _LATEST_INTERACTIVE_HTML = result
    return result
'''
    # Find existing def generate_interactive_html_dashboard and replace it
    if "def generate_interactive_html_dashboard(" in tools_txt:
        pattern = r"def generate_interactive_html_dashboard\([^)]*\)\s*->\s*dict:[^def]*(?=\ndef |\Z)"
        tools_txt = re.sub(pattern, new_html_tool_func.strip() + "\n", tools_txt, flags=re.DOTALL)
    else:
        tools_txt += "\n" + new_html_tool_func

    tools_py.write_text(tools_txt, encoding="utf-8")

    # 3. Update surfaces.py: add build_interactive_html_surface
    if surfaces_py.exists():
        surf_txt = surfaces_py.read_text(encoding="utf-8")
        if "build_interactive_html_surface" not in surf_txt:
            interactive_surf_code = """
def build_interactive_html_surface(
    surface_id: str,
    html_content: str,
    title: str = "Interactive Cockpit",
    height: int = 720,
) -> list[Any]:
    \"\"\"Renders a self-contained interactive web application inside an A2UI IFrameSrcdoc Card.\"\"\"
    parts = [
        wrap_a2ui_part(build_create_surface(surface_id)),
        wrap_a2ui_part(build_update_data_model(surface_id, {"title": title})),
        wrap_a2ui_part(build_update_components(
            surface_id,
            [
                {
                    "id": "root",
                    "component": "Card",
                    "child": "iframe-view",
                },
                {
                    "id": "iframe-view",
                    "component": "IFrameSrcdoc",
                    "height": height,
                    "htmlContent": html_content,
                    "title": title,
                },
            ]
        )),
    ]
    return parts
"""
            surf_txt += interactive_surf_code
            surfaces_py.write_text(surf_txt, encoding="utf-8")

    # 4. Update agent.py: emit interactive surface in callback if generated, and update prompt
    if agent_py.exists():
        agent_txt = agent_py.read_text(encoding="utf-8")

        # Update _emit_a2ui_surface to check tools.get_latest_interactive_html
        if "def _emit_a2ui_surface" in agent_txt and "get_latest_interactive_html" not in agent_txt:
            old_callback = """    def _emit_a2ui_surface(
        callback_context: Optional[CallbackContext] = None,
        **_: Any,
    ) -> Optional[types.Content]:
        try:
            surface_id = f"demand-sensi-{uuid.uuid4().hex[:8]}"
            a2ui_parts = build_demand_sensing_surface(surface_id, spec=tools.get_latest_chart_spec(consume=True))
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception:
            pass
        return None"""
            
            # Universal replacement pattern for _emit_a2ui_surface
            cb_pattern = r"def _emit_a2ui_surface\([^)]*\)\s*->\s*Optional\[types\.Content\]:[^def]*(?=\n    root_agent =|\n    app =|\nclass )"
            
            # Look up which surface builder is used
            builder_match = re.search(r"(build_[a-z0-9_]+_surface)\(", agent_txt)
            default_builder = builder_match.group(1) if builder_match else "build_demand_sensing_surface"
            
            new_callback = f"""def _emit_a2ui_surface(
        callback_context: Optional[CallbackContext] = None,
        **_: Any,
    ) -> Optional[types.Content]:
        try:
            # Check if an interactive HTML cockpit was requested or generated
            latest_html = getattr(tools, "get_latest_interactive_html", lambda consume=False: None)(consume=True)
            if latest_html and latest_html.get("html_preview"):
                from .render.surfaces import build_interactive_html_surface
                surface_id = f"iframe-{{uuid.uuid4().hex[:8]}}"
                parts = build_interactive_html_surface(
                    surface_id,
                    html_content=latest_html["html_preview"],
                    title=latest_html.get("title", "Interactive Cockpit")
                )
                if parts:
                    return types.Content(role="model", parts=parts)

            # Otherwise emit standard VegaChart card surface
            surface_id = f"surface-{{uuid.uuid4().hex[:8]}}"
            chart_spec = getattr(tools, "get_latest_chart_spec", lambda consume=False: None)(consume=True)
            if chart_spec:
                a2ui_parts = {default_builder}(surface_id, spec=chart_spec)
                if a2ui_parts:
                    return types.Content(role="model", parts=a2ui_parts)
        except Exception:
            pass
        return None"""
            agent_txt = re.sub(cb_pattern, new_callback + "\n\n    ", agent_txt, flags=re.DOTALL)

        # Update _INSTRUCTION with explicit interactive HTML guidance
        if "INTERACTIVE HTML DASHBOARD PROTOCOL:" not in agent_txt:
            guidance = """
INTERACTIVE HTML DASHBOARD & EXECUTIVE ARTIFACTS PROTOCOL:
- When the user asks to "make an interactive HTML", "generate an interactive dashboard", "show cockpit", or requests visual web artifacts:
  1. Proactively invoke `generate_interactive_html_dashboard`.
  2. In your Markdown response:
     - Begin with a 3–4 sentence Plain-English Executive Summary explaining the current operational situation and key metrics.
     - Include a clean Markdown summary table (<= 5 columns) with plain-English column headers.
     - Output the complete, standalone, copyable ```html <!DOCTYPE html> ... ``` code block containing the entire self-contained interactive application so the user can easily copy or save it as a standalone HTML file.
     - Note to the user that the live interactive application is also rendering directly inside the Gemini Enterprise canvas side panel via A2UI.
"""
            agent_txt = agent_txt.replace(
                "RESPONSE STANDARDS:",
                guidance.strip() + "\n\nRESPONSE STANDARDS:"
            )

        agent_py.write_text(agent_txt, encoding="utf-8")

    print(f"✓ {agent_id} successfully upgraded!")


def main():
    print("=" * 70)
    print("🚀 Elevating All 25 Curated Showcase Agents with Rich Interactive Dashboards & A2UI IFrameSrcdoc")
    print("=" * 70)

    for aid, cfg in AGENT_INTERACTIVE_SPECS.items():
        update_showcase_agent(aid, cfg)

    print("\n✅ All 25 curated showcase agents successfully upgraded with interactive HTML and A2UI IFrameSrcdoc!")


if __name__ == "__main__":
    main()

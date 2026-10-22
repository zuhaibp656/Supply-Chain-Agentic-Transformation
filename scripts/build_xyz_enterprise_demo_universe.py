#!/usr/bin/env python3
"""Builds the comprehensive 'Aetherion / XYZ Corporation' Multi-Modal Enterprise Demo Data Universe.

Creates a realistic, interconnected corporate data ecosystem ("XYZ Global Industries Corp.")
spanning BOTH data inside the 35 supply chain agents AND broader enterprise organizational data
outside individual agents (ERP master data, HR plant shift rosters, Finance GL cost centers,
facility leases, legal MSAs, carrier contracts, X12 EDI streams, unstructured emails,
multi-tab Excel workbooks, multi-page PDFs, Word .docx SOPs, and high-res industrial images)
so all 35 agents across all 6 SCOR Pillars + Universal Core operate in tandem on shared IDs.

Output Structure (`demo_data/xyz_corporation/`):
  - `excel/`  : 7 multi-tab .xlsx workbooks (28+ worksheets total)
  - `pdfs/`   : 7 multi-page formatted .pdf enterprise documents (contracts, COAs, invoices, eBHR, CBAM, PODs)
  - `images/` : 8 high-resolution .png operational & computer-vision images (QR cartons, inline defects, RMA grading, shelf audit, FFT vibration, EUDR satellite, typhoon AIS radar, 3D LIFO bay)
  - `docs/`   : 4 Microsoft Word .docx SOPs & policy manuals + .eml unstructured emails + .edi X12 streams
  - `tables/` : 12 cross-enterprise master & organizational tables (.json & .csv) + unified `xyz_enterprise_manifest.json`
"""

from __future__ import annotations

import csv
import io
import json
import math
import os
import time
import zipfile
from pathlib import Path
from typing import Any, Dict, List

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "demo_data" / "xyz_corporation"

COMPANY_NAME = "XYZ Global Industries Corp."
COMPANY_CODE = "XYZ-CORP-01"
FISCAL_YEAR = "FY2026"

# ==============================================================================
# 1. Shared Golden-Thread Enterprise Master Data (Inside + Outside Agents)
# ==============================================================================
ENTERPRISE_SKUS = [
    {
        "sku_id": "SKU-XYZ-101",
        "material_number_sap": "MAT-1000841",
        "product_name": "CryoCell Pro 800V Thermal Battery Module",
        "business_unit": "Industrial Power & Mobility",
        "product_family": "EV & Grid Storage",
        "uom": "EA",
        "unit_cost_usd": 420.00,
        "list_price_usd": 685.00,
        "gross_margin_pct": 38.7,
        "weight_kg": 18.5,
        "dimensions_cm": "60x40x25",
        "crush_fragility_index": 0.35,
        "hazmat_class": "UN3480-CLASS9",
        "primary_plant_id": "PLANT-XYZ-STUTTGART",
        "secondary_plant_id": "PLANT-XYZ-AUSTIN",
        "lead_time_days": 14,
        "abc_velocity_tier": "A",
        "hs_tariff_code": "8507.60.0020",
        "cbam_carbon_kg_co2e": 64.2,
    },
    {
        "sku_id": "SKU-XYZ-204",
        "material_number_sap": "MAT-2000319",
        "product_name": "Aseptic HydraPure Electrolyte Beverage (24-Pack Case)",
        "business_unit": "Consumer Health & Beverages",
        "product_family": "Aseptic Cold-Fill Drinks",
        "uom": "CASE",
        "unit_cost_usd": 14.80,
        "list_price_usd": 28.50,
        "gross_margin_pct": 48.1,
        "weight_kg": 12.4,
        "dimensions_cm": "40x30x22",
        "crush_fragility_index": 0.72,
        "hazmat_class": "NONE-FOOD-GRADE",
        "primary_plant_id": "PLANT-XYZ-AUSTIN",
        "secondary_plant_id": "PLANT-XYZ-BENGALURU",
        "lead_time_days": 5,
        "abc_velocity_tier": "A",
        "hs_tariff_code": "2202.99.9000",
        "cbam_carbon_kg_co2e": 3.8,
    },
    {
        "sku_id": "SKU-XYZ-309",
        "material_number_sap": "MAT-3000512",
        "product_name": "Precision CNC Servo-Hydraulic Valve Manifold",
        "business_unit": "Industrial Automation",
        "product_family": "Hydraulic Actuators",
        "uom": "EA",
        "unit_cost_usd": 310.00,
        "list_price_usd": 540.00,
        "gross_margin_pct": 42.6,
        "weight_kg": 9.2,
        "dimensions_cm": "35x25x20",
        "crush_fragility_index": 0.15,
        "hazmat_class": "NONE",
        "primary_plant_id": "PLANT-XYZ-STUTTGART",
        "secondary_plant_id": "PLANT-XYZ-MONTERREY",
        "lead_time_days": 21,
        "abc_velocity_tier": "B",
        "hs_tariff_code": "8481.20.0050",
        "cbam_carbon_kg_co2e": 29.4,
    },
    {
        "sku_id": "SKU-XYZ-412",
        "material_number_sap": "MAT-4000908",
        "product_name": "OmniSense Edge IoT Cold-Chain Telemetry Gateway",
        "business_unit": "Connected Supply Chain Devices",
        "product_family": "Industrial IoT",
        "uom": "EA",
        "unit_cost_usd": 185.00,
        "list_price_usd": 349.00,
        "gross_margin_pct": 47.0,
        "weight_kg": 1.8,
        "dimensions_cm": "24x18x10",
        "crush_fragility_index": 0.85,
        "hazmat_class": "UN3481-LITHIUM-CELL",
        "primary_plant_id": "PLANT-XYZ-BENGALURU",
        "secondary_plant_id": "PLANT-XYZ-AUSTIN",
        "lead_time_days": 12,
        "abc_velocity_tier": "A",
        "hs_tariff_code": "8517.62.0090",
        "cbam_carbon_kg_co2e": 11.6,
    },
    {
        "sku_id": "SKU-XYZ-518",
        "material_number_sap": "MAT-5000774",
        "product_name": "AeroFlex Aluminum Brazed Heat Exchanger Core",
        "business_unit": "Thermal Management Systems",
        "product_family": "HVAC & Powertrain Cooling",
        "uom": "EA",
        "unit_cost_usd": 142.50,
        "list_price_usd": 245.00,
        "gross_margin_pct": 41.8,
        "weight_kg": 6.4,
        "dimensions_cm": "50x35x18",
        "crush_fragility_index": 0.65,
        "hazmat_class": "NONE",
        "primary_plant_id": "PLANT-XYZ-MONTERREY",
        "secondary_plant_id": "PLANT-XYZ-STUTTGART",
        "lead_time_days": 10,
        "abc_velocity_tier": "B",
        "hs_tariff_code": "8419.50.5000",
        "cbam_carbon_kg_co2e": 41.2,
    },
    {
        "sku_id": "SKU-XYZ-625",
        "material_number_sap": "MAT-6000215",
        "product_name": "EcoGrip Vulcanized Natural Rubber Vibration Mount (Box of 50)",
        "business_unit": "Elastomers & Acoustic Dampening",
        "product_family": "EUDR Certified Elastomers",
        "uom": "BOX",
        "unit_cost_usd": 88.00,
        "list_price_usd": 156.00,
        "gross_margin_pct": 43.6,
        "weight_kg": 14.0,
        "dimensions_cm": "45x30x25",
        "crush_fragility_index": 0.10,
        "hazmat_class": "NONE-EUDR-VERIFIED",
        "primary_plant_id": "PLANT-XYZ-BENGALURU",
        "secondary_plant_id": "PLANT-XYZ-MONTERREY",
        "lead_time_days": 18,
        "abc_velocity_tier": "C",
        "hs_tariff_code": "4016.99.3500",
        "cbam_carbon_kg_co2e": 8.9,
    },
]

ENTERPRISE_FACILITIES = [
    {
        "facility_id": "PLANT-XYZ-STUTTGART",
        "facility_name": "XYZ Stuttgart Gigafactory & Precision Machining Plant",
        "facility_type": "MANUFACTURING_PLANT",
        "region": "EMEA",
        "country": "DE",
        "city": "Stuttgart",
        "lat": 48.7758,
        "lon": 9.1829,
        "erp_system": "SAP S/4HANA Production (EU-01)",
        "mes_wms_system": "Siemens Opcenter MES",
        "daily_capacity_units": 4800,
        "current_oee_pct": 86.4,
        "headcount_fte": 420,
        "annual_lease_opex_usd": 8400000,
    },
    {
        "facility_id": "PLANT-XYZ-AUSTIN",
        "facility_name": "XYZ Austin Aseptic Bottling & Battery Assembly Campus",
        "facility_type": "MANUFACTURING_PLANT",
        "region": "NAMER",
        "country": "US",
        "city": "Austin, TX",
        "lat": 30.2672,
        "lon": -97.7431,
        "erp_system": "SAP S/4HANA Production (US-01)",
        "mes_wms_system": "Rockwell FactoryTalk + Veeva QMS",
        "daily_capacity_units": 12500,
        "current_oee_pct": 89.2,
        "headcount_fte": 510,
        "annual_lease_opex_usd": 9600000,
    },
    {
        "facility_id": "PLANT-XYZ-BENGALURU",
        "facility_name": "XYZ Bengaluru Electronics & Elastomer Smart Factory",
        "facility_type": "MANUFACTURING_PLANT",
        "region": "APAC",
        "country": "IN",
        "city": "Bengaluru (Nelamangala)",
        "lat": 13.0998,
        "lon": 77.3936,
        "erp_system": "SAP S/4HANA Production (IN-01)",
        "mes_wms_system": "Siemens Opcenter + GigE Vision",
        "daily_capacity_units": 9200,
        "current_oee_pct": 88.1,
        "headcount_fte": 640,
        "annual_lease_opex_usd": 4200000,
    },
    {
        "facility_id": "PLANT-XYZ-MONTERREY",
        "facility_name": "XYZ Monterrey Thermal Brazing & Nearshore Assembly Plant",
        "facility_type": "MANUFACTURING_PLANT",
        "region": "LATAM",
        "country": "MX",
        "city": "Monterrey",
        "lat": 25.6866,
        "lon": -100.3161,
        "erp_system": "SAP S/4HANA Production (MX-01)",
        "mes_wms_system": "Honeywell Forge MES",
        "daily_capacity_units": 6400,
        "current_oee_pct": 84.7,
        "headcount_fte": 380,
        "annual_lease_opex_usd": 5100000,
    },
    {
        "facility_id": "RDC-XYZ-CHICAGO",
        "facility_name": "XYZ Midwest Mega-Regional Distribution Center (Joliet)",
        "facility_type": "REGIONAL_DC",
        "region": "NAMER",
        "country": "US",
        "city": "Chicago, IL",
        "lat": 41.5250,
        "lon": -88.0817,
        "erp_system": "SAP S/4HANA Inventory",
        "mes_wms_system": "Manhattan Active WMS + AMR Fleet",
        "daily_capacity_units": 45000,
        "current_oee_pct": 94.2,
        "headcount_fte": 290,
        "annual_lease_opex_usd": 6800000,
    },
    {
        "facility_id": "FDC-XYZ-ATLANTA",
        "facility_name": "XYZ Southeast Forward Fulfillment & Cross-Dock Hub",
        "facility_type": "FORWARD_DC",
        "region": "NAMER",
        "country": "US",
        "city": "Atlanta, GA",
        "lat": 33.7490,
        "lon": -84.3880,
        "erp_system": "SAP S/4HANA Inventory",
        "mes_wms_system": "Manhattan Active WMS",
        "daily_capacity_units": 22000,
        "current_oee_pct": 92.8,
        "headcount_fte": 145,
        "annual_lease_opex_usd": 3400000,
    },
    {
        "facility_id": "FDC-XYZ-ROTTERDAM",
        "facility_name": "XYZ Europort Bonded Cross-Dock & Rhine Barge Terminal",
        "facility_type": "FORWARD_DC",
        "region": "EMEA",
        "country": "NL",
        "city": "Rotterdam",
        "lat": 51.9244,
        "lon": 4.4777,
        "erp_system": "SAP S/4HANA GTS & Inventory",
        "mes_wms_system": "Blue Yonder WMS",
        "daily_capacity_units": 30000,
        "current_oee_pct": 95.1,
        "headcount_fte": 175,
        "annual_lease_opex_usd": 4900000,
    },
    {
        "facility_id": "FDC-XYZ-MUMBAI",
        "facility_name": "XYZ Mumbai Bhiwandi Last-Mile & TM&D Fulfillment Hub",
        "facility_type": "FORWARD_DC",
        "region": "APAC",
        "country": "IN",
        "city": "Mumbai (Bhiwandi)",
        "lat": 19.2813,
        "lon": 73.0483,
        "erp_system": "SAP S/4HANA + DMS",
        "mes_wms_system": "Manhattan Active WMS + FleetFlow",
        "daily_capacity_units": 28000,
        "current_oee_pct": 93.5,
        "headcount_fte": 210,
        "annual_lease_opex_usd": 2600000,
    },
]

ENTERPRISE_SUPPLIERS = [
    {
        "supplier_id": "SUP-XYZ-T1-ALUWELD",
        "vendor_code_sap": "VEND-900112",
        "supplier_name": "AluWeld Precision Thermal GmbH",
        "tier_level": "TIER_1",
        "country": "DE",
        "city": "Essen",
        "supplied_skus": ["SKU-XYZ-101", "SKU-XYZ-518"],
        "contract_payment_terms": "2/10 Net 45",
        "annual_spend_usd": 18400000,
        "on_time_delivery_pct": 96.4,
        "quality_cpk": 1.54,
        "geopolitical_risk_score": 14.0,
        "cbam_verified_smelter": True,
        "upstream_tier2_supplier_id": "SUP-XYZ-T2-NORSKHYDRO",
    },
    {
        "supplier_id": "SUP-XYZ-T1-SILICONCORE",
        "vendor_code_sap": "VEND-900245",
        "supplier_name": "Taiwan SiliconCore Microelectronics Co.",
        "tier_level": "TIER_1",
        "country": "TW",
        "city": "Hsinchu",
        "supplied_skus": ["SKU-XYZ-101", "SKU-XYZ-412"],
        "contract_payment_terms": "Net 60",
        "annual_spend_usd": 29500000,
        "on_time_delivery_pct": 91.2,
        "quality_cpk": 1.68,
        "geopolitical_risk_score": 78.5,
        "cbam_verified_smelter": True,
        "upstream_tier2_supplier_id": "SUP-XYZ-T2-KYOTOWAFER",
    },
    {
        "supplier_id": "SUP-XYZ-T1-ASEPTIPACK",
        "vendor_code_sap": "VEND-900389",
        "supplier_name": "AseptiPack Foil & Closures North America",
        "tier_level": "TIER_1",
        "country": "US",
        "city": "Dallas, TX",
        "supplied_skus": ["SKU-XYZ-204"],
        "contract_payment_terms": "Net 30",
        "annual_spend_usd": 11200000,
        "on_time_delivery_pct": 94.8,
        "quality_cpk": 1.18,
        "geopolitical_risk_score": 11.0,
        "cbam_verified_smelter": False,
        "upstream_tier2_supplier_id": "SUP-XYZ-T2-NOVELISALU",
    },
    {
        "supplier_id": "SUP-XYZ-T1-SUMATRARUBBER",
        "vendor_code_sap": "VEND-900514",
        "supplier_name": "PT Sumatra Agro-Elastomers Indonesia",
        "tier_level": "TIER_1",
        "country": "ID",
        "city": "Medan",
        "supplied_skus": ["SKU-XYZ-625"],
        "contract_payment_terms": "Net 45",
        "annual_spend_usd": 6800000,
        "on_time_delivery_pct": 89.5,
        "quality_cpk": 1.42,
        "geopolitical_risk_score": 46.0,
        "cbam_verified_smelter": True,
        "upstream_tier2_supplier_id": "PLOT-IDN-882-EUDR",
    },
    {
        "supplier_id": "SUP-XYZ-T2-KYOTOWAFER",
        "vendor_code_sap": "VEND-900801",
        "supplier_name": "Kyoto UltraPure Silicon Wafer Ltd.",
        "tier_level": "TIER_2",
        "country": "JP",
        "city": "Kyoto",
        "supplied_skus": ["SKU-XYZ-101", "SKU-XYZ-412"],
        "contract_payment_terms": "Net 45",
        "annual_spend_usd": 14100000,
        "on_time_delivery_pct": 98.1,
        "quality_cpk": 1.82,
        "geopolitical_risk_score": 22.0,
        "cbam_verified_smelter": True,
        "upstream_tier2_supplier_id": "SUP-XYZ-T3-QUARTZMINE",
    },
]

# Non-agent organizational tables (HR Shift Rosters, Finance Cost Centers, Customer Master, End-to-End Golden Thread Orders)
ORG_FINANCE_GL_COST_CENTERS = [
    {"cost_center_id": "CC-XYZ-1000", "department": "Office of the CSCO & Global Control Tower", "vp_owner": "Elena Rostova (CSCO)", "annual_budget_usd": 15000000, "delegation_limit_usd": 2000000, "erp_ledger": "SAP-FI-GLOBAL"},
    {"cost_center_id": "CC-XYZ-2100", "department": "Global Demand Planning & S&OP", "vp_owner": "Marcus Vance (VP Demand)", "annual_budget_usd": 8200000, "delegation_limit_usd": 500000, "erp_ledger": "SAP-FI-NAMER"},
    {"cost_center_id": "CC-XYZ-3200", "department": "Strategic Sourcing & Direct Procurement", "vp_owner": "Priya Nair (CPO)", "annual_budget_usd": 94500000, "delegation_limit_usd": 1500000, "erp_ledger": "SAP-FI-EMEA"},
    {"cost_center_id": "CC-XYZ-4300", "department": "Global Manufacturing & Plant Operations", "vp_owner": "Hans Becker (VP Mfg)", "annual_budget_usd": 42000000, "delegation_limit_usd": 750000, "erp_ledger": "SAP-FI-EMEA"},
    {"cost_center_id": "CC-XYZ-5400", "department": "Multi-Echelon Inventory & Warehousing", "vp_owner": "Carlos Mendez (VP Fulfillment)", "annual_budget_usd": 28500000, "delegation_limit_usd": 600000, "erp_ledger": "SAP-FI-NAMER"},
    {"cost_center_id": "CC-XYZ-6500", "department": "Global Fleet, Multi-Modal Transit & TM&D", "vp_owner": "Suman Banerjee (VP Logistics)", "annual_budget_usd": 36800000, "delegation_limit_usd": 800000, "erp_ledger": "SAP-FI-APAC"},
    {"cost_center_id": "CC-XYZ-7600", "department": "Circular RMA, Customer OTIF & ESG Compliance", "vp_owner": "Claire Dubois (VP Sustainability)", "annual_budget_usd": 11400000, "delegation_limit_usd": 450000, "erp_ledger": "SAP-FI-EMEA"},
]

ORG_HR_PLANT_SHIFT_ROSTERS = [
    {"shift_id": "SHIFT-STUT-A", "facility_id": "PLANT-XYZ-STUTTGART", "shift_pattern": "06:00-14:00 CET", "supervisor": "Lukas Weber", "certified_cnc_operators": 38, "maintenance_techs_on_duty": 6, "overtime_authorized": True},
    {"shift_id": "SHIFT-AUST-A", "facility_id": "PLANT-XYZ-AUSTIN", "shift_pattern": "06:00-14:00 CST", "supervisor": "Sarah Jenkins", "certified_cnc_operators": 52, "maintenance_techs_on_duty": 8, "overtime_authorized": True},
    {"shift_id": "SHIFT-BLR-A", "facility_id": "PLANT-XYZ-BENGALURU", "shift_pattern": "07:00-15:00 IST", "supervisor": "Arjun Rao", "certified_cnc_operators": 64, "maintenance_techs_on_duty": 9, "overtime_authorized": True},
    {"shift_id": "SHIFT-MUM-FLEET", "facility_id": "FDC-XYZ-MUMBAI", "shift_pattern": "05:30-14:30 IST", "supervisor": "Vikram Deshmukh", "active_commercial_drivers": 24, "lead_west_corridor_driver": "Ravi Sharma (TRK-T14-01)", "overtime_authorized": False},
]

ORG_CUSTOMER_MASTER = [
    {"customer_id": "CUST-XYZ-TIER1-AUTOWORKS", "customer_name": "EuroAuto Mobility AG", "tier": "STRATEGIC_TIER_1", "country": "DE", "otif_target_pct": 98.5, "chargeback_penalty_pct": 5.0, "primary_skus": ["SKU-XYZ-101", "SKU-XYZ-309", "SKU-XYZ-518"]},
    {"customer_id": "CUST-XYZ-TIER1-MEGAMART", "customer_name": "MegaMart National Retail Corp", "tier": "STRATEGIC_TIER_1", "country": "US", "otif_target_pct": 99.0, "chargeback_penalty_pct": 3.5, "primary_skus": ["SKU-XYZ-204", "SKU-XYZ-412"]},
    {"customer_id": "CUST-XYZ-TIER2-METROCPG", "customer_name": "MetroFresh Hypermarkets India", "tier": "PREMIER_TIER_2", "country": "IN", "otif_target_pct": 96.0, "chargeback_penalty_pct": 2.0, "primary_skus": ["SKU-XYZ-204", "SKU-XYZ-625"]},
]

# Cross-Agent Golden Thread Transaction Ledger (links Plan -> Source -> Make -> Fulfill -> Deliver -> Return)
GOLDEN_THREAD_TRANSACTIONS = [
    {
        "golden_thread_id": "GT-XYZ-2026-001",
        "sku_id": "SKU-XYZ-101",
        "demand_signal_id": "SIG-WEATH-HEATWAVE-EU",
        "sop_scenario_id": "SOP-2026-11-CONSENSUS",
        "purchase_order_id": "PO-XYZ-880142",
        "supplier_id": "SUP-XYZ-T1-ALUWELD",
        "production_batch_id": "BATCH-XYZ-STUT-904",
        "plant_id": "PLANT-XYZ-STUTTGART",
        "meio_transfer_id": "XFER-XYZ-STUT-ROT-11",
        "sales_order_id": "SO-XYZ-20261022-801",
        "customer_id": "CUST-XYZ-TIER1-AUTOWORKS",
        "shipment_id": "SHP-XYZ-9041",
        "container_or_truck_id": "TRK-EU-RHINE-08",
        "scope3_emissions_kg_co2e": 1420.5,
        "rma_ticket_id": "NONE",
        "end_to_end_status": "IN_TRANSIT_ON_TIME",
    },
    {
        "golden_thread_id": "GT-XYZ-2026-002",
        "sku_id": "SKU-XYZ-204",
        "demand_signal_id": "SIG-POS-HEATWAVE-MW",
        "sop_scenario_id": "SOP-2026-11-PROMO-LIFT",
        "purchase_order_id": "PO-XYZ-880219",
        "supplier_id": "SUP-XYZ-T1-ASEPTIPACK",
        "production_batch_id": "BATCH-XYZ-AUST-8841",
        "plant_id": "PLANT-XYZ-AUSTIN",
        "meio_transfer_id": "XFER-XYZ-CHI-ATL-04",
        "sales_order_id": "SO-XYZ-20261022-802",
        "customer_id": "CUST-XYZ-TIER1-MEGAMART",
        "shipment_id": "SHP-XYZ-9088",
        "container_or_truck_id": "TRK-T17-WEST-01",
        "scope3_emissions_kg_co2e": 412.8,
        "rma_ticket_id": "RMA-20261022-501",
        "end_to_end_status": "DELIVERED_RMA_BACKHAUL_MATCHED",
    },
    {
        "golden_thread_id": "GT-XYZ-2026-003",
        "sku_id": "SKU-XYZ-412",
        "demand_signal_id": "SIG-CPFR-DIST-SYNC",
        "sop_scenario_id": "SOP-2026-11-AIR-EXPEDITE",
        "purchase_order_id": "PO-XYZ-880355",
        "supplier_id": "SUP-XYZ-T1-SILICONCORE",
        "production_batch_id": "BATCH-XYZ-BLR-7712",
        "plant_id": "PLANT-XYZ-BENGALURU",
        "meio_transfer_id": "XFER-XYZ-BLR-MUM-09",
        "sales_order_id": "SO-XYZ-20261022-803",
        "customer_id": "CUST-XYZ-TIER2-METROCPG",
        "shipment_id": "SHP-XYZ-9102",
        "container_or_truck_id": "ULD-LD3-AERO-04",
        "scope3_emissions_kg_co2e": 890.0,
        "rma_ticket_id": "NONE",
        "end_to_end_status": "DISRUPTION_MITIGATED_BY_AIR_ULD",
    },
]


# ==============================================================================
# 2. Excel (.xlsx) Multi-Tab Workbook Generator
# ==============================================================================
def _style_worksheet(ws, title: str, subtitle: str, headers: List[str], rows: List[List[Any]], accent_hex: str = "1E3A8A") -> None:
    ws.views.sheetView[0].showGridLines = True

    # Title Banner
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=max(len(headers), 4))
    c_title = ws.cell(row=1, column=1, value=f"{COMPANY_NAME} — {title}")
    c_title.font = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
    c_title.fill = PatternFill(start_color=accent_hex, end_color=accent_hex, fill_type="solid")
    c_title.alignment = Alignment(vertical="center", horizontal="left", indent=1)
    ws.row_dimensions[1].height = 26

    # Subtitle Banner
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=max(len(headers), 4))
    c_sub = ws.cell(row=2, column=1, value=subtitle)
    c_sub.font = Font(name="Calibri", size=9, italic=True, color="334155")
    c_sub.fill = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid")
    c_sub.alignment = Alignment(vertical="center", horizontal="left", indent=1)
    ws.row_dimensions[2].height = 19

    thin_border = Border(
        left=Side(style="thin", color="CBD5E1"),
        right=Side(style="thin", color="CBD5E1"),
        top=Side(style="thin", color="CBD5E1"),
        bottom=Side(style="thin", color="CBD5E1"),
    )

    # Header Row
    ws.row_dimensions[4].height = 22
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=4, column=col_idx, value=h)
        cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
        cell.alignment = Alignment(vertical="center", horizontal="center")
        cell.border = thin_border

    # Data Rows
    for r_idx, row_vals in enumerate(rows, 5):
        ws.row_dimensions[r_idx].height = 19
        row_bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_vals, 1):
            if isinstance(val, (list, dict)):
                val = json.dumps(val)
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name="Calibri", size=10, color="0F172A")
            cell.fill = PatternFill(start_color=row_bg, end_color=row_bg, fill_type="solid")
            cell.border = thin_border
            if isinstance(val, (int, float)):
                cell.alignment = Alignment(vertical="center", horizontal="right")
            else:
                cell.alignment = Alignment(vertical="center", horizontal="left")

    # Auto-fit columns
    for col_idx in range(1, len(headers) + 1):
        col_letter = get_column_letter(col_idx)
        max_len = len(str(headers[col_idx - 1]))
        for r_idx in range(5, 5 + len(rows)):
            v = ws.cell(row=r_idx, column=col_idx).value
            if v is not None:
                max_len = max(max_len, min(len(str(v)), 44))
        ws.column_dimensions[col_letter].width = max(max_len + 4, 14)


def _dict_list_to_headers_rows(records: List[Dict[str, Any]]) -> tuple[List[str], List[List[Any]]]:
    if not records:
        return ["Status"], [["No records"]]
    headers = list(records[0].keys())
    for r in records:
        for k in r.keys():
            if k not in headers:
                headers.append(k)
    rows = [[r.get(k, "") for k in headers] for r in records]
    return headers, rows


def build_excel_workbooks(excel_dir: Path, all_agent_tables: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    excel_dir.mkdir(parents=True, exist_ok=True)
    workbooks_spec = [
        {
            "filename": "XYZ_Corp_00_Global_ERP_Master_and_Org_Data.xlsx",
            "title": "Global ERP Master Data, Finance GL Cost Centers & HR Plant Rosters",
            "pillar": "Universal CSCO Core & Enterprise Backbone",
            "accent": "1E3A8A",
            "sheets": [
                ("Material_Master_MARA", "SAP S/4HANA Material Master (Cross-Agent SKUs)", ENTERPRISE_SKUS),
                ("Facility_Network_Nodes", "Global Manufacturing Plants, Mega-RDCs & Forward DCs", ENTERPRISE_FACILITIES),
                ("Vendor_Master_LFA1", "Multi-Tier Direct Materials Supplier Master", ENTERPRISE_SUPPLIERS),
                ("Customer_Master_KNA1", "Strategic B2B & Retail Customer Master", ORG_CUSTOMER_MASTER),
                ("Finance_GL_CostCenters", "Corporate Cost Centers & CSCO Delegation Authority", ORG_FINANCE_GL_COST_CENTERS),
                ("HR_Plant_Shift_Rosters", "Plant Floor & Commercial Fleet Shift Rosters", ORG_HR_PLANT_SHIFT_ROSTERS),
                ("Golden_Thread_Ledger", "End-to-End Plan-to-Return Connected Order Ledger", GOLDEN_THREAD_TRANSACTIONS),
            ],
        },
        {
            "filename": "XYZ_Corp_01_Plan_Demand_SOP_and_CPFR_Workbook.xlsx",
            "title": "01 · PLAN — Demand Sensing, TimesFM Forecasts, S&OP & CPFR Consensus",
            "pillar": "01 · Plan",
            "accent": "0284C7",
            "sheets": [
                ("POS_Store_Scans", "Daily Retail POS Velocity & Sell-Through Scans", all_agent_tables.get("pos_store_scans", [])),
                ("WeatherNext_Signals", "Google DeepMind WeatherNext 3 Heatwave & Storm Signals", all_agent_tables.get("external_signals_weathernext", [])),
                ("TimesFM_Quantiles", "Vertex AI TimesFM P10/P50/P90 Probabilistic Horizon", all_agent_tables.get("timesfm_quantile_horizons", [])),
                ("SOP_Capacity_Scenarios", "Monthly S&OP Consensus Tradeoff Matrix", all_agent_tables.get("sop_scenario_tradeoffs", [])),
                ("Promo_Elasticity_Matrix", "Causal Promo Lift & Halo/Cannibalization", all_agent_tables.get("causal_promo_elasticity", [])),
                ("CPFR_Retailer_Sync", "EDI 830/852 Collaborative Forecast Packets", all_agent_tables.get("joint_cpfr_consensus_packets", [])),
            ],
        },
        {
            "filename": "XYZ_Corp_02_Source_ShouldCost_RFQ_and_TierN_Risk.xlsx",
            "title": "02 · SOURCE — Parametric Should-Cost BOM, RFQ Bids & Spanner Tier-N Graph",
            "pillar": "02 · Source",
            "accent": "4F46E5",
            "sheets": [
                ("Parametric_Should_Cost", "Bottom-Up BOM Should-Cost Breakdown", all_agent_tables.get("material_should_cost_bom", [])),
                ("Supplier_RFQ_Bids", "Autonomous Supplier RFQ Quote Evaluations", all_agent_tables.get("supplier_rfq_bids", [])),
                ("Commodity_Index_LME", "London Metal Exchange & Resin Index Feed", all_agent_tables.get("commodity_index_rates", [])),
                ("TierN_Supplier_Graph", "Spanner Graph Sub-Tier Dependency Network", all_agent_tables.get("subtier_supplier_network", [])),
                ("HS_Tariff_Duty_Matrix", "Cross-Border Customs HS Tariff & Duty Impact", all_agent_tables.get("hs_tariff_classifications", [])),
                ("Supplier_COA_Quality", "Incoming Certificate of Analysis & Cpk Audits", all_agent_tables.get("supplier_coa_inspections", [])),
            ],
        },
        {
            "filename": "XYZ_Corp_03_Make_Plant_OEE_Production_and_Vision_QA.xlsx",
            "title": "03 · MAKE — Plant OEE Telemetry, Job-Shop Schedules & Inline Vision QA",
            "pillar": "03 · Make",
            "accent": "D97706",
            "sheets": [
                ("Plant_OEE_Breakdown", "Shift Availability, Performance & Quality OEE", all_agent_tables.get("oee_breakdown_metrics", [])),
                ("Machine_IoT_Telemetry", "CNC Spindle Vibration & Bearing Thermal Telemetry", all_agent_tables.get("plant_machine_telemetry", [])),
                ("Finite_JobShop_Schedule", "OR-Tools CP-SAT Sequence-Dependent Setup Schedule", all_agent_tables.get("optimized_sequence_schedule", [])),
                ("Vision_Defect_Frames", "Gemini 3.8 Flash 120FPS Optical Defect Detections", all_agent_tables.get("vision_defect_classification_results", [])),
                ("eBHR_Batch_Deviations", "21 CFR Part 11 Electronic Batch Record Logs", all_agent_tables.get("ebhr_batch_record_deviations", [])),
                ("PLM_ECO_Cutover", "Engineering Change Order BOM Effectivity Cutover", all_agent_tables.get("plm_engineering_change_orders", [])),
            ],
        },
        {
            "filename": "XYZ_Corp_04_Fulfill_MEIO_3D_Slotting_and_Spanner_ATP.xlsx",
            "title": "04 · FULFILL — Clark-Scarf MEIO, 3D Warehouse Slotting, Spanner ATP & Yard",
            "pillar": "04 · Fulfill",
            "accent": "059669",
            "sheets": [
                ("Echelon_Inventory", "RDC & FDC Multi-Echelon Inventory Balances", all_agent_tables.get("dc_inventory_echelon_balances", [])),
                ("Clark_Scarf_MEIO", "Stochastic Multi-Echelon Safety Stock Recommendations", all_agent_tables.get("multi_echelon_safety_stock_recommendations", [])),
                ("Spanner_Realtime_ATP", "Sub-50ms Spanner Available-to-Promise Ledger", all_agent_tables.get("realtime_sku_atp_allocations", [])),
                ("Warehouse_3D_Slotting", "SKU Velocity Tiers & AMR Picker Travel Slotting", all_agent_tables.get("warehouse_slotting_velocity_tiers", [])),
                ("CrossDock_Transfers", "Inbound-to-Outbound Flow-Through Manifests", all_agent_tables.get("inbound_outbound_crossdock_manifests", [])),
                ("Yard_Dock_Schedules", "Trailer Geofence & Dock Door Turnaround", all_agent_tables.get("dock_door_turnaround_schedules", [])),
            ],
        },
        {
            "filename": "XYZ_Corp_05_Deliver_MultiModal_Fleet_3D_LIFO_and_TMD.xlsx",
            "title": "05 · DELIVER — FleetFlow Corridors, CubeMaster 3D LIFO, Ocean/Air/Rail & TM&D",
            "pillar": "05 · Deliver",
            "accent": "0D9488",
            "sheets": [
                ("FleetFlow_Corridors", "Google Maps Polar Corridor Delivery Orders", all_agent_tables.get("corridor_delivery_orders", [])),
                ("CubeMaster_3D_Cartons", "3D Carton Dimensions, Fragility & LIFO Sequence", all_agent_tables.get("outbound_shipment_carton_dimensions", [])),
                ("Ocean_Port_Drayage", "Spire AIS Vessel Berth & Container Demurrage", all_agent_tables.get("container_discharge_demurrage_ledger", [])),
                ("Air_Cargo_ULD_Manifest", "3D Contoured ULD Belly-Hold Build Plans", all_agent_tables.get("uld_3d_packing_manifests", [])),
                ("Rail_Intermodal_EDI417", "Railinc EDI 417 Train Consists & Ramp Cutoffs", all_agent_tables.get("railinc_edi417_train_consists", [])),
                ("TMD_Distributor_Claims", "Beat Inventory & Trade Scheme Claim Audits", all_agent_tables.get("distributor_secondary_claim_submissions", [])),
            ],
        },
        {
            "filename": "XYZ_Corp_06_Return_RMA_OTIF_Shield_and_Scope3_CBAM.xlsx",
            "title": "06 · RETURN & ENABLE — Circular RMA Grading, OTIF Disputes & ISO 14083 Scope-3",
            "pillar": "06 · Return & Enable",
            "accent": "16A34A",
            "sheets": [
                ("Customer_RMA_Queue", "Customer RMA Intake & Optical Seal Grading", all_agent_tables.get("multimodal_vision_grading_results", [])),
                ("Backhaul_Pickup_Slots", "Returning FleetFlow Truck Backhaul Slots", all_agent_tables.get("fleet_backhaul_pickup_slots", [])),
                ("OTIF_Penalty_Shield", "Retailer EDI 856 Geofence Dispute Dossiers", all_agent_tables.get("geofence_edi856_dispute_dossiers", [])),
                ("ISO14083_Scope3_Ledger", "Shipment-Level WTW Scope-3 Carbon Ledger", all_agent_tables.get("shipment_level_scope3_emissions", [])),
                ("EU_CBAM_Declarations", "Verified Primary Smelter Carbon Certificates", all_agent_tables.get("eu_cbam_embedded_carbon_declarations", [])),
                ("EUDR_Satellite_Plots", "Earth Engine Zero-Deforestation Plot Verifications", all_agent_tables.get("eudr_earth_engine_plot_verifications", [])),
            ],
        },
    ]

    manifest_items = []
    for wb_spec in workbooks_spec:
        wb = openpyxl.Workbook()
        # remove default sheet
        wb.remove(wb.active)
        sheet_names = []
        total_rows = 0
        for s_name, s_sub, records in wb_spec["sheets"]:
            ws = wb.create_sheet(title=s_name[:31])
            headers, rows = _dict_list_to_headers_rows(records)
            _style_worksheet(ws, f"{wb_spec['title']} — {s_name}", s_sub, headers, rows, wb_spec["accent"])
            sheet_names.append(s_name)
            total_rows += len(rows)

        out_path = excel_dir / wb_spec["filename"]
        wb.save(out_path)
        manifest_items.append({
            "filename": wb_spec["filename"],
            "path": f"demo_data/xyz_corporation/excel/{wb_spec['filename']}",
            "title": wb_spec["title"],
            "pillar": wb_spec["pillar"],
            "format": "XLSX",
            "sheets": sheet_names,
            "row_count": total_rows,
            "size_kb": round(out_path.stat().st_size / 1024, 1),
        })
    print(f"[OK] Generated {len(manifest_items)} multi-tab Excel (.xlsx) workbooks in {excel_dir}")
    return manifest_items


# ==============================================================================
# 3. High-Resolution Computer Vision & Operational PNG Images Generator
# ==============================================================================
def _load_font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size=size)
            except Exception:
                pass
    return ImageFont.load_default()


def _draw_header_banner(draw: ImageDraw.ImageDraw, width: int, title: str, subtitle: str, badge: str, accent: tuple[int, int, int]) -> None:
    draw.rectangle([0, 0, width, 78], fill=(15, 23, 42))
    draw.rectangle([0, 74, width, 78], fill=accent)
    f_title = _load_font(22, bold=True)
    f_sub = _load_font(14, bold=False)
    f_badge = _load_font(13, bold=True)
    draw.text((24, 14), f"{COMPANY_NAME}  |  {title}", fill=(255, 255, 255), font=f_title)
    draw.text((24, 46), subtitle, fill=(148, 163, 184), font=f_sub)
    bw = 260
    draw.rounded_rectangle([width - bw - 24, 18, width - 24, 58], radius=8, fill=accent)
    draw.text((width - bw - 10, 29), badge, fill=(255, 255, 255), font=f_badge)


def build_operational_images(img_dir: Path) -> List[Dict[str, Any]]:
    img_dir.mkdir(parents=True, exist_ok=True)
    f_lg = _load_font(18, bold=True)
    f_md = _load_font(15, bold=True)
    f_sm = _load_font(13, bold=False)
    f_xs = _load_font(11, bold=False)

    images_meta = []

    # 1. Dock QR Carton & Pallet Staging Photo
    w, h = 1100, 680
    im1 = Image.new("RGB", (w, h), (226, 232, 240))
    d1 = ImageDraw.Draw(im1)
    _draw_header_banner(d1, w, "DOCK STAGING VISION & QR CARTON INTAKE", "Facility: FDC-XYZ-MUMBAI  |  Order: SO-XYZ-20261022-802  |  Corridor: WEST (Driver: Ravi Sharma)", "QR 100% DECODED", (13, 148, 136))
    # Warehouse floor & wooden pallet
    d1.rectangle([0, 520, w, h], fill=(100, 116, 139))
    d1.rectangle([120, 495, 980, 525], fill=(180, 130, 70), outline=(120, 80, 30), width=2)
    carton_specs = [
        (150, 220, 390, 495, "CTN-XYZ-802-01", "SKU-XYZ-204 (24-Pack)", "12.4 kg | Drop #1 (Door)", "40x30x22 cm"),
        (415, 190, 685, 495, "CTN-XYZ-802-02", "SKU-XYZ-101 (CryoCell)", "18.5 kg | Drop #2 (Mid)", "60x40x25 cm"),
        (710, 240, 955, 495, "CTN-XYZ-802-03", "SKU-XYZ-412 (IoT Hub)", "8.2 kg  | Drop #3 (Cab)", "24x18x10 cm"),
    ]
    for x1, y1, x2, y2, cid, sku_lbl, wt_lbl, dim_lbl in carton_specs:
        # Kraft cardboard box
        d1.rectangle([x1, y1, x2, y2], fill=(212, 172, 118), outline=(140, 102, 56), width=3)
        # BOPP tape strip
        d1.rectangle([x1, y1 + 14, x2, y1 + 36], fill=(235, 205, 155), outline=(180, 145, 95))
        # White thermal shipping label
        lx1, ly1, lx2, ly2 = x1 + 18, y1 + 52, x2 - 18, y2 - 22
        d1.rectangle([lx1, ly1, lx2, ly2], fill=(255, 255, 255), outline=(51, 65, 85), width=2)
        d1.text((lx1 + 10, ly1 + 8), f"XYZ CORP | {cid}", fill=(15, 23, 42), font=f_md)
        d1.text((lx1 + 10, ly1 + 32), sku_lbl, fill=(30, 58, 138), font=f_sm)
        d1.text((lx1 + 10, ly1 + 54), wt_lbl, fill=(15, 118, 110), font=f_sm)
        d1.text((lx1 + 10, ly1 + 74), f"DIM: {dim_lbl}", fill=(71, 85, 105), font=f_xs)
        # Draw real QR code if qrcode installed, else deterministic finder matrix
        try:
            import qrcode
            qr = qrcode.QRCode(box_size=3, border=1)
            qr.add_data(f"XYZ|{cid}|{sku_lbl}|{dim_lbl}")
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB").resize((96, 96))
            im1.paste(qr_img, (lx2 - 108, ly2 - 108))
        except Exception:
            d1.rectangle([lx2 - 104, ly2 - 104, lx2 - 12, ly2 - 12], outline=(0, 0, 0), width=3)
        # Green OpenCV detection bounding box around QR
        d1.rectangle([lx2 - 112, ly2 - 112, lx2 - 8, ly2 - 8], outline=(16, 185, 129), width=3)
    d1.rectangle([24, 545, w - 24, 655], fill=(15, 23, 42), outline=(13, 148, 136), width=2)
    d1.text((42, 560), "GEMINI 3.8 FLASH + OPENCV QR INTAKE TELEMETRY:", fill=(45, 212, 191), font=f_md)
    d1.text((42, 588), "• Decoded 3/3 Staging Cartons in 38ms  |  Total Weight: 39.1 kg  |  Assigned Vehicle: TRK-14FT-W01 (Driver: Ravi Sharma)", fill=(255, 255, 255), font=f_sm)
    d1.text((42, 614), "• LIFO Bay Sequence Verified: Drop #3 loaded at Cab (0-75cm) -> Drop #2 Mid -> Drop #1 at Rear Door (Zero Re-handling)", fill=(148, 163, 184), font=f_sm)
    p1 = img_dir / "XYZ_01_Dock_QR_Carton_Staging_Vision.png"
    im1.save(p1)
    images_meta.append({"filename": p1.name, "path": f"demo_data/xyz_corporation/images/{p1.name}", "title": "Dock QR Carton & Pallet Staging Vision Scan", "pillar": "05 · Deliver / 04 · Fulfill", "agent_id": "fleetflow_dispatch"})

    # 2. VisionInspect Inline High-Speed Packaging Seal Inspection Frame
    im2 = Image.new("RGB", (w, h), (15, 23, 42))
    d2 = ImageDraw.Draw(im2)
    _draw_header_banner(d2, w, "GIGE 120-FPS INLINE OPTICAL QUALITY INSPECTION", "Plant: PLANT-XYZ-AUSTIN (Line 03)  |  Batch: BATCH-XYZ-AUST-8841  |  SKU: SKU-XYZ-204", "DEFECT DIVERTED 14.2ms", (220, 38, 38))
    # Left panel: Frame 841 (Defect) | Right panel: Frame 842 (Nominal)
    d2.rectangle([30, 100, 535, 520], fill=(30, 41, 59), outline=(239, 68, 68), width=3)
    d2.text((48, 114), "FRAME-00841  |  INDUCTION FOIL SEAL TEAR (CRITICAL)", fill=(248, 113, 113), font=f_md)
    # Draw bottle neck & torn foil seal
    d2.rectangle([210, 220, 355, 480], fill=(56, 189, 248), outline=(186, 230, 253), width=2)
    d2.ellipse([205, 185, 360, 245], fill=(203, 213, 225), outline=(255, 255, 255), width=2)
    # Red tear anomaly + bounding box
    d2.polygon([(255, 205), (320, 195), (335, 225), (270, 232)], fill=(220, 38, 38))
    d2.rectangle([195, 175, 370, 255], outline=(239, 68, 68), width=4)
    d2.text((195, 152), "BBOX [0.34, 0.28, 0.66, 0.41] CONF: 98.5%", fill=(252, 165, 165), font=f_sm)
    d2.text((48, 485), "ACTION: Pneumatic Gate DIVERT-01 Fired (14.2ms) -> Quarantine Bin 01", fill=(254, 202, 202), font=f_xs)

    d2.rectangle([565, 100, 1070, 520], fill=(30, 41, 59), outline=(16, 185, 129), width=3)
    d2.text((583, 114), "FRAME-00842  |  NOMINAL HERMETIC SEAL (PASSED)", fill=(52, 211, 153), font=f_md)
    d2.rectangle([745, 220, 890, 480], fill=(56, 189, 248), outline=(186, 230, 253), width=2)
    d2.ellipse([740, 185, 895, 245], fill=(226, 232, 240), outline=(16, 185, 129), width=3)
    d2.rectangle([730, 175, 905, 255], outline=(16, 185, 129), width=3)
    d2.text((730, 152), "SEAL INTEGRITY: 99.8% NOMINAL", fill=(110, 231, 183), font=f_sm)
    d2.text((583, 485), "ACTION: Main Conveyor Flow-Through -> Case Packer Station 04", fill=(167, 243, 208), font=f_xs)

    d2.rectangle([30, 540, 1070, 650], fill=(30, 41, 59), outline=(71, 85, 105), width=2)
    d2.text((48, 555), "21 CFR PART 11 ELECTRONIC BATCH RECORD (eBHR) AUTO-LOGGED:", fill=(56, 189, 248), font=f_md)
    d2.text((48, 585), "• Veeva Vault Ticket: VEEVA-DEV-2026-8841  |  SAP QM Lot: QM-LOT-8841  |  Illumination: 4,200 Lux Strobe", fill=(255, 255, 255), font=f_sm)
    d2.text((48, 612), "• Zero defective units escaped to palletizer; induction sealer coil voltage recalibrated automatically.", fill=(148, 163, 184), font=f_sm)
    p2 = img_dir / "XYZ_02_VisionInspect_Inline_Seal_Defect_Frame841.png"
    im2.save(p2)
    images_meta.append({"filename": p2.name, "path": f"demo_data/xyz_corporation/images/{p2.name}", "title": "VisionInspect 120FPS Inline Seal Defect & Pneumatic Divert", "pillar": "03 · Make", "agent_id": "inline_quality_inspection_agent"})

    # 3. ReturnLoop Customer RMA Optical Grading & Backhaul Scan
    im3 = Image.new("RGB", (w, h), (241, 245, 249))
    d3 = ImageDraw.Draw(im3)
    _draw_header_banner(d3, w, "RETURNLOOP MULTIMODAL RMA OPTICAL CONDITION GRADER", "RMA Ticket: RMA-20261022-501  |  Customer: CUST-XYZ-TIER1-MEGAMART  |  Backhaul Truck: TRK-12T-TX14", "GRADE-A RESTOCK ($9,024)", (5, 150, 105))
    # Two comparison boxes: Grade-A Intact Seal vs Grade-C Harvest
    d3.rectangle([30, 100, 535, 520], fill=(255, 255, 255), outline=(16, 185, 129), width=3)
    d3.text((48, 116), "RMA-20261022-501  |  GRADE-A: FACTORY SEAL INTACT", fill=(5, 150, 105), font=f_md)
    d3.rectangle([130, 180, 435, 430], fill=(226, 232, 240), outline=(71, 85, 105), width=2)
    d3.rectangle([130, 285, 435, 325], fill=(16, 185, 129))
    d3.text((155, 297), "XYZ HOLOGRAPHIC TAMPER SEAL: UNBROKEN", fill=(255, 255, 255), font=f_sm)
    d3.text((48, 450), "• Optical Confidence: 99.2%  |  Disposition: Direct FDC Restock (FDC-AUSTIN-02)", fill=(15, 23, 42), font=f_sm)
    d3.text((48, 478), "• Value Recovered: 94.0% ($9,024 USD)  |  Instant SAP Credit Memo Issued", fill=(5, 150, 105), font=f_sm)

    d3.rectangle([565, 100, 1070, 520], fill=(255, 255, 255), outline=(217, 119, 6), width=3)
    d3.text((583, 116), "RMA-20261022-509  |  GRADE-C: HOUSING FRACTURE", fill=(180, 83, 9), font=f_md)
    d3.rectangle([665, 180, 970, 430], fill=(226, 232, 240), outline=(71, 85, 105), width=2)
    d3.line([(720, 210), (795, 290), (760, 350), (850, 400)], fill=(220, 38, 38), width=5)
    d3.rectangle([700, 195, 870, 415], outline=(220, 38, 38), width=3)
    d3.text((583, 450), "• Optical Confidence: 97.6%  |  Disposition: Component Harvest (Depot-03)", fill=(15, 23, 42), font=f_sm)
    d3.text((583, 478), "• Value Recovered: 48.0% ($3,072 USD)  |  PCB & Gold Connectors Salvaged", fill=(180, 83, 9), font=f_sm)

    d3.rectangle([30, 540, 1070, 650], fill=(15, 23, 42), outline=(5, 150, 105), width=2)
    d3.text((48, 558), "CIRCULAR BACKHAUL INSERTION (FLEETFLOW INTEGRATION):", fill=(52, 211, 153), font=f_md)
    d3.text((48, 588), "• Matched to returning empty truck TRK-12T-TX14 (1.8 km detour from Stop #8) -> Eliminated $420 LTL reverse freight cost.", fill=(255, 255, 255), font=f_sm)
    d3.text((48, 614), "• Avoided 41.2 kg CO2e deadhead emissions and bypassed Central Return Hub double-handling.", fill=(148, 163, 184), font=f_sm)
    p3 = img_dir / "XYZ_03_ReturnLoop_RMA_Optical_Grading_Scan.png"
    im3.save(p3)
    images_meta.append({"filename": p3.name, "path": f"demo_data/xyz_corporation/images/{p3.name}", "title": "ReturnLoop Multimodal RMA Grading & Backhaul Match", "pillar": "06 · Return & Enable", "agent_id": "reverse_rma_optimizer"})

    # 4. ShelfVision Retail Store Planogram & OSA Vision Audit
    im4 = Image.new("RGB", (w, h), (30, 41, 59))
    d4 = ImageDraw.Draw(im4)
    _draw_header_banner(d4, w, "SHELFVISION RETAIL PLANOGRAM & OSA COMPLIANCE AUDIT", "Outlet: MetroFresh Hypermarket BLR-104  |  Template:PLANO-BEV-Q4  |  SKU: SKU-XYZ-204", "OSA SCORE: 78.4% (ALERT)", (79, 70, 229))
    # Draw 3 retail shelves
    for s_idx, y_top in enumerate([130, 270, 410], 1):
        d4.rectangle([50, y_top + 100, 1050, y_top + 112], fill=(148, 163, 184))
        d4.text((60, y_top - 22), f"SHELF TIER 0{s_idx} — {'EYE-LEVEL CONTRACTED FACINGS (SKU-XYZ-204)' if s_idx==1 else 'SECONDARY CATEGORY ASSORTMENT'}", fill=(226, 232, 240), font=f_sm)
        for bx in range(80, 980, 110):
            if s_idx == 1 and bx in (410, 520):
                # Out of stock gap!
                d4.rectangle([bx, y_top + 10, bx + 95, y_top + 98], fill=(69, 10, 10), outline=(239, 68, 68), width=3)
                d4.text((bx + 10, y_top + 42), "OOS GAP", fill=(252, 165, 165), font=f_sm)
            else:
                color = (14, 165, 233) if s_idx == 1 else ((16, 185, 129) if s_idx == 2 else (245, 158, 11))
                d4.rectangle([bx, y_top + 12, bx + 92, y_top + 98], fill=color, outline=(255, 255, 255), width=2)
                d4.text((bx + 12, y_top + 45), "XYZ-204" if s_idx == 1 else f"FAC-{bx//110}", fill=(255, 255, 255), font=f_xs)
    d4.rectangle([50, 545, 1050, 650], fill=(15, 23, 42), outline=(99, 102, 241), width=2)
    d4.text((68, 560), "GEMINI 3.8 FLASH PLANOGRAM AUDIT & FIELD BEAT ACTION:", fill=(129, 140, 248), font=f_md)
    d4.text((68, 588), "• Detected 2 Missing Eye-Level Facings (OOS Gap) on Tier 01 + Missing Promo Wobbler Tag at Store BLR-104.", fill=(255, 255, 255), font=f_sm)
    d4.text((68, 614), "• Auto-dispatched Field Merchandiser Task TASK-MERCH-902 & triggered BeatSync van replenishment from FDC-XYZ-BENGALURU.", fill=(148, 163, 184), font=f_sm)
    p4 = img_dir / "XYZ_04_ShelfVision_Retail_Planogram_Audit.png"
    im4.save(p4)
    images_meta.append({"filename": p4.name, "path": f"demo_data/xyz_corporation/images/{p4.name}", "title": "ShelfVision Retail Store Planogram & OOS Gap Detection", "pillar": "05 · Deliver (TM&D)", "agent_id": "planogram_merchandising_vision_auditor"})

    # 5. AssetGuard CNC Spindle Vibration FFT Spectrogram
    im5 = Image.new("RGB", (w, h), (15, 23, 42))
    d5 = ImageDraw.Draw(im5)
    _draw_header_banner(d5, w, "ASSETGUARD CNC SPINDLE VIBRATION FFT SPECTROGRAM", "Plant: PLANT-XYZ-STUTTGART  |  Asset: CNC-MACH-04 (5-Axis Milling)  |  SKU: SKU-XYZ-309", "RMS: 4.82 mm/s (WARNING)", (217, 119, 6))
    # Draw FFT frequency plot area
    d5.rectangle([60, 110, 1040, 500], fill=(30, 41, 59), outline=(71, 85, 105), width=2)
    # Threshold line
    d5.line([(60, 230), (1040, 230)], fill=(239, 68, 68), width=2)
    d5.text((75, 206), "ISO 10816 CRITICAL ALARM THRESHOLD (4.50 mm/s RMS)", fill=(248, 113, 113), font=f_sm)
    # Draw spectrum bars
    for i in range(45):
        x = 85 + i * 21
        val = 35 + int(25 * abs(math.sin(i * 0.4)))
        bar_col = (56, 189, 248)
        if i in (27, 28, 29):
            val = 295 if i == 28 else 220
            bar_col = (239, 68, 68)
        d5.rectangle([x, 480 - val, x + 14, 480], fill=bar_col)
    d5.text((610, 150), "PEAK HARMONIC: 1,420 Hz (4.82 mm/s)\nOuter-Race Spindle Bearing Spall", fill=(252, 165, 165), font=f_md)
    d5.rectangle([60, 525, 1040, 645], fill=(30, 41, 59), outline=(245, 158, 11), width=2)
    d5.text((80, 542), "PREDICTIVE MAINTENANCE & MRO SPARE PARTS RESERVATION:", fill=(251, 191, 36), font=f_md)
    d5.text((80, 572), "• Remaining Useful Life (RUL): 34.5 operating hours before catastrophic spindle seizure ($185,000 avoided downtime).", fill=(255, 255, 255), font=f_sm)
    d5.text((80, 600), "• Reserved SKF Ceramic Bearing Kit (MRO-BRG-7741) in SAP PM & scheduled 2-hour preventive swap at Shift Handover.", fill=(148, 163, 184), font=f_sm)
    p5 = img_dir / "XYZ_05_AssetGuard_CNC_Vibration_FFT_Spectrogram.png"
    im5.save(p5)
    images_meta.append({"filename": p5.name, "path": f"demo_data/xyz_corporation/images/{p5.name}", "title": "AssetGuard CNC Spindle Bearing FFT Vibration Spectrogram", "pillar": "03 · Make", "agent_id": "plant_oee_maintenance_agent"})

    # 6. EcoChain EUDR Satellite Deforestation Polygon Verification
    im6 = Image.new("RGB", (w, h), (15, 23, 42))
    d6 = ImageDraw.Draw(im6)
    _draw_header_banner(d6, w, "GOOGLE EARTH ENGINE EUDR DEFORESTATION POLYGON VERIFICATION", "Supplier: SUP-XYZ-T1-SUMATRARUBBER  |  Plot: PLOT-IDN-882 (2.84°N, 98.67°E)  |  SKU: SKU-XYZ-625", "100% EUDR COMPLIANT", (22, 163, 74))
    # Left: 2020 Baseline NDVI | Right: 2026 Current Sentinel-2 NDVI
    for idx_p, (x0, lbl) in enumerate([(40, "DEC 2020 EUDR CUTOFF BASELINE (SENTINEL-2 NDVI: 0.84)"), (560, "OCT 2026 LIVE MULTISPECTRAL SCAN (SENTINEL-2 NDVI: 0.85)")]):
        d6.rectangle([x0, 105, x0 + 500, 510], fill=(20, 83, 45), outline=(34, 197, 94), width=3)
        d6.text((x0 + 18, 120), lbl, fill=(134, 239, 172), font=f_sm)
        # Canopy texture blocks
        for gx in range(x0 + 25, x0 + 475, 45):
            for gy in range(160, 480, 45):
                g_shade = 95 + ((gx * gy) % 55)
                d6.rectangle([gx, gy, gx + 40, gy + 40], fill=(16, g_shade, 48))
        # Geofence polygon
        poly = [(x0 + 110, 210), (x0 + 390, 190), (x0 + 430, 390), (x0 + 150, 430), (x0 + 110, 210)]
        d6.line(poly, fill=(56, 189, 248), width=4)
        d6.text((x0 + 145, 300), "GEOFENCE PLOT-IDN-882\nCanopy Loss: 0.00 ha\nPrimary Forest Intact", fill=(255, 255, 255), font=f_md)
    d6.rectangle([40, 535, 1060, 648], fill=(30, 41, 59), outline=(34, 197, 94), width=2)
    d6.text((60, 552), "EU DEFORESTATION REGULATION (EUDR) & CBAM CUSTOMS CLEARANCE:", fill=(74, 222, 128), font=f_md)
    d6.text((60, 582), "• Verified 0.0% tree cover loss across 412 hectares between Dec 31, 2020 and Oct 2026 via Google Earth Engine.", fill=(255, 255, 255), font=f_sm)
    d6.text((60, 610), "• TRACES NT Due Diligence Reference: EUDR-DDS-2026-99412 attached to Rotterdam Port Customs Declaration.", fill=(148, 163, 184), font=f_sm)
    p6 = img_dir / "XYZ_06_EcoChain_EUDR_Satellite_Deforestation_Scan.png"
    im6.save(p6)
    images_meta.append({"filename": p6.name, "path": f"demo_data/xyz_corporation/images/{p6.name}", "title": "EcoChain Earth Engine EUDR Satellite Polygon Scan", "pillar": "06 · Return & Enable", "agent_id": "carbon_scope3_ledger"})

    # 7. StormShield Typhoon Maritime AIS Corridor Reroute Radar
    im7 = Image.new("RGB", (w, h), (15, 23, 42))
    d7 = ImageDraw.Draw(im7)
    _draw_header_banner(d7, w, "STORMSHIELD GLOBAL MARITIME AIS & TYPHOON WAR ROOM RADAR", "Vessel: MV-AETHER-PRIDE (IMO 9841201)  |  Cargo: SKU-XYZ-101 & SKU-XYZ-412 ($4.8M at Risk)", "REROUTED + AIR BRIDGE", (225, 29, 72))
    d7.rectangle([40, 105, 1060, 515], fill=(12, 34, 64), outline=(56, 189, 248), width=2)
    # Typhoon vortex rings
    for r_rad, col_r in [(115, (127, 29, 29)), (80, (185, 28, 28)), (45, (239, 68, 68))]:
        d7.ellipse([480 - r_rad, 290 - r_rad, 480 + r_rad, 290 + r_rad], outline=col_r, width=4)
    d7.text((415, 280), "TYPHOON VONGFONG\n145 kt Sustained", fill=(254, 202, 202), font=f_sm)
    # Blocked Red Route vs Green Reroute
    d7.line([(120, 320), (480, 290), (920, 250)], fill=(239, 68, 68), width=3)
    d7.line([(120, 320), (460, 455), (920, 250)], fill=(16, 185, 129), width=5)
    d7.text((430, 468), "ACTIVE SOUTHERN BYPASS CORRIDOR (+38 hrs | 100% Safe)", fill=(52, 211, 153), font=f_md)
    d7.rectangle([40, 535, 1060, 648], fill=(30, 41, 59), outline=(225, 29, 72), width=2)
    d7.text((60, 552), "WAR ROOM PLAYBOOK EXECUTED (STORMSHIELD + AEROFREIGHT IN TANDEM):", fill=(251, 113, 133), font=f_md)
    d7.text((60, 582), "• Diverted MV-AETHER-PRIDE south of Luzon Strait; booked 4 LD3 air cargo ULDs (ULD-LD3-AERO-04) for critical buffer SKUs.", fill=(255, 255, 255), font=f_sm)
    d7.text((60, 610), "• Protected Stuttgart & Bengaluru assembly lines from line-stop ($4.8M revenue preserved).", fill=(148, 163, 184), font=f_sm)
    p7 = img_dir / "XYZ_07_StormShield_Typhoon_Maritime_AIS_Radar.png"
    im7.save(p7)
    images_meta.append({"filename": p7.name, "path": f"demo_data/xyz_corporation/images/{p7.name}", "title": "StormShield Maritime AIS & Typhoon Reroute Radar", "pillar": "Universal Core / 05 · Deliver", "agent_id": "disruption_war_room_orchestrator"})

    # 8. CubeMaster 3D Isometric LIFO Bay & Axle Load Blueprint
    im8 = Image.new("RGB", (w, h), (15, 23, 42))
    d8 = ImageDraw.Draw(im8)
    _draw_header_banner(d8, w, "CUBEMASTER 3D ISOMETRIC LIFO TRAILER BAY & AXLE TORQUE STUDIO", "Vehicle: TRK-T17-WEST-01 (53-ft / 17-Ton)  |  Shipment: SHP-XYZ-9088  |  Cube Utilization: 91.4%", "100% LIFO & CMVR 93", (14, 165, 233))
    d8.rectangle([40, 105, 1060, 515], fill=(30, 41, 59), outline=(56, 189, 248), width=2)
    # Draw trailer bay cross-section from Cab (left) to Rear Door (right)
    d8.rectangle([100, 175, 960, 425], fill=(15, 23, 42), outline=(148, 163, 184), width=3)
    d8.text((110, 145), "◀── CAB BULKHEAD (LAST STOP #4 LOADED FIRST)", fill=(148, 163, 184), font=f_sm)
    d8.text((620, 145), "REAR DOCK DOORS (FIRST STOP #1 LOADED LAST) ──▶", fill=(56, 189, 248), font=f_sm)
    zones = [
        (115, 315, "ZONE 4 (CAB)\nStop #4: Pune DC\nSKU-XYZ-309 (Heavy)\n4,200 kg", (99, 102, 241)),
        (325, 535, "ZONE 3 (MID-CAB)\nStop #3: Thane Hub\nSKU-XYZ-101 (CryoCell)\n4,650 kg", (14, 165, 233)),
        (545, 755, "ZONE 2 (MID-DOOR)\nStop #2: Andheri Retail\nSKU-XYZ-204 (Beverage)\n3,800 kg", (16, 185, 129)),
        (765, 945, "ZONE 1 (REAR DOOR)\nStop #1: Bandra Hyper\nSKU-XYZ-412 (Fragile Top)\n2,150 kg", (245, 158, 11)),
    ]
    for zx1, zx2, zlbl, zcol in zones:
        d8.rectangle([zx1, 195, zx2, 415], fill=zcol, outline=(255, 255, 255), width=2)
        d8.text((zx1 + 14, 265), zlbl, fill=(255, 255, 255), font=f_sm)
    # Wheels / Axles
    d8.ellipse([165, 425, 235, 495], fill=(51, 65, 85), outline=(226, 232, 240), width=3)
    d8.text((135, 498), "Steer Axle: 31.8% (Nominal)", fill=(52, 211, 153), font=f_xs)
    d8.ellipse([760, 425, 830, 495], fill=(51, 65, 85), outline=(226, 232, 240), width=3)
    d8.ellipse([845, 425, 915, 495], fill=(51, 65, 85), outline=(226, 232, 240), width=3)
    d8.text((735, 498), "Drive Tandem Axle: 68.2% (CMVR Rule 93 Pass)", fill=(52, 211, 153), font=f_xs)
    d8.rectangle([40, 535, 1060, 648], fill=(30, 41, 59), outline=(14, 165, 233), width=2)
    d8.text((60, 552), "3D GUILLOTINE PACKER & CRUSH-FRAGILITY PHYSICS VERIFICATION:", fill=(56, 189, 248), font=f_md)
    d8.text((60, 582), "• Vertical Support >= 88.5% across all upper tiers; fragile SKU-XYZ-412 placed on top tier with zero over-stacking.", fill=(255, 255, 255), font=f_sm)
    d8.text((60, 610), "• Eliminated 1 entire overflow LTL truck ($1,180 saved on SHP-XYZ-9088) and synced manifest to Manhattan Active WMS.", fill=(148, 163, 184), font=f_sm)
    p8 = img_dir / "XYZ_08_CubeMaster_3D_LIFO_Trailer_Load_Plan.png"
    im8.save(p8)
    images_meta.append({"filename": p8.name, "path": f"demo_data/xyz_corporation/images/{p8.name}", "title": "CubeMaster 3D LIFO Trailer Bay & Axle Physics Plan", "pillar": "05 · Deliver", "agent_id": "load_consolidation_agent"})

    print(f"[OK] Generated {len(images_meta)} high-res operational PNG images in {img_dir}")
    return images_meta


# ==============================================================================
# 4. Multi-Page Corporate PDF Documents Generator
# ==============================================================================
def _render_pdf_page(title: str, doc_code: str, pillar: str, sections: List[tuple[str, List[str]]], table_headers: List[str], table_rows: List[List[str]], page_num: int, total_pages: int) -> Image.Image:
    # 1240 x 1754 (A4 at 150 DPI)
    w, h = 1240, 1754
    im = Image.new("RGB", (w, h), (255, 255, 255))
    d = ImageDraw.Draw(im)
    f_h1 = _load_font(24, bold=True)
    f_h2 = _load_font(17, bold=True)
    f_b = _load_font(14, bold=False)
    f_b_bold = _load_font(14, bold=True)
    f_sm = _load_font(12, bold=False)

    # Top Corporate Header
    d.rectangle([0, 0, w, 115], fill=(15, 23, 42))
    d.rectangle([0, 110, w, 118], fill=(37, 99, 235))
    d.text((50, 22), f"{COMPANY_NAME}  —  OFFICIAL ENTERPRISE RECORD", fill=(148, 163, 184), font=f_sm)
    d.text((50, 48), title, fill=(255, 255, 255), font=f_h1)
    d.text((w - 380, 30), f"DOC ID: {doc_code}", fill=(56, 189, 248), font=f_b_bold)
    d.text((w - 380, 58), f"SCOR PILLAR: {pillar}", fill=(226, 232, 240), font=f_sm)
    d.text((w - 380, 80), f"DATE: 2026-10-22  |  PAGE {page_num} OF {total_pages}", fill=(148, 163, 184), font=f_sm)

    y = 150
    for sec_title, bullets in sections:
        d.rectangle([50, y, w - 50, y + 34], fill=(241, 245, 249), outline=(203, 213, 225))
        d.text((64, y + 7), sec_title, fill=(15, 23, 42), font=f_h2)
        y += 46
        for b_line in bullets:
            d.text((68, y), f"•  {b_line}", fill=(30, 41, 59), font=f_b)
            y += 28
        y += 16

    # Render Structured Table
    if table_headers and table_rows:
        d.text((50, y), "STRUCTURED ENTERPRISE LEDGER & VERIFICATION TABLE", fill=(15, 23, 42), font=f_h2)
        y += 32
        col_w = (w - 100) // len(table_headers)
        d.rectangle([50, y, w - 50, y + 34], fill=(30, 58, 138))
        for ci, th in enumerate(table_headers):
            d.text((58 + ci * col_w, y + 8), th, fill=(255, 255, 255), font=f_b_bold)
        y += 34
        for ri, rvals in enumerate(table_rows):
            bg = (248, 250, 252) if ri % 2 == 0 else (255, 255, 255)
            d.rectangle([50, y, w - 50, y + 32], fill=bg, outline=(203, 213, 225))
            for ci, val in enumerate(rvals):
                d.text((58 + ci * col_w, y + 7), str(val)[:32], fill=(15, 23, 42), font=f_sm)
            y += 32
        y += 28

    # Digital Signature & Audit Seal Box at bottom
    d.rectangle([50, h - 190, w - 50, h - 70], fill=(248, 250, 252), outline=(148, 163, 184), width=2)
    d.text((70, h - 172), "DIGITAL CRYPTOGRAPHIC AUDIT SEAL & ENTERPRISE SIGN-OFF", fill=(15, 23, 42), font=f_b_bold)
    d.text((70, h - 144), f"Organization: {COMPANY_NAME} ({COMPANY_CODE})  |  ERP Sync: SAP S/4HANA + Cloud Spanner Twin", fill=(51, 65, 85), font=f_sm)
    d.text((70, h - 120), "HMAC-SHA256 Verification Hash: 9f84c2a10e7b4d33a81e6c992b10d4f7e3a2118c6d004f9a  |  Status: APPROVED & VERIFIED", fill=(5, 150, 105), font=f_sm)
    d.text((70, h - 94), "Authorized By: Elena Rostova (CSCO)  &  Vertex AI Agent Engine Autonomous Governance Enclave", fill=(71, 85, 105), font=f_sm)
    return im


def build_pdf_documents(pdf_dir: Path) -> List[Dict[str, Any]]:
    pdf_dir.mkdir(parents=True, exist_ok=True)
    pdf_specs = [
        {
            "filename": "XYZ_Corp_Master_Supplier_MSA_and_Force_Majeure_2026.pdf",
            "title": "MASTER SUPPLIER SERVICES AGREEMENT (MSA) & FORCE MAJEURE",
            "doc_code": "MSA-XYZ-2026-01",
            "pillar": "02 · Source (ClauseGuard & SourcePulse)",
            "sections": [
                ("1. PARTIES & CONTRACTED DIRECT MATERIALS SCOPE", [
                    "Buyer: XYZ Global Industries Corp. (Stuttgart, Austin, Bengaluru, Monterrey Plants).",
                    "Primary Suppliers: AluWeld Thermal GmbH (VEND-900112) & Taiwan SiliconCore Co. (VEND-900245).",
                    "Covered Materials: SKU-XYZ-101 (CryoCell 800V Module), SKU-XYZ-412 (OmniSense Gateway), SKU-XYZ-518 (Heat Exchanger).",
                ]),
                ("2. PARAMETRIC SHOULD-COST INDEXATION & LME COMMODITY COLLARS", [
                    "Unit pricing is indexed quarterly to London Metal Exchange (LME) High-Grade Aluminum ($2,410/MT baseline).",
                    "Supplier non-raw-material conversion margin is capped at 11.5% under Clause 8.4 (audited by SourcePulse).",
                    "Early payment discount: 2/10 Net 45 (2.0% discount unlocked when AP invoice is settled within 10 days).",
                ]),
                ("3. FORCE MAJEURE, DUAL-SOURCING & LIQUIDATED DAMAGES (CLAUSE 14.2)", [
                    "In the event of typhoon, port closure, or geopolitical embargo > 48 hours, Supplier must notify StormShield within 4 hours.",
                    "Buyer reserves automatic right to shift up to 45% of allocation to secondary plant/supplier without penalty.",
                    "Late delivery below 96.0% OTIF incurs a 3.5% liquidated damages rebate credit in SAP Ariba.",
                ]),
            ],
            "headers": ["Clause Ref", "Supplier ID", "SKU Covered", "Price Cap / SLA", "Enforcement Agent"],
            "rows": [
                ["Clause 4.1", "SUP-XYZ-T1-ALUWELD", "SKU-XYZ-101", "LME + 11.5% Margin Cap", "rfq_should_cost_agent"],
                ["Clause 8.4", "SUP-XYZ-T1-SILICONCORE", "SKU-XYZ-412", "Dual-Source 65/35 Split", "tier_n_risk_sentinel"],
                ["Clause 12.1", "SUP-XYZ-T1-ASEPTIPACK", "SKU-XYZ-204", "Cpk >= 1.33 Mandatory", "supplier_quality_sentinel"],
                ["Clause 14.2", "ALL TIER-1 VENDORS", "ALL DIRECT SKUS", "4hr Force Majeure Alert", "tariff_esg_agent"],
            ],
        },
        {
            "filename": "XYZ_Corp_Supplier_Certificate_of_Analysis_COA_Batch_8841.pdf",
            "title": "SUPPLIER CERTIFICATE OF ANALYSIS (COA) & SPC CPK REPORT",
            "doc_code": "COA-XYZ-BATCH-8841",
            "pillar": "02 · Source / 03 · Make (QualiShield & VisionInspect)",
            "sections": [
                ("1. INCOMING LOT IDENTIFICATION & MATERIAL TRACEABILITY", [
                    "Lot / Batch Number: BATCH-XYZ-AUST-8841  |  Supplier: AseptiPack Foil & Closures (SUP-XYZ-T1-ASEPTIPACK).",
                    "Target Finished Good: SKU-XYZ-204 (Aseptic HydraPure Electrolyte Beverage 24-Pack) at PLANT-XYZ-AUSTIN.",
                    "Inspection Method: Document AI OCR Extraction + Inline GigE 120-FPS Optical Vision Verification.",
                ]),
                ("2. STATISTICAL PROCESS CONTROL (SPC) & CPK DRIFT FINDINGS", [
                    "Induction Foil Laminate Thickness: Spec 38.0 ± 2.0 microns | Measured Mean: 36.4 microns | Cpk = 1.18 (DRIFT ALERT).",
                    "Tensile Seal Burst Pressure: Spec >= 4.2 Bar | Measured: 4.45 Bar (PASS).",
                    "Action Taken: QualiShield placed Lot 8841 on Conditional Hold in SAP QM and issued SCAR-2026-119 + $14,200 COPQ Debit.",
                ]),
            ],
            "headers": ["Parameter", "Engineering Spec", "Measured Value", "SPC Cpk", "Lot Disposition"],
            "rows": [
                ["Foil Thickness", "38.0 +/- 2.0 um", "36.4 um", "1.18 (Drift)", "CONDITIONAL_HOLD"],
                ["Burst Pressure", ">= 4.20 Bar", "4.45 Bar", "1.64 (Nominal)", "PASSED"],
                ["Polymer Coating", "12.0 +/- 0.8 g/m2", "11.9 g/m2", "1.71 (Nominal)", "PASSED"],
                ["Heat Seal Tear", "0.0% Micro-Leaks", "1 Unit Diverted", "98.5% Vision Conf", "GATE_DIVERTED"],
            ],
        },
        {
            "filename": "XYZ_Corp_Commercial_Invoice_and_Customs_BOL_SHP9041.pdf",
            "title": "COMMERCIAL INVOICE, PACKING LIST & CUSTOMS BILL OF LADING",
            "doc_code": "INV-BOL-SHP-9041",
            "pillar": "05 · Deliver / 02 · Source (ClauseGuard, PortWatch & SentinelMove)",
            "sections": [
                ("1. CROSS-BORDER CONSIGNMENT & VESSEL MANIFEST", [
                    "Shipment ID: SHP-XYZ-9041  |  Purchase Order: PO-XYZ-880142  |  Sales Order: SO-XYZ-20261022-801.",
                    "Exporter: XYZ Stuttgart Plant (DE)  ->  Consignee: XYZ Midwest Mega-RDC Chicago (US) via Rotterdam Europort.",
                    "Ocean Vessel: MV-AETHER-PRIDE (Container MSKU-884120-9, 40ft High-Cube Reefers).",
                ]),
                ("2. HARMONIZED TARIFF SCHEDULE (HTS) & DUTY OPTIMIZATION", [
                    "Classified under HTS 8507.60.0020 (Lithium-Ion Thermal Battery Modules) & HTS 8481.20.0050 (Hydraulic Manifolds).",
                    "Verified USMCA / EU-FTA Preferential Origin Certificate attached; zero customs hold at Port of Discharge.",
                ]),
            ],
            "headers": ["Line", "SKU ID", "HTS Tariff Code", "Qty (Units)", "Total Value (USD)"],
            "rows": [
                ["001", "SKU-XYZ-101 (CryoCell 800V)", "8507.60.0020", "450 EA", "$308,250.00"],
                ["002", "SKU-XYZ-309 (CNC Manifold)", "8481.20.0050", "280 EA", "$151,200.00"],
                ["003", "SKU-XYZ-518 (Heat Exchanger)", "8419.50.5000", "320 EA", "$78,400.00"],
                ["TOTAL", "3 CONTAINERIZED LOTS", "INCOTERMS DDP", "1,050 EA", "$537,850.00"],
            ],
        },
        {
            "filename": "XYZ_Corp_EU_CBAM_Embedded_Carbon_and_EUDR_Certificate.pdf",
            "title": "EU CBAM EMBEDDED CARBON & EUDR DUE DILIGENCE CERTIFICATE",
            "doc_code": "ESG-CBAM-2026-882",
            "pillar": "06 · Return & Enable (EcoChain Scope-3 & CBAM Ledger)",
            "sections": [
                ("1. ISO 14083 & GLEC v3.0 SHIPMENT-LEVEL SCOPE-3 ACCOUNTING", [
                    "Reporting Entity: XYZ Global Industries Corp.  |  EU EORI: DE8841920144.",
                    "Replaced generic Spend-Based secondary averages with primary smelter & carrier telematics (-31.4% CBAM tax liability).",
                    "Barge & Road Corridor switched to HVO100 Renewable Diesel on Rotterdam -> Stuttgart lane.",
                ]),
                ("2. EUDR GEOSPATIAL POLYGON DEFORESTATION VERIFICATION", [
                    "Natural Rubber SKU-XYZ-625 traced to Plot PLOT-IDN-882 (2.84°N, 98.67°E, North Sumatra).",
                    "Google Earth Engine Sentinel-2 analysis confirmed 0.00 hectares canopy loss post-Dec 31, 2020.",
                ]),
            ],
            "headers": ["SKU / Shipment", "Regulation", "Primary Metric", "Verified Value", "Audit Status"],
            "rows": [
                ["SKU-XYZ-101", "EU CBAM (Aluminum)", "Embedded Carbon", "1.48 tCO2e / t", "PRIMARY_SMELTER_CERT"],
                ["SKU-XYZ-518", "EU CBAM (Brazed Core)", "Embedded Carbon", "1.62 tCO2e / t", "PRIMARY_SMELTER_CERT"],
                ["SKU-XYZ-625", "EU EUDR (Elastomer)", "Post-2020 Canopy Loss", "0.00 Hectares", "EARTH_ENGINE_PASSED"],
                ["SHP-XYZ-9041", "ISO 14083 / GLEC v3", "WTW Transport CO2e", "1,420.5 kg CO2e", "HVO100_BIOFUEL_SWAP"],
            ],
        },
        {
            "filename": "XYZ_Corp_21CFR11_Electronic_Batch_Record_eBHR_8841.pdf",
            "title": "21 CFR PART 11 ELECTRONIC BATCH MANUFACTURING RECORD (eBHR)",
            "doc_code": "EBHR-AUST-8841",
            "pillar": "03 · Make (VisionInspect, YieldMax & SyncChange)",
            "sections": [
                ("1. BATCH EXECUTION & INLINE MULTIMODAL VISION TELEMETRY", [
                    "Facility: PLANT-XYZ-AUSTIN (Aseptic Bottling Line 03)  |  Batch Size: 24,000 Units of SKU-XYZ-204.",
                    "At 10:14:22.418 UTC, GigE Camera #2 captured Frame FRAME-00841 showing an induction foil seal micro-tear.",
                    "Gemini 3.8 Flash classified INDUCTION_FOIL_SEAL_TEAR (98.5% confidence) in 11.4ms; Pneumatic Gate DIVERT-01 fired in 14.2ms.",
                ]),
                ("2. CLOSED-LOOP PLC PARAMETER CORRECTION & LOT RELEASE", [
                    "YieldMax correlated foil tear to induction coil voltage droop (-4.2V) and restored nominal 240.0V setpoint via OPC-UA.",
                    "23,999 conforming units passed hermetic seal verification and were released to Warehouse Slot A-01.",
                ]),
            ],
            "headers": ["Timestamp UTC", "Event / Frame ID", "Telemetry Reading", "Automated Action", "21 CFR 11 Sign-Off"],
            "rows": [
                ["10:14:22.406", "FRAME-00841 Capture", "4,200 Lux / 120 FPS", "Sent to Gemini 3.8 Flash", "SYS-VISION-03"],
                ["10:14:22.418", "Defect Classified", "98.5% Conf (Foil Tear)", "Trigger DIVERT-01 Gate", "AGENT-VISIONINSPECT"],
                ["10:14:22.432", "Solenoid Actuated", "14.2ms Gate Latency", "Unit in Quarantine Bin 1", "PLC-MODBUS-01"],
                ["10:15:00.000", "eBHR Deviation Log", "VEEVA-DEV-2026-8841", "Batch Released (99.99%)", "QA-DIR-AUSTIN"],
            ],
        },
        {
            "filename": "XYZ_Corp_Transporter_Lorry_Receipt_Challan_and_POD_SHP9088.pdf",
            "title": "TRANSPORTER LORRY RECEIPT (LR CHALLAN), 3D LOAD & DIGITAL POD",
            "doc_code": "LR-POD-SHP-9088",
            "pillar": "05 · Deliver / 06 · Return (FleetFlow, CubeMaster 3D & OTIF Shield)",
            "sections": [
                ("1. COMMERCIAL VEHICLE & CORRIDOR DISPATCH MANIFEST", [
                    "Origin Hub: FDC-XYZ-MUMBAI (Bhiwandi)  |  Corridor: WEST EXPRESSWAY  |  Vehicle: TRK-T17-WEST-01 (Driver: Ravi Sharma).",
                    "Total Consignment: 68 Cartons (14,800 kg, 91.4% Cube Utilization) loaded in strict Reverse-Stop LIFO sequence.",
                    "CMVR Rule 93 Axle Weight Balance: Steer Axle 31.8% / Drive Tandem 68.2% (100% Statutory Compliant).",
                ]),
                ("2. GEOFENCE ARRIVAL TELEMETRY & RETAILER OTIF CHARGEBACK SHIELD", [
                    "GPS Geofence Entry at Customer Dock (CUST-XYZ-TIER1-MEGAMART): 07:42:11 Local Time (18 mins ahead of 08:00 SLA).",
                    "EDI 856 ASN & Digital Proof of Delivery (POD) countersigned; $8,400 erroneous OTIF penalty automatically refuted.",
                ]),
            ],
            "headers": ["Stop #", "Customer / Outlet", "Bay Zone (LIFO)", "Cartons / Weight", "GPS Arrival & POD"],
            "rows": [
                ["Stop 1", "Bandra Hypermarket", "Zone 1 (0-180cm Door)", "14 ctn / 2,150 kg", "07:42 (ON-TIME POD)"],
                ["Stop 2", "Andheri Retail Hub", "Zone 2 (180-360cm)", "22 ctn / 3,800 kg", "09:15 (ON-TIME POD)"],
                ["Stop 3", "Thane Cold-Storage", "Zone 3 (360-540cm)", "18 ctn / 4,650 kg", "11:05 (ON-TIME POD)"],
                ["Stop 4", "Pune Express Depot", "Zone 4 (540-720cm Cab)", "14 ctn / 4,200 kg", "13:20 + RMA Backhaul"],
            ],
        },
        {
            "filename": "XYZ_Corp_CSCO_Executive_Board_Briefing_and_WarRoom_Dossier.pdf",
            "title": "OFFICE OF THE CSCO — EXECUTIVE CONTROL TOWER & S&OP DOSSIER",
            "doc_code": "CSCO-BOARD-2026-Q4",
            "pillar": "Universal CSCO Core (TowerMind, StormShield, MasterGuard & CashBridge)",
            "sections": [
                ("1. ENTERPRISE-WIDE GOLDEN THREAD PERFORMANCE SUMMARY", [
                    "Global Forecast Accuracy (WAPE): Improved from 24.8% error to 11.2% via PulseCast + WeatherNext 3 + TimesFM.",
                    "Multi-Echelon Inventory Working Capital: Released $42.6M in trapped cash while lifting service level to 98.7%.",
                    "Fleet & 3D Load Consolidation: Reduced daily truck dispatches by 20% and eliminated 100% of LIFO re-handling.",
                ]),
                ("2. AUTONOMOUS AGENT TANDEM ORCHESTRATION AUDIT", [
                    "All 35 AI Agents across 6 ASCM SCOR Pillars + Universal Core operate on shared XYZ Corp ERP/Spanner master IDs.",
                    "Every mutation action is gated by deterministic delegation limits ($2.0M CSCO cap) and idempotency keys.",
                ]),
            ],
            "headers": ["SCOR Pillar", "Flagship Agents Live", "Primary Business KPI", "Verified Financial Impact"],
            "rows": [
                ["Universal Core", "TowerMind & StormShield", "Disruption Recovery Time", "14 Days -> 4 Hours ($18.4M)"],
                ["01 · Plan", "PulseCast & Synapse", "Consensus S&OP Margin", "+$14.2M Q4 Gross Margin"],
                ["02 · Source", "SourcePulse & NexusShield", "Direct Material Should-Cost", "-6.8% RFQ Overcharge Saved"],
                ["03 · Make", "AssetGuard & VisionInspect", "Unplanned Downtime & Scrap", "-41% Downtime / 0 Escapes"],
                ["04 · Fulfill", "EchelonFlow & PromiseGuard", "MEIO Safety Stock Capital", "-$22.4M Working Capital"],
                ["05 · Deliver", "FleetFlow & CubeMaster 3D", "Fleet Trucks & Cube Fill", "10->8 Trucks / 91.4% Cube"],
                ["06 · Return", "ReturnLoop & EcoChain", "RMA Recovery & CBAM Tax", "94% Grade-A / -31% CBAM"],
            ],
        },
    ]

    manifest_pdfs = []
    for spec in pdf_specs:
        page1 = _render_pdf_page(
            spec["title"],
            spec["doc_code"],
            spec["pillar"],
            spec["sections"],
            spec["headers"],
            spec["rows"],
            page_num=1,
            total_pages=2,
        )
        # Page 2: Cross-Agent Tandem Lineage & Appendix
        page2 = _render_pdf_page(
            f"{spec['title']} — APPENDIX: CROSS-AGENT TANDEM LINEAGE",
            spec["doc_code"],
            spec["pillar"],
            [
                ("4. CROSS-PILLAR AGENT HANDOFF & GOLDEN THREAD TRACEABILITY", [
                    "This document is automatically indexed in AlloyDB pgvector and linked to BigQuery dataset `supply_chain_twin`.",
                    "Shared Enterprise SKUs referenced: SKU-XYZ-101, SKU-XYZ-204, SKU-XYZ-309, SKU-XYZ-412, SKU-XYZ-518, SKU-XYZ-625.",
                    "Shared Facilities referenced: PLANT-XYZ-STUTTGART, PLANT-XYZ-AUSTIN, PLANT-XYZ-BENGALURU, RDC-XYZ-CHICAGO, FDC-XYZ-MUMBAI.",
                ]),
                ("5. GOVERNANCE, MODEL ARMOR & DETERMINISTIC QUALITY GATES", [
                    "All agent write-backs require pre-execution `enforce_tool_contract()` validation and a unique `idempotency_key`.",
                    "PII, vendor bank coordinates, and GSTIN/tax identifiers are tokenized via Google Cloud DLP prior to LLM context injection.",
                ]),
            ],
            ["Golden Thread ID", "SKU ID", "Purchase Order", "Production Batch", "Sales Order / Shipment"],
            [[g["golden_thread_id"], g["sku_id"], g["purchase_order_id"], g["production_batch_id"], f"{g['sales_order_id']} / {g['shipment_id']}"] for g in GOLDEN_THREAD_TRANSACTIONS],
            page_num=2,
            total_pages=2,
        )
        out_pdf = pdf_dir / spec["filename"]
        page1.save(out_pdf, "PDF", resolution=150.0, save_all=True, append_images=[page2])
        manifest_pdfs.append({
            "filename": spec["filename"],
            "path": f"demo_data/xyz_corporation/pdfs/{spec['filename']}",
            "title": spec["title"],
            "doc_code": spec["doc_code"],
            "pillar": spec["pillar"],
            "format": "PDF",
            "pages": 2,
            "size_kb": round(out_pdf.stat().st_size / 1024, 1),
        })
    print(f"[OK] Generated {len(manifest_pdfs)} multi-page PDF documents in {pdf_dir}")
    return manifest_pdfs


# ==============================================================================
# 5. Microsoft Word (.docx) SOPs, Unstructured Emails (.eml) & EDI (.edi)
# ==============================================================================
def _write_docx(path: Path, title: str, subtitle: str, paragraphs: List[str]) -> None:
    """Writes a standard OpenXML .docx file readable by Microsoft Word, Google Docs & LibreOffice."""
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>"""
    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

    def _esc(s: str) -> str:
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    p_xml = [
        f'<w:p><w:r><w:rPr><w:b/><w:sz w:val="32"/></w:rPr><w:t>{_esc(title)}</w:t></w:r></w:p>',
        f'<w:p><w:r><w:rPr><w:i/><w:sz w:val="22"/></w:rPr><w:t>{_esc(subtitle)}</w:t></w:r></w:p>',
    ]
    for para in paragraphs:
        p_xml.append(f'<w:p><w:r><w:rPr><w:sz w:val="22"/></w:rPr><w:t>{_esc(para)}</w:t></w:r></w:p>')

    doc_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        "<w:body>" + "".join(p_xml) + "</w:body></w:document>"
    )
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("word/document.xml", doc_xml)


def build_docs_emails_and_edi(docs_dir: Path) -> List[Dict[str, Any]]:
    docs_dir.mkdir(parents=True, exist_ok=True)
    items = []

    docx_specs = [
        (
            "XYZ_Corp_Global_Supply_Chain_SOP_and_Delegation_Matrix.docx",
            "XYZ Global Industries Corp — Global Supply Chain SOP & Delegation of Authority Matrix",
            "Policy ID: SOP-CSCO-2026-001 | Effective across all 6 SCOR Pillars & 35 AI Agents",
            [
                "1. PURPOSE: Establish unified operational governance across Demand Planning, Strategic Sourcing, Manufacturing, Multi-Echelon Fulfillment, Multi-Modal Logistics, and Circular Returns for XYZ Global Industries Corp.",
                "2. DELEGATION OF AUTHORITY: Autonomous AI Agent execution is authorized up to $2,000,000 USD per playbook for the CSCO Control Tower Copilot (TowerMind). Actions above $2,000,000 require dual CSCO + CFO electronic sign-off.",
                "3. MANDATORY IDEMPOTENCY & QUALITY GATES: Every ERP/WMS/TMS write-back tool must pass a non-empty idempotency_key and validate entity master codes (SKU-XYZ-*, PLANT-XYZ-*, SUP-XYZ-*).",
                "4. CROSS-PILLAR TANDEM WORKFLOW: When PulseCast detects a >12% demand surge, it triggers Synapse S&OP capacity balancing, SourcePulse raw-material RFQ checks, EchelonFlow safety-stock reallocation, and FleetFlow corridor dispatch.",
            ],
        ),
        (
            "XYZ_Corp_Disruption_WarRoom_and_MultiModal_Reroute_Playbook.docx",
            "XYZ Global Industries Corp — Geopolitical & Typhoon Disruption War Room Playbook",
            "Policy ID: SOP-RISK-2026-002 | StormShield, NexusShield, PortWatch & AeroFreight",
            [
                "1. TRIGGER THRESHOLD: Activated automatically when Spire Maritime AIS or WeatherNext 3 detects a Category 3+ typhoon or port strike impacting >$1,000,000 in active shipments.",
                "2. MARITIME REROUTING: Vessel MV-AETHER-PRIDE reroutes via Southern Bypass Corridor; PortWatch shifts drayage appointments from congested terminals to off-peak gates.",
                "3. AIR CARGO BRIDGE: AeroFreight books belly-hold LD3/LD7 ULDs for critical A-velocity SKUs (SKU-XYZ-101, SKU-XYZ-412) with <72 hours plant line buffer.",
            ],
        ),
        (
            "XYZ_Corp_Quality_21CFR11_and_Supplier_SCAR_Protocol.docx",
            "XYZ Global Industries Corp — 21 CFR Part 11 Inline Quality & Supplier SCAR Protocol",
            "Policy ID: SOP-QUAL-2026-003 | VisionInspect, QualiShield, YieldMax & AssetGuard",
            [
                "1. INLINE VISION THRESHOLD: GigE 120-FPS optical cameras classify every unit with Gemini 3.8 Flash. Any critical seal or crack defect >= 0.95 confidence fires the pneumatic reject gate within 15 milliseconds.",
                "2. SUPPLIER CPK DRIFT: Incoming lots with Cpk < 1.33 on critical dimensions (e.g., Batch BATCH-XYZ-AUST-8841 foil thickness Cpk 1.18) trigger automatic SAP QM quarantine and Cost of Poor Quality (COPQ) debit notes.",
            ],
        ),
        (
            "XYZ_Corp_Circular_RMA_and_ISO14083_ESG_Compliance_Manual.docx",
            "XYZ Global Industries Corp — Circular RMA Grading, CBAM & EUDR Compliance Manual",
            "Policy ID: SOP-ESG-2026-004 | ReturnLoop, OTIF Penalty Shield & EcoChain",
            [
                "1. OPTICAL RMA GRADING: Customer returns are graded via Gemini 3.8 Flash into Grade-A (Factory Seal Intact -> Direct FDC Restock, 94% recovery), Grade-B (Certified Refurb), and Grade-C (Component Harvest).",
                "2. EMPTY BACKHAUL MATCHING: ReturnLoop pairs retail RMA pickups with returning FleetFlow delivery trucks (<5 km detour) to eliminate LTL reverse freight.",
                "3. CBAM & EUDR: Every import into the EU must attach primary smelter carbon declarations and Google Earth Engine zero-deforestation polygon verification.",
            ],
        ),
    ]

    for fname, title, sub, paras in docx_specs:
        fpath = docs_dir / fname
        _write_docx(fpath, title, sub, paras)
        items.append({
            "filename": fname,
            "path": f"demo_data/xyz_corporation/docs/{fname}",
            "title": title,
            "format": "DOCX",
            "size_kb": round(fpath.stat().st_size / 1024, 1),
        })

    # Unstructured Emails (.eml)
    eml_path = docs_dir / "XYZ_Corp_Unstructured_Customer_and_Carrier_Emails.eml"
    eml_content = """From: dispatch-alerts@megamart-retail.com
To: order-desk@xyz-corp.com, fleetflow-intake@xyz-corp.com
Subject: URGENT RUSH ORDER & PROMO LIFT: SO-XYZ-20261022-802 (Midwest & Mumbai Hubs)
Date: Thu, 22 Oct 2026 06:15:00 +0000
Content-Type: text/plain; charset="utf-8"

Team XYZ Global Industries,

Due to the 38C heatwave alert and weekend end-cap promotion, please expedite our replenishment order SO-XYZ-20261022-802:
1. SKU-XYZ-204 (Aseptic HydraPure 24-Pack): 1,200 Cases -> Deliver before 08:00 AM window (Dock Door #4).
2. SKU-XYZ-101 (CryoCell 800V Module): 85 Units -> Require strict LIFO loading at rear door for immediate cross-dock.
3. Also, we have 12 unopened cartons under RMA-20261022-501 (factory tamper seal intact) ready for backhaul pickup when your driver Ravi arrives on truck TRK-T17-WEST-01.

---
From: marine-ops@spire-ais-alerts.com
To: war-room@xyz-corp.com
Subject: TYPHOON VONGFONG ALERT — Vessel MV-AETHER-PRIDE (Shipment SHP-XYZ-9041)
Date: Thu, 22 Oct 2026 06:42:00 +0000

ALERT: Typhoon Vongfong (145 kt) is intersecting the Luzon Strait corridor.
Impacted XYZ Corp Purchase Orders: PO-XYZ-880142 & PO-XYZ-880355 (SKU-XYZ-101, SKU-XYZ-412).
Recommended Action: Convene StormShield War Room, reroute vessel via Southern Bypass, and allocate 4 LD3 air cargo ULDs for Stuttgart & Bengaluru plant buffer protection.
"""
    eml_path.write_text(eml_content, encoding="utf-8")
    items.append({
        "filename": eml_path.name,
        "path": f"demo_data/xyz_corporation/docs/{eml_path.name}",
        "title": "Unstructured Customer Rush Order, RMA Pickup & Typhoon Carrier Alert Emails",
        "format": "EML",
        "size_kb": round(eml_path.stat().st_size / 1024, 1),
    })

    # X12 EDI Stream (.edi)
    edi_path = docs_dir / "XYZ_Corp_X12_EDI_850_856_210_417_Stream.edi"
    edi_content = """ISA*00*          *00*          *ZZ*XYZCORP01      *ZZ*MEGAMART01     *261022*0630*U*00401*000090412*0*P*>~
GS*PO*MEGAMART01*XYZCORP01*20261022*0630*90412*X*004010~
ST*850*0001~
BEG*00*SA*PO-XYZ-880219**20261022~
REF*DP*01-PLAN-DEMAND-SOP~
N1*ST*FDC-XYZ-ATLANTA*92*PLANT-XYZ-AUSTIN~
PO1*1*1200*CA*28.50*PE*VP*SKU-XYZ-204*MG*MAT-2000319~
PO1*2*85*EA*685.00*PE*VP*SKU-XYZ-101*MG*MAT-1000841~
CTT*2~
SE*8*0001~
ST*856*0002~
BSN*00*SHP-XYZ-9088*20261022*0742*0001~
DTM*011*20261022*0742*LT~
REF*BM*LR-POD-SHP-9088~
REF*CN*TRK-T17-WEST-01~
HL*1**S~
TD5*B*2*FLEETFLOW*M*WEST-CORRIDOR-LIFO~
SE*7*0002~
ST*210*0003~
B3**INV-CARRIER-210-9088*SHP-XYZ-9088*PP*L*20261022*184500****20261022~
N1*CA*TRANSGLOBAL-FREIGHT*2*SCAC-TGLF~
LX*1~
L1*1*1845.00*FR*184500****LHF~
SE*6*0003~
GE*3*90412~
IEA*1*000090412~
"""
    edi_path.write_text(edi_content, encoding="utf-8")
    items.append({
        "filename": edi_path.name,
        "path": f"demo_data/xyz_corporation/docs/{edi_path.name}",
        "title": "X12 EDI Transaction Stream (EDI 850 PO, EDI 856 ASN, EDI 210 Freight Invoice)",
        "format": "EDI",
        "size_kb": round(edi_path.stat().st_size / 1024, 1),
    })

    print(f"[OK] Generated {len(items)} Word (.docx), Email (.eml), and X12 (.edi) files in {docs_dir}")
    return items


# ==============================================================================
# 6. Export Shared Organizational Master Tables & Sync into demo_data/tables/
# ==============================================================================
def export_org_tables(org_tables_dir: Path, main_tables_dir: Path) -> List[Dict[str, Any]]:
    org_tables_dir.mkdir(parents=True, exist_ok=True)
    main_tables_dir.mkdir(parents=True, exist_ok=True)

    org_datasets = {
        "xyz_erp_material_master_mara": ENTERPRISE_SKUS,
        "xyz_enterprise_facility_network": ENTERPRISE_FACILITIES,
        "xyz_vendor_master_lfa1": ENTERPRISE_SUPPLIERS,
        "xyz_customer_master_kna1": ORG_CUSTOMER_MASTER,
        "xyz_finance_gl_cost_centers": ORG_FINANCE_GL_COST_CENTERS,
        "xyz_hr_plant_shift_rosters": ORG_HR_PLANT_SHIFT_ROSTERS,
        "xyz_golden_thread_order_ledger": GOLDEN_THREAD_TRANSACTIONS,
    }

    exported = []
    for tbl_name, rows in org_datasets.items():
        for target_dir in (org_tables_dir, main_tables_dir):
            jp = target_dir / f"{tbl_name}.json"
            cp = target_dir / f"{tbl_name}.csv"
            jp.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
            headers, r_list = _dict_list_to_headers_rows(rows)
            with cp.open("w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(headers)
                for r in r_list:
                    w.writerow([json.dumps(x) if isinstance(x, (list, dict)) else x for x in r])
        exported.append({
            "table_name": tbl_name,
            "row_count": len(rows),
            "scope": "Enterprise Backbone (Shared Across All 35 Agents & Non-Agent ERP/HR/Finance)",
            "json_path": f"demo_data/xyz_corporation/tables/{tbl_name}.json",
            "csv_path": f"demo_data/xyz_corporation/tables/{tbl_name}.csv",
        })
    print(f"[OK] Exported {len(exported)} shared XYZ Corporation master & org tables (.json & .csv)")
    return exported


def load_all_existing_agent_tables() -> Dict[str, List[Dict[str, Any]]]:
    res: Dict[str, List[Dict[str, Any]]] = {}
    for p in sorted((ROOT / "agents").glob("*/fixtures/tables/*.json")):
        try:
            res[p.stem] = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return res


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    all_agent_tables = load_all_existing_agent_tables()

    excel_items = build_excel_workbooks(OUT_DIR / "excel", all_agent_tables)
    pdf_items = build_pdf_documents(OUT_DIR / "pdfs")
    image_items = build_operational_images(OUT_DIR / "images")
    doc_items = build_docs_emails_and_edi(OUT_DIR / "docs")
    org_tables = export_org_tables(OUT_DIR / "tables", ROOT / "demo_data" / "tables")

    manifest = {
        "company_name": COMPANY_NAME,
        "company_code": COMPANY_CODE,
        "fiscal_year": FISCAL_YEAR,
        "description": "End-to-End Multi-Modal Enterprise Demo Data Universe spanning 35 AI Agents across 6 ASCM SCOR Pillars + Universal Core AND organizational ERP/HR/Finance/Legal systems outside individual agents.",
        "summary_counts": {
            "agent_digital_twin_tables": len(all_agent_tables),
            "enterprise_org_backbone_tables": len(org_tables),
            "total_relational_tables": len(all_agent_tables) + len(org_tables),
            "excel_workbooks_xlsx": len(excel_items),
            "pdf_documents": len(pdf_items),
            "operational_vision_images_png": len(image_items),
            "word_docs_edi_emails": len(doc_items),
        },
        "shared_golden_thread_entities": {
            "skus": [s["sku_id"] for s in ENTERPRISE_SKUS],
            "facilities": [f["facility_id"] for f in ENTERPRISE_FACILITIES],
            "suppliers": [s["supplier_id"] for s in ENTERPRISE_SUPPLIERS],
            "customers": [c["customer_id"] for c in ORG_CUSTOMER_MASTER],
            "golden_threads": GOLDEN_THREAD_TRANSACTIONS,
        },
        "excel_workbooks": excel_items,
        "pdf_documents": pdf_items,
        "images": image_items,
        "docs_and_streams": doc_items,
        "org_backbone_tables": org_tables,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    manifest_path = OUT_DIR / "xyz_enterprise_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"\n✅ XYZ Corporation Multi-Modal Enterprise Demo Universe built at {manifest_path}")


if __name__ == "__main__":
    main()

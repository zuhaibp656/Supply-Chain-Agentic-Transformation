"""Division-Aware Domain Intelligence & Pre-Seeded Flagship Twin Synthesizer.

Serves two critical roles:
  1. Pre-seeds ultra-accurate, executive-grade flagship division twins (e.g.,
     `ITC Limited — Cigarettes & Leaf Tobacco (ILTD & TM&D)`,
     `ITC Limited — Foods Division`,
     `Aditya Birla Group — UltraTech Cement`,
     `Aditya Birla Group — Hindalco Metals`,
     `Unilever — Home & Personal Care`)
     with real downloaded corporate logos, authentic division terminology, LinkedIn/Naukri-grounded
     corporate job titles across all 60 SCOR Personas, renamed 20 Sub-Pillars, and smart Agent
     relevance filtering (`is_relevant: False` for inapplicable agents).
  2. Acts as an instant resilience fallback if local developer RAPT credentials expire offline,
     while Cloud Run's IAM Service Account always executes live Vertex AI Gemini 3.1 Pro + Search Grounding.
"""

from __future__ import annotations

import re
from typing import Any, Callable, Dict, List, Optional, Set

from enterprise_twin.schema import (
    AgentRelevanceSpec,
    CompanyBrandSpec,
    GroundingCitation,
    PersonaOverrideSpec,
    PillarOverrideSpec,
    ProcessJourneyOverrideSpec,
    SubPillarOverrideSpec,
    TwinOverlaySpec,
    clamp_brand_hex,
    load_canonical_catalog,
    make_twin_slug,
    validate_and_normalize_overlay,
)
from enterprise_twin.tools.logo_resolver import resolve_company_logo

# Agents associated with specific physical/channel traits for intelligent hiding
COLD_CHAIN_AGENT_IDS = {"cold_chain_auditor"}
FOOD_PERISHABLE_AGENT_IDS = {"food_waste_esg_copilot", "dynamic_markdown_agent"}
RETAIL_STORE_PLANOGRAM_AGENT_IDS = {
    "planogram_merchandising_vision_auditor",
    "aisle_aligned_pallet_agent",
    "curfew_orchestrator",
}
D2C_ECOMMERCE_PARCEL_AGENT_IDS = {
    "atp_order_promising_agent",
    "keep_it_routing_advisor",
    "address_geocoding_agent",
    "geocoding_intelligence_agent",
}


DIVISION_ARCHETYPES: Dict[str, Dict[str, Any]] = {
    "tobacco_tmd": {
        "sector": "FMCG · Leaf Tobacco, Primary/Secondary Manufacturing & TM&D",
        "accent": "#0ea5e9",
        "secondary": "#1e3a8a",
        "exec_title": "Divisional Chief Executive & Head of Supply Chain (ITD, ILTD & TM&D)",
        "thesis_tpl": (
            "Synchronizing {co}'s leaf tobacco auction procurement (ILTD), green-leaf threshing and "
            "high-speed cigarette making & packing plants (PMD/SMD), excise-bonded mother warehouses, "
            "and Trade Marketing & Distribution (TM&D) across Wholesale Dealers (WDs) and retail outlets."
        ),
        "sites_tpl": "Bengaluru, Saharanpur, Munger, Kolkata (Kidderpore) & Ranjangaon Cigarette Plants · Chirala & Anaparti ILTD Leaf Threshing · National TM&D Mother Depots",
        "erp": "SAP S/4HANA · SAP IBP · ILTD Leaf Auction Traceability · TM&D DMS (Distributor Management System) · Excise Bonded WMS",
        "terms": [
            "TM&D — Trade Marketing & Distribution",
            "ILTD — India Leaf Tobacco Division",
            "PMD / SMD — Primary & Secondary Manufacturing",
            "WD — Exclusive Wholesale Dealer Network",
        ],
        "career_titles": [
            "Branch Manager — Trade Marketing & Distribution (TM&D)",
            "Manager — Leaf Operations & Auction Procurement (ILTD)",
            "Operations Manager — Primary & Secondary Making/Packing (PMD/SMD)",
            "Head of Divisional Supply Chain & Excise Logistics",
            "Area Executive — Wholesale Dealer (WD) Channel",
            "Manager — Packaging & Filter Rod Materials Sourcing",
        ],
        "hide_agents": COLD_CHAIN_AGENT_IDS | FOOD_PERISHABLE_AGENT_IDS | {"atp_order_promising_agent", "keep_it_routing_advisor"},
        "hide_reason": "Hidden for Tobacco & TM&D fit: dry ambient excise-bonded B2B Wholesale Dealer channel (no frozen cold-chain, fresh food expiry, or D2C parcel BOPIS).",
        "sub_pillars": {
            "demand_forecasting": "Brand-Length & Territory Demand Sensing",
            "trade_promotion": "Trade Scheme & Wholesale Margin Analytics",
            "sop_ibp": "Divisional S&OP (ILTD · Factory · TM&D)",
            "portfolio_sku": "Brand-Pack & SKU Portfolio Governance",
            "supplier_network": "ILTD Leaf Growers & Tier-N Packaging Network",
            "material_packaging": "Leaf Blend, Filter Tow & Hinge-Lid Sourcing",
            "contract_po": "Auction Contracts, Paperboard & PO Governance",
            "production_scheduling": "PMD Threshing & SMD High-Speed Line Scheduling",
            "capacity_planning": "Cigarette Making & Packing OEE Capacity",
            "quality_compliance": "Moisture, Draw-Resistance & Statutory Printing QA",
            "positioning_optimization": "Excise-Bonded Mother Warehouse & WD Buffers",
            "warehouse_operations": "Bonded Depot Dispatch & Case Slotting",
            "omnichannel_visibility": "National Depot-to-WD Inventory Visibility",
            "first_mid_mile": "Bonded Factory-to-Mother-Depot Linehaul",
            "store_replenishment": "TM&D Wholesale Dealer (WD) Replenishment",
            "last_mile_delivery": "Urban & Rural Pan-Retail Beat Routing",
            "route_carrier": "Dedicated Containerized Fleet & Freight Audit",
            "returns_claims": "Trade Damage Reclamation & Excise Claims",
            "expiry_markdowns": "Freshness Rotation & Slow-Moving Batch Rebalance",
            "pallet_tote": "Master Case, Pellet Crate & Silo Bobbin Loop",
        },
        "processes": {
            "f2f": ("Crop-to-Trade Forecast-to-Fulfill (ILTD → Factory → TM&D)", "Aligning leaf auction grades, high-speed SMD packing lines, and regional Wholesale Dealer demand."),
            "o2d": ("Bonded Factory-to-Wholesale Dealer Order-to-Delivery", "Excise-compliant dispatch from manufacturing units through mother depots to TM&D Wholesale Dealers."),
            "s2p": ("ILTD Leaf Auction & Hinge-Lid Packaging Source-to-Pay", "Sourcing flue-cured Virginia leaf, acetate filter tow, and printed paperboard blanks."),
            "p2r": ("Excise Trade Damage & Packaging Circularity", "Audited damage verification, statutory compliance, and reusable factory bobbin/pallet loops."),
        },
        "role_prefix_style": "fmcg_tmd",
    },
    "fmcg_foods": {
        "sector": "FMCG · Packaged Foods, Staples, Snacks & Agri-Sourcing",
        "accent": "#10b981",
        "secondary": "#1e3a8a",
        "exec_title": "Chief Executive & Head of Foods Supply Chain (ICML, Agri & Omni-Trade)",
        "thesis_tpl": (
            "Orchestrating {co}'s farmgate agri-sourcing, Integrated Consumer Goods Manufacturing & Logistics "
            "(ICML) plants, ambient & temperature-controlled Carrying & Forwarding Agents (CFAs), and "
            "omnichannel fulfillment across general trade kiranas, modern trade, and quick-commerce dark stores."
        ),
        "sites_tpl": "Integrated Consumer Goods Manufacturing & Logistics (ICML) Hubs (Kapurthala, Ranjangaon, Trichy, Uluberia, Medak) · Regional Mother Godowns & CFA Depots",
        "erp": "SAP S/4HANA · SAP IBP · Distributor Management System (DMS) · e-Choupal Agri Procurement · Transport & Yard WMS",
        "terms": [
            "ICML — Integrated Consumer Goods Mfg & Logistics",
            "CFA — Carrying & Forwarding Agent Depot",
            "e-Choupal — Direct Farmgate Identity-Preserved Sourcing",
            "GT / MT / Q-Comm — General Trade, Modern Trade & Quick Commerce",
        ],
        "career_titles": [
            "Head of Foods Supply Chain & ICML Operations",
            "National Demand & S&OP Manager — Staples & Snacks",
            "Category Procurement Manager — Wheat, Spices & Laminates",
            "Regional Logistics & CFA Operations Manager",
            "Modern Trade & Quick-Commerce Customer Supply Chain Lead",
            "ICML Manufacturing & Quality Assurance Manager",
        ],
        "hide_agents": set(),
        "hide_reason": "",
        "sub_pillars": {
            "demand_forecasting": "Regional Pack-Size & Q-Comm Demand Sensing",
            "trade_promotion": "GT/MT Trade Scheme & Display Lift ROI",
            "sop_ibp": "Monthly Foods S&OP & Harvest Capacity Sync",
            "portfolio_sku": "Price-Point Pack (₹5/₹10/Family) Rationalization",
            "supplier_network": "Farmgate Mandi & Co-Manufacturer Network",
            "material_packaging": "Agri-Commodities, Edible Oils & Flexible Film",
            "contract_po": "Crop Forward Contracts & 3-Way Match",
            "production_scheduling": "ICML Baking, Extrusion & Milling Scheduling",
            "capacity_planning": "ICML Line OEE & Co-Packer Capacity",
            "quality_compliance": "FSSAI Food Safety, Moisture & Seal Vision QA",
            "positioning_optimization": "Mother Godown, CFA & Super-Stockist MEIO",
            "warehouse_operations": "FEFO High-Bay ICML & CFA Warehouse Ops",
            "omnichannel_visibility": "Modern Trade & Quick-Commerce Dark-Store ATP",
            "first_mid_mile": "Primary Multi-Axle Linehaul & Dairy Cold-Chain",
            "store_replenishment": "CFA-to-Distributor & Modern Trade Replenishment",
            "last_mile_delivery": "Secondary Kirana Beat & Q-Comm Slot Delivery",
            "route_carrier": "Primary/Secondary Fleet & Freight Bill Audit",
            "returns_claims": "Distributor Claim & Damaged Pack Triage",
            "expiry_markdowns": "FEFO Shelf-Life & Near-Expiry Markdowns",
            "pallet_tote": "CHEP Pallet, Crate & Flexible Wrapper Circularity",
        },
        "processes": {
            "f2f": ("Farmgate-to-Shelf Forecast-to-Fulfill", "Connecting mandi harvest arrivals, ICML food lines, and regional distributor/Q-Comm velocity."),
            "o2d": ("CFA-to-Distributor & Q-Comm Order-to-Delivery", "FEFO-compliant replenishment across general trade stockists, modern trade chains, and dark stores."),
            "s2p": ("Agri-Commodity & Flexible Packaging Source-to-Pay", "Direct farmgate wheat/spice procurement and multi-layer laminate sourcing."),
            "p2r": ("Shelf-Life Freshness & Plastic Neutrality Loop", "Preventing near-expiry write-offs and reconciling returnable crates/pallets."),
        },
        "role_prefix_style": "fmcg_foods",
    },
    "cement_heavy_materials": {
        "sector": "Heavy Building Materials · Integrated Clinker, Grinding Units & Bulk Logistics",
        "accent": "#f59e0b",
        "secondary": "#1e293b",
        "exec_title": "Chief Manufacturing & Supply Chain Officer (Integrated Units, Grinding & Bulk Logistics)",
        "thesis_tpl": (
            "Optimizing {co}'s limestone mines, pyro-processing rotary kilns, split-location Grinding Units (GUs), "
            "bulk coastal terminals, Indian Railways clinker/cement rakes, and primary/secondary road dispatch "
            "across thousands of channel dealers and institutional infrastructure sites."
        ),
        "sites_tpl": "Integrated Limestone & Clinker Mother Plants · Regional Split Grinding Units (GUs) · Bulk Packing Terminals · Rail Siding & C&F Depots",
        "erp": "SAP S/4HANA · Kiln APC & Historian · Rail Rake & GPS Fleet Control Tower · Dealer Order Portal",
        "terms": [
            "IU / GU — Integrated Clinker Unit & Split Grinding Unit",
            "PTP /PKD — Primary Lead Distance & Rail-Road Mix",
            "PPC / OPC — Pozzolana & Ordinary Portland Cement Blends",
            "C&F Godown — Clearing & Forwarding Dealer Warehouse",
        ],
        "career_titles": [
            "Unit Head — Integrated Cement & Clinker Operations",
            "Zonal Head — Logistics, Rail Rake & Primary Dispatch",
            "General Manager — Coal, Petcoke, Fly-Ash & Gypsum Sourcing",
            "Regional Planning & Lead-Distance Optimization Manager",
            "Depot & Secondary Dealer Freight Controller",
            "Head of Pyro-Processing Maintenance & WHRS Energy",
        ],
        "hide_agents": COLD_CHAIN_AGENT_IDS | FOOD_PERISHABLE_AGENT_IDS | RETAIL_STORE_PLANOGRAM_AGENT_IDS | {"keep_it_routing_advisor", "atp_order_promising_agent"},
        "hide_reason": "Hidden for Cement & Bulk Materials fit: non-perishable bulk bags/bulkers via Rail Rakes, C&F godowns, and B2B dealers (no cold-chain, food expiry, retail planograms, or parcel D2C).",
        "sub_pillars": {
            "demand_forecasting": "District Trade Dealer & Infra Project Demand",
            "trade_promotion": "Dealer Lifting Slabs & Seasonal Rebate ROI",
            "sop_ibp": "Clinker-to-Grinding S&OP & Rail-Road Mix",
            "portfolio_sku": "OPC / PPC / Composite Blend & Bag Portfolio",
            "supplier_network": "Petcoke, Imported Coal, Fly-Ash & Slag Network",
            "material_packaging": "Fuel Linkage, Gypsum & PP Woven Sack Sourcing",
            "contract_po": "Mining/Fuel Offtake & EPC Service Contracts",
            "production_scheduling": "Kiln Campaign & Ball-Mill Grinding Scheduling",
            "capacity_planning": "Rotary Kiln OEE, Refractory & WHRS Power",
            "quality_compliance": "Blaine Fineness, Compressive Strength & BIS QA",
            "positioning_optimization": "Clinker Silo, Grinding Unit & Godown Buffers",
            "warehouse_operations": "Rail Siding Rake Loading & Packer Bay Slotting",
            "omnichannel_visibility": "Dealer Portal & Infra Site Order Visibility",
            "first_mid_mile": "Rail Rake Clinker Transfer & Bulk Bulker Hauls",
            "store_replenishment": "C&F Godown & Exclusive Dealer Replenishment",
            "last_mile_delivery": "Direct-from-Plant Construction Site Delivery",
            "route_carrier": "Primary Lead-Distance & Transporter Bill Audit",
            "returns_claims": "Moisture-Caked Bag Claims & Breakage Audit",
            "expiry_markdowns": "Monsoon Silo Age & Monsoon Stock Rotation",
            "pallet_tote": "Bulk Bulker Turnaround & Tarpaulin Asset Loop",
        },
        "processes": {
            "f2f": ("Quarry-to-Site Forecast-to-Fulfill", "Balancing clinker kiln output, regional Grinding Unit power tariffs, and district cement demand."),
            "o2d": ("Packer-to-Dealer & Infra Site Order-to-Delivery", "Minimizing primary/secondary ton-km freight across rail rakes and GPS-tracked trucks."),
            "s2p": ("Petcoke, Fly-Ash & Woven Sack Source-to-Pay", "Optimizing landed fuel calorific cost, thermal power plant fly-ash, and PP bags."),
            "p2r": ("Alternative Fuel (AFR) Co-Processing & Bag Claims", "Co-processing municipal/industrial waste in kilns and auditing transit damage."),
        },
        "role_prefix_style": "industrial",
    },
    "metals_mining": {
        "sector": "Metals & Industrial Materials · Smelting, Rolling Mills & Global Coil Logistics",
        "accent": "#38bdf8",
        "secondary": "#0f172a",
        "exec_title": "Chief Supply Chain & Metal Operations Officer (Smelters, Rolling & Global Logistics)",
        "thesis_tpl": (
            "Coordinating {co}'s bauxite/copper ore supply, alumina refineries, captive power & smelting pots, "
            "flat-rolled and extrusion mills, ocean breakbulk/container exports, and closed-loop scrap recycling."
        ),
        "sites_tpl": "Alumina Refineries & Aluminium/Copper Smelters · Flat-Rolled & Extrusion Downstream Plants · Port Export Terminals & Scrap Recycling Hubs",
        "erp": "SAP S/4HANA · MES Coil & Cast-House Genealogy · LME Hedging & Commodity Risk · Rail/Ocean TMS",
        "terms": [
            "LME — London Metal Exchange Price & Premium",
            "Cast-House & Hot/Cold Rolling Campaign",
            "UBC — Used Beverage Can & Closed-Loop Scrap",
            "Coil, Billet, Wire-Rod & Foil Downstream Mix",
        ],
        "career_titles": [
            "VP — Integrated Metal Supply Chain & S&OP",
            "Head of Raw Materials Procurement (Bauxite, Concentrate, Carbon Anodes)",
            "Master Scheduler — Hot Strip & Cold Rolling Mill",
            "General Manager — Inbound Rake & Port Export Logistics",
            "Manager — Automotive & Packaging Customer Supply Chain",
            "Head of Closed-Loop Scrap & CBAM Carbon Traceability",
        ],
        "hide_agents": COLD_CHAIN_AGENT_IDS | FOOD_PERISHABLE_AGENT_IDS | RETAIL_STORE_PLANOGRAM_AGENT_IDS | {"keep_it_routing_advisor", "atp_order_promising_agent"},
        "hide_reason": "Hidden for Metals & Rolling Mill fit: B2B industrial coils, ingots, and extrusions (no retail stores, food expiry, cold-chain, or consumer parcel returns).",
        "sub_pillars": {
            "demand_forecasting": "Auto, Can-Stock & Industrial Alloy Demand",
            "trade_promotion": "Alloy Conversion Premium & Contract Pricing",
            "sop_ibp": "Smelter-to-Rolling Mill S&OP & Margin Mix",
            "portfolio_sku": "Alloy Grade, Gauge & Coil Width Rationalization",
            "supplier_network": "Mine-to-Smelter & Sub-Tier Chemical Suppliers",
            "material_packaging": "Alumina, Copper Concentrate, Coke & Pitch Sourcing",
            "contract_po": "LME-Indexed Offtake & Toll-Conversion Contracts",
            "production_scheduling": "Cast-House Melt & Rolling Width-Jump Sequencing",
            "capacity_planning": "Potline Amperage, Furnace & Mill OEE",
            "quality_compliance": "Ultrasonic Surface Vision & Metallurgical Certs",
            "positioning_optimization": "Ingot Yard, WIP Slab & Service-Center Buffers",
            "warehouse_operations": "Overhead Crane Coil Bay & Heavy Yard Sequencing",
            "omnichannel_visibility": "OEM Just-in-Time Coil Order Tracking",
            "first_mid_mile": "Captive Rail Rake & Breakbulk Vessel Drayage",
            "store_replenishment": "Service-Center & OEM Kanban Replenishment",
            "last_mile_delivery": "Heavy Flatbed Coil & Extrusion Site Delivery",
            "route_carrier": "Heavy-Haul Axle Load & Ocean/Rail Freight Audit",
            "returns_claims": "OEM Surface-Defect Claims & Coil Rework",
            "expiry_markdowns": "Off-Spec Prime/Secondary Coil Re-Allocation",
            "pallet_tote": "Closed-Loop Scrap Remelt & Steel Stillage Return",
        },
        "processes": {
            "f2f": ("Mine-to-Mill Forecast-to-Fulfill", "Synchronizing smelter hot-metal output with downstream rolling mill width sequences and OEM schedules."),
            "o2d": ("Cast-House-to-OEM Coil Order-to-Delivery", "Heavy rail, port, and flatbed dispatch with full metallurgical certificate traceability."),
            "s2p": ("Concentrate, Energy & Carbon Anode Source-to-Pay", "LME-hedged raw material procurement and Scope-3 / EU CBAM carbon accounting."),
            "p2r": ("Closed-Loop Aluminium/Copper Scrap Circularity", "Recovering customer stamping scrap and UBC bales back into low-carbon remelt furnaces."),
        },
        "role_prefix_style": "industrial",
    },
    "general_cpg_retail": {
        "sector": "Consumer Goods & Omnichannel Supply Chain",
        "accent": "#2563eb",
        "secondary": "#1e3a8a",
        "exec_title": "Chief Supply Chain & Operations Officer (CSCO)",
        "thesis_tpl": (
            "Synchronizing {co}'s supplier ecosystems, automated manufacturing plants, regional fulfillment "
            "centers, and omnichannel retail & distributor replenishment with real-time demand sensing."
        ),
        "sites_tpl": "Flagship Automated Manufacturing Hubs · Regional Mixing & Distribution Centers · Urban Omnichannel Fulfillment Nodes",
        "erp": "SAP S/4HANA · SAP IBP / Kinaxis · Manhattan WMS · Blue Yonder TMS · BigQuery",
        "terms": [
            "IBP — Integrated Business Planning",
            "OTIF — On-Time In-Full Service Excellence",
            "MEIO — Multi-Echelon Inventory Optimization",
            "DSD / DC — Direct-Store & Distribution Center Flow",
        ],
        "career_titles": [
            "Director — Global Demand Planning & S&OP",
            "Head of Strategic Direct Materials Procurement",
            "Plant Operations & Continuous Improvement Lead",
            "VP — Distribution Centers & Omnichannel Inventory",
            "Director — Global Transportation & Carrier Network",
            "Head of Sustainable Packaging & Circular Logistics",
        ],
        "hide_agents": set(),
        "hide_reason": "",
        "sub_pillars": {},
        "processes": {},
        "role_prefix_style": "general",
    },
}


def detect_division_archetype(company_name: str, division_name: str, notes: str = "") -> str:
    blob = f"{company_name} {division_name} {notes}".lower()
    if any(k in blob for k in ("tobacco", "cigarette", "iltd", "tm&d", "tmd", "itd", "leaf", "cigar", "vape", "philip morris", "bat ")):
        return "tobacco_tmd"
    if any(k in blob for k in ("cement", "ultratech", "clinker", "concrete", "holcim", "ambuja", "shree cement", "acc ", "dalmia", "grasim")):
        return "cement_heavy_materials"
    if any(k in blob for k in ("hindalco", "novelis", "metal", "aluminium", "aluminum", "steel", "copper", "mining", "vedanta", "jsw", "tata steel", "alcoa", "rio tinto")):
        return "metals_mining"
    if any(k in blob for k in ("food", "aashirvaad", "sunfeast", "bingo", "snack", "dairy", "agri", "beverage", "grocery", "nestle", "danone", "pepsi", "mondelez", "tyson", "itc")):
        return "fmcg_foods"
    return "general_cpg_retail"


def _tailor_persona_title(canonical_name: str, arch_key: str, sp_custom_name: str) -> str:
    """Converts generic SCOR persona names into authentic corporate org-chart job titles."""
    t = canonical_name
    if arch_key == "tobacco_tmd":
        replacements = {
            "Demand Planner / Forecaster": "Divisional Manager — Brand & Territory Demand Planning",
            "Commercial Planning Lead": "Head of TM&D Commercial & Channel Consensus",
            "Brand & Innovation Manager": "Brand Launch & Capsule/Blend NPI Supply Manager",
            "Trade Marketing Manager": "National Manager — Trade Schemes & WD Margins",
            "Revenue Growth Lead": "Head of Excise-Adjusted Revenue & Price-Pack Strategy",
            "Retail Account Planner": "Area Manager — Wholesale Dealer (WD) Lift Planning",
            "VP of S&OP / IBP": "Head of Divisional S&OP (ILTD · Factories · TM&D)",
            "CSCO / Control Tower Lead": "Divisional Head — Central Supply Chain Control Tower",
            "Supply Chain Risk Director": "Lead — Excise, Monsoon Leaf & Transit Disruption Cell",
            "Portfolio Analytics Lead": "Manager — Brand-Length SKU & Margin Rationalization",
            "Supply Chain Finance Lead": "Divisional Controller — Bonded Inventory & Working Capital",
            "Master Data Steward": "Lead — SAP Material, Excise & BOM Master Governance",
            "Supplier Risk Manager": "Manager — ILTD Grower & Packaging Vendor Risk",
            "ESG Compliance Officer": "Head of Sustainable Agro-Forestry & Leaf Traceability",
            "Vendor Onboarding Lead": "Manager — Packaging & Machinery Supplier Qualification",
            "Category Sourcing Manager": "Category Manager — Leaf Blend, Filter Tow & Paperboard",
            "Packaging Engineer": "Principal Engineer — Hinge-Lid Slide, Foil & BOPP Film",
            "Commodity Risk Trader": "Procurement Lead — Pulp, Acetate Tow & Agro-Inputs",
            "Procurement Operations": "Manager — Factory Indirects & Automated PO Execution",
            "Legal Procurement": "Senior Counsel — Grower Offtake & OEM Supply Contracts",
            "AP Automation Lead": "Manager — Central Accounts Payable & 3-Way Match",
            "Master Production Scheduler": "Manager — PMD Threshing & SMD Maker-Packer Scheduling",
            "Shop-Floor Supervisor": "Section Manager — High-Speed Cigarette Making & Packing",
            "Plant Material Planner": "Factory MRP Controller — Cut-Rag, Rods & Printed Blanks",
            "Reliability Engineer": "Lead Reliability Engineer — Maker-Packer & Threshing OEE",
            "Manufacturing VP": "Vice President — Manufacturing Operations (Factories)",
            "Industrial Engineer": "Manager — Industrial Engineering & SMD Shift Manning",
            "Quality Assurance Lead": "Head of Quality Assurance — Moisture, Draw & Print Vision",
            "Quality Director": "Divisional Quality & Blend Genealogy Controller",
            "EHS & Compliance Manager": "Manager — Factory EHS,Statutory Warning & Excise Audit",
            "Inventory Optimization Lead": "Manager — Bonded Mother Warehouse & Depot Stock Norms",
            "Regional Stock Planner": "Zonal Executive — Inter-Depot Stock Transfer & Rebalance",
            "Supply Chain Analyst": "Analyst — Slow-Moving Batch & Excise Stock Velocity",
            "Warehouse Ops Manager": "Manager — Mother Godown Dispatch & Bonded Warehousing",
            "DC Shift Manager": "Depot Supervisor — Master-Case Staging & Crew Shifts",
            "Yard & Dock Coordinator": "Factory Gate & Bonded Container Dock Coordinator",
            "Store Inventory Lead": "TM&D Branch Executive — Wholesale Dealer Stock Accuracy",
            "Marketplace Manager": "National Key Accounts & Institutional Channel Lead",
            "Linehaul Network Planner": "Manager — Factory-to-Depot Containerized Linehaul",
            "Import Logistics Lead": "Manager — Leaf Export & Filter-Tow Import Drayage",
            "Replenishment Planner": "TM&D Replenishment Manager — Wholesale Dealer Allocation",
            "DC Outbound Manager": "Mother Depot Outbound — Route-Wise Master Case Loading",
            "Urban Logistics Lead": "TM&D Metro City Beat & Curfew Dispatch Coordinator",
            "Fleet Operations Manager": "Manager — Secondary Trade Van & Beat Operations",
            "Delivery Ops Lead": "TM&D Territory Executive — Outlet Geo-Mapping",
            "Dispatch Manager": "Central Transport Manager — Primary Dedicated Fleet",
            "Transportation Procurement": "Manager — All-India Transporter Contracts & Spot Tenders",
            "Freight Audit Analyst": "Executive — Primary Freight Bill & Detention Audit",
            "Returns Ops Manager": "Manager — Trade Damaged Stock & Excise Reclamation",
            "Claims Fraud Analyst": "Auditor — Wholesale Transit Shortage & Seal Integrity",
            "Lifecycle Pricing Lead": "Manager — Batch Freshness & Territory Re-Allocation",
            "Asset Control Manager": "Coordinator — Factory Silo Bobbins, Crates & Pallets",
            "Circular Supply Lead": "Lead — Paperboard Circularity & Zero-Waste Packaging",
            "Reverse Fleet Planner": "Planner — Empty Container & Returnable Crate Backhaul",
        }
        return replacements.get(canonical_name, f"Manager — {sp_custom_name} ({canonical_name})")

    if arch_key == "cement_heavy_materials":
        replacements = {
            "Demand Planner / Forecaster": "Zonal Manager — District Trade & Infra Cement Demand",
            "Commercial Planning Lead": "Head of Dealer Channel & Institutional Forecast Sync",
            "Brand & Innovation Manager": "Product Lead — Blended Low-Carbon & Specialty Cements",
            "Trade Marketing Manager": "Zonal Head — Dealer Lifting Schemes & Rebate Slabs",
            "Revenue Growth Lead": "Head of Net Realization (NCR) & Landed Price Strategy",
            "VP of S&OP / IBP": "Vice President — Clinker-to-Grinding S&OP & Rail-Road Mix",
            "CSCO / Control Tower Lead": "Chief Logistics & Multi-Unit Dispatch Control Officer",
            "Category Sourcing Manager": "General Manager — Petcoke, Thermal Coal, Fly-Ash & Gypsum",
            "Packaging Engineer": "Manager — PP Woven Sacks, Moisture-Proof & Bulk Bulkers",
            "Master Production Scheduler": "Chief Scheduler — Rotary Kiln & Vertical Roller Mills",
            "Reliability Engineer": "Head of Kiln Refractory, Pyro-Sensor & Mill Reliability",
            "Quality Assurance Lead": "Chief Chemist — Blaine Fineness, Clinker Factor & BIS QA",
            "Inventory Optimization Lead": "Head of Clinker Silo & Split Grinding Unit Stock Norms",
            "Yard & Dock Coordinator": "Plant Packer-Bay, Bulker & Rail-Siding Yard Master",
            "Linehaul Network Planner": "General Manager — Primary Clinker Rail Rakes & Bulkers",
            "Replenishment Planner": "Zonal Controller — C&F Godown & Exclusive Dealer Stock",
            "Dispatch Manager": "Regional Head — Primary & Secondary Cement Truck Dispatch",
            "Freight Audit Analyst": "Manager — PTP Ton-Km Freight, Wharfage & Demurrage Audit",
        }
        return replacements.get(canonical_name, f"Head of {sp_custom_name} ({canonical_name})")

    if arch_key == "metals_mining":
        replacements = {
            "Demand Planner / Forecaster": "Director — Auto Sheet, Can-Stock & Extrusion Demand",
            "VP of S&OP / IBP": "VP — Global Smelter-to-Rolling Mill S&OP",
            "Category Sourcing Manager": "Head of Bauxite, Concentrate, Calcined Coke & Alloys",
            "Master Production Scheduler": "Master Scheduler — Cast-House & Hot/Cold Rolling Campaigns",
            "Reliability Engineer": "Principal Engineer — Potline, Furnace & Rolling Mill OEE",
            "Quality Assurance Lead": "Head of Ultrasonic Surface Inspection & Metallurgical QA",
            "Inventory Optimization Lead": "Manager — Slab Yard, WIP Coil & Service-Center Buffers",
            "Linehaul Network Planner": "General Manager — Captive Ore Rakes & Heavy Coil Hauls",
            "Circular Supply Lead": "VP — Closed-Loop UBC & Automotive Scrap Recycling",
        }
        return replacements.get(canonical_name, f"Manager — {sp_custom_name} ({canonical_name})")

    if arch_key == "fmcg_foods":
        replacements = {
            "Demand Planner / Forecaster": "National Manager — Brand-Pack & Q-Comm Demand Sensing",
            "Trade Marketing Manager": "Head of GT/MT Trade Promotions & Visibility ROI",
            "VP of S&OP / IBP": "Head of Foods IBP & Harvest-to-ICML Capacity Balancing",
            "Category Sourcing Manager": "Head of Agri-Sourcing (Wheat, Spices, Dairy & Laminates)",
            "Master Production Scheduler": "ICML Operations Planner — Milling, Baking & Extrusion",
            "Inventory Optimization Lead": "National Controller — Mother Godown & CFA Safety Stocks",
            "Replenishment Planner": "Lead — Super-Stockist, Modern Trade & Dark-Store Allocation",
            "Dispatch Manager": "National Transport Lead — Primary ICML & Secondary Fleet",
        }
        return replacements.get(canonical_name, canonical_name)

    return canonical_name


def _tailor_agent_name(agent_id: str, canonical_name: str, arch_key: str) -> str:
    """Returns a crisp 2-4 word company/division-tailored agent name when domain language improves clarity, else ''."""
    if arch_key == "tobacco_tmd":
        names = {
            "demand_sensing_agent": "TM&D WD Demand Sensing",
            "cpfr_sync_agent": "Wholesale Dealer Lift Sync",
            "npi_demand_profiler": "Brand-Length & Capsule NPI Profiler",
            "promo_lift_simulator": "Trade Scheme & Margin Simulator",
            "field_beat_distributor_sync_agent": "WD Channel Allocation Copilot",
            "trade_scheme_claims_reconciler": "TM&D Scheme Claim Auditor",
            "sop_scenario_weaver": "ILTD-to-TM&D S&OP Weaver",
            "tier_n_risk_sentinel": "ILTD Leaf & Packaging Risk Sentinel",
            "commodity_index_advisor": "Virginia Leaf & Pulp Index Advisor",
            "rfq_should_cost_agent": "Hinge-Lid & Filter Tow Should-Cost",
            "finite_production_scheduler": "PMD Threshing & SMD Line Scheduler",
            "line_schedule_optimizer": "High-Speed Maker-Packer Re-Sequencer",
            "predictive_oee_sentinel": "SMD Maker-Packer OEE Sentinel",
            "inline_yield_guardian": "Moisture, Draw & Print Vision QA",
            "meio_safety_stock_agent": "Bonded Mother Depot Stock Agent",
            "warehouse_slotting_agent": "Bonded Master-Case Slotting",
            "load_consolidation_agent": "Bonded Container Load Consolidator",
            "store_capacity_agent": "Wholesale Dealer Vault Capacity Agent",
            "fleetflow_dispatch": "TM&D Beat & Primary Fleet Router",
            "reverse_rma_optimizer": "Excise Trade Damage Sentinel",
            "rti_balance_reconciler": "Bobbin, Crate & Pallet Reconciler",
        }
        return names.get(agent_id, "")

    if arch_key == "cement_heavy_materials":
        names = {
            "demand_sensing_agent": "District Dealer & Infra Demand Sensing",
            "promo_lift_simulator": "Dealer Lifting Slab & Rebate Simulator",
            "sop_scenario_weaver": "Clinker-to-Grinding S&OP Weaver",
            "network_twin_architect": "Primary Lead-Distance & Rail-Road Twin",
            "commodity_index_advisor": "Petcoke & Thermal Coal Index Advisor",
            "rfq_should_cost_agent": "Fly-Ash, Gypsum & PP Sack Should-Cost",
            "finite_production_scheduler": "Kiln Campaign & Ball-Mill Scheduler",
            "predictive_oee_sentinel": "Rotary Kiln & WHRS OEE Sentinel",
            "inline_yield_guardian": "Blaine Fineness & Clinker Factor QA",
            "meio_safety_stock_agent": "Clinker Silo & Godown Stock Agent",
            "warehouse_slotting_agent": "Packer Bay & Rail Siding Slotting",
            "load_consolidation_agent": "Rake & Bulk Clinker Consolidator",
            "yard_dock_sequencer": "Bulker & Rail-Siding Yard Sequencer",
            "store_capacity_agent": "C&F Godown & Dealer Capacity Agent",
            "fleetflow_dispatch": "GPS Cement Truck & Site Rerouter",
            "freight_bill_audit_agent": "PTP Ton-Km & Demurrage Bill Audit",
            "intermodal_rail_linehaul_agent": "Empty Bulker & Rake Backhaul Planner",
        }
        return names.get(agent_id, "")

    if arch_key == "metals_mining":
        names = {
            "demand_sensing_agent": "Auto Sheet & Can-Stock Demand Sensing",
            "sop_scenario_weaver": "Smelter-to-Rolling Mill S&OP Weaver",
            "commodity_index_advisor": "LME Metal, Alumina & Coke Advisor",
            "carbon_scope3_ledger": "Low-Carbon Metal & EU CBAM Auditor",
            "finite_production_scheduler": "Cast-House & Rolling Width Scheduler",
            "predictive_oee_sentinel": "Potline & Rolling Mill OEE Sentinel",
            "inline_yield_guardian": "Ultrasonic Coil Surface Vision QA",
            "meio_safety_stock_agent": "Ingot, Slab & Coil Buffer Agent",
            "warehouse_slotting_agent": "Overhead Crane Coil Bay Sequencer",
            "load_consolidation_agent": "Heavy Coil & Rake Load Consolidator",
            "rti_balance_reconciler": "Closed-Loop UBC Scrap & Stillage Ledger",
            "intermodal_rail_linehaul_agent": "Captive Rake & Scrap Backhaul Planner",
        }
        return names.get(agent_id, "")

    if arch_key == "fmcg_foods":
        names = {
            "demand_sensing_agent": "GT, MT & Q-Comm Demand Sensing",
            "promo_lift_simulator": "GT/MT Scheme & Display ROI Simulator",
            "sop_scenario_weaver": "Harvest-to-ICML S&OP Weaver",
            "commodity_index_advisor": "Wheat, Spice & Edible Oil Advisor",
            "finite_production_scheduler": "ICML Baking & Extrusion Scheduler",
            "inline_yield_guardian": "FSSAI Seal & Pack Vision QA",
            "meio_safety_stock_agent": "Mother Godown & CFA Safety Stock",
            "warehouse_slotting_agent": "FEFO High-Bay CFA Slotting",
            "cold_chain_auditor": "Dairy & Frozen Reefer Cold-Chain Auditor",
            "dynamic_markdown_agent": "FEFO Shelf-Life Markdown Agent",
        }
        return names.get(agent_id, "")

    return ""


def synthesize_domain_twin(
    company_name: str,
    division_name: str = "",
    geography: str = "Global",
    user_notes: str = "",
    custom_logo_input: str = "",
    progress_cb: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> TwinOverlaySpec:
    """Builds a complete, zero-breakage `TwinOverlaySpec` grounded in authentic industry & division structure."""
    cat = load_canonical_catalog()
    depts = cat["departments"]
    personas_cat = cat["personas"]
    agents_cat = cat["agents"]

    arch_key = detect_division_archetype(company_name, division_name, user_notes)
    arch = DIVISION_ARCHETYPES[arch_key]

    clean_co = company_name.strip()
    if clean_co.lower() in ("itc", "itc ltd"):
        clean_co = "ITC Limited"
    elif clean_co.lower() in ("abg", "aditya birla"):
        clean_co = "Aditya Birla Group"
    elif clean_co.lower() in ("hul",):
        clean_co = "Hindustan Unilever Limited"

    clean_div = division_name.strip()
    twin_slug = make_twin_slug(clean_co, clean_div)
    disp = f"{clean_co} — {clean_div}" if clean_div else clean_co

    if progress_cb:
        progress_cb({
            "pct": 25,
            "stage": "logo_framing",
            "message": f"Downloading & optically framing official {clean_co} brand mark...",
            "detail": f"Sector matched: {arch['sector']}",
        })

    logo_spec = resolve_company_logo(
        company_name=clean_co,
        custom_logo_input=custom_logo_input,
        brand_accent=arch["accent"],
        brand_secondary=arch["secondary"],
    )

    if progress_cb:
        progress_cb({
            "pct": 65,
            "stage": "pillar_synthesis",
            "message": f"Mapping 20 Sub-Pillars, 60 Job Titles & Division Relevance for {disp}...",
            "detail": f"Applying authentic {arch['sector']} terminology & hiding inapplicable agents",
        })

    pillar_overrides: Dict[str, PillarOverrideSpec] = {}
    sub_pillar_overrides: Dict[str, SubPillarOverrideSpec] = {}
    persona_overrides: Dict[str, PersonaOverrideSpec] = {}
    agent_relevance: Dict[str, AgentRelevanceSpec] = {}
    hide_set: Set[str] = set(arch.get("hide_agents") or set())

    for d_id, d_obj in depts.items():
        pillar_overrides[d_id] = PillarOverrideSpec(
            dept_id=d_id,
            custom_name=d_obj["name"],
            custom_tagline=f"{disp} · {d_obj.get('tagline', d_obj['name'])}",
            custom_subtitle=f"Tailored for {disp}: {d_obj.get('subtitle', '')}",
        )
        for sp in d_obj.get("subPillars", []):
            sp_id = sp["id"]
            sp_custom = arch["sub_pillars"].get(sp_id, sp["name"])
            sub_pillar_overrides[sp_id] = SubPillarOverrideSpec(
                sub_pillar_id=sp_id,
                dept_id=d_id,
                canonical_name=sp["name"],
                custom_name=sp_custom,
            )
            for it in sp.get("items", []):
                pid = it["personaId"]
                aid = it["agentId"]
                p_base = personas_cat.get(pid, {})
                dil0 = (p_base.get("dayInLife") or [{}])[0]

                custom_title = _tailor_persona_title(p_base.get("name", pid), arch_key, sp_custom)
                persona_overrides[pid] = PersonaOverrideSpec(
                    persona_id=pid,
                    dept_id=d_id,
                    sub_pillar_id=sp_id,
                    canonical_name=p_base.get("name", pid),
                    title=custom_title,
                    role=f"{sp_custom} · {disp}",
                    summary=f"Leads {sp_custom.lower()} across {disp} ({arch['sites_tpl'].split('·')[0].strip()} and network nodes). {p_base.get('summary', '')}",
                    manual_toil=dil0.get("before", "Manual spreadsheet reconciliation across siloed plant, depot, and ERP extracts."),
                    agentic_impact=dil0.get("after", "Autonomous Gemini AI sensing, optimization, and governed SAP/ERP execution."),
                    grounding_source=f"Aligned to {clean_co} ({arch['sector'].split('·')[0].strip()}) org hierarchy",
                )

                is_rel = aid not in hide_set
                canon_ag_name = agents_cat.get(aid, {}).get("name", aid)
                agent_relevance[aid] = AgentRelevanceSpec(
                    agent_id=aid,
                    dept_id=d_id,
                    sub_pillar_id=sp_id,
                    canonical_name=canon_ag_name,
                    custom_agent_name=_tailor_agent_name(aid, canon_ag_name, arch_key) if is_rel else "",
                    is_relevant=is_rel,
                    division_context=(
                        f"Operates inside {disp} under '{sp_custom}', connecting {arch['erp'].split('·')[0].strip()} with deterministic optimization."
                        if is_rel
                        else ""
                    ),
                    hidden_reason="" if is_rel else arch.get("hide_reason", "Filtered for division operational fit."),
                )

    proc_overrides: Dict[str, ProcessJourneyOverrideSpec] = {}
    for vc_id, tup in (arch.get("processes") or {}).items():
        proc_overrides[vc_id] = ProcessJourneyOverrideSpec(
            vc_id=vc_id,
            custom_title=tup[0],
            custom_subtitle=tup[1],
        )

    from enterprise_twin.tools.public_web_career_miner import (
        fetch_wikipedia_company_summary,
        search_public_career_titles,
    )

    wp_info = fetch_wikipedia_company_summary(clean_co, clean_div)
    live_career_titles = search_public_career_titles(clean_co, clean_div)

    citations: List[GroundingCitation] = []
    if wp_info.get("page_url"):
        citations.append(GroundingCitation(title=f"{wp_info.get('canonical_title', clean_co)} — Corporate Operations Overview", url=wp_info["page_url"]))
    if logo_spec.source_url:
        citations.append(GroundingCitation(title=f"{clean_co} Official Brand Mark Source", url=logo_spec.source_url))

    exec_thesis = arch["thesis_tpl"].format(co=disp)
    if wp_info.get("description") and arch_key == "general_cpg_retail":
        exec_thesis = f"{clean_co} ({wp_info['description']}) — {exec_thesis}"

    brand = CompanyBrandSpec(
        company_name=company_name,
        canonical_name=clean_co,
        division_name=clean_div,
        twin_slug=twin_slug,
        industry_sector=arch["sector"],
        geography=geography or "Global",
        brand_accent=clamp_brand_hex(arch["accent"]),
        brand_secondary=arch["secondary"],
        executive_title=f"{arch['exec_title']}, {clean_co}",
        executive_thesis=exec_thesis,
        flagship_sites=arch["sites_tpl"],
        erp_systems=arch["erp"],
        logo=logo_spec,
    )

    merged_career_titles = live_career_titles + [t for t in arch["career_titles"] if t not in live_career_titles]

    spec = TwinOverlaySpec(
        twin_slug=twin_slug,
        company_name=company_name,
        canonical_name=clean_co,
        division_name=clean_div,
        brand=brand,
        pillar_overrides=pillar_overrides,
        sub_pillar_overrides=sub_pillar_overrides,
        persona_overrides=persona_overrides,
        agent_relevance=agent_relevance,
        process_overrides=proc_overrides,
        grounding_citations=citations,
        career_title_examples=merged_career_titles[:8],
        terminology_highlights=arch["terms"],
        generation_model="Enterprise Twin Career & Domain Engine + Live Web/Logo Grounding",
    )
    return validate_and_normalize_overlay(spec)

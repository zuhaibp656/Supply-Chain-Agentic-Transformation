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
    CustomPillarSpec,
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
        "custom_pillars": [
            ("iltd_leaf_sourcing", "01 · ILTD LEAF & AGRI", "ILTD Leaf Agronomy, Auction & Packaging", "Flue-cured leaf auctions, filter tow & printed hinge-lid blanks", "Governs grower crop trace, auction grade buying, acetate filter tow, and printed paperboard sourcing.", "#7c3aed", "supplier_graph", ["supplier_network", "material_packaging", "contract_po"]),
            ("tmd_demand_planning", "02 · DEMAND & S&OP", "Brand-Length Demand & Divisional S&OP", "Territory velocity, excise-band elasticity & SKU portfolio", "Synchronizes brand-length demand sensing across ILTD threshing capacity, cigarette factories, and TM&D branches.", "#2563eb", "demand_wave", ["demand_forecasting", "sop_ibp", "portfolio_sku"]),
            ("pmd_smd_factories", "03 · PMD & SMD PLANTS", "Primary Threshing & Cigarette Manufacturing", "Green-leaf threshing, cut-rag & high-speed maker-packer lines", "Runs finite line scheduling, maker-packer OEE reliability, and moisture/draw/print vision QA across cigarette factories.", "#ea580c", "factory_arm", ["production_scheduling", "capacity_planning", "quality_compliance"]),
            ("bonded_warehousing", "04 · BONDED GODOWNS", "Excise-Bonded Warehouses & Mother Depots", "Factory bonded vaults, tax-stamp control & depot buffers", "Optimizes multi-echelon stock norms and master-case slotting across excise-bonded mother warehouses.", "#0284c7", "warehouse_rack", ["positioning_optimization", "warehouse_operations", "omnichannel_visibility"]),
            ("primary_linehaul", "05 · PRIMARY LINEHAUL", "Containerized Factory-to-Depot Linehaul", "GPS-sealed container haulage & freight bill governance", "Coordinates high-security primary container dispatch from cigarette plants to regional mother depots.", "#4f46e5", "corridor_lifo", ["first_mid_mile", "route_carrier"]),
            ("tmd_wholesale_channel", "06 · TM&D & WD CHANNEL", "TM&D Trade Schemes & Wholesale Dealers", "Wholesale Dealer (WD) replenishment, trade schemes & pan-retail beats", "Steers trade scheme ROI, Wholesale Dealer vault replenishment, and urban/rural retail beat execution.", "#059669", "demand_wave", ["trade_promotion", "store_replenishment", "last_mile_delivery"]),
            ("excise_circularity", "07 · EXCISE & CIRCULAR", "Track-and-Trace, Claims & Paperboard Loop", "Statutory compliance, transit reclamation & bobbin/crate return", "Manages audited trade damage claims, batch freshness rotation, and closed-loop factory bobbin/pallet recovery.", "#e11d48", "conveyor_rack", ["returns_claims", "expiry_markdowns", "pallet_tote"]),
        ],
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
        "custom_pillars": [
            ("echoupal_agri_sourcing", "01 · E-CHOUPAL AGRI", "e-Choupal Farmgate Agri & Packaging Sourcing", "Identity-preserved wheat, spices, dairy & flexible laminates", "Connects direct farmgate mandi procurement, commodity hedging, and food-grade laminate vendors.", "#7c3aed", "supplier_graph", ["supplier_network", "material_packaging", "contract_po"]),
            ("foods_ibp_demand", "02 · FOODS IBP & PACKS", "Category Demand, Harvest S&OP & Pack Mix", "Regional taste profiles, festival peaks & ₹5/₹10/Family packs", "Aligns regional pack-size demand sensing with crop harvest windows and ICML line capacities.", "#2563eb", "demand_wave", ["demand_forecasting", "sop_ibp", "portfolio_sku"]),
            ("icml_manufacturing", "03 · ICML SMART PLANTS", "ICML Milling, Baking, Extrusion & FSSAI QA", "Automated food lines, allergen changeovers & seal vision", "Schedules multi-category food lines across ICML hubs with zero-defect FSSAI food safety compliance.", "#ea580c", "factory_arm", ["production_scheduling", "capacity_planning", "quality_compliance"]),
            ("cfa_mother_godowns", "04 · MOTHER HUBS & CFAs", "FEFO Mother Godowns & CFA Warehouse Network", "First-Expired-First-Out slotting & ambient/chilled buffers", "Positions freshness-dated inventory across ICML mother hubs and regional Carrying & Forwarding Agents (CFAs).", "#0284c7", "warehouse_rack", ["positioning_optimization", "warehouse_operations"]),
            ("cold_ambient_linehaul", "05 · REEFER & LINEHAUL", "Primary Multi-Axle & Dairy Cold-Chain Fleet", "ICML-to-CFA primary haulage & temperature telemetry", "Governs multi-axle primary freight, reefer cold-chain integrity, and carrier bill auditing.", "#4f46e5", "corridor_lifo", ["first_mid_mile", "route_carrier"]),
            ("omnitrade_qcomm", "06 · GT, MT & Q-COMM", "General Trade, Modern Trade & Quick-Commerce", "Kirana stockists, retail chains & 10-minute dark-store ATP", "Drives trade promotion ROI, dark-store fill rates, and secondary beat replenishment.", "#059669", "demand_wave", ["trade_promotion", "omnichannel_visibility", "store_replenishment", "last_mile_delivery"]),
            ("freshness_plastic_loop", "07 · FRESHNESS & ESG", "Shelf-Life Governance, Claims & Plastic Loop", "Near-expiry markdowns, distributor claims & CHEP crates", "Prevents shelf-life write-offs, automates distributor damage claims, and tracks plastic neutrality.", "#e11d48", "conveyor_rack", ["returns_claims", "expiry_markdowns", "pallet_tote"]),
        ],
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
            "PTP / PKD — Primary Lead Distance & Rail-Road Mix",
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
        "custom_pillars": [
            ("clinker_sop_demand", "01 · S&OP & BLEND MIX", "Integrated S&OP, Blend Mix & Infra Demand", "District trade velocity, infra project pipelines & OPC/PPC mix", "Balances regional construction demand against clinker kiln output, GU power tariffs, and rail-road economics.", "#2563eb", "demand_wave", ["demand_forecasting", "sop_ibp", "portfolio_sku"]),
            ("mines_fuel_sourcing", "02 · MINES, FUEL & BAGS", "Captive Limestone, Petcoke/Coal & Packaging", "Calorific fuel mix, thermal fly-ash, gypsum & PP woven sacks", "Optimizes landed kcal fuel cost, power-plant fly-ash linkages, and moisture-proof bag procurement.", "#7c3aed", "supplier_graph", ["supplier_network", "material_packaging", "contract_po"]),
            ("kilns_grinding_units", "03 · KILNS & GRINDING", "Pyro-Processing Kilns & Split Grinding Units", "Rotary kiln campaigns, vertical roller mills, WHRS & BIS QA", "Maximizes kiln thermal reliability, off-peak grinding schedules, and Blaine fineness / 28-day strength QA.", "#ea580c", "factory_arm", ["production_scheduling", "capacity_planning", "quality_compliance"]),
            ("silos_packing_terminals", "04 · SILOS & TERMINALS", "Clinker Silos, Bulk Terminals & Packer Bays", "Multi-plant silo buffers, coastal terminals & packer slotting", "Controls clinker/cement silo inventory norms and automated rotary packer bay turnaround.", "#0284c7", "warehouse_rack", ["positioning_optimization", "warehouse_operations"]),
            ("rail_rake_bulk_haul", "05 · RAIL RAKE & BULK", "Multi-Modal Rail Rakes & Primary Bulker Fleet", "Railway siding rakes, coastal barges & ton-km freight audit", "Minimizes primary lead distance, railway demurrage/wharfage, and bulk clinker transfer costs.", "#d97706", "corridor_lifo", ["first_mid_mile", "route_carrier"]),
            ("dealer_infra_channel", "06 · DEALER & INFRA OPS", "Dealer Channel (UBS), Rebates & Direct-to-Site", "C&F godowns, dealer lifting slabs & RMC / project site delivery", "Synchronizes dealer rebate schemes, C&F godown stock norms, and GPS-tracked site deliveries.", "#059669", "demand_wave", ["trade_promotion", "omnichannel_visibility", "store_replenishment", "last_mile_delivery"]),
            ("afr_green_circularity", "07 · AFR & GREEN CEMENT", "AFR Co-Processing, Monsoon Rotation & Claims", "Kiln waste co-processing, moisture-cake prevention & bulker loop", "Drives Alternative Fuel & Raw Material (AFR) substitution, monsoon stock rotation, and transit bag claims.", "#e11d48", "conveyor_rack", ["returns_claims", "expiry_markdowns", "pallet_tote"]),
        ],
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
        "custom_pillars": [
            ("mine_concentrate_sourcing", "01 · MINE & CONCENTRATE", "Bauxite, Concentrate, Energy & Carbon Sourcing", "Captive mines, copper concentrate, calcined coke & LME hedging", "Secures ore, concentrate, pitch/anodes, and energy contracts hedged against LME metal indices.", "#7c3aed", "supplier_graph", ["supplier_network", "material_packaging", "contract_po"]),
            ("metal_ibp_margin_mix", "02 · METAL IBP & ALLOYS", "Smelter-to-Mill S&OP, Alloy Mix & OEM Pricing", "Auto sheet, beverage can-stock, extrusions & conversion premiums", "Optimizes hot-metal allocation across ingot, billet, wire-rod, and high-margin flat-rolled alloys.", "#2563eb", "demand_wave", ["demand_forecasting", "trade_promotion", "sop_ibp", "portfolio_sku"]),
            ("smelters_rolling_mills", "03 · SMELTERS & ROLLING", "Refining, Potlines, Cast-House & Rolling Mills", "Potline amperage, width-jump rolling campaigns & ultrasonic QA", "Synchronizes cast-house melt schedules, hot/cold mill width sequences, and metallurgical surface QA.", "#ea580c", "factory_arm", ["production_scheduling", "capacity_planning", "quality_compliance"]),
            ("coil_yards_oem_dispatch", "04 · YARDS, RAIL & OEM", "Heavy Coil Yards, Captive Rakes & Global Dispatch", "Overhead crane coil bays, rail rakes, port drayage & JIT Kanban", "Unifies slab/coil yard positioning with heavy-haul rail, ocean breakbulk exports, and OEM Kanban delivery.", "#0284c7", "corridor_lifo", ["positioning_optimization", "warehouse_operations", "omnichannel_visibility", "first_mid_mile", "store_replenishment", "last_mile_delivery", "route_carrier"]),
            ("closed_loop_scrap_cbam", "05 · SCRAP & EU CBAM", "Closed-Loop UBC Scrap Remelt, Claims & Carbon", "Customer stamping scrap, steel stillages & Scope-3 CBAM ledger", "orchestrates closed-loop aluminium/copper scrap remelting, OEM surface claims, and EU CBAM carbon passports.", "#059669", "conveyor_rack", ["returns_claims", "expiry_markdowns", "pallet_tote"]),
        ],
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
    "beverages_packaged_foods": {
        "sector": "Consumer Beverages, Tea, Coffee, Salt & Packaged Staples",
        "accent": "#0284c7",
        "secondary": "#1e3a8a",
        "exec_title": "Chief Supply Chain Officer (Integrated Beverages, Staples & Omni-Channel)",
        "thesis_tpl": (
            "Integrating {co}'s tea/coffee auction & farmgate pulse sourcing, automated blending & vacuum-evaporated "
            "packing centers, Carrying & Forwarding Agent (CFA) depots, and direct urban/rural stockist & quick-commerce fulfillment."
        ),
        "sites_tpl": "Tea & Coffee Blending Centers · Mithapur/Regional Salt & Pulse Packing Hubs · Automated Mother Warehouses & CFA Network",
        "erp": "SAP S/4HANA · Blue Yonder / Kinaxis IBP · Auto-Replenishment DMS · Warehouse & Transport Control Tower",
        "terms": [
            "Tea Auction & Master Blend Genealogy",
            "CFA & Super-Stockist Multi-Tier Network",
            "FEFO — First-Expired-First-Out Freshness",
            "GT / MT / Q-Comm Direct Distribution",
        ],
        "career_titles": [
            "VP — India Supply Chain, Blending & CFA Logistics",
            "Head of Tea Buying, Blending & Agri-Commodities",
            "National S&OP & Customer Replenishment Lead",
            "General Manager — Co-Packing & Automated Packaging Centers",
            "Regional CFA & Primary Transportation Controller",
            "Lead — Modern Trade & Quick-Commerce Supply Chain",
        ],
        "hide_agents": set(),
        "hide_reason": "",
        "custom_pillars": [
            ("bev_foods_ibp", "01 · BEVERAGE & FOODS IBP", "Integrated S&OP, Seasonal Demand & Pack Mix", "Monsoon/winter beverage shifts, harvest sync & pack architecture", "Aligns regional tea, coffee, salt, and staples velocity with seasonal crop cycles and pack-size economics.", "#2563eb", "demand_wave", ["demand_forecasting", "sop_ibp", "portfolio_sku"]),
            ("tea_salt_agri_sourcing", "02 · AUCTIONS & AGRI BUYING", "Tea Auctions, Salt, Pulses & Packaging Sourcing", "Garden/auction tasting lots, organic pulses & barrier pouches", "Optimizes tea auction lot buying, farmgate pulse/spice sourcing, and recyclable pouch procurement.", "#7c3aed", "supplier_graph", ["supplier_network", "material_packaging", "contract_po"]),
            ("blending_packing_qa", "03 · BLENDING & PACKING", "Tea/Coffee Blending, Packing Centers & FSSAI QA", "Master blend consistency, high-speed pouch lines & co-packers", "Schedules blending drums, high-speed form-fill-seal lines, and co-manufacturing quality release.", "#ea580c", "factory_arm", ["production_scheduling", "capacity_planning", "quality_compliance"]),
            ("mother_depots_cfas", "04 · MOTHER HUBS & CFAs", "Regional Mother Warehouses & CFA Inventory", "Multi-echelon safety stocks, FEFO slotting & channel ATP", "Balances freshness-sensitive inventory across mother warehouses, CFAs, and e-commerce fulfillment nodes.", "#0284c7", "warehouse_rack", ["positioning_optimization", "warehouse_operations", "omnichannel_visibility"]),
            ("direct_trade_qcomm", "05 · GT, MT & Q-COMM REACH", "Stockist Replenishment, Schemes & Fleet Ops", "Direct urban outlets, rural super-stockists, MT & dark stores", "Synchronizes trade schemes, primary/secondary fleet dispatch, and quick-commerce slot replenishment.", "#059669", "corridor_lifo", ["trade_promotion", "first_mid_mile", "store_replenishment", "last_mile_delivery", "route_carrier"]),
            ("freshness_sustainability", "06 · FRESHNESS & SUSTAIN", "Aroma/Shelf-Life Governance, Claims & Packaging", "Near-expiry rotation, distributor claims & recyclable loops", "Protects beverage aroma/freshness windows, automates trade claims, and governs sustainable packaging.", "#e11d48", "conveyor_rack", ["returns_claims", "expiry_markdowns", "pallet_tote"]),
        ],
        "sub_pillars": {
            "demand_forecasting": "Regional Beverage & Staples Demand Sensing",
            "trade_promotion": "GT/MT Trade Scheme & Festive Pack ROI",
            "sop_ibp": "Crop-to-Cart Integrated Business Planning",
            "portfolio_sku": "Sachet, Caddy & Family Pack Rationalization",
            "supplier_network": "Tea Estates, Mandis & Co-Packer Ecosystem",
            "material_packaging": "Tea/Coffee Lots, Pulses & Barrier Laminates",
            "contract_po": "Auction Settlements & Co-Packer Contracts",
            "production_scheduling": "Master Blending & Form-Fill-Seal Scheduling",
            "capacity_planning": "Packing Center OEE & Co-Packer Allocation",
            "quality_compliance": "Sensory Blend, Moisture & FSSAI Vision QA",
            "positioning_optimization": "Mother Warehouse & Regional CFA Buffers",
            "warehouse_operations": "FEFO Pallet & Case Slotting",
            "omnichannel_visibility": "Modern Trade, E-Comm & Dark-Store ATP",
            "first_mid_mile": "Rail/Road Salt & Beverage Primary Linehaul",
            "store_replenishment": "Distributor, MT & Dark-Store Replenishment",
            "last_mile_delivery": "Urban Beat & Quick-Commerce Slot Dispatch",
            "route_carrier": "Primary/Secondary Carrier & Freight Audit",
            "returns_claims": "Trade Damage & Shortage Claim Triage",
            "expiry_markdowns": "FEFO Freshness & Slow-Mover Re-Allocation",
            "pallet_tote": "Recyclable Pouch & Returnable Pallet Loop",
        },
        "processes": {
            "f2f": ("Garden-and-Farm-to-Cup Forecast-to-Fulfill", "Linking tea auction & pulse harvests to blending centers, CFAs, and retail/Q-Comm demand."),
            "o2d": ("CFA-to-Stockist & Dark-Store Order-to-Delivery", "High-fill-rate OTIF execution across general trade, modern trade, and quick commerce."),
            "s2p": ("Tea Auction, Pulse & Barrier Pouch Source-to-Pay", "Procuring quality-graded tea lots, unpolished pulses, and sustainable packaging."),
            "p2r": ("Freshness Protection & Recyclable Packaging Loop", "Zero-waste FEFO stock rotation and audited distributor claim resolution."),
        },
        "role_prefix_style": "fmcg_foods",
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
        "sites_tpl": "WEF Lighthouse Formulation & Filling Plants · Regional Mixing & Distribution Centers · Urban Omnichannel Fulfillment Nodes",
        "erp": "SAP S/4HANA · SAP IBP / Kinaxis · Manhattan WMS · Blue Yonder TMS · BigQuery",
        "terms": [
            "IBP — Integrated Business Planning",
            "OTIF — On-Time In-Full Service Excellence",
            "MEIO — Multi-Echelon Inventory Optimization",
            "Customer Collaborative Replenishment (CPFR)",
        ],
        "career_titles": [
            "Director — Global Demand Planning & Customer IBP",
            "Head of Partner-to-Win Chemicals & Packaging Procurement",
            "Lighthouse Factory Operations & OEE Lead",
            "VP — Mixing Centers & Omnichannel Inventory",
            "Director — Collaborative Customer Logistics & Fleet",
            "Head of Regenerative Packaging & Circular Logistics",
        ],
        "hide_agents": set(),
        "hide_reason": "",
        "custom_pillars": [
            ("customer_ibp_promo", "01 · CUSTOMER IBP & NRM", "Customer IBP, Demand Sensing & Revenue Growth", "POS velocity, net revenue management & launch analogs", "Unifies AI demand sensing, joint retail business planning, and promotional lift optimization.", "#2563eb", "demand_wave", ["demand_forecasting", "trade_promotion", "sop_ibp", "portfolio_sku"]),
            ("partner_sourcing", "02 · PARTNER SOURCING", "Surfactants, Actives, Resins & Supplier Network", "Oleochemicals, fragrances, PCR plastics & 3-way match", "Manages multi-tier chemical/packaging supplier resilience, parametric should-costing, and autonomous POs.", "#7c3aed", "supplier_graph", ["supplier_network", "material_packaging", "contract_po"]),
            ("lighthouse_factories", "03 · LIGHTHOUSE PLANTS", "Batch Formulation, High-Speed Filling & QA", "Clean-in-Place (CIP) changeovers, filling OEE & vision QA", "Optimizes batch vessel sequencing, high-speed bottle/sachet filling lines, and inline quality release.", "#ea580c", "factory_arm", ["production_scheduling", "capacity_planning", "quality_compliance"]),
            ("mixing_centers_atp", "04 · MIXING CENTERS & DC", "Regional Mixing Centers, Automated DCs & ATP", "Multi-echelon inventory, robotic slotting & omnichannel ATP", "Positions safety stock across plant DCs, regional mixing centers, and e-commerce fulfillment nodes.", "#0284c7", "warehouse_rack", ["positioning_optimization", "warehouse_operations", "omnichannel_visibility"]),
            ("omnichannel_logistics", "05 · COLLABORATIVE FLEET", "Primary Linehaul, Retail Replenishment & Fleet", "Full-truckload cube consolidation, retail OTIF & urban delivery", "Orchestrates plant-to-DC linehaul, customer collaborative replenishment, and carrier freight audit.", "#059669", "corridor_lifo", ["first_mid_mile", "store_replenishment", "last_mile_delivery", "route_carrier"]),
            ("regenerative_circular", "06 · REGENERATIVE LOOP", "PCR Plastic Circularity, Claims & Markdowns", "Recycled resin loops, retail deduction audit & shelf-life", "Governs post-consumer recycled (PCR) packaging targets, retail returns/claims, and slow-mover clearance.", "#e11d48", "conveyor_rack", ["returns_claims", "expiry_markdowns", "pallet_tote"]),
        ],
        "sub_pillars": {},
        "processes": {},
        "role_prefix_style": "general",
    },
    "automotive_oem": {
        "sector": "Automotive & Mobility Manufacturing · Multi-Tier Supplier JIS, Assembly & Dealer Network",
        "accent": "#2563eb",
        "secondary": "#0f172a",
        "exec_title": "Executive Director — Supply Chain, Production Engineering & Parts Logistics",
        "thesis_tpl": (
            "Synchronizing {co}'s Tier-1/2/3 component localization & Just-in-Sequence (JIS) vendor parks, "
            "press/weld/paint/assembly lines, finished-vehicle rail/car-carrier dispatch, and national genuine spare-parts depots."
        ),
        "sites_tpl": "Integrated Press, Weld, Paint & Final Assembly Plants · Vendor Park JIS Hubs · Rail Auto-Wagon Sidings · Regional Genuine Parts Depots",
        "erp": "SAP S/4HANA Automotive · JIS/Kanban EDI Vendor Portal · Plant MES & Andon · Finished Vehicle & Spare-Parts TMS",
        "terms": [
            "JIS / JIT — Just-in-Sequence Vendor Park Sync",
            "Takt-Time & Mixed-Model Line Balancing",
            "AFD / Rail Auto-Rake Finished Vehicle Dispatch",
            "VOR — Vehicle-Off-Road Genuine Parts Priority",
        ],
        "career_titles": [
            "Vice President — Supply Chain & Vendor Localization",
            "General Manager — Production Planning & Control (PPC)",
            "Head of Semiconductor, Powertrain & Sheet-Metal Sourcing",
            "Divisional Manager — Outbound Vehicle Logistics & Auto-Rakes",
            "National Head — Genuine Parts Warehouse & Dealer Replenishment",
            "Lead — Paint-Shop Sequencing & Plant OEE Reliability",
        ],
        "hide_agents": COLD_CHAIN_AGENT_IDS | FOOD_PERISHABLE_AGENT_IDS | RETAIL_STORE_PLANOGRAM_AGENT_IDS | {"keep_it_routing_advisor"},
        "hide_reason": "Hidden for Automotive OEM fit: discrete vehicle & spare-parts supply chain via vendor parks, auto-rakes, and dealerships (no cold-chain, perishable food expiry, or grocery planograms).",
        "custom_pillars": [
            ("model_variant_ibp", "01 · MODEL & VARIANT S&OP", "Model-Variant Demand, Trim Mix & Launch IBP", "Dealer booking velocity, EV/ICE trim mix & new model ramps", "Aligns regional dealership bookings and model/color/trim mix with multi-plant assembly capacity.", "#2563eb", "demand_wave", ["demand_forecasting", "sop_ibp", "portfolio_sku"]),
            ("tier_n_vendor_park", "02 · VENDOR PARK & SOURCING", "Tier-1/2/3 Vendor Localization, Chips & Tooling", "JIS supplier parks, steel/aluminium coils, semiconductors & PPAP", "Governs multi-tier component risk, sheet-metal/alloy indexing, and automated vendor scheduling agreements.", "#7c3aed", "supplier_graph", ["supplier_network", "material_packaging", "contract_po"]),
            ("press_paint_assembly", "03 · PRESS, PAINT & ASSEMBLY", "Mixed-Model Line Sequencing, Paint-Shop & QA", "Color-batch paint optimization, weld robotics OEE & torque QA", "Sequences mixed-model assembly lines at takt-time while minimizing paint-shop purge waste and defects.", "#ea580c", "factory_arm", ["production_scheduling", "capacity_planning", "quality_compliance"]),
            ("parts_warehousing", "04 · GENUINE PARTS & YARDS", "Genuine Spare-Parts Depots & Vehicle Stockyards", "VOR spare-parts MEIO, high-bay bin slotting & VIN yard tracking", "Optimizes regional spare-parts fill rates and finished-vehicle factory stockyard staging.", "#0284c7", "warehouse_rack", ["positioning_optimization", "warehouse_operations", "omnichannel_visibility"]),
            ("auto_rake_carrier_fleet", "05 · AUTO-RAKE & CARRIERS", "Rail Auto-Wagons, Car-Carrier Trailers & Export", "Bi-level rail rakes, port Ro-Ro drayage & transporter audit", "Maximizes rail share via dedicated auto-wagons and optimizes multi-car trailer load consolidation.", "#4f46e5", "corridor_lifo", ["first_mid_mile", "route_carrier"]),
            ("dealer_allocation_vor", "06 · DEALER & SERVICE NETWORK", "Dealership Vehicle Allocation, Schemes & VOR Parts", "Dealer wholesale dispatch, exchange schemes & workshop milk-runs", "Coordinates dealer inventory allocation, retail finance/exchange schemes, and rapid workshop parts delivery.", "#059669", "demand_wave", ["trade_promotion", "store_replenishment", "last_mile_delivery"]),
            ("warranty_returnable_racks", "07 · WARRANTY & STEEL RACKS", "Warranty Part Recovery, Remanufacturing & Racks", "Failed-part RMA root cause, transit damage & returnable stillages", "Tracks returnable vendor steel racks/dunnage, transit scratch claims, and warranty part remanufacturing.", "#e11d48", "conveyor_rack", ["returns_claims", "expiry_markdowns", "pallet_tote"]),
        ],
        "sub_pillars": {
            "demand_forecasting": "Regional Dealership Booking & Trim-Mix Sensing",
            "trade_promotion": "Festive Exchange Schemes & Dealer Incentive ROI",
            "sop_ibp": "Multi-Plant Vehicle & Powertrain S&OP",
            "portfolio_sku": "Model-Variant, Color & Trim Rationalization",
            "supplier_network": "Tier-1/2/3 Vendor Park & Semiconductor Risk",
            "material_packaging": "Auto-Grade Steel, Aluminium & Tooling Should-Cost",
            "contract_po": "Blanket Scheduling Agreements & 3-Way Match",
            "production_scheduling": "Mixed-Model Takt & Paint-Batch Sequencing",
            "capacity_planning": "Weld/Press Robotics OEE & Shift Manning",
            "quality_compliance": "End-of-Line Vision, Torque & PPAP Traceability",
            "positioning_optimization": "Genuine Parts Depot & Regional Stockyard MEIO",
            "warehouse_operations": "Parts High-Bay Slotting & VIN Yard Dispatch",
            "omnichannel_visibility": "Dealer Booking-to-VIN & Workshop Parts ATP",
            "first_mid_mile": "Rail Auto-Rake & Ro-Ro Port Export Linehaul",
            "store_replenishment": "Dealership Stock & Workshop VOR Replenishment",
            "last_mile_delivery": "Multi-Car Carrier & City Parts Milk-Run Routing",
            "route_carrier": "Car-Carrier Fleet & Freight Detention Audit",
            "returns_claims": "Warranty Part RMA & Transit Damage Claims",
            "expiry_markdowns": "Model-Year Changeover & Slow-Moving Parts Clearance",
            "pallet_tote": "Vendor Returnable Steel Rack & Dunnage Loop",
        },
        "processes": {
            "f2f": ("Booking-to-Assembly Forecast-to-Fulfill", "Connecting dealer variant bookings to vendor-park JIS call-offs and mixed-model assembly."),
            "o2d": ("VIN-to-Dealership Order-to-Delivery", "Tracking every vehicle from final assembly gate across rail auto-rakes to dealer handover."),
            "s2p": ("Tier-N Component, Coil & Chip Source-to-Pay", "Managing vendor localization, steel/alloy commodity indices, and blanket scheduling agreements."),
            "p2r": ("Warranty Diagnostics & Returnable Steel Rack Loop", "Reconciling high-value vendor racks/bins and automating warranty part root-cause recovery."),
        },
        "role_prefix_style": "industrial",
    },
    "pharma_lifesciences": {
        "sector": "Pharmaceuticals, Biologics & Regulated GMP Cold-Chain Supply Chain",
        "accent": "#0284c7",
        "secondary": "#0f172a",
        "exec_title": "Chief Technical Operations & Global Supply Chain Officer (API, Formulation & GMP Cold-Chain)",
        "thesis_tpl": (
            "Governing {co}'s Active Pharmaceutical Ingredient (API) synthesis, FDA/EMA-compliant oral & sterile "
            "formulation plants, 2–8°C validated cold-chain lanes, DSCSA/track-and-trace serialization, and hospital/wholesaler fulfillment."
        ),
        "sites_tpl": "API Chemical & Fermentation Plants · Sterile Fill-Finish & Oral Solid Dosage (OSD) Units · GDP-Validated 2–8°C Distribution Hubs",
        "erp": "SAP S/4HANA Life Sciences · LIMS & Electronic Batch Record (eBR) · Kinaxis RapidResponse · GDP Cold-Chain Telemetry",
        "terms": [
            "API / OSD — Active Ingredient & Oral Solid Dosage",
            "cGMP / eBR — Batch Release by Exception",
            "GDP 2–8°C — Validated Biologics Cold-Chain",
            "FEFO — Strict Expiry & Lot Serialization",
        ],
        "career_titles": [
            "VP — Global External Supply, API & Formulation Planning",
            "Head of GMP Quality Release & Electronic Batch Records",
            "Director — Validated Cold-Chain & Global Air/Ocean Logistics",
            "Category Lead — API Intermediates, Excipients & Sterile Vials",
            "Master Scheduler — Sterile Fill-Finish & Packaging Suites",
            "Head of Tender/Hospital Forecasting & Wholesaler Allocation",
        ],
        "hide_agents": RETAIL_STORE_PLANOGRAM_AGENT_IDS | {"keep_it_routing_advisor"},
        "hide_reason": "Hidden for Regulated Pharma fit: prescription hospital/wholesaler/pharmacy GDP distribution (no fashion keep-it refunds or supermarket aisle planograms).",
        "custom_pillars": [
            ("therapeutic_ibp", "01 · THERAPEUTIC & TENDER IBP", "Epidemiology Demand, Tender Bids & Launch IBP", "Seasonal disease surges, institutional tenders & LOE/launch ramps", "Forecasts prescription, hospital tender, and seasonal demand synchronized with regulatory market authorizations.", "#2563eb", "demand_wave", ["demand_forecasting", "trade_promotion", "sop_ibp", "portfolio_sku"]),
            ("api_excipient_sourcing", "02 · API & STERILE SOURCING", "API Intermediates, Excipients, Vials & CMO Sourcing", "DMF-qualified suppliers, sterile glass/stoppers & CMO governance", "Qualifies multi-source API/excipient vendors and manages contract manufacturing (CMO) supply agreements.", "#7c3aed", "supplier_graph", ["supplier_network", "material_packaging", "contract_po"]),
            ("gmp_formulation_qa", "03 · cGMP PLANTS & eBR QA", "API Synthesis, Sterile Fill-Finish & Batch Release", "Campaign scheduling, cleanroom OEE & LIMS/eBR release-by-exception", "Optimizes sterile/OSD suite changeovers and cuts batch record quality release lead-times from weeks to hours.", "#ea580c", "factory_arm", ["production_scheduling", "capacity_planning", "quality_compliance"]),
            ("gdp_vault_warehousing", "04 · GDP & SERIALIZED HUBS", "GDP Cold-Vaults, FEFO Buffers & Lot Serialization", "2–8°C / -20°C vaults, quarantine holds & serialized stock ATP", "Positions lot-tracked safety stock across regional GDP depots while preventing patient drug shortages.", "#0284c7", "warehouse_rack", ["positioning_optimization", "warehouse_operations", "omnichannel_visibility"]),
            ("validated_cold_logistics", "05 · 2–8°C COLD LOGISTICS", "Validated Air/Ocean Reefers & Wholesaler Dispatch", "Thermal lane qualification, excursion triage & hospital delivery", "Monitors real-time thermal logger telemetry across air/road lanes and prioritizes life-critical hospital orders.", "#059669", "corridor_lifo", ["first_mid_mile", "store_replenishment", "last_mile_delivery", "route_carrier"]),
            ("recall_expiry_containers", "06 · RECALL, FEFO & PASSIVE", "FEFO Expiry Prevention, DSCSA Recalls & Thermal Shippers", "Short-dated stock reallocation, recall trace & reusable phase-change boxes", "Minimizes expiry destruction, automates serialized lot returns, and recovers high-cost passive thermal shippers.", "#e11d48", "conveyor_rack", ["returns_claims", "expiry_markdowns", "pallet_tote"]),
        ],
        "sub_pillars": {},
        "processes": {
            "f2f": ("Molecule-to-Patient Forecast-to-Fulfill", "Linking API synthesis campaigns, sterile fill-finish suites, and global hospital/pharmacy demand."),
            "o2d": ("GDP Cold-Chain & Serialized Order-to-Delivery", "Zero-excursion 2–8°C fulfillment with full DSCSA lot traceability."),
            "s2p": ("DMF-Qualified API, Excipient & Vial Source-to-Pay", "Multi-tier GMP vendor qualification, CMO orchestration, and COA verification."),
            "p2r": ("FEFO Expiry Prevention & Reusable Thermal Shipper Loop", "Reallocating short-dated stock and recovering passive phase-change cold boxes."),
        },
        "role_prefix_style": "industrial",
    },
    "tech_enterprise_services": {
        "sector": "Enterprise Technology, Cloud Infrastructure Hardware & Global Operations",
        "accent": "#2563eb",
        "secondary": "#0f172a",
        "exec_title": "Chief Procurement, Hardware Supply Chain & Global Operations Officer",
        "thesis_tpl": (
            "Orchestrating {co}'s global IT/cloud server & edge hardware procurement, ODM/EMS contract manufacturing, "
            "regional integration & staging depots, client site deployment logistics, and circular e-waste / asset recovery."
        ),
        "sites_tpl": "Global Integration & Rack Staging Centers · Regional Spare-Parts Forward Stocking Locations (FSLs) · ODM/EMS Partner Hubs",
        "erp": "SAP S/4HANA · Ariba Strategic Sourcing · Kinaxis Supply Planning · Global IT Asset & Spare-Parts WMS",
        "terms": [
            "ODM / EMS — Contract Hardware & Rack Integration",
            "FSL — 4-Hour SLA Forward Stocking Location",
            "BOM / ECO — Engineering Change & Component Lifecycle",
            "ITAD — Certified IT Asset Disposition & Circularity",
        ],
        "career_titles": [
            "VP — Global Supply Chain, Procurement & Asset Operations",
            "Head of Semiconductor, Server & Telecom Sourcing",
            "Director — Demand & Spares Forecasting (FSL Network)",
            "Global Logistics & Trade Compliance Controller",
            "Manager — ODM Quality, Rack Integration & ECO Cutovers",
            "Head of ITAD Circularity & Scope-3 Supplier Carbon",
        ],
        "hide_agents": COLD_CHAIN_AGENT_IDS | FOOD_PERISHABLE_AGENT_IDS | RETAIL_STORE_PLANOGRAM_AGENT_IDS | {"keep_it_routing_advisor"},
        "hide_reason": "Hidden for Enterprise Tech & Hardware Operations fit: B2B server/device staging, FSL spares, and ODM sourcing (no cold-chain, perishable food, or retail grocery aisles).",
        "custom_pillars": [
            ("program_demand_ibp", "01 · DEPLOYMENT & SPARES IBP", "Client Rollout Demand, Refresh S&OP & Lifecycle", "Data-center rack rollouts, enterprise refresh cycles & EOL transitions", "Synchronizes enterprise deployment pipelines and 4-hour SLA spare-part buffers with ODM lead-times.", "#2563eb", "demand_wave", ["demand_forecasting", "trade_promotion", "sop_ibp", "portfolio_sku"]),
            ("odm_semicon_sourcing", "02 · ODM, SILICON & CONTRACTS", "Semiconductor, Server ODM & Strategic Sourcing", "GPU/ASIC allocation, EMS should-costing & MSA contract governance", "Secures long-lead silicon, server/network hardware, and global vendor service-level agreements.", "#7c3aed", "supplier_graph", ["supplier_network", "material_packaging", "contract_po"]),
            ("staging_integration_qa", "03 · RACK STAGING & ODM QA", "ODM Assembly, Rack Burn-In & ECO Cutovers", "Custom rack configuration, burn-in testing & zero-obsolescence ECOs", "Schedules rack integration centers, firmware/burn-in validation, and seamless hardware revision cutovers.", "#ea580c", "factory_arm", ["production_scheduling", "capacity_planning", "quality_compliance"]),
            ("fsl_global_logistics", "04 · FSL DEPOTS & GLOBAL TRADE", "Forward Stocking Locations (FSL) & White-Glove Logistics", "4-hour SLA spare hubs, customs/IOR clearance & air-ride delivery", "Positions critical spares across global FSLs and orchestrates customs-cleared white-glove site delivery.", "#0284c7", "corridor_lifo", ["positioning_optimization", "warehouse_operations", "omnichannel_visibility", "first_mid_mile", "store_replenishment", "last_mile_delivery", "route_carrier"]),
            ("rma_itad_circularity", "05 · RMA REPAIR & ITAD LOOP", "RMA Diagnostics, Refurbishment & Certified E-Waste", "Board-level RMA triage, harvest-for-spares & Scope-3 ledger", "Automates RMA failure triage, component refurbishment, and certified IT Asset Disposition (ITAD).", "#059669", "conveyor_rack", ["returns_claims", "expiry_markdowns", "pallet_tote"]),
        ],
        "sub_pillars": {},
        "processes": {
            "f2f": ("Pipeline-to-Deployment Forecast-to-Fulfill", "Aligning enterprise deal pipelines with silicon/ODM build slots and staging center capacity."),
            "o2d": ("Staging-to-Site White-Glove Order-to-Delivery", "Customs-compliant global dispatch and 4-hour SLA forward-stocking spare replenishment."),
            "s2p": ("Silicon, ODM & Cloud Hardware Source-to-Pay", "Multi-tier component risk sensing, BOM should-costing, and automated 3-way match."),
            "p2r": ("RMA Harvest-for-Spares & Certified ITAD Circularity", "Recovering high-value boards/optics and auditing zero-landfill e-waste recycling."),
        },
        "role_prefix_style": "industrial",
    },
}


def detect_division_archetype(company_name: str, division_name: str, notes: str = "", wiki_text: str = "") -> str:
    # Prioritize explicit company + division + user notes first so conglomerate divisions stay razor-sharp
    primary = f"{company_name} {division_name} {notes}".lower()
    full_blob = f"{primary} {wiki_text}".lower()

    if any(k in primary for k in ("tobacco", "cigarette", "iltd", "tm&d", "tmd", "itd", "leaf", "cigar", "vape", "philip morris", "bat ")):
        return "tobacco_tmd"
    if any(k in primary for k in ("cement", "ultratech", "clinker", "concrete", "holcim", "ambuja", "shree cement", "acc ", "dalmia", "grasim")):
        return "cement_heavy_materials"
    if any(k in primary for k in ("hindalco", "novelis", "metal", "aluminium", "aluminum", "steel", "copper", "mining", "vedanta", "jsw", "tata steel", "alcoa", "rio tinto")):
        return "metals_mining"
    if any(k in primary for k in ("tata consumer", "beverage", "tea", "coffee", "tetley", "starbucks", "pepsi", "coca-cola", "coke", "keurig")):
        return "beverages_packaged_foods"
    if any(k in primary for k in ("food", "aashirvaad", "sunfeast", "bingo", "snack", "dairy", "agri", "grocery", "nestle", "danone", "mondelez", "tyson")):
        return "fmcg_foods"

    # Check both primary & Wikipedia company intelligence for broader global industries
    if any(k in full_blob for k in ("automobile", "automotive", "maruti", "suzuki", "motor", "vehicle", "car manufacturer", "toyota", "hyundai", "mahindra", "ford", "volkswagen", "bmw", "tesla", "bajaj auto", "hero motocorp", "ashok leyland")):
        return "automotive_oem"
    if any(k in full_blob for k in ("pharmaceutical", "biopharmaceutical", "biotech", "vaccin", "pfizer", "novartis", "roche", "sanofi", "astrazeneca", "dr. reddy", "sun pharma", "cipla", "lupin", "biocon", "abbott", "merck")):
        return "pharma_lifesciences"
    if any(k in full_blob for k in ("cement", "clinker", "ready-mix concrete")):
        return "cement_heavy_materials"
    if any(k in full_blob for k in ("smelting", "steelmaker", "aluminium", "mining", "metallurg", "iron ore")):
        return "metals_mining"
    if any(k in full_blob for k in ("information technology", "it services", "software", "semiconductor", "electronics", "wipro", "infosys", "tcs", "hcl", "tech mahindra", "cisco", "dell", "hp ", "lenovo", "apple", "tsmc", "nvidia", "foxconn")):
        return "tech_enterprise_services"
    if any(k in full_blob for k in ("beverage", "tea", "coffee", "soft drink", "brewery")):
        return "beverages_packaged_foods"
    if any(k in full_blob for k in ("food", "confectionery", "dairy", "packaged goods", "agri", "itc")):
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

    if arch_key == "beverages_packaged_foods":
        names = {
            "demand_sensing_agent": "Beverage & Staples Demand Sensing",
            "promo_lift_simulator": "Festive Pack & GT/MT Scheme Simulator",
            "sop_scenario_weaver": "Crop-to-Cart S&OP Weaver",
            "commodity_index_advisor": "Tea Auction, Pulse & Spice Advisor",
            "finite_production_scheduler": "Master Blending & Pouch Scheduler",
            "inline_yield_guardian": "Aroma, Moisture & FSSAI Vision QA",
            "meio_safety_stock_agent": "Mother Depot & CFA Safety Stock",
            "warehouse_slotting_agent": "FEFO CFA Pallet & Case Slotting",
            "dynamic_markdown_agent": "FEFO Freshness Re-Allocation Agent",
        }
        return names.get(agent_id, "")

    if arch_key == "automotive_oem":
        names = {
            "demand_sensing_agent": "Dealer Booking & Trim-Mix Sensing",
            "sop_scenario_weaver": "Multi-Plant Vehicle & Powertrain S&OP",
            "tier_n_risk_sentinel": "Vendor Park & Semiconductor Sentinel",
            "commodity_index_advisor": "Auto-Steel, Alloy & Chip Index Advisor",
            "finite_production_scheduler": "Mixed-Model Takt & Paint Sequencer",
            "predictive_oee_sentinel": "Weld/Press Robotics OEE Sentinel",
            "inline_yield_guardian": "End-of-Line Vision & Torque QA",
            "meio_safety_stock_agent": "Genuine Parts & VOR Depot Stock Agent",
            "load_consolidation_agent": "Auto-Rake & Car-Carrier Consolidator",
            "rti_balance_reconciler": "Vendor Steel Rack & Dunnage Ledger",
        }
        return names.get(agent_id, "")

    if arch_key == "pharma_lifesciences":
        names = {
            "demand_sensing_agent": "Epidemiology & Tender Demand Sensing",
            "sop_scenario_weaver": "API-to-Sterile Fill S&OP Weaver",
            "tier_n_risk_sentinel": "DMF API & Excipient Risk Sentinel",
            "finite_production_scheduler": "Sterile Suite & OSD Campaign Scheduler",
            "batch_record_auditor": "Electronic Batch Record (eBR) Release Agent",
            "meio_safety_stock_agent": "GDP Vault & Hospital Shortage Buffer",
            "cold_chain_auditor": "Validated 2–8°C GDP Lane Auditor",
            "dynamic_markdown_agent": "FEFO Short-Dated Lot Re-Allocator",
            "rti_balance_reconciler": "Passive Thermal Shipper Loop Ledger",
        }
        return names.get(agent_id, "")

    if arch_key == "tech_enterprise_services":
        names = {
            "demand_sensing_agent": "Deployment & FSL Spares Sensing",
            "sop_scenario_weaver": "Silicon-to-Rack Rollout S&OP Weaver",
            "tier_n_risk_sentinel": "Foundry, ASIC & ODM Risk Sentinel",
            "eco_cutover_orchestrator": "Hardware Revision & BOM Cutover Agent",
            "meio_safety_stock_agent": "4-Hour SLA Forward Stocking (FSL) Agent",
            "reverse_rma_optimizer": "Board-Level RMA & ITAD Triage Agent",
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
    from enterprise_twin.tools.public_web_career_miner import (
        fetch_wikipedia_company_summary,
        search_public_career_titles,
    )

    cat = load_canonical_catalog()
    depts = cat["departments"]
    personas_cat = cat["personas"]
    agents_cat = cat["agents"]

    clean_co = company_name.strip()
    if clean_co.lower() in ("itc", "itc ltd"):
        clean_co = "ITC Limited"
    elif clean_co.lower() in ("abg", "aditya birla"):
        clean_co = "Aditya Birla Group"
    elif clean_co.lower() in ("hul",):
        clean_co = "Hindustan Unilever Limited"

    clean_div = division_name.strip()
    wp_info = fetch_wikipedia_company_summary(clean_co, clean_div)
    wiki_blob = f"{wp_info.get('description', '')} {wp_info.get('extract', '')}"

    arch_key = detect_division_archetype(clean_co, clean_div, user_notes, wiki_blob)
    arch = DIVISION_ARCHETYPES[arch_key]

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
            "message": f"Mapping Organization Pillars, 20 Sub-Pillars & Corporate Job Titles for {disp}...",
            "detail": f"Applying authentic {arch['sector']} structure & filtering inapplicable agents",
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

    live_career_titles = search_public_career_titles(clean_co, clean_div)

    citations: List[GroundingCitation] = []
    if wp_info.get("page_url"):
        citations.append(GroundingCitation(title=f"{wp_info.get('canonical_title', clean_co)} — Corporate Operations Overview", url=wp_info["page_url"]))
    if logo_spec.source_url:
        citations.append(GroundingCitation(title=f"{clean_co} Official Brand Mark Source", url=logo_spec.source_url))

    exec_thesis = arch["thesis_tpl"].format(co=disp)
    if wp_info.get("description"):
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

    custom_pillars: List[CustomPillarSpec] = []
    for idx, cp_tup in enumerate(arch.get("custom_pillars") or []):
        p_id, badge, p_name, p_tag, p_sub, p_col, p_wm, p_sps = cp_tup
        custom_pillars.append(
            CustomPillarSpec(
                pillar_id=p_id,
                v_num=f"{idx + 1:02d}",
                scor_badge=badge,
                name=p_name,
                tagline=f"{disp} · {p_tag}",
                subtitle=p_sub,
                color=p_col,
                watermark_type=p_wm,
                sub_pillar_ids=list(p_sps),
            )
        )

    spec = TwinOverlaySpec(
        twin_slug=twin_slug,
        company_name=company_name,
        canonical_name=clean_co,
        division_name=clean_div,
        brand=brand,
        custom_pillars=custom_pillars,
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

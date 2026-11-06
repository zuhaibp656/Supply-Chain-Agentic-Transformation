"""Enterprise Supply Chain Abbreviation Expander & Executive Glossary.

Mandate: Never present cryptic supply chain or corporate domain acronyms
without their full plain-English expansion (e.g. SCOT -> Supply Chain Optimization
Technologies (SCOT), CBAM -> Carbon Border Adjustment Mechanism (CBAM),
TM&D -> Trade Marketing & Distribution (TM&D), OTIF -> On-Time In-Full (OTIF)).
"""

from typing import Any, Dict, List
import re

# Comprehensive registry of domain acronyms -> full executive form & explanation
DOMAIN_ABBREVIATIONS: List[Dict[str, str]] = [
    {
        "abbr": "SCOT",
        "full_name": "Supply Chain Optimization Technologies (SCOT)",
        "expansion": "Supply Chain Optimization Technologies",
        "category": "E-Commerce & AI Demand Placement",
        "definition": "Amazon's proprietary machine learning and mathematical optimization suite that automates multi-echelon demand forecasting, automated procurement, and regional inventory placement across fulfillment centers.",
    },
    {
        "abbr": "CBAM",
        "full_name": "Carbon Border Adjustment Mechanism (CBAM)",
        "expansion": "Carbon Border Adjustment Mechanism",
        "category": "Regulatory & Global Trade ESG",
        "definition": "The European Union's landmark climate policy tariff requiring importers of carbon-intensive goods (steel, cement, aluminum, fertilizer, electricity, hydrogen) to buy CBAM certificates reflecting their embedded Scope 1 and Scope 2 emissions.",
    },
    {
        "abbr": "TM&D",
        "full_name": "Trade Marketing & Distribution (TM&D)",
        "expansion": "Trade Marketing & Distribution",
        "category": "FMCG / CPG Distribution Channels",
        "definition": "The dedicated field sales, wholesale distributor management, and retail outlet execution arm responsible for secondary replenishment, beat planning, and point-of-sale visibility.",
    },
    {
        "abbr": "TMD",
        "full_name": "Trade Marketing & Distribution (TM&D)",
        "expansion": "Trade Marketing & Distribution",
        "category": "FMCG / CPG Distribution Channels",
        "definition": "Alternate abbreviation for Trade Marketing & Distribution.",
    },
    {
        "abbr": "ILTD",
        "full_name": "India Leaf Tobacco Division (ILTD)",
        "expansion": "India Leaf Tobacco Division",
        "category": "Agri-Sourcing & Primary Processing",
        "definition": "ITC's primary leaf procurement, grower partnership, and redrying operations division managing farmer relationships, crop grading, and bonded storage.",
    },
    {
        "abbr": "SMIPL",
        "full_name": "Suzuki Motorcycle India Private Limited (SMIPL)",
        "expansion": "Suzuki Motorcycle India Private Limited",
        "category": "Automotive OEM & Two-Wheelers",
        "definition": "Suzuki Motor Corporation's wholly owned two-wheeler manufacturing subsidiary in India, operating assembly plants in Gurugram and nationwide dealership networks.",
    },
    {
        "abbr": "OTIF",
        "full_name": "On-Time In-Full (OTIF)",
        "expansion": "On-Time In-Full",
        "category": "Service Level & Customer Fulfillment",
        "definition": "The premier supply chain delivery KPI measuring the exact percentage of orders delivered to the customer on the agreed date with complete requested quantities and zero split-shipment defects.",
    },
    {
        "abbr": "RMA",
        "full_name": "Return Merchandise Authorization (RMA)",
        "expansion": "Return Merchandise Authorization",
        "category": "Reverse Logistics & Customer Service",
        "definition": "The official authorization and tracking record that initiates a product return, warranty evaluation, credit issuance, or reverse grading workflow.",
    },
    {
        "abbr": "OEE",
        "full_name": "Overall Equipment Effectiveness (OEE)",
        "expansion": "Overall Equipment Effectiveness",
        "category": "Manufacturing & Plant Reliability",
        "definition": "The gold-standard manufacturing metric multiplying plant equipment Availability × Performance rate × Quality yield to quantify true asset productivity.",
    },
    {
        "abbr": "CSRD",
        "full_name": "Corporate Sustainability Reporting Directive (CSRD)",
        "expansion": "Corporate Sustainability Reporting Directive",
        "category": "ESG Compliance & Disclosure",
        "definition": "EU directive requiring large enterprises to audit and publicly disclose double-materiality environmental, social, and supply-chain carbon governance metrics.",
    },
    {
        "abbr": "EUDR",
        "full_name": "European Union Deforestation Regulation (EUDR)",
        "expansion": "European Union Deforestation Regulation",
        "category": "ESG & Commodity Due Diligence",
        "definition": "European Union regulation prohibiting the import or sale of commodities (cattle, cocoa, coffee, oil palm, rubber, soya, wood) linked to deforestation after December 2020, mandating plot-level GPS polygon geolocation.",
    },
    {
        "abbr": "ATS",
        "full_name": "Amazon Transportation Services (ATS)",
        "expansion": "Amazon Transportation Services",
        "category": "Middle-Mile Logistics & Linehaul",
        "definition": "Amazon's dedicated middle-mile logistics network moving freight between vendor facilities, fulfillment centers, sortation centers, air hubs, and delivery stations.",
    },
    {
        "abbr": "AMZL",
        "full_name": "Amazon Logistics (AMZL)",
        "expansion": "Amazon Logistics",
        "category": "Last-Mile Delivery",
        "definition": "Amazon's proprietary last-mile delivery network operating out of regional delivery stations through Delivery Service Partners (DSPs) and Flex drivers.",
    },
    {
        "abbr": "DSP",
        "full_name": "Delivery Service Partner (DSP)",
        "expansion": "Delivery Service Partner",
        "category": "Last-Mile Delivery Ecosystem",
        "definition": "Independent contracted logistics business owners who operate branded delivery van fleets to execute last-mile doorstep parcel deliveries for Amazon.",
    },
    {
        "abbr": "MEIO",
        "full_name": "Multi-Echelon Inventory Optimization (MEIO)",
        "expansion": "Multi-Echelon Inventory Optimization",
        "category": "Inventory Theory & Network Buffers",
        "definition": "A mathematical planning technique that models inventory across all network tiers simultaneously (plants, central DCs, regional hubs, stores) to place safety buffers at minimum holding cost.",
    },
    {
        "abbr": "PPAP",
        "full_name": "Production Part Approval Process (PPAP)",
        "expansion": "Production Part Approval Process",
        "category": "Supplier Quality & Sourcing",
        "definition": "The automotive and aerospace industry standard process establishing that a supplier's manufacturing process can consistently produce parts meeting all engineering specifications during actual production runs.",
    },
    {
        "abbr": "S&OP",
        "full_name": "Sales and Operations Planning (S&OP)",
        "expansion": "Sales and Operations Planning",
        "category": "Integrated Planning & Consensus",
        "definition": "The monthly executive consensus process balancing customer commercial demand with operational supply capacity, manufacturing constraints, and financial targets.",
    },
    {
        "abbr": "IBP",
        "full_name": "Integrated Business Planning (IBP)",
        "expansion": "Integrated Business Planning",
        "category": "Integrated Planning & Enterprise Finance",
        "definition": "The advanced evolution of S&OP integrating product portfolios, operational supply chains, multi-year strategic plans, and enterprise financial P&Ls into one continuous plan.",
    },
    {
        "abbr": "SCOR",
        "full_name": "Supply Chain Operations Reference (SCOR)",
        "expansion": "Supply Chain Operations Reference",
        "category": "Industry Standard Framework",
        "definition": "The global standard process reference model developed by the Association for Supply Chain Management (ASCM) categorizing end-to-end supply chains into Plan, Source, Make, Deliver, Return, and Enable.",
    },
    {
        "abbr": "ASN",
        "full_name": "Advance Shipping Notice (ASN)",
        "expansion": "Advance Shipping Notice",
        "category": "Inbound Warehouse & EDI",
        "definition": "An electronic data transmission (EDI 856) sent by a supplier prior to cargo arrival detailing shipment contents, purchase order line items, lot codes, carrier details, and estimated time of arrival.",
    },
    {
        "abbr": "BOM",
        "full_name": "Bill of Materials (BOM)",
        "expansion": "Bill of Materials",
        "category": "Manufacturing & Product Structure",
        "definition": "A comprehensive list of raw materials, sub-assemblies, components, packaging, and quantities required to manufacture an end product.",
    },
    {
        "abbr": "EDI",
        "full_name": "Electronic Data Interchange (EDI)",
        "expansion": "Electronic Data Interchange",
        "category": "B2B Transaction Automation",
        "definition": "Standardized computer-to-computer exchange of business transaction documents between enterprise trading partners (e.g. POs, ASNs, Invoices, STOs).",
    },
    {
        "abbr": "VMI",
        "full_name": "Vendor-Managed Inventory (VMI)",
        "expansion": "Vendor-Managed Inventory",
        "category": "Collaborative Replenishment",
        "definition": "A collaborative supply chain model where the supplier takes full operational responsibility for monitoring and replenishing stock at the customer's warehouse or plant within agreed minimum/maximum bands.",
    },
    {
        "abbr": "DIO",
        "full_name": "Days Inventory Outstanding (DIO)",
        "expansion": "Days Inventory Outstanding",
        "category": "Working Capital & Cash Conversion",
        "definition": "Financial efficiency metric indicating the average number of days an enterprise holds inventory before turning it into sales.",
    },
    {
        "abbr": "DPO",
        "full_name": "Days Payable Outstanding (DPO)",
        "expansion": "Days Payable Outstanding",
        "category": "Working Capital & Procurement",
        "definition": "Financial metric showing the average number of days a company takes to pay its suppliers and trade vendors.",
    },
    {
        "abbr": "DSO",
        "full_name": "Days Sales Outstanding (DSO)",
        "expansion": "Days Sales Outstanding",
        "category": "Working Capital & Receivables",
        "definition": "Financial metric measuring the average number of days it takes a company to collect cash receivables after completing a commercial sale.",
    },
    {
        "abbr": "ATP",
        "full_name": "Available-to-Promise (ATP)",
        "expansion": "Available-to-Promise",
        "category": "Order Commitment & Allocation",
        "definition": "Real-time enterprise calculation of uncommitted inventory and planned production available to quote confirmed delivery dates to incoming customer orders.",
    },
    {
        "abbr": "CTP",
        "full_name": "Capable-to-Promise (CTP)",
        "expansion": "Capable-to-Promise",
        "category": "Dynamic Production Commitment",
        "definition": "An advanced order quoting process that dynamically commits unallocated manufacturing capacity, raw material availability, and machine time for orders exceeding on-hand inventory.",
    },
    {
        "abbr": "TCO",
        "full_name": "Total Cost of Ownership (TCO)",
        "expansion": "Total Cost of Ownership",
        "category": "Strategic Sourcing & Cost Analysis",
        "definition": "Comprehensive evaluation of the true landed cost of a purchased component or equipment over its entire lifecycle, including purchase price, freight, duties, quality failures, downtime, and disposal.",
    },
    {
        "abbr": "SRM",
        "full_name": "Supplier Relationship Management (SRM)",
        "expansion": "Supplier Relationship Management",
        "category": "Procurement Strategy & Governance",
        "definition": "Systematic enterprise approach to managing supplier relationships, scorecard performance, joint innovation, risk mitigation, and contractual governance.",
    },
    {
        "abbr": "TMS",
        "full_name": "Transportation Management System (TMS)",
        "expansion": "Transportation Management System",
        "category": "Freight & Fleet Execution",
        "definition": "Software platform that manages carrier contracting, route planning, freight audit, load tendering, shipment tracking, and yard logistics.",
    },
    {
        "abbr": "WMS",
        "full_name": "Warehouse Management System (WMS)",
        "expansion": "Warehouse Management System",
        "category": "Distribution Center Operations",
        "definition": "Software application controlling daily warehouse operations including receiving, put-away, slotting, wave picking, packing, and dispatch.",
    },
    {
        "abbr": "MRP",
        "full_name": "Material Requirements Planning (MRP)",
        "expansion": "Material Requirements Planning",
        "category": "Production Scheduling & Purchasing",
        "definition": "Time-phased calculation determining what materials to order, how much to order, and when to order based on BOM explosions, lead times, and Master Production Schedules.",
    },
    {
        "abbr": "LIFO",
        "full_name": "Last-In, First-Out (LIFO)",
        "expansion": "Last-In, First-Out",
        "category": "Truck Loading & Inventory Method",
        "definition": "Inventory and vehicle load planning principle where items loaded last into a trailer are delivered first along multi-stop delivery routes to eliminate reshuffling.",
    },
    {
        "abbr": "FIFO",
        "full_name": "First-In, First-Out (FIFO)",
        "expansion": "First-In, First-Out",
        "category": "Perishables & Batch Rotation",
        "definition": "Inventory stock rotation rule where the oldest acquired batches are consumed or dispatched first to eliminate spoilage and obsolescence.",
    },
    {
        "abbr": "3PL",
        "full_name": "Third-Party Logistics (3PL)",
        "expansion": "Third-Party Logistics",
        "category": "Outsourced Logistics",
        "definition": "External logistics service provider contracted to manage warehousing, transportation, packaging, and freight distribution.",
    },
    {
        "abbr": "4PL",
        "full_name": "Fourth-Party Logistics (4PL)",
        "expansion": "Fourth-Party Logistics",
        "category": "Lead Logistics Partner",
        "definition": "An overarching integrator that oversees, manages, and orchestrates an enterprise's entire logistics network, including multiple 3PLs and carriers.",
    },
    {
        "abbr": "FC",
        "full_name": "Fulfillment Center (FC)",
        "expansion": "Fulfillment Center",
        "category": "E-Commerce Fulfillment",
        "definition": "High-velocity distribution facility designed specifically for receiving inventory, robotic stowage, pick-pack-ship operations, and parcel carrier sorting.",
    },
]

ABBR_MAP: Dict[str, Dict[str, str]] = {item["abbr"]: item for item in DOMAIN_ABBREVIATIONS}


def _safe_expand(text: str, abbr: str, full_name: str, check_keyword: str) -> str:
    """Replaces standalone abbr with full_name unless check_keyword is already in text."""
    if not text or not isinstance(text, str):
        return text
    if check_keyword.lower() in text.lower():
        return text
    pattern = rf"\b{re.escape(abbr)}\b"
    return re.sub(pattern, full_name, text)


def expand_text_abbreviations(text: str, target_company: str = "") -> str:
    """Smartly expands standalone domain acronyms into 'Full Form (ABBR)'. Guaranteed idempotent."""
    if not text or not isinstance(text, str):
        return text

    res = text

    # 1. High-priority user complained terms: SCOT, CBAM, TM&D, ILTD, SMIPL
    res = _safe_expand(res, "SCOT", "Supply Chain Optimization Technologies (SCOT)", "Supply Chain Optimization")
    res = _safe_expand(res, "CBAM", "Carbon Border Adjustment Mechanism (CBAM)", "Carbon Border Adjustment")
    res = _safe_expand(res, "TM&D", "Trade Marketing & Distribution (TM&D)", "Trade Marketing")
    res = _safe_expand(res, "TMD", "Trade Marketing & Distribution (TM&D)", "Trade Marketing")
    res = _safe_expand(res, "ILTD", "India Leaf Tobacco Division (ILTD)", "India Leaf Tobacco")
    res = _safe_expand(res, "SMIPL", "Suzuki Motorcycle India Private Limited (SMIPL)", "Suzuki Motorcycle India")

    # 2. General supply chain acronyms
    res = _safe_expand(res, "OTIF", "On-Time In-Full (OTIF)", "On-Time In-Full")
    res = _safe_expand(res, "OEE", "Overall Equipment Effectiveness (OEE)", "Overall Equipment")
    res = _safe_expand(res, "RMA", "Return Merchandise Authorization (RMA)", "Return Merchandise")
    res = _safe_expand(res, "CSRD", "Corporate Sustainability Reporting Directive (CSRD)", "Corporate Sustainability Reporting")
    res = _safe_expand(res, "EUDR", "European Union Deforestation Regulation (EUDR)", "European Union Deforestation")
    res = _safe_expand(res, "PPAP", "Production Part Approval Process (PPAP)", "Production Part Approval")
    res = _safe_expand(res, "MEIO", "Multi-Echelon Inventory Optimization (MEIO)", "Multi-Echelon")

    # 3. Contextual Amazon terms
    if "amazon" in res.lower() or target_company.lower() == "amazon" or "fulfillment" in res.lower():
        res = _safe_expand(res, "ATS", "Amazon Transportation Services (ATS)", "Amazon Transportation")
        res = _safe_expand(res, "AMZL", "Amazon Logistics (AMZL)", "Amazon Logistics")
        res = _safe_expand(res, "DSP", "Delivery Service Partner (DSP)", "Delivery Service Partner")
        res = _safe_expand(res, "DSPs", "Delivery Service Partners (DSPs)", "Delivery Service Partner")
        if " FC " in res or " FCs " in res or res.endswith(" FC") or " FC," in res or " FC." in res:
            res = _safe_expand(res, "FCs", "Fulfillment Centers (FCs)", "Fulfillment Center")
            res = _safe_expand(res, "FC", "Fulfillment Center (FC)", "Fulfillment Center")

    return res


def canonicalize_division_display(company: str, division: str) -> str:
    """Canonicalizes informal colloquial inputs into official formal corporate operating entities."""
    co_clean = (company or "").strip().lower()
    div_clean = (division or "").strip().lower()

    if "amazon" in co_clean:
        if not div_clean or any(k in div_clean for k in ("e-com", "ecom", "retail", "consumer", "stores", "india", "seller")):
            return "Worldwide Amazon Stores & Consumer Fulfillment"
        if "aws" in div_clean or "cloud" in div_clean:
            return "Amazon Web Services (AWS Infrastructure & Cloud Operations)"
        return f"Amazon — {division.strip()}"

    if "suzuki" in co_clean:
        if not div_clean or any(k in div_clean for k in ("two", "bike", "motor", "2w", "scooter", "smipl")):
            return "Suzuki Motorcycle Division (Two-Wheelers & SMIPL)"
        return f"Suzuki — {division.strip()}"

    if "itc" in co_clean:
        if any(k in div_clean for k in ("tm&d", "tmd", "cigar", "tobacco", "iltd", "leaf")):
            return "Cigarettes & Leaf Tobacco (India Leaf Tobacco Division [ILTD] & Trade Marketing and Distribution [TM&D])"
        if any(k in div_clean for k in ("food", "aashirvaad", "sunfeast", "agri", "bingo")):
            return "Foods Division (ICML Agri-Business & Branded Packaged Foods)"
        return f"ITC Limited — {division.strip()}"

    if "aditya birla" in co_clean or "abg" in co_clean:
        if any(k in div_clean for k in ("cement", "ultra", "clinker")):
            return "UltraTech Cement Division"
        if any(k in div_clean for k in ("metal", "hindalco", "copper", "alu")):
            return "Hindalco Industries (Aluminium & Copper)"

    return division.strip()


def recursive_expand_twin_data(obj: Any, target_company: str = "") -> Any:
    """Recursively walks a twin JSON structure and applies abbreviation expansions."""
    if isinstance(obj, str):
        return expand_text_abbreviations(obj, target_company=target_company)
    elif isinstance(obj, list):
        return [recursive_expand_twin_data(item, target_company) for item in obj]
    elif isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            if k in ("twin_slug", "brand_accent", "brand_secondary", "data_uri", "source_url", "color", "pillar_id", "id", "agent_id", "persona_id", "aspect_ratio", "watermark_type"):
                new_dict[k] = v
            else:
                new_dict[k] = recursive_expand_twin_data(v, target_company)
        return new_dict
    return obj

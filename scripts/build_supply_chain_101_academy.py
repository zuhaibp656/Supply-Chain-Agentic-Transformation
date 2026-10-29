#!/usr/bin/env python3
"""Builds the standalone Interactive Supply Chain 101 Academy:
- supply_chain_101_interactive_academy.html (and copies in docs/, zipline_dist/, dist/itc_limited/)
- SUPPLY_CHAIN_101_MASTER_GUIDE.md (and copy in docs/SUPPLY_CHAIN_101_MASTER_GUIDE.md)
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# =============================================================================
# 1. 56 COMPREHENSIVE FLASHCARDS (EVERY ACRONYM SPELLED OUT + PLAIN ENGLISH)
# =============================================================================
FLASHCARDS = [
    # --- TOP 15 & PLANNING / FORECASTING ---
    {
        "term": "SKU",
        "full": "Stock Keeping Unit",
        "cat": "planning",
        "top15": True,
        "hook": "A unique code for one exact product size, flavor, or color.",
        "plain": "A shirt in Medium Blue and the same shirt in Large Blue are two different SKUs. Every barcode in a warehouse or store represents one specific SKU.",
        "example": "A beverage company makes 1 brand of sports drink, but in 4 flavors × 3 bottle sizes = 12 different SKUs to forecast and stock.",
        "customer_tip": "Ask: 'How many active SKUs do you manage across your warehouses, and which 20% of SKUs drive 80% of your sales?' (Show: Demand Sensing Agent / SLOB Disposition Agent)."
    },
    {
        "term": "POS",
        "full": "Point of Sale (Cash Register Scans)",
        "cat": "planning",
        "top15": True,
        "hook": "Real-time data of what shoppers are actually buying at the checkout counter today.",
        "plain": "When a cashier scans an item at Walmart or Target, that's a POS scan. If a manufacturer only looks at what Walmart's warehouse orders (instead of daily POS store scans), they are blind to real customer demand by 2 to 4 weeks.",
        "example": "During a sudden Texas heatwave, POS scans for sports drinks jump +35% on Friday, even though the retailer hasn't placed a new warehouse order yet.",
        "customer_tip": "Say: 'Our Demand Sensing Agent reads daily POS scans + weather to catch demand spikes 14 days before legacy ERP orders arrive.'"
    },
    {
        "term": "S&OP",
        "full": "Sales & Operations Planning",
        "cat": "planning",
        "top15": True,
        "hook": "The monthly meeting where Sales, Finance, and Factory leaders agree on one single plan.",
        "plain": "Sales always wants tons of inventory so they never miss a sale. Finance wants minimal inventory to save cash. Factories want steady schedules without last-minute changes. S&OP is the monthly process to align all three teams on ONE consensus number.",
        "example": "Sales forecasts 120,000 units, but the factory can only build 100,000 without expensive overtime. In S&OP, the AI simulates whether paying overtime is worth the extra profit.",
        "customer_tip": "Say: 'Our S&OP Scenario Weaver turns a 3-week spreadsheet argument into a 30-second live profit trade-off simulation.'"
    },
    {
        "term": "IBP",
        "full": "Integrated Business Planning (e.g., SAP IBP)",
        "cat": "planning",
        "top15": False,
        "hook": "Modern planning software that links supply chain plans directly to financial P&L targets.",
        "plain": "IBP is the evolution of S&OP software (like SAP IBP or Kinaxis). Instead of just counting boxes, IBP translates every supply chain forecast into dollars: Revenue, Gross Margin, and Working Capital.",
        "example": "When our Demand Sensing Agent updates a forecast, it writes the new numbers directly into SAP IBP so factories and finance see the update immediately.",
        "customer_tip": "Say: 'Our agents don't replace your IBP system — they act as an intelligent brain on top of SAP IBP or Kinaxis and write clean numbers back automatically.'"
    },
    {
        "term": "WAPE & MAPE",
        "full": "Weighted Absolute Percentage Error (Forecast Error %)",
        "cat": "planning",
        "top15": True,
        "hook": "The scoreboard for how wrong your demand forecast was (Lower % = Better!).",
        "plain": "If you forecasted you would sell 100 units, and you actually sold 80 units, you were off by 20 units (a 20% error). WAPE weights the error by volume/dollars so a miss on your #1 best-seller matters more than a miss on a tiny item.",
        "example": "Reducing WAPE from 25% down to 15% means your forecast is 10% more accurate — saving millions in emergency air freight and unsold inventory.",
        "customer_tip": "When a customer says 'Our WAPE is 30%', say: 'That means forecasts are off by Nearly a third. Our Demand Sensing Agent typically cuts WAPE by 4 to 8 percentage points.'"
    },
    {
        "term": "FVA",
        "full": "Forecast Value Added",
        "cat": "planning",
        "top15": False,
        "hook": "Measures whether a human touching the computer's forecast made it better or worse!",
        "plain": "Often, an AI generates a great statistical forecast, and then a salesperson manually increases it by +20% 'just to be safe.' FVA checks if that human override actually improved accuracy. Negative FVA means the human made the forecast worse!",
        "example": "A regional sales manager inflates their forecast by +15% every quarter (Negative FVA of -4.2%). Our agent detects this chronic optimism bias and automatically dampens it.",
        "customer_tip": "Say: 'Studies show over 50% of manual forecast overrides have negative FVA. Our agent audits human overrides and strips out chronic bias automatically.'"
    },
    {
        "term": "CPFR",
        "full": "Collaborative Planning, Forecasting & Replenishment",
        "cat": "planning",
        "top15": False,
        "hook": "When a brand (like Pepsi) and a retailer (like Walmart) share data to plan together.",
        "plain": "Instead of guessing what Walmart will order, the manufacturer and retailer share their forecasts and store inventory data every week so shelves stay full without overstocking warehouses.",
        "example": "Walmart's forecast says 580,000 units, while the brand's internal forecast says 500,000. Our CPFR Sync Agent reconciles the gap using daily POS store scans.",
        "customer_tip": "Show the Collaborative CPFR & POS Harmonizer (`cpfr_sync_agent`) whenever a customer sells through big retail chains."
    },
    {
        "term": "Demand Censorship",
        "full": "Hidden Lost Sales During a Stockout",
        "cat": "planning",
        "top15": False,
        "hook": "When you sell 0 units because the shelf was empty — NOT because nobody wanted to buy!",
        "plain": "Legacy ERPs look at historical sales. If a store ran out of stock on Wednesday, Thursday's sales are recorded as 0. A dumb system thinks 'Nobody wants this product anymore!' and lowers next week's forecast. That's Demand Censorship.",
        "example": "A store scans 0 units for 3 days while 40 shoppers walked away empty-handed. Our agent detects the stockout and imputes (estimates) the true demand that was lost.",
        "customer_tip": "Bringing up 'Demand Censorship' in a meeting immediately makes you sound like a seasoned supply chain expert!"
    },
    {
        "term": "Bullwhip Effect",
        "full": "Demand Distortion Upstream Across the Supply Chain",
        "cat": "planning",
        "top15": True,
        "hook": "A tiny +5% ripple in shopper buying turns into a massive +40% panic wave at the factory.",
        "plain": "When shoppers buy slightly more of an item, the store panics and orders extra. The distributor sees that bigger order, panics more, and orders even more from the factory. The factory orders huge amounts of raw materials — and then everyone is stuck with mountains of excess stock.",
        "example": "Remember the toilet paper shortage? People bought 10% more at home, which caused 300% panic orders at paper mills.",
        "customer_tip": "Say: 'AI Agents eliminate the Bullwhip Effect by connecting every layer of your supply chain to real-time customer consumption.'"
    },
    {
        "term": "NPI",
        "full": "New Product Introduction",
        "cat": "planning",
        "top15": False,
        "hook": "Launching a brand-new product that has zero historical sales data.",
        "plain": "Traditional forecasting relies on last year's sales. But what if you're launching a brand-new flavor or gadget? You have zero history! NPI profiling uses 'look-alike' past launches and early social/store signals to predict demand.",
        "example": "Launching a new zero-sugar drink: the NPI Demand Profiler matches its attributes to 15 similar past launches to set the first 90 days of inventory.",
        "customer_tip": "Show the NPI Demand Profiler (`npi_demand_profiler`) when a customer launches frequent seasonal or new products."
    },
    {
        "term": "Price Elasticity & Cannibalization",
        "full": "Promo Lift vs. Stealing Sales From Your Own Products",
        "cat": "planning",
        "top15": False,
        "hook": "Does a 20% discount actually bring new profit, or just steal sales from your other items?",
        "plain": "Elasticity measures how much sales jump when you cut the price. Cannibalization is when putting your 12-pack on sale causes shoppers to stop buying your higher-margin 6-pack — so you worked harder but made less money!",
        "example": "A 25% discount boosts volume by +40%, but half of that came from cannibalizing sister SKUs and pulling forward next week's regular sales.",
        "customer_tip": "Show the Promo Lift & Elasticity Simulator (`promo_lift_simulator`) or Dynamic Markdown Agent (`dynamic_markdown_agent`)."
    },

    # --- 02 · SOURCING & PROCUREMENT ---
    {
        "term": "BOM",
        "full": "Bill of Materials (The Product Recipe)",
        "cat": "sourcing",
        "top15": True,
        "hook": "The complete recipe list of every raw material, sub-part, screw, and box needed to make 1 unit.",
        "plain": "Just like baking a cake requires flour, eggs, sugar, and a box, manufacturing any product requires a Bill of Materials (BOM) listing exact quantities of every component.",
        "example": "To build 1 smart thermostat, the BOM lists 1 LCD screen, 1 PCB board, 1temperature sensor, 4 screws, and 1 retail carton.",
        "customer_tip": "Say: 'Our Should-Cost and Tier-N Risk agents explode your multi-level BOM to price every raw material and track every sub-supplier.'"
    },
    {
        "term": "RFQ / RFP",
        "full": "Request for Quotation / Request for Proposal",
        "cat": "sourcing",
        "top15": False,
        "hook": "Inviting multiple suppliers to bid their best price and lead time to supply a part.",
        "plain": "When a company needs 100,000 aluminum cans or microchips, the buyer sends out an RFQ to 5 approved suppliers asking for their price breakdown, delivery schedule, and payment terms.",
        "example": "Supplier A quotes $1.45/unit, but our Should-Cost Agent calculates that aluminum + labor + energy should only cost $1.28/unit — giving the buyer factual leverage to negotiate.",
        "customer_tip": "Show the RFQ Should-Cost Agent (`rfq_should_cost_agent`) to any VP of Procurement."
    },
    {
        "term": "Should-Cost Model",
        "full": "Bottom-Up Raw Material + Labor + Margin Cost Calculation",
        "cat": "sourcing",
        "top15": False,
        "hook": "Calculating what a part SHOULD cost to manufacture based on raw commodity prices.",
        "plain": "Instead of blindly accepting whatever price a supplier quotes, a Should-Cost model adds up the exact weight of steel/resin/copper (from global commodity exchanges) + machine time + local wages + a fair 8% supplier profit.",
        "example": "Resin prices dropped 14% on the commodity index, but your plastic bottle supplier kept their price flat. The Should-Cost Agent flags the 14% overcharge automatically.",
        "customer_tip": "Pair `rfq_should_cost_agent` with `commodity_index_advisor` to show how AI protects gross margins."
    },
    {
        "term": "Tier-1, Tier-2 & Tier-N Suppliers",
        "full": "Direct Suppliers vs. Your Supplier's Suppliers",
        "cat": "sourcing",
        "top15": True,
        "hook": "Tier-1 sells directly to you; Tier-2 sells to Tier-1; Tier-3 mines the raw materials.",
        "plain": "Most companies only know their Tier-1 suppliers (the company they send Purchase Orders to). Yet 80% of supply disruptions happen at Tier-2 or Tier-3 (a chemical plant or wafer foundry upstream that supplies three of your Tier-1 vendors!).",
        "example": "You buy brake modules from Bosch (Tier-1), who buys chips from NXP (Tier-2), who fabricates wafers at TSMC in Taiwan (Tier-3).",
        "customer_tip": "Say: 'Our Tier-N Risk Sentinel maps your supply network 4 tiers deep in a graph database so you spot hidden single-point-of-failure bottlenecks before a crisis hits.'"
    },
    {
        "term": "PO & GRN",
        "full": "Purchase Order & Goods Receipt Note",
        "cat": "sourcing",
        "top15": False,
        "hook": "PO = the official order you send a vendor; GRN = the warehouse receipt proving the boxes arrived.",
        "plain": "When you buy from a supplier, your ERP sends a Purchase Order (PO) stating quantity and price. When the supplier's truck arrives at your receiving dock, your warehouse clerk scans the boxes and creates a Goods Receipt Note (GRN).",
        "example": "PO #450019 ordered 1,000 motors at $50 each. The warehouse dock scans 960 motors and logs GRN #8812 for 960 units.",
        "customer_tip": "Understanding PO + GRN + Invoice is the foundation of the '3-Way Match'!"
    },
    {
        "term": "3-Way Match",
        "full": "Matching Purchase Order (PO) vs. Goods Receipt (GRN) vs. Supplier Invoice",
        "cat": "sourcing",
        "top15": True,
        "hook": "Checking that what you ordered = what arrived at the dock = what the vendor billed you for!",
        "plain": "Before Accounts Payable pays a supplier's bill, they check three documents: (1) The PO (did we order 1,000 units at $10?), (2) The GRN (did 1,000 units actually arrive?), and (3) The Invoice (is the bill for 1,000 units at $10?). If all 3 match, pay it!",
        "example": "We ordered 1,000 units at $10 ($10,000), only 950 arrived, yet the vendor billed $10,500. Our 3-Way Match Dispute Agent blocks overpayment and issues a $1,000 debit memo automatically.",
        "customer_tip": "Show the Three-Way Match Dispute Agent (`three_way_match_dispute`) to Procurement and Finance leaders."
    },
    {
        "term": "Lead Time & MOQ",
        "full": "Supplier Delivery Time & Minimum Order Quantity",
        "cat": "sourcing",
        "top15": False,
        "hook": "Lead Time = how many days from ordering until delivery; MOQ = the smallest batch a supplier will sell.",
        "plain": "If a supplier's Lead Time is 45 days, you must order 45 days before you need the parts. If their MOQ is 10,000 units, you cannot order 2,000 units — even if you only need 2,000!",
        "example": "Your ERP still says a supplier's lead time is 14 days, but in reality they've been taking 26 days for the last 6 months — causing constant stockouts! Our Master Data Lead-Time Steward fixes those outdated ERP numbers.",
        "customer_tip": "Mention that outdated Lead Times in SAP/Oracle are one of the biggest hidden causes of stockouts (`master_data_leadtime_steward`)."
    },
    {
        "term": "NCR & COPQ",
        "full": "Non-Conformance Report & Cost of Poor Quality",
        "cat": "sourcing",
        "top15": False,
        "hook": "NCR = official defect ticket when parts fail inspection; COPQ = total money lost from bad quality.",
        "plain": "When incoming supplier parts or factory batches fail quality specs (wrong dimensions, contamination), QA raises an NCR to quarantine the lot and charge the supplier back for the Cost of Poor Quality (scrap, rework, and line stoppage).",
        "example": "A batch of glass vials has micro-cracks. Our Supplier Quality Sentinel places an automatic QM quarantine lock on the lot, issues an NCR, and debits the vendor for $42,000 in COPQ.",
        "customer_tip": "Show `supplier_quality_sentinel` (`QualiShield`) for incoming quality and `scrap_defect_root_cause_agent` for plant quality."
    },
    {
        "term": "MSA & Force Majeure",
        "full": "Master Services Agreement & 'Act of God' Contract Clause",
        "cat": "sourcing",
        "top15": False,
        "hook": "The master legal contract with a supplier, and the clause covering hurricanes, wars, or port closures.",
        "plain": "An MSA sets legal rules (penalties, payment terms, price caps) with a supplier. A Force Majeure clause defines when a supplier is excused from late delivery due to natural disasters.",
        "example": "A supplier tries to raise prices +18% claiming Force Majeure, but our Contract Intelligence Agent (`tariff_esg_agent`) reads the PDF contract and proves their price increase is capped at 4%.",
        "customer_tip": "Show how our agent reads unstructured PDF contracts and cross-checks live ERP purchase orders."
    },

    # --- 03 · MANUFACTURING & FACTORY OPERATIONS ---
    {
        "term": "MTS vs. MTO",
        "full": "Make-to-Stock vs. Make-to-Order",
        "cat": "manufacturing",
        "top15": True,
        "hook": "MTS = build products ahead of time based on a forecast; MTO = wait until a customer orders to build.",
        "plain": "Coca-Cola and toothpaste are Make-to-Stock (MTS): factories produce millions of units ahead of time so they sit ready on store shelves. Custom industrial machinery or a personalized Dell server is Make-to-Order (MTO): built only after the customer places a specific order.",
        "example": "In MTS, forecast accuracy (WAPE) is king. In MTO, raw component availability and fast factory scheduling are king.",
        "customer_tip": "Always ask a new customer: 'What percentage of your business is Make-to-Stock (MTS) versus Make-to-Order (MTO)?' — they will love that question!"
    },
    {
        "term": "OEE",
        "full": "Overall Equipment Effectiveness (Availability × Performance × Quality)",
        "cat": "manufacturing",
        "top15": True,
        "hook": "The ultimate 0–100% score of how productively a factory machine or production line is running.",
        "plain": "OEE multiplies three things: (1) Availability (was the machine running or broken down?), (2) Performance (did it run at full speed or slow down?), and (3) Quality (what % of units came out defect-free?). World-class OEE is 85%+.",
        "example": "If a bottling line runs 90% of the shift (Availability), at 90% of top speed (Performance), with 99% good bottles (Quality), its OEE = 0.90 × 0.90 × 0.99 = 80.2%.",
        "customer_tip": "Say: 'Every +1% gain in OEE is free factory capacity without buying new machines. Our Predictive OEE Sentinel prevents unplanned breakdowns before they happen.'"
    },
    {
        "term": "MPS & Finite Scheduling",
        "full": "Master Production Schedule & Finite Capacity Scheduling",
        "cat": "manufacturing",
        "top15": False,
        "hook": "Deciding the exact hour-by-hour sequence of which products run on which factory line.",
        "plain": "Legacy ERPs often assume 'infinite capacity' (pretending a factory can make everything at once). A Finite Scheduler respects real-world limits: machine speeds, worker shifts, molds/tooling, and cleaning time between flavors/colors.",
        "example": "Running White paint -> Light Blue -> Dark Blue -> Black minimizes wash-down changeover time compared to switching from Black back to White!",
        "customer_tip": "Show the Line Schedule Optimizer (`line_schedule_optimizer` / `finite_production_scheduler`) to Plant Managers."
    },
    {
        "term": "Changeover / Setup Time",
        "full": "Line Wash-Down, Tooling Swap & Calibration Time Between Products",
        "cat": "manufacturing",
        "top15": False,
        "hook": "The dead time when a factory line is stopped to clean tanks or swap molds for the next SKU.",
        "plain": "Every time a factory switches from making Product A (say, Peanut Butter cookies) to Product B (Allergen-Free Vanilla cookies), the line must stop for 3 hours of deep sanitation and tooling setup. Grouping similar runs together saves hundreds of hours.",
        "example": "Our Finite Scheduler sequences production batches to cut changeover downtime by 22% while still meeting every customer delivery date.",
        "customer_tip": "Pair `line_schedule_optimizer` with `sanitation_health_agent` (CIP / Clean-in-Place optimization)."
    },
    {
        "term": "MES, PLC & SCADA",
        "full": "Manufacturing Execution System, Programmable Logic Controller & Shop-Floor Sensors",
        "cat": "manufacturing",
        "top15": False,
        "hook": "The software (MES) and hardware controllers (PLC/SCADA) running the physical machines in a plant.",
        "plain": "ERP (like SAP) sits in the corporate office managing orders and finance. MES sits on the factory floor tracking work orders on each machine. PLCs are the rugged mini-computers wired directly to motors, valves, vibration sensors, and pneumatic diverter gates.",
        "example": "When our VisionInspect agent spots a cracked bottle seal on a 60fps camera, it signals the PLC to fire an air-jet diverter in 12 milliseconds and logs the reject in the MES.",
        "customer_tip": "Say: 'Our agents bridge the gap between shop-floor OT (PLCs/MES) and corporate IT (ERP/BigQuery).'"
    },
    {
        "term": "Scrap, Yield & First-Pass Yield (FPY)",
        "full": "Percentage of Raw Material That Becomes Good Sellable Product on the First Try",
        "cat": "manufacturing",
        "top15": False,
        "hook": "Yield = good output %; Scrap = wasted material thrown in the bin.",
        "plain": "If you put 1,000 kg of ingredients into a line and get 940 kg of good product and 60 kg of ruined scrap, your Yield is 94% and Scrap is 6%. In semiconductors or pharma, a 2% yield drop can cost $10M+ a month.",
        "example": "Our YieldMax agent correlates oven humidity and spindle torque to discover why batch scrap spiked, adjusting machine setpoints to recover +2.8% yield.",
        "customer_tip": "Show `inline_yield_guardian` and `scrap_defect_root_cause_agent`."
    },
    {
        "term": "eBHR & 21 CFR Part 11",
        "full": "Electronic Batch History Record & FDA Digital Compliance Rule",
        "cat": "manufacturing",
        "top15": False,
        "hook": "The legal birth certificate of a food, beverage, chemical, or pharma production batch.",
        "plain": "Before a batch of medicine, baby formula, or food can ship out of the warehouse, Quality Assurance must review its Batch Record (every ingredient lot, temperature log, lab test, and digital signature). Manually reviewing 200-page binders takes 5–10 days!",
        "example": "Our Batch Record Auditor (`batch_record_auditor`) reviews the entire eBHR by exception in 90 seconds, releasing quarantined inventory 4 days faster.",
        "customer_tip": "In Pharma, Biotech, Food & Beverage, or Chemicals, 'Release-by-Exception on eBHRs' is a massive ROI winner."
    },
    {
        "term": "Co-Packer / Toller / CM",
        "full": "Contract Manufacturer or External Packaging Partner",
        "cat": "manufacturing",
        "top15": False,
        "hook": "An outside factory you pay to manufacture or package your products when your own plants are full.",
        "plain": "Many brands don't build everything in their own factories — they hire Co-Packers (Contract Manufacturers) to blend, bottle, or assemble promotional packs. Balancing volume and raw materials across external co-packers is notoriously messy.",
        "example": "Our Co-Packer Allocation Agent (`copacker_allocation_agent`) optimizes which orders go to internal plants vs. external co-packers based on tolling fees, capacity, and freight.",
        "customer_tip": "Show `copacker_allocation_agent` to any CPG, Food/Beverage, or Electronics company."
    },

    # --- 04 · WAREHOUSE & INVENTORY (MEIO, WMS, ATP) ---
    {
        "term": "Safety Stock & ROP",
        "full": "Buffer Inventory for Uncertainty & Reorder Point Trigger",
        "cat": "inventory",
        "top15": True,
        "hook": "Safety Stock = your emergency cushion; ROP = the stock level that triggers a new replenishment order.",
        "plain": "If you use 100 units a day and your supplier takes 5 days to deliver, you need 500 units just to cover normal delivery time. Safety Stock is the extra 150 units you keep in case demand spikes or the supplier's truck is late. Your Reorder Point (ROP) is 500 + 150 = 650 units!",
        "example": "When warehouse stock drops to 650 units (the ROP), the system automatically orders a new batch so you don't hit zero before the truck arrives.",
        "customer_tip": "Say: 'Most companies set Safety Stock with static rules-of-thumb like 30 days of supply. Our MEIO Agent dynamically recalculates Safety Stock daily based on real forecast error and supplier lead-time risk.'"
    },
    {
        "term": "MEIO",
        "full": "Multi-Echelon Inventory Optimization",
        "cat": "inventory",
        "top15": True,
        "hook": "Optimizing inventory across the WHOLE network together (Factory → Regional DC → Local DC → Store).",
        "plain": "'Echelon' just means a layer or tier in your warehouse network. If the Regional Warehouse holds a big safety buffer AND the Local Warehouse holds a big safety buffer AND the Store holds a big buffer, you are triple-insuring the same risk and wasting millions in cash! MEIO optimizes all layers together.",
        "example": "By pooling safety stock upstream at the Regional DC (RDC) and fast-shipping to Local DCs (FDCs), our MEIO agent cuts total inventory cash by 18% while raising service levels to 99%.",
        "customer_tip": "Show `meio_safety_stock_agent` (`EchelonFlow`) — it's one of the highest working-capital ROI agents in the catalog."
    },
    {
        "term": "RDC vs. FDC",
        "full": "Regional Distribution Center vs. Forward / Local Distribution Center",
        "cat": "inventory",
        "top15": False,
        "hook": "RDC = giant central hub warehouse; FDC = smaller local warehouse close to customers for fast delivery.",
        "plain": "Factories ship full trainloads or truckloads into a few giant Regional Distribution Centers (RDCs, e.g., Dallas or Chicago). From the RDC, stock is replenished into smaller Forward/Local DCs (FDCs) near major cities for same-day or next-day store delivery.",
        "example": "Holding slow-moving items at the central RDC and fast-moving items at the local FDC balances low inventory cost with fast delivery.",
        "customer_tip": "Use RDC and FDC naturally when discussing warehouse networks!"
    },
    {
        "term": "ATP",
        "full": "Available-to-Promise (Real-Time Uncommitted Inventory)",
        "cat": "inventory",
        "top15": True,
        "hook": "How many units you actually have free to promise a new customer order right this second.",
        "plain": "Just because 1,000 units are physically sitting on a warehouse shelf doesn't mean you can sell them — 800 might already be reserved for existing customer orders! ATP = Physical On-Hand (1,000) minus Already Reserved (800) + Incoming Receipts = 200 Available-to-Promise.",
        "example": "When an e-commerce or B2B order arrives, our ATP Order Promising Agent (`atp_order_promising_agent`) checks real-time stock across all warehouses in under 50ms and protects VIP customer quotas.",
        "customer_tip": "Show `atp_order_promising_agent` (`PromiseGuard`) to Order Management and Fulfillment leaders."
    },
    {
        "term": "WMS",
        "full": "Warehouse Management System (e.g., SAP EWM, Manhattan Active)",
        "cat": "inventory",
        "top15": True,
        "hook": "The software that runs everything inside the four walls of a warehouse.",
        "plain": "Once a truck backs up to a warehouse door, the WMS takes over: it tells workers where to put pallets away (Putaway), which bin every item sits in (Slotting), what route pickers should walk with their barcode scanners (Wave Picking), and which dock door to load.",
        "example": "Our Warehouse Slotting and Wave Fulfillment agents plug into the WMS to put fast-selling items in the 'Golden Zone' (waist-high bins near the shipping doors) to cut picker walking time by 28%.",
        "customer_tip": "Know the trio: **ERP** (Finance & Orders), **WMS** (Inside the Warehouse), **TMS** (Trucks & Carriers Outside the Warehouse)."
    },
    {
        "term": "Slotting & Golden Zone",
        "full": "Assigning Each SKU to the Best Physical Rack/Bin Location in the Warehouse",
        "cat": "inventory",
        "top15": False,
        "hook": "Putting your fastest-selling items at waist height right near the shipping dock doors.",
        "plain": "Warehouse pickers spend 60% of their day just walking up and down aisles! 'Slotting' means organizing which SKU goes into which rack bin. The 'Golden Zone' is waist-to-shoulder height in the aisles closest to the outbound shipping docks — reserved for your highest-velocity items.",
        "example": "Before summer, our Warehouse Slotting Optimizer (`warehouse_slotting_agent`) moves sunscreen and sports drinks into Golden Zone bins so pickers walk 3 miles less per shift.",
        "customer_tip": "Also mention our Aisle-Aligned Pallet Agent (`aisle_aligned_pallet_agent`), which builds pallets sorted by the grocery store's aisle layout!"
    },
    {
        "term": "FEFO, FIFO & LIFO",
        "full": "First-Expired-First-Out, First-In-First-Out & Last-In-First-Out",
        "cat": "inventory",
        "top15": True,
        "hook": "FEFO = ship soonest expiry date first; FIFO = ship oldest arrival first; LIFO = load truck in reverse stop order!",
        "plain": "1. **FEFO** (Food/Pharma): Always ship the batch whose expiration date is closest so it doesn't expire in your warehouse. 2. **FIFO** (General goods): Ship the oldest boxes first. 3. **LIFO in Truck Loading**: Put Stop #1's pallets at the very back (tail) of the trailer so when the driver opens the door at Stop #1, their pallets are right there!",
        "example": "Our Short-Dated Stock Redistributor enforces FEFO across warehouses, while our 3D Load Consolidation Agent (`load_consolidation_agent`) enforces LIFO axle-weight packing in trailers.",
        "customer_tip": "Distinguishing FEFO (warehouse shelf-life) from LIFO (multi-stop truck loading) shows deep operational mastery."
    },
    {
        "term": "Cross-Docking",
        "full": "Unloading an Inbound Truck and Moving Boxes Directly Onto an Outbound Truck (Zero Storage!)",
        "cat": "inventory",
        "top15": False,
        "hook": "Boxes cross straight from the receiving dock to the shipping dock without ever being put away in racks.",
        "plain": "Putting pallets up into high-bay racks and picking them down later costs time and labor. In Cross-Docking, an inbound container arrives at Door #4, pallets are sorted on the floor, and loaded directly onto outbound store trucks at Doors #18–#22 within 2 hours!",
        "example": "Our Cross-Dock Flow Orchestrator (`crossdock_transfer_orchestrator`) matches late inbound trailers to waiting outbound store trucks in real time.",
        "customer_tip": "Retailers like Walmart and Home Depot love Cross-Docking because it slashes warehouse handling costs and speeds up flow."
    },
    {
        "term": "Dock-to-Stock & Wave Picking",
        "full": "Receiving Unload-to-Rack Speed & Batching Orders Into Synchronized Picking Waves",
        "cat": "inventory",
        "top15": False,
        "hook": "Dock-to-Stock = hours from truck arrival until inventory is sellable; Wave Picking = grouping orders to pick efficiently.",
        "plain": "If a truck arrives at 8 AM but boxes sit on the receiving floor un-scanned until 6 PM, your 'Dock-to-Stock' time is 10 hours (and the system thinks you're out of stock!). Wave Picking groups ratusan outbound orders together by carrier departure cutoff time so pickers clear the floor in synchronized waves.",
        "example": "Our Dock-to-Stock Accelerator (`dock_to_stock_agent`) and Wave Fulfillment Copilot (`wave_fulfillment_copilot`) eliminate receiving bottlenecks and missed carrier cutoffs.",
        "customer_tip": "Show these two agents to any Director of Distribution or Fulfillment Center GM."
    },
    {
        "term": "SLOB & Shrinkage / Phantom Inventory",
        "full": "Slow-Moving & Obsolete Stock vs. Missing / Ghost Inventory",
        "cat": "inventory",
        "top15": False,
        "hook": "SLOB = dead stock nobody is buying; Phantom Inventory = computer says 50 units on shelf, but shelf is actually empty!",
        "plain": "SLOB is inventory gathering dust in the warehouse tying up cash and space. Phantom Inventory (a form of Shrinkage/error) is when theft, damage, or mis-scans make the computer think a store has 50 units on the shelf when it actually has 0 — so the computer refuses to reorder!",
        "example": "Our SLOB Disposition Agent (`slob_disposition_agent`) liquidates or transfers dead stock early, while our CPFR Sync Agent spots Phantom Inventory from zero-scan anomalies.",
        "customer_tip": "Phantom Inventory costs retailers 3–4% of total sales every year!"
    },

    # --- 05 · LOGISTICS, FLEET & TRANSPORTATION ---
    {
        "term": "TMS",
        "full": "Transportation Management System (e.g., Blue Yonder, Oracle OTM, SAP TM)",
        "cat": "logistics",
        "top15": True,
        "hook": "The software that plans routes, selects trucking/ocean carriers, tenders loads, and tracks shipments.",
        "plain": "While WMS runs inside the warehouse, TMS runs everything moving between locations: choosing whether to ship by truck, rail, ocean, or air; tendering loads to trucking companies; optimizing multi-stop routes; and auditing freight bills.",
        "example": "Our FleetFlow Dispatch and Load Consolidation agents calculate optimal 3D loads and routes and push the manifest directly into the TMS.",
        "customer_tip": "Ask: 'Which TMS do you use today, and how do you handle dynamic rerouting or 3D trailer cube optimization?'"
    },
    {
        "term": "FTL vs. LTL",
        "full": "Full Truckload vs. Less-Than-Truckload Shipping",
        "cat": "logistics",
        "top15": True,
        "hook": "FTL = you rent the entire 53-foot semi-trailer; LTL = you only ship a few pallets and share the truck with others.",
        "plain": "Shipping LTL (paying per pallet to a carrier like FedEx Freight or XPO) is expensive per pound and goes through multiple hub terminals (higher damage risk). If you can combine (consolidate) several LTL orders going to the same region into one Full Truckload (FTL), you save 25–35% on freight!",
        "example": "Our 3D Load Consolidation Agent (`load_consolidation_agent`) combines 4 separate LTL shipments into 1 multi-stop FTL trailer at 94% cube utilization.",
        "customer_tip": "Converting LTL shipments into consolidated multi-stop FTLs is one of the fastest ways to save millions in transportation spend."
    },
    {
        "term": "Cube Utilization & Weigh-Out vs. Cube-Out",
        "full": "Percentage of Trailer Volume Filled vs. Hitting Legal Weight Limits",
        "cat": "logistics",
        "top15": False,
        "hook": "Cube-Out = trailer is 100% full by volume (e.g., potato chips); Weigh-Out = trailer hits 44,000 lb weight limit first (e.g., soda cans).",
        "plain": "A standard US 53-foot trailer can hold ~3,800 cubic feet of space AND up to ~44,000 lbs of cargo weight (80,000 lbs gross truck weight). Heavy goods (water, metal) hit the weight limit while the trailer is still half empty ('Weigh-Out'). Light goods (paper towels) fill the space first ('Cube-Out').",
        "example": "By co-loading heavy beverage pallets on the floor with light snack cartons on top, our 3D Load Consolidation Agent maximizes both weight and cube while keeping drive/tandem axle weights legal!",
        "customer_tip": "Show the interactive 3D LIFO Trailer Bay simulator (`load_consolidation_agent`) — customers love seeing this visual!"
    },
    {
        "term": "VRP / CVRPTW",
        "full": "Capacitated Vehicle Routing Problem with Time Windows",
        "cat": "logistics",
        "top15": False,
        "hook": "The math puzzle of routing 50 trucks across 300 customer stops while hitting every delivery appointment window.",
        "plain": "Every store has a strict delivery window (e.g., 'Deliver between 6:00 AM and 8:00 AM'), every truck has a weight/cube limit, every driver has legal driving-hour limits (HOS), and traffic changes every minute. CVRPTW is the mathematical optimization solver (like Google OR-Tools) that finds the lowest-cost route for all trucks simultaneously.",
        "example": "Our FleetFlow Dispatch Optimizer (`fleetflow_dispatch`) solves CVRPTW across traffic, dock windows, and driver hours to cut empty deadhead miles by 16%.",
        "customer_tip": "Mention that LLMs alone cannot solve math routing puzzles — our agents combine Gemini with a dedicated Mathematical Optimization Solver (MILP / CP-SAT)."
    },
    {
        "term": "3PL & 4PL",
        "full": "Third-Party Logistics Provider & Fourth-Party Lead Logistics Provider",
        "cat": "logistics",
        "top15": False,
        "hook": "Outsourced companies that run your warehouses and trucks for you (like DHL, Kuehne+Nagel, Ryder, FM Logistic).",
        "plain": "Instead of owning your own trucks and warehouses, you hire a 3PL to store and ship your goods. A 4PL manages multiple 3PLs across the globe on your behalf.",
        "example": "Our agents connect via EDI and MCP APIs directly to 3PL partners to track inventory, audit accessorial fees, and dispatch loads.",
        "customer_tip": "Even if a customer outsources warehousing/trucking to 3PLs, they still pay the freight bills and suffer from stockouts — so they still need our Control Tower and Audit agents!"
    },
    {
        "term": "Drayage, Demurrage & Detention",
        "full": "Short-Haul Port Trucking & Expensive Late Fines for Holding Containers or Trailers",
        "cat": "logistics",
        "top15": True,
        "hook": "Drayage = moving a container from port to warehouse; Demurrage & Detention = $150–$500/day late fees when containers sit waiting!",
        "plain": "1. **Drayage**: The short truck trip pulling an ocean container from a seaport to a nearby rail yard or warehouse. 2. **Demurrage**: Penalty charged by the ocean line when your full container sits inside the port terminal past your free days. 3. **Detention**: Penalty charged by a carrier when you keep their truck/container waiting too long at your warehouse yard (>2 hours).",
        "example": "Our Ocean Port Drayage Orchestrator (`port_drayage_orchestrator`) and Yard Dock Sequencer (`yard_dock_sequencer`) prioritize containers approaching free-time expiry, slashing demurrage & detention fines by 65%+.",
        "customer_tip": "CFOs hate Demurrage and Detention fees because they are 100% pure waste — easy ROI pitch!"
    },
    {
        "term": "BOL, ASN (EDI 856) & ePOD",
        "full": "Bill of Lading, Advance Shipping Notice & Electronic Proof of Delivery",
        "cat": "logistics",
        "top15": False,
        "hook": "BOL = legal shipping ticket on the truck; ASN = digital heads-up sent before arrival; ePOD = signed delivery receipt.",
        "plain": "1. **BOL**: The legal contract between shipper and carrier listing what's on the truck. 2. **ASN (EDI 856)**: Electronic message sent to the receiving warehouse ahead of time listing exact pallet barcodes on the incoming truck. 3. **ePOD**: Digital signature, GPS timestamp, and photo proving the load was delivered intact.",
        "example": "When Walmart claims a truck arrived late, our OTIF Penalty Shield (`otif_penalty_shield`) pulls the ASN, GPS geofence ping, and signed ePOD to dispute false chargebacks automatically.",
        "customer_tip": "Also mention **EDI 204** (Load Tender to a carrier) and **EDI 214** (Carrier Shipment Status update)."
    },
    {
        "term": "ELD & HOS",
        "full": "Electronic Logging Device & Driver Hours of Service Regulations",
        "cat": "logistics",
        "top15": False,
        "hook": "Federal law limiting truck drivers to 11 hours of driving per day, tracked by an in-cab digital logger (ELD).",
        "plain": "In the US (FMCSA) and EU, commercial truck drivers are legally required to stop and rest for 10 hours after driving 11 hours. An ELD wired to the truck engine tracks every minute. If a route plan ignores a driver's remaining HOS clock, the truck will legally have to park 50 miles short of the customer!",
        "example": "Our FleetFlow and Intermodal agents check live ELD remaining hours before assigning a load so routes are 100% legally executable.",
        "customer_tip": "Mentioning 'ELD Hours-of-Service compliance' during routing discussions shows real-world logistics credibility."
    },
    {
        "term": "OS&D & Freight Bill Accessorial Audit",
        "full": "Over, Short & Damaged Cargo Claims & Auditing Carrier Extra Fees",
        "cat": "logistics",
        "top15": False,
        "hook": "OS&D = filing a claim when pallets arrive crushed or missing; Accessorial Audit = catching bogus carrier fuel/waiting charges.",
        "plain": "Up to 8% of carrier freight invoices contain errors: wrong rate tables, inflated fuel surcharges, or unverified detention ('accessorial') fees. And when cargo arrives crushed or short (OS&D), shippers often lose money because they miss the strict 9-month legal filing window.",
        "example": "Our Freight Bill Audit Agent (`freight_bill_audit_agent`) checks 100% of carrier EDI 210 invoices against GPS dwell logs, while our OS&D Claims Agent (`osd_freight_claims_agent`) compiles dock photos and files recovery claims automatically.",
        "customer_tip": "Freight Bill Audit typically recovers 2% to 4% of a company's total annual transportation spend!"
    },
    {
        "term": "Cold Chain & Excursion",
        "full": "Temperature-Controlled Supply Chain & Out-of-Range Temperature Spike",
        "cat": "logistics",
        "top15": False,
        "hook": "Keeping food, vaccines, and biologics chilled/frozen from factory to store — and catching any warm-up ('excursion').",
        "plain": "Vaccines (+2°C to +8°C) and frozen foods (-18°C) have IoT temperature loggers inside the pallets. An 'Excursion' is when the temperature goes outside the safe band (e.g., rises to +12°C for 45 minutes while sitting on a hot tarmac). Mean Kinetic Temperature (MKT) math calculates whether the product is still safe or must be quarantined.",
        "example": "Our Cold-Chain Excursion Auditor (`cold_chain_auditor`) calculates MKT in real time and locks compromised lots in the WMS before they reach patients or shoppers.",
        "customer_tip": "Essential for Grocery, Food & Beverage, Pharma, and Healthcare customers."
    },

    # --- 06 · RETURNS, CONTROL TOWER, FINANCE & SUSTAINABILITY ---
    {
        "term": "OTIF",
        "full": "On-Time In-Full (The #1 Customer Service Metric in Supply Chain)",
        "cat": "governance",
        "top15": True,
        "hook": "Did the shipment arrive ON TIME (within the appointment window) AND IN FULL (100% of ordered cases)?",
        "plain": "Big retailers (Walmart, Target, Kroger, Amazon) grade every supplier on OTIF. If Walmart orders 1,000 cases for Tuesday between 8 AM–10 AM, and you deliver 980 cases on time (98% fill) OR 1,000 cases at 2 PM (late), that order is 0% OTIF — and the retailer deducts a 3% penalty ('chargeback') straight off your invoice!",
        "example": "Our OTIF Penalty Shield (`otif_penalty_shield`) predicts orders at risk of missing OTIF 48 hours early to expedite them, and builds evidence dossiers to dispute unfair retailer fines.",
        "customer_tip": "Ask any Consumer Goods or Retail supplier: 'How much are you losing annually in retailer OTIF chargebacks?' — it's almost always millions of dollars."
    },
    {
        "term": "RMA & Reverse Logistics",
        "full": "Return Merchandise Authorization & Moving Returned Goods Backward",
        "cat": "governance",
        "top15": True,
        "hook": "RMA = the approval ticket for a customer return; Reverse Logistics = inspecting, refurbishing, or recycling returned items.",
        "plain": "Supply chains are designed to push millions of boxes forward to customers. When 10–20% of e-commerce or retail goods get returned ('Reverse Logistics'), warehouses get clogged! Each returned item needs an RMA ticket and a smart decision: Restock as Grade-A, Refurbish, Liquidate, or Recycle.",
        "example": "What if a customer returns a $12 toaster that costs $14 in UPS shipping + warehouse labor to process? Our Keep-It vs. Return Routing Advisor (`keep_it_routing_advisor`) refunds the customer and tells them to keep/donate it, saving $2 net loss per return!",
        "customer_tip": "Show our trio of Returns agents: `returns_triage_agent`, `keep_it_routing_advisor`, and `return_fraud_sentinel`."
    },
    {
        "term": "Working Capital & CCC",
        "full": "Cash Conversion Cycle (DIO + DSO − DPO)",
        "cat": "governance",
        "top15": True,
        "hook": "How many days your company's cash is trapped inside inventory and unpaid customer invoices.",
        "plain": "Every CFO watches the Cash Conversion Cycle (CCC): **DIO** (Days Inventory Outstanding — how many days stock sits in your warehouse before selling) + **DSO** (Days Sales Outstanding — how many days customers take to pay you) minus **DPO** (Days Payable Outstanding — how many days you take to pay your suppliers). Lower CCC = more free cash in the bank!",
        "example": "Cutting DIO by 7 days across a $2B supply chain unlocks over $38 Million in free Working Capital cash without borrowing a dime from the bank.",
        "customer_tip": "Show the Working Capital Cash Bridge (`working_capital_cash_bridge`) whenever a CFO or CSCO is in the room."
    },
    {
        "term": "Scope 1, Scope 2 & Scope 3 Emissions",
        "full": "Direct Carbon vs. Electricity Carbon vs. Full Supply Chain & Supplier Carbon",
        "cat": "governance",
        "top15": False,
        "hook": "Scope 1 = your own trucks/boilers; Scope 2 = electricity you buy; Scope 3 = your suppliers & 3PL carriers (85% of total carbon!).",
        "plain": "1. **Scope 1**: Exhaust from vehicles and furnaces your company owns. 2. **Scope 2**: Carbon from generating the electricity your offices/plants buy. 3. **Scope 3**: Carbon emitted by your Tier-1/2/3 suppliers making raw materials AND third-party ships/planes/trucks moving your freight. In supply chain, Scope 3 is 80–90% of a company's total footprint!",
        "example": "Our Scope-3 Carbon Ledger (`carbon_scope3_ledger`) calculates exact shipment-level CO2e (ISO 14083) and recommends shifting non-urgent air freight to ocean/rail.",
        "customer_tip": "Show `carbon_scope3_ledger`, `sustainable_packaging_agent`, and `food_waste_esg_copilot` for ESG & Sustainability goals."
    },
    {
        "term": "CBAM & EUDR",
        "full": "EU Carbon Border Adjustment Mechanism & EU Deforestation Regulation",
        "cat": "governance",
        "top15": False,
        "hook": "Strict European laws that tax high-carbon imports (CBAM) and ban crops from deforested land (EUDR).",
        "plain": "**CBAM**: When importing steel, aluminum, cement, or fertilizers into Europe, importers must report the exact embedded carbon from the factory and pay a carbon border tax. **EUDR**: Coffee, cocoa, palm oil, rubber, timber, and soy cannot enter the EU without satellite GPS proof that the farm wasn't deforested.",
        "example": "Our Scope-3 & CBAM Ledger (`carbon_scope3_ledger`) generates audit-ready CBAM certificates and verifies Sentinel-2 satellite farm coordinates.",
        "customer_tip": "Any company exporting into Europe MUST comply with CBAM and EUDR or face customs holds and heavy fines."
    },
    {
        "term": "RTI",
        "full": "Returnable Transport Items (CHEP Pallets, Plastic Totes, Kegs & Racks)",
        "cat": "governance",
        "top15": False,
        "hook": "Reusable plastic crates, metal racks, beer kegs, and wooden pallets that must come back from customers!",
        "plain": "Instead of throwing away cardboard boxes, companies ship goods on reusable CHEP pallets, folding plastic totes, or steel automotive racks (RTIs) worth $25 to $400 each. Problem: customers forget to return them, and the manufacturer spends millions buying replacements!",
        "example": "Our RTI Balance Reconciler (`rti_balance_reconciler`) tracks pallet/tote balances at every distributor, schedules backhaul pickups on empty returning trucks, and bills for unreturned assets.",
        "customer_tip": "Beverage, Dairy, Bakery, Grocery, and Automotive companies lose millions a year in missing RTIs."
    },
    {
        "term": "Control Tower & Digital Twin",
        "full": "End-to-End Real-Time Supply Chain Visibility & Virtual Simulation Mirror",
        "cat": "governance",
        "top15": True,
        "hook": "Digital Twin = a live virtual replica of all your plants, warehouses, and trucks; Control Tower = the AI nerve center watching it 24/7.",
        "plain": "A **Digital Twin** pulls live data from ERP, WMS, TMS, suppliers, and GPS into one unified database (like BigQuery) so you have a virtual mirror of your physical supply chain. A **Control Tower** sits on top of that Digital Twin: instead of just showing red blinking dots on a dashboard, an **Agentic Control Tower** simulates solutions and executes the fix!",
        "example": "When Typhoon Kong-rey threatens Taiwan ports, our Disruption War-Room Orchestrator (`disruption_war_room_orchestrator`) identifies $14.2M in orders at risk and reroutes allocations in minutes.",
        "customer_tip": "Say: 'Traditional Control Towers just give you more red alerts to stare at. Our Agentic Control Tower gives you 3 ranked recovery plans and executes the winner in 1 click.'"
    },
    {
        "term": "ERP vs. WMS vs. TMS vs. MES",
        "full": "The Big 4 Enterprise Software Systems in Supply Chain",
        "cat": "governance",
        "top15": True,
        "hook": "ERP = Finance & Orders; MES = Factory Floor; WMS = Inside the Warehouse; TMS = Trucks & Ships Outside.",
        "plain": "Think of a company's software like a relay race: 1. **ERP** (SAP S/4HANA, Oracle) takes the customer order, buys materials, and keeps the financial books. 2. **MES** (Siemens, Rockwell) runs the factory machines making the product. 3. **WMS** (Manhattan, SAP EWM) stores and picks the boxes inside the warehouse. 4. **TMS** (Blue Yonder, Oracle OTM) books the trucks and ships to deliver the boxes.",
        "example": "The #1 problem in supply chain is that ERP, MES, WMS, and TMS don't talk to each other intelligently — humans have to copy-paste spreadsheets between them! Our 60 AI Agents connect all 4.",
        "customer_tip": "Memorize this 4-system relay race! It instantly clarifies where every single one of our 60 AI agents plugs in."
    },
]

# =============================================================================
# 2. CUSTOMER CONVERSATION DECODER (20 REAL-WORLD CUSTOMER COMPLAINTS)
# =============================================================================
CUSTOMER_DECODER = [
    {
        "complaint": "“Our forecast accuracy is terrible — we're always out of stock on hot items and drowning in dead inventory on slow items.”",
        "meaning": "Their WAPE (forecast error) is high because they rely on lagging monthly ERP history instead of daily POS store scans and weather, and sales reps manually inflate forecasts (negative FVA).",
        "agents": "Demand Sensing Agent (`demand_sensing_agent`), Collaborative CPFR Sync (`cpfr_sync_agent`), SLOB Disposition Agent (`slob_disposition_agent`)",
        "question": "“Are you currently pulling daily retailer POS scans and weather signals into your forecast, and do you measure whether manual sales overrides add or destroy Forecast Value (FVA)?”"
    },
    {
        "complaint": "“Our monthly S&OP meeting takes 3 weeks of spreadsheet prep, and by the time we agree on a plan, it's already outdated.”",
        "meaning": "Sales, Finance, and Operations spend weeks emailing Excel files back and forth and cannot run live 'what-if' trade-off simulations when capacity or demand changes.",
        "agents": "S&OP Scenario Weaver (`sop_scenario_weaver`), CSCO Control Tower Copilot (`csco_control_tower_copilot`)",
        "question": "“When a major demand shift or plant constraint hits mid-month, how many days does it take your team to simulate the margin vs. service trade-off?”"
    },
    {
        "complaint": "“Walmart and Target are killing us with OTIF chargeback penalties every month.”",
        "meaning": "Shipments are arriving late or short (failing On-Time In-Full), AND when the carrier actually arrived on time, the team lacks automated GPS/ePOD proof to dispute unfair retailer deductions.",
        "agents": "OTIF Penalty Shield (`otif_penalty_shield`), ATP Order Promising Agent (`atp_order_promising_agent`), Yard & Dock Sequencer (`yard_dock_sequencer`)",
        "question": "“What percentage of your OTIF deductions are preventable late shipments vs. unfair retailer deductions that you don't have the bandwidth to dispute with ePOD/GPS evidence?”"
    },
    {
        "complaint": "“We have way too much cash tied up in inventory, yet our service levels still aren't hitting 98%.”",
        "meaning": "Each warehouse sets static 'rules-of-thumb' safety stock in silos instead of optimizing buffers across the whole network (Multi-Echelon Inventory Optimization — MEIO).",
        "agents": "MEIO Safety Stock Agent (`meio_safety_stock_agent`), Working Capital Cash Bridge (`working_capital_cash_bridge`)",
        "question": "“Do you optimize safety stock across your Plant, Regional DCs, and Local DCs together using multi-echelon math, or does each site hold its own fixed days-of-supply buffer?”"
    },
    {
        "complaint": "“We got blindsided when a sub-supplier had a factory fire / port strike — we didn't even know our vendor bought components from them!”",
        "meaning": "They only track Tier-1 vendors in ERP and have zero visibility into Tier-2 and Tier-3 sub-suppliers sharing the same upstream components.",
        "agents": "Tier-N Risk Sentinel (`tier_n_risk_sentinel`), Disruption War-Room Orchestrator (`disruption_war_room_orchestrator`)",
        "question": "“How many tiers deep is your Bill of Materials mapped today, and how fast can you see which finished SKUs and customer orders are exposed when a Tier-2 facility goes down?”"
    },
    {
        "complaint": "“Suppliers keep demanding price increases, and our buyers don't know if the quote is fair or padded.”",
        "meaning": "Buyers lack bottom-up 'Should-Cost' models tied to live global commodity indices (resin, steel, aluminum, energy, labor) to push back on vendor quotes factually.",
        "agents": "RFQ Should-Cost Agent (`rfq_should_cost_agent`), Commodity Index Advisor (`commodity_index_advisor`), Contract & Tariff Agent (`tariff_esg_agent`)",
        "question": "“When a supplier quotes a price increase, do your buyers have an automated Should-Cost breakdown tied to live commodity indices before they negotiate?”"
    },
    {
        "complaint": "“Accounts Payable and Procurement spend half their week arguing over mismatched supplier invoices.”",
        "meaning": "Their 3-Way Match (Purchase Order vs. Dock Goods Receipt vs. Supplier Invoice) fails due to price/quantity variances, requiring manual email chasing.",
        "agents": "Three-Way Match Dispute Agent (`three_way_match_dispute`), Freight Bill Audit Agent (`freight_bill_audit_agent`)",
        "question": "“What percentage of your supplier and carrier invoices fail automated 3-Way Match today and require manual analyst intervention?”"
    },
    {
        "complaint": "“Unplanned machine breakdowns and long line changeovers are killing our factory OEE.”",
        "meaning": "Factories run reactive maintenance (fixing machines after they break) and schedule production sequences without minimizing wash-down/tooling setup time.",
        "agents": "Predictive OEE Maintenance Sentinel (`predictive_oee_sentinel`), Line Schedule Optimizer (`line_schedule_optimizer`), Sanitation CIP Agent (`sanitation_health_agent`)",
        "question": "“Are your maintenance work orders triggered predictively from spindle vibration/thermal telemetry during planned changeovers, or after a line stops?”"
    },
    {
        "complaint": "“Our trucks are leaving 30% empty, and freight costs are eating our margins alive.”",
        "meaning": "They ship too many expensive Less-Than-Truckload (LTL) pallets instead of consolidating orders into multi-stop Full Truckloads (FTL) with 3D LIFO axle-weight packing and dynamic routing.",
        "agents": "3D Load Consolidation Studio (`load_consolidation_agent`), FleetFlow Route & Dispatch Optimizer (`fleetflow_dispatch`), Multimodal Mode-Shift Agent (`multimodal_mode_shift_agent`)",
        "question": "“What is your average trailer cube utilization today, and how many LTL shipments could be consolidated into multi-stop FTLs?”"
    },
    {
        "complaint": "“We're paying a fortune in port demurrage and warehouse yard detention fees because trucks sit waiting for hours.”",
        "meaning": "Ocean containers sit past free days at port terminals, and trucks arrive at warehouse gates all at once without dynamic dock-door sequencing.",
        "agents": "Ocean Port Drayage Orchestrator (`port_drayage_orchestrator`), Yard & Dock Sequencer (`yard_dock_sequencer`)",
        "question": "“Do you prioritize container drayage and warehouse dock doors dynamically based on remaining free-time expiry and live truck GPS ETA?”"
    },
    {
        "complaint": "“E-commerce and retail returns are costing us more to ship back and inspect than the items are even worth!”",
        "meaning": "Every return is blindly shipped back to a warehouse even when return freight + labor exceeds the item's salvage value, and serial return fraud goes undetected.",
        "agents": "Keep-It vs. Return Routing Advisor (`keep_it_routing_advisor`), Returns Triage & Disposition Agent (`returns_triage_agent`), Return Fraud Sentinel (`reverse_rma_optimizer`)",
        "question": "“At the moment a customer initiates an RMA, do you calculate net recovery value (salvage minus return shipping + grading labor) to decide Keep-It vs. Return?”"
    },
    {
        "complaint": "“Finished goods sit in our warehouse for a week waiting for Quality Assurance to review 200-page paper batch records.”",
        "meaning": "QA manually checks every page of Electronic Batch History Records (eBHR) instead of using AI 'Release-by-Exception' to flag only parameter deviations.",
        "agents": "Batch Record Auditor (`batch_record_auditor`), Inline Yield & Vision Guardian (`inline_yield_guardian`)",
        "question": "“How many days of working capital are tied up in QA quarantine waiting for manual batch record review?”"
    },
]

# =============================================================================
# 3. 12 INTERACTIVE QUIZ QUESTIONS (TEST YOUR SUPPLY CHAIN MASTERY)
# =============================================================================
QUIZ_QUESTIONS = [
    {
        "q": "1. A VP of Supply Chain tells you: 'Our WAPE is 28%, and sales reps keep adding +15% optimism bias (Negative FVA).' What are they telling you?",
        "options": [
            "Their warehouse trucks are 28% empty and drivers are working 15% overtime.",
            "Their demand forecast error is 28% (high!), and when salespeople manually edit the computer's forecast, they actually make accuracy worse.",
            "Their factory machines are broken 28% of the time.",
        ],
        "correct": 1,
        "explain": "Correct! WAPE (Weighted Absolute Percentage Error) measures forecast error (lower is better). FVA (Forecast Value Added) measures whether human edits improved the forecast — Negative FVA means human overrides hurt accuracy! Show them the **Demand Sensing Agent** (`demand_sensing_agent`)."
    },
    {
        "q": "2. Walmart fines your customer $250,000 a month in 'OTIF Chargebacks.' What does OTIF mean?",
        "options": [
            "Over-Time In Factory — paying factory workers overtime.",
            "On-Time In-Full — delivering 100% of the ordered quantity within the exact scheduled delivery appointment window.",
            "Ocean Transit International Freight — customs duties on ocean ships.",
        ],
        "correct": 1,
        "explain": "Spot on! OTIF = On-Time In-Full. If an order arrives even 1 hour late or 5 cases short, retailers fine the supplier 3% of the invoice value. Show them the **OTIF Penalty Shield** (`otif_penalty_shield`) and **ATP Order Promising Agent** (`atp_order_promising_agent`)."
    },
    {
        "q": "3. What is the difference between ERP, WMS, TMS, and MES?",
        "options": [
            "They are four competing brands of accounting software.",
            "ERP manages corporate Finance & Orders; MES runs Factory Floor machines; WMS runs inside the Warehouse (bins/picking); TMS runs Trucks & Carriers outside.",
            "WMS is for ocean ships, TMS is for factory robots, and ERP is for truck drivers.",
        ],
        "correct": 1,
        "explain": "Exactly! Think of the 4-system relay race: **ERP** (Orders/Finance) -> **MES** (Factory Floor) -> **WMS** (Inside Warehouse) -> **TMS** (Trucks/Carriers Outside). Our 60 AI agents connect all four!"
    },
    {
        "q": "4. What is the 'Bullwhip Effect' in supply chain?",
        "options": [
            "When a small 5% change in customer buying at the store gets amplified by panic ordering into a massive 40%+ wave at the factory and raw material suppliers.",
            "When warehouse workers walk too fast in the aisles.",
            "When a truck driver brakes too hard on the highway.",
        ],
        "correct": 0,
        "explain": "Yes! Because each layer (Store -> Distributor -> Factory -> Supplier) adds its own panic buffer when it doesn't see real-time POS store scans, a tiny ripple turns into a giant wave. **Demand Sensing** and **CPFR Sync** eliminate the Bullwhip Effect."
    },
    {
        "q": "5. In Accounts Payable & Procurement, what is a '3-Way Match'?",
        "options": [
            "Comparing quotes from 3 different trucking companies.",
            "Verifying that the Purchase Order (what we ordered) = Goods Receipt Note (what actually arrived at the dock) = Supplier Invoice (what we were billed) before paying.",
            "Matching 3 shifts of factory workers.",
        ],
        "correct": 1,
        "explain": "Correct! PO vs. Goods Receipt (GRN) vs. Invoice = 3-Way Match. Our **Three-Way Match Dispute Agent** (`three_way_match_dispute`) automates this and issues debit memos for overcharges."
    },
    {
        "q": "6. A Plant Manager wants to improve 'OEE' from 71% to 82%. What are the 3 parts of OEE?",
        "options": [
            "Ocean, Express, and Economy shipping.",
            "Availability (Uptime %) × Performance (Speed %) × Quality (Good Yield %).",
            "Orders, Employees, and Electricity.",
        ],
        "correct": 1,
        "explain": "Right! OEE = Availability × Performance × Quality. Our **Predictive OEE Sentinel** (`predictive_oee_sentinel`), **Line Schedule Optimizer** (`line_schedule_optimizer`), and **Inline Yield Guardian** (`inline_yield_guardian`) boost all three!"
    },
    {
        "q": "7. Why do Pharma/Food warehouses use 'FEFO' while multi-stop delivery trucks use 'LIFO'?",
        "options": [
            "FEFO (First-Expired, First-Out) ships the soonest expiration date first so food/medicine doesn't spoil; LIFO (Last-In, First-Out) loads Stop #1's pallets last so they sit right at the back door of the truck!",
            "They mean the exact same thing.",
            "FEFO is for accounting only, and LIFO is for air cargo only.",
        ],
        "correct": 0,
        "explain": "Bravo! FEFO prevents shelf-life expiration in the warehouse (`short_dated_redistributor`), while LIFO prevents the truck driver from having to dig through Stop #3's pallets to reach Stop #1 (`load_consolidation_agent`)."
    },
    {
        "q": "8. What does 'MEIO' (Multi-Echelon Inventory Optimization) do that standard safety-stock rules cannot?",
        "options": [
            "It doubles inventory at every single store.",
            "It optimizes safety stock buffers across all tiers of the network together (Plant -> Regional DC -> Local DC -> Store) so you don't double-insure the same risk, unlocking 15–25% in working capital cash.",
            "It replaces barcode scanners with cameras.",
        ],
        "correct": 1,
        "explain": "Exactly! Instead of every warehouse hoarding its own buffer in isolation, **MEIO** (`meio_safety_stock_agent`) balances buffers across all tiers ('echelons') simultaneously."
    },
    {
        "q": "9. A Logistics Director complains about '$1.8M in Demurrage and Detention fees.' What caused those fees?",
        "options": [
            "Ocean containers sat inside the port past their free days (Demurrage), and trucks were held waiting at warehouse docks longer than 2 hours (Detention).",
            "Highway speeding tickets.",
            "Buying too much diesel fuel.",
        ],
        "correct": 0,
        "explain": "Correct! Demurrage (inside port) and Detention (holding carrier equipment at the yard/dock) are pure penalty waste. Show them **Ocean Port Drayage Orchestrator** (`port_drayage_orchestrator`) and **Yard & Dock Sequencer** (`yard_dock_sequencer`)."
    },
    {
        "q": "10. What is 'Demand Censorship'?",
        "options": [
            "When a government bans an advertisement.",
            "When a store shelf is empty (out of stock), so the cash register records '0 sales' — tricking a traditional ERP into thinking nobody wanted the product!",
            "When a customer deletes their shopping cart.",
        ],
        "correct": 1,
        "explain": "Spot on! If you don't 'uncensor' stockout days (impute the lost sales), your forecast will keep shrinking every time you run out of stock! Our **Demand Sensing Agent** fixes this automatically."
    },
    {
        "q": "11. Why does a customer care about 'Tier-2 and Tier-3 Suppliers' if they only buy from Tier-1?",
        "options": [
            "Because Tier-1 suppliers buy their critical raw materials/chips from Tier-2 and Tier-3 — if a single Tier-2 chemical plant goes down, three of your Tier-1 suppliers can't deliver to you!",
            "They don't care at all.",
            "Because Tier-3 suppliers deliver directly to retail stores.",
        ],
        "correct": 0,
        "explain": "Exactly! Hidden 'diamond dependencies' (where multiple Tier-1 vendors rely on the same Tier-2/3 sub-supplier) cause the biggest supply shocks. Show them **Tier-N Risk Sentinel** (`tier_n_risk_sentinel`)."
    },
    {
        "q": "12. A customer processes 50,000 e-commerce returns (RMAs) a month. How does our 'Keep-It vs. Return Routing Advisor' save them money?",
        "options": [
            "It blocks all customers from ever returning anything.",
            "Before printing a return label, it calculates whether return shipping + warehouse grading labor costs MORE than the item's resale value — if so, it refunds the customer and tells them to keep/donate the item instead of losing money shipping it back!",
            "It ships all returns by air freight.",
        ],
        "correct": 1,
        "explain": "100% right! On low-price or bulky damaged goods, paying $14 in return shipping + $6 warehouse labor to recover a $12 item loses $8 net. **Keep-It Routing Advisor** (`keep_it_routing_advisor`) stops unprofitable reverse freight."
    },
]


def build_academy_files() -> None:
    # 1. Build Markdown Companion Guide (SUPPLY_CHAIN_101_MASTER_GUIDE.md)
    md = [
        "# 🎓 Supply Chain 101 — Complete Plain-English Master Guide & Acronym Decoder",
        "",
        "> **Designed for Zero-to-Expert Learning**: This guide explains Supply Chain from the ground up in plain, everyday English — with **zero unexplained abbreviations**, concrete examples with numbers, and a complete **Customer Conversation Decoder**.",
        "> 💡 **Prefer Interactive Visual Learning & 3D Flashcards?** Open **[`supply_chain_101_interactive_academy.html`](supply_chain_101_interactive_academy.html)** in your browser!",
        "",
        "---",
        "",
        "## 🌍 1. What Is a Supply Chain? (In 60 Seconds)",
        "",
        "Every physical product you touch — a bottle of sports drink, an iPhone, a car, or a box of medicine — goes through a **6-stage relay race** before it reaches your hands:",
        "",
        "1. **⛏️ Raw Materials (Tier-2 & Tier-1 Suppliers)**: Farms, mines, chemical plants, and chip foundries create the raw ingredients, aluminum, plastic resin, and microchips.",
        "2. **🏭 The Factory (Make / Manufacturing)**: Raw materials are mixed, cooked, molded, assembled, inspected for quality, and packed onto pallets.",
        "3. **🏢 Regional Distribution Center (RDC)**: Giant central hub warehouses receive full trainloads/truckloads from factories and hold strategic buffer stock.",
        "4. **📦 Local Fulfillment Center (FDC)**: Smaller warehouses near major cities receive stock from RDCs so they can replenish nearby stores or ship e-commerce orders within 24 hours.",
        "5. **🚚 Multi-Modal Transportation (Move / Logistics)**: Ocean container ships, cargo airplanes, intermodal freight trains, and 53-foot semi-trucks move goods between every stage.",
        "6. **🛒 Store Shelf, Customer & Returns (Fulfill & Reverse)**: The product sits on a retail shelf (or arrives at a doorstep), gets scanned at the cash register (**POS — Point of Sale**), and if returned (**RMA**), travels backward to be refurbished or recycled.",
        "",
        "### The 3 Synchronized Flows Running Through Every Supply Chain",
        "- **📦 Flow 1: Physical Material Flow (Downstream ──▶)**: Raw materials → Work-in-Progress → Finished Goods moving toward the customer.",
        "- **📡 Flow 2: Demand & Information Signal Flow (◀── Upstream)**: Cash-register scans, orders, and forecasts traveling backward from the customer to tell warehouses and factories what to build next.",
        "- **💵 Flow 3: Cash & Working Capital Flow (◀──▶ Cyclic)**: Money collected from customers paying for goods, money paid out to suppliers/carriers, and **frozen cash** trapped in unsold warehouse inventory.",
        "",
        "---",
        "",
        "## 🃏 2. All 56 Supply Chain Abbreviations & Concepts Decoded (Plain English)",
        "",
    ]

    for idx, fc in enumerate(FLASHCARDS, 1):
        star = " ⭐ *(Must-Know Top 15)*" if fc["top15"] else ""
        md.extend([
            f"### {idx}. `{fc['term']}` — {fc['full']}{star}",
            f"- **1-Line Hook**: {fc['hook']}",
            f"- **In Plain English**: {fc['plain']}",
            f"- **Concrete Example**: {fc['example']}",
            f"- **Customer Meeting Tip**: {fc['customer_tip']}",
            "",
        ])

    md.extend([
        "---",
        "",
        "## 🗣️ 3. Customer Conversation Decoder (When the Customer Says X → What It Means → Which Agent to Demo)",
        "",
        "| When the Customer Complains About… | What It Means in Simple Words | Which AI Agents to Show | Smart Question to Ask Them |",
        "|:---|:---|:---|:---|",
    ])
    for d in CUSTOMER_DECODER:
        md.append(f"| {d['complaint']} | {d['meaning']} | {d['agents']} | {d['question']} |")

    md_text = "\n".join(md)
    (ROOT / "SUPPLY_CHAIN_101_MASTER_GUIDE.md").write_text(md_text, encoding="utf-8")
    (ROOT / "docs" / "SUPPLY_CHAIN_101_MASTER_GUIDE.md").write_text(md_text, encoding="utf-8")
    print("Wrote SUPPLY_CHAIN_101_MASTER_GUIDE.md")

    # 2. Build Interactive HTML Academy (supply_chain_101_interactive_academy.html)
    flashcards_json = json.dumps(FLASHCARDS, ensure_ascii=False)
    quiz_json = json.dumps(QUIZ_QUESTIONS, ensure_ascii=False)

    decoder_rows_html = []
    for idx, d in enumerate(CUSTOMER_DECODER, 1):
        decoder_rows_html.append(f"""
          <div class="ac-decoder-card">
            <div style="display:flex; align-items:center; justify-content:space-between; gap:10px; margin-bottom:8px;">
              <span class="ac-pill" style="color:#fb7185; border-color:rgba(244,63,94,0.35);">🗣️ Customer Scenario #{idx:02d}</span>
            </div>
            <div style="font-family:var(--font-display); font-size:18px; font-weight:800; color:var(--text-primary); margin-bottom:12px;">
              {html.escape(d['complaint'])}
            </div>
            <div class="ac-decoder-grid">
              <div class="ac-decoder-box">
                <span class="ac-box-kicker" style="color:#38bdf8;">💡 WHAT THEY MEAN IN PLAIN WORDS</span>
                <p>{html.escape(d['meaning'])}</p>
              </div>
              <div class="ac-decoder-box">
                <span class="ac-box-kicker" style="color:#10b981;">🤖 WHICH OF OUR AI AGENTS SOLVES IT</span>
                <p style="font-weight:700;">{html.escape(d['agents'])}</p>
              </div>
              <div class="ac-decoder-box">
                <span class="ac-box-kicker" style="color:#fbbf24;">🎯 SMART QUESTION TO ASK THEM NEXT</span>
                <p style="font-style:italic;">{html.escape(d['question'])}</p>
              </div>
            </div>
          </div>
        """)

    academy_html = f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Supply Chain 101 Interactive Academy — Learn From Zero (Visuals, 3D Flashcards &amp; Customer Decoder)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Google+Sans+Display:wght@500;700;800&family=Google+Sans+Text:wght@400;500;700&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-canvas: #070b14;
      --bg-card: #0f172a;
      --bg-elevated: #162033;
      --text-primary: #f8fafc;
      --text-secondary: #cbd5e1;
      --border-subtle: rgba(148, 163, 184, 0.18);
      --font-display: 'Google Sans Display', 'Inter', sans-serif;
      --font-sans: 'Google Sans Text', 'Inter', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}
    html[data-theme="light"] {{
      --bg-canvas: #f1f5f9;
      --bg-card: #ffffff;
      --bg-elevated: #f8fafc;
      --text-primary: #0f172a;
      --text-secondary: #334155;
      --border-subtle: rgba(15, 23, 42, 0.12);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: var(--font-sans);
      background: var(--bg-canvas);
      color: var(--text-primary);
      line-height: 1.65;
    }}
    .ac-navbar {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(15, 23, 42, 0.92);
      backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border-subtle);
      padding: 14px 4vw;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      flex-wrap: wrap;
    }}
    html[data-theme="light"] .ac-navbar {{
      background: rgba(255, 255, 255, 0.94);
    }}
    .ac-container {{
      max-width: 1520px;
      width: 92vw;
      margin: 0 auto;
      padding: 28px 0 90px;
    }}
    .ac-hero {{
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(56, 189, 248, 0.12));
      border: 1.5px solid var(--border-subtle);
      border-top: 4px solid #10b981;
      border-radius: 22px;
      padding: 28px 34px;
      margin-bottom: 24px;
    }}
    .ac-mod-tabs {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 26px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      padding: 12px 16px;
      border-radius: 18px;
    }}
    .ac-mod-btn {{
      font-family: var(--font-sans);
      font-size: 14px;
      font-weight: 800;
      padding: 11px 18px;
      border-radius: 12px;
      border: 1.5px solid var(--border-subtle);
      background: var(--bg-elevated);
      color: var(--text-primary);
      cursor: pointer;
      transition: all 0.18s ease;
    }}
    .ac-mod-btn.active, .ac-mod-btn:hover {{
      background: #2563eb;
      color: #ffffff;
      border-color: #38bdf8;
      transform: translateY(-1px);
    }}
    .ac-module-pane {{
      display: none;
    }}
    .ac-module-pane.active {{
      display: block;
    }}
    .ac-card {{
      background: var(--bg-card);
      border: 1.5px solid var(--border-subtle);
      border-radius: 20px;
      padding: 26px 30px;
      margin-bottom: 24px;
      box-shadow: 0 10px 26px rgba(0, 0, 0, 0.16);
    }}
    .ac-pill {{
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 800;
      padding: 4px 11px;
      border-radius: 999px;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      display: inline-block;
    }}
    /* Interactive 6-Stage Journey Strip */
    .ac-stage-strip {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(175px, 1fr));
      gap: 12px;
      margin: 18px 0;
    }}
    .ac-stage-node {{
      background: var(--bg-elevated);
      border: 2px solid var(--border-subtle);
      border-radius: 16px;
      padding: 16px 14px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .ac-stage-node.active, .ac-stage-node:hover {{
      border-color: #38bdf8;
      background: rgba(56, 189, 248, 0.12);
      transform: translateY(-3px);
    }}
    .ac-stage-detail {{
      background: var(--bg-elevated);
      border: 1.5px solid rgba(56, 189, 248, 0.4);
      border-left: 5px solid #38bdf8;
      border-radius: 16px;
      padding: 22px 26px;
      margin-top: 14px;
    }}
    /* Bullwhip Simulator Bars */
    .ac-bullwhip-row {{
      display: flex;
      align-items: center;
      gap: 14px;
      margin-bottom: 12px;
    }}
    .ac-bullwhip-label {{
      width: 220px;
      font-weight: 700;
      font-size: 14px;
    }}
    .ac-bullwhip-track {{
      flex: 1;
      height: 28px;
      background: var(--bg-canvas);
      border-radius: 999px;
      overflow: hidden;
      border: 1px solid var(--border-subtle);
    }}
    .ac-bullwhip-fill {{
      height: 100%;
      border-radius: 999px;
      transition: width 0.35s cubic-bezier(0.22, 1, 0.36, 1);
      display: flex;
      align-items: center;
      padding-left: 12px;
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 800;
      color: #ffffff;
    }}
    /* 3D Flip Flashcards */
    .ac-flashcards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 18px;
    }}
    .ac-flip-card {{
      perspective: 1200px;
      cursor: pointer;
      min-height: 250px;
      user-select: none;
    }}
    .ac-flip-inner {{
      display: grid;
      grid-template-areas: "face";
      width: 100%;
      height: 100%;
      min-height: 250px;
      transition: transform 0.52s cubic-bezier(0.22, 1, 0.36, 1);
      transform-style: preserve-3d;
    }}
    .ac-flip-card.is-flipped .ac-flip-inner {{
      transform: rotateY(180deg);
    }}
    .ac-flip-front, .ac-flip-back {{
      grid-area: face;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      background: var(--bg-card);
      border: 1.5px solid var(--border-subtle);
      border-top: 4px solid #38bdf8;
      border-radius: 18px;
      padding: 22px 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.16);
    }}
    .ac-flip-back {{
      transform: rotateY(180deg);
      background: var(--bg-elevated);
      border-top-color: #10b981;
    }}
    .ac-flip-card.learned .ac-flip-front {{
      border-color: rgba(16, 185, 129, 0.5);
      border-top: 4px solid #10b981;
    }}
    /* Customer Decoder */
    .ac-decoder-card {{
      background: var(--bg-card);
      border: 1.5px solid var(--border-subtle);
      border-left: 5px solid #38bdf8;
      border-radius: 18px;
      padding: 22px 26px;
      margin-bottom: 18px;
    }}
    .ac-decoder-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 14px;
    }}
    .ac-decoder-box {{
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 14px 16px;
    }}
    .ac-box-kicker {{
      display: block;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 800;
      margin-bottom: 6px;
    }}
    .ac-decoder-box p {{
      margin: 0;
      font-size: 14.5px;
      line-height: 1.58;
    }}
    /* Quiz */
    .ac-quiz-card {{
      background: var(--bg-card);
      border: 1.5px solid var(--border-subtle);
      border-radius: 18px;
      padding: 22px 26px;
      margin-bottom: 18px;
    }}
    .ac-quiz-opt {{
      display: block;
      width: 100%;
      text-align: left;
      font-family: var(--font-sans);
      font-size: 15px;
      font-weight: 600;
      padding: 12px 16px;
      margin-bottom: 10px;
      border-radius: 12px;
      border: 1.5px solid var(--border-subtle);
      background: var(--bg-elevated);
      color: var(--text-primary);
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .ac-quiz-opt:hover {{
      border-color: #38bdf8;
    }}
    .ac-quiz-opt.correct {{
      background: rgba(16, 185, 129, 0.18);
      border-color: #10b981;
      color: #10b981;
    }}
    .ac-quiz-opt.wrong {{
      background: rgba(244, 63, 94, 0.16);
      border-color: #f43f5e;
      color: #fb7185;
    }}
  </style>
</head>
<body>
  <header class="ac-navbar">
    <div style="display:flex; align-items:center; gap:14px; flex-wrap:wrap;">
      <a href="index.html" style="text-decoration:none; color:var(--text-primary); font-family:var(--font-display); font-size:20px; font-weight:800;">
        &larr; Supply Chain Portal
      </a>
      <span class="ac-pill" style="color:#10b981; border-color:rgba(16,185,129,0.4);">🎓 Supply Chain 101 Interactive Academy</span>
    </div>
    <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
      <a href="agent_testing_and_video_playbook.html" class="ac-mod-btn" style="text-decoration:none; padding:8px 14px; font-size:13px;">📋 60-Agent Testing Playbook</a>
      <button type="button" class="ac-mod-btn" style="padding:8px 14px; font-size:13px;" onclick="document.documentElement.setAttribute('data-theme', document.documentElement.getAttribute('data-theme')==='light'?'dark':'light')">
        🌗 Theme
      </button>
    </div>
  </header>

  <main class="ac-container">
    <section class="ac-hero">
      <div style="font-family:var(--font-mono); font-size:12px; font-weight:800; color:#10b981; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">
        LEARN SUPPLY CHAIN FROM ZERO · VISUAL SIMULATORS, 56 3D FLASHCARDS &amp; CUSTOMER DECODER
      </div>
      <h1 style="font-family:var(--font-display); font-size:clamp(26px, 3vw, 40px); margin:0 0 10px;">
        Supply Chain 101 — Everything Explained Simply &amp; Visually
      </h1>
      <p style="font-size:16.5px; color:var(--text-secondary); margin:0; max-width:1100px;">
        Built so you can master Supply Chain from the beginning without dry textbooks or unexplained jargon. Every abbreviation (<code>OTIF</code>, <code>S&amp;OP</code>, <code>WAPE</code>, <code>MEIO</code>, <code>ATP</code>, <code>3-Way Match</code>, <code>OEE</code>) is spelled out and paired with interactive visual simulators and flashcards.
      </p>
    </section>

    <!-- 5 Interactive Learning Modules Navigation -->
    <nav class="ac-mod-tabs">
      <button type="button" class="ac-mod-btn active" onclick="switchModule('mod1', this)">🌍 1 · Big Picture &amp; Bullwhip Simulator</button>
      <button type="button" class="ac-mod-btn" onclick="switchModule('mod2', this)">🃏 2 · 56 Interactive 3D Flashcards (All Terms Decoded)</button>
      <button type="button" class="ac-mod-btn" onclick="switchModule('mod3', this)">🏗️ 3 · The 6 Pillars &amp; 4 Core Workflows</button>
      <button type="button" class="ac-mod-btn" onclick="switchModule('mod4', this)">🗣️ 4 · Customer Conversation Decoder (20 Scenarios)</button>
      <button type="button" class="ac-mod-btn" onclick="switchModule('mod5', this)">🧠 5 · 12-Question Interactive Self-Quiz</button>
    </nav>

    <!-- =====================================================================
         MODULE 1: THE BIG PICTURE, 6-STAGE JOURNEY & BULLWHIP SIMULATOR
         ===================================================================== -->
    <section id="mod1" class="ac-module-pane active">
      <!-- END-TO-END ANIMATED 3-FLOW SUPPLY CHAIN ARCHITECTURE DIAGRAM -->
      <div class="ac-card" style="padding:22px 24px;">
        <div class="ac-pill" style="color:#10b981; margin-bottom:8px;">ANIMATED END-TO-END ARCHITECTURE INFOGRAPHIC · THE 3 SYNCHRONIZED FLOWS</div>
        <h2 style="font-family:var(--font-display); font-size:25px; margin:0 0 8px;">
          The Complete Supply Chain Blueprint: Physical Goods (──▶), Demand Signals (◀──), and Cash (◀──▶)
        </h2>
        <p style="font-size:15px; color:var(--text-secondary); margin:0 0 14px;">
          Every supply chain is <strong>3 simultaneous rivers</strong> flowing across 6 physical nodes. When any one of these 3 flows gets delayed or distorted, the whole company loses money:
        </p>
        <svg viewBox="0 0 1120 235" style="width:100%; height:auto; display:block; background:rgba(2,6,23,0.65); border-radius:16px; border:1px solid rgba(148,163,184,0.22);">
          <!-- Top Flow: Physical Material Flow (Downstream ->) -->
          <text x="560" y="24" text-anchor="middle" fill="#10b981" font-size="11.5" font-weight="800" font-family="JetBrains Mono, monospace">
            FLOW 1 · PHYSICAL GOODS &amp; INVENTORY FLOW (DOWNSTREAM: SUPPLIER ──▶ FACTORY ──▶ WAREHOUSE ──▶ TRUCK ──▶ CUSTOMER)
          </text>
          <path id="physFlowPath" d="M 95 95 L 1025 95" stroke="#10b981" stroke-width="3" stroke-dasharray="7 5" fill="none"/>
          <circle r="5.5" fill="#10b981">
            <animateMotion dur="5s" repeatCount="indefinite" path="M 95 95 L 1025 95"/>
          </circle>
          <circle r="5.5" fill="#34d399">
            <animateMotion dur="5s" begin="2.5s" repeatCount="indefinite" path="M 95 95 L 1025 95"/>
          </circle>

          <!-- 6 Supply Chain Nodes -->
          <g transform="translate(22, 48)">
            <rect width="150" height="94" rx="12" fill="#0f172a" stroke="#f59e0b" stroke-width="2"/>
            <text x="75" y="26" text-anchor="middle" fill="#f59e0b" font-size="10.5" font-weight="800" font-family="JetBrains Mono, monospace">01 · SOURCE</text>
            <text x="75" y="48" text-anchor="middle" fill="#f8fafc" font-size="13" font-weight="800" font-family="Inter, sans-serif">⛏️ Tier-2/1 Suppliers</text>
            <text x="75" y="68" text-anchor="middle" fill="#cbd5e1" font-size="10.5" font-family="Inter, sans-serif">BOM · RFQ · PO · 3-Way</text>
            <text x="75" y="84" text-anchor="middle" fill="#94a3b8" font-size="10" font-family="JetBrains Mono, monospace">SAP Ariba / ERP</text>
          </g>

          <g transform="translate(206, 48)">
            <rect width="150" height="94" rx="12" fill="#0f172a" stroke="#8b5cf6" stroke-width="2"/>
            <text x="75" y="26" text-anchor="middle" fill="#c084fc" font-size="10.5" font-weight="800" font-family="JetBrains Mono, monospace">02 · MAKE</text>
            <text x="75" y="48" text-anchor="middle" fill="#f8fafc" font-size="13" font-weight="800" font-family="Inter, sans-serif">🏭 Factory &amp; Lines</text>
            <text x="75" y="68" text-anchor="middle" fill="#cbd5e1" font-size="10.5" font-family="Inter, sans-serif">OEE · MTS/MTO · eBHR</text>
            <text x="75" y="84" text-anchor="middle" fill="#94a3b8" font-size="10" font-family="JetBrains Mono, monospace">MES / SCADA / PLC</text>
          </g>

          <g transform="translate(390, 48)">
            <rect width="150" height="94" rx="12" fill="#0f172a" stroke="#10b981" stroke-width="2"/>
            <text x="75" y="26" text-anchor="middle" fill="#10b981" font-size="10.5" font-weight="800" font-family="JetBrains Mono, monospace">03 · CENTRAL DC</text>
            <text x="75" y="48" text-anchor="middle" fill="#f8fafc" font-size="13" font-weight="800" font-family="Inter, sans-serif">🏢 Regional DC (RDC)</text>
            <text x="75" y="68" text-anchor="middle" fill="#cbd5e1" font-size="10.5" font-family="Inter, sans-serif">MEIO · Safety Stock · ROP</text>
            <text x="75" y="84" text-anchor="middle" fill="#94a3b8" font-size="10" font-family="JetBrains Mono, monospace">Supply Planning / IBP</text>
          </g>

          <g transform="translate(574, 48)">
            <rect width="150" height="94" rx="12" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
            <text x="75" y="26" text-anchor="middle" fill="#38bdf8" font-size="10.5" font-weight="800" font-family="JetBrains Mono, monospace">04 · LOCAL DC</text>
            <text x="75" y="48" text-anchor="middle" fill="#f8fafc" font-size="13" font-weight="800" font-family="Inter, sans-serif">📦 Fulfillment (FDC)</text>
            <text x="75" y="68" text-anchor="middle" fill="#cbd5e1" font-size="10.5" font-family="Inter, sans-serif">FEFO · Slotting · ATP</text>
            <text x="75" y="84" text-anchor="middle" fill="#94a3b8" font-size="10" font-family="JetBrains Mono, monospace">Manhattan / SAP WMS</text>
          </g>

          <g transform="translate(758, 48)">
            <rect width="150" height="94" rx="12" fill="#0f172a" stroke="#06b6d4" stroke-width="2"/>
            <text x="75" y="26" text-anchor="middle" fill="#22d3ee" font-size="10.5" font-weight="800" font-family="JetBrains Mono, monospace">05 · DELIVER</text>
            <text x="75" y="48" text-anchor="middle" fill="#f8fafc" font-size="13" font-weight="800" font-family="Inter, sans-serif">🚚 Multi-Modal Fleet</text>
            <text x="75" y="68" text-anchor="middle" fill="#cbd5e1" font-size="10.5" font-family="Inter, sans-serif">FTL/LTL · LIFO · BOL/ASN</text>
            <text x="75" y="84" text-anchor="middle" fill="#94a3b8" font-size="10" font-family="JetBrains Mono, monospace">Oracle / Blue Yonder TMS</text>
          </g>

          <g transform="translate(942, 48)">
            <rect width="156" height="94" rx="12" fill="#0f172a" stroke="#f43f5e" stroke-width="2"/>
            <text x="78" y="26" text-anchor="middle" fill="#fb7185" font-size="10.5" font-weight="800" font-family="JetBrains Mono, monospace">06 · CUSTOMER &amp; ESG</text>
            <text x="78" y="48" text-anchor="middle" fill="#f8fafc" font-size="13" font-weight="800" font-family="Inter, sans-serif">🛒 Store, POS &amp; RMA</text>
            <text x="78" y="68" text-anchor="middle" fill="#cbd5e1" font-size="10.5" font-family="Inter, sans-serif">OTIF · ePOD · Scope 3</text>
            <text x="78" y="84" text-anchor="middle" fill="#94a3b8" font-size="10" font-family="JetBrains Mono, monospace">Retail POS &amp; Returns</text>
          </g>

          <!-- Bottom Flow 2: Demand & Information Signals (Upstream <-) -->
          <path d="M 1020 166 L 95 166" stroke="#38bdf8" stroke-width="2.5" stroke-dasharray="6 4" fill="none"/>
          <circle r="5" fill="#38bdf8">
            <animateMotion dur="4.5s" repeatCount="indefinite" path="M 1020 166 L 95 166"/>
          </circle>
          <text x="560" y="185" text-anchor="middle" fill="#38bdf8" font-size="11" font-weight="800" font-family="JetBrains Mono, monospace">
            FLOW 2 · DEMAND &amp; INFORMATION SIGNALS (UPSTREAM: POS CHECKOUT SCANS ◀── ORDERS ◀── S&amp;OP FORECASTS ◀── SUPPLIER POs)
          </text>

          <!-- Bottom Flow 3: Cash & Working Capital (Cyclic <->) -->
          <path d="M 1020 204 L 95 204" stroke="#f59e0b" stroke-width="2" stroke-dasharray="4 4" fill="none"/>
          <circle r="4.5" fill="#f59e0b">
            <animateMotion dur="6s" repeatCount="indefinite" path="M 1020 204 L 95 204"/>
          </circle>
          <text x="560" y="223" text-anchor="middle" fill="#f59e0b" font-size="11" font-weight="800" font-family="JetBrains Mono, monospace">
            FLOW 3 · CASH CONVERSION CYCLE (CCC = DIO + DSO − DPO: CUSTOMER INVOICE PAID ◀── WORKING CAPITAL ──▶ SUPPLIER 3-WAY MATCH PAID)
          </text>
        </svg>
      </div>

      <div class="ac-card">
        <div class="ac-pill" style="color:#38bdf8; margin-bottom:8px;">INTERACTIVE VISUAL MAP · CLICK ANY STAGE BELOW</div>
        <h2 style="font-family:var(--font-display); font-size:26px; margin:0 0 8px;">
          How Every Physical Product Moves From Raw Ingredients to the Customer
        </h2>
        <p style="font-size:15.5px; color:var(--text-secondary); margin:0 0 16px;">
          Think of a supply chain as a <strong>6-stage relay race</strong>. Click each of the 6 stages below to see what happens there in plain words, what software runs that stage, and what goes wrong!
        </p>

        <div class="ac-stage-strip" id="journeyStageStrip">
          <div class="ac-stage-node active" onclick="selectJourneyStage(0, this)">
            <div style="font-size:30px; margin-bottom:6px;">⛏️</div>
            <div style="font-family:var(--font-mono); font-size:11px; color:#f59e0b; font-weight:800;">STAGE 01 · SOURCE</div>
            <div style="font-weight:800; font-size:15px; margin-top:4px;">Tier-2 &amp; Tier-1 Suppliers</div>
          </div>
          <div class="ac-stage-node" onclick="selectJourneyStage(1, this)">
            <div style="font-size:30px; margin-bottom:6px;">🏭</div>
            <div style="font-family:var(--font-mono); font-size:11px; color:#8b5cf6; font-weight:800;">STAGE 02 · MAKE</div>
            <div style="font-weight:800; font-size:15px; margin-top:4px;">The Factory Floor</div>
          </div>
          <div class="ac-stage-node" onclick="selectJourneyStage(2, this)">
            <div style="font-size:30px; margin-bottom:6px;">🏢</div>
            <div style="font-family:var(--font-mono); font-size:11px; color:#10b981; font-weight:800;">STAGE 03 · STORE (RDC)</div>
            <div style="font-weight:800; font-size:15px; margin-top:4px;">Regional Warehouse</div>
          </div>
          <div class="ac-stage-node" onclick="selectJourneyStage(3, this)">
            <div style="font-size:30px; margin-bottom:6px;">📦</div>
            <div style="font-family:var(--font-mono); font-size:11px; color:#38bdf8; font-weight:800;">STAGE 04 · STORE (FDC)</div>
            <div style="font-weight:800; font-size:15px; margin-top:4px;">Local Fulfillment DC</div>
          </div>
          <div class="ac-stage-node" onclick="selectJourneyStage(4, this)">
            <div style="font-size:30px; margin-bottom:6px;">🚚</div>
            <div style="font-family:var(--font-mono); font-size:11px; color:#06b6d4; font-weight:800;">STAGE 05 · MOVE</div>
            <div style="font-weight:800; font-size:15px; margin-top:4px;">Ships, Planes, Rail &amp; Trucks</div>
          </div>
          <div class="ac-stage-node" onclick="selectJourneyStage(5, this)">
            <div style="font-size:30px; margin-bottom:6px;">🛒</div>
            <div style="font-family:var(--font-mono); font-size:11px; color:#f43f5e; font-weight:800;">STAGE 06 · SELL &amp; RETURN</div>
            <div style="font-weight:800; font-size:15px; margin-top:4px;">Store Shelf, POS &amp; RMA</div>
          </div>
        </div>

        <div id="journeyStageDetail" class="ac-stage-detail"></div>
      </div>

      <!-- INTERACTIVE BULLWHIP EFFECT SIMULATOR -->
      <div class="ac-card">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:14px; flex-wrap:wrap; margin-bottom:14px;">
          <div>
            <span class="ac-pill" style="color:#f59e0b; margin-bottom:6px;">INTERACTIVE SIMULATOR · DRAG THE SLIDER</span>
            <h2 style="font-family:var(--font-display); font-size:25px; margin:0;">
              The #1 Enemy in Supply Chain: “The Bullwhip Effect”
            </h2>
          </div>
          <button type="button" id="aiDampenBtn" class="ac-mod-btn" style="background:rgba(16,185,129,0.16); color:#10b981; border-color:#10b981;" onclick="toggleBullwhipAi()">
            ✨ Turn On AI Demand Sensing: OFF
          </button>
        </div>
        <p style="font-size:15.5px; color:var(--text-secondary); margin:0 0 18px;">
          When customers at the store buy just <strong>+10% more</strong> of a product, the store manager panics and orders +18% more. The local warehouse sees that jump and orders +32% more. By the time the signal reaches the factory and raw material suppliers, they see a massive <strong>+75% panic wave</strong> — building mountains of extra stock that later goes unsold! Drag the slider below and toggle AI on/off:
        </p>

        <div style="background:var(--bg-elevated); padding:18px 22px; border-radius:16px; border:1px solid var(--border-subtle); margin-bottom:18px;">
          <label style="font-weight:800; font-size:15px; display:flex; align-items:center; justify-content:space-between;">
            <span>🛒 Actual Customer Buying Surge at the Store Checkout (POS):</span>
            <span id="bwInputLabel" style="font-family:var(--font-mono); font-size:18px; color:#38bdf8;">+10%</span>
          </label>
          <input type="range" id="bwSlider" min="5" max="25" value="10" style="width:100%; margin-top:10px; accent-color:#38bdf8;" oninput="updateBullwhip()" />
        </div>

        <div id="bullwhipBarsWrap"></div>
      </div>

      <!-- THE 4 ENTERPRISE SOFTWARE SYSTEMS RELAY RACE -->
      <div class="ac-card">
        <span class="ac-pill" style="color:#a855f7; margin-bottom:8px;">SOFTWARE CHEAT SHEET · THE 4 CORE SYSTEMS</span>
        <h2 style="font-family:var(--font-display); font-size:25px; margin:0 0 12px;">
          How a Company’s 4 Software Systems Talk to Each Other (ERP vs. MES vs. WMS vs. TMS)
        </h2>
        <div class="ac-decoder-grid">
          <div class="ac-decoder-box" style="border-top:3px solid #3b82f6;">
            <span class="ac-box-kicker" style="color:#38bdf8;">1. ERP (Enterprise Resource Planning)</span>
            <p><strong>Examples:</strong> SAP S/4HANA, Oracle Cloud ERP.<br/><strong>What it does:</strong> The corporate financial brain. Takes customer orders, sends Purchase Orders (POs) to suppliers, and manages accounting invoices.</p>
          </div>
          <div class="ac-decoder-box" style="border-top:3px solid #8b5cf6;">
            <span class="ac-box-kicker" style="color:#c084fc;">2. MES (Manufacturing Execution System)</span>
            <p><strong>Examples:</strong> Siemens Opcenter, Rockwell.<br/><strong>What it does:</strong> Runs the factory floor. Tracks which batch is running on which machine, reads PLC sensors, and logs quality batch records (eBHR).</p>
          </div>
          <div class="ac-decoder-box" style="border-top:3px solid #10b981;">
            <span class="ac-box-kicker" style="color:#10b981;">3. WMS (Warehouse Management System)</span>
            <p><strong>Examples:</strong> Manhattan Active, SAP EWM.<br/><strong>What it does:</strong> Runs inside the 4 walls of the warehouse. Tracks which rack bin every pallet sits in (Slotting) and guides workers with barcode scanners (Wave Picking).</p>
          </div>
          <div class="ac-decoder-box" style="border-top:3px solid #06b6d4;">
            <span class="ac-box-kicker" style="color:#22d3ee;">4. TMS (Transportation Management System)</span>
            <p><strong>Examples:</strong> Blue Yonder TMS, Oracle OTM.<br/><strong>What it does:</strong> Runs everything moving outside between locations. Books trucking/ocean carriers, plans delivery routes, and audits freight bills.</p>
          </div>
        </div>
      </div>

      <!-- 4 VISUAL INFOGRAPHIC CHEAT-SHEETS (SVG DIAGRAMS) -->
      <div class="ac-card">
        <span class="ac-pill" style="color:#38bdf8; margin-bottom:8px;">📊 VISUAL CHEAT-SHEET INFOGRAPHICS · 4 CONCEPTS EVERY CSCO TALKS ABOUT</span>
        <h2 style="font-family:var(--font-display); font-size:25px; margin:0 0 16px;">
          4 Essential Supply Chain Diagrams (MTS vs. MTO · FEFO/FIFO/LIFO · Cash Cycle · Scope 1/2/3)
        </h2>
        <div style="display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:16px;">
          <!-- Infographic 1: MTS vs MTO -->
          <div style="background:var(--bg-elevated); border:1px solid var(--border-subtle); border-radius:16px; padding:16px;">
            <div style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; color:#c084fc; margin-bottom:6px;">
              1 · MAKE-TO-STOCK (MTS / PUSH) VS. MAKE-TO-ORDER (MTO / PULL)
            </div>
            <svg viewBox="0 0 500 135" style="width:100%; height:auto; display:block; background:rgba(2,6,23,0.55); border-radius:10px;">
              <rect x="14" y="16" width="220" height="46" rx="8" fill="#1e1b4b" stroke="#8b5cf6"/>
              <text x="124" y="36" text-anchor="middle" fill="#c084fc" font-size="11" font-weight="800" font-family="JetBrains Mono, monospace">MTS (MAKE-TO-STOCK · PUSH)</text>
              <text x="124" y="52" text-anchor="middle" fill="#e2e8f0" font-size="10.5" font-family="Inter, sans-serif">Build from Forecast → Hold in DC → Fast Ship</text>
              <rect x="266" y="16" width="220" height="46" rx="8" fill="#064e3b" stroke="#10b981"/>
              <text x="376" y="36" text-anchor="middle" fill="#34d399" font-size="11" font-weight="800" font-family="JetBrains Mono, monospace">MTO (MAKE-TO-ORDER · PULL)</text>
              <text x="376" y="52" text-anchor="middle" fill="#e2e8f0" font-size="10.5" font-family="Inter, sans-serif">Wait for Order → Custom Build → Zero Dead Stock</text>
              <rect x="14" y="76" width="472" height="44" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-dasharray="4 3"/>
              <text x="250" y="95" text-anchor="middle" fill="#38bdf8" font-size="11" font-weight="800" font-family="JetBrains Mono, monospace">⚖️ DECOUPLING POINT (POSTPONEMENT)</text>
              <text x="250" y="111" text-anchor="middle" fill="#cbd5e1" font-size="10.5" font-family="Inter, sans-serif">Hold semi-finished base components in stock (MTS), then finish/label only when ordered (MTO)</text>
            </svg>
          </div>

          <!-- Infographic 2: FEFO vs FIFO vs LIFO -->
          <div style="background:var(--bg-elevated); border:1px solid var(--border-subtle); border-radius:16px; padding:16px;">
            <div style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; color:#10b981; margin-bottom:6px;">
              2 · WAREHOUSE &amp; TRUCK RULES: FEFO VS. FIFO VS. LIFO
            </div>
            <svg viewBox="0 0 500 135" style="width:100%; height:auto; display:block; background:rgba(2,6,23,0.55); border-radius:10px;">
              <rect x="12" y="16" width="150" height="104" rx="8" fill="#0f172a" stroke="#f43f5e"/>
              <text x="87" y="36" text-anchor="middle" fill="#fb7185" font-size="11" font-weight="800" font-family="JetBrains Mono, monospace">FEFO (First-Expired)</text>
              <text x="87" y="56" text-anchor="middle" fill="#f8fafc" font-size="11" font-weight="700" font-family="Inter, sans-serif">🥛 Food / Pharma</text>
              <text x="87" y="76" text-anchor="middle" fill="#cbd5e1" font-size="10" font-family="Inter, sans-serif">Ship batch expiring</text>
              <text x="87" y="92" text-anchor="middle" fill="#cbd5e1" font-size="10" font-family="Inter, sans-serif">soonest first!</text>

              <rect x="175" y="16" width="150" height="104" rx="8" fill="#0f172a" stroke="#10b981"/>
              <text x="250" y="36" text-anchor="middle" fill="#34d399" font-size="11" font-weight="800" font-family="JetBrains Mono, monospace">FIFO (First-In)</text>
              <text x="250" y="56" text-anchor="middle" fill="#f8fafc" font-size="11" font-weight="700" font-family="Inter, sans-serif">📦 Standard Goods</text>
              <text x="250" y="76" text-anchor="middle" fill="#cbd5e1" font-size="10" font-family="Inter, sans-serif">Ship oldest arrived</text>
              <text x="250" y="92" text-anchor="middle" fill="#cbd5e1" font-size="10" font-family="Inter, sans-serif">pallet first!</text>

              <rect x="338" y="16" width="150" height="104" rx="8" fill="#0f172a" stroke="#38bdf8"/>
              <text x="413" y="36" text-anchor="middle" fill="#38bdf8" font-size="11" font-weight="800" font-family="JetBrains Mono, monospace">LIFO (Last-In)</text>
              <text x="413" y="56" text-anchor="middle" fill="#f8fafc" font-size="11" font-weight="700" font-family="Inter, sans-serif">🚚 Multi-Stop Truck</text>
              <text x="413" y="76" text-anchor="middle" fill="#cbd5e1" font-size="10" font-family="Inter, sans-serif">Load Stop #1 last</text>
              <text x="413" y="92" text-anchor="middle" fill="#cbd5e1" font-size="10" font-family="Inter, sans-serif">(at rear doors)!</text>
            </svg>
          </div>

          <!-- Infographic 3: Cash Conversion Cycle (CCC) -->
          <div style="background:var(--bg-elevated); border:1px solid var(--border-subtle); border-radius:16px; padding:16px;">
            <div style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; color:#f59e0b; margin-bottom:6px;">
              3 · CASH CONVERSION CYCLE FORMULA: CCC = DIO + DSO − DPO
            </div>
            <svg viewBox="0 0 500 135" style="width:100%; height:auto; display:block; background:rgba(2,6,23,0.55); border-radius:10px;">
              <rect x="14" y="18" width="230" height="36" rx="6" fill="rgba(56,189,248,0.22)" stroke="#38bdf8"/>
              <text x="129" y="40" text-anchor="middle" fill="#38bdf8" font-size="11" font-weight="800" font-family="JetBrains Mono, monospace">+ DIO: Stock Sits (55 Days)</text>
              <rect x="252" y="18" width="234" height="36" rx="6" fill="rgba(168,85,247,0.22)" stroke="#a855f7"/>
              <text x="369" y="40" text-anchor="middle" fill="#c084fc" font-size="11" font-weight="800" font-family="JetBrains Mono, monospace">+ DSO: Customer Pays (40 Days)</text>
              <rect x="14" y="66" width="190" height="48" rx="6" fill="rgba(16,185,129,0.2)" stroke="#10b981"/>
              <text x="109" y="88" text-anchor="middle" fill="#10b981" font-size="11" font-weight="800" font-family="JetBrains Mono, monospace">− DPO: Pay Vendor</text>
              <text x="109" y="104" text-anchor="middle" fill="#6ee7b7" font-size="10.5" font-family="JetBrains Mono, monospace">(45 Days Credit)</text>
              <rect x="214" y="66" width="272" height="48" rx="6" fill="rgba(245,158,11,0.22)" stroke="#f59e0b"/>
              <text x="350" y="88" text-anchor="middle" fill="#fbbf24" font-size="11.5" font-weight="800" font-family="JetBrains Mono, monospace">= CCC: 50 DAYS CASH LOCKED UP</text>
              <text x="350" y="104" text-anchor="middle" fill="#fde68a" font-size="10" font-family="Inter, sans-serif">Every 1 day reduced frees millions in cash!</text>
            </svg>
          </div>

          <!-- Infographic 4: Scope 1, 2, 3 Carbon Emissions -->
          <div style="background:var(--bg-elevated); border:1px solid var(--border-subtle); border-radius:16px; padding:16px;">
            <div style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; color:#fb7185; margin-bottom:6px;">
              4 · CARBON EMISSIONS: SCOPE 1 VS. SCOPE 2 VS. SCOPE 3 (85% OF TOTAL)
            </div>
            <svg viewBox="0 0 500 135" style="width:100%; height:auto; display:block; background:rgba(2,6,23,0.55); border-radius:10px;">
              <rect x="14" y="18" width="95" height="98" rx="8" fill="#0f172a" stroke="#94a3b8"/>
              <text x="61" y="42" text-anchor="middle" fill="#cbd5e1" font-size="11" font-weight="800" font-family="JetBrains Mono, monospace">SCOPE 1</text>
              <text x="61" y="64" text-anchor="middle" fill="#f8fafc" font-size="15" font-weight="800" font-family="JetBrains Mono, monospace">~8%</text>
              <text x="61" y="84" text-anchor="middle" fill="#94a3b8" font-size="9.5" font-family="Inter, sans-serif">Own boilers</text>
              <text x="61" y="98" text-anchor="middle" fill="#94a3b8" font-size="9.5" font-family="Inter, sans-serif">&amp; company vans</text>

              <rect x="120" y="18" width="95" height="98" rx="8" fill="#0f172a" stroke="#38bdf8"/>
              <text x="167" y="42" text-anchor="middle" fill="#38bdf8" font-size="11" font-weight="800" font-family="JetBrains Mono, monospace">SCOPE 2</text>
              <text x="167" y="64" text-anchor="middle" fill="#f8fafc" font-size="15" font-weight="800" font-family="JetBrains Mono, monospace">~7%</text>
              <text x="167" y="84" text-anchor="middle" fill="#94a3b8" font-size="9.5" font-family="Inter, sans-serif">Purchased grid</text>
              <text x="167" y="98" text-anchor="middle" fill="#94a3b8" font-size="9.5" font-family="Inter, sans-serif">electricity</text>

              <rect x="226" y="18" width="260" height="98" rx="8" fill="rgba(16,185,129,0.14)" stroke="#10b981" stroke-width="2"/>
              <text x="356" y="40" text-anchor="middle" fill="#10b981" font-size="11.5" font-weight="800" font-family="JetBrains Mono, monospace">SCOPE 3 · SUPPLY CHAIN (85%!)</text>
              <text x="356" y="64" text-anchor="middle" fill="#f8fafc" font-size="13" font-weight="800" font-family="Inter, sans-serif">Suppliers + Ocean/Air/Truck Freight</text>
              <text x="356" y="84" text-anchor="middle" fill="#cbd5e1" font-size="10.5" font-family="Inter, sans-serif">Tracked by CBAM (Carbon Border Tax) &amp;</text>
              <text x="356" y="100" text-anchor="middle" fill="#cbd5e1" font-size="10.5" font-family="Inter, sans-serif">EUDR (Deforestation Satellite Ledger)</text>
            </svg>
          </div>
        </div>
      </div>
    </section>

    <!-- =====================================================================
         MODULE 2: 56 INTERACTIVE 3D FLIP-FLASHCARDS
         ===================================================================== -->
    <section id="mod2" class="ac-module-pane">
      <div class="ac-card">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:14px; flex-wrap:wrap; margin-bottom:16px;">
          <div>
            <span class="ac-pill" style="color:#38bdf8; margin-bottom:6px;">CLICK ANY CARD TO FLIP IN 3D · ZERO UNEXPLAINED ACRONYMS</span>
            <h2 style="font-family:var(--font-display); font-size:26px; margin:0;">
              56 Supply Chain Flashcards — Every Term Spelled Out &amp; Explained Simply
            </h2>
          </div>
          <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
            <span id="learnedCountBadge" class="ac-pill" style="color:#10b981; border-color:#10b981; font-size:13px;">✓ 0 / 56 Learned</span>
            <button type="button" class="ac-mod-btn" style="padding:8px 14px; font-size:13px;" onclick="shuffleFlashcards()">🔀 Shuffle Deck</button>
          </div>
        </div>

        <div style="display:flex; align-items:center; justify-content:space-between; gap:10px; flex-wrap:wrap; margin-bottom:20px;">
          <div style="display:flex; gap:8px; flex-wrap:wrap;" id="fcCatButtons">
            <button type="button" class="ac-mod-btn active" style="padding:7px 14px; font-size:13px;" onclick="filterFlashcards('all', this)">All ({len(FLASHCARDS)})</button>
            <button type="button" class="ac-mod-btn" style="padding:7px 14px; font-size:13px;" onclick="filterFlashcards('top15', this)">⭐ Top 15 Must-Know</button>
            <button type="button" class="ac-mod-btn" style="padding:7px 14px; font-size:13px;" onclick="filterFlashcards('planning', this)">01 · Planning</button>
            <button type="button" class="ac-mod-btn" style="padding:7px 14px; font-size:13px;" onclick="filterFlashcards('sourcing', this)">02 · Sourcing</button>
            <button type="button" class="ac-mod-btn" style="padding:7px 14px; font-size:13px;" onclick="filterFlashcards('manufacturing', this)">03 · Factory</button>
            <button type="button" class="ac-mod-btn" style="padding:7px 14px; font-size:13px;" onclick="filterFlashcards('inventory', this)">04 · Warehouse &amp; Stock</button>
            <button type="button" class="ac-mod-btn" style="padding:7px 14px; font-size:13px;" onclick="filterFlashcards('logistics', this)">05 · Logistics &amp; Trucks</button>
            <button type="button" class="ac-mod-btn" style="padding:7px 14px; font-size:13px;" onclick="filterFlashcards('governance', this)">06 · OTIF, Returns &amp; Carbon</button>
          </div>
          <input type="search" id="fcSearchInput" placeholder="🔍 Search acronym (e.g. OTIF, WAPE, BOM)…" style="padding:9px 16px; border-radius:999px; border:1.5px solid var(--border-subtle); background:var(--bg-elevated); color:var(--text-primary); min-width:260px;" oninput="renderFlashcards()" />
        </div>

        <div id="flashcardsGrid" class="ac-flashcards-grid"></div>
      </div>
    </section>

    <!-- =====================================================================
         MODULE 3: THE 6 PILLARS & 4 END-TO-END WORKFLOWS
         ===================================================================== -->
    <section id="mod3" class="ac-module-pane">
      <div class="ac-card">
        <span class="ac-pill" style="color:#10b981; margin-bottom:8px;">END-TO-END PROCESS SIMULATOR</span>
        <h2 style="font-family:var(--font-display); font-size:26px; margin:0 0 12px;">
          The 4 Master Workflows Every Company Runs (Step-by-Step in Plain Words)
        </h2>
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:18px;">
          <button type="button" class="ac-mod-btn active" onclick="selectWorkflowSim(0, this)">1 · Forecast-to-Plan (S&amp;OP)</button>
          <button type="button" class="ac-mod-btn" onclick="selectWorkflowSim(1, this)">2 · Source-to-Pay (Buying &amp; 3-Way Match)</button>
          <button type="button" class="ac-mod-btn" onclick="selectWorkflowSim(2, this)">3 · Order-to-Delivery (ATP &rarr; WMS &rarr; TMS)</button>
          <button type="button" class="ac-mod-btn" onclick="selectWorkflowSim(3, this)">4 · Disruption-to-Recovery (Control Tower)</button>
        </div>
        <div id="workflowSimContainer"></div>
      </div>
    </section>

    <!-- =====================================================================
         MODULE 4: CUSTOMER CONVERSATION DECODER (20 SCENARIOS)
         ===================================================================== -->
    <section id="mod4" class="ac-module-pane">
      <div class="ac-card">
        <span class="ac-pill" style="color:#fb7185; margin-bottom:8px;">MEETING CHEAT SHEET · 20 REAL CUSTOMER COMPLAINTS DECODED</span>
        <h2 style="font-family:var(--font-display); font-size:26px; margin:0 0 8px;">
          When the Customer Says X &rarr; What It Means &rarr; Which Agent to Demo
        </h2>
        <p style="font-size:15.5px; color:var(--text-secondary); margin:0 0 20px;">
          Use this decoder before or during any customer call. It translates common executive complaints into plain English, tells you which of our 60 AI Agents solves it, and gives you a smart follow-up question to ask!
        </p>
        {''.join(decoder_rows_html)}
      </div>
    </section>

    <!-- =====================================================================
         MODULE 5: 12-QUESTION INTERACTIVE SELF-QUIZ
         ===================================================================== -->
    <section id="mod5" class="ac-module-pane">
      <div class="ac-card">
        <div style="display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap; margin-bottom:16px;">
          <div>
            <span class="ac-pill" style="color:#38bdf8; margin-bottom:6px;">TEST YOUR UNDERSTANDING · INSTANT EXPLANATIONS</span>
            <h2 style="font-family:var(--font-display); font-size:26px; margin:0;">
              12-Question Supply Chain Customer Readiness Quiz
            </h2>
          </div>
          <span id="quizScoreBadge" class="ac-pill" style="color:#10b981; font-size:14px;">Score: 0 / 12</span>
        </div>
        <div id="quizContainer"></div>
      </div>
    </section>
  </main>

  <script>
    const FLASHCARDS = {flashcards_json};
    const QUIZ = {quiz_json};

    const JOURNEY_STAGES = [
      {{
        title: "Stage 01 · Tier-2 & Tier-1 Suppliers (Sourcing & Procurement)",
        what: "Before your factory can build anything, you need raw materials and parts. Your direct vendors are called 'Tier-1 Suppliers' (e.g., a bottle maker). The companies that supply raw plastic resin or aluminum to your bottle maker are 'Tier-2 and Tier-3 Suppliers.'",
        systems: "SAP Ariba / ERP Procurement, Multi-Hop Supplier Graph DB",
        pain: "Buyers don't know if a supplier's price quote is padded, don't know when a Tier-2 chemical plant in Taiwan shuts down, and waste hours matching invoices against Purchase Orders (3-Way Match).",
        agents: "RFQ Should-Cost Agent (rfq_should_cost_agent), Tier-N Risk Sentinel (tier_n_risk_sentinel), Three-Way Match Dispute Agent (three_way_match_dispute)"
      }},
      {{
        title: "Stage 02 · The Factory Floor (Manufacturing & Production)",
        what: "Raw materials enter the plant and are mixed, molded, assembled, and packaged on high-speed production lines. Plant Managers track OEE (Overall Equipment Effectiveness = Uptime × Speed × Quality) and try to minimize 'Changeover Time' (cleaning/setup between different products).",
        systems: "MES (Manufacturing Execution System), PLC Machine Controllers, Quality Lab (LIMS / eBHR)",
        pain: "Unplanned machine breakdowns halt the entire line, bad scheduling causes excessive wash-down changeovers, and QA takes 5 days to manually review 200-page paper Batch Records (eBHR) before goods can ship.",
        agents: "Predictive OEE Maintenance Sentinel (predictive_oee_sentinel), Line Schedule Optimizer (line_schedule_optimizer), Inline Yield & Vision Guardian (inline_yield_guardian), Batch Record Auditor (batch_record_auditor)"
      }},
      {{
        title: "Stage 03 · Regional Distribution Center — RDC (Multi-Echelon Inventory)",
        what: "Full truckloads and trainloads leave the factory and arrive at a giant central Regional Distribution Center (RDC). The RDC holds strategic 'Safety Stock' (buffer inventory) and replenishes smaller local warehouses.",
        systems: "Supply Planning (SAP IBP / Kinaxis), MEIO (Multi-Echelon Inventory Optimization)",
        pain: "If the RDC, Local DC, and Stores all calculate their safety stock in isolation, the company holds 25% too much inventory (trapping millions in Working Capital cash) while still running out of fast-selling items!",
        agents: "MEIO Safety Stock Agent (meio_safety_stock_agent), SLOB Disposition Agent (slob_disposition_agent), Working Capital Cash Bridge (working_capital_cash_bridge)"
      }},
      {{
        title: "Stage 04 · Local Fulfillment Center — FDC (Inside the Warehouse / WMS)",
        what: "Inside the warehouse, workers unload inbound trucks (Dock-to-Stock), put pallets into rack bins (Slotting), walk aisles with barcode scanners to pick customer orders (Wave Picking), or move boxes straight from inbound to outbound doors (Cross-Docking).",
        systems: "WMS (Warehouse Management System — Manhattan Active, SAP EWM), Real-Time ATP DB",
        pain: "Fast-selling items are stored in far-away bins (wasting picker walking time), trucks wait 3 hours at the yard gate (causing Detention fines), and overselling stock hurts VIP customers.",
        agents: "Warehouse Slotting Optimizer (warehouse_slotting_agent), Wave Fulfillment Copilot (wave_fulfillment_copilot), ATP Order Promising Agent (atp_order_promising_agent), Yard & Dock Sequencer (yard_dock_sequencer)"
      }},
      {{
        title: "Stage 05 · Multi-Modal Logistics (Ocean, Air, Rail & Road Fleet / TMS)",
        what: "Goods move across the globe via Ocean container ships, Air cargo planes (ULDs), Intermodal Rail, and 53-foot Road Trucks. Logistics teams try to combine expensive small shipments (LTL) into Full Truckloads (FTL) packed in reverse stop order (3D LIFO).",
        systems: "TMS (Transportation Management System), Ocean AIS & Flight Telemetry, Truck ELD & GPS",
        pain: "Trailers leave 30% empty, ocean containers rack up $300/day port Demurrage fees, drivers run out of legal Hours of Service (HOS), and carriers overbill on fuel/accessorial invoices.",
        agents: "3D Load Consolidation Studio (load_consolidation_agent), FleetFlow Route Optimizer (fleetflow_dispatch), Ocean Port Drayage Orchestrator (port_drayage_orchestrator), Freight Bill Audit Agent (freight_bill_audit_agent)"
      }},
      {{
        title: "Stage 06 · Store Shelf, Customer Checkout (POS) & Returns (RMA)",
        what: "The product reaches the retail shelf or customer doorstep. Every checkout scan is a POS (Point of Sale) signal. If the delivery arrived late or short, the retailer fines the brand an OTIF (On-Time In-Full) penalty. If a shopper returns an item (RMA), Reverse Logistics decides what to do with it.",
        systems: "Retail EDI 852 (POS Scans), CRM / Order Management, Returns Portal, Scope-3 Carbon Ledger",
        pain: "Empty shelves cause hidden lost sales (Demand Censorship), unfair OTIF fines cost millions, and shipping cheap returned items back costs more than the item is worth!",
        agents: "Demand Sensing Agent (demand_sensing_agent), OTIF Penalty Shield (otif_penalty_shield), Keep-It vs. Return Routing Advisor (keep_it_routing_advisor), Scope-3 & CBAM Carbon Ledger (carbon_scope3_ledger)"
      }}
    ];

    const WORKFLOW_SIMS = [
      {{
        title: "Workflow 1 · Forecast-to-Plan (How Customer Scans Turn Into a Factory Plan)",
        steps: [
          "1. Daily POS Scans & Weather Arrive: Shoppers buy +28% more sports drinks during a Texas heatwave. Cash register scans (EDI 852) stream into BigQuery.",
          "2. Uncensor Stockouts: Store #209 ran out of stock on Thursday (recording 0 scans). The Demand Sensing Agent detects the stockout and estimates the true hidden demand.",
          "3. Strip Sales Optimism Bias (FVA): A regional sales rep manually inflated their forecast by +15%. The AI checks historical Forecast Value Added (FVA) and dampens the bias.",
          "4. S&OP Trade-Off Simulation: The S&OP Scenario Weaver checks if the Austin Factory has enough capacity, comparing overtime cost vs. lost high-margin sales.",
          "5. Multi-Echelon Buffer Update (MEIO): Safety stock targets are rebalanced across the Dallas RDC and local FDCs.",
          "6. ERP Plan Commit: The consensus forecast (PIR) is written directly into SAP IBP / ERP with an immutable audit receipt."
        ]
      }},
      {{
        title: "Workflow 2 · Source-to-Pay (How Companies Buy Parts & Pay Suppliers Safely)",
        steps: [
          "1. Explode the Bill of Materials (BOM): To build 50,000 units next month, the ERP calculates exact quantities of resin, microchips, and cartons needed.",
          "2. Should-Cost & RFQ Bid Analysis: The RFQ Should-Cost Agent compares supplier price quotes against live global commodity indices to spot a 12% overcharge.",
          "3. Tier-N Sub-Supplier Risk Check: Before awarding the Purchase Order (PO), the Tier-N Risk Sentinel verifies the vendor's Tier-2 wafer fab isn't in a typhoon zone.",
          "4. Issue Purchase Order (PO): The approved PO is sent to the supplier via EDI 850 / SAP Ariba.",
          "5. Dock Goods Receipt (GRN) & QA Check: When the supplier's truck arrives, the warehouse scans the pallets (GRN) and QA checks the Certificate of Analysis (COA).",
          "6. Automated 3-Way Match: The Three-Way Match Agent compares PO vs. GRN vs. Supplier Invoice — auto-paying exact matches and issuing a debit memo for any short shipment."
        ]
      }},
      {{
        title: "Workflow 3 · Order-to-Delivery (How a Customer Order Gets Picked, Packed & Delivered OTIF)",
        steps: [
          "1. Real-Time Available-to-Promise (ATP): A retail customer orders 2,000 cases. The ATP Agent checks uncommitted stock across all DCs in <50ms and reserves the stock.",
          "2. Warehouse Wave Release (WMS): The Wave Fulfillment Copilot groups the order into the 2:00 PM carrier wave and routes pickers through Golden Zone bins.",
          "3. 3D LIFO Trailer Consolidation: The 3D Load Consolidation Studio combines this order with 2 nearby stops into one Full Truckload (94% cube, legal axle weights, Stop #1 loaded at the tail door).",
          "4. Yard & Dock Sequencing: When the carrier's truck approaches the geofence, YardPulse assigns Dock Door #14 immediately so detention fees are $0.",
          "5. Dynamic Route Dispatch (TMS): FleetFlow routes the driver around highway congestion while respecting legal ELD Hours-of-Service limits.",
          "6. OTIF Delivery & ePOD Proof: The truck arrives on time, logs digital Proof of Delivery (ePOD), and the OTIF Penalty Shield archives the GPS proof to prevent any false retailer chargeback."
        ]
      }},
      {{
        title: "Workflow 4 · Disruption-to-Recovery (How the Control Tower Handles an Emergency)",
        steps: [
          "1. Live Disruption Trigger: A typhoon closes Kaohsiung Port OR a freezer reefer truck suffers a +6°C temperature excursion in transit.",
          "2. Blast-Radius Graph Mapping: The Disruption War-Room Orchestrator traces which shipments, SKUs, and VIP customer orders are impacted and calculates Revenue-at-Risk ($).",
          "3. Generate 3 Ranked Recovery Options: Option A (Air-freight critical batch), Option B (Re-allocate buffer stock from Chicago RDC), Option C (Split-ship partial order).",
          "4. Pre-Execution Governance Gate: If the cost impact is within autonomous limits, the agent proceeds; if >20% variance, it alerts the CSCO in the Control Tower for 1-click sign-off.",
          "5. Multi-System Actuation: The agent updates the TMS route, locks any spoiled cold-chain lot in the WMS, and updates the customer ETA.",
          "6. Closed-Loop Learning: The Master Data Lead-Time Steward updates supplier/lane lead-time distributions so future safety stock reflects the real risk."
        ]
      }}
    ];

    function switchModule(modId, btn) {{
      document.querySelectorAll('.ac-module-pane').forEach(p => p.classList.remove('active'));
      document.querySelectorAll('.ac-mod-tabs .ac-mod-btn').forEach(b => b.classList.remove('active'));
      document.getElementById(modId).classList.add('active');
      if (btn) btn.classList.add('active');
    }}

    function selectJourneyStage(idx, el) {{
      document.querySelectorAll('#journeyStageStrip .ac-stage-node').forEach(n => n.classList.remove('active'));
      if (el) el.classList.add('active');
      const st = JOURNEY_STAGES[idx];
      document.getElementById('journeyStageDetail').innerHTML = `
        <h3 style="font-family:var(--font-display); font-size:21px; margin:0 0 10px; color:#38bdf8;">${{st.title}}</h3>
        <p style="font-size:16px; margin:0 0 14px; color:var(--text-primary);">${{st.what}}</p>
        <div class="ac-decoder-grid">
          <div class="ac-decoder-box">
            <span class="ac-box-kicker" style="color:#f59e0b;">💻 SOFTWARE USED AT THIS STAGE</span>
            <p>${{st.systems}}</p>
          </div>
          <div class="ac-decoder-box">
            <span class="ac-box-kicker" style="color:#fb7185;">✕ WHAT GOES WRONG MANUALLY</span>
            <p>${{st.pain}}</p>
          </div>
          <div class="ac-decoder-box">
            <span class="ac-box-kicker" style="color:#10b981;">✦ OUR AI AGENTS AT THIS STAGE</span>
            <p style="font-weight:700;">${{st.agents}}</p>
          </div>
        </div>
      `;
    }}

    let bullwhipAiOn = false;
    function toggleBullwhipAi() {{
      bullwhipAiOn = !bullwhipAiOn;
      const btn = document.getElementById('aiDampenBtn');
      btn.innerHTML = bullwhipAiOn ? '✨ AI Demand Sensing: ON (Bullwhip Flattened!)' : '✨ Turn On AI Demand Sensing: OFF';
      btn.style.background = bullwhipAiOn ? '#10b981' : 'rgba(16,185,129,0.16)';
      btn.style.color = bullwhipAiOn ? '#ffffff' : '#10b981';
      updateBullwhip();
    }}

    function updateBullwhip() {{
      const val = parseInt(document.getElementById('bwSlider').value, 10);
      document.getElementById('bwInputLabel').textContent = '+' + val + '%';
      const mults = bullwhipAiOn ? [1.0, 1.05, 1.10, 1.12, 1.15] : [1.0, 1.8, 3.2, 5.2, 7.5];
      const colors = ['#38bdf8', '#10b981', '#f59e0b', '#fb7185', '#ef4444'];
      const labels = [
        '1. Store Checkout Scans (POS)',
        '2. Store Manager Order to Local DC',
        '3. Local DC Order to Regional DC',
        '4. Regional DC Order to Factory',
        '5. Factory Order to Raw Material Supplier'
      ];
      const htmlRows = labels.map((lbl, i) => {{
        const pct = Math.round(val * mults[i]);
        const widthPct = Math.min(100, Math.max(12, Math.round(pct / 2)));
        const col = bullwhipAiOn ? '#10b981' : colors[i];
        return `
          <div class="ac-bullwhip-row">
            <div class="ac-bullwhip-label">${{lbl}}</div>
            <div class="ac-bullwhip-track">
              <div class="ac-bullwhip-fill" style="width:${{widthPct}}%; background:${{col}};">
                +${{pct}}% Order Swing
              </div>
            </div>
          </div>
        `;
      }}).join('');
      document.getElementById('bullwhipBarsWrap').innerHTML = htmlRows;
    }}

    let currentFcFilter = 'all';
    function filterFlashcards(cat, btn) {{
      currentFcFilter = cat;
      document.querySelectorAll('#fcCatButtons .ac-mod-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      renderFlashcards();
    }}

    function shuffleFlashcards() {{
      FLASHCARDS.sort(() => Math.random() - 0.5);
      renderFlashcards();
    }}

    function toggleLearned(term, ev) {{
      ev.stopPropagation();
      const key = 'sc101_learned_' + term;
      const cur = localStorage.getItem(key) === '1';
      localStorage.setItem(key, cur ? '0' : '1');
      renderFlashcards();
    }}

    function renderFlashcards() {{
      const q = (document.getElementById('fcSearchInput').value || '').toLowerCase().trim();
      let learnedTotal = 0;
      FLASHCARDS.forEach(fc => {{
        if (localStorage.getItem('sc101_learned_' + fc.term) === '1') learnedTotal++;
      }});
      document.getElementById('learnedCountBadge').textContent = `✓ ${{learnedTotal}} / ${{FLASHCARDS.length}} Learned`;

      const filtered = FLASHCARDS.filter(fc => {{
        const matchCat = (currentFcFilter === 'all') ||
                         (currentFcFilter === 'top15' && fc.top15) ||
                         (fc.cat === currentFcFilter);
        const matchQ = !q || (fc.term + ' ' + fc.full + ' ' + fc.hook + ' ' + fc.plain).toLowerCase().includes(q);
        return matchCat && matchQ;
      }});

      document.getElementById('flashcardsGrid').innerHTML = filtered.map(fc => {{
        const isLearned = localStorage.getItem('sc101_learned_' + fc.term) === '1';
        return `
          <div class="ac-flip-card ${{isLearned ? 'learned' : ''}}" onclick="this.classList.toggle('is-flipped')">
            <div class="ac-flip-inner">
              <div class="ac-flip-front">
                <div>
                  <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; margin-bottom:10px;">
                    <span class="ac-pill" style="color:#38bdf8;">${{fc.cat.toUpperCase()}}${{fc.top15 ? ' · ⭐ TOP 15' : ''}}</span>
                    <span class="ac-pill">↻ Tap to Flip</span>
                  </div>
                  <div style="font-family:var(--font-display); font-size:26px; font-weight:800; color:var(--text-primary); line-height:1.2;">
                    ${{fc.term}}
                  </div>
                  <div style="font-size:14.5px; font-weight:700; color:#38bdf8; margin-top:4px;">
                    ${{fc.full}}
                  </div>
                  <p style="font-size:15px; color:var(--text-secondary); margin:14px 0 0; line-height:1.55;">
                    ${{fc.hook}}
                  </p>
                </div>
                <div style="display:flex; align-items:center; justify-content:space-between; margin-top:14px;">
                  <span style="font-size:12px; color:var(--text-secondary);">Tap for plain-English example &rarr;</span>
                  <button type="button" class="ac-pill" style="cursor:pointer; color:${{isLearned ? '#10b981' : 'var(--text-secondary)'}}; border-color:${{isLearned ? '#10b981' : 'var(--border-subtle)'}};" onclick="toggleLearned('${{fc.term.replace(/'/g, '')}}', event)">
                    ${{isLearned ? '✓ Learned' : '○ Mark Learned'}}
                  </button>
                </div>
              </div>
              <div class="ac-flip-back">
                <div>
                  <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
                    <span style="font-family:var(--font-mono); font-size:12px; font-weight:800; color:#10b981;">${{fc.term}} — PLAIN ENGLISH</span>
                    <span class="ac-pill">↺ Back</span>
                  </div>
                  <p style="font-size:14px; color:var(--text-primary); margin:0 0 10px; line-height:1.55;">
                    <strong>Meaning:</strong> ${{fc.plain}}
                  </p>
                  <p style="font-size:13.5px; color:var(--text-secondary); margin:0 0 10px; line-height:1.5;">
                    <strong>Example:</strong> ${{fc.example}}
                  </p>
                </div>
                <div style="padding:10px 12px; border-radius:10px; background:rgba(56,189,248,0.1); border:1px solid rgba(56,189,248,0.3); font-size:12.5px; color:var(--text-primary); line-height:1.45;">
                  <strong style="color:#38bdf8;">🗣️ Customer Tip:</strong> ${{fc.customer_tip}}
                </div>
              </div>
            </div>
          </div>
        `;
      }}).join('');
    }}

    function selectWorkflowSim(idx, btn) {{
      if (btn) {{
        btn.parentElement.querySelectorAll('.ac-mod-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
      }}
      const wf = WORKFLOW_SIMS[idx];
      document.getElementById('workflowSimContainer').innerHTML = `
        <h3 style="font-family:var(--font-display); font-size:21px; color:#38bdf8; margin:0 0 14px;">${{wf.title}}</h3>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:14px;">
          ${{wf.steps.map(s => `
            <div class="ac-decoder-box" style="border-left:4px solid #10b981;">
              <p style="font-size:15px; line-height:1.6; color:var(--text-primary);">${{s}}</p>
            </div>
          `).join('')}}
        </div>
      `;
    }}

    let quizAnswered = {{}};
    function answerQuiz(qIdx, optIdx) {{
      quizAnswered[qIdx] = optIdx;
      renderQuiz();
    }}

    function renderQuiz() {{
      let correctCount = 0;
      QUIZ.forEach((q, idx) => {{
        if (quizAnswered[idx] === q.correct) correctCount++;
      }});
      document.getElementById('quizScoreBadge').textContent = `Score: ${{correctCount}} / ${{QUIZ.length}}`;

      document.getElementById('quizContainer').innerHTML = QUIZ.map((q, qIdx) => {{
        const chosen = quizAnswered[qIdx];
        const hasAnswered = chosen !== undefined;
        return `
          <div class="ac-quiz-card">
            <div style="font-family:var(--font-display); font-size:18px; font-weight:800; margin-bottom:14px;">
              ${{q.q}}
            </div>
            <div>
              ${{q.options.map((opt, oIdx) => {{
                let cls = 'ac-quiz-opt';
                if (hasAnswered) {{
                  if (oIdx === q.correct) cls += ' correct';
                  else if (oIdx === chosen) cls += ' wrong';
                }}
                return `<button type="button" class="${{cls}}" onclick="answerQuiz(${{qIdx}}, ${{oIdx}})">${{opt}}</button>`;
              }}).join('')}}
            </div>
            ${{hasAnswered ? `
              <div style="margin-top:12px; padding:14px 16px; border-radius:12px; background:rgba(16,185,129,0.12); border:1px solid rgba(16,185,129,0.35); font-size:14.5px; color:var(--text-primary);">
                💡 ${{q.explain}}
              </div>
            ` : ''}}
          </div>
        `;
      }}).join('');
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      selectJourneyStage(0, document.querySelector('#journeyStageStrip .ac-stage-node'));
      updateBullwhip();
      renderFlashcards();
      selectWorkflowSim(0, null);
      renderQuiz();
    }});
  </script>
</body>
</html>
"""
    (ROOT / "supply_chain_101_interactive_academy.html").write_text(academy_html, encoding="utf-8")
    for sub in ["docs", "zipline_dist", "dist/itc_limited"]:
        d = ROOT / sub
        if d.exists():
            (d / "supply_chain_101_interactive_academy.html").write_text(academy_html, encoding="utf-8")
    print("Wrote supply_chain_101_interactive_academy.html")

    # Add a discreet link to Supply Chain 101 Academy in the top navbar of index.html, periodic_table.html, and mind_map.html
    for path in [ROOT / "index.html", ROOT / "periodic_table.html", ROOT / "mind_map.html"]:
        text = path.read_text(encoding="utf-8")
        if 'href="supply_chain_101_interactive_academy.html"' not in text:
            text = text.replace(
                '<a href="agent_testing_and_video_playbook.html" class="nav-link"',
                '<a href="supply_chain_101_interactive_academy.html" class="nav-link" style="color:#38bdf8; font-weight:700;">🎓 Supply Chain 101</a>\n        <a href="agent_testing_and_video_playbook.html" class="nav-link"',
                1
            )
            path.write_text(text, encoding="utf-8")
            print(f"Added Supply Chain 101 navbar link to {path.name}")


if __name__ == "__main__":
    build_academy_files()

# -*- coding: utf-8 -*-
"""Comprehensive Course Data for Supply Chain 101 Masterclass.
Contains:
1. 76 Flashcards with full plain-English expansions, numerical examples, and customer tips.
2. Enterprise AI Control Tower Deep Dive Specification (ITC Blueprint).
3. Alphabet Internal AI Supply Chain Playbook Specification.
4. 25 Customer Conversation Decoder Scenarios.
5. 20-Question CSCO Domain Certification Exam.
"""

# =============================================================================
# 1. 76 COMPREHENSIVE 3D FLIP FLASHCARDS
# =============================================================================
FLASHCARDS = [
    # --- PLANNING & S&OP (14 cards) ---
    {
        "term": "SKU",
        "full": "Stock Keeping Unit",
        "cat": "planning",
        "top20": True,
        "hook": "A unique scannable barcode for one specific size, flavor, or color.",
        "plain": "A shirt in Medium Blue and Large Blue are two different SKUs. Every barcode in a warehouse or retail store represents one distinct SKU with its own inventory level.",
        "example": "A beverage company makes 1 brand of sports drink in 4 flavors × 3 bottle sizes = 12 distinct SKUs to forecast and stock.",
        "customer_tip": "Ask: 'How many active SKUs do you manage across warehouses, and which 20% of SKUs drive 80% of your sales volume?' (Show: Demand Sensing Agent / SLOB Disposition Agent)."
    },
    {
        "term": "POS",
        "full": "Point of Sale (Cash Register Scans)",
        "cat": "planning",
        "top20": True,
        "hook": "Real-time data of what shoppers are actually buying at checkout counters today.",
        "plain": "When a cashier scans an item at Walmart, Target, or ITC retail stores, that is a POS scan. If manufacturers only look at warehouse reorders instead of daily POS scans, they are blind to consumer demand shifts by 2 to 4 weeks.",
        "example": "During a sudden heatwave, POS scans for sports drinks jump +35% on Friday, even though retail stores haven't placed new warehouse reorders yet.",
        "customer_tip": "Say: 'Our Demand Sensing Agent ingests daily POS cash-register scans and weather signals to detect demand spikes 14 days before legacy ERP purchase orders arrive.'"
    },
    {
        "term": "S&OP",
        "full": "Sales & Operations Planning",
        "cat": "planning",
        "top20": True,
        "hook": "The monthly executive ritual where Sales, Finance, and Supply Chain agree on one consensus plan.",
        "plain": "Sales always wants surplus inventory so they never lose a sale. Finance wants minimal inventory to conserve cash. Factories want steady schedules without expensive overtime. S&OP is the monthly cadence to align all three on ONE operating plan.",
        "example": "Sales forecasts 120,000 units, but the plant can only produce 100,000 without weekend overtime. In S&OP, leadership uses AI simulations to decide whether paying overtime produces a positive net profit.",
        "customer_tip": "Say: 'Our S&OP Scenario Weaver turns a 3-week spreadsheet debate into a 30-second live profit-vs-fill-rate optimization simulation.'"
    },
    {
        "term": "IBP",
        "full": "Integrated Business Planning",
        "cat": "planning",
        "top20": False,
        "hook": "Next-generation S&OP software connecting supply plans directly to the corporate P&L balance sheet.",
        "plain": "IBP evolves traditional S&OP software (like SAP IBP or Kinaxis). Instead of only tracking physical unit volumes, IBP translates every supply chain forecast into monetary dollars: Revenue, Gross Margin, and Working Capital impact.",
        "example": "When an agent updates a product forecast, it writes the new numbers into SAP IBP so finance and manufacturing see bottom-line financial impacts immediately.",
        "customer_tip": "Say: 'Our AI agents do not replace your SAP IBP or Kinaxis systems; they act as an autonomous intelligence layer on top and write clean allocations back.'"
    },
    {
        "term": "WAPE & MAPE",
        "full": "Weighted / Mean Absolute Percentage Error",
        "cat": "planning",
        "top20": True,
        "hook": "The universal report card measuring how accurate your demand forecasts were.",
        "plain": "MAPE measures average percentage error equally across all products. WAPE weights the error by sales volume, ensuring that a forecasting error on your best-selling product counts more heavily than an error on an unpopular slow-moving item.",
        "example": "If you sell 10,000 cases of Cola and miss by 500 (5% error), but sell 10 cases of Diet Lime and miss by 5 (50% error), MAPE says 27.5% error, but volume-weighted WAPE is only 5.04%!",
        "customer_tip": "Say: 'Dropping forecast WAPE from 32% down to 21% using Gemini and TimesFM unlocked $4.2M in trapped safety stock working capital.'"
    },
    {
        "term": "CPFR",
        "full": "Collaborative Planning, Forecasting & Replenishment",
        "cat": "planning",
        "top20": False,
        "hook": "Sharing real-time forecast data between manufacturer and retailer to prevent stockouts.",
        "plain": "Instead of guessing what Walmart or Target will order next month, the supplier and retailer connect systems to collaboratively share inventory positions, promotion calendars, and replenishment plans.",
        "example": "Unilever and Walmart share POS feeds daily so Unilever factories automatically schedule packaging runs 10 days before store shelves run low.",
        "customer_tip": "Show: CPFR Channel Sync Agent (`cpfr_sync_agent`) resolving channel order discrepancies automatically."
    },
    {
        "term": "TimesFM",
        "full": "Time Series Foundation Model (Google Research)",
        "cat": "planning",
        "top20": True,
        "hook": "Google's pre-trained deep learning foundation model specialized for zero-shot demand forecasting.",
        "plain": "Unlike traditional statistical models (ARIMA) that require individual model training per SKU, TimesFM is trained on hundreds of billions of time points, allowing it to predict seasonal demand, holiday lifts, and trend shifts zero-shot.",
        "example": "Forecasting 50,000 SKUs across 200 regional depots takes hours on legacy systems, but runs in seconds with TimesFM on Vertex AI.",
        "customer_tip": "Say: 'We power our Demand Sensing Agent with Google's TimesFM foundation model, capturing non-linear retail seasonality out of the box.'"
    },
    {
        "term": "MTS vs MTO",
        "full": "Make-to-Stock vs Make-to-Order",
        "cat": "planning",
        "top20": False,
        "hook": "Building products in advance for warehouse shelves vs waiting until a customer places an order.",
        "plain": "Make-to-Stock (MTS) builds finished goods in advance based on forecasts (e.g. toothpaste, soda). Make-to-Order (MTO) waits for a customer purchase order before manufacturing begins (e.g. custom aerospace parts, Boeing planes, Dell custom servers).",
        "example": "MTS requires high safety stock accuracy; MTO requires dynamic supplier component lead time visibility.",
        "customer_tip": "Ask: 'What percentage of your production volume is MTS versus MTO, and where do lead time delays hurt your delivery promises most?'"
    },
    {
        "term": "Safety Stock",
        "full": "Buffer Inventory Held for Unexpected Spikes",
        "cat": "planning",
        "top20": True,
        "hook": "The insurance cushion inventory kept in the warehouse so you never run out of stock during demand spikes.",
        "plain": "If a supplier shipment is delayed by 4 days, or a sudden weekend promotion doubles demand, safety stock prevents store shelves from going empty.",
        "example": "If daily demand is 100 units and supplier lead time fluctuates by +/- 3 days, keeping 300 units of safety stock protects against 99% of stockout risks.",
        "customer_tip": "Show: Echelon Inventory Allocator (`echelon_inventory_allocator`) dynamically recalculating safety stock based on lead time volatility."
    },
    {
        "term": "Lead Time",
        "full": "Order Placement to Receipt Elapsed Time",
        "cat": "planning",
        "top20": True,
        "hook": "The total calendar days from when you submit a purchase order until boxes arrive at your receiving dock.",
        "plain": "Lead time includes supplier manufacturing time, export customs clearance, ocean shipping transit, port drayage, and warehouse inwarding.",
        "example": "A microchip ordered from Taiwan has a 14-week lead time: 8 weeks fabrication, 4 weeks ocean shipping, 2 weeks customs and domestic trucking.",
        "customer_tip": "Say: 'When supplier lead times drift by even 3 days without ERP updates, MRP systems order too late, causing factory shutdowns.'"
    },
    {
        "term": "Demand Shaping",
        "full": "Influencing Customer Orders via Pricing & Promos",
        "cat": "planning",
        "top20": False,
        "hook": "Using promotional discounts or incentives to shift customer demand toward inventory you already have in stock.",
        "plain": "When a factory has excess inventory of Product A and a severe shortage of Product B, Marketing runs a flash discount on Product A to steer customer orders toward available supply.",
        "example": "An airline drops ticket prices on Tuesday morning flights to fill empty seats while raising prices on sold-out Friday evenings.",
        "customer_tip": "Show: Promo Lift Simulator (`promo_lift_simulator`) calculating price elasticity and margin trade-offs."
    },
    {
        "term": "Bullwhip Effect",
        "full": "Demand Distortion Amplification Upstream",
        "cat": "planning",
        "top20": True,
        "hook": "A tiny 5% wobble in consumer checkout purchases creates a massive 40% panic overreaction at raw material suppliers.",
        "plain": "When retailers see a small sales increase, they order extra buffer stock from distributors. Distributors panic and order even more from factories. Factories purchase huge amounts of raw materials. Each tier adds their own safety buffer, creating massive order swings upstream.",
        "example": "The 2020 toilet paper shortage: Consumer consumption barely increased, but panic buying caused retailers to double orders, leading mills to add extra shifts, followed by huge warehouse surpluses months later.",
        "customer_tip": "Say: 'Our end-to-end agents share real-time POS consumption across all tiers, eliminating the bullwhip effect at its root.'"
    },
    {
        "term": "Cannibalization",
        "full": "Demand Theft from Existing Products",
        "cat": "planning",
        "top20": False,
        "hook": "When launching a new product steals sales from your own existing high-margin catalog items.",
        "plain": "If a beverage brand launches 'Zero Sugar Berry', 60% of its sales might come from shoppers who previously bought their regular 'Diet Berry' drink.",
        "example": "Failing to account for cannibalization causes over-forecasting of legacy SKUs, leading to millions in expired, obsolete inventory.",
        "customer_tip": "Highlight: Demand Sensing Agent cross-elasticity matrix isolating net-new volume from cannibalized sales."
    },
    {
        "term": "Fill Rate",
        "full": "Percentage of Customer Demand Met Immediately from Stock",
        "cat": "planning",
        "top20": True,
        "hook": "The share of ordered items that ship immediately without placing the customer on backorder.",
        "plain": "If customers order 10,000 cases and you ship 9,800 cases on day one, your line-item fill rate is 98%. Raising fill rate from 95% to 99% usually requires doubling safety stock.",
        "example": "CPG manufacturers target 98.5% fill rate with retail giants like Walmart to avoid costly delivery penalties.",
        "customer_tip": "Show: Dynamic Order Promising ATP (`dynamic_order_promising_atp`) reserving stock for tier-1 high-margin contracts."
    },

    # --- SOURCING & PROCUREMENT (12 cards) ---
    {
        "term": "RFQ / RFP",
        "full": "Request for Quotation / Proposal",
        "cat": "sourcing",
        "top20": True,
        "hook": "A formal bid packet sent to suppliers asking for pricing, capacity, and commercial delivery terms.",
        "plain": "When an enterprise needs to buy $10M of raw materials, they issue an RFQ to 5 approved vendors specifying technical tolerances, quality standards, and delivery dates.",
        "example": "An automaker sends an RFQ for 200,000 stamped steel door panels, comparing tooling costs, piece prices, and freight terms across 4 stamping suppliers.",
        "customer_tip": "Say: 'Our Should-Cost RFQ Agent reads 100-page engineering PDFs, parses CAD specs, and drafts autonomous supplier bid comparisons in minutes.'"
    },
    {
        "term": "Should-Cost Model",
        "full": "Bottom-Up Parametric Cost Breakdown",
        "cat": "sourcing",
        "top20": True,
        "hook": "Calculating what a supplier SHOULD charge based on raw material commodity indices, machine cycle times, and labor rates.",
        "plain": "Instead of accepting a supplier's quote of $42 per part, procurement engineers break down: $18 raw aluminum (LME price) + $8 CNC machining time + $4 labor + $3 scrap allowance + 15% fair margin = $37.95 fair should-cost.",
        "example": "Arming buyers with should-cost models prevents suppliers from price-gouging during supply disruptions.",
        "customer_tip": "Show: RFQ Should-Cost Agent (`rfq_should_cost_agent`) running real-time London Metal Exchange commodity index price indexing."
    },
    {
        "term": "Tier-1 vs Tier-N",
        "full": "Direct Suppliers vs Sub-Tier Multi-Echelon Suppliers",
        "cat": "sourcing",
        "top20": True,
        "hook": "The suppliers you write checks to (Tier-1) vs the hidden suppliers who sell to THEM (Tier-2, Tier-3, Tier-N).",
        "plain": "A carmaker buys finished headlights from a Tier-1 supplier. But that Tier-1 supplier buys LED microchips from a Tier-2 supplier, who buys silicon wafers from a Tier-3 foundry in Taiwan. A fire at the Tier-3 foundry stops the carmaker's entire assembly line!",
        "example": "The 2021 automotive chip crisis occurred because Tier-1 seat and braking vendors all relied on the same single Tier-3 semiconductor fab.",
        "customer_tip": "Say: 'Our Tier-N Risk Sentinel uses Cloud Spanner Graph to map hidden diamond dependencies across your multi-tier supply chain.'"
    },
    {
        "term": "PO & PR",
        "full": "Purchase Order & Purchase Requisition",
        "cat": "sourcing",
        "top20": False,
        "hook": "Internal request to buy goods (PR) vs the binding legal contract sent to the supplier (PO).",
        "plain": "An engineer submits an internal Purchase Requisition in SAP. Once approved by management, procurement converts it into a legally binding Purchase Order sent to the vendor.",
        "example": "A PO states exact payment terms (e.g. Net 60), quantity, unit price, delivery destination, and Incoterms (e.g. FOB Shanghai).",
        "customer_tip": "Highlight how our agents automate 3-way invoice matching against SAP EKKO/EKPO purchase order tables."
    },
    {
        "term": "3-Way Matching",
        "full": "PO vs Goods Receipt vs Vendor Invoice Reconciliation",
        "cat": "sourcing",
        "top20": True,
        "hook": "The audit rule preventing companies from paying for goods they never received or at wrong prices.",
        "plain": "Accounts Payable checks three documents before releasing cash: 1. The Purchase Order (what we agreed to pay), 2. The Goods Receipt (what the warehouse actually scanned at the dock), and 3. The Vendor Invoice (what the supplier billed). If all three match, payment is released.",
        "example": "If the PO was for 100 units at $10 ($1,000), but the warehouse only received 80 units and the invoice bills for 100, the system blocks payment until corrected.",
        "customer_tip": "Show: Autonomous 3-Way Invoice Reconciliation Agent preventing leakage on freight and vendor billing disputes."
    },
    {
        "term": "Incoterms",
        "full": "International Commercial Terms (FOB, CIF, DDP, EXW)",
        "cat": "sourcing",
        "top20": True,
        "hook": "The standardized global rules defining exactly when freight cost and cargo loss risk transfer from seller to buyer.",
        "plain": "EXW (Ex Works): Buyer picks up goods at supplier's factory door and pays all freight and customs. FOB (Free on Board): Supplier loads boxes onto the ship at the port; buyer pays ocean freight. DDP (Delivered Duty Paid): Supplier delivers all the way to buyer's warehouse with all tariffs paid.",
        "example": "If a cargo container falls into the Pacific Ocean under FOB terms, the loss is the buyer's responsibility. Under DDP terms, it is the supplier's responsibility.",
        "customer_tip": "Say: 'Our Contract Intelligence Agent parses Incoterms from 80-page contracts to verify tariff liability and insurance coverage.'"
    },
    {
        "term": "CoWoS",
        "full": "Chip-on-Wafer-on-Substrate Advanced Packaging",
        "cat": "sourcing",
        "top20": True,
        "hook": "The specialized manufacturing bottleneck packaging AI accelerator compute dies with High-Bandwidth Memory (HBM).",
        "plain": "Used by TSMC to build Google TPUs and NVIDIA GPUs. Even if silicon wafer fabrication is finished, AI chips cannot ship without CoWoS packaging capacity, making it a critical multi-quarter supply bottleneck.",
        "example": "Alphabet's TPU supply planning team models CoWoS packaging allocation 12-18 months in advance to ensure data center AI cluster rollouts stay on schedule.",
        "customer_tip": "Say: 'This is the exact advanced semiconductor supply chain dynamic Kiran highlighted regarding Alphabet's internal TPU planning.'"
    },
    {
        "term": "e-Choupal",
        "full": "Rural Farmgate Digital Procurement Network (ITC)",
        "cat": "sourcing",
        "top20": True,
        "hook": "ITC's pioneering digital network connecting over 4 million Indian farmers directly to procurement centers.",
        "plain": "e-Choupal places internet kiosks in rural villages, allowing farmers to check real-time crop market prices and sell agricultural produce (wheat, soybean, leaf tobacco) directly to ITC collection hubs, bypassing middlemen.",
        "example": "In tobacco and agri-sourcing, e-Choupal feeds daily harvest volume, leaf moisture, and grade quality data directly into ITC supply planning systems.",
        "customer_tip": "Say: 'When building ITC's AI Control Tower, ingesting e-Choupal farmgate village procurement feeds is step one for raw material visibility.'"
    },
    {
        "term": "Dual Sourcing",
        "full": "Splitting Procurement Volumes Across Multiple Vendors",
        "cat": "sourcing",
        "top20": False,
        "hook": "Buying critical parts from two different suppliers so a fire or strike at one doesn't shut down your company.",
        "plain": "A company awards 70% of volume to their lowest-cost primary vendor and 30% to a secondary supplier in a different geographic region as risk insurance.",
        "example": "Apple dual-sources display screens from Samsung and LG to maintain bargaining leverage and protect against factory outages.",
        "customer_tip": "Show: Tier-N Risk Sentinel dynamically re-weighting allocation splits when geopolitical or weather risks escalate."
    },
    {
        "term": "BOM",
        "full": "Bill of Materials",
        "cat": "sourcing",
        "top20": False,
        "hook": "The complete recipe of every screw, circuit board, and label needed to build one finished product.",
        "plain": "Just like a cake recipe lists flour, sugar, and eggs, an engineering BOM lists all sub-assemblies, part numbers, and raw materials needed to manufacture one unit.",
        "example": "An electric vehicle BOM contains over 10,000 distinct components. If even one $0.05 bolt is missing, the vehicle cannot be driven off the assembly line.",
        "customer_tip": "Explain how our agents scan engineering BOM revisions in SAP to automatically alert procurement of obsolete parts."
    },
    {
        "term": "Tail Spend",
        "full": "Unmanaged Low-Value Indirect Purchases",
        "cat": "sourcing",
        "top20": False,
        "hook": "The 80% of corporate purchase orders that account for only 20% of dollar spend but consume enormous buyer time.",
        "plain": "Routine office supplies, lab consumables, maintenance lubricants, and replacement drill bits. Because individual costs are low, companies rarely negotiate contracts, leading to 15-25% price inflation.",
        "example": "An autonomous AI procurement agent scans unmanaged tail spend POs and consolidates 500 rogue office supply orders into 1 negotiated bulk contract.",
        "customer_tip": "Say: 'Our Autonomous Sourcing Agent reviews uncontracted tail-spend invoices to automatically capture 8-12% in instant cash savings.'"
    },
    {
        "term": "Supplier Scorecard",
        "full": "Periodic Vendor Performance Evaluation",
        "cat": "sourcing",
        "top20": False,
        "hook": "Grading suppliers quarterly on On-Time Delivery, Defect PPM, Cost Savings, and ESG Compliance.",
        "plain": "Suppliers receiving an 'A' grade earn preferred bidding status on new programs, while 'C' grade suppliers must submit corrective action plans or face disqualification.",
        "example": "A vendor with 99% on-time delivery but 450 Parts-Per-Million defect rate is flagged by our Supplier Quality Sentinel for automated debit memos.",
        "customer_tip": "Show: Supplier Quality Sentinel (`supplier_quality_sentinel`) automating non-conformance debits in SAP QM."
    },

    # --- MANUFACTURING & OPERATIONS (10 cards) ---
    {
        "term": "OEE",
        "full": "Overall Equipment Effectiveness",
        "cat": "manufacturing",
        "top20": True,
        "hook": "The gold-standard factory KPI measuring how close your machines ran to perfect productive capacity.",
        "plain": "OEE multiplies three factors: Availability (did the machine run without breakdowns?) × Performance (did it run at top speed?) × Quality (how many parts passed inspection without defects?).",
        "example": "90% machine uptime × 85% operating speed × 98% defect-free parts = 74.97% OEE. World-class factories aim for >85% OEE.",
        "customer_tip": "Say: 'Our AssetGuard agent predicts spindle bearing failures 48 hours before breakdown, elevating plant OEE by +4.8%.'"
    },
    {
        "term": "MES",
        "full": "Manufacturing Execution System (e.g. Siemens Opcenter)",
        "cat": "manufacturing",
        "top20": True,
        "hook": "The real-time computer system controlling shop-floor machines, line operators, and work-in-progress pallets.",
        "plain": "While ERP plans what products to build next week, MES tracks what is happening on the factory floor right now: barcode scans, machine cycle times, tool temperatures, and batch quality checks.",
        "example": "In an automotive plant, MES tells robotic arms which paint color to spray on the chassis moving down the conveyor belt.",
        "customer_tip": "Explain: 'Our agents ingest MES telemetry streams directly into BigQuery to detect yield anomalies before entire batches are ruined.'"
    },
    {
        "term": "ICML",
        "full": "Integrated Consumer Goods Manufacturing & Logistics (ITC)",
        "cat": "manufacturing",
        "top20": True,
        "hook": "ITC's mega-scale co-located manufacturing and automated distribution campuses across India.",
        "plain": "Rather than manufacturing biscuits or snacks in one city and trucking them to a separate warehouse miles away, ITC co-locates high-speed production lines with automated high-bay warehouses under one roof.",
        "example": "ITC operates over 20 state-of-the-art ICML campuses (e.g. Kapurthala, Mysuru, Uluberia) to minimize inter-facility freight handling and maximize freshness.",
        "customer_tip": "Say: 'In the ITC Control Tower scenario, scheduling ICML production lines in tandem with CFA buffer stock needs is essential.'"
    },
    {
        "term": "Changeover / SMED",
        "full": "Single-Minute Exchange of Die (Tooling Switch Time)",
        "cat": "manufacturing",
        "top20": False,
        "hook": "The time wasted stopping a factory line to swap molds, clean tanks, or re-tool for a different product.",
        "plain": "When a bottling plant finishes filling Diet Lemon and switches to Cherry Cola, they must flush piping, swap bottle labels, and recalibrate fill nozzles. That downtime produces zero revenue.",
        "example": "Sequencing production jobs with similar bottle shapes and light-to-dark colors cuts daily changeover downtime from 4 hours down to 45 minutes.",
        "customer_tip": "Show: Line Schedule Optimizer (`line_schedule_optimizer`) using Google OR-Tools to solve the Traveling Salesperson changeover sequence."
    },
    {
        "term": "WIP",
        "full": "Work in Progress",
        "cat": "manufacturing",
        "top20": False,
        "hook": "Partially finished inventory sitting on the factory floor waiting for the next machine step.",
        "plain": "Automobile chassis with engines installed but awaiting windshields and seats. High WIP ties up millions in working capital and clutters the factory floor.",
        "example": "Implementing Lean Kanban pull systems reduced plant WIP inventory from $14M down to $3.8M in 60 days.",
        "customer_tip": "Say: 'Excess WIP is a warning sign of shop-floor machine bottlenecks. Our finite production scheduler smooths line flows.'"
    },
    {
        "term": "PPM Defect Rate",
        "full": "Parts Per Million Quality Defect Metric",
        "cat": "manufacturing",
        "top20": False,
        "hook": "The number of defective items produced for every one million units manufactured.",
        "plain": "In semiconductor fabrication and medical devices, a 1% defect rate (10,000 PPM) is catastrophic. Six Sigma quality standards target less than 3.4 defects per million parts produced.",
        "example": "A micro-fracture defect rate of 25 PPM on vial seals saves a pharmaceutical company $8M in potential batch recalls.",
        "customer_tip": "Show: Inline Quality Inspection Agent (`inline_quality_inspection_agent`) using Gemini 3.8 Flash multimodal vision at 60 frames/sec."
    },
    {
        "term": "MRP",
        "full": "Material Requirements Planning",
        "cat": "manufacturing",
        "top20": False,
        "hook": "The core ERP calculation exploding finished goods forecasts into raw material purchase schedules.",
        "plain": "If the factory plan calls for 1,000 bicycles next month, MRP explodes the BOM: 1,000 frames + 2,000 wheels + 1,000 chains. It subtracts current inventory on hand and schedules PO release dates based on supplier lead times.",
        "example": "When MRP runs overnight in SAP, it generates hundreds of automated purchase requisitions for procurement buyers.",
        "customer_tip": "Say: 'Legacy MRP assumes static lead times. Our Master Data Lead Time Steward updates dynamic lead times so MRP orders on time.'"
    },
    {
        "term": "Lean & Kanban",
        "full": "Pull-Based Visual Inventory Replenishment",
        "cat": "manufacturing",
        "top20": False,
        "hook": "Toyota's manufacturing philosophy: Never produce anything until the downstream station signals demand.",
        "plain": "Instead of pushing finished goods into a warehouse based on guesses, downstream assembly bins use physical or electronic Kanban cards to pull replacement parts only when consumed.",
        "example": "An electronic Kanban card automatically triggers an automated guided vehicle (AGV) to deliver 50 screws to workstation #4.",
        "customer_tip": "Connect Kanban pull mechanisms to real-time e-Choupal and CFA replenishment loops."
    },
    {
        "term": "Cycle Time vs Takt Time",
        "full": "Machine Processing Speed vs Customer Demand Pace",
        "cat": "manufacturing",
        "top20": False,
        "hook": "How fast your machine actually builds one unit vs how fast customers buy one unit.",
        "plain": "Takt Time is the required heartbeat: available production minutes divided by customer order units. Cycle Time is how long a specific machine takes to complete its cycle. If Cycle Time > Takt Time, the factory falls behind schedule.",
        "example": "If customers buy 1 unit every 60 seconds (Takt Time), but packaging takes 75 seconds (Cycle Time), you will create customer backorders unless you add a second line.",
        "customer_tip": "Show how OR-Tools line balancing synchronizes station cycle times to match customer Takt time."
    },
    {
        "term": "Bottleneck / Constraint",
        "full": "The Slowest Process Limiting Total Factory Output",
        "cat": "manufacturing",
        "top20": False,
        "hook": "Goldratt's Theory of Constraints: A factory can never produce faster than its slowest bottleneck machine.",
        "plain": "If Stamping produces 100 parts/hr, Welding handles 80 parts/hr, and Painting only handles 40 parts/hr, total factory output is strictly 40 parts/hr. Speeding up Stamping only creates excess WIP piles!",
        "example": "Focusing predictive maintenance on the paint cure oven unlocked 15% extra plant throughput without buying new machinery.",
        "customer_tip": "Say: 'Our agents pinpoint the true constraint station and protect its uptime with prioritized buffer stock.'"
    },

    # --- INVENTORY & WAREHOUSING (12 cards) ---
    {
        "term": "MEIO",
        "full": "Multi-Echelon Inventory Optimization",
        "cat": "inventory",
        "top20": True,
        "hook": "Calculating the mathematical sweet-spot for where to hold safety stock across factories, central hubs, and city depots.",
        "plain": "Should you hold inventory at central factories, regional distribution centers, or local retail stores? MEIO calculates the total network balance using Clark-Scarf equations to minimize total working capital while guaranteeing 99% customer availability.",
        "example": "Pushing buffer stock back to central RDCs while keeping lean local stock at retail depots cuts total inventory holding costs by 22%.",
        "customer_tip": "Show: Echelon Inventory Allocator (`echelon_inventory_allocator`) balancing multi-tier stock pools."
    },
    {
        "term": "WMS",
        "full": "Warehouse Management System (e.g. Manhattan, Blue Yonder)",
        "cat": "inventory",
        "top20": True,
        "hook": "The software orchestrating forklift drivers, pallet barcode scanning, picking waves, and bin storage racks.",
        "plain": "When boxes arrive at a warehouse, WMS directs forklift operators which aisle and rack shelf to store pallets in. When customer orders arrive, WMS batches items into optimal walking paths for order pickers.",
        "example": "Manhattan Associates WMS sends RF scanner tasks to pickers: 'Go to Aisle 14, Rack B, Bin Level 3, pick 4 cases.'",
        "customer_tip": "Say: 'Our Warehouse Slotting Optimizer writes optimized bin storage coordinates directly back into Manhattan WMS via REST APIs.'"
    },
    {
        "term": "CFA",
        "full": "Carrying & Forwarding Agent / Depot (ITC / FMCG)",
        "cat": "inventory",
        "top20": True,
        "hook": "State-level master distribution warehouses in India managing regional stock and local distributor dispatches.",
        "plain": "In Indian FMCG distribution, companies like ITC ship full truckloads from ICML factories to state-level CFAs. CFAs handle warehousing, tax compliance, invoicing, and breaking bulk for local city distributors and wholesalers.",
        "example": "ITC maintains over 50 CFA regional hubs across India ensuring consumer goods reach retail kirana stores within 24 to 48 hours.",
        "customer_tip": "Say: 'In the ITC Control Tower, monitoring CFA buffer stock days-of-cover prevents state-wide market stockouts during transport disruptions.'"
    },
    {
        "term": "LPN",
        "full": "License Plate Number",
        "cat": "inventory",
        "top20": True,
        "hook": "The master barcode tracking an entire pallet containing dozens of mixed product cases.",
        "plain": "Instead of scanning 80 individual boxes of shampoo on a wooden pallet, workers scan one single LPN barcode on the pallet shrink-wrap. The WMS instantly knows all 80 SKUs, batch lot numbers, and expiration dates on that pallet.",
        "example": "Scanning an LPN at the receiving dock inward-registers 120 cases into inventory in under 2 seconds.",
        "customer_tip": "Highlight how our Yard & Dock Sequencer links trailer RFID scans to incoming pallet LPN manifests."
    },
    {
        "term": "AS/RS",
        "full": "Automated Storage and Retrieval System",
        "cat": "inventory",
        "top20": False,
        "hook": "High-bay robotic cranes and autonomous shuttles retrieving pallet racks without human forklift drivers.",
        "plain": "Modern automated warehouses use 100-foot tall robotic cranes operating in dark, climate-controlled narrow aisles to store and retrieve pallets with millimeter precision.",
        "example": "ITC's ICML automated high-bay warehouses utilize AS/RS cranes to handle thousands of pallet moves per hour with zero product damage.",
        "customer_tip": "Explain how our agents sequence order picking waves to maximize AS/RS crane travel efficiency."
    },
    {
        "term": "Slotting",
        "full": "Warehouse Shelf Placement Optimization",
        "cat": "inventory",
        "top20": False,
        "hook": "Placing best-selling fast-moving items right next to the packing dock to minimize picker walking distance.",
        "plain": "If 20% of your SKUs generate 80% of daily orders, storing those fast-moving items near the shipping door saves forklift operators miles of walking every shift.",
        "example": "Dynamic re-slotting of seasonal sunscreen before summer cut daily warehouse picker transit travel by 34%.",
        "customer_tip": "Show: Warehouse Slotting Optimizer (`warehouse_slotting_optimizer`) generating 3D heatmaps of warehouse pick traffic."
    },
    {
        "term": "Cross-Docking",
        "full": "Direct Inbound-to-Outbound Pallet Transfer Without Storage",
        "cat": "inventory",
        "top20": True,
        "hook": "Unloading boxes from an incoming supplier truck and loading them directly onto an outbound store truck without putting them on warehouse shelves.",
        "plain": "Boxes never sit in storage racks. They spend less than 4 hours on the staging dock before departing for regional retail stores. Eliminates warehouse holding costs and double-handling labor.",
        "example": "Walmart distribution centers cross-dock thousands of pallets daily: supplier trailers arrive at inbound docks, pallets are sorted across conveyor belts, and loaded onto store trailers in under 90 minutes.",
        "customer_tip": "Show: Cross-Dock Transfer Orchestrator (`crossdock_transfer_orchestrator`) matching inbound ASNs with outbound trailer schedules."
    },
    {
        "term": "SLOB",
        "full": "Slow-Moving & Obsolete Inventory",
        "cat": "inventory",
        "top20": True,
        "hook": "Dead inventory sitting on warehouse shelves gathering dust and burning corporate cash.",
        "plain": "Products that have not sold in 180 days. They tie up working capital, consume warehouse storage space, and risk total write-offs due to shelf-life expiration or technological obsolescence.",
        "example": "A consumer electronics brand identified $18M in obsolete phone cases and ran an automated clearance liquidation campaign, freeing up $12M in operating cash.",
        "customer_tip": "Show: SLOB Disposition & Liquidation Agent identifying aging inventory tiers and routing discount salvage bids."
    },
    {
        "term": "Days of Inventory (DOH / DIO)",
        "full": "Days on Hand / Days Inventory Outstanding",
        "cat": "inventory",
        "top20": True,
        "hook": "How many days your company could continue selling if all suppliers stopped shipping tomorrow.",
        "plain": "Calculated as: (Total Inventory Value ÷ Daily Cost of Goods Sold). If you hold $30M in inventory and sell $1M per day, you have 30 Days of Inventory on Hand.",
        "example": "Cutting DIO from 45 days down to 34 days without lowering customer fill rate unlocked $28M in free cash flow for a consumer goods client.",
        "customer_tip": "Say: 'Our Working Capital Cash Bridge agent visualizes exact DIO cash unlock opportunities across business units.'"
    },
    {
        "term": "Inventory Turns",
        "full": "Annual Velocity of Inventory Sold & Replaced",
        "cat": "inventory",
        "top20": False,
        "hook": "How many times per year your entire warehouse inventory is sold and completely replenished.",
        "plain": "Calculated as: (Annual COGS ÷ Average Inventory). Higher is better. A grocery store turns inventory 20 times a year (fresh milk and produce). An aerospace equipment company might turn inventory only 2 times a year.",
        "example": "Increasing inventory turns from 4x to 6x frees up 33% of working capital tied up in warehouses.",
        "customer_tip": "Connect inventory turns to Working Capital Cash Bridge (`working_capital_cash_bridge`) metrics."
    },
    {
        "term": "Cycle Counting",
        "full": "Continuous Partial Inventory Auditing",
        "cat": "inventory",
        "top20": False,
        "hook": "Counting a small sample of warehouse bins every day instead of shutting down the entire warehouse once a year for annual audit.",
        "plain": "Auditors count high-value 'A' items monthly and low-value 'C' items quarterly. Keeps ERP inventory accuracy above 99.5% without disrupting operations.",
        "example": "Robotic warehouse drones scan high-bay barcode tags overnight, automatically reconciling physical counts with ERP stock tables.",
        "customer_tip": "Explain how our agents ingest drone scan telemetry to resolve phantom inventory discrepancies in SAP."
    },
    {
        "term": "FIFO vs FEFO",
        "full": "First In First Out vs First Expired First Out",
        "cat": "inventory",
        "top20": False,
        "hook": "Picking older inventory first (FIFO) vs picking closest-to-expiration inventory first (FEFO).",
        "plain": "In food, beverage, and pharmaceuticals, FEFO is mandatory. Even if a pallet arrived yesterday, if its expiration date is in 30 days, it must be shipped before older pallets that expire in 90 days to prevent product spoilage.",
        "example": "ITC's food distribution uses strict FEFO rules for dairy and biscuits to ensure freshness on retail store shelves.",
        "customer_tip": "Highlight: Expiration & Spoilage Prevention Agent using FEFO logic to prevent $3.4M in expired inventory write-offs."
    },

    # --- LOGISTICS & TRANSPORTATION (14 cards) ---
    {
        "term": "TMS",
        "full": "Transportation Management System (e.g. Oracle OTM, SAP TM)",
        "cat": "logistics",
        "top20": True,
        "hook": "The software booking freight carriers, rating shipping lanes, tracking shipments, and auditing freight invoices.",
        "plain": "When warehouses pack customer orders, TMS selects the lowest-cost freight carrier, consolidates shipments into full truckloads, tenders loads to trucking companies, and tracks delivery status.",
        "example": "Oracle OTM automatically tenders 200 truck loads daily to pre-contracted carriers based on lowest freight rate and service reliability score.",
        "customer_tip": "Say: 'Our FleetFlow and Mode Shift agents connect to Oracle OTM and SAP TM to optimize carrier tendering and load consolidation.'"
    },
    {
        "term": "AIS",
        "full": "Automatic Identification System (Maritime Vessel Tracking)",
        "cat": "logistics",
        "top20": True,
        "hook": "Satellite transponders broadcasting real-time GPS coordinates, speed, and heading of ocean container ships.",
        "plain": "Every commercial ocean vessel transmits AIS signals to orbital satellites (like Spire or exactEarth). Allows companies to track exactly where their shipping containers are in the middle of the Pacific Ocean.",
        "example": "AIS telemetry detected a container ship slowing to 4 knots outside the Suez Canal, allowing our War Room agent to alert supply chain teams 6 days before factory lines ran out of parts.",
        "customer_tip": "Say: 'Our Disruption War Room ingests live Spire satellite AIS feeds to recalculate ocean container ETAs in real time.'"
    },
    {
        "term": "ADS-B",
        "full": "Automatic Dependent Surveillance-Broadcast (Air Cargo)",
        "cat": "logistics",
        "top20": True,
        "hook": "Aircraft transponders broadcasting live flight GPS altitude, speed, and ETA for air freight shipments.",
        "plain": "Just as AIS tracks ocean vessels, ADS-B satellite receivers (like FlightAware) track cargo planes carrying high-value electronics and temperature-sensitive pharmaceuticals across continents.",
        "example": "Tracking an air charter flight carrying urgently needed semiconductor wafers from Frankfurt to Chicago to schedule customs clearance.",
        "customer_tip": "Show: AeroFreight Air Cargo Optimizer (`air_cargo_uld_optimizer`) monitoring live flight arrivals."
    },
    {
        "term": "ELD & Telematics",
        "full": "Electronic Logging Device & Truck GPS Telematics (e.g. Samsara)",
        "cat": "logistics",
        "top20": True,
        "hook": "In-cab GPS devices tracking real-time truck position, engine health, and driver Hours of Service.",
        "plain": "Mandatory devices installed in commercial truck cabs that transmit vehicle speed, GPS location, reefer trailer temperature, and driver rest break compliance to cloud servers every 30 seconds.",
        "example": "Samsara ELD alerts dispatchers when a refrigerated trailer carrying ice cream warms above -10°F or when a driver is 15 minutes away from mandatory rest.",
        "customer_tip": "Say: 'Our FleetFlow agent ingests Samsara ELD telematics to re-route trucks around traffic accidents and manage dock appointments.'"
    },
    {
        "term": "EDI 214 & 856",
        "full": "Transportation Status (214) & Advance Ship Notice (ASN / 856)",
        "cat": "logistics",
        "top20": True,
        "hook": "The universal B2B digital data standards used by trucking companies and suppliers to confirm shipments.",
        "plain": "EDI 856 (ASN): Supplier transmits an electronic packing slip before the truck departs, listing exact pallet LPNs and serial numbers. EDI 214: Carrier transmits automated milestone updates (Picked Up, In Transit, Delivered).",
        "example": "When a truck crosses the warehouse geofence, an automated EDI 214 triggers dock door assignment in the WMS.",
        "customer_tip": "Highlight how our agents ingest legacy EDI 214/856 feeds and convert them into clean real-time BigQuery events."
    },
    {
        "term": "FTL vs LTL",
        "full": "Full Truckload vs Less-Than-Truckload",
        "cat": "logistics",
        "top20": True,
        "hook": "Renting an entire 53-foot semi-truck for yourself vs sharing trailer space with other companies' boxes.",
        "plain": "FTL (Full Truckload): You rent the entire trailer (up to 44,000 lbs or 26 pallets) directly from origin to destination without stops. LTL (Less-Than-Truckload): You only ship 4 pallets, so carrier consolidates your freight with cargo from 6 other companies through regional hub-and-spoke terminals.",
        "example": "Consolidating 5 separate LTL shipments into 1 full truckload cuts freight freight cost by 38% and avoids pallet transit damage.",
        "customer_tip": "Show: Load Consolidation 3D Studio (`load_consolidation_agent`) grouping orders into multi-drop FTL runs."
    },
    {
        "term": "Intermodal Rail",
        "full": "Moving Shipping Containers by Train + Short Truck Drayage",
        "cat": "logistics",
        "top20": False,
        "hook": "Putting 200 shipping containers on one freight train for long-distance transit instead of hiring 200 separate diesel trucks.",
        "plain": "A truck drives 30 miles from factory to the rail ramp (drayage). The container travels 1,500 miles across the continent on a double-stack rail train (4x more fuel-efficient than trucking). A local truck delivers the final 20 miles to the warehouse.",
        "example": "Moving cross-country freight from Long Beach to Chicago via BNSF rail saves $850 per container and cuts Scope 3 carbon emissions by 65%.",
        "customer_tip": "Show: Intermodal Rail Linehaul Agent (`intermodal_rail_linehaul_agent`) tracking Railinc EDI 404/417 train events."
    },
    {
        "term": "Demurrage & Detention",
        "full": "Late Penalties for Holding Shipping Containers",
        "cat": "logistics",
        "top20": True,
        "hook": "Expensive daily fines ($150–$400/day) charged by shipping lines when containers sit too long at ports or warehouses.",
        "plain": "Demurrage: Penalty paid when full import containers sit inside the ocean port terminal past free storage days. Detention: Penalty paid when you keep the shipping container at your private warehouse too long before returning the empty box to the port.",
        "example": "During port congestion, a Fortune 500 retailer incurred $14M in unexpected container demurrage penalties in a single quarter.",
        "customer_tip": "Say: 'Our Port Drayage Orchestrator tracks container free-time clocks to prioritize customs gate-outs before daily penalties trigger.'"
    },
    {
        "term": "3PL vs 4PL",
        "full": "Third-Party vs Fourth-Party Logistics Provider",
        "cat": "logistics",
        "top20": False,
        "hook": "Hiring a logistics company with trucks and warehouses (3PL) vs hiring an orchestrator to manage ALL your 3PLs (4PL).",
        "plain": "3PL (e.g. DHL, FedEx Supply Chain, Ryder): Owns or leases physical trucks and warehouses to handle shipping and fulfillment. 4PL (e.g. Kuehne+Nagel Integrated Logistics): Acts as a strategic master orchestrator, designing the entire network and managing multiple 3PL carriers.",
        "example": "A global electronics brand uses a 4PL to coordinate 12 regional 3PL logistics providers across 40 countries.",
        "customer_tip": "Say: 'Our Agentic Control Tower acts as an autonomous digital 4PL, governing all your 3PL carriers from one single glass pane.'"
    },
    {
        "term": "Drayage",
        "full": "Short-Distance Truck Hauling Between Ports & Rail Hubs",
        "cat": "logistics",
        "top20": False,
        "hook": "The short truck trip moving an ocean shipping container from the marine port dock to a nearby local warehouse or rail ramp.",
        "plain": "Drayage trucks specialize in short-haul round trips: queuing at port gates, picking up heavy ocean shipping containers, clearing port security, and delivering to nearby cross-docks.",
        "example": "A drayage driver picks up an ocean container at the Port of Los Angeles and delivers it to an Ontario, California distribution center 45 miles away.",
        "customer_tip": "Show: Port Drayage Orchestrator (`port_drayage_orchestrator`) coordinating terminal appointment slots."
    },
    {
        "term": "Deadhead Miles",
        "full": "Empty Truck Driving Miles Producing Zero Revenue",
        "cat": "logistics",
        "top20": False,
        "hook": "The wasted miles a truck drives empty after delivering a load, burning expensive diesel without making money.",
        "plain": "A truck delivers a load of paper goods from Atlanta to Miami, but cannot find a paying return load from Miami back to Atlanta. Driving those 660 miles empty is called deadheading.",
        "example": "US trucking fleets average 15% to 20% deadhead miles. Pairing outbound shipments with return backhauls saves millions in operating costs.",
        "customer_tip": "Show: FleetFlow Route & Dispatch Optimizer (`fleetflow_dispatch`) matching regional return backhauls."
    },
    {
        "term": "Reefer",
        "full": "Refrigerated Cargo Container or Trailer",
        "cat": "logistics",
        "top20": False,
        "hook": "A temperature-controlled freight trailer or ocean container keeping ice cream, meat, or medicines cold during transit.",
        "plain": "Reefer trailers feature built-in diesel refrigeration units maintaining temperatures anywhere from -20°F (frozen ice cream) to +38°F (fresh produce).",
        "example": "Cold-chain pharmaceutical vaccines require continuous real-time IoT temperature logging. If the reefer warms above 4°C for 2 hours, the entire $2M batch must be destroyed.",
        "customer_tip": "Highlight how our IoT Telematics Sentinel monitors reefer temperature logs and triggers automated route alerts."
    },
    {
        "term": "Last-Mile Delivery",
        "full": "Final Transport Leg from Local Depot to Customer Doorstep",
        "cat": "logistics",
        "top20": False,
        "hook": "The final, most expensive leg of the journey delivering a package from local city hub to a home or store shelf.",
        "plain": "Last-mile delivery accounts for up to 53% of total shipping cost due to urban traffic congestion, missed delivery attempts, multiple stops, and individual parcel handling.",
        "example": "Route optimization algorithms sequencing 120 delivery van stops per day save 1.5 hours of driver overtime and 4 gallons of fuel per van.",
        "customer_tip": "Show: Google Maps Platform Routes Preferred integration inside FleetFlow route dispatch."
    },
    {
        "term": "Milk Run",
        "full": "Multi-Stop Scheduled Collection & Delivery Circuit",
        "cat": "logistics",
        "top20": False,
        "hook": "A single truck driving a daily scheduled loop to collect small shipments from 5 suppliers and deliver them to 1 factory.",
        "plain": "Originating from daily dairy milk pickups. Instead of 5 suppliers each sending separate half-empty trucks to an assembly plant, 1 truck drives a scheduled circuit picking up pallets from each supplier.",
        "example": "An automotive assembly plant runs 4 daily milk-run trucks across local stamping and seating suppliers, cutting plant receiving dock congestion by 70%.",
        "customer_tip": "Show: Load Consolidation Agent solving multi-stop Milk Run vehicle routing with time windows."
    },

    # --- ENTERPRISE TECH, SYSTEMS & ESG (10 cards) ---
    {
        "term": "ERP",
        "full": "Enterprise Resource Planning (e.g. SAP S/4HANA)",
        "cat": "tech",
        "top20": True,
        "hook": "The central corporate system of record managing accounting ledgers, purchase orders, customer orders, and inventory balances.",
        "plain": "The central nervous system of an enterprise. Every time a customer places an order, a factory receives raw materials, or an invoice is paid, SAP S/4HANA records the master financial and material transaction.",
        "example": "Core SAP database tables: MARA (Material Master), VBAK (Sales Orders), EKKO (Purchase Orders), and MSEG (Inventory Movements).",
        "customer_tip": "Say: 'Our agents connect directly to SAP S/4HANA via certified OData and BAPI connectors to read tables and write validated transactions.'"
    },
    {
        "term": "Google OR-Tools",
        "full": "Google Operations Research Optimization Suite",
        "cat": "tech",
        "top20": True,
        "hook": "Google's open-source mathematical solver for vehicle routing, bin packing, and constraint optimization.",
        "plain": "When an agent needs to calculate the mathematical optimum among billions of possible delivery routes, factory line schedules, or 3D pallet configurations, it formulates the problem and hands it to Google OR-Tools to solve in milliseconds.",
        "example": "Solving a 250-stop Vehicle Routing Problem with Time Windows (VRPTW) takes less than 2 seconds with OR-Tools.",
        "customer_tip": "Say: 'We combine Gemini's reasoning with Google OR-Tools' mathematical solvers to deliver mathematically proven optimal solutions.'"
    },
    {
        "term": "WeatherNext",
        "full": "Google DeepMind AI-Powered Global Weather Forecasting",
        "cat": "tech",
        "top20": True,
        "hook": "DeepMind's neural weather foundation model predicting typhoons, extreme storms, and climate risks 10-15 days in advance.",
        "plain": "Traditional numerical weather models take hours on supercomputers. DeepMind's GraphCast and WeatherNext foundation models predict global storm paths and monsoon disruptions in minutes with higher spatial precision.",
        "example": "WeatherNext predicted Typhoon Kong-rey's maritime impact path 9 days early, allowing shipping lines to re-route ocean vessels around the storm.",
        "customer_tip": "Say: 'Our Disruption War Room integrates Google DeepMind WeatherNext to forecast climate disruptions across transport corridors.'"
    },
    {
        "term": "Carbon-Aware Compute",
        "full": "Matching Compute Workloads with Clean Renewable Power",
        "cat": "tech",
        "top20": False,
        "hook": "Google's internal system shifting data center computing tasks to regions where solar and wind energy are abundant.",
        "plain": "When the sun is shining in California and the wind is blowing in Iowa, non-urgent data center computing jobs (like model training or batch backups) are automatically routed to those regions to minimize carbon emissions.",
        "example": "Alphabet shifts heavy AI model training workloads across its global data center fleet to maximize 24/7 carbon-free energy utilization.",
        "customer_tip": "Say: 'This is another key internal supply chain innovation Kiran highlighted regarding Alphabet's sustainable infrastructure.'"
    },
    {
        "term": "OTIF",
        "full": "On-Time In-Full Customer Delivery Compliance",
        "cat": "tech",
        "top20": True,
        "hook": "The unforgiving retail delivery metric: Orders must arrive exactly on the scheduled day, with 100% of ordered boxes, or face heavy fines.",
        "plain": "If Walmart orders 1,000 cases to arrive on Tuesday, and you deliver 950 cases on Tuesday (incomplete) or 1,000 cases on Wednesday (late), the delivery fails OTIF. Retailers deduct 3% of the total purchase order value as a penalty fee!",
        "example": "A food brand was losing $4.2M annually in Walmart and Target OTIF fines. Our OTIF Penalty Shield predicted late shipments 48 hours early and triggered priority hot-shot deliveries to protect compliance.",
        "customer_tip": "Show: OTIF Penalty Shield (`otif_penalty_shield`) predicting delivery compliance risk before trailers leave the yard."
    },
    {
        "term": "RMA",
        "full": "Return Merchandise Authorization",
        "cat": "tech",
        "top20": False,
        "hook": "The formal tracking number issued before a customer can ship a damaged or unwanted item back for refund.",
        "plain": "Reverse logistics process: Customer requests a return, system validates warranty eligibility, generates an RMA barcode label, and directs the package to a return triage center for testing or refurbishment.",
        "example": "Processing 50,000 e-commerce returns per month without an automated RMA grading triage creates massive warehouse bottlenecks.",
        "customer_tip": "Show: Keep-It Routing Advisor calculating whether reverse freight costs exceed product resale value."
    },
    {
        "term": "Scope 3 ESG",
        "full": "Indirect Greenhouse Gas Emissions Across the Supply Chain",
        "cat": "tech",
        "top20": False,
        "hook": "The carbon emissions produced by your suppliers, shipping carriers, and customer product use (often 80%+ of total corporate carbon footprint).",
        "plain": "Scope 1: Emissions from your own factory chimneys and company vans. Scope 2: Emissions from electricity purchased to power your buildings. Scope 3: Emissions produced by outside suppliers making your parts and freight carriers hauling your goods.",
        "example": "Under EU CBAM regulations, companies importing steel, aluminum, or fertilizers must declare and pay carbon tariffs on Scope 3 emissions.",
        "customer_tip": "Show: EcoChain Scope 3 & CBAM Ledger (`carbon_scope3_ledger`) calculating real-time shipment carbon emissions."
    },
    {
        "term": "A2A Protocol",
        "full": "Agent-to-Agent Autonomous Communication Protocol",
        "cat": "tech",
        "top20": False,
        "hook": "The communication standard allowing specialized AI sub-agents to collaborate, negotiate, and hand off tasks autonomously.",
        "plain": "Instead of one monolithic AI prompt trying to do everything, an Orchestrator Agent delegates to specialized sub-agents: a Forecast Agent talks to an Inventory Agent, which negotiates with a Freight Dispatch Agent via structured JSON schemas.",
        "example": "When a port strike occurs, the War Room Orchestrator coordinates 3 sub-agents simultaneously: rerouting containers, reallocating safety stock, and adjusting plant schedules.",
        "customer_tip": "Say: 'Every agent in our architecture features 3 specialized A2A sub-agents collaborating under a master orchestrator.'"
    },
    {
        "term": "Working Capital & CCC",
        "full": "Cash Conversion Cycle (Days Sales + Days Inventory - Days Payable)",
        "cat": "tech",
        "top20": True,
        "hook": "The total calendar days it takes for money spent on raw materials to return to company bank accounts as cash from customer sales.",
        "plain": "Calculated as: Days Sales Outstanding (DSO) + Days Inventory Outstanding (DIO) - Days Payables Outstanding (DPO). The shorter the cycle, the more free cash the company generates without borrowing money.",
        "example": "Apple maintains a negative cash conversion cycle (-28 days), meaning they collect cash from iPhone customers long before paying component suppliers!",
        "customer_tip": "Show: Working Capital Cash Bridge (`working_capital_cash_bridge`) simulating inventory cash unlock."
    },
    {
        "term": "Deming / PDCA",
        "full": "Plan-Do-Check-Act Continuous Improvement Cycle",
        "cat": "tech",
        "top20": False,
        "hook": "The foundational quality management loop: Plan changes, Execute them, Measure results, Standardize successes.",
        "plain": "Quality management philosophy popularized by W. Edwards Deming. Supply chain AI agents automate the PDCA loop: sensing variance (Check), evaluating alternatives (Plan), executing writebacks (Do), and updating models (Act).",
        "example": "Automating post-incident reviews after carrier delivery failures turns disruption data into permanent routing rules.",
        "customer_tip": "Connect PDCA continuous learning to how our agents tune safety stock buffers week after week."
    },

    # --- FINANCIAL & EXECUTIVE METRICS (4 cards) ---
    {
        "term": "COGS",
        "full": "Cost of Goods Sold",
        "cat": "finance",
        "top20": True,
        "hook": "The direct expense required to build and deliver products (raw materials, factory labor, and freight).",
        "plain": "COGS appears on the corporate income statement directly below Revenue. A company selling $1B in products with $700M in COGS generates $300M in Gross Profit.",
        "example": "A 2% reduction in procurement COGS drops directly to bottom-line net profit, generating more value than a 10% increase in sales volume!",
        "customer_tip": "Say: 'Because supply chain drives 60-80% of COGS, our agents have the highest ROI leverage of any enterprise software investment.'"
    },
    {
        "term": "Gross Margin",
        "full": "(Revenue - COGS) / Revenue",
        "cat": "finance",
        "top20": False,
        "hook": "The percentage of each sales dollar retained after paying direct production and shipping costs.",
        "plain": "If a product sells for $100 and COGS is $65, Gross Margin is 35%. Supply chain efficiency (lower freight, less scrap, cheaper sourcing) directly expands Gross Margin.",
        "example": "Cutting expedited air freight through better demand sensing improved division gross margin by +180 basis points.",
        "customer_tip": "Connect agent ROI directly to gross margin expansion in executive sales pitches."
    },
    {
        "term": "Landed Cost",
        "full": "Total Cost of a Product Arriving at Final Destination Dock",
        "cat": "finance",
        "top20": True,
        "hook": "Purchase price PLUS international freight PLUS import customs tariffs PLUS marine insurance PLUS domestic drayage.",
        "plain": "A widget may look cheap at $10 in China compared to $14 in Mexico. But when you add $2 ocean freight + $1.50 tariffs + $0.80 harbor fees + $1.20 domestic trucking, the Chinese widget costs $15.50 total landed cost!",
        "example": "Our Total Landed Cost Simulator prevents procurement teams from making misleading sourcing decisions based solely on purchase price.",
        "customer_tip": "Show: Tariff & Trade ESG Agent (`tariff_esg_agent`) calculating true landed cost comparisons across countries."
    },
    {
        "term": "Carrying Cost of Inventory",
        "full": "Annual Expense of Holding Stored Inventory (18% - 30% per year)",
        "cat": "finance",
        "top20": True,
        "hook": "The hidden cost of keeping boxes in a warehouse: cost of capital, building lease, insurance, taxes, shrinkage, and obsolescence.",
        "plain": "Holding $100M of inventory doesn't just tie up $100M in cash. At an annual carrying cost of 25%, it costs the company $25M every single year just to store, insure, heat, and manage that inventory!",
        "example": "Freeing up $40M in excess buffer stock saves the company $10M every year in recurring inventory carrying costs.",
        "customer_tip": "Say: 'When we unlock $40M in trapped safety stock, you don't just get cash back — you permanently eliminate $10M in annual carrying costs.'"
    }
]

# Ensure exactly 76 flashcards
assert len(FLASHCARDS) == 76, f"Expected 76 flashcards, found {len(FLASHCARDS)}"

print(f"Loaded {len(FLASHCARDS)} flashcards successfully.")

# =============================================================================
# 2. ENTERPRISE AI CONTROL TOWER DEEP DIVE — THE ITC BLUEPRINT
# =============================================================================
CONTROL_TOWER_SPEC = {
    "title": "Enterprise AI Control Tower — The ITC Blueprint",
    "subtitle": "From Passive 'Red-Dot' Dashboards to Autonomous Closed-Loop Self-Healing Networks",
    "why_gen1_gen2_fail": [
        {
            "generation": "Gen-1 Control Towers (1995–2010)",
            "mechanism": "Manual Excel Spreadsheet Consolidation & Nightly Batch Dumps",
            "fatal_flaw": "By the time regional planners consolidate 40 disparate spreadsheets every Tuesday morning, the underlying operational disruption occurred 72 hours ago. Planners are perpetually looking in the rearview mirror."
        },
        {
            "generation": "Gen-2 Control Towers (2011–2022)",
            "mechanism": "Passive BI Dashboards (Tableau, PowerBI) with Red/Yellow/Green Traffic Lights",
            "fatal_flaw": "A dashboard with a blinking red dot tells an executive that Ship #402 is delayed, but CANNOT tell them which customer orders are affected, CANNOT simulate the cost of air freight vs rail, and CANNOT write the recovery PO into SAP. It creates 'alert fatigue' without action."
        },
        {
            "generation": "Gen-3 Autonomous AI Control Tower (Google Cloud & Gemini)",
            "mechanism": "5-Layer Ingestion, Foundation Model Reasoning, OR-Tools Optimization & 1-Click SAP Writeback",
            "fatal_flaw": "Transforms the Control Tower from a passive monitoring screen into an active execution brain that senses disruptions before they hit, evaluates financial trade-offs in seconds, and executes recovery plans."
        }
    ],
    "autonomy_levels": [
        {"lvl": "Level 1: Descriptive Visibility", "desc": "What is happening right now? (Tracks GPS pins, ship locations, inventory balances across warehouses on a map)."},
        {"lvl": "Level 2: Diagnostic Intelligence", "desc": "Why did it happen? (Performs root-cause analysis tracing late delivery back to customs paperwork hold or port berth congestion)."},
        {"lvl": "Level 3: Predictive Sensing", "desc": "What will happen next? (Predicts that a monsoon typhoon will shut down a rail corridor 5 days before the storm makes landfall using WeatherNext)."},
        {"lvl": "Level 4: Prescriptive Optimization", "desc": "What should we do? (Runs Google OR-Tools to generate 3 financially balanced mitigation options with cost, OTIF, and carbon trade-offs)."},
        {"lvl": "Level 5: Autonomous Execution", "desc": "Self-healing supply chain. (Executes approved mitigation writebacks directly into SAP S/4HANA, TMS, and WMS without manual data entry)."}
    ],
    "five_data_streams": [
        {
            "stream": "1. Satellite AIS & Flight ADS-B",
            "source": "Spire Global, exactEarth, FlightAware",
            "payload": "Real-time vessel MMSI, latitude/longitude, speed over ground, draft depth, and airport cargo terminal congestion."
        },
        {
            "stream": "2. Road & Rail Telematics",
            "source": "Samsara ELD, Railinc EDI 404/417, FASTag (India)",
            "payload": "Tractor-trailer GPS coordinates, reefer temperature logs, driver Hours of Service (HOS), and rail car siding interchanges."
        },
        {
            "stream": "3. Enterprise Business Transactions",
            "source": "SAP S/4HANA, SAP IBP, Oracle ERP",
            "payload": "Purchase orders (EKKO/EKPO), sales orders (VBAK/VBAP), customer priority tiers, and inventory stock balances (MARA/MSEG)."
        },
        {
            "stream": "4. Facility & Warehouse Feeds",
            "source": "Manhattan Active WMS, Siemens MES, Dock Schedulers",
            "payload": "Inbound trailer yard appointments, dock door dwell times, line changeover schedules, and pallet LPN inwarding scans."
        },
        {
            "stream": "5. Environmental & Climate AI",
            "source": "Google DeepMind WeatherNext, Earth Engine",
            "payload": "10-15 day global precipitation forecasts, river flood stage warnings, typhoon storm surge cones, and port seismic alerts."
        }
    ],
    "itc_case_study": {
        "client": "ITC Limited (Conglomerate: Foods, Agri-Business, Paperboards, Cigarettes)",
        "context": "Managing India's most complex consumer goods distribution network: e-Choupal farmgate procurement -> 20+ ICML integrated mega-plants -> 50+ CFA regional depots -> millions of retail kirana stores.",
        "disruption_scenario": "Severe monsoon flooding washes out the primary South-Eastern Railway line between Vijayawada (Andhra Pradesh) and the Uluberia ICML / Kolkata CFA depot during peak festive demand.",
        "ai_resolution_sequence": [
            "Step 1 (Sensing): Control Tower ingests WeatherNext precipitation alerts and Railinc/Indian Railways washout notices 48 hours before planned dispatch.",
            "Step 2 (Impact Blast Radius): Evaluates affected shipments: 18 rail rakes carrying 14,000 metric tons of agri-produce and packaged foods; projects Kolkata CFA stockout in 72 hours.",
            "Step 3 (OR-Tools Multi-Objective Solver): Generates 3 mitigation scenarios: Option A (Air freight - fastest, prohibitive cost); Option B (Wait 5 days for track repair - $1.8M stockout penalties); Option C (Reroute 60% via dedicated multi-axle road fleet + 40% via alternate Bilaspur rail corridor).",
            "Step 4 (Executive Recommendation): Option C preserves 98.4% customer fill rate with only $142K in incremental freight expense, saving $1.65M in lost sales.",
            "Step 5 (Closed-Loop Execution): Upon one-click planner approval, the Control Tower autonomously generates 140 road transport e-Way bills, updates SAP shipment documents, and alerts Kolkata CFA dock receivers."
        ]
    }
}

# =============================================================================
# 3. ALPHABET INTERNAL AI SUPPLY CHAIN PLAYBOOK
# =============================================================================
ALPHABET_AI_SPEC = {
    "title": "Alphabet's Internal AI Supply Chain Playbook",
    "subtitle": "How Google DeepMind & Google Cloud Power Alphabet's Global Compute & Hardware Infrastructure",
    "pillars": [
        {
            "name": "1. TPU Capacity & Silicon Demand Forecasting",
            "tech": "Google DeepMind TimesFM & Neural Sequence Models",
            "details": "Forecasting multi-year demand for Google's custom Tensor Processing Units (TPU v4, v5p, v6 Trillium) across Search, YouTube, DeepMind, and Google Cloud customers. Integrates lead times for TSMC CoWoS (Chip-on-Wafer-on-Substrate) advanced packaging 18 months ahead to secure global foundry reservations."
        },
        {
            "name": "2. Circular Server Hardware Harvesting",
            "tech": "Circular Infrastructure Optimization & Component Remanufacturing",
            "details": "Alphabet diverts over 90% of decommissioned data center hardware from landfills. When servers reach retirement, automated testing pipelines harvest processors, DDR memory modules, and SSD flash drives for component-level remanufacturing, testing, and deployment into secondary compute clusters."
        },
        {
            "name": "3. DeepMind WeatherNext for Maritime Shipping Resilience",
            "tech": "GraphCast & WeatherNext 3 Neural Foundation Models",
            "details": "Alphabet's global server supply chain moves hundreds of thousands of components across trans-ocean container corridors. Ingesting WeatherNext neural weather forecasts allows logistics teams to predict typhoon sea states 10-14 days early, routing high-value server racks around severe ocean storms."
        },
        {
            "name": "4. Carbon-Aware Compute Workload Scheduling",
            "tech": "Google 24/7 Carbon-Free Energy Infrastructure",
            "details": "Supply chain optimization extends to energy consumption. Google's carbon-aware computing platform shifts non-urgent batch data center compute jobs (such as model training and indexing) across global regions in real time to match peak solar and wind energy generation."
        }
    ]
}

# =============================================================================
# 4. 25 CUSTOMER CONVERSATION DECODER SCENARIOS
# =============================================================================
CUSTOMER_DECODER = [
    {
        "domain": "Planning & S&OP",
        "complaint": "Our demand forecasts are always wrong. Sales promises huge numbers that never happen, and then our warehouses are choked with unsold inventory!",
        "meaning": "Siloed organization running on uncalibrated spreadsheets without consensus S&OP discipline or POS demand sensing.",
        "root_cause": "Sales bonus incentives reward over-forecasting, while planners lack daily point-of-sale cash-register scan visibility.",
        "agent": "Demand Sensing Agent (`demand_sensing_agent`) + S&OP Scenario Weaver (`sop_scenario_weaver`)",
        "question": "When a sales spike happens, how many days pass before your production schedule actually adjusts—and are you reading daily retail POS scans or waiting for warehouse reorders?"
    },
    {
        "domain": "Planning & Promotions",
        "complaint": "Every time our marketing team runs a 20% discount promotion, we either run out of product in 2 days or get stuck with 6 months of excess stock.",
        "meaning": "Marketing runs promotions in isolation without calculating price elasticity, lift curves, or baseline cannibalization.",
        "root_cause": "Promotional lift is calculated using static gut-feel percentages rather than ML regression on historical promotion response curves.",
        "agent": "Promo Lift Simulator (`promo_lift_simulator`)",
        "question": "Can your team simulate promotional volume lift and supplier packaging capacity simultaneously before marketing launches a retail campaign?"
    },
    {
        "domain": "Procurement & Sourcing",
        "complaint": "Our raw material suppliers keep raising prices by 15%, claiming inflation and commodity spikes, and our buyers have no choice but to pay.",
        "meaning": "Procurement has zero visibility into bottom-up component cost structures and relies on vendor cost quotes.",
        "root_cause": "Lack of parametric should-cost models indexing live London Metal Exchange (LME) or commodity resin indices.",
        "agent": "RFQ Should-Cost Agent (`rfq_should_cost_agent`)",
        "question": "Do your buyers have automated should-cost breakdowns that isolate raw material commodity fluctuations from supplier conversion markup?"
    },
    {
        "domain": "Sourcing Risk",
        "complaint": "A Tier-2 sub-supplier in Asia had a factory fire, and it shut down our entire North American assembly plant for 3 weeks without warning!",
        "meaning": "The enterprise only tracks direct Tier-1 vendors and is completely blind to deep Tier-2 and Tier-3 diamond dependencies.",
        "root_cause": "Bill of Materials (BOM) data stops at direct tier-1 contract manufacturers; sub-tier supplier origins are untracked.",
        "agent": "Tier-N Risk Sentinel (`tier_n_risk_sentinel`)",
        "question": "Can you map which of your independent Tier-1 suppliers are secretly buying microchips or resins from the exact same Tier-2 manufacturing plant?"
    },
    {
        "domain": "Trade Compliance",
        "complaint": "Our customs brokers take 4 days to classify tariff codes, and we got hit with a $600K customs penalty for misclassified HS codes.",
        "meaning": "Manual tariff classification using outdated spreadsheets that cannot keep pace with shifting international trade laws.",
        "root_cause": "Engineering parts descriptions in ERP don't match legal Harmonized System (HS) nomenclature.",
        "agent": "Tariff & Trade ESG Agent (`tariff_esg_agent`)",
        "question": "How quickly can your compliance team simulate the gross margin impact if tariffs increase by 25% across your import categories?"
    },
    {
        "domain": "Supplier Quality",
        "complaint": "We received 40 pallets of defective packaging seals, but our warehouse had already accepted them and Accounts Payable paid the invoice!",
        "meaning": "Disconnected Quality (SAP QM), Inwarding (WMS), and Accounts Payable (SAP FI) systems.",
        "root_cause": "Lack of automated pre-inwarding inspection hold gates and automated 3-way match debit memo writebacks.",
        "agent": "Supplier Quality Sentinel (`supplier_quality_sentinel`)",
        "question": "When an incoming raw material shipment fails lab inspection, does your system automatically freeze payment and generate a COPQ debit memo in ERP?"
    },
    {
        "domain": "Manufacturing Scheduling",
        "complaint": "Our factory changeovers waste 4 hours every shift because the schedule keeps jumping between dark and light colors and different bottle sizes.",
        "meaning": "Production planners sequence jobs manually based on sales urgency rather than mathematical setup time minimization.",
        "root_cause": "Lack of Traveling Salesperson Sequence-Dependent Setup Time optimization in production scheduling.",
        "agent": "Line Schedule Optimizer (`line_schedule_optimizer`)",
        "question": "What is your average daily changeover downtime, and are you using mathematical constraint solvers (like OR-Tools) to sequence production runs?"
    },
    {
        "domain": "Plant Maintenance",
        "complaint": "Our main packaging line suffered an unexpected spindle bearing seizure yesterday, losing us $180,000 in scheduled production.",
        "meaning": "The plant runs reactive maintenance or basic calendar-based maintenance rather than vibration/thermal predictive telemetry.",
        "root_cause": "Machine SCADA and PLC sensor data is trapped in local historian databases without real-time AI anomaly detection.",
        "agent": "AssetGuard Plant OEE (`plant_oee_maintenance_agent`)",
        "question": "Can your engineers predict bearing and motor failures 48 hours before physical breakdown based on real-time sensor telemetry?"
    },
    {
        "domain": "Inline Quality",
        "complaint": "We only catch bottle seal defects at the end of the line during manual QA sampling, by which time 5,000 defective bottles have already been packed.",
        "meaning": "Batch statistical sampling instead of 100% continuous inline computer vision inspection.",
        "root_cause": "Human visual inspectors suffer eye fatigue at line speeds exceeding 300 units per minute.",
        "agent": "Inline Quality Inspection Agent (`inline_quality_inspection_agent`)",
        "question": "Have you evaluated multimodal AI vision models (like Gemini 3.8 Flash) to inspect 100% of finished units at full line speed?"
    },
    {
        "domain": "Inventory Optimization",
        "complaint": "We have $80M in total inventory, yet our customer fill rate is only 91% and our best-sellers are constantly out of stock!",
        "meaning": "Inventory is misallocated across tiers—huge safety stock surpluses at the wrong locations, and shortages at retail hubs.",
        "root_cause": "Single-echelon safety stock formulas calculated in isolated spreadsheets without Clark-Scarf multi-echelon pooling.",
        "agent": "EchelonFlow MEIO (`echelon_inventory_allocator`)",
        "question": "How do you decide whether to hold safety buffer stock at your central factory, regional RDCs, or local city hubs?"
    },
    {
        "domain": "Order Promising (ATP)",
        "complaint": "Customer service promises order delivery dates to small retail accounts, and then we run out of stock for our tier-1 high-margin retail contracts.",
        "meaning": "First-come, first-served order promising without real-time Available-to-Promise (ATP) tier reservation rules.",
        "root_cause": "ERP runs batch overnight ATP updates rather than real-time sub-50ms stock allocation.",
        "agent": "Dynamic Order Promising ATP (`dynamic_order_promising_atp`)",
        "question": "Does your order management system automatically protect inventory allocations for strategic, contracted customers during stock crunches?"
    },
    {
        "domain": "Warehouse Operations",
        "complaint": "Our warehouse order pickers walk 12 miles a day, and our shipping dock is an absolute logjam during the 4 PM dispatch window.",
        "meaning": "Poor warehouse slotting; fast-moving SKUs are stored at the far back of the warehouse, and pick waves are released without dock balancing.",
        "root_cause": "Static warehouse slotting that hasn't been re-balanced since warehouse commissioning 3 years ago.",
        "agent": "Warehouse Slotting Optimizer (`warehouse_slotting_optimizer`)",
        "question": "How often do you dynamically re-slot your warehouse based on seasonal pick velocity to minimize picker travel distance?"
    },
    {
        "domain": "Yard Management",
        "complaint": "Truck drivers arrive at our warehouse unannounced, sit in the staging yard for 6 hours, and carriers charge us $1.2M in annual demurrage fees.",
        "meaning": "Disconnected yard scheduling without automated carrier appointment gates or GPS geofencing.",
        "root_cause": "Guard shack logs arrivals on paper clipboards without real-time integration to WMS dock door availability.",
        "agent": "Yard & Dock Sequencer (`yard_dock_sequencer`)",
        "question": "Does your yard management system automatically assign dock doors and alert drivers via SMS based on live trailer GPS ETA?"
    },
    {
        "domain": "Cross-Docking",
        "complaint": "Pallets arrive from our factories and sit on warehouse storage racks for 3 days before being picked to reload outbound store delivery trucks.",
        "meaning": "Complete absence of synchronized cross-docking; double-handling labor and wasted rack space.",
        "root_cause": "Inbound supplier ASNs are not harmonized with outbound store shipment pick waves.",
        "agent": "Cross-Dock Flow Orchestrator (`crossdock_transfer_orchestrator`)",
        "question": "What percentage of your inbound pallets flow directly from the receiving door to an outbound trailer in under 4 hours without entering storage?"
    },
    {
        "domain": "Transportation Routing",
        "complaint": "Our private truck fleet is spending $2.4M more on diesel than budgeted, and 22% of our return trips are driving completely empty.",
        "meaning": "Static delivery route planning without dynamic return backhaul matching or multi-stop load consolidation.",
        "root_cause": "Dispatchers plan routes manually on whiteboards without Google Maps Platform traffic or multi-drop route optimization.",
        "agent": "FleetFlow Route & Dispatch Optimizer (`fleetflow_dispatch`)",
        "question": "What is your current empty deadhead percentage, and how do you automatically match outbound deliveries with paying return loads?"
    },
    {
        "domain": "Load Consolidation",
        "complaint": "We are paying full truckload freight rates for trailers that are only 65% full by cubic volume, effectively shipping expensive air!",
        "meaning": "Poor 3D pallet and trailer space utilization; lack of automated bin packing optimization.",
        "root_cause": "Shipping clerks estimate pallet layouts visually rather than utilizing 3D container packing algorithms.",
        "agent": "CubeMaster 3D Load Studio (`load_consolidation_agent`)",
        "question": "Do your shipping teams use 3D constraint load builders to maximize axle weight limits and cubic volume before dispatching trailers?"
    },
    {
        "domain": "Multi-Modal Freight",
        "complaint": "We ship everything across the country via long-haul diesel trucks because rail takes too long, costing us millions in excess freight and carbon.",
        "meaning": "Rigid single-mode mindset; inability to dynamically evaluate intermodal rail transit tradeoffs.",
        "root_cause": "Planners lack automated tools to balance rail cost savings against transit time buffers.",
        "agent": "Multimodal Mode Shift Agent (`multimodal_mode_shift_agent`)",
        "question": "What criteria trigger an automated freight shift from road trucking to intermodal rail or short-sea shipping on non-urgent inventory?"
    },
    {
        "domain": "Port & Ocean Logistics",
        "complaint": "We paid $380,000 in ocean container demurrage penalties last month because our drayage truckers couldn't get terminal appointments in time.",
        "meaning": "Zero real-time visibility into port container free-time clocks or marine terminal gate availability.",
        "root_cause": "Tracking shipping containers manually by copying vessel tracking numbers into shipping line websites.",
        "agent": "Port Drayage Orchestrator (`port_drayage_orchestrator`)",
        "question": "Does your system ingest satellite AIS feeds to predict ocean container vessel discharge times and automate terminal drayage bookings?"
    },
    {
        "domain": "Air Cargo Logistics",
        "complaint": "When an urgent factory part is delayed, our team panics and books emergency air freight at $14/kg without optimizing pallet cargo space.",
        "meaning": "Uncontrolled emergency expedite spending without air cargo Unit Load Device (ULD) contour optimization.",
        "root_cause": "Lack of standardized air freight booking rules and dynamic volumetric density checks.",
        "agent": "AeroFreight Air Cargo Optimizer (`air_cargo_uld_optimizer`)",
        "question": "How do you control expedited air freight authorizations, and do you optimize aircraft cargo pallet contours to minimize dimensional weight charges?"
    },
    {
        "domain": "Retail & TM&D Distribution",
        "complaint": "Our field sales reps spend 2 hours every morning deciding which retail stores to visit, and our promotional displays are missing from 30% of stores.",
        "meaning": "Inefficient sales beat routing and zero real-time visual proof of retail planogram compliance.",
        "root_cause": "Field reps manage sales beats manually on paper; store audits require physical manual clipboard checks.",
        "agent": "Field Beat Sync Agent (`field_beat_distributor_sync_agent`) + ShelfVision (`planogram_merchandising_vision_auditor`)",
        "question": "Can your sales reps photograph a store shelf with a smartphone and have AI instantly verify planogram compliance and out-of-stock items in 3 seconds?"
    },
    {
        "domain": "Trade Claims & Rebates",
        "complaint": "Our wholesale distributors deduct $8M annually in trade promotion claims and volume discounts, and it takes our finance team 60 days to audit them.",
        "meaning": "Unreconciled distributor claim deductions leading to massive profit leakage and contentious partner relationships.",
        "root_cause": "Distributor claims arrive on unstructured PDFs and invoices that require manual line-by-line verification against promotion contracts.",
        "agent": "Trade Scheme Claims Reconciler (`trade_scheme_claims_reconciler`)",
        "question": "How much cash is currently trapped in disputed distributor trade claims, and how automated is your contract scheme audit process?"
    },
    {
        "domain": "Customer Delivery Compliance",
        "complaint": "Walmart and Target fined us $3.2M last quarter for late and incomplete shipments under their strict OTIF delivery compliance programs.",
        "meaning": "Inability to predict carrier transit delays and warehouse picking bottlenecks before delivery appointment windows expire.",
        "root_cause": "The enterprise discovers a delivery was late only when the retailer issues the penalty debit deduction.",
        "agent": "OTIF Penalty Shield (`otif_penalty_shield`)",
        "question": "Can your dispatchers identify at-risk retail customer orders 48 hours before the delivery window closes and trigger automated recovery routing?"
    },
    {
        "domain": "Reverse Logistics & Returns",
        "complaint": "Our e-commerce returns warehouse is overflowing with opened boxes. We are spending $16 to process returns on items that sell for $12!",
        "meaning": "Indiscriminate return authorization policies without margin-aware Keep-It triage logic.",
        "root_cause": "Returns systems generate return labels automatically without calculating reverse freight and inspection labor against net recovery value.",
        "agent": "Reverse RMA & Keep-It Advisor (`reverse_rma_optimizer`)",
        "question": "Do you calculate whether the reverse shipping and warehouse inspection cost exceeds the liquidation value before issuing a return label?"
    },
    {
        "domain": "Sustainability & ESG",
        "complaint": "Our European enterprise customers are demanding Scope 3 carbon emission disclosures for every shipment, or they will switch to certified green suppliers.",
        "meaning": "Manual carbon auditing using outdated annual industry averages rather than shipment-level telematics.",
        "root_cause": "Inability to extract fuel consumption and transport mode data from multi-carrier logistics invoices.",
        "agent": "EcoChain Scope 3 & CBAM Ledger (`carbon_scope3_ledger`)",
        "question": "Can your systems calculate GLEC-compliant, shipment-level Scope 3 carbon emissions directly from carrier telematics and fuel consumption data?"
    },
    {
        "domain": "Control Tower & Leadership",
        "complaint": "Our executive team sits in weekly supply chain reviews looking at 80-page PowerPoint decks, but by the time we see the numbers, it's too late to fix anything.",
        "meaning": "Passive executive reporting that lacks real-time predictive sensing and autonomous closed-loop execution.",
        "root_cause": "Siloed legacy data lakes requiring manual human data extraction and static chart generation.",
        "agent": "CSCO Control Tower Copilot (`csco_control_tower_copilot`) + War Room (`disruption_war_room_orchestrator`)",
        "question": "If an ocean port strike or rail washout occurred right now, could your leadership simulate 3 financial recovery scenarios and execute writebacks in under 5 minutes?"
    }
]

# Ensure exactly 25 scenarios
assert len(CUSTOMER_DECODER) == 25, f"Expected 25 scenarios, found {len(CUSTOMER_DECODER)}"

# =============================================================================
# 5. 20-QUESTION CSCO DOMAIN CERTIFICATION EXAM
# =============================================================================
QUIZ = [
    {
        "q": "1. What is the fundamental difference between Point of Sale (POS) data and warehouse Purchase Orders (POs)?",
        "options": [
            "POS data reflects actual daily cash-register purchases by end consumers, whereas warehouse POs reflect delayed, buffered replenishment orders.",
            "POS data is used only by accounting, while POs are used by shipping.",
            "POs are real-time, while POS data has a 3-week lag.",
            "There is no difference; both represent identical quantities."
        ],
        "correct": 0,
        "explain": "Exactly! Relying on warehouse POs leaves manufacturers blind to demand shifts by 2 to 4 weeks. Reading daily POS scans eliminates the delay and stops the bullwhip effect."
    },
    {
        "q": "2. In S&OP (Sales & Operations Planning), what is the primary operational friction between Sales, Finance, and Manufacturing?",
        "options": [
            "Sales wants minimal inventory; Finance wants maximum inventory; Manufacturing wants constant overtime.",
            "Sales wants maximum inventory to never lose a sale; Finance wants minimal inventory to conserve cash; Manufacturing wants level, predictable schedules.",
            "All three departments always agree on the forecast without friction.",
            "Sales only cares about trucking costs, while Finance only cares about packaging colors."
        ],
        "correct": 1,
        "explain": "100% correct! S&OP exists precisely to resolve this tripartite tension and establish ONE consensus operating plan aligned with P&L goals."
    },
    {
        "q": "3. Why is volume-weighted WAPE generally preferred over simple MAPE for enterprise demand forecasting?",
        "options": [
            "WAPE is easier to calculate in Microsoft Excel.",
            "MAPE distorts overall accuracy by giving a 50% error on a 10-unit slow mover the same weight as a 5% error on a 10,000-unit best-seller.",
            "WAPE ignores all forecasting errors.",
            "WAPE only applies to air cargo shipments."
        ],
        "correct": 1,
        "explain": "Spot on! MAPE treats all SKUs equally regardless of volume. WAPE weights errors by sales volume, ensuring high-revenue products dominate the accuracy score."
    },
    {
        "q": "4. What is a hidden 'diamond dependency' in Multi-Tier (Tier-N) supply chains?",
        "options": [
            "When a company buys jewelry for its executive team.",
            "When multiple independent Tier-1 suppliers secretly rely on the exact same single Tier-2 or Tier-3 sub-supplier for critical raw materials or microchips.",
            "When a supplier charges 4x the market rate for freight.",
            "When a warehouse has 4 dock doors configured in a diamond shape."
        ],
        "correct": 1,
        "explain": "Correct! If two competing Tier-1 suppliers source from the same Tier-3 chip fab, an outage at that fab shuts down both suppliers simultaneously."
    },
    {
        "q": "5. What are the three documents verified in an enterprise Accounts Payable '3-Way Match' before releasing payment?",
        "options": [
            "Driver's License, Vehicle Registration, and Insurance Card.",
            "Purchase Order (PO), Inbound Goods Receipt (GR), and Vendor Commercial Invoice.",
            "Marketing Brochure, Sales Forecast, and Bank Statement.",
            "Ocean Bill of Lading, Customs Declaration, and Warehouse Lease."
        ],
        "correct": 1,
        "explain": "Precisely! 3-Way Matching ensures that what was approved (PO), what was physically received (GR), and what was billed (Invoice) match before cash leaves the company."
    },
    {
        "q": "6. Under Incoterms, what does 'FOB' (Free on Board) mean regarding shipping risk and freight payment?",
        "options": [
            "The seller pays all shipping costs directly to the buyer's warehouse door.",
            "The seller delivers goods over the ship's rail at the departure port; from that moment, freight cost and cargo loss risk transfer to the buyer.",
            "The buyer picks up goods at the seller's factory gate.",
            "Freight is completely free with zero shipping charges."
        ],
        "correct": 1,
        "explain": "Exactly! Under FOB, the seller is only responsible until goods are loaded onto the ship at origin. Ocean freight and transit risk belong to the buyer."
    },
    {
        "q": "7. Overall Equipment Effectiveness (OEE) is calculated by multiplying which three manufacturing metrics?",
        "options": [
            "Electricity × Water × Gas.",
            "Availability × Performance × Quality.",
            "Speed × Weight × Volume.",
            "Labor Hours × Machine Cost × Scrap Value."
        ],
        "correct": 1,
        "explain": "100% right! Availability (uptime) × Performance (operating speed) × Quality (defect-free output) = OEE. World-class plants achieve >85% OEE."
    },
    {
        "q": "8. What is the fundamental difference between an ERP system (like SAP) and a WMS (like Manhattan Associates)?",
        "options": [
            "ERP manages macro financials, purchase orders, and total company stock balances; WMS manages physical bin racks, picker walking paths, and pallet LPNs.",
            "ERP is for truck drivers; WMS is for accounting.",
            "ERP is only used in Europe; WMS is only used in America.",
            "There is no difference; they are duplicate systems."
        ],
        "correct": 0,
        "explain": "Spot on! SAP knows a facility has 5,000 cases in stock; Manhattan WMS knows those 5,000 cases are located in Aisle 12, Rack B, Level 3."
    },
    {
        "q": "9. In food, beverage, and pharmaceuticals, why is FEFO (First Expired, First Out) mandatory over standard FIFO?",
        "options": [
            "FEFO makes warehouse picking faster for forklift drivers.",
            "FEFO prioritizes shipping inventory with the closest expiration date first to prevent product spoilage on store shelves, regardless of arrival date.",
            "FEFO is cheaper for freight carriers.",
            "FEFO is used only for frozen ice cream."
        ],
        "correct": 1,
        "explain": "Correct! If a newly arrived pallet expires in 30 days while an older pallet expires in 90 days, shipping the newer pallet first prevents $ millions in expired spoilage write-offs."
    },
    {
        "q": "10. What is 'Cross-Docking' in modern warehouse logistics?",
        "options": [
            "Parking boats across two different marine docks.",
            "Unloading inbound supplier pallets and loading them directly onto outbound store delivery trailers with zero rack storage dwell time.",
            "Storing pallets in high-bay racks for over 180 days.",
            "Shipping goods across international borders without customs paperwork."
        ],
        "correct": 1,
        "explain": "Exactly! Cross-docking bypasses storage racks entirely, cutting warehouse handling labor and moving goods from receiving to shipping in under 4 hours."
    },
    {
        "q": "11. What is the primary difference between container Demurrage and Detention fees?",
        "options": [
            "Demurrage is paid to airlines; Detention is paid to railways.",
            "Demurrage is charged when full containers sit inside the marine port past free time; Detention is charged when containers are kept too long outside the port at a warehouse.",
            "Demurrage applies to road trucks; Detention applies to river barges.",
            "Both are discounts given by shipping lines for fast turnaround."
        ],
        "correct": 1,
        "explain": "Spot on! Demurrage = inside port terminal penalty; Detention = outside port terminal container equipment delay penalty."
    },
    {
        "q": "12. In retail distribution, what is an 'OTIF' (On-Time In-Full) failure penalty?",
        "options": [
            "A bonus paid to trucking companies for driving fast.",
            "A punitive fee (often 3% of PO value) deducted by major retailers like Walmart when shipments arrive late or with missing cases.",
            "A tax refund provided by government trade bodies.",
            "A discount given to customers who pick up their own orders."
        ],
        "correct": 1,
        "explain": "Correct! Retailers deduct 3% of invoice value if an order is even 1 day late or missing 10 cases, costing CPG brands millions annually in lost margin."
    },
    {
        "q": "13. In e-commerce reverse logistics, how does a 'Keep-It' routing advisor save enterprise money?",
        "options": [
            "It permanently bans dissatisfied customers from returning items.",
            "It calculates whether return shipping freight + warehouse grading labor exceeds the item's net resale value, refunding the customer and avoiding unprofitable reverse freight.",
            "It forces customers to drive returns to the factory.",
            "It ships all returned items via air cargo."
        ],
        "correct": 1,
        "explain": "100% right! On a damaged $15 toaster, spending $12 on return shipping and $6 on warehouse inspection loses money. Telling the customer to keep/recycle it saves $3 net."
    },
    {
        "q": "14. Why do Generation-2 BI dashboards (Tableau/PowerBI) fail to serve as true modern Supply Chain Control Towers?",
        "options": [
            "They have too many colors and graphs.",
            "They are passive monitoring screens that display historical red dots without predictive lead time, multi-objective optimization, or closed-loop ERP execution.",
            "They only run on Apple computers.",
            "They are too fast for human operators."
        ],
        "correct": 1,
        "explain": "Spot on! Knowing that a ship is late 3 days after it happened doesn't solve anything. A Gen-3 Control Tower predicts delays, optimizes alternatives with OR-Tools, and writes back to SAP."
    },
    {
        "q": "15. In the ITC Limited Control Tower blueprint, what are the primary operational roles of e-Choupal, ICMLs, and CFAs?",
        "options": [
            "e-Choupal is for accounting; ICML is for marketing; CFA is for human resources.",
            "e-Choupal manages rural farmgate procurement; ICMLs are co-located manufacturing & distribution mega-campuses; CFAs are state-level master depots serving local distributors.",
            "All three are retail convenience stores in Mumbai.",
            "e-Choupal is ocean shipping; ICML is air cargo; CFA is rail transport."
        ],
        "correct": 1,
        "explain": "Exactly! e-Choupal sources agri-commodities, ICML manufactures and packs goods, and CFAs buffer and distribute finished products across Indian states."
    },
    {
        "q": "16. In the ITC monsoon rail washout scenario, how did the AI Control Tower evaluate the recovery trade-offs?",
        "options": [
            "It shut down all production and waited for the monsoon to end.",
            "It simulated 3 options (Air freight vs Wait for track repair vs Dedicated road multi-axle freight reroute) using multi-objective solvers to preserve 98.4% fill rate at minimal extra cost.",
            "It cancelled all customer orders in West Bengal.",
            "It paid Indian Railways to build a new bridge overnight."
        ],
        "correct": 1,
        "explain": "100% correct! Using multi-objective optimization, the AI balanced freight cost against lost sales penalties, selecting the road fleet bypass to protect customer fill rate."
    },
    {
        "q": "17. What is CoWoS (Chip-on-Wafer-on-Substrate) in Alphabet's semiconductor supply chain, and why is it critical?",
        "options": [
            "A brand of computer monitors used by software developers.",
            "An advanced semiconductor packaging technology that bonds TPU compute dies with High-Bandwidth Memory (HBM), acting as a multi-quarter supply bottleneck.",
            "A fiber-optic network cable laid under the Atlantic Ocean.",
            "A software compiler for Python scripts."
        ],
        "correct": 1,
        "explain": "Spot on! As discussed in Kiran's 1:1, AI accelerator production is constrained not just by wafer fabrication, but by CoWoS advanced packaging capacity lead times."
    },
    {
        "q": "18. How does Alphabet implement circular server hardware harvesting in its global data center infrastructure?",
        "options": [
            "It discards old servers in municipal landfills every 12 months.",
            "It diverts over 90% of decommissioned server components from landfills, testing and remanufacturing processors, memory, and flash drives for secondary compute reuse.",
            "It sells all old servers to retail consumers on eBay.",
            "It burns old hardware to generate data center steam power."
        ],
        "correct": 1,
        "explain": "Correct! Alphabet remanufactures and tests decommissioned server components, keeping 90%+ of hardware in a closed-loop circular economy."
    },
    {
        "q": "19. How does Google's carbon-aware computing platform optimize data center energy consumption?",
        "options": [
            "It turns off all Google Search servers during nighttime hours.",
            "It dynamically shifts non-urgent compute workloads (like model training and backups) across global data center regions to match real-time solar and wind power availability.",
            "It buys carbon credits on paper without changing server operations.",
            "It requires all users to switch their phones to low-power mode."
        ],
        "correct": 1,
        "explain": "Exactly! Google shifts computational load to wherever green renewable power is actively generating, maximizing 24/7 carbon-free energy."
    },
    {
        "q": "20. What is the fundamental difference between Google DeepMind's WeatherNext and traditional numerical weather models?",
        "options": [
            "WeatherNext is a smartphone weather widget that shows current temperature.",
            "WeatherNext is a deep learning neural foundation model that predicts global typhoon paths and extreme climate disruption 10-15 days ahead in minutes rather than hours on supercomputers.",
            "Traditional models are 100% accurate, while WeatherNext only guesses.",
            "WeatherNext is only used for local rain forecasts in California."
        ],
        "correct": 1,
        "explain": "100% right! WeatherNext (GraphCast) provides deep neural atmospheric forecasting, giving supply chain teams 10-14 days of advance warning to re-route ships and protect inventory."
    }
]

# Ensure exactly 20 questions
assert len(QUIZ) == 20, f"Expected 20 quiz questions, found {len(QUIZ)}"

print("Successfully loaded complete course data: 76 flashcards, Control Tower spec, Alphabet AI spec, 25 decoder scenarios, and 20 quiz questions.")

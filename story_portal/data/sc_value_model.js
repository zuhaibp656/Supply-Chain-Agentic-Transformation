/* Supply Chain 4-Lever Financial Value & Build Priority Model
   Modeled Enterprise Baseline: $5.0B annual Cost of Goods Sold (COGS) / $8.0B annual revenue
   multi-site Consumer Packaged Goods (CPG), Retail & Manufacturing enterprise:
     - $950M average inventory pool (~22% annual carrying cost = $209M/yr; McKinsey AI 20–35% reduction benchmark)
     - $480M annual freight & distribution spend (5–15% carrier billing error rate; 15–25% empty-mile opportunity)
     - $2.8B direct & indirect procurement spend (0.8–2.5% contract/rebate/3-way match leakage)
     - $360M annual trade promotion spend (25–50% historically fail ROI breakeven; McKinsey/BCG)
     - 12 manufacturing plants averaging 68% Overall Equipment Effectiveness (OEE)
     - $420M gross returns & short-dated perishables pool (National Retail Federation (NRF) ~16.9% retail return baseline)

   ZERO DOUBLE-COUNTING RULE:
   1. prod   (#3186FF) Productivity & Expert Redeployment: (toil hrs freed/yr * team FTEs * $105 loaded rate).
   2. flow   (#00AF57) Flow & Working Capital: Annual inventory carrying cost released (22% of freed safety stock) + OEE changeover uptime + trailer consolidation savings. Set to $0 on audit/compliance/commercial-only roles.
   3. shield (#4B31E3) Leakage & Risk Shield: Contract/invoice clawbacks + negative-ROI promo halted + Tier-2+ disruption, CBAM & detention penalty avoidance + defect scrap prevented.
   4. recov  (#12B5CB) Revenue & Salvage Recovery: Stockout lost gross-margin saved (margin contribution only) + perishable markdown margin recovery + A-grade returns & Returnable Transport Item (RTI) asset recovery. Set to $0 on back-office AP/maintenance/compliance roles.
*/
window.SC_VALUES = (function () {
  var ESTATE_BASELINE = {
    label: "$5.0B COGS / $8.0B Revenue Multi-Site Enterprise Benchmark",
    inventoryCarryingM: 209,
    freightSpendM: 480,
    procurementSpendM: 2800,
    tradeSpendM: 360,
    returnsPoolM: 420,
    plantsCount: 12,
    loadedRateHr: 105,
    note: "Figures represent single-site-normalized enterprise annual EBITDA & carrying-cost impact grounded in 2025-2026 McKinsey, Gartner, BCG, Capgemini, and National Retail Federation (NRF) benchmarks. Avoids double-counting balance-sheet cash with annual carrying cost or revenue with gross margin."
  };

  var LEVERS = [
    {
      id: "prod",
      name: "Productivity & Redeployment",
      color: "#3186FF",
      unit: "$M/yr",
      def: "Expert hours freed from manual ERP/spreadsheet reconciliation across planners, buyers, dispatchers, and QA leads, redeployed to high-judgment negotiation and exception mastery."
    },
    {
      id: "flow",
      name: "Flow & Working Capital",
      color: "#00AF57",
      unit: "$M/yr",
      def: "Annualized inventory carrying cost saved (22% cost of capital on reduced safety stock & SLOB), plant changeover & Overall Equipment Effectiveness (OEE) hours recovered, and empty freight miles eliminated."
    },
    {
      id: "shield",
      name: "Leakage & Risk Shield",
      color: "#4B31E3",
      unit: "$M/yr",
      def: "Hard cash recovered from freight & AP three-way match overbilling, blocked margin-negative promotions, contract/tariff rebate leakage, Tier-2+ disruption downtime avoided, and food/pharma scrap prevented."
    },
    {
      id: "recov",
      name: "Revenue & Salvage Recovery",
      color: "#12B5CB",
      unit: "$M/yr",
      def: "Incremental gross margin saved from prevented out-of-stocks (up to 65% lost-sales recovery), dynamic short-dated markdown optimization, and Return Merchandise Authorization (RMA) & pooled pallet salvage."
    }
  ];

  // Explicit 60-agent research-backed table (tier: 'first' [18] | 'next' [36] | 'routine' [6])
  var BY_AGENT = {
    // 01 · Planning & Strategy (12 agents: 3 first, 7 next, 2 routine)
    demand_sensing_agent: {
      tier: "first", paybackDays: 45, ftes: 18,
      prod: 0.9, flow: 6.4, shield: 1.8, recov: 9.2,
      why: "20-35% short-horizon forecast error reduction directly cuts emergency air-freight expedites, trims excess safety stock carrying cost, and prevents high-velocity stockouts."
    },
    promo_lift_simulator: {
      tier: "first", paybackDays: 60, ftes: 14,
      prod: 0.6, flow: 0.0, shield: 11.4, recov: 4.8,
      why: "25-50% of CPG trade promotions destroy margin; gating spend pre-commit stops millions in unprofitable discounts while capturing incremental baseline lift."
    },
    trade_scheme_claims_reconciler: {
      tier: "first", paybackDays: 30, ftes: 10,
      prod: 0.5, flow: 0.0, shield: 8.6, recov: 0.0,
      why: "Automates OCR deduction audits against retail circulars and proofs of performance to claw back invalid trade-spend deductions immediately."
    },
    cpfr_sync_agent: {
      tier: "next", paybackDays: 90, ftes: 12,
      prod: 0.6, flow: 2.8, shield: 0.9, recov: 3.6,
      why: "Harmonizes Collaborative Planning, Forecasting & Replenishment (CPFR) buyer overrides with point-of-sale reality to eliminate bullwhip swings across retail partners."
    },
    npi_demand_profiler: {
      tier: "next", paybackDays: 120, ftes: 8,
      prod: 0.3, flow: 1.9, shield: 2.4, recov: 2.9,
      why: "Reduces 90-day New Product Introduction (NPI) launch error via attribute lookalikes so new SKUs neither starve retail resets nor strand packaging write-offs."
    },
    field_beat_distributor_sync_agent: {
      tier: "next", paybackDays: 110, ftes: 16,
      prod: 0.8, flow: 0.0, shield: 2.1, recov: 4.4,
      why: "Equips Key Account Managers (KAM) with real-time Joint Business Plan (JBP) margin guardrails and secondary distributor sell-out visibility."
    },
    sop_scenario_weaver: {
      tier: "next", paybackDays: 105, ftes: 10,
      prod: 0.7, flow: 4.1, shield: 3.2, recov: 2.8,
      why: "Compresses monthly Sales & Operations Planning (S&OP) spreadsheet cycles from days to 15-minute constrained P&L scenarios balancing overtime, co-packers, and service."
    },
    disruption_war_room_orchestrator: {
      tier: "next", paybackDays: 95, ftes: 8,
      prod: 0.4, flow: 2.2, shield: 6.5, recov: 3.1,
      why: "Replaces multi-day crisis bridge calls with 15-minute multi-echelon allocation playbooks that defend On-Time In-Full (OTIF) compliance on top customers."
    },
    working_capital_cash_bridge: {
      tier: "next", paybackDays: 120, ftes: 9,
      prod: 0.5, flow: 4.6, shield: 2.1, recov: 1.4,
      why: "Links tail SKU pruning directly to changeover downtime freed and stranded working capital released."
    },
    eco_cutover_orchestrator: {
      tier: "next", paybackDays: 130, ftes: 7,
      prod: 0.4, flow: 1.8, shield: 3.4, recov: 0.0,
      why: "Synchronizes Engineering Change Order (ECO) Phase-In/Phase-Out (PIPO) dates across BOM components to eliminate obsolete film and carton write-offs."
    },
    csco_control_tower_copilot: {
      tier: "routine", paybackDays: 160, ftes: 6,
      prod: 0.6, flow: 0.0, shield: 1.5, recov: 0.0,
      why: "Executive briefing productivity enabler consolidating weekly Integrated Business Planning (IBP) variance notes across pillars."
    },
    network_twin_architect: {
      tier: "routine", paybackDays: 180, ftes: 6,
      prod: 0.5, flow: 2.9, shield: 1.1, recov: 0.0,
      why: "Strategic quarterly Cost-to-Serve diagnostic exposing margin-dilutive lanes and regional customer minimum order policies."
    },

    // 02 · Sourcing & Procurement (9 agents: 3 first, 4 next, 2 routine)
    tier_n_risk_sentinel: {
      tier: "first", paybackDays: 60, ftes: 11,
      prod: 0.6, flow: 2.4, shield: 11.8, recov: 4.1,
      why: "With 65%+ of disruptions starting in Tier-2+ suppliers, early AIS/financial sensing averts factory line starvation and expensive spot buys."
    },
    tariff_esg_agent: {
      tier: "first", paybackDays: 45, ftes: 8,
      prod: 0.4, flow: 0.0, shield: 9.4, recov: 0.0,
      why: "Flags uncaptured volume rebates, Harmonized Tariff (HS) duty drawbacks, and Carbon Border Adjustment Mechanism (CBAM) compliance penalties before invoice settle."
    },
    three_way_match_dispute: {
      tier: "first", paybackDays: 30, ftes: 16,
      prod: 0.9, flow: 0.0, shield: 7.8, recov: 0.0,
      why: "Direct accounts payable cash shield: resolves PO, Goods Receipt Note (GRN), and vendor invoice mismatches immediately while blocking duplicate billing."
    },
    supplier_quality_sentinel: {
      tier: "next", paybackDays: 110, ftes: 9,
      prod: 0.5, flow: 1.2, shield: 4.2, recov: 0.0,
      why: "Automates Certificate of Analysis (COA) verification and British Retail Consortium (BRC) / ISO audit qualification cycles to cut onboarding lead times."
    },
    commodity_index_advisor: {
      tier: "next", paybackDays: 95, ftes: 8,
      prod: 0.4, flow: 0.0, shield: 5.9, recov: 0.0,
      why: "Tracks CBOT/Platts resin, aluminum, and agricultural indexes so category buyers lock forward contracts during trough windows."
    },
    rfq_should_cost_agent: {
      tier: "next", paybackDays: 90, ftes: 10,
      prod: 0.5, flow: 0.0, shield: 6.8, recov: 0.0,
      why: "Deconstructs supplier quotes into clean raw-material, conversion, and tolling components ahead of Request for Quotation (RFQ) negotiations."
    },
    master_data_leadtime_steward: {
      tier: "next", paybackDays: 100, ftes: 14,
      prod: 0.8, flow: 2.7, shield: 1.9, recov: 0.0,
      why: "Closes silent EDI 855/856 confirmation gaps and updates SAP ERP vendor lead times dynamically before MRP triggers late POs."
    },
    carbon_scope3_ledger: {
      tier: "routine", paybackDays: 170, ftes: 6,
      prod: 0.5, flow: 0.0, shield: 2.2, recov: 0.0,
      why: "Consolidates supplier Scope 3 emissions ledgers and audit evidence for European Union CSRD & SEC sustainability disclosures."
    },
    sustainable_packaging_agent: {
      tier: "routine", paybackDays: 155, ftes: 7,
      prod: 0.4, flow: 0.8, shield: 2.6, recov: 0.0,
      why: "Evaluates Extended Producer Responsibility (EPR) plastic-tax exposure and recycled-resin spec substitutions during R&D design."
    },

    // 03 · Manufacturing & Production (9 agents: 2 first, 6 next, 1 routine)
    finite_production_scheduler: {
      tier: "first", paybackDays: 60, ftes: 14,
      prod: 0.7, flow: 8.6, shield: 2.1, recov: 3.4,
      why: "Eliminates manual allergen/flavor changeover waste in Excel, unlocking 3-6% incremental Overall Equipment Effectiveness (OEE) across bottling & packaging lines."
    },
    inline_yield_guardian: {
      tier: "first", paybackDays: 75, ftes: 12,
      prod: 0.6, flow: 1.9, shield: 6.4, recov: 1.5,
      why: "High-speed computer vision defect triage halts bad label/seal runs early, slashing quarantine scrap and retail recall exposure."
    },
    line_schedule_optimizer: {
      tier: "next", paybackDays: 90, ftes: 15,
      prod: 0.8, flow: 4.2, shield: 1.7, recov: 1.9,
      why: "Re-routes perishable work-in-process within 3 minutes when packaging or filler breakdowns hit during active shifts."
    },
    labor_line_balancing_agent: {
      tier: "next", paybackDays: 105, ftes: 12,
      prod: 0.7, flow: 2.8, shield: 2.4, recov: 0.0,
      why: "Matches certified operator skills against shift overtime budgets and dynamic line run schedules."
    },
    predictive_oee_sentinel: {
      tier: "next", paybackDays: 115, ftes: 9,
      prod: 0.4, flow: 5.1, shield: 2.9, recov: 0.0,
      why: "Detects Clean-in-Place (CIP) and boiler utility bottlenecks early to prevent unscheduled shift stalls."
    },
    copacker_allocation_agent: {
      tier: "next", paybackDays: 120, ftes: 7,
      prod: 0.4, flow: 2.5, shield: 3.1, recov: 1.8,
      why: "Optimizes make-vs-buy Contract Manufacturing Organization (CMO) tolling runs based on delivered lane freight + conversion cost."
    },
    batch_record_auditor: {
      tier: "next", paybackDays: 110, ftes: 10,
      prod: 0.6, flow: 1.1, shield: 3.8, recov: 0.0,
      why: "Automates Critical Control Point (CCP) and Batch Production Record review so FDA/ISO hold releases happen in minutes instead of shifts."
    },
    scrap_defect_root_cause_agent: {
      tier: "next", paybackDays: 125, ftes: 9,
      prod: 0.5, flow: 2.3, shield: 3.3, recov: 0.0,
      why: "Synthesizes cross-shift maintenance logs, humidity telemetry, and vendor resin batches into Corrective & Preventive Action (CAPA) briefs."
    },
    capex_simulator_agent: {
      tier: "routine", paybackDays: 180, ftes: 5,
      prod: 0.4, flow: 1.8, shield: 2.4, recov: 0.0,
      why: "Strategic engineering twin stress-testing multi-year line investment Internal Rate of Return (IRR) before capital approval."
    },

    // 04 · Inventory & Warehousing (9 agents: 3 first, 6 next, 0 routine)
    meio_safety_stock_agent: {
      tier: "first", paybackDays: 55, ftes: 10,
      prod: 0.5, flow: 14.8, shield: 0.0, recov: 4.5,
      why: "Multi-Echelon Inventory Optimization (MEIO) releases 20-30% trapped safety stock across plants & DCs while raising case-fill protection."
    },
    slob_disposition_agent: {
      tier: "first", paybackDays: 45, ftes: 11,
      prod: 0.5, flow: 4.9, shield: 3.6, recov: 4.2,
      why: "Identifies Slow-Moving & Obsolete (SLOB) inventory 60+ days ahead of write-off thresholds and automates profitable secondary clearance."
    },
    planogram_merchandising_vision_auditor: {
      tier: "first", paybackDays: 60, ftes: 16,
      prod: 0.8, flow: 1.5, shield: 0.0, recov: 8.9,
      why: "Detects zero-scan phantom inventory across retail stores immediately so eCommerce orders don't cancel and physical shelves stay stocked."
    },
    crossdock_transfer_orchestrator: {
      tier: "next", paybackDays: 95, ftes: 12,
      prod: 0.6, flow: 5.4, shield: 1.4, recov: 2.8,
      why: "Executes dynamic inter-facility stock rebalancing and cross-docking instead of letting one DC starve while another overflows."
    },
    warehouse_slotting_agent: {
      tier: "next", paybackDays: 105, ftes: 14,
      prod: 0.7, flow: 4.8, shield: 0.8, recov: 0.0,
      why: "Re-slots fast-pick warehouse faces continuously by pick affinity, reducing picker travel distance by 12-18% inside Fulfillment Centers (FC)."
    },
    dock_to_stock_agent: {
      tier: "next", paybackDays: 95, ftes: 14,
      prod: 0.7, flow: 2.9, shield: 2.3, recov: 0.0,
      why: "Reconciles inbound Bills of Lading (BOL) and Advance Shipping Notices (ASN) on dock arrival to eliminate yard dwell and putaway lag."
    },
    wave_fulfillment_copilot: {
      tier: "next", paybackDays: 100, ftes: 16,
      prod: 0.8, flow: 3.2, shield: 1.9, recov: 1.6,
      why: "Balances dynamic Fulfillment Center (FC) wave labor to hit tight parcel and retail carrier dock cutoffs without overtime spikes."
    },
    atp_order_promising_agent: {
      tier: "next", paybackDays: 110, ftes: 10,
      prod: 0.5, flow: 2.1, shield: 0.0, recov: 5.2,
      why: "Selects optimal Ship-from-Store (SFS) or Buy-Online-Pickup-in-Store (BOPIS) nodes using live parcel zone rates and store backroom capacity."
    },
    returns_triage_agent: {
      tier: "next", paybackDays: 115, ftes: 11,
      prod: 0.6, flow: 1.8, shield: 1.2, recov: 3.9,
      why: "Classifies inbound reverse warehouse returns within 24 hours so A-grade stock returns straight to Available-to-Promise (ATP) inventory."
    },

    // 05 · Distribution & Logistics (12 agents: 4 first, 8 next, 0 routine)
    load_consolidation_agent: {
      tier: "first", paybackDays: 45, ftes: 14,
      prod: 0.7, flow: 9.8, shield: 1.4, recov: 0.0,
      why: "Combines fragmented Less-than-Truckload (LTL) tenders into cube-optimal multi-stop Full Truckloads (FTL) via 3D OR-Tools bin-packing."
    },
    fleetflow_dispatch: {
      tier: "first", paybackDays: 45, ftes: 18,
      prod: 0.9, flow: 7.4, shield: 2.8, recov: 3.1,
      why: "Live FleetFlow control tower re-routes commercial corridors around weather/congestion and enforces Load-In-First-Out (LIFO) stability."
    },
    otif_penalty_shield: {
      tier: "first", paybackDays: 40, ftes: 14,
      prod: 0.7, flow: 0.0, shield: 7.9, recov: 2.2,
      why: "Intercepts carrier exceptions proactively to cut retail On-Time In-Full (OTIF) chargebacks and Where-Is-My-Order (WISMO) inbound calls."
    },
    freight_bill_audit_agent: {
      tier: "first", paybackDays: 30, ftes: 12,
      prod: 0.6, flow: 0.0, shield: 10.6, recov: 0.0,
      why: "Benchmarked 5-15% of carrier freight invoices contain accessorial/detention/fuel-surcharge errors; automated POD reconciliation claws cash back fast."
    },
    yard_dock_sequencer: {
      tier: "next", paybackDays: 95, ftes: 12,
      prod: 0.6, flow: 3.4, shield: 2.2, recov: 0.0,
      why: "Uses gate telemetry to dynamically sequence trailer dock doors, eliminating live-load driver detention fees."
    },
    cold_chain_auditor: {
      tier: "next", paybackDays: 100, ftes: 8,
      prod: 0.4, flow: 0.0, shield: 6.2, recov: 1.4,
      why: "Monitors refrigerated trailer IoT sensors continuously to prevent cold-chain thermal excursions and food/pharma load rejections."
    },
    aisle_aligned_pallet_agent: {
      tier: "next", paybackDays: 115, ftes: 10,
      prod: 0.5, flow: 3.6, shield: 0.0, recov: 1.5,
      why: "Builds store-aisle-sequenced pallets in the DC so retail night-crews restock shelves 30% faster with zero double handling."
    },
    store_capacity_agent: {
      tier: "next", paybackDays: 120, ftes: 11,
      prod: 0.5, flow: 2.9, shield: 0.0, recov: 2.4,
      why: "Prevents store backroom gridlock by pacing DC replenishment pushes to actual receiving bay capacity."
    },
    port_drayage_orchestrator: {
      tier: "next", paybackDays: 110, ftes: 9,
      prod: 0.5, flow: 2.8, shield: 3.7, recov: 0.0,
      why: "Coordinates port container drayage and urban night-curfew delivery windows to avoid port demurrage and city congestion fines."
    },
    geocoding_intelligence_agent: {
      tier: "next", paybackDays: 105, ftes: 10,
      prod: 0.5, flow: 2.4, shield: 1.1, recov: 1.8,
      why: "Fixes ambiguous apartment and rural delivery pins via Google Maps validation to raise first-attempt delivery success rates."
    },
    multimodal_mode_shift_agent: {
      tier: "next", paybackDays: 100, ftes: 10,
      prod: 0.5, flow: 4.5, shield: 1.6, recov: 0.0,
      why: "Shifts parcels and mid-mile freight dynamically between internal fleet, rail intermodal, and 3PL rate cards as fuel and capacity move."
    },
    freight_control_tower: {
      tier: "next", paybackDays: 95, ftes: 9,
      prod: 0.5, flow: 3.1, shield: 4.3, recov: 0.0,
      why: "Enforces primary routing-guide tender waterfall compliance so spot-market broker leakage is flagged before dispatch."
    },

    // 06 · Returns & Reverse Logistics (9 agents: 3 first, 5 next, 1 routine)
    reverse_rma_optimizer: {
      tier: "first", paybackDays: 45, ftes: 12,
      prod: 0.6, flow: 0.0, shield: 8.2, recov: 3.1,
      why: "Against the National Retail Federation (NRF) 16.9% returns rate, multimodal fraud scoring catches wardrobing/empty-box abuse prior to refund issuance."
    },
    dynamic_markdown_agent: {
      tier: "first", paybackDays: 50, ftes: 11,
      prod: 0.5, flow: 1.6, shield: 0.0, recov: 8.7,
      why: "Triggers electronic shelf-label (ESL) dynamic price drops on short-dated fresh/seasonal stock early to convert waste into recovered margin."
    },
    rti_balance_reconciler: {
      tier: "first", paybackDays: 60, ftes: 9,
      prod: 0.5, flow: 4.2, shield: 2.9, recov: 2.1,
      why: "Reconciles RFID portal scans against CHEP/PECO pooled pallet statements to halt $10M+ annual hoarding fines and lost tote CapEx."
    },
    keep_it_routing_advisor: {
      tier: "next", paybackDays: 90, ftes: 10,
      prod: 0.5, flow: 1.8, shield: 1.4, recov: 3.6,
      why: "Calculates net reverse shipping + refurbishment vs item margin in real time to authorize profitable 'returnless keep-it' refunds."
    },
    osd_freight_claims_agent: {
      tier: "next", paybackDays: 95, ftes: 10,
      prod: 0.6, flow: 0.0, shield: 5.4, recov: 0.0,
      why: "Automates Over, Short & Damaged (OS&D) evidence packet assembly within strict 9-month carrier claim filing windows."
    },
    short_dated_redistributor: {
      tier: "next", paybackDays: 115, ftes: 8,
      prod: 0.4, flow: 1.7, shield: 1.1, recov: 3.4,
      why: "Matches expiring DC inventory to secondary discount brokers or tax-deductible food banks before disposal fees hit."
    },
    intermodal_rail_linehaul_agent: {
      tier: "next", paybackDays: 110, ftes: 8,
      prod: 0.4, flow: 3.9, shield: 0.0, recov: 1.1,
      why: "Eliminates dedicated reverse freight by backhauling collapsed totes, pallets, and RMAs on empty store return delivery legs."
    },
    sanitation_health_agent: {
      tier: "next", paybackDays: 120, ftes: 8,
      prod: 0.4, flow: 0.0, shield: 4.1, recov: 0.0,
      why: "Enforces food-safety allergen wash logs and structural fatigue cycle limits on every reusable container."
    },
    food_waste_esg_copilot: {
      tier: "routine", paybackDays: 165, ftes: 6,
      prod: 0.5, flow: 0.0, shield: 1.9, recov: 0.9,
      why: "Automates closed-loop landfill diversion reporting and circular packaging Environmental, Social & Governance (ESG) tax credits."
    }
  };

  // Helper to round to 1 decimal place cleanly
  function r1(n) { return Math.round((n || 0) * 10) / 10; }

  // Build lookup keyed by persona (using SC_DATA if already loaded, or via computeEstate())
  function computeForPersonas(personas) {
    var byPersonaId = {};
    var byDeptId = {};
    var estateTotals = {
      prod: 0, flow: 0, shield: 0, recov: 0, total: 0,
      savedHrsWk: 0, personas: 0,
      firstCount: 0, nextCount: 0, routineCount: 0
    };

    (personas || []).forEach(function (p) {
      var agId = p.primaryAgentId;
      var entry = BY_AGENT[agId] || {
        tier: "next", paybackDays: 120, ftes: 8,
        prod: 0.4, flow: 1.5, shield: 1.5, recov: 1.0,
        why: "Eliminates cross-system manual reconciliation while grounding operational decisions in BigQuery Cortex v7."
      };
      var total = r1(entry.prod + entry.flow + entry.shield + entry.recov);
      var rec = {
        personaId: p.id,
        agentId: agId,
        deptId: p.deptId,
        tier: entry.tier,
        paybackDays: entry.paybackDays,
        ftes: entry.ftes,
        prod: entry.prod,
        flow: entry.flow,
        shield: entry.shield,
        recov: entry.recov,
        total: total,
        why: entry.why
      };
      byPersonaId[p.id] = rec;

      if (!byDeptId[p.deptId]) {
        byDeptId[p.deptId] = {
          prod: 0, flow: 0, shield: 0, recov: 0, total: 0,
          savedHrsWk: 0, personas: 0, firstCount: 0, nextCount: 0, routineCount: 0
        };
      }
      var d = byDeptId[p.deptId];
      d.prod = r1(d.prod + entry.prod);
      d.flow = r1(d.flow + entry.flow);
      d.shield = r1(d.shield + entry.shield);
      d.recov = r1(d.recov + entry.recov);
      d.total = r1(d.total + total);
      d.savedHrsWk += (p.savedHrs || 0);
      d.personas += 1;
      if (entry.tier === "first") d.firstCount += 1;
      else if (entry.tier === "next") d.nextCount += 1;
      else d.routineCount += 1;

      estateTotals.prod = r1(estateTotals.prod + entry.prod);
      estateTotals.flow = r1(estateTotals.flow + entry.flow);
      estateTotals.shield = r1(estateTotals.shield + entry.shield);
      estateTotals.recov = r1(estateTotals.recov + entry.recov);
      estateTotals.total = r1(estateTotals.total + total);
      estateTotals.savedHrsWk += (p.savedHrs || 0);
      estateTotals.personas += 1;
      if (entry.tier === "first") estateTotals.firstCount += 1;
      else if (entry.tier === "next") estateTotals.nextCount += 1;
      else estateTotals.routineCount += 1;
    });

    return {
      byPersonaId: byPersonaId,
      byDeptId: byDeptId,
      estateTotals: estateTotals
    };
  }

  return {
    ESTATE_BASELINE: ESTATE_BASELINE,
    LEVERS: LEVERS,
    BY_AGENT: BY_AGENT,
    computeForPersonas: computeForPersonas
  };
})();

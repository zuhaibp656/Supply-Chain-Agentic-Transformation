# 🎬 Supply Chain AI Agents — Complete Testing, Demo Data & Video Recording Playbook

> **Purpose of This Playbook**: A clear, step-by-step reference for all **60 Built Supply Chain AI Agents** across the 6 SCOR Operating Pillars. For every agent, this document explains:
> 1. **What the Agent Does** (simple 3-line explanation ready for your video voiceover).
> 2. **What Demo Data It Uses** (exact fixture tables, sample SKUs/Orders/Plants, and seeded anomalies).
> 3. **What the Agent Will Do During the Test** (which read tools it calls, how it solves the problem, what safety gate it checks, and what ERP/WMS write-back + visual `VegaChart` it produces).
> 4. **How to Test It Immediately** (1-click copy-paste prompts and terminal commands).

---

## 🚀 Quick-Start: 4 Ways to Run & Record Any Agent Tomorrow

### Method 1: Instant 1-Line CLI Demo Runner (Recommended for Quick Verification & Terminal Demos)
We built a dedicated CLI helper (`scripts/test_agent_demo.py`) that runs any of the 60 agents end-to-end, prints the executed ERP/WMS write-back receipts, shows the A2UI `VegaChart` metadata, and outputs the formatted Markdown report & copy-ready table:
```bash
# 1. Run an agent's full autonomous scenario (Read -> Solve -> Safety Gate -> Write-Back + Markdown Report):
python3 scripts/test_agent_demo.py demand_sensing_agent

# 2. Inspect the agent's Demo Data tables and sample rows before recording:
python3 scripts/test_agent_demo.py demand_sensing_agent --show-data

# 3. Test the Pre-Execution Governance / Safety Gate (shows how missing idempotency_key is blocked):
python3 scripts/test_agent_demo.py demand_sensing_agent --test-guardrail

# 4. List all 60 built agents grouped by SCOR Pillar:
python3 scripts/test_agent_demo.py --list
```

### Method 2: Interactive Local Google ADK Web UI (Best for Browser Screen Recording)
Launch the Google ADK Web UI locally to chat with any of the 60 agents, watch live tool calls (`query_*` and `action_*`), and record the interactive session:
```bash
adk web agents --port 8080
# Then open http://localhost:8080 in Chrome, select the agent from the top-left dropdown, and paste the Demo Prompt from below!
```

### Method 3: Automated Pytest Smoke Test Suite (Verifies All 7 Unit & Governance Tests per Agent)
```bash
# Test a single agent:
pytest agents/demand_sensing_agent/tests/test_smoke.py -v

# Or run all 60 agent smoke test suites (420+ tests):
pytest agents/*/tests/test_smoke.py -v
```

### Method 4: Gemini Enterprise Web UI (For the 14 Cloud-Deployed Flagship Agents in `zuhaibp-ai`)
- **GCP Project**: `zuhaibp-ai` (`632239123109`, Region: `us-central1`)
- **Gemini Enterprise App Engine**: `gemini-enterprise-zuhaibp_1784012666241`
- **Dynamic Orchestrator Model Routing**: Every agent automatically routes high-speed telemetry/lookup queries to **`Gemini 3.8 Flash` (`gemini-3.8-flash`)** and escalates complex multi-echelon optimization/trade-offs to **`Gemini 3.1 Pro / 4 Argon` (`gemini-3.1-pro` / `gemini-4-argon`, subject to availability)**.

---

## 🗄️ Shared Enterprise Demo Data Universe (`XYZ Global Industries Corp. — XYZ-CORP-01`)

All 60 agents are grounded on deterministic, interconnected enterprise demo data so you never get empty results or hallucinated numbers:

| Data Asset Layer | Location in Repository / Cloud | Count | Key Shared Entity IDs You Can Mention in Prompts |
|:---|:---|---:|:---|
| **Per-Agent Fixture Tables (`.json`)** | `agents/<agent_id>/fixtures/tables/*.json` | **245 Tables** | `SKU-BEV-ISOTONIC-32OZ`, `SKU-SEMI-9900-X1`, `SKU-CRYO-4410-BIO` |
| **Exported CSV & JSON Tables** | `demo_data/tables/*.csv` & `*.json` | **245 Tables** | `ORD-XYZ-2026-99401`, `SHP-XYZ-90884`, `RMA-2026-7741` |
| **BigQuery Digital Twin Dataset** | `zuhaibp-ai:supply_chain_twin` | **149 Tables** | `FAC-PLANT-US-AUS01`, `DC-DALLAS-CENTRAL`, `VND-T1-TSMC-TW01` |
| **Multi-Tab Excel Workbooks (`.xlsx`)** | `demo_data/xyz_corporation/excel/` | **7 Workbooks (43 Tabs)** | `XYZ_Corp_00_Global_ERP_Master_and_Org_Data.xlsx` – `06_Return_RMA...xlsx` |
| **Corporate PDFs (`.pdf`)** | `demo_data/xyz_corporation/pdfs/` | **7 Multi-Page PDFs** | Master Supplier MSA, Lab COA, Commercial Invoice & BOL, EU CBAM Cert |
| **Computer Vision PNG Feeds (`.png`)** | `demo_data/xyz_corporation/images/` | **8 HD Vision Frames** | Dock Door #14 QR Scan, VisionInspect Seal Defect, ShelfVision Planogram |
| **SOPs, Emails & X12 EDI Streams** | `demo_data/xyz_corporation/docs/` | **6 Docs/EDI Files** | ANSI X12 852 POS, 856 ASN, 204 Motor Carrier Load Tender, 214 Status |

---

## 01 · Planning & Strategy (12 Agents)

### 1. Demand Sensing Agent (`demand_sensing_agent`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **Demand Forecasting**
- **Primary Human Persona**: Demand Planner / Forecaster · **ROI Badge**: `Detects demand shifts 7–14 days earlier` · 🟢 **Live Vertex AI RE**: `6872242617594150912`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Demand Forecasting, Demand Planner / Forecaster teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Demand Sensing Agent intervenes.
2. **What the Agent Does**: Synthesizes POS velocity, weather anomalies, and macro trends.
3. **Expected Outcome**: Detects demand shifts 7–14 days earlier. (**Detects demand shifts 7–14 days earlier**).

#### 🗄️ Demo Data Details (`agents/demand_sensing_agent/fixtures/tables/`)
- **`external_signals_weathernext.json`** (3 rows) — Columns: `signal_id, provider, region, event_type, temperature_anomaly_celsius, precipitation_anomaly_mm` · Sample Record: `signal_id=SIG-WN3-TX-HEAT`, `provider=Google DeepMind WeatherNext 3`, `region=US-CENTRAL`, `event_type=UNSEASONABLE_HEATWAVE`
- **`fva_sales_bias.json`** (2 rows) — Columns: `override_id, sku_id, sales_account, planner_id, statistical_baseline_units, sales_override_units` · Sample Record: `override_id=OVR-SALES-202610-01`, `sku_id=SKU-BEV-ISOTONIC-32OZ`, `sales_account=Key Account Walmart`, `planner_id=REP-JOHNSON-CENTRAL`
- **`pos_store_scans.json`** (6 rows) — Columns: `store_id, retailer, region, sku_id, category, daily_scan_units` · Sample Record: `store_id=STORE-WALMART-DAL-104`, `retailer=Walmart`, `region=US-CENTRAL`, `sku_id=SKU-BEV-ISOTONIC-32OZ`
- **`timesfm_quantile_horizons.json`** (3 rows) — Columns: `forecast_id, sku_id, region, horizon_days, p10_units, p50_units` · Sample Record: `forecast_id=TFM-FC-202610-001`, `sku_id=SKU-BEV-ISOTONIC-32OZ`, `region=US-CENTRAL`, `horizon_days=14`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_pos_store_scans, query_external_demand_signals, query_timesfm_forecast_horizons` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Time-Series Forecasting Foundation Model + BigQuery ML Hierarchical Bayesian Censored-Demand Imputation**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_ibp_pir_change, action_suppress_fva_bias` (Supply Planning System (MCP / API) Key Figure & BAPI_PIR_CHANGE Write-Back (P10/P50/P90) via MCP / REST / On-Prem Gateway) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Demand Forecasting signals for Demand Sensing Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_ibp_pir_change immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py demand_sensing_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py demand_sensing_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py demand_sensing_agent --test-guardrail

# Run unit smoke tests:
pytest agents/demand_sensing_agent/tests/test_smoke.py -v
```

---

### 2. Forecast Reconciliation (`cpfr_sync_agent`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **Demand Forecasting**
- **Primary Human Persona**: Commercial Planning Lead · **ROI Badge**: `Replaces black-box variance models`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Demand Forecasting, Commercial Planning Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Forecast Reconciliation intervenes.
2. **What the Agent Does**: Identifies unmodeled drivers across eCommerce and retail channels.
3. **Expected Outcome**: Replaces black-box variance models. (**Replaces black-box variance models**).

#### 🗄️ Demo Data Details (`agents/cpfr_sync_agent/fixtures/tables/`)
- **`joint_cpfr_consensus_packets.json`** (2 rows) — Columns: `packet_id, retailer, sku_id, retailer_forecast_units, manufacturer_unconstrained_units, variance_gap_units` · Sample Record: `packet_id=CPFR-PKT-202611-WMT`, `retailer=Walmart`, `sku_id=SKU-BEV-ISOTONIC-32OZ`, `retailer_forecast_units=620000`
- **`retailer_edi830_order_forecasts.json`** (2 rows) — Columns: `forecast_id, retailer, sku_id, horizon_weeks, current_week_order_units, forward_4wk_projected_units` · Sample Record: `forecast_id=EDI830-WMT-202611`, `retailer=Walmart`, `sku_id=SKU-BEV-ISOTONIC-32OZ`, `horizon_weeks=12`
- **`retailer_edi852_daily_pos.json`** (3 rows) — Columns: `edi_record_id, retailer, store_id, region, sku_id, scan_date` · Sample Record: `edi_record_id=EDI852-20261016-01`, `retailer=Walmart`, `store_id=STORE-WALMART-DAL-104`, `region=US-CENTRAL`
- **`store_phantom_inventory_anomalies.json`** (2 rows) — Columns: `anomaly_id, store_id, retailer, sku_id, book_inventory_units, consecutive_zero_scan_days` · Sample Record: `anomaly_id=PHANTOM-KROGER-ATL-01`, `store_id=STORE-KROGER-ATL-209`, `retailer=Kroger`, `sku_id=SKU-BEV-ISOTONIC-32OZ`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_retailer_edi852_pos, query_retailer_edi830_forecasts, query_phantom_inventory_anomalies` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **BigQuery ML Zero-Scan Poisson Anomaly Detector + Vertex AI ADK CPFR Consensus Reconciler**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_dispatch_vmi_replenishment_order, action_flag_retail_phantom_audit` (EDI 855 / VMI Replenishment Order & Retail Store Audit Trigger via MCP / REST / On-Prem Gateway) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Demand Forecasting signals for Forecast Reconciliation, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_dispatch_vmi_replenishment_order immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py cpfr_sync_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py cpfr_sync_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py cpfr_sync_agent --test-guardrail

# Run unit smoke tests:
pytest agents/cpfr_sync_agent/tests/test_smoke.py -v
```

---

### 3. NPI Demand Profiler (`npi_demand_profiler`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **Demand Forecasting**
- **Primary Human Persona**: Brand & Innovation Manager · **ROI Badge**: `Cuts 90-day launch forecast errors`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Demand Forecasting, Brand & Innovation Manager teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before NPI Demand Profiler intervenes.
2. **What the Agent Does**: Matches launch packaging and attributes to historical lookalikes.
3. **Expected Outcome**: Cuts 90-day launch forecast errors. (**Cuts 90-day launch forecast errors**).

#### 🗄️ Demo Data Details (`agents/npi_demand_profiler/fixtures/tables/`)
- **`npi_demand_profiler_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=NPI_DE-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Demand Forecasting`
- **`npi_demand_profiler_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=NPI_DE-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Brand & Innovation Manager`
- **`npi_demand_profiler_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=01 · Plan | Demand Forecasting`, `service_level_pct=88.4`
- **`npi_demand_profiler_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=NPI_DE-TEL-101`, `company_id=XYZ-CORP-01`, `category=01 · Planning & Strategy — Demand Forecasting`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_npi_demand_profiler_telemetry_feed, query_npi_demand_profiler_constraint_matrix, query_npi_demand_profiler_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Time-Series Forecasting Foundation Model + BigQuery ML Hierarchical Bayesian Censored-Demand Imputation**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_npi_demand_profiler_plan, action_dispatch_npi_demand_profiler_alert` (Supply Planning System (MCP / API) Key Figure & BAPI_PIR_CHANGE Write-Back (P10/P50/P90) via MCP / REST / On-Prem Gateway) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Demand Forecasting signals for NPI Demand Profiler, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_npi_demand_profiler_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py npi_demand_profiler

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py npi_demand_profiler --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py npi_demand_profiler --test-guardrail

# Run unit smoke tests:
pytest agents/npi_demand_profiler/tests/test_smoke.py -v
```

---

### 4. Promo ROI Simulator (`promo_lift_simulator`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **Trade Promotion**
- **Primary Human Persona**: Trade Marketing Manager · **ROI Badge**: `Prevents break-even trade leakage`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Trade Promotion, Trade Marketing Manager teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Promo ROI Simulator intervenes.
2. **What the Agent Does**: Simulates price elasticity, shelf lift, and incremental spend return.
3. **Expected Outcome**: Prevents break-even trade leakage. (**Prevents break-even trade leakage**).

#### 🗄️ Demo Data Details (`agents/promo_lift_simulator/fixtures/tables/`)
- **`causal_promo_elasticity.json`** (3 rows) — Columns: `sku_id, base_price_usd, discounted_price_usd, price_elasticity, baseline_units, gross_lift_units` · Sample Record: `sku_id=SKU-BEV-ISOTONIC-32OZ`, `base_price_usd=2.99`, `discounted_price_usd=2.24`, `price_elasticity=-2.45`
- **`cross_sku_cannibalization.json`** (3 rows) — Columns: `promoted_sku, cannibalized_sku, cannibalization_rate_pct, volume_diverted_units, margin_loss_per_unit_usd, total_cannibalization_loss_usd` · Sample Record: `promoted_sku=SKU-BEV-ISOTONIC-32OZ`, `cannibalized_sku=SKU-BEV-ISOTONIC-16OZ`, `cannibalization_rate_pct=18.5`, `volume_diverted_units=16000`
- **`planned_promo_campaigns.json`** (3 rows) — Columns: `campaign_id, name, retailer, channel, start_date, end_date` · Sample Record: `campaign_id=CMP-202611-BOGO`, `name=BOGO Hydration Blitz`, `retailer=Walmart`, `channel=Retail Stores & Omnichannel`
- **`warehouse_promo_availability.json`** (3 rows) — Columns: `sku_id, distribution_center, available_to_promise_units, promo_surge_forecast_units, buffer_safety_stock_units, post_promo_stockout_risk` · Sample Record: `sku_id=SKU-BEV-ISOTONIC-32OZ`, `distribution_center=DC-DALLAS-CENTRAL`, `available_to_promise_units=95000`, `promo_surge_forecast_units=85000`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_planned_promo_campaigns, query_causal_promo_elasticity, query_cross_sku_cannibalization` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **BigQuery ML Causal Double-ML Uplift + Cross-SKU Cannibalization Matrix + Mathematical Optimization Solver (MILP / CP-SAT) Supply-Aware Price Shaper**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_shape_promotional_mechanic, action_lock_tpm_calendar` (Salesforce / SAP Trade Promo Calendar Lock & Shaped Regional SKU Curve Update) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Trade Promotion signals for Promo ROI Simulator, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_shape_promotional_mechanic immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py promo_lift_simulator

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py promo_lift_simulator --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py promo_lift_simulator --test-guardrail

# Run unit smoke tests:
pytest agents/promo_lift_simulator/tests/test_smoke.py -v
```

---

### 5. JBP Negotiation Agent (`field_beat_distributor_sync_agent`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **Trade Promotion**
- **Primary Human Persona**: Key Account Manager (KAM) · **ROI Badge**: `Aligns buyer margins and volume goals`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Trade Promotion, Key Account Manager (KAM) teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before JBP Negotiation Agent intervenes.
2. **What the Agent Does**: Creates customized sell-in story decks and joint promotional calendars.
3. **Expected Outcome**: Aligns buyer margins and volume goals. (**Aligns buyer margins and volume goals**).

#### 🗄️ Demo Data Details (`agents/field_beat_distributor_sync_agent/fixtures/tables/`)
- **`distributor_dms_live_inventory.json`** (2 rows) — Columns: `distributor_id, sku_id, on_hand_cases, stock_status, substitute_sku_id, substitute_on_hand_cases` · Sample Record: `distributor_id=DIST-MUM-WEST-04`, `sku_id=SKU-BEV-500ML`, `on_hand_cases=0`, `stock_status=STOCKED_OUT`
- **`fso_daily_beat_store_outlets.json`** (1 rows) — Columns: `fso_id, beat_id, planned_outlets, high_propensity_outlets, route_time_saved_mins, productive_call_rate_pct` · Sample Record: `fso_id=FSO-WEST-112`, `beat_id=BEAT-ANDHERI-NORTH`, `planned_outlets=38`, `high_propensity_outlets=28`
- **`pitch_to_stock_substitution_rules.json`** (1 rows) — Columns: `rule_id, stocked_out_sku, recommended_in_stock_sku, cross_elasticity_retention_pct, dealer_margin_bonus_pct` · Sample Record: `rule_id=SUB-BEV-01`, `stocked_out_sku=SKU-BEV-500ML`, `recommended_in_stock_sku=SKU-BEV-750ML-PROMO`, `cross_elasticity_retention_pct=94.2`
- **`primary_replenishment_auto_orders.json`** (1 rows) — Columns: `primary_so_id, distributor_id, sku_id, replenish_cases, source_cfa_depot, eta_hours` · Sample Record: `primary_so_id=SO-PRIM-20261022-55`, `distributor_id=DIST-MUM-WEST-04`, `sku_id=SKU-BEV-500ML`, `replenish_cases=600`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_distributor_dms_live_inventory, query_fso_daily_beat_store_outlets, query_pitch_to_stock_substitution_rules` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Geospatial Routing & Traffic API CVRPTW Beat Sequencer + Real-Time DMS Inventory Reconciliation Broker + Smart Variant Recommender**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_push_fso_dynamic_beat_and_pitch_list, action_trigger_distributor_primary_replenishment` (Live Handheld SKU Catalog Override, Secondary Order Booking in DMS & Optimized Daily Route Sheet) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Trade Promotion signals for JBP Negotiation Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_push_fso_dynamic_beat_and_pitch_list immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py field_beat_distributor_sync_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py field_beat_distributor_sync_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py field_beat_distributor_sync_agent --test-guardrail

# Run unit smoke tests:
pytest agents/field_beat_distributor_sync_agent/tests/test_smoke.py -v
```

---

### 6. Deduction Audit Agent (`trade_scheme_claims_reconciler`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **Trade Promotion**
- **Primary Human Persona**: Revenue / Trade Finance Lead · **ROI Badge**: `Resolves claim disputes in hours`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Trade Promotion, Revenue / Trade Finance Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Deduction Audit Agent intervenes.
2. **What the Agent Does**: Audits scanned proof-of-performance circulars and invoices via OCR.
3. **Expected Outcome**: Resolves claim disputes in hours. (**Resolves claim disputes in hours**).

#### 🗄️ Demo Data Details (`agents/trade_scheme_claims_reconciler/fixtures/tables/`)
- **`active_trade_promotion_schemes.json`** (1 rows) — Columns: `scheme_id, scheme_name, min_slab_cases, rebate_pct, requires_shelfvision_pass, valid_window` · Sample Record: `scheme_id=SCH-FEST-Q4-2026`, `scheme_name=Q4 Festive Volume Slab & Display Rebate`, `min_slab_cases=50`, `rebate_pct=6.5`
- **`claim_anomaly_audit_findings.json`** (1 rows) — Columns: `audit_id, claim_id, flagged_invoices, anomaly_type, disallowed_leakage_usd, verified_net_payout_usd` · Sample Record: `audit_id=CLM-AUD-9921`, `claim_id=CLM-DIST04-9921`, `flagged_invoices=['INV-SEC-8812', 'INV-SEC-8819']`, `anomaly_type=POST_SCHEME_WINDOW_AND_DUPLICATE_GSTIN`
- **`distributor_secondary_claim_submissions.json`** (1 rows) — Columns: `claim_id, distributor_id, scheme_id, submitted_invoices_count, claimed_amount_usd` · Sample Record: `claim_id=CLM-DIST04-9921`, `distributor_id=DIST-MUM-WEST-04`, `scheme_id=SCH-FEST-Q4-2026`, `submitted_invoices_count=142`
- **`sap_fi_credit_note_settlements.json`** (1 rows) — Columns: `credit_note_id, claim_id, approved_amount_usd, leakage_blocked_usd, settlement_cycle_hours` · Sample Record: `credit_note_id=SAP-CN-20261022-88`, `claim_id=CLM-DIST04-9921`, `approved_amount_usd=16260.0`, `leakage_blocked_usd=2190.0`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_active_trade_promotion_schemes, query_distributor_secondary_claim_submissions, query_claim_anomaly_audit_findings` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Deterministic Secondary Sales Volume Slab Engine + BigQuery Phantom Invoice Anomaly Classifier + ERP Credit Note Broker**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_flag_phantom_invoice_for_audit_hold, action_post_sap_fi_trade_credit_note` (Enterprise ERP (MCP / On-Prem DB) Credit Memo (FB01/VF01), Distributor Statement Reconciliation & Instant Settlement Notice) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Trade Promotion signals for Deduction Audit Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_flag_phantom_invoice_for_audit_hold immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py trade_scheme_claims_reconciler

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py trade_scheme_claims_reconciler --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py trade_scheme_claims_reconciler --test-guardrail

# Run unit smoke tests:
pytest agents/trade_scheme_claims_reconciler/tests/test_smoke.py -v
```

---

### 7. Consensus & Gap Agent (`sop_scenario_weaver`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **S&OP / IBP**
- **Primary Human Persona**: S&OP / Supply Planning Dir. · **ROI Badge**: `Highlights margin-dilutive imbalances` · 🟢 **Live Vertex AI RE**: `8086384929635565568`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In S&OP / IBP, S&OP / Supply Planning Dir. teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Consensus & Gap Agent intervenes.
2. **What the Agent Does**: Reconciles unconstrained demand with factory plant bottleneck limits.
3. **Expected Outcome**: Highlights margin-dilutive imbalances. (**Highlights margin-dilutive imbalances**).

#### 🗄️ Demo Data Details (`agents/sop_scenario_weaver/fixtures/tables/`)
- **`plant_line_capacities.json`** (3 rows) — Columns: `facility_id, line_id, process_type, standard_rate_units_per_hr, current_shifts_per_week, max_shifts_per_week` · Sample Record: `facility_id=PLANT-CINCINNATI-01`, `line_id=LINE-PKG-03`, `process_type=Aseptic Bottling & Retort Autoclave`, `standard_rate_units_per_hr=12500`
- **`sop_scenario_tradeoffs.json`** (3 rows) — Columns: `scenario_id, name, description, revenue_usd, gross_margin_usd, gross_margin_pct` · Sample Record: `scenario_id=SCEN-01-UNCONSTRAINED`, `name=Unconstrained Sales Forecast Plan`, `description=Produce strictly to unconstrained commercial forecast without overtime or alternate routing.`, `revenue_usd=68400000.0`
- **`sop_unconstrained_demand.json`** (3 rows) — Columns: `plan_month, business_unit, product_family, unconstrained_demand_units, constrained_supply_units, gap_units` · Sample Record: `plan_month=2026-11`, `business_unit=Consumer Packaged Goods`, `product_family=Hydration RTD`, `unconstrained_demand_units=4800000`
- **`supplier_component_allocations.json`** (2 rows) — Columns: `supplier_id, supplier_name, component_id, monthly_allocation_units, committed_to_orders_units, remaining_quota_units` · Sample Record: `supplier_id=VEND-BALL-CORP-101`, `supplier_name=Ball Metal Packaging`, `component_id=COMP-CAN-ALUM-330ML`, `monthly_allocation_units=5000000`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_unconstrained_demand_gaps, query_plant_line_capacities, query_supplier_allocations` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Gemini 3.1 Pro + Multi-Hop Constraint Graph DB + Mathematical Optimization Solver (MILP / CP-SAT) Multi-Objective MILP Capacity & Margin Solver**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_mps_consensus_plan, action_lock_sop_financial_bridge` (Enterprise Planning & ERP (MCP / On-Prem / API) Master Production Schedule (MPS) & Financial P&L Bridge Commit) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live S&OP / IBP signals for Consensus & Gap Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_mps_consensus_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py sop_scenario_weaver

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py sop_scenario_weaver --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py sop_scenario_weaver --test-guardrail

# Run unit smoke tests:
pytest agents/sop_scenario_weaver/tests/test_smoke.py -v
```

---

### 8. Digital War-Room Agent (`disruption_war_room_orchestrator`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **S&OP / IBP**
- **Primary Human Persona**: Supply Chain VP / COO · **ROI Badge**: `Rapid OTIF impact scenario brief` · 🟢 **Live Vertex AI RE**: `1211217885989437440`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In S&OP / IBP, Supply Chain VP / COO teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Digital War-Room Agent intervenes.
2. **What the Agent Does**: Evaluates co-packer shifts and allocation trade-offs during supply outages.
3. **Expected Outcome**: Rapid OTIF impact scenario brief. (**Rapid OTIF impact scenario brief**).

#### 🗄️ Demo Data Details (`agents/disruption_war_room_orchestrator/fixtures/tables/`)
- **`incident_war_rooms.json`** (1 rows) — Columns: `incident_id, title, severity, created_at, status, owner` · Sample Record: `incident_id=INC-WR-2026-001`, `title=Red Sea Bab-el-Mandeb Houthis Missile Reroute`, `severity=CRITICAL`, `created_at=2026-10-10T12:00:00Z`
- **`maritime_ais_vessels.json`** (2 rows) — Columns: `vessel_imo, vessel_name, carrier, current_lat, current_lon, speed_knots` · Sample Record: `vessel_imo=9811000`, `vessel_name=EVER GLOBE`, `carrier=Evergreen Line`, `current_lat=23.9`
- **`news_disruptions.json`** (2 rows) — Columns: `signal_id, timestamp, source, headline, summary, entities_extracted` · Sample Record: `signal_id=NEWS-9014`, `timestamp=2026-10-15T18:30:00Z`, `source=Reuters Global Logistics Wire`, `headline=Dockworker Union Strikes Paralyze Antwerp Container Terminal Operations`
- **`supplier_facilities.json`** (2 rows) — Columns: `supplier_id, supplier_name, tier_level, parent_tier1_vendor, facility_name, country` · Sample Record: `supplier_id=VEND-10492`, `supplier_name=Taiwan Micro-Power Semiconductor Corp`, `tier_level=2`, `parent_tier1_vendor=VEND-8820 (Bosch Mobility Electronics)`
- **`weather_alerts.json`** (2 rows) — Columns: `alert_id, event_type, severity, region, lat, lon` · Sample Record: `alert_id=WX-2026-0812`, `event_type=TYPHOON`, `severity=CRITICAL`, `region=East China Sea / Taiwan Strait`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_weather_alerts, query_maritime_ais_vessels, query_resilinc_supplier_facilities` across the 5 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Weather & Climate Ensemble Feed Ensemble Probabilistic Impact Model + Multi-Hop Graph Database (Cloud / On-Prem) + Mathematical Optimization Solver (MILP / CP-SAT) Multi-Modal War-Room MILP Solver**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_create_war_room_incident, action_dispatch_expedite_remediation` (Coordinated Pre-Positioning STOs, Backup Supplier POs, Sea/Air/Rail/Road Mode Reroutes & Plant Shift Re-Slotting) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live S&OP / IBP signals for Digital War-Room Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_create_war_room_incident immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py disruption_war_room_orchestrator

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py disruption_war_room_orchestrator --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py disruption_war_room_orchestrator --test-guardrail

# Run unit smoke tests:
pytest agents/disruption_war_room_orchestrator/tests/test_smoke.py -v
```

---

### 9. Executive Copilot (`csco_control_tower_copilot`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **S&OP / IBP**
- **Primary Human Persona**: IBP Lead / Chief Planning Off. · **ROI Badge**: `Reduces deck preparation by days` · 🟢 **Live Vertex AI RE**: `2865587061606318080`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In S&OP / IBP, IBP Lead / Chief Planning Off. teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Executive Copilot intervenes.
2. **What the Agent Does**: Generates pre-read decks and tracks sign-offs across cross-functional leads.
3. **Expected Outcome**: Reduces deck preparation by days. (**Reduces deck preparation by days**).

#### 🗄️ Demo Data Details (`agents/csco_control_tower_copilot/fixtures/tables/`)
- **`cross_erp_order_backlog.json`** (2 rows) — Columns: `order_id, order_type, customer, destination_country, total_value_usd, required_delivery_date` · Sample Record: `order_id=SO-8840192`, `order_type=CUSTOMER_SALES_ORDER`, `customer=Global Auto Group North America`, `destination_country=USA`
- **`executive_playbooks.json`** (2 rows) — Columns: `playbook_id, name, target_bottleneck_type, max_authorized_budget_usd, actions, expected_roi` · Sample Record: `playbook_id=PLAYBOOK-INTERMODAL-AIR-EXPEDITE`, `name=Suez Re-Route Critical Air Freight Bridge & Lateral DC Rebalance`, `target_bottleneck_type=GEOPOLITICAL_TRANSIT_REROUTE`, `max_authorized_budget_usd=1500000`
- **`multiechelon_twin_status.json`** (3 rows) — Columns: `node_id, name, echelon_level, capacity_utilization_pct, inventory_value_usd, days_of_supply` · Sample Record: `node_id=NODE-CENTRAL-US`, `name=Chicago Central Fulfillment Mega-Hub`, `echelon_level=1`, `capacity_utilization_pct=91.2`
- **`network_bottlenecks.json`** (3 rows) — Columns: `bottleneck_id, location, region, bottleneck_type, severity, revenue_impact_usd` · Sample Record: `bottleneck_id=BN-SUEZ-041`, `location=Red Sea / Suez Canal Maritime Chokepoint`, `region=EMEA`, `bottleneck_type=GEOPOLITICAL_TRANSIT_REROUTE`
- **`sc_kpi_summary.json`** (4 rows) — Columns: `region, period, otif_delivery_pct, otif_target_pct, days_inventory_outstanding_dio, dio_target` · Sample Record: `region=GLOBAL`, `period=CURRENT_MONTH`, `otif_delivery_pct=94.2`, `otif_target_pct=98.0`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_executive_kpis, query_network_bottlenecks, query_multiechelon_twin_status` across the 5 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Gemini 3.1 Pro Conversational Analytics + Looker Governed Semantic Layer + Multi-Hop Graph Database (Cloud / On-Prem) + A2A Cross-Domain Action Router**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_execute_executive_playbook, action_rebalance_network_allocation` (Signed Role-Based Action Dispatch across Enterprise ERP (MCP / On-Prem DB), IBP, WMS, TMS, CargoWise & Ariba via MCP / REST / On-Prem Gateway) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live S&OP / IBP signals for Executive Copilot, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_execute_executive_playbook immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py csco_control_tower_copilot

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py csco_control_tower_copilot --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py csco_control_tower_copilot --test-guardrail

# Run unit smoke tests:
pytest agents/csco_control_tower_copilot/tests/test_smoke.py -v
```

---

### 10. SKU Pruning Agent (`working_capital_cash_bridge`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **Portfolio & SKU**
- **Primary Human Persona**: Category Manager · **ROI Badge**: `Unlocks tail working capital`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Portfolio & SKU, Category Manager teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before SKU Pruning Agent intervenes.
2. **What the Agent Does**: Scores velocity, plant changeover cost, and shelf revenue yield.
3. **Expected Outcome**: Unlocks tail working capital. (**Unlocks tail working capital**).

#### 🗄️ Demo Data Details (`agents/working_capital_cash_bridge/fixtures/tables/`)
- **`inventory_valuation_ledger.json`** (3 rows) — Columns: `valuation_area, valuation_class, material_id, material_description, total_stock_units, standard_cost_per_unit_usd` · Sample Record: `valuation_area=PLANT-1010`, `valuation_class=3000_FINISHED_GOODS`, `material_id=MAT-880019`, `material_description=High-Voltage Power Inverter Module 800V SiC`
- **`supplier_ap_invoices.json`** (2 rows) — Columns: `invoice_id, vendor_id, vendor_name, invoice_amount_usd, invoice_date, standard_net_due_date` · Sample Record: `invoice_id=INV-AP-489012`, `vendor_id=VEND-10492`, `vendor_name=Taiwan Micro-Power Semiconductor Corp`, `invoice_amount_usd=940000.0`
- **`trapped_cash_opportunities.json`** (2 rows) — Columns: `opportunity_id, valuation_area, material_id, category, priority_rank, cash_freed_usd` · Sample Record: `opportunity_id=OPP-CASH-001`, `valuation_area=DC-DALLAS-CENTRAL`, `material_id=MAT-HVAC-901`, `category=SLOW_MOVING_BUFFER_REDUCTION`
- **`working_capital_metrics.json`** (3 rows) — Columns: `business_unit, region, cash_conversion_cycle_days, target_ccc_days, days_inventory_outstanding_dio, dio_target` · Sample Record: `business_unit=GLOBAL_ENTERPRISE`, `region=GLOBAL`, `cash_conversion_cycle_days=72.4`, `target_ccc_days=54.0`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_working_capital_metrics, query_inventory_valuation_ledger, query_trapped_cash_opportunities` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Mathematical Optimization Solver (MILP / CP-SAT) Stochastic Cash-Conversion-Cycle (DSI + DSO - DPO) Optimizer + BigQuery Real-Time Margin & COGS Bridge**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_rebalance_working_capital_buffer, action_trigger_dynamic_ap_discounting` (Joint CSCO–CFO Scenario Sign-Off, Dynamic Discounting Trigger & Working-Capital Budget Lock in Enterprise ERP (MCP / On-Prem DB)) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Portfolio & SKU signals for SKU Pruning Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_rebalance_working_capital_buffer immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py working_capital_cash_bridge

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py working_capital_cash_bridge --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py working_capital_cash_bridge --test-guardrail

# Run unit smoke tests:
pytest agents/working_capital_cash_bridge/tests/test_smoke.py -v
```

---

### 11. PIPO Run-Out Agent (`eco_cutover_orchestrator`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **Portfolio & SKU**
- **Primary Human Persona**: Lifecycle / Materials Mgr · **ROI Badge**: `Eliminates stranded write-offs`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Portfolio & SKU, Lifecycle / Materials Mgr teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before PIPO Run-Out Agent intervenes.
2. **What the Agent Does**: Orchestrates transition buffers to sync packaging and formulation cuts.
3. **Expected Outcome**: Eliminates stranded write-offs. (**Eliminates stranded write-offs**).

#### 🗄️ Demo Data Details (`agents/eco_cutover_orchestrator/fixtures/tables/`)
- **`eco_optimal_cutover_schedules.json`** (1 rows) — Columns: `schedule_id, eco_id, optimal_effectivity_date, supplier_po_converted_to_rev_c, obsolete_scrap_writeoff_usd, scrap_avoided_usd` · Sample Record: `schedule_id=CUT-ECO-8841`, `eco_id=ECO-2026-8841`, `optimal_effectivity_date=2026-11-11`, `supplier_po_converted_to_rev_c=2800`
- **`erp_bom_effectivity_sync_audit.json`** (1 rows) — Columns: `sync_id, eco_id, open_po_id, sap_bom_status, npi_launch_on_time` · Sample Record: `sync_id=SYNC-SAP-8841`, `eco_id=ECO-2026-8841`, `open_po_id=PO-ARIBA-55910`, `sap_bom_status=EFFECTIVITY_ALIGNED_TO_RUNOUT`
- **`multi_plant_predecessor_inventory_runout.json`** (2 rows) — Columns: `eco_id, plant_id, predecessor_on_hand_units, open_supplier_po_units, daily_burn_rate_units, uncoordinated_scrap_exposure_usd` · Sample Record: `eco_id=ECO-2026-8841`, `plant_id=PLANT-AUSTIN-01`, `predecessor_on_hand_units=4200`, `open_supplier_po_units=2800`
- **`plm_engineering_change_orders.json`** (1 rows) — Columns: `eco_id, assembly_sku, predecessor_part, successor_part, change_class, interchangeable` · Sample Record: `eco_id=ECO-2026-8841`, `assembly_sku=ASM-INVERTER-GEN4`, `predecessor_part=PCB-DRV-REV-B`, `successor_part=PCB-DRV-REV-C`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_plm_engineering_change_orders, query_multi_plant_predecessor_inventory_runout, query_eco_optimal_cutover_schedules` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Low-Latency Transactional State DB eBOM-to-mBOM Graph Verifier + Mathematical Optimization Solver (MILP / CP-SAT) Multi-Plant BOM Burn-Down & Effectivity Date MILP**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_lock_multi_plant_eco_effectivity_dates, action_modify_open_supplier_po_revision` (SAP Engineering Change Master (CC02) Effectivity Lock & e-Procurement & Sourcing Portal (MCP / API) Supplier PO Revision Swap) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Portfolio & SKU signals for PIPO Run-Out Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_lock_multi_plant_eco_effectivity_dates immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py eco_cutover_orchestrator

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py eco_cutover_orchestrator --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py eco_cutover_orchestrator --test-guardrail

# Run unit smoke tests:
pytest agents/eco_cutover_orchestrator/tests/test_smoke.py -v
```

---

### 12. Cost-to-Serve Diagnostic (`network_twin_architect`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **Portfolio & SKU**
- **Primary Human Persona**: Commercial Finance Director · **ROI Badge**: `Re-engineers MOQ and pack rules`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Portfolio & SKU, Commercial Finance Director teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Cost-to-Serve Diagnostic intervenes.
2. **What the Agent Does**: Calculates net-net margin across Club, Grocery, and eCommerce packs.
3. **Expected Outcome**: Re-engineers MOQ and pack rules. (**Re-engineers MOQ and pack rules**).

#### 🗄️ Demo Data Details (`agents/network_twin_architect/fixtures/tables/`)
- **`center_of_gravity_milp_scenarios.json`** (1 rows) — Columns: `scenario_id, scenario_name, stem_miles_reduction_pct, annual_net_savings_usd, 1_day_ground_coverage_pct` · Sample Record: `scenario_id=SCEN-COG-SE-2026`, `scenario_name=Southeast 3PL Node Addition & Territory Realignment`, `stem_miles_reduction_pct=14.6`, `annual_net_savings_usd=6840000.0`
- **`network_facility_nodes_and_leases.json`** (2 rows) — Columns: `facility_id, facility_type, annual_lease_usd, capacity_pallets_yr, handling_cost_per_pallet_usd, utilization_pct` · Sample Record: `facility_id=RDC-COLUMBUS-OH`, `facility_type=REGIONAL_DC`, `annual_lease_usd=4200000.0`, `capacity_pallets_yr=480000`
- **`network_stress_test_simulations.json`** (1 rows) — Columns: `stress_test_id, shock_event, recommended_shift, duty_and_freight_saved_usd` · Sample Record: `stress_test_id=STRESS-TARIFF-60PCT`, `shock_event=60% Section 301 Tariff + East Coast Port Congestion`, `recommended_shift=Nearshore Monterrey MX + Savannah/Houston Split`, `duty_and_freight_saved_usd=11200000.0`
- **`sku_customer_cost_to_serve_matrix.json`** (1 rows) — Columns: `customer_segment_id, avg_order_pallets, each_pick_cost_usd, stem_miles_from_ohio, net_operating_margin_pct, remediated_margin_pct` · Sample Record: `customer_segment_id=SEG-SOUTHEAST-L2`, `avg_order_pallets=1.5`, `each_pick_cost_usd=184.0`, `stem_miles_from_ohio=685`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_network_facility_nodes_and_leases, query_sku_customer_cost_to_serve_matrix, query_center_of_gravity_milp_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **BigQuery Activity-Based Landed Cost-to-Serve Attribution + Mathematical Optimization Solver (MILP / CP-SAT) Capacitated Facility Location & Multi-Modal Flow MILP**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_publish_network_territory_realignment, action_update_cost_to_serve_order_policy` (ERP Order Management (SD / MCP) Customer MOQ / Bracket Pricing Policy Update & Enterprise ERP (MCP / On-Prem DB) Sourcing Assignment Split) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Portfolio & SKU signals for Cost-to-Serve Diagnostic, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_publish_network_territory_realignment immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py network_twin_architect

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py network_twin_architect --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py network_twin_architect --test-guardrail

# Run unit smoke tests:
pytest agents/network_twin_architect/tests/test_smoke.py -v
```

---

## 02 · Sourcing & Procurement (9 Agents)

### 13. Disruption Sensing Agent (`tier_n_risk_sentinel`)
- **Pillar / Sub-Pillar**: 02 · Sourcing & Procurement — **Supplier Network**
- **Primary Human Persona**: Procurement Dir. / Risk Mgr · **ROI Badge**: `2–3 week advance disruption warning` · 🟢 **Live Vertex AI RE**: `5121890474918936576`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Supplier Network, Procurement Dir. / Risk Mgr teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Disruption Sensing Agent intervenes.
2. **What the Agent Does**: Monitors multi-tier supply feeds, port delays, and vendor financials.
3. **Expected Outcome**: 2–3 week advance disruption warning. (**2–3 week advance disruption warning**).

#### 🗄️ Demo Data Details (`agents/tier_n_risk_sentinel/fixtures/tables/`)
- **`active_disruption_threats.json`** (2 rows) — Columns: `threat_id, threat_type, region, impacted_node_id, supplier_name, disruption_severity` · Sample Record: `threat_id=THREAT-CYCLONE-QLD-01`, `threat_type=CATEGORY_4_TROPICAL_CYCLONE`, `region=Queensland, Australia`, `impacted_node_id=NODE-WEIPA-BAUXITE-AU`
- **`bom_finished_good_lineage.json`** (2 rows) — Columns: `impacted_subtier_node, component_id, tier_depth, finished_goods_impacted, total_revenue_at_risk_usd, factory_line_down_buffer_days` · Sample Record: `impacted_subtier_node=NODE-WEIPA-BAUXITE-AU`, `component_id=ORE-BAUXITE-METALLURGICAL`, `tier_depth=4`, `finished_goods_impacted=[{'sku_id': 'SKU-BEV-ISOTONIC-32OZ', 'product_name': 'Hydration RTD 32oz Can', 'monthly_volume_units': 4500000, 'revenue_at_risk_usd': 13455000.0}, {'sku_id': 'SKU-BEV-ELECTROLYTE-500ML', 'product_name': 'Electrolyte Recovery 500ml', 'monthly_volume_units': 1200000, 'revenue_at_risk_usd': 4788000.0}]`
- **`mitigation_playbook_options.json`** (2 rows) — Columns: `playbook_id, threat_id, impacted_component, primary_supplier_impacted, backup_qualified_supplier, target_po_reallocation_units` · Sample Record: `playbook_id=PB-DUAL-SOURCE-ALUM`, `threat_id=THREAT-CYCLONE-QLD-01`, `impacted_component=RAW-ALUM-INGOT-P1020A`, `primary_supplier_impacted=Alcoa International Smelter (IS)`
- **`subtier_supplier_network.json`** (4 rows) — Columns: `node_id, supplier_name, tier_level, component_provided, facility_country, facility_city` · Sample Record: `node_id=NODE-BALL-US-01`, `supplier_name=Ball Metal Packaging`, `tier_level=1`, `component_provided=COMP-CAN-ALUM-330ML`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_subtier_network_nodes, query_active_disruption_threats, query_bom_revenue_lineage` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Low-Latency Transactional State DB Multi-Tier Knowledge Graph + Vertex AI GNN + Mathematical Optimization Solver (MILP / CP-SAT) Revenue-at-Risk BOM Mitigation Solver**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_dispatch_dual_source_po_split, action_surge_meio_safety_buffer` (e-Procurement & Sourcing Portal (MCP / API) / S/4HANA Dual-Source PO Split (BAPI_PO_CREATE1), MEIO Buffer Surge & ModalShift Expedite Booking) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Supplier Network signals for Disruption Sensing Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_dispatch_dual_source_po_split immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py tier_n_risk_sentinel

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py tier_n_risk_sentinel --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py tier_n_risk_sentinel --test-guardrail

# Run unit smoke tests:
pytest agents/tier_n_risk_sentinel/tests/test_smoke.py -v
```

---

### 14. Onboarding & Qual. Agent (`supplier_quality_sentinel`)
- **Pillar / Sub-Pillar**: 02 · Sourcing & Procurement — **Supplier Network**
- **Primary Human Persona**: Procurement Operations Lead · **ROI Badge**: `Cuts onboarding from weeks to <48h`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Supplier Network, Procurement Operations Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Onboarding & Qual. Agent intervenes.
2. **What the Agent Does**: Parses BRC/ISO audits, food-safety filings, and tax registrations.
3. **Expected Outcome**: Cuts onboarding from weeks to <48h. (**Cuts onboarding from weeks to <48h**).

#### 🗄️ Demo Data Details (`agents/supplier_quality_sentinel/fixtures/tables/`)
- **`cost_of_poor_quality_ledger.json`** (2 rows) — Columns: `copq_id, ticket_id, supplier_id, supplier_name, scrap_material_cost_usd, sorting_inspection_labor_usd` · Sample Record: `copq_id=COPQ-202610-8841`, `ticket_id=NCR-202610-0914`, `supplier_id=VEND-KYOCERA-PREC-09`, `supplier_name=Kyocera Precision Ceramics`
- **`quality_deviation_tickets.json`** (2 rows) — Columns: `ticket_id, inspection_lot_id, supplier_id, supplier_name, part_number, defect_category` · Sample Record: `ticket_id=NCR-202610-0914`, `inspection_lot_id=LOT-INSP-202610-8841`, `supplier_id=VEND-KYOCERA-PREC-09`, `supplier_name=Kyocera Precision Ceramics`
- **`spc_cpk_drift_metrics.json`** (2 rows) — Columns: `metric_id, supplier_id, part_number, production_line, sample_timestamp, target_nominal` · Sample Record: `metric_id=SPC-KY-ALN-2026W41`, `supplier_id=VEND-KYOCERA-PREC-09`, `part_number=PART-SUBSTRATE-ALN-01`, `production_line=LINE-SINTERING-04`
- **`supplier_coa_inspections.json`** (2 rows) — Columns: `inspection_lot_id, po_number, supplier_id, supplier_name, part_number, part_description` · Sample Record: `inspection_lot_id=LOT-INSP-202610-8841`, `po_number=PO-4500918231`, `supplier_id=VEND-KYOCERA-PREC-09`, `supplier_name=Kyocera Precision Ceramics`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_supplier_coa_inspections, query_spc_cpk_drift_metrics, query_quality_deviation_tickets` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Document AI & Gemini Multimodal COA Spec Verifier + BigQuery ML Bayesian SPC/Cpk Drift Predictor**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_quarantine_inspection_lot, action_trigger_8d_capa_debit` (Quality Management System (QMS / ERP) Inspection Lot Quarantine (BAPI_INSPLOT_SETUSAGEDECISION), 8D CAPA Workflow & COPQ Debit Note) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Supplier Network signals for Onboarding & Qual. Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_quarantine_inspection_lot immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py supplier_quality_sentinel

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py supplier_quality_sentinel --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py supplier_quality_sentinel --test-guardrail

# Run unit smoke tests:
pytest agents/supplier_quality_sentinel/tests/test_smoke.py -v
```

---

### 15. ESG & Scope 3 Auditor (`carbon_scope3_ledger`)
- **Pillar / Sub-Pillar**: 02 · Sourcing & Procurement — **Supplier Network**
- **Primary Human Persona**: Chief Sustainability Officer · **ROI Badge**: `Automates Scope 3 disclosure audits` · 🟢 **Live Vertex AI RE**: `1067102697913581568`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Supplier Network, Chief Sustainability Officer teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before ESG & Scope 3 Auditor intervenes.
2. **What the Agent Does**: Standardizes chain-of-custody certificates (RSPO/FSC) and packaging LCAs.
3. **Expected Outcome**: Automates Scope 3 disclosure audits. (**Automates Scope 3 disclosure audits**).

#### 🗄️ Demo Data Details (`agents/carbon_scope3_ledger/fixtures/tables/`)
- **`eu_cbam_embedded_carbon_declarations.json`** (1 rows) — Columns: `import_declaration_id, cn_code, supplier_smelter, imported_tonnes, primary_specific_emissions_tco2e_per_t, eu_default_penalty_tco2e_per_t` · Sample Record: `import_declaration_id=CBAM-EU-2026-Q4-09`, `cn_code=7606_12_92_ALUMINUM_SHEET`, `supplier_smelter=NORSK_HYDRO_RENEWABLE_EAF`, `imported_tonnes=120.0`
- **`eudr_earth_engine_plot_verifications.json`** (1 rows) — Columns: `plot_id, commodity, geojson_centroid, sentinel2_ndvi_change_post2020, deforestation_free_verified, eudr_due_diligence_ref` · Sample Record: `plot_id=PLOT-BR-PARA-4410`, `commodity=NATURAL_RUBBER_AND_PULP`, `geojson_centroid=-3.1190,-60.0217`, `sentinel2_ndvi_change_post2020=0.0`
- **`low_carbon_carrier_and_supplier_swaps.json`** (1 rows) — Columns: `swap_id, target_corridor_or_bom, recommended_partner, annual_tco2e_reduction, net_cost_delta_pct` · Sample Record: `swap_id=SWAP-DEC-2026-04`, `target_corridor_or_bom=DE_NL_RHINE_CORRIDOR`, `recommended_partner=HVO100_BIOFUEL_AND_ELECTRIC_BARGE`, `annual_tco2e_reduction=1420.0`
- **`shipment_level_scope3_emissions.json`** (1 rows) — Columns: `shipment_id, corridor, mode, payload_tonnes, distance_km, wtw_co2e_kg` · Sample Record: `shipment_id=SHP-GLB-20261022-301`, `corridor=Rotterdam➔Duisburg`, `mode=ELECTRIC_BARGE_AND_EV_TRUCK`, `payload_tonnes=42.0`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_shipment_level_scope3_emissions, query_eu_cbam_embedded_carbon_declarations, query_eudr_earth_engine_plot_verifications` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **BigQuery ISO-14083 Primary Telemetry Carbon Calculator + Earth Engine Canopy Verifier + Mathematical Optimization Solver (MILP / CP-SAT) Cost/Carbon Mode-Shift MILP**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_certify_cbam_and_eudr_compliance_dossier, action_commit_scope3_decarbonization_swap` (EU CBAM / EUDR XML Customs Filing & Transportation Management System (TMS / MCP) / Supply Chain Execution Platform (MCP / API) Low-Carbon Rail/EV/Ocean Lane Allocation) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Supplier Network signals for ESG & Scope 3 Auditor, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_certify_cbam_and_eudr_compliance_dossier immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py carbon_scope3_ledger

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py carbon_scope3_ledger --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py carbon_scope3_ledger --test-guardrail

# Run unit smoke tests:
pytest agents/carbon_scope3_ledger/tests/test_smoke.py -v
```

---

### 16. Commodity Index Advisor (`commodity_index_advisor`)
- **Pillar / Sub-Pillar**: 02 · Sourcing & Procurement — **Material & Packaging**
- **Primary Human Persona**: Category Sourcing Mgr (Direct) · **ROI Badge**: `Optimizes forward-contract windows`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Material & Packaging, Category Sourcing Mgr (Direct) teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Commodity Index Advisor intervenes.
2. **What the Agent Does**: Correlates CBOT/Platts feedstocks with depletion to advise hedging.
3. **Expected Outcome**: Optimizes forward-contract windows. (**Optimizes forward-contract windows**).

#### 🗄️ Demo Data Details (`agents/commodity_index_advisor/fixtures/tables/`)
- **`commodity_index_advisor_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=COMMOD-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Material & Packaging`
- **`commodity_index_advisor_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=COMMOD-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Category Sourcing Mgr (Direct)`
- **`commodity_index_advisor_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=02 · Source | Material & Packaging`, `service_level_pct=88.4`
- **`commodity_index_advisor_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=COMMOD-TEL-101`, `company_id=XYZ-CORP-01`, `category=02 · Sourcing & Procurement — Material & Packaging`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_commodity_index_advisor_telemetry_feed, query_commodity_index_advisor_constraint_matrix, query_commodity_index_advisor_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **BigQuery Parametric BOM Cost Tear-Down + Document AI Quote Parser + Mathematical Optimization Solver (MILP / CP-SAT) Combinatorial MILP Award Split Solver**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_commodity_index_advisor_plan, action_dispatch_commodity_index_advisor_alert` (e-Procurement & Sourcing Portal (MCP / API) Award Allocation, Redlined Negotiation Fact-Pack & SAP Purchasing Info-Record Update (ME12)) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Material & Packaging signals for Commodity Index Advisor, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_commodity_index_advisor_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py commodity_index_advisor

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py commodity_index_advisor --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py commodity_index_advisor --test-guardrail

# Run unit smoke tests:
pytest agents/commodity_index_advisor/tests/test_smoke.py -v
```

---

### 17. Dynamic Should-Cost Agent (`rfq_should_cost_agent`)
- **Pillar / Sub-Pillar**: 02 · Sourcing & Procurement — **Material & Packaging**
- **Primary Human Persona**: Strategic Sourcing Lead · **ROI Badge**: `Fact-based margin leverage in RFPs` · 🟢 **Live Vertex AI RE**: `7647283965966942208`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Material & Packaging, Strategic Sourcing Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Dynamic Should-Cost Agent intervenes.
2. **What the Agent Does**: Deconstructs packaging specs (resin weight, corrugate, conversion energy).
3. **Expected Outcome**: Fact-based margin leverage in RFPs. (**Fact-based margin leverage in RFPs**).

#### 🗄️ Demo Data Details (`agents/rfq_should_cost_agent/fixtures/tables/`)
- **`award_allocation_scenarios.json`** (2 rows) — Columns: `scenario_id, name, part_number, annual_demand_units, primary_supplier, primary_split_pct` · Sample Record: `scenario_id=SCEN-AWARD-DUAL-70-30`, `name=OR-Tools Optimal Dual-Source Risk & Cost Frontier`, `part_number=PART-CAN-ALUM-330ML`, `annual_demand_units=50000000`
- **`commodity_index_rates.json`** (3 rows) — Columns: `index_symbol, commodity, current_price_usd_per_mt, one_month_change_pct, three_month_forecast_usd_per_mt, effective_date` · Sample Record: `index_symbol=LME-ALUM-CASH`, `commodity=London Metal Exchange Primary Aluminum Cash`, `current_price_usd_per_mt=2420.0`, `one_month_change_pct=-2.4`
- **`material_should_cost_bom.json`** (2 rows) — Columns: `part_number, description, commodity_base, net_weight_grams, raw_material_cost_usd, stamping_die_cycle_sec` · Sample Record: `part_number=PART-CAN-ALUM-330ML`, `description=330ml Aluminum Beverage Can & Stay-on-Tab End`, `commodity_base=LME High Grade Aluminum (AL-99.7)`, `net_weight_grams=12.8`
- **`supplier_rfq_bids.json`** (3 rows) — Columns: `bid_id, part_number, supplier_id, supplier_name, quoted_unit_cost_usd, should_cost_gap_pct` · Sample Record: `bid_id=BID-BALL-2026-01`, `part_number=PART-CAN-ALUM-330ML`, `supplier_id=VEND-BALL-CORP-101`, `supplier_name=Ball Metal Packaging`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_material_should_cost_bom, query_commodity_index_rates, query_supplier_rfq_bids` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **BigQuery Parametric BOM Cost Tear-Down + Document AI Quote Parser + Mathematical Optimization Solver (MILP / CP-SAT) Combinatorial MILP Award Split Solver**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_award_supplier_contract, action_challenge_vendor_outlier` (e-Procurement & Sourcing Portal (MCP / API) Award Allocation, Redlined Negotiation Fact-Pack & SAP Purchasing Info-Record Update (ME12)) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Material & Packaging signals for Dynamic Should-Cost Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_award_supplier_contract immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py rfq_should_cost_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py rfq_should_cost_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py rfq_should_cost_agent --test-guardrail

# Run unit smoke tests:
pytest agents/rfq_should_cost_agent/tests/test_smoke.py -v
```

---

### 18. Sustainable Packaging Agent (`sustainable_packaging_agent`)
- **Pillar / Sub-Pillar**: 02 · Sourcing & Procurement — **Material & Packaging**
- **Primary Human Persona**: Packaging R&D Engineer · **ROI Badge**: `Mitigates EPR and landfill taxation`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Material & Packaging, Packaging R&D Engineer teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Sustainable Packaging Agent intervenes.
2. **What the Agent Does**: Evaluates PCR resins and barrier materials against line runnability & taxes.
3. **Expected Outcome**: Mitigates EPR and landfill taxation. (**Mitigates EPR and landfill taxation**).

#### 🗄️ Demo Data Details (`agents/sustainable_packaging_agent/fixtures/tables/`)
- **`sustainable_packaging_agent_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=SUSTAI-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Material & Packaging`
- **`sustainable_packaging_agent_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=SUSTAI-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Packaging R&D Engineer`
- **`sustainable_packaging_agent_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=02 · Source | Material & Packaging`, `service_level_pct=88.4`
- **`sustainable_packaging_agent_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=SUSTAI-TEL-101`, `company_id=XYZ-CORP-01`, `category=02 · Sourcing & Procurement — Material & Packaging`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_sustainable_packaging_agent_telemetry_feed, query_sustainable_packaging_agent_constraint_matrix, query_sustainable_packaging_agent_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **BigQuery ISO-14083 Primary Telemetry Carbon Calculator + Earth Engine Canopy Verifier + Mathematical Optimization Solver (MILP / CP-SAT) Cost/Carbon Mode-Shift MILP**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_sustainable_packaging_agent_plan, action_dispatch_sustainable_packaging_agent_alert` (EU CBAM / EUDR XML Customs Filing & Transportation Management System (TMS / MCP) / Supply Chain Execution Platform (MCP / API) Low-Carbon Rail/EV/Ocean Lane Allocation) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Material & Packaging signals for Sustainable Packaging Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_sustainable_packaging_agent_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py sustainable_packaging_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py sustainable_packaging_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py sustainable_packaging_agent --test-guardrail

# Run unit smoke tests:
pytest agents/sustainable_packaging_agent/tests/test_smoke.py -v
```

---

### 19. Contract Leakage Agent (`tariff_esg_agent`)
- **Pillar / Sub-Pillar**: 02 · Sourcing & Procurement — **Contract & PO Mgmt**
- **Primary Human Persona**: Commercial Sourcing / Legal · **ROI Badge**: `Recovers missed rebates & surcharges`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Contract & PO Mgmt, Commercial Sourcing / Legal teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Contract Leakage Agent intervenes.
2. **What the Agent Does**: Reconciles live spend against negotiated rebate tiers and volume discount scales.
3. **Expected Outcome**: Recovers missed rebates & surcharges. (**Recovers missed rebates & surcharges**).

#### 🗄️ Demo Data Details (`agents/tariff_esg_agent/fixtures/tables/`)
- **`contract_clause_obligations.json`** (2 rows) — Columns: `contract_id, supplier_id, supplier_name, effective_start, effective_end, clause_id` · Sample Record: `contract_id=MSA-BALL-2025-09`, `supplier_id=VEND-BALL-CORP-101`, `supplier_name=Ball Metal Packaging`, `effective_start=2025-01-01`
- **`cross_border_duty_impact.json`** (2 rows) — Columns: `entry_id, part_number, customs_port, declared_customs_value_usd, declared_hs_code, standard_duty_usd` · Sample Record: `entry_id=CUST-ENTRY-202610-01`, `part_number=PART-CAN-ALUM-330ML`, `customs_port=Port of New York / Newark`, `declared_customs_value_usd=485000.0`
- **`hs_tariff_classifications.json`** (2 rows) — Columns: `part_number, description, ten_digit_hs_code, wco_six_digit_heading, general_duty_rate_pct, preferential_fta_rate_pct` · Sample Record: `part_number=PART-CAN-ALUM-330ML`, `description=Aluminum Cans for Preserving Food or Drink (Capacity under 50 Liters)`, `ten_digit_hs_code=7612.90.1065`, `wco_six_digit_heading=7612.90`
- **`supplier_rebate_accruals.json`** (2 rows) — Columns: `accrual_id, contract_id, supplier_id, supplier_name, cumulative_spend_usd, actual_volume_units` · Sample Record: `accrual_id=REB-BALL-2026-YTD`, `contract_id=MSA-BALL-2025-09`, `supplier_id=VEND-BALL-CORP-101`, `supplier_name=Ball Metal Packaging`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_contract_clause_obligations, query_supplier_rebate_accruals, query_hs_tariff_classifications` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Document AI + Vector Search & Semantic Index (DB / MCP) Legal Contract RAG + Gemini 3.1 Pro Hierarchical HS Code Legal-Ruling Classifier**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_lock_hs_tariff_classification, action_issue_supplier_rebate_debit_memo` (Global Trade & Tariff System (MCP / API) 10-Digit HS Code Lock, FTA Certificate Filing & SAP AP Supplier Rebate Debit Memo) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Contract & PO Mgmt signals for Contract Leakage Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_lock_hs_tariff_classification immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py tariff_esg_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py tariff_esg_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py tariff_esg_agent --test-guardrail

# Run unit smoke tests:
pytest agents/tariff_esg_agent/tests/test_smoke.py -v
```

---

### 20. PO Expediting Agent (`master_data_leadtime_steward`)
- **Pillar / Sub-Pillar**: 02 · Sourcing & Procurement — **Contract & PO Mgmt**
- **Primary Human Persona**: Buyer / Procurement Coord. · **ROI Badge**: `Resolves ~70% of standard PO delays`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Contract & PO Mgmt, Buyer / Procurement Coord. teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before PO Expediting Agent intervenes.
2. **What the Agent Does**: Monitors EDI 855/856 delay feeds and orchestrates supplier split-shipments.
3. **Expected Outcome**: Resolves ~70% of standard PO delays. (**Resolves ~70% of standard PO delays**).

#### 🗄️ Demo Data Details (`agents/master_data_leadtime_steward/fixtures/tables/`)
- **`bom_routing_leadtimes.json`** (2 rows) — Columns: `bom_id, parent_material_id, component_count, critical_path_leadtime_days, system_recorded_leadtime_days, discrepancy_days` · Sample Record: `bom_id=BOM-EV-INVERTER-V2`, `parent_material_id=MAT-880019`, `component_count=48`, `critical_path_leadtime_days=46`
- **`dimension_audit_scans.json`** (2 rows) — Columns: `scan_id, material_id, scanned_plant, cubiscan_length_cm, recorded_length_cm, cubiscan_width_cm` · Sample Record: `scan_id=SCAN-3D-99014`, `material_id=MAT-880019`, `scanned_plant=PLANT-1010`, `cubiscan_length_cm=52.0`
- **`material_master_mara_marc.json`** (3 rows) — Columns: `material_id, description, material_type, base_uom, plant, mrp_type` · Sample Record: `material_id=MAT-880019`, `description=High-Voltage Power Inverter Module 800V SiC`, `material_type=FERT`, `base_uom=EA`
- **`vendor_master_records.json`** (2 rows) — Columns: `vendor_id, vendor_name, tax_id, country, bank_account_verification, incoterms` · Sample Record: `vendor_id=VEND-10492`, `vendor_name=Taiwan Micro-Power Semiconductor Corp`, `tax_id=TW-88401923`, `country=Taiwan`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_material_master_records, query_leadtime_drift_anomalies, query_cubiscan_dimension_discrepancies` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **BigQuery ML Empirical Bayesian Lead-Time Estimator + Isolation-Forest Master Anomaly Detector + Enterprise API & MCP Gateway SAP BAPI Steward**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_heal_material_leadtime, action_remediate_cubiscan_dimensions` (SAP BAPI_MATERIAL_SAVEDATA & Purchasing Info-Record Lead-Time / Route / 3D Dimension Auto-Update) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Contract & PO Mgmt signals for PO Expediting Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_heal_material_leadtime immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py master_data_leadtime_steward

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py master_data_leadtime_steward --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py master_data_leadtime_steward --test-guardrail

# Run unit smoke tests:
pytest agents/master_data_leadtime_steward/tests/test_smoke.py -v
```

---

### 21. Three-Way Match Dispute (`three_way_match_dispute`)
- **Pillar / Sub-Pillar**: 02 · Sourcing & Procurement — **Contract & PO Mgmt**
- **Primary Human Persona**: Accounts Payable Lead · **ROI Badge**: `Prevents vendor holds & saves discounts`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Contract & PO Mgmt, Accounts Payable Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Three-Way Match Dispute intervenes.
2. **What the Agent Does**: Diagnoses price/quantity discrepancies across POs, GRNs, and carrier invoices.
3. **Expected Outcome**: Prevents vendor holds & saves discounts. (**Prevents vendor holds & saves discounts**).

#### 🗄️ Demo Data Details (`agents/three_way_match_dispute/fixtures/tables/`)
- **`three_way_match_dispute_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=THREE_-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Contract & PO Mgmt`
- **`three_way_match_dispute_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=THREE_-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Accounts Payable Lead`
- **`three_way_match_dispute_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=02 · Source | Contract & PO Mgmt`, `service_level_pct=88.4`
- **`three_way_match_dispute_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=THREE_-TEL-101`, `company_id=XYZ-CORP-01`, `category=02 · Sourcing & Procurement — Contract & PO Mgmt`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_three_way_match_dispute_telemetry_feed, query_three_way_match_dispute_constraint_matrix, query_three_way_match_dispute_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Document AI + Vector Search & Semantic Index (DB / MCP) Legal Contract RAG + Gemini 3.1 Pro Hierarchical HS Code Legal-Ruling Classifier**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_three_way_match_dispute_plan, action_dispatch_three_way_match_dispute_alert` (Global Trade & Tariff System (MCP / API) 10-Digit HS Code Lock, FTA Certificate Filing & SAP AP Supplier Rebate Debit Memo) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Contract & PO Mgmt signals for Three-Way Match Dispute, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_three_way_match_dispute_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py three_way_match_dispute

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py three_way_match_dispute --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py three_way_match_dispute --test-guardrail

# Run unit smoke tests:
pytest agents/three_way_match_dispute/tests/test_smoke.py -v
```

---

## 03 · Manufacturing & Operations (9 Agents)

### 22. Changeover Optimizer (`finite_production_scheduler`)
- **Pillar / Sub-Pillar**: 03 · Manufacturing & Operations — **Production Scheduling**
- **Primary Human Persona**: Master Production Scheduler · **ROI Badge**: `Cuts sanitation downtime by 15–25%`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Production Scheduling, Master Production Scheduler teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Changeover Optimizer intervenes.
2. **What the Agent Does**: Sequences allergen, kosher, and packaging runs to minimize washdowns.
3. **Expected Outcome**: Cuts sanitation downtime by 15–25%. (**Cuts sanitation downtime by 15–25%**).

#### 🗄️ Demo Data Details (`agents/finite_production_scheduler/fixtures/tables/`)
- **`changeover_matrix_rules.json`** (3 rows) — Columns: `rule_id, from_product_family, to_product_family, changeover_type, setup_duration_hours, changeover_cost_usd` · Sample Record: `rule_id=CO-RULE-ALLERGEN-CLEANOUT`, `from_product_family=BEVERAGE_NUT_BASE`, `to_product_family=BEVERAGE_OAT_BASE`, `changeover_type=DEEP_ALLERGEN_CIP_WASH_ATP_SWAB`
- **`optimized_sequence_schedule.json`** (1 rows) — Columns: `schedule_id, workcenter_id, solver_engine, objective_value_min_changeover_hours, baseline_unoptimized_changeover_hours, changeover_hours_saved` · Sample Record: `schedule_id=SCHED-OR-TOOLS-2026W42-01`, `workcenter_id=WC-LINE-ASEPTIC-01`, `solver_engine=OR_TOOLS_CPSAT_SOLVER`, `objective_value_min_changeover_hours=4.5`
- **`plant_line_workcenters.json`** (2 rows) — Columns: `workcenter_id, workcenter_name, plant_id, max_throughput_liters_hr, current_scheduled_load_pct, cleaning_in_place_system` · Sample Record: `workcenter_id=WC-LINE-ASEPTIC-01`, `workcenter_name=Aseptic Tetra Pak High-Speed Filling Line 01`, `plant_id=PLANT-1020-AUSTIN`, `max_throughput_liters_hr=9000`
- **`production_orders_backlog.json`** (3 rows) — Columns: `order_id, material_id, material_description, product_family, allergen_group, order_quantity_liters` · Sample Record: `order_id=ORD-PROD-202610-771`, `material_id=SKU-BEV-OATMILK-ORIGINAL-1L`, `material_description=Organic Oat Milk Original 1L Tetra Brik`, `product_family=BEVERAGE_OAT_BASE`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_production_orders_backlog, query_changeover_matrix_rules, query_plant_line_workcenters` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Mathematical Optimization Solver (MILP / CP-SAT) CP-SAT Sequence-Dependent Setup & Finite Capacity Job-Shop Solver + Multi-Modal Outbound Cutoff Sync**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_solve_and_lock_finite_sequence, action_dispatch_sap_ppds_sequence` (SAP PP/DS Production Order Dispatch Sequence (BAPI_PRODORD_CHANGE) & Siemens MES Line Recipe Queue) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Production Scheduling signals for Changeover Optimizer, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_solve_and_lock_finite_sequence immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py finite_production_scheduler

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py finite_production_scheduler --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py finite_production_scheduler --test-guardrail

# Run unit smoke tests:
pytest agents/finite_production_scheduler/tests/test_smoke.py -v
```

---

### 23. Disruption Re-sequencer (`line_schedule_optimizer`)
- **Pillar / Sub-Pillar**: 03 · Manufacturing & Operations — **Production Scheduling**
- **Primary Human Persona**: Shop Floor / Shift Lead · **ROI Badge**: `Line reallocation in <3 minutes`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Production Scheduling, Shop Floor / Shift Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Disruption Re-sequencer intervenes.
2. **What the Agent Does**: Detects machine halts and re-routes perishable WIP to alternate lines.
3. **Expected Outcome**: Line reallocation in <3 minutes. (**Line reallocation in <3 minutes**).

#### 🗄️ Demo Data Details (`agents/line_schedule_optimizer/fixtures/tables/`)
- **`changeover_matrix_rules.json`** (3 rows) — Columns: `rule_id, from_product_family, to_product_family, changeover_type, setup_duration_hours, changeover_cost_usd` · Sample Record: `rule_id=CO-RULE-ALLERGEN-CLEANOUT`, `from_product_family=BEVERAGE_NUT_BASE`, `to_product_family=BEVERAGE_OAT_BASE`, `changeover_type=DEEP_ALLERGEN_CIP_WASH_ATP_SWAB`
- **`optimized_sequence_schedule.json`** (1 rows) — Columns: `schedule_id, workcenter_id, solver_engine, objective_value_min_changeover_hours, baseline_unoptimized_changeover_hours, changeover_hours_saved` · Sample Record: `schedule_id=SCHED-OR-TOOLS-2026W42-01`, `workcenter_id=WC-LINE-ASEPTIC-01`, `solver_engine=OR_TOOLS_CPSAT_SOLVER`, `objective_value_min_changeover_hours=4.5`
- **`plant_line_workcenters.json`** (2 rows) — Columns: `workcenter_id, workcenter_name, plant_id, max_throughput_liters_hr, current_scheduled_load_pct, cleaning_in_place_system` · Sample Record: `workcenter_id=WC-LINE-ASEPTIC-01`, `workcenter_name=Aseptic Tetra Pak High-Speed Filling Line 01`, `plant_id=PLANT-1020-AUSTIN`, `max_throughput_liters_hr=9000`
- **`production_orders_backlog.json`** (3 rows) — Columns: `order_id, material_id, material_description, product_family, allergen_group, order_quantity_liters` · Sample Record: `order_id=ORD-PROD-202610-771`, `material_id=SKU-BEV-OATMILK-ORIGINAL-1L`, `material_description=Organic Oat Milk Original 1L Tetra Brik`, `product_family=BEVERAGE_OAT_BASE`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_production_orders_backlog, query_changeover_matrix_rules, query_plant_line_workcenters` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Mathematical Optimization Solver (MILP / CP-SAT) CP-SAT Sequence-Dependent Setup & Finite Capacity Job-Shop Solver + Multi-Modal Outbound Cutoff Sync**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_solve_and_lock_finite_sequence, action_dispatch_sap_ppds_sequence` (SAP PP/DS Production Order Dispatch Sequence (BAPI_PRODORD_CHANGE) & Siemens MES Line Recipe Queue) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Production Scheduling signals for Disruption Re-sequencer, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_solve_and_lock_finite_sequence immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py line_schedule_optimizer

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py line_schedule_optimizer --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py line_schedule_optimizer --test-guardrail

# Run unit smoke tests:
pytest agents/line_schedule_optimizer/tests/test_smoke.py -v
```

---

### 24. Labor & Line Balancing (`labor_line_balancing_agent`)
- **Pillar / Sub-Pillar**: 03 · Manufacturing & Operations — **Production Scheduling**
- **Primary Human Persona**: Plant Operations Manager · **ROI Badge**: `Prevents certified skill bottlenecks`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Production Scheduling, Plant Operations Manager teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Labor & Line Balancing intervenes.
2. **What the Agent Does**: Maps shift skill certifications and fatigue constraints to line speeds.
3. **Expected Outcome**: Prevents certified skill bottlenecks. (**Prevents certified skill bottlenecks**).

#### 🗄️ Demo Data Details (`agents/labor_line_balancing_agent/fixtures/tables/`)
- **`labor_line_balancing_agent_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=LABOR_-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Production Scheduling`
- **`labor_line_balancing_agent_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=LABOR_-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Plant Operations Manager`
- **`labor_line_balancing_agent_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=03 · Make | Production Scheduling`, `service_level_pct=88.4`
- **`labor_line_balancing_agent_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=LABOR_-TEL-101`, `company_id=XYZ-CORP-01`, `category=03 · Manufacturing & Production — Production Scheduling`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_labor_line_balancing_agent_telemetry_feed, query_labor_line_balancing_agent_constraint_matrix, query_labor_line_balancing_agent_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Mathematical Optimization Solver (MILP / CP-SAT) CP-SAT Sequence-Dependent Setup & Finite Capacity Job-Shop Solver + Multi-Modal Outbound Cutoff Sync**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_labor_line_balancing_agent_plan, action_dispatch_labor_line_balancing_agent_alert` (SAP PP/DS Production Order Dispatch Sequence (BAPI_PRODORD_CHANGE) & Siemens MES Line Recipe Queue) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Production Scheduling signals for Labor & Line Balancing, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_labor_line_balancing_agent_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py labor_line_balancing_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py labor_line_balancing_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py labor_line_balancing_agent --test-guardrail

# Run unit smoke tests:
pytest agents/labor_line_balancing_agent/tests/test_smoke.py -v
```

---

### 25. Bottleneck Diagnostic (`predictive_oee_sentinel`)
- **Pillar / Sub-Pillar**: 03 · Manufacturing & Operations — **Capacity Planning**
- **Primary Human Persona**: Supply Chain Ops Director · **ROI Badge**: `Flags facility constraints 3–6 mos out` · 🟢 **Live Vertex AI RE**: `4659145613206618112`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Capacity Planning, Supply Chain Ops Director teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Bottleneck Diagnostic intervenes.
2. **What the Agent Does**: Assesses CIP utilities, boiler loads, and cold storage holding limits.
3. **Expected Outcome**: Flags facility constraints 3–6 mos out. (**Flags facility constraints 3–6 mos out**).

#### 🗄️ Demo Data Details (`agents/predictive_oee_sentinel/fixtures/tables/`)
- **`oee_breakdown_metrics.json`** (2 rows) — Columns: `metric_id, asset_id, production_line, shift_id, planned_production_time_min, operating_time_min` · Sample Record: `metric_id=OEE-MILLING-CNC-04-2026W42`, `asset_id=ASSET-MILLING-CNC-04`, `production_line=LINE-MACHINING-BAY-02`, `shift_id=SHIFT-MORNING-A`
- **`plant_machine_telemetry.json`** (2 rows) — Columns: `sensor_id, asset_id, asset_name, plant_id, component, timestamp` · Sample Record: `sensor_id=SENS-CNC-SPINDLE-VIB-01`, `asset_id=ASSET-MILLING-CNC-04`, `asset_name=5-Axis High-Precision Milling Center CNC-04`, `plant_id=PLANT-1020-AUSTIN`
- **`predictive_maintenance_anomalies.json`** (2 rows) — Columns: `anomaly_id, asset_id, asset_name, failure_mode, severity, estimated_time_to_failure_hours` · Sample Record: `anomaly_id=ANOM-CNC-04-VIB-992`, `asset_id=ASSET-MILLING-CNC-04`, `asset_name=5-Axis High-Precision Milling Center CNC-04`, `failure_mode=SPINDLE_FRONT_ROLLER_BEARING_FLAKING`
- **`spare_parts_inventory_status.json`** (2 rows) — Columns: `part_number, description, compatible_assets, stock_on_hand, reserved_quantity, available_quantity` · Sample Record: `part_number=PART-SPARE-BEARING-CERAMIC-7014`, `description=High-Precision Angular Contact Ceramic Spindle Bearing (7014-C-P4A)`, `compatible_assets=['ASSET-MILLING-CNC-04', 'ASSET-MILLING-CNC-05']`, `stock_on_hand=3`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_plant_machine_telemetry, query_oee_breakdown_metrics, query_predictive_maintenance_anomalies` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Vertex AI Multimodal Vibration/Acoustic Spectral Anomaly Model + Mathematical Optimization Solver (MILP / CP-SAT) Joint PM-Production Window MILP**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_dispatch_preventive_work_order, action_reserve_spare_parts` (Plant Maintenance System (EAM / ERP) Preventive Work Order (BAPI_ALM_ORDER_MAINTAIN), MRO Spare Reservation & Siemens MES Window Lock) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Capacity Planning signals for Bottleneck Diagnostic, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_dispatch_preventive_work_order immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py predictive_oee_sentinel

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py predictive_oee_sentinel --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py predictive_oee_sentinel --test-guardrail

# Run unit smoke tests:
pytest agents/predictive_oee_sentinel/tests/test_smoke.py -v
```

---

### 26. Co-Packer Allocation (`copacker_allocation_agent`)
- **Pillar / Sub-Pillar**: 03 · Manufacturing & Operations — **Capacity Planning**
- **Primary Human Persona**: External Sourcing / CMO Lead · **ROI Badge**: `Optimizes net gross margin per case`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Capacity Planning, External Sourcing / CMO Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Co-Packer Allocation intervenes.
2. **What the Agent Does**: Models internal conversion costs against co-packer tolling agreements.
3. **Expected Outcome**: Optimizes net gross margin per case. (**Optimizes net gross margin per case**).

#### 🗄️ Demo Data Details (`agents/copacker_allocation_agent/fixtures/tables/`)
- **`copacker_allocation_agent_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=COPACK-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Capacity Planning`
- **`copacker_allocation_agent_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=COPACK-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=External Sourcing / CMO Lead`
- **`copacker_allocation_agent_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=03 · Make | Capacity Planning`, `service_level_pct=88.4`
- **`copacker_allocation_agent_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=COPACK-TEL-101`, `company_id=XYZ-CORP-01`, `category=03 · Manufacturing & Production — Capacity Planning`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_copacker_allocation_agent_telemetry_feed, query_copacker_allocation_agent_constraint_matrix, query_copacker_allocation_agent_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Gemini 3.1 Pro + Multi-Hop Constraint Graph DB + Mathematical Optimization Solver (MILP / CP-SAT) Multi-Objective MILP Capacity & Margin Solver**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_copacker_allocation_agent_plan, action_dispatch_copacker_allocation_agent_alert` (Enterprise Planning & ERP (MCP / On-Prem / API) Master Production Schedule (MPS) & Financial P&L Bridge Commit) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Capacity Planning signals for Co-Packer Allocation, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_copacker_allocation_agent_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py copacker_allocation_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py copacker_allocation_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py copacker_allocation_agent --test-guardrail

# Run unit smoke tests:
pytest agents/copacker_allocation_agent/tests/test_smoke.py -v
```

---

### 27. CapEx Simulator (`capex_simulator_agent`)
- **Pillar / Sub-Pillar**: 03 · Manufacturing & Operations — **Capacity Planning**
- **Primary Human Persona**: VP Manufacturing Engineering · **ROI Badge**: `Delivers defensible board CapEx ROI`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Capacity Planning, VP Manufacturing Engineering teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before CapEx Simulator intervenes.
2. **What the Agent Does**: Simulates multi-year volume trends to test high-speed line expansions.
3. **Expected Outcome**: Delivers defensible board CapEx ROI. (**Delivers defensible board CapEx ROI**).

#### 🗄️ Demo Data Details (`agents/capex_simulator_agent/fixtures/tables/`)
- **`capex_simulator_agent_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=CAPEX_-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Capacity Planning`
- **`capex_simulator_agent_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=CAPEX_-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=VP Manufacturing Engineering`
- **`capex_simulator_agent_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=03 · Make | Capacity Planning`, `service_level_pct=88.4`
- **`capex_simulator_agent_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=CAPEX_-TEL-101`, `company_id=XYZ-CORP-01`, `category=03 · Manufacturing & Production — Capacity Planning`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_capex_simulator_agent_telemetry_feed, query_capex_simulator_agent_constraint_matrix, query_capex_simulator_agent_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **BigQuery Activity-Based Landed Cost-to-Serve Attribution + Mathematical Optimization Solver (MILP / CP-SAT) Capacitated Facility Location & Multi-Modal Flow MILP**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_capex_simulator_agent_plan, action_dispatch_capex_simulator_agent_alert` (ERP Order Management (SD / MCP) Customer MOQ / Bracket Pricing Policy Update & Enterprise ERP (MCP / On-Prem DB) Sourcing Assignment Split) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Capacity Planning signals for CapEx Simulator, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_capex_simulator_agent_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py capex_simulator_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py capex_simulator_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py capex_simulator_agent --test-guardrail

# Run unit smoke tests:
pytest agents/capex_simulator_agent/tests/test_smoke.py -v
```

---

### 28. Visual Defect Triager (`inline_yield_guardian`)
- **Pillar / Sub-Pillar**: 03 · Manufacturing & Operations — **Quality & Compliance**
- **Primary Human Persona**: QA Manager / Line Inspector · **ROI Badge**: `Prevents full pallet scrap & holds` · 🟢 **Live Vertex AI RE**: `2816047465705242624`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Quality & Compliance, QA Manager / Line Inspector teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Visual Defect Triager intervenes.
2. **What the Agent Does**: Inspects high-speed video frames for crimped seals, lot codes, and labels.
3. **Expected Outcome**: Prevents full pallet scrap & holds. (**Prevents full pallet scrap & holds**).

#### 🗄️ Demo Data Details (`agents/inline_yield_guardian/fixtures/tables/`)
- **`camera_vision_inspection_frames.json`** (2 rows) — Columns: `frame_id, camera_station_id, line_id, conveyor_speed_m_s, capture_timestamp, product_package_barcode` · Sample Record: `frame_id=FRAME-CAM01-20261022-00841`, `camera_station_id=STATION-VISION-LINE01-ENTRY`, `line_id=LINE-ASEPTIC-01`, `conveyor_speed_m_s=1.25`
- **`ebhr_batch_record_deviations.json`** (1 rows) — Columns: `deviation_id, batch_number, product_id, station_id, incident_timestamp, deviation_type` · Sample Record: `deviation_id=DEV-EBHR-20261022-044`, `batch_number=BATCH-OAT-2026W42-01`, `product_id=SKU-BEV-OATMILK-ORIGINAL-1L`, `station_id=STATION-VISION-LINE01-ENTRY`
- **`pneumatic_reject_gate_events.json`** (1 rows) — Columns: `event_id, frame_id, classification_id, line_id, pneumatic_diverter_id, actuation_latency_ms` · Sample Record: `event_id=REJ-GATE-20261022-00841`, `frame_id=FRAME-CAM01-20261022-00841`, `classification_id=CLS-FLASH-VISION-20261022-00841`, `line_id=LINE-ASEPTIC-01`
- **`vision_defect_classification_results.json`** (2 rows) — Columns: `classification_id, frame_id, defect_type, vision_model, confidence_score, bounding_box_normalized` · Sample Record: `classification_id=CLS-FLASH-VISION-20261022-00841`, `frame_id=FRAME-CAM01-20261022-00841`, `defect_type=INDUCTION_FOIL_SEAL_TEAR_MICRO_LEAK`, `vision_model=gemini-3.8-flash`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_camera_vision_inspection_frames, query_vision_defect_classification_results, query_ebhr_batch_record_deviations` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Vertex AI Edge Multimodal Vision Defect Classifier + BigQuery ML Bayesian Closed-Loop SPC Parameter Controller**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_trigger_pneumatic_reject_diverter, action_log_ebhr_quality_deviation` (Bounded PLC Recipe Offset Recommendation & Automated Quality Management System (QMS / ERP) Usage Decision (BAPI_INSPLOT_SETUSAGEDECISION)) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Quality & Compliance signals for Visual Defect Triager, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_trigger_pneumatic_reject_diverter immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py inline_yield_guardian

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py inline_yield_guardian --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py inline_yield_guardian --test-guardrail

# Run unit smoke tests:
pytest agents/inline_yield_guardian/tests/test_smoke.py -v
```

---

### 29. Batch Record Auditor (`batch_record_auditor`)
- **Pillar / Sub-Pillar**: 03 · Manufacturing & Operations — **Quality & Compliance**
- **Primary Human Persona**: Regulatory Compliance Lead · **ROI Badge**: `60–80% faster batch release review`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Quality & Compliance, Regulatory Compliance Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Batch Record Auditor intervenes.
2. **What the Agent Does**: Parses BPR and COA documents to flag pasteurization & CCP deviations.
3. **Expected Outcome**: 60–80% faster batch release review. (**60–80% faster batch release review**).

#### 🗄️ Demo Data Details (`agents/batch_record_auditor/fixtures/tables/`)
- **`batch_record_auditor_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=BATCH_-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Quality & Compliance`
- **`batch_record_auditor_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=BATCH_-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Regulatory Compliance Lead`
- **`batch_record_auditor_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=03 · Make | Quality & Compliance`, `service_level_pct=88.4`
- **`batch_record_auditor_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=BATCH_-TEL-101`, `company_id=XYZ-CORP-01`, `category=03 · Manufacturing & Production — Quality & Compliance`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_batch_record_auditor_telemetry_feed, query_batch_record_auditor_constraint_matrix, query_batch_record_auditor_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Vertex AI Edge Multimodal Vision Defect Classifier + BigQuery ML Bayesian Closed-Loop SPC Parameter Controller**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_batch_record_auditor_plan, action_dispatch_batch_record_auditor_alert` (Bounded PLC Recipe Offset Recommendation & Automated Quality Management System (QMS / ERP) Usage Decision (BAPI_INSPLOT_SETUSAGEDECISION)) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Quality & Compliance signals for Batch Record Auditor, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_batch_record_auditor_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py batch_record_auditor

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py batch_record_auditor --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py batch_record_auditor --test-guardrail

# Run unit smoke tests:
pytest agents/batch_record_auditor/tests/test_smoke.py -v
```

---

### 30. RCA & CAPA Copilot (`scrap_defect_root_cause_agent`)
- **Pillar / Sub-Pillar**: 03 · Manufacturing & Operations — **Quality & Compliance**
- **Primary Human Persona**: Continuous Improvement Lead · **ROI Badge**: `Speeds 5-Why investigation closures`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Quality & Compliance, Continuous Improvement Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before RCA & CAPA Copilot intervenes.
2. **What the Agent Does**: Correlates consumer complaints with ingredient lots and machine telemetry.
3. **Expected Outcome**: Speeds 5-Why investigation closures. (**Speeds 5-Why investigation closures**).

#### 🗄️ Demo Data Details (`agents/scrap_defect_root_cause_agent/fixtures/tables/`)
- **`batch_process_parameter_correlations.json`** (2 rows) — Columns: `correlation_id, defect_id, parameter_name, nominal_setpoint, actual_observed_mean, upper_tolerance_limit` · Sample Record: `correlation_id=CORR-FLASH-IMM-02-01`, `defect_id=DEF-FLASH-IMM-02`, `parameter_name=Injection Holding Pressure (bar)`, `nominal_setpoint=820.0`
- **`scada_setpoint_recommendations.json`** (1 rows) — Columns: `recommendation_id, asset_id, recipe_name, parameter_adjustments, projected_scrap_rate_after_pct, projected_cost_savings_per_shift_usd` · Sample Record: `recommendation_id=REC-SETPOINT-IMM-02-FLASH`, `asset_id=ASSET-INJECTION-MOLD-02`, `recipe_name=TETHERED_CAP_PP_HIGH_SPEED_V4`, `parameter_adjustments=[{'parameter_name': 'Injection Holding Pressure', 'current_val': 945.0, 'recommended_val': 820.0, 'unit': 'bar', 'delta': -125.0}, {'parameter_name': 'Barrel Zone 4 Temperature', 'current_val': 248.5, 'recommended_val': 235.0, 'unit': '°C', 'delta': -13.5}]`
- **`scrap_financial_cost_ledger.json`** (1 rows) — Columns: `ledger_id, production_order_id, asset_id, material_id, scrap_quantity_pieces, unit_material_cost_usd` · Sample Record: `ledger_id=SCRAP-LEDGER-202610-09`, `production_order_id=ORD-PROD-202610-771`, `asset_id=ASSET-INJECTION-MOLD-02`, `material_id=SKU-BEV-CAP-TETHERED-28MM`
- **`scrap_loss_pareto_records.json`** (3 rows) — Columns: `defect_id, defect_name, asset_id, production_line, scrap_units, total_lot_units` · Sample Record: `defect_id=DEF-FLASH-IMM-02`, `defect_name=Parting Line Polymer Flash Excess`, `asset_id=ASSET-INJECTION-MOLD-02`, `production_line=LINE-MOLDING-BAY-01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_scrap_loss_pareto_records, query_batch_process_parameter_correlations, query_scrap_financial_cost_ledger` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Vertex AI Edge Multimodal Vision Defect Classifier + BigQuery ML Bayesian Closed-Loop SPC Parameter Controller**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_update_scada_recipe_setpoints, action_post_scrap_variance_adjustment` (Bounded PLC Recipe Offset Recommendation & Automated Quality Management System (QMS / ERP) Usage Decision (BAPI_INSPLOT_SETUSAGEDECISION)) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Quality & Compliance signals for RCA & CAPA Copilot, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_update_scada_recipe_setpoints immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py scrap_defect_root_cause_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py scrap_defect_root_cause_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py scrap_defect_root_cause_agent --test-guardrail

# Run unit smoke tests:
pytest agents/scrap_defect_root_cause_agent/tests/test_smoke.py -v
```

---

## 04 · Logistics & Distribution (12 Agents)

### 31. Load Consolidation (`load_consolidation_agent`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **First & Mid-Mile**
- **Primary Human Persona**: Transport Planner / Inbound Mgr · **ROI Badge**: `12–18% higher trailer fill rate` · 🟢 **Live Vertex AI RE**: `3771936486614630400`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In First & Mid-Mile, Transport Planner / Inbound Mgr teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Load Consolidation intervenes.
2. **What the Agent Does**: Consolidates vendor LTLs into multi-stop FTL linehauls via cube & weight modeling.
3. **Expected Outcome**: 12–18% higher trailer fill rate. (**12–18% higher trailer fill rate**).

#### 🗄️ Demo Data Details (`agents/load_consolidation_agent/fixtures/tables/`)
- **`axle_weight_crush_audit_logs.json`** (1 rows) — Columns: `audit_id, load_plan_id, steer_axle_kg, drive_tandem_kg, trailer_tandem_kg, cog_lateral_offset_mm` · Sample Record: `audit_id=AXL-AUD-88`, `load_plan_id=LP-3D-20261022-88`, `steer_axle_kg=5120`, `drive_tandem_kg=14680`
- **`lifo_3d_voxel_load_plans.json`** (1 rows) — Columns: `load_plan_id, shipment_wave_id, trailer_type_id, cube_utilization_pct, weight_utilization_pct, lifo_sequence_order` · Sample Record: `load_plan_id=LP-3D-20261022-88`, `shipment_wave_id=WAVE-3D-20261022-09`, `trailer_type_id=TRL-53FT-DRYVAN`, `cube_utilization_pct=92.4`
- **`outbound_shipment_carton_dimensions.json`** (3 rows) — Columns: `pallet_group_id, shipment_wave_id, stop_number, Stop_Name, length_mm, width_mm` · Sample Record: `pallet_group_id=PLT-STOP3-HVY01`, `shipment_wave_id=WAVE-3D-20261022-09`, `stop_number=3`, `Stop_Name=San Antonio Depot`
- **`trailer_bay_geometry_specs.json`** (1 rows) — Columns: `trailer_type_id, internal_length_mm, internal_width_mm, internal_height_mm, max_payload_kg, max_steer_axle_kg` · Sample Record: `trailer_type_id=TRL-53FT-DRYVAN`, `internal_length_mm=15900`, `internal_width_mm=2480`, `internal_height_mm=2740`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_outbound_shipment_carton_dimensions, query_trailer_bay_geometry_specs, query_lifo_3d_voxel_load_plans` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Mathematical Optimization Solver (MILP / CP-SAT) 3D Guillotine Bin-Packing + Reverse-Stop LIFO Zoning + Longitudinal Axle Torque & CoG Solver**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_3d_lifo_load_plan, action_resequence_dock_staging_lanes` (Step-by-Step 3D Dock Loading Plan, Warehouse Management System (WMS / MCP) HU Packing Instruction & Certified Axle Weight Manifest) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live First & Mid-Mile signals for Load Consolidation, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_3d_lifo_load_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py load_consolidation_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py load_consolidation_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py load_consolidation_agent --test-guardrail

# Run unit smoke tests:
pytest agents/load_consolidation_agent/tests/test_smoke.py -v
```

---

### 32. Yard Disruption Agent (`yard_dock_sequencer`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **First & Mid-Mile**
- **Primary Human Persona**: Yard Master / Plant Logistics · **ROI Badge**: `Eliminates demurrage & line starvation`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In First & Mid-Mile, Yard Master / Plant Logistics teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Yard Disruption Agent intervenes.
2. **What the Agent Does**: Parses GPS & gate feeds to flag delays and reassign dock staging doors dynamically.
3. **Expected Outcome**: Eliminates demurrage & line starvation. (**Eliminates demurrage & line starvation**).

#### 🗄️ Demo Data Details (`agents/yard_dock_sequencer/fixtures/tables/`)
- **`carrier_detention_risk_records.json`** (1 rows) — Columns: `record_id, trailer_id, carrier_id, carrier_name, current_dwell_minutes, free_detention_threshold_minutes` · Sample Record: `record_id=DET-RISK-20261022-01`, `trailer_id=TRL-SWIFT-7741`, `carrier_id=CARRIER-SWIFT-TRANS`, `carrier_name=Swift Transportation`
- **`dock_door_turnaround_schedules.json`** (2 rows) — Columns: `door_id, facility_zone, assigned_trailer_id, door_status, target_dock_time, scheduled_unload_duration_minutes` · Sample Record: `door_id=DOOR-CROSSDOCK-08`, `facility_zone=CROSSDOCK_NORTH_QUADRANT`, `assigned_trailer_id=TRL-SWIFT-7741`, `door_status=READY_FOR_DOCKING`
- **`yard_spotter_move_tasks.json`** (1 rows) — Columns: `task_id, spotter_truck_id, operator_name, trailer_id, pickup_slot, target_door` · Sample Record: `task_id=SPOT-TASK-20261022-012`, `spotter_truck_id=SPOTTER-HOSTLER-03`, `operator_name=Marcus Vance`, `trailer_id=TRL-SWIFT-7741`
- **`yard_trailer_geofence_status.json`** (2 rows) — Columns: `trailer_id, carrier_id, carrier_name, yard_id, current_slot_id, geofence_entry_timestamp` · Sample Record: `trailer_id=TRL-SWIFT-7741`, `carrier_id=CARRIER-SWIFT-TRANS`, `carrier_name=Swift Transportation`, `yard_id=YARD-DALLAS-02`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_yard_trailer_geofence_status, query_yard_spotter_move_tasks, query_dock_door_turnaround_schedules` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Google Maps Live ETA + Mathematical Optimization Solver (MILP / CP-SAT) Bipartite Dock-Door Matching + Shortest-Path Hostler Task Interleaving**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_dispatch_yard_spotter_move, action_resolve_carrier_detention_alert` (YMS / Warehouse Management System (WMS / MCP) Dock Door Assignment, Driver SMS Gate Pass & Hostler Tablet Dispatch) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live First & Mid-Mile signals for Yard Disruption Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_dispatch_yard_spotter_move immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py yard_dock_sequencer

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py yard_dock_sequencer --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py yard_dock_sequencer --test-guardrail

# Run unit smoke tests:
pytest agents/yard_dock_sequencer/tests/test_smoke.py -v
```

---

### 33. Cold-Chain Auditor (`cold_chain_auditor`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **First & Mid-Mile**
- **Primary Human Persona**: Cold Chain QA / Logistics Dir. · **ROI Badge**: `Prevents perishable food spoilage`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In First & Mid-Mile, Cold Chain QA / Logistics Dir. teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Cold-Chain Auditor intervenes.
2. **What the Agent Does**: Analyzes reefer IoT telemetry to flag thermal excursions and file carrier claims.
3. **Expected Outcome**: Prevents perishable food spoilage. (**Prevents perishable food spoilage**).

#### 🗄️ Demo Data Details (`agents/cold_chain_auditor/fixtures/tables/`)
- **`cold_chain_auditor_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=COLD_C-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=First & Mid-Mile`
- **`cold_chain_auditor_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=COLD_C-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Cold Chain QA / Logistics Dir.`
- **`cold_chain_auditor_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=05 · Logistics | First & Mid-Mile`, `service_level_pct=88.4`
- **`cold_chain_auditor_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=COLD_C-TEL-101`, `company_id=XYZ-CORP-01`, `category=05 · Distribution & Logistics — First & Mid-Mile`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_cold_chain_auditor_telemetry_feed, query_cold_chain_auditor_constraint_matrix, query_cold_chain_auditor_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Pub/Sub + Dataflow Spatiotemporal ETA/Thermal Drift Predictor + Google Maps Geofence & Document AI Rate-Card Audit Engine**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_cold_chain_auditor_plan, action_dispatch_cold_chain_auditor_alert` (Automated Carrier Claim Dispute Packet & Approved Enterprise ERP (MCP / On-Prem DB) AP Freight Voucher (BAPI_INCOMINGINVOICE_CREATE)) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live First & Mid-Mile signals for Cold-Chain Auditor, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_cold_chain_auditor_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py cold_chain_auditor

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py cold_chain_auditor --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py cold_chain_auditor --test-guardrail

# Run unit smoke tests:
pytest agents/cold_chain_auditor/tests/test_smoke.py -v
```

---

### 34. Aisle-Aligned Pallet (`aisle_aligned_pallet_agent`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **Store Replenishment**
- **Primary Human Persona**: Outbound Lead / Industrial Eng. · **ROI Badge**: `Cuts store stocking labor by 20–35%`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Store Replenishment, Outbound Lead / Industrial Eng. teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Aisle-Aligned Pallet intervenes.
2. **What the Agent Does**: Sequences DC pick waves to match individual store planograms and shelf layouts.
3. **Expected Outcome**: Cuts store stocking labor by 20–35%. (**Cuts store stocking labor by 20–35%**).

#### 🗄️ Demo Data Details (`agents/aisle_aligned_pallet_agent/fixtures/tables/`)
- **`aisle_aligned_pallet_agent_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=AISLE_-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Store Replenishment`
- **`aisle_aligned_pallet_agent_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=AISLE_-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Outbound Lead / Industrial Eng.`
- **`aisle_aligned_pallet_agent_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=05 · Logistics | Store Replenishment`, `service_level_pct=88.4`
- **`aisle_aligned_pallet_agent_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=AISLE_-TEL-101`, `company_id=XYZ-CORP-01`, `category=05 · Distribution & Logistics — Store Replenishment`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_aisle_aligned_pallet_agent_telemetry_feed, query_aisle_aligned_pallet_agent_constraint_matrix, query_aisle_aligned_pallet_agent_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Mathematical Optimization Solver (MILP / CP-SAT) 3D Contoured ULD (LD3/PMC) Weight-Balance Packer + Belly-vs-Charter Allotment MILP + ADS-B Flight Connection Guard**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_aisle_aligned_pallet_agent_plan, action_dispatch_aisle_aligned_pallet_agent_alert` (IATA e-AWB (FWB/FHL) Execution, 3D ULD Build-Up Manifest & Airport Ramp Transfer Dispatch) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Store Replenishment signals for Aisle-Aligned Pallet, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_aisle_aligned_pallet_agent_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py aisle_aligned_pallet_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py aisle_aligned_pallet_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py aisle_aligned_pallet_agent --test-guardrail

# Run unit smoke tests:
pytest agents/aisle_aligned_pallet_agent/tests/test_smoke.py -v
```

---

### 35. Store Capacity Agent (`store_capacity_agent`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **Store Replenishment**
- **Primary Human Persona**: Store Replenishment Lead · **ROI Badge**: `Reduces backroom stock by 25%`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Store Replenishment, Store Replenishment Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Store Capacity Agent intervenes.
2. **What the Agent Does**: Throttles push replenishment based on store backroom limits and live POS velocity.
3. **Expected Outcome**: Reduces backroom stock by 25%. (**Reduces backroom stock by 25%**).

#### 🗄️ Demo Data Details (`agents/store_capacity_agent/fixtures/tables/`)
- **`store_capacity_agent_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=STORE_-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Store Replenishment`
- **`store_capacity_agent_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=STORE_-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Store Replenishment Lead`
- **`store_capacity_agent_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=05 · Logistics | Store Replenishment`, `service_level_pct=88.4`
- **`store_capacity_agent_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=STORE_-TEL-101`, `company_id=XYZ-CORP-01`, `category=05 · Distribution & Logistics — Store Replenishment`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_store_capacity_agent_telemetry_feed, query_store_capacity_agent_constraint_matrix, query_store_capacity_agent_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Low-Latency Transactional State DB Echelon Graph + Coupled Stochastic Guaranteed-Service MEIO + Mathematical Optimization Solver (MILP / CP-SAT) Lateral Flow MILP**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_store_capacity_agent_plan, action_dispatch_store_capacity_agent_alert` (SAP BAPI_MATERIAL_SAVEDATA Safety Stock / ROP Update & STO Lateral Transfer Creation (BAPI_PO_CREATE1)) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Store Replenishment signals for Store Capacity Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_store_capacity_agent_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py store_capacity_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py store_capacity_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py store_capacity_agent --test-guardrail

# Run unit smoke tests:
pytest agents/store_capacity_agent/tests/test_smoke.py -v
```

---

### 36. Curfew Orchestrator (`port_drayage_orchestrator`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **Store Replenishment**
- **Primary Human Persona**: Retail Logistics Dispatcher · **ROI Badge**: `98%+ on-time store window compliance`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Store Replenishment, Retail Logistics Dispatcher teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Curfew Orchestrator intervenes.
2. **What the Agent Does**: Coordinates municipal delivery curfews and store dock shift schedules dynamically.
3. **Expected Outcome**: 98%+ on-time store window compliance. (**98%+ on-time store window compliance**).

#### 🗄️ Demo Data Details (`agents/port_drayage_orchestrator/fixtures/tables/`)
- **`container_discharge_demurrage_ledger.json`** (2 rows) — Columns: `container_id, vessel_imo, size_type, stowage_tier, last_free_day, daily_demurrage_usd` · Sample Record: `container_id=MSKU-904812-0`, `vessel_imo=IMO-9839179`, `size_type=40HC`, `stowage_tier=UPPER_DECK_BAY14`
- **`drayage_chassis_transload_allocations.json`** (1 rows) — Columns: `allocation_id, container_id, drayage_carrier_id, chassis_pool_id, routing_decision, demurrage_avoided_usd` · Sample Record: `allocation_id=DRAY-LAX-881`, `container_id=MSKU-904812-0`, `drayage_carrier_id=PAC-HARBOR-DRAY`, `chassis_pool_id=DCLI-40HC-991`
- **`ocean_vessel_ais_berth_telemetry.json`** (1 rows) — Columns: `vessel_imo, vessel_name, service_loop, port_of_discharge, carrier_published_eta, ai_predicted_berth_eta` · Sample Record: `vessel_imo=IMO-9839179`, `vessel_name=MAERSK MC-KINNEY MOLLER`, `service_loop=TP6_TRANS_PACIFIC`, `port_of_discharge=USLAX_APM_PIER400`
- **`port_terminal_gate_appointments.json`** (1 rows) — Columns: `gate_slot_id, terminal_id, window_utc, transaction_type, turn_time_mins, available_slots` · Sample Record: `gate_slot_id=GATE-LAX-20261028-T1`, `terminal_id=USLAX_APM_PIER400`, `window_utc=2026-10-28T07:00-09:00Z`, `transaction_type=DUAL_EMPTY_RETURN_FULL_PICKUP`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_ocean_vessel_ais_berth_telemetry, query_container_discharge_demurrage_ledger, query_port_terminal_gate_appointments` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Weather & Climate Ensemble Feed Marine ETA Ensemble + Mathematical Optimization Solver (MILP / CP-SAT) Port Free-Time Demurrage Optimizer + Coastal Transload Split MILP**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_book_dual_transaction_drayage_gate, action_divert_container_to_transload_hub` (INTTRA / CargoWise Ocean Booking, Terminal Gate Appointment, Chassis Dispatch & SAP STO Transload Split) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Store Replenishment signals for Curfew Orchestrator, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_book_dual_transaction_drayage_gate immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py port_drayage_orchestrator

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py port_drayage_orchestrator --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py port_drayage_orchestrator --test-guardrail

# Run unit smoke tests:
pytest agents/port_drayage_orchestrator/tests/test_smoke.py -v
```

---

### 37. Geocoding Intelligence (`geocoding_intelligence_agent`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **Last-Mile Delivery**
- **Primary Human Persona**: Last-Mile Operations Lead · **ROI Badge**: `Drops failed deliveries by 30–45%`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Last-Mile Delivery, Last-Mile Operations Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Geocoding Intelligence intervenes.
2. **What the Agent Does**: Interprets gate codes, apartment delivery notes, and aerial imagery to guide drivers.
3. **Expected Outcome**: Drops failed deliveries by 30–45%. (**Drops failed deliveries by 30–45%**).

#### 🗄️ Demo Data Details (`agents/geocoding_intelligence_agent/fixtures/tables/`)
- **`geocoding_intelligence_agent_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=GEOCOD-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Last-Mile Delivery`
- **`geocoding_intelligence_agent_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=GEOCOD-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Last-Mile Operations Lead`
- **`geocoding_intelligence_agent_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=05 · Logistics | Last-Mile Delivery`, `service_level_pct=88.4`
- **`geocoding_intelligence_agent_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=GEOCOD-TEL-101`, `company_id=XYZ-CORP-01`, `category=05 · Distribution & Logistics — Last-Mile Delivery`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_geocoding_intelligence_agent_telemetry_feed, query_geocoding_intelligence_agent_constraint_matrix, query_geocoding_intelligence_agent_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Google Maps Distance Matrix + Angular Sector Corridor Clustering + Mathematical Optimization Solver (MILP / CP-SAT) Heterogeneous CVRPTW**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_geocoding_intelligence_agent_plan, action_dispatch_geocoding_intelligence_agent_alert` (Transportation Management System (TMS / MCP) / Transportation Management System (TMS / API) Load Tender (EDI 204), Google Maps Driver Route Manifest & Live ETA Broadcast) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Last-Mile Delivery signals for Geocoding Intelligence, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_geocoding_intelligence_agent_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py geocoding_intelligence_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py geocoding_intelligence_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py geocoding_intelligence_agent --test-guardrail

# Run unit smoke tests:
pytest agents/geocoding_intelligence_agent/tests/test_smoke.py -v
```

---

### 38. Courier Allocation (`multimodal_mode_shift_agent`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **Last-Mile Delivery**
- **Primary Human Persona**: E-Commerce Logistics Dir. · **ROI Badge**: `Lowers last-mile cost by 8–14%`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Last-Mile Delivery, E-Commerce Logistics Dir. teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Courier Allocation intervenes.
2. **What the Agent Does**: Routes parcels dynamically across internal fleet, 3PL, and gig couriers by rate card.
3. **Expected Outcome**: Lowers last-mile cost by 8–14%. (**Lowers last-mile cost by 8–14%**).

#### 🗄️ Demo Data Details (`agents/multimodal_mode_shift_agent/fixtures/tables/`)
- **`dynamic_mode_split_recommendations.json`** (1 rows) — Columns: `split_plan_id, po_id, base_ocean_units, expedite_sea_air_units, panic_full_air_cost_usd, optimal_split_cost_usd` · Sample Record: `split_plan_id=SPLIT-VN-RTM-01`, `po_id=PO-FAC-VN-88210`, `base_ocean_units=17000`, `expedite_sea_air_units=3000`
- **`factory_gate_outbound_pos.json`** (1 rows) — Columns: `po_id, origin_factory, dest_dc, total_units, weight_kg, dest_days_of_supply` · Sample Record: `po_id=PO-FAC-VN-88210`, `origin_factory=Hai Phong Plant (Vietnam)`, `dest_dc=Rotterdam Euro Hub`, `total_units=20000`
- **`in_transit_mode_diversion_triggers.json`** (1 rows) — Columns: `diversion_id, po_id, transship_hub, units_upgraded_to_air, days_recovered, stockout_penalty_avoided_usd` · Sample Record: `diversion_id=DIV-SEA-AIR-09`, `po_id=PO-FAC-VN-88210`, `transship_hub=DXB_JEBEL_ALI_DWC`, `units_upgraded_to_air=3000`
- **`multimodal_corridor_rate_tariff_matrix.json`** (3 rows) — Columns: `mode_code, transit_days, cost_per_kg_usd, co2e_g_per_tkm` · Sample Record: `mode_code=OCEAN_FCL_SUEZ`, `transit_days=34`, `cost_per_kg_usd=0.42`, `co2e_g_per_tkm=11.2`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_factory_gate_outbound_pos, query_multimodal_corridor_rate_tariff_matrix, query_dynamic_mode_split_recommendations` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Low-Latency Transactional State DB Multi-Modal Network Graph + Mathematical Optimization Solver (MILP / CP-SAT) Pareto Cost / Carbon / SLA Mode-Switch MILP**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_execute_dynamic_mode_split_booking, action_trigger_mid_route_sea_air_upgrade` (Transportation Management System (TMS / MCP) / Supply Chain Execution Platform (MCP / API) Multi-Leg Booking Split (Ocean / Sea-Air / Rail / Road) & OMS Promise Update) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Last-Mile Delivery signals for Courier Allocation, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_execute_dynamic_mode_split_booking immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py multimodal_mode_shift_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py multimodal_mode_shift_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py multimodal_mode_shift_agent --test-guardrail

# Run unit smoke tests:
pytest agents/multimodal_mode_shift_agent/tests/test_smoke.py -v
```

---

### 39. Delivery Exception Copilot (`otif_penalty_shield`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **Last-Mile Delivery**
- **Primary Human Persona**: Customer Support Ops Lead · **ROI Badge**: `Decreases WISMO calls by up to 60%`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Last-Mile Delivery, Customer Support Ops Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Delivery Exception Copilot intervenes.
2. **What the Agent Does**: Detects en-route exceptions and updates customers proactively with reschedule links.
3. **Expected Outcome**: Decreases WISMO calls by up to 60%. (**Decreases WISMO calls by up to 60%**).

#### 🗄️ Demo Data Details (`agents/otif_penalty_shield/fixtures/tables/`)
- **`geofence_edi856_dispute_dossiers.json`** (1 rows) — Columns: `dossier_id, deduction_id, mabd_cutoff_utc, google_maps_geofence_entry_utc, edi856_asn_timestamp, epod_signature_verified` · Sample Record: `dossier_id=DOS-OTIF-44910`, `deduction_id=DED-RET01-44910`, `mabd_cutoff_utc=2026-10-18T16:00:00Z`, `google_maps_geofence_entry_utc=2026-10-18T14:12:00Z`
- **`open_retail_customer_orders_sla.json`** (1 rows) — Columns: `order_id, customer_id, order_value_usd, mabd_window_utc, otif_penalty_pct, potential_fine_usd` · Sample Record: `order_id=SO-WMT-20261022-881`, `customer_id=BIGBOX-RETAIL-01`, `order_value_usd=420000.0`, `mabd_window_utc=2026-10-25T14:00:00Z`
- **`predicted_otif_breach_alerts.json`** (1 rows) — Columns: `alert_id, order_id, breach_probability, root_cause, rescue_option, rescue_cost_usd` · Sample Record: `alert_id=OTIF-ALT-881`, `order_id=SO-WMT-20261022-881`, `breach_probability=0.78`, `root_cause=PRIMARY_DC_WAVE_BACKLOG_6HRS`
- **`retailer_otif_chargeback_deductions.json`** (1 rows) — Columns: `deduction_id, customer_id, shipment_id, claimed_reason, deducted_amount_usd` · Sample Record: `deduction_id=DED-RET01-44910`, `customer_id=BIGBOX-RETAIL-01`, `shipment_id=SHP-WMT-4012`, `claimed_reason=LATE_ARRIVAL_PAST_MABD`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_open_retail_customer_orders_sla, query_predicted_otif_breach_alerts, query_retailer_otif_chargeback_deductions` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **BigQuery ML 72-Hr MABD Breach Predictor + Mathematical Optimization Solver (MILP / CP-SAT) Penalty-vs-Expedite NPV Solver + Document AI Dispute Assembler**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_execute_otif_sla_rescue_intervention, action_submit_chargeback_dispute_dossier` (ERP Order Management (SD / MCP) Alternate-DC Order Re-Allocation & Automated Retailer Portal Dispute Submission via MCP / REST / On-Prem Gateway) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Last-Mile Delivery signals for Delivery Exception Copilot, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_execute_otif_sla_rescue_intervention immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py otif_penalty_shield

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py otif_penalty_shield --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py otif_penalty_shield --test-guardrail

# Run unit smoke tests:
pytest agents/otif_penalty_shield/tests/test_smoke.py -v
```

---

### 40. Dynamic Rerouter (`fleetflow_dispatch`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **Route & Carrier**
- **Primary Human Persona**: Fleet Dispatcher / Central Ops · **ROI Badge**: `Cuts fleet fuel usage by 6–10%` · 🟢 **Live Vertex AI RE**: `1064147210658119680`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Route & Carrier, Fleet Dispatcher / Central Ops teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Dynamic Rerouter intervenes.
2. **What the Agent Does**: Recalculates multi-stop routes using live Google Maps traffic, radar, and bridge limits.
3. **Expected Outcome**: Cuts fleet fuel usage by 6–10%. (**Cuts fleet fuel usage by 6–10%**).

#### 🗄️ Demo Data Details (`agents/fleetflow_dispatch/fixtures/tables/`)
- **`backhaul_consolidation_opportunities.json`** (1 rows) — Columns: `backhaul_id, origin_hub, destination_dc, weight_kg, pallets, deadhead_miles_eliminated` · Sample Record: `backhaul_id=BKH-SAT-DAL-44`, `origin_hub=San Antonio Vendor Park`, `destination_dc=Dallas Central RDC`, `weight_kg=14200`
- **`corridor_delivery_orders.json`** (3 rows) — Columns: `order_id, corridor_id, customer_hub, stop_sequence, weight_kg, cube_m3` · Sample Record: `order_id=ORD-FF-901`, `corridor_id=CORR-I35-TEX`, `customer_hub=Austin Supercenter #14`, `stop_sequence=1`
- **`fleet_vehicle_telematics_hos.json`** (2 rows) — Columns: `vehicle_id, vehicle_class, max_payload_kg, max_cube_m3, driver_hos_remaining_hrs, fuel_type` · Sample Record: `vehicle_id=TRK-24T-TX08`, `vehicle_class=24t_Class8_Heavy_Tractor`, `max_payload_kg=21500`, `max_cube_m3=82.0`
- **`google_maps_corridor_routes.json`** (2 rows) — Columns: `route_id, corridor_id, assigned_vehicle_id, total_distance_km, baseline_distance_km, distance_saved_pct` · Sample Record: `route_id=RTE-I35-20261022-01`, `corridor_id=CORR-I35-TEX`, `assigned_vehicle_id=TRK-24T-TX08`, `total_distance_km=462.5`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_corridor_delivery_orders, query_fleet_vehicle_telematics_hos, query_google_maps_corridor_routes` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Google Maps Distance Matrix + Angular Sector Corridor Clustering + Mathematical Optimization Solver (MILP / CP-SAT) Heterogeneous CVRPTW**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_dispatch_corridor_route_manifest, action_assign_backhaul_return_load` (Transportation Management System (TMS / MCP) / Transportation Management System (TMS / API) Load Tender (EDI 204), Google Maps Driver Route Manifest & Live ETA Broadcast) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Route & Carrier signals for Dynamic Rerouter, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_dispatch_corridor_route_manifest immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py fleetflow_dispatch

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py fleetflow_dispatch --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py fleetflow_dispatch --test-guardrail

# Run unit smoke tests:
pytest agents/fleetflow_dispatch/tests/test_smoke.py -v
```

---

### 41. Routing Guide Compliance (`freight_control_tower`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **Route & Carrier**
- **Primary Human Persona**: Transport Procurement Lead · **ROI Badge**: `Reduces spot freight by 15–20%`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Route & Carrier, Transport Procurement Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Routing Guide Compliance intervenes.
2. **What the Agent Does**: Tracks carrier tender acceptance & OTIF to reprioritize waterfall routing guides.
3. **Expected Outcome**: Reduces spot freight by 15–20%. (**Reduces spot freight by 15–20%**).

#### 🗄️ Demo Data Details (`agents/freight_control_tower/fixtures/tables/`)
- **`carrier_edi210_freight_invoices.json`** (1 rows) — Columns: `invoice_id, carrier_id, shipment_id, billed_amount_usd, billed_detention_hrs, billed_detention_fee_usd` · Sample Record: `invoice_id=INV-EDI210-77410`, `carrier_id=KNIGHT-SWIFT-TL`, `shipment_id=SHP-DRY-5519`, `billed_amount_usd=3490.0`
- **`cold_chain_thermal_excursion_alerts.json`** (1 rows) — Columns: `alert_id, shipment_id, cargo_value_at_risk_usd, nearest_cold_crossdock, distance_to_hub_km, recommended_action` · Sample Record: `alert_id=THRM-ALT-8841`, `shipment_id=SHP-REEF-8841`, `cargo_value_at_risk_usd=148000.0`, `nearest_cold_crossdock=DES_MOINES_COLD_HUB_04`
- **`freight_audit_discrepancy_ledger.json`** (1 rows) — Columns: `audit_id, invoice_id, geofence_verified_dwell_hrs, contract_free_time_hrs, contract_fsc_pct, overcharge_detected_usd` · Sample Record: `audit_id=FAUD-77410`, `invoice_id=INV-EDI210-77410`, `geofence_verified_dwell_hrs=1.2`, `contract_free_time_hrs=2.0`
- **`in_transit_multimodal_telemetry.json`** (1 rows) — Columns: `shipment_id, carrier_id, corridor, cargo_type, setpoint_c, current_temp_c` · Sample Record: `shipment_id=SHP-REEF-8841`, `carrier_id=PRIME-REEFER-INC`, `corridor=I-80 Omaha➔Chicago`, `cargo_type=CHILLED_PROTEIN_2C`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_in_transit_multimodal_telemetry, query_cold_chain_thermal_excursion_alerts, query_carrier_edi210_freight_invoices` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Pub/Sub + Dataflow Spatiotemporal ETA/Thermal Drift Predictor + Google Maps Geofence & Document AI Rate-Card Audit Engine**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_reroute_in_transit_reefer_shipment, action_issue_freight_audit_debit_adjustment` (Automated Carrier Claim Dispute Packet & Approved Enterprise ERP (MCP / On-Prem DB) AP Freight Voucher (BAPI_INCOMINGINVOICE_CREATE)) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Route & Carrier signals for Routing Guide Compliance, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_reroute_in_transit_reefer_shipment immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py freight_control_tower

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py freight_control_tower --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py freight_control_tower --test-guardrail

# Run unit smoke tests:
pytest agents/freight_control_tower/tests/test_smoke.py -v
```

---

### 42. Freight Bill Audit Agent (`freight_bill_audit_agent`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **Route & Carrier**
- **Primary Human Persona**: Freight Controller / Claims · **ROI Badge**: `Captures 3–7% in overbilled fees`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Route & Carrier, Freight Controller / Claims teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Freight Bill Audit Agent intervenes.
2. **What the Agent Does**: Extracts signed PODs and rate contracts via OCR to audit accessorial surcharges.
3. **Expected Outcome**: Captures 3–7% in overbilled fees. (**Captures 3–7% in overbilled fees**).

#### 🗄️ Demo Data Details (`agents/freight_bill_audit_agent/fixtures/tables/`)
- **`freight_bill_audit_agent_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=FREIGH-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Route & Carrier`
- **`freight_bill_audit_agent_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=FREIGH-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Freight Controller / Claims`
- **`freight_bill_audit_agent_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=05 · Logistics | Route & Carrier`, `service_level_pct=88.4`
- **`freight_bill_audit_agent_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=FREIGH-TEL-101`, `company_id=XYZ-CORP-01`, `category=05 · Distribution & Logistics — Route & Carrier`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_freight_bill_audit_agent_telemetry_feed, query_freight_bill_audit_agent_constraint_matrix, query_freight_bill_audit_agent_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Pub/Sub + Dataflow Spatiotemporal ETA/Thermal Drift Predictor + Google Maps Geofence & Document AI Rate-Card Audit Engine**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_freight_bill_audit_agent_plan, action_dispatch_freight_bill_audit_agent_alert` (Automated Carrier Claim Dispute Packet & Approved Enterprise ERP (MCP / On-Prem DB) AP Freight Voucher (BAPI_INCOMINGINVOICE_CREATE)) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Route & Carrier signals for Freight Bill Audit Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_freight_bill_audit_agent_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py freight_bill_audit_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py freight_bill_audit_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py freight_bill_audit_agent --test-guardrail

# Run unit smoke tests:
pytest agents/freight_bill_audit_agent/tests/test_smoke.py -v
```

---

## 05 · Inventory & Warehousing (9 Agents)

### 43. Safety Stock Agent (`meio_safety_stock_agent`)
- **Pillar / Sub-Pillar**: 05 · Inventory & Warehousing — **Positioning & Optimization**
- **Primary Human Persona**: Inventory Optimization Lead · **ROI Badge**: `Cuts working capital by 10–18%` · 🟢 **Live Vertex AI RE**: `9178085626807844864`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Positioning & Optimization, Inventory Optimization Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Safety Stock Agent intervenes.
2. **What the Agent Does**: Recalibrates multi-echelon buffers using live lead-time and demand variance.
3. **Expected Outcome**: Cuts working capital by 10–18%. (**Cuts working capital by 10–18%**).

#### 🗄️ Demo Data Details (`agents/meio_safety_stock_agent/fixtures/tables/`)
- **`dc_inventory_echelon_balances.json`** (3 rows) — Columns: `dc_id, dc_name, echelon_tier, sku_id, on_hand_inventory_units, allocated_inventory_units` · Sample Record: `dc_id=CDC-CHICAGO-01`, `dc_name=Midwest Central Distribution Center`, `echelon_tier=TIER_1_CENTRAL_DC`, `sku_id=SKU-BEV-OATMILK-ORIGINAL-1L`
- **`echelon_service_level_projections.json`** (1 rows) — Columns: `projection_id, sku_id, network_node_id, days_of_supply_baseline, stockout_probability_without_rebalance_pct, stockout_probability_with_rebalance_pct` · Sample Record: `projection_id=SL-PROJ-202610-001`, `sku_id=SKU-BEV-OATMILK-ORIGINAL-1L`, `network_node_id=RDC-DALLAS-02`, `days_of_supply_baseline=3.8`
- **`lateral_dc_rebalance_transfers.json`** (1 rows) — Columns: `transfer_id, sku_id, source_dc_id, destination_dc_id, quantity_transferred_units, transport_mode` · Sample Record: `transfer_id=REBAL-TRANSFER-202610-001`, `sku_id=SKU-BEV-OATMILK-ORIGINAL-1L`, `source_dc_id=CDC-CHICAGO-01`, `destination_dc_id=RDC-DALLAS-02`
- **`multi_echelon_safety_stock_recommendations.json`** (2 rows) — Columns: `recommendation_id, sku_id, sku_description, echelon_tier, network_node_id, current_safety_stock_units` · Sample Record: `recommendation_id=MEIO-REC-202610-001`, `sku_id=SKU-BEV-OATMILK-ORIGINAL-1L`, `sku_description=Barista Organic Oat Milk 1L Tetra`, `echelon_tier=TIER_1_CENTRAL_DC`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_multi_echelon_safety_stock_recommendations, query_dc_inventory_echelon_balances, query_lateral_dc_rebalance_transfers` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Low-Latency Transactional State DB Echelon Graph + Coupled Stochastic Guaranteed-Service MEIO + Mathematical Optimization Solver (MILP / CP-SAT) Lateral Flow MILP**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_execute_lateral_dc_rebalance, action_update_echelon_safety_stock_policy` (SAP BAPI_MATERIAL_SAVEDATA Safety Stock / ROP Update & STO Lateral Transfer Creation (BAPI_PO_CREATE1)) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Positioning & Optimization signals for Safety Stock Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_execute_lateral_dc_rebalance immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py meio_safety_stock_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py meio_safety_stock_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py meio_safety_stock_agent --test-guardrail

# Run unit smoke tests:
pytest agents/meio_safety_stock_agent/tests/test_smoke.py -v
```

---

### 44. SLOB Disposition Agent (`slob_disposition_agent`)
- **Pillar / Sub-Pillar**: 05 · Inventory & Warehousing — **Positioning & Optimization**
- **Primary Human Persona**: Inventory Controller / Buyer · **ROI Badge**: `Prevents expired stock write-offs`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Positioning & Optimization, Inventory Controller / Buyer teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before SLOB Disposition Agent intervenes.
2. **What the Agent Does**: Analyzes shelf-life risk and triggers promotional bundles or liquidations.
3. **Expected Outcome**: Prevents expired stock write-offs. (**Prevents expired stock write-offs**).

#### 🗄️ Demo Data Details (`agents/slob_disposition_agent/fixtures/tables/`)
- **`slob_disposition_agent_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=SLOB_D-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Positioning & Optimization`
- **`slob_disposition_agent_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=SLOB_D-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Inventory Controller / Buyer`
- **`slob_disposition_agent_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=04 · Inventory & DC | Positioning & Optimization`, `service_level_pct=88.4`
- **`slob_disposition_agent_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=SLOB_D-TEL-101`, `company_id=XYZ-CORP-01`, `category=04 · Inventory & Warehousing — Positioning & Optimization`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_slob_disposition_agent_telemetry_feed, query_slob_disposition_agent_constraint_matrix, query_slob_disposition_agent_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Low-Latency Transactional State DB Echelon Graph + Coupled Stochastic Guaranteed-Service MEIO + Mathematical Optimization Solver (MILP / CP-SAT) Lateral Flow MILP**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_slob_disposition_agent_plan, action_dispatch_slob_disposition_agent_alert` (SAP BAPI_MATERIAL_SAVEDATA Safety Stock / ROP Update & STO Lateral Transfer Creation (BAPI_PO_CREATE1)) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Positioning & Optimization signals for SLOB Disposition Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_slob_disposition_agent_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py slob_disposition_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py slob_disposition_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py slob_disposition_agent --test-guardrail

# Run unit smoke tests:
pytest agents/slob_disposition_agent/tests/test_smoke.py -v
```

---

### 45. Inter-Facility Rebalancer (`crossdock_transfer_orchestrator`)
- **Pillar / Sub-Pillar**: 05 · Inventory & Warehousing — **Positioning & Optimization**
- **Primary Human Persona**: Replenishment Planner · **ROI Badge**: `Eliminates regional out-of-stocks`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Positioning & Optimization, Replenishment Planner teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Inter-Facility Rebalancer intervenes.
2. **What the Agent Does**: Generates automated inter-DC and store transfers to balance localized gluts.
3. **Expected Outcome**: Eliminates regional out-of-stocks. (**Eliminates regional out-of-stocks**).

#### 🗄️ Demo Data Details (`agents/crossdock_transfer_orchestrator/fixtures/tables/`)
- **`crossdock_dwell_time_records.json`** (2 rows) — Columns: `record_id, pallet_id, inbound_door_id, outbound_bay_id, dwell_time_minutes, forklift_transfer_distance_m` · Sample Record: `record_id=XDOCK-DWELL-20261022-01`, `pallet_id=PLT-OAT-9921-01`, `inbound_door_id=DOOR-INBOUND-04`, `outbound_bay_id=BAY-OUTBOUND-12`
- **`inbound_carrier_eta_milestones.json`** (1 rows) — Columns: `shipment_id, carrier_id, trailer_id, geofence_arrival_timestamp, dock_checkin_timestamp, unloading_start_timestamp` · Sample Record: `shipment_id=SHP-SWIFT-20261022-9921`, `carrier_id=CARRIER-SWIFT-TRANS`, `trailer_id=TRL-INB-SWIFT-9921`, `geofence_arrival_timestamp=2026-10-22T05:15:00Z`
- **`inbound_outbound_crossdock_manifests.json`** (1 rows) — Columns: `manifest_id, inbound_trailer_id, supplier_id, carrier_name, inbound_door_id, total_pallets_count` · Sample Record: `manifest_id=XDOCK-MNF-20261022-041`, `inbound_trailer_id=TRL-INB-SWIFT-9921`, `supplier_id=SUP-OATLY-PLANT-01`, `carrier_name=Swift Transportation`
- **`outbound_trailer_bay_assignments.json`** (2 rows) — Columns: `bay_id, outbound_trailer_id, carrier_name, destination_dc, route_code, current_pallet_load_count` · Sample Record: `bay_id=BAY-OUTBOUND-12`, `outbound_trailer_id=TRL-OUT-JB-HUNT-4481`, `carrier_name=J.B. Hunt Transport`, `destination_dc=RDC-HOUSTON-05`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_inbound_outbound_crossdock_manifests, query_inbound_carrier_eta_milestones, query_outbound_trailer_bay_assignments` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Mathematical Optimization Solver (MILP / CP-SAT) CP-SAT Inbound-to-Outbound Door Coupling + Flow-Through Pallet De-Consolidation MILP**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_dispatch_direct_crossdock_transfer, action_hold_pallet_for_staging_buffer` (Warehouse Management System (WMS / MCP) / Manhattan Cross-Dock Flow-Through Directive, Conveyor Sortation Route & Outbound Staging Lock) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Positioning & Optimization signals for Inter-Facility Rebalancer, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_dispatch_direct_crossdock_transfer immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py crossdock_transfer_orchestrator

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py crossdock_transfer_orchestrator --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py crossdock_transfer_orchestrator --test-guardrail

# Run unit smoke tests:
pytest agents/crossdock_transfer_orchestrator/tests/test_smoke.py -v
```

---

### 46. Dynamic Slotting Agent (`warehouse_slotting_agent`)
- **Pillar / Sub-Pillar**: 05 · Inventory & Warehousing — **Warehouse Operations**
- **Primary Human Persona**: DC Operations Mgr / IE Lead · **ROI Badge**: `Reduces picker transit time by 15–30%`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Warehouse Operations, DC Operations Mgr / IE Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Dynamic Slotting Agent intervenes.
2. **What the Agent Does**: Evaluates co-pick affinity matrices to recommend fast-pick zone re-slotting.
3. **Expected Outcome**: Reduces picker transit time by 15–30%. (**Reduces picker transit time by 15–30%**).

#### 🗄️ Demo Data Details (`agents/warehouse_slotting_agent/fixtures/tables/`)
- **`amr_picker_travel_telemetry.json`** (2 rows) — Columns: `telemetry_id, dc_id, amr_id, wave_id, average_picker_speed_m_s, total_travel_distance_km` · Sample Record: `telemetry_id=AMR-TEL-20261022-001`, `dc_id=RDC-DALLAS-02`, `amr_id=AMR-KION-BOT-07`, `wave_id=WAVE-20261022-AM-01`
- **`slot_reassignment_recommendations.json`** (1 rows) — Columns: `recommendation_id, sku_id, current_bin_id, recommended_bin_id, priority, estimated_picker_travel_reduction_pct` · Sample Record: `recommendation_id=SLOT-REC-202610-001`, `sku_id=SKU-BEV-OATMILK-ORIGINAL-1L`, `current_bin_id=BIN-AISLE-14-SHELF-04-HIGH`, `recommended_bin_id=BIN-AISLE-02-SHELF-02-GOLDEN`
- **`warehouse_slotting_velocity_tiers.json`** (2 rows) — Columns: `sku_id, sku_name, velocity_tier, pick_frequency_lines_per_day, current_bin_id, recommended_bin_id` · Sample Record: `sku_id=SKU-BEV-OATMILK-ORIGINAL-1L`, `sku_name=Barista Organic Oat Milk 1L Tetra`, `velocity_tier=FAST_MOVER_TIER_A`, `pick_frequency_lines_per_day=840`
- **`wave_release_order_allocations.json`** (2 rows) — Columns: `wave_id, dc_id, zone_id, allocated_orders_count, total_pick_lines, active_pickers_count` · Sample Record: `wave_id=WAVE-20261022-AM-01`, `dc_id=RDC-DALLAS-02`, `zone_id=ZONE-BULK-MEZZANINE`, `allocated_orders_count=450`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_warehouse_slotting_velocity_tiers, query_amr_picker_travel_telemetry, query_wave_release_order_allocations` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **3D Spatial Digital Twin + BigQuery FP-Growth Order Affinity + Mathematical Optimization Solver (MILP / CP-SAT) CP-SAT Congestion Wave Solver**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_execute_slot_reassignment, action_balance_wave_release_profile` (Manhattan / Warehouse Management System (WMS / MCP) Directed Putaway, Re-Slot Tasks & Dynamic Wave Release via MCP / REST / On-Prem Gateway) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Warehouse Operations signals for Dynamic Slotting Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_execute_slot_reassignment immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py warehouse_slotting_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py warehouse_slotting_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py warehouse_slotting_agent --test-guardrail

# Run unit smoke tests:
pytest agents/warehouse_slotting_agent/tests/test_smoke.py -v
```

---

### 47. Dock-to-Stock Agent (`dock_to_stock_agent`)
- **Pillar / Sub-Pillar**: 05 · Inventory & Warehousing — **Warehouse Operations**
- **Primary Human Persona**: Inbound Receiving Supervisor · **ROI Badge**: `Dock turnaround in minutes vs. hours`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Warehouse Operations, Inbound Receiving Supervisor teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Dock-to-Stock Agent intervenes.
2. **What the Agent Does**: Parses scanned BOLs and pallet photos to reconcile open ASN variances.
3. **Expected Outcome**: Dock turnaround in minutes vs. hours. (**Dock turnaround in minutes vs. hours**).

#### 🗄️ Demo Data Details (`agents/dock_to_stock_agent/fixtures/tables/`)
- **`dock_to_stock_agent_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=DOCK_T-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Warehouse Operations`
- **`dock_to_stock_agent_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=DOCK_T-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Inbound Receiving Supervisor`
- **`dock_to_stock_agent_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=04 · Inventory & DC | Warehouse Operations`, `service_level_pct=88.4`
- **`dock_to_stock_agent_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=DOCK_T-TEL-101`, `company_id=XYZ-CORP-01`, `category=04 · Inventory & Warehousing — Warehouse Operations`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_dock_to_stock_agent_telemetry_feed, query_dock_to_stock_agent_constraint_matrix, query_dock_to_stock_agent_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Google Maps Live ETA + Mathematical Optimization Solver (MILP / CP-SAT) Bipartite Dock-Door Matching + Shortest-Path Hostler Task Interleaving**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_dock_to_stock_agent_plan, action_dispatch_dock_to_stock_agent_alert` (YMS / Warehouse Management System (WMS / MCP) Dock Door Assignment, Driver SMS Gate Pass & Hostler Tablet Dispatch) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Warehouse Operations signals for Dock-to-Stock Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_dock_to_stock_agent_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py dock_to_stock_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py dock_to_stock_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py dock_to_stock_agent --test-guardrail

# Run unit smoke tests:
pytest agents/dock_to_stock_agent/tests/test_smoke.py -v
```

---

### 48. Wave Fulfillment Copilot (`wave_fulfillment_copilot`)
- **Pillar / Sub-Pillar**: 05 · Inventory & Warehousing — **Warehouse Operations**
- **Primary Human Persona**: DC Shift Floor Lead · **ROI Badge**: `Prevents missed dispatch windows (OTIF)`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Warehouse Operations, DC Shift Floor Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Wave Fulfillment Copilot intervenes.
2. **What the Agent Does**: Balances picker lines dynamically to protect carrier pickup cutoff times.
3. **Expected Outcome**: Prevents missed dispatch windows (OTIF). (**Prevents missed dispatch windows (OTIF)**).

#### 🗄️ Demo Data Details (`agents/wave_fulfillment_copilot/fixtures/tables/`)
- **`wave_fulfillment_copilot_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=WAVE_F-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Warehouse Operations`
- **`wave_fulfillment_copilot_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=WAVE_F-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=DC Shift Floor Lead`
- **`wave_fulfillment_copilot_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=04 · Inventory & DC | Warehouse Operations`, `service_level_pct=88.4`
- **`wave_fulfillment_copilot_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=WAVE_F-TEL-101`, `company_id=XYZ-CORP-01`, `category=04 · Inventory & Warehousing — Warehouse Operations`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_wave_fulfillment_copilot_telemetry_feed, query_wave_fulfillment_copilot_constraint_matrix, query_wave_fulfillment_copilot_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **3D Spatial Digital Twin + BigQuery FP-Growth Order Affinity + Mathematical Optimization Solver (MILP / CP-SAT) CP-SAT Congestion Wave Solver**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_wave_fulfillment_copilot_plan, action_dispatch_wave_fulfillment_copilot_alert` (Manhattan / Warehouse Management System (WMS / MCP) Directed Putaway, Re-Slot Tasks & Dynamic Wave Release via MCP / REST / On-Prem Gateway) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Warehouse Operations signals for Wave Fulfillment Copilot, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_wave_fulfillment_copilot_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py wave_fulfillment_copilot

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py wave_fulfillment_copilot --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py wave_fulfillment_copilot --test-guardrail

# Run unit smoke tests:
pytest agents/wave_fulfillment_copilot/tests/test_smoke.py -v
```

---

### 49. Phantom Inventory Sensor (`planogram_merchandising_vision_auditor`)
- **Pillar / Sub-Pillar**: 05 · Inventory & Warehousing — **Omnichannel Visibility**
- **Primary Human Persona**: Store Operations / Omni Lead · **ROI Badge**: `Triggers targeted floor cycle counts`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Omnichannel Visibility, Store Operations / Omni Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Phantom Inventory Sensor intervenes.
2. **What the Agent Does**: Identifies shrinkage anomalies when on-hand stock stops scanning at POS.
3. **Expected Outcome**: Triggers targeted floor cycle counts. (**Triggers targeted floor cycle counts**).

#### 🗄️ Demo Data Details (`agents/planogram_merchandising_vision_auditor/fixtures/tables/`)
- **`contracted_planogram_templates.json`** (1 rows) — Columns: `template_id, channel_tier, required_sos_pct, required_eye_level_facings, monthly_visibility_payout_usd` · Sample Record: `template_id=PLG-BEV-GONDOLA-Q4`, `channel_tier=MODERN_TRADE_HYPER`, `required_sos_pct=45.0`, `required_eye_level_facings=14`
- **`merchandising_corrective_tasks.json`** (1 rows) — Columns: `task_id, outlet_id, fso_id, directive` · Sample Record: `task_id=MRCH-TSK-409`, `outlet_id=OUTLET-HYPER-882`, `fso_id=FSO-WEST-112`, `directive=Restock 2 empty gaps of SKU-BEV-500ML from backroom and remove 3 competitor facings from Eye-Level Tier 2`
- **`shelf_compliance_scoring_ledger.json`** (1 rows) — Columns: `audit_id, outlet_id, measured_sos_pct, post_correction_sos_pct, compliance_status, osa_lift_pct` · Sample Record: `audit_id=SHLF-AUD-409`, `outlet_id=OUTLET-HYPER-882`, `measured_sos_pct=32.1`, `post_correction_sos_pct=46.8`
- **`store_shelf_vision_audit_captures.json`** (1 rows) — Columns: `capture_id, outlet_id, shelf_zone, detected_brand_facings, contracted_brand_facings, competitor_intrusion_facings` · Sample Record: `capture_id=IMG-SHLF-20261022-409`, `outlet_id=OUTLET-HYPER-882`, `shelf_zone=EYE_LEVEL_TIER_2`, `detected_brand_facings=9`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_store_shelf_vision_audit_captures, query_contracted_planogram_templates, query_shelf_compliance_scoring_ledger` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Vertex AI Multimodal Vision Object & Facing Detection + Share-of-Shelf Planogram Compliance Classifier**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_dispatch_instore_restock_directive, action_certify_store_planogram_audit` (Store Planogram Audit Scorecard, Retailer Visibility Incentive Approval & Penalty Dispute Memo) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Omnichannel Visibility signals for Phantom Inventory Sensor, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_dispatch_instore_restock_directive immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py planogram_merchandising_vision_auditor

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py planogram_merchandising_vision_auditor --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py planogram_merchandising_vision_auditor --test-guardrail

# Run unit smoke tests:
pytest agents/planogram_merchandising_vision_auditor/tests/test_smoke.py -v
```

---

### 50. SFS / BOPIS Sourcing (`atp_order_promising_agent`)
- **Pillar / Sub-Pillar**: 05 · Inventory & Warehousing — **Omnichannel Visibility**
- **Primary Human Persona**: Omnichannel Fulfillment Dir. · **ROI Badge**: `Lowers parcel costs & split rates` · 🟢 **Live Vertex AI RE**: `8558136990602625024`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Omnichannel Visibility, Omnichannel Fulfillment Dir. teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before SFS / BOPIS Sourcing intervenes.
2. **What the Agent Does**: Selects lowest-cost fulfillment nodes based on store labor and parcel zones.
3. **Expected Outcome**: Lowers parcel costs & split rates. (**Lowers parcel costs & split rates**).

#### 🗄️ Demo Data Details (`agents/atp_order_promising_agent/fixtures/tables/`)
- **`customer_tier_sla_commitments.json`** (2 rows) — Columns: `customer_id, customer_name, contract_tier, minimum_fill_rate_sla_pct, on_time_in_full_otif_sla_pct, otif_penalty_fee_per_late_day_usd` · Sample Record: `customer_id=CUST-KROGER-CORP`, `customer_name=Kroger National Distribution`, `contract_tier=TIER_1_STRATEGIC`, `minimum_fill_rate_sla_pct=98.5`
- **`inbound_customer_order_requests.json`** (2 rows) — Columns: `order_id, customer_id, sku_id, requested_units, requested_delivery_date, destination_zip` · Sample Record: `order_id=ORD-20261022-8841`, `customer_id=CUST-KROGER-CORP`, `sku_id=SKU-BEV-OATMILK-ORIGINAL-1L`, `requested_units=8000`
- **`order_promising_routing_decisions.json`** (1 rows) — Columns: `decision_id, order_id, customer_id, sku_id, promised_units, promised_fulfillment_node` · Sample Record: `decision_id=OP-DEC-20261022-001`, `order_id=ORD-20261022-8841`, `customer_id=CUST-KROGER-CORP`, `sku_id=SKU-BEV-OATMILK-ORIGINAL-1L`
- **`realtime_sku_atp_allocations.json`** (2 rows) — Columns: `sku_id, network_node_id, node_type, total_physical_on_hand_units, allocated_committed_units, tier1_contract_reserved_units` · Sample Record: `sku_id=SKU-BEV-OATMILK-ORIGINAL-1L`, `network_node_id=CDC-CHICAGO-01`, `node_type=CENTRAL_DC`, `total_physical_on_hand_units=68400`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_realtime_sku_atp_allocations, query_customer_tier_sla_commitments, query_inbound_customer_order_requests` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Low-Latency Transactional State DB Global Inventory Ledger + Mathematical Optimization Solver (MILP / CP-SAT) Sub-50ms Margin-Aware Multi-Node Sourcing MILP**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_dynamic_order_promise, action_protect_tier1_allocation_reserve` (OMS Order Node Allocation & Enterprise ERP (MCP / On-Prem DB) Sales Order Schedule Line Lock (BAPI_SALESORDER_CHANGE)) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Omnichannel Visibility signals for SFS / BOPIS Sourcing, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_dynamic_order_promise immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py atp_order_promising_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py atp_order_promising_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py atp_order_promising_agent --test-guardrail

# Run unit smoke tests:
pytest agents/atp_order_promising_agent/tests/test_smoke.py -v
```

---

### 51. Returns Triage Agent (`returns_triage_agent`)
- **Pillar / Sub-Pillar**: 05 · Inventory & Warehousing — **Omnichannel Visibility**
- **Primary Human Persona**: Reverse Logistics Lead · **ROI Badge**: `Restocks sellable returns within 24h`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Omnichannel Visibility, Reverse Logistics Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Returns Triage Agent intervenes.
2. **What the Agent Does**: Evaluates item condition scans to triage restock, vendor return, or liquidation.
3. **Expected Outcome**: Restocks sellable returns within 24h. (**Restocks sellable returns within 24h**).

#### 🗄️ Demo Data Details (`agents/returns_triage_agent/fixtures/tables/`)
- **`returns_triage_agent_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=RETURN-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Omnichannel Visibility`
- **`returns_triage_agent_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=RETURN-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Reverse Logistics Lead`
- **`returns_triage_agent_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=04 · Inventory & DC | Omnichannel Visibility`, `service_level_pct=88.4`
- **`returns_triage_agent_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=RETURN-TEL-101`, `company_id=XYZ-CORP-01`, `category=04 · Inventory & Warehousing — Omnichannel Visibility`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_returns_triage_agent_telemetry_feed, query_returns_triage_agent_constraint_matrix, query_returns_triage_agent_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Gemini Multimodal Vision Defect Grader + Google Maps & Mathematical Optimization Solver (MILP / CP-SAT) Dynamic Backhaul Insertion CVRPTW**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_returns_triage_agent_plan, action_dispatch_returns_triage_agent_alert` (TMS Fleet Backhaul Pickup Stop, Warehouse Management System (WMS / MCP) Direct-to-Hub Restock & Vendor Warranty Debit Memo) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Omnichannel Visibility signals for Returns Triage Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_returns_triage_agent_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py returns_triage_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py returns_triage_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py returns_triage_agent --test-guardrail

# Run unit smoke tests:
pytest agents/returns_triage_agent/tests/test_smoke.py -v
```

---

## 06 · Control Tower & Governance (9 Agents)

### 52. Return Fraud Sentinel (`reverse_rma_optimizer`)
- **Pillar / Sub-Pillar**: 06 · Control Tower & Governance — **Returns & Claims Mgmt**
- **Primary Human Persona**: Reverse Logistics / Fraud Lead · **ROI Badge**: `Cuts returns fraud abuse by 25–40%` · 🟢 **Live Vertex AI RE**: `5468667646226464768`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Returns & Claims Mgmt, Reverse Logistics / Fraud Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Return Fraud Sentinel intervenes.
2. **What the Agent Does**: Analyzes item photos and packaging video feeds to detect wear or swapped tags.
3. **Expected Outcome**: Cuts returns fraud abuse by 25–40%. (**Cuts returns fraud abuse by 25–40%**).

#### 🗄️ Demo Data Details (`agents/reverse_rma_optimizer/fixtures/tables/`)
- **`circular_disposition_routing_ledger.json`** (1 rows) — Columns: `disposition_id, rma_id, routing_path, target_facility_id, central_return_touch_bypassed` · Sample Record: `disposition_id=DISP-501`, `rma_id=RMA-20261022-501`, `routing_path=DIRECT_REGIONAL_FDC_RESTOCK`, `target_facility_id=FDC-AUSTIN-02`
- **`customer_rma_intake_requests.json`** (2 rows) — Columns: `rma_id, customer_id, sku_id, units, retail_value_usd, stated_reason` · Sample Record: `rma_id=RMA-20261022-501`, `customer_id=RETAIL-PARTNER-09`, `sku_id=SKU-PRO-ESPRESSO-X1`, `units=12`
- **`fleet_backhaul_pickup_slots.json`** (1 rows) — Columns: `pickup_slot_id, rma_id, returning_vehicle_id, detour_distance_km, ltl_shipping_saved_usd` · Sample Record: `pickup_slot_id=BKH-RMA-501`, `rma_id=RMA-20261022-501`, `returning_vehicle_id=TRK-12T-TX14`, `detour_distance_km=2.4`
- **`multimodal_vision_grading_results.json`** (1 rows) — Columns: `grading_id, rma_id, optical_grade, tamper_seal_verified, net_recovery_pct, recoverable_value_usd` · Sample Record: `grading_id=GRD-501`, `rma_id=RMA-20261022-501`, `optical_grade=GRADE_A_FACTORY_SEAL_INTACT`, `tamper_seal_verified=True`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_customer_rma_intake_requests, query_multimodal_vision_grading_results, query_fleet_backhaul_pickup_slots` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Gemini Multimodal Vision Defect Grader + Google Maps & Mathematical Optimization Solver (MILP / CP-SAT) Dynamic Backhaul Insertion CVRPTW**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_assign_rma_disposition_and_backhaul, action_issue_instant_customer_rma_credit_or_swap` (TMS Fleet Backhaul Pickup Stop, Warehouse Management System (WMS / MCP) Direct-to-Hub Restock & Vendor Warranty Debit Memo) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Returns & Claims Mgmt signals for Return Fraud Sentinel, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_assign_rma_disposition_and_backhaul immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py reverse_rma_optimizer

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py reverse_rma_optimizer --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py reverse_rma_optimizer --test-guardrail

# Run unit smoke tests:
pytest agents/reverse_rma_optimizer/tests/test_smoke.py -v
```

---

### 53. Keep-It & Routing Advisor (`keep_it_routing_advisor`)
- **Pillar / Sub-Pillar**: 06 · Control Tower & Governance — **Returns & Claims Mgmt**
- **Primary Human Persona**: Customer Experience (CX) Lead · **ROI Badge**: `Lowers net return costs by 15–22%`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Returns & Claims Mgmt, Customer Experience (CX) Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Keep-It & Routing Advisor intervenes.
2. **What the Agent Does**: Evaluates salvage margins vs reverse freight to determine keep-it instant refunds.
3. **Expected Outcome**: Lowers net return costs by 15–22%. (**Lowers net return costs by 15–22%**).

#### 🗄️ Demo Data Details (`agents/keep_it_routing_advisor/fixtures/tables/`)
- **`keep_it_routing_advisor_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=KEEP_I-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Returns & Claims Mgmt`
- **`keep_it_routing_advisor_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=KEEP_I-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Customer Experience (CX) Lead`
- **`keep_it_routing_advisor_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=06 · Returns & ESG | Returns & Claims Mgmt`, `service_level_pct=88.4`
- **`keep_it_routing_advisor_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=KEEP_I-TEL-101`, `company_id=XYZ-CORP-01`, `category=06 · Returns & Reverse Logistics — Returns & Claims Mgmt`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_keep_it_routing_advisor_telemetry_feed, query_keep_it_routing_advisor_constraint_matrix, query_keep_it_routing_advisor_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Gemini Multimodal Vision Defect Grader + Google Maps & Mathematical Optimization Solver (MILP / CP-SAT) Dynamic Backhaul Insertion CVRPTW**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_keep_it_routing_advisor_plan, action_dispatch_keep_it_routing_advisor_alert` (TMS Fleet Backhaul Pickup Stop, Warehouse Management System (WMS / MCP) Direct-to-Hub Restock & Vendor Warranty Debit Memo) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Returns & Claims Mgmt signals for Keep-It & Routing Advisor, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_keep_it_routing_advisor_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py keep_it_routing_advisor

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py keep_it_routing_advisor --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py keep_it_routing_advisor --test-guardrail

# Run unit smoke tests:
pytest agents/keep_it_routing_advisor/tests/test_smoke.py -v
```

---

### 54. OS&D Freight Claims (`osd_freight_claims_agent`)
- **Pillar / Sub-Pillar**: 06 · Control Tower & Governance — **Returns & Claims Mgmt**
- **Primary Human Persona**: Claims Specialist / Controller · **ROI Badge**: `Resolves carrier claims in <72 hours`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Returns & Claims Mgmt, Claims Specialist / Controller teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before OS&D Freight Claims intervenes.
2. **What the Agent Does**: Reconciles eBOLs, dock damage logs, and carrier contracts to auto-file disputes.
3. **Expected Outcome**: Resolves carrier claims in <72 hours. (**Resolves carrier claims in <72 hours**).

#### 🗄️ Demo Data Details (`agents/osd_freight_claims_agent/fixtures/tables/`)
- **`osd_freight_claims_agent_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=OSD_FR-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Returns & Claims Mgmt`
- **`osd_freight_claims_agent_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=OSD_FR-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Claims Specialist / Controller`
- **`osd_freight_claims_agent_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=06 · Returns & ESG | Returns & Claims Mgmt`, `service_level_pct=88.4`
- **`osd_freight_claims_agent_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=OSD_FR-TEL-101`, `company_id=XYZ-CORP-01`, `category=06 · Returns & Reverse Logistics — Returns & Claims Mgmt`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_osd_freight_claims_agent_telemetry_feed, query_osd_freight_claims_agent_constraint_matrix, query_osd_freight_claims_agent_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **BigQuery ML 72-Hr MABD Breach Predictor + Mathematical Optimization Solver (MILP / CP-SAT) Penalty-vs-Expedite NPV Solver + Document AI Dispute Assembler**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_osd_freight_claims_agent_plan, action_dispatch_osd_freight_claims_agent_alert` (ERP Order Management (SD / MCP) Alternate-DC Order Re-Allocation & Automated Retailer Portal Dispute Submission via MCP / REST / On-Prem Gateway) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Returns & Claims Mgmt signals for OS&D Freight Claims, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_osd_freight_claims_agent_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py osd_freight_claims_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py osd_freight_claims_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py osd_freight_claims_agent --test-guardrail

# Run unit smoke tests:
pytest agents/osd_freight_claims_agent/tests/test_smoke.py -v
```

---

### 55. Dynamic Markdown Agent (`dynamic_markdown_agent`)
- **Pillar / Sub-Pillar**: 06 · Control Tower & Governance — **Expiry & Markdowns**
- **Primary Human Persona**: Merchandising / Store Ops Mgr · **ROI Badge**: `Cuts perishable scrap by 20–35%`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Expiry & Markdowns, Merchandising / Store Ops Mgr teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Dynamic Markdown Agent intervenes.
2. **What the Agent Does**: Correlates days-to-expiry (DTE) with sales velocity to trigger ESL shelf price cuts.
3. **Expected Outcome**: Cuts perishable scrap by 20–35%. (**Cuts perishable scrap by 20–35%**).

#### 🗄️ Demo Data Details (`agents/dynamic_markdown_agent/fixtures/tables/`)
- **`dynamic_markdown_agent_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=DYNAMI-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Expiry & Markdowns`
- **`dynamic_markdown_agent_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=DYNAMI-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Merchandising / Store Ops Mgr`
- **`dynamic_markdown_agent_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=06 · Returns & ESG | Expiry & Markdowns`, `service_level_pct=88.4`
- **`dynamic_markdown_agent_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=DYNAMI-TEL-101`, `company_id=XYZ-CORP-01`, `category=06 · Returns & Reverse Logistics — Expiry & Markdowns`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_dynamic_markdown_agent_telemetry_feed, query_dynamic_markdown_agent_constraint_matrix, query_dynamic_markdown_agent_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **BigQuery ML Causal Double-ML Uplift + Cross-SKU Cannibalization Matrix + Mathematical Optimization Solver (MILP / CP-SAT) Supply-Aware Price Shaper**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_dynamic_markdown_agent_plan, action_dispatch_dynamic_markdown_agent_alert` (Salesforce / SAP Trade Promo Calendar Lock & Shaped Regional SKU Curve Update) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Expiry & Markdowns signals for Dynamic Markdown Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_dynamic_markdown_agent_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py dynamic_markdown_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py dynamic_markdown_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py dynamic_markdown_agent --test-guardrail

# Run unit smoke tests:
pytest agents/dynamic_markdown_agent/tests/test_smoke.py -v
```

---

### 56. Short-Dated Redistributor (`short_dated_redistributor`)
- **Pillar / Sub-Pillar**: 06 · Control Tower & Governance — **Expiry & Markdowns**
- **Primary Human Persona**: Inventory Disposition Lead · **ROI Badge**: `Diverts bulk perishables from landfill`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Expiry & Markdowns, Inventory Disposition Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Short-Dated Redistributor intervenes.
2. **What the Agent Does**: Matches near-date DC lots with discounters or food banks before acceptance cutoffs.
3. **Expected Outcome**: Diverts bulk perishables from landfill. (**Diverts bulk perishables from landfill**).

#### 🗄️ Demo Data Details (`agents/short_dated_redistributor/fixtures/tables/`)
- **`short_dated_redistributor_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=SHORT_-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Expiry & Markdowns`
- **`short_dated_redistributor_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=SHORT_-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Inventory Disposition Lead`
- **`short_dated_redistributor_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=06 · Returns & ESG | Expiry & Markdowns`, `service_level_pct=88.4`
- **`short_dated_redistributor_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=SHORT_-TEL-101`, `company_id=XYZ-CORP-01`, `category=06 · Returns & Reverse Logistics — Expiry & Markdowns`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_short_dated_redistributor_telemetry_feed, query_short_dated_redistributor_constraint_matrix, query_short_dated_redistributor_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Mathematical Optimization Solver (MILP / CP-SAT) CP-SAT Inbound-to-Outbound Door Coupling + Flow-Through Pallet De-Consolidation MILP**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_short_dated_redistributor_plan, action_dispatch_short_dated_redistributor_alert` (Warehouse Management System (WMS / MCP) / Manhattan Cross-Dock Flow-Through Directive, Conveyor Sortation Route & Outbound Staging Lock) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Expiry & Markdowns signals for Short-Dated Redistributor, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_short_dated_redistributor_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py short_dated_redistributor

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py short_dated_redistributor --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py short_dated_redistributor --test-guardrail

# Run unit smoke tests:
pytest agents/short_dated_redistributor/tests/test_smoke.py -v
```

---

### 57. Food Waste & ESG Copilot (`food_waste_esg_copilot`)
- **Pillar / Sub-Pillar**: 06 · Control Tower & Governance — **Expiry & Markdowns**
- **Primary Human Persona**: Chief Sustainability Officer · **ROI Badge**: `Automates annual circularity reporting`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Expiry & Markdowns, Chief Sustainability Officer teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Food Waste & ESG Copilot intervenes.
2. **What the Agent Does**: Aggregates store shrink and organic haul logs to generate audited GHG diversion filings.
3. **Expected Outcome**: Automates annual circularity reporting. (**Automates annual circularity reporting**).

#### 🗄️ Demo Data Details (`agents/food_waste_esg_copilot/fixtures/tables/`)
- **`food_waste_esg_copilot_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=FOOD_W-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Expiry & Markdowns`
- **`food_waste_esg_copilot_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=FOOD_W-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Chief Sustainability Officer`
- **`food_waste_esg_copilot_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=06 · Returns & ESG | Expiry & Markdowns`, `service_level_pct=88.4`
- **`food_waste_esg_copilot_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=FOOD_W-TEL-101`, `company_id=XYZ-CORP-01`, `category=06 · Returns & Reverse Logistics — Expiry & Markdowns`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_food_waste_esg_copilot_telemetry_feed, query_food_waste_esg_copilot_constraint_matrix, query_food_waste_esg_copilot_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **BigQuery ISO-14083 Primary Telemetry Carbon Calculator + Earth Engine Canopy Verifier + Mathematical Optimization Solver (MILP / CP-SAT) Cost/Carbon Mode-Shift MILP**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_food_waste_esg_copilot_plan, action_dispatch_food_waste_esg_copilot_alert` (EU CBAM / EUDR XML Customs Filing & Transportation Management System (TMS / MCP) / Supply Chain Execution Platform (MCP / API) Low-Carbon Rail/EV/Ocean Lane Allocation) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Expiry & Markdowns signals for Food Waste & ESG Copilot, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_food_waste_esg_copilot_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py food_waste_esg_copilot

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py food_waste_esg_copilot --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py food_waste_esg_copilot --test-guardrail

# Run unit smoke tests:
pytest agents/food_waste_esg_copilot/tests/test_smoke.py -v
```

---

### 58. RTI Balance Reconciler (`rti_balance_reconciler`)
- **Pillar / Sub-Pillar**: 06 · Control Tower & Governance — **Pallet & Tote Reclamation**
- **Primary Human Persona**: Asset Recovery / RTI Manager · **ROI Badge**: `Eliminates 30% in non-return fee fines`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Pallet & Tote Reclamation, Asset Recovery / RTI Manager teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before RTI Balance Reconciler intervenes.
2. **What the Agent Does**: Reconciles RFID portal scans with CHEP/PECO statements to detect hoarding nodes.
3. **Expected Outcome**: Eliminates 30% in non-return fee fines. (**Eliminates 30% in non-return fee fines**).

#### 🗄️ Demo Data Details (`agents/rti_balance_reconciler/fixtures/tables/`)
- **`rti_balance_reconciler_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=RTI_BA-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Pallet & Tote Reclamation`
- **`rti_balance_reconciler_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=RTI_BA-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Asset Recovery / RTI Manager`
- **`rti_balance_reconciler_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=06 · Returns & ESG | Pallet & Tote Reclamation`, `service_level_pct=88.4`
- **`rti_balance_reconciler_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=RTI_BA-TEL-101`, `company_id=XYZ-CORP-01`, `category=06 · Returns & Reverse Logistics — Pallet & Tote Reclamation`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_rti_balance_reconciler_telemetry_feed, query_rti_balance_reconciler_constraint_matrix, query_rti_balance_reconciler_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **BigQuery ML Empirical Bayesian Lead-Time Estimator + Isolation-Forest Master Anomaly Detector + Enterprise API & MCP Gateway SAP BAPI Steward**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_rti_balance_reconciler_plan, action_dispatch_rti_balance_reconciler_alert` (SAP BAPI_MATERIAL_SAVEDATA & Purchasing Info-Record Lead-Time / Route / 3D Dimension Auto-Update) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Pallet & Tote Reclamation signals for RTI Balance Reconciler, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_rti_balance_reconciler_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py rti_balance_reconciler

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py rti_balance_reconciler --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py rti_balance_reconciler --test-guardrail

# Run unit smoke tests:
pytest agents/rti_balance_reconciler/tests/test_smoke.py -v
```

---

### 59. Milk-Run Consolidation (`intermodal_rail_linehaul_agent`)
- **Pillar / Sub-Pillar**: 06 · Control Tower & Governance — **Pallet & Tote Reclamation**
- **Primary Human Persona**: Reverse Transport Planner · **ROI Badge**: `Boosts backhaul fill rate by 25–40%`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Pallet & Tote Reclamation, Reverse Transport Planner teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Milk-Run Consolidation intervenes.
2. **What the Agent Does**: Schedules dynamic backhauls to collect empty roll cages and RPCs from retail stores.
3. **Expected Outcome**: Boosts backhaul fill rate by 25–40%. (**Boosts backhaul fill rate by 25–40%**).

#### 🗄️ Demo Data Details (`agents/intermodal_rail_linehaul_agent/fixtures/tables/`)
- **`intermodal_corridor_shipments.json`** (1 rows) — Columns: `shipment_id, origin_hub, dest_dc, distance_miles, otr_truck_cost_usd, cofc_rail_cost_usd` · Sample Record: `shipment_id=SHP-IM-LA-CHI-701`, `origin_hub=Los Angeles Factory Hub`, `dest_dc=Chicago Joliet RDC`, `distance_miles=2015`
- **`otr_to_rail_mode_conversion_ledger.json`** (1 rows) — Columns: `corridor_lane, containers_converted, cost_savings_pct, total_usd_saved, co2e_reduction_pct, tonnes_co2e_avoided` · Sample Record: `corridor_lane=LAX_TO_JOLIET_CHI`, `containers_converted=18`, `cost_savings_pct=37.8`, `total_usd_saved=31680.0`
- **`rail_ramp_cutoff_and_drayage.json`** (1 rows) — Columns: `ramp_id, crane_grounding_utc, free_time_hours, assigned_dray_tractor, chassis_id, zero_storage_dwell_verified` · Sample Record: `ramp_id=LPC_JOLIET_CHI`, `crane_grounding_utc=2026-10-25T15:30:00Z`, `free_time_hours=24`, `assigned_dray_tractor=JBHT-DRAY-CHI42`
- **`railinc_edi417_train_consists.json`** (1 rows) — Columns: `train_id, rail_carrier, origin_ramp, dest_ramp, articulated_well_car, clm_sighting` · Sample Record: `train_id=BNSF-Q-LACCHI-22`, `rail_carrier=BNSF_RAILWAY`, `origin_ramp=HOBART_LAX`, `dest_ramp=LPC_JOLIET_CHI`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_intermodal_corridor_shipments, query_railinc_edi417_train_consists, query_rail_ramp_cutoff_and_drayage` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Mathematical Optimization Solver (MILP / CP-SAT) Multi-Corridor Rail/Truck Linehaul MILP + Rail Ramp Cutoff & Chassis Pool Synchronizer**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_tender_edi404_rail_intermodal_bill, action_synchronize_ramp_crane_drayage_slot` (Railinc EDI 404 Rail Bill Tender, EDI 322 Ramp Gate Slot & Coupled Origin/Destination Drayage Dispatch) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Pallet & Tote Reclamation signals for Milk-Run Consolidation, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_tender_edi404_rail_intermodal_bill immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py intermodal_rail_linehaul_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py intermodal_rail_linehaul_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py intermodal_rail_linehaul_agent --test-guardrail

# Run unit smoke tests:
pytest agents/intermodal_rail_linehaul_agent/tests/test_smoke.py -v
```

---

### 60. Sanitation & Health Agent (`sanitation_health_agent`)
- **Pillar / Sub-Pillar**: 06 · Control Tower & Governance — **Pallet & Tote Reclamation**
- **Primary Human Persona**: Packaging QA / Food Safety · **ROI Badge**: `Extends reusable lifecycle by 15–20%`

#### 🎯 What This Agent Does (Simple Voiceover Summary)
1. **The Problem It Solves**: In Pallet & Tote Reclamation, Packaging QA / Food Safety teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Sanitation & Health Agent intervenes.
2. **What the Agent Does**: Inspects return photos and wash logs for structural fatigue and chemical compliance.
3. **Expected Outcome**: Extends reusable lifecycle by 15–20%. (**Extends reusable lifecycle by 15–20%**).

#### 🗄️ Demo Data Details (`agents/sanitation_health_agent/fixtures/tables/`)
- **`sanitation_health_agent_constraint_matrix.json`** (3 rows) — Columns: `constraint_id, sku_id, vendor_id, sub_pillar, capacity_limit, current_load` · Sample Record: `constraint_id=SANITA-CON-201`, `sku_id=SKU-SEMI-9900-X1`, `vendor_id=VND-T1-TSMC-TW01`, `sub_pillar=Pallet & Tote Reclamation`
- **`sanitation_health_agent_execution_ledger.json`** (3 rows) — Columns: `execution_id, shipment_id, order_id, persona_owner, erp_system, writeback_bapi` · Sample Record: `execution_id=SANITA-EXE-301`, `shipment_id=SHP-XYZ-90884`, `order_id=ORD-XYZ-2026-99401`, `persona_owner=Packaging QA / Food Safety`
- **`sanitation_health_agent_optimization_scenarios.json`** (3 rows) — Columns: `scenario_id, scenario_name, category, service_level_pct, annual_cost_usd, cycle_time_hrs` · Sample Record: `scenario_id=SCEN-BASELINE-MANUAL`, `scenario_name=Legacy Manual Spreadsheet Baseline`, `category=06 · Returns & ESG | Pallet & Tote Reclamation`, `service_level_pct=88.4`
- **`sanitation_health_agent_telemetry_feed.json`** (4 rows) — Columns: `record_id, company_id, category, facility_id, sku_id, order_id` · Sample Record: `record_id=SANITA-TEL-101`, `company_id=XYZ-CORP-01`, `category=06 · Returns & Reverse Logistics — Pallet & Tote Reclamation`, `facility_id=FAC-PLANT-US-AUS01`

#### ⚙️ What Happens When You Test It (Step-by-Step Flow)
1. **Reads Live Demo Tables**: Calls `query_sanitation_health_agent_telemetry_feed, query_sanitation_health_agent_constraint_matrix, query_sanitation_health_agent_optimization_scenarios` across the 4 fixture tables above.
2. **Solves & Optimizes**: Routes via Dynamic Orchestrator (`Gemini 3.8 Flash` ↔ `Gemini 3.1 Pro / 4 Argon`) + **Vertex AI Edge Multimodal Vision Defect Classifier + BigQuery ML Bayesian Closed-Loop SPC Parameter Controller**.
3. **Checks Governance Gate**: Validates required fields & `idempotency_key` via `enforce_tool_contract()`.
4. **Executes Write-Back & Visual**: Calls `action_commit_sanitation_health_agent_plan, action_dispatch_sanitation_health_agent_alert` (Bounded PLC Recipe Offset Recommendation & Automated Quality Management System (QMS / ERP) Usage Decision (BAPI_INSPLOT_SETUSAGEDECISION)) and outputs an interactive **A2UI `VegaChart`** + **Copy-Ready Markdown Table**.

#### 🧪 How to Test It (Copy-Paste Prompts & Commands)
- **Demo Prompt (Paste in ADK Web UI or Gemini Enterprise)**:
  > `Analyze live Pallet & Tote Reclamation signals for Sanitation & Health Agent, identify critical bottlenecks or anomalies, and execute the recommended write-back with idempotency_key='DEMO-2026-001'.`
- **Safety Gate Test Prompt (Shows Governance Blocking Un-Keyed Writes)**:
  > `Call action_commit_sanitation_health_agent_plan immediately WITHOUT providing an idempotency_key to verify the pre-execution governance gate.`
- **Terminal Commands**:
```bash
# Run full scenario & print Markdown report + write-back receipts:
python3 scripts/test_agent_demo.py sanitation_health_agent

# Inspect demo data tables & sample rows:
python3 scripts/test_agent_demo.py sanitation_health_agent --show-data

# Test pre-execution safety gate:
python3 scripts/test_agent_demo.py sanitation_health_agent --test-guardrail

# Run unit smoke tests:
pytest agents/sanitation_health_agent/tests/test_smoke.py -v
```

---

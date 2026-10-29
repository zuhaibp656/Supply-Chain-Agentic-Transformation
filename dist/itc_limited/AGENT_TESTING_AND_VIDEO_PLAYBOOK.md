# 🎬 Supply Chain AI Agents — Manual Testing, Expected Output & Customer Explanation Playbook

> **Built for Manual Verification & Customer Demos**: For all **60 Supply Chain AI Agents**, this playbook gives you:
> 1. **Plain-English Customer Explanation (Zero Unexplained Abbreviations)**: What problem the customer has, why it matters, and how this agent solves it — with every acronym (`OTIF`, `WAPE`, `S&OP`, `ATP`, `MEIO`, etc.) spelled out and explained.
> 2. **Exact Input Data -> Exact Expected Output**: What input prompt you give, which demo data tables & resources the agent must read, the **exact Markdown table & numbers** it must reply with, the **exact A2UI `VegaChart` graphic** it must render, and the **exact ERP/WMS Write-Back receipt** it must return.
> 3. **5-Point Manual Verification Checklist**: So you can verify manually that every agent does what it says, uses all its resources, and renders its A2UI graphics.

> 💡 **New to Supply Chain?** Open the companion **[🎓 Supply Chain 101 Interactive Academy (`supply_chain_101_interactive_academy.html`)](supply_chain_101_interactive_academy.html)** (or **[`SUPPLY_CHAIN_101_MASTER_GUIDE.md`](SUPPLY_CHAIN_101_MASTER_GUIDE.md)**) to learn Supply Chain from scratch with visual diagrams, 56 3D flip-flashcards, and a Customer Conversation Decoder!

---

## 01 · Planning & Strategy (12 Agents)

### 1. Demand Sensing Agent (`demand_sensing_agent`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **Demand Forecasting** · **Persona**: Demand Planner / Forecaster · **ROI**: `Detects demand shifts 7–14 days earlier`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Demand Forecasting, Demand Planner / Forecaster teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Demand Sensing Agent intervenes.
- **What This Agent Does**: Synthesizes POS (Point of Sale — cash-register store scans) velocity, weather anomalies, and macro trends.
- **Business Result**: Detects demand shifts 7–14 days earlier. (**Detects demand shifts 7–14 days earlier**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Demand Sensing Agent.`
- **Read Tools It Must Call**: `query_pos_store_scans, query_external_demand_signals, query_timesfm_forecast_horizons, query_fva_sales_bias`
- **Write-Back Tools It Must Call**: `action_commit_ibp_pir_change, action_suppress_fva_bias`
- **Demo Data Input Values It Reads**:
  - Table `external_signals_weathernext.json` (3 rows): Sample input record has `signal_id=SIG-WN3-TX-HEAT, provider=Google DeepMind WeatherNext 3, region=US-CENTRAL, event_type=UNSEASONABLE_HEATWAVE, temperature_anomaly_celsius=6.8`
  - Table `fva_sales_bias.json` (2 rows): Sample input record has `override_id=OVR-SALES-202610-01, sku_id=SKU-BEV-ISOTONIC-32OZ, sales_account=Key Account Walmart, planner_id=REP-JOHNSON-CENTRAL, statistical_baseline_units=262000`
  - Table `pos_store_scans.json` (6 rows): Sample input record has `store_id=STORE-WALMART-DAL-104, retailer=Walmart, region=US-CENTRAL, sku_id=SKU-BEV-ISOTONIC-32OZ, category=Hydration Beverages`
  - Table `timesfm_quantile_horizons.json` (3 rows): Sample input record has `forecast_id=TFM-FC-202610-001, sku_id=SKU-BEV-ISOTONIC-32OZ, region=US-CENTRAL, horizon_days=14, p10_units=245000`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `Operational A2UI Visual Surface`
  - **Visual Mark Type**: `AREA + LINE + POINT` (16 data points: `date=2026-10-01, type=HISTORICAL, actual_units=14200 | date=2026-10-03, type=HISTORICAL, actual_units=13950 | date=2026-10-05, type=HISTORICAL, actual_units=15800`)
- **Expected Write-Back Receipt**: `{"dampen_id": "FVA-DAMPEN-43C92615", "override_id": "OVR-SALES-202610-01", "recommended_dampened_units": 298000, "status": "BIAS_DAMPENED_APPLIED", "rationale": "Strip -4.2% historical FVA optimism bias to prevent stranded safety stock.", "idempotency_key": "DAMPEN-20261017-001"}`
- **Expected Markdown Report & Table**:

### 🌊 PulseCast Demand Sensing & TimesFM Quantile Briefing

> **Executive Summary**: Identified unseasonable heatwave surge (+28.5% category lift) in US-Central via **Google DeepMind WeatherNext 3** paired with severe POS stockout censorship at Kroger. Imputed true latent demand in BigQuery and generated 14-day P10/P50/P90 quantile fans using **Vertex AI TimesFM** (WAPE reduced to **5.2%**). Neutralized chronic commercial optimism bias (-4.2% FVA) and committed updated PIR directly to **SAP IBP**.

#### 📊 Sensed Demand & TimesFM Horizon Ledger (Atomic Copy-Ready Table)

| SKU ID | Region | Weather Trigger | TimesFM P50 | Baseline ERP | WAPE % | Revenue at Risk |
|:---|:---|:---|---:|---:|---:|---:|
| `SKU-BEV-ISOTONIC-32OZ` | US-CENTRAL | WeatherNext Heatwave (+6.8°C) | 298,000 | 262,000 | 5.2% | $180,000 |
| `SKU-SNACK-PROTEIN-BAR` | US-MIDWEST | Maps Marathon Lift (+19.0%) | 142,000 | 135,000 | 4.8% | $35,000 |
| `SKU-BEV-ELECTROLYTE-500ML` | EU-UK | Retail Promo Carryover | 105,000 | 98,000 | 6.1% | $42,000 |

#### ⚡ Autonomous Writebacks & Bias Governance Executed

- **FVA Sales Bias Dampened**: `FVA-DAMPEN-43C92615` | Override ID: `OVR-SALES-202610-01` | Dampened To: **298,000** units | Status: `BIAS_DAMPENED_APPLIED`
- **SAP IBP Key Figure Committed**: `IBP-PIR-5EEF3A8C` | SKU: `SKU-BEV-ISOTONIC-32OZ` | Key Figure: `CONSENSUS_DEMAND_SAMPLED_P50` | Units: **298,000** | Status: `IBP_COMMITTED_SUCCESS`

### 🔗 Connected Systems & Data Foundation
- **BigQuery Enterprise Demand Lake**: Ingesting daily EDI 852 store scans and censured sales imputation.
- **Google DeepMind WeatherNext 3**: Real-time atmospheric temperature and precipitation anomaly forecasting.
- **Vertex AI TimesFM**: High-throughput zero-shot foundation model generating calibrated quantile fans.
- **SAP IBP & Apigee**: BAPI_PIR_CHANGE writeback protocol updating Planned Independent Requirements.

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_pos_store_scans, query_external_demand_signals` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `Operational A2UI Visual Surface` (`AREA + LINE + POINT`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_ibp_pir_change` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 2. Forecast Reconciliation (`cpfr_sync_agent`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **Demand Forecasting** · **Persona**: Commercial Planning Lead · **ROI**: `Replaces black-box variance models`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Demand Forecasting, Commercial Planning Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Forecast Reconciliation intervenes.
- **What This Agent Does**: Identifies unmodeled drivers across eCommerce and retail channels.
- **Business Result**: Replaces black-box variance models. (**Replaces black-box variance models**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Forecast Reconciliation.`
- **Read Tools It Must Call**: `query_retailer_edi852_pos, query_retailer_edi830_forecasts, query_phantom_inventory_anomalies, query_joint_cpfr_packets`
- **Write-Back Tools It Must Call**: `action_dispatch_vmi_replenishment_order, action_flag_retail_phantom_audit`
- **Demo Data Input Values It Reads**:
  - Table `joint_cpfr_consensus_packets.json` (2 rows): Sample input record has `packet_id=CPFR-PKT-202611-WMT, retailer=Walmart, sku_id=SKU-BEV-ISOTONIC-32OZ, retailer_forecast_units=620000, manufacturer_unconstrained_units=540000`
  - Table `retailer_edi830_order_forecasts.json` (2 rows): Sample input record has `forecast_id=EDI830-WMT-202611, retailer=Walmart, sku_id=SKU-BEV-ISOTONIC-32OZ, horizon_weeks=12, current_week_order_units=125000`
  - Table `retailer_edi852_daily_pos.json` (3 rows): Sample input record has `edi_record_id=EDI852-20261016-01, retailer=Walmart, store_id=STORE-WALMART-DAL-104, region=US-CENTRAL, sku_id=SKU-BEV-ISOTONIC-32OZ`
  - Table `store_phantom_inventory_anomalies.json` (2 rows): Sample input record has `anomaly_id=PHANTOM-KROGER-ATL-01, store_id=STORE-KROGER-ATL-209, retailer=Kroger, sku_id=SKU-BEV-ISOTONIC-32OZ, book_inventory_units=380`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `Operational A2UI Visual Surface`
  - **Visual Mark Type**: `BAR + LINE + POINT` (9 data points: `date=2026-10-01, store_scans=48200, cpfr_consensus=46500 | date=2026-10-03, store_scans=49100, cpfr_consensus=47800 | date=2026-10-05, store_scans=52400, cpfr_consensus=51000`)
- **Expected Write-Back Receipt**: `{"audit_id": "AUDIT-TASK-94134425", "anomaly_id": "PHANTOM-KROGER-ATL-01", "store_id": "STORE-KROGER-ATL-209", "retailer": "Kroger", "sku_id": "SKU-BEV-ISOTONIC-32OZ", "expected_audit_date": "2026-10-18", "status": "STORE_AUDIT_DISPATCHED", "rationale": "4 consecutive days zero scans with 380 book units; trigger urgent on-shelf physical cycle count.", "idempotency_key": "AUDIT-20261017-001"}`
- **Expected Markdown Report & Table**:

### 📡 ChannelSync Collaborative CPFR & POS Harmonizer Briefing

> **Executive Summary**: Harmonized multi-retailer daily EDI 852 scan feeds across Walmart, Kroger, and Target via **Cloud Dataflow** and **BigQuery**. Flagged a critical **phantom inventory stockout at Kroger Atlanta** (4 consecutive days of zero scans masked by 380 units of ghost book inventory, leaking $2,451/day). Reconciled Walmart's **80,000-unit bullwhip forecast divergence** down to realistic POS consumption velocity, and autonomously dispatched a **95,000-unit VMI replenishment order (EDI 855)** to DC Dallas, lifting retail On-Shelf Availability (OSA) by **+3.8 points**.

#### 📊 Multi-Retailer CPFR Reconciliation Ledger (Atomic Copy-Ready Table)

| Retailer | Store / DC | SKU ID | Daily Scans | Book Stock | Anomaly Status | CPFR Consensus | VMI Order Units | Retail OSA % |
|:---|:---|:---|---:|---:|:---|---:|---:|---:|
| `Walmart` | `DC-DALLAS-CENTRAL` | `SKU-BEV-ISOTONIC-32OZ` | 1,840 | 420 | `ALIGNED_FLOW` | 580,000 | **95,000** | 98.2% |
| `Kroger` | `STORE-KROGER-ATL-209` | `SKU-BEV-ISOTONIC-32OZ` | 0 | 380 | `PHANTOM_STOCKOUT` | 42,000 | **Audit Triggered** | 84.5% (Depleted) |
| `Target` | `DC-CHICAGO-MIDWEST` | `SKU-SNACK-PROTEIN-BAR` | 1,280 | 310 | `STABLE_CONSENSUS` | 275,000 | **45,000** | 96.8% |

#### ⚡ Automated CPFR Dispatches & Physical Audits Executed

- **Store Phantom Stockout Audit Dispatched**: `AUDIT-TASK-94134425` | Store: `STORE-KROGER-ATL-209` | Retailer: `Kroger` | Due Date: `2026-10-18` | Status: `STORE_AUDIT_DISPATCHED`
- **VMI Replenishment Order Dispatched (EDI 855)**: `VMI-PO-C8CF3A6E` | Retailer: `Walmart` | SKU: `SKU-BEV-ISOTONIC-32OZ` | Quantity: **95,000** units | Target: `DC-DALLAS-CENTRAL` | Status: `VMI_PO_TRANSMITTED_EDI855`

### 🔗 Connected Systems & EDI Integration Stack
- **Cloud Dataflow EDI Pipeline**: High-throughput AS2/SFTP ingestion normalizing EDI 852 (POS) and EDI 830 (Forecasts).
- **BigQuery Zero-Scan Poisson Model**: Anomaly detection isolating phantom inventory and ghost shelf stock.
- **SAP IBP Collaborative Planning**: Real-time CPFR exception workbench harmonizing retailer vs supplier forecasts.
- **Vendor Managed Inventory (VMI) Gateway**: Automated EDI 855 purchase order generation directly to 3PL logistics.

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_retailer_edi852_pos, query_retailer_edi830_forecasts` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `Operational A2UI Visual Surface` (`BAR + LINE + POINT`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_dispatch_vmi_replenishment_order` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 3. NPI Demand Profiler (`npi_demand_profiler`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **Demand Forecasting** · **Persona**: Brand & Innovation Manager · **ROI**: `Cuts 90-day launch forecast errors`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Demand Forecasting, Brand & Innovation Manager teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before NPI (New Product Introduction — launching a new item) Demand Profiler intervenes.
- **What This Agent Does**: Matches launch packaging and attributes to historical lookalikes.
- **Business Result**: Cuts 90-day launch forecast errors. (**Cuts 90-day launch forecast errors**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for NPI Demand Profiler.`
- **Read Tools It Must Call**: `query_npi_demand_profiler_telemetry_feed, query_npi_demand_profiler_constraint_matrix, query_npi_demand_profiler_optimization_scenarios, query_npi_demand_profiler_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_npi_demand_profiler_plan, action_dispatch_npi_demand_profiler_alert`
- **Demo Data Input Values It Reads**:
  - Table `npi_demand_profiler_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=NPI_DE-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Demand Forecasting, capacity_limit=12500`
  - Table `npi_demand_profiler_execution_ledger.json` (3 rows): Sample input record has `execution_id=NPI_DE-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Brand & Innovation Manager, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `npi_demand_profiler_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=01 · Plan | Demand Forecasting, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `npi_demand_profiler_telemetry_feed.json` (4 rows): Sample input record has `record_id=NPI_DE-TEL-101, company_id=XYZ-CORP-01, category=01 · Planning & Strategy — Demand Forecasting, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[01 · Plan | Demand Forecasting] NPI Demand Profiler — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-NPI_-F91EA654", "status": "COMMITTED", "category": "01 · Planning & Strategy — Demand Forecasting", "agent": "[01 · Plan | Demand Forecasting] NPI Demand Profiler", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "SAP IBP Key Figure & BAPI_PIR_CHANGE Write-Back (P10/P50/P90) via Apigee"}`
- **Expected Markdown Report & Table**:

#### 📊 [01 · Plan | Demand Forecasting] NPI Demand Profiler — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `NPI_DE-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `01 · Planning & Strategy — Demand Forecasting` · **Persona**: `Brand & Innovation Manager` · **Write-Back Receipt**: `ACT-NPI_-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_npi_demand_profiler_telemetry_feed, query_npi_demand_profiler_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[01 · Plan | Demand Forecasting] NPI Demand Profiler — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_npi_demand_profiler_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 4. Promo ROI Simulator (`promo_lift_simulator`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **Trade Promotion** · **Persona**: Trade Marketing Manager · **ROI**: `Prevents break-even trade leakage`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Trade Promotion, Trade Marketing Manager teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Promo ROI Simulator intervenes.
- **What This Agent Does**: Simulates price elasticity, shelf lift, and incremental spend return.
- **Business Result**: Prevents break-even trade leakage. (**Prevents break-even trade leakage**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Promo ROI Simulator.`
- **Read Tools It Must Call**: `query_planned_promo_campaigns, query_causal_promo_elasticity, query_cross_sku_cannibalization, query_warehouse_promo_availability`
- **Write-Back Tools It Must Call**: `action_shape_promotional_mechanic, action_lock_tpm_calendar`
- **Demo Data Input Values It Reads**:
  - Table `causal_promo_elasticity.json` (3 rows): Sample input record has `sku_id=SKU-BEV-ISOTONIC-32OZ, base_price_usd=2.99, discounted_price_usd=2.24, price_elasticity=-2.45, baseline_units=140000`
  - Table `cross_sku_cannibalization.json` (3 rows): Sample input record has `promoted_sku=SKU-BEV-ISOTONIC-32OZ, cannibalized_sku=SKU-BEV-ISOTONIC-16OZ, cannibalization_rate_pct=18.5, volume_diverted_units=16000, margin_loss_per_unit_usd=0.85`
  - Table `planned_promo_campaigns.json` (3 rows): Sample input record has `campaign_id=CMP-202611-BOGO, name=BOGO Hydration Blitz, retailer=Walmart, channel=Retail Stores & Omnichannel, start_date=2026-11-05`
  - Table `warehouse_promo_availability.json` (3 rows): Sample input record has `sku_id=SKU-BEV-ISOTONIC-32OZ, distribution_center=DC-DALLAS-CENTRAL, available_to_promise_units=95000, promo_surge_forecast_units=85000, buffer_safety_stock_units=20000`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `Operational A2UI Visual Surface`
  - **Visual Mark Type**: `BAR` (12 data points: `campaign=BOGO Hydration Blitz, component=Gross Promo Lift, volume_units=85000 | campaign=BOGO Hydration Blitz, component=Cannibalization Loss, volume_units=-26000 | campaign=BOGO Hydration Blitz, component=Post-Promo Trough, volume_units=-11000`)
- **Expected Write-Back Receipt**: `{"shape_id": "PROMO-SHAPE-4732C531", "campaign_id": "CMP-202611-BOGO", "adjusted_discount_pct": 20.0, "bundle_sku": "SKU-BEV-ELECTROLYTE-500ML", "status": "PROMO_MECHANIC_RESHAPED", "rationale": "Shift from unconstrained 25% BOGO to 20% bundle with surplus Electrolytes to eliminate DC stockout risk and reduce sister-SKU cannibalization by $26.1k.", "idempotency_key": "SHAPE-BOGO-202611-001"}`
- **Expected Markdown Report & Table**:

### 🎯 ElasticityIQ Demand Shaping & Promo Briefing

> **Executive Summary**: Evaluated Walmart Q4 *BOGO Hydration Blitz* using **BigQuery ML Double-ML** causal inference. Identified that an uncoordinated 25% discount would trigger **26,000 units of sister-SKU cannibalization** ($26,100 brand margin loss) and deplete DC Dallas stock below safety buffer (elevated stockout risk). Reshaped campaign to a **20% bundle paired with surplus Electrolyte 500ml stock**, protecting inventory and delivering **48,000 net incremental units** with **+$83,000 net profit (+22% trade spend ROI)**.

#### 📊 Promotional Lift & Cannibalization Decomposition (Atomic Copy-Ready Table)

| Campaign Name | Target SKU | Base Price | Promo Discount | Gross Lift | Cannibalization | Net Incremental | Net Margin Gain | Double-ML P-Value |
|:---|:---|---:|---:|---:|---:|---:|---:|:---|
| `BOGO Hydration Blitz` | `SKU-BEV-ISOTONIC-32OZ` | $2.99 | 20.0% (Reshaped) | 85,000 | -26,000 | **+48,000** | **+$83,000** | `p = 0.002` (Stat Sig) |
| `20% Off Protein Snack` | `SKU-SNACK-PROTEIN-BAR` | $3.49 | 20.0% | 42,000 | -8,500 | **+29,000** | **+$68,250** | `p = 0.001` (Stat Sig) |
| `Bundle & Save Electrolyte` | `SKU-BEV-ELECTROLYTE-500ML` | $3.99 | 15.0% | 31,000 | -4,200 | **+24,000** | **+$69,900** | `p = 0.004` (Stat Sig) |

#### ⚡ Trade Promotion Decisions & System Locks Executed

- **Promotional Mechanic Reshaped**: `PROMO-SHAPE-4732C531` | Campaign: `CMP-202611-BOGO` | Discount: **20.0%** | Bundle SKU: `SKU-BEV-ELECTROLYTE-500ML` | Status: `PROMO_MECHANIC_RESHAPED`
- **SAP TPM & Salesforce Calendar Locked**: `TPM-LOCK-5AF2B78C` | Net Lift: **48,000** units | Trade Spend: **$110,000.00** | Status: `TPM_CALENDAR_LOCKED_ACTIVE`

### 🔗 Connected Systems & Causal Engine
- **BigQuery ML Double-ML Causal Models**: Partially Linear Regression (PLR) estimating unconfounded price elasticity.
- **AlloyDB pgvector Multi-Echelon Stock Buffer**: Real-time checking of warehouse available-to-promise inventory.
- **SAP Trade Promotion Management (TPM)**: Automated calendar lock synchronizing retailer promotion baseline curves.
- **Salesforce Consumer Goods Cloud**: Mobile field sales execution and retail store planogram alignment.

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_planned_promo_campaigns, query_causal_promo_elasticity` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `Operational A2UI Visual Surface` (`BAR`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_shape_promotional_mechanic` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 5. JBP Negotiation Agent (`field_beat_distributor_sync_agent`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **Trade Promotion** · **Persona**: Key Account Manager (KAM) · **ROI**: `Aligns buyer margins and volume goals`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Trade Promotion, Key Account Manager (KAM) teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before JBP Negotiation Agent intervenes.
- **What This Agent Does**: Creates customized sell-in story decks and joint promotional calendars.
- **Business Result**: Aligns buyer margins and volume goals. (**Aligns buyer margins and volume goals**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for JBP Negotiation Agent.`
- **Read Tools It Must Call**: `query_distributor_dms_live_inventory, query_fso_daily_beat_store_outlets, query_pitch_to_stock_substitution_rules, query_primary_replenishment_auto_orders`
- **Write-Back Tools It Must Call**: `action_push_fso_dynamic_beat_and_pitch_list, action_trigger_distributor_primary_replenishment`
- **Demo Data Input Values It Reads**:
  - Table `distributor_dms_live_inventory.json` (2 rows): Sample input record has `distributor_id=DIST-MUM-WEST-04, sku_id=SKU-BEV-500ML, on_hand_cases=0, stock_status=STOCKED_OUT, substitute_sku_id=SKU-BEV-750ML-PROMO`
  - Table `fso_daily_beat_store_outlets.json` (1 rows): Sample input record has `fso_id=FSO-WEST-112, beat_id=BEAT-ANDHERI-NORTH, planned_outlets=38, high_propensity_outlets=28, route_time_saved_mins=54`
  - Table `pitch_to_stock_substitution_rules.json` (1 rows): Sample input record has `rule_id=SUB-BEV-01, stocked_out_sku=SKU-BEV-500ML, recommended_in_stock_sku=SKU-BEV-750ML-PROMO, cross_elasticity_retention_pct=94.2, dealer_margin_bonus_pct=2.5`
  - Table `primary_replenishment_auto_orders.json` (1 rows): Sample input record has `primary_so_id=SO-PRIM-20261022-55, distributor_id=DIST-MUM-WEST-04, sku_id=SKU-BEV-500ML, replenish_cases=600, source_cfa_depot=CFA-BHIWANDI-HUB`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `BeatSync Secondary Order Fill-Rate & FSO Productive Call Lift`
  - **Visual Mark Type**: `BAR + LINE` (3 data points: `beat_territory=West Zone (BeatSync Live), fill_rate_pct=98.4, productive_call_pct=89.5 | beat_territory=North Zone (BeatSync Live), fill_rate_pct=97.6, productive_call_pct=87.2 | beat_territory=Unsynced Static Beat, fill_rate_pct=76.5, productive_call_pct=62.0`)
- **Expected Write-Back Receipt**: `{"dispatch_execution_id": "BEAT-SYNC-9DF3E5F5", "fso_id": "FSO-WEST-112", "distributor_id": "DIST-MUM-WEST-04", "suppressed_sku_id": "SKU-BEV-500ML", "promoted_substitute_sku": "SKU-BEV-750ML-PROMO", "rationale": "Suppressed stocked-out SKU-BEV-500ML on FSO-WEST-112 mobile handheld and pushed in-stock SKU-BEV-750ML-PROMO (420 cases in DMS), preventing zero-fill secondary orders across 28 retail stores.", "status": "FSO_BEAT_AND_PITCH_SYNCED", "idempotency_key": "BEAT-SYNC-20261022-01"}`
- **Expected Markdown Report & Table**:

### ✦ BeatSync — Field Sales & Distributor Inventory Harmonizer — Executive Operations Brief

> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **05 · Deliver**.

#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)

| Dimension | Metric Value | Secondary KPI | Execution Mode |
|:---|---:|---:|:---|
| `West Zone (BeatSync Live)` | **98.4** | 89.5 | `OPTIMIZED_CVRPTW` |
| `North Zone (BeatSync Live)` | **97.6** | 87.2 | `OPTIMIZED_CVRPTW` |
| `Unsynced Static Beat` | **76.5** | 62.0 | `LEGACY_STATIC` |

#### ⚡ Autonomous Write-Backs & Actions Executed

- **Action Executed**: `BEAT-SYNC-9DF3E5F5` | Status: `FSO_BEAT_AND_PITCH_SYNCED` | Rationale: Suppressed stocked-out SKU-BEV-500ML on FSO-WEST-112 mobile handheld and pushed in-stock SKU-BEV-750ML-PROMO (420 cases in DMS), preventing zero-fill secondary orders across 28 retail stores.
- **Action Executed**: `BEAT-REPL-8B3D0ACB` | Status: `PRIMARY_REPLENISHMENT_RELEASED` | Rationale: Auto-released 600-case primary billing order from Bhiwandi CFA Depot to replenish DIST-MUM-WEST-04 within 14 hours.

### 🔗 Connected Enterprise Systems
- **Enterprise Distributor Management System (DMS) Real-Time Stock Ledger** (`REST API / Webhook`)
- **Sales Force Automation (SFA) + Google Maps Beat Route Sequencer** (`gRPC / Mobile Sync`)
- **Vertex AI Pitch-to-Stock Dynamic SKU Substitution Engine** (`Python / BigQuery ML`)
- **SAP S/4HANA SD Primary Factory-to-Distributor Auto-Replenishment** (`OData v4 / IDoc`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_distributor_dms_live_inventory, query_fso_daily_beat_store_outlets` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `BeatSync Secondary Order Fill-Rate & FSO Productive Call Lift` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_push_fso_dynamic_beat_and_pitch_list` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 6. Deduction Audit Agent (`trade_scheme_claims_reconciler`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **Trade Promotion** · **Persona**: Revenue / Trade Finance Lead · **ROI**: `Resolves claim disputes in hours`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Trade Promotion, Revenue / Trade Finance Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Deduction Audit Agent intervenes.
- **What This Agent Does**: Audits scanned proof-of-performance circulars and invoices via OCR.
- **Business Result**: Resolves claim disputes in hours. (**Resolves claim disputes in hours**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Deduction Audit Agent.`
- **Read Tools It Must Call**: `query_active_trade_promotion_schemes, query_distributor_secondary_claim_submissions, query_claim_anomaly_audit_findings, query_sap_fi_credit_note_settlements`
- **Write-Back Tools It Must Call**: `action_flag_phantom_invoice_for_audit_hold, action_post_sap_fi_trade_credit_note`
- **Demo Data Input Values It Reads**:
  - Table `active_trade_promotion_schemes.json` (1 rows): Sample input record has `scheme_id=SCH-FEST-Q4-2026, scheme_name=Q4 Festive Volume Slab & Display Rebate, min_slab_cases=50, rebate_pct=6.5, requires_shelfvision_pass=True`
  - Table `claim_anomaly_audit_findings.json` (1 rows): Sample input record has `audit_id=CLM-AUD-9921, claim_id=CLM-DIST04-9921, flagged_invoices=['INV-SEC-8812', 'INV-SEC-8819'], anomaly_type=POST_SCHEME_WINDOW_AND_DUPLICATE_GSTIN, disallowed_leakage_usd=2190.0`
  - Table `distributor_secondary_claim_submissions.json` (1 rows): Sample input record has `claim_id=CLM-DIST04-9921, distributor_id=DIST-MUM-WEST-04, scheme_id=SCH-FEST-Q4-2026, submitted_invoices_count=142, claimed_amount_usd=18450.0`
  - Table `sap_fi_credit_note_settlements.json` (1 rows): Sample input record has `credit_note_id=SAP-CN-20261022-88, claim_id=CLM-DIST04-9921, approved_amount_usd=16260.0, leakage_blocked_usd=2190.0, settlement_cycle_hours=1.8`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `SchemeGuard Trade Spend Leakage Prevention & Settlement Speed`
  - **Visual Mark Type**: `BAR + LINE` (3 data points: `claim_batch=CLM-9921 (West Zone), approved_usd=16260, leakage_blocked_usd=2190 | claim_batch=CLM-9928 (North Zone), approved_usd=22400, leakage_blocked_usd=3150 | claim_batch=Manual 5% Sample Audit, approved_usd=18450, leakage_blocked_usd=110`)
- **Expected Write-Back Receipt**: `{"dispatch_execution_id": "SCHM-HOLD-8E9D9DEB", "claim_id": "CLM-DIST04-9921", "flagged_invoices": ["INV-SEC-8812", "INV-SEC-8819"], "disallowed_amount_usd": 2190.0, "rationale": "Disallowed $2,190.00 across 2 secondary invoices (post-dated outside scheme window and duplicate outlet tax ID) on claim CLM-DIST04-9921.", "status": "ANOMALOUS_INVOICES_DISALLOWED", "idempotency_key": "SCHM-HOLD-20261022-01"}`
- **Expected Markdown Report & Table**:

### ✦ SchemeGuard — Secondary Trade Payout & Claims Sentinel — Executive Operations Brief

> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **05 · Deliver**.

#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)

| Dimension | Metric Value | Secondary KPI | Execution Mode |
|:---|---:|---:|:---|
| `CLM-9921 (West Zone)` | **16260** | 2190 | `OPTIMIZED_CVRPTW` |
| `CLM-9928 (North Zone)` | **22400** | 3150 | `OPTIMIZED_CVRPTW` |
| `Manual 5% Sample Audit` | **18450** | 110 | `LEGACY_STATIC` |

#### ⚡ Autonomous Write-Backs & Actions Executed

- **Action Executed**: `SCHM-HOLD-8E9D9DEB` | Status: `ANOMALOUS_INVOICES_DISALLOWED` | Rationale: Disallowed $2,190.00 across 2 secondary invoices (post-dated outside scheme window and duplicate outlet tax ID) on claim CLM-DIST04-9921.
- **Action Executed**: `SCHM-CN-0E1E132E` | Status: `SAP_FI_CREDIT_NOTE_POSTED` | Rationale: Posted verified SAP S/4HANA FI credit note for $16,260.00 (140 compliant secondary invoices) in 1.8 hours instead of 45 days.

### 🔗 Connected Enterprise Systems
- **Enterprise Trade Promotion Management (TPM) Circular & Slab Rule Engine** (`REST / JSON`)
- **Distributor Secondary Billing & Scheme Claim Submission Portal** (`OData / REST`)
- **BigQuery ML Anomaly & Split-Invoice Leakage Detector** (`BigQuery SQL`)
- **SAP S/4HANA FI Accounts Receivable Automated Credit Memo BAPI** (`RFC / OData v4`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_active_trade_promotion_schemes, query_distributor_secondary_claim_submissions` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `SchemeGuard Trade Spend Leakage Prevention & Settlement Speed` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_flag_phantom_invoice_for_audit_hold` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 7. Consensus & Gap Agent (`sop_scenario_weaver`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **S&OP / IBP** · **Persona**: S&OP / Supply Planning Dir. · **ROI**: `Highlights margin-dilutive imbalances`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In S&OP (Sales & Operations Planning — monthly alignment meeting) / IBP (Integrated Business Planning software), S&OP / Supply Planning Dir. teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Consensus & Gap Agent intervenes.
- **What This Agent Does**: Reconciles unconstrained demand with factory plant bottleneck limits.
- **Business Result**: Highlights margin-dilutive imbalances. (**Highlights margin-dilutive imbalances**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Consensus & Gap Agent.`
- **Read Tools It Must Call**: `query_unconstrained_demand_gaps, query_plant_line_capacities, query_supplier_allocations, query_sop_scenario_evaluations`
- **Write-Back Tools It Must Call**: `action_commit_mps_consensus_plan, action_lock_sop_financial_bridge`
- **Demo Data Input Values It Reads**:
  - Table `plant_line_capacities.json` (3 rows): Sample input record has `facility_id=PLANT-CINCINNATI-01, line_id=LINE-PKG-03, process_type=Aseptic Bottling & Retort Autoclave, standard_rate_units_per_hr=12500, current_shifts_per_week=15`
  - Table `sop_scenario_tradeoffs.json` (3 rows): Sample input record has `scenario_id=SCEN-01-UNCONSTRAINED, name=Unconstrained Sales Forecast Plan, description=Produce strictly to unconstrained commercial forecast without overtime or alternate routing., revenue_usd=68400000.0, gross_margin_usd=41200000.0`
  - Table `sop_unconstrained_demand.json` (3 rows): Sample input record has `plan_month=2026-11, business_unit=Consumer Packaged Goods, product_family=Hydration RTD, unconstrained_demand_units=4800000, constrained_supply_units=4150000`
  - Table `supplier_component_allocations.json` (2 rows): Sample input record has `supplier_id=VEND-BALL-CORP-101, supplier_name=Ball Metal Packaging, component_id=COMP-CAN-ALUM-330ML, monthly_allocation_units=5000000, committed_to_orders_units=4400000`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `Operational A2UI Visual Surface`
  - **Visual Mark Type**: `BAR / LINE` (9 data points: `scenario=1. Baseline Unconstrained, metric=Gross Margin ($M), value=41.2 | scenario=2. Overtime Max Volume, metric=Gross Margin ($M), value=44.8 | scenario=3. Synapse Balanced Pareto, metric=Gross Margin ($M), value=48.6`)
- **Expected Write-Back Receipt**: `{"mps_id": "MPS-SOP-71543ACE", "scenario_id": "SCEN-03-SYNAPSE-PARETO", "business_unit": "Consumer Packaged Goods", "committed_volume_units": 4750000, "approved_overtime_cost_usd": 220000.0, "status": "MPS_COMMITTED_TO_SAP", "rationale": "Reroute 400k units Hydration RTD to Plant Dallas with 2-shift overtime at Cincinnati to capture $72.6M revenue at 66.9% gross margin.", "idempotency_key": "MPS-202611-CPG-001"}`
- **Expected Markdown Report & Table**:

### ⚖️ Synapse Autonomous S&OP Consensus Briefing

> **Executive Summary**: Compressed monthly 21-day cross-functional S&OP consensus into a **45-minute** automated optimization run. Identified a **650,000-unit** unmet demand gap ($3.25M uncaptured revenue) on Hydration RTD constrained by packaging line 3 at Plant Cincinnati (98.4% utilization). Solved 3 alternative multi-plant scenarios in **Google OR-Tools MILP**: selected the **Pareto Optimal Frontier** rerouting 400k units to Plant Dallas plus 2 weekend shifts at Cincinnati, delivering **$48.6M gross margin (+180 bps)** and **98.7% OTIF** while reducing working capital by **$5.7M**.

#### 📊 S&OP Scenario Trade-Off Matrix (Atomic Copy-Ready Table)

| Scenario ID | Strategy Description | Revenue ($M) | Gross Margin ($M) | Margin % | OTIF % | Overtime Cost ($) | Trapped Cash ($M) | OR-Tools Solver Status |
|:---|:---|---:|---:|---:|---:|---:|---:|:---|
| `SCEN-01-UNCONSTRAINED` | Status-Quo Unconstrained Demand | $68.4M | $41.2M | 60.2% | 91.4% | $0 | $38.5M | `FEASIBLE_SUBOPTIMAL` |
| `SCEN-02-OVERTIME-MAX` | Max Overtime & Air Expedite | $72.8M | $44.8M | 61.5% | 99.2% | $850,000 | $46.2M | `FEASIBLE_EXPENSIVE` |
| `SCEN-03-SYNAPSE-PARETO` | **Synapse Balanced Pareto Plan** | **$72.6M** | **$48.6M** | **66.9%** | **98.7%** | **$220,000** | **$32.8M** | `OPTIMAL_PARETO_FRONTIER` |

#### ⚡ Enterprise S&OP Commitments Executed

- **Master Production Schedule Committed**: `MPS-SOP-71543ACE` | Business Unit: `Consumer Packaged Goods` | Volume: **4,750,000** units | Overtime: **$220,000.00** | Status: `MPS_COMMITTED_TO_SAP`
- **FP&A Financial Bridge Locked**: `FPA-BRIDGE-4845EFD1` | Target Margin: **$48,600,000.00** | Cash Ceiling: **$32,800,000.00** | Status: `FPA_FINANCIAL_LOCKED`

### 🔗 Connected Systems & Optimization Stack
- **Cloud Spanner S&OP Constraint Graph**: Real-time line rates, tooling changeovers, and Tier-1 raw material quotas.
- **Google OR-Tools Mixed-Integer Programming**: High-performance multi-objective solver computing Pareto frontier in <4 seconds.
- **SAP S/4HANA PP/DS**: Automated writeback committing production orders and planned order splits.
- **BigQuery Cortex Framework & Anaplan**: Instant financial P&L translation bridging supply choices to EBITDA.

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_unconstrained_demand_gaps, query_plant_line_capacities` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `Operational A2UI Visual Surface` (`BAR / LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_mps_consensus_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 8. Digital War-Room Agent (`disruption_war_room_orchestrator`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **S&OP / IBP** · **Persona**: Supply Chain VP / COO · **ROI**: `Rapid OTIF impact scenario brief`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In S&OP (Sales & Operations Planning — monthly alignment meeting) / IBP (Integrated Business Planning software), Supply Chain VP / COO teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Digital War-Room Agent intervenes.
- **What This Agent Does**: Evaluates co-packer shifts and allocation trade-offs during supply outages.
- **Business Result**: Rapid OTIF (On-Time In-Full — delivering 100% of ordered units before the deadline) impact scenario brief. (**Rapid OTIF impact scenario brief**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Digital War-Room Agent.`
- **Read Tools It Must Call**: `query_weather_alerts, query_maritime_ais_vessels, query_resilinc_supplier_facilities, query_news_disruptions`
- **Write-Back Tools It Must Call**: `action_create_war_room_incident, action_dispatch_expedite_remediation`
- **Demo Data Input Values It Reads**:
  - Table `incident_war_rooms.json` (1 rows): Sample input record has `incident_id=INC-WR-2026-001, title=Red Sea Bab-el-Mandeb Houthis Missile Reroute, severity=CRITICAL, created_at=2026-10-10T12:00:00Z, status=MITIGATED`
  - Table `maritime_ais_vessels.json` (2 rows): Sample input record has `vessel_imo=9811000, vessel_name=EVER GLOBE, carrier=Evergreen Line, current_lat=23.9, current_lon=120.8`
  - Table `news_disruptions.json` (2 rows): Sample input record has `signal_id=NEWS-9014, timestamp=2026-10-15T18:30:00Z, source=Reuters Global Logistics Wire, headline=Dockworker Union Strikes Paralyze Antwerp Container Terminal Operations, summary=Belgian transport unions initiate an unannounced 72-hour wildcat strike across Port of Antwerp docks, freezing customs release and crane shifts.`
  - Table `supplier_facilities.json` (2 rows): Sample input record has `supplier_id=VEND-10492, supplier_name=Taiwan Micro-Power Semiconductor Corp, tier_level=2, parent_tier1_vendor=VEND-8820 (Bosch Mobility Electronics), facility_name=Hsinchu Fab 4 Advanced Packaging`
  - Table `weather_alerts.json` (2 rows): Sample input record has `alert_id=WX-2026-0812, event_type=TYPHOON, severity=CRITICAL, region=East China Sea / Taiwan Strait, lat=24.8`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `StormShield · War Room Disruption Risk & Expedite Infographic`
  - **Visual Mark Type**: `BAR / LINE` (0 data points: `Live fixture series`)
- **Expected Write-Back Receipt**: `{"status": "created", "incident_id": "INC-WR-3850172F", "audit_trail": "War room 'Super Typhoon Gaemi & Antwerp Port Disruption Multi-Modal Response' initialized [INC-WR-3850172F] with severity CRITICAL. Lead assigned to Director of Global Supply Chain."}`
- **Expected Markdown Report & Table**:

### ⚡ Crisis Briefing: Super Typhoon Gaemi & Antwerp Port Multi-Modal Response

Correlated **3 multi-tier disruption vectors** across meteorological radars, satellite AIS telemetry, and Tier-1/2 fab statuses. **$15.4M** in pipeline inventory was at immediate risk with only **4.5 days** of buffer stock remaining at assembly plants. Autonomous War Room created and emergency freight shift dispatched.

### 📋 Disrupted Inventory & Remediation Schedule

| PO Number | Material SKU | Supplier Name | Tier | Origin / Transit | Delay (Hours) | Mitigation Action | Expedite Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `PO-450091281` | `SKU-BATTERY-MEB-01` | Taiwan Adv Packaging | Tier 2 | Kaohsiung / EVER GLOBE | +126h (5.2d) | Fast-Track Air Charter (C-17) | **DISPATCHED** |
| `PO-450091285` | `SKU-INVERTER-HV-800V` | Delta Power Systems | Tier 1 | Taichung / EVER GLOBE | +126h (5.2d) | Fast-Track Air Charter (C-17) | **DISPATCHED** |
| `PO-450091304` | `SKU-TI-FORGING-W52` | Global Wafer Fab | Tier 3 | Hsinchu / EVER GLOBE | +126h (5.2d) | Re-allocate from EU buffer | **ALLOCATED** |
| `PO-450089100` | `SKU-STERILE-VIAL-10ML` | EuroPharma Glass | Tier 1 | Antwerp / MAERSK MOLLER | +114h (4.8d) | Reroute via Rotterdam Corridor | **IN TRANSIT** |

### 🚀 Executed Autonomous Playbooks

1. **War Room Initialized**: Incident `INC-WR-3850172F` registered with cross-functional triage.
2. **Emergency Air Freight Dispatched**: Order `EXP-450091281-AIR` approved for critical EV battery modules to avoid line-down halt.

### 🔗 Connected Systems & Data Sources

* **WeatherNext 3 Numerical Radar**: Forecast bounding box `23.5°N - 25.5°N, 120.0°E - 123.0°E` (Typhoon Gaemi Sustained Winds 145 kts).
* **Spire Global Maritime AIS**: Real-time position tracking vessel `EVER GLOBE` (IMO `9811000`) anchored for weather evasion.
* **Resilinc EventWatch AI**: Tier-2 supplier facility exposure confirmed for `Taiwan Adv Packaging Fab 2`.
* **SAP S/4HANA Supply Chain Execution**: Purchasing Document `PO-450091281` flagged for expedited goods receipt.

### 🛡️ Compliance & Verification Audit

* **Pre-execution Idempotency Key**: `GAEMI-ANTWERP-20261016` (Verified)
* **CSCO Delegated Authority Limit**: Approved under $500,000 threshold ($42,000 air charter expense)
* **Audit Signature**: `sha256:7f83b2e9d41c8f4201be91456a094`


#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_weather_alerts, query_maritime_ais_vessels` against its `5` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `StormShield · War Room Disruption Risk & Expedite Infographic` (`BAR / LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_create_war_room_incident` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 9. Executive Copilot (`csco_control_tower_copilot`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **S&OP / IBP** · **Persona**: IBP Lead / Chief Planning Off. · **ROI**: `Reduces deck preparation by days`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In S&OP (Sales & Operations Planning — monthly alignment meeting) / IBP (Integrated Business Planning software), IBP Lead / Chief Planning Off. teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Executive Copilot intervenes.
- **What This Agent Does**: Generates pre-read decks and tracks sign-offs across cross-functional leads.
- **Business Result**: Reduces deck preparation by days. (**Reduces deck preparation by days**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Executive Copilot.`
- **Read Tools It Must Call**: `query_executive_kpis, query_network_bottlenecks, query_multiechelon_twin_status, query_cross_erp_order_backlog`
- **Write-Back Tools It Must Call**: `action_execute_executive_playbook, action_rebalance_network_allocation`
- **Demo Data Input Values It Reads**:
  - Table `cross_erp_order_backlog.json` (2 rows): Sample input record has `order_id=SO-8840192, order_type=CUSTOMER_SALES_ORDER, customer=Global Auto Group North America, destination_country=USA, total_value_usd=1850000`
  - Table `executive_playbooks.json` (2 rows): Sample input record has `playbook_id=PLAYBOOK-INTERMODAL-AIR-EXPEDITE, name=Suez Re-Route Critical Air Freight Bridge & Lateral DC Rebalance, target_bottleneck_type=GEOPOLITICAL_TRANSIT_REROUTE, max_authorized_budget_usd=1500000, actions=['Charter 2x Boeing 777F cargo flights from Taipei to Frankfurt for 12,000 PMIC chips', 'Trigger lateral stock transfer of 200 battery modules from Chicago Mega-Hub to Ontario DC', 'Re-sequence assembly line shifts at Stuttgart Plant to preserve high-margin EV production']`
  - Table `multiechelon_twin_status.json` (3 rows): Sample input record has `node_id=NODE-CENTRAL-US, name=Chicago Central Fulfillment Mega-Hub, echelon_level=1, capacity_utilization_pct=91.2, inventory_value_usd=68400000`
  - Table `network_bottlenecks.json` (3 rows): Sample input record has `bottleneck_id=BN-SUEZ-041, location=Red Sea / Suez Canal Maritime Chokepoint, region=EMEA, bottleneck_type=GEOPOLITICAL_TRANSIT_REROUTE, severity=CRITICAL`
  - Table `sc_kpi_summary.json` (4 rows): Sample input record has `region=GLOBAL, period=CURRENT_MONTH, otif_delivery_pct=94.2, otif_target_pct=98.0, days_inventory_outstanding_dio=58.4`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `TowerMind · CSCO Multi-Echelon Control Tower Cockpit`
  - **Visual Mark Type**: `BAR / LINE` (0 data points: `Live fixture series`)
- **Expected Write-Back Receipt**: `{"status": "executed", "execution_id": "EXEC-PB-0FA7187B", "audit_trail": "Executive Playbook 'PLAYBOOK-INTERMODAL-AIR-EXPEDITE' executed [EXEC-PB-0FA7187B] with budget $650,000.00 across 2 facilities. Rationale: Mitigate BN-SUEZ-041 (Red Sea / Suez Canal Maritime Chokepoint) preventing line down at Stuttgart.."}`
- **Expected Markdown Report & Table**:

### 🌐 Executive Briefing: Global Multi-Echelon Bottleneck & Line-Down Mitigation

Autonomous scan correlated **3 critical choke points** across EMEA and North America. Identified **$13.4M** total revenue exposure across in-flight battery assemblies and HVAC compressors. Approved playbook dispatched under CSCO delegation authority ($650,000 allocated) and lateral stock rebalancing initiated.

### 📊 Enterprise Bottleneck & Capacity Triage

| Bottleneck ID | Location / Facility | Type | Revenue at Risk ($) | Transit Delay (Days) | Remediation Playbook | Budget ($) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `BN-SUEZ-041` | Red Sea / Suez Chokepoint | Geopolitical Reroute | $7,200,000 | +14.5d | Intermodal Air Expedite | $650,000 | **DISPATCHED** |
| `BN-FRANKFURT-012` | Frankfurt Airport Cargo T2 | Air Freight Congestion | $3,800,000 | +4.2d | Direct Ramp Transfer | $120,000 | **ACTIVE** |
| `BN-DALLAS-089` | Dallas Cross-Dock Hub | Warehouse Labor Limit | $2,400,000 | +3.8d | Dynamic AMR Re-Slotting | $85,000 | **SCHEDULED** |

### 🚀 Executed Executive Actions

1. **Playbook Execution (`EXEC-PB-0FA7187B`)**: Dispatched intermodal air expedite for 8 stranded vessels avoiding line-down at Stuttgart.
2. **Lateral Inventory Rebalancing (`REBAL-BATTERY-001`)**: Transferred 200 EV battery modules from Central US Mega-Hub to European staging.

### 🔗 Connected Systems & Data Feeds

* **SAP S/4HANA Multi-Echelon Twin**: Node telemetry synchronized for 4 echelons (Raw Materials, Hubs, Forward DCs, Plants).
* **Blue Yonder TMS Transit Engine**: Cape of Good Hope transit delay calculated at +14.5 days.
* **Manhattan Associates WMS**: Dallas cross-dock outbound dock door utilization tracked at 94%.

### 🛡️ CSCO Governance & Authority Audit

* **CSCO Delegated Expenditure Gate**: $650,000 (Within authorized $2,000,000 threshold)
* **Pre-execution Idempotency**: `EXEC-SUEZ-STUTTGART-20261016` (Verified)
* **Tamper-Evident HMAC Signature**: `sha256:4a92c81e7d03...`


#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_executive_kpis, query_network_bottlenecks` against its `5` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `TowerMind · CSCO Multi-Echelon Control Tower Cockpit` (`BAR / LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_execute_executive_playbook` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 10. SKU Pruning Agent (`working_capital_cash_bridge`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **Portfolio & SKU** · **Persona**: Category Manager · **ROI**: `Unlocks tail working capital`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Portfolio & SKU (Stock Keeping Unit — a specific product code), Category Manager teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before SKU Pruning Agent intervenes.
- **What This Agent Does**: Scores velocity, plant changeover cost, and shelf revenue yield.
- **Business Result**: Unlocks tail working capital. (**Unlocks tail working capital**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for SKU Pruning Agent.`
- **Read Tools It Must Call**: `query_working_capital_metrics, query_inventory_valuation_ledger, query_trapped_cash_opportunities, query_ap_supplier_discount_invoices`
- **Write-Back Tools It Must Call**: `action_rebalance_working_capital_buffer, action_trigger_dynamic_ap_discounting`
- **Demo Data Input Values It Reads**:
  - Table `inventory_valuation_ledger.json` (3 rows): Sample input record has `valuation_area=PLANT-1010, valuation_class=3000_FINISHED_GOODS, material_id=MAT-880019, material_description=High-Voltage Power Inverter Module 800V SiC, total_stock_units=450`
  - Table `supplier_ap_invoices.json` (2 rows): Sample input record has `invoice_id=INV-AP-489012, vendor_id=VEND-10492, vendor_name=Taiwan Micro-Power Semiconductor Corp, invoice_amount_usd=940000.0, invoice_date=2026-10-10`
  - Table `trapped_cash_opportunities.json` (2 rows): Sample input record has `opportunity_id=OPP-CASH-001, valuation_area=DC-DALLAS-CENTRAL, material_id=MAT-HVAC-901, category=SLOW_MOVING_BUFFER_REDUCTION, priority_rank=1`
  - Table `working_capital_metrics.json` (3 rows): Sample input record has `business_unit=GLOBAL_ENTERPRISE, region=GLOBAL, cash_conversion_cycle_days=72.4, target_ccc_days=54.0, days_inventory_outstanding_dio=58.4`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `MarginBridge · Working Capital & CCC Financial Infographic`
  - **Visual Mark Type**: `BAR / LINE` (0 data points: `Live fixture series`)
- **Expected Write-Back Receipt**: `{"status": "rebalanced", "rebal_id": "REBAL-WC-947FD6AD", "audit_trail": "Working capital rightsized [REBAL-WC-947FD6AD]: MAT-HVAC-901 at DC-DALLAS-CENTRAL reduced by 343 units, releasing $1,646,400.00 to treasury cash flow. Rationale: Rightsize buffer for MAT-HVAC-901 releasing $1,646,400.00 with negligible SLA risk.."}`
- **Expected Markdown Report & Table**:

### 💰 Financial Executive Briefing: Working Capital & CCC Cash Optimization

Autonomous audit scanned **ACDOCA General Ledger** and supplier accounts payable schedules across global operations. Identified **$85.2M** in trapped working capital across excess safety stocks. Executed rightsizing on slow-moving inventory buffers (compressing DIO from 58.4 to 45.0 days) and captured dynamic 2/10 Net 60 early-pay discounts yielding **36.5% risk-free annualized ROI**.

### 📋 Trapped Working Capital & Discount Optimization Schedule

| Plant / Valuation Area | Material SKU | Category | Current Stock Value ($) | Units Reduced | Cash Unlocked ($) | Working Capital Impact | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `PLANT-1010` | `SKU-BATTERY-MODULE-800V` | High-Tech Modules | $14,200,000 | 450 units | **$3,825,000** | DIO -4.2 Days | **BUFFER RIGHTSIZED** |
| `PLANT-1020` | `SKU-INVERTER-HV-800V` | Power Electronics | $9,800,000 | 320 units | **$2,450,000** | DIO -2.8 Days | **BUFFER RIGHTSIZED** |
| `VENDOR-V9021` | Invoice `INV-990214-A` | 2/10 Net 60 AP Early Pay | $1,250,000 | N/A | **$25,000** | APR 36.5% Yield | **DISCOUNT CAPTURED** |
| `VENDOR-V8812` | Invoice `INV-881203-B` | 1.5/15 Net 45 AP Early Pay | $850,000 | N/A | **$12,750** | APR 18.2% Yield | **DISCOUNT CAPTURED** |

### 🚀 Executed Financial Actions

1. **Inventory Buffer Rightsizing (`REBAL-BUF-001`)**: Safely trimmed slow-moving safety buffers at PLANT-1010, unlocking $3.82M in liquid cash flow.
2. **Dynamic Early Pay Settlement (`DISC-AP-001`)**: Dispatched early settlement instructions for high-APR supplier discounts, capturing $37,750 in direct bottom-line cash.

### 🔗 Connected Financial Systems & Ledgers

* **SAP S/4HANA Finance**: Universal Journal (`ACDOCA`) and Material Ledger inventory valuation.
* **Taulia / Kyriba Working Capital Platform**: Dynamic AP supplier discount matching engine.
* **Treasury Cash Flow Liquidity Engine**: Real-time overnight yield vs cost of capital spread.

### 🛡️ Treasury Policy & Governance Audit

* **Minimum Liquidity Covenant Check**: Passed ($250M covenant floor preserved).
* **Cost of Capital Hurdle Rate**: 8.5% WACC exceeded by 2800 bps.
* **Pre-execution Idempotency**: Verified.


#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_working_capital_metrics, query_inventory_valuation_ledger` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `MarginBridge · Working Capital & CCC Financial Infographic` (`BAR / LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_rebalance_working_capital_buffer` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 11. PIPO Run-Out Agent (`eco_cutover_orchestrator`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **Portfolio & SKU** · **Persona**: Lifecycle / Materials Mgr · **ROI**: `Eliminates stranded write-offs`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Portfolio & SKU (Stock Keeping Unit — a specific product code), Lifecycle / Materials Mgr teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before PIPO Run-Out Agent intervenes.
- **What This Agent Does**: Orchestrates transition buffers to sync packaging and formulation cuts.
- **Business Result**: Eliminates stranded write-offs. (**Eliminates stranded write-offs**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for PIPO Run-Out Agent.`
- **Read Tools It Must Call**: `query_plm_engineering_change_orders, query_multi_plant_predecessor_inventory_runout, query_eco_optimal_cutover_schedules, query_erp_bom_effectivity_sync_audit`
- **Write-Back Tools It Must Call**: `action_lock_multi_plant_eco_effectivity_dates, action_modify_open_supplier_po_revision`
- **Demo Data Input Values It Reads**:
  - Table `eco_optimal_cutover_schedules.json` (1 rows): Sample input record has `schedule_id=CUT-ECO-8841, eco_id=ECO-2026-8841, optimal_effectivity_date=2026-11-11, supplier_po_converted_to_rev_c=2800, obsolete_scrap_writeoff_usd=8400.0`
  - Table `erp_bom_effectivity_sync_audit.json` (1 rows): Sample input record has `sync_id=SYNC-SAP-8841, eco_id=ECO-2026-8841, open_po_id=PO-ARIBA-55910, sap_bom_status=EFFECTIVITY_ALIGNED_TO_RUNOUT, npi_launch_on_time=True`
  - Table `multi_plant_predecessor_inventory_runout.json` (2 rows): Sample input record has `eco_id=ECO-2026-8841, plant_id=PLANT-AUSTIN-01, predecessor_on_hand_units=4200, open_supplier_po_units=2800, daily_burn_rate_units=350`
  - Table `plm_engineering_change_orders.json` (1 rows): Sample input record has `eco_id=ECO-2026-8841, assembly_sku=ASM-INVERTER-GEN4, predecessor_part=PCB-DRV-REV-B, successor_part=PCB-DRV-REV-C, change_class=COST_AND_EFFICIENCY_UPGRADE`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `ChangeSync Multi-Plant ECO Runout & E&O Write-Off Prevention`
  - **Visual Mark Type**: `BAR + LINE` (3 data points: `cutover_mode=ChangeSync Dynamic Runout, scrap_writeoff_usd=8400, exhaustion_pct=98.1 | cutover_mode=Blind Immediate Cutover, scrap_writeoff_usd=436500, exhaustion_pct=12.0 | cutover_mode=Manual Spreadsheet Guess, scrap_writeoff_usd=194000, exhaustion_pct=55.5`)
- **Expected Write-Back Receipt**: `{"dispatch_execution_id": "ECO-LOCK-C456B4EC", "eco_id": "ECO-2026-8841", "optimal_effectivity_date": "2026-11-11", "scrap_avoided_usd": 428100.0, "rationale": "Aligned Austin and Guadalajara SAP BOM effectivity to 2026-11-11 to exhaust 6,000 on-hand Rev-B boards prior to Rev-C cutover, avoiding $428,100 in obsolete E&O write-offs.", "status": "BOM_EFFECTIVITY_LOCKED", "idempotency_key": "ECO-LOCK-20261022-01"}`
- **Expected Markdown Report & Table**:

### ✦ ChangeSync — Engineering Change (ECO) & NPI Cutover Orchestrator — Executive Operations Brief

> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **03 · Make**.

#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)

| Dimension | Metric Value | Secondary KPI | Execution Mode |
|:---|---:|---:|:---|
| `ChangeSync Dynamic Runout` | **8400** | 98.1 | `OPTIMIZED_CVRPTW` |
| `Blind Immediate Cutover` | **436500** | 12.0 | `LEGACY_STATIC` |
| `Manual Spreadsheet Guess` | **194000** | 55.5 | `LEGACY_STATIC` |

#### ⚡ Autonomous Write-Backs & Actions Executed

- **Action Executed**: `ECO-LOCK-C456B4EC` | Status: `BOM_EFFECTIVITY_LOCKED` | Rationale: Aligned Austin and Guadalajara SAP BOM effectivity to 2026-11-11 to exhaust 6,000 on-hand Rev-B boards prior to Rev-C cutover, avoiding $428,100 in obsolete E&O write-offs.
- **Action Executed**: `ECO-PO-4C873ACF` | Status: `SUPPLIER_PO_REVISION_UPDATED` | Rationale: Converted 2,800 unshipped units on open supplier PO-ARIBA-55910 from Rev-B to Rev-C prior to supplier SMT production freeze.

### 🔗 Connected Enterprise Systems
- **Siemens Teamcenter / PTC Windchill PLM Engineering Change (ECO) Feed** (`REST / Webhook`)
- **SAP S/4HANA MM/PP Multi-Plant WIP & Open Supplier PO Runout Ledger** (`OData v4 / BAPI`)
- **Google OR-Tools Dynamic BOM Phase-In / Phase-Out Cutover Solver** (`Python MILP SDK`)
- **SAP Ariba Open Supplier Purchase Order Revision Cutover Engine** (`cXML / REST`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_plm_engineering_change_orders, query_multi_plant_predecessor_inventory_runout` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `ChangeSync Multi-Plant ECO Runout & E&O Write-Off Prevention` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_lock_multi_plant_eco_effectivity_dates` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 12. Cost-to-Serve Diagnostic (`network_twin_architect`)
- **Pillar / Sub-Pillar**: 01 · Planning & Strategy — **Portfolio & SKU** · **Persona**: Commercial Finance Director · **ROI**: `Re-engineers MOQ and pack rules`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Portfolio & SKU (Stock Keeping Unit — a specific product code), Commercial Finance Director teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Cost-to-Serve Diagnostic intervenes.
- **What This Agent Does**: Calculates net-net margin across Club, Grocery, and eCommerce packs.
- **Business Result**: Re-engineers MOQ and pack rules. (**Re-engineers MOQ and pack rules**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Cost-to-Serve Diagnostic.`
- **Read Tools It Must Call**: `query_network_facility_nodes_and_leases, query_sku_customer_cost_to_serve_matrix, query_center_of_gravity_milp_scenarios, query_network_stress_test_simulations`
- **Write-Back Tools It Must Call**: `action_publish_network_territory_realignment, action_update_cost_to_serve_order_policy`
- **Demo Data Input Values It Reads**:
  - Table `center_of_gravity_milp_scenarios.json` (1 rows): Sample input record has `scenario_id=SCEN-COG-SE-2026, scenario_name=Southeast 3PL Node Addition & Territory Realignment, stem_miles_reduction_pct=14.6, annual_net_savings_usd=6840000.0, 1_day_ground_coverage_pct=91.2`
  - Table `network_facility_nodes_and_leases.json` (2 rows): Sample input record has `facility_id=RDC-COLUMBUS-OH, facility_type=REGIONAL_DC, annual_lease_usd=4200000.0, capacity_pallets_yr=480000, handling_cost_per_pallet_usd=14.2`
  - Table `network_stress_test_simulations.json` (1 rows): Sample input record has `stress_test_id=STRESS-TARIFF-60PCT, shock_event=60% Section 301 Tariff + East Coast Port Congestion, recommended_shift=Nearshore Monterrey MX + Savannah/Houston Split, duty_and_freight_saved_usd=11200000.0`
  - Table `sku_customer_cost_to_serve_matrix.json` (1 rows): Sample input record has `customer_segment_id=SEG-SOUTHEAST-L2, avg_order_pallets=1.5, each_pick_cost_usd=184.0, stem_miles_from_ohio=685, net_operating_margin_pct=-3.8`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `TwinDesign Network Center-of-Gravity & Cost-to-Serve Optimization`
  - **Visual Mark Type**: `BAR + LINE` (3 data points: `network_topology=Optimized + Savannah Hub, annual_cost_m_usd=67.4, one_day_sla_pct=91.2 | network_topology=Nearshore Tariff Resilient, annual_cost_m_usd=69.1, one_day_sla_pct=89.8 | network_topology=Legacy 3-RDC Baseline, annual_cost_m_usd=74.2, one_day_sla_pct=76.4`)
- **Expected Write-Back Receipt**: `{"dispatch_execution_id": "TWIN-NET-382C036A", "scenario_id": "SCEN-COG-SE-2026", "new_hub_id": "3PL-SAVANNAH-EXP", "annual_savings_usd": 6840000.0, "rationale": "OR-Tools Center-of-Gravity MILP reassigned 142 Southeast zip-3 territories from Columbus OH to Savannah 3PL hub, cutting stem miles by 14.6% and saving $6.84M/yr.", "status": "NETWORK_TERRITORY_REALIGNED", "idempotency_key": "TWIN-NET-20261022-01"}`
- **Expected Markdown Report & Table**:

### ✦ TwinDesign — Supply Chain Network & Cost-to-Serve Optimizer — Executive Operations Brief

> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **04 · Fulfill**.

#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)

| Dimension | Metric Value | Secondary KPI | Execution Mode |
|:---|---:|---:|:---|
| `Optimized + Savannah Hub` | **67.4** | 91.2 | `OPTIMIZED_CVRPTW` |
| `Nearshore Tariff Resilient` | **69.1** | 89.8 | `OPTIMIZED_CVRPTW` |
| `Legacy 3-RDC Baseline` | **74.2** | 76.4 | `LEGACY_STATIC` |

#### ⚡ Autonomous Write-Backs & Actions Executed

- **Action Executed**: `TWIN-NET-382C036A` | Status: `NETWORK_TERRITORY_REALIGNED` | Rationale: OR-Tools Center-of-Gravity MILP reassigned 142 Southeast zip-3 territories from Columbus OH to Savannah 3PL hub, cutting stem miles by 14.6% and saving $6.84M/yr.
- **Action Executed**: `TWIN-CTS-99B4FDFB` | Status: `COST_TO_SERVE_POLICY_UPDATED` | Rationale: Activity-based Cost-to-Serve identified -3.8% margin erosion from broken-case LTL orders; enforced 4-pallet layer MOQ and weekly consolidated delivery, restoring +8.4% net margin.

### 🔗 Connected Enterprise Systems
- **Google OR-Tools Capacitated Facility Location & Territory MILP** (`C++ / Python MILP`)
- **BigQuery Activity-Based Cost-to-Serve (CTS) & Margin Waterfall Engine** (`BigQuery SQL`)
- **Macro Tariff & Port Disruption Network Stress-Test Simulator** (`Python Monte Carlo + MILP`)
- **SAP IBP & S/4HANA Sourcing Rules & Customer Territory Master** (`OData v4`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_network_facility_nodes_and_leases, query_sku_customer_cost_to_serve_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `TwinDesign Network Center-of-Gravity & Cost-to-Serve Optimization` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_publish_network_territory_realignment` without `idempotency_key` triggers `missing_idempotency_key`.

---

## 02 · Sourcing & Procurement (9 Agents)

### 13. Disruption Sensing Agent (`tier_n_risk_sentinel`)
- **Pillar / Sub-Pillar**: 02 · Sourcing & Procurement — **Supplier Network** · **Persona**: Procurement Dir. / Risk Mgr · **ROI**: `2–3 week advance disruption warning`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Supplier Network, Procurement Dir. / Risk Mgr teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Disruption Sensing Agent intervenes.
- **What This Agent Does**: Monitors multi-tier supply feeds, port delays, and vendor financials.
- **Business Result**: 2–3 week advance disruption warning. (**2–3 week advance disruption warning**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Disruption Sensing Agent.`
- **Read Tools It Must Call**: `query_subtier_network_nodes, query_active_disruption_threats, query_bom_revenue_lineage, query_mitigation_playbook_options`
- **Write-Back Tools It Must Call**: `action_dispatch_dual_source_po_split, action_surge_meio_safety_buffer`
- **Demo Data Input Values It Reads**:
  - Table `active_disruption_threats.json` (2 rows): Sample input record has `threat_id=THREAT-CYCLONE-QLD-01, threat_type=CATEGORY_4_TROPICAL_CYCLONE, region=Queensland, Australia, impacted_node_id=NODE-WEIPA-BAUXITE-AU, supplier_name=Weipa Bauxite Mining & Refinery`
  - Table `bom_finished_good_lineage.json` (2 rows): Sample input record has `impacted_subtier_node=NODE-WEIPA-BAUXITE-AU, component_id=ORE-BAUXITE-METALLURGICAL, tier_depth=4, finished_goods_impacted=[{'sku_id': 'SKU-BEV-ISOTONIC-32OZ', 'product_name': 'Hydration RTD 32oz Can', 'monthly_volume_units': 4500000, 'revenue_at_risk_usd': 13455000.0}, {'sku_id': 'SKU-BEV-ELECTROLYTE-500ML', 'product_name': 'Electrolyte Recovery 500ml', 'monthly_volume_units': 1200000, 'revenue_at_risk_usd': 4788000.0}], total_revenue_at_risk_usd=18243000.0`
  - Table `mitigation_playbook_options.json` (2 rows): Sample input record has `playbook_id=PB-DUAL-SOURCE-ALUM, threat_id=THREAT-CYCLONE-QLD-01, impacted_component=RAW-ALUM-INGOT-P1020A, primary_supplier_impacted=Alcoa International Smelter (IS), backup_qualified_supplier=Hydro Aluminium (NO)`
  - Table `subtier_supplier_network.json` (4 rows): Sample input record has `node_id=NODE-BALL-US-01, supplier_name=Ball Metal Packaging, tier_level=1, component_provided=COMP-CAN-ALUM-330ML, facility_country=US`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `Operational A2UI Visual Surface`
  - **Visual Mark Type**: `CIRCLE` (8 data points: `tier=Tier-1 Assembly, node_id=Ball Metal Packaging, country=US | tier=Tier-1 Assembly, node_id=Crown Holdings, country=US | tier=Tier-2 Smelting, node_id=Alcoa Int. Smelter, country=IS`)
- **Expected Write-Back Receipt**: `{"po_split_id": "PO-SPLIT-A3723A37", "playbook_id": "PB-DUAL-SOURCE-ALUM", "backup_supplier": "Hydro Aluminium (NO)", "reallocation_split_pct": 50.0, "target_po_reallocation_units": 4500000, "status": "SAP_PO_SPLIT_DISPATCHED", "rationale": "Reallocate 50% ingot demand to backup qualified Norwegian smelter to bypass Australian cyclone disruption.", "idempotency_key": "SPLIT-ALUM-202610-001"}`
- **Expected Markdown Report & Table**:

### 🛡️ NexusShield Multi-Tier Supply Network Risk Briefing

> **Executive Summary**: Detected a **Category 4 Tropical Cyclone (11-day advance warning)** threatening the *Weipa Bauxite Mining & Refinery* in Queensland, Australia via **Google DeepMind WeatherNext 3**. Queried the multi-tier enterprise knowledge graph in **Cloud Spanner Graph** to traverse 4 supply chain echelons (Tier-4 Bauxite Mine &rarr; Tier-2 Smelter in Iceland &rarr; Tier-1 Can Plant in Colorado &rarr; Finished RTD Beverage). Traced **$18,243,000 revenue at risk** across 2 high-volume SKUs with only 16.5 days of line-side buffer remaining. Autonomously reallocated **50% of PO ingot volume (4.5M units) to Hydro Aluminium in Norway** and **surged regional MEIO safety buffers by +7.0 days**, preventing factory line-down with zero customer stockouts.

#### 📊 Multi-Tier Sub-Supplier Disruption Ledger (Atomic Copy-Ready Table)

| Tier Depth | Impacted Supplier Node | Country | Threat Trigger | Finished SKU Lineage | Revenue at Risk | Current Buffer | Advance Warning | Mitigation Action |
|:---|:---|:---|:---|:---|---:|---:|---:|:---|
| `Tier-4 Mine` | `Weipa Bauxite Refinery` | Australia | Category 4 Cyclone | `SKU-BEV-ISOTONIC-32OZ` | $13,455,000 | 16.5 Days | **+11 Days** | Dual-Source PO Split to Norway |
| `Tier-4 Mine` | `Weipa Bauxite Refinery` | Australia | Category 4 Cyclone | `SKU-BEV-ELECTROLYTE-500ML` | $4,788,000 | 16.5 Days | **+11 Days** | +7.0 Days MEIO Buffer Surge |
| `Tier-3 Chem` | `Showa Denko Chemical` | Japan | Seismic Precaution | `SKU-BEV-ELECTROLYTE-500ML` | $4,788,000 | 24.0 Days | +4 Days | Monitored / Stable |

#### ⚡ Autonomous Risk Mitigations Executed

- **SAP S/4HANA PO Split Reallocated**: `PO-SPLIT-A3723A37` | Backup Supplier: **Hydro Aluminium (NO)** | Reallocation Split: **50.0%** | Units: **4,500,000** | Status: `SAP_PO_SPLIT_DISPATCHED`
- **MEIO Safety Stock Buffer Surged**: `SURGE-MEIO-658CBA08` | Impacted SKUs: `SKU-BEV-ISOTONIC-32OZ, SKU-BEV-ELECTROLYTE-500ML` | Days Increase: **+7.0 Days** | Status: `MEIO_BUFFER_SURGE_COMMITTED`

### 🔗 Connected Systems & Graph Architecture
- **Cloud Spanner Multi-Tier Knowledge Graph**: Sub-tier vendor relationships inferred from customs Bill of Lading (BOL) and supplier declarations.
- **Google DeepMind WeatherNext 3**: Real-time atmospheric cyclone tracking with 11-day advance predictive trajectory.
- **SAP S/4HANA Strategic Sourcing**: BAPI_PO_CREATE1 writeback executing secondary supplier purchase order splits.
- **Multi-Echelon Inventory Optimization (MEIO)**: Dynamic safety stock recalibration protecting finished goods OTIF.

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_subtier_network_nodes, query_active_disruption_threats` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `Operational A2UI Visual Surface` (`CIRCLE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_dispatch_dual_source_po_split` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 14. Onboarding & Qual. Agent (`supplier_quality_sentinel`)
- **Pillar / Sub-Pillar**: 02 · Sourcing & Procurement — **Supplier Network** · **Persona**: Procurement Operations Lead · **ROI**: `Cuts onboarding from weeks to <48h`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Supplier Network, Procurement Operations Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Onboarding & Qual. Agent intervenes.
- **What This Agent Does**: Parses BRC/ISO audits, food-safety filings, and tax registrations.
- **Business Result**: Cuts onboarding from weeks to <48h. (**Cuts onboarding from weeks to <48h**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Onboarding & Qual. Agent.`
- **Read Tools It Must Call**: `query_supplier_coa_inspections, query_spc_cpk_drift_metrics, query_quality_deviation_tickets, query_cost_of_poor_quality_ledger`
- **Write-Back Tools It Must Call**: `action_quarantine_inspection_lot, action_trigger_8d_capa_debit`
- **Demo Data Input Values It Reads**:
  - Table `cost_of_poor_quality_ledger.json` (2 rows): Sample input record has `copq_id=COPQ-202610-8841, ticket_id=NCR-202610-0914, supplier_id=VEND-KYOCERA-PREC-09, supplier_name=Kyocera Precision Ceramics, scrap_material_cost_usd=68750.0`
  - Table `quality_deviation_tickets.json` (2 rows): Sample input record has `ticket_id=NCR-202610-0914, inspection_lot_id=LOT-INSP-202610-8841, supplier_id=VEND-KYOCERA-PREC-09, supplier_name=Kyocera Precision Ceramics, part_number=PART-SUBSTRATE-ALN-01`
  - Table `spc_cpk_drift_metrics.json` (2 rows): Sample input record has `metric_id=SPC-KY-ALN-2026W41, supplier_id=VEND-KYOCERA-PREC-09, part_number=PART-SUBSTRATE-ALN-01, production_line=LINE-SINTERING-04, sample_timestamp=2026-10-18T14:30:00Z`
  - Table `supplier_coa_inspections.json` (2 rows): Sample input record has `inspection_lot_id=LOT-INSP-202610-8841, po_number=PO-4500918231, supplier_id=VEND-KYOCERA-PREC-09, supplier_name=Kyocera Precision Ceramics, part_number=PART-SUBSTRATE-ALN-01`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `QualiShield SPC Process Capability Drift (Kyocera AlN Substrates)`
  - **Visual Mark Type**: `LINE + RULE` (7 data points: `lot_sample=Lot 8835, measurement=181.2, status=CONFORMING | lot_sample=Lot 8836, measurement=179.8, status=CONFORMING | lot_sample=Lot 8837, measurement=178.5, status=CONFORMING`)
- **Expected Write-Back Receipt**: `{"quarantine_id": "QM-BLOCK-FF8C397B", "inspection_lot_id": "LOT-INSP-202610-8841", "supplier_id": "VEND-KYOCERA-PREC-09", "part_number": "PART-SUBSTRATE-ALN-01", "plant_id": "PLANT-1020-AUSTIN", "status": "SAP_QM_QUARANTINED_BLOCKED", "quarantine_reason": "Thermal conductivity 164.2 W/m·K is below LSL (170.0 W/m·K); Cpk collapsed to 0.54 with 52,600 PPM defect risk.", "idempotency_key": "QUARANTINE-KY-202610-001"}`
- **Expected Markdown Report & Table**:

### 🛡️ QualiShield Predictive Supplier Quality & Non-Conformance Resolution Briefing

> **Executive Summary**: Intercepted incoming Lot `LOT-INSP-202610-8841` (25,000 units of AlN Substrates from Kyocera Precision Ceramics) at Plant Austin. Telemetry and Certificate of Analysis (CoA) testing revealed a **critical thermal conductivity deficiency of 164.2 W/m·K** (violating the Lower Specification Limit of 170.0 W/m·K), driving process capability **Cpk down to 0.54** (unstable; 52,600 PPM defect risk). Executed an instantaneous **digital quarantine block in SAP QM** to protect surface-mount assembly lines, dispatched an **8D CAPA investigation** via TrackWise, and posted an automated **$114,650.00 COPQ debit memo in SAP FI** to recover scrap, sorting labor, and line downtime costs.

#### 📊 Supplier Lot Inspection & Process Capability Ledger (Atomic Copy-Ready Table)

| Inspection Lot | Supplier | Part Number | Measured Val | Spec Limits (LSL / USL) | Cpk Status | Defect PPM | Disposition | Quarantine Action | COPQ Debit |
|:---|:---|:---|:---|:---|:---|---:|:---|:---|---:|
| `LOT-INSP-202610-8841` | Kyocera Precision | `PART-SUBSTRATE-ALN-01` | 164.2 W/m·K | 170.0 / 190.0 | **0.54 (CRITICAL)** | 52,600 PPM | `REJECT_OUT_OF_SPEC` | **SAP QM QUARANTINED** | **$114,650.00** |
| `LOT-INSP-202610-8842` | Murata Mfg | `PART-MLCC-0402-10UF` | 10.02 µF | 9.00 / 11.00 | **1.81 (CAPABLE)** | 0.3 PPM | `ACCEPTED_CONFORMING` | Released to Line | $0.00 |

#### ⚡ Immediate Mitigation & Containment Executed

- **SAP QM Digital Quarantine Block Activated**: `QM-BLOCK-FF8C397B` | Lot: `LOT-INSP-202610-8841` | Plant: `PLANT-1020-AUSTIN` | Status: `SAP_QM_QUARANTINED_BLOCKED`
- **SAP FI Cost of Poor Quality Debit Posted**: `COPQ-DEBIT-2BF72CCD` | NCR Ticket: `NCR-202610-0914` | Debit Amount: **$114,650.00** | Cost Center: `CC-MFG-AUSTIN-SMT-40` | Status: `SAP_FI_COPQ_DEBIT_POSTED`

### 🔗 Connected Systems & Quality Architecture
- **SAP S/4HANA Quality Management (QM)**: Usage decision locks, goods receipt block, and warehouse transfer order cancellation.
- **Supplier MES Telemetry Lake**: High-frequency shopfloor sensor ingestion and real-time Cpk/SPC statistical drift alerting.
- **TrackWise / ETQ Reliance**: D1–D8 root cause analysis workflow, Ishikawa diagram, and 5-Why corrective containment.
- **SAP S/4HANA Finance (FI/CO)**: Itemized scrap, sorting labor, and machine idle chargeback ledger via automated EDI 812.

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_supplier_coa_inspections, query_spc_cpk_drift_metrics` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `QualiShield SPC Process Capability Drift (Kyocera AlN Substrates)` (`LINE + RULE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_quarantine_inspection_lot` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 15. ESG & Scope 3 Auditor (`carbon_scope3_ledger`)
- **Pillar / Sub-Pillar**: 02 · Sourcing & Procurement — **Supplier Network** · **Persona**: Chief Sustainability Officer · **ROI**: `Automates Scope 3 disclosure audits`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Supplier Network, Chief Sustainability Officer teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before ESG & Scope 3 Auditor intervenes.
- **What This Agent Does**: Standardizes chain-of-custody certificates (RSPO/FSC) and packaging LCAs.
- **Business Result**: Automates Scope 3 disclosure audits. (**Automates Scope 3 disclosure audits**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for ESG & Scope 3 Auditor.`
- **Read Tools It Must Call**: `query_shipment_level_scope3_emissions, query_eu_cbam_embedded_carbon_declarations, query_eudr_earth_engine_plot_verifications, query_low_carbon_carrier_and_supplier_swaps`
- **Write-Back Tools It Must Call**: `action_certify_cbam_and_eudr_compliance_dossier, action_commit_scope3_decarbonization_swap`
- **Demo Data Input Values It Reads**:
  - Table `eu_cbam_embedded_carbon_declarations.json` (1 rows): Sample input record has `import_declaration_id=CBAM-EU-2026-Q4-09, cn_code=7606_12_92_ALUMINUM_SHEET, supplier_smelter=NORSK_HYDRO_RENEWABLE_EAF, imported_tonnes=120.0, primary_specific_emissions_tco2e_per_t=2.1`
  - Table `eudr_earth_engine_plot_verifications.json` (1 rows): Sample input record has `plot_id=PLOT-BR-PARA-4410, commodity=NATURAL_RUBBER_AND_PULP, geojson_centroid=-3.1190,-60.0217, sentinel2_ndvi_change_post2020=0.0, deforestation_free_verified=True`
  - Table `low_carbon_carrier_and_supplier_swaps.json` (1 rows): Sample input record has `swap_id=SWAP-DEC-2026-04, target_corridor_or_bom=DE_NL_RHINE_CORRIDOR, recommended_partner=HVO100_BIOFUEL_AND_ELECTRIC_BARGE, annual_tco2e_reduction=1420.0, net_cost_delta_pct=-1.2`
  - Table `shipment_level_scope3_emissions.json` (1 rows): Sample input record has `shipment_id=SHP-GLB-20261022-301, corridor=Rotterdam➔Duisburg, mode=ELECTRIC_BARGE_AND_EV_TRUCK, payload_tonnes=42.0, distance_km=215.0`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `EcoChain Scope-3 Carbon Intensity & EU CBAM Tax Shield`
  - **Visual Mark Type**: `BAR + LINE` (3 data points: `compliance_scope=Hydro EAF Aluminum (Primary), emissions_tco2e=252, cbam_eur_saved=64260 | compliance_scope=EU Default Penalty Factor, emissions_tco2e=1008, cbam_eur_saved=0 | compliance_scope=Rhine HVO100 + Barge Swap, emissions_tco2e=410, cbam_eur_saved=28400`)
- **Expected Write-Back Receipt**: `{"dispatch_execution_id": "ESG-CERT-56ED48C7", "import_declaration_id": "CBAM-EU-2026-Q4-09", "plot_id": "PLOT-BR-PARA-4410", "cbam_tax_avoided_eur": 64260.0, "rationale": "Certified primary smelter emissions (2.1 tCO2e/t vs 8.4 EU default penalty, saving €64,260 in CBAM certificates) and verified zero post-2020 deforestation on PLOT-BR-PARA-4410 via Google Earth Engine.", "status": "CBAM_AND_EUDR_DOSSIER_CERTIFIED", "idempotency_key": "ESG-CERT-20261022-01"}`
- **Expected Markdown Report & Table**:

### ✦ EcoChain — Shipment-Level Scope-3 Carbon, CBAM & EUDR Ledger — Executive Operations Brief

> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **06 · Return & Enable**.

#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)

| Dimension | Metric Value | Secondary KPI | Execution Mode |
|:---|---:|---:|:---|
| `Hydro EAF Aluminum (Primary)` | **252** | 64260 | `OPTIMIZED_CVRPTW` |
| `EU Default Penalty Factor` | **1008** | 0 | `LEGACY_STATIC` |
| `Rhine HVO100 + Barge Swap` | **410** | 28400 | `OPTIMIZED_CVRPTW` |

#### ⚡ Autonomous Write-Backs & Actions Executed

- **Action Executed**: `ESG-CERT-56ED48C7` | Status: `CBAM_AND_EUDR_DOSSIER_CERTIFIED` | Rationale: Certified primary smelter emissions (2.1 tCO2e/t vs 8.4 EU default penalty, saving €64,260 in CBAM certificates) and verified zero post-2020 deforestation on PLOT-BR-PARA-4410 via Google Earth Engine.
- **Action Executed**: `ESG-SWAP-FA6F7930` | Status: `LOW_CARBON_LANE_SWAP_COMMITTED` | Rationale: Shifted Rhine corridor volume to HVO100 renewable diesel and electric barge, cutting annual Scope-3 emissions by 1,420 tCO2e at -1.2% lower freight cost.

### 🔗 Connected Enterprise Systems
- **ISO 14083 & GLEC Framework v3.0 Primary Telemetry Carbon Ledger** (`BigQuery SQL / Python`)
- **EU Carbon Border Adjustment Mechanism (CBAM) Embedded Carbon Engine** (`XML / REST API`)
- **Google Earth Engine Satellite Polygon Deforestation Verifier (EUDR)** (`Earth Engine Python API`)
- **OR-Tools Low-Carbon Carrier & Smelter Swap Optimizer** (`Python MILP`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_shipment_level_scope3_emissions, query_eu_cbam_embedded_carbon_declarations` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `EcoChain Scope-3 Carbon Intensity & EU CBAM Tax Shield` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_certify_cbam_and_eudr_compliance_dossier` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 16. Commodity Index Advisor (`commodity_index_advisor`)
- **Pillar / Sub-Pillar**: 02 · Sourcing & Procurement — **Material & Packaging** · **Persona**: Category Sourcing Mgr (Direct) · **ROI**: `Optimizes forward-contract windows`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Material & Packaging, Category Sourcing Mgr (Direct) teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Commodity Index Advisor intervenes.
- **What This Agent Does**: Correlates CBOT/Platts feedstocks with depletion to advise hedging.
- **Business Result**: Optimizes forward-contract windows. (**Optimizes forward-contract windows**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Commodity Index Advisor.`
- **Read Tools It Must Call**: `query_commodity_index_advisor_telemetry_feed, query_commodity_index_advisor_constraint_matrix, query_commodity_index_advisor_optimization_scenarios, query_commodity_index_advisor_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_commodity_index_advisor_plan, action_dispatch_commodity_index_advisor_alert`
- **Demo Data Input Values It Reads**:
  - Table `commodity_index_advisor_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=COMMOD-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Material & Packaging, capacity_limit=12500`
  - Table `commodity_index_advisor_execution_ledger.json` (3 rows): Sample input record has `execution_id=COMMOD-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Category Sourcing Mgr (Direct), erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `commodity_index_advisor_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=02 · Source | Material & Packaging, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `commodity_index_advisor_telemetry_feed.json` (4 rows): Sample input record has `record_id=COMMOD-TEL-101, company_id=XYZ-CORP-01, category=02 · Sourcing & Procurement — Material & Packaging, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[02 · Source | Material & Packaging] Commodity Index Advisor — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-COMM-F91EA654", "status": "COMMITTED", "category": "02 · Sourcing & Procurement — Material & Packaging", "agent": "[02 · Source | Material & Packaging] Commodity Index Advisor", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "SAP Ariba Award Allocation, Redlined Negotiation Fact-Pack & SAP Purchasing Info-Record Update (ME12)"}`
- **Expected Markdown Report & Table**:

#### 📊 [02 · Source | Material & Packaging] Commodity Index Advisor — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `COMMOD-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `02 · Sourcing & Procurement — Material & Packaging` · **Persona**: `Category Sourcing Mgr (Direct)` · **Write-Back Receipt**: `ACT-COMM-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_commodity_index_advisor_telemetry_feed, query_commodity_index_advisor_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[02 · Source | Material & Packaging] Commodity Index Advisor — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_commodity_index_advisor_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 17. Dynamic Should-Cost Agent (`rfq_should_cost_agent`)
- **Pillar / Sub-Pillar**: 02 · Sourcing & Procurement — **Material & Packaging** · **Persona**: Strategic Sourcing Lead · **ROI**: `Fact-based margin leverage in RFPs`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Material & Packaging, Strategic Sourcing Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Dynamic Should-Cost Agent intervenes.
- **What This Agent Does**: Deconstructs packaging specs (resin weight, corrugate, conversion energy).
- **Business Result**: Fact-based margin leverage in RFPs. (**Fact-based margin leverage in RFPs**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Dynamic Should-Cost Agent.`
- **Read Tools It Must Call**: `query_material_should_cost_bom, query_commodity_index_rates, query_supplier_rfq_bids, query_combinatorial_award_scenarios`
- **Write-Back Tools It Must Call**: `action_award_supplier_contract, action_challenge_vendor_outlier`
- **Demo Data Input Values It Reads**:
  - Table `award_allocation_scenarios.json` (2 rows): Sample input record has `scenario_id=SCEN-AWARD-DUAL-70-30, name=OR-Tools Optimal Dual-Source Risk & Cost Frontier, part_number=PART-CAN-ALUM-330ML, annual_demand_units=50000000, primary_supplier=Ball Metal Packaging`
  - Table `commodity_index_rates.json` (3 rows): Sample input record has `index_symbol=LME-ALUM-CASH, commodity=London Metal Exchange Primary Aluminum Cash, current_price_usd_per_mt=2420.0, one_month_change_pct=-2.4, three_month_forecast_usd_per_mt=2380.0`
  - Table `material_should_cost_bom.json` (2 rows): Sample input record has `part_number=PART-CAN-ALUM-330ML, description=330ml Aluminum Beverage Can & Stay-on-Tab End, commodity_base=LME High Grade Aluminum (AL-99.7), net_weight_grams=12.8, raw_material_cost_usd=14.2`
  - Table `supplier_rfq_bids.json` (3 rows): Sample input record has `bid_id=BID-BALL-2026-01, part_number=PART-CAN-ALUM-330ML, supplier_id=VEND-BALL-CORP-101, supplier_name=Ball Metal Packaging, quoted_unit_cost_usd=31.2`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `Operational A2UI Visual Surface`
  - **Visual Mark Type**: `BAR` (20 data points: `source=1. Parametric Should-Cost, cost_component=Raw Material, cost_usd=14.2 | source=1. Parametric Should-Cost, cost_component=Machine Processing, cost_usd=6.8 | source=1. Parametric Should-Cost, cost_component=Direct Labor, cost_usd=3.4`)
- **Expected Write-Back Receipt**: `{"challenge_id": "CHAL-OUTLIER-70722333", "bid_id": "BID-ARDAGH-2026-03", "supplier_id": "VEND-ARDAGH-METAL-103", "part_number": "PART-CAN-ALUM-330ML", "target_reduction_pct": 18.0, "should_cost_gap_pct": 31.8, "status": "NEGOTIATION_CHALLENGE_DISPATCHED", "rationale": "Quoted SG&A and machine processing margin ($6.80/1k) exceeds clean-sheet benchmark ($3.10/1k) by 119%.", "idempotency_key": "CHAL-ARDAGH-202610-001"}`
- **Expected Markdown Report & Table**:

### 💎 SourcePulse Parametric Should-Cost & RFQ Award Briefing

> **Executive Summary**: Normalized 3 supplier RFQ quote proposals for **330ml Aluminum Cans (50M units annual volume)** against a bottom-up parametric should-cost baseline of **$29.60/1,000 units** (indexed to live LME cash aluminum at $2,420/MT). Identified an inflated bid from Ardagh Metal (+31.8% over should-cost) and issued an automated fact-based negotiation challenge. Solved optimal dual-sourcing in **Google OR-Tools MILP**, awarding **70% to Ball Corp ($31.20)** and **30% to Crown Holdings ($32.60)** to unlock **$115,000 annual direct material savings (6.8% net reduction)** with **96.5% supply security**.

#### 📊 Parametric Should-Cost vs Supplier Bid Ledger (Atomic Copy-Ready Table)

| Source / Bidder | Part Number | Raw Material | Machine Time | Labor | Freight | Margin / SG&A | Quoted Total / 1k | Variance vs Should-Cost | Document AI Confidence |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|:---|
| `1. Should-Cost Baseline` | `PART-CAN-ALUM-330ML` | $14.20 | $6.80 | $3.40 | $2.10 | $3.10 | **$29.60** | Baseline (0.0%) | Grounded Engineering Math |
| `2. Ball Metal Packaging` | `PART-CAN-ALUM-330ML` | $14.50 | $7.10 | $3.60 | $2.20 | $3.80 | **$31.20** | +5.4% (Competitive) | 99.0% Confidence |
| `3. Crown Holdings` | `PART-CAN-ALUM-330ML` | $14.80 | $7.40 | $3.80 | $2.40 | $4.20 | **$32.60** | +10.1% (Acceptable) | 98.0% Confidence |
| `4. Ardagh Metal Packaging` | `PART-CAN-ALUM-330ML` | $15.60 | $8.90 | $4.50 | $3.20 | $6.80 | **$39.00** | **+31.8% (Outlier High)** | 97.0% Confidence |

#### ⚡ Sourcing Actions & Commercial Awards Executed

- **Supplier Margin Challenge Dispatched**: `CHAL-OUTLIER-70722333` | Supplier: `VEND-ARDAGH-METAL-103` | Part: `PART-CAN-ALUM-330ML` | Target Reduction: **-18.0%** | Status: `NEGOTIATION_CHALLENGE_DISPATCHED`
- **SAP Ariba Dual-Source Contract Awarded**: `AWD-ARIBA-329EADB4` | Part: `PART-CAN-ALUM-330ML` | Primary: **Ball Metal Packaging (70.0%)** | Secondary: **Crown Holdings (30.0%)** | Status: `ARIBA_CONTRACT_AWARDED`

### 🔗 Connected Systems & Sourcing Stack
- **BigQuery Direct Materials Lake**: Clean-sheet parametric BOM equations linked to London Metal Exchange (LME) and ICIS resin indices.
- **Google Document AI**: Automated table and quote extraction parsing supplier bids with 98%+ field confidence.
- **Google OR-Tools Mixed-Integer Linear Programming**: Combinatorial split award balancing cost minimization against multi-supplier risk.
- **SAP Ariba Strategic Sourcing**: Direct contract award writeback creating outline agreements and purchase info records.

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_material_should_cost_bom, query_commodity_index_rates` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `Operational A2UI Visual Surface` (`BAR`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_award_supplier_contract` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 18. Sustainable Packaging Agent (`sustainable_packaging_agent`)
- **Pillar / Sub-Pillar**: 02 · Sourcing & Procurement — **Material & Packaging** · **Persona**: Packaging R&D Engineer · **ROI**: `Mitigates EPR and landfill taxation`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Material & Packaging, Packaging R&D Engineer teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Sustainable Packaging Agent intervenes.
- **What This Agent Does**: Evaluates PCR resins and barrier materials against line runnability & taxes.
- **Business Result**: Mitigates EPR and landfill taxation. (**Mitigates EPR and landfill taxation**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Sustainable Packaging Agent.`
- **Read Tools It Must Call**: `query_sustainable_packaging_agent_telemetry_feed, query_sustainable_packaging_agent_constraint_matrix, query_sustainable_packaging_agent_optimization_scenarios, query_sustainable_packaging_agent_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_sustainable_packaging_agent_plan, action_dispatch_sustainable_packaging_agent_alert`
- **Demo Data Input Values It Reads**:
  - Table `sustainable_packaging_agent_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=SUSTAI-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Material & Packaging, capacity_limit=12500`
  - Table `sustainable_packaging_agent_execution_ledger.json` (3 rows): Sample input record has `execution_id=SUSTAI-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Packaging R&D Engineer, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `sustainable_packaging_agent_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=02 · Source | Material & Packaging, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `sustainable_packaging_agent_telemetry_feed.json` (4 rows): Sample input record has `record_id=SUSTAI-TEL-101, company_id=XYZ-CORP-01, category=02 · Sourcing & Procurement — Material & Packaging, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[02 · Source | Material & Packaging] Sustainable Packaging Agent — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-SUST-F91EA654", "status": "COMMITTED", "category": "02 · Sourcing & Procurement — Material & Packaging", "agent": "[02 · Source | Material & Packaging] Sustainable Packaging Agent", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "EU CBAM / EUDR XML Customs Filing & SAP TM / Blue Yonder Low-Carbon Rail/EV/Ocean Lane Allocation"}`
- **Expected Markdown Report & Table**:

#### 📊 [02 · Source | Material & Packaging] Sustainable Packaging Agent — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `SUSTAI-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `02 · Sourcing & Procurement — Material & Packaging` · **Persona**: `Packaging R&D Engineer` · **Write-Back Receipt**: `ACT-SUST-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_sustainable_packaging_agent_telemetry_feed, query_sustainable_packaging_agent_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[02 · Source | Material & Packaging] Sustainable Packaging Agent — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_sustainable_packaging_agent_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 19. Contract Leakage Agent (`tariff_esg_agent`)
- **Pillar / Sub-Pillar**: 02 · Sourcing & Procurement — **Contract & PO Mgmt** · **Persona**: Commercial Sourcing / Legal · **ROI**: `Recovers missed rebates & surcharges`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Contract & PO Mgmt, Commercial Sourcing / Legal teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Contract Leakage Agent intervenes.
- **What This Agent Does**: Reconciles live spend against negotiated rebate tiers and volume discount scales.
- **Business Result**: Recovers missed rebates & surcharges. (**Recovers missed rebates & surcharges**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Contract Leakage Agent.`
- **Read Tools It Must Call**: `query_contract_clause_obligations, query_supplier_rebate_accruals, query_hs_tariff_classifications, query_cross_border_duty_impact`
- **Write-Back Tools It Must Call**: `action_lock_hs_tariff_classification, action_issue_supplier_rebate_debit_memo`
- **Demo Data Input Values It Reads**:
  - Table `contract_clause_obligations.json` (2 rows): Sample input record has `contract_id=MSA-BALL-2025-09, supplier_id=VEND-BALL-CORP-101, supplier_name=Ball Metal Packaging, effective_start=2025-01-01, effective_end=2027-12-31`
  - Table `cross_border_duty_impact.json` (2 rows): Sample input record has `entry_id=CUST-ENTRY-202610-01, part_number=PART-CAN-ALUM-330ML, customs_port=Port of New York / Newark, declared_customs_value_usd=485000.0, declared_hs_code=7612.90.1065`
  - Table `hs_tariff_classifications.json` (2 rows): Sample input record has `part_number=PART-CAN-ALUM-330ML, description=Aluminum Cans for Preserving Food or Drink (Capacity under 50 Liters), ten_digit_hs_code=7612.90.1065, wco_six_digit_heading=7612.90, general_duty_rate_pct=5.7`
  - Table `supplier_rebate_accruals.json` (2 rows): Sample input record has `accrual_id=REB-BALL-2026-YTD, contract_id=MSA-BALL-2025-09, supplier_id=VEND-BALL-CORP-101, supplier_name=Ball Metal Packaging, cumulative_spend_usd=1581000.0`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `Operational A2UI Visual Surface`
  - **Visual Mark Type**: `BAR` (12 data points: `lane=Rotterdam -> New York, metric=1. Standard Duty (Unoptimized), amount_usd=68000.0 | lane=Rotterdam -> New York, metric=2. Optimized Preferential Duty, amount_usd=12000.0 | lane=Rotterdam -> New York, metric=3. Supplier Rebate Recovered, amount_usd=42000.0`)
- **Expected Write-Back Receipt**: `{"debit_id": "AP-DEBIT-12C7DE39", "accrual_id": "REB-BALL-2026-YTD", "supplier_id": "VEND-BALL-CORP-101", "claim_amount_usd": 47430.0, "contract_reference": "MSA-BALL-2025-09", "status": "SAP_AP_DEBIT_MEMO_POSTED", "rationale": "Contractual 3.0% volume growth incentive threshold (40M units) exceeded with 48.2M units purchased. Recovering $47,430 uncredited rebate.", "idempotency_key": "DEBIT-BALL-202610-001"}`
- **Expected Markdown Report & Table**:

### ⚖️ ClauseGuard Contract Intelligence & Trade Compliance Briefing

> **Executive Summary**: Reconciled enterprise purchasing spend against **Document AI** parsed Master Supply Agreements in **AlloyDB pgvector**. Identified **$47,430.00 of uncollected volume rebate cash leakage** from Ball Metal Packaging (annual 40M-unit tier achieved at 48.2M units with zero vendor credit issued) and posted an automated debit memo in SAP AP. Concurrently audited cross-border container entries through the Port of New York, classifying 330ml aluminum cans under **10-digit HS Code `7612.90.1065`** with verified US Customs CROSS Ruling citations (`HQ H312891`), unlocking **$27,645.00 in preferential duty-free savings** with **99.6% audit compliance**.

#### 📊 Contract Compliance & Customs Tariff Ledger (Atomic Copy-Ready Table)

| Part Number | Description | 10-Digit HS Code | Legal Ruling Citation | General Duty | FTA Preferential Duty | Customs Duty Saved | Uncollected Rebate Recovered | Compliance Status |
|:---|:---|:---|:---|---:|---:|---:|---:|:---|
| `PART-CAN-ALUM-330ML` | 330ml Aluminum Cans | `7612.90.1065` | US Customs HQ H312891 | 5.7% ($27,645) | **0.0% ($0)** | **+$27,645.00** | **+$47,430.00** | `DUTY_FREE_CLEARED` |
| `PART-ELECTROLYTE-SALT` | LipF6 Electrolyte Salt | `2826.90.9000` | US Customs NY N298104 | 3.1% ($9,920) | **0.0% ($0)** | **+$9,920.00** | Settled | `DUTY_FREE_CLEARED` |

#### ⚡ Financial Recovery & Legal Governance Executed

- **SAP AP Supplier Rebate Debit Memo Posted**: `AP-DEBIT-12C7DE39` | Supplier: `VEND-BALL-CORP-101` | Claim Amount: **$47,430.00** | Contract: `MSA-BALL-2025-09` | Status: `SAP_AP_DEBIT_MEMO_POSTED`
- **SAP GTS 10-Digit HS Tariff Code Locked**: `GTS-HS-E72CBB3B` | Part: `PART-CAN-ALUM-330ML` | HS Code: **`7612.90.1065`** | Ruling: `US Customs HQ H312891 / NY N301452` | Status: `SAP_GTS_HS_LOCKED`

### 🔗 Connected Systems & Legal Architecture
- **AlloyDB pgvector Legal Contract RAG**: Automated parsing of Master Supply Agreements, price escalation formulas, and volume rebate tiers.
- **Global Customs & WCO Tariff Database**: CROSS legal rulings and Harmonized System 10-digit classification engine.
- **SAP Global Trade Services (GTS)**: Binding writeback locking customs commodity codes and preferential trade declarations.
- **SAP S/4HANA Accounts Payable**: Automated EDI 812 debit memo generation to deduct earned rebates from vendor remittances.

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_contract_clause_obligations, query_supplier_rebate_accruals` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `Operational A2UI Visual Surface` (`BAR`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_lock_hs_tariff_classification` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 20. PO Expediting Agent (`master_data_leadtime_steward`)
- **Pillar / Sub-Pillar**: 02 · Sourcing & Procurement — **Contract & PO Mgmt** · **Persona**: Buyer / Procurement Coord. · **ROI**: `Resolves ~70% of standard PO delays`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Contract & PO Mgmt, Buyer / Procurement Coord. teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before PO Expediting Agent intervenes.
- **What This Agent Does**: Monitors EDI 855/856 delay feeds and orchestrates supplier split-shipments.
- **Business Result**: Resolves ~70% of standard PO delays. (**Resolves ~70% of standard PO delays**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for PO Expediting Agent.`
- **Read Tools It Must Call**: `query_material_master_records, query_leadtime_drift_anomalies, query_cubiscan_dimension_discrepancies, query_vendor_master_integrity`
- **Write-Back Tools It Must Call**: `action_heal_material_leadtime, action_remediate_cubiscan_dimensions`
- **Demo Data Input Values It Reads**:
  - Table `bom_routing_leadtimes.json` (2 rows): Sample input record has `bom_id=BOM-EV-INVERTER-V2, parent_material_id=MAT-880019, component_count=48, critical_path_leadtime_days=46, system_recorded_leadtime_days=21`
  - Table `dimension_audit_scans.json` (2 rows): Sample input record has `scan_id=SCAN-3D-99014, material_id=MAT-880019, scanned_plant=PLANT-1010, cubiscan_length_cm=52.0, recorded_length_cm=45.0`
  - Table `material_master_mara_marc.json` (3 rows): Sample input record has `material_id=MAT-880019, description=High-Voltage Power Inverter Module 800V SiC, material_type=FERT, base_uom=EA, plant=PLANT-1010`
  - Table `vendor_master_records.json` (2 rows): Sample input record has `vendor_id=VEND-10492, vendor_name=Taiwan Micro-Power Semiconductor Corp, tax_id=TW-88401923, country=Taiwan, bank_account_verification=VERIFIED_ACTIVE`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `DataCleanse · Master Data Self-Healing Lead Time & Volume Cockpit`
  - **Visual Mark Type**: `BAR / LINE` (0 data points: `Live fixture series`)
- **Expected Write-Back Receipt**: `{"status": "healed", "heal_id": "HEAL-LT-200BF8BC", "audit_trail": "SAP Material Master updated [HEAL-LT-200BF8BC]: MAT-880019 at PLANT-1010 calibrated to 46 days delivery lead time. Rationale: Auto-heal 25-day drift between planned and empirical vendor lead time.."}`
- **Expected Markdown Report & Table**:

### 🧹 Master Data Hygiene Briefing: SAP Lead-Time & 3D Packaging Audit

Autonomous audit scanned **2,480 Material Master records** across MARC/MARA and engineering BOMs. Detected critical lead-time drift on **14 high-velocity components** (up to +34 days late), creating phantom safety stockouts. Reconciled 3D CubiScan volumetric laser scans, eliminating **$3.8M** in excess working capital buffer and avoiding carrier freight surcharges.

### 📋 Remediated Material Master & Dimension Schedule

| Material SKU | Description | Plant | Planned Lead Time (Days) | Actual P95 Cycle (Days) | Drift | Remediated Status | Working Capital Freed ($) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `MAT-880019` | HV Power Inverter 800V SiC | PLANT-1010 | 21 days | 46 days | **+25 days** | `MARC-PLIFZ CALIBRATED` | $1,240,000 |
| `MAT-901140` | Cavitating Flow Valve | PLANT-1020 | 14 days | 48 days | **+34 days** | `MARC-PLIFZ CALIBRATED` | $1,180,000 |
| `MAT-440212` | LFP Battery Cell 3.2V 100Ah | PLANT-1010 | 35 days | 38 days | +3 days | `TOLERANCE OK` | $0 |
| `MAT-102944` | High-Pressure Seal Ring | PLANT-2010 | 10 days | 8 days | -2 days | `SAFETY BUFFER REDUCED` | $420,000 |

### 🚀 Executed Autonomous Master Data Actions

1. **ERP Lead-Time Recalibration (`ECO-20261016-01`)**: Updated SAP field `MARC-PLIFZ` to 46 days for `MAT-880019`, synchronizing MRP schedule.
2. **CubiScan 3D Dimension Reconciliation (`DIM-20261016-01`)**: Corrected volumetric packaging profile from `28,000 cm³` to `34,650 cm³`, preventing LTL carrier volumetric penalties.

### 🔗 Connected Systems & Data Sources

* **SAP S/4HANA ERP**: BAPI Material Master read/write interface (`BAPI_MATERIAL_MAINTAINDAK_PV`).
* **CubiScan 125 Automated Laser Dimensioning**: Warehouse inbound scanning conveyor telemetry.
* **Siemens Teamcenter PLM**: Engineering Change Order (ECO) routing tolerance validation.

### 🛡️ Engineering Governance & Quality Gate

* **ECO Threshold Verification**: Lead-time delta of 25 days verified within approved autonomous <90 day window.
* **Audit Hash**: `sha256:3d81b49e1f0c...`
* **Pre-execution Idempotency**: Verified.


#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_material_master_records, query_leadtime_drift_anomalies` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `DataCleanse · Master Data Self-Healing Lead Time & Volume Cockpit` (`BAR / LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_heal_material_leadtime` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 21. Three-Way Match Dispute (`three_way_match_dispute`)
- **Pillar / Sub-Pillar**: 02 · Sourcing & Procurement — **Contract & PO Mgmt** · **Persona**: Accounts Payable Lead · **ROI**: `Prevents vendor holds & saves discounts`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Contract & PO Mgmt, Accounts Payable Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Three-Way Match Dispute intervenes.
- **What This Agent Does**: Diagnoses price/quantity discrepancies across POs, GRNs, and carrier invoices.
- **Business Result**: Prevents vendor holds & saves discounts. (**Prevents vendor holds & saves discounts**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Three-Way Match Dispute.`
- **Read Tools It Must Call**: `query_three_way_match_dispute_telemetry_feed, query_three_way_match_dispute_constraint_matrix, query_three_way_match_dispute_optimization_scenarios, query_three_way_match_dispute_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_three_way_match_dispute_plan, action_dispatch_three_way_match_dispute_alert`
- **Demo Data Input Values It Reads**:
  - Table `three_way_match_dispute_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=THREE_-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Contract & PO Mgmt, capacity_limit=12500`
  - Table `three_way_match_dispute_execution_ledger.json` (3 rows): Sample input record has `execution_id=THREE_-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Accounts Payable Lead, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `three_way_match_dispute_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=02 · Source | Contract & PO Mgmt, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `three_way_match_dispute_telemetry_feed.json` (4 rows): Sample input record has `record_id=THREE_-TEL-101, company_id=XYZ-CORP-01, category=02 · Sourcing & Procurement — Contract & PO Mgmt, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[02 · Source | Contract & PO Mgmt] Three-Way Match Dispute — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-THRE-F91EA654", "status": "COMMITTED", "category": "02 · Sourcing & Procurement — Contract & PO Mgmt", "agent": "[02 · Source | Contract & PO Mgmt] Three-Way Match Dispute", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "SAP GTS 10-Digit HS Code Lock, FTA Certificate Filing & SAP AP Supplier Rebate Debit Memo"}`
- **Expected Markdown Report & Table**:

#### 📊 [02 · Source | Contract & PO Mgmt] Three-Way Match Dispute — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `THREE_-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `02 · Sourcing & Procurement — Contract & PO Mgmt` · **Persona**: `Accounts Payable Lead` · **Write-Back Receipt**: `ACT-THRE-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_three_way_match_dispute_telemetry_feed, query_three_way_match_dispute_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[02 · Source | Contract & PO Mgmt] Three-Way Match Dispute — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_three_way_match_dispute_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

## 03 · Manufacturing & Operations (9 Agents)

### 22. Changeover Optimizer (`finite_production_scheduler`)
- **Pillar / Sub-Pillar**: 03 · Manufacturing & Operations — **Production Scheduling** · **Persona**: Master Production Scheduler · **ROI**: `Cuts sanitation downtime by 15–25%`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Production Scheduling, Master Production Scheduler teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Changeover Optimizer intervenes.
- **What This Agent Does**: Sequences allergen, kosher, and packaging runs to minimize washdowns.
- **Business Result**: Cuts sanitation downtime by 15–25%. (**Cuts sanitation downtime by 15–25%**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Changeover Optimizer.`
- **Read Tools It Must Call**: `query_production_orders_backlog, query_changeover_matrix_rules, query_plant_line_workcenters, query_optimized_sequence_schedule`
- **Write-Back Tools It Must Call**: `action_solve_and_lock_finite_sequence, action_dispatch_sap_ppds_sequence`
- **Demo Data Input Values It Reads**:
  - Table `changeover_matrix_rules.json` (3 rows): Sample input record has `rule_id=CO-RULE-ALLERGEN-CLEANOUT, from_product_family=BEVERAGE_NUT_BASE, to_product_family=BEVERAGE_OAT_BASE, changeover_type=DEEP_ALLERGEN_CIP_WASH_ATP_SWAB, setup_duration_hours=4.0`
  - Table `optimized_sequence_schedule.json` (1 rows): Sample input record has `schedule_id=SCHED-OR-TOOLS-2026W42-01, workcenter_id=WC-LINE-ASEPTIC-01, solver_engine=OR_TOOLS_CPSAT_SOLVER, objective_value_min_changeover_hours=4.5, baseline_unoptimized_changeover_hours=9.5`
  - Table `plant_line_workcenters.json` (2 rows): Sample input record has `workcenter_id=WC-LINE-ASEPTIC-01, workcenter_name=Aseptic Tetra Pak High-Speed Filling Line 01, plant_id=PLANT-1020-AUSTIN, max_throughput_liters_hr=9000, current_scheduled_load_pct=82.5`
  - Table `production_orders_backlog.json` (3 rows): Sample input record has `order_id=ORD-PROD-202610-771, material_id=SKU-BEV-OATMILK-ORIGINAL-1L, material_description=Organic Oat Milk Original 1L Tetra Brik, product_family=BEVERAGE_OAT_BASE, allergen_group=NON_ALLERGENIC`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `FlowMaster Production Sequence Gantt (Aseptic Filling Line 01)`
  - **Visual Mark Type**: `BAR` (5 data points: `task=Oat Milk Original, start_hour=0.0, end_hour=6.0 | task=Color Flush, start_hour=6.0, end_hour=6.5 | task=Oat Chocolate, start_hour=6.5, end_hour=11.5`)
- **Expected Write-Back Receipt**: `{"sequence_id": "SEQ-CPSAT-A24ECFE6", "workcenter_id": "WC-LINE-ASEPTIC-01", "order_ids": ["ORD-PROD-202610-771", "ORD-PROD-202610-772", "ORD-PROD-202610-773"], "objective_type": "MINIMIZE_CHANGEOVER_HOURS", "changeover_hours_saved": 5.0, "status": "OR_TOOLS_SEQUENCE_LOCKED", "rationale": "Solved optimal job order: Oat Milk Original -> Oat Chocolate -> Almond Vanilla. Slashes changeover from 9.5h to 4.5h, saving 5.0h of line uptime.", "idempotency_key": "SEQ-LOCK-202610-001"}`
- **Expected Markdown Report & Table**:

### ⏱️ FlowMaster Finite Production Line Sequence Briefing

> **Executive Summary**: Formulated and solved a finite capacity job shop schedule on **Aseptic Tetra Pak Line 01** at Plant Austin using **Google OR-Tools CP-SAT**. Evaluated a 112,500-liter production backlog across organic oat milk, chocolate oat milk, and tree-nut allergen vanilla almond milk. By solving sequence-dependent Cleaning-in-Place (CIP) matrices, the agent scheduled light non-allergenic batches first and clustered dark and allergen runs at the end of the shift block. This reduced changeover wash time from **9.5 hours to 4.5 hours**, unlocking **5.0 hours of extra filling line uptime**, adding **+37,500 liters of throughput capacity**, and generating **+$18,750.00 in net production margin**.

#### 📊 Optimized Production Sequence & CIP Cleanout Schedule (Atomic Copy-Ready Table)

| Seq | Production Order | Material Description | Batch Volume | Run Time | Preceding Cleanout | Cleanout Type | Scheduled Window |
|---:|:---|:---|---:|---:|---:|:---|:---|
| **1** | `ORD-PROD-202610-771` | Oat Milk Original 1L | 45,000 L | 6.0 hrs | 0.0 hrs | Clean Start | 23-Oct 06:00 – 12:00 |
| **2** | `ORD-PROD-202610-773` | Oat Milk Chocolate 1L | 37,500 L | 5.0 hrs | **0.5 hrs** | Light Line Flush | 23-Oct 12:30 – 17:30 |
| **3** | `ORD-PROD-202610-772` | Almond Milk Vanilla 1L | 30,000 L | 4.0 hrs | **4.0 hrs** | Deep Allergen CIP | 23-Oct 21:30 – 01:30 |

#### ⚡ Production Scheduling Execution Dispatched

- **OR-Tools CP-SAT Sequence Locked**: `SEQ-CPSAT-A24ECFE6` | Workcenter: `WC-LINE-ASEPTIC-01` | Changeover Saved: **5.0 hrs** | Status: `OR_TOOLS_SEQUENCE_LOCKED`
- **SAP PP/DS Sequence Dispatched**: `PPDS-DISP-194D65BB` | Schedule: `SCHED-OR-TOOLS-2026W42-01` | Plant: `PLANT-1020-AUSTIN` | Status: `SAP_PPDS_SCHEDULE_DISPATCHED`

### 🔗 Connected Systems & Optimization Architecture
- **Google OR-Tools CP-SAT Engine**: Exact constraint programming solver optimizing sequence-dependent setup times and shift calendars.
- **Allergen & Color Matrix Vault**: FDA FALCPA compliant changeover rules and ATP biological swab validation requirements.
- **SAP S/4HANA PP/DS**: Detailed scheduling board writeback, planned order freezing, and material staging trigger.
- **Siemens Opcenter MES**: Work order dispatch queue and automated CIP skid cycle initiation.

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_production_orders_backlog, query_changeover_matrix_rules` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `FlowMaster Production Sequence Gantt (Aseptic Filling Line 01)` (`BAR`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_solve_and_lock_finite_sequence` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 23. Disruption Re-sequencer (`line_schedule_optimizer`)
- **Pillar / Sub-Pillar**: 03 · Manufacturing & Operations — **Production Scheduling** · **Persona**: Shop Floor / Shift Lead · **ROI**: `Line reallocation in <3 minutes`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Production Scheduling, Shop Floor / Shift Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Disruption Re-sequencer intervenes.
- **What This Agent Does**: Detects machine halts and re-routes perishable WIP to alternate lines.
- **Business Result**: Line reallocation in <3 minutes. (**Line reallocation in <3 minutes**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Disruption Re-sequencer.`
- **Read Tools It Must Call**: `query_production_orders_backlog, query_changeover_matrix_rules, query_plant_line_workcenters, query_optimized_sequence_schedule`
- **Write-Back Tools It Must Call**: `action_solve_and_lock_finite_sequence, action_dispatch_sap_ppds_sequence`
- **Demo Data Input Values It Reads**:
  - Table `changeover_matrix_rules.json` (3 rows): Sample input record has `rule_id=CO-RULE-ALLERGEN-CLEANOUT, from_product_family=BEVERAGE_NUT_BASE, to_product_family=BEVERAGE_OAT_BASE, changeover_type=DEEP_ALLERGEN_CIP_WASH_ATP_SWAB, setup_duration_hours=4.0`
  - Table `optimized_sequence_schedule.json` (1 rows): Sample input record has `schedule_id=SCHED-OR-TOOLS-2026W42-01, workcenter_id=WC-LINE-ASEPTIC-01, solver_engine=OR_TOOLS_CPSAT_SOLVER, objective_value_min_changeover_hours=4.5, baseline_unoptimized_changeover_hours=9.5`
  - Table `plant_line_workcenters.json` (2 rows): Sample input record has `workcenter_id=WC-LINE-ASEPTIC-01, workcenter_name=Aseptic Tetra Pak High-Speed Filling Line 01, plant_id=PLANT-1020-AUSTIN, max_throughput_liters_hr=9000, current_scheduled_load_pct=82.5`
  - Table `production_orders_backlog.json` (3 rows): Sample input record has `order_id=ORD-PROD-202610-771, material_id=SKU-BEV-OATMILK-ORIGINAL-1L, material_description=Organic Oat Milk Original 1L Tetra Brik, product_family=BEVERAGE_OAT_BASE, allergen_group=NON_ALLERGENIC`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `FlowMaster Production Sequence Gantt (Aseptic Filling Line 01)`
  - **Visual Mark Type**: `BAR` (5 data points: `task=Oat Milk Original, start_hour=0.0, end_hour=6.0 | task=Color Flush, start_hour=6.0, end_hour=6.5 | task=Oat Chocolate, start_hour=6.5, end_hour=11.5`)
- **Expected Write-Back Receipt**: `{"sequence_id": "SEQ-CPSAT-A24ECFE6", "workcenter_id": "WC-LINE-ASEPTIC-01", "order_ids": ["ORD-PROD-202610-771", "ORD-PROD-202610-772", "ORD-PROD-202610-773"], "objective_type": "MINIMIZE_CHANGEOVER_HOURS", "changeover_hours_saved": 5.0, "status": "OR_TOOLS_SEQUENCE_LOCKED", "rationale": "Solved optimal job order: Oat Milk Original -> Oat Chocolate -> Almond Vanilla. Slashes changeover from 9.5h to 4.5h, saving 5.0h of line uptime.", "idempotency_key": "SEQ-LOCK-202610-001"}`
- **Expected Markdown Report & Table**:

### ⏱️ FlowMaster Finite Production Line Sequence Briefing

> **Executive Summary**: Formulated and solved a finite capacity job shop schedule on **Aseptic Tetra Pak Line 01** at Plant Austin using **Google OR-Tools CP-SAT**. Evaluated a 112,500-liter production backlog across organic oat milk, chocolate oat milk, and tree-nut allergen vanilla almond milk. By solving sequence-dependent Cleaning-in-Place (CIP) matrices, the agent scheduled light non-allergenic batches first and clustered dark and allergen runs at the end of the shift block. This reduced changeover wash time from **9.5 hours to 4.5 hours**, unlocking **5.0 hours of extra filling line uptime**, adding **+37,500 liters of throughput capacity**, and generating **+$18,750.00 in net production margin**.

#### 📊 Optimized Production Sequence & CIP Cleanout Schedule (Atomic Copy-Ready Table)

| Seq | Production Order | Material Description | Batch Volume | Run Time | Preceding Cleanout | Cleanout Type | Scheduled Window |
|---:|:---|:---|---:|---:|---:|:---|:---|
| **1** | `ORD-PROD-202610-771` | Oat Milk Original 1L | 45,000 L | 6.0 hrs | 0.0 hrs | Clean Start | 23-Oct 06:00 – 12:00 |
| **2** | `ORD-PROD-202610-773` | Oat Milk Chocolate 1L | 37,500 L | 5.0 hrs | **0.5 hrs** | Light Line Flush | 23-Oct 12:30 – 17:30 |
| **3** | `ORD-PROD-202610-772` | Almond Milk Vanilla 1L | 30,000 L | 4.0 hrs | **4.0 hrs** | Deep Allergen CIP | 23-Oct 21:30 – 01:30 |

#### ⚡ Production Scheduling Execution Dispatched

- **OR-Tools CP-SAT Sequence Locked**: `SEQ-CPSAT-A24ECFE6` | Workcenter: `WC-LINE-ASEPTIC-01` | Changeover Saved: **5.0 hrs** | Status: `OR_TOOLS_SEQUENCE_LOCKED`
- **SAP PP/DS Sequence Dispatched**: `PPDS-DISP-194D65BB` | Schedule: `SCHED-OR-TOOLS-2026W42-01` | Plant: `PLANT-1020-AUSTIN` | Status: `SAP_PPDS_SCHEDULE_DISPATCHED`

### 🔗 Connected Systems & Optimization Architecture
- **Google OR-Tools CP-SAT Engine**: Exact constraint programming solver optimizing sequence-dependent setup times and shift calendars.
- **Allergen & Color Matrix Vault**: FDA FALCPA compliant changeover rules and ATP biological swab validation requirements.
- **SAP S/4HANA PP/DS**: Detailed scheduling board writeback, planned order freezing, and material staging trigger.
- **Siemens Opcenter MES**: Work order dispatch queue and automated CIP skid cycle initiation.

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_production_orders_backlog, query_changeover_matrix_rules` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `FlowMaster Production Sequence Gantt (Aseptic Filling Line 01)` (`BAR`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_solve_and_lock_finite_sequence` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 24. Labor & Line Balancing (`labor_line_balancing_agent`)
- **Pillar / Sub-Pillar**: 03 · Manufacturing & Operations — **Production Scheduling** · **Persona**: Plant Operations Manager · **ROI**: `Prevents certified skill bottlenecks`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Production Scheduling, Plant Operations Manager teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Labor & Line Balancing intervenes.
- **What This Agent Does**: Maps shift skill certifications and fatigue constraints to line speeds.
- **Business Result**: Prevents certified skill bottlenecks. (**Prevents certified skill bottlenecks**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Labor & Line Balancing.`
- **Read Tools It Must Call**: `query_labor_line_balancing_agent_telemetry_feed, query_labor_line_balancing_agent_constraint_matrix, query_labor_line_balancing_agent_optimization_scenarios, query_labor_line_balancing_agent_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_labor_line_balancing_agent_plan, action_dispatch_labor_line_balancing_agent_alert`
- **Demo Data Input Values It Reads**:
  - Table `labor_line_balancing_agent_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=LABOR_-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Production Scheduling, capacity_limit=12500`
  - Table `labor_line_balancing_agent_execution_ledger.json` (3 rows): Sample input record has `execution_id=LABOR_-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Plant Operations Manager, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `labor_line_balancing_agent_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=03 · Make | Production Scheduling, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `labor_line_balancing_agent_telemetry_feed.json` (4 rows): Sample input record has `record_id=LABOR_-TEL-101, company_id=XYZ-CORP-01, category=03 · Manufacturing & Production — Production Scheduling, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[03 · Make | Production Scheduling] Labor & Line Balancing — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-LABO-F91EA654", "status": "COMMITTED", "category": "03 · Manufacturing & Production — Production Scheduling", "agent": "[03 · Make | Production Scheduling] Labor & Line Balancing", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "SAP PP/DS Production Order Dispatch Sequence (BAPI_PRODORD_CHANGE) & Siemens MES Line Recipe Queue"}`
- **Expected Markdown Report & Table**:

#### 📊 [03 · Make | Production Scheduling] Labor & Line Balancing — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `LABOR_-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `03 · Manufacturing & Production — Production Scheduling` · **Persona**: `Plant Operations Manager` · **Write-Back Receipt**: `ACT-LABO-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_labor_line_balancing_agent_telemetry_feed, query_labor_line_balancing_agent_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[03 · Make | Production Scheduling] Labor & Line Balancing — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_labor_line_balancing_agent_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 25. Bottleneck Diagnostic (`predictive_oee_sentinel`)
- **Pillar / Sub-Pillar**: 03 · Manufacturing & Operations — **Capacity Planning** · **Persona**: Supply Chain Ops Director · **ROI**: `Flags facility constraints 3–6 mos out`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Capacity Planning, Supply Chain Ops Director teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Bottleneck Diagnostic intervenes.
- **What This Agent Does**: Assesses CIP utilities, boiler loads, and cold storage holding limits.
- **Business Result**: Flags facility constraints 3–6 mos out. (**Flags facility constraints 3–6 mos out**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Bottleneck Diagnostic.`
- **Read Tools It Must Call**: `query_plant_machine_telemetry, query_oee_breakdown_metrics, query_predictive_maintenance_anomalies, query_spare_parts_inventory_status`
- **Write-Back Tools It Must Call**: `action_dispatch_preventive_work_order, action_reserve_spare_parts`
- **Demo Data Input Values It Reads**:
  - Table `oee_breakdown_metrics.json` (2 rows): Sample input record has `metric_id=OEE-MILLING-CNC-04-2026W42, asset_id=ASSET-MILLING-CNC-04, production_line=LINE-MACHINING-BAY-02, shift_id=SHIFT-MORNING-A, planned_production_time_min=480.0`
  - Table `plant_machine_telemetry.json` (2 rows): Sample input record has `sensor_id=SENS-CNC-SPINDLE-VIB-01, asset_id=ASSET-MILLING-CNC-04, asset_name=5-Axis High-Precision Milling Center CNC-04, plant_id=PLANT-1020-AUSTIN, component=High-Speed Spindle Bearing Assembly`
  - Table `predictive_maintenance_anomalies.json` (2 rows): Sample input record has `anomaly_id=ANOM-CNC-04-VIB-992, asset_id=ASSET-MILLING-CNC-04, asset_name=5-Axis High-Precision Milling Center CNC-04, failure_mode=SPINDLE_FRONT_ROLLER_BEARING_FLAKING, severity=CRITICAL_HIGH`
  - Table `spare_parts_inventory_status.json` (2 rows): Sample input record has `part_number=PART-SPARE-BEARING-CERAMIC-7014, description=High-Precision Angular Contact Ceramic Spindle Bearing (7014-C-P4A), compatible_assets=['ASSET-MILLING-CNC-04', 'ASSET-MILLING-CNC-05'], stock_on_hand=3, reserved_quantity=0`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `AssetGuard OEE Loss Waterfall (CNC Milling Center CNC-04)`
  - **Visual Mark Type**: `BAR + TICK` (4 data points: `component=Availability, rate_pct=73.33, benchmark_pct=90.0 | component=Performance, rate_pct=84.66, benchmark_pct=95.0 | component=Quality, rate_pct=91.95, benchmark_pct=99.0`)
- **Expected Write-Back Receipt**: `{"work_order_id": "PM-WO-C082ED34", "asset_id": "ASSET-MILLING-CNC-04", "maintenance_type": "EMERGENCY_PREVENTIVE_OVERHAUL", "priority": "HIGH_PRIORITY", "maintenance_window": "NEXT_SHIFT_WINDOW_2200_TO_0230", "status": "SAP_PM_WORK_ORDER_DISPATCHED", "rationale": "Vibration velocity RMS 7.42 mm/s exceeds critical limit 7.10 mm/s. Spindle bearing flaking predicted in 36 hours. Intercepting before catastrophic $85k breakdown.", "idempotency_key": "WO-CNC04-202610-001"}`
- **Expected Markdown Report & Table**:

### ⚙️ AssetGuard Plant Predictive Maintenance & OEE Briefing

> **Executive Summary**: Intercepted severe spindle bearing degradation on **5-Axis CNC Milling Center CNC-04** at Plant Austin. Real-time vibration telemetry reached **7.42 mm/s RMS** (violating the critical threshold of 7.10 mm/s), driving line OEE down to **57.1%** (due to 128 minutes of vibration trips and speed throttling). Machine learning anomaly models project catastrophic spindle seizure within **36 hours**, risking **$85,000.00 in unplanned scrap and line downtime**. Dispatched an automated **SAP PM preventive work order** scheduled for the upcoming shift window (22:00–02:30) and reserved the replacement **ceramic angular contact bearing** in SAP MM, achieving **$80,800.00 in net avoided breakdown losses**.

#### 📊 Machine Health & OEE Decomposition (Atomic Copy-Ready Table)

| Asset ID | Description | Vibration RMS | Temp (°C) | Live OEE | Availability | Est. TTF | Unplanned Risk | Avoided Loss | Maintenance Action |
|:---|:---|---:|---:|---:|---:|---:|---:|---:|:---|
| `ASSET-MILLING-CNC-04` | 5-Axis Milling Center CNC-04 | **7.42 mm/s** | 84.6°C | **57.08%** | 73.33% | **36.0 hrs** | $85,000.00 | **+$80,800.00** | `SAP_PM_WORK_ORDER_DISPATCHED` |
| `ASSET-INJECTION-MOLD-02` | Hydraulic Mold IMM-02 | 2.15 mm/s | 52.3°C | **94.58%** | 96.88% | 340.0 hrs | $12,000.00 | Settled | `NORMAL_OPTIMAL` |

#### ⚡ Autonomous Maintenance Execution Dispatched

- **SAP PM Work Order Dispatched**: `PM-WO-C082ED34` | Asset: `ASSET-MILLING-CNC-04` | Window: `NEXT_SHIFT_WINDOW_2200_TO_0230` | Priority: `HIGH_PRIORITY` | Status: `SAP_PM_WORK_ORDER_DISPATCHED`
- **SAP MM Spare Parts Reserved**: `RES-MM-183E6296` | Part: `PART-SPARE-BEARING-CERAMIC-7014` | Quantity: **1 ea** | WO: `PM-WO-C082ED34` | Status: `SAP_MM_PARTS_RESERVED`

### 🔗 Connected Systems & Industrial IoT Architecture
- **Siemens Opcenter MES**: Machine state events, shift run hours, and automated OEE Availability / Performance / Quality calculation.
- **OSIsoft PI Historian**: High-frequency vibration, acoustic emission, and motor current signature analytics (MCSA).
- **SAP S/4HANA Plant Maintenance (PM)**: BAPI_ALM_ORDER_MAINTAIN automated order creation and technician routing.
- **SAP S/4HANA Materials Management (MM)**: Real-time M&R crib inventory reservation and automated replenishment PO triggers.

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_plant_machine_telemetry, query_oee_breakdown_metrics` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `AssetGuard OEE Loss Waterfall (CNC Milling Center CNC-04)` (`BAR + TICK`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_dispatch_preventive_work_order` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 26. Co-Packer Allocation (`copacker_allocation_agent`)
- **Pillar / Sub-Pillar**: 03 · Manufacturing & Operations — **Capacity Planning** · **Persona**: External Sourcing / CMO Lead · **ROI**: `Optimizes net gross margin per case`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Capacity Planning, External Sourcing / CMO Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Co-Packer Allocation intervenes.
- **What This Agent Does**: Models internal conversion costs against co-packer tolling agreements.
- **Business Result**: Optimizes net gross margin per case. (**Optimizes net gross margin per case**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Co-Packer Allocation.`
- **Read Tools It Must Call**: `query_copacker_allocation_agent_telemetry_feed, query_copacker_allocation_agent_constraint_matrix, query_copacker_allocation_agent_optimization_scenarios, query_copacker_allocation_agent_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_copacker_allocation_agent_plan, action_dispatch_copacker_allocation_agent_alert`
- **Demo Data Input Values It Reads**:
  - Table `copacker_allocation_agent_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=COPACK-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Capacity Planning, capacity_limit=12500`
  - Table `copacker_allocation_agent_execution_ledger.json` (3 rows): Sample input record has `execution_id=COPACK-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=External Sourcing / CMO Lead, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `copacker_allocation_agent_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=03 · Make | Capacity Planning, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `copacker_allocation_agent_telemetry_feed.json` (4 rows): Sample input record has `record_id=COPACK-TEL-101, company_id=XYZ-CORP-01, category=03 · Manufacturing & Production — Capacity Planning, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[03 · Make | Capacity Planning] Co-Packer Allocation — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-COPA-F91EA654", "status": "COMMITTED", "category": "03 · Manufacturing & Production — Capacity Planning", "agent": "[03 · Make | Capacity Planning] Co-Packer Allocation", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "SAP IBP / S/4HANA Master Production Schedule (MPS) & Financial P&L Bridge Commit"}`
- **Expected Markdown Report & Table**:

#### 📊 [03 · Make | Capacity Planning] Co-Packer Allocation — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `COPACK-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `03 · Manufacturing & Production — Capacity Planning` · **Persona**: `External Sourcing / CMO Lead` · **Write-Back Receipt**: `ACT-COPA-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_copacker_allocation_agent_telemetry_feed, query_copacker_allocation_agent_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[03 · Make | Capacity Planning] Co-Packer Allocation — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_copacker_allocation_agent_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 27. CapEx Simulator (`capex_simulator_agent`)
- **Pillar / Sub-Pillar**: 03 · Manufacturing & Operations — **Capacity Planning** · **Persona**: VP Manufacturing Engineering · **ROI**: `Delivers defensible board CapEx ROI`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Capacity Planning, VP Manufacturing Engineering teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before CapEx (Capital Expenditure — buying heavy equipment) Simulator intervenes.
- **What This Agent Does**: Simulates multi-year volume trends to test high-speed line expansions.
- **Business Result**: Delivers defensible board CapEx (Capital Expenditure — buying heavy equipment) ROI. (**Delivers defensible board CapEx ROI**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for CapEx Simulator.`
- **Read Tools It Must Call**: `query_capex_simulator_agent_telemetry_feed, query_capex_simulator_agent_constraint_matrix, query_capex_simulator_agent_optimization_scenarios, query_capex_simulator_agent_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_capex_simulator_agent_plan, action_dispatch_capex_simulator_agent_alert`
- **Demo Data Input Values It Reads**:
  - Table `capex_simulator_agent_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=CAPEX_-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Capacity Planning, capacity_limit=12500`
  - Table `capex_simulator_agent_execution_ledger.json` (3 rows): Sample input record has `execution_id=CAPEX_-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=VP Manufacturing Engineering, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `capex_simulator_agent_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=03 · Make | Capacity Planning, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `capex_simulator_agent_telemetry_feed.json` (4 rows): Sample input record has `record_id=CAPEX_-TEL-101, company_id=XYZ-CORP-01, category=03 · Manufacturing & Production — Capacity Planning, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[03 · Make | Capacity Planning] CapEx Simulator — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-CAPE-F91EA654", "status": "COMMITTED", "category": "03 · Manufacturing & Production — Capacity Planning", "agent": "[03 · Make | Capacity Planning] CapEx Simulator", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "SAP SD Customer MOQ / Bracket Pricing Policy Update & SAP S/4HANA Sourcing Assignment Split"}`
- **Expected Markdown Report & Table**:

#### 📊 [03 · Make | Capacity Planning] CapEx Simulator — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `CAPEX_-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `03 · Manufacturing & Production — Capacity Planning` · **Persona**: `VP Manufacturing Engineering` · **Write-Back Receipt**: `ACT-CAPE-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_capex_simulator_agent_telemetry_feed, query_capex_simulator_agent_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[03 · Make | Capacity Planning] CapEx Simulator — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_capex_simulator_agent_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 28. Visual Defect Triager (`inline_yield_guardian`)
- **Pillar / Sub-Pillar**: 03 · Manufacturing & Operations — **Quality & Compliance** · **Persona**: QA Manager / Line Inspector · **ROI**: `Prevents full pallet scrap & holds`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Quality & Compliance, QA Manager / Line Inspector teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Visual Defect Triager intervenes.
- **What This Agent Does**: Inspects high-speed video frames for crimped seals, lot codes, and labels.
- **Business Result**: Prevents full pallet scrap & holds. (**Prevents full pallet scrap & holds**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Visual Defect Triager.`
- **Read Tools It Must Call**: `query_camera_vision_inspection_frames, query_vision_defect_classification_results, query_ebhr_batch_record_deviations, query_pneumatic_reject_gate_events`
- **Write-Back Tools It Must Call**: `action_trigger_pneumatic_reject_diverter, action_log_ebhr_quality_deviation`
- **Demo Data Input Values It Reads**:
  - Table `camera_vision_inspection_frames.json` (2 rows): Sample input record has `frame_id=FRAME-CAM01-20261022-00841, camera_station_id=STATION-VISION-LINE01-ENTRY, line_id=LINE-ASEPTIC-01, conveyor_speed_m_s=1.25, capture_timestamp=2026-10-22T04:45:12.180Z`
  - Table `ebhr_batch_record_deviations.json` (1 rows): Sample input record has `deviation_id=DEV-EBHR-20261022-044, batch_number=BATCH-OAT-2026W42-01, product_id=SKU-BEV-OATMILK-ORIGINAL-1L, station_id=STATION-VISION-LINE01-ENTRY, incident_timestamp=2026-10-22T04:45:12Z`
  - Table `pneumatic_reject_gate_events.json` (1 rows): Sample input record has `event_id=REJ-GATE-20261022-00841, frame_id=FRAME-CAM01-20261022-00841, classification_id=CLS-FLASH-VISION-20261022-00841, line_id=LINE-ASEPTIC-01, pneumatic_diverter_id=DIVERTER-SOLENOID-LINE01-A`
  - Table `vision_defect_classification_results.json` (2 rows): Sample input record has `classification_id=CLS-FLASH-VISION-20261022-00841, frame_id=FRAME-CAM01-20261022-00841, defect_type=INDUCTION_FOIL_SEAL_TEAR_MICRO_LEAK, vision_model=gemini-3.8-flash, confidence_score=0.985`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `VisionInspect Inline Optical Defect Classification (Aseptic Line 01)`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `station=Induction Seal Integrity, confidence_pct=98.5, defect_ppm=320 | station=Cap Screw Torque & Flange, confidence_pct=99.1, defect_ppm=45 | station=2D DataMatrix Barcode, confidence_pct=99.8, defect_ppm=12`)
- **Expected Write-Back Receipt**: `{"divert_id": "DIVERT-PNEUM-75BF7ABB", "frame_id": "FRAME-CAM01-20261022-00841", "line_id": "LINE-ASEPTIC-01", "pneumatic_diverter_id": "DIVERTER-SOLENOID-LINE01-A", "defect_type": "INDUCTION_FOIL_SEAL_TEAR_MICRO_LEAK", "actuation_latency_ms": 14.2, "status": "PNEUMATIC_DIVERTER_ACTIVATED", "rationale": "Gemini 3.8 Flash Vision detected radial induction seal tear (1.8mm) with 98.5% confidence. Solenoid diverter fired at 14.2ms latency to isolate non-conforming carton.", "idempotency_key": "DIVERT-20261022-00841-A"}`
- **Expected Markdown Report & Table**:

### 👁️ VisionInspect Inline Quality Inspection & Defect Containment Briefing

> **Executive Summary**: Real-time multimodal optical inspection on **High-Speed Aseptic Packaging Line 01** operating at 1.25 m/s (120 fpm) detected an acute hermetic seal integrity excursion. Under **Gemini 3.8 Flash Vision**, high-resolution frame `FRAME-CAM01-20261022-00841` flagged a **1.8mm radial induction foil seal tear** with **98.5% model confidence** (`CRITICAL_CONTAMINATION_RISK`). In response, the sub-15ms **Pneumatic Solenoid Reject Diverter `DIVERTER-SOLENOID-LINE01-A`** fired in **14.2 ms**, physically segregating the contaminated unit into quarantine bin `REJECT-BIN-LINE01-01` before reaching downstream case packers. In parallel, a 21 CFR Part 11 compliant deviation ticket (`VEEVA-QMS-DEV-99214`) and SAP QM notification (`100084920`) were logged.

#### 📊 High-Speed Vision Classification & Physical Diverter Telemetry (Atomic Copy-Ready Table)

| Frame ID | Inspection Station | Defect Classification | Vision AI Model | Confidence | Divert Latency | Physical Target | Status |
|:---|:---|:---|:---|---:|---:|:---|:---|
| `FRAME-00841` | Induction Seal Integrity | **INDUCTION_FOIL_SEAL_TEAR** | `gemini-3.8-flash` | **98.5%** | **14.2 ms** | `Quarantine Bin 01` | `DIVERTED_CONTAINED` |
| `FRAME-00842` | Induction Seal Integrity | `NONE_CONFORMING` | `gemini-3.8-flash` | 99.8% | N/A (Conforming) | Main Downstream Packer | `IN_SPEC_PASSED` |
| `FRAME-00843` | Cap Screw Torque & Flange | `IN_SPEC_NOMINAL` | `gemini-3.8-flash` | 99.1% | N/A (Conforming) | Main Downstream Packer | `IN_SPEC_PASSED` |

#### ⚡ Automated Inline Diverter Actuation & eBHR Compliance Actions Executed

- **Pneumatic Solenoid Reject Actuated**: `DIVERT-PNEUM-75BF7ABB` | Frame: `FRAME-CAM01-20261022-00841` | Defect: `INDUCTION_FOIL_SEAL_TEAR_MICRO_LEAK` | Latency: `14.2 ms` | Status: `PNEUMATIC_DIVERTER_ACTIVATED`
- **eBHR Quality Deviation Logged**: `DEV-LOG-EBHR-0B1D24DE` | Batch: `BATCH-OAT-2026W42-01` | Severity: `CRITICAL_CONTAINMENT` | QMS Ticket: `VEEVA-QMS-1D24DE` | Status: `EBHR_DEVIATION_LOGGED`

### 🔗 Connected Systems & Industrial Automation Architecture
- **GigE Industrial Vision Array**: 120 FPS high-resolution optical inspection cameras with 4,200 lux LED illumination.
- **Gemini 3.8 Flash Multimodal Classifier**: Sub-50ms zero-shot visual defect localization and normalized bounding box extraction.
- **Modbus TCP / IO-Link Pneumatic Diverter**: Ultra-low latency (<15ms) solenoid mechanical gate diverting defective cartons.
- **Veeva Vault QualityOne & SAP QM**: 21 CFR Part 11 compliant electronic Batch Manufacturing Record (eBHR) deviation audit trail.

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_camera_vision_inspection_frames, query_vision_defect_classification_results` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `VisionInspect Inline Optical Defect Classification (Aseptic Line 01)` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_trigger_pneumatic_reject_diverter` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 29. Batch Record Auditor (`batch_record_auditor`)
- **Pillar / Sub-Pillar**: 03 · Manufacturing & Operations — **Quality & Compliance** · **Persona**: Regulatory Compliance Lead · **ROI**: `60–80% faster batch release review`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Quality & Compliance, Regulatory Compliance Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Batch Record Auditor intervenes.
- **What This Agent Does**: Parses BPR and COA documents to flag pasteurization & CCP deviations.
- **Business Result**: 60–80% faster batch release review. (**60–80% faster batch release review**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Batch Record Auditor.`
- **Read Tools It Must Call**: `query_batch_record_auditor_telemetry_feed, query_batch_record_auditor_constraint_matrix, query_batch_record_auditor_optimization_scenarios, query_batch_record_auditor_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_batch_record_auditor_plan, action_dispatch_batch_record_auditor_alert`
- **Demo Data Input Values It Reads**:
  - Table `batch_record_auditor_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=BATCH_-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Quality & Compliance, capacity_limit=12500`
  - Table `batch_record_auditor_execution_ledger.json` (3 rows): Sample input record has `execution_id=BATCH_-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Regulatory Compliance Lead, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `batch_record_auditor_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=03 · Make | Quality & Compliance, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `batch_record_auditor_telemetry_feed.json` (4 rows): Sample input record has `record_id=BATCH_-TEL-101, company_id=XYZ-CORP-01, category=03 · Manufacturing & Production — Quality & Compliance, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[03 · Make | Quality & Compliance] Batch Record Auditor — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-BATC-F91EA654", "status": "COMMITTED", "category": "03 · Manufacturing & Production — Quality & Compliance", "agent": "[03 · Make | Quality & Compliance] Batch Record Auditor", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "Bounded PLC Recipe Offset Recommendation & Automated SAP QM Usage Decision (BAPI_INSPLOT_SETUSAGEDECISION)"}`
- **Expected Markdown Report & Table**:

#### 📊 [03 · Make | Quality & Compliance] Batch Record Auditor — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `BATCH_-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `03 · Manufacturing & Production — Quality & Compliance` · **Persona**: `Regulatory Compliance Lead` · **Write-Back Receipt**: `ACT-BATC-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_batch_record_auditor_telemetry_feed, query_batch_record_auditor_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[03 · Make | Quality & Compliance] Batch Record Auditor — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_batch_record_auditor_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 30. RCA & CAPA Copilot (`scrap_defect_root_cause_agent`)
- **Pillar / Sub-Pillar**: 03 · Manufacturing & Operations — **Quality & Compliance** · **Persona**: Continuous Improvement Lead · **ROI**: `Speeds 5-Why investigation closures`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Quality & Compliance, Continuous Improvement Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before RCA & CAPA Copilot intervenes.
- **What This Agent Does**: Correlates consumer complaints with ingredient lots and machine telemetry.
- **Business Result**: Speeds 5-Why investigation closures. (**Speeds 5-Why investigation closures**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for RCA & CAPA Copilot.`
- **Read Tools It Must Call**: `query_scrap_loss_pareto_records, query_batch_process_parameter_correlations, query_scrap_financial_cost_ledger, query_scada_setpoint_recommendations`
- **Write-Back Tools It Must Call**: `action_update_scada_recipe_setpoints, action_post_scrap_variance_adjustment`
- **Demo Data Input Values It Reads**:
  - Table `batch_process_parameter_correlations.json` (2 rows): Sample input record has `correlation_id=CORR-FLASH-IMM-02-01, defect_id=DEF-FLASH-IMM-02, parameter_name=Injection Holding Pressure (bar), nominal_setpoint=820.0, actual_observed_mean=945.0`
  - Table `scada_setpoint_recommendations.json` (1 rows): Sample input record has `recommendation_id=REC-SETPOINT-IMM-02-FLASH, asset_id=ASSET-INJECTION-MOLD-02, recipe_name=TETHERED_CAP_PP_HIGH_SPEED_V4, parameter_adjustments=[{'parameter_name': 'Injection Holding Pressure', 'current_val': 945.0, 'recommended_val': 820.0, 'unit': 'bar', 'delta': -125.0}, {'parameter_name': 'Barrel Zone 4 Temperature', 'current_val': 248.5, 'recommended_val': 235.0, 'unit': '°C', 'delta': -13.5}], projected_scrap_rate_after_pct=0.42`
  - Table `scrap_financial_cost_ledger.json` (1 rows): Sample input record has `ledger_id=SCRAP-LEDGER-202610-09, production_order_id=ORD-PROD-202610-771, asset_id=ASSET-INJECTION-MOLD-02, material_id=SKU-BEV-CAP-TETHERED-28MM, scrap_quantity_pieces=2210`
  - Table `scrap_loss_pareto_records.json` (3 rows): Sample input record has `defect_id=DEF-FLASH-IMM-02, defect_name=Parting Line Polymer Flash Excess, asset_id=ASSET-INJECTION-MOLD-02, production_line=LINE-MOLDING-BAY-01, scrap_units=1420`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `YieldMax Scrap Loss Pareto Distribution (Injection Mold IMM-02)`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `defect=Parting Line Flash, scrap_units=1420, cumulative_pct=58.4 | defect=Thermal Warpage, scrap_units=610, cumulative_pct=83.5 | defect=Short Shot Cavity, scrap_units=180, cumulative_pct=91.0`)
- **Expected Write-Back Receipt**: `{"writeback_id": "SCADA-SET-61EE08D8", "recommendation_id": "REC-SETPOINT-IMM-02-FLASH", "asset_id": "ASSET-INJECTION-MOLD-02", "recipe_name": "TETHERED_CAP_PP_HIGH_SPEED_V4", "parameter_updates": {"injection_holding_pressure_bar": 820.0, "barrel_zone_4_temperature_c": 235.0}, "status": "SCADA_PLC_SETPOINTS_LOCKED", "rationale": "Holding pressure spiked to 945 bar (r=0.88 with parting flash). Locking holding pressure setpoint at 820 bar and zone 4 temp at 235°C to restore zero-flash capability.", "idempotency_key": "SCADA-IMM02-202610-001"}`
- **Expected Markdown Report & Table**:

### 🔬 YieldMax Yield Optimization & Scrap Defect Root-Cause Briefing

> **Executive Summary**: Diagnosed an acute scrap spike on **Hydraulic Injection Molding Machine IMM-02** producing tethered beverage caps at Plant Austin. Pareto defect analysis revealed **parting line flash accounted for 58.4% of total scrap** (1,420 scrapped parts, 5.68% scrap rate). Multivariate regression across shopfloor machine telemetry isolated a statistically significant correlation with **Injection Holding Pressure ($r=0.88, p=0.0002$)**, which had drifted to **945 bar** (+125 bar above nominal), overcoming mold clamp tonnage. Wrote back calibrated setpoints directly to **SCADA / PLC** (resetting holding pressure to **820 bar** and melt temperature to **235°C**), reducing projected scrap to **0.42%** and saving **$2,450.00 per shift**, while posting the **$2,806.70** scrap variance to SAP CO.

#### 📊 Scrap Defect Pareto & Multivariate Regression Findings (Atomic Copy-Ready Table)

| Defect Category | Scrap Units | Scrap Rate | Root Cause Variable | Observed vs Nominal | Pearson Correlation ($r$) | Setpoint Writeback | Status |
|:---|---:|---:|:---|:---|:---|:---|:---|
| `Parting Line Flash` | 1,420 pcs | **5.68%** | Injection Holding Pressure | 945 bar (nom 820 bar) | **r = 0.88 (p<0.001)** | `820 bar (Locked)` | `ROOT_CAUSE_ISOLATED` |
| `Thermal Warpage` | 610 pcs | 2.44% | Barrel Zone 4 Melt Temp | 248.5°C (nom 235°C) | **r = 0.74 (p=0.003)** | `235°C (Locked)` | `SECONDARY_RESOLVED` |
| `Short Shot Fill` | 180 pcs | 0.72% | Injection Transfer Position | Nominal | r = 0.12 (p=0.45) | No change required | `MONITORED_IN_SPEC` |

#### ⚡ Automated Process Setpoint Writeback Executed

- **SCADA PLC Setpoints Locked**: `SCADA-SET-61EE08D8` | Asset: `ASSET-INJECTION-MOLD-02` | Recipe: `TETHERED_CAP_PP_HIGH_SPEED_V4` | Parameters: `{'injection_holding_pressure_bar': 820.0, 'barrel_zone_4_temperature_c': 235.0}` | Status: `SCADA_PLC_SETPOINTS_LOCKED`
- **SAP CO Scrap Variance Posted**: `SAP-CO-SCRAP-91D7D841` | Cost Center: `CC-MFG-AUSTIN-MOLD-20` | Financial Loss: **$2,806.70** | Status: `SAP_CO_VARIANCE_POSTED`

### 🔗 Connected Systems & Industrial Automation Architecture
- **Siemens Opcenter MES Scrap Lake**: Real-time scrap logging, defect taxonomy attribution, and Pareto classification.
- **SCADA / PLC Setpoint Bridge**: Bi-directional EtherNet/IP and OPC UA recipe writeback to machine PLC controllers.
- **BigQuery ML Multivariate Regression**: Automated root-cause correlation between process parameters and defect telemetry.
- **SAP S/4HANA Controlling (CO)**: Automated manufacturing variance calculation, GL scrap expense debit, and work order closure.

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_scrap_loss_pareto_records, query_batch_process_parameter_correlations` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `YieldMax Scrap Loss Pareto Distribution (Injection Mold IMM-02)` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_update_scada_recipe_setpoints` without `idempotency_key` triggers `missing_idempotency_key`.

---

## 04 · Logistics & Distribution (12 Agents)

### 31. Load Consolidation (`load_consolidation_agent`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **First & Mid-Mile** · **Persona**: Transport Planner / Inbound Mgr · **ROI**: `12–18% higher trailer fill rate`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In First & Mid-Mile, Transport Planner / Inbound Mgr teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Load Consolidation intervenes.
- **What This Agent Does**: Consolidates vendor LTLs into multi-stop FTL linehauls via cube & weight modeling.
- **Business Result**: 12–18% higher trailer fill rate. (**12–18% higher trailer fill rate**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Load Consolidation.`
- **Read Tools It Must Call**: `query_outbound_shipment_carton_dimensions, query_trailer_bay_geometry_specs, query_lifo_3d_voxel_load_plans, query_axle_weight_crush_audit_logs`
- **Write-Back Tools It Must Call**: `action_commit_3d_lifo_load_plan, action_resequence_dock_staging_lanes`
- **Demo Data Input Values It Reads**:
  - Table `axle_weight_crush_audit_logs.json` (1 rows): Sample input record has `audit_id=AXL-AUD-88, load_plan_id=LP-3D-20261022-88, steer_axle_kg=5120, drive_tandem_kg=14680, trailer_tandem_kg=14210`
  - Table `lifo_3d_voxel_load_plans.json` (1 rows): Sample input record has `load_plan_id=LP-3D-20261022-88, shipment_wave_id=WAVE-3D-20261022-09, trailer_type_id=TRL-53FT-DRYVAN, cube_utilization_pct=92.4, weight_utilization_pct=90.5`
  - Table `outbound_shipment_carton_dimensions.json` (3 rows): Sample input record has `pallet_group_id=PLT-STOP3-HVY01, shipment_wave_id=WAVE-3D-20261022-09, stop_number=3, Stop_Name=San Antonio Depot, length_mm=1200`
  - Table `trailer_bay_geometry_specs.json` (1 rows): Sample input record has `trailer_type_id=TRL-53FT-DRYVAN, internal_length_mm=15900, internal_width_mm=2480, internal_height_mm=2740, max_payload_kg=20400`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `CubeMaster 3D Isometric Bay Utilization & LIFO Zone Fill`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `bay_zone=Zone A (Nose · Stop 3), cube_fill_pct=94.2, weight_kg=6840 | bay_zone=Zone B (Mid · Stop 2), cube_fill_pct=92.8, weight_kg=6320 | bay_zone=Zone C (Tail · Stop 1), cube_fill_pct=90.2, weight_kg=5300`)
- **Expected Write-Back Receipt**: `{"dispatch_execution_id": "CUBE-LP-A0289D84", "load_plan_id": "LP-3D-20261022-88", "trailer_type_id": "TRL-53FT-DRYVAN", "cube_utilization_pct": 92.4, "lifo_zones": ["STOP_3_NOSE_ZONE_A", "STOP_2_MID_ZONE_B", "STOP_1_TAIL_ZONE_C"], "rationale": "Packed 53ft trailer to 92.4% cube utilization in strict reverse-stop LIFO order (Stop 3 nose ➔ Stop 2 mid ➔ Stop 1 tail door) with zero crush violations and DOT-legal axle balance.", "status": "LOAD_PLAN_3D_COMMITTED", "idempotency_key": "CUBE-LP-20261022-01"}`
- **Expected Markdown Report & Table**:

### ✦ CubeMaster 3D — Isometric LIFO Bay & Load Consolidation Studio — Executive Operations Brief

> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **05 · Deliver**.

#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)

| Dimension | Metric Value | Secondary KPI | Execution Mode |
|:---|---:|---:|:---|
| `Zone A (Nose · Stop 3)` | **94.2** | 6840 | `OPTIMIZED_CVRPTW` |
| `Zone B (Mid · Stop 2)` | **92.8** | 6320 | `OPTIMIZED_CVRPTW` |
| `Zone C (Tail · Stop 1)` | **90.2** | 5300 | `OPTIMIZED_CVRPTW` |
| `Legacy Manual Pack` | **68.0** | 12400 | `LEGACY_STATIC` |

#### ⚡ Autonomous Write-Backs & Actions Executed

- **Action Executed**: `CUBE-LP-A0289D84` | Status: `LOAD_PLAN_3D_COMMITTED` | Rationale: Packed 53ft trailer to 92.4% cube utilization in strict reverse-stop LIFO order (Stop 3 nose ➔ Stop 2 mid ➔ Stop 1 tail door) with zero crush violations and DOT-legal axle balance.
- **Action Executed**: `CUBE-STG-DBAF929D` | Status: `DOCK_STAGING_RESEQUENCED` | Rationale: Resequenced dock floor staging lane 08 so forklift loaders load Stop-3 heavy base pallets into the trailer nose first and Stop-1 fragile pallets at the tail door last.

### 🔗 Connected Enterprise Systems
- **Google OR-Tools 3D Extreme-Point & Guillotine Bin Packing Solver** (`C++ / Python 3D Voxel Engine`)
- **SAP EWM & Material Master 3D Carton Geometry & Fragility Feed** (`OData v4 / BAPI`)
- **Fleet Trailer Bay & DOT Axle-Weight Compliance Registry** (`REST / JSON`)
- **Dock Scale & Crush-Pressure Physics Verification Engine** (`IoT Weighbridge / REST`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_outbound_shipment_carton_dimensions, query_trailer_bay_geometry_specs` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `CubeMaster 3D Isometric Bay Utilization & LIFO Zone Fill` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_3d_lifo_load_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 32. Yard Disruption Agent (`yard_dock_sequencer`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **First & Mid-Mile** · **Persona**: Yard Master / Plant Logistics · **ROI**: `Eliminates demurrage & line starvation`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In First & Mid-Mile, Yard Master / Plant Logistics teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Yard Disruption Agent intervenes.
- **What This Agent Does**: Parses GPS & gate feeds to flag delays and reassign dock staging doors dynamically.
- **Business Result**: Eliminates demurrage & line starvation. (**Eliminates demurrage & line starvation**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Yard Disruption Agent.`
- **Read Tools It Must Call**: `query_yard_trailer_geofence_status, query_yard_spotter_move_tasks, query_dock_door_turnaround_schedules, query_carrier_detention_risk_records`
- **Write-Back Tools It Must Call**: `action_dispatch_yard_spotter_move, action_resolve_carrier_detention_alert`
- **Demo Data Input Values It Reads**:
  - Table `carrier_detention_risk_records.json` (1 rows): Sample input record has `record_id=DET-RISK-20261022-01, trailer_id=TRL-SWIFT-7741, carrier_id=CARRIER-SWIFT-TRANS, carrier_name=Swift Transportation, current_dwell_minutes=85.0`
  - Table `dock_door_turnaround_schedules.json` (2 rows): Sample input record has `door_id=DOOR-CROSSDOCK-08, facility_zone=CROSSDOCK_NORTH_QUADRANT, assigned_trailer_id=TRL-SWIFT-7741, door_status=READY_FOR_DOCKING, target_dock_time=2026-10-22T05:50:00Z`
  - Table `yard_spotter_move_tasks.json` (1 rows): Sample input record has `task_id=SPOT-TASK-20261022-012, spotter_truck_id=SPOTTER-HOSTLER-03, operator_name=Marcus Vance, trailer_id=TRL-SWIFT-7741, pickup_slot=SLOT-STAGING-SOUTH-44`
  - Table `yard_trailer_geofence_status.json` (2 rows): Sample input record has `trailer_id=TRL-SWIFT-7741, carrier_id=CARRIER-SWIFT-TRANS, carrier_name=Swift Transportation, yard_id=YARD-DALLAS-02, current_slot_id=SLOT-STAGING-SOUTH-44`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `YardPulse Trailer Turnaround & Detention Demurrage Shield`
  - **Visual Mark Type**: `BAR + RULE` (4 data points: `trailer=TRL-SWIFT-7741, carrier=Swift, dwell_minutes=85.0 | trailer=TRL-JB-HUNT-1204, carrier=J.B. Hunt, dwell_minutes=35.0 | trailer=TRL-SCHNEIDER-882, carrier=Schneider, dwell_minutes=48.0`)
- **Expected Write-Back Receipt**: `{"move_id": "YARD-MOVE-66095D8E", "trailer_id": "TRL-SWIFT-7741", "current_yard_slot": "SLOT-STAGING-SOUTH-44", "target_dock_door": "DOOR-CROSSDOCK-08", "spotter_truck_id": "SPOTTER-HOSTLER-03", "priority": "EXPEDITE_DETENTION_AVOIDANCE", "spotter_job_id": "HOSTLER-JOB-095D8E", "status": "SPOTTER_MOVE_DISPATCHED", "rationale": "Swift trailer TRL-SWIFT-7741 has reached 85 min dwell (only 35 min remaining before 120-min free detention penalty kicks in). Dispatching hostler spotter to pull trailer to Door Crossdock 08 clears trailer within 95 min, avoiding $255 accessorial fee.", "idempotency_key": "SPOT-DISP-20261022-01"}`
- **Expected Markdown Report & Table**:

### 🚛 YardPulse Yard Gate & Turnaround Demurrage Shield Briefing

> **Executive Summary**: Real-time trailer geofencing powered by **Google Maps Fleet Engine** at **Dallas Distribution Center Yard 02** flagged an acute demurrage risk on **Swift Transportation trailer `TRL-SWIFT-7741`**. The trailer had accumulated **85.0 minutes of dwell** in Slot South 44, leaving only **35 minutes** before breaching the carrier's **120-minute free detention threshold** ($85.00/hour demurrage charge). YardPulse dynamically dispatched terminal tractor **`SPOTTER-HOSTLER-03`** under high-priority expedite, moving the trailer to ready **Door Crossdock 08**. Unloading crew Delta-02 was assigned, completing turnaround at **95.0 minutes (25 minutes ahead of cutoff)** and saving **$255.00 in accessorial detention penalties**.

#### 📊 Inbound Trailer Turnaround & Demurrage Risk Telemetry (Atomic Copy-Ready Table)

| Trailer ID | Carrier Name | Current Yard Slot | Assigned Dock Door | Dwell Time | Free Time Remaining | Expedite Action | Detention Penalty Avoided |
|:---|:---|:---|:---|---:|---:|:---|---:|
| `TRL-SWIFT-7741` | Swift Transportation | Slot South 44 | **Door Crossdock 08** | **85.0 min** | **35.0 min** | `SPOTTER_EXPEDITE_DISPATCHED` | **$255.00 (Neutralized)** |
| `TRL-JB-HUNT-1204` | J.B. Hunt | Slot North 12 | Door Outbound 14 | 35.0 min | 85.0 min | `ON_SCHEDULE_LOADING` | $0.00 (In-Spec) |
| `TRL-SCHNEIDER-882` | Schneider National | Slot West 06 | Door Inbound 02 | 48.0 min | 72.0 min | `ON_SCHEDULE_UNLOAD` | $0.00 (In-Spec) |

#### ⚡ Automated Yard Spotter Moves & Demurrage Shield Actions Executed

- **Yard Spotter Hostler Dispatched**: `YARD-MOVE-66095D8E` | Trailer: `TRL-SWIFT-7741` | From: `SLOT-STAGING-SOUTH-44` ➔ To: `DOOR-CROSSDOCK-08` | Tractor: `SPOTTER-HOSTLER-03` | Job: `HOSTLER-JOB-095D8E` | Status: `SPOTTER_MOVE_DISPATCHED`
- **Carrier Detention Alert Neutralized**: `DET-RESOLV-1DFEA825` | Trailer: `TRL-SWIFT-7741` | Carrier: `CARRIER-SWIFT-TRANS` | Turnaround: **95.0 min** | Fee Avoided: **$255.00** | Status: `DETENTION_PENALTY_NEUTRALIZED`

### 🔗 Connected Yard & Fleet Engine Infrastructure
- **Google Maps Fleet Engine**: Sub-second GPS geofence arrival detection, gate wait queues, and yard map layers.
- **Kalmar / TICO Hostler Telematics**: Automated task dispatch, optimal tractor routing, and hook-and-drop confirmation.
- **SAP EWM Yard Management**: Real-time dock door clearance, crew scheduling, and bill-of-lading closing.
- **Carrier Demurrage Rule Engine**: Contractual 2-hour detention threshold monitoring and automated accessorial audit.

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_yard_trailer_geofence_status, query_yard_spotter_move_tasks` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `YardPulse Trailer Turnaround & Detention Demurrage Shield` (`BAR + RULE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_dispatch_yard_spotter_move` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 33. Cold-Chain Auditor (`cold_chain_auditor`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **First & Mid-Mile** · **Persona**: Cold Chain QA / Logistics Dir. · **ROI**: `Prevents perishable food spoilage`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In First & Mid-Mile, Cold Chain QA / Logistics Dir. teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Cold-Chain Auditor intervenes.
- **What This Agent Does**: Analyzes reefer IoT telemetry to flag thermal excursions and file carrier claims.
- **Business Result**: Prevents perishable food spoilage. (**Prevents perishable food spoilage**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Cold-Chain Auditor.`
- **Read Tools It Must Call**: `query_cold_chain_auditor_telemetry_feed, query_cold_chain_auditor_constraint_matrix, query_cold_chain_auditor_optimization_scenarios, query_cold_chain_auditor_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_cold_chain_auditor_plan, action_dispatch_cold_chain_auditor_alert`
- **Demo Data Input Values It Reads**:
  - Table `cold_chain_auditor_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=COLD_C-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=First & Mid-Mile, capacity_limit=12500`
  - Table `cold_chain_auditor_execution_ledger.json` (3 rows): Sample input record has `execution_id=COLD_C-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Cold Chain QA / Logistics Dir., erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `cold_chain_auditor_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=05 · Logistics | First & Mid-Mile, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `cold_chain_auditor_telemetry_feed.json` (4 rows): Sample input record has `record_id=COLD_C-TEL-101, company_id=XYZ-CORP-01, category=05 · Distribution & Logistics — First & Mid-Mile, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[05 · Logistics | First & Mid-Mile] Cold-Chain Auditor — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-COLD-F91EA654", "status": "COMMITTED", "category": "05 · Distribution & Logistics — First & Mid-Mile", "agent": "[05 · Logistics | First & Mid-Mile] Cold-Chain Auditor", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "Automated Carrier Claim Dispute Packet & Approved SAP S/4HANA AP Freight Voucher (BAPI_INCOMINGINVOICE_CREATE)"}`
- **Expected Markdown Report & Table**:

#### 📊 [05 · Logistics | First & Mid-Mile] Cold-Chain Auditor — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `COLD_C-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `05 · Distribution & Logistics — First & Mid-Mile` · **Persona**: `Cold Chain QA / Logistics Dir.` · **Write-Back Receipt**: `ACT-COLD-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_cold_chain_auditor_telemetry_feed, query_cold_chain_auditor_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[05 · Logistics | First & Mid-Mile] Cold-Chain Auditor — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_cold_chain_auditor_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 34. Aisle-Aligned Pallet (`aisle_aligned_pallet_agent`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **Store Replenishment** · **Persona**: Outbound Lead / Industrial Eng. · **ROI**: `Cuts store stocking labor by 20–35%`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Store Replenishment, Outbound Lead / Industrial Eng. teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Aisle-Aligned Pallet intervenes.
- **What This Agent Does**: Sequences DC pick waves to match individual store planograms and shelf layouts.
- **Business Result**: Cuts store stocking labor by 20–35%. (**Cuts store stocking labor by 20–35%**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Aisle-Aligned Pallet.`
- **Read Tools It Must Call**: `query_aisle_aligned_pallet_agent_telemetry_feed, query_aisle_aligned_pallet_agent_constraint_matrix, query_aisle_aligned_pallet_agent_optimization_scenarios, query_aisle_aligned_pallet_agent_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_aisle_aligned_pallet_agent_plan, action_dispatch_aisle_aligned_pallet_agent_alert`
- **Demo Data Input Values It Reads**:
  - Table `aisle_aligned_pallet_agent_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=AISLE_-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Store Replenishment, capacity_limit=12500`
  - Table `aisle_aligned_pallet_agent_execution_ledger.json` (3 rows): Sample input record has `execution_id=AISLE_-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Outbound Lead / Industrial Eng., erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `aisle_aligned_pallet_agent_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=05 · Logistics | Store Replenishment, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `aisle_aligned_pallet_agent_telemetry_feed.json` (4 rows): Sample input record has `record_id=AISLE_-TEL-101, company_id=XYZ-CORP-01, category=05 · Distribution & Logistics — Store Replenishment, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[05 · Logistics | Store Replenishment] Aisle-Aligned Pallet — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-AISL-F91EA654", "status": "COMMITTED", "category": "05 · Distribution & Logistics — Store Replenishment", "agent": "[05 · Logistics | Store Replenishment] Aisle-Aligned Pallet", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "IATA e-AWB (FWB/FHL) Execution, 3D ULD Build-Up Manifest & Airport Ramp Transfer Dispatch"}`
- **Expected Markdown Report & Table**:

#### 📊 [05 · Logistics | Store Replenishment] Aisle-Aligned Pallet — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `AISLE_-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `05 · Distribution & Logistics — Store Replenishment` · **Persona**: `Outbound Lead / Industrial Eng.` · **Write-Back Receipt**: `ACT-AISL-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_aisle_aligned_pallet_agent_telemetry_feed, query_aisle_aligned_pallet_agent_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[05 · Logistics | Store Replenishment] Aisle-Aligned Pallet — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_aisle_aligned_pallet_agent_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 35. Store Capacity Agent (`store_capacity_agent`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **Store Replenishment** · **Persona**: Store Replenishment Lead · **ROI**: `Reduces backroom stock by 25%`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Store Replenishment, Store Replenishment Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Store Capacity Agent intervenes.
- **What This Agent Does**: Throttles push replenishment based on store backroom limits and live POS (Point of Sale — cash-register store scans) velocity.
- **Business Result**: Reduces backroom stock by 25%. (**Reduces backroom stock by 25%**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Store Capacity Agent.`
- **Read Tools It Must Call**: `query_store_capacity_agent_telemetry_feed, query_store_capacity_agent_constraint_matrix, query_store_capacity_agent_optimization_scenarios, query_store_capacity_agent_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_store_capacity_agent_plan, action_dispatch_store_capacity_agent_alert`
- **Demo Data Input Values It Reads**:
  - Table `store_capacity_agent_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=STORE_-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Store Replenishment, capacity_limit=12500`
  - Table `store_capacity_agent_execution_ledger.json` (3 rows): Sample input record has `execution_id=STORE_-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Store Replenishment Lead, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `store_capacity_agent_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=05 · Logistics | Store Replenishment, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `store_capacity_agent_telemetry_feed.json` (4 rows): Sample input record has `record_id=STORE_-TEL-101, company_id=XYZ-CORP-01, category=05 · Distribution & Logistics — Store Replenishment, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[05 · Logistics | Store Replenishment] Store Capacity Agent — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-STOR-F91EA654", "status": "COMMITTED", "category": "05 · Distribution & Logistics — Store Replenishment", "agent": "[05 · Logistics | Store Replenishment] Store Capacity Agent", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "SAP BAPI_MATERIAL_SAVEDATA Safety Stock / ROP Update & STO Lateral Transfer Creation (BAPI_PO_CREATE1)"}`
- **Expected Markdown Report & Table**:

#### 📊 [05 · Logistics | Store Replenishment] Store Capacity Agent — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `STORE_-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `05 · Distribution & Logistics — Store Replenishment` · **Persona**: `Store Replenishment Lead` · **Write-Back Receipt**: `ACT-STOR-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_store_capacity_agent_telemetry_feed, query_store_capacity_agent_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[05 · Logistics | Store Replenishment] Store Capacity Agent — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_store_capacity_agent_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 36. Curfew Orchestrator (`port_drayage_orchestrator`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **Store Replenishment** · **Persona**: Retail Logistics Dispatcher · **ROI**: `98%+ on-time store window compliance`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Store Replenishment, Retail Logistics Dispatcher teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Curfew Orchestrator intervenes.
- **What This Agent Does**: Coordinates municipal delivery curfews and store dock shift schedules dynamically.
- **Business Result**: 98%+ on-time store window compliance. (**98%+ on-time store window compliance**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Curfew Orchestrator.`
- **Read Tools It Must Call**: `query_ocean_vessel_ais_berth_telemetry, query_container_discharge_demurrage_ledger, query_port_terminal_gate_appointments, query_drayage_chassis_transload_allocations`
- **Write-Back Tools It Must Call**: `action_book_dual_transaction_drayage_gate, action_divert_container_to_transload_hub`
- **Demo Data Input Values It Reads**:
  - Table `container_discharge_demurrage_ledger.json` (2 rows): Sample input record has `container_id=MSKU-904812-0, vessel_imo=IMO-9839179, size_type=40HC, stowage_tier=UPPER_DECK_BAY14, last_free_day=2026-10-29`
  - Table `drayage_chassis_transload_allocations.json` (1 rows): Sample input record has `allocation_id=DRAY-LAX-881, container_id=MSKU-904812-0, drayage_carrier_id=PAC-HARBOR-DRAY, chassis_pool_id=DCLI-40HC-991, routing_decision=PORT_TRANSLOAD_TO_53FT_OTR`
  - Table `ocean_vessel_ais_berth_telemetry.json` (1 rows): Sample input record has `vessel_imo=IMO-9839179, vessel_name=MAERSK MC-KINNEY MOLLER, service_loop=TP6_TRANS_PACIFIC, port_of_discharge=USLAX_APM_PIER400, carrier_published_eta=2026-10-25T06:00:00Z`
  - Table `port_terminal_gate_appointments.json` (1 rows): Sample input record has `gate_slot_id=GATE-LAX-20261028-T1, terminal_id=USLAX_APM_PIER400, window_utc=2026-10-28T07:00-09:00Z, transaction_type=DUAL_EMPTY_RETURN_FULL_PICKUP, turn_time_mins=34`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `PortWatch Container Dwell & Demurrage Avoidance`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `container_batch=MSKU-904812 (Transload), dwell_hours=18.0, demurrage_saved_usd=1875 | container_batch=MSKU-904819 (Dual Gate), dwell_hours=26.5, demurrage_saved_usd=1500 | container_batch=CMAU-441029 (Rail Ramp), dwell_hours=31.0, demurrage_saved_usd=1125`)
- **Expected Write-Back Receipt**: `{"dispatch_execution_id": "PORT-GATE-E6BBE6A9", "container_id": "MSKU-904812-0", "terminal_id": "USLAX_APM_PIER400", "gate_slot_id": "GATE-LAX-20261028-T1", "drayage_carrier_id": "PAC-HARBOR-DRAY", "rationale": "Booked dual-transaction Pier 400 gate slot 24 hours prior to Last Free Day using upper-deck discharge prediction, avoiding $1,875 in port demurrage.", "status": "DUAL_DRAYAGE_GATE_BOOKED", "idempotency_key": "PORT-GATE-20261022-01"}`
- **Expected Markdown Report & Table**:

### ✦ PortWatch — Global Ocean Vessel, Container Stowage & Port Drayage Orchestrator — Executive Operations Brief

> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **05 · Deliver**.

#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)

| Dimension | Metric Value | Secondary KPI | Execution Mode |
|:---|---:|---:|:---|
| `MSKU-904812 (Transload)` | **18.0** | 1875 | `OPTIMIZED_CVRPTW` |
| `MSKU-904819 (Dual Gate)` | **26.5** | 1500 | `OPTIMIZED_CVRPTW` |
| `CMAU-441029 (Rail Ramp)` | **31.0** | 1125 | `OPTIMIZED_CVRPTW` |
| `Unmonitored Port Baseline` | **114.0** | 0 | `LEGACY_STATIC` |

#### ⚡ Autonomous Write-Backs & Actions Executed

- **Action Executed**: `PORT-GATE-E6BBE6A9` | Status: `DUAL_DRAYAGE_GATE_BOOKED` | Rationale: Booked dual-transaction Pier 400 gate slot 24 hours prior to Last Free Day using upper-deck discharge prediction, avoiding $1,875 in port demurrage.
- **Action Executed**: `PORT-TRNS-55A0A10A` | Status: `CONTAINER_DIVERTED_TO_TRANSLOAD` | Rationale: WeatherNext 3 detected 60-hour North Pacific swell delay; diverting MSKU-904812-0 from slow inland rail to Carson transload hub saves 4.5 transit days and prevents RDC stockout.

### 🔗 Connected Enterprise Systems
- **Spire Maritime Satellite AIS & Google DeepMind WeatherNext 3 Feed** (`GraphQL / gRPC Stream`)
- **CargoWise One Global Ocean Container & LFD Demurrage Ledger** (`EDI 315 / XML`)
- **Port of LA/LB PierPASS & Rotterdam Terminal Gate Appointment API** (`REST / Webhook`)
- **Google OR-Tools Bipartite Drayage & Transload Allocation Solver** (`Python MILP SDK`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_ocean_vessel_ais_berth_telemetry, query_container_discharge_demurrage_ledger` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `PortWatch Container Dwell & Demurrage Avoidance` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_book_dual_transaction_drayage_gate` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 37. Geocoding Intelligence (`geocoding_intelligence_agent`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **Last-Mile Delivery** · **Persona**: Last-Mile Operations Lead · **ROI**: `Drops failed deliveries by 30–45%`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Last-Mile Delivery, Last-Mile Operations Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Geocoding Intelligence intervenes.
- **What This Agent Does**: Interprets gate codes, apartment delivery notes, and aerial imagery to guide drivers.
- **Business Result**: Drops failed deliveries by 30–45%. (**Drops failed deliveries by 30–45%**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Geocoding Intelligence.`
- **Read Tools It Must Call**: `query_geocoding_intelligence_agent_telemetry_feed, query_geocoding_intelligence_agent_constraint_matrix, query_geocoding_intelligence_agent_optimization_scenarios, query_geocoding_intelligence_agent_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_geocoding_intelligence_agent_plan, action_dispatch_geocoding_intelligence_agent_alert`
- **Demo Data Input Values It Reads**:
  - Table `geocoding_intelligence_agent_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=GEOCOD-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Last-Mile Delivery, capacity_limit=12500`
  - Table `geocoding_intelligence_agent_execution_ledger.json` (3 rows): Sample input record has `execution_id=GEOCOD-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Last-Mile Operations Lead, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `geocoding_intelligence_agent_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=05 · Logistics | Last-Mile Delivery, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `geocoding_intelligence_agent_telemetry_feed.json` (4 rows): Sample input record has `record_id=GEOCOD-TEL-101, company_id=XYZ-CORP-01, category=05 · Distribution & Logistics — Last-Mile Delivery, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[05 · Logistics | Last-Mile Delivery] Geocoding Intelligence — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-GEOC-F91EA654", "status": "COMMITTED", "category": "05 · Distribution & Logistics — Last-Mile Delivery", "agent": "[05 · Logistics | Last-Mile Delivery] Geocoding Intelligence", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "SAP TM / Blue Yonder TMS Load Tender (EDI 204), Google Maps Driver Route Manifest & Live ETA Broadcast"}`
- **Expected Markdown Report & Table**:

#### 📊 [05 · Logistics | Last-Mile Delivery] Geocoding Intelligence — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `GEOCOD-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `05 · Distribution & Logistics — Last-Mile Delivery` · **Persona**: `Last-Mile Operations Lead` · **Write-Back Receipt**: `ACT-GEOC-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_geocoding_intelligence_agent_telemetry_feed, query_geocoding_intelligence_agent_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[05 · Logistics | Last-Mile Delivery] Geocoding Intelligence — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_geocoding_intelligence_agent_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 38. Courier Allocation (`multimodal_mode_shift_agent`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **Last-Mile Delivery** · **Persona**: E-Commerce Logistics Dir. · **ROI**: `Lowers last-mile cost by 8–14%`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Last-Mile Delivery, E-Commerce Logistics Dir. teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Courier Allocation intervenes.
- **What This Agent Does**: Routes parcels dynamically across internal fleet, 3PL, and gig couriers by rate card.
- **Business Result**: Lowers last-mile cost by 8–14%. (**Lowers last-mile cost by 8–14%**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Courier Allocation.`
- **Read Tools It Must Call**: `query_factory_gate_outbound_pos, query_multimodal_corridor_rate_tariff_matrix, query_dynamic_mode_split_recommendations, query_in_transit_mode_diversion_triggers`
- **Write-Back Tools It Must Call**: `action_execute_dynamic_mode_split_booking, action_trigger_mid_route_sea_air_upgrade`
- **Demo Data Input Values It Reads**:
  - Table `dynamic_mode_split_recommendations.json` (1 rows): Sample input record has `split_plan_id=SPLIT-VN-RTM-01, po_id=PO-FAC-VN-88210, base_ocean_units=17000, expedite_sea_air_units=3000, panic_full_air_cost_usd=106200.0`
  - Table `factory_gate_outbound_pos.json` (1 rows): Sample input record has `po_id=PO-FAC-VN-88210, origin_factory=Hai Phong Plant (Vietnam), dest_dc=Rotterdam Euro Hub, total_units=20000, weight_kg=18000`
  - Table `in_transit_mode_diversion_triggers.json` (1 rows): Sample input record has `diversion_id=DIV-SEA-AIR-09, po_id=PO-FAC-VN-88210, transship_hub=DXB_JEBEL_ALI_DWC, units_upgraded_to_air=3000, days_recovered=20`
  - Table `multimodal_corridor_rate_tariff_matrix.json` (3 rows): Sample input record has `mode_code=OCEAN_FCL_SUEZ, transit_days=34, cost_per_kg_usd=0.42, co2e_g_per_tkm=11.2`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `ModalShift Multi-Modal Split vs. Single-Mode Panic Expedite`
  - **Visual Mark Type**: `BAR + LINE` (3 data points: `routing_strategy=ModalShift 85/15 Split, freight_cost_usd=12975, effective_lead_days=14 | routing_strategy=100% Panic Air Charter, freight_cost_usd=106200, effective_lead_days=4 | routing_strategy=100% Slow Ocean (+Stockout), freight_cost_usd=7560, effective_lead_days=34`)
- **Expected Write-Back Receipt**: `{"dispatch_execution_id": "MODAL-SPL-6C3F9AF3", "po_id": "PO-FAC-VN-88210", "primary_mode": "OCEAN_FCL_SUEZ", "primary_units": 17000, "expedite_mode": "SEA_AIR_DXB_HYBRID", "expedite_units": 3000, "rationale": "Splitting PO-FAC-VN-88210 into 85% Ocean FCL (17,000 units) + 15% Dubai Sea-Air bridge (3,000 units) bridges the 9-day Rotterdam stockout gap while saving $93,225 vs. full air expedite.", "status": "DYNAMIC_MODE_SPLIT_BOOKED", "idempotency_key": "MODAL-SPL-20261022-01"}`
- **Expected Markdown Report & Table**:

### ✦ ModalShift — Factory→Ship→Air→Rail→Truck Dynamic Mode-Switch Broker — Executive Operations Brief

> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **05 · Deliver**.

#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)

| Dimension | Metric Value | Secondary KPI | Execution Mode |
|:---|---:|---:|:---|
| `ModalShift 85/15 Split` | **12975** | 14 | `OPTIMIZED_CVRPTW` |
| `100% Panic Air Charter` | **106200** | 4 | `LEGACY_STATIC` |
| `100% Slow Ocean (+Stockout)` | **7560** | 34 | `LEGACY_STATIC` |

#### ⚡ Autonomous Write-Backs & Actions Executed

- **Action Executed**: `MODAL-SPL-6C3F9AF3` | Status: `DYNAMIC_MODE_SPLIT_BOOKED` | Rationale: Splitting PO-FAC-VN-88210 into 85% Ocean FCL (17,000 units) + 15% Dubai Sea-Air bridge (3,000 units) bridges the 9-day Rotterdam stockout gap while saving $93,225 vs. full air expedite.
- **Action Executed**: `MODAL-UPG-D8F876E0` | Status: `MID_ROUTE_SEA_AIR_UPGRADED` | Rationale: Triggered Jebel Ali port-to-DWC airport Sea-Air transshipment for 3,000 critical units, recovering 20 transit days and protecting $142,500 in downstream margin.

### 🔗 Connected Enterprise Systems
- **Google OR-Tools Multi-Modal Cost / Carbon / Stockout Pareto MILP** (`Python MILP SDK`)
- **SAP IBP & Cloud Spanner Downstream Hub Stockout Exposure Feed** (`OData v4 / Spanner SQL`)
- **CargoWise & Xeneta Multi-Modal Spot/Contract Tariff & Transit Matrix** (`REST API`)
- **Dubai / LAX / Singapore Sea-Air Transshipment Hub Orchestrator** (`EDI 315 / ONE Record`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_factory_gate_outbound_pos, query_multimodal_corridor_rate_tariff_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `ModalShift Multi-Modal Split vs. Single-Mode Panic Expedite` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_execute_dynamic_mode_split_booking` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 39. Delivery Exception Copilot (`otif_penalty_shield`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **Last-Mile Delivery** · **Persona**: Customer Support Ops Lead · **ROI**: `Decreases WISMO calls by up to 60%`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Last-Mile Delivery, Customer Support Ops Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Delivery Exception Copilot intervenes.
- **What This Agent Does**: Detects en-route exceptions and updates customers proactively with reschedule links.
- **Business Result**: Decreases WISMO calls by up to 60%. (**Decreases WISMO calls by up to 60%**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Delivery Exception Copilot.`
- **Read Tools It Must Call**: `query_open_retail_customer_orders_sla, query_predicted_otif_breach_alerts, query_retailer_otif_chargeback_deductions, query_geofence_edi856_dispute_dossiers`
- **Write-Back Tools It Must Call**: `action_execute_otif_sla_rescue_intervention, action_submit_chargeback_dispute_dossier`
- **Demo Data Input Values It Reads**:
  - Table `geofence_edi856_dispute_dossiers.json` (1 rows): Sample input record has `dossier_id=DOS-OTIF-44910, deduction_id=DED-RET01-44910, mabd_cutoff_utc=2026-10-18T16:00:00Z, google_maps_geofence_entry_utc=2026-10-18T14:12:00Z, edi856_asn_timestamp=2026-10-17T08:00:00Z`
  - Table `open_retail_customer_orders_sla.json` (1 rows): Sample input record has `order_id=SO-WMT-20261022-881, customer_id=BIGBOX-RETAIL-01, order_value_usd=420000.0, mabd_window_utc=2026-10-25T14:00:00Z, otif_penalty_pct=3.0`
  - Table `predicted_otif_breach_alerts.json` (1 rows): Sample input record has `alert_id=OTIF-ALT-881, order_id=SO-WMT-20261022-881, breach_probability=0.78, root_cause=PRIMARY_DC_WAVE_BACKLOG_6HRS, rescue_option=PRIORITY_DOCK_RELEASE_AND_TEAM_DRIVER`
  - Table `retailer_otif_chargeback_deductions.json` (1 rows): Sample input record has `deduction_id=DED-RET01-44910, customer_id=BIGBOX-RETAIL-01, shipment_id=SHP-WMT-4012, claimed_reason=LATE_ARRIVAL_PAST_MABD, deducted_amount_usd=9450.0`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `OTIFShield Penalty Prevention & Chargeback Recovery`
  - **Visual Mark Type**: `BAR + LINE` (3 data points: `key_account=BigBox Retail #01 (OTIFShield), otif_pct=99.2, penalties_saved_usd=22050 | key_account=National Grocer #02 (OTIFShield), otif_pct=98.9, penalties_saved_usd=16800 | key_account=Reactive Post-Mortem Baseline, otif_pct=93.4, penalties_saved_usd=0`)
- **Expected Write-Back Receipt**: `{"dispatch_execution_id": "OTIF-RSC-0CA3068F", "order_id": "SO-WMT-20261022-881", "customer_id": "BIGBOX-RETAIL-01", "rescue_option": "PRIORITY_DOCK_RELEASE_AND_TEAM_DRIVER", "penalty_avoided_usd": 12600.0, "rationale": "Predicted 78% MABD breach risk 72 hours early; spent $650 on priority dock wave release to avoid a $12,600 (3% COGS) retail OTIF chargeback.", "status": "OTIF_SLA_RESCUE_EXECUTED", "idempotency_key": "OTIF-RSC-20261022-01"}`
- **Expected Markdown Report & Table**:

### ✦ OTIFShield — Customer SLA Rescue & Chargeback Dispute Agent — Executive Operations Brief

> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **06 · Return & Enable**.

#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)

| Dimension | Metric Value | Secondary KPI | Execution Mode |
|:---|---:|---:|:---|
| `BigBox Retail #01 (OTIFShield)` | **99.2** | 22050 | `OPTIMIZED_CVRPTW` |
| `National Grocer #02 (OTIFShield)` | **98.9** | 16800 | `OPTIMIZED_CVRPTW` |
| `Reactive Post-Mortem Baseline` | **93.4** | 0 | `LEGACY_STATIC` |

#### ⚡ Autonomous Write-Backs & Actions Executed

- **Action Executed**: `OTIF-RSC-0CA3068F` | Status: `OTIF_SLA_RESCUE_EXECUTED` | Rationale: Predicted 78% MABD breach risk 72 hours early; spent $650 on priority dock wave release to avoid a $12,600 (3% COGS) retail OTIF chargeback.
- **Action Executed**: `OTIF-DSP-7C673239` | Status: `CHARGEBACK_DISPUTE_SUBMITTED` | Rationale: Auto-compiled Google Maps geofence gate entry (14:12 UTC vs 16:00 UTC MABD cutoff), EDI 856 ASN, and signed ePOD to overturn invalid $9,450 late-arrival chargeback.

### 🔗 Connected Enterprise Systems
- **Vertex AI 72-Hour Customer MABD & OTIF Breach Risk Scorer** (`BigQuery ML / Spanner`)
- **Walmart Retail Link / Target Partners Online Deduction Feed** (`EDI 812 / Portal API`)
- **Google Maps Geofence + EDI 856 ASN + Signed ePOD Evidence Compiler** (`Document AI / GIS`)
- **SAP S/4HANA SD Priority Wave & Alternate Hub Split-Ship Broker** (`OData v4`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_open_retail_customer_orders_sla, query_predicted_otif_breach_alerts` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `OTIFShield Penalty Prevention & Chargeback Recovery` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_execute_otif_sla_rescue_intervention` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 40. Dynamic Rerouter (`fleetflow_dispatch`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **Route & Carrier** · **Persona**: Fleet Dispatcher / Central Ops · **ROI**: `Cuts fleet fuel usage by 6–10%`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Route & Carrier, Fleet Dispatcher / Central Ops teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Dynamic Rerouter intervenes.
- **What This Agent Does**: Recalculates multi-stop routes using live Google Maps traffic, radar, and bridge limits.
- **Business Result**: Cuts fleet fuel usage by 6–10%. (**Cuts fleet fuel usage by 6–10%**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Dynamic Rerouter.`
- **Read Tools It Must Call**: `query_corridor_delivery_orders, query_fleet_vehicle_telematics_hos, query_google_maps_corridor_routes, query_backhaul_consolidation_opportunities`
- **Write-Back Tools It Must Call**: `action_dispatch_corridor_route_manifest, action_assign_backhaul_return_load`
- **Demo Data Input Values It Reads**:
  - Table `backhaul_consolidation_opportunities.json` (1 rows): Sample input record has `backhaul_id=BKH-SAT-DAL-44, origin_hub=San Antonio Vendor Park, destination_dc=Dallas Central RDC, weight_kg=14200, pallets=22`
  - Table `corridor_delivery_orders.json` (3 rows): Sample input record has `order_id=ORD-FF-901, corridor_id=CORR-I35-TEX, customer_hub=Austin Supercenter #14, stop_sequence=1, weight_kg=4850`
  - Table `fleet_vehicle_telematics_hos.json` (2 rows): Sample input record has `vehicle_id=TRK-24T-TX08, vehicle_class=24t_Class8_Heavy_Tractor, max_payload_kg=21500, max_cube_m3=82.0, driver_hos_remaining_hrs=9.8`
  - Table `google_maps_corridor_routes.json` (2 rows): Sample input record has `route_id=RTE-I35-20261022-01, corridor_id=CORR-I35-TEX, assigned_vehicle_id=TRK-24T-TX08, total_distance_km=462.5, baseline_distance_km=574.0`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `FleetFlow Corridor Route Optimization & Deadhead Reduction`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `corridor=I-35 Dallas➔San Antonio, distance_km=462.5, cube_fill_pct=91.4 | corridor=I-35 Legacy Postcode, distance_km=574.0, cube_fill_pct=67.0 | corridor=I-45 Dallas➔Houston, distance_km=388.0, cube_fill_pct=89.2`)
- **Expected Write-Back Receipt**: `{"dispatch_execution_id": "FF-DISP-5CE0787F", "route_id": "RTE-I35-20261022-01", "vehicle_id": "TRK-24T-TX08", "corridor_id": "CORR-I35-TEX", "stop_count": 3, "rationale": "OR-Tools CVRPTW + Google Maps Routes Preferred solved 3-stop I-35 corridor route (18,450 kg / 72.3 m3) cutting stem distance by 19.4% with 99.4% SLA confidence.", "status": "CORRIDOR_ROUTE_DISPATCHED", "idempotency_key": "FF-DISP-20261022-01"}`
- **Expected Markdown Report & Table**:

### ✦ FleetFlow — Google Maps Corridor Route & Fleet Dispatch Studio — Executive Operations Brief

> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **05 · Deliver**.

#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)

| Dimension | Metric Value | Secondary KPI | Execution Mode |
|:---|---:|---:|:---|
| `I-35 Dallas➔San Antonio` | **462.5** | 91.4 | `OPTIMIZED_CVRPTW` |
| `I-35 Legacy Postcode` | **574.0** | 67.0 | `LEGACY_STATIC` |
| `I-45 Dallas➔Houston` | **388.0** | 89.2 | `OPTIMIZED_CVRPTW` |
| `I-10 Houston➔El Paso` | **1190.0** | 93.8 | `OPTIMIZED_CVRPTW` |

#### ⚡ Autonomous Write-Backs & Actions Executed

- **Action Executed**: `FF-DISP-5CE0787F` | Status: `CORRIDOR_ROUTE_DISPATCHED` | Rationale: OR-Tools CVRPTW + Google Maps Routes Preferred solved 3-stop I-35 corridor route (18,450 kg / 72.3 m3) cutting stem distance by 19.4% with 99.4% SLA confidence.
- **Action Executed**: `FF-BKH-CD884A35` | Status: `BACKHAUL_RETURN_ASSIGNED` | Rationale: Matched returning 24t tractor TRK-24T-TX08 with 22-pallet vendor backhaul in San Antonio, eliminating 274 empty return miles and saving $1,480.

### 🔗 Connected Enterprise Systems
- **Google Maps Platform Routes Preferred & Live Traffic Matrix API** (`gRPC / REST v2`)
- **Google OR-Tools Capacitated Vehicle Routing (CVRPTW) Engine** (`C++ / Python Solver SDK`)
- **Samsara ELD & Google Maps Fleet Engine Vehicle Telemetry** (`Webhook / MQTT`)
- **Blue Yonder TMS Backhaul & Deadhead Elimination Broker** (`OData / EDI 204`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_corridor_delivery_orders, query_fleet_vehicle_telematics_hos` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `FleetFlow Corridor Route Optimization & Deadhead Reduction` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_dispatch_corridor_route_manifest` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 41. Routing Guide Compliance (`freight_control_tower`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **Route & Carrier** · **Persona**: Transport Procurement Lead · **ROI**: `Reduces spot freight by 15–20%`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Route & Carrier, Transport Procurement Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Routing Guide Compliance intervenes.
- **What This Agent Does**: Tracks carrier tender acceptance & OTIF (On-Time In-Full — delivering 100% of ordered units before the deadline) to reprioritize waterfall routing guides.
- **Business Result**: Reduces spot freight by 15–20%. (**Reduces spot freight by 15–20%**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Routing Guide Compliance.`
- **Read Tools It Must Call**: `query_in_transit_multimodal_telemetry, query_cold_chain_thermal_excursion_alerts, query_carrier_edi210_freight_invoices, query_freight_audit_discrepancy_ledger`
- **Write-Back Tools It Must Call**: `action_reroute_in_transit_reefer_shipment, action_issue_freight_audit_debit_adjustment`
- **Demo Data Input Values It Reads**:
  - Table `carrier_edi210_freight_invoices.json` (1 rows): Sample input record has `invoice_id=INV-EDI210-77410, carrier_id=KNIGHT-SWIFT-TL, shipment_id=SHP-DRY-5519, billed_amount_usd=3490.0, billed_detention_hrs=4.5`
  - Table `cold_chain_thermal_excursion_alerts.json` (1 rows): Sample input record has `alert_id=THRM-ALT-8841, shipment_id=SHP-REEF-8841, cargo_value_at_risk_usd=148000.0, nearest_cold_crossdock=DES_MOINES_COLD_HUB_04, distance_to_hub_km=24.5`
  - Table `freight_audit_discrepancy_ledger.json` (1 rows): Sample input record has `audit_id=FAUD-77410, invoice_id=INV-EDI210-77410, geofence_verified_dwell_hrs=1.2, contract_free_time_hrs=2.0, contract_fsc_pct=28.5`
  - Table `in_transit_multimodal_telemetry.json` (1 rows): Sample input record has `shipment_id=SHP-REEF-8841, carrier_id=PRIME-REEFER-INC, corridor=I-80 Omaha➔Chicago, cargo_type=CHILLED_PROTEIN_2C, setpoint_c=2.0`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `SentinelMove 3-Way Freight Bill Audit & Cold-Chain Rescue`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `invoice_batch=INV-77410 (Detention+FSC), billed_usd=3490, overcharge_saved_usd=615 | invoice_batch=INV-77418 (Mileage Audit), billed_usd=4120, overcharge_saved_usd=485 | invoice_batch=INV-77425 (Accessorial), billed_usd=2890, overcharge_saved_usd=390`)
- **Expected Write-Back Receipt**: `{"dispatch_execution_id": "SENT-DIV-8B2A19FA", "shipment_id": "SHP-REEF-8841", "diversion_hub_id": "DES_MOINES_COLD_HUB_04", "cargo_value_protected_usd": 148000.0, "rationale": "IoT telemetry detected compressor coolant pressure drop (+3.4°C drift) 52 minutes before excursion limit; diverted SHP-REEF-8841 to Des Moines Cold Hub (24.5 km) for cross-dock into backup reefer, saving $148,000 cargo.", "status": "REEFER_DIVERTED_TO_COLD_HUB", "idempotency_key": "SENT-DIV-20261022-01"}`
- **Expected Markdown Report & Table**:

### ✦ SentinelMove — Multi-Modal In-Transit Control Tower & Freight Auditor — Executive Operations Brief

> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **05 · Deliver**.

#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)

| Dimension | Metric Value | Secondary KPI | Execution Mode |
|:---|---:|---:|:---|
| `INV-77410 (Detention+FSC)` | **3490** | 615 | `OPTIMIZED_CVRPTW` |
| `INV-77418 (Mileage Audit)` | **4120** | 485 | `OPTIMIZED_CVRPTW` |
| `INV-77425 (Accessorial)` | **2890** | 390 | `OPTIMIZED_CVRPTW` |
| `Un-Audited Auto-Pay` | **3490** | 0 | `LEGACY_STATIC` |

#### ⚡ Autonomous Write-Backs & Actions Executed

- **Action Executed**: `SENT-DIV-8B2A19FA` | Status: `REEFER_DIVERTED_TO_COLD_HUB` | Rationale: IoT telemetry detected compressor coolant pressure drop (+3.4°C drift) 52 minutes before excursion limit; diverted SHP-REEF-8841 to Des Moines Cold Hub (24.5 km) for cross-dock into backup reefer, saving $148,000 cargo.
- **Action Executed**: `SENT-AUD-2CA32A20` | Status: `FREIGHT_INVOICE_ADJUSTED` | Rationale: Google Maps dock geofence proved trailer dwell was 1.2 hrs (within 2.0 hr free window) and contract DOE fuel index is 28.5%; auto-deducted $615.00 overcharge prior to SAP AP release.

### 🔗 Connected Enterprise Systems
- **Project44 / FourKites Real-Time GPS & Cold-Chain IoT Stream** (`Webhook / REST v4`)
- **Google Maps Platform Dock Geofence Timestamp & Detention Verifier** (`REST / BigQuery GIS`)
- **Google Cloud Document AI & EDI 210 3-Way Freight Invoice Auditor** (`gRPC / EDI 210`)
- **SAP S/4HANA TM/AP Automated Freight Settlement & Debit Memo Engine** (`OData v4`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_in_transit_multimodal_telemetry, query_cold_chain_thermal_excursion_alerts` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `SentinelMove 3-Way Freight Bill Audit & Cold-Chain Rescue` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_reroute_in_transit_reefer_shipment` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 42. Freight Bill Audit Agent (`freight_bill_audit_agent`)
- **Pillar / Sub-Pillar**: 04 · Logistics & Distribution — **Route & Carrier** · **Persona**: Freight Controller / Claims · **ROI**: `Captures 3–7% in overbilled fees`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Route & Carrier, Freight Controller / Claims teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Freight Bill Audit Agent intervenes.
- **What This Agent Does**: Extracts signed PODs and rate contracts via OCR to audit accessorial surcharges.
- **Business Result**: Captures 3–7% in overbilled fees. (**Captures 3–7% in overbilled fees**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Freight Bill Audit Agent.`
- **Read Tools It Must Call**: `query_freight_bill_audit_agent_telemetry_feed, query_freight_bill_audit_agent_constraint_matrix, query_freight_bill_audit_agent_optimization_scenarios, query_freight_bill_audit_agent_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_freight_bill_audit_agent_plan, action_dispatch_freight_bill_audit_agent_alert`
- **Demo Data Input Values It Reads**:
  - Table `freight_bill_audit_agent_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=FREIGH-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Route & Carrier, capacity_limit=12500`
  - Table `freight_bill_audit_agent_execution_ledger.json` (3 rows): Sample input record has `execution_id=FREIGH-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Freight Controller / Claims, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `freight_bill_audit_agent_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=05 · Logistics | Route & Carrier, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `freight_bill_audit_agent_telemetry_feed.json` (4 rows): Sample input record has `record_id=FREIGH-TEL-101, company_id=XYZ-CORP-01, category=05 · Distribution & Logistics — Route & Carrier, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[05 · Logistics | Route & Carrier] Freight Bill Audit Agent — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-FREI-F91EA654", "status": "COMMITTED", "category": "05 · Distribution & Logistics — Route & Carrier", "agent": "[05 · Logistics | Route & Carrier] Freight Bill Audit Agent", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "Automated Carrier Claim Dispute Packet & Approved SAP S/4HANA AP Freight Voucher (BAPI_INCOMINGINVOICE_CREATE)"}`
- **Expected Markdown Report & Table**:

#### 📊 [05 · Logistics | Route & Carrier] Freight Bill Audit Agent — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `FREIGH-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `05 · Distribution & Logistics — Route & Carrier` · **Persona**: `Freight Controller / Claims` · **Write-Back Receipt**: `ACT-FREI-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_freight_bill_audit_agent_telemetry_feed, query_freight_bill_audit_agent_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[05 · Logistics | Route & Carrier] Freight Bill Audit Agent — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_freight_bill_audit_agent_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

## 05 · Inventory & Warehousing (9 Agents)

### 43. Safety Stock Agent (`meio_safety_stock_agent`)
- **Pillar / Sub-Pillar**: 05 · Inventory & Warehousing — **Positioning & Optimization** · **Persona**: Inventory Optimization Lead · **ROI**: `Cuts working capital by 10–18%`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Positioning & Optimization, Inventory Optimization Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Safety Stock Agent intervenes.
- **What This Agent Does**: Recalibrates multi-echelon buffers using live lead-time and demand variance.
- **Business Result**: Cuts working capital by 10–18%. (**Cuts working capital by 10–18%**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Safety Stock Agent.`
- **Read Tools It Must Call**: `query_multi_echelon_safety_stock_recommendations, query_dc_inventory_echelon_balances, query_lateral_dc_rebalance_transfers, query_echelon_service_level_projections`
- **Write-Back Tools It Must Call**: `action_execute_lateral_dc_rebalance, action_update_echelon_safety_stock_policy`
- **Demo Data Input Values It Reads**:
  - Table `dc_inventory_echelon_balances.json` (3 rows): Sample input record has `dc_id=CDC-CHICAGO-01, dc_name=Midwest Central Distribution Center, echelon_tier=TIER_1_CENTRAL_DC, sku_id=SKU-BEV-OATMILK-ORIGINAL-1L, on_hand_inventory_units=68400`
  - Table `echelon_service_level_projections.json` (1 rows): Sample input record has `projection_id=SL-PROJ-202610-001, sku_id=SKU-BEV-OATMILK-ORIGINAL-1L, network_node_id=RDC-DALLAS-02, days_of_supply_baseline=3.8, stockout_probability_without_rebalance_pct=34.2`
  - Table `lateral_dc_rebalance_transfers.json` (1 rows): Sample input record has `transfer_id=REBAL-TRANSFER-202610-001, sku_id=SKU-BEV-OATMILK-ORIGINAL-1L, source_dc_id=CDC-CHICAGO-01, destination_dc_id=RDC-DALLAS-02, quantity_transferred_units=6500`
  - Table `multi_echelon_safety_stock_recommendations.json` (2 rows): Sample input record has `recommendation_id=MEIO-REC-202610-001, sku_id=SKU-BEV-OATMILK-ORIGINAL-1L, sku_description=Barista Organic Oat Milk 1L Tetra, echelon_tier=TIER_1_CENTRAL_DC, network_node_id=CDC-CHICAGO-01`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `EchelonFlow Multi-Echelon Stock & Safety Buffer Positioning`
  - **Visual Mark Type**: `BAR + TICK` (4 data points: `node=CDC Chicago (Tier 1), current_stock=68400, optimal_safety_stock=32000 | node=RDC Dallas (Tier 2), current_stock=7200, optimal_safety_stock=14200 | node=RDC Atlanta (Tier 2), current_stock=24500, optimal_safety_stock=11000`)
- **Expected Write-Back Receipt**: `{"rebalance_transfer_id": "REBAL-TRF-9A95179E", "source_dc_id": "CDC-CHICAGO-01", "destination_dc_id": "RDC-DALLAS-02", "sku_id": "SKU-BEV-OATMILK-ORIGINAL-1L", "transfer_quantity_units": 6500, "otm_shipment_id": "OTM-SHP-95179E", "status": "LATERAL_REBALANCE_DISPATCHED", "rationale": "RDC Dallas stock dropped to 3.8 days of supply (34.2% stockout probability). Dispatching 6,500 units from surplus stock at CDC Chicago avoids $18,500 in lost margin against $1,420 freight cost (13.0x ROI).", "idempotency_key": "REBAL-ORD-20261022-01"}`
- **Expected Markdown Report & Table**:

### 📦 EchelonFlow Multi-Echelon Inventory Optimization (MEIO) Briefing

> **Executive Summary**: Executed Clark-Scarf multi-echelon stochastic inventory rebalancing across the fulfillment network for **Barista Organic Oat Milk 1L Tetra**. Identified an acute imbalance: **RDC Dallas (Tier 2)** was operating at critical risk with only **3.8 days of supply** and a **34.2% stockout probability** ($18,500 at-risk sales margin), while **CDC Chicago (Tier 1)** held a substantial surplus of **68,400 units (28.5 days of supply)**. Dispatched a **6,500-unit lateral transshipment** from Chicago to Dallas via dedicated dry van ($1,420 freight cost, delivering **13.0x net ROI** and securing a **98.6% customer SLA**). Simultaneously updated SAP IBP safety stock policy, reducing central pooling buffer from 45,000 to 32,000 units to unlock **$38,480 in working capital**.

#### 📊 Multi-Echelon Stock Positions & Rebalance Telemetry (Atomic Copy-Ready Table)

| Echelon Node | Node Tier | On-Hand Stock | Days of Supply | Optimal Buffer | Delta Units | Rebalance Action | Stockout Risk |
|:---|:---|---:|---:|---:|---:|:---|:---|
| `CDC-CHICAGO-01` | Central DC (Tier 1) | 68,400 units | 28.5 days | 32,000 units | **-13,000 units** | `DISPATCH_LATERAL_SOURCE` | 0.2% (Protected) |
| `RDC-DALLAS-02` | Regional DC (Tier 2) | 7,200 units | **3.8 days** | 14,200 units | **+6,500 units** | `LATERAL_TRANSFER_RECEIPT` | **0.8% (Averted from 34.2%)** |
| `RDC-ATLANTA-03` | Regional DC (Tier 2) | 24,500 units | 18.2 days | 11,000 units | 0 units | `MAINTAIN_CURRENT_POLICY` | 1.1% (In-Spec) |
| `FDC-AUSTIN-04` | Forward DC (Tier 3) | 4,100 units | 12.0 days | 4,500 units | 0 units | `MAINTAIN_CURRENT_POLICY` | 1.4% (In-Spec) |

#### ⚡ Automated Logistics & SAP IBP Policy Mutations Executed

- **Lateral Transshipment Dispatched**: `REBAL-TRF-9A95179E` | From: `CDC-CHICAGO-01` ➔ To: `RDC-DALLAS-02` | Qty: **6,500 units** | OTM ID: `OTM-SHP-95179E` | Status: `LATERAL_REBALANCE_DISPATCHED`
- **SAP IBP Safety Stock Policy Updated**: `MEIO-POL-13DEA677` | Tier: `TIER_1_CENTRAL_DC` | SKU: `SKU-BEV-OATMILK-ORIGINAL-1L` | New Buffer: **32,000 units** | IBP Job: `IBP-JOB-DEA677` | Status: `MEIO_SAFETY_STOCK_POLICY_UPDATED`

### 🔗 Connected Systems & Optimization Architecture
- **SAP IBP for MEIO**: Clark-Scarf stochastic multi-echelon positioning and service level target synchronization.
- **Manhattan Active WMS**: Real-time perpetual inventory balances, dock receipts, and allocated order queues.
- **Oracle OTM Lateral Dispatcher**: Automated freight rating, carrier dispatch, and cross-DC EDI 204 tender.
- **BigQuery ML Monte Carlo Engine**: Stochastic simulation of lead-time variance and stockout probability curves.

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_multi_echelon_safety_stock_recommendations, query_dc_inventory_echelon_balances` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `EchelonFlow Multi-Echelon Stock & Safety Buffer Positioning` (`BAR + TICK`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_execute_lateral_dc_rebalance` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 44. SLOB Disposition Agent (`slob_disposition_agent`)
- **Pillar / Sub-Pillar**: 05 · Inventory & Warehousing — **Positioning & Optimization** · **Persona**: Inventory Controller / Buyer · **ROI**: `Prevents expired stock write-offs`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Positioning & Optimization, Inventory Controller / Buyer teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before SLOB (Slow-Moving & Obsolete inventory sitting unsold) Disposition Agent intervenes.
- **What This Agent Does**: Analyzes shelf-life risk and triggers promotional bundles or liquidations.
- **Business Result**: Prevents expired stock write-offs. (**Prevents expired stock write-offs**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for SLOB Disposition Agent.`
- **Read Tools It Must Call**: `query_slob_disposition_agent_telemetry_feed, query_slob_disposition_agent_constraint_matrix, query_slob_disposition_agent_optimization_scenarios, query_slob_disposition_agent_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_slob_disposition_agent_plan, action_dispatch_slob_disposition_agent_alert`
- **Demo Data Input Values It Reads**:
  - Table `slob_disposition_agent_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=SLOB_D-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Positioning & Optimization, capacity_limit=12500`
  - Table `slob_disposition_agent_execution_ledger.json` (3 rows): Sample input record has `execution_id=SLOB_D-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Inventory Controller / Buyer, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `slob_disposition_agent_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=04 · Inventory & DC | Positioning & Optimization, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `slob_disposition_agent_telemetry_feed.json` (4 rows): Sample input record has `record_id=SLOB_D-TEL-101, company_id=XYZ-CORP-01, category=04 · Inventory & Warehousing — Positioning & Optimization, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[04 · Inventory & DC | Positioning & Optimization] SLOB Disposition Agent — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-SLOB-F91EA654", "status": "COMMITTED", "category": "04 · Inventory & Warehousing — Positioning & Optimization", "agent": "[04 · Inventory & DC | Positioning & Optimization] SLOB Disposition Agent", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "SAP BAPI_MATERIAL_SAVEDATA Safety Stock / ROP Update & STO Lateral Transfer Creation (BAPI_PO_CREATE1)"}`
- **Expected Markdown Report & Table**:

#### 📊 [04 · Inventory & DC | Positioning & Optimization] SLOB Disposition Agent — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `SLOB_D-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `04 · Inventory & Warehousing — Positioning & Optimization` · **Persona**: `Inventory Controller / Buyer` · **Write-Back Receipt**: `ACT-SLOB-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_slob_disposition_agent_telemetry_feed, query_slob_disposition_agent_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[04 · Inventory & DC | Positioning & Optimization] SLOB Disposition Agent — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_slob_disposition_agent_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 45. Inter-Facility Rebalancer (`crossdock_transfer_orchestrator`)
- **Pillar / Sub-Pillar**: 05 · Inventory & Warehousing — **Positioning & Optimization** · **Persona**: Replenishment Planner · **ROI**: `Eliminates regional out-of-stocks`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Positioning & Optimization, Replenishment Planner teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Inter-Facility Rebalancer intervenes.
- **What This Agent Does**: Generates automated inter-DC and store transfers to balance localized gluts.
- **Business Result**: Eliminates regional out-of-stocks. (**Eliminates regional out-of-stocks**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Inter-Facility Rebalancer.`
- **Read Tools It Must Call**: `query_inbound_outbound_crossdock_manifests, query_inbound_carrier_eta_milestones, query_outbound_trailer_bay_assignments, query_crossdock_dwell_time_records`
- **Write-Back Tools It Must Call**: `action_dispatch_direct_crossdock_transfer, action_hold_pallet_for_staging_buffer`
- **Demo Data Input Values It Reads**:
  - Table `crossdock_dwell_time_records.json` (2 rows): Sample input record has `record_id=XDOCK-DWELL-20261022-01, pallet_id=PLT-OAT-9921-01, inbound_door_id=DOOR-INBOUND-04, outbound_bay_id=BAY-OUTBOUND-12, dwell_time_minutes=18.5`
  - Table `inbound_carrier_eta_milestones.json` (1 rows): Sample input record has `shipment_id=SHP-SWIFT-20261022-9921, carrier_id=CARRIER-SWIFT-TRANS, trailer_id=TRL-INB-SWIFT-9921, geofence_arrival_timestamp=2026-10-22T05:15:00Z, dock_checkin_timestamp=2026-10-22T05:22:00Z`
  - Table `inbound_outbound_crossdock_manifests.json` (1 rows): Sample input record has `manifest_id=XDOCK-MNF-20261022-041, inbound_trailer_id=TRL-INB-SWIFT-9921, supplier_id=SUP-OATLY-PLANT-01, carrier_name=Swift Transportation, inbound_door_id=DOOR-INBOUND-04`
  - Table `outbound_trailer_bay_assignments.json` (2 rows): Sample input record has `bay_id=BAY-OUTBOUND-12, outbound_trailer_id=TRL-OUT-JB-HUNT-4481, carrier_name=J.B. Hunt Transport, destination_dc=RDC-HOUSTON-05, route_code=RTE-TX-SOUTH-HOU-01`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `CrossDockFlow Inbound-to-Outbound Direct Pallet Transfer`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `door_route=Door 04 ➔ Bay 12 (Houston), dwell_minutes=18.5, pallets=10 | door_route=Door 04 ➔ Bay 14 (Austin), dwell_minutes=22.0, pallets=8 | door_route=Door 02 ➔ Bay 08 (Dallas), dwell_minutes=25.5, pallets=14`)
- **Expected Write-Back Receipt**: `{"transfer_dispatch_id": "XDOCK-TRF-8D87AE6A", "inbound_manifest_id": "XDOCK-MNF-20261022-041", "inbound_door_id": "DOOR-INBOUND-04", "outbound_bay_id": "BAY-OUTBOUND-12", "pallet_ids": ["PLT-OAT-9921-01", "PLT-OAT-9921-02", "PLT-OAT-9921-03", "PLT-OAT-9921-04"], "pallet_count": 4, "wms_forklift_mission_id": "FL-MISSION-87AE6A", "status": "CROSSDOCK_TRANSFER_DISPATCHED", "rationale": "Inbound Swift trailer at Door 04 synchronized with outbound J.B. Hunt trailer at Bay 12 (Houston RDC). Direct cross-dock transfer of 4 pallets avoids rack putaway, holding dwell time to 18.5 min and saving 2 touches per pallet.", "idempotency_key": "XDOCK-DISP-20261022-01"}`
- **Expected Markdown Report & Table**:

### 🔄 CrossDockFlow Real-Time Cross-Dock & Flow-Through Briefing

> **Executive Summary**: Successfully orchestrated real-time door-to-door cross-dock synchronization for **Swift Transportation inbound shipment `SHP-SWIFT-20261022-9921`** carrying 24 pallets of organic beverage SKUs at **Door Inbound 04**. Using live carrier arrival milestones and outbound trailer availability, routed **18 eligible flow-through pallets** directly across the dock floor into outbound retail linehauls without rack putaway staging. Dispatched **4 high-priority pallets directly into J.B. Hunt Bay 12 (Houston RDC)**, achieving an average dwell time of **18.5 minutes** (compared to 145 minutes for staged storage), eliminating **2 labor touches per pallet (66.7% labor touch reduction)**, and routing remaining evening lots safely to Buffer Lane B.

#### 📊 Inbound-to-Outbound Dock Transfer & Dwell Telemetry (Atomic Copy-Ready Table)

| Inbound Door | Outbound Bay | Destination Route | Pallets Handled | Dwell Time | Labor Touches | Flow-Through Mode | Status |
|:---|:---|:---|---:|---:|---:|:---|:---|
| `DOOR-04` | `BAY-12` | Houston RDC (J.B. Hunt) | 10 pallets | **18.5 min** | **1 touch (was 3)** | `DIRECT_FLOWTHROUGH` | `COMPLETED` |
| `DOOR-04` | `BAY-14` | Austin FDC (Schneider) | 8 pallets | **22.0 min** | **1 touch (was 3)** | `DIRECT_FLOWTHROUGH` | `IN_PROGRESS` |
| `DOOR-04` | Buffer Lane B | San Antonio (Evening) | 6 pallets | 145.0 min | 3 touches | `BUFFER_STAGED` | `HELD_IN_BUFFER` |

#### ⚡ Automated Door-to-Door Forklift Missions Executed

- **Direct Cross-Dock Transfer Dispatched**: `XDOCK-TRF-8D87AE6A` | From: `DOOR-INBOUND-04` ➔ To: `BAY-OUTBOUND-12` | Pallets: **4** | Mission: `FL-MISSION-87AE6A` | Status: `CROSSDOCK_TRANSFER_DISPATCHED`
- **Pallet Staging Buffer Hold**: `XDOCK-HOLD-C089EDA6` | Pallet: `PLT-OAT-9921-05` | Location: `STAGING-BUFFER-LANE-B` | Reason: `EVENING_DEPARTURE_TRAILER_UNAVAILABLE` | Status: `PALLET_HELD_IN_STAGING`

### 🔗 Connected Systems & Dock Flow Architecture
- **Manhattan Active WMS Cross-Dock Sorter**: Automated inbound-to-outbound pallet matching and wave prioritization.
- **Carrier EDI 214 & Google Maps Fleet Engine**: Precise trailer geofence milestone tracking and dock door reservation.
- **Industrial IoT Forklift Telemetry**: RFID pallet tag tracking, path routing, and dwell time monitoring.
- **SAP EWM Dock & Yard Integration**: Outbound trailer departure scheduling and seal verification.

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_inbound_outbound_crossdock_manifests, query_inbound_carrier_eta_milestones` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `CrossDockFlow Inbound-to-Outbound Direct Pallet Transfer` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_dispatch_direct_crossdock_transfer` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 46. Dynamic Slotting Agent (`warehouse_slotting_agent`)
- **Pillar / Sub-Pillar**: 05 · Inventory & Warehousing — **Warehouse Operations** · **Persona**: DC Operations Mgr / IE Lead · **ROI**: `Reduces picker transit time by 15–30%`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Warehouse Operations, DC Operations Mgr / IE Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Dynamic Slotting Agent intervenes.
- **What This Agent Does**: Evaluates co-pick affinity matrices to recommend fast-pick zone re-slotting.
- **Business Result**: Reduces picker transit time by 15–30%. (**Reduces picker transit time by 15–30%**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Dynamic Slotting Agent.`
- **Read Tools It Must Call**: `query_warehouse_slotting_velocity_tiers, query_amr_picker_travel_telemetry, query_wave_release_order_allocations, query_slot_reassignment_recommendations`
- **Write-Back Tools It Must Call**: `action_execute_slot_reassignment, action_balance_wave_release_profile`
- **Demo Data Input Values It Reads**:
  - Table `amr_picker_travel_telemetry.json` (2 rows): Sample input record has `telemetry_id=AMR-TEL-20261022-001, dc_id=RDC-DALLAS-02, amr_id=AMR-KION-BOT-07, wave_id=WAVE-20261022-AM-01, average_picker_speed_m_s=1.4`
  - Table `slot_reassignment_recommendations.json` (1 rows): Sample input record has `recommendation_id=SLOT-REC-202610-001, sku_id=SKU-BEV-OATMILK-ORIGINAL-1L, current_bin_id=BIN-AISLE-14-SHELF-04-HIGH, recommended_bin_id=BIN-AISLE-02-SHELF-02-GOLDEN, priority=HIGH`
  - Table `warehouse_slotting_velocity_tiers.json` (2 rows): Sample input record has `sku_id=SKU-BEV-OATMILK-ORIGINAL-1L, sku_name=Barista Organic Oat Milk 1L Tetra, velocity_tier=FAST_MOVER_TIER_A, pick_frequency_lines_per_day=840, current_bin_id=BIN-AISLE-14-SHELF-04-HIGH`
  - Table `wave_release_order_allocations.json` (2 rows): Sample input record has `wave_id=WAVE-20261022-AM-01, dc_id=RDC-DALLAS-02, zone_id=ZONE-BULK-MEZZANINE, allocated_orders_count=450, total_pick_lines=1820`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `SlotMaster 3D Warehouse Picker Travel Reduction (RDC Dallas)`
  - **Visual Mark Type**: `BAR` (4 data points: `sku=Oat Milk 1L (Fast), baseline_dist_m=142.0, optimized_dist_m=22.0 | sku=Almond Milk 1L (Med), baseline_dist_m=45.0, optimized_dist_m=45.0 | sku=Soy Milk 1L (Med), baseline_dist_m=88.0, optimized_dist_m=35.0`)
- **Expected Write-Back Receipt**: `{"relocation_task_id": "SLOT-RELOC-C2A8941D", "sku_id": "SKU-BEV-OATMILK-ORIGINAL-1L", "current_bin_id": "BIN-AISLE-14-SHELF-04-HIGH", "target_bin_id": "BIN-AISLE-02-SHELF-02-GOLDEN", "priority": "HIGH", "wms_move_ticket_id": "WMS-MOV-A8941D", "status": "RELOCATION_TASK_DISPATCHED", "rationale": "Fast-mover SKU-BEV-OATMILK relocated from mezzanine Aisle 14 (142m walk) to golden zone Aisle 02 (22m walk), saving 100.8 km of walking and 412 labor hours annually.", "idempotency_key": "SLOT-MOVE-20261022-01"}`
- **Expected Markdown Report & Table**:

### 🏗️ SlotMaster 3D Warehouse Velocity Slotting & Wave Optimization Briefing

> **Executive Summary**: Comprehensive 3D warehouse slotting telemetry at **RDC Dallas (South Regional DC)** diagnosed severe picker travel inefficiency and mezzanine congestion. Fast-mover **Barista Organic Oat Milk 1L** (840 lines/day) was improperly slotted on overhead mezzanine shelves in **Aisle 14** (142 meters from pack stations), forcing AMR bots and pickers to spend **68.2% of shift time walking** and generating aisle gridlock (congestion score 0.84). Dispatched a high-priority WMS physical relocation task moving Oat Milk to **Aisle 02 Golden Zone** (22 meters from pack), cutting travel distance by **84.5% (-120m per pick)** and eliminating **100.8 km of walking per day (412 annual labor hours saved)**. Concurrently throttled concurrent pickers in Zone Bulk Mezzanine from 16 down to 10 to clear traffic jams.

#### 📊 3D Velocity Slotting & Picker Travel Impact (Atomic Copy-Ready Table)

| Product SKU | Velocity Class | Current Bin Location | Recommended Golden Bin | Baseline Walk | Optimized Walk | Daily Travel Saved | Ergonomic Status |
|:---|:---|:---|:---|---:|---:|---:|:---|
| `SKU-BEV-OATMILK-1L` | **Tier A (840 lines/day)** | Aisle 14 Shelf 04 (High) | **Aisle 02 Shelf 02 (Golden)** | 142.0 m | **22.0 m** | **100.8 km/day** | `ERGONOMIC_WAIST_HEIGHT` |
| `SKU-BEV-ALMOND-1L` | Tier B (310 lines/day) | Aisle 05 Shelf 02 (Golden) | Aisle 05 Shelf 02 (Golden) | 45.0 m | 45.0 m | 0.0 km/day | `OPTIMALLY_SLOTTED` |
| `SKU-BEV-SOY-1L` | Tier B (280 lines/day) | Aisle 11 Shelf 03 (High) | Aisle 06 Shelf 02 (Golden) | 88.0 m | 35.0 m | 28.5 km/day | `PENDING_PHASE_2` |

#### ⚡ Automated WMS Move Tickets & Wave Release Controls Executed

- **WMS Stock Relocation Task Dispatched**: `SLOT-RELOC-C2A8941D` | SKU: `SKU-BEV-OATMILK-ORIGINAL-1L` | From: `BIN-AISLE-14-SHELF-04-HIGH` ➔ To: `BIN-AISLE-02-SHELF-02-GOLDEN` | Ticket: `WMS-MOV-A8941D` | Status: `RELOCATION_TASK_DISPATCHED`
- **Wave Release Profile Rebalanced**: `WAVE-THROT-7B95F743` | Wave: `WAVE-20261022-AM-01` | Zone: `ZONE-BULK-MEZZANINE` | Picker Cap: **10 pickers** | Status: `WAVE_PROFILE_REBALANCED`

### 🔗 Connected Intralogistics & Robotic Swarm Architecture
- **Manhattan Active WMS 3D Slotting**: Real-time velocity heatmap, cubic utilization, and pick frequency profiling.
- **KION / Dematic AMR Controller**: VDA 5050 autonomous mobile robot fleet dispatch, pathing, and collision avoidance.
- **Blue Yonder Wave Engine**: Dynamic order batching, zone picker caps, and bottleneck pacing.
- **OSHA Ergonomic Standard Module**: Elimination of overhead reach and deep-bend heavy SKU lifting injuries.

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_warehouse_slotting_velocity_tiers, query_amr_picker_travel_telemetry` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `SlotMaster 3D Warehouse Picker Travel Reduction (RDC Dallas)` (`BAR`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_execute_slot_reassignment` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 47. Dock-to-Stock Agent (`dock_to_stock_agent`)
- **Pillar / Sub-Pillar**: 05 · Inventory & Warehousing — **Warehouse Operations** · **Persona**: Inbound Receiving Supervisor · **ROI**: `Dock turnaround in minutes vs. hours`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Warehouse Operations, Inbound Receiving Supervisor teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Dock-to-Stock Agent intervenes.
- **What This Agent Does**: Parses scanned BOLs and pallet photos to reconcile open ASN (Advance Shipping Notice — EDI 856 pre-arrival manifest) variances.
- **Business Result**: Dock turnaround in minutes vs. hours. (**Dock turnaround in minutes vs. hours**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Dock-to-Stock Agent.`
- **Read Tools It Must Call**: `query_dock_to_stock_agent_telemetry_feed, query_dock_to_stock_agent_constraint_matrix, query_dock_to_stock_agent_optimization_scenarios, query_dock_to_stock_agent_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_dock_to_stock_agent_plan, action_dispatch_dock_to_stock_agent_alert`
- **Demo Data Input Values It Reads**:
  - Table `dock_to_stock_agent_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=DOCK_T-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Warehouse Operations, capacity_limit=12500`
  - Table `dock_to_stock_agent_execution_ledger.json` (3 rows): Sample input record has `execution_id=DOCK_T-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Inbound Receiving Supervisor, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `dock_to_stock_agent_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=04 · Inventory & DC | Warehouse Operations, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `dock_to_stock_agent_telemetry_feed.json` (4 rows): Sample input record has `record_id=DOCK_T-TEL-101, company_id=XYZ-CORP-01, category=04 · Inventory & Warehousing — Warehouse Operations, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[04 · Inventory & DC | Warehouse Operations] Dock-to-Stock Agent — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-DOCK-F91EA654", "status": "COMMITTED", "category": "04 · Inventory & Warehousing — Warehouse Operations", "agent": "[04 · Inventory & DC | Warehouse Operations] Dock-to-Stock Agent", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "YMS / SAP EWM Dock Door Assignment, Driver SMS Gate Pass & Hostler Tablet Dispatch"}`
- **Expected Markdown Report & Table**:

#### 📊 [04 · Inventory & DC | Warehouse Operations] Dock-to-Stock Agent — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `DOCK_T-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `04 · Inventory & Warehousing — Warehouse Operations` · **Persona**: `Inbound Receiving Supervisor` · **Write-Back Receipt**: `ACT-DOCK-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_dock_to_stock_agent_telemetry_feed, query_dock_to_stock_agent_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[04 · Inventory & DC | Warehouse Operations] Dock-to-Stock Agent — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_dock_to_stock_agent_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 48. Wave Fulfillment Copilot (`wave_fulfillment_copilot`)
- **Pillar / Sub-Pillar**: 05 · Inventory & Warehousing — **Warehouse Operations** · **Persona**: DC Shift Floor Lead · **ROI**: `Prevents missed dispatch windows (OTIF)`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Warehouse Operations, DC Shift Floor Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Wave Fulfillment Copilot intervenes.
- **What This Agent Does**: Balances picker lines dynamically to protect carrier pickup cutoff times.
- **Business Result**: Prevents missed dispatch windows (OTIF (On-Time In-Full — delivering 100% of ordered units before the deadline)). (**Prevents missed dispatch windows (OTIF)**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Wave Fulfillment Copilot.`
- **Read Tools It Must Call**: `query_wave_fulfillment_copilot_telemetry_feed, query_wave_fulfillment_copilot_constraint_matrix, query_wave_fulfillment_copilot_optimization_scenarios, query_wave_fulfillment_copilot_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_wave_fulfillment_copilot_plan, action_dispatch_wave_fulfillment_copilot_alert`
- **Demo Data Input Values It Reads**:
  - Table `wave_fulfillment_copilot_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=WAVE_F-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Warehouse Operations, capacity_limit=12500`
  - Table `wave_fulfillment_copilot_execution_ledger.json` (3 rows): Sample input record has `execution_id=WAVE_F-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=DC Shift Floor Lead, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `wave_fulfillment_copilot_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=04 · Inventory & DC | Warehouse Operations, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `wave_fulfillment_copilot_telemetry_feed.json` (4 rows): Sample input record has `record_id=WAVE_F-TEL-101, company_id=XYZ-CORP-01, category=04 · Inventory & Warehousing — Warehouse Operations, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[04 · Inventory & DC | Warehouse Operations] Wave Fulfillment Copilot — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-WAVE-F91EA654", "status": "COMMITTED", "category": "04 · Inventory & Warehousing — Warehouse Operations", "agent": "[04 · Inventory & DC | Warehouse Operations] Wave Fulfillment Copilot", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "Manhattan / SAP EWM Directed Putaway, Re-Slot Tasks & Dynamic Wave Release via Apigee"}`
- **Expected Markdown Report & Table**:

#### 📊 [04 · Inventory & DC | Warehouse Operations] Wave Fulfillment Copilot — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `WAVE_F-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `04 · Inventory & Warehousing — Warehouse Operations` · **Persona**: `DC Shift Floor Lead` · **Write-Back Receipt**: `ACT-WAVE-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_wave_fulfillment_copilot_telemetry_feed, query_wave_fulfillment_copilot_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[04 · Inventory & DC | Warehouse Operations] Wave Fulfillment Copilot — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_wave_fulfillment_copilot_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 49. Phantom Inventory Sensor (`planogram_merchandising_vision_auditor`)
- **Pillar / Sub-Pillar**: 05 · Inventory & Warehousing — **Omnichannel Visibility** · **Persona**: Store Operations / Omni Lead · **ROI**: `Triggers targeted floor cycle counts`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Omnichannel Visibility, Store Operations / Omni Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Phantom Inventory Sensor intervenes.
- **What This Agent Does**: Identifies shrinkage anomalies when on-hand stock stops scanning at POS (Point of Sale — cash-register store scans).
- **Business Result**: Triggers targeted floor cycle counts. (**Triggers targeted floor cycle counts**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Phantom Inventory Sensor.`
- **Read Tools It Must Call**: `query_store_shelf_vision_audit_captures, query_contracted_planogram_templates, query_shelf_compliance_scoring_ledger, query_merchandising_corrective_tasks`
- **Write-Back Tools It Must Call**: `action_dispatch_instore_restock_directive, action_certify_store_planogram_audit`
- **Demo Data Input Values It Reads**:
  - Table `contracted_planogram_templates.json` (1 rows): Sample input record has `template_id=PLG-BEV-GONDOLA-Q4, channel_tier=MODERN_TRADE_HYPER, required_sos_pct=45.0, required_eye_level_facings=14, monthly_visibility_payout_usd=450.0`
  - Table `merchandising_corrective_tasks.json` (1 rows): Sample input record has `task_id=MRCH-TSK-409, outlet_id=OUTLET-HYPER-882, fso_id=FSO-WEST-112, directive=Restock 2 empty gaps of SKU-BEV-500ML from backroom and remove 3 competitor facings from Eye-Level Tier 2`
  - Table `shelf_compliance_scoring_ledger.json` (1 rows): Sample input record has `audit_id=SHLF-AUD-409, outlet_id=OUTLET-HYPER-882, measured_sos_pct=32.1, post_correction_sos_pct=46.8, compliance_status=CORRECTED_IN_STORE`
  - Table `store_shelf_vision_audit_captures.json` (1 rows): Sample input record has `capture_id=IMG-SHLF-20261022-409, outlet_id=OUTLET-HYPER-882, shelf_zone=EYE_LEVEL_TIER_2, detected_brand_facings=9, contracted_brand_facings=14`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `ShelfVision Gemini 3.8 Flash Share-of-Shelf (SOS) & OSA Compliance`
  - **Visual Mark Type**: `BAR + LINE` (3 data points: `store_segment=Hyper #882 (Post-ShelfVision), sos_pct=46.8, osa_pct=98.2 | store_segment=Hyper #882 (Pre-Correction), sos_pct=32.1, osa_pct=84.0 | store_segment=Supermarket #410 (Verified), sos_pct=48.2, osa_pct=97.5`)
- **Expected Write-Back Receipt**: `{"dispatch_execution_id": "SHLF-FIX-C5DBABAE", "capture_id": "IMG-SHLF-20261022-409", "outlet_id": "OUTLET-HYPER-882", "fso_id": "FSO-WEST-112", "missing_facings_count": 5, "rationale": "Gemini 3.8 Flash detected 32.1% Share-of-Shelf (9/14 eye-level facings, 2 empty gaps, 3 competitor intrusions) in 1.18s; pushed instant restock prompt to FSO-WEST-112 while still in store.", "status": "INSTORE_RESTOCK_DIRECTIVE_SENT", "idempotency_key": "SHLF-FIX-20261022-01"}`
- **Expected Markdown Report & Table**:

### ✦ ShelfVision — Retail Planogram & Visibility Auditor — Executive Operations Brief

> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **05 · Deliver**.

#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)

| Dimension | Metric Value | Secondary KPI | Execution Mode |
|:---|---:|---:|:---|
| `Hyper #882 (Post-ShelfVision)` | **46.8** | 98.2 | `OPTIMIZED_CVRPTW` |
| `Hyper #882 (Pre-Correction)` | **32.1** | 84.0 | `LEGACY_STATIC` |
| `Supermarket #410 (Verified)` | **48.2** | 97.5 | `OPTIMIZED_CVRPTW` |

#### ⚡ Autonomous Write-Backs & Actions Executed

- **Action Executed**: `SHLF-FIX-C5DBABAE` | Status: `INSTORE_RESTOCK_DIRECTIVE_SENT` | Rationale: Gemini 3.8 Flash detected 32.1% Share-of-Shelf (9/14 eye-level facings, 2 empty gaps, 3 competitor intrusions) in 1.18s; pushed instant restock prompt to FSO-WEST-112 while still in store.
- **Action Executed**: `SHLF-CRT-763DBD06` | Status: `PLANOGRAM_COMPLIANCE_CERTIFIED` | Rationale: Verified post-correction shelf photo achieved 46.8% SOS (exceeding 45.0% threshold) with 14/14 eye-level facings; unlocked $450 monthly visibility payout.

### 🔗 Connected Enterprise Systems
- **Vertex AI Gemini 3.8 Flash Dense Retail SKU & Facing Detector** (`gRPC Multimodal API`)
- **Enterprise Category Management & Contracted Planogram Registry** (`REST / BigQuery`)
- **Share-of-Shelf (SOS) & Cooler Purity Compliance Scorer** (`Python Analytics`)
- **In-Store Mobile Merchandising Corrective Action Dispatcher** (`Webhook / Push`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_store_shelf_vision_audit_captures, query_contracted_planogram_templates` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `ShelfVision Gemini 3.8 Flash Share-of-Shelf (SOS) & OSA Compliance` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_dispatch_instore_restock_directive` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 50. SFS / BOPIS Sourcing (`atp_order_promising_agent`)
- **Pillar / Sub-Pillar**: 05 · Inventory & Warehousing — **Omnichannel Visibility** · **Persona**: Omnichannel Fulfillment Dir. · **ROI**: `Lowers parcel costs & split rates`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Omnichannel Visibility, Omnichannel Fulfillment Dir. teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before SFS / BOPIS Sourcing intervenes.
- **What This Agent Does**: Selects lowest-cost fulfillment nodes based on store labor and parcel zones.
- **Business Result**: Lowers parcel costs & split rates. (**Lowers parcel costs & split rates**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for SFS / BOPIS Sourcing.`
- **Read Tools It Must Call**: `query_realtime_sku_atp_allocations, query_customer_tier_sla_commitments, query_inbound_customer_order_requests, query_order_promising_routing_decisions`
- **Write-Back Tools It Must Call**: `action_commit_dynamic_order_promise, action_protect_tier1_allocation_reserve`
- **Demo Data Input Values It Reads**:
  - Table `customer_tier_sla_commitments.json` (2 rows): Sample input record has `customer_id=CUST-KROGER-CORP, customer_name=Kroger National Distribution, contract_tier=TIER_1_STRATEGIC, minimum_fill_rate_sla_pct=98.5, on_time_in_full_otif_sla_pct=97.0`
  - Table `inbound_customer_order_requests.json` (2 rows): Sample input record has `order_id=ORD-20261022-8841, customer_id=CUST-KROGER-CORP, sku_id=SKU-BEV-OATMILK-ORIGINAL-1L, requested_units=8000, requested_delivery_date=2026-10-24T12:00:00Z`
  - Table `order_promising_routing_decisions.json` (1 rows): Sample input record has `decision_id=OP-DEC-20261022-001, order_id=ORD-20261022-8841, customer_id=CUST-KROGER-CORP, sku_id=SKU-BEV-OATMILK-ORIGINAL-1L, promised_units=8000`
  - Table `realtime_sku_atp_allocations.json` (2 rows): Sample input record has `sku_id=SKU-BEV-OATMILK-ORIGINAL-1L, network_node_id=CDC-CHICAGO-01, node_type=CENTRAL_DC, total_physical_on_hand_units=68400, allocated_committed_units=14200`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `PromiseGuard Real-Time Order Promising & ATP Inventory Pools`
  - **Visual Mark Type**: `BAR` (4 data points: `node=CDC Chicago (Tier 1), tier1_reserved=20000, uncommitted_atp=34200 | node=RDC Dallas (Tier 2), tier1_reserved=5000, uncommitted_atp=3300 | node=RDC Atlanta (Tier 2), tier1_reserved=8000, uncommitted_atp=12400`)
- **Expected Write-Back Receipt**: `{"protection_id": "TIER-RINGFENCE-19208698", "sku_id": "SKU-BEV-OATMILK-ORIGINAL-1L", "network_node_id": "CDC-CHICAGO-01", "reserve_quantity": 20000, "status": "TIER1_ALLOCATION_RINGFENCED", "rationale": "Ringfencing 20,000 units at Central DC Chicago exclusively for strategic Tier 1 accounts (Kroger SLA 98.5% fill rate, avoiding $2,500/day OTIF penalty).", "idempotency_key": "TIER1-RING-20261022-01"}`
- **Expected Markdown Report & Table**:

### 🤝 PromiseGuard Real-Time Order Promising & ATP Briefing

> **Executive Summary**: Sub-50ms Cloud Spanner evaluation successfully committed high-value inbound order `ORD-20261022-8841` (**8,000 units** of Barista Organic Oat Milk 1L) for strategic account **Kroger National Distribution** (Tier 1 Strategic, 98.5% fill rate SLA). Ingested global stock across Central and Regional DCs with **14.8 ms Spanner query latency**. While local RDC Dallas held only 3,300 uncommitted units, PromiseGuard dynamically allocated the full 8,000 units from **CDC Chicago Tier 1 Protected Quota** (where 20,000 units are ringfenced). Guaranteed delivery by **Oct 24, 2026 at 10:00 AM** (2 hours ahead of contractual cutoff), completely neutralizing a **$2,500/day OTIF penalty** risk.

#### 📊 Inbound Order Promising & Sourcing Evaluation (Atomic Copy-Ready Table)

| Order ID | Customer Account | Contract Tier | Requested Units | Promised Units | Sourcing Node | Promised Delivery | OTIF Risk | Status |
|:---|:---|:---|---:|---:|:---|:---|---:|:---|
| `ORD-8841` | **Kroger National** | `TIER_1_STRATEGIC` | 8,000 units | **8,000 units** | `CDC-CHICAGO-01` | **2026-10-24 10:00 AM** | **$0.00 (Neutralized)** | `ATP_COMMITTED` |
| `ORD-8842` | Lone Star Co-op | `TIER_3_STANDARD` | 1,200 units | 1,200 units | `RDC-DALLAS-02` | 2026-10-24 03:00 PM | $0.00 (Nominal) | `ATP_CONFIRMED` |

#### ⚡ Automated Spanner Reservations & Tier Quota Ringfences Executed

- **Tier 1 Allocation Ringfenced**: `TIER-RINGFENCE-19208698` | SKU: `SKU-BEV-OATMILK-ORIGINAL-1L` | Node: `CDC-CHICAGO-01` | Reserved Quota: **20,000 units** | Status: `TIER1_ALLOCATION_RINGFENCED`
- **Binding ATP Promise Committed**: `PROMISE-COMMIT-6CA9EED9` | Order: `ORD-20261022-8841` | Node: `CDC-CHICAGO-01` | Units: **8,000** | Spanner Txn: `SPAN-TXN-A9EED9` | Status: `ATP_PROMISE_COMMITTED`

### 🔗 Connected Systems & Order Promising Architecture
- **Google Cloud Spanner**: Globally distributed, strongly consistent real-time ATP/CTP inventory engine (<20ms).
- **SAP S/4HANA Sales & Distribution (SD)**: Customer master, contractual allocation tiers, and pricing schedules.
- **Enterprise OMS / Pub/Sub**: Event-driven omnichannel order orchestration with sub-second order promising.
- **Google OR-Tools Sourcing Optimizer**: Cost-to-serve, multi-stop linehaul routing, and SLA constraint solving.

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_realtime_sku_atp_allocations, query_customer_tier_sla_commitments` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `PromiseGuard Real-Time Order Promising & ATP Inventory Pools` (`BAR`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_dynamic_order_promise` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 51. Returns Triage Agent (`returns_triage_agent`)
- **Pillar / Sub-Pillar**: 05 · Inventory & Warehousing — **Omnichannel Visibility** · **Persona**: Reverse Logistics Lead · **ROI**: `Restocks sellable returns within 24h`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Omnichannel Visibility, Reverse Logistics Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Returns Triage Agent intervenes.
- **What This Agent Does**: Evaluates item condition scans to triage restock, vendor return, or liquidation.
- **Business Result**: Restocks sellable returns within 24h. (**Restocks sellable returns within 24h**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Returns Triage Agent.`
- **Read Tools It Must Call**: `query_returns_triage_agent_telemetry_feed, query_returns_triage_agent_constraint_matrix, query_returns_triage_agent_optimization_scenarios, query_returns_triage_agent_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_returns_triage_agent_plan, action_dispatch_returns_triage_agent_alert`
- **Demo Data Input Values It Reads**:
  - Table `returns_triage_agent_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=RETURN-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Omnichannel Visibility, capacity_limit=12500`
  - Table `returns_triage_agent_execution_ledger.json` (3 rows): Sample input record has `execution_id=RETURN-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Reverse Logistics Lead, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `returns_triage_agent_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=04 · Inventory & DC | Omnichannel Visibility, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `returns_triage_agent_telemetry_feed.json` (4 rows): Sample input record has `record_id=RETURN-TEL-101, company_id=XYZ-CORP-01, category=04 · Inventory & Warehousing — Omnichannel Visibility, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[04 · Inventory & DC | Omnichannel Visibility] Returns Triage Agent — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-RETU-F91EA654", "status": "COMMITTED", "category": "04 · Inventory & Warehousing — Omnichannel Visibility", "agent": "[04 · Inventory & DC | Omnichannel Visibility] Returns Triage Agent", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "TMS Fleet Backhaul Pickup Stop, SAP EWM Direct-to-Hub Restock & Vendor Warranty Debit Memo"}`
- **Expected Markdown Report & Table**:

#### 📊 [04 · Inventory & DC | Omnichannel Visibility] Returns Triage Agent — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `RETURN-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `04 · Inventory & Warehousing — Omnichannel Visibility` · **Persona**: `Reverse Logistics Lead` · **Write-Back Receipt**: `ACT-RETU-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_returns_triage_agent_telemetry_feed, query_returns_triage_agent_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[04 · Inventory & DC | Omnichannel Visibility] Returns Triage Agent — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_returns_triage_agent_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

## 06 · Control Tower & Governance (9 Agents)

### 52. Return Fraud Sentinel (`reverse_rma_optimizer`)
- **Pillar / Sub-Pillar**: 06 · Control Tower & Governance — **Returns & Claims Mgmt** · **Persona**: Reverse Logistics / Fraud Lead · **ROI**: `Cuts returns fraud abuse by 25–40%`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Returns & Claims Mgmt, Reverse Logistics / Fraud Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Return Fraud Sentinel intervenes.
- **What This Agent Does**: Analyzes item photos and packaging video feeds to detect wear or swapped tags.
- **Business Result**: Cuts returns fraud abuse by 25–40%. (**Cuts returns fraud abuse by 25–40%**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Return Fraud Sentinel.`
- **Read Tools It Must Call**: `query_customer_rma_intake_requests, query_multimodal_vision_grading_results, query_fleet_backhaul_pickup_slots, query_circular_disposition_routing_ledger`
- **Write-Back Tools It Must Call**: `action_assign_rma_disposition_and_backhaul, action_issue_instant_customer_rma_credit_or_swap`
- **Demo Data Input Values It Reads**:
  - Table `circular_disposition_routing_ledger.json` (1 rows): Sample input record has `disposition_id=DISP-501, rma_id=RMA-20261022-501, routing_path=DIRECT_REGIONAL_FDC_RESTOCK, target_facility_id=FDC-AUSTIN-02, central_return_touch_bypassed=True`
  - Table `customer_rma_intake_requests.json` (2 rows): Sample input record has `rma_id=RMA-20261022-501, customer_id=RETAIL-PARTNER-09, sku_id=SKU-PRO-ESPRESSO-X1, units=12, retail_value_usd=9600.0`
  - Table `fleet_backhaul_pickup_slots.json` (1 rows): Sample input record has `pickup_slot_id=BKH-RMA-501, rma_id=RMA-20261022-501, returning_vehicle_id=TRK-12T-TX14, detour_distance_km=2.4, ltl_shipping_saved_usd=420.0`
  - Table `multimodal_vision_grading_results.json` (1 rows): Sample input record has `grading_id=GRD-501, rma_id=RMA-20261022-501, optical_grade=GRADE_A_FACTORY_SEAL_INTACT, tamper_seal_verified=True, net_recovery_pct=94.0`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `ReturnLoop Circular Margin Recovery & Backhaul Freight Savings`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `disposition_path=Grade-A Direct FDC Restock, recovery_pct=94.0, recovered_usd=9024 | disposition_path=Grade-B Certified Refurb, recovery_pct=72.5, recovered_usd=4640 | disposition_path=Grade-C Component Harvest, recovery_pct=48.0, recovered_usd=3072`)
- **Expected Write-Back Receipt**: `{"dispatch_execution_id": "RMA-LOOP-20AF3E56", "rma_id": "RMA-20261022-501", "optical_grade": "GRADE_A_FACTORY_SEAL_INTACT", "target_facility_id": "FDC-AUSTIN-02", "backhaul_vehicle_id": "TRK-12T-TX14", "rationale": "Gemini 3.8 Flash verified factory tamper seal intact (Grade A); routed 12 units directly to Austin FDC-02 for immediate resale via returning truck TRK-12T-TX14, recovering 94% value ($9,024) and saving $420 LTL freight.", "status": "RMA_DISPOSITION_AND_BACKHAUL_LOCKED", "idempotency_key": "RMA-LOOP-20261022-01"}`
- **Expected Markdown Report & Table**:

### ✦ ReturnLoop — Autonomous RMA Grading & Backhaul Optimizer — Executive Operations Brief

> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **06 · Return & Enable**.

#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)

| Dimension | Metric Value | Secondary KPI | Execution Mode |
|:---|---:|---:|:---|
| `Grade-A Direct FDC Restock` | **94.0** | 9024 | `OPTIMIZED_CVRPTW` |
| `Grade-B Certified Refurb` | **72.5** | 4640 | `OPTIMIZED_CVRPTW` |
| `Grade-C Component Harvest` | **48.0** | 3072 | `OPTIMIZED_CVRPTW` |
| `Legacy Central Return Hub` | **38.0** | 3648 | `LEGACY_STATIC` |

#### ⚡ Autonomous Write-Backs & Actions Executed

- **Action Executed**: `RMA-LOOP-20AF3E56` | Status: `RMA_DISPOSITION_AND_BACKHAUL_LOCKED` | Rationale: Gemini 3.8 Flash verified factory tamper seal intact (Grade A); routed 12 units directly to Austin FDC-02 for immediate resale via returning truck TRK-12T-TX14, recovering 94% value ($9,024) and saving $420 LTL freight.
- **Action Executed**: `RMA-CRED-86695C52` | Status: `INSTANT_RMA_CREDIT_ISSUED` | Rationale: Issued instant SAP credit memo upon optical seal verification and backhaul scan.

### 🔗 Connected Enterprise Systems
- **Vertex AI Gemini 3.8 Flash Optical RMA Condition & Seal Grader** (`gRPC Multimodal API`)
- **SAP S/4HANA Returns & Customer RMA Intake Portal** (`REST / OData v4`)
- **FleetFlow Returning Delivery Truck Backhaul Milk-Run Matcher** (`Google Maps CVRPTW`)
- **OR-Tools Circular Recovery Margin Solver (Restock vs Refurb vs Harvest)** (`Python MILP`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_customer_rma_intake_requests, query_multimodal_vision_grading_results` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `ReturnLoop Circular Margin Recovery & Backhaul Freight Savings` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_assign_rma_disposition_and_backhaul` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 53. Keep-It & Routing Advisor (`keep_it_routing_advisor`)
- **Pillar / Sub-Pillar**: 06 · Control Tower & Governance — **Returns & Claims Mgmt** · **Persona**: Customer Experience (CX) Lead · **ROI**: `Lowers net return costs by 15–22%`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Returns & Claims Mgmt, Customer Experience (CX) Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Keep-It & Routing Advisor intervenes.
- **What This Agent Does**: Evaluates salvage margins vs reverse freight to determine keep-it instant refunds.
- **Business Result**: Lowers net return costs by 15–22%. (**Lowers net return costs by 15–22%**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Keep-It & Routing Advisor.`
- **Read Tools It Must Call**: `query_keep_it_routing_advisor_telemetry_feed, query_keep_it_routing_advisor_constraint_matrix, query_keep_it_routing_advisor_optimization_scenarios, query_keep_it_routing_advisor_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_keep_it_routing_advisor_plan, action_dispatch_keep_it_routing_advisor_alert`
- **Demo Data Input Values It Reads**:
  - Table `keep_it_routing_advisor_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=KEEP_I-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Returns & Claims Mgmt, capacity_limit=12500`
  - Table `keep_it_routing_advisor_execution_ledger.json` (3 rows): Sample input record has `execution_id=KEEP_I-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Customer Experience (CX) Lead, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `keep_it_routing_advisor_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=06 · Returns & ESG | Returns & Claims Mgmt, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `keep_it_routing_advisor_telemetry_feed.json` (4 rows): Sample input record has `record_id=KEEP_I-TEL-101, company_id=XYZ-CORP-01, category=06 · Returns & Reverse Logistics — Returns & Claims Mgmt, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[06 · Returns & ESG | Returns & Claims Mgmt] Keep-It & Routing Advisor — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-KEEP-F91EA654", "status": "COMMITTED", "category": "06 · Returns & Reverse Logistics — Returns & Claims Mgmt", "agent": "[06 · Returns & ESG | Returns & Claims Mgmt] Keep-It & Routing Advisor", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "TMS Fleet Backhaul Pickup Stop, SAP EWM Direct-to-Hub Restock & Vendor Warranty Debit Memo"}`
- **Expected Markdown Report & Table**:

#### 📊 [06 · Returns & ESG | Returns & Claims Mgmt] Keep-It & Routing Advisor — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `KEEP_I-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `06 · Returns & Reverse Logistics — Returns & Claims Mgmt` · **Persona**: `Customer Experience (CX) Lead` · **Write-Back Receipt**: `ACT-KEEP-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_keep_it_routing_advisor_telemetry_feed, query_keep_it_routing_advisor_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[06 · Returns & ESG | Returns & Claims Mgmt] Keep-It & Routing Advisor — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_keep_it_routing_advisor_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 54. OS&D Freight Claims (`osd_freight_claims_agent`)
- **Pillar / Sub-Pillar**: 06 · Control Tower & Governance — **Returns & Claims Mgmt** · **Persona**: Claims Specialist / Controller · **ROI**: `Resolves carrier claims in <72 hours`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Returns & Claims Mgmt, Claims Specialist / Controller teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before OS&D (Over, Short & Damaged freight claims) Freight Claims intervenes.
- **What This Agent Does**: Reconciles eBOLs, dock damage logs, and carrier contracts to auto-file disputes.
- **Business Result**: Resolves carrier claims in <72 hours. (**Resolves carrier claims in <72 hours**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for OS&D Freight Claims.`
- **Read Tools It Must Call**: `query_osd_freight_claims_agent_telemetry_feed, query_osd_freight_claims_agent_constraint_matrix, query_osd_freight_claims_agent_optimization_scenarios, query_osd_freight_claims_agent_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_osd_freight_claims_agent_plan, action_dispatch_osd_freight_claims_agent_alert`
- **Demo Data Input Values It Reads**:
  - Table `osd_freight_claims_agent_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=OSD_FR-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Returns & Claims Mgmt, capacity_limit=12500`
  - Table `osd_freight_claims_agent_execution_ledger.json` (3 rows): Sample input record has `execution_id=OSD_FR-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Claims Specialist / Controller, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `osd_freight_claims_agent_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=06 · Returns & ESG | Returns & Claims Mgmt, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `osd_freight_claims_agent_telemetry_feed.json` (4 rows): Sample input record has `record_id=OSD_FR-TEL-101, company_id=XYZ-CORP-01, category=06 · Returns & Reverse Logistics — Returns & Claims Mgmt, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[06 · Returns & ESG | Returns & Claims Mgmt] OS&D Freight Claims — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-OSD_-F91EA654", "status": "COMMITTED", "category": "06 · Returns & Reverse Logistics — Returns & Claims Mgmt", "agent": "[06 · Returns & ESG | Returns & Claims Mgmt] OS&D Freight Claims", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "SAP SD Alternate-DC Order Re-Allocation & Automated Retailer Portal Dispute Submission via Apigee"}`
- **Expected Markdown Report & Table**:

#### 📊 [06 · Returns & ESG | Returns & Claims Mgmt] OS&D Freight Claims — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `OSD_FR-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `06 · Returns & Reverse Logistics — Returns & Claims Mgmt` · **Persona**: `Claims Specialist / Controller` · **Write-Back Receipt**: `ACT-OSD_-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_osd_freight_claims_agent_telemetry_feed, query_osd_freight_claims_agent_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[06 · Returns & ESG | Returns & Claims Mgmt] OS&D Freight Claims — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_osd_freight_claims_agent_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 55. Dynamic Markdown Agent (`dynamic_markdown_agent`)
- **Pillar / Sub-Pillar**: 06 · Control Tower & Governance — **Expiry & Markdowns** · **Persona**: Merchandising / Store Ops Mgr · **ROI**: `Cuts perishable scrap by 20–35%`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Expiry & Markdowns, Merchandising / Store Ops Mgr teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Dynamic Markdown Agent intervenes.
- **What This Agent Does**: Correlates days-to-expiry (DTE) with sales velocity to trigger ESL shelf price cuts.
- **Business Result**: Cuts perishable scrap by 20–35%. (**Cuts perishable scrap by 20–35%**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Dynamic Markdown Agent.`
- **Read Tools It Must Call**: `query_dynamic_markdown_agent_telemetry_feed, query_dynamic_markdown_agent_constraint_matrix, query_dynamic_markdown_agent_optimization_scenarios, query_dynamic_markdown_agent_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_dynamic_markdown_agent_plan, action_dispatch_dynamic_markdown_agent_alert`
- **Demo Data Input Values It Reads**:
  - Table `dynamic_markdown_agent_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=DYNAMI-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Expiry & Markdowns, capacity_limit=12500`
  - Table `dynamic_markdown_agent_execution_ledger.json` (3 rows): Sample input record has `execution_id=DYNAMI-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Merchandising / Store Ops Mgr, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `dynamic_markdown_agent_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=06 · Returns & ESG | Expiry & Markdowns, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `dynamic_markdown_agent_telemetry_feed.json` (4 rows): Sample input record has `record_id=DYNAMI-TEL-101, company_id=XYZ-CORP-01, category=06 · Returns & Reverse Logistics — Expiry & Markdowns, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[06 · Returns & ESG | Expiry & Markdowns] Dynamic Markdown Agent — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-DYNA-F91EA654", "status": "COMMITTED", "category": "06 · Returns & Reverse Logistics — Expiry & Markdowns", "agent": "[06 · Returns & ESG | Expiry & Markdowns] Dynamic Markdown Agent", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "Salesforce / SAP Trade Promo Calendar Lock & Shaped Regional SKU Curve Update"}`
- **Expected Markdown Report & Table**:

#### 📊 [06 · Returns & ESG | Expiry & Markdowns] Dynamic Markdown Agent — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `DYNAMI-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `06 · Returns & Reverse Logistics — Expiry & Markdowns` · **Persona**: `Merchandising / Store Ops Mgr` · **Write-Back Receipt**: `ACT-DYNA-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_dynamic_markdown_agent_telemetry_feed, query_dynamic_markdown_agent_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[06 · Returns & ESG | Expiry & Markdowns] Dynamic Markdown Agent — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_dynamic_markdown_agent_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 56. Short-Dated Redistributor (`short_dated_redistributor`)
- **Pillar / Sub-Pillar**: 06 · Control Tower & Governance — **Expiry & Markdowns** · **Persona**: Inventory Disposition Lead · **ROI**: `Diverts bulk perishables from landfill`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Expiry & Markdowns, Inventory Disposition Lead teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Short-Dated Redistributor intervenes.
- **What This Agent Does**: Matches near-date DC lots with discounters or food banks before acceptance cutoffs.
- **Business Result**: Diverts bulk perishables from landfill. (**Diverts bulk perishables from landfill**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Short-Dated Redistributor.`
- **Read Tools It Must Call**: `query_short_dated_redistributor_telemetry_feed, query_short_dated_redistributor_constraint_matrix, query_short_dated_redistributor_optimization_scenarios, query_short_dated_redistributor_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_short_dated_redistributor_plan, action_dispatch_short_dated_redistributor_alert`
- **Demo Data Input Values It Reads**:
  - Table `short_dated_redistributor_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=SHORT_-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Expiry & Markdowns, capacity_limit=12500`
  - Table `short_dated_redistributor_execution_ledger.json` (3 rows): Sample input record has `execution_id=SHORT_-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Inventory Disposition Lead, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `short_dated_redistributor_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=06 · Returns & ESG | Expiry & Markdowns, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `short_dated_redistributor_telemetry_feed.json` (4 rows): Sample input record has `record_id=SHORT_-TEL-101, company_id=XYZ-CORP-01, category=06 · Returns & Reverse Logistics — Expiry & Markdowns, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[06 · Returns & ESG | Expiry & Markdowns] Short-Dated Redistributor — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-SHOR-F91EA654", "status": "COMMITTED", "category": "06 · Returns & Reverse Logistics — Expiry & Markdowns", "agent": "[06 · Returns & ESG | Expiry & Markdowns] Short-Dated Redistributor", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "SAP EWM / Manhattan Cross-Dock Flow-Through Directive, Conveyor Sortation Route & Outbound Staging Lock"}`
- **Expected Markdown Report & Table**:

#### 📊 [06 · Returns & ESG | Expiry & Markdowns] Short-Dated Redistributor — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `SHORT_-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `06 · Returns & Reverse Logistics — Expiry & Markdowns` · **Persona**: `Inventory Disposition Lead` · **Write-Back Receipt**: `ACT-SHOR-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_short_dated_redistributor_telemetry_feed, query_short_dated_redistributor_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[06 · Returns & ESG | Expiry & Markdowns] Short-Dated Redistributor — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_short_dated_redistributor_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 57. Food Waste & ESG Copilot (`food_waste_esg_copilot`)
- **Pillar / Sub-Pillar**: 06 · Control Tower & Governance — **Expiry & Markdowns** · **Persona**: Chief Sustainability Officer · **ROI**: `Automates annual circularity reporting`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Expiry & Markdowns, Chief Sustainability Officer teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Food Waste & ESG Copilot intervenes.
- **What This Agent Does**: Aggregates store shrink and organic haul logs to generate audited GHG diversion filings.
- **Business Result**: Automates annual circularity reporting. (**Automates annual circularity reporting**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Food Waste & ESG Copilot.`
- **Read Tools It Must Call**: `query_food_waste_esg_copilot_telemetry_feed, query_food_waste_esg_copilot_constraint_matrix, query_food_waste_esg_copilot_optimization_scenarios, query_food_waste_esg_copilot_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_food_waste_esg_copilot_plan, action_dispatch_food_waste_esg_copilot_alert`
- **Demo Data Input Values It Reads**:
  - Table `food_waste_esg_copilot_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=FOOD_W-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Expiry & Markdowns, capacity_limit=12500`
  - Table `food_waste_esg_copilot_execution_ledger.json` (3 rows): Sample input record has `execution_id=FOOD_W-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Chief Sustainability Officer, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `food_waste_esg_copilot_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=06 · Returns & ESG | Expiry & Markdowns, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `food_waste_esg_copilot_telemetry_feed.json` (4 rows): Sample input record has `record_id=FOOD_W-TEL-101, company_id=XYZ-CORP-01, category=06 · Returns & Reverse Logistics — Expiry & Markdowns, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[06 · Returns & ESG | Expiry & Markdowns] Food Waste & ESG Copilot — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-FOOD-F91EA654", "status": "COMMITTED", "category": "06 · Returns & Reverse Logistics — Expiry & Markdowns", "agent": "[06 · Returns & ESG | Expiry & Markdowns] Food Waste & ESG Copilot", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "EU CBAM / EUDR XML Customs Filing & SAP TM / Blue Yonder Low-Carbon Rail/EV/Ocean Lane Allocation"}`
- **Expected Markdown Report & Table**:

#### 📊 [06 · Returns & ESG | Expiry & Markdowns] Food Waste & ESG Copilot — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `FOOD_W-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `06 · Returns & Reverse Logistics — Expiry & Markdowns` · **Persona**: `Chief Sustainability Officer` · **Write-Back Receipt**: `ACT-FOOD-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_food_waste_esg_copilot_telemetry_feed, query_food_waste_esg_copilot_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[06 · Returns & ESG | Expiry & Markdowns] Food Waste & ESG Copilot — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_food_waste_esg_copilot_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 58. RTI Balance Reconciler (`rti_balance_reconciler`)
- **Pillar / Sub-Pillar**: 06 · Control Tower & Governance — **Pallet & Tote Reclamation** · **Persona**: Asset Recovery / RTI Manager · **ROI**: `Eliminates 30% in non-return fee fines`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Pallet & Tote Reclamation, Asset Recovery / RTI (Returnable Transport Items — reusable plastic crates, kegs & pallets) Manager teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before RTI Balance Reconciler intervenes.
- **What This Agent Does**: Reconciles RFID portal scans with CHEP/PECO statements to detect hoarding nodes.
- **Business Result**: Eliminates 30% in non-return fee fines. (**Eliminates 30% in non-return fee fines**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for RTI Balance Reconciler.`
- **Read Tools It Must Call**: `query_rti_balance_reconciler_telemetry_feed, query_rti_balance_reconciler_constraint_matrix, query_rti_balance_reconciler_optimization_scenarios, query_rti_balance_reconciler_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_rti_balance_reconciler_plan, action_dispatch_rti_balance_reconciler_alert`
- **Demo Data Input Values It Reads**:
  - Table `rti_balance_reconciler_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=RTI_BA-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Pallet & Tote Reclamation, capacity_limit=12500`
  - Table `rti_balance_reconciler_execution_ledger.json` (3 rows): Sample input record has `execution_id=RTI_BA-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Asset Recovery / RTI Manager, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `rti_balance_reconciler_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=06 · Returns & ESG | Pallet & Tote Reclamation, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `rti_balance_reconciler_telemetry_feed.json` (4 rows): Sample input record has `record_id=RTI_BA-TEL-101, company_id=XYZ-CORP-01, category=06 · Returns & Reverse Logistics — Pallet & Tote Reclamation, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[06 · Returns & ESG | Pallet & Tote Reclamation] RTI Balance Reconciler — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-RTI_-F91EA654", "status": "COMMITTED", "category": "06 · Returns & Reverse Logistics — Pallet & Tote Reclamation", "agent": "[06 · Returns & ESG | Pallet & Tote Reclamation] RTI Balance Reconciler", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "SAP BAPI_MATERIAL_SAVEDATA & Purchasing Info-Record Lead-Time / Route / 3D Dimension Auto-Update"}`
- **Expected Markdown Report & Table**:

#### 📊 [06 · Returns & ESG | Pallet & Tote Reclamation] RTI Balance Reconciler — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `RTI_BA-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `06 · Returns & Reverse Logistics — Pallet & Tote Reclamation` · **Persona**: `Asset Recovery / RTI Manager` · **Write-Back Receipt**: `ACT-RTI_-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_rti_balance_reconciler_telemetry_feed, query_rti_balance_reconciler_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[06 · Returns & ESG | Pallet & Tote Reclamation] RTI Balance Reconciler — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_rti_balance_reconciler_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 59. Milk-Run Consolidation (`intermodal_rail_linehaul_agent`)
- **Pillar / Sub-Pillar**: 06 · Control Tower & Governance — **Pallet & Tote Reclamation** · **Persona**: Reverse Transport Planner · **ROI**: `Boosts backhaul fill rate by 25–40%`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Pallet & Tote Reclamation, Reverse Transport Planner teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Milk-Run Consolidation intervenes.
- **What This Agent Does**: Schedules dynamic backhauls to collect empty roll cages and RPCs from retail stores.
- **Business Result**: Boosts backhaul fill rate by 25–40%. (**Boosts backhaul fill rate by 25–40%**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Milk-Run Consolidation.`
- **Read Tools It Must Call**: `query_intermodal_corridor_shipments, query_railinc_edi417_train_consists, query_rail_ramp_cutoff_and_drayage, query_otr_to_rail_mode_conversion_ledger`
- **Write-Back Tools It Must Call**: `action_tender_edi404_rail_intermodal_bill, action_synchronize_ramp_crane_drayage_slot`
- **Demo Data Input Values It Reads**:
  - Table `intermodal_corridor_shipments.json` (1 rows): Sample input record has `shipment_id=SHP-IM-LA-CHI-701, origin_hub=Los Angeles Factory Hub, dest_dc=Chicago Joliet RDC, distance_miles=2015, otr_truck_cost_usd=4650.0`
  - Table `otr_to_rail_mode_conversion_ledger.json` (1 rows): Sample input record has `corridor_lane=LAX_TO_JOLIET_CHI, containers_converted=18, cost_savings_pct=37.8, total_usd_saved=31680.0, co2e_reduction_pct=68.4`
  - Table `rail_ramp_cutoff_and_drayage.json` (1 rows): Sample input record has `ramp_id=LPC_JOLIET_CHI, crane_grounding_utc=2026-10-25T15:30:00Z, free_time_hours=24, assigned_dray_tractor=JBHT-DRAY-CHI42, chassis_id=TRAC-53-8821`
  - Table `railinc_edi417_train_consists.json` (1 rows): Sample input record has `train_id=BNSF-Q-LACCHI-22, rail_carrier=BNSF_RAILWAY, origin_ramp=HOBART_LAX, dest_ramp=LPC_JOLIET_CHI, articulated_well_car=DTTX-749201-WELL-B`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `IntermodalSync OTR-to-Rail Cost & Carbon Reduction`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `corridor_mode=LAX➔CHI (COFC Rail), cost_usd=2890, co2e_kg=890 | corridor_mode=LAX➔CHI (OTR Truck), cost_usd=4650, co2e_kg=2815 | corridor_mode=SAV➔MEM (CSX Rail), cost_usd=1420, co2e_kg=410`)
- **Expected Write-Back Receipt**: `{"dispatch_execution_id": "RAIL-404-5ECFA9DC", "shipment_id": "SHP-IM-LA-CHI-701", "rail_carrier": "BNSF_RAILWAY", "train_id": "BNSF-Q-LACCHI-22", "origin_ramp": "HOBART_LAX", "dest_ramp": "LPC_JOLIET_CHI", "rationale": "Chicago Joliet RDC has 14.5 days of supply buffer; converting 2,015-mile linehaul from OTR truck to BNSF double-stack COFC rail saves $1,760 (-37.8%) and cuts Scope-3 CO2e by 68.4%.", "status": "EDI404_RAIL_TENDER_ACCEPTED", "idempotency_key": "RAIL-404-20261022-01"}`
- **Expected Markdown Report & Table**:

### ✦ IntermodalSync — Factory-to-DC Intermodal Rail, Barge & Linehaul Orchestrator — Executive Operations Brief

> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **05 · Deliver**.

#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)

| Dimension | Metric Value | Secondary KPI | Execution Mode |
|:---|---:|---:|:---|
| `LAX➔CHI (COFC Rail)` | **2890** | 890 | `OPTIMIZED_CVRPTW` |
| `LAX➔CHI (OTR Truck)` | **4650** | 2815 | `LEGACY_STATIC` |
| `SAV➔MEM (CSX Rail)` | **1420** | 410 | `OPTIMIZED_CVRPTW` |
| `SAV➔MEM (OTR Truck)` | **2350** | 1290 | `LEGACY_STATIC` |

#### ⚡ Autonomous Write-Backs & Actions Executed

- **Action Executed**: `RAIL-404-5ECFA9DC` | Status: `EDI404_RAIL_TENDER_ACCEPTED` | Rationale: Chicago Joliet RDC has 14.5 days of supply buffer; converting 2,015-mile linehaul from OTR truck to BNSF double-stack COFC rail saves $1,760 (-37.8%) and cuts Scope-3 CO2e by 68.4%.
- **Action Executed**: `RAIL-DRAY-C3EC7046` | Status: `RAMP_CRANE_DRAYAGE_SYNCHRONIZED` | Rationale: Synchronized J.B. Hunt drayage tractor JBHT-DRAY-CHI42 and chassis TRAC-53-8821 with BNSF Joliet crane grounding at 15:30 UTC, eliminating rail ramp storage fees.

### 🔗 Connected Enterprise Systems
- **Railinc Car Location Message (CLM) & Class-I Rail EDI 404/417 Gateway** (`EDI 404 / 417 / REST`)
- **Google OR-Tools OTR-to-Rail Intermodal Mode Conversion Solver** (`Python MILP SDK`)
- **BNSF / Union Pacific / CSX Intermodal Ramp Cut-Off & Crane Scheduler** (`REST API / Webhook`)
- **GLEC v3.0 Intermodal Rail vs OTR Truck Carbon Intensity Ledger** (`BigQuery SQL / JSON`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_intermodal_corridor_shipments, query_railinc_edi417_train_consists` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `IntermodalSync OTR-to-Rail Cost & Carbon Reduction` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_tender_edi404_rail_intermodal_bill` without `idempotency_key` triggers `missing_idempotency_key`.

---

### 60. Sanitation & Health Agent (`sanitation_health_agent`)
- **Pillar / Sub-Pillar**: 06 · Control Tower & Governance — **Pallet & Tote Reclamation** · **Persona**: Packaging QA / Food Safety · **ROI**: `Extends reusable lifecycle by 15–20%`

#### 🗣️ How to Explain This Agent to a Customer (Plain English, Abbreviations Explained)
- **The Customer Problem**: In Pallet & Tote Reclamation, Packaging QA / Food Safety teams face manual bottlenecks across disconnected spreadsheets and ERP screens—delaying decisions before Sanitation & Health Agent intervenes.
- **What This Agent Does**: Inspects return photos and wash logs for structural fatigue and chemical compliance.
- **Business Result**: Extends reusable lifecycle by 15–20%. (**Extends reusable lifecycle by 15–20%**).

#### 📥 1. Input You Give & Demo Data Resources Used
- **Prompt to Type / Paste**:
  > `Execute full autonomous analysis and write-back for Sanitation & Health Agent.`
- **Read Tools It Must Call**: `query_sanitation_health_agent_telemetry_feed, query_sanitation_health_agent_constraint_matrix, query_sanitation_health_agent_optimization_scenarios, query_sanitation_health_agent_execution_ledger`
- **Write-Back Tools It Must Call**: `action_commit_sanitation_health_agent_plan, action_dispatch_sanitation_health_agent_alert`
- **Demo Data Input Values It Reads**:
  - Table `sanitation_health_agent_constraint_matrix.json` (3 rows): Sample input record has `constraint_id=SANITA-CON-201, sku_id=SKU-SEMI-9900-X1, vendor_id=VND-T1-TSMC-TW01, sub_pillar=Pallet & Tote Reclamation, capacity_limit=12500`
  - Table `sanitation_health_agent_execution_ledger.json` (3 rows): Sample input record has `execution_id=SANITA-EXE-301, shipment_id=SHP-XYZ-90884, order_id=ORD-XYZ-2026-99401, persona_owner=Packaging QA / Food Safety, erp_system=SAP S/4HANA & BigQuery Twin`
  - Table `sanitation_health_agent_optimization_scenarios.json` (3 rows): Sample input record has `scenario_id=SCEN-BASELINE-MANUAL, scenario_name=Legacy Manual Spreadsheet Baseline, category=06 · Returns & ESG | Pallet & Tote Reclamation, service_level_pct=88.4, annual_cost_usd=4850000`
  - Table `sanitation_health_agent_telemetry_feed.json` (4 rows): Sample input record has `record_id=SANITA-TEL-101, company_id=XYZ-CORP-01, category=06 · Returns & Reverse Logistics — Pallet & Tote Reclamation, facility_id=FAC-PLANT-US-AUS01, sku_id=SKU-SEMI-9900-X1`

#### 📤 2. Exact Output You Must Receive When Testing Manually
- **Expected A2UI Visual Card (`VegaChart`)**:
  - **Chart Title**: `[06 · Returns & ESG | Pallet & Tote Reclamation] Sanitation & Health Agent — Performance & ROI Telemetry`
  - **Visual Mark Type**: `BAR + LINE` (4 data points: `unit=FAC-PLANT-US-AUS01, Baseline=78.4, Optimized=96.2 | unit=FAC-DC-US-DAL02, Baseline=81.0, Optimized=97.5 | unit=FAC-PORT-NL-RTM01, Baseline=74.2, Optimized=95.8`)
- **Expected Write-Back Receipt**: `{"action_id": "ACT-SANI-F91EA654", "status": "COMMITTED", "category": "06 · Returns & Reverse Logistics — Pallet & Tote Reclamation", "agent": "[06 · Returns & ESG | Pallet & Tote Reclamation] Sanitation & Health Agent", "target_node": "FAC-PLANT-US-AUS01", "sku_id": "SKU-SEMI-9900-X1", "confidence_score": 0.96, "erp_writeback": "Bounded PLC Recipe Offset Recommendation & Automated SAP QM Usage Decision (BAPI_INSPLOT_SETUSAGEDECISION)"}`
- **Expected Markdown Report & Table**:

#### 📊 [06 · Returns & ESG | Pallet & Tote Reclamation] Sanitation & Health Agent — Verified Enterprise Telemetry

| Record ID | Facility | SKU | Baseline | Optimized | Status |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `SANITA-TEL-101` | `FAC-PLANT-US-AUS01` | `SKU-SEMI-9900-X1` | 78.4% | **96.2%** | `ACTION_REQUIRED` |

**Category**: `06 · Returns & Reverse Logistics — Pallet & Tote Reclamation` · **Persona**: `Packaging QA / Food Safety` · **Write-Back Receipt**: `ACT-SANI-F91EA654` (`COMMITTED`)

#### ✅ 3. Manual Verification Checklist
- [ ] **Resource Check**: Agent invoked `query_sanitation_health_agent_telemetry_feed, query_sanitation_health_agent_constraint_matrix` against its `4` fixture tables.
- [ ] **A2UI Graphic Check**: Agent rendered the `[06 · Returns & ESG | Pallet & Tote Reclamation] Sanitation & Health Agent — Performance & ROI Telemetry` (`BAR + LINE`) visual surface.
- [ ] **Data Accuracy Check**: Output table matches the exact SKU/Facility/Order numbers above with zero hallucination.
- [ ] **Governance Gate Check**: Calling `action_commit_sanitation_health_agent_plan` without `idempotency_key` triggers `missing_idempotency_key`.

---

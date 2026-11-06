# 🎬 Supply Chain AI Agents — Complete Testing, Demo Data & Video Recording Playbook

> **Executive Summary for Leadership & Evaluators**:
> This Playbook provides a clear, human-understandable walkthrough for all **60 Supply Chain AI Agents** spanning the 6 ASCM SCOR Operating Pillars.
> For each agent, you will find:
> 1. **The Real-World Business Use Case**: What specific operational problem it solves in plain English.
> 2. **Connected Enterprise Systems & Data Sources**: Simple enterprise connectors (SAP, BigQuery, Manhattan WMS, Oracle OTM, Siemens MES) — zero raw SQL table clutter.
> 3. **The 3-Step Execution Flow**: How the agent ingests data, solves constraints, and executes safe writebacks.
> 4. **3 Realistic High-Impact Business Prompts**: Authentic plain-English questions you can paste directly into Gemini Enterprise or the local ADK chat.

---

## 01 · Planning & Strategy (12 Agents)
*Demand Forecasting, Trade Promotion, S&OP / IBP, Portfolio & SKU*

### #01 · Demand Sensing Agent (`demand_sensing_agent`)
- **Sub-Pillar**: Demand Forecasting | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Demand Planner / Forecaster · **ROI Benchmark**: `-20%–35% Short-Term WAPE` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: $1.77T/yr global stockout & overstock distortion · 32%–45% manual SKU-week WAPE. Retailers & CPGs lose $1.77 Trillion annually ($1.2T stockouts + $562B overstocks) due to lagged monthly ERP forecasts that miss POS, promo, and weather shifts.
- **The AI Solution**: Synthesizes POS velocity, weather anomalies, and macro trends.
- **Quantified Outcome**: Fuses daily POS sell-through, weather ensembles, and stockout imputation to cut short-horizon WAPE by 20%–35% and reduce safety-stock buffers.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🛒 SAP S/4HANA (SD/MM)**: Pulls daily store checkout scans (EDI 852), open customer orders, and baseline ERP demand forecasts.
- **☁️ BigQuery Demand Lake**: Streams real-time weather anomalies (Google DeepMind WeatherNext), foot-traffic indices, and channel sales.
- **🧠 Vertex AI TimesFM**: Foundation time-series forecasting model generating probabilistic P10/P50/P90 demand envelopes.
- **📊 SAP IBP**: Reconciles unconstrained commercial plans and publishes approved consensus forecast key figures.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and BigQuery) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Vertex) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Run a multi-signal demand sensing audit across our Western Logistics Corridor (Mumbai & Gujarat) and Northern NCR retail hubs by querying daily checkout scans from SAP S/4HANA and weather anomaly feeds from Google DeepMind WeatherNext. Detect store stockout censorship at DMart (Avenue Supermarts), evaluate commercial sales overrides for chronic optimism bias, and output a copy-ready CSV schedule with revised forecast allocations.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Generate an interactive visual fan chart comparing our latest sensed TimesFM P10/P50/P90 demand forecast against the static ERP baseline plan across top beverage and snack SKUs, highlighting weather-driven demand spikes and stockout buffers.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft an executive briefing note and interactive HTML dashboard for the Chief Supply Chain Officer summarizing the revenue protected, forecast error reduction, and recommended SAP IBP consensus adjustments.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py demand_sensing_agent
```

---

### #02 · Forecast Reconciliation (`cpfr_sync_agent`)
- **Sub-Pillar**: Demand Forecasting | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Commercial Planning Lead · **ROI Benchmark**: `-40%–55% CPFR Variance` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: $1.77T/yr global stockout & overstock distortion · 32%–45% manual SKU-week WAPE. Retailers & CPGs lose $1.77 Trillion annually ($1.2T stockouts + $562B overstocks) due to lagged monthly ERP forecasts that miss POS, promo, and weather shifts.
- **The AI Solution**: Identifies unmodeled drivers across eCommerce and retail channels.
- **Quantified Outcome**: Reconciles retailer EDI 830 forecasts against commercial & supply baselines, eliminating systematic bias and cutting stockout/overstock swings.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🛒 SAP S/4HANA (SD/MM)**: Pulls daily store checkout scans (EDI 852), open customer orders, and baseline ERP demand forecasts.
- **☁️ BigQuery Demand Lake**: Streams real-time weather anomalies (Google DeepMind WeatherNext), foot-traffic indices, and channel sales.
- **🧠 Vertex AI TimesFM**: Foundation time-series forecasting model generating probabilistic P10/P50/P90 demand envelopes.
- **📊 SAP IBP**: Reconciles unconstrained commercial plans and publishes approved consensus forecast key figures.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and BigQuery) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Vertex) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Where do our internal demand forecasts disagree most with what our retail partners and online channels are projecting? Please highlight the biggest gaps.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Create a chart comparing our internal forecast against our retail partners' order projections across key accounts so I can see the largest mismatches at a glance.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Prepare a clear summary note for our joint retail planning meeting outlining the top forecast discrepancies, the service or inventory risk, and how we should align the numbers.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py cpfr_sync_agent
```

---

### #03 · NPI Demand Profiler (`npi_demand_profiler`)
- **Sub-Pillar**: Demand Forecasting | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Brand & Innovation Manager · **ROI Benchmark**: `-30% Launch Forecast Error` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: $1.77T/yr global stockout & overstock distortion · 32%–45% manual SKU-week WAPE. Retailers & CPGs lose $1.77 Trillion annually ($1.2T stockouts + $562B overstocks) due to lagged monthly ERP forecasts that miss POS, promo, and weather shifts.
- **The AI Solution**: Matches launch packaging and attributes to historical lookalikes.
- **Quantified Outcome**: Clusters new SKU attributes against historical lookalikes and updates early POS velocity curves in week 1–4 to prevent launch stockouts or dead stock.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🛒 SAP S/4HANA (SD/MM)**: Pulls daily store checkout scans (EDI 852), open customer orders, and baseline ERP demand forecasts.
- **☁️ BigQuery Demand Lake**: Streams real-time weather anomalies (Google DeepMind WeatherNext), foot-traffic indices, and channel sales.
- **🧠 Vertex AI TimesFM**: Foundation time-series forecasting model generating probabilistic P10/P50/P90 demand envelopes.
- **📊 SAP IBP**: Reconciles unconstrained commercial plans and publishes approved consensus forecast key figures.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and BigQuery) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Vertex) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `How are our upcoming new product launches expected to perform based on similar past launches, and which items face the highest risk of early stockouts or excess inventory?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Show me a visual comparison of projected launch demand versus initial supply commitments across our new products, and explain which launch needs immediate attention.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a launch readiness brief for the commercial and supply teams summarizing expected trial and repeat demand, comparable past launches, and recommended opening inventory.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py npi_demand_profiler
```

---

### #04 · Promo ROI Simulator (`promo_lift_simulator`)
- **Sub-Pillar**: Trade Promotion | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Trade Marketing Manager · **ROI Benchmark**: `+15%–25% Promo Net ROI` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 59%–67% of CPG trade promotions fail to break even · 4%–7% revenue leaked. Trade spend is typically the #2 P&L line item (15%–25% of gross sales), yet 59%–67% of promotions lose money due to subsidized baseline volume, forward-buying, and unverified retailer deductions.
- **The AI Solution**: Simulates price elasticity, shelf lift, and incremental spend return.
- **Quantified Outcome**: Simulates baseline cannibalization, post-promo dip, and incremental gross margin before trade funds are committed—blocking unprofitable events.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🛒 SAP S/4HANA (SD/MM)**: Pulls daily store checkout scans (EDI 852), open customer orders, and baseline ERP demand forecasts.
- **☁️ BigQuery Demand Lake**: Streams real-time weather anomalies (Google DeepMind WeatherNext), foot-traffic indices, and channel sales.
- **🧠 Vertex AI TimesFM**: Foundation time-series forecasting model generating probabilistic P10/P50/P90 demand envelopes.
- **📊 SAP IBP**: Reconciles unconstrained commercial plans and publishes approved consensus forecast key figures.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and BigQuery) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Vertex) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Evaluate our upcoming Q4 retail trade promotion campaigns in Salesforce TPM across DMart (Avenue Supermarts) and Reliance Retail & Wholesale. Model causal price elasticity, forward-buying inventory drag, and cross-SKU cannibalization, flag any margin-dilutive discounts, and provide an atomic CSV ledger of projected financial returns.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Render an interactive promotional margin waterfall and cannibalization matrix chart comparing promotional volume lift against net dollar margin impact across all planned retail campaigns.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a formal trade spend review memorandum and interactive HTML promotion approval brief for Sales and Finance detailing which promotional campaigns to fund, which to restructure with bundled cross-sells, and why.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py promo_lift_simulator
```

---

### #05 · JBP Negotiation Agent (`field_beat_distributor_sync_agent`)
- **Sub-Pillar**: Trade Promotion | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Key Account Manager (KAM) · **ROI Benchmark**: `+2–4 pts JBP Margin` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 59%–67% of CPG trade promotions fail to break even · 4%–7% revenue leaked. Trade spend is typically the #2 P&L line item (15%–25% of gross sales), yet 59%–67% of promotions lose money due to subsidized baseline volume, forward-buying, and unverified retailer deductions.
- **The AI Solution**: Creates customized sell-in story decks and joint promotional calendars.
- **Quantified Outcome**: Optimizes joint retailer-manufacturer volume, funding tiers, and display slotting simultaneously so trade investment grows net contribution.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🛒 SAP S/4HANA (SD/MM)**: Pulls daily store checkout scans (EDI 852), open customer orders, and baseline ERP demand forecasts.
- **☁️ BigQuery Demand Lake**: Streams real-time weather anomalies (Google DeepMind WeatherNext), foot-traffic indices, and channel sales.
- **🧠 Vertex AI TimesFM**: Foundation time-series forecasting model generating probabilistic P10/P50/P90 demand envelopes.
- **📊 SAP IBP**: Reconciles unconstrained commercial plans and publishes approved consensus forecast key figures.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and BigQuery) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Vertex) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `How are our regional distributors and field sales territories performing against our joint business targets, and where is distributor stock piling up versus running short?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Show me a chart comparing distributor sell-in orders against actual retail sell-through across regions, and explain where channel inventory is out of balance.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Prepare a clear joint business planning summary we can use in our next distributor review covering volume progress, channel health, and recommended order adjustments.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py field_beat_distributor_sync_agent
```

---

### #06 · Deduction Audit Agent (`trade_scheme_claims_reconciler`)
- **Sub-Pillar**: Trade Promotion | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Revenue / Trade Finance Lead · **ROI Benchmark**: `Recovers 1.5%–3% Trade Spend` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 59%–67% of CPG trade promotions fail to break even · 4%–7% revenue leaked. Trade spend is typically the #2 P&L line item (15%–25% of gross sales), yet 59%–67% of promotions lose money due to subsidized baseline volume, forward-buying, and unverified retailer deductions.
- **The AI Solution**: Audits scanned proof-of-performance circulars and invoices via OCR.
- **Quantified Outcome**: Cross-matches retailer deduction claims against contracted scan dates, POS lift, and proof-of-performance—recovering invalid chargebacks.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🛒 SAP S/4HANA (SD/MM)**: Pulls daily store checkout scans (EDI 852), open customer orders, and baseline ERP demand forecasts.
- **☁️ BigQuery Demand Lake**: Streams real-time weather anomalies (Google DeepMind WeatherNext), foot-traffic indices, and channel sales.
- **🧠 Vertex AI TimesFM**: Foundation time-series forecasting model generating probabilistic P10/P50/P90 demand envelopes.
- **📊 SAP IBP**: Reconciles unconstrained commercial plans and publishes approved consensus forecast key figures.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and BigQuery) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Vertex) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Can you review our open retailer promotional deduction claims and tell me which claims match verified store promotions versus unauthorized over-deductions we should dispute?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Generate a chart comparing claimed retailer deductions against verified promotional performance across accounts so I can see where leakage is highest.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a clear deduction audit memo for Finance and Sales detailing the invalid claims uncovered, the recoverable dollar amount, and our dispute plan.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py trade_scheme_claims_reconciler
```

---

### #07 · Consensus & Gap Agent (`sop_scenario_weaver`)
- **Sub-Pillar**: S&OP / IBP | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: S&OP / Supply Planning Dir. · **ROI Benchmark**: `+1.5–3 pts EBITDA Protection` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 2–4 week manual S&OP reconciliation lag · 2%–4% EBITDA lost to siloed plans. Disconnected sales, plant, and finance spreadsheets take 15–22 business days to reconcile each month, forcing costly expedite freight and margin-dilutive allocation trade-offs.
- **The AI Solution**: Reconciles unconstrained demand with factory plant bottleneck limits.
- **Quantified Outcome**: Translates supply-demand gaps into margin-optimal constrained scenarios (overtime vs. co-packer vs. air freight vs. customer priority).

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🛒 SAP S/4HANA (SD/MM)**: Pulls daily store checkout scans (EDI 852), open customer orders, and baseline ERP demand forecasts.
- **☁️ BigQuery Demand Lake**: Streams real-time weather anomalies (Google DeepMind WeatherNext), foot-traffic indices, and channel sales.
- **🧠 Vertex AI TimesFM**: Foundation time-series forecasting model generating probabilistic P10/P50/P90 demand envelopes.
- **📊 SAP IBP**: Reconciles unconstrained commercial plans and publishes approved consensus forecast key figures.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and BigQuery) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Vertex) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Reconcile unconstrained commercial demand from SAP IBP against factory capacity constraints from Siemens MES and raw material allocations from SAP Ariba. Run an OR-Tools optimization across 3 operating scenarios (Overtime vs. Co-Packer vs. Priority Allocation) and provide a CSV capacity tradeoff matrix.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Plot an interactive S&OP scenario trade-off frontier chart displaying margin contribution against customer fulfillment percentage across our baseline, overtime, and co-packer supply plans.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a monthly S&OP consensus alignment memorandum and interactive HTML executive review pack for the Executive S&OP committee outlining the recommended operating plan and supply commitments.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py sop_scenario_weaver
```

---

### #08 · Digital War-Room Agent (`disruption_war_room_orchestrator`)
- **Sub-Pillar**: S&OP / IBP | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Supply Chain VP / COO · **ROI Benchmark**: `Protects 97%+ Strategic OTIF` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 2–4 week manual S&OP reconciliation lag · 2%–4% EBITDA lost to siloed plans. Disconnected sales, plant, and finance spreadsheets take 15–22 business days to reconcile each month, forcing costly expedite freight and margin-dilutive allocation trade-offs.
- **The AI Solution**: Evaluates co-packer shifts and allocation trade-offs during supply outages.
- **Quantified Outcome**: Maps port, plant, or supplier shocks to affected customer orders in minutes and executes the lowest-cost mitigation playbook to protect OTIF.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🛒 SAP S/4HANA (SD/MM)**: Pulls daily store checkout scans (EDI 852), open customer orders, and baseline ERP demand forecasts.
- **☁️ BigQuery Demand Lake**: Streams real-time weather anomalies (Google DeepMind WeatherNext), foot-traffic indices, and channel sales.
- **🧠 Vertex AI TimesFM**: Foundation time-series forecasting model generating probabilistic P10/P50/P90 demand envelopes.
- **📊 SAP IBP**: Reconciles unconstrained commercial plans and publishes approved consensus forecast key figures.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and BigQuery) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Vertex) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Scan global inbound shipping corridors and tier-1 supplier plants by querying Google DeepMind WeatherNext severe storm feeds, maritime AIS vessel coordinates, and Resilinc supplier outage alerts. Identify all delayed shipments and impacted production orders, calculate dollar revenue at risk, and output an incident CSV ledger.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Generate an interactive geographic war-room map visualizing active maritime vessel routes, impacted ocean ports, and disrupted supplier facilities with color-coded delay severity bands.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft an emergency war-room leadership briefing note and interactive HTML crisis dashboard recommending expedited air-freight transfers and alternate co-packer activations to safeguard customer OTIF.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py disruption_war_room_orchestrator
```

---

### #09 · Executive Copilot (`csco_control_tower_copilot`)
- **Sub-Pillar**: S&OP / IBP | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: IBP Lead / Chief Planning Off. · **ROI Benchmark**: `-85% Executive Latency` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 2–4 week manual S&OP reconciliation lag · 2%–4% EBITDA lost to siloed plans. Disconnected sales, plant, and finance spreadsheets take 15–22 business days to reconcile each month, forcing costly expedite freight and margin-dilutive allocation trade-offs.
- **The AI Solution**: Generates pre-read decks and tracks sign-offs across cross-functional leads.
- **Quantified Outcome**: Synthesizes cross-pillar service, cash-to-cash, and cost variances on demand—turning 5-day analyst deck cycles into instant executive action.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🛒 SAP S/4HANA (SD/MM)**: Pulls daily store checkout scans (EDI 852), open customer orders, and baseline ERP demand forecasts.
- **☁️ BigQuery Demand Lake**: Streams real-time weather anomalies (Google DeepMind WeatherNext), foot-traffic indices, and channel sales.
- **🧠 Vertex AI TimesFM**: Foundation time-series forecasting model generating probabilistic P10/P50/P90 demand envelopes.
- **📊 SAP IBP**: Reconciles unconstrained commercial plans and publishes approved consensus forecast key figures.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and BigQuery) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Vertex) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Provide an executive health audit across our 6 operating pillars by querying SAP S/4HANA order backlog, plant bottlenecks, and BigQuery digital twin telemetry. Identify our top 3 operational choke points, calculate total revenue at risk, and output an executive CSV bottleneck matrix.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Generate an interactive multi-echelon supply chain risk radar and operational health visualization illustrating OTIF compliance, manufacturing bottlenecks, and inventory buffer health across all operating regions.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft an executive board briefing memo and interactive HTML CSCO cockpit summarizing our critical operational decisions, working capital unlocks, and recommended cross-functional directives.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py csco_control_tower_copilot
```

---

### #10 · SKU Pruning Agent (`working_capital_cash_bridge`)
- **Sub-Pillar**: Portfolio & SKU | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Category Manager · **ROI Benchmark**: `Frees 12%–20% Tail Capital` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Bottom 30%–50% of SKUs generate <5% of profit while trapping 25%+ of inventory. Unpruned long-tail SKUs, uncoordinated PIPO engineering cutovers, and static MOQs inflate changeover losses, obsolescence write-offs (1.5%–3% of COGS), and cost-to-serve.
- **The AI Solution**: Scores velocity, plant changeover cost, and shelf revenue yield.
- **Quantified Outcome**: Scores every SKU on true net contribution after carrying, changeover, and obsolescence cost—unlocking trapped working capital from the long tail.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🛒 SAP S/4HANA (SD/MM)**: Pulls daily store checkout scans (EDI 852), open customer orders, and baseline ERP demand forecasts.
- **☁️ BigQuery Demand Lake**: Streams real-time weather anomalies (Google DeepMind WeatherNext), foot-traffic indices, and channel sales.
- **🧠 Vertex AI TimesFM**: Foundation time-series forecasting model generating probabilistic P10/P50/P90 demand envelopes.
- **📊 SAP IBP**: Reconciles unconstrained commercial plans and publishes approved consensus forecast key figures.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and BigQuery) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Vertex) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Perform a portfolio rationalization and working capital cash bridge analysis across our active SKU catalog by querying SAP S/4HANA inventory valuation and BigQuery sales velocity data. Identify negative-margin tail SKUs with high days inventory outstanding (DIO), calculate trapped working capital, and generate a copyable CSV pruning schedule.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Render an interactive working capital cash release waterfall chart breaking down trapped cash across raw materials, work-in-progress, and finished goods, illustrating potential liquidity unlocked by pruning tail SKUs.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a formal portfolio rationalization brief and interactive HTML executive cash memo for the Chief Financial Officer and Commercial Leads outlining recommended SKU phase-outs and safety stock adjustments.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py working_capital_cash_bridge
```

---

### #11 · PIPO Run-Out Agent (`eco_cutover_orchestrator`)
- **Sub-Pillar**: Portfolio & SKU | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Lifecycle / Materials Mgr · **ROI Benchmark**: `-60%–80% Obsolescence Scrap` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Bottom 30%–50% of SKUs generate <5% of profit while trapping 25%+ of inventory. Unpruned long-tail SKUs, uncoordinated PIPO engineering cutovers, and static MOQs inflate changeover losses, obsolescence write-offs (1.5%–3% of COGS), and cost-to-serve.
- **The AI Solution**: Orchestrates transition buffers to sync packaging and formulation cuts.
- **Quantified Outcome**: Synchronizes old-component run-out with new-artwork/BOM ramp-up across plants and DCs to eliminate stranded packaging and obsolete inventory.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🛒 SAP S/4HANA (SD/MM)**: Pulls daily store checkout scans (EDI 852), open customer orders, and baseline ERP demand forecasts.
- **☁️ BigQuery Demand Lake**: Streams real-time weather anomalies (Google DeepMind WeatherNext), foot-traffic indices, and channel sales.
- **🧠 Vertex AI TimesFM**: Foundation time-series forecasting model generating probabilistic P10/P50/P90 demand envelopes.
- **📊 SAP IBP**: Reconciles unconstrained commercial plans and publishes approved consensus forecast key figures.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and BigQuery) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Vertex) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `How are our upcoming packaging and formula changeovers tracking, and where do we risk scrapping old materials or delaying the new version's launch date?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Create a chart comparing remaining old-version material run-out dates against target new-version launch dates across plants, and explain where the transition gap is widest.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Write a clear transition plan summary for Manufacturing, Procurement, and Marketing showing the recommended cutover dates and how we avoid material write-offs.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py eco_cutover_orchestrator
```

---

### #12 · Cost-to-Serve Diagnostic (`network_twin_architect`)
- **Sub-Pillar**: Portfolio & SKU | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Commercial Finance Director · **ROI Benchmark**: `-6%–11% Network Cost-to-Serve` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Bottom 30%–50% of SKUs generate <5% of profit while trapping 25%+ of inventory. Unpruned long-tail SKUs, uncoordinated PIPO engineering cutovers, and static MOQs inflate changeover losses, obsolescence write-offs (1.5%–3% of COGS), and cost-to-serve.
- **The AI Solution**: Calculates net-net margin across Club, Grocery, and eCommerce packs.
- **Quantified Outcome**: Computes granular SKU-customer-lane cost-to-serve and re-optimizes MOQs, pallet tiers, and DC sourcing assignments to restore pocket margin.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🛒 SAP S/4HANA (SD/MM)**: Pulls daily store checkout scans (EDI 852), open customer orders, and baseline ERP demand forecasts.
- **☁️ BigQuery Demand Lake**: Streams real-time weather anomalies (Google DeepMind WeatherNext), foot-traffic indices, and channel sales.
- **🧠 Vertex AI TimesFM**: Foundation time-series forecasting model generating probabilistic P10/P50/P90 demand envelopes.
- **📊 SAP IBP**: Reconciles unconstrained commercial plans and publishes approved consensus forecast key figures.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and BigQuery) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Vertex) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `When we include warehousing, handling, freight, and returns, which customer channels and pack formats are genuinely profitable to serve and which ones are quietly losing margin?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Show me a chart comparing gross revenue against true net margin after fulfillment and freight costs across our main channels and accounts.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a plain-English cost-to-serve summary for Commercial and Supply Chain leadership explaining where fulfillment costs are eroding profit and how order policies should change.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py network_twin_architect
```

---

## 02 · Sourcing & Procurement (9 Agents)
*Supplier Network, Material & Packaging, Contract & PO Management*

### #13 · Disruption Sensing Agent (`tier_n_risk_sentinel`)
- **Sub-Pillar**: Supplier Network | **Pillar**: 02 · Sourcing & Procurement
- **Primary Human Persona**: Procurement Dir. / Risk Mgr · **ROI Benchmark**: `-55% Disruption Downtime` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 42% of 1 year's EBITDA lost per decade to shocks · 65%+ originate in Tier-2+. Over 65% of supply disruptions originate in unmapped Tier-2/Tier-3 sub-suppliers, while manual supplier qualification and Scope 3 audits stall sourcing agility for 4–8 weeks.
- **The AI Solution**: Monitors multi-tier supply feeds, port delays, and vendor financials.
- **Quantified Outcome**: Continuously monitors sub-tier financial, geopolitical, weather, and port signals—triggering alternate allocations weeks before line stoppage.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🤝 SAP Ariba**: Manages supplier master agreements, active RFQ bid sheets, and multi-tier vendor compliance records.
- **📈 Commodity Indices (LME/ICIS)**: Live spot and futures market benchmarks for aluminum, steel, polymer resins, and corrugated packaging.
- **🕸️ Cloud Spanner Graph**: Multi-tier supply chain graph tracing Tier-1 to Tier-3 component lineage and sole-source bottlenecks.
- **📑 Accounts Payable OCR / EDI 810**: Automated 3-way matching across purchase orders, receiving dock receipts, and vendor invoices.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and Commodity) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Cloud) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Accounts).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Trace our end-to-end multi-tier bill of materials into Tier-2 and Tier-3 suppliers using Cloud Spanner Graph lineage and Dun & Bradstreet credit health feeds. Detect single-source dependencies, identify suppliers facing insolvency or regional shutdown risk, calculate downstream revenue at risk, and output a CSV risk ledger.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Generate an interactive multi-tier supplier network graph and risk radar visualizing tier-1 to tier-3 nodes, highlighting sole-source bottlenecks, geographic concentration, and operational risk tiers.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft an executive supplier resilience briefing and interactive HTML supply network audit report detailing secondary qualification timelines and recommended safety stock buffers for critical components.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py tier_n_risk_sentinel
```

---

### #14 · Onboarding & Qual. Agent (`supplier_quality_sentinel`)
- **Sub-Pillar**: Supplier Network | **Pillar**: 02 · Sourcing & Procurement
- **Primary Human Persona**: Procurement Operations Lead · **ROI Benchmark**: `-80% Onboarding Cycle Time` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 42% of 1 year's EBITDA lost per decade to shocks · 65%+ originate in Tier-2+. Over 65% of supply disruptions originate in unmapped Tier-2/Tier-3 sub-suppliers, while manual supplier qualification and Scope 3 audits stall sourcing agility for 4–8 weeks.
- **The AI Solution**: Parses BRC/ISO audits, food-safety filings, and tax registrations.
- **Quantified Outcome**: Automates ISO/HACCP certificate verification, financial health scoring, and sanctions screening—cutting vendor qualification from weeks to hours.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🤝 SAP Ariba**: Manages supplier master agreements, active RFQ bid sheets, and multi-tier vendor compliance records.
- **📈 Commodity Indices (LME/ICIS)**: Live spot and futures market benchmarks for aluminum, steel, polymer resins, and corrugated packaging.
- **🕸️ Cloud Spanner Graph**: Multi-tier supply chain graph tracing Tier-1 to Tier-3 component lineage and sole-source bottlenecks.
- **📑 Accounts Payable OCR / EDI 810**: Automated 3-way matching across purchase orders, receiving dock receipts, and vendor invoices.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and Commodity) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Cloud) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Accounts).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `How do our suppliers look on quality audits, food-safety certifications, and recent defect rates, and are any vendors close to failing compliance or expiring certifications?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Plot a chart comparing supplier quality scores and defect rates across active vendors so I can quickly spot who needs corrective action.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a clear quality and onboarding review note for Procurement and Quality Assurance detailing which suppliers are fully cleared and which require corrective plans.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py supplier_quality_sentinel
```

---

### #15 · ESG & Scope 3 Auditor (`carbon_scope3_ledger`)
- **Sub-Pillar**: Supplier Network | **Pillar**: 02 · Sourcing & Procurement
- **Primary Human Persona**: Chief Sustainability Officer · **ROI Benchmark**: `100% Audit-Ready Scope 3` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 42% of 1 year's EBITDA lost per decade to shocks · 65%+ originate in Tier-2+. Over 65% of supply disruptions originate in unmapped Tier-2/Tier-3 sub-suppliers, while manual supplier qualification and Scope 3 audits stall sourcing agility for 4–8 weeks.
- **The AI Solution**: Standardizes chain-of-custody certificates (RSPO/FSC) and packaging LCAs.
- **Quantified Outcome**: Replaces coarse spend-based averages with primary supplier + lane emissions—preventing EU CBAM penalties and cutting external assurance fees.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🤝 SAP Ariba**: Manages supplier master agreements, active RFQ bid sheets, and multi-tier vendor compliance records.
- **📈 Commodity Indices (LME/ICIS)**: Live spot and futures market benchmarks for aluminum, steel, polymer resins, and corrugated packaging.
- **🕸️ Cloud Spanner Graph**: Multi-tier supply chain graph tracing Tier-1 to Tier-3 component lineage and sole-source bottlenecks.
- **📑 Accounts Payable OCR / EDI 810**: Automated 3-way matching across purchase orders, receiving dock receipts, and vendor invoices.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and Commodity) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Cloud) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Accounts).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Audit our Scope 3 transportation and supplier emissions across global freight corridors by querying BigQuery telematics, SAP customs declarations, and Google Earth Engine EUDR deforestation verifications. Identify high-emission lane outliers, calculate EU CBAM tax liabilities, and output an auditable CSV carbon disclosure ledger.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Render an interactive Marginal Abatement Cost Curve (MACC) chart illustrating carbon reduction potential in metric tons versus dollar cost per ton across rail conversion, alternative biofuels, and green carrier awards.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft an executive sustainability compliance brief and interactive HTML carbon disclosure dossier for ESG auditors and Procurement leadership detailing progress toward 2030 net-zero targets.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py carbon_scope3_ledger
```

---

### #16 · Commodity Index Advisor (`commodity_index_advisor`)
- **Sub-Pillar**: Material & Packaging | **Pillar**: 02 · Sourcing & Procurement
- **Primary Human Persona**: Category Sourcing Mgr (Direct) · **ROI Benchmark**: `-4%–8% Direct Material Spend` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 6%–14% supplier quote variance vs. clean-sheet · rising EU EPR/PPWR fees. Without live commodity index decomposition and clean-sheet BOM models, buyers overpay by 5%–12% on direct materials and face escalating Extended Producer Responsibility (EPR) packaging levies.
- **The AI Solution**: Correlates CBOT/Platts feedstocks with depletion to advise hedging.
- **Quantified Outcome**: Tracks LME, resin, pulp, energy, and agri-commodity curves against BOM exposure to recommend optimal forward-contract split and index clauses.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🤝 SAP Ariba**: Manages supplier master agreements, active RFQ bid sheets, and multi-tier vendor compliance records.
- **📈 Commodity Indices (LME/ICIS)**: Live spot and futures market benchmarks for aluminum, steel, polymer resins, and corrugated packaging.
- **🕸️ Cloud Spanner Graph**: Multi-tier supply chain graph tracing Tier-1 to Tier-3 component lineage and sole-source bottlenecks.
- **📑 Accounts Payable OCR / EDI 810**: Automated 3-way matching across purchase orders, receiving dock receipts, and vendor invoices.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and Commodity) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Cloud) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Accounts).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `How are raw material and packaging commodity market prices moving compared to our current contract rates, and should we lock in forward hedges or wait?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Create a chart comparing live commodity market trends against our budgeted contract prices and inventory coverage across key feedstocks.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a clear market advisory note for Procurement and Treasury explaining recent commodity price swings, our cost exposure, and recommended hedging coverage.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py commodity_index_advisor
```

---

### #17 · Dynamic Should-Cost Agent (`rfq_should_cost_agent`)
- **Sub-Pillar**: Material & Packaging | **Pillar**: 02 · Sourcing & Procurement
- **Primary Human Persona**: Strategic Sourcing Lead · **ROI Benchmark**: `5%–10% RFP Spend Savings` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 6%–14% supplier quote variance vs. clean-sheet · rising EU EPR/PPWR fees. Without live commodity index decomposition and clean-sheet BOM models, buyers overpay by 5%–12% on direct materials and face escalating Extended Producer Responsibility (EPR) packaging levies.
- **The AI Solution**: Deconstructs packaging specs (resin weight, corrugate, conversion energy).
- **Quantified Outcome**: Decomposes every supplier quote into raw material, conversion, energy, logistics, and margin—arming buyers with hard clean-sheet leverage.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🤝 SAP Ariba**: Manages supplier master agreements, active RFQ bid sheets, and multi-tier vendor compliance records.
- **📈 Commodity Indices (LME/ICIS)**: Live spot and futures market benchmarks for aluminum, steel, polymer resins, and corrugated packaging.
- **🕸️ Cloud Spanner Graph**: Multi-tier supply chain graph tracing Tier-1 to Tier-3 component lineage and sole-source bottlenecks.
- **📑 Accounts Payable OCR / EDI 810**: Automated 3-way matching across purchase orders, receiving dock receipts, and vendor invoices.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and Commodity) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Cloud) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Accounts).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Conduct a bottom-up parametric should-cost teardown on incoming supplier packaging and component bids by querying SAP Ariba RFQs and live commodity indices from the London Metal Exchange and ICIS. Deconstruct quotes into raw material resin, machine cycle time, energy, and supplier margin, flag unearned price premiums, and output a CSV variance table.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Plot an interactive should-cost teardown waterfall chart contrasting supplier quoted prices with our bottom-up engineering baseline cost across raw material, direct labor, overhead, and margin.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft an executive category negotiation memo and interactive HTML should-cost dossier for procurement buyers outlining line-item negotiation targets and volume split recommendations.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py rfq_should_cost_agent
```

---

### #18 · Sustainable Packaging Agent (`sustainable_packaging_agent`)
- **Sub-Pillar**: Material & Packaging | **Pillar**: 02 · Sourcing & Procurement
- **Primary Human Persona**: Packaging R&D Engineer · **ROI Benchmark**: `-15%–25% EPR & Spec Cost` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 6%–14% supplier quote variance vs. clean-sheet · rising EU EPR/PPWR fees. Without live commodity index decomposition and clean-sheet BOM models, buyers overpay by 5%–12% on direct materials and face escalating Extended Producer Responsibility (EPR) packaging levies.
- **The AI Solution**: Evaluates PCR resins and barrier materials against line runnability & taxes.
- **Quantified Outcome**: Balances resin/fiber cost, crush/barrier physics, and country-by-country EPR/PPWR eco-modulation fees to lower total packaging cost.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🤝 SAP Ariba**: Manages supplier master agreements, active RFQ bid sheets, and multi-tier vendor compliance records.
- **📈 Commodity Indices (LME/ICIS)**: Live spot and futures market benchmarks for aluminum, steel, polymer resins, and corrugated packaging.
- **🕸️ Cloud Spanner Graph**: Multi-tier supply chain graph tracing Tier-1 to Tier-3 component lineage and sole-source bottlenecks.
- **📑 Accounts Payable OCR / EDI 810**: Automated 3-way matching across purchase orders, receiving dock receipts, and vendor invoices.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and Commodity) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Cloud) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Accounts).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `How do our proposed recycled and eco-friendly packaging options compare on cost, factory line speed, product shelf-life protection, and plastic tax savings?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Display a chart comparing total landed cost, recycled content, and line compatibility across candidate packaging materials, and explain the best choice clearly.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Write a plain-English packaging recommendation brief for Research and Development and Procurement comparing our top sustainable options and net cost impact.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py sustainable_packaging_agent
```

---

### #19 · Contract Leakage Agent (`tariff_esg_agent`)
- **Sub-Pillar**: Contract & PO Mgmt | **Pillar**: 02 · Sourcing & Procurement
- **Primary Human Persona**: Commercial Sourcing / Legal · **ROI Benchmark**: `Recovers 2%–4% Addressable Spend` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: $12.88–$15.96 per manual invoice vs. $2.18 digital · 3%–5% contract leakage. Enterprises lose 3%–5% of contracted savings to uncaptured volume rebates, off-contract price creep, missed 2/10 Net 30 early-pay discounts, and manual 3-way match holds.
- **The AI Solution**: Reconciles live spend against negotiated rebate tiers and volume discount scales.
- **Quantified Outcome**: Audits live POs and invoices against master PDF contract tiers, volume rebates, and de-escalation clauses to stop off-contract value leakage.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🤝 SAP Ariba**: Manages supplier master agreements, active RFQ bid sheets, and multi-tier vendor compliance records.
- **📈 Commodity Indices (LME/ICIS)**: Live spot and futures market benchmarks for aluminum, steel, polymer resins, and corrugated packaging.
- **🕸️ Cloud Spanner Graph**: Multi-tier supply chain graph tracing Tier-1 to Tier-3 component lineage and sole-source bottlenecks.
- **📑 Accounts Payable OCR / EDI 810**: Automated 3-way matching across purchase orders, receiving dock receipts, and vendor invoices.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and Commodity) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Cloud) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Accounts).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Where are we leaving money on the table by missing volume rebates, buying off-contract, or paying outdated supplier pricing tiers across active agreements?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Show me a chart comparing contracted pricing and earned volume rebates against actual invoiced spend across major suppliers, and point out the biggest leakage.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a clear contract value recovery memo for Sourcing and Legal summarizing missed rebates, off-contract spend, and how much money we can reclaim.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py tariff_esg_agent
```

---

### #20 · PO Expediting Agent (`master_data_leadtime_steward`)
- **Sub-Pillar**: Contract & PO Mgmt | **Pillar**: 02 · Sourcing & Procurement
- **Primary Human Persona**: Buyer / Procurement Coord. · **ROI Benchmark**: `-35%–50% Expedite Freight` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: $12.88–$15.96 per manual invoice vs. $2.18 digital · 3%–5% contract leakage. Enterprises lose 3%–5% of contracted savings to uncaptured volume rebates, off-contract price creep, missed 2/10 Net 30 early-pay discounts, and manual 3-way match holds.
- **The AI Solution**: Monitors EDI 855/856 delay feeds and orchestrates supplier split-shipments.
- **Quantified Outcome**: Continuously recalibrates ERP vendor lead times and autonomously resolves ~70% of routine PO acknowledgments and date slips before expedite crises.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🤝 SAP Ariba**: Manages supplier master agreements, active RFQ bid sheets, and multi-tier vendor compliance records.
- **📈 Commodity Indices (LME/ICIS)**: Live spot and futures market benchmarks for aluminum, steel, polymer resins, and corrugated packaging.
- **🕸️ Cloud Spanner Graph**: Multi-tier supply chain graph tracing Tier-1 to Tier-3 component lineage and sole-source bottlenecks.
- **📑 Accounts Payable OCR / EDI 810**: Automated 3-way matching across purchase orders, receiving dock receipts, and vendor invoices.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and Commodity) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Cloud) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Accounts).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Which open supplier purchase orders are running late compared to promised delivery dates, and which delays threaten to stop production or cause stockouts?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Plot a chart comparing promised supplier lead times against actual transit and delivery delays across open purchase orders so we can prioritize expediting.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Prepare an actionable expediting summary for our buyers listing the most critical delayed purchase orders, plant impact, and split-shipment options.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py master_data_leadtime_steward
```

---

### #21 · Three-Way Match Dispute (`three_way_match_dispute`)
- **Sub-Pillar**: Contract & PO Mgmt | **Pillar**: 02 · Sourcing & Procurement
- **Primary Human Persona**: Accounts Payable Lead · **ROI Benchmark**: `-80% Invoice Exception Cost` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: $12.88–$15.96 per manual invoice vs. $2.18 digital · 3%–5% contract leakage. Enterprises lose 3%–5% of contracted savings to uncaptured volume rebates, off-contract price creep, missed 2/10 Net 30 early-pay discounts, and manual 3-way match holds.
- **The AI Solution**: Diagnoses price/quantity discrepancies across POs, GRNs, and carrier invoices.
- **Quantified Outcome**: Reconciles PO, Goods Receipt (ASN/GRN), and Invoice line variances automatically—capturing early-payment discounts and cutting AP unit cost by 80%.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🤝 SAP Ariba**: Manages supplier master agreements, active RFQ bid sheets, and multi-tier vendor compliance records.
- **📈 Commodity Indices (LME/ICIS)**: Live spot and futures market benchmarks for aluminum, steel, polymer resins, and corrugated packaging.
- **🕸️ Cloud Spanner Graph**: Multi-tier supply chain graph tracing Tier-1 to Tier-3 component lineage and sole-source bottlenecks.
- **📑 Accounts Payable OCR / EDI 810**: Automated 3-way matching across purchase orders, receiving dock receipts, and vendor invoices.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and Commodity) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Cloud) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Accounts).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Audit pending vendor invoices by performing automated 3-way matching across SAP S/4HANA purchase orders, Manhattan WMS receiving receipts, and OCR invoice headers. Detect price creep, freight charge discrepancies, and quantity shortages, calculate early-payment discount capture windows, and generate an AP discrepancy CSV schedule.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Render an interactive 3-way match variance chart highlighting disputed dollar amounts by category (unapproved price variance, missing goods receipt, accessorial overcharges) versus discount savings captured.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a formal vendor debit memo and remittance advice document along with an interactive HTML AP settlement brief detailing line-item deductions, approved payable balances, and ERP posting references.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py three_way_match_dispute
```

---

## 03 · Manufacturing & Production (9 Agents)
*Production Scheduling, Capacity Planning, Quality & Compliance*

### #22 · Changeover Optimizer (`finite_production_scheduler`)
- **Sub-Pillar**: Production Scheduling | **Pillar**: 03 · Manufacturing & Production
- **Primary Human Persona**: Master Production Scheduler · **ROI Benchmark**: `+4–7 pts Line OEE Lift` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 12%–22% scheduled runtime lost to changeovers & reactive line re-sequencing. Sequence-blind ERP schedules trigger excessive allergen/color washouts, uncertified shift bottlenecks, and hours of manual schedule rebuilding whenever a machine or material slips.
- **The AI Solution**: Sequences allergen, kosher, and packaging runs to minimize washdowns.
- **Quantified Outcome**: Solves finite-capacity campaign wheels across allergens, colors, and pack formats—cutting sanitation/changeover downtime by 15%–25%.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **⚙️ Siemens Opcenter MES**: Live plant machine work center status, run rates, job dispatch queues, and maintenance schedules.
- **🏭 SAP PP/DS**: Planned production orders, bill of material routings, and plant line capacity envelopes.
- **📡 SCADA / IoT Vibration Telemetry**: Industrial vibration FFT spectrograms, bearing temperatures, and predictive failure alarms.
- **🎯 Google OR-Tools CP-SAT**: Finite capacity constraint solver minimizing sequence-dependent wash and changeover downtime.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Siemens and SAP) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (SCADA) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Optimize our plant manufacturing schedule across active packaging and filling lines by querying SAP PP/DS production orders and Siemens Opcenter MES work center states. Run Google OR-Tools CP-SAT to minimize sequence-dependent wash and changeover downtime between allergen and flavor families, respect tooling constraints, and output a CSV machine dispatch schedule.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Generate an interactive multi-line production Gantt schedule visual displaying job sequences, setup changeover blocks, maintenance windows, and order completion milestones across all plant lines.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a plant floor shift handover briefing note and interactive HTML master production schedule for plant superintendents and operations leadership summarizing throughput gains and scheduled changeover reductions.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py finite_production_scheduler
```

---

### #23 · Disruption Re-sequencer (`line_schedule_optimizer`)
- **Sub-Pillar**: Production Scheduling | **Pillar**: 03 · Manufacturing & Production
- **Primary Human Persona**: Shop Floor / Shift Lead · **ROI Benchmark**: `-40% Disruption Output Loss` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 12%–22% scheduled runtime lost to changeovers & reactive line re-sequencing. Sequence-blind ERP schedules trigger excessive allergen/color washouts, uncertified shift bottlenecks, and hours of manual schedule rebuilding whenever a machine or material slips.
- **The AI Solution**: Detects machine halts and re-routes perishable WIP to alternate lines.
- **Quantified Outcome**: Re-optimizes shift schedules in under 3 minutes when a filler trips or raw material arrives late—minimizing lost cases and missed dispatch waves.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **⚙️ Siemens Opcenter MES**: Live plant machine work center status, run rates, job dispatch queues, and maintenance schedules.
- **🏭 SAP PP/DS**: Planned production orders, bill of material routings, and plant line capacity envelopes.
- **📡 SCADA / IoT Vibration Telemetry**: Industrial vibration FFT spectrograms, bearing temperatures, and predictive failure alarms.
- **🎯 Google OR-Tools CP-SAT**: Finite capacity constraint solver minimizing sequence-dependent wash and changeover downtime.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Siemens and SAP) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (SCADA) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `We have unexpected machine slowdowns and stops on the shop floor—which work-in-progress batches are at risk of spoiling or missing customer cutoffs, and which alternate lines can take them?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Create a chart comparing remaining batch shelf-life windows against alternate production line availability and recovery output.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a crisp shift-handover recovery note for shop-floor supervisors detailing which halted batches to reroute, to which lines, and in what order.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py line_schedule_optimizer
```

---

### #24 · Labor & Line Balancing (`labor_line_balancing_agent`)
- **Sub-Pillar**: Production Scheduling | **Pillar**: 03 · Manufacturing & Production
- **Primary Human Persona**: Plant Operations Manager · **ROI Benchmark**: `+8%–12% Direct Labor Output` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 12%–22% scheduled runtime lost to changeovers & reactive line re-sequencing. Sequence-blind ERP schedules trigger excessive allergen/color washouts, uncertified shift bottlenecks, and hours of manual schedule rebuilding whenever a machine or material slips.
- **The AI Solution**: Maps shift skill certifications and fatigue constraints to line speeds.
- **Quantified Outcome**: Matches certified operator skills, absenteeism signals, and ergonomic rotation rules to live line schedules—cutting overtime and micro-stoppages.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **⚙️ Siemens Opcenter MES**: Live plant machine work center status, run rates, job dispatch queues, and maintenance schedules.
- **🏭 SAP PP/DS**: Planned production orders, bill of material routings, and plant line capacity envelopes.
- **📡 SCADA / IoT Vibration Telemetry**: Industrial vibration FFT spectrograms, bearing temperatures, and predictive failure alarms.
- **🎯 Google OR-Tools CP-SAT**: Finite capacity constraint solver minimizing sequence-dependent wash and changeover downtime.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Siemens and SAP) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (SCADA) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Do we have the right mix of certified operators assigned across shifts and packaging lines today, or are staffing gaps and overtime fatigue slowing down output?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Show me a chart comparing required operator staffing and skill coverage against actual shift assignments across our production lines.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Prepare a clear shift staffing summary for the Plant Manager highlighting operator bottlenecks, overtime fatigue risks, and recommended cross-line reassignments.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py labor_line_balancing_agent
```

---

### #25 · Bottleneck Diagnostic (`predictive_oee_sentinel`)
- **Sub-Pillar**: Capacity Planning | **Pillar**: 03 · Manufacturing & Production
- **Primary Human Persona**: Supply Chain Ops Director · **ROI Benchmark**: `-30%–45% Unplanned Stops` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 5%–20% of manufacturing capacity lost to unplanned downtime ($50B+/yr). Late detection of OEE bottlenecks forces reactive external co-packer allocation (+12%–25% unit cost penalty) and poorly targeted CapEx expansions.
- **The AI Solution**: Assesses CIP utilities, boiler loads, and cold storage holding limits.
- **Quantified Outcome**: Combines PLC telemetry with 6-month Rough-Cut Capacity Planning (RCCP) to prevent unplanned breakdowns and expose plant bottlenecks months ahead.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **⚙️ Siemens Opcenter MES**: Live plant machine work center status, run rates, job dispatch queues, and maintenance schedules.
- **🏭 SAP PP/DS**: Planned production orders, bill of material routings, and plant line capacity envelopes.
- **📡 SCADA / IoT Vibration Telemetry**: Industrial vibration FFT spectrograms, bearing temperatures, and predictive failure alarms.
- **🎯 Google OR-Tools CP-SAT**: Finite capacity constraint solver minimizing sequence-dependent wash and changeover downtime.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Siemens and SAP) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (SCADA) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Diagnose line micro-stoppages and equipment degradation across critical plant packaging machines by querying Siemens SCADA telemetry and BigQuery historical sensor readings. Isolate the Six Big Losses (unplanned downtime, speed loss, minor stops), verify critical spare parts in SAP PM, and output a CSV machine anomaly log.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Render an interactive OEE breakdown waterfall and loss Pareto chart decomposing planned production time into Availability, Performance, and Quality components across each work center.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft an executive plant maintenance briefing and interactive HTML OEE diagnostic dashboard for the Plant Director recommending planned predictive maintenance intervals and spare parts replenishment.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py predictive_oee_sentinel
```

---

### #26 · Co-Packer Allocation (`copacker_allocation_agent`)
- **Sub-Pillar**: Capacity Planning | **Pillar**: 03 · Manufacturing & Production
- **Primary Human Persona**: External Sourcing / CMO Lead · **ROI Benchmark**: `-8%–14% External Tolling Cost` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 5%–20% of manufacturing capacity lost to unplanned downtime ($50B+/yr). Late detection of OEE bottlenecks forces reactive external co-packer allocation (+12%–25% unit cost penalty) and poorly targeted CapEx expansions.
- **The AI Solution**: Models internal conversion costs against co-packer tolling agreements.
- **Quantified Outcome**: Allocates SKUs across internal plants and external CMOs by optimizing conversion fees, component freight, MOQ tiers, and delivered gross margin.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **⚙️ Siemens Opcenter MES**: Live plant machine work center status, run rates, job dispatch queues, and maintenance schedules.
- **🏭 SAP PP/DS**: Planned production orders, bill of material routings, and plant line capacity envelopes.
- **📡 SCADA / IoT Vibration Telemetry**: Industrial vibration FFT spectrograms, bearing temperatures, and predictive failure alarms.
- **🎯 Google OR-Tools CP-SAT**: Finite capacity constraint solver minimizing sequence-dependent wash and changeover downtime.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Siemens and SAP) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (SCADA) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Given our internal plant capacity and conversion costs versus external co-packer fees and freight, which products should we build in-house and which should go to contract manufacturers?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Show me a chart comparing all-in unit cost between internal production and external co-packers across candidate product families.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a clear make-versus-buy recommendation memo for Manufacturing and Sourcing leaders showing the optimal co-packer volume split and net cost savings.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py copacker_allocation_agent
```

---

### #27 · CapEx Simulator (`capex_simulator_agent`)
- **Sub-Pillar**: Capacity Planning | **Pillar**: 03 · Manufacturing & Production
- **Primary Human Persona**: VP Manufacturing Engineering · **ROI Benchmark**: `Avoids 15%–25% Idle CapEx` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 5%–20% of manufacturing capacity lost to unplanned downtime ($50B+/yr). Late detection of OEE bottlenecks forces reactive external co-packer allocation (+12%–25% unit cost penalty) and poorly targeted CapEx expansions.
- **The AI Solution**: Simulates multi-year volume trends to test high-speed line expansions.
- **Quantified Outcome**: Stress-tests new line, automation, and plant investments across stochastic demand, tariff, and OEE scenarios before committing board capital.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **⚙️ Siemens Opcenter MES**: Live plant machine work center status, run rates, job dispatch queues, and maintenance schedules.
- **🏭 SAP PP/DS**: Planned production orders, bill of material routings, and plant line capacity envelopes.
- **📡 SCADA / IoT Vibration Telemetry**: Industrial vibration FFT spectrograms, bearing temperatures, and predictive failure alarms.
- **🎯 Google OR-Tools CP-SAT**: Finite capacity constraint solver minimizing sequence-dependent wash and changeover downtime.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Siemens and SAP) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (SCADA) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Looking at multi-year demand growth across regions, when will our existing factories run out of capacity, and which capital equipment expansion gives the strongest financial payback?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Display a chart comparing multi-year capacity shortfall, capital investment cost, and net present value across our proposed line expansion options.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Prepare an executive capital investment memo for Engineering and Finance comparing the proposed factory expansion options, payback timeline, and risk.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py capex_simulator_agent
```

---

### #28 · Visual Defect Triager (`inline_yield_guardian`)
- **Sub-Pillar**: Quality & Compliance | **Pillar**: 03 · Manufacturing & Production
- **Primary Human Persona**: QA Manager / Line Inspector · **ROI Benchmark**: `-35%–50% Quality Scrap` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: COPQ erodes 3%–8% of manufacturing COGS · 7–18 days manual batch QA hold. End-of-line sampling catches defects only after full pallets are produced, while manual paper/PDF batch record review traps finished goods in quarantine for 1–2+ weeks.
- **The AI Solution**: Inspects high-speed video frames for crimped seals, lot codes, and labels.
- **Quantified Outcome**: Detects seal, fill, label, and surface defects inline in milliseconds—halting drift before whole pallets turn into scrap or rework.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **⚙️ Siemens Opcenter MES**: Live plant machine work center status, run rates, job dispatch queues, and maintenance schedules.
- **🏭 SAP PP/DS**: Planned production orders, bill of material routings, and plant line capacity envelopes.
- **📡 SCADA / IoT Vibration Telemetry**: Industrial vibration FFT spectrograms, bearing temperatures, and predictive failure alarms.
- **🎯 Google OR-Tools CP-SAT**: Finite capacity constraint solver minimizing sequence-dependent wash and changeover downtime.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Siemens and SAP) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (SCADA) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Analyze high-speed optical vision inspection frames across our packaging and bottling lines using Gemini 3.8 Flash image classification and Siemens MES electronic batch records. Detect container micro-fractures, cap seal misalignments, and foreign inclusions, calculate batch scrap yield impact, and output an inspection CSV classification log.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Generate an interactive visual defect spatial heatmap and bounding box distribution illustrating defect concentration zones across line speeds and container geometries.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a formal Non-Conformance Report (NCR) and interactive HTML batch quality dossier for Quality Assurance and Plant Management detailing root-cause findings and automated reject gate calibrations.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py inline_yield_guardian
```

---

### #29 · Batch Record Auditor (`batch_record_auditor`)
- **Sub-Pillar**: Quality & Compliance | **Pillar**: 03 · Manufacturing & Production
- **Primary Human Persona**: Regulatory Compliance Lead · **ROI Benchmark**: `-70% Batch Release Lead Time` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: COPQ erodes 3%–8% of manufacturing COGS · 7–18 days manual batch QA hold. End-of-line sampling catches defects only after full pallets are produced, while manual paper/PDF batch record review traps finished goods in quarantine for 1–2+ weeks.
- **The AI Solution**: Parses BPR and COA documents to flag pasteurization & CCP deviations.
- **Quantified Outcome**: Audits electronic/scanned batch records, LIMS lab results, and sterilization logs automatically—freeing millions in quarantined finished goods.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **⚙️ Siemens Opcenter MES**: Live plant machine work center status, run rates, job dispatch queues, and maintenance schedules.
- **🏭 SAP PP/DS**: Planned production orders, bill of material routings, and plant line capacity envelopes.
- **📡 SCADA / IoT Vibration Telemetry**: Industrial vibration FFT spectrograms, bearing temperatures, and predictive failure alarms.
- **🎯 Google OR-Tools CP-SAT**: Finite capacity constraint solver minimizing sequence-dependent wash and changeover downtime.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Siemens and SAP) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (SCADA) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Can you audit our recent production batch records and lab certificates to tell me which batches passed every critical safety check cleanly and which ones have deviations blocking release?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Create a chart comparing recorded batch processing parameters (such as pasteurization temperature and hold time) against regulatory limits across active lots.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Write a clear regulatory compliance review summary for Quality Assurance listing batches ready for fast release and detailing any critical deviations requiring investigation.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py batch_record_auditor
```

---

### #30 · RCA & CAPA Copilot (`scrap_defect_root_cause_agent`)
- **Sub-Pillar**: Quality & Compliance | **Pillar**: 03 · Manufacturing & Production
- **Primary Human Persona**: Continuous Improvement Lead · **ROI Benchmark**: `-40%–55% Repeat Quality Loss` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: COPQ erodes 3%–8% of manufacturing COGS · 7–18 days manual batch QA hold. End-of-line sampling catches defects only after full pallets are produced, while manual paper/PDF batch record review traps finished goods in quarantine for 1–2+ weeks.
- **The AI Solution**: Correlates consumer complaints with ingredient lots and machine telemetry.
- **Quantified Outcome**: Correlates supplier raw-material lots, ambient humidity, operator shifts, and machine parameters to isolate true root causes and prevent repeat scrap.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **⚙️ Siemens Opcenter MES**: Live plant machine work center status, run rates, job dispatch queues, and maintenance schedules.
- **🏭 SAP PP/DS**: Planned production orders, bill of material routings, and plant line capacity envelopes.
- **📡 SCADA / IoT Vibration Telemetry**: Industrial vibration FFT spectrograms, bearing temperatures, and predictive failure alarms.
- **🎯 Google OR-Tools CP-SAT**: Finite capacity constraint solver minimizing sequence-dependent wash and changeover downtime.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Siemens and SAP) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (SCADA) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Why did scrap and customer quality complaints spike recently—does the pattern trace back to a specific raw ingredient supplier lot, shift, or machine setting?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Show me a chart correlating defect and complaint rates across ingredient lots and machine operating conditions to pinpoint the primary root cause.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a plain-English root-cause and corrective action report for Quality and Plant Engineering explaining what caused the defect spike and how to prevent recurrence.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py scrap_defect_root_cause_agent
```

---

## 04 · Inventory & Warehousing (9 Agents)
*Positioning & Optimization (MEIO), 3D Warehouse Operations, Omnichannel ATP*

### #31 · Safety Stock Agent (`meio_safety_stock_agent`)
- **Sub-Pillar**: Positioning & Optimization | **Pillar**: 04 · Inventory & Warehousing
- **Primary Human Persona**: Inventory Optimization Lead · **ROI Benchmark**: `-12%–22% Safety Stock Capital` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 25%–32% annual inventory carrying cost · 20%–35% excess single-node buffer. Static ERP reorder rules buffer each DC independently—trapping 20%–35% excess working capital in slow movers while fast-moving regional hubs still suffer stockouts.
- **The AI Solution**: Recalibrates multi-echelon buffers using live lead-time and demand variance.
- **Quantified Outcome**: Simultaneously optimizes safety stocks across plants, central hubs, and regional DCs—freeing 12%–22% in working capital while lifting fill rates.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **📦 Manhattan Active WMS**: Real-time bin/aisle slotting, picker travel telemetry, wave release queues, and dock door schedules.
- **🌐 Cloud Spanner ATP**: Sub-50ms distributed transactional ledger maintaining committed customer orders and available inventory.
- **⚖️ Clark-Scarf MEIO Optimizer**: Coupled stochastic inventory solver balancing safety stock across Plants, RDCs, and Dark Stores.
- **🏢 SAP EWM**: Plant-to-warehouse stock transfer orders, pallet serialization, and inventory reconciliation.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Manhattan and Cloud) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Clark-Scarf) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Execute a Clark-Scarf multi-echelon inventory optimization (MEIO) across our central plants, regional distribution centers, and forward fulfillment hubs using SAP S/4HANA stock levels and BigQuery lead time variability data. Calculate optimal safety stock buffers to guarantee 99.2% customer OTIF while minimizing trapped working capital, and generate a CSV rebalancing schedule.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Render an interactive multi-echelon stocking post visualization comparing current inventory positioning against the optimized posture across each supply echelon.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft an inventory strategy memorandum and interactive HTML inventory health report for the Inventory Director outlining recommended reorder points, lateral transfers, and freed working capital.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py meio_safety_stock_agent
```

---

### #32 · SLOB Disposition Agent (`slob_disposition_agent`)
- **Sub-Pillar**: Positioning & Optimization | **Pillar**: 04 · Inventory & Warehousing
- **Primary Human Persona**: Inventory Controller / Buyer · **ROI Benchmark**: `+25%–40% Aged Stock Recovery` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 25%–32% annual inventory carrying cost · 20%–35% excess single-node buffer. Static ERP reorder rules buffer each DC independently—trapping 20%–35% excess working capital in slow movers while fast-moving regional hubs still suffer stockouts.
- **The AI Solution**: Analyzes shelf-life risk and triggers promotional bundles or liquidations.
- **Quantified Outcome**: Flags slow-moving and aging lots 60–90 days earlier and ranks inter-DC transfer, promo bundling, or secondary channels to avoid write-offs.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **📦 Manhattan Active WMS**: Real-time bin/aisle slotting, picker travel telemetry, wave release queues, and dock door schedules.
- **🌐 Cloud Spanner ATP**: Sub-50ms distributed transactional ledger maintaining committed customer orders and available inventory.
- **⚖️ Clark-Scarf MEIO Optimizer**: Coupled stochastic inventory solver balancing safety stock across Plants, RDCs, and Dark Stores.
- **🏢 SAP EWM**: Plant-to-warehouse stock transfer orders, pallet serialization, and inventory reconciliation.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Manhattan and Cloud) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Clark-Scarf) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Which slow-moving or aging inventory lots in our warehouses are at risk of expiring or becoming obsolete, and what is the highest-recovery way to clear them?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Plot a chart comparing aging inventory value and remaining shelf life against expected cash recovery across promo bundling, discount channels, and liquidation.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a practical inventory disposition plan for Merchandising and Finance recommending how to clear at-risk stock while recovering maximum margin.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py slob_disposition_agent
```

---

### #33 · Inter-Facility Rebalancer (`crossdock_transfer_orchestrator`)
- **Sub-Pillar**: Positioning & Optimization | **Pillar**: 04 · Inventory & Warehousing
- **Primary Human Persona**: Replenishment Planner · **ROI Benchmark**: `-35%–50% Lost-Sale Stockouts` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 25%–32% annual inventory carrying cost · 20%–35% excess single-node buffer. Static ERP reorder rules buffer each DC independently—trapping 20%–35% excess working capital in slow movers while fast-moving regional hubs still suffer stockouts.
- **The AI Solution**: Generates automated inter-DC and store transfers to balance localized gluts.
- **Quantified Outcome**: Balances inventory imbalances across regional DCs before stockouts hit—weighing transfer freight cost against saved gross margin and OTIF penalties.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **📦 Manhattan Active WMS**: Real-time bin/aisle slotting, picker travel telemetry, wave release queues, and dock door schedules.
- **🌐 Cloud Spanner ATP**: Sub-50ms distributed transactional ledger maintaining committed customer orders and available inventory.
- **⚖️ Clark-Scarf MEIO Optimizer**: Coupled stochastic inventory solver balancing safety stock across Plants, RDCs, and Dark Stores.
- **🏢 SAP EWM**: Plant-to-warehouse stock transfer orders, pallet serialization, and inventory reconciliation.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Manhattan and Cloud) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Clark-Scarf) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Do we have products stocked out in one regional warehouse while sitting in excess at another hub nearby, and which inter-warehouse transfers make financial sense after freight cost?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Show me a chart comparing regional stockout exposure against nearby surplus inventory and net margin saved after transfer freight.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Write a clear inventory rebalancing summary for Replenishment Planners listing which stock transfers to run between hubs and the customer orders they will save.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py crossdock_transfer_orchestrator
```

---

### #34 · Dynamic Slotting Agent (`warehouse_slotting_agent`)
- **Sub-Pillar**: Warehouse Operations | **Pillar**: 04 · Inventory & Warehousing
- **Primary Human Persona**: DC Operations Mgr / IE Lead · **ROI Benchmark**: `-15%–28% Picker Travel Time` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Order picking = 50%–55% of DC operating cost · ~55% of picker time is walking. Static warehouse slotting, congested receiving docks (6–24h dock-to-stock lag), and rigid wave releases waste over half of floor labor in unproductive travel and overtime.
- **The AI Solution**: Evaluates co-pick affinity matrices to recommend fast-pick zone re-slotting.
- **Quantified Outcome**: Re-slots fast-moving and co-ordered SKUs into ergonomic golden zones and optimizes TSP pick paths—boosting DC throughput with $0 automation CapEx.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **📦 Manhattan Active WMS**: Real-time bin/aisle slotting, picker travel telemetry, wave release queues, and dock door schedules.
- **🌐 Cloud Spanner ATP**: Sub-50ms distributed transactional ledger maintaining committed customer orders and available inventory.
- **⚖️ Clark-Scarf MEIO Optimizer**: Coupled stochastic inventory solver balancing safety stock across Plants, RDCs, and Dark Stores.
- **🏢 SAP EWM**: Plant-to-warehouse stock transfer orders, pallet serialization, and inventory reconciliation.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Manhattan and Cloud) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Clark-Scarf) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Re-slot our high-bay automated warehouse by evaluating SKU picking velocity, cube dimensions, and order pick paths from Manhattan Active WMS and AMR robot telemetry. Identify fast-moving SKUs trapped in upper levels, calculate picker travel distance reduction, and output an actionable CSV slot-move execution table.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Generate an interactive 3D warehouse rack elevation and velocity heatmap visual showing SKU positioning across golden picking zones, overhead storage, and aisle congestion tiers.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a warehouse operations briefing note and interactive HTML slotting visualizer for the DC General Manager detailing labor travel hours saved, ergonomic improvements, and wave completion speedups.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py warehouse_slotting_agent
```

---

### #35 · Dock-to-Stock Agent (`dock_to_stock_agent`)
- **Sub-Pillar**: Warehouse Operations | **Pillar**: 04 · Inventory & Warehousing
- **Primary Human Persona**: Inbound Receiving Supervisor · **ROI Benchmark**: `-75% Dock-to-Stock Latency` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Order picking = 50%–55% of DC operating cost · ~55% of picker time is walking. Static warehouse slotting, congested receiving docks (6–24h dock-to-stock lag), and rigid wave releases waste over half of floor labor in unproductive travel and overtime.
- **The AI Solution**: Parses scanned BOLs and pallet photos to reconcile open ASN variances.
- **Quantified Outcome**: Prioritizes inbound trailers holding stockout/backorder SKUs and directs instant putaway or cross-docking—clearing receiving bottlenecks.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **📦 Manhattan Active WMS**: Real-time bin/aisle slotting, picker travel telemetry, wave release queues, and dock door schedules.
- **🌐 Cloud Spanner ATP**: Sub-50ms distributed transactional ledger maintaining committed customer orders and available inventory.
- **⚖️ Clark-Scarf MEIO Optimizer**: Coupled stochastic inventory solver balancing safety stock across Plants, RDCs, and Dark Stores.
- **🏢 SAP EWM**: Plant-to-warehouse stock transfer orders, pallet serialization, and inventory reconciliation.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Manhattan and Cloud) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Clark-Scarf) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Which inbound trucks and unloaded pallets at our receiving docks have mismatches against advance shipping notices or are stuck waiting to be put away into sellable stock?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Show me a chart comparing dock-to-stock putaway cycle times and quantity variances across recent inbound shipments.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Prepare a clear receiving exception summary for the Inbound Dock Supervisor highlighting discrepant shipments, urgent out-of-stock items on the dock, and priority putaway tasks.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py dock_to_stock_agent
```

---

### #36 · Wave Fulfillment Copilot (`wave_fulfillment_copilot`)
- **Sub-Pillar**: Warehouse Operations | **Pillar**: 04 · Inventory & Warehousing
- **Primary Human Persona**: DC Shift Floor Lead · **ROI Benchmark**: `-30% DC Rush Overtime` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Order picking = 50%–55% of DC operating cost · ~55% of picker time is walking. Static warehouse slotting, congested receiving docks (6–24h dock-to-stock lag), and rigid wave releases waste over half of floor labor in unproductive travel and overtime.
- **The AI Solution**: Balances picker lines dynamically to protect carrier pickup cutoff times.
- **Quantified Outcome**: Monitors pick, sort, and pack-wall queues in real time—re-prioritizing waves and labor zones so every carrier trailer departs on time in full.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **📦 Manhattan Active WMS**: Real-time bin/aisle slotting, picker travel telemetry, wave release queues, and dock door schedules.
- **🌐 Cloud Spanner ATP**: Sub-50ms distributed transactional ledger maintaining committed customer orders and available inventory.
- **⚖️ Clark-Scarf MEIO Optimizer**: Coupled stochastic inventory solver balancing safety stock across Plants, RDCs, and Dark Stores.
- **🏢 SAP EWM**: Plant-to-warehouse stock transfer orders, pallet serialization, and inventory reconciliation.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Manhattan and Cloud) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Clark-Scarf) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `How are our active warehouse picking and packing waves progressing against today's carrier departure cutoffs, and which zones need labor rebalanced right now?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Plot a chart comparing remaining pick-wave workload against available labor capacity and carrier cutoff countdowns across warehouse zones.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a quick floor-action note for Shift Leads detailing which zones are falling behind cutoff, how many pickers to move, and which customer orders to prioritize.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py wave_fulfillment_copilot
```

---

### #37 · Phantom Inventory Sensor (`planogram_merchandising_vision_auditor`)
- **Sub-Pillar**: Omnichannel Visibility | **Pillar**: 04 · Inventory & Warehousing
- **Primary Human Persona**: Store Operations / Omni Lead · **ROI Benchmark**: `+2.5%–4% On-Shelf Sales Lift` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 8%–15% store inventory record inaccuracy · 2.1x parcel cost on split orders. Phantom store stock triggers 6%–12% BOPIS/Ship-From-Store cancellations and costly multi-node split shipments, while sellable returns sit un-restocked for 5–14 days.
- **The AI Solution**: Identifies shrinkage anomalies when on-hand stock stops scanning at POS.
- **Quantified Outcome**: Detects zero-scan POS velocity anomalies and shelf gaps to eliminate phantom inventory—lifting on-shelf availability and stopping BOPIS cancels.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **📦 Manhattan Active WMS**: Real-time bin/aisle slotting, picker travel telemetry, wave release queues, and dock door schedules.
- **🌐 Cloud Spanner ATP**: Sub-50ms distributed transactional ledger maintaining committed customer orders and available inventory.
- **⚖️ Clark-Scarf MEIO Optimizer**: Coupled stochastic inventory solver balancing safety stock across Plants, RDCs, and Dark Stores.
- **🏢 SAP EWM**: Plant-to-warehouse stock transfer orders, pallet serialization, and inventory reconciliation.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Manhattan and Cloud) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Clark-Scarf) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Where does our store inventory system claim stock is on hand, yet zero units are scanning at checkout—pointing to phantom inventory, misplaced backroom stock, or shrink?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Show me a chart comparing recorded on-hand store inventory against expected versus actual checkout scan velocity to spotlight phantom stock anomalies.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Write a clear store operations alert note listing the top phantom-inventory stores and items so associates can audit shelves and trigger replenishment.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py planogram_merchandising_vision_auditor
```

---

### #38 · SFS / BOPIS Sourcing (`atp_order_promising_agent`)
- **Sub-Pillar**: Omnichannel Visibility | **Pillar**: 04 · Inventory & Warehousing
- **Primary Human Persona**: Omnichannel Fulfillment Dir. · **ROI Benchmark**: `-15%–25% Parcel & Split Cost` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 8%–15% store inventory record inaccuracy · 2.1x parcel cost on split orders. Phantom store stock triggers 6%–12% BOPIS/Ship-From-Store cancellations and costly multi-node split shipments, while sellable returns sit un-restocked for 5–14 days.
- **The AI Solution**: Selects lowest-cost fulfillment nodes based on store labor and parcel zones.
- **Quantified Outcome**: Routes every e-commerce and BOPIS order to the DC or store that maximizes net order margin across parcel zone cost, split risk, and markdown avoidance.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **📦 Manhattan Active WMS**: Real-time bin/aisle slotting, picker travel telemetry, wave release queues, and dock door schedules.
- **🌐 Cloud Spanner ATP**: Sub-50ms distributed transactional ledger maintaining committed customer orders and available inventory.
- **⚖️ Clark-Scarf MEIO Optimizer**: Coupled stochastic inventory solver balancing safety stock across Plants, RDCs, and Dark Stores.
- **🏢 SAP EWM**: Plant-to-warehouse stock transfer orders, pallet serialization, and inventory reconciliation.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Manhattan and Cloud) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Clark-Scarf) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Evaluate incoming high-priority customer orders against real-time global inventory in Cloud Spanner and order requests in Salesforce Commerce Cloud. Determine optimal fulfillment routing between Distribution Centers, Ship-From-Store (SFS), and Direct-Store-Delivery (DSD) to eliminate split shipments while protecting contractual SLAs, and generate an order fulfillment CSV schedule.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Render an interactive omnichannel fulfillment cost and routing matrix chart comparing delivery speed and margin impact across alternate fulfillment nodes.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft an omnichannel order promising executive memo and interactive HTML order routing brief for Customer Operations leadership outlining fulfillment decisions and SLA protections.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py atp_order_promising_agent
```

---

### #39 · Returns Triage Agent (`returns_triage_agent`)
- **Sub-Pillar**: Omnichannel Visibility | **Pillar**: 04 · Inventory & Warehousing
- **Primary Human Persona**: Reverse Logistics Lead · **ROI Benchmark**: `+18%–30% Full-Price Recovery` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 8%–15% store inventory record inaccuracy · 2.1x parcel cost on split orders. Phantom store stock triggers 6%–12% BOPIS/Ship-From-Store cancellations and costly multi-node split shipments, while sellable returns sit un-restocked for 5–14 days.
- **The AI Solution**: Evaluates item condition scans to triage restock, vendor return, or liquidation.
- **Quantified Outcome**: Grades returned items at first touch and immediately restores Grade-A stock to sellable ATP—capturing full-price resale before seasonal markdowns.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **📦 Manhattan Active WMS**: Real-time bin/aisle slotting, picker travel telemetry, wave release queues, and dock door schedules.
- **🌐 Cloud Spanner ATP**: Sub-50ms distributed transactional ledger maintaining committed customer orders and available inventory.
- **⚖️ Clark-Scarf MEIO Optimizer**: Coupled stochastic inventory solver balancing safety stock across Plants, RDCs, and Dark Stores.
- **🏢 SAP EWM**: Plant-to-warehouse stock transfer orders, pallet serialization, and inventory reconciliation.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Manhattan and Cloud) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Clark-Scarf) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (SAP).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Looking at incoming customer returns across our hubs, which items are in clean condition to restock immediately versus needing vendor return credit, refurbishment, or liquidation?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Show me a chart comparing return volumes and net value recovered across restock, refurbishment, vendor credit, and liquidation paths.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a clear reverse-logistics triage summary for Warehouse and Merchandising teams showing how returned inventory is graded and how much value we recover.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py returns_triage_agent
```

---

## 05 · Distribution & Logistics (12 Agents)
*First & Mid-Mile, Store Replenishment, Last-Mile Delivery, Route & Carrier*

### #40 · Load Consolidation (`load_consolidation_agent`)
- **Sub-Pillar**: First & Mid-Mile | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Transport Planner / Inbound Mgr · **ROI Benchmark**: `+12%–18% Cube · -10% Trucks` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: $2.27/mile trucking cost · 24%–32% unused trailer cube · $1.1B+ detention fees. Weight-only load planning ships 25%+ air, uncoordinated plant yards incur $75–$150/hr carrier detention after 2 hours, and reefer excursions spoil 2%–5% of cold-chain loads.
- **The AI Solution**: Consolidates vendor LTLs into multi-stop FTL linehauls via cube & weight modeling.
- **Quantified Outcome**: Solves 3D bin-packing, bridge-formula axle weights, and LIFO stop unloading order—shipping the same volume in 10%–15% fewer trucks.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🚚 Oracle OTM**: Outbound freight shipment orders, load tenders, rate tariffs, and carrier contractual commitments.
- **🗺️ Google Maps Routes Preferred**: Real-time highway traffic matrix, bridge height clearances, and dynamic corridor routing.
- **🛰️ Samsara ELD & IoT Telematics**: Live GPS truck tracking, driver Hours-of-Service (HOS) clocks, and continuous reefer temperature probes.
- **🚛 Google OR-Tools VRPTW**: Capacitated Vehicle Routing Problem solver with strict customer delivery time windows.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Oracle and Google) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Samsara) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Build an optimized 3D truckload consolidation plan for multi-stop linehaul shipments by querying Oracle OTM shipment orders and 53ft trailer geometry specs. Calculate 3D voxel packing that enforces LIFO unloading sequence, respects DOT axle weight limits, eliminates transit crush damage, and output an atomic CSV loading manifest.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Generate an interactive 3D isometric trailer loading visualization showing carton placement by stop, deck tier height, and steer/drive/trailer axle weight distribution.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a shipping supervisor loading instruction sheet and interactive HTML 3D load consolidation dossier detailing trailer cube utilization, fuel savings, and bridge formula compliance.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py load_consolidation_agent
```

---

### #41 · Yard Disruption Agent (`yard_dock_sequencer`)
- **Sub-Pillar**: First & Mid-Mile | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Yard Master / Plant Logistics · **ROI Benchmark**: `-60%–75% Yard Demurrage` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: $2.27/mile trucking cost · 24%–32% unused trailer cube · $1.1B+ detention fees. Weight-only load planning ships 25%+ air, uncoordinated plant yards incur $75–$150/hr carrier detention after 2 hours, and reefer excursions spoil 2%–5% of cold-chain loads.
- **The AI Solution**: Parses GPS & gate feeds to flag delays and reassign dock staging doors dynamically.
- **Quantified Outcome**: Synchronizes live carrier GPS ETAs, yard jockey moves, and dock door crew capacity to eliminate gate queues, detention fees, and plant starvation.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🚚 Oracle OTM**: Outbound freight shipment orders, load tenders, rate tariffs, and carrier contractual commitments.
- **🗺️ Google Maps Routes Preferred**: Real-time highway traffic matrix, bridge height clearances, and dynamic corridor routing.
- **🛰️ Samsara ELD & IoT Telematics**: Live GPS truck tracking, driver Hours-of-Service (HOS) clocks, and continuous reefer temperature probes.
- **🚛 Google OR-Tools VRPTW**: Capacitated Vehicle Routing Problem solver with strict customer delivery time windows.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Oracle and Google) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Samsara) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Which inbound and outbound trucks in our yard or en route are delayed or queuing for dock doors, and how should we reassign doors to avoid carrier detention penalties?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Create a chart comparing truck dwell times, carrier detention risk, and dock door utilization across our active yard schedule.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Write a concise yard-dispatch brief for the Yard Master listing urgent dock door reassignments, priority live-loads, and detention fees avoided.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py yard_dock_sequencer
```

---

### #42 · Cold-Chain Auditor (`cold_chain_auditor`)
- **Sub-Pillar**: First & Mid-Mile | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Cold Chain QA / Logistics Dir. · **ROI Benchmark**: `-50%–70% Cold-Chain Claims` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: $2.27/mile trucking cost · 24%–32% unused trailer cube · $1.1B+ detention fees. Weight-only load planning ships 25%+ air, uncoordinated plant yards incur $75–$150/hr carrier detention after 2 hours, and reefer excursions spoil 2%–5% of cold-chain loads.
- **The AI Solution**: Analyzes reefer IoT telemetry to flag thermal excursions and file carrier claims.
- **Quantified Outcome**: Monitors continuous IoT temperature/humidity and calculates Mean Kinetic Temperature (MKT) in transit—intervening before perishable or pharma loads spoil.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🚚 Oracle OTM**: Outbound freight shipment orders, load tenders, rate tariffs, and carrier contractual commitments.
- **🗺️ Google Maps Routes Preferred**: Real-time highway traffic matrix, bridge height clearances, and dynamic corridor routing.
- **🛰️ Samsara ELD & IoT Telematics**: Live GPS truck tracking, driver Hours-of-Service (HOS) clocks, and continuous reefer temperature probes.
- **🚛 Google OR-Tools VRPTW**: Capacitated Vehicle Routing Problem solver with strict customer delivery time windows.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Oracle and Google) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Samsara) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Audit refrigerated trailer shipments carrying temperature-sensitive goods by querying continuous IoT sensor logs from Samsara and shipment manifests from Oracle OTM. Detect thermal excursions exceeding contractual temperature setpoints, calculate Mean Kinetic Temperature (MKT) degradation and product shelf-life impact, and output a CSV temperature excursion log.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Generate an interactive continuous thermal telemetry chart illustrating reefer temperature over transit time with safe operating threshold bands, defrost cycles, and violation periods.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a formal carrier cargo claim and interactive HTML cold chain quality audit report for Logistics and Legal summarizing thermal violations, estimated spoilage, and contractual chargeback amounts.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py cold_chain_auditor
```

---

### #43 · Aisle-Aligned Pallet (`aisle_aligned_pallet_agent`)
- **Sub-Pillar**: Store Replenishment | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Outbound Lead / Industrial Eng. · **ROI Benchmark**: `-20%–35% Store Unload Labor` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: In-store handling = ~50% of retail supply chain labor · 18%–28% backroom overflow. Mixed-aisle DC pallets force store associates to sort cases multiple times on the sales floor, while backroom-blind pushes and municipal noise/curfew violations erode store margin.
- **The AI Solution**: Sequences DC pick waves to match individual store planograms and shelf layouts.
- **Quantified Outcome**: Builds DC pallets sequenced to each store's exact planogram aisle layout and case crush physics—slashing in-store restocking labor by 20%–35%.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🚚 Oracle OTM**: Outbound freight shipment orders, load tenders, rate tariffs, and carrier contractual commitments.
- **🗺️ Google Maps Routes Preferred**: Real-time highway traffic matrix, bridge height clearances, and dynamic corridor routing.
- **🛰️ Samsara ELD & IoT Telematics**: Live GPS truck tracking, driver Hours-of-Service (HOS) clocks, and continuous reefer temperature probes.
- **🚛 Google OR-Tools VRPTW**: Capacitated Vehicle Routing Problem solver with strict customer delivery time windows.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Oracle and Google) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Samsara) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `How can we build store-bound pallets by supermarket aisle layout and crush strength so store crews spend far less time sorting boxes and fragile items never get crushed?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Plot a chart comparing store restocking labor minutes and case-damage rates between standard mixed pallets and aisle-aligned pallet builds.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a practical outbound pallet-building brief for Distribution Center and Store Ops leads showing the stability, damage reduction, and store labor savings.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py aisle_aligned_pallet_agent
```

---

### #44 · Store Capacity Agent (`store_capacity_agent`)
- **Sub-Pillar**: Store Replenishment | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Store Replenishment Lead · **ROI Benchmark**: `-25% Backroom Congestion` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: In-store handling = ~50% of retail supply chain labor · 18%–28% backroom overflow. Mixed-aisle DC pallets force store associates to sort cases multiple times on the sales floor, while backroom-blind pushes and municipal noise/curfew violations erode store margin.
- **The AI Solution**: Throttles push replenishment based on store backroom limits and live POS velocity.
- **Quantified Outcome**: Caps and paces DC replenishment dispatches against each store's live backroom cubic capacity and receiving labor—preventing overflow and damage.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🚚 Oracle OTM**: Outbound freight shipment orders, load tenders, rate tariffs, and carrier contractual commitments.
- **🗺️ Google Maps Routes Preferred**: Real-time highway traffic matrix, bridge height clearances, and dynamic corridor routing.
- **🛰️ Samsara ELD & IoT Telematics**: Live GPS truck tracking, driver Hours-of-Service (HOS) clocks, and continuous reefer temperature probes.
- **🚛 Google OR-Tools VRPTW**: Capacitated Vehicle Routing Problem solver with strict customer delivery time windows.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Oracle and Google) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Samsara) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Which retail stores are about to get overwhelmed with more replenishment pallets than their backrooms can physically hold, and where should we throttle or smooth deliveries?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Show me a chart comparing scheduled inbound replenishment volume against store backroom capacity and daily shelf sell-through across flagged stores.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Write a clear store replenishment note explaining which deliveries to meter or reschedule so backrooms stay safe and fast-selling shelves stay stocked.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py store_capacity_agent
```

---

### #45 · Curfew Orchestrator (`port_drayage_orchestrator`)
- **Sub-Pillar**: Store Replenishment | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Retail Logistics Dispatcher · **ROI Benchmark**: `-80% Curfew & Slot Penalties` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: In-store handling = ~50% of retail supply chain labor · 18%–28% backroom overflow. Mixed-aisle DC pallets force store associates to sort cases multiple times on the sales floor, while backroom-blind pushes and municipal noise/curfew violations erode store margin.
- **The AI Solution**: Coordinates municipal delivery curfews and store dock shift schedules dynamically.
- **Quantified Outcome**: Aligns store dispatch times, EV/low-noise tractor assignment, and urban curfew/school-zone rules to eliminate municipal fines and refused drops.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🚚 Oracle OTM**: Outbound freight shipment orders, load tenders, rate tariffs, and carrier contractual commitments.
- **🗺️ Google Maps Routes Preferred**: Real-time highway traffic matrix, bridge height clearances, and dynamic corridor routing.
- **🛰️ Samsara ELD & IoT Telematics**: Live GPS truck tracking, driver Hours-of-Service (HOS) clocks, and continuous reefer temperature probes.
- **🚛 Google OR-Tools VRPTW**: Capacitated Vehicle Routing Problem solver with strict customer delivery time windows.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Oracle and Google) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Samsara) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Optimize import container drayage across major marine terminals by querying vessel discharge logs from terminal operating systems and demurrage free-time clocks in BigQuery. Prioritize container pulls based on expiring detention deadlines and Clean Truck curfew windows, minimize demurrage fees, and generate an actionable drayage dispatch CSV schedule.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Render an interactive port container demurrage timeline and gate appointment heatmap illustrating free-time expiration risk across all queued shipping containers.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a port logistics operations memo and interactive HTML demurrage shield dashboard for International Logistics leadership detailing container pull priorities and fee avoidances.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py port_drayage_orchestrator
```

---

### #46 · Geocoding Intelligence (`geocoding_intelligence_agent`)
- **Sub-Pillar**: Last-Mile Delivery | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Last-Mile Operations Lead · **ROI Benchmark**: `-30%–45% Failed Deliveries` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Last-mile = 53% of total shipping cost · $15–$18 cost per failed delivery. 4%–8% of e-commerce parcels fail first-attempt delivery due to bad rooftop geocodes, static carrier selection overpays on parcel zones, and WISMO calls drive 35%–45% of support tickets.
- **The AI Solution**: Interprets gate codes, apartment delivery notes, and aerial imagery to guide drivers.
- **Quantified Outcome**: Validates address rooftop/loading-bay coordinates and driver access notes before dispatch—eliminating $15–$18 failed-delivery redelivery costs.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🚚 Oracle OTM**: Outbound freight shipment orders, load tenders, rate tariffs, and carrier contractual commitments.
- **🗺️ Google Maps Routes Preferred**: Real-time highway traffic matrix, bridge height clearances, and dynamic corridor routing.
- **🛰️ Samsara ELD & IoT Telematics**: Live GPS truck tracking, driver Hours-of-Service (HOS) clocks, and continuous reefer temperature probes.
- **🚛 Google OR-Tools VRPTW**: Capacitated Vehicle Routing Problem solver with strict customer delivery time windows.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Oracle and Google) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Samsara) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Validate and cleanse ambiguous retail and customer delivery addresses by querying Salesforce customer records and Google Maps Geocoding API. Resolve street mismatches to high-precision rooftop coordinates, verify dock clearances and gate access restrictions, and output a verified customer delivery coordinates CSV table.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Generate an interactive rooftop geocoding map and accuracy distribution visual displaying delivery address density clusters, rooftop versus street-level precision ratings, and dock pins.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a last-mile delivery quality brief and interactive HTML geocoding validation dashboard for Dispatch Operations detailing address match rates, delivery failure preventions, and routing improvements.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py geocoding_intelligence_agent
```

---

### #47 · Courier Allocation (`multimodal_mode_shift_agent`)
- **Sub-Pillar**: Last-Mile Delivery | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: E-Commerce Logistics Dir. · **ROI Benchmark**: `-8%–14% Parcel & Courier Spend` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Last-mile = 53% of total shipping cost · $15–$18 cost per failed delivery. 4%–8% of e-commerce parcels fail first-attempt delivery due to bad rooftop geocodes, static carrier selection overpays on parcel zones, and WISMO calls drive 35%–45% of support tickets.
- **The AI Solution**: Routes parcels dynamically across internal fleet, 3PL, and gig couriers by rate card.
- **Quantified Outcome**: Dynamically selects the lowest-cost parcel, regional courier, crowdsourced, or LTL mode per order that still hits the promised customer delivery date.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🚚 Oracle OTM**: Outbound freight shipment orders, load tenders, rate tariffs, and carrier contractual commitments.
- **🗺️ Google Maps Routes Preferred**: Real-time highway traffic matrix, bridge height clearances, and dynamic corridor routing.
- **🛰️ Samsara ELD & IoT Telematics**: Live GPS truck tracking, driver Hours-of-Service (HOS) clocks, and continuous reefer temperature probes.
- **🚛 Google OR-Tools VRPTW**: Capacitated Vehicle Routing Problem solver with strict customer delivery time windows.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Oracle and Google) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Samsara) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Across today's outbound e-commerce and parcel shipments, how should we split volume between our own vans, regional parcel carriers, and gig couriers to hit delivery promises at the lowest cost?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Plot a chart comparing per-package delivery cost and on-time performance across internal fleet, national parcel, and local courier options by delivery zone.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a clear carrier allocation summary for E-Commerce Logistics explaining the recommended parcel split, peak surcharge avoidance, and total cost savings.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py multimodal_mode_shift_agent
```

---

### #48 · Delivery Exception Copilot (`otif_penalty_shield`)
- **Sub-Pillar**: Last-Mile Delivery | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Customer Support Ops Lead · **ROI Benchmark**: `-50%–65% WISMO & Chargebacks` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Last-mile = 53% of total shipping cost · $15–$18 cost per failed delivery. 4%–8% of e-commerce parcels fail first-attempt delivery due to bad rooftop geocodes, static carrier selection overpays on parcel zones, and WISMO calls drive 35%–45% of support tickets.
- **The AI Solution**: Detects en-route exceptions and updates customers proactively with reschedule links.
- **Quantified Outcome**: Detects mid-route parcel and retail-delivery delays early, triggers carrier rescue or proactive customer self-rescheduling, and cuts WISMO cost.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🚚 Oracle OTM**: Outbound freight shipment orders, load tenders, rate tariffs, and carrier contractual commitments.
- **🗺️ Google Maps Routes Preferred**: Real-time highway traffic matrix, bridge height clearances, and dynamic corridor routing.
- **🛰️ Samsara ELD & IoT Telematics**: Live GPS truck tracking, driver Hours-of-Service (HOS) clocks, and continuous reefer temperature probes.
- **🚛 Google OR-Tools VRPTW**: Capacitated Vehicle Routing Problem solver with strict customer delivery time windows.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Oracle and Google) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Samsara) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Which customer shipments currently in transit are running late due to weather, traffic, or hub delays, and what proactive updates or recovery actions should we trigger right now?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Show me a chart comparing shipment delay risk, retailer On-Time In-Full penalty exposure, and customer impact across active in-transit loads.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Write a clear customer-care and logistics exception summary listing delayed orders, updated arrival windows, and proactive customer reschedule actions.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py otif_penalty_shield
```

---

### #49 · Dynamic Rerouter (`fleetflow_dispatch`)
- **Sub-Pillar**: Route & Carrier | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Fleet Dispatcher / Central Ops · **ROI Benchmark**: `-6%–11% Fleet Miles & Fuel` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 20%+ empty/out-of-route miles · 12%–25% spot premium · 3%–8% invoice error rate. Static dispatch routes burn excess fuel in weather/traffic corridors, primary tender rejections spike spot rates by 15%–25%, and 3%–8% of EDI 210 freight bills contain unverified accessorial or tariff errors.
- **The AI Solution**: Recalculates multi-stop routes using live Google Maps traffic, radar, and bridge limits.
- **Quantified Outcome**: Continuously re-solves multi-stop Vehicle Routing (VRP) against live traffic, weather, and driver Hours-of-Service (HOS) to cut fuel and empty miles.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🚚 Oracle OTM**: Outbound freight shipment orders, load tenders, rate tariffs, and carrier contractual commitments.
- **🗺️ Google Maps Routes Preferred**: Real-time highway traffic matrix, bridge height clearances, and dynamic corridor routing.
- **🛰️ Samsara ELD & IoT Telematics**: Live GPS truck tracking, driver Hours-of-Service (HOS) clocks, and continuous reefer temperature probes.
- **🚛 Google OR-Tools VRPTW**: Capacitated Vehicle Routing Problem solver with strict customer delivery time windows.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Oracle and Google) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Samsara) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Dynamically dispatch and route our commercial delivery fleet by querying pending shipments from Oracle OTM, real-time highway congestion from Google Maps Routes Preferred, and driver Hours-of-Service limits from Samsara ELD. Solve a multi-stop Capacitated Vehicle Routing Problem with Time Windows (VRPTW) to cut deadhead miles and output a turn-by-turn CSV dispatch manifest.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Generate an interactive multi-stop delivery corridor route map visual with color-coded traffic congestion overlays, customer waypoint stop sequences, and driver break rest stops.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a daily fleet dispatch operational memorandum and interactive HTML route control board for the Fleet Operations Manager detailing mileage reductions, fuel savings, and on-time arrival forecasts.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py fleetflow_dispatch
```

---

### #50 · Routing Guide Compliance (`freight_control_tower`)
- **Sub-Pillar**: Route & Carrier | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Transport Procurement Lead · **ROI Benchmark**: `-15%–22% Spot Freight Spend` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 20%+ empty/out-of-route miles · 12%–25% spot premium · 3%–8% invoice error rate. Static dispatch routes burn excess fuel in weather/traffic corridors, primary tender rejections spike spot rates by 15%–25%, and 3%–8% of EDI 210 freight bills contain unverified accessorial or tariff errors.
- **The AI Solution**: Tracks carrier tender acceptance & OTIF to reprioritize waterfall routing guides.
- **Quantified Outcome**: Predicts primary carrier tender rejections by lane and cascades early to contracted Tier-2/3 carriers before loads leak onto expensive spot markets.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🚚 Oracle OTM**: Outbound freight shipment orders, load tenders, rate tariffs, and carrier contractual commitments.
- **🗺️ Google Maps Routes Preferred**: Real-time highway traffic matrix, bridge height clearances, and dynamic corridor routing.
- **🛰️ Samsara ELD & IoT Telematics**: Live GPS truck tracking, driver Hours-of-Service (HOS) clocks, and continuous reefer temperature probes.
- **🚛 Google OR-Tools VRPTW**: Capacitated Vehicle Routing Problem solver with strict customer delivery time windows.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Oracle and Google) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Samsara) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Which contracted trucking carriers are rejecting load tenders or missing on-time delivery targets on key lanes, forcing us into expensive spot-market trucks?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Show me a chart comparing contracted tender acceptance rates, On-Time In-Full reliability, and spot-market cost leakage across our primary freight lanes.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a clear carrier routing-guide review memo for Transportation Procurement identifying underperforming carriers and recommending backup waterfall changes.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py freight_control_tower
```

---

### #51 · Freight Bill Audit Agent (`freight_bill_audit_agent`)
- **Sub-Pillar**: Route & Carrier | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Freight Controller / Claims · **ROI Benchmark**: `Recovers 3%–7% Freight Spend` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 20%+ empty/out-of-route miles · 12%–25% spot premium · 3%–8% invoice error rate. Static dispatch routes burn excess fuel in weather/traffic corridors, primary tender rejections spike spot rates by 15%–25%, and 3%–8% of EDI 210 freight bills contain unverified accessorial or tariff errors.
- **The AI Solution**: Extracts signed PODs and rate contracts via OCR to audit accessorial surcharges.
- **Quantified Outcome**: Audits 100% of carrier EDI 210/PDF freight invoices against contracted rate tables, DOE fuel indices, and GPS arrival timestamps before payment.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🚚 Oracle OTM**: Outbound freight shipment orders, load tenders, rate tariffs, and carrier contractual commitments.
- **🗺️ Google Maps Routes Preferred**: Real-time highway traffic matrix, bridge height clearances, and dynamic corridor routing.
- **🛰️ Samsara ELD & IoT Telematics**: Live GPS truck tracking, driver Hours-of-Service (HOS) clocks, and continuous reefer temperature probes.
- **🚛 Google OR-Tools VRPTW**: Capacitated Vehicle Routing Problem solver with strict customer delivery time windows.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (Oracle and Google) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (Samsara) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Google).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Audit incoming motor carrier freight bills by cross-checking carrier EDI 210 invoices against contractual tariffs in Oracle OTM and actual GPS detention telemetry from Samsara. Identify unapproved accessorial charges, mileage overstatements, and inaccurate fuel surcharge calculations, and generate a line-item CSV freight discrepancy ledger.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Render an interactive freight overcharge variance waterfall chart illustrating billed versus contractual freight costs across base freight, fuel surcharges, detention, and accessorial fees.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a formal carrier freight dispute claim letter and interactive HTML freight audit review brief detailing disputed invoice amounts, evidence records, and net payable balances.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py freight_bill_audit_agent
```

---

## 06 · Returns & Reverse Logistics (9 Agents)
*Returns & Claims Management, Expiry & Markdowns, Pallet & Tote Reclamation*

### #52 · Return Fraud Sentinel (`reverse_rma_optimizer`)
- **Sub-Pillar**: Returns & Claims Mgmt | **Pillar**: 06 · Returns & Reverse Logistics
- **Primary Human Persona**: Reverse Logistics / Fraud Lead · **ROI Benchmark**: `-25%–40% Return Fraud Loss` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: $890B annual returns (16.9% of sales) · $101B fraud · 20%–65% COGS reverse cost. Processing a return costs 20%–65% of an item's original value—shipping low-margin goods back destroys net margin, while $101B in fraudulent/wardrobed returns and missed OS&D windows leak straight from EBIT.
- **The AI Solution**: Analyzes item photos and packaging video feeds to detect wear or swapped tags.
- **Quantified Outcome**: Scores return requests against serial history, account abuse patterns, and item telemetry—blocking fraudulent RMAs without friction for loyal buyers.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🔄 SAP Customer Returns (SD/LE)**: Automated customer RMA intake, warranty claims, and credit memo release processing.
- **🏷️ Zebra RFID Dock Portals**: High-speed dock door RFID scanners tracking reusable transport items (pallets, totes, and cages).
- **🌱 BigQuery Scope-3 ESG Ledger**: GLEC-compliant carbon emission accounting, CBAM embedded carbon, and EUDR deforestation audits.
- **💰 Dynamic Markdown Optimizer**: Price elasticity model balancing clearance markdown depth against charitable food bank tax deductions.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and Zebra) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (BigQuery) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Dynamic).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Screen incoming customer return merchandise authorizations (RMA) in Salesforce Service Cloud by cross-referencing customer historical return frequency, serialized barcode claims, and backhaul logistics capacity. Detect wardrobing and return fraud patterns, optimize reverse routing between restock, refurbish, and liquidation, and output a CSV return disposition table.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Render an interactive customer return fraud risk distribution and circular disposition matrix chart categorizing claims by fraud risk level and net recovery value.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft an executive reverse logistics policy memo and interactive HTML return fraud audit report for the Customer Experience and Reverse Logistics Directors detailing fraud savings and disposition recovery rates.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py reverse_rma_optimizer
```

---

### #53 · Keep-It & Routing Advisor (`keep_it_routing_advisor`)
- **Sub-Pillar**: Returns & Claims Mgmt | **Pillar**: 06 · Returns & Reverse Logistics
- **Primary Human Persona**: Customer Experience (CX) Lead · **ROI Benchmark**: `+15%–22% Net Return Margin` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: $890B annual returns (16.9% of sales) · $101B fraud · 20%–65% COGS reverse cost. Processing a return costs 20%–65% of an item's original value—shipping low-margin goods back destroys net margin, while $101B in fraudulent/wardrobed returns and missed OS&D windows leak straight from EBIT.
- **The AI Solution**: Evaluates salvage margins vs reverse freight to determine keep-it instant refunds.
- **Quantified Outcome**: Calculates reverse shipping + grading cost vs. resale recovery in real time—routing items to store, refurb hub, outlet, or Keep-It credit.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🔄 SAP Customer Returns (SD/LE)**: Automated customer RMA intake, warranty claims, and credit memo release processing.
- **🏷️ Zebra RFID Dock Portals**: High-speed dock door RFID scanners tracking reusable transport items (pallets, totes, and cages).
- **🌱 BigQuery Scope-3 ESG Ledger**: GLEC-compliant carbon emission accounting, CBAM embedded carbon, and EUDR deforestation audits.
- **💰 Dynamic Markdown Optimizer**: Price elasticity model balancing clearance markdown depth against charitable food bank tax deductions.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and Zebra) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (BigQuery) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Dynamic).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `For which low-price or bulky customer returns does reverse shipping and warehouse processing cost more than we could ever recover by bringing the item back?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Create a chart comparing net resale recovery value against reverse shipping and handling cost across active return categories.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Write a clear return-economics brief for Customer Experience and Finance showing when instant keep-it or local donation beats shipping items back.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py keep_it_routing_advisor
```

---

### #54 · OS&D Freight Claims (`osd_freight_claims_agent`)
- **Sub-Pillar**: Returns & Claims Mgmt | **Pillar**: 06 · Returns & Reverse Logistics
- **Primary Human Persona**: Claims Specialist / Controller · **ROI Benchmark**: `2x Faster OS&D Cash Recovery` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: $890B annual returns (16.9% of sales) · $101B fraud · 20%–65% COGS reverse cost. Processing a return costs 20%–65% of an item's original value—shipping low-margin goods back destroys net margin, while $101B in fraudulent/wardrobed returns and missed OS&D windows leak straight from EBIT.
- **The AI Solution**: Reconciles eBOLs, dock damage logs, and carrier contracts to auto-file disputes.
- **Quantified Outcome**: Assembles dock damage photos, signed BOL exceptions, and SKU invoice values into compliant carrier claim packets within hours of unloading.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🔄 SAP Customer Returns (SD/LE)**: Automated customer RMA intake, warranty claims, and credit memo release processing.
- **🏷️ Zebra RFID Dock Portals**: High-speed dock door RFID scanners tracking reusable transport items (pallets, totes, and cages).
- **🌱 BigQuery Scope-3 ESG Ledger**: GLEC-compliant carbon emission accounting, CBAM embedded carbon, and EUDR deforestation audits.
- **💰 Dynamic Markdown Optimizer**: Price elasticity model balancing clearance markdown depth against charitable food bank tax deductions.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and Zebra) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (BigQuery) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Dynamic).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Which recent shipments arrived with crushed pallets, wet cartons, or missing cases at the receiving dock, and do we have the signed delivery receipts and photos needed to win carrier claims?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Show me a chart comparing damaged and short-shipped cargo value by carrier and lane alongside claim recovery readiness.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Prepare a complete cargo-damage claim summary for Claims and Finance listing the documented losses, carrier liability evidence, and filing deadlines.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py osd_freight_claims_agent
```

---

### #55 · Dynamic Markdown Agent (`dynamic_markdown_agent`)
- **Sub-Pillar**: Expiry & Markdowns | **Pillar**: 06 · Returns & Reverse Logistics
- **Primary Human Persona**: Merchandising / Store Ops Mgr · **ROI Benchmark**: `-22%–35% Expiry Shrink` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 2.5%–6.0% of grocery sales lost to shrink · $408B+ annual food value lost. Flat, late manual markdowns (e.g., 50% off on final day) sacrifice gross margin without clearing short-dated lots in time, driving 3%+ perishable write-offs and landfill disposal fees.
- **The AI Solution**: Correlates days-to-expiry (DTE) with sales velocity to trigger ESL shelf price cuts.
- **Quantified Outcome**: Triggers shallow, early price-elasticity markdowns synced to lot sell-by dates and local store velocity—clearing stock at higher margin with less waste.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🔄 SAP Customer Returns (SD/LE)**: Automated customer RMA intake, warranty claims, and credit memo release processing.
- **🏷️ Zebra RFID Dock Portals**: High-speed dock door RFID scanners tracking reusable transport items (pallets, totes, and cages).
- **🌱 BigQuery Scope-3 ESG Ledger**: GLEC-compliant carbon emission accounting, CBAM embedded carbon, and EUDR deforestation audits.
- **💰 Dynamic Markdown Optimizer**: Price elasticity model balancing clearance markdown depth against charitable food bank tax deductions.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and Zebra) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (BigQuery) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Dynamic).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Optimize price markdowns on short-dated perishable inventory by querying lot expiration dates in SAP S/4HANA and localized price elasticity in BigQuery. Determine the optimal timing and discount depth to maximize revenue recovery before expiration, compare liquidation against charitable tax donation write-offs, and output an atomic CSV markdown schedule.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Plot an interactive dynamic markdown curve comparing projected unit sell-through velocity and net cash recovery across varying discount depths (10%, 25%, 40%, donation).`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft a commercial markdown recommendation brief and interactive HTML inventory salvage report for Merchandising and Retail Store Operations outlining pricing actions and waste reduction figures.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py dynamic_markdown_agent
```

---

### #56 · Short-Dated Redistributor (`short_dated_redistributor`)
- **Sub-Pillar**: Expiry & Markdowns | **Pillar**: 06 · Returns & Reverse Logistics
- **Primary Human Persona**: Inventory Disposition Lead · **ROI Benchmark**: `Diverts 30%–45% At-Risk Lots` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 2.5%–6.0% of grocery sales lost to shrink · $408B+ annual food value lost. Flat, late manual markdowns (e.g., 50% off on final day) sacrifice gross margin without clearing short-dated lots in time, driving 3%+ perishable write-offs and landfill disposal fees.
- **The AI Solution**: Matches near-date DC lots with discounters or food banks before acceptance cutoffs.
- **Quantified Outcome**: Matches short-dated DC lots at risk of customer shelf-life rejection to fast-turning stores, foodservice channels, or tax-advantaged donations.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🔄 SAP Customer Returns (SD/LE)**: Automated customer RMA intake, warranty claims, and credit memo release processing.
- **🏷️ Zebra RFID Dock Portals**: High-speed dock door RFID scanners tracking reusable transport items (pallets, totes, and cages).
- **🌱 BigQuery Scope-3 ESG Ledger**: GLEC-compliant carbon emission accounting, CBAM embedded carbon, and EUDR deforestation audits.
- **💰 Dynamic Markdown Optimizer**: Price elasticity model balancing clearance markdown depth against charitable food bank tax deductions.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and Zebra) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (BigQuery) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Dynamic).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Which warehouse lots are approaching retailer minimum shelf-life cutoffs and should be redirected now to discount outlets or regional food banks before they become unsellable?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Show me a chart comparing short-dated lot value, days remaining before cutoff, and recovery value across discount resale and tax-advantaged food-bank donation.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Write a clear disposition summary for Inventory Control and Sustainability detailing which near-date lots to reallocate to secondary buyers or community food banks.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py short_dated_redistributor
```

---

### #57 · Food Waste & ESG Copilot (`food_waste_esg_copilot`)
- **Sub-Pillar**: Expiry & Markdowns | **Pillar**: 06 · Returns & Reverse Logistics
- **Primary Human Persona**: Chief Sustainability Officer · **ROI Benchmark**: `-75% ESG Reporting Cost` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 2.5%–6.0% of grocery sales lost to shrink · $408B+ annual food value lost. Flat, late manual markdowns (e.g., 50% off on final day) sacrifice gross margin without clearing short-dated lots in time, driving 3%+ perishable write-offs and landfill disposal fees.
- **The AI Solution**: Aggregates store shrink and organic haul logs to generate audited GHG diversion filings.
- **Quantified Outcome**: Routes unsellable organics to highest circular tier (donation tax credits, upcycling, feed, digester) and automates Scope 3 waste reporting.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🔄 SAP Customer Returns (SD/LE)**: Automated customer RMA intake, warranty claims, and credit memo release processing.
- **🏷️ Zebra RFID Dock Portals**: High-speed dock door RFID scanners tracking reusable transport items (pallets, totes, and cages).
- **🌱 BigQuery Scope-3 ESG Ledger**: GLEC-compliant carbon emission accounting, CBAM embedded carbon, and EUDR deforestation audits.
- **💰 Dynamic Markdown Optimizer**: Price elasticity model balancing clearance markdown depth against charitable food bank tax deductions.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and Zebra) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (BigQuery) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Dynamic).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `How much unsellable organic and food waste are our stores and hubs diverting away from landfills into donation, animal feed, composting, or bio-energy, and how does that reduce emissions?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Create a chart comparing organic waste tonnage diverted by recovery pathway and the resulting greenhouse-gas emissions avoided across facilities.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Prepare an audit-ready sustainability summary for our Chief Sustainability Officer covering landfill diversion rates, avoided emissions, and verified hauler manifests.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py food_waste_esg_copilot
```

---

### #58 · RTI Balance Reconciler (`rti_balance_reconciler`)
- **Sub-Pillar**: Pallet & Tote Reclamation | **Pillar**: 06 · Returns & Reverse Logistics
- **Primary Human Persona**: Asset Recovery / RTI Manager · **ROI Benchmark**: `-25%–35% RTI Replacement Cost` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 10%–20% annual pallet/tote pool loss · 28%–40% empty store-return backhauls. Unreconciled pallet/tote ledgers trigger millions in pool non-return fines and replacement CapEx, while returning store fleets haul empty air and manual wash logs risk food-safety recalls.
- **The AI Solution**: Reconciles RFID portal scans with CHEP/PECO statements to detect hoarding nodes.
- **Quantified Outcome**: Reconciles serialized pallet, tote, rack, and keg balances across plants, DCs, and customers—slashing pool rental fines and replacement CapEx.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🔄 SAP Customer Returns (SD/LE)**: Automated customer RMA intake, warranty claims, and credit memo release processing.
- **🏷️ Zebra RFID Dock Portals**: High-speed dock door RFID scanners tracking reusable transport items (pallets, totes, and cages).
- **🌱 BigQuery Scope-3 ESG Ledger**: GLEC-compliant carbon emission accounting, CBAM embedded carbon, and EUDR deforestation audits.
- **💰 Dynamic Markdown Optimizer**: Price elasticity model balancing clearance markdown depth against charitable food bank tax deductions.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and Zebra) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (BigQuery) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Dynamic).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Audit reusable transport items (pallets, totes, and plastic crates) across our distribution network by querying RFID dock portal scans and CHEP/PECO asset exchange statements. Identify unreturned pallet balances accumulating at retail customer distribution centers beyond contractual dwell periods, calculate demurrage liabilities, and output a CSV customer pallet reconciliation table.`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Generate an interactive RTI asset velocity loop and unreturned dwell time chart highlighting customer facilities with severe pallet retention delays and missing asset fees.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Draft an executive reusable asset audit memorandum and interactive HTML pallet reconciliation dossier for Logistics and Billing leadership detailing outstanding pallet counts, collection orders, and recovery chargebacks.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py rti_balance_reconciler
```

---

### #59 · Milk-Run Consolidation (`intermodal_rail_linehaul_agent`)
- **Sub-Pillar**: Pallet & Tote Reclamation | **Pillar**: 06 · Returns & Reverse Logistics
- **Primary Human Persona**: Reverse Transport Planner · **ROI Benchmark**: `-20%–30% Reverse Haul Cost` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 10%–20% annual pallet/tote pool loss · 28%–40% empty store-return backhauls. Unreconciled pallet/tote ledgers trigger millions in pool non-return fines and replacement CapEx, while returning store fleets haul empty air and manual wash logs risk food-safety recalls.
- **The AI Solution**: Schedules dynamic backhauls to collect empty roll cages and RPCs from retail stores.
- **Quantified Outcome**: Pairs empty outbound store/DC return legs with pallet stacks, collapsible totes, and consolidated RMAs—eliminating dedicated reverse freight.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🔄 SAP Customer Returns (SD/LE)**: Automated customer RMA intake, warranty claims, and credit memo release processing.
- **🏷️ Zebra RFID Dock Portals**: High-speed dock door RFID scanners tracking reusable transport items (pallets, totes, and cages).
- **🌱 BigQuery Scope-3 ESG Ledger**: GLEC-compliant carbon emission accounting, CBAM embedded carbon, and EUDR deforestation audits.
- **💰 Dynamic Markdown Optimizer**: Price elasticity model balancing clearance markdown depth against charitable food bank tax deductions.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and Zebra) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (BigQuery) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Dynamic).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Which outbound delivery trucks returning empty from stores can collect stacked empty totes, pallets, and roll cages on their backhaul trip so we stop running empty miles?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Plot a chart comparing empty backhaul miles eliminated, asset recovery volume, and fuel savings across candidate milk-run return routes.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Write a practical backhaul dispatch plan for Reverse Transport Planners showing which returning trucks should pick up empty totes and cages at which stops.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py intermodal_rail_linehaul_agent
```

---

### #60 · Sanitation & Health Agent (`sanitation_health_agent`)
- **Sub-Pillar**: Pallet & Tote Reclamation | **Pillar**: 06 · Returns & Reverse Logistics
- **Primary Human Persona**: Packaging QA / Food Safety · **ROI Benchmark**: `Zero Sanitation Recall Breaches` · 📦 **High-Code ADK Package**

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: 10%–20% annual pallet/tote pool loss · 28%–40% empty store-return backhauls. Unreconciled pallet/tote ledgers trigger millions in pool non-return fines and replacement CapEx, while returning store fleets haul empty air and manual wash logs risk food-safety recalls.
- **The AI Solution**: Inspects return photos and wash logs for structural fatigue and chemical compliance.
- **Quantified Outcome**: Enforces wash-temperature, allergen segregation, and structural cycle limits on every reusable container—extending asset life while guaranteeing safety.

#### 🔌 2. Connected Enterprise Systems & Data Sources
- **🔄 SAP Customer Returns (SD/LE)**: Automated customer RMA intake, warranty claims, and credit memo release processing.
- **🏷️ Zebra RFID Dock Portals**: High-speed dock door RFID scanners tracking reusable transport items (pallets, totes, and cages).
- **🌱 BigQuery Scope-3 ESG Ledger**: GLEC-compliant carbon emission accounting, CBAM embedded carbon, and EUDR deforestation audits.
- **💰 Dynamic Markdown Optimizer**: Price elasticity model balancing clearance markdown depth against charitable food bank tax deductions.

#### 🔄 3. How the Agent Works (The 3-Step Execution Flow)
1. **Sense & Ingest**: Automatically queries live operational transactions from connected enterprise connectors (SAP and Zebra) without asking the user for technical table names or SQL parameters.
2. **Predict & Optimize**: Evaluates operational constraints, detects anomalies, and runs specialized mathematical solvers (BigQuery) to identify the optimal action plan.
3. **Deliver & Action**: Renders an interactive visual chart, generates an atomic copy-ready CSV table for Google Sheets, and prepares approved updates for system writeback (Dynamic).

#### 💬 4. 3 Realistic High-Impact Business Prompts (Actual Use Cases)
- **Prompt 1 · Operational Diagnostic & Reconciliation**:
  > `Are all returned reusable totes, crates, and pallets passing structural crack inspections and wash-cycle temperature and sanitizer checks before going back into food contact?`
- **Prompt 2 · Visual Analytics & Comparison Chart**:
  > `Show me a chart comparing wash-tunnel temperature and sanitizer compliance plus structural damage rates across inspected return container batches.`
- **Prompt 3 · Executive Decision Brief & S&OP Alignment**:
  > `Prepare a clear food-safety and container quality summary listing batches cleared for reuse and any cracked or under-sanitized lots quarantined for re-wash or recycling.`

```bash
# Run full autonomous scenario & print copy-ready table:
python3 scripts/test_agent_demo.py sanitation_health_agent
```

---

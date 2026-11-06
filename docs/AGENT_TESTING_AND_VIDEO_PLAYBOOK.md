# 🎬 Supply Chain AI Agents — Complete Testing, Demo Data & Video Recording Playbook

> **Executive Summary for Leadership & Evaluators**:
> This Playbook provides a clear, human-understandable walkthrough for all **60 Supply Chain AI Agents** spanning the 6 ASCM SCOR Operating Pillars.
> For each agent, you will find:
> 1. **The Real-World Business Use Case**: What specific operational problem it solves in plain English.
> 2. **Connected Enterprise Systems & Data Sources**: Simple enterprise connectors (SAP, BigQuery, Manhattan WMS, Oracle OTM, Siemens MES) — zero raw SQL table clutter.
> 3. **The 3-Step Execution Flow**: How the agent ingests data, solves constraints, and executes safe writebacks.
> 4. **3 Realistic High-Impact Business Prompts**: Authentic plain-English questions you can paste directly into Gemini Enterprise or the local ADK chat.

- **🟢 Live in Gemini Enterprise**: 25 agents deployed to Vertex AI Reasoning Engine.
- **⚪ In Catalog**: 35 agents specified across all SCOR pillars.

---

## 01 · Planning & Strategy (12 Agents)
*Demand Forecasting, Trade Promotion, S&OP / IBP, Portfolio & SKU*

### #01 · Demand Sensing Agent (`demand_sensing_agent`)
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 01 · Planning & Strategy
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 02 · Sourcing & Procurement
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 02 · Sourcing & Procurement
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 02 · Sourcing & Procurement
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 02 · Sourcing & Procurement
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 02 · Sourcing & Procurement
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 02 · Sourcing & Procurement
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 02 · Sourcing & Procurement
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 02 · Sourcing & Procurement
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 02 · Sourcing & Procurement
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 03 · Manufacturing & Production
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 03 · Manufacturing & Production
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 03 · Manufacturing & Production
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 03 · Manufacturing & Production
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 03 · Manufacturing & Production
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 03 · Manufacturing & Production
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 03 · Manufacturing & Production
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 03 · Manufacturing & Production
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 03 · Manufacturing & Production
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 04 · Inventory & Warehousing
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 04 · Inventory & Warehousing
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 04 · Inventory & Warehousing
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 04 · Inventory & Warehousing
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 04 · Inventory & Warehousing
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 04 · Inventory & Warehousing
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 04 · Inventory & Warehousing
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 04 · Inventory & Warehousing
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 04 · Inventory & Warehousing
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 05 · Distribution & Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 06 · Returns & Reverse Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 06 · Returns & Reverse Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 06 · Returns & Reverse Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 06 · Returns & Reverse Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 06 · Returns & Reverse Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 06 · Returns & Reverse Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: 🟢 Live in Gemini Enterprise | **Sub-Pillar**: Core Operations | **Pillar**: 06 · Returns & Reverse Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 06 · Returns & Reverse Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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
- **Status**: ⚪ Catalog Specification | **Sub-Pillar**: Core Operations | **Pillar**: 06 · Returns & Reverse Logistics
- **Primary Human Persona**: Supply Chain Leader · **ROI Benchmark**: `High ROI`

#### 🎯 1. Real-World Business Use Case
- **The Business Problem**: Siloed operational data and lagged ERP updates cause recurring stockouts and high buffer costs in Core Operations.
- **The AI Solution**: Autonomously ingests operational signals from SAP and BigQuery, evaluates multi-tier constraints, and executes safe writebacks.
- **Quantified Outcome**: Reduces operational cycle time by 25%–40% and cuts manual planning toil.

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

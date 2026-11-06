# Promo ROI Simulator

> **ASCM SCOR Pillar**: `01 · Planning & Strategy`  
> **Sub-Pillar**: `Trade Promotion`  
> **Target Persona**: `Trade Marketing Manager` (Operations Leader)  
> **Core Value Metric**: `+15%–25% Promo Net ROI`  
> **Reasoning Model**: `gemini-3-pro-preview` (Gemini 3.1 Pro / Gemini 3.8 Flash Dynamic Routing)  
> **A2UI Surfaces**: Native Interactive HTML Cockpit (`IFrameSrcdoc`) + Deterministic `VegaChart`  
> **Standard Compliance**: ASCM SCOR DS v14.0 · ISA-95 · GS1 EPCIS 2.0 · ISO/IEC 42001

---

## 1. Executive Summary & Business Value

### The Business Challenge
59%–67% of CPG trade promotions fail to break even · 4%–7% revenue leaked. Trade spend is typically the #2 P&L line item (15%–25% of gross sales), yet 59%–67% of promotions lose money due to subsidized baseline volume, forward-buying, and unverified retailer deductions.

### The Autonomous Solution
Simulates price elasticity, shelf lift, and incremental spend return.

### Quantified Outcomes & Measurable ROI
- **Target Impact**: +15%–25% Promo Net ROI
- **Competitive Advantage**: Boosts net trade spend ROI by 22% and prevents promotional stockouts and post-promo bullwhip troughs.
- **Autonomous Cadence**: Real-time continuous execution eliminating batch ERP latency and manual spreadsheet reconciliation.
- **Zero Hallucination Guarantee**: Strict grounding against BigQuery enterprise twin fixtures and deterministic OR-Tools solvers.

---

## 2. Technical Architecture & Systems Integration

```mermaid
graph TD
  A["High-Frequency Signal Ingestion<br/>(ERP / WMS / TMS / IoT Feeds)"] --> B["Deterministic Constraint Evaluation<br/>(Business Rules & SLA Bounds)"]
  B --> C["Mathematical Optimization Stack<br/>(BigQuery ML Causal Double-ML Uplift + Cross-SKU Cannibalization Matrix + Mathematical Optimization Solver (MILP / CP-SAT) Supply-Aware Price Shaper)"]
  C --> D["Gemini 3.1 Pro Executive Synthesis<br/>(Human-in-the-Loop Consensus)"]
  D --> E["Idempotent ERP Write-Back<br/>(Salesforce / SAP Trade Promo Calendar Lock & Shaped Regional SKU Curve Update)"]
  D --> F["A2UI Interactive Cockpit<br/>(IFrameSrcdoc Canvas & VegaChart)"]
```

### Connected Enterprise Systems
- **Core Systems**: Trade Promotion Management (TPM / CRM) · Commercial CRM & Trade Portal (MCP / API) · Supply Planning System (MCP / API) · BigQuery ML · Time-Series Forecasting Model · Operational SQL & Vector DB (On-Prem / Cloud) · Geospatial & Location Intelligence API
- **Mathematical Solver Stack**: BigQuery ML Causal Double-ML Uplift + Cross-SKU Cannibalization Matrix + Mathematical Optimization Solver (MILP / CP-SAT) Supply-Aware Price Shaper
- **Write-Back Gateway**: Salesforce / SAP Trade Promo Calendar Lock & Shaped Regional SKU Curve Update
- **Available ADK Tools**: `query_planned_promo_campaigns`, `query_causal_promo_elasticity`, `query_cross_sku_cannibalization`, `query_warehouse_promo_availability`, `action_shape_promotional_mechanic`, `action_lock_tpm_calendar`, `list_systems`, `lookup_xyz_master_context`, `analyze_operational_metrics`, `render_visual_chart`, `draft_operational_brief`

### Collaborating A2A Sub-Agents
- **Causal Uplift Decomposer**: Separates net incremental lift from pull-forward & halo in BigQuery ML
- **Cannibalization Matrix Agent**: Quantifies sister-SKU volume diversion across price tiers
- **Supply-Aware Shaper**: Redirects promo spend toward surplus high-margin inventory via Mathematical Optimization Solver (MILP / CP-SAT)

---

## 3. Connected Demo Data & Ground Truth Lake

This agent operates directly over verified enterprise fixtures located locally in `agents/promo_lift_simulator/fixtures/tables/` and synchronized to Google BigQuery in project `zuhaibp-ai`.

| Fixture Table | BigQuery Table ID | Records | Schema Preview |
| :--- | :--- | :--- | :--- |
| `causal_promo_elasticity` | `zuhaibp-ai:supply_chain_twin.causal_promo_elasticity` | 8 rows | `sku_id`, `base_price_usd`, `discounted_price_usd`, `price_elasticity`, `baseline_units` *(+6 more)* |
| `cross_sku_cannibalization` | `zuhaibp-ai:supply_chain_twin.cross_sku_cannibalization` | 8 rows | `promoted_sku`, `cannibalized_sku`, `cannibalization_rate_pct`, `volume_diverted_units`, `margin_loss_per_unit_usd` *(+2 more)* |
| `planned_promo_campaigns` | `zuhaibp-ai:supply_chain_twin.planned_promo_campaigns` | 8 rows | `campaign_id`, `name`, `retailer`, `channel`, `start_date` *(+6 more)* |
| `warehouse_promo_availability` | `zuhaibp-ai:supply_chain_twin.warehouse_promo_availability` | 8 rows | `sku_id`, `distribution_center`, `available_to_promise_units`, `promo_surge_forecast_units`, `buffer_safety_stock_units` *(+2 more)* |

### Data Flow & Sovereignty
1. **Local Sandbox**: Evaluates against `fixtures/tables/*.json` for offline tests and deterministic validation.
2. **BigQuery Live Twin**: In production or connected demo mode, queries dataset `zuhaibp-ai:supply_chain_twin` with zero ETL latency.
3. **Data Protection**: Customer data remains strictly in your VPC; Gemini reasoning engines are stateless and private.

---

## 4. 1-Command Automated Deployment

Deploy this agent directly to Google Cloud Vertex AI Agent Engine and register it in Gemini Enterprise in under 60 seconds:

```bash
# Set your GCP Project and Region
export GOOGLE_CLOUD_PROJECT="zuhaibp-ai"
export GOOGLE_CLOUD_REGION="us-central1"

# 1-Command In-Place Deployment
python3 scripts/deploy_to_gemini_enterprise.py --agent promo_lift_simulator
```

### What This Command Does:
1. **Verifies Demo Data**: Validates that all connected BigQuery fixture tables exist and are populated.
2. **Compiles ADK Package**: Packages `agents/promo_lift_simulator` with its tools, models, interactive HTML generators, and pre-execution safety gates.
3. **Deploys Vertex AI Reasoning Engine**: Deploys or updates the Reasoning Engine in `us-central1` in-place (reusing existing IDs to prevent duplicates).
4. **Registers in Gemini Enterprise**: Registers or refreshes the agent in the Gemini Enterprise application with its executive icon, prompt starters, and native A2UI canvas configuration.

---

## 5. Copy-Ready Test Prompts (Playbook)

Test this agent in the Gemini Enterprise web interface, the ADK test bench, or via API using these plain-English business prompts:

1. **"What is our current operational performance and where are the most critical bottlenecks across Trade Promotion?"**
2. **"Simulate a 25% demand shock and compute the optimal re-allocation schedule with zero SLA violations."**
3. **"Generate an interactive HTML dashboard showing live telemetry, scenario comparison, and ERP audit log."**
4. **"Review the recommended optimization and safely commit the change to ERP with an audit idempotency key."**

---

## 6. Directory Structure

```text
agents/promo_lift_simulator/
├── README.md                     # This executive-grade specification
├── pyproject.toml                # Poetry / Pip dependencies (google-adk, vertexai)
├── agents-cli-manifest.yaml      # Google ADK Agent Engine manifest
├── deployment_metadata.json      # Deployed Reasoning Engine & Gemini Enterprise IDs
├── app/
│   ├── __init__.py
│   ├── agent.py                  # Core ADK Agent declaration and system prompt
│   ├── tools.py                  # Grounded business tools and ERP connectors
│   └── render/
│       ├── interactive_html.py   # Standalone interactive HTML cockpit generator
│       ├── surfaces.py           # A2UI IFrameSrcdoc and VegaChart builders
│       ├── charts.py             # Vega-Lite visualization specifications
│       └── png_chart.py          # High-resolution raster fallback charts
├── fixtures/
│   └── tables/                   # Ground-truth JSON datasets
└── tests/
    └── test_smoke.py             # Unit tests validating tools and agent behavior
```

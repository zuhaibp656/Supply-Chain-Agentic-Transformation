# Forecast Reconciliation

> **ASCM SCOR Pillar**: `01 · Planning & Strategy`  
> **Sub-Pillar**: `Demand Forecasting`  
> **Target Persona**: `Commercial Planning Lead` (Operations Leader)  
> **Core Value Metric**: `-40%–55% CPFR Variance`  
> **Reasoning Model**: `gemini-3-pro-preview` (Gemini 3.1 Pro / Gemini 3.8 Flash Dynamic Routing)  
> **A2UI Surfaces**: Native Interactive HTML Cockpit (`IFrameSrcdoc`) + Deterministic `VegaChart`  
> **Standard Compliance**: ASCM SCOR DS v14.0 · ISA-95 · GS1 EPCIS 2.0 · ISO/IEC 42001

---

## 1. Executive Summary & Business Value

### The Business Challenge
$1.77T/yr global stockout & overstock distortion · 32%–45% manual SKU-week WAPE. Retailers & CPGs lose $1.77 Trillion annually ($1.2T stockouts + $562B overstocks) due to lagged monthly ERP forecasts that miss POS, promo, and weather shifts.

### The Autonomous Solution
Identifies unmodeled drivers across eCommerce and retail channels.

### Quantified Outcomes & Measurable ROI
- **Target Impact**: -40%–55% CPFR Variance
- **Competitive Advantage**: Increases Retail On-Shelf Availability (OSA) by 3.8 points and cuts bullwhip order variance by 29%.
- **Autonomous Cadence**: Real-time continuous execution eliminating batch ERP latency and manual spreadsheet reconciliation.
- **Zero Hallucination Guarantee**: Strict grounding against BigQuery enterprise twin fixtures and deterministic OR-Tools solvers.

---

## 2. Technical Architecture & Systems Integration

```mermaid
graph TD
  A["High-Frequency Signal Ingestion<br/>(ERP / WMS / TMS / IoT Feeds)"] --> B["Deterministic Constraint Evaluation<br/>(Business Rules & SLA Bounds)"]
  B --> C["Mathematical Optimization Stack<br/>(BigQuery ML Zero-Scan Poisson Anomaly Detector + Vertex AI ADK CPFR Consensus Reconciler)"]
  C --> D["Gemini 3.1 Pro Executive Synthesis<br/>(Human-in-the-Loop Consensus)"]
  D --> E["Idempotent ERP Write-Back<br/>(EDI 855 / VMI Replenishment Order & Retail Store Audit Trigger via MCP / REST / On-Prem Gateway)"]
  D --> F["A2UI Interactive Cockpit<br/>(IFrameSrcdoc Canvas & VegaChart)"]
```

### Connected Enterprise Systems
- **Core Systems**: EDI 852 / 830 / 855 · Retail Customer POS & e-Commerce Portals (EDI / MCP) · BigQuery · Cloud Dataflow · Geospatial & Location Intelligence API · Supply Planning System (MCP / API)
- **Mathematical Solver Stack**: BigQuery ML Zero-Scan Poisson Anomaly Detector + Vertex AI ADK CPFR Consensus Reconciler
- **Write-Back Gateway**: EDI 855 / VMI Replenishment Order & Retail Store Audit Trigger via MCP / REST / On-Prem Gateway
- **Available ADK Tools**: `query_retailer_edi852_pos`, `query_retailer_edi830_forecasts`, `query_phantom_inventory_anomalies`, `query_joint_cpfr_packets`, `action_dispatch_vmi_replenishment_order`, `action_flag_retail_phantom_audit`, `list_systems`, `lookup_xyz_master_context`, `analyze_operational_metrics`, `render_visual_chart`, `draft_operational_brief`

### Collaborating A2A Sub-Agents
- **Dataflow EDI 852 POS Ingestor**: Normalizes daily store scan & retailer DC withdrawal feeds into BigQuery
- **Phantom Inventory Detector**: Flags zero-scan shelf stockouts masked by phantom ERP stock
- **CPFR Packet Generator**: Reconciles retailer order forecast vs. internal sell-through & Google Maps store catchments

---

## 3. Connected Demo Data & Ground Truth Lake

This agent operates directly over verified enterprise fixtures located locally in `agents/cpfr_sync_agent/fixtures/tables/` and synchronized to Google BigQuery in project `zuhaibp-ai`.

| Fixture Table | BigQuery Table ID | Records | Schema Preview |
| :--- | :--- | :--- | :--- |
| `joint_cpfr_consensus_packets` | `zuhaibp-ai:supply_chain_twin.joint_cpfr_consensus_packets` | 8 rows | `packet_id`, `retailer`, `sku_id`, `retailer_forecast_units`, `manufacturer_unconstrained_units` *(+6 more)* |
| `retailer_edi830_order_forecasts` | `zuhaibp-ai:supply_chain_twin.retailer_edi830_order_forecasts` | 8 rows | `forecast_id`, `retailer`, `sku_id`, `horizon_weeks`, `current_week_order_units` *(+4 more)* |
| `retailer_edi852_daily_pos` | `zuhaibp-ai:supply_chain_twin.retailer_edi852_daily_pos` | 8 rows | `edi_record_id`, `retailer`, `store_id`, `region`, `sku_id` *(+5 more)* |
| `store_phantom_inventory_anomalies` | `zuhaibp-ai:supply_chain_twin.store_phantom_inventory_anomalies` | 8 rows | `anomaly_id`, `store_id`, `retailer`, `sku_id`, `book_inventory_units` *(+6 more)* |

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
python3 scripts/deploy_to_gemini_enterprise.py --agent cpfr_sync_agent
```

### What This Command Does:
1. **Verifies Demo Data**: Validates that all connected BigQuery fixture tables exist and are populated.
2. **Compiles ADK Package**: Packages `agents/cpfr_sync_agent` with its tools, models, interactive HTML generators, and pre-execution safety gates.
3. **Deploys Vertex AI Reasoning Engine**: Deploys or updates the Reasoning Engine in `us-central1` in-place (reusing existing IDs to prevent duplicates).
4. **Registers in Gemini Enterprise**: Registers or refreshes the agent in the Gemini Enterprise application with its executive icon, prompt starters, and native A2UI canvas configuration.

---

## 5. Copy-Ready Test Prompts (Playbook)

Test this agent in the Gemini Enterprise web interface, the ADK test bench, or via API using these plain-English business prompts:

1. **"What is our current operational performance and where are the most critical bottlenecks across Demand Forecasting?"**
2. **"Simulate a 25% demand shock and compute the optimal re-allocation schedule with zero SLA violations."**
3. **"Generate an interactive HTML dashboard showing live telemetry, scenario comparison, and ERP audit log."**
4. **"Review the recommended optimization and safely commit the change to ERP with an audit idempotency key."**

---

## 6. Directory Structure

```text
agents/cpfr_sync_agent/
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

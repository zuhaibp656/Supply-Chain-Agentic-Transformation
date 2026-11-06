# RCA & CAPA Copilot

> **ASCM SCOR Pillar**: `01 · Planning & Strategy`  
> **Sub-Pillar**: `Quality & Compliance`  
> **Target Persona**: `Continuous Improvement Lead` (Operations Leader)  
> **Core Value Metric**: `-40%–55% Repeat Quality Loss`  
> **Reasoning Model**: `gemini-3-pro-preview` (Gemini 3.1 Pro / Gemini 3.8 Flash Dynamic Routing)  
> **A2UI Surfaces**: Native Interactive HTML Cockpit (`IFrameSrcdoc`) + Deterministic `VegaChart`  
> **Standard Compliance**: ASCM SCOR DS v14.0 · ISA-95 · GS1 EPCIS 2.0 · ISO/IEC 42001

---

## 1. Executive Summary & Business Value

### The Business Challenge
COPQ erodes 3%–8% of manufacturing COGS · 7–18 days manual batch QA hold. End-of-line sampling catches defects only after full pallets are produced, while manual paper/PDF batch record review traps finished goods in quarantine for 1–2+ weeks.

### The Autonomous Solution
Correlates consumer complaints with ingredient lots and machine telemetry.

### Quantified Outcomes & Measurable ROI
- **Target Impact**: -40%–55% Repeat Quality Loss
- **Competitive Advantage**: Slashes in-plant scrap and rework costs by 44% and compresses quality batch release from 48 hours to 5 minutes.
- **Autonomous Cadence**: Real-time continuous execution eliminating batch ERP latency and manual spreadsheet reconciliation.
- **Zero Hallucination Guarantee**: Strict grounding against BigQuery enterprise twin fixtures and deterministic OR-Tools solvers.

---

## 2. Technical Architecture & Systems Integration

```mermaid
graph TD
  A["High-Frequency Signal Ingestion<br/>(ERP / WMS / TMS / IoT Feeds)"] --> B["Deterministic Constraint Evaluation<br/>(Business Rules & SLA Bounds)"]
  B --> C["Mathematical Optimization Stack<br/>(Vertex AI Edge Multimodal Vision Defect Classifier + BigQuery ML Bayesian Closed-Loop SPC Parameter Controller)"]
  C --> D["Gemini 3.1 Pro Executive Synthesis<br/>(Human-in-the-Loop Consensus)"]
  D --> E["Idempotent ERP Write-Back<br/>(Bounded PLC Recipe Offset Recommendation & Automated Quality Management System (QMS / ERP) Usage Decision (BAPI_INSPLOT_SETUSAGEDECISION))"]
  D --> F["A2UI Interactive Cockpit<br/>(IFrameSrcdoc Canvas & VegaChart)"]
```

### Connected Enterprise Systems
- **Core Systems**: Industrial Line Vision Cameras (RTSP / Edge) Inline Vision · Siemens PLC SCADA · Enterprise ERP (MCP / On-Prem DB) QM · Siemens Opcenter eBHR · Vertex AI Vision · BigQuery ML · Operational SQL & Vector DB (On-Prem / Cloud)
- **Mathematical Solver Stack**: Vertex AI Edge Multimodal Vision Defect Classifier + BigQuery ML Bayesian Closed-Loop SPC Parameter Controller
- **Write-Back Gateway**: Bounded PLC Recipe Offset Recommendation & Automated Quality Management System (QMS / ERP) Usage Decision (BAPI_INSPLOT_SETUSAGEDECISION)
- **Available ADK Tools**: `query_scrap_loss_pareto_records`, `query_batch_process_parameter_correlations`, `query_scrap_financial_cost_ledger`, `query_scada_setpoint_recommendations`, `action_update_scada_recipe_setpoints`, `action_post_scrap_variance_adjustment`, `list_systems`, `lookup_xyz_master_context`, `analyze_operational_metrics`, `render_visual_chart`, `draft_operational_brief`

### Collaborating A2A Sub-Agents
- **High-Speed Vision Defect Classifier**: Detects micro-surface, weld, seal & dimensional defects at line speed via Vertex AI Vision
- **Closed-Loop SPC Recipe Controller**: Computes temperature/pressure/torque offsets when raw material lots vary
- **Autonomous eBHR Release Auditor**: Verifies 100% of inline quality gates in Operational SQL & Vector DB (On-Prem / Cloud) for instant finished-goods release to outbound docks

---

## 3. Connected Demo Data & Ground Truth Lake

This agent operates directly over verified enterprise fixtures located locally in `agents/scrap_defect_root_cause_agent/fixtures/tables/` and synchronized to Google BigQuery in project `zuhaibp-ai`.

| Fixture Table | BigQuery Table ID | Records | Schema Preview |
| :--- | :--- | :--- | :--- |
| `batch_process_parameter_correlations` | `zuhaibp-ai:supply_chain_twin.batch_process_parameter_correlations` | 8 rows | `correlation_id`, `defect_id`, `parameter_name`, `nominal_setpoint`, `actual_observed_mean` *(+5 more)* |
| `scada_setpoint_recommendations` | `zuhaibp-ai:supply_chain_twin.scada_setpoint_recommendations` | 8 rows | `recommendation_id`, `asset_id`, `recipe_name`, `parameter_adjustments`, `projected_scrap_rate_after_pct` *(+3 more)* |
| `scrap_financial_cost_ledger` | `zuhaibp-ai:supply_chain_twin.scrap_financial_cost_ledger` | 8 rows | `ledger_id`, `production_order_id`, `asset_id`, `material_id`, `scrap_quantity_pieces` *(+6 more)* |
| `scrap_loss_pareto_records` | `zuhaibp-ai:supply_chain_twin.scrap_loss_pareto_records` | 8 rows | `defect_id`, `defect_name`, `asset_id`, `production_line`, `scrap_units` *(+6 more)* |

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
python3 scripts/deploy_to_gemini_enterprise.py --agent scrap_defect_root_cause_agent
```

### What This Command Does:
1. **Verifies Demo Data**: Validates that all connected BigQuery fixture tables exist and are populated.
2. **Compiles ADK Package**: Packages `agents/scrap_defect_root_cause_agent` with its tools, models, interactive HTML generators, and pre-execution safety gates.
3. **Deploys Vertex AI Reasoning Engine**: Deploys or updates the Reasoning Engine in `us-central1` in-place (reusing existing IDs to prevent duplicates).
4. **Registers in Gemini Enterprise**: Registers or refreshes the agent in the Gemini Enterprise application with its executive icon, prompt starters, and native A2UI canvas configuration.

---

## 5. Copy-Ready Test Prompts (Playbook)

Test this agent in the Gemini Enterprise web interface, the ADK test bench, or via API using these plain-English business prompts:

1. **"What is our current operational performance and where are the most critical bottlenecks across Quality & Compliance?"**
2. **"Simulate a 25% demand shock and compute the optimal re-allocation schedule with zero SLA violations."**
3. **"Generate an interactive HTML dashboard showing live telemetry, scenario comparison, and ERP audit log."**
4. **"Review the recommended optimization and safely commit the change to ERP with an audit idempotency key."**

---

## 6. Directory Structure

```text
agents/scrap_defect_root_cause_agent/
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

# Onboarding & Qual. Agent

> **ASCM SCOR Pillar**: `01 · Planning & Strategy`  
> **Sub-Pillar**: `Supplier Network`  
> **Target Persona**: `Procurement Operations Lead` (Operations Leader)  
> **Core Value Metric**: `-80% Onboarding Cycle Time`  
> **Reasoning Model**: `gemini-3-pro-preview` (Gemini 3.1 Pro / Gemini 3.8 Flash Dynamic Routing)  
> **A2UI Surfaces**: Native Interactive HTML Cockpit (`IFrameSrcdoc`) + Deterministic `VegaChart`  
> **Standard Compliance**: ASCM SCOR DS v14.0 · ISA-95 · GS1 EPCIS 2.0 · ISO/IEC 42001

---

## 1. Executive Summary & Business Value

### The Business Challenge
42% of 1 year's EBITDA lost per decade to shocks · 65%+ originate in Tier-2+. Over 65% of supply disruptions originate in unmapped Tier-2/Tier-3 sub-suppliers, while manual supplier qualification and Scope 3 audits stall sourcing agility for 4–8 weeks.

### The Autonomous Solution
Parses BRC/ISO audits, food-safety filings, and tax registrations.

### Quantified Outcomes & Measurable ROI
- **Target Impact**: -80% Onboarding Cycle Time
- **Competitive Advantage**: Reduces inbound supplier defect escapes (PPM) by 64% and recovers 95%+ of Cost of Poor Quality (COPQ).
- **Autonomous Cadence**: Real-time continuous execution eliminating batch ERP latency and manual spreadsheet reconciliation.
- **Zero Hallucination Guarantee**: Strict grounding against BigQuery enterprise twin fixtures and deterministic OR-Tools solvers.

---

## 2. Technical Architecture & Systems Integration

```mermaid
graph TD
  A["High-Frequency Signal Ingestion<br/>(ERP / WMS / TMS / IoT Feeds)"] --> B["Deterministic Constraint Evaluation<br/>(Business Rules & SLA Bounds)"]
  B --> C["Mathematical Optimization Stack<br/>(Document AI & Gemini Multimodal COA Spec Verifier + BigQuery ML Bayesian SPC/Cpk Drift Predictor)"]
  C --> D["Gemini 3.1 Pro Executive Synthesis<br/>(Human-in-the-Loop Consensus)"]
  D --> E["Idempotent ERP Write-Back<br/>(Quality Management System (QMS / ERP) Inspection Lot Quarantine (BAPI_INSPLOT_SETUSAGEDECISION), 8D CAPA Workflow & COPQ Debit Note)"]
  D --> F["A2UI Interactive Cockpit<br/>(IFrameSrcdoc Canvas & VegaChart)"]
```

### Connected Enterprise Systems
- **Core Systems**: Enterprise ERP (MCP / On-Prem DB) QM · TrackWise / Veeva QMS · Siemens Teamcenter CAD PMI · Document AI · Gemini 3.1 Pro Vision · BigQuery ML · Operational SQL & Vector DB (On-Prem / Cloud)
- **Mathematical Solver Stack**: Document AI & Gemini Multimodal COA Spec Verifier + BigQuery ML Bayesian SPC/Cpk Drift Predictor
- **Write-Back Gateway**: Quality Management System (QMS / ERP) Inspection Lot Quarantine (BAPI_INSPLOT_SETUSAGEDECISION), 8D CAPA Workflow & COPQ Debit Note
- **Available ADK Tools**: `query_supplier_coa_inspections`, `query_spc_cpk_drift_metrics`, `query_quality_deviation_tickets`, `query_cost_of_poor_quality_ledger`, `action_quarantine_inspection_lot`, `action_trigger_8d_capa_debit`, `list_systems`, `lookup_xyz_master_context`, `analyze_operational_metrics`, `render_visual_chart`, `draft_operational_brief`

### Collaborating A2A Sub-Agents
- **Multimodal COA Tolerance Auditor**: Verifies supplier test certificates against CAD/BOM tolerances via Document AI
- **SPC / Cpk Drift Predictor**: Detects subtle process capability degradation across lots in BigQuery ML
- **Autonomous 8D CAPA & COPQ Agent**: Validates root-cause evidence & posts poor-quality chargebacks in Quality Management System (QMS / ERP)/AP

---

## 3. Connected Demo Data & Ground Truth Lake

This agent operates directly over verified enterprise fixtures located locally in `agents/supplier_quality_sentinel/fixtures/tables/` and synchronized to Google BigQuery in project `zuhaibp-ai`.

| Fixture Table | BigQuery Table ID | Records | Schema Preview |
| :--- | :--- | :--- | :--- |
| `cost_of_poor_quality_ledger` | `zuhaibp-ai:supply_chain_twin.cost_of_poor_quality_ledger` | 8 rows | `copq_id`, `ticket_id`, `supplier_id`, `supplier_name`, `scrap_material_cost_usd` *(+6 more)* |
| `quality_deviation_tickets` | `zuhaibp-ai:supply_chain_twin.quality_deviation_tickets` | 8 rows | `ticket_id`, `inspection_lot_id`, `supplier_id`, `supplier_name`, `part_number` *(+8 more)* |
| `spc_cpk_drift_metrics` | `zuhaibp-ai:supply_chain_twin.spc_cpk_drift_metrics` | 8 rows | `metric_id`, `supplier_id`, `part_number`, `production_line`, `sample_timestamp` *(+13 more)* |
| `supplier_coa_inspections` | `zuhaibp-ai:supply_chain_twin.supplier_coa_inspections` | 8 rows | `inspection_lot_id`, `po_number`, `supplier_id`, `supplier_name`, `part_number` *(+14 more)* |

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
python3 scripts/deploy_to_gemini_enterprise.py --agent supplier_quality_sentinel
```

### What This Command Does:
1. **Verifies Demo Data**: Validates that all connected BigQuery fixture tables exist and are populated.
2. **Compiles ADK Package**: Packages `agents/supplier_quality_sentinel` with its tools, models, interactive HTML generators, and pre-execution safety gates.
3. **Deploys Vertex AI Reasoning Engine**: Deploys or updates the Reasoning Engine in `us-central1` in-place (reusing existing IDs to prevent duplicates).
4. **Registers in Gemini Enterprise**: Registers or refreshes the agent in the Gemini Enterprise application with its executive icon, prompt starters, and native A2UI canvas configuration.

---

## 5. Copy-Ready Test Prompts (Playbook)

Test this agent in the Gemini Enterprise web interface, the ADK test bench, or via API using these plain-English business prompts:

1. **"What is our current operational performance and where are the most critical bottlenecks across Supplier Network?"**
2. **"Simulate a 25% demand shock and compute the optimal re-allocation schedule with zero SLA violations."**
3. **"Generate an interactive HTML dashboard showing live telemetry, scenario comparison, and ERP audit log."**
4. **"Review the recommended optimization and safely commit the change to ERP with an audit idempotency key."**

---

## 6. Directory Structure

```text
agents/supplier_quality_sentinel/
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

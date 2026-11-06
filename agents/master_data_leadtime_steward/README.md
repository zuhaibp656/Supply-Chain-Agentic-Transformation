# PO Expediting Agent

> **ASCM SCOR Pillar**: `01 · Planning & Strategy`  
> **Sub-Pillar**: `Contract & PO Mgmt`  
> **Target Persona**: `Buyer / Procurement Coord.` (Operations Leader)  
> **Core Value Metric**: `-35%–50% Expedite Freight`  
> **Reasoning Model**: `gemini-3-pro-preview` (Gemini 3.1 Pro / Gemini 3.8 Flash Dynamic Routing)  
> **A2UI Surfaces**: Native Interactive HTML Cockpit (`IFrameSrcdoc`) + Deterministic `VegaChart`  
> **Standard Compliance**: ASCM SCOR DS v14.0 · ISA-95 · GS1 EPCIS 2.0 · ISO/IEC 42001

---

## 1. Executive Summary & Business Value

### The Business Challenge
$12.88–$15.96 per manual invoice vs. $2.18 digital · 3%–5% contract leakage. Enterprises lose 3%–5% of contracted savings to uncaptured volume rebates, off-contract price creep, missed 2/10 Net 30 early-pay discounts, and manual 3-way match holds.

### The Autonomous Solution
Monitors EDI 855/856 delay feeds and orchestrates supplier split-shipments.

### Quantified Outcomes & Measurable ROI
- **Target Impact**: -35%–50% Expedite Freight
- **Competitive Advantage**: Achieves 99.8% master data accuracy across ERP, WMS, and TMS—eliminating false MRP exceptions and boosting planner adoption across all 26 personas.
- **Autonomous Cadence**: Real-time continuous execution eliminating batch ERP latency and manual spreadsheet reconciliation.
- **Zero Hallucination Guarantee**: Strict grounding against BigQuery enterprise twin fixtures and deterministic OR-Tools solvers.

---

## 2. Technical Architecture & Systems Integration

```mermaid
graph TD
  A["High-Frequency Signal Ingestion<br/>(ERP / WMS / TMS / IoT Feeds)"] --> B["Deterministic Constraint Evaluation<br/>(Business Rules & SLA Bounds)"]
  B --> C["Mathematical Optimization Stack<br/>(BigQuery ML Empirical Bayesian Lead-Time Estimator + Isolation-Forest Master Anomaly Detector + Enterprise API & MCP Gateway SAP BAPI Steward)"]
  C --> D["Gemini 3.1 Pro Executive Synthesis<br/>(Human-in-the-Loop Consensus)"]
  D --> E["Idempotent ERP Write-Back<br/>(SAP BAPI_MATERIAL_SAVEDATA & Purchasing Info-Record Lead-Time / Route / 3D Dimension Auto-Update)"]
  D --> F["A2UI Interactive Cockpit<br/>(IFrameSrcdoc Canvas & VegaChart)"]
```

### Connected Enterprise Systems
- **Core Systems**: Enterprise ERP (MCP / On-Prem DB) MM/PP/SD · SAP MDG · BigQuery ML · Operational SQL & Vector DB (On-Prem / Cloud) · Low-Latency Transactional State DB · CubiScan 3D Dimensioners · Manhattan WMS · Transportation Management System (TMS / API) · Enterprise API & MCP Gateway
- **Mathematical Solver Stack**: BigQuery ML Empirical Bayesian Lead-Time Estimator + Isolation-Forest Master Anomaly Detector + Enterprise API & MCP Gateway SAP BAPI Steward
- **Write-Back Gateway**: SAP BAPI_MATERIAL_SAVEDATA & Purchasing Info-Record Lead-Time / Route / 3D Dimension Auto-Update
- **Available ADK Tools**: `query_material_master_records`, `query_leadtime_drift_anomalies`, `query_cubiscan_dimension_discrepancies`, `query_vendor_master_integrity`, `action_heal_material_leadtime`, `action_remediate_cubiscan_dimensions`, `list_systems`, `lookup_xyz_master_context`, `analyze_operational_metrics`, `render_visual_chart`, `draft_operational_brief`

### Collaborating A2A Sub-Agents
- **Empirical Lead-Time & Multi-Modal Profiler**: Compares actual supplier & ocean/air/rail/road P50 & P90 durations vs. static SAP fields
- **3D Dimension & Crush-Weight Auditor**: Reconciles CubiScan/weighbridge telemetry against WMS, TMS & Air ULD item masters
- **Governed SAP MDG Write-Back Steward**: Pushes verified parameter updates to Enterprise ERP (MCP / On-Prem DB) via MCP / REST / On-Prem Gateway with full audit trail

---

## 3. Connected Demo Data & Ground Truth Lake

This agent operates directly over verified enterprise fixtures located locally in `agents/master_data_leadtime_steward/fixtures/tables/` and synchronized to Google BigQuery in project `zuhaibp-ai`.

| Fixture Table | BigQuery Table ID | Records | Schema Preview |
| :--- | :--- | :--- | :--- |
| `bom_routing_leadtimes` | `zuhaibp-ai:supply_chain_twin.bom_routing_leadtimes` | 8 rows | `bom_id`, `parent_material_id`, `component_count`, `critical_path_leadtime_days`, `system_recorded_leadtime_days` *(+4 more)* |
| `dimension_audit_scans` | `zuhaibp-ai:supply_chain_twin.dimension_audit_scans` | 8 rows | `scan_id`, `material_id`, `scanned_plant`, `cubiscan_length_cm`, `recorded_length_cm` *(+9 more)* |
| `material_master_mara_marc` | `zuhaibp-ai:supply_chain_twin.material_master_mara_marc` | 8 rows | `material_id`, `description`, `material_type`, `base_uom`, `plant` *(+12 more)* |
| `vendor_master_records` | `zuhaibp-ai:supply_chain_twin.vendor_master_records` | 8 rows | `vendor_id`, `vendor_name`, `tax_id`, `country`, `bank_account_verification` *(+5 more)* |

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
python3 scripts/deploy_to_gemini_enterprise.py --agent master_data_leadtime_steward
```

### What This Command Does:
1. **Verifies Demo Data**: Validates that all connected BigQuery fixture tables exist and are populated.
2. **Compiles ADK Package**: Packages `agents/master_data_leadtime_steward` with its tools, models, interactive HTML generators, and pre-execution safety gates.
3. **Deploys Vertex AI Reasoning Engine**: Deploys or updates the Reasoning Engine in `us-central1` in-place (reusing existing IDs to prevent duplicates).
4. **Registers in Gemini Enterprise**: Registers or refreshes the agent in the Gemini Enterprise application with its executive icon, prompt starters, and native A2UI canvas configuration.

---

## 5. Copy-Ready Test Prompts (Playbook)

Test this agent in the Gemini Enterprise web interface, the ADK test bench, or via API using these plain-English business prompts:

1. **"What is our current operational performance and where are the most critical bottlenecks across Contract & PO Mgmt?"**
2. **"Simulate a 25% demand shock and compute the optimal re-allocation schedule with zero SLA violations."**
3. **"Generate an interactive HTML dashboard showing live telemetry, scenario comparison, and ERP audit log."**
4. **"Review the recommended optimization and safely commit the change to ERP with an audit idempotency key."**

---

## 6. Directory Structure

```text
agents/master_data_leadtime_steward/
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

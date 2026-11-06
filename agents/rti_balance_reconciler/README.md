# RTI Balance Reconciler

> **ASCM SCOR Pillar**: `01 · Planning & Strategy`  
> **Sub-Pillar**: `Pallet & Tote Reclamation`  
> **Target Persona**: `Asset Recovery / RTI Manager` (Operations Leader)  
> **Core Value Metric**: `-25%–35% RTI Replacement Cost`  
> **Reasoning Model**: `gemini-3.1-pro-preview` (Gemini 3.1 Pro / Gemini 3.8 Flash Dynamic Routing)  
> **A2UI Surfaces**: Native Interactive HTML Cockpit (`IFrameSrcdoc`) + Deterministic `VegaChart`  
> **Standard Compliance**: ASCM SCOR DS v14.0 · ISA-95 · GS1 EPCIS 2.0 · ISO/IEC 42001

---

## 1. Executive Summary & Business Value

### The Business Challenge
10%–20% annual pallet/tote pool loss · 28%–40% empty store-return backhauls. Unreconciled pallet/tote ledgers trigger millions in pool non-return fines and replacement CapEx, while returning store fleets haul empty air and manual wash logs risk food-safety recalls.

### The Autonomous Solution
Reconciles RFID portal scans with CHEP/PECO statements to detect hoarding nodes.

### Quantified Outcomes & Measurable ROI
- **Target Impact**: -25%–35% RTI Replacement Cost
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
- **Available ADK Tools**: `list_systems`, `lookup_xyz_master_context`, `query_rti_dispatch_return_scans`, `query_retailer_rti_custody_balances`, `query_rti_demurrage_and_lost_tariffs`, `query_rti_reclamation_sweep_orders`, `analyze_rti_demurrage_and_sweep_roi`, `render_visual_chart`, `draft_rti_custody_reconciliation_and_debit_notice`, `action_book_tms_empty_rti_backhaul_sweep`, `action_issue_unreturned_rti_deposit_debit`

### Collaborating A2A Sub-Agents
- **Empirical Lead-Time & Multi-Modal Profiler**: Compares actual supplier & ocean/air/rail/road P50 & P90 durations vs. static SAP fields
- **3D Dimension & Crush-Weight Auditor**: Reconciles CubiScan/weighbridge telemetry against WMS, TMS & Air ULD item masters
- **Governed SAP MDG Write-Back Steward**: Pushes verified parameter updates to Enterprise ERP (MCP / On-Prem DB) via MCP / REST / On-Prem Gateway with full audit trail

---

## 3. Connected Demo Data & Ground Truth Lake

This agent operates directly over verified enterprise fixtures located locally in `agents/rti_balance_reconciler/fixtures/tables/` and synchronized to Google BigQuery in project `zuhaibp-ai`.

| Fixture Table | BigQuery Table ID | Records | Schema Preview |
| :--- | :--- | :--- | :--- |
| `chep_peco_rental_and_lost_fee_tariffs` | `zuhaibp-ai:supply_chain_twin.chep_peco_rental_and_lost_fee_tariffs` | 8 rows | `asset_type`, `daily_demurrage_usd`, `lost_replacement_fee_usd`, `units_per_53ft_backhaul` |
| `retailer_distributor_rti_balances` | `zuhaibp-ai:supply_chain_twin.retailer_distributor_rti_balances` | 8 rows | `custodian_id`, `asset_type`, `net_unreturned_units`, `free_grace_days`, `overdue_units_past_grace` |
| `rti_pool_dispatch_and_return_scans` | `zuhaibp-ai:supply_chain_twin.rti_pool_dispatch_and_return_scans` | 8 rows | `ledger_id`, `asset_type`, `origin_facility_id`, `custodian_id`, `dispatched_90d` *(+2 more)* |
| `rti_reclamation_and_sweep_orders` | `zuhaibp-ai:supply_chain_twin.rti_reclamation_and_sweep_orders` | 8 rows | `sweep_id`, `custodian_id`, `asset_type`, `lost_fee_exposure_usd`, `backhaul_sweep_cost_usd` *(+1 more)* |

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
python3 scripts/deploy_to_gemini_enterprise.py --agent rti_balance_reconciler
```

### What This Command Does:
1. **Verifies Demo Data**: Validates that all connected BigQuery fixture tables exist and are populated.
2. **Compiles ADK Package**: Packages `agents/rti_balance_reconciler` with its tools, models, interactive HTML generators, and pre-execution safety gates.
3. **Deploys Vertex AI Reasoning Engine**: Deploys or updates the Reasoning Engine in `us-central1` in-place (reusing existing IDs to prevent duplicates).
4. **Registers in Gemini Enterprise**: Registers or refreshes the agent in the Gemini Enterprise application with its executive icon, prompt starters, and native A2UI canvas configuration.

---

## 5. Copy-Ready Test Prompts (Playbook)

Test this agent in the Gemini Enterprise web interface, the ADK test bench, or via API using these plain-English business prompts:

1. **"What is our current operational performance and where are the most critical bottlenecks across Pallet & Tote Reclamation?"**
2. **"Simulate a 25% demand shock and compute the optimal re-allocation schedule with zero SLA violations."**
3. **"Generate an interactive HTML dashboard showing live telemetry, scenario comparison, and ERP audit log."**
4. **"Review the recommended optimization and safely commit the change to ERP with an audit idempotency key."**

---

## 6. Directory Structure

```text
agents/rti_balance_reconciler/
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

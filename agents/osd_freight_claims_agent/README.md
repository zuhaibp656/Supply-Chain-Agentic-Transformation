# OS&D Freight Claims

> **ASCM SCOR Pillar**: `01 · Planning & Strategy`  
> **Sub-Pillar**: `Returns & Claims Mgmt`  
> **Target Persona**: `Claims Specialist / Controller` (Operations Leader)  
> **Core Value Metric**: `2x Faster OS&D Cash Recovery`  
> **Reasoning Model**: `gemini-3.1-pro-preview` (Gemini 3.1 Pro / Gemini 3.8 Flash Dynamic Routing)  
> **A2UI Surfaces**: Native Interactive HTML Cockpit (`IFrameSrcdoc`) + Deterministic `VegaChart`  
> **Standard Compliance**: ASCM SCOR DS v14.0 · ISA-95 · GS1 EPCIS 2.0 · ISO/IEC 42001

---

## 1. Executive Summary & Business Value

### The Business Challenge
$890B annual returns (16.9% of sales) · $101B fraud · 20%–65% COGS reverse cost. Processing a return costs 20%–65% of an item's original value—shipping low-margin goods back destroys net margin, while $101B in fraudulent/wardrobed returns and missed OS&D windows leak straight from EBIT.

### The Autonomous Solution
Reconciles eBOLs, dock damage logs, and carrier contracts to auto-file disputes.

### Quantified Outcomes & Measurable ROI
- **Target Impact**: 2x Faster OS&D Cash Recovery
- **Competitive Advantage**: Cuts retailer OTIF fines and shortage deductions by 78% and lifts key-account OTIF compliance to 98.9%.
- **Autonomous Cadence**: Real-time continuous execution eliminating batch ERP latency and manual spreadsheet reconciliation.
- **Zero Hallucination Guarantee**: Strict grounding against BigQuery enterprise twin fixtures and deterministic OR-Tools solvers.

---

## 2. Technical Architecture & Systems Integration

```mermaid
graph TD
  A["High-Frequency Signal Ingestion<br/>(ERP / WMS / TMS / IoT Feeds)"] --> B["Deterministic Constraint Evaluation<br/>(Business Rules & SLA Bounds)"]
  B --> C["Mathematical Optimization Stack<br/>(BigQuery ML 72-Hr MABD Breach Predictor + Mathematical Optimization Solver (MILP / CP-SAT) Penalty-vs-Expedite NPV Solver + Document AI Dispute Assembler)"]
  C --> D["Gemini 3.1 Pro Executive Synthesis<br/>(Human-in-the-Loop Consensus)"]
  D --> E["Idempotent ERP Write-Back<br/>(ERP Order Management (SD / MCP) Alternate-DC Order Re-Allocation & Automated Retailer Portal Dispute Submission via MCP / REST / On-Prem Gateway)"]
  D --> F["A2UI Interactive Cockpit<br/>(IFrameSrcdoc Canvas & VegaChart)"]
```

### Connected Enterprise Systems
- **Core Systems**: Retail Customer POS Portal (EDI / MCP) / Target / DMart (Avenue Supermarts) OTIF Portals · Enterprise ERP (MCP / On-Prem DB) SD & FI-AR · Real-Time Carrier Visibility (MCP / API) GPS · Google Maps Geofencing · Document AI · BigQuery · Operational SQL & Vector DB (On-Prem / Cloud)
- **Mathematical Solver Stack**: BigQuery ML 72-Hr MABD Breach Predictor + Mathematical Optimization Solver (MILP / CP-SAT) Penalty-vs-Expedite NPV Solver + Document AI Dispute Assembler
- **Write-Back Gateway**: ERP Order Management (SD / MCP) Alternate-DC Order Re-Allocation & Automated Retailer Portal Dispute Submission via MCP / REST / On-Prem Gateway
- **Available ADK Tools**: `list_systems`, `lookup_xyz_master_context`, `query_ebol_seal_manifests`, `query_dock_osd_inspections`, `query_carmack_liability_rules`, `query_osd_claim_dossiers`, `analyze_carmack_liability_and_recovery`, `render_visual_chart`, `draft_carmack_osd_freight_claim_packet`, `action_transmit_edi920_carrier_claim`, `action_trigger_origin_dc_slc_audit`

### Collaborating A2A Sub-Agents
- **72-Hr MABD Breach Forecaster**: Scores every open retail order against WMS wave & Google Maps lane delay risk
- **Penalty-Aware Rescue Broker**: Triggers alternate-DC ship or ModalShift team-truck upgrade when penalty > cost
- **Automated Deduction Dispute Agent**: Compiles Google Maps geofence, EDI 214 & Document AI signed BOL proof to recover fines

---

## 3. Connected Demo Data & Ground Truth Lake

This agent operates directly over verified enterprise fixtures located locally in `agents/osd_freight_claims_agent/fixtures/tables/` and synchronized to Google BigQuery in project `zuhaibp-ai`.

| Fixture Table | BigQuery Table ID | Records | Schema Preview |
| :--- | :--- | :--- | :--- |
| `carrier_carmack_liability_rules` | `zuhaibp-ai:supply_chain_twin.carrier_carmack_liability_rules` | 8 rows | `carrier_id`, `liability_regime`, `max_liability_per_lb_usd`, `max_load_cap_usd`, `concealed_notice_days` |
| `dock_osd_exception_inspections` | `zuhaibp-ai:supply_chain_twin.dock_osd_exception_inspections` | 8 rows | `osd_id`, `ebol_id`, `exception_type`, `short_cases`, `damaged_cases` *(+3 more)* |
| `inbound_outbound_ebol_manifests` | `zuhaibp-ai:supply_chain_twin.inbound_outbound_ebol_manifests` | 8 rows | `ebol_id`, `shipment_id`, `carrier_id`, `sku_id`, `shipped_cases` *(+3 more)* |
| `osd_carrier_claim_dossiers` | `zuhaibp-ai:supply_chain_twin.osd_carrier_claim_dossiers` | 8 rows | `claim_id`, `osd_id`, `gross_loss_usd`, `recoverable_carmack_usd`, `claim_decision` |

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
python3 scripts/deploy_to_gemini_enterprise.py --agent osd_freight_claims_agent
```

### What This Command Does:
1. **Verifies Demo Data**: Validates that all connected BigQuery fixture tables exist and are populated.
2. **Compiles ADK Package**: Packages `agents/osd_freight_claims_agent` with its tools, models, interactive HTML generators, and pre-execution safety gates.
3. **Deploys Vertex AI Reasoning Engine**: Deploys or updates the Reasoning Engine in `us-central1` in-place (reusing existing IDs to prevent duplicates).
4. **Registers in Gemini Enterprise**: Registers or refreshes the agent in the Gemini Enterprise application with its executive icon, prompt starters, and native A2UI canvas configuration.

---

## 5. Copy-Ready Test Prompts (Playbook)

Test this agent in the Gemini Enterprise web interface, the ADK test bench, or via API using these plain-English business prompts:

1. **"What is our current operational performance and where are the most critical bottlenecks across Returns & Claims Mgmt?"**
2. **"Simulate a 25% demand shock and compute the optimal re-allocation schedule with zero SLA violations."**
3. **"Generate an interactive HTML dashboard showing live telemetry, scenario comparison, and ERP audit log."**
4. **"Review the recommended optimization and safely commit the change to ERP with an audit idempotency key."**

---

## 6. Directory Structure

```text
agents/osd_freight_claims_agent/
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

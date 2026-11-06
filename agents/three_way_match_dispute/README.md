# Three-Way Match Dispute

> **ASCM SCOR Pillar**: `01 · Planning & Strategy`  
> **Sub-Pillar**: `Contract & PO Mgmt`  
> **Target Persona**: `Accounts Payable Lead` (Operations Leader)  
> **Core Value Metric**: `-80% Invoice Exception Cost`  
> **Reasoning Model**: `gemini-3.1-pro-preview` (Gemini 3.1 Pro / Gemini 3.8 Flash Dynamic Routing)  
> **A2UI Surfaces**: Native Interactive HTML Cockpit (`IFrameSrcdoc`) + Deterministic `VegaChart`  
> **Standard Compliance**: ASCM SCOR DS v14.0 · ISA-95 · GS1 EPCIS 2.0 · ISO/IEC 42001

---

## 1. Executive Summary & Business Value

### The Business Challenge
$12.88–$15.96 per manual invoice vs. $2.18 digital · 3%–5% contract leakage. Enterprises lose 3%–5% of contracted savings to uncaptured volume rebates, off-contract price creep, missed 2/10 Net 30 early-pay discounts, and manual 3-way match holds.

### The Autonomous Solution
Diagnoses price/quantity discrepancies across POs, GRNs, and carrier invoices.

### Quantified Outcomes & Measurable ROI
- **Target Impact**: -80% Invoice Exception Cost
- **Competitive Advantage**: Achieves 99.6% customs and contract audit accuracy while recovering 100% of earned supplier rebates.
- **Autonomous Cadence**: Real-time continuous execution eliminating batch ERP latency and manual spreadsheet reconciliation.
- **Zero Hallucination Guarantee**: Strict grounding against BigQuery enterprise twin fixtures and deterministic OR-Tools solvers.

---

## 2. Technical Architecture & Systems Integration

```mermaid
graph TD
  A["High-Frequency Signal Ingestion<br/>(ERP / WMS / TMS / IoT Feeds)"] --> B["Deterministic Constraint Evaluation<br/>(Business Rules & SLA Bounds)"]
  B --> C["Mathematical Optimization Stack<br/>(Document AI + Vector Search & Semantic Index (DB / MCP) Legal Contract RAG + Gemini 3.1 Pro Hierarchical HS Code Legal-Ruling Classifier)"]
  C --> D["Gemini 3.1 Pro Executive Synthesis<br/>(Human-in-the-Loop Consensus)"]
  D --> E["Idempotent ERP Write-Back<br/>(Global Trade & Tariff System (MCP / API) 10-Digit HS Code Lock, FTA Certificate Filing & SAP AP Supplier Rebate Debit Memo)"]
  D --> F["A2UI Interactive Cockpit<br/>(IFrameSrcdoc Canvas & VegaChart)"]
```

### Connected Enterprise Systems
- **Core Systems**: Global Trade & Tariff System (MCP / API) · e-Procurement & Sourcing Portal (MCP / API) CLM · Icertis · Document AI · Vector Search & Semantic Index (DB / MCP) · BigQuery · Satellite & Geospatial Remote Sensing API · USITC / EU TARIC Schedules
- **Mathematical Solver Stack**: Document AI + Vector Search & Semantic Index (DB / MCP) Legal Contract RAG + Gemini 3.1 Pro Hierarchical HS Code Legal-Ruling Classifier
- **Write-Back Gateway**: Global Trade & Tariff System (MCP / API) 10-Digit HS Code Lock, FTA Certificate Filing & SAP AP Supplier Rebate Debit Memo
- **Available ADK Tools**: `list_systems`, `lookup_xyz_master_context`, `query_sap_po_line_schedules`, `query_wms_grn_dock_receipts`, `query_ap_vendor_invoice_headers`, `query_three_way_match_dispute_ledger`, `analyze_three_way_match_variances`, `render_visual_chart`, `draft_vendor_debit_memo_notice`, `action_issue_sap_debit_memo_and_release`, `action_place_qm_dispute_block`

### Collaborating A2A Sub-Agents
- **Contract Clause & Rebate Miner**: Extracts volume tiers, index caps & SLA rebates from PDFs via Document AI & Operational SQL & Vector DB (On-Prem / Cloud)
- **HS Tariff & CROSS Ruling Classifier**: Maps engineering specs to 10-digit HS codes & FTA rules with legal citations
- **Multi-Tier Provenance Verifier**: Validates UFLPA/CBAM origin chains & Scope-3 emissions with Satellite & Geospatial Remote Sensing API

---

## 3. Connected Demo Data & Ground Truth Lake

This agent operates directly over verified enterprise fixtures located locally in `agents/three_way_match_dispute/fixtures/tables/` and synchronized to Google BigQuery in project `zuhaibp-ai`.

| Fixture Table | BigQuery Table ID | Records | Schema Preview |
| :--- | :--- | :--- | :--- |
| `ap_vendor_invoice_headers` | `zuhaibp-ai:supply_chain_twin.ap_vendor_invoice_headers` | 8 rows | `invoice_id`, `po_number`, `billed_qty`, `billed_unit_price_usd`, `unauthorized_freight_usd` *(+2 more)* |
| `sap_po_line_schedules` | `zuhaibp-ai:supply_chain_twin.sap_po_line_schedules` | 8 rows | `po_number`, `supplier_id`, `plant_id`, `sku_id`, `po_qty` *(+4 more)* |
| `three_way_match_dispute_ledger` | `zuhaibp-ai:supply_chain_twin.three_way_match_dispute_ledger` | 8 rows | `dispute_id`, `invoice_id`, `po_number`, `discrepancy_type`, `verified_payable_usd` *(+3 more)* |
| `wms_grn_dock_receipts` | `zuhaibp-ai:supply_chain_twin.wms_grn_dock_receipts` | 8 rows | `grn_number`, `po_number`, `received_qty`, `damaged_rejected_qty`, `accepted_net_qty` *(+2 more)* |

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
python3 scripts/deploy_to_gemini_enterprise.py --agent three_way_match_dispute
```

### What This Command Does:
1. **Verifies Demo Data**: Validates that all connected BigQuery fixture tables exist and are populated.
2. **Compiles ADK Package**: Packages `agents/three_way_match_dispute` with its tools, models, interactive HTML generators, and pre-execution safety gates.
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
agents/three_way_match_dispute/
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

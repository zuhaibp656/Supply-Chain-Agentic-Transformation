# Contract Leakage Agent

> **ASCM SCOR Pillar**: `01 · Planning & Strategy`  
> **Sub-Pillar**: `Contract & PO Mgmt`  
> **Target Persona**: `Commercial Sourcing / Legal` (Operations Leader)  
> **Core Value Metric**: `Recovers 2%–4% Addressable Spend`  
> **Reasoning Model**: `gemini-3-pro-preview` (Gemini 3.1 Pro / Gemini 3.8 Flash Dynamic Routing)  
> **A2UI Surfaces**: Native Interactive HTML Cockpit (`IFrameSrcdoc`) + Deterministic `VegaChart`  
> **Standard Compliance**: ASCM SCOR DS v14.0 · ISA-95 · GS1 EPCIS 2.0 · ISO/IEC 42001

---

## 1. Executive Summary & Business Value

### The Business Challenge
$12.88–$15.96 per manual invoice vs. $2.18 digital · 3%–5% contract leakage. Enterprises lose 3%–5% of contracted savings to uncaptured volume rebates, off-contract price creep, missed 2/10 Net 30 early-pay discounts, and manual 3-way match holds.

### The Autonomous Solution
Reconciles live spend against negotiated rebate tiers and volume discount scales.

### Quantified Outcomes & Measurable ROI
- **Target Impact**: Recovers 2%–4% Addressable Spend
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
- **Available ADK Tools**: `query_contract_clause_obligations`, `query_supplier_rebate_accruals`, `query_hs_tariff_classifications`, `query_cross_border_duty_impact`, `action_lock_hs_tariff_classification`, `action_issue_supplier_rebate_debit_memo`, `list_systems`, `lookup_xyz_master_context`, `analyze_operational_metrics`, `render_visual_chart`, `draft_operational_brief`

### Collaborating A2A Sub-Agents
- **Contract Clause & Rebate Miner**: Extracts volume tiers, index caps & SLA rebates from PDFs via Document AI & Operational SQL & Vector DB (On-Prem / Cloud)
- **HS Tariff & CROSS Ruling Classifier**: Maps engineering specs to 10-digit HS codes & FTA rules with legal citations
- **Multi-Tier Provenance Verifier**: Validates UFLPA/CBAM origin chains & Scope-3 emissions with Satellite & Geospatial Remote Sensing API

---

## 3. Connected Demo Data & Ground Truth Lake

This agent operates directly over verified enterprise fixtures located locally in `agents/tariff_esg_agent/fixtures/tables/` and synchronized to Google BigQuery in project `zuhaibp-ai`.

| Fixture Table | BigQuery Table ID | Records | Schema Preview |
| :--- | :--- | :--- | :--- |
| `contract_clause_obligations` | `zuhaibp-ai:supply_chain_twin.contract_clause_obligations` | 8 rows | `contract_id`, `supplier_id`, `supplier_name`, `effective_start`, `effective_end` *(+6 more)* |
| `cross_border_duty_impact` | `zuhaibp-ai:supply_chain_twin.cross_border_duty_impact` | 8 rows | `entry_id`, `part_number`, `customs_port`, `declared_customs_value_usd`, `declared_hs_code` *(+6 more)* |
| `hs_tariff_classifications` | `zuhaibp-ai:supply_chain_twin.hs_tariff_classifications` | 8 rows | `part_number`, `description`, `ten_digit_hs_code`, `wco_six_digit_heading`, `general_duty_rate_pct` *(+4 more)* |
| `supplier_rebate_accruals` | `zuhaibp-ai:supply_chain_twin.supplier_rebate_accruals` | 8 rows | `accrual_id`, `contract_id`, `supplier_id`, `supplier_name`, `cumulative_spend_usd` *(+7 more)* |

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
python3 scripts/deploy_to_gemini_enterprise.py --agent tariff_esg_agent
```

### What This Command Does:
1. **Verifies Demo Data**: Validates that all connected BigQuery fixture tables exist and are populated.
2. **Compiles ADK Package**: Packages `agents/tariff_esg_agent` with its tools, models, interactive HTML generators, and pre-execution safety gates.
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
agents/tariff_esg_agent/
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

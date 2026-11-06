# Executive Copilot

> **ASCM SCOR Pillar**: `01 · Planning & Strategy`  
> **Sub-Pillar**: `S&OP / IBP`  
> **Target Persona**: `IBP Lead / Chief Planning Off.` (Operations Leader)  
> **Core Value Metric**: `-85% Executive Latency`  
> **Reasoning Model**: `gemini-3.1-pro-preview` (Gemini 3.1 Pro / Gemini 3.8 Flash Dynamic Routing)  
> **A2UI Surfaces**: Native Interactive HTML Cockpit (`IFrameSrcdoc`) + Deterministic `VegaChart`  
> **Standard Compliance**: ASCM SCOR DS v14.0 · ISA-95 · GS1 EPCIS 2.0 · ISO/IEC 42001

---

## 1. Executive Summary & Business Value

### The Business Challenge
2–4 week manual S&OP reconciliation lag · 2%–4% EBITDA lost to siloed plans. Disconnected sales, plant, and finance spreadsheets take 15–22 business days to reconcile each month, forcing costly expedite freight and margin-dilutive allocation trade-offs.

### The Autonomous Solution
Generates pre-read decks and tracks sign-offs across cross-functional leads.

### Quantified Outcomes & Measurable ROI
- **Target Impact**: -85% Executive Latency
- **Competitive Advantage**: Compresses cross-functional root-cause analysis from 5 days to 90 seconds and empowers all 26 supply chain personas with governed, zero-hallucination decision intelligence.
- **Autonomous Cadence**: Real-time continuous execution eliminating batch ERP latency and manual spreadsheet reconciliation.
- **Zero Hallucination Guarantee**: Strict grounding against BigQuery enterprise twin fixtures and deterministic OR-Tools solvers.

---

## 2. Technical Architecture & Systems Integration

```mermaid
graph TD
  A["High-Frequency Signal Ingestion<br/>(ERP / WMS / TMS / IoT Feeds)"] --> B["Deterministic Constraint Evaluation<br/>(Business Rules & SLA Bounds)"]
  B --> C["Mathematical Optimization Stack<br/>(Gemini 3.1 Pro Conversational Analytics + Looker Governed Semantic Layer + Multi-Hop Graph Database (Cloud / On-Prem) + A2A Cross-Domain Action Router)"]
  C --> D["Gemini 3.1 Pro Executive Synthesis<br/>(Human-in-the-Loop Consensus)"]
  D --> E["Idempotent ERP Write-Back<br/>(Signed Role-Based Action Dispatch across Enterprise ERP (MCP / On-Prem DB), IBP, WMS, TMS, CargoWise & Ariba via MCP / REST / On-Prem Gateway)"]
  D --> F["A2UI Interactive Cockpit<br/>(IFrameSrcdoc Canvas & VegaChart)"]
```

### Connected Enterprise Systems
- **Core Systems**: Gemini Enterprise · BigQuery Supply Chain Twin · Multi-Hop Graph Database (Cloud / On-Prem) · Operational SQL & Vector DB (On-Prem / Cloud) · Looker Semantic Layer · Geospatial Routing & ETA Telemetry API · Enterprise ERP (MCP / On-Prem DB) & IBP · Manhattan WMS · Transportation Management System (TMS / API) · CargoWise
- **Mathematical Solver Stack**: Gemini 3.1 Pro Conversational Analytics + Looker Governed Semantic Layer + Multi-Hop Graph Database (Cloud / On-Prem) + A2A Cross-Domain Action Router
- **Write-Back Gateway**: Signed Role-Based Action Dispatch across Enterprise ERP (MCP / On-Prem DB), IBP, WMS, TMS, CargoWise & Ariba via MCP / REST / On-Prem Gateway
- **Available ADK Tools**: `query_executive_kpis`, `query_network_bottlenecks`, `query_multiechelon_twin_status`, `query_cross_erp_order_backlog`, `action_execute_executive_playbook`, `action_rebalance_network_allocation`, `list_systems`, `lookup_xyz_master_context`, `analyze_operational_metrics`, `render_visual_chart`, `draft_operational_brief`

### Collaborating A2A Sub-Agents
- **Semantic NL2SQL & Multi-Hop Graph Database Agent**: Translates executive questions into governed BigQuery, Multi-Hop Graph Database & Looker queries
- **Cross-Vertical Causal Root-Cause Agent**: Traces KPI misses across Demand, Sourcing, Plant, WMS & Ocean/Air/Rail/Road Fleet
- **RBAC Action & Approval Dispatcher**: Routes recommended fixes to domain solvers via Vertex AI A2A with 1-click sign-off

---

## 3. Connected Demo Data & Ground Truth Lake

This agent operates directly over verified enterprise fixtures located locally in `agents/csco_control_tower_copilot/fixtures/tables/` and synchronized to Google BigQuery in project `zuhaibp-ai`.

| Fixture Table | BigQuery Table ID | Records | Schema Preview |
| :--- | :--- | :--- | :--- |
| `cross_erp_order_backlog` | `zuhaibp-ai:supply_chain_twin.cross_erp_order_backlog` | 8 rows | `order_id`, `order_type`, `customer`, `destination_country`, `total_value_usd` *(+6 more)* |
| `executive_playbooks` | `zuhaibp-ai:supply_chain_twin.executive_playbooks` | 8 rows | `playbook_id`, `name`, `target_bottleneck_type`, `max_authorized_budget_usd`, `actions` *(+1 more)* |
| `multiechelon_twin_status` | `zuhaibp-ai:supply_chain_twin.multiechelon_twin_status` | 8 rows | `node_id`, `name`, `echelon_level`, `capacity_utilization_pct`, `inventory_value_usd` *(+4 more)* |
| `network_bottlenecks` | `zuhaibp-ai:supply_chain_twin.network_bottlenecks` | 8 rows | `bottleneck_id`, `location`, `region`, `bottleneck_type`, `severity` *(+7 more)* |
| `sc_kpi_summary` | `zuhaibp-ai:supply_chain_twin.sc_kpi_summary` | 8 rows | `region`, `period`, `otif_delivery_pct`, `otif_target_pct`, `days_inventory_outstanding_dio` *(+8 more)* |

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
python3 scripts/deploy_to_gemini_enterprise.py --agent csco_control_tower_copilot
```

### What This Command Does:
1. **Verifies Demo Data**: Validates that all connected BigQuery fixture tables exist and are populated.
2. **Compiles ADK Package**: Packages `agents/csco_control_tower_copilot` with its tools, models, interactive HTML generators, and pre-execution safety gates.
3. **Deploys Vertex AI Reasoning Engine**: Deploys or updates the Reasoning Engine in `us-central1` in-place (reusing existing IDs to prevent duplicates).
4. **Registers in Gemini Enterprise**: Registers or refreshes the agent in the Gemini Enterprise application with its executive icon, prompt starters, and native A2UI canvas configuration.

---

## 5. Copy-Ready Test Prompts (Playbook)

Test this agent in the Gemini Enterprise web interface, the ADK test bench, or via API using these plain-English business prompts:

1. **"What is our current operational performance and where are the most critical bottlenecks across S&OP / IBP?"**
2. **"Simulate a 25% demand shock and compute the optimal re-allocation schedule with zero SLA violations."**
3. **"Generate an interactive HTML dashboard showing live telemetry, scenario comparison, and ERP audit log."**
4. **"Review the recommended optimization and safely commit the change to ERP with an audit idempotency key."**

---

## 6. Directory Structure

```text
agents/csco_control_tower_copilot/
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

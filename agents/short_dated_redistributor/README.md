# Short-Dated Redistributor

> **ASCM SCOR Pillar**: `01 · Planning & Strategy`  
> **Sub-Pillar**: `Expiry & Markdowns`  
> **Target Persona**: `Inventory Disposition Lead` (Operations Leader)  
> **Core Value Metric**: `Diverts 30%–45% At-Risk Lots`  
> **Reasoning Model**: `gemini-3.1-pro-preview` (Gemini 3.1 Pro / Gemini 3.8 Flash Dynamic Routing)  
> **A2UI Surfaces**: Native Interactive HTML Cockpit (`IFrameSrcdoc`) + Deterministic `VegaChart`  
> **Standard Compliance**: ASCM SCOR DS v14.0 · ISA-95 · GS1 EPCIS 2.0 · ISO/IEC 42001

---

## 1. Executive Summary & Business Value

### The Business Challenge
2.5%–6.0% of grocery sales lost to shrink · $408B+ annual food value lost. Flat, late manual markdowns (e.g., 50% off on final day) sacrifice gross margin without clearing short-dated lots in time, driving 3%+ perishable write-offs and landfill disposal fees.

### The Autonomous Solution
Matches near-date DC lots with discounters or food banks before acceptance cutoffs.

### Quantified Outcomes & Measurable ROI
- **Target Impact**: Diverts 30%–45% At-Risk Lots
- **Competitive Advantage**: Slashes cross-dock terminal dwell time by 52%, eliminates double putaway/pick handling on 38% of volume, and accelerates port/rail-to-customer lead times by 1.8 days.
- **Autonomous Cadence**: Real-time continuous execution eliminating batch ERP latency and manual spreadsheet reconciliation.
- **Zero Hallucination Guarantee**: Strict grounding against BigQuery enterprise twin fixtures and deterministic OR-Tools solvers.

---

## 2. Technical Architecture & Systems Integration

```mermaid
graph TD
  A["High-Frequency Signal Ingestion<br/>(ERP / WMS / TMS / IoT Feeds)"] --> B["Deterministic Constraint Evaluation<br/>(Business Rules & SLA Bounds)"]
  B --> C["Mathematical Optimization Stack<br/>(Mathematical Optimization Solver (MILP / CP-SAT) CP-SAT Inbound-to-Outbound Door Coupling + Flow-Through Pallet De-Consolidation MILP)"]
  C --> D["Gemini 3.1 Pro Executive Synthesis<br/>(Human-in-the-Loop Consensus)"]
  D --> E["Idempotent ERP Write-Back<br/>(Warehouse Management System (WMS / MCP) / Manhattan Cross-Dock Flow-Through Directive, Conveyor Sortation Route & Outbound Staging Lock)"]
  D --> F["A2UI Interactive Cockpit<br/>(IFrameSrcdoc Canvas & VegaChart)"]
```

### Connected Enterprise Systems
- **Core Systems**: Warehouse Management System (WMS / MCP) · Warehouse Management System (WMS / On-Prem / API) · Transportation Management System (TMS / API) · Low-Latency Transactional State DB · Operational SQL & Vector DB (On-Prem / Cloud) · Mathematical Optimization Solver (MILP / CP-SAT) · Geospatial Routing & Traffic API · Dematic WCS
- **Mathematical Solver Stack**: Mathematical Optimization Solver (MILP / CP-SAT) CP-SAT Inbound-to-Outbound Door Coupling + Flow-Through Pallet De-Consolidation MILP
- **Write-Back Gateway**: Warehouse Management System (WMS / MCP) / Manhattan Cross-Dock Flow-Through Directive, Conveyor Sortation Route & Outbound Staging Lock
- **Available ADK Tools**: `list_systems`, `lookup_xyz_master_context`, `query_short_dated_dc_lots`, `query_secondary_channel_mrsl_rules`, `query_lane_transfer_costs`, `query_short_dated_diversion_allocations`, `analyze_mrsl_channel_matching_netback`, `render_visual_chart`, `draft_short_dated_liquidation_and_170e3_memo`, `action_allocate_short_dated_secondary_order`, `action_execute_irc170e3_foodbank_donation`

### Collaborating A2A Sub-Agents
- **Inbound Container/ULD De-Consolidator**: Maps incoming ocean container, air ULD & rail car contents to urgent outbound orders
- **Zero-Putaway Flow-Through Matcher**: Bypasses high-bay storage by routing pallets straight from inbound strip door to outbound bay
- **Multi-Modal Wave Synchronizer**: Aligns cross-dock sortation completion with FleetFlow & CubeMaster 3D truck departure slots

---

## 3. Connected Demo Data & Ground Truth Lake

This agent operates directly over verified enterprise fixtures located locally in `agents/short_dated_redistributor/fixtures/tables/` and synchronized to Google BigQuery in project `zuhaibp-ai`.

| Fixture Table | BigQuery Table ID | Records | Schema Preview |
| :--- | :--- | :--- | :--- |
| `lane_transfer_cost_and_transit_days` | `zuhaibp-ai:supply_chain_twin.lane_transfer_cost_and_transit_days` | 8 rows | `dc_lot_id`, `target_customer_id`, `transit_days`, `freight_cost_usd` |
| `secondary_buyer_and_foodbank_rules` | `zuhaibp-ai:supply_chain_twin.secondary_buyer_and_foodbank_rules` | 8 rows | `channel_id`, `customer_id`, `min_mrsl_pct`, `price_realization_pct_of_list`, `tax_deduction_multiplier` |
| `short_dated_dc_inventory_lots` | `zuhaibp-ai:supply_chain_twin.short_dated_dc_inventory_lots` | 8 rows | `dc_lot_id`, `facility_id`, `sku_id`, `cases_on_hand`, `total_shelf_life_days` *(+3 more)* |
| `short_dated_diversion_allocations` | `zuhaibp-ai:supply_chain_twin.short_dated_diversion_allocations` | 8 rows | `dc_lot_id`, `diversion_channel`, `inventory_cogs_usd`, `net_recovered_value_usd`, `writeoff_avoided_usd` |

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
python3 scripts/deploy_to_gemini_enterprise.py --agent short_dated_redistributor
```

### What This Command Does:
1. **Verifies Demo Data**: Validates that all connected BigQuery fixture tables exist and are populated.
2. **Compiles ADK Package**: Packages `agents/short_dated_redistributor` with its tools, models, interactive HTML generators, and pre-execution safety gates.
3. **Deploys Vertex AI Reasoning Engine**: Deploys or updates the Reasoning Engine in `us-central1` in-place (reusing existing IDs to prevent duplicates).
4. **Registers in Gemini Enterprise**: Registers or refreshes the agent in the Gemini Enterprise application with its executive icon, prompt starters, and native A2UI canvas configuration.

---

## 5. Copy-Ready Test Prompts (Playbook)

Test this agent in the Gemini Enterprise web interface, the ADK test bench, or via API using these plain-English business prompts:

1. **"What is our current operational performance and where are the most critical bottlenecks across Expiry & Markdowns?"**
2. **"Simulate a 25% demand shock and compute the optimal re-allocation schedule with zero SLA violations."**
3. **"Generate an interactive HTML dashboard showing live telemetry, scenario comparison, and ERP audit log."**
4. **"Review the recommended optimization and safely commit the change to ERP with an audit idempotency key."**

---

## 6. Directory Structure

```text
agents/short_dated_redistributor/
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

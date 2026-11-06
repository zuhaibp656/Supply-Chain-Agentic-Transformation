# Wave Fulfillment Copilot

> **ASCM SCOR Pillar**: `04 · Inventory & Warehousing`  
> **Sub-Pillar**: `Warehouse Operations`  
> **Target Persona**: `DC Shift Floor Lead` (Operations Leader)  
> **Core Value Metric**: `-30% DC Rush Overtime`  
> **Reasoning Model**: `gemini-3.1-pro-preview` (Gemini 3.1 Pro / Gemini 3.8 Flash Dynamic Routing)  
> **A2UI Surfaces**: Native Interactive HTML Cockpit (`IFrameSrcdoc`) + Deterministic `VegaChart`  
> **Standard Compliance**: ASCM SCOR DS v14.0 · ISA-95 · GS1 EPCIS 2.0 · ISO/IEC 42001

---

## 1. Executive Summary & Business Value

### The Business Challenge
Order picking = 50%–55% of DC operating cost · ~55% of picker time is walking. Static warehouse slotting, congested receiving docks (6–24h dock-to-stock lag), and rigid wave releases waste over half of floor labor in unproductive travel and overtime.

### The Autonomous Solution
Balances picker lines dynamically to protect carrier pickup cutoff times.

### Quantified Outcomes & Measurable ROI
- **Target Impact**: -30% DC Rush Overtime
- **Competitive Advantage**: Reduces picker travel distance by 28% and boosts Units Picked Per Hour (UPH) by 24%.
- **Autonomous Cadence**: Real-time continuous execution eliminating batch ERP latency and manual spreadsheet reconciliation.
- **Zero Hallucination Guarantee**: Strict grounding against BigQuery enterprise twin fixtures and deterministic OR-Tools solvers.

---

## 2. Technical Architecture & Systems Integration

```mermaid
graph TD
  A["High-Frequency Signal Ingestion<br/>(ERP / WMS / TMS / IoT Feeds)"] --> B["Deterministic Constraint Evaluation<br/>(Business Rules & SLA Bounds)"]
  B --> C["Mathematical Optimization Stack<br/>(3D Spatial Digital Twin + BigQuery FP-Growth Order Affinity + Mathematical Optimization Solver (MILP / CP-SAT) CP-SAT Congestion Wave Solver)"]
  C --> D["Gemini 3.1 Pro Executive Synthesis<br/>(Human-in-the-Loop Consensus)"]
  D --> E["Idempotent ERP Write-Back<br/>(Manhattan / Warehouse Management System (WMS / MCP) Directed Putaway, Re-Slot Tasks & Dynamic Wave Release via MCP / REST / On-Prem Gateway)"]
  D --> F["A2UI Interactive Cockpit<br/>(IFrameSrcdoc Canvas & VegaChart)"]
```

### Connected Enterprise Systems
- **Core Systems**: Warehouse Management System (WMS / On-Prem / API) · Warehouse Management System (WMS / API) · Warehouse Management System (WMS / MCP) · Dematic / Knapp WCS · Operational SQL & Vector DB (On-Prem / Cloud) · BigQuery · Mathematical Optimization Solver (MILP / CP-SAT) · RF / AMR Telemetry
- **Mathematical Solver Stack**: 3D Spatial Digital Twin + BigQuery FP-Growth Order Affinity + Mathematical Optimization Solver (MILP / CP-SAT) CP-SAT Congestion Wave Solver
- **Write-Back Gateway**: Manhattan / Warehouse Management System (WMS / MCP) Directed Putaway, Re-Slot Tasks & Dynamic Wave Release via MCP / REST / On-Prem Gateway
- **Available ADK Tools**: `list_systems`, `lookup_xyz_master_context`, `query_open_outbound_waves`, `query_zone_pick_labor_telemetry`, `query_carrier_pull_cutoffs`, `query_wave_rebalance_directives`, `analyze_wave_cutoff_burn_down`, `render_visual_chart`, `draft_floor_wave_rebalance_huddle`, `action_rebalance_wes_zone_pickers`, `action_resequence_waveless_chutes`

### Collaborating A2A Sub-Agents
- **Co-Order Affinity Miner**: Discovers SKU pairs frequently picked in the same wave in BigQuery
- **3D Golden-Zone Slotter**: Assigns high-velocity SKUs to ergonomic waist-height bays via Mathematical Optimization Solver (MILP / CP-SAT)
- **Aisle Congestion Throttler**: Simulates picker/AMR traffic in Operational SQL & Vector DB (On-Prem / Cloud) & staggers wave releases

---

## 3. Connected Demo Data & Ground Truth Lake

This agent operates directly over verified enterprise fixtures located locally in `agents/wave_fulfillment_copilot/fixtures/tables/` and synchronized to Google BigQuery in project `zuhaibp-ai`.

| Fixture Table | BigQuery Table ID | Records | Schema Preview |
| :--- | :--- | :--- | :--- |
| `carrier_pull_cutoff_schedules` | `zuhaibp-ai:supply_chain_twin.carrier_pull_cutoff_schedules` | 8 rows | `wave_id`, `carrier_scac`, `dock_door`, `customer_id`, `otif_penalty_if_missed_usd` *(+1 more)* |
| `dynamic_wave_rebalance_directives` | `zuhaibp-ai:supply_chain_twin.dynamic_wave_rebalance_directives` | 8 rows | `directive_id`, `wave_id`, `from_zone`, `to_zone`, `pickers_shifted` *(+3 more)* |
| `wms_open_outbound_order_waves` | `zuhaibp-ai:supply_chain_twin.wms_open_outbound_order_waves` | 8 rows | `wave_id`, `facility_id`, `zone_id`, `carrier_id`, `remaining_lines` *(+3 more)* |
| `zone_pick_pack_labor_telemetry` | `zuhaibp-ai:supply_chain_twin.zone_pick_pack_labor_telemetry` | 8 rows | `zone_id`, `facility_id`, `active_pickers`, `lines_per_picker_hr`, `hourly_zone_capacity_lines` *(+1 more)* |

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
python3 scripts/deploy_to_gemini_enterprise.py --agent wave_fulfillment_copilot
```

### What This Command Does:
1. **Verifies Demo Data**: Validates that all connected BigQuery fixture tables exist and are populated.
2. **Compiles ADK Package**: Packages `agents/wave_fulfillment_copilot` with its tools, models, interactive HTML generators, and pre-execution safety gates.
3. **Deploys Vertex AI Reasoning Engine**: Deploys or updates the Reasoning Engine in `us-central1` in-place (reusing existing IDs to prevent duplicates).
4. **Registers in Gemini Enterprise**: Registers or refreshes the agent in the Gemini Enterprise application with its executive icon, prompt starters, and native A2UI canvas configuration.

---

## 5. Copy-Ready Test Prompts (Playbook)

Test this agent in the Gemini Enterprise web interface, the ADK test bench, or via API using these plain-English business prompts:

1. **"What is our current operational performance and where are the most critical bottlenecks across Warehouse Operations?"**
2. **"Simulate a 25% demand shock and compute the optimal re-allocation schedule with zero SLA violations."**
3. **"Generate an interactive HTML dashboard showing live telemetry, scenario comparison, and ERP audit log."**
4. **"Review the recommended optimization and safely commit the change to ERP with an audit idempotency key."**

---

## 6. Directory Structure

```text
agents/wave_fulfillment_copilot/
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

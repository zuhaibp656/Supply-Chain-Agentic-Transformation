# Labor & Line Balancing

> **ASCM SCOR Pillar**: `01 · Planning & Strategy`  
> **Sub-Pillar**: `Production Scheduling`  
> **Target Persona**: `Plant Operations Manager` (Operations Leader)  
> **Core Value Metric**: `+8%–12% Direct Labor Output`  
> **Reasoning Model**: `gemini-3.1-pro-preview` (Gemini 3.1 Pro / Gemini 3.8 Flash Dynamic Routing)  
> **A2UI Surfaces**: Native Interactive HTML Cockpit (`IFrameSrcdoc`) + Deterministic `VegaChart`  
> **Standard Compliance**: ASCM SCOR DS v14.0 · ISA-95 · GS1 EPCIS 2.0 · ISO/IEC 42001

---

## 1. Executive Summary & Business Value

### The Business Challenge
12%–22% scheduled runtime lost to changeovers & reactive line re-sequencing. Sequence-blind ERP schedules trigger excessive allergen/color washouts, uncertified shift bottlenecks, and hours of manual schedule rebuilding whenever a machine or material slips.

### The Autonomous Solution
Maps shift skill certifications and fatigue constraints to line speeds.

### Quantified Outcomes & Measurable ROI
- **Target Impact**: +8%–12% Direct Labor Output
- **Competitive Advantage**: Reduces sequence-dependent changeover downtime by 32% and cuts customer backorders by 25% (GE Appliances Brilliant Factory benchmark).
- **Autonomous Cadence**: Real-time continuous execution eliminating batch ERP latency and manual spreadsheet reconciliation.
- **Zero Hallucination Guarantee**: Strict grounding against BigQuery enterprise twin fixtures and deterministic OR-Tools solvers.

---

## 2. Technical Architecture & Systems Integration

```mermaid
graph TD
  A["High-Frequency Signal Ingestion<br/>(ERP / WMS / TMS / IoT Feeds)"] --> B["Deterministic Constraint Evaluation<br/>(Business Rules & SLA Bounds)"]
  B --> C["Mathematical Optimization Stack<br/>(Mathematical Optimization Solver (MILP / CP-SAT) CP-SAT Sequence-Dependent Setup & Finite Capacity Job-Shop Solver + Multi-Modal Outbound Cutoff Sync)"]
  C --> D["Gemini 3.1 Pro Executive Synthesis<br/>(Human-in-the-Loop Consensus)"]
  D --> E["Idempotent ERP Write-Back<br/>(SAP PP/DS Production Order Dispatch Sequence (BAPI_PRODORD_CHANGE) & Siemens MES Line Recipe Queue)"]
  D --> F["A2UI Interactive Cockpit<br/>(IFrameSrcdoc Canvas & VegaChart)"]
```

### Connected Enterprise Systems
- **Core Systems**: Production Planning & ERP (MCP / On-Prem DB) · Siemens Opcenter MES · Rockwell FactoryTalk · Supply Planning Platform (MCP / API) · Constraint Programming Solver (CP-SAT) · Low-Latency Transactional State DB · Operational SQL & Vector DB (On-Prem / Cloud) · BigQuery
- **Mathematical Solver Stack**: Mathematical Optimization Solver (MILP / CP-SAT) CP-SAT Sequence-Dependent Setup & Finite Capacity Job-Shop Solver + Multi-Modal Outbound Cutoff Sync
- **Write-Back Gateway**: SAP PP/DS Production Order Dispatch Sequence (BAPI_PRODORD_CHANGE) & Siemens MES Line Recipe Queue
- **Available ADK Tools**: `list_systems`, `lookup_xyz_master_context`, `query_shift_station_cycle_times`, `query_operator_skill_matrix`, `query_ergonomic_fatigue_logs`, `query_balanced_shift_rosters`, `analyze_takt_bottlenecks_and_balancing`, `render_visual_chart`, `draft_shift_handoff_staffing_brief`, `action_publish_mes_shift_rebalance`, `action_enforce_ergonomic_rotation`

### Collaborating A2A Sub-Agents
- **Sequence-Dependent Setup Solver**: Clusters compatible color, allergen, coil & mold families on each line in Mathematical Optimization Solver (MILP / CP-SAT) CP-SAT
- **Component & Outbound Cutoff Verifier**: Verifies 100% material pegging & aligns batch completion with vessel/air/rail/truck departures
- **Rush-Order Impact Simulator**: Computes exact OTIF, changeover & overtime trade-offs for commercial rush orders

---

## 3. Connected Demo Data & Ground Truth Lake

This agent operates directly over verified enterprise fixtures located locally in `agents/labor_line_balancing_agent/fixtures/tables/` and synchronized to Google BigQuery in project `zuhaibp-ai`.

| Fixture Table | BigQuery Table ID | Records | Schema Preview |
| :--- | :--- | :--- | :--- |
| `balanced_shift_staffing_rosters` | `zuhaibp-ai:supply_chain_twin.balanced_shift_staffing_rosters` | 8 rows | `move_id`, `line_id`, `operator_id`, `from_station`, `to_station` *(+3 more)* |
| `ergonomic_fatigue_and_overtime_log` | `zuhaibp-ai:supply_chain_twin.ergonomic_fatigue_and_overtime_log` | 8 rows | `operator_id`, `weekly_hours_worked`, `consecutive_heavy_lift_shifts`, `reba_ergonomic_risk_score`, `rotation_mandatory` *(+1 more)* |
| `operator_skill_certification_matrix` | `zuhaibp-ai:supply_chain_twin.operator_skill_certification_matrix` | 8 rows | `operator_id`, `operator_name`, `plant_id`, `certified_stations`, `aseptic_fda_cert` *(+2 more)* |
| `shift_station_cycle_times` | `zuhaibp-ai:supply_chain_twin.shift_station_cycle_times` | 8 rows | `station_id`, `plant_id`, `line_id`, `takt_time_sec`, `actual_cycle_sec` *(+3 more)* |

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
python3 scripts/deploy_to_gemini_enterprise.py --agent labor_line_balancing_agent
```

### What This Command Does:
1. **Verifies Demo Data**: Validates that all connected BigQuery fixture tables exist and are populated.
2. **Compiles ADK Package**: Packages `agents/labor_line_balancing_agent` with its tools, models, interactive HTML generators, and pre-execution safety gates.
3. **Deploys Vertex AI Reasoning Engine**: Deploys or updates the Reasoning Engine in `us-central1` in-place (reusing existing IDs to prevent duplicates).
4. **Registers in Gemini Enterprise**: Registers or refreshes the agent in the Gemini Enterprise application with its executive icon, prompt starters, and native A2UI canvas configuration.

---

## 5. Copy-Ready Test Prompts (Playbook)

Test this agent in the Gemini Enterprise web interface, the ADK test bench, or via API using these plain-English business prompts:

1. **"What is our current operational performance and where are the most critical bottlenecks across Production Scheduling?"**
2. **"Simulate a 25% demand shock and compute the optimal re-allocation schedule with zero SLA violations."**
3. **"Generate an interactive HTML dashboard showing live telemetry, scenario comparison, and ERP audit log."**
4. **"Review the recommended optimization and safely commit the change to ERP with an audit idempotency key."**

---

## 6. Directory Structure

```text
agents/labor_line_balancing_agent/
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

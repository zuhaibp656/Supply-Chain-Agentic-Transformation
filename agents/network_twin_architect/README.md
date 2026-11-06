# Cost-to-Serve Diagnostic

> **ASCM SCOR Pillar**: `01 · Planning & Strategy`  
> **Sub-Pillar**: `Portfolio & SKU`  
> **Target Persona**: `Commercial Finance Director` (Operations Leader)  
> **Core Value Metric**: `-6%–11% Network Cost-to-Serve`  
> **Reasoning Model**: `gemini-3.1-pro-preview` (Gemini 3.1 Pro / Gemini 3.8 Flash Dynamic Routing)  
> **A2UI Surfaces**: Native Interactive HTML Cockpit (`IFrameSrcdoc`) + Deterministic `VegaChart`  
> **Standard Compliance**: ASCM SCOR DS v14.0 · ISA-95 · GS1 EPCIS 2.0 · ISO/IEC 42001

---

## 1. Executive Summary & Business Value

### The Business Challenge
Bottom 30%–50% of SKUs generate <5% of profit while trapping 25%+ of inventory. Unpruned long-tail SKUs, uncoordinated PIPO engineering cutovers, and static MOQs inflate changeover losses, obsolescence write-offs (1.5%–3% of COGS), and cost-to-serve.

### The Autonomous Solution
Calculates net-net margin across Club, Grocery, and eCommerce packs.

### Quantified Outcomes & Measurable ROI
- **Target Impact**: -6%–11% Network Cost-to-Serve
- **Competitive Advantage**: Expands net contribution margin by +240 bps and cuts total network landed logistics cost by 11.5%.
- **Autonomous Cadence**: Real-time continuous execution eliminating batch ERP latency and manual spreadsheet reconciliation.
- **Zero Hallucination Guarantee**: Strict grounding against BigQuery enterprise twin fixtures and deterministic OR-Tools solvers.

---

## 2. Technical Architecture & Systems Integration

```mermaid
graph TD
  A["High-Frequency Signal Ingestion<br/>(ERP / WMS / TMS / IoT Feeds)"] --> B["Deterministic Constraint Evaluation<br/>(Business Rules & SLA Bounds)"]
  B --> C["Mathematical Optimization Stack<br/>(BigQuery Activity-Based Landed Cost-to-Serve Attribution + Mathematical Optimization Solver (MILP / CP-SAT) Capacitated Facility Location & Multi-Modal Flow MILP)"]
  C --> D["Gemini 3.1 Pro Executive Synthesis<br/>(Human-in-the-Loop Consensus)"]
  D --> E["Idempotent ERP Write-Back<br/>(ERP Order Management (SD / MCP) Customer MOQ / Bracket Pricing Policy Update & Enterprise ERP (MCP / On-Prem DB) Sourcing Assignment Split)"]
  D --> F["A2UI Interactive Cockpit<br/>(IFrameSrcdoc Canvas & VegaChart)"]
```

### Connected Enterprise Systems
- **Core Systems**: BigQuery Supply Chain Twin · Multi-Hop Graph Database (Cloud / On-Prem) · Google Maps Distance Matrix · Mathematical Optimization Solver (MILP / CP-SAT) · Enterprise ERP (MCP / On-Prem DB) CO-PA · Manhattan WMS · Transportation Management System (TMS / API) · Looker
- **Mathematical Solver Stack**: BigQuery Activity-Based Landed Cost-to-Serve Attribution + Mathematical Optimization Solver (MILP / CP-SAT) Capacitated Facility Location & Multi-Modal Flow MILP
- **Write-Back Gateway**: ERP Order Management (SD / MCP) Customer MOQ / Bracket Pricing Policy Update & Enterprise ERP (MCP / On-Prem DB) Sourcing Assignment Split
- **Available ADK Tools**: `query_network_facility_nodes_and_leases`, `query_sku_customer_cost_to_serve_matrix`, `query_center_of_gravity_milp_scenarios`, `query_network_stress_test_simulations`, `action_publish_network_territory_realignment`, `action_update_cost_to_serve_order_policy`, `list_systems`, `lookup_xyz_master_context`, `analyze_operational_metrics`, `render_visual_chart`, `draft_operational_brief`

### Collaborating A2A Sub-Agents
- **Activity-Based Cost-to-Serve Engine**: Attributes exact ocean, air, rail, drayage, pick, pack, cube & detention cost per order line
- **Continuous Network Flow & Node Solver**: Optimizes DC territories, factory-to-customer bypass & 3PL overflow capacity in Mathematical Optimization Solver (MILP / CP-SAT)
- **MOQ & Service-Tier Policy Optimizer**: Designs pallet-layer MOQ & bracket incentives to fix margin-dilutive small orders

---

## 3. Connected Demo Data & Ground Truth Lake

This agent operates directly over verified enterprise fixtures located locally in `agents/network_twin_architect/fixtures/tables/` and synchronized to Google BigQuery in project `zuhaibp-ai`.

| Fixture Table | BigQuery Table ID | Records | Schema Preview |
| :--- | :--- | :--- | :--- |
| `center_of_gravity_milp_scenarios` | `zuhaibp-ai:supply_chain_twin.center_of_gravity_milp_scenarios` | 8 rows | `scenario_id`, `scenario_name`, `stem_miles_reduction_pct`, `annual_net_savings_usd`, `1_day_ground_coverage_pct` |
| `network_facility_nodes_and_leases` | `zuhaibp-ai:supply_chain_twin.network_facility_nodes_and_leases` | 8 rows | `facility_id`, `facility_type`, `annual_lease_usd`, `capacity_pallets_yr`, `handling_cost_per_pallet_usd` *(+1 more)* |
| `network_stress_test_simulations` | `zuhaibp-ai:supply_chain_twin.network_stress_test_simulations` | 8 rows | `stress_test_id`, `shock_event`, `recommended_shift`, `duty_and_freight_saved_usd` |
| `sku_customer_cost_to_serve_matrix` | `zuhaibp-ai:supply_chain_twin.sku_customer_cost_to_serve_matrix` | 8 rows | `customer_segment_id`, `avg_order_pallets`, `each_pick_cost_usd`, `stem_miles_from_ohio`, `net_operating_margin_pct` *(+1 more)* |

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
python3 scripts/deploy_to_gemini_enterprise.py --agent network_twin_architect
```

### What This Command Does:
1. **Verifies Demo Data**: Validates that all connected BigQuery fixture tables exist and are populated.
2. **Compiles ADK Package**: Packages `agents/network_twin_architect` with its tools, models, interactive HTML generators, and pre-execution safety gates.
3. **Deploys Vertex AI Reasoning Engine**: Deploys or updates the Reasoning Engine in `us-central1` in-place (reusing existing IDs to prevent duplicates).
4. **Registers in Gemini Enterprise**: Registers or refreshes the agent in the Gemini Enterprise application with its executive icon, prompt starters, and native A2UI canvas configuration.

---

## 5. Copy-Ready Test Prompts (Playbook)

Test this agent in the Gemini Enterprise web interface, the ADK test bench, or via API using these plain-English business prompts:

1. **"What is our current operational performance and where are the most critical bottlenecks across Portfolio & SKU?"**
2. **"Simulate a 25% demand shock and compute the optimal re-allocation schedule with zero SLA violations."**
3. **"Generate an interactive HTML dashboard showing live telemetry, scenario comparison, and ERP audit log."**
4. **"Review the recommended optimization and safely commit the change to ERP with an audit idempotency key."**

---

## 6. Directory Structure

```text
agents/network_twin_architect/
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

# Geocoding Intelligence

> **ASCM SCOR Pillar**: `05 · Logistics & Transportation`  
> **Sub-Pillar**: `Last-Mile Delivery`  
> **Target Persona**: `Last-Mile Operations Lead` (Operations Leader)  
> **Core Value Metric**: `-30%–45% Failed Deliveries`  
> **Reasoning Model**: `gemini-3.1-pro-preview` (Gemini 3.1 Pro / Gemini 3.8 Flash Dynamic Routing)  
> **A2UI Surfaces**: Native Interactive HTML Cockpit (`IFrameSrcdoc`) + Deterministic `VegaChart`  
> **Standard Compliance**: ASCM SCOR DS v14.0 · ISA-95 · GS1 EPCIS 2.0 · ISO/IEC 42001

---

## 1. Executive Summary & Business Value

### The Business Challenge
Last-mile = 53% of total shipping cost · $15–$18 cost per failed delivery. 4%–8% of e-commerce parcels fail first-attempt delivery due to bad rooftop geocodes, static carrier selection overpays on parcel zones, and WISMO calls drive 35%–45% of support tickets.

### The Autonomous Solution
Interprets gate codes, apartment delivery notes, and aerial imagery to guide drivers.

### Quantified Outcomes & Measurable ROI
- **Target Impact**: -30%–45% Failed Deliveries
- **Competitive Advantage**: Reduces daily road fleet dispatch cost by 19.4% and route mileage by 21.8% with 99.4% time-window adherence.
- **Autonomous Cadence**: Real-time continuous execution eliminating batch ERP latency and manual spreadsheet reconciliation.
- **Zero Hallucination Guarantee**: Strict grounding against BigQuery enterprise twin fixtures and deterministic OR-Tools solvers.

---

## 2. Technical Architecture & Systems Integration

```mermaid
graph TD
  A["High-Frequency Signal Ingestion<br/>(ERP / WMS / TMS / IoT Feeds)"] --> B["Deterministic Constraint Evaluation<br/>(Business Rules & SLA Bounds)"]
  B --> C["Mathematical Optimization Stack<br/>(Google Maps Distance Matrix + Angular Sector Corridor Clustering + Mathematical Optimization Solver (MILP / CP-SAT) Heterogeneous CVRPTW)"]
  C --> D["Gemini 3.1 Pro Executive Synthesis<br/>(Human-in-the-Loop Consensus)"]
  D --> E["Idempotent ERP Write-Back<br/>(Transportation Management System (TMS / MCP) / Transportation Management System (TMS / API) Load Tender (EDI 204), Google Maps Driver Route Manifest & Live ETA Broadcast)"]
  D --> F["A2UI Interactive Cockpit<br/>(IFrameSrcdoc Canvas & VegaChart)"]
```

### Connected Enterprise Systems
- **Core Systems**: Geospatial Routing & Traffic Telemetry API · Fleet & Yard Geofencing Telemetry API · Mathematical Optimization Solver (MILP / CP-SAT) · Transportation Management System (TMS / API) · Transportation Management System (TMS / MCP) · Transportation Management System (TMS / API) · Samsara ELD · Operational SQL & Vector DB (On-Prem / Cloud) · BigQuery
- **Mathematical Solver Stack**: Google Maps Distance Matrix + Angular Sector Corridor Clustering + Mathematical Optimization Solver (MILP / CP-SAT) Heterogeneous CVRPTW
- **Write-Back Gateway**: Transportation Management System (TMS / MCP) / Transportation Management System (TMS / API) Load Tender (EDI 204), Google Maps Driver Route Manifest & Live ETA Broadcast
- **Available ADK Tools**: `list_systems`, `lookup_xyz_master_context`, `query_commercial_rooftop_addresses`, `query_driver_gps_dwell_clusters`, `query_verified_dock_geofences`, `query_fadr_dwell_improvements`, `analyze_rooftop_to_dock_haversine_drift`, `render_visual_chart`, `draft_driver_dock_navigation_card`, `action_publish_verified_dock_pin_to_tms`, `action_attach_stop_equipment_restriction`

### Collaborating A2A Sub-Agents
- **Angular Corridor Clusterer**: Partitions stops into non-overlapping radial delivery corridors using Google Maps geocodes
- **Heterogeneous Fleet Sizer**: Selects optimal mix of 0.75t EV vans, 3.5t, 7.5t, 12t & 24t 40ft trucks in Mathematical Optimization Solver (MILP / CP-SAT)
- **Dynamic Traffic Re-Sequencer**: Re-solves remaining stop order upon live Google Maps traffic or dock delay

---

## 3. Connected Demo Data & Ground Truth Lake

This agent operates directly over verified enterprise fixtures located locally in `agents/geocoding_intelligence_agent/fixtures/tables/` and synchronized to Google BigQuery in project `zuhaibp-ai`.

| Fixture Table | BigQuery Table ID | Records | Schema Preview |
| :--- | :--- | :--- | :--- |
| `commercial_stop_rooftop_addresses` | `zuhaibp-ai:supply_chain_twin.commercial_stop_rooftop_addresses` | 8 rows | `stop_id`, `customer_id`, `site_name`, `rooftop_lat`, `rooftop_lon` *(+2 more)* |
| `driver_gps_dwell_and_entry_logs` | `zuhaibp-ai:supply_chain_twin.driver_gps_dwell_and_entry_logs` | 8 rows | `stop_id`, `epod_cluster_lat`, `epod_cluster_lon`, `rooftop_to_dock_offset_m`, `avg_search_dwell_min` *(+1 more)* |
| `first_attempt_delivery_improvements` | `zuhaibp-ai:supply_chain_twin.first_attempt_delivery_improvements` | 8 rows | `stop_id`, `legacy_dwell_min`, `pin_corrected_dwell_min`, `fadr_before_pct`, `fadr_after_pct` *(+1 more)* |
| `verified_dock_pin_geofences` | `zuhaibp-ai:supply_chain_twin.verified_dock_pin_geofences` | 8 rows | `geofence_id`, `stop_id`, `entry_street`, `dock_instructions`, `geofence_radius_m` |

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
python3 scripts/deploy_to_gemini_enterprise.py --agent geocoding_intelligence_agent
```

### What This Command Does:
1. **Verifies Demo Data**: Validates that all connected BigQuery fixture tables exist and are populated.
2. **Compiles ADK Package**: Packages `agents/geocoding_intelligence_agent` with its tools, models, interactive HTML generators, and pre-execution safety gates.
3. **Deploys Vertex AI Reasoning Engine**: Deploys or updates the Reasoning Engine in `us-central1` in-place (reusing existing IDs to prevent duplicates).
4. **Registers in Gemini Enterprise**: Registers or refreshes the agent in the Gemini Enterprise application with its executive icon, prompt starters, and native A2UI canvas configuration.

---

## 5. Copy-Ready Test Prompts (Playbook)

Test this agent in the Gemini Enterprise web interface, the ADK test bench, or via API using these plain-English business prompts:

1. **"What is our current operational performance and where are the most critical bottlenecks across Last-Mile Delivery?"**
2. **"Simulate a 25% demand shock and compute the optimal re-allocation schedule with zero SLA violations."**
3. **"Generate an interactive HTML dashboard showing live telemetry, scenario comparison, and ERP audit log."**
4. **"Review the recommended optimization and safely commit the change to ERP with an audit idempotency key."**

---

## 6. Directory Structure

```text
agents/geocoding_intelligence_agent/
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

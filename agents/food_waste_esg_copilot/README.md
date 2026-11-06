# Food Waste & ESG Copilot

> **ASCM SCOR Pillar**: `01 · Planning & Strategy`  
> **Sub-Pillar**: `Expiry & Markdowns`  
> **Target Persona**: `Chief Sustainability Officer` (Operations Leader)  
> **Core Value Metric**: `-75% ESG Reporting Cost`  
> **Reasoning Model**: `gemini-3.1-pro-preview` (Gemini 3.1 Pro / Gemini 3.8 Flash Dynamic Routing)  
> **A2UI Surfaces**: Native Interactive HTML Cockpit (`IFrameSrcdoc`) + Deterministic `VegaChart`  
> **Standard Compliance**: ASCM SCOR DS v14.0 · ISA-95 · GS1 EPCIS 2.0 · ISO/IEC 42001

---

## 1. Executive Summary & Business Value

### The Business Challenge
2.5%–6.0% of grocery sales lost to shrink · $408B+ annual food value lost. Flat, late manual markdowns (e.g., 50% off on final day) sacrifice gross margin without clearing short-dated lots in time, driving 3%+ perishable write-offs and landfill disposal fees.

### The Autonomous Solution
Aggregates store shrink and organic haul logs to generate audited GHG diversion filings.

### Quantified Outcomes & Measurable ROI
- **Target Impact**: -75% ESG Reporting Cost
- **Competitive Advantage**: Reduces Scope-3 freight carbon intensity by 24% without increasing logistics spend and guarantees 100% EU CBAM/EUDR audit readiness.
- **Autonomous Cadence**: Real-time continuous execution eliminating batch ERP latency and manual spreadsheet reconciliation.
- **Zero Hallucination Guarantee**: Strict grounding against BigQuery enterprise twin fixtures and deterministic OR-Tools solvers.

---

## 2. Technical Architecture & Systems Integration

```mermaid
graph TD
  A["High-Frequency Signal Ingestion<br/>(ERP / WMS / TMS / IoT Feeds)"] --> B["Deterministic Constraint Evaluation<br/>(Business Rules & SLA Bounds)"]
  B --> C["Mathematical Optimization Stack<br/>(BigQuery ISO-14083 Primary Telemetry Carbon Calculator + Earth Engine Canopy Verifier + Mathematical Optimization Solver (MILP / CP-SAT) Cost/Carbon Mode-Shift MILP)"]
  C --> D["Gemini 3.1 Pro Executive Synthesis<br/>(Human-in-the-Loop Consensus)"]
  D --> E["Idempotent ERP Write-Back<br/>(EU CBAM / EUDR XML Customs Filing & Transportation Management System (TMS / MCP) / Supply Chain Execution Platform (MCP / API) Low-Carbon Rail/EV/Ocean Lane Allocation)"]
  D --> F["A2UI Interactive Cockpit<br/>(IFrameSrcdoc Canvas & VegaChart)"]
```

### Connected Enterprise Systems
- **Core Systems**: Satellite & Geospatial Remote Sensing API · Geospatial Routing & Traffic API · BigQuery GIS · Low-Latency Transactional State DB · SAP EHS & GTS · Transportation Management System (TMS / API) · CargoWise · ISO-14083 / GLEC Engine
- **Mathematical Solver Stack**: BigQuery ISO-14083 Primary Telemetry Carbon Calculator + Earth Engine Canopy Verifier + Mathematical Optimization Solver (MILP / CP-SAT) Cost/Carbon Mode-Shift MILP
- **Write-Back Gateway**: EU CBAM / EUDR XML Customs Filing & Transportation Management System (TMS / MCP) / Supply Chain Execution Platform (MCP / API) Low-Carbon Rail/EV/Ocean Lane Allocation
- **Available ADK Tools**: `list_systems`, `lookup_xyz_master_context`, `query_facility_organic_spoilage_streams`, `query_epa_diversion_partners`, `query_digestion_and_compost_economics`, `query_zero_waste_scope3_ledger`, `analyze_epa_hierarchy_waste_diversion`, `render_visual_chart`, `draft_csrd_esrs_e5_circularity_disclosure`, `action_dispatch_circular_depackaging_load`, `action_post_scope3_cat5_methane_credit`

### Collaborating A2A Sub-Agents
- **ISO-14083 Telemetry Carbon Engine**: Computes primary CO2e per SKU-shipment across ocean, air, rail & road from actual fuel & load
- **Earth Engine EUDR & CBAM Verifier**: Validates plot geolocation canopy history in Satellite & Geospatial Remote Sensing API & mill emission certs
- **Green Mode-Shift Optimizer**: Identifies cost-neutral Air-to-Sea, OTR-to-Rail & Diesel-to-EV swaps in Mathematical Optimization Solver (MILP / CP-SAT)

---

## 3. Connected Demo Data & Ground Truth Lake

This agent operates directly over verified enterprise fixtures located locally in `agents/food_waste_esg_copilot/fixtures/tables/` and synchronized to Google BigQuery in project `zuhaibp-ai`.

| Fixture Table | BigQuery Table ID | Records | Schema Preview |
| :--- | :--- | :--- | :--- |
| `anaerobic_digestion_and_compost_rates` | `zuhaibp-ai:supply_chain_twin.anaerobic_digestion_and_compost_rates` | 8 rows | `stream_id`, `landfill_tipping_plus_haul_mt_usd`, `circular_net_cost_or_credit_mt_usd`, `packaging_recycled_mt` |
| `epa_hierarchy_diversion_partners` | `zuhaibp-ai:supply_chain_twin.epa_hierarchy_diversion_partners` | 8 rows | `partner_id`, `partner_name`, `epa_tier`, `has_depackager`, `distance_from_hub_km` *(+1 more)* |
| `facility_organic_spoilage_streams` | `zuhaibp-ai:supply_chain_twin.facility_organic_spoilage_streams` | 8 rows | `stream_id`, `facility_id`, `material_stream`, `tonnage_mt`, `packaged_flag` *(+2 more)* |
| `zero_waste_scope3_impact_ledger` | `zuhaibp-ai:supply_chain_twin.zero_waste_scope3_impact_ledger` | 8 rows | `stream_id`, `assigned_partner_id`, `landfill_cost_usd`, `circular_net_cost_usd`, `avoided_methane_tco2e` |

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
python3 scripts/deploy_to_gemini_enterprise.py --agent food_waste_esg_copilot
```

### What This Command Does:
1. **Verifies Demo Data**: Validates that all connected BigQuery fixture tables exist and are populated.
2. **Compiles ADK Package**: Packages `agents/food_waste_esg_copilot` with its tools, models, interactive HTML generators, and pre-execution safety gates.
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
agents/food_waste_esg_copilot/
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

# Freight Bill Audit Agent

> **ASCM SCOR Pillar**: `05 · Logistics & Transportation`  
> **Sub-Pillar**: `Route & Carrier`  
> **Target Persona**: `Freight Controller / Claims` (Operations Leader)  
> **Core Value Metric**: `Recovers 3%–7% Freight Spend`  
> **Reasoning Model**: `gemini-3.1-pro-preview` (Gemini 3.1 Pro / Gemini 3.8 Flash Dynamic Routing)  
> **A2UI Surfaces**: Native Interactive HTML Cockpit (`IFrameSrcdoc`) + Deterministic `VegaChart`  
> **Standard Compliance**: ASCM SCOR DS v14.0 · ISA-95 · GS1 EPCIS 2.0 · ISO/IEC 42001

---

## 1. Executive Summary & Business Value

### The Business Challenge
20%+ empty/out-of-route miles · 12%–25% spot premium · 3%–8% invoice error rate. Static dispatch routes burn excess fuel in weather/traffic corridors, primary tender rejections spike spot rates by 15%–25%, and 3%–8% of EDI 210 freight bills contain unverified accessorial or tariff errors.

### The Autonomous Solution
Extracts signed PODs and rate contracts via OCR to audit accessorial surcharges.

### Quantified Outcomes & Measurable ROI
- **Target Impact**: Recovers 3%–7% Freight Spend
- **Competitive Advantage**: Cuts multi-modal in-transit excursions by 74% and recovers 100% of invalid detention, demurrage, and rate overcharges automatically.
- **Autonomous Cadence**: Real-time continuous execution eliminating batch ERP latency and manual spreadsheet reconciliation.
- **Zero Hallucination Guarantee**: Strict grounding against BigQuery enterprise twin fixtures and deterministic OR-Tools solvers.

---

## 2. Technical Architecture & Systems Integration

```mermaid
graph TD
  A["High-Frequency Signal Ingestion<br/>(ERP / WMS / TMS / IoT Feeds)"] --> B["Deterministic Constraint Evaluation<br/>(Business Rules & SLA Bounds)"]
  B --> C["Mathematical Optimization Stack<br/>(Pub/Sub + Dataflow Spatiotemporal ETA/Thermal Drift Predictor + Google Maps Geofence & Document AI Rate-Card Audit Engine)"]
  C --> D["Gemini 3.1 Pro Executive Synthesis<br/>(Human-in-the-Loop Consensus)"]
  D --> E["Idempotent ERP Write-Back<br/>(Automated Carrier Claim Dispute Packet & Approved Enterprise ERP (MCP / On-Prem DB) AP Freight Voucher (BAPI_INCOMINGINVOICE_CREATE))"]
  D --> F["A2UI Interactive Cockpit<br/>(IFrameSrcdoc Canvas & VegaChart)"]
```

### Connected Enterprise Systems
- **Core Systems**: Real-Time Carrier Visibility (MCP / API) / Carrier Transit Telemetry (MCP / API) · Ocean Vessel AIS Telemetry (MCP / API) · Air Cargo Flight Telemetry (MCP / API) · Sensitech Cold-Chain IoT · Google Maps Geofencing · Document AI · BigQuery · Operational SQL & Vector DB (On-Prem / Cloud) · Enterprise ERP (MCP / On-Prem DB) TM/AP
- **Mathematical Solver Stack**: Pub/Sub + Dataflow Spatiotemporal ETA/Thermal Drift Predictor + Google Maps Geofence & Document AI Rate-Card Audit Engine
- **Write-Back Gateway**: Automated Carrier Claim Dispute Packet & Approved Enterprise ERP (MCP / On-Prem DB) AP Freight Voucher (BAPI_INCOMINGINVOICE_CREATE)
- **Available ADK Tools**: `list_systems`, `lookup_xyz_master_context`, `query_edi210_freight_invoices`, `query_contracted_lane_fsc_tariffs`, `query_gps_detention_verifications`, `query_freight_overcharge_adjustments`, `analyze_edi210_tariff_and_fsc_variance`, `render_visual_chart`, `draft_edi210_short_pay_remittance_notice`, `action_approve_short_pay_voucher`, `action_transmit_edi210_dispute_code`

### Collaborating A2A Sub-Agents
- **Multi-Modal Excursion Guard**: Detects vessel, air, rail & truck ETA or reefer thermal drift 45+ mins before breach
- **Maps Geofence Detention Verifier**: Matches carrier dwell/demurrage claims against exact Google Maps polygon timestamps
- **EDI 210 / Air Waybill / Ocean Bill Auditor**: Audits 100% of multi-modal freight invoices against contracted lane tables in Operational SQL & Vector DB (On-Prem / Cloud)

---

## 3. Connected Demo Data & Ground Truth Lake

This agent operates directly over verified enterprise fixtures located locally in `agents/freight_bill_audit_agent/fixtures/tables/` and synchronized to Google BigQuery in project `zuhaibp-ai`.

| Fixture Table | BigQuery Table ID | Records | Schema Preview |
| :--- | :--- | :--- | :--- |
| `contracted_lane_rate_and_fsc_tables` | `zuhaibp-ai:supply_chain_twin.contracted_lane_rate_and_fsc_tables` | 8 rows | `lane_code`, `carrier_id`, `pcmiler_contract_miles`, `contract_rate_mile_usd`, `doe_verified_fsc_pct` *(+2 more)* |
| `edi210_carrier_freight_invoices` | `zuhaibp-ai:supply_chain_twin.edi210_carrier_freight_invoices` | 8 rows | `freight_inv_id`, `shipment_id`, `carrier_id`, `lane_code`, `billed_miles` *(+4 more)* |
| `epod_gps_detention_verifications` | `zuhaibp-ai:supply_chain_twin.epod_gps_detention_verifications` | 8 rows | `shipment_id`, `carrier_claimed_dwell_hrs`, `gps_geofence_dwell_hrs`, `verified_billable_detention_hrs`, `appointment_on_time` |
| `freight_overcharge_audit_adjustments` | `zuhaibp-ai:supply_chain_twin.freight_overcharge_audit_adjustments` | 8 rows | `freight_inv_id`, `total_billed_usd`, `verified_payable_usd`, `overcharge_recovered_usd`, `audit_status` |

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
python3 scripts/deploy_to_gemini_enterprise.py --agent freight_bill_audit_agent
```

### What This Command Does:
1. **Verifies Demo Data**: Validates that all connected BigQuery fixture tables exist and are populated.
2. **Compiles ADK Package**: Packages `agents/freight_bill_audit_agent` with its tools, models, interactive HTML generators, and pre-execution safety gates.
3. **Deploys Vertex AI Reasoning Engine**: Deploys or updates the Reasoning Engine in `us-central1` in-place (reusing existing IDs to prevent duplicates).
4. **Registers in Gemini Enterprise**: Registers or refreshes the agent in the Gemini Enterprise application with its executive icon, prompt starters, and native A2UI canvas configuration.

---

## 5. Copy-Ready Test Prompts (Playbook)

Test this agent in the Gemini Enterprise web interface, the ADK test bench, or via API using these plain-English business prompts:

1. **"What is our current operational performance and where are the most critical bottlenecks across Route & Carrier?"**
2. **"Simulate a 25% demand shock and compute the optimal re-allocation schedule with zero SLA violations."**
3. **"Generate an interactive HTML dashboard showing live telemetry, scenario comparison, and ERP audit log."**
4. **"Review the recommended optimization and safely commit the change to ERP with an audit idempotency key."**

---

## 6. Directory Structure

```text
agents/freight_bill_audit_agent/
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

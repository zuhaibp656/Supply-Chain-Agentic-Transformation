# Deployable Supply Chain AI Agents (Argolis & Vertex AI Agent Engine)

This directory serves as the engineering launchpad and decoupled deployment foundation for the **32 Supply Chain & Demand AI Agents** defined in the [Supply Chain Agentic Transformation Blueprint](../SUPPLY_CHAIN_AGENTIC_BLUEPRINT.md).

---

## 1. Architectural Model: Decoupled Agent Topology

```
┌──────────────────────────────────────┐          ┌──────────────────────────────────────┐
│         FRONTEND PRESENTATION        │          │        BACKEND REASONING ENGINE      │
│                                      │  REST    │                                      │
│  • Zipline Web Hosting (go/zipline)  │ ───────▶ │  • Argolis GCP Project Environment   │
│  • 60fps Kinetic SVG/Canvas          │ ◀─────── │  • Vertex AI Agent Engine (ADK)      │
│  • macOS Genie Drill-Downs           │          │  • Cloud Run Containerized Services  │
│  • Interactive 3D CAD Simulators     │          │  • Google OR-Tools Solvers & BigQuery│
└──────────────────────────────────────┘          └──────────────────────────────────────┘
```

1. **Frontend (Zipline / Static / Cloud Run)**:
   - Contains zero hardcoded business logic or API keys.
   - Hosted effortlessly on **Zipline** (`go/zipline`) as a client-side bundle or as a Cloud Run lightweight static web app.
   - Dispatches autonomous customization requests to the backend agent via `POST /api/v1/generate-twin`.

2. **Backend Agent Engine (Argolis GCP / Cloud Run)**:
   - Houses the high-code Python agents, autonomous corporate research scrapers, and deterministic mathematical solvers.
   - Deployable to **Vertex AI Reasoning Engine** (`reasoning_engines.ReasoningEngine.create` / `remote_engine.update`) or containerized on **Cloud Run** in the Argolis environment.

---

## 2. Agent Catalog & Deployment Roadmap

The 32 agents will be progressively implemented, tested locally, and deployed to Argolis:

### Universal Cross-Persona Core (4 Agents)
- `csco_control_tower_copilot`: Looker Semantic Layer + BigQuery / Spanner Graph NL2SQL.
- `disruption_war_room_orchestrator`: WeatherNext 3 probabilistic ensembles + OR-Tools MILP mode rerouter.
- `master_data_leadtime_steward`: Bayesian lead-time estimator + SAP BAPI auto-healer.
- `working_capital_cash_bridge`: Cash-Conversion-Cycle (CCC) DSI/DSO/DPO optimizer.

### Domain-Specific Swarms (28 Agents)
- **01 · Plan (Demand & S&OP)**: `demand_sensing_agent` (TimesFM), `sop_scenario_weaver` (MILP), `promo_lift_simulator` (Double-ML), `cpfr_sync_agent` (EDI 852).
- **02 · Source (Procurement & Risk)**: `rfq_should_cost_agent` (BOM tear-down), `tier_n_risk_sentinel` (Spanner Graph), `tariff_esg_agent` (HS legal RAG), `supplier_quality_sentinel` (8D CAPA).
- **03 · Make (Manufacturing & OEE)**: `line_schedule_optimizer` (CP-SAT), `predictive_oee_sentinel` (PLC FFT vibration), `inline_yield_guardian` (Vision SPC), `eco_cutover_orchestrator` (eBOM burn-down).
- **04 · Fulfill (Inventory & Warehousing)**: `meio_safety_stock_agent` (Guaranteed-Service), `warehouse_slotting_agent` (3D Golden-Zone), `atp_order_promising_agent` (Global ATP), `yard_dock_sequencer` (Hostler routing), `crossdock_transfer_orchestrator` (Flow-through).
- **05 · Deliver (Multi-Modal Logistics)**: `fleetflow_dispatch` (CVRPTW), `load_consolidation_agent` (3D Guillotine LIFO), `freight_control_tower` (Telemetry audit), `port_drayage_orchestrator` (Demurrage), `air_cargo_uld_optimizer` (3D ULD contour), `intermodal_rail_linehaul_agent` (Railinc EDI), `multimodal_mode_shift_agent` (Pareto modal split).
- **06 · Return & Enable (Circular & ESG)**: `otif_penalty_shield` (72-hr MABD rescue), `reverse_rma_optimizer` (Backhaul CVRPTW), `carbon_scope3_ledger` (ISO-14083), `network_twin_architect` (Cost-to-Serve).

---

## 3. Vertex AI Reasoning Engine Deployment Pattern

When deploying to Argolis via Vertex AI Agent Engine, follow the canonical in-place update rule to prevent duplicate endpoints:

```python
import vertexai
from vertexai.preview import reasoning_engines

vertexai.init(project="YOUR_ARGOLIS_PROJECT_ID", location="us-central1")

# In-place deployment / update
remote_agent = reasoning_engines.ReasoningEngine.create(
    reasoning_engines.LangchainAgent(
        model="gemini-2.5-pro",
        tools=[or_tools_solver, sap_bapi_connector, weather_next_sensor],
    ),
    requirements=[
        "google-cloud-aiplatform",
        "ortools",
        "requests",
        "pydantic",
    ],
    display_name="DemandSensingAgent-v1",
    description="Multi-Signal Demand Sensing with TimesFM & WeatherNext 3",
)
```

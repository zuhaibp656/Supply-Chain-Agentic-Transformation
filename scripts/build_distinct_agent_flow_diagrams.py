#!/usr/bin/env python3
"""
Upgrades `renderSimpleAgentArchitectureDiagram(ag, dept)` across `index.html`,
`periodic_table.html`, and `mind_map.html` so that every single one of the 60
Supply Chain AI Agents renders a genuinely distinct, domain-accurate full-canvas
SVG flow diagram that is TECHNOLOGY-FIRST and OPEN to any customer's stack
(BigQuery, On-Premise Databases, 3rd-Party SaaS MCP Servers, REST/EDI Gateways)
rather than locking into specific products like AlloyDB, Spanner, or single-vendor ERPs.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FLOW_CSS = """
    /* =========================================================================
       AGENT-SPECIFIC MEANINGFUL FLOW & ARCHITECTURE DIAGRAM (DARK & LIGHT THEME)
       ========================================================================= */
    .ag-flow-canvas-wrap {
      border-radius: 16px;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      padding: 18px 18px 14px;
      margin-bottom: 16px;
      overflow-x: auto;
    }
    html[data-theme="light"] .ag-flow-canvas-wrap {
      background: #f8fafc;
      border-color: rgba(15, 23, 42, 0.1);
    }

    .ag-flow-svg {
      width: 100%;
      min-width: 960px;
      height: auto;
      display: block;
    }
    .ag-flow-svg .svg-node-box {
      fill: #0f172a;
      transition: fill 0.2s ease, stroke 0.2s ease;
    }
    .ag-flow-svg .svg-node-box-alt {
      fill: #131c31;
    }
    .ag-flow-svg .svg-node-box-out {
      fill: #0d281e;
    }
    .ag-flow-svg .svg-node-box-warn {
      fill: #271a0c;
    }
    .ag-flow-svg .svg-text-main {
      fill: #f8fafc;
      font-family: var(--font-display);
    }
    .ag-flow-svg .svg-text-sub {
      fill: #cbd5e1;
      font-family: var(--font-sans);
    }
    .ag-flow-svg .svg-text-mono {
      fill: #94a3b8;
      font-family: var(--font-mono);
    }
    .ag-flow-svg .svg-pill-bg {
      fill: rgba(15, 23, 42, 0.92);
    }
    .ag-flow-svg .svg-viz-well {
      fill: rgba(2, 6, 23, 0.55);
    }

    html[data-theme="light"] .ag-flow-svg .svg-node-box {
      fill: #ffffff;
    }
    html[data-theme="light"] .ag-flow-svg .svg-node-box-alt {
      fill: #f1f5f9;
    }
    html[data-theme="light"] .ag-flow-svg .svg-node-box-out {
      fill: #ecfdf5;
    }
    html[data-theme="light"] .ag-flow-svg .svg-node-box-warn {
      fill: #fffbeb;
    }
    html[data-theme="light"] .ag-flow-svg .svg-text-main {
      fill: #0f172a;
    }
    html[data-theme="light"] .ag-flow-svg .svg-text-sub {
      fill: #334155;
    }
    html[data-theme="light"] .ag-flow-svg .svg-text-mono {
      fill: #475569;
    }
    html[data-theme="light"] .ag-flow-svg .svg-pill-bg {
      fill: #ffffff;
    }
    html[data-theme="light"] .ag-flow-svg .svg-viz-well {
      fill: rgba(241, 245, 249, 0.9);
    }

    /* 5-Stage Meaningful Step Strip Below the SVG */
    .ag-flow-steps-grid {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 12px;
      margin-top: 12px;
    }
    @media (max-width: 1180px) {
      .ag-flow-steps-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr));
      }
    }
    @media (max-width: 720px) {
      .ag-flow-steps-grid {
        grid-template-columns: 1fr;
      }
    }
    .ag-flow-step-card {
      position: relative;
      padding: 14px 15px;
      border-radius: 14px;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      border-top: 3px solid var(--step-accent, #38bdf8);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 8px;
    }
    .ag-flow-step-head {
      display: flex;
      align-items: center;
      gap: 9px;
    }
    .ag-flow-step-icon {
      width: 34px;
      height: 34px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 17px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      flex-shrink: 0;
    }
    .ag-flow-step-kicker {
      font-family: var(--font-mono);
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--step-accent, #38bdf8);
    }
    .ag-flow-step-title {
      font-family: var(--font-display);
      font-size: 13.5px;
      font-weight: 800;
      color: var(--text-primary);
      line-height: 1.25;
    }
    .ag-flow-step-desc {
      font-size: 12px;
      color: var(--text-secondary);
      line-height: 1.45;
      margin: 0;
    }
    .ag-flow-step-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      padding-top: 6px;
      border-top: 1px dashed var(--border-subtle);
    }
    .ag-flow-mini-chip {
      font-family: var(--font-mono);
      font-size: 10.5px;
      font-weight: 600;
      padding: 2px 6px;
      border-radius: 5px;
      background: var(--bg-surface);
      color: var(--text-primary);
      border: 1px solid var(--border-subtle);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%;
    }
"""

NEW_ARCH_DIAGRAM_JS = r"""
    /* =========================================================================
       AGENT-SPECIFIC MEANINGFUL FLOW & ARCHITECTURE DIAGRAM
       (OPEN, TECHNOLOGY-FIRST & CUSTOMER-AGNOSTIC: BIGQUERY, ON-PREM DBs, 3RD-PARTY MCPs)
       ========================================================================= */
    const AGENT_TOPOLOGY_MAP = {
      // 1. Probabilistic Multi-Signal Sensing & Forecast Fan
      demand_sensing_agent: 'sensing_fan',
      npi_demand_profiler: 'sensing_fan',
      cpfr_sync_agent: 'sensing_fan',
      geocoding_intelligence_agent: 'sensing_fan',

      // 2. Price / Promo Elasticity & Counterfactual Revenue Curve
      promo_lift_simulator: 'elasticity_curve',
      dynamic_markdown_agent: 'elasticity_curve',
      trade_scheme_claims_reconciler: 'elasticity_curve',
      short_dated_redistributor: 'elasticity_curve',

      // 3. Closed-Loop MILP Optimization & Pareto Trade-Off Solver
      sop_scenario_weaver: 'milp_pareto_loop',
      sku_rationalization_agent: 'milp_pareto_loop',
      capex_simulator_agent: 'milp_pareto_loop',
      finite_production_scheduler: 'milp_pareto_loop',
      line_schedule_optimizer: 'milp_pareto_loop',
      labor_line_balancing_agent: 'milp_pareto_loop',
      copacker_allocation_agent: 'milp_pareto_loop',
      echelon_inventory_allocator: 'milp_pareto_loop',
      meio_safety_stock_agent: 'milp_pareto_loop',
      network_twin_architect: 'milp_pareto_loop',
      working_capital_cash_bridge: 'milp_pareto_loop',

      // 4. Multi-Hop Graph Traversal & Semantic Contract / Invoice Audit
      tier_n_risk_sentinel: 'graph_contract_audit',
      rfq_should_cost_agent: 'graph_contract_audit',
      commodity_index_advisor: 'graph_contract_audit',
      tariff_esg_agent: 'graph_contract_audit',
      sustainable_packaging_agent: 'graph_contract_audit',
      three_way_match_dispute: 'graph_contract_audit',
      freight_bill_audit_agent: 'graph_contract_audit',
      carbon_scope3_ledger: 'graph_contract_audit',
      food_waste_esg_copilot: 'graph_contract_audit',
      master_data_leadtime_steward: 'graph_contract_audit',

      // 5. Edge Multimodal Computer Vision, IoT Spectrogram & Line Actuator
      plant_oee_maintenance_agent: 'edge_vision_iot',
      predictive_oee_sentinel: 'edge_vision_iot',
      scrap_defect_root_cause_agent: 'edge_vision_iot',
      inline_quality_inspection_agent: 'edge_vision_iot',
      inline_yield_guardian: 'edge_vision_iot',
      batch_record_auditor: 'edge_vision_iot',
      supplier_quality_sentinel: 'edge_vision_iot',
      cold_chain_auditor: 'edge_vision_iot',
      planogram_merchandising_vision_auditor: 'edge_vision_iot',
      sanitation_health_agent: 'edge_vision_iot',
      eco_cutover_orchestrator: 'edge_vision_iot',

      // 6. Spatial 3D Warehouse, Yard Geofence & Low-Latency ATP Reservation
      warehouse_slotting_optimizer: 'spatial_wms_atp',
      warehouse_slotting_agent: 'spatial_wms_atp',
      dynamic_order_promising_atp: 'spatial_wms_atp',
      atp_order_promising_agent: 'spatial_wms_atp',
      crossdock_transfer_orchestrator: 'spatial_wms_atp',
      yard_dock_scheduling_agent: 'spatial_wms_atp',
      yard_dock_sequencer: 'spatial_wms_atp',
      dock_to_stock_agent: 'spatial_wms_atp',
      wave_fulfillment_copilot: 'spatial_wms_atp',
      slob_disposition_agent: 'spatial_wms_atp',
      aisle_aligned_pallet_agent: 'spatial_wms_atp',
      store_capacity_agent: 'spatial_wms_atp',
      rti_balance_reconciler: 'spatial_wms_atp',

      // 7. Multi-Modal Global Corridor, Fleet VRP & 3D Load Studio
      fleetflow_dispatch: 'multimodal_corridor_vrp',
      load_consolidation_agent: 'multimodal_corridor_vrp',
      port_drayage_orchestrator: 'multimodal_corridor_vrp',
      air_cargo_uld_optimizer: 'multimodal_corridor_vrp',
      intermodal_rail_linehaul_agent: 'multimodal_corridor_vrp',
      multimodal_mode_shift_agent: 'multimodal_corridor_vrp',
      freight_control_tower: 'multimodal_corridor_vrp',
      field_beat_distributor_sync_agent: 'multimodal_corridor_vrp',

      // 8. Circular Return Triage, OTIF Shield & War-Room Orchestration
      reverse_rma_optimizer: 'circular_warroom_triage',
      keep_it_routing_advisor: 'circular_warroom_triage',
      returns_triage_agent: 'circular_warroom_triage',
      osd_freight_claims_agent: 'circular_warroom_triage',
      otif_penalty_shield: 'circular_warroom_triage',
      csco_control_tower_copilot: 'circular_warroom_triage',
      disruption_war_room_orchestrator: 'circular_warroom_triage'
    };

    const TOPOLOGY_META = {
      sensing_fan: {
        badge: 'Probabilistic Multi-Signal Sensing & Quantile Forecast Architecture',
        icons: ['📡', '🗄️', '📈', '🛡️', '🎯'],
        stageLabels: ['1 · Multi-Signal Feeds', '2 · Censorship Imputation', '3 · Quantile Forecast Fan', '4 · Bias Filter Gate', '5 · Planning System Commit']
      },
      elasticity_curve: {
        badge: 'Counterfactual Price/Promo Elasticity & Margin Waterfall Architecture',
        icons: ['🏷️', '📊', '🧮', '⚖️', '💰'],
        stageLabels: ['1 · Price & Shelf Matrix', '2 · Baseline Decomposer', '3 · Bayesian Uplift Curve', '4 · Breakeven ROI Gate', '5 · Pricing / ERP Commit']
      },
      milp_pareto_loop: {
        badge: 'Bidirectional Constraint & Mathematical Optimization Loop Architecture',
        icons: ['📥', '🔗', '⚙️', '🛡️', '🚀'],
        stageLabels: ['1 · Dual Constraint Feeds', '2 · LP Constraint Matrix', '3 · Iterative MILP Solver', '4 · Feasibility Gate', '5 · Signed Plan Commit']
      },
      graph_contract_audit: {
        badge: 'Multi-Hop Supply Graph & Semantic Document/Invoice Audit Architecture',
        icons: ['📄', '🕸️', '🔍', '🔒', '✅'],
        stageLabels: ['1 · Docs & Tier-N Feeds', '2 · Graph & Vector Index', '3 · Clause & Rate Auditor', '4 · Compliance Hold Gate', '5 · ERP Block / Award']
      },
      edge_vision_iot: {
        badge: 'Industrial Edge Computer Vision, FFT Telemetry & Line Actuator Architecture',
        icons: ['📷', '⚡', '🔬', '🚨', '🔧'],
        stageLabels: ['1 · Edge Camera & PLC IoT', '2 · Stream Normalizer', '3 · Vision & FFT Classifier', '4 · Safety & QA Interlock', '5 · PLC & MES Actuator']
      },
      spatial_wms_atp: {
        badge: 'Spatial 3D Warehouse Rack, Yard Geofence & Real-Time ATP Architecture',
        icons: ['🛒', '📐', '📦', '🚦', '🏢'],
        stageLabels: ['1 · Live Orders & Yard GPS', '2 · Low-Latency State DB', '3 · 3D Spatial & Wave Solver', '4 · Quota & Congestion Gate', '5 · WMS / OMS Execution']
      },
      multimodal_corridor_vrp: {
        badge: '4-Mode Global Corridor, Geospatial VRP & 3D LIFO Load Architecture',
        icons: ['🚢', '🗺️', '🚚', '🛣️', '📍'],
        stageLabels: ['1 · Ocean/Air/Rail/Road Feeds', '2 · Corridor Digital Twin', '3 · VRP + 3D Axle Solver', '4 · DOT & HOS Safety Gate', '5 · Carrier & TMS Dispatch']
      },
      circular_warroom_triage: {
        badge: '3-Branch Exception Triage, OTIF Shield & Executive War-Room Architecture',
        icons: ['🚨', '🧭', '🔀', '🛡️', '⚡'],
        stageLabels: ['1 · Disruption / RMA Alert', '2 · Cross-System Evidence', '3 · 3-Branch Triage Tree', '4 · Financial Authority Gate', '5 · Auto Claim / Re-Route']
      }
    };

    /* Maps product-specific vendor strings to open, customer-agnostic technology descriptions */
    function toOpenTechLabel(rawStr) {
      if (!rawStr) return 'Enterprise System (MCP / API / On-Prem DB)';
      let s = String(rawStr).trim();
      const replacements = [
        [/AlloyDB\s*pgvector/gi, 'Vector Search Index (DB / MCP)'],
        [/AlloyDB/gi, 'Operational SQL / Vector DB'],
        [/Cloud\s*Spanner\s*Graph/gi, 'Multi-Hop Graph DB (Cloud / On-Prem)'],
        [/Cloud\s*Spanner/gi, 'Distributed Transactional DB'],
        [/Spanner/gi, 'Low-Latency State DB'],
        [/Google\s*WeatherNext\s*3/gi, 'Weather & Climate Telemetry API'],
        [/WeatherNext\s*3/gi, 'Weather Ensemble Feed'],
        [/Google\s*Earth\s*Engine/gi, 'Satellite & Geospatial Imagery API'],
        [/Google\s*Maps\s*Routes\s*Preferred\s*API/gi, 'Geospatial Routing & Traffic API'],
        [/Google\s*Maps\s*Routes\s*API/gi, 'Geospatial Routing & Traffic API'],
        [/Google\s*Maps\s*Fleet\s*Engine/gi, 'Fleet & Yard Geofencing API'],
        [/Google\s*Maps\s*Places/gi, 'Geospatial & POI Intelligence API'],
        [/Google\s*Maps\s*Platform/gi, 'Geospatial Routing & ETA API'],
        [/Vertex\s*AI\s*TimesFM\s*Foundation\s*Model/gi, 'Time-Series Forecasting Foundation Model'],
        [/Vertex\s*AI\s*TimesFM/gi, 'Time-Series Forecasting Model'],
        [/TimesFM\s*2\.5/gi, 'Time-Series Forecasting Model'],
        [/TimesFM/gi, 'Time-Series Forecasting Model'],
        [/Google\s*OR-Tools/gi, 'Mathematical Optimization Solver (MILP / CP-SAT)'],
        [/OR-Tools/gi, 'Constraint Optimization Solver (MILP)'],
        [/SAP\s*IBP\s*&\s*S\/4HANA/gi, 'Enterprise ERP & Supply Planning (MCP / On-Prem)'],
        [/SAP\s*IBP/gi, 'Supply Planning System (MCP / API)'],
        [/SAP\s*S\/4HANA\s*PP\/DS/gi, 'Production Planning & ERP (MCP / On-Prem)'],
        [/SAP\s*S\/4HANA\s*SD\/FI/gi, 'ERP Order & Finance Ledger (MCP / On-Prem)'],
        [/SAP\s*S\/4HANA/gi, 'Enterprise ERP (MCP / On-Prem DB)'],
        [/SAP\s*EWM/gi, 'Warehouse Management System (WMS / MCP)'],
        [/SAP\s*QM/gi, 'Quality Management System (QMS / ERP)'],
        [/SAP\s*PM/gi, 'Plant Maintenance System (EAM / ERP)'],
        [/SAP\s*TM/gi, 'Transportation Management System (TMS)'],
        [/SAP\s*GTS/gi, 'Global Trade & Tariff System (MCP / API)'],
        [/SAP\s*TPM/gi, 'Trade Promotion Management (TPM / CRM)'],
        [/SAP\s*Ariba/gi, 'e-Procurement & Sourcing Portal (MCP / API)'],
        [/Kinaxis\s*RapidResponse/gi, 'Concurrent Supply Planning Engine (MCP / API)'],
        [/Kinaxis/gi, 'Supply Planning Platform (MCP / API)'],
        [/Manhattan\s*Active\s*WMS/gi, 'Warehouse Management System (WMS / API)'],
        [/Blue\s*Yonder\s*TMS/gi, 'Transportation Management System (TMS / API)'],
        [/Blue\s*Yonder/gi, 'Supply Chain Execution System (MCP / API)'],
        [/Oracle\s*OTM/gi, 'Transportation Management System (TMS / API)'],
        [/Salesforce\s*Consumer\s*Goods\s*Cloud/gi, 'Commercial CRM & Trade Portal (MCP / API)'],
        [/Walmart\s*Luminate\s*·\s*Target\s*Greenfield\s*·\s*Amazon\s*Vendor\s*Central/gi, 'Retail Customer POS & Vendor Portals (EDI / MCP)'],
        [/Walmart\s*Luminate/gi, 'Retail Customer POS Portal (EDI / MCP)'],
        [/Target\s*Greenfield/gi, 'Retail Partner Analytics (MCP / EDI)'],
        [/Amazon\s*Vendor\s*Central/gi, 'e-Commerce Vendor Portal (API / EDI)'],
        [/Spire\s*Ocean\s*AIS/gi, 'Ocean Vessel AIS Telemetry (API / MCP)'],
        [/FlightAware\s*ADS-B/gi, 'Air Cargo Flight Telemetry (API / MCP)'],
        [/Project44/gi, 'Real-Time Carrier Visibility (MCP / API)'],
        [/FourKites/gi, 'Carrier Transit Telemetry (MCP / API)'],
        [/Apigee\s*APIs/gi, 'Enterprise API & MCP Gateway'],
        [/via\s*Apigee/gi, 'via MCP / REST / On-Prem Gateway'],
        [/Apigee/gi, 'MCP / REST API Gateway']
      ];
      for (const [regex, rep] of replacements) {
        s = s.replace(regex, rep);
      }
      return s;
    }

    function pickSystemIcon(sysName) {
      const s = String(sysName || '').toLowerCase();
      if (s.includes('weather') || s.includes('climate') || s.includes('satellite')) return '🌦️';
      if (s.includes('geospatial') || s.includes('routing') || s.includes('gps') || s.includes('fleet') || s.includes('traffic')) return '🗺️';
      if (s.includes('pos') || s.includes('edi 852') || s.includes('retail') || s.includes('syndicated') || s.includes('vendor')) return '🛒';
      if (s.includes('vision') || s.includes('camera') || s.includes('optical')) return '📷';
      if (s.includes('plc') || s.includes('opc') || s.includes('scada') || s.includes('mqtt') || s.includes('vibration') || s.includes('iot')) return '📳';
      if (s.includes('ais') || s.includes('ocean') || s.includes('port') || s.includes('vessel')) return '🚢';
      if (s.includes('air') || s.includes('iata') || s.includes('flight') || s.includes('uld')) return '✈️';
      if (s.includes('rail') || s.includes('intermodal')) return '🚆';
      if (s.includes('wms') || s.includes('warehouse') || s.includes('yard')) return '🏢';
      if (s.includes('tms') || s.includes('carrier') || s.includes('freight') || s.includes('transportation')) return '🚚';
      if (s.includes('procurement') || s.includes('sourcing') || s.includes('supplier') || s.includes('contract')) return '🤝';
      if (s.includes('graph')) return '🕸️';
      if (s.includes('vector') || s.includes('semantic')) return '🔍';
      if (s.includes('forecast') || s.includes('time-series') || s.includes('vertex')) return '🧠';
      if (s.includes('bigquery') || s.includes('warehouse') || s.includes('sql')) return '🗄️';
      if (s.includes('erp') || s.includes('planning') || s.includes('finance')) return '🏦';
      return '🔌';
    }

    function renderFullTopologySvg(topology, ctx) {
      const {
        ag, dept, cls, cleanName, trunc,
        sys1, sys2, sys3, ic1, ic2, ic3,
        tbl1, tbl2, tbl3, tablesCount,
        q1, q2, a1, subs, solverLabel, writebackLabel
      } = ctx;

      const uid = ag.id;

      // =====================================================================
      // TOPOLOGY 1: PROBABILISTIC MULTI-SIGNAL SENSING & QUANTILE FAN CONE
      // =====================================================================
      if (topology === 'sensing_fan') {
        return `
          <!-- Fan-In Signal Streams -> Imputation Hub -->
          <path d="M 192 56 C 212 56, 212 126, 232 126" fill="none" stroke="${dept.color}" stroke-width="2" stroke-dasharray="5 3" />
          <path d="M 192 165 L 232 165" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="5 3" />
          <path d="M 192 274 C 212 274, 212 204, 232 204" fill="none" stroke="#f59e0b" stroke-width="2" stroke-dasharray="5 3" />
          <circle r="3.5" fill="${dept.color}"><animateMotion dur="1.8s" repeatCount="indefinite" path="M 192 56 C 212 56, 212 126, 232 126" /></circle>
          <circle r="3.5" fill="#38bdf8"><animateMotion dur="1.5s" repeatCount="indefinite" path="M 192 165 L 232 165" /></circle>
          <circle r="3.5" fill="#f59e0b"><animateMotion dur="2.1s" repeatCount="indefinite" path="M 192 274 C 212 274, 212 204, 232 204" /></circle>

          <!-- Imputation Hub -> Wide Quantile Fan Canvas -->
          <path d="M 412 165 L 444 165" fill="none" stroke="#38bdf8" stroke-width="2.5" marker-end="url(#arrowCyan_${uid})" />

          <!-- Quantile Fan Canvas -> FVA Bias Filter Gate -->
          <path d="M 704 125 L 736 125" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4 2" />
          <path d="M 704 165 L 736 165" fill="none" stroke="${dept.color}" stroke-width="2.5" marker-end="url(#arrowAccent_${uid})" />
          <path d="M 704 205 L 736 205" fill="none" stroke="#f59e0b" stroke-width="2" stroke-dasharray="4 2" />

          <!-- FVA Gate -> Planning System Write-Back & A2UI Fan -->
          <path d="M 896 135 C 912 135, 912 96, 928 96" fill="none" stroke="#10b981" stroke-width="2.4" marker-end="url(#arrowGreen_${uid})" />
          <path d="M 896 195 C 912 195, 912 234, 928 234" fill="none" stroke="#38bdf8" stroke-width="2.2" marker-end="url(#arrowCyan_${uid})" />

          <!-- 3 Left Multi-Signal Stream Nodes (Open MCP / BigQuery / On-Prem) -->
          <g transform="translate(12, 18)">
            <rect class="svg-node-box" width="180" height="76" rx="12" stroke="${dept.color}" stroke-width="1.8" />
            <text x="14" y="25" font-size="16">${ic1}</text>
            <text x="36" y="23" fill="${dept.color}" font-size="9" font-weight="800" font-family="var(--font-mono)">MCP / ON-PREM / API 01</text>
            <text x="14" y="45" class="svg-text-main" font-size="12" font-weight="800">${trunc(sys1, 20)}</text>
            <text x="14" y="62" class="svg-text-mono" font-size="9.5">↳ ${trunc(tbl1, 21)}</text>
          </g>
          <g transform="translate(12, 127)">
            <rect class="svg-node-box" width="180" height="76" rx="12" stroke="#38bdf8" stroke-width="1.8" />
            <text x="14" y="25" font-size="16">${ic2}</text>
            <text x="36" y="23" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">BIGQUERY / DW / FEED 02</text>
            <text x="14" y="45" class="svg-text-main" font-size="12" font-weight="800">${trunc(sys2, 20)}</text>
            <text x="14" y="62" class="svg-text-mono" font-size="9.5">↳ ${trunc(tbl2, 21)}</text>
          </g>
          <g transform="translate(12, 236)">
            <rect class="svg-node-box" width="180" height="76" rx="12" stroke="#f59e0b" stroke-width="1.8" />
            <text x="14" y="25" font-size="16">${ic3}</text>
            <text x="36" y="23" fill="#f59e0b" font-size="9" font-weight="800" font-family="var(--font-mono)">3RD-PARTY MCP / EDI 03</text>
            <text x="14" y="45" class="svg-text-main" font-size="12" font-weight="800">${trunc(sys3, 20)}</text>
            <text x="14" y="62" class="svg-text-mono" font-size="9.5">↳ ${trunc(tbl3, 21)}</text>
          </g>

          <!-- Stage 2: Censorship & Stockout Imputation Hub (Sub-Agent 1) -->
          <g transform="translate(232, 62)">
            <rect class="svg-node-box-alt" width="180" height="206" rx="14" stroke="#38bdf8" stroke-width="2" />
            <text x="14" y="25" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🗄️ BQ / SQL / MCP GROUNDING</text>
            <text x="14" y="45" class="svg-text-main" font-size="12.5" font-weight="800">${trunc(subs[0].name, 21)}</text>
            <text x="14" y="62" class="svg-text-sub" font-size="10">${trunc(subs[0].role, 25)}</text>
            <rect class="svg-pill-bg" x="10" y="76" width="160" height="38" rx="7" stroke="rgba(56,189,248,0.4)" />
            <text x="16" y="92" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🔍 ${trunc(q1, 21)}</text>
            <text x="16" y="106" class="svg-text-mono" font-size="9">Uncensors OOS Zero-Scans</text>
            <rect class="svg-pill-bg" x="10" y="122" width="160" height="38" rx="7" stroke="rgba(56,189,248,0.4)" />
            <text x="16" y="138" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🔍 ${trunc(q2, 21)}</text>
            <text x="16" y="152" class="svg-text-mono" font-size="9">${tablesCount} BigQuery / SQL Tables</text>
            <text x="14" y="186" fill="#10b981" font-size="9.5" font-weight="800" font-family="var(--font-mono)">✓ Pluggable DB / MCP Layer</text>
          </g>

          <!-- Stage 3: Wide Probabilistic Quantile Fan Canvas (Sub-Agent 2) -->
          <g transform="translate(444, 24)">
            <rect class="svg-node-box-alt" width="260" height="282" rx="16" stroke="${cls.color}" stroke-width="2.4" />
            <rect x="14" y="12" width="232" height="22" rx="6" fill="${cls.color}26" stroke="${cls.color}" />
            <text x="130" y="27" text-anchor="middle" class="svg-text-main" font-size="9.5" font-weight="800" font-family="var(--font-mono)">📈 TIME-SERIES QUANTILE ENGINE</text>
            <text x="16" y="54" class="svg-text-main" font-size="13.5" font-weight="800">${trunc(subs[1].name, 28)}</text>
            <text x="16" y="71" fill="${cls.color}" font-size="10.5" font-weight="700">${trunc(solverLabel, 33)}</text>

            <!-- Large Interactive-Looking SVG P10/P50/P90 Forecast Fan Cone -->
            <g transform="translate(16, 84)">
              <rect class="svg-viz-well" width="228" height="126" rx="10" stroke="${dept.color}66" stroke-width="1.2" />
              <line x1="14" y1="32" x2="214" y2="32" stroke="rgba(148,163,184,0.18)" stroke-dasharray="2 2" />
              <line x1="14" y1="64" x2="214" y2="64" stroke="rgba(148,163,184,0.18)" stroke-dasharray="2 2" />
              <line x1="14" y1="96" x2="214" y2="96" stroke="rgba(148,163,184,0.18)" stroke-dasharray="2 2" />
              <path d="M 92 68 C 130 52, 170 28, 210 16 L 210 108 C 170 96, 130 82, 92 68 Z" fill="${dept.color}38" />
              <path d="M 16 86 Q 42 74, 66 78 T 92 68" fill="none" stroke="#94a3b8" stroke-width="2.2" />
              <path d="M 92 68 C 130 52, 170 28, 210 16" fill="none" stroke="#38bdf8" stroke-width="1.8" stroke-dasharray="4 2" />
              <path d="M 92 68 C 132 62, 172 56, 210 52" fill="none" stroke="${dept.color}" stroke-width="2.6" />
              <path d="M 92 68 C 130 82, 170 96, 210 108" fill="none" stroke="#fbbf24" stroke-width="1.8" stroke-dasharray="4 2" />
              <circle cx="92" cy="68" r="4.5" fill="#ffffff" stroke="${dept.color}" stroke-width="2" />
              <text x="164" y="15" fill="#38bdf8" font-size="8.5" font-weight="800" font-family="var(--font-mono)">P90 UPPER</text>
              <text x="164" y="47" fill="${dept.color}" font-size="8.5" font-weight="800" font-family="var(--font-mono)">P50 MEDIAN</text>
              <text x="164" y="118" fill="#fbbf24" font-size="8.5" font-weight="800" font-family="var(--font-mono)">P10 LOWER</text>
              <text x="14" y="20" class="svg-text-mono" font-size="8.5">ACTUALS</text>
            </g>

            <text x="16" y="232" class="svg-text-mono" font-size="9.5">• Orchestrator: Gemini 3.8 Flash ↔ 3.1 Pro/Argon</text>
            <text x="16" y="249" class="svg-text-mono" font-size="9.5">• Horizon: Multi-Week SKU×Location Quantiles</text>
            <text x="16" y="266" fill="#10b981" font-size="9.5" font-weight="700" font-family="var(--font-mono)">✓ Dynamic Uncertainty Bounds Emitted</text>
          </g>

          <!-- Stage 4: FVA & Bias Filter Gate (Sub-Agent 3) -->
          <g transform="translate(736, 62)">
            <rect class="svg-node-box-warn" width="160" height="206" rx="14" stroke="#f59e0b" stroke-width="2" />
            <polygon points="80,16 96,32 80,48 64,32" fill="rgba(245,158,11,0.22)" stroke="#f59e0b" stroke-width="1.6" />
            <text x="80" y="36" text-anchor="middle" font-size="12">🛡️</text>
            <text x="80" y="66" text-anchor="middle" fill="#f59e0b" font-size="9.5" font-weight="800" font-family="var(--font-mono)">FVA BIAS FILTER GATE</text>
            <text x="80" y="86" text-anchor="middle" class="svg-text-main" font-size="11.5" font-weight="800">${trunc(subs[2].name, 19)}</text>
            <rect class="svg-pill-bg" x="12" y="100" width="136" height="44" rx="7" stroke="#f59e0b66" />
            <text x="80" y="118" text-anchor="middle" fill="#fbbf24" font-size="9" font-weight="800" font-family="var(--font-mono)">Suppresses Negative</text>
            <text x="80" y="133" text-anchor="middle" class="svg-text-mono" font-size="9">FVA Manual Overrides</text>
            <text x="80" y="166" text-anchor="middle" class="svg-text-mono" font-size="9">enforce_tool_contract()</text>
            <text x="80" y="186" text-anchor="middle" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">✓ Zero-Bias Verified</text>
          </g>

          <!-- Stage 5: Open MCP / API / On-Prem Write-Back & A2UI Fan -->
          <g transform="translate(928, 38)">
            <rect class="svg-node-box-out" width="180" height="114" rx="14" stroke="#10b981" stroke-width="2" />
            <text x="14" y="24" font-size="15">🎯</text>
            <text x="36" y="22" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">MCP / API / ERP COMMIT</text>
            <text x="14" y="42" class="svg-text-main" font-size="11.5" font-weight="800">${writebackLabel}</text>
            <rect class="svg-pill-bg" x="10" y="52" width="160" height="24" rx="5" stroke="#10b98166" />
            <text x="16" y="68" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">⚡ ${trunc(a1, 21)}</text>
            <text x="14" y="96" class="svg-text-mono" font-size="9">REST / MCP / On-Prem DB</text>
          </g>
          <g transform="translate(928, 176)">
            <rect class="svg-node-box" width="180" height="114" rx="14" stroke="#38bdf8" stroke-width="2" />
            <text x="14" y="24" font-size="15">📊</text>
            <text x="36" y="22" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">A2UI FAN SURFACE</text>
            <text x="14" y="42" class="svg-text-main" font-size="11.5" font-weight="800">${trunc(ag.badge || ag.outcome, 22)}</text>
            <rect class="svg-pill-bg" x="10" y="52" width="160" height="24" rx="5" stroke="#38bdf866" />
            <text x="16" y="68" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">✦ Quantile VegaChart</text>
            <text x="14" y="96" class="svg-text-sub" font-size="9.5">${trunc(ag.primaryPersonaName || 'Demand Lead', 22)}</text>
          </g>
        `;
      }

      // =====================================================================
      // TOPOLOGY 2: PRICE / PROMO ELASTICITY & MARGIN WATERFALL SIMULATOR
      // =====================================================================
      if (topology === 'elasticity_curve') {
        return `
          <!-- Dual Commercial & Inventory Inputs -> Baseline Decomposer -->
          <path d="M 196 92 C 214 92, 214 134, 232 134" fill="none" stroke="${dept.color}" stroke-width="2.2" stroke-dasharray="5 3" />
          <path d="M 196 238 C 214 238, 214 196, 232 196" fill="none" stroke="#10b981" stroke-width="2.2" stroke-dasharray="5 3" />
          <circle r="3.5" fill="${dept.color}"><animateMotion dur="1.7s" repeatCount="indefinite" path="M 196 92 C 214 92, 214 134, 232 134" /></circle>
          <circle r="3.5" fill="#10b981"><animateMotion dur="2.0s" repeatCount="indefinite" path="M 196 238 C 214 238, 214 196, 232 196" /></circle>

          <!-- Decomposer -> Counterfactual Elasticity & Waterfall Simulator -->
          <path d="M 412 165 L 444 165" fill="none" stroke="#10b981" stroke-width="2.5" marker-end="url(#arrowGreen_${uid})" />

          <!-- Simulator -> Breakeven ROI Diamond Gate -->
          <path d="M 704 165 L 736 165" fill="none" stroke="#fbbf24" stroke-width="2.5" marker-end="url(#arrowAccent_${uid})" />

          <!-- Rejected Counterfactual Loopback -->
          <path d="M 816 266 C 720 312, 610 312, 560 286" fill="none" stroke="#f43f5e" stroke-width="1.6" stroke-dasharray="4 3" />
          <text x="688" y="314" text-anchor="middle" fill="#fb7185" font-size="9" font-weight="800" font-family="var(--font-mono)">↺ Rejects Margin-Dilutive Depth &amp; Re-Optimizes Price Point</text>

          <!-- ROI Gate -> Approved Price/Trade Commit -->
          <path d="M 896 135 C 912 135, 912 96, 928 96" fill="none" stroke="#10b981" stroke-width="2.4" marker-end="url(#arrowGreen_${uid})" />
          <path d="M 896 195 C 912 195, 912 234, 928 234" fill="none" stroke="#38bdf8" stroke-width="2.2" marker-end="url(#arrowCyan_${uid})" />

          <!-- Left Top: Price, Promo & Trade Calendar Input (MCP / BigQuery / On-Prem) -->
          <g transform="translate(12, 34)">
            <rect class="svg-node-box" width="184" height="116" rx="14" stroke="${dept.color}" stroke-width="2" />
            <text x="14" y="26" font-size="17">🏷️</text>
            <text x="38" y="24" fill="${dept.color}" font-size="9" font-weight="800" font-family="var(--font-mono)">PRICING &amp; CRM (MCP / DB)</text>
            <text x="14" y="46" class="svg-text-main" font-size="12.5" font-weight="800">${trunc(sys1, 21)}</text>
            <text x="14" y="64" class="svg-text-mono" font-size="9.5">Table: ${trunc(tbl1, 20)}</text>
            <rect class="svg-pill-bg" x="12" y="76" width="160" height="26" rx="6" stroke="${dept.color}55" />
            <text x="18" y="93" fill="${dept.color}" font-size="9" font-weight="800" font-family="var(--font-mono)">🔍 ${trunc(q1, 20)}</text>
          </g>

          <!-- Left Bottom: Shelf Life, Lot Stock & POS Ledger -->
          <g transform="translate(12, 178)">
            <rect class="svg-node-box" width="184" height="116" rx="14" stroke="#10b981" stroke-width="2" />
            <text x="14" y="26" font-size="17">${ic2}</text>
            <text x="38" y="24" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">BIGQUERY / ON-PREM STOCK</text>
            <text x="14" y="46" class="svg-text-main" font-size="12.5" font-weight="800">${trunc(sys2, 21)}</text>
            <text x="14" y="64" class="svg-text-mono" font-size="9.5">Table: ${trunc(tbl2, 20)}</text>
            <rect class="svg-pill-bg" x="12" y="76" width="160" height="26" rx="6" stroke="#10b98155" />
            <text x="18" y="93" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">🔍 ${trunc(q2, 20)}</text>
          </g>

          <!-- Stage 2: Baseline & Cannibalization Decomposer (Sub-Agent 1) -->
          <g transform="translate(232, 54)">
            <rect class="svg-node-box-alt" width="180" height="222" rx="14" stroke="#38bdf8" stroke-width="2" />
            <text x="14" y="26" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">📊 BASELINE DECOMPOSER</text>
            <text x="14" y="46" class="svg-text-main" font-size="12.5" font-weight="800">${trunc(subs[0].name, 21)}</text>
            <text x="14" y="64" class="svg-text-sub" font-size="10">${trunc(subs[0].role, 25)}</text>
            <rect class="svg-pill-bg" x="12" y="80" width="156" height="36" rx="6" stroke="rgba(56,189,248,0.4)" />
            <text x="18" y="96" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">1. Strip Organic Trend</text>
            <text x="18" y="109" class="svg-text-mono" font-size="8.5">Seasonality + Macro Index</text>
            <rect class="svg-pill-bg" x="12" y="124" width="156" height="36" rx="6" stroke="rgba(244,63,94,0.4)" />
            <text x="18" y="140" fill="#fb7185" font-size="9" font-weight="800" font-family="var(--font-mono)">2. Cross-SKU Drag Matrix</text>
            <text x="18" y="153" class="svg-text-mono" font-size="8.5">Cannibalization &amp; Pull-Forward</text>
            <text x="14" y="186" class="svg-text-mono" font-size="9.5">Audit: ${trunc(tbl3, 19)}</text>
            <text x="14" y="204" fill="#10b981" font-size="9.5" font-weight="800" font-family="var(--font-mono)">✓ Net Incremental Matrix</text>
          </g>

          <!-- Stage 3: Bayesian Elasticity Curve & Margin Waterfall (Sub-Agent 2) -->
          <g transform="translate(444, 24)">
            <rect class="svg-node-box-alt" width="260" height="262" rx="16" stroke="#10b981" stroke-width="2.4" />
            <rect x="14" y="12" width="232" height="22" rx="6" fill="rgba(16,185,129,0.18)" stroke="#10b981" />
            <text x="130" y="27" text-anchor="middle" class="svg-text-main" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🧮 ELASTICITY &amp; MARGIN WATERFALL</text>
            <text x="16" y="54" class="svg-text-main" font-size="13.5" font-weight="800">${trunc(subs[1].name, 28)}</text>
            <text x="16" y="71" fill="#10b981" font-size="10.5" font-weight="700">${trunc(solverLabel, 33)}</text>

            <g transform="translate(16, 84)">
              <rect class="svg-viz-well" width="228" height="118" rx="10" stroke="#10b98166" stroke-width="1.2" />
              <rect x="20" y="48" width="22" height="52" rx="3" fill="#38bdf8" />
              <rect x="52" y="22" width="22" height="36" rx="3" fill="#10b981" />
              <rect x="84" y="34" width="22" height="28" rx="3" fill="#f43f5e" />
              <rect x="116" y="28" width="22" height="72" rx="3" fill="#fbbf24" />
              <text x="31" y="111" text-anchor="middle" class="svg-text-mono" font-size="8">BASE</text>
              <text x="63" y="111" text-anchor="middle" fill="#10b981" font-size="8" font-weight="800">+LIFT</text>
              <text x="95" y="111" text-anchor="middle" fill="#fb7185" font-size="8" font-weight="800">-DRAG</text>
              <text x="127" y="111" text-anchor="middle" fill="#fbbf24" font-size="8" font-weight="800">NET $</text>
              <path d="M 148 92 C 165 88, 178 24, 214 18" fill="none" stroke="#38bdf8" stroke-width="2.2" />
              <circle cx="182" cy="36" r="4.5" fill="#10b981" stroke="#ffffff" stroke-width="1.5" />
              <text x="152" y="16" fill="#38bdf8" font-size="8.5" font-weight="800" font-family="var(--font-mono)">OPTIMAL</text>
              <text x="152" y="27" fill="#10b981" font-size="8.5" font-weight="800" font-family="var(--font-mono)">PRICE PT</text>
            </g>

            <text x="16" y="224" class="svg-text-mono" font-size="9.5">• Simulates Counterfactual Depth Tiers</text>
            <text x="16" y="242" fill="#10b981" font-size="9.5" font-weight="700" font-family="var(--font-mono)">✓ Maximizes Net Pocket Margin &amp; Sell-Through</text>
          </g>

          <!-- Stage 4: Breakeven & Margin Guardrail Diamond Gate (Sub-Agent 3) -->
          <g transform="translate(736, 62)">
            <rect class="svg-node-box-warn" width="160" height="204" rx="14" stroke="#fbbf24" stroke-width="2" />
            <polygon points="80,16 100,36 80,56 60,36" fill="rgba(251,191,36,0.2)" stroke="#fbbf24" stroke-width="1.8" />
            <text x="80" y="41" text-anchor="middle" font-size="13">⚖️</text>
            <text x="80" y="74" text-anchor="middle" fill="#fbbf24" font-size="9.5" font-weight="800" font-family="var(--font-mono)">BREAKEVEN ROI GATE</text>
            <text x="80" y="93" text-anchor="middle" class="svg-text-main" font-size="11.5" font-weight="800">${trunc(subs[2].name, 19)}</text>
            <rect class="svg-pill-bg" x="12" y="106" width="136" height="42" rx="7" stroke="#fbbf2466" />
            <text x="80" y="123" text-anchor="middle" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">PASS: ROI &gt; 1.15x</text>
            <text x="80" y="138" text-anchor="middle" fill="#fb7185" font-size="9" font-weight="800" font-family="var(--font-mono)">FAIL: Loop Counterfactual</text>
            <text x="80" y="174" text-anchor="middle" class="svg-text-mono" font-size="9">enforce_tool_contract()</text>
          </g>

          <!-- Stage 5: Open Pricing / Trade Commit & Waterfall A2UI -->
          <g transform="translate(928, 38)">
            <rect class="svg-node-box-out" width="180" height="114" rx="14" stroke="#10b981" stroke-width="2" />
            <text x="14" y="24" font-size="15">💰</text>
            <text x="36" y="22" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">MCP / API / ERP COMMIT</text>
            <text x="14" y="42" class="svg-text-main" font-size="11.5" font-weight="800">${writebackLabel}</text>
            <rect class="svg-pill-bg" x="10" y="52" width="160" height="24" rx="5" stroke="#10b98166" />
            <text x="16" y="68" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">⚡ ${trunc(a1, 21)}</text>
            <text x="14" y="96" class="svg-text-mono" font-size="9">POS / CRM / ERP via MCP</text>
          </g>
          <g transform="translate(928, 176)">
            <rect class="svg-node-box" width="180" height="114" rx="14" stroke="#38bdf8" stroke-width="2" />
            <text x="14" y="24" font-size="15">📊</text>
            <text x="36" y="22" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">A2UI WATERFALL</text>
            <text x="14" y="42" class="svg-text-main" font-size="11.5" font-weight="800">${trunc(ag.badge || ag.outcome, 22)}</text>
            <rect class="svg-pill-bg" x="10" y="52" width="160" height="24" rx="5" stroke="#38bdf866" />
            <text x="16" y="68" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">✦ Elasticity VegaChart</text>
            <text x="14" y="96" class="svg-text-sub" font-size="9.5">${trunc(ag.primaryPersonaName || 'RGM / Trade Lead', 22)}</text>
          </g>
        `;
      }

      // =====================================================================
      // TOPOLOGY 3: BIDIRECTIONAL CONSTRAINT & ITERATIVE MILP PARETO LOOP
      // =====================================================================
      if (topology === 'milp_pareto_loop') {
        return `
          <!-- Dual Opposing Constraint Streams (Top: Demand vs Bottom: Capacity/Cash) -->
          <path d="M 196 76 C 216 76, 216 132, 232 132" fill="none" stroke="#38bdf8" stroke-width="2.2" stroke-dasharray="5 3" />
          <path d="M 196 254 C 216 254, 216 198, 232 198" fill="none" stroke="#f59e0b" stroke-width="2.2" stroke-dasharray="5 3" />
          <circle r="3.5" fill="#38bdf8"><animateMotion dur="1.6s" repeatCount="indefinite" path="M 196 76 C 216 76, 216 132, 232 132" /></circle>
          <circle r="3.5" fill="#f59e0b"><animateMotion dur="1.9s" repeatCount="indefinite" path="M 196 254 C 216 254, 216 198, 232 198" /></circle>

          <!-- Constraint Matrix -> Central Iterative MILP Pareto Loop -->
          <path d="M 408 165 L 440 165" fill="none" stroke="${cls.color}" stroke-width="2.6" marker-end="url(#arrowAccent_${uid})" />

          <!-- MILP Pareto Loop -> Feasibility Gate -->
          <path d="M 708 165 L 738 165" fill="none" stroke="#10b981" stroke-width="2.5" marker-end="url(#arrowGreen_${uid})" />

          <!-- Gate -> Signed Plan Commit & Pareto Surface -->
          <path d="M 896 135 C 912 135, 912 96, 928 96" fill="none" stroke="#10b981" stroke-width="2.4" marker-end="url(#arrowGreen_${uid})" />
          <path d="M 896 195 C 912 195, 912 234, 928 234" fill="none" stroke="#38bdf8" stroke-width="2.2" marker-end="url(#arrowCyan_${uid})" />

          <!-- Top-Left Opposing Stream: Demand & Service Targets (BigQuery / MCP / On-Prem) -->
          <g transform="translate(12, 22)">
            <rect class="svg-node-box" width="184" height="112" rx="14" stroke="#38bdf8" stroke-width="2" />
            <text x="14" y="25" font-size="16">${ic1}</text>
            <text x="38" y="23" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">DEMAND &amp; SLA (BQ / MCP)</text>
            <text x="14" y="44" class="svg-text-main" font-size="12" font-weight="800">${trunc(sys1, 21)}</text>
            <text x="14" y="61" class="svg-text-mono" font-size="9.5">Table: ${trunc(tbl1, 20)}</text>
            <rect class="svg-pill-bg" x="12" y="72" width="160" height="26" rx="6" stroke="#38bdf855" />
            <text x="18" y="89" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">🔍 ${trunc(q1, 20)}</text>
          </g>

          <!-- Bottom-Left Opposing Stream: Capacity, Lead-Time & Working Capital (On-Prem DB / ERP / MCP) -->
          <g transform="translate(12, 194)">
            <rect class="svg-node-box" width="184" height="112" rx="14" stroke="#f59e0b" stroke-width="2" />
            <text x="14" y="25" font-size="16">${ic2}</text>
            <text x="38" y="23" fill="#f59e0b" font-size="9" font-weight="800" font-family="var(--font-mono)">ON-PREM ERP / CAPACITY DB</text>
            <text x="14" y="44" class="svg-text-main" font-size="12" font-weight="800">${trunc(sys2, 21)}</text>
            <text x="14" y="61" class="svg-text-mono" font-size="9.5">Table: ${trunc(tbl2, 20)}</text>
            <rect class="svg-pill-bg" x="12" y="72" width="160" height="26" rx="6" stroke="#f59e0b55" />
            <text x="18" y="89" fill="#f59e0b" font-size="9" font-weight="800" font-family="var(--font-mono)">🔍 ${trunc(q2, 20)}</text>
          </g>

          <!-- Stage 2: LP / MILP Constraint Matrix Builder (Sub-Agent 1) -->
          <g transform="translate(232, 62)">
            <rect class="svg-node-box-alt" width="176" height="206" rx="14" stroke="${dept.color}" stroke-width="2" />
            <text x="14" y="26" fill="${dept.color}" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🔗 CONSTRAINT MATRIX</text>
            <text x="14" y="46" class="svg-text-main" font-size="12.5" font-weight="800">${trunc(subs[0].name, 20)}</text>
            <text x="14" y="64" class="svg-text-sub" font-size="10">${trunc(subs[0].role, 24)}</text>
            <rect class="svg-pill-bg" x="12" y="78" width="152" height="58" rx="8" stroke="${dept.color}55" />
            <text x="18" y="96" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">min Σ(Cost + Penalty)</text>
            <text x="18" y="112" class="svg-text-mono" font-size="9">s.t. Ax ≤ b (Cap/Setup)</text>
            <text x="18" y="126" class="svg-text-mono" font-size="9">Service CSL ≥ Target</text>
            <text x="14" y="160" class="svg-text-mono" font-size="9.5">+ ${trunc(sys3, 19)}</text>
            <text x="14" y="182" fill="#10b981" font-size="9.5" font-weight="800" font-family="var(--font-mono)">✓ ${tablesCount} BQ / SQL Tables</text>
          </g>

          <!-- Stage 3: Central Circular MILP Solver & Pareto Convergence Loop -->
          <g transform="translate(440, 20)">
            <rect class="svg-node-box-alt" width="268" height="290" rx="18" stroke="${cls.color}" stroke-width="2.5" />
            <rect x="14" y="12" width="240" height="22" rx="6" fill="${cls.color}28" stroke="${cls.color}" />
            <text x="134" y="27" text-anchor="middle" class="svg-text-main" font-size="9.5" font-weight="800" font-family="var(--font-mono)">⚙️ MATHEMATICAL MILP &amp; PARETO SOLVER</text>
            <text x="16" y="54" class="svg-text-main" font-size="13.5" font-weight="800">${trunc(subs[1].name, 29)}</text>
            <text x="16" y="71" fill="${cls.color}" font-size="10.5" font-weight="700">${trunc(solverLabel, 34)}</text>

            <!-- Pareto Frontier Curve + Circular Solver Loop Graphic -->
            <g transform="translate(16, 82)">
              <rect class="svg-viz-well" width="236" height="132" rx="10" stroke="${cls.color}66" stroke-width="1.2" />
              <path d="M 22 24 C 28 84, 68 104, 126 108" fill="none" stroke="${cls.color}" stroke-width="2.4" />
              <circle cx="34" cy="54" r="4.5" fill="#38bdf8" />
              <circle cx="64" cy="86" r="5.5" fill="#10b981" stroke="#ffffff" stroke-width="1.6" />
              <circle cx="104" cy="103" r="4.5" fill="#fbbf24" />
              <text x="44" y="52" fill="#38bdf8" font-size="8" font-weight="800" font-family="var(--font-mono)">MAX OTIF</text>
              <text x="74" y="84" fill="#10b981" font-size="8.5" font-weight="800" font-family="var(--font-mono)">★ OPTIMAL</text>
              <text x="80" y="120" fill="#fbbf24" font-size="8" font-weight="800" font-family="var(--font-mono)">MIN CASH</text>

              <circle cx="184" cy="64" r="32" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="6 3" />
              <circle r="3.5" fill="#10b981">
                <animateMotion dur="2.4s" repeatCount="indefinite" path="M 184 32 A 32 32 0 1 1 183.9 32" />
              </circle>
              <text x="184" y="61" text-anchor="middle" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">CP-SAT /</text>
              <text x="184" y="73" text-anchor="middle" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">MILP LOOP</text>
            </g>

            <text x="16" y="234" class="svg-text-mono" font-size="9.5">• Orchestrator: Gemini 3.8 Flash ↔ 3.1 Pro/Argon</text>
            <text x="16" y="251" class="svg-text-mono" font-size="9.5">• Evaluates Cost vs. Service vs. Working Capital</text>
            <text x="16" y="268" fill="#10b981" font-size="9.5" font-weight="700" font-family="var(--font-mono)">✓ Provably Optimal Feasible Schedule</text>
          </g>

          <!-- Stage 4: Hard Feasibility & Governance Gate (Sub-Agent 3) -->
          <g transform="translate(738, 62)">
            <rect class="svg-node-box" width="158" height="206" rx="14" stroke="#10b981" stroke-width="2" />
            <text x="14" y="25" fill="#10b981" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🛡️ FEASIBILITY GATE</text>
            <text x="14" y="45" class="svg-text-main" font-size="12" font-weight="800">${trunc(subs[2].name, 19)}</text>
            <text x="14" y="63" class="svg-text-sub" font-size="9.5">${trunc(subs[2].role, 22)}</text>
            <rect class="svg-pill-bg" x="12" y="78" width="134" height="62" rx="7" stroke="#10b98155" />
            <text x="18" y="95" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">✓ 0 Capacity Breaches</text>
            <text x="18" y="111" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">✓ 0 Material Shortages</text>
            <text x="18" y="127" fill="#fbbf24" font-size="9" font-weight="800" font-family="var(--font-mono)">✓ Idempotency Locked</text>
            <text x="14" y="166" class="svg-text-mono" font-size="9">Audit: ${trunc(tbl3, 18)}</text>
            <text x="14" y="186" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">enforce_tool_contract()</text>
          </g>

          <!-- Stage 5: Open MCP / API / On-Prem Plan Commit & Pareto A2UI -->
          <g transform="translate(928, 38)">
            <rect class="svg-node-box-out" width="180" height="114" rx="14" stroke="#10b981" stroke-width="2" />
            <text x="14" y="24" font-size="15">🚀</text>
            <text x="36" y="22" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">MCP / API / ERP COMMIT</text>
            <text x="14" y="42" class="svg-text-main" font-size="11.5" font-weight="800">${writebackLabel}</text>
            <rect class="svg-pill-bg" x="10" y="52" width="160" height="24" rx="5" stroke="#10b98166" />
            <text x="16" y="68" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">⚡ ${trunc(a1, 21)}</text>
            <text x="14" y="96" class="svg-text-mono" font-size="9">ERP / APS via MCP or API</text>
          </g>
          <g transform="translate(928, 176)">
            <rect class="svg-node-box" width="180" height="114" rx="14" stroke="#38bdf8" stroke-width="2" />
            <text x="14" y="24" font-size="15">📊</text>
            <text x="36" y="22" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">PARETO A2UI SURFACE</text>
            <text x="14" y="42" class="svg-text-main" font-size="11.5" font-weight="800">${trunc(ag.badge || ag.outcome, 22)}</text>
            <rect class="svg-pill-bg" x="10" y="52" width="160" height="24" rx="5" stroke="#38bdf866" />
            <text x="16" y="68" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">✦ Trade-Off VegaChart</text>
            <text x="14" y="96" class="svg-text-sub" font-size="9.5">${trunc(ag.primaryPersonaName || 'Planning Lead', 22)}</text>
          </g>
        `;
      }

      // =====================================================================
      // TOPOLOGY 4: MULTI-HOP KNOWLEDGE GRAPH & SEMANTIC CONTRACT/INVOICE AUDIT
      // =====================================================================
      if (topology === 'graph_contract_audit') {
        return `
          <!-- Docs & Tier-N Feeds -> Multi-Hop Graph & Vector Index Canvas -->
          <path d="M 192 56 C 210 56, 210 120, 226 120" fill="none" stroke="${dept.color}" stroke-width="2" stroke-dasharray="5 3" />
          <path d="M 192 165 L 226 165" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="5 3" />
          <path d="M 192 274 C 210 274, 210 210, 226 210" fill="none" stroke="#f59e0b" stroke-width="2" stroke-dasharray="5 3" />
          <circle r="3.5" fill="${dept.color}"><animateMotion dur="1.8s" repeatCount="indefinite" path="M 192 56 C 210 56, 210 120, 226 120" /></circle>
          <circle r="3.5" fill="#38bdf8"><animateMotion dur="1.5s" repeatCount="indefinite" path="M 192 165 L 226 165" /></circle>

          <!-- Graph Canvas -> Clause & Discrepancy Auditor -->
          <path d="M 468 165 L 498 165" fill="none" stroke="#38bdf8" stroke-width="2.5" marker-end="url(#arrowCyan_${uid})" />

          <!-- Auditor -> Compliance Hold Gate -->
          <path d="M 712 165 L 740 165" fill="none" stroke="#f43f5e" stroke-width="2.4" marker-end="url(#arrowAccent_${uid})" />

          <!-- Gate -> ERP Block / Debit Memo / Award -->
          <path d="M 896 135 C 912 135, 912 96, 928 96" fill="none" stroke="#10b981" stroke-width="2.4" marker-end="url(#arrowGreen_${uid})" />
          <path d="M 896 195 C 912 195, 912 234, 928 234" fill="none" stroke="#38bdf8" stroke-width="2.2" marker-end="url(#arrowCyan_${uid})" />

          <!-- Left 3 Document, BOM & Index Feeds (Open MCP / On-Prem / BigQuery) -->
          <g transform="translate(12, 18)">
            <rect class="svg-node-box" width="180" height="76" rx="12" stroke="${dept.color}" stroke-width="1.8" />
            <text x="14" y="25" font-size="16">📄</text>
            <text x="36" y="23" fill="${dept.color}" font-size="9" font-weight="800" font-family="var(--font-mono)">DOCS / INVOICES (MCP / DB)</text>
            <text x="14" y="45" class="svg-text-main" font-size="12" font-weight="800">${trunc(sys1, 20)}</text>
            <text x="14" y="62" class="svg-text-mono" font-size="9.5">↳ ${trunc(tbl1, 21)}</text>
          </g>
          <g transform="translate(12, 127)">
            <rect class="svg-node-box" width="180" height="76" rx="12" stroke="#38bdf8" stroke-width="1.8" />
            <text x="14" y="25" font-size="16">🕸️</text>
            <text x="36" y="23" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">MULTI-TIER BOM (BQ / SQL)</text>
            <text x="14" y="45" class="svg-text-main" font-size="12" font-weight="800">${trunc(sys2, 20)}</text>
            <text x="14" y="62" class="svg-text-mono" font-size="9.5">↳ ${trunc(tbl2, 21)}</text>
          </g>
          <g transform="translate(12, 236)">
            <rect class="svg-node-box" width="180" height="76" rx="12" stroke="#f59e0b" stroke-width="1.8" />
            <text x="14" y="25" font-size="16">${ic3}</text>
            <text x="36" y="23" fill="#f59e0b" font-size="9" font-weight="800" font-family="var(--font-mono)">3RD-PARTY INDEX / MCP</text>
            <text x="14" y="45" class="svg-text-main" font-size="12" font-weight="800">${trunc(sys3, 20)}</text>
            <text x="14" y="62" class="svg-text-mono" font-size="9.5">↳ ${trunc(tbl3, 21)}</text>
          </g>

          <!-- Stage 2: Open Graph Lineage & Vector Search Index Canvas (Sub-Agent 1) -->
          <g transform="translate(226, 26)">
            <rect class="svg-node-box-alt" width="242" height="278" rx="16" stroke="#38bdf8" stroke-width="2.2" />
            <text x="14" y="24" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🕸️ GRAPH LINEAGE &amp; VECTOR INDEX</text>
            <text x="14" y="44" class="svg-text-main" font-size="13" font-weight="800">${trunc(subs[0].name, 25)}</text>
            <text x="14" y="61" class="svg-text-sub" font-size="10">Pluggable Graph / Vector DB / BigQuery</text>

            <!-- Multi-Hop Knowledge Graph Visual Network -->
            <g transform="translate(14, 72)">
              <rect class="svg-viz-well" width="214" height="122" rx="10" stroke="#38bdf866" />
              <line x1="34" y1="62" x2="92" y2="30" stroke="#38bdf8" stroke-width="1.8" />
              <line x1="34" y1="62" x2="92" y2="94" stroke="#38bdf8" stroke-width="1.8" />
              <line x1="92" y1="30" x2="162" y2="44" stroke="#f43f5e" stroke-width="2" stroke-dasharray="4 2" />
              <line x1="92" y1="94" x2="162" y2="86" stroke="#10b981" stroke-width="1.8" />
              <line x1="92" y1="30" x2="92" y2="94" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="2 2" />
              <circle cx="34" cy="62" r="11" fill="#0f172a" stroke="#38bdf8" stroke-width="2" />
              <text x="34" y="65" text-anchor="middle" fill="#38bdf8" font-size="8" font-weight="800">SKU</text>
              <circle cx="92" cy="30" r="11" fill="#0f172a" stroke="#fbbf24" stroke-width="2" />
              <text x="92" y="33" text-anchor="middle" fill="#fbbf24" font-size="8" font-weight="800">T-1</text>
              <circle cx="92" cy="94" r="11" fill="#0f172a" stroke="#10b981" stroke-width="2" />
              <text x="92" y="97" text-anchor="middle" fill="#10b981" font-size="8" font-weight="800">DOC</text>
              <circle cx="162" cy="44" r="13" fill="rgba(244,63,94,0.25)" stroke="#f43f5e" stroke-width="2.2" />
              <text x="162" y="47" text-anchor="middle" fill="#fb7185" font-size="8" font-weight="800">RISK</text>
              <circle cx="162" cy="86" r="11" fill="#0f172a" stroke="#10b981" stroke-width="2" />
              <text x="162" y="89" text-anchor="middle" fill="#10b981" font-size="8" font-weight="800">ALT</text>
            </g>

            <rect class="svg-pill-bg" x="14" y="204" width="214" height="26" rx="6" stroke="rgba(56,189,248,0.4)" />
            <text x="20" y="221" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">🔍 ${trunc(q1, 25)}</text>
            <rect class="svg-pill-bg" x="14" y="236" width="214" height="26" rx="6" stroke="rgba(56,189,248,0.4)" />
            <text x="20" y="253" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">🔍 ${trunc(q2, 25)}</text>
          </g>

          <!-- Stage 3: Clause, Rate & Discrepancy Auditor (Sub-Agent 2) -->
          <g transform="translate(498, 42)">
            <rect class="svg-node-box-alt" width="214" height="246" rx="16" stroke="${cls.color}" stroke-width="2.4" />
            <text x="14" y="25" fill="${cls.color}" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🔍 SEMANTIC &amp; RATE AUDITOR</text>
            <text x="14" y="45" class="svg-text-main" font-size="13" font-weight="800">${trunc(subs[1].name, 22)}</text>
            <text x="14" y="63" fill="${cls.color}" font-size="10" font-weight="700">Gemini 3.8 Flash ↔ 3.1 Pro/Argon</text>
            <rect class="svg-pill-bg" x="12" y="78" width="190" height="44" rx="7" stroke="${cls.color}55" />
            <text x="18" y="95" class="svg-text-main" font-size="10" font-weight="700">Contract vs. Billed Audit</text>
            <text x="18" y="111" class="svg-text-mono" font-size="9">${trunc(solverLabel, 25)}</text>
            <rect class="svg-pill-bg" x="12" y="130" width="190" height="44" rx="7" stroke="#f43f5e55" />
            <text x="18" y="147" fill="#fb7185" font-size="9.5" font-weight="800" font-family="var(--font-mono)">⚠️ Variance &amp; Risk Pinpoint</text>
            <text x="18" y="163" class="svg-text-mono" font-size="9">Line-Item Clause Citation</text>
            <text x="14" y="198" class="svg-text-mono" font-size="9.5">• Zero-Hallucination Citation</text>
            <text x="14" y="216" fill="#10b981" font-size="9.5" font-weight="700" font-family="var(--font-mono)">✓ Exact Dollar/Carbon Delta</text>
          </g>

          <!-- Stage 4: Compliance & 3-Way Match Hold Gate (Sub-Agent 3) -->
          <g transform="translate(740, 62)">
            <rect class="svg-node-box-warn" width="156" height="206" rx="14" stroke="#f43f5e" stroke-width="2" />
            <text x="14" y="25" fill="#fb7185" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🔒 COMPLIANCE GATE</text>
            <text x="14" y="45" class="svg-text-main" font-size="12" font-weight="800">${trunc(subs[2].name, 18)}</text>
            <text x="14" y="63" class="svg-text-sub" font-size="9.5">${trunc(subs[2].role, 21)}</text>
            <rect class="svg-pill-bg" x="12" y="80" width="132" height="58" rx="7" stroke="#f43f5e66" />
            <text x="18" y="98" fill="#fb7185" font-size="9" font-weight="800" font-family="var(--font-mono)">Blocks Overbill /</text>
            <text x="18" y="113" fill="#fb7185" font-size="9" font-weight="800" font-family="var(--font-mono)">Non-Compliant Tier-N</text>
            <text x="18" y="128" fill="#10b981" font-size="8.5" font-weight="800" font-family="var(--font-mono)">Auto-Clears Exact Match</text>
            <text x="14" y="168" class="svg-text-mono" font-size="9">enforce_tool_contract()</text>
            <text x="14" y="186" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">✓ Audit Trail Signed</text>
          </g>

          <!-- Stage 5: Open ERP / Procurement MCP Write-Back & Graph A2UI -->
          <g transform="translate(928, 38)">
            <rect class="svg-node-box-out" width="180" height="114" rx="14" stroke="#10b981" stroke-width="2" />
            <text x="14" y="24" font-size="15">✅</text>
            <text x="36" y="22" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">MCP / API / ERP ACTION</text>
            <text x="14" y="42" class="svg-text-main" font-size="11.5" font-weight="800">${writebackLabel}</text>
            <rect class="svg-pill-bg" x="10" y="52" width="160" height="24" rx="5" stroke="#10b98166" />
            <text x="16" y="68" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">⚡ ${trunc(a1, 21)}</text>
            <text x="14" y="96" class="svg-text-mono" font-size="9">ERP / Sourcing via MCP</text>
          </g>
          <g transform="translate(928, 176)">
            <rect class="svg-node-box" width="180" height="114" rx="14" stroke="#38bdf8" stroke-width="2" />
            <text x="14" y="24" font-size="15">📊</text>
            <text x="36" y="22" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">LINEAGE A2UI SURFACE</text>
            <text x="14" y="42" class="svg-text-main" font-size="11.5" font-weight="800">${trunc(ag.badge || ag.outcome, 22)}</text>
            <rect class="svg-pill-bg" x="10" y="52" width="160" height="24" rx="5" stroke="#38bdf866" />
            <text x="16" y="68" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">✦ Audit VegaChart</text>
            <text x="14" y="96" class="svg-text-sub" font-size="9.5">${trunc(ag.primaryPersonaName || 'Sourcing / AP Lead', 22)}</text>
          </g>
        `;
      }

      // =====================================================================
      // TOPOLOGY 5: INDUSTRIAL EDGE VISION, FFT TELEMETRY & PLC LINE ACTUATOR
      // =====================================================================
      if (topology === 'edge_vision_iot') {
        return `
          <!-- High-Frequency Edge Camera / PLC Sensors -> Stream Normalizer -->
          <path d="M 192 56 C 210 56, 210 126, 228 126" fill="none" stroke="#f59e0b" stroke-width="2.2" stroke-dasharray="4 2" />
          <path d="M 192 165 L 228 165" fill="none" stroke="#38bdf8" stroke-width="2.2" stroke-dasharray="4 2" />
          <path d="M 192 274 C 210 274, 210 204, 228 204" fill="none" stroke="#10b981" stroke-width="2.2" stroke-dasharray="4 2" />
          <circle r="3.5" fill="#f59e0b"><animateMotion dur="1.1s" repeatCount="indefinite" path="M 192 56 C 210 56, 210 126, 228 126" /></circle>
          <circle r="3.5" fill="#38bdf8"><animateMotion dur="0.9s" repeatCount="indefinite" path="M 192 165 L 228 165" /></circle>
          <circle r="3.5" fill="#10b981"><animateMotion dur="1.3s" repeatCount="indefinite" path="M 192 274 C 210 274, 210 204, 228 204" /></circle>

          <!-- Stream Normalizer -> Vision & FFT Spectrogram Classifier -->
          <path d="M 406 165 L 438 165" fill="none" stroke="#f59e0b" stroke-width="2.6" marker-end="url(#arrowAccent_${uid})" />

          <!-- Classifier -> Safety & QA Interlock -->
          <path d="M 702 165 L 734 165" fill="none" stroke="#10b981" stroke-width="2.5" marker-end="url(#arrowGreen_${uid})" />

          <!-- Interlock -> Physical PLC Actuator + MES/ERP Work Order -->
          <path d="M 894 135 C 910 135, 910 96, 926 96" fill="none" stroke="#10b981" stroke-width="2.4" marker-end="url(#arrowGreen_${uid})" />
          <path d="M 894 195 C 910 195, 910 234, 926 234" fill="none" stroke="#38bdf8" stroke-width="2.2" marker-end="url(#arrowCyan_${uid})" />

          <!-- 3 Industrial Edge Sensor Nodes (On-Prem OPC-UA / MQTT / BigQuery) -->
          <g transform="translate(12, 18)">
            <rect class="svg-node-box" width="180" height="76" rx="12" stroke="#f59e0b" stroke-width="1.8" />
            <text x="14" y="25" font-size="16">📷</text>
            <text x="36" y="23" fill="#f59e0b" font-size="9" font-weight="800" font-family="var(--font-mono)">EDGE VISION / RTSP STREAM</text>
            <text x="14" y="45" class="svg-text-main" font-size="12" font-weight="800">${trunc(sys1, 20)}</text>
            <text x="14" y="62" class="svg-text-mono" font-size="9.5">↳ ${trunc(tbl1, 21)}</text>
          </g>
          <g transform="translate(12, 127)">
            <rect class="svg-node-box" width="180" height="76" rx="12" stroke="#38bdf8" stroke-width="1.8" />
            <text x="14" y="25" font-size="16">📳</text>
            <text x="36" y="23" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">OPC-UA / MQTT / HISTORIAN</text>
            <text x="14" y="45" class="svg-text-main" font-size="12" font-weight="800">${trunc(sys2, 20)}</text>
            <text x="14" y="62" class="svg-text-mono" font-size="9.5">↳ ${trunc(tbl2, 21)}</text>
          </g>
          <g transform="translate(12, 236)">
            <rect class="svg-node-box" width="180" height="76" rx="12" stroke="#10b981" stroke-width="1.8" />
            <text x="14" y="25" font-size="16">${ic3}</text>
            <text x="36" y="23" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">MES / LIMS / ON-PREM DB</text>
            <text x="14" y="45" class="svg-text-main" font-size="12" font-weight="800">${trunc(sys3, 20)}</text>
            <text x="14" y="62" class="svg-text-mono" font-size="9.5">↳ ${trunc(tbl3, 21)}</text>
          </g>

          <!-- Stage 2: Sub-Second Edge Stream Normalizer (Sub-Agent 1) -->
          <g transform="translate(228, 62)">
            <rect class="svg-node-box-alt" width="178" height="206" rx="14" stroke="#38bdf8" stroke-width="2" />
            <text x="14" y="25" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">⚡ STREAM NORMALIZER</text>
            <text x="14" y="45" class="svg-text-main" font-size="12.5" font-weight="800">${trunc(subs[0].name, 20)}</text>
            <text x="14" y="62" class="svg-text-sub" font-size="10">${trunc(subs[0].role, 24)}</text>
            <rect class="svg-pill-bg" x="10" y="76" width="158" height="38" rx="7" stroke="rgba(56,189,248,0.4)" />
            <text x="16" y="92" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🔍 ${trunc(q1, 20)}</text>
            <text x="16" y="106" class="svg-text-mono" font-size="9">60fps + kHz FFT Window</text>
            <rect class="svg-pill-bg" x="10" y="122" width="158" height="38" rx="7" stroke="rgba(56,189,248,0.4)" />
            <text x="16" y="138" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🔍 ${trunc(q2, 20)}</text>
            <text x="16" y="152" class="svg-text-mono" font-size="9">BigQuery / Historian Sync</text>
            <text x="14" y="186" fill="#10b981" font-size="9.5" font-weight="800" font-family="var(--font-mono)">✓ Edge-to-Cloud Sync</text>
          </g>

          <!-- Stage 3: Multimodal Vision Bounding-Box & FFT Waveform Classifier (Sub-Agent 2) -->
          <g transform="translate(438, 24)">
            <rect class="svg-node-box-alt" width="264" height="282" rx="16" stroke="#f59e0b" stroke-width="2.4" />
            <rect x="14" y="12" width="236" height="22" rx="6" fill="rgba(245,158,11,0.2)" stroke="#f59e0b" />
            <text x="132" y="27" text-anchor="middle" class="svg-text-main" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🔬 VISION &amp; FFT SPECTROGRAM ENGINE</text>
            <text x="16" y="54" class="svg-text-main" font-size="13.5" font-weight="800">${trunc(subs[1].name, 28)}</text>
            <text x="16" y="71" fill="#fbbf24" font-size="10.5" font-weight="700">Gemini 3.8 Flash Multimodal + Edge CV</text>

            <g transform="translate(16, 82)">
              <rect class="svg-viz-well" width="232" height="126" rx="10" stroke="#f59e0b66" stroke-width="1.2" />
              <path d="M 12 66 L 26 66 L 32 28 L 38 98 L 44 20 L 50 92 L 56 42 L 62 76 L 70 66 L 94 66" fill="none" stroke="#fbbf24" stroke-width="2" />
              <line x1="12" y1="32" x2="96" y2="32" stroke="#f43f5e" stroke-width="1" stroke-dasharray="3 2" />
              <text x="14" y="25" fill="#fb7185" font-size="8" font-weight="800" font-family="var(--font-mono)">FFT SPIKE</text>
              <text x="14" y="114" class="svg-text-mono" font-size="8">VIBRATION / TEMP</text>

              <rect x="108" y="14" width="110" height="96" rx="6" fill="rgba(15,23,42,0.75)" stroke="#38bdf8" stroke-width="1.4" />
              <rect x="124" y="30" width="54" height="44" rx="4" fill="rgba(244,63,94,0.18)" stroke="#f43f5e" stroke-width="1.8" stroke-dasharray="4 2" />
              <circle cx="151" cy="52" r="8" fill="rgba(244,63,94,0.45)" stroke="#f43f5e" stroke-width="1.5" />
              <text x="124" y="26" fill="#fb7185" font-size="8" font-weight="800" font-family="var(--font-mono)">DEFECT 99.4%</text>
              <text x="120" y="96" fill="#10b981" font-size="8" font-weight="800" font-family="var(--font-mono)">✓ ZERO-FALSE-REJECT</text>
            </g>

            <text x="16" y="230" class="svg-text-mono" font-size="9.5">• Tech: ${trunc(solverLabel, 32)}</text>
            <text x="16" y="247" class="svg-text-mono" font-size="9.5">• Pinpoints Root-Cause Parameter Drift</text>
            <text x="16" y="264" fill="#10b981" font-size="9.5" font-weight="700" font-family="var(--font-mono)">✓ Real-Time Anomaly Classification</text>
          </g>

          <!-- Stage 4: ISO / FDA / Safety Interlock Gate (Sub-Agent 3) -->
          <g transform="translate(734, 62)">
            <rect class="svg-node-box-warn" width="160" height="206" rx="14" stroke="#f59e0b" stroke-width="2" />
            <text x="14" y="25" fill="#fbbf24" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🚨 SAFETY &amp; QA INTERLOCK</text>
            <text x="14" y="45" class="svg-text-main" font-size="12" font-weight="800">${trunc(subs[2].name, 19)}</text>
            <text x="14" y="63" class="svg-text-sub" font-size="9.5">${trunc(subs[2].role, 22)}</text>
            <rect class="svg-pill-bg" x="12" y="80" width="136" height="58" rx="7" stroke="#f59e0b66" />
            <text x="18" y="98" fill="#fbbf24" font-size="9" font-weight="800" font-family="var(--font-mono)">ISO / GxP / HACCP</text>
            <text x="18" y="113" class="svg-text-mono" font-size="9">Tolerance Verification</text>
            <text x="18" y="128" fill="#10b981" font-size="8.5" font-weight="800" font-family="var(--font-mono)">Blocks Unsafe Actuation</text>
            <text x="14" y="168" class="svg-text-mono" font-size="9">enforce_tool_contract()</text>
            <text x="14" y="186" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">✓ Interlock Cleared</text>
          </g>

          <!-- Stage 5: Dual PLC Actuator + MES/QMS/ERP Write-Back -->
          <g transform="translate(926, 38)">
            <rect class="svg-node-box-out" width="182" height="114" rx="14" stroke="#10b981" stroke-width="2" />
            <text x="14" y="24" font-size="15">🔧</text>
            <text x="36" y="22" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">PLC / MES / ERP ACTION</text>
            <text x="14" y="42" class="svg-text-main" font-size="11.5" font-weight="800">${writebackLabel}</text>
            <rect class="svg-pill-bg" x="10" y="52" width="162" height="24" rx="5" stroke="#10b98166" />
            <text x="16" y="68" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">⚡ ${trunc(a1, 21)}</text>
            <text x="14" y="96" class="svg-text-mono" font-size="9">OPC-UA / MES / QMS via MCP</text>
          </g>
          <g transform="translate(926, 176)">
            <rect class="svg-node-box" width="182" height="114" rx="14" stroke="#38bdf8" stroke-width="2" />
            <text x="14" y="24" font-size="15">📊</text>
            <text x="36" y="22" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">TELEMETRY A2UI</text>
            <text x="14" y="42" class="svg-text-main" font-size="11.5" font-weight="800">${trunc(ag.badge || ag.outcome, 22)}</text>
            <rect class="svg-pill-bg" x="10" y="52" width="162" height="24" rx="5" stroke="#38bdf866" />
            <text x="16" y="68" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">✦ Spectrogram VegaChart</text>
            <text x="14" y="96" class="svg-text-sub" font-size="9.5">${trunc(ag.primaryPersonaName || 'Plant / QA Lead', 22)}</text>
          </g>
        `;
      }

      // =====================================================================
      // TOPOLOGY 6: SPATIAL 3D WAREHOUSE, YARD GEOFENCE & LOW-LATENCY ATP
      // =====================================================================
      if (topology === 'spatial_wms_atp') {
        return `
          <!-- Live Orders & Yard GPS -> Low-Latency State & Reservation Store -->
          <path d="M 196 92 C 214 92, 214 134, 232 134" fill="none" stroke="#10b981" stroke-width="2.2" stroke-dasharray="5 3" />
          <path d="M 196 238 C 214 238, 214 196, 232 196" fill="none" stroke="#38bdf8" stroke-width="2.2" stroke-dasharray="5 3" />
          <circle r="3.5" fill="#10b981"><animateMotion dur="1.3s" repeatCount="indefinite" path="M 196 92 C 214 92, 214 134, 232 134" /></circle>
          <circle r="3.5" fill="#38bdf8"><animateMotion dur="1.6s" repeatCount="indefinite" path="M 196 238 C 214 238, 214 196, 232 196" /></circle>

          <!-- State Twin -> 3D Spatial Rack & Wave Solver -->
          <path d="M 412 165 L 444 165" fill="none" stroke="#10b981" stroke-width="2.6" marker-end="url(#arrowGreen_${uid})" />

          <!-- Spatial Solver -> Quota & Congestion Gate -->
          <path d="M 704 165 L 736 165" fill="none" stroke="#38bdf8" stroke-width="2.5" marker-end="url(#arrowCyan_${uid})" />

          <!-- Gate -> Direct WMS / OMS Execution -->
          <path d="M 896 135 C 912 135, 912 96, 928 96" fill="none" stroke="#10b981" stroke-width="2.4" marker-end="url(#arrowGreen_${uid})" />
          <path d="M 896 195 C 912 195, 912 234, 928 234" fill="none" stroke="#38bdf8" stroke-width="2.2" marker-end="url(#arrowCyan_${uid})" />

          <!-- Left Top: Live Order / WMS Stream (MCP / On-Prem / API) -->
          <g transform="translate(12, 34)">
            <rect class="svg-node-box" width="184" height="116" rx="14" stroke="#10b981" stroke-width="2" />
            <text x="14" y="26" font-size="17">🛒</text>
            <text x="38" y="24" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">WMS / OMS (MCP / ON-PREM)</text>
            <text x="14" y="46" class="svg-text-main" font-size="12.5" font-weight="800">${trunc(sys1, 21)}</text>
            <text x="14" y="64" class="svg-text-mono" font-size="9.5">Table: ${trunc(tbl1, 20)}</text>
            <rect class="svg-pill-bg" x="12" y="76" width="160" height="26" rx="6" stroke="#10b98155" />
            <text x="18" y="93" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">🔍 ${trunc(q1, 20)}</text>
          </g>

          <!-- Left Bottom: Yard GPS Geofence / RFID / BigQuery Twin -->
          <g transform="translate(12, 178)">
            <rect class="svg-node-box" width="184" height="116" rx="14" stroke="#38bdf8" stroke-width="2" />
            <text x="14" y="26" font-size="17">${ic2}</text>
            <text x="38" y="24" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">YARD GPS / BIGQUERY TWIN</text>
            <text x="14" y="46" class="svg-text-main" font-size="12.5" font-weight="800">${trunc(sys2, 21)}</text>
            <text x="14" y="64" class="svg-text-mono" font-size="9.5">Table: ${trunc(tbl2, 20)}</text>
            <rect class="svg-pill-bg" x="12" y="76" width="160" height="26" rx="6" stroke="#38bdf855" />
            <text x="18" y="93" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">🔍 ${trunc(q2, 20)}</text>
          </g>

          <!-- Stage 2: Low-Latency Transactional & Inventory State Store (Sub-Agent 1) -->
          <g transform="translate(232, 54)">
            <rect class="svg-node-box-alt" width="180" height="222" rx="14" stroke="#10b981" stroke-width="2" />
            <text x="14" y="26" fill="#10b981" font-size="9.5" font-weight="800" font-family="var(--font-mono)">📐 STATE &amp; LOCK STORE</text>
            <text x="14" y="46" class="svg-text-main" font-size="12.5" font-weight="800">${trunc(subs[0].name, 21)}</text>
            <text x="14" y="64" class="svg-text-sub" font-size="10">Transactional SQL / On-Prem / BQ</text>
            <rect class="svg-pill-bg" x="12" y="80" width="156" height="44" rx="7" stroke="#10b98166" />
            <text x="18" y="98" fill="#10b981" font-size="9.5" font-weight="800" font-family="var(--font-mono)">⚡ Atomic Inventory Lock</text>
            <text x="18" y="113" class="svg-text-mono" font-size="9">Zero-Oversell Reservation</text>
            <rect class="svg-pill-bg" x="12" y="132" width="156" height="44" rx="7" stroke="#38bdf866" />
            <text x="18" y="150" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">📏 3D Cube &amp; Velocity</text>
            <text x="18" y="165" class="svg-text-mono" font-size="9">${tablesCount} Live WMS/ATP Tables</text>
            <text x="14" y="202" fill="#10b981" font-size="9.5" font-weight="800" font-family="var(--font-mono)">✓ Pluggable State DB</text>
          </g>

          <!-- Stage 3: 3D Isometric Warehouse Rack, Slotting & Wave Optimizer (Sub-Agent 2) -->
          <g transform="translate(444, 24)">
            <rect class="svg-node-box-alt" width="260" height="282" rx="16" stroke="${cls.color}" stroke-width="2.4" />
            <rect x="14" y="12" width="232" height="22" rx="6" fill="${cls.color}26" stroke="${cls.color}" />
            <text x="130" y="27" text-anchor="middle" class="svg-text-main" font-size="9.5" font-weight="800" font-family="var(--font-mono)">📦 3D SPATIAL RACK, DOCK &amp; ATP SOLVER</text>
            <text x="16" y="54" class="svg-text-main" font-size="13.5" font-weight="800">${trunc(subs[1].name, 28)}</text>
            <text x="16" y="71" fill="${cls.color}" font-size="10.5" font-weight="700">${trunc(solverLabel, 33)}</text>

            <g transform="translate(16, 84)">
              <rect class="svg-viz-well" width="228" height="124" rx="10" stroke="#10b98166" stroke-width="1.2" />
              <rect x="16" y="18" width="26" height="20" rx="3" fill="#334155" stroke="#64748b" />
              <rect x="48" y="18" width="26" height="20" rx="3" fill="#38bdf8" />
              <rect x="80" y="18" width="26" height="20" rx="3" fill="#334155" stroke="#64748b" />
              <rect x="16" y="46" width="26" height="20" rx="3" fill="#10b981" stroke="#ffffff" stroke-width="1.2" />
              <rect x="48" y="46" width="26" height="20" rx="3" fill="#10b981" stroke="#ffffff" stroke-width="1.2" />
              <rect x="80" y="46" width="26" height="20" rx="3" fill="#fbbf24" />
              <rect x="16" y="74" width="26" height="20" rx="3" fill="#38bdf8" />
              <rect x="48" y="74" width="26" height="20" rx="3" fill="#10b981" />
              <rect x="80" y="74" width="26" height="20" rx="3" fill="#334155" stroke="#64748b" />
              <text x="61" y="110" text-anchor="middle" fill="#10b981" font-size="8" font-weight="800" font-family="var(--font-mono)">GOLDEN ZONE SLOTS</text>

              <path d="M 126 92 L 126 26 L 164 26 L 164 92 L 204 92 L 204 26" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4 2" />
              <circle cx="126" cy="56" r="4.5" fill="#10b981" />
              <circle cx="164" cy="44" r="4.5" fill="#fbbf24" />
              <circle cx="204" cy="26" r="5" fill="#38bdf8" />
              <text x="166" y="110" text-anchor="middle" fill="#38bdf8" font-size="8" font-weight="800" font-family="var(--font-mono)">OPTIMAL PICK / DOCK</text>
            </g>

            <text x="16" y="230" class="svg-text-mono" font-size="9.5">• Minimizes Travel Distance &amp; Dock Dwell</text>
            <text x="16" y="247" class="svg-text-mono" font-size="9.5">• Respects Crushability, Hazmat &amp; Cold Zones</text>
            <text x="16" y="264" fill="#10b981" font-size="9.5" font-weight="700" font-family="var(--font-mono)">✓ Zero-Conflict Spatial Assignment</text>
          </g>

          <!-- Stage 4: Quota & Aisle Congestion Gate (Sub-Agent 3) -->
          <g transform="translate(736, 62)">
            <rect class="svg-node-box" width="160" height="206" rx="14" stroke="#38bdf8" stroke-width="2" />
            <text x="14" y="25" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🚦 QUOTA &amp; DOCK GATE</text>
            <text x="14" y="45" class="svg-text-main" font-size="12" font-weight="800">${trunc(subs[2].name, 19)}</text>
            <text x="14" y="63" class="svg-text-sub" font-size="9.5">${trunc(subs[2].role, 22)}</text>
            <rect class="svg-pill-bg" x="12" y="80" width="136" height="58" rx="7" stroke="#38bdf855" />
            <text x="18" y="98" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">✓ Tier-1 Quota Protected</text>
            <text x="18" y="113" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">✓ MHE Aisle De-Conflicted</text>
            <text x="18" y="128" fill="#fbbf24" font-size="9" font-weight="800" font-family="var(--font-mono)">✓ Cut-Off SLA Verified</text>
            <text x="14" y="168" class="svg-text-mono" font-size="9">enforce_tool_contract()</text>
            <text x="14" y="186" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">✓ Atomic Lock Released</text>
          </g>

          <!-- Stage 5: Open WMS / OMS / ERP Commit & Spatial A2UI -->
          <g transform="translate(928, 38)">
            <rect class="svg-node-box-out" width="180" height="114" rx="14" stroke="#10b981" stroke-width="2" />
            <text x="14" y="24" font-size="15">🏢</text>
            <text x="36" y="22" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">WMS / OMS WRITE-BACK</text>
            <text x="14" y="42" class="svg-text-main" font-size="11.5" font-weight="800">${writebackLabel}</text>
            <rect class="svg-pill-bg" x="10" y="52" width="160" height="24" rx="5" stroke="#10b98166" />
            <text x="16" y="68" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">⚡ ${trunc(a1, 21)}</text>
            <text x="14" y="96" class="svg-text-mono" font-size="9">WMS / ERP via MCP or API</text>
          </g>
          <g transform="translate(928, 176)">
            <rect class="svg-node-box" width="180" height="114" rx="14" stroke="#38bdf8" stroke-width="2" />
            <text x="14" y="24" font-size="15">📊</text>
            <text x="36" y="22" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">SPATIAL A2UI SURFACE</text>
            <text x="14" y="42" class="svg-text-main" font-size="11.5" font-weight="800">${trunc(ag.badge || ag.outcome, 22)}</text>
            <rect class="svg-pill-bg" x="10" y="52" width="160" height="24" rx="5" stroke="#38bdf866" />
            <text x="16" y="68" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">✦ 3D Slot/ATP VegaChart</text>
            <text x="14" y="96" class="svg-text-sub" font-size="9.5">${trunc(ag.primaryPersonaName || 'DC / Fulfillment Lead', 22)}</text>
          </g>
        `;
      }

      // =====================================================================
      // TOPOLOGY 7: 4-MODE GLOBAL CORRIDOR, GEOSPATIAL VRP & 3D LIFO LOAD
      // =====================================================================
      if (topology === 'multimodal_corridor_vrp') {
        return `
          <!-- 4 Parallel Mode Feeds (Ocean / Air / Rail / Road) -> Corridor Digital Twin -->
          <path d="M 192 44 C 212 44, 212 118, 228 118" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="5 3" />
          <path d="M 192 122 C 212 122, 212 148, 228 148" fill="none" stroke="#a855f7" stroke-width="2" stroke-dasharray="5 3" />
          <path d="M 192 200 C 212 200, 212 178, 228 178" fill="none" stroke="#f59e0b" stroke-width="2" stroke-dasharray="5 3" />
          <path d="M 192 278 C 212 278, 212 208, 228 208" fill="none" stroke="#10b981" stroke-width="2" stroke-dasharray="5 3" />
          <circle r="3" fill="#38bdf8"><animateMotion dur="1.7s" repeatCount="indefinite" path="M 192 44 C 212 44, 212 118, 228 118" /></circle>
          <circle r="3" fill="#10b981"><animateMotion dur="1.4s" repeatCount="indefinite" path="M 192 278 C 212 278, 212 208, 228 208" /></circle>

          <!-- Corridor Twin -> Geospatial VRP + 3D LIFO Axle Solver -->
          <path d="M 408 165 L 440 165" fill="none" stroke="#38bdf8" stroke-width="2.6" marker-end="url(#arrowCyan_${uid})" />

          <!-- Solver -> DOT Axle-Weight & HOS Safety Gate -->
          <path d="M 704 165 L 736 165" fill="none" stroke="#10b981" stroke-width="2.5" marker-end="url(#arrowGreen_${uid})" />

          <!-- Gate -> Carrier Tender / TMS Dispatch -->
          <path d="M 896 135 C 912 135, 912 96, 928 96" fill="none" stroke="#10b981" stroke-width="2.4" marker-end="url(#arrowGreen_${uid})" />
          <path d="M 896 195 C 912 195, 912 234, 928 234" fill="none" stroke="#38bdf8" stroke-width="2.2" marker-end="url(#arrowCyan_${uid})" />

          <!-- 4 Parallel Mode Feed Cards on Left (MCP / EDI / API / BigQuery) -->
          <g transform="translate(12, 12)">
            <rect class="svg-node-box" width="180" height="64" rx="10" stroke="#38bdf8" stroke-width="1.7" />
            <text x="12" y="23" font-size="15">🚢</text>
            <text x="34" y="21" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">OCEAN / PORT (MCP / AIS)</text>
            <text x="12" y="40" class="svg-text-main" font-size="11.5" font-weight="800">${trunc(sys1, 21)}</text>
            <text x="12" y="55" class="svg-text-mono" font-size="9">↳ ${trunc(tbl1, 21)}</text>
          </g>
          <g transform="translate(12, 90)">
            <rect class="svg-node-box" width="180" height="64" rx="10" stroke="#a855f7" stroke-width="1.7" />
            <text x="12" y="23" font-size="15">✈️</text>
            <text x="34" y="21" fill="#c084fc" font-size="9" font-weight="800" font-family="var(--font-mono)">AIR / CARRIER TELEMETRY</text>
            <text x="12" y="40" class="svg-text-main" font-size="11.5" font-weight="800">${trunc(sys2, 21)}</text>
            <text x="12" y="55" class="svg-text-mono" font-size="9">↳ ${trunc(tbl2, 21)}</text>
          </g>
          <g transform="translate(12, 168)">
            <rect class="svg-node-box" width="180" height="64" rx="10" stroke="#f59e0b" stroke-width="1.7" />
            <text x="12" y="23" font-size="15">🚆</text>
            <text x="34" y="21" fill="#fbbf24" font-size="9" font-weight="800" font-family="var(--font-mono)">TMS / RAIL / ON-PREM DB</text>
            <text x="12" y="40" class="svg-text-main" font-size="11.5" font-weight="800">${trunc(sys3, 21)}</text>
            <text x="12" y="55" class="svg-text-mono" font-size="9">↳ ${trunc(tbl3, 21)}</text>
          </g>
          <g transform="translate(12, 246)">
            <rect class="svg-node-box" width="180" height="64" rx="10" stroke="#10b981" stroke-width="1.7" />
            <text x="12" y="23" font-size="15">🗺️</text>
            <text x="34" y="21" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">GEOSPATIAL ROUTING API</text>
            <text x="12" y="40" class="svg-text-main" font-size="11.5" font-weight="800">Live Traffic &amp; ELD HOS</text>
            <text x="12" y="55" class="svg-text-mono" font-size="9">↳ Dynamic ETA Matrix</text>
          </g>

          <!-- Stage 2: Geospatial Corridor Digital Twin (Sub-Agent 1) -->
          <g transform="translate(228, 58)">
            <rect class="svg-node-box-alt" width="180" height="214" rx="14" stroke="#38bdf8" stroke-width="2" />
            <text x="14" y="25" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🗺️ CORRIDOR STATE TWIN</text>
            <text x="14" y="45" class="svg-text-main" font-size="12.5" font-weight="800">${trunc(subs[0].name, 21)}</text>
            <text x="14" y="62" class="svg-text-sub" font-size="10">BigQuery / TMS DB / MCP</text>
            <rect class="svg-pill-bg" x="10" y="76" width="160" height="38" rx="7" stroke="rgba(56,189,248,0.4)" />
            <text x="16" y="92" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🔍 ${trunc(q1, 20)}</text>
            <text x="16" y="106" class="svg-text-mono" font-size="9">Lane ETA &amp; Dwell Matrix</text>
            <rect class="svg-pill-bg" x="10" y="122" width="160" height="38" rx="7" stroke="rgba(56,189,248,0.4)" />
            <text x="16" y="138" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🔍 ${trunc(q2, 20)}</text>
            <text x="16" y="152" class="svg-text-mono" font-size="9">3D Cube, Weight &amp; Stops</text>
            <text x="14" y="190" fill="#10b981" font-size="9.5" font-weight="800" font-family="var(--font-mono)">✓ Multi-Modal Sync</text>
          </g>

          <!-- Stage 3: Geospatial VRP + 3D LIFO Axle-Weight Solver (Sub-Agent 2) -->
          <g transform="translate(440, 24)">
            <rect class="svg-node-box-alt" width="264" height="282" rx="16" stroke="${cls.color}" stroke-width="2.4" />
            <rect x="14" y="12" width="236" height="22" rx="6" fill="${cls.color}26" stroke="${cls.color}" />
            <text x="132" y="27" text-anchor="middle" class="svg-text-main" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🚚 VRP CORRIDOR + 3D LIFO LOAD SOLVER</text>
            <text x="16" y="54" class="svg-text-main" font-size="13.5" font-weight="800">${trunc(subs[1].name, 28)}</text>
            <text x="16" y="71" fill="${cls.color}" font-size="10.5" font-weight="700">${trunc(solverLabel, 33)}</text>

            <g transform="translate(16, 84)">
              <rect class="svg-viz-well" width="232" height="124" rx="10" stroke="#38bdf866" stroke-width="1.2" />
              <path d="M 20 46 Q 68 12, 118 36 T 212 22" fill="none" stroke="#38bdf8" stroke-width="2.2" stroke-dasharray="4 2" />
              <circle cx="20" cy="46" r="5" fill="#f59e0b" />
              <circle cx="118" cy="36" r="5" fill="#38bdf8" />
              <circle cx="212" cy="22" r="5.5" fill="#10b981" />
              <text x="20" y="60" fill="#fbbf24" font-size="8" font-weight="800" font-family="var(--font-mono)">ORIGIN</text>
              <text x="100" y="52" fill="#38bdf8" font-size="8" font-weight="800" font-family="var(--font-mono)">HUB / STOP 1</text>
              <text x="172" y="40" fill="#10b981" font-size="8" font-weight="800" font-family="var(--font-mono)">FINAL DEST</text>

              <rect x="20" y="70" width="154" height="34" rx="4" fill="rgba(15,23,42,0.85)" stroke="#94a3b8" stroke-width="1.4" />
              <rect x="24" y="74" width="34" height="26" rx="2" fill="#10b981" />
              <rect x="62" y="74" width="34" height="26" rx="2" fill="#38bdf8" />
              <rect x="100" y="74" width="34" height="26" rx="2" fill="#fbbf24" />
              <circle cx="42" cy="110" r="5" fill="#64748b" />
              <circle cx="152" cy="110" r="5" fill="#64748b" />
              <text x="180" y="86" fill="#10b981" font-size="8" font-weight="800" font-family="var(--font-mono)">94% CUBE</text>
              <text x="180" y="98" fill="#38bdf8" font-size="8" font-weight="800" font-family="var(--font-mono)">LIFO OK</text>
            </g>

            <text x="16" y="230" class="svg-text-mono" font-size="9.5">• Co-Optimizes Multi-Stop Route + 3D Packing</text>
            <text x="16" y="247" class="svg-text-mono" font-size="9.5">• Balances Drive/Tandem Axle Weights &amp; CG</text>
            <text x="16" y="264" fill="#10b981" font-size="9.5" font-weight="700" font-family="var(--font-mono)">✓ Minimum Landed Cost &amp; CO2e</text>
          </g>

          <!-- Stage 4: DOT Axle-Weight, Crush & HOS Gate (Sub-Agent 3) -->
          <g transform="translate(736, 62)">
            <rect class="svg-node-box" width="160" height="206" rx="14" stroke="#10b981" stroke-width="2" />
            <text x="14" y="25" fill="#10b981" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🛣️ DOT &amp; HOS GATE</text>
            <text x="14" y="45" class="svg-text-main" font-size="12" font-weight="800">${trunc(subs[2].name, 19)}</text>
            <text x="14" y="63" class="svg-text-sub" font-size="9.5">${trunc(subs[2].role, 22)}</text>
            <rect class="svg-pill-bg" x="12" y="80" width="136" height="58" rx="7" stroke="#10b98155" />
            <text x="18" y="98" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">✓ Legal Axle Load &lt; 34k</text>
            <text x="18" y="113" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">✓ Driver HOS Compliant</text>
            <text x="18" y="128" fill="#fbbf24" font-size="9" font-weight="800" font-family="var(--font-mono)">✓ Zero Stack Crush</text>
            <text x="14" y="168" class="svg-text-mono" font-size="9">enforce_tool_contract()</text>
            <text x="14" y="186" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">✓ Manifest Certified</text>
          </g>

          <!-- Stage 5: Open Carrier Tender / TMS Dispatch & Corridor A2UI -->
          <g transform="translate(928, 38)">
            <rect class="svg-node-box-out" width="180" height="114" rx="14" stroke="#10b981" stroke-width="2" />
            <text x="14" y="24" font-size="15">📍</text>
            <text x="36" y="22" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">TMS / CARRIER DISPATCH</text>
            <text x="14" y="42" class="svg-text-main" font-size="11.5" font-weight="800">${writebackLabel}</text>
            <rect class="svg-pill-bg" x="10" y="52" width="160" height="24" rx="5" stroke="#10b98166" />
            <text x="16" y="68" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">⚡ ${trunc(a1, 21)}</text>
            <text x="14" y="96" class="svg-text-mono" font-size="9">TMS / EDI 204 via MCP</text>
          </g>
          <g transform="translate(928, 176)">
            <rect class="svg-node-box" width="180" height="114" rx="14" stroke="#38bdf8" stroke-width="2" />
            <text x="14" y="24" font-size="15">📊</text>
            <text x="36" y="22" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">CORRIDOR A2UI</text>
            <text x="14" y="42" class="svg-text-main" font-size="11.5" font-weight="800">${trunc(ag.badge || ag.outcome, 22)}</text>
            <rect class="svg-pill-bg" x="10" y="52" width="160" height="24" rx="5" stroke="#38bdf866" />
            <text x="16" y="68" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">✦ Route &amp; Load VegaChart</text>
            <text x="14" y="96" class="svg-text-sub" font-size="9.5">${trunc(ag.primaryPersonaName || 'Logistics Lead', 22)}</text>
          </g>
        `;
      }

      // =====================================================================
      // TOPOLOGY 8: 3-BRANCH EXCEPTION TRIAGE, OTIF SHIELD & WAR-ROOM TREE
      // =====================================================================
      return `
        <!-- Disruption / RMA Trigger -> Cross-System Evidence Aggregator -->
        <path d="M 196 165 L 228 165" fill="none" stroke="#f43f5e" stroke-width="2.6" marker-end="url(#arrowAccent_${uid})" />
        <circle r="4" fill="#f43f5e"><animateMotion dur="1.2s" repeatCount="indefinite" path="M 196 165 L 228 165" /></circle>

        <!-- Evidence Aggregator -> 3-Branch Decision Tree Engine -->
        <path d="M 408 165 L 440 165" fill="none" stroke="#38bdf8" stroke-width="2.5" marker-end="url(#arrowCyan_${uid})" />

        <!-- 3-Branch Decision Tree -> Authority Gate -->
        <path d="M 704 115 L 736 140" fill="none" stroke="#10b981" stroke-width="2" />
        <path d="M 704 165 L 736 165" fill="none" stroke="#38bdf8" stroke-width="2.2" />
        <path d="M 704 215 L 736 190" fill="none" stroke="#fbbf24" stroke-width="2" />

        <!-- Authority Gate -> Autonomous Resolution Write-Back -->
        <path d="M 896 135 C 912 135, 912 96, 928 96" fill="none" stroke="#10b981" stroke-width="2.4" marker-end="url(#arrowGreen_${uid})" />
        <path d="M 896 195 C 912 195, 912 234, 928 234" fill="none" stroke="#38bdf8" stroke-width="2.2" marker-end="url(#arrowCyan_${uid})" />

        <!-- Stage 1: High-Priority Exception / RMA / OTIF Trigger (MCP / Webhook / DB) -->
        <g transform="translate(12, 46)">
          <rect class="svg-node-box-warn" width="184" height="238" rx="14" stroke="#f43f5e" stroke-width="2.2" />
          <text x="14" y="28" font-size="18">🚨</text>
          <text x="40" y="26" fill="#fb7185" font-size="9" font-weight="800" font-family="var(--font-mono)">ALERT / RMA (MCP / API)</text>
          <text x="14" y="50" class="svg-text-main" font-size="12.5" font-weight="800">${trunc(sys1, 21)}</text>
          <text x="14" y="68" class="svg-text-mono" font-size="9.5">↳ ${trunc(tbl1, 20)}</text>
          <rect class="svg-pill-bg" x="12" y="84" width="160" height="62" rx="8" stroke="#f43f5e55" />
          <text x="18" y="102" fill="#fbbf24" font-size="9.5" font-weight="800" font-family="var(--font-mono)">+ ${trunc(sys2, 18)}</text>
          <text x="18" y="118" class="svg-text-mono" font-size="9">↳ ${trunc(tbl2, 19)}</text>
          <text x="18" y="134" class="svg-text-mono" font-size="9">+ ${trunc(sys3, 18)}</text>
          <text x="14" y="174" fill="#fb7185" font-size="9.5" font-weight="800" font-family="var(--font-mono)">⏱️ Event Stream / Webhook</text>
          <text x="14" y="194" class="svg-text-sub" font-size="10">On-Prem / Cloud / 3rd-Party</text>
        </g>

        <!-- Stage 2: Cross-System Evidence & Penalty Exposure Aggregator (Sub-Agent 1) -->
        <g transform="translate(228, 54)">
          <rect class="svg-node-box-alt" width="180" height="222" rx="14" stroke="#38bdf8" stroke-width="2" />
          <text x="14" y="26" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🧭 EVIDENCE AGGREGATOR</text>
          <text x="14" y="46" class="svg-text-main" font-size="12.5" font-weight="800">${trunc(subs[0].name, 21)}</text>
          <text x="14" y="64" class="svg-text-sub" font-size="10">BigQuery / On-Prem SQL / MCP</text>
          <rect class="svg-pill-bg" x="12" y="80" width="156" height="40" rx="7" stroke="rgba(56,189,248,0.4)" />
          <text x="18" y="97" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">🔍 ${trunc(q1, 20)}</text>
          <text x="18" y="111" class="svg-text-mono" font-size="8.5">Computes Value-at-Risk ($)</text>
          <rect class="svg-pill-bg" x="12" y="128" width="156" height="40" rx="7" stroke="rgba(56,189,248,0.4)" />
          <text x="18" y="145" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">🔍 ${trunc(q2, 20)}</text>
          <text x="18" y="159" class="svg-text-mono" font-size="8.5">Pulls SLA / POD / Lot Proof</text>
          <text x="14" y="196" fill="#10b981" font-size="9.5" font-weight="800" font-family="var(--font-mono)">✓ ${tablesCount} BQ / SQL Tables</text>
        </g>

        <!-- Stage 3: 3-Branch Decision Tree Engine (Sub-Agent 2) -->
        <g transform="translate(440, 22)">
          <rect class="svg-node-box-alt" width="264" height="286" rx="16" stroke="${cls.color}" stroke-width="2.4" />
          <rect x="14" y="12" width="236" height="22" rx="6" fill="${cls.color}26" stroke="${cls.color}" />
          <text x="132" y="27" text-anchor="middle" class="svg-text-main" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🔀 3-PATH TRIAGE &amp; RESOLUTION TREE</text>
          <text x="16" y="54" class="svg-text-main" font-size="13.5" font-weight="800">${trunc(subs[1].name, 28)}</text>
          <text x="16" y="71" fill="${cls.color}" font-size="10.5" font-weight="700">${trunc(solverLabel, 33)}</text>

          <g transform="translate(16, 82)">
            <rect class="svg-viz-well" width="232" height="134" rx="10" stroke="#fb718566" stroke-width="1.2" />
            <path d="M 32 67 L 78 26 M 32 67 L 78 67 M 32 67 L 78 108" stroke="#94a3b8" stroke-width="2" />
            <circle cx="32" cy="67" r="12" fill="#f43f5e" />
            <text x="32" y="70" text-anchor="middle" fill="#ffffff" font-size="8" font-weight="800">ROI</text>

            <rect x="78" y="10" width="142" height="32" rx="6" fill="rgba(16,185,129,0.16)" stroke="#10b981" stroke-width="1.4" />
            <text x="86" y="24" fill="#10b981" font-size="8.5" font-weight="800" font-family="var(--font-mono)">PATH A · RE-ROUTE / REFURB</text>
            <text x="86" y="36" class="svg-text-mono" font-size="8">Highest Net Value Recovery</text>

            <rect x="78" y="51" width="142" height="32" rx="6" fill="rgba(56,189,248,0.16)" stroke="#38bdf8" stroke-width="1.4" />
            <text x="86" y="65" fill="#38bdf8" font-size="8.5" font-weight="800" font-family="var(--font-mono)">PATH B · SPLIT-SHIP / KEEP-IT</text>
            <text x="86" y="77" class="svg-text-mono" font-size="8">Avoids Penalty / Return Cost</text>

            <rect x="78" y="92" width="142" height="32" rx="6" fill="rgba(245,158,11,0.16)" stroke="#f59e0b" stroke-width="1.4" />
            <text x="86" y="106" fill="#fbbf24" font-size="8.5" font-weight="800" font-family="var(--font-mono)">PATH C · CLAIM / WAR-ROOM</text>
            <text x="86" y="118" class="svg-text-mono" font-size="8">Full Evidence Dossier + HITL</text>
          </g>

          <text x="16" y="236" class="svg-text-mono" font-size="9.5">• Ranks Paths by Net P&amp;L &amp; SLA Protection</text>
          <text x="16" y="254" fill="#10b981" font-size="9.5" font-weight="700" font-family="var(--font-mono)">✓ Deterministic Disposition Selected</text>
        </g>

        <!-- Stage 4: Financial Authority & Fraud Gate (Sub-Agent 3) -->
        <g transform="translate(736, 62)">
          <rect class="svg-node-box" width="160" height="206" rx="14" stroke="#f59e0b" stroke-width="2" />
          <text x="14" y="25" fill="#fbbf24" font-size="9.5" font-weight="800" font-family="var(--font-mono)">🛡️ AUTHORITY GATE</text>
          <text x="14" y="45" class="svg-text-main" font-size="12" font-weight="800">${trunc(subs[2].name, 19)}</text>
          <text x="14" y="63" class="svg-text-sub" font-size="9.5">${trunc(subs[2].role, 22)}</text>
          <rect class="svg-pill-bg" x="12" y="80" width="136" height="58" rx="7" stroke="#f59e0b55" />
          <text x="18" y="98" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">✓ Auto-Approve &lt; Limit</text>
          <text x="18" y="113" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">✓ Fraud Score Verified</text>
          <text x="18" y="128" fill="#fbbf24" font-size="9" font-weight="800" font-family="var(--font-mono)">✓ Executive War-Room</text>
          <text x="14" y="168" class="svg-text-mono" font-size="9">enforce_tool_contract()</text>
          <text x="14" y="186" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">✓ Signed Resolution</text>
        </g>

        <!-- Stage 5: Open MCP / API / On-Prem Resolution Commit & War-Room A2UI -->
        <g transform="translate(928, 38)">
          <rect class="svg-node-box-out" width="180" height="114" rx="14" stroke="#10b981" stroke-width="2" />
          <text x="14" y="24" font-size="15">⚡</text>
          <text x="36" y="22" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">MCP / API / ERP COMMIT</text>
          <text x="14" y="42" class="svg-text-main" font-size="11.5" font-weight="800">${writebackLabel}</text>
          <rect class="svg-pill-bg" x="10" y="52" width="160" height="24" rx="5" stroke="#10b98166" />
          <text x="16" y="68" fill="#10b981" font-size="9" font-weight="800" font-family="var(--font-mono)">⚡ ${trunc(a1, 21)}</text>
          <text x="14" y="96" class="svg-text-mono" font-size="9">ERP / WMS / Carrier MCP</text>
        </g>
        <g transform="translate(928, 176)">
          <rect class="svg-node-box" width="180" height="114" rx="14" stroke="#38bdf8" stroke-width="2" />
          <text x="14" y="24" font-size="15">📊</text>
          <text x="36" y="22" fill="#38bdf8" font-size="9.5" font-weight="800" font-family="var(--font-mono)">TRIAGE A2UI SURFACE</text>
          <text x="14" y="42" class="svg-text-main" font-size="11.5" font-weight="800">${trunc(ag.badge || ag.outcome, 22)}</text>
          <rect class="svg-pill-bg" x="10" y="52" width="160" height="24" rx="5" stroke="#38bdf866" />
          <text x="16" y="68" fill="#38bdf8" font-size="9" font-weight="800" font-family="var(--font-mono)">✦ Decision VegaChart</text>
          <text x="14" y="96" class="svg-text-sub" font-size="9.5">${trunc(ag.primaryPersonaName || 'CSCO / Ops Lead', 22)}</text>
        </g>
      `;
    }

    function renderSimpleAgentArchitectureDiagram(ag, dept) {
      const adk = ag.adkImplementation || {};
      const spec = ag.adkSpec || {};
      const cls = getAgentBuildClassification(ag);
      const cleanName = cleanAgentName(ag.name);
      const topology = AGENT_TOPOLOGY_MAP[ag.id] || 'milp_pareto_loop';
      const tMeta = TOPOLOGY_META[topology] || TOPOLOGY_META.milp_pareto_loop;

      const trunc = (str, max = 24) => {
        const s = String(str || '').trim();
        return s.length > max ? s.slice(0, max - 1) + '…' : s;
      };

      // 1. Open, Technology-First Connected Systems (MCPs, On-Prem DBs, BigQuery, REST/EDI)
      const rawSysArr = (spec.systems && spec.systems.length)
        ? spec.systems.map(s => s.name)
        : toSysArray(ag.systems);
      const sysArr = rawSysArr.map(s => toOpenTechLabel(s));
      const sys1 = sysArr[0] || 'Enterprise ERP (MCP / On-Prem DB)';
      const sys2 = sysArr[1] || 'BigQuery / Analytical Data Warehouse';
      const sys3 = sysArr[2] || '3rd-Party SaaS MCP & EDI Streams';
      const ic1 = pickSystemIcon(sys1);
      const ic2 = pickSystemIcon(sys2);
      const ic3 = pickSystemIcon(sys3);

      // 2. Real Fixture Tables & Query/Action Tools for this agent
      const tables = (adk.fixtureTables || []).map(t => t.table_name);
      const tbl1 = tables[0] || 'primary_twin_ledger';
      const tbl2 = tables[1] || tables[0] || 'signal_telemetry';
      const tbl3 = tables[2] || tables[1] || 'constraint_audit';

      const rawTools = (spec.toolsMeta && spec.toolsMeta.length)
        ? spec.toolsMeta.map(t => t.name)
        : (adk.tools || []).filter(t => t !== 'list_systems');
      const qTools = rawTools.filter(t => !String(t).startsWith('action_'));
      const aTools = rawTools.filter(t => String(t).startsWith('action_'));
      const q1 = qTools[0] || 'query_domain_signals';
      const q2 = qTools[1] || qTools[0] || 'query_twin_constraints';
      const a1 = aTools[0] || 'action_commit_writeback';

      // 3. Real 3 A2A Sub-Agents for this agent (cleaned of vendor lock-in names)
      const rawSubs = (ag.subAgents && ag.subAgents.length >= 3)
        ? ag.subAgents.slice(0, 3)
        : [
            { name: 'Signal Ingestion & Context Node', role: 'Streams & validates live operational inputs' },
            { name: 'Scenario & Optimization Engine', role: 'Evaluates constraints & ranks actions' },
            { name: 'Exception & Write-Back Dispatcher', role: 'Enforces quality gates & signed payloads' }
          ];
      const subs = rawSubs.map(sa => ({
        name: toOpenTechLabel(sa.name),
        role: toOpenTechLabel(sa.role)
      }));

      const cadence = (ag.costModel && ag.costModel.triggerCadence) || 'Event-Driven + 15-Min Telemetry';
      const solverLabel = toOpenTechLabel(ag.solverStack || 'Time-Series & Mathematical Optimization Engine');
      const writebackFull = toOpenTechLabel(ag.apiWriteback || 'Enterprise ERP / WMS Write-Back via MCP or REST');
      const writebackLabel = trunc(writebackFull, 24);

      const svgBody = renderFullTopologySvg(topology, {
        ag, dept, cls, cleanName, trunc,
        sys1, sys2, sys3, ic1, ic2, ic3,
        tbl1, tbl2, tbl3, tablesCount: tables.length || 4,
        q1, q2, a1, subs, solverLabel, writebackLabel
      });

      return `
        <div class="simple-arch-card">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:14px;">
            <div>
              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:4px;">
                <span style="font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color};">
                  ${tMeta.badge}
                </span>
                <span class="sc-spec-count-badge" style="font-size:11px;">
                  ⏱️ ${cadence}
                </span>
              </div>
              <h2 style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary); margin:0;">
                How ${cleanName} Works — Open Technology &amp; Execution Flow
              </h2>
            </div>

            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="sc-spec-count-badge" style="color:#10b981; border-color:rgba(16,185,129,0.35);">
                🔌 Pluggable: BigQuery · On-Prem DBs · 3rd-Party MCPs · REST/EDI
              </span>
              <span class="sc-spec-count-badge" style="color:${dept.color}; border-color:${dept.color}44;">
                🧠 Gemini 3.8 Flash ↔ 3.1 Pro / 4 Argon
              </span>
            </div>
          </div>

          <!-- Custom Agent-Specific Animated Full-Canvas SVG Flow Diagram -->
          <div class="ag-flow-canvas-wrap">
            <svg class="ag-flow-svg" viewBox="0 0 1120 326">
              <defs>
                <marker id="arrowAccent_${ag.id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 1 L 10 5 L 0 9 z" fill="${dept.color}" />
                </marker>
                <marker id="arrowGreen_${ag.id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 1 L 10 5 L 0 9 z" fill="#10b981" />
                </marker>
                <marker id="arrowCyan_${ag.id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8" />
                </marker>
              </defs>
              ${svgBody}
            </svg>
          </div>

          <!-- 5-Stage Agent-Specific Meaningful Step Cards (Technology-First & Open Integration) -->
          <div class="ag-flow-steps-grid">
            <div class="ag-flow-step-card" style="--step-accent:${dept.color};">
              <div>
                <div class="ag-flow-step-head">
                  <div class="ag-flow-step-icon">${ic1}</div>
                  <div>
                    <div class="ag-flow-step-kicker">${tMeta.stageLabels[0]}</div>
                    <div class="ag-flow-step-title">Open Source Connectors</div>
                  </div>
                </div>
                <p class="ag-flow-step-desc" style="margin-top:8px;">
                  Connects via <strong>MCP servers, REST/EDI, or On-Prem DB adapters</strong> to <strong>${sys1}</strong>, <strong>${sys2}</strong>, and <strong>${sys3}</strong>.
                </p>
              </div>
              <div class="ag-flow-step-chips">
                ${sysArr.slice(0, 3).map(s => `<span class="ag-flow-mini-chip">${pickSystemIcon(s)} ${trunc(s, 20)}</span>`).join('')}
              </div>
            </div>

            <div class="ag-flow-step-card" style="--step-accent:#38bdf8;">
              <div>
                <div class="ag-flow-step-head">
                  <div class="ag-flow-step-icon">${tMeta.icons[1]}</div>
                  <div>
                    <div class="ag-flow-step-kicker">${tMeta.stageLabels[1]}</div>
                    <div class="ag-flow-step-title">${subs[0].name}</div>
                  </div>
                </div>
                <p class="ag-flow-step-desc" style="margin-top:8px;">
                  ${subs[0].role}. Queries <strong>${tables.length || 4} domain tables</strong> across BigQuery, On-Prem SQL, or customer data lakes.
                </p>
              </div>
              <div class="ag-flow-step-chips">
                ${qTools.slice(0, 3).map(qt => `<span class="ag-flow-mini-chip">🔍 ${qt}</span>`).join('')}
              </div>
            </div>

            <div class="ag-flow-step-card" style="--step-accent:${cls.color};">
              <div>
                <div class="ag-flow-step-head">
                  <div class="ag-flow-step-icon">${tMeta.icons[2]}</div>
                  <div>
                    <div class="ag-flow-step-kicker">${tMeta.stageLabels[2]}</div>
                    <div class="ag-flow-step-title">${subs[1].name}</div>
                  </div>
                </div>
                <p class="ag-flow-step-desc" style="margin-top:8px;">
                  ${subs[1].role} powered by <strong>${solverLabel}</strong>.
                </p>
              </div>
              <div class="ag-flow-step-chips">
                <span class="ag-flow-mini-chip">⚡ gemini-3.8-flash</span>
                <span class="ag-flow-mini-chip">🧠 gemini-3.1-pro / 4-argon</span>
              </div>
            </div>

            <div class="ag-flow-step-card" style="--step-accent:#f59e0b;">
              <div>
                <div class="ag-flow-step-head">
                  <div class="ag-flow-step-icon">${tMeta.icons[3]}</div>
                  <div>
                    <div class="ag-flow-step-kicker">${tMeta.stageLabels[3]}</div>
                    <div class="ag-flow-step-title">${subs[2].name}</div>
                  </div>
                </div>
                <p class="ag-flow-step-desc" style="margin-top:8px;">
                  ${subs[2].role}. Enforces pre-execution <code style="font-family:var(--font-mono); font-size:11px;">enforce_tool_contract()</code> &amp; idempotency.
                </p>
              </div>
              <div class="ag-flow-step-chips">
                <span class="ag-flow-mini-chip">🛡️ idempotency_key</span>
                <span class="ag-flow-mini-chip">👤 HITL Escalation Gate</span>
              </div>
            </div>

            <div class="ag-flow-step-card" style="--step-accent:#10b981;">
              <div>
                <div class="ag-flow-step-head">
                  <div class="ag-flow-step-icon">${tMeta.icons[4]}</div>
                  <div>
                    <div class="ag-flow-step-kicker">${tMeta.stageLabels[4]}</div>
                    <div class="ag-flow-step-title">MCP / API Write-Back</div>
                  </div>
                </div>
                <p class="ag-flow-step-desc" style="margin-top:8px;">
                  Commits signed action via <strong>${writebackFull}</strong> (MCP, REST API, or On-Prem connector) and renders the A2UI <code style="font-family:var(--font-mono); font-size:11px;">VegaChart</code>.
                </p>
              </div>
              <div class="ag-flow-step-chips">
                ${aTools.slice(0, 2).map(at => `<span class="ag-flow-mini-chip">⚡ ${at}</span>`).join('')}
                <span class="ag-flow-mini-chip">📊 ${trunc(ag.badge || 'KPI Impact', 20)}</span>
              </div>
            </div>
          </div>
        </div>
      `;
    }
"""


def update_file(path: Path):
    text = path.read_text(encoding="utf-8")

    # 1. Inject or update FLOW_CSS before </style>
    if ".ag-flow-canvas-wrap {" not in text:
        text = text.replace("  </style>", FLOW_CSS + "\n  </style>", 1)

    # 2. Replace from AGENT_TOPOLOGY_MAP (or renderSimpleAgentArchitectureDiagram) to SIMPLE AGENT COST DETAILS CARD
    start_marker = "const AGENT_TOPOLOGY_MAP ="
    if start_marker not in text:
        start_marker = "function renderSimpleAgentArchitectureDiagram(ag, dept) {"
    end_marker = "/* =========================================================================\n       SIMPLE AGENT COST DETAILS CARD"
    s_idx = text.find(start_marker)
    e_idx = text.find(end_marker)
    if s_idx == -1 or e_idx == -1 or e_idx <= s_idx:
        raise RuntimeError(f"Could not locate renderSimpleAgentArchitectureDiagram bounds in {path} (s={s_idx}, e={e_idx})")

    text = text[:s_idx] + NEW_ARCH_DIAGRAM_JS.strip() + "\n\n    " + text[e_idx:]
    path.write_text(text, encoding="utf-8")
    print(f"Updated {path} ({len(text.splitlines())} lines)")


def main():
    for name in ("index.html", "periodic_table.html", "mind_map.html"):
        p = ROOT / name
        if p.exists():
            update_file(p)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Incorporates the 'AI in Supply Chain Function' 4-Layer Operating Model Stack
(mirroring the executive 'AI in Finance Function' reference pattern):
  - Coral-Red Dashed Agentic Transformation Zone enclosing:
      1. Top Layer (Blue): Executive Steering & Network Capital Allocation (4 tiles)
      2. Service Delivery Layer (Purple): Transactional, Technical, Embedded Plant/DC/Field Copilots (3 tiles)
  - Underlying Enterprise Foundation & Real-Time Signals:
      3. Core Apps (Green): Central ERP & Planning Hub, WMS/TMS, Master Data Governance (MDG), Supplier/Trade/QMS (4 tiles)
      4. Operational Inputs (Amber): POS & Demand Signals, Bills of Materials (BOM), Order & Stock Ledgers,
         Machine Run Hours & OEE, Supplier Delivery & ASN, IIoT / Cold-Chain & GPS (6 tiles)

Rendered cleanly (zero clutter inside tiles, matching the executive slide aesthetic) with:
  - Interactive click-to-inspect drawer underneath mapping every tile to live Supply Chain AI Agents
  - Placed on #pageHome (directly below the 6 Core Operating Pillars) AND as the hero visual of #architecture
  - Quick-jump 'AI Stack' pill added to the top navigation bar across index.html, periodic_table.html, and mind_map.html
  - Full Dark Mode + Light Mode (html[data-theme="light"]) support
"""

from __future__ import annotations

import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HTML_FILES = [
    ROOT / "index.html",
    ROOT / "periodic_table.html",
    ROOT / "mind_map.html",
]

AI_FN_STACK_CSS = """
    /* =========================================================================
       AI IN SUPPLY CHAIN FUNCTION — 4-LAYER EXECUTIVE OPERATING MODEL STACK
       ========================================================================= */
    .sc-fn-stack-wrap {
      width: 100%;
      background: #0c0f17;
      border: 1px solid rgba(148, 163, 184, 0.18);
      border-radius: 28px;
      padding: 34px 36px 36px;
      box-shadow: 0 26px 64px rgba(0, 0, 0, 0.48);
      position: relative;
      overflow: hidden;
    }
    .sc-fn-stack-header {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 14px;
      margin-bottom: 24px;
    }
    .sc-fn-stack-title {
      font-family: var(--font-display);
      font-size: clamp(28px, 3vw, 40px);
      font-weight: 800;
      color: #ffffff;
      letter-spacing: -0.02em;
      margin: 0;
      line-height: 1.15;
    }
    .sc-fn-stack-hint {
      font-family: var(--font-sans);
      font-size: 13px;
      font-weight: 600;
      color: #94a3b8;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      border-radius: 999px;
      background: rgba(30, 41, 59, 0.55);
      border: 1px solid rgba(148, 163, 184, 0.2);
    }
    .sc-fn-dashed-agentic-zone {
      position: relative;
      border: 3px dashed #ef533f;
      border-radius: 30px;
      padding: 22px 20px 20px;
      margin-bottom: 18px;
      background: radial-gradient(ellipse at 50% 0%, rgba(239, 83, 63, 0.055), rgba(15, 23, 42, 0.0) 70%);
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .sc-fn-zone-badge {
      position: absolute;
      top: -13px;
      right: 28px;
      background: #131722;
      color: #ff7b6b;
      border: 1.5px solid rgba(239, 83, 63, 0.65);
      border-radius: 999px;
      padding: 3px 14px;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.07em;
      text-transform: uppercase;
    }
    .sc-fn-foundation-rows {
      display: flex;
      flex-direction: column;
      gap: 16px;
      padding: 0 20px;
    }
    .sc-fn-row {
      display: grid;
      grid-template-columns: 246px minmax(0, 1fr);
      gap: 16px;
      align-items: stretch;
    }
    .sc-fn-layer-head {
      border-radius: 16px;
      padding: 22px 20px 22px 22px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 6px;
      min-height: 112px;
      position: relative;
    }
    .sc-fn-layer-head-title {
      font-family: var(--font-display);
      font-size: 21px;
      font-weight: 700;
      line-height: 1.22;
      letter-spacing: -0.01em;
    }
    .sc-fn-layer-head-sub {
      font-family: var(--font-sans);
      font-size: 13.5px;
      font-weight: 500;
      line-height: 1.42;
      color: #cbd5e1;
    }
    .sc-fn-layer-head.layer-blue {
      background: linear-gradient(135deg, rgba(29, 78, 216, 0.28) 0%, rgba(17, 24, 39, 0.95) 100%);
      border: 1.5px solid rgba(59, 130, 246, 0.68);
      border-left: 7px solid #3b82f6;
    }
    .sc-fn-layer-head.layer-blue .sc-fn-layer-head-title { color: #60a5fa; }

    .sc-fn-layer-head.layer-purple {
      background: linear-gradient(135deg, rgba(126, 34, 206, 0.28) 0%, rgba(22, 16, 36, 0.95) 100%);
      border: 1.5px solid rgba(168, 85, 247, 0.68);
      border-left: 7px solid #a855f7;
    }
    .sc-fn-layer-head.layer-purple .sc-fn-layer-head-title { color: #c084fc; }

    .sc-fn-layer-head.layer-green {
      background: linear-gradient(135deg, rgba(5, 150, 105, 0.28) 0%, rgba(12, 26, 22, 0.95) 100%);
      border: 1.5px solid rgba(16, 185, 129, 0.68);
      border-left: 7px solid #10b981;
    }
    .sc-fn-layer-head.layer-green .sc-fn-layer-head-title { color: #34d399; }

    .sc-fn-layer-head.layer-amber {
      background: linear-gradient(135deg, rgba(180, 83, 9, 0.28) 0%, rgba(27, 20, 12, 0.95) 100%);
      border: 1.5px solid rgba(245, 158, 11, 0.68);
      border-left: 7px solid #f59e0b;
    }
    .sc-fn-layer-head.layer-amber .sc-fn-layer-head-title { color: #fbbf24; }

    .sc-fn-tiles-grid {
      display: grid;
      gap: 16px;
      align-items: stretch;
    }
    .sc-fn-tiles-grid.cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
    .sc-fn-tiles-grid.cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .sc-fn-tiles-grid.cols-6 { grid-template-columns: repeat(6, minmax(0, 1fr)); }

    .sc-fn-tile {
      background: #171a21;
      border: 1px solid rgba(255, 255, 255, 0.11);
      border-radius: 16px;
      padding: 20px 18px;
      min-height: 112px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      gap: 6px;
      cursor: pointer;
      transition: transform 0.22s cubic-bezier(0.22, 1, 0.36, 1), border-color 0.22s ease, background 0.22s ease, box-shadow 0.22s ease;
      user-select: none;
    }
    .sc-fn-tile:hover {
      transform: translateY(-4px);
      background: #1e2330;
      border-color: var(--tile-accent, rgba(96, 165, 250, 0.65));
      box-shadow: 0 14px 30px rgba(0, 0, 0, 0.42), 0 0 0 1px var(--tile-accent, rgba(96, 165, 250, 0.35));
    }
    .sc-fn-tile.is-selected {
      background: #1f2637;
      border-color: var(--tile-accent, #60a5fa);
      box-shadow: 0 0 0 2px var(--tile-accent, #60a5fa), 0 14px 32px rgba(0, 0, 0, 0.45);
    }
    .sc-fn-tile-title {
      font-family: var(--font-display);
      font-size: 16.5px;
      font-weight: 600;
      color: #f8fafc;
      line-height: 1.32;
      letter-spacing: -0.01em;
    }
    .sc-fn-tiles-grid.cols-6 .sc-fn-tile {
      padding: 16px 12px;
      min-height: 102px;
    }
    .sc-fn-tiles-grid.cols-6 .sc-fn-tile-title {
      font-size: 15px;
    }
    .sc-fn-tile-sub {
      font-family: var(--font-sans);
      font-size: 13px;
      font-weight: 400;
      color: #94a3b8;
      line-height: 1.38;
    }

    /* Slide-down Interactive Inspector Below the 4-Layer Stack */
    .sc-fn-inspector {
      margin-top: 22px;
      padding: 22px 26px;
      border-radius: 20px;
      background: rgba(15, 23, 42, 0.92);
      border: 1.5px solid rgba(96, 165, 250, 0.38);
      animation: dropdownUnroll 0.26s cubic-bezier(0.22, 1, 0.36, 1);
    }
    .sc-fn-inspector-top {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 14px;
    }
    .sc-fn-inspector-agents {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 12px;
      margin-top: 14px;
    }
    .sc-fn-agent-link-chip {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 12px 15px;
      border-radius: 14px;
      background: rgba(30, 41, 59, 0.72);
      border: 1px solid rgba(148, 163, 184, 0.22);
      cursor: pointer;
      text-align: left;
      transition: all 0.18s ease;
    }
    .sc-fn-agent-link-chip:hover {
      transform: translateY(-2px);
      border-color: #38bdf8;
      background: rgba(30, 41, 59, 0.98);
    }

    /* Light Theme Support for AI in Supply Chain Function Stack */
    html[data-theme="light"] .sc-fn-stack-wrap {
      background: #ffffff;
      border-color: #d2e3fc;
      box-shadow: 0 18px 44px rgba(26, 115, 232, 0.08);
    }
    html[data-theme="light"] .sc-fn-stack-title {
      color: #0f172a;
    }
    html[data-theme="light"] .sc-fn-stack-hint {
      background: #f1f5f9;
      border-color: #cbd5e1;
      color: #334155;
    }
    html[data-theme="light"] .sc-fn-dashed-agentic-zone {
      border-color: #e53935;
      background: rgba(229, 57, 53, 0.025);
    }
    html[data-theme="light"] .sc-fn-zone-badge {
      background: #ffffff;
      color: #d93025;
      border-color: rgba(217, 48, 37, 0.55);
    }
    html[data-theme="light"] .sc-fn-layer-head.layer-blue {
      background: linear-gradient(135deg, #e8f0fe 0%, #f8fbff 100%);
      border-color: #93c5fd;
      border-left: 7px solid #2563eb;
    }
    html[data-theme="light"] .sc-fn-layer-head.layer-blue .sc-fn-layer-head-title { color: #1d4ed8; }
    html[data-theme="light"] .sc-fn-layer-head.layer-purple {
      background: linear-gradient(135deg, #f3e8ff 0%, #fcfaff 100%);
      border-color: #d8b4fe;
      border-left: 7px solid #9333ea;
    }
    html[data-theme="light"] .sc-fn-layer-head.layer-purple .sc-fn-layer-head-title { color: #7e22ce; }
    html[data-theme="light"] .sc-fn-layer-head.layer-green {
      background: linear-gradient(135deg, #dcfce7 0%, #f7fee7 100%);
      border-color: #86efac;
      border-left: 7px solid #059669;
    }
    html[data-theme="light"] .sc-fn-layer-head.layer-green .sc-fn-layer-head-title { color: #047857; }
    html[data-theme="light"] .sc-fn-layer-head.layer-amber {
      background: linear-gradient(135deg, #fef3c7 0%, #fffbeb 100%);
      border-color: #fcd34d;
      border-left: 7px solid #d97706;
    }
    html[data-theme="light"] .sc-fn-layer-head.layer-amber .sc-fn-layer-head-title { color: #b45309; }
    html[data-theme="light"] .sc-fn-layer-head-sub {
      color: #334155;
    }
    html[data-theme="light"] .sc-fn-tile {
      background: #f8fafc;
      border-color: #cbd5e1;
    }
    html[data-theme="light"] .sc-fn-tile:hover,
    html[data-theme="light"] .sc-fn-tile.is-selected {
      background: #ffffff;
      box-shadow: 0 10px 26px rgba(15, 23, 42, 0.09), 0 0 0 1.5px var(--tile-accent, #2563eb);
    }
    html[data-theme="light"] .sc-fn-tile-title {
      color: #0f172a;
    }
    html[data-theme="light"] .sc-fn-tile-sub {
      color: #475569;
    }
    html[data-theme="light"] .sc-fn-inspector {
      background: #f8fafc;
      border-color: #93c5fd;
    }
    html[data-theme="light"] .sc-fn-agent-link-chip {
      background: #ffffff;
      border-color: #cbd5e1;
    }

    @media (max-width: 1120px) {
      .sc-fn-row {
        grid-template-columns: 1fr;
      }
      .sc-fn-layer-head {
        min-height: auto;
        padding: 16px 20px;
      }
      .sc-fn-tiles-grid.cols-4 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .sc-fn-tiles-grid.cols-3 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
      .sc-fn-tiles-grid.cols-6 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    }
    @media (max-width: 640px) {
      .sc-fn-stack-wrap { padding: 22px 16px; }
      .sc-fn-dashed-agentic-zone { padding: 18px 12px 14px; }
      .sc-fn-foundation-rows { padding: 0 4px; }
      .sc-fn-tiles-grid.cols-4,
      .sc-fn-tiles-grid.cols-6 { grid-template-columns: 1fr; }
    }
"""

AI_FN_STACK_JS = """
    /* =========================================================================
       AI IN SUPPLY CHAIN FUNCTION — 4-LAYER OPERATING MODEL DATA & RENDERER
       ========================================================================= */
    const SC_AI_FUNCTION_TILES = {
      top_profitability: {
        layer: 'Top Layer · Executive Steering',
        accent: '#3b82f6',
        title: 'Predictive Cost-to-Serve & Margin',
        sub: '',
        summary: 'Continuously calculates true net profitability across channels, pack formats, and promotions after accounting for warehousing, pick-pack handling, freight, deductions, and returns.',
        agentIds: ['network_twin_architect', 'promo_lift_simulator', 'trade_scheme_claims_reconciler', 'tariff_esg_agent']
      },
      top_rolling_sop: {
        layer: 'Top Layer · Executive Steering',
        accent: '#3b82f6',
        title: 'Dynamic Rolling S&OP Forecasts',
        sub: '',
        summary: 'Replaces static monthly spreadsheets with continuous demand sensing, retail Point of Sale (POS) harmonization, launch analog modeling, and profit-optimal Sales & Operations Planning (S&OP) trade-offs.',
        agentIds: ['demand_sensing_agent', 'sop_scenario_weaver', 'cpfr_sync_agent', 'npi_demand_profiler']
      },
      top_working_capital: {
        layer: 'Top Layer · Executive Steering',
        accent: '#3b82f6',
        title: 'Multi-Echelon Working Capital (MEIO)',
        sub: '',
        summary: 'Right-sizes inventory buffers across plants, distribution centers, and stores while unlocking cash trapped in slow-moving stock and underperforming tail items.',
        agentIds: ['meio_safety_stock_agent', 'working_capital_cash_bridge', 'slob_disposition_agent', 'crossdock_transfer_orchestrator']
      },
      top_capex_warroom: {
        layer: 'Top Layer · Executive Steering',
        accent: '#3b82f6',
        title: 'Portfolio CapEx & Network Risk Allocation',
        sub: '',
        summary: 'Steers multi-year factory capital investments, internal-versus-co-packer volume splits, and executive disruption war-room recovery plans to protect customer service and return on capital.',
        agentIds: ['csco_control_tower_copilot', 'disruption_war_room_orchestrator', 'capex_simulator_agent', 'copacker_allocation_agent']
      },
      svc_transactional: {
        layer: 'Service Delivery Layer · Autonomous Workflows',
        accent: '#a855f7',
        title: 'Transactional',
        sub: '(S2P, O2D, R2R)',
        summary: 'Automates high-volume transactional execution across Source-to-Pay (3-way match, PO expediting), Order-to-Delivery (omnichannel order promising, freight bill audit), and Returns-to-Recovery (RMA fraud & claims).',
        agentIds: ['three_way_match_dispute', 'master_data_leadtime_steward', 'atp_order_promising_agent', 'freight_bill_audit_agent', 'reverse_rma_optimizer', 'osd_freight_claims_agent']
      },
      svc_technical: {
        layer: 'Service Delivery Layer · Specialist Optimization',
        accent: '#a855f7',
        title: 'Technical',
        sub: '(Should-Cost, Solvers, Trade & ESG)',
        summary: 'Runs mathematical optimization solvers, parametric should-cost models, commodity hedging analytics, 3D trailer load consolidation, dynamic route optimization, and Scope 3 carbon accounting.',
        agentIds: ['rfq_should_cost_agent', 'commodity_index_advisor', 'finite_production_scheduler', 'load_consolidation_agent', 'fleetflow_dispatch', 'carbon_scope3_ledger']
      },
      svc_embedded: {
        layer: 'Service Delivery Layer · Embedded Copilots',
        accent: '#a855f7',
        title: 'Embedded Plant, DC & Field Partners',
        sub: '',
        summary: 'Equips plant managers, warehouse supervisors, quality leads, and retail replenishment teams with real-time floor copilots for bottleneck diagnostics, 3D slotting, cold-chain release, and curfew-safe dispatch.',
        agentIds: ['predictive_oee_sentinel', 'inline_yield_guardian', 'warehouse_slotting_agent', 'wave_fulfillment_copilot', 'cold_chain_auditor', 'port_drayage_orchestrator']
      },
      core_erp_hub: {
        layer: 'Core Apps · Systems of Record',
        accent: '#10b981',
        title: 'Central ERP & Planning Hub',
        sub: '(e.g., SAP S/4HANA / Oracle / IBP)',
        summary: 'Core transactional system of record for purchase orders, production orders, financial ledgers, and baseline supply plans—augmented via governed read/write APIs and Model Context Protocol (MCP) connectors without rip-and-replace.',
        agentIds: ['sop_scenario_weaver', 'three_way_match_dispute', 'eco_cutover_orchestrator']
      },
      core_wms_tms: {
        layer: 'Core Apps · Execution Engines',
        accent: '#10b981',
        title: 'Warehouse & Transport Engines',
        sub: '(Enterprise WMS, Yard & TMS)',
        summary: 'Executes physical bin putaway, wave picking, dock door scheduling, carrier load tendering, and shipment tracking fed by AI slotting, wave, and consolidation directives.',
        agentIds: ['warehouse_slotting_agent', 'dock_to_stock_agent', 'yard_dock_sequencer', 'freight_control_tower']
      },
      core_mdg: {
        layer: 'Core Apps · Master Data Foundation',
        accent: '#10b981',
        title: 'Master Data Governance (MDG)',
        sub: '(Item, BOM, Vendor & Lead-Time)',
        summary: 'Maintains governed item hierarchies, multi-tier Bills of Materials (BOM), supplier lead-time distributions, packaging specs, and verified rooftop delivery coordinates.',
        agentIds: ['master_data_leadtime_steward', 'sustainable_packaging_agent', 'geocoding_intelligence_agent']
      },
      core_portals: {
        layer: 'Core Apps · Partner & Quality Systems',
        accent: '#10b981',
        title: 'Automated Quality & Trade Portals',
        sub: '(e.g., Ariba, EDI Gateways, QMS)',
        summary: 'Connects external supplier portals, Electronic Data Interchange (EDI 856/210) feeds, electronic batch records, and returnable transport asset ledgers.',
        agentIds: ['supplier_quality_sentinel', 'batch_record_auditor', 'rti_balance_reconciler']
      },
      inp_pos: {
        layer: 'Operational Inputs · Demand Telemetry',
        accent: '#f59e0b',
        title: 'POS & Demand Signals',
        sub: '',
        summary: 'Daily retail checkout scans, distributor sell-through, weather shifts, and store shelf phantom-inventory signals feeding demand sensing and markdown models.',
        agentIds: ['demand_sensing_agent', 'planogram_merchandising_vision_auditor', 'dynamic_markdown_agent']
      },
      inp_bom: {
        layer: 'Operational Inputs · Product Structure',
        accent: '#f59e0b',
        title: 'Bills of Materials (BOM)',
        sub: '',
        summary: 'Multi-level ingredient recipes, allergen matrices, packaging specifications, and engineering revision cutover schedules.',
        agentIds: ['eco_cutover_orchestrator', 'rfq_should_cost_agent', 'scrap_defect_root_cause_agent']
      },
      inp_orders: {
        layer: 'Operational Inputs · Fulfillment Stream',
        accent: '#f59e0b',
        title: 'Order Management',
        sub: '',
        summary: 'Live omnichannel customer orders, retail replenishment allocations, minimum shelf-life rules, and return authorizations.',
        agentIds: ['atp_order_promising_agent', 'store_capacity_agent', 'short_dated_redistributor']
      },
      inp_machine: {
        layer: 'Operational Inputs · Shop-Floor Cadence',
        accent: '#f59e0b',
        title: 'Machine Run Hours',
        sub: '',
        summary: 'Production line runtime, changeover washdown durations, operator shift coverage, and utility load telemetry.',
        agentIds: ['finite_production_scheduler', 'line_schedule_optimizer', 'labor_line_balancing_agent']
      },
      inp_supplier: {
        layer: 'Operational Inputs · Upstream Signals',
        accent: '#f59e0b',
        title: 'Supplier Delivery',
        sub: '',
        summary: 'Advance Shipping Notices (ASN), supplier On-Time In-Full (OTIF) receipts, upstream Tier-N risk alerts, and raw material market indices.',
        agentIds: ['tier_n_risk_sentinel', 'dock_to_stock_agent', 'supplier_quality_sentinel']
      },
      inp_iiot: {
        layer: 'Operational Inputs · Physical IoT Telemetry',
        accent: '#f59e0b',
        title: 'IIoT / MES & Fleet Telemetry',
        sub: '',
        summary: 'High-speed inline vision cameras, SCADA/PLC vibration & pasteurization sensors, refrigerated trailer temperature loggers, and live GPS truck feeds.',
        agentIds: ['inline_yield_guardian', 'cold_chain_auditor', 'otif_penalty_shield', 'sanitation_health_agent']
      }
    };

    const _activeScFnTileByMount = {};

    function renderAiInSupplyChainFunctionBoard(mountKey = 'home') {
      const renderTile = (id) => {
        const t = SC_AI_FUNCTION_TILES[id];
        if (!t) return '';
        const selected = _activeScFnTileByMount[mountKey] === id ? 'is-selected' : '';
        return `
          <div class="sc-fn-tile ${selected}"
               data-fn-mount="${mountKey}"
               data-fn-tile="${id}"
               style="--tile-accent: ${t.accent};"
               onclick="selectScFunctionTile('${mountKey}', '${id}')">
            <div class="sc-fn-tile-title">${t.title}</div>
            ${t.sub ? `<div class="sc-fn-tile-sub">${t.sub}</div>` : ''}
          </div>
        `;
      };

      return `
        <div class="sc-fn-stack-wrap" id="scFnStackWrap_${mountKey}">
          <div class="sc-fn-stack-header">
            <h2 class="sc-fn-stack-title">AI in Supply Chain Function</h2>
            <span class="sc-fn-stack-hint">
              <span style="color:#ef533f;">●</span>
              <span>Agentic AI Layer Inside Dashed Zone · Click Any Tile to Inspect Connected AI Agents</span>
            </span>
          </div>

          <!-- CORAL-RED DASHED AGENTIC TRANSFORMATION ZONE (TOP LAYER + SERVICE DELIVERY LAYER) -->
          <div class="sc-fn-dashed-agentic-zone">
            <span class="sc-fn-zone-badge">✦ Agentic AI Operating Zone · 60 Specialized Agents</span>

            <!-- Row 1: Top Layer -->
            <div class="sc-fn-row">
              <div class="sc-fn-layer-head layer-blue">
                <div class="sc-fn-layer-head-title">Top Layer</div>
                <div class="sc-fn-layer-head-sub">Executive Steering &amp; Capital Allocation</div>
              </div>
              <div class="sc-fn-tiles-grid cols-4">
                ${renderTile('top_profitability')}
                ${renderTile('top_rolling_sop')}
                ${renderTile('top_working_capital')}
                ${renderTile('top_capex_warroom')}
              </div>
            </div>

            <!-- Row 2: Service Delivery Layer -->
            <div class="sc-fn-row">
              <div class="sc-fn-layer-head layer-purple">
                <div class="sc-fn-layer-head-title">Service Delivery Layer</div>
              </div>
              <div class="sc-fn-tiles-grid cols-3">
                ${renderTile('svc_transactional')}
                ${renderTile('svc_technical')}
                ${renderTile('svc_embedded')}
              </div>
            </div>
          </div>

          <!-- FOUNDATION SYSTEMS & OPERATIONAL TELEMETRY INPUTS -->
          <div class="sc-fn-foundation-rows">
            <!-- Row 3: Core Apps -->
            <div class="sc-fn-row">
              <div class="sc-fn-layer-head layer-green">
                <div class="sc-fn-layer-head-title">Core Apps</div>
              </div>
              <div class="sc-fn-tiles-grid cols-4">
                ${renderTile('core_erp_hub')}
                ${renderTile('core_wms_tms')}
                ${renderTile('core_mdg')}
                ${renderTile('core_portals')}
              </div>
            </div>

            <!-- Row 4: Operational Inputs -->
            <div class="sc-fn-row">
              <div class="sc-fn-layer-head layer-amber">
                <div class="sc-fn-layer-head-title">Operational Inputs</div>
              </div>
              <div class="sc-fn-tiles-grid cols-6">
                ${renderTile('inp_pos')}
                ${renderTile('inp_bom')}
                ${renderTile('inp_orders')}
                ${renderTile('inp_machine')}
                ${renderTile('inp_supplier')}
                ${renderTile('inp_iiot')}
              </div>
            </div>
          </div>

          <div id="scFnInspectorDrawer_${mountKey}" style="display:none;"></div>
        </div>
      `;
    }

    function selectScFunctionTile(mountKey, tileId) {
      const drawer = document.getElementById('scFnInspectorDrawer_' + mountKey);
      const wrap = document.getElementById('scFnStackWrap_' + mountKey);
      if (!drawer || !wrap) return;

      if (_activeScFnTileByMount[mountKey] === tileId && drawer.style.display !== 'none') {
        _activeScFnTileByMount[mountKey] = null;
        drawer.style.display = 'none';
        wrap.querySelectorAll('.sc-fn-tile').forEach(el => el.classList.remove('is-selected'));
        return;
      }

      const tile = SC_AI_FUNCTION_TILES[tileId];
      if (!tile) return;
      _activeScFnTileByMount[mountKey] = tileId;

      wrap.querySelectorAll('.sc-fn-tile').forEach(el => {
        el.classList.toggle('is-selected', el.getAttribute('data-fn-tile') === tileId);
      });

      const agentCardsHtml = (tile.agentIds || [])
        .map(aid => AGENTS[aid])
        .filter(Boolean)
        .map(ag => {
          const dept = DEPARTMENTS[ag.deptId] || { color: tile.accent, name: '' };
          return `
            <button type="button" class="sc-fn-agent-link-chip" onclick="openAgentPage('${ag.id}', true, event)">
              <div style="display:flex; align-items:center; gap:10px; min-width:0;">
                <div class="ai-bot-square" style="width:34px; height:34px; font-size:15px; flex-shrink:0;">✦</div>
                <div style="min-width:0;">
                  <div style="font-family:var(--font-display); font-size:14.5px; font-weight:700; color:var(--text-primary); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                    ${cleanAgentName(ag.name)}
                  </div>
                  <div style="font-size:12px; color:var(--text-secondary); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                    ${ag.subPillarName || dept.name}
                  </div>
                </div>
              </div>
              <span style="font-family:var(--font-mono); font-size:12px; font-weight:700; color:${tile.accent}; flex-shrink:0;">Open &rarr;</span>
            </button>
          `;
        })
        .join('');

      drawer.style.borderColor = tile.accent;
      drawer.style.display = 'block';
      drawer.innerHTML = `
        <div class="sc-fn-inspector-top">
          <div>
            <div style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${tile.accent}; margin-bottom:4px;">
              ${tile.layer}
            </div>
            <div style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary);">
              ${tile.title} ${tile.sub ? `<span style="font-weight:500; color:var(--text-secondary); font-size:16px;">${tile.sub}</span>` : ''}
            </div>
            <p style="font-size:14.5px; line-height:1.62; color:var(--text-secondary); margin:8px 0 0; max-width:980px;">
              ${tile.summary}
            </p>
          </div>
          <button type="button" class="back-btn" style="padding:6px 12px; font-size:12.5px; flex-shrink:0;" onclick="selectScFunctionTile('${mountKey}', '${tileId}')">
            ✕ Close
          </button>
        </div>
        <div style="font-family:var(--font-mono); font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:var(--text-secondary);">
          Connected Supply Chain AI Agents (${(tile.agentIds || []).length}) — Click to Open Live Agent &amp; Demo
        </div>
        <div class="sc-fn-inspector-agents">
          ${agentCardsHtml}
        </div>
      `;
    }

    function mountHomeAiFunctionStack() {
      const homeMount = document.getElementById('homeAiFunctionStackMount');
      if (homeMount) {
        homeMount.innerHTML = renderAiInSupplyChainFunctionBoard('home');
      }
    }
"""

NEW_OPEN_ARCH_FN = """    function openArchitecturePage(pushHash = true, ev = null) {
      if (pushHash) {
        history.pushState({ page: 'architecture' }, '', '#architecture');
      }

      const transClass = getPageTransitionClass(ev, null);
      const container = document.getElementById('architecturePageContent');
      container.innerHTML = `
        <div class="${transClass}">
          <div class="back-bar">
            <button type="button" class="back-btn" onclick="goToOrgChart()">
              <span>&larr;</span>
              <span>Back to CSCO Org Chart</span>
            </button>

            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              <button type="button" class="switch-pill" onclick="openPersonasDirectoryPage('all', '', true, 'agents', event)">
                Explore All 60 AI Agents &rarr;
              </button>
              <button type="button" class="switch-pill" onclick="openPersonasDirectoryPage('all', '', true, 'personas', event)">
                Explore All 60 Personas &rarr;
              </button>
            </div>
          </div>

          <!-- 4-Layer Executive Operating Stack ('AI in Supply Chain Function') -->
          <div style="margin-bottom: 30px;">
            ${renderAiInSupplyChainFunctionBoard('arch')}
          </div>

          <!-- ONE Single Button to Expand All 60 Flippable Agent Architecture Cards -->"""


def update_html_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    # 1. Inject or update AI_FN_STACK_CSS right before </style>
    css_start_marker = "    /* =========================================================================\n       AI IN SUPPLY CHAIN FUNCTION — 4-LAYER EXECUTIVE OPERATING MODEL STACK"
    if css_start_marker in text:
        s_idx = text.index(css_start_marker)
        e_idx = text.index("  </style>", s_idx)
        text = text[:s_idx] + AI_FN_STACK_CSS.lstrip("\n") + "\n" + text[e_idx:]
    else:
        style_close = "  </style>\n</head>"
        if style_close not in text:
            raise RuntimeError(f"Could not find {style_close!r} in {path}")
        text = text.replace(style_close, AI_FN_STACK_CSS + "\n  </style>\n</head>", 1)

    # 2. Add 'AI Stack' button to top navbar if not already present
    nav_target = """      <button type="button" class="nav-pill-btn" onclick="openPeriodicTablePage('all', null, true)">Periodic Table</button>"""
    nav_with_stack = """      <button type="button" class="nav-pill-btn" onclick="openArchitecturePage(true, event)">AI Stack</button>
      <button type="button" class="nav-pill-btn" onclick="openPeriodicTablePage('all', null, true)">Periodic Table</button>"""
    if 'onclick="openArchitecturePage(true, event)">AI Stack</button>' not in text:
        if nav_target not in text:
            raise RuntimeError(f"Could not find navbar Periodic Table button in {path}")
        text = text.replace(nav_target, nav_with_stack, 1)

    # 3. Add #aiFunctionStackSection on #pageHome right after #orgChartSection
    home_section_html = """      <!-- Progressive Pillar Drawer (What This Pillar Means + Personas & Agents) -->
      <div id="deptShowcaseContainer"></div>
    </section>

    <!-- 3. AI IN SUPPLY CHAIN FUNCTION — 4-LAYER OPERATING MODEL STACK -->
    <section id="aiFunctionStackSection" class="org-section" style="padding-top: 8px; padding-bottom: 76px;">
      <div id="homeAiFunctionStackMount"></div>
    </section>"""

    old_home_end = """      <!-- Progressive Pillar Drawer (What This Pillar Means + Personas & Agents) -->
      <div id="deptShowcaseContainer"></div>
    </section>"""

    if 'id="aiFunctionStackSection"' not in text:
        if old_home_end not in text:
            raise RuntimeError(f"Could not find #orgChartSection end in {path}")
        text = text.replace(old_home_end, home_section_html, 1)

    # 4. Inject or update AI_FN_STACK_JS right before openArchitecturePage AND update openArchitecturePage header/diagram
    js_marker = "    /* =========================================================================\n       AI IN SUPPLY CHAIN FUNCTION — 4-LAYER OPERATING MODEL DATA & RENDERER"
    if js_marker in text:
        j_start = text.index(js_marker)
        j_end = text.index("    function openArchitecturePage(", j_start)
        text = text[:j_start] + AI_FN_STACK_JS.lstrip("\n") + "\n" + text[j_end:]
    else:
        arch_fn_anchor = "    function openArchitecturePage(pushHash = true, ev = null) {"
        if arch_fn_anchor not in text:
            raise RuntimeError(f"Could not find openArchitecturePage in {path}")
        text = text.replace(arch_fn_anchor, AI_FN_STACK_JS + "\n" + arch_fn_anchor, 1)

    # Replace top half of openArchitecturePage up to the 60-agent trigger bar
    arch_start = text.index("    function openArchitecturePage(pushHash = true, ev = null) {")
    trigger_marker = "          <!-- ONE Single Button to Expand All 60 Flippable Agent Architecture Cards -->"
    arch_trigger_idx = text.index(trigger_marker, arch_start)
    text = (
        text[:arch_start]
        + NEW_OPEN_ARCH_FN
        + text[arch_trigger_idx + len(trigger_marker):]
    )

    # 5. Mount the home board on DOMContentLoaded
    if "mountHomeAiFunctionStack();" not in text:
        dom_target = "      renderOrgChart();"
        # Replace the one inside DOMContentLoaded (last occurrence)
        r_idx = text.rfind(dom_target)
        if r_idx == -1:
            raise RuntimeError(f"Could not find renderOrgChart() in {path}")
        text = (
            text[:r_idx]
            + "      renderOrgChart();\n      mountHomeAiFunctionStack();"
            + text[r_idx + len(dom_target):]
        )

    path.write_text(text, encoding="utf-8")
    print(f"[OK] Updated {path.name} ({len(text):,} bytes)")


def verify_inline_js(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    s_idx = text.rfind("<script>")
    e_idx = text.rfind("</script>")
    js_code = text[s_idx + len("<script>"):e_idx]
    tmp_js = Path("/tmp/verify_sc_fn_stack.js")
    tmp_js.write_text(js_code, encoding="utf-8")
    subprocess.run(["node", "--check", str(tmp_js)], check=True)
    print(f"[JS SYNTAX PASS] {path.name}")


def sync_docs_and_zipline() -> None:
    for folder_name in ("docs", "zipline_dist"):
        target_dir = ROOT / folder_name
        if target_dir.exists():
            for f in HTML_FILES:
                shutil.copy2(f, target_dir / f.name)
            print(f"[SYNC] Copied updated HTML files to {folder_name}/")

    zip_targets = [
        ROOT / "supply_chain_zipline_bundle.zip",
        ROOT / "Supply_Chain_Agentic_Portal.zip",
        ROOT / "Zipline_Supply_Chain_Agentic_Portal.zip",
        ROOT / "zipline" / "supply_chain_zipline_bundle.zip",
        ROOT / "zipline" / "supply_chain_zipline_light.zip",
    ]
    dist_dir = ROOT / "zipline_dist"
    if dist_dir.exists():
        for zpath in zip_targets:
            if zpath.exists():
                with zipfile.ZipFile(zpath, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                    for item in sorted(dist_dir.rglob("*")):
                        if item.is_file():
                            zf.write(item, item.relative_to(dist_dir))
                print(f"[ZIP] Refreshed {zpath.relative_to(ROOT)}")


if __name__ == "__main__":
    for html_file in HTML_FILES:
        update_html_file(html_file)
    verify_inline_js(ROOT / "index.html")
    sync_docs_and_zipline()

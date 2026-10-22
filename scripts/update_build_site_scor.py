#!/usr/bin/env python3
"""
Updates build_site.py to reflect the canonical 6 ASCM SCOR Pillars:
- 3x2 grid CSS for .dept-row
- 3-line animated telemetry tree in .org-connectors
- Front-page 6-pillar tabs (#verticalTabsNavBar)
- Synchronized tab switching logic with alias normalization
- Process workflow ribbons for all 6 pillars
- 6-pillar + universal core PERIODIC_GROUPS and PERIODIC_AGENT_META
- Updated copy (6 ASCM SCOR Pillars, 29 Personas, 35 Agents)
"""

import re
from pathlib import Path

BUILD_SITE = Path(__file__).resolve().parent.parent / "build_site.py"

def update_build_site():
    print(f"Reading {BUILD_SITE}...")
    content = BUILD_SITE.read_text(encoding="utf-8")

    # 1. Update .dept-row CSS for 3x2 grid
    old_dept_row = """.dept-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
      width: 100%;
    }

    @media (max-width: 1280px) {
      .dept-row { grid-template-columns: repeat(2, 1fr); }
    }"""
    
    new_dept_row = """.dept-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      width: 100%;
    }

    @media (max-width: 1100px) {
      .dept-row { grid-template-columns: repeat(2, 1fr); }
    }"""
    
    if old_dept_row in content:
        content = content.replace(old_dept_row, new_dept_row, 1)
        print("Updated .dept-row grid CSS to 3 columns.")
    else:
        print("Warning: old_dept_row pattern not found verbatim.")

    # 2. Update CSCO Org Chart section header
    old_section_header = """    <!-- 2. CSCO ORG CHART (PROGRESSIVE EXPLORATION ACROSS THE 8 OPERATIONAL VERTICALS) -->
    <section id="orgChartSection" class="org-section">
      <div class="section-header">
        <h2 class="section-title">Office of the CSCO — The 8 Operational Verticals</h2>"""

    new_section_header = """    <!-- 2. CSCO ORG CHART (PROGRESSIVE EXPLORATION ACROSS THE 6 SCOR PILLARS) -->
    <section id="orgChartSection" class="org-section">
      <div class="section-header">
        <h2 class="section-title">Office of the CSCO — The 6 ASCM SCOR Pillars</h2>"""

    if old_section_header in content:
        content = content.replace(old_section_header, new_section_header, 1)
        print("Updated section header to 6 ASCM SCOR Pillars.")

    # 3. Update master tab bar #verticalTabsNavBar
    old_tab_bar_start = '<!-- 8-Vertical Interactive Master Navigation Tab Bar on the Front Page -->'
    old_tab_bar_end = '<!-- CSCO Apex Box featuring Animated 3D Isometric Conveyor & Control Tower Emblem -->'
    
    new_tab_bar = """<!-- 6-Pillar Interactive Master Navigation Tab Bar on the Front Page -->
      <div class="vertical-tabs-nav-bar" id="verticalTabsNavBar">
        <button type="button" class="v-tab-btn active" data-vtab="all" onclick="switchVerticalTab('all', this)">
          <span class="v-tab-num" style="color:#38bdf8;">ALL 6</span>
          <span class="v-tab-title">All 6 Pillars</span>
          <span class="v-tab-tag">SCOR End-to-End</span>
          <span class="v-tab-badge">29 Personas · 35 Agents</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="demand_sop" onclick="switchVerticalTab('demand_sop', this)" style="--v-accent: #10b981;">
          <span class="v-tab-num">01 · PLAN</span>
          <span class="v-tab-title">Demand &amp; S&amp;OP</span>
          <span class="v-tab-tag">The Forecasters</span>
          <span class="v-tab-badge">4 Roles · 4 Agents</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="sourcing_procurement" onclick="switchVerticalTab('sourcing_procurement', this)" style="--v-accent: #a142f4;">
          <span class="v-tab-num">02 · SOURCE</span>
          <span class="v-tab-title">Sourcing &amp; Procurement</span>
          <span class="v-tab-tag">The Buyers</span>
          <span class="v-tab-badge">4 Roles · 4 Agents</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="manufacturing_prod" onclick="switchVerticalTab('manufacturing_prod', this)" style="--v-accent: #3b82f6;">
          <span class="v-tab-num">03 · MAKE</span>
          <span class="v-tab-title">Manufacturing &amp; MPS</span>
          <span class="v-tab-tag">The Makers</span>
          <span class="v-tab-badge">4 Roles · 4 Agents</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="inventory_warehouse" onclick="switchVerticalTab('inventory_warehouse', this)" style="--v-accent: #00d2ff;">
          <span class="v-tab-num">04 · FULFILL</span>
          <span class="v-tab-title">Inventory &amp; Warehousing</span>
          <span class="v-tab-tag">The Buffers &amp; Custodians</span>
          <span class="v-tab-badge">5 Roles · 6 Agents</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="logistics_fleet" onclick="switchVerticalTab('logistics_fleet', this)" style="--v-accent: #ff8c00;">
          <span class="v-tab-num">05 · DELIVER</span>
          <span class="v-tab-title">Logistics, Fleet &amp; TM&amp;D</span>
          <span class="v-tab-tag">The Movers &amp; Distributors</span>
          <span class="v-tab-badge">9 Roles · 10 Agents</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="circular_enable" onclick="switchVerticalTab('circular_enable', this)" style="--v-accent: #ec4899;">
          <span class="v-tab-num">06 · RETURN &amp; ENABLE</span>
          <span class="v-tab-title">Customer OTIF, RMA &amp; ESG</span>
          <span class="v-tab-tag">The Guardians</span>
          <span class="v-tab-badge">3 Roles · 3 Agents</span>
        </button>
      </div>

      <div class="cfo-root-wrapper">
        <!-- CSCO Apex Box featuring Animated 3D Isometric Conveyor & Control Tower Emblem -->"""

    idx_start = content.find(old_tab_bar_start)
    idx_end = content.find(old_tab_bar_end)
    if idx_start != -1 and idx_end != -1:
        content = content[:idx_start] + new_tab_bar + content[idx_end + len(old_tab_bar_end):]
        print("Updated #verticalTabsNavBar to 6 SCOR pillars.")
    else:
        print("Warning: #verticalTabsNavBar bounds not found.")

    # 4. Update CSCO Apex Box subtitle & SVG Connectors
    old_cfo_sub = '<div class="cfo-box-sub"><span class="sc-hl-metric">8 Operational Verticals</span> · <span class="sc-hl-metric">26 Personas</span> · <span class="sc-hl-metric">28 Domain Agents</span> + <span class="sc-hl-metric">4 Universal Cross-Persona Agents</span></div>'
    new_cfo_sub = '<div class="cfo-box-sub"><span class="sc-hl-metric">6 ASCM SCOR Pillars</span> · <span class="sc-hl-metric">29 Personas</span> · <span class="sc-hl-metric">31 Domain Agents</span> + <span class="sc-hl-metric">4 Universal Core Flagship Copilots</span></div>'
    if old_cfo_sub in content:
        content = content.replace(old_cfo_sub, new_cfo_sub, 1)
        print("Updated CSCO apex box subtitle.")

    # SVG Connectors to 3 branches for 3x2 grid
    old_svg_conn_start = '<!-- SVG Tree Lines to 8 Supply Chain Verticals (4x2 Grid) with Animated Telemetry Packets -->'
    old_svg_conn_end = '<div id="deptRowContainer" class="dept-row"></div>'

    new_svg_conn = """<!-- SVG Tree Lines to 6 Supply Chain Pillars (3x2 Grid) with Animated Telemetry Packets -->
        <svg class="org-connectors" viewBox="0 0 1000 56" preserveAspectRatio="none">
          <defs>
            <linearGradient id="orgLineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#10b981" stop-opacity="0.55" />
              <stop offset="20%" stop-color="#a142f4" stop-opacity="0.65" />
              <stop offset="40%" stop-color="#3b82f6" stop-opacity="0.75" />
              <stop offset="60%" stop-color="#00d2ff" stop-opacity="0.75" />
              <stop offset="80%" stop-color="#ff8c00" stop-opacity="0.75" />
              <stop offset="100%" stop-color="#ec4899" stop-opacity="0.55" />
            </linearGradient>
          </defs>
          <path d="M500,0 L500,24 M166,24 L834,24 M166,24 L166,56 M500,24 L500,56 M834,24 L834,56" />
          <path d="M500,0 L500,24 M166,24 L834,24 M166,24 L166,56 M500,24 L500,56 M834,24 L834,56"
                stroke="url(#orgLineGrad)" stroke-width="2.2" stroke-dasharray="8 10" fill="none"
                style="animation: scDashFlow 2.4s linear infinite;" />
          <circle r="3.5" fill="#10b981">
            <animateMotion dur="2.4s" repeatCount="indefinite" path="M500,0 L500,24 L166,24 L166,56" />
          </circle>
          <circle r="3.5" fill="#00d2ff">
            <animateMotion dur="2.0s" repeatCount="indefinite" path="M500,0 L500,24 L500,56" />
          </circle>
          <circle r="3.5" fill="#ec4899">
            <animateMotion dur="2.6s" repeatCount="indefinite" path="M500,0 L500,24 L834,24 L834,56" />
          </circle>
        </svg>

        <!-- 6 Clean Supply Chain Pillar Boxes -->
        <div id="deptRowContainer" class="dept-row"></div>"""

    idx_conn_start = content.find(old_svg_conn_start)
    idx_conn_end = content.find(old_svg_conn_end)
    if idx_conn_start != -1 and idx_conn_end != -1:
        content = content[:idx_conn_start] + new_svg_conn + content[idx_conn_end + len(old_svg_conn_end):]
        print("Updated .org-connectors SVG to 3 branches.")

    # 5. Update DEPARTMENTS aliases in script
    old_dept_script = """    /* 1. EIGHT CANONICAL OPERATIONAL VERTICALS UNDER THE CSCO */
    const DEPARTMENTS = __EMBEDDED_DEPARTMENTS_JSON__;
    Object.defineProperty(DEPARTMENTS, 'sourcing_risk', { get: () => DEPARTMENTS.sourcing_procurement, enumerable: false, configurable: true });
    Object.defineProperty(DEPARTMENTS, 'inventory_warehouse', { get: () => DEPARTMENTS.warehousing_qa, enumerable: false, configurable: true });
    Object.defineProperty(DEPARTMENTS, 'circular_enable', { get: () => DEPARTMENTS.reverse_risk_esg, enumerable: false, configurable: true });"""

    new_dept_script = """    /* 1. SIX CANONICAL SCOR PILLARS UNDER THE CSCO */
    const DEPARTMENTS = __EMBEDDED_DEPARTMENTS_JSON__;
    Object.defineProperty(DEPARTMENTS, 'sourcing_risk', { get: () => DEPARTMENTS.sourcing_procurement, enumerable: false, configurable: true });
    Object.defineProperty(DEPARTMENTS, 'inventory_meio', { get: () => DEPARTMENTS.inventory_warehouse, enumerable: false, configurable: true });
    Object.defineProperty(DEPARTMENTS, 'warehousing_qa', { get: () => DEPARTMENTS.inventory_warehouse, enumerable: false, configurable: true });
    Object.defineProperty(DEPARTMENTS, 'warehouse_intralogistics', { get: () => DEPARTMENTS.inventory_warehouse, enumerable: false, configurable: true });
    Object.defineProperty(DEPARTMENTS, 'trade_mkt_dist', { get: () => DEPARTMENTS.logistics_fleet, enumerable: false, configurable: true });
    Object.defineProperty(DEPARTMENTS, 'reverse_risk_esg', { get: () => DEPARTMENTS.circular_enable, enumerable: false, configurable: true });
    Object.defineProperty(DEPARTMENTS, 'reverse_logistics_esg', { get: () => DEPARTMENTS.circular_enable, enumerable: false, configurable: true });"""

    if old_dept_script in content:
        content = content.replace(old_dept_script, new_dept_script, 1)
        print("Updated DEPARTMENTS non-enumerable aliases in script.")

    # 6. Update switchVerticalTab controller
    old_switch_tab_start = '/* 8-Vertical Interactive Master Navigation & Tab Controller */'
    old_switch_tab_end = 'function renderOrgChart()'

    new_switch_tab = """/* 6-Pillar Interactive Master Navigation & Tab Controller */
    let currentFrontPageVerticalTab = 'all';

    function switchVerticalTab(vId, btnEl) {
      const DEPT_ALIASES = {
        'inventory_meio': 'inventory_warehouse',
        'warehousing_qa': 'inventory_warehouse',
        'warehouse_intralogistics': 'inventory_warehouse',
        'trade_mkt_dist': 'logistics_fleet',
        'reverse_risk_esg': 'circular_enable',
        'reverse_logistics_esg': 'circular_enable',
        'sourcing_risk': 'sourcing_procurement'
      };
      const canonicalVId = DEPT_ALIASES[vId] || vId;
      currentFrontPageVerticalTab = canonicalVId;
      document.querySelectorAll('#verticalTabsNavBar .v-tab-btn').forEach(b => {
        const targetAttr = b.getAttribute('data-vtab');
        const isTarget = targetAttr === canonicalVId || targetAttr === vId;
        b.classList.toggle('active', isTarget);
      });

      if (canonicalVId === 'all') {
        selectedDeptId = null;
        document.querySelectorAll('#verticalTabsNavBar .v-tab-btn').forEach(b => {
          b.classList.toggle('active', b.getAttribute('data-vtab') === 'all');
        });

        document.querySelectorAll('#deptRowContainer .dept-node').forEach(node => {
          node.classList.remove('active');
          node.style.display = 'flex';
        });
        renderDepartmentShowcaseBox();
        const row = document.getElementById('deptRowContainer');
        if (row) row.scrollIntoView({ behavior: 'smooth', block: 'start' });
      } else {
        selectedDeptId = canonicalVId;
        document.querySelectorAll('#deptRowContainer .dept-node').forEach(node => {
          const nid = node.getAttribute('data-dept-id');
          const isTarget = nid === canonicalVId;
          node.classList.toggle('active', isTarget);
          node.style.display = 'flex'; // keep visible in 3x2 grid
        });
        renderDepartmentShowcaseBox();
        hydrateAssets();
        setTimeout(() => {
          const showcase = document.getElementById('deptShowcaseBoxEl');
          if (showcase) showcase.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 80);
      }
    }

    """

    idx_sw_start = content.find(old_switch_tab_start)
    idx_sw_end = content.find(old_switch_tab_end)
    if idx_sw_start != -1 and idx_sw_end != -1:
        content = content[:idx_sw_start] + new_switch_tab + content[idx_sw_end:]
        print("Updated switchVerticalTab controller.")

    # 7. Update selectDepartment to keep tabs synchronized
    old_select_dept = """    function selectDepartment(deptId, ev) {
      const sRect = getClickedCardRect(ev);
      selectedDeptId = (selectedDeptId === deptId) ? null : deptId;

      // Update active state on the 6 SCOR Vertical cards in-place without re-creating DOM nodes
      document.querySelectorAll('#deptRowContainer .dept-node').forEach(node => {
        const nid = node.getAttribute('data-dept-id');
        const active = nid === selectedDeptId;
        node.classList.toggle('active', active);
      });"""

    new_select_dept = """    function selectDepartment(deptId, ev) {
      const sRect = getClickedCardRect(ev);
      selectedDeptId = (selectedDeptId === deptId) ? null : deptId;

      // Update active state on the 6 SCOR Pillar cards in-place without re-creating DOM nodes
      document.querySelectorAll('#deptRowContainer .dept-node').forEach(node => {
        const nid = node.getAttribute('data-dept-id');
        const active = nid === selectedDeptId;
        node.classList.toggle('active', active);
      });

      // Synchronize front-page master tab bar
      const activeTabId = selectedDeptId || 'all';
      document.querySelectorAll('#verticalTabsNavBar .v-tab-btn').forEach(b => {
        b.classList.toggle('active', b.getAttribute('data-vtab') === activeTabId);
      });"""

    if old_select_dept in content:
        content = content.replace(old_select_dept, new_select_dept, 1)
        print("Updated selectDepartment tab sync.")

    # 8. Update renderVerticalWorkflowStrip conditions
    content = content.replace(
        "if (dept.id === 'warehouse_intralogistics')",
        "if (dept.id === 'inventory_warehouse' || dept.id === 'warehouse_intralogistics' || dept.id === 'warehousing_qa' || dept.id === 'inventory_meio')",
        1
    )
    content = content.replace(
        "if (dept.id === 'logistics_fleet')",
        "if (dept.id === 'logistics_fleet' || dept.id === 'trade_mkt_dist')",
        1
    )
    content = content.replace(
        "if (dept.id === 'reverse_logistics_esg')",
        "if (dept.id === 'circular_enable' || dept.id === 'reverse_risk_esg' || dept.id === 'reverse_logistics_esg')",
        1
    )
    print("Updated renderVerticalWorkflowStrip conditions.")

    # 9. Update PERIODIC_AGENT_META and PERIODIC_GROUPS in script
    old_pt_meta_start = "// 04 · Fulfill (3D WMS, MEIO & Cross-Dock)"
    old_pt_meta_end = "let currentPeriodicFilter = 'all';"

    new_pt_meta = """// 04 · Fulfill (3D WMS, MEIO & Cross-Dock)
      meio_safety_stock_agent:         { code: '401', sym: 'Ef', short: 'EchelonFlow',     group: 'inventory_warehouse', layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Scheduled',         trigIcon: '⏱️' },
      warehouse_slotting_agent:        { code: '402', sym: 'Sm', short: 'SlotMaster 3D',   group: 'inventory_warehouse', layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Scheduled',         trigIcon: '⏱️' },
      atp_order_promising_agent:       { code: '403', sym: 'Pg', short: 'PromiseGuard',    group: 'inventory_warehouse', layer: 'Spanner Graph + AI',    layerColor: '#a855f7', trigger: 'Event-Driven',      trigIcon: '⚡' },
      yard_dock_sequencer:             { code: '404', sym: 'Yp', short: 'YardPulse',       group: 'inventory_warehouse', layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Event-Driven',      trigIcon: '⚡' },
      crossdock_transfer_orchestrator: { code: '405', sym: 'Xd', short: 'CrossDockFlow',   group: 'inventory_warehouse', layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Event-Driven',      trigIcon: '⚡' },
      network_twin_architect:          { code: '406', sym: 'Td', short: 'TwinDesign',      group: 'inventory_warehouse', layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Human-in-the-loop', trigIcon: '🛡️' },
      // 05 · Deliver (Multi-Modal Ship, Air, Rail, Road & TM&D)
      load_consolidation_agent:        { code: '501', sym: 'Cb', short: 'CubeMaster 3D',   group: 'logistics_fleet',     layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Event-Driven',      trigIcon: '⚡' },
      fleetflow_dispatch:              { code: '502', sym: 'Ff', short: 'FleetFlow Maps',  group: 'logistics_fleet',    layer: 'OR-Tools + Google Maps', layerColor: '#f59e0b', trigger: 'Event-Driven',      trigIcon: '⚡' },
      field_beat_distributor_sync_agent: { code: '503', sym: 'Bs', short: 'BeatSync FSO', group: 'logistics_fleet', layer: 'OR-Tools + Google Maps', layerColor: '#f59e0b', trigger: 'Event-Driven',      trigIcon: '⚡' },
      planogram_merchandising_vision_auditor: { code: '504', sym: 'Sv', short: 'ShelfVision IR', group: 'logistics_fleet', layer: 'Gemini 3.8 Flash Vision', layerColor: '#3b82f6', trigger: 'Event-Driven',      trigIcon: '⚡' },
      trade_scheme_claims_reconciler: { code: '505', sym: 'Sg', short: 'SchemeGuard', group: 'logistics_fleet', layer: 'BigQuery + Vertex ADK', layerColor: '#10b981', trigger: 'Scheduled',         trigIcon: '⏱️' },
      port_drayage_orchestrator:       { code: '506', sym: 'Pw', short: 'PortWatch Sea',   group: 'logistics_fleet',     layer: 'Spanner Graph + AI',    layerColor: '#a855f7', trigger: 'Event-Driven',      trigIcon: '⚡' },
      air_cargo_uld_optimizer:         { code: '507', sym: 'Af', short: 'AeroFreight Air', group: 'logistics_fleet',     layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Event-Driven',      trigIcon: '⚡' },
      intermodal_rail_linehaul_agent:  { code: '508', sym: 'Ir', short: 'IntermodalSync',  group: 'logistics_fleet',     layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Scheduled',         trigIcon: '⏱️' },
      multimodal_mode_shift_agent:     { code: '509', sym: 'Ms', short: 'ModalShift',      group: 'logistics_fleet',     layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Human-in-the-loop', trigIcon: '🛡️' },
      freight_control_tower:           { code: '510', sym: 'St', short: 'SentinelMove',    group: 'logistics_fleet',     layer: 'Vertex AI ADK + A2A',   layerColor: '#3b82f6', trigger: 'Event-Driven',      trigIcon: '⚡' },
      // 06 · Return & Enable (OTIF, RMA & ESG)
      otif_penalty_shield:             { code: '601', sym: 'Ot', short: 'OTIFShield',      group: 'circular_enable',     layer: 'Vertex AI ADK + A2A',   layerColor: '#3b82f6', trigger: 'Event-Driven',      trigIcon: '⚡' },
      reverse_rma_optimizer:           { code: '602', sym: 'Rl', short: 'ReturnLoop RMA',  group: 'circular_enable',     layer: 'Vertex AI ADK + A2A',   layerColor: '#3b82f6', trigger: 'Event-Driven',      trigIcon: '⚡' },
      carbon_scope3_ledger:            { code: '603', sym: 'Ec', short: 'EcoChain CO2e',   group: 'circular_enable',     layer: 'BigQuery ML + TimesFM', layerColor: '#10b981', trigger: 'Scheduled',         trigIcon: '⏱️' },
      // 00 · Universal Cross-Persona CSCO Core
      csco_control_tower_copilot:      { code: '001', sym: 'Ct', short: 'TowerMind',       group: 'universal_csco',      layer: 'Vertex AI ADK + A2A',   layerColor: '#3b82f6', trigger: 'Chat-Initiated',    trigIcon: '💬' },
      disruption_war_room_orchestrator:{ code: '002', sym: 'Sw', short: 'StormShield',     group: 'universal_csco',      layer: 'Spanner Graph + AI',    layerColor: '#a855f7', trigger: 'Event-Driven',      trigIcon: '⚡' },
      master_data_leadtime_steward:    { code: '003', sym: 'Dc', short: 'DataCleanse',     group: 'universal_csco',      layer: 'BigQuery ML + TimesFM', layerColor: '#10b981', trigger: 'Scheduled',         trigIcon: '⏱️' },
      working_capital_cash_bridge:     { code: '004', sym: 'Mb', short: 'MarginBridge',    group: 'universal_csco',      layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Human-in-the-loop', trigIcon: '🛡️' }
    };

    const PERIODIC_GROUPS = [
      { id: 'demand_sop',          shortTab: 'Plan (01)',            title: '01 · PLAN — DEMAND PLANNING, SENSING & S&OP',          color: '#10b981', count: 4 },
      { id: 'sourcing_procurement', shortTab: 'Source (02)',          title: '02 · SOURCE — STRATEGIC SOURCING & PROCUREMENT',        color: '#a142f4', count: 4 },
      { id: 'manufacturing_prod',  shortTab: 'Make (03)',            title: '03 · MAKE — PRODUCTION PLANNING & MANUFACTURING',       color: '#3b82f6', count: 4 },
      { id: 'inventory_warehouse', shortTab: 'Fulfill (04)',         title: '04 · FULFILL — MULTI-ECHELON INVENTORY & 3D WMS',       color: '#00d2ff', count: 6 },
      { id: 'logistics_fleet',     shortTab: 'Deliver (05)',         title: '05 · DELIVER — MULTI-MODAL FLEET & TRADE DISTRIBUTION', color: '#ff8c00', count: 10 },
      { id: 'circular_enable',     shortTab: 'Return & Enable (06)', title: '06 · RETURN & ENABLE — CIRCULAR RMA, OTIF & ESG',        color: '#ec4899', count: 3 },
      { id: 'universal_csco',      shortTab: 'Universal Core',       title: '00 · UNIVERSAL CROSS-PERSONA CSCO CONTROL TOWER CORE',  color: '#38bdf8', count: 4 }
    ];

    """

    idx_pt_start = content.find(old_pt_meta_start)
    idx_pt_end = content.find(old_pt_meta_end)
    if idx_pt_start != -1 and idx_pt_end != -1:
        content = content[:idx_pt_start] + new_pt_meta + content[idx_pt_end:]
        print("Updated PERIODIC_AGENT_META and PERIODIC_GROUPS to 6 pillars.")

    # 10. Update text mentions of 26 Personas -> 29 Personas and 32 Agents -> 35 Agents
    replacements = [
        ("Used by All 26 Personas Across 6 SCOR Domains", "Used by All 29 Personas Across 6 SCOR Pillars"),
        ("🌐 Universal · All 26 Personas", "🌐 Universal · All 29 Personas"),
        ("All 26 Personas &amp; 32 Agents", "All 29 Personas &amp; 35 Agents"),
        ("🌐 Cross-Persona Universal Agent (All 26 Roles)", "🌐 Cross-Persona Universal Agent (All 29 Roles)"),
        ("🌐 Cross-Persona Universal Agent · All 26 Roles", "🌐 Cross-Persona Universal Agent · All 29 Roles"),
        ("Browse All 26 Personas &rarr;", "Browse All 29 Personas &rarr;"),
        ("Used by all 26 Personas", "Used by all 29 Personas"),
        ("// Default mode: 'personas' (26 Personas)", "// Default mode: 'personas' (29 Personas)"),
        ("👥 View All 26 Personas", "👥 View All 29 Personas"),
        ("6 SCOR Verticals · 26 Personas · 28 Domain Agents + 4 Universal Agents", "6 SCOR Pillars · 29 Personas · 31 Domain Agents + 4 Universal Core Copilots"),
        ("All 6 SCOR Verticals (${currentDirMode === 'agents' ? '32 Agents' : '26 Personas'})", "All 6 SCOR Pillars (${currentDirMode === 'agents' ? '35 Agents' : '29 Personas'})"),
        ("👥 Explore All 26 Personas", "👥 Explore All 29 Personas"),
        ("4 Universal + 28 Domain Agents · 96 A2A Sub-Agents · 26 Personas", "4 Universal + 31 Domain Agents · 105 A2A Sub-Agents · 29 Personas"),
        ("Cross-Persona Universal Core Agents (Shared Across All 26 Roles)", "Cross-Persona Universal Core Agents (Shared Across All 29 Roles)"),
        ("🌐 Universal Core · All 26 Roles", "🌐 Universal Core · All 29 Roles"),
        ("// Build Left Column Sections (Either by 7 SCOR Domains or by 26 Personas)", "// Build Left Column Sections (Either by 6 SCOR Pillars or by 29 Personas)"),
        ("26 Personas &harr; 32 Agents", "29 Personas &harr; 35 Agents"),
        ("26 Supply Chain Roles · Before vs. After Toil", "29 Supply Chain Roles · Before vs. After Toil")
    ]

    for old_s, new_s in replacements:
        if old_s in content:
            content = content.replace(old_s, new_s)
            print(f"Replaced text: '{old_s[:40]}...' -> '{new_s[:40]}...'")

    BUILD_SITE.write_text(content, encoding="utf-8")
    print(f"Successfully updated {BUILD_SITE}.")

if __name__ == "__main__":
    update_build_site()

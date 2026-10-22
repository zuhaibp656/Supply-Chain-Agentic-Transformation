#!/usr/bin/env python3
"""Restore and upgrade the 4 End-to-End Supply Chain Process Journeys (F2F, O2D, S2P, P2R)
and Pillar Process Flows with less text, rich visual effects, and interactive SVG diagrams.
"""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD_PY = ROOT / "build_site.py"


def main() -> None:
    text = BUILD_PY.read_text(encoding="utf-8")

    # 1. Add CSS for Visual Process Journeys (Light & Dark Themes) right before </style>
    process_css = """
    /* =========================================================================
       VISUAL END-TO-END PROCESS JOURNEYS (F2F, O2D, S2P, P2R) — LESS TEXT, MORE DIAGRAMS
       ========================================================================= */
    .vc-mini-pipeline {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 6px;
      margin-top: 12px;
      position: relative;
      z-index: 2;
    }

    .vc-mini-stage-pill {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 4px 10px;
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.14);
      font-size: 11.5px;
      font-weight: 700;
      color: #f8fafc;
      white-space: nowrap;
    }

    .vc-mini-stage-pill .st-idx {
      font-family: var(--font-mono);
      font-size: 10px;
      font-weight: 800;
      color: var(--vc-accent, #34a853);
    }

    .vc-mini-arrow {
      font-size: 11px;
      color: var(--vc-accent, #34a853);
      font-weight: 800;
      opacity: 0.85;
    }

    /* Visual 3-Block Stage Spotlight Schematic */
    .vc-spotlight-card {
      padding: 22px 24px;
      border-radius: 20px;
      background: linear-gradient(155deg, rgba(15, 23, 42, 0.96) 0%, rgba(9, 14, 26, 0.99) 100%);
      border: 1.5px solid var(--vc-accent, #34a853);
      box-shadow: 0 18px 42px rgba(0, 0, 0, 0.42);
      margin-bottom: 24px;
      animation: ptExpandIn 0.28s var(--ease-spring) forwards;
    }

    .vc-schematic-row {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 48px minmax(0, 1.15fr) 48px minmax(0, 1fr);
      align-items: stretch;
      gap: 8px;
      margin: 16px 0 20px;
    }

    @media (max-width: 960px) {
      .vc-schematic-row {
        grid-template-columns: 1fr;
      }
      .vc-schematic-arrow {
        transform: rotate(90deg);
        margin: 4px auto;
      }
    }

    .vc-schematic-node {
      padding: 16px 18px;
      border-radius: 14px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.12);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 8px;
    }

    .vc-schematic-arrow {
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-mono);
      font-size: 18px;
      font-weight: 800;
      color: var(--vc-accent, #34a853);
    }

    /* 6-Stage At-a-Glance Visual Pipeline Cards */
    .vc-pipeline-strip-grid {
      display: grid;
      grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 28px;
    }

    @media (max-width: 1180px) {
      .vc-pipeline-strip-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr));
      }
    }

    @media (max-width: 680px) {
      .vc-pipeline-strip-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }

    .vc-pipe-step-card {
      padding: 14px 14px;
      border-radius: 14px;
      background: rgba(15, 23, 42, 0.86);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-top: 3.5px solid var(--st-color, #34a853);
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 10px;
      transition: transform 0.25s var(--ease-spring), box-shadow 0.25s var(--ease-spring), border-color 0.2s ease, background 0.2s ease;
    }

    .vc-pipe-step-card:hover,
    .vc-pipe-step-card.active {
      transform: translateY(-5px);
      background: rgba(24, 36, 64, 0.98);
      border-color: var(--st-color, #34a853);
      box-shadow: 0 12px 26px rgba(0, 0, 0, 0.45);
    }

    /* Light Theme Overrides for Visual Process Journeys */
    html[data-theme="light"] .vc-entry-card {
      background: #ffffff;
      border: 1.5px solid #cbd5e1;
      border-top: 4px solid var(--vc-accent, #1a73e8);
      box-shadow: 0 8px 22px rgba(26, 115, 232, 0.07);
    }

    html[data-theme="light"] .vc-entry-card:hover {
      background: #ffffff;
      border-color: var(--vc-accent, #1a73e8);
      box-shadow: 0 20px 42px rgba(26, 115, 232, 0.18);
    }

    html[data-theme="light"] .vc-mini-stage-pill {
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      color: #0f172a;
    }

    html[data-theme="light"] .vc-spotlight-card {
      background: #ffffff;
      border: 2px solid var(--vc-accent, #1a73e8);
      box-shadow: 0 14px 34px rgba(26, 115, 232, 0.12);
    }

    html[data-theme="light"] .vc-schematic-node {
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      color: #0f172a;
    }

    html[data-theme="light"] .vc-pipe-step-card {
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-top: 3.5px solid var(--st-color, #1a73e8);
      box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
    }

    html[data-theme="light"] .vc-pipe-step-card:hover,
    html[data-theme="light"] .vc-pipe-step-card.active {
      background: #f4f8ff;
      border-color: var(--st-color, #1a73e8);
      box-shadow: 0 12px 26px rgba(26, 115, 232, 0.16);
    }
"""
    if ".vc-mini-pipeline {" not in text:
        text = text.replace("  </style>", process_css + "\n  </style>", 1)

    # 2. Add Processes (4) dropdown to Top Navbar & Hero CTA button
    old_nav = """      <div class="nav-dropdown-wrap" style="position:relative;">
        <button type="button" class="nav-pill-btn" onclick="goToOrgChart()">6 SCOR Pillars ▾</button>
        <div class="nav-quick-menu" id="navPillarsQuickMenu"></div>
      </div>"""
    new_nav = """      <div class="nav-dropdown-wrap" style="position:relative;">
        <button type="button" class="nav-pill-btn" onclick="goToOrgChart()">6 SCOR Pillars ▾</button>
        <div class="nav-quick-menu" id="navPillarsQuickMenu"></div>
      </div>

      <div class="nav-dropdown-wrap" style="position:relative;">
        <button type="button" class="nav-pill-btn" onclick="scrollToProcessJourneys()">Processes (4) ▾</button>
        <div class="nav-quick-menu" id="navProcessesQuickMenu"></div>
      </div>"""
    if "navProcessesQuickMenu" not in text:
        assert old_nav in text, "Could not locate navPillarsQuickMenu in navbar"
        text = text.replace(old_nav, new_nav, 1)

    # 3. Restore the End-to-End Process Journeys Section (#valueChainEntryContainer) on #pageHome
    old_home_end = """      <!-- Progressive Pillar Drawer (What This Pillar Means + Personas Only) -->
      <div id="deptShowcaseContainer"></div>
    </section>

  </main>"""
    new_home_end = """      <!-- Progressive Pillar Drawer (What This Pillar Means + Personas & Agents) -->
      <div id="deptShowcaseContainer"></div>

      <!-- 3. END-TO-END CROSS-PILLAR SUPPLY CHAIN PROCESS JOURNEYS (F2F, O2D, S2P, P2R) -->
      <div id="processJourneysSection" class="vc-home-block">
        <div class="section-header" style="margin-bottom: 26px;">
          <div style="display:inline-flex; align-items:center; gap:8px; padding:5px 14px; border-radius:999px; background:rgba(52,168,83,0.14); border:1px solid rgba(52,168,83,0.4); color:#34a853; font-size:11.5px; font-weight:800; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:10px;">
            <span>🔗 4 End-to-End Cross-Pillar Process Journeys</span>
          </div>
          <h2 class="section-title">End-to-End Supply Chain Process Flows</h2>
          <p class="section-subtitle">Click any end-to-end process below to explore its interactive 6-stage visual diagram, system handoffs, and live simulation.</p>
        </div>

        <div id="valueChainEntryContainer" class="vc-entry-grid"></div>
      </div>
    </section>

  </main>"""
    if 'id="valueChainEntryContainer"' not in text:
        assert old_home_end in text, "Could not locate deptShowcaseContainer end on #pageHome"
        text = text.replace(old_home_end, new_home_end, 1)

    # 4. Upgrade renderValueChainEntryCards() to show visual 6-stage mini-pipeline chips instead of paragraph text
    old_vc_cards_start = text.find("    function renderValueChainEntryCards() {")
    old_vc_cards_end = text.find("    function selectDepartment(deptId, ev) {", old_vc_cards_start)
    assert old_vc_cards_start != -1 and old_vc_cards_end != -1

    new_vc_cards_fn = """    function scrollToProcessJourneys() {
      history.pushState({ page: 'home' }, '', '#processes');
      showActivePage('pageHome');
      renderValueChainEntryCards();
      setTimeout(() => {
        const el = document.getElementById('processJourneysSection');
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 40);
    }

    function renderValueChainEntryCards() {
      const vcContainer = document.getElementById('valueChainEntryContainer');
      if (!vcContainer) return;
      vcContainer.innerHTML = Object.values(VALUE_CHAINS).map(vc => {
        const wmType = getVcWatermarkType(vc.id);
        const miniStagesHtml = (vc.stages || []).map((st, idx) => {
          const shortName = st.name.split('&')[0].replace(/Multi-Signal |Autonomous |Multi-Echelon |Multi-Tier |3D |Factory Gate |Ocean Vessel |Air Cargo |Intermodal Rail |Google Maps |Multi-Modal /g, '').trim();
          return `
            <span class="vc-mini-stage-pill">
              <span class="st-idx">0${idx + 1}</span>
              <span>${shortName}</span>
            </span>
            ${idx < vc.stages.length - 1 ? '<span class="vc-mini-arrow">&rarr;</span>' : ''}
          `;
        }).join('');

        return `
          <div class="vc-entry-card"
               style="--vc-accent: ${vc.color}; --dept-accent: ${vc.color};"
               onclick="openValueChainPage('${vc.id}', true, event)">
            <div style="position:relative; z-index:2;">
              <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-bottom:10px;">
                <div class="vc-flow-badge" style="margin-bottom:0; background: ${vc.color}20; color: ${vc.color}; border: 1px solid ${vc.color}50;">
                  <span>🔗 ${vc.flowBadge}</span>
                </div>
                <span style="font-family:var(--font-mono); font-size:12.5px; font-weight:800; padding:4px 10px; border-radius:8px; background:${vc.color}22; color:${vc.color}; border:1px solid ${vc.color}55;">
                  ${vc.headlineStat}
                </span>
              </div>
              <div class="dept-node-title" style="font-size: 22px; margin-bottom: 4px;">${vc.shortTitle}</div>
              <div class="vc-mini-pipeline">
                ${miniStagesHtml}
              </div>
            </div>
            <div class="dept-anim-stage" style="--dept-accent: ${vc.color};">
              ${renderSupplyChainWatermarkSvg(wmType, vc.color, 'dept-stage-svg')}
              <span class="dept-anim-meta">${vc.cardFooterLeft} · Interactive Process Diagram &rarr;</span>
            </div>
          </div>
        `;
      }).join('');
    }

"""
    text = text[:old_vc_cards_start] + new_vc_cards_fn + text[old_vc_cards_end:]

    # 5. Add populateNavbarQuickMenus support for #navProcessesQuickMenu and visual pillar process flow inside renderDepartmentShowcaseBox
    old_pop_start = text.find("    function populateNavbarQuickMenus() {")
    old_pop_end = text.find("    function togglePersonaJourneyStep(", old_pop_start)
    assert old_pop_start != -1 and old_pop_end != -1

    new_pop_and_showcase = """    function populateNavbarQuickMenus() {
      const pillarsMenu = document.getElementById('navPillarsQuickMenu');
      const processesMenu = document.getElementById('navProcessesQuickMenu');
      const personasMenu = document.getElementById('navPersonasQuickMenu');
      const agentsMenu = document.getElementById('navAgentsQuickMenu');

      if (pillarsMenu) {
        pillarsMenu.innerHTML = Object.values(DEPARTMENTS).map(d => {
          const agCount = Object.values(AGENTS).filter(a => !a.isUniversal && a.deptId === d.id).length;
          return `
            <button type="button" class="nav-quick-item" onclick="goHome(); setTimeout(() => switchVerticalTab('${d.id}'), 40);">
              <span style="display:flex; align-items:center; gap:8px;">
                <span style="width:8px; height:8px; border-radius:50%; background:${d.color};"></span>
                <span>${d.scorBadge || ''} · ${d.name}</span>
              </span>
              <span style="font-size:11px; color:var(--text-secondary);">${d.personaIds.length}P · ${agCount}A</span>
            </button>
          `;
        }).join('');
      }

      if (processesMenu) {
        processesMenu.innerHTML = `
          <button type="button" class="nav-quick-item" style="color:var(--g-blue); font-weight:800;" onclick="scrollToProcessJourneys()">
            <span>🔗 View All 4 End-to-End Processes</span>
            <span>&rarr;</span>
          </button>
          <div class="nav-quick-group-title" style="color:#34a853;">Cross-Pillar End-to-End Process Suites (6 Stages Each)</div>
          ${Object.values(VALUE_CHAINS).map(vc => `
            <button type="button" class="nav-quick-item" onclick="openValueChainPage('${vc.id}', true, event)">
              <span style="display:flex; align-items:center; gap:8px;">
                <span style="width:8px; height:8px; border-radius:50%; background:${vc.color};"></span>
                <span>${vc.shortTitle}</span>
              </span>
              <span style="font-family:var(--font-mono); font-size:11px; color:${vc.color}; font-weight:700;">${vc.headlineStat}</span>
            </button>
          `).join('')}
        `;
      }

      if (personasMenu) {
        let html = `
          <button type="button" class="nav-quick-item" style="color:var(--g-blue); font-weight:800;" onclick="openPersonasDirectoryPage('all', '', true, 'personas')">
            <span>👥 Open Full Personas Directory (29)</span>
            <span>&rarr;</span>
          </button>
        `;
        Object.values(DEPARTMENTS).forEach(d => {
          html += `<div class="nav-quick-group-title" style="color:${d.color};">${d.scorBadge || ''} · ${d.name}</div>`;
          (d.personaIds || []).forEach(pid => {
            const p = PERSONAS[pid];
            if (!p) return;
            html += `
              <button type="button" class="nav-quick-item" onclick="openPersonaPage('${p.id}', true, event)">
                <span>${p.icon} ${p.name}</span>
                <span style="color:${d.color};">&rarr;</span>
              </button>
            `;
          });
        });
        personasMenu.innerHTML = html;
      }

      if (agentsMenu) {
        let html = `
          <button type="button" class="nav-quick-item" style="color:var(--g-blue); font-weight:800;" onclick="openPersonasDirectoryPage('all', '', true, 'agents')">
            <span>🤖 Open Full AI Agents Directory (35)</span>
            <span>&rarr;</span>
          </button>
          <div class="nav-quick-group-title" style="color:#4285f4;">🌐 Universal CSCO Core Agents (4)</div>
        `;
        UNIVERSAL_AGENT_IDS.forEach(uid => {
          const ag = AGENTS[uid];
          if (!ag) return;
          const cls = getAgentBuildClassification(ag);
          html += `
            <button type="button" class="nav-quick-item" onclick="openAgentPage('${ag.id}', true, event)">
              <span>${ag.name}</span>
              <span style="font-size:10.5px; color:${cls.color};">${cls.tier}</span>
            </button>
          `;
        });
        Object.values(DEPARTMENTS).forEach(d => {
          const dAgents = Object.values(AGENTS).filter(a => !a.isUniversal && a.deptId === d.id);
          if (!dAgents.length) return;
          html += `<div class="nav-quick-group-title" style="color:${d.color};">${d.scorBadge || ''} · ${d.name} (${dAgents.length})</div>`;
          dAgents.forEach(ag => {
            const cls = getAgentBuildClassification(ag);
            html += `
              <button type="button" class="nav-quick-item" onclick="openAgentPage('${ag.id}', true, event)">
                <span>${ag.name}</span>
                <span style="font-size:10.5px; color:${cls.color};">${cls.tier}</span>
              </button>
            `;
          });
        });
        agentsMenu.innerHTML = html;
      }
    }

    /* Visual 5-Stage Pillar Process Diagram (No Text Bloat — Pure Visual Flow + Link to Full E2E Process) */
    function renderVisualPillarProcessStrip(dept) {
      const PILLAR_FLOWS = {
        demand_sop: {
          title: '5-Stage S&OP & Demand Consensus Process',
          vcId: 'f2f',
          vcLabel: 'Open Full Forecast-to-Fulfill (F2F) Process &rarr;',
          steps: [
            { icon: '📡', name: '1. POS & Macro Sensing', sub: 'TimesFM + WeatherNext' },
            { icon: '📈', name: '2. Promo & Uplift Shaping', sub: 'Cannibalization Filter' },
            { icon: '🤝', name: '3. CPFR Channel Sync', sub: 'Retail EDI 852 Lock' },
            { icon: '⚖️', name: '4. Supply-Demand Match', sub: 'RCCP Capacity Check' },
            { icon: '🔒', name: '5. Executive S&OP Lock', sub: 'P&L Consensus Plan' }
          ]
        },
        sourcing_procurement: {
          title: '5-Stage Source-to-Pay & Tier-N Resilience Process',
          vcId: 's2p',
          vcLabel: 'Open Full Source-to-Pay (S2P) Process &rarr;',
          steps: [
            { icon: '🕸️', name: '1. Tier-N Graph Mapping', sub: 'Spanner BOM Lineage' },
            { icon: '🧮', name: '2. Parametric Should-Cost', sub: 'Index & Labor Teardown' },
            { icon: '🏆', name: '3. Combinatorial RFQ', sub: 'OR-Tools Split Award' },
            { icon: '🛃', name: '4. HS Tariff & FTA Guard', sub: 'SAP GTS Compliance' },
            { icon: '🔬', name: '5. COA Quality & Settlement', sub: 'Zero-Escape Lot Lock' }
          ]
        },
        manufacturing_prod: {
          title: '5-Stage Finite Production & Plant OEE Process',
          vcId: 'f2f',
          vcLabel: 'Open Full Forecast-to-Fulfill (F2F) Process &rarr;',
          steps: [
            { icon: '🗓️', name: '1. Master Schedule (MPS)', sub: 'Frozen Fence Lock' },
            { icon: '⚙️', name: '2. Finite CP-SAT Sequence', sub: 'Setup Minimization' },
            { icon: '🔧', name: '3. Predictive Asset OEE', sub: 'Spindle & Bearing Guard' },
            { icon: '📷', name: '4. Inline Vision QA Gate', sub: 'Sub-50ms Defect Eject' },
            { icon: '🎯', name: '5. Yield & Scrap Loop', sub: 'Closed-Loop PLC Tune' }
          ]
        },
        inventory_warehouse: {
          title: '5-Stage MEIO Buffer, Yard & 3D Warehouse Process',
          vcId: 'p2r',
          vcLabel: 'Open Full Plan-to-Recovery (P2R) Process &rarr;',
          steps: [
            { icon: '🌐', name: '1. Multi-Echelon MEIO', sub: 'Coupled Safety Stock' },
            { icon: '⚡', name: '2. Sub-50ms Spanner ATP', sub: 'Order Promising Lock' },
            { icon: '🚛', name: '3. Autonomous Yard & Dock', sub: 'Door Sequencing' },
            { icon: '🔄', name: '4. Zero-Putaway Cross-Dock', sub: 'Inbound-to-Outbound' },
            { icon: '📦', name: '5. 3D Golden-Zone Slotting', sub: 'Wave & Pick Path' }
          ]
        },
        logistics_fleet: {
          title: '5-Stage Multi-Modal Global Transit & Last-Mile Process',
          vcId: 'o2d',
          vcLabel: 'Open Full Order-to-Delivery (O2D) Process &rarr;',
          steps: [
            { icon: '🧭', name: '1. Factory Mode-Split', sub: 'Ship / Air / Rail / Road' },
            { icon: '🚢', name: '2. Ocean AIS & Air ULD', sub: 'Port Drayage & 3D ULD' },
            { icon: '🚆', name: '3. Intermodal Rail Linehaul', sub: 'COFC Ramp Sync' },
            { icon: '🚚', name: '4. Maps Fleet & 3D LIFO', sub: 'Axle-Safe Bay Packing' },
            { icon: '🏪', name: '5. Retail Beat & ePOD Audit', sub: 'ShelfVision & Claims' }
          ]
        },
        circular_enable: {
          title: '5-Stage Customer OTIF, Circular RMA & Scope 3 Process',
          vcId: 'p2r',
          vcLabel: 'Open Full Plan-to-Recovery (P2R) Process &rarr;',
          steps: [
            { icon: '🛡️', name: '1. Proactive OTIF Shield', sub: 'Penalty Prevention' },
            { icon: '↩️', name: '2. Fleet Backhaul RMA', sub: 'Zero-Deadhead Pickup' },
            { icon: '🔍', name: '3. Vision RMA Grading', sub: 'Restock vs Harvest' },
            { icon: '♻️', name: '4. Circular Re-Commerce', sub: 'Margin Recovery' },
            { icon: '🌿', name: '5. Scope 3 & CBAM Ledger', sub: 'Audit-Ready Carbon' }
          ]
        }
      };

      const cfg = PILLAR_FLOWS[dept.id] || PILLAR_FLOWS.demand_sop;
      return `
        <div style="margin-top:18px; padding:16px 18px; border-radius:16px; background:rgba(15,23,42,0.55); border:1px solid ${dept.color}44;">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
            <div style="font-size:12.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:${dept.color};">
              ⚡ ${cfg.title}
            </div>
            <button type="button" class="switch-pill" style="padding:5px 12px; font-size:12px; border-color:${dept.color}; color:${dept.color}; font-weight:700;" onclick="openValueChainPage('${cfg.vcId}', true, event)">
              ${cfg.vcLabel}
            </button>
          </div>
          <div style="display:grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap:10px;">
            ${cfg.steps.map((s, idx) => `
              <div style="position:relative; padding:12px 12px; border-radius:12px; background:var(--bg-card); border:1px solid var(--border-subtle); border-top:3px solid ${dept.color}; display:flex; flex-direction:column; gap:4px;">
                <div style="display:flex; align-items:center; justify-content:space-between;">
                  <span style="font-size:18px;">${s.icon}</span>
                  <span style="font-family:var(--font-mono); font-size:10px; font-weight:800; color:${dept.color};">${idx < 4 ? '──▶' : '✓'}</span>
                </div>
                <div style="font-family:var(--font-display); font-size:13px; font-weight:800; color:var(--text-primary); line-height:1.25;">
                  ${s.name}
                </div>
                <div style="font-size:11px; color:var(--text-secondary); font-weight:600;">
                  ${s.sub}
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    function renderDepartmentShowcaseBox() {
      const container = document.getElementById('deptShowcaseContainer');
      if (!container) return;
      if (!selectedDeptId || !DEPARTMENTS[selectedDeptId]) {
        container.innerHTML = '';
        return;
      }
      const dept = DEPARTMENTS[selectedDeptId];
      const pillarAgents = Object.values(AGENTS).filter(a => !a.isUniversal && a.deptId === dept.id);

      container.innerHTML = `
        <div id="deptShowcaseBoxEl" class="dept-showcase-box genie-enter" style="--dept-accent: ${dept.color};">
          <div class="showcase-header">
            <div class="showcase-dept-name">
              <span class="accent-dot" style="background: ${dept.color};"></span>
              <span>${dept.scorBadge || ''} · ${dept.name}</span>
            </div>
            <button type="button" class="switch-pill" onclick="selectDepartment('${dept.id}')">
              ✕ Close
            </button>
          </div>

          <!-- What This Pillar Means -->
          <div class="showcase-visual-strip">
            <div class="showcase-emblem-box">
              ${renderSupplyChainWatermarkSvg(dept.watermarkType, dept.color, 'dept-stage-svg')}
            </div>
            <div class="showcase-visual-meta">
              <div class="showcase-visual-title" style="color:${dept.color};">
                What This Pillar Means
              </div>
              <div class="showcase-visual-desc">
                ${shortSentence(dept.subtitle, 160)}
              </div>
            </div>
          </div>

          <!-- Visual 5-Stage Pillar Process Diagram + Link to Full End-to-End Process Journey -->
          ${renderVisualPillarProcessStrip(dept)}

          <!-- SECTION 1: PRIMARY HIGHLIGHTED HUMAN PERSONAS (Executive Role Cards) -->
          <div style="margin-top: 22px;">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-bottom:14px;">
              <div style="display:flex; align-items:center; gap:10px;">
                <span style="padding:4px 10px; border-radius:8px; background:${dept.color}; color:#ffffff; font-size:11.5px; font-weight:800; letter-spacing:0.06em; text-transform:uppercase;">
                  👤 Human Personas (${dept.personaIds.length})
                </span>
                <span style="font-size:14.5px; font-weight:700; color:var(--text-primary);">
                  Click any supply chain role to open their daily journey
                </span>
              </div>
            </div>

            <div class="persona-cards-grid">
              ${dept.personaIds.map(pid => {
                const p = PERSONAS[pid];
                if (!p) return '';
                return `
                  <div class="human-persona-card"
                       style="--dept-accent: ${dept.color};"
                       onclick="openPersonaPage('${p.id}', true, event)">
                    <div style="display:flex; align-items:center; gap:14px;">
                      <div class="human-avatar-circle" style="--dept-accent: ${dept.color};">${p.icon}</div>
                      <div>
                        <div class="human-role-tag">👤 Human Role</div>
                        <div class="human-persona-title">${p.name}</div>
                        <div class="human-persona-sub">${p.role}</div>
                      </div>
                    </div>
                    <span class="persona-open-arrow" style="color:${dept.color}; font-weight:800;">Open &rarr;</span>
                  </div>
                `;
              }).join('')}
            </div>
          </div>

          <!-- SECTION 2: DISTINCT AI AGENT DOCK (Tech Module Chips) -->
          <div class="ai-agent-dock-box">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-bottom:14px;">
              <div style="display:flex; align-items:center; gap:10px;">
                <span class="ai-agent-type-tag" style="padding:4px 10px; font-size:11px;">
                  ✦ AI Agents (${pillarAgents.length})
                </span>
                <span style="font-size:13.5px; font-weight:700; color:var(--text-secondary);">
                  Autonomous AI copilots &amp; solvers plugging into ${dept.name}
                </span>
              </div>
            </div>

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(245px, 1fr)); gap:12px;">
              ${pillarAgents.map(ag => {
                const cls = getAgentBuildClassification(ag);
                return `
                  <div class="ai-agent-chip-card"
                       onclick="openAgentPage('${ag.id}', true, event)">
                    <div style="display:flex; align-items:center; gap:12px;">
                      <div class="ai-bot-square">✦</div>
                      <div>
                        <div style="display:flex; align-items:center; gap:6px; margin-bottom:3px;">
                          <span class="ai-agent-type-tag">AI Agent</span>
                          <span class="build-tier-badge ${cls.cssClass}" style="font-size:9.5px; padding:1px 7px;">${cls.tier}</span>
                        </div>
                        <div class="ai-agent-chip-title">${ag.name}</div>
                      </div>
                    </div>
                    <span style="color:#818cf8; font-weight:800; font-size:14px;">&rarr;</span>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        </div>
      `;
    }

"""
    text = text[:old_pop_start] + new_pop_and_showcase + text[old_pop_end:]

    # 6. Replace openValueChainPage(vcId) with the Visual End-to-End Process Diagram & Stage Spotlight Studio
    old_vc_page_start = text.find("    function openValueChainPage(vcId, pushHash = true, ev = null) {")
    old_vc_page_end = text.find("    function attachValueChainVideo(event, vcId) {", old_vc_page_start)
    assert old_vc_page_start != -1 and old_vc_page_end != -1

    new_vc_page_fn = """    let currentVcSelectedStageIdx = 0;

    function selectVcStage(vcId, stageIdx) {
      currentVcSelectedStageIdx = stageIdx;
      openValueChainPage(vcId, false, null);
    }

    /* Interactive Full-Width Animated 6-Stage Process Diagram SVG */
    function renderVisualValueChainDiagramSvg(vc, activeIdx) {
      const stages = vc.stages || [];
      const nodePositions = [42, 224, 406, 588, 770, 952];

      const stageIcons = {
        f2f: ['📡', '📈', '⚖️', '🌐', '🕸️', '📦'],
        o2d: ['🧭', '🚢', '✈️', '🚆', '🚚', '🛡️'],
        s2p: ['🕸️', '🧮', '🏆', '🛃', '🔬', '💳'],
        p2r: ['🛒', '🚛', '📦', '↩️', '📷', '♻️']
      };
      const icons = stageIcons[vc.id] || ['01', '02', '03', '04', '05', '06'];

      const nodesSvg = stages.map((st, idx) => {
        const x = nodePositions[idx] || (42 + idx * 182);
        const isAct = idx === activeIdx;
        const shortTitle = st.name.split('&')[0].replace(/Multi-Signal |Autonomous |Multi-Echelon |Multi-Tier |3D |Factory Gate |Ocean Vessel |Air Cargo |Intermodal Rail |Google Maps |Multi-Modal /g, '').trim();
        const titleLine1 = shortTitle.slice(0, 19);
        const titleLine2 = shortTitle.length > 19 ? shortTitle.slice(19, 36) : '';
        const sysFirst = (st.systems || '').split('·')[0].trim().slice(0, 18);
        const modShort = (st.modality || '').slice(0, 18);

        return `
          <g style="cursor:pointer;" onclick="selectVcStage('${vc.id}', ${idx})">
            <!-- Active Outer Glow Ring -->
            ${isAct ? `
              <rect x="${x - 5}" y="83" width="176" height="194" rx="18"
                    fill="none" stroke="${st.color}" stroke-width="2.5" stroke-dasharray="6 4" />
            ` : ''}
            <!-- Stage Node Box -->
            <rect x="${x}" y="88" width="166" height="184" rx="15"
                  fill="${isAct ? '#172542' : '#0f172a'}"
                  stroke="${isAct ? '#ffffff' : st.color}"
                  stroke-width="${isAct ? '2.5' : '1.6'}" />
            <!-- Top Color Header Strip -->
            <rect x="${x}" y="88" width="166" height="32" rx="15" fill="${st.color}28" />
            <text x="${x + 14}" y="109" fill="${st.color}" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="800">
              STAGE 0${idx + 1}
            </text>
            <text x="${x + 148}" y="110" text-anchor="end" font-size="15">${icons[idx] || '⚡'}</text>

            <!-- Stage Name -->
            <text x="${x + 83}" y="142" text-anchor="middle" fill="#ffffff" font-family="'Google Sans Display', sans-serif" font-size="13" font-weight="800">
              ${titleLine1}
            </text>
            ${titleLine2 ? `
              <text x="${x + 83}" y="158" text-anchor="middle" fill="#ffffff" font-family="'Google Sans Display', sans-serif" font-size="12.5" font-weight="800">
                ${titleLine2}
              </text>
            ` : ''}

            <!-- AI Solver Pill -->
            <rect x="${x + 12}" y="172" width="142" height="24" rx="6" fill="#090d16" stroke="${st.color}66" stroke-width="1" />
            <text x="${x + 83}" y="188" text-anchor="middle" fill="#a5b4fc" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="700">
              ✦ ${modShort}
            </text>

            <!-- Enterprise System Pill -->
            <rect x="${x + 12}" y="203" width="142" height="22" rx="6" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.12)" stroke-width="1" />
            <text x="${x + 83}" y="218" text-anchor="middle" fill="#e2e8f0" font-family="'Google Sans Text', sans-serif" font-size="10" font-weight="600">
              ${sysFirst}
            </text>

            <!-- Cycle Time Badge -->
            <rect x="${x + 28}" y="236" width="110" height="22" rx="11" fill="rgba(52,168,83,0.18)" stroke="#34a853" stroke-width="1" />
            <text x="${x + 83}" y="251" text-anchor="middle" fill="#81c995" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="800">
              ⚡ ${st.afterTime}
            </text>
          </g>
        `;
      }).join('');

      const connectorsSvg = [0, 1, 2, 3, 4].map(idx => {
        const x1 = nodePositions[idx] + 166;
        const x2 = nodePositions[idx + 1];
        const col = stages[idx] ? stages[idx].color : vc.color;
        return `
          <g>
            <path id="vcConn_${vc.id}_${idx}" d="M${x1},180 L${x2},180"
                  stroke="${col}" stroke-width="2.2" stroke-dasharray="4 3" fill="none" />
            <polygon points="${x2},180 ${x2 - 6},176 ${x2 - 6},184" fill="${col}" />
            <circle r="3.5" fill="#ffffff">
              <animateMotion dur="${1.4 + idx * 0.15}s" repeatCount="indefinite" path="M${x1},180 L${x2},180" />
            </circle>
          </g>
        `;
      }).join('');

      return `
        <div class="simple-arch-card" style="margin-bottom: 22px;">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
            <div>
              <div style="font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${vc.color};">
                ✦ Interactive End-to-End Process Architecture Diagram
              </div>
              <div style="font-family:var(--font-display); font-size:20px; font-weight:800; color:var(--text-primary);">
                6-Stage Connected Golden Thread Pipeline (Click Any Stage Node to Inspect)
              </div>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="pt-side-tag" style="border-color:${vc.color}66; color:${vc.color};">⚡ Cycle: ${vc.headlineStat}</span>
              <span class="pt-side-tag">6 Connected Stages</span>
            </div>
          </div>

          <div class="simple-arch-svg-wrap">
            <svg viewBox="0 0 1160 335" style="width:100%; height:auto; display:block;" role="img" aria-label="${vc.title} 6-Stage Process Diagram">
              <defs>
                <pattern id="vcGrid_${vc.id}" width="28" height="28" patternUnits="userSpaceOnUse">
                  <path d="M 28 0 L 0 0 0 28" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="1" />
                </pattern>
              </defs>
              <rect width="1160" height="335" rx="14" fill="url(#vcGrid_${vc.id})" />

              <!-- Top 3 Synchronized Enterprise Flow Ribbons -->
              <g>
                <rect x="42" y="18" width="340" height="26" rx="13" fill="rgba(66,133,244,0.14)" stroke="#4285f4" stroke-width="1" />
                <text x="212" y="35" text-anchor="middle" fill="#93c5fd" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700">
                  FLOW 1 · PHYSICAL MATERIAL &amp; INVENTORY ──▶
                </text>

                <rect x="410" y="18" width="340" height="26" rx="13" fill="rgba(52,168,83,0.14)" stroke="#34a853" stroke-width="1" />
                <text x="580" y="35" text-anchor="middle" fill="#86efac" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700">
                  FLOW 2 · GOLDEN THREAD DATA HANDOFF ⚡ ──▶
                </text>

                <rect x="778" y="18" width="340" height="26" rx="13" fill="rgba(168,85,247,0.14)" stroke="#a855f7" stroke-width="1" />
                <text x="948" y="35" text-anchor="middle" fill="#d8b4fe" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700">
                  FLOW 3 · CLOSED-LOOP DIGITAL TWIN SYNC ◀──▶
                </text>
              </g>

              <!-- Stage-to-Stage Animated Connectors -->
              ${connectorsSvg}

              <!-- 6 Interactive Stage Nodes -->
              ${nodesSvg}

              <!-- Bottom Closed-Loop Digital Twin Feedback Conduit (Stage 06 -> Stage 01) -->
              <path d="M1035,272 L1035,312 L125,312 L125,272"
                    stroke="${vc.color}" stroke-width="1.6" stroke-dasharray="6 4" fill="none" opacity="0.75" />
              <polygon points="125,272 121,280 129,280" fill="${vc.color}" />
              <circle r="3.5" fill="${vc.color}">
                <animateMotion dur="4.2s" repeatCount="indefinite" path="M1035,272 L1035,312 L125,312 L125,272" />
              </circle>
              <rect x="420" y="299" width="320" height="22" rx="11" fill="#0b1120" stroke="${vc.color}66" stroke-width="1" />
              <text x="580" y="314" text-anchor="middle" fill="#e2e8f0" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="700">
                🔄 CLOSED-LOOP BIGQUERY &amp; SPANNER DIGITAL TWIN FEEDBACK
              </text>
            </svg>
          </div>
        </div>
      `;
    }

    function openValueChainPage(vcId, pushHash = true, ev = null) {
      const vc = VALUE_CHAINS[vcId];
      if (!vc) return;
      const useSlide = isPillOrNavSwitch(ev);
      const sRect = useSlide ? null : getClickedCardRect(ev);
      const transClass = getPageTransitionClass(ev, sRect);

      const videoUrl = customVcVideos[vc.id] || vc.videoSrc;
      const showVideoPlayer = vc.hasPreloadedVideo || Boolean(customVcVideos[vc.id]);
      const wmType = getVcWatermarkType(vc.id);

      if (pushHash) {
        currentVcSelectedStageIdx = 0;
        history.pushState({ page: 'valuechain', id: vcId }, '', `#valuechain/${vcId}`);
      }

      const stages = vc.stages || [];
      if (currentVcSelectedStageIdx >= stages.length) currentVcSelectedStageIdx = 0;
      const activeStage = stages[currentVcSelectedStageIdx] || stages[0];
      const ownerPersona = PERSONAS[activeStage.ownerId];
      const ownerDept = ownerPersona ? (DEPARTMENTS[ownerPersona.deptId] || { color: vc.color }) : { color: vc.color };
      const stageAgentId = (ownerPersona && ownerPersona.agentIds && ownerPersona.agentIds[0]) ? ownerPersona.agentIds[0] : 'demand_sensing_agent';
      const stageAgent = AGENTS[stageAgentId] || Object.values(AGENTS)[0];
      const stageAgentCls = getAgentBuildClassification(stageAgent);

      const container = document.getElementById('valueChainPageContent');
      container.innerHTML = `
        <div id="vcGenieWrap" class="${transClass}">
          <div class="back-bar">
            <button type="button" class="back-btn" onclick="goToOrgChart()">
              <span>&larr;</span>
              <span>Back to CSCO Org Chart</span>
            </button>

            <div class="persona-switcher-pills">
              ${Object.values(VALUE_CHAINS).map(other => `
                <button type="button"
                        class="switch-pill ${other.id === vc.id ? 'active' : ''}"
                        style="${other.id === vc.id ? `background:${other.color}; border-color:${other.color}; color:#040810; font-weight:700;` : ''}"
                        onclick="openValueChainPage('${other.id}', true, event)">
                  ${other.shortTitle}
                </button>
              `).join('')}
            </div>
          </div>

          <!-- Compact Visual Process Header -->
          <div class="persona-header-card" style="border-color: ${vc.color}44; padding: 24px 28px; margin-bottom: 22px;">
            ${renderSupplyChainWatermarkSvg(wmType, vc.color, 'persona-header-sc-watermark')}

            <div style="position:relative; z-index:2;">
              <div class="persona-badge" style="background: ${vc.color}22; color: ${vc.color}; border: 1px solid ${vc.color}55;">
                <span>🔗 ${vc.flowBadge}</span>
              </div>
              <h1 class="persona-page-title" style="font-size:clamp(24px, 2.8vw, 34px); margin-bottom:6px;">${vc.title}</h1>
              <div class="persona-focus-pills" style="margin-top:8px;">
                ${vc.focusAreas.map(f => `<span class="focus-pill">${f}</span>`).join('')}
              </div>
            </div>

            <div class="persona-stat-highlight" style="border-color: ${vc.color}44;">
              <div class="persona-stat-value" style="color: ${vc.color};">${vc.headlineStat}</div>
              <div class="persona-stat-label">${vc.headlineLabel}</div>
            </div>
          </div>

          <!-- 1. FULL-WIDTH INTERACTIVE 6-STAGE ANIMATED PROCESS ARCHITECTURE DIAGRAM -->
          ${renderVisualValueChainDiagramSvg(vc, currentVcSelectedStageIdx)}

          <!-- 2. INTERACTIVE STAGE SPOTLIGHT SCHEMATIC (3-Node Visual Flow + Distinct Persona & Agent Cards) -->
          <div class="vc-spotlight-card" style="--vc-accent: ${activeStage.color || vc.color};">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
              <div style="display:flex; align-items:center; gap:10px;">
                <span style="padding:4px 12px; border-radius:8px; background:${activeStage.color || vc.color}; color:#041019; font-family:var(--font-mono); font-size:12px; font-weight:800;">
                  ${activeStage.num.toUpperCase()} SPOTLIGHT
                </span>
                <h2 style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary); margin:0;">
                  ${activeStage.name}
                </h2>
              </div>
              <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
                ${stages.map((st, idx) => `
                  <button type="button"
                          class="switch-pill"
                          style="padding:5px 11px; font-size:11.5px; ${idx === currentVcSelectedStageIdx ? `background:${st.color}; color:#041019; font-weight:800; border-color:${st.color};` : ''}"
                          onclick="selectVcStage('${vc.id}', ${idx})">
                    0${idx + 1}
                  </button>
                `).join('')}
              </div>
            </div>

            <!-- 3-Node Visual Stage Flow Schematic (Systems -> Autonomous AI Engine -> Golden Thread Output) -->
            <div class="vc-schematic-row" style="--vc-accent: ${activeStage.color || vc.color};">
              <div class="vc-schematic-node" style="border-left: 4px solid #38bdf8;">
                <div style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:#38bdf8; text-transform:uppercase;">
                  📥 1. Stage Input &amp; Systems
                </div>
                <div style="display:flex; flex-wrap:wrap; gap:6px; margin:4px 0;">
                  ${toSysArray(activeStage.systems).map(s => `
                    <span class="pt-side-tag" style="font-size:11.5px;">${s}</span>
                  `).join('')}
                </div>
                <div style="font-size:12.5px; color:var(--text-secondary);">
                  Live telemetry &amp; ERP state ingested into Digital Twin.
                </div>
              </div>

              <div class="vc-schematic-arrow">──⚡──▶</div>

              <div class="vc-schematic-node" style="border-left: 4px solid ${activeStage.color || vc.color};">
                <div style="display:flex; align-items:center; justify-content:space-between; gap:8px;">
                  <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:${activeStage.color || vc.color}; text-transform:uppercase;">
                    🧠 2. AI Process Engine (${activeStage.modality})
                  </span>
                  <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:#34a853;">
                    ${activeStage.toilTime} &rarr; ${activeStage.afterTime}
                  </span>
                </div>
                <div style="font-size:14px; font-weight:600; color:var(--text-primary); line-height:1.45;">
                  ${shortSentence(activeStage.after, 130)}
                </div>
              </div>

              <div class="vc-schematic-arrow">──🔗──▶</div>

              <div class="vc-schematic-node" style="border-left: 4px solid #34a853;">
                <div style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:#34a853; text-transform:uppercase;">
                  📤 3. Golden Thread Handoff
                </div>
                <div style="font-size:13.5px; font-weight:600; color:var(--text-primary); line-height:1.45;">
                  ${shortSentence(activeStage.goldenThread, 125)}
                </div>
              </div>
            </div>

            <!-- Distinct Human Persona Owner Card vs. AI Agent Card for This Stage -->
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:16px; padding-top:14px; border-top:1px solid var(--border-subtle);">
              ${ownerPersona ? `
                <div class="human-persona-card"
                     style="--dept-accent: ${ownerDept.color}; padding: 14px 18px;"
                     onclick="openPersonaPage('${ownerPersona.id}', true, event)">
                  <div style="display:flex; align-items:center; gap:12px;">
                    <div class="human-avatar-circle" style="--dept-accent: ${ownerDept.color}; width:42px; height:42px; font-size:20px;">${ownerPersona.icon}</div>
                    <div>
                      <div class="human-role-tag">👤 Stage Owner (Human Persona)</div>
                      <div class="human-persona-title" style="font-size:16px;">${ownerPersona.name}</div>
                      <div class="human-persona-sub" style="font-size:12px;">${ownerPersona.role}</div>
                    </div>
                  </div>
                  <span style="color:${ownerDept.color}; font-weight:800; font-size:13px;">Persona &rarr;</span>
                </div>
              ` : ''}

              ${stageAgent ? `
                <div class="ai-agent-chip-card"
                     style="padding: 14px 18px;"
                     onclick="openAgentPage('${stageAgent.id}', true, event)">
                  <div style="display:flex; align-items:center; gap:12px;">
                    <div class="ai-bot-square" style="width:40px; height:40px;">✦</div>
                    <div>
                      <div style="display:flex; align-items:center; gap:6px; margin-bottom:3px;">
                        <span class="ai-agent-type-tag">✦ Stage AI Agent</span>
                        <span class="build-tier-badge ${stageAgentCls.cssClass}" style="font-size:9.5px; padding:1px 7px;">${stageAgentCls.tier}</span>
                      </div>
                      <div class="ai-agent-chip-title" style="font-size:16px;">${stageAgent.name}</div>
                    </div>
                  </div>
                  <span style="color:#818cf8; font-weight:800; font-size:13px;">Agent Studio &rarr;</span>
                </div>
              ` : ''}
            </div>
          </div>

          <!-- 3. ALL 6 STAGES AT-A-GLANCE VISUAL PIPELINE STRIP -->
          <div style="margin-bottom: 10px; display:flex; align-items:center; justify-content:space-between;">
            <h3 style="font-family:var(--font-display); font-size:17px; font-weight:800; color:var(--text-primary);">
              All 6 Process Stages (Click Any Card to Focus Diagram)
            </h3>
          </div>
          <div class="vc-pipeline-strip-grid">
            ${stages.map((st, idx) => {
              const isAct = idx === currentVcSelectedStageIdx;
              return `
                <div class="vc-pipe-step-card ${isAct ? 'active' : ''}"
                     style="--st-color: ${st.color};"
                     onclick="selectVcStage('${vc.id}', ${idx})">
                  <div>
                    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:6px;">
                      <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:${st.color};">${st.num}</span>
                      <span style="font-family:var(--font-mono); font-size:10.5px; color:#34a853; font-weight:700;">⚡ ${st.afterTime}</span>
                    </div>
                    <div style="font-family:var(--font-display); font-size:14.5px; font-weight:800; color:var(--text-primary); line-height:1.25; margin-bottom:8px;">
                      ${st.name}
                    </div>
                  </div>
                  <div style="display:flex; flex-direction:column; gap:5px;">
                    <span class="pt-side-tag" style="font-size:10.5px; justify-content:center;">✦ ${st.modality}</span>
                    <span style="font-size:11.5px; font-weight:700; color:${st.color}; text-align:center;">
                      👤 ${st.ownerLabel}
                    </span>
                  </div>
                </div>
              `;
            }).join('')}
          </div>

          <!-- 4. INTERACTIVE SIMULATION & VIDEO WALKTHROUGH -->
          <h2 class="block-title" style="font-size:20px; margin-bottom: 10px;">Interactive Process Simulation &amp; Demo Walkthrough</h2>
          <div class="video-stage-box">
            <div class="video-viewport">
              ${renderStageViewportHtml(vc, 'vc', videoUrl, showVideoPlayer)}
            </div>

            <div class="video-toolbar">
              <span>${stageViewMode === 'cad' ? `Interactive Vector CAD Studio: ${vc.title}` : `End-to-End Recording: ${vc.title}`}</span>
              <div style="display:flex; flex-wrap:wrap; gap:8px;">
                <button type="button" class="upload-video-btn ${stageViewMode==='cad'?'active':''}"
                        onclick="stageViewMode='cad';openValueChainPage('${vc.id}', false)">
                  <span>✦ Interactive CAD Simulator</span>
                </button>
                <button type="button" class="upload-video-btn ${stageViewMode==='video'?'active':''}"
                        onclick="stageViewMode='video';openValueChainPage('${vc.id}', false)">
                  <span>▶ Watch Walkthrough (.mp4)</span>
                </button>
                <label class="upload-video-btn">
                  <span>Swap Local .mp4</span>
                  <input type="file" accept="video/*" style="display:none;" onchange="attachValueChainVideo(event, '${vc.id}')" />
                </label>
              </div>
            </div>
          </div>
        </div>
      `;

      hydrateAssets();
      showActivePage('pageValueChain');
      const wrap = document.getElementById('vcGenieWrap');
      if (sRect && wrap) {
        animateGenieOutOfBox(sRect, wrap, vc.color);
      }
    }

"""
    text = text[:old_vc_page_start] + new_vc_page_fn + text[old_vc_page_end:]

    # 7. Ensure DOMContentLoaded calls populateNavbarQuickMenus() and renderValueChainEntryCards()
    old_dom_init = """      initPortalTheme();
      hydrateAssets();
      initHeroSupplyChainCanvas();
      renderOrgChart();
      hydrateAssets();
      handleUrlHash();"""
    new_dom_init = """      initPortalTheme();
      hydrateAssets();
      initHeroSupplyChainCanvas();
      renderOrgChart();
      renderValueChainEntryCards();
      populateNavbarQuickMenus();
      hydrateAssets();
      handleUrlHash();"""
    if "renderValueChainEntryCards();\n      populateNavbarQuickMenus();" not in text:
        assert old_dom_init in text, "Could not locate DOMContentLoaded init block"
        text = text.replace(old_dom_init, new_dom_init, 1)

    BUILD_PY.write_text(text, encoding="utf-8")
    print("Successfully updated build_site.py with Visual Process Journeys (F2F, O2D, S2P, P2R)!")


if __name__ == "__main__":
    main()

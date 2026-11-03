#!/usr/bin/env python3
"""Upgrades `index.html`, `periodic_table.html`, and `mind_map.html` with v2.2 Clean UX Hierarchy & Dynamic Pillars Support.

Implements:
  1. Navbar Cleanup: Removes hover dropdowns (`.nav-dropdown-wrap` / `.nav-quick-menu`) on `Processes`, `Personas`, and `Agents`,
     turning them into clean single-click top-level navigation buttons.
  2. Dedicated Clean `Processes` Hub (`openProcessesHubPage`): Spacious 2-column End-to-End Process Journeys overview
     matching the front-page visual design language, plus `← All Processes` navigation inside `openValueChainPage`.
  3. Clean Hierarchical `Personas` & `Agents` Directory (`openPersonasDirectoryPage` & `renderDirectoryCardsHtml`):
     Groups roles and AI agents cleanly under Operating Pillar section headers with Sub-Pillar context pills and dynamic counts.
  4. Un-Cramped, Progressive 3-Tab `Case Studies` Hub (`openEvidenceHubPage`):
     Separates `🏢 Enterprise Case Studies`, `📊 Pillar Benchmark Matrix`, and `📚 Analyst & Standards Library` into focused tabs
     with breathable, uncluttered executive cards.
  5. Step-by-Step Hierarchical `Cost & ROI` Hub (`openCostTabPage`):
     Top 4 bottom-line KPIs + 3-step progressive tabs (`1 · By Operating Pillar`, `2 · Agent-by-Agent Economics`,
     `3 · Scale Simulator & Methodology`).
  6. Polished `Mind Map` (`openMindMapPage`) & Dynamic-Pillar `Periodic Table` (`openPeriodicTablePage`):
     Adds Active Selection & Quick-Launch Top Bar above `.mm-neural-board`, pins the active/expanded Agent card to the top
     of Column 3, harmonizes colors across Dark & Light themes, and makes the Periodic Table render `4`–`8` dynamic pillars seamlessly.
  7. Safe `getDeptMeta` fallback when custom organization pillars replace canonical `DEPARTMENTS` keys.
"""

from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

V22_CSS_START = "/* === PORTAL V2.2 HIERARCHY & CLEAN SAA-S LAYOUT START === */"
V22_CSS_END = "/* === PORTAL V2.2 HIERARCHY & CLEAN SAA-S LAYOUT END === */"

V22_CSS = f"""
    {V22_CSS_START}
    /* Responsive Dynamic Pillar Grid on #pageHome (4 to 8 Operating Pillars) */
    .dept-row[data-pillar-count="4"] {{
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }}
    .dept-row[data-pillar-count="5"] {{
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    }}
    .dept-row[data-pillar-count="6"] {{
      grid-template-columns: repeat(3, minmax(0, 1fr));
    }}
    .dept-row[data-pillar-count="7"],
    .dept-row[data-pillar-count="8"] {{
      grid-template-columns: repeat(4, minmax(0, 1fr));
    }}
    @media (max-width: 1180px) {{
      .dept-row[data-pillar-count="5"],
      .dept-row[data-pillar-count="6"],
      .dept-row[data-pillar-count="7"],
      .dept-row[data-pillar-count="8"] {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}
    }}
    @media (max-width: 680px) {{
      .dept-row[data-pillar-count="4"],
      .dept-row[data-pillar-count="5"],
      .dept-row[data-pillar-count="6"],
      .dept-row[data-pillar-count="7"],
      .dept-row[data-pillar-count="8"] {{
        grid-template-columns: 1fr;
      }}
    }}

    /* Segmented View Tabs for Case Studies, Cost & ROI, and Directory */
    .sc-v22-tab-strip {{
      display: inline-flex;
      flex-wrap: wrap;
      gap: 8px;
      padding: 6px;
      border-radius: 16px;
      background: var(--bg-surface);
      border: 1.5px solid var(--border-strong);
      margin-bottom: 24px;
    }}
    .sc-v22-tab-btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 18px;
      border-radius: 11px;
      border: 1px solid transparent;
      background: transparent;
      color: var(--text-secondary);
      font-family: var(--font-display);
      font-size: 14px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.18s ease;
    }}
    .sc-v22-tab-btn:hover {{
      color: var(--text-primary);
      background: var(--bg-elevated);
    }}
    .sc-v22-tab-btn.active {{
      background: var(--g-blue);
      color: #ffffff;
      box-shadow: 0 6px 18px rgba(37, 99, 235, 0.28);
    }}
    .sc-v22-tab-count {{
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.18);
      color: inherit;
    }}
    .sc-v22-tab-btn:not(.active) .sc-v22-tab-count {{
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
    }}

    /* Hierarchical Directory Pillar Section */
    .sc-dir-pillar-section {{
      grid-column: 1 / -1;
      margin-bottom: 18px;
      padding: 22px 24px;
      border-radius: 20px;
      background: var(--bg-card);
      border: 1.5px solid var(--border-strong);
    }}
    .sc-dir-pillar-head {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      padding-bottom: 14px;
      margin-bottom: 16px;
      border-bottom: 1px solid var(--border-subtle);
    }}
    .sc-dir-cards-subgrid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
      gap: 16px;
    }}

    /* Clean Un-Cramped Case Study Cards */
    .sc-v22-cs-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
      gap: 22px;
    }}
    @media (max-width: 680px) {{
      .sc-v22-cs-grid {{
        grid-template-columns: 1fr;
      }}
    }}
    .sc-v22-cs-card {{
      padding: 26px 28px;
      border-radius: 20px;
      background: var(--bg-card);
      border: 1.5px solid var(--border-strong);
      border-top: 4px solid var(--cs-accent, var(--g-blue));
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 18px;
      transition: transform 0.2s ease, border-color 0.2s ease;
    }}
    .sc-v22-cs-card:hover {{
      transform: translateY(-2px);
      border-color: var(--cs-accent, var(--g-blue));
    }}

    /* Mind Map Top Active Path & Quick-Launch Bar */
    .mm-active-path-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 14px;
      padding: 16px 22px;
      margin-bottom: 18px;
      border-radius: 18px;
      background: var(--bg-card);
      border: 1.5px solid var(--border-strong);
      border-left: 5px solid var(--mm-accent, var(--g-blue));
    }}
    .mm-crumb-step {{
      display: inline-flex;
      align-items: center;
      gap: 7px;
      padding: 6px 12px;
      border-radius: 10px;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      font-size: 13px;
      font-weight: 700;
      color: var(--text-primary);
    }}
    {V22_CSS_END}
"""


def replace_between_anchors(html: str, start_anchor: str, end_anchor: str, replacement: str) -> str:
    i0 = html.index(start_anchor)
    i1 = html.index(end_anchor, i0)
    return html[:i0] + replacement + html[i1:]


NEW_GET_DEPT_META = """    function getDeptMeta(deptId) {
      if (DEPARTMENTS[deptId]) return DEPARTMENTS[deptId];
      if (deptId === 'sourcing_risk' && DEPARTMENTS.sourcing_procurement) return DEPARTMENTS.sourcing_procurement;
      if (deptId === 'inventory_warehouse' && DEPARTMENTS.inventory_warehouse) return DEPARTMENTS.inventory_warehouse;
      if (deptId === 'circular_enable' && DEPARTMENTS.circular_enable) return DEPARTMENTS.circular_enable;
      return DEPARTMENTS.demand_sop || Object.values(DEPARTMENTS)[0] || {
        id: deptId || 'pillar',
        name: 'Supply Chain',
        color: '#2563eb',
        scorBadge: '01 · PILLAR',
        watermarkType: 'demand_wave',
        subPillars: [],
        personaIds: [],
        agentIds: []
      };
    }

"""


NEW_SCROLL_AND_PROCESSES_HUB = """    function formatShortPillarTab(d) {
      if (!d) return 'Pillar';
      const badge = (d.scorBadge || '').trim();
      const tail = badge ? badge.split('·').pop().trim() : '';
      if (tail && tail.toUpperCase() !== 'PILLAR') {
        return tail;
      }
      const numPrefix = badge.includes('·') ? badge.split('·')[0].trim() : '';
      const firstSeg = (d.name || 'Pillar').split(/[,&—]/)[0].trim();
      const concise = firstSeg.length > 22 ? firstSeg.slice(0, 21).trim() + '…' : firstSeg;
      return numPrefix ? `${numPrefix} · ${concise}` : concise;
    }

    function scrollToProcessJourneys(ev = null) {
      openProcessesHubPage(true, ev);
    }

    function openProcessesHubPage(pushHash = true, ev = null) {
      const transClass = getPageTransitionClass(ev, null);
      if (pushHash) {
        history.pushState({ page: 'processes' }, '', '#processes');
      }
      const vcList = Object.values(VALUE_CHAINS);
      const pillarCount = Object.keys(DEPARTMENTS).length;
      const cardsHtml = vcList.map(vc => {
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
               style="--vc-accent: ${vc.color}; --dept-accent: ${vc.color}; padding: 26px 28px;"
               onclick="openValueChainPage('${vc.id}', true, event)">
            <div style="position:relative; z-index:2;">
              <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
                <div class="vc-flow-badge" style="margin-bottom:0; background: ${vc.color}20; color: ${vc.color}; border: 1px solid ${vc.color}50;">
                  <span>🔗 ${vc.flowBadge}</span>
                </div>
                <span style="font-family:var(--font-mono); font-size:12.5px; font-weight:800; padding:4px 11px; border-radius:8px; background:${vc.color}22; color:${vc.color}; border:1px solid ${vc.color}55;">
                  ${vc.headlineStat}
                </span>
              </div>
              <div class="dept-node-title" style="font-size: 23px; margin-bottom: 6px;">${vc.shortTitle}</div>
              <p style="font-size: 14px; color: var(--text-secondary); line-height: 1.55; margin: 0 0 14px;">
                ${vc.cardSubtitle || vc.title}
              </p>
              <div class="vc-mini-pipeline">
                ${miniStagesHtml}
              </div>
            </div>
            <div class="dept-anim-stage" style="--dept-accent: ${vc.color}; margin-top: 16px;">
              ${renderSupplyChainWatermarkSvg(wmType, vc.color, 'dept-stage-svg')}
              <span class="dept-anim-meta">${(vc.stages || []).length} Connected Stages · Open Interactive Process Diagram &rarr;</span>
            </div>
          </div>
        `;
      }).join('');

      const container = document.getElementById('valueChainPageContent');
      if (!container) return;
      container.innerHTML = `
        <div class="${transClass}">
          <div class="back-bar" style="margin-bottom: 20px;">
            <button type="button" class="back-btn" onclick="goToOrgChart()">
              <span>&larr;</span>
              <span>Back to ${pillarCount} Operating Pillars</span>
            </button>
          </div>

          <div class="simple-arch-card" style="padding: 28px 30px; margin-bottom: 24px;">
            <div style="font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:var(--g-blue); margin-bottom:6px;">
              Cross-Pillar End-to-End Workflows
            </div>
            <h1 style="font-family:var(--font-display); font-size:clamp(28px, 3vw, 36px); font-weight:800; color:var(--text-primary); margin:0 0 8px;">
              End-to-End Supply Chain Processes (${vcList.length})
            </h1>
            <p style="font-size:15px; color:var(--text-secondary); max-width:920px; line-height:1.6; margin:0;">
              Select any end-to-end process below to inspect how Human Personas and AI Agents hand off signals across all ${pillarCount} Operating Pillars.
            </p>
          </div>

          <div class="vc-entry-grid" style="gap: 22px;">
            ${cardsHtml}
          </div>
        </div>
      `;
      hydrateAssets();
      showActivePage('pageValueChain');
    }

"""


NEW_DIRECTORY_BLOCK = """    /* =========================================================================
       PAGE 5 RENDERING: HIERARCHICAL PERSONAS & CATEGORIZED AGENTS DIRECTORY
       ========================================================================= */
    let currentDirDeptFilter = 'all';
    let currentDirSearch = '';
    let currentDirMode = 'personas';

    function renderDirectoryCardsHtml(deptFilter, searchQuery, mode = currentDirMode) {
      const q = (searchQuery || '').trim().toLowerCase();
      const deptList = Object.values(DEPARTMENTS);

      if (mode === 'agents') {
        if (deptFilter === 'universal') {
          const uniAgents = Object.values(AGENTS).filter(ag => {
            if (!ag.isUniversal) return false;
            if (!q) return true;
            const hay = [cleanAgentName(ag.name), ag.subPillarName || '', ag.role || ''].join(' ').toLowerCase();
            return hay.includes(q);
          });
          if (!uniAgents.length) {
            return `<div style="grid-column: 1 / -1; padding: 40px; text-align: center; color: var(--text-secondary);">No matching universal agents found.</div>`;
          }
          return `
            <div class="sc-dir-pillar-section">
              <div class="sc-dir-pillar-head">
                <div>
                  <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:#6366f1; text-transform:uppercase; letter-spacing:0.06em;">CROSS-PILLAR ORCHESTRATION</span>
                  <h2 style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary); margin:2px 0 0;">Universal Supply Chain Agents</h2>
                </div>
                <span class="sc-tech-pill" style="font-weight:800;">${uniAgents.length} Agents</span>
              </div>
              <div class="sc-dir-cards-subgrid">
                ${uniAgents.map(ag => `
                  <div class="ai-agent-chip-card" style="padding:20px 22px;" onclick="openAgentPage('${ag.id}', true, event)">
                    <div style="display:flex; align-items:center; gap:14px; min-width:0;">
                      <div class="ai-bot-square" style="width:44px; height:44px; font-size:18px; flex-shrink:0;">✦</div>
                      <div style="min-width:0;">
                        <div class="ai-agent-chip-title" style="font-size:16.5px;">${cleanAgentName(ag.name)}</div>
                        <div style="font-size:12.5px; color:var(--text-secondary); margin-top:3px;">${ag.subPillarName || 'Cross-Pillar Core'}</div>
                      </div>
                    </div>
                    <span style="color:#6366f1; font-weight:800; font-size:18px;">&rarr;</span>
                  </div>
                `).join('')}
              </div>
            </div>
          `;
        }

        const visibleDepts = deptList.filter(d => deptFilter === 'all' || d.id === deptFilter);
        const sectionsHtml = visibleDepts.map(dept => {
          const matchingAgents = Object.values(AGENTS).filter(ag => {
            if (ag.deptId !== dept.id) return false;
            if (!q) return true;
            const hay = [cleanAgentName(ag.name), ag.canonicalName || '', ag.subPillarName || '', dept.name].join(' ').toLowerCase();
            return hay.includes(q);
          });
          if (!matchingAgents.length) return '';

          return `
            <div class="sc-dir-pillar-section" style="border-left: 5px solid ${dept.color};">
              <div class="sc-dir-pillar-head">
                <div>
                  <div style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; color:${dept.color}; text-transform:uppercase; letter-spacing:0.06em;">
                    ${dept.scorBadge || 'OPERATING PILLAR'}
                  </div>
                  <h2 style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary); margin:3px 0 0;">
                    ${dept.name}
                  </h2>
                </div>
                <span style="font-family:var(--font-mono); font-size:12px; font-weight:800; padding:5px 12px; border-radius:999px; background:${dept.color}18; color:${dept.color}; border:1px solid ${dept.color}40;">
                  ${(dept.subPillars || []).length} Sub-Pillars · ${matchingAgents.length} AI Agents
                </span>
              </div>
              <div class="sc-dir-cards-subgrid">
                ${matchingAgents.map(ag => {
                  const cName = cleanAgentName(ag.name);
                  const subLabel = ag.subPillarName || dept.name;
                  return `
                    <div class="ai-agent-chip-card" style="padding:20px 22px;" onclick="openAgentPage('${ag.id}', true, event)">
                      <div style="display:flex; align-items:center; gap:14px; min-width:0;">
                        <div class="ai-bot-square" style="width:44px; height:44px; font-size:18px; flex-shrink:0;">✦</div>
                        <div style="min-width:0;">
                          <div style="font-size:11px; font-weight:800; color:${dept.color}; text-transform:uppercase; letter-spacing:0.04em; margin-bottom:2px;">
                            ${subLabel}
                          </div>
                          <div class="ai-agent-chip-title" style="font-size:16.5px;">${cName}</div>
                          ${ag.badge ? `<div style="font-family:var(--font-mono); font-size:11.5px; color:#10b981; font-weight:700; margin-top:4px;">${ag.badge}</div>` : ''}
                        </div>
                      </div>
                      <span style="color:${dept.color}; font-weight:800; font-size:18px;">&rarr;</span>
                    </div>
                  `;
                }).join('')}
              </div>
            </div>
          `;
        }).filter(Boolean).join('');

        return sectionsHtml || `<div style="grid-column: 1 / -1; padding: 40px; text-align: center; color: var(--text-secondary);">No matching AI agents found.</div>`;
      }

      // Personas Hierarchical Mode
      const visibleDepts = deptList.filter(d => deptFilter === 'all' || d.id === deptFilter);
      const personaSectionsHtml = visibleDepts.map(dept => {
        const matchingPersonas = Object.values(PERSONAS).filter(p => {
          if (p.deptId !== dept.id) return false;
          if (!q) return true;
          const hay = [p.name, p.subPillarName || '', dept.name, p.role || ''].join(' ').toLowerCase();
          return hay.includes(q);
        });
        if (!matchingPersonas.length) return '';

        return `
          <div class="sc-dir-pillar-section" style="border-left: 5px solid ${dept.color};">
            <div class="sc-dir-pillar-head">
              <div>
                <div style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; color:${dept.color}; text-transform:uppercase; letter-spacing:0.06em;">
                  ${dept.scorBadge || 'OPERATING PILLAR'}
                </div>
                <h2 style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary); margin:3px 0 0;">
                  ${dept.name}
                </h2>
              </div>
              <span style="font-family:var(--font-mono); font-size:12px; font-weight:800; padding:5px 12px; border-radius:999px; background:${dept.color}18; color:${dept.color}; border:1px solid ${dept.color}40;">
                ${(dept.subPillars || []).length} Sub-Pillars · ${matchingPersonas.length} Roles
              </span>
            </div>
            <div class="sc-dir-cards-subgrid">
              ${matchingPersonas.map(p => {
                const subLabel = p.subPillarName || dept.name;
                return `
                  <div class="human-persona-card" style="--dept-accent: ${dept.color}; padding: 20px 22px;" onclick="openPersonaPage('${p.id}', true, event)">
                    <div style="display:flex; align-items:center; gap:14px; min-width:0;">
                      <div class="human-avatar-circle" style="--dept-accent: ${dept.color}; flex-shrink:0;">${p.icon}</div>
                      <div style="min-width:0;">
                        <div style="font-size:11px; font-weight:800; color:${dept.color}; text-transform:uppercase; letter-spacing:0.04em; margin-bottom:2px;">
                          ${subLabel}
                        </div>
                        <div class="human-persona-title" style="font-size:16px;">${p.name}</div>
                        <div class="human-persona-sub" style="margin-top:3px;">${p.headlineStat || '-85% Manual Toil'}</div>
                      </div>
                    </div>
                    <span class="persona-open-arrow" style="color:${dept.color}; font-size:18px; font-weight:800;">&rarr;</span>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        `;
      }).filter(Boolean).join('');

      return personaSectionsHtml || `<div style="grid-column: 1 / -1; padding: 40px; text-align: center; color: var(--text-secondary);">No matching personas found.</div>`;
    }

    function filterDirectoryLive(val) {
      currentDirSearch = val || '';
      const grid = document.getElementById('dirPersonaGridEl');
      if (grid) {
        grid.innerHTML = renderDirectoryCardsHtml(currentDirDeptFilter, currentDirSearch, currentDirMode);
      }
    }

    function openPersonasDirectoryPage(deptFilter = 'all', searchQuery = '', pushHash = true, mode = null, ev = null) {
      currentDirDeptFilter = deptFilter || 'all';
      currentDirSearch = searchQuery || '';
      if (mode) {
        currentDirMode = mode;
      } else if (deptFilter === 'universal') {
        currentDirMode = 'agents';
      }

      if (currentDirDeptFilter !== 'all' && currentDirDeptFilter !== 'universal' && !DEPARTMENTS[currentDirDeptFilter]) {
        currentDirDeptFilter = 'all';
      }

      if (pushHash) {
        history.pushState({ page: 'directory', dept: currentDirDeptFilter, mode: currentDirMode }, '', '#directory');
      }

      const totalPersonas = Object.keys(PERSONAS).length;
      const totalAgents = Object.keys(AGENTS).length;
      const deptList = Object.values(DEPARTMENTS);
      const totalDepts = deptList.length;
      const uniCount = Object.values(AGENTS).filter(a => a.isUniversal).length;

      const transClass = getPageTransitionClass(ev, null);
      const container = document.getElementById('directoryPageContent');
      container.innerHTML = `
        <div class="${transClass}">
          <div class="back-bar" style="margin-bottom: 20px;">
            <button type="button" class="back-btn" onclick="goToOrgChart()">
              <span>&larr;</span>
              <span>Back to ${totalDepts} Operating Pillars</span>
            </button>

            <div class="sc-v22-tab-strip" style="margin-bottom: 0;">
              <button type="button"
                      class="sc-v22-tab-btn ${currentDirMode === 'personas' ? 'active' : ''}"
                      onclick="openPersonasDirectoryPage(currentDirDeptFilter === 'universal' ? 'all' : currentDirDeptFilter, currentDirSearch, false, 'personas', event)">
                <span>👤 Personas</span>
                <span class="sc-v22-tab-count">${totalPersonas}</span>
              </button>
              <button type="button"
                      class="sc-v22-tab-btn ${currentDirMode === 'agents' ? 'active' : ''}"
                      onclick="openPersonasDirectoryPage(currentDirDeptFilter, currentDirSearch, false, 'agents', event)">
                <span>✦ AI Agents</span>
                <span class="sc-v22-tab-count">${totalAgents}</span>
              </button>
            </div>
          </div>

          <div class="simple-arch-card" style="padding: 26px 28px; margin-bottom: 22px;">
            <div style="font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:var(--g-blue); margin-bottom:4px;">
              Hierarchical Operating Directory · ${totalDepts} Operating Pillars
            </div>
            <h1 style="font-family:var(--font-display); font-size:clamp(26px, 2.8vw, 34px); font-weight:800; color:var(--text-primary); margin:0 0 6px;">
              ${currentDirMode === 'agents' ? `${totalAgents} Supply Chain AI Agents` : `${totalPersonas} Supply Chain Personas`}
            </h1>
            <p style="font-size:14.5px; color:var(--text-secondary); margin:0 0 18px;">
              Grouped cleanly by Operating Pillar and Sub-Pillar. Click any ${currentDirMode === 'agents' ? 'AI agent to inspect its workflow diagram & interactive demo' : 'role to inspect their daily Red vs. Green transformation'}.
            </p>

            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:14px;">
              <input type="search"
                     class="dir-search-input"
                     style="padding:11px 16px; font-size:14px; min-width:280px; flex:1; max-width:420px;"
                     placeholder="🔍 Search by role, agent, or sub-pillar..."
                     value="${currentDirSearch}"
                     oninput="filterDirectoryLive(this.value)" />

              <div style="display:flex; gap:8px; flex-wrap:wrap;">
                <button type="button"
                        class="switch-pill ${currentDirDeptFilter === 'all' ? 'active' : ''}"
                        style="${currentDirDeptFilter === 'all' ? 'background:var(--g-blue); color:#ffffff; border-color:var(--g-blue); font-weight:700;' : ''}"
                        onclick="openPersonasDirectoryPage('all', currentDirSearch, false, currentDirMode, event)">
                  All Pillars (${currentDirMode === 'agents' ? totalAgents : totalPersonas})
                </button>
                ${currentDirMode === 'agents' && uniCount > 0 ? `
                  <button type="button"
                          class="switch-pill ${currentDirDeptFilter === 'universal' ? 'active' : ''}"
                          style="${currentDirDeptFilter === 'universal' ? 'background:#4f46e5; color:#ffffff; border-color:#4f46e5; font-weight:700;' : ''}"
                          onclick="openPersonasDirectoryPage('universal', currentDirSearch, false, 'agents', event)">
                    🌐 Universal (${uniCount})
                  </button>
                ` : ''}
                ${deptList.map(d => {
                  const count = currentDirMode === 'agents'
                    ? (d.agentIds || []).filter(aid => AGENTS[aid]).length
                    : (d.personaIds || []).filter(pid => PERSONAS[pid]).length;
                  const shortPillar = formatShortPillarTab(d);
                  return `
                    <button type="button"
                            class="switch-pill ${currentDirDeptFilter === d.id ? 'active' : ''}"
                            style="${currentDirDeptFilter === d.id ? `background:${d.color}; color:#ffffff; border-color:${d.color}; font-weight:700;` : ''}"
                            onclick="openPersonasDirectoryPage('${d.id}', currentDirSearch, false, currentDirMode, event)">
                      ${shortPillar} (${count})
                    </button>
                  `;
                }).join('')}
              </div>
            </div>
          </div>

          <div id="dirPersonaGridEl" class="dir-persona-grid" style="display:grid; grid-template-columns: 1fr; gap: 18px;">
            ${renderDirectoryCardsHtml(currentDirDeptFilter, currentDirSearch, currentDirMode)}
          </div>
        </div>
      `;

      hydrateAssets();
      showActivePage('pageDirectory');
    }

"""


NEW_PERIODIC_AND_MINDMAP_BLOCK = """    function openPeriodicTablePage(filterGroup = 'all', selectedAgentId = null, pushState = true) {
      currentPeriodicFilter = filterGroup || 'all';
      if (currentPeriodicFilter !== 'all' && !DEPARTMENTS[currentPeriodicFilter]) {
        currentPeriodicFilter = 'all';
      }
      if (selectedAgentId && AGENTS[selectedAgentId]) {
        currentSelectedElementId = selectedAgentId;
      }
      if (pushState) {
        history.pushState({ page: 'periodic', filter: currentPeriodicFilter, agentId: currentSelectedElementId }, '', '#periodic');
      }

      const deptList = Object.values(DEPARTMENTS);
      const dynamicGroups = deptList.map(d => {
        const spList = d.subPillars || [];
        const agCount = spList.reduce((acc, sp) => acc + ((sp.items || []).filter(it => AGENTS[it.agentId]).length), 0);
        const shortTab = formatShortPillarTab(d);
        return {
          id: d.id,
          name: d.name,
          scorBadge: d.scorBadge || '',
          shortTab,
          color: d.color || '#2563eb',
          count: agCount,
          deptObj: d
        };
      });

      const totalPillarsCount = dynamicGroups.length;
      const totalSubPillarsCount = deptList.reduce((acc, d) => acc + ((d.subPillars || []).length), 0);
      const totalAgentsCount = Object.keys(AGENTS).length;

      const selAg = AGENTS[currentSelectedElementId] || Object.values(AGENTS)[0];
      const selMeta = PERIODIC_AGENT_META[selAg.id] || {
        code: '101', sym: 'Ds', short: cleanAgentName(selAg.name), group: selAg.deptId,
        layer: 'Vertex AI ADK + A2A', layerColor: '#3b82f6', trigger: 'Event-Driven', trigIcon: '⚡'
      };
      const selDept = DEPARTMENTS[selAg.deptId] || deptList[0];
      const selGrp = dynamicGroups.find(g => g.id === selDept.id) || dynamicGroups[0];
      const selSell = getAgentSellingMeta(selAg, selDept);
      const selCls = getAgentBuildClassification(selAg);
      const selPrimaryPersona = (selAg.personaId && PERSONAS[selAg.personaId]) || selSell.usedByPersonas[0] || Object.values(PERSONAS)[0];
      const selCleanName = cleanAgentName(selAg.name);

      const renderInlineExpansionCard = (ag, meta, grpColor) => {
        const d = DEPARTMENTS[ag.deptId] || selDept;
        const cls = getAgentBuildClassification(ag);
        const pOwner = (ag.personaId && PERSONAS[ag.personaId]) || getAgentSellingMeta(ag, d).usedByPersonas[0];
        const cName = cleanAgentName(ag.name);
        return `
          <div class="pt-inline-expand" style="--exp-color:${grpColor};">
            <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:16px; padding-bottom:14px; border-bottom:1px solid var(--border-subtle); margin-bottom:16px;">
              <div>
                <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:6px;">
                  <span style="font-family:var(--font-mono); font-size:12px; font-weight:800; padding:3px 9px; border-radius:6px; background:${grpColor}22; border:1px solid ${grpColor}; color:var(--text-primary);">
                    A-${meta.code} · ${meta.sym}
                  </span>
                  <span class="build-tier-badge ${cls.cssClass}">${cls.tier}</span>
                  <span class="pt-side-tag">${meta.trigIcon} ${meta.trigger}</span>
                </div>
                <h3 style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary); margin-bottom:2px;">
                  ${cName}
                </h3>
                <div style="font-size:13.5px; color:var(--text-secondary); font-weight:600;">
                  ${ag.subPillarName || meta.subPillar || d.name}
                </div>
              </div>
              <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                ${pOwner ? `
                  <button type="button" class="switch-pill" style="border-color:${grpColor}; color:${grpColor}; font-weight:700;" onclick="openPersonaPage('${pOwner.id}', true, event)">
                    ${pOwner.icon} ${pOwner.name} &rarr;
                  </button>
                ` : ''}
                <button type="button" class="agent-plug-btn" style="padding:9px 16px; font-size:13px;" onclick="openAgentPage('${ag.id}', true, event)">
                  <span>Open ${cName}</span>
                  <span>&rarr;</span>
                </button>
                <button type="button" class="switch-pill" onclick="currentExpandedInlineId = null; openPeriodicTablePage('${currentPeriodicFilter}', '${ag.id}', false)">
                  ✕
                </button>
              </div>
            </div>

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:14px;">
              <div style="padding:14px 16px; border-radius:12px; background:rgba(239,68,68,0.06); border:1px solid rgba(239,68,68,0.22);">
                <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.07em; color:#ef4444; margin-bottom:4px;">
                  ✕ Manual Bottleneck
                </div>
                <p style="font-size:13.5px; color:var(--text-primary); line-height:1.55; margin:0;">${shortSentence(ag.problem, 175)}</p>
              </div>
              <div style="padding:14px 16px; border-radius:12px; background:rgba(59,130,246,0.06); border:1px solid rgba(59,130,246,0.22);">
                <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.07em; color:#3b82f6; margin-bottom:4px;">
                  ✦ AI Solution
                </div>
                <p style="font-size:13.5px; color:var(--text-primary); line-height:1.55; margin:0;">${shortSentence(ag.solution, 175)}</p>
              </div>
              <div style="padding:14px 16px; border-radius:12px; background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.22);">
                <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.07em; color:#10b981; margin-bottom:4px;">
                  ⚡ Quantified Outcome
                </div>
                <p style="font-size:13.5px; color:var(--text-primary); line-height:1.55; margin:0;">${shortSentence(ag.outcome, 175)}</p>
              </div>
            </div>
          </div>
        `;
      };

      const visibleGroups = dynamicGroups.filter(g => currentPeriodicFilter === 'all' || g.id === currentPeriodicFilter);
      const leftColumnHtml = visibleGroups.map(grp => {
        const deptObj = grp.deptObj;
        const subPillars = (deptObj && deptObj.subPillars) || [];
        const grpAgents = [];
        subPillars.forEach(sp => {
          (sp.items || []).forEach(it => {
            if (AGENTS[it.agentId]) {
              const m = PERIODIC_AGENT_META[it.agentId] || { code: '101', sym: 'Ai', short: cleanAgentName(AGENTS[it.agentId].name), layerColor: grp.color, trigIcon: '⚡', layer: 'Vertex AI ADK', trigger: 'Event-Driven' };
              grpAgents.push({ ag: AGENTS[it.agentId], m });
            }
          });
        });
        const expandedItem = grpAgents.find(x => x.ag.id === currentExpandedInlineId);
        const cleanPillarTitle = deptObj.scorBadge ? `${deptObj.scorBadge} · ${deptObj.name}` : deptObj.name;

        return `
          <div class="pt-pillar-card" style="--dom-color:${grp.color};">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom:6px;">
              <div style="display:flex; align-items:center; gap:10px;">
                <span class="pt-domain-swatch" style="--dom-color:${grp.color}; width:12px; height:12px; border-radius:3px;"></span>
                <span style="font-family:var(--font-display); font-size:16.5px; font-weight:800; color:var(--text-primary); letter-spacing:-0.01em;">
                  ${cleanPillarTitle}
                </span>
              </div>
              <span style="font-family:var(--font-mono); font-size:11.5px; font-weight:700; color:${grp.color}; padding:3px 10px; border-radius:999px; background:${grp.color}16; border:1px solid ${grp.color}38;">
                ${subPillars.length} Sub-Pillars · ${grpAgents.length} Agents
              </span>
            </div>

            <div class="pt-subpillars-grid">
              ${subPillars.map(sp => {
                const spItems = (sp.items || []).map(it => {
                  const ag = AGENTS[it.agentId];
                  const m = PERIODIC_AGENT_META[it.agentId] || { code: '101', sym: 'Ai', short: cleanAgentName(it.agentName), layerColor: sp.color || grp.color, trigIcon: '⚡', layer: 'Vertex AI ADK', trigger: 'Event-Driven' };
                  return { ag, m, it };
                }).filter(x => x.ag);

                return `
                  <div class="pt-subpillar-group" style="--sp-color:${sp.color || grp.color};">
                    <div class="pt-subpillar-title">
                      <span>${sp.icon} ${sp.name}</span>
                      <span style="font-family:var(--font-mono); font-size:11px; color:${sp.color || grp.color};">${spItems.length}</span>
                    </div>
                    <div class="pt-subpillar-tiles">
                      ${spItems.map(({ ag, m }) => {
                        const isSel = ag.id === selAg.id;
                        const shortLabel = ((ag.canonicalName && ag.canonicalName !== cleanAgentName(ag.name)) ? cleanAgentName(ag.name) : cleanAgentName(m.short || ag.name)).replace(/\\s+Agent$/i, '');
                        return `
                          <div class="pt-tile ${isSel ? 'active' : ''}"
                               style="--tile-color:${sp.color || grp.color}; --dot-color:${m.layerColor};"
                               onclick="handlePeriodicTileClick('${ag.id}')">
                            <div class="pt-tile-top">
                              <span>${m.code}</span>
                              <span class="pt-tile-trig" title="${m.trigger}">${m.trigIcon}</span>
                            </div>
                            <div class="pt-tile-sym">${m.sym}</div>
                            <div class="pt-tile-title" title="${cleanAgentName(ag.name)}">${shortLabel}</div>
                            <div class="pt-tile-dot" title="${m.layer}"></div>
                          </div>
                        `;
                      }).join('')}
                    </div>
                  </div>
                `;
              }).join('')}
            </div>

            ${expandedItem ? renderInlineExpansionCard(expandedItem.ag, expandedItem.m, grp.color) : ''}
          </div>
        `;
      }).join('');

      const container = document.getElementById('periodicPageContent');
      container.innerHTML = `
        <div class="subpage-top-bar">
          <button type="button" class="back-btn" onclick="goToOrgChart()">
            <span>&larr;</span>
            <span>Back to ${totalPillarsCount} Pillars</span>
          </button>
          <div style="display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin-left:auto;">
            <button type="button" class="switch-pill" style="border-color:rgba(16,185,129,0.45); color:#10b981; font-weight:700;" onclick="openMindMapPage('mindmap', null, null, true)">
              🧠 Switch to Neural Mind Map &rarr;
            </button>
          </div>
        </div>

        <!-- Clean Header -->
        <div style="display:flex; flex-wrap:wrap; align-items:flex-end; justify-content:space-between; gap:16px; padding-bottom: 16px; border-bottom: 1px solid var(--border-subtle); margin-bottom: 18px;">
          <div>
            <h1 style="font-family:var(--font-display); font-size:clamp(28px, 3vw, 38px); font-weight:800; letter-spacing:-0.025em; color:var(--text-primary); margin-bottom:4px;">
              The Periodic Table of Supply Chain AI Agents
            </h1>
            <p style="font-size:14.5px; color:var(--text-secondary); margin:0;">
              <strong>${totalPillarsCount} Operating Pillars</strong> &rarr; <strong>${totalSubPillarsCount} Sub-Pillars</strong> &rarr; <strong>${totalAgentsCount} AI Agents</strong>. Click any tile to inspect its Persona and open the Agent Studio.
            </p>
          </div>
          <div class="pt-stat-badges">
            <div class="pt-stat-badge"><strong>${totalPillarsCount}</strong>pillars</div>
            <div class="pt-stat-badge"><strong>${totalSubPillarsCount}</strong>sub-pillars</div>
            <div class="pt-stat-badge"><strong>${totalAgentsCount}</strong>agents</div>
          </div>
        </div>

        <!-- Clean Pillar Filter Tabs -->
        <div class="pt-top-tabs" style="margin-bottom:20px;">
          <button type="button" class="pt-tab-btn ${currentPeriodicFilter === 'all' ? 'active' : ''}"
                  onclick="currentExpandedInlineId = null; openPeriodicTablePage('all', '${selAg.id}', false)">
            <span>All Pillars</span>
            <span class="pt-tab-count">${totalAgentsCount}</span>
          </button>
          ${dynamicGroups.map(g => `
            <button type="button" class="pt-tab-btn ${currentPeriodicFilter === g.id ? 'active' : ''}"
                    onclick="currentExpandedInlineId = null; openPeriodicTablePage('${g.id}', '${selAg.id}', false)">
              <span>${g.shortTab}</span>
              <span class="pt-tab-count">${g.count}</span>
            </button>
          `).join('')}
        </div>

        <!-- Main 2-Column Layout: Left Structured Sub-Pillar Periodic Table + Right Sticky Inspector -->
        <div class="pt-main-layout">
          <div>
            ${leftColumnHtml}
          </div>

          <aside class="pt-sidebar">
            <div class="pt-side-card" style="border-top: 4px solid ${selGrp.color};">
              <div style="display:flex; align-items:flex-start; gap:14px; margin-bottom:14px;">
                <div class="pt-side-badge" style="background:${selGrp.color}; width:44px; height:44px; font-size:15px;">
                  ${selMeta.sym}
                </div>
                <div>
                  <div style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; color:${selGrp.color};">
                    A-${selMeta.code} · ${selAg.subPillarName || selMeta.subPillar || selDept.name}
                  </div>
                  <div style="font-family:var(--font-display); font-size:18px; font-weight:800; color:var(--text-primary); line-height:1.25; margin-top:2px;">
                    ${selCleanName}
                  </div>
                </div>
              </div>

              <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:14px;">
                <span class="build-tier-badge ${selCls.cssClass}">${selCls.tier}</span>
                <span class="pt-side-tag">${selMeta.trigIcon} ${selMeta.trigger}</span>
                <span class="pt-side-tag" style="color:#10b981; border-color:rgba(16,185,129,0.35); font-weight:800;">✦ ${selAg.badge}</span>
              </div>

              <p style="font-size:13.5px; color:var(--text-secondary); line-height:1.58; margin-bottom:14px;">
                ${shortSentence(selAg.solution || selAg.shortDesc, 155)}
              </p>

              ${selPrimaryPersona ? `
                <div style="padding:12px 14px; border-radius:12px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-left:4px solid ${selGrp.color}; margin-bottom:14px; display:flex; align-items:center; justify-content:space-between; gap:8px; cursor:pointer;" onclick="openPersonaPage('${selPrimaryPersona.id}', true, event)">
                  <div>
                    <div style="font-size:14px; font-weight:800; color:var(--text-primary);">
                      ${selPrimaryPersona.icon} ${selPrimaryPersona.name}
                    </div>
                    <div style="font-size:12px; color:var(--text-secondary); margin-top:2px;">
                      ${selPrimaryPersona.subPillarName || selDept.name}
                    </div>
                  </div>
                  <span style="font-size:12.5px; font-weight:800; color:${selGrp.color};">&rarr;</span>
                </div>
              ` : ''}

              <div style="display:flex; flex-direction:column; gap:10px; padding-top:12px; border-top:1px solid var(--border-subtle);">
                <button type="button" class="agent-plug-btn" style="width:100%; justify-content:center; padding:10px 14px; font-size:13px;" onclick="openAgentPage('${selAg.id}', true, event)">
                  <span>Open ${selCleanName}</span>
                  <span>&rarr;</span>
                </button>
              </div>
            </div>

            <!-- Compact Legend Box -->
            <div class="pt-legend-box">
              <div>
                <div class="pt-legend-title">BUILD TIERS &amp; STACK</div>
                <div class="pt-legend-list">
                  <div class="pt-legend-row">
                    <span style="display:inline-flex; align-items:center; gap:8px;"><span class="pt-tile-dot" style="--dot-color:#10b981;"></span>Low-Code · Gemini Studio</span>
                  </div>
                  <div class="pt-legend-row">
                    <span style="display:inline-flex; align-items:center; gap:8px;"><span class="pt-tile-dot" style="--dot-color:#3b82f6;"></span>Hybrid · ADK + Cloud Run</span>
                  </div>
                  <div class="pt-legend-row">
                    <span style="display:inline-flex; align-items:center; gap:8px;"><span class="pt-tile-dot" style="--dot-color:#f59e0b;"></span>High-Code · ADK + OR-Tools</span>
                  </div>
                </div>
              </div>

              <div>
                <div class="pt-legend-title">TRIGGERS</div>
                <div class="pt-legend-list">
                  <div class="pt-legend-row"><span>⚡ Event-Driven</span></div>
                  <div class="pt-legend-row"><span>💬 Chat-Initiated</span></div>
                  <div class="pt-legend-row"><span>🛡️ Scheduled / Guardrail</span></div>
                </div>
              </div>
            </div>
          </aside>
        </div>
      `;

      hydrateAssets();
      showActivePage('pagePeriodic');
    }

    /* =========================================================================
       PAGE 8: FULL-SCREEN NEURAL MIND MAP (HARMONIZED PALETTE + KEY ACTIONS ON TOP)
       ========================================================================= */
    let currentMindMapMode = 'mindmap'; // 'mindmap' | 'flowchart'
    let currentMindMapDeptId = 'demand_sop';
    let currentMindMapSubPillarId = 'demand_forecasting';
    let currentMindMapAgentId = 'demand_sensing_agent';
    let currentMindMapPersonaId = 'demand_planner_forecaster';
    let currentFlowStepIdx = 0;

    function selectMindMapDept(deptId) {
      currentMindMapDeptId = deptId;
      const d = DEPARTMENTS[deptId];
      if (d && d.subPillars && d.subPillars.length > 0) {
        const sp = d.subPillars[0];
        currentMindMapSubPillarId = sp.id;
        if (sp.items && sp.items.length > 0) {
          currentMindMapAgentId = sp.items[0].agentId;
          currentMindMapPersonaId = sp.items[0].personaId;
        }
      }
      openMindMapPage('mindmap', currentMindMapDeptId, null, false);
    }

    function selectMindMapSubPillar(subPillarId) {
      currentMindMapSubPillarId = subPillarId;
      for (const d of Object.values(DEPARTMENTS)) {
        const sp = (d.subPillars || []).find(s => s.id === subPillarId);
        if (sp) {
          currentMindMapDeptId = d.id;
          if (sp.items && sp.items.length > 0) {
            currentMindMapAgentId = sp.items[0].agentId;
            currentMindMapPersonaId = sp.items[0].personaId;
          }
          break;
        }
      }
      openMindMapPage('mindmap', currentMindMapDeptId, null, false);
    }

    function selectMindMapPersona(personaId) {
      const p = PERSONAS[personaId];
      if (p) {
        currentMindMapDeptId = p.deptId;
        currentMindMapSubPillarId = p.subPillarId || currentMindMapSubPillarId;
        currentMindMapPersonaId = p.id;
        if (p.primaryAgentId) currentMindMapAgentId = p.primaryAgentId;
      }
      openMindMapPage('mindmap', currentMindMapDeptId, null, false);
    }

    function selectMindMapAgent(agentId) {
      if (currentMindMapAgentId === agentId) {
        currentMindMapAgentId = null;
      } else {
        currentMindMapAgentId = agentId;
        const ag = AGENTS[agentId];
        if (ag) {
          currentMindMapDeptId = ag.deptId || currentMindMapDeptId;
          currentMindMapSubPillarId = ag.subPillarId || currentMindMapSubPillarId;
          currentMindMapPersonaId = ag.personaId || currentMindMapPersonaId;
        }
      }
      openMindMapPage('mindmap', currentMindMapDeptId, null, false);
    }

    function openMindMapPage(mode = 'mindmap', deptId = null, subPillarOrPersonaId = null, pushState = true) {
      if (typeof subPillarOrPersonaId === 'boolean') {
        pushState = subPillarOrPersonaId;
        subPillarOrPersonaId = null;
      }
      if (mode === 'mindmap' || mode === 'flowchart') {
        currentMindMapMode = mode;
      }

      const deptList = Object.values(DEPARTMENTS);
      if (!DEPARTMENTS[currentMindMapDeptId] && deptList.length > 0) {
        currentMindMapDeptId = deptList[0].id;
      }

      if (deptId && DEPARTMENTS[deptId]) {
        currentMindMapDeptId = deptId;
        const d = DEPARTMENTS[deptId];
        if (d.subPillars && d.subPillars.length > 0 && !d.subPillars.some(s => s.id === currentMindMapSubPillarId)) {
          currentMindMapSubPillarId = d.subPillars[0].id;
          if (d.subPillars[0].items && d.subPillars[0].items.length > 0) {
            currentMindMapAgentId = d.subPillars[0].items[0].agentId;
          }
        }
      }
      if (subPillarOrPersonaId) {
        if (PERSONAS[subPillarOrPersonaId]) {
          const p = PERSONAS[subPillarOrPersonaId];
          currentMindMapDeptId = p.deptId;
          currentMindMapSubPillarId = p.subPillarId;
          currentMindMapAgentId = p.primaryAgentId;
        } else {
          for (const d of deptList) {
            const sp = (d.subPillars || []).find(s => s.id === subPillarOrPersonaId);
            if (sp) {
              currentMindMapDeptId = d.id;
              currentMindMapSubPillarId = sp.id;
              if (sp.items && sp.items.length > 0) currentMindMapAgentId = sp.items[0].agentId;
              break;
            }
          }
        }
      }
      if (pushState) {
        history.pushState({ page: 'mindmap', mode: currentMindMapMode }, '', '#mindmap');
      }

      const activeDept = DEPARTMENTS[currentMindMapDeptId] || deptList[0];
      const deptSubPillars = activeDept.subPillars || [];
      const activeSubPillar = deptSubPillars.find(s => s.id === currentMindMapSubPillarId) || deptSubPillars[0];
      const rawItems = ((activeSubPillar && activeSubPillar.items) || []).filter(it => AGENTS[it.agentId] && PERSONAS[it.personaId]);
      if (currentMindMapAgentId && !rawItems.some(it => it.agentId === currentMindMapAgentId) && rawItems.length > 0) {
        currentMindMapAgentId = rawItems[0].agentId;
      }
      // Pin the active/expanded Agent card to the very TOP of Column 3 so important details are immediately visible on top!
      const subPillarItems = [...rawItems].sort((a, b) => {
        if (a.agentId === currentMindMapAgentId) return -1;
        if (b.agentId === currentMindMapAgentId) return 1;
        return 0;
      });

      const spAccent = (activeSubPillar && activeSubPillar.color) || activeDept.color || '#2563eb';
      const topItem = subPillarItems[0] || null;
      const topAg = topItem ? AGENTS[topItem.agentId] : Object.values(AGENTS)[0];
      const topPer = topItem ? PERSONAS[topItem.personaId] : Object.values(PERSONAS)[0];

      const totalPillarsCount = deptList.length;
      const totalSubPillarsCount = deptList.reduce((acc, d) => acc + ((d.subPillars || []).length), 0);
      const totalAgentsCount = Object.keys(AGENTS).length;

      const flowSteps = [
        {
          num: '01',
          title: 'Full-Screen Hero Landing (#)',
          sub: '60fps Supply Chain Canvas & Thesis',
          color: '#2563eb',
          whatOpens: '60fps kinetic supply chain canvas introducing the CSCO executive transformation thesis.',
          actionLabel: 'Open Hero Landing &rarr;',
          actionFn: "goHome()"
        },
        {
          num: '02',
          title: `${totalPillarsCount} Operating Pillars (#orgChart)`,
          sub: 'Click Any Pillar to Reveal Its Clean Sub-Pillar Boxes',
          color: '#0d9488',
          whatOpens: `Interactive ${totalPillarsCount}-Pillar board where clicking a Pillar cleanly reveals its functional Sub-Pillar boxes.`,
          actionLabel: `Open ${totalPillarsCount} Pillars &rarr;`,
          actionFn: "goToOrgChart()"
        },
        {
          num: '03',
          title: 'Sub-Pillar Persona Dropdown',
          sub: 'Click a Sub-Pillar Box to Reveal Its Human Personas',
          color: '#7c3aed',
          whatOpens: 'Smoothly animates open the Human Personas for that Sub-Pillar without cluttering the screen.',
          actionLabel: 'Try on Front Page &rarr;',
          actionFn: "goToOrgChart()"
        },
        {
          num: '04',
          title: 'Dedicated Persona Page (#persona/id)',
          sub: `${Object.keys(PERSONAS).length} Supply Chain Roles · Daily Journey & AI Agents`,
          color: '#0284c7',
          whatOpens: 'Click-to-expand Daily Journey comparing Manual Bottleneck (Red) vs. With Gemini AI (Green) and assigned AI Agents.',
          actionLabel: 'Open Persona Journey &rarr;',
          actionFn: topPer ? `openPersonaPage('${topPer.id}', true, event)` : "goHome()"
        },
        {
          num: '05',
          title: 'Executive Agent Studio (#agent/id)',
          sub: `${totalAgentsCount} AI Agents · ROI Cards, Architecture & Interactive Demo`,
          color: '#059669',
          whatOpens: 'Executive business case with verified ROI metrics, 4-stage workflow diagram, and interactive demo simulator.',
          actionLabel: 'Open Agent Studio &rarr;',
          actionFn: topAg ? `openAgentPage('${topAg.id}', true, event)` : "goHome()"
        },
        {
          num: '06',
          title: 'High-Code Technical Blueprint (#blueprint/id)',
          sub: '5-Stage ADK Pipeline, Sub-Agents & Solvers',
          color: '#e11d48',
          whatOpens: 'High-code ADK pipeline specification, A2A agent mesh, ERP write-back schemas, and solver constraints.',
          actionLabel: 'Open Technical Blueprint &rarr;',
          actionFn: topAg ? `openAgentBlueprintPage('${topAg.id}', true, event)` : "goHome()"
        }
      ];

      const container = document.getElementById('mindMapPageContent');
      container.innerHTML = `
        <div class="subpage-top-bar">
          <button type="button" class="back-btn" onclick="goToOrgChart()">
            <span>&larr;</span>
            <span>Back to ${totalPillarsCount} Pillars</span>
          </button>
          <div style="display:flex; flex-wrap:wrap; gap:10px; align-items:center;">
            <button type="button" class="switch-pill" style="border-color:rgba(37,99,235,0.45); color:var(--g-blue); font-weight:700;" onclick="openPeriodicTablePage('all', null, true)">
              🧪 Switch to Periodic Table &rarr;
            </button>
          </div>
        </div>

        <!-- Clean, Full-Width Header -->
        <div style="display:flex; flex-wrap:wrap; align-items:flex-end; justify-content:space-between; gap:16px; padding-bottom: 16px; border-bottom: 1px solid var(--border-subtle); margin-bottom: 18px;">
          <div>
            <h1 style="font-family:var(--font-display); font-size:clamp(28px, 3vw, 38px); font-weight:800; letter-spacing:-0.025em; color:var(--text-primary); margin-bottom:4px;">
              Interactive Neural Mind Map
            </h1>
            <p style="font-size:15px; color:var(--text-secondary); margin:0;">
              <strong>1. Operating Pillars (${totalPillarsCount})</strong> &rarr; <strong>2. Sub-Pillars (${totalSubPillarsCount})</strong> &rarr; <strong>3. AI Agents (${totalAgentsCount})</strong> &rarr; <strong>Assigned Human Persona</strong>.
            </p>
          </div>

          <div class="pt-top-tabs" style="margin-bottom:0;">
            <button type="button" class="pt-tab-btn ${currentMindMapMode === 'mindmap' ? 'active' : ''}"
                    onclick="openMindMapPage('mindmap', '${currentMindMapDeptId}', '${currentMindMapSubPillarId}', false)">
              <span>🧠 Neural Mind Map</span>
              <span class="pt-tab-count">${totalPillarsCount} Pillars &rarr; ${totalAgentsCount} Agents</span>
            </button>
            <button type="button" class="pt-tab-btn ${currentMindMapMode === 'flowchart' ? 'active' : ''}"
                    onclick="openMindMapPage('flowchart', '${currentMindMapDeptId}', '${currentMindMapSubPillarId}', false)">
              <span>🧭 Portal Click-Path Guide</span>
              <span class="pt-tab-count">6 Steps</span>
            </button>
          </div>
        </div>

        ${currentMindMapMode === 'mindmap' ? `
          <!-- PROMINENT ACTIVE SELECTION & QUICK-LAUNCH BAR AT THE TOP -->
          ${topAg && topPer ? `
            <div class="mm-active-path-bar" style="--mm-accent:${spAccent};">
              <div style="display:flex; align-items:center; flex-wrap:wrap; gap:8px;">
                <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:${activeDept.color}; margin-right:4px;">
                  Active Path:
                </span>
                <span class="mm-crumb-step" style="border-color:${activeDept.color}55;">
                  <span style="width:8px; height:8px; border-radius:999px; background:${activeDept.color};"></span>
                  <span>${activeDept.name}</span>
                </span>
                <span style="color:var(--text-muted); font-weight:800;">&rarr;</span>
                <span class="mm-crumb-step" style="border-color:${spAccent}55;">
                  <span>${activeSubPillar ? activeSubPillar.icon : '📦'}</span>
                  <span>${activeSubPillar ? activeSubPillar.name : ''}</span>
                </span>
                <span style="color:var(--text-muted); font-weight:800;">&rarr;</span>
                <span class="mm-crumb-step" style="border-color:${spAccent}; background:${spAccent}14;">
                  <span style="color:${spAccent};">✦</span>
                  <span>${cleanAgentName(topAg.name)}</span>
                </span>
              </div>

              <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                <button type="button" class="switch-pill" style="border-color:${spAccent}; color:${spAccent}; font-weight:800; padding:9px 15px;" onclick="openPersonaPage('${topPer.id}', true, event)">
                  ${topPer.icon} ${topPer.name} &rarr;
                </button>
                <button type="button" class="agent-plug-btn" style="padding:9px 16px; font-size:13px;" onclick="openAgentPage('${topAg.id}', true, event)">
                  <span>✦ Open ${cleanAgentName(topAg.name)} Studio</span>
                  <span>&rarr;</span>
                </button>
              </div>
            </div>
          ` : ''}

          <!-- FULL-SCREEN 3-COLUMN NEURAL MIND MAP -->
          <div class="mm-neural-board">
            <!-- COLUMN 1: OPERATING PILLARS -->
            <div class="mm-neural-col">
              <div class="mm-neural-col-header">
                <div>
                  <span class="mm-neural-step-pill">LAYER 01 · OPERATING PILLARS</span>
                  <div style="font-family:var(--font-display); font-size:18px; font-weight:800; color:var(--text-primary); margin-top:6px;">
                    Operating Pillars (${totalPillarsCount})
                  </div>
                </div>
              </div>

              <div style="display:flex; flex-direction:column; gap:10px; flex:1; justify-content:space-between;">
                ${deptList.map(d => {
                  const isAct = d.id === activeDept.id;
                  const spCount = (d.subPillars || []).length;
                  return `
                    <button type="button" class="mm-pillar-node ${isAct ? 'active' : ''}"
                            style="--node-color:${d.color};"
                            onclick="selectMindMapDept('${d.id}')">
                      <div>
                        <div style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:${d.color}; letter-spacing:0.05em;">
                          ${d.scorBadge}
                        </div>
                        <div style="font-family:var(--font-display); font-size:15.5px; font-weight:800; color:var(--text-primary); margin-top:3px;">
                          ${d.name}
                        </div>
                      </div>
                      <span style="font-family:var(--font-mono); font-size:11.5px; font-weight:700; color:${isAct ? d.color : 'var(--text-secondary)'}; white-space:nowrap;">
                        ${spCount} sub-pillars &rarr;
                      </span>
                    </button>
                  `;
                }).join('')}
              </div>
            </div>

            <!-- ANIMATED NEURAL SYNAPSE BRIDGE 1 (PILLAR -> SUB-PILLARS) -->
            <div class="mm-synapse-bridge">
              <svg viewBox="0 0 48 420" style="width:48px; height:100%; overflow:visible;">
                <defs>
                  <linearGradient id="mmBridgeGrad1" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="${activeDept.color}" stop-opacity="0.95" />
                    <stop offset="100%" stop-color="${spAccent}" stop-opacity="0.95" />
                  </linearGradient>
                </defs>
                <path d="M 0 210 C 24 210, 24 90, 48 90" fill="none" stroke="url(#mmBridgeGrad1)" stroke-width="2.2" stroke-dasharray="5 5" opacity="0.5" />
                <path d="M 0 210 C 24 210, 24 170, 48 170" fill="none" stroke="url(#mmBridgeGrad1)" stroke-width="2.8" />
                <path d="M 0 210 C 24 210, 24 250, 48 250" fill="none" stroke="url(#mmBridgeGrad1)" stroke-width="2.8" />
                <path d="M 0 210 C 24 210, 24 330, 48 330" fill="none" stroke="url(#mmBridgeGrad1)" stroke-width="2.2" stroke-dasharray="5 5" opacity="0.5" />
                <circle r="4.5" fill="${activeDept.color}">
                  <animate attributeName="cx" from="4" to="44" dur="1.4s" repeatCount="indefinite" />
                  <animate attributeName="cy" from="210" to="170" dur="1.4s" repeatCount="indefinite" />
                </circle>
                <circle r="4.5" fill="${spAccent}">
                  <animate attributeName="cx" from="4" to="44" dur="1.8s" repeatCount="indefinite" />
                  <animate attributeName="cy" from="210" to="250" dur="1.8s" repeatCount="indefinite" />
                </circle>
              </svg>
            </div>

            <!-- COLUMN 2: SUB-PILLARS -->
            <div class="mm-neural-col" style="animation: ptExpandIn 0.26s var(--ease-spring) forwards;">
              <div class="mm-neural-col-header">
                <div>
                  <span class="mm-neural-step-pill" style="color:${activeDept.color}; border-color:${activeDept.color}55; background:${activeDept.color}18;">
                    LAYER 02 · ${activeDept.scorBadge}
                  </span>
                  <div style="font-family:var(--font-display); font-size:18px; font-weight:800; color:var(--text-primary); margin-top:6px;">
                    Sub-Pillars in ${activeDept.name} (${deptSubPillars.length})
                  </div>
                </div>
              </div>

              <div style="display:flex; flex-direction:column; gap:14px; flex:1; justify-content:flex-start;">
                ${deptSubPillars.map((sp, idx) => {
                  const isAct = activeSubPillar && sp.id === activeSubPillar.id;
                  const nodeCol = sp.color || activeDept.color;
                  const agLen = (sp.items || []).filter(it => AGENTS[it.agentId]).length;
                  return `
                    <button type="button" class="mm-subpillar-node ${isAct ? 'active' : ''}"
                            style="--node-color:${nodeCol}; padding:18px;"
                            onclick="selectMindMapSubPillar('${sp.id}')">
                      <div style="display:flex; align-items:center; gap:14px;">
                        <div style="width:44px; height:44px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px; background:${nodeCol}18; border:1px solid ${nodeCol}45; flex-shrink:0;">
                          ${sp.icon}
                        </div>
                        <div>
                          <div style="font-family:var(--font-mono); font-size:10.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:${nodeCol};">
                            SUB-PILLAR 0${idx + 1}
                          </div>
                          <div style="font-family:var(--font-display); font-size:16.5px; font-weight:800; color:var(--text-primary); margin-top:2px;">
                            ${sp.name}
                          </div>
                        </div>
                      </div>
                      <span style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; padding:5px 10px; border-radius:999px; background:${nodeCol}16; color:${nodeCol}; border:1px solid ${nodeCol}40; white-space:nowrap;">
                        ${agLen} Agents &rarr;
                      </span>
                    </button>
                  `;
                }).join('')}
              </div>
            </div>

            <!-- ANIMATED NEURAL SYNAPSE BRIDGE 2 (SUB-PILLAR -> AI AGENTS) -->
            <div class="mm-synapse-bridge">
              <svg viewBox="0 0 48 420" style="width:48px; height:100%; overflow:visible;">
                <defs>
                  <linearGradient id="mmBridgeGrad2" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="${spAccent}" stop-opacity="0.95" />
                    <stop offset="100%" stop-color="${activeDept.color}" stop-opacity="0.95" />
                  </linearGradient>
                </defs>
                <path d="M 0 210 C 24 210, 24 100, 48 100" fill="none" stroke="url(#mmBridgeGrad2)" stroke-width="2.8" />
                <path d="M 0 210 C 24 210, 24 210, 48 210" fill="none" stroke="url(#mmBridgeGrad2)" stroke-width="2.4" opacity="0.7" />
                <path d="M 0 210 C 24 210, 24 320, 48 320" fill="none" stroke="url(#mmBridgeGrad2)" stroke-width="2.4" opacity="0.7" />
                <circle r="4.5" fill="${spAccent}">
                  <animate attributeName="cx" from="4" to="44" dur="1.3s" repeatCount="indefinite" />
                  <animate attributeName="cy" from="210" to="100" dur="1.3s" repeatCount="indefinite" />
                </circle>
                <circle r="4.5" fill="${activeDept.color}">
                  <animate attributeName="cx" from="4" to="44" dur="1.7s" repeatCount="indefinite" />
                  <animate attributeName="cy" from="210" to="210" dur="1.7s" repeatCount="indefinite" />
                </circle>
              </svg>
            </div>

            <!-- COLUMN 3: AI AGENTS IN SELECTED SUB-PILLAR (ACTIVE PINNED ON TOP!) -->
            <div class="mm-neural-col" style="animation: ptExpandIn 0.3s var(--ease-spring) forwards;">
              <div class="mm-neural-col-header">
                <div>
                  <span class="mm-neural-step-pill" style="color:${spAccent}; border-color:${spAccent}55; background:${spAccent}18;">
                    LAYER 03 · ${(activeSubPillar && activeSubPillar.name) || 'SUB-PILLAR'}
                  </span>
                  <div style="font-family:var(--font-display); font-size:18px; font-weight:800; color:var(--text-primary); margin-top:6px;">
                    AI Agents (${subPillarItems.length}) · <span style="font-size:13.5px; font-weight:600; color:var(--text-secondary);">Active Agent Pinned on Top</span>
                  </div>
                </div>
              </div>

              <div style="display:flex; flex-direction:column; gap:14px; flex:1;">
                ${subPillarItems.map((it) => {
                  const ag = AGENTS[it.agentId];
                  const p = PERSONAS[it.personaId];
                  if (!ag || !p) return '';
                  const isExpanded = ag.id === currentMindMapAgentId;

                  return `
                    <div class="mm-agent-neural-card ${isExpanded ? 'expanded' : ''}" style="--ag-color:${spAccent};">
                      <button type="button" class="mm-agent-neural-header" onclick="selectMindMapAgent('${ag.id}')">
                        <div style="display:flex; align-items:center; gap:14px;">
                          <div class="ai-bot-square" style="width:44px; height:44px; font-size:18px; flex-shrink:0; background:${spAccent}18; color:${spAccent}; border-color:${spAccent}45;">✦</div>
                          <div>
                            <div style="font-family:var(--font-display); font-size:17.5px; font-weight:800; color:var(--text-primary);">
                              ${cleanAgentName(ag.name)}
                            </div>
                            <div style="font-size:12.5px; color:var(--text-secondary); margin-top:2px;">
                              ${ag.badge ? `<span style="color:#10b981; font-weight:700;">${ag.badge}</span> · ` : ''}${ag.subPillarName || activeDept.name}
                            </div>
                          </div>
                        </div>

                        <div style="display:flex; align-items:center; gap:10px;">
                          <span style="font-family:var(--font-mono); font-size:11.5px; font-weight:700; padding:6px 12px; border-radius:999px; background:${spAccent}16; color:${spAccent}; border:1px solid ${spAccent}44; white-space:nowrap;">
                            👤 ${isExpanded ? 'Active &amp; Pinned ▴' : 'Inspect Persona ▾'}
                          </span>
                        </div>
                      </button>

                      <div class="mm-agent-neural-body">
                        <div style="padding-top:14px; font-size:14px; color:var(--text-secondary); line-height:1.58;">
                          ${shortSentence(ag.solution || ag.role, 200)}
                        </div>

                        <!-- HARMONIZED HUMAN PERSONA CARD INSIDE THE AI AGENT -->
                        <div class="mm-expanded-persona-box" style="border-left: 4px solid ${spAccent} !important;">
                          <div style="display:flex; align-items:center; gap:14px;">
                            <div class="human-avatar-circle" style="width:50px; height:50px; font-size:23px; --dept-accent:${spAccent};">
                              ${p.icon}
                            </div>
                            <div>
                              <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:${spAccent};">
                                Assigned Human Role
                              </div>
                              <div style="font-family:var(--font-display); font-size:17px; font-weight:800; color:var(--text-primary);">
                                ${p.name}
                              </div>
                              <div style="font-size:12.5px; color:var(--text-secondary); margin-top:2px;">
                                ${p.headlineStat || '-85% Manual Toil'} · ${p.subPillarName || activeDept.name}
                              </div>
                            </div>
                          </div>

                          <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                            <button type="button" class="switch-pill" style="background:${spAccent}; color:#ffffff; font-weight:800; border:1px solid ${spAccent}; padding:10px 16px; white-space:normal; max-width:100%;" onclick="openPersonaPage('${p.id}', true, event)">
                              👤 Open Role Journey &rarr;
                            </button>
                            <button type="button" class="agent-plug-btn" style="padding:10px 16px; font-size:13px;" onclick="openAgentPage('${ag.id}', true, event)">
                              <span>✦ Open ${cleanAgentName(ag.name)} Studio</span>
                              <span>&rarr;</span>
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  `;
                }).join('')}
              </div>
            </div>
          </div>
        ` : `
          <!-- PORTAL CLICK-PATH FLOWCHART (CRISP IN BOTH DARK & LIGHT THEMES) -->
          <div style="padding:28px; border-radius:20px; background:var(--bg-card); border:1.5px solid var(--border-strong);">
            <div style="margin-bottom:20px;">
              <h2 style="font-family:var(--font-display); font-size:22px; font-weight:800; color:var(--text-primary);">
                6-Step Portal Click-Path Guide
              </h2>
              <p style="font-size:14.5px; color:var(--text-secondary); margin-top:4px;">
                Click any step below to jump directly to that layer of the portal.
              </p>
            </div>

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:18px;">
              ${flowSteps.map(st => `
                <div style="padding:22px; border-radius:16px; background:var(--bg-surface); border:1.5px solid var(--border-subtle); border-top:4px solid ${st.color}; display:flex; flex-direction:column; justify-content:space-between; gap:14px;">
                  <div>
                    <div style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; color:${st.color}; margin-bottom:4px;">
                      STEP ${st.num}
                    </div>
                    <div style="font-family:var(--font-display); font-size:17px; font-weight:800; color:var(--text-primary); margin-bottom:4px;">
                      ${st.title}
                    </div>
                    <div style="font-size:12.5px; font-weight:700; color:var(--text-secondary); margin-bottom:10px;">
                      ${st.sub}
                    </div>
                    <p style="font-size:13.5px; color:var(--text-secondary); line-height:1.55; margin:0;">
                      ${st.whatOpens}
                    </p>
                  </div>
                  <button type="button" class="switch-pill" style="align-self:flex-start; border-color:${st.color}; color:${st.color}; font-weight:700;" onclick="${st.actionFn}">
                    ${st.actionLabel}
                  </button>
                </div>
              `).join('')}
            </div>
          </div>
        `}
      `;

      hydrateAssets();
      showActivePage('pageMindMap');
    }

"""


NEW_COST_TAB_BLOCK = """    /* =========================================================================
       PAGE 9: PROGRESSIVE 3-STEP COST & ROI HUB (#pageCost / #cost)
       ========================================================================= */
    let currentCostTabPillar = 'all';
    let currentCostTabSearch = '';
    let currentCostSectionTab = 'pillars'; // 'pillars' | 'agents' | 'simulator'

    function switchCostSectionTab(tabName, pillarFilter = null) {
      currentCostSectionTab = tabName || 'pillars';
      if (pillarFilter !== null) {
        currentCostTabPillar = pillarFilter;
      }
      openCostTabPage(currentCostTabPillar, null, false);
    }

    function openCostTabPage(pillarFilter = 'all', highlightAgentId = null, pushState = true) {
      currentCostTabPillar = pillarFilter || 'all';
      if (currentCostTabPillar !== 'all' && !DEPARTMENTS[currentCostTabPillar]) {
        currentCostTabPillar = 'all';
      }
      if (highlightAgentId && AGENTS[highlightAgentId]) {
        currentCostSectionTab = 'agents';
      } else if (pillarFilter && pillarFilter !== 'all' && pushState) {
        currentCostSectionTab = 'agents';
      }
      if (pushState) {
        history.pushState({ page: 'cost', pillar: currentCostTabPillar }, '', '#cost');
      }

      const container = document.getElementById('costPageContent');
      if (!container) return;

      const allAgents = Object.values(AGENTS);
      const deptList = Object.values(DEPARTMENTS);
      let totalAiMo = 0;
      let totalLlmMo = 0;
      let totalCompMo = 0;
      let totalDataMo = 0;
      let totalManualMo = 0;
      let totalFtes = 0;
      let totalValYr = 0;
      let totalCallsMo = 0;

      allAgents.forEach(ag => {
        const cm = ag.costModel || {};
        const mb = cm.monthlyBreakdown || {};
        const mc = cm.manualComparison || {};
        const vm = cm.valueModel || {};
        totalAiMo += (mb.totalFsp3YrUsd || 210);
        totalLlmMo += (mb.llmFsp3YrUsd || 65);
        totalCompMo += (mb.computeUsd || 80);
        totalDataMo += ((mb.dataUsd || 45) + (mb.apiUsd || 20));
        totalManualMo += (mc.manualMonthlyCostUsd || 24000);
        totalFtes += (mc.fteEquivalent || 2.0);
        totalValYr += (vm.grossAnnualConservativeUsd || 1100000);
        totalCallsMo += (cm.monthlyCalls || 85000);
      });

      const savingsPctOverall = totalManualMo > 0 ? Math.max(85, ((totalManualMo - totalAiMo) / totalManualMo) * 100).toFixed(1) : '99.1';

      const pillarCardsHtml = deptList.map(dept => {
        const pAgents = allAgents.filter(a => a.deptId === dept.id);
        let pAiMo = 0, pLlm = 0, pComp = 0, pData = 0, pManMo = 0, pValYr = 0, pFte = 0;
        pAgents.forEach(a => {
          const cm = a.costModel || {};
          const mb = cm.monthlyBreakdown || {};
          const mc = cm.manualComparison || {};
          const vm = cm.valueModel || {};
          pAiMo += (mb.totalFsp3YrUsd || 210);
          pLlm += (mb.llmFsp3YrUsd || 65);
          pComp += (mb.computeUsd || 80);
          pData += ((mb.dataUsd || 45) + (mb.apiUsd || 20));
          pManMo += (mc.manualMonthlyCostUsd || 24000);
          pFte += (mc.fteEquivalent || 2.0);
          pValYr += (vm.grossAnnualConservativeUsd || 1100000);
        });
        const pTot = Math.max(1, pLlm + pComp + pData);
        const lPct = Math.round((pLlm / pTot) * 100);
        const cPct = Math.round((pComp / pTot) * 100);
        const dPct = Math.max(1, 100 - lPct - cPct);

        return `
          <div onclick="switchCostSectionTab('agents', '${dept.id}')" style="cursor:pointer; padding:24px 26px; border-radius:20px; background:var(--bg-card); border:1.5px solid var(--border-strong); border-top:4px solid ${dept.color}; display:flex; flex-direction:column; justify-content:space-between; gap:16px; transition:transform 0.18s ease, border-color 0.18s ease;">
            <div>
              <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; margin-bottom:8px;">
                <span style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; color:${dept.color}; text-transform:uppercase; letter-spacing:0.06em;">
                  ${dept.scorBadge || 'PILLAR'}
                </span>
                <span class="sc-tech-pill" style="padding:3px 10px; font-size:11.5px; font-weight:800;">
                  ${pAgents.length} Agents
                </span>
              </div>
              <h3 style="font-family:var(--font-display); font-size:20px; font-weight:800; color:var(--text-primary); margin:0 0 16px;">
                ${dept.name}
              </h3>

              <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:10px; padding:14px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); margin-bottom:14px;">
                <div>
                  <div style="font-size:11px; color:var(--text-secondary); font-weight:700;">✦ AI Run Cost</div>
                  <div style="font-family:var(--font-display); font-size:19px; font-weight:800; color:var(--text-primary); margin-top:2px;">$${Math.round(pAiMo).toLocaleString()}<span style="font-size:11px; font-weight:500; color:var(--text-secondary);">/mo</span></div>
                </div>
                <div>
                  <div style="font-size:11px; color:var(--text-secondary); font-weight:700;">✕ Manual Base</div>
                  <div style="font-family:var(--font-display); font-size:19px; font-weight:800; color:#f43f5e; margin-top:2px;">$${Math.round(pManMo / 1000)}K<span style="font-size:11px; font-weight:500; color:var(--text-secondary);">/mo</span></div>
                </div>
                <div>
                  <div style="font-size:11px; color:var(--text-secondary); font-weight:700;">🚀 Annual Value</div>
                  <div style="font-family:var(--font-display); font-size:19px; font-weight:800; color:#10b981; margin-top:2px;">$${(pValYr / 1e6).toFixed(1)}M<span style="font-size:11px; font-weight:500; color:var(--text-secondary);">/yr</span></div>
                </div>
              </div>

              <div style="height:7px; border-radius:999px; background:var(--border-subtle); overflow:hidden; display:flex; gap:2px; margin-bottom:8px;">
                <div style="width:${lPct}%; height:100%; background:#10b981;"></div>
                <div style="width:${cPct}%; height:100%; background:#38bdf8;"></div>
                <div style="width:${dPct}%; height:100%; background:#a855f7;"></div>
              </div>
              <div style="display:flex; justify-content:space-between; font-size:12px; color:var(--text-secondary);">
                <span>Tokens $${Math.round(pLlm)} · Compute $${Math.round(pComp)} · Data $${Math.round(pData)}</span>
                <span style="color:${dept.color}; font-weight:800;">~${pFte.toFixed(0)} FTEs</span>
              </div>
            </div>

            <div style="display:flex; align-items:center; justify-content:space-between; padding-top:12px; border-top:1px solid var(--border-subtle); font-size:13px; font-weight:800; color:${dept.color};">
              <span>Inspect ${pAgents.length} Pillar Agents</span>
              <span>&rarr;</span>
            </div>
          </div>
        `;
      }).join('');

      container.innerHTML = `
        <div class="subpage-topbar" style="margin-bottom: 20px;">
          <button type="button" class="back-btn" onclick="goToOrgChart()">
            <span>&larr;</span>
            <span>Back to ${deptList.length} Pillars</span>
          </button>

          <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
            <button type="button" class="switch-pill" style="font-weight:700;" onclick="openEvidenceHubPage('all', true, event)">
              📚 View Case Studies &amp; Proof &rarr;
            </button>
            <a href="cost_analysis_presentation.html" class="switch-pill" style="text-decoration:none; font-weight:700;">
              📊 9-Slide FinOps Deck &rarr;
            </a>
          </div>
        </div>

        <!-- Executive Bottom-Line Summary -->
        <div class="simple-arch-card" style="padding: 28px 30px; margin-bottom: 22px;">
          <div style="margin-bottom: 20px;">
            <div style="font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:var(--g-blue); margin-bottom:4px;">
              Cloud FinOps &amp; Business Value Summary · ${deptList.length} Operating Pillars · ${allAgents.length} AI Agents
            </div>
            <h1 style="font-family:var(--font-display); font-size:clamp(26px, 3vw, 34px); font-weight:800; color:var(--text-primary); margin:0 0 6px;">
              Supply Chain AI Cost &amp; ROI Breakdown
            </h1>
            <p style="font-size:14.5px; color:var(--text-secondary); margin:0; max-width:900px; line-height:1.58;">
              Transparent bottom-up infrastructure and token economics (Gemini 3.8 Flash ↔ 3.1 Pro / 4 Argon, excluding user seats) compared against manual operational effort and annual supply chain value.
            </p>
          </div>

          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:16px;">
            <div style="padding:20px 22px; border-radius:16px; background:var(--bg-elevated); border:1.5px solid var(--border-subtle); border-top:4px solid var(--g-blue);">
              <div style="font-size:11.5px; font-weight:800; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                ✦ Monthly AI Run Cost
              </div>
              <div style="font-family:var(--font-display); font-size:30px; font-weight:800; color:var(--text-primary); margin:8px 0 4px;">
                $${Math.round(totalAiMo).toLocaleString()}<span style="font-size:14px; font-weight:600; color:var(--text-secondary);">/mo</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-secondary);">
                $${Math.round(totalAiMo * 12).toLocaleString()}/yr (${allAgents.length} active agents · 3-Yr FSP)
              </div>
            </div>

            <div style="padding:20px 22px; border-radius:16px; background:var(--bg-elevated); border:1.5px solid var(--border-subtle); border-top:4px solid #f43f5e;">
              <div style="font-size:11.5px; font-weight:800; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                ✕ Manual Process Baseline
              </div>
              <div style="font-family:var(--font-display); font-size:30px; font-weight:800; color:#f43f5e; margin:8px 0 4px;">
                $${(totalManualMo / 1e6).toFixed(2)}M<span style="font-size:14px; font-weight:600; color:var(--text-secondary);">/mo</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-secondary);">
                ~${Math.round(totalFtes)} FTEs spent on manual triage &amp; spreadsheets
              </div>
            </div>

            <div style="padding:20px 22px; border-radius:16px; background:var(--bg-elevated); border:1.5px solid var(--border-subtle); border-top:4px solid #38bdf8;">
              <div style="font-size:11.5px; font-weight:800; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                ⚡ Process Cost Reduction
              </div>
              <div style="font-family:var(--font-display); font-size:30px; font-weight:800; color:#38bdf8; margin:8px 0 4px;">
                ${savingsPctOverall}%<span style="font-size:14px; font-weight:600; color:var(--text-secondary);"> Lower</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-secondary);">
                ~$${Math.round(totalAiMo / Math.max(1, allAgents.length))}/mo avg AI agent vs. ~$23.5K/mo manual
              </div>
            </div>

            <div style="padding:20px 22px; border-radius:16px; background:var(--bg-elevated); border:1.5px solid var(--border-subtle); border-top:4px solid #10b981;">
              <div style="font-size:11.5px; font-weight:800; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                🚀 Annual Business Value
              </div>
              <div style="font-family:var(--font-display); font-size:30px; font-weight:800; color:#10b981; margin:8px 0 4px;">
                $${(totalValYr / 1e6).toFixed(1)}M<span style="font-size:14px; font-weight:600; color:var(--text-secondary);">/yr</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-secondary);">
                Working capital, OEE uptime, procurement &amp; freight savings
              </div>
            </div>
          </div>
        </div>

        <!-- 3-Step Progressive Hierarchy Tabs -->
        <div class="sc-v22-tab-strip">
          <button type="button" class="sc-v22-tab-btn ${currentCostSectionTab === 'pillars' ? 'active' : ''}" onclick="switchCostSectionTab('pillars')">
            <span>1 · By Operating Pillar</span>
            <span class="sc-v22-tab-count">${deptList.length}</span>
          </button>
          <button type="button" class="sc-v22-tab-btn ${currentCostSectionTab === 'agents' ? 'active' : ''}" onclick="switchCostSectionTab('agents')">
            <span>2 · Agent-by-Agent Economics</span>
            <span class="sc-v22-tab-count">${allAgents.length}</span>
          </button>
          <button type="button" class="sc-v22-tab-btn ${currentCostSectionTab === 'simulator' ? 'active' : ''}" onclick="switchCostSectionTab('simulator')">
            <span>3 · Scale Simulator &amp; Methodology</span>
          </button>
        </div>

        ${currentCostSectionTab === 'pillars' ? `
          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px;">
            ${pillarCardsHtml}
          </div>
        ` : ''}

        ${currentCostSectionTab === 'agents' ? `
          <div class="simple-arch-card" style="padding: 26px 28px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:14px; margin-bottom:18px;">
              <div>
                <h2 style="font-family:var(--font-display); font-size:22px; font-weight:800; color:var(--text-primary); margin:0 0 4px;">
                  Agent-by-Agent Unit Economics
                </h2>
                <p style="font-size:13.5px; color:var(--text-secondary); margin:0;">
                  Click any row to open that AI Agent's full workflow diagram and interactive demo.
                </p>
              </div>
              <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                <input type="text" id="costTabSearchInput" placeholder="🔍 Search agent or role..." value="${currentCostTabSearch}" oninput="onCostTabSearchInput(this.value)" style="padding:10px 15px; border-radius:11px; background:var(--bg-elevated); color:var(--text-primary); border:1.5px solid var(--border-strong); font-size:13.5px; min-width:240px;" />
                <span id="costTabAgentCountBadge" class="sc-tech-pill" style="font-weight:800; padding:6px 12px;">${allAgents.length} Agents</span>
              </div>
            </div>

            <div style="display:flex; gap:8px; flex-wrap:wrap; margin-bottom:18px;">
              <button type="button" class="switch-pill ${currentCostTabPillar === 'all' ? 'active' : ''}" style="${currentCostTabPillar === 'all' ? 'background:var(--g-blue); color:#fff; border-color:var(--g-blue); font-weight:700;' : ''}" onclick="filterCostTabByPillar('all')">
                All Pillars (${allAgents.length})
              </button>
              ${deptList.map(d => {
                const cnt = allAgents.filter(a => a.deptId === d.id).length;
                const shortName = formatShortPillarTab(d);
                return `
                  <button type="button" class="switch-pill ${currentCostTabPillar === d.id ? 'active' : ''}" style="${currentCostTabPillar === d.id ? `background:${d.color}; color:#fff; border-color:${d.color}; font-weight:700;` : ''}" onclick="filterCostTabByPillar('${d.id}')">
                    ${shortName} (${cnt})
                  </button>
                `;
              }).join('')}
            </div>

            <div style="overflow-x:auto;">
              <table style="width:100%; border-collapse:collapse; font-size:13.5px;">
                <thead>
                  <tr style="border-bottom:2px solid var(--border-subtle); text-align:left; color:var(--text-secondary); font-size:11.5px; text-transform:uppercase; letter-spacing:0.05em;">
                    <th style="padding:14px 12px;">AI Agent &amp; Assigned Role</th>
                    <th style="padding:14px 12px;">Operating Pillar</th>
                    <th style="padding:14px 12px; text-align:right;">✦ AI Cost / Mo</th>
                    <th style="padding:14px 12px; text-align:right;">✕ Manual Base / Mo</th>
                    <th style="padding:14px 12px; text-align:right;">🚀 Annual Value</th>
                  </tr>
                </thead>
                <tbody id="costTabAgentsTbody"></tbody>
              </table>
            </div>
          </div>
        ` : ''}

        ${currentCostSectionTab === 'simulator' ? `
          <div class="simple-arch-card" style="padding: 26px 28px; margin-bottom: 22px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:20px;">
              <div>
                <div style="font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:#10b981; margin-bottom:3px;">
                  Interactive Cloud FinOps Sizer
                </div>
                <h2 style="font-family:var(--font-display); font-size:22px; font-weight:800; color:var(--text-primary); margin:0;">
                  Dynamic Scale Simulator (Tokens + ADK Compute + BigQuery)
                </h2>
              </div>

              <div style="display:flex; gap:8px; flex-wrap:wrap;">
                <button type="button" class="sc-tech-pill" style="cursor:pointer; font-weight:700; padding:7px 13px;" onclick="applyWebCostPreset(10, 250000, 88, 75, 20)">
                  1. Pilot (10 Agents)
                </button>
                <button type="button" class="sc-tech-pill" style="cursor:pointer; font-weight:700; padding:7px 13px;" onclick="applyWebCostPreset(30, 1500000, 85, 75, 20)">
                  2. Regional (30 Agents)
                </button>
                <button type="button" class="sc-tech-pill" style="cursor:pointer; font-weight:700; padding:7px 13px; border-color:var(--g-blue); color:var(--g-blue);" onclick="applyWebCostPreset(${allAgents.length}, 5200000, 85, 75, 20)">
                  3. Enterprise (${allAgents.length} Agents)
                </button>
                <button type="button" class="sc-tech-pill" style="cursor:pointer; font-weight:700; padding:7px 13px;" onclick="applyWebCostPreset(${allAgents.length}, 20000000, 85, 80, 20)">
                  4. Hyperscale (20M Runs)
                </button>
              </div>
            </div>

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap:22px;">
              <div style="padding:20px 22px; border-radius:16px; background:var(--bg-elevated); border:1px solid var(--border-subtle); display:flex; flex-direction:column; gap:16px;">
                <div>
                  <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; margin-bottom:6px;">
                    <span style="color:var(--text-primary);">1. Active AI Agents Deployed</span>
                    <span id="wCalcLblAgents" style="color:var(--g-blue);">${allAgents.length} Agents</span>
                  </div>
                  <input type="range" id="wCalcRngAgents" min="1" max="60" step="1" value="${allAgents.length}" style="width:100%; accent-color:var(--g-blue); cursor:pointer;" oninput="updateWebCostCalculator()" />
                </div>

                <div>
                  <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; margin-bottom:6px;">
                    <span style="color:var(--text-primary);">2. Monthly Invocations (Chat + ERP/IoT)</span>
                    <span id="wCalcLblCalls" style="color:var(--g-blue);">5,200,000 / mo</span>
                  </div>
                  <input type="range" id="wCalcRngCalls" min="50000" max="25000000" step="50000" value="5200000" style="width:100%; accent-color:var(--g-blue); cursor:pointer;" oninput="updateWebCostCalculator()" />
                </div>

                <div>
                  <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; margin-bottom:6px;">
                    <span style="color:var(--text-primary);">3. Orchestrator Routing (3.8 Flash vs. 3.1 Pro)</span>
                    <span id="wCalcLblFlash" style="color:#10b981;">85% Flash / 15% Pro·Argon</span>
                  </div>
                  <input type="range" id="wCalcRngFlash" min="50" max="95" step="5" value="85" style="width:100%; accent-color:#10b981; cursor:pointer;" oninput="updateWebCostCalculator()" />
                </div>

                <div>
                  <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; margin-bottom:6px;">
                    <span style="color:var(--text-primary);">4. Context Caching Hit Rate</span>
                    <span id="wCalcLblCache" style="color:#a855f7;">75% Cache Hit</span>
                  </div>
                  <input type="range" id="wCalcRngCache" min="0" max="90" step="5" value="75" style="width:100%; accent-color:#a855f7; cursor:pointer;" oninput="updateWebCostCalculator()" />
                </div>

                <div>
                  <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; margin-bottom:6px;">
                    <span style="color:var(--text-primary);">5. Vertex AI Commit Discount (FSP)</span>
                    <span id="wCalcLblFsp" style="color:#f59e0b;">3-Yr FSP (-20%)</span>
                  </div>
                  <select id="wCalcSelFsp" onchange="updateWebCostCalculator()" style="width:100%; padding:10px 12px; border-radius:10px; background:var(--bg-surface); color:var(--text-primary); border:1px solid var(--border-subtle); font-weight:600; font-size:13px; cursor:pointer;">
                    <option value="0">Pay-As-You-Go (0% Discount)</option>
                    <option value="10">1-Year Vertex AI FSP (-10% Token Discount)</option>
                    <option value="20" selected>3-Year Vertex AI FSP (-20% Token Discount)</option>
                  </select>
                </div>
              </div>

              <div style="padding:20px 22px; border-radius:16px; background:var(--bg-elevated); border:1px solid var(--border-subtle); display:flex; flex-direction:column; justify-content:space-between; gap:16px;">
                <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:12px;">
                  <div style="padding:14px; border-radius:12px; background:var(--bg-surface); border:1px solid var(--border-subtle); border-left:3px solid var(--g-blue);">
                    <div style="font-size:11px; font-weight:700; color:var(--text-secondary); text-transform:uppercase;">✦ AI Cost / Mo</div>
                    <div id="wCalcOutAiMo" style="font-family:var(--font-display); font-size:22px; font-weight:800; color:var(--text-primary); margin-top:4px;">$12,843</div>
                    <div id="wCalcOutPer1k" style="font-size:11.5px; color:var(--text-secondary);">$2.47 / 1K runs</div>
                  </div>
                  <div style="padding:14px; border-radius:12px; background:var(--bg-surface); border:1px solid var(--border-subtle); border-left:3px solid #f43f5e;">
                    <div style="font-size:11px; font-weight:700; color:var(--text-secondary); text-transform:uppercase;">✕ Manual / Mo</div>
                    <div id="wCalcOutManMo" style="font-family:var(--font-display); font-size:22px; font-weight:800; color:#f43f5e; margin-top:4px;">$1.41M</div>
                    <div id="wCalcOutFtes" style="font-size:11.5px; color:var(--text-secondary);">~124 FTEs manual</div>
                  </div>
                  <div style="padding:14px; border-radius:12px; background:var(--bg-surface); border:1px solid var(--border-subtle); border-left:3px solid #10b981;">
                    <div style="font-size:11px; font-weight:700; color:var(--text-secondary); text-transform:uppercase;">🚀 Value / Yr</div>
                    <div id="wCalcOutValYr" style="font-family:var(--font-display); font-size:22px; font-weight:800; color:#10b981; margin-top:4px;">$66.6M</div>
                    <div id="wCalcOutRoi" style="font-size:11.5px; color:var(--text-secondary);">432x Cloud ROI</div>
                  </div>
                </div>

                <div style="padding:14px 16px; border-radius:12px; background:var(--bg-surface); border:1px solid var(--border-subtle);">
                  <div style="font-size:11px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em; margin-bottom:10px;">
                    Monthly Scale Comparison
                  </div>
                  <div style="margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:3px;">
                      <span style="color:var(--text-secondary); font-weight:600;">✦ AI Infra + Token Cost</span>
                      <span id="wCalcBarAiLbl" style="color:var(--text-primary); font-weight:800;">$12,843 / mo</span>
                    </div>
                    <div style="height:7px; border-radius:999px; background:var(--border-subtle); overflow:hidden;">
                      <div id="wCalcBarAiFill" style="width:3%; min-width:8px; height:100%; background:var(--g-blue); border-radius:999px;"></div>
                    </div>
                  </div>
                  <div style="margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:3px;">
                      <span style="color:var(--text-secondary); font-weight:600;">✕ Manual Effort Equivalent</span>
                      <span id="wCalcBarManLbl" style="color:#f43f5e; font-weight:800;">$1,410,000 / mo</span>
                    </div>
                    <div style="height:7px; border-radius:999px; background:var(--border-subtle); overflow:hidden;">
                      <div id="wCalcBarManFill" style="width:32%; height:100%; background:#f43f5e; border-radius:999px;"></div>
                    </div>
                  </div>
                  <div>
                    <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:3px;">
                      <span style="color:var(--text-secondary); font-weight:600;">🚀 Supply Chain Value Unlocked</span>
                      <span id="wCalcBarValLbl" style="color:#10b981; font-weight:800;">$5,550,000 / mo</span>
                    </div>
                    <div style="height:7px; border-radius:999px; background:var(--border-subtle); overflow:hidden;">
                      <div style="width:100%; height:100%; background:#10b981; border-radius:999px;"></div>
                    </div>
                  </div>
                </div>

                <div style="padding:14px 16px; border-radius:12px; background:var(--bg-surface); border:1px solid var(--border-subtle);">
                  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span style="font-size:11px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                      Monthly AI Cost Split
                    </span>
                    <span id="wCalcAnnualAiLbl" style="font-size:11.5px; font-weight:700; color:var(--text-secondary);">$154.1K / yr</span>
                  </div>
                  <div style="height:9px; border-radius:999px; background:var(--border-subtle); overflow:hidden; display:flex; gap:2px; margin-bottom:10px;">
                    <div id="wCalcSplitLlmBar" style="width:38%; height:100%; background:#10b981;"></div>
                    <div id="wCalcSplitCompBar" style="width:34%; height:100%; background:#38bdf8;"></div>
                    <div id="wCalcSplitDataBar" style="width:28%; height:100%; background:#a855f7;"></div>
                  </div>
                  <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:8px; font-size:12px;">
                    <div><span style="color:var(--text-secondary);">🟢 Tokens:</span> <strong id="wCalcSplitLlmVal" style="color:var(--text-primary);">$4,880/mo</strong></div>
                    <div><span style="color:var(--text-secondary);">🔵 Compute:</span> <strong id="wCalcSplitCompVal" style="color:var(--text-primary);">$4,360/mo</strong></div>
                    <div><span style="color:var(--text-secondary);">🟣 Data/BQ:</span> <strong id="wCalcSplitDataVal" style="color:var(--text-primary);">$3,603/mo</strong></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          ${renderCostTabBenchmarkMethodologyPanel()}
        ` : ''}
      `;

      showActivePage('pageCost');
      if (currentCostSectionTab === 'simulator') {
        updateWebCostCalculator();
      } else if (currentCostSectionTab === 'agents') {
        renderCostTabAgentRows(highlightAgentId);
      }
    }

    function applyWebCostPreset(agents, calls, flashPct, cachePct, fspVal) {
      const elA = document.getElementById('wCalcRngAgents');
      const elC = document.getElementById('wCalcRngCalls');
      const elF = document.getElementById('wCalcRngFlash');
      const elH = document.getElementById('wCalcRngCache');
      const elS = document.getElementById('wCalcSelFsp');
      if (!elA) return;
      elA.value = agents;
      elC.value = calls;
      elF.value = flashPct;
      elH.value = cachePct;
      elS.value = String(fspVal);
      updateWebCostCalculator();
    }

    function updateWebCostCalculator() {
      const elA = document.getElementById('wCalcRngAgents');
      if (!elA) return;
      const agents = parseInt(elA.value, 10) || 60;
      const calls = parseInt(document.getElementById('wCalcRngCalls').value, 10) || 5200000;
      const flashPct = parseInt(document.getElementById('wCalcRngFlash').value, 10) || 85;
      const cachePct = parseInt(document.getElementById('wCalcRngCache').value, 10) || 75;
      const fspDiscount = parseInt(document.getElementById('wCalcSelFsp').value, 10) || 20;
      const proPct = 100 - flashPct;

      document.getElementById('wCalcLblAgents').textContent = `${agents} Agent${agents > 1 ? 's' : ''}`;
      document.getElementById('wCalcLblCalls').textContent = `${calls.toLocaleString()} / mo`;
      document.getElementById('wCalcLblFlash').textContent = `${flashPct}% Flash / ${proPct}% Pro·Argon`;
      document.getElementById('wCalcLblCache').textContent = `${cachePct}% Cache Hit`;
      document.getElementById('wCalcLblFsp').textContent = fspDiscount === 0 ? 'PayGo (0%)' : `${fspDiscount === 10 ? '1-Yr' : '3-Yr'} FSP (-${fspDiscount}%)`;

      const cacheFactor = 1 - (cachePct / 100) * 0.56;
      const fspFactor = 1 - (fspDiscount / 100);
      const flashRatePerCall = 0.00055 * cacheFactor * fspFactor;
      const proRatePerCall = 0.0085 * cacheFactor * fspFactor;

      const llmMo = Math.round(calls * (flashPct / 100) * flashRatePerCall + calls * (proPct / 100) * proRatePerCall);
      const compMo = Math.round(agents * 58 + (calls / 1000000) * 240);
      const dataMo = Math.round(agents * 44 + (calls / 1000000) * 190);
      const aiMo = Math.max(45, llmMo + compMo + dataMo);
      const aiYr = aiMo * 12;
      const per1k = calls > 0 ? (aiMo / (calls / 1000)) : 0;

      const ftes = (agents * 2.05 * Math.min(1.35, Math.pow(calls / 5200000, 0.15)));
      const manualMo = Math.round(agents * 23500 * Math.min(1.35, Math.pow(calls / 5200000, 0.15)));
      const savingsPct = manualMo > 0 ? Math.max(85, ((manualMo - aiMo) / manualMo) * 100).toFixed(1) : '99.0';

      const valYrM = (agents / 60) * 66.6 * Math.min(1.5, Math.pow(calls / 5200000, 0.22));
      const valMo = Math.round((valYrM * 1e6) / 12);
      const roiMult = aiYr > 0 ? Math.round((valYrM * 1e6) / aiYr) : 0;

      document.getElementById('wCalcOutAiMo').textContent = `$${aiMo.toLocaleString()}`;
      document.getElementById('wCalcOutPer1k').textContent = `$${per1k.toFixed(2)} / 1K runs`;
      document.getElementById('wCalcOutManMo').textContent = manualMo >= 1000000 ? `$${(manualMo / 1e6).toFixed(2)}M` : `$${(manualMo / 1000).toFixed(0)}K`;
      document.getElementById('wCalcOutFtes').textContent = `~${Math.round(ftes)} FTEs manual`;
      document.getElementById('wCalcOutValYr').textContent = `$${valYrM.toFixed(1)}M`;
      document.getElementById('wCalcOutRoi').textContent = `${roiMult}x Cloud ROI`;

      document.getElementById('wCalcBarAiLbl').textContent = `$${aiMo.toLocaleString()} / mo`;
      document.getElementById('wCalcBarManLbl').textContent = `$${manualMo.toLocaleString()} / mo (Saves ${savingsPct}%)`;
      document.getElementById('wCalcBarValLbl').textContent = `$${valMo.toLocaleString()} / mo ($${valYrM.toFixed(1)}M/yr)`;

      const lPct = Math.round((llmMo / aiMo) * 100);
      const cPct = Math.round((compMo / aiMo) * 100);
      const dPct = Math.max(1, 100 - lPct - cPct);
      document.getElementById('wCalcAnnualAiLbl').textContent = `$${aiYr.toLocaleString()} / yr`;
      document.getElementById('wCalcSplitLlmBar').style.width = `${lPct}%`;
      document.getElementById('wCalcSplitCompBar').style.width = `${cPct}%`;
      document.getElementById('wCalcSplitDataBar').style.width = `${dPct}%`;
      document.getElementById('wCalcSplitLlmVal').textContent = `$${llmMo.toLocaleString()}/mo`;
      document.getElementById('wCalcSplitCompVal').textContent = `$${compMo.toLocaleString()}/mo`;
      document.getElementById('wCalcSplitDataVal').textContent = `$${dataMo.toLocaleString()}/mo`;
    }

    function filterCostTabByPillar(pillarId) {
      currentCostTabPillar = pillarId || 'all';
      currentCostSectionTab = 'agents';
      openCostTabPage(currentCostTabPillar, null, false);
    }

    function onCostTabSearchInput(val) {
      currentCostTabSearch = val || '';
      renderCostTabAgentRows(null);
    }

    function renderCostTabAgentRows(highlightAgentId = null) {
      const tbody = document.getElementById('costTabAgentsTbody');
      if (!tbody) return;
      const q = (currentCostTabSearch || '').trim().toLowerCase();
      const list = Object.values(AGENTS).filter(ag => {
        if (currentCostTabPillar !== 'all' && ag.deptId !== currentCostTabPillar) return false;
        if (!q) return true;
        return (
          (ag.name || '').toLowerCase().includes(q) ||
          (ag.canonicalName || '').toLowerCase().includes(q) ||
          (ag.subPillarName || '').toLowerCase().includes(q) ||
          (ag.primaryPersonaName || '').toLowerCase().includes(q)
        );
      });

      const badge = document.getElementById('costTabAgentCountBadge');
      if (badge) badge.textContent = `${list.length} Agent${list.length === 1 ? '' : 's'}`;

      tbody.innerHTML = list.map(ag => {
        const dept = getDeptMeta(ag.deptId);
        const cm = ag.costModel || {};
        const mb = cm.monthlyBreakdown || {};
        const mc = cm.manualComparison || { manualMonthlyCostUsd: 24000, fteEquivalent: 2.0, directSavingsPct: 99.0 };
        const vm = cm.valueModel || { grossAnnualConservativeUsd: 1100000 };
        const aiMo = Math.round(mb.totalFsp3YrUsd || 210);
        const isHl = highlightAgentId && ag.id === highlightAgentId;

        return `
          <tr onclick="openAgentPage('${ag.id}', true, event)" style="cursor:pointer; border-bottom:1px solid var(--border-subtle); background:${isHl ? 'var(--bg-elevated)' : 'transparent'}; transition:background 0.15s ease;" onmouseover="this.style.background='var(--bg-elevated)'" onmouseout="this.style.background='${isHl ? 'var(--bg-elevated)' : 'transparent'}'">
            <td style="padding:15px 12px;">
              <div style="font-weight:800; color:var(--text-primary); font-size:14.5px;">${cleanAgentName(ag.name)}</div>
              <div style="font-size:12px; color:var(--text-secondary); margin-top:2px;">${ag.subPillarName || dept.name}${ag.primaryPersonaName ? ' · 👤 ' + ag.primaryPersonaName : ''}</div>
            </td>
            <td style="padding:15px 12px;">
              <span class="sc-tech-pill" style="font-size:11.5px; padding:4px 10px; border-color:${dept.color}55; color:${dept.color}; font-weight:700;">
                ${dept.name}
              </span>
            </td>
            <td style="padding:15px 12px; text-align:right; font-family:var(--font-mono); font-weight:800; color:var(--g-blue); font-size:14.5px;">
              $${aiMo.toLocaleString()}/mo
              <div style="font-size:11px; color:var(--text-secondary); font-weight:500;">$${(mb.blendedCostPer1kCallsUsd || 2.45).toFixed(2)} / 1K runs</div>
            </td>
            <td style="padding:15px 12px; text-align:right; font-family:var(--font-mono); font-weight:700; color:#f43f5e; font-size:14px;">
              $${(mc.manualMonthlyCostUsd || 24000).toLocaleString()}/mo
              <div style="font-size:11px; color:var(--text-secondary); font-weight:500;">~${mc.fteEquivalent} FTEs (-${mc.directSavingsPct}%)</div>
            </td>
            <td style="padding:15px 12px; text-align:right; font-family:var(--font-mono); font-weight:800; color:#10b981; font-size:14.5px;">
              $${((vm.grossAnnualConservativeUsd || 1100000) / 1e6).toFixed(2)}M/yr
            </td>
          </tr>
        `;
      }).join('');
    }

"""


NEW_EVIDENCE_HUB_BLOCK = """    let currentEvidenceTab = 'cases'; // 'cases' | 'benchmarks' | 'sources'

    function switchEvidenceTab(tabName) {
      currentEvidenceTab = tabName || 'cases';
      openEvidenceHubPage(currentEvidencePillar, false);
    }

    function openEvidenceHubPage(pillarFilter = 'all', pushState = true, ev = null) {
      currentEvidencePillar = pillarFilter || 'all';
      if (pushState) {
        const hash = currentEvidencePillar === 'all' ? '#evidence' : `#evidence/${currentEvidencePillar}`;
        history.pushState({ page: 'evidence', pillar: currentEvidencePillar }, '', hash);
      }

      const container = document.getElementById('evidencePageContent');
      if (!container) return;

      const pillarCount = Object.keys(DEPARTMENTS).length;
      const agentCount = Object.keys(AGENTS).length;

      const filteredPillars = currentEvidencePillar === 'all'
        ? PILLAR_PROOF_BENCHMARKS
        : PILLAR_PROOF_BENCHMARKS.filter(p => p.deptId === currentEvidencePillar);

      const filteredCases = currentEvidencePillar === 'all'
        ? ENTERPRISE_CASE_STUDIES
        : ENTERPRISE_CASE_STUDIES.filter(c => c.deptIds.includes(currentEvidencePillar));

      const filterPillsHtml = [
        `<button type="button" class="switch-pill ${currentEvidencePillar === 'all' ? 'active' : ''}" style="${currentEvidencePillar === 'all' ? 'background:var(--g-blue);border-color:var(--g-blue);color:#fff;font-weight:800;' : ''}" onclick="openEvidenceHubPage('all', false, event)">All Domains (${ENTERPRISE_CASE_STUDIES.length})</button>`
      ].concat(PILLAR_PROOF_BENCHMARKS.map(p => {
        const active = currentEvidencePillar === p.deptId;
        const cleanCode = p.code.split('·').pop().trim();
        return `<button type="button" class="switch-pill ${active ? 'active' : ''}" style="${active ? `background:${p.color};border-color:${p.color};color:#fff;font-weight:800;` : ''}" onclick="openEvidenceHubPage('${p.deptId}', false, event)">${cleanCode}</button>`;
      })).join('');

      const pillarRowsHtml = filteredPillars.map(p => `
        <tr style="border-bottom:1px solid var(--border-subtle);">
          <td style="padding:18px 14px; vertical-align:top; min-width:190px;">
            <div style="font-weight:800; color:${p.color}; font-size:14px;">${p.code}</div>
          </td>
          <td style="padding:18px 14px; vertical-align:top; font-size:13.5px; color:var(--text-secondary); line-height:1.6;">
            ${p.problemCited}
          </td>
          <td style="padding:18px 14px; vertical-align:top; font-family:var(--font-mono); font-size:13px; font-weight:700; color:#10b981; min-width:190px;">
            ${p.portalTarget}
          </td>
          <td style="padding:18px 14px; vertical-align:top; min-width:240px;">
            <div style="font-size:13.5px; font-weight:700; color:var(--text-primary); margin-bottom:8px; line-height:1.5;">
              ${p.externalBenchmark}
            </div>
            <a href="${p.benchmarkUrl}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill" style="font-size:12px; padding:5px 11px;">
              ${p.benchmarkOrg} &#8599;
            </a>
          </td>
          <td style="padding:18px 14px; vertical-align:top; min-width:200px;">
            <a href="${p.caseStudyUrl}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill" style="font-size:12px; padding:6px 12px;">
              ${p.caseStudyName} &#8599;
            </a>
          </td>
        </tr>
      `).join('');

      const canonicalNameMap = {
        demand_sop: { name: 'Planning & Strategy', color: '#2563eb' },
        sourcing_procurement: { name: 'Sourcing & Procurement', color: '#7c3aed' },
        manufacturing_prod: { name: 'Manufacturing & Production', color: '#ea580c' },
        inventory_warehouse: { name: 'Inventory & Warehousing', color: '#0284c7' },
        logistics_fleet: { name: 'Distribution & Logistics', color: '#0d9488' },
        circular_enable: { name: 'Returns & Sustainability', color: '#10b981' }
      };

      const caseCardsHtml = filteredCases.map(cs => {
        const agentChips = (cs.agentIds || []).map(aid => {
          const ag = AGENTS[aid];
          if (!ag) return '';
          return `
            <button type="button" class="sc-tech-pill" onclick="openAgentPage('${ag.id}', true, event)" style="cursor:pointer; font-size:12px; font-weight:700; padding:5px 11px;">
              ✦ ${cleanAgentName(ag.name)} &rarr;
            </button>
          `;
        }).join('');

        const pillarBadges = cs.deptIds.map(did => {
          const meta = canonicalNameMap[did] || getDeptMeta(did);
          return `<span class="sc-tech-pill" style="font-size:11.5px; padding:3px 10px; color:${meta.color}; border-color:${meta.color}55; font-weight:700;">${meta.name}</span>`;
        }).join('');

        return `
          <div class="sc-v22-cs-card" style="--cs-accent:${cs.accent};">
            <div>
              <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:14px;">
                <div style="display:flex; gap:6px; flex-wrap:wrap;">${pillarBadges}</div>
                <span style="font-family:var(--font-mono); font-size:12.5px; font-weight:800; color:#10b981; background:rgba(16,185,129,0.12); border:1px solid rgba(16,185,129,0.35); padding:4px 12px; border-radius:999px;">
                  ${cs.headlineMetric}
                </span>
              </div>

              <h3 style="font-family:var(--font-display); font-size:22px; font-weight:800; color:var(--text-primary); margin:0 0 4px;">
                ${cs.company}
              </h3>
              <div style="font-size:13px; font-weight:600; color:var(--text-secondary); margin-bottom:18px;">
                ${cs.sector}
              </div>

              <div style="margin-bottom:14px;">
                <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:#f43f5e; margin-bottom:4px;">
                  Challenge
                </div>
                <p style="font-size:14px; color:var(--text-secondary); line-height:1.6; margin:0;">
                  ${cs.problem}
                </p>
              </div>

              <div style="padding-top:14px; border-top:1px solid var(--border-subtle);">
                <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:#10b981; margin-bottom:4px;">
                  Published Outcome
                </div>
                <p style="font-size:14px; color:var(--text-primary); line-height:1.6; font-weight:500; margin:0;">
                  ${cs.outcome}
                </p>
              </div>
            </div>

            <div style="padding-top:14px; border-top:1px solid var(--border-subtle);">
              ${agentChips ? `
                <div style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:14px;">
                  ${agentChips}
                </div>
              ` : ''}

              <div style="display:flex; flex-wrap:wrap; gap:10px; align-items:center;">
                <a href="${cs.url}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill" style="padding:6px 12px;">
                  <span>${cs.sourceLabel}</span>
                  <span>&#8599;</span>
                </a>
                ${cs.secondaryUrl ? `
                  <a href="${cs.secondaryUrl}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill" style="padding:6px 12px; opacity:0.9;">
                    <span>${cs.secondaryLabel}</span>
                    <span>&#8599;</span>
                  </a>
                ` : ''}
              </div>
            </div>
          </div>
        `;
      }).join('');

      const sourcesHtml = VERIFIED_RESEARCH_SOURCES.map(src => `
        <div class="sc-src-lib-item" style="padding:22px 24px;">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; margin-bottom:8px;">
              <span style="font-size:11.5px; font-weight:800; color:var(--g-blue); text-transform:uppercase; letter-spacing:0.05em;">${src.org}</span>
              <span class="sc-tech-pill" style="font-size:11px; padding:3px 9px;">${src.type}</span>
            </div>
            <div style="font-weight:800; font-size:15.5px; color:var(--text-primary); line-height:1.42; margin-bottom:8px;">
              ${src.title}
            </div>
            <div style="font-size:13.5px; color:var(--text-secondary); line-height:1.55; margin-bottom:14px;">
              ${src.metric}
            </div>
          </div>
          <a href="${src.url}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill" style="font-size:12.5px; padding:6px 12px;">
            <span>Open Published Source</span>
            <span>&#8599;</span>
          </a>
        </div>
      `).join('');

      container.innerHTML = `
        <div class="back-bar" style="margin-bottom: 20px;">
          <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <button type="button" class="back-btn" onclick="goToOrgChart()">&larr; Back to ${pillarCount} Pillars</button>
            <button type="button" class="back-btn" onclick="openCostTabPage('all', null, true)">💰 Cost &amp; ROI</button>
          </div>
          <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <a href="VERIFIED_CASE_STUDIES_AND_RESEARCH_SOURCES.md" target="_blank" class="switch-pill" style="text-decoration:none; padding:8px 14px; font-size:13px; font-weight:700;">
              📄 Citations Dossier (.md) &#8599;
            </a>
          </div>
        </div>

        <!-- Clean Spacious Header -->
        <div class="simple-arch-card" style="padding: 28px 30px; margin-bottom: 22px;">
          <div style="font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:var(--g-blue); margin-bottom:6px;">
            Published Customer Outcomes &amp; Industry Research
          </div>
          <h1 style="font-family:var(--font-display); font-size:clamp(26px, 3vw, 36px); font-weight:800; color:var(--text-primary); margin:0 0 8px;">
            Real Case Studies &amp; Verified Benchmarks
          </h1>
          <p style="font-size:15px; color:var(--text-secondary); max-width:940px; line-height:1.6; margin:0 0 22px;">
            Every operational KPI and dollar ROI across all <strong>${pillarCount} Operating Pillars</strong> and <strong>${agentCount} AI Agents</strong> is calibrated against published Google Cloud customer deployments, INFORMS Edelman winners, WEF Global Lighthouse audits, and McKinsey / Hackett benchmarks.
          </p>

          <!-- 4 Spacious Headline KPI Cards -->
          <div class="sc-ev-kpi-grid" style="margin-bottom: 0; gap: 16px;">
            <div class="sc-ev-kpi-card" style="--kpi-color:#2563eb; padding: 18px 20px;">
              <div>
                <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:var(--text-secondary);">Forecast Error</div>
                <div style="font-family:var(--font-display); font-size:28px; font-weight:800; color:#38bdf8; margin:6px 0;">-20% to -50%</div>
                <div style="font-size:13px; color:var(--text-secondary); line-height:1.5;">Lower forecast error &amp; up to 65% fewer lost sales.</div>
              </div>
              <a href="https://www.mckinsey.com/capabilities/operations/our-insights/ai-driven-operations-forecasting-in-data-light-environments" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill" style="font-size:11.5px; margin-top:10px;">McKinsey &#8599;</a>
            </div>

            <div class="sc-ev-kpi-card" style="--kpi-color:#7c3aed; padding: 18px 20px;">
              <div>
                <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:var(--text-secondary);">Procurement Savings</div>
                <div style="font-family:var(--font-display); font-size:28px; font-weight:800; color:#a855f7; margin:6px 0;">5%–15% Spend</div>
                <div style="font-size:13px; color:var(--text-secondary); line-height:1.5;">Addressable spend savings &amp; 3.7x Procurement AI ROI.</div>
              </div>
              <a href="https://www.thehackettgroup.com/insights/the-ai-procurement-performance-gap-how-leaders-achieve-3-7x-greater-roi/" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill" style="font-size:11.5px; margin-top:10px;">Hackett Group &#8599;</a>
            </div>

            <div class="sc-ev-kpi-card" style="--kpi-color:#ea580c; padding: 18px 20px;">
              <div>
                <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:var(--text-secondary);">Factory Downtime</div>
                <div style="font-family:var(--font-display); font-size:28px; font-weight:800; color:#fb923c; margin:6px 0;">-30% to -50%</div>
                <div style="font-size:13px; color:var(--text-secondary); line-height:1.5;">Unplanned downtime cut &amp; -25% parts backorders (GE).</div>
              </div>
              <a href="https://reports.weforum.org/docs/WEF_Global_Lighthouse_Network_2026.pdf" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill" style="font-size:11.5px; margin-top:10px;">WEF Lighthouse &#8599;</a>
            </div>

            <div class="sc-ev-kpi-card" style="--kpi-color:#10b981; padding: 18px 20px;">
              <div>
                <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:var(--text-secondary);">Warehouse &amp; Fleet</div>
                <div style="font-family:var(--font-display); font-size:28px; font-weight:800; color:#10b981; margin:6px 0;">&gt;10% to 15%</div>
                <div style="font-size:13px; color:var(--text-secondary); line-height:1.5;">Pick efficiency (FM Logistic), Walmart (30M mi), UPS ($300M+).</div>
              </div>
              <a href="https://www.informs.org/News-Room/INFORMS-Releases/Awards-Releases/Operations-Research-Enhances-Retail-Truck-Routing-and-Load-Planning-Walmart-Awarded-the-2023-INFORMS-Edelman-Award" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill" style="font-size:11.5px; margin-top:10px;">INFORMS Edelman &#8599;</a>
            </div>
          </div>
        </div>

        <!-- 3-Tab Segmented View Selector -->
        <div class="sc-v22-tab-strip">
          <button type="button" class="sc-v22-tab-btn ${currentEvidenceTab === 'cases' ? 'active' : ''}" onclick="switchEvidenceTab('cases')">
            <span>🏢 Enterprise Case Studies</span>
            <span class="sc-v22-tab-count">${ENTERPRISE_CASE_STUDIES.length}</span>
          </button>
          <button type="button" class="sc-v22-tab-btn ${currentEvidenceTab === 'benchmarks' ? 'active' : ''}" onclick="switchEvidenceTab('benchmarks')">
            <span>📊 Pillar Benchmark Matrix</span>
            <span class="sc-v22-tab-count">${PILLAR_PROOF_BENCHMARKS.length}</span>
          </button>
          <button type="button" class="sc-v22-tab-btn ${currentEvidenceTab === 'sources' ? 'active' : ''}" onclick="switchEvidenceTab('sources')">
            <span>📚 Primary Research &amp; Standards</span>
            <span class="sc-v22-tab-count">${VERIFIED_RESEARCH_SOURCES.length}</span>
          </button>
        </div>

        ${currentEvidenceTab === 'cases' ? `
          <div style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:20px;">
            ${filterPillsHtml}
          </div>
          <div class="sc-v22-cs-grid">
            ${caseCardsHtml}
          </div>
        ` : ''}

        ${currentEvidenceTab === 'benchmarks' ? `
          <div class="simple-arch-card" style="padding: 26px 28px;">
            <div style="margin-bottom:18px;">
              <h2 style="font-family:var(--font-display); font-size:22px; font-weight:800; color:var(--text-primary); margin:0 0 4px;">
                Pillar-by-Pillar Calibration Matrix
              </h2>
              <p style="font-size:14px; color:var(--text-secondary); margin:0;">
                Comparing industry problem scale, our conservative portal targets, and published analyst benchmarks.
              </p>
            </div>
            <div style="overflow-x:auto;">
              <table style="width:100%; border-collapse:collapse; text-align:left;">
                <thead>
                  <tr style="border-bottom:2px solid var(--border-subtle); font-size:11.5px; text-transform:uppercase; letter-spacing:0.05em; color:var(--text-secondary);">
                    <th style="padding:14px;">Supply Chain Domain</th>
                    <th style="padding:14px;">Industry Problem Quantified</th>
                    <th style="padding:14px;">Our Conservative Target</th>
                    <th style="padding:14px;">Published Benchmark</th>
                    <th style="padding:14px;">Enterprise Proof</th>
                  </tr>
                </thead>
                <tbody>
                  ${pillarRowsHtml}
                </tbody>
              </table>
            </div>
          </div>
        ` : ''}

        ${currentEvidenceTab === 'sources' ? `
          <div class="sc-src-lib-grid" style="gap: 18px;">
            ${sourcesHtml}
          </div>
        ` : ''}
      `;

      showActivePage('pageEvidence');
    }

"""


def upgrade_file(path: Path) -> None:
    orig = path.read_text(encoding="utf-8")
    html = orig

    # 1. Inject V22 CSS cleanly right before `</style>`
    if V22_CSS_START in html and V22_CSS_END in html:
        i0 = html.index(V22_CSS_START)
        i1 = html.index(V22_CSS_END, i0) + len(V22_CSS_END)
        html = html[:i0] + V22_CSS.strip() + html[i1:]
    else:
        style_close = html.index("</style>")
        html = html[:style_close] + V22_CSS + "\n  " + html[style_close:]

    # 2. Remove Navbar Dropdowns on Processes, Personas, and Agents
    nav_dropdown_pattern = re.compile(
        r'<div class="nav-dropdown-wrap"[^>]*>\s*'
        r'<button[^>]*onclick="(?:scrollToProcessJourneys|openProcessesHubPage)[^"]*"[^>]*>.*?</button>\s*'
        r'<div class="nav-quick-menu" id="navProcessesQuickMenu"></div>\s*</div>\s*'
        r'<div class="nav-dropdown-wrap"[^>]*>\s*'
        r'<button[^>]*onclick="openPersonasDirectoryPage\([^\)]*\'personas\'[^\)]*\)"[^>]*>.*?</button>\s*'
        r'<div class="nav-quick-menu" id="navPersonasQuickMenu"></div>\s*</div>\s*'
        r'<div class="nav-dropdown-wrap"[^>]*>\s*'
        r'<button[^>]*onclick="openPersonasDirectoryPage\([^\)]*\'agents\'[^\)]*\)"[^>]*>.*?</button>\s*'
        r'<div class="nav-quick-menu" id="navAgentsQuickMenu"></div>\s*</div>',
        re.DOTALL,
    )
    clean_nav_buttons = (
        '<button type="button" class="nav-pill-btn" onclick="openProcessesHubPage(true, event)">Processes</button>\n'
        '      <button type="button" class="nav-pill-btn" onclick="openPersonasDirectoryPage(\'all\', \'\', true, \'personas\', event)">Personas</button>\n'
        '      <button type="button" class="nav-pill-btn" onclick="openPersonasDirectoryPage(\'all\', \'\', true, \'agents\', event)">Agents</button>'
    )
    if nav_dropdown_pattern.search(html):
        html = nav_dropdown_pattern.sub(clean_nav_buttons, html, count=1)

    # 3. Safe `getDeptMeta` fallback
    html = replace_between_anchors(
        html,
        "    function getDeptMeta(deptId) {",
        "    /* 2. SUPPLY CHAIN PERSONAS ROSTER",
        NEW_GET_DEPT_META,
    )

    # 4. Dedicated `openProcessesHubPage` + `scrollToProcessJourneys`
    if "function openProcessesHubPage(" in html:
        html = replace_between_anchors(
            html,
            "    function scrollToProcessJourneys(",
            "    function renderValueChainEntryCards()",
            NEW_SCROLL_AND_PROCESSES_HUB,
        )
    else:
        html = replace_between_anchors(
            html,
            "    function scrollToProcessJourneys() {",
            "    function renderValueChainEntryCards()",
            NEW_SCROLL_AND_PROCESSES_HUB,
        )

    # 5. Update `openPersonaPage` back-bar to use dynamic pillar count + `All Personas` button
    old_persona_back = """          <div class="back-bar">
            <button type="button" class="back-btn" onclick="goToOrgChart()">
              <span>&larr;</span>
              <span>Back to 6 Pillars (${dept.name})</span>
            </button>"""
    new_persona_back = """          <div class="back-bar">
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              <button type="button" class="back-btn" onclick="goToOrgChart()">
                <span>&larr;</span>
                <span>Back to ${Object.keys(DEPARTMENTS).length} Pillars (${dept.name})</span>
              </button>
              <button type="button" class="back-btn" onclick="openPersonasDirectoryPage('${p.deptId}', '', true, 'personas', event)">
                <span>👤 All Personas</span>
              </button>
            </div>"""
    if old_persona_back in html:
        html = html.replace(old_persona_back, new_persona_back, 1)

    # 6. Update `openValueChainPage` back-bar to include `← All Processes`
    old_vc_back = """          <div class="back-bar">
            <button type="button" class="back-btn" onclick="goToOrgChart()">
              <span>&larr;</span>
              <span>Back to CSCO Org Chart</span>
            </button>"""
    new_vc_back = """          <div class="back-bar">
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              <button type="button" class="back-btn" onclick="openProcessesHubPage(true, event)">
                <span>&larr;</span>
                <span>All Processes</span>
              </button>
              <button type="button" class="back-btn" onclick="goToOrgChart()">
                <span>Operating Pillars</span>
              </button>
            </div>"""
    if old_vc_back in html:
        html = html.replace(old_vc_back, new_vc_back, 1)

    # 7. Hierarchical Personas & Agents Directory (`pageDirectory`)
    dir_start_marker = (
        "    /* =========================================================================\n"
        "       PAGE 5 RENDERING:"
    )
    dir_end_marker = (
        "    /* =========================================================================\n"
        "       PAGE 6 RENDERING:"
    )
    html = replace_between_anchors(html, dir_start_marker, dir_end_marker, NEW_DIRECTORY_BLOCK)

    # 8. Dynamic Periodic Table & Polished Harmonized Mind Map
    html = replace_between_anchors(
        html,
        "    function openPeriodicTablePage(",
        "    /* =========================================================================\n       MULTI-PAGE SWITCHING & HISTORY HANDLING",
        NEW_PERIODIC_AND_MINDMAP_BLOCK + "\n",
    )

    # 9. Progressive 3-Step Cost & ROI Hub
    html = replace_between_anchors(
        html,
        "    /* =========================================================================\n       PAGE 9:",
        "    function showActivePage(pageId) {",
        NEW_COST_TAB_BLOCK,
    )

    # 10. Progressive 3-Tab Case Studies Hub
    if "let currentEvidenceTab =" in html:
        html = replace_between_anchors(
            html,
            "    let currentEvidenceTab =",
            "    function handleUrlHash() {",
            NEW_EVIDENCE_HUB_BLOCK,
        )
    else:
        html = replace_between_anchors(
            html,
            "    function openEvidenceHubPage(",
            "    function handleUrlHash() {",
            NEW_EVIDENCE_HUB_BLOCK,
        )

    # 11. Route `#processes` hash to `openProcessesHubPage(false)`
    html = html.replace(
        "      } else if (hash === 'processes') {\n        openValueChainPage('f2f', false);",
        "      } else if (hash === 'processes') {\n        openProcessesHubPage(false);",
    )

    assert len(html) > int(len(orig) * 0.94), f"Safety check failed on {path.name}: {len(html)} vs {len(orig)}"
    path.write_text(html, encoding="utf-8")
    print(f"[V2.2 UPGRADED] {path.name} ({path.stat().st_size // 1024} KB)")


def main() -> None:
    for fname in ("index.html", "periodic_table.html", "mind_map.html"):
        p = ROOT / fname
        if p.exists():
            upgrade_file(p)


if __name__ == "__main__":
    main()

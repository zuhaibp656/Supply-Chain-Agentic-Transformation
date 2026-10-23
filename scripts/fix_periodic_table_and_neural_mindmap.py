#!/usr/bin/env python3
"""
Fixes the Periodic Table (`getAgentSellingMeta` restoration + clean Sub-Pillar Periodic Grid)
and redesigns the Neural Mind Map (`#mindmap` / `mind_map.html`) to:
  1. Fill the full page width & height generously (no cramped small columns).
  2. Follow the exact neural hierarchy:
     Column 1: Core Domains / Pillars (6)
     Column 2: Sub-Pillars ONLY (3-4 per Pillar — no Personas mixed into Column 2)
     Column 3: AI Agents in Selected Sub-Pillar (3 Agents) -> Expanding an Agent reveals its Human Persona & action links.
"""

import re
from pathlib import Path

ROOT = Path("/usr/local/google/home/zuhaibp/Supply_chain_Agentic_Transformation")
HTML_FILES = [
    ROOT / "index.html",
    ROOT / "periodic_table.html",
    ROOT / "mind_map.html",
]

EXTRA_CSS = """
    /* =========================================================================
       CLEAN PERIODIC TABLE & FULL-SCREEN NEURAL MIND MAP OVERRIDES
       ========================================================================= */
    #pagePeriodic .subpage-container,
    #pageMindMap .subpage-container {
      max-width: 1820px !important;
      width: 95vw !important;
    }

    /* Clean Sub-Pillar Periodic Table Grid inside each Pillar Section */
    .pt-pillar-card {
      margin-bottom: 24px;
      padding: 20px 22px;
      border-radius: 18px;
      background: rgba(11, 17, 30, 0.82);
      border: 1px solid rgba(148, 163, 184, 0.18);
      border-left: 5px solid var(--dom-color, #38bdf8);
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.28);
    }
    html[data-theme="light"] .pt-pillar-card {
      background: #ffffff;
      border-color: rgba(15, 23, 42, 0.12);
      box-shadow: 0 10px 26px rgba(15, 23, 42, 0.06);
    }

    .pt-subpillars-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
      margin-top: 12px;
    }

    .pt-subpillar-group {
      padding: 14px 14px 12px;
      border-radius: 14px;
      background: rgba(15, 23, 42, 0.65);
      border: 1px solid rgba(148, 163, 184, 0.16);
      border-top: 3px solid var(--sp-color, #38bdf8);
    }
    html[data-theme="light"] .pt-subpillar-group {
      background: #f8fafc;
      border-color: rgba(15, 23, 42, 0.1);
    }

    .pt-subpillar-title {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      font-family: var(--font-display);
      font-size: 13.5px;
      font-weight: 800;
      color: var(--text-primary);
      margin-bottom: 10px;
      padding-bottom: 7px;
      border-bottom: 1px solid rgba(148, 163, 184, 0.14);
    }

    .pt-subpillar-tiles {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
    }

    .pt-tile {
      height: 98px !important;
      padding: 10px 10px 8px !important;
    }

    .pt-tile-sym {
      font-family: var(--font-display);
      font-size: 18px;
      font-weight: 800;
      color: var(--tile-color, #38bdf8);
      line-height: 1.05;
      letter-spacing: -0.02em;
    }

    /* Full-Viewport Neural Mind Map Canvas (Domains -> Sub-Pillars -> Agents -> Expanded Persona) */
    .mm-neural-board {
      position: relative;
      display: grid;
      grid-template-columns: 330px 48px 340px 48px minmax(460px, 1fr);
      gap: 0;
      align-items: stretch;
      min-height: 74vh;
      padding: 26px;
      border-radius: 24px;
      background:
        radial-gradient(circle at 18% 22%, rgba(37, 99, 235, 0.12), transparent 42%),
        radial-gradient(circle at 52% 50%, rgba(124, 58, 237, 0.10), transparent 45%),
        radial-gradient(circle at 86% 30%, rgba(16, 185, 129, 0.12), transparent 45%),
        rgba(8, 13, 24, 0.92);
      border: 1px solid rgba(148, 163, 184, 0.22);
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.45);
      margin-bottom: 32px;
    }
    html[data-theme="light"] .mm-neural-board {
      background:
        radial-gradient(circle at 18% 22%, rgba(37, 99, 235, 0.06), transparent 42%),
        radial-gradient(circle at 86% 30%, rgba(16, 185, 129, 0.06), transparent 45%),
        #ffffff;
      border-color: rgba(15, 23, 42, 0.14);
      box-shadow: 0 18px 44px rgba(15, 23, 42, 0.07);
    }

    @media (max-width: 1260px) {
      .mm-neural-board {
        grid-template-columns: 1fr;
        gap: 20px;
      }
      .mm-synapse-bridge {
        display: none !important;
      }
    }

    .mm-neural-col {
      display: flex;
      flex-direction: column;
      background: rgba(15, 23, 42, 0.76);
      border: 1px solid rgba(148, 163, 184, 0.2);
      border-radius: 18px;
      padding: 20px 18px;
      position: relative;
      z-index: 2;
    }
    html[data-theme="light"] .mm-neural-col {
      background: #f8fafc;
      border-color: rgba(15, 23, 42, 0.12);
    }

    .mm-neural-col-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding-bottom: 14px;
      margin-bottom: 16px;
      border-bottom: 1px solid rgba(148, 163, 184, 0.18);
    }

    .mm-neural-step-pill {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 4px 10px;
      border-radius: 999px;
      background: rgba(56, 189, 248, 0.14);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.35);
    }
    html[data-theme="light"] .mm-neural-step-pill {
      background: rgba(37, 99, 235, 0.1);
      color: #1d4ed8;
      border-color: rgba(37, 99, 235, 0.3);
    }

    .mm-synapse-bridge {
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      z-index: 1;
    }

    .mm-pillar-node,
    .mm-subpillar-node {
      width: 100%;
      padding: 16px 18px;
      border-radius: 14px;
      background: rgba(17, 25, 42, 0.88);
      border: 1.5px solid rgba(148, 163, 184, 0.18);
      border-left: 5px solid var(--node-color, #38bdf8);
      text-align: left;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 12px;
      cursor: pointer;
      transition: all 0.25s var(--ease-spring);
    }
    html[data-theme="light"] .mm-pillar-node,
    html[data-theme="light"] .mm-subpillar-node {
      background: #ffffff;
      border-color: rgba(15, 23, 42, 0.12);
    }

    .mm-pillar-node:hover,
    .mm-subpillar-node:hover {
      transform: translateX(4px);
      border-color: var(--node-color, #38bdf8);
      box-shadow: 0 10px 24px rgba(0, 0, 0, 0.3);
    }

    .mm-pillar-node.active,
    .mm-subpillar-node.active {
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.98), rgba(15, 23, 42, 0.96));
      border-color: var(--node-color, #38bdf8);
      box-shadow: 0 0 0 2px var(--node-color, #38bdf8), 0 12px 28px rgba(0, 0, 0, 0.45);
      transform: translateX(5px);
    }
    html[data-theme="light"] .mm-pillar-node.active,
    html[data-theme="light"] .mm-subpillar-node.active {
      background: #ffffff;
      box-shadow: 0 0 0 2px var(--node-color, #38bdf8), 0 12px 26px rgba(15, 23, 42, 0.12);
    }

    /* Column 3: Agent Neural Accordion Node (Expands to reveal Human Persona!) */
    .mm-agent-neural-card {
      border-radius: 16px;
      background: rgba(17, 25, 42, 0.9);
      border: 1.5px solid rgba(148, 163, 184, 0.2);
      border-left: 5px solid var(--ag-color, #6366f1);
      margin-bottom: 14px;
      overflow: hidden;
      transition: all 0.28s var(--ease-spring);
    }
    html[data-theme="light"] .mm-agent-neural-card {
      background: #ffffff;
      border-color: rgba(15, 23, 42, 0.12);
    }

    .mm-agent-neural-card.expanded {
      border-color: var(--ag-color, #6366f1);
      box-shadow: 0 14px 36px rgba(0, 0, 0, 0.42);
    }
    html[data-theme="light"] .mm-agent-neural-card.expanded {
      box-shadow: 0 14px 32px rgba(15, 23, 42, 0.1);
    }

    .mm-agent-neural-header {
      width: 100%;
      padding: 18px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      text-align: left;
      cursor: pointer;
      background: transparent;
      border: none;
      color: inherit;
    }

    .mm-agent-neural-body {
      display: none;
      padding: 0 20px 20px;
      border-top: 1px solid rgba(148, 163, 184, 0.15);
      animation: ptExpandIn 0.26s var(--ease-spring) forwards;
    }

    .mm-agent-neural-card.expanded .mm-agent-neural-body {
      display: block;
    }

    .mm-expanded-persona-box {
      margin-top: 16px;
      padding: 18px 20px;
      border-radius: 14px;
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.10), rgba(15, 23, 42, 0.85));
      border: 1.5px solid rgba(245, 158, 11, 0.42);
      border-left: 6px solid #f59e0b;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 16px;
    }
    html[data-theme="light"] .mm-expanded-persona-box {
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.08), #fffbeb);
      border-color: rgba(217, 119, 6, 0.4);
    }
"""

NEW_SELLING_META_AND_PERIODIC_AND_MINDMAP_JS = r"""    /* =========================================================================
       EXECUTIVE SELLING METADATA HELPER FOR ALL 60 AGENTS
       ========================================================================= */
    function getAgentSellingMeta(ag, dept) {
      const d = dept || (ag && DEPARTMENTS[ag.deptId]) || Object.values(DEPARTMENTS)[0] || { id: 'demand_sop', name: 'Planning & Strategy', color: '#2563eb' };
      const isHighCodeSolver = /OR-Tools|MILP|CP-SAT|3D|LIFO|ULD|CVRPTW|Finite|Kalman|Isolation|Vision|Spanner/i.test((ag && ag.solverStack) || '');
      const buildType = (ag && ag.buildType) || (isHighCodeSolver
        ? 'High-Code ADK + OR-Tools + Spanner/BigQuery'
        : 'Gemini Enterprise + Vertex AI + BigQuery');

      let usedByPersonas = [];
      if (ag) {
        const direct = Object.values(PERSONAS).filter(p => (p.agentIds || []).includes(ag.id));
        const primary = ag.personaId && PERSONAS[ag.personaId] ? [PERSONAS[ag.personaId]] : [];
        const sameSubPillar = Object.values(PERSONAS).filter(p => ag.subPillarId && p.subPillarId === ag.subPillarId);
        const seen = new Set();
        [...primary, ...direct, ...sameSubPillar].forEach(p => {
          if (p && !seen.has(p.id)) {
            seen.add(p.id);
            usedByPersonas.push(p);
          }
        });
      }
      if (usedByPersonas.length === 0 && d && d.personaIds) {
        usedByPersonas = d.personaIds.slice(0, 3).map(pid => PERSONAS[pid]).filter(Boolean);
      }

      const primaryPersona = usedByPersonas[0];
      const roiMetrics = (ag && ag.roiMetrics) || [
        {
          val: (ag && ag.badge) || '+24% Lift',
          label: 'Quantifiable KPI Improvement',
          sub: `Verified across ${d.name} workflows`,
          color: d.color || '#2563eb'
        },
        {
          val: primaryPersona ? `${(primaryPersona.toilHoursBefore || '6.5h').split(' ')[0]} → ${(primaryPersona.toilHoursAfter || '1.0h').split(' ')[0]}h` : '-85% Effort',
          label: 'Daily Team Effort & Time Saved',
          sub: primaryPersona ? `${primaryPersona.name} daily manual toil cut by ~85%` : 'Automated exception triage & ERP write-back',
          color: '#10b981'
        },
        {
          val: '$15M+ Value',
          label: 'Annual Working Capital & Cost Impact',
          sub: 'Replaces manual spreadsheet handoffs with autonomous execution',
          color: '#38bdf8'
        },
        {
          val: 'Days → 90s',
          label: 'Decision & Execution Speed',
          sub: 'Real-time BigQuery + Cloud Spanner twin to 1-click ERP write-back',
          color: '#f59e0b'
        }
      ];

      const gcpStack = [
        { name: 'BigQuery & BigQuery ML / GIS', role: 'Canonical Supply Chain Digital Twin, spatiotemporal GIS & bayesian ML' },
        { name: 'Cloud Spanner & Spanner Graph', role: 'Multi-tier BOM graph, global ATP inventory ledger & multi-modal network state' },
        { name: 'AlloyDB for PostgreSQL + pgvector', role: 'Sub-millisecond operational state store, contract/tariff vector RAG & agent memory' },
        { name: 'Vertex AI Agent Engine (ADK & A2A)', role: 'Managed runtime orchestrating root supervisor & 3 collaborating A2A sub-agents' },
        { name: 'Gemini 3.1 Pro & Gemini 3.8 Flash', role: 'Multimodal reasoning, COA/contract vision parsing & conversational analytics' },
        { name: 'Google OR-Tools (CP-SAT / CVRPTW / MILP)', role: '100% deterministic finite scheduling, multi-modal routing & 3D LIFO/ULD bin-packing' }
      ];

      return {
        roiMetrics,
        customerProof: (ag && ag.customerProof) || `Verified across global ${d.name} deployments on Vertex AI Agent Engine & BigQuery.`,
        buildType,
        gcpStack,
        enterpriseConnectors: toSysArray(ag ? ag.systems : []),
        dataSegments: {
          privateData: 'SAP S/4HANA, SAP IBP, Oracle ERP, Manhattan Active WMS, Blue Yonder TMS in BigQuery & Spanner',
          communityData: 'Supplier & Carrier Portals, EDI 850/856/214/315, Spire AIS, FlightAware ADS-B, Project44',
          publicData: 'Google DeepMind WeatherNext 3, Google Maps Live Traffic, Global Commodity & Tariff Indices'
        },
        usedByPersonas
      };
    }

    let currentPeriodicFilter = 'all'; // 'all' | group.id
    let currentSelectedElementId = 'demand_sensing_agent';
    let currentExpandedInlineId = null;

    function handlePeriodicTileClick(agentId) {
      currentSelectedElementId = agentId;
      if (currentExpandedInlineId === agentId) {
        currentExpandedInlineId = null;
      } else {
        currentExpandedInlineId = agentId;
      }
      openPeriodicTablePage(currentPeriodicFilter, currentSelectedElementId, false);
    }

    function openPeriodicTablePage(filterGroup = 'all', selectedAgentId = null, pushState = true) {
      currentPeriodicFilter = filterGroup || 'all';
      if (selectedAgentId && AGENTS[selectedAgentId]) {
        currentSelectedElementId = selectedAgentId;
      }
      if (pushState) {
        history.pushState({ page: 'periodic', filter: currentPeriodicFilter, agentId: currentSelectedElementId }, '', '#periodic');
      }

      const selAg = AGENTS[currentSelectedElementId] || Object.values(AGENTS)[0];
      const selMeta = PERIODIC_AGENT_META[selAg.id] || {
        code: '101', sym: 'Ai', short: selAg.name, group: selAg.deptId,
        layer: 'Vertex AI ADK + A2A', layerColor: '#3b82f6', trigger: 'Event-Driven', trigIcon: '⚡'
      };
      const selGrp = PERIODIC_GROUPS.find(g => g.id === selMeta.group) || PERIODIC_GROUPS[0];
      const selDept = DEPARTMENTS[selAg.deptId] || Object.values(DEPARTMENTS)[0];
      const selSell = getAgentSellingMeta(selAg, selDept);
      const selCls = getAgentBuildClassification(selAg);
      const selPrimaryPersona = (selAg.personaId && PERSONAS[selAg.personaId]) || selSell.usedByPersonas[0] || Object.values(PERSONAS)[0];

      const renderInlineExpansionCard = (ag, meta, grpColor) => {
        const d = DEPARTMENTS[ag.deptId] || selDept;
        const cls = getAgentBuildClassification(ag);
        const pOwner = (ag.personaId && PERSONAS[ag.personaId]) || getAgentSellingMeta(ag, d).usedByPersonas[0];
        return `
          <div class="pt-inline-expand" style="--exp-color:${grpColor};">
            <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:16px; padding-bottom:14px; border-bottom:1px solid var(--border-subtle); margin-bottom:16px;">
              <div>
                <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:6px;">
                  <span style="font-family:var(--font-mono); font-size:12px; font-weight:800; padding:3px 9px; border-radius:6px; background:${grpColor}22; border:1px solid ${grpColor}; color:var(--text-primary);">
                    A-${meta.code} · ${meta.sym}
                  </span>
                  <span class="build-tier-badge ${cls.cssClass}">${cls.label}</span>
                  <span class="pt-side-tag">${meta.trigIcon} ${meta.trigger}</span>
                  <span class="pt-side-tag" style="color:#10b981; border-color:rgba(16,185,129,0.4); font-weight:800;">✦ ${ag.badge}</span>
                </div>
                <h3 style="font-family:var(--font-display); font-size:22px; font-weight:800; color:var(--text-primary); margin-bottom:2px;">
                  ${ag.name}
                </h3>
                <div style="font-size:13.5px; color:var(--text-secondary);">
                  ${d.scorBadge} · <strong>${ag.subPillarName || meta.subPillar || d.name}</strong>
                </div>
              </div>
              <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                ${pOwner ? `
                  <button type="button" class="switch-pill" style="border-color:#f59e0b; color:#f59e0b; font-weight:700;" onclick="openPersonaPage('${pOwner.id}', true, event)">
                    👤 ${pOwner.name} &rarr;
                  </button>
                ` : ''}
                <button type="button" class="agent-plug-btn" style="padding:9px 16px; font-size:13px;" onclick="openAgentPage('${ag.id}', true, event)">
                  <span>Open ${ag.name} Studio</span>
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
                <p style="font-size:13.5px; color:var(--text-primary); line-height:1.55; margin:0;">${shortSentence(ag.problem, 180)}</p>
              </div>
              <div style="padding:14px 16px; border-radius:12px; background:rgba(59,130,246,0.06); border:1px solid rgba(59,130,246,0.22);">
                <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.07em; color:#3b82f6; margin-bottom:4px;">
                  ✦ AI Agent Solution
                </div>
                <p style="font-size:13.5px; color:var(--text-primary); line-height:1.55; margin:0;">${shortSentence(ag.solution, 180)}</p>
              </div>
              <div style="padding:14px 16px; border-radius:12px; background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.22);">
                <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.07em; color:#10b981; margin-bottom:4px;">
                  ⚡ Quantified Outcome
                </div>
                <p style="font-size:13.5px; color:var(--text-primary); line-height:1.55; margin:0;">${shortSentence(ag.outcome, 180)}</p>
              </div>
            </div>
          </div>
        `;
      };

      const visibleGroups = PERIODIC_GROUPS.filter(g => currentPeriodicFilter === 'all' || g.id === currentPeriodicFilter);
      const leftColumnHtml = visibleGroups.map(grp => {
        const deptObj = DEPARTMENTS[grp.id];
        const subPillars = (deptObj && deptObj.subPillars) || [];
        const grpAgents = Object.entries(PERIODIC_AGENT_META)
          .filter(([_, m]) => m.group === grp.id)
          .map(([aid, m]) => ({ ag: AGENTS[aid], m }))
          .filter(x => x.ag);
        const expandedItem = grpAgents.find(x => x.ag.id === currentExpandedInlineId);

        return `
          <div class="pt-pillar-card" style="--dom-color:${grp.color};">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom:8px;">
              <div style="display:flex; align-items:center; gap:10px;">
                <span class="pt-domain-swatch" style="--dom-color:${grp.color}; width:12px; height:12px; border-radius:3px;"></span>
                <span style="font-family:var(--font-display); font-size:16px; font-weight:800; color:var(--text-primary); letter-spacing:0.02em;">
                  ${grp.title}
                </span>
              </div>
              <span style="font-family:var(--font-mono); font-size:12px; font-weight:700; color:${grp.color}; padding:3px 10px; border-radius:999px; background:${grp.color}18; border:1px solid ${grp.color}40;">
                ${subPillars.length} Sub-Pillars · ${grpAgents.length} AI Agents
              </span>
            </div>

            <div class="pt-subpillars-grid">
              ${subPillars.map(sp => {
                const spItems = (sp.items || []).map(it => {
                  const ag = AGENTS[it.agentId];
                  const m = PERIODIC_AGENT_META[it.agentId] || { code: '101', sym: 'Ai', short: it.agentName, layerColor: sp.color, trigIcon: '⚡', layer: 'Vertex AI ADK', trigger: 'Event-Driven' };
                  return { ag, m, it };
                }).filter(x => x.ag);

                return `
                  <div class="pt-subpillar-group" style="--sp-color:${sp.color || grp.color};">
                    <div class="pt-subpillar-title">
                      <span>${sp.icon} ${sp.name}</span>
                      <span style="font-family:var(--font-mono); font-size:11px; color:${sp.color || grp.color};">3</span>
                    </div>
                    <div class="pt-subpillar-tiles">
                      ${spItems.map(({ ag, m }) => {
                        const isSel = ag.id === selAg.id;
                        return `
                          <div class="pt-tile ${isSel ? 'active' : ''}"
                               style="--tile-color:${sp.color || grp.color}; --dot-color:${m.layerColor};"
                               onclick="handlePeriodicTileClick('${ag.id}')">
                            <div class="pt-tile-top">
                              <span>${m.code}</span>
                              <span class="pt-tile-trig" title="${m.trigger}">${m.trigIcon}</span>
                            </div>
                            <div class="pt-tile-sym">${m.sym}</div>
                            <div class="pt-tile-title" title="${ag.name}">${m.short}</div>
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
          <button type="button" class="back-btn" onclick="goHome()">
            <span>&larr;</span>
            <span>Back to 6 Pillars</span>
          </button>
          <div style="display:flex; flex-wrap:wrap; gap:10px; align-items:center;">
            <button type="button" class="switch-pill" style="border-color:rgba(16,185,129,0.45); color:#10b981; font-weight:700;" onclick="openMindMapPage('mindmap', null, null, true)">
              🧠 Switch to Neural Mind Map &rarr;
            </button>
          </div>
        </div>

        <!-- Clean Header -->
        <div style="display:flex; flex-wrap:wrap; align-items:flex-end; justify-content:space-between; gap:16px; padding-bottom: 16px; border-bottom: 1px solid var(--border-subtle); margin-bottom: 18px;">
          <div>
            <h1 style="font-family:var(--font-display); font-size:clamp(28px, 3vw, 40px); font-weight:800; letter-spacing:-0.025em; color:var(--text-primary); margin-bottom:4px;">
              The Periodic Table of Supply Chain AI Agents
            </h1>
            <p style="font-size:14.5px; color:var(--text-secondary); margin:0;">
              <strong>6 Core Pillars</strong> &rarr; <strong>20 Sub-Pillars</strong> &rarr; <strong>60 AI Agents</strong> (3 per Sub-Pillar). Click any element tile to inspect its Persona and launch the Agent Studio.
            </p>
          </div>
          <div class="pt-stat-badges">
            <div class="pt-stat-badge"><strong>6</strong>pillars</div>
            <div class="pt-stat-badge"><strong>20</strong>sub-pillars</div>
            <div class="pt-stat-badge"><strong>60</strong>agents</div>
          </div>
        </div>

        <!-- Clean Pillar Filter Tabs -->
        <div class="pt-top-tabs" style="margin-bottom:20px;">
          <button type="button" class="pt-tab-btn ${currentPeriodicFilter === 'all' ? 'active' : ''}"
                  onclick="currentExpandedInlineId = null; openPeriodicTablePage('all', '${selAg.id}', false)">
            <span>All 6 Pillars</span>
            <span class="pt-tab-count">60</span>
          </button>
          ${PERIODIC_GROUPS.map(g => `
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
                    ELEMENT A-${selMeta.code} · ${selAg.subPillarName || selMeta.subPillar || selGrp.shortTab}
                  </div>
                  <div style="font-family:var(--font-display); font-size:18px; font-weight:800; color:var(--text-primary); line-height:1.25; margin-top:2px;">
                    ${selAg.name}
                  </div>
                </div>
              </div>

              <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:14px;">
                <span class="build-tier-badge ${selCls.cssClass}">${selCls.tier}</span>
                <span class="pt-side-tag">${selMeta.trigIcon} ${selMeta.trigger}</span>
                <span class="pt-side-tag" style="color:#10b981; border-color:rgba(16,185,129,0.35); font-weight:800;">✦ ${selAg.badge}</span>
              </div>

              <p style="font-size:13.5px; color:var(--text-secondary); line-height:1.58; margin-bottom:16px;">
                ${shortSentence(selAg.solution || selAg.shortDesc, 165)}
              </p>

              <!-- Primary Human Persona Box inside Inspector -->
              ${selPrimaryPersona ? `
                <div style="padding:12px 14px; border-radius:12px; background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.35); border-left:4px solid #f59e0b; margin-bottom:16px;">
                  <div style="font-family:var(--font-mono); font-size:10.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:#f59e0b; margin-bottom:4px;">
                    👤 Human Persona in the Loop
                  </div>
                  <div style="display:flex; align-items:center; justify-content:space-between; gap:8px;">
                    <div style="font-size:14px; font-weight:800; color:var(--text-primary);">
                      ${selPrimaryPersona.icon} ${selPrimaryPersona.name}
                    </div>
                    <button type="button" style="font-size:12px; font-weight:700; color:#f59e0b; background:none; border:none; cursor:pointer;" onclick="openPersonaPage('${selPrimaryPersona.id}', true, event)">
                      Journey &rarr;
                    </button>
                  </div>
                </div>
              ` : ''}

              <div style="display:flex; flex-direction:column; gap:10px; padding-top:12px; border-top:1px solid var(--border-subtle);">
                <button type="button" class="agent-plug-btn" style="width:100%; justify-content:center; padding:10px 14px; font-size:13px;" onclick="openAgentPage('${selAg.id}', true, event)">
                  <span>Open ${selAg.name} Studio</span>
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
       PAGE 8: FULL-SCREEN NEURAL MIND MAP (DOMAINS -> SUB-PILLARS -> AGENTS -> EXPANDED PERSONA)
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
      if (deptId && DEPARTMENTS[deptId]) {
        currentMindMapDeptId = deptId;
        const d = DEPARTMENTS[deptId];
        if (d.subPillars && !d.subPillars.some(s => s.id === currentMindMapSubPillarId)) {
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
          for (const d of Object.values(DEPARTMENTS)) {
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

      const activeDept = DEPARTMENTS[currentMindMapDeptId] || Object.values(DEPARTMENTS)[0];
      const deptSubPillars = activeDept.subPillars || [];
      const activeSubPillar = deptSubPillars.find(s => s.id === currentMindMapSubPillarId) || deptSubPillars[0];
      const subPillarItems = (activeSubPillar && activeSubPillar.items) || [];

      const flowSteps = [
        {
          num: '01',
          title: 'Full-Screen Hero Landing (#)',
          sub: '60fps Supply Chain Canvas & Thesis',
          color: '#1a73e8',
          whatOpens: '60fps kinetic supply chain canvas introducing the CSCO executive transformation thesis.',
          actionLabel: 'Open Hero Landing &rarr;',
          actionFn: "goHome()"
        },
        {
          num: '02',
          title: '6 Core Operating Pillars (#orgChart)',
          sub: 'Click Any Pillar to Reveal Its 3–4 Clean Sub-Pillar Boxes',
          color: '#2e8b57',
          whatOpens: 'Interactive 6-Pillar board where clicking a Pillar cleanly shows only its 3 or 4 functional Sub-Pillar boxes.',
          actionLabel: 'Open 6 Pillars &rarr;',
          actionFn: "goToOrgChart()"
        },
        {
          num: '03',
          title: 'Sub-Pillar Persona Dropdown',
          sub: 'Click a Sub-Pillar Box to Drop Down Its 3 Human Personas',
          color: '#7e57c2',
          whatOpens: 'Smoothly animates open the 3 Human Personas for that Sub-Pillar without cluttering the screen.',
          actionLabel: 'Try on Front Page &rarr;',
          actionFn: "goToOrgChart()"
        },
        {
          num: '04',
          title: 'Dedicated Persona Page (#persona/id)',
          sub: '60 Supply Chain Roles · Daily Journey & AI Agents',
          color: '#00897b',
          whatOpens: 'Click-to-expand Daily Journey comparing Manual Bottleneck (Red) vs. With Gemini AI (Green) and assigned AI Agents.',
          actionLabel: 'Open Sample Persona Page &rarr;',
          actionFn: "openPersonaPage('demand_planner_forecaster', true, event)"
        },
        {
          num: '05',
          title: 'Executive Agent Studio (#agent/id)',
          sub: '60 AI Agents · ROI Cards, Architecture & Interactive Demo',
          color: '#d97706',
          whatOpens: 'Executive business case with verified ROI metrics, branching workflow diagram, and interactive CAD/Video simulator.',
          actionLabel: 'Open Sample Agent Studio &rarr;',
          actionFn: "openAgentPage('demand_sensing_agent', true, event)"
        },
        {
          num: '06',
          title: 'High-Code Technical Blueprint (#blueprint/id)',
          sub: '5-Stage ADK Pipeline, 3 Sub-Agents & Solvers',
          color: '#c53929',
          whatOpens: 'High-code ADK pipeline specification, A2A agent mesh, ERP write-back schemas, and solver constraints.',
          actionLabel: 'Open Sample Blueprint &rarr;',
          actionFn: "openAgentBlueprintPage('demand_sensing_agent', true, event)"
        }
      ];

      const container = document.getElementById('mindMapPageContent');
      container.innerHTML = `
        <div class="subpage-top-bar">
          <button type="button" class="back-btn" onclick="goHome()">
            <span>&larr;</span>
            <span>Back to 6 Pillars</span>
          </button>
          <div style="display:flex; flex-wrap:wrap; gap:10px; align-items:center;">
            <button type="button" class="switch-pill" style="border-color:rgba(0,210,255,0.45); color:var(--g-blue); font-weight:700;" onclick="openPeriodicTablePage('all', null, true)">
              🧪 Switch to Periodic Table &rarr;
            </button>
          </div>
        </div>

        <!-- Clean, Full-Width Header -->
        <div style="display:flex; flex-wrap:wrap; align-items:flex-end; justify-content:space-between; gap:16px; padding-bottom: 16px; border-bottom: 1px solid var(--border-subtle); margin-bottom: 18px;">
          <div>
            <h1 style="font-family:var(--font-display); font-size:clamp(30px, 3.2vw, 42px); font-weight:800; letter-spacing:-0.025em; color:var(--text-primary); margin-bottom:4px;">
              Interactive Neural Mind Map
            </h1>
            <p style="font-size:15px; color:var(--text-secondary); margin:0;">
              <strong>1. Core Pillars (6)</strong> &rarr; <strong>2. Sub-Pillars (20)</strong> &rarr; <strong>3. AI Agents (60)</strong> &rarr; <strong>Click any AI Agent to expand its Human Persona</strong>.
            </p>
          </div>

          <!-- Pill Tabs -->
          <div class="pt-top-tabs" style="margin-bottom:0;">
            <button type="button" class="pt-tab-btn ${currentMindMapMode === 'mindmap' ? 'active' : ''}"
                    onclick="openMindMapPage('mindmap', '${currentMindMapDeptId}', '${currentMindMapSubPillarId}', false)">
              <span>🧠 Neural Mind Map</span>
              <span class="pt-tab-count">6 Pillars &rarr; 20 Sub-Pillars &rarr; 60 Agents</span>
            </button>
            <button type="button" class="pt-tab-btn ${currentMindMapMode === 'flowchart' ? 'active' : ''}"
                    onclick="openMindMapPage('flowchart', '${currentMindMapDeptId}', '${currentMindMapSubPillarId}', false)">
              <span>🧭 Portal Navigation Flowchart</span>
              <span class="pt-tab-count">6 Steps</span>
            </button>
          </div>
        </div>

        ${currentMindMapMode === 'mindmap' ? `
          <!-- FULL-SCREEN 3-COLUMN NEURAL MIND MAP: PILLARS -> SUB-PILLARS -> AGENTS (EXPAND FOR PERSONA) -->
          <div class="mm-neural-board">
            <!-- COLUMN 1: 6 CORE OPERATING PILLARS / DOMAINS -->
            <div class="mm-neural-col">
              <div class="mm-neural-col-header">
                <div>
                  <span class="mm-neural-step-pill">NODE LAYER 01</span>
                  <div style="font-family:var(--font-display); font-size:18px; font-weight:800; color:var(--text-primary); margin-top:6px;">
                    Core Pillars (6 Domains)
                  </div>
                </div>
              </div>

              <div style="display:flex; flex-direction:column; flex:1; justify-content:space-between;">
                ${Object.values(DEPARTMENTS).map(d => {
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
                        <div style="font-family:var(--font-display); font-size:16px; font-weight:800; color:var(--text-primary); margin-top:3px;">
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
                    <stop offset="100%" stop-color="${(activeSubPillar && activeSubPillar.color) || activeDept.color}" stop-opacity="0.95" />
                  </linearGradient>
                </defs>
                <path d="M 0 210 C 24 210, 24 90, 48 90" fill="none" stroke="url(#mmBridgeGrad1)" stroke-width="2.2" stroke-dasharray="5 5" opacity="0.55" />
                <path d="M 0 210 C 24 210, 24 170, 48 170" fill="none" stroke="url(#mmBridgeGrad1)" stroke-width="2.8" />
                <path d="M 0 210 C 24 210, 24 250, 48 250" fill="none" stroke="url(#mmBridgeGrad1)" stroke-width="2.8" />
                <path d="M 0 210 C 24 210, 24 330, 48 330" fill="none" stroke="url(#mmBridgeGrad1)" stroke-width="2.2" stroke-dasharray="5 5" opacity="0.55" />
                <circle r="4.5" fill="${activeDept.color}">
                  <animate attributeName="cx" from="4" to="44" dur="1.4s" repeatCount="indefinite" />
                  <animate attributeName="cy" from="210" to="170" dur="1.4s" repeatCount="indefinite" />
                </circle>
                <circle r="4.5" fill="${(activeSubPillar && activeSubPillar.color) || activeDept.color}">
                  <animate attributeName="cx" from="4" to="44" dur="1.8s" repeatCount="indefinite" />
                  <animate attributeName="cy" from="210" to="250" dur="1.8s" repeatCount="indefinite" />
                </circle>
              </svg>
            </div>

            <!-- COLUMN 2: SUB-PILLARS ONLY (NO PERSONAS HERE!) -->
            <div class="mm-neural-col" style="animation: ptExpandIn 0.26s var(--ease-spring) forwards;">
              <div class="mm-neural-col-header">
                <div>
                  <span class="mm-neural-step-pill" style="color:${activeDept.color}; border-color:${activeDept.color}55; background:${activeDept.color}18;">
                    NODE LAYER 02 · ${activeDept.scorBadge}
                  </span>
                  <div style="font-family:var(--font-display); font-size:18px; font-weight:800; color:var(--text-primary); margin-top:6px;">
                    Sub-Pillars in ${activeDept.name} (${deptSubPillars.length})
                  </div>
                </div>
              </div>

              <div style="display:flex; flex-direction:column; gap:14px; flex:1; justify-content:center;">
                ${deptSubPillars.map((sp, idx) => {
                  const isAct = activeSubPillar && sp.id === activeSubPillar.id;
                  return `
                    <button type="button" class="mm-subpillar-node ${isAct ? 'active' : ''}"
                            style="--node-color:${sp.color}; padding:20px 18px;"
                            onclick="selectMindMapSubPillar('${sp.id}')">
                      <div style="display:flex; align-items:center; gap:14px;">
                        <div style="width:44px; height:44px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px; background:${sp.color}18; border:1px solid ${sp.color}45; flex-shrink:0;">
                          ${sp.icon}
                        </div>
                        <div>
                          <div style="font-family:var(--font-mono); font-size:10.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:${sp.color};">
                            SUB-PILLAR 0${idx + 1}
                          </div>
                          <div style="font-family:var(--font-display); font-size:17px; font-weight:800; color:var(--text-primary); margin-top:2px;">
                            ${sp.name}
                          </div>
                        </div>
                      </div>
                      <span style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; padding:5px 10px; border-radius:999px; background:${sp.color}18; color:${sp.color}; border:1px solid ${sp.color}40; white-space:nowrap;">
                        3 AI Agents &rarr;
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
                    <stop offset="0%" stop-color="${(activeSubPillar && activeSubPillar.color) || activeDept.color}" stop-opacity="0.95" />
                    <stop offset="100%" stop-color="#10b981" stop-opacity="0.95" />
                  </linearGradient>
                </defs>
                <path d="M 0 210 C 24 210, 24 100, 48 100" fill="none" stroke="url(#mmBridgeGrad2)" stroke-width="2.6" />
                <path d="M 0 210 C 24 210, 24 210, 48 210" fill="none" stroke="url(#mmBridgeGrad2)" stroke-width="2.8" />
                <path d="M 0 210 C 24 210, 24 320, 48 320" fill="none" stroke="url(#mmBridgeGrad2)" stroke-width="2.6" />
                <circle r="4.5" fill="#10b981">
                  <animate attributeName="cx" from="4" to="44" dur="1.3s" repeatCount="indefinite" />
                  <animate attributeName="cy" from="210" to="100" dur="1.3s" repeatCount="indefinite" />
                </circle>
                <circle r="4.5" fill="${(activeSubPillar && activeSubPillar.color) || activeDept.color}">
                  <animate attributeName="cx" from="4" to="44" dur="1.6s" repeatCount="indefinite" />
                  <animate attributeName="cy" from="210" to="210" dur="1.6s" repeatCount="indefinite" />
                </circle>
                <circle r="4.5" fill="#38bdf8">
                  <animate attributeName="cx" from="4" to="44" dur="1.9s" repeatCount="indefinite" />
                  <animate attributeName="cy" from="210" to="320" dur="1.9s" repeatCount="indefinite" />
                </circle>
              </svg>
            </div>

            <!-- COLUMN 3: AI AGENTS IN SELECTED SUB-PILLAR (EXPAND AN AGENT TO SEE ITS HUMAN PERSONA!) -->
            <div class="mm-neural-col" style="animation: ptExpandIn 0.3s var(--ease-spring) forwards;">
              <div class="mm-neural-col-header">
                <div>
                  <span class="mm-neural-step-pill" style="color:${(activeSubPillar && activeSubPillar.color) || activeDept.color}; border-color:${(activeSubPillar && activeSubPillar.color) || activeDept.color}55; background:${(activeSubPillar && activeSubPillar.color) || activeDept.color}18;">
                    NODE LAYER 03 · ${(activeSubPillar && activeSubPillar.name) || 'SUB-PILLAR'}
                  </span>
                  <div style="font-family:var(--font-display); font-size:18px; font-weight:800; color:var(--text-primary); margin-top:6px;">
                    AI Agents (${subPillarItems.length}) · <span style="font-size:14px; font-weight:600; color:var(--text-secondary);">Click any Agent to expand its Human Persona</span>
                  </div>
                </div>
              </div>

              <div style="display:flex; flex-direction:column; gap:14px; flex:1;">
                ${subPillarItems.map((it, idx) => {
                  const ag = AGENTS[it.agentId];
                  const p = PERSONAS[it.personaId];
                  if (!ag || !p) return '';
                  const m = PERIODIC_AGENT_META[ag.id] || { code: '101', sym: 'Ai', short: ag.name, trigIcon: '⚡', trigger: 'Event-Driven', layer: 'Vertex AI ADK' };
                  const cls = getAgentBuildClassification(ag);
                  const isExpanded = ag.id === currentMindMapAgentId;
                  const spColor = (activeSubPillar && activeSubPillar.color) || activeDept.color;

                  return `
                    <div class="mm-agent-neural-card ${isExpanded ? 'expanded' : ''}" style="--ag-color:${spColor};">
                      <button type="button" class="mm-agent-neural-header" onclick="selectMindMapAgent('${ag.id}')">
                        <div style="display:flex; align-items:center; gap:14px;">
                          <div class="ai-bot-square" style="width:46px; height:46px; font-size:19px; flex-shrink:0;">✦</div>
                          <div>
                            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:4px;">
                              <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; padding:2px 8px; border-radius:6px; background:${spColor}22; color:${spColor}; border:1px solid ${spColor}55;">
                                A-${m.code} · ${m.sym}
                              </span>
                              <span class="build-tier-badge ${cls.cssClass}" style="font-size:10.5px; padding:2px 8px;">${cls.label}</span>
                              <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:#10b981;">✦ ${ag.badge}</span>
                            </div>
                            <div style="font-family:var(--font-display); font-size:18px; font-weight:800; color:var(--text-primary);">
                              ${ag.name}
                            </div>
                          </div>
                        </div>

                        <div style="display:flex; align-items:center; gap:10px;">
                          <span style="font-family:var(--font-mono); font-size:11.5px; font-weight:700; padding:6px 12px; border-radius:999px; background:rgba(245,158,11,0.14); color:#f59e0b; border:1px solid rgba(245,158,11,0.38); white-space:nowrap;">
                            👤 ${isExpanded ? 'Persona Expanded ▴' : 'Show Persona ▾'}
                          </span>
                        </div>
                      </button>

                      <div class="mm-agent-neural-body">
                        <div style="padding-top:14px; font-size:14px; color:var(--text-secondary); line-height:1.58;">
                          ${shortSentence(ag.solution || ag.role, 200)}
                        </div>

                        <!-- EXPANDED HUMAN PERSONA NODE INSIDE THE AI AGENT -->
                        <div class="mm-expanded-persona-box">
                          <div style="display:flex; align-items:center; gap:14px;">
                            <div class="human-avatar-circle" style="width:52px; height:52px; font-size:24px; --dept-accent:#f59e0b;">
                              ${p.icon}
                            </div>
                            <div>
                              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:3px;">
                                <span class="human-role-tag">👤 Connected Human Persona</span>
                                <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:#10b981;">
                                  ⚡ ${p.toilHoursBefore || '6.5h'} &rarr; ${p.toilHoursAfter || '1.0h'} (${p.headlineStat || '-85% Toil'})
                                </span>
                              </div>
                              <div style="font-family:var(--font-display); font-size:17.5px; font-weight:800; color:var(--text-primary);">
                                ${p.name}
                              </div>
                              <div style="font-size:13px; color:var(--text-secondary); margin-top:2px;">
                                ${shortSentence(p.mandate || p.role, 130)}
                              </div>
                            </div>
                          </div>

                          <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                            <button type="button" class="switch-pill" style="background:#f59e0b; color:#041019; font-weight:800; border:none; padding:10px 16px;" onclick="openPersonaPage('${p.id}', true, event)">
                              👤 Open ${p.name} Journey &rarr;
                            </button>
                            <button type="button" class="agent-plug-btn" style="padding:10px 16px; font-size:13px;" onclick="openAgentPage('${ag.id}', true, event)">
                              <span>✦ Open ${ag.name} Studio</span>
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
          <!-- PORTAL CLICK-PATH FLOWCHART ("WHAT OPENS WHEN YOU CLICK") -->
          <div style="padding:26px; border-radius:20px; background:rgba(11,17,30,0.85); border:1px solid var(--border-subtle);">
            <div style="margin-bottom:18px;">
              <h2 style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary);">
                6-Step Portal Click-Path Architecture
              </h2>
              <p style="font-size:14px; color:var(--text-secondary); margin-top:4px;">
                Click any step below to jump directly to that layer of the portal.
              </p>
            </div>

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:16px;">
              ${flowSteps.map((st, idx) => `
                <div style="padding:20px; border-radius:16px; background:var(--bg-surface); border:1px solid var(--border-subtle); border-top:4px solid ${st.color}; display:flex; flex-direction:column; justify-content:space-between; gap:14px;">
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


def patch_html(path: Path):
    text = path.read_text(encoding="utf-8")

    # 1. Inject EXTRA_CSS before </style>
    if "CLEAN PERIODIC TABLE & FULL-SCREEN NEURAL MIND MAP OVERRIDES" not in text:
        text = text.replace("  </style>", EXTRA_CSS + "\n  </style>", 1)

    # 2. Replace from `let currentPeriodicFilter =` through the end of `openMindMapPage` (right before `/* =========================================================================\n       MULTI-PAGE SWITCHING`)
    pattern = re.compile(
        r"    (?:function getAgentSellingMeta[\s\S]*?)?let currentPeriodicFilter =[\s\S]*?(?=    /\* =========================================================================\n       MULTI-PAGE SWITCHING)",
        re.M,
    )
    if not pattern.search(text):
        raise RuntimeError(f"Could not find Periodic Table / Mind Map block in {path}")
    text = pattern.sub(NEW_SELLING_META_AND_PERIODIC_AND_MINDMAP_JS + "\n\n", text, count=1)

    path.write_text(text, encoding="utf-8")
    print(f"Updated: {path}")


if __name__ == "__main__":
    for f in HTML_FILES:
        if f.exists():
            patch_html(f)

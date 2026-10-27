#!/usr/bin/env python3
"""
Reverts the Periodic Table (#pagePeriodic) back to the structured 6-Pillar ->
Sub-Pillar -> 3-Tile layout from commit 8f2f196 and polishes its visual presentation:
- Restores .pt-top-tabs, .pt-main-layout, .pt-pillar-card, .pt-subpillars-grid,
  .pt-subpillar-group, .pt-subpillar-tiles, .pt-tile, .pt-inline-expand,
  .pt-sidebar, .pt-side-card, and .pt-legend-box.
- Polishes .pt-tile so agent names wrap cleanly across 2 lines (never truncated
  with ellipsis), with balanced height, crisp borders, and smooth hover/active states.
- Keeps all Persona and Agent boxes across the portal clean (just Name + Sub-Pillar/Pillar,
  no redundant 'Human Persona' or 'AI Agent' tags).
"""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML_FILES = [
    ROOT / "index.html",
    ROOT / "periodic_table.html",
    ROOT / "mind_map.html",
]

POLISHED_PT_CSS = """    /* =========================================================================
       POLISHED PERIODIC TABLE OF AGENTS (.pt-pillar-card, .pt-subpillar-group, .pt-tile)
       ========================================================================= */
    .pt-pillar-card {
      margin-bottom: 22px;
      padding: 20px 22px;
      border-radius: 18px;
      background: rgba(11, 17, 30, 0.86);
      border: 1px solid rgba(148, 163, 184, 0.2);
      border-left: 5px solid var(--dom-color, #38bdf8);
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.28);
      transition: border-color 0.22s ease, box-shadow 0.22s ease;
    }

    html[data-theme="light"] .pt-pillar-card {
      background: #ffffff;
      border-color: rgba(15, 23, 42, 0.12);
      border-left: 5px solid var(--dom-color, #2563eb);
      box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    }

    .pt-subpillars-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
      margin-top: 14px;
    }

    .pt-subpillar-group {
      padding: 14px 14px 14px;
      border-radius: 14px;
      background: rgba(15, 23, 42, 0.72);
      border: 1px solid rgba(148, 163, 184, 0.16);
      border-top: 3px solid var(--sp-color, #38bdf8);
    }

    html[data-theme="light"] .pt-subpillar-group {
      background: #f8fafc;
      border-color: rgba(15, 23, 42, 0.1);
      border-top: 3px solid var(--sp-color, #2563eb);
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
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid rgba(148, 163, 184, 0.14);
    }

    .pt-subpillar-tiles {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
    }

    .pt-tile {
      position: relative;
      min-height: 106px !important;
      height: auto !important;
      padding: 10px 8px 9px !important;
      border-radius: 12px;
      background: rgba(15, 23, 42, 0.84);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-top: 3px solid var(--tile-color, #38bdf8);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      text-align: center;
      cursor: pointer;
      user-select: none;
      transition: transform 0.24s var(--ease-spring), background 0.2s ease, border-color 0.2s ease, box-shadow 0.24s var(--ease-spring);
    }

    html[data-theme="light"] .pt-tile {
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-top: 3px solid var(--tile-color, #2563eb);
      box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
    }

    .pt-tile:hover {
      transform: translateY(-4px);
      background: rgba(23, 35, 62, 0.96);
      border-color: var(--tile-color, #38bdf8);
      box-shadow: 0 12px 24px rgba(0, 0, 0, 0.38);
    }

    html[data-theme="light"] .pt-tile:hover {
      background: #f8fbff;
      border-color: var(--tile-color, #2563eb);
      box-shadow: 0 10px 20px rgba(37, 99, 235, 0.14);
    }

    .pt-tile.active {
      background: rgba(28, 43, 75, 0.98);
      border-color: var(--tile-color, #38bdf8);
      box-shadow: 0 0 0 1.5px var(--tile-color, #38bdf8), 0 12px 28px rgba(0, 0, 0, 0.48);
      transform: translateY(-3px);
    }

    html[data-theme="light"] .pt-tile.active {
      background: #eff6ff;
      border-color: var(--tile-color, #2563eb);
      box-shadow: 0 0 0 1.5px var(--tile-color, #2563eb), 0 10px 22px rgba(37, 99, 235, 0.18);
    }

    .pt-tile-sym {
      font-family: var(--font-display);
      font-size: 18px;
      font-weight: 800;
      color: var(--tile-color, #38bdf8);
      line-height: 1.05;
      letter-spacing: -0.02em;
      margin: 2px 0;
    }

    .pt-tile-title {
      font-family: var(--font-sans);
      font-size: 12px !important;
      font-weight: 700 !important;
      color: var(--text-primary) !important;
      line-height: 1.22 !important;
      max-width: 100%;
      white-space: normal !important;
      overflow: hidden;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      word-break: break-word;
      margin: 2px 0 4px;
    }
"""

POLISHED_PERIODIC_JS = """    let currentPeriodicFilter = 'all'; // 'all' | group.id
    let currentSelectedElementId = 'demand_sensing_agent';
    let currentExpandedInlineId = null;

    function cleanAgentName(rawName) {
      if (!rawName) return '';
      return String(rawName).replace(/^\\[[^\\]]+\\]\\s*/, '').trim();
    }

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
        code: '101', sym: 'Ds', short: cleanAgentName(selAg.name), group: selAg.deptId,
        layer: 'Vertex AI ADK + A2A', layerColor: '#3b82f6', trigger: 'Event-Driven', trigIcon: '⚡'
      };
      const selGrp = PERIODIC_GROUPS.find(g => g.id === selMeta.group) || PERIODIC_GROUPS[0];
      const selDept = DEPARTMENTS[selAg.deptId] || Object.values(DEPARTMENTS)[0];
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
                  <button type="button" class="switch-pill" style="border-color:#f59e0b; color:#f59e0b; font-weight:700;" onclick="openPersonaPage('${pOwner.id}', true, event)">
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

      const visibleGroups = PERIODIC_GROUPS.filter(g => currentPeriodicFilter === 'all' || g.id === currentPeriodicFilter);
      const leftColumnHtml = visibleGroups.map(grp => {
        const deptObj = DEPARTMENTS[grp.id];
        const subPillars = (deptObj && deptObj.subPillars) || [];
        const grpAgents = Object.entries(PERIODIC_AGENT_META)
          .filter(([_, m]) => m.group === grp.id)
          .map(([aid, m]) => ({ ag: AGENTS[aid], m }))
          .filter(x => x.ag);
        const expandedItem = grpAgents.find(x => x.ag.id === currentExpandedInlineId);
        const cleanPillarTitle = deptObj ? `${deptObj.scorBadge || ''} · ${deptObj.name}` : grp.shortTab;

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
                  const m = PERIODIC_AGENT_META[it.agentId] || { code: '101', sym: 'Ai', short: cleanAgentName(it.agentName), layerColor: sp.color, trigIcon: '⚡', layer: 'Vertex AI ADK', trigger: 'Event-Driven' };
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
                        const shortLabel = cleanAgentName(m.short || ag.name).replace(/\\s+Agent$/i, '');
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
              <strong>6 Core Pillars</strong> &rarr; <strong>20 Sub-Pillars</strong> &rarr; <strong>60 AI Agents</strong> (3 per Sub-Pillar). Click any tile to inspect its Persona and open the Agent Studio.
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
            <span>All Pillars</span>
            <span class="pt-tab-count">60</span>
          </button>
          ${PERIODIC_GROUPS.map(g => {
            const cleanTab = g.shortTab.replace(/\\s*\\(\\d+\\)$/, '');
            return `
              <button type="button" class="pt-tab-btn ${currentPeriodicFilter === g.id ? 'active' : ''}"
                      onclick="currentExpandedInlineId = null; openPeriodicTablePage('${g.id}', '${selAg.id}', false)">
                <span>${cleanTab}</span>
                <span class="pt-tab-count">${g.count}</span>
              </button>
            `;
          }).join('')}
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

              ${selAg.costModel ? `
                <div style="padding:10px 12px; border-radius:10px; background:var(--bg-elevated); border:1px solid var(--border-subtle); margin-bottom:14px; font-family:var(--font-mono); font-size:11.5px; color:var(--text-secondary);">
                  💰 <strong style="color:var(--text-primary);">$${selAg.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo</strong> vs. <strong style="color:#f43f5e;">$${(selAg.costModel.manualComparison ? selAg.costModel.manualComparison.manualMonthlyCostUsd : 24000).toLocaleString()}/mo</strong> manual
                </div>
              ` : ''}

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
    }"""


def update_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    # 1. Remove the injected Vamshi .pt CSS block and replace with POLISHED_PT_CSS
    css_start = "    /* =========================================================================\n       VAMSHI-ALIGNED PERIODIC TABLE OF AGENTS (.pt-*) — DARK & LIGHT THEMES"
    css_end = "    /* =========================================================================\n       PERIODIC TABLE & MIND MAP HIGH-CONTRAST READABILITY CLASSES (BOTH THEMES)"
    if css_start in text and css_end in text:
        s_idx = text.index(css_start)
        e_idx = text.index(css_end)
        text = text[:s_idx] + POLISHED_PT_CSS + "\n\n" + text[e_idx:]

    # 2. Replace the Periodic Table JS block with POLISHED_PERIODIC_JS
    pt_start = "    let currentPeriodicFilter = 'all';"
    pt_end = "    /* =========================================================================\n       PAGE 8: FULL-SCREEN NEURAL MIND MAP"
    assert pt_start in text and pt_end in text, f"PT JS markers not found in {path}"
    s_idx = text.index(pt_start)
    e_idx = text.index(pt_end)
    text = text[:s_idx] + POLISHED_PERIODIC_JS + "\n\n" + text[e_idx:]

    path.write_text(text, encoding="utf-8")
    print(f"Restored and polished Periodic Table in {path.name} ({len(text):,} bytes)")


def main() -> None:
    for hp in HTML_FILES:
        if hp.exists():
            update_file(hp)


if __name__ == "__main__":
    main()

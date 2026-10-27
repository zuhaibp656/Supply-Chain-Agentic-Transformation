#!/usr/bin/env python3
"""
Aligns the Periodic Table of Supply Chain AI Agents 100% with Vamshi's Periodic Table
(https://vamsiramakrishnan.github.io/ge-agent-factory/catalog/) — including exact
CSS, top pill tabs, flat domain rows, compact .pt-cell tiles with top-center number,
top-left HITL shield SVG, top-right Trigger SVG (lightning/chat/clock), 2-line short
name (no fake chemical symbols), bottom layer dot, live hover preview in the right
sticky .pt-detail card, and .pt-legend box.

Also cleans up all Persona & Agent boxes across the portal to remove redundant
'Human Persona' / 'AI Agent' badges and duplicate Pillar/Sub-Pillar labels, leaving
just the clean Name + single Sub-Pillar/Pillar subtitle.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML_FILES = [
    ROOT / "index.html",
    ROOT / "periodic_table.html",
    ROOT / "mind_map.html",
]

VAMSHI_PT_CSS = """
    /* =========================================================================
       VAMSHI-ALIGNED PERIODIC TABLE OF AGENTS (.pt-*) — DARK & LIGHT THEMES
       ========================================================================= */
    .pt {
      --pt-border: rgba(148, 163, 184, 0.22);
      --pt-surface: rgba(15, 23, 42, 0.72);
      --pt-surface-hover: rgba(30, 41, 59, 0.95);
      --pt-text: #f8fafc;
      --pt-muted: #94a3b8;
      margin: 0.5rem 0 2rem;
    }

    html[data-theme="light"] .pt {
      --pt-border: rgba(15, 23, 42, 0.12);
      --pt-surface: #ffffff;
      --pt-surface-hover: #f8fafc;
      --pt-text: #0f172a;
      --pt-muted: #475569;
    }

    .pt-tabs {
      display: flex;
      flex-wrap: wrap;
      gap: 0.4rem;
      margin: 0 0 1.25rem;
      padding: 0 0 0.9rem;
      border-bottom: 1px solid var(--pt-border);
    }

    .pt-tab {
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.42rem 0.85rem;
      border: 1px solid var(--pt-border);
      border-radius: 999px;
      background: var(--pt-surface);
      color: var(--pt-text);
      font-family: var(--font-sans);
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 120ms ease;
    }

    .pt-tab:hover {
      border-color: var(--g-blue);
      transform: translateY(-1px);
    }

    .pt-tab.is-active {
      background: var(--g-blue);
      color: #ffffff !important;
      border-color: var(--g-blue);
    }

    .pt-tab-label {
      color: inherit;
    }

    .pt-tab-count {
      font-family: var(--font-mono);
      font-size: 0.68rem;
      font-weight: 700;
      padding: 0.08rem 0.42rem;
      border-radius: 999px;
      background: rgba(148, 163, 184, 0.18);
      color: inherit;
    }

    .pt-tab.is-active .pt-tab-count {
      background: rgba(255, 255, 255, 0.24);
      color: #ffffff;
    }

    .pt-head {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: flex-end;
      gap: 1rem;
      margin-bottom: 1.1rem;
      padding-bottom: 0.85rem;
      border-bottom: 1px solid var(--pt-border);
    }

    .pt-title {
      margin: 0;
      font-family: var(--font-display);
      font-size: 1.45rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: var(--pt-text);
    }

    .pt-subtitle {
      margin: 0.25rem 0 0;
      font-size: 0.86rem;
      color: var(--pt-muted);
      max-width: 52rem;
      line-height: 1.45;
    }

    .pt-stats {
      display: flex;
      gap: 1.1rem;
    }

    .pt-stat {
      font-size: 0.78rem;
      color: var(--pt-muted);
    }

    .pt-stat strong {
      display: block;
      font-size: 1.25rem;
      font-weight: 800;
      color: var(--pt-text);
      font-variant-numeric: tabular-nums;
      line-height: 1.1;
    }

    .pt-body {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 17.5rem;
      gap: 1.25rem;
      align-items: start;
    }

    @media (max-width: 1080px) {
      .pt-body {
        grid-template-columns: 1fr;
      }
    }

    .pt-grid-wrap {
      min-width: 0;
    }

    .pt-group {
      margin-bottom: 0.95rem;
    }

    .pt-group:last-child {
      margin-bottom: 0;
    }

    .pt-group-head {
      display: flex;
      align-items: center;
      gap: 0.45rem;
      margin-bottom: 0.35rem;
    }

    .pt-group-swatch {
      width: 0.62rem;
      height: 0.62rem;
      border-radius: 0.16rem;
      flex-shrink: 0;
    }

    .pt-group-title {
      font-size: 0.74rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--pt-text);
    }

    .pt-group-pillar-tag {
      font-family: var(--font-mono);
      font-size: 0.64rem;
      font-weight: 600;
      color: var(--pt-muted);
      padding: 0.05rem 0.38rem;
      border-radius: 4px;
      border: 1px solid var(--pt-border);
    }

    .pt-group-count {
      font-family: var(--font-mono);
      font-size: 0.68rem;
      color: var(--pt-muted);
      font-variant-numeric: tabular-nums;
    }

    .pt-grid {
      display: grid;
      grid-template-columns: repeat(var(--pt-cols, 6), minmax(0, 1fr));
      gap: 6px;
    }

    @media (max-width: 1100px) {
      .pt-grid {
        grid-template-columns: repeat(4, minmax(0, 1fr));
      }
    }

    @media (max-width: 640px) {
      .pt-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr));
      }
    }

    .pt-cell {
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      padding: 1.25rem 0.35rem 0.42rem;
      min-height: 4.1rem;
      border: 1px solid var(--pt-border);
      border-top: 3px solid var(--pt-domain, #475569);
      border-radius: 6px 6px 4px 4px;
      background: var(--pt-surface);
      color: var(--pt-text);
      text-decoration: none;
      transition: transform 120ms ease, box-shadow 120ms ease, border-color 120ms ease, background 120ms ease;
      overflow: hidden;
      cursor: pointer;
    }

    .pt-cell:hover,
    .pt-cell:focus-visible,
    .pt-cell.is-selected {
      transform: scale(1.08);
      z-index: 5;
      background: var(--pt-surface-hover);
      border-color: var(--pt-domain, #475569);
      box-shadow: 0 8px 22px -4px rgba(0, 0, 0, 0.32);
      outline: none;
    }

    .pt-cell-num {
      position: absolute;
      top: 0.28rem;
      left: 50%;
      transform: translateX(-50%);
      font-family: var(--font-mono);
      font-size: 0.6rem;
      font-weight: 700;
      color: var(--pt-muted);
      font-variant-numeric: tabular-nums;
      letter-spacing: -0.02em;
      line-height: 1;
    }

    .pt-cell-name {
      font-size: 0.68rem;
      font-weight: 600;
      line-height: 1.18;
      text-align: center;
      color: var(--pt-text);
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      word-break: break-word;
      hyphens: auto;
      max-width: 100%;
      margin-top: 0.1rem;
    }

    .pt-cell-dot {
      width: 0.42rem;
      height: 0.42rem;
      border-radius: 999px;
      flex-shrink: 0;
      margin-top: 0.32rem;
    }

    .pt-cell-trig {
      position: absolute;
      top: 0.26rem;
      right: 0.28rem;
      width: 0.72rem;
      height: 0.72rem;
      opacity: 0.85;
      color: var(--pt-text);
      flex-shrink: 0;
    }

    .pt-cell-trig[data-trig="event-driven"] { color: #10b981; }
    .pt-cell-trig[data-trig="chat-initiated"] { color: #3b82f6; }
    .pt-cell-trig[data-trig="scheduled"] { color: #f59e0b; }

    .pt-cell-hitl {
      position: absolute;
      top: 0.26rem;
      left: 0.28rem;
      width: 0.72rem;
      height: 0.72rem;
      color: #ef4444;
      opacity: 0.9;
      flex-shrink: 0;
    }

    .pt-side {
      position: sticky;
      top: 5.2rem;
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
    }

    .pt-detail {
      border: 1px solid var(--pt-border);
      border-radius: 0.65rem;
      padding: 0.9rem;
      background: var(--pt-surface);
      min-height: 7.5rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 0.65rem;
    }

    .pt-detail-top {
      display: flex;
      gap: 0.65rem;
      align-items: flex-start;
    }

    .pt-detail-badge {
      font-family: var(--font-mono);
      font-size: 0.72rem;
      font-weight: 700;
      color: #ffffff;
      padding: 0.28rem 0.5rem;
      border-radius: 0.32rem;
      font-variant-numeric: tabular-nums;
      flex-shrink: 0;
    }

    .pt-detail-titles {
      min-width: 0;
    }

    .pt-detail-name {
      font-weight: 700;
      font-size: 0.92rem;
      line-height: 1.25;
      color: var(--pt-text);
    }

    .pt-detail-meta {
      font-size: 0.74rem;
      color: var(--pt-muted);
      margin-top: 0.14rem;
    }

    .pt-detail-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 0.35rem;
    }

    .pt-tag {
      font-size: 0.68rem;
      padding: 0.14rem 0.46rem;
      border-radius: 0.28rem;
      border: 1px solid var(--pt-border);
      color: var(--pt-text);
      font-weight: 600;
    }

    .pt-tag--layer {
      border-color: var(--tag-c);
      color: var(--tag-c);
      font-weight: 700;
    }

    .pt-tag--hitl {
      border-color: rgba(239, 68, 68, 0.45);
      color: #ef4444;
    }

    .pt-detail-link {
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--g-blue);
      text-decoration: none;
      align-self: flex-start;
      cursor: pointer;
    }

    .pt-detail-link:hover {
      text-decoration: underline;
    }

    .pt-legend {
      border: 1px solid var(--pt-border);
      border-radius: 0.65rem;
      padding: 0.8rem 0.9rem;
      background: var(--pt-surface);
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }

    .pt-legend-title {
      font-size: 0.66rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--pt-muted);
      margin-bottom: 0.35rem;
    }

    .pt-legend-items {
      display: flex;
      flex-direction: column;
      gap: 0.28rem;
    }

    .pt-legend-item {
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      font-size: 0.74rem;
      color: var(--pt-text);
    }

    .pt-legend-dot {
      width: 0.5rem;
      height: 0.5rem;
      border-radius: 999px;
      flex-shrink: 0;
    }

    .pt-legend-ico {
      width: 0.8rem;
      height: 0.8rem;
      flex-shrink: 0;
    }

    .pt-legend-domains {
      display: flex;
      flex-direction: column;
      gap: 0.24rem;
      max-height: 16rem;
      overflow-y: auto;
      padding-right: 0.2rem;
    }

    .pt-legend-domain {
      display: grid;
      grid-template-columns: 0.55rem 1fr auto;
      align-items: center;
      gap: 0.45rem;
      font-size: 0.72rem;
      padding: 0.16rem 0.25rem;
      border-radius: 4px;
      cursor: pointer;
      transition: background 120ms ease;
    }

    .pt-legend-domain:hover {
      background: rgba(148, 163, 184, 0.14);
    }

    .pt-legend-swatch {
      width: 0.55rem;
      height: 0.55rem;
      border-radius: 2px;
    }

    .pt-legend-domain-title {
      color: var(--pt-text);
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .pt-legend-domain-count {
      font-family: var(--font-mono);
      font-size: 0.66rem;
      color: var(--pt-muted);
      font-variant-numeric: tabular-nums;
    }
"""

NEW_PERIODIC_JS = """    let currentPeriodicFilter = 'all'; // 'all' | group.id | 'sp:' + subPillarId
    let currentSelectedElementId = 'demand_sensing_agent';
    let currentExpandedInlineId = null;

    function cleanAgentName(rawName) {
      if (!rawName) return '';
      return String(rawName).replace(/^\\[[^\\]]+\\]\\s*/, '').trim();
    }

    function getVamshiTriggerMeta(triggerStr) {
      const t = String(triggerStr || '').toLowerCase();
      if (t.includes('chat')) {
        return {
          slug: 'chat-initiated',
          label: 'Chat-Initiated',
          svgPath: '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'
        };
      }
      if (t.includes('sched') || t.includes('guard')) {
        return {
          slug: 'scheduled',
          label: 'Scheduled',
          svgPath: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'
        };
      }
      return {
        slug: 'event-driven',
        label: 'Event-Driven',
        svgPath: '<path d="M13 2 3 14h8l-1 8 10-12h-8l1-8z"/>'
      };
    }

    function getVamshiLayerMeta(ag, meta) {
      const l = String((meta && meta.layer) || '').toLowerCase();
      const cls = getAgentBuildClassification(ag);
      if (cls.tier === 'Low-Code' || l.includes('studio')) {
        return { name: 'OOTB', color: '#10b981' };
      }
      if (cls.tier === 'Hybrid' || l.includes('cloud run')) {
        return { name: 'Agent Designer', color: '#3b82f6' };
      }
      if (ag && ag.id && (ag.id.includes('steward') || ag.id.includes('auditor') || ag.id.includes('ledger') || ag.id.includes('sensor'))) {
        return { name: 'Data Agent', color: '#64748b' };
      }
      return { name: 'Custom ADK', color: '#f59e0b' };
    }

    function previewPeriodicAgent(agentId) {
      const ag = AGENTS[agentId];
      if (!ag) return;
      currentSelectedElementId = agentId;
      const meta = PERIODIC_AGENT_META[agentId] || {
        code: '101', short: cleanAgentName(ag.name), group: ag.deptId,
        subPillar: ag.subPillarName || 'Supply Chain', subPillarColor: '#2563eb',
        personaName: ag.primaryPersonaName || 'Supply Chain Lead',
        layer: 'Custom ADK', layerColor: '#f59e0b', trigger: 'Event-Driven'
      };
      const trig = getVamshiTriggerMeta(meta.trigger);
      const layer = getVamshiLayerMeta(ag, meta);
      const spColor = ag.subPillarColor || meta.subPillarColor || '#2563eb';
      const domainTitle = ag.subPillarName || meta.subPillar || 'Supply Chain';
      const cName = cleanAgentName(ag.name);

      const badgeEl = document.getElementById('ptDetailBadge');
      const nameEl = document.getElementById('ptDetailName');
      const metaEl = document.getElementById('ptDetailMeta');
      const tagsEl = document.getElementById('ptDetailTags');
      const linkEl = document.getElementById('ptDetailLink');

      if (badgeEl) {
        badgeEl.textContent = `A-${meta.code}`;
        badgeEl.style.background = spColor;
      }
      if (nameEl) nameEl.textContent = cName;
      if (metaEl) metaEl.textContent = `A-${meta.code} · ${domainTitle}`;
      if (tagsEl) {
        const hitlName = meta.personaName || ag.primaryPersonaName || 'Domain Lead';
        tagsEl.innerHTML = `
          <span class="pt-tag pt-tag--layer" style="--tag-c:${layer.color}">${layer.name}</span>
          <span class="pt-tag">${trig.label}</span>
          <span class="pt-tag pt-tag--hitl" title="${hitlName}">HITL · ${hitlName}</span>
        `;
      }
      if (linkEl) {
        linkEl.setAttribute('href', `#agent/${ag.id}`);
        linkEl.onclick = function(ev) {
          ev.preventDefault();
          openAgentPage(ag.id, true, ev);
        };
      }

      document.querySelectorAll('.pt-cell.is-selected').forEach(el => el.classList.remove('is-selected'));
      const activeCell = document.querySelector(`.pt-cell[data-agent-id="${agentId}"]`);
      if (activeCell) activeCell.classList.add('is-selected');
    }

    function handlePeriodicTileClick(agentId, ev) {
      currentSelectedElementId = agentId;
      openAgentPage(agentId, true, ev);
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
        code: '101', short: cleanAgentName(selAg.name), group: selAg.deptId,
        subPillar: selAg.subPillarName || 'Demand Forecasting', subPillarColor: '#2563eb',
        personaName: selAg.primaryPersonaName || 'Demand Planner / Forecaster',
        layer: 'Custom ADK', layerColor: '#f59e0b', trigger: 'Event-Driven'
      };
      const selTrig = getVamshiTriggerMeta(selMeta.trigger);
      const selLayer = getVamshiLayerMeta(selAg, selMeta);
      const selSpColor = selAg.subPillarColor || selMeta.subPillarColor || '#2563eb';
      const selDomainTitle = selAg.subPillarName || selMeta.subPillar || 'Demand Forecasting';
      const selCleanName = cleanAgentName(selAg.name);

      // Collect all 20 Sub-Pillar Domains across the 6 Pillars
      const allDomains = [];
      PERIODIC_GROUPS.forEach(grp => {
        const deptObj = DEPARTMENTS[grp.id];
        const subPillars = (deptObj && deptObj.subPillars) || [];
        subPillars.forEach(sp => {
          const spItems = (sp.items || []).map(it => {
            const ag = AGENTS[it.agentId];
            const m = PERIODIC_AGENT_META[it.agentId] || {
              code: '101', short: cleanAgentName(it.agentName),
              subPillar: sp.name, subPillarColor: sp.color || grp.color,
              personaName: it.personaName || 'Supply Chain Lead',
              layer: 'Custom ADK', layerColor: '#f59e0b', trigger: 'Event-Driven'
            };
            return { ag, m, it };
          }).filter(x => x.ag);
          allDomains.push({
            id: sp.id,
            name: sp.name,
            color: sp.color || grp.color,
            pillarId: grp.id,
            pillarShort: grp.shortTab.replace(/\\s*\\(\\d+\\)$/, ''),
            items: spItems
          });
        });
      });

      const visibleDomains = allDomains.filter(dom => {
        if (currentPeriodicFilter === 'all') return true;
        if (currentPeriodicFilter.startsWith('sp:')) return dom.id === currentPeriodicFilter.slice(3);
        return dom.pillarId === currentPeriodicFilter;
      });

      const totalVisibleAgents = visibleDomains.reduce((acc, d) => acc + d.items.length, 0);
      const activeGroupObj = PERIODIC_GROUPS.find(g => g.id === currentPeriodicFilter);
      const headTitle = currentPeriodicFilter === 'all'
        ? 'All Supply Chain'
        : (activeGroupObj ? activeGroupObj.shortTab.replace(/\\s*\\(\\d+\\)$/, '') : (visibleDomains[0] ? visibleDomains[0].name : 'Supply Chain'));
      const headSubtitle = currentPeriodicFilter === 'all'
        ? 'Cross-pillar view of all 60 Supply Chain AI agents across 20 operational domains — hover any tile to preview, click to open.'
        : `Showing ${totalVisibleAgents} Supply Chain AI agents across ${visibleDomains.length} operational ${visibleDomains.length === 1 ? 'domain' : 'domains'} — hover any tile to preview, click to open.`;

      const domainRowsHtml = visibleDomains.map(dom => {
        const cols = Math.max(6, dom.items.length);
        const cellsHtml = dom.items.map(({ ag, m }) => {
          const trig = getVamshiTriggerMeta(m.trigger);
          const layer = getVamshiLayerMeta(ag, m);
          const shortTitle = cleanAgentName(m.short || ag.name).replace(/\\s+Agent$/i, '');
          const hitlPersona = m.personaName || ag.primaryPersonaName || 'Domain Lead';
          const isSel = ag.id === selAg.id;

          return `
            <a class="pt-cell ${isSel ? 'is-selected' : ''}"
               href="#agent/${ag.id}"
               data-agent-id="${ag.id}"
               style="--pt-domain:${dom.color}"
               onmouseenter="previewPeriodicAgent('${ag.id}')"
               onfocus="previewPeriodicAgent('${ag.id}')"
               onclick="event.preventDefault(); handlePeriodicTileClick('${ag.id}', event)">
              <span class="pt-cell-num">${m.code}</span>
              <svg class="pt-cell-hitl" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" aria-label="Human-in-the-loop required">
                <title>Human-in-the-loop: ${hitlPersona}</title>
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                <path d="m9 12 2 2 4-4"/>
              </svg>
              <svg class="pt-cell-trig" data-trig="${trig.slug}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-label="Trigger: ${trig.label}">
                <title>Trigger: ${trig.label}</title>
                ${trig.svgPath}
              </svg>
              <span class="pt-cell-name">${shortTitle}</span>
              <span class="pt-cell-dot" style="background:${layer.color}" title="Layer: ${layer.name}"></span>
            </a>
          `;
        }).join('');

        return `
          <div class="pt-group">
            <div class="pt-group-head">
              <span class="pt-group-swatch" style="background:${dom.color}"></span>
              <span class="pt-group-title">${dom.name}</span>
              <span class="pt-group-count">${dom.items.length}</span>
            </div>
            <div class="pt-grid" style="--pt-cols:${cols}">
              ${cellsHtml}
            </div>
          </div>
        `;
      }).join('');

      const legendDomainsHtml = visibleDomains.map(dom => `
        <div class="pt-legend-domain" onclick="openPeriodicTablePage('sp:${dom.id}', '${dom.items[0] ? dom.items[0].ag.id : selAg.id}', false)">
          <span class="pt-legend-swatch" style="background:${dom.color}"></span>
          <span class="pt-legend-domain-title">${dom.name}</span>
          <span class="pt-legend-domain-count">${dom.items.length}</span>
        </div>
      `).join('');

      const container = document.getElementById('periodicPageContent');
      container.innerHTML = `
        <div class="pt">
          <!-- Top Pill Tabs (Vamshi Periodic Table Style) -->
          <div class="pt-tabs" role="tablist" aria-label="Supply Chain Pillars">
            <button type="button" role="tab" class="pt-tab ${currentPeriodicFilter === 'all' ? 'is-active' : ''}"
                    onclick="openPeriodicTablePage('all', '${selAg.id}', false)">
              <span class="pt-tab-label">All Supply Chain</span>
              <span class="pt-tab-count">60</span>
            </button>
            ${PERIODIC_GROUPS.map(g => {
              const cleanTab = g.shortTab.replace(/\\s*\\(\\d+\\)$/, '');
              return `
                <button type="button" role="tab" class="pt-tab ${currentPeriodicFilter === g.id ? 'is-active' : ''}"
                        onclick="openPeriodicTablePage('${g.id}', '${selAg.id}', false)">
                  <span class="pt-tab-label">${cleanTab}</span>
                  <span class="pt-tab-count">${g.count}</span>
                </button>
              `;
            }).join('')}
          </div>

          <!-- Header Row -->
          <div class="pt-head">
            <div>
              <h2 class="pt-title">${headTitle}</h2>
              <p class="pt-subtitle">${headSubtitle}</p>
            </div>
            <div class="pt-stats">
              <span class="pt-stat"><strong>${totalVisibleAgents}</strong> agents</span>
              <span class="pt-stat"><strong>${visibleDomains.length}</strong> domains</span>
            </div>
          </div>

          <!-- 2-Column Body: Left Flat Domain Grid + Right Sticky Detail & Legend -->
          <div class="pt-body">
            <div class="pt-grid-wrap">
              ${domainRowsHtml}
            </div>

            <aside class="pt-side">
              <!-- Live Hover Preview Card (.pt-detail) -->
              <div class="pt-detail">
                <div class="pt-detail-top">
                  <span class="pt-detail-badge" id="ptDetailBadge" style="background:${selSpColor}">A-${selMeta.code}</span>
                  <div class="pt-detail-titles">
                    <div class="pt-detail-name" id="ptDetailName">${selCleanName}</div>
                    <div class="pt-detail-meta" id="ptDetailMeta">A-${selMeta.code} · ${selDomainTitle}</div>
                  </div>
                </div>
                <div class="pt-detail-tags" id="ptDetailTags">
                  <span class="pt-tag pt-tag--layer" style="--tag-c:${selLayer.color}">${selLayer.name}</span>
                  <span class="pt-tag">${selTrig.label}</span>
                  <span class="pt-tag pt-tag--hitl" title="${selMeta.personaName || ''}">HITL · ${selMeta.personaName || 'Domain Lead'}</span>
                </div>
                <a class="pt-detail-link" id="ptDetailLink" href="#agent/${selAg.id}" onclick="event.preventDefault(); openAgentPage('${selAg.id}', true, event)">
                  View agent spec &rarr;
                </a>
              </div>

              <!-- Legend Box (.pt-legend) -->
              <div class="pt-legend">
                <div>
                  <div class="pt-legend-title">Layers</div>
                  <div class="pt-legend-items">
                    <span class="pt-legend-item"><span class="pt-legend-dot" style="background:#10b981"></span>OOTB</span>
                    <span class="pt-legend-item"><span class="pt-legend-dot" style="background:#3b82f6"></span>Agent Designer</span>
                    <span class="pt-legend-item"><span class="pt-legend-dot" style="background:#f59e0b"></span>Custom ADK</span>
                    <span class="pt-legend-item"><span class="pt-legend-dot" style="background:#64748b"></span>Data Agent</span>
                  </div>
                </div>

                <div>
                  <div class="pt-legend-title">Triggers</div>
                  <div class="pt-legend-items">
                    <span class="pt-legend-item">
                      <svg class="pt-legend-ico" style="color:#10b981" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h8l-1 8 10-12h-8l1-8z"/></svg>
                      Event-Driven
                    </span>
                    <span class="pt-legend-item">
                      <svg class="pt-legend-ico" style="color:#3b82f6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
                      Chat-Initiated
                    </span>
                    <span class="pt-legend-item">
                      <svg class="pt-legend-ico" style="color:#f59e0b" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>
                      Scheduled
                    </span>
                    <span class="pt-legend-item">
                      <svg class="pt-legend-ico" style="color:#ef4444" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>
                      Human-in-the-loop
                    </span>
                  </div>
                </div>

                <div>
                  <div class="pt-legend-title">Domains</div>
                  <div class="pt-legend-domains">
                    ${legendDomainsHtml}
                  </div>
                </div>
              </div>
            </aside>
          </div>
        </div>
      `;

      hydrateAssets();
      showActivePage('pagePeriodic');
    }"""


NEW_DIRECTORY_CARDS_JS = """    function renderDirectoryCardsHtml(deptFilter, searchQuery, mode = currentDirMode) {
      const q = (searchQuery || '').trim().toLowerCase();

      if (mode === 'agents') {
        const agentsList = Object.values(AGENTS).filter(ag => {
          if (deptFilter === 'universal' && !ag.isUniversal) return false;
          if (deptFilter !== 'all' && deptFilter !== 'universal' && ag.deptId !== deptFilter) return false;
          if (!q) return true;
          const dept = getDeptMeta(ag.deptId);
          const haystack = [cleanAgentName(ag.name), ag.subPillarName || '', dept ? dept.name : ''].join(' ').toLowerCase();
          return haystack.includes(q);
        });

        if (!agentsList.length) {
          return `<div style="grid-column: 1 / -1; padding: 36px; text-align: center; color: var(--text-secondary);">No matching agents found.</div>`;
        }

        return agentsList.map(ag => {
          const dept = getDeptMeta(ag.deptId);
          const cName = cleanAgentName(ag.name);
          const subLabel = ag.isUniversal ? 'Cross-Pillar Core' : (ag.subPillarName || dept.name);
          return `
            <div class="ai-agent-chip-card" style="padding:18px 20px;" onclick="openAgentPage('${ag.id}', true, event)">
              <div style="display:flex; align-items:center; gap:14px; min-width:0;">
                <div class="ai-bot-square" style="width:42px; height:42px; font-size:18px;">✦</div>
                <div style="min-width:0;">
                  <div class="ai-agent-chip-title" style="font-size:17px;">${cName}</div>
                  <div style="font-size:13px; color:var(--text-secondary); margin-top:2px;">
                    ${subLabel}
                  </div>
                </div>
              </div>
              <span style="color:#6366f1; font-weight:800; font-size:18px;">&rarr;</span>
            </div>
          `;
        }).join('');
      }

      const personasList = Object.values(PERSONAS).filter(p => {
        if (deptFilter !== 'all' && deptFilter !== 'universal' && p.deptId !== deptFilter) return false;
        if (!q) return true;
        const dept = getDeptMeta(p.deptId);
        const haystack = [p.name, p.subPillarName || '', dept ? dept.name : ''].join(' ').toLowerCase();
        return haystack.includes(q);
      });

      if (!personasList.length) {
        return `<div style="grid-column: 1 / -1; padding: 36px; text-align: center; color: var(--text-secondary);">No matching personas found.</div>`;
      }

      return personasList.map(p => {
        const dept = getDeptMeta(p.deptId);
        const subLabel = p.subPillarName || dept.name;
        return `
          <div class="human-persona-card" style="--dept-accent: ${dept.color};" onclick="openPersonaPage('${p.id}', true, event)">
            <div style="display:flex; align-items:center; gap:14px; min-width:0;">
              <div class="human-avatar-circle" style="--dept-accent: ${dept.color};">${p.icon}</div>
              <div style="min-width:0;">
                <div class="human-persona-title">${p.name}</div>
                <div class="human-persona-sub">${subLabel}</div>
              </div>
            </div>
            <span class="persona-open-arrow" style="color:${dept.color}; font-size:18px; font-weight:800;">&rarr;</span>
          </div>
        `;
      }).join('');
    }"""


def update_html_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    # 1. Inject Vamshi PT CSS before /* =========================================================================\n       PERIODIC TABLE & MIND MAP HIGH-CONTRAST READABILITY CLASSES
    css_anchor = "    /* =========================================================================\n       PERIODIC TABLE & MIND MAP HIGH-CONTRAST READABILITY CLASSES (BOTH THEMES)"
    if ".pt-cell-hitl" not in text:
        assert css_anchor in text, f"CSS anchor not found in {path}"
        text = text.replace(css_anchor, VAMSHI_PT_CSS + "\n" + css_anchor, 1)

    # 2. Replace Periodic Table JS block (from `let currentPeriodicFilter = 'all';` to just before `/* =========================================================================\n       PAGE 8: FULL-SCREEN NEURAL MIND MAP`)
    pt_start_marker = "    let currentPeriodicFilter = 'all';"
    pt_end_marker = "    /* =========================================================================\n       PAGE 8: FULL-SCREEN NEURAL MIND MAP"
    assert pt_start_marker in text and pt_end_marker in text, f"PT JS markers not found in {path}"
    start_idx = text.index(pt_start_marker)
    end_idx = text.index(pt_end_marker)
    text = text[:start_idx] + NEW_PERIODIC_JS + "\n\n" + text[end_idx:]

    # 3. Replace renderDirectoryCardsHtml function
    dir_start_marker = "    function renderDirectoryCardsHtml(deptFilter, searchQuery, mode = currentDirMode) {"
    dir_end_marker = "    function filterDirectoryLive(val) {"
    assert dir_start_marker in text and dir_end_marker in text, f"Directory markers not found in {path}"
    d_start = text.index(dir_start_marker)
    d_end = text.index(dir_end_marker)
    text = text[:d_start] + NEW_DIRECTORY_CARDS_JS + "\n\n" + text[d_end:]

    # 4. Clean up openPersonasDirectoryPage header switcher pills ("Personas (60)" / "Agents (60)" instead of "👤 Human Personas (60)")
    text = text.replace("👤 Human Personas (60)", "Personas (60)")
    text = text.replace("✦ AI Agents (60)", "Agents (60)")
    text = text.replace(
        "${currentDirMode === 'agents' ? '✦ 60 Supply Chain AI Agents' : '👤 60 Supply Chain Human Personas'}",
        "${currentDirMode === 'agents' ? '60 Supply Chain Agents' : '60 Supply Chain Personas'}"
    )

    # 5. Clean up Home Page Sub-Pillar Personas Drawer (`#subPillarPersonasDrawerEl`) — remove `<div class="human-role-tag" style="margin-bottom:4px;">👤 Human Persona</div>`
    text = text.replace(
        '<div class="human-role-tag" style="margin-bottom:4px;">👤 Human Persona</div>\n                          ',
        ''
    )

    # 6. Clean up Persona Page Header (`openPersonaPage`) — remove `👤 Human Persona` tag and redundant `p.role` (which repeats `SubPillar · Pillar`)
    old_persona_hdr = """                <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:6px;">
                  <span class="human-role-tag">👤 Human Persona</span>
                  <span class="persona-badge" style="margin-bottom:0; background: ${dept.color}18; color: ${dept.color}; border: 1px solid ${dept.color}45;">
                    ${dept.scorBadge || ''} · ${p.subPillarName || dept.name}
                  </span>
                </div>
                <h1 class="persona-page-title" style="margin-bottom:4px;">${p.name}</h1>
                <div style="font-size:15px; color:var(--text-secondary); font-weight:600;">${p.role}</div>"""
    new_persona_hdr = """                <h1 class="persona-page-title" style="margin-bottom:4px;">${p.name}</h1>
                <div style="font-size:15px; color:var(--text-secondary); font-weight:600;">${p.subPillarName || dept.name}</div>"""
    if old_persona_hdr in text:
        text = text.replace(old_persona_hdr, new_persona_hdr, 1)

    # 7. Clean up Persona Page Bottom Agent Dock Cards (`.persona-agent-dock-card`)
    old_dock_card = """                          <div>
                            <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap; margin-bottom:3px;">
                              <span class="ai-agent-type-tag">${ag.isUniversal ? 'UNIVERSAL AI' : 'DOMAIN AI'}</span>
                              <span class="build-tier-badge ${cls.cssClass}" style="font-size:10px; padding:2px 8px;">${cls.tier}</span>
                            </div>
                            <div class="ai-agent-chip-title" style="font-size:16.5px;">${ag.name}</div>
                          </div>"""
    new_dock_card = """                          <div>
                            <div class="ai-agent-chip-title" style="font-size:16.5px;">${cleanAgentName(ag.name)}</div>
                            <div style="font-size:12.5px; color:var(--text-secondary); margin-top:2px;">${ag.subPillarName || dept.name}</div>
                          </div>"""
    if old_dock_card in text:
        text = text.replace(old_dock_card, new_dock_card, 1)

    # 8. Clean up Agent Page Header (`openAgentPage`) — use cleanAgentName(ag.name) and single sub-pillar subtitle, no bracketed prefix
    old_agent_hdr = """            <div style="position:relative; z-index:2; display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin-bottom:12px;">
              <div class="persona-badge" style="margin-bottom:0; background: ${dept.color}18; color: ${dept.color}; border: 1px solid ${dept.color}40;">
                <span>${ag.isUniversal ? '🌐 Universal Core Agent' : `${dept.scorBadge} · ${dept.name}`}</span>
              </div>
              <span class="build-tier-badge ${cls.cssClass}">
                ${cls.label}
              </span>
              ${ag.badge ? `<span class="build-tier-badge" style="background:${dept.color}18; color:${dept.color}; border:1px solid ${dept.color}45;">✦ ${ag.badge}</span>` : ''}
              ${ag.costModel ? `<span class="build-tier-badge" style="background:${dept.color}14; color:${dept.color}; border:1px solid ${dept.color}40;">💰 $${ag.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo · $${ag.costModel.monthlyBreakdown.blendedCostPer1kCallsUsd.toFixed(2)}/1K</span>` : ''}
            </div>

            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
              <div style="display:flex; align-items:center; gap:14px;">
                <div class="ai-bot-square" style="width:48px; height:48px; font-size:22px;">✦</div>
                <div>
                  <h1 class="agent-title" style="font-size: clamp(24px, 2.7vw, 34px); margin: 0;">${ag.categoryDisplayName || ag.name}</h1>
                  <div style="font-size:14.5px; color:var(--text-secondary); margin-top:4px;">${shortSentence(ag.categorizedDescription || ag.shortDesc, 175)}</div>
                </div>
              </div>"""
    new_agent_hdr = """            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
              <div style="display:flex; align-items:center; gap:14px;">
                <div class="ai-bot-square" style="width:48px; height:48px; font-size:22px;">✦</div>
                <div>
                  <h1 class="agent-title" style="font-size: clamp(24px, 2.7vw, 34px); margin: 0;">${cleanAgentName(ag.name)}</h1>
                  <div style="font-size:14.5px; color:var(--text-secondary); margin-top:4px; font-weight:600;">${ag.subPillarName || dept.name}</div>
                </div>
              </div>"""
    if old_agent_hdr in text:
        text = text.replace(old_agent_hdr, new_agent_hdr, 1)

    # 9. Clean up Value Chain Stage Owner & Agent Cards (`openValueChainPage`)
    old_vc_cards = """                    <div>
                      <div class="human-role-tag">👤 Stage Owner (Human Persona)</div>
                      <div class="human-persona-title" style="font-size:16px;">${ownerPersona.name}</div>
                      <div class="human-persona-sub" style="font-size:12px;">${ownerPersona.role}</div>
                    </div>"""
    new_vc_cards = """                    <div>
                      <div class="human-persona-title" style="font-size:16px;">${ownerPersona.name}</div>
                      <div class="human-persona-sub" style="font-size:12px;">${ownerPersona.subPillarName || ownerDept.name}</div>
                    </div>"""
    if old_vc_cards in text:
        text = text.replace(old_vc_cards, new_vc_cards, 1)

    old_vc_ag = """                    <div>
                      <div style="display:flex; align-items:center; gap:6px; margin-bottom:3px;">
                        <span class="ai-agent-type-tag">✦ Stage AI Agent</span>
                        <span class="build-tier-badge ${stageAgentCls.cssClass}" style="font-size:9.5px; padding:1px 7px;">${stageAgentCls.tier}</span>
                      </div>
                      <div class="ai-agent-chip-title" style="font-size:16px;">${stageAgent.name}</div>
                    </div>"""
    new_vc_ag = """                    <div>
                      <div class="ai-agent-chip-title" style="font-size:16px;">${cleanAgentName(stageAgent.name)}</div>
                      <div style="font-size:12px; color:var(--text-secondary); margin-top:2px;">${stageAgent.subPillarName || ownerDept.name}</div>
                    </div>"""
    if old_vc_ag in text:
        text = text.replace(old_vc_ag, new_vc_ag, 1)

    # 10. Clean up Mind Map Agent & Persona Cards (`openMindMapPage`)
    old_mm_agent = """                          <div>
                            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:4px;">
                              <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; padding:2px 8px; border-radius:6px; background:${spColor}22; color:${spColor}; border:1px solid ${spColor}55;">
                                A-${m.code} · ${m.sym}
                              </span>
                              <span class="build-tier-badge ${cls.cssClass}" style="font-size:10.5px; padding:2px 8px;">${cls.label}</span>
                              <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:#10b981;">✦ ${ag.badge}</span>
                              ${ag.costModel ? `
                                <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; padding:2px 8px; border-radius:6px; background:rgba(2,132,199,0.14); color:#0284c7; border:1px solid rgba(2,132,199,0.35);">
                                  💰 $${ag.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo · $${ag.costModel.monthlyBreakdown.blendedCostPer1kCallsUsd.toFixed(2)}/1K · 📈 $${(ag.costModel.valueModel.grossAnnualConservativeUsd/1e6).toFixed(2)}M/yr (${ag.costModel.valueModel.cloudRoiMultipleConservative}x ROI)
                                </span>
                              ` : ''}
                            </div>
                            <div style="font-family:var(--font-display); font-size:18px; font-weight:800; color:var(--text-primary);">
                              ${ag.name}
                            </div>
                          </div>"""
    new_mm_agent = """                          <div>
                            <div style="font-family:var(--font-display); font-size:18px; font-weight:800; color:var(--text-primary);">
                              ${cleanAgentName(ag.name)}
                            </div>
                            <div style="font-size:13px; color:var(--text-secondary); margin-top:2px;">
                              ${ag.subPillarName || activeDept.name}
                            </div>
                          </div>"""
    if old_mm_agent in text:
        text = text.replace(old_mm_agent, new_mm_agent, 1)

    old_mm_persona = """                              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:3px;">
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
                              </div>"""
    new_mm_persona = """                              <div style="font-family:var(--font-display); font-size:17.5px; font-weight:800; color:var(--text-primary);">
                                ${p.name}
                              </div>
                              <div style="font-size:13px; color:var(--text-secondary); margin-top:2px;">
                                ${p.subPillarName || activeDept.name}
                              </div>"""
    if old_mm_persona in text:
        text = text.replace(old_mm_persona, new_mm_persona, 1)

    path.write_text(text, encoding="utf-8")
    print(f"Updated {path.name} ({len(text):,} bytes)")


def main() -> None:
    for hp in HTML_FILES:
        if hp.exists():
            update_html_file(hp)


if __name__ == "__main__":
    main()

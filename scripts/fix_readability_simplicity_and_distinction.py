#!/usr/bin/env python3
"""Fixes Periodic Table & Mind Map text contrast/readability in both Light & Dark themes,
simplifies Personas & Agents pages (Name-first, click to expand details), and introduces a
clear visual & structural distinction between Human Persona cards and AI Agent cards."""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD_SITE = ROOT / "build_site.py"


ADDITIONAL_DISTINCTION_AND_READABILITY_CSS = """
    /* =========================================================================
       UNMISTAKABLE VISUAL DISTINCTION: HUMAN PERSONAS VS. AI AGENTS
       ========================================================================= */
    /* 1. HUMAN PERSONA CARD: Warm/Solid Executive Role Card with Circular Avatar & Left Pillar Bar */
    .human-persona-card {
      position: relative;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 18px 22px;
      border-radius: 16px;
      background: linear-gradient(145deg, rgba(17, 25, 40, 0.96) 0%, rgba(11, 17, 30, 0.98) 100%);
      border: 1.5px solid rgba(255, 255, 255, 0.14);
      border-left: 6px solid var(--dept-accent, #2e8b57);
      box-shadow: 0 10px 26px rgba(0, 0, 0, 0.32);
      cursor: pointer;
      transition: transform 0.28s cubic-bezier(0.22, 1, 0.36, 1),
                  box-shadow 0.28s cubic-bezier(0.22, 1, 0.36, 1),
                  border-color 0.22s ease,
                  background 0.22s ease;
    }

    .human-persona-card:hover {
      transform: translateY(-6px) scale(1.015);
      border-color: var(--dept-accent, #2e8b57);
      box-shadow: 0 18px 38px rgba(0, 0, 0, 0.48), 0 0 0 1px var(--dept-accent, #2e8b57);
    }

    .human-avatar-circle {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.08);
      border: 2px solid var(--dept-accent, #2e8b57);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      flex-shrink: 0;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }

    .human-role-tag {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 2px 8px;
      border-radius: 6px;
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      background: rgba(251, 188, 4, 0.16);
      color: #fbbc04;
      border: 1px solid rgba(251, 188, 4, 0.4);
      margin-bottom: 4px;
    }

    .human-persona-title {
      font-family: var(--font-display);
      font-size: 18px;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.25;
    }

    .human-persona-sub {
      font-size: 13px;
      color: #cbd5e1;
      margin-top: 2px;
      font-weight: 500;
    }

    /* 2. AI AGENT CARD: Distinct Indigo/Violet Tech Module with Hex/Square Bot Badge */
    .ai-agent-dock-box {
      margin-top: 22px;
      padding: 18px 20px;
      border-radius: 16px;
      background: rgba(30, 27, 75, 0.28);
      border: 1px dashed rgba(129, 140, 248, 0.45);
    }

    .ai-agent-chip-card {
      position: relative;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 13px 16px;
      border-radius: 12px;
      background: linear-gradient(135deg, rgba(23, 27, 54, 0.95) 0%, rgba(15, 20, 40, 0.98) 100%);
      border: 1.5px solid rgba(99, 102, 241, 0.42);
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.28);
      cursor: pointer;
      transition: transform 0.26s cubic-bezier(0.22, 1, 0.36, 1),
                  box-shadow 0.26s cubic-bezier(0.22, 1, 0.36, 1),
                  border-color 0.22s ease,
                  background 0.22s ease;
    }

    .ai-agent-chip-card:hover {
      transform: translateY(-4px) scale(1.012);
      border-color: #818cf8;
      background: linear-gradient(135deg, rgba(30, 36, 72, 0.98) 0%, rgba(20, 26, 52, 1) 100%);
      box-shadow: 0 14px 30px rgba(99, 102, 241, 0.28);
    }

    .ai-bot-square {
      width: 36px;
      height: 36px;
      border-radius: 9px;
      background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
      color: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      font-weight: 800;
      flex-shrink: 0;
      box-shadow: 0 4px 10px rgba(79, 70, 229, 0.35);
    }

    .ai-agent-type-tag {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 2px 7px;
      border-radius: 5px;
      font-family: var(--font-mono);
      font-size: 9.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      background: rgba(99, 102, 241, 0.2);
      color: #a5b4fc;
      border: 1px solid rgba(99, 102, 241, 0.45);
    }

    .ai-agent-chip-title {
      font-family: var(--font-display);
      font-size: 15.5px;
      font-weight: 800;
      color: #f8fafc;
      line-height: 1.25;
    }

    /* Click-to-Expand Persona Journey Accordion Step */
    .journey-accordion-item {
      border-radius: 16px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      margin-bottom: 12px;
      overflow: hidden;
      transition: border-color 0.24s ease, box-shadow 0.24s ease, transform 0.24s ease;
    }

    .journey-accordion-item:hover {
      border-color: var(--dept-accent, #1a73e8);
      box-shadow: 0 8px 22px rgba(0, 0, 0, 0.22);
    }

    .journey-accordion-header {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 16px 22px;
      cursor: pointer;
      text-align: left;
      background: transparent;
    }

    .journey-accordion-body {
      display: none;
      padding: 0 22px 20px;
      border-top: 1px solid var(--border-subtle);
      animation: dropdownUnroll 0.26s var(--ease-spring) forwards;
    }

    .journey-accordion-item.open .journey-accordion-body {
      display: block;
    }

    .journey-accordion-chevron {
      font-size: 13px;
      font-weight: 800;
      color: var(--text-secondary);
      padding: 5px 12px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border-subtle);
      transition: transform 0.25s ease, background 0.25s ease, color 0.25s ease;
    }

    .journey-accordion-item.open .journey-accordion-chevron {
      background: var(--dept-accent, #1a73e8);
      color: #ffffff;
      border-color: var(--dept-accent, #1a73e8);
    }

    /* =========================================================================
       PERIODIC TABLE & MIND MAP HIGH-CONTRAST READABILITY CLASSES (BOTH THEMES)
       ========================================================================= */
    .pt-page-title,
    .mm-page-title {
      font-family: var(--font-display);
      font-size: clamp(28px, 3vw, 38px);
      font-weight: 800;
      letter-spacing: -0.025em;
      color: #ffffff;
      margin-bottom: 6px;
    }

    .pt-page-sub,
    .mm-page-sub {
      font-size: 15px;
      color: #cbd5e1;
      line-height: 1.55;
      max-width: 920px;
    }

    .pt-domain-heading {
      color: #f1f5f9 !important;
      font-weight: 800 !important;
    }

    .pt-domain-count {
      color: #94a3b8 !important;
      font-weight: 700 !important;
    }

    .pt-tile-title {
      color: #ffffff !important;
      font-weight: 700 !important;
    }

    .pt-side-title {
      font-family: var(--font-display);
      font-size: 18px;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.25;
    }

    .pt-side-sub {
      font-family: var(--font-mono);
      font-size: 12px;
      color: #cbd5e1;
      margin-top: 3px;
      font-weight: 600;
    }

    .pt-side-desc {
      font-size: 14px;
      color: #e2e8f0;
      line-height: 1.58;
      margin-bottom: 14px;
    }

    .mm-node-title {
      font-size: 14.5px;
      font-weight: 700;
      color: #ffffff;
      margin-top: 2px;
    }

    .mm-node-sub {
      font-size: 12px;
      color: #cbd5e1;
      margin-top: 2px;
      font-weight: 500;
    }

    .mm-node-meta {
      font-family: var(--font-mono);
      font-size: 11.5px;
      color: #e2e8f0;
      font-weight: 600;
    }

    /* =========================================================================
       LIGHT THEME OVERRIDES FOR PERSONA VS AGENT DISTINCTION & PT/MM READABILITY
       ========================================================================= */
    html[data-theme="light"] .human-persona-card {
      background: #ffffff;
      border: 1.5px solid #cbd5e1;
      border-left: 6px solid var(--dept-accent, #2e8b57);
      box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
    }

    html[data-theme="light"] .human-persona-card:hover {
      background: #ffffff;
      border-color: var(--dept-accent, #2e8b57);
      box-shadow: 0 16px 34px rgba(26, 115, 232, 0.16);
    }

    html[data-theme="light"] .human-avatar-circle {
      background: #f8fafc;
      border: 2px solid var(--dept-accent, #2e8b57);
      box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08);
    }

    html[data-theme="light"] .human-role-tag {
      background: #fef3c7;
      color: #b45309;
      border: 1px solid #fcd34d;
    }

    html[data-theme="light"] .human-persona-title {
      color: #111827 !important;
    }

    html[data-theme="light"] .human-persona-sub {
      color: #374151 !important;
    }

    html[data-theme="light"] .ai-agent-dock-box {
      background: #eef2ff;
      border: 1.5px dashed #818cf8;
    }

    html[data-theme="light"] .ai-agent-chip-card {
      background: linear-gradient(135deg, #ffffff 0%, #f5f3ff 100%);
      border: 1.5px solid #818cf8;
      box-shadow: 0 4px 12px rgba(79, 70, 229, 0.08);
    }

    html[data-theme="light"] .ai-agent-chip-card:hover {
      background: #ffffff;
      border-color: #4f46e5;
      box-shadow: 0 14px 28px rgba(79, 70, 229, 0.20);
    }

    html[data-theme="light"] .ai-agent-type-tag {
      background: #e0e7ff;
      color: #3730a3;
      border: 1px solid #a5b4fc;
    }

    html[data-theme="light"] .ai-agent-chip-title {
      color: #1e1b4b !important;
    }

    html[data-theme="light"] .journey-accordion-item {
      background: #ffffff;
      border: 1px solid #cbd5e1;
      box-shadow: 0 3px 10px rgba(15, 23, 42, 0.04);
    }

    html[data-theme="light"] .journey-accordion-chevron {
      background: #f1f5f9;
      color: #1e293b;
      border-color: #cbd5e1;
    }

    /* High-Contrast Periodic Table & Mind Map in Light Theme */
    html[data-theme="light"] .pt-page-title,
    html[data-theme="light"] .mm-page-title,
    html[data-theme="light"] .pt-side-title,
    html[data-theme="light"] .mm-node-title,
    html[data-theme="light"] .pt-tile-title,
    html[data-theme="light"] .pt-domain-heading {
      color: #111827 !important;
    }

    html[data-theme="light"] .pt-page-sub,
    html[data-theme="light"] .mm-page-sub,
    html[data-theme="light"] .pt-side-desc,
    html[data-theme="light"] .mm-node-sub,
    html[data-theme="light"] .pt-legend-list,
    html[data-theme="light"] .pt-legend-row {
      color: #1f2937 !important;
      font-weight: 500;
    }

    html[data-theme="light"] .pt-side-sub,
    html[data-theme="light"] .mm-node-meta,
    html[data-theme="light"] .pt-domain-count,
    html[data-theme="light"] .pt-legend-title,
    html[data-theme="light"] .mm-col-header {
      color: #374151 !important;
      font-weight: 700 !important;
    }

    html[data-theme="light"] .pt-tab-btn {
      background: #ffffff;
      border: 1px solid #cbd5e1;
      color: #1f2937 !important;
      font-weight: 700;
    }

    html[data-theme="light"] .pt-tab-btn:hover {
      background: #e8f0fe;
      border-color: #1a73e8;
      color: #1a73e8 !important;
    }

    html[data-theme="light"] .pt-tab-btn.active {
      background: #1a73e8;
      border-color: #1a73e8;
      color: #ffffff !important;
    }

    html[data-theme="light"] .pt-stat-badge {
      background: #ffffff;
      border: 1px solid #cbd5e1;
      color: #374151 !important;
      font-weight: 600;
    }

    html[data-theme="light"] .pt-stat-badge strong {
      color: #111827 !important;
    }

    html[data-theme="light"] .pt-side-tag {
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      color: #1e293b !important;
      font-weight: 700;
    }

    /* Catch-all for any inline light/grey text inside #pagePeriodic and #pageMindMap in Light Theme */
    html[data-theme="light"] #pagePeriodic h1,
    html[data-theme="light"] #pagePeriodic h2,
    html[data-theme="light"] #pagePeriodic h3,
    html[data-theme="light"] #pageMindMap h1,
    html[data-theme="light"] #pageMindMap h2,
    html[data-theme="light"] #pageMindMap h3,
    html[data-theme="light"] #pagePeriodic strong,
    html[data-theme="light"] #pageMindMap strong {
      color: #111827 !important;
    }

    html[data-theme="light"] #pagePeriodic p,
    html[data-theme="light"] #pageMindMap p {
      color: #1f2937 !important;
    }
"""


NEW_SHOWCASE_BOX_JS = """    function renderDepartmentShowcaseBox() {
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

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap:14px;">
              ${dept.personaIds.map(pid => {
                const p = PERSONAS[pid];
                if (!p) return '';
                return `
                  <div class="human-persona-card" style="--dept-accent: ${dept.color};" onclick="openPersonaPage('${p.id}', true, event)">
                    <div style="display:flex; align-items:center; gap:14px; min-width:0;">
                      <div class="human-avatar-circle" style="--dept-accent: ${dept.color};">${p.icon}</div>
                      <div style="min-width:0;">
                        <div class="human-role-tag">👤 Human Role</div>
                        <div class="human-persona-title">${p.name}</div>
                        <div class="human-persona-sub">${p.role}</div>
                      </div>
                    </div>
                    <span class="persona-open-arrow" style="color:${dept.color}; font-size:18px; font-weight:800;">&rarr;</span>
                  </div>
                `;
              }).join('')}
            </div>
          </div>

          <!-- SECTION 2: VISUALLY DISTINCT AI AGENT DOCK (Indigo/Violet Tech Chips) -->
          <div class="ai-agent-dock-box">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-bottom:12px;">
              <div style="display:flex; align-items:center; gap:10px;">
                <span style="padding:4px 10px; border-radius:8px; background:linear-gradient(135deg,#4f46e5,#7c3aed); color:#ffffff; font-size:11.5px; font-weight:800; letter-spacing:0.06em; text-transform:uppercase;">
                  ✦ AI Agents (${pillarAgents.length})
                </span>
                <span style="font-size:13.5px; font-weight:600; color:var(--text-secondary);">
                  Direct jump to AI agents in ${dept.name}
                </span>
              </div>
            </div>

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap:10px;">
              ${pillarAgents.map(ag => {
                const cls = getAgentBuildClassification(ag);
                return `
                  <div class="ai-agent-chip-card" onclick="openAgentPage('${ag.id}', true, event)">
                    <div style="display:flex; align-items:center; gap:12px; min-width:0;">
                      <div class="ai-bot-square">✦</div>
                      <div style="min-width:0;">
                        <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap; margin-bottom:3px;">
                          <span class="ai-agent-type-tag">AI AGENT</span>
                          <span class="build-tier-badge ${cls.cssClass}" style="font-size:9.5px; padding:1px 7px;">${cls.tier}</span>
                        </div>
                        <div class="ai-agent-chip-title">${ag.name}</div>
                      </div>
                    </div>
                    <span style="color:#6366f1; font-weight:800; font-size:16px;">&rarr;</span>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        </div>
      `;
    }"""


NEW_PERSONA_PAGE_SIMPLE_JS = """    function togglePersonaJourneyStep(stepElId) {
      const el = document.getElementById(stepElId);
      if (el) el.classList.toggle('open');
    }

    function openPersonaPage(personaId, pushHash = true, ev = null) {
      const p = PERSONAS[personaId];
      if (!p) return;
      const useSlide = isPillOrNavSwitch(ev);
      const sRect = useSlide ? null : getClickedCardRect(ev);
      const transClass = getPageTransitionClass(ev, sRect);

      lastPersonaId = personaId;
      selectedDeptId = p.deptId;
      const dept = getDeptMeta(p.deptId);

      if (pushHash) {
        history.pushState({ page: 'persona', id: personaId }, '', `#persona/${personaId}`);
      }

      // Track first toil index so only the first toil step is open by default (rest open on click!)
      let firstToilOpened = false;

      const container = document.getElementById('personaPageContent');
      container.innerHTML = `
        <div id="personaGenieWrap" class="${transClass}">
          <!-- Top Back & Switcher Bar -->
          <div class="back-bar">
            <button type="button" class="back-btn" onclick="goToOrgChart()">
              <span>&larr;</span>
              <span>Back to 6 Pillars (${dept.name})</span>
            </button>

            <div class="persona-switcher-pills">
              ${dept.personaIds.map(pid => {
                const other = PERSONAS[pid];
                if (!other) return '';
                return `
                  <button type="button"
                          class="switch-pill ${pid === p.id ? 'active' : ''}"
                          style="${pid === p.id ? `background:${dept.color}; border-color:${dept.color}; color:#ffffff; font-weight:700;` : ''}"
                          onclick="openPersonaPage('${pid}', true, event)">
                    ${other.icon} ${other.name}
                  </button>
                `;
              }).join('')}
            </div>
          </div>

          <!-- Clean, Compact Persona Header -->
          <div class="persona-header-card" style="padding: 24px 30px; margin-bottom: 22px;">
            ${renderSupplyChainWatermarkSvg(dept.watermarkType, dept.color, 'persona-header-sc-watermark')}

            <div style="position:relative; z-index:2; display:flex; align-items:center; gap:18px; flex-wrap:wrap;">
              <div class="human-avatar-circle" style="width:60px; height:60px; font-size:28px; --dept-accent:${dept.color};">
                ${p.icon}
              </div>
              <div>
                <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:6px;">
                  <span class="human-role-tag">👤 Human Persona</span>
                  <span class="persona-badge" style="margin-bottom:0; background: ${dept.color}18; color: ${dept.color}; border: 1px solid ${dept.color}45;">
                    ${dept.scorBadge || ''} · ${dept.name}
                  </span>
                </div>
                <h1 class="persona-page-title" style="margin-bottom:4px;">${p.name}</h1>
                <div style="font-size:15px; color:var(--text-secondary); font-weight:600;">${p.role}</div>
              </div>
            </div>

            <div class="persona-stat-highlight" style="border-color: ${dept.color}45;">
              <div class="persona-stat-value" style="color: ${dept.color};">${p.headlineStat || '-85% Toil'}</div>
              <div class="persona-stat-label">${p.toilHoursBefore || '6.5h'} &rarr; ${p.toilHoursAfter || '1.0h'}</div>
            </div>
          </div>

          <!-- Click-to-Expand Persona Daily Journey (Name First, Click for Red vs Green Details) -->
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom: 14px;">
            <div>
              <h2 class="block-title" style="border-left-color: ${dept.color}; margin-bottom:2px;">Persona Daily Journey</h2>
              <p class="block-subtitle" style="margin:0;">Click any daily task below to compare <strong style="color:#ea4335;">Manual Bottleneck (Red)</strong> vs. <strong style="color:#34a853;">With Gemini AI (Green)</strong>.</p>
            </div>
          </div>

          <div style="margin-bottom: 34px;">
            ${p.dayInLife.map((slot, idx) => {
              const stepId = `pStep_${p.id}_${idx}`;
              const plugAgent = slot.agentId ? AGENTS[slot.agentId] : null;
              const plugCls = plugAgent ? getAgentBuildClassification(plugAgent) : null;
              const isDefaultOpen = slot.isToil && !firstToilOpened;
              if (isDefaultOpen) firstToilOpened = true;

              return `
                <div id="${stepId}" class="journey-accordion-item ${isDefaultOpen ? 'open' : ''}" style="--dept-accent:${dept.color};">
                  <button type="button" class="journey-accordion-header" onclick="togglePersonaJourneyStep('${stepId}')">
                    <div style="display:flex; align-items:center; gap:14px; flex-wrap:wrap;">
                      <span class="time-badge" style="min-width:82px;">${slot.time}</span>
                      <span class="task-title" style="font-size:16.5px;">${slot.task}</span>
                      ${slot.isToil ? `
                        <span style="font-size:12px; font-weight:700; padding:3px 10px; border-radius:999px; background:rgba(52,168,83,0.14); color:#34a853; border:1px solid rgba(52,168,83,0.35);">
                          ${slot.toilDuration || '2.0 hrs'} &rarr; ${slot.afterDuration || '10 mins'}
                        </span>
                      ` : `
                        <span class="core-tag-pill">👤 ${slot.tag || 'Leadership'}</span>
                      `}
                    </div>

                    <div style="display:flex; align-items:center; gap:10px;">
                      ${plugAgent ? `
                        <span class="ai-agent-type-tag" style="padding:4px 9px; font-size:11px;" onclick="event.stopPropagation(); openAgentPage('${plugAgent.id}', true, event)">
                          ✦ ${plugAgent.name} &rarr;
                        </span>
                      ` : ''}
                      <span class="journey-accordion-chevron">Details ▾</span>
                    </div>
                  </button>

                  <div class="journey-accordion-body">
                    ${slot.isToil ? `
                      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap:14px; padding-top:14px;">
                        <div class="toil-highlight-box">
                          <div class="toil-top-bar">
                            <span class="toil-badge">✕ Manual Bottleneck</span>
                            <span class="toil-duration">${slot.toilDuration || '2.0 hrs'}</span>
                          </div>
                          <div class="toil-text">${shortSentence(slot.before, 115)}</div>
                        </div>

                        <div class="gemini-improve-box">
                          <div class="improve-top-bar">
                            <span class="improve-badge">✦ With Gemini AI</span>
                            <span class="improve-time-saved">${slot.toilDuration || '2.0 hrs'} &rarr; ${slot.afterDuration || '10 mins'}</span>
                          </div>
                          <div class="improve-text">${shortSentence(slot.after, 115)}</div>
                        </div>
                      </div>
                      ${plugAgent ? `
                        <div style="margin-top:12px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px;">
                          <span class="build-tier-badge ${plugCls.cssClass}">${plugCls.label}</span>
                          <button type="button" class="agent-plug-btn" onclick="openAgentPage('${plugAgent.id}', true, event)">
                            <span>Open ${plugAgent.name} Architecture &amp; Video</span>
                            <span>&rarr;</span>
                          </button>
                        </div>
                      ` : ''}
                    ` : `
                      <div style="padding-top:12px; font-size:14.5px; color:var(--text-secondary);">
                        ${shortSentence(slot.activity, 130)}
                      </div>
                    `}
                  </div>
                </div>
              `;
            }).join('')}
          </div>

          <!-- Visually Distinct AI Agents Dock for this Persona (Name + Tier Badge Only, Click to Open) -->
          <div class="ai-agent-dock-box">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-bottom:14px;">
              <div style="display:flex; align-items:center; gap:10px;">
                <span style="padding:4px 10px; border-radius:8px; background:linear-gradient(135deg,#4f46e5,#7c3aed); color:#ffffff; font-size:11.5px; font-weight:800; letter-spacing:0.06em; text-transform:uppercase;">
                  ✦ AI Agents for ${p.name}
                </span>
                <span style="font-size:13.5px; color:var(--text-secondary); font-weight:600;">
                  Click any AI agent to view its workflow diagram &amp; demo video
                </span>
              </div>
            </div>

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:12px;">
              ${[...new Set([...(p.agentIds || []), ...UNIVERSAL_AGENT_IDS])].map(aid => {
                const ag = AGENTS[aid];
                if (!ag) return '';
                const cls = getAgentBuildClassification(ag);
                return `
                  <div class="ai-agent-chip-card" onclick="openAgentPage('${ag.id}', true, event)">
                    <div style="display:flex; align-items:center; gap:12px; min-width:0;">
                      <div class="ai-bot-square">✦</div>
                      <div style="min-width:0;">
                        <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap; margin-bottom:3px;">
                          <span class="ai-agent-type-tag">${ag.isUniversal ? 'UNIVERSAL AI' : 'DOMAIN AI'}</span>
                          <span class="build-tier-badge ${cls.cssClass}" style="font-size:9.5px; padding:1px 7px;">${cls.tier}</span>
                        </div>
                        <div class="ai-agent-chip-title">${ag.name}</div>
                      </div>
                    </div>
                    <span style="color:#6366f1; font-weight:800; font-size:16px;">&rarr;</span>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        </div>
      `;

      hydrateAssets();
      showActivePage('pagePersona');
      const wrap = document.getElementById('personaGenieWrap');
      if (sRect && wrap) {
        animateGenieOutOfBox(sRect, wrap, dept.color);
      }
    }"""


NEW_DIRECTORY_SIMPLE_JS = """    let currentDirDeptFilter = 'all';
    let currentDirSearch = '';
    let currentDirMode = 'personas'; // 'personas' (29) | 'agents' (35)

    function renderDirectoryCardsHtml(deptFilter, searchQuery, mode = currentDirMode) {
      const q = (searchQuery || '').trim().toLowerCase();

      if (mode === 'agents') {
        const agentsList = Object.values(AGENTS).filter(ag => {
          if (deptFilter === 'universal' && !ag.isUniversal) return false;
          if (deptFilter !== 'all' && deptFilter !== 'universal' && ag.deptId !== deptFilter) return false;
          if (!q) return true;
          const dept = getDeptMeta(ag.deptId);
          const haystack = [ag.name, ag.shortDesc, dept ? dept.name : ''].join(' ').toLowerCase();
          return haystack.includes(q);
        });

        if (!agentsList.length) {
          return `<div style="grid-column: 1 / -1; padding: 36px; text-align: center; color: var(--text-secondary);">No matching agents found.</div>`;
        }

        return agentsList.map(ag => {
          const dept = getDeptMeta(ag.deptId);
          const cls = getAgentBuildClassification(ag);
          return `
            <div class="ai-agent-chip-card" style="padding:18px 20px;" onclick="openAgentPage('${ag.id}', true, event)">
              <div style="display:flex; align-items:center; gap:14px; min-width:0;">
                <div class="ai-bot-square" style="width:42px; height:42px; font-size:18px;">✦</div>
                <div style="min-width:0;">
                  <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap; margin-bottom:4px;">
                    <span class="ai-agent-type-tag">${ag.isUniversal ? 'UNIVERSAL CORE' : (dept.scorBadge || 'SCOR')}</span>
                    <span class="build-tier-badge ${cls.cssClass}" style="font-size:10px; padding:2px 8px;">
                      ${cls.shortLabel}
                    </span>
                  </div>
                  <div class="ai-agent-chip-title" style="font-size:17px;">${ag.name}</div>
                  <div style="font-size:12.5px; color:var(--text-secondary); margin-top:2px;">
                    ${ag.isUniversal ? 'All 6 SCOR Pillars' : dept.name}
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
        const haystack = [p.name, p.role, p.summary, dept ? dept.name : ''].join(' ').toLowerCase();
        return haystack.includes(q);
      });

      if (!personasList.length) {
        return `<div style="grid-column: 1 / -1; padding: 36px; text-align: center; color: var(--text-secondary);">No matching personas found.</div>`;
      }

      return personasList.map(p => {
        const dept = getDeptMeta(p.deptId);
        return `
          <div class="human-persona-card" style="--dept-accent: ${dept.color};" onclick="openPersonaPage('${p.id}', true, event)">
            <div style="display:flex; align-items:center; gap:14px; min-width:0;">
              <div class="human-avatar-circle" style="--dept-accent: ${dept.color};">${p.icon}</div>
              <div style="min-width:0;">
                <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap; margin-bottom:3px;">
                  <span class="human-role-tag">👤 Human Persona</span>
                  <span style="font-size:11px; font-weight:800; color:${dept.color}; text-transform:uppercase;">
                    ${dept.scorBadge || ''} · ${dept.name}
                  </span>
                </div>
                <div class="human-persona-title">${p.name}</div>
                <div class="human-persona-sub">${p.role}</div>
              </div>
            </div>
            <span class="persona-open-arrow" style="color:${dept.color}; font-size:18px; font-weight:800;">&rarr;</span>
          </div>
        `;
      }).join('');
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

      if (pushHash) {
        history.pushState({ page: 'directory', dept: currentDirDeptFilter, mode: currentDirMode }, '', '#directory');
      }

      const transClass = getPageTransitionClass(ev, null);
      const container = document.getElementById('directoryPageContent');
      container.innerHTML = `
        <div class="${transClass}">
          <div class="back-bar">
            <button type="button" class="back-btn" onclick="goToOrgChart()">
              <span>&larr;</span>
              <span>Back to 6 SCOR Pillars</span>
            </button>

            <div style="display:flex; gap:10px; flex-wrap:wrap;">
              <button type="button"
                      class="switch-pill ${currentDirMode === 'personas' ? 'active' : ''}"
                      style="${currentDirMode === 'personas' ? 'background:#d97706; color:#ffffff; border-color:#d97706; font-weight:800;' : ''}"
                      onclick="openPersonasDirectoryPage(currentDirDeptFilter === 'universal' ? 'all' : currentDirDeptFilter, currentDirSearch, false, 'personas', event)">
                👤 Human Personas (29)
              </button>
              <button type="button"
                      class="switch-pill ${currentDirMode === 'agents' ? 'active' : ''}"
                      style="${currentDirMode === 'agents' ? 'background:#4f46e5; color:#ffffff; border-color:#4f46e5; font-weight:800;' : ''}"
                      onclick="openPersonasDirectoryPage(currentDirDeptFilter, currentDirSearch, false, 'agents', event)">
                ✦ AI Agents (35)
              </button>
            </div>
          </div>

          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:14px; margin-bottom:18px;">
            <div>
              <h1 style="font-family:var(--font-display); font-size:clamp(26px, 2.8vw, 34px); font-weight:800; color:var(--text-primary); margin:0;">
                ${currentDirMode === 'agents' ? '✦ 35 Supply Chain AI Agents' : '👤 29 Supply Chain Human Personas'}
              </h1>
              <p style="font-size:14.5px; color:var(--text-secondary); margin:4px 0 0;">
                Click any ${currentDirMode === 'agents' ? 'AI agent to view its workflow diagram & demo video' : 'persona to view their daily Red vs. Green journey'}.
              </p>
            </div>
          </div>

          <!-- Clean Search & Pillar Filter Bar -->
          <div class="dir-controls-bar" style="padding:16px 20px; margin-bottom:24px;">
            <input type="search"
                   class="dir-search-input"
                   style="padding:10px 14px; font-size:14px;"
                   placeholder="🔍 Quick filter by name or pillar..."
                   value="${currentDirSearch}"
                   oninput="filterDirectoryLive(this.value)" />

            <div style="display:flex; gap:6px; flex-wrap:wrap;">
              <button type="button"
                      class="switch-pill ${currentDirDeptFilter === 'all' ? 'active' : ''}"
                      style="${currentDirDeptFilter === 'all' ? 'background:#1a73e8; color:#ffffff; border-color:#1a73e8; font-weight:700;' : ''}"
                      onclick="openPersonasDirectoryPage('all', currentDirSearch, false, currentDirMode, event)">
                All (${currentDirMode === 'agents' ? '35' : '29'})
              </button>
              ${currentDirMode === 'agents' ? `
                <button type="button"
                        class="switch-pill ${currentDirDeptFilter === 'universal' ? 'active' : ''}"
                        style="${currentDirDeptFilter === 'universal' ? 'background:#4f46e5; color:#ffffff; border-color:#4f46e5; font-weight:700;' : ''}"
                        onclick="openPersonasDirectoryPage('universal', currentDirSearch, false, 'agents', event)">
                  🌐 Universal (4)
                </button>
              ` : ''}
              ${Object.values(DEPARTMENTS).map(d => {
                const count = currentDirMode === 'agents'
                  ? Object.values(AGENTS).filter(a => !a.isUniversal && a.deptId === d.id).length
                  : d.personaIds.length;
                return `
                  <button type="button"
                          class="switch-pill ${currentDirDeptFilter === d.id ? 'active' : ''}"
                          style="${currentDirDeptFilter === d.id ? `background:${d.color}; color:#ffffff; border-color:${d.color}; font-weight:700;` : ''}"
                          onclick="openPersonasDirectoryPage('${d.id}', currentDirSearch, false, currentDirMode, event)">
                    ${d.scorBadge ? d.scorBadge.split('·')[1].trim() : d.name} (${count})
                  </button>
                `;
              }).join('')}
            </div>
          </div>

          <div id="dirPersonaGridEl" class="dir-persona-grid" style="grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 14px;">
            ${renderDirectoryCardsHtml(currentDirDeptFilter, currentDirSearch, currentDirMode)}
          </div>
        </div>
      `;

      hydrateAssets();
      showActivePage('pageDirectory');
    }"""


def fix_periodic_and_mindmap_inline_colors(text: str) -> str:
    """Replaces hardcoded light/grey inline styles inside openPeriodicTablePage and openMindMapPage
    with CSS variables so text is 100% crisp and readable in both Light and Dark themes."""
    start_marker = "    /* =========================================================================\n       PAGE 7: THE PERIODIC TABLE OF AGENTS"
    end_marker = "    /* =========================================================================\n       MULTI-PAGE SWITCHING & HISTORY HANDLING"

    idx1 = text.find(start_marker)
    idx2 = text.find(end_marker)
    if idx1 == -1 or idx2 == -1:
        raise RuntimeError("Could not locate Periodic Table / Mind Map section in build_site.py")

    section = text[idx1:idx2]

    # Replace inline text colors with theme-adaptive CSS variables
    replacements = [
        ("color:#ffffff;", "color:var(--text-primary);"),
        ("color:#fff;", "color:var(--text-primary);"),
        ("color:#f8fafc;", "color:var(--text-primary);"),
        ("color:#f1f5f9;", "color:var(--text-primary);"),
        ("color:#e2e8f0;", "color:var(--text-primary);"),
        ("color:#cbd5e1;", "color:var(--text-secondary);"),
        ("color:#94a3b8;", "color:var(--text-secondary);"),
        ("color:#64748b;", "color:var(--text-secondary);"),
        ("color:#7dd3fc;", "color:var(--g-blue);"),
        ("color:#60a5fa;", "color:var(--g-blue);"),
        ("color:#6ee7b7;", "color:#2e8b57;"),
        ("color:#34d399;", "color:#2e8b57;"),
        ("color:#fca5a5;", "color:#c53929;"),
        ("color:#c084fc;", "color:#7e57c2;"),
        ("color:#e9d5ff;", "color:#7e57c2;"),
        ("background:rgba(255,255,255,0.03);", "background:var(--bg-surface);"),
        ("border:1px solid rgba(255,255,255,0.08);", "border:1px solid var(--border-subtle);"),
        ("border:1px solid rgba(255,255,255,0.07);", "border:1px solid var(--border-subtle);"),
        ("border-top:1px solid rgba(255,255,255,0.08);", "border-top:1px solid var(--border-subtle);"),
        ("border-bottom:1px solid rgba(255,255,255,0.1);", "border-bottom:1px solid var(--border-subtle);"),
        ("border-bottom: 1px solid rgba(255,255,255,0.10);", "border-bottom: 1px solid var(--border-subtle);"),
    ]
    for old, new in replacements:
        section = section.replace(old, new)

    # Also update PERIODIC_GROUPS colors to match the Google Brand palette
    section = section.replace("color: '#10b981'", "color: '#2e8b57'")
    section = section.replace("color: '#a142f4'", "color: '#7e57c2'")
    section = section.replace("color: '#3b82f6'", "color: '#3b78e7'")
    section = section.replace("color: '#00d2ff'", "color: '#00897b'")
    section = section.replace("color: '#ff8c00'", "color: '#d97706'")
    section = section.replace("color: '#ec4899'", "color: '#c53929'")
    section = section.replace("color: '#38bdf8'", "color: '#1a73e8'")

    return text[:idx1] + section + text[idx2:]


def main():
    text = BUILD_SITE.read_text(encoding="utf-8")

    # 1. Inject the new CSS classes before </style>
    if "UNMISTAKABLE VISUAL DISTINCTION: HUMAN PERSONAS VS. AI AGENTS" not in text:
        text = text.replace("  </style>", ADDITIONAL_DISTINCTION_AND_READABILITY_CSS + "\n  </style>", 1)

    # 2. Replace renderDepartmentShowcaseBox() with the new distinct Persona vs. AI Agent layout
    showcase_pattern = re.compile(
        r"    function renderDepartmentShowcaseBox\(\) \{.*?\n    \}\n\n    /\* =========================================================================\n       EXECUTIVE SELLING METADATA HELPER",
        re.DOTALL,
    )
    if not showcase_pattern.search(text):
        raise RuntimeError("Could not find renderDepartmentShowcaseBox in build_site.py")
    text = showcase_pattern.sub(
        NEW_SHOWCASE_BOX_JS
        + "\n\n    /* =========================================================================\n       EXECUTIVE SELLING METADATA HELPER",
        text,
        count=1,
    )

    # 3. Replace openPersonaPage() with the simplified Name-first click-to-expand journey + distinct AI Agent dock
    persona_pattern = re.compile(
        r"    function openPersonaPage\(personaId, pushHash = true, ev = null\) \{.*?\n    \}\n\n    /\* =========================================================================\n       AGENT ARCHITECTURE BLUEPRINT HELPER",
        re.DOTALL,
    )
    if not persona_pattern.search(text):
        raise RuntimeError("Could not find openPersonaPage in build_site.py")
    text = persona_pattern.sub(
        NEW_PERSONA_PAGE_SIMPLE_JS
        + "\n\n    /* =========================================================================\n       AGENT ARCHITECTURE BLUEPRINT HELPER",
        text,
        count=1,
    )

    # 4. Also simplify the Agent Page header so it shows Name + Badges first, with a click-to-expand Details drawer for the description
    old_agent_banner = """            <h1 class="agent-title" style="font-size: clamp(28px, 3.2vw, 40px); margin-bottom: 10px;">${ag.name}</h1>
            <p class="agent-subtitle" style="font-size: 16.5px;">
              ${shortSentence(ag.shortDesc, 175)} ${shortSentence(ag.solution, 175)}
            </p>"""
    new_agent_banner = """            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
              <div style="display:flex; align-items:center; gap:14px;">
                <div class="ai-bot-square" style="width:48px; height:48px; font-size:22px;">✦</div>
                <div>
                  <h1 class="agent-title" style="font-size: clamp(26px, 3vw, 36px); margin: 0;">${ag.name}</h1>
                  <div style="font-size:14.5px; color:var(--text-secondary); margin-top:3px;">${shortSentence(ag.shortDesc, 115)}</div>
                </div>
              </div>
              <button type="button" class="switch-pill" onclick="togglePersonaJourneyStep('agentMoreDetailsDrawer')">
                ▾ Click for Problem &amp; Outcome Details
              </button>
            </div>
            <div id="agentMoreDetailsDrawer" class="journey-accordion-item" style="margin-top:14px; margin-bottom:0;">
              <div class="journey-accordion-body" style="padding:16px 18px;">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:14px;">
                  <div class="toil-highlight-box">
                    <div class="toil-top-bar"><span class="toil-badge">✕ Problem Solved</span></div>
                    <div class="toil-text">${shortSentence(ag.problem, 130)}</div>
                  </div>
                  <div class="gemini-improve-box">
                    <div class="improve-top-bar"><span class="improve-badge">✦ Agentic Solution &amp; Outcome</span></div>
                    <div class="improve-text">${shortSentence(ag.solution, 110)} ${shortSentence(ag.outcome, 110)}</div>
                  </div>
                </div>
              </div>
            </div>"""
    if old_agent_banner in text:
        text = text.replace(old_agent_banner, new_agent_banner, 1)

    # 5. Replace the Directory Page (openPersonasDirectoryPage) with the clean Name-First cards & distinct Persona vs. Agent styling
    dir_pattern = re.compile(
        r"    let currentDirDeptFilter = 'all';.*?showActivePage\('pageDirectory'\);\n    \}",
        re.DOTALL,
    )
    if not dir_pattern.search(text):
        raise RuntimeError("Could not find openPersonasDirectoryPage section in build_site.py")
    text = dir_pattern.sub(NEW_DIRECTORY_SIMPLE_JS, text, count=1)

    # 6. Fix all grey/unreadable inline text inside Periodic Table and Mind Map
    text = fix_periodic_and_mindmap_inline_colors(text)

    BUILD_SITE.write_text(text, encoding="utf-8")
    print("Successfully updated build_site.py with high-contrast Periodic Table & Mind Map text, Name-First click-to-expand Personas & Agents pages, and distinct Human Persona vs. AI Agent card designs!")


if __name__ == "__main__":
    main()

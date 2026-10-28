#!/usr/bin/env python3
"""
Updates index.html, periodic_table.html, and mind_map.html from the clean 05f074b baseline to:
1. Keep 100% of the Enterprise Agent Contract & Technical Specification information
   (01 Playbook & Governance with 1A/1B/1C, 02 Workflow, 03 Agent Tools, 04 Source Systems,
   05 Data Model, 06 Evals & Proof + 8-KPI Quick Stats), wrapped under ONE single clean
   expandable tab/drawer on the main Agent page (collapsed by default on the main Agent page,
   and open inside once expanded so zero information is removed).
2. Fix all sharp corners across buttons, badges, pills, headers, and boxes (including
   .agent-plug-btn "Open ... & Demo ->", .journey-accordion-header, .time-badge, .toil-badge,
   .improve-badge, .core-tag-pill, .btn-generate-twin, .adk-demo-tab-btn, .xyz-lake-tab-btn).
3. Make text bigger, more readable, and more spacious across the entire website — especially
   the Persona Day-to-Day Life Comparison (Persona Daily Journey) and Process Stage Comparisons,
   removing mid-sentence truncations so full Before vs. After comparisons are clear and legible.
"""

from pathlib import Path

ROOT = Path("/usr/local/google/home/zuhaibp/Supply_chain_Agentic_Transformation")
HTML_FILES = [
    ROOT / "index.html",
    ROOT / "periodic_table.html",
    ROOT / "mind_map.html",
]

SPACIOUS_AND_ROUNDED_CSS = """
    /* =========================================================================
       MILD ROUNDED EDGES, BIG READABLE TYPOGRAPHY & SINGLE MASTER CONTRACT TAB
       ========================================================================= */
    .agent-plug-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      border-radius: 12px !important;
      padding: 12px 22px;
      font-family: var(--font-sans);
      font-size: 14.5px;
      font-weight: 700;
      line-height: 1.25;
      cursor: pointer;
      text-decoration: none;
      background: rgba(59, 130, 246, 0.14);
      border: 1.5px solid rgba(59, 130, 246, 0.45);
      color: #60a5fa;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      white-space: nowrap;
    }

    .agent-plug-btn:hover {
      background: #2563eb;
      border-color: #2563eb;
      color: #ffffff;
      transform: translateY(-1px);
      box-shadow: 0 8px 20px rgba(37, 99, 235, 0.28);
    }

    html[data-theme="light"] .agent-plug-btn {
      background: #e8f0fe;
      border: 1.5px solid #8ab4f8;
      color: #1967d2;
      border-radius: 12px !important;
    }

    html[data-theme="light"] .agent-plug-btn:hover {
      background: #1a73e8;
      border-color: #1a73e8;
      color: #ffffff;
      box-shadow: 0 8px 20px rgba(26, 115, 232, 0.22);
    }

    /* Universal mild rounded corners for badges, pills, headers, and buttons */
    .time-badge {
      border-radius: 10px !important;
      padding: 6px 14px !important;
      font-size: 13.5px !important;
      font-weight: 800 !important;
    }

    .core-tag-pill,
    .toil-badge,
    .improve-badge,
    .toil-duration,
    .improve-time-saved,
    .ai-agent-type-tag,
    .journey-accordion-chevron,
    .subagent-tag,
    .pt-tab-count {
      border-radius: 999px !important;
    }

    .toil-badge,
    .improve-badge {
      padding: 5px 14px !important;
      font-size: 13px !important;
      font-weight: 800 !important;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    .toil-duration,
    .improve-time-saved {
      padding: 5px 14px !important;
      font-size: 13.5px !important;
      font-weight: 800 !important;
    }

    .btn-generate-twin,
    .adk-demo-tab-btn,
    .xyz-lake-tab-btn {
      border-radius: 12px !important;
    }

    .twin-preset-card,
    .mm-agent-neural-header,
    .mm-neural-col-header,
    .video-placeholder-stage {
      border-radius: 16px !important;
    }

    /* Spacious, Big-Text Persona Day-to-Day Life Comparison & Accordion Items */
    .journey-accordion-item {
      border-radius: 18px !important;
      margin-bottom: 16px !important;
      overflow: hidden;
    }

    .journey-accordion-header {
      border-radius: 18px !important;
      padding: 20px 26px !important;
    }

    .journey-accordion-header .task-title {
      font-size: 18.5px !important;
      font-weight: 800 !important;
      line-height: 1.35 !important;
    }

    .journey-accordion-body {
      padding: 6px 26px 26px !important;
    }

    .toil-highlight-box,
    .gemini-improve-box {
      border-radius: 16px !important;
      padding: 22px 26px !important;
    }

    .toil-top-bar,
    .improve-top-bar {
      margin-bottom: 12px !important;
      padding-bottom: 10px !important;
    }

    .toil-text,
    .improve-text {
      font-size: 16px !important;
      line-height: 1.72 !important;
    }

    .persona-step-agent-box {
      border-radius: 16px !important;
      padding: 20px 24px !important;
      margin-top: 18px !important;
      gap: 18px !important;
    }

    .ai-agent-dock-box {
      border-radius: 22px !important;
      padding: 26px 30px !important;
    }

    .persona-agent-dock-card {
      border-radius: 18px !important;
      padding: 22px 24px !important;
      gap: 16px !important;
    }

    /* Execution Flow 5-Step Cards: Spacious & Zero Text Clipping */
    .ag-flow-steps-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(215px, 1fr)) !important;
      gap: 16px !important;
      margin-top: 18px !important;
    }

    .ag-flow-step-card {
      border-radius: 16px !important;
      padding: 18px 20px !important;
      min-width: 0;
    }

    .ag-flow-step-title {
      font-size: 16px !important;
      line-height: 1.35 !important;
      overflow-wrap: break-word;
    }

    .ag-flow-step-desc {
      font-size: 14px !important;
      line-height: 1.62 !important;
    }

    .ag-flow-mini-chip {
      border-radius: 8px !important;
      font-size: 11.5px !important;
      padding: 4px 9px !important;
      max-width: 100%;
      overflow-wrap: anywhere;
      white-space: normal !important;
    }

    /* Single Expandable Master Tab for Enterprise Agent Contract & Technical Spec */
    details.sc-master-contract-drawer {
      margin-top: 24px;
      margin-bottom: 28px;
      border-radius: 20px;
      background: var(--bg-card);
      border: 1.5px solid var(--border-subtle);
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.16);
      overflow: hidden;
      transition: all 0.25s ease;
    }

    html[data-theme="light"] details.sc-master-contract-drawer {
      background: #ffffff;
      border-color: #cbd5e1;
      box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
    }

    details.sc-master-contract-drawer > summary.sc-master-contract-summary {
      list-style: none;
      cursor: pointer;
      user-select: none;
      padding: 24px 30px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
      flex-wrap: wrap;
      background: linear-gradient(145deg, rgba(15, 23, 42, 0.85), rgba(9, 13, 22, 0.92));
      transition: background 0.2s ease;
    }

    html[data-theme="light"] details.sc-master-contract-drawer > summary.sc-master-contract-summary {
      background: linear-gradient(145deg, #f8fafc, #eff6ff);
    }

    details.sc-master-contract-drawer > summary.sc-master-contract-summary::-webkit-details-marker {
      display: none;
    }

    details.sc-master-contract-drawer[open] > summary.sc-master-contract-summary {
      border-bottom: 1px solid var(--border-subtle);
    }

    .sc-master-contract-toggle-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 11px 20px;
      border-radius: 999px;
      font-family: var(--font-sans);
      font-size: 13.5px;
      font-weight: 800;
      background: rgba(59, 130, 246, 0.15);
      border: 1.5px solid rgba(59, 130, 246, 0.45);
      color: var(--text-primary);
      transition: all 0.2s ease;
    }

    details.sc-master-contract-drawer > summary.sc-master-contract-summary:hover .sc-master-contract-toggle-btn {
      background: #2563eb;
      border-color: #2563eb;
      color: #ffffff;
    }

    .sc-master-contract-toggle-btn::before {
      content: '▾ Expand Enterprise Agent Contract & Full Specs (6 Sections)';
    }

    details.sc-master-contract-drawer[open] .sc-master-contract-toggle-btn::before {
      content: '▴ Hide Enterprise Agent Contract & Full Specs';
    }

    .sc-master-contract-body {
      padding: 24px 28px 30px;
    }

    /* Spacious typography inside the 6 Enterprise Agent Contract Sections */
    .sc-spec-section-card {
      border-radius: 18px !important;
      margin-bottom: 20px !important;
    }

    .sc-spec-sec-head {
      padding: 20px 26px !important;
    }

    .sc-spec-sec-title {
      font-size: 21px !important;
    }

    .sc-spec-sec-body {
      padding: 22px 26px 26px !important;
    }

    .sc-spec-sub-drawer {
      border-radius: 14px !important;
      margin-bottom: 14px !important;
    }

    .sc-spec-sub-drawer > summary {
      padding: 15px 20px !important;
      font-size: 15px !important;
    }

    .sc-spec-sub-drawer-body {
      padding: 18px 22px 22px !important;
    }

    .sc-spec-scope-col {
      border-radius: 14px !important;
      padding: 20px 22px !important;
    }

    .sc-spec-scope-list li {
      font-size: 15px !important;
      line-height: 1.68 !important;
      margin-bottom: 10px !important;
    }

    .sc-spec-table th {
      font-size: 12.5px !important;
      padding: 13px 16px !important;
    }

    .sc-spec-table td {
      font-size: 14.5px !important;
      line-height: 1.62 !important;
      padding: 14px 16px !important;
    }

    .sc-spec-tool-card,
    .sc-spec-sys-card {
      border-radius: 16px !important;
      padding: 20px 22px !important;
    }

    .sc-spec-flow-step {
      border-radius: 16px !important;
      padding: 20px 22px !important;
    }
"""


def update_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    # 1. Inject SPACIOUS_AND_ROUNDED_CSS right before </style>
    if "details.sc-master-contract-drawer {" not in text:
        idx = text.rfind("</style>")
        assert idx != -1, f"</style> not found in {path}"
        text = text[:idx] + SPACIOUS_AND_ROUNDED_CSS + "\n  </style>" + text[idx + len("</style>"):]

    # 2. Update openAndScrollToSpecSection so it also opens #agentMasterContractDrawer
    old_scroll_fn = """    function openAndScrollToSpecSection(sectionId, childId = null) {
      const sec = document.getElementById(sectionId);
      if (sec) {
        if (sec.tagName === 'DETAILS') sec.open = true;
        const parentDetails = sec.closest('details.sc-spec-collapsible');
        if (parentDetails) parentDetails.open = true;
      }"""
    new_scroll_fn = """    function openAndScrollToSpecSection(sectionId, childId = null) {
      const master = document.getElementById('agentMasterContractDrawer');
      if (master && master.tagName === 'DETAILS') master.open = true;
      const sec = document.getElementById(sectionId);
      if (sec) {
        if (sec.tagName === 'DETAILS') sec.open = true;
        const parentDetails = sec.closest('details.sc-spec-collapsible');
        if (parentDetails) parentDetails.open = true;
      }"""
    assert old_scroll_fn in text, f"openAndScrollToSpecSection not found in {path}"
    text = text.replace(old_scroll_fn, new_scroll_fn, 1)

    # Also add toggleAllPersonaDailySteps helper right after toggleAllAgentSpecSections
    old_toggle_all = """    function toggleAllAgentSpecSections(btn) {
      const root = btn.closest('#agentGenieWrap, #blueprintGenieWrap') || document;
      const drawers = Array.from(root.querySelectorAll('details.sc-spec-collapsible'));
      if (!drawers.length) return;
      const anyClosed = drawers.some(d => !d.open);
      drawers.forEach(d => {
        d.open = anyClosed;
        if (anyClosed) {
          d.querySelectorAll('details.sc-spec-sub-drawer').forEach(sub => { sub.open = true; });
        }
      });
      btn.textContent = anyClosed ? '▴ Collapse All 6 Spec Sections' : '▾ Expand All 6 Spec Sections Inline';
    }"""
    new_toggle_all = """    function toggleAllAgentSpecSections(btn) {
      const master = document.getElementById('agentMasterContractDrawer');
      if (master && master.tagName === 'DETAILS') master.open = true;
      const root = btn.closest('#agentGenieWrap, #blueprintGenieWrap') || document;
      const drawers = Array.from(root.querySelectorAll('details.sc-spec-collapsible'));
      if (!drawers.length) return;
      const anyClosed = drawers.some(d => !d.open);
      drawers.forEach(d => {
        d.open = anyClosed;
        if (anyClosed) {
          d.querySelectorAll('details.sc-spec-sub-drawer').forEach(sub => { sub.open = true; });
        }
      });
      btn.textContent = anyClosed ? '▴ Collapse All 6 Spec Sections' : '▾ Expand All 6 Spec Sections';
    }

    function toggleAllPersonaDailySteps(btn) {
      const root = document.getElementById('personaGenieWrap') || document;
      const items = Array.from(root.querySelectorAll('.journey-accordion-item'));
      if (!items.length) return;
      const anyClosed = items.some(el => !el.classList.contains('open'));
      items.forEach(el => {
        if (anyClosed) el.classList.add('open');
        else el.classList.remove('open');
      });
      btn.textContent = anyClosed ? '▴ Collapse Daily Tasks' : '▾ Expand All Daily Tasks';
    }"""
    assert old_toggle_all in text, f"toggleAllAgentSpecSections not found in {path}"
    text = text.replace(old_toggle_all, new_toggle_all, 1)

    # 3. Update openPersonaPage to have bigger, untruncated, spacious Day-to-Day Life Comparison
    old_persona_chunk = """          <!-- Clean, Compact Persona Header -->
          <div class="persona-header-card" style="padding: 24px 30px; margin-bottom: 22px;">
            ${renderSupplyChainWatermarkSvg(dept.watermarkType, dept.color, 'persona-header-sc-watermark')}

            <div style="position:relative; z-index:2; display:flex; align-items:center; gap:18px; flex-wrap:wrap;">
              <div class="human-avatar-circle" style="width:60px; height:60px; font-size:28px; --dept-accent:${dept.color};">
                ${p.icon}
              </div>
              <div>
                <h1 class="persona-page-title" style="margin-bottom:4px;">${p.name}</h1>
                <div style="font-size:15px; color:var(--text-secondary); font-weight:600;">${p.subPillarName || dept.name}</div>
              </div>
            </div>

            <div class="persona-stat-highlight" style="border-color: ${dept.color}45;">
              <div class="persona-stat-value" style="color: ${dept.color};">${p.headlineStat || '-85% Toil'}</div>
              <div class="persona-stat-label">${p.toilHoursBefore || '6.5h'} &rarr; ${p.toilHoursAfter || '1.0h'}</div>
            </div>
          </div>

          <!-- Simple Persona Daily Journey -->
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom: 14px;">
            <div>
              <h2 class="block-title" style="border-left-color: ${dept.color}; margin-bottom:2px;">Persona Daily Journey</h2>
              <p class="block-subtitle" style="margin:0;">Click any daily task below to compare <strong style="color:#ea4335;">Manual Bottleneck (Red)</strong> vs. <strong style="color:#34a853;">With Gemini AI (Green)</strong> and launch the assigned AI Agent.</p>
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
                      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:16px; padding-top:14px;">
                        <div class="toil-highlight-box" style="padding:16px 18px;">
                          <div class="toil-top-bar" style="margin-bottom:8px;">
                            <span class="toil-badge">✕ Manual Bottleneck</span>
                            <span class="toil-duration">⏱ ${slot.toilDuration || '2.0 hrs'}</span>
                          </div>
                          <div class="toil-text" style="font-size:14.5px; line-height:1.58;">${shortSentence(slot.before, 220)}</div>
                        </div>

                        <div class="gemini-improve-box" style="padding:16px 18px;">
                          <div class="improve-top-bar" style="margin-bottom:8px;">
                            <span class="improve-badge">✦ With Gemini AI</span>
                            <span class="improve-time-saved">⚡ ${slot.toilDuration || '2.0 hrs'} &rarr; ${slot.afterDuration || '10 mins'}</span>
                          </div>
                          <div class="improve-text" style="font-size:14.5px; line-height:1.58;">${shortSentence(slot.after, 220)}</div>
                        </div>
                      </div>

                      ${plugAgent ? `
                        <div class="persona-step-agent-box">
                          <div style="display:flex; align-items:center; gap:14px; flex:1; min-width:240px;">
                            <div class="ai-bot-square" style="width:42px; height:42px; font-size:18px; flex-shrink:0;">✦</div>
                            <div>
                              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:4px;">
                                <span style="font-family:var(--font-display); font-size:16.5px; font-weight:800; color:var(--text-primary);">
                                  ${plugAgent.name}
                                </span>
                                <span class="build-tier-badge ${plugCls.cssClass}">${plugCls.label}</span>
                                ${plugAgent.badge ? `
                                  <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; padding:2px 9px; border-radius:999px; background:rgba(16,185,129,0.16); color:#10b981; border:1px solid rgba(16,185,129,0.4);">
                                    ${plugAgent.badge}
                                  </span>
                                ` : ''}
                              </div>
                              <div style="font-size:13.5px; color:var(--text-secondary); line-height:1.45;">
                                ${shortSentence(plugAgent.solution || plugAgent.role, 155)}
                              </div>
                              ${plugAgent.costModel ? `
                                <div style="margin-top:6px;">
                                  <span style="font-family:var(--font-mono); font-size:11px; font-weight:700; color:var(--text-secondary);">
                                    💰 Est. Cost: <strong style="color:var(--text-primary);">$${plugAgent.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo</strong> ($${plugAgent.costModel.monthlyBreakdown.blendedCostPer1kCallsUsd.toFixed(2)}/1K runs)
                                  </span>
                                </div>
                              ` : ''}
                            </div>
                          </div>

                          <button type="button" class="agent-plug-btn" style="padding:10px 18px; font-size:13px;" onclick="openAgentPage('${plugAgent.id}', true, event)">
                            <span>Open ${plugAgent.name} &amp; Demo</span>
                            <span>&rarr;</span>
                          </button>
                        </div>
                      ` : ''}
                    ` : `
                      <div style="padding-top:12px; font-size:14.5px; line-height:1.58; color:var(--text-secondary);">
                        ${shortSentence(slot.activity, 200)}
                      </div>
                    `}
                  </div>
                </div>
              `;
            }).join('')}
          </div>

          <!-- Structured AI Agents Dock for this Persona (Good Boxes + Clear Button) -->
          <div class="ai-agent-dock-box">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-bottom:16px;">
              <div style="display:flex; align-items:center; gap:10px;">
                <span style="padding:4px 10px; border-radius:8px; background:linear-gradient(135deg,#4f46e5,#7c3aed); color:#ffffff; font-size:11.5px; font-weight:800; letter-spacing:0.06em; text-transform:uppercase;">
                  ✦ AI Agents for ${p.name}
                </span>
                <span style="font-size:13.5px; color:var(--text-secondary); font-weight:600;">
                  Explore each AI agent's architecture, ROI, and demo video
                </span>
              </div>
            </div>

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:16px;">
              ${[...new Set(p.agentIds || [])].map(aid => {
                const ag = AGENTS[aid];
                if (!ag) return '';
                const cls = getAgentBuildClassification(ag);
                return `
                  <div class="persona-agent-dock-card">
                    <div>
                      <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:10px; margin-bottom:10px;">
                        <div style="display:flex; align-items:center; gap:12px;">
                          <div class="ai-bot-square" style="width:40px; height:40px; font-size:17px; flex-shrink:0;">✦</div>
                          <div>
                            <div class="ai-agent-chip-title" style="font-size:16.5px;">${cleanAgentName(ag.name)}</div>
                            <div style="font-size:12.5px; color:var(--text-secondary); margin-top:2px;">${ag.subPillarName || dept.name}</div>
                          </div>
                        </div>
                      </div>

                      <div style="font-size:13.5px; color:var(--text-secondary); line-height:1.5; margin-bottom:10px;">
                        ${shortSentence(ag.solution || ag.role, 135)}
                      </div>

                      ${ag.badge ? `
                        <div style="display:inline-flex; align-items:center; padding:3px 10px; border-radius:999px; background:rgba(16,185,129,0.14); border:1px solid rgba(16,185,129,0.38); color:#10b981; font-family:var(--font-mono); font-size:11px; font-weight:800; margin-bottom:6px;">
                          ✦ ${ag.badge}
                        </div>
                      ` : ''}
                      ${ag.costModel ? `
                        <div style="font-family:var(--font-mono); font-size:11.5px; color:var(--text-secondary); margin-top:6px;">
                          💰 Est. Cost: <strong style="color:var(--text-primary);">$${ag.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo</strong> ($${ag.costModel.monthlyBreakdown.blendedCostPer1kCallsUsd.toFixed(2)}/1K)
                        </div>
                      ` : ''}
                    </div>

                    <button type="button" class="agent-plug-btn" style="width:100%; justify-content:center; padding:10px 16px; font-size:13px;" onclick="openAgentPage('${ag.id}', true, event)">
                      <span>Open ${ag.name} &amp; Demo</span>
                      <span>&rarr;</span>
                    </button>
                  </div>
                `;
              }).join('')}
            </div>
          </div>"""

    new_persona_chunk = """          <!-- Spacious, Readable Persona Header -->
          <div class="persona-header-card" style="padding: 28px 34px; margin-bottom: 26px; border-radius: 22px;">
            ${renderSupplyChainWatermarkSvg(dept.watermarkType, dept.color, 'persona-header-sc-watermark')}

            <div style="position:relative; z-index:2; display:flex; align-items:flex-start; gap:20px; flex-wrap:wrap; flex:1;">
              <div class="human-avatar-circle" style="width:66px; height:66px; font-size:30px; --dept-accent:${dept.color}; flex-shrink:0;">
                ${p.icon}
              </div>
              <div style="flex:1; min-width:260px;">
                <h1 class="persona-page-title" style="font-size:clamp(26px, 2.8vw, 36px); margin-bottom:6px;">${p.name}</h1>
                <div style="font-size:15.5px; color:${dept.color}; font-weight:700; margin-bottom:8px;">${p.subPillarName || dept.name}</div>
                <p style="font-size:16px; line-height:1.68; color:var(--text-secondary); margin:0; max-width:820px;">
                  ${p.role || ''}
                </p>
              </div>
            </div>

            <div class="persona-stat-highlight" style="border-color: ${dept.color}45; border-radius: 18px; padding: 18px 24px;">
              <div class="persona-stat-value" style="color: ${dept.color}; font-size: 28px;">${p.headlineStat || '-85% Toil'}</div>
              <div class="persona-stat-label" style="font-size: 14px;">${p.toilHoursBefore || '6.5h'} &rarr; ${p.toilHoursAfter || '1.0h'}</div>
            </div>
          </div>

          <!-- Spacious Persona Day-to-Day Life Comparison -->
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:14px; margin-bottom: 18px;">
            <div>
              <h2 class="block-title" style="border-left-color: ${dept.color}; font-size: 24px; margin-bottom: 4px;">Day-to-Day Life Comparison — ${p.name}</h2>
              <p class="block-subtitle" style="margin:0; font-size: 15.5px; line-height: 1.6;">Compare <strong style="color:#ea4335;">Manual Bottleneck (Before AI)</strong> vs. <strong style="color:#34a853;">With Gemini AI (Autonomous Flow)</strong> across each daily workflow step.</p>
            </div>
            <button type="button" class="switch-pill" style="padding: 9px 18px; font-size: 13.5px; font-weight: 700;" onclick="toggleAllPersonaDailySteps(this)">
              ▾ Expand All Daily Tasks
            </button>
          </div>

          <div style="margin-bottom: 38px;">
            ${(() => {
              let openedToilCount = 0;
              return p.dayInLife.map((slot, idx) => {
                const stepId = `pStep_${p.id}_${idx}`;
                const plugAgent = slot.agentId ? AGENTS[slot.agentId] : null;
                const plugCls = plugAgent ? getAgentBuildClassification(plugAgent) : null;
                const isDefaultOpen = slot.isToil && openedToilCount < 2;
                if (isDefaultOpen) openedToilCount++;

                return `
                  <div id="${stepId}" class="journey-accordion-item ${isDefaultOpen ? 'open' : ''}" style="--dept-accent:${dept.color};">
                    <button type="button" class="journey-accordion-header" onclick="togglePersonaJourneyStep('${stepId}')">
                      <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
                        <span class="time-badge" style="min-width:92px; text-align:center;">${slot.time}</span>
                        <span class="task-title">${slot.task}</span>
                        ${slot.isToil ? `
                          <span style="font-size:13.5px; font-weight:800; padding:5px 14px; border-radius:999px; background:rgba(52,168,83,0.14); color:#34a853; border:1px solid rgba(52,168,83,0.35);">
                            ⚡ ${slot.toilDuration || '2.0 hrs'} &rarr; ${slot.afterDuration || '10 mins'}
                          </span>
                        ` : `
                          <span class="core-tag-pill">👤 ${slot.tag || 'Leadership'}</span>
                        `}
                      </div>

                      <div style="display:flex; align-items:center; gap:12px;">
                        ${plugAgent ? `
                          <span class="ai-agent-type-tag" style="padding:6px 14px; font-size:12.5px;" onclick="event.stopPropagation(); openAgentPage('${plugAgent.id}', true, event)">
                            ✦ ${plugAgent.name} &rarr;
                          </span>
                        ` : ''}
                        <span class="journey-accordion-chevron" style="padding:6px 14px; font-size:13px;">Details ▾</span>
                      </div>
                    </button>

                    <div class="journey-accordion-body">
                      ${slot.isToil ? `
                        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap:22px; padding-top:18px;">
                          <div class="toil-highlight-box">
                            <div class="toil-top-bar">
                              <span class="toil-badge">✕ Manual Bottleneck (Before AI)</span>
                              <span class="toil-duration">⏱ ${slot.toilDuration || '2.0 hrs'}</span>
                            </div>
                            <div class="toil-text">${slot.before}</div>
                          </div>

                          <div class="gemini-improve-box">
                            <div class="improve-top-bar">
                              <span class="improve-badge">✦ With Gemini AI (Autonomous Flow)</span>
                              <span class="improve-time-saved">⚡ ${slot.toilDuration || '2.0 hrs'} &rarr; ${slot.afterDuration || '10 mins'}</span>
                            </div>
                            <div class="improve-text">${slot.after}</div>
                          </div>
                        </div>

                        ${plugAgent ? `
                          <div class="persona-step-agent-box">
                            <div style="display:flex; align-items:flex-start; gap:16px; flex:1; min-width:260px;">
                              <div class="ai-bot-square" style="width:46px; height:46px; font-size:20px; border-radius:14px; flex-shrink:0;">✦</div>
                              <div>
                                <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:6px;">
                                  <span style="font-family:var(--font-display); font-size:18.5px; font-weight:800; color:var(--text-primary);">
                                    ${plugAgent.name}
                                  </span>
                                  <span class="build-tier-badge ${plugCls.cssClass}">${plugCls.label}</span>
                                  ${plugAgent.badge ? `
                                    <span style="font-family:var(--font-mono); font-size:12px; font-weight:800; padding:4px 12px; border-radius:999px; background:rgba(16,185,129,0.16); color:#10b981; border:1px solid rgba(16,185,129,0.4);">
                                      ${plugAgent.badge}
                                    </span>
                                  ` : ''}
                                </div>
                                <div style="font-size:15.5px; color:var(--text-secondary); line-height:1.68;">
                                  ${plugAgent.solution || plugAgent.role}
                                </div>
                                ${plugAgent.costModel ? `
                                  <div style="margin-top:8px;">
                                    <span style="font-family:var(--font-mono); font-size:12.5px; font-weight:700; color:var(--text-secondary);">
                                      💰 Est. Run Cost: <strong style="color:var(--text-primary);">$${plugAgent.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo</strong> ($${plugAgent.costModel.monthlyBreakdown.blendedCostPer1kCallsUsd.toFixed(2)}/1K runs)
                                    </span>
                                  </div>
                                ` : ''}
                              </div>
                            </div>

                            <button type="button" class="agent-plug-btn" onclick="openAgentPage('${plugAgent.id}', true, event)">
                              <span>Open ${plugAgent.name} &amp; Demo</span>
                              <span>&rarr;</span>
                            </button>
                          </div>
                        ` : ''}
                      ` : `
                        <div style="padding-top:16px; font-size:16px; line-height:1.72; color:var(--text-secondary);">
                          ${slot.activity}
                        </div>
                      `}
                    </div>
                  </div>
                `;
              }).join('');
            })()}
          </div>

          <!-- Structured AI Agents Dock for this Persona (Spacious Cards + Rounded Buttons) -->
          <div class="ai-agent-dock-box">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom:20px;">
              <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
                <span style="padding:6px 14px; border-radius:999px; background:linear-gradient(135deg,#4f46e5,#7c3aed); color:#ffffff; font-size:12.5px; font-weight:800; letter-spacing:0.06em; text-transform:uppercase;">
                  ✦ AI Agents Assigned to ${p.name}
                </span>
                <span style="font-size:15px; color:var(--text-secondary); font-weight:600;">
                  Explore each agent's execution flow, ROI, demo video, and full enterprise contract
                </span>
              </div>
            </div>

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(330px, 1fr)); gap:20px;">
              ${[...new Set(p.agentIds || [])].map(aid => {
                const ag = AGENTS[aid];
                if (!ag) return '';
                const cls = getAgentBuildClassification(ag);
                return `
                  <div class="persona-agent-dock-card">
                    <div>
                      <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:12px; margin-bottom:12px;">
                        <div style="display:flex; align-items:center; gap:14px;">
                          <div class="ai-bot-square" style="width:46px; height:46px; font-size:19px; border-radius:14px; flex-shrink:0;">✦</div>
                          <div>
                            <div class="ai-agent-chip-title" style="font-size:18.5px; font-weight:800;">${cleanAgentName(ag.name)}</div>
                            <div style="font-size:13.5px; color:var(--text-secondary); margin-top:3px;">${ag.subPillarName || dept.name}</div>
                          </div>
                        </div>
                      </div>

                      <div style="font-size:15.5px; color:var(--text-secondary); line-height:1.68; margin-bottom:14px;">
                        ${ag.solution || ag.role}
                      </div>

                      ${ag.badge ? `
                        <div style="display:inline-flex; align-items:center; padding:5px 12px; border-radius:999px; background:rgba(16,185,129,0.14); border:1px solid rgba(16,185,129,0.38); color:#10b981; font-family:var(--font-mono); font-size:12px; font-weight:800; margin-bottom:8px;">
                          ✦ ${ag.badge}
                        </div>
                      ` : ''}
                      ${ag.costModel ? `
                        <div style="font-family:var(--font-mono); font-size:12.5px; color:var(--text-secondary); margin-top:6px;">
                          💰 Est. Cost: <strong style="color:var(--text-primary);">$${ag.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo</strong> ($${ag.costModel.monthlyBreakdown.blendedCostPer1kCallsUsd.toFixed(2)}/1K)
                        </div>
                      ` : ''}
                    </div>

                    <button type="button" class="agent-plug-btn" style="width:100%; justify-content:center;" onclick="openAgentPage('${ag.id}', true, event)">
                      <span>Open ${ag.name} &amp; Demo</span>
                      <span>&rarr;</span>
                    </button>
                  </div>
                `;
              }).join('')}
            </div>
          </div>"""
    assert old_persona_chunk in text, f"old_persona_chunk not found in {path}"
    text = text.replace(old_persona_chunk, new_persona_chunk, 1)

    # 4. Wrap the ENTIRE renderAgentFullSpecSheet (including Quick Stats + all 6 sections open inside)
    #    under ONE single <details class="sc-master-contract-drawer" id="agentMasterContractDrawer" ${openByDefault ? 'open' : ''}>
    old_spec_launcher = """      const openAttr = openByDefault ? 'open' : '';"""
    new_spec_launcher = """      const masterOpenAttr = openByDefault ? 'open' : '';
      const openAttr = 'open';"""
    assert old_spec_launcher in text, f"old_spec_launcher not found in {path}"
    text = text.replace(old_spec_launcher, new_spec_launcher, 1)

    old_spec_return_head = """      return `
        <!-- MASTER LAUNCHER BAR FOR COLLAPSIBLE CONTRACT & SPEC SECTIONS -->
        <div class="sc-spec-master-launcher" style="border-left: 4px solid ${dept.color};">
          <div>
            <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:3px;">
              📋 Enterprise Agent Contract · Playbook, Governance &amp; Technical Specification
            </div>
            <div style="font-family:var(--font-display); font-size:18px; font-weight:800; color:var(--text-primary);">
              ${cleanName} — 6 Modular Specification Drawers
            </div>
            <div style="font-size:12.5px; color:var(--text-secondary); margin-top:2px;">
              ${openByDefault
                ? 'Dedicated Contract &amp; Specification View · Click any section or sub-section header below to collapse or expand.'
                : 'Collapsed by default to keep this view simple and clean · Click any section to expand inline, or open in a dedicated page.'}
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
            <button type="button" class="switch-pill" onclick="toggleAllAgentSpecSections(this)">
              ${openByDefault ? '▴ Collapse All 6 Spec Sections' : '▾ Expand All 6 Spec Sections Inline'}
            </button>
            ${!openByDefault ? `
              <button type="button" class="switch-pill" style="background:${dept.color}; border-color:${dept.color}; color:#ffffff; font-weight:700;" onclick="openAgentBlueprintPage('${ag.id}', true, event, 'spec-governance')">
                📄 Open Contract &amp; Spec in Dedicated Page &rarr;
              </button>
            ` : `
              <button type="button" class="switch-pill" onclick="openAgentPage('${ag.id}', true, event)">
                &larr; Back to ${cleanName} Overview
              </button>
            `}
          </div>
        </div>"""

    new_spec_return_head = """      return `
        <!-- SINGLE EXPANDABLE MASTER TAB CONTAINING THE ENTIRE ENTERPRISE AGENT CONTRACT & ALL 6 SPEC SECTIONS -->
        <details class="sc-master-contract-drawer" id="agentMasterContractDrawer" style="border-left: 5px solid ${dept.color};" ${masterOpenAttr}>
          <summary class="sc-master-contract-summary">
            <div style="flex:1; min-width:280px;">
              <div style="font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:5px;">
                📋 01–06 · Enterprise Agent Contract · Playbook, Governance &amp; Technical Specification
              </div>
              <div style="font-family:var(--font-display); font-size:22px; font-weight:800; color:var(--text-primary);">
                ${cleanName} — Complete Enterprise Agent Contract &amp; Technical Specification
              </div>
              <div style="font-size:14.5px; color:var(--text-secondary); margin-top:5px; line-height:1.55;">
                All 6 sections preserved in full: <strong>01 Playbook &amp; Governance</strong> (Role Mandate, In-Scope / Out-of-Scope, Escalation Gates, Hard Guardrails &amp; Evidence) · <strong>02 Workflow</strong> · <strong>03 Agent Tools (${rawTools.length})</strong> · <strong>04 Source Systems (${sysList.length})</strong> · <strong>05 Data Model (${tables.length} tables · ${totalFields} fields)</strong> · <strong>06 Evals &amp; Proof</strong>
              </div>
            </div>
            <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
              <span class="sc-master-contract-toggle-btn"></span>
              ${!openByDefault ? `
                <button type="button" class="switch-pill" style="background:${dept.color}; border-color:${dept.color}; color:#ffffff; font-weight:700; padding:11px 18px; font-size:13.5px;" onclick="event.preventDefault(); event.stopPropagation(); openAgentBlueprintPage('${ag.id}', true, event, 'spec-governance')">
                  📄 Open in Dedicated Page &rarr;
                </button>
              ` : `
                <button type="button" class="switch-pill" style="padding:11px 18px; font-size:13.5px;" onclick="event.preventDefault(); event.stopPropagation(); openAgentPage('${ag.id}', true, event)">
                  &larr; Back to ${cleanName} Overview
                </button>
              `}
            </div>
          </summary>

          <div class="sc-master-contract-body">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:14px;">
              <div style="font-size:14px; font-weight:700; color:var(--text-secondary);">
                Jump to any specification section below, or collapse/expand individual sections:
              </div>
              <button type="button" class="switch-pill" onclick="toggleAllAgentSpecSections(this)">
                ▴ Collapse All 6 Spec Sections
              </button>
            </div>
            ${renderAgentAtAGlanceStrip(ag, dept, openByDefault)}"""

    assert old_spec_return_head in text, f"old_spec_return_head not found in {path}"
    text = text.replace(old_spec_return_head, new_spec_return_head, 1)

    old_spec_return_tail = """                <div style="font-size:12.5px; color:var(--text-secondary); line-height:1.55; padding:10px 12px; border-radius:10px; background:var(--bg-elevated); border:1px solid var(--border-subtle);">
                  <strong>Spec Source:</strong> <code class="sc-spec-code">agents/${ag.id}/app/agent.py</code> · <code class="sc-spec-code">agents/${ag.id}/tests/test_smoke.py</code> · Verified 7/7 deterministic contract &amp; A2UI surface checks passing.
                </div>
              </div>
            </div>
          </div>
        </details>
      `;
    }"""

    new_spec_return_tail = """                <div style="font-size:13.5px; color:var(--text-secondary); line-height:1.62; padding:12px 16px; border-radius:12px; background:var(--bg-elevated); border:1px solid var(--border-subtle);">
                  <strong>Spec Source:</strong> <code class="sc-spec-code">agents/${ag.id}/app/agent.py</code> · <code class="sc-spec-code">agents/${ag.id}/tests/test_smoke.py</code> · Verified 7/7 deterministic contract &amp; A2UI surface checks passing.
                </div>
              </div>
            </div>
          </div>
        </details>
          </div>
        </details>
      `;
    }"""

    assert old_spec_return_tail in text, f"old_spec_return_tail not found in {path}"
    text = text.replace(old_spec_return_tail, new_spec_return_tail, 1)

    # 5. Clean up openAgentPage hero banner so renderAgentAtAGlanceStrip is NOT duplicated outside the single expandable tab,
    #    and make the Problem & Outcome drawer text full and spacious
    old_agent_hero = """            <div id="agentMoreDetailsDrawer" class="journey-accordion-item" style="margin-top:14px; margin-bottom:0;">
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
            </div>
            ${renderAgentAtAGlanceStrip(ag, dept, false)}
          </div>"""

    new_agent_hero = """            <div id="agentMoreDetailsDrawer" class="journey-accordion-item open" style="margin-top:18px; margin-bottom:0;">
              <div class="journey-accordion-body" style="padding:18px 22px 22px;">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap:20px;">
                  <div class="toil-highlight-box">
                    <div class="toil-top-bar"><span class="toil-badge">✕ Legacy Bottleneck Solved</span></div>
                    <div class="toil-text">${ag.problem}</div>
                  </div>
                  <div class="gemini-improve-box">
                    <div class="improve-top-bar"><span class="improve-badge">✦ Agentic AI Solution &amp; Outcome</span></div>
                    <div class="improve-text">${ag.solution} <strong>${ag.outcome}</strong></div>
                  </div>
                </div>
              </div>
            </div>
          </div>"""

    assert old_agent_hero in text, f"old_agent_hero not found in {path}"
    text = text.replace(old_agent_hero, new_agent_hero, 1)

    # Also remove duplicate renderAgentAtAGlanceStrip from openAgentBlueprintPage hero banner
    old_bp_hero = """              <button type="button" class="switch-pill" onclick="openAgentPage('${ag.id}', true, event)">
                &larr; Return to Clean Agent Overview
              </button>
            </div>
            ${renderAgentAtAGlanceStrip(ag, dept, true)}
          </div>"""
    new_bp_hero = """              <button type="button" class="switch-pill" onclick="openAgentPage('${ag.id}', true, event)">
                &larr; Return to Clean Agent Overview
              </button>
            </div>
          </div>"""
    assert old_bp_hero in text, f"old_bp_hero not found in {path}"
    text = text.replace(old_bp_hero, new_bp_hero, 1)

    # 6. Fix (st.systems || '').split('·')[0] bug in renderVisualValueChainDiagramSvg
    #    and make Process Stage Spotlight comparison in openValueChainPage bigger and untruncated
    text = text.replace(
        "const sysFirst = (st.systems || '').split('·')[0].trim().slice(0, 18);",
        "const sysFirst = (toSysArray(st.systems)[0] || '').trim().slice(0, 18);"
    )

    old_vc_spotlight = """                <div style="font-size:14px; font-weight:600; color:var(--text-primary); line-height:1.45;">
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
            </div>"""

    new_vc_spotlight = """                <div style="font-size:15.5px; font-weight:600; color:var(--text-primary); line-height:1.65;">
                  ${activeStage.after}
                </div>
              </div>

              <div class="vc-schematic-arrow">──🔗──▶</div>

              <div class="vc-schematic-node" style="border-left: 4px solid #34a853;">
                <div style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:#34a853; text-transform:uppercase;">
                  📤 3. Golden Thread Handoff
                </div>
                <div style="font-size:15.5px; font-weight:600; color:var(--text-primary); line-height:1.65;">
                  ${activeStage.goldenThread}
                </div>
              </div>
            </div>

            <!-- Spacious Before vs. After Stage Comparison -->
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap:22px; margin: 18px 0;">
              <div class="toil-highlight-box">
                <div class="toil-top-bar">
                  <span class="toil-badge">✕ Manual Bottleneck (Before AI)</span>
                  <span class="toil-duration">⏱ ${activeStage.toilTime}</span>
                </div>
                <div class="toil-text">${activeStage.before}</div>
              </div>
              <div class="gemini-improve-box">
                <div class="improve-top-bar">
                  <span class="improve-badge">✦ With Gemini AI (Autonomous Stage)</span>
                  <span class="improve-time-saved">⚡ ${activeStage.toilTime} &rarr; ${activeStage.afterTime}</span>
                </div>
                <div class="improve-text">${activeStage.after}</div>
              </div>
            </div>"""

    assert old_vc_spotlight in text, f"old_vc_spotlight not found in {path}"
    text = text.replace(old_vc_spotlight, new_vc_spotlight, 1)

    path.write_text(text, encoding="utf-8")
    print(f"Updated {path.name} successfully")


if __name__ == "__main__":
    for f in HTML_FILES:
        update_file(f)

#!/usr/bin/env python3
"""
Fixes all UI clipping/overflow issues and simplifies the Agent Page & website cards:
1. Removes the redundant 5-column step cards (.ag-flow-steps-grid) below the SVG Execution Flow
   diagram (the SVG diagram already visualizes all 5 stages).
2. Humanizes all snake_case tool/table identifiers inside the SVG diagram (no raw query_... or
   table_name_... code strings).
3. Fixes .sc-flip-card CSS using a CSS Grid overlay (grid-template-areas: "flipface") and full-width
   headings so text NEVER clips horizontally or vertically, and removes noisy bottom chip lists
   and mid-word '....' truncations.
4. Simplifies 'Playbook & Governance' under 1 button to 3 clean, relevant, plain-English
   Flippable Cards (Autonomous Scope, Human Approval Guardrails, Connected Enterprise Systems).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HTML_FILES = [
    ROOT / "index.html",
    ROOT / "periodic_table.html",
    ROOT / "mind_map.html",
]

CLEAN_FLIP_CSS = """
    /* =========================================================================
       3D FLIPPABLE CARDS (.sc-flip-card) — ZERO CLIPPING, FULL-WIDTH BIG HEADINGS
       ========================================================================= */
    .sc-flip-card {
      perspective: 1100px;
      cursor: pointer;
      user-select: none;
      position: relative;
      height: 100%;
    }
    .sc-flip-inner {
      display: grid;
      grid-template-areas: "flipface";
      width: 100%;
      height: 100%;
      min-height: 148px;
      transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1);
      transform-style: preserve-3d;
    }
    .sc-flip-card.is-flipped .sc-flip-inner {
      transform: rotateY(180deg);
    }
    .sc-flip-front,
    .sc-flip-back {
      grid-area: flipface;
      position: relative;
      width: 100%;
      height: 100%;
      box-sizing: border-box;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      border-radius: 16px;
      padding: 20px 22px;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      border-top: 4px solid var(--flip-accent, #38bdf8);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 10px;
      box-shadow: 0 8px 22px rgba(0, 0, 0, 0.14);
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    html[data-theme="light"] .sc-flip-front,
    html[data-theme="light"] .sc-flip-back {
      background: #ffffff;
      border-color: rgba(15, 23, 42, 0.12);
      border-top: 4px solid var(--flip-accent, #2563eb);
      box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
    }
    .sc-flip-card:hover .sc-flip-front,
    .sc-flip-card:hover .sc-flip-back {
      border-color: var(--flip-accent, #38bdf8);
      box-shadow: 0 12px 26px rgba(0, 0, 0, 0.2);
    }
    .sc-flip-back {
      transform: rotateY(180deg);
      background: var(--bg-card);
    }
    html[data-theme="light"] .sc-flip-back {
      background: #f8fafc;
    }
    .sc-flip-top-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }
    .sc-flip-kicker {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--flip-accent, #38bdf8);
    }
    .sc-flip-hint {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      padding: 3px 9px;
      border-radius: 999px;
      background: rgba(148, 163, 184, 0.12);
      color: var(--text-secondary);
      border: 1px solid var(--border-subtle);
      white-space: nowrap;
      flex-shrink: 0;
    }
    .sc-flip-big-heading {
      font-family: var(--font-display);
      font-size: 21px;
      font-weight: 800;
      color: var(--text-primary);
      line-height: 1.28;
      margin: 2px 0;
      word-break: normal;
      overflow-wrap: break-word;
    }
    .sc-flip-sub-label {
      font-size: 13px;
      font-weight: 600;
      color: var(--text-secondary);
    }
    .sc-flip-back-text {
      font-size: 14.5px;
      font-weight: 600;
      color: var(--text-primary);
      line-height: 1.55;
      margin: 4px 0;
    }

    /* Single Expandable Bar for Playbook & Governance */
    .sc-single-spec-trigger-bar {
      margin-top: 22px;
      margin-bottom: 14px;
      padding: 20px 26px;
      border-radius: 18px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 14px;
      box-shadow: 0 10px 26px rgba(0, 0, 0, 0.16);
    }
    html[data-theme="light"] .sc-single-spec-trigger-bar {
      background: #ffffff;
      border-color: rgba(15, 23, 42, 0.12);
      box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
    }
"""

NEW_SIMPLE_AGENT_JS = """    function cleanSentence(str, maxLen = 140) {
      const s = String(str || '').trim();
      if (!s) return '';
      const first = s.split(/(?<=\\.)\\s+/)[0] || s;
      if (first.length <= maxLen) return first;
      const cut = first.slice(0, maxLen);
      const lastSpace = cut.lastIndexOf(' ');
      return (lastSpace > 40 ? cut.slice(0, lastSpace) : cut).replace(/[.,;:\\s]+$/, '') + '.';
    }

    function humanizeCodeName(raw, prefixRemove = '') {
      let s = String(raw || '').trim();
      if (prefixRemove) {
        s = s.replace(new RegExp('^' + prefixRemove + '_?', 'i'), '');
      }
      s = s.replace(/^(query_|action_|xyz_)/i, '');
      const words = s.split('_').filter(Boolean);
      const cleanWords = words.slice(-3).map(w => w.charAt(0).toUpperCase() + w.slice(1));
      return cleanWords.join(' ') || 'Live Records';
    }

    function shortStepHeading(rawTitle, fallback) {
      const s = String(rawTitle || fallback || '').trim()
        .replace(/^Transactional State DB\\s+/i, '')
        .replace(/^Multi-Hop Graph DB\\s+/i, '')
        .replace(/^Time-Series Forecasting FM\\s+/i, '')
        .replace(/^Mathematical Optimization Solver \\(MILP \\/ CP-SAT\\)\\s+/i, '')
        .replace(/^Vector Search & Semantic Index\\s+/i, '');
      const words = s.split(/\\s+/).filter(Boolean);
      if (words.length <= 4) return s;
      return words.slice(0, 4).join(' ');
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

      // 1. Open, Technology-First Connected Systems
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

      // 2. Human-readable labels for the SVG diagram (no ugly raw snake_case code strings)
      const tables = (adk.fixtureTables || []).map(t => t.table_name);
      const tbl1 = humanizeCodeName(tables[0] || 'Operational Ledger', ag.id);
      const tbl2 = humanizeCodeName(tables[1] || 'Signal Telemetry', ag.id);
      const tbl3 = humanizeCodeName(tables[2] || 'Constraint Matrix', ag.id);

      const rawTools = (spec.toolsMeta && spec.toolsMeta.length)
        ? spec.toolsMeta.map(t => t.name)
        : (adk.tools || []).filter(t => t !== 'list_systems');
      const qTools = rawTools.filter(t => !String(t).startsWith('action_'));
      const aTools = rawTools.filter(t => String(t).startsWith('action_'));
      const q1 = humanizeCodeName(qTools[0] || 'Fetch Live Signals', ag.id);
      const q2 = humanizeCodeName(qTools[1] || 'Verify Constraints', ag.id);
      const a1 = humanizeCodeName(aTools[0] || 'Commit Governed Action', ag.id);

      // 3. Real 3 Sub-Agents for this agent
      const rawSubs = (ag.subAgents && ag.subAgents.length >= 3)
        ? ag.subAgents.slice(0, 3)
        : [
            { name: 'Signal Context Node', role: 'Streams & validates live operational inputs' },
            { name: 'Optimization Engine', role: 'Evaluates constraints & ranks actions' },
            { name: 'Write-Back Dispatcher', role: 'Enforces quality gates & signed payloads' }
          ];
      const subs = rawSubs.map(sa => ({
        name: shortStepHeading(toOpenTechLabel(sa.name), 'Agent Node'),
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
      }).replace(/enforce_tool_contract\\(\\)/g, 'Policy & Threshold Gate');

      return `
        <div class="simple-arch-card">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:14px;">
            <div>
              <div style="font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:3px;">
                ${tMeta.badge} · ${cadence}
              </div>
              <h2 style="font-family:var(--font-display); font-size:24px; font-weight:800; color:var(--text-primary); margin:0;">
                Execution Flow — ${cleanName}
              </h2>
            </div>

            <span class="sc-spec-count-badge" style="color:#10b981; border-color:rgba(16,185,129,0.35);">
              🔌 Open Integration: BigQuery · On-Prem DBs · 3rd-Party MCPs · REST/EDI
            </span>
          </div>

          <!-- Custom Agent-Specific Animated Full-Canvas SVG Flow Diagram (No Redundant 5-Card Row Below) -->
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
        </div>
      `;
    }

    /* =========================================================================
       CLEAN AGENT COST & VALUE FLIPPABLE CARDS (ZERO CLIPPING)
       ========================================================================= */
    function renderAgentCostAndRoiPanel(ag, dept) {
      const cm = ag.costModel;
      if (!cm) return '';
      const mb = cm.monthlyBreakdown;
      const vm = cm.valueModel;
      const mc = cm.manualComparison || {
        manualHoursPerMonth: 320,
        fteEquivalent: 2.0,
        hourlyRateUsd: 65,
        manualErrorReworkMoUsd: 3200,
        manualMonthlyCostUsd: 24000,
        manualAnnualCostUsd: 288000,
        directMonthlySavingsUsd: Math.round(24000 - mb.totalFsp3YrUsd),
        directSavingsPct: 99.0
      };

      const aiMo = Math.round(mb.totalFsp3YrUsd);
      const valMo = Math.round(vm.grossAnnualConservativeUsd / 12);

      return `
        <div class="simple-arch-card" style="margin-top: 22px; margin-bottom: 22px;">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
            <div>
              <div style="font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:3px;">
                Cost &amp; ROI Summary
              </div>
              <h2 style="font-family:var(--font-display); font-size:24px; font-weight:800; color:var(--text-primary); margin:0;">
                Cost vs. Value — ${cleanAgentName(ag.name)}
              </h2>
            </div>

            <button type="button" class="switch-pill" onclick="openCostTabPage('${ag.deptId}', '${ag.id}', true)">
              📊 Interactive Cost Calculator &rarr;
            </button>
          </div>

          <!-- 4 Clean Flippable KPI Cards -->
          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:14px;">
            <div class="sc-flip-card" style="--flip-accent:${dept.color};" onclick="this.classList.toggle('is-flipped')">
              <div class="sc-flip-inner">
                <div class="sc-flip-front">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">✦ AI AGENT COST</span>
                    <span class="sc-flip-hint">↻ Flip</span>
                  </div>
                  <div class="sc-flip-big-heading" style="font-size:30px;">
                    $${aiMo.toLocaleString()}<span style="font-size:15px; font-weight:600; color:var(--text-secondary);"> / mo</span>
                  </div>
                  <div class="sc-flip-sub-label">Cloud Infra + Gemini Tokens</div>
                </div>
                <div class="sc-flip-back">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">UNIT ECONOMICS</span>
                    <span class="sc-flip-hint">↺ Back</span>
                  </div>
                  <div class="sc-flip-back-text">
                    $${mb.blendedCostPer1kCallsUsd.toFixed(2)} per 1,000 runs (pilot scale starts at ~$${mb.pilotScaleMoUsd.toFixed(0)}/mo).
                  </div>
                </div>
              </div>
            </div>

            <div class="sc-flip-card" style="--flip-accent:#f43f5e;" onclick="this.classList.toggle('is-flipped')">
              <div class="sc-flip-inner">
                <div class="sc-flip-front">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">✕ MANUAL EFFORT</span>
                    <span class="sc-flip-hint">↻ Flip</span>
                  </div>
                  <div class="sc-flip-big-heading" style="font-size:30px;">
                    $${mc.manualMonthlyCostUsd.toLocaleString()}<span style="font-size:15px; font-weight:600; color:var(--text-secondary);"> / mo</span>
                  </div>
                  <div class="sc-flip-sub-label">~${mc.fteEquivalent} FTE Manual Baseline</div>
                </div>
                <div class="sc-flip-back">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">MANUAL BASELINE</span>
                    <span class="sc-flip-hint">↺ Back</span>
                  </div>
                  <div class="sc-flip-back-text">
                    Replaces ~${mc.manualHoursPerMonth} hours/month of manual spreadsheet reconciliation and rework.
                  </div>
                </div>
              </div>
            </div>

            <div class="sc-flip-card" style="--flip-accent:#38bdf8;" onclick="this.classList.toggle('is-flipped')">
              <div class="sc-flip-inner">
                <div class="sc-flip-front">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">⚡ PROCESS SAVINGS</span>
                    <span class="sc-flip-hint">↻ Flip</span>
                  </div>
                  <div class="sc-flip-big-heading" style="font-size:30px; color:#38bdf8;">
                    ${mc.directSavingsPct}%<span style="font-size:15px; font-weight:600; color:var(--text-secondary);"> Less</span>
                  </div>
                  <div class="sc-flip-sub-label">Saves $${mc.directMonthlySavingsUsd.toLocaleString()} / mo</div>
                </div>
                <div class="sc-flip-back">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">DIRECT SAVINGS</span>
                    <span class="sc-flip-hint">↺ Back</span>
                  </div>
                  <div class="sc-flip-back-text">
                    Reduces monthly operational execution cost by $${mc.directMonthlySavingsUsd.toLocaleString()}/mo across ~${cm.eventsPerDay.toLocaleString()} daily runs.
                  </div>
                </div>
              </div>
            </div>

            <div class="sc-flip-card" style="--flip-accent:#10b981;" onclick="this.classList.toggle('is-flipped')">
              <div class="sc-flip-inner">
                <div class="sc-flip-front">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">🚀 VALUE UNLOCKED</span>
                    <span class="sc-flip-hint">↻ Flip</span>
                  </div>
                  <div class="sc-flip-big-heading" style="font-size:30px; color:#10b981;">
                    $${(vm.grossAnnualConservativeUsd / 1e6).toFixed(2)}M<span style="font-size:15px; font-weight:600; color:var(--text-secondary);"> / yr</span>
                  </div>
                  <div class="sc-flip-sub-label">${vm.cloudRoiMultipleConservative}x Annual Cloud ROI</div>
                </div>
                <div class="sc-flip-back">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">SUPPLY CHAIN VALUE</span>
                    <span class="sc-flip-hint">↺ Back</span>
                  </div>
                  <div class="sc-flip-back-text">
                    Unlocks ~$${(valMo / 1000).toFixed(1)}K/mo in working capital, margin protection, and service-level gains.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    function toggleSingleAgentSpecDrawer(agentId) {
      const wrap = document.getElementById(`agentSingleSpecBody_${agentId}`);
      const btn = document.getElementById(`agentSingleSpecBtn_${agentId}`);
      if (!wrap) return;
      const isHidden = wrap.style.display === 'none';
      wrap.style.display = isHidden ? 'block' : 'none';
      if (btn) {
        btn.textContent = isHidden ? '▴ Hide Playbook & Governance' : '▾ View Playbook & Governance';
      }
      if (isHidden) {
        setTimeout(() => wrap.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 40);
      }
    }

    function openAndScrollToSpecSection(sectionId) {
      if (typeof lastAgentId !== 'undefined' && lastAgentId) {
        const wrap = document.getElementById(`agentSingleSpecBody_${lastAgentId}`);
        if (wrap) wrap.style.display = 'block';
      }
      const sec = document.getElementById(sectionId);
      if (sec) {
        setTimeout(() => sec.scrollIntoView({ behavior: 'smooth', block: 'start' }), 40);
      }
      return false;
    }

    function renderAgentAtAGlanceStrip(ag, dept) {
      return '';
    }

    function renderAgentFullSpecSheet(ag, dept, openByDefault = false) {
      const spec = ag.adkSpec || {};
      const cleanName = cleanAgentName(ag.name);
      const personaName = ag.primaryPersonaName || 'Supply Chain Lead';
      const subPillar = ag.subPillarName || dept.name;

      const sysStrings = toSysArray(ag.systems).map(s => toOpenTechLabel(s));
      const sysList = (spec.systems && spec.systems.length)
        ? spec.systems.map((s, idx) => toOpenTechLabel(s.name || sysStrings[idx] || 'Enterprise System'))
        : sysStrings.slice(0, 4);

      const standards = (ag.standardsCompliance && ag.standardsCompliance.length)
        ? ag.standardsCompliance.slice(0, 3).join(' · ')
        : 'ASCM SCOR DS · ISO 9001 · ISO/IEC 42001';

      return `
        <!-- ONE SIMPLE BUTTON FOR PLAYBOOK & GOVERNANCE -->
        <div class="sc-single-spec-trigger-bar" style="border-left: 5px solid ${dept.color};">
          <div>
            <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:2px;">
              🛡️ Enterprise Agent Governance
            </div>
            <div style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary);">
              Playbook, Guardrails &amp; Connected Systems
            </div>
          </div>

          <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
            <button type="button" id="agentSingleSpecBtn_${ag.id}" class="switch-pill" style="font-weight:800; padding:10px 18px;" onclick="toggleSingleAgentSpecDrawer('${ag.id}')">
              ${openByDefault ? '▴ Hide Playbook & Governance' : '▾ View Playbook & Governance'}
            </button>
          </div>
        </div>

        <!-- SIMPLE 3-CARD FLIPPABLE GOVERNANCE DRAWER (Hidden by default on #agent/<id>) -->
        <div id="agentSingleSpecBody_${ag.id}" class="sc-spec-section-card sc-spec-collapsible" style="display:${openByDefault ? 'block' : 'none'}; margin-top:0;">
          <div id="spec-governance" style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:16px;">
            <div class="sc-flip-card" style="--flip-accent:#10b981;" onclick="this.classList.toggle('is-flipped')">
              <div class="sc-flip-inner">
                <div class="sc-flip-front">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">✓ IN SCOPE</span>
                    <span class="sc-flip-hint">↻ Flip</span>
                  </div>
                  <div class="sc-flip-big-heading">Autonomous Execution</div>
                  <div class="sc-flip-sub-label">What ${cleanName} runs automatically</div>
                </div>
                <div class="sc-flip-back">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">AUTONOMOUS MANDATE</span>
                    <span class="sc-flip-hint">↺ Back</span>
                  </div>
                  <div class="sc-flip-back-text">
                    ${cleanSentence(ag.solution, 135)}
                  </div>
                </div>
              </div>
            </div>

            <div class="sc-flip-card" style="--flip-accent:#f59e0b;" onclick="this.classList.toggle('is-flipped')">
              <div class="sc-flip-inner">
                <div class="sc-flip-front">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">👤 HUMAN-IN-THE-LOOP</span>
                    <span class="sc-flip-hint">↻ Flip</span>
                  </div>
                  <div class="sc-flip-big-heading">Approval &amp; Guardrails</div>
                  <div class="sc-flip-sub-label">Managed by ${personaName}</div>
                </div>
                <div class="sc-flip-back">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">ESCALATION POLICY</span>
                    <span class="sc-flip-hint">↺ Back</span>
                  </div>
                  <div class="sc-flip-back-text">
                    Escalates to ${personaName} whenever financial or volume impact exceeds 20% plan variance or policy limits.
                  </div>
                </div>
              </div>
            </div>

            <div class="sc-flip-card" style="--flip-accent:#38bdf8;" onclick="this.classList.toggle('is-flipped')">
              <div class="sc-flip-inner">
                <div class="sc-flip-front">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">🔌 INTEGRATIONS</span>
                    <span class="sc-flip-hint">↻ Flip</span>
                  </div>
                  <div class="sc-flip-big-heading">${sysList.length || 3} Connected Systems</div>
                  <div class="sc-flip-sub-label">BigQuery · On-Prem DBs · 3rd-Party MCPs</div>
                </div>
                <div class="sc-flip-back">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">SYSTEMS &amp; STANDARDS</span>
                    <span class="sc-flip-hint">↺ Back</span>
                  </div>
                  <div class="sc-flip-back-text">
                    ${sysList.join(' · ')}. Compliant with ${standards}.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    function openAgentPage(agentId, pushHash = true, ev = null) {
      const ag = AGENTS[agentId];
      if (!ag) return;
      const useSlide = isPillOrNavSwitch(ev);
      const sRect = useSlide ? null : getClickedCardRect(ev);
      const transClass = getPageTransitionClass(ev, sRect);

      lastAgentId = agentId;
      const dept = getDeptMeta(ag.deptId);
      const cls = getAgentBuildClassification(ag);
      const backPersona = PERSONAS[lastPersonaId] || Object.values(PERSONAS)[0];
      const videoUrl = customVideos[ag.id] || ag.videoSrc;
      const hasVideo = Boolean(customVideos[ag.id]) || Boolean(ag.hasPreloadedVideo);

      const siblingAgents = Object.values(AGENTS).filter(a => a.deptId === dept.id && (!ag.subPillarId || a.subPillarId === ag.subPillarId));

      if (pushHash) {
        history.pushState({ page: 'agent', id: agentId }, '', `#agent/${agentId}`);
      }

      const container = document.getElementById('agentPageContent');
      container.innerHTML = `
        <div id="agentGenieWrap" class="${transClass}">
          <div class="back-bar">
            <div style="display:flex; gap:10px; flex-wrap:wrap;">
              <button type="button" class="back-btn" onclick="openPersonaPage('${backPersona.id}', true, event)">
                <span>&larr;</span>
                <span>Back to ${backPersona.name}</span>
              </button>
              <button type="button" class="back-btn" onclick="goToOrgChart()">
                <span>6 SCOR Pillars</span>
              </button>
            </div>

            <!-- 1-Click Sibling Agent Switcher Pills -->
            <div class="persona-switcher-pills">
              ${siblingAgents.map(other => `
                <button type="button"
                        class="switch-pill ${other.id === ag.id ? 'active' : ''}"
                        style="${other.id === ag.id ? `background:${dept.color}; border-color:${dept.color}; color:#ffffff; font-weight:700;` : ''}"
                        onclick="openAgentPage('${other.id}', true, event)">
                  🤖 ${cleanAgentName(other.name)}
                </button>
              `).join('')}
            </div>
          </div>

          <!-- 1. Clean Big-Heading Hero + 3 Simple Flippable Cards (Problem / Solution / Outcome) -->
          <div class="agent-hero-banner" style="padding: 28px 32px; margin-bottom: 22px;">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:18px;">
              <div style="display:flex; align-items:center; gap:14px;">
                <div class="ai-bot-square" style="width:52px; height:52px; font-size:24px;">✦</div>
                <div>
                  <h1 class="agent-title" style="font-size: clamp(26px, 3vw, 36px); margin: 0;">${cleanAgentName(ag.name)}</h1>
                  <div style="font-size:15px; color:var(--text-secondary); margin-top:4px; font-weight:700;">${ag.subPillarName || dept.name}</div>
                </div>
              </div>
              <span class="build-tier-badge ${cls.cssClass}">${cls.label}</span>
            </div>

            <!-- 3 Simple Flippable Summary Cards (Zero Clipping) -->
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:16px;">
              <div class="sc-flip-card" style="--flip-accent:#f43f5e;" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">✕ 01 · CHALLENGE</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading">The Bottleneck</div>
                    <div class="sc-flip-sub-label">Click to view operational gap</div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">✕ PROBLEM SOLVED</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">${cleanSentence(ag.problem, 135)}</div>
                  </div>
                </div>
              </div>

              <div class="sc-flip-card" style="--flip-accent:${dept.color};" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">✦ 02 · CAPABILITY</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading">AI Agent Solution</div>
                    <div class="sc-flip-sub-label">Click to view how it works</div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">✦ AGENTIC SOLUTION</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">${cleanSentence(ag.solution, 135)}</div>
                  </div>
                </div>
              </div>

              <div class="sc-flip-card" style="--flip-accent:#10b981;" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">🚀 03 · BUSINESS IMPACT</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading">${ag.badge || 'Verified ROI'}</div>
                    <div class="sc-flip-sub-label">Click to view quantified outcome</div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">🚀 VERIFIED OUTCOME</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">${cleanSentence(ag.outcome, 135)}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 2. Clean Full-SVG Execution Flow Diagram -->
          ${renderSimpleAgentArchitectureDiagram(ag, dept)}

          <!-- 3. 4 Clean Flippable Cost & Value KPI Cards -->
          ${renderAgentCostAndRoiPanel(ag, dept)}

          <!-- 4. Dedicated Box for a Video -->
          <div class="video-stage-box">
            <div class="video-toolbar" style="border-top:none; border-bottom:1px solid var(--border-subtle);">
              <span style="font-weight:700; color:var(--text-primary);">🎬 Agent Demo Video — ${cleanAgentName(ag.name)}</span>
              <div style="display:flex; flex-wrap:wrap; gap:8px;">
                <button type="button" class="upload-video-btn ${stageViewMode==='video'?'active':''}"
                        onclick="stageViewMode='video';openAgentPage('${ag.id}', false)">
                  <span>▶ Video Box</span>
                </button>
                <button type="button" class="upload-video-btn ${stageViewMode==='cad'?'active':''}"
                        onclick="stageViewMode='cad';openAgentPage('${ag.id}', false)">
                  <span>✦ Interactive Preview</span>
                </button>
                <label class="upload-video-btn" title="Attach an .mp4 demo video for this agent">
                  <span>📎 Attach Video (.mp4)</span>
                  <input type="file" accept="video/*" style="display:none;" onchange="attachAgentVideo(event, '${ag.id}')" />
                </label>
              </div>
            </div>

            <div class="video-viewport" id="agentVideoViewport" style="min-height: 360px;">
              ${stageViewMode === 'cad'
                ? renderInteractiveCadStage(ag.cadType || 'demand_wave', 'agentCadMount')
                : (hasVideo
                    ? `<video id="agentVideoPlayer" controls autoplay loop muted playsinline src="${videoUrl}"></video>`
                    : `
                      <div class="video-placeholder-stage">
                        <div class="video-placeholder-icon">▶</div>
                        <div style="font-family:var(--font-display); font-size:22px; font-weight:800; color:var(--text-primary);">
                          ${cleanAgentName(ag.name)} — Demo Studio
                        </div>
                        <div style="display:flex; gap:10px; margin-top:8px;">
                          <label class="upload-video-btn active" style="cursor:pointer;">
                            <span>📎 Attach .mp4 Video</span>
                            <input type="file" accept="video/*" style="display:none;" onchange="attachAgentVideo(event, '${ag.id}')" />
                          </label>
                          <button type="button" class="upload-video-btn" onclick="stageViewMode='cad';openAgentPage('${ag.id}', false)">
                            <span>✦ View Interactive Animation</span>
                          </button>
                        </div>
                      </div>
                    `)
              }
            </div>
          </div>

          <!-- 5. Simple 1-Button Playbook & Governance Drawer -->
          ${renderAgentFullSpecSheet(ag, dept, false)}
        </div>
      `;

      hydrateAssets();
      showActivePage('pageAgent');
      const wrap = document.getElementById('agentGenieWrap');
      if (sRect && wrap) {
        animateGenieOutOfBox(sRect, wrap, dept.color);
      }
    }

    function attachAgentVideo(event, agentId) {
      const file = event.target.files && event.target.files[0];
      if (!file) return;
      customVideos[agentId] = URL.createObjectURL(file);
      stageViewMode = 'video';
      openAgentPage(agentId, false);
    }

    function openAgentBlueprintPage(agentId, pushHash = true, ev = null, focusSectionId = null) {
      const ag = AGENTS[agentId];
      if (!ag) return;
      const useSlide = isPillOrNavSwitch(ev);
      const sRect = useSlide ? null : getClickedCardRect(ev);
      const transClass = getPageTransitionClass(ev, sRect);

      lastAgentId = agentId;
      const dept = getDeptMeta(ag.deptId);
      const siblingAgents = Object.values(AGENTS).filter(a => a.deptId === dept.id && (!ag.subPillarId || a.subPillarId === ag.subPillarId));

      if (pushHash) {
        history.pushState({ page: 'blueprint', id: agentId }, '', `#blueprint/${agentId}`);
      }

      const container = document.getElementById('blueprintPageContent');
      container.innerHTML = `
        <div id="blueprintGenieWrap" class="${transClass}">
          <div class="back-bar">
            <div style="display:flex; gap:10px; flex-wrap:wrap;">
              <button type="button" class="back-btn" onclick="openAgentPage('${ag.id}', true, event)">
                <span>&larr;</span>
                <span>Back to ${cleanAgentName(ag.name)}</span>
              </button>
              <button type="button" class="back-btn" onclick="goToOrgChart()">
                <span>6 SCOR Pillars</span>
              </button>
            </div>

            <div class="persona-switcher-pills">
              ${siblingAgents.map(other => `
                <button type="button"
                        class="switch-pill ${other.id === ag.id ? 'active' : ''}"
                        style="${other.id === ag.id ? `background:${dept.color}; border-color:${dept.color}; color:#ffffff; font-weight:700;` : ''}"
                        onclick="openAgentBlueprintPage('${other.id}', true, event)">
                  📋 ${cleanAgentName(other.name)}
                </button>
              `).join('')}
            </div>
          </div>

          ${renderAgentFullSpecSheet(ag, dept, true)}
        </div>
      `;

      hydrateAssets();
      showActivePage('pageBlueprint');
      const wrap = document.getElementById('blueprintGenieWrap');
      if (sRect && wrap) {
        animateGenieOutOfBox(sRect, wrap, dept.color);
      }
      if (focusSectionId) {
        openAndScrollToSpecSection(focusSectionId);
      } else {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }"""


def update_other_flip_cards(text: str) -> str:
    """Updates Persona Page, Value Chain Page, and Architecture Page flip cards to use full-width headings (no side-by-side icon clipping) and clean complete sentences."""
    # 1. Persona Page AI Agent Dock Cards
    p_start = "          <!-- Big-Heading Flippable AI Agent Cards for this Persona -->"
    p_end = "      hydrateAssets();\n      showActivePage('pagePersona');"
    ps = text.find(p_start)
    pe = text.find(p_end, ps)
    if ps != -1 and pe != -1:
        new_p_dock = """          <!-- Big-Heading Flippable AI Agent Cards for this Persona -->
          <div class="ai-agent-dock-box">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-bottom:16px;">
              <h2 style="font-family:var(--font-display); font-size:22px; font-weight:800; color:var(--text-primary); margin:0;">
                ✦ AI Agents for ${p.name}
              </h2>
              <span style="font-size:12.5px; color:var(--text-secondary); font-weight:600;">
                Click any card to flip for summary, or open the Agent
              </span>
            </div>

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:16px;">
              ${[...new Set(p.agentIds || [])].map(aid => {
                const ag = AGENTS[aid];
                if (!ag) return '';
                return `
                  <div class="sc-flip-card" style="--flip-accent:${dept.color};" onclick="this.classList.toggle('is-flipped')">
                    <div class="sc-flip-inner">
                      <div class="sc-flip-front">
                        <div class="sc-flip-top-row">
                          <span class="sc-flip-kicker">✦ ${ag.subPillarName || dept.name}</span>
                          <span class="sc-flip-hint">↻ Flip</span>
                        </div>
                        <div class="sc-flip-big-heading">${cleanAgentName(ag.name)}</div>
                        <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; flex-wrap:wrap; margin-top:4px;">
                          <span class="sc-flip-sub-label" style="color:#10b981; font-weight:700;">${ag.badge || 'Verified ROI'}</span>
                          <button type="button" class="agent-plug-btn" style="padding:7px 14px; font-size:12.5px;" onclick="event.stopPropagation(); openAgentPage('${ag.id}', true, event)">
                            <span>Open Agent &rarr;</span>
                          </button>
                        </div>
                      </div>
                      <div class="sc-flip-back">
                        <div class="sc-flip-top-row">
                          <span class="sc-flip-kicker">WHAT IT DOES</span>
                          <span class="sc-flip-hint">↺ Back</span>
                        </div>
                        <div class="sc-flip-back-text">${cleanSentence(ag.solution || ag.role, 125)}</div>
                        <div style="display:flex; align-items:center; justify-content:flex-end;">
                          <button type="button" class="agent-plug-btn" style="padding:7px 14px; font-size:12.5px;" onclick="event.stopPropagation(); openAgentPage('${ag.id}', true, event)">
                            <span>Open Studio &rarr;</span>
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
      `;

"""
        text = text[:ps] + new_p_dock + text[pe:]

    # 2. Value Chain 3 Stage Cards
    vc_start = "            <!-- 3 Big-Heading Flippable Stage Cards -->"
    vc_end = "            <!-- Distinct Human Persona Owner Card vs. AI Agent Card for This Stage -->"
    vs = text.find(vc_start)
    ve = text.find(vc_end, vs)
    if vs != -1 and ve != -1:
        new_vc = """            <!-- 3 Big-Heading Flippable Stage Cards -->
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:16px; margin: 16px 0;">
              <div class="sc-flip-card" style="--flip-accent:#38bdf8;" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">📥 01 · STAGE INPUT</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading">Connected Systems</div>
                    <div class="sc-flip-sub-label">${toSysArray(activeStage.systems).length} live data feeds</div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">SOURCE SYSTEMS</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">${toSysArray(activeStage.systems).map(s => toOpenTechLabel(s)).join(' · ')}</div>
                  </div>
                </div>
              </div>

              <div class="sc-flip-card" style="--flip-accent:${activeStage.color || vc.color};" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">⚡ 02 · AI EXECUTION</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading">${activeStage.toilTime} &rarr; ${activeStage.afterTime}</div>
                    <div class="sc-flip-sub-label">Autonomous ${activeStage.modality}</div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">AI ACTION</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">${cleanSentence(activeStage.after, 125)}</div>
                  </div>
                </div>
              </div>

              <div class="sc-flip-card" style="--flip-accent:#10b981;" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">🔗 03 · HANDOFF</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading">Downstream Output</div>
                    <div class="sc-flip-sub-label">Synchronized state handoff</div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">GOLDEN THREAD</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">${cleanSentence(activeStage.goldenThread, 125)}</div>
                  </div>
                </div>
              </div>
            </div>

"""
        text = text[:vs] + new_vc + text[ve:]

    # 3. Architecture Page 60-Agent Catalog Cards
    arch_start = "          <!-- ONE Single Button to Expand All 60 Flippable Agent Architecture Cards -->"
    arch_end = "      hydrateAssets();\n      showActivePage('pageArchitecture');"
    as_idx = text.find(arch_start)
    ae_idx = text.find(arch_end, as_idx)
    if as_idx != -1 and ae_idx != -1:
        new_arch = """          <!-- ONE Single Button to Expand All 60 Flippable Agent Architecture Cards -->
          <div class="sc-single-spec-trigger-bar" style="border-left: 5px solid #a855f7; margin-top: 8px;">
            <div>
              <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:#c084fc; margin-bottom:3px;">
                🤖 60-Agent Catalog
              </div>
              <div style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary);">
                Explore All 60 Agents by SCOR Pillar
              </div>
            </div>
            <button type="button" class="switch-pill" style="font-weight:800; padding:10px 18px;" onclick="const el=document.getElementById('archAll60MatrixDrawer'); if(el){const open=el.style.display==='none'; el.style.display=open?'block':'none'; this.textContent=open?'▴ Hide 60-Agent Catalog':'▾ Open 60-Agent Catalog';}">
              ${currentArchVerticalFilter !== 'all' ? '▴ Hide 60-Agent Catalog' : '▾ Open 60-Agent Catalog'}
            </button>
          </div>

          <div id="archAll60MatrixDrawer" style="display:${currentArchVerticalFilter !== 'all' ? 'block' : 'none'}; margin-top:16px;">
            <div class="dir-controls-bar" style="margin-bottom:22px;">
              <div style="display:flex; gap:8px; flex-wrap:wrap;">
                <button type="button"
                        class="switch-pill ${currentArchVerticalFilter === 'all' ? 'active' : ''}"
                        style="${currentArchVerticalFilter === 'all' ? 'background:#00d2ff; color:#040810; border-color:#00d2ff; font-weight:700;' : ''}"
                        onclick="filterArchVertical('all')">
                  All 60 Agents
                </button>
                ${Object.values(DEPARTMENTS).map(d => `
                  <button type="button"
                          class="switch-pill ${currentArchVerticalFilter === d.id ? 'active' : ''}"
                          style="${currentArchVerticalFilter === d.id ? `background:${d.color}; color:#040810; border-color:${d.color}; font-weight:700;` : ''}"
                          onclick="filterArchVertical('${d.id}')">
                    ${d.name} (${d.agentIds.length})
                  </button>
                `).join('')}
              </div>
            </div>

            ${Object.values(DEPARTMENTS)
              .filter(dept => currentArchVerticalFilter === 'all' || dept.id === currentArchVerticalFilter)
              .map(dept => {
                const deptAgents = Object.values(AGENTS).filter(a => a.deptId === dept.id);
                return `
                  <div style="margin-bottom: 28px;">
                    <h3 style="font-family:var(--font-display); font-size:20px; font-weight:800; color:var(--text-primary); margin-bottom:12px;">
                      ${dept.scorBadge} · ${dept.name} (${deptAgents.length})
                    </h3>
                    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:14px;">
                      ${deptAgents.map(ag => `
                        <div class="sc-flip-card" style="--flip-accent:${dept.color};" onclick="this.classList.toggle('is-flipped')">
                          <div class="sc-flip-inner">
                            <div class="sc-flip-front">
                              <div class="sc-flip-top-row">
                                <span class="sc-flip-kicker">✦ ${ag.subPillarName || dept.name}</span>
                                <span class="sc-flip-hint">↻ Flip</span>
                              </div>
                              <div class="sc-flip-big-heading">${cleanAgentName(ag.name)}</div>
                              <div style="display:flex; align-items:center; justify-content:space-between; gap:8px;">
                                <span class="sc-flip-sub-label" style="color:#10b981; font-weight:700;">${ag.badge || 'Verified ROI'}</span>
                                <button type="button" class="switch-pill" style="padding:5px 12px; font-size:12px;" onclick="event.stopPropagation(); openAgentPage('${ag.id}', true, event)">
                                  Open &rarr;
                                </button>
                              </div>
                            </div>
                            <div class="sc-flip-back">
                              <div class="sc-flip-top-row">
                                <span class="sc-flip-kicker">SUMMARY</span>
                                <span class="sc-flip-hint">↺ Back</span>
                              </div>
                              <div class="sc-flip-back-text">${cleanSentence(ag.solution || ag.role, 120)}</div>
                            </div>
                          </div>
                        </div>
                      `).join('')}
                    </div>
                  </div>
                `;
              }).join('')}
          </div>
        </div>
      `;

"""
        text = text[:as_idx] + new_arch + text[ae_idx:]

    return text


def update_file(path: Path):
    text = path.read_text(encoding="utf-8")

    # 1. Replace FLIP_AND_SINGLE_TAB_CSS block
    css_start = text.find("    /* =========================================================================\n       3D FLIPPABLE CARDS")
    css_end = text.find("    .sc-spec-sec-head {")
    if css_start != -1 and css_end != -1 and css_start < css_end:
        text = text[:css_start] + CLEAN_FLIP_CSS.lstrip("\n") + "\n" + text[css_end:]

    # 2. Replace shortStepHeading .. openAgentBlueprintPage
    start_marker = "    function shortStepHeading("
    if start_marker not in text:
        start_marker = "    function renderSimpleAgentArchitectureDiagram(ag, dept) {"
    s_idx = text.find(start_marker)
    e_idx = text.find("    function selectDemoTableTab(", s_idx)
    if s_idx == -1 or e_idx == -1:
        raise RuntimeError(f"Could not locate JS markers in {path}")

    text = text[:s_idx] + NEW_SIMPLE_AGENT_JS + "\n\n" + text[e_idx:]

    # 3. Update Persona, Value Chain & Architecture flip cards
    text = update_other_flip_cards(text)

    path.write_text(text, encoding="utf-8")
    print(f"Updated {path.name}")


if __name__ == "__main__":
    for f in HTML_FILES:
        if f.exists():
            update_file(f)

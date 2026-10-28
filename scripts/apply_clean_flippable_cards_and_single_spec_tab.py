#!/usr/bin/env python3
"""
Transforms text-heavy cards across the website into clean, Big-Heading 3D Flippable Cards
(.sc-flip-card) with minimal, high-impact text on the back, and consolidates all 6 Agent
Specification sections (01 · Playbook & Governance through 06 · Evals & Proof) under ONE
single expandable button / 6-Tab switcher on the main Agent page (#agent/<id>).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HTML_FILES = [
    ROOT / "index.html",
    ROOT / "periodic_table.html",
    ROOT / "mind_map.html",
]

FLIP_AND_SINGLE_TAB_CSS = """
    /* =========================================================================
       3D FLIPPABLE CARDS (.sc-flip-card) — BIG HEADINGS ON FRONT, CLEAN CONCISE BACK
       ========================================================================= */
    .sc-flip-card {
      perspective: 1100px;
      cursor: pointer;
      user-select: none;
      min-height: 178px;
      position: relative;
    }
    .sc-flip-card.sc-flip-tall {
      min-height: 204px;
    }
    .sc-flip-card.sc-flip-compact {
      min-height: 148px;
    }
    .sc-flip-inner {
      position: relative;
      width: 100%;
      height: 100%;
      min-height: inherit;
      transition: transform 0.52s cubic-bezier(0.22, 1, 0.36, 1);
      transform-style: preserve-3d;
    }
    .sc-flip-card.is-flipped .sc-flip-inner {
      transform: rotateY(180deg);
    }
    .sc-flip-front,
    .sc-flip-back {
      position: absolute;
      inset: 0;
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      border-radius: 16px;
      padding: 18px 20px;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      border-top: 4px solid var(--flip-accent, #38bdf8);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 8px 22px rgba(0, 0, 0, 0.16);
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
      overflow: hidden;
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
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.24);
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
      font-size: 10.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      color: var(--flip-accent, #38bdf8);
    }
    .sc-flip-hint {
      font-family: var(--font-mono);
      font-size: 10.5px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 999px;
      background: rgba(148, 163, 184, 0.12);
      color: var(--text-secondary);
      border: 1px solid var(--border-subtle);
      white-space: nowrap;
    }
    .sc-flip-big-heading {
      font-family: var(--font-display);
      font-size: 20px;
      font-weight: 800;
      color: var(--text-primary);
      line-height: 1.22;
      margin: 8px 0 6px;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .sc-flip-icon-box {
      width: 42px;
      height: 42px;
      border-radius: 12px;
      background: rgba(148, 163, 184, 0.1);
      border: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      flex-shrink: 0;
    }
    .sc-flip-back-text {
      font-size: 13.5px;
      font-weight: 600;
      color: var(--text-primary);
      line-height: 1.48;
      margin: 6px 0;
    }
    .sc-flip-bottom-pills {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }
    .sc-flip-pill {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      padding: 3px 9px;
      border-radius: 999px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
    }

    /* Single Master Button + 6-Tab Spec Switcher */
    .sc-single-spec-trigger-bar {
      margin-top: 22px;
      margin-bottom: 14px;
      padding: 22px 28px;
      border-radius: 20px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 16px;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
    }
    html[data-theme="light"] .sc-single-spec-trigger-bar {
      background: #ffffff;
      border-color: rgba(15, 23, 42, 0.12);
      box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
    }
    .sc-spec-tabs-nav {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      padding-bottom: 16px;
      margin-bottom: 18px;
      border-bottom: 1px solid var(--border-subtle);
    }
    .sc-spec-tab-btn {
      padding: 9px 16px;
      border-radius: 999px;
      font-family: var(--font-display);
      font-size: 13.5px;
      font-weight: 800;
      color: var(--text-secondary);
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      cursor: pointer;
      transition: all 0.18s ease;
    }
    .sc-spec-tab-btn:hover {
      color: var(--text-primary);
      transform: translateY(-1px);
    }
    .sc-spec-tab-btn.active {
      background: var(--spec-accent, #2563eb);
      border-color: var(--spec-accent, #2563eb);
      color: #ffffff;
      box-shadow: 0 6px 16px rgba(37, 99, 235, 0.25);
    }
    .sc-spec-tab-pane {
      display: none;
    }
    .sc-spec-tab-pane.active {
      display: block;
      animation: fadeIn 0.22s ease;
    }
"""


NEW_ARCH_COST_SPEC_BLOCK = """    function shortStepHeading(rawTitle, fallback) {
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

      // 1. Open, Technology-First Connected Systems (MCPs, On-Prem DBs, BigQuery, REST/EDI)
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

      // 2. Real Fixture Tables & Query/Action Tools for this agent
      const tables = (adk.fixtureTables || []).map(t => t.table_name);
      const tbl1 = tables[0] || 'primary_twin_ledger';
      const tbl2 = tables[1] || tables[0] || 'signal_telemetry';
      const tbl3 = tables[2] || tables[1] || 'constraint_audit';

      const rawTools = (spec.toolsMeta && spec.toolsMeta.length)
        ? spec.toolsMeta.map(t => t.name)
        : (adk.tools || []).filter(t => t !== 'list_systems');
      const qTools = rawTools.filter(t => !String(t).startsWith('action_'));
      const aTools = rawTools.filter(t => String(t).startsWith('action_'));
      const q1 = qTools[0] || 'query_domain_signals';
      const q2 = qTools[1] || qTools[0] || 'query_twin_constraints';
      const a1 = aTools[0] || 'action_commit_writeback';

      // 3. Real 3 A2A Sub-Agents for this agent
      const rawSubs = (ag.subAgents && ag.subAgents.length >= 3)
        ? ag.subAgents.slice(0, 3)
        : [
            { name: 'Signal Context Node', role: 'Streams & validates live operational inputs' },
            { name: 'Optimization Engine', role: 'Evaluates constraints & ranks actions' },
            { name: 'Write-Back Dispatcher', role: 'Enforces quality gates & signed payloads' }
          ];
      const subs = rawSubs.map(sa => ({
        name: toOpenTechLabel(sa.name),
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
      });

      const flipSteps = [
        {
          kicker: '01 · INGEST',
          icon: ic1,
          heading: 'Open Connectors',
          frontPill: `🔌 ${sysArr.length || 3} Systems`,
          accent: dept.color,
          backText: `Ingests live state via MCP, REST/EDI, or On-Prem DB adapters from ${trunc(sys1, 32)}.`,
          backPills: [trunc(sys1, 24), trunc(sys2, 24)]
        },
        {
          kicker: '02 · NORMALIZE',
          icon: tMeta.icons[1],
          heading: shortStepHeading(subs[0].name, 'State Normalizer'),
          frontPill: `🗄️ ${tables.length || 4} Tables`,
          accent: '#38bdf8',
          backText: shortSentence(subs[0].role, 88),
          backPills: [q1, tbl1]
        },
        {
          kicker: '03 · SOLVE',
          icon: tMeta.icons[2],
          heading: shortStepHeading(subs[1].name, 'AI & Math Solver'),
          frontPill: '🧠 Gemini 3.8 + 4 Argon',
          accent: cls.color,
          backText: shortSentence(`${subs[1].role} using ${solverLabel}.`, 88),
          backPills: ['gemini-3.8-flash', 'gemini-3.1-pro / 4-argon']
        },
        {
          kicker: '04 · GOVERN',
          icon: tMeta.icons[3],
          heading: shortStepHeading(subs[2].name, 'Safety & Policy Gate'),
          frontPill: '🛡️ Pre-Gate Verified',
          accent: '#f59e0b',
          backText: 'Verifies idempotency_key, schema contracts & delegation thresholds before commit.',
          backPills: ['enforce_tool_contract()', 'HITL Escalation']
        },
        {
          kicker: '05 · ACTUATE',
          icon: tMeta.icons[4],
          heading: 'MCP / API Write-Back',
          frontPill: `⚡ ${trunc(ag.badge || 'Signed Commit', 18)}`,
          accent: '#10b981',
          backText: `Commits governed payload via ${trunc(writebackFull, 38)} and renders VegaChart.`,
          backPills: [a1, 'A2UI VegaChart']
        }
      ];

      return `
        <div class="simple-arch-card">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:14px;">
            <div>
              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:4px;">
                <span style="font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color};">
                  ${tMeta.badge}
                </span>
                <span class="sc-spec-count-badge" style="font-size:11px;">
                  ⏱️ ${cadence}
                </span>
              </div>
              <h2 style="font-family:var(--font-display); font-size:24px; font-weight:800; color:var(--text-primary); margin:0;">
                Execution Flow — ${cleanName}
              </h2>
            </div>

            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="sc-spec-count-badge" style="color:#10b981; border-color:rgba(16,185,129,0.35);">
                🔌 BigQuery · On-Prem DBs · 3rd-Party MCPs · REST/EDI
              </span>
            </div>
          </div>

          <!-- Custom Agent-Specific Animated Full-Canvas SVG Flow Diagram -->
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

          <!-- 5 Big-Heading Flippable Step Cards (Zero Paragraph Clutter on Front; Click to Flip) -->
          <div class="ag-flow-steps-grid" style="margin-top:16px;">
            ${flipSteps.map(st => `
              <div class="sc-flip-card" style="--flip-accent:${st.accent};" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">${st.kicker}</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading">
                      <div class="sc-flip-icon-box">${st.icon}</div>
                      <span>${st.heading}</span>
                    </div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">${st.frontPill}</span>
                    </div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">${st.kicker}</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">${st.backText}</div>
                    <div class="sc-flip-bottom-pills">
                      ${st.backPills.map(p => `<span class="sc-flip-pill">${p}</span>`).join('')}
                    </div>
                  </div>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    /* =========================================================================
       CLEAN AGENT COST & VALUE FLIPPABLE CARDS + 1-BUTTON BREAKDOWN DRAWER
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
      const llmMo = Math.round(mb.llmFsp3YrUsd);
      const compMo = Math.round(mb.computeUsd);
      const dataMo = Math.round(mb.dataUsd + mb.apiUsd);
      const totalParts = Math.max(1, llmMo + compMo + dataMo);
      const llmPct = Math.round((llmMo / totalParts) * 100);
      const compPct = Math.round((compMo / totalParts) * 100);
      const dataPct = Math.max(1, 100 - llmPct - compPct);
      const valMo = Math.round(vm.grossAnnualConservativeUsd / 12);

      return `
        <div class="simple-arch-card" style="margin-top: 22px; margin-bottom: 22px;">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
            <div>
              <div style="font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:3px;">
                FinOps &amp; Business ROI
              </div>
              <h2 style="font-family:var(--font-display); font-size:24px; font-weight:800; color:var(--text-primary); margin:0;">
                Cost vs. Value — ${cleanAgentName(ag.name)}
              </h2>
            </div>

            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <button type="button" class="switch-pill" onclick="const el=document.getElementById('costBarsDrawer_${ag.id}'); if(el){const open=el.style.display==='none'; el.style.display=open?'grid':'none'; this.textContent=open?'▴ Hide Breakdown Bars':'▾ View Breakdown Bars';}">
                ▾ View Breakdown Bars
              </button>
              <button type="button" class="switch-pill" onclick="openCostTabPage('${ag.deptId}', '${ag.id}', true)">
                📊 Cost Calculator &rarr;
              </button>
            </div>
          </div>

          <!-- 4 Big-Heading Flippable KPI Cards -->
          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap:14px;">
            <div class="sc-flip-card sc-flip-compact" style="--flip-accent:${dept.color};" onclick="this.classList.toggle('is-flipped')">
              <div class="sc-flip-inner">
                <div class="sc-flip-front">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">✦ AI AGENT COST</span>
                    <span class="sc-flip-hint">↻ Flip</span>
                  </div>
                  <div style="font-family:var(--font-display); font-size:30px; font-weight:800; color:var(--text-primary);">
                    $${aiMo.toLocaleString()}<span style="font-size:15px; font-weight:600; color:var(--text-secondary);">/mo</span>
                  </div>
                  <div class="sc-flip-bottom-pills">
                    <span class="sc-flip-pill">Infra + Tokens</span>
                  </div>
                </div>
                <div class="sc-flip-back">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">UNIT ECONOMICS</span>
                    <span class="sc-flip-hint">↺ Back</span>
                  </div>
                  <div class="sc-flip-back-text">
                    $${mb.blendedCostPer1kCallsUsd.toFixed(2)} per 1K runs · Pilot scale: $${mb.pilotScaleMoUsd.toFixed(0)}/mo.
                  </div>
                  <div class="sc-flip-bottom-pills">
                    <span class="sc-flip-pill">🟢 LLM $${llmMo}</span>
                    <span class="sc-flip-pill">🔵 Compute $${compMo}</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="sc-flip-card sc-flip-compact" style="--flip-accent:#f43f5e;" onclick="this.classList.toggle('is-flipped')">
              <div class="sc-flip-inner">
                <div class="sc-flip-front">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">✕ MANUAL EFFORT</span>
                    <span class="sc-flip-hint">↻ Flip</span>
                  </div>
                  <div style="font-family:var(--font-display); font-size:30px; font-weight:800; color:var(--text-primary);">
                    $${mc.manualMonthlyCostUsd.toLocaleString()}<span style="font-size:15px; font-weight:600; color:var(--text-secondary);">/mo</span>
                  </div>
                  <div class="sc-flip-bottom-pills">
                    <span class="sc-flip-pill">~${mc.fteEquivalent} FTE Baseline</span>
                  </div>
                </div>
                <div class="sc-flip-back">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">MANUAL BASELINE</span>
                    <span class="sc-flip-hint">↺ Back</span>
                  </div>
                  <div class="sc-flip-back-text">
                    Replaces ~${mc.manualHoursPerMonth} hrs/mo of manual spreadsheet &amp; exception rework.
                  </div>
                  <div class="sc-flip-bottom-pills">
                    <span class="sc-flip-pill">${mc.manualHoursPerMonth} hrs/mo</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="sc-flip-card sc-flip-compact" style="--flip-accent:#38bdf8;" onclick="this.classList.toggle('is-flipped')">
              <div class="sc-flip-inner">
                <div class="sc-flip-front">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">⚡ PROCESS SAVINGS</span>
                    <span class="sc-flip-hint">↻ Flip</span>
                  </div>
                  <div style="font-family:var(--font-display); font-size:30px; font-weight:800; color:#38bdf8;">
                    ${mc.directSavingsPct}%<span style="font-size:15px; font-weight:600; color:var(--text-secondary);"> Less</span>
                  </div>
                  <div class="sc-flip-bottom-pills">
                    <span class="sc-flip-pill">-$${mc.directMonthlySavingsUsd.toLocaleString()}/mo</span>
                  </div>
                </div>
                <div class="sc-flip-back">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">NET SAVINGS</span>
                    <span class="sc-flip-hint">↺ Back</span>
                  </div>
                  <div class="sc-flip-back-text">
                    Saves $${mc.directMonthlySavingsUsd.toLocaleString()}/mo directly vs. manual analyst effort.
                  </div>
                  <div class="sc-flip-bottom-pills">
                    <span class="sc-flip-pill">~${cm.eventsPerDay.toLocaleString()} runs/day</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="sc-flip-card sc-flip-compact" style="--flip-accent:#10b981;" onclick="this.classList.toggle('is-flipped')">
              <div class="sc-flip-inner">
                <div class="sc-flip-front">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">🚀 VALUE UNLOCKED</span>
                    <span class="sc-flip-hint">↻ Flip</span>
                  </div>
                  <div style="font-family:var(--font-display); font-size:30px; font-weight:800; color:#10b981;">
                    $${(vm.grossAnnualConservativeUsd / 1e6).toFixed(2)}M<span style="font-size:15px; font-weight:600; color:var(--text-secondary);">/yr</span>
                  </div>
                  <div class="sc-flip-bottom-pills">
                    <span class="sc-flip-pill">${vm.cloudRoiMultipleConservative}x Cloud ROI</span>
                  </div>
                </div>
                <div class="sc-flip-back">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">ANNUAL IMPACT</span>
                    <span class="sc-flip-hint">↺ Back</span>
                  </div>
                  <div class="sc-flip-back-text">
                    Unlocks ~$${(valMo / 1000).toFixed(1)}K/mo in inventory, margin &amp; SLA protection.
                  </div>
                  <div class="sc-flip-bottom-pills">
                    <span class="sc-flip-pill">${ag.badge || 'Verified ROI'}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Collapsible Visual Breakdown Bars (Hidden by Default for Clean Main Page) -->
          <div id="costBarsDrawer_${ag.id}" style="display:none; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:14px; margin-top:14px;">
            <div style="padding:14px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle);">
              <div style="font-size:11.5px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; margin-bottom:10px;">
                Monthly Cost vs. Manual &amp; Value
              </div>
              <div style="margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between; font-size:12.5px; margin-bottom:3px;">
                  <span>✦ AI Agent</span><strong>$${aiMo.toLocaleString()}/mo</strong>
                </div>
                <div style="height:7px; border-radius:999px; background:var(--border-subtle); overflow:hidden;">
                  <div style="width:4%; min-width:8px; height:100%; background:${dept.color};"></div>
                </div>
              </div>
              <div style="margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between; font-size:12.5px; margin-bottom:3px;">
                  <span>✕ Manual Effort</span><strong style="color:#f43f5e;">$${mc.manualMonthlyCostUsd.toLocaleString()}/mo</strong>
                </div>
                <div style="height:7px; border-radius:999px; background:var(--border-subtle); overflow:hidden;">
                  <div style="width:36%; height:100%; background:#f43f5e;"></div>
                </div>
              </div>
              <div>
                <div style="display:flex; justify-content:space-between; font-size:12.5px; margin-bottom:3px;">
                  <span>🚀 Value Created</span><strong style="color:#10b981;">$${valMo.toLocaleString()}/mo</strong>
                </div>
                <div style="height:7px; border-radius:999px; background:var(--border-subtle); overflow:hidden;">
                  <div style="width:100%; height:100%; background:#10b981;"></div>
                </div>
              </div>
            </div>

            <div style="padding:14px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); display:flex; flex-direction:column; justify-content:space-between;">
              <div>
                <div style="display:flex; justify-content:space-between; font-size:11.5px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; margin-bottom:10px;">
                  <span>Monthly Infra &amp; Token Split</span><span>~${cm.eventsPerDay.toLocaleString()} runs/day</span>
                </div>
                <div style="height:10px; border-radius:999px; background:var(--border-subtle); overflow:hidden; display:flex; gap:2px; margin-bottom:12px;">
                  <div style="width:${llmPct}%; height:100%; background:#10b981;"></div>
                  <div style="width:${compPct}%; height:100%; background:#38bdf8;"></div>
                  <div style="width:${dataPct}%; height:100%; background:#a855f7;"></div>
                </div>
              </div>
              <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:8px;">
                <div style="padding:8px; border-radius:10px; background:var(--bg-surface); border:1px solid var(--border-subtle); font-size:12px;">
                  🟢 LLM: <strong>$${llmMo}</strong> (${llmPct}%)
                </div>
                <div style="padding:8px; border-radius:10px; background:var(--bg-surface); border:1px solid var(--border-subtle); font-size:12px;">
                  🔵 ADK: <strong>$${compMo}</strong> (${compPct}%)
                </div>
                <div style="padding:8px; border-radius:10px; background:var(--bg-surface); border:1px solid var(--border-subtle); font-size:12px;">
                  🟣 Data: <strong>$${dataMo}</strong> (${dataPct}%)
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    function inferColumnTypeAndConstraint(colName, rows) {
      const c = String(colName || '').toLowerCase();
      const isPk = c.endsWith('_id') && (c === Object.keys(rows[0] || {})[0]?.toLowerCase());
      const vals = (rows || []).map(r => r && r[colName]).filter(v => v !== undefined && v !== null && v !== '');
      const firstVal = vals[0];

      let colType = 'string';
      if (typeof firstVal === 'boolean' || c.endsWith('_flag')) {
        colType = 'boolean';
      } else if (typeof firstVal === 'number' || c.endsWith('_pct') || c.endsWith('_usd') || c.endsWith('_units') || c.endsWith('_days') || c.endsWith('_score') || c.endsWith('_count')) {
        colType = Number.isInteger(firstVal) ? 'integer' : 'numeric(12,2)';
      } else if (c.includes('timestamp') || c.endsWith('_at') || c.endsWith('_date')) {
        colType = 'timestamp';
      } else if (c.endsWith('_id') || c.endsWith('_code') || c === 'sku' || c === 'region') {
        colType = 'string (key)';
      }

      const uniqSamples = [];
      for (const v of vals) {
        const s = typeof v === 'object' ? JSON.stringify(v) : String(v);
        if (!uniqSamples.includes(s)) uniqSamples.push(s);
        if (uniqSamples.length >= 2) break;
      }
      const sampleStr = uniqSamples.map(s => s.length > 28 ? s.slice(0, 27) + '…' : s).join(', ');
      return { colType, isPk, sampleStr };
    }

    function computeAgentSpecStats(ag) {
      const adk = ag.adkImplementation || {};
      const spec = ag.adkSpec || {};
      const tables = adk.fixtureTables || [];
      const totalFields = tables.reduce((acc, t) => acc + ((t.columns || []).length), 0);
      const sysArr = (spec.systems && spec.systems.length) ? spec.systems : toSysArray(ag.systems);
      const toolsList = (spec.toolsMeta && spec.toolsMeta.length)
        ? spec.toolsMeta
        : (adk.tools || []).filter(t => t !== 'list_systems').map(t => ({ name: t }));
      const stepsCount = (ag.subAgents && ag.subAgents.length) ? ag.subAgents.length : 3;
      const evalsCount = (spec.evalScenarios && spec.evalScenarios.length) ? spec.evalScenarios.length : 1;
      return {
        systemsCount: sysArr.length || 4,
        entitiesCount: tables.length || 4,
        fieldsCount: totalFields || 36,
        toolsCount: toolsList.length || 6,
        stepsCount,
        evidenceRulesCount: Math.max(2, tables.length > 0 ? Math.min(4, tables.length) : 2),
        evalsCount,
        anomaliesCount: Math.max(1, tables.length >= 3 ? 2 : 1)
      };
    }

    function switchAgentSpecTab(agentId, tabKey, btnEl) {
      const wrap = document.getElementById(`agentSingleSpecBody_${agentId}`);
      if (!wrap) return;
      wrap.style.display = 'block';
      const toggleBtn = document.getElementById(`agentSingleSpecBtn_${agentId}`);
      if (toggleBtn) toggleBtn.textContent = '▴ Hide Playbook & Technical Specs';

      wrap.querySelectorAll('.sc-spec-tab-btn').forEach(b => {
        b.classList.toggle('active', b.getAttribute('data-spec-tab') === tabKey);
      });
      wrap.querySelectorAll('.sc-spec-tab-pane').forEach(p => {
        p.classList.toggle('active', p.getAttribute('data-spec-pane') === tabKey);
      });
    }

    function toggleSingleAgentSpecDrawer(agentId) {
      const wrap = document.getElementById(`agentSingleSpecBody_${agentId}`);
      const btn = document.getElementById(`agentSingleSpecBtn_${agentId}`);
      if (!wrap) return;
      const isHidden = wrap.style.display === 'none';
      wrap.style.display = isHidden ? 'block' : 'none';
      if (btn) {
        btn.textContent = isHidden ? '▴ Hide Playbook & Technical Specs' : '▾ Open Playbook, Governance & Technical Specs';
      }
      if (isHidden) {
        setTimeout(() => wrap.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 40);
      }
    }

    function openAndScrollToSpecSection(sectionId, childId = null) {
      const mapTab = {
        'spec-governance': 'governance',
        'spec-workflow': 'workflow',
        'spec-tools': 'tools',
        'spec-systems': 'systems',
        'spec-data-model': 'datamodel',
        'spec-evals': 'evals'
      };
      const tabKey = mapTab[sectionId] || 'governance';
      if (typeof lastAgentId !== 'undefined' && lastAgentId) {
        switchAgentSpecTab(lastAgentId, tabKey);
      }
      const sec = document.getElementById(sectionId);
      if (sec) {
        setTimeout(() => sec.scrollIntoView({ behavior: 'smooth', block: 'start' }), 40);
      }
      return false;
    }

    function renderAgentAtAGlanceStrip(ag, dept, isDedicatedSpecPage = false) {
      const st = computeAgentSpecStats(ag);
      return `
        <div class="sc-spec-stats-strip">
          <div class="sc-spec-stat-box"><span class="sc-spec-stat-num" style="color:${dept.color};">${st.systemsCount}</span><span class="sc-spec-stat-label">systems</span></div>
          <div class="sc-spec-stat-box"><span class="sc-spec-stat-num">${st.entitiesCount}</span><span class="sc-spec-stat-label">entities</span></div>
          <div class="sc-spec-stat-box"><span class="sc-spec-stat-num">${st.fieldsCount}</span><span class="sc-spec-stat-label">fields</span></div>
          <div class="sc-spec-stat-box"><span class="sc-spec-stat-num">${st.toolsCount}</span><span class="sc-spec-stat-label">tools</span></div>
          <div class="sc-spec-stat-box"><span class="sc-spec-stat-num">${st.stepsCount}</span><span class="sc-spec-stat-label">stages</span></div>
          <div class="sc-spec-stat-box"><span class="sc-spec-stat-num">${st.evidenceRulesCount}</span><span class="sc-spec-stat-label">rules</span></div>
          <div class="sc-spec-stat-box"><span class="sc-spec-stat-num">${st.evalsCount}</span><span class="sc-spec-stat-label">evals</span></div>
          <div class="sc-spec-stat-box"><span class="sc-spec-stat-num">${st.anomaliesCount}</span><span class="sc-spec-stat-label">anomalies</span></div>
        </div>
      `;
    }

    function renderAgentFullSpecSheet(ag, dept, openByDefault = false) {
      const adk = ag.adkImplementation || {};
      const spec = ag.adkSpec || {};
      const cleanName = cleanAgentName(ag.name);
      const personaName = ag.primaryPersonaName || 'Supply Chain Operations Lead';
      const subPillar = ag.subPillarName || dept.name;
      const tables = adk.fixtureTables || [];
      const totalFields = tables.reduce((acc, t) => acc + ((t.columns || []).length), 0);

      // 1. Tools metadata
      const rawTools = (spec.toolsMeta && spec.toolsMeta.length)
        ? spec.toolsMeta
        : (adk.tools || []).filter(t => t !== 'list_systems').map(tName => {
            const isAct = String(tName).startsWith('action_');
            return {
              name: tName,
              kind: isAct ? 'action' : 'query',
              description: isAct
                ? `Executes governed write-back (${tName}) after pre-execution gate & idempotency validation.`
                : `Queries live records from connected ${subPillar} tables (${tName}).`,
              inputs: isAct ? ['target_id', 'rationale', 'idempotency_key'] : ['lookup_key', 'region', 'sku_id'],
              outputs: isAct ? ['action_id', 'status', 'idempotency_key'] : ['records', 'total_count'],
              table: tables[0]?.table_name || 'supply_chain_records'
            };
          });

      const queryTools = rawTools.filter(t => t.kind === 'query');
      const actionTools = rawTools.filter(t => t.kind === 'action');
      const writeToolNames = actionTools.map(t => t.name).join(', ') || 'action_commit_writeback';

      // 2. Source systems metadata
      const sysStrings = toSysArray(ag.systems).map(s => toOpenTechLabel(s));
      const sysList = (spec.systems && spec.systems.length)
        ? spec.systems.map((s, idx) => {
            const ownedTables = (s.tables && s.tables.length)
              ? s.tables
              : (tables[idx] ? [tables[idx].table_name] : (tables[0] ? [tables[0].table_name] : []));
            const hasWrite = idx === spec.systems.length - 1 && actionTools.length > 0;
            return {
              name: toOpenTechLabel(s.name || sysStrings[idx] || 'Enterprise System'),
              protocol: toOpenTechLabel(s.protocol || 'MCP / REST / SQL Adapter'),
              mode: hasWrite ? 'read / write' : 'read',
              ownedTables
            };
          })
        : sysStrings.slice(0, 4).map((sName, idx) => ({
            name: sName,
            protocol: idx === 0 ? 'MCP / REST / On-Prem Adapter' : 'BigQuery / Analytical SQL / EDI',
            mode: idx === 0 ? 'read / write' : 'read',
            ownedTables: tables[idx] ? [tables[idx].table_name] : []
          }));

      // 3. Workflow Stages
      const subs = (ag.subAgents && ag.subAgents.length >= 3)
        ? ag.subAgents.slice(0, 3)
        : [
            { name: 'Signal Context Node', role: 'Streams & validates live operational records' },
            { name: 'Optimization Engine', role: 'Evaluates multi-echelon constraints & trade-offs' },
            { name: 'Write-Back Dispatcher', role: 'Enforces quality gates & commits signed payloads' }
          ];

      // 4. Golden Eval Scenario
      const evalObj = (spec.evalScenarios && spec.evalScenarios[0]) || {
        scenario_id: `SCENARIO-${ag.id.toUpperCase().slice(0, 12)}-01`,
        name: `${cleanName} Golden Eval`,
        query: `Execute ${cleanName} for the current horizon, cite table evidence, and commit governed remediation.`,
        expected_proof_obligations: [
          `Query primary ${subPillar} records from ${(tables[0]?.table_name) || 'digital_twin'}`,
          `Validate constraints before invoking ${writeToolNames}`,
          `Emit A2UI VegaChart and copy-ready markdown table`
        ],
        sla_seconds: 15
      };

      const standards = (ag.standardsCompliance && ag.standardsCompliance.length)
        ? ag.standardsCompliance
        : ['ASCM SCOR DS v14.0', 'ISO 9001:2015', 'Google ADK + A2A + MCP + A2UI v0.9', 'ISO/IEC 42001'];

      return `
        <!-- ONE SINGLE BUTTON / BAR ON THE MAIN AGENT PAGE -->
        <div class="sc-single-spec-trigger-bar" style="border-left: 5px solid ${dept.color};">
          <div>
            <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:3px;">
              🛡️ Enterprise Agent Contract · Playbook, Governance &amp; Technical Specification
            </div>
            <div style="font-family:var(--font-display); font-size:22px; font-weight:800; color:var(--text-primary);">
              ${cleanName} — Deep-Dive Specification
            </div>
          </div>

          <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
            <button type="button" id="agentSingleSpecBtn_${ag.id}" class="switch-pill" style="font-weight:800; padding:10px 18px;" onclick="toggleSingleAgentSpecDrawer('${ag.id}')">
              ${openByDefault ? '▴ Hide Playbook & Technical Specs' : '▾ Open Playbook, Governance & Technical Specs'}
            </button>
            ${!openByDefault ? `
              <button type="button" class="switch-pill" style="background:${dept.color}; border-color:${dept.color}; color:#ffffff; font-weight:800; padding:10px 18px;" onclick="openAgentBlueprintPage('${ag.id}', true, event, 'spec-governance')">
                📄 Open in Dedicated Page &rarr;
              </button>
            ` : ''}
          </div>
        </div>

        <!-- EXPANDABLE 6-TAB SPECIFICATION CONTAINER (Hidden by default on #agent/<id>, Open on #blueprint/<id>) -->
        <div id="agentSingleSpecBody_${ag.id}" class="sc-spec-section-card sc-spec-collapsible" style="display:${openByDefault ? 'block' : 'none'}; margin-top:0; --spec-accent:${dept.color};">
          ${renderAgentAtAGlanceStrip(ag, dept, true)}

          <!-- Clean 6-Tab Switcher Bar -->
          <div class="sc-spec-tabs-nav" style="margin-top:16px;">
            <button type="button" class="sc-spec-tab-btn active" data-spec-tab="governance" onclick="switchAgentSpecTab('${ag.id}', 'governance', this)">
              🛡️ 01 · Playbook &amp; Governance
            </button>
            <button type="button" class="sc-spec-tab-btn" data-spec-tab="workflow" onclick="switchAgentSpecTab('${ag.id}', 'workflow', this)">
              ⚡ 02 · 3-Stage Workflow
            </button>
            <button type="button" class="sc-spec-tab-btn" data-spec-tab="tools" onclick="switchAgentSpecTab('${ag.id}', 'tools', this)">
              🔧 03 · Agent Tools (${rawTools.length})
            </button>
            <button type="button" class="sc-spec-tab-btn" data-spec-tab="systems" onclick="switchAgentSpecTab('${ag.id}', 'systems', this)">
              🔌 04 · Source Systems (${sysList.length})
            </button>
            <button type="button" class="sc-spec-tab-btn" data-spec-tab="datamodel" onclick="switchAgentSpecTab('${ag.id}', 'datamodel', this)">
              🗄️ 05 · Data Model (${tables.length})
            </button>
            <button type="button" class="sc-spec-tab-btn" data-spec-tab="evals" onclick="switchAgentSpecTab('${ag.id}', 'evals', this)">
              ✅ 06 · Evals &amp; Proof
            </button>
          </div>

          <!-- TAB 01: PLAYBOOK & GOVERNANCE (4 Big-Heading Flippable Cards) -->
          <div id="spec-governance" class="sc-spec-tab-pane active" data-spec-pane="governance">
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:16px;">
              <div class="sc-flip-card sc-flip-tall" style="--flip-accent:#10b981;" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">01A · AUTONOMOUS</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading">
                      <div class="sc-flip-icon-box">✓</div>
                      <span>In-Scope Mandate</span>
                    </div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">${personaName}</span>
                    </div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">IN-SCOPE EXECUTION</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">${shortSentence(ag.solution, 105)}</div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">${tables[0]?.table_name || 'digital_twin'}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="sc-flip-card sc-flip-tall" style="--flip-accent:#f43f5e;" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">01B · BOUNDARIES</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading">
                      <div class="sc-flip-icon-box">✕</div>
                      <span>Out-of-Scope Limits</span>
                    </div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">Human Sign-Off Retained</span>
                    </div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">HUMAN AUTHORITY</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">No unapproved CapEx, contract termination, or policy overrides outside ${personaName} limits.</div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">No Unverified Writes</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="sc-flip-card sc-flip-tall" style="--flip-accent:#f59e0b;" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">01C · QUALITY GATES</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading">
                      <div class="sc-flip-icon-box">🚦</div>
                      <span>Escalation Rules</span>
                    </div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">enforce_tool_contract()</span>
                    </div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">4 GOVERNED TRIGGERS</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">&gt;20% plan variance escalates to human; missing idempotency_key or schema fields blocks mutation.</div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">escalate_to_human</span>
                      <span class="sc-flip-pill">idempotency_key</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="sc-flip-card sc-flip-tall" style="--flip-accent:#38bdf8;" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">01D · AUDIT TRAIL</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading">
                      <div class="sc-flip-icon-box">🔒</div>
                      <span>Hard Guardrails</span>
                    </div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">${tables.length || 4} Cited Tables</span>
                    </div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">EVIDENCE MANDATE</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">Zero fabricated metrics; every decision cites live rows and logs to action-events.jsonl.</div>
                    <div class="sc-flip-bottom-pills">
                      ${tables.slice(0, 2).map(t => `<span class="sc-flip-pill">${t.table_name}</span>`).join('')}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB 02: WORKFLOW (3 Big-Heading Flippable Stage Cards) -->
          <div id="spec-workflow" class="sc-spec-tab-pane" data-spec-pane="workflow">
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:16px;">
              ${subs.map((sub, idx) => `
                <div class="sc-flip-card sc-flip-tall" style="--flip-accent:${dept.color};" onclick="this.classList.toggle('is-flipped')">
                  <div class="sc-flip-inner">
                    <div class="sc-flip-front">
                      <div class="sc-flip-top-row">
                        <span class="sc-flip-kicker">STAGE 0${idx + 1} · A2A NODE</span>
                        <span class="sc-flip-hint">↻ Flip</span>
                      </div>
                      <div class="sc-flip-big-heading">
                        <div class="sc-flip-icon-box">0${idx + 1}</div>
                        <span>${shortStepHeading(toOpenTechLabel(sub.name), `Stage ${idx + 1}`)}</span>
                      </div>
                      <div class="sc-flip-bottom-pills">
                        <span class="sc-flip-pill">${tables[idx]?.table_name || 'digital_twin'}</span>
                      </div>
                    </div>
                    <div class="sc-flip-back">
                      <div class="sc-flip-top-row">
                        <span class="sc-flip-kicker">STAGE 0${idx + 1} ROLE</span>
                        <span class="sc-flip-hint">↺ Back</span>
                      </div>
                      <div class="sc-flip-back-text">${shortSentence(toOpenTechLabel(sub.role), 100)}</div>
                      <div class="sc-flip-bottom-pills">
                        <span class="sc-flip-pill">${rawTools[idx]?.name || 'query_state'}</span>
                      </div>
                    </div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <!-- TAB 03: AGENT TOOLS (Flippable Tool Cards) -->
          <div id="spec-tools" class="sc-spec-tab-pane" data-spec-pane="tools">
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:14px;">
              ${rawTools.map(t => `
                <div class="sc-flip-card" id="spec-tool-${t.name}" style="--flip-accent:${t.kind === 'action' ? '#f43f5e' : '#38bdf8'};" onclick="this.classList.toggle('is-flipped')">
                  <div class="sc-flip-inner">
                    <div class="sc-flip-front">
                      <div class="sc-flip-top-row">
                        <span class="sc-flip-kicker">${t.kind === 'action' ? '⚡ ACTION TOOL' : '🔍 QUERY TOOL'}</span>
                        <span class="sc-flip-hint">↻ Flip</span>
                      </div>
                      <div class="sc-flip-big-heading" style="font-size:16.5px; font-family:var(--font-mono); word-break:break-word;">
                        <span>${t.name}</span>
                      </div>
                      <div class="sc-flip-bottom-pills">
                        <span class="sc-flip-pill">${t.table || 'supply_chain_twin'}</span>
                      </div>
                    </div>
                    <div class="sc-flip-back">
                      <div class="sc-flip-top-row">
                        <span class="sc-flip-kicker">CONTRACT I/O</span>
                        <span class="sc-flip-hint">↺ Back</span>
                      </div>
                      <div class="sc-flip-back-text">${shortSentence(t.description, 95)}</div>
                      <div class="sc-flip-bottom-pills">
                        <span class="sc-flip-pill">IN: ${(t.inputs || []).slice(0, 2).join(', ')}</span>
                        <span class="sc-flip-pill">OUT: ${(t.outputs || []).slice(0, 2).join(', ')}</span>
                      </div>
                    </div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <!-- TAB 04: SOURCE SYSTEMS (Flippable System Cards) -->
          <div id="spec-systems" class="sc-spec-tab-pane" data-spec-pane="systems">
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:14px;">
              ${sysList.map(sys => `
                <div class="sc-flip-card" style="--flip-accent:${sys.mode.includes('write') ? '#10b981' : '#38bdf8'};" onclick="this.classList.toggle('is-flipped')">
                  <div class="sc-flip-inner">
                    <div class="sc-flip-front">
                      <div class="sc-flip-top-row">
                        <span class="sc-flip-kicker">${sys.mode.toUpperCase()}</span>
                        <span class="sc-flip-hint">↻ Flip</span>
                      </div>
                      <div class="sc-flip-big-heading" style="font-size:18px;">
                        <div class="sc-flip-icon-box">${pickSystemIcon(sys.name)}</div>
                        <span>${sys.name}</span>
                      </div>
                      <div class="sc-flip-bottom-pills">
                        <span class="sc-flip-pill">Pluggable MCP / DB / API</span>
                      </div>
                    </div>
                    <div class="sc-flip-back">
                      <div class="sc-flip-top-row">
                        <span class="sc-flip-kicker">INTEGRATION PROTOCOL</span>
                        <span class="sc-flip-hint">↺ Back</span>
                      </div>
                      <div class="sc-flip-back-text">Protocol: ${sys.protocol}</div>
                      <div class="sc-flip-bottom-pills">
                        ${(sys.ownedTables || []).slice(0, 2).map(tb => `<span class="sc-flip-pill">${tb}</span>`).join('')}
                      </div>
                    </div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <!-- TAB 05: DATA MODEL (Collapsible Table Schemas) -->
          <div id="spec-data-model" class="sc-spec-tab-pane" data-spec-pane="datamodel">
            <div class="sc-spec-entities-list">
              ${tables.map((t, idx) => {
                const cols = t.columns || [];
                const rows = t.rows || [];
                return `
                  <details class="sc-spec-entity" id="spec-entity-${t.table_name}" ${idx === 0 ? 'open' : ''}>
                    <summary>
                      <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                        <code class="sc-spec-code ev-code" style="font-size:14px; font-weight:800;">${t.table_name}</code>
                        <span style="font-size:12.5px; color:var(--text-secondary); font-weight:600;">
                          ${cols.length} cols · ${t.row_count || rows.length} rows
                        </span>
                      </div>
                      <span style="font-size:12px; color:${dept.color}; font-weight:700;">▾ Schema &amp; Samples</span>
                    </summary>
                    <div style="padding:14px 18px;">
                      <div class="sc-spec-table-wrap">
                        <table class="sc-spec-table">
                          <thead>
                            <tr><th>Column</th><th>Type</th><th>Sample Values</th></tr>
                          </thead>
                          <tbody>
                            ${cols.map(col => {
                              const info = inferColumnTypeAndConstraint(col, rows);
                              return `<tr><td><code class="sc-spec-code">${col}</code></td><td>${info.colType}</td><td style="font-family:var(--font-mono); font-size:12px;">${info.sampleStr || '—'}</td></tr>`;
                            }).join('')}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </details>
                `;
              }).join('')}
            </div>
          </div>

          <!-- TAB 06: EVALS & PROOF (3 Big-Heading Flippable Cards) -->
          <div id="spec-evals" class="sc-spec-tab-pane" data-spec-pane="evals">
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:16px;">
              <div class="sc-flip-card sc-flip-tall" style="--flip-accent:${dept.color};" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">${evalObj.scenario_id}</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading">
                      <div class="sc-flip-icon-box">🎯</div>
                      <span>Golden Eval Scenario</span>
                    </div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">SLA &le;${evalObj.sla_seconds || 15}s · 7/7 Pass</span>
                    </div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">EVAL PROMPT</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">“${shortSentence(evalObj.query, 105)}”</div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">gemini-3.8-flash</span>
                      <span class="sc-flip-pill">gemini-3.1-pro / 4-argon</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="sc-flip-card sc-flip-tall" style="--flip-accent:#10b981;" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">VERIFICATION</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading">
                      <div class="sc-flip-icon-box">✅</div>
                      <span>Proof Obligations</span>
                    </div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">test_smoke.py Verified</span>
                    </div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">REQUIRED CHECKS</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">${(evalObj.expected_proof_obligations || []).slice(0, 2).join(' · ')}</div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">A2UI VegaChart</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="sc-flip-card sc-flip-tall" style="--flip-accent:#a855f7;" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">COMPLIANCE</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading">
                      <div class="sc-flip-icon-box">📜</div>
                      <span>Industry Standards</span>
                    </div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">${standards[0] || 'ASCM SCOR DS'}</span>
                    </div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">STANDARDS ALIGNED</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">Aligned with global supply chain &amp; AI governance frameworks.</div>
                    <div class="sc-flip-bottom-pills">
                      ${standards.slice(0, 3).map(st => `<span class="sc-flip-pill">${st}</span>`).join('')}
                    </div>
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

          <!-- 1. Clean Big-Heading Hero + 3 Flippable Executive Cards (Problem / Solution / Outcome) -->
          <div class="agent-hero-banner" style="padding: 28px 32px; margin-bottom: 22px;">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:18px;">
              <div style="display:flex; align-items:center; gap:14px;">
                <div class="ai-bot-square" style="width:52px; height:52px; font-size:24px;">✦</div>
                <div>
                  <h1 class="agent-title" style="font-size: clamp(26px, 3vw, 36px); margin: 0;">${cleanAgentName(ag.name)}</h1>
                  <div style="font-size:15px; color:var(--text-secondary); margin-top:4px; font-weight:700;">${ag.subPillarName || dept.name}</div>
                </div>
              </div>
              <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                <span class="build-tier-badge ${cls.cssClass}">${cls.label}</span>
              </div>
            </div>

            <!-- 3 Big-Heading Flippable Summary Cards -->
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap:14px;">
              <div class="sc-flip-card sc-flip-compact" style="--flip-accent:#f43f5e;" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">01 · CHALLENGE</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading">
                      <div class="sc-flip-icon-box">✕</div>
                      <span>The Bottleneck</span>
                    </div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">Click to read problem</span>
                    </div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">✕ PROBLEM SOLVED</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">${shortSentence(ag.problem, 105)}</div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">${ag.subPillarName || dept.name}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="sc-flip-card sc-flip-compact" style="--flip-accent:${dept.color};" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">02 · CAPABILITY</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading">
                      <div class="sc-flip-icon-box">✦</div>
                      <span>AI Agent Solution</span>
                    </div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">Click to read solution</span>
                    </div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">✦ AGENTIC SOLUTION</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">${shortSentence(ag.solution, 105)}</div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">Autonomous Execution</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="sc-flip-card sc-flip-compact" style="--flip-accent:#10b981;" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">03 · BUSINESS IMPACT</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading">
                      <div class="sc-flip-icon-box">🚀</div>
                      <span>${ag.badge || 'Verified ROI'}</span>
                    </div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">Click to read outcome</span>
                    </div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">🚀 VERIFIED OUTCOME</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">${shortSentence(ag.outcome, 105)}</div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">${ag.badge || 'KPI Impact'}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 2. Execution Flow SVG + 5 Flippable Step Cards -->
          ${renderSimpleAgentArchitectureDiagram(ag, dept)}

          <!-- 3. 4 Flippable Cost & Value KPI Cards -->
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

          <!-- 5. ONE Single Button / Tab for Playbook, Governance & Technical Specs -->
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

    /* =========================================================================
       DEDICATED ENTERPRISE AGENT CONTRACT, PLAYBOOK & TECHNICAL BLUEPRINT PAGE (#blueprint/<id>)
       ========================================================================= */
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


def update_persona_page_block(text: str) -> str:
    """Makes Persona Daily Journey steps collapsed by default and converts Persona Agent Dock cards into clean Flippable Cards."""
    old_dock_start = "          <!-- Structured AI Agents Dock for this Persona (Good Boxes + Clear Button) -->"
    old_dock_end = "      hydrateAssets();\n      showActivePage('pagePersona');"
    s_idx = text.find(old_dock_start)
    e_idx = text.find(old_dock_end, s_idx)
    if s_idx == -1 or e_idx == -1:
        return text

    # Also make firstToilOpened = true so all daily tasks start collapsed (less clutter on main persona page)
    text = text.replace("let firstToilOpened = false;", "let firstToilOpened = true;")

    new_dock = """          <!-- Big-Heading Flippable AI Agent Cards for this Persona -->
          <div class="ai-agent-dock-box">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-bottom:16px;">
              <h2 style="font-family:var(--font-display); font-size:22px; font-weight:800; color:var(--text-primary); margin:0;">
                ✦ AI Agents for ${p.name}
              </h2>
              <span style="font-size:12.5px; color:var(--text-secondary); font-weight:600;">
                Click any card to flip for details, or open the Agent Studio
              </span>
            </div>

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap:16px;">
              ${[...new Set(p.agentIds || [])].map(aid => {
                const ag = AGENTS[aid];
                if (!ag) return '';
                return `
                  <div class="sc-flip-card sc-flip-tall" style="--flip-accent:${dept.color};" onclick="this.classList.toggle('is-flipped')">
                    <div class="sc-flip-inner">
                      <div class="sc-flip-front">
                        <div class="sc-flip-top-row">
                          <span class="sc-flip-kicker">${ag.subPillarName || dept.name}</span>
                          <span class="sc-flip-hint">↻ Flip for Info</span>
                        </div>
                        <div class="sc-flip-big-heading" style="font-size:21px;">
                          <div class="ai-bot-square" style="width:42px; height:42px; font-size:18px; flex-shrink:0;">✦</div>
                          <span>${cleanAgentName(ag.name)}</span>
                        </div>
                        <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; flex-wrap:wrap;">
                          <span class="sc-flip-pill" style="color:#10b981; border-color:rgba(16,185,129,0.35);">✦ ${ag.badge || 'High ROI'}</span>
                          <button type="button" class="agent-plug-btn" style="padding:7px 14px; font-size:12.5px;" onclick="event.stopPropagation(); openAgentPage('${ag.id}', true, event)">
                            <span>Open Agent &rarr;</span>
                          </button>
                        </div>
                      </div>
                      <div class="sc-flip-back">
                        <div class="sc-flip-top-row">
                          <span class="sc-flip-kicker">AGENT SUMMARY</span>
                          <span class="sc-flip-hint">↺ Back</span>
                        </div>
                        <div class="sc-flip-back-text">${shortSentence(ag.solution || ag.role, 100)}</div>
                        <div style="display:flex; align-items:center; justify-content:space-between; gap:8px;">
                          ${ag.costModel ? `<span class="sc-flip-pill">💰 $${ag.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo</span>` : ''}
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
    s_idx = text.find(old_dock_start)
    e_idx = text.find(old_dock_end, s_idx)
    return text[:s_idx] + new_dock + text[e_idx:]


def update_value_chain_and_arch_pages(text: str) -> str:
    """Converts Process Journey stage nodes and Architecture Page agent cards into Big-Heading Flippable Cards, and tucks the 60-agent matrix on #architecture under 1 expandable button."""
    text = text.replace(
        "const sysFirst = (st.systems || '').split('·')[0].trim().slice(0, 18);",
        "const sysFirst = (toSysArray(st.systems)[0] || '').trim().slice(0, 18);"
    )
    # 1. Value Chain Stage Spotlight 3 nodes -> 3 Flippable Cards
    vc_start = "            <!-- 3-Node Visual Stage Flow Schematic (Systems -> Autonomous AI Engine -> Golden Thread Output) -->"
    vc_end = "            <!-- Distinct Human Persona Owner Card vs. AI Agent Card for This Stage -->"
    vs = text.find(vc_start)
    ve = text.find(vc_end, vs)
    if vs != -1 and ve != -1:
        new_vc_schematic = """            <!-- 3 Big-Heading Flippable Stage Cards -->
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap:14px; margin: 16px 0;">
              <div class="sc-flip-card sc-flip-compact" style="--flip-accent:#38bdf8;" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">01 · STAGE INPUT</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading">
                      <div class="sc-flip-icon-box">📥</div>
                      <span>Source Systems</span>
                    </div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">${toSysArray(activeStage.systems).length} Connected Feeds</span>
                    </div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">CONNECTED SYSTEMS</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">Live operational state &amp; telemetry ingested into the Digital Twin.</div>
                    <div class="sc-flip-bottom-pills">
                      ${toSysArray(activeStage.systems).slice(0, 3).map(s => `<span class="sc-flip-pill">${toOpenTechLabel(s)}</span>`).join('')}
                    </div>
                  </div>
                </div>
              </div>

              <div class="sc-flip-card sc-flip-compact" style="--flip-accent:${activeStage.color || vc.color};" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">02 · AI ENGINE (${activeStage.modality})</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading">
                      <div class="sc-flip-icon-box">⚡</div>
                      <span>${activeStage.toilTime} &rarr; ${activeStage.afterTime}</span>
                    </div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">Click for AI Action</span>
                    </div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">AUTONOMOUS EXECUTION</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">${shortSentence(activeStage.after, 95)}</div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">${activeStage.modality}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="sc-flip-card sc-flip-compact" style="--flip-accent:#10b981;" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">03 · GOLDEN THREAD</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading">
                      <div class="sc-flip-icon-box">🔗</div>
                      <span>Downstream Handoff</span>
                    </div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">Click for Handoff</span>
                    </div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">GOLDEN THREAD OUTPUT</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">${shortSentence(activeStage.goldenThread, 95)}</div>
                    <div class="sc-flip-bottom-pills">
                      <span class="sc-flip-pill">Signed State Commit</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

"""
        text = text[:vs] + new_vc_schematic + text[ve:]

    # 2. Architecture Page: Put 60-agent matrix under 1 single expandable button & use Flippable Cards
    arch_start = "          <!-- Interactive SCOR Vertical Filter Bar on Architecture Page -->"
    arch_end = "      hydrateAssets();\n      showActivePage('pageArchitecture');"
    as_idx = text.find(arch_start)
    ae_idx = text.find(arch_end, as_idx)
    if as_idx != -1 and ae_idx != -1:
        new_arch_matrix = """          <!-- ONE Single Button to Expand All 60 Flippable Agent Architecture Cards -->
          <div class="sc-single-spec-trigger-bar" style="border-left: 5px solid #a855f7; margin-top: 8px;">
            <div>
              <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:#c084fc; margin-bottom:3px;">
                🤖 60-Agent Technical Catalog · Flippable Architecture Cards
              </div>
              <div style="font-family:var(--font-display); font-size:22px; font-weight:800; color:var(--text-primary);">
                Explore Individual Agent Solvers, Write-Backs &amp; A2A Swarms
              </div>
            </div>
            <button type="button" class="switch-pill" style="font-weight:800; padding:10px 18px;" onclick="const el=document.getElementById('archAll60MatrixDrawer'); if(el){const open=el.style.display==='none'; el.style.display=open?'block':'none'; this.textContent=open?'▴ Hide 60-Agent Catalog':'▾ Open 60-Agent Flippable Catalog';}">
              ${currentArchVerticalFilter !== 'all' ? '▴ Hide 60-Agent Catalog' : '▾ Open 60-Agent Flippable Catalog'}
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
                        <div class="sc-flip-card sc-flip-tall" style="--flip-accent:${dept.color};" onclick="this.classList.toggle('is-flipped')">
                          <div class="sc-flip-inner">
                            <div class="sc-flip-front">
                              <div class="sc-flip-top-row">
                                <span class="sc-flip-kicker">${ag.subPillarName || dept.name}</span>
                                <span class="sc-flip-hint">↻ Flip</span>
                              </div>
                              <div class="sc-flip-big-heading" style="font-size:19px;">
                                <div class="ai-bot-square" style="width:38px; height:38px; font-size:16px; flex-shrink:0;">✦</div>
                                <span>${cleanAgentName(ag.name)}</span>
                              </div>
                              <div style="display:flex; align-items:center; justify-content:space-between; gap:8px;">
                                <span class="sc-flip-pill">${ag.badge || 'High ROI'}</span>
                                <button type="button" class="switch-pill" style="padding:5px 12px; font-size:12px;" onclick="event.stopPropagation(); openAgentPage('${ag.id}', true, event)">
                                  Open &rarr;
                                </button>
                              </div>
                            </div>
                            <div class="sc-flip-back">
                              <div class="sc-flip-top-row">
                                <span class="sc-flip-kicker">TECH STACK</span>
                                <span class="sc-flip-hint">↺ Back</span>
                              </div>
                              <div class="sc-flip-back-text">
                                <strong>Solver:</strong> ${shortSentence(toOpenTechLabel(ag.solverStack || 'Vertex AI + BigQuery ML'), 60)}
                              </div>
                              <div style="display:flex; align-items:center; justify-content:space-between; gap:8px;">
                                <span class="sc-flip-pill">${toOpenTechLabel(ag.apiWriteback || 'MCP Write-Back').slice(0, 24)}</span>
                                <button type="button" class="switch-pill" style="padding:5px 12px; font-size:12px;" onclick="event.stopPropagation(); openAgentBlueprintPage('${ag.id}', true, event)">
                                  Spec ↗
                                </button>
                              </div>
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
        text = text[:as_idx] + new_arch_matrix + text[ae_idx:]

    return text


def update_file(path: Path):
    text = path.read_text(encoding="utf-8")

    # 1. Inject FLIP_AND_SINGLE_TAB_CSS
    css_anchor = "    .sc-spec-sec-head {"
    if ".sc-flip-card {" not in text:
        if css_anchor in text:
            text = text.replace(css_anchor, FLIP_AND_SINGLE_TAB_CSS + "\n" + css_anchor, 1)
        else:
            raise RuntimeError(f"Could not find {css_anchor} in {path}")

    # 2. Replace renderSimpleAgentArchitectureDiagram .. openAgentBlueprintPage
    start_marker = "    function renderSimpleAgentArchitectureDiagram(ag, dept) {"
    if "    function shortStepHeading(" in text:
        start_marker = "    function shortStepHeading("
    s_idx = text.find(start_marker)
    if s_idx == -1:
        raise RuntimeError(f"Could not find {start_marker} in {path}")

    end_marker = "    function selectDemoTableTab("
    e_idx = text.find(end_marker, s_idx)
    if e_idx == -1:
        raise RuntimeError(f"Could not find {end_marker} in {path}")

    text = text[:s_idx] + NEW_ARCH_COST_SPEC_BLOCK + "\n\n" + text[e_idx:]

    # 3. Clean up Persona Page (collapsed daily tasks by default + Flippable AI Agent cards)
    text = update_persona_page_block(text)

    # 4. Clean up Value Chain and Architecture pages
    text = update_value_chain_and_arch_pages(text)

    path.write_text(text, encoding="utf-8")
    print(f"Updated {path.name}")


if __name__ == "__main__":
    for f in HTML_FILES:
        if f.exists():
            update_file(f)

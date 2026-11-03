#!/usr/bin/env python3
"""Refines Persona & Agent UX clarity across `index.html`, `periodic_table.html`, and `mind_map.html`:

1. Removes inline monthly cost clutter from Persona daily toil step boxes & Persona bottom agent cards.
2. Declutters `#pageAgent` (`openAgentPage`):
   - Removes the duplicate `.agent-what-it-does-box` paragraph+bullet wall above the 3 summary cards.
   - Makes the 3 summary cards (`01 · Challenge`, `02 · AI Solution`, `03 · Impact`) crisp & scannable.
   - Shows ONLY the 4-stage animated SVG flow inside `renderSimpleAgentArchitectureDiagram` by default.
   - Moves Cost & ROI, 5 Execution Step Cards, Benchmark Proof, and the 6-tab Governance & Tech Specs
     into a sleek, collapsed-by-default Deep-Dive Tab Bar (`💰 Cost & ROI ▾`, `⚡ 5 Execution Steps ▾`,
     `📚 Benchmark Proof ▾`, `🛡️ Governance & Tech Specs ▾`) while preserving 100% of the 6-tab
     Enterprise Agent Contract.
3. Updates `openPeriodicTablePage` tile labels so company-tailored agent names (`custom_agent_name`)
   render cleanly on Periodic Table tiles and revert cleanly on reset.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def refine_single_html(path: Path) -> None:
    orig = path.read_text(encoding="utf-8")
    orig_len = len(orig)
    html = orig

    # -------------------------------------------------------------------------
    # 1. Remove inline Cost details & trim verbosity inside `openPersonaPage`
    # -------------------------------------------------------------------------
    old_persona_step_agent = """                              <div style="font-size:15.5px; color:var(--text-secondary); line-height:1.68;">
                                ${plugAgent.solution || plugAgent.role}
                              </div>
                              ${plugAgent.costModel ? `
                                <div style="margin-top:6px;">
                                  <span style="font-family:var(--font-mono); font-size:11px; font-weight:700; color:var(--text-secondary);">
                                    💰 Est. Cost: <strong style="color:var(--text-primary);">$${plugAgent.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo</strong> ($${plugAgent.costModel.monthlyBreakdown.blendedCostPer1kCallsUsd.toFixed(2)}/1K runs)
                                  </span>
                                </div>
                              ` : ''}"""

    new_persona_step_agent = """                              <div style="font-size:14.5px; color:var(--text-secondary); line-height:1.58;">
                                ${shortSentence(plugAgent.solution || plugAgent.role, 120)}
                              </div>"""

    if old_persona_step_agent in html:
        html = html.replace(old_persona_step_agent, new_persona_step_agent, 1)

    old_persona_dock_back = """                        <div class="sc-flip-back-text">${ag.solution || ag.role}</div>
                        <div style="display:flex; align-items:center; justify-content:space-between; gap:8px;">
                          ${ag.costModel ? `<span class="sc-flip-pill">💰 $${ag.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo</span>` : ''}
                          <button type="button" class="agent-plug-btn" style="padding:7px 14px; font-size:12.5px;" onclick="event.stopPropagation(); openAgentPage('${ag.id}', true, event)">
                            <span>Open Studio &rarr;</span>
                          </button>
                        </div>"""

    new_persona_dock_back = """                        <div class="sc-flip-back-text">${shortSentence(ag.solution || ag.role, 135)}</div>
                        <div style="display:flex; align-items:center; justify-content:space-between; gap:8px;">
                          <span class="sc-flip-pill">${getAgentBuildClassification(ag).label}</span>
                          <button type="button" class="agent-plug-btn" style="padding:7px 14px; font-size:12.5px;" onclick="event.stopPropagation(); openAgentPage('${ag.id}', true, event)">
                            <span>Open Studio &rarr;</span>
                          </button>
                        </div>"""

    if old_persona_dock_back in html:
        html = html.replace(old_persona_dock_back, new_persona_dock_back, 1)

    # -------------------------------------------------------------------------
    # 2. Separate 5 Step Flip Cards from `renderSimpleAgentArchitectureDiagram`
    # -------------------------------------------------------------------------
    old_steps_tail = """          <!-- 5 Big-Heading Flippable Step Cards (Zero Paragraph Clutter on Front; Click to Flip) -->
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
    }"""

    new_steps_tail = """        </div>
      `;
    }

    function renderAgentFiveStepCards(ag, dept) {
      const cls = getAgentBuildClassification(ag);
      const topology = AGENT_TOPOLOGY_MAP[ag.id] || 'milp_pareto_loop';
      const tMeta = TOPOLOGY_META[topology] || TOPOLOGY_META.milp_pareto_loop;
      const adk = ag.adkImplementation || {};
      const spec = ag.adkSpec || {};
      const trunc = (str, max = 26) => {
        const s = String(str || '').trim();
        return s.length > max ? s.slice(0, max - 1) + '…' : s;
      };
      const sysArr = toSysArray(ag.systems).map(s => toOpenTechLabel(s));
      const sys1 = sysArr[0] || 'Enterprise ERP / Order Ledger';
      const sys2 = sysArr[1] || 'Operational Telemetry & Signals';
      const ic1 = pickSystemIcon(sys1);
      const tables = (adk.fixtureTables || []).map(t => t.table_name);
      const tbl1 = tables[0] || 'primary_twin_ledger';
      const rawTools = (spec.toolsMeta && spec.toolsMeta.length)
        ? spec.toolsMeta.map(t => t.name)
        : (adk.tools || []).filter(t => t !== 'list_systems');
      const qTools = rawTools.filter(t => !String(t).startsWith('action_'));
      const aTools = rawTools.filter(t => String(t).startsWith('action_'));
      const q1 = qTools[0] || 'query_domain_signals';
      const a1 = aTools[0] || 'action_commit_writeback';
      const rawSubs = (ag.subAgents && ag.subAgents.length >= 3)
        ? ag.subAgents.slice(0, 3)
        : [
            { name: 'Signal Context Node', role: 'Streams & validates live operational inputs' },
            { name: 'Optimization Engine', role: 'Evaluates constraints & ranks actions' },
            { name: 'Write-Back Dispatcher', role: 'Enforces quality gates & signed payloads' }
          ];
      const subs = rawSubs.map(sa => ({ name: toOpenTechLabel(sa.name), role: toOpenTechLabel(sa.role) }));
      const solverLabel = toOpenTechLabel(ag.solverStack || 'Time-Series & Mathematical Optimization Engine');
      const writebackFull = toOpenTechLabel(ag.apiWriteback || 'Enterprise ERP / WMS Write-Back via MCP or REST');

      const flipSteps = [
        {
          kicker: '01 · INGEST', icon: ic1, heading: 'Open Connectors',
          frontPill: `🔌 ${sysArr.length || 3} Systems`, accent: dept.color,
          backText: `Ingests live state via MCP, REST/EDI, or On-Prem DB adapters from ${trunc(sys1, 32)}.`,
          backPills: [trunc(sys1, 24), trunc(sys2, 24)]
        },
        {
          kicker: '02 · NORMALIZE', icon: tMeta.icons[1], heading: shortStepHeading(subs[0].name, 'State Normalizer'),
          frontPill: `🗄️ ${tables.length || 4} Tables`, accent: '#38bdf8',
          backText: subs[0].role, backPills: [q1, tbl1]
        },
        {
          kicker: '03 · SOLVE', icon: tMeta.icons[2], heading: shortStepHeading(subs[1].name, 'AI & Math Solver'),
          frontPill: '🧠 Gemini 3.8 + 3.1 Pro', accent: cls.color,
          backText: `${subs[1].role} using ${solverLabel}.`,
          backPills: ['gemini-3.8-flash', 'gemini-3.1-pro / 4-argon']
        },
        {
          kicker: '04 · GOVERN', icon: tMeta.icons[3], heading: shortStepHeading(subs[2].name, 'Safety & Policy Gate'),
          frontPill: '🛡️ Pre-Gate Verified', accent: '#f59e0b',
          backText: 'Verifies idempotency_key, schema contracts & delegation thresholds before commit.',
          backPills: ['enforce_tool_contract()', 'HITL Escalation']
        },
        {
          kicker: '05 · ACTUATE', icon: tMeta.icons[4], heading: 'MCP / API Write-Back',
          frontPill: `⚡ ${trunc(ag.badge || 'Signed Commit', 18)}`, accent: '#10b981',
          backText: `Commits governed payload via ${trunc(writebackFull, 38)} and renders VegaChart.`,
          backPills: [a1, 'A2UI VegaChart']
        }
      ];

      return `
        <div class="simple-arch-card" style="margin-top:14px; margin-bottom:18px;">
          <div style="display:flex; align-items:center; justify-content:space-between; gap:10px; margin-bottom:14px;">
            <div style="font-family:var(--font-display); font-size:19px; font-weight:800; color:var(--text-primary);">
              ⚡ 5-Stage Agentic Execution Pipeline — ${cleanAgentName(ag.name)}
            </div>
            <span style="font-size:12px; color:var(--text-secondary); font-weight:600;">Click any step card to flip</span>
          </div>
          <div class="ag-flow-steps-grid">
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
    }"""

    if "function renderAgentFiveStepCards(" not in html:
        assert old_steps_tail in html, f"Could not locate old_steps_tail in {path.name}"
        html = html.replace(old_steps_tail, new_steps_tail, 1)
    else:
        fn5_start = html.index("    function renderAgentFiveStepCards(ag, dept) {")
        fn_cost_anchor = html.index("    /* =========================================================================\n       CLEAN AGENT COST & VALUE", fn5_start)
        replacement_fn5 = new_steps_tail[new_steps_tail.index("    function renderAgentFiveStepCards(ag, dept) {"):] + "\n\n"
        html = html[:fn5_start] + replacement_fn5 + html[fn_cost_anchor:]

    # -------------------------------------------------------------------------
    # 3. Allow `renderAgentFullSpecSheet` to omit its bulky top bar when hosted
    #    under the unified Deep-Dive Tab Bar on `#pageAgent`
    # -------------------------------------------------------------------------
    old_spec_sig = """    function renderAgentFullSpecSheet(ag, dept, openByDefault = false) {"""
    new_spec_sig = """    function renderAgentFullSpecSheet(ag, dept, openByDefault = false, hideTriggerBar = false) {"""
    if old_spec_sig in html:
        html = html.replace(old_spec_sig, new_spec_sig, 1)

    old_spec_bar = """      return `
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
        </div>"""

    new_spec_bar = """      return `
        ${hideTriggerBar ? '' : `
        <!-- ONE SINGLE BUTTON / BAR ON THE BLUEPRINT PAGE -->
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
        `}"""

    if "${hideTriggerBar ? ''" not in html:
        assert old_spec_bar in html, f"Could not locate old_spec_bar in {path.name}"
        html = html.replace(old_spec_bar, new_spec_bar, 1)

    # -------------------------------------------------------------------------
    # 4. Declutter `openAgentPage` & add `toggleAgentDeepDiveDrawer`
    # -------------------------------------------------------------------------
    fn_open_agent = "    function openAgentPage(agentId, pushHash = true, ev = null) {"
    fn_attach_vid = "    function attachAgentVideo(event, agentId) {"
    i_start = html.index(fn_open_agent)
    # If toggleAgentDeepDiveDrawer was already prepended on a prior run, include it in slice
    helper_marker = "    function toggleAgentDeepDiveDrawer("
    if helper_marker in html:
        i_start = html.index(helper_marker)
    i_end = html.index(fn_attach_vid, i_start)

    clean_open_agent_fn = """    function toggleAgentDeepDiveDrawer(agentId, key) {
      const mapping = {
        cost: { panelId: `agentDrawer_cost_${agentId}`, btnId: `agentDeepBtn_cost_${agentId}`, openTxt: '💰 Cost & ROI ▴', closedTxt: '💰 Cost & ROI ▾' },
        steps: { panelId: `agentDrawer_steps_${agentId}`, btnId: `agentDeepBtn_steps_${agentId}`, openTxt: '⚡ 5 Execution Steps ▴', closedTxt: '⚡ 5 Execution Steps ▾' },
        proof: { panelId: `agentDrawer_proof_${agentId}`, btnId: `agentDeepBtn_proof_${agentId}`, openTxt: '📚 Benchmark Proof ▴', closedTxt: '📚 Benchmark Proof ▾' },
        specs: { panelId: `agentSingleSpecBody_${agentId}`, btnId: `agentDeepBtn_specs_${agentId}`, openTxt: '🛡️ Governance & Tech Specs ▴', closedTxt: '🛡️ Governance & Tech Specs ▾' }
      };
      const target = mapping[key];
      if (!target) return;
      const targetPanel = document.getElementById(target.panelId);
      if (!targetPanel) return;
      const willOpen = targetPanel.style.display === 'none';

      Object.entries(mapping).forEach(([k, cfg]) => {
        const pEl = document.getElementById(cfg.panelId);
        const bEl = document.getElementById(cfg.btnId);
        const openNow = (k === key) && willOpen;
        if (pEl) pEl.style.display = openNow ? 'block' : 'none';
        if (bEl) {
          bEl.classList.toggle('active', openNow);
          bEl.textContent = openNow ? cfg.openTxt : cfg.closedTxt;
        }
      });

      if (willOpen) {
        setTimeout(() => targetPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 40);
      }
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
      const dispAgentName = cleanAgentName(ag.name);
      const hasCustomCompanyAgentName = Boolean(ag.canonicalName && ag.canonicalName !== dispAgentName);

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
          ${renderAgentTwinDivisionBanner(ag)}

          <!-- 1. Crisp, Minimal-Text Executive Hero + 3 Clear Summary Cards -->
          <div class="agent-hero-banner" style="padding: 26px 30px; margin-bottom: 20px;">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:14px; margin-bottom:20px;">
              <div style="display:flex; align-items:center; gap:15px;">
                <div class="ai-bot-square" style="width:52px; height:52px; font-size:24px;">✦</div>
                <div>
                  <h1 class="agent-title" style="font-size: clamp(25px, 2.8vw, 34px); margin: 0; line-height: 1.15;">${dispAgentName}</h1>
                  <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-top:5px;">
                    <span style="font-size:14.5px; color:var(--text-secondary); font-weight:700;">${ag.subPillarName || dept.name}</span>
                    ${hasCustomCompanyAgentName ? `
                      <span class="sc-twin-core-engine-chip">Core Engine: ${escTwinHtml(ag.canonicalName)}</span>
                    ` : ''}
                  </div>
                </div>
              </div>
              <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                <a href="agent_testing_and_video_playbook.html#agent-${ag.id}"
                   style="text-decoration:none; font-size:13px; font-weight:700; padding:8px 15px; border-radius:999px; background:rgba(56,189,248,0.14); color:#38bdf8; border:1.5px solid rgba(56,189,248,0.42);">
                  📋 Test Prompts &amp; Data &rarr;
                </a>
                <span class="build-tier-badge ${cls.cssClass}">${cls.label}</span>
              </div>
            </div>

            <!-- 3 Crisp, Scannable Summary Cards (Click to Flip for Full Text) -->
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:16px;">
              <div class="sc-flip-card sc-flip-compact" style="--flip-accent:#f43f5e;" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">01 · CHALLENGE</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading" style="font-size:20px;">
                      <div class="sc-flip-icon-box">✕</div>
                      <span>The Bottleneck</span>
                    </div>
                    <div class="sc-agent-card-brief">${shortSentence(ag.problem, 108)}</div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">✕ PROBLEM SOLVED</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">${ag.problem}</div>
                  </div>
                </div>
              </div>

              <div class="sc-flip-card sc-flip-compact" style="--flip-accent:${dept.color};" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">02 · AI SOLUTION</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading" style="font-size:20px;">
                      <div class="sc-flip-icon-box">✦</div>
                      <span>How It Works</span>
                    </div>
                    <div class="sc-agent-card-brief">${shortSentence(ag.solution, 108)}</div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">✦ AGENTIC EXECUTION</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">${ag.solution}</div>
                  </div>
                </div>
              </div>

              <div class="sc-flip-card sc-flip-compact" style="--flip-accent:#10b981;" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">03 · IMPACT</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading" style="font-size:20px;">
                      <div class="sc-flip-icon-box">🚀</div>
                      <span>${ag.badge || 'Verified ROI'}</span>
                    </div>
                    <div class="sc-agent-card-brief">${shortSentence(ag.outcome, 108)}</div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">🚀 BUSINESS OUTCOME</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">${ag.outcome}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 2. Clean 4-Stage Visual Flow Diagram (SVG Only) -->
          ${renderSimpleAgentArchitectureDiagram(ag, dept)}

          <!-- 3. Dedicated Agent Demo Video / Interactive Preview Stage -->
          <div class="video-stage-box" style="margin-top:20px;">
            <div class="video-toolbar" style="border-top:none; border-bottom:1.5px solid var(--border-subtle);">
              <span style="font-weight:700; color:var(--text-primary);">🎬 Agent Demo Studio — ${dispAgentName}</span>
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

            <div class="video-viewport" id="agentVideoViewport" style="min-height: 340px;">
              ${stageViewMode === 'cad'
                ? renderInteractiveCadStage(ag.cadType || 'demand_wave', 'agentCadMount')
                : (hasVideo
                    ? `<video id="agentVideoPlayer" controls autoplay loop muted playsinline src="${videoUrl}"></video>`
                    : `
                      <div class="video-placeholder-stage">
                        <div class="video-placeholder-icon">▶</div>
                        <div style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary);">
                          ${dispAgentName} — Demo Studio
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

          <!-- 4. Sleek Collapsed-by-Default Deep-Dive Tab Bar (Cost, Steps, Benchmarks, Governance & Specs) -->
          <div class="agent-deepdive-bar" style="--deep-accent:${dept.color};">
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="agent-deepdive-label">Optional Deep-Dive:</span>
              <button type="button" id="agentDeepBtn_cost_${ag.id}" class="agent-deepdive-pill" onclick="toggleAgentDeepDiveDrawer('${ag.id}', 'cost')">
                💰 Cost &amp; ROI ▾
              </button>
              <button type="button" id="agentDeepBtn_steps_${ag.id}" class="agent-deepdive-pill" onclick="toggleAgentDeepDiveDrawer('${ag.id}', 'steps')">
                ⚡ 5 Execution Steps ▾
              </button>
              <button type="button" id="agentDeepBtn_proof_${ag.id}" class="agent-deepdive-pill" onclick="toggleAgentDeepDiveDrawer('${ag.id}', 'proof')">
                📚 Benchmark Proof ▾
              </button>
              <button type="button" id="agentDeepBtn_specs_${ag.id}" class="agent-deepdive-pill" onclick="toggleAgentDeepDiveDrawer('${ag.id}', 'specs')">
                🛡️ Governance &amp; Tech Specs ▾
              </button>
            </div>
            <button type="button" class="agent-deepdive-pill blueprint-jump" onclick="openAgentBlueprintPage('${ag.id}', true, event, 'spec-governance')">
              📄 Full Blueprint Page &rarr;
            </button>
          </div>

          <!-- Collapsed Optional Deep-Dive Drawers (100% Details Preserved On Demand) -->
          <div id="agentDrawer_cost_${ag.id}" class="agent-deepdive-drawer" style="display:none;">
            ${renderAgentCostAndRoiPanel(ag, dept)}
          </div>
          <div id="agentDrawer_steps_${ag.id}" class="agent-deepdive-drawer" style="display:none;">
            ${renderAgentFiveStepCards(ag, dept)}
          </div>
          <div id="agentDrawer_proof_${ag.id}" class="agent-deepdive-drawer" style="display:none;">
            ${renderAgentExternalProofCard(ag, dept)}
          </div>
          ${renderAgentFullSpecSheet(ag, dept, false, true)}
        </div>
      `;

      hydrateAssets();
      showActivePage('pageAgent');
      const wrap = document.getElementById('agentGenieWrap');
      if (sRect && wrap) {
        animateGenieOutOfBox(sRect, wrap, dept.color);
      }
    }

"""
    html = html[:i_start] + clean_open_agent_fn + html[i_end:]

    # -------------------------------------------------------------------------
    # 5. Update `openPeriodicTablePage` tile shortLabel so tailored company
    #    agent names (`custom_agent_name`) display cleanly on Periodic Table
    # -------------------------------------------------------------------------
    old_pt_label = "const shortLabel = cleanAgentName(m.short || ag.name).replace(/\\s+Agent$/i, '');"
    new_pt_label = "const shortLabel = ((ag.canonicalName && ag.canonicalName !== cleanAgentName(ag.name)) ? cleanAgentName(ag.name) : cleanAgentName(m.short || ag.name)).replace(/\\s+Agent$/i, '');"
    if old_pt_label in html:
        html = html.replace(old_pt_label, new_pt_label, 1)

    assert len(html) >= int(orig_len * 0.95), f"Safety check failed for {path.name}: {len(html)} < {orig_len}"
    path.write_text(html, encoding="utf-8")
    print(f"[REFINED UX] {path.name} ({path.stat().st_size // 1024} KB)")


def main() -> None:
    for fname in ("index.html", "periodic_table.html", "mind_map.html"):
        p = ROOT / fname
        if p.exists():
            refine_single_html(p)


if __name__ == "__main__":
    main()

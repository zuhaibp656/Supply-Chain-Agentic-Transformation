#!/usr/bin/env python3
"""Simplifies the Agent Studio Page (#agent/<id>), Blueprint Page (#blueprint/<id>),
and cost badges across `index.html`, `periodic_table.html`, and `mind_map.html`:
- Removes the heavy `renderAgentAdkAndDemoDataPanel(ag)` dump and multi-table dark-mode
  calculator from `#agent/<id>`.
- Replaces `renderAgentCostAndRoiPanel(ag, dept)` with a clean, simple `.simple-arch-card`
  that uses the exact website color scheme (`var(--bg-surface)`, `var(--bg-elevated)`,
  `var(--text-primary)`, `var(--text-secondary)`, `var(--border-subtle)`, `${dept.color}`)
  and displays just 4 basic cost & ROI stat boxes + a 1-line monthly cost split.
- Simplifies cost tags on Persona, Directory, Periodic Table, and Mind Map cards to a
  clean 1-pill badge matching the website's native design.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML_FILES = [
    ROOT / "index.html",
    ROOT / "periodic_table.html",
    ROOT / "mind_map.html",
]

SIMPLE_COST_PANEL_JS = r"""
    /* =========================================================================
       SIMPLE AGENT COST DETAILS CARD (MATCHING WEBSITE THEME & DESIGN)
       ========================================================================= */
    function renderAgentCostAndRoiPanel(ag, dept) {
      const cm = ag.costModel;
      if (!cm) return '';
      const mb = cm.monthlyBreakdown;
      const vm = cm.valueModel;
      const modelShort = cm.modelName.replace(' (Vertex AI)', '');

      return `
        <div class="simple-arch-card" style="margin-top: 22px; margin-bottom: 22px;">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
            <div>
              <div style="font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:4px;">
                Cloud FinOps &amp; Value Summary
              </div>
              <h2 style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary); margin:0;">
                Estimated Cost Details — ${ag.name}
              </h2>
            </div>

            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class=" sc-tech-pill" style="border-color:${dept.color}55; color:${dept.color}; font-weight:700;">
                Model: ${modelShort}
              </span>
              <span class="sc-tech-pill" style="font-weight:700;">
                ~${cm.eventsPerDay.toLocaleString()} runs/day
              </span>
            </div>
          </div>

          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:14px;">
            <div style="padding:16px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-top:3px solid ${dept.color};">
              <div style="font-size:12px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                Enterprise Monthly Cost
              </div>
              <div style="font-family:var(--font-display); font-size:26px; font-weight:800; color:var(--text-primary); margin:6px 0 2px;">
                $${mb.totalFsp3YrUsd.toFixed(0)} <span style="font-size:14px; font-weight:600; color:var(--text-secondary);">/ mo</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-secondary);">
                $${Math.round(mb.annualCloudFsp3YrUsd).toLocaleString()} / year (with 3-Yr FSP)
              </div>
            </div>

            <div style="padding:16px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-top:3px solid ${dept.color};">
              <div style="font-size:12px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                Pilot Scale Cost (1 Site)
              </div>
              <div style="font-family:var(--font-display); font-size:26px; font-weight:800; color:var(--text-primary); margin:6px 0 2px;">
                $${mb.pilotScaleMoUsd.toFixed(0)} <span style="font-size:14px; font-weight:600; color:var(--text-secondary);">/ mo</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-secondary);">
                ~$${Math.round(mb.pilotScaleMoUsd * 12).toLocaleString()} / year pilot run rate
              </div>
            </div>

            <div style="padding:16px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-top:3px solid ${dept.color};">
              <div style="font-size:12px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                Cost per 1,000 Runs
              </div>
              <div style="font-family:var(--font-display); font-size:26px; font-weight:800; color:var(--text-primary); margin:6px 0 2px;">
                $${mb.blendedCostPer1kCallsUsd.toFixed(2)} <span style="font-size:14px; font-weight:600; color:var(--text-secondary);">/ 1K</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-secondary);">
                AI: $${mb.llmFsp3YrUsd.toFixed(0)} · Compute: $${mb.computeUsd.toFixed(0)} · Data: $${(mb.dataUsd + mb.apiUsd).toFixed(0)}
              </div>
            </div>

            <div style="padding:16px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-top:3px solid #10b981;">
              <div style="font-size:12px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                Estimated Annual Value
              </div>
              <div style="font-family:var(--font-display); font-size:26px; font-weight:800; color:#10b981; margin:6px 0 2px;">
                $${(vm.grossAnnualConservativeUsd / 1e6).toFixed(2)}M <span style="font-size:14px; font-weight:600; color:var(--text-secondary);">/ yr</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-secondary);">
                ${vm.cloudRoiMultipleConservative}x return · ${vm.paybackDays} days payback
              </div>
            </div>
          </div>
        </div>
      `;
    }
"""

CLEAN_OPEN_AGENT_PAGE_JS = r"""    function openAgentPage(agentId, pushHash = true, ev = null) {
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
                  🤖 ${other.name}
                </button>
              `).join('')}
            </div>
          </div>

          <!-- 1. What This Agent Does + Low-Code / Hybrid / High-Code Badge -->
          <div class="agent-hero-banner" style="padding: 30px 34px; margin-bottom: 24px;">
            <div style="position:relative; z-index:2; display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin-bottom:12px;">
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
            </div>
          </div>

          <!-- 2. Branching Multi-Stage Workflow Architecture Diagram -->
          ${renderSimpleAgentArchitectureDiagram(ag, dept)}

          <!-- 3. Simple Basic Cost Details Card (Same Website Design & Theme) -->
          ${renderAgentCostAndRoiPanel(ag, dept)}

          <!-- 4. Dedicated Box for a Video -->
          <div class="video-stage-box">
            <div class="video-toolbar" style="border-top:none; border-bottom:1px solid var(--border-subtle);">
              <span style="font-weight:700; color:var(--text-primary);">🎬 Agent Demo Video Box — ${ag.name}</span>
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

            <div class="video-viewport" id="agentVideoViewport" style="min-height: 380px;">
              ${stageViewMode === 'cad'
                ? renderInteractiveCadStage(ag.cadType || 'demand_wave', 'agentCadMount')
                : (hasVideo
                    ? `<video id="agentVideoPlayer" controls autoplay loop muted playsinline src="${videoUrl}"></video>`
                    : `
                      <div class="video-placeholder-stage">
                        <div class="video-placeholder-icon">▶</div>
                        <div style="font-family:var(--font-display); font-size:20px; font-weight:700; color:var(--text-primary);">
                          Demo Video Box · ${ag.name}
                        </div>
                        <div style="font-size:14.5px; color:var(--text-secondary); max-width:500px;">
                          Dedicated slot reserved for your demo video. Click <strong>Attach Video (.mp4)</strong> to load a recording, or switch to <strong>Interactive Preview</strong>.
                        </div>
                        <div style="display:flex; gap:10px; margin-top:6px;">
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
        </div>
      `;

      hydrateAssets();
      showActivePage('pageAgent');
      const wrap = document.getElementById('agentGenieWrap');
      if (sRect && wrap) {
        animateGenieOutOfBox(sRect, wrap, dept.color);
      }
    }"""

CLEAN_OPEN_BLUEPRINT_PAGE_JS = r"""    function openAgentBlueprintPage(agentId, pushHash = true, ev = null) {
      const ag = AGENTS[agentId];
      if (!ag) return;
      const useSlide = isPillOrNavSwitch(ev);
      const sRect = useSlide ? null : getClickedCardRect(ev);
      const transClass = getPageTransitionClass(ev, sRect);

      const dept = getDeptMeta(ag.deptId);

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
                <span>Back to ${ag.name}</span>
              </button>
              <button type="button" class="back-btn" onclick="goToOrgChart()">
                <span>6 SCOR Pillars</span>
              </button>
            </div>
          </div>

          ${renderSimpleAgentArchitectureDiagram(ag, dept)}

          ${renderAgentCostAndRoiPanel(ag, dept)}
        </div>
      `;

      hydrateAssets();
      showActivePage('pageBlueprint');
      const wrap = document.getElementById('blueprintGenieWrap');
      if (sRect && wrap) {
        animateGenieOutOfBox(sRect, wrap, dept.color);
      }
    }"""


def main() -> None:
    for path in HTML_FILES:
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")

        # 1. Replace `setSingleAgentScalePreset` + `updateSingleAgentCostCalc` + `renderAgentCostAndRoiPanel` with the simple version
        cost_fn_pattern = re.compile(
            r"    /\* =========================================================================\n       SINGLE-AGENT CLOUD COST, TOKENOMICS & 3-YEAR ROI SHOWCASE CALCULATOR[\s\S]*?function openAgentPage\(agentId, pushHash = true, ev = null\) \{",
            re.M,
        )
        if cost_fn_pattern.search(html):
            html = cost_fn_pattern.sub(
                lambda _: SIMPLE_COST_PANEL_JS.strip("\n") + "\n\n    function openAgentPage(agentId, pushHash = true, ev = null) {",
                html,
                count=1,
            )

        # 2. Replace `openAgentPage` with the clean, simple version (no ADK/XYZ data dump, no duplicate cost banner inside drawer)
        open_agent_pattern = re.compile(
            r"    function openAgentPage\(agentId, pushHash = true, ev = null\) \{[\s\S]*?\n    \}\n\n    function attachAgentVideo",
            re.M,
        )
        if not open_agent_pattern.search(html):
            raise RuntimeError(f"Could not find openAgentPage in {path}")
        html = open_agent_pattern.sub(
            lambda _: CLEAN_OPEN_AGENT_PAGE_JS + "\n\n    function attachAgentVideo",
            html,
            count=1,
        )

        # 3. Replace `openAgentBlueprintPage` with the clean, simple version
        open_bp_pattern = re.compile(
            r"    function openAgentBlueprintPage\(agentId, pushHash = true, ev = null\) \{[\s\S]*?\n    \}\n\n    function selectDemoTableTab",
            re.M,
        )
        if open_bp_pattern.search(html):
            html = open_bp_pattern.sub(
                lambda _: CLEAN_OPEN_BLUEPRINT_PAGE_JS + "\n\n    function selectDemoTableTab",
                html,
                count=1,
            )

        # 4. Simplify Persona Page `.persona-step-agent-box` & `.persona-agent-dock-card` cost badges to 1 clean pill
        old_step_cost = """                              ${plugAgent.costModel ? `
                                <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:7px;">
                                  <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; padding:3px 9px; border-radius:6px; background:rgba(2,132,199,0.12); color:#0284c7; border:1px solid rgba(2,132,199,0.3);">
                                    💰 Cloud: $${plugAgent.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo ($${plugAgent.costModel.monthlyBreakdown.blendedCostPer1kCallsUsd.toFixed(2)}/1K calls · ${plugAgent.costModel.modelName.replace(' (Vertex AI)', '')})
                                  </span>
                                  <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; padding:3px 9px; border-radius:6px; background:rgba(16,185,129,0.12); color:#059669; border:1px solid rgba(16,185,129,0.3);">
                                    📈 Value: $${(plugAgent.costModel.valueModel.grossAnnualConservativeUsd/1e6).toFixed(2)}M–$${(plugAgent.costModel.valueModel.grossAnnualLikelyUsd/1e6).toFixed(2)}M/yr (${plugAgent.costModel.valueModel.cloudRoiMultipleConservative}x ROI)
                                  </span>
                                </div>
                              ` : ''}"""
        new_step_cost = """                              ${plugAgent.costModel ? `
                                <div style="margin-top:6px;">
                                  <span style="font-family:var(--font-mono); font-size:11px; font-weight:700; color:var(--text-secondary);">
                                    💰 Est. Cost: <strong style="color:var(--text-primary);">$${plugAgent.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo</strong> ($${plugAgent.costModel.monthlyBreakdown.blendedCostPer1kCallsUsd.toFixed(2)}/1K runs)
                                  </span>
                                </div>
                              ` : ''}"""
        html = html.replace(old_step_cost, new_step_cost)

        old_dock_cost = """                      ${ag.costModel ? `
                        <div style="padding:8px 10px; border-radius:8px; background:rgba(2,132,199,0.08); border:1px solid rgba(2,132,199,0.25); font-family:var(--font-mono); font-size:11px; color:var(--text-primary); margin-top:4px; line-height:1.45;">
                          <div><strong>💰 Cloud Run Rate:</strong> $${ag.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo ($${ag.costModel.monthlyBreakdown.blendedCostPer1kCallsUsd.toFixed(2)}/1K calls)</div>
                          <div style="color:#059669; font-weight:800;"><strong>📈 Net Value:</strong> $${(ag.costModel.valueModel.grossAnnualConservativeUsd/1e6).toFixed(2)}M/yr (${ag.costModel.valueModel.cloudRoiMultipleConservative}x ROI · ${ag.costModel.valueModel.paybackDays}d payback)</div>
                        </div>
                      ` : ''}"""
        new_dock_cost = """                      ${ag.costModel ? `
                        <div style="font-family:var(--font-mono); font-size:11.5px; color:var(--text-secondary); margin-top:6px;">
                          💰 Est. Cost: <strong style="color:var(--text-primary);">$${ag.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo</strong> ($${ag.costModel.monthlyBreakdown.blendedCostPer1kCallsUsd.toFixed(2)}/1K)
                        </div>
                      ` : ''}"""
        html = html.replace(old_dock_cost, new_dock_cost)

        # 5. Clean up Periodic Table tiles (remove tiny text inside small tile) and simplify Sticky Inspector cost line
        html = html.replace(
            """                            ${ag.costModel ? `<div style="font-family:var(--font-mono); font-size:9.5px; font-weight:800; color:#0284c7; margin-top:2px;">$${ag.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo · ${ag.costModel.valueModel.cloudRoiMultipleConservative}x</div>` : ''}\n""",
            "",
        )

        old_pt_inspector_cost = """              <!-- Cloud Cost & ROI Summary inside Sticky Inspector -->
              ${selAg.costModel ? `
                <div style="padding:12px 14px; border-radius:12px; background:rgba(2,132,199,0.08); border:1px solid rgba(2,132,199,0.32); border-left:4px solid #0284c7; margin-bottom:14px;">
                  <div style="font-family:var(--font-mono); font-size:10.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:#0284c7; margin-bottom:6px;">
                    💰 Cloud FinOps &amp; 3-Year ROI (${selAg.costModel.modelName.replace(' (Vertex AI)', '')})
                  </div>
                  <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; font-family:var(--font-mono); font-size:11.5px; color:var(--text-primary);">
                    <div><span style="color:var(--text-secondary);">Enterprise:</span> <strong>$${selAg.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo</strong></div>
                    <div><span style="color:var(--text-secondary);">Pilot Scale:</span> <strong>$${selAg.costModel.monthlyBreakdown.pilotScaleMoUsd.toFixed(0)}/mo</strong></div>
                    <div><span style="color:var(--text-secondary);">Unit Cost:</span> <strong>$${selAg.costModel.monthlyBreakdown.blendedCostPer1kCallsUsd.toFixed(2)}/1K</strong></div>
                    <div><span style="color:var(--text-secondary);">Payback:</span> <strong>${selAg.costModel.valueModel.paybackDays} Days</strong></div>
                  </div>
                  <div style="margin-top:6px; padding-top:6px; border-top:1px dashed rgba(148,163,184,0.3); font-family:var(--font-mono); font-size:11.5px; font-weight:800; color:#059669;">
                    📈 Value: $${(selAg.costModel.valueModel.grossAnnualConservativeUsd/1e6).toFixed(2)}M–$${(selAg.costModel.valueModel.grossAnnualLikelyUsd/1e6).toFixed(2)}M/yr (${selAg.costModel.valueModel.cloudRoiMultipleConservative}x ROI)
                  </div>
                </div>
              ` : ''}"""
        new_pt_inspector_cost = """              ${selAg.costModel ? `
                <div style="padding:10px 12px; border-radius:10px; background:var(--bg-elevated); border:1px solid var(--border-subtle); margin-bottom:14px; font-family:var(--font-mono); font-size:11.5px; color:var(--text-secondary);">
                  💰 Est. Cost: <strong style="color:var(--text-primary);">$${selAg.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo</strong> · Pilot: <strong style="color:var(--text-primary);">$${selAg.costModel.monthlyBreakdown.pilotScaleMoUsd.toFixed(0)}/mo</strong> · <strong style="color:var(--text-primary);">$${selAg.costModel.monthlyBreakdown.blendedCostPer1kCallsUsd.toFixed(2)}/1K</strong>
                </div>
              ` : ''}"""
        html = html.replace(old_pt_inspector_cost, new_pt_inspector_cost)

        path.write_text(html, encoding="utf-8")
        print(f"✅ Simplified Agent Page & Cost Details in {path.name}")


if __name__ == "__main__":
    main()

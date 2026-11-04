#!/usr/bin/env python3
"""
Declutters and redesigns:
  1. Case Studies & Proof Hub (#pageEvidence / openEvidenceHubPage)
  2. Cost & ROI Hub (#pageCost / openCostTabPage / renderCostTabAgentRows / renderCostTabBenchmarkMethodologyPanel)
  3. Per-Agent Cost & ROI Panel (renderAgentCostAndRoiPanel)

Design principles requested by user:
  - Clean, breathable, highly readable layout (zero paragraph walls or pill soup)
  - Focus on crisp headings, key numbers, and direct clickable links
  - Progressive click-to-reveal (<details class="sc-clean-reveal">) for deeper context
  - Full Dark Mode + Light Mode contrast parity
  - Regenerates periodic_table.html, mind_map.html, docs/*, and zipline_dist/*
"""
import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path("/usr/local/google/home/zuhaibp/Supply_chain_Agentic_Transformation")
INDEX_HTML = ROOT / "index.html"

CLEAN_PROGRESSIVE_CSS = """
    /* =========================================================================
       CLEAN PROGRESSIVE-DISCLOSURE UI FOR PROOF & COST PAGES (DARK + LIGHT)
       ========================================================================= */
    .sc-ev-nav-shell {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 14px 18px;
      margin-bottom: 20px;
    }

    .sc-ev-filter-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 14px;
      align-items: end;
    }

    .sc-ev-filter-field {
      display: flex;
      flex-direction: column;
      gap: 5px;
    }

    .sc-ev-nav-label {
      font-family: var(--font-mono);
      font-size: 10.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-secondary);
    }

    .sc-clean-select {
      width: 100%;
      padding: 9px 12px;
      border-radius: 10px;
      background: var(--bg-elevated);
      color: var(--text-primary);
      border: 1px solid var(--border-strong);
      font-family: var(--font-sans);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: border-color 0.16s ease, box-shadow 0.16s ease;
    }

    .sc-clean-select:hover,
    .sc-clean-select:focus {
      border-color: var(--g-blue);
      outline: none;
    }

    /* Progressive Click-to-Reveal (<details>) */
    details.sc-clean-reveal {
      margin-top: 10px;
      border-top: 1px dashed var(--border-subtle);
      padding-top: 8px;
    }

    details.sc-clean-reveal > summary {
      list-style: none;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-weight: 700;
      color: var(--g-blue);
      user-select: none;
      padding: 3px 0;
      transition: color 0.15s ease, opacity 0.15s ease;
    }

    details.sc-clean-reveal > summary::-webkit-details-marker {
      display: none;
    }

    details.sc-clean-reveal > summary::before {
      content: '▸';
      font-size: 12px;
      transition: transform 0.18s ease;
      display: inline-block;
    }

    details.sc-clean-reveal[open] > summary::before {
      transform: rotate(90deg);
    }

    details.sc-clean-reveal > summary:hover {
      opacity: 0.85;
      text-decoration: underline;
    }

    .sc-clean-reveal-body {
      margin-top: 8px;
      padding: 11px 13px;
      border-radius: 11px;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      font-size: 13px;
      line-height: 1.58;
      color: var(--text-secondary);
    }

    /* Clean Expandable Accordion Rows for Benchmarks & Agent Economics */
    .sc-clean-pillar-group {
      margin-bottom: 22px;
    }

    .sc-clean-pillar-group:last-child {
      margin-bottom: 0;
    }

    .sc-clean-pillar-hdr {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding: 0 4px 10px;
      margin-bottom: 10px;
      border-bottom: 2px solid var(--border-subtle);
    }

    details.sc-clean-acc-item,
    details.sc-proof-target-focused {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 13px;
      margin-bottom: 9px;
      transition: border-color 0.16s ease, box-shadow 0.16s ease, background 0.16s ease;
    }

    details.sc-clean-acc-item:hover {
      border-color: var(--border-strong);
      box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
    }

    details.sc-proof-target-focused {
      border: 2px solid #10b981 !important;
      box-shadow: 0 10px 28px rgba(16, 185, 129, 0.15) !important;
      background: color-mix(in srgb, #10b981 5%, var(--bg-card));
    }

    details.sc-clean-acc-item > summary,
    details.sc-proof-target-focused > summary {
      list-style: none;
      cursor: pointer;
      padding: 14px 18px;
      display: grid;
      grid-template-columns: minmax(220px, 1.5fr) minmax(180px, 1.1fr) auto auto;
      align-items: center;
      gap: 14px;
      user-select: none;
    }

    details.sc-clean-acc-item > summary::-webkit-details-marker,
    details.sc-proof-target-focused > summary::-webkit-details-marker {
      display: none;
    }

    @media (max-width: 900px) {
      details.sc-clean-acc-item > summary,
      details.sc-proof-target-focused > summary {
        grid-template-columns: 1fr;
        gap: 8px;
      }
    }

    .sc-acc-chevron {
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 700;
      color: var(--text-secondary);
      padding: 4px 10px;
      border-radius: 999px;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      white-space: nowrap;
      transition: background 0.15s ease, color 0.15s ease;
    }

    details[open] > summary .sc-acc-chevron {
      background: var(--g-blue);
      color: #ffffff;
      border-color: var(--g-blue);
    }

    .sc-acc-drawer {
      padding: 0 18px 16px;
      border-top: 1px solid var(--border-subtle);
      padding-top: 14px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 14px;
    }

    .sc-acc-drawer-box {
      padding: 12px 14px;
      border-radius: 11px;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      font-size: 12.8px;
      line-height: 1.55;
      color: var(--text-secondary);
    }

    .sc-entity-inline-link {
      background: none;
      border: none;
      padding: 0;
      font: inherit;
      color: var(--text-primary);
      font-weight: 800;
      cursor: pointer;
      text-align: left;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: color 0.15s ease;
    }

    .sc-entity-inline-link:hover {
      color: var(--g-blue);
      text-decoration: underline;
    }

    .sc-entity-sub-link {
      background: none;
      border: none;
      padding: 0;
      font-size: 12.5px;
      font-weight: 600;
      color: var(--text-secondary);
      cursor: pointer;
      text-align: left;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: color 0.15s ease;
    }

    .sc-entity-sub-link:hover {
      color: var(--g-blue);
      text-decoration: underline;
    }

    .sc-proof-spotlight-card {
      background: var(--bg-card);
      border: 1.5px solid var(--spot-accent, #10b981);
      border-top: 4px solid var(--spot-accent, #10b981);
      border-radius: 18px;
      padding: 22px 24px;
      margin-bottom: 22px;
      box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
    }

    .sc-spot-clean-card {
      padding: 16px 18px;
      border-radius: 14px;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    html[data-theme="light"] .sc-spot-clean-card,
    html[data-theme="light"] .sc-acc-drawer-box,
    html[data-theme="light"] .sc-clean-reveal-body {
      background: #f8fafc;
      border-color: #e2e8f0;
    }

    html[data-theme="light"] details.sc-clean-acc-item {
      background: #ffffff;
      border-color: #e2e8f0;
    }

    html[data-theme="light"] details.sc-clean-acc-item:hover {
      border-color: #cbd5e1;
      box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
    }
"""

NEW_AGENT_COST_ROI_FN = """    function renderAgentCostAndRoiPanel(ag, dept) {
      const cm = ag.costModel || {};
      const mb = cm.monthlyBreakdown || {};
      const mc = cm.manualComparison || { manualHoursPerMonth: 320, manualMonthlyCostUsd: 24000, fteEquivalent: 2.0, directSavingsPct: 99.1, directMonthlySavingsUsd: 23780 };
      const vm = cm.valueModel || { grossAnnualConservativeUsd: 1100000, cloudRoiMultipleConservative: 430 };

      const aiMo = Math.round(mb.totalFsp3YrUsd || 210);
      const llmMo = Math.round(mb.llmFsp3YrUsd || 65);
      const compMo = Math.round(mb.computeUsd || 80);
      const dataMo = Math.round((mb.dataUsd || 45) + (mb.apiUsd || 20));
      const totSplit = Math.max(1, llmMo + compMo + dataMo);
      const llmPct = Math.round((llmMo / totSplit) * 100);
      const compPct = Math.round((compMo / totSplit) * 100);
      const dataPct = Math.max(1, 100 - llmPct - compPct);

      return `
        <div class="simple-arch-card" style="margin-top: 18px; margin-bottom: 18px; padding: 22px 24px;">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
            <div>
              <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:3px;">
                Unit Economics &amp; ROI
              </div>
              <h2 style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary); margin:0;">
                Cost vs. Value — ${cleanAgentName(ag.name)}
              </h2>
            </div>

            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <button type="button" class="switch-pill" onclick="openProofForAgent('${ag.id}', event)">
                📚 Supporting Proof &#8599;
              </button>
              <button type="button" class="switch-pill" onclick="openCostTabPage('${ag.deptId}', '${ag.id}', true)">
                📊 Full Cost Calculator &rarr;
              </button>
            </div>
          </div>

          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:14px;">
            <div class="sc-spot-clean-card" style="border-top:3px solid ${dept.color};">
              <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.05em; color:var(--text-secondary);">
                ✦ AI Run Cost
              </div>
              <div style="font-family:var(--font-display); font-size:28px; font-weight:800; color:var(--text-primary); margin-top:4px;">
                $${aiMo.toLocaleString()}<span style="font-size:14px; font-weight:600; color:var(--text-secondary);">/mo</span>
              </div>
            </div>

            <div class="sc-spot-clean-card" style="border-top:3px solid #f43f5e;">
              <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.05em; color:var(--text-secondary);">
                ✕ Manual Baseline
              </div>
              <div style="font-family:var(--font-display); font-size:28px; font-weight:800; color:#f43f5e; margin-top:4px;">
                $${mc.manualMonthlyCostUsd.toLocaleString()}<span style="font-size:14px; font-weight:600; color:var(--text-secondary);">/mo</span>
              </div>
            </div>

            <div class="sc-spot-clean-card sc-impact-link-box" style="border-top:3px solid #10b981; --imp-accent:#10b981;" onclick="openProofForAgent('${ag.id}', event)" title="Click to inspect supporting proof &amp; case study">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.05em; color:#10b981;">🚀 Modeled Value</span>
                <span class="sc-impact-cue">&#8599;</span>
              </div>
              <div style="font-family:var(--font-display); font-size:28px; font-weight:800; color:#10b981; margin-top:4px;">
                $${(vm.grossAnnualConservativeUsd / 1e6).toFixed(2)}M<span style="font-size:14px; font-weight:600; color:var(--text-secondary);">/yr</span>
              </div>
            </div>
          </div>

          <details class="sc-clean-reveal">
            <summary>Reveal token, compute &amp; manual effort breakdown</summary>
            <div class="sc-clean-reveal-body" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(230px, 1fr)); gap:14px;">
              <div>
                <div style="font-weight:800; color:var(--text-primary); margin-bottom:4px;">Cloud &amp; Token Economics</div>
                <div>$${(mb.blendedCostPer1kCallsUsd || 2.45).toFixed(2)} per 1K runs (~${(cm.eventsPerDay || 2800).toLocaleString()} runs/day)</div>
                <div style="margin-top:6px; font-family:var(--font-mono); font-size:12px;">
                  🟢 LLM $${llmMo} (${llmPct}%) · 🔵 ADK $${compMo} (${compPct}%) · 🟣 Data $${dataMo} (${dataPct}%)
                </div>
              </div>
              <div>
                <div style="font-weight:800; color:var(--text-primary); margin-bottom:4px;">Manual Effort Saved (${mc.directSavingsPct}% Lower)</div>
                <div>Replaces ~${mc.manualHoursPerMonth} hrs/mo (~${mc.fteEquivalent} FTEs) of spreadsheet &amp; exception triage, saving $${mc.directMonthlySavingsUsd.toLocaleString()}/mo directly.</div>
              </div>
            </div>
          </details>
        </div>
      `;
    }"""

NEW_OPEN_COST_TAB_FN = """    function openCostTabPage(pillarFilter = 'all', highlightAgentId = null, pushState = true, ev = null) {
      if (pillarFilter && pillarFilter !== 'all') {
        currentCostTabPillar = pillarFilter;
        currentCostSectionTab = 'agents';
      } else if (highlightAgentId) {
        currentCostSectionTab = 'agents';
      } else if (!currentCostSectionTab) {
        currentCostSectionTab = 'pillars';
      }
      if (pushState) {
        history.pushState({ page: 'cost', pillar: currentCostTabPillar }, '', currentCostTabPillar === 'all' ? '#cost' : `#cost/${currentCostTabPillar}`);
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
          <div style="padding:22px 24px; border-radius:18px; background:var(--bg-card); border:1px solid var(--border-strong); border-top:4px solid ${dept.color}; display:flex; flex-direction:column; justify-content:space-between; gap:14px;">
            <div>
              <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; margin-bottom:6px;">
                <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:${dept.color}; text-transform:uppercase; letter-spacing:0.06em;">
                  ${dept.vNum || ''} · ${dept.scorBadge || 'PILLAR'}
                </span>
                <span class="sc-tech-pill" style="padding:2px 9px; font-size:11px; font-weight:700;">
                  ${pAgents.length} Agents
                </span>
              </div>

              <h3 onclick="switchCostSectionTab('agents', '${dept.id}')" style="cursor:pointer; font-family:var(--font-display); font-size:19px; font-weight:800; color:var(--text-primary); margin:0 0 14px;">
                ${dept.name}
              </h3>

              <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; padding:12px 14px; border-radius:12px; background:var(--bg-elevated); border:1px solid var(--border-subtle);">
                <div>
                  <div style="font-size:11px; color:var(--text-secondary); font-weight:700;">✦ AI Run Cost</div>
                  <div style="font-family:var(--font-display); font-size:20px; font-weight:800; color:var(--text-primary); margin-top:2px;">
                    $${Math.round(pAiMo).toLocaleString()}<span style="font-size:11.5px; font-weight:500; color:var(--text-secondary);">/mo</span>
                  </div>
                </div>
                <div>
                  <div style="font-size:11px; color:var(--text-secondary); font-weight:700;">🚀 Modeled Value</div>
                  <div style="font-family:var(--font-display); font-size:20px; font-weight:800; color:#10b981; margin-top:2px;">
                    $${(pValYr / 1e6).toFixed(1)}M<span style="font-size:11.5px; font-weight:500; color:var(--text-secondary);">/yr</span>
                  </div>
                </div>
              </div>

              <details class="sc-clean-reveal">
                <summary>Reveal manual baseline &amp; infra split</summary>
                <div class="sc-clean-reveal-body">
                  <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:12.5px;">
                    <span>Manual Baseline: <strong style="color:#f43f5e;">$${Math.round(pManMo / 1000)}K/mo</strong></span>
                    <span style="font-weight:700; color:${dept.color};">~${pFte.toFixed(0)} FTEs</span>
                  </div>
                  <div style="height:6px; border-radius:999px; background:var(--border-subtle); overflow:hidden; display:flex; gap:2px; margin-bottom:6px;">
                    <div style="width:${lPct}%; height:100%; background:#10b981;"></div>
                    <div style="width:${cPct}%; height:100%; background:#38bdf8;"></div>
                    <div style="width:${dPct}%; height:100%; background:#a855f7;"></div>
                  </div>
                  <div style="font-size:11.5px; color:var(--text-secondary);">
                    Tokens $${Math.round(pLlm)} · Compute $${Math.round(pComp)} · Data $${Math.round(pData)}
                  </div>
                </div>
              </details>
            </div>

            <button type="button" onclick="switchCostSectionTab('agents', '${dept.id}')" style="background:none; border:none; border-top:1px solid var(--border-subtle); padding:11px 0 0; cursor:pointer; display:flex; align-items:center; justify-content:space-between; font-size:13px; font-weight:800; color:${dept.color}; width:100%;">
              <span>Inspect ${pAgents.length} Pillar Agents</span>
              <span>&rarr;</span>
            </button>
          </div>
        `;
      }).join('');

      container.innerHTML = `
        <div class="subpage-topbar" style="margin-bottom: 18px;">
          <button type="button" class="back-btn" onclick="goToOrgChart()">
            <span>&larr;</span>
            <span>Back to ${deptList.length} Pillars</span>
          </button>

          <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
            <button type="button" class="switch-pill" style="font-weight:700;" onclick="openEvidenceHubPage('all', true, event)">
              📚 Case Studies &amp; Proof &rarr;
            </button>
            <a href="cost_analysis_presentation.html" class="switch-pill" style="text-decoration:none; font-weight:700;">
              📊 9-Slide FinOps Deck &#8599;
            </a>
          </div>
        </div>

        <!-- Clean Executive Summary -->
        <div class="simple-arch-card" style="padding: 26px 28px; margin-bottom: 20px;">
          <div style="margin-bottom: 18px;">
            <div style="font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:var(--g-blue); margin-bottom:4px;">
              Cloud FinOps &amp; ROI · ${deptList.length} Pillars · ${allAgents.length} AI Agents
            </div>
            <h1 style="font-family:var(--font-display); font-size:clamp(25px, 2.8vw, 32px); font-weight:800; color:var(--text-primary); margin:0 0 6px;">
              Supply Chain AI Cost &amp; ROI
            </h1>
            <p style="font-size:14px; color:var(--text-secondary); margin:0;">
              Select a pillar or agent below to inspect unit costs, or click to reveal underlying assumptions.
            </p>
          </div>

          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:14px;">
            <div style="padding:16px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-top:3px solid var(--g-blue);">
              <div style="font-size:11px; font-weight:800; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                ✦ Monthly AI Cost
              </div>
              <div style="font-family:var(--font-display); font-size:28px; font-weight:800; color:var(--text-primary); margin-top:6px;">
                $${Math.round(totalAiMo).toLocaleString()}<span style="font-size:13.5px; font-weight:600; color:var(--text-secondary);">/mo</span>
              </div>
            </div>

            <div style="padding:16px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-top:3px solid #f43f5e;">
              <div style="font-size:11px; font-weight:800; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                ✕ Manual Baseline
              </div>
              <div style="font-family:var(--font-display); font-size:28px; font-weight:800; color:#f43f5e; margin-top:6px;">
                $${(totalManualMo / 1e6).toFixed(2)}M<span style="font-size:13.5px; font-weight:600; color:var(--text-secondary);">/mo</span>
              </div>
            </div>

            <div style="padding:16px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-top:3px solid #38bdf8;">
              <div style="font-size:11px; font-weight:800; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                ⚡ Cost Reduction
              </div>
              <div style="font-family:var(--font-display); font-size:28px; font-weight:800; color:#38bdf8; margin-top:6px;">
                ${savingsPctOverall}%<span style="font-size:13.5px; font-weight:600; color:var(--text-secondary);"> Lower</span>
              </div>
            </div>

            <div style="padding:16px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-top:3px solid #10b981;">
              <div style="font-size:11px; font-weight:800; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                🚀 Modeled Value
              </div>
              <div style="font-family:var(--font-display); font-size:28px; font-weight:800; color:#10b981; margin-top:6px;">
                $${(totalValYr / 1e6).toFixed(1)}M<span style="font-size:13.5px; font-weight:600; color:var(--text-secondary);">/yr</span>
              </div>
            </div>
          </div>

          <details class="sc-clean-reveal">
            <summary>Reveal pricing &amp; FTE baseline assumptions</summary>
            <div class="sc-clean-reveal-body">
              <strong>AI Run Rate ($${Math.round(totalAiMo * 12).toLocaleString()}/yr):</strong> Bottom-up Vertex AI token + ADK runtime + BigQuery cost across ${allAgents.length} active agents under 3-Yr FSP (-20%), routing 85% Gemini Flash / 15% Gemini Pro (excludes end-user workspace seats).<br/>
              <strong>Manual Baseline (~${Math.round(totalFtes)} FTEs):</strong> Equivalent analyst &amp; planner hours spent on spreadsheet reconciliation, ERP exception triage, and manual expediting (~$${Math.round(totalAiMo / Math.max(1, allAgents.length))}/mo avg AI agent vs. ~$23.5K/mo manual).
            </div>
          </details>
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
          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(310px, 1fr)); gap: 18px;">
            ${pillarCardsHtml}
          </div>
        ` : ''}

        ${currentCostSectionTab === 'agents' ? `
          <div class="simple-arch-card" style="padding: 24px 26px;">
            <div style="display:flex; justify-content:space-between; align-items:flex-end; flex-wrap:wrap; gap:14px; margin-bottom:18px;">
              <div>
                <h2 style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary); margin:0 0 4px;">
                  Agent-by-Agent Unit Economics
                </h2>
                <p style="font-size:13px; color:var(--text-secondary); margin:0;">
                  Click any agent heading to launch its workflow, or click <strong>Details</strong> to reveal unit economics.
                </p>
              </div>
              <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                <select class="sc-clean-select" style="width:auto; min-width:210px;" onchange="filterCostTabByPillar(this.value)">
                  <option value="all" ${currentCostTabPillar === 'all' ? 'selected' : ''}>All Operating Pillars (${allAgents.length})</option>
                  ${deptList.map(d => {
                    const cnt = allAgents.filter(a => a.deptId === d.id).length;
                    return `<option value="${d.id}" ${currentCostTabPillar === d.id ? 'selected' : ''}>${d.vNum} · ${d.name} (${cnt})</option>`;
                  }).join('')}
                </select>
                <input type="text" id="costTabSearchInput" placeholder="🔍 Search agent or role..." value="${currentCostTabSearch}" oninput="onCostTabSearchInput(this.value)" class="sc-clean-select" style="width:auto; min-width:220px;" />
                <span id="costTabAgentCountBadge" class="sc-tech-pill" style="font-weight:800; padding:6px 12px;">${allAgents.length} Agents</span>
              </div>
            </div>

            <div id="costTabAgentsTbody"></div>
          </div>
        ` : ''}

        ${currentCostSectionTab === 'simulator' ? `
          <div class="simple-arch-card" style="padding: 24px 26px; margin-bottom: 20px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:18px;">
              <div>
                <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:#10b981; margin-bottom:3px;">
                  Interactive Cloud FinOps Sizer
                </div>
                <h2 style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary); margin:0;">
                  Dynamic Scale Simulator
                </h2>
              </div>

              <div style="display:flex; gap:8px; flex-wrap:wrap;">
                <button type="button" class="sc-tech-pill" style="cursor:pointer; font-weight:700; padding:6px 12px;" onclick="applyWebCostPreset(10, 250000, 88, 75, 20)">
                  1. Pilot (10)
                </button>
                <button type="button" class="sc-tech-pill" style="cursor:pointer; font-weight:700; padding:6px 12px;" onclick="applyWebCostPreset(30, 1500000, 85, 75, 20)">
                  2. Regional (30)
                </button>
                <button type="button" class="sc-tech-pill" style="cursor:pointer; font-weight:700; padding:6px 12px; border-color:var(--g-blue); color:var(--g-blue);" onclick="applyWebCostPreset(${allAgents.length}, 5200000, 85, 75, 20)">
                  3. Enterprise (${allAgents.length})
                </button>
                <button type="button" class="sc-tech-pill" style="cursor:pointer; font-weight:700; padding:6px 12px;" onclick="applyWebCostPreset(${allAgents.length}, 20000000, 85, 80, 20)">
                  4. Hyperscale (20M)
                </button>
              </div>
            </div>

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(310px, 1fr)); gap:20px;">
              <div style="padding:18px 20px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); display:flex; flex-direction:column; gap:14px;">
                <div>
                  <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; margin-bottom:5px;">
                    <span style="color:var(--text-primary);">1. Active AI Agents</span>
                    <span id="wCalcLblAgents" style="color:var(--g-blue);">${allAgents.length} Agents</span>
                  </div>
                  <input type="range" id="wCalcRngAgents" min="1" max="60" step="1" value="${allAgents.length}" style="width:100%; accent-color:var(--g-blue); cursor:pointer;" oninput="updateWebCostCalculator()" />
                </div>

                <div>
                  <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; margin-bottom:5px;">
                    <span style="color:var(--text-primary);">2. Monthly Invocations</span>
                    <span id="wCalcLblCalls" style="color:var(--g-blue);">5,200,000 / mo</span>
                  </div>
                  <input type="range" id="wCalcRngCalls" min="50000" max="25000000" step="50000" value="5200000" style="width:100%; accent-color:var(--g-blue); cursor:pointer;" oninput="updateWebCostCalculator()" />
                </div>

                <div>
                  <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; margin-bottom:5px;">
                    <span style="color:var(--text-primary);">3. Flash vs. Pro Routing</span>
                    <span id="wCalcLblFlash" style="color:#10b981;">85% Flash / 15% Pro·Argon</span>
                  </div>
                  <input type="range" id="wCalcRngFlash" min="50" max="95" step="5" value="85" style="width:100%; accent-color:#10b981; cursor:pointer;" oninput="updateWebCostCalculator()" />
                </div>

                <div>
                  <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; margin-bottom:5px;">
                    <span style="color:var(--text-primary);">4. Context Cache Hit Rate</span>
                    <span id="wCalcLblCache" style="color:#a855f7;">75% Cache Hit</span>
                  </div>
                  <input type="range" id="wCalcRngCache" min="0" max="90" step="5" value="75" style="width:100%; accent-color:#a855f7; cursor:pointer;" oninput="updateWebCostCalculator()" />
                </div>

                <div>
                  <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; margin-bottom:5px;">
                    <span style="color:var(--text-primary);">5. Vertex AI Commit (FSP)</span>
                    <span id="wCalcLblFsp" style="color:#f59e0b;">3-Yr FSP (-20%)</span>
                  </div>
                  <select id="wCalcSelFsp" onchange="updateWebCostCalculator()" class="sc-clean-select">
                    <option value="0">Pay-As-You-Go (0% Discount)</option>
                    <option value="10">1-Year Vertex AI FSP (-10% Discount)</option>
                    <option value="20" selected>3-Year Vertex AI FSP (-20% Discount)</option>
                  </select>
                </div>
              </div>

              <div style="padding:18px 20px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); display:flex; flex-direction:column; justify-content:space-between; gap:14px;">
                <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:12px;">
                  <div style="padding:14px; border-radius:12px; background:var(--bg-surface); border:1px solid var(--border-subtle); border-top:3px solid var(--g-blue);">
                    <div style="font-size:11px; font-weight:700; color:var(--text-secondary); text-transform:uppercase;">✦ AI Cost / Mo</div>
                    <div id="wCalcOutAiMo" style="font-family:var(--font-display); font-size:23px; font-weight:800; color:var(--text-primary); margin-top:4px;">$12,843</div>
                    <div id="wCalcOutPer1k" style="font-size:11.5px; color:var(--text-secondary);">$2.47 / 1K runs</div>
                  </div>
                  <div style="padding:14px; border-radius:12px; background:var(--bg-surface); border:1px solid var(--border-subtle); border-top:3px solid #f43f5e;">
                    <div style="font-size:11px; font-weight:700; color:var(--text-secondary); text-transform:uppercase;">✕ Manual / Mo</div>
                    <div id="wCalcOutManMo" style="font-family:var(--font-display); font-size:23px; font-weight:800; color:#f43f5e; margin-top:4px;">$1.41M</div>
                    <div id="wCalcOutFtes" style="font-size:11.5px; color:var(--text-secondary);">~124 FTEs manual</div>
                  </div>
                  <div style="padding:14px; border-radius:12px; background:var(--bg-surface); border:1px solid var(--border-subtle); border-top:3px solid #10b981;">
                    <div style="font-size:11px; font-weight:700; color:var(--text-secondary); text-transform:uppercase;">🚀 Value / Yr</div>
                    <div id="wCalcOutValYr" style="font-family:var(--font-display); font-size:23px; font-weight:800; color:#10b981; margin-top:4px;">$66.6M</div>
                    <div id="wCalcOutRoi" style="font-size:11.5px; color:var(--text-secondary);">432x Cloud ROI</div>
                  </div>
                </div>

                <details class="sc-clean-reveal" open>
                  <summary>Monthly infra split &amp; scale comparison</summary>
                  <div class="sc-clean-reveal-body" style="background:var(--bg-surface);">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                      <span style="font-size:11px; font-weight:700; color:var(--text-secondary); text-transform:uppercase;">Token / Compute / Data Split</span>
                      <span id="wCalcAnnualAiLbl" style="font-size:11.5px; font-weight:700; color:var(--text-secondary);">$154.1K / yr</span>
                    </div>
                    <div style="height:8px; border-radius:999px; background:var(--border-subtle); overflow:hidden; display:flex; gap:2px; margin-bottom:10px;">
                      <div id="wCalcSplitLlmBar" style="width:38%; height:100%; background:#10b981;"></div>
                      <div id="wCalcSplitCompBar" style="width:34%; height:100%; background:#38bdf8;"></div>
                      <div id="wCalcSplitDataBar" style="width:28%; height:100%; background:#a855f7;"></div>
                    </div>
                    <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:8px; font-size:12px; margin-bottom:12px;">
                      <div>🟢 Tokens: <strong id="wCalcSplitLlmVal" style="color:var(--text-primary);">$4,880/mo</strong></div>
                      <div>🔵 Compute: <strong id="wCalcSplitCompVal" style="color:var(--text-primary);">$4,360/mo</strong></div>
                      <div>🟣 Data/BQ: <strong id="wCalcSplitDataVal" style="color:var(--text-primary);">$3,603/mo</strong></div>
                    </div>
                    <div style="font-size:11.5px; color:var(--text-secondary); display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px; padding-top:8px; border-top:1px solid var(--border-subtle);">
                      <span>AI: <strong id="wCalcBarAiLbl">$12,843 / mo</strong><span id="wCalcBarAiFill" style="display:none;"></span></span>
                      <span>Manual: <strong id="wCalcBarManLbl" style="color:#f43f5e;">$1,410,000 / mo</strong><span id="wCalcBarManFill" style="display:none;"></span></span>
                      <span>Value: <strong id="wCalcBarValLbl" style="color:#10b981;">$5,550,000 / mo</strong></span>
                    </div>
                  </div>
                </details>
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
    }"""

NEW_RENDER_COST_ROWS_FN = """    function renderCostTabAgentRows(highlightAgentId = null) {
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
        const llmMo = Math.round(mb.llmFsp3YrUsd || 65);
        const compMo = Math.round(mb.computeUsd || 80);
        const dataMo = Math.round((mb.dataUsd || 45) + (mb.apiUsd || 20));
        const isHl = Boolean(highlightAgentId && ag.id === highlightAgentId);

        return `
          <details class="${isHl ? 'sc-proof-target-focused' : 'sc-clean-acc-item'}" ${isHl ? 'open' : ''}>
            <summary>
              <div>
                <button type="button" class="sc-entity-inline-link" onclick="event.stopPropagation(); openAgentPage('${ag.id}', true, event)">
                  ${renderInlineAgentSvg(ag, 15, ag.subPillarColor || dept.color)}
                  <span>${cleanAgentName(ag.name)} &rarr;</span>
                </button>
                <div style="font-size:12px; color:var(--text-secondary); margin-top:2px;">
                  ${ag.primaryPersonaName || ag.subPillarName || dept.name}
                </div>
              </div>

              <div>
                <span class="sc-tech-pill" style="font-size:11px; padding:3px 9px; border-color:${dept.color}55; color:${dept.color}; font-weight:700;">
                  ${dept.vNum || ''} · ${dept.name}
                </span>
              </div>

              <div style="display:flex; align-items:center; gap:16px; font-family:var(--font-mono); font-size:13.5px;">
                <span title="Monthly AI Run Cost"><strong style="color:var(--g-blue);">$${aiMo.toLocaleString()}/mo</strong></span>
                <span title="Modeled Annual Value"><strong style="color:#10b981;">$${((vm.grossAnnualConservativeUsd || 1100000) / 1e6).toFixed(2)}M/yr</strong></span>
              </div>

              <span class="sc-acc-chevron">Details</span>
            </summary>

            <div class="sc-acc-drawer">
              <div class="sc-acc-drawer-box">
                <div style="font-weight:800; color:var(--text-primary); margin-bottom:4px;">AI Infrastructure &amp; Token Split</div>
                <div>$${(mb.blendedCostPer1kCallsUsd || 2.45).toFixed(2)} / 1K runs · Tokens $${llmMo} · Compute $${compMo} · Data $${dataMo}/mo</div>
              </div>
              <div class="sc-acc-drawer-box">
                <div style="font-weight:800; color:var(--text-primary); margin-bottom:4px;">Manual Effort Baseline</div>
                <div><strong style="color:#f43f5e;">$${(mc.manualMonthlyCostUsd || 24000).toLocaleString()}/mo</strong> (~${mc.fteEquivalent} FTEs · -${mc.directSavingsPct}% direct cost reduction)</div>
              </div>
              <div class="sc-acc-drawer-box" style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px;">
                <button type="button" class="sc-ext-link-pill" style="cursor:pointer;" onclick="openAgentPage('${ag.id}', true, event)">
                  Open Agent Workflow &rarr;
                </button>
                <button type="button" class="sc-ext-link-pill" style="cursor:pointer;" onclick="openProofForAgent('${ag.id}', event)">
                  Supporting Proof &#8599;
                </button>
              </div>
            </div>
          </details>
        `;
      }).join('');
    }"""

NEW_COST_METHODOLOGY_FN = """    function renderCostTabBenchmarkMethodologyPanel() {
      return `
        <div class="simple-arch-card" style="margin-bottom: 20px; padding: 22px 26px;">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:14px;">
            <div>
              <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:#10b981;">
                Empirical Cost Sources
              </div>
              <h2 style="font-family:var(--font-display); font-size:20px; font-weight:800; color:var(--text-primary); margin:2px 0 0;">
                Industry Problem Benchmarks &amp; Source Links
              </h2>
            </div>
            <button type="button" class="switch-pill" onclick="currentEvidenceTab='benchmarks'; openEvidenceHubPage('all', true, event)" style="padding:7px 14px; font-size:12.5px; font-weight:800; cursor:pointer;">
              📚 All 60 Problem-Data Profiles &rarr;
            </button>
          </div>

          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:12px;">
            <div class="sc-spot-clean-card">
              <div>
                <div style="font-weight:800; color:var(--text-primary); font-size:14.5px; margin-bottom:8px;">01 · Forecast &amp; Promo Distortion</div>
                <a href="https://www.ihlservices.com/product/inventory-distortion/" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill">IHL Group $1.77T Report &#8599;</a>
              </div>
              <details class="sc-clean-reveal">
                <summary>Reveal benchmark context</summary>
                <div class="sc-clean-reveal-body">IHL Group cites $1.77T/yr stockout &amp; overstock distortion; NielsenIQ finds 59%–67% of CPG trade promotions fail to break even.</div>
              </details>
            </div>

            <div class="sc-spot-clean-card">
              <div>
                <div style="font-weight:800; color:var(--text-primary); font-size:14.5px; margin-bottom:8px;">02 · Procurement &amp; AP Cost</div>
                <a href="https://www.thehackettgroup.com/insights/the-ai-procurement-performance-gap-how-leaders-achieve-3-7x-greater-roi/" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill">Hackett &amp; APQC Data &#8599;</a>
              </div>
              <details class="sc-clean-reveal">
                <summary>Reveal benchmark context</summary>
                <div class="sc-clean-reveal-body">APQC &amp; Hackett document $12.88–$15.96 per manual invoice vs. $2.18 digital and 3%–6% off-contract tail-spend leakage.</div>
              </details>
            </div>

            <div class="sc-spot-clean-card">
              <div>
                <div style="font-weight:800; color:var(--text-primary); font-size:14.5px; margin-bottom:8px;">03 · Plant Downtime &amp; Quality</div>
                <a href="https://www.weforum.org/publications/global-lighthouse-network-unlocking-sustainability-through-fourth-industrial-revolution-technologies/" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill">WEF Global Lighthouse &#8599;</a>
              </div>
              <details class="sc-clean-reveal">
                <summary>Reveal benchmark context</summary>
                <div class="sc-clean-reveal-body">Unplanned downtime erodes 5%–20% of manufacturing capacity; ASQ/WEF cite 3%–8% COGS lost to scrap and 7–18 day batch QA holds.</div>
              </details>
            </div>

            <div class="sc-spot-clean-card">
              <div>
                <div style="font-weight:800; color:var(--text-primary); font-size:14.5px; margin-bottom:8px;">04–06 · DC Walk, Fleet &amp; Returns</div>
                <a href="https://nrf.com/media-center/press-releases/nrf-and-happy-returns-report-2024-retail-returns-total-890-billion" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill">NRF &amp; ATRI Reports &#8599;</a>
              </div>
              <details class="sc-clean-reveal">
                <summary>Reveal benchmark context</summary>
                <div class="sc-clean-reveal-body">Georgia Tech cites 55% picker travel time; ATRI cites $2.27/mi trucking cost &amp; 20%+ empty miles; NRF cites $890B annual retail returns.</div>
              </details>
            </div>
          </div>
        </div>
      `;
    }"""

NEW_OPEN_EVIDENCE_FN = """    function jumpEvidenceEntitySelect(val) {
      if (!val) return;
      const [kind, id] = val.split(':');
      if (kind === 'persona' && id) {
        openProofForPersona(id, null);
      } else if (kind === 'agent' && id) {
        openProofForAgent(id, null);
      }
    }

    function openEvidenceHubPage(pillarFilter = 'all', pushState = true, ev = null, focusCtx = undefined, subPillarFilter = undefined) {
      if (focusCtx !== undefined) {
        currentEvidenceFocus = focusCtx;
      }
      if (subPillarFilter !== undefined) {
        currentEvidenceSubPillar = subPillarFilter || 'all';
      } else if (pillarFilter === 'all' && !currentEvidenceFocus) {
        currentEvidenceSubPillar = 'all';
      }

      const liveDepts = Object.values(DEPARTMENTS);
      if (pillarFilter && pillarFilter !== 'all' && !DEPARTMENTS[pillarFilter]) {
        const matchDept = liveDepts.find(d =>
          d.id === pillarFilter ||
          (d.subPillars || []).some(sp => (SUBPILLAR_ID_TO_CANONICAL[sp.id] && PILLAR_PROOF_BENCHMARKS.some(pb => pb.deptId === pillarFilter)))
        );
        currentEvidencePillar = matchDept ? matchDept.id : 'all';
      } else {
        currentEvidencePillar = pillarFilter || 'all';
      }

      const activeDeptObj = currentEvidencePillar !== 'all' ? DEPARTMENTS[currentEvidencePillar] : null;
      if (activeDeptObj && currentEvidenceSubPillar !== 'all') {
        const hasSp = (activeDeptObj.subPillars || []).some(sp => sp.id === currentEvidenceSubPillar);
        if (!hasSp) currentEvidenceSubPillar = 'all';
      }

      if (pushState) {
        let hash = '#evidence';
        if (currentEvidenceFocus && currentEvidenceFocus.kind && currentEvidenceFocus.id) {
          hash = `#evidence/${currentEvidenceFocus.kind}/${currentEvidenceFocus.id}`;
        } else if (currentEvidenceSubPillar && currentEvidenceSubPillar !== 'all') {
          hash = `#evidence/subpillar/${currentEvidenceSubPillar}`;
        } else if (currentEvidencePillar !== 'all') {
          hash = `#evidence/${currentEvidencePillar}`;
        }
        history.pushState({
          page: 'evidence',
          pillar: currentEvidencePillar,
          subPillar: currentEvidenceSubPillar,
          focus: currentEvidenceFocus
        }, '', hash);
      }

      const container = document.getElementById('evidencePageContent');
      if (!container) return;

      const pillarCount = liveDepts.length;
      const agentCount = Object.keys(AGENTS).length;

      // Build dynamic Case Study -> Live Pillars, Sub-Pillars, Personas & Agents index
      const caseLiveLinks = {};
      ENTERPRISE_CASE_STUDIES.forEach(cs => {
        caseLiveLinks[cs.id] = { deptIds: new Set(), subPillars: [], personas: [], agents: [] };
      });

      liveDepts.forEach(d => {
        (d.subPillars || []).forEach(sp => {
          const primaryCsId = SUBPILLAR_PRIMARY_CASE_ID[sp.id];
          if (primaryCsId && caseLiveLinks[primaryCsId]) {
            caseLiveLinks[primaryCsId].deptIds.add(d.id);
            if (!caseLiveLinks[primaryCsId].subPillars.some(x => x.id === sp.id)) {
              caseLiveLinks[primaryCsId].subPillars.push({ id: sp.id, name: sp.name, color: sp.color || d.color, deptId: d.id });
            }
          }
          (sp.items || []).forEach(it => {
            const p = PERSONAS[it.personaId];
            const ag = AGENTS[it.agentId];
            const agCsId = (ag && AGENT_SPECIFIC_CASE_OVERRIDE[ag.id]) || primaryCsId;
            if (p && primaryCsId && caseLiveLinks[primaryCsId]) {
              if (!caseLiveLinks[primaryCsId].personas.some(x => x.id === p.id)) {
                caseLiveLinks[primaryCsId].personas.push(p);
              }
            }
            if (ag && agCsId && caseLiveLinks[agCsId]) {
              caseLiveLinks[agCsId].deptIds.add(d.id);
              if (!caseLiveLinks[agCsId].agents.some(x => x.id === ag.id)) {
                caseLiveLinks[agCsId].agents.push(ag);
              }
            }
          });
        });
      });

      ENTERPRISE_CASE_STUDIES.forEach(cs => {
        (cs.agentIds || []).forEach(aid => {
          const ag = AGENTS[aid];
          if (ag && caseLiveLinks[cs.id]) {
            const spId = resolveEntitySubPillarId(ag);
            const ld = resolveLiveDeptForSubPillar(spId, ag.deptId);
            if (ld) caseLiveLinks[cs.id].deptIds.add(ld.id);
            if (!caseLiveLinks[cs.id].agents.some(x => x.id === ag.id)) {
              caseLiveLinks[cs.id].agents.push(ag);
            }
          }
        });
      });

      // Resolve focused entity (Persona or Agent) if arriving from a clicked Impact Box
      let focusedEntity = null;
      let focusedProof = null;
      let focusedDept = null;
      let focusedSubPillar = null;
      let focusedCaseId = null;
      let focusedAgentId = null;

      if (currentEvidenceFocus && currentEvidenceFocus.id) {
        if (currentEvidenceFocus.kind === 'agent' && AGENTS[currentEvidenceFocus.id]) {
          focusedEntity = AGENTS[currentEvidenceFocus.id];
          focusedAgentId = focusedEntity.id;
          const spId = resolveEntitySubPillarId(focusedEntity);
          focusedDept = resolveLiveDeptForSubPillar(spId, focusedEntity.deptId);
          focusedSubPillar = focusedDept ? (focusedDept.subPillars || []).find(s => s.id === spId) : null;
          focusedProof = getProofForAgent(focusedEntity, focusedDept);
          focusedCaseId = focusedProof.primaryCaseId;
        } else if (currentEvidenceFocus.kind === 'persona' && PERSONAS[currentEvidenceFocus.id]) {
          focusedEntity = PERSONAS[currentEvidenceFocus.id];
          focusedAgentId = focusedEntity.primaryAgentId || (focusedEntity.agentIds && focusedEntity.agentIds[0]) || null;
          const spId = resolveEntitySubPillarId(focusedEntity);
          focusedDept = resolveLiveDeptForSubPillar(spId, focusedEntity.deptId);
          focusedSubPillar = focusedDept ? (focusedDept.subPillars || []).find(s => s.id === spId) : null;
          focusedProof = getProofForPersona(focusedEntity, focusedDept);
          focusedCaseId = focusedProof.primaryCaseId;
        }
      } else if (currentEvidenceSubPillar && currentEvidenceSubPillar !== 'all') {
        const spProof = getProofForSubPillarId(currentEvidenceSubPillar);
        focusedCaseId = spProof.primaryCaseId;
      }

      // Filter Case Studies
      let filteredCases = ENTERPRISE_CASE_STUDIES.filter(cs => {
        const meta = caseLiveLinks[cs.id];
        if (currentEvidenceSubPillar && currentEvidenceSubPillar !== 'all') {
          return meta.subPillars.some(s => s.id === currentEvidenceSubPillar) ||
                 meta.agents.some(a => resolveEntitySubPillarId(a) === currentEvidenceSubPillar) ||
                 cs.id === focusedCaseId;
        }
        if (currentEvidencePillar === 'all') return true;
        return meta.deptIds.has(currentEvidencePillar) || cs.deptIds.includes(currentEvidencePillar) || cs.id === focusedCaseId;
      });

      if (focusedCaseId) {
        filteredCases = filteredCases.slice().sort((a, b) => (a.id === focusedCaseId ? -1 : b.id === focusedCaseId ? 1 : 0));
      }

      // Compact Single-Row Filter Dropdowns (replaces multi-row pill clutter)
      const activeSubPillars = activeDeptObj
        ? (activeDeptObj.subPillars || [])
        : liveDepts.flatMap(d => (d.subPillars || []).map(sp => ({ ...sp, _deptId: d.id, _deptNum: d.vNum })));

      const activeSpObj = (activeDeptObj ? (activeDeptObj.subPillars || []) : activeSubPillars)
        .find(s => s.id === currentEvidenceSubPillar) || null;

      const scopedItems = activeSpObj
        ? (activeSpObj.items || [])
        : (activeDeptObj ? (activeDeptObj.subPillars || []).flatMap(sp => sp.items || []) : []);

      const selectedEntityVal = (focusedEntity && currentEvidenceFocus)
        ? `${currentEvidenceFocus.kind}:${focusedEntity.id}`
        : '';

      const cleanFilterBarHtml = `
        <div class="sc-ev-nav-shell">
          <div class="sc-ev-filter-grid">
            <div class="sc-ev-filter-field">
              <label class="sc-ev-nav-label">Operating Pillars:</label>
              <select class="sc-clean-select" onchange="currentEvidenceFocus=null; currentEvidenceSubPillar='all'; openEvidenceHubPage(this.value, true, event)">
                <option value="all" ${currentEvidencePillar === 'all' ? 'selected' : ''}>All ${pillarCount} Pillars (${agentCount} Profiles)</option>
                ${liveDepts.map(d => `<option value="${d.id}" ${currentEvidencePillar === d.id ? 'selected' : ''}>${d.vNum} · ${d.name}</option>`).join('')}
              </select>
            </div>

            <div class="sc-ev-filter-field">
              <label class="sc-ev-nav-label">Sub-Pillars:</label>
              <select class="sc-clean-select" onchange="const v=this.value; if(v==='all'){selectEvidenceSubPillar('${currentEvidencePillar}', 'all', event);} else {const [did,spid]=v.split('::'); selectEvidenceSubPillar(did, spid, event);}">
                <option value="all" ${currentEvidenceSubPillar === 'all' ? 'selected' : ''}>All Sub-Pillars (${activeSubPillars.length})</option>
                ${activeSubPillars.map(sp => {
                  const did = activeDeptObj ? activeDeptObj.id : sp._deptId;
                  const prefix = activeDeptObj ? '' : `${sp._deptNum} · `;
                  return `<option value="${did}::${sp.id}" ${currentEvidenceSubPillar === sp.id ? 'selected' : ''}>${prefix}${sp.name}</option>`;
                }).join('')}
              </select>
            </div>

            <div class="sc-ev-filter-field">
              <label class="sc-ev-nav-label">Personas &amp; Agents:</label>
              <select class="sc-clean-select" onchange="jumpEvidenceEntitySelect(this.value)">
                <option value="">Jump to Persona or AI Agent...</option>
                ${(scopedItems.length ? scopedItems : liveDepts.flatMap(d => (d.subPillars || []).flatMap(sp => sp.items || []))).map(it => {
                  const p = PERSONAS[it.personaId];
                  const ag = AGENTS[it.agentId];
                  let opts = '';
                  if (p) opts += `<option value="persona:${p.id}" ${selectedEntityVal === `persona:${p.id}` ? 'selected' : ''}>Role · ${p.name}</option>`;
                  if (ag) opts += `<option value="agent:${ag.id}" ${selectedEntityVal === `agent:${ag.id}` ? 'selected' : ''}>Agent · ${cleanAgentName(ag.name)}</option>`;
                  return opts;
                }).join('')}
              </select>
            </div>

            ${(currentEvidencePillar !== 'all' || currentEvidenceSubPillar !== 'all' || focusedEntity) ? `
              <div style="display:flex; align-items:center;">
                <button type="button" class="switch-pill" style="width:100%; justify-content:center; padding:9px 14px; font-weight:700;" onclick="currentEvidenceFocus=null; currentEvidenceSubPillar='all'; openEvidenceHubPage('all', true, event)">
                  ↺ Show All ${pillarCount} Pillars
                </button>
              </div>
            ` : ''}
          </div>
        </div>
      `;

      // Clean 3-Card Focused Spotlight: Headings & Direct Links First, Click to Reveal Context
      let spotlightHtml = '';
      if (focusedEntity && focusedProof && focusedProof.caseStudy) {
        const isAgent = currentEvidenceFocus.kind === 'agent';
        const entityLabel = isAgent ? cleanAgentName(focusedEntity.name) : focusedEntity.name;
        const spotAccent = (focusedSubPillar && focusedSubPillar.color) || (focusedDept && focusedDept.color) || '#10b981';
        const entityIcon = isAgent ? renderAgentIconBadge(focusedEntity, 38, spotAccent) : renderPersonaIconBadge(focusedEntity, 38, spotAccent);
        const headlineImpact = isAgent
          ? (focusedProof.agentBadge || focusedEntity.badge || 'Modeled ROI')
          : `${focusedEntity.headlineStat}`;
        const cs = focusedProof.caseStudy;
        const pairedAgent = focusedAgentId ? AGENTS[focusedAgentId] : null;

        spotlightHtml = `
          <div id="evidenceFocusedSpotlight" class="sc-proof-spotlight-card" style="--spot-accent:${spotAccent};">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
              <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
                ${entityIcon}
                <div>
                  <div style="font-family:var(--font-mono); font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:${spotAccent};">
                    ${focusedDept ? `${focusedDept.vNum} · ${focusedDept.name}` : 'Operating Pillar'}${focusedSubPillar ? ` &rarr; ${focusedSubPillar.name}` : ''}
                  </div>
                  <h2 style="font-family:var(--font-display); font-size:clamp(19px, 2vw, 23px); font-weight:800; color:var(--text-primary); margin:2px 0 0;">
                    ${entityLabel}
                  </h2>
                </div>
              </div>

              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                <button type="button" class="agent-plug-btn" style="padding:8px 14px; font-size:12.5px;"
                        onclick="${isAgent ? `openAgentPage('${focusedEntity.id}', true, event)` : `openPersonaPage('${focusedEntity.id}', true, event)`}">
                  <span>&larr; Back to ${entityLabel}</span>
                </button>
              </div>
            </div>

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:14px;">
              <!-- Card 1: Backed Problem & Cost Data -->
              <div class="sc-spot-clean-card" style="border-top:3px solid #f43f5e;">
                <div>
                  <div style="font-size:10.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:#f43f5e; margin-bottom:6px;">
                    01 · Backed Problem &amp; Cost Data
                  </div>
                  <div style="font-weight:800; font-size:15.5px; color:var(--text-primary); line-height:1.38; margin-bottom:10px;">
                    ${focusedProof.problemCostMetric}
                  </div>
                  <div style="display:flex; flex-wrap:wrap; gap:6px;">
                    <a href="${focusedProof.problemUrl}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill">
                      <span>${focusedProof.problemOrg}</span>
                      <span>&#8599;</span>
                    </a>
                    ${focusedProof.problemAltUrl ? `
                      <a href="${focusedProof.problemAltUrl}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill">
                        <span>Secondary Source</span>
                        <span>&#8599;</span>
                      </a>
                    ` : ''}
                  </div>
                </div>
                <details class="sc-clean-reveal">
                  <summary>Reveal problem context</summary>
                  <div class="sc-clean-reveal-body">${focusedProof.problemFinding}</div>
                </details>
              </div>

              <!-- Card 2: Potential Impact With Our Agent -->
              <div class="sc-spot-clean-card" style="border-top:3px solid #10b981;">
                <div>
                  <div style="font-size:10.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:#10b981; margin-bottom:6px;">
                    02 · Potential Impact With Our Agent
                  </div>
                  <div style="font-weight:800; font-size:15.5px; color:#10b981; line-height:1.38; margin-bottom:10px;">
                    🚀 ${focusedProof.agentBadge || headlineImpact}
                  </div>
                  ${pairedAgent ? `
                    <button type="button" class="sc-ext-link-pill" style="cursor:pointer;" onclick="openAgentPage('${pairedAgent.id}', true, event)">
                      <span>Open ${cleanAgentName(pairedAgent.name)}</span>
                      <span>&rarr;</span>
                    </button>
                  ` : ''}
                </div>
                <details class="sc-clean-reveal">
                  <summary>Reveal how our agent achieves this</summary>
                  <div class="sc-clean-reveal-body">
                    <strong>${focusedProof.beforeState || 'Manual'} &rarr; ${focusedProof.afterState || 'Agentic'}:</strong> ${focusedProof.potentialMechanism || ''}
                  </div>
                </details>
              </div>

              <!-- Card 3: Supporting Reference Case -->
              <div class="sc-spot-clean-card" style="border-top:3px solid ${cs.accent || spotAccent};">
                <div>
                  <div style="font-size:10.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:${spotAccent}; margin-bottom:6px;">
                    03 · Reference Deployment
                  </div>
                  <div style="font-weight:800; font-size:15.5px; color:var(--text-primary); line-height:1.38; margin-bottom:10px;">
                    ${cs.company} · ${cs.headlineMetric}
                  </div>
                  <a href="${cs.url}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill">
                    <span>${cs.sourceLabel}</span>
                    <span>&#8599;</span>
                  </a>
                </div>
                <details class="sc-clean-reveal">
                  <summary>Reveal deployment outcome</summary>
                  <div class="sc-clean-reveal-body">${cs.outcome}</div>
                </details>
              </div>
            </div>
          </div>
        `;
      }

      // Tab 1: Clean Pillar-Grouped Expandable Rows (Headings + Source Links First, Click to Reveal Context!)
      const visibleBenchDepts = currentEvidencePillar === 'all'
        ? liveDepts
        : liveDepts.filter(d => d.id === currentEvidencePillar);

      const problemDataGroupsHtml = visibleBenchDepts.map(d => {
        const spList = (d.subPillars || []).filter(sp => currentEvidenceSubPillar === 'all' || sp.id === currentEvidenceSubPillar);
        const rowsHtml = spList.map(sp => {
          return (sp.items || []).map(it => {
            const p = PERSONAS[it.personaId];
            const ag = AGENTS[it.agentId];
            if (!p || !ag) return '';
            const pr = getProofForAgent(ag, d);
            const cs = pr.caseStudy;
            const isFocusedRow = Boolean(focusedAgentId && ag.id === focusedAgentId);

            return `
              <details id="proofRow_${ag.id}" class="${isFocusedRow ? 'sc-proof-target-focused' : 'sc-clean-acc-item'}" ${isFocusedRow ? 'open' : ''}>
                <summary>
                  <div>
                    <button type="button" class="sc-entity-inline-link" onclick="event.stopPropagation(); openAgentPage('${ag.id}', true, event)">
                      ${renderInlineAgentSvg(ag, 15, ag.subPillarColor || d.color)}
                      <span>${cleanAgentName(ag.name)} &rarr;</span>
                    </button>
                    <div style="margin-top:3px;">
                      <button type="button" class="sc-entity-sub-link" onclick="event.stopPropagation(); openPersonaPage('${p.id}', true, event)">
                        <span>${p.name}</span>
                        <span>&middot; ${sp.name}</span>
                      </button>
                    </div>
                  </div>

                  <div>
                    <span class="sc-impact-pill-link" style="pointer-events:none; font-size:11.5px; padding:4px 10px;">
                      🚀 ${pr.agentBadge || ag.badge}
                    </span>
                  </div>

                  <div>
                    <a href="${pr.problemUrl}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill" onclick="event.stopPropagation();" style="font-size:11.5px; padding:5px 10px;">
                      <span>${pr.problemOrg}</span>
                      <span>&#8599;</span>
                    </a>
                  </div>

                  <span class="sc-acc-chevron">Context</span>
                </summary>

                <div class="sc-acc-drawer">
                  <div class="sc-acc-drawer-box">
                    <div style="font-size:11px; font-weight:800; text-transform:uppercase; color:#f43f5e; margin-bottom:4px;">Backed Problem Data</div>
                    <div style="font-weight:800; color:var(--text-primary); margin-bottom:4px;">${pr.problemCostMetric}</div>
                    <div>${pr.problemFinding}</div>
                  </div>

                  <div class="sc-acc-drawer-box">
                    <div style="font-size:11px; font-weight:800; text-transform:uppercase; color:#10b981; margin-bottom:4px;">Modeled Agentic Impact</div>
                    <div style="font-weight:800; color:var(--text-primary); margin-bottom:4px;">${p.toilHoursBefore} &rarr; ${p.toilHoursAfter}</div>
                    <div>${pr.potentialMechanism || ag.outcome}</div>
                  </div>

                  <div class="sc-acc-drawer-box" style="display:flex; flex-direction:column; justify-content:space-between; gap:8px;">
                    <div>
                      <div style="font-size:11px; font-weight:800; text-transform:uppercase; color:${d.color}; margin-bottom:4px;">Reference Case Study</div>
                      <div style="font-weight:800; color:var(--text-primary);">${cs.company} · ${cs.headlineMetric}</div>
                    </div>
                    <div>
                      <a href="${cs.url}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill" style="font-size:11.5px;">
                        <span>${cs.sourceLabel}</span>
                        <span>&#8599;</span>
                      </a>
                    </div>
                  </div>
                </div>
              </details>
            `;
          }).join('');
        }).join('');

        if (!rowsHtml.trim()) return '';
        return `
          <div class="sc-clean-pillar-group">
            <div class="sc-clean-pillar-hdr">
              <div style="display:flex; align-items:center; gap:8px;">
                <span style="width:10px; height:10px; border-radius:50%; background:${d.color}; display:inline-block;"></span>
                <h3 style="font-family:var(--font-display); font-size:16.5px; font-weight:800; color:var(--text-primary); margin:0;">
                  ${d.vNum} · ${d.name}
                </h3>
              </div>
              <span style="font-family:var(--font-mono); font-size:11.5px; color:var(--text-secondary); font-weight:700;">
                Click any row to reveal context
              </span>
            </div>
            ${rowsHtml}
          </div>
        `;
      }).join('');

      // Tab 2: Clean Reference Case Study Cards (Heading + Metric + Links Visible; Story & Agent Chips Revealed on Click!)
      const caseCardsHtml = filteredCases.map(cs => {
        const liveMeta = caseLiveLinks[cs.id] || { deptIds: new Set(), subPillars: [], personas: [], agents: [] };
        const isTargetCard = focusedCaseId === cs.id;

        const pillarBadges = Array.from(liveMeta.deptIds).map(did => {
          const d = DEPARTMENTS[did];
          if (!d) return '';
          return `<button type="button" class="sc-tech-pill" onclick="currentEvidenceFocus=null; currentEvidenceSubPillar='all'; openEvidenceHubPage('${d.id}', true, event)" style="cursor:pointer; font-size:11px; padding:3px 9px; color:${d.color}; border-color:${d.color}55; font-weight:700;">${d.vNum} · ${d.name}</button>`;
        }).join('');

        const personaChips = liveMeta.personas.slice(0, 4).map(p => `
          <button type="button" class="sc-tech-pill" onclick="openPersonaPage('${p.id}', true, event)" style="cursor:pointer; font-size:11.5px; font-weight:700; padding:4px 9px;">
            ${p.name} &rarr;
          </button>
        `).join('');

        const agentChips = liveMeta.agents.slice(0, 5).map(ag => `
          <button type="button" class="sc-tech-pill" onclick="openAgentPage('${ag.id}', true, event)" style="cursor:pointer; font-size:11.5px; font-weight:700; padding:4px 9px;">
            ${cleanAgentName(ag.name)} &rarr;
          </button>
        `).join('');

        return `
          <div id="caseCard_${cs.id}" class="sc-v22-cs-card ${isTargetCard ? 'sc-proof-target-focused' : ''}" style="--cs-accent:${cs.accent}; padding:22px 24px;">
            <div>
              <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:10px;">
                <div style="display:flex; gap:6px; flex-wrap:wrap;">${pillarBadges}</div>
                <span style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; padding:4px 10px; border-radius:8px; background:${cs.accent}18; color:${cs.accent}; border:1px solid ${cs.accent}45;">
                  ${cs.headlineMetric}
                </span>
              </div>

              <h3 style="font-family:var(--font-display); font-size:20px; font-weight:800; color:var(--text-primary); line-height:1.28; margin:0 0 4px;">
                ${cs.company}
              </h3>
              <div style="font-size:12.5px; font-weight:600; color:var(--text-secondary); margin-bottom:14px;">
                ${cs.industry}
              </div>

              <div style="display:flex; flex-wrap:wrap; gap:8px;">
                <a href="${cs.url}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill">
                  <span>${cs.sourceLabel}</span>
                  <span>&#8599;</span>
                </a>
                ${cs.secondaryUrl ? `
                  <a href="${cs.secondaryUrl}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill">
                    <span>${cs.secondaryLabel}</span>
                    <span>&#8599;</span>
                  </a>
                ` : ''}
              </div>
            </div>

            <details class="sc-clean-reveal" ${isTargetCard ? 'open' : ''}>
              <summary>Reveal challenge, outcome &amp; linked agents (${liveMeta.agents.length})</summary>
              <div class="sc-clean-reveal-body">
                <div style="margin-bottom:8px;"><strong style="color:var(--text-primary);">Challenge:</strong> ${cs.problem}</div>
                <div style="margin-bottom:10px;"><strong style="color:#10b981;">Verified Outcome:</strong> ${cs.outcome}</div>
                ${personaChips ? `<div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:6px;">${personaChips}</div>` : ''}
                ${agentChips ? `<div style="display:flex; flex-wrap:wrap; gap:6px;">${agentChips}</div>` : ''}
              </div>
            </details>
          </div>
        `;
      }).join('');

      // Tab 3: Clean Research Report Headings & Direct Links (Key Metric Revealed on Click!)
      const researchCardsHtml = VERIFIED_RESEARCH_SOURCES.map(src => `
        <div class="sc-spot-clean-card" style="padding:18px 20px; background:var(--bg-card);">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; margin-bottom:6px;">
              <span style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:var(--g-blue);">${src.org}</span>
              <span style="font-size:10.5px; font-weight:700; padding:2px 8px; border-radius:999px; background:var(--bg-elevated); color:var(--text-secondary); border:1px solid var(--border-subtle);">${src.type}</span>
            </div>
            <a href="${src.url}" target="_blank" rel="noopener noreferrer" style="text-decoration:none; display:block; font-weight:800; font-size:15.5px; color:var(--text-primary); line-height:1.4; margin-bottom:12px;">
              ${src.title}
            </a>
            <a href="${src.url}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill">
              <span>Open Official Report / Data</span>
              <span>&#8599;</span>
            </a>
          </div>
          <details class="sc-clean-reveal">
            <summary>Reveal benchmark finding</summary>
            <div class="sc-clean-reveal-body">${src.metric}</div>
          </details>
        </div>
      `).join('');

      container.innerHTML = `
        <div class="page-slide-right">
          <div class="back-bar" style="margin-bottom:18px;">
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              <button type="button" class="back-btn" onclick="goToOrgChart()">
                <span>&larr;</span>
                <span>Back to ${pillarCount} Operating Pillars</span>
              </button>
              <button type="button" class="back-btn" onclick="openPersonasDirectoryPage('all', '', true, 'personas', event)">
                <span>Personas</span>
              </button>
              <button type="button" class="back-btn" onclick="openPersonasDirectoryPage('all', '', true, 'agents', event)">
                <span>AI Agents (${agentCount})</span>
              </button>
              <button type="button" class="back-btn" onclick="openCostTabPage('all', null, true, event)">
                <span>💰 Cost &amp; ROI</span>
              </button>
            </div>
          </div>

          <!-- Clean Airy Header -->
          <div class="simple-arch-card" style="padding: 24px 28px; margin-bottom: 18px;">
            <div style="font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:#10b981; margin-bottom:4px;">
              Benchmarks, Case Studies &amp; Primary Sources
            </div>
            <h1 style="font-family:var(--font-display); font-size:clamp(24px, 2.8vw, 32px); font-weight:800; color:var(--text-primary); margin:0 0 6px;">
              Case Studies, Benchmarks &amp; Proof
            </h1>
            <p style="font-size:14px; color:var(--text-secondary); margin:0;">
              Open any source link directly, or click any item below to reveal supporting context.
            </p>
          </div>

          <!-- Crisp 3-Tab Segmented Control -->
          <div class="sc-v22-tab-strip">
            <button type="button" class="sc-v22-tab-btn ${currentEvidenceTab === 'benchmarks' ? 'active' : ''}" onclick="switchEvidenceTab('benchmarks')">
              <span>1 · Problem Data &amp; Potential ROI</span>
              <span class="sc-v22-tab-count">${agentCount}</span>
            </button>
            <button type="button" class="sc-v22-tab-btn ${currentEvidenceTab === 'cases' ? 'active' : ''}" onclick="switchEvidenceTab('cases')">
              <span>2 · Reference Case Studies</span>
              <span class="sc-v22-tab-count">${ENTERPRISE_CASE_STUDIES.length}</span>
            </button>
            <button type="button" class="sc-v22-tab-btn ${currentEvidenceTab === 'sources' ? 'active' : ''}" onclick="switchEvidenceTab('sources')">
              <span>3 · Primary Research Reports</span>
              <span class="sc-v22-tab-count">${VERIFIED_RESEARCH_SOURCES.length}</span>
            </button>
          </div>

          <!-- Compact 1-Row Filter Bar -->
          ${cleanFilterBarHtml}

          <!-- Focused Spotlight Card when arriving from a Persona or Agent Impact Box -->
          ${spotlightHtml}

          ${currentEvidenceTab === 'benchmarks' ? `
            <div class="simple-arch-card" style="padding: 22px 24px;">
              <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:18px;">
                <h2 style="font-family:var(--font-display); font-size:19px; font-weight:800; color:var(--text-primary); margin:0;">
                  Backed Problem Cost Data vs. Modeled Agentic Impact
                </h2>
                <span style="font-size:12.5px; color:var(--text-secondary);">
                  Headings &amp; direct report links shown — click <strong>Context</strong> to expand
                </span>
              </div>
              ${problemDataGroupsHtml}
            </div>
          ` : ''}

          ${currentEvidenceTab === 'cases' ? `
            <div class="sc-v22-cs-grid">
              ${caseCardsHtml}
            </div>
          ` : ''}

          ${currentEvidenceTab === 'sources' ? `
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap:16px;">
              ${researchCardsHtml}
            </div>
          ` : ''}
        </div>
      `;

      showActivePage('pageEvidence');
      if (focusedEntity) {
        setTimeout(() => {
          const spot = document.getElementById('evidenceFocusedSpotlight');
          if (spot) spot.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 50);
      }
    }"""


def replace_between(src: str, start_marker: str, end_marker: str, replacement: str) -> str:
    s = src.find(start_marker)
    assert s != -1, f"Missing start marker: {start_marker}"
    e = src.find(end_marker, s)
    assert e != -1, f"Missing end marker: {end_marker}"
    return src[:s] + replacement + "\n\n" + src[e:]


def main():
    html = INDEX_HTML.read_text(encoding="utf-8")

    # 1. Inject or replace Clean Progressive-Disclosure CSS
    css_anchor = "/* Evidence Hub Navigation Hierarchy & Focused Spotlight */"
    css_end = "/* =========================================================================\n       PROGRESSIVE PILLAR -> SUB-PILLAR -> PERSONA STAGE CASCADE & FLOW ANIMATIONS"
    if "CLEAN PROGRESSIVE-DISCLOSURE UI FOR PROOF & COST PAGES" in html:
        s = html.find("/* =========================================================================\n       CLEAN PROGRESSIVE-DISCLOSURE UI FOR PROOF & COST PAGES")
        e = html.find(css_end, s)
        assert s != -1 and e != -1
        html = html[:s] + CLEAN_PROGRESSIVE_CSS.strip() + "\n\n    " + html[e:]
    else:
        s = html.find(css_anchor)
        e = html.find(css_end, s)
        assert s != -1 and e != -1, "Could not locate Evidence CSS block"
        # Keep Light Mode impact hover rules that start at /* Crisp Light Mode Contrast Guarantees
        lm_anchor = "/* Crisp Light Mode Contrast Guarantees for Impact Hover & Proof Spotlight */"
        lm_pos = html.find(lm_anchor, s)
        assert lm_pos != -1 and lm_pos < e
        html = html[:s] + CLEAN_PROGRESSIVE_CSS.strip() + "\n\n    " + html[lm_pos:]

    # 2. Replace renderAgentCostAndRoiPanel
    html = replace_between(
        html,
        "    function renderAgentCostAndRoiPanel(ag, dept) {",
        "    function inferColumnTypeAndConstraint(colName, rows) {",
        NEW_AGENT_COST_ROI_FN,
    )

    # 3. Replace openCostTabPage
    open_cost_start = (
        "    function openCostTabPage(pillarFilter = 'all', highlightAgentId = null, pushState = true, ev = null) {"
        if "    function openCostTabPage(pillarFilter = 'all', highlightAgentId = null, pushState = true, ev = null) {" in html
        else "    function openCostTabPage(pillarFilter = 'all', highlightAgentId = null, pushState = true) {"
    )
    html = replace_between(
        html,
        open_cost_start,
        "    function applyWebCostPreset(agents, calls, flashPct, cachePct, fspVal) {",
        NEW_OPEN_COST_TAB_FN,
    )

    # 4. Replace renderCostTabAgentRows
    html = replace_between(
        html,
        "    function renderCostTabAgentRows(highlightAgentId = null) {",
        "    function showActivePage(pageId) {",
        NEW_RENDER_COST_ROWS_FN,
    )

    # 5. Replace renderCostTabBenchmarkMethodologyPanel
    html = replace_between(
        html,
        "    function renderCostTabBenchmarkMethodologyPanel() {",
        "    let currentEvidenceTab = 'benchmarks';",
        NEW_COST_METHODOLOGY_FN,
    )

    # 6. Replace openEvidenceHubPage
    start_ev = "    function jumpEvidenceEntitySelect(val) {" if "function jumpEvidenceEntitySelect(val)" in html else "    function openEvidenceHubPage("
    html = replace_between(
        html,
        start_ev,
        "    function handleUrlHash() {",
        NEW_OPEN_EVIDENCE_FN,
    )

    # 7. Ensure handleUrlHash respects window.__BOOT_PAGE__ for standalone periodic_table.html & mind_map.html
    boot_hook = """      if (window.__BOOT_PAGE__ === 'periodic') {
        openPeriodicTablePage('all', null, false);
        return;
      }
      if (window.__BOOT_PAGE__ === 'mindmap') {
        openMindMapPage('mindmap', null, null, false);
        return;
      }
"""
    if "window.__BOOT_PAGE__ === 'periodic'" not in html:
        target_home = "      showActivePage('pageHome');"
        assert target_home in html, "Could not find showActivePage('pageHome') in handleUrlHash"
        html = html.replace(target_home, boot_hook + target_home, 1)

    INDEX_HTML.write_text(html, encoding="utf-8")
    print("✅ Updated index.html with clean, scannable, click-to-reveal Case Studies & Proof and Cost & ROI pages!")

    def build_standalone_variant(base_html: str, boot_key: str, hash_target: str) -> str:
        variant = base_html.replace(
            "<script>",
            f"<script>\n    window.__BOOT_PAGE__ = '{boot_key}';",
            1,
        )
        old_pop = """    window.addEventListener('popstate', () => {\n      handleUrlHash();\n    });"""
        new_pop = f"""    window.addEventListener('popstate', () => {{\n      if (!window.location.hash) {{ try {{ history.replaceState(null, '', '{hash_target}'); }} catch (e) {{}} }} handleUrlHash();\n    }});"""
        if old_pop in variant:
            variant = variant.replace(old_pop, new_pop, 1)

        old_boot = """      hydrateAssets();\n      handleUrlHash();"""
        new_boot = f"""      if (!window.location.hash) {{ try {{ history.replaceState(null, '', '{hash_target}'); }} catch (e) {{ window.location.hash = '{hash_target}'; }} }}\n      hydrateAssets();\n      handleUrlHash();"""
        if old_boot in variant:
            variant = variant.replace(old_boot, new_boot, 1)
        return variant

    periodic_html = build_standalone_variant(html, "periodic", "#periodic")
    mindmap_html = build_standalone_variant(html, "mindmap", "#mindmap")
    (ROOT / "periodic_table.html").write_text(periodic_html, encoding="utf-8")
    (ROOT / "mind_map.html").write_text(mindmap_html, encoding="utf-8")

    html_sync_names = [
        "index.html",
        "periodic_table.html",
        "mind_map.html",
        "cost_analysis_presentation.html",
        "agent_testing_and_video_playbook.html",
        "supply_chain_101_interactive_academy.html",
    ]
    for folder in ["docs", "zipline_dist"]:
        dest_dir = ROOT / folder
        if dest_dir.exists():
            for fname in html_sync_names:
                src_f = ROOT / fname
                if src_f.exists():
                    shutil.copy2(src_f, dest_dir / fname)
            cat_src = ROOT / "data" / "supply_chain_catalog.json"
            cat_dst = dest_dir / "data" / "supply_chain_catalog.json"
            if cat_src.exists() and cat_dst.parent.exists():
                shutil.copy2(cat_src, cat_dst)
    print("✅ Synced periodic_table.html, mind_map.html, docs/*, and zipline_dist/*!")

    dist_dir = ROOT / "zipline_dist"
    zip_targets = [
        ROOT / "supply_chain_zipline_bundle.zip",
        ROOT / "Supply_Chain_Agentic_Portal.zip",
        ROOT / "Zipline_Supply_Chain_Agentic_Portal.zip",
        ROOT / "zipline" / "supply_chain_zipline_bundle.zip",
        ROOT / "zipline" / "supply_chain_zipline_folder_bundle.zip",
        ROOT / "zipline" / "supply_chain_zipline_light.zip",
    ]
    if dist_dir.exists():
        for zpath in zip_targets:
            if not zpath.exists():
                continue
            wrap_folder = ""
            try:
                with zipfile.ZipFile(zpath, "r") as zprev:
                    names = zprev.namelist()
                    if names and "/" in names[0]:
                        first_seg = names[0].split("/", 1)[0]
                        if all(n.startswith(first_seg + "/") for n in names if not n.endswith("/")):
                            wrap_folder = first_seg
            except Exception:
                wrap_folder = "zipline_dist" if "folder_bundle" in zpath.name else ""

            with zipfile.ZipFile(zpath, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                for item in sorted(dist_dir.rglob("*")):
                    if item.is_file():
                        rel = item.relative_to(dist_dir)
                        arcname = f"{wrap_folder}/{rel.as_posix()}" if wrap_folder else rel.as_posix()
                        zf.write(item, arcname)
            print(f"✅ Refreshed {zpath.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

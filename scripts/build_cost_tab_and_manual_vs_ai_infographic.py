#!/usr/bin/env python3
"""Builds the visual AI Cost vs. Manual Effort vs. Business Value infographic breakdown
and adds the interactive Dynamic Cost & ROI Calculator Tab (`#pageCost` / `#cost`)
directly into `index.html`, `periodic_table.html`, and `mind_map.html` in the exact same
website design language (simple on the eyes, minimal text, visual bars & breakdowns).
Also updates `cost_analysis_presentation.html` with the Manual Effort comparison.
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SIMPLE_AGENT_COST_AND_MANUAL_PANEL_JS = r"""    /* =========================================================================
       SIMPLE AGENT COST DETAILS CARD (AI COST VS. MANUAL ESTIMATE + INFOGRAPHIC)
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
              <div style="font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:4px;">
                Infra &amp; Token Cost vs. Manual Estimate
              </div>
              <h2 style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary); margin:0;">
                Cost &amp; Value Breakdown — ${ag.name}
              </h2>
            </div>

            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="sc-tech-pill" style="border-color:${dept.color}55; color:${dept.color}; font-weight:700;">
                🧠 Orchestrator: Gemini 3.8 Flash ↔ 3.1 Pro / 4 Argon
              </span>
              <button type="button" class="sc-tech-pill" style="cursor:pointer; font-weight:700; background:var(--bg-elevated); color:var(--text-primary);" onclick="openCostTabPage('${ag.deptId}', '${ag.id}', true)">
                📊 Open Dynamic Cost Calculator &rarr;
              </button>
            </div>
          </div>

          <!-- Top 4 Simple KPI Cards: AI Cost vs Manual Estimate vs Savings vs Value -->
          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:14px; margin-bottom:16px;">
            <div style="padding:16px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-top:3px solid ${dept.color};">
              <div style="font-size:11.5px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                ✦ AI Agent Cost (Infra + Tokens)
              </div>
              <div style="font-family:var(--font-display); font-size:26px; font-weight:800; color:var(--text-primary); margin:6px 0 2px;">
                $${aiMo.toLocaleString()} <span style="font-size:14px; font-weight:600; color:var(--text-secondary);">/ mo</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-secondary);">
                $${mb.blendedCostPer1kCallsUsd.toFixed(2)} / 1K runs · Pilot: $${mb.pilotScaleMoUsd.toFixed(0)}/mo
              </div>
            </div>

            <div style="padding:16px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-top:3px solid #f43f5e;">
              <div style="font-size:11.5px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                ✕ Manual Effort Estimate
              </div>
              <div style="font-family:var(--font-display); font-size:26px; font-weight:800; color:var(--text-primary); margin:6px 0 2px;">
                $${mc.manualMonthlyCostUsd.toLocaleString()} <span style="font-size:14px; font-weight:600; color:var(--text-secondary);">/ mo</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-secondary);">
                ~${mc.fteEquivalent} FTEs (${mc.manualHoursPerMonth} hrs/mo + error rework)
              </div>
            </div>

            <div style="padding:16px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-top:3px solid #38bdf8;">
              <div style="font-size:11.5px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                ⚡ Direct Process Savings
              </div>
              <div style="font-family:var(--font-display); font-size:26px; font-weight:800; color:#38bdf8; margin:6px 0 2px;">
                ${mc.directSavingsPct}% <span style="font-size:14px; font-weight:600; color:var(--text-secondary);">Less</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-secondary);">
                Saves $${mc.directMonthlySavingsUsd.toLocaleString()}/mo vs. manual process
              </div>
            </div>

            <div style="padding:16px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-top:3px solid #10b981;">
              <div style="font-size:11.5px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                🚀 Supply Chain Value Unlocked
              </div>
              <div style="font-family:var(--font-display); font-size:26px; font-weight:800; color:#10b981; margin:6px 0 2px;">
                $${(vm.grossAnnualConservativeUsd / 1e6).toFixed(2)}M <span style="font-size:14px; font-weight:600; color:var(--text-secondary);">/ yr</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-secondary);">
                $${(valMo / 1000).toFixed(1)}K/mo business impact (${vm.cloudRoiMultipleConservative}x ROI)
              </div>
            </div>
          </div>

          <!-- Visual Infographic Breakdown Row (2 Simple Cards: Visual Bars + Infra Split) -->
          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:14px;">
            <!-- Left: Visual Cost vs Manual vs Value Comparison -->
            <div style="padding:14px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle);">
              <div style="font-size:11.5px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em; margin-bottom:10px;">
                Monthly Cost vs. Manual &amp; Value Comparison
              </div>

              <div style="margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between; font-size:12.5px; margin-bottom:3px;">
                  <span style="color:var(--text-secondary); font-weight:600;">✦ AI Agent (Infra + Tokens)</span>
                  <span style="color:var(--text-primary); font-weight:800;">$${aiMo.toLocaleString()} / mo</span>
                </div>
                <div style="height:7px; border-radius:999px; background:var(--border-subtle); overflow:hidden;">
                  <div style="width:4%; min-width:8px; height:100%; background:${dept.color}; border-radius:999px;"></div>
                </div>
              </div>

              <div style="margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between; font-size:12.5px; margin-bottom:3px;">
                  <span style="color:var(--text-secondary); font-weight:600;">✕ Manual Analyst &amp; Rework</span>
                  <span style="color:#f43f5e; font-weight:800;">$${mc.manualMonthlyCostUsd.toLocaleString()} / mo</span>
                </div>
                <div style="height:7px; border-radius:999px; background:var(--border-subtle); overflow:hidden;">
                  <div style="width:36%; height:100%; background:#f43f5e; border-radius:999px;"></div>
                </div>
              </div>

              <div>
                <div style="display:flex; justify-content:space-between; font-size:12.5px; margin-bottom:3px;">
                  <span style="color:var(--text-secondary); font-weight:600;">🚀 Supply Chain Value Created</span>
                  <span style="color:#10b981; font-weight:800;">$${valMo.toLocaleString()} / mo</span>
                </div>
                <div style="height:7px; border-radius:999px; background:var(--border-subtle); overflow:hidden;">
                  <div style="width:100%; height:100%; background:#10b981; border-radius:999px;"></div>
                </div>
              </div>
            </div>

            <!-- Right: Visual Monthly Infra & Token Breakdown -->
            <div style="padding:14px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); display:flex; flex-direction:column; justify-content:space-between;">
              <div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                  <span style="font-size:11.5px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                    Inside the $${aiMo}/mo AI Cost (Excl. Seats)
                  </span>
                  <span style="font-size:12px; font-weight:700; color:var(--text-secondary);">
                    ~${cm.eventsPerDay.toLocaleString()} runs/day
                  </span>
                </div>

                <!-- 3-Segment Stacked Bar -->
                <div style="height:10px; border-radius:999px; background:var(--border-subtle); overflow:hidden; display:flex; gap:2px; margin-bottom:12px;">
                  <div style="width:${llmPct}%; height:100%; background:#10b981;" title="LLM Tokens: $${llmMo}/mo"></div>
                  <div style="width:${compPct}%; height:100%; background:#38bdf8;" title="ADK Runtime: $${compMo}/mo"></div>
                  <div style="width:${dataPct}%; height:100%; background:#a855f7;" title="BigQuery & APIs: $${dataMo}/mo"></div>
                </div>
              </div>

              <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:8px;">
                <div style="padding:8px 10px; border-radius:10px; background:var(--bg-surface); border:1px solid var(--border-subtle);">
                  <div style="font-size:11px; color:var(--text-secondary); font-weight:600;">🟢 LLM Tokens</div>
                  <div style="font-size:15px; font-weight:800; color:var(--text-primary); margin-top:2px;">$${llmMo}/mo <span style="font-size:11px; color:var(--text-secondary); font-weight:600;">(${llmPct}%)</span></div>
                </div>
                <div style="padding:8px 10px; border-radius:10px; background:var(--bg-surface); border:1px solid var(--border-subtle);">
                  <div style="font-size:11px; color:var(--text-secondary); font-weight:600;">🔵 ADK Runtime</div>
                  <div style="font-size:15px; font-weight:800; color:var(--text-primary); margin-top:2px;">$${compMo}/mo <span style="font-size:11px; color:var(--text-secondary); font-weight:600;">(${compPct}%)</span></div>
                </div>
                <div style="padding:8px 10px; border-radius:10px; background:var(--bg-surface); border:1px solid var(--border-subtle);">
                  <div style="font-size:11px; color:var(--text-secondary); font-weight:600;">🟣 BQ &amp; APIs</div>
                  <div style="font-size:15px; font-weight:800; color:var(--text-primary); margin-top:2px;">$${dataMo}/mo <span style="font-size:11px; color:var(--text-secondary); font-weight:600;">(${dataPct}%)</span></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    }"""


COST_TAB_PAGE_JS = r"""
    /* =========================================================================
       PAGE 9: DEDICATED COST & ROI TAB (#pageCost / #cost)
       SAME WEBSITE DESIGN LANGUAGE · VISUAL INFOGRAPHIC · DYNAMIC CALCULATOR
       ========================================================================= */
    let currentCostTabPillar = 'all';
    let currentCostTabSearch = '';

    function openCostTabPage(pillarFilter = 'all', highlightAgentId = null, pushState = true) {
      currentCostTabPillar = pillarFilter || 'all';
      if (pushState) {
        history.pushState({ page: 'cost', pillar: currentCostTabPillar }, '', '#cost');
      }

      const container = document.getElementById('costPageContent');
      if (!container) return;

      const allAgents = Object.values(AGENTS);
      // Compute bottom-up defaults across all 60 agents
      let totalAiMo = 0;
      let totalLlmMo = 0;
      let totalCompMo = 0;
      let totalDataMo = 0;
      let totalManualMo = 0;
      let totalFtes = 0;
      let totalValYr = 0;
      let totalCallsMo = 0;

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
        totalCallsMo += (cm.monthlyCalls || 85000);
      });

      // Pillar rollups
      const pillarCardsHtml = DEPARTMENTS.map(dept => {
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
        const isSelected = currentCostTabPillar === dept.id;

        return `
          <div onclick="filterCostTabByPillar('${dept.id}')" style="cursor:pointer; padding:16px 18px; border-radius:16px; background:var(--bg-elevated); border:2px solid ${isSelected ? dept.color : 'var(--border-subtle)'}; transition:all 0.18s ease;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
              <span style="font-size:11.5px; font-weight:800; color:${dept.color}; text-transform:uppercase; letter-spacing:0.06em;">
                ${dept.shortTitle || dept.title}
              </span>
              <span class="sc-tech-pill" style="padding:2px 8px; font-size:11px; font-weight:700;">
                ${pAgents.length} Agents
              </span>
            </div>

            <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:8px; margin-bottom:10px;">
              <div>
                <div style="font-size:10.5px; color:var(--text-secondary); font-weight:600;">✦ AI Cost</div>
                <div style="font-family:var(--font-display); font-size:17px; font-weight:800; color:var(--text-primary);">$${Math.round(pAiMo).toLocaleString()}<span style="font-size:11px; font-weight:500; color:var(--text-secondary);">/mo</span></div>
              </div>
              <div>
                <div style="font-size:10.5px; color:var(--text-secondary); font-weight:600;">✕ Manual Est.</div>
                <div style="font-family:var(--font-display); font-size:17px; font-weight:800; color:#f43f5e;">$${Math.round(pManMo / 1000)}K<span style="font-size:11px; font-weight:500; color:var(--text-secondary);">/mo</span></div>
              </div>
              <div>
                <div style="font-size:10.5px; color:var(--text-secondary); font-weight:600;">🚀 Value</div>
                <div style="font-family:var(--font-display); font-size:17px; font-weight:800; color:#10b981;">$${(pValYr / 1e6).toFixed(1)}M<span style="font-size:11px; font-weight:500; color:var(--text-secondary);">/yr</span></div>
              </div>
            </div>

            <div style="height:6px; border-radius:999px; background:var(--border-subtle); overflow:hidden; display:flex; gap:2px; margin-bottom:6px;">
              <div style="width:${lPct}%; height:100%; background:#10b981;"></div>
              <div style="width:${cPct}%; height:100%; background:#38bdf8;"></div>
              <div style="width:${dPct}%; height:100%; background:#a855f7;"></div>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:11px; color:var(--text-secondary);">
              <span>Tokens $${Math.round(pLlm)} · Compute $${Math.round(pComp)} · BQ $${Math.round(pData)}</span>
              <span style="color:${dept.color}; font-weight:700;">~${pFte.toFixed(0)} FTEs saved</span>
            </div>
          </div>
        `;
      }).join('');

      container.innerHTML = `
        <!-- Top Subpage Bar -->
        <div class="subpage-topbar" style="margin-bottom: 20px;">
          <button type="button" class="back-btn" onclick="goHome()">
            <span>&larr;</span>
            <span>Back to Home</span>
          </button>

          <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
            <span class="sc-tech-pill" style="font-weight:700; color:var(--g-blue); border-color:rgba(37,99,235,0.35);">
              🧠 Orchestrator: Gemini 3.8 Flash ↔ 3.1 Pro / 4 Argon (subject to availability)
            </span>
            <span class="sc-tech-pill" style="font-weight:700;">
              Infra, Invocation &amp; Token Cost Only (Excl. Seats)
            </span>
          </div>
        </div>

        <!-- Clean Header -->
        <div class="simple-arch-card" style="margin-bottom: 20px;">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:14px; margin-bottom:18px;">
            <div>
              <div style="font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:var(--g-blue); margin-bottom:4px;">
                Cloud FinOps, Manual Effort Comparison &amp; ROI Simulator
              </div>
              <h1 style="font-family:var(--font-display); font-size:28px; font-weight:800; color:var(--text-primary); margin:0;">
                AI Agent Cost vs. Manual Effort &amp; Dynamic Scale Calculator
              </h1>
            </div>
          </div>

          <!-- 4 Simple Top KPI Cards -->
          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap:14px;">
            <div style="padding:16px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-top:3px solid var(--g-blue);">
              <div style="font-size:11.5px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                ✦ 60-Agent AI Cost (Infra + Tokens)
              </div>
              <div style="font-family:var(--font-display); font-size:28px; font-weight:800; color:var(--text-primary); margin:6px 0 2px;">
                $${Math.round(totalAiMo).toLocaleString()} <span style="font-size:14px; font-weight:600; color:var(--text-secondary);">/ mo</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-secondary);">
                $${Math.round(totalAiMo * 12).toLocaleString()} / yr (3-Yr FSP · ~${(totalCallsMo / 1e6).toFixed(1)}M runs/mo)
              </div>
            </div>

            <div style="padding:16px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-top:3px solid #f43f5e;">
              <div style="font-size:11.5px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                ✕ Manual Process Estimate
              </div>
              <div style="font-family:var(--font-display); font-size:28px; font-weight:800; color:var(--text-primary); margin:6px 0 2px;">
                $${(totalManualMo / 1e6).toFixed(2)}M <span style="font-size:14px; font-weight:600; color:var(--text-secondary);">/ mo</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-secondary);">
                $${((totalManualMo * 12) / 1e6).toFixed(1)}M / yr (~${Math.round(totalFtes)} FTEs manual triage &amp; rework)
              </div>
            </div>

            <div style="padding:16px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-top:3px solid #38bdf8;">
              <div style="font-size:11.5px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                ⚡ Direct Process Cost Reduction
              </div>
              <div style="font-family:var(--font-display); font-size:28px; font-weight:800; color:#38bdf8; margin:6px 0 2px;">
                99.1% <span style="font-size:14px; font-weight:600; color:var(--text-secondary);">Less</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-secondary);">
                ~$214/mo avg per AI agent vs. ~$23.5K/mo manual
              </div>
            </div>

            <div style="padding:16px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-top:3px solid #10b981;">
              <div style="font-size:11.5px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                🚀 Supply Chain Business Value
              </div>
              <div style="font-family:var(--font-display); font-size:28px; font-weight:800; color:#10b981; margin:6px 0 2px;">
                $${(totalValYr / 1e6).toFixed(1)}M <span style="font-size:14px; font-weight:600; color:var(--text-secondary);">/ yr</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-secondary);">
                $${(totalValYr / 12 / 1e6).toFixed(2)}M / mo inventory, OEE &amp; freight value
              </div>
            </div>
          </div>
        </div>

        <!-- Section 2: Interactive Dynamic Cost & Value Calculator + Visual Infographic Breakdown -->
        <div class="simple-arch-card" style="margin-bottom: 20px;">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
            <div>
              <div style="font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:#10b981; margin-bottom:3px;">
                Interactive Sizer &amp; Infographic Breakdown
              </div>
              <h2 style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary); margin:0;">
                Dynamic Scale Calculator (Infra + Invocation + Token Cost)
              </h2>
            </div>

            <!-- 4 Quick Scale Preset Pills -->
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              <button type="button" class="sc-tech-pill" style="cursor:pointer; font-weight:700;" onclick="applyWebCostPreset(10, 250000, 88, 75, 20)">
                1. Pilot (10 Agents)
              </button>
              <button type="button" class="sc-tech-pill" style="cursor:pointer; font-weight:700;" onclick="applyWebCostPreset(30, 1500000, 85, 75, 20)">
                2. Regional (30 Agents)
              </button>
              <button type="button" class="sc-tech-pill" style="cursor:pointer; font-weight:700; border-color:var(--g-blue); color:var(--g-blue);" onclick="applyWebCostPreset(60, 5200000, 85, 75, 20)">
                3. Enterprise (All 60)
              </button>
              <button type="button" class="sc-tech-pill" style="cursor:pointer; font-weight:700;" onclick="applyWebCostPreset(60, 20000000, 85, 80, 20)">
                4. Hyperscale (20M Runs)
              </button>
            </div>
          </div>

          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap:20px;">
            <!-- Left: 5 Simple Sliders -->
            <div style="padding:18px; border-radius:16px; background:var(--bg-elevated); border:1px solid var(--border-subtle); display:flex; flex-direction:column; gap:14px;">
              <div>
                <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; margin-bottom:5px;">
                  <span style="color:var(--text-primary);">1. Active AI Agents Deployed</span>
                  <span id="wCalcLblAgents" style="color:var(--g-blue);">60 Agents</span>
                </div>
                <input type="range" id="wCalcRngAgents" min="1" max="60" step="1" value="60" style="width:100%; accent-color:var(--g-blue); cursor:pointer;" oninput="updateWebCostCalculator()" />
              </div>

              <div>
                <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; margin-bottom:5px;">
                  <span style="color:var(--text-primary);">2. Monthly Invocations (Chat + ERP/IoT)</span>
                  <span id="wCalcLblCalls" style="color:var(--g-blue);">5,200,000 / mo</span>
                </div>
                <input type="range" id="wCalcRngCalls" min="50000" max="25000000" step="50000" value="5200000" style="width:100%; accent-color:var(--g-blue); cursor:pointer;" oninput="updateWebCostCalculator()" />
              </div>

              <div>
                <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; margin-bottom:5px;">
                  <span style="color:var(--text-primary);">3. Orchestrator Routing (3.8 Flash vs. 3.1 Pro/4 Argon)</span>
                  <span id="wCalcLblFlash" style="color:#10b981;">85% Flash / 15% Pro·Argon</span>
                </div>
                <input type="range" id="wCalcRngFlash" min="50" max="95" step="5" value="85" style="width:100%; accent-color:#10b981; cursor:pointer;" oninput="updateWebCostCalculator()" />
              </div>

              <div>
                <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; margin-bottom:5px;">
                  <span style="color:var(--text-primary);">4. Context Caching Hit Rate</span>
                  <span id="wCalcLblCache" style="color:#a855f7;">75% Cache Hit</span>
                </div>
                <input type="range" id="wCalcRngCache" min="0" max="90" step="5" value="75" style="width:100%; accent-color:#a855f7; cursor:pointer;" oninput="updateWebCostCalculator()" />
              </div>

              <div>
                <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700; margin-bottom:5px;">
                  <span style="color:var(--text-primary);">5. Vertex AI Commit Discount (FSP)</span>
                  <span id="wCalcLblFsp" style="color:#f59e0b;">3-Yr FSP (-20%)</span>
                </div>
                <select id="wCalcSelFsp" onchange="updateWebCostCalculator()" style="width:100%; padding:9px 12px; border-radius:10px; background:var(--bg-surface); color:var(--text-primary); border:1px solid var(--border-subtle); font-weight:600; font-size:13px; cursor:pointer;">
                  <option value="0">Pay-As-You-Go (0% Discount)</option>
                  <option value="10">1-Year Vertex AI FSP (-10% Token Discount)</option>
                  <option value="20" selected>3-Year Vertex AI FSP (-20% Token Discount)</option>
                </select>
              </div>
            </div>

            <!-- Right: Live Visual Infographic Breakdown -->
            <div style="padding:18px; border-radius:16px; background:var(--bg-elevated); border:1px solid var(--border-subtle); display:flex; flex-direction:column; justify-content:space-between; gap:16px;">
              <!-- Live Top Numbers -->
              <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:10px;">
                <div style="padding:12px 14px; border-radius:12px; background:var(--bg-surface); border:1px solid var(--border-subtle); border-left:3px solid var(--g-blue);">
                  <div style="font-size:11px; font-weight:700; color:var(--text-secondary); text-transform:uppercase;">✦ AI Cost / Mo</div>
                  <div id="wCalcOutAiMo" style="font-family:var(--font-display); font-size:22px; font-weight:800; color:var(--text-primary); margin-top:2px;">$12,843</div>
                  <div id="wCalcOutPer1k" style="font-size:11.5px; color:var(--text-secondary);">$2.47 / 1K runs</div>
                </div>
                <div style="padding:12px 14px; border-radius:12px; background:var(--bg-surface); border:1px solid var(--border-subtle); border-left:3px solid #f43f5e;">
                  <div style="font-size:11px; font-weight:700; color:var(--text-secondary); text-transform:uppercase;">✕ Manual Est. / Mo</div>
                  <div id="wCalcOutManMo" style="font-family:var(--font-display); font-size:22px; font-weight:800; color:#f43f5e; margin-top:2px;">$1.41M</div>
                  <div id="wCalcOutFtes" style="font-size:11.5px; color:var(--text-secondary);">~124 FTEs manual</div>
                </div>
                <div style="padding:12px 14px; border-radius:12px; background:var(--bg-surface); border:1px solid var(--border-subtle); border-left:3px solid #10b981;">
                  <div style="font-size:11px; font-weight:700; color:var(--text-secondary); text-transform:uppercase;">🚀 Value / Yr</div>
                  <div id="wCalcOutValYr" style="font-family:var(--font-display); font-size:22px; font-weight:800; color:#10b981; margin-top:2px;">$66.6M</div>
                  <div id="wCalcOutRoi" style="font-size:11.5px; color:var(--text-secondary);">432x Cloud ROI</div>
                </div>
              </div>

              <!-- Visual Bar Comparison: AI Cost vs Manual vs Value -->
              <div style="padding:12px 14px; border-radius:12px; background:var(--bg-surface); border:1px solid var(--border-subtle);">
                <div style="font-size:11px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">
                  Visual Scale Comparison (Monthly)
                </div>
                <div style="margin-bottom:7px;">
                  <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:2px;">
                    <span style="color:var(--text-secondary); font-weight:600;">✦ AI Infra + Token Cost</span>
                    <span id="wCalcBarAiLbl" style="color:var(--text-primary); font-weight:800;">$12,843 / mo</span>
                  </div>
                  <div style="height:7px; border-radius:999px; background:var(--border-subtle); overflow:hidden;">
                    <div id="wCalcBarAiFill" style="width:3%; min-width:8px; height:100%; background:var(--g-blue); border-radius:999px;"></div>
                  </div>
                </div>
                <div style="margin-bottom:7px;">
                  <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:2px;">
                    <span style="color:var(--text-secondary); font-weight:600;">✕ Manual Effort Equivalent</span>
                    <span id="wCalcBarManLbl" style="color:#f43f5e; font-weight:800;">$1,410,000 / mo (Saves 99.1%)</span>
                  </div>
                  <div style="height:7px; border-radius:999px; background:var(--border-subtle); overflow:hidden;">
                    <div id="wCalcBarManFill" style="width:32%; height:100%; background:#f43f5e; border-radius:999px;"></div>
                  </div>
                </div>
                <div>
                  <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:2px;">
                    <span style="color:var(--text-secondary); font-weight:600;">🚀 Supply Chain Value Unlocked</span>
                    <span id="wCalcBarValLbl" style="color:#10b981; font-weight:800;">$5,550,000 / mo</span>
                  </div>
                  <div style="height:7px; border-radius:999px; background:var(--border-subtle); overflow:hidden;">
                    <div style="width:100%; height:100%; background:#10b981; border-radius:999px;"></div>
                  </div>
                </div>
              </div>

              <!-- 3-Bucket Infra & Token Breakdown -->
              <div style="padding:12px 14px; border-radius:12px; background:var(--bg-surface); border:1px solid var(--border-subtle);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                  <span style="font-size:11px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                    Monthly AI Cost Split (Tokens · ADK Compute · BigQuery/APIs)
                  </span>
                  <span id="wCalcAnnualAiLbl" style="font-size:11.5px; font-weight:700; color:var(--text-secondary);">$154.1K / yr</span>
                </div>
                <div style="height:9px; border-radius:999px; background:var(--border-subtle); overflow:hidden; display:flex; gap:2px; margin-bottom:10px;">
                  <div id="wCalcSplitLlmBar" style="width:38%; height:100%; background:#10b981;"></div>
                  <div id="wCalcSplitCompBar" style="width:34%; height:100%; background:#38bdf8;"></div>
                  <div id="wCalcSplitDataBar" style="width:28%; height:100%; background:#a855f7;"></div>
                </div>
                <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:8px; font-size:12px;">
                  <div>
                    <span style="color:var(--text-secondary);">🟢 LLM Tokens:</span>
                    <strong id="wCalcSplitLlmVal" style="color:var(--text-primary); margin-left:4px;">$4,880/mo</strong>
                  </div>
                  <div>
                    <span style="color:var(--text-secondary);">🔵 ADK Compute:</span>
                    <strong id="wCalcSplitCompVal" style="color:var(--text-primary); margin-left:4px;">$4,360/mo</strong>
                  </div>
                  <div>
                    <span style="color:var(--text-secondary);">🟣 BQ &amp; APIs:</span>
                    <strong id="wCalcSplitDataVal" style="color:var(--text-primary); margin-left:4px;">$3,603/mo</strong>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Section 3: 6-Pillar Visual Infographic Breakdown -->
        <div class="simple-arch-card" style="margin-bottom: 20px;">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:14px;">
            <div>
              <div style="font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:var(--text-secondary);">
                6-Pillar Cost vs. Manual Effort Breakdown
              </div>
              <h2 style="font-family:var(--font-display); font-size:20px; font-weight:800; color:var(--text-primary); margin:2px 0 0;">
                Click Any Pillar to Filter the 60 Agents Below
              </h2>
            </div>
            <button type="button" class="sc-tech-pill" style="cursor:pointer; font-weight:700;" onclick="filterCostTabByPillar('all')">
              Show All 60 Agents
            </button>
          </div>

          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(270px, 1fr)); gap:12px;">
            ${pillarCardsHtml}
          </div>
        </div>

        <!-- Section 4: All 60 Agents Simple Cost vs. Manual Estimate Table -->
        <div class="simple-arch-card">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:14px;">
            <div>
              <div style="font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:var(--g-blue);">
                Agent-by-Agent Unit Economics (All 60 Categorized Agents)
              </div>
              <h2 style="font-family:var(--font-display); font-size:20px; font-weight:800; color:var(--text-primary); margin:2px 0 0;">
                Individual Agent AI Cost vs. Manual Estimate &amp; Value
              </h2>
            </div>

            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
              <input type="text" id="costTabSearchInput" placeholder="Search agent or persona..." value="${currentCostTabSearch}" oninput="onCostTabSearchInput(this.value)" style="padding:8px 14px; border-radius:10px; background:var(--bg-elevated); color:var(--text-primary); border:1px solid var(--border-subtle); font-size:13px; min-width:220px;" />
              <span id="costTabAgentCountBadge" class="sc-tech-pill" style="font-weight:700;">60 Agents</span>
            </div>
          </div>

          <div style="overflow-x:auto;">
            <table style="width:100%; border-collapse:collapse; font-size:13px;">
              <thead>
                <tr style="border-bottom:2px solid var(--border-subtle); text-align:left; color:var(--text-secondary); font-size:11.5px; text-transform:uppercase; letter-spacing:0.05em;">
                  <th style="padding:10px 12px;">Agent &amp; Category</th>
                  <th style="padding:10px 12px;">Orchestrator Routing</th>
                  <th style="padding:10px 12px; text-align:right;">Cost / 1K Runs</th>
                  <th style="padding:10px 12px; text-align:right;">✦ AI Cost / Mo</th>
                  <th style="padding:10px 12px; text-align:right;">✕ Manual Est. / Mo</th>
                  <th style="padding:10px 12px; text-align:right;">Savings</th>
                  <th style="padding:10px 12px; text-align:right;">🚀 Annual Value</th>
                </tr>
              </thead>
              <tbody id="costTabAgentsTbody"></tbody>
            </table>
          </div>
        </div>
      `;

      showActivePage('pageCost');
      updateWebCostCalculator();
      renderCostTabAgentRows(highlightAgentId);
    }

    function applyWebCostPreset(agents, calls, flashPct, cachePct, fspVal) {
      const elA = document.getElementById('wCalcRngAgents');
      const elC = document.getElementById('wCalcRngCalls');
      const elF = document.getElementById('wCalcRngFlash');
      const elH = document.getElementById('wCalcRngCache');
      const elS = document.getElementById('wCalcSelFsp');
      if (!elA) return;
      elA.value = agents;
      elC.value = calls;
      elF.value = flashPct;
      elH.value = cachePct;
      elS.value = String(fspVal);
      updateWebCostCalculator();
    }

    function updateWebCostCalculator() {
      const elA = document.getElementById('wCalcRngAgents');
      if (!elA) return;
      const agents = parseInt(elA.value, 10) || 60;
      const calls = parseInt(document.getElementById('wCalcRngCalls').value, 10) || 5200000;
      const flashPct = parseInt(document.getElementById('wCalcRngFlash').value, 10) || 85;
      const cachePct = parseInt(document.getElementById('wCalcRngCache').value, 10) || 75;
      const fspDiscount = parseInt(document.getElementById('wCalcSelFsp').value, 10) || 20;
      const proPct = 100 - flashPct;

      document.getElementById('wCalcLblAgents').textContent = `${agents} Agent${agents > 1 ? 's' : ''}`;
      document.getElementById('wCalcLblCalls').textContent = `${calls.toLocaleString()} / mo`;
      document.getElementById('wCalcLblFlash').textContent = `${flashPct}% Flash / ${proPct}% Pro·Argon`;
      document.getElementById('wCalcLblCache').textContent = `${cachePct}% Cache Hit`;
      document.getElementById('wCalcLblFsp').textContent = fspDiscount === 0 ? 'PayGo (0%)' : `${fspDiscount === 10 ? '1-Yr' : '3-Yr'} FSP (-${fspDiscount}%)`;

      // Token cost math (Dynamic Orchestrator: Gemini 3.8 Flash + 3.1 Pro / 4 Argon)
      const cacheFactor = 1 - (cachePct / 100) * 0.56;
      const fspFactor = 1 - (fspDiscount / 100);
      const flashRatePerCall = 0.00055 * cacheFactor * fspFactor;
      const proRatePerCall = 0.0085 * cacheFactor * fspFactor;

      const llmMo = Math.round(calls * (flashPct / 100) * flashRatePerCall + calls * (proPct / 100) * proRatePerCall);
      const compMo = Math.round(agents * 58 + (calls / 1000000) * 240);
      const dataMo = Math.round(agents * 44 + (calls / 1000000) * 190);
      const aiMo = Math.max(45, llmMo + compMo + dataMo);
      const aiYr = aiMo * 12;
      const per1k = calls > 0 ? (aiMo / (calls / 1000)) : 0;

      // Manual equivalent scales with active agents & volume
      const ftes = (agents * 2.05 * Math.min(1.35, Math.pow(calls / 5200000, 0.15)));
      const manualMo = Math.round(agents * 23500 * Math.min(1.35, Math.pow(calls / 5200000, 0.15)));
      const savingsPct = manualMo > 0 ? Math.max(85, ((manualMo - aiMo) / manualMo) * 100).toFixed(1) : '99.0';

      // Annual business value unlocked
      const valYrM = (agents / 60) * 66.6 * Math.min(1.5, Math.pow(calls / 5200000, 0.22));
      const valMo = Math.round((valYrM * 1e6) / 12);
      const roiMult = aiYr > 0 ? Math.round((valYrM * 1e6) / aiYr) : 0;

      document.getElementById('wCalcOutAiMo').textContent = `$${aiMo.toLocaleString()}`;
      document.getElementById('wCalcOutPer1k').textContent = `$${per1k.toFixed(2)} / 1K runs`;
      document.getElementById('wCalcOutManMo').textContent = manualMo >= 1000000 ? `$${(manualMo / 1e6).toFixed(2)}M` : `$${(manualMo / 1000).toFixed(0)}K`;
      document.getElementById('wCalcOutFtes').textContent = `~${Math.round(ftes)} FTEs manual`;
      document.getElementById('wCalcOutValYr').textContent = `$${valYrM.toFixed(1)}M`;
      document.getElementById('wCalcOutRoi').textContent = `${roiMult}x Cloud ROI`;

      document.getElementById('wCalcBarAiLbl').textContent = `$${aiMo.toLocaleString()} / mo`;
      document.getElementById('wCalcBarManLbl').textContent = `$${manualMo.toLocaleString()} / mo (Saves ${savingsPct}%)`;
      document.getElementById('wCalcBarValLbl').textContent = `$${valMo.toLocaleString()} / mo ($${valYrM.toFixed(1)}M/yr)`;

      const lPct = Math.round((llmMo / aiMo) * 100);
      const cPct = Math.round((compMo / aiMo) * 100);
      const dPct = Math.max(1, 100 - lPct - cPct);
      document.getElementById('wCalcAnnualAiLbl').textContent = `$${aiYr.toLocaleString()} / yr`;
      document.getElementById('wCalcSplitLlmBar').style.width = `${lPct}%`;
      document.getElementById('wCalcSplitCompBar').style.width = `${cPct}%`;
      document.getElementById('wCalcSplitDataBar').style.width = `${dPct}%`;
      document.getElementById('wCalcSplitLlmVal').textContent = `$${llmMo.toLocaleString()}/mo (${lPct}%)`;
      document.getElementById('wCalcSplitCompVal').textContent = `$${compMo.toLocaleString()}/mo (${cPct}%)`;
      document.getElementById('wCalcSplitDataVal').textContent = `$${dataMo.toLocaleString()}/mo (${dPct}%)`;
    }

    function filterCostTabByPillar(pillarId) {
      currentCostTabPillar = pillarId || 'all';
      openCostTabPage(currentCostTabPillar, null, false);
    }

    function onCostTabSearchInput(val) {
      currentCostTabSearch = val || '';
      renderCostTabAgentRows(null);
    }

    function renderCostTabAgentRows(highlightAgentId = null) {
      const tbody = document.getElementById('costTabAgentsTbody');
      if (!tbody) return;
      const q = (currentCostTabSearch || '').trim().toLowerCase();
      const list = Object.values(AGENTS).filter(ag => {
        if (currentCostTabPillar !== 'all' && ag.deptId !== currentCostTabPillar) return false;
        if (!q) return true;
        return (
          (ag.name || '').toLowerCase().includes(q) ||
          (ag.categoryDisplayName || '').toLowerCase().includes(q) ||
          (ag.owner || '').toLowerCase().includes(q)
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
        const isHl = highlightAgentId && ag.id === highlightAgentId;
        const isPro = (cm.modelSlug || '').includes('pro');

        return `
          <tr onclick="openAgentPage('${ag.id}', true, event)" style="cursor:pointer; border-bottom:1px solid var(--border-subtle); background:${isHl ? 'var(--bg-elevated)' : 'transparent'}; transition:background 0.15s ease;" onmouseover="this.style.background='var(--bg-elevated)'" onmouseout="this.style.background='${isHl ? 'var(--bg-elevated)' : 'transparent'}'">
            <td style="padding:12px;">
              <div style="font-weight:800; color:var(--text-primary); font-size:13.5px;">${ag.name}</div>
              <div style="font-size:11.5px; color:${dept.color}; font-weight:700;">${dept.shortTitle || dept.title} · ${ag.owner || ''}</div>
            </td>
            <td style="padding:12px;">
              <span class="sc-tech-pill" style="font-size:11px; padding:3px 8px; border-color:${isPro ? '#a855f755' : '#10b98155'}; color:${isPro ? '#a855f7' : '#10b981'}; font-weight:700;">
                ${isPro ? '3.1 Pro / 4 Argon + 3.8 Flash' : '3.8 Flash ↔ 3.1 Pro / 4 Argon'}
              </span>
            </td>
            <td style="padding:12px; text-align:right; font-family:var(--font-mono); font-weight:700; color:var(--text-primary);">
              $${(mb.blendedCostPer1kCallsUsd || 2.45).toFixed(2)}
            </td>
            <td style="padding:12px; text-align:right; font-family:var(--font-mono); font-weight:800; color:var(--g-blue); font-size:14px;">
              $${aiMo.toLocaleString()}/mo
            </td>
            <td style="padding:12px; text-align:right; font-family:var(--font-mono); font-weight:700; color:#f43f5e;">
              $${(mc.manualMonthlyCostUsd || 24000).toLocaleString()}/mo
              <div style="font-size:10.5px; color:var(--text-secondary); font-weight:500;">~${mc.fteEquivalent} FTEs</div>
            </td>
            <td style="padding:12px; text-align:right;">
              <span class="sc-tech-pill" style="font-size:11px; padding:2px 8px; color:#38bdf8; border-color:#38bdf855; font-weight:800;">
                -${mc.directSavingsPct}%
              </span>
            </td>
            <td style="padding:12px; text-align:right; font-family:var(--font-mono); font-weight:800; color:#10b981;">
              $${((vm.grossAnnualConservativeUsd || 1100000) / 1e6).toFixed(2)}M/yr
            </td>
          </tr>
        `;
      }).join('');
    }
"""


def update_website_files(catalog: dict) -> None:
    agents_json = json.dumps(catalog["agents"], indent=2)

    for fname in ["index.html", "periodic_table.html", "mind_map.html"]:
        p = ROOT / fname
        if not p.exists():
            continue
        html = p.read_text(encoding="utf-8")

        # 1. Sync `const AGENTS = ...;` with updated manualComparison & costModel
        agents_pat = re.compile(
            r"    const AGENTS = \{[\s\S]*?\n\};\n    Object\.defineProperty\(AGENTS,",
            re.M,
        )
        if agents_pat.search(html):
            html = agents_pat.sub(
                lambda _: f"    const AGENTS = {agents_json};\n    Object.defineProperty(AGENTS,",
                html,
                count=1,
            )

        # 2. Add "Cost & ROI" button to top navbar if not already present
        if 'onclick="openCostTabPage(' not in html:
            html = html.replace(
                '<button type="button" class="nav-pill-btn" onclick="openMindMapPage(\'all\', null, true)">Mind Map</button>',
                '<button type="button" class="nav-pill-btn" onclick="openMindMapPage(\'all\', null, true)">Mind Map</button>\n'
                '      <button type="button" class="nav-pill-btn" onclick="openCostTabPage(\'all\', null, true)">Cost &amp; ROI</button>',
            )

        # 3. Add `<main id="pageCost" class="page-view">` after `#pageMindMap` if not present
        if 'id="pageCost"' not in html:
            html = html.replace(
                '  <main id="pageMindMap" class="page-view">\n    <div id="mindMapPageContent" class="subpage-container"></div>\n  </main>',
                '  <main id="pageMindMap" class="page-view">\n    <div id="mindMapPageContent" class="subpage-container"></div>\n  </main>\n\n'
                '  <!-- =========================================================================\n'
                '       PAGE 9: INTERACTIVE COST & ROI CALCULATOR & MANUAL COMPARISON TAB\n'
                '       ========================================================================= -->\n'
                '  <main id="pageCost" class="page-view">\n    <div id="costPageContent" class="subpage-container"></div>\n  </main>',
            )

        # 4. Replace `renderAgentCostAndRoiPanel` with the new AI Cost vs Manual Estimate + Infographic panel
        panel_pat = re.compile(
            r"    /\* =========================================================================\n"
            r"       SIMPLE AGENT COST DETAILS CARD[\s\S]*?function renderAgentCostAndRoiPanel\(ag, dept\) \{[\s\S]*?\n    \}",
            re.M,
        )
        if panel_pat.search(html):
            html = panel_pat.sub(lambda _: SIMPLE_AGENT_COST_AND_MANUAL_PANEL_JS, html, count=1)

        # 5. Inject `openCostTabPage` and wire `#cost` in `handleUrlHash`
        if "function openCostTabPage(" not in html:
            html = html.replace(
                "    function showActivePage(pageId) {",
                COST_TAB_PAGE_JS.lstrip("\n") + "\n    function showActivePage(pageId) {",
                1,
            )
        else:
            existing_cost_pat = re.compile(
                r"    /\* =========================================================================\n"
                r"       PAGE 9: DEDICATED COST & ROI TAB[\s\S]*?function showActivePage\(pageId\) \{",
                re.M,
            )
            html = existing_cost_pat.sub(
                lambda _: COST_TAB_PAGE_JS.lstrip("\n") + "\n    function showActivePage(pageId) {",
                html,
                count=1,
            )

        if "hash === 'cost'" not in html:
            html = html.replace(
                "      if (hash === 'mindmap' || hash.startsWith('mindmap/')) {",
                "      if (hash === 'cost' || hash.startsWith('cost/')) {\n"
                "        const pId = hash.split('/')[1] || 'all';\n"
                "        openCostTabPage(pId, null, false);\n"
                "        return;\n"
                "      }\n"
                "      if (hash === 'mindmap' || hash.startsWith('mindmap/')) {",
            )

        p.write_text(html, encoding="utf-8")
        print(f"✅ Updated {fname} with AI vs. Manual Cost Infographic and native Cost & ROI Calculator Tab (#cost).")


def sync_all_copies() -> None:
    files_to_sync = [
        "index.html",
        "periodic_table.html",
        "mind_map.html",
        "cost_analysis_presentation.html",
    ]
    for target_dir_name in ["docs", "zipline_dist", "dist/itc_limited"]:
        tdir = ROOT / target_dir_name
        if not tdir.exists():
            continue
        for fname in files_to_sync:
            src = ROOT / fname
            dst = tdir / fname
            if src.exists() and dst.exists():
                shutil.copy2(src, dst)
        if (ROOT / "data" / "supply_chain_catalog.json").exists() and (tdir / "data" / "supply_chain_catalog.json").exists():
            shutil.copy2(ROOT / "data" / "supply_chain_catalog.json", tdir / "data" / "supply_chain_catalog.json")
    print("✅ Synced updated HTML and catalog files to docs/, zipline_dist/, and dist/itc_limited/.")


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_granular_agent_cost_models_and_ui.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "upgrade_all_models_and_evals_38flash_4argon.py")], check=True)
    catalog = json.loads((ROOT / "data" / "supply_chain_catalog.json").read_text(encoding="utf-8"))
    update_website_files(catalog)
    sync_all_copies()


if __name__ == "__main__":
    main()

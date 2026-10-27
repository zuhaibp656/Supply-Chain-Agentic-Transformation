#!/usr/bin/env python3
"""Injects granular per-agent Cloud Cost, Tokenomics & 3-Year ROI UI components
directly into:
1. index.html, periodic_table.html, mind_map.html:
   - Syncs `const AGENTS = ...;` with `.costModel` and `.finopsProfile` for all 60 agents
   - Adds `renderAgentCostAndRoiPanel(ag, dept)`, `updateSingleAgentCostCalc(agentId)`,
     and `setSingleAgentScalePreset(agentId, callsPerDay, fspDiscountPct)`
   - Injects a prominent Hero Cost & ROI Banner Strip + full Interactive Cost & ROI Panel
     into `openAgentPage` (#agent/<id>) and `openAgentBlueprintPage` (#blueprint/<id>)
   - Injects Cloud Cost & ROI badges onto Persona Page agent cards (#persona/<id>),
     Directory agent cards (#directory), Periodic Table tiles/inspector/inline card (#periodic),
     and Neural Mind Map Column 3 agent cards (#mindmap)
2. cost_analysis_presentation.html:
   - Synchronizes `ALL_60_AGENTS_COST` and Slide 7 table with exact bottom-up `costModel`
     metrics from `data/supply_chain_catalog.json` and adds direct links (`index.html#agent/<id>`)
     to open any agent's live showcase cost calculator.
3. agents/<id>/agents-cli-manifest.yaml:
   - Updates `finops_tier` with each agent's exact bottom-up monthly and per-1K cost.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "data" / "supply_chain_catalog.json"
HTML_FILES = [
    ROOT / "index.html",
    ROOT / "periodic_table.html",
    ROOT / "mind_map.html",
]

PILLAR_LABELS = {
    "demand_sop": "01 · Plan & Demand",
    "sourcing_procurement": "02 · Source",
    "manufacturing_prod": "03 · Make",
    "inventory_warehouse": "04 · Store",
    "logistics_fleet": "05 · Move",
    "circular_enable": "06 · Sustain",
}

AGENT_COST_UI_JS = r"""
    /* =========================================================================
       SINGLE-AGENT CLOUD COST, TOKENOMICS & 3-YEAR ROI SHOWCASE CALCULATOR
       ========================================================================= */
    function setSingleAgentScalePreset(agentId, dailyCalls, fspPct) {
      const sliderEl = document.getElementById(`agCostCallsSlider_${agentId}`);
      const fspEl = document.getElementById(`agCostFspSelect_${agentId}`);
      if (sliderEl) sliderEl.value = dailyCalls;
      if (fspEl && typeof fspPct === 'number') fspEl.value = String(fspPct);
      updateSingleAgentCostCalc(agentId);
    }

    function updateSingleAgentCostCalc(agentId) {
      const ag = AGENTS[agentId];
      if (!ag || !ag.costModel) return;
      const cm = ag.costModel;

      const sliderEl = document.getElementById(`agCostCallsSlider_${agentId}`);
      const fspEl = document.getElementById(`agCostFspSelect_${agentId}`);
      if (!sliderEl || !fspEl) return;

      const dailyCalls = parseInt(sliderEl.value, 10) || cm.eventsPerDay;
      const fspPct = parseInt(fspEl.value, 10) || 0;
      const monthlyCalls = dailyCalls * 30;
      const scaleRatio = monthlyCalls / Math.max(1, cm.monthlyCalls);
      const fspMult = 1 - (fspPct / 100.0);

      // 1. Gemini Token Inference Cost
      const llmMo = +(monthlyCalls * cm.tokens.tokenCostPerCallUsd * fspMult).toFixed(2);

      // 2. Agent Engine + Solver Compute Cost (base warm pool + dynamic vCPU/GiB hours)
      const dynamicComputeBase = Math.max(0, cm.compute.monthlyComputeUsd - cm.compute.baseWarmPoolUsd);
      const computeMo = +(cm.compute.baseWarmPoolUsd + dynamicComputeBase * scaleRatio).toFixed(2);

      // 3. BigQuery Digital Twin Scan & Storage Cost (fixed active storage + dynamic query scan)
      const fixedStorageCost = +(cm.data.activeStorageGb * 0.18).toFixed(2);
      const dynamicScanBase = Math.max(8, cm.data.monthlyDataUsd - fixedStorageCost);
      const dataMo = +(fixedStorageCost + dynamicScanBase * scaleRatio).toFixed(2);

      // 4. External API & Enterprise Connector Cost
      const apiMo = +(cm.api.monthlyApiUsd * scaleRatio).toFixed(2);

      const totalMo = +(llmMo + computeMo + dataMo + apiMo).toFixed(2);
      const totalYr = +(totalMo * 12).toFixed(2);
      const maintYr = +(totalYr * 0.15).toFixed(2);
      const totalRunYr = +(totalYr + maintYr).toFixed(2);
      const unit1k = monthlyCalls > 0 ? +((totalMo / monthlyCalls) * 1000).toFixed(2) : 0;

      // Value scales sub-linearly with coverage volume
      const valScale = Math.min(2.2, Math.max(0.35, Math.pow(scaleRatio, 0.35)));
      const consValYr = Math.round(cm.valueModel.grossAnnualConservativeUsd * valScale);
      const likeValYr = Math.round(cm.valueModel.grossAnnualLikelyUsd * valScale);
      const roiCons = Math.max(1, Math.round(consValYr / Math.max(1, totalYr)));
      const roiLike = Math.max(1, Math.round(likeValYr / Math.max(1, totalYr)));
      const paybackDays = Math.max(1, Math.round((totalRunYr / Math.max(1, consValYr)) * 365));

      const setTxt = (id, txt) => {
        const el = document.getElementById(id);
        if (el) el.textContent = txt;
      };

      setTxt(`agCallsLbl_${agentId}`, `${dailyCalls.toLocaleString()} calls/day (${monthlyCalls.toLocaleString()}/mo)`);
      setTxt(`agLiveMoCost_${agentId}`, `$${totalMo.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})} / mo`);
      setTxt(`agLiveYrCost_${agentId}`, `$${Math.round(totalYr).toLocaleString()} / yr Cloud ($${Math.round(totalRunYr).toLocaleString()}/yr incl. 15% Ops)`);
      setTxt(`agLiveUnit1k_${agentId}`, `$${unit1k.toFixed(2)} / 1K calls`);
      setTxt(`agLiveRoiMult_${agentId}`, `${roiCons}x – ${roiLike}x Cloud ROI · ${paybackDays}d Payback`);

      setTxt(`agBktLlm_${agentId}`, `$${llmMo.toFixed(2)}/mo`);
      setTxt(`agBktComp_${agentId}`, `$${computeMo.toFixed(2)}/mo`);
      setTxt(`agBktData_${agentId}`, `$${dataMo.toFixed(2)}/mo`);
      setTxt(`agBktApi_${agentId}`, `$${apiMo.toFixed(2)}/mo`);
      setTxt(`agLiveTotalBanner_${agentId}`, `$${totalMo.toFixed(2)}/mo ($${Math.round(totalYr).toLocaleString()}/yr)`);

      const pct = (v) => totalMo > 0 ? Math.max(4, Math.round((v / totalMo) * 100)) : 25;
      const barLlm = document.getElementById(`agBarLlm_${agentId}`);
      const barComp = document.getElementById(`agBarComp_${agentId}`);
      const barData = document.getElementById(`agBarData_${agentId}`);
      const barApi = document.getElementById(`agBarApi_${agentId}`);
      if (barLlm) barLlm.style.width = `${pct(llmMo)}%`;
      if (barComp) barComp.style.width = `${pct(computeMo)}%`;
      if (barData) barData.style.width = `${pct(dataMo)}%`;
      if (barApi) barApi.style.width = `${pct(apiMo)}%`;
    }

    function renderAgentCostAndRoiPanel(ag, dept) {
      const cm = ag.costModel;
      if (!cm) return '';
      const mb = cm.monthlyBreakdown;
      const vm = cm.valueModel;
      const d1 = vm.drivers[0];
      const d2 = vm.drivers[1];
      const pilotCallsDay = Math.max(50, Math.round(cm.eventsPerDay * 0.28));
      const hyperCallsDay = cm.eventsPerDay * 5;

      const llmPct = Math.max(5, Math.round((mb.llmFsp3YrUsd / mb.totalFsp3YrUsd) * 100));
      const compPct = Math.max(5, Math.round((mb.computeUsd / mb.totalFsp3YrUsd) * 100));
      const dataPct = Math.max(5, Math.round((mb.dataUsd / mb.totalFsp3YrUsd) * 100));
      const apiPct = Math.max(4, 100 - llmPct - compPct - dataPct);

      return `
        <div id="agentCostRoiSection_${ag.id}" class="agent-arch-box" style="margin-top:26px; margin-bottom:26px; border:1px solid rgba(16,185,129,0.42); background:linear-gradient(180deg, rgba(6,18,32,0.96), rgba(9,24,42,0.94)); box-shadow:0 16px 40px rgba(0,0,0,0.28);">
          <!-- Top Header -->
          <div style="display:flex; flex-wrap:wrap; align-items:flex-start; justify-content:space-between; gap:14px; padding-bottom:16px; border-bottom:1px solid rgba(148,163,184,0.2); margin-bottom:20px;">
            <div>
              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:6px;">
                <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; padding:4px 10px; border-radius:999px; background:rgba(16,185,129,0.18); color:#34d399; border:1px solid rgba(16,185,129,0.45); letter-spacing:0.06em; text-transform:uppercase;">
                  💰 SINGLE-AGENT CLOUD COST, TOKENOMICS &amp; 3-YEAR ROI MODEL
                </span>
                <span style="font-family:var(--font-mono); font-size:11px; font-weight:700; padding:4px 10px; border-radius:999px; background:rgba(56,189,248,0.15); color:#38bdf8; border:1px solid rgba(56,189,248,0.38);">
                  ${cm.modelName} · ${cm.tierLabel.split('·')[0].trim()}
                </span>
                <span style="font-family:var(--font-mono); font-size:11px; font-weight:700; padding:4px 10px; border-radius:999px; background:rgba(168,85,247,0.15); color:#c084fc; border:1px solid rgba(168,85,247,0.38);">
                  Context Cache -75% · 3-Yr FSP -20%
                </span>
              </div>
              <h3 style="font-family:var(--font-display); font-size:clamp(20px, 2.2vw, 25px); font-weight:800; color:#f8fafc; margin:0;">
                How Much Does <span style="color:#34d399;">${ag.name}</span> Cost to Run &amp; What Is Its Net ROI?
              </h3>
              <p style="font-size:13.5px; color:#cbd5e1; margin:5px 0 0; line-height:1.5;">
                Deterministic bottom-up FinOps calculation across <strong>Vertex AI Gemini tokens</strong>, <strong>Agent Engine + ${cm.compute.solverEngine}</strong>, <strong>4 Partitioned BigQuery Tables</strong>, and <strong>${cm.api.connectorName}</strong>.
              </p>
            </div>
            <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center;">
              <a href="cost_analysis_presentation.html" target="_blank"
                 style="text-decoration:none; display:inline-flex; align-items:center; gap:7px; padding:9px 15px; border-radius:999px; background:linear-gradient(135deg,#059669,#0284c7); color:#ffffff; font-size:12.5px; font-weight:800; border:1px solid rgba(52,211,153,0.5); box-shadow:0 4px 14px rgba(16,185,129,0.28);">
                📊 Open Full 60-Agent Portfolio Cost Deck &rarr;
              </a>
            </div>
          </div>

          <!-- 4 Executive KPI Cards -->
          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap:14px; margin-bottom:20px;">
            <!-- Card 1: Enterprise Monthly Run Rate -->
            <div style="padding:16px 18px; border-radius:14px; background:rgba(15,23,42,0.85); border:1px solid rgba(56,189,248,0.38); border-top:3px solid #38bdf8;">
              <div style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:#38bdf8; text-transform:uppercase; letter-spacing:0.05em;">
                01 · Enterprise Cloud Cost (3-Yr FSP)
              </div>
              <div id="agLiveMoCost_${ag.id}" style="font-family:var(--font-display); font-size:28px; font-weight:800; color:#ffffff; margin:6px 0 4px;">
                $${mb.totalFsp3YrUsd.toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2})} / mo
              </div>
              <div id="agLiveYrCost_${ag.id}" style="font-size:12.5px; color:#94a3b8; line-height:1.45;">
                $${Math.round(mb.annualCloudFsp3YrUsd).toLocaleString()} / yr Cloud ($${Math.round(mb.totalAnnualRunCostUsd).toLocaleString()}/yr incl. 15% Ops)
              </div>
            </div>

            <!-- Card 2: Unit Cost per 1K Invocations -->
            <div style="padding:16px 18px; border-radius:14px; background:rgba(15,23,42,0.85); border:1px solid rgba(168,85,247,0.38); border-top:3px solid #a855f7;">
              <div style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:#c084fc; text-transform:uppercase; letter-spacing:0.05em;">
                02 · Blended Unit Cost / 1,000 Calls
              </div>
              <div id="agLiveUnit1k_${ag.id}" style="font-family:var(--font-display); font-size:28px; font-weight:800; color:#ffffff; margin:6px 0 4px;">
                $${mb.blendedCostPer1kCallsUsd.toFixed(2)} / 1K calls
              </div>
              <div style="font-size:12.5px; color:#94a3b8; line-height:1.45;">
                Token Inference: <strong>$${cm.tokens.tokenCostPer1kCallsUsd.toFixed(2)}/1K</strong> (${cm.tokens.totalPerCall.toLocaleString()} tok/call)
              </div>
            </div>

            <!-- Card 3: Scale Envelopes (Pilot vs Hyperscale) -->
            <div style="padding:16px 18px; border-radius:14px; background:rgba(15,23,42,0.85); border:1px solid rgba(245,158,11,0.38); border-top:3px solid #f59e0b;">
              <div style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:#fbbf24; text-transform:uppercase; letter-spacing:0.05em;">
                03 · Pilot (1 Plant) vs. Hyperscale (5x)
              </div>
              <div style="font-family:var(--font-display); font-size:24px; font-weight:800; color:#ffffff; margin:6px 0 4px;">
                $${mb.pilotScaleMoUsd.toFixed(0)}/mo <span style="font-size:14px; color:#94a3b8; font-weight:600;">&rarr;</span> $${Math.round(mb.hyperscaleMoUsd).toLocaleString()}/mo
              </div>
              <div style="font-size:12.5px; color:#94a3b8; line-height:1.45;">
                PayGo List: $${mb.totalPayGoUsd.toFixed(2)}/mo · 1-Yr FSP: $${mb.totalFsp1YrUsd.toFixed(2)}/mo
              </div>
            </div>

            <!-- Card 4: Single-Agent Net Annual Value & Payback -->
            <div style="padding:16px 18px; border-radius:14px; background:rgba(15,23,42,0.85); border:1px solid rgba(16,185,129,0.45); border-top:3px solid #10b981;">
              <div style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:#34d399; text-transform:uppercase; letter-spacing:0.05em;">
                04 · Single-Agent Annual Business Value
              </div>
              <div style="font-family:var(--font-display); font-size:26px; font-weight:800; color:#34d399; margin:6px 0 4px;">
                $${(vm.grossAnnualConservativeUsd / 1e6).toFixed(2)}M – $${(vm.grossAnnualLikelyUsd / 1e6).toFixed(2)}M/yr
              </div>
              <div id="agLiveRoiMult_${ag.id}" style="font-size:12.5px; color:#d1fae5; font-weight:700; line-height:1.45;">
                ${vm.cloudRoiMultipleConservative}x – ${vm.cloudRoiMultipleLikely}x Cloud ROI · ${vm.paybackDays}d Payback
              </div>
            </div>
          </div>

          <!-- Interactive Live Single-Agent Volume & FSP Sizer -->
          <div style="padding:18px 20px; border-radius:14px; background:rgba(15,23,42,0.9); border:1px solid rgba(148,163,184,0.24); margin-bottom:20px;">
            <div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:12px; margin-bottom:14px;">
              <div>
                <div style="font-family:var(--font-display); font-size:16px; font-weight:800; color:#f8fafc;">
                  🎛️ Live Showcase Sizer — Test ${ag.name} at Your Enterprise Volume
                </div>
                <div style="font-size:12.5px; color:#94a3b8;">
                  Drag daily invocation frequency or click a scale preset to recalculate monthly cloud spend &amp; ROI live during customer presentations:
                </div>
              </div>
              <div style="display:flex; gap:8px; flex-wrap:wrap;">
                <button type="button" class="switch-pill" style="font-size:11.5px; padding:5px 11px; border-color:rgba(245,158,11,0.45); color:#fbbf24;"
                        onclick="setSingleAgentScalePreset('${ag.id}', ${pilotCallsDay}, 20)">
                  🌱 Pilot (1 Plant · ${pilotCallsDay.toLocaleString()}/day)
                </button>
                <button type="button" class="switch-pill" style="font-size:11.5px; padding:5px 11px; border-color:rgba(56,189,248,0.5); color:#38bdf8; font-weight:700;"
                        onclick="setSingleAgentScalePreset('${ag.id}', ${cm.eventsPerDay}, 20)">
                  🏢 Enterprise Baseline (${cm.eventsPerDay.toLocaleString()}/day)
                </button>
                <button type="button" class="switch-pill" style="font-size:11.5px; padding:5px 11px; border-color:rgba(16,185,129,0.5); color:#34d399;"
                        onclick="setSingleAgentScalePreset('${ag.id}', ${hyperCallsDay}, 20)">
                  🌐 Global Hyperscale (${hyperCallsDay.toLocaleString()}/day)
                </button>
              </div>
            </div>

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:16px; align-items:center; margin-bottom:16px;">
              <div>
                <div style="display:flex; justify-content:space-between; font-size:12.5px; font-weight:700; color:#e2e8f0; margin-bottom:6px;">
                  <span>Daily Agent Runs (${cm.triggerCadence})</span>
                  <span id="agCallsLbl_${ag.id}" style="font-family:var(--font-mono); color:#38bdf8;">${cm.eventsPerDay.toLocaleString()} calls/day (${cm.monthlyCalls.toLocaleString()}/mo)</span>
                </div>
                <input id="agCostCallsSlider_${ag.id}" type="range" min="50" max="20000" step="50" value="${cm.eventsPerDay}"
                       style="width:100%; accent-color:#38bdf8; cursor:pointer;"
                       oninput="updateSingleAgentCostCalc('${ag.id}')" />
              </div>

              <div>
                <div style="display:flex; justify-content:space-between; font-size:12.5px; font-weight:700; color:#e2e8f0; margin-bottom:6px;">
                  <span>Vertex AI FSP Commitment Tier</span>
                  <span style="font-family:var(--font-mono); color:#34d399;"> Applies to Gemini Token Inference</span>
                </div>
                <select id="agCostFspSelect_${ag.id}" onchange="updateSingleAgentCostCalc('${ag.id}')"
                        style="width:100%; padding:8px 12px; border-radius:8px; background:#0f172a; color:#f8fafc; border:1px solid rgba(56,189,248,0.4); font-family:var(--font-mono); font-size:12.5px; font-weight:700;">
                  <option value="0">Pay-As-You-Go (0% Discount · $${mb.totalPayGoUsd.toFixed(2)}/mo baseline)</option>
                  <option value="10">1-Year Vertex AI FSP (-10% Token Discount · $${mb.totalFsp1YrUsd.toFixed(2)}/mo baseline)</option>
                  <option value="20" selected>3-Year Vertex AI FSP (-20% Token Discount · $${mb.totalFsp3YrUsd.toFixed(2)}/mo baseline)</option>
                </select>
              </div>
            </div>

            <!-- Visual 4-Component Cost Distribution Bar -->
            <div style="height:10px; border-radius:999px; overflow:hidden; display:flex; background:#090d16; margin-bottom:12px;">
              <div id="agBarLlm_${ag.id}" style="width:${llmPct}%; background:#38bdf8;" title="Vertex AI Gemini Token Inference"></div>
              <div id="agBarComp_${ag.id}" style="width:${compPct}%; background:#a855f7;" title="Agent Engine + OR-Tools Solver Compute"></div>
              <div id="agBarData_${ag.id}" style="width:${dataPct}%; background:#10b981;" title="BigQuery Digital Twin Scan & Storage"></div>
              <div id="agBarApi_${ag.id}" style="width:${apiPct}%; background:#f59e0b;" title="Domain APIs & Enterprise Connectors"></div>
            </div>

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:10px;">
              <div style="padding:10px 12px; border-radius:10px; background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.28); display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:12px; color:#bae6fd; font-weight:700;">● Gemini Tokens</span>
                <span id="agBktLlm_${ag.id}" style="font-family:var(--font-mono); font-size:13px; font-weight:800; color:#38bdf8;">$${mb.llmFsp3YrUsd.toFixed(2)}/mo</span>
              </div>
              <div style="padding:10px 12px; border-radius:10px; background:rgba(168,85,247,0.08); border:1px solid rgba(168,85,247,0.28); display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:12px; color:#e9d5ff; font-weight:700;">● Agent Engine + Solver</span>
                <span id="agBktComp_${ag.id}" style="font-family:var(--font-mono); font-size:13px; font-weight:800; color:#c084fc;">$${mb.computeUsd.toFixed(2)}/mo</span>
              </div>
              <div style="padding:10px 12px; border-radius:10px; background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.28); display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:12px; color:#a7f3d0; font-weight:700;">● BigQuery (4 Tables)</span>
                <span id="agBktData_${ag.id}" style="font-family:var(--font-mono); font-size:13px; font-weight:800; color:#34d399;">$${mb.dataUsd.toFixed(2)}/mo</span>
              </div>
              <div style="padding:10px 12px; border-radius:10px; background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.28); display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:12px; color:#fde68a; font-weight:700;">● Domain APIs / ERP</span>
                <span id="agBktApi_${ag.id}" style="font-family:var(--font-mono); font-size:13px; font-weight:800; color:#fbbf24;">$${mb.apiUsd.toFixed(2)}/mo</span>
              </div>
            </div>
          </div>

          <!-- Two Side-by-Side Audit Ledger Tables: (1) Cloud Cost Math & (2) Business Value Math -->
          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(440px, 1fr)); gap:16px;">
            <!-- Left Table: 4-Bucket Bottom-Up Cloud Cost Formula -->
            <div style="padding:16px 18px; border-radius:14px; background:rgba(15,23,42,0.82); border:1px solid rgba(148,163,184,0.22); overflow-x:auto;">
              <div style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; color:#38bdf8; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:10px;">
                🧮 Bottom-Up Monthly Cloud Cost Formula (${cm.monthlyCalls.toLocaleString()} calls/mo)
              </div>
              <table style="width:100%; border-collapse:collapse; font-size:12.5px; color:#e2e8f0;">
                <thead>
                  <tr style="border-bottom:1px solid rgba(148,163,184,0.25); text-align:left; color:#94a3b8; font-family:var(--font-mono); font-size:11px;">
                    <th style="padding:7px 6px;">Cost Bucket</th>
                    <th style="padding:7px 6px;">Engineering Formula</th>
                    <th style="padding:7px 6px; text-align:right;">Monthly (3-Yr FSP)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr style="border-bottom:1px solid rgba(148,163,184,0.12);">
                    <td style="padding:9px 6px; font-weight:700; color:#38bdf8;">1. Gemini Tokens<br><span style="font-size:11px; color:#94a3b8; font-weight:500;">${cm.modelSlug}</span></td>
                    <td style="padding:9px 6px; font-family:var(--font-mono); font-size:11.5px; color:#cbd5e1;">${cm.tokens.formula}<br><span style="color:#94a3b8;">× ${cm.monthlyCalls.toLocaleString()} calls/mo × 0.80 (3-Yr FSP)</span></td>
                    <td style="padding:9px 6px; text-align:right; font-family:var(--font-mono); font-weight:800; color:#38bdf8;">$${mb.llmFsp3YrUsd.toFixed(2)}<br><span style="font-size:10.5px; color:#94a3b8; font-weight:500;">PayGo: $${mb.llmPayGoUsd.toFixed(2)}</span></td>
                  </tr>
                  <tr style="border-bottom:1px solid rgba(148,163,184,0.12);">
                    <td style="padding:9px 6px; font-weight:700; color:#c084fc;">2. Agent Engine<br><span style="font-size:11px; color:#94a3b8; font-weight:500;">${cm.compute.solverEngine}</span></td>
                    <td style="padding:9px 6px; font-family:var(--font-mono); font-size:11.5px; color:#cbd5e1;">${cm.compute.formula}<br><span style="color:#94a3b8;">(${cm.compute.avgDurationSec}s avg · ${cm.compute.vcpuCount} vCPU / ${cm.compute.ramGib} GiB)</span></td>
                    <td style="padding:9px 6px; text-align:right; font-family:var(--font-mono); font-weight:800; color:#c084fc;">$${mb.computeUsd.toFixed(2)}</td>
                  </tr>
                  <tr style="border-bottom:1px solid rgba(148,163,184,0.12);">
                    <td style="padding:9px 6px; font-weight:700; color:#34d399;">3. BigQuery Twin<br><span style="font-size:11px; color:#94a3b8; font-weight:500;">4 Partitioned Tables</span></td>
                    <td style="padding:9px 6px; font-family:var(--font-mono); font-size:11.5px; color:#cbd5e1;">${cm.data.formula}</td>
                    <td style="padding:9px 6px; text-align:right; font-family:var(--font-mono); font-weight:800; color:#34d399;">$${mb.dataUsd.toFixed(2)}</td>
                  </tr>
                  <tr style="border-bottom:1px solid rgba(148,163,184,0.22);">
                    <td style="padding:9px 6px; font-weight:700; color:#fbbf24;">4. Domain APIs<br><span style="font-size:11px; color:#94a3b8; font-weight:500;">External Connectors</span></td>
                    <td style="padding:9px 6px; font-family:var(--font-mono); font-size:11.5px; color:#cbd5e1;">${cm.api.formula}</td>
                    <td style="padding:9px 6px; text-align:right; font-family:var(--font-mono); font-weight:800; color:#fbbf24;">$${mb.apiUsd.toFixed(2)}</td>
                  </tr>
                  <tr style="background:rgba(56,189,248,0.1);">
                    <td colspan="2" style="padding:10px 8px; font-weight:800; color:#ffffff;">Total Single-Agent Cloud Run-Rate (3-Yr FSP)</td>
                    <td style="padding:10px 8px; text-align:right; font-family:var(--font-mono); font-weight:800; color:#38bdf8; font-size:14px;">$${mb.totalFsp3YrUsd.toFixed(2)}/mo<br><span style="font-size:11px; color:#cbd5e1;">$${Math.round(mb.annualCloudFsp3YrUsd).toLocaleString()}/yr</span></td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Right Table: Quantified Business Value Drivers (Conservative vs. Likely) -->
            <div style="padding:16px 18px; border-radius:14px; background:rgba(15,23,42,0.82); border:1px solid rgba(148,163,184,0.22); overflow-x:auto;">
              <div style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; color:#34d399; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:10px;">
                📈 Single-Agent Value Model &amp; 3-Year ROI (Conservative vs. Likely)
              </div>
              <table style="width:100%; border-collapse:collapse; font-size:12.5px; color:#e2e8f0;">
                <thead>
                  <tr style="border-bottom:1px solid rgba(148,163,184,0.25); text-align:left; color:#94a3b8; font-family:var(--font-mono); font-size:11px;">
                    <th style="padding:7px 6px;">Value Driver &amp; Baseline</th>
                    <th style="padding:7px 6px; text-align:right;">Conservative</th>
                    <th style="padding:7px 6px; text-align:right;">Likely</th>
                  </tr>
                </thead>
                <tbody>
                  <tr style="border-bottom:1px solid rgba(148,163,184,0.12);">
                    <td style="padding:9px 6px;">
                      <span style="font-family:var(--font-mono); font-size:10.5px; font-weight:800; color:#38bdf8; text-transform:uppercase;">${d1.category}</span>
                      <div style="font-weight:700; color:#f8fafc; margin:2px 0;">${d1.name}</div>
                      <div style="font-size:11.5px; color:#94a3b8;">${d1.formula}</div>
                    </td>
                    <td style="padding:9px 6px; text-align:right; font-family:var(--font-mono); font-weight:700; color:#e2e8f0;">
                      +$${(d1.conservativeAnnualUsd / 1e3).toLocaleString()}K/yr<br>
                      <span style="font-size:10.5px; color:#94a3b8;">(${d1.conservativeLiftPct}% lift)</span>
                    </td>
                    <td style="padding:9px 6px; text-align:right; font-family:var(--font-mono); font-weight:800; color:#34d399;">
                      +$${(d1.likelyAnnualUsd / 1e3).toLocaleString()}K/yr<br>
                      <span style="font-size:10.5px; color:#a7f3d0;">(${d1.likelyLiftPct}% lift)</span>
                    </td>
                  </tr>
                  <tr style="border-bottom:1px solid rgba(148,163,184,0.12);">
                    <td style="padding:9px 6px;">
                      <span style="font-family:var(--font-mono); font-size:10.5px; font-weight:800; color:#c084fc; text-transform:uppercase;">${d2.category}</span>
                      <div style="font-weight:700; color:#f8fafc; margin:2px 0;">${d2.name}</div>
                      <div style="font-size:11.5px; color:#94a3b8;">${d2.formula}</div>
                    </td>
                    <td style="padding:9px 6px; text-align:right; font-family:var(--font-mono); font-weight:700; color:#e2e8f0;">
                      +$${(d2.conservativeAnnualUsd / 1e3).toLocaleString()}K/yr<br>
                      <span style="font-size:10.5px; color:#94a3b8;">(${d2.conservativeLiftPct}% lift)</span>
                    </td>
                    <td style="padding:9px 6px; text-align:right; font-family:var(--font-mono); font-weight:800; color:#34d399;">
                      +$${(d2.likelyAnnualUsd / 1e3).toLocaleString()}K/yr<br>
                      <span style="font-size:10.5px; color:#a7f3d0;">(${d2.likelyLiftPct}% lift)</span>
                    </td>
                  </tr>
                  <tr style="border-bottom:1px solid rgba(148,163,184,0.2);">
                    <td style="padding:8px 6px; color:#fca5a5; font-weight:600;">Less Annual Cloud + 15% Ops Maintenance Cost</td>
                    <td style="padding:8px 6px; text-align:right; font-family:var(--font-mono); color:#fca5a5;">-$${Math.round(mb.totalAnnualRunCostUsd).toLocaleString()}/yr</td>
                    <td style="padding:8px 6px; text-align:right; font-family:var(--font-mono); color:#fca5a5;">-$${Math.round(mb.totalAnnualRunCostUsd).toLocaleString()}/yr</td>
                  </tr>
                  <tr style="background:rgba(16,185,129,0.12);">
                    <td style="padding:10px 8px; font-weight:800; color:#ffffff;">Net Annual Value &amp; Cloud ROI Multiple</td>
                    <td style="padding:10px 8px; text-align:right; font-family:var(--font-mono); font-weight:800; color:#e2e8f0; font-size:13.5px;">
                      $${(vm.netAnnualConservativeUsd / 1e6).toFixed(2)}M/yr<br>
                      <span style="font-size:11px; color:#38bdf8;">${vm.cloudRoiMultipleConservative}x Cloud ROI</span>
                    </td>
                    <td style="padding:10px 8px; text-align:right; font-family:var(--font-mono); font-weight:800; color:#34d399; font-size:14px;">
                      $${(vm.netAnnualLikelyUsd / 1e6).toFixed(2)}M/yr<br>
                      <span style="font-size:11px; color:#a7f3d0;">${vm.cloudRoiMultipleLikely}x ROI · ${vm.paybackDays}d Payback</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      `;
    }
"""


def update_html_files(catalog: dict) -> None:
    agents_json = json.dumps(catalog["agents"], indent=2)

    for path in HTML_FILES:
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")

        # 1. Replace `const AGENTS = { ... };`
        pattern = re.compile(
            r"    const AGENTS = \{[\s\S]*?\n\};\n    Object\.defineProperty\(AGENTS,",
            re.M,
        )
        if not pattern.search(html):
            raise RuntimeError(f"Could not find `const AGENTS =` block in {path}")
        html = pattern.sub(
            lambda _: f"    const AGENTS = {agents_json};\n    Object.defineProperty(AGENTS,",
            html,
            count=1,
        )

        # 2. Inject `renderAgentCostAndRoiPanel` & `updateSingleAgentCostCalc` right before `function openAgentPage`
        if "function renderAgentCostAndRoiPanel(" not in html:
            html = html.replace(
                "    function openAgentPage(agentId, pushHash = true, ev = null) {",
                AGENT_COST_UI_JS + "\n    function openAgentPage(agentId, pushHash = true, ev = null) {",
                1,
            )

        # 3. Add Hero Cost & ROI Showcase Strip inside `.agent-hero-banner` in `openAgentPage`
        old_hero_drawer_Anchor = """            <div id="agentMoreDetailsDrawer" class="journey-accordion-item" style="margin-top:14px; margin-bottom:0;">"""
        new_hero_cost_strip = """            ${ag.costModel ? `
              <div style="margin-top:16px; padding:12px 16px; border-radius:12px; background:rgba(16,185,129,0.10); border:1px solid rgba(16,185,129,0.38); display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:12px;">
                <div style="display:flex; flex-wrap:wrap; align-items:center; gap:14px; font-size:13px;">
                  <span style="font-family:var(--font-mono); font-weight:800; color:#10b981;">
                    💰 Est. Cloud Cost: <span id="agLiveTotalBanner_${ag.id}">$${ag.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(2)}/mo ($${Math.round(ag.costModel.monthlyBreakdown.annualCloudFsp3YrUsd).toLocaleString()}/yr w/ 3-Yr FSP)</span>
                  </span>
                  <span style="color:var(--text-secondary);">|</span>
                  <span style="font-family:var(--font-mono); font-weight:700; color:var(--text-primary);">
                    ⚡ Unit: $${ag.costModel.monthlyBreakdown.blendedCostPer1kCallsUsd.toFixed(2)}/1K calls (${ag.costModel.modelName.replace(' (Vertex AI)', '')})
                  </span>
                  <span style="color:var(--text-secondary);">|</span>
                  <span style="font-family:var(--font-mono); font-weight:700; color:#0284c7;">
                    🌱 Pilot: $${ag.costModel.monthlyBreakdown.pilotScaleMoUsd.toFixed(0)}/mo
                  </span>
                  <span style="color:var(--text-secondary);">|</span>
                  <span style="font-family:var(--font-mono); font-weight:800; color:#059669;">
                    📈 Net Value: $${(ag.costModel.valueModel.grossAnnualConservativeUsd / 1e6).toFixed(2)}M–$${(ag.costModel.valueModel.grossAnnualLikelyUsd / 1e6).toFixed(2)}M/yr (${ag.costModel.valueModel.cloudRoiMultipleConservative}x ROI · ${ag.costModel.valueModel.paybackDays}d Payback)
                  </span>
                </div>
                <button type="button" class="switch-pill" style="background:#059669; color:#ffffff; border-color:#059669; font-weight:800; font-size:12px; padding:6px 13px;"
                        onclick="const el = document.getElementById('agentCostRoiSection_${ag.id}'); if (el) el.scrollIntoView({behavior:'smooth', block:'start'});">
                  🧮 Interactive Cost &amp; ROI Calculator &darr;
                </button>
              </div>
            ` : ''}
            <div id="agentMoreDetailsDrawer" class="journey-accordion-item" style="margin-top:14px; margin-bottom:0;">"""
        if "agLiveTotalBanner_" not in html and old_hero_drawer_Anchor in html:
            html = html.replace(old_hero_drawer_Anchor, new_hero_cost_strip, 1)

        # 4. Render `renderAgentCostAndRoiPanel(ag, dept)` above `renderAgentAdkAndDemoDataPanel(ag)` in both `openAgentPage` and `openAgentBlueprintPage`
        if "${renderAgentCostAndRoiPanel(ag, dept)}" not in html:
            html = html.replace(
                "          ${renderAgentAdkAndDemoDataPanel(ag)}",
                "          ${renderAgentCostAndRoiPanel(ag, dept)}\n\n          ${renderAgentAdkAndDemoDataPanel(ag)}",
            )

        # 5. Add Cost & ROI pill to Persona Page `.persona-step-agent-box` and `.persona-agent-dock-card`
        old_step_agent_desc = """                              <div style="font-size:13.5px; color:var(--text-secondary); line-height:1.45;">
                                ${shortSentence(plugAgent.solution || plugAgent.role, 155)}
                              </div>"""
        new_step_agent_desc = """                              <div style="font-size:13.5px; color:var(--text-secondary); line-height:1.45;">
                                ${shortSentence(plugAgent.solution || plugAgent.role, 155)}
                              </div>
                              ${plugAgent.costModel ? `
                                <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:7px;">
                                  <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; padding:3px 9px; border-radius:6px; background:rgba(2,132,199,0.12); color:#0284c7; border:1px solid rgba(2,132,199,0.3);">
                                    💰 Cloud: $${plugAgent.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo ($${plugAgent.costModel.monthlyBreakdown.blendedCostPer1kCallsUsd.toFixed(2)}/1K calls · ${plugAgent.costModel.modelName.replace(' (Vertex AI)', '')})
                                  </span>
                                  <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; padding:3px 9px; border-radius:6px; background:rgba(16,185,129,0.12); color:#059669; border:1px solid rgba(16,185,129,0.3);">
                                    📈 Value: $${(plugAgent.costModel.valueModel.grossAnnualConservativeUsd/1e6).toFixed(2)}M–$${(plugAgent.costModel.valueModel.grossAnnualLikelyUsd/1e6).toFixed(2)}M/yr (${plugAgent.costModel.valueModel.cloudRoiMultipleConservative}x ROI)
                                  </span>
                                </div>
                              ` : ''}"""
        if "plugAgent.costModel" not in html and old_step_agent_desc in html:
            html = html.replace(old_step_agent_desc, new_step_agent_desc, 1)

        old_dock_badge = """                      ${ag.badge ? `
                        <div style="display:inline-flex; align-items:center; padding:3px 10px; border-radius:999px; background:rgba(16,185,129,0.14); border:1px solid rgba(16,185,129,0.38); color:#10b981; font-family:var(--font-mono); font-size:11px; font-weight:800;">
                          ✦ ${ag.badge}
                        </div>
                      ` : ''}"""
        new_dock_badge = """                      ${ag.badge ? `
                        <div style="display:inline-flex; align-items:center; padding:3px 10px; border-radius:999px; background:rgba(16,185,129,0.14); border:1px solid rgba(16,185,129,0.38); color:#10b981; font-family:var(--font-mono); font-size:11px; font-weight:800; margin-bottom:6px;">
                          ✦ ${ag.badge}
                        </div>
                      ` : ''}
                      ${ag.costModel ? `
                        <div style="padding:8px 10px; border-radius:8px; background:rgba(2,132,199,0.08); border:1px solid rgba(2,132,199,0.25); font-family:var(--font-mono); font-size:11px; color:var(--text-primary); margin-top:4px; line-height:1.45;">
                          <div><strong>💰 Cloud Run Rate:</strong> $${ag.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo ($${ag.costModel.monthlyBreakdown.blendedCostPer1kCallsUsd.toFixed(2)}/1K calls)</div>
                          <div style="color:#059669; font-weight:800;"><strong>📈 Net Value:</strong> $${(ag.costModel.valueModel.grossAnnualConservativeUsd/1e6).toFixed(2)}M/yr (${ag.costModel.valueModel.cloudRoiMultipleConservative}x ROI · ${ag.costModel.valueModel.paybackDays}d payback)</div>
                        </div>
                      ` : ''}"""
        if "💰 Cloud Run Rate:" not in html and old_dock_badge in html:
            html = html.replace(old_dock_badge, new_dock_badge, 1)

        # 6. Add Cost & ROI badge to Directory Agent Cards (`renderDirectoryCardsHtml`)
        old_dir_card = """                  <div class="ai-agent-chip-title" style="font-size:17px;">${ag.name}</div>
                  <div style="font-size:12.5px; color:var(--text-secondary); margin-top:2px;">
                    ${ag.isUniversal ? 'All 6 SCOR Pillars' : dept.name}
                  </div>"""
        new_dir_card = """                  <div class="ai-agent-chip-title" style="font-size:16px;">${ag.categoryDisplayName || ag.name}</div>
                  <div style="font-size:12.5px; color:var(--text-secondary); margin-top:2px;">
                    ${ag.isUniversal ? 'All 6 SCOR Pillars' : dept.name}
                  </div>
                  ${ag.costModel ? `
                    <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:6px; font-family:var(--font-mono); font-size:10.5px; font-weight:800;">
                      <span style="padding:2px 7px; border-radius:5px; background:rgba(2,132,199,0.12); color:#0284c7; border:1px solid rgba(2,132,199,0.28);">
                        💰 $${ag.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo · $${ag.costModel.monthlyBreakdown.blendedCostPer1kCallsUsd.toFixed(2)}/1K
                      </span>
                      <span style="padding:2px 7px; border-radius:5px; background:rgba(16,185,129,0.12); color:#059669; border:1px solid rgba(16,185,129,0.28);">
                        📈 $${(ag.costModel.valueModel.grossAnnualConservativeUsd/1e6).toFixed(2)}M/yr (${ag.costModel.valueModel.cloudRoiMultipleConservative}x ROI)
                      </span>
                    </div>
                  ` : ''}"""
        if old_dir_card in html:
            html = html.replace(old_dir_card, new_dir_card, 1)

        # 7. Add Cost & FinOps box to Periodic Table Inline Expansion Card & Right Sticky Inspector
        old_pt_inline_grid = """            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:14px;">"""
        new_pt_inline_grid = """            ${ag.costModel ? `
              <div style="padding:12px 16px; border-radius:12px; background:rgba(2,132,199,0.08); border:1px solid rgba(2,132,199,0.28); margin-bottom:14px; display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:10px; font-family:var(--font-mono); font-size:12px;">
                <div><strong>💰 Enterprise Cloud Cost (3-Yr FSP):</strong> <span style="color:#0284c7; font-weight:800;">$${ag.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(2)}/mo</span> ($${Math.round(ag.costModel.monthlyBreakdown.annualCloudFsp3YrUsd).toLocaleString()}/yr · Pilot: $${ag.costModel.monthlyBreakdown.pilotScaleMoUsd.toFixed(0)}/mo)</div>
                <div><strong>⚡ Unit Cost:</strong> $${ag.costModel.monthlyBreakdown.blendedCostPer1kCallsUsd.toFixed(2)}/1K calls (${ag.costModel.modelName.replace(' (Vertex AI)', '')})</div>
                <div style="color:#059669; font-weight:800;">📈 Net Value: $${(ag.costModel.valueModel.grossAnnualConservativeUsd/1e6).toFixed(2)}M–$${(ag.costModel.valueModel.grossAnnualLikelyUsd/1e6).toFixed(2)}M/yr (${ag.costModel.valueModel.cloudRoiMultipleConservative}x ROI)</div>
              </div>
            ` : ''}
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:14px;">"""
        if "Enterprise Cloud Cost (3-Yr FSP):" not in html and old_pt_inline_grid in html:
            html = html.replace(old_pt_inline_grid, new_pt_inline_grid, 1)

        old_pt_side_persona = """              <!-- Primary Human Persona Box inside Inspector -->"""
        new_pt_side_cost_and_persona = """              <!-- Cloud Cost & ROI Summary inside Sticky Inspector -->
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
              ` : ''}

              <!-- Primary Human Persona Box inside Inspector -->"""
        if "Cloud FinOps &amp; 3-Year ROI" not in html and old_pt_side_persona in html:
            html = html.replace(old_pt_side_persona, new_pt_side_cost_and_persona, 1)

        # 8. Add Cost & ROI badge to Neural Mind Map Column 3 Agent Cards (`openMindMapPage`)
        old_mm_header_tag = """                              <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:#10b981;">✦ ${ag.badge}</span>
                            </div>"""
        new_mm_header_tag = """                              <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:#10b981;">✦ ${ag.badge}</span>
                              ${ag.costModel ? `
                                <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; padding:2px 8px; border-radius:6px; background:rgba(2,132,199,0.14); color:#0284c7; border:1px solid rgba(2,132,199,0.35);">
                                  💰 $${ag.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo · $${ag.costModel.monthlyBreakdown.blendedCostPer1kCallsUsd.toFixed(2)}/1K · 📈 $${(ag.costModel.valueModel.grossAnnualConservativeUsd/1e6).toFixed(2)}M/yr (${ag.costModel.valueModel.cloudRoiMultipleConservative}x ROI)
                                </span>
                              ` : ''}
                            </div>"""
        if old_mm_header_tag in html:
            html = html.replace(old_mm_header_tag, new_mm_header_tag, 1)

        # 9. Add compact monthly cost badge to each Periodic Table element tile (`.pt-tile`)
        old_pt_tile = """                            <div class="pt-tile-sym">${m.sym}</div>
                            <div class="pt-tile-title" title="${ag.name}">${m.short}</div>
                            <div class="pt-tile-dot" title="${m.layer}"></div>"""
        new_pt_tile = """                            <div class="pt-tile-sym">${m.sym}</div>
                            <div class="pt-tile-title" title="${ag.name}">${m.short}</div>
                            ${ag.costModel ? `<div style="font-family:var(--font-mono); font-size:9.5px; font-weight:800; color:#0284c7; margin-top:2px;">$${ag.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo · ${ag.costModel.valueModel.cloudRoiMultipleConservative}x</div>` : ''}
                            <div class="pt-tile-dot" title="${m.layer}"></div>"""
        if old_pt_tile in html:
            html = html.replace(old_pt_tile, new_pt_tile, 1)

        # 10. Add CLOUD FINOPS row to Enterprise Architecture Page (`#architecture`) agent cards
        old_arch_swarm = """                          <div style="display:grid; grid-template-columns:88px 1fr; gap:4px 8px; font-size:12.5px; align-items:baseline;">
                            <span style="font-weight:700; color:#94a3b8; text-transform:uppercase; font-size:11px;">A2A SWARM</span>
                            <span style="color:#cbd5e1; font-size:12px;">${(ag.subAgents || []).map(sa => `<strong style="color:#f8fafc;">${sa.name}</strong>`).join(' · ')}</span>
                          </div>"""
        new_arch_swarm = """                          <div style="display:grid; grid-template-columns:88px 1fr; gap:4px 8px; font-size:12.5px; align-items:baseline;">
                            <span style="font-weight:700; color:#94a3b8; text-transform:uppercase; font-size:11px;">A2A SWARM</span>
                            <span style="color:#cbd5e1; font-size:12px;">${(ag.subAgents || []).map(sa => `<strong style="color:#f8fafc;">${sa.name}</strong>`).join(' · ')}</span>
                          </div>
                          ${ag.costModel ? `
                          <div style="display:grid; grid-template-columns:88px 1fr; gap:4px 8px; font-size:12.5px; align-items:baseline; padding-top:4px; border-top:1px dashed rgba(148,163,184,0.2);">
                            <span style="font-weight:800; color:#38bdf8; text-transform:uppercase; font-size:11px;">FINOPS &amp; ROI</span>
                            <span style="color:#34d399; font-family:var(--font-mono); font-size:11.5px; font-weight:700;">💰 $${ag.costModel.monthlyBreakdown.totalFsp3YrUsd.toFixed(0)}/mo ($${ag.costModel.monthlyBreakdown.blendedCostPer1kCallsUsd.toFixed(2)}/1K) · 📈 $${(ag.costModel.valueModel.grossAnnualConservativeUsd/1e6).toFixed(2)}M/yr (${ag.costModel.valueModel.cloudRoiMultipleConservative}x ROI)</span>
                          </div>
                          ` : ''}"""
        if "FINOPS &amp; ROI" not in html and old_arch_swarm in html:
            html = html.replace(old_arch_swarm, new_arch_swarm)

        path.write_text(html, encoding="utf-8")
        print(f"✅ Injected per-agent Cloud Cost & ROI UI across {path.name}")


def update_cost_presentation(catalog: dict) -> None:
    pres_path = ROOT / "cost_analysis_presentation.html"
    if not pres_path.exists():
        return
    txt = pres_path.read_text(encoding="utf-8")

    # Build the exact 60-agent JS array from catalog["agents"]
    rows_js = []
    for aid, ag in catalog["agents"].items():
        cm = ag["costModel"]
        mb = cm["monthlyBreakdown"]
        vm = cm["valueModel"]
        pillar_lbl = PILLAR_LABELS.get(ag.get("departmentId", "demand_sop"), "01 · Plan & Demand")
        rows_js.append(
            {
                "id": aid,
                "name": ag.get("categoryDisplayName", ag["name"]),
                "pillar": pillar_lbl,
                "role": ag.get("personaTitle", "Supply Chain Lead"),
                "model": cm["modelSlug"],
                "modelDisplay": cm["modelName"],
                "tokensPerCall": cm["tokens"]["totalPerCall"],
                "tokenCost1k": cm["tokens"]["tokenCostPer1kCallsUsd"],
                "cost1k": mb["blendedCostPer1kCallsUsd"],
                "callsMo": cm["monthlyCalls"],
                "pilotMo": mb["pilotScaleMoUsd"],
                "infraPayGoMo": mb["totalPayGoUsd"],
                "infraMo": mb["totalFsp3YrUsd"],
                "valConsYr": vm["grossAnnualConservativeUsd"],
                "valLikeYr": vm["grossAnnualLikelyUsd"],
                "roiMult": vm["cloudRoiMultipleConservative"],
                "paybackDays": vm["paybackDays"],
                "outcome": (ag.get("roiBadges") or [ag.get("badge", "High ROI")])[0],
            }
        )

    array_str = "    const ALL_60_AGENTS_COST = " + json.dumps(rows_js, indent=6) + ";"
    txt = re.sub(
        r"    const ALL_60_AGENTS_COST = \[[\s\S]*?\n    \];",
        lambda _: array_str,
        txt,
        count=1,
    )

    # Update `renderAgentTable` in cost_analysis_presentation.html to use exact `a.infraMo`, `a.pilotMo`, `a.valConsYr`, `a.roiMult` and link to `index.html#agent/${a.id}`
    old_render_fn = re.compile(
        r"    function renderAgentTable\(filterText = '', pillarFilter = 'ALL'\) \{[\s\S]*?\n    \}",
        re.M,
    )
    new_render_fn = """    function renderAgentTable(filterText = '', pillarFilter = 'ALL') {
      const tbody = document.getElementById('all60AgentsTbody');
      const q = filterText.trim().toLowerCase();
      const filtered = ALL_60_AGENTS_COST.filter(a => {
        const matchPillar = (pillarFilter === 'ALL') || a.pillar === pillarFilter;
        const matchText = !q || a.name.toLowerCase().includes(q) || a.role.toLowerCase().includes(q) || a.id.toLowerCase().includes(q) || a.outcome.toLowerCase().includes(q) || a.model.toLowerCase().includes(q);
        return matchPillar && matchText;
      });

      document.getElementById('agentTableCountBadge').textContent = `Showing ${filtered.length} / 60 Categorized Agents`;

      tbody.innerHTML = filtered.map((a, idx) => {
        const badgeClass = a.model.includes('pro') ? 'badge-purple' : (a.model.includes('lite') ? 'badge-blue' : 'badge-emerald');
        return `
          <tr>
            <td class="mono">${String(idx + 1).padStart(2, '0')}</td>
            <td>
              <a href="index.html#agent/${a.id}" style="color:#f8fafc; font-weight:700; text-decoration:none; border-bottom:1px dashed rgba(56,189,248,0.5);">
                ${a.name} &nearr;
              </a><br>
              <span class="mono" style="font-size:11px;color:var(--text-muted);">${a.id} · ${a.tokensPerCall.toLocaleString()} tok/call · Pilot: $${a.pilotMo.toFixed(0)}/mo</span>
            </td>
            <td>${a.role}</td>
            <td><span class="badge ${badgeClass}">${a.model}</span></td>
            <td class="mono">$${a.cost1k.toFixed(2)}<br><span style="font-size:10px;color:var(--text-muted);">LLM: $${a.tokenCost1k.toFixed(2)}</span></td>
            <td class="mono">${a.callsMo.toLocaleString()}</td>
            <td class="mono" style="color:#38bdf8;font-weight:700;">$${a.infraMo.toFixed(2)}/mo<br><span style="font-size:10px;color:#10b981;">Value: $${(a.valConsYr/1e6).toFixed(2)}M/yr (${a.roiMult}x)</span></td>
            <td>${a.outcome} · <a href="index.html#agent/${a.id}" style="color:#38bdf8;font-size:11.5px;font-weight:700;">Live Sizer &rarr;</a></td>
          </tr>
        `;
      }).join('');
    }"""
    txt = old_render_fn.sub(lambda _: new_render_fn, txt, count=1)

    pres_path.write_text(txt, encoding="utf-8")
    print("✅ Synchronized cost_analysis_presentation.html with exact bottom-up 60-agent costModel data & website deep links.")


def update_manifests(catalog: dict) -> None:
    count = 0
    for aid, ag in catalog["agents"].items():
        manifest_path = ROOT / "agents" / aid / "agents-cli-manifest.yaml"
        if not manifest_path.exists():
            continue
        cm = ag["costModel"]
        mb = cm["monthlyBreakdown"]
        vm = cm["valueModel"]
        mtxt = manifest_path.read_text(encoding="utf-8")
        new_line = (
            f"  finops_tier: \"{cm['modelSlug']} (Context Cached -75%, 3-Yr FSP -20%, "
            f"${mb['blendedCostPer1kCallsUsd']:.2f}/1K calls, ${mb['totalFsp3YrUsd']:.2f}/mo enterprise, "
            f"${vm['grossAnnualConservativeUsd']/1e6:.2f}M/yr value, {vm['cloudRoiMultipleConservative']}x ROI)\""
        )
        if "  finops_tier:" in mtxt:
            mtxt = re.sub(r"  finops_tier:.*", new_line, mtxt)
        else:
            mtxt = mtxt.rstrip() + "\n" + new_line + "\n"
        manifest_path.write_text(mtxt, encoding="utf-8")
        count += 1
    print(f"✅ Updated {count} agents/<id>/agents-cli-manifest.yaml files with exact per-agent cost & ROI metrics.")


def main() -> None:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    update_html_files(catalog)
    update_cost_presentation(catalog)
    update_manifests(catalog)


if __name__ == "__main__":
    main()

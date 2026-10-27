#!/usr/bin/env python3
"""Removes seat licensing calculations across the website and cost presentation,
keeping ONLY Cloud Infrastructure, Agent Invocation, and Gemini Token Costs
(Gemini 3.8 Flash & Gemini 3.1 Pro / 4 Argon via Dynamic Orchestrator Routing).
"""

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SIMPLE_INFRA_TOKEN_COST_PANEL_JS = r"""    /* =========================================================================
       SIMPLE AGENT COST DETAILS CARD (INFRA + INVOCATION + TOKEN COST ONLY)
       ========================================================================= */
    function renderAgentCostAndRoiPanel(ag, dept) {
      const cm = ag.costModel;
      if (!cm) return '';
      const mb = cm.monthlyBreakdown;
      const vm = cm.valueModel;
      const infraDataMo = (mb.computeUsd + mb.dataUsd + mb.apiUsd);

      return `
        <div class="simple-arch-card" style="margin-top: 22px; margin-bottom: 22px;">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
            <div>
              <div style="font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:4px;">
                Infra, Invocation &amp; Token Cost (Excl. Seat Licensing)
              </div>
              <h2 style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary); margin:0;">
                Cost Details — ${ag.name}
              </h2>
            </div>

            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="sc-tech-pill" style="border-color:${dept.color}55; color:${dept.color}; font-weight:700;">
                🧠 Orchestrator: Gemini 3.8 Flash ↔ 3.1 Pro / 4 Argon (subject to availability)
              </span>
              <span class="sc-tech-pill" style="font-weight:700;">
                ~${cm.eventsPerDay.toLocaleString()} invocations/day
              </span>
            </div>
          </div>

          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:14px;">
            <div style="padding:16px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-top:3px solid ${dept.color};">
              <div style="font-size:12px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                Monthly Infra + Token Cost
              </div>
              <div style="font-family:var(--font-display); font-size:26px; font-weight:800; color:var(--text-primary); margin:6px 0 2px;">
                $${mb.totalFsp3YrUsd.toFixed(0)} <span style="font-size:14px; font-weight:600; color:var(--text-secondary);">/ mo</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-secondary);">
                $${Math.round(mb.annualCloudFsp3YrUsd).toLocaleString()} / yr (3-Yr FSP · Pilot: $${mb.pilotScaleMoUsd.toFixed(0)}/mo)
              </div>
            </div>

            <div style="padding:16px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-top:3px solid ${dept.color};">
              <div style="font-size:12px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                LLM Token Invocation Cost
              </div>
              <div style="font-family:var(--font-display); font-size:26px; font-weight:800; color:var(--text-primary); margin:6px 0 2px;">
                $${mb.llmFsp3YrUsd.toFixed(0)} <span style="font-size:14px; font-weight:600; color:var(--text-secondary);">/ mo</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-secondary);">
                $${cm.tokens.tokenCostPer1kCallsUsd.toFixed(2)} / 1K token runs · 75% Cache Hit
              </div>
            </div>

            <div style="padding:16px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-top:3px solid ${dept.color};">
              <div style="font-size:12px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                Runtime &amp; Data Infra Cost
              </div>
              <div style="font-family:var(--font-display); font-size:26px; font-weight:800; color:var(--text-primary); margin:6px 0 2px;">
                $${infraDataMo.toFixed(0)} <span style="font-size:14px; font-weight:600; color:var(--text-secondary);">/ mo</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-secondary);">
                ADK Compute: $${mb.computeUsd.toFixed(0)} · BQ/API: $${(mb.dataUsd + mb.apiUsd).toFixed(0)}
              </div>
            </div>

            <div style="padding:16px 18px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-top:3px solid #10b981;">
              <div style="font-size:12px; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">
                Cost per 1,000 Invocations
              </div>
              <div style="font-family:var(--font-display); font-size:26px; font-weight:800; color:#10b981; margin:6px 0 2px;">
                $${mb.blendedCostPer1kCallsUsd.toFixed(2)} <span style="font-size:14px; font-weight:600; color:var(--text-secondary);">/ 1K</span>
              </div>
              <div style="font-size:12.5px; color:var(--text-secondary);">
                Est. Value: $${(vm.grossAnnualConservativeUsd / 1e6).toFixed(2)}M/yr (${vm.cloudRoiMultipleConservative}x ROI)
              </div>
            </div>
          </div>
        </div>
      `;
    }"""


def update_website_html_files() -> None:
    pattern = re.compile(
        r"    /\* =========================================================================\n"
        r"       SIMPLE AGENT COST DETAILS CARD[\s\S]*?function renderAgentCostAndRoiPanel\(ag, dept\) \{[\s\S]*?\n    \}",
        re.M,
    )
    for name in ["index.html", "periodic_table.html", "mind_map.html"]:
        p = ROOT / name
        if not p.exists():
            continue
        html = p.read_text(encoding="utf-8")
        if pattern.search(html):
            html = pattern.sub(lambda _: SIMPLE_INFRA_TOKEN_COST_PANEL_JS, html, count=1)
            p.write_text(html, encoding="utf-8")
            print(f"✅ Updated renderAgentCostAndRoiPanel in {name} (Infra + Invocation + Token Cost only).")


def update_cost_presentation() -> None:
    pres_path = ROOT / "cost_analysis_presentation.html"
    if not pres_path.exists():
        return
    html = pres_path.read_text(encoding="utf-8")

    # 1. Slide 1 KPI card & Cost Stack (Remove Seat Licensing, update to $22.1K/mo Infra + Token)
    old_slide1_kpi = """        <div class="card">
          <div class="kpi-label">Global Enterprise Run-Rate (Tier 3)</div>
          <div class="kpi-value" style="color: var(--accent-blue);">$46.1K<span style="font-size:16px;color:var(--text-muted);">/mo</span></div>
          <span class="badge badge-blue">$553.4K Annual TCO (w/ 3-Yr FSP)</span>
          <p class="kpi-foot">Full 60-Agent mesh, 5.0M monthly invocations, 15 TB BigQuery Twin, and 1,000 Gemini Enterprise seats.</p>
        </div>"""
    new_slide1_kpi = """        <div class="card">
          <div class="kpi-label">Global Infra &amp; Token Run-Rate (Tier 3)</div>
          <div class="kpi-value" style="color: var(--accent-blue);">$22.1K<span style="font-size:16px;color:var(--text-muted);">/mo</span></div>
          <span class="badge badge-blue">$265.4K Annual Run-Rate (w/ 3-Yr FSP)</span>
          <p class="kpi-foot">Full 60-Agent mesh, 5.0M monthly invocations, and 15 TB BigQuery Twin (pure infra &amp; token cost; excludes seat licensing).</p>
        </div>"""
    html = html.replace(old_slide1_kpi, new_slide1_kpi)

    old_slide1_stack = """        <div class="card">
          <div class="card-header">
            <div class="card-title">Monthly Enterprise Cost Stack (Tier 3: 5M Invocations/Mo · 60 Agents)</div>
            <span class="badge badge-blue">$46,120 / Month (3-Yr FSP) · $48,400 / Month (PayGo)</span>
          </div>
          <div style="margin-top: 14px;">
            <div class="calc-row">
              <div class="calc-label-row">
                <span>1. Gemini Enterprise (Agentspace) Named User Licenses (1,000 Planners/Buyers)</span>
                <span class="mono" style="color:#38bdf8;">$24,000 / mo (52.0%)</span>
              </div>
              <div class="bar-meter"><div class="bar-fill" style="width: 52.0%; background: #38bdf8;"></div></div>
            </div>
            <div class="calc-row">
              <div class="calc-label-row">
                <span>2. Vertex AI Gemini 3.8 Flash (85%) &amp; 2.5 Pro (15%) Token Inference (3-Yr FSP -20%)</span>
                <span class="mono" style="color:#10b981;">$9,120 / mo (19.8%)</span>
              </div>
              <div class="bar-meter"><div class="bar-fill" style="width: 19.8%; background: #10b981;"></div></div>
            </div>
            <div class="calc-row">
              <div class="calc-label-row">
                <span>3. Vertex AI Agent Engine (Reasoning Engine) Serverless Compute Pool</span>
                <span class="mono" style="color:#a855f7;">$6,800 / mo (14.7%)</span>
              </div>
              <div class="bar-meter"><div class="bar-fill" style="width: 14.7%; background: #a855f7;"></div></div>
            </div>
            <div class="calc-row" style="margin-bottom:0;">
              <div class="calc-label-row">
                <span>4. BigQuery Digital Twin (245 Tables) + Spanner Graph + Maps/Weather APIs</span>
                <span class="mono" style="color:#f59e0b;">$6,200 / mo (13.5%)</span>
              </div>
              <div class="bar-meter"><div class="bar-fill" style="width: 13.5%; background: #f59e0b;"></div></div>
            </div>
          </div>
        </div>"""
    new_slide1_stack = """        <div class="card">
          <div class="card-header">
            <div class="card-title">Monthly Infra, Invocation &amp; Token Cost Stack (Tier 3: 5M Invocations/Mo · 60 Agents)</div>
            <span class="badge badge-blue">$22,120 / Month (3-Yr FSP) · $24,400 / Month (PayGo)</span>
          </div>
          <div style="margin-top: 14px;">
            <div class="calc-row">
              <div class="calc-label-row">
                <span>1. Vertex AI Gemini 3.8 Flash (85%) &amp; 3.1 Pro / 4 Argon (15%) Token Inference (3-Yr FSP -20%)</span>
                <span class="mono" style="color:#10b981;">$9,120 / mo (41.2%)</span>
              </div>
              <div class="bar-meter"><div class="bar-fill" style="width: 41.2%; background: #10b981;"></div></div>
            </div>
            <div class="calc-row">
              <div class="calc-label-row">
                <span>2. Vertex AI Agent Engine (Reasoning Engine) Serverless Invocation &amp; Compute Pool</span>
                <span class="mono" style="color:#a855f7;">$6,800 / mo (30.7%)</span>
              </div>
              <div class="bar-meter"><div class="bar-fill" style="width: 30.7%; background: #a855f7;"></div></div>
            </div>
            <div class="calc-row" style="margin-bottom:0;">
              <div class="calc-label-row">
                <span>3. BigQuery Digital Twin (245 Tables) + Spanner Graph + Maps/Weather APIs</span>
                <span class="mono" style="color:#f59e0b;">$6,200 / mo (28.0%)</span>
              </div>
              <div class="bar-meter"><div class="bar-fill" style="width: 28.0%; background: #f59e0b;"></div></div>
            </div>
            <p class="kpi-foot" style="margin-top:12px;">Note: Focuses strictly on Cloud Infrastructure, Agent Invocation, and Gemini Token costs. User seat licensing is excluded as it depends on existing enterprise agreements.</p>
          </div>
        </div>"""
    html = html.replace(old_slide1_stack, new_slide1_stack)

    html = html.replace("$553.4K / yr (3-Yr FSP)", "$265.4K / yr (3-Yr FSP)")
    html = html.replace("123x ROI", "257x ROI")

    # 2. Slide 2 (4-Tier Scale Envelope)
    html = html.replace(
        "enterprises can start with a 10-agent regional pilot for <strong>$1,490/month in cloud infrastructure</strong> ($8,990/mo with 250 user seats) and scale linearly to 25M+ monthly autonomous ERP/IoT invocations.",
        "enterprises can start with a 10-agent regional pilot for <strong>$1,490/month in cloud &amp; token infrastructure</strong> and scale linearly to 25M+ monthly autonomous ERP/IoT invocations (seat licensing excluded).",
    )
    old_slide2_seats_row = """            <tr>
              <td><strong>Named Gemini Enterprise Users</strong></td>
              <td class="mono">250 Planners</td>
              <td class="mono">900 Planners</td>
              <td class="mono">1,000 Planners (+ ERP API)</td>
              <td class="mono">3,000 Global Users</td>
            </tr>\n"""
    html = html.replace(old_slide2_seats_row, "")

    old_slide2_totals = """            <tr>
              <td><strong>4. Gemini Enterprise Seat Licensing</strong><br><span style="font-size:11px;color:var(--text-muted);">Optional if using Headless API / Custom UI</span></td>
              <td class="mono">$7,500 / mo</td>
              <td class="mono">$24,300 / mo</td>
              <td class="mono" style="color:#34d399;font-weight:700;">$24,000 / mo</td>
              <td class="mono">$75,000 / mo</td>
            </tr>
            <tr style="background: rgba(16, 185, 129, 0.08);">
              <td><strong>TOTAL MONTHLY RUN-RATE (PayGo)</strong><br><span style="font-size:11px;color:var(--text-muted);">(Infrastructure-Only Run-Rate Excl. Seats)</span></td>
              <td class="mono" style="font-size:15px;font-weight:800;color:#38bdf8;">$8,990 / mo<br><span style="font-size:11px;color:#94a3b8;">($1,490/mo Infra-Only)</span></td>
              <td class="mono" style="font-size:15px;font-weight:800;color:#c084fc;">$31,850 / mo<br><span style="font-size:11px;color:#94a3b8;">($7,550/mo Infra-Only)</span></td>
              <td class="mono" style="font-size:15px;font-weight:800;color:#34d399;">$48,400 / mo<br><span style="font-size:11px;color:#94a3b8;">($24,400/mo Infra-Only)</span></td>
              <td class="mono" style="font-size:15px;font-weight:800;color:#fbbf24;">$158,700 / mo<br><span style="font-size:11px;color:#94a3b8;">($83,700/mo Infra-Only)</span></td>
            </tr>
            <tr>
              <td><strong>TOTAL ANNUALIZED SPEND (3-Yr FSP -20%)</strong></td>
              <td class="mono">$106,728 / yr</td>
              <td class="mono">$374,712 / yr</td>
              <td class="mono" style="color:#34d399;font-weight:700;">$553,440 / yr</td>
              <td class="mono">$1,802,400 / yr</td>
            </tr>"""
    new_slide2_totals = """            <tr style="background: rgba(16, 185, 129, 0.08);">
              <td><strong>TOTAL MONTHLY INFRA &amp; TOKEN RUN-RATE</strong><br><span style="font-size:11px;color:var(--text-muted);">(Pure Infra, Invocation &amp; Token Cost · Excl. Seats)</span></td>
              <td class="mono" style="font-size:15px;font-weight:800;color:#38bdf8;">$1,490 / mo<br><span style="font-size:11px;color:#34d399;">($1,394 w/ 3-Yr FSP)</span></td>
              <td class="mono" style="font-size:15px;font-weight:800;color:#c084fc;">$7,550 / mo<br><span style="font-size:11px;color:#34d399;">($6,926 w/ 3-Yr FSP)</span></td>
              <td class="mono" style="font-size:15px;font-weight:800;color:#34d399;">$24,400 / mo<br><span style="font-size:11px;color:#38bdf8;">($22,120 w/ 3-Yr FSP)</span></td>
              <td class="mono" style="font-size:15px;font-weight:800;color:#fbbf24;">$83,700 / mo<br><span style="font-size:11px;color:#34d399;">($75,200 w/ 3-Yr FSP)</span></td>
            </tr>
            <tr>
              <td><strong>TOTAL ANNUALIZED INFRA &amp; TOKEN SPEND (3-Yr FSP)</strong></td>
              <td class="mono">$16,728 / yr</td>
              <td class="mono">$83,112 / yr</td>
              <td class="mono" style="color:#34d399;font-weight:700;">$265,440 / yr</td>
              <td class="mono">$902,400 / yr</td>
            </tr>"""
    html = html.replace(old_slide2_totals, new_slide2_totals)

    # 3. Slide 6 (Pillar Allocation without seats)
    html = html.replace(
        "Breakdown of the <strong>$48,400/month (PayGo) / $46,120/month (3-Yr FSP)</strong> Enterprise Standard (Tier 3) investment",
        "Breakdown of the <strong>$24,400/month (PayGo) / $22,120/month (3-Yr FSP)</strong> pure Infrastructure, Invocation &amp; Token investment (excluding seat licensing)",
    )
    html = html.replace('<td class="mono">$7,850 / mo</td>\n              <td class="mono">$94.2K / yr</td>', '<td class="mono">$3,850 / mo</td>\n              <td class="mono">$46.2K / yr</td>')
    html = html.replace('<td class="mono">$8,420 / mo</td>\n              <td class="mono">$101.0K / yr</td>', '<td class="mono">$4,120 / mo</td>\n              <td class="mono">$49.4K / yr</td>')
    html = html.replace('<td class="mono">$8,190 / mo</td>\n              <td class="mono">$98.3K / yr</td>', '<td class="mono">$4,190 / mo</td>\n              <td class="mono">$50.3K / yr</td>')
    html = html.replace('<td class="mono">$7,940 / mo</td>\n              <td class="mono">$95.3K / yr</td>', '<td class="mono">$3,940 / mo</td>\n              <td class="mono">$47.3K / yr</td>')
    html = html.replace('<td class="mono">$9,680 / mo</td>\n              <td class="mono">$116.2K / yr</td>', '<td class="mono">$5,180 / mo</td>\n              <td class="mono">$62.2K / yr</td>')
    html = html.replace('<td class="mono">$6,320 / mo</td>\n              <td class="mono">$75.8K / yr</td>', '<td class="mono">$3,120 / mo</td>\n              <td class="mono">$37.4K / yr</td>')
    html = html.replace('<td class="mono" style="color:#38bdf8;font-weight:800;"><strong>$48,400 / mo</strong></td>\n              <td class="mono" style="color:#38bdf8;font-weight:800;"><strong>$580.8K / yr</strong></td>', '<td class="mono" style="color:#38bdf8;font-weight:800;"><strong>$24,400 / mo ($22.1K FSP)</strong></td>\n              <td class="mono" style="color:#38bdf8;font-weight:800;"><strong>$265.4K / yr (FSP)</strong></td>')

    # 4. Slide 8 Interactive Calculator (Remove rngSeats slider, tdSeatMo row, and JS seat math)
    old_calc_seat_slider = """          <div class="calc-row">
            <div class="calc-label-row">
              <span>6. Named Gemini Enterprise (Agentspace) Users</span>
              <span class="calc-val" id="lblSeats">1,000 Users</span>
            </div>
            <input type="range" id="rngSeats" min="0" max="5000" step="50" value="1000" oninput="updateCalculator()" />
          </div>

          <div class="calc-row" style="margin-bottom: 0;">
            <div class="calc-label-row">
              <span>7. Vertex AI Flexible Spending Plan (FSP Discount Tier)</span>"""
    new_calc_fsp_only = """          <div class="calc-row" style="margin-bottom: 0;">
            <div class="calc-label-row">
              <span>6. Vertex AI Flexible Spending Plan (FSP Discount Tier)</span>"""
    html = html.replace(old_calc_seat_slider, new_calc_fsp_only)

    old_calc_cards = """            <div style="background:rgba(15,23,42,0.9);padding:14px;border-radius:10px;border:1px solid var(--border-subtle);">
              <div class="kpi-label">Monthly Cloud + AI Infra</div>
              <div class="kpi-value" style="color:#38bdf8;font-size:26px;" id="outInfraMo">$22,120</div>
              <div class="kpi-foot" id="outUnitCost">$0.0044 / invocation</div>
            </div>
            <div style="background:rgba(15,23,42,0.9);padding:14px;border-radius:10px;border:1px solid var(--border-subtle);">
              <div class="kpi-label">Total Monthly (Incl. Seats)</div>
              <div class="kpi-value" style="color:#10b981;font-size:26px;" id="outTotalMo">$46,120</div>
              <div class="kpi-foot" id="outAnnualTco">$553,440 / year TCO</div>
            </div>"""
    new_calc_cards = """            <div style="background:rgba(15,23,42,0.9);padding:14px;border-radius:10px;border:1px solid var(--border-subtle);">
              <div class="kpi-label">Monthly Infra + Token Cost</div>
              <div class="kpi-value" style="color:#38bdf8;font-size:26px;" id="outInfraMo">$22,120</div>
              <div class="kpi-foot" id="outUnitCost">$0.0044 / invocation (Excl. Seats)</div>
            </div>
            <div style="background:rgba(15,23,42,0.9);padding:14px;border-radius:10px;border:1px solid var(--border-subtle);">
              <div class="kpi-label">Annual Infra + Token Run-Rate</div>
              <div class="kpi-value" style="color:#10b981;font-size:26px;" id="outTotalMo">$265,440</div>
              <div class="kpi-foot" id="outAnnualTco">Pure Cloud, Invocation &amp; Token Spend</div>
            </div>"""
    html = html.replace(old_calc_cards, new_calc_cards)

    old_calc_seat_row = """                <tr>
                  <td>Gemini Enterprise Named User Seats</td>
                  <td class="mono" id="tdSeatMo">$24,000</td>
                  <td class="mono" id="tdSeatYr">$288,000</td>
                  <td class="mono" id="tdSeatPct">52.0%</td>
                </tr>\n"""
    html = html.replace(old_calc_seat_row, "")

    old_calc_js = """      const bqTb = parseInt(document.getElementById('rngBq').value, 10);
      const seats = parseInt(document.getElementById('rngSeats').value, 10);
      const fspDiscount = parseInt(document.getElementById('selFsp').value, 10);

      const proPct = 100 - flashPct;

      document.getElementById('lblAgents').textContent = `${agents} Agent${agents > 1 ? 's' : ''}`;
      document.getElementById('lblCalls').textContent = `${calls.toLocaleString()} / mo`;
      document.getElementById('lblFlash').textContent = `${flashPct}% Flash / ${proPct}% Pro`;
      document.getElementById('lblCache').textContent = `${cachePct}% Cache Hit`;
      document.getElementById('lblBq').textContent = `${bqTb} TB`;
      document.getElementById('lblSeats').textContent = `${seats.toLocaleString()} Users`;
      document.getElementById('lblFsp').textContent = fspDiscount === 0 ? 'PayGo (0%)' : `${fspDiscount === 10 ? '1-Yr' : '3-Yr'} FSP (-${fspDiscount}%)`;

      // Token cost math
      const cacheDiscountFactor = 1 - (cachePct / 100) * 0.56;
      const fspFactor = 1 - (fspDiscount / 100);
      const flashCostPerCall = 0.00085 * cacheDiscountFactor * fspFactor;
      const proCostPerCall = 0.0195 * cacheDiscountFactor * fspFactor;

      const flashCalls = calls * (flashPct / 100);
      const proCalls = calls * (proPct / 100);
      const llmMo = Math.round(flashCalls * flashCostPerCall + proCalls * proCostPerCall);

      // Vertex AI Agent Engine runtime math (pooled across active agents + call volume)
      const reMo = Math.round(agents * 45 + (calls / 1000000) * 820);

      // BigQuery + Spanner + Maps math
      const dataMo = Math.round(bqTb * 210 + (calls / 1000000) * 610);

      // Seats math ($24/seat volume tier)
      const seatMo = seats * 24;

      const infraMo = llmMo + reMo + dataMo;
      const totalMo = infraMo + seatMo;
      const annualTco = totalMo * 12;
      const unitCost = calls > 0 ? (infraMo / calls) : 0;

      // Estimated value scales with active agents & invocation coverage
      const estAnnualValM = (agents / 60) * 68.2 * Math.min(1.6, Math.pow(calls / 5000000, 0.25));
      const estMoValM = estAnnualValM / 12;
      const roiMultiple = annualTco > 0 ? Math.round((estAnnualValM * 1000000) / annualTco) : 0;
      const paybackMonths = estMoValM > 0 ? ((annualTco / 1000000) / estMoValM).toFixed(1) : '0.0';

      document.getElementById('outInfraMo').textContent = `$${infraMo.toLocaleString()}`;
      document.getElementById('outUnitCost').textContent = `$${unitCost.toFixed(4)} / invocation (Infra)`;
      document.getElementById('outTotalMo').textContent = `$${totalMo.toLocaleString()}`;
      document.getElementById('outAnnualTco').textContent = `$${annualTco.toLocaleString()} / year Total TCO`;
      document.getElementById('calcRoiBadge').textContent = `${roiMultiple}x Blended ROI`;

      const fmtPct = (v) => totalMo > 0 ? ((v / totalMo) * 100).toFixed(1) + '%' : '0%';
      document.getElementById('tdLlmMo').textContent = `$${llmMo.toLocaleString()}`;
      document.getElementById('tdLlmYr').textContent = `$${(llmMo * 12).toLocaleString()}`;
      document.getElementById('tdLlmPct').textContent = fmtPct(llmMo);

      document.getElementById('tdReMo').textContent = `$${reMo.toLocaleString()}`;
      document.getElementById('tdReYr').textContent = `$${(reMo * 12).toLocaleString()}`;
      document.getElementById('tdRePct').textContent = fmtPct(reMo);

      document.getElementById('tdDataMo').textContent = `$${dataMo.toLocaleString()}`;
      document.getElementById('tdDataYr').textContent = `$${(dataMo * 12).toLocaleString()}`;
      document.getElementById('tdDataPct').textContent = fmtPct(dataMo);

      document.getElementById('tdSeatMo').textContent = `$${seatMo.toLocaleString()}`;
      document.getElementById('tdSeatYr').textContent = `$${(seatMo * 12).toLocaleString()}`;
      document.getElementById('tdSeatPct').textContent = fmtPct(seatMo);

      document.getElementById('tdValMo').textContent = `$${estMoValM.toFixed(2)}M / mo`;
      document.getElementById('tdValYr').textContent = `$${estAnnualValM.toFixed(1)}M / yr`;
      document.getElementById('tdPayback').textContent = `Payback: ${paybackMonths} mo`;
    }

    function resetCalculator() {
      document.getElementById('rngAgents').value = 60;
      document.getElementById('rngCalls').value = 5000000;
      document.getElementById('rngFlash').value = 85;
      document.getElementById('rngCache').value = 75;
      document.getElementById('rngBq').value = 15;
      document.getElementById('rngSeats').value = 1000;
      document.getElementById('selFsp').value = '20';
      updateCalculator();
    }"""

    new_calc_js = """      const bqTb = parseInt(document.getElementById('rngBq').value, 10);
      const fspDiscount = parseInt(document.getElementById('selFsp').value, 10);

      const proPct = 100 - flashPct;

      document.getElementById('lblAgents').textContent = `${agents} Agent${agents > 1 ? 's' : ''}`;
      document.getElementById('lblCalls').textContent = `${calls.toLocaleString()} / mo`;
      document.getElementById('lblFlash').textContent = `${flashPct}% 3.8 Flash / ${proPct}% 3.1 Pro·4 Argon`;
      document.getElementById('lblCache').textContent = `${cachePct}% Cache Hit`;
      document.getElementById('lblBq').textContent = `${bqTb} TB`;
      document.getElementById('lblFsp').textContent = fspDiscount === 0 ? 'PayGo (0%)' : `${fspDiscount === 10 ? '1-Yr' : '3-Yr'} FSP (-${fspDiscount}%)`;

      // Token cost math (Dynamic Agent Orchestrator Routing: Gemini 3.8 Flash + Gemini 3.1 Pro / 4 Argon)
      const cacheDiscountFactor = 1 - (cachePct / 100) * 0.56;
      const fspFactor = 1 - (fspDiscount / 100);
      const flashCostPerCall = 0.00085 * cacheDiscountFactor * fspFactor;
      const proCostPerCall = 0.0195 * cacheDiscountFactor * fspFactor;

      const flashCalls = calls * (flashPct / 100);
      const proCalls = calls * (proPct / 100);
      const llmMo = Math.round(flashCalls * flashCostPerCall + proCalls * proCostPerCall);

      // Vertex AI Agent Engine runtime math (pooled across active agents + call volume)
      const reMo = Math.round(agents * 45 + (calls / 1000000) * 820);

      // BigQuery + Spanner + Maps math
      const dataMo = Math.round(bqTb * 210 + (calls / 1000000) * 610);

      // Pure Infra, Invocation & Token cost (Seat licensing excluded)
      const infraMo = llmMo + reMo + dataMo;
      const totalMo = infraMo;
      const annualTco = totalMo * 12;
      const unitCost = calls > 0 ? (infraMo / calls) : 0;

      // Estimated value scales with active agents & invocation coverage
      const estAnnualValM = (agents / 60) * 68.2 * Math.min(1.6, Math.pow(calls / 5000000, 0.25));
      const estMoValM = estAnnualValM / 12;
      const roiMultiple = annualTco > 0 ? Math.round((estAnnualValM * 1000000) / annualTco) : 0;
      const paybackMonths = estMoValM > 0 ? ((annualTco / 1000000) / estMoValM).toFixed(1) : '0.0';

      document.getElementById('outInfraMo').textContent = `$${infraMo.toLocaleString()}`;
      document.getElementById('outUnitCost').textContent = `$${unitCost.toFixed(4)} / invocation (Excl. Seats)`;
      document.getElementById('outTotalMo').textContent = `$${annualTco.toLocaleString()}`;
      document.getElementById('outAnnualTco').textContent = `Pure Cloud, Invocation & Token Spend / yr`;
      document.getElementById('calcRoiBadge').textContent = `${roiMultiple}x Cloud ROI`;

      const fmtPct = (v) => totalMo > 0 ? ((v / totalMo) * 100).toFixed(1) + '%' : '0%';
      document.getElementById('tdLlmMo').textContent = `$${llmMo.toLocaleString()}`;
      document.getElementById('tdLlmYr').textContent = `$${(llmMo * 12).toLocaleString()}`;
      document.getElementById('tdLlmPct').textContent = fmtPct(llmMo);

      document.getElementById('tdReMo').textContent = `$${reMo.toLocaleString()}`;
      document.getElementById('tdReYr').textContent = `$${(reMo * 12).toLocaleString()}`;
      document.getElementById('tdRePct').textContent = fmtPct(reMo);

      document.getElementById('tdDataMo').textContent = `$${dataMo.toLocaleString()}`;
      document.getElementById('tdDataYr').textContent = `$${(dataMo * 12).toLocaleString()}`;
      document.getElementById('tdDataPct').textContent = fmtPct(dataMo);

      document.getElementById('tdValMo').textContent = `$${estMoValM.toFixed(2)}M / mo`;
      document.getElementById('tdValYr').textContent = `$${estAnnualValM.toFixed(1)}M / yr`;
      document.getElementById('tdPayback').textContent = `Payback: ${paybackMonths} mo`;
    }

    function resetCalculator() {
      document.getElementById('rngAgents').value = 60;
      document.getElementById('rngCalls').value = 5000000;
      document.getElementById('rngFlash').value = 85;
      document.getElementById('rngCache').value = 75;
      document.getElementById('rngBq').value = 15;
      document.getElementById('selFsp').value = '20';
      updateCalculator();
    }"""

    html = html.replace(old_calc_js, new_calc_js)
    pres_path.write_text(html, encoding="utf-8")
    print("✅ Updated cost_analysis_presentation.html to exclude seat costs and calculate only Infra, Invocation & Token costs.")


def sync_distribution_copies() -> None:
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
    update_website_html_files()
    update_cost_presentation()
    sync_distribution_copies()


if __name__ == "__main__":
    main()

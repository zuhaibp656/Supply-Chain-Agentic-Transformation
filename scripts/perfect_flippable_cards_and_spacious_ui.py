#!/usr/bin/env python3
"""
Enhances the 9bd8b2b Flippable Cards (.sc-flip-card) view across index.html,
periodic_table.html, and mind_map.html:
1. Preserves 100% of the 3D Flippable Cards (.sc-flip-card) and 6-Tab Single-Button Spec Switcher
   from 9bd8b2b across Agent, Blueprint, Persona, Process Journey, and Architecture pages.
2. Upgrades .sc-flip-card CSS to use a CSS Grid overlay (grid-template-areas: "flipface") so
   flippable cards auto-size to fit both front and back content with ZERO text clipping, bigger
   readable typography (21px headings, 15.5px back text, 22px 24px padding, 18px border-radius),
   and responsive grid columns for .ag-flow-steps-grid.
3. Restores the full Enterprise Agent Contract details inside Tab 01 (Playbook & Governance)
   and removes mid-sentence shortSentence() truncations on the back of flippable cards across
   Tabs 01–06 so zero contract information is lost while keeping the page clean.
4. Fixes all sharp corners (.agent-plug-btn "Open ... & Demo ->", .time-badge, .toil-badge,
   .improve-badge, .journey-accordion-header, etc.) with smooth mild rounded edges, and makes
   the Persona Day-to-Day Life comparison big, readable (16px), spacious, and untruncated.
"""

from pathlib import Path

ROOT = Path("/usr/local/google/home/zuhaibp/Supply_chain_Agentic_Transformation")
HTML_FILES = [
    ROOT / "index.html",
    ROOT / "periodic_table.html",
    ROOT / "mind_map.html",
]

OLD_FLIP_CSS = """    /* =========================================================================
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
    }"""

NEW_FLIP_AND_ROUNDED_CSS = """    /* =========================================================================
       3D FLIPPABLE CARDS (.sc-flip-card) — AUTO-HEIGHT, ZERO CLIPPING, SPACIOUS & ROUNDED
       ========================================================================= */
    .sc-flip-card {
      perspective: 1200px;
      cursor: pointer;
      user-select: none;
      min-height: 196px;
      position: relative;
      border-radius: 18px;
    }
    .sc-flip-card.sc-flip-tall {
      min-height: 224px;
    }
    .sc-flip-card.sc-flip-compact {
      min-height: 176px;
    }
    .sc-flip-inner {
      display: grid;
      grid-template-areas: "flipface";
      width: 100%;
      height: 100%;
      min-height: inherit;
      transition: transform 0.52s cubic-bezier(0.22, 1, 0.36, 1);
      transform-style: preserve-3d;
      border-radius: 18px;
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
      backface-visibility: hidden;
      -webkit-backface-visibility: hidden;
      border-radius: 18px !important;
      padding: 22px 24px;
      background: var(--bg-elevated);
      border: 1.5px solid var(--border-subtle);
      border-top: 4px solid var(--flip-accent, #38bdf8);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 12px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.16);
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
      box-sizing: border-box;
    }
    html[data-theme="light"] .sc-flip-front,
    html[data-theme="light"] .sc-flip-back {
      background: #ffffff;
      border-color: rgba(15, 23, 42, 0.12);
      border-top: 4px solid var(--flip-accent, #2563eb);
      box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
    }
    .sc-flip-card:hover .sc-flip-front,
    .sc-flip-card:hover .sc-flip-back {
      border-color: var(--flip-accent, #38bdf8);
      box-shadow: 0 14px 30px rgba(0, 0, 0, 0.24);
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
      flex-wrap: wrap;
    }
    .sc-flip-kicker {
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      color: var(--flip-accent, #38bdf8);
    }
    .sc-flip-hint {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 999px;
      background: rgba(148, 163, 184, 0.12);
      color: var(--text-secondary);
      border: 1px solid var(--border-subtle);
      white-space: nowrap;
    }
    .sc-flip-big-heading {
      font-family: var(--font-display);
      font-size: 21px;
      font-weight: 800;
      color: var(--text-primary);
      line-height: 1.28;
      margin: 6px 0;
      display: flex;
      align-items: center;
      gap: 14px;
      overflow-wrap: break-word;
      word-break: normal;
    }
    .sc-flip-icon-box {
      width: 44px;
      height: 44px;
      border-radius: 13px;
      background: rgba(148, 163, 184, 0.1);
      border: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 21px;
      flex-shrink: 0;
    }
    .sc-flip-back-text {
      font-size: 15.5px;
      font-weight: 600;
      color: var(--text-primary);
      line-height: 1.65;
      margin: 6px 0;
      overflow-wrap: break-word;
    }
    .sc-flip-bottom-pills {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .sc-flip-pill {
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      padding: 5px 12px;
      border-radius: 999px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      max-width: 100%;
      overflow-wrap: anywhere;
    }

    /* Responsive 5-step Execution Flow grid so cards never clip horizontally */
    .ag-flow-steps-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(235px, 1fr)) !important;
      gap: 16px !important;
      margin-top: 18px !important;
    }

    /* Universal Mild Rounded Edges & Spacious Persona Day-to-Day Comparison */
    .agent-plug-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      border-radius: 12px !important;
      padding: 11px 20px;
      font-family: var(--font-sans);
      font-size: 14px;
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
      box-shadow: 0 8px 20px rgba(37, 99, 246, 0.28);
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
    }
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
    }"""


def update_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    # 1. Replace OLD_FLIP_CSS with NEW_FLIP_AND_ROUNDED_CSS
    assert OLD_FLIP_CSS in text, f"OLD_FLIP_CSS not found in {path}"
    text = text.replace(OLD_FLIP_CSS, NEW_FLIP_AND_ROUNDED_CSS, 1)

    # 2. Remove mid-sentence shortSentence() truncations inside Flippable Cards on Agent Hero & Spec Tabs
    text = text.replace(
        '<div class="sc-flip-back-text">${shortSentence(ag.problem, 105)}</div>',
        '<div class="sc-flip-back-text">${ag.problem}</div>'
    )
    text = text.replace(
        '<div class="sc-flip-back-text">${shortSentence(ag.solution, 105)}</div>',
        '<div class="sc-flip-back-text">${ag.solution}</div>'
    )
    text = text.replace(
        '<div class="sc-flip-back-text">${shortSentence(ag.outcome, 105)}</div>',
        '<div class="sc-flip-back-text">${ag.outcome}</div>'
    )
    text = text.replace(
        '<div class="sc-flip-back-text">${shortSentence(toOpenTechLabel(sub.role), 100)}</div>',
        '<div class="sc-flip-back-text">${toOpenTechLabel(sub.role)}</div>'
    )
    text = text.replace(
        '<div class="sc-flip-back-text">${shortSentence(t.description, 95)}</div>',
        '<div class="sc-flip-back-text">${t.description}</div>'
    )
    text = text.replace(
        '<div class="sc-flip-back-text">“${shortSentence(evalObj.query, 105)}”</div>',
        '<div class="sc-flip-back-text">“${evalObj.query}”</div>'
    )
    text = text.replace(
        '<div class="sc-flip-back-text">${shortSentence(ag.solution || ag.role, 100)}</div>',
        '<div class="sc-flip-back-text">${ag.solution || ag.role}</div>'
    )
    text = text.replace(
        '<div class="sc-flip-back-text">${shortSentence(activeStage.after, 95)}</div>',
        '<div class="sc-flip-back-text">${activeStage.after}</div>'
    )
    text = text.replace(
        '<div class="sc-flip-back-text">${shortSentence(activeStage.goldenThread, 95)}</div>',
        '<div class="sc-flip-back-text">${activeStage.goldenThread}</div>'
    )
    text = text.replace(
        'backText: shortSentence(subs[0].role, 88),',
        'backText: subs[0].role,'
    )
    text = text.replace(
        'backText: shortSentence(`${subs[1].role} using ${solverLabel}.`, 88),',
        'backText: `${subs[1].role} using ${solverLabel}.`,'
    )
    text = text.replace(
        '<strong>Solver:</strong> ${shortSentence(toOpenTechLabel(ag.solverStack || \'Vertex AI + BigQuery ML\'), 60)}',
        '<strong>Solver:</strong> ${toOpenTechLabel(ag.solverStack || \'Vertex AI + BigQuery ML\')}'
    )

    # 3. In Tab 01 (Playbook & Governance), keep the 4 Big-Heading Flippable Cards AND add the full
    #    Enterprise Agent Contract details (Scope Lists, 4-Row Escalation Rules Table, Guardrails & Evidence)
    #    right underneath inside Tab 01 so zero contract information is lost!
    old_tab01_end = """                    <div class="sc-flip-bottom-pills">
                      ${tables.slice(0, 2).map(t => `<span class="sc-flip-pill">${t.table_name}</span>`).join('')}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- TAB 02: WORKFLOW (3 Big-Heading Flippable Stage Cards) -->"""

    new_tab01_end = """                    <div class="sc-flip-bottom-pills">
                      ${tables.slice(0, 2).map(t => `<span class="sc-flip-pill">${t.table_name}</span>`).join('')}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Full Enterprise Agent Contract Details Preserved Inside Tab 01 -->
            <div style="margin-top: 22px; display: flex; flex-direction: column; gap: 16px;">
              <details class="sc-spec-sub-drawer" open>
                <summary>
                  <span>🛡️ 1A · Full Role Mandate &amp; Autonomous Scope (In-Scope vs. Out-of-Scope)</span>
                  <span class="sc-sub-toggle-hint"></span>
                </summary>
                <div class="sc-spec-sub-drawer-body">
                  <p style="font-size:15.5px; color:var(--text-primary); line-height:1.68; margin:0 0 16px;">
                    <strong>Role Mandate:</strong> Autonomous <strong>${personaName}</strong> agent for the <strong>${cleanName}</strong> workflow in <strong>${subPillar}</strong>. ${ag.solution} ${ag.advantage || ag.outcome}
                  </p>
                  <div class="sc-spec-scope-grid">
                    <div class="sc-spec-scope-col scope-in" style="padding:18px 22px; border-radius:14px;">
                      <div style="font-family:var(--font-mono); font-size:12px; font-weight:800; text-transform:uppercase; color:#10b981; letter-spacing:0.06em; margin-bottom:10px;">
                        ✓ In Scope (Autonomous Execution)
                      </div>
                      <ul class="sc-spec-scope-list" style="font-size:15px; line-height:1.68;">
                        <li>${ag.solution}</li>
                        <li>Multi-table evidence synthesis across ${tables.map(t => `<code class="sc-spec-code">${t.table_name}</code>`).join(' ')} using <strong>${toOpenTechLabel(ag.solverStack || 'Time-Series & Mathematical Optimization Engine')}</strong>.</li>
                        <li>Governed write-back execution via <strong>${toOpenTechLabel(ag.apiWriteback || 'Signed MCP / REST / On-Prem ERP Connector')}</strong> with deterministic <code class="sc-spec-code">idempotency_key</code> audit logging.</li>
                      </ul>
                    </div>
                    <div class="sc-spec-scope-col scope-out" style="padding:18px 22px; border-radius:14px;">
                      <div style="font-family:var(--font-mono); font-size:12px; font-weight:800; text-transform:uppercase; color:#f43f5e; letter-spacing:0.06em; margin-bottom:10px;">
                        ✕ Out of Scope (Human Authority Retained)
                      </div>
                      <ul class="sc-spec-scope-list" style="font-size:15px; line-height:1.68;">
                        <li>Unapproved capital expenditure, legal contract termination, or policy overrides outside ${personaName} delegation limits.</li>
                        <li>Direct database mutations bypassing <code class="sc-spec-code">enforce_tool_contract()</code> or missing mandatory <code class="sc-spec-code">idempotency_key</code> tokens.</li>
                        <li>Executing external ERP/WMS write-backs when source telemetry exceeds staleness thresholds without human confirmation.</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </details>

              <details class="sc-spec-sub-drawer" open>
                <summary>
                  <span>🚦 1B · Escalation Rules &amp; Pre-Execution Quality Gates (4 Governed Triggers)</span>
                  <span class="sc-sub-toggle-hint"></span>
                </summary>
                <div class="sc-spec-sub-drawer-body">
                  <div class="sc-spec-table-wrap">
                    <table class="sc-spec-table">
                      <thead>
                        <tr>
                          <th style="width:38%;">Trigger Condition</th>
                          <th style="width:20%;">Gate Action</th>
                          <th>Governance Rationale</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td style="font-size:14.5px; line-height:1.6;">Financial or volume impact exceeds <strong>${personaName}</strong> autonomous threshold (&gt;20% variance vs. baseline plan)</td>
                          <td><span class="sc-spec-code action-code">escalate_to_human</span></td>
                          <td style="font-size:14.5px; line-height:1.6; color:var(--text-secondary);">High-magnitude supply chain reallocations require human sign-off in Control Tower before ERP commit.</td>
                        </tr>
                        <tr>
                          <td style="font-size:14.5px; line-height:1.6;">Mutation call to <code class="sc-spec-code">${writeToolNames}</code> missing required contract fields</td>
                          <td><span class="sc-spec-code">request_more_info</span></td>
                          <td style="font-size:14.5px; line-height:1.6; color:var(--text-secondary);">Enforced by <code class="sc-spec-code">enforce_tool_contract()</code> in <code class="sc-spec-code">agents/${ag.id}/app/agent.py</code> to prevent partial ERP writes.</td>
                        </tr>
                        <tr>
                          <td style="font-size:14.5px; line-height:1.6;">Mutation call lacks a non-empty <code class="sc-spec-code">idempotency_key</code> or attempts duplicate replay</td>
                          <td><span class="sc-spec-code">request_confirmation</span></td>
                          <td style="font-size:14.5px; line-height:1.6; color:var(--text-secondary);">Guarantees exactly-once execution across Enterprise ERP (MCP / On-Prem DB), IBP, WMS, and TMS connectors.</td>
                        </tr>
                        <tr>
                          <td style="font-size:14.5px; line-height:1.6;">Proposed action contradicts physical constraints or lacks corroborating records across at least 2 tables</td>
                          <td><span class="sc-spec-code action-code">refuse / reject_mutation</span></td>
                          <td style="font-size:14.5px; line-height:1.6; color:var(--text-secondary);">Single-source or unverified assertions cannot trigger production state changes.</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </details>

              <details class="sc-spec-sub-drawer" open>
                <summary>
                  <span>🔒 1C · Hard Guardrails &amp; Source-Table Evidence Requirements</span>
                  <span class="sc-sub-toggle-hint"></span>
                </summary>
                <div class="sc-spec-sub-drawer-body">
                  <ul class="sc-spec-scope-list" style="font-size:15px; line-height:1.68; margin:0;">
                    <li>Never fabricate SKU quantities, lead times, or financial metrics; cite exact rows from ${tables.slice(0, 2).map(t => `<code class="sc-spec-code">${t.table_name}</code>`).join(' & ')}.</li>
                    <li>Never bypass <code class="sc-spec-code">enforce_tool_contract()</code> before invoking ${actionTools.map(t => `<code class="sc-spec-code action-code">${t.name}</code>`).join(' ') || 'write tools'}.</li>
                    <li>Append every executed mutation to immutable audit trail <code class="sc-spec-code ev-code">artifacts/action-events.jsonl</code>.</li>
                    <li>Route routine operational queries to <strong>Gemini 3.8 Flash</strong> and escalate multi-echelon trade-offs to <strong>Gemini 3.1 Pro / 4 Argon</strong>.</li>
                  </ul>
                </div>
              </details>
            </div>
          </div>

          <!-- TAB 02: WORKFLOW (3 Big-Heading Flippable Stage Cards) -->"""

    assert old_tab01_end in text, f"old_tab01_end not found in {path}"
    text = text.replace(old_tab01_end, new_tab01_end, 1)

    # 4. In openPersonaPage, open the first 2 toil tasks by default and make the Day-to-Day Life
    #    Comparison text full (no shortSentence truncation), big (16px), and spacious, while keeping
    #    the Flippable AI Agent Cards at the bottom!
    old_persona_journey = """      // Open the first toil step by default; rest open on click
      let firstToilOpened = true;"""
    new_persona_journey = """      // Open the first toil step by default so the Day-to-Day comparison is immediately visible
      let firstToilOpened = false;"""
    assert old_persona_journey in text, f"old_persona_journey not found in {path}"
    text = text.replace(old_persona_journey, new_persona_journey, 1)

    text = text.replace(
        '<div class="toil-text" style="font-size:14.5px; line-height:1.58;">${shortSentence(slot.before, 220)}</div>',
        '<div class="toil-text">${slot.before}</div>'
    )
    text = text.replace(
        '<div class="improve-text" style="font-size:14.5px; line-height:1.58;">${shortSentence(slot.after, 220)}</div>',
        '<div class="improve-text">${slot.after}</div>'
    )
    text = text.replace(
        '<div style="font-size:13.5px; color:var(--text-secondary); line-height:1.45;">\n                                ${shortSentence(plugAgent.solution || plugAgent.role, 155)}\n                              </div>',
        '<div style="font-size:15.5px; color:var(--text-secondary); line-height:1.68;">\n                                ${plugAgent.solution || plugAgent.role}\n                              </div>'
    )
    text = text.replace(
        '<div style="padding-top:12px; font-size:14.5px; line-height:1.58; color:var(--text-secondary);">\n                        ${shortSentence(slot.activity, 200)}\n                      </div>',
        '<div style="padding-top:16px; font-size:16px; line-height:1.72; color:var(--text-secondary);">\n                        ${slot.activity}\n                      </div>'
    )

    path.write_text(text, encoding="utf-8")
    print(f"Updated {path.name} successfully")


if __name__ == "__main__":
    for f in HTML_FILES:
        update_file(f)

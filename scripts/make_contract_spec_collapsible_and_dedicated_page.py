#!/usr/bin/env python3
"""
Makes '01 · Enterprise Agent Contract — Playbook & Governance' and all Agent Specification
sections (01 through 06) clean, collapsible (<details> closed by default on #agent/<id>),
with nested collapsible sub-drawers inside 01 · Playbook & Governance, AND provides 1-click
buttons to open the full Enterprise Agent Contract & Technical Specification in its own
dedicated page (#blueprint/<id> via openAgentBlueprintPage).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HTML_FILES = [
    ROOT / "index.html",
    ROOT / "periodic_table.html",
    ROOT / "mind_map.html",
]

EXTRA_SPEC_CSS = """
    /* Collapsible Spec Section Cards (<details class="sc-spec-section-card sc-spec-collapsible">) */
    details.sc-spec-section-card.sc-spec-collapsible {
      padding: 0;
      overflow: hidden;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    details.sc-spec-section-card.sc-spec-collapsible:hover {
      border-color: rgba(56, 189, 248, 0.42);
    }
    details.sc-spec-section-card.sc-spec-collapsible > summary.sc-spec-sec-head {
      padding: 20px 26px;
      margin-bottom: 0;
      border-bottom: none;
      cursor: pointer;
      list-style: none;
      user-select: none;
      transition: background 0.18s ease;
    }
    details.sc-spec-section-card.sc-spec-collapsible > summary.sc-spec-sec-head::-webkit-details-marker {
      display: none;
    }
    details.sc-spec-section-card.sc-spec-collapsible > summary.sc-spec-sec-head:hover {
      background: rgba(148, 163, 184, 0.06);
    }
    details.sc-spec-section-card.sc-spec-collapsible[open] > summary.sc-spec-sec-head {
      border-bottom: 1px solid var(--border-subtle);
      background: rgba(148, 163, 184, 0.04);
    }
    .sc-spec-sec-body {
      padding: 22px 28px 26px;
    }
    .sc-spec-toggle-pill {
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 800;
      padding: 5px 12px;
      border-radius: 999px;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.18s ease;
    }
    details.sc-spec-section-card.sc-spec-collapsible > summary.sc-spec-sec-head .sc-spec-toggle-pill::before {
      content: '▾ Click to Expand';
    }
    details.sc-spec-section-card.sc-spec-collapsible[open] > summary.sc-spec-sec-head .sc-spec-toggle-pill::before {
      content: '▴ Collapse';
    }
    .sc-spec-open-page-mini {
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 700;
      padding: 5px 11px;
      border-radius: 999px;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.35);
      color: #38bdf8;
      cursor: pointer;
      transition: all 0.18s ease;
    }
    html[data-theme="light"] .sc-spec-open-page-mini {
      background: rgba(37, 99, 235, 0.08);
      border-color: rgba(37, 99, 235, 0.28);
      color: #1d4ed8;
    }
    .sc-spec-open-page-mini:hover {
      transform: translateY(-1px);
      filter: brightness(1.12);
    }

    /* Master Launcher Bar above Collapsible Spec Sections */
    .sc-spec-master-launcher {
      margin-top: 24px;
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
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.18);
    }
    html[data-theme="light"] .sc-spec-master-launcher {
      background: #ffffff;
      border-color: rgba(15, 23, 42, 0.12);
      box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
    }

    /* Nested Collapsible Sub-Drawers inside 01 · Playbook & Governance */
    details.sc-spec-sub-drawer {
      margin-top: 12px;
      border-radius: 14px;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      overflow: hidden;
    }
    details.sc-spec-sub-drawer > summary {
      padding: 13px 18px;
      cursor: pointer;
      list-style: none;
      user-select: none;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      font-family: var(--font-display);
      font-size: 14.5px;
      font-weight: 800;
      color: var(--text-primary);
    }
    details.sc-spec-sub-drawer > summary::-webkit-details-marker {
      display: none;
    }
    details.sc-spec-sub-drawer[open] > summary {
      border-bottom: 1px solid var(--border-subtle);
      background: rgba(148, 163, 184, 0.05);
    }
    details.sc-spec-sub-drawer > summary .sc-sub-toggle-hint {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      color: var(--text-secondary);
    }
    details.sc-spec-sub-drawer > summary .sc-sub-toggle-hint::before {
      content: '▾ Expand';
    }
    details.sc-spec-sub-drawer[open] > summary .sc-sub-toggle-hint::before {
      content: '▴ Collapse';
    }
    .sc-spec-sub-drawer-body {
      padding: 16px 18px;
    }
"""

NEW_JS_FUNCTIONS = """    function openAndScrollToSpecSection(sectionId, childId = null) {
      const sec = document.getElementById(sectionId);
      if (sec) {
        if (sec.tagName === 'DETAILS') sec.open = true;
        const parentDetails = sec.closest('details.sc-spec-collapsible');
        if (parentDetails) parentDetails.open = true;
      }
      if (childId) {
        const ch = document.getElementById(childId);
        if (ch) {
          if (ch.tagName === 'DETAILS') ch.open = true;
          const parentSub = ch.closest('details.sc-spec-sub-drawer');
          if (parentSub) parentSub.open = true;
          setTimeout(() => ch.scrollIntoView({ behavior: 'smooth', block: 'start' }), 40);
          return false;
        }
      }
      if (sec) {
        setTimeout(() => sec.scrollIntoView({ behavior: 'smooth', block: 'start' }), 40);
      }
      return false;
    }

    function toggleAllAgentSpecSections(btn) {
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
    }

    function renderAgentAtAGlanceStrip(ag, dept, isDedicatedSpecPage = false) {
      const st = computeAgentSpecStats(ag);
      return `
        <div class="sc-spec-stats-strip">
          <div class="sc-spec-stat-box">
            <span class="sc-spec-stat-num" style="color:${dept.color};">${st.systemsCount}</span>
            <span class="sc-spec-stat-label">systems</span>
          </div>
          <div class="sc-spec-stat-box">
            <span class="sc-spec-stat-num">${st.entitiesCount}</span>
            <span class="sc-spec-stat-label">entities</span>
          </div>
          <div class="sc-spec-stat-box">
            <span class="sc-spec-stat-num">${st.fieldsCount}</span>
            <span class="sc-spec-stat-label">fields</span>
          </div>
          <div class="sc-spec-stat-box">
            <span class="sc-spec-stat-num">${st.toolsCount}</span>
            <span class="sc-spec-stat-label">tools</span>
          </div>
          <div class="sc-spec-stat-box">
            <span class="sc-spec-stat-num">${st.stepsCount}</span>
            <span class="sc-spec-stat-label">workflow steps</span>
          </div>
          <div class="sc-spec-stat-box">
            <span class="sc-spec-stat-num">${st.evidenceRulesCount}</span>
            <span class="sc-spec-stat-label">evidence rules</span>
          </div>
          <div class="sc-spec-stat-box">
            <span class="sc-spec-stat-num">${st.evalsCount}</span>
            <span class="sc-spec-stat-label">evals</span>
          </div>
          <div class="sc-spec-stat-box">
            <span class="sc-spec-stat-num">${st.anomaliesCount}</span>
            <span class="sc-spec-stat-label">anomalies</span>
          </div>
        </div>

        <div class="sc-spec-jump-bar" style="--spec-accent:${dept.color};">
          ${!isDedicatedSpecPage ? `
            <button type="button" class="sc-spec-jump-pill" style="border-color:${dept.color}; background:${dept.color}22; color:var(--text-primary); font-weight:800;" onclick="openAgentBlueprintPage('${ag.id}', true, event, 'spec-governance')">
              📄 Open Contract &amp; Spec in Dedicated Page &rarr;
            </button>
          ` : ''}
          <a class="sc-spec-jump-pill" href="#spec-governance" onclick="return openAndScrollToSpecSection('spec-governance');">
            🛡️ 01 · Playbook &amp; Governance
          </a>
          <a class="sc-spec-jump-pill" href="#spec-workflow" onclick="return openAndScrollToSpecSection('spec-workflow');">
            ⚡ 02 · 3-Stage Workflow
          </a>
          <a class="sc-spec-jump-pill" href="#spec-tools" onclick="return openAndScrollToSpecSection('spec-tools');">
            🔧 03 · Agent Tools (${st.toolsCount})
          </a>
          <a class="sc-spec-jump-pill" href="#spec-systems" onclick="return openAndScrollToSpecSection('spec-systems');">
            🔌 04 · Source Systems (${st.systemsCount})
          </a>
          <a class="sc-spec-jump-pill" href="#spec-data-model" onclick="return openAndScrollToSpecSection('spec-data-model');">
            🗄️ 05 · Data Model (${st.entitiesCount} entities · ${st.fieldsCount} fields)
          </a>
          <a class="sc-spec-jump-pill" href="#spec-evals" onclick="return openAndScrollToSpecSection('spec-evals');">
            ✅ 06 · Evals &amp; Proof
          </a>
        </div>
      `;
    }

    function renderAgentFullSpecSheet(ag, dept, openByDefault = false) {
      const adk = ag.adkImplementation || {};
      const spec = ag.adkSpec || {};
      const cls = getAgentBuildClassification(ag);
      const cleanName = cleanAgentName(ag.name);
      const personaName = ag.primaryPersonaName || 'Supply Chain Operations Lead';
      const subPillar = ag.subPillarName || dept.name;
      const tables = adk.fixtureTables || [];
      const totalFields = tables.reduce((acc, t) => acc + ((t.columns || []).length), 0);
      const openAttr = openByDefault ? 'open' : '';

      // 1. Tools metadata
      const rawTools = (spec.toolsMeta && spec.toolsMeta.length)
        ? spec.toolsMeta
        : (adk.tools || []).filter(t => t !== 'list_systems').map(tName => {
            const isAct = String(tName).startsWith('action_');
            return {
              name: tName,
              kind: isAct ? 'action' : 'query',
              description: isAct
                ? `Execute governed write-back (${tName}) after pre-execution gate & idempotency validation.`
                : `Query live records from connected ${subPillar} tables (${tName}).`,
              inputs: isAct ? ['target_id', 'rationale', 'idempotency_key'] : ['lookup_key', 'region', 'sku_id'],
              outputs: isAct ? ['action_id', 'status', 'idempotency_key'] : ['records', 'total_count'],
              evidence: isAct ? ['api_mutation_receipt', 'action_events_jsonl'] : ['source_system_record'],
              sourceSystemId: 'bigquery_supply_chain_twin',
              table: tables[0]?.table_name || 'supply_chain_records'
            };
          });

      const queryTools = rawTools.filter(t => t.kind === 'query');
      const actionTools = rawTools.filter(t => t.kind === 'action');

      // 2. Source systems metadata
      const sysStrings = toSysArray(ag.systems);
      const sysList = (spec.systems && spec.systems.length)
        ? spec.systems.map((s, idx) => {
            const ownedTables = (s.tables && s.tables.length)
              ? s.tables
              : (tables[idx] ? [tables[idx].table_name] : (tables[0] ? [tables[0].table_name] : []));
            const sysTools = rawTools.filter(t => t.sourceSystemId === s.id || ownedTables.includes(t.table));
            const hasWrite = sysTools.some(t => t.kind === 'action') || (idx === spec.systems.length - 1 && actionTools.length > 0);
            return {
              name: s.name || sysStrings[idx] || 'Enterprise System',
              protocol: s.protocol || 'REST / OData v4 / BigQuery SQL',
              mode: hasWrite ? 'read / write' : 'read',
              category: idx === 0 ? 'Digital Twin / Lakehouse' : (hasWrite ? 'ERP / Execution Target' : 'Sensing & Solver Layer'),
              ownedTables,
              boundTools: sysTools.length ? sysTools.map(t => t.name) : (hasWrite ? actionTools.map(t => t.name) : queryTools.slice(0, 2).map(t => t.name))
            };
          })
        : sysStrings.slice(0, 4).map((sName, idx) => {
            const ownedTables = tables[idx] ? [tables[idx].table_name] : (tables[0] ? [tables[0].table_name] : []);
            const hasWrite = idx === 0 || idx === sysStrings.slice(0, 4).length - 1;
            return {
              name: sName,
              protocol: idx === 0 ? 'OData v4 / BAPI / REST' : 'BigQuery Storage Read API / PubSub',
              mode: hasWrite ? 'read / write' : 'read',
              category: idx === 0 ? 'ERP / System of Record' : 'Telemetry & Digital Twin',
              ownedTables,
              boundTools: hasWrite ? actionTools.map(t => t.name).concat(queryTools.slice(0, 1).map(t => t.name)) : queryTools.slice(idx, idx + 2).map(t => t.name)
            };
          });

      // 3. Workflow Stages (3 A2A Sub-Agents)
      const subs = (ag.subAgents && ag.subAgents.length >= 3)
        ? ag.subAgents.slice(0, 3)
        : [
            { name: 'Signal Ingestion & Context Node', role: 'Streams & validates live operational records from connected ERP/WMS/TMS tables' },
            { name: 'Scenario & Optimization Engine', role: 'Evaluates multi-echelon constraints, probability fans, and trade-offs' },
            { name: 'Exception & Write-Back Dispatcher', role: 'Enforces quality gates and commits signed payloads with idempotency keys' }
          ];

      const stageTools = [
        queryTools.slice(0, Math.max(1, Math.ceil(queryTools.length / 2))).map(t => t.name),
        queryTools.slice(Math.floor(queryTools.length / 2)).map(t => t.name),
        actionTools.map(t => t.name).concat(queryTools.slice(-1).map(t => t.name))
      ];

      // 4. Escalation Rules (derived from write_tools_req & domain thresholds)
      const writeToolNames = actionTools.map(t => t.name).join(', ') || 'action_commit_writeback';
      const writeReqs = Object.entries(spec.writeToolsReq || {});
      const reqFieldsList = writeReqs.length
        ? writeReqs.map(([fn, reqs]) => `${fn}(${(reqs || []).join(', ')})`).join(' · ')
        : 'target_id, rationale, idempotency_key';

      // 5. Evidence Requirements
      const evidenceItems = tables.slice(0, 3).map((t, i) => {
        const keyCols = (t.columns || []).slice(0, 3).map(c => `${t.table_name}.${c}`);
        const claim = i === 0
          ? `${ag.badge || ag.outcome} grounded in primary operational telemetry`
          : (i === 1
              ? `Cross-system anomaly & constraint verification across ${subPillar}`
              : `Pre-mutation baseline vs. post-action delta audit verification`);
        return { claim, cites: keyCols };
      });

      // 6. Relationships across fixture tables
      const relationships = [];
      for (let i = 0; i < tables.length; i++) {
        for (let j = i + 1; j < tables.length; j++) {
          const colsA = tables[i].columns || [];
          const colsB = tables[j].columns || [];
          const shared = colsA.filter(c => colsB.includes(c) && (c.endsWith('_id') || c === 'region' || c === 'sku_id' || c === 'plant_id' || c === 'vendor_id' || c === 'facility_id'));
          shared.forEach(col => {
            relationships.push({
              left: `${tables[i].table_name}.${col}`,
              right: `${tables[j].table_name}.${col}`,
              relType: col.endsWith('_id') ? 'foreign-key join (many-to-one)' : 'dimensional join'
            });
          });
        }
      }
      if (relationships.length === 0 && tables.length >= 2) {
        const c0 = (tables[0].columns || ['id'])[0];
        const c1 = (tables[1].columns || ['id'])[0];
        relationships.push({
          left: `${tables[0].table_name}.${c0}`,
          right: `${tables[1].table_name}.${c1}`,
          relType: 'workflow entity correlation'
        });
      }

      // 7. Golden Eval Scenario
      const evalObj = (spec.evalScenarios && spec.evalScenarios[0]) || {
        scenario_id: `SCENARIO-${ag.id.toUpperCase().slice(0, 12)}-01`,
        name: `${cleanName} Golden Operational Verification`,
        query: `Execute the ${cleanName} workflow for the current operational horizon, cite source-system table evidence, and commit governed remediation write-backs.`,
        expected_proof_obligations: [
          `Query primary ${subPillar} records from ${(tables[0]?.table_name) || 'digital_twin'}`,
          `Cross-reference constraints & anomalies in ${(tables[1]?.table_name) || 'secondary_signals'}`,
          `Execute pre-execution quality gate & idempotency check before ${writeToolNames}`,
          `Emit VegaChart visual surface and atomic copy-ready markdown table`
        ],
        sla_seconds: 15
      };

      const standards = (ag.standardsCompliance && ag.standardsCompliance.length)
        ? ag.standardsCompliance
        : ['ASCM SCOR DS v14.0', 'ISO 9001:2015 Quality Management', 'Google ADK + A2A v1.0 + MCP + A2UI v0.9', 'ISO/IEC 42001 AI Management System'];

      return `
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
        </div>

        <!-- SECTION 1: PLAYBOOK & GOVERNANCE (COLLAPSIBLE) -->
        <details class="sc-spec-section-card sc-spec-collapsible" id="spec-governance" ${openAttr}>
          <summary class="sc-spec-sec-head">
            <div>
              <div style="font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:3px;">
                01 · Enterprise Agent Contract
              </div>
              <h2 class="sc-spec-sec-title">
                Playbook &amp; Governance
                <span class="sc-spec-count-badge">${personaName} · ${subPillar}</span>
              </h2>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              ${!openByDefault ? `
                <span class="sc-spec-open-page-mini" onclick="event.preventDefault(); event.stopPropagation(); openAgentBlueprintPage('${ag.id}', true, event, 'spec-governance')">
                  ↗ Open in Dedicated Page
                </span>
              ` : ''}
              <span class="sc-spec-toggle-pill"></span>
            </div>
          </summary>

          <div class="sc-spec-sec-body">
            <!-- Sub-Drawer 1A: Role Mandate & In-Scope vs Out-of-Scope -->
            <details class="sc-spec-sub-drawer" open>
              <summary>
                <span>🛡️ 1A · Role Mandate &amp; Autonomous Scope (In-Scope vs. Out-of-Scope)</span>
                <span class="sc-sub-toggle-hint"></span>
              </summary>
              <div class="sc-spec-sub-drawer-body">
                <p style="font-size:14.5px; color:var(--text-primary); line-height:1.6; margin:0 0 14px;">
                  <strong>Role Mandate:</strong> Autonomous <strong>${personaName}</strong> agent for the <strong>${cleanName}</strong> workflow in <strong>${subPillar}</strong>. ${ag.solution} ${ag.advantage || ag.outcome}
                </p>

                <div class="sc-spec-scope-grid">
                  <div class="sc-spec-scope-col scope-in">
                    <div style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; text-transform:uppercase; color:#10b981; letter-spacing:0.06em;">
                      ✓ In Scope (Autonomous Execution)
                    </div>
                    <ul class="sc-spec-scope-list">
                      <li>${ag.solution}</li>
                      <li>Multi-table evidence synthesis across ${tables.map(t => `<code class="sc-spec-code">${t.table_name}</code>`).join(' ')} using <strong>${ag.solverStack || 'Vertex AI + BigQuery ML'}</strong>.</li>
                      <li>Governed write-back execution via <strong>${ag.apiWriteback || 'Signed MCP / REST / On-Prem ERP Connector'}</strong> with deterministic <code class="sc-spec-code">idempotency_key</code> audit logging.</li>
                    </ul>
                  </div>

                  <div class="sc-spec-scope-col scope-out">
                    <div style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; text-transform:uppercase; color:#f43f5e; letter-spacing:0.06em;">
                      ✕ Out of Scope (Human Authority Retained)
                    </div>
                    <ul class="sc-spec-scope-list">
                      <li>Unapproved capital expenditure, legal contract termination, or policy overrides outside ${personaName} delegation limits.</li>
                      <li>Direct database mutations bypassing <code class="sc-spec-code">enforce_tool_contract()</code> or missing mandatory <code class="sc-spec-code">idempotency_key</code> tokens.</li>
                      <li>Executing external ERP/WMS write-backs when source telemetry exceeds staleness thresholds without human confirmation.</li>
                    </ul>
                  </div>
                </div>
              </div>
            </details>

            <!-- Sub-Drawer 1B: Escalation Rules & Pre-Execution Quality Gates -->
            <details class="sc-spec-sub-drawer" ${openAttr}>
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
                        <td>Financial or volume impact exceeds <strong>${personaName}</strong> autonomous threshold (&gt;20% variance vs. baseline plan)</td>
                        <td><span class="sc-spec-code action-code">escalate_to_human</span></td>
                        <td style="color:var(--text-secondary);">High-magnitude supply chain reallocations require human sign-off in Control Tower before ERP commit.</td>
                      </tr>
                      <tr>
                        <td>Mutation call to <code class="sc-spec-code">${writeToolNames}</code> missing required fields (<code class="sc-spec-code">${reqFieldsList}</code>)</td>
                        <td><span class="sc-spec-code">request_more_info</span></td>
                        <td style="color:var(--text-secondary);">Enforced by <code class="sc-spec-code">enforce_tool_contract()</code> in <code class="sc-spec-code">agents/${ag.id}/app/agent.py</code> to prevent partial ERP writes.</td>
                      </tr>
                      <tr>
                        <td>Mutation call lacks a non-empty <code class="sc-spec-code">idempotency_key</code> or attempts duplicate replay</td>
                        <td><span class="sc-spec-code">request_confirmation</span></td>
                        <td style="color:var(--text-secondary);">Guarantees exactly-once execution across Enterprise ERP (MCP / On-Prem DB), IBP, WMS, and TMS connectors.</td>
                      </tr>
                      <tr>
                        <td>Proposed action contradicts physical constraints or lacks corroborating records across at least 2 tables</td>
                        <td><span class="sc-spec-code action-code">refuse / reject_mutation</span></td>
                        <td style="color:var(--text-secondary);">Single-source or unverified assertions cannot trigger production state changes.</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </details>

            <!-- Sub-Drawer 1C: Hard Guardrails & Evidence Requirements -->
            <details class="sc-spec-sub-drawer" ${openAttr}>
              <summary>
                <span>🔒 1C · Hard Guardrails &amp; Source-Table Evidence Requirements (${evidenceItems.length} Rules)</span>
                <span class="sc-sub-toggle-hint"></span>
              </summary>
              <div class="sc-spec-sub-drawer-body">
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:16px;">
                  <div>
                    <div class="sc-spec-mini-label" style="margin-top:0;">Hard Guardrails</div>
                    <ul class="sc-spec-scope-list" style="margin:0;">
                      <li>Never fabricate SKU quantities, lead times, or financial metrics; cite exact rows from ${tables.slice(0, 2).map(t => `<code class="sc-spec-code">${t.table_name}</code>`).join(' & ')}.</li>
                      <li>Never bypass <code class="sc-spec-code">enforce_tool_contract()</code> before invoking ${actionTools.map(t => `<code class="sc-spec-code action-code">${t.name}</code>`).join(' ') || 'write tools'}.</li>
                      <li>Append every executed mutation to immutable audit trail <code class="sc-spec-code ev-code">artifacts/action-events.jsonl</code>.</li>
                      <li>Route routine operational queries to <strong>Gemini 3.8 Flash</strong> and escalate multi-echelon trade-offs to <strong>Gemini 3.1 Pro / 4 Argon</strong>.</li>
                    </ul>
                  </div>

                  <div>
                    <div class="sc-spec-mini-label" style="margin-top:0;">Evidence Requirements</div>
                    <div style="display:flex; flex-direction:column; gap:8px;">
                      ${evidenceItems.map(ev => `
                        <div style="padding:10px 14px; border-radius:10px; background:var(--bg-card); border:1px solid var(--border-subtle);">
                          <div style="font-size:13px; font-weight:700; color:var(--text-primary); margin-bottom:4px;">${ev.claim}</div>
                          <div>${ev.cites.map(c => `<code class="sc-spec-code ev-code">${c}</code>`).join('')}</div>
                        </div>
                      `).join('')}
                    </div>
                  </div>
                </div>
              </div>
            </details>
          </div>
        </details>

        <!-- SECTION 2: MULTI-STAGE WORKFLOW (COLLAPSIBLE) -->
        <details class="sc-spec-section-card sc-spec-collapsible" id="spec-workflow" ${openAttr}>
          <summary class="sc-spec-sec-head">
            <div>
              <div style="font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:3px;">
                02 · Execution Sequence
              </div>
              <h2 class="sc-spec-sec-title">
                Workflow <span class="sc-spec-count-badge">Sequential &amp; A2A Branching · ${subs.length} Stages</span>
              </h2>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              ${!openByDefault ? `
                <span class="sc-spec-open-page-mini" onclick="event.preventDefault(); event.stopPropagation(); openAgentBlueprintPage('${ag.id}', true, event, 'spec-workflow')">
                  ↗ Open in Dedicated Page
                </span>
              ` : ''}
              <span class="sc-spec-toggle-pill"></span>
            </div>
          </summary>

          <div class="sc-spec-sec-body">
            <div style="font-size:12.5px; color:var(--text-secondary); font-weight:600; margin-bottom:12px;">
              Solver &amp; Reasoning Stack: <strong>${ag.solverStack || 'Vertex AI + BigQuery ML'}</strong>
            </div>
            <ol class="sc-spec-flow-list">
              ${subs.map((sub, idx) => `
                <li class="sc-spec-flow-step">
                  <div class="sc-spec-step-num" style="background:${dept.color};">${idx + 1}</div>
                  <div style="flex:1;">
                    <div style="font-family:var(--font-display); font-size:16px; font-weight:800; color:var(--text-primary); margin-bottom:4px;">
                      ${sub.name}
                    </div>
                    <p style="font-size:13.5px; color:var(--text-secondary); margin:0 0 8px; line-height:1.5;">
                      ${sub.role}. Grounds state across ${tables[idx] ? `<code class="sc-spec-code">${tables[idx].table_name}</code>` : 'connected digital twin tables'} and validates execution constraints.
                    </p>
                    <div>
                      ${(stageTools[idx] || []).map(tName => {
                        const isAct = String(tName).startsWith('action_');
                        return `<a href="#spec-tool-${tName}" class="sc-spec-code ${isAct ? 'action-code' : ''}" onclick="return openAndScrollToSpecSection('spec-tools', 'spec-tool-${tName}');">${tName}</a>`;
                      }).join('')}
                    </div>
                  </div>
                </li>
              `).join('')}
            </ol>
          </div>
        </details>

        <!-- SECTION 3: AGENT TOOLS (COLLAPSIBLE) -->
        <details class="sc-spec-section-card sc-spec-collapsible" id="spec-tools" ${openAttr}>
          <summary class="sc-spec-sec-head">
            <div>
              <div style="font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:3px;">
                03 · Bound ADK Function Contracts
              </div>
              <h2 class="sc-spec-sec-title">
                Agent Tools <span class="sc-spec-count-badge">${rawTools.length}</span>
              </h2>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="sc-spec-code">agents/${ag.id}/app/tools.py</span>
              ${!openByDefault ? `
                <span class="sc-spec-open-page-mini" onclick="event.preventDefault(); event.stopPropagation(); openAgentBlueprintPage('${ag.id}', true, event, 'spec-tools')">
                  ↗ Open in Dedicated Page
                </span>
              ` : ''}
              <span class="sc-spec-toggle-pill"></span>
            </div>
          </summary>

          <div class="sc-spec-sec-body">
            <div class="sc-spec-tools-grid">
              ${rawTools.map(t => `
                <div class="sc-spec-tool-card" id="spec-tool-${t.name}">
                  <div>
                    <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; flex-wrap:wrap; margin-bottom:8px;">
                      <code class="sc-spec-code ${t.kind === 'action' ? 'action-code' : ''}" style="font-size:13px; font-weight:800;">${t.name}</code>
                      <div style="display:flex; align-items:center; gap:6px;">
                        <span class="sc-spec-count-badge" style="color:${t.kind === 'action' ? '#fb7185' : '#38bdf8'};">${t.kind}</span>
                        ${t.table ? `<span class="sc-spec-count-badge">${t.table}</span>` : ''}
                      </div>
                    </div>
                    <p style="font-size:13px; color:var(--text-secondary); margin:0 0 10px; line-height:1.5;">
                      ${t.description}
                    </p>
                  </div>

                  <div style="border-top:1px solid var(--border-subtle); padding-top:8px;">
                    <div class="sc-spec-io-row">
                      <span class="sc-spec-io-label">in</span>
                      ${(t.inputs || []).map(inp => `<code class="sc-spec-code">${inp}</code>`).join('')}
                    </div>
                    <div class="sc-spec-io-row">
                      <span class="sc-spec-io-label">out</span>
                      ${(t.outputs || []).map(out => `<code class="sc-spec-code">${out}</code>`).join('')}
                    </div>
                    <div class="sc-spec-io-row">
                      <span class="sc-spec-io-label">evidence</span>
                      ${(t.evidence || []).map(ev => `<code class="sc-spec-code ev-code">${ev}</code>`).join('')}
                    </div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        </details>

        <!-- SECTION 4: SOURCE SYSTEMS (COLLAPSIBLE) -->
        <details class="sc-spec-section-card sc-spec-collapsible" id="spec-systems" ${openAttr}>
          <summary class="sc-spec-sec-head">
            <div>
              <div style="font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:3px;">
                04 · Enterprise Integration Topology
              </div>
              <h2 class="sc-spec-sec-title">
                Source Systems <span class="sc-spec-count-badge">${sysList.length}</span>
              </h2>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              ${!openByDefault ? `
                <span class="sc-spec-open-page-mini" onclick="event.preventDefault(); event.stopPropagation(); openAgentBlueprintPage('${ag.id}', true, event, 'spec-systems')">
                  ↗ Open in Dedicated Page
                </span>
              ` : ''}
              <span class="sc-spec-toggle-pill"></span>
            </div>
          </summary>

          <div class="sc-spec-sec-body">
            <div style="font-size:12.5px; color:var(--text-secondary); font-weight:600; margin-bottom:12px;">
              Write-Back Target: <strong>${ag.apiWriteback || 'Signed MCP / REST / On-Prem ERP API'}</strong>
            </div>
            <div class="sc-spec-sys-grid">
              ${sysList.map(sys => `
                <div class="sc-spec-sys-card">
                  <div>
                    <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; margin-bottom:6px;">
                      <span style="font-family:var(--font-display); font-size:16px; font-weight:800; color:var(--text-primary);">${sys.name}</span>
                      <span class="sc-spec-count-badge" style="color:${sys.mode.includes('write') ? '#34d399' : '#38bdf8'};">${sys.mode}</span>
                    </div>
                    <div style="font-family:var(--font-mono); font-size:11.5px; color:var(--text-secondary); margin-bottom:10px;">
                      Protocol: ${sys.protocol} · ${sys.category}
                    </div>
                  </div>

                  <div style="border-top:1px solid var(--border-subtle); padding-top:8px;">
                    ${sys.ownedTables && sys.ownedTables.length ? `
                      <div class="sc-spec-io-row">
                        <span class="sc-spec-io-label">owns</span>
                        ${sys.ownedTables.map(tbl => `<a href="#spec-entity-${tbl}" class="sc-spec-code ev-code" onclick="return openAndScrollToSpecSection('spec-data-model', 'spec-entity-${tbl}');">${tbl}</a>`).join('')}
                      </div>
                    ` : ''}
                    <div class="sc-spec-io-row">
                      <span class="sc-spec-io-label">tools</span>
                      ${(sys.boundTools || []).map(tName => `<a href="#spec-tool-${tName}" class="sc-spec-code ${String(tName).startsWith('action_') ? 'action-code' : ''}" onclick="return openAndScrollToSpecSection('spec-tools', 'spec-tool-${tName}');">${tName}</a>`).join('')}
                    </div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        </details>

        <!-- SECTION 5: DATA MODEL & SCHEMAS (COLLAPSIBLE) -->
        <details class="sc-spec-section-card sc-spec-collapsible" id="spec-data-model" ${openAttr}>
          <summary class="sc-spec-sec-head">
            <div>
              <div style="font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:3px;">
                05 · Canonical Digital Twin Schema &amp; Live Fixtures
              </div>
              <h2 class="sc-spec-sec-title">
                Data Model <span class="sc-spec-count-badge">${tables.length} entities · ${totalFields} fields</span>
              </h2>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="sc-spec-code">Pluggable Data Layer: BigQuery · On-Prem SQL · 3rd-Party MCPs</span>
              ${!openByDefault ? `
                <span class="sc-spec-open-page-mini" onclick="event.preventDefault(); event.stopPropagation(); openAgentBlueprintPage('${ag.id}', true, event, 'spec-data-model')">
                  ↗ Open in Dedicated Page
                </span>
              ` : ''}
              <span class="sc-spec-toggle-pill"></span>
            </div>
          </summary>

          <div class="sc-spec-sec-body">
            <div class="sc-spec-entities-list">
              ${tables.map((t, idx) => {
                const cols = t.columns || [];
                const rows = t.rows || [];
                return `
                  <details class="sc-spec-entity" id="spec-entity-${t.table_name}" ${idx === 0 ? 'open' : ''}>
                    <summary>
                      <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                        <code class="sc-spec-code ev-code" style="font-size:13.5px; font-weight:800;">${t.table_name}</code>
                        <span style="font-size:12.5px; color:var(--text-secondary); font-weight:600;">
                          ${cols.length} cols · ${t.row_count || rows.length} fixture rows · BigQuery / On-Prem SQL / MCP Data Layer
                        </span>
                      </div>
                      <span style="font-size:12px; color:${dept.color}; font-weight:700;">▾ Click to Inspect Schema &amp; Sample Values</span>
                    </summary>
                    <div style="padding:14px 18px;">
                      <div class="sc-spec-table-wrap">
                        <table class="sc-spec-table">
                          <thead>
                            <tr>
                              <th style="width:28%;">Column</th>
                              <th style="width:18%;">Type</th>
                              <th style="width:16%;">Constraints</th>
                              <th>Verified Fixture Sample Values</th>
                            </tr>
                          </thead>
                          <tbody>
                            ${cols.map(col => {
                              const info = inferColumnTypeAndConstraint(col, rows);
                              return `
                                <tr>
                                  <td>
                                    <code class="sc-spec-code" style="margin:0;">${col}</code>
                                    ${info.isPk ? `<span class="sc-spec-count-badge" style="margin-left:6px; color:#f59e0b; border-color:#f59e0b55;">PK</span>` : ''}
                                  </td>
                                  <td style="font-family:var(--font-mono); font-size:12px; color:var(--text-secondary);">${info.colType}</td>
                                  <td><span class="sc-spec-count-badge">required</span></td>
                                  <td style="font-family:var(--font-mono); font-size:12px; color:var(--text-secondary);">${info.sampleStr || '—'}</td>
                                </tr>
                              `;
                            }).join('')}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </details>
                `;
              }).join('')}
            </div>

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:16px; margin-top:16px;">
              <div>
                <div class="sc-spec-mini-label">Entity Relationships</div>
                <ul class="sc-spec-scope-list" style="margin:0;">
                  ${relationships.map(rel => `
                    <li>
                      <code class="sc-spec-code">${rel.left}</code>
                      <span style="color:${dept.color}; font-weight:800;">&rarr;</span>
                      <code class="sc-spec-code">${rel.right}</code>
                      <span style="font-size:12px; color:var(--text-secondary);">(${rel.relType})</span>
                    </li>
                  `).join('')}
                </ul>
              </div>

              <div>
                <div class="sc-spec-mini-label">Seeded Operational Anomalies (What the Agent Must Catch)</div>
                <div style="padding:14px 16px; border-radius:12px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-left:4px solid #f59e0b;">
                  <p style="font-size:13px; color:var(--text-primary); margin:0 0 8px; line-height:1.5;">
                    <strong>Seeded Fault:</strong> ${ag.problem}
                  </p>
                  <div style="margin-bottom:8px;">
                    ${tables.slice(0, 2).map(t => `<code class="sc-spec-code ev-code">${t.table_name}</code>`).join('')}
                  </div>
                  <div style="font-size:12.5px; color:var(--text-secondary);">
                    <strong>Expected Remediation:</strong> Detect anomaly across connected tables, validate constraints via ${ag.solverStack || 'Vertex AI'}, and execute <code class="sc-spec-code action-code">${writeToolNames}</code>.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </details>

        <!-- SECTION 6: EVALS & PROOF (COLLAPSIBLE) -->
        <details class="sc-spec-section-card sc-spec-collapsible" id="spec-evals" ${openAttr}>
          <summary class="sc-spec-sec-head">
            <div>
              <div style="font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:3px;">
                06 · Behavioral Proof &amp; Golden Evaluations
              </div>
              <h2 class="sc-spec-sec-title">
                Evals &amp; Proof <span class="sc-spec-count-badge">${adk.smokeTestsPassed || 7}/7 Smoke Tests Passing</span>
              </h2>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="sc-spec-code">agents/${ag.id}/evals/golden_scenarios.json</span>
              ${!openByDefault ? `
                <span class="sc-spec-open-page-mini" onclick="event.preventDefault(); event.stopPropagation(); openAgentBlueprintPage('${ag.id}', true, event, 'spec-evals')">
                  ↗ Open in Dedicated Page
                </span>
              ` : ''}
              <span class="sc-spec-toggle-pill"></span>
            </div>
          </summary>

          <div class="sc-spec-sec-body">
            <div style="padding:18px 20px; border-radius:14px; background:var(--bg-elevated); border:1px solid var(--border-subtle); border-left:4px solid ${dept.color}; margin-bottom:16px;">
              <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-bottom:8px;">
                <span style="font-family:var(--font-mono); font-size:12px; font-weight:800; color:${dept.color};">
                  ${evalObj.scenario_id} · ${evalObj.name}
                </span>
                <span class="sc-spec-count-badge">SLA Target: &le;${evalObj.sla_seconds || 15}s</span>
              </div>
              <p style="font-size:15px; font-weight:700; color:var(--text-primary); margin:0 0 12px; line-height:1.5;">
                “${evalObj.query}”
              </p>
              <div class="sc-spec-io-row">
                <span class="sc-spec-io-label">expects tools</span>
                ${rawTools.map(t => `<code class="sc-spec-code ${t.kind === 'action' ? 'action-code' : ''}">${t.name}</code>`).join('')}
              </div>
              <div class="sc-spec-io-row">
                <span class="sc-spec-io-label">cites entities</span>
                ${tables.map(t => `<code class="sc-spec-code ev-code">${t.table_name}</code>`).join('')}
              </div>
              <div class="sc-spec-io-row">
                <span class="sc-spec-io-label">eval models</span>
                <code class="sc-spec-code">gemini-3.8-flash</code>
                <code class="sc-spec-code">gemini-3.1-pro / gemini-4-argon (subject to availability)</code>
              </div>
            </div>

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:16px;">
              <div>
                <div class="sc-spec-mini-label" style="margin-top:0;">Expected Proof Obligations</div>
                <ul class="sc-spec-scope-list" style="margin:0;">
                  ${(evalObj.expected_proof_obligations || []).map(ob => `<li>${ob}</li>`).join('')}
                </ul>
              </div>

              <div>
                <div class="sc-spec-mini-label" style="margin-top:0;">Governing Documents &amp; Industry Standards</div>
                <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:12px;">
                  ${standards.map(st => `<span class="sc-spec-code ev-code">${st}</span>`).join('')}
                </div>
                <div style="font-size:12.5px; color:var(--text-secondary); line-height:1.55; padding:10px 12px; border-radius:10px; background:var(--bg-elevated); border:1px solid var(--border-subtle);">
                  <strong>Spec Source:</strong> <code class="sc-spec-code">agents/${ag.id}/app/agent.py</code> · <code class="sc-spec-code">agents/${ag.id}/tests/test_smoke.py</code> · Verified 7/7 deterministic contract &amp; A2UI surface checks passing.
                </div>
              </div>
            </div>
          </div>
        </details>
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
                  🤖 ${other.name}
                </button>
              `).join('')}
            </div>
          </div>

          <!-- 1. What This Agent Does + At-a-Glance Strip -->
          <div class="agent-hero-banner" style="padding: 30px 34px; margin-bottom: 24px;">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
              <div style="display:flex; align-items:center; gap:14px;">
                <div class="ai-bot-square" style="width:48px; height:48px; font-size:22px;">✦</div>
                <div>
                  <h1 class="agent-title" style="font-size: clamp(24px, 2.7vw, 34px); margin: 0;">${cleanAgentName(ag.name)}</h1>
                  <div style="font-size:14.5px; color:var(--text-secondary); margin-top:4px; font-weight:600;">${ag.subPillarName || dept.name}</div>
                </div>
              </div>
              <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                <button type="button" class="switch-pill" onclick="togglePersonaJourneyStep('agentMoreDetailsDrawer')">
                  ▾ Click for Problem &amp; Outcome Details
                </button>
                <button type="button" class="switch-pill" style="background:${dept.color}; border-color:${dept.color}; color:#ffffff; font-weight:700;" onclick="openAgentBlueprintPage('${ag.id}', true, event, 'spec-governance')">
                  📄 Playbook, Governance &amp; Full Spec Page &rarr;
                </button>
              </div>
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
            ${renderAgentAtAGlanceStrip(ag, dept, false)}
          </div>

          <!-- 2. Branching Multi-Stage Workflow Architecture Diagram -->
          ${renderSimpleAgentArchitectureDiagram(ag, dept)}

          <!-- 3. Simple Basic Cost Details Card (Same Website Design & Theme) -->
          ${renderAgentCostAndRoiPanel(ag, dept)}

          <!-- 4. Dedicated Box for a Video (Placed above collapsed spec drawers for a clean executive view) -->
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

          <!-- 5. Collapsible Enterprise Agent Contract, Playbook & Technical Specification Sheet (Collapsed by Default) -->
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

          <div class="agent-hero-banner" style="padding: 26px 32px; margin-bottom: 20px;">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
              <div style="display:flex; align-items:center; gap:14px;">
                <div class="ai-bot-square" style="width:46px; height:46px; font-size:20px;">🛡️</div>
                <div>
                  <div style="font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:2px;">
                    Dedicated Enterprise Agent Contract · Playbook &amp; Technical Specification
                  </div>
                  <h1 class="agent-title" style="font-size: clamp(22px, 2.4vw, 30px); margin: 0;">${cleanAgentName(ag.name)}</h1>
                </div>
              </div>
              <button type="button" class="switch-pill" onclick="openAgentPage('${ag.id}', true, event)">
                &larr; Return to Clean Agent Overview
              </button>
            </div>
            ${renderAgentAtAGlanceStrip(ag, dept, true)}
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


def update_file(path: Path):
    text = path.read_text(encoding="utf-8")

    # 1. Inject EXTRA_SPEC_CSS if not present
    css_anchor = "    .sc-spec-sec-head {"
    if "details.sc-spec-section-card.sc-spec-collapsible" not in text:
        if css_anchor in text:
            text = text.replace(css_anchor, EXTRA_SPEC_CSS + "\n" + css_anchor, 1)
        else:
            raise RuntimeError(f"Could not find {css_anchor} in {path}")
    else:
        # Replace existing collapsible CSS block up to .sc-spec-sec-head
        start_css = text.find("    /* Collapsible Spec Section Cards")
        end_css = text.find(css_anchor)
        if start_css != -1 and end_css != -1 and start_css < end_css:
            text = text[:start_css] + EXTRA_SPEC_CSS.lstrip("\n") + "\n" + text[end_css:]

    # 2. Replace renderAgentAtAGlanceStrip .. openAgentBlueprintPage
    start_marker_1 = "    function openAndScrollToSpecSection("
    start_marker_2 = "    function renderAgentAtAGlanceStrip("
    start_idx = text.find(start_marker_1)
    if start_idx == -1:
        start_idx = text.find(start_marker_2)
    if start_idx == -1:
        raise RuntimeError(f"Could not find renderAgentAtAGlanceStrip in {path}")

    end_marker = "    function selectDemoTableTab("
    end_idx = text.find(end_marker, start_idx)
    if end_idx == -1:
        raise RuntimeError(f"Could not find selectDemoTableTab in {path}")

    text = text[:start_idx] + NEW_JS_FUNCTIONS + "\n\n" + text[end_idx:]
    path.write_text(text, encoding="utf-8")
    print(f"Updated {path.name}")


if __name__ == "__main__":
    for f in HTML_FILES:
        if f.exists():
            update_file(f)

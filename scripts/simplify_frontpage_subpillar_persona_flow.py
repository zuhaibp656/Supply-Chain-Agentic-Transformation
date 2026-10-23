#!/usr/bin/env python3
"""
Simplifies the Front Page (#pageHome) Pillar -> Sub-Pillar -> Persona flow
per user feedback:
  1. Main Pillar Cards on #pageHome: Clean & minimal (Badge, Pillar Name,
     1-line subtitle, SVG stage — no mini-pill clutter).
  2. Clicking a Main Pillar expands ONLY the 3 or 4 Sub-Pillar Boxes
     (e.g. Demand Forecasting -> Trade Promotion -> S&OP / IBP -> Portfolio & SKU).
     Zero walls of text, zero Agent cards on the front page.
  3. Clicking any Sub-Pillar Box smoothly animates / drops down ONLY the 3
     Human Persona Cards for that Sub-Pillar.
  4. Clicking a Persona Card opens the Persona Page (#persona/<id>), which
     leads to their Daily Journey and AI Agents (#agent/<id>).
  5. Keeps the rich Sub-Pillar + Agent + Persona details inside the
     Periodic Table (#periodic) and Neural Mind Map (#mindmap).
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT, "index.html")
PERIODIC_HTML_PATH = os.path.join(ROOT, "periodic_table.html")
MINDMAP_HTML_PATH = os.path.join(ROOT, "mind_map.html")


def main():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Add clean CSS for the progressive Sub-Pillar Box -> Persona Dropdown drawer
    clean_subpillar_css = """
    /* =========================================================================
       CLEAN PROGRESSIVE FRONT-PAGE FLOW: MAIN PILLAR -> SUB-PILLAR BOXES -> PERSONAS
       ========================================================================= */
    .subpillar-boxes-row {
      display: grid;
      grid-template-columns: repeat(var(--sp-count, 4), minmax(0, 1fr));
      gap: 18px;
      margin-top: 8px;
    }

    @media (max-width: 1080px) {
      .subpillar-boxes-row {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }

    @media (max-width: 640px) {
      .subpillar-boxes-row {
        grid-template-columns: 1fr;
      }
    }

    .subpillar-box-card {
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 18px;
      padding: 24px 22px;
      border-radius: 18px;
      background: var(--bg-card);
      border: 1.5px solid var(--border-strong);
      border-top: 5px solid var(--sp-color, #2563eb);
      cursor: pointer;
      transition: transform 0.26s var(--ease-spring), box-shadow 0.26s var(--ease-spring), border-color 0.2s ease, background 0.2s ease;
      text-align: left;
    }

    .subpillar-box-card:hover {
      transform: translateY(-6px) scale(1.015);
      border-color: var(--sp-color, #2563eb);
      box-shadow: 0 18px 38px rgba(0, 0, 0, 0.38);
    }

    .subpillar-box-card.active {
      background: linear-gradient(160deg, rgba(30, 41, 59, 0.96) 0%, rgba(15, 23, 42, 0.98) 100%);
      border-color: var(--sp-color, #2563eb);
      box-shadow: 0 20px 44px rgba(0, 0, 0, 0.48), 0 0 0 2px var(--sp-color, #2563eb);
      transform: translateY(-4px);
    }

    .subpillar-step-num {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 999px;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      background: rgba(255, 255, 255, 0.06);
      color: var(--sp-color, #38bdf8);
      border: 1px solid rgba(255, 255, 255, 0.12);
    }

    .subpillar-box-icon {
      width: 46px;
      height: 46px;
      border-radius: 13px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.12);
    }

    .subpillar-box-title {
      font-family: var(--font-display);
      font-size: 21px;
      font-weight: 800;
      color: var(--text-primary);
      line-height: 1.25;
      letter-spacing: -0.015em;
    }

    .subpillar-box-cta {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: 14px;
      border-top: 1px solid var(--border-subtle);
      font-size: 13px;
      font-weight: 800;
      color: var(--sp-color, #38bdf8);
    }

    .subpillar-personas-drawer {
      margin-top: 22px;
      padding: 24px 26px;
      border-radius: 20px;
      background: rgba(15, 23, 42, 0.78);
      border: 1.5px solid var(--sp-color, #2563eb);
      box-shadow: 0 20px 48px rgba(0, 0, 0, 0.42);
      animation: ptExpandIn 0.32s var(--ease-spring) forwards;
    }

    html[data-theme="light"] .subpillar-box-card {
      background: #ffffff;
      border-color: #cbd5e1;
      border-top: 5px solid var(--sp-color, #2563eb);
      box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
    }

    html[data-theme="light"] .subpillar-box-card:hover,
    html[data-theme="light"] .subpillar-box-card.active {
      background: #f8fbff;
      border-color: var(--sp-color, #2563eb);
      box-shadow: 0 18px 38px rgba(26, 115, 232, 0.16);
    }

    html[data-theme="light"] .subpillar-step-num {
      background: #f1f5f9;
      border-color: #cbd5e1;
    }

    html[data-theme="light"] .subpillar-box-icon {
      background: #f8fafc;
      border-color: #e2e8f0;
    }

    html[data-theme="light"] .subpillar-personas-drawer {
      background: #ffffff;
      border-color: var(--sp-color, #2563eb);
      box-shadow: 0 16px 38px rgba(15, 23, 42, 0.1);
    }
"""
    if ".subpillar-boxes-row" not in html:
        html = html.replace("  </style>\n</head>", clean_subpillar_css + "\n  </style>\n</head>", 1)

    # 2. Simplify section subtitle & tab labels on #pageHome
    html = html.replace(
        "Click any of the 6 Core Operating Pillars below to expand its Sub-Pillar Lifecycle Spine, 60 Personas, and 60 AI Agents.",
        "Select a Pillar to view its Sub-Pillars, then click any Sub-Pillar to explore its Personas.",
    )
    html = html.replace("20 Sub-Pillars · 60 Agents", "20 Sub-Pillars · 60 Personas")
    html = html.replace("4 Sub-Pillars · 12 Agents", "4 Sub-Pillars · 12 Personas")
    html = html.replace("3 Sub-Pillars · 9 Agents", "3 Sub-Pillars · 9 Personas")

    # 3. Clean up renderOrgChart() so Main Pillar cards are minimal and uncluttered (no mini-pipeline pills inside the main card)
    clean_render_org_chart = """    function renderOrgChart() {
      const row = document.getElementById('deptRowContainer');
      if (!row) return;
      row.innerHTML = Object.values(DEPARTMENTS).map(dept => {
        const isActive = dept.id === selectedDeptId;
        const subPillars = dept.subPillars || [];
        return `
          <div class="dept-node ${isActive ? 'active' : ''}"
               data-dept-id="${dept.id}"
               style="--dept-accent: ${dept.color};"
               onclick="selectDepartment('${dept.id}', event)">
            <div style="position:relative; z-index:2;">
              <div style="display:inline-flex; align-items:center; gap:6px; padding:4px 11px; border-radius:999px; font-size:11px; font-weight:800; letter-spacing:0.06em; text-transform:uppercase; background:${dept.color}18; color:${dept.color}; border:1px solid ${dept.color}40; margin-bottom:10px;">
                <span>${dept.scorBadge || 'PILLAR'}</span>
              </div>
              <div class="dept-node-title">${dept.name}</div>
              <div class="dept-node-sub">${dept.subtitle}</div>
            </div>
            <div class="dept-anim-stage">
              ${renderSupplyChainWatermarkSvg(dept.watermarkType, dept.color, 'dept-stage-svg')}
              <span class="dept-anim-meta">${subPillars.length} Sub-Pillars · ${dept.personaIds.length} Personas &rarr;</span>
            </div>
          </div>
        `;
      }).join('');

      renderDepartmentShowcaseBox();
    }"""

    html = re.sub(
        r"    function renderOrgChart\(\) \{.*?\n    \}",
        clean_render_org_chart,
        html,
        count=1,
        flags=re.S,
    )

    # 4. Update selectDepartment() so clicking a Main Pillar resets currentSelectedSubPillarId = null (shows ONLY the 3-4 Sub-Pillar boxes first!)
    html = html.replace(
        "selectedDeptId = (selectedDeptId === deptId) ? null : deptId;",
        "selectedDeptId = (selectedDeptId === deptId) ? null : deptId;\n      currentSelectedSubPillarId = null;",
    )
    html = html.replace(
        "selectedDeptId = canonicalVId;",
        "selectedDeptId = canonicalVId;\n        currentSelectedSubPillarId = null;",
    )

    # 5. Replace renderDepartmentShowcaseBox() so:
    #    - Step 1: Expanding a Main Pillar shows ONLY the 3 or 4 clean Sub-Pillar Boxes.
    #    - Step 2: Clicking a Sub-Pillar Box smoothly drops down ONLY its 3 Human Persona Cards.
    #    - Step 3: Clicking a Persona Card opens #persona/<id> (where their Daily Journey & AI Agents live).
    clean_showcase_js = """    let currentSelectedSubPillarId = null;

    function selectSubPillarFilter(spId, ev) {
      const sRect = ev ? getClickedCardRect(ev) : null;
      currentSelectedSubPillarId = (currentSelectedSubPillarId === spId) ? null : spId;
      renderDepartmentShowcaseBox();
      if (currentSelectedSubPillarId) {
        const drawerEl = document.getElementById('subPillarPersonasDrawerEl');
        if (sRect && drawerEl && typeof animateGenieOutOfBox === 'function') {
          const dept = DEPARTMENTS[selectedDeptId];
          const sp = (dept && dept.subPillars || []).find(s => s.id === currentSelectedSubPillarId);
          animateGenieOutOfBox(sRect, drawerEl, (sp && sp.color) || (dept && dept.color) || '#2563eb');
        }
        setTimeout(() => {
          if (drawerEl) drawerEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 70);
      }
    }

    function renderDepartmentShowcaseBox() {
      const container = document.getElementById('deptShowcaseContainer');
      if (!container) return;
      if (!selectedDeptId || !DEPARTMENTS[selectedDeptId]) {
        container.innerHTML = '';
        return;
      }
      const dept = DEPARTMENTS[selectedDeptId];
      const subPillars = dept.subPillars || [];
      if (currentSelectedSubPillarId && !subPillars.some(sp => sp.id === currentSelectedSubPillarId)) {
        currentSelectedSubPillarId = null;
      }
      const activeSubPillar = subPillars.find(sp => sp.id === currentSelectedSubPillarId) || null;

      container.innerHTML = `
        <div id="deptShowcaseBoxEl" class="dept-showcase-box genie-enter" style="--dept-accent: ${dept.color}; padding: 28px 30px;">
          <!-- Clean, Minimal Pillar Header -->
          <div class="showcase-header" style="margin-bottom: 18px;">
            <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
              <span style="padding:5px 12px; border-radius:999px; background:${dept.color}20; color:${dept.color}; border:1px solid ${dept.color}45; font-family:var(--font-mono); font-size:11.5px; font-weight:800; letter-spacing:0.06em;">
                PILLAR ${dept.vNum} · ${subPillars.length} SUB-PILLARS
              </span>
              <div class="showcase-dept-name" style="font-size:clamp(22px, 2.3vw, 28px); margin:0;">
                <span>${dept.name}</span>
              </div>
            </div>

            <button type="button" class="switch-pill" onclick="selectDepartment('${dept.id}')">
              ✕ Close
            </button>
          </div>

          <!-- Step 1 Instruction -->
          <div style="font-size:13.5px; font-weight:600; color:var(--text-secondary); margin-bottom:14px;">
            Select a sub-pillar below to view its supply chain personas:
          </div>

          <!-- ONLY the 3 or 4 Clean Sub-Pillar Boxes -->
          <div class="subpillar-boxes-row" style="--sp-count: ${subPillars.length};">
            ${subPillars.map((sp, idx) => {
              const isAct = activeSubPillar && activeSubPillar.id === sp.id;
              return `
                <button type="button"
                        class="subpillar-box-card ${isAct ? 'active' : ''}"
                        style="--sp-color: ${sp.color};"
                        onclick="selectSubPillarFilter('${sp.id}', event)">
                  <div>
                    <div style="display:flex; align-items:center; justify-content:space-between; gap:10px; margin-bottom:16px;">
                      <span class="subpillar-step-num" style="--sp-color: ${sp.color};">
                        0${idx + 1} · SUB-PILLAR
                      </span>
                      <div class="subpillar-box-icon">${sp.icon}</div>
                    </div>
                    <div class="subpillar-box-title">${sp.name}</div>
                  </div>

                  <div class="subpillar-box-cta" style="--sp-color: ${sp.color};">
                    <span>👤 ${(sp.items || []).length} Personas</span>
                    <span>${isAct ? '▴ Hide' : '▾ Expand'}</span>
                  </div>
                </button>
              `;
            }).join('')}
          </div>

          <!-- Step 2: Smooth Animated Dropdown Drawer Showing ONLY the 3 Personas of the Clicked Sub-Pillar -->
          ${activeSubPillar ? `
            <div id="subPillarPersonasDrawerEl" class="subpillar-personas-drawer" style="--sp-color: ${activeSubPillar.color};">
              <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom:16px;">
                <div style="display:flex; align-items:center; gap:10px;">
                  <span style="padding:4px 11px; border-radius:8px; background:${activeSubPillar.color}; color:#ffffff; font-size:11.5px; font-weight:800; letter-spacing:0.05em; text-transform:uppercase;">
                    ${activeSubPillar.icon} ${activeSubPillar.name}
                  </span>
                  <span style="font-size:14.5px; font-weight:700; color:var(--text-primary);">
                    Select a persona to open their daily journey &amp; AI agents
                  </span>
                </div>
                <button type="button" class="switch-pill" style="padding:4px 12px; font-size:12px;" onclick="selectSubPillarFilter('${activeSubPillar.id}')">
                  ✕ Close Sub-Pillar
                </button>
              </div>

              <div class="persona-cards-grid" style="grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px;">
                ${(activeSubPillar.items || []).map(item => {
                  const p = PERSONAS[item.personaId];
                  if (!p) return '';
                  return `
                    <div class="human-persona-card"
                         style="--dept-accent: ${activeSubPillar.color}; padding: 20px 22px;"
                         onclick="openPersonaPage('${p.id}', true, event)">
                      <div style="display:flex; align-items:center; gap:14px;">
                        <div class="human-avatar-circle" style="--dept-accent: ${activeSubPillar.color}; width:48px; height:48px; font-size:22px;">
                          ${p.icon}
                        </div>
                        <div>
                          <div class="human-role-tag" style="margin-bottom:4px;">👤 Human Persona</div>
                          <div class="human-persona-title" style="font-size:17.5px;">${p.name}</div>
                          <div class="human-persona-sub" style="font-size:12.5px; margin-top:2px;">${activeSubPillar.name}</div>
                        </div>
                      </div>
                      <span class="persona-open-arrow" style="color:${activeSubPillar.color}; font-weight:800; font-size:16px;">&rarr;</span>
                    </div>
                  `;
                }).join('')}
              </div>
            </div>
          ` : ''}
        </div>
      `;
    }"""

    html = re.sub(
        r"    let currentSelectedSubPillarId = 'all';.*?\n    function togglePersonaJourneyStep",
        clean_showcase_js + "\n\n    function togglePersonaJourneyStep",
        html,
        count=1,
        flags=re.S,
    )

    # 6. In openPersonaPage, keep the top switcher pills scoped to the 3 Personas in the SAME Sub-Pillar so the top bar isn't crowded with 12 buttons!
    old_persona_switcher = """            <div class="persona-switcher-pills">
              ${dept.personaIds.map(pid => {
                const other = PERSONAS[pid];
                if (!other) return '';
                return `
                  <button type="button"
                          class="switch-pill ${pid === p.id ? 'active' : ''}"
                          style="${pid === p.id ? `background:${dept.color}; border-color:${dept.color}; color:#ffffff; font-weight:700;` : ''}"
                          onclick="openPersonaPage('${pid}', true, event)">
                    ${other.icon} ${other.name}
                  </button>
                `;
              }).join('')}
            </div>"""

    new_persona_switcher = """            <div class="persona-switcher-pills">
              ${dept.personaIds.filter(pid => PERSONAS[pid] && PERSONAS[pid].subPillarId === p.subPillarId).map(pid => {
                const other = PERSONAS[pid];
                if (!other) return '';
                return `
                  <button type="button"
                          class="switch-pill ${pid === p.id ? 'active' : ''}"
                          style="${pid === p.id ? `background:${p.subPillarColor || dept.color}; border-color:${p.subPillarColor || dept.color}; color:#ffffff; font-weight:700;` : ''}"
                          onclick="openPersonaPage('${pid}', true, event)">
                    ${other.icon} ${other.name}
                  </button>
                `;
              }).join('')}
            </div>"""

    html = html.replace(old_persona_switcher, new_persona_switcher)

    # Also when clicking "Back to 6 Pillars" from a Persona page, keep that Persona's Sub-Pillar expanded so the user returns right where they were!
    html = html.replace(
        "lastPersonaId = personaId;\n      selectedDeptId = p.deptId;",
        "lastPersonaId = personaId;\n      selectedDeptId = p.deptId;\n      currentSelectedSubPillarId = p.subPillarId || null;",
    )

    # 7. In openAgentPage, scope the top sibling agent switcher pills to the 3 Agents in the same Sub-Pillar so the top bar is super clean!
    old_agent_switcher = """      const siblingAgents = ag.isUniversal
        ? UNIVERSAL_AGENT_IDS.map(id => AGENTS[id]).filter(Boolean)
        : Object.values(AGENTS).filter(a => !a.isUniversal && a.deptId === dept.id);"""

    new_agent_switcher = """      const siblingAgents = Object.values(AGENTS).filter(a => a.deptId === dept.id && (!ag.subPillarId || a.subPillarId === ag.subPillarId));"""

    html = html.replace(old_agent_switcher, new_agent_switcher)

    # 8. Enhance Column 2 of the Neural Mind Map (#mindmap) so it groups Personas by Sub-Pillar!
    old_mm_col2 = """              <!-- Column 2: Personas in Selected Domain (Animated on Domain Click) -->
              <div class="mm-col-card" style="animation: ptExpandIn 0.28s var(--ease-spring) forwards;">
                <div class="mm-col-header" style="color:${activeDept.color};">
                  2. Select Persona in ${activeDept.name} (${deptPersonas.length})
                </div>
                ${deptPersonas.map(p => {
                  const isAct = p.id === activePersona.id;
                  return `
                    <button type="button" class="mm-node-btn ${isAct ? 'active' : ''}"
                            style="--node-color:${activeDept.color};"
                            onclick="selectMindMapPersona('${p.id}')">
                      <div>
                        <div style="font-size:14px; font-weight:700; color:var(--text-primary);">
                          ${p.icon} ${p.name}
                        </div>
                        <div style="font-size:12px; color:var(--text-secondary); margin-top:2px;">
                          ${p.timeSaved || '-75% Manual Toil'}
                        </div>
                      </div>
                      <span style="font-family:var(--font-mono); font-size:11.5px; color:${activeDept.color};">
                        ${(p.agentIds || []).length + 4} agents &rarr;
                      </span>
                    </button>
                  `;
                }).join('')}"""

    new_mm_col2 = """              <!-- Column 2: Sub-Pillars & Personas in Selected Pillar -->
              <div class="mm-col-card" style="animation: ptExpandIn 0.28s var(--ease-spring) forwards;">
                <div class="mm-col-header" style="color:${activeDept.color};">
                  2. Sub-Pillars &amp; Personas in ${activeDept.name} (${deptPersonas.length})
                </div>
                ${(activeDept.subPillars || []).map(sp => `
                  <div style="margin-bottom:10px;">
                    <div style="font-family:var(--font-mono); font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:${sp.color}; padding:4px 8px; margin-bottom:6px; border-left:3px solid ${sp.color}; background:rgba(255,255,255,0.03);">
                      ${sp.icon} ${sp.name}
                    </div>
                    ${(sp.items || []).map(it => {
                      const p = PERSONAS[it.personaId];
                      if (!p) return '';
                      const isAct = p.id === activePersona.id;
                      return `
                        <button type="button" class="mm-node-btn ${isAct ? 'active' : ''}"
                                style="--node-color:${sp.color};"
                                onclick="selectMindMapPersona('${p.id}')">
                          <div>
                            <div style="font-size:13.5px; font-weight:700; color:var(--text-primary);">
                              ${p.icon} ${p.name}
                            </div>
                            <div style="font-size:11.5px; color:var(--text-secondary); margin-top:2px;">
                              ✦ ${it.agentName}
                            </div>
                          </div>
                          <span style="font-family:var(--font-mono); font-size:11px; color:${sp.color};">
                            3 agents &rarr;
                          </span>
                        </button>
                      `;
                    }).join('')}
                  </div>
                `).join('')}"""

    html = html.replace(old_mm_col2, new_mm_col2)

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated:", INDEX_PATH)

    # Sync periodic_table.html and mind_map.html
    pt_html = html.replace(
        "handleUrlHash();",
        "if (!window.location.hash) { window.location.hash = '#periodic'; } handleUrlHash();",
        1,
    )
    with open(PERIODIC_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(pt_html)
    print("Updated:", PERIODIC_HTML_PATH)

    mm_html = html.replace(
        "handleUrlHash();",
        "if (!window.location.hash) { window.location.hash = '#mindmap'; } handleUrlHash();",
        1,
    )
    with open(MINDMAP_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(mm_html)
    print("Updated:", MINDMAP_HTML_PATH)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Remove 'AI in Supply Chain Function' from #pageHome (keeping top navbar 'AI Stack' tab intact)
and upgrade Pillar -> Sub-Pillar -> Persona click animations with reliable silky auto-scroll
to the newly revealed stage.
"""

from __future__ import annotations

from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.link_impact_boxes_to_aligned_proofs import build_standalone_variant  # noqa: E402


STAGE_ANIMATION_CSS = """
    /* =========================================================================
       PROGRESSIVE PILLAR -> SUB-PILLAR -> PERSONA STAGE CASCADE & FLOW ANIMATIONS
       ========================================================================= */
    #orgChartSection {
      padding-bottom: clamp(120px, 18vh, 190px) !important;
    }

    .dept-row {
      transition: opacity 0.28s ease;
    }

    .dept-row.has-active-pillar .dept-node:not(.active) {
      opacity: 0.74;
      transform: scale(0.99);
      transition: transform 0.32s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.28s ease, border-color 0.28s ease, box-shadow 0.28s ease;
    }

    .dept-row.has-active-pillar .dept-node:not(.active):hover {
      opacity: 0.98;
      transform: translateY(-4px) scale(1.005);
    }

    .dept-row .dept-node.active {
      transform: translateY(-5px) scale(1.014);
      border-color: var(--dept-accent, #2563eb) !important;
      box-shadow:
        0 20px 44px -14px rgba(15, 23, 42, 0.42),
        0 0 0 2px var(--dept-accent, #2563eb),
        0 0 28px -6px var(--dept-accent, #2563eb) !important;
    }

    html[data-theme="light"] .dept-row .dept-node.active {
      box-shadow:
        0 18px 38px -12px rgba(15, 23, 42, 0.16),
        0 0 0 2.5px var(--dept-accent, #2563eb),
        0 10px 26px -10px var(--dept-accent, #2563eb) !important;
    }

    /* Animated Vertical Flow Connector Stem between Pillar -> Sub-Pillars and Sub-Pillar -> Personas */
    .sc-stage-flow-stem {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      margin: 14px auto -10px;
      position: relative;
      z-index: 4;
      pointer-events: none;
      animation: scStemFadeIn 0.34s cubic-bezier(0.22, 1, 0.36, 1) both;
    }

    .sc-stage-flow-line {
      width: 2.5px;
      height: 32px;
      border-radius: 999px;
      background: linear-gradient(180deg, transparent 0%, var(--stem-color, #2563eb) 45%, var(--stem-color, #2563eb) 100%);
      position: relative;
      overflow: visible;
    }

    .sc-stage-flow-dot {
      width: 9px;
      height: 9px;
      border-radius: 50%;
      background: var(--stem-color, #2563eb);
      box-shadow: 0 0 0 4px color-mix(in srgb, var(--stem-color, #2563eb) 24%, transparent);
      animation: scStemPulseDot 1.5s cubic-bezier(0.22, 1, 0.36, 1) infinite;
    }

    @keyframes scStemFadeIn {
      from { opacity: 0; transform: translateY(-8px) scaleY(0.7); }
      to   { opacity: 1; transform: translateY(0) scaleY(1); }
    }

    @keyframes scStemPulseDot {
      0%, 100% { transform: scale(0.92); opacity: 0.85; }
      50%      { transform: scale(1.22); opacity: 1; }
    }

    @keyframes scStageCardCascade {
      0% {
        opacity: 0;
        transform: translate3d(0, 20px, 0) scale(0.965);
      }
      100% {
        opacity: 1;
        transform: translate3d(0, 0, 0) scale(1);
      }
    }

    @keyframes scDrawerUnfold {
      0% {
        opacity: 0;
        transform: translate3d(0, 18px, 0) scale(0.985);
      }
      100% {
        opacity: 1;
        transform: translate3d(0, 0, 0) scale(1);
      }
    }

    .dept-showcase-box.sc-stage-unfold {
      animation: scDrawerUnfold 0.44s cubic-bezier(0.22, 1, 0.36, 1) both;
    }

    .subpillar-boxes-row .subpillar-box-card {
      animation: scStageCardCascade 0.46s cubic-bezier(0.22, 1, 0.36, 1) both;
      animation-delay: calc(var(--stagger-idx, 0) * 65ms + 50ms);
      transition: transform 0.24s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.24s ease, border-color 0.24s ease, background 0.24s ease;
    }

    .subpillar-boxes-row .subpillar-box-card.active {
      transform: translateY(-4px) scale(1.015);
      border-color: var(--sp-color, #2563eb) !important;
      box-shadow:
        0 16px 34px -12px rgba(15, 23, 42, 0.35),
        0 0 0 2px var(--sp-color, #2563eb) !important;
    }

    .subpillar-personas-drawer {
      animation: scDrawerUnfold 0.42s cubic-bezier(0.22, 1, 0.36, 1) both;
    }

    .subpillar-personas-drawer .human-persona-card {
      animation: scStageCardCascade 0.44s cubic-bezier(0.22, 1, 0.36, 1) both;
      animation-delay: calc(var(--stagger-idx, 0) * 60ms + 45ms);
      transition: transform 0.22s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.22s ease, border-color 0.22s ease;
    }

    @media (prefers-reduced-motion: reduce) {
      .dept-showcase-box.sc-stage-unfold,
      .subpillar-boxes-row .subpillar-box-card,
      .subpillar-personas-drawer,
      .subpillar-personas-drawer .human-persona-card {
        animation: none !important;
      }
    }
"""


SMOOTH_SCROLL_HELPER_JS = """    /* Silky Transform-Immune Auto-Scroll Helper for Pillar -> Sub-Pillar -> Persona Progression */
    let _scGlideRafId = null;

    function getTrueDocumentTop(el) {
      let y = 0;
      let node = el;
      while (node) {
        y += (node.offsetTop || 0);
        node = node.offsetParent;
      }
      return y;
    }

    function smoothGlideToElement(el, offsetPx = 94, durationMs = 560) {
      if (!el || typeof window === 'undefined') return;
      if (_scGlideRafId) {
        cancelAnimationFrame(_scGlideRafId);
        _scGlideRafId = null;
      }
      const startY = window.scrollY || window.pageYOffset || 0;
      const rawTargetY = Math.max(0, getTrueDocumentTop(el) - offsetPx);
      const maxScrollY = Math.max(0, (document.documentElement.scrollHeight || document.body.scrollHeight || 0) - window.innerHeight);
      const targetY = Math.min(rawTargetY, maxScrollY);
      const delta = targetY - startY;
      if (Math.abs(delta) < 6) return;

      const prefersReduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (prefersReduced) {
        window.scrollTo(0, targetY);
        return;
      }

      const startTime = performance.now();
      const cancelOnUserInput = () => {
        if (_scGlideRafId) {
          cancelAnimationFrame(_scGlideRafId);
          _scGlideRafId = null;
        }
        window.removeEventListener('wheel', cancelOnUserInput, { passive: true });
        window.removeEventListener('touchstart', cancelOnUserInput, { passive: true });
      };
      window.addEventListener('wheel', cancelOnUserInput, { passive: true });
      window.addEventListener('touchstart', cancelOnUserInput, { passive: true });

      function step(now) {
        const t = Math.min(1, (now - startTime) / durationMs);
        // Smooth quintic ease-out
        const eased = 1 - Math.pow(1 - t, 4);
        window.scrollTo(0, Math.round(startY + delta * eased));
        if (t < 1) {
          _scGlideRafId = requestAnimationFrame(step);
        } else {
          _scGlideRafId = null;
          window.removeEventListener('wheel', cancelOnUserInput, { passive: true });
          window.removeEventListener('touchstart', cancelOnUserInput, { passive: true });
        }
      }
      _scGlideRafId = requestAnimationFrame(step);
    }
"""


def apply_changes() -> str:
    index_path = ROOT / "index.html"
    html = index_path.read_text(encoding="utf-8")

    # 1. Remove AI in Supply Chain Function section from #pageHome (keeping top navbar 'AI Stack' tab intact!)
    old_home_ai_stack = """    <!-- 3. AI IN SUPPLY CHAIN FUNCTION — 4-LAYER OPERATING MODEL STACK -->
    <section id="aiFunctionStackSection" class="org-section" style="padding-top: 8px; padding-bottom: 76px;">
      <div id="homeAiFunctionStackMount"></div>
    </section>"""
    if old_home_ai_stack in html:
        html = html.replace(old_home_ai_stack, "", 1)

    # 2. Inject Stage Cascade & Flow Stem CSS right before </style> if not already present
    if ".sc-stage-flow-stem" not in html:
        style_end = html.index("</style>")
        html = html[:style_end] + STAGE_ANIMATION_CSS + "\n  </style>" + html[style_end + len("</style>") :]

    # 3. Inject smoothGlideToElement helper right before selectDepartment
    if "function smoothGlideToElement(" not in html:
        target_sel_dept = "    function selectDepartment(deptId, ev) {"
        if target_sel_dept not in html:
            raise RuntimeError("Could not find selectDepartment in index.html")
        html = html.replace(target_sel_dept, SMOOTH_SCROLL_HELPER_JS + "\n" + target_sel_dept, 1)

    # 4. Upgrade renderOrgChart to set .has-active-pillar class on #deptRowContainer and dynamic active meta cue
    old_render_org = """    function renderOrgChart() {
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

    new_render_org = """    function renderOrgChart() {
      const row = document.getElementById('deptRowContainer');
      if (!row) return;
      row.classList.toggle('has-active-pillar', Boolean(selectedDeptId && DEPARTMENTS[selectedDeptId]));
      row.innerHTML = Object.values(DEPARTMENTS).map(dept => {
        const isActive = dept.id === selectedDeptId;
        const subPillars = dept.subPillars || [];
        const defaultMeta = `${subPillars.length} Sub-Pillars · ${dept.personaIds.length} Personas →`;
        const activeMeta = `▾ ${subPillars.length} Sub-Pillars Open Below`;
        return `
          <div class="dept-node ${isActive ? 'active' : ''}"
               data-dept-id="${dept.id}"
               data-default-meta="${defaultMeta}"
               data-active-meta="${activeMeta}"
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
              <span class="dept-anim-meta">${isActive ? activeMeta : defaultMeta}</span>
            </div>
          </div>
        `;
      }).join('');

      renderDepartmentShowcaseBox();
    }"""
    if old_render_org not in html:
        raise RuntimeError("Could not find renderOrgChart block in index.html")
    html = html.replace(old_render_org, new_render_org, 1)

    # 5. Upgrade selectDepartment & switchVerticalTab to use transform-immune smoothGlideToElement
    old_select_dept = """    function selectDepartment(deptId, ev) {
      const sRect = getClickedCardRect(ev);
      selectedDeptId = (selectedDeptId === deptId) ? null : deptId;
      currentSelectedSubPillarId = null;

      // Update active state on the 6 SCOR Pillar cards in-place without re-creating DOM nodes
      document.querySelectorAll('#deptRowContainer .dept-node').forEach(node => {
        const nid = node.getAttribute('data-dept-id');
        const active = nid === selectedDeptId;
        node.classList.toggle('active', active);
      });

      // Synchronize front-page master tab bar
      const activeTabId = selectedDeptId || 'all';
      document.querySelectorAll('#verticalTabsNavBar .v-tab-btn').forEach(b => {
        b.classList.toggle('active', b.getAttribute('data-vtab') === activeTabId);
      });

      renderDepartmentShowcaseBox();
      hydrateAssets();

      if (selectedDeptId && DEPARTMENTS[selectedDeptId]) {
        const dept = DEPARTMENTS[selectedDeptId];
        const showcaseEl = document.getElementById('deptShowcaseBoxEl');
        if (sRect && showcaseEl) {
          animateGenieOutOfBox(sRect, showcaseEl, dept.color);
        }
        setTimeout(() => {
          const outer = document.getElementById('deptShowcaseContainer');
          if (outer) outer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 90);
      }
    }"""

    new_select_dept = """    function selectDepartment(deptId, ev) {
      const sRect = getClickedCardRect(ev);
      selectedDeptId = (selectedDeptId === deptId) ? null : deptId;
      currentSelectedSubPillarId = null;

      const row = document.getElementById('deptRowContainer');
      if (row) row.classList.toggle('has-active-pillar', Boolean(selectedDeptId && DEPARTMENTS[selectedDeptId]));

      // Update active state & meta label on the Pillar cards in-place without re-creating DOM nodes
      document.querySelectorAll('#deptRowContainer .dept-node').forEach(node => {
        const nid = node.getAttribute('data-dept-id');
        const active = nid === selectedDeptId;
        node.classList.toggle('active', active);
        const metaEl = node.querySelector('.dept-anim-meta');
        if (metaEl) {
          const defTxt = node.getAttribute('data-default-meta');
          const actTxt = node.getAttribute('data-active-meta');
          if (defTxt && actTxt) metaEl.textContent = active ? actTxt : defTxt;
        }
      });

      // Synchronize front-page master tab bar
      const activeTabId = selectedDeptId || 'all';
      document.querySelectorAll('#verticalTabsNavBar .v-tab-btn').forEach(b => {
        b.classList.toggle('active', b.getAttribute('data-vtab') === activeTabId);
      });

      renderDepartmentShowcaseBox();
      hydrateAssets();

      if (selectedDeptId && DEPARTMENTS[selectedDeptId]) {
        const dept = DEPARTMENTS[selectedDeptId];
        const showcaseEl = document.getElementById('deptShowcaseBoxEl');
        if (sRect && showcaseEl) {
          animateGenieOutOfBox(sRect, showcaseEl, dept.color);
        }
        requestAnimationFrame(() => {
          const outer = document.getElementById('deptShowcaseContainer');
          if (outer) smoothGlideToElement(outer, 92, 580);
        });
      } else if (row) {
        requestAnimationFrame(() => {
          smoothGlideToElement(row, 110, 480);
        });
      }
    }"""
    if old_select_dept not in html:
        raise RuntimeError("Could not find selectDepartment block in index.html")
    html = html.replace(old_select_dept, new_select_dept, 1)

    old_switch_scroll = """        setTimeout(() => {
          const showcase = document.getElementById('deptShowcaseBoxEl');
          if (showcase) showcase.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 80);"""
    new_switch_scroll = """        requestAnimationFrame(() => {
          const outer = document.getElementById('deptShowcaseContainer');
          if (outer) smoothGlideToElement(outer, 92, 580);
        });"""
    if old_switch_scroll in html:
        html = html.replace(old_switch_scroll, new_switch_scroll, 1)

    # 6. Upgrade selectSubPillarFilter & renderDepartmentShowcaseBox with flow connector stems, staggered cascades & auto-scroll to Personas!
    old_subpillar_and_showcase = """    function selectSubPillarFilter(spId, ev) {
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

    new_subpillar_and_showcase = """    function selectSubPillarFilter(spId, ev) {
      const sRect = ev ? getClickedCardRect(ev) : null;
      currentSelectedSubPillarId = (currentSelectedSubPillarId === spId) ? null : spId;
      renderDepartmentShowcaseBox();
      if (currentSelectedSubPillarId) {
        const drawerEl = document.getElementById('subPillarPersonasDrawerEl');
        const anchorEl = document.getElementById('subPillarPersonasAnchorEl') || drawerEl;
        if (sRect && drawerEl && typeof animateGenieOutOfBox === 'function') {
          const dept = DEPARTMENTS[selectedDeptId];
          const sp = (dept && dept.subPillars || []).find(s => s.id === currentSelectedSubPillarId);
          animateGenieOutOfBox(sRect, drawerEl, (sp && sp.color) || (dept && dept.color) || '#2563eb');
        }
        requestAnimationFrame(() => {
          if (anchorEl) smoothGlideToElement(anchorEl, 118, 540);
        });
      } else {
        requestAnimationFrame(() => {
          const outer = document.getElementById('deptShowcaseContainer');
          if (outer) smoothGlideToElement(outer, 92, 460);
        });
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
        <div class="sc-stage-flow-stem" style="--stem-color: ${dept.color};" aria-hidden="true">
          <div class="sc-stage-flow-line"></div>
          <div class="sc-stage-flow-dot"></div>
        </div>
        <div id="deptShowcaseBoxEl" class="dept-showcase-box sc-stage-unfold" style="--dept-accent: ${dept.color}; padding: 28px 30px;">
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
                        style="--sp-color: ${sp.color}; --stagger-idx: ${idx};"
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

          <!-- Step 2: Smooth Animated Dropdown Drawer Showing ONLY the Personas of the Clicked Sub-Pillar -->
          ${activeSubPillar ? `
            <div id="subPillarPersonasAnchorEl" style="height:1px; width:100%;"></div>
            <div class="sc-stage-flow-stem" style="--stem-color: ${activeSubPillar.color}; margin: 16px auto 6px;" aria-hidden="true">
              <div class="sc-stage-flow-line" style="height: 22px;"></div>
              <div class="sc-stage-flow-dot"></div>
            </div>
            <div id="subPillarPersonasDrawerEl" class="subpillar-personas-drawer" style="--sp-color: ${activeSubPillar.color}; margin-top: 8px;">
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
                ${(activeSubPillar.items || []).map((item, pIdx) => {
                  const p = PERSONAS[item.personaId];
                  if (!p) return '';
                  return `
                    <div class="human-persona-card"
                         style="--dept-accent: ${activeSubPillar.color}; --stagger-idx: ${pIdx}; padding: 20px 22px;"
                         onclick="openPersonaPage('${p.id}', true, event)">
                      <div style="display:flex; align-items:center; gap:14px;">
                        <div class="human-avatar-circle" style="--dept-accent: ${activeSubPillar.color}; width:48px; height:48px; font-size:22px;">
                          ${p.icon}
                        </div>
                        <div>
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

    if old_subpillar_and_showcase not in html:
        raise RuntimeError("Could not find selectSubPillarFilter / renderDepartmentShowcaseBox block in index.html")
    html = html.replace(old_subpillar_and_showcase, new_subpillar_and_showcase, 1)

    # 7. Also upgrade goToOrgChart() to use smoothGlideToElement
    old_goto_org = """      setTimeout(() => {
        const el = document.getElementById('orgChartSection');
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 40);"""
    new_goto_org = """      requestAnimationFrame(() => {
        const el = document.getElementById('orgChartSection');
        if (el) smoothGlideToElement(el, 74, 540);
      });"""
    if old_goto_org in html:
        html = html.replace(old_goto_org, new_goto_org, 1)

    index_path.write_text(html, encoding="utf-8")
    return html


def main() -> None:
    updated_index = apply_changes()

    periodic_html = build_standalone_variant(
        updated_index, "#periodic", "openPeriodicTablePage('all', null, false)"
    )
    mindmap_html = build_standalone_variant(
        updated_index, "#mindmap", "openMindMapPage('all', null, false)"
    )

    (ROOT / "periodic_table.html").write_text(periodic_html, encoding="utf-8")
    (ROOT / "mind_map.html").write_text(mindmap_html, encoding="utf-8")

    for mirror_dir in ("docs", "zipline_dist"):
        mdir = ROOT / mirror_dir
        if mdir.is_dir():
            for fname in ("index.html", "periodic_table.html", "mind_map.html"):
                shutil.copy2(ROOT / fname, mdir / fname)
                print(f"Synced {mirror_dir}/{fname}")

    print("Successfully removed AI Stack from front page and upgraded Pillar -> Sub-Pillar -> Persona scroll & cascade animations!")


if __name__ == "__main__":
    main()

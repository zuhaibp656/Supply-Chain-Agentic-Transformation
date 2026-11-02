#!/usr/bin/env python3
"""Upgrades `index.html`, `periodic_table.html`, and `mind_map.html` with the Immaculate v2.0 Enterprise Twin Overlay Engine.

Guarantees zero breakage across all 10 portal views while supporting:
  1. Optically framed, contrast-plated real corporate logos (`.sc-twin-logo-plate`) in Navbar, Hero & Context Bar.
  2. Dynamic renaming of 6 Pillars, 20 Sub-Pillars, and 4 Cross-Pillar Process Journeys (`VALUE_CHAINS`).
  3. Grounded corporate job titles & Red/Green daily toil scenarios across all 60 Personas (`#persona/<id>`).
  4. Intelligent hiding of division-irrelevant agents (`hidden_agent_ids`) with clean count updates,
     Value Chain stage remapping guards, and a 1-click `'Show All 60'` toggle—while keeping 100% of
     Demo Agent names, 4-stage SVG workflows, Cost/ROI math, Playbook links, and Case Studies intact.
  5. Seamless integration with `/welcome` Studio, `/t/<slug>` server hydration (`window.__INITIAL_TWIN__`),
     `?twin=<slug>` URL links, and embedded flagship twins (`EMBEDDED_TWINS_V2`) for offline/Zipline parity.
"""

from __future__ import annotations

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
TWINS_V2_DIR = ROOT / "data" / "twins" / "v2"

CSS_MARKER_START = "/* === ENTERPRISE TWIN STUDIO V2 OVERLAY STYLES START === */"
CSS_MARKER_END = "/* === ENTERPRISE TWIN STUDIO V2 OVERLAY STYLES END === */"

TWIN_CSS = f"""
    {CSS_MARKER_START}
    .sc-twin-nav-lockup {{
      display: inline-flex;
      align-items: center;
      gap: 9px;
      flex-wrap: nowrap;
      max-width: 440px;
    }}
    .sc-twin-logo-plate {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      height: 28px;
      min-width: 28px;
      max-width: 104px;
      padding: 3px 8px;
      border-radius: 7px;
      flex-shrink: 0;
      box-sizing: border-box;
      transition: transform 0.2s var(--ease-spring);
    }}
    .sc-twin-logo-plate.plate-light {{
      background: #ffffff;
      border: 1px solid rgba(148, 163, 184, 0.36);
      box-shadow: 0 2px 6px rgba(2, 6, 23, 0.20);
    }}
    .sc-twin-logo-plate.plate-dark {{
      background: #0f172a;
      border: 1px solid rgba(148, 163, 184, 0.30);
      box-shadow: 0 2px 6px rgba(2, 6, 23, 0.28);
    }}
    .sc-twin-logo-plate.plate-self {{
      background: transparent;
      padding: 1px;
      border-radius: 6px;
      overflow: hidden;
    }}
    .sc-twin-logo-plate img {{
      max-height: 20px;
      max-width: 88px;
      width: auto;
      height: auto;
      object-fit: contain;
      display: block;
    }}
    .sc-twin-logo-plate.size-lg {{
      height: 40px;
      max-width: 146px;
      padding: 5px 12px;
      border-radius: 10px;
    }}
    .sc-twin-logo-plate.size-lg img {{
      max-height: 28px;
      max-width: 122px;
    }}
    .sc-twin-nav-co {{
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 800;
      color: var(--text-primary);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 185px;
    }}
    .sc-twin-nav-div {{
      font-size: 11px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 999px;
      background: rgba(66, 133, 244, 0.14);
      color: var(--sc-cyan);
      border: 1px solid rgba(66, 133, 244, 0.32);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 175px;
    }}
    .sc-twin-hero-cobrand {{
      display: inline-flex;
      align-items: center;
      gap: 12px;
      padding: 7px 16px 7px 9px;
      margin-bottom: 18px;
      border-radius: 999px;
      background: rgba(15, 23, 42, 0.76);
      border: 1px solid var(--border-strong);
      backdrop-filter: blur(12px);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.26);
    }}
    html[data-theme="light"] .sc-twin-hero-cobrand {{
      background: rgba(255, 255, 255, 0.92);
      box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
    }}
    .sc-twin-context-bar {{
      margin: 0 auto 26px auto;
      padding: 18px 22px;
      border-radius: 18px;
      background: var(--bg-card);
      border: 1px solid var(--border-strong);
      border-left: 5px solid var(--sc-cyan);
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.22);
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 18px;
      flex-wrap: wrap;
    }}
    html[data-theme="light"] .sc-twin-context-bar {{
      box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    }}
    .sc-twin-term-chip {{
      display: inline-flex;
      align-items: center;
      padding: 3px 10px;
      border-radius: 999px;
      font-size: 11.5px;
      font-weight: 600;
      background: rgba(66, 133, 244, 0.10);
      color: var(--text-primary);
      border: 1px solid var(--border-strong);
    }}
    .sc-twin-action-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 13px;
      border-radius: 10px;
      font-family: var(--font-sans);
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      background: var(--bg-surface);
      color: var(--text-primary);
      border: 1px solid var(--border-strong);
      transition: all 0.18s ease;
    }}
    .sc-twin-action-btn:hover {{
      border-color: var(--sc-cyan);
      transform: translateY(-1px);
    }}
    .sc-twin-agent-lens {{
      margin: 0 0 18px 0;
      padding: 13px 18px;
      border-radius: 14px;
      background: var(--bg-card);
      border: 1px solid var(--border-strong);
      border-left: 4px solid var(--sc-cyan);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      flex-wrap: wrap;
    }}
    .nav-pill-btn.twin-studio-pill {{
      border: 1px solid rgba(66, 133, 244, 0.38);
      background: rgba(66, 133, 244, 0.10);
      font-weight: 700;
    }}
    {CSS_MARKER_END}
"""


def build_embedded_twins_js() -> str:
    """Loads our pre-seeded v2 flagship division twins so static/offline mode works instantaneously."""
    twins = {}
    if TWINS_V2_DIR.exists():
        for p in sorted(TWINS_V2_DIR.glob("*.json")):
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
                if d.get("schema_version") == "2.0" and d.get("twin_slug"):
                    twins[d["twin_slug"]] = d
            except Exception:
                continue
    return "const EMBEDDED_TWINS_V2 = " + json.dumps(twins, ensure_ascii=False) + ";"


def build_v2_modal_html() -> str:
    return """  <!-- =========================================================================
       ENTERPRISE TWIN STUDIO MODAL V2 (DIVISION-AWARE + CAREER GROUNDED)
       ========================================================================= -->
  <div id="enterpriseTwinModal" class="modal-overlay" style="display:none; position:fixed; inset:0; z-index:99999; background:rgba(2,6,18,0.82); backdrop-filter:blur(16px); align-items:center; justify-content:center; padding:20px;">
    <div class="modal-card" style="background:var(--bg-card); border:1px solid var(--border-strong); border-radius:24px; max-width:900px; width:100%; max-height:90vh; overflow-y:auto; padding:30px 32px; box-shadow:0 30px 90px rgba(0,0,0,0.65); position:relative; color:var(--text-primary);">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px; margin-bottom:16px;">
        <div>
          <div style="font-size:11.5px; font-weight:800; letter-spacing:0.08em; text-transform:uppercase; color:var(--g-blue); margin-bottom:4px;">
            Enterprise Twin Studio · Gemini 3.1 Pro + 3.8 Flash
          </div>
          <h2 style="font-family:var(--font-display); font-size:23px; font-weight:800; color:var(--text-primary); margin:0;">
            Tailor Supply Chain Portal to Any Company &amp; Division
          </h2>
          <div style="font-size:13.5px; color:var(--text-secondary); margin-top:4px;">
            Downloads the official corporate logo, adapts process names &amp; 60 job titles to career listings, and hides division-irrelevant agents while keeping all Demo AI Agents intact.
          </div>
        </div>
        <div style="display:flex; gap:8px; flex-shrink:0;">
          <a id="openFullWelcomeStudioLink" href="/welcome" style="display:none; text-decoration:none;" class="sc-twin-action-btn">
            ↗ Full Welcome Studio
          </a>
          <button type="button" class="back-btn" style="padding:6px 14px; font-size:13px;" onclick="closeEnterpriseTwinModal()">
            ✕ Close
          </button>
        </div>
      </div>

      <!-- Intake Form -->
      <div style="background:var(--bg-surface); border:1px solid var(--border-strong); border-radius:18px; padding:20px 22px; margin-bottom:22px;">
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:14px; margin-bottom:14px;">
          <div>
            <label style="display:block; font-size:11.5px; font-weight:700; color:var(--text-secondary); margin-bottom:6px; text-transform:uppercase; letter-spacing:0.05em;">
              Company Name <span style="color:var(--g-red);">*</span>
            </label>
            <input type="text" id="twinCompanyInput" class="twin-input-field" placeholder="e.g. ITC Limited, Aditya Birla Group, Unilever..." value="" style="width:100%; padding:10px 13px; border-radius:10px; background:var(--bg-card); color:var(--text-primary); border:1px solid var(--border-strong); font-size:14px;" />
          </div>
          <div>
            <label style="display:block; font-size:11.5px; font-weight:700; color:var(--text-secondary); margin-bottom:6px; text-transform:uppercase; letter-spacing:0.05em;">
              Business Division / Org Unit
            </label>
            <input type="text" id="twinDivisionInput" class="twin-input-field" placeholder="e.g. Tobacco (ILTD & TM&D), UltraTech Cement, Foods..." value="" style="width:100%; padding:10px 13px; border-radius:10px; background:var(--bg-card); color:var(--text-primary); border:1px solid var(--border-strong); font-size:14px;" />
          </div>
          <div>
            <label style="display:block; font-size:11.5px; font-weight:700; color:var(--text-secondary); margin-bottom:6px; text-transform:uppercase; letter-spacing:0.05em;">
              Primary Geography
            </label>
            <input type="text" id="twinGeoInput" class="twin-input-field" placeholder="e.g. India, Global, North America..." value="India" style="width:100%; padding:10px 13px; border-radius:10px; background:var(--bg-card); color:var(--text-primary); border:1px solid var(--border-strong); font-size:14px;" />
          </div>
        </div>

        <div style="margin-bottom:14px;">
          <label style="display:block; font-size:11.5px; font-weight:700; color:var(--text-secondary); margin-bottom:6px; text-transform:uppercase; letter-spacing:0.05em;">
            Optional Persona, Process Vocabulary or Custom Logo URL
          </label>
          <div style="display:grid; grid-template-columns: 2fr 1fr; gap:12px;">
            <input type="text" id="twinFocusInput" class="twin-input-field" placeholder="e.g. Calls distribution TM&D, Wholesale Dealers (WD), SAP S/4HANA..." style="width:100%; padding:10px 13px; border-radius:10px; background:var(--bg-card); color:var(--text-primary); border:1px solid var(--border-strong); font-size:13.5px;" />
            <input type="text" id="twinLogoUrlInput" class="twin-input-field" placeholder="Optional Logo HTTPS URL" style="width:100%; padding:10px 13px; border-radius:10px; background:var(--bg-card); color:var(--text-primary); border:1px solid var(--border-strong); font-size:13.5px;" />
          </div>
        </div>

        <div style="display:flex; flex-wrap:wrap; gap:12px; align-items:center; justify-content:space-between;">
          <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <button type="button" onclick="executeTwinGeneration()" style="display:inline-flex; align-items:center; gap:8px; padding:11px 22px; border-radius:11px; background:var(--g-blue); color:#ffffff; font-family:var(--font-display); font-size:14px; font-weight:700; border:none; cursor:pointer;">
              <span>✦ Synthesize &amp; Apply Company Portal</span>
            </button>
            <button type="button" class="sc-twin-action-btn" onclick="switchClientTwin('reset')">
              ↺ Reset to Base Industry-Agnostic Portal (60 Agents)
            </button>
          </div>
          <label style="display:inline-flex; align-items:center; gap:6px; font-size:12px; color:var(--text-secondary); cursor:pointer;">
            <input type="checkbox" id="twinForceRefreshCheckbox" />
            <span>Force fresh re-synthesis</span>
          </label>
        </div>

        <!-- Streaming Synthesis HUD -->
        <div id="twinProgressHud" style="display:none; margin-top:16px; padding:16px; border-radius:12px; background:var(--bg-card); border:1px solid var(--border-strong);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span id="hudStatusText" style="font-family:var(--font-mono); font-size:12.5px; color:var(--g-blue); font-weight:700;">
              Initializing Enterprise Twin Agent...
            </span>
            <span id="hudPercentText" style="font-family:var(--font-mono); font-size:12px; color:var(--g-green); font-weight:700;">0%</span>
          </div>
          <div style="height:6px; background:rgba(148,163,184,0.2); border-radius:10px; overflow:hidden; margin-bottom:10px;">
            <div id="hudProgressBar" style="width:0%; height:100%; background:linear-gradient(90deg, var(--g-blue), var(--g-green)); transition:width 0.3s ease;"></div>
          </div>
          <div id="hudStepLog" style="font-family:var(--font-mono); font-size:11.5px; color:var(--text-secondary); line-height:1.65;"></div>
        </div>
      </div>

      <!-- Instant Saved Company & Division Portals -->
      <div style="font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.07em; color:var(--text-secondary); margin-bottom:10px;">
        Saved Company &amp; Division Portals (Instant Launch):
      </div>
      <div id="modalSavedTwinsGrid" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(245px, 1fr)); gap:10px;"></div>
    </div>
  </div>"""


def build_v2_engine_js(embedded_twins_js: str) -> str:
    return f"""    /* =========================================================================
       ENTERPRISE TWIN STUDIO V2 — IMMACULATE ZERO-BREAKAGE OVERLAY ENGINE
       ========================================================================= */
    {embedded_twins_js}

    let BASELINE_DEPARTMENTS = null;
    let BASELINE_PERSONAS = null;
    let BASELINE_AGENTS = null;
    let BASELINE_VALUE_CHAINS = null;
    let CURRENT_TWIN = null;
    let TWIN_SHOW_ALL_60 = false;
    let STUDIO_BACKEND_AVAILABLE = false;

    function escTwinHtml(str) {{
      return String(str == null ? '' : str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }}

    function ensureTwinBaselines() {{
      if (!BASELINE_DEPARTMENTS) BASELINE_DEPARTMENTS = JSON.parse(JSON.stringify(DEPARTMENTS));
      if (!BASELINE_PERSONAS) BASELINE_PERSONAS = JSON.parse(JSON.stringify(PERSONAS));
      if (!BASELINE_AGENTS) BASELINE_AGENTS = JSON.parse(JSON.stringify(AGENTS));
      if (!BASELINE_VALUE_CHAINS) BASELINE_VALUE_CHAINS = JSON.parse(JSON.stringify(VALUE_CHAINS));
    }}

    function restoreCanonicalBaselines() {{
      ensureTwinBaselines();
      for (const k of Object.keys(DEPARTMENTS)) delete DEPARTMENTS[k];
      for (const k of Object.keys(BASELINE_DEPARTMENTS)) {{
        DEPARTMENTS[k] = JSON.parse(JSON.stringify(BASELINE_DEPARTMENTS[k]));
      }}
      for (const k of Object.keys(PERSONAS)) delete PERSONAS[k];
      for (const k of Object.keys(BASELINE_PERSONAS)) {{
        PERSONAS[k] = JSON.parse(JSON.stringify(BASELINE_PERSONAS[k]));
      }}
      for (const k of Object.keys(AGENTS)) delete AGENTS[k];
      for (const k of Object.keys(BASELINE_AGENTS)) {{
        AGENTS[k] = JSON.parse(JSON.stringify(BASELINE_AGENTS[k]));
      }}
      for (const k of Object.keys(VALUE_CHAINS)) delete VALUE_CHAINS[k];
      for (const k of Object.keys(BASELINE_VALUE_CHAINS)) {{
        VALUE_CHAINS[k] = JSON.parse(JSON.stringify(BASELINE_VALUE_CHAINS[k]));
      }}
    }}

    function renderAdaptiveTwinLogoBadge(brand, sizeClass = '') {{
      if (!brand) return '';
      const logo = brand.logo || {{}};
      const uri = logo.data_uri || '';
      const rawPlate = logo.plate_style || 'light_plate';
      const plateCls = rawPlate === 'dark_plate' ? 'plate-dark' : (rawPlate === 'self_plated' ? 'plate-self' : 'plate-light');
      const mono = escTwinHtml(logo.monogram || (brand.canonical_name || 'SC').slice(0, 2).toUpperCase());
      if (!uri) {{
        return `<span class="sc-twin-logo-plate plate-dark ${{sizeClass}}" style="font-family:var(--font-display); font-weight:800; font-size:12px; color:#fff;">${{mono}}</span>`;
      }}
      return `<span class="sc-twin-logo-plate ${{plateCls}} ${{sizeClass}}"><img src="${{escTwinHtml(uri)}}" alt="${{escTwinHtml(brand.canonical_name || 'Company')}} logo" loading="eager" /></span>`;
    }}

    function renderAgentTwinDivisionBanner(ag) {{
      if (!CURRENT_TWIN || !ag) return '';
      const brand = CURRENT_TWIN.brand || {{}};
      const disp = CURRENT_TWIN.display_label || brand.canonical_name || CURRENT_TWIN.canonicalName || '';
      const ctx = ag.twinDivisionContext || '';
      if (!disp || !ctx) return '';
      return `
        <div class="sc-twin-agent-lens">
          <div style="display:flex; align-items:center; gap:12px; flex:1; min-width:240px;">
            ${{renderAdaptiveTwinLogoBadge(brand)}}
            <div style="font-size:13.5px; line-height:1.5; color:var(--text-primary);">
              <strong style="color:var(--sc-cyan);">${{escTwinHtml(disp)}} Operational Lens:</strong>
              <span> ${{escTwinHtml(ctx)}}</span>
            </div>
          </div>
          <span style="font-size:11.5px; font-weight:700; color:var(--text-muted); white-space:nowrap;">
            Core Demo Engine &amp; Data Preserved
          </span>
        </div>
      `;
    }}

    function updateNavbarAndTabCounts() {{
      const pCount = Object.keys(PERSONAS).length;
      const aCount = Object.keys(AGENTS).length;
      const navBtns = document.querySelectorAll('.nav-right .nav-pill-btn');
      navBtns.forEach(btn => {{
        const txt = btn.textContent || '';
        if (txt.includes('Personas (')) btn.textContent = `Personas (${{pCount}}) ▾`;
        if (txt.includes('Agents (')) btn.textContent = `Agents (${{aCount}}) ▾`;
      }});

      const allTabTag = document.querySelector('#verticalTabsNavBar button[data-vtab="all"] .v-tab-tag');
      let totalSp = 0;
      Object.values(DEPARTMENTS).forEach(d => {{
        const spLen = (d.subPillars || []).length;
        totalSp += spLen;
        const tabTag = document.querySelector(`#verticalTabsNavBar button[data-vtab="${{d.id}}"] .v-tab-tag`);
        if (tabTag) tabTag.textContent = `${{spLen}} Sub-Pillars · ${{d.personaIds.length}} Personas`;
      }});
      if (allTabTag) allTabTag.textContent = `${{totalSp}} Sub-Pillars · ${{pCount}} Personas`;
      return {{ pCount, aCount, totalSp }};
    }}

    function mountTwinContextBar() {{
      let bar = document.getElementById('twinActiveContextBar');
      const orgSec = document.getElementById('orgChartSection');
      const cfoWrap = orgSec ? orgSec.querySelector('.cfo-root-wrapper') : null;
      if (!orgSec || !cfoWrap) return;

      if (!CURRENT_TWIN) {{
        if (bar) bar.remove();
        const heroBanner = document.getElementById('twinHeroCoBrandBanner');
        if (heroBanner) heroBanner.remove();
        return;
      }}

      if (!bar) {{
        bar = document.createElement('div');
        bar.id = 'twinActiveContextBar';
        bar.className = 'sc-twin-context-bar';
        orgSec.insertBefore(bar, cfoWrap);
      }}

      const brand = CURRENT_TWIN.brand || {{}};
      const disp = CURRENT_TWIN.display_label || brand.canonical_name || CURRENT_TWIN.canonicalName || 'Enterprise';
      const thesis = brand.executive_thesis || CURRENT_TWIN.executiveThesis || '';
      const terms = CURRENT_TWIN.terminology_highlights || [];
      const hiddenIds = CURRENT_TWIN.hidden_agent_ids || [];
      const hiddenCount = hiddenIds.length;
      const activeCount = 60 - (TWIN_SHOW_ALL_60 ? 0 : hiddenCount);

      bar.innerHTML = `
        <div style="display:flex; align-items:flex-start; gap:14px; flex:1; min-width:280px;">
          ${{renderAdaptiveTwinLogoBadge(brand, 'size-lg')}}
          <div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:4px;">
              <span style="font-family:var(--font-display); font-size:17px; font-weight:800; color:var(--text-primary);">${{escTwinHtml(disp)}}</span>
              <span style="font-size:11px; font-weight:700; padding:2px 9px; border-radius:999px; background:rgba(52,168,83,0.14); color:var(--g-green); border:1px solid rgba(52,168,83,0.34);">
                ✓ Tailored Supply Chain Twin
              </span>
            </div>
            ${{thesis ? `<div style="font-size:13.5px; color:var(--text-secondary); line-height:1.55; max-width:880px; margin-bottom:${{terms.length ? '8px' : '0'}};">${{escTwinHtml(thesis)}}</div>` : ''}}
            ${{terms.length ? `<div style="display:flex; flex-wrap:wrap; gap:6px;">${{terms.map(t => `<span class="sc-twin-term-chip">${{escTwinHtml(t)}}</span>`).join('')}}</div>` : ''}}
          </div>
        </div>
        <div style="display:flex; flex-direction:column; align-items:flex-end; gap:8px;">
          <div style="display:flex; flex-wrap:wrap; gap:8px; justify-content:flex-end;">
            ${{hiddenCount > 0 ? `
              <button type="button" class="sc-twin-action-btn" onclick="toggleTwinShowAllAgents()" title="Toggle division-irrelevant agents">
                ${{TWIN_SHOW_ALL_60
                  ? `🎯 Filter to Relevant (${{60 - hiddenCount}}/60)`
                  : `👁️ Showing ${{activeCount}}/60 Relevant (${{hiddenCount}} Hidden · Show All)`}}
              </button>
            ` : `
              <span style="font-size:12px; font-weight:700; padding:7px 11px; border-radius:10px; background:var(--bg-surface); border:1px solid var(--border-subtle); color:var(--text-secondary);">
                🎯 All 60/60 Agents Relevant
              </span>
            `}}
            <button type="button" class="sc-twin-action-btn" onclick="openTwinStudioEntry(event)">
              ⇄ Switch Company
            </button>
            <button type="button" class="sc-twin-action-btn" onclick="switchClientTwin('reset')">
              ↺ Base Framework
            </button>
          </div>
        </div>
      `;
    }}

    function toggleTwinShowAllAgents() {{
      if (!CURRENT_TWIN) return;
      TWIN_SHOW_ALL_60 = !TWIN_SHOW_ALL_60;
      applyBrowserTwin(CURRENT_TWIN, {{ preserveShowAllFlag: true }});
    }}

    function applyBrowserTwin(twinData, opts = {{}}) {{
      if (!twinData) return;
      if (!opts.preserveShowAllFlag) TWIN_SHOW_ALL_60 = false;
      ensureTwinBaselines();
      restoreCanonicalBaselines();

      CURRENT_TWIN = twinData;
      const isV2 = twinData.schema_version === '2.0' || Boolean(twinData.brand);
      const brand = isV2 ? (twinData.brand || {{}}) : {{
        canonical_name: twinData.canonicalName || twinData.company_name || 'Enterprise',
        division_name: twinData.division_name || '',
        brand_accent: twinData.brandAccent || '#4285f4',
        executive_title: twinData.executiveTitle || ('Chief Supply Chain Officer, ' + (twinData.canonicalName || 'Enterprise')),
        executive_thesis: twinData.executiveThesis || '',
        logo: {{ data_uri: '', monogram: (twinData.canonicalName || 'SC').slice(0, 2).toUpperCase(), plate_style: 'dark_plate' }}
      }};

      const cName = brand.canonical_name || twinData.canonical_name || twinData.canonicalName || 'Enterprise';
      const divName = brand.division_name || twinData.division_name || '';
      const dispLabel = twinData.display_label || (divName ? `${{cName}} — ${{divName}}` : cName);
      const accent = brand.brand_accent || '#4285f4';

      // 1. Apply Pillar & Sub-Pillar Process Renaming
      const pOvMap = twinData.pillar_overrides || {{}};
      const spOvMap = twinData.sub_pillar_overrides || {{}};
      Object.values(DEPARTMENTS).forEach(dept => {{
        const po = pOvMap[dept.id];
        if (po) {{
          if (po.custom_tagline) dept.tagline = po.custom_tagline;
          if (po.custom_subtitle) dept.subtitle = po.custom_subtitle;
        }}
        (dept.subPillars || []).forEach(sp => {{
          const spo = spOvMap[sp.id];
          if (spo && spo.custom_name) {{
            sp.canonicalName = sp.name;
            sp.name = spo.custom_name;
          }}
        }});
      }});

      // 2. Apply 60 Persona Job Titles & Daily Toils
      const perMap = twinData.persona_overrides || twinData.personaOverrides || {{}};
      Object.keys(perMap).forEach(pid => {{
        const p = PERSONAS[pid];
        if (!p) return;
        const po = perMap[pid];
        if (po.title) p.name = po.title;
        if (po.role) p.role = po.role;
        if (po.summary) p.summary = po.summary;
        if (po.grounding_source) p.groundingSource = po.grounding_source;
        const beforeTxt = po.manual_toil || po.manualToil;
        const afterTxt = po.agentic_impact || po.agenticImpact;
        if (p.dayInLife && p.dayInLife.length > 0) {{
          const toilSlot = p.dayInLife.find(s => s.isToil) || p.dayInLife[0];
          if (beforeTxt) toilSlot.before = beforeTxt;
          if (afterTxt) toilSlot.after = afterTxt;
        }}
      }});

      // Sync renamed Sub-Pillars & Persona titles onto Sub-Pillar items and Agent metadata
      const agRelMap = twinData.agent_relevance || {{}};
      Object.values(DEPARTMENTS).forEach(dept => {{
        (dept.subPillars || []).forEach(sp => {{
          (sp.items || []).forEach(it => {{
            if (PERSONAS[it.personaId]) {{
              PERSONAS[it.personaId].subPillarName = sp.name;
              it.personaName = PERSONAS[it.personaId].name;
            }}
            if (AGENTS[it.agentId]) {{
              AGENTS[it.agentId].subPillarName = sp.name;
              if (PERSONAS[it.personaId]) {{
                AGENTS[it.agentId].primaryPersonaName = PERSONAS[it.personaId].name;
              }}
              const rel = agRelMap[it.agentId];
              if (rel && rel.division_context) {{
                AGENTS[it.agentId].twinDivisionContext = rel.division_context;
              }}
            }}
          }});
        }});
      }});

      // 3. Apply Smart Division Agent & Paired-Persona Filtering (unless TWIN_SHOW_ALL_60 is true)
      const hiddenAgents = new Set(TWIN_SHOW_ALL_60 ? [] : (twinData.hidden_agent_ids || []));
      const hiddenPersonas = new Set(TWIN_SHOW_ALL_60 ? [] : (twinData.hidden_persona_ids || []));

      if (hiddenAgents.size > 0) {{
        hiddenAgents.forEach(aid => {{ delete AGENTS[aid]; }});
        hiddenPersonas.forEach(pid => {{ delete PERSONAS[pid]; }});

        Object.values(DEPARTMENTS).forEach(dept => {{
          dept.subPillars = (dept.subPillars || [])
            .map(sp => ({{
              ...sp,
              items: (sp.items || []).filter(it => !hiddenAgents.has(it.agentId) && Boolean(AGENTS[it.agentId]))
            }}))
            .filter(sp => sp.items.length > 0);

          dept.agentIds = (dept.agentIds || []).filter(aid => Boolean(AGENTS[aid]));
          dept.personaIds = (dept.personaIds || []).filter(pid => Boolean(PERSONAS[pid]));
        }});
      }}

      // 4. Update 4 Cross-Pillar Process Journeys & Guard Any Stage Referencing a Hidden Agent
      const procMap = twinData.process_overrides || {{}};
      Object.values(VALUE_CHAINS).forEach(vc => {{
        const pr = procMap[vc.id];
        if (pr) {{
          if (pr.custom_title) {{
            vc.shortTitle = pr.custom_title;
            vc.title = pr.custom_title;
          }}
          if (pr.custom_subtitle) vc.cardSubtitle = pr.custom_subtitle;
        }}
        (vc.stages || []).forEach(st => {{
          if (!AGENTS[st.agentId]) {{
            // Remap gracefully to an active agent so clicking stage never fails
            const fallbackAg = Object.values(AGENTS)[0];
            if (fallbackAg) {{
              st.agentId = fallbackAg.id;
              if (fallbackAg.primaryPersonaId && PERSONAS[fallbackAg.primaryPersonaId]) {{
                st.ownerPersonaId = fallbackAg.primaryPersonaId;
              }}
            }}
          }}
          if (st.ownerPersonaId && PERSONAS[st.ownerPersonaId]) {{
            st.ownerLabel = PERSONAS[st.ownerPersonaId].name;
          }}
        }});
      }});

      // 5. Update Brand Accent, Navbar Medallion, Hero Title & CSCO Box
      document.documentElement.style.setProperty('--sc-cyan', accent);
      const counts = updateNavbarAndTabCounts();

      const cscoBadgeEl = document.querySelector('.nav-csco-badge');
      if (cscoBadgeEl) {{
        cscoBadgeEl.innerHTML = `
          <span class="sc-twin-nav-lockup">
            ${{renderAdaptiveTwinLogoBadge(brand)}}
            <span class="sc-twin-nav-co">${{escTwinHtml(cName)}}</span>
            ${{divName ? `<span class="sc-twin-nav-div">${{escTwinHtml(divName)}}</span>` : ''}}
          </span>
        `;
      }}

      const heroContent = document.querySelector('.hero-content');
      const heroTitleEl = document.querySelector('.hero-title');
      if (heroContent && heroTitleEl) {{
        let heroCobrand = document.getElementById('twinHeroCoBrandBanner');
        if (!heroCobrand) {{
          heroCobrand = document.createElement('div');
          heroCobrand.id = 'twinHeroCoBrandBanner';
          heroCobrand.className = 'sc-twin-hero-cobrand';
          heroContent.insertBefore(heroCobrand, heroTitleEl);
        }}
        heroCobrand.innerHTML = `
          ${{renderAdaptiveTwinLogoBadge(brand)}}
          <span style="font-family:var(--font-display); font-size:13.5px; font-weight:700; color:var(--text-primary);">
            ${{escTwinHtml(dispLabel)}}
          </span>
          <span style="font-size:11.5px; font-weight:700; color:var(--g-green);">● Tailored View</span>
        `;
        heroTitleEl.innerHTML = `Agentic Transformation for <span class="gradient-word">${{escTwinHtml(cName)}} Supply Chain</span>`;
      }}

      const cfoTitleEl = document.querySelector('.cfo-box-title');
      const cfoSubEl = document.querySelector('.cfo-box-sub');
      if (cfoTitleEl) cfoTitleEl.textContent = brand.executive_title || `Chief Supply Chain Officer, ${{cName}}`;
      if (cfoSubEl) {{
        cfoSubEl.textContent = `6 Core Operating Pillars · ${{counts.totalSp}} Sub-Pillars · ${{counts.pCount}} Corporate Roles · ${{counts.aCount}} Relevant AI Agents`;
      }}
      document.title = `${{dispLabel}} — Supply Chain Agentic Transformation`;

      // 6. Re-render All Dynamic Surfaces Safely
      mountTwinContextBar();
      renderOrgChart();
      if (typeof renderValueChainEntryCards === 'function') renderValueChainEntryCards();
      if (typeof populateNavbarQuickMenus === 'function') populateNavbarQuickMenus();

      // Refresh active subpage if open
      const activeView = document.querySelector('.page-view.active');
      const activeId = activeView ? activeView.id : 'pageHome';
      if (activeId === 'pagePersona') {{
        if (typeof lastPersonaId !== 'undefined' && PERSONAS[lastPersonaId]) {{
          openPersonaPage(lastPersonaId, false);
        }} else {{
          goHome();
        }}
      }} else if (activeId === 'pageAgent') {{
        if (typeof lastAgentId !== 'undefined' && AGENTS[lastAgentId]) {{
          openAgentPage(lastAgentId, false);
        }} else {{
          goHome();
        }}
      }} else if (activeId === 'pagePeriodic' && typeof openPeriodicTablePage === 'function') {{
        openPeriodicTablePage('all', null, false);
      }} else if (activeId === 'pageMindMap' && typeof openMindMapPage === 'function') {{
        openMindMapPage('all', null, false);
      }} else if (activeId === 'pageCost' && typeof openCostTabPage === 'function') {{
        openCostTabPage('all', null, false);
      }} else if (activeId === 'pageDirectory' && typeof openPersonasDirectoryPage === 'function') {{
        openPersonasDirectoryPage('all', '', false, 'personas');
      }}

      try {{
        localStorage.setItem('ACTIVE_ENTERPRISE_TWIN_V2', JSON.stringify(twinData));
      }} catch (e) {{}}
    }}

    function switchClientTwin(clientKey) {{
      if (clientKey === 'reset') {{
        closeEnterpriseTwinModal();
        CURRENT_TWIN = null;
        TWIN_SHOW_ALL_60 = false;
        try {{
          localStorage.removeItem('ACTIVE_ENTERPRISE_TWIN_V2');
          localStorage.removeItem('ACTIVE_ENTERPRISE_TWIN');
        }} catch (e) {{}}

        restoreCanonicalBaselines();
        document.documentElement.style.setProperty('--sc-cyan', '#4285f4');
        updateNavbarAndTabCounts();

        const cscoBadgeEl = document.querySelector('.nav-csco-badge');
        if (cscoBadgeEl) cscoBadgeEl.textContent = 'Office of the CSCO · Supply Chain';

        const heroTitleEl = document.querySelector('.hero-title');
        if (heroTitleEl) {{
          heroTitleEl.innerHTML = 'Agentic Transformation for <span class="gradient-word">Supply Chain &amp; Demand</span>';
        }}
        const cfoTitleEl = document.querySelector('.cfo-box-title');
        const cfoSubEl = document.querySelector('.cfo-box-sub');
        if (cfoTitleEl) cfoTitleEl.textContent = 'Chief Supply Chain Officer (CSCO)';
        if (cfoSubEl) cfoSubEl.textContent = '6 Core Operating Pillars · 20 Sub-Pillars · 60 Personas · 60 AI Agents';
        document.title = 'Gemini Enterprise — Supply Chain & Demand (Office of the CSCO)';

        mountTwinContextBar();
        renderOrgChart();
        if (typeof renderValueChainEntryCards === 'function') renderValueChainEntryCards();
        if (typeof populateNavbarQuickMenus === 'function') populateNavbarQuickMenus();

        if (window.location.pathname.startsWith('/t/')) {{
          window.location.href = '/base';
          return;
        }}
        goHome();
        return;
      }}

      if (EMBEDDED_TWINS_V2[clientKey]) {{
        closeEnterpriseTwinModal();
        applyBrowserTwin(EMBEDDED_TWINS_V2[clientKey]);
        return;
      }}
      fetch(`/api/v1/twins/${{encodeURIComponent(clientKey)}}`)
        .then(r => r.ok ? r.json() : Promise.reject('not found'))
        .then(d => {{
          if (d && d.overlay) {{
            closeEnterpriseTwinModal();
            applyBrowserTwin(d.overlay);
          }}
        }})
        .catch(() => {{}});
    }}

    function openTwinStudioEntry(ev) {{
      if (ev) ev.stopPropagation();
      if (window.__ENTERPRISE_STUDIO_SERVER__ || STUDIO_BACKEND_AVAILABLE) {{
        window.location.href = '/welcome';
        return;
      }}
      openEnterpriseTwinModal();
    }}

    function openEnterpriseTwinModal() {{
      const m = document.getElementById('enterpriseTwinModal');
      if (m) {{
        m.style.display = 'flex';
        populateModalSavedTwins();
      }}
    }}

    function closeEnterpriseTwinModal() {{
      const m = document.getElementById('enterpriseTwinModal');
      if (m) m.style.display = 'none';
    }}

    function populateModalSavedTwins() {{
      const grid = document.getElementById('modalSavedTwinsGrid');
      if (!grid) return;
      const renderItems = (items) => {{
        grid.innerHTML = items.map(it => {{
          const fakeBrand = {{
            canonical_name: it.company_name,
            logo: {{ data_uri: it.logo_data_uri || '', plate_style: it.logo_plate_style || 'light_plate', monogram: it.logo_monogram || 'SC' }}
          }};
          return `
            <button type="button" onclick="switchClientTwin('${{escTwinHtml(it.twin_slug)}}')" style="text-align:left; background:var(--bg-surface); border:1px solid var(--border-strong); border-radius:14px; padding:12px 14px; cursor:pointer; display:flex; align-items:center; gap:11px; color:var(--text-primary);">
              ${{renderAdaptiveTwinLogoBadge(fakeBrand)}}
              <div style="min-width:0; flex:1;">
                <div style="font-size:13.5px; font-weight:800; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${{escTwinHtml(it.company_name)}}</div>
                <div style="font-size:11.5px; color:var(--text-secondary); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${{escTwinHtml(it.division_name || it.industry_sector || 'Enterprise')}} · ${{it.active_agents_count || 60}}/60 Agents</div>
              </div>
            </button>
          `;
        }}).join('');
      }};

      const localItems = Object.values(EMBEDDED_TWINS_V2).map(ov => ({{
        twin_slug: ov.twin_slug,
        company_name: ov.canonical_name,
        division_name: ov.division_name,
        industry_sector: (ov.brand || {{}}).industry_sector,
        logo_data_uri: ((ov.brand || {{}}).logo || {{}}).data_uri,
        logo_plate_style: ((ov.brand || {{}}).logo || {{}}).plate_style,
        logo_monogram: ((ov.brand || {{}}).logo || {{}}).monogram,
        active_agents_count: ov.active_agents_count || 60
      }}));
      renderItems(localItems);

      fetch('/api/v1/twins')
        .then(r => r.ok ? r.json() : null)
        .then(d => {{
          if (d && Array.isArray(d.twins) && d.twins.length > 0) {{
            STUDIO_BACKEND_AVAILABLE = true;
            const link = document.getElementById('openFullWelcomeStudioLink');
            if (link) link.style.display = 'inline-flex';
            renderItems(d.twins);
          }}
        }})
        .catch(() => {{}});
    }}

    function executeTwinGeneration() {{
      const coEl = document.getElementById('twinCompanyInput');
      const divEl = document.getElementById('twinDivisionInput');
      const geoEl = document.getElementById('twinGeoInput');
      const focusEl = document.getElementById('twinFocusInput');
      const logoEl = document.getElementById('twinLogoUrlInput');
      const refreshEl = document.getElementById('twinForceRefreshCheckbox');

      const company = (coEl ? coEl.value : '').trim() || 'ITC Limited';
      const division = (divEl ? divEl.value : '').trim();
      const geography = (geoEl ? geoEl.value : '').trim() || 'Global';
      const notes = (focusEl ? focusEl.value : '').trim();
      const logoUrl = (logoEl ? logoEl.value : '').trim();
      const forceRefresh = Boolean(refreshEl && refreshEl.checked);

      const hud = document.getElementById('twinProgressHud');
      const hudStatus = document.getElementById('hudStatusText');
      const hudPct = document.getElementById('hudPercentText');
      const hudBar = document.getElementById('hudProgressBar');
      const hudLog = document.getElementById('hudStepLog');
      if (hud) hud.style.display = 'block';
      if (hudLog) hudLog.innerHTML = '';

      const appendStep = (pct, msg, detail) => {{
        if (hudStatus) hudStatus.textContent = msg;
        if (hudPct) hudPct.textContent = pct + '%';
        if (hudBar) hudBar.style.width = pct + '%';
        if (hudLog) {{
          const row = document.createElement('div');
          row.innerHTML = `<span style="color:var(--g-green);">✓</span> ${{escTwinHtml(msg)}} ${{detail ? `<span style="color:var(--text-muted);">— ${{escTwinHtml(detail)}}</span>` : ''}}`;
          hudLog.appendChild(row);
        }}
      }};

      fetch('/api/v1/generate-twin', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{
          company_name: company,
          division_name: division,
          geography: geography,
          focus: notes,
          custom_logo_input: logoUrl,
          force_refresh: forceRefresh
        }})
      }})
        .then(r => r.ok ? r.json() : Promise.reject('backend_offline'))
        .then(data => {{
          appendStep(100, `Portal ready for ${{data.display_label || company}}!`, `Source: ${{data.source}}`);
          if (data.overlay) {{
            applyBrowserTwin(data.overlay);
            setTimeout(() => closeEnterpriseTwinModal(), 500);
          }}
        }})
        .catch(() => {{
          // Offline / Static Zipline fallback: match closest embedded flagship twin or clean generic overlay
          const needle = (company + ' ' + division).toLowerCase();
          let matched = null;
          for (const [slug, ov] of Object.entries(EMBEDDED_TWINS_V2)) {{
            if (needle.includes('tobacco') && slug.includes('tobacco')) {{ matched = ov; break; }}
            if (needle.includes('cement') || needle.includes('ultratech')) {{ if (slug.includes('ultratech')) {{ matched = ov; break; }} }}
            if (needle.includes('hindalco') || needle.includes('metal')) {{ if (slug.includes('hindalco')) {{ matched = ov; break; }} }}
            if (needle.includes('itc') && slug.includes('foods')) matched = ov;
            if (needle.includes('unilever') && slug.includes('unilever')) {{ matched = ov; break; }}
          }}
          if (matched) {{
            const clone = JSON.parse(JSON.stringify(matched));
            clone.canonical_name = company;
            clone.brand.canonical_name = company;
            if (division) {{
              clone.division_name = division;
              clone.brand.division_name = division;
              clone.display_label = `${{company}} — ${{division}}`;
            }} else {{
              clone.display_label = company;
            }}
            appendStep(100, `Applied embedded twin template for ${{clone.display_label}}`, 'Offline / Static Mode');
            applyBrowserTwin(clone);
            setTimeout(() => closeEnterpriseTwinModal(), 500);
          }}
        }});
    }}

    document.addEventListener('DOMContentLoaded', () => {{
      ensureTwinBaselines();

      initPortalTheme();
      hydrateAssets();
      initHeroSupplyChainCanvas();
      renderOrgChart();
      if (typeof mountHomeAiFunctionStack === 'function') mountHomeAiFunctionStack();
      if (typeof renderValueChainEntryCards === 'function') renderValueChainEntryCards();
      if (typeof populateNavbarQuickMenus === 'function') populateNavbarQuickMenus();
      hydrateAssets();
      handleUrlHash();

      // Check backend studio availability quietly
      fetch('/api/v1/health')
        .then(r => r.ok ? r.json() : null)
        .then(d => {{ if (d && d.status === 'healthy') STUDIO_BACKEND_AVAILABLE = true; }})
        .catch(() => {{}});

      const params = new URLSearchParams(window.location.search || '');
      if (params.get('reset_twin') === '1') {{
        try {{
          localStorage.removeItem('ACTIVE_ENTERPRISE_TWIN_V2');
          localStorage.removeItem('ACTIVE_ENTERPRISE_TWIN');
        }} catch (e) {{}}
        return;
      }}

      // Priority 1: Server-hydrated twin injected on `/t/<twin_slug>`
      if (window.__INITIAL_TWIN__) {{
        applyBrowserTwin(window.__INITIAL_TWIN__);
        return;
      }}

      // Priority 2: URL query `?twin=<slug>`
      const urlTwin = params.get('twin');
      if (urlTwin) {{
        if (EMBEDDED_TWINS_V2[urlTwin]) {{
          applyBrowserTwin(EMBEDDED_TWINS_V2[urlTwin]);
        }} else {{
          fetch(`/api/v1/twins/${{encodeURIComponent(urlTwin)}}`)
            .then(r => r.ok ? r.json() : null)
            .then(d => {{ if (d && d.overlay) applyBrowserTwin(d.overlay); }})
            .catch(() => {{}});
        }}
        return;
      }}

      // Priority 3: Restore active v2 twin from localStorage if previously selected
      try {{
        const cachedStr = localStorage.getItem('ACTIVE_ENTERPRISE_TWIN_V2');
        if (cachedStr) {{
          const cached = JSON.parse(cachedStr);
          if (cached && cached.schema_version === '2.0') {{
            applyBrowserTwin(cached);
          }}
        }}
      }} catch (e) {{}}
    }});
"""


def upgrade_single_html_file(path: Path, is_periodic: bool = False, is_mindmap: bool = False) -> None:
    orig_html = path.read_text(encoding="utf-8")
    orig_len = len(orig_html)
    html = orig_html

    # 1. Inject or update CSS block right before `</style>`
    if CSS_MARKER_START in html and CSS_MARKER_END in html:
        i0 = html.index(CSS_MARKER_START)
        i1 = html.index(CSS_MARKER_END, i0) + len(CSS_MARKER_END)
        html = html[:i0] + TWIN_CSS.strip() + html[i1:]
    else:
        style_close = html.index("</style>")
        html = html[:style_close] + TWIN_CSS + "\n  " + html[style_close:]

    # 2. Add `Company Twin` pill button in `<header class="navbar">` if not present
    nav_btn_html = '      <button type="button" class="nav-pill-btn twin-studio-pill" onclick="openTwinStudioEntry(event)">Company Twin</button>\n'
    if 'onclick="openTwinStudioEntry(event)"' not in html:
        target_theme_btn = '      <button type="button" id="themeToggleBtn"'
        if target_theme_btn in html:
            html = html.replace(target_theme_btn, nav_btn_html + target_theme_btn, 1)

    # 3. Inject subtle grounding badge inside `openPersonaPage` if not present
    grounding_line = "${p.groundingSource ? `<div style=\"margin-top:5px; font-size:11.5px; font-weight:700; color:var(--sc-cyan);\">🔍 ${escTwinHtml(p.groundingSource)}</div>` : ''}"
    if "p.groundingSource" not in html:
        persona_sub_target = '<div style="font-size:15px; color:var(--text-secondary); font-weight:600;">${p.subPillarName || dept.name}</div>'
        if persona_sub_target in html:
            html = html.replace(persona_sub_target, persona_sub_target + "\n                " + grounding_line, 1)

    # 4. Inject 1-line `renderAgentTwinDivisionBanner(ag)` inside `openAgentPage` right below `.back-bar`
    if "renderAgentTwinDivisionBanner(ag)" not in html:
        fn_pos = html.index("function openAgentPage(")
        back_bar_pos = html.index('<div class="back-bar">', fn_pos)
        # Find the closing of `.back-bar` right before the hero banner in openAgentPage
        next_comment_pos = html.index("<!--", back_bar_pos + 250)
        # Insert right before the comment following `.back-bar` if it's after persona-switcher-pills
        pills_pos = html.index('<div class="persona-switcher-pills">', back_bar_pos)
        close_after_pills = html.index("</div>\n          </div>", pills_pos) + len("</div>\n          </div>")
        html = html[:close_after_pills] + "\n          ${renderAgentTwinDivisionBanner(ag)}" + html[close_after_pills:]

    # 5. Replace `<div id="enterpriseTwinModal"...` block right before `GLOBAL EXECUTIVE ATTRIBUTION FOOTER`
    modal_start = html.index('<div id="enterpriseTwinModal"')
    # Include preceding comment block if present
    comment_before = html.rfind("<!-- ===", max(0, modal_start - 260), modal_start)
    slice_modal_start = comment_before if comment_before != -1 else modal_start
    footer_anchor = html.index("GLOBAL EXECUTIVE ATTRIBUTION FOOTER", modal_start)
    footer_comment_start = html.rfind("<!-- ===", modal_start, footer_anchor)
    html = html[:slice_modal_start] + build_v2_modal_html() + "\n\n  " + html[footer_comment_start:]

    # 6. Replace bottom Enterprise Twin JS block right before final `</script>`
    embedded_js = build_embedded_twins_js()
    v2_js = build_v2_engine_js(embedded_js)
    if is_periodic:
        v2_js = v2_js.replace(
            "handleUrlHash();",
            "handleUrlHash();\n      if (!window.location.hash) openPeriodicTablePage('all', null, false);",
        )
    elif is_mindmap:
        v2_js = v2_js.replace(
            "handleUrlHash();",
            "handleUrlHash();\n      if (!window.location.hash) openMindMapPage('all', null, false);",
        )

    last_script_close = html.rindex("</script>")
    # Find the comment header immediately above the bottom Enterprise Twin JS block
    if "ENTERPRISE TWIN STUDIO V2 — IMMACULATE" in html:
        js_block_marker = html.rindex("ENTERPRISE TWIN STUDIO V2 — IMMACULATE", 0, last_script_close)
    else:
        js_block_marker = html.rindex("ENTERPRISE TWIN CLIENT-SIDE SWITCHER", 0, last_script_close)
    js_comment_start = html.rfind("/*", 0, js_block_marker)

    html = html[:js_comment_start] + v2_js.lstrip() + "\n  " + html[last_script_close:]

    assert len(html) >= int(orig_len * 0.95), f"Safety assertion failed on {path.name}: {len(html)} < {orig_len}"
    path.write_text(html, encoding="utf-8")
    print(f"[UPGRADED] {path.name} ({path.stat().st_size // 1024} KB)")


def main() -> None:
    upgrade_single_html_file(ROOT / "index.html", is_periodic=False, is_mindmap=False)
    if (ROOT / "periodic_table.html").exists():
        upgrade_single_html_file(ROOT / "periodic_table.html", is_periodic=True, is_mindmap=False)
    if (ROOT / "mind_map.html").exists():
        upgrade_single_html_file(ROOT / "mind_map.html", is_periodic=False, is_mindmap=True)


if __name__ == "__main__":
    main()

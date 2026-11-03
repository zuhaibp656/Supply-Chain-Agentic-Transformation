#!/usr/bin/env python3
"""Upgrades `index.html`, `periodic_table.html`, and `mind_map.html` with the Immaculate v2.1 Enterprise Twin Overlay & Visual Polish Engine.

Guarantees zero breakage across all 10 portal views while supporting:
  1. Larger, prominently placed & contrast-plated real corporate logos (`.sc-twin-logo-plate`):
     - `40px` Navbar lockup
     - `70px` (`size-hero`) Hero Showcase Co-Brand Lockup above `.hero-title`
     - `58px` (`size-xl`) Official Company Logo inside the CSCO Root Box (`.cfo-box`) & Active Context Bar
     - `50px` (`size-lg`) Logo Plate in Saved Portals & Agent Operational Lens
  2. Dynamic renaming of 6 Pillars, 20 Sub-Pillars, 4 Cross-Pillar Process Journeys (`VALUE_CHAINS`),
     and optional company-specific Agent Display Names (`custom_agent_name`) while keeping `ag.canonicalName`,
     `ag.id`, Playbook deep-links, and all 60 core ADK Demo Engines 100% intact.
  3. Grounded corporate job titles & Red/Green daily toil scenarios across all 60 Personas (`#persona/<id>`).
  4. Intelligent hiding of division-irrelevant agents (`hidden_agent_ids`) with clean count updates,
     Value Chain stage remapping guards, and a 1-click `'Show All 60'` toggle.
  5. Stronger, high-contrast architectural box outlines (`1.5px solid`), nested container luminance separation,
     and sleek collapsed-by-default Deep-Dive Tab Bar styling (`💰 Cost & ROI ▾`, `⚡ 5 Execution Steps ▾`,
     `📚 Benchmark Proof ▾`, `🛡️ Governance & Tech Specs ▾`) across Dark & Light themes.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TWINS_V2_DIR = ROOT / "data" / "twins" / "v2"

CSS_MARKER_START = "/* === ENTERPRISE TWIN STUDIO V2 OVERLAY STYLES START === */"
CSS_MARKER_END = "/* === ENTERPRISE TWIN STUDIO V2 OVERLAY STYLES END === */"

TWIN_CSS = f"""
    {CSS_MARKER_START}
    /* 1. Stronger Architectural Box Outlines & Visual Segregation (Dark + Light) */
    :root {{
      --border-subtle: rgba(148, 163, 184, 0.24);
      --border-strong: rgba(148, 163, 184, 0.44);
    }}
    html[data-theme="light"] {{
      --border-subtle: #cbd5e1;
      --border-strong: #94a3b8;
    }}
    #orgChartSection {{
      scroll-margin-top: 138px;
    }}

    .cfo-box,
    .dept-node,
    .dept-showcase-box,
    .subpillar-box-card,
    .human-persona-card,
    .ai-agent-chip-card,
    .persona-header-card,
    .time-shift-banner,
    .journey-accordion-item,
    .persona-step-agent-box,
    .agent-hero-banner,
    .simple-arch-card,
    .video-stage-box,
    .sc-proof-strip,
    .sc-spec-section-card,
    .pt-pillar-card,
    .pt-side-card,
    .pt-legend-card,
    .mm-col-panel,
    .mm-agent-neural-card {{
      border: 1.5px solid var(--border-strong) !important;
      box-shadow: 0 12px 32px rgba(2, 6, 23, 0.34), inset 0 1px 0 rgba(255, 255, 255, 0.08);
    }}
    html[data-theme="light"] .cfo-box,
    html[data-theme="light"] .dept-node,
    html[data-theme="light"] .dept-showcase-box,
    html[data-theme="light"] .subpillar-box-card,
    html[data-theme="light"] .human-persona-card,
    html[data-theme="light"] .ai-agent-chip-card,
    html[data-theme="light"] .persona-header-card,
    html[data-theme="light"] .time-shift-banner,
    html[data-theme="light"] .journey-accordion-item,
    html[data-theme="light"] .persona-step-agent-box,
    html[data-theme="light"] .agent-hero-banner,
    html[data-theme="light"] .simple-arch-card,
    html[data-theme="light"] .video-stage-box,
    html[data-theme="light"] .sc-proof-strip,
    html[data-theme="light"] .sc-spec-section-card,
    html[data-theme="light"] .pt-pillar-card,
    html[data-theme="light"] .pt-side-card,
    html[data-theme="light"] .pt-legend-card,
    html[data-theme="light"] .mm-col-panel,
    html[data-theme="light"] .mm-agent-neural-card {{
      border: 1.5px solid #cbd5e1 !important;
      box-shadow: 0 10px 26px rgba(15, 23, 42, 0.07), inset 0 1px 0 #ffffff;
    }}

    /* Preserve unmistakable Human Role left accent bar */
    .human-persona-card {{
      border-left: 5px solid var(--dept-accent, var(--sc-cyan)) !important;
    }}

    /* Nested Containers & Drawers: Distinct Surface Contrast + Crisp Outlines */
    .dept-anim-stage,
    .subpillar-personas-drawer,
    .ag-flow-canvas-wrap,
    .sc-proof-box,
    .sc-spec-sub-drawer,
    .sc-spec-entity,
    .pt-subpillar-group,
    .pt-tile,
    .mm-node-btn,
    .mm-expanded-persona-box {{
      border: 1.5px solid rgba(148, 163, 184, 0.30) !important;
    }}
    html[data-theme="light"] .dept-anim-stage,
    html[data-theme="light"] .subpillar-personas-drawer,
    html[data-theme="light"] .ag-flow-canvas-wrap,
    html[data-theme="light"] .sc-proof-box,
    html[data-theme="light"] .sc-spec-sub-drawer,
    html[data-theme="light"] .sc-spec-entity,
    html[data-theme="light"] .pt-subpillar-group,
    html[data-theme="light"] .pt-tile,
    html[data-theme="light"] .mm-node-btn,
    html[data-theme="light"] .mm-expanded-persona-box {{
      border: 1.5px solid #cbd5e1 !important;
    }}

    .manual-toil-box {{
      border: 1.5px solid rgba(244, 63, 94, 0.45) !important;
    }}
    .gemini-improve-box {{
      border: 1.5px solid rgba(16, 185, 129, 0.45) !important;
    }}
    .ai-agent-dock-box {{
      border: 1.5px dashed rgba(99, 102, 241, 0.52) !important;
    }}

    /* Crisp 3D Flip Card Faces with Top Accent Bar Segregation */
    .sc-flip-front,
    .sc-flip-back {{
      border: 1.5px solid rgba(148, 163, 184, 0.34) !important;
      border-top: 3px solid var(--flip-accent, var(--sc-cyan)) !important;
      box-shadow: 0 10px 24px rgba(2, 6, 23, 0.28), inset 0 1px 0 rgba(255, 255, 255, 0.06);
    }}
    html[data-theme="light"] .sc-flip-front,
    html[data-theme="light"] .sc-flip-back {{
      border: 1.5px solid #cbd5e1 !important;
      border-top: 3px solid var(--flip-accent, var(--sc-cyan)) !important;
      box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
    }}
    .sc-flip-card:hover .sc-flip-front,
    .sc-flip-card:hover .sc-flip-back {{
      border-color: var(--flip-accent, var(--sc-cyan)) !important;
    }}

    .sc-agent-card-brief {{
      font-size: 14px;
      line-height: 1.52;
      color: var(--text-secondary);
      font-weight: 500;
      margin-top: 4px;
    }}
    .sc-twin-core-engine-chip {{
      display: inline-flex;
      align-items: center;
      padding: 2px 9px;
      border-radius: 999px;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      color: var(--sc-cyan);
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.34);
    }}

    /* 2. Sleek Collapsed-by-Default Deep-Dive Tab Bar on #pageAgent */
    .agent-deepdive-bar {{
      margin-top: 20px;
      margin-bottom: 10px;
      padding: 13px 18px;
      border-radius: 16px;
      background: var(--bg-card);
      border: 1.5px solid var(--border-strong);
      border-left: 5px solid var(--deep-accent, var(--sc-cyan));
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
      box-shadow: 0 10px 26px rgba(2, 6, 23, 0.24);
    }}
    html[data-theme="light"] .agent-deepdive-bar {{
      background: #ffffff;
      border-color: #cbd5e1;
      border-left: 5px solid var(--deep-accent, var(--sc-cyan));
      box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
    }}
    .agent-deepdive-label {{
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      color: var(--text-muted);
      margin-right: 4px;
    }}
    .agent-deepdive-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 14px;
      border-radius: 10px;
      font-family: var(--font-sans);
      font-size: 13px;
      font-weight: 700;
      color: var(--text-primary);
      background: var(--bg-elevated);
      border: 1.5px solid var(--border-strong);
      cursor: pointer;
      transition: all 0.18s ease;
    }}
    .agent-deepdive-pill:hover {{
      border-color: var(--deep-accent, var(--sc-cyan));
      transform: translateY(-1px);
    }}
    .agent-deepdive-pill.active {{
      background: var(--deep-accent, var(--sc-cyan));
      border-color: var(--deep-accent, var(--sc-cyan));
      color: #ffffff;
    }}
    .agent-deepdive-pill.blueprint-jump {{
      background: rgba(56, 189, 248, 0.12);
      border-color: rgba(56, 189, 248, 0.42);
      color: #38bdf8;
    }}
    html[data-theme="light"] .agent-deepdive-pill.blueprint-jump {{
      color: #0284c7;
      background: rgba(2, 132, 199, 0.08);
    }}
    .agent-deepdive-drawer {{
      animation: fadeIn 0.24s ease;
    }}

    /* 3. Upgraded, Larger & Prominently Framed Corporate Logo Plates */
    .sc-twin-nav-lockup {{
      display: inline-flex;
      align-items: center;
      gap: 11px;
      flex-wrap: nowrap;
      max-width: 490px;
    }}
    .sc-twin-logo-plate {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      height: 40px;
      min-width: 44px;
      max-width: 142px;
      padding: 5px 11px;
      border-radius: 10px;
      flex-shrink: 0;
      box-sizing: border-box;
      transition: transform 0.2s var(--ease-spring);
    }}
    .sc-twin-logo-plate.plate-light {{
      background: #ffffff;
      border: 1.5px solid rgba(148, 163, 184, 0.48);
      box-shadow: 0 4px 12px rgba(2, 6, 23, 0.24);
    }}
    .sc-twin-logo-plate.plate-dark {{
      background: #0f172a;
      border: 1.5px solid rgba(148, 163, 184, 0.42);
      box-shadow: 0 4px 12px rgba(2, 6, 23, 0.32);
    }}
    .sc-twin-logo-plate.plate-self {{
      background: transparent;
      padding: 2px;
      border-radius: 9px;
      overflow: hidden;
    }}
    .sc-twin-logo-plate img {{
      max-height: 29px;
      max-width: 118px;
      width: auto;
      height: auto;
      object-fit: contain;
      display: block;
    }}
    .sc-twin-logo-plate.size-lg {{
      height: 50px;
      min-width: 56px;
      max-width: 172px;
      padding: 6px 13px;
      border-radius: 12px;
    }}
    .sc-twin-logo-plate.size-lg img {{
      max-height: 36px;
      max-width: 144px;
    }}
    .sc-twin-logo-plate.size-xl {{
      height: 58px;
      min-width: 66px;
      max-width: 196px;
      padding: 7px 15px;
      border-radius: 14px;
    }}
    .sc-twin-logo-plate.size-xl img {{
      max-height: 44px;
      max-width: 164px;
    }}
    .sc-twin-logo-plate.size-hero {{
      height: 70px;
      min-width: 82px;
      max-width: 234px;
      padding: 9px 18px;
      border-radius: 16px;
    }}
    .sc-twin-logo-plate.size-hero img {{
      max-height: 52px;
      max-width: 196px;
    }}

    .cfo-sc-emblem.has-twin-logo {{
      width: auto !important;
      height: auto !important;
      min-width: 0 !important;
      background: transparent !important;
      border: none !important;
      padding: 0 !important;
      overflow: visible !important;
      box-shadow: none !important;
    }}

    .sc-twin-nav-co {{
      font-family: var(--font-display);
      font-size: 14px;
      font-weight: 800;
      color: var(--text-primary);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 195px;
    }}
    .sc-twin-nav-div {{
      font-size: 11.5px;
      font-weight: 700;
      padding: 3px 9px;
      border-radius: 999px;
      background: rgba(66, 133, 244, 0.15);
      color: var(--sc-cyan);
      border: 1px solid rgba(66, 133, 244, 0.38);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 185px;
    }}
    .sc-twin-hero-cobrand {{
      display: inline-flex;
      align-items: center;
      gap: 16px;
      padding: 12px 24px 12px 14px;
      margin-bottom: 24px;
      border-radius: 22px;
      background: rgba(15, 23, 42, 0.84);
      border: 1.5px solid var(--border-strong);
      backdrop-filter: blur(16px);
      box-shadow: 0 18px 44px rgba(0, 0, 0, 0.36), inset 0 1px 0 rgba(255, 255, 255, 0.10);
      text-align: left;
    }}
    html[data-theme="light"] .sc-twin-hero-cobrand {{
      background: rgba(255, 255, 255, 0.94);
      border-color: #cbd5e1;
      box-shadow: 0 14px 34px rgba(15, 23, 42, 0.09);
    }}
    .sc-twin-context-bar {{
      margin: 0 auto 26px auto;
      padding: 18px 22px;
      border-radius: 18px;
      background: var(--bg-card);
      border: 1.5px solid var(--border-strong);
      border-left: 5px solid var(--sc-cyan);
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.24);
      display: flex;
      align-items: center;
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
      padding: 8px 14px;
      border-radius: 10px;
      font-family: var(--font-sans);
      font-size: 12.5px;
      font-weight: 700;
      cursor: pointer;
      background: var(--bg-surface);
      color: var(--text-primary);
      border: 1.5px solid var(--border-strong);
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
      border: 1.5px solid var(--border-strong);
      border-left: 4px solid var(--sc-cyan);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      flex-wrap: wrap;
    }}
    .nav-pill-btn.twin-studio-pill {{
      padding: 6px 10px;
      min-width: 34px;
      font-size: 13px;
      opacity: 0.72;
    }}
    .nav-pill-btn.twin-studio-pill:hover {{
      opacity: 1;
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
       ENTERPRISE TWIN STUDIO MODAL V2.1 (MINIMAL, CLEAN + SAVED TAB)
       ========================================================================= -->
  <div id="enterpriseTwinModal" class="modal-overlay" style="display:none; position:fixed; inset:0; z-index:99999; background:rgba(2,6,18,0.82); backdrop-filter:blur(16px); align-items:center; justify-content:center; padding:20px;">
    <div class="modal-card" style="background:var(--bg-card); border:1.5px solid var(--border-strong); border-radius:24px; max-width:860px; width:100%; max-height:90vh; overflow-y:auto; padding:28px 30px; box-shadow:0 30px 90px rgba(0,0,0,0.65); position:relative; color:var(--text-primary);">
      <div style="display:flex; justify-content:space-between; align-items:center; gap:12px; margin-bottom:18px;">
        <div>
          <div style="font-size:11px; font-weight:800; letter-spacing:0.08em; text-transform:uppercase; color:var(--g-blue); margin-bottom:3px;">
            Enterprise Portal Studio
          </div>
          <h2 style="font-family:var(--font-display); font-size:24px; font-weight:800; color:var(--text-primary); margin:0;">
            Welcome to Supply Chain
          </h2>
        </div>
        <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
          <button type="button" id="modalToggleShowAllBtn" style="display:none;" class="sc-twin-action-btn" onclick="toggleTwinShowAllAgents()">
            Show All 60 Agents
          </button>
          <a id="openFullWelcomeStudioLink" href="/welcome" style="display:none; text-decoration:none;" class="sc-twin-action-btn">
            ↗ Journey View
          </a>
          <button type="button" class="back-btn" style="padding:6px 14px; font-size:13px;" onclick="closeEnterpriseTwinModal()">
            ✕ Close
          </button>
        </div>
      </div>

      <!-- Segmented Tabs: Create Portal vs Saved Portals -->
      <div style="display:inline-flex; gap:6px; padding:5px; border-radius:999px; background:var(--bg-surface); border:1.5px solid var(--border-strong); margin-bottom:18px;">
        <button type="button" id="modalTabCreateBtn" onclick="switchTwinModalTab('create')" style="padding:7px 16px; border-radius:999px; border:none; font-size:13px; font-weight:700; cursor:pointer; background:var(--g-blue); color:#fff;">
          ✦ Enter Details
        </button>
        <button type="button" id="modalTabSavedBtn" onclick="switchTwinModalTab('saved')" style="padding:7px 16px; border-radius:999px; border:none; font-size:13px; font-weight:700; cursor:pointer; background:transparent; color:var(--text-secondary);">
          🗂️ Saved Companies
        </button>
      </div>

      <!-- Create Pane -->
      <div id="modalCreatePane" style="background:var(--bg-surface); border:1.5px solid var(--border-strong); border-radius:18px; padding:20px 22px;">
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap:14px; margin-bottom:14px;">
          <div>
            <label style="display:block; font-size:11.5px; font-weight:700; color:var(--text-secondary); margin-bottom:6px; text-transform:uppercase; letter-spacing:0.05em;">
              Company Name <span style="color:var(--g-red);">*</span>
            </label>
            <input type="text" id="twinCompanyInput" class="twin-input-field" placeholder="e.g. ITC Limited" value="" style="width:100%; padding:10px 13px; border-radius:10px; background:var(--bg-card); color:var(--text-primary); border:1.5px solid var(--border-strong); font-size:14px;" />
          </div>
          <div>
            <label style="display:block; font-size:11.5px; font-weight:700; color:var(--text-secondary); margin-bottom:6px; text-transform:uppercase; letter-spacing:0.05em;">
              Division / Business Unit
            </label>
            <input type="text" id="twinDivisionInput" class="twin-input-field" placeholder="e.g. Cigarettes &amp; Leaf Tobacco, Foods..." value="" style="width:100%; padding:10px 13px; border-radius:10px; background:var(--bg-card); color:var(--text-primary); border:1.5px solid var(--border-strong); font-size:14px;" />
          </div>
          <div>
            <label style="display:block; font-size:11.5px; font-weight:700; color:var(--text-secondary); margin-bottom:6px; text-transform:uppercase; letter-spacing:0.05em;">
              Geography
            </label>
            <input type="text" id="twinGeoInput" class="twin-input-field" placeholder="e.g. India, Global" value="India" style="width:100%; padding:10px 13px; border-radius:10px; background:var(--bg-card); color:var(--text-primary); border:1.5px solid var(--border-strong); font-size:14px;" />
          </div>
        </div>

        <div style="display:grid; grid-template-columns: 2fr 1fr; gap:12px; margin-bottom:16px;">
          <input type="text" id="twinFocusInput" class="twin-input-field" placeholder="Optional context (e.g. Wholesale Dealers, SAP S/4HANA)" style="width:100%; padding:10px 13px; border-radius:10px; background:var(--bg-card); color:var(--text-primary); border:1.5px solid var(--border-strong); font-size:13.5px;" />
          <input type="text" id="twinLogoUrlInput" class="twin-input-field" placeholder="Optional Logo URL" style="width:100%; padding:10px 13px; border-radius:10px; background:var(--bg-card); color:var(--text-primary); border:1.5px solid var(--border-strong); font-size:13.5px;" />
        </div>

        <div style="display:flex; flex-wrap:wrap; gap:12px; align-items:center; justify-content:space-between;">
          <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <button type="button" onclick="executeTwinGeneration()" style="display:inline-flex; align-items:center; gap:8px; padding:11px 22px; border-radius:11px; background:var(--g-blue); color:#ffffff; font-family:var(--font-display); font-size:14px; font-weight:700; border:none; cursor:pointer;">
              <span>✦ Build Tailored Portal &rarr;</span>
            </button>
            <button type="button" class="sc-twin-action-btn" onclick="switchClientTwin('reset')">
              ↺ Base Portal (60 Agents)
            </button>
          </div>
          <label style="display:inline-flex; align-items:center; gap:6px; font-size:12px; color:var(--text-secondary); cursor:pointer;">
            <input type="checkbox" id="twinForceRefreshCheckbox" checked />
            <span>Run live AI research</span>
          </label>
        </div>

        <!-- Streaming Synthesis HUD -->
        <div id="twinProgressHud" style="display:none; margin-top:16px; padding:16px; border-radius:12px; background:var(--bg-card); border:1.5px solid var(--border-strong);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span id="hudStatusText" style="font-family:var(--font-mono); font-size:12.5px; color:var(--g-blue); font-weight:700;">
              Synthesizing portal...
            </span>
            <span id="hudPercentText" style="font-family:var(--font-mono); font-size:12px; color:var(--g-green); font-weight:700;">0%</span>
          </div>
          <div style="height:6px; background:rgba(148,163,184,0.2); border-radius:10px; overflow:hidden; margin-bottom:10px;">
            <div id="hudProgressBar" style="width:0%; height:100%; background:linear-gradient(90deg, var(--g-blue), var(--g-green)); transition:width 0.3s ease;"></div>
          </div>
          <div id="hudStepLog" style="font-family:var(--font-mono); font-size:11.5px; color:var(--text-secondary); line-height:1.65;"></div>
        </div>
      </div>

      <!-- Saved Companies Pane -->
      <div id="modalSavedPane" style="display:none;">
        <div id="modalSavedTwinsGrid" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(255px, 1fr)); gap:12px;"></div>
      </div>
    </div>
  </div>"""


def build_v2_engine_js(embedded_twins_js: str) -> str:
    return f"""    /* =========================================================================
       ENTERPRISE TWIN STUDIO V2.1 — IMMACULATE ZERO-BREAKAGE OVERLAY ENGINE
       ========================================================================= */
    {embedded_twins_js}

    let BASELINE_DEPARTMENTS = null;
    let BASELINE_PERSONAS = null;
    let BASELINE_AGENTS = null;
    let BASELINE_VALUE_CHAINS = null;
    let ORIG_CFO_EMBLEM_HTML = null;
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
      if (ORIG_CFO_EMBLEM_HTML === null) {{
        const emb = document.querySelector('.cfo-sc-emblem');
        if (emb) ORIG_CFO_EMBLEM_HTML = emb.innerHTML;
      }}
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
        return `<span class="sc-twin-logo-plate plate-dark ${{sizeClass}}" style="font-family:var(--font-display); font-weight:800; font-size:14px; color:#fff;">${{mono}}</span>`;
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
          <div style="display:flex; align-items:center; gap:14px; flex:1; min-width:240px;">
            ${{renderAdaptiveTwinLogoBadge(brand, 'size-lg')}}
            <div style="font-size:13.5px; line-height:1.5; color:var(--text-primary);">
              <strong style="color:var(--sc-cyan);">${{escTwinHtml(disp)}} Operational Context:</strong>
              <span> ${{escTwinHtml(ctx)}}</span>
            </div>
          </div>
        </div>
      `;
    }}

    function updateNavbarAndTabCounts() {{
      const pCount = Object.keys(PERSONAS).length;
      const aCount = Object.keys(AGENTS).length;
      const pillarCount = Object.keys(DEPARTMENTS).length;

      const rowEl = document.getElementById('deptRowContainer');
      if (rowEl) rowEl.setAttribute('data-pillar-count', String(pillarCount));

      const allTabTag = document.querySelector('#verticalTabsNavBar button[data-vtab="all"] .v-tab-tag');
      let totalSp = 0;
      Object.values(DEPARTMENTS).forEach(d => {{
        const spLen = (d.subPillars || []).length;
        totalSp += spLen;
        const tabTag = document.querySelector(`#verticalTabsNavBar button[data-vtab="${{d.id}}"] .v-tab-tag`);
        if (tabTag) tabTag.textContent = `${{spLen}} Sub-Pillars · ${{d.personaIds.length}} Personas`;
      }});
      if (allTabTag) allTabTag.textContent = `${{totalSp}} Sub-Pillars · ${{pCount}} Personas`;
      return {{ pCount, aCount, totalSp, pillarCount }};
    }}

    function mountTwinContextBar() {{
      // Customer-facing front page: NEVER render `#twinActiveContextBar` ("Switch Company / Tailored Supply Chain Twin")
      const existingBar = document.getElementById('twinActiveContextBar');
      if (existingBar) existingBar.remove();

      const modalToggleBtn = document.getElementById('modalToggleShowAllBtn');
      if (!CURRENT_TWIN) {{
        const heroBanner = document.getElementById('twinHeroCoBrandBanner');
        if (heroBanner) heroBanner.remove();
        const heroLockup = document.querySelector('.hero-logo-lockup');
        if (heroLockup) heroLockup.style.display = '';
        if (modalToggleBtn) modalToggleBtn.style.display = 'none';
        return;
      }}

      const hiddenCount = (CURRENT_TWIN.hidden_agent_ids || []).length;
      if (modalToggleBtn) {{
        if (hiddenCount > 0) {{
          modalToggleBtn.style.display = 'inline-flex';
          modalToggleBtn.textContent = TWIN_SHOW_ALL_60
            ? `🎯 Focused View (${{60 - hiddenCount}}/60)`
            : `👁️ Show All 60 Agents`;
        }} else {{
          modalToggleBtn.style.display = 'none';
        }}
      }}
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

      // 1A. Reconstruct Dynamic Organization-Specific Operating Pillars (`4` to `8` Pillars) if provided
      if (Array.isArray(twinData.custom_pillars) && twinData.custom_pillars.length >= 4) {{
        const canonicalSpMap = {{}};
        Object.values(BASELINE_DEPARTMENTS).forEach(bd => {{
          (bd.subPillars || []).forEach(sp => {{
            canonicalSpMap[sp.id] = JSON.parse(JSON.stringify(sp));
          }});
        }});

        for (const k of Object.keys(DEPARTMENTS)) delete DEPARTMENTS[k];

        twinData.custom_pillars.forEach((cp, idx) => {{
          const pid = cp.pillar_id || (`pillar_${{idx + 1}}`);
          const pColor = cp.color || '#2563eb';
          const vNum = String(idx + 1).padStart(2, '0');
          const builtSubPillars = (cp.sub_pillar_ids || [])
            .map(spid => canonicalSpMap[spid] ? JSON.parse(JSON.stringify(canonicalSpMap[spid])) : null)
            .filter(Boolean);

          const builtPersonaIds = [];
          const builtAgentIds = [];

          builtSubPillars.forEach(sp => {{
            sp.color = pColor;
            (sp.items || []).forEach(it => {{
              if (it.personaId && PERSONAS[it.personaId]) {{
                PERSONAS[it.personaId].deptId = pid;
                PERSONAS[it.personaId].subPillarColor = pColor;
                if (!builtPersonaIds.includes(it.personaId)) builtPersonaIds.push(it.personaId);
              }}
              if (it.agentId && AGENTS[it.agentId]) {{
                AGENTS[it.agentId].deptId = pid;
                if (!builtAgentIds.includes(it.agentId)) builtAgentIds.push(it.agentId);
              }}
            }});
          }});

          DEPARTMENTS[pid] = {{
            id: pid,
            vNum,
            scorBadge: cp.scor_badge || cp.badge || `${{vNum}} · PILLAR`,
            name: cp.name || `Pillar ${{idx + 1}}`,
            tagline: cp.tagline || `${{dispLabel}} · ${{cp.name || 'Operations'}}`,
            subtitle: cp.subtitle || '',
            color: pColor,
            watermarkType: cp.watermark_type || 'demand_wave',
            subPillars: builtSubPillars,
            personaIds: builtPersonaIds,
            agentIds: builtAgentIds
          }};
        }});

        const firstPid = Object.keys(DEPARTMENTS)[0];
        Object.values(AGENTS).forEach(ag => {{
          if (!DEPARTMENTS[ag.deptId] && firstPid) ag.deptId = firstPid;
        }});
        Object.values(PERSONAS).forEach(p => {{
          if (!DEPARTMENTS[p.deptId] && firstPid) p.deptId = firstPid;
        }});
      }}

      // 1B. Apply Pillar & Sub-Pillar Process Renaming
      const pOvMap = twinData.pillar_overrides || {{}};
      const spOvMap = twinData.sub_pillar_overrides || {{}};
      Object.values(DEPARTMENTS).forEach(dept => {{
        const po = pOvMap[dept.id];
        if (po) {{
          if (po.custom_name && (!Array.isArray(twinData.custom_pillars) || twinData.custom_pillars.length < 4)) {{
            dept.name = po.custom_name;
          }}
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

      // 2B. Apply Optional Company-Tailored Agent Names (`custom_agent_name`) while keeping `canonicalName`
      const agRelMap = twinData.agent_relevance || {{}};
      Object.keys(AGENTS).forEach(aid => {{
        const baseAg = BASELINE_AGENTS[aid];
        const origClean = typeof cleanAgentName === 'function' ? cleanAgentName(baseAg ? baseAg.name : AGENTS[aid].name) : AGENTS[aid].name;
        AGENTS[aid].canonicalName = origClean;
        const rel = agRelMap[aid];
        if (rel) {{
          if (rel.division_context) AGENTS[aid].twinDivisionContext = rel.division_context;
          if (rel.custom_agent_name && String(rel.custom_agent_name).trim()) {{
            AGENTS[aid].name = String(rel.custom_agent_name).trim();
          }}
        }}
      }});

      // Sync renamed Sub-Pillars, Persona titles, & tailored Agent names onto Sub-Pillar items
      Object.values(DEPARTMENTS).forEach(dept => {{
        (dept.subPillars || []).forEach(sp => {{
          (sp.items || []).forEach(it => {{
            if (PERSONAS[it.personaId]) {{
              PERSONAS[it.personaId].subPillarName = sp.name;
              it.personaName = PERSONAS[it.personaId].name;
            }}
            if (AGENTS[it.agentId]) {{
              AGENTS[it.agentId].subPillarName = sp.name;
              it.agentName = AGENTS[it.agentId].name;
              if (PERSONAS[it.personaId]) {{
                AGENTS[it.agentId].primaryPersonaName = PERSONAS[it.personaId].name;
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

      // Reset selectedDeptId if previous pillar no longer exists in DEPARTMENTS
      if (typeof selectedDeptId !== 'undefined' && selectedDeptId && !DEPARTMENTS[selectedDeptId]) {{
        selectedDeptId = null;
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

      // 5. Update Brand Accent, 40px Navbar Logo Lockup, 70px Hero Showcase Card, & 58px CSCO Box Logo
      document.documentElement.style.setProperty('--sc-cyan', accent);
      const counts = updateNavbarAndTabCounts();

      const orgSecTitle = document.querySelector('#orgChartSection .section-title');
      if (orgSecTitle) {{
        orgSecTitle.textContent = `${{cName}} Supply Chain — ${{counts.pillarCount}} Operating Pillars`;
      }}

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
      const heroLockup = document.querySelector('.hero-logo-lockup');
      if (heroLockup) heroLockup.style.display = 'none';
      if (heroContent && heroTitleEl) {{
        let heroCobrand = document.getElementById('twinHeroCoBrandBanner');
        if (!heroCobrand) {{
          heroCobrand = document.createElement('div');
          heroCobrand.id = 'twinHeroCoBrandBanner';
          heroCobrand.className = 'sc-twin-hero-cobrand';
          heroContent.insertBefore(heroCobrand, heroTitleEl);
        }}
        heroCobrand.innerHTML = `
          ${{renderAdaptiveTwinLogoBadge(brand, 'size-hero')}}
          <div style="display:flex; flex-direction:column; gap:3px;">
            <div style="font-family:var(--font-display); font-size:18px; font-weight:800; color:var(--text-primary); line-height:1.2;">
              ${{escTwinHtml(cName)}}
            </div>
            ${{divName ? `<div style="font-size:13px; font-weight:700; color:var(--sc-cyan);">${{escTwinHtml(divName)}}</div>` : ''}}
            <div style="font-size:11px; font-weight:700; color:var(--g-green); letter-spacing:0.04em; text-transform:uppercase;">
              ● Powered by Gemini Enterprise
            </div>
          </div>
        `;
        heroTitleEl.innerHTML = `Agentic Transformation for <span class="gradient-word">${{escTwinHtml(cName)}} Supply Chain</span>`;
      }}

      const cfoEmblemEl = document.querySelector('.cfo-sc-emblem');
      if (cfoEmblemEl) {{
        cfoEmblemEl.classList.add('has-twin-logo');
        cfoEmblemEl.innerHTML = renderAdaptiveTwinLogoBadge(brand, 'size-xl');
      }}
      const cfoTitleEl = document.querySelector('.cfo-box-title');
      const cfoSubEl = document.querySelector('.cfo-box-sub');
      if (cfoTitleEl) cfoTitleEl.textContent = brand.executive_title || `Chief Supply Chain Officer, ${{cName}}`;
      if (cfoSubEl) {{
        cfoSubEl.textContent = `${{counts.pillarCount}} Core Operating Pillars · ${{counts.totalSp}} Sub-Pillars · ${{counts.pCount}} Corporate Roles · ${{counts.aCount}} AI Agents`;
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
        openMindMapPage('mindmap', null, null, false);
      }} else if (activeId === 'pageCost' && typeof openCostTabPage === 'function') {{
        openCostTabPage('all', null, false);
      }} else if (activeId === 'pageDirectory' && typeof openPersonasDirectoryPage === 'function') {{
        openPersonasDirectoryPage('all', '', false, currentDirMode || 'personas');
      }} else if (activeId === 'pageEvidence' && typeof openEvidenceHubPage === 'function') {{
        openEvidenceHubPage('all', false);
      }} else if (activeId === 'pageValueChain' && typeof openProcessesHubPage === 'function') {{
        openProcessesHubPage(false);
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
        if (typeof selectedDeptId !== 'undefined') selectedDeptId = null;
        try {{
          localStorage.removeItem('ACTIVE_ENTERPRISE_TWIN_V2');
          localStorage.removeItem('ACTIVE_ENTERPRISE_TWIN');
        }} catch (e) {{}}

        restoreCanonicalBaselines();
        document.documentElement.style.setProperty('--sc-cyan', '#4285f4');
        updateNavbarAndTabCounts();

        const orgSecTitle = document.querySelector('#orgChartSection .section-title');
        if (orgSecTitle) orgSecTitle.textContent = 'Enterprise Supply Chain — 6 Core Operating Pillars';

        const cscoBadgeEl = document.querySelector('.nav-csco-badge');
        if (cscoBadgeEl) cscoBadgeEl.textContent = 'Office of the CSCO · Supply Chain';

        const heroLockup = document.querySelector('.hero-logo-lockup');
        if (heroLockup) heroLockup.style.display = '';
        const heroTitleEl = document.querySelector('.hero-title');
        if (heroTitleEl) {{
          heroTitleEl.innerHTML = 'Agentic Transformation for <span class="gradient-word">Supply Chain &amp; Demand</span>';
        }}

        const cfoEmblemEl = document.querySelector('.cfo-sc-emblem');
        if (cfoEmblemEl && ORIG_CFO_EMBLEM_HTML !== null) {{
          cfoEmblemEl.classList.remove('has-twin-logo');
          cfoEmblemEl.innerHTML = ORIG_CFO_EMBLEM_HTML;
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
          const ov = d && (d.twin || d.overlay);
          if (ov) {{
            closeEnterpriseTwinModal();
            applyBrowserTwin(ov);
          }}
        }})
        .catch(() => {{}});
    }}

    function switchTwinModalTab(mode) {{
      const createPane = document.getElementById('modalCreatePane');
      const savedPane = document.getElementById('modalSavedPane');
      const createBtn = document.getElementById('modalTabCreateBtn');
      const savedBtn = document.getElementById('modalTabSavedBtn');
      const isCreate = mode !== 'saved';
      if (createPane) createPane.style.display = isCreate ? 'block' : 'none';
      if (savedPane) savedPane.style.display = isCreate ? 'none' : 'block';
      if (createBtn) {{
        createBtn.style.background = isCreate ? 'var(--g-blue)' : 'transparent';
        createBtn.style.color = isCreate ? '#fff' : 'var(--text-secondary)';
      }}
      if (savedBtn) {{
        savedBtn.style.background = !isCreate ? 'var(--g-blue)' : 'transparent';
        savedBtn.style.color = !isCreate ? '#fff' : 'var(--text-secondary)';
      }}
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
        switchTwinModalTab('create');
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
          const pCnt = it.active_pillars_count || 6;
          return `
            <button type="button" onclick="switchClientTwin('${{escTwinHtml(it.twin_slug)}}')" style="text-align:left; background:var(--bg-surface); border:1.5px solid var(--border-strong); border-radius:16px; padding:14px 16px; cursor:pointer; display:flex; align-items:center; gap:14px; color:var(--text-primary);">
              ${{renderAdaptiveTwinLogoBadge(fakeBrand, 'size-lg')}}
              <div style="min-width:0; flex:1;">
                <div style="font-size:14.5px; font-weight:800; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${{escTwinHtml(it.company_name)}}</div>
                <div style="font-size:12px; color:var(--text-secondary); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${{escTwinHtml(it.division_name || it.industry_sector || 'Enterprise')}} · ${{pCnt}} Pillars · ${{it.active_agents_count || 60}}/60 Agents</div>
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
        active_pillars_count: ov.active_pillars_count || (ov.custom_pillars || []).length || 6,
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

    async function resolveTwinStudioApiBase() {{
      try {{
        const r0 = await fetch('/api/v1/health');
        if (r0.ok) {{
          const d0 = await r0.json();
          if (d0 && d0.status === 'healthy') return '';
        }}
      }} catch (e) {{}}
      try {{
        const r1 = await fetch('http://localhost:8095/api/v1/health');
        if (r1.ok) {{
          const d1 = await r1.json();
          if (d1 && d1.status === 'healthy') return 'http://localhost:8095';
        }}
      }} catch (e) {{}}
      return null;
    }}

    async function executeTwinGeneration() {{
      const coEl = document.getElementById('twinCompanyInput');
      const divEl = document.getElementById('twinDivisionInput');
      const geoEl = document.getElementById('twinGeoInput');
      const focusEl = document.getElementById('twinFocusInput');
      const logoEl = document.getElementById('twinLogoUrlInput');
      const refreshEl = document.getElementById('twinForceRefreshCheckbox');

      const company = (coEl ? coEl.value : '').trim();
      if (!company) {{
        if (coEl) coEl.focus();
        return;
      }}
      const division = (divEl ? divEl.value : '').trim();
      const geography = (geoEl ? geoEl.value : '').trim() || 'Global';
      const notes = (focusEl ? focusEl.value : '').trim();
      const logoUrl = (logoEl ? logoEl.value : '').trim();
      const forceRefresh = refreshEl ? Boolean(refreshEl.checked) : true;

      const hud = document.getElementById('twinProgressHud');
      const hudStatus = document.getElementById('hudStatusText');
      const hudPct = document.getElementById('hudPercentText');
      const hudBar = document.getElementById('hudProgressBar');
      const hudLog = document.getElementById('hudStepLog');
      if (hud) hud.style.display = 'block';
      if (hudLog) hudLog.innerHTML = '';

      const appendStep = (pct, msg, detail, isErr = false) => {{
        if (hudStatus) {{
          hudStatus.textContent = msg;
          hudStatus.style.color = isErr ? 'var(--g-red)' : 'var(--g-blue)';
        }}
        if (hudPct) hudPct.textContent = pct + '%';
        if (hudBar) hudBar.style.width = pct + '%';
        if (hudLog) {{
          const row = document.createElement('div');
          row.innerHTML = `<span style="color:${{isErr ? 'var(--g-red)' : 'var(--g-green)'}}; font-weight:700;">[${{pct}}%]</span> ${{escTwinHtml(msg)}} ${{detail ? `<span style="color:var(--text-muted);">— ${{escTwinHtml(detail)}}</span>` : ''}}`;
          hudLog.appendChild(row);
        }}
      }};

      appendStep(5, `Connecting to Enterprise Twin Research Engine for ${{company}}...`, 'Gemini 3.1 Pro + Google Search Grounding');
      const apiBase = await resolveTwinStudioApiBase();
      if (apiBase === null) {{
        appendStep(0, 'Live Research Server unreachable on this static host.', 'Open Enterprise Twin Studio (port 8095 / Cloud Run) to synthesize new companies in real time.', true);
        return;
      }}

      try {{
        const response = await fetch(`${{apiBase}}/api/v1/twins/generate-stream`, {{
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
        }});

        if (!response.ok || !response.body) {{
          throw new Error(`HTTP ${{response.status}}`);
        }}

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buf = '';
        let finalPayload = null;

        while (true) {{
          const {{ value, done }} = await reader.read();
          if (done) break;
          buf += decoder.decode(value, {{ stream: true }});
          const blocks = buf.split('\\n\\n');
          buf = blocks.pop() || '';
          for (const block of blocks) {{
            const dataLine = block.split('\\n').find(l => l.startsWith('data:'));
            if (!dataLine) continue;
            const ev = JSON.parse(dataLine.slice(5).trim());
            if (ev.error) throw new Error(ev.error);
            const pct = Number(ev.pct || 10);
            if (ev.message) appendStep(pct, ev.message, ev.detail || '');
            if (ev.stage === 'done') finalPayload = ev;
          }}
        }}

        if (finalPayload && finalPayload.overlay) {{
          if (apiBase === '' && finalPayload.redirect_url) {{
            setTimeout(() => {{ window.location.href = finalPayload.redirect_url; }}, 400);
          }} else {{
            applyBrowserTwin(finalPayload.overlay);
            setTimeout(() => closeEnterpriseTwinModal(), 500);
          }}
        }}
      }} catch (err) {{
        appendStep(0, `Synthesis failed: ${{err.message || err}}`, 'Please retry.', true);
      }}
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

    # 2. Add or update discreet `⇄` Portal Studio button in `<header class="navbar">`
    old_nav_btn = '      <button type="button" class="nav-pill-btn twin-studio-pill" onclick="openTwinStudioEntry(event)">Company Twin</button>\n'
    nav_btn_html = '      <button type="button" class="nav-pill-btn twin-studio-pill" onclick="openTwinStudioEntry(event)" title="Portal Studio" aria-label="Portal Studio">⇄</button>\n'
    if old_nav_btn in html:
        html = html.replace(old_nav_btn, nav_btn_html, 1)
    elif 'onclick="openTwinStudioEntry(event)"' not in html:
        target_theme_btn = '      <button type="button" id="themeToggleBtn"'
        if target_theme_btn in html:
            html = html.replace(target_theme_btn, nav_btn_html + target_theme_btn, 1)

    # 3. Ensure meta groundingSource badge is NOT shown on customer-facing Persona pages
    grounding_line = "\n                ${p.groundingSource ? `<div style=\"margin-top:5px; font-size:11.5px; font-weight:700; color:var(--sc-cyan);\">🔍 ${escTwinHtml(p.groundingSource)}</div>` : ''}"
    if grounding_line in html:
        html = html.replace(grounding_line, "")

    # 4. Inject 1-line `renderAgentTwinDivisionBanner(ag)` inside `openAgentPage` right below `.back-bar`
    if "renderAgentTwinDivisionBanner(ag)" not in html:
        fn_pos = html.index("function openAgentPage(")
        back_bar_pos = html.index('<div class="back-bar">', fn_pos)
        pills_pos = html.index('<div class="persona-switcher-pills">', back_bar_pos)
        close_after_pills = html.index("</div>\n          </div>", pills_pos) + len("</div>\n          </div>")
        html = html[:close_after_pills] + "\n          ${renderAgentTwinDivisionBanner(ag)}" + html[close_after_pills:]

    # 5. Replace `<div id="enterpriseTwinModal"...` block right before `GLOBAL EXECUTIVE ATTRIBUTION FOOTER`
    modal_start = html.index('<div id="enterpriseTwinModal"')
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
    if "ENTERPRISE TWIN STUDIO V2" in html:
        js_block_marker = html.rindex("ENTERPRISE TWIN STUDIO V2", 0, last_script_close)
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

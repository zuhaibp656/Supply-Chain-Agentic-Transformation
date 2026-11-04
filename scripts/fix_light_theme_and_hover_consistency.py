#!/usr/bin/env python3
"""Fix Light Theme hover text disappearance and enforce 100% Light/Dark UI consistency.

Updates index.html, regenerates periodic_table.html and mind_map.html with their
boot-route overrides preserved, and syncs docs/ and zipline_dist/ mirrors.
"""

from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parent.parent


def must_replace(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"Expected snippet not found for [{label}]")
    return text.replace(old, new, 1)


def apply_fixes(html: str) -> str:
    # 1. Root & Light Theme CSS custom properties (--bg-elevated, --svg-*, --vc-*, --cad-*)
    old_root_vars = """    :root, html[data-theme="dark"] {
      --bg-page: #080b12;
      --bg-surface: #0f1522;
      --bg-card: #131b2b;
      --bg-card-hover: #192338;
      --text-primary: #f1f5f9;
      --text-secondary: #cbd5e1;
      --text-muted: #94a3b8;
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-strong: rgba(255, 255, 255, 0.14);"""

    new_root_vars = """    :root, html[data-theme="dark"] {
      --bg-page: #080b12;
      --bg-surface: #0f1522;
      --bg-card: #131b2b;
      --bg-card-hover: #192338;
      --bg-elevated: #172236;
      --text-primary: #f1f5f9;
      --text-secondary: #cbd5e1;
      --text-muted: #94a3b8;
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-strong: rgba(255, 255, 255, 0.14);

      /* Theme-Aware SVG, Process Diagram & CAD Simulator Tokens */
      --svg-node-fill: #081122;
      --svg-node-alt: #0f172a;
      --svg-node-text: #f8fafc;
      --svg-guide-stroke: rgba(255, 255, 255, 0.48);
      --svg-track-bg: #1e293b;
      --svg-packet-fill: #ffffff;
      --vc-node-fill: #0f172a;
      --vc-node-active: #172542;
      --vc-node-active-stroke: #ffffff;
      --vc-pill-bg: #090d16;
      --vc-pill-text: #a5b4fc;
      --vc-sys-bg: rgba(255, 255, 255, 0.04);
      --vc-sys-border: rgba(255, 255, 255, 0.12);
      --vc-sys-text: #e2e8f0;
      --vc-grid-stroke: rgba(255, 255, 255, 0.04);
      --cad-svg-bg: #04070f;
      --cad-panel-bg: rgba(15, 23, 42, 0.88);
      --cad-node-bg: #081020;
      --cad-hud-bg: rgba(11, 15, 24, 0.94);
      --cad-hud-border: rgba(255, 255, 255, 0.15);
      --cad-text-main: #f8fafc;
      --cad-text-muted: #9aa0a6;
      --cad-text-blue: #8ab4f8;
      --cad-text-green: #81c995;
      --cad-text-amber: #fde293;
      --cad-text-red: #ff8a80;"""

    html = must_replace(html, old_root_vars, new_root_vars, "dark root vars")

    old_light_vars = """    html[data-theme="light"] {
      --bg-page: #ffffff;
      --bg-surface: #f8f9fa;
      --bg-card: #ffffff;
      --bg-card-hover: #f1f3f4;
      --text-primary: #202124;
      --text-secondary: #3c4043;
      --text-muted: #5f6368;
      --border-subtle: #e0e3e7;
      --border-strong: #cbd2d9;"""

    new_light_vars = """    html[data-theme="light"] {
      --bg-page: #f4f7fc;
      --bg-surface: #eef3fa;
      --bg-card: #ffffff;
      --bg-card-hover: #f0f6ff;
      --bg-elevated: #f3f7fd;
      --text-primary: #0f172a;
      --text-secondary: #334155;
      --text-muted: #5f6368;
      --border-subtle: #dbe3ee;
      --border-strong: #cbd5e1;

      /* Theme-Aware SVG, Process Diagram & CAD Simulator Tokens (Light Mode) */
      --svg-node-fill: #ffffff;
      --svg-node-alt: #e8f0fe;
      --svg-node-text: #0f172a;
      --svg-guide-stroke: rgba(26, 115, 232, 0.45);
      --svg-track-bg: #dbe7f6;
      --svg-packet-fill: #1a73e8;
      --vc-node-fill: #ffffff;
      --vc-node-active: #eff6ff;
      --vc-node-active-stroke: #1a73e8;
      --vc-pill-bg: #eef4ff;
      --vc-pill-text: #1e40af;
      --vc-sys-bg: #f8fafc;
      --vc-sys-border: #cbd5e1;
      --vc-sys-text: #334155;
      --vc-grid-stroke: rgba(26, 115, 232, 0.08);
      --cad-svg-bg: #f4f8ff;
      --cad-panel-bg: #ffffff;
      --cad-node-bg: #ffffff;
      --cad-hud-bg: #ffffff;
      --cad-hud-border: #cbd5e1;
      --cad-text-main: #0f172a;
      --cad-text-muted: #475569;
      --cad-text-blue: #1d4ed8;
      --cad-text-green: #15803d;
      --cad-text-amber: #b45309;
      --cad-text-red: #dc2626;"""

    html = must_replace(html, old_light_vars, new_light_vars, "light root vars")

    # 2. Append comprehensive Light Mode hover & consistency stylesheet before </style>
    light_mode_consistency_css = """
    /* =========================================================================
       LIGHT MODE HOVER & SURFACE CONSISTENCY OVERRIDES (ZERO DISAPPEARING TEXT)
       ========================================================================= */

    /* Fix badge contrast on saturated pillar colors in both themes */
    .dept-node:hover .dept-anim-badge,
    .dept-node.active .dept-anim-badge,
    .vc-entry-card:hover .dept-anim-badge,
    .vc-entry-card.active .dept-anim-badge {
      color: #ffffff !important;
    }

    /* Fix Pillar & Process Card Hover Disappearing Text ("4 Sub-Pillars · 12 Personas →") */
    html[data-theme="light"] .dept-anim-stage,
    html[data-theme="light"] .vc-entry-card .dept-anim-stage {
      background: linear-gradient(145deg, #f0f6ff 0%, #f8fbff 100%) !important;
      border: 1.5px solid #cbd5e1 !important;
      box-shadow: inset 0 1px 4px rgba(26, 115, 232, 0.06) !important;
    }
    html[data-theme="light"] .dept-node:hover .dept-anim-stage,
    html[data-theme="light"] .dept-node.active .dept-anim-stage,
    html[data-theme="light"] .vc-entry-card:hover .dept-anim-stage,
    html[data-theme="light"] .vc-entry-card.active .dept-anim-stage {
      background: linear-gradient(145deg, #e3eeff 0%, #f1f7ff 100%) !important;
      border-color: var(--dept-accent, var(--vc-accent, #1a73e8)) !important;
      box-shadow: 0 8px 20px rgba(26, 115, 232, 0.12) !important;
    }
    html[data-theme="light"] .dept-anim-badge {
      background: rgba(255, 255, 255, 0.96) !important;
      color: #0f172a !important;
      border: 1px solid #cbd5e1 !important;
      box-shadow: 0 2px 6px rgba(15, 23, 42, 0.06) !important;
    }
    html[data-theme="light"] .dept-anim-meta {
      background: rgba(255, 255, 255, 0.96) !important;
      color: #1a73e8 !important;
      border: 1px solid #bfdbfe !important;
      box-shadow: 0 2px 6px rgba(15, 23, 42, 0.05) !important;
    }
    html[data-theme="light"] .dept-node:hover .dept-anim-badge,
    html[data-theme="light"] .dept-node.active .dept-anim-badge,
    html[data-theme="light"] .vc-entry-card:hover .dept-anim-badge,
    html[data-theme="light"] .vc-entry-card.active .dept-anim-badge,
    html[data-theme="light"] .dept-node:hover .dept-anim-meta,
    html[data-theme="light"] .dept-node.active .dept-anim-meta,
    html[data-theme="light"] .vc-entry-card:hover .dept-anim-meta,
    html[data-theme="light"] .vc-entry-card.active .dept-anim-meta {
      background: var(--dept-accent, var(--vc-accent, #1a73e8)) !important;
      color: #ffffff !important;
      border-color: var(--dept-accent, var(--vc-accent, #1a73e8)) !important;
      box-shadow: 0 4px 12px rgba(15, 23, 42, 0.16) !important;
    }

    /* Restore Colored Top/Left Accent Bars & Hover Highlights Across All Portal Cards */
    html[data-theme="light"] .dept-node {
      background: #ffffff !important;
      border: 1.5px solid #cbd5e1 !important;
      border-top: 4px solid var(--dept-accent, #1a73e8) !important;
    }
    html[data-theme="light"] .dept-node:hover,
    html[data-theme="light"] .dept-node.active {
      background: #ffffff !important;
      border-color: var(--dept-accent, #1a73e8) !important;
      border-top: 4px solid var(--dept-accent, #1a73e8) !important;
      box-shadow: 0 18px 38px rgba(26, 115, 232, 0.16) !important;
    }
    html[data-theme="light"] .dept-node:hover .dept-name,
    html[data-theme="light"] .dept-node.active .dept-name {
      color: #0f172a !important;
    }
    html[data-theme="light"] .dept-node:hover .dept-tagline,
    html[data-theme="light"] .dept-node.active .dept-tagline {
      color: #334155 !important;
    }

    html[data-theme="light"] .vc-entry-card {
      background: #ffffff !important;
      border: 1.5px solid #cbd5e1 !important;
      border-top: 4px solid var(--vc-accent, #1a73e8) !important;
      box-shadow: 0 10px 26px rgba(15, 23, 42, 0.07) !important;
    }
    html[data-theme="light"] .vc-entry-card:hover {
      background: #ffffff !important;
      border-color: var(--vc-accent, #1a73e8) !important;
      border-top: 4px solid var(--vc-accent, #1a73e8) !important;
      box-shadow: 0 18px 38px rgba(26, 115, 232, 0.16) !important;
    }
    html[data-theme="light"] .vc-entry-title,
    html[data-theme="light"] .vc-entry-card:hover .vc-entry-title {
      color: #0f172a !important;
    }
    html[data-theme="light"] .vc-entry-desc,
    html[data-theme="light"] .vc-entry-card:hover .vc-entry-desc {
      color: #334155 !important;
    }

    html[data-theme="light"] .subpillar-box-card {
      background: #ffffff !important;
      border: 1.5px solid #cbd5e1 !important;
      border-top: 4px solid var(--sp-color, var(--dept-accent, #1a73e8)) !important;
    }
    html[data-theme="light"] .subpillar-box-card:hover,
    html[data-theme="light"] .subpillar-box-card.active {
      background: #f8fbff !important;
      border-color: var(--sp-color, var(--dept-accent, #1a73e8)) !important;
      border-top: 4px solid var(--sp-color, var(--dept-accent, #1a73e8)) !important;
      box-shadow: 0 14px 30px rgba(26, 115, 232, 0.14) !important;
    }
    html[data-theme="light"] .subpillar-box-card:hover .subpillar-box-title,
    html[data-theme="light"] .subpillar-box-card.active .subpillar-box-title {
      color: #0f172a !important;
    }

    html[data-theme="light"] .human-persona-card {
      background: #ffffff !important;
      border: 1.5px solid #cbd5e1 !important;
      border-left: 5px solid var(--dept-accent, #1a73e8) !important;
    }
    html[data-theme="light"] .human-persona-card:hover {
      background: #f8fbff !important;
      border-color: var(--dept-accent, #1a73e8) !important;
      border-left: 5px solid var(--dept-accent, #1a73e8) !important;
      box-shadow: 0 14px 30px rgba(26, 115, 232, 0.14) !important;
    }
    html[data-theme="light"] .human-persona-card:hover .human-persona-title {
      color: #0f172a !important;
    }

    html[data-theme="light"] .ai-agent-chip-card {
      background: #fafbff !important;
      border: 1.5px solid #d8dee9 !important;
    }
    html[data-theme="light"] .ai-agent-chip-card:hover {
      background: #f3f0ff !important;
      border-color: var(--sc-violet, #681da8) !important;
      box-shadow: 0 12px 24px rgba(104, 29, 168, 0.12) !important;
    }
    html[data-theme="light"] .ai-agent-chip-card:hover .ai-agent-chip-name {
      color: #1e1b4b !important;
    }

    html[data-theme="light"] .catalog-card,
    html[data-theme="light"] .dir-persona-card {
      background: #ffffff !important;
      border: 1.5px solid #cbd5e1 !important;
      border-top: 4px solid var(--dept-accent, #1a73e8) !important;
    }
    html[data-theme="light"] .catalog-card:hover,
    html[data-theme="light"] .dir-persona-card:hover {
      background: #ffffff !important;
      border-color: var(--dept-accent, #1a73e8) !important;
      border-top: 4px solid var(--dept-accent, #1a73e8) !important;
      box-shadow: 0 18px 36px rgba(26, 115, 232, 0.15) !important;
    }
    html[data-theme="light"] .catalog-thumb {
      background: linear-gradient(145deg, #eef4ff 0%, #f8fbff 100%) !important;
      border-bottom: 1px solid #dbe5f3 !important;
    }

    html[data-theme="light"] .pt-tile {
      background: #ffffff !important;
      border: 1.5px solid #cbd5e1 !important;
      border-top: 3.5px solid var(--tile-color, #1a73e8) !important;
    }
    html[data-theme="light"] .pt-tile:hover,
    html[data-theme="light"] .pt-tile.active {
      background: #eff6ff !important;
      border-color: var(--tile-color, #1a73e8) !important;
      border-top: 3.5px solid var(--tile-color, #1a73e8) !important;
      box-shadow: 0 12px 24px rgba(26, 115, 232, 0.16) !important;
    }
    html[data-theme="light"] .pt-tile:hover .pt-tile-title,
    html[data-theme="light"] .pt-tile.active .pt-tile-title {
      color: #0f172a !important;
    }

    html[data-theme="light"] .mm-node-btn {
      background: #f8fafd !important;
      border: 1.5px solid #cbd5e1 !important;
      border-left: 4px solid var(--node-color, #1a73e8) !important;
      color: #0f172a !important;
    }
    html[data-theme="light"] .mm-node-btn:hover,
    html[data-theme="light"] .mm-node-btn.active {
      background: #e8f0fe !important;
      border-color: var(--node-color, #1a73e8) !important;
      border-left: 4px solid var(--node-color, #1a73e8) !important;
      color: #0f172a !important;
    }
    html[data-theme="light"] .mm-flow-card:hover,
    html[data-theme="light"] .mm-flow-card.active {
      background: #f0f6ff !important;
      border-color: var(--fc-color, #1a73e8) !important;
      color: #0f172a !important;
    }

    /* Fix AI Function Stack Agent Link Chip Hover (Prevent Dark Background on Dark Text) */
    html[data-theme="light"] .sc-fn-agent-link-chip {
      background: #f8fafc !important;
      border: 1px solid #cbd5e1 !important;
      color: #0f172a !important;
    }
    html[data-theme="light"] .sc-fn-agent-link-chip:hover {
      background: #e8f0fe !important;
      border-color: #1a73e8 !important;
      color: #0f172a !important;
      box-shadow: 0 6px 16px rgba(26, 115, 232, 0.15) !important;
    }
    html[data-theme="light"] .sc-fn-agent-link-chip:hover .chip-name {
      color: #174ea6 !important;
    }

    /* Fix Value Chain Stage Owner Button, Switch Pills, CAD Simulator Controls & Hero Secondary CTA */
    html[data-theme="light"] .vc-owner-btn {
      background: #f1f5fb !important;
      color: #0f172a !important;
      border: 1px solid #cbd5e1 !important;
    }
    html[data-theme="light"] .vc-owner-btn:hover {
      background: var(--g-blue) !important;
      color: #ffffff !important;
      border-color: var(--g-blue) !important;
    }
    html[data-theme="light"] .switch-pill.active,
    html[data-theme="light"] .switch-pill.active:hover {
      background: var(--g-blue);
      color: #ffffff;
      border-color: var(--g-blue);
    }
    html[data-theme="light"] .cad-bar {
      background: #eef4fb !important;
      border-bottom: 1px solid #cbd5e1 !important;
      color: #0f172a !important;
    }
    html[data-theme="light"] .cad-pill-btn {
      background: #ffffff !important;
      color: #334155 !important;
      border: 1px solid #cbd5e1 !important;
    }
    html[data-theme="light"] .cad-pill-btn:hover {
      background: #e8f0fe !important;
      color: #1a73e8 !important;
      border-color: #1a73e8 !important;
    }
    html[data-theme="light"] .cad-pill-btn.active,
    html[data-theme="light"] .cad-pill-btn.active:hover {
      background: #1a73e8 !important;
      color: #ffffff !important;
      border-color: #1a73e8 !important;
    }
    html[data-theme="light"] .secondary-hero-btn {
      background: #ffffff !important;
      color: #0f172a !important;
      border: 1.5px solid #cbd5e1 !important;
      box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08) !important;
    }
    html[data-theme="light"] .secondary-hero-btn:hover {
      background: #e8f0fe !important;
      color: #1a73e8 !important;
      border-color: #1a73e8 !important;
    }

    /* Process 6-Stage Diagram Wrap, Rich Bullet Points, Footer Accent Pills & Studio Modal */
    html[data-theme="light"] .simple-arch-svg-wrap {
      background: linear-gradient(180deg, #f8fbff 0%, #eef4ff 100%) !important;
      border: 1.5px solid #bfdbfe !important;
    }
    html[data-theme="light"] .sc-rich-points li {
      color: var(--text-secondary) !important;
    }
    html[data-theme="light"] .footer-accent-pill-blue {
      border-color: #93c5fd !important;
      color: #1d4ed8 !important;
      background: #eff6ff !important;
    }
    html[data-theme="light"] .footer-accent-pill-blue:hover {
      background: #1d4ed8 !important;
      color: #ffffff !important;
      border-color: #1d4ed8 !important;
    }
    html[data-theme="light"] .footer-accent-pill-green {
      border-color: #86efac !important;
      color: #047857 !important;
      background: #ecfdf5 !important;
    }
    html[data-theme="light"] .footer-accent-pill-green:hover {
      background: #047857 !important;
      color: #ffffff !important;
      border-color: #047857 !important;
    }
    html[data-theme="light"] #enterpriseTwinModal {
      background: rgba(15, 23, 42, 0.45) !important;
    }
    html[data-theme="light"] #enterpriseTwinModal .modal-card {
      box-shadow: 0 28px 72px rgba(15, 23, 42, 0.22) !important;
    }
"""

    html = must_replace(
        html,
        "    /* === PORTAL V2.2 HIERARCHY & CLEAN SAA-S LAYOUT END === */\n\n  </style>",
        "    /* === PORTAL V2.2 HIERARCHY & CLEAN SAA-S LAYOUT END === */\n"
        + light_mode_consistency_css
        + "\n  </style>",
        "append light mode consistency CSS",
    )

    # 3. Fix Global Footer Brand Title & Accent Pills (L8536-8553)
    old_footer = """      <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
        <span style="font-family:var(--font-display); font-size:17px; font-weight:800; color:#ffffff;">
          Gemini Enterprise · Supply Chain &amp; Demand (Office of the CSCO)
        </span>"""
    new_footer = """      <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
        <span style="font-family:var(--font-display); font-size:17px; font-weight:800; color:var(--text-primary);">
          Gemini Enterprise · Supply Chain &amp; Demand (Office of the CSCO)
        </span>"""
    html = must_replace(html, old_footer, new_footer, "footer brand title")

    old_footer_pills = """      <button type="button" class="switch-pill" style="border-color:rgba(0,210,255,0.45); color:#7dd3fc;" onclick="openPeriodicTablePage('all', null, true)">🧪 Periodic Table</button>
      <button type="button" class="switch-pill" style="border-color:rgba(16,185,129,0.45); color:#6ee7b7;" onclick="openMindMapPage('all', null, true)">🧠 Neural Mind Map</button>
      <a href="periodic_table.html" class="switch-pill" style="border-color:rgba(56,189,248,0.35); color:#bae6fd;">Standalone Periodic Table ↗</a>
      <a href="mind_map.html" class="switch-pill" style="border-color:rgba(16,185,129,0.35); color:#a7f3d0;">Standalone Mind Map ↗</a>"""
    new_footer_pills = """      <button type="button" class="switch-pill footer-accent-pill-blue" style="border-color:rgba(0,210,255,0.45); color:#7dd3fc;" onclick="openPeriodicTablePage('all', null, true)">🧪 Periodic Table</button>
      <button type="button" class="switch-pill footer-accent-pill-green" style="border-color:rgba(16,185,129,0.45); color:#6ee7b7;" onclick="openMindMapPage('all', null, true)">🧠 Neural Mind Map</button>
      <a href="periodic_table.html" class="switch-pill footer-accent-pill-blue" style="border-color:rgba(56,189,248,0.35); color:#bae6fd;">Standalone Periodic Table ↗</a>
      <a href="mind_map.html" class="switch-pill footer-accent-pill-green" style="border-color:rgba(16,185,129,0.35); color:#a7f3d0;">Standalone Mind Map ↗</a>"""
    html = must_replace(html, old_footer_pills, new_footer_pills, "footer accent pills")

    # 4. Hero Supply Chain Canvas Light Mode awareness (L66049-66226)
    old_hero_wms = """        // Glowing 3D WMS & Fulfillment Hub Node at the outbound end of the conveyor
        ctx.beginPath();
        ctx.arc(wmsHubX, wmsHubY, 24, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(0, 210, 255, 0.14)';
        ctx.fill();

        ctx.beginPath();
        ctx.arc(wmsHubX, wmsHubY, 15, 0, Math.PI * 2);
        ctx.fillStyle = '#081020';
        ctx.fill();
        ctx.strokeStyle = '#38bdf8';
        ctx.lineWidth = 2.8;
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(wmsHubX, wmsHubY, 6, 0, Math.PI * 2);
        ctx.fillStyle = '#00d2ff';
        ctx.fill();

        ctx.fillStyle = 'rgba(248, 249, 250, 0.88)';"""

    new_hero_wms = """        const isLightHero = document.documentElement.getAttribute('data-theme') === 'light';
        // Glowing 3D WMS & Fulfillment Hub Node at the outbound end of the conveyor
        ctx.beginPath();
        ctx.arc(wmsHubX, wmsHubY, 24, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(0, 210, 255, 0.14)';
        ctx.fill();

        ctx.beginPath();
        ctx.arc(wmsHubX, wmsHubY, 15, 0, Math.PI * 2);
        ctx.fillStyle = isLightHero ? '#ffffff' : '#081020';
        ctx.fill();
        ctx.strokeStyle = '#38bdf8';
        ctx.lineWidth = 2.8;
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(wmsHubX, wmsHubY, 6, 0, Math.PI * 2);
        ctx.fillStyle = '#00d2ff';
        ctx.fill();

        ctx.fillStyle = isLightHero ? 'rgba(15, 23, 42, 0.88)' : 'rgba(248, 249, 250, 0.88)';"""
    html = must_replace(html, old_hero_wms, new_hero_wms, "hero canvas wms hub")

    html = must_replace(
        html,
        """          ctx.beginPath();
          ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
          ctx.fillStyle = '#081020';""",
        """          ctx.beginPath();
          ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
          ctx.fillStyle = isLightHero ? '#ffffff' : '#081020';""",
        "hero canvas tier nodes",
    )

    old_hero_corridors = """        // 6. MID/BOTTOM-RIGHT WING: Enlarged Multi-Modal Global Transit & Fleet Network
        [64, 122, 182, 240].forEach((rad, rIdx) => {
          ctx.beginPath();
          ctx.arc(hubX, hubY, rad, 0, Math.PI * 2);
          ctx.strokeStyle = rIdx % 2 === 0 ? 'rgba(0, 210, 255, 0.08)' : 'rgba(255, 255, 255, 0.05)';"""
    new_hero_corridors = """        // 6. MID/BOTTOM-RIGHT WING: Enlarged Multi-Modal Global Transit & Fleet Network
        const isLightCorridor = document.documentElement.getAttribute('data-theme') === 'light';
        [64, 122, 182, 240].forEach((rad, rIdx) => {
          ctx.beginPath();
          ctx.arc(hubX, hubY, rad, 0, Math.PI * 2);
          ctx.strokeStyle = isLightCorridor ? (rIdx % 2 === 0 ? 'rgba(26, 115, 232, 0.14)' : 'rgba(15, 23, 42, 0.07)') : (rIdx % 2 === 0 ? 'rgba(0, 210, 255, 0.08)' : 'rgba(255, 255, 255, 0.05)');"""
    html = must_replace(html, old_hero_corridors, new_hero_corridors, "hero corridor rings")

    html = must_replace(
        html,
        """          ctx.beginPath();
          ctx.arc(c.ex, c.ey, 7, 0, Math.PI * 2);
          ctx.fillStyle = '#070b14';""",
        """          ctx.beginPath();
          ctx.arc(c.ex, c.ey, 7, 0, Math.PI * 2);
          ctx.fillStyle = isLightCorridor ? '#ffffff' : '#070b14';""",
        "hero corridor endpoints",
    )

    html = must_replace(
        html,
        """          ctx.fillStyle = '#080d18';
          ctx.strokeStyle = c.col;
          ctx.lineWidth = 1.9;
          ctx.beginPath();
          ctx.roundRect(pt.x - 13, pt.y - 8, 26, 16, 4.5);""",
        """          ctx.fillStyle = isLightCorridor ? '#ffffff' : '#080d18';
          ctx.strokeStyle = c.col;
          ctx.lineWidth = 1.9;
          ctx.beginPath();
          ctx.roundRect(pt.x - 13, pt.y - 8, 26, 16, 4.5);""",
        "hero corridor moving carrier",
    )

    html = must_replace(
        html,
        """        ctx.beginPath();
        ctx.arc(hubX, hubY, 18, 0, Math.PI * 2);
        ctx.fillStyle = '#081020';
        ctx.fill();
        ctx.strokeStyle = '#00d2ff';
        ctx.lineWidth = 3.2;
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(hubX, hubY, 7, 0, Math.PI * 2);
        ctx.fillStyle = '#00d2ff';
        ctx.fill();

        ctx.fillStyle = 'rgba(248, 249, 250, 0.90)';""",
        """        ctx.beginPath();
        ctx.arc(hubX, hubY, 18, 0, Math.PI * 2);
        ctx.fillStyle = isLightCorridor ? '#ffffff' : '#081020';
        ctx.fill();
        ctx.strokeStyle = '#00d2ff';
        ctx.lineWidth = 3.2;
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(hubX, hubY, 7, 0, Math.PI * 2);
        ctx.fillStyle = '#00d2ff';
        ctx.fill();

        ctx.fillStyle = isLightCorridor ? 'rgba(15, 23, 42, 0.88)' : 'rgba(248, 249, 250, 0.90)';""",
        "hero central multimodal hub",
    )

    # 5. Pillar & Process Card Watermark SVGs (renderSupplyChainWatermarkSvg)
    wm_start = "    function renderSupplyChainWatermarkSvg(watermarkType, color, cssClass = 'dept-stage-svg') {"
    wm_end = "    /* =========================================================================\n       3-PART PURPOSE-BUILT ANIMATION TAXONOMY:"
    s_idx = html.index(wm_start)
    e_idx = html.index(wm_end, s_idx)
    wm_block = html[s_idx:e_idx]
    wm_block = wm_block.replace('fill="#081122"', 'fill="var(--svg-node-fill)"')
    wm_block = wm_block.replace('fill="#0f172a"', 'fill="var(--svg-node-alt)"')
    wm_block = wm_block.replace('fill="rgba(8,17,34,0.9)"', 'fill="var(--svg-node-fill)"')
    wm_block = wm_block.replace('fill="#1e293b"', 'fill="var(--svg-track-bg)"')
    wm_block = wm_block.replace('fill="#fff"', 'fill="var(--svg-node-text)"')
    wm_block = wm_block.replace('fill="#f8fafc"', 'fill="var(--svg-node-text)"')
    wm_block = wm_block.replace('fill="#e2e8f0"', 'fill="var(--svg-node-text)"')
    wm_block = wm_block.replace('fill="#ffffff"', 'fill="var(--svg-packet-fill)"')
    wm_block = wm_block.replace('stroke="#ffffff" stroke-opacity="0.45"', 'stroke="var(--svg-guide-stroke)"')
    wm_block = wm_block.replace('stroke="#ffffff" stroke-opacity="0.65"', 'stroke="var(--svg-guide-stroke)"')
    html = html[:s_idx] + wm_block + html[e_idx:]

    # 6. Interactive CAD Stage SVGs (renderInteractiveCadStage)
    cad_start = "    function renderInteractiveCadStage(cadType, mountId) {"
    cad_end = "    function refreshCadMount(cadType, mountId) {"
    cs_idx = html.index(cad_start)
    ce_idx = html.index(cad_end, cs_idx)
    cad_block = html[cs_idx:ce_idx]
    cad_block = cad_block.replace(
        'style="width:100%;height:auto;display:block;background:#04070f;"',
        'class="cad-sim-svg" style="width:100%;height:auto;display:block;background:var(--cad-svg-bg);"',
    )
    cad_block = cad_block.replace('fill="rgba(15,23,42,0.85)"', 'fill="var(--cad-panel-bg)"')
    cad_block = cad_block.replace('fill="rgba(15,23,42,0.88)"', 'fill="var(--cad-panel-bg)"')
    cad_block = cad_block.replace('fill="rgba(8,13,24,0.95)"', 'fill="var(--cad-node-bg)"')
    cad_block = cad_block.replace('fill="rgba(4,9,18,0.92)"', 'fill="var(--cad-node-bg)"')
    cad_block = cad_block.replace('fill="#080d18"', 'fill="var(--cad-node-bg)"')
    cad_block = cad_block.replace('fill="#081020"', 'fill="var(--cad-node-bg)"')
    cad_block = cad_block.replace('fill="#0b0f18"', 'fill="var(--cad-node-bg)"')
    cad_block = cad_block.replace(
        'fill="rgba(11,15,24,0.94)" stroke="rgba(255,255,255,0.15)"',
        'fill="var(--cad-hud-bg)" stroke="var(--cad-hud-border)" stroke-width="1.4"',
    )
    cad_block = cad_block.replace('fill="#9aa0a6"', 'fill="var(--cad-text-muted)"')
    cad_block = cad_block.replace('fill="#f8fafc"', 'fill="var(--cad-text-main)"')
    cad_block = cad_block.replace('fill="#f8f9fa"', 'fill="var(--cad-text-main)"')
    cad_block = cad_block.replace('fill="#8ab4f8"', 'fill="var(--cad-text-blue)"')
    cad_block = cad_block.replace("color:#8ab4f8;", "color:var(--cad-text-blue);")
    cad_block = cad_block.replace('fill="#81c995"', 'fill="var(--cad-text-green)"')
    cad_block = cad_block.replace("color:#81c995", "color:var(--cad-text-green)")
    cad_block = cad_block.replace('fill="#fde293"', 'fill="var(--cad-text-amber)"')
    cad_block = cad_block.replace("?#81c995:#ff8a80", "?var(--cad-text-green):var(--cad-text-red)")
    cad_block = cad_block.replace("?'#81c995':'#ff8a80'", "?'var(--cad-text-green)':'var(--cad-text-red)'")
    # supplier_radar node labels that sit on --cad-node-bg circles
    cad_block = cad_block.replace(
        '<circle cx="85" cy="115" r="18" fill="var(--cad-node-bg)" stroke="#4285f4" stroke-width="2" /><text x="85" y="119" text-anchor="middle" fill="#fff" font-size="10">T3-A</text>',
        '<circle cx="85" cy="115" r="18" fill="var(--cad-node-bg)" stroke="#4285f4" stroke-width="2" /><text x="85" y="119" text-anchor="middle" fill="var(--cad-text-main)" font-size="10" font-weight="700">T3-A</text>',
    )
    cad_block = cad_block.replace(
        '<circle cx="85" cy="235" r="18" fill="var(--cad-node-bg)" stroke="#34a853" stroke-width="2" /><text x="85" y="239" text-anchor="middle" fill="#fff" font-size="10">T3-B</text>',
        '<circle cx="85" cy="235" r="18" fill="var(--cad-node-bg)" stroke="#34a853" stroke-width="2" /><text x="85" y="239" text-anchor="middle" fill="var(--cad-text-main)" font-size="10" font-weight="700">T3-B</text>',
    )
    cad_block = cad_block.replace(
        "fill=\"${tier2Disrupted ? '#ff8a80' : '#fff'}\"",
        "fill=\"${tier2Disrupted ? 'var(--cad-text-red)' : 'var(--cad-text-main)'}\"",
    )
    cad_block = cad_block.replace(
        '<circle cx="390" cy="175" r="25" fill="var(--cad-node-bg)" stroke="#4285f4" stroke-width="2.5" /><text x="390" y="179" text-anchor="middle" fill="#fff" font-size="10" font-weight="700">TIER-1</text>',
        '<circle cx="390" cy="175" r="25" fill="var(--cad-node-bg)" stroke="#4285f4" stroke-width="2.5" /><text x="390" y="179" text-anchor="middle" fill="var(--cad-text-main)" font-size="10" font-weight="700">TIER-1</text>',
    )
    cad_block = cad_block.replace(
        '<rect x="468" y="148" width="56" height="54" rx="10" fill="rgba(52,168,83,0.2)" stroke="#34a853" stroke-width="2.2" /><text x="496" y="179" text-anchor="middle" fill="#fff" font-size="10" font-weight="700">PLANT</text>',
        '<rect x="468" y="148" width="56" height="54" rx="10" fill="rgba(52,168,83,0.2)" stroke="#34a853" stroke-width="2.2" /><text x="496" y="179" text-anchor="middle" fill="var(--cad-text-main)" font-size="10" font-weight="700">PLANT</text>',
    )
    html = html[:cs_idx] + cad_block + html[ce_idx:]

    # 7. Sync Theme Storage Keys (sc_portal_theme & SC_PORTAL_THEME) + Universal Agents Heading
    old_theme_sync = """      try {
        localStorage.setItem('sc_portal_theme', validTheme);
      } catch (e) {}
    }

    function togglePortalTheme() {
      const cur = document.documentElement.getAttribute('data-theme') || 'dark';
      applyPortalTheme(cur === 'light' ? 'dark' : 'light');
    }

    function initPortalTheme() {
      let saved = 'dark';
      try {
        const params = new URLSearchParams(window.location.search);
        if (params.get('theme') === 'light' || params.get('theme') === 'dark') {
          saved = params.get('theme');
        } else {
          saved = localStorage.getItem('sc_portal_theme') || 'dark';
        }
      } catch (e) {}
      applyPortalTheme(saved);
    }"""

    new_theme_sync = """      try {
        localStorage.setItem('sc_portal_theme', validTheme);
        localStorage.setItem('SC_PORTAL_THEME', validTheme);
      } catch (e) {}
    }

    function togglePortalTheme() {
      const cur = document.documentElement.getAttribute('data-theme') || 'dark';
      applyPortalTheme(cur === 'light' ? 'dark' : 'light');
    }

    function initPortalTheme() {
      let saved = 'dark';
      try {
        const params = new URLSearchParams(window.location.search);
        if (params.get('theme') === 'light' || params.get('theme') === 'dark') {
          saved = params.get('theme');
        } else {
          saved = localStorage.getItem('sc_portal_theme') || localStorage.getItem('SC_PORTAL_THEME') || 'dark';
        }
      } catch (e) {}
      applyPortalTheme(saved);
    }"""
    html = must_replace(html, old_theme_sync, new_theme_sync, "portal theme storage sync")

    html = must_replace(
        html,
        """              <h3 style="font-family:var(--font-display); font-size:24px; font-weight:800; color:#f8fafc;">
                4 Cross-Persona Universal Supply Chain Agents
              </h3>""",
        """              <h3 style="font-family:var(--font-display); font-size:24px; font-weight:800; color:var(--text-primary);">
                4 Cross-Persona Universal Supply Chain Agents
              </h3>""",
        "universal agents heading",
    )

    # 8. Pillar Cadence Flow Cards (L67640-67962)
    cadence_start = "                <span>📅 5-Step Monthly S&amp;OP Cadence Timeline"
    cadence_end = "    /* Low-Code vs. Hybrid vs. High-Code Classification Helper */"
    p_s = html.index(cadence_start)
    p_e = html.index(cadence_end, p_s)
    cadence_block = html[p_s:p_e]
    cadence_block = cadence_block.replace("background:rgba(15,23,42,0.85);", "background:var(--bg-card);")
    cadence_block = cadence_block.replace("color:#fff;", "color:var(--text-primary);")
    cadence_block = cadence_block.replace("color:#94a3b8;", "color:var(--text-secondary);")
    html = html[:p_s] + cadence_block + html[p_e:]

    # 9. Blueprint 5-Stage SVG & GCP Connectors Panel (L68480-68630)
    bp_start = "              <div style=\"font-size:12.5px; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; color:${dept.color}; margin-bottom:4px;\">\n                ✦ 5-Stage Multi-Agent A2A System Topology"
    bp_end = "    /* =========================================================================\n       PAGE 3 RENDERING: EXECUTIVE SELLING AGENT PAGE (#agent/<id>)"
    b_s = html.index(bp_start)
    b_e = html.index(bp_end, b_s)
    bp_block = html[b_s:b_e]
    bp_block = bp_block.replace("color:#f8fafc;", "color:var(--text-primary);")
    bp_block = bp_block.replace("color:#cbd5e1;", "color:var(--text-secondary);")
    bp_block = bp_block.replace("background:rgba(4,9,18,0.85);", "background:var(--bg-elevated);")
    bp_block = bp_block.replace("background:#040812;", "background:var(--cad-svg-bg);")
    bp_block = bp_block.replace('fill="rgba(15,23,42,0.95)"', 'fill="var(--vc-node-fill)"')
    bp_block = bp_block.replace('fill="rgba(20,30,55,0.98)"', 'fill="var(--vc-node-active)"')
    bp_block = bp_block.replace('fill="#ffffff"', 'fill="var(--svg-node-text)"')
    bp_block = bp_block.replace('fill="#e2e8f0"', 'fill="var(--vc-sys-text)"')
    bp_block = bp_block.replace('fill="#f1f5f9"', 'fill="var(--vc-sys-text)"')
    html = html[:b_s] + bp_block + html[b_e:]

    # 10. Agent 4-Stage Topology Center Graphics (renderFullTopologySvg)
    topo_start = "    function renderFullTopologySvg(topology, ctx) {"
    topo_end = "        <!-- Animated Connection Arrows Across the 4 Simple, Meaningful Stages -->"
    t_s = html.index(topo_start)
    t_e = html.index(topo_end, t_s)
    topo_block = html[t_s:t_e]
    topo_block = topo_block.replace('fill="#0f172a"', 'fill="var(--svg-node-fill)"')
    topo_block = topo_block.replace('fill="rgba(15,23,42,0.78)"', 'fill="var(--svg-node-fill)"')
    topo_block = topo_block.replace('fill="rgba(15,23,42,0.85)"', 'fill="var(--svg-node-fill)"')
    html = html[:t_s] + topo_block + html[t_e:]

    # 11. ADK Codebase & XYZ Multi-Modal Data Lake Explorer (L70635-70984)
    adk_start = "    function selectDemoTableTab(agentId, tabIdx) {"
    adk_end = "    /* =========================================================================\n       PAGE 4 RENDERING: DEDICATED END-TO-END VALUE CHAIN PAGE"
    a_s = html.index(adk_start)
    a_e = html.index(adk_end, a_s)
    adk_block = html[a_s:a_e]
    adk_block = adk_block.replace(
        "          btn.style.background = 'rgba(0, 210, 255, 0.2)';\n          btn.style.borderColor = '#00d2ff';\n          btn.style.color = '#ffffff';\n        } else {\n          btn.style.background = 'rgba(15, 23, 42, 0.75)';\n          btn.style.borderColor = 'rgba(148, 163, 184, 0.28)';\n          btn.style.color = '#cbd5e1';",
        "          btn.style.background = 'var(--g-blue)';\n          btn.style.borderColor = 'var(--g-blue)';\n          btn.style.color = '#ffffff';\n        } else {\n          btn.style.background = 'var(--bg-elevated)';\n          btn.style.borderColor = 'var(--border-strong)';\n          btn.style.color = 'var(--text-secondary)';",
    )
    adk_block = adk_block.replace(
        "          btn.style.background = 'rgba(168, 85, 247, 0.24)';\n          btn.style.borderColor = '#c084fc';\n          btn.style.color = '#ffffff';\n        } else {\n          btn.style.background = 'rgba(15, 23, 42, 0.75)';\n          btn.style.borderColor = 'rgba(148, 163, 184, 0.28)';\n          btn.style.color = '#cbd5e1';",
        "          btn.style.background = 'var(--sc-violet)';\n          btn.style.borderColor = 'var(--sc-violet)';\n          btn.style.color = '#ffffff';\n        } else {\n          btn.style.background = 'var(--bg-elevated)';\n          btn.style.borderColor = 'var(--border-strong)';\n          btn.style.color = 'var(--text-secondary)';",
    )
    adk_block = adk_block.replace(
        "border:1px solid ${idx === 0 ? '#00d2ff' : 'rgba(148, 163, 184, 0.28)'}; background:${idx === 0 ? 'rgba(0, 210, 255, 0.2)' : 'rgba(15, 23, 42, 0.75)'}; color:${idx === 0 ? '#ffffff' : '#cbd5e1'};",
        "border:1px solid ${idx === 0 ? 'var(--g-blue)' : 'var(--border-strong)'}; background:${idx === 0 ? 'var(--g-blue)' : 'var(--bg-elevated)'}; color:${idx === 0 ? '#ffffff' : 'var(--text-secondary)'};",
    )
    adk_block = adk_block.replace(
        "border:1px solid #c084fc; background:rgba(168,85,247,0.24); color:#ffffff;",
        "border:1px solid var(--sc-violet); background:var(--sc-violet); color:#ffffff;",
    )
    adk_block = adk_block.replace(
        "border:1px solid rgba(148,163,184,0.28); background:rgba(15,23,42,0.75); color:#cbd5e1;",
        "border:1px solid var(--border-strong); background:var(--bg-elevated); color:var(--text-secondary);",
    )
    adk_block = adk_block.replace(
        "background:linear-gradient(145deg, rgba(15,23,42,0.94), rgba(9,13,22,0.97)); border:1px solid rgba(0,210,255,0.34); box-shadow:0 16px 40px rgba(0,0,0,0.42);",
        "background:var(--bg-card); border:1.5px solid var(--border-strong); box-shadow:0 12px 32px rgba(15,23,42,0.10);",
    )
    adk_block = adk_block.replace("background:rgba(15,23,42,0.8);", "background:var(--bg-elevated);")
    adk_block = adk_block.replace("background:rgba(15,23,42,0.95);", "background:var(--bg-elevated);")
    adk_block = adk_block.replace("background:rgba(9,13,22,0.88);", "background:var(--bg-card);")
    adk_block = adk_block.replace("background:rgba(9,13,22,0.92);", "background:var(--bg-elevated);")
    adk_block = adk_block.replace("background:rgba(9,13,22,0.9);", "background:var(--bg-elevated);")
    adk_block = adk_block.replace("color:#ffffff;", "color:var(--text-primary);")
    adk_block = adk_block.replace("color:#f8fafc;", "color:var(--text-primary);")
    adk_block = adk_block.replace("color:#e2e8f0;", "color:var(--text-primary);")
    adk_block = adk_block.replace("color:#cbd5e1;", "color:var(--text-secondary);")
    adk_block = adk_block.replace("color:#94a3b8;", "color:var(--text-muted);")
    adk_block = adk_block.replace("color:#fef3c7;", "color:var(--text-primary);")
    adk_block = adk_block.replace("color:#d1fae5;", "color:var(--text-primary);")
    adk_block = adk_block.replace("color:#e9d5ff;", "color:var(--sc-violet);")
    # Restore #ffffff on active first modality button where color:#ffffff; became var(--text-primary)
    adk_block = adk_block.replace(
        "border:1px solid var(--sc-violet); background:var(--sc-violet); color:var(--text-primary);",
        "border:1px solid var(--sc-violet); background:var(--sc-violet); color:#ffffff;",
    )
    html = html[:a_s] + adk_block + html[a_e:]

    # 12. Process 6-Stage Diagram SVG & Active Stage Pills (L70995-71245)
    old_vc_svg = """            <!-- Stage Node Box -->
            <rect x="${x}" y="88" width="166" height="184" rx="15"
                  fill="${isAct ? '#172542' : '#0f172a'}"
                  stroke="${isAct ? '#ffffff' : st.color}"
                  stroke-width="${isAct ? '2.5' : '1.6'}" />
            <!-- Top Color Header Strip -->
            <rect x="${x}" y="88" width="166" height="32" rx="15" fill="${st.color}28" />
            <text x="${x + 14}" y="109" fill="${st.color}" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="800">
              STAGE 0${idx + 1}
            </text>
            <text x="${x + 148}" y="110" text-anchor="end" font-size="15">${icons[idx] || '⚡'}</text>

            <!-- Stage Name -->
            <text x="${x + 83}" y="142" text-anchor="middle" fill="#ffffff" font-family="'Google Sans Display', sans-serif" font-size="13" font-weight="800">
              ${titleLine1}
            </text>
            ${titleLine2 ? `
              <text x="${x + 83}" y="158" text-anchor="middle" fill="#ffffff" font-family="'Google Sans Display', sans-serif" font-size="12.5" font-weight="800">
                ${titleLine2}
              </text>
            ` : ''}

            <!-- AI Solver Pill -->
            <rect x="${x + 12}" y="172" width="142" height="24" rx="6" fill="#090d16" stroke="${st.color}66" stroke-width="1" />
            <text x="${x + 83}" y="188" text-anchor="middle" fill="#a5b4fc" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="700">
              ✦ ${modShort}
            </text>

            <!-- Enterprise System Pill -->
            <rect x="${x + 12}" y="203" width="142" height="22" rx="6" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.12)" stroke-width="1" />
            <text x="${x + 83}" y="218" text-anchor="middle" fill="#e2e8f0" font-family="'Google Sans Text', sans-serif" font-size="10" font-weight="600">
              ${sysFirst}
            </text>

            <!-- Cycle Time Badge -->
            <rect x="${x + 28}" y="236" width="110" height="22" rx="11" fill="rgba(52,168,83,0.18)" stroke="#34a853" stroke-width="1" />
            <text x="${x + 83}" y="251" text-anchor="middle" fill="#81c995" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="800">"""

    new_vc_svg = """            <!-- Stage Node Box -->
            <rect x="${x}" y="88" width="166" height="184" rx="15"
                  fill="${isAct ? 'var(--vc-node-active)' : 'var(--vc-node-fill)'}"
                  stroke="${isAct ? 'var(--vc-node-active-stroke)' : st.color}"
                  stroke-width="${isAct ? '2.5' : '1.6'}" />
            <!-- Top Color Header Strip -->
            <rect x="${x}" y="88" width="166" height="32" rx="15" fill="${st.color}28" />
            <text x="${x + 14}" y="109" fill="${st.color}" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="800">
              STAGE 0${idx + 1}
            </text>
            <text x="${x + 148}" y="110" text-anchor="end" font-size="15">${icons[idx] || '⚡'}</text>

            <!-- Stage Name -->
            <text x="${x + 83}" y="142" text-anchor="middle" fill="var(--svg-node-text)" font-family="'Google Sans Display', sans-serif" font-size="13" font-weight="800">
              ${titleLine1}
            </text>
            ${titleLine2 ? `
              <text x="${x + 83}" y="158" text-anchor="middle" fill="var(--svg-node-text)" font-family="'Google Sans Display', sans-serif" font-size="12.5" font-weight="800">
                ${titleLine2}
              </text>
            ` : ''}

            <!-- AI Solver Pill -->
            <rect x="${x + 12}" y="172" width="142" height="24" rx="6" fill="var(--vc-pill-bg)" stroke="${st.color}66" stroke-width="1" />
            <text x="${x + 83}" y="188" text-anchor="middle" fill="var(--vc-pill-text)" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="700">
              ✦ ${modShort}
            </text>

            <!-- Enterprise System Pill -->
            <rect x="${x + 12}" y="203" width="142" height="22" rx="6" fill="var(--vc-sys-bg)" stroke="var(--vc-sys-border)" stroke-width="1" />
            <text x="${x + 83}" y="218" text-anchor="middle" fill="var(--vc-sys-text)" font-family="'Google Sans Text', sans-serif" font-size="10" font-weight="600">
              ${sysFirst}
            </text>

            <!-- Cycle Time Badge -->
            <rect x="${x + 28}" y="236" width="110" height="22" rx="11" fill="rgba(52,168,83,0.18)" stroke="#34a853" stroke-width="1" />
            <text x="${x + 83}" y="251" text-anchor="middle" fill="var(--cad-text-green)" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="800">"""
    html = must_replace(html, old_vc_svg, new_vc_svg, "value chain stage nodes")

    html = must_replace(
        html,
        """            <circle r="3.5" fill="#ffffff">
              <animateMotion dur="${1.4 + idx * 0.15}s" repeatCount="indefinite" path="M${x1},180 L${x2},180" />""",
        """            <circle r="3.5" fill="var(--svg-packet-fill)">
              <animateMotion dur="${1.4 + idx * 0.15}s" repeatCount="indefinite" path="M${x1},180 L${x2},180" />""",
        "value chain connector packet",
    )

    old_vc_ribbons = """              <defs>
                <pattern id="vcGrid_${vc.id}" width="28" height="28" patternUnits="userSpaceOnUse">
                  <path d="M 28 0 L 0 0 0 28" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="1" />
                </pattern>
              </defs>
              <rect width="1160" height="335" rx="14" fill="url(#vcGrid_${vc.id})" />

              <!-- Top 3 Synchronized Enterprise Flow Ribbons -->
              <g>
                <rect x="42" y="18" width="340" height="26" rx="13" fill="rgba(66,133,244,0.14)" stroke="#4285f4" stroke-width="1" />
                <text x="212" y="35" text-anchor="middle" fill="#93c5fd" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700">
                  FLOW 1 · PHYSICAL MATERIAL &amp; INVENTORY ──▶
                </text>

                <rect x="410" y="18" width="340" height="26" rx="13" fill="rgba(52,168,83,0.14)" stroke="#34a853" stroke-width="1" />
                <text x="580" y="35" text-anchor="middle" fill="#86efac" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700">
                  FLOW 2 · GOLDEN THREAD DATA HANDOFF ⚡ ──▶
                </text>

                <rect x="778" y="18" width="340" height="26" rx="13" fill="rgba(168,85,247,0.14)" stroke="#a855f7" stroke-width="1" />
                <text x="948" y="35" text-anchor="middle" fill="#d8b4fe" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700">
                  FLOW 3 · CLOSED-LOOP DIGITAL TWIN SYNC ◀──▶
                </text>
              </g>"""

    new_vc_ribbons = """              <defs>
                <pattern id="vcGrid_${vc.id}" width="28" height="28" patternUnits="userSpaceOnUse">
                  <path d="M 28 0 L 0 0 0 28" fill="none" stroke="var(--vc-grid-stroke)" stroke-width="1" />
                </pattern>
              </defs>
              <rect width="1160" height="335" rx="14" fill="url(#vcGrid_${vc.id})" />

              <!-- Top 3 Synchronized Enterprise Flow Ribbons -->
              <g>
                <rect x="42" y="18" width="340" height="26" rx="13" fill="rgba(66,133,244,0.14)" stroke="#4285f4" stroke-width="1" />
                <text x="212" y="35" text-anchor="middle" fill="var(--cad-text-blue)" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700">
                  FLOW 1 · PHYSICAL MATERIAL &amp; INVENTORY ──▶
                </text>

                <rect x="410" y="18" width="340" height="26" rx="13" fill="rgba(52,168,83,0.14)" stroke="#34a853" stroke-width="1" />
                <text x="580" y="35" text-anchor="middle" fill="var(--cad-text-green)" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700">
                  FLOW 2 · GOLDEN THREAD DATA HANDOFF ⚡ ──▶
                </text>

                <rect x="778" y="18" width="340" height="26" rx="13" fill="rgba(168,85,247,0.14)" stroke="#a855f7" stroke-width="1" />
                <text x="948" y="35" text-anchor="middle" fill="var(--sc-violet)" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700">
                  FLOW 3 · CLOSED-LOOP DIGITAL TWIN SYNC ◀──▶
                </text>
              </g>"""
    html = must_replace(html, old_vc_ribbons, new_vc_ribbons, "value chain top ribbons")

    html = must_replace(
        html,
        """              <rect x="420" y="299" width="320" height="22" rx="11" fill="#0b1120" stroke="${vc.color}66" stroke-width="1" />
              <text x="580" y="314" text-anchor="middle" fill="#e2e8f0" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="700">""",
        """              <rect x="420" y="299" width="320" height="22" rx="11" fill="var(--vc-node-fill)" stroke="${vc.color}88" stroke-width="1.2" />
              <text x="580" y="314" text-anchor="middle" fill="var(--vc-sys-text)" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="700">""",
        "value chain feedback pill",
    )

    # Fix dark-text-on-dark-accent active pills in Value Chain & AI Stack
    html = must_replace(
        html,
        "style=\"${other.id === vc.id ? `background:${other.color}; border-color:${other.color}; color:#040810; font-weight:700;` : ''}\"",
        "style=\"${other.id === vc.id ? `background:${other.color}; border-color:${other.color}; color:#ffffff; font-weight:700;` : ''}\"",
        "vc switcher active pill text",
    )
    html = must_replace(
        html,
        '<span style="padding:4px 12px; border-radius:8px; background:${activeStage.color || vc.color}; color:#041019; font-family:var(--font-mono); font-size:12px; font-weight:800;">',
        '<span style="padding:4px 12px; border-radius:8px; background:${activeStage.color || vc.color}; color:#ffffff; font-family:var(--font-mono); font-size:12px; font-weight:800;">',
        "vc spotlight badge text",
    )
    html = must_replace(
        html,
        "style=\"padding:5px 11px; font-size:11.5px; ${idx === currentVcSelectedStageIdx ? `background:${st.color}; color:#041019; font-weight:800; border-color:${st.color};` : ''}\"",
        "style=\"padding:5px 11px; font-size:11.5px; ${idx === currentVcSelectedStageIdx ? `background:${st.color}; color:#ffffff; font-weight:800; border-color:${st.color};` : ''}\"",
        "vc stage number pill text",
    )
    html = must_replace(
        html,
        "style=\"${currentArchVerticalFilter === 'all' ? 'background:#00d2ff; color:#040810; border-color:#00d2ff; font-weight:700;' : ''}\"",
        "style=\"${currentArchVerticalFilter === 'all' ? 'background:var(--g-blue); color:#ffffff; border-color:var(--g-blue); font-weight:700;' : ''}\"",
        "arch all filter pill",
    )
    html = must_replace(
        html,
        "style=\"${currentArchVerticalFilter === d.id ? `background:${d.color}; color:#040810; border-color:${d.color}; font-weight:700;` : ''}\"",
        "style=\"${currentArchVerticalFilter === d.id ? `background:${d.color}; color:#ffffff; border-color:${d.color}; font-weight:700;` : ''}\"",
        "arch dept filter pill",
    )

    return html


def build_standalone_variant(base_html: str, hash_target: str, boot_call: str) -> str:
    variant = must_replace(
        base_html,
        """    window.addEventListener('popstate', () => {
      handleUrlHash();
    });""",
        f"""    window.addEventListener('popstate', () => {{
      if (!window.location.hash) {{ window.location.hash = '{hash_target}'; }} handleUrlHash();
    }});""",
        f"{hash_target} popstate hook",
    )
    variant = must_replace(
        variant,
        """      hydrateAssets();
      handleUrlHash();""",
        f"""      hydrateAssets();
      handleUrlHash();
      if (!window.location.hash) {boot_call};""",
        f"{hash_target} boot hook",
    )
    return variant


def main() -> None:
    index_path = ROOT / "index.html"
    orig_html = index_path.read_text(encoding="utf-8")
    updated_index = apply_fixes(orig_html)
    index_path.write_text(updated_index, encoding="utf-8")

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

    print("Successfully updated Light Mode & hover consistency across all portal files and mirrors.")


if __name__ == "__main__":
    main()

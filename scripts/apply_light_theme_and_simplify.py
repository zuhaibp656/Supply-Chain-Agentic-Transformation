#!/usr/bin/env python3
"""Apply Dual Theme (Dark + White/Light Theme with dimmed Google Brand colors)
and strip excessive text across the Main Page, 6 Pillars, Persona Pages,
and Agent Pages in `build_site.py`.
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD_SITE = ROOT / "build_site.py"


def main():
    src = BUILD_SITE.read_text(encoding="utf-8")

    # -------------------------------------------------------------------------
    # 1. UPDATE :root CSS VARIABLES TO GOOGLE BRAND LANGUAGE & ADD LIGHT THEME
    # -------------------------------------------------------------------------
    old_root_pattern = re.compile(
        r":root\s*\{[\s\S]*?--ease-fluid:\s*cubic-bezier\(0\.16,\s*1,\s*0\.3,\s*1\);\s*\}",
        re.MULTILINE,
    )
    new_root_css = """:root, html[data-theme="dark"] {
      --bg-page: #080b12;
      --bg-surface: #0f1522;
      --bg-card: #131b2b;
      --bg-card-hover: #192338;
      --text-primary: #f1f5f9;
      --text-secondary: #cbd5e1;
      --text-muted: #94a3b8;
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-strong: rgba(255, 255, 255, 0.14);

      /* Official Google Brand Language Palette (Toned-Down, No Harsh Neon) */
      --g-blue: #4285f4;
      --g-green: #34a853;
      --g-yellow: #fbbc04;
      --g-red: #ea4335;
      --sc-cyan: #4285f4;
      --sc-emerald: #2e8b57;
      --sc-amber: #d97706;
      --sc-violet: #7e57c2;

      --font-sans: 'Google Sans Text', 'Google Sans', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-display: 'Google Sans Display', 'Google Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', 'Roboto Mono', 'SF Mono', Menlo, Consolas, monospace;
      --ease-spring: cubic-bezier(0.22, 1, 0.36, 1);
      --ease-fluid: cubic-bezier(0.16, 1, 0.3, 1);
    }

    html[data-theme="light"] {
      --bg-page: #ffffff;
      --bg-surface: #f8f9fa;
      --bg-card: #ffffff;
      --bg-card-hover: #f1f3f4;
      --text-primary: #202124;
      --text-secondary: #3c4043;
      --text-muted: #5f6368;
      --border-subtle: #e0e3e7;
      --border-strong: #cbd2d9;

      /* Dimmed Google Brand Palette for White Website */
      --g-blue: #1a73e8;
      --g-green: #1e8e3e;
      --g-yellow: #b06000;
      --g-red: #c5221f;
      --sc-cyan: #1a73e8;
      --sc-emerald: #1e8e3e;
      --sc-amber: #b06000;
      --sc-violet: #681da8;
    }"""

    assert old_root_pattern.search(src), "Could not locate :root block in build_site.py"
    src = old_root_pattern.sub(lambda _: new_root_css, src, count=1)

    # Make headings use var(--text-primary) instead of hardcoded #ffffff
    src = src.replace(
        """    h1, h2, h3, h4, .hero-title, .section-title, .persona-page-title, .agent-title, .block-title {
      text-wrap: balance;
      font-weight: 800;
      letter-spacing: -0.025em;
      color: #ffffff;
    }""",
        """    h1, h2, h3, h4, .hero-title, .section-title, .persona-page-title, .agent-title, .block-title {
      text-wrap: balance;
      font-weight: 800;
      letter-spacing: -0.025em;
      color: var(--text-primary);
    }""",
    )

    # Make highlight spans use var(--text-primary) instead of hardcoded #ffffff
    src = src.replace(
        """    .sc-hl-metric {
      color: #ffffff;
      font-weight: 700;
      font-variant-numeric: tabular-nums;
    }

    .sc-hl-underline {
      color: #f8fafc;
      font-weight: 600;
    }

    .sc-hl-bold {
      color: #ffffff;
      font-weight: 600;
    }""",
        """    .sc-hl-metric {
      color: var(--text-primary);
      font-weight: 600;
      font-variant-numeric: tabular-nums;
    }

    .sc-hl-underline {
      color: var(--text-primary);
      font-weight: 600;
    }

    .sc-hl-bold {
      color: var(--text-primary);
      font-weight: 600;
    }""",
    )

    # -------------------------------------------------------------------------
    # 2. ADD COMPREHENSIVE LIGHT THEME & SIMPLIFIED COMPONENT CSS BEFORE </style>
    # -------------------------------------------------------------------------
    light_theme_css = """
    /* =========================================================================
       SIMPLIFIED PERSONA JOURNEY & COMPACT AGENT ARCHITECTURE STYLES
       ========================================================================= */
    .journey-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-bottom: 42px;
    }

    .journey-step-row {
      display: grid;
      grid-template-columns: 240px minmax(0, 1fr) auto;
      gap: 18px;
      align-items: center;
      padding: 16px 22px;
      border-radius: 14px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      transition: border-color 0.22s ease, background 0.22s ease;
    }

    .journey-step-row:hover {
      border-color: var(--border-strong);
      background: var(--bg-card-hover);
    }

    @media (max-width: 860px) {
      .journey-step-row {
        grid-template-columns: 1fr;
        gap: 10px;
      }
    }

    .journey-step-time {
      font-family: var(--font-mono);
      font-size: 12.5px;
      font-weight: 700;
      color: var(--text-muted);
      margin-bottom: 2px;
    }

    .journey-step-title {
      font-family: var(--font-display);
      font-size: 15.5px;
      font-weight: 700;
      color: var(--text-primary);
      line-height: 1.3;
    }

    .journey-step-desc {
      font-size: 14.5px;
      color: var(--text-secondary);
      line-height: 1.55;
    }

    .journey-agent-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 14px;
      border-radius: 999px;
      background: rgba(66, 133, 244, 0.12);
      border: 1px solid rgba(66, 133, 244, 0.32);
      color: var(--g-blue);
      font-size: 13px;
      font-weight: 600;
      white-space: nowrap;
      transition: all 0.22s ease;
    }

    .journey-agent-pill:hover {
      background: var(--g-blue);
      color: #ffffff;
    }

    .showcase-emblem-box {
      width: 180px;
      height: 84px;
      flex-shrink: 0;
      border-radius: 12px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 6px;
    }

    .simple-arch-card {
      padding: 24px 28px;
      border-radius: 18px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      margin-bottom: 28px;
    }

    .simple-arch-svg-wrap {
      border-radius: 14px;
      overflow: hidden;
      border: 1px solid var(--border-subtle);
      background: var(--bg-surface);
      padding: 12px;
    }

    .video-placeholder-stage {
      width: 100%;
      min-height: 360px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 36px 24px;
      gap: 14px;
      color: var(--text-secondary);
    }

    .video-placeholder-icon {
      width: 64px;
      height: 64px;
      border-radius: 50%;
      background: rgba(66, 133, 244, 0.12);
      border: 1px solid rgba(66, 133, 244, 0.35);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--g-blue);
      font-size: 24px;
    }

    .theme-toggle-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 14px;
      border-radius: 999px;
      border: 1px solid var(--border-strong) !important;
      background: var(--bg-surface) !important;
      color: var(--text-primary) !important;
      font-weight: 600 !important;
      font-size: 13px !important;
    }

    .theme-toggle-btn:hover {
      border-color: var(--g-blue) !important;
    }

    /* =========================================================================
       TONED-DOWN DARK THEME REFINEMENTS (LESS NEON, MORE GOOGLE BRAND)
       ========================================================================= */
    .cfo-box {
      border: 1.5px solid rgba(66, 133, 244, 0.45);
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.35);
    }

    .dept-node {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.28);
    }

    .dept-node:hover,
    .dept-node.active {
      background: var(--bg-card-hover);
      border-color: var(--dept-accent, var(--g-blue));
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.36);
    }

    .dept-anim-stage svg.dept-stage-svg {
      opacity: 0.84;
      filter: saturate(0.88);
    }

    .dept-node:hover .dept-anim-stage svg.dept-stage-svg,
    .dept-node.active .dept-anim-stage svg.dept-stage-svg {
      opacity: 0.96;
      filter: saturate(1.0);
    }

    /* =========================================================================
       LIGHT THEME OVERRIDES (WHITE BACKGROUND, DIMMED GOOGLE BRAND COLORS)
       ========================================================================= */
    html[data-theme="light"],
    html[data-theme="light"] body {
      background: #ffffff;
      color: #202124;
    }

    html[data-theme="light"] .navbar {
      background: rgba(255, 255, 255, 0.95);
      border-bottom: 1px solid #dadce0;
      box-shadow: 0 1px 4px rgba(60, 64, 67, 0.06);
    }

    html[data-theme="light"] .nav-brand img.gemini-logo,
    html[data-theme="light"] .hero-logo-lockup img.gemini-hero {
      filter: invert(1) hue-rotate(180deg);
    }

    html[data-theme="light"] .nav-csco-badge {
      background: #f1f3f4;
      border-color: #dadce0;
      color: #3c4043;
    }

    html[data-theme="light"] .nav-pill-btn {
      color: #3c4043;
    }

    html[data-theme="light"] .nav-pill-btn:hover {
      background: #f1f3f4;
      color: #1a73e8;
    }

    html[data-theme="light"] .hero-section {
      background: #ffffff;
      border-bottom: 1px solid #e0e3e7;
    }

    html[data-theme="light"] .hero-aurora-backdrop {
      background:
        radial-gradient(circle 520px at 16% 26%, rgba(66, 133, 244, 0.06), transparent 72%),
        radial-gradient(circle 560px at 84% 32%, rgba(52, 168, 83, 0.05), transparent 72%),
        radial-gradient(circle 480px at 22% 76%, rgba(251, 188, 4, 0.05), transparent 70%),
        radial-gradient(circle 520px at 82% 78%, rgba(234, 67, 53, 0.05), transparent 72%);
    }

    html[data-theme="light"] .hero-vignette {
      background:
        radial-gradient(ellipse 36% 42% at 50% 48%, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.72) 56%, rgba(255, 255, 255, 0.0) 100%),
        linear-gradient(180deg, rgba(255, 255, 255, 0.4) 0%, rgba(255, 255, 255, 0.05) 50%, rgba(255, 255, 255, 0.95) 100%);
    }

    html[data-theme="light"] .hero-logo-lockup {
      background: #f8f9fa;
      border: 1px solid #dadce0;
      box-shadow: 0 2px 10px rgba(60, 64, 67, 0.07);
    }

    html[data-theme="light"] .hero-title {
      color: #202124;
      text-shadow: none;
    }

    html[data-theme="light"] .hero-title .gradient-word {
      background: linear-gradient(92deg, #1a73e8 0%, #1e8e3e 52%, #b06000 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    html[data-theme="light"] .hero-subtitle {
      color: #5f6368;
      text-shadow: none;
    }

    html[data-theme="light"] .hero-cta-btn {
      background: #1a73e8;
      color: #ffffff;
      box-shadow: 0 4px 12px rgba(26, 115, 232, 0.22);
    }

    html[data-theme="light"] .hero-cta-btn.secondary-hero-btn {
      background: #f8f9fa !important;
      color: #3c4043 !important;
      border: 1px solid #dadce0 !important;
      box-shadow: 0 1px 4px rgba(60, 64, 67, 0.06) !important;
    }

    html[data-theme="light"] .four-color-bar {
      box-shadow: none;
    }

    html[data-theme="light"] .section-title,
    html[data-theme="light"] .cfo-box-title,
    html[data-theme="light"] .dept-node-title,
    html[data-theme="light"] .showcase-dept-name,
    html[data-theme="light"] .persona-link-name,
    html[data-theme="light"] .persona-page-title,
    html[data-theme="light"] .agent-title,
    html[data-theme="light"] .block-title,
    html[data-theme="light"] .catalog-title {
      color: #202124 !important;
    }

    html[data-theme="light"] .section-subtitle,
    html[data-theme="light"] .cfo-box-sub,
    html[data-theme="light"] .dept-node-sub,
    html[data-theme="light"] .showcase-visual-desc,
    html[data-theme="light"] .persona-link-role,
    html[data-theme="light"] .persona-page-summary,
    html[data-theme="light"] .agent-subtitle,
    html[data-theme="light"] .block-subtitle,
    html[data-theme="light"] .catalog-desc {
      color: #5f6368 !important;
    }

    html[data-theme="light"] .vertical-tabs-nav-bar {
      background: rgba(248, 249, 250, 0.96);
      border: 1px solid #dadce0;
      box-shadow: 0 4px 14px rgba(60, 64, 67, 0.07);
    }

    html[data-theme="light"] .v-tab-btn {
      background: #ffffff;
      color: #5f6368;
      border: 1px solid #e0e3e7;
    }

    html[data-theme="light"] .v-tab-btn .v-tab-title {
      color: #202124;
    }

    html[data-theme="light"] .v-tab-btn:hover {
      background: #f1f3f4;
      border-color: #bdc1c6;
      box-shadow: 0 2px 8px rgba(60, 64, 67, 0.08);
    }

    html[data-theme="light"] .v-tab-btn.active {
      background: #e8f0fe;
      border-color: var(--v-accent, #1a73e8);
      box-shadow: 0 2px 8px rgba(26, 115, 232, 0.12);
    }

    html[data-theme="light"] .v-tab-btn.active .v-tab-tag {
      color: #3c4043;
    }

    html[data-theme="light"] .cfo-box {
      background: #f8f9fa;
      border: 1.5px solid #dadce0;
      box-shadow: 0 4px 14px rgba(60, 64, 67, 0.07);
    }

    html[data-theme="light"] .cfo-sc-emblem {
      background: #ffffff;
      border: 1px solid #e0e3e7;
    }

    html[data-theme="light"] .dept-node {
      background: #ffffff;
      border: 1px solid #dadce0;
      box-shadow: 0 2px 8px rgba(60, 64, 67, 0.06);
    }

    html[data-theme="light"] .dept-node:hover,
    html[data-theme="light"] .dept-node.active {
      background: #f8f9fa;
      border-color: var(--dept-accent, #1a73e8);
      box-shadow: 0 6px 20px rgba(60, 64, 67, 0.11);
    }

    html[data-theme="light"] .dept-anim-stage {
      background: #f8f9fa;
      border: 1px solid #e8eaed;
    }

    html[data-theme="light"] .dept-node:hover .dept-anim-stage,
    html[data-theme="light"] .dept-node.active .dept-anim-stage {
      background: #f1f3f4;
      border-color: #dadce0;
    }

    html[data-theme="light"] .dept-anim-stage svg.dept-stage-svg {
      opacity: 0.78;
      filter: saturate(0.72) contrast(0.92);
    }

    html[data-theme="light"] .dept-node:hover .dept-anim-stage svg.dept-stage-svg,
    html[data-theme="light"] .dept-node.active .dept-anim-stage svg.dept-stage-svg {
      opacity: 0.92;
      filter: saturate(0.85) contrast(0.96);
    }

    html[data-theme="light"] .dept-anim-meta {
      background: rgba(255, 255, 255, 0.92);
      color: #3c4043;
      border: 1px solid #dadce0;
    }

    html[data-theme="light"] .dept-showcase-box {
      background: #f8f9fa;
      border: 1px solid #dadce0;
      box-shadow: 0 8px 24px rgba(60, 64, 67, 0.09);
    }

    html[data-theme="light"] .showcase-visual-strip {
      background: #ffffff;
      border: 1px solid #e0e3e7;
    }

    html[data-theme="light"] .persona-link-card {
      background: #ffffff;
      border: 1px solid #dadce0;
      box-shadow: 0 1px 3px rgba(60, 64, 67, 0.05);
    }

    html[data-theme="light"] .persona-link-card:hover {
      background: #f1f3f4;
      border-color: var(--dept-accent, #1a73e8);
      box-shadow: 0 4px 12px rgba(60, 64, 67, 0.09);
    }

    html[data-theme="light"] .persona-emoji {
      background: #f8f9fa;
      border: 1px solid #e0e3e7;
    }

    html[data-theme="light"] .persona-header-card,
    html[data-theme="light"] .agent-hero-banner {
      background: #f8f9fa;
      border: 1px solid #dadce0;
      box-shadow: 0 4px 14px rgba(60, 64, 67, 0.06);
    }

    html[data-theme="light"] .persona-header-sc-watermark {
      opacity: 0.14;
      filter: saturate(0.65);
    }

    html[data-theme="light"] .catalog-card,
    html[data-theme="light"] .dir-persona-card {
      background: #ffffff;
      border: 1px solid #dadce0;
      box-shadow: 0 2px 8px rgba(60, 64, 67, 0.06);
    }

    html[data-theme="light"] .catalog-card:hover,
    html[data-theme="light"] .dir-persona-card:hover {
      background: #f8f9fa;
      border-color: #bdc1c6;
      box-shadow: 0 6px 18px rgba(60, 64, 67, 0.11);
    }

    html[data-theme="light"] .catalog-thumb {
      background: #f1f3f4;
      border-bottom: 1px solid #e0e3e7;
    }

    html[data-theme="light"] .play-circle {
      background: #ffffff;
      color: #1a73e8;
      border: 1px solid #dadce0;
    }

    html[data-theme="light"] .video-stage-box {
      background: #f8f9fa;
      border: 1px solid #dadce0;
      box-shadow: 0 4px 16px rgba(60, 64, 67, 0.08);
    }

    html[data-theme="light"] .video-viewport {
      background: #f1f3f4;
    }

    html[data-theme="light"] .upload-video-btn {
      background: #ffffff;
      color: #3c4043;
      border: 1px solid #dadce0;
    }

    html[data-theme="light"] .upload-video-btn:hover,
    html[data-theme="light"] .upload-video-btn.active {
      background: #1a73e8;
      color: #ffffff;
      border-color: #1a73e8;
    }

    html[data-theme="light"] .dir-search-input {
      background: #ffffff;
      border: 1px solid #dadce0;
      color: #202124;
    }

    html[data-theme="light"] .dir-agent-launch-row {
      background: #f8f9fa;
      border: 1px solid #e0e3e7;
    }

    html[data-theme="light"] .dir-agent-launch-row:hover {
      background: #e8f0fe;
      border-color: #1a73e8;
    }

    html[data-theme="light"] .pt-tile {
      background: #ffffff;
      border: 1px solid #dadce0;
      border-top: 3px solid var(--tile-color, #1a73e8);
      box-shadow: 0 1px 4px rgba(60, 64, 67, 0.05);
    }

    html[data-theme="light"] .pt-tile-title {
      color: #202124;
    }

    html[data-theme="light"] .pt-tile:hover,
    html[data-theme="light"] .pt-tile.active {
      background: #f8f9fa;
      box-shadow: 0 4px 12px rgba(60, 64, 67, 0.12);
    }

    html[data-theme="light"] .pt-side-card,
    html[data-theme="light"] .pt-legend-box,
    html[data-theme="light"] .pt-inline-expand,
    html[data-theme="light"] .mm-col-card,
    html[data-theme="light"] .mm-flow-card {
      background: #f8f9fa;
      border: 1px solid #dadce0;
      box-shadow: 0 2px 10px rgba(60, 64, 67, 0.06);
      color: #202124;
    }

    html[data-theme="light"] .mm-node-btn {
      background: #ffffff;
      border: 1px solid #dadce0;
      border-left: 3.5px solid var(--node-color, #1a73e8);
    }

    html[data-theme="light"] .mm-node-btn:hover,
    html[data-theme="light"] .mm-node-btn.active {
      background: #e8f0fe;
    }

    html[data-theme="light"] .global-authors-footer {
      background: #f8f9fa;
      border: 1px solid #dadce0;
      box-shadow: 0 2px 8px rgba(60, 64, 67, 0.05);
    }

    html[data-theme="light"] .authors-credit-pill {
      background: #e8f0fe;
      border: 1px solid #d2e3fc;
      color: #1967d2;
      box-shadow: none;
    }

    html[data-theme="light"] .authors-credit-pill strong {
      color: #174ea6;
      text-decoration-color: rgba(23, 78, 166, 0.4);
    }
"""

    src = src.replace("  </style>", light_theme_css + "\n  </style>", 1)

    # -------------------------------------------------------------------------
    # 3. UPDATE NAVBAR & HERO SECTION (CLEAN BUTTONS + THEME TOGGLE)
    # -------------------------------------------------------------------------
    old_nav_pattern = re.compile(
        r'<header class="navbar">[\s\S]*?</header>',
        re.MULTILINE,
    )
    new_navbar_html = """<header class="navbar">
    <div class="nav-brand" onclick="goHome()">
      <img data-asset="gemini_enterprise_dark.png" alt="Gemini Enterprise" class="gemini-logo" />
      <div class="nav-divider"></div>
      <span class="nav-csco-badge">Office of the CSCO · Supply Chain</span>
    </div>

    <div class="nav-right">
      <button type="button" class="nav-pill-btn" onclick="goHome()">Home</button>
      <button type="button" class="nav-pill-btn" onclick="goToOrgChart()">6 SCOR Pillars</button>
      <button type="button" class="nav-pill-btn" onclick="openPersonasDirectoryPage('all', '', true, 'personas')">Personas (29)</button>
      <button type="button" class="nav-pill-btn" onclick="openPersonasDirectoryPage('all', '', true, 'agents')">Agents (35)</button>
      <button type="button" class="nav-pill-btn" onclick="openPeriodicTablePage('all', null, true)">Periodic Table</button>
      <button type="button" class="nav-pill-btn" onclick="openMindMapPage('all', null, true)">Mind Map</button>
      <button type="button" id="themeToggleBtn" class="nav-pill-btn theme-toggle-btn" onclick="togglePortalTheme()" title="Switch between Light and Dark Theme">
        <span id="themeToggleIcon">☀️</span>
        <span id="themeToggleLabel">Light Theme</span>
      </button>
    </div>
  </header>"""
    assert old_nav_pattern.search(src), "Could not locate <header class=\"navbar\">"
    src = old_nav_pattern.sub(lambda _: new_navbar_html, src, count=1)

    # Simplify Hero CTA buttons & 4-color Google bar
    old_hero_content_pattern = re.compile(
        r'<div class="hero-content">[\s\S]*?</div>\s*</section>',
        re.MULTILINE,
    )
    new_hero_content_html = """<div class="hero-content">
        <div class="hero-logo-lockup">
          <img data-asset="gemini_enterprise_dark.png" alt="Gemini Enterprise" class="gemini-hero" />
        </div>

        <h1 class="hero-title" style="margin-bottom: 32px;">
          Agentic Transformation for <span class="gradient-word">Supply Chain &amp; Demand</span>
        </h1>

        <div style="display:flex; flex-wrap:wrap; justify-content:center; gap:12px;">
          <button type="button" class="hero-cta-btn" onclick="goToOrgChart()">
            <span>Explore 6 SCOR Pillars</span>
            <span>&darr;</span>
          </button>
          <button type="button" class="hero-cta-btn secondary-hero-btn" style="background:rgba(19,27,43,0.9); color:#f1f5f9; border:1px solid rgba(255,255,255,0.16);" onclick="openPersonasDirectoryPage('all', '', true, 'agents')">
            <span>Browse Personas &amp; Agents &rarr;</span>
          </button>
        </div>

        <div class="four-color-bar" style="width:160px;">
          <span style="background:var(--g-blue);"></span>
          <span style="background:var(--g-red);"></span>
          <span style="background:var(--g-yellow);"></span>
          <span style="background:var(--g-green);"></span>
        </div>
      </div>
    </section>"""
    assert old_hero_content_pattern.search(src), "Could not locate .hero-content"
    src = old_hero_content_pattern.sub(lambda _: new_hero_content_html, src, count=1)

    # -------------------------------------------------------------------------
    # 4. SIMPLIFY #orgChartSection ON MAIN PAGE (REMOVE RIVERS BANNER, UNIVERSAL
    #    BANNER, AND VALUE CHAIN BLOCK SO ONLY 6 PILLARS + DRAWER REMAIN)
    # -------------------------------------------------------------------------
    old_org_section_pattern = re.compile(
        r'<section id="orgChartSection" class="org-section">[\s\S]*?</section>\s*</main>',
        re.MULTILINE,
    )
    new_org_section_html = """<section id="orgChartSection" class="org-section">
      <div class="section-header" style="margin-bottom: 32px;">
        <h2 class="section-title">Office of the CSCO — The 6 ASCM SCOR Pillars</h2>
        <p class="section-subtitle">Select any pillar below to view what it means and explore its supply chain personas.</p>
      </div>

      <!-- 6-Pillar Interactive Master Navigation Tab Bar -->
      <div class="vertical-tabs-nav-bar" id="verticalTabsNavBar">
        <button type="button" class="v-tab-btn active" data-vtab="all" onclick="switchVerticalTab('all', this)">
          <span class="v-tab-num" style="color:var(--g-blue);">ALL 6</span>
          <span class="v-tab-title">All 6 Pillars</span>
          <span class="v-tab-tag">SCOR End-to-End</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="demand_sop" onclick="switchVerticalTab('demand_sop', this)" style="--v-accent: #2e8b57;">
          <span class="v-tab-num">01 · PLAN</span>
          <span class="v-tab-title">Demand &amp; S&amp;OP</span>
          <span class="v-tab-tag">4 Personas</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="sourcing_procurement" onclick="switchVerticalTab('sourcing_procurement', this)" style="--v-accent: #7e57c2;">
          <span class="v-tab-num">02 · SOURCE</span>
          <span class="v-tab-title">Sourcing &amp; Procurement</span>
          <span class="v-tab-tag">4 Personas</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="manufacturing_prod" onclick="switchVerticalTab('manufacturing_prod', this)" style="--v-accent: #3b78e7;">
          <span class="v-tab-num">03 · MAKE</span>
          <span class="v-tab-title">Manufacturing &amp; MPS</span>
          <span class="v-tab-tag">4 Personas</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="inventory_warehouse" onclick="switchVerticalTab('inventory_warehouse', this)" style="--v-accent: #00897b;">
          <span class="v-tab-num">04 · FULFILL</span>
          <span class="v-tab-title">Inventory &amp; Warehousing</span>
          <span class="v-tab-tag">5 Personas</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="logistics_fleet" onclick="switchVerticalTab('logistics_fleet', this)" style="--v-accent: #d97706;">
          <span class="v-tab-num">05 · DELIVER</span>
          <span class="v-tab-title">Logistics &amp; Distribution</span>
          <span class="v-tab-tag">9 Personas</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="circular_enable" onclick="switchVerticalTab('circular_enable', this)" style="--v-accent: #c53929;">
          <span class="v-tab-num">06 · RETURN &amp; ENABLE</span>
          <span class="v-tab-title">OTIF, Returns &amp; ESG</span>
          <span class="v-tab-tag">3 Personas</span>
        </button>
      </div>

      <div class="cfo-root-wrapper">
        <div class="cfo-box">
          <div class="cfo-sc-emblem" aria-hidden="true">
            <svg viewBox="0 0 84 64" style="width:100%;height:100%;">
              <polygon points="8,42 42,24 76,42 42,58" fill="rgba(66,133,244,0.10)" stroke="#4285f4" stroke-width="1.3" />
              <line x1="18" y1="37" x2="66" y2="37" stroke="#4285f4" stroke-width="1" stroke-dasharray="4 3" class="sc-arc-flow" />
              <g class="sc-conveyor-box-anim" style="animation-duration:2.6s;">
                <polygon points="16,30 26,25 36,30 26,35" fill="#4285f4" />
                <polygon points="16,30 26,35 26,44 16,39" fill="#1a73e8" />
                <polygon points="36,30 26,35 26,44 36,39" fill="#174ea6" />
              </g>
              <circle cx="42" cy="16" r="7" fill="none" stroke="#34a853" stroke-width="1.4" stroke-dasharray="4 2" class="sc-arc-flow" />
              <circle cx="42" cy="16" r="2.8" fill="#fbbc04" class="sc-node-pulse" />
            </svg>
          </div>
          <div>
            <div class="cfo-box-title">Chief Supply Chain Officer (CSCO)</div>
            <div class="cfo-box-sub">6 ASCM SCOR Pillars · 29 Personas · 35 AI Agents</div>
          </div>
        </div>

        <!-- SVG Tree Lines to 6 Supply Chain Pillars (3x2 Grid) -->
        <svg class="org-connectors" viewBox="0 0 1000 56" preserveAspectRatio="none">
          <defs>
            <linearGradient id="orgLineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#34a853" stop-opacity="0.55" />
              <stop offset="35%" stop-color="#4285f4" stop-opacity="0.65" />
              <stop offset="70%" stop-color="#fbbc04" stop-opacity="0.65" />
              <stop offset="100%" stop-color="#ea4335" stop-opacity="0.55" />
            </linearGradient>
          </defs>
          <path d="M500,0 L500,24 M166,24 L834,24 M166,24 L166,56 M500,24 L500,56 M834,24 L834,56" stroke="var(--border-strong)" stroke-width="1.5" fill="none" />
          <path d="M500,0 L500,24 M166,24 L834,24 M166,24 L166,56 M500,24 L500,56 M834,24 L834,56"
                stroke="url(#orgLineGrad)" stroke-width="2" stroke-dasharray="8 10" fill="none"
                style="animation: scDashFlow 2.4s linear infinite;" />
          <circle r="3" fill="#34a853">
            <animateMotion dur="2.4s" repeatCount="indefinite" path="M500,0 L500,24 L166,24 L166,56" />
          </circle>
          <circle r="3" fill="#4285f4">
            <animateMotion dur="2.0s" repeatCount="indefinite" path="M500,0 L500,24 L500,56" />
          </circle>
          <circle r="3" fill="#ea4335">
            <animateMotion dur="2.6s" repeatCount="indefinite" path="M500,0 L500,24 L834,24 L834,56" />
          </circle>
        </svg>

        <!-- 6 Clean Supply Chain Pillar Boxes -->
        <div id="deptRowContainer" class="dept-row"></div>
      </div>

      <!-- Progressive Pillar Drawer (What This Pillar Means + Personas Only) -->
      <div id="deptShowcaseContainer"></div>
    </section>

  </main>"""
    assert old_org_section_pattern.search(src), "Could not locate #orgChartSection"
    src = old_org_section_pattern.sub(lambda _: new_org_section_html, src, count=1)

    # -------------------------------------------------------------------------
    # 5. REPLACE formatRichText / formatRichBullets & ADD shortSentence + THEME CONTROLLER
    # -------------------------------------------------------------------------
    old_rich_text_pattern = re.compile(
        r"function formatRichText\(raw\)\s*\{[\s\S]*?function renderUniversalAgentsHomeBanner\(\)",
        re.MULTILINE,
    )
    new_rich_text_js = """function shortSentence(raw, maxLen = 140) {
      if (!raw) return '';
      let s = String(raw).replace(/\\s+/g, ' ').trim();
      // Remove parenthetical technical bloat for cleaner executive reading
      s = s.replace(/\\s*\\([^)]{18,}\\)\\s*/g, ' ').replace(/\\s+/g, ' ').trim();
      const firstSplit = s.split(/(?:\\.\\s+|\\s+—\\s+|\\s+;\\s+)/)[0].trim();
      let out = firstSplit || s;
      if (out.length > maxLen) {
        out = out.slice(0, maxLen - 1).replace(/[,;:\\s]+$/, '') + '…';
      }
      if (!/[.!?…]$/.test(out)) out += '.';
      return out;
    }

    function formatRichText(raw) {
      if (!raw) return '';
      return String(raw).replace(/\\s+/g, ' ').trim();
    }

    function formatRichBullets(raw, bulletColor = '#4285f4') {
      if (!raw) return '';
      return `<p style="margin:0;">${shortSentence(raw, 165)}</p>`;
    }

    /* Theme Controller (Dark Theme & Light Theme with Google Brand Colors) */
    function applyPortalTheme(theme) {
      const validTheme = theme === 'light' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', validTheme);
      const iconEl = document.getElementById('themeToggleIcon');
      const labelEl = document.getElementById('themeToggleLabel');
      if (iconEl && labelEl) {
        if (validTheme === 'light') {
          iconEl.textContent = '🌙';
          labelEl.textContent = 'Dark Theme';
        } else {
          iconEl.textContent = '☀️';
          labelEl.textContent = 'Light Theme';
        }
      }
      try {
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
    }

    function renderUniversalAgentsHomeBanner()"""
    assert old_rich_text_pattern.search(src), "Could not locate formatRichText block"
    src = old_rich_text_pattern.sub(lambda _: new_rich_text_js, src, count=1)

    # -------------------------------------------------------------------------
    # 6. SIMPLIFY renderOrgChart() CARD TEXT
    # -------------------------------------------------------------------------
    old_render_org_pattern = re.compile(
        r"function renderOrgChart\(\)\s*\{[\s\S]*?renderValueChainEntryCards\(\);\s*\}",
        re.MULTILINE,
    )
    new_render_org_js = """function renderOrgChart() {
      const row = document.getElementById('deptRowContainer');
      if (!row) return;
      row.innerHTML = Object.values(DEPARTMENTS).map(dept => {
        const isActive = dept.id === selectedDeptId;
        const domainAgentCount = Object.values(AGENTS).filter(a => !a.isUniversal && a.deptId === dept.id).length;
        return `
          <div class="dept-node ${isActive ? 'active' : ''}"
               data-dept-id="${dept.id}"
               style="--dept-accent: ${dept.color};"
               onclick="selectDepartment('${dept.id}', event)">
            <div style="position:relative; z-index:2;">
              <div style="display:inline-flex; align-items:center; gap:6px; padding:4px 11px; border-radius:999px; font-size:11px; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; background:${dept.color}18; color:${dept.color}; border:1px solid ${dept.color}40; margin-bottom:10px;">
                <span>${dept.scorBadge || 'SCOR PILLAR'}</span>
              </div>
              <div class="dept-node-title">${dept.name}</div>
              <div class="dept-node-sub">${shortSentence(dept.subtitle, 110)}</div>
            </div>
            <div class="dept-anim-stage">
              ${renderSupplyChainWatermarkSvg(dept.watermarkType, dept.color, 'dept-stage-svg')}
              <span class="dept-anim-meta">${dept.personaIds.length} Personas · ${domainAgentCount} Agents</span>
            </div>
          </div>
        `;
      }).join('');

      renderDepartmentShowcaseBox();
    }"""
    assert old_render_org_pattern.search(src), "Could not locate renderOrgChart()"
    src = old_render_org_pattern.sub(lambda _: new_render_org_js, src, count=1)

    # -------------------------------------------------------------------------
    # 7. SIMPLIFY renderDepartmentShowcaseBox() (ONLY WHAT PILLAR MEANS + PERSONAS)
    # -------------------------------------------------------------------------
    old_showcase_pattern = re.compile(
        r"function renderDepartmentShowcaseBox\(\)\s*\{[\s\S]*?/\*\s*=========================================================================\s*EXECUTIVE SELLING METADATA HELPER",
        re.MULTILINE,
    )
    new_showcase_js = """function renderDepartmentShowcaseBox() {
      const container = document.getElementById('deptShowcaseContainer');
      if (!container) return;
      if (!selectedDeptId || !DEPARTMENTS[selectedDeptId]) {
        container.innerHTML = '';
        return;
      }
      const dept = DEPARTMENTS[selectedDeptId];

      container.innerHTML = `
        <div id="deptShowcaseBoxEl" class="dept-showcase-box genie-enter" style="--dept-accent: ${dept.color};">
          <div class="showcase-header">
            <div class="showcase-dept-name">
              <span class="accent-dot" style="background: ${dept.color};"></span>
              <span>${dept.scorBadge || ''} · ${dept.name}</span>
            </div>
            <button type="button" class="switch-pill" onclick="selectDepartment('${dept.id}')">
              ✕ Close
            </button>
          </div>

          <!-- What This Pillar Means -->
          <div class="showcase-visual-strip">
            <div class="showcase-emblem-box">
              ${renderSupplyChainWatermarkSvg(dept.watermarkType, dept.color, 'dept-stage-svg')}
            </div>
            <div class="showcase-visual-meta">
              <div class="showcase-visual-title" style="color:${dept.color};">
                What This Pillar Means
              </div>
              <div class="showcase-visual-desc">
                ${shortSentence(dept.subtitle, 165)}
              </div>
            </div>
          </div>

          <!-- Personas in this Pillar -->
          <div style="margin-top: 20px;">
            <div style="font-size:15px; font-weight:700; color:var(--text-primary); margin-bottom:14px; display:flex; align-items:center; gap:8px;">
              <span class="accent-dot" style="background:${dept.color};"></span>
              <span>Personas (${dept.personaIds.length})</span>
            </div>

            <div class="dept-personas-list" style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:12px;">
              ${dept.personaIds.map(pid => {
                const p = PERSONAS[pid];
                if (!p) return '';
                return `
                  <div class="persona-link-card" onclick="openPersonaPage('${p.id}', true, event)">
                    <div class="persona-link-left">
                      <div class="persona-emoji">${p.icon}</div>
                      <div>
                        <div class="persona-link-name">${p.name}</div>
                        <div class="persona-link-role">${p.role}</div>
                      </div>
                    </div>
                    <span class="persona-open-arrow" style="color:${dept.color};">&rarr;</span>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        </div>
      `;
    }

    /* =========================================================================
       EXECUTIVE SELLING METADATA HELPER"""
    assert old_showcase_pattern.search(src), "Could not locate renderDepartmentShowcaseBox()"
    src = old_showcase_pattern.sub(lambda _: new_showcase_js, src, count=1)

    # -------------------------------------------------------------------------
    # 8. SIMPLIFY openPersonaPage() (HEADER + CLEAN JOURNEY + AGENTS ONLY)
    # -------------------------------------------------------------------------
    old_persona_pattern = re.compile(
        r"function openPersonaPage\(personaId,\s*pushHash\s*=\s*true,\s*ev\s*=\s*null\)\s*\{[\s\S]*?/\*\s*=========================================================================\s*AGENT ARCHITECTURE BLUEPRINT HELPER",
        re.MULTILINE,
    )
    new_persona_js = """function openPersonaPage(personaId, pushHash = true, ev = null) {
      const p = PERSONAS[personaId];
      if (!p) return;
      const useSlide = isPillOrNavSwitch(ev);
      const sRect = useSlide ? null : getClickedCardRect(ev);
      const transClass = getPageTransitionClass(ev, sRect);

      lastPersonaId = personaId;
      selectedDeptId = p.deptId;
      const dept = getDeptMeta(p.deptId);

      if (pushHash) {
        history.pushState({ page: 'persona', id: personaId }, '', `#persona/${personaId}`);
      }

      const container = document.getElementById('personaPageContent');
      container.innerHTML = `
        <div id="personaGenieWrap" class="${transClass}">
          <!-- Top Back & Switcher Bar -->
          <div class="back-bar">
            <button type="button" class="back-btn" onclick="goToOrgChart()">
              <span>&larr;</span>
              <span>Back to 6 Pillars (${dept.name})</span>
            </button>

            <div class="persona-switcher-pills">
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
            </div>
          </div>

          <!-- Simple Persona Overview Header -->
          <div class="persona-header-card" style="grid-template-columns: 1fr; padding: 30px 34px; margin-bottom: 28px;">
            ${renderSupplyChainWatermarkSvg(dept.watermarkType, dept.color, 'persona-header-sc-watermark')}

            <div style="position:relative; z-index:2;">
              <div class="persona-badge" style="background: ${dept.color}18; color: ${dept.color}; border: 1px solid ${dept.color}40;">
                <span>${p.icon}</span>
                <span>${dept.scorBadge || ''} · ${dept.name} · ${p.role}</span>
              </div>
              <h1 class="persona-page-title">${p.name}</h1>
              <p class="persona-page-summary">${shortSentence(p.summary, 160)}</p>
            </div>
          </div>

          <!-- Simple, Scannable Persona Journey -->
          <div style="margin-bottom: 14px;">
            <h2 class="block-title" style="border-left-color: ${dept.color};">Persona Journey</h2>
            <p class="block-subtitle">Key daily workflow steps and where AI agents assist.</p>
          </div>

          <div class="journey-list">
            ${p.dayInLife.map(slot => {
              const plugAgent = slot.agentId ? AGENTS[slot.agentId] : null;
              const desc = shortSentence(slot.isToil ? slot.after : slot.activity, 125);
              return `
                <div class="journey-step-row">
                  <div>
                    <div class="journey-step-time">${slot.time}</div>
                    <div class="journey-step-title">${slot.task}</div>
                  </div>
                  <div class="journey-step-desc">${desc}</div>
                  <div>
                    ${plugAgent ? `
                      <button type="button" class="journey-agent-pill" onclick="openAgentPage('${plugAgent.id}', true, event)">
                        <span>🤖 ${plugAgent.name}</span>
                        <span>&rarr;</span>
                      </button>
                    ` : `<span style="font-size:12.5px; color:var(--text-muted);">👤 ${slot.tag || 'Core Task'}</span>`}
                  </div>
                </div>
              `;
            }).join('')}
          </div>

          <!-- Clean Agent Catalogue for this Persona -->
          <div style="margin-bottom: 16px;">
            <h2 class="block-title" style="border-left-color: ${dept.color};">AI Agents for ${p.name}</h2>
          </div>

          <div class="catalog-grid">
            ${[...new Set([...(p.agentIds || []), ...UNIVERSAL_AGENT_IDS])].map(aid => {
              const ag = AGENTS[aid];
              if (!ag) return '';
              const agDept = getDeptMeta(ag.deptId);
              return `
                <div class="catalog-card" onclick="openAgentPage('${ag.id}', true, event)">
                  <div class="catalog-thumb" style="height: 136px;">
                    ${renderMiniCatalogCadSvg(ag.cadType, agDept.color)}
                  </div>
                  <div class="catalog-body" style="padding: 20px;">
                    <div>
                      <div style="font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:${agDept.color}; margin-bottom:6px;">
                        ${ag.isUniversal ? 'Universal Core Agent' : `${dept.name} Agent`}
                      </div>
                      <div class="catalog-title" style="font-size:18.5px;">${ag.name}</div>
                      <div class="catalog-desc" style="font-size:14.5px;">${shortSentence(ag.shortDesc, 115)}</div>
                    </div>
                    <div class="catalog-footer" style="margin-top:12px; padding-top:12px;">
                      <span style="color: ${agDept.color}; font-size:13.5px;">Open Agent</span>
                      <span>&rarr;</span>
                    </div>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>
      `;

      hydrateAssets();
      showActivePage('pagePersona');
      const wrap = document.getElementById('personaGenieWrap');
      if (sRect && wrap) {
        animateGenieOutOfBox(sRect, wrap, dept.color);
      }
    }

    /* =========================================================================
       AGENT ARCHITECTURE BLUEPRINT HELPER"""
    assert old_persona_pattern.search(src), "Could not locate openPersonaPage()"
    src = old_persona_pattern.sub(lambda _: new_persona_js, src, count=1)

    # -------------------------------------------------------------------------
    # 9. SIMPLIFY openAgentPage() (ONLY: 1. WHAT AGENT DOES, 2. SMALL ARCH
    #    DIAGRAM, 3. BOX FOR A VIDEO)
    # -------------------------------------------------------------------------
    old_agent_pattern = re.compile(
        r"function openAgentPage\(agentId,\s*pushHash\s*=\s*true,\s*ev\s*=\s*null\)\s*\{[\s\S]*?function attachAgentVideo\(event,\s*agentId\)\s*\{[\s\S]*?\}",
        re.MULTILINE,
    )
    new_agent_js = """function renderSimpleAgentArchitectureDiagram(ag, dept) {
      const sysArr = toSysArray(ag.systems);
      const trunc = (str, max = 22) => {
        const s = String(str || '').trim();
        return s.length > max ? s.slice(0, max - 1) + '…' : s;
      };
      const s1 = trunc(sysArr[0] || 'Enterprise ERP', 22);
      const s2 = trunc(sysArr[1] || 'WMS / TMS Feeds', 22);
      const agentShort = trunc(ag.name, 22);

      return `
        <div class="simple-arch-card">
          <div style="font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:4px;">
            Architecture Overview
          </div>
          <h2 style="font-family:var(--font-display); font-size:20px; font-weight:800; color:var(--text-primary); margin-bottom:14px;">
            How ${ag.name} Works
          </h2>

          <div class="simple-arch-svg-wrap">
            <svg viewBox="0 0 920 148" style="width:100%; height:auto; display:block;">
              <!-- Connecting Arrows -->
              <line x1="205" y1="74" x2="245" y2="74" stroke="${dept.color}" stroke-width="2" stroke-dasharray="5 4" />
              <polygon points="245,74 237,69 237,79" fill="${dept.color}" />

              <line x1="435" y1="74" x2="475" y2="74" stroke="#4285f4" stroke-width="2" stroke-dasharray="5 4" />
              <polygon points="475,74 467,69 467,79" fill="#4285f4" />

              <line x1="675" y1="74" x2="715" y2="74" stroke="#34a853" stroke-width="2" stroke-dasharray="5 4" />
              <polygon points="715,74 707,69 707,79" fill="#34a853" />

              <!-- Box 1: Data Sources -->
              <rect x="15" y="20" width="190" height="108" rx="12" fill="var(--bg-card)" stroke="${dept.color}" stroke-width="1.5" />
              <text x="30" y="46" fill="${dept.color}" font-size="11" font-weight="700">01 · DATA SOURCES</text>
              <text x="30" y="72" fill="var(--text-primary)" font-size="13.5" font-weight="700">${s1}</text>
              <text x="30" y="96" fill="var(--text-secondary)" font-size="12">${s2}</text>

              <!-- Box 2: Digital Twin -->
              <rect x="245" y="20" width="190" height="108" rx="12" fill="var(--bg-card)" stroke="#4285f4" stroke-width="1.5" />
              <text x="260" y="46" fill="#4285f4" font-size="11" font-weight="700">02 · DATA PLATFORM</text>
              <text x="260" y="72" fill="var(--text-primary)" font-size="13.5" font-weight="700">BigQuery &amp; Spanner</text>
              <text x="260" y="96" fill="var(--text-secondary)" font-size="12">Unified Supply Chain Data</text>

              <!-- Box 3: AI Agent & Reasoning -->
              <rect x="475" y="16" width="200" height="116" rx="12" fill="var(--bg-card)" stroke="#7e57c2" stroke-width="2" />
              <text x="490" y="44" fill="#7e57c2" font-size="11" font-weight="700">03 · AI AGENT</text>
              <text x="490" y="70" fill="var(--text-primary)" font-size="13.5" font-weight="700">${agentShort}</text>
              <text x="490" y="94" fill="var(--text-secondary)" font-size="12">Gemini + OR-Tools Solver</text>

              <!-- Box 4: Enterprise Execution -->
              <rect x="715" y="20" width="190" height="108" rx="12" fill="var(--bg-card)" stroke="#34a853" stroke-width="1.5" />
              <text x="730" y="46" fill="#34a853" font-size="11" font-weight="700">04 · EXECUTION</text>
              <text x="730" y="72" fill="var(--text-primary)" font-size="13.5" font-weight="700">Automated Action</text>
              <text x="730" y="96" fill="var(--text-secondary)" font-size="12">ERP / WMS Write-Back</text>
            </svg>
          </div>
        </div>
      `;
    }

    function openAgentPage(agentId, pushHash = true, ev = null) {
      const ag = AGENTS[agentId];
      if (!ag) return;
      const useSlide = isPillOrNavSwitch(ev);
      const sRect = useSlide ? null : getClickedCardRect(ev);
      const transClass = getPageTransitionClass(ev, sRect);

      const dept = getDeptMeta(ag.deptId);
      const backPersona = PERSONAS[lastPersonaId] || Object.values(PERSONAS)[0];
      const videoUrl = customVideos[ag.id] || ag.videoSrc;
      const hasVideo = Boolean(customVideos[ag.id]) || Boolean(ag.hasPreloadedVideo);

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
          </div>

          <!-- 1. What This Agent Does -->
          <div class="agent-hero-banner" style="padding: 30px 34px; margin-bottom: 24px;">
            <div style="position:relative; z-index:2; display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin-bottom:12px;">
              <div class="persona-badge" style="margin-bottom:0; background: ${dept.color}18; color: ${dept.color}; border: 1px solid ${dept.color}40;">
                <span>${ag.isUniversal ? '🌐 Universal Core Agent' : `${dept.scorBadge} · ${dept.name}`}</span>
              </div>
            </div>

            <h1 class="agent-title" style="font-size: clamp(28px, 3.2vw, 40px); margin-bottom: 10px;">${ag.name}</h1>
            <p class="agent-subtitle" style="font-size: 16.5px;">
              ${shortSentence(ag.shortDesc, 175)} ${shortSentence(ag.solution, 175)}
            </p>
          </div>

          <!-- 2. Small Architecture Diagram -->
          ${renderSimpleAgentArchitectureDiagram(ag, dept)}

          <!-- 3. Dedicated Box for a Video -->
          <div class="video-stage-box">
            <div class="video-toolbar" style="border-top:none; border-bottom:1px solid var(--border-subtle);">
              <span style="font-weight:700; color:var(--text-primary);">🎬 Agent Demo Video — ${ag.name}</span>
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
                        <div style="font-size:14.5px; color:var(--text-secondary); max-width:480px;">
                          Video slot ready. Click <strong>Attach Video (.mp4)</strong> to load a recording, or switch to <strong>Interactive Preview</strong>.
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
    }"""
    assert old_agent_pattern.search(src), "Could not locate openAgentPage()"
    src = old_agent_pattern.sub(lambda _: new_agent_js, src, count=1)

    # Default stageViewMode to 'video' so the Video Box is immediately shown on Agent pages
    src = src.replace("let stageViewMode = 'cad';", "let stageViewMode = 'video';")

    # -------------------------------------------------------------------------
    # 10. SIMPLIFY DIRECTORY CARDS (NO ROI / NO BLUEPRINT CLUTTER)
    # -------------------------------------------------------------------------
    old_dir_cards_pattern = re.compile(
        r"function renderDirectoryCardsHtml\(deptFilter,\s*searchQuery,\s*mode\s*=\s*currentDirMode\)\s*\{[\s\S]*?function filterDirectoryLive\(val\)",
        re.MULTILINE,
    )
    new_dir_cards_js = """function renderDirectoryCardsHtml(deptFilter, searchQuery, mode = currentDirMode) {
      const q = (searchQuery || '').trim().toLowerCase();

      if (mode === 'agents') {
        const agentsList = Object.values(AGENTS).filter(ag => {
          if (deptFilter === 'universal' && !ag.isUniversal) return false;
          if (deptFilter !== 'all' && deptFilter !== 'universal' && ag.deptId !== deptFilter) return false;
          if (!q) return true;
          const dept = getDeptMeta(ag.deptId);
          const haystack = [ag.name, ag.shortDesc, dept ? dept.name : ''].join(' ').toLowerCase();
          return haystack.includes(q);
        });

        if (!agentsList.length) {
          return `<div style="grid-column: 1 / -1; padding: 36px; text-align: center; color: var(--text-secondary);">No matching agents found.</div>`;
        }

        return agentsList.map(ag => {
          const dept = getDeptMeta(ag.deptId);
          return `
            <div class="dir-persona-card" style="--dept-accent: ${dept.color}; cursor:pointer;" onclick="openAgentPage('${ag.id}', true, event)">
              <div>
                <div style="font-size:11.5px; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:${dept.color}; margin-bottom:4px;">
                  ${ag.isUniversal ? 'Universal Core Agent' : `${dept.scorBadge || ''} · ${dept.name}`}
                </div>
                <div style="font-family:var(--font-display); font-size:19px; font-weight:800; color:var(--text-primary); margin-bottom:8px;">
                  ${ag.name}
                </div>
                <p style="font-size:14.5px; color:var(--text-secondary); line-height:1.58; margin:0;">
                  ${shortSentence(ag.shortDesc, 130)}
                </p>
              </div>
              <div style="display:flex; justify-content:space-between; align-items:center; padding-top:12px; border-top:1px solid var(--border-subtle); font-size:13.5px; font-weight:700; color:${dept.color};">
                <span>Open Agent</span>
                <span>&rarr;</span>
              </div>
            </div>
          `;
        }).join('');
      }

      const personasList = Object.values(PERSONAS).filter(p => {
        if (deptFilter !== 'all' && deptFilter !== 'universal' && p.deptId !== deptFilter) return false;
        if (!q) return true;
        const dept = getDeptMeta(p.deptId);
        const haystack = [p.name, p.role, p.summary, dept ? dept.name : ''].join(' ').toLowerCase();
        return haystack.includes(q);
      });

      if (!personasList.length) {
        return `<div style="grid-column: 1 / -1; padding: 36px; text-align: center; color: var(--text-secondary);">No matching personas found.</div>`;
      }

      return personasList.map(p => {
        const dept = getDeptMeta(p.deptId);
        return `
          <div class="dir-persona-card" style="--dept-accent: ${dept.color}; cursor:pointer;" onclick="openPersonaPage('${p.id}', true, event)">
            <div>
              <div class="dir-card-person" style="margin-bottom: 10px;">
                <div class="persona-emoji" style="width:42px; height:42px; font-size:20px;">${p.icon}</div>
                <div>
                  <div style="font-size:11.5px; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:${dept.color};">
                    ${dept.scorBadge || ''} · ${dept.name}
                  </div>
                  <div style="font-family:var(--font-display); font-size:18.5px; font-weight:800; color:var(--text-primary);">
                    ${p.name}
                  </div>
                  <div style="font-size:13px; color:var(--text-secondary);">${p.role}</div>
                </div>
              </div>
              <p style="font-size:14.5px; color:var(--text-secondary); line-height:1.58; margin:0;">
                ${shortSentence(p.summary, 130)}
              </p>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; padding-top:12px; border-top:1px solid var(--border-subtle); font-size:13.5px; font-weight:700; color:${dept.color};">
              <span>Open Persona (${(p.agentIds || []).length} Agents)</span>
              <span>&rarr;</span>
            </div>
          </div>
        `;
      }).join('');
    }

    function filterDirectoryLive(val)"""
    assert old_dir_cards_pattern.search(src), "Could not locate renderDirectoryCardsHtml()"
    src = old_dir_cards_pattern.sub(lambda _: new_dir_cards_js, src, count=1)

    # -------------------------------------------------------------------------
    # 11. MAKE HERO CANVAS THEME-AWARE (DIMMER COLORS ON LIGHT THEME) & CALL initPortalTheme()
    # -------------------------------------------------------------------------
    src = src.replace(
        "ctx.clearRect(0, 0, w, h);",
        """ctx.clearRect(0, 0, w, h);
        const isLightTheme = document.documentElement.getAttribute('data-theme') === 'light';
        ctx.globalAlpha = isLightTheme ? 0.55 : 0.85;""",
    )

    src = src.replace(
        "hydrateAssets();\n      initHeroSupplyChainCanvas();",
        "initPortalTheme();\n      hydrateAssets();\n      initHeroSupplyChainCanvas();",
    )

    BUILD_SITE.write_text(src, encoding="utf-8")
    print("Successfully updated build_site.py with Light/Dark themes and simplified content.")


if __name__ == "__main__":
    main()

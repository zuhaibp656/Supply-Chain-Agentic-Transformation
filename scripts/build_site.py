#!/usr/bin/env python3
"""Build the Apple/Gemini-style scrollable, zero-clutter, multi-page
Supply Chain & Demand (Office of the CSCO) Agentic Transformation website (`index.html`).

Matches the exact visual language, Google Sans typography, full-screen scrollable
Gemini hero, progressive one-by-one disclosure, and 4-page isolation of the
reference CFO portal—while adding:
  1. 100% Industry-Agnostic Supply Chain & Demand (Office of the CSCO) taxonomy
     (4 Departments, 12 Personas, 12 Process-Fixing Agents, 2 6-Stage Value Chains: F2F & O2D)
  2. macOS Genie Effect transitions when expanding Department Showcase cards and opening pages
  3. Interactive Supply Chain Vector CAD Simulations alongside pre-rendered MP4 demo videos
"""

from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
CFO_HTML = pathlib.Path("/tmp/cfo_site.html")
OUT_HTML = ROOT / "index.html"


def extract_embedded_webp_blobs() -> str:
    """Extract only brand/sparkle blobs from /tmp/cfo_site.html (no abstract flowers/sculptures)."""
    if not CFO_HTML.exists():
        return "{}"
    text = CFO_HTML.read_text(errors="ignore")
    marker = "const EMBEDDED_WEBP_BLOBS = "
    idx = text.find(marker)
    if idx == -1:
        return "{}"
    end_idx = text.find("};\n    const EMBEDDED_ASSET_MAP", idx)
    if end_idx == -1:
        end_idx = text.find("};", idx)
    if end_idx == -1:
        return "{}"
    raw_json = text[idx + len(marker) : end_idx + 1]
    try:
        data = json.loads(raw_json)
        keep = {
            "gemini_enterprise_dark.webp",
            "google_cloud_logo.webp",
            "sparkle_blue_violet.webp",
        }
        filtered = {k: v for k, v in data.items() if k in keep}
        return json.dumps(filtered)
    except Exception:
        return raw_json


def load_all_twins_json() -> str:
    twins_dir = ROOT / "data" / "twins"
    twins = {}
    if twins_dir.exists():
        for p in sorted(twins_dir.glob("*.json")):
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                key = p.stem.lower()
                twins[key] = data
            except Exception as e:
                print(f"Warning: could not load twin {p}: {e}")
    return json.dumps(twins, indent=2)


def build_html() -> str:
    blobs_js = extract_embedded_webp_blobs()
    twins_js = load_all_twins_json()

    catalog_path = ROOT / "data" / "supply_chain_catalog.json"
    cat_data = json.loads(catalog_path.read_text(encoding="utf-8"))
    depts_js = json.dumps(cat_data["departments"], indent=2, ensure_ascii=False)
    personas_js = json.dumps(cat_data["personas"], indent=2, ensure_ascii=False)
    agents_js = json.dumps(cat_data["agents"], indent=2, ensure_ascii=False)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Gemini Enterprise — Supply Chain &amp; Demand (Office of the CSCO)</title>
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23050811'/%3E%3Cpolygon points='32,10 52,21 52,43 32,54 12,43 12,21' fill='rgba(0,210,255,0.18)' stroke='%2300d2ff' stroke-width='3'/%3E%3Cpath d='M32 10 L32 32 L52 21 M32 32 L12 21 M32 32 L32 54' stroke='%2334d399' stroke-width='2.5' fill='none'/%3E%3Ccircle cx='32' cy='32' r='4.5' fill='%23ffffff'/%3E%3C/svg%3E" />
  <!-- Google Sans, Google Sans Text, Google Sans Display, Inter & JetBrains Mono Typography -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Google+Sans:ital,wght@0,400;0,500;0,700;1,400&family=Google+Sans+Display:wght@400;500;700;800&family=Google+Sans+Text:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">

  <style>
    :root {
      --bg-page: #04060a;
      --bg-surface: #0b0f19;
      --bg-card: #101726;
      --bg-card-hover: #162033;
      --text-primary: #ffffff;
      --text-secondary: #cbd5e1;
      --text-muted: #94a3b8;
      --border-subtle: rgba(255, 255, 255, 0.09);
      --border-strong: rgba(255, 255, 255, 0.18);

      /* Official Google + Supply Chain Vibrant Palette */
      --g-blue: #4285f4;
      --g-green: #34a853;
      --g-yellow: #fbbc04;
      --g-red: #ea4335;
      --sc-cyan: #00d2ff;
      --sc-emerald: #10b981;
      --sc-amber: #ff8c00;
      --sc-violet: #a142f4;

      --font-sans: 'Google Sans Text', 'Google Sans', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-display: 'Google Sans Display', 'Google Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', 'Roboto Mono', 'SF Mono', Menlo, Consolas, monospace;
      --ease-spring: cubic-bezier(0.22, 1, 0.36, 1);
      --ease-fluid: cubic-bezier(0.16, 1, 0.3, 1);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    html {
      scroll-behavior: smooth;
      font-family: var(--font-sans);
      background: var(--bg-page);
      color: var(--text-primary);
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      text-rendering: optimizeLegibility;
      font-feature-settings: "cv02", "cv03", "cv04", "cv11";
    }

    body {
      font-family: var(--font-sans);
      background: var(--bg-page);
      color: var(--text-primary);
      min-height: 100vh;
      overflow-x: hidden;
      line-height: 1.66;
      letter-spacing: -0.006em;
    }

    h1, h2, h3, h4, .hero-title, .section-title, .persona-page-title, .agent-title, .block-title {
      text-wrap: balance;
      font-weight: 800;
      letter-spacing: -0.025em;
      color: #ffffff;
    }

    p, li, .hero-subtitle, .section-subtitle, .persona-page-summary, .agent-subtitle, .detail-card-text, .exec-pitch-text, .exec-pitch-body {
      text-wrap: pretty;
    }

    button, input, a {
      font-family: var(--font-sans);
      color: inherit;
      text-decoration: none;
      border: none;
      background: none;
      cursor: pointer;
    }

    /* =========================================================================
       CLEAN, CALM READABILITY SYSTEM (NO NOISY BOXES OR UNDERLINES IN TEXT)
       ========================================================================= */
    .sc-hl-metric {
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
    }

    .sc-rich-points {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin: 0;
      padding: 0;
    }

    .sc-rich-points li {
      display: flex;
      align-items: flex-start;
      gap: 10px;
      line-height: 1.65;
      color: #e2e8f0;
      font-size: inherit;
    }

    .sc-rich-points li .sc-pt-bullet {
      color: var(--pt-color, var(--pitch-accent, var(--dept-accent, #38bdf8)));
      font-weight: 700;
      font-size: 1em;
      line-height: 1.5;
      flex-shrink: 0;
    }

    /* =========================================================================
       3-PART PURPOSE-BUILT ANIMATION SYSTEM:
       1) GENIE EFFECT — For Expanding Cards / Verticals (animateGenieOutOfBox)
       2) DROPDOWN EFFECT — For Dropdown Menus & Accordions (smooth unroll)
       3) SLIDE EFFECT — For Page & Tab Switching (page-slide-right / left)
       ========================================================================= */
    #genieSvgOverlay {
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 9999;
      opacity: 0;
      transition: opacity 0.22s var(--ease-fluid);
    }

    #genieSvgOverlay.active {
      opacity: 1;
    }

    .genie-target, .genie-enter, .page-slide-right, .page-slide-left {
      will-change: transform, opacity, clip-path, filter;
    }

    @keyframes fluidicGenieEnter {
      0% {
        opacity: 0;
        transform: translateY(16px) scale(0.985);
      }
      100% {
        opacity: 1;
        transform: translateY(0) scale(1);
      }
    }

    @keyframes pageSlideFromRight {
      0% {
        opacity: 0;
        transform: translate3d(44px, 0, 0);
      }
      100% {
        opacity: 1;
        transform: translate3d(0, 0, 0);
      }
    }

    @keyframes pageSlideFromLeft {
      0% {
        opacity: 0;
        transform: translate3d(-44px, 0, 0);
      }
      100% {
        opacity: 1;
        transform: translate3d(0, 0, 0);
      }
    }

    @keyframes dropdownUnroll {
      0% {
        opacity: 0;
        transform: translateY(-10px) scaleY(0.95);
        transform-origin: top center;
      }
      100% {
        opacity: 1;
        transform: translateY(0) scaleY(1);
        transform-origin: top center;
      }
    }

    @keyframes staggerCardRise {
      0% {
        opacity: 0;
        transform: translateY(14px);
      }
      100% {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @keyframes cadStageReveal {
      0% {
        opacity: 0.45;
        transform: translateX(14px);
      }
      100% {
        opacity: 1;
        transform: translateX(0);
      }
    }

    .genie-enter {
      animation: fluidicGenieEnter 0.52s var(--ease-spring) both;
    }

    .page-slide-right, .slide-down-enter {
      animation: pageSlideFromRight 0.46s var(--ease-spring) both;
    }

    .page-slide-left {
      animation: pageSlideFromLeft 0.46s var(--ease-spring) both;
    }

    .cad-stage-anim {
      animation: cadStageReveal 0.34s var(--ease-spring) both;
    }

    /* Staggered Fluidic Cascade for Cards & Schedule Rows */
    .dept-node,
    .universal-agent-card,
    .vc-entry-card,
    .showcase-panel,
    .persona-link-card,
    .agent-roi-card,
    .exec-pitch-card,
    .detail-card,
    .schedule-row-human,
    .schedule-row-toil,
    .catalog-card,
    .dir-persona-card,
    .vc-stage-row,
    .subagent-card,
    .arch-layer-card {
      animation: staggerCardRise 0.48s var(--ease-spring) both;
    }

    .dept-row > :nth-child(1), .universal-agents-grid > :nth-child(1), .agent-roi-grid > :nth-child(1), .exec-pitch-grid > :nth-child(1), .catalog-grid > :nth-child(1), .dir-persona-grid > :nth-child(1), .day-schedule > :nth-child(1), .showcase-grid > :nth-child(1), .agent-details-grid > :nth-child(1) { animation-delay: 0.02s; }
    .dept-row > :nth-child(2), .universal-agents-grid > :nth-child(2), .agent-roi-grid > :nth-child(2), .exec-pitch-grid > :nth-child(2), .catalog-grid > :nth-child(2), .dir-persona-grid > :nth-child(2), .day-schedule > :nth-child(2), .showcase-grid > :nth-child(2), .agent-details-grid > :nth-child(2) { animation-delay: 0.06s; }
    .dept-row > :nth-child(3), .universal-agents-grid > :nth-child(3), .agent-roi-grid > :nth-child(3), .exec-pitch-grid > :nth-child(3), .catalog-grid > :nth-child(3), .dir-persona-grid > :nth-child(3), .day-schedule > :nth-child(3), .showcase-grid > :nth-child(3), .agent-details-grid > :nth-child(3) { animation-delay: 0.10s; }
    .dept-row > :nth-child(4), .universal-agents-grid > :nth-child(4), .agent-roi-grid > :nth-child(4), .catalog-grid > :nth-child(4), .dir-persona-grid > :nth-child(4), .day-schedule > :nth-child(4) { animation-delay: 0.14s; }
    .dept-row > :nth-child(5), .catalog-grid > :nth-child(5), .dir-persona-grid > :nth-child(5), .day-schedule > :nth-child(5) { animation-delay: 0.18s; }
    .dept-row > :nth-child(6), .catalog-grid > :nth-child(6), .dir-persona-grid > :nth-child(6), .day-schedule > :nth-child(6) { animation-delay: 0.22s; }
    .dept-row > :nth-child(7) { animation-delay: 0.25s; }
    .dept-row > :nth-child(8) { animation-delay: 0.28s; }

    /* =========================================================================
       TOP NAVIGATION BAR (ZERO OVERFLOW, RESPONSIVE WRAP)
       ========================================================================= */
    .navbar {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      min-height: 72px;
      z-index: 100;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px 20px;
      padding: 10px 36px;
      background: rgba(4, 6, 10, 0.86);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--border-subtle);
    }

    @media (max-width: 900px) {
      .navbar {
        padding: 10px 20px;
      }
    }

    .nav-brand {
      display: flex;
      align-items: center;
      gap: 14px;
      cursor: pointer;
      flex-shrink: 0;
    }

    .nav-brand img.gemini-logo {
      height: 26px;
      width: auto;
      display: block;
    }

    .nav-divider {
      width: 1px;
      height: 20px;
      background: var(--border-strong);
    }

    .nav-brand img.gcloud-logo {
      height: 20px;
      width: auto;
      display: block;
      opacity: 0.92;
    }

    .nav-right {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
    }

    .nav-pill-btn {
      padding: 8px 16px;
      border-radius: 999px;
      font-size: 13.5px;
      font-weight: 500;
      color: var(--text-secondary);
      border: 1px solid transparent;
      white-space: nowrap;
      transition: all 0.28s var(--ease-spring);
    }

    .nav-pill-btn:hover {
      color: var(--text-primary);
      background: rgba(255, 255, 255, 0.07);
      transform: translateY(-1px);
    }

    .nav-pill-btn.primary {
      color: #ffffff;
      background: linear-gradient(135deg, #4285f4, #2563eb);
      box-shadow: 0 6px 20px rgba(66, 133, 244, 0.32);
    }

    .nav-pill-btn.primary:hover {
      background: linear-gradient(135deg, #5a95f5, #3b82f6);
      box-shadow: 0 10px 26px rgba(66, 133, 244, 0.48);
    }

    /* =========================================================================
       PAGE VIEWS (STRICT MULTI-PAGE ISOLATION — ONE BY ONE, ZERO CLUTTER)
       ========================================================================= */
    .page-view {
      display: none;
      min-height: 100vh;
    }

    .page-view.active {
      display: block;
    }

    /* =========================================================================
       PAGE 1, SECTION 1: FULL-SCREEN APPLE / GEMINI SCROLLABLE HERO LANDING
       WITH LIVE 3D ISOMETRIC CONVEYOR BELT, MOVING CARGO BOXES & ROUTE NETWORK
       ========================================================================= */
    .hero-section {
      position: relative;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      padding: 128px 24px 88px;
      background: #020408;
      overflow: hidden;
      border-bottom: 1px solid var(--border-subtle);
    }

    /* Smooth Ambient Aurora & Architectural Horizon Backdrop (Replaces scattering particle sprinkles) */
    @keyframes auroraFloat {
      0%, 100% {
        transform: translate3d(0, 0, 0) scale(1);
        opacity: 0.72;
      }
      50% {
        transform: translate3d(18px, -14px, 0) scale(1.06);
        opacity: 0.95;
      }
    }

    .hero-aurora-backdrop {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 1;
      background:
        radial-gradient(circle 520px at 16% 26%, rgba(0, 210, 255, 0.14), transparent 72%),
        radial-gradient(circle 560px at 84% 32%, rgba(161, 66, 244, 0.14), transparent 72%),
        radial-gradient(circle 480px at 22% 76%, rgba(16, 185, 129, 0.12), transparent 70%),
        radial-gradient(circle 520px at 82% 78%, rgba(255, 140, 0, 0.11), transparent 72%);
      animation: auroraFloat 11s ease-in-out infinite;
    }

    #heroSupplyChainCanvas {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 2;
    }

    @keyframes dashFlow {
      to { stroke-dashoffset: -64; }
    }

    .sc-arc-flow {
      stroke-dasharray: 10 8;
      animation: dashFlow 2.4s linear infinite;
    }

    @keyframes conveyorBoxSlide {
      0% { transform: translate(0px, 0px); opacity: 0.25; }
      18% { opacity: 1; }
      82% { opacity: 1; }
      100% { transform: translate(78px, 39px); opacity: 0.25; }
    }

    .sc-conveyor-box-anim {
      animation: conveyorBoxSlide 3.4s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    .sc-conveyor-box-anim-delayed {
      animation: conveyorBoxSlide 3.4s cubic-bezier(0.4, 0, 0.6, 1) 1.7s infinite;
    }

    @keyframes pulseNode {
      0%, 100% { transform: scale(1); opacity: 0.88; }
      50% { transform: scale(1.22); opacity: 1; }
    }

    .sc-node-pulse {
      transform-box: fill-box;
      transform-origin: center;
      animation: pulseNode 2.6s ease-in-out infinite;
    }

    /* Feathered radial vignette that keeps the central hero text column legible while letting background animations flow seamlessly */
    .hero-vignette {
      position: absolute;
      inset: 0;
      background:
        radial-gradient(ellipse 32% 38% at 50% 48%, rgba(2, 4, 8, 0.86) 0%, rgba(2, 4, 8, 0.48) 54%, rgba(2, 4, 8, 0.0) 100%),
        linear-gradient(180deg, rgba(2, 4, 8, 0.28) 0%, rgba(2, 4, 8, 0.04) 50%, rgba(4, 6, 10, 0.85) 100%);
      pointer-events: none;
      z-index: 3;
    }

    .hero-content {
      position: relative;
      z-index: 5;
      max-width: 1080px;
      padding: 0 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      animation: fluidicGenieEnter 0.72s var(--ease-spring) both;
    }

    .hero-logo-lockup {
      display: inline-flex;
      align-items: center;
      gap: 18px;
      padding: 10px 26px;
      border-radius: 999px;
      background: rgba(11, 15, 25, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.18);
      margin-bottom: 30px;
      backdrop-filter: blur(16px);
      box-shadow: 0 14px 36px rgba(0, 0, 0, 0.55);
    }

    .hero-logo-lockup img.gemini-hero {
      height: 30px;
      width: auto;
    }

    .hero-logo-lockup img.sparkle-icon {
      width: 24px;
      height: 24px;
      animation: pulseSparkle 3s infinite ease-in-out;
    }

    @keyframes pulseSparkle {
      0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.9; }
      50% { transform: scale(1.18) rotate(8deg); opacity: 1; }
    }

    .hero-title {
      font-family: var(--font-display);
      font-size: clamp(44px, 5.5vw, 74px);
      font-weight: 800;
      line-height: 1.08;
      letter-spacing: -0.028em;
      color: #ffffff;
      margin-bottom: 24px;
      text-shadow: 0 10px 36px rgba(0, 0, 0, 0.85);
    }

    .hero-title .gradient-word {
      background: linear-gradient(92deg, #8ab4f8 0%, #38bdf8 36%, #81c995 70%, #fde293 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
      font-size: clamp(18.5px, 2.0vw, 22.5px);
      font-weight: 500;
      color: #f1f5f9;
      max-width: 940px;
      line-height: 1.68;
      margin-bottom: 40px;
      text-shadow: 0 4px 20px rgba(0, 0, 0, 0.9);
    }

    .hero-cta-btn {
      display: inline-flex;
      align-items: center;
      gap: 12px;
      padding: 15px 32px;
      border-radius: 999px;
      background: #ffffff;
      color: #04060a;
      font-size: 16px;
      font-weight: 700;
      transition: transform 0.32s var(--ease-spring), box-shadow 0.32s var(--ease-spring), background 0.25s ease;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.55);
    }

    .hero-cta-btn:hover {
      transform: translateY(-3px) scale(1.015);
      box-shadow: 0 18px 44px rgba(0, 210, 255, 0.38);
    }

    .four-color-bar {
      display: flex;
      width: 180px;
      height: 4px;
      border-radius: 999px;
      overflow: hidden;
      margin-top: 48px;
      box-shadow: 0 0 20px rgba(0, 210, 255, 0.28);
    }
    .four-color-bar span { flex: 1; }

    /* =========================================================================
       PAGE 1, SECTION 2: CSCO ORG CHART & PROGRESSIVE DEPARTMENT SHOWCASE BOX
       WIDER BALANCED CANVAS (1580PX / 92VW) SO SIDES ARE NOT EMPTY
       ========================================================================= */
    .org-section {
      position: relative;
      max-width: 1580px;
      width: 92vw;
      margin: 0 auto;
      padding: 88px 20px 120px;
    }

    .section-header {
      text-align: center;
      margin-bottom: 48px;
    }

    .section-title {
      font-family: var(--font-display);
      font-size: clamp(32px, 3.8vw, 48px);
      font-weight: 800;
      letter-spacing: -0.026em;
      line-height: 1.14;
      margin-bottom: 14px;
      color: #ffffff;
    }

    .section-subtitle {
      font-size: 18.5px;
      color: #e2e8f0;
      max-width: 1160px;
      margin: 0 auto;
      line-height: 1.68;
    }

    .cfo-root-wrapper {
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .cfo-box {
      position: relative;
      display: flex;
      align-items: center;
      gap: 22px;
      padding: 22px 42px 22px 26px;
      border-radius: 22px;
      background: linear-gradient(145deg, #0b111e 0%, #060911 100%);
      border: 2px solid var(--sc-cyan);
      box-shadow: 0 18px 52px rgba(0, 210, 255, 0.18), inset 0 1px 0 rgba(255, 255, 255, 0.12);
      overflow: hidden;
      transition: transform 0.35s var(--ease-spring), box-shadow 0.35s var(--ease-spring);
    }

    .cfo-box:hover {
      transform: translateY(-2px);
      box-shadow: 0 22px 60px rgba(0, 210, 255, 0.26), inset 0 1px 0 rgba(255, 255, 255, 0.18);
    }

    .cfo-sc-emblem {
      width: 82px;
      height: 64px;
      border-radius: 14px;
      border: 1px solid rgba(0, 210, 255, 0.32);
      background: radial-gradient(circle at 50% 50%, rgba(0, 210, 255, 0.16), #04070f 85%);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      overflow: hidden;
    }

    .cfo-box-title {
      font-family: var(--font-display);
      font-size: 24px;
      font-weight: 800;
      letter-spacing: -0.018em;
      color: #ffffff;
    }

    .cfo-box-sub {
      font-size: 15.5px;
      color: #e2e8f0;
      margin-top: 4px;
      line-height: 1.52;
    }

    .org-connectors {
      width: 100%;
      max-width: 1280px;
      height: 58px;
      display: block;
    }

    .org-connectors path.tree-base {
      fill: none;
      stroke: rgba(255, 255, 255, 0.18);
      stroke-width: 2;
    }

    .org-connectors path.tree-pulse {
      fill: none;
      stroke: var(--sc-cyan);
      stroke-width: 2.2;
      stroke-dasharray: 8 10;
      animation: dashFlow 2.6s linear infinite;
      opacity: 0.75;
    }

    .dept-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
      width: 100%;
    }

    @media (max-width: 1280px) {
      .dept-row { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 680px) {
      .dept-row { grid-template-columns: 1fr; }
      .org-connectors { display: none; }
      .cfo-box { margin-bottom: 28px; }
    }

    /* Three Rivers Flow Architecture Banner */
    .rivers-banner {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin: 28px 0 32px;
      width: 100%;
    }
    @media (max-width: 900px) {
      .rivers-banner { grid-template-columns: 1fr; }
    }
    .river-box {
      background: linear-gradient(165deg, rgba(16, 26, 46, 0.88) 0%, rgba(9, 14, 26, 0.94) 100%);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 14px;
      padding: 18px 20px;
      border-left: 4px solid #38bdf8;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
      position: relative;
      overflow: hidden;
      transition: transform 0.25s ease, border-color 0.25s ease;
    }
    .river-box:hover {
      transform: translateY(-2px);
      border-color: rgba(255, 255, 255, 0.22);
    }
    .river-box.signal { border-left-color: #f472b6; }
    .river-box.cash { border-left-color: #10b981; }
    .river-box h4 {
      font-size: 14.5px;
      font-weight: 800;
      color: #fff;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .river-box p {
      font-size: 13px;
      color: #94a3b8;
      line-height: 1.58;
    }

    /* 8-Vertical Interactive Master Navigation Tab Bar on Front Page */
    .vertical-tabs-nav-bar {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 10px;
      padding: 14px 18px;
      background: rgba(9, 14, 25, 0.92);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 20px;
      margin: 18px 0 34px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.45);
      position: sticky;
      top: 68px;
      z-index: 95;
    }
    .v-tab-btn {
      background: rgba(18, 28, 48, 0.85);
      color: #94a3b8;
      border: 1.5px solid rgba(255, 255, 255, 0.1);
      padding: 10px 16px;
      border-radius: 12px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.26s var(--ease-spring);
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 3px;
      text-align: left;
      min-width: 140px;
      position: relative;
    }
    .v-tab-btn:hover {
      background: rgba(28, 44, 72, 0.95);
      color: #fff;
      border-color: var(--v-accent, #38bdf8);
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
    }
    .v-tab-btn.active {
      background: linear-gradient(145deg, rgba(22, 38, 64, 0.98), rgba(12, 20, 36, 0.98));
      color: #fff;
      border-color: var(--v-accent, #38bdf8);
      box-shadow: 0 0 22px rgba(56, 189, 248, 0.28), inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    .v-tab-btn .v-tab-num {
      font-size: 10.5px;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--v-accent, #38bdf8);
    }
    .v-tab-btn .v-tab-title {
      font-size: 13px;
      font-weight: 800;
      color: #fff;
      white-space: nowrap;
    }
    .v-tab-btn .v-tab-tag {
      font-size: 11px;
      font-weight: 500;
      color: #94a3b8;
    }
    .v-tab-btn.active .v-tab-tag {
      color: #cbd5e1;
    }
    .v-tab-btn .v-tab-badge {
      font-size: 10px;
      font-weight: 600;
      color: #64748b;
      margin-top: 2px;
    }

    /* 4-Quadrant Level-1 to Level-3 Decomposition Grid inside Showcase */
    .quad-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
      margin: 20px 0;
      width: 100%;
    }
    .quad-card {
      background: rgba(14, 22, 38, 0.95);
      border: 1px solid rgba(255, 255, 255, 0.09);
      border-radius: 14px;
      padding: 18px 20px;
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
    }
    .quad-card h5 {
      font-size: 12.5px;
      font-weight: 800;
      color: var(--dept-accent, #38bdf8);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .quad-card ul {
      list-style: none;
      padding: 0;
      margin: 0;
    }
    .quad-card li {
      font-size: 13px;
      color: #cbd5e1;
      margin-bottom: 8px;
      padding-left: 16px;
      position: relative;
      line-height: 1.52;
    }
    .quad-card li::before {
      content: "▸";
      position: absolute;
      left: 0;
      color: var(--dept-accent, #38bdf8);
      font-weight: 700;
    }

    /* Interactive Multi-Echelon Safety Stock & ROP Calculator */
    .ss-calc-card {
      background: linear-gradient(165deg, rgba(14, 24, 42, 0.96) 0%, rgba(8, 14, 26, 0.98) 100%);
      border: 1px solid rgba(56, 189, 248, 0.28);
      border-radius: 20px;
      padding: 28px;
      margin: 36px 0 20px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
    }
    .ss-calc-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 20px;
    }
    .ss-calc-title {
      font-size: 20px;
      font-weight: 800;
      color: #fff;
    }
    .ss-calc-sub {
      font-size: 13.5px;
      color: #94a3b8;
      margin-top: 4px;
    }
    .control-row {
      display: flex;
      align-items: center;
      gap: 24px;
      flex-wrap: wrap;
      margin: 20px 0;
    }
    .control-field {
      flex: 1;
      min-width: 240px;
    }
    .control-field label {
      display: block;
      font-size: 12.5px;
      font-weight: 600;
      color: #94a3b8;
      margin-bottom: 6px;
    }
    .control-field input[type="range"] {
      width: 100%;
      accent-color: #38bdf8;
      cursor: pointer;
    }
    .ss-output-box {
      background: #060a12;
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 14px;
      padding: 20px;
      font-size: 14px;
      margin-top: 14px;
    }
    .bar-line { margin: 14px 0 6px; }
    .bar-meta { display: flex; justify-content: space-between; font-size: 12.5px; margin-bottom: 6px; color: #94a3b8; }
    .bar-outer {
      width: 100%;
      height: 24px;
      background: #090e17;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.1);
      overflow: hidden;
    }
    .bar-inner {
      height: 100%;
      background: linear-gradient(90deg, #38bdf8, #ec4899);
      transition: width 0.35s ease;
    }

    /* 5-Step S&OP Cadence Table */
    .sop-table-wrap {
      width: 100%;
      overflow-x: auto;
      margin: 24px 0;
      border-radius: 14px;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .sop-cadence-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13.5px;
      background: rgba(10, 16, 28, 0.95);
    }
    .sop-cadence-table th {
      background: #080d18;
      color: #38bdf8;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      padding: 12px 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      text-align: left;
    }
    .sop-cadence-table td {
      padding: 12px 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.07);
      color: #cbd5e1;
    }
    .sop-cadence-table tr:hover td {
      background: rgba(255, 255, 255, 0.03);
    }

    /* 6 SCOR Vertical Cards — Fitted Visible Animation Stage that Brightens on Hover & Expands on Click */
    .dept-node {
      position: relative;
      padding: 26px 26px 22px;
      border-radius: 22px;
      background: linear-gradient(165deg, rgba(15, 23, 38, 0.96) 0%, rgba(8, 13, 23, 0.99) 100%);
      border: 1px solid rgba(255, 255, 255, 0.13);
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.38), inset 0 1px 0 rgba(255, 255, 255, 0.08);
      text-align: left;
      cursor: pointer;
      transition: transform 0.34s var(--ease-spring), border-color 0.28s ease, box-shadow 0.34s var(--ease-spring), background 0.28s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 18px;
      min-height: 304px;
      overflow: hidden;
    }

    /* Dedicated, Clearly Visible & Seamless Supply Chain Animation Stage Inside Each Vertical Card */
    .dept-anim-stage {
      position: relative;
      width: calc(100% + 16px);
      margin: 0 -8px;
      height: 156px;
      border-radius: 18px;
      background: radial-gradient(ellipse 84% 78% at 50% 50%, rgba(20, 36, 68, 0.58) 0%, rgba(8, 13, 24, 0.0) 100%);
      border: 1px solid rgba(255, 255, 255, 0.05);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      padding: 6px 10px 26px;
      transition: all 0.36s var(--ease-spring);
    }

    .dept-anim-stage svg.dept-stage-svg {
      width: 100%;
      height: 100%;
      max-height: 144px;
      opacity: 0.92;
      transform: scale(1.06);
      filter: brightness(1.1) saturate(1.16);
      transition: transform 0.42s var(--ease-spring), opacity 0.32s ease, filter 0.32s ease;
    }

    .dept-anim-badge {
      position: absolute;
      right: 10px;
      bottom: 8px;
      padding: 4px 11px;
      border-radius: 999px;
      font-size: 11.5px;
      font-weight: 700;
      letter-spacing: 0.02em;
      background: rgba(6, 10, 20, 0.88);
      border: 1px solid rgba(255, 255, 255, 0.16);
      color: var(--text-secondary);
      backdrop-filter: blur(8px);
      transition: all 0.3s var(--ease-spring);
      pointer-events: none;
    }

    .dept-anim-meta {
      position: absolute;
      left: 12px;
      bottom: 8px;
      font-size: 12px;
      font-weight: 700;
      color: #f1f5f9;
      background: rgba(6, 10, 20, 0.78);
      border: 1px solid rgba(255, 255, 255, 0.12);
      padding: 4px 10px;
      border-radius: 999px;
      pointer-events: none;
      transition: color 0.28s ease, border-color 0.28s ease;
    }

    .dept-node:hover .dept-anim-stage,
    .dept-node.active .dept-anim-stage,
    .vc-entry-card:hover .dept-anim-stage {
      border-color: rgba(0, 210, 255, 0.28);
      background: radial-gradient(ellipse 88% 82% at 50% 50%, rgba(28, 52, 94, 0.74) 0%, rgba(7, 13, 26, 0.0) 100%);
      transform: scale(1.02);
    }

    .dept-node:hover .dept-anim-stage svg.dept-stage-svg,
    .dept-node.active .dept-anim-stage svg.dept-stage-svg,
    .vc-entry-card:hover .dept-anim-stage svg.dept-stage-svg {
      opacity: 1;
      transform: scale(1.12);
      filter: brightness(1.3) saturate(1.28) drop-shadow(0 0 12px rgba(0, 210, 255, 0.32));
    }

    .dept-node:hover .dept-anim-badge,
    .dept-node.active .dept-anim-badge,
    .vc-entry-card:hover .dept-anim-badge {
      background: var(--dept-accent, var(--vc-accent, #00d2ff));
      border-color: var(--dept-accent, var(--vc-accent, #00d2ff));
      color: #040810;
      transform: translateY(-1px);
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.45);
    }

    .dept-node:hover .dept-anim-meta,
    .dept-node.active .dept-anim-meta {
      color: #ffffff;
      border-color: var(--dept-accent, #00d2ff);
    }

    /* Subtle watermark class kept ONLY for Persona/Architecture header cards */
    .dept-node-sc-watermark {
      position: absolute;
      right: -12px;
      bottom: -10px;
      width: 190px;
      height: 135px;
      opacity: 0.32;
      pointer-events: none;
      z-index: 1;
      transition: transform 0.45s var(--ease-spring), opacity 0.35s ease;
    }

    .dept-node::before {
      content: '';
      position: absolute;
      top: 0;
      left: 24px;
      right: 24px;
      height: 4px;
      border-radius: 0 0 4px 4px;
      background: var(--dept-accent);
      opacity: 0.85;
      transition: opacity 0.28s ease, left 0.32s var(--ease-spring), right 0.32s var(--ease-spring);
    }

    .dept-node:hover {
      background: linear-gradient(165deg, rgba(22, 32, 52, 0.98) 0%, rgba(12, 18, 32, 1) 100%);
      transform: translateY(-5px);
      border-color: var(--dept-accent);
      box-shadow: 0 20px 46px rgba(0, 0, 0, 0.54), inset 0 1px 0 rgba(255, 255, 255, 0.12);
    }

    .dept-node.active {
      background: linear-gradient(165deg, rgba(22, 34, 56, 0.99) 0%, rgba(11, 17, 30, 1) 100%);
      border-color: var(--dept-accent);
      box-shadow: 0 22px 52px rgba(0, 0, 0, 0.65), 0 0 30px rgba(0, 210, 255, 0.16);
    }

    .dept-node.active::before {
      opacity: 1;
      left: 0;
      right: 0;
      border-radius: 22px 22px 0 0;
    }

    .dept-node-title {
      position: relative;
      z-index: 2;
      font-family: var(--font-display);
      font-size: 23.5px;
      font-weight: 800;
      letter-spacing: -0.02em;
      line-height: 1.24;
      color: #ffffff;
      margin-bottom: 8px;
    }

    .dept-node-sub {
      position: relative;
      z-index: 2;
      font-size: 16px;
      color: #e2e8f0;
      line-height: 1.62;
    }

    /* Department Showcase Box (Blossoms OUT of the clicked Department box via macOS Genie) */
    .dept-showcase-box {
      position: relative;
      margin-top: 28px;
      border-radius: 24px;
      background: linear-gradient(165deg, rgba(13, 19, 32, 0.98) 0%, rgba(8, 12, 22, 0.99) 100%);
      border: 1px solid var(--dept-accent, var(--border-strong));
      padding: 36px;
      box-shadow: 0 28px 68px rgba(0, 0, 0, 0.68), inset 0 1px 0 rgba(255, 255, 255, 0.08);
      overflow: hidden;
    }

    .showcase-bg-sc-watermark {
      position: absolute;
      right: -28px;
      bottom: -24px;
      width: 440px;
      height: 290px;
      opacity: 0.22;
      pointer-events: none;
      z-index: 1;
      -webkit-mask-image: radial-gradient(ellipse 75% 75% at 65% 65%, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0) 82%);
      mask-image: radial-gradient(ellipse 75% 75% at 65% 65%, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0) 82%);
    }

    .showcase-header {
      position: relative;
      z-index: 2;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding-bottom: 22px;
      margin-bottom: 24px;
      border-bottom: 1px solid var(--border-subtle);
    }

    .showcase-dept-name {
      font-family: var(--font-display);
      font-size: clamp(23px, 2.5vw, 29px);
      font-weight: 800;
      letter-spacing: -0.02em;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .accent-dot {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      display: inline-block;
      flex-shrink: 0;
    }

    /* Live Supply Chain Diagram Strip inside Opened Department Showcase */
    .showcase-visual-strip {
      position: relative;
      z-index: 2;
      margin-bottom: 24px;
      padding: 20px 24px;
      border-radius: 18px;
      background: rgba(6, 10, 18, 0.92);
      border: 1px solid var(--border-subtle);
      display: grid;
      grid-template-columns: 210px minmax(0, 1fr);
      gap: 24px;
      align-items: center;
    }

    @media (max-width: 760px) {
      .showcase-visual-strip { grid-template-columns: 1fr; }
    }

    .showcase-visual-meta {
      display: flex;
      flex-direction: column;
      gap: 6px;
      min-width: 0;
    }

    .showcase-visual-title {
      font-family: var(--font-display);
      font-size: 17.5px;
      font-weight: 800;
      letter-spacing: -0.012em;
    }

    .showcase-visual-desc {
      font-size: 15.8px;
      color: #f1f5f9;
      line-height: 1.64;
    }

    .showcase-grid {
      position: relative;
      z-index: 2;
      display: grid;
      grid-template-columns: 1fr 1fr 1.25fr;
      gap: 24px;
    }

    @media (max-width: 1060px) {
      .showcase-grid { grid-template-columns: 1fr; }
    }

    .showcase-panel {
      padding: 28px;
      border-radius: 18px;
      background: rgba(16, 22, 35, 0.92);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-subtle);
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }

    .panel-tag {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 12.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 12px;
    }

    .panel-metric {
      font-family: var(--font-display);
      font-size: clamp(24px, 2.3vw, 29px);
      font-weight: 800;
      letter-spacing: -0.022em;
      color: #ffffff;
      margin-bottom: 18px;
      line-height: 1.22;
      font-variant-numeric: tabular-nums;
      padding-bottom: 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .clean-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .clean-list li {
      display: flex;
      align-items: flex-start;
      gap: 11px;
      font-size: 16.5px;
      color: #f8fafc;
      line-height: 1.64;
    }

    .clean-list li span.bullet {
      font-weight: 800;
      flex-shrink: 0;
      margin-top: 1px;
    }

    .dept-personas-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .persona-link-card {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      padding: 16px 18px;
      border-radius: 14px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border-subtle);
      cursor: pointer;
      transition: all 0.28s var(--ease-spring);
    }

    .persona-link-card:hover {
      background: var(--bg-card-hover);
      border-color: var(--dept-accent);
      transform: translateX(5px);
      box-shadow: 0 10px 24px rgba(0, 0, 0, 0.35);
    }

    .persona-link-left {
      display: flex;
      align-items: center;
      gap: 14px;
      min-width: 0;
    }

    .persona-emoji {
      width: 46px;
      height: 46px;
      border-radius: 12px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.11);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      flex-shrink: 0;
    }

    .persona-link-name {
      font-family: var(--font-display);
      font-size: 17px;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.28;
    }

    .persona-link-role {
      font-size: 14px;
      color: #e2e8f0;
      margin-top: 2px;
      line-height: 1.45;
    }

    .persona-open-arrow {
      font-size: 14px;
      font-weight: 700;
      color: var(--dept-accent);
      white-space: nowrap;
      flex-shrink: 0;
    }

    /* =========================================================================
       PAGE 2–6: WIDER SUBPAGE CONTAINER (1580PX / 92VW) FOR BETTER READABILITY
       ========================================================================= */
    .subpage-container {
      max-width: 1580px;
      width: 92vw;
      margin: 0 auto;
      padding: 108px 20px 116px;
    }

    @media (max-width: 760px) {
      .subpage-container {
        width: 95vw;
        padding: 124px 14px 96px;
      }
    }

    .back-bar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      margin-bottom: 30px;
    }

    .back-btn {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 10px 22px;
      border-radius: 999px;
      background: var(--bg-surface);
      border: 1px solid var(--border-strong);
      font-size: 14.5px;
      font-weight: 600;
      color: var(--text-primary);
      transition: all 0.28s var(--ease-spring);
    }

    .back-btn:hover {
      background: var(--bg-card-hover);
      border-color: var(--sc-cyan);
      transform: translateX(-3px);
    }

    .twin-input-field {
      width: 100%;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.16);
      border-radius: 12px;
      padding: 12px 16px;
      color: #ffffff;
      font-family: var(--font-sans);
      font-size: 14px;
      outline: none;
      transition: all 0.2s ease;
      box-sizing: border-box;
    }
    .twin-input-field:focus {
      border-color: #a855f7;
      box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.25);
      background: rgba(15, 23, 42, 0.98);
    }
    .twin-input-field option {
      background: #090d18;
      color: #ffffff;
    }
    .btn-generate-twin:hover {
      transform: translateY(-2px);
      box-shadow: 0 12px 30px rgba(168, 85, 247, 0.5) !important;
    }
    .btn-generate-twin:active {
      transform: translateY(0);
    }
    .twin-preset-card {
      transition: all 0.2s ease;
    }
    .twin-preset-card:hover {
      border-color: var(--sc-cyan) !important;
      transform: translateY(-2px);
      background: rgba(255, 255, 255, 0.08) !important;
    }

    .persona-switcher-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .switch-pill {
      padding: 8px 16px;
      border-radius: 999px;
      font-size: 14px;
      font-weight: 600;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      white-space: nowrap;
      transition: all 0.26s var(--ease-spring);
    }

    .switch-pill:hover {
      color: var(--text-primary);
      border-color: var(--border-strong);
      background: var(--bg-card-hover);
      transform: translateY(-1px);
    }

    .switch-pill.active {
      color: #ffffff;
      background: var(--g-blue);
      border-color: var(--g-blue);
    }

    .persona-header-card {
      position: relative;
      padding: 40px 44px;
      border-radius: 24px;
      background:
        radial-gradient(circle 420px at 88% 24%, rgba(0, 210, 255, 0.12), transparent 72%),
        linear-gradient(155deg, #090e1a 0%, #050811 100%);
      border: 1px solid var(--border-strong);
      box-shadow: 0 22px 56px rgba(0, 0, 0, 0.52), inset 0 1px 0 rgba(255, 255, 255, 0.08);
      margin-bottom: 36px;
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      align-items: center;
      gap: 36px;
      overflow: hidden;
    }

    @media (max-width: 900px) {
      .persona-header-card {
        grid-template-columns: 1fr;
        padding: 28px 24px;
      }
    }

    /* Subtle non-competing watermark placement in headers */
    .persona-header-sc-watermark {
      position: absolute;
      right: 180px;
      bottom: -24px;
      width: 400px;
      height: 255px;
      opacity: 0.28;
      pointer-events: none;
      z-index: 1;
      -webkit-mask-image: radial-gradient(ellipse 75% 75% at 60% 60%, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0) 84%);
      mask-image: radial-gradient(ellipse 75% 75% at 60% 60%, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0) 84%);
    }

    /* 4-Layer Agentic Reference Architecture Strip on Agent & Value Chain Pages */
    .arch-layer-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
      margin-top: 18px;
    }

    @media (max-width: 980px) {
      .arch-layer-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 600px) {
      .arch-layer-grid { grid-template-columns: 1fr; }
    }

    .arch-layer-card {
      padding: 26px 26px;
      border-radius: 18px;
      background: rgba(11, 16, 28, 0.94);
      border: 1px solid var(--border-subtle);
      border-top: 3px solid var(--layer-color, var(--g-blue));
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .arch-layer-num {
      font-size: 12.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    .arch-layer-title {
      font-family: var(--font-display);
      font-size: 19.5px;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.3;
    }

    .arch-layer-desc {
      font-size: 16px;
      color: #f1f5f9;
      line-height: 1.64;
    }

    .persona-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 15px;
      border-radius: 999px;
      font-size: 13.5px;
      font-weight: 700;
      letter-spacing: 0.01em;
      margin-bottom: 14px;
    }

    .persona-page-title {
      font-family: var(--font-display);
      font-size: clamp(30px, 3.6vw, 46px);
      font-weight: 800;
      letter-spacing: -0.025em;
      line-height: 1.14;
      color: #ffffff;
      margin-bottom: 12px;
    }

    .persona-page-summary {
      font-size: 18.5px;
      color: #f1f5f9;
      max-width: 1120px;
      line-height: 1.68;
    }

    .persona-focus-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 18px;
    }

    .focus-pill {
      padding: 8px 16px;
      border-radius: 10px;
      background: rgba(19, 27, 44, 0.94);
      border: 1px solid rgba(56, 189, 248, 0.28);
      font-size: 14px;
      font-weight: 600;
      color: #ffffff;
    }

    .persona-stat-highlight {
      position: relative;
      z-index: 2;
      padding: 26px 30px;
      border-radius: 20px;
      background: rgba(15, 22, 36, 0.94);
      backdrop-filter: blur(14px);
      border: 1px solid var(--border-strong);
      text-align: center;
      min-width: 245px;
      max-width: 295px;
    }

    .persona-stat-value {
      font-family: var(--font-display);
      font-size: 40px;
      font-weight: 800;
      line-height: 1.1;
      margin-bottom: 6px;
      font-variant-numeric: tabular-nums;
    }

    .persona-stat-label {
      font-size: 14.5px;
      font-weight: 600;
      color: #e2e8f0;
      line-height: 1.48;
    }

    /* =========================================================================
       REALISTIC DAY IN THE LIFE SCHEDULE (WITH COLOR-CODED MANUAL TOIL)
       ========================================================================= */
    .ditl-header-row {
      display: flex;
      flex-wrap: wrap;
      align-items: flex-end;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 24px;
    }

    .block-title {
      font-family: var(--font-display);
      font-size: clamp(25px, 2.8vw, 32px);
      font-weight: 800;
      letter-spacing: -0.022em;
      color: #ffffff;
      margin-bottom: 8px;
      padding-left: 14px;
      border-left: 4px solid var(--sc-cyan);
      line-height: 1.22;
    }

    .block-subtitle {
      font-size: 17.5px;
      color: #e2e8f0;
      line-height: 1.65;
      max-width: 1180px;
    }

    .ditl-legend {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 16px;
      padding: 10px 18px;
      border-radius: 999px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      font-size: 14px;
    }

    .legend-item {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      color: var(--text-secondary);
      font-weight: 600;
    }

    .legend-swatch {
      width: 10px;
      height: 10px;
      border-radius: 3px;
    }

    .time-shift-banner {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 28px;
    }

    @media (max-width: 780px) {
      .time-shift-banner { grid-template-columns: 1fr; }
    }

    .shift-meter-card {
      padding: 20px 24px;
      border-radius: 16px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .shift-meter-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      font-size: 15.5px;
      font-weight: 600;
    }

    .shift-bar-track {
      height: 10px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.08);
      overflow: hidden;
      display: flex;
    }

    .day-schedule {
      display: flex;
      flex-direction: column;
      gap: 16px;
      margin-bottom: 68px;
    }

    .schedule-row-human {
      display: grid;
      grid-template-columns: 225px minmax(0, 1fr);
      gap: 24px;
      align-items: center;
      padding: 20px 26px;
      border-radius: 18px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--border-subtle);
      transition: border-color 0.25s ease, background 0.25s ease;
    }

    .schedule-row-human:hover {
      border-color: var(--border-strong);
      background: rgba(255, 255, 255, 0.05);
    }

    .schedule-row-toil {
      display: grid;
      grid-template-columns: 225px minmax(0, 1fr) minmax(0, 1.18fr);
      gap: 22px;
      align-items: stretch;
      padding: 24px 26px;
      border-radius: 18px;
      background: var(--bg-surface);
      border: 1px solid rgba(234, 67, 53, 0.34);
      box-shadow: inset 4px 0 0 var(--g-red);
      transition: transform 0.28s var(--ease-spring), border-color 0.28s ease;
    }

    .schedule-row-toil:hover {
      border-color: rgba(234, 67, 53, 0.55);
    }

    @media (max-width: 980px) {
      .schedule-row-human,
      .schedule-row-toil {
        grid-template-columns: 1fr;
      }
    }

    .slot-time-col {
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 6px;
    }

    .slot-clock {
      font-family: var(--font-display);
      font-size: 18px;
      font-weight: 800;
      color: #ffffff;
      font-variant-numeric: tabular-nums;
    }

    .slot-title {
      font-size: 16.5px;
      font-weight: 700;
      color: #ffffff;
      line-height: 1.42;
    }

    .human-task-box {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
    }

    .human-task-desc {
      font-size: 16.5px;
      color: #f8fafc;
      line-height: 1.62;
    }

    .human-pill {
      padding: 6px 14px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.08);
      color: #ffffff;
      font-size: 13px;
      font-weight: 600;
      white-space: nowrap;
    }

    .toil-highlight-box {
      padding: 20px 22px;
      border-radius: 14px;
      background: rgba(234, 67, 53, 0.11);
      border: 1px solid rgba(234, 67, 53, 0.38);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 12px;
    }

    .toil-top-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      padding-bottom: 8px;
      border-bottom: 1px solid rgba(234, 67, 53, 0.24);
    }

    .toil-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      color: #ff8a80;
    }

    .toil-duration {
      font-size: 13.5px;
      font-weight: 800;
      padding: 3px 10px;
      border-radius: 6px;
      background: rgba(234, 67, 53, 0.25);
      color: #ff8a80;
      font-variant-numeric: tabular-nums;
    }

    .toil-text {
      font-size: 16.5px;
      color: #ffffff;
      line-height: 1.65;
    }

    .gemini-improve-box {
      padding: 20px 22px;
      border-radius: 14px;
      background: rgba(52, 168, 83, 0.11);
      border: 1px solid rgba(52, 168, 83, 0.4);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 12px;
    }

    .improve-top-bar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      padding-bottom: 8px;
      border-bottom: 1px solid rgba(52, 168, 83, 0.24);
    }

    .improve-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      color: #81c995;
    }

    .improve-badge img {
      width: 14px;
      height: 14px;
    }

    .improve-time-saved {
      font-size: 13.5px;
      font-weight: 800;
      padding: 3px 10px;
      border-radius: 6px;
      background: rgba(52, 168, 83, 0.25);
      color: #81c995;
      font-variant-numeric: tabular-nums;
    }

    .improve-text {
      font-size: 16.5px;
      color: #ffffff;
      line-height: 1.65;
    }

    .plugin-agent-btn {
      display: inline-flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      width: 100%;
      padding: 11px 16px;
      border-radius: 10px;
      background: rgba(66, 133, 244, 0.18);
      border: 1px solid rgba(66, 133, 244, 0.48);
      color: #bfdbfe;
      font-size: 14.5px;
      font-weight: 700;
      transition: all 0.26s var(--ease-spring);
    }

    .plugin-agent-btn:hover {
      background: var(--g-blue);
      color: #ffffff;
      transform: translateY(-1px);
    }

    /* =========================================================================
       AGENT CATALOGUE CARDS (ON PERSONA PAGE)
       ========================================================================= */
    .catalog-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      margin-top: 22px;
    }

    @media (max-width: 980px) {
      .catalog-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 640px) {
      .catalog-grid { grid-template-columns: 1fr; }
    }

    .catalog-card {
      border-radius: 22px;
      background: linear-gradient(165deg, rgba(15, 22, 36, 0.96) 0%, rgba(9, 14, 24, 0.99) 100%);
      border: 1px solid var(--border-subtle);
      overflow: hidden;
      cursor: pointer;
      transition: transform 0.34s var(--ease-spring), border-color 0.28s ease, box-shadow 0.34s var(--ease-spring), background 0.28s ease;
      display: flex;
      flex-direction: column;
    }

    .catalog-card:hover {
      transform: translateY(-6px);
      border-color: var(--border-strong);
      background: var(--bg-card-hover);
      box-shadow: 0 22px 48px rgba(0, 0, 0, 0.58);
    }

    .catalog-thumb {
      position: relative;
      height: 172px;
      background: radial-gradient(ellipse at 50% 50%, #0b1528 0%, #050811 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      border-bottom: 1px solid var(--border-subtle);
    }

    .play-circle {
      position: absolute;
      right: 16px;
      bottom: 14px;
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: rgba(4, 6, 10, 0.85);
      border: 1px solid var(--border-strong);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      z-index: 3;
      transition: transform 0.28s var(--ease-spring), background 0.25s ease;
    }

    .catalog-card:hover .play-circle {
      transform: scale(1.12);
      background: var(--g-blue);
      border-color: var(--g-blue);
    }

    .catalog-body {
      padding: 24px;
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 18px;
    }

    .catalog-title {
      font-family: var(--font-display);
      font-size: 21px;
      font-weight: 800;
      letter-spacing: -0.018em;
      color: #ffffff;
      line-height: 1.28;
      margin-bottom: 8px;
    }

    .catalog-desc {
      font-size: 16px;
      color: #f1f5f9;
      line-height: 1.64;
    }

    .catalog-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      font-size: 14.5px;
      font-weight: 700;
      padding-top: 14px;
      border-top: 1px solid var(--border-subtle);
    }

    /* =========================================================================
       PAGE 3: DEDICATED AGENT DEMO PAGE — BIG EXECUTIVE PITCH CARDS
       ========================================================================= */
    .agent-hero-banner {
      position: relative;
      padding: 40px 44px;
      border-radius: 24px;
      background:
        radial-gradient(circle 420px at 86% 24%, rgba(0, 210, 255, 0.12), transparent 72%),
        linear-gradient(155deg, #090e1a 0%, #050811 100%);
      border: 1px solid var(--border-strong);
      box-shadow: 0 22px 54px rgba(0, 0, 0, 0.52), inset 0 1px 0 rgba(255, 255, 255, 0.08);
      margin-bottom: 28px;
      overflow: hidden;
    }

    .agent-title {
      position: relative;
      z-index: 2;
      font-family: var(--font-display);
      font-size: clamp(32px, 3.8vw, 48px);
      font-weight: 800;
      letter-spacing: -0.025em;
      line-height: 1.14;
      color: #ffffff;
      margin-bottom: 14px;
    }

    .agent-subtitle {
      position: relative;
      z-index: 2;
      font-size: 19px;
      color: #f1f5f9;
      max-width: 1180px;
      line-height: 1.68;
    }

    /* HERO-SIZED EXECUTIVE PITCH CARDS: Business Problem, Executive Solution, Bottom-Line Outcome */
    .exec-pitch-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 24px;
      margin-bottom: 34px;
    }

    @media (max-width: 1040px) {
      .exec-pitch-grid { grid-template-columns: 1fr; }
    }

    .exec-pitch-card {
      position: relative;
      padding: 34px 32px;
      border-radius: 22px;
      background: linear-gradient(165deg, rgba(16, 24, 42, 0.98) 0%, rgba(9, 14, 26, 0.99) 100%);
      border: 1px solid rgba(255, 255, 255, 0.16);
      border-top: 5px solid var(--pitch-accent, var(--g-blue));
      box-shadow: 0 18px 44px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.09);
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      gap: 14px;
      transition: transform 0.32s var(--ease-spring), box-shadow 0.32s var(--ease-spring), border-color 0.28s ease;
    }

    .exec-pitch-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 24px 54px rgba(0, 0, 0, 0.65);
    }

    .exec-pitch-badge,
    .exec-pitch-eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      border-radius: 999px;
      font-size: 12.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      width: fit-content;
      margin-bottom: 4px;
    }

    .exec-pitch-heading,
    .exec-pitch-title {
      font-family: var(--font-display);
      font-size: 23.5px;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: #ffffff;
      line-height: 1.24;
      margin-bottom: 6px;
      padding-bottom: 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
    }

    .exec-pitch-text,
    .exec-pitch-body {
      font-size: 17.5px;
      font-weight: 500;
      color: #f8fafc;
      line-height: 1.68;
    }

    .exec-pitch-proof {
      margin-top: auto;
      padding: 15px 18px;
      border-radius: 14px;
      background: rgba(16, 185, 129, 0.13);
      border: 1px solid rgba(16, 185, 129, 0.42);
      font-size: 15.5px;
      color: #ecfdf5;
      line-height: 1.6;
    }

    .video-stage-box {
      border-radius: 24px;
      background: #03060c;
      border: 1px solid var(--border-strong);
      overflow: hidden;
      margin-bottom: 34px;
      box-shadow: 0 26px 68px rgba(0, 0, 0, 0.58);
    }

    .video-viewport {
      width: 100%;
      min-height: 420px;
      background: #03060c;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      position: relative;
      overflow: hidden;
    }

    .video-viewport video {
      width: 100%;
      max-height: 560px;
      object-fit: contain;
      background: #000;
      position: relative;
      z-index: 2;
    }

    .video-toolbar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 14px 24px;
      background: var(--bg-surface);
      border-top: 1px solid var(--border-subtle);
      font-size: 14px;
      color: var(--text-secondary);
    }

    .upload-video-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 16px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.07);
      border: 1px solid var(--border-strong);
      color: #ffffff;
      font-size: 13.5px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.25s var(--ease-spring);
    }

    .upload-video-btn:hover, .upload-video-btn.active {
      background: var(--g-blue);
      border-color: var(--g-blue);
      transform: translateY(-1px);
    }

    .agent-details-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 22px;
    }

    @media (max-width: 900px) {
      .agent-details-grid { grid-template-columns: 1fr; }
    }

    .detail-card {
      padding: 28px;
      border-radius: 20px;
      background: linear-gradient(165deg, rgba(15, 22, 36, 0.96) 0%, rgba(9, 14, 24, 0.99) 100%);
      border: 1px solid var(--border-subtle);
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.06);
    }

    .detail-card-label {
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      color: var(--text-secondary);
      margin-bottom: 12px;
    }

    .detail-card-text {
      font-size: 17px;
      color: #f8fafc;
      line-height: 1.64;
    }

    /* =========================================================================
       END-TO-END VALUE CHAINS (F2F & O2D ENTRY CARDS + DEDICATED PIPELINE PAGE)
       ========================================================================= */
    .vc-home-block {
      margin-top: 64px;
      padding-top: 52px;
      border-top: 1px solid var(--border-subtle);
    }

    .vc-entry-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 24px;
      width: 100%;
    }

    @media (max-width: 860px) {
      .vc-entry-grid { grid-template-columns: 1fr; }
    }

    .vc-entry-card {
      position: relative;
      padding: 28px 26px 22px;
      border-radius: 22px;
      background: linear-gradient(165deg, rgba(16, 23, 38, 0.96) 0%, rgba(10, 14, 24, 0.99) 100%);
      border: 1px solid rgba(255, 255, 255, 0.11);
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.06);
      cursor: pointer;
      transition: transform 0.34s var(--ease-spring), border-color 0.28s ease, box-shadow 0.34s var(--ease-spring), background 0.28s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 16px;
      min-height: 280px;
      overflow: hidden;
    }

    .vc-entry-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 24px;
      right: 24px;
      height: 3px;
      border-radius: 0 0 4px 4px;
      background: var(--vc-accent);
      opacity: 0.78;
      transition: opacity 0.25s ease, left 0.32s var(--ease-spring), right 0.32s var(--ease-spring);
    }

    .vc-entry-card:hover {
      background: var(--bg-card-hover);
      transform: translateY(-5px);
      border-color: var(--vc-accent, var(--border-strong));
      box-shadow: 0 20px 48px rgba(0, 0, 0, 0.54);
    }

    .vc-entry-card:hover::before {
      opacity: 1;
      left: 0;
      right: 0;
      border-radius: 22px 22px 0 0;
    }

    .vc-flow-badge {
      position: relative;
      z-index: 2;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 5px 12px;
      border-radius: 999px;
      font-size: 12.5px;
      font-weight: 600;
      width: fit-content;
      margin-bottom: 12px;
    }

    .vc-stage-row {
      display: grid;
      grid-template-columns: 240px minmax(0, 1fr) minmax(0, 1.25fr);
      gap: 18px;
      align-items: stretch;
      padding: 22px 24px;
      border-radius: 18px;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      box-shadow: inset 4px 0 0 var(--vc-stage-color, var(--g-blue));
    }

    @media (max-width: 980px) {
      .vc-stage-row { grid-template-columns: 1fr; }
    }

    .vc-stage-meta {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 10px;
    }

    .vc-stage-num {
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.07em;
    }

    .vc-stage-name {
      font-family: var(--font-display);
      font-size: 18px;
      font-weight: 700;
      color: #ffffff;
      line-height: 1.32;
    }

    .vc-modality-row {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }

    .vc-modality-pill {
      padding: 4px 10px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 500;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border-subtle);
      color: var(--text-primary);
    }

    .vc-owner-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 13.5px;
      font-weight: 600;
      color: var(--text-secondary);
      width: fit-content;
      transition: color 0.2s ease, transform 0.2s ease;
    }

    .vc-owner-btn:hover {
      color: #ffffff;
      transform: translateX(3px);
    }

    .vc-golden-thread {
      padding: 11px 14px;
      border-radius: 10px;
      background: rgba(66, 133, 244, 0.12);
      border: 1px solid rgba(66, 133, 244, 0.36);
      font-size: 14px;
      color: #f8fafc;
      line-height: 1.52;
    }

    .vc-golden-label {
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #93c5fd;
      margin-bottom: 3px;
    }

    .persona-vc-banner {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 18px 24px;
      border-radius: 18px;
      background: rgba(16, 22, 35, 0.92);
      border: 1px solid var(--border-strong);
      margin-bottom: 36px;
      cursor: pointer;
      transition: all 0.28s var(--ease-spring);
    }

    .persona-vc-banner:hover {
      background: var(--bg-card-hover);
      border-color: var(--g-blue);
      transform: translateY(-2px);
    }

    /* Interactive CAD Controls inside Agent / ValueChain Stage Box */
    .cad-bar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      width: 100%;
      padding: 14px 20px;
      background: #070b14;
      border-bottom: 1px solid var(--border-subtle);
      font-size: 13.5px;
    }

    .cad-pill-btn {
      padding: 7px 14px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border-subtle);
      font-size: 12.5px;
      font-weight: 500;
      color: var(--text-secondary);
      transition: all 0.24s var(--ease-spring);
    }

    .cad-pill-btn:hover {
      color: var(--text-primary);
      background: rgba(255, 255, 255, 0.11);
    }

    .cad-pill-btn.active {
      background: var(--g-blue);
      border-color: var(--g-blue);
      color: #fff;
      box-shadow: 0 4px 14px rgba(66, 133, 244, 0.35);
    }

    /* =========================================================================
       SMOOTH DROPDOWN UNROLL DRAWERS, DIRECTORY & ARCHITECTURE
       ========================================================================= */
    .nav-csco-badge {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      padding: 5px 12px;
      border-radius: 999px;
      background: rgba(0, 210, 255, 0.09);
      border: 1px solid rgba(0, 210, 255, 0.28);
      font-size: 12.5px;
      font-weight: 500;
      color: #e2e8f0;
      letter-spacing: 0.01em;
    }

    .nav-csco-badge::before {
      content: '';
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--sc-cyan);
      box-shadow: 0 0 8px var(--sc-cyan);
    }

    /* Navbar Smooth Dropdown Menu */
    .nav-dropdown-wrap {
      position: relative;
      display: inline-block;
    }

    .nav-dropdown-menu {
      position: absolute;
      top: calc(100% + 8px);
      right: 0;
      min-width: 280px;
      padding: 10px;
      border-radius: 16px;
      background: rgba(11, 15, 24, 0.97);
      backdrop-filter: blur(22px);
      border: 1px solid var(--border-strong);
      box-shadow: 0 22px 54px rgba(0, 0, 0, 0.78);
      display: none;
      flex-direction: column;
      gap: 4px;
      z-index: 200;
      animation: dropdownUnroll 0.26s var(--ease-spring) forwards;
    }

    .nav-dropdown-wrap:hover .nav-dropdown-menu,
    .nav-dropdown-wrap.open .nav-dropdown-menu {
      display: flex;
    }

    .nav-dropdown-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 10px 14px;
      border-radius: 11px;
      text-align: left;
      font-size: 13.5px;
      color: var(--text-primary);
      transition: background 0.18s ease, transform 0.18s ease;
    }

    .nav-dropdown-item:hover {
      background: rgba(255, 255, 255, 0.08);
      transform: translateX(2px);
    }

    /* Smooth Collapsible / Expandable Dropdown Drawers (True Dropdown Unroll Effect) */
    .sc-dropdown-block {
      margin-top: 16px;
      border-radius: 16px;
      background: rgba(8, 12, 22, 0.90);
      border: 1px solid var(--border-subtle);
      overflow: hidden;
      transition: border-color 0.28s ease, box-shadow 0.28s ease;
    }

    .sc-dropdown-block.open {
      border-color: var(--sc-cyan);
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45);
    }

    .sc-dropdown-btn {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 15px 20px;
      font-size: 14.5px;
      font-weight: 600;
      color: var(--text-primary);
      background: rgba(255, 255, 255, 0.03);
      transition: background 0.22s ease;
      text-align: left;
    }

    .sc-dropdown-btn:hover {
      background: rgba(255, 255, 255, 0.07);
    }

    .sc-dropdown-chevron {
      font-size: 13px;
      color: var(--text-secondary);
      transition: transform 0.34s var(--ease-spring);
    }

    .sc-dropdown-block.open .sc-dropdown-chevron {
      transform: rotate(180deg);
      color: var(--sc-cyan);
    }

    .sc-dropdown-body {
      display: none;
      padding: 20px 22px;
      border-top: 1px solid var(--border-subtle);
      animation: dropdownUnroll 0.34s var(--ease-spring) forwards;
    }

    .sc-dropdown-block.open .sc-dropdown-body {
      display: block;
    }

    .sc-dropdown-inner {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    /* Personas & Agents Directory Tab (#pageDirectory) */
    .dir-controls-bar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 20px 24px;
      border-radius: 20px;
      background: var(--bg-surface);
      border: 1px solid var(--border-strong);
      margin-bottom: 36px;
    }

    .dir-search-input {
      flex: 1;
      min-width: 260px;
      padding: 13px 18px;
      border-radius: 12px;
      background: rgba(4, 6, 10, 0.92);
      border: 1px solid var(--border-strong);
      color: var(--text-primary);
      font-size: 15px;
      outline: none;
      transition: border-color 0.22s ease, box-shadow 0.22s ease;
    }

    .dir-search-input:focus {
      border-color: var(--sc-cyan);
      box-shadow: 0 0 0 3px rgba(0, 210, 255, 0.16);
    }

    .dir-dept-section {
      margin-bottom: 48px;
    }

    .dir-dept-header {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding-bottom: 14px;
      margin-bottom: 20px;
      border-bottom: 1px solid var(--border-subtle);
    }

    .dir-persona-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 22px;
    }

    @media (max-width: 920px) {
      .dir-persona-grid { grid-template-columns: 1fr; }
    }

    .dir-persona-card {
      padding: 26px;
      border-radius: 20px;
      background: linear-gradient(165deg, rgba(15, 22, 36, 0.96) 0%, rgba(9, 14, 24, 0.99) 100%);
      border: 1px solid var(--border-subtle);
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 16px;
      transition: border-color 0.28s ease, transform 0.32s var(--ease-spring), box-shadow 0.32s var(--ease-spring);
    }

    .dir-persona-card:hover {
      border-color: var(--dept-accent, var(--border-strong));
      transform: translateY(-4px);
      box-shadow: 0 18px 40px rgba(0, 0, 0, 0.48);
    }

    .dir-card-top {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
    }

    .dir-card-person {
      display: flex;
      align-items: flex-start;
      gap: 14px;
      min-width: 0;
    }

    .dir-agent-chip-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-top: 6px;
    }

    .dir-agent-launch-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 14px 18px;
      border-radius: 12px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border-subtle);
      cursor: pointer;
      transition: all 0.24s var(--ease-spring);
    }

    .dir-agent-launch-row:hover {
      background: rgba(0, 210, 255, 0.12);
      border-color: var(--sc-cyan);
      transform: translateX(3px);
    }

    /* Interactive Per-Agent Architecture Diagram Box */
    .agent-arch-box {
      margin-top: 28px;
      padding: 30px;
      border-radius: 22px;
      background: #070b13;
      border: 1px solid var(--border-strong);
    }

    .subagent-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-top: 16px;
    }

    @media (max-width: 860px) {
      .subagent-grid { grid-template-columns: 1fr; }
    }

    .subagent-card {
      padding: 20px 22px;
      border-radius: 16px;
      background: rgba(16, 22, 35, 0.94);
      border: 1px solid var(--border-subtle);
      transition: border-color 0.25s ease, transform 0.28s var(--ease-spring);
    }

    .subagent-card:hover {
      border-color: var(--border-strong);
      transform: translateY(-2px);
    }

    .subagent-tag {
      font-size: 11.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 6px;
    }

    .subagent-name {
      font-family: var(--font-display);
      font-size: 18px;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 6px;
    }

    .subagent-role {
      font-size: 15px;
      color: #e2e8f0;
      line-height: 1.56;
    }

    .sc-tech-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .sc-tech-pill {
      padding: 5px 12px;
      border-radius: 999px;
      font-size: 12.5px;
      font-weight: 500;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border-subtle);
      color: #e2e8f0;
    }

    /* =========================================================================
       EXECUTIVE SELLING KPI CARDS ON AGENT FRONT PAGE (NUMBERS, ROI, GROWTH)
       ========================================================================= */
    .agent-roi-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
      margin-bottom: 28px;
    }

    @media (max-width: 980px) {
      .agent-roi-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 560px) {
      .agent-roi-grid { grid-template-columns: 1fr; }
    }

    .agent-roi-card {
      padding: 24px 24px;
      border-radius: 20px;
      background: linear-gradient(160deg, rgba(16, 23, 38, 0.96) 0%, rgba(8, 12, 22, 0.98) 100%);
      border: 1px solid var(--border-strong);
      border-top: 3px solid var(--roi-accent, var(--sc-cyan));
      box-shadow: 0 14px 34px rgba(0, 0, 0, 0.42);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 8px;
      transition: transform 0.32s var(--ease-spring), box-shadow 0.32s var(--ease-spring);
    }

    .agent-roi-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 20px 44px rgba(0, 0, 0, 0.56);
    }

    .agent-roi-val {
      font-family: var(--font-display);
      font-size: clamp(26px, 2.5vw, 34px);
      font-weight: 700;
      line-height: 1.12;
      letter-spacing: -0.02em;
      font-variant-numeric: tabular-nums;
    }

    .agent-roi-label {
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #f8fafc;
    }

    .agent-roi-sub {
      font-size: 14px;
      color: var(--text-secondary);
      line-height: 1.48;
    }

    /* Cross-Persona Universal Agents Banner on CSCO Org Chart */
    .universal-agents-banner {
      margin-top: 36px;
      padding: 30px 32px;
      border-radius: 24px;
      background: linear-gradient(135deg, rgba(10, 17, 32, 0.96) 0%, rgba(18, 14, 36, 0.96) 100%);
      border: 1px solid rgba(56, 189, 248, 0.36);
      box-shadow: 0 22px 56px rgba(0, 0, 0, 0.52), inset 0 1px 0 rgba(255, 255, 255, 0.08);
    }

    .universal-agents-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-top: 20px;
    }

    @media (max-width: 1080px) {
      .universal-agents-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 600px) {
      .universal-agents-grid { grid-template-columns: 1fr; }
    }

    .universal-agent-card {
      padding: 22px;
      border-radius: 18px;
      background: linear-gradient(165deg, rgba(16, 24, 40, 0.94) 0%, rgba(10, 15, 26, 0.98) 100%);
      border: 1px solid var(--border-subtle);
      cursor: pointer;
      transition: transform 0.34s var(--ease-spring), border-color 0.28s ease, box-shadow 0.34s var(--ease-spring), background 0.28s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 14px;
    }

    .universal-agent-card:hover {
      transform: translateY(-5px);
      background: var(--bg-card-hover);
      border-color: var(--sc-cyan);
      box-shadow: 0 18px 40px rgba(0, 210, 255, 0.18);
    }

    .universal-agent-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 999px;
      background: rgba(56, 189, 248, 0.14);
      border: 1px solid rgba(56, 189, 248, 0.38);
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.07em;
      color: #38bdf8;
      margin-bottom: 10px;
    }

    .universal-agent-name {
      font-family: var(--font-display);
      font-size: 18.5px;
      font-weight: 700;
      letter-spacing: -0.012em;
      color: #ffffff;
      line-height: 1.3;
      margin-bottom: 8px;
    }

    .universal-agent-desc {
      font-size: 14.5px;
      color: #e2e8f0;
      line-height: 1.56;
    }

    .universal-agent-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      padding-top: 12px;
      border-top: 1px solid rgba(255, 255, 255, 0.07);
      font-size: 13.5px;
      font-weight: 600;
      color: #38bdf8;
    }

    .used-by-strip {
      margin-top: 28px;
      padding: 20px 24px;
      border-radius: 18px;
      background: rgba(9, 13, 24, 0.85);
      border: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .used-by-pills {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
    }

    .used-by-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 15px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-strong);
      font-size: 13.5px;
      font-weight: 500;
      color: #f8fafc;
      cursor: pointer;
      transition: all 0.26s var(--ease-spring);
    }

    .used-by-pill:hover {
      background: rgba(0, 210, 255, 0.15);
      border-color: var(--sc-cyan);
      transform: translateY(-2px);
    }

    .blueprint-cta-banner {
      margin-top: 28px;
      padding: 28px 32px;
      border-radius: 22px;
      background: linear-gradient(135deg, rgba(16, 24, 44, 0.97) 0%, rgba(28, 18, 52, 0.97) 100%);
      border: 1px solid rgba(168, 85, 247, 0.45);
      box-shadow: 0 20px 52px rgba(0, 0, 0, 0.48);
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 24px;
    }

    .cta-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      padding: 15px 26px;
      border-radius: 999px;
      font-size: 15px;
      font-weight: 700;
      white-space: nowrap;
      box-shadow: 0 12px 32px rgba(168, 85, 247, 0.35);
      transition: transform 0.3s var(--ease-spring), box-shadow 0.3s var(--ease-spring);
    }

    .cta-btn:hover {
      transform: translateY(-3px) scale(1.015);
      box-shadow: 0 18px 42px rgba(0, 210, 255, 0.42);
    }

    /* =========================================================================
       AUTHORS ATTRIBUTION BADGE & GLOBAL FOOTER (ZUHAIB PARVEZ & SUMAN BANERJEE)
       ========================================================================= */
    .authors-credit-pill {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 8px 18px;
      border-radius: 999px;
      background: linear-gradient(135deg, rgba(0, 210, 255, 0.14) 0%, rgba(168, 85, 247, 0.16) 100%);
      border: 1px solid rgba(0, 210, 255, 0.42);
      color: #f8fafc;
      font-family: var(--font-display);
      font-size: 13.5px;
      font-weight: 700;
      letter-spacing: 0.02em;
      box-shadow: 0 8px 24px rgba(0, 210, 255, 0.16);
    }

    .authors-credit-pill strong {
      color: #7dd3fc;
      font-weight: 800;
      text-decoration: underline;
      text-decoration-color: rgba(0, 210, 255, 0.55);
      text-underline-offset: 3px;
    }

    .global-authors-footer {
      max-width: 1580px;
      width: 92vw;
      margin: 40px auto 36px;
      padding: 26px 32px;
      border-radius: 22px;
      background: linear-gradient(160deg, rgba(11, 17, 30, 0.96) 0%, rgba(6, 10, 18, 0.98) 100%);
      border: 1px solid rgba(255, 255, 255, 0.14);
      box-shadow: 0 18px 44px rgba(0, 0, 0, 0.48);
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
    }

    /* =========================================================================
       CLEAN, SPACIOUS PERIODIC TABLE OF AGENTS (#pagePeriodic & periodic_table.html)
       ========================================================================= */
    .pt-top-tabs {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
      padding: 18px 0 22px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      margin-bottom: 24px;
    }

    .pt-tab-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 18px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.14);
      color: #cbd5e1;
      font-family: var(--font-sans);
      font-size: 14px;
      font-weight: 600;
      transition: all 0.25s var(--ease-spring);
    }

    .pt-tab-btn:hover {
      background: rgba(255, 255, 255, 0.09);
      color: #ffffff;
      transform: translateY(-1px);
    }

    .pt-tab-btn.active {
      background: #1d4ed8;
      border-color: #3b82f6;
      color: #ffffff;
      box-shadow: 0 6px 20px rgba(59, 130, 246, 0.35);
    }

    .pt-tab-count {
      font-size: 12px;
      font-weight: 500;
      opacity: 0.72;
    }

    .pt-subheader-bar {
      display: flex;
      flex-wrap: wrap;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 30px;
    }

    .pt-stat-badges {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .pt-stat-badge {
      padding: 7px 14px;
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.12);
      font-size: 13.5px;
      color: #cbd5e1;
    }

    .pt-stat-badge strong {
      color: #ffffff;
      font-weight: 700;
      margin-right: 4px;
    }

    /* 2-Column Main Periodic Layout: Left Domain Rows + Right Sticky Inspector & Legend */
    .pt-main-layout {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 340px;
      gap: 36px;
      align-items: start;
    }

    @media (max-width: 1100px) {
      .pt-main-layout {
        grid-template-columns: 1fr;
      }
    }

    .pt-domain-section {
      margin-bottom: 32px;
    }

    .pt-domain-heading {
      display: flex;
      align-items: center;
      gap: 9px;
      font-family: var(--font-sans);
      font-size: 12.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #cbd5e1;
      margin-bottom: 14px;
    }

    .pt-domain-swatch {
      width: 9px;
      height: 9px;
      border-radius: 2px;
      background: var(--dom-color, #38bdf8);
      box-shadow: 0 0 8px var(--dom-color, #38bdf8);
    }

    .pt-domain-count {
      color: #64748b;
      font-weight: 600;
      margin-left: 2px;
    }

    .pt-tiles-row {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(136px, 148px));
      gap: 12px;
    }

    @media (max-width: 640px) {
      .pt-tiles-row {
        grid-template-columns: repeat(2, 1fr);
      }
    }

    /* Minimalist Periodic Element Tile — Easy on the Eyes! */
    .pt-tile {
      position: relative;
      height: 92px;
      padding: 10px 12px 9px;
      border-radius: 12px;
      background: rgba(15, 23, 42, 0.78);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-top: 3px solid var(--tile-color, #38bdf8);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      text-align: center;
      cursor: pointer;
      user-select: none;
      transition: transform 0.28s var(--ease-spring), background 0.22s ease, border-color 0.22s ease, box-shadow 0.28s var(--ease-spring), opacity 0.22s ease;
    }

    .pt-tile:hover {
      transform: translateY(-4px);
      background: rgba(23, 35, 62, 0.95);
      border-color: var(--tile-color, #38bdf8);
      box-shadow: 0 12px 26px rgba(0, 0, 0, 0.45);
    }

    .pt-tile.active {
      background: rgba(28, 43, 75, 0.98);
      border-color: #ffffff;
      box-shadow: 0 0 0 1.5px var(--tile-color, #38bdf8), 0 14px 32px rgba(0, 0, 0, 0.55);
      transform: translateY(-3px);
    }

    .pt-tile.dimmed {
      opacity: 0.24;
    }

    .pt-tile-top {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      color: var(--tile-color, #38bdf8);
    }

    .pt-tile-trig {
      font-size: 11px;
      opacity: 0.78;
    }

    .pt-tile-title {
      font-family: var(--font-sans);
      font-size: 13px;
      font-weight: 700;
      color: #f8fafc;
      line-height: 1.22;
      max-width: 100%;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .pt-tile-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--dot-color, #38bdf8);
    }

    /* Smooth Animated Inline Expansion Card when a Tile is Clicked */
    @keyframes ptExpandIn {
      0% {
        opacity: 0;
        transform: translateY(-8px) scale(0.985);
      }
      100% {
        opacity: 1;
        transform: translateY(0) scale(1);
      }
    }

    .pt-inline-expand {
      margin-top: 16px;
      padding: 24px 26px;
      border-radius: 18px;
      background: linear-gradient(160deg, rgba(15, 23, 42, 0.97) 0%, rgba(9, 14, 26, 0.99) 100%);
      border: 1px solid var(--exp-color, #38bdf8);
      box-shadow: 0 20px 48px rgba(0, 0, 0, 0.52);
      animation: ptExpandIn 0.34s var(--ease-spring) forwards;
    }

    /* Right Sticky Sidebar: Preview Card + Legend */
    .pt-sidebar {
      position: sticky;
      top: 86px;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }

    .pt-side-card {
      padding: 22px 22px;
      border-radius: 16px;
      background: rgba(13, 20, 36, 0.92);
      border: 1px solid rgba(255, 255, 255, 0.13);
      box-shadow: 0 14px 36px rgba(0, 0, 0, 0.42);
      animation: ptExpandIn 0.28s var(--ease-spring) forwards;
    }

    .pt-side-badge {
      width: 38px;
      height: 38px;
      border-radius: 9px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 800;
      color: #ffffff;
      flex-shrink: 0;
    }

    .pt-side-tag {
      display: inline-flex;
      align-items: center;
      padding: 4px 10px;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.12);
      font-size: 11.5px;
      font-weight: 600;
      color: #cbd5e1;
    }

    .pt-legend-box {
      padding: 22px;
      border-radius: 16px;
      background: rgba(11, 17, 30, 0.78);
      border: 1px solid rgba(255, 255, 255, 0.1);
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .pt-legend-title {
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.09em;
      color: #64748b;
      margin-bottom: 10px;
    }

    .pt-legend-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
      font-size: 13px;
      color: #cbd5e1;
    }

    .pt-legend-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }

    /* =========================================================================
       CLEAN, PROGRESSIVE NEURAL MIND MAP & FLOWCHART (#pageMindMap)
       ========================================================================= */
    .mm-progressive-grid {
      display: grid;
      grid-template-columns: 270px 310px minmax(0, 1fr);
      gap: 22px;
      align-items: start;
      margin-bottom: 36px;
    }

    @media (max-width: 1120px) {
      .mm-progressive-grid {
        grid-template-columns: 1fr;
      }
    }

    .mm-col-card {
      padding: 20px;
      border-radius: 18px;
      background: rgba(11, 17, 30, 0.86);
      border: 1px solid rgba(255, 255, 255, 0.11);
    }

    .mm-col-header {
      font-size: 11.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #94a3b8;
      margin-bottom: 14px;
      padding-bottom: 10px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    .mm-node-btn {
      width: 100%;
      padding: 13px 15px;
      border-radius: 12px;
      background: rgba(17, 25, 42, 0.82);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-left: 3.5px solid var(--node-color, #38bdf8);
      text-align: left;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 9px;
      transition: all 0.25s var(--ease-spring);
    }

    .mm-node-btn:hover {
      background: rgba(26, 38, 64, 0.95);
      transform: translateX(3px);
      border-color: var(--node-color, #38bdf8);
    }

    .mm-node-btn.active {
      background: rgba(30, 46, 78, 0.98);
      border-color: #ffffff;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
      transform: translateX(4px);
    }

    .mm-flow-cards {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 18px;
      margin-bottom: 28px;
    }

    @media (max-width: 960px) {
      .mm-flow-cards {
        grid-template-columns: 1fr;
      }
    }

    .mm-flow-card {
      padding: 22px 24px;
      border-radius: 16px;
      background: rgba(13, 20, 36, 0.88);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-top: 3px solid var(--fc-color, #38bdf8);
      cursor: pointer;
      transition: all 0.28s var(--ease-spring);
    }

    .mm-flow-card:hover,
    .mm-flow-card.active {
      transform: translateY(-3px);
      background: rgba(20, 31, 56, 0.96);
      border-color: var(--fc-color, #38bdf8);
      box-shadow: 0 14px 32px rgba(0, 0, 0, 0.45);
    }
  </style>
</head>
<body>

  <!-- macOS Genie Curved Funnel Overlay -->
  <svg id="genieSvgOverlay" preserveAspectRatio="none">
    <defs>
      <linearGradient id="genieGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop id="genieStop1" offset="0%" stop-color="#00d2ff" stop-opacity="0.52" />
        <stop id="genieStop2" offset="50%" stop-color="#10b981" stop-opacity="0.38" />
        <stop id="genieStop3" offset="100%" stop-color="#ff8c00" stop-opacity="0.52" />
      </linearGradient>
    </defs>
    <path id="genieFunnelPath" fill="url(#genieGrad)" stroke="#00d2ff" stroke-width="1.8" d="" />
  </svg>

  <!-- =========================================================================
       TOP NAVIGATION BAR (SEAMLESS BRANDING + PERIODIC TABLE + NEURAL MIND MAP)
       ========================================================================= -->
  <header class="navbar">
    <div class="nav-brand" onclick="goHome()">
      <img data-asset="gemini_enterprise_dark.png" alt="Gemini Enterprise" class="gemini-logo" />
      <div class="nav-divider"></div>
      <span class="nav-csco-badge">Office of the CSCO · Supply Chain</span>
    </div>

    <div class="nav-right">
      <button type="button" class="nav-pill-btn" onclick="goHome()">Home</button>
      <button type="button" class="nav-pill-btn" onclick="goToOrgChart()">CSCO Org Chart (6)</button>
      <button type="button" class="nav-pill-btn" onclick="openPersonasDirectoryPage('all', '', true, 'personas')">Personas (26)</button>
      <button type="button" class="nav-pill-btn" onclick="openPersonasDirectoryPage('all', '', true, 'agents')">Agents Gallery (32)</button>
      <button type="button" class="nav-pill-btn" style="border-color:rgba(0,210,255,0.45); color:#7dd3fc; font-weight:700;" onclick="openPeriodicTablePage('all', null, true)">Periodic Table (32)</button>
      <button type="button" class="nav-pill-btn" style="border-color:rgba(16,185,129,0.45); color:#6ee7b7; font-weight:700;" onclick="openMindMapPage('all', null, true)">Neural Mind Map</button>
      <button type="button" class="nav-pill-btn" style="border-color:rgba(168,85,247,0.55); color:#d8b4fe; background:rgba(168,85,247,0.12); font-weight:700;" onclick="openEnterpriseTwinModal()">🪄 Client Twin</button>

      <!-- Smooth Dropdown for All 4 End-to-End Value Chains -->
      <div class="nav-dropdown-wrap" id="navVcDropdown">
        <button type="button" class="nav-pill-btn" onclick="document.getElementById('navVcDropdown').classList.toggle('open')">
          <span>Value Chains (4) &#9662;</span>
        </button>
        <div class="nav-dropdown-menu">
          <button type="button" class="nav-dropdown-item" onclick="openValueChainPage('f2f', true)">
            <span><strong style="color:#10b981;">F2F</strong> · Forecast-to-Fulfill</span>
            <span style="font-size:11px;color:var(--text-secondary);">6 Stages &rarr;</span>
          </button>
          <button type="button" class="nav-dropdown-item" onclick="openValueChainPage('o2d', true)">
            <span><strong style="color:#ff8c00;">O2D</strong> · Multi-Modal Order-to-Delivery</span>
            <span style="font-size:11px;color:var(--text-secondary);">Factory&rarr;Ship&rarr;Air&rarr;Truck &rarr;</span>
          </button>
          <button type="button" class="nav-dropdown-item" onclick="openValueChainPage('s2p', true)">
            <span><strong style="color:#a142f4;">S2P</strong> · Source-to-Pay Resilience</span>
            <span style="font-size:11px;color:var(--text-secondary);">6 Stages &rarr;</span>
          </button>
          <button type="button" class="nav-dropdown-item" onclick="openValueChainPage('p2r', true)">
            <span><strong style="color:#00d2ff;">P2R</strong> · Plan-to-Recovery Circular</span>
            <span style="font-size:11px;color:var(--text-secondary);">6 Stages &rarr;</span>
          </button>
        </div>
      </div>

      <button type="button" class="nav-pill-btn primary" onclick="openArchitecturePage(true)">Agent Architecture</button>
    </div>
  </header>

  <!-- =========================================================================
       PAGE 1: HOME PAGE (FULL-SCREEN GEMINI HERO + CSCO ORG CHART + VALUE CHAINS)
       ========================================================================= -->
  <main id="pageHome" class="page-view active">

    <!-- 1. FULL-VIEWPORT APPLE / GEMINI SCROLLABLE HERO LANDING -->
    <section class="hero-section">
      <!-- Smooth Ambient Aurora & Architectural Horizon Backdrop (No Scattering Sprinkles) -->
      <div class="hero-aurora-backdrop"></div>

      <!-- Full-Bleed 60fps Supply Chain Kinetic Canvas -->
      <canvas id="heroSupplyChainCanvas"></canvas>

      <div class="hero-vignette"></div>

      <div class="hero-content">
        <!-- Single Clean Gemini Enterprise Lockup (No Duplicate Sparkle Logo) -->
        <div class="hero-logo-lockup">
          <img data-asset="gemini_enterprise_dark.png" alt="Gemini Enterprise" class="gemini-hero" />
        </div>

        <h1 class="hero-title" style="margin-bottom: 36px;">
          Agentic Transformation for <span class="gradient-word">Supply Chain &amp; Demand</span>
        </h1>

        <div style="display:flex; flex-wrap:wrap; justify-content:center; gap:14px;">
          <button type="button" class="hero-cta-btn" onclick="goToOrgChart()">
            <span>Explore CSCO Organization (6 Verticals)</span>
            <span>&darr;</span>
          </button>
          <button type="button" class="hero-cta-btn" style="background:rgba(16,22,34,0.88); color:#fff; border:1px solid rgba(0,210,255,0.4);" onclick="openPersonasDirectoryPage('all', '', true, 'agents')">
            <span>Explore All 32 AI Agents &amp; ROI &rarr;</span>
          </button>
          <button type="button" class="hero-cta-btn" style="background:rgba(14,26,44,0.92); color:#7dd3fc; border:1px solid rgba(0,210,255,0.55);" onclick="openPeriodicTablePage('all', null, true)">
            <span>🧪 Periodic Table of Agents (32) &rarr;</span>
          </button>
          <button type="button" class="hero-cta-btn" style="background:rgba(12,32,28,0.92); color:#6ee7b7; border:1px solid rgba(16,185,129,0.55);" onclick="openMindMapPage('all', null, true)">
            <span>🧠 Neural Mind Map &amp; Flowchart &rarr;</span>
          </button>
        </div>

        <div class="four-color-bar" style="width:180px;">
          <span style="background:var(--sc-emerald);"></span>
          <span style="background:var(--sc-violet);"></span>
          <span style="background:#3b82f6;"></span>
          <span style="background:var(--sc-cyan);"></span>
          <span style="background:var(--sc-amber);"></span>
          <span style="background:#ec4899;"></span>
        </div>
      </div>
    </section>

    <!-- 2. CSCO ORG CHART (PROGRESSIVE EXPLORATION ACROSS THE 8 OPERATIONAL VERTICALS) -->
    <section id="orgChartSection" class="org-section">
      <div class="section-header">
        <h2 class="section-title">Office of the CSCO — The 8 Operational Verticals</h2>
        <p class="section-subtitle">The End-to-End Operating Topology decomposed from <span class="sc-hl-underline">Level-1 to Level-3</span> across the <strong class="sc-hl-bold">Three Synchronized Enterprise Flows</strong> (Physical Material, Demand Signal, and Working Capital Cash) — powered by deterministic math solvers and Gemini Enterprise agentic orchestration.</p>
      </div>

      <!-- Three Synchronized Enterprise Flows Architecture Banner -->
      <div class="rivers-banner">
        <div class="river-box">
          <h4>📦 Flow 1: Physical Material Flow (Downstream ──▶)</h4>
          <p>Raw Materials / Sourcing ──▶ Manufacturing Transformation ──▶ Mother Warehouses ──▶ Multi-Modal Transit ──▶ Regional Hubs ──▶ Retail Shelf.</p>
        </div>
        <div class="river-box signal">
          <h4>📡 Flow 2: Demand &amp; Information Signal Flow (◀── Upstream)</h4>
          <p>Consumer POS Checkouts ◀── Channel Sell-Through ◀── Continuous Replenishment ◀── S&amp;OP Consensus ◀── MRP Master Schedule ◀── Supplier Contracts.</p>
        </div>
        <div class="river-box cash">
          <h4>💰 Flow 3: Working Capital &amp; Cash Flow (◀──▶ Cyclic)</h4>
          <p>Cash-to-Cash Cycle = Days Inventory Outstanding (DIO) + Days Sales Outstanding (DSO) − Days Payables (DPO). Unlocking trapped capital while protecting service fill rates.</p>
        </div>
      </div>

      <!-- 8-Vertical Interactive Master Navigation Tab Bar on the Front Page -->
      <div class="vertical-tabs-nav-bar" id="verticalTabsNavBar">
        <button type="button" class="v-tab-btn active" data-vtab="all" onclick="switchVerticalTab('all', this)">
          <span class="v-tab-num" style="color:#38bdf8;">ALL 8</span>
          <span class="v-tab-title">All Verticals</span>
          <span class="v-tab-tag">End-to-End Network</span>
          <span class="v-tab-badge">26 Roles · 32 Agents</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="demand_sop" onclick="switchVerticalTab('demand_sop', this)" style="--v-accent: #10b981;">
          <span class="v-tab-num">V1 · PLAN</span>
          <span class="v-tab-title">Demand &amp; S&amp;OP</span>
          <span class="v-tab-tag">The Forecasters</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="sourcing_procurement" onclick="switchVerticalTab('sourcing_procurement', this)" style="--v-accent: #a142f4;">
          <span class="v-tab-num">V2 · SOURCE</span>
          <span class="v-tab-title">Sourcing &amp; Procurement</span>
          <span class="v-tab-tag">The Buyers</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="manufacturing_prod" onclick="switchVerticalTab('manufacturing_prod', this)" style="--v-accent: #3b82f6;">
          <span class="v-tab-num">V3 · MAKE</span>
          <span class="v-tab-title">Manufacturing &amp; MPS</span>
          <span class="v-tab-tag">The Makers</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="inventory_meio" onclick="switchVerticalTab('inventory_meio', this)" style="--v-accent: #06b6d4;">
          <span class="v-tab-num">V4 · BUFFER</span>
          <span class="v-tab-title">Inventory &amp; MEIO</span>
          <span class="v-tab-tag">The Buffers</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="warehousing_qa" onclick="switchVerticalTab('warehousing_qa', this)" style="--v-accent: #00d2ff;">
          <span class="v-tab-num">V5 · WMS &amp; QA</span>
          <span class="v-tab-title">Warehousing &amp; QA</span>
          <span class="v-tab-tag">The Custodians</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="logistics_fleet" onclick="switchVerticalTab('logistics_fleet', this)" style="--v-accent: #ff8c00;">
          <span class="v-tab-num">V6 · LOGISTICS</span>
          <span class="v-tab-title">Logistics &amp; Fleet</span>
          <span class="v-tab-tag">The Movers</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="trade_mkt_dist" onclick="switchVerticalTab('trade_mkt_dist', this)" style="--v-accent: #f59e0b;">
          <span class="v-tab-num">V7 · TM&amp;D</span>
          <span class="v-tab-title">TM&amp;D Last-Mile</span>
          <span class="v-tab-tag">The Last-Mile Push</span>
        </button>
        <button type="button" class="v-tab-btn" data-vtab="reverse_risk_esg" onclick="switchVerticalTab('reverse_risk_esg', this)" style="--v-accent: #ec4899;">
          <span class="v-tab-num">V8 · GUARDIAN</span>
          <span class="v-tab-title">Reverse &amp; Risk ESG</span>
          <span class="v-tab-tag">The Guardians</span>
        </button>
      </div>

      <div class="cfo-root-wrapper">
        <!-- CSCO Apex Box featuring Animated 3D Isometric Conveyor & Control Tower Emblem -->
        <div class="cfo-box">
          <div class="cfo-sc-emblem" aria-hidden="true">
            <svg viewBox="0 0 84 64" style="width:100%;height:100%;">
              <polygon points="8,42 42,24 76,42 42,58" fill="rgba(0,210,255,0.12)" stroke="#00d2ff" stroke-width="1.3" />
              <line x1="18" y1="37" x2="66" y2="37" stroke="#00d2ff" stroke-width="1" stroke-dasharray="4 3" class="sc-arc-flow" />
              <g class="sc-conveyor-box-anim" style="animation-duration:2.6s;">
                <polygon points="16,30 26,25 36,30 26,35" fill="#00d2ff" />
                <polygon points="16,30 26,35 26,44 16,39" fill="#0284c7" />
                <polygon points="36,30 26,35 26,44 36,39" fill="#0369a1" />
              </g>
              <circle cx="42" cy="16" r="7" fill="none" stroke="#10b981" stroke-width="1.4" stroke-dasharray="4 2" class="sc-arc-flow" />
              <circle cx="42" cy="16" r="2.8" fill="#ff8c00" class="sc-node-pulse" />
            </svg>
          </div>
          <div>
            <div class="cfo-box-title">Chief Supply Chain Officer (CSCO)</div>
            <div class="cfo-box-sub"><span class="sc-hl-metric">8 Operational Verticals</span> · <span class="sc-hl-metric">26 Personas</span> · <span class="sc-hl-metric">28 Domain Agents</span> + <span class="sc-hl-metric">4 Universal Cross-Persona Agents</span></div>
          </div>
        </div>

        <!-- SVG Tree Lines to 8 Supply Chain Verticals (4x2 Grid) with Animated Telemetry Packets -->
        <svg class="org-connectors" viewBox="0 0 1000 56" preserveAspectRatio="none">
          <defs>
            <linearGradient id="orgLineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#10b981" stop-opacity="0.55" />
              <stop offset="33%" stop-color="#3b82f6" stop-opacity="0.75" />
              <stop offset="66%" stop-color="#ff8c00" stop-opacity="0.75" />
              <stop offset="100%" stop-color="#ec4899" stop-opacity="0.55" />
            </linearGradient>
          </defs>
          <path d="M500,0 L500,24 M125,24 L875,24 M125,24 L125,56 M375,24 L375,56 M625,24 L625,56 M875,24 L875,56" />
          <path d="M500,0 L500,24 M125,24 L875,24 M125,24 L125,56 M375,24 L375,56 M625,24 L625,56 M875,24 L875,56"
                stroke="url(#orgLineGrad)" stroke-width="2.2" stroke-dasharray="8 10" fill="none"
                style="animation: scDashFlow 2.4s linear infinite;" />
          <circle r="3.5" fill="#10b981">
            <animateMotion dur="2.4s" repeatCount="indefinite" path="M500,0 L500,24 L125,24 L125,56" />
          </circle>
          <circle r="3.5" fill="#3b82f6">
            <animateMotion dur="2.0s" repeatCount="indefinite" path="M500,0 L500,24 L375,24 L375,56" />
          </circle>
          <circle r="3.5" fill="#ff8c00">
            <animateMotion dur="2.2s" repeatCount="indefinite" path="M500,0 L500,24 L625,24 L625,56" />
          </circle>
          <circle r="3.5" fill="#ec4899">
            <animateMotion dur="2.6s" repeatCount="indefinite" path="M500,0 L500,24 L875,24 L875,56" />
          </circle>
        </svg>

        <!-- 6 Clean Supply Chain Vertical Boxes -->
        <div id="deptRowContainer" class="dept-row"></div>
      </div>

      <!-- Progressive Department Showcase Box (Smooth Slide-Down Accordion Drawer) -->
      <div id="deptShowcaseContainer"></div>

      <!-- Cross-Persona Universal Supply Chain Agents (Used by All 26 Personas) -->
      <div id="universalAgentsHomeContainer"></div>

      <!-- End-to-End Agentic Value Chains (4 Suites: F2F, O2D, S2P, P2R) -->
      <div class="vc-home-block">
        <div class="section-header" style="margin-bottom: 36px;">
          <h2 class="section-title" style="font-size: clamp(28px, 3.2vw, 38px);">End-to-End Agentic Value Chains (4 Suites)</h2>
          <p class="section-subtitle">Connected <span class="sc-hl-metric">6-stage pipelines</span> that synchronize <span class="sc-hl-underline">demand sensing</span>, <span class="sc-hl-underline">finite manufacturing</span>, <span class="sc-hl-underline">multi-echelon inventory</span>, <strong class="sc-hl-bold">Factory &rarr; Ship &rarr; Airplane &rarr; Rail &rarr; Warehouse &rarr; 3D LIFO Truck delivery</strong>, <span class="sc-hl-underline">strategic sourcing</span>, and <span class="sc-hl-underline">circular recovery</span>.</p>
        </div>
        <div id="valueChainEntryContainer" class="vc-entry-grid"></div>
      </div>
    </section>

  </main>

  <!-- =========================================================================
       PAGE 2: DEDICATED PERSONA PAGE
       ========================================================================= -->
  <main id="pagePersona" class="page-view">
    <div id="personaPageContent" class="subpage-container"></div>
  </main>

  <!-- =========================================================================
       PAGE 3: DEDICATED AGENT EXECUTIVE SELLING & DEMO PAGE
       ========================================================================= -->
  <main id="pageAgent" class="page-view">
    <div id="agentPageContent" class="subpage-container"></div>
  </main>

  <!-- =========================================================================
       PAGE 3B: DEDICATED PER-AGENT HIGH-CODE ARCHITECTURE & SUB-AGENT FLOW PAGE
       ========================================================================= -->
  <main id="pageBlueprint" class="page-view">
    <div id="blueprintPageContent" class="subpage-container"></div>
  </main>

  <!-- =========================================================================
       PAGE 4: DEDICATED END-TO-END VALUE CHAIN PAGE (F2F, O2D, S2P, P2R)
       ========================================================================= -->
  <main id="pageValueChain" class="page-view">
    <div id="valueChainPageContent" class="subpage-container"></div>
  </main>

  <!-- =========================================================================
       PAGE 5: DEDICATED PERSONAS & AGENTS SEARCHABLE DIRECTORY TAB
       ========================================================================= -->
  <main id="pageDirectory" class="page-view">
    <div id="directoryPageContent" class="subpage-container"></div>
  </main>

  <!-- =========================================================================
       PAGE 6: DEDICATED MULTI-AGENT REFERENCE ARCHITECTURE TAB
       ========================================================================= -->
  <main id="pageArchitecture" class="page-view">
    <div id="architecturePageContent" class="subpage-container"></div>
  </main>

  <!-- =========================================================================
       PAGE 7: PERIODIC TABLE OF SUPPLY CHAIN AI (32 AGENTS & 26 PERSONAS)
       ========================================================================= -->
  <main id="pagePeriodic" class="page-view">
    <div id="periodicPageContent" class="subpage-container"></div>
  </main>

  <!-- =========================================================================
       PAGE 8: INTERACTIVE NEURAL MIND MAP & PORTAL FLOWCHART
       ========================================================================= -->
  <main id="pageMindMap" class="page-view">
    <div id="mindMapPageContent" class="subpage-container"></div>
  </main>

  <!-- =========================================================================
       ENTERPRISE TWIN MODAL (AUTONOMOUS CLIENT ADAPTATION & PREVIEW SWITCHER)
       ========================================================================= -->
  <div id="enterpriseTwinModal" class="modal-overlay" style="display:none; position:fixed; inset:0; z-index:99999; background:rgba(2,6,18,0.85); backdrop-filter:blur(16px); align-items:center; justify-content:center; padding:20px;">
    <div class="modal-card" style="background:#090d18; border:1px solid rgba(168,85,247,0.45); border-radius:24px; max-width:820px; width:100%; max-height:90vh; overflow-y:auto; padding:32px; box-shadow:0 30px 90px rgba(0,0,0,0.85); position:relative;">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:16px;">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="width:44px; height:44px; border-radius:12px; background:linear-gradient(135deg,#a855f7,#38bdf8); display:flex; align-items:center; justify-content:center; font-size:22px;">
            🪄
          </div>
          <div>
            <h2 style="font-family:var(--font-display); font-size:22px; font-weight:800; color:#ffffff; margin:0;">
              Autonomous Enterprise Twin Agent
            </h2>
            <div style="font-size:12.5px; color:#cbd5e1; margin-top:2px;">
              Re-skins and adapts this entire 60fps transformation framework in any enterprise customer's image
            </div>
          </div>
        </div>
        <button type="button" class="back-btn" style="padding:6px 14px; font-size:13px;" onclick="closeEnterpriseTwinModal()">
          ✕ Close
        </button>
      </div>

      <p style="font-size:14px; color:#94a3b8; line-height:1.65; margin-bottom:20px;">
        Instead of hardcoding single industries, the <strong>Enterprise Twin Agent</strong> uses autonomous Python research tools (Company Profiler, Career Persona Miner, Ecosystem Miner) to map your 26 SCOR personas and 32 AI agents to the customer's real job titles, factory hubs, and product nomenclature.
      </p>

      <!-- Interactive Form: Inputs for Custom Enterprise Research & Live-Apply -->
      <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(168,85,247,0.3); border-radius:18px; padding:22px; margin-bottom:24px;">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; flex-wrap:wrap; gap:8px;">
          <div style="font-family:var(--font-display); font-size:16px; font-weight:800; color:#ffffff;">
            🎯 Research Any Enterprise &amp; Generate Client Twin
          </div>
          <span style="font-size:11.5px; font-weight:700; color:#34d399; background:rgba(16,185,129,0.14); border:1px solid rgba(16,185,129,0.35); padding:3px 10px; border-radius:10px;">
            ● Live In-Browser Synthesis Active
          </span>
        </div>

        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:14px; margin-bottom:14px;">
          <div>
            <label style="display:block; font-size:12px; font-weight:700; color:#cbd5e1; margin-bottom:6px; text-transform:uppercase; letter-spacing:0.05em;">
              Company Name <span style="color:#f43f5e;">*</span>
            </label>
            <input type="text" id="twinCompanyInput" class="twin-input-field" placeholder="e.g. Caterpillar, Boeing, BMW, Walmart, L'Oréal, Tesla..." value="" />
          </div>

          <div>
            <label style="display:block; font-size:12px; font-weight:700; color:#cbd5e1; margin-bottom:6px; text-transform:uppercase; letter-spacing:0.05em;">
              Industry / Sector <span style="color:#f43f5e;">*</span>
            </label>
            <select id="twinIndustrySelect" class="twin-input-field" style="cursor:pointer;">
              <option value="auto">✨ Auto-Detect from Company Name</option>
              <option value="automotive">🚗 Automotive, EV &amp; Mobility</option>
              <option value="oil_gas_energy">🛢️ Energy, Oil &amp; Gas / Petrochemicals</option>
              <option value="life_sciences_pharma">💊 Life Sciences, Pharma &amp; BioTech</option>
              <option value="cpg_retail">🛒 Consumer Goods (CPG) &amp; Retail</option>
              <option value="aerospace">✈️ Aerospace &amp; Heavy Machinery</option>
              <option value="hightech">⚡ High-Tech Electronics &amp; Semis</option>
            </select>
          </div>
        </div>

        <div style="margin-bottom:18px;">
          <label style="display:block; font-size:12px; font-weight:700; color:#cbd5e1; margin-bottom:6px; text-transform:uppercase; letter-spacing:0.05em;">
            Strategic Operational Focus / Key Products (Optional)
          </label>
          <input type="text" id="twinFocusInput" class="twin-input-field" placeholder="e.g. Battery gigafactories & JIS chassis line feeding, cold-chain vaccines, pipeline hydraulics..." />
        </div>

        <div style="display:flex; flex-wrap:wrap; gap:12px; align-items:center; justify-content:space-between;">
          <button type="button" class="btn-generate-twin" onclick="executeTwinGeneration()" style="display:inline-flex; align-items:center; gap:8px; padding:12px 24px; border-radius:12px; background:linear-gradient(135deg, #a855f7 0%, #38bdf8 100%); color:#ffffff; font-family:var(--font-display); font-size:14.5px; font-weight:800; border:none; cursor:pointer; box-shadow:0 8px 24px rgba(168,85,247,0.35); transition:transform 0.15s ease;">
            <span>⚡ Research &amp; Live-Apply Client Twin</span>
          </button>
          
          <div style="font-size:12px; color:#94a3b8;">
            Instant live browser morph + optional decoupled Argolis/local backend call.
          </div>
        </div>

        <!-- Animated Progress HUD -->
        <div id="twinProgressHud" style="display:none; margin-top:16px; padding:16px; border-radius:12px; background:#04060a; border:1px solid rgba(168,85,247,0.4);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span id="hudStatusText" style="font-family:var(--font-mono); font-size:12.5px; color:#38bdf8; font-weight:700;">
              🔍 Autonomous Agent researching company identity...
            </span>
            <span id="hudPercentText" style="font-family:var(--font-mono); font-size:12px; color:#a7f3d0; font-weight:700;">0%</span>
          </div>
          <div style="height:6px; background:rgba(255,255,255,0.1); border-radius:10px; overflow:hidden; margin-bottom:10px;">
            <div id="hudProgressBar" style="width:0%; height:100%; background:linear-gradient(90deg, #a855f7, #00d2ff, #10b981); transition:width 0.3s ease;"></div>
          </div>
          <div id="hudStepLog" style="font-family:var(--font-mono); font-size:11.5px; color:#cbd5e1; line-height:1.6;"></div>
        </div>
      </div>

      <!-- Quick 1-Click Presets -->
      <div style="font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#d8b4fe; margin-bottom:10px;">
        Or Select Instant Preset Showcase:
      </div>
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(170px, 1fr)); gap:10px; margin-bottom:24px;">
        <button type="button" class="twin-preset-card" onclick="quickSelectPreset('volkswagen')" style="text-align:left; background:rgba(0,30,80,0.4); border:1px solid rgba(0,210,255,0.4); border-radius:14px; padding:12px; cursor:pointer;">
          <div style="font-size:16px; font-weight:700; color:#fff; margin-bottom:3px;">🚗 Volkswagen</div>
          <div style="font-size:11px; color:#7dd3fc;">Auto · MEB Gigafactory</div>
        </button>
        <button type="button" class="twin-preset-card" onclick="quickSelectPreset('itc')" style="text-align:left; background:rgba(16,185,129,0.22); border:1px solid rgba(16,185,129,0.45); border-radius:14px; padding:12px; cursor:pointer;">
          <div style="font-size:16px; font-weight:700; color:#fff; margin-bottom:3px;">🌾 ITC Limited</div>
          <div style="font-size:11px; color:#6ee7b7;">FMCG · e-Choupal Agri</div>
        </button>
        <button type="button" class="twin-preset-card" onclick="quickSelectPreset('boeing')" style="text-align:left; background:rgba(0,51,160,0.22); border:1px solid rgba(56,189,248,0.4); border-radius:14px; padding:12px; cursor:pointer;">
          <div style="font-size:16px; font-weight:700; color:#fff; margin-bottom:3px;">✈️ Boeing</div>
          <div style="font-size:11px; color:#7dd3fc;">Aerospace · Titanium Forgings</div>
        </button>
        <button type="button" class="twin-preset-card" onclick="quickSelectPreset('caterpillar')" style="text-align:left; background:rgba(255,205,17,0.18); border:1px solid rgba(255,205,17,0.45); border-radius:14px; padding:12px; cursor:pointer;">
          <div style="font-size:16px; font-weight:700; color:#fff; margin-bottom:3px;">🚜 Caterpillar</div>
          <div style="font-size:11px; color:#fef08a;">Heavy Machinery · Cat Reman</div>
        </button>
        <button type="button" class="twin-preset-card" onclick="quickSelectPreset('shell')" style="text-align:left; background:rgba(185,28,28,0.2); border:1px solid rgba(251,191,36,0.4); border-radius:14px; padding:12px; cursor:pointer;">
          <div style="font-size:16px; font-weight:700; color:#fff; margin-bottom:3px;">🛢️ Shell plc</div>
          <div style="font-size:11px; color:#fde047;">Energy · Crude Pipelines</div>
        </button>
        <button type="button" class="twin-preset-card" onclick="quickSelectPreset('pfizer')" style="text-align:left; background:rgba(0,0,255,0.2); border:1px solid rgba(0,210,255,0.4); border-radius:14px; padding:12px; cursor:pointer;">
          <div style="font-size:16px; font-weight:700; color:#fff; margin-bottom:3px;">💊 Pfizer Inc.</div>
          <div style="font-size:11px; color:#93c5fd;">Pharma · cGMP Biologics</div>
        </button>
        <button type="button" class="twin-preset-card" onclick="quickSelectPreset('unilever')" style="text-align:left; background:rgba(16,185,129,0.18); border:1px solid rgba(16,185,129,0.4); border-radius:14px; padding:12px; cursor:pointer;">
          <div style="font-size:16px; font-weight:700; color:#fff; margin-bottom:3px;">🛒 Unilever</div>
          <div style="font-size:11px; color:#a7f3d0;">CPG · 400 Retail Brands</div>
        </button>
        <button type="button" class="twin-preset-card" onclick="switchClientTwin('reset')" style="text-align:left; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.18); border-radius:14px; padding:12px; cursor:pointer;">
          <div style="font-size:16px; font-weight:700; color:#fff; margin-bottom:3px;">🌐 Golden SCOR</div>
          <div style="font-size:11px; color:#94a3b8;">Industry-Agnostic Base</div>
        </button>
      </div>

      <!-- Decoupled Backend Architecture Information & Setting -->
      <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:8px;">
          <div style="font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:0.07em; color:#38bdf8;">
            🔗 Decoupled Backend Agent Service (Local / Cloud Run / Argolis):
          </div>
          <span style="font-family:var(--font-mono); font-size:11px; color:#94a3b8;">
            POST /api/v1/generate-twin
          </span>
        </div>
        <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap; margin-bottom:8px;">
          <input type="text" id="twinBackendUrlInput" class="twin-input-field" style="flex:1; min-width:260px; font-family:var(--font-mono); font-size:12.5px; padding:8px 12px;" value="http://localhost:8080/api/v1/generate-twin" />
          <label style="display:flex; align-items:center; gap:6px; font-size:12px; color:#cbd5e1; cursor:pointer;">
            <input type="checkbox" id="twinCallBackendCheckbox" checked />
            Call backend if reachable
          </label>
        </div>
        <div style="font-size:11.5px; color:#94a3b8; line-height:1.5;">
          The website runs standalone on <strong>Zipline</strong> with full in-browser synthesis. If the local backend agent (<code>python3 -m enterprise_twin.server</code>) or Cloud Run / Argolis service is running, it compiles the persistent static files into <code>dist/&lt;company&gt;/</code> and builds the Zipline bundle automatically.
        </div>
      </div>
    </div>
  </div>

  <!-- =========================================================================
       GLOBAL EXECUTIVE ATTRIBUTION FOOTER (ZUHAIB PARVEZ & SUMAN BANERJEE)
       ========================================================================= -->
  <footer class="global-authors-footer">
    <div style="display:flex; flex-direction:column; gap:6px;">
      <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
        <span style="font-family:var(--font-display); font-size:17px; font-weight:800; color:#ffffff;">
          Gemini Enterprise · Supply Chain &amp; Demand (Office of the CSCO)
        </span>
        <span class="authors-credit-pill" style="padding:5px 14px; font-size:12.5px;">
          ✦ Built by <strong>Zuhaib Parvez</strong> &amp; <strong>Suman Banerjee</strong>
        </span>
      </div>
      <div style="font-size:14px; color:var(--text-secondary);">
        6 ASCM SCOR Verticals · 26 Enterprise Supply Chain Personas · 32 Agentic AI Systems (4 Universal Core + 28 Domain Agents) · 96 A2A Sub-Agents
      </div>
    </div>
    <div style="display:flex; flex-wrap:wrap; gap:10px; align-items:center;">
      <button type="button" class="switch-pill" onclick="goHome()">Home</button>
      <button type="button" class="switch-pill" onclick="goToOrgChart()">CSCO Org Chart</button>
      <button type="button" class="switch-pill" style="border-color:rgba(0,210,255,0.45); color:#7dd3fc;" onclick="openPeriodicTablePage('all', null, true)">🧪 Periodic Table</button>
      <button type="button" class="switch-pill" style="border-color:rgba(16,185,129,0.45); color:#6ee7b7;" onclick="openMindMapPage('all', null, true)">🧠 Neural Mind Map</button>
      <a href="periodic_table.html" class="switch-pill" style="border-color:rgba(56,189,248,0.35); color:#bae6fd;">Standalone Periodic Table ↗</a>
      <a href="mind_map.html" class="switch-pill" style="border-color:rgba(16,185,129,0.35); color:#a7f3d0;">Standalone Mind Map ↗</a>
    </div>
  </footer>

  <!-- =========================================================================
       DATA & MULTI-PAGE CONTROLLER
       ========================================================================= -->
  <script>    /* 1. EIGHT CANONICAL OPERATIONAL VERTICALS UNDER THE CSCO */
    const DEPARTMENTS = __EMBEDDED_DEPARTMENTS_JSON__;
    Object.defineProperty(DEPARTMENTS, 'sourcing_risk', { get: () => DEPARTMENTS.sourcing_procurement, enumerable: false, configurable: true });
    Object.defineProperty(DEPARTMENTS, 'inventory_warehouse', { get: () => DEPARTMENTS.warehousing_qa, enumerable: false, configurable: true });
    Object.defineProperty(DEPARTMENTS, 'circular_enable', { get: () => DEPARTMENTS.reverse_risk_esg, enumerable: false, configurable: true });

    function getDeptMeta(deptId) {
      if (DEPARTMENTS[deptId]) return DEPARTMENTS[deptId];
      if (deptId === 'sourcing_risk') return DEPARTMENTS.sourcing_procurement;
      if (deptId === 'inventory_warehouse') return DEPARTMENTS.warehousing_qa;
      if (deptId === 'circular_enable') return DEPARTMENTS.reverse_risk_esg;
      return DEPARTMENTS.demand_sop;
    }

    /* 2. SUPPLY CHAIN PERSONAS ROSTER (29 ENTERPRISE ROLES ACROSS 8 VERTICALS) */
    const PERSONAS = __EMBEDDED_PERSONAS_JSON__;

    /* 3. SUPPLY CHAIN AGENTS ROSTER (35 AGENTS: 4 UNIVERSAL CORE + 31 DOMAIN AGENTS) */
    const AGENTS = __EMBEDDED_AGENTS_JSON__;

    /* 4. PERSONA -> VALUE CHAIN MAPPING (ALL 26 PERSONAS MAPPED ACROSS 4 SUITES) */
    const PERSONA_VALUE_CHAIN_MAP = {
      demand_planning_dir: 'f2f',
      sop_ibp_lead: 'f2f',
      promo_launch_planner: 'f2f',
      cpfr_channel_mgr: 'f2f',
      category_sourcing_mgr: 's2p',
      supplier_risk_lead: 's2p',
      tariff_compliance_spec: 's2p',
      supplier_quality_lead: 's2p',
      mps_scheduling_lead: 'f2f',
      plant_oee_maintenance_mgr: 'f2f',
      manufacturing_quality_eng: 's2p',
      bom_change_launch_lead: 's2p',
      meio_inventory_mgr: 'f2f',
      warehouse_slotting_lead: 'p2r',
      atp_fulfillment_spec: 'o2d',
      dock_yard_supervisor: 'p2r',
      global_trade_port_mgr: 'o2d',
      air_cargo_charter_lead: 'o2d',
      intermodal_rail_linehaul_lead: 'o2d',
      fleet_dispatch_mgr: 'o2d',
      network_logistics_lead: 'o2d',
      freight_claims_analyst: 'o2d',
      otif_customer_service_lead: 'o2d',
      reverse_logistics_mgr: 'p2r',
      sc_sustainability_esg_lead: 'p2r',
      sc_finops_network_architect: 'p2r'
    };

    /* 5. FOUR END-TO-END 6-STAGE AGENTIC VALUE CHAINS (F2F, O2D, S2P, P2R) */
    const VALUE_CHAINS = {
      f2f: {
        id: 'f2f',
        shortTitle: 'Forecast-to-Fulfill (F2F)',
        title: 'Forecast-to-Fulfill (F2F) Autonomous Suite',
        flowBadge: 'End-to-End Planning-to-Warehouse Pipeline',
        cardSubtitle: 'Synchronizes Demand Sensing, Promo Shaping, S&OP Consensus, Multi-Echelon Inventory, Tier-N Sourcing & 3D Slotting.',
        cardFooterLeft: '6 Stages · 6 Personas',
        color: '#34a853',
        sculpture: 'sculpture_emerald_ribbon.png',
        animGif: 'anim_genome_dark.gif',
        cadType: 'demand_wave',
        headlineStat: '21d → 45m',
        headlineLabel: 'End-to-End Planning-to-Execution Cycle',
        toilHoursBefore: '21-day siloed spreadsheet planning cycle',
        toilHoursAfter: '45-minute synchronized Golden Thread loop',
        summary: 'Eliminates the weeks-long disconnect between commercial forecasting, S&OP capacity planning, multi-echelon safety stocks, sub-tier sourcing, and warehouse slotting.',
        focusAreas: ['Multi-Signal Demand Sensing', 'Autonomous S&OP Consensus', 'Stochastic MEIO Buffers', '3D Golden-Zone Slotting'],
        videoSrc: 'videos/demand_sensing_demo.mp4',
        hasPreloadedVideo: true,
        problem: 'Demand, S&OP, Inventory, Procurement, and Warehouse teams operate in sequential spreadsheet silos—amplifying bullwhip buffers while still stocking out at the edge.',
        solution: 'Six specialized agents pass probabilistic demand, capacity envelopes, safety-stock targets, and slotting directives along a single verified Golden Thread.',
        advantage: 'Compresses planning cycles from 21 days to 45 minutes (-95% time), improves forecast accuracy by 24% (6.4% lower WAPE forecast error), and releases 18% of working capital ($35M+ cash freed).',
        stages: [
          {
            num: 'Stage 01',
            name: 'Multi-Signal Demand Sensing',
            color: '#34a853',
            modality: 'TimesFM + Bayesian',
            systems: 'POS · EDI · BigQuery',
            ownerId: 'demand_planning_dir',
            ownerLabel: 'Demand Planning Director',
            toilTime: '2.0 hrs/day',
            afterTime: '5 mins',
            before: 'Lagged ERP order history misses real-time regional consumption shifts and distorts baseline forecasts after stockouts.',
            after: 'PulseCast ingests daily POS sell-through and macro drivers, imputes stockouts, and outputs P10/P50/P90 demand curves.',
            goldenThread: 'Streams probabilistic P10/P50/P90 SKU-hub demand distributions to Stage 02 (ElasticityIQ).'
          },
          {
            num: 'Stage 02',
            name: 'Demand Shaping & Cannibalization Filter',
            color: '#34a853',
            modality: 'Causal Uplift AI',
            systems: 'Promo Calendar · Pricing',
            ownerId: 'promo_launch_planner',
            ownerLabel: 'Demand Shaping Manager',
            toilTime: '1.5 hrs/day',
            afterTime: '10 mins',
            before: 'Promotions spike constrained items and silently cannibalize 30%+ of sister SKUs without baseline adjustment.',
            after: 'ElasticityIQ strips out sister-SKU cannibalization and steers promotional features toward surplus high-margin inventory.',
            goldenThread: 'Publishes net shaped, cannibalization-adjusted demand vectors to Stage 03 (Synapse S&OP).'
          },
          {
            num: 'Stage 03',
            name: 'Autonomous S&OP Capacity Consensus',
            color: '#4285f4',
            modality: 'MILP + P&L Twin',
            systems: 'ERP MPS · Plant Lines',
            ownerId: 'sop_ibp_lead',
            ownerLabel: 'S&OP / IBP Process Lead',
            toilTime: '2.5 hrs/day',
            afterTime: '15 mins',
            before: 'Reconciling demand surges against plant line capacity and financial budgets takes 3 weeks of sequential meetings.',
            after: 'Synapse simulates 50+ capacity trade-offs (overtime, alternate plant, pre-build) and locks the P&L-optimal supply plan.',
            goldenThread: 'Commits constrained master production envelopes to Stage 04 (EchelonFlow MEIO).'
          },
          {
            num: 'Stage 04',
            name: 'Multi-Echelon Safety Stock Rebalancing',
            color: '#4285f4',
            modality: 'Stochastic MEIO',
            systems: 'ERP Inventory · Hubs',
            ownerId: 'meio_inventory_mgr',
            ownerLabel: 'Global Inventory Manager',
            toilTime: '2.0 hrs/day',
            afterTime: '10 mins',
            before: 'Static single-echelon Days-of-Supply rules hoard excess buffer upstream while regional hubs stock out.',
            after: 'EchelonFlow recalculates coupled multi-echelon buffers and triggers lateral hub-to-hub transfers before new production.',
            goldenThread: 'Transmits net component requirements to Stage 05 (NexusShield) and hub stock targets to Stage 06.'
          },
          {
            num: 'Stage 05',
            name: 'Multi-Tier Supplier & Material Lock',
            color: '#ea4335',
            modality: 'Tier-N Graph + RFQ',
            systems: 'BOM · Supplier Portal',
            ownerId: 'supplier_risk_lead',
            ownerLabel: 'Supplier Risk Lead',
            toilTime: '2.0 hrs/day',
            afterTime: '10 mins',
            before: 'Tier-2 raw material bottlenecks remain hidden until Tier-1 suppliers miss factory delivery dates.',
            after: 'NexusShield verifies Tier-1 to Tier-3 availability and releases dual-source PO allocations at parametric should-cost.',
            goldenThread: 'Confirms verified inbound ASN arrival schedules into Stage 06 (SlotMaster 3D Twin).'
          },
          {
            num: 'Stage 06',
            name: '3D Warehouse Slotting & Wave Release',
            color: '#fbbc04',
            modality: '3D Spatial Twin',
            systems: 'WMS · AS/RS · Docks',
            ownerId: 'warehouse_slotting_lead',
            ownerLabel: 'Warehouse & Slotting Lead',
            toilTime: '1.5 hrs/day',
            afterTime: '10 mins',
            before: 'Surging SKUs sit in distant upper racks and uncoordinated wave releases cause aisle congestion.',
            after: 'SlotMaster re-slots high-velocity SKUs into Golden-Zone bays and releases balanced pick waves synced to outbound docks.',
            goldenThread: 'Hands staged outbound pallets directly into Stage 01 of the Order-to-Delivery (O2D) pipeline.'
          }
        ]
      },
      o2d: {
        id: 'o2d',
        shortTitle: 'Order-to-Delivery (O2D) Multi-Modal',
        title: 'Order-to-Delivery (O2D) Factory-to-Ship-to-Air-to-Rail-to-Road Suite',
        flowBadge: 'Factory → Ocean Ship → Air Cargo → Intermodal Rail → Cross-Dock → Road Fleet',
        cardSubtitle: 'Unifies Factory Mode-Split ATP, Ocean Vessel AIS & Port Drayage, 3D Air Cargo ULD Packing, Intermodal Rail Cross-Dock, Google Maps Road Fleet & 3D LIFO Loading.',
        cardFooterLeft: '6 Stages · 7 Multi-Modal Personas',
        color: '#fbbc04',
        sculpture: 'sculpture_amber_mesh.png',
        animGif: 'anim_ribbon_dark.gif',
        cadType: 'corridor_map',
        headlineStat: '-24% Cost',
        headlineLabel: 'Global Multi-Modal Transit Cost @ 92% Cube & 99.4% OTIF',
        toilHoursBefore: 'Siloed Ocean, Air, Rail, WMS & Road Truck Dispatch',
        toilHoursAfter: 'Factory → Ship/Air/Rail → Cross-Dock → Maps CVRPTW & 3D LIFO',
        summary: 'Orchestrates the entire physical movement of goods from the Factory Gate across Ocean Vessels, Airplanes (Belly/Charter ULDs), Intermodal Rail, Cross-Dock Warehouses, and Google Maps Road Fleet.',
        focusAreas: ['Factory Mode-Split & ATP', 'Ocean AIS & Port Drayage', 'Air Cargo 3D ULD Contour', 'Intermodal Rail & Road 3D LIFO'],
        videoSrc: 'videos/fleetflow_dispatch_demo.mp4',
        hasPreloadedVideo: true,
        problem: 'Global distribution is fractured across siloed ocean forwarders, emergency air brokers, Class-I rail ramps, warehouse cross-docks, and local road fleets—causing port demurrage, air volumetric waste, and half-empty trucks.',
        solution: 'Connects PromiseGuard + ModalShift at the factory gate with PortWatch (Ocean), AeroFreight (Air ULD), IntermodalSync + CrossDockFlow (Rail & Warehouse), FleetFlow + CubeMaster 3D (Road Fleet), and SentinelMove (Audit).',
        advantage: 'Cuts global multi-modal transit cost by 24%, port demurrage by 67%, air cargo spend by 28%, and road fleet cost by 19.4% at 92% 3D cube utilization.',
        stages: [
          {
            num: 'Stage 01',
            name: 'Factory Gate ATP & Dynamic Mode-Split (Ship / Air / Rail / Truck)',
            color: '#4285f4',
            modality: 'Spanner + Mode MILP',
            systems: 'SAP aATP · TM · Cloud Spanner',
            ownerId: 'atp_fulfillment_spec',
            ownerLabel: 'Order Promising Specialist',
            toilTime: '2.0 hrs/day',
            afterTime: '10 mins',
            before: 'Static routing guides ship entire factory POs via slow ocean or panic-expedite the entire batch by expensive air freight.',
            after: 'PromiseGuard & ModalShift allocate factory output across Ocean, Sea-Air, Air, Rail, and Road based on downstream DC stockout risk.',
            goldenThread: 'Dispatches multi-modal booking splits to Stage 02 (Ocean PortWatch) and Stage 03 (AeroFreight Air).'
          },
          {
            num: 'Stage 02',
            name: 'Ocean Vessel AIS, Stowage & Port Drayage',
            color: '#00d2ff',
            modality: 'Satellite AIS + MILP',
            systems: 'Spire AIS · CargoWise · WeatherNext 3',
            ownerId: 'global_trade_port_mgr',
            ownerLabel: 'Ocean & Port Logistics Manager',
            toilTime: '2.0 hrs/day',
            afterTime: '10 mins',
            before: 'Containers sit at congested port terminals accruing $350+/day demurrage while inland DCs wait on blind ocean carrier ETAs.',
            after: 'PortWatch predicts berth discharge 5 days ahead via satellite AIS & WeatherNext 3, auto-books drayage gates, and transloads urgent SKUs.',
            goldenThread: 'Routes discharged port containers to Stage 04 (Intermodal Rail & Cross-Dock) or Stage 03 (Sea-Air Upgrade).'
          },
          {
            num: 'Stage 03',
            name: 'Air Cargo Charter, Belly Capacity & 3D ULD Contour Packing',
            color: '#a142f4',
            modality: '3D ULD Solver + ADS-B',
            systems: 'IATA ONE Record · FlightAware ADS-B',
            ownerId: 'air_cargo_charter_lead',
            ownerLabel: 'Air Cargo & ULD Lead',
            toilTime: '2.0 hrs/day',
            afterTime: '10 mins',
            before: 'Emergency air shipments waste 25%+ chargeable volumetric weight in contoured ULDs and miss tarmac connections.',
            after: 'AeroFreight packs 3D contoured aircraft ULDs (LD3/LD7/PMC), optimizes belly vs. charter rates, and tracks live ADS-B tail numbers.',
            goldenThread: 'Streams airport tarmac recovery & de-consolidation manifests directly into Stage 04 (Cross-Dock Flow-Through).'
          },
          {
            num: 'Stage 04',
            name: 'Intermodal Rail Linehaul & Warehouse Cross-Dock Flow-Through',
            color: '#34a853',
            modality: 'Rail MILP + Cross-Dock',
            systems: 'Railinc EDI 404 · SAP EWM · Maps',
            ownerId: 'intermodal_rail_linehaul_lead',
            ownerLabel: 'Intermodal Rail & Linehaul Lead',
            toilTime: '1.5 hrs/day',
            afterTime: '10 mins',
            before: 'Long-haul freight defaults to costly OTR trucks, and inbound containers/ULDs get put away into reserve racks only to be re-picked hours later.',
            after: 'IntermodalSync & CrossDockFlow move 500+ mi corridors on COFC rail and route urgent pallets straight from inbound strip doors to outbound truck bays.',
            goldenThread: 'Stages consolidated cross-dock waves at outbound doors for Stage 05 (FleetFlow & CubeMaster 3D).'
          },
          {
            num: 'Stage 05',
            name: 'Google Maps Corridor Road Fleet & 3D Isometric LIFO Bay Packing',
            color: '#fbbc04',
            modality: 'Maps CVRPTW + 3D LIFO',
            systems: 'Google Maps Routes · OR-Tools 3D',
            ownerId: 'fleet_dispatch_mgr',
            ownerLabel: 'Fleet & Dispatch Manager',
            toilTime: '2.0 hrs/day',
            afterTime: '5 mins',
            before: '2D postcode routing creates spaghetti truck paths and paper dock sheets bury Stop-1 cargo behind Stop-5 cargo.',
            after: 'FleetFlow solves Google Maps corridor routes across 0.75t–24t trucks while CubeMaster 3D packs every bay in strict reverse-stop LIFO order.',
            goldenThread: 'Activates live multi-modal telemetry across Ocean, Air, Rail & Road in Stage 06 (SentinelMove).'
          },
          {
            num: 'Stage 06',
            name: 'Multi-Modal In-Transit Control Tower & Automated Freight Audit',
            color: '#ea4335',
            modality: 'AIS/ADS-B/GPS + DocAI',
            systems: 'Project44 · Maps Geofence · SAP AP',
            ownerId: 'freight_claims_analyst',
            ownerLabel: 'Freight & Exceptions Analyst',
            toilTime: '2.5 hrs/day',
            afterTime: '10 mins',
            before: 'In-transit excursions and 3–5% carrier billing overcharges across ocean, air, rail, and road go undetected.',
            after: 'SentinelMove predicts ETA/thermal drift 45+ mins early and audits 100% of carrier bills against Google Maps geofences and contract rates.',
            goldenThread: 'Closes the Golden Thread by feeding verified multi-modal transit times and landed costs back to Stage 01.'
          }
        ]
      },
      s2p: {
        id: 's2p',
        shortTitle: 'Source-to-Pay Resilience (S2P)',
        title: 'Source-to-Pay & Tier-N Resilience (S2P) Suite',
        flowBadge: 'End-to-End Sub-Tier Sourcing-to-Settlement Pipeline',
        cardSubtitle: 'Unifies Multi-Tier BOM Risk Mapping, Parametric Should-Cost RFQ, Contract Rebate Audit, HS Tariff Engineering & Inbound COA Quality.',
        cardFooterLeft: '6 Stages · 4 Sourcing Personas',
        color: '#a142f4',
        cadType: 'supplier_radar',
        headlineStat: '-6.8% Spend',
        headlineLabel: 'Direct Material Spend & +11 Days Disruption Lead',
        toilHoursBefore: '3-week manual RFQ spreadsheets & blind Tier-2/Tier-3 exposure',
        toilHoursAfter: '15-minute parametric RFQ + continuous Tier-N & COA guard',
        summary: 'Eliminates commercial value leakage and sub-tier blind spots across the entire direct/indirect procurement lifecycle—from Tier-4 raw materials to customs clearance and quality settlement.',
        focusAreas: ['Tier-1 to Tier-4 Supply Graph', 'Parametric BOM Should-Cost', 'HS Tariff & Rebate Audit', 'Predictive COA Quality'],
        videoSrc: 'videos/o2d_suite_demo.mp4',
        hasPreloadedVideo: true,
        problem: 'Procurement teams negotiate without bottom-up should-cost models, discover Tier-2 disruptions only after factory lines stop, and lose millions to unrecovered rebates and out-of-spec lots.',
        solution: 'Connects NexusShield Tier-N mapping, SourcePulse parametric RFQ, ClauseGuard tariff/rebate audit, and QualiShield COA inspection into one autonomous Source-to-Pay loop.',
        advantage: 'Reduces direct material spend by 6.8%, detects sub-tier disruptions 11 days earlier, and cuts inbound defect escapes by 64%.',
        stages: [
          {
            num: 'Stage 01',
            name: 'Multi-Tier (Tier-1 to Tier-4) Supply Graph Mapping',
            color: '#a142f4',
            modality: 'Knowledge Graph GNN',
            systems: 'Customs BOL · SAP BOM · Resilinc',
            ownerId: 'supplier_risk_lead',
            ownerLabel: 'Supplier Risk & Resilience Lead',
            toilTime: '2.0 hrs/day',
            afterTime: '5 mins',
            before: 'Sub-tier (Tier-2 / Tier-3) raw material bottlenecks remain invisible until Tier-1 misses factory delivery.',
            after: 'NexusShield maps Tier-1 to Tier-4 dependencies continuously and traces BOM revenue at risk in seconds.',
            goldenThread: 'Passes qualified multi-tier supplier risk scores & dual-source targets to Stage 02 (SourcePulse).'
          },
          {
            num: 'Stage 02',
            name: 'Parametric BOM Should-Cost Tear-Down',
            color: '#a142f4',
            modality: 'Parametric Cost AI',
            systems: 'Teamcenter BOM · LME/ICIS Indices',
            ownerId: 'category_sourcing_mgr',
            ownerLabel: 'Category Sourcing Manager',
            toilTime: '2.0 hrs/day',
            afterTime: '10 mins',
            before: 'Category buyers benchmark supplier bids only against historical PO prices, missing raw commodity drops.',
            after: 'SourcePulse decomposes every BOM part into raw material, machine cycle time, labor, and overhead should-costs.',
            goldenThread: 'Feeds component-level should-cost targets into Stage 03 (Combinatorial RFQ Solver).'
          },
          {
            num: 'Stage 03',
            name: 'Multi-Bid Normalization & Combinatorial Award',
            color: '#4285f4',
            modality: 'Combinatorial MILP',
            systems: 'SAP Ariba · Coupa · Supplier Quotes',
            ownerId: 'category_sourcing_mgr',
            ownerLabel: 'Category Sourcing Manager',
            toilTime: '2.5 hrs/day',
            afterTime: '10 mins',
            before: 'Days spent manually copying 40 inconsistent supplier PDF and Excel quotes into comparison sheets.',
            after: 'Normalizes all bids onto one landed-cost matrix and solves optimal dual-source award splits under MOQ/risk rules.',
            goldenThread: 'Commits awarded contract terms and rebate tiers to Stage 04 (ClauseGuard Compliance).'
          },
          {
            num: 'Stage 04',
            name: 'HS Tariff Engineering & FTA Duty Optimization',
            color: '#00d2ff',
            modality: 'Legal RAG + TARIC',
            systems: 'SAP GTS · USITC / EU TARIC',
            ownerId: 'tariff_compliance_spec',
            ownerLabel: 'Contract & Trade Compliance Specialist',
            toilTime: '2.0 hrs/day',
            afterTime: '10 mins',
            before: 'Manual Harmonized System (HS) classification causes customs holds and misses Free Trade Agreement duty savings.',
            after: 'ClauseGuard assigns audit-ready 10-digit HS codes with legal rulings and qualifies FTA origin certificates.',
            goldenThread: 'Attaches verified customs & CAD tolerance specs to inbound POs for Stage 05 (QualiShield).'
          },
          {
            num: 'Stage 05',
            name: 'Predictive Inbound COA Quality & Cpk Screening',
            color: '#10b981',
            modality: 'Multimodal COA + SPC',
            systems: 'SAP QM · Supplier COA Portal',
            ownerId: 'supplier_quality_lead',
            ownerLabel: 'Supplier Quality & PPAP Lead',
            toilTime: '2.0 hrs/day',
            afterTime: '5 mins',
            before: 'Out-of-spec supplier lots slip past manual PDF COA reviews and fixed sampling, causing factory line stops.',
            after: 'QualiShield verifies 100% of inbound COA PDFs against CAD tolerances and flags SPC/Cpk drift prior to receipt.',
            goldenThread: 'Releases quality-certified ASN receipts to Stage 06 for automated settlement.'
          },
          {
            num: 'Stage 06',
            name: 'Contract Rebate, Index Cap & COPQ Settlement',
            color: '#ff8c00',
            modality: '3-Way Match + CLM AI',
            systems: 'SAP S/4HANA AP · Icertis CLM',
            ownerId: 'tariff_compliance_spec',
            ownerLabel: 'Contract & Trade Compliance Specialist',
            toilTime: '2.0 hrs/day',
            afterTime: '10 mins',
            before: 'Earned volume rebates, commodity index caps, and poor-quality chargebacks leak unnoticed during AP payment.',
            after: 'Audits 100% of supplier invoices against contract indexation caps, rebate tiers, and 8D COPQ debit memos.',
            goldenThread: 'Updates supplier total-cost-of-ownership (TCO) scorecards back in Stage 01 & 02.'
          }
        ]
      },
      p2r: {
        id: 'p2r',
        shortTitle: 'Plan-to-Recovery Circular (P2R)',
        title: 'Plan-to-Recovery & Yard-to-Backhaul (P2R) Circular Suite',
        flowBadge: 'End-to-End DC Yard, Slotting & Reverse Circular Pipeline',
        cardSubtitle: 'Synchronizes CPFR Retail Signals, Autonomous Yard & Dock Sequencing, 3D Slotting, RMA Vision Grading & Fleet Backhaul Recovery.',
        cardFooterLeft: '6 Stages · Cross-Vertical Loop',
        color: '#00d2ff',
        cadType: 'warehouse_crane',
        headlineStat: '+31% Recovery',
        headlineLabel: 'Circular Return Margin & -41% Yard Dwell',
        toilHoursBefore: 'Clipboard yard queues, static racks & empty fleet return miles',
        toilHoursAfter: 'Synchronized Yard → 3D Slotting → Fleet Backhaul → Circular Restock',
        summary: 'Transforms the distribution center yard, warehouse floor, and reverse logistics loop into a single bidirectional engine—eliminating trailer detention and turning returns into immediate regional stock.',
        focusAreas: ['CPFR Phantom Stock Fix', 'Autonomous Yard & Dock Sync', '3D Golden-Zone Slotting', 'Fleet Backhaul RMA Recovery'],
        videoSrc: 'videos/smart_warehouse_demo.mp4',
        hasPreloadedVideo: true,
        problem: 'Trailers wait hours at yard gates, pickers walk miles across static racks, and outbound fleet trucks return empty while third-party LTL carriers haul ungraded customer returns.',
        solution: 'Links ChannelSync CPFR, YardPulse dock sequencing, SlotMaster 3D slotting, and ReturnLoop fleet backhaul recovery in one closed-loop operational pipeline.',
        advantage: 'Cuts trailer yard dwell by 41%, reduces picker travel by 28%, and boosts net margin recovery on returned goods by 31%.',
        stages: [
          {
            num: 'Stage 01',
            name: 'CPFR Retail POS & Phantom Inventory Sync',
            color: '#10b981',
            modality: 'EDI 852 + Poisson AI',
            systems: 'Retail Portals · EDI 852 · BigQuery',
            ownerId: 'cpfr_channel_mgr',
            ownerLabel: 'CPFR & Retail Channel Lead',
            toilTime: '2.0 hrs/day',
            afterTime: '5 mins',
            before: 'Incompatible retail portal spreadsheets hide store phantom inventory and create sudden replenishment spikes.',
            after: 'ChannelSync harmonizes daily store POS scans, flags zero-scan phantom stock, and locks joint VMI waves.',
            goldenThread: 'Streams prioritized inbound/outbound wave schedules to Stage 02 (YardPulse Dock Sequencer).'
          },
          {
            num: 'Stage 02',
            name: 'Autonomous Gate, Yard Jockey & Dock Door Sequencing',
            color: '#00d2ff',
            modality: 'Bipartite Yard Solver',
            systems: 'Manhattan YMS · Gate ANPR · GPS',
            ownerId: 'dock_yard_supervisor',
            ownerLabel: 'Dock & Yard Operations Lead',
            toilTime: '2.0 hrs/day',
            afterTime: '5 mins',
            before: 'Whiteboard dock assignments ignore interior rack proximity and live truck ETAs, causing detention bills.',
            after: 'YardPulse assigns every arriving trailer to the optimal dock door and sequences yard hostler moves.',
            goldenThread: 'Triggers synchronized cross-dock and putaway waves in Stage 03 (SlotMaster 3D Twin).'
          },
          {
            num: 'Stage 03',
            name: '3D Golden-Zone Affinity Slotting & Wave Throttling',
            color: '#00d2ff',
            modality: '3D Spatial Twin',
            systems: 'WMS · AS/RS WCS · RF Pickers',
            ownerId: 'warehouse_slotting_lead',
            ownerLabel: 'Warehouse & Slotting Ops Lead',
            toilTime: '2.5 hrs/day',
            afterTime: '15 mins',
            before: 'Fast-moving co-ordered SKUs sit in distant upper bays while unthrottled waves gridlock aisles.',
            after: 'SlotMaster mines order-line affinity to slot Golden-Zone pick faces and throttles waves to prevent congestion.',
            goldenThread: 'Aligns outbound staged loads with returning fleet capacity in Stage 04 (ReturnLoop).'
          },
          {
            num: 'Stage 04',
            name: 'Fleet Backhaul Milk-Run & RMA Pickup Insertion',
            color: '#ff8c00',
            modality: 'Backhaul CVRPTW',
            systems: 'Blue Yonder TMS · FleetFlow GPS',
            ownerId: 'reverse_logistics_mgr',
            ownerLabel: 'Reverse Logistics & Circularity Lead',
            toilTime: '2.0 hrs/day',
            afterTime: '10 mins',
            before: 'Outbound fleet trucks return empty while expensive third-party LTL carriers are hired for customer returns.',
            after: 'ReturnLoop injects customer RMA and reusable pallet pickups directly into returning corridor fleet vehicles.',
            goldenThread: 'Delivers consolidated return loads to edge grading kiosks in Stage 05.'
          },
          {
            num: 'Stage 05',
            name: 'Multimodal Vision Grading & Disposition Routing',
            color: '#a142f4',
            modality: 'Gemini Multimodal Vision',
            systems: 'Vision Kiosks · Loop RMA · WMS',
            ownerId: 'reverse_logistics_mgr',
            ownerLabel: 'Reverse Logistics & Circularity Lead',
            toilTime: '2.0 hrs/day',
            afterTime: '10 mins',
            before: 'All returns ship blindly to a central depot before inspection, delaying Grade-A restock by 3+ weeks.',
            after: 'Classifies returns via multimodal vision into Grade-A immediate restock, refurbish, or supplier warranty claim.',
            goldenThread: 'Routes Grade-A stock into regional ATP pools and defect data into Stage 06.'
          },
          {
            num: 'Stage 06',
            name: 'Supplier Defect Chargeback & Circular Margin Ledger',
            color: '#10b981',
            modality: '8D CAPA + ERP Ledger',
            systems: 'SAP QM · ERP AR/AP · MEIO',
            ownerId: 'supplier_quality_lead',
            ownerLabel: 'Supplier Quality & PPAP Lead',
            toilTime: '1.5 hrs/day',
            afterTime: '10 mins',
            before: 'Field return write-offs are absorbed because RMA defect codes are never linked back to supplier lot warranties.',
            after: 'Links field RMA spikes to supplier production lots, triggers 8D CAPAs, and posts automated warranty debit memos.',
            goldenThread: 'Updates net recoverable inventory in EchelonFlow MEIO and PromiseGuard ATP.'
          }
        ]
      }
    };

    /* BASE64 EMBEDDED DESIGN ASSETS (BRAND LOGOS & SPARKLES ONLY) */
    const EMBEDDED_WEBP_BLOBS = __EMBEDDED_WEBP_BLOBS__;
    const EMBEDDED_TWINS = __EMBEDDED_TWINS_JSON__;

    const EMBEDDED_ASSET_MAP = {
      "gemini_enterprise_dark.png": "gemini_enterprise_dark.webp",
      "google_cloud_logo.png": "google_cloud_logo.webp",
      "sparkle_blue_violet.png": "sparkle_blue_violet.webp"
    };

    function resolveAsset(path) {
      if (!path) return '';
      const mapped = EMBEDDED_ASSET_MAP[path] || path;
      return EMBEDDED_WEBP_BLOBS[mapped] || path;
    }

    function hydrateAssets() {
      document.querySelectorAll('[data-asset]').forEach(el => {
        const asset = el.getAttribute('data-asset');
        const resolved = resolveAsset(asset);
        if (resolved && el.getAttribute('src') !== resolved) {
          el.setAttribute('src', resolved);
        }
      });
    }

    /* =========================================================================
       60FPS HERO SUPPLY CHAIN CANVAS:
       LARGE, SEAMLESSLY CONNECTED END-TO-END SUPPLY CHAIN TAPESTRY
       (DEMAND WAVE + 3D WMS CONVEYOR & AS/RS RACK + TIER-N FACTORY + MULTI-MODAL HUB
        LINKED BY CONTINUOUS CROSS-CANVAS AMBIENT TELEMETRY STREAMS)
       ========================================================================= */
    function initHeroSupplyChainCanvas() {
      const canvas = document.getElementById('heroSupplyChainCanvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      let w = 1440, h = 900;

      function resize() {
        const rect = canvas.parentElement.getBoundingClientRect();
        w = Math.max(800, rect.width || window.innerWidth);
        h = Math.max(600, rect.height || window.innerHeight);
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        canvas.width = w * dpr;
        canvas.height = h * dpr;
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      }
      resize();
      window.addEventListener('resize', resize);

      // Helper to draw a clean 3D isometric box at screen (cx, cy)
      function drawIsoBox(cx, cy, lx, ly, hz, topCol, leftCol, rightCol, strokeCol, alpha = 1) {
        ctx.save();
        ctx.globalAlpha = alpha;
        const isoX = (u, v) => cx + (u - v) * 0.866;
        const isoY = (u, v, z) => cy + (u + v) * 0.5 - z;

        // Top face
        ctx.beginPath();
        ctx.moveTo(isoX(0, 0), isoY(0, 0, hz));
        ctx.lineTo(isoX(lx, 0), isoY(lx, 0, hz));
        ctx.lineTo(isoX(lx, ly), isoY(lx, ly, hz));
        ctx.lineTo(isoX(0, ly), isoY(0, ly, hz));
        ctx.closePath();
        ctx.fillStyle = topCol;
        ctx.fill();
        ctx.strokeStyle = strokeCol;
        ctx.lineWidth = 1.25;
        ctx.stroke();

        // Left-front face (u from 0..lx, v=ly)
        ctx.beginPath();
        ctx.moveTo(isoX(0, ly), isoY(0, ly, hz));
        ctx.lineTo(isoX(lx, ly), isoY(lx, ly, hz));
        ctx.lineTo(isoX(lx, ly), isoY(lx, ly, 0));
        ctx.lineTo(isoX(0, ly), isoY(0, ly, 0));
        ctx.closePath();
        ctx.fillStyle = leftCol;
        ctx.fill();
        ctx.stroke();

        // Right-front face (u=lx, v from 0..ly)
        ctx.beginPath();
        ctx.moveTo(isoX(lx, 0), isoY(lx, 0, hz));
        ctx.lineTo(isoX(lx, ly), isoY(lx, ly, hz));
        ctx.lineTo(isoX(lx, ly), isoY(lx, ly, 0));
        ctx.lineTo(isoX(lx, 0), isoY(lx, 0, 0));
        ctx.closePath();
        ctx.fillStyle = rightCol;
        ctx.fill();
        ctx.stroke();
        ctx.restore();
      }

      // Helper to evaluate cubic Bezier point at u in [0,1]
      function bezierPt(u, x0, y0, x1, y1, x2, y2, x3, y3) {
        const inv = 1 - u;
        return {
          x: inv*inv*inv*x0 + 3*inv*inv*u*x1 + 3*inv*u*u*x2 + u*u*u*x3,
          y: inv*inv*inv*y0 + 3*inv*inv*u*y1 + 3*inv*u*u*y2 + u*u*u*y3
        };
      }

      const boxes = [
        { offset: 0.00, col: ['#38bdf8', '#0284c7', '#0369a1'], stroke: '#bae6fd', h: 32 },
        { offset: 0.14, col: ['#34d399', '#059669', '#047857'], stroke: '#a7f3d0', h: 36 },
        { offset: 0.28, col: ['#fbbf24', '#d97706', '#b45309'], stroke: '#fde68a', h: 28 },
        { offset: 0.43, col: ['#c084fc', '#9333ea', '#7e22ce'], stroke: '#e9d5ff', h: 34 },
        { offset: 0.57, col: ['#60a5fa', '#2563eb', '#1d4ed8'], stroke: '#bfdbfe', h: 30 },
        { offset: 0.72, col: ['#2dd4bf', '#0d9488', '#0f766e'], stroke: '#99f6e4', h: 35 },
        { offset: 0.86, col: ['#f472b6', '#db2777', '#be185d'], stroke: '#fbcfe8', h: 29 }
      ];

      function renderFrame(now) {
        const t = now * 0.001;
        ctx.clearRect(0, 0, w, h);

        // 1. Continuous Isometric Supply Chain Perspective Grid (softly breathing)
        ctx.strokeStyle = 'rgba(0, 210, 255, 0.05)';
        ctx.lineWidth = 1;
        const step = 84;
        const gridShift = (t * 12) % step;
        for (let x = -h + gridShift; x < w + h; x += step) {
          ctx.beginPath();
          ctx.moveTo(x, 0);
          ctx.lineTo(x + h * 0.866, h);
          ctx.stroke();
          ctx.beginPath();
          ctx.moveTo(x, 0);
          ctx.lineTo(x - h * 0.866, h);
          ctx.stroke();
        }

        // Key hub anchor coordinates forming a seamless 360-degree supply chain circuit
        const demandHubX = w * 0.205;
        const demandHubY = h * 0.24;

        const wmsHubX = w * 0.215;
        const wmsHubY = h * 0.68;

        const tierHubX = w * 0.825;
        const tierHubY = h * 0.22;

        const hubX = w * 0.835;
        const hubY = h * 0.58;
        const spanR = Math.min(210, w * 0.155);

        // 2. SEAMLESS 360° HUB-TO-HUB CROSS-CANVAS SUPPLY CHAIN STREAMS
        const ambientStreams = [
          // Top arc: Demand & S&OP Hub (Top-Left) -> Smart Plant & Tier-N Hub (Top-Right)
          {
            x0: demandHubX, y0: demandHubY,
            x1: w * 0.40, y1: h * 0.05,
            x2: w * 0.62, y2: h * 0.05,
            x3: tierHubX, y3: tierHubY + 18,
            col: 'rgba(16, 185, 129, 0.24)',
            pulseCol: '#34d399',
            speed: 0.10,
            phase: 0.0
          },
          // Upper-mid diagonal: Demand & S&OP Hub (Top-Left) -> Multi-Modal Hub (Bottom-Right)
          {
            x0: demandHubX, y0: demandHubY,
            x1: w * 0.44, y1: h * 0.17,
            x2: w * 0.64, y2: h * 0.34,
            x3: hubX, y3: hubY,
            col: 'rgba(0, 210, 255, 0.16)',
            pulseCol: '#00d2ff',
            speed: 0.085,
            phase: 0.35
          },
          // Left vertical replenishment link: Demand & S&OP Hub (Top-Left) -> 3D WMS Fulfillment Hub (Bottom-Left)
          {
            x0: demandHubX, y0: demandHubY,
            x1: w * 0.14, y1: h * 0.40,
            x2: w * 0.15, y2: h * 0.54,
            x3: wmsHubX, y3: wmsHubY,
            col: 'rgba(56, 189, 248, 0.22)',
            pulseCol: '#38bdf8',
            speed: 0.14,
            phase: 0.15
          },
          // Lower outbound arc: 3D WMS Fulfillment Hub (Bottom-Left) -> Multi-Modal Global Hub (Bottom-Right)
          {
            x0: wmsHubX, y0: wmsHubY,
            x1: w * 0.42, y1: h * 0.88,
            x2: w * 0.64, y2: h * 0.86,
            x3: hubX, y3: hubY,
            col: 'rgba(0, 210, 255, 0.25)',
            pulseCol: '#38bdf8',
            speed: 0.11,
            phase: 0.2
          },
          // Bottom reverse-logistics / circularity arc: Multi-Modal Hub (Bottom-Right) -> 3D WMS Hub (Bottom-Left)
          {
            x0: hubX, y0: hubY,
            x1: w * 0.62, y1: h * 0.95,
            x2: w * 0.40, y2: h * 0.95,
            x3: wmsHubX, y3: wmsHubY,
            col: 'rgba(161, 66, 244, 0.20)',
            pulseCol: '#c084fc',
            speed: 0.08,
            phase: 0.65
          }
        ];

        ctx.save();
        ambientStreams.forEach(s => {
          // Soft outer glow ribbon
          ctx.beginPath();
          ctx.moveTo(s.x0, s.y0);
          ctx.bezierCurveTo(s.x1, s.y1, s.x2, s.y2, s.x3, s.y3);
          ctx.strokeStyle = s.col;
          ctx.lineWidth = 4.5;
          ctx.stroke();

          // Dashed core telemetry line
          ctx.beginPath();
          ctx.moveTo(s.x0, s.y0);
          ctx.bezierCurveTo(s.x1, s.y1, s.x2, s.y2, s.x3, s.y3);
          ctx.strokeStyle = s.col;
          ctx.setLineDash([6, 8]);
          ctx.lineWidth = 1.5;
          ctx.stroke();
          ctx.setLineDash([]);

          // 3 flowing telemetry packets per cross-canvas stream
          [0, 0.33, 0.66].forEach(offset => {
            const u = (t * s.speed + s.phase + offset) % 1;
            const pt = bezierPt(u, s.x0, s.y0, s.x1, s.y1, s.x2, s.y2, s.x3, s.y3);
            ctx.beginPath();
            ctx.arc(pt.x, pt.y, 6, 0, Math.PI * 2);
            ctx.fillStyle = s.pulseCol + '28';
            ctx.fill();
            ctx.beginPath();
            ctx.arc(pt.x, pt.y, 2.6, 0, Math.PI * 2);
            ctx.fillStyle = s.pulseCol;
            ctx.fill();
          });
        });
        ctx.restore();

        // 3. TOP-LEFT WING: Seamlessly Tapered Demand Sensing Wave + S&OP Signals Hub (Zero Hard Vertical Edges)
        ctx.save();
        const waveStartX = -12;
        const waveEndX = demandHubX;
        const waveSpan = waveEndX - waveStartX;
        const waveSteps = 60;

        const waveCenterY = (i) => {
          const u = i / waveSteps;
          // Taper wave oscillation gently as it converges into the Demand Hub
          const amp = Math.sin(u * Math.PI);
          return demandHubY + (Math.sin(i * 0.20 - t * 2.0) * 28 + Math.cos(i * 0.11 + t) * 12) * (0.35 + 0.65 * amp);
        };

        // Tapered P10-P90 Confidence Fan (pinches to 0 at both ends so there is never a flat vertical cut)
        ctx.beginPath();
        for (let i = 0; i <= waveSteps; i++) {
          const u = i / waveSteps;
          const px = waveStartX + u * waveSpan;
          const band = Math.sin(u * Math.PI) * 34;
          const py = waveCenterY(i) - band;
          if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
        }
        for (let i = waveSteps; i >= 0; i--) {
          const u = i / waveSteps;
          const px = waveStartX + u * waveSpan;
          const band = Math.sin(u * Math.PI) * 34;
          const py = waveCenterY(i) + band;
          ctx.lineTo(px, py);
        }
        ctx.closePath();
        const fanGrad = ctx.createLinearGradient(0, demandHubY, waveEndX, demandHubY);
        fanGrad.addColorStop(0.0, 'rgba(16, 185, 129, 0.0)');
        fanGrad.addColorStop(0.25, 'rgba(16, 185, 129, 0.14)');
        fanGrad.addColorStop(0.75, 'rgba(0, 210, 255, 0.14)');
        fanGrad.addColorStop(1.0, 'rgba(0, 210, 255, 0.0)');
        ctx.fillStyle = fanGrad;
        ctx.fill();

        // Tapered P90 Upper Bound Curve
        ctx.beginPath();
        for (let i = 0; i <= waveSteps; i++) {
          const u = i / waveSteps;
          const px = waveStartX + u * waveSpan;
          const py = waveCenterY(i) - Math.sin(u * Math.PI) * 24;
          if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
        }
        const strokeGrad = ctx.createLinearGradient(0, demandHubY, waveEndX, demandHubY);
        strokeGrad.addColorStop(0.0, 'rgba(52, 211, 153, 0.0)');
        strokeGrad.addColorStop(0.2, 'rgba(52, 211, 153, 0.78)');
        strokeGrad.addColorStop(0.85, 'rgba(0, 210, 255, 0.82)');
        strokeGrad.addColorStop(1.0, 'rgba(0, 210, 255, 0.25)');
        ctx.strokeStyle = 'rgba(52, 211, 153, 0.26)';
        ctx.setLineDash([4, 6]);
        ctx.lineWidth = 1.4;
        ctx.stroke();
        ctx.setLineDash([]);

        // Primary P50 TimesFM Demand Wave (feathered gradient stroke flowing directly into Demand Hub)
        ctx.beginPath();
        for (let i = 0; i <= waveSteps; i++) {
          const u = i / waveSteps;
          const px = waveStartX + u * waveSpan;
          const py = waveCenterY(i);
          if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
        }
        ctx.strokeStyle = strokeGrad;
        ctx.lineWidth = 2.8;
        ctx.stroke();

        // Moving demand sensing pulse dots along wave
        [0, 20, 40].forEach(offset => {
          const waveIdx = ((t * 10 + offset) % waveSteps);
          const u = waveIdx / waveSteps;
          const wPx = waveStartX + u * waveSpan;
          const wPy = waveCenterY(waveIdx);
          const dotAlpha = Math.sin(u * Math.PI);
          ctx.save();
          ctx.globalAlpha = dotAlpha;
          ctx.beginPath();
          ctx.arc(wPx, wPy, 10, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(52, 211, 153, 0.22)';
          ctx.fill();
          ctx.beginPath();
          ctx.arc(wPx, wPy, 4.5, 0, Math.PI * 2);
          ctx.fillStyle = '#34d399';
          ctx.fill();
          ctx.restore();
        });

        // Curved feeder signals into Demand & S&OP Hub
        const demandFeeders = [
          { name: 'POS & PROMO SIGNALS', col: '#34d399', sx: demandHubX - 115, sy: demandHubY - 82, cpx: demandHubX - 45, cpy: demandHubY - 64 },
          { name: 'WEATHERNEXT 3 · AI', col: '#00d2ff', sx: demandHubX - 88, sy: demandHubY + 86, cpx: demandHubX - 32, cpy: demandHubY + 62 }
        ];
        demandFeeders.forEach((df, idx) => {
          ctx.beginPath();
          ctx.moveTo(df.sx, df.sy);
          ctx.quadraticCurveTo(df.cpx, df.cpy, demandHubX, demandHubY);
          ctx.strokeStyle = df.col + '55';
          ctx.lineWidth = 2;
          ctx.stroke();

          ctx.beginPath();
          ctx.arc(df.sx, df.sy, 5.5, 0, Math.PI * 2);
          ctx.fillStyle = '#070b14';
          ctx.fill();
          ctx.strokeStyle = df.col;
          ctx.lineWidth = 2;
          ctx.stroke();

          ctx.fillStyle = df.col;
          ctx.font = '700 9.5px "Google Sans", sans-serif';
          ctx.fillText(df.name, Math.max(18, df.sx - 28), df.sy < demandHubY ? df.sy - 10 : df.sy + 18);
        });

        // Glowing Demand & S&OP Hub Node
        [42, 78].forEach(rad => {
          ctx.beginPath();
          ctx.arc(demandHubX, demandHubY, rad, 0, Math.PI * 2);
          ctx.strokeStyle = 'rgba(16, 185, 129, 0.08)';
          ctx.setLineDash([4, 6]);
          ctx.lineWidth = 1.1;
          ctx.stroke();
        });
        ctx.setLineDash([]);

        ctx.beginPath();
        ctx.arc(demandHubX, demandHubY, 15, 0, Math.PI * 2);
        ctx.fillStyle = '#081020';
        ctx.fill();
        ctx.strokeStyle = '#10b981';
        ctx.lineWidth = 2.8;
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(demandHubX, demandHubY, 5.5, 0, Math.PI * 2);
        ctx.fillStyle = '#34d399';
        ctx.fill();

        ctx.fillStyle = 'rgba(52, 211, 153, 0.90)';
        ctx.font = '700 10px "Google Sans", sans-serif';
        ctx.fillText('DEMAND & S&OP HUB', demandHubX - 52, demandHubY - 22);
        ctx.restore();

        // 4. BOTTOM-LEFT WING: Feathered 3D Isometric WMS Stream + Fulfillment Hub (Zero Hard Corners)
        ctx.save();
        // Radar rings around the 3D WMS & Fulfillment Hub so Left and Right wings are visually balanced
        [52, 98, 146].forEach((rad, rIdx) => {
          ctx.beginPath();
          ctx.arc(wmsHubX, wmsHubY, rad, 0, Math.PI * 2);
          ctx.strokeStyle = rIdx % 2 === 0 ? 'rgba(0, 210, 255, 0.08)' : 'rgba(255, 255, 255, 0.04)';
          ctx.setLineDash([5, 7]);
          ctx.lineWidth = 1.1;
          ctx.stroke();
        });
        ctx.setLineDash([]);

        // Curved warehouse automation branches around the WMS Hub
        const wmsBranches = [
          { name: 'AS/RS ROBOTICS', col: '#38bdf8', ex: wmsHubX - 95, ey: wmsHubY + 115, cpx: wmsHubX - 52, cpy: wmsHubY + 65 },
          { name: 'CROSS-DOCK SORT', col: '#10b981', ex: wmsHubX + 54, ey: wmsHubY + 125, cpx: wmsHubX + 28, cpy: wmsHubY + 68 }
        ];
        wmsBranches.forEach((wb, bIdx) => {
          ctx.beginPath();
          ctx.moveTo(wmsHubX, wmsHubY);
          ctx.quadraticCurveTo(wb.cpx, wb.cpy, wb.ex, wb.ey);
          ctx.strokeStyle = wb.col + '66';
          ctx.lineWidth = 2.2;
          ctx.stroke();

          ctx.beginPath();
          ctx.arc(wb.ex, wb.ey, 6, 0, Math.PI * 2);
          ctx.fillStyle = '#070b14';
          ctx.fill();
          ctx.strokeStyle = wb.col;
          ctx.lineWidth = 2;
          ctx.stroke();

          ctx.fillStyle = wb.col;
          ctx.font = '700 9.5px "Google Sans", sans-serif';
          ctx.fillText(wb.name, Math.max(18, wb.ex - 36), wb.ey + 18);
        });

        // Feathered 3D Isometric Conveyor Track feeding directly into (wmsHubX, wmsHubY)
        const dirX = 0.866;
        const dirY = 0.5;
        const convLen = Math.min(310, w * 0.21);
        const perpX = -0.866 * 36;
        const perpY = 0.5 * 36;
        // Center the end of the conveyor right at (wmsHubX, wmsHubY)
        const convEndX = wmsHubX - perpX * 0.5;
        const convEndY = wmsHubY - perpY * 0.5;
        const convStartX = convEndX - convLen * dirX;
        const convStartY = convEndY - convLen * dirY;

        // Linear gradients along the conveyor so both ends fade smoothly to 0 opacity (zero hard edges!)
        const deckGrad = ctx.createLinearGradient(convStartX, convStartY, convEndX, convEndY);
        deckGrad.addColorStop(0.0, 'rgba(14, 24, 42, 0.0)');
        deckGrad.addColorStop(0.22, 'rgba(14, 24, 42, 0.78)');
        deckGrad.addColorStop(0.78, 'rgba(14, 24, 42, 0.78)');
        deckGrad.addColorStop(1.0, 'rgba(14, 24, 42, 0.0)');

        const railGrad = ctx.createLinearGradient(convStartX, convStartY, convEndX, convEndY);
        railGrad.addColorStop(0.0, 'rgba(0, 210, 255, 0.0)');
        railGrad.addColorStop(0.22, 'rgba(0, 210, 255, 0.58)');
        railGrad.addColorStop(0.78, 'rgba(0, 210, 255, 0.58)');
        railGrad.addColorStop(1.0, 'rgba(0, 210, 255, 0.0)');

        // Conveyor surface (feathered fill, no hard end-cap lines)
        ctx.beginPath();
        ctx.moveTo(convStartX, convStartY);
        ctx.lineTo(convEndX, convEndY);
        ctx.lineTo(convEndX + perpX, convEndY + perpY);
        ctx.lineTo(convStartX + perpX, convStartY + perpY);
        ctx.closePath();
        ctx.fillStyle = deckGrad;
        ctx.fill();

        // Stroke only the two long rails with feathered gradient (no sharp start/end cutoff lines!)
        ctx.strokeStyle = railGrad;
        ctx.lineWidth = 2.0;
        ctx.beginPath();
        ctx.moveTo(convStartX, convStartY);
        ctx.lineTo(convEndX, convEndY);
        ctx.moveTo(convStartX + perpX, convStartY + perpY);
        ctx.lineTo(convEndX + perpX, convEndY + perpY);
        ctx.stroke();

        // Feathered animated conveyor rollers
        const rollerShift = (t * 44) % 24;
        ctx.lineWidth = 1.2;
        for (let d = rollerShift; d < convLen; d += 24) {
          const u = d / convLen;
          const rAlpha = Math.sin(u * Math.PI) * 0.28;
          ctx.strokeStyle = `rgba(0, 210, 255, ${rAlpha.toFixed(3)})`;
          const rx = convStartX + d * dirX;
          const ry = convStartY + d * dirY;
          ctx.beginPath();
          ctx.moveTo(rx, ry);
          ctx.lineTo(rx + perpX, ry + perpY);
          ctx.stroke();
        }

        // 4 well-spaced, sleek 3D cargo parcels that smoothly fade in and dissolve into the WMS Hub
        const sleekBoxes = [
          { offset: 0.00, col: ['#38bdf8', '#0284c7', '#0369a1'], stroke: '#bae6fd', h: 24 },
          { offset: 0.25, col: ['#34d399', '#059669', '#047857'], stroke: '#a7f3d0', h: 27 },
          { offset: 0.50, col: ['#60a5fa', '#2563eb', '#1d4ed8'], stroke: '#bfdbfe', h: 23 },
          { offset: 0.75, col: ['#c084fc', '#9333ea', '#7e22ce'], stroke: '#e9d5ff', h: 26 }
        ];

        const activeBoxes = sleekBoxes.map(b => {
          const prog = (b.offset + t * 0.10) % 1;
          return { ...b, prog };
        }).sort((a, b) => a.prog - b.prog);

        activeBoxes.forEach(b => {
          const dist = b.prog * (convLen - 28);
          const bx = convStartX + dist * dirX - 13;
          const by = convStartY + dist * dirY + 4;
          // Smooth sine fade at both ends so boxes never pop abruptly at the edge!
          const boxAlpha = Math.pow(Math.sin(b.prog * Math.PI), 0.75);
          drawIsoBox(bx, by, 23, 20, b.h, b.col[0], b.col[1], b.col[2], b.stroke, boxAlpha);

          if (Math.abs(b.prog - 0.52) < 0.06) {
            ctx.save();
            ctx.globalAlpha = boxAlpha;
            ctx.beginPath();
            ctx.arc(bx, by - 10, 26, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(0, 210, 255, 0.22)';
            ctx.fill();
            ctx.restore();
          }
        });

        // Single clean 3D RFID / Vision Scanner Gate Arch over the midpoint of the conveyor
        const gateDist = convLen * 0.52;
        const gx1 = convStartX + gateDist * dirX;
        const gy1 = convStartY + gateDist * dirY;
        const gx2 = gx1 + perpX;
        const gy2 = gy1 + perpY;
        const archH = 52;
        ctx.strokeStyle = 'rgba(0, 210, 255, 0.80)';
        ctx.lineWidth = 2.2;
        ctx.beginPath();
        ctx.moveTo(gx1, gy1);
        ctx.lineTo(gx1, gy1 - archH);
        ctx.lineTo(gx2, gy2 - archH);
        ctx.lineTo(gx2, gy2);
        ctx.stroke();

        ctx.fillStyle = 'rgba(0, 210, 255, 0.12)';
        ctx.beginPath();
        ctx.moveTo(gx1, gy1 - archH);
        ctx.lineTo(gx2, gy2 - archH);
        ctx.lineTo(gx2, gy2);
        ctx.lineTo(gx1, gy1);
        ctx.closePath();
        ctx.fill();

        // Glowing 3D WMS & Fulfillment Hub Node at the outbound end of the conveyor
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

        ctx.fillStyle = 'rgba(248, 249, 250, 0.88)';
        ctx.font = '700 10px "Google Sans", sans-serif';
        ctx.fillText('3D WMS & FULFILLMENT HUB', wmsHubX - 64, wmsHubY - 24);
        ctx.restore();

        // 5. TOP-RIGHT WING: Tier-N Supplier & Smart Factory OEE Constellation
        ctx.save();
        const tierNodes = [
          { x: tierHubX - 115, y: tierHubY - 42, label: 'TIER-3 RAW', col: '#a142f4', r: 7 },
          { x: tierHubX - 35,  y: tierHubY - 62, label: 'TIER-2 FAB', col: '#00d2ff', r: 8 },
          { x: tierHubX + 68,  y: tierHubY - 34, label: 'TIER-1 SUB', col: '#34d399', r: 8 },
          { x: tierHubX,       y: tierHubY + 18, label: 'SMART PLANT · OEE 94%', col: '#fbbf24', r: 12 }
        ];
        const tierLinks = [
          [0, 1], [1, 2], [0, 3], [1, 3], [2, 3]
        ];
        tierLinks.forEach(([i, j], lIdx) => {
          const n1 = tierNodes[i], n2 = tierNodes[j];
          ctx.beginPath();
          ctx.moveTo(n1.x, n1.y);
          ctx.lineTo(n2.x, n2.y);
          ctx.strokeStyle = 'rgba(0, 210, 255, 0.28)';
          ctx.lineWidth = 1.8;
          ctx.stroke();

          const u = (t * 0.28 + lIdx * 0.21) % 1;
          const px = n1.x + (n2.x - n1.x) * u;
          const py = n1.y + (n2.y - n1.y) * u;
          ctx.beginPath();
          ctx.arc(px, py, 3.2, 0, Math.PI * 2);
          ctx.fillStyle = n2.col;
          ctx.fill();
        });

        // Stream connecting Smart Plant down into Multi-Modal Hub
        ctx.beginPath();
        ctx.moveTo(tierNodes[3].x, tierNodes[3].y);
        ctx.bezierCurveTo(tierHubX + 28, (tierHubY + hubY) * 0.45, hubX - 24, (tierHubY + hubY) * 0.65, hubX, hubY);
        ctx.strokeStyle = 'rgba(251, 191, 36, 0.32)';
        ctx.setLineDash([5, 6]);
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.setLineDash([]);

        tierNodes.forEach((n, idx) => {
          ctx.beginPath();
          ctx.arc(n.x, n.y, n.r + 8 + Math.sin(t * 2.5 + idx) * 3, 0, Math.PI * 2);
          ctx.strokeStyle = n.col + '44';
          ctx.lineWidth = 1.4;
          ctx.stroke();

          ctx.beginPath();
          ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
          ctx.fillStyle = '#081020';
          ctx.fill();
          ctx.strokeStyle = n.col;
          ctx.lineWidth = 2.4;
          ctx.stroke();

          ctx.fillStyle = n.col;
          ctx.font = '700 9.5px "Google Sans", sans-serif';
          ctx.fillText(n.label, Math.min(w - 135, n.x - 28), n.y - n.r - 8);
        });
        ctx.restore();

        // 6. MID/BOTTOM-RIGHT WING: Enlarged Multi-Modal Global Transit & Fleet Network
        [64, 122, 182, 240].forEach((rad, rIdx) => {
          ctx.beginPath();
          ctx.arc(hubX, hubY, rad, 0, Math.PI * 2);
          ctx.strokeStyle = rIdx % 2 === 0 ? 'rgba(0, 210, 255, 0.08)' : 'rgba(255, 255, 255, 0.05)';
          ctx.setLineDash([5, 7]);
          ctx.lineWidth = 1.2;
          ctx.stroke();
        });
        ctx.setLineDash([]);

        const corridors = [
          { name: 'OCEAN AIS · FEU', col: '#00d2ff', cpx1: hubX - 48, cpy1: hubY - 95, cpx2: hubX - 115, cpy2: hubY - 175, ex: hubX - spanR * 0.95, ey: hubY - 225, speed: 0.16, phase: 0.1 },
          { name: 'AIR CARGO · 3D ULD', col: '#a142f4', cpx1: hubX + 46, cpy1: hubY - 82, cpx2: hubX + 95, cpy2: hubY - 155, ex: Math.min(w - 36, hubX + spanR * 0.85), ey: hubY - 195, speed: 0.25, phase: 0.45 },
          { name: 'RAIL COFC · RAMP', col: '#10b981', cpx1: hubX - 52, cpy1: hubY + 88, cpx2: hubX - 118, cpy2: hubY + 165, ex: hubX - spanR * 0.90, ey: hubY + 215, speed: 0.19, phase: 0.7 },
          { name: 'MAPS ROAD · 3D LIFO', col: '#ff8c00', cpx1: hubX + 48, cpy1: hubY + 78, cpx2: hubX + 98, cpy2: hubY + 148, ex: Math.min(w - 36, hubX + spanR * 0.85), ey: hubY + 190, speed: 0.22, phase: 0.3 }
        ];

        corridors.forEach(c => {
          // Soft corridor aura
          ctx.beginPath();
          ctx.moveTo(hubX, hubY);
          ctx.bezierCurveTo(c.cpx1, c.cpy1, c.cpx2, c.cpy2, c.ex, c.ey);
          ctx.strokeStyle = c.col + '33';
          ctx.lineWidth = 6.5;
          ctx.stroke();

          // Crisp corridor route line
          ctx.beginPath();
          ctx.moveTo(hubX, hubY);
          ctx.bezierCurveTo(c.cpx1, c.cpy1, c.cpx2, c.cpy2, c.ex, c.ey);
          ctx.strokeStyle = c.col;
          ctx.lineWidth = 2.6;
          ctx.stroke();

          ctx.beginPath();
          ctx.arc(c.ex, c.ey, 7, 0, Math.PI * 2);
          ctx.fillStyle = '#070b14';
          ctx.fill();
          ctx.strokeStyle = c.col;
          ctx.lineWidth = 2.4;
          ctx.stroke();

          const labelX = Math.max(w * 0.70, Math.min(w - 138, c.ex - 44));
          const labelY = c.ey < hubY ? c.ey - 12 : c.ey + 22;
          ctx.fillStyle = c.col;
          ctx.font = '700 10.5px "Google Sans", sans-serif';
          ctx.fillText(c.name, labelX, labelY);

          // Moving Multi-Modal Carrier along Bezier curve
          const u = (t * c.speed + c.phase) % 1;
          const pt = bezierPt(u, hubX, hubY, c.cpx1, c.cpy1, c.cpx2, c.cpy2, c.ex, c.ey);

          ctx.beginPath();
          ctx.arc(pt.x, pt.y, 14, 0, Math.PI * 2);
          ctx.fillStyle = c.col + '33';
          ctx.fill();

          ctx.fillStyle = '#080d18';
          ctx.strokeStyle = c.col;
          ctx.lineWidth = 1.9;
          ctx.beginPath();
          ctx.roundRect(pt.x - 13, pt.y - 8, 26, 16, 4.5);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = c.col;
          ctx.fillRect(pt.x - 9, pt.y - 4.5, 12, 9);
        });

        // Central Multi-Modal Hub Node (Enlarged)
        ctx.beginPath();
        ctx.arc(hubX, hubY, 28, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(0, 210, 255, 0.14)';
        ctx.fill();

        ctx.beginPath();
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

        ctx.fillStyle = 'rgba(248, 249, 250, 0.90)';
        ctx.font = '700 10.5px "Google Sans", sans-serif';
        ctx.fillText('MULTI-MODAL HUB', hubX - 52, hubY + 34);

        requestAnimationFrame(renderFrame);
      }

      requestAnimationFrame(renderFrame);
    }

    /* =========================================================================
       ANIMATED SUPPLY CHAIN STAGE GRAPHICS (CLEARLY VISIBLE IN EACH VERTICAL CARD,
       BRIGHTEN ON HOVER, AND CLICK-TO-EXPAND)
       ========================================================================= */
    function renderSupplyChainWatermarkSvg(watermarkType, color, cssClass = 'dept-stage-svg') {
      if (watermarkType === 'tmd_retail_network') {
        return `<svg viewBox="0 0 320 118" class="${cssClass}" aria-hidden="true">
          <!-- Trade Marketing & Distribution: Retail Kirana/Storefront + Shelf Planogram + Laser Scanner + SFA Delivery Beat -->
          <!-- Retail Storefront Silhouette -->
          <polygon points="20,52 64,24 108,52" fill="${color}" fill-opacity="0.30" stroke="${color}" stroke-width="1.8" />
          <rect x="26" y="52" width="76" height="52" rx="4" fill="#081122" stroke="${color}" stroke-width="2" />
          <rect x="52" y="70" width="24" height="34" rx="2" fill="#0f172a" stroke="${color}" stroke-width="1.4" />
          <circle cx="70" cy="87" r="1.8" fill="${color}" />
          <!-- Store Awning Stripes -->
          <path d="M 22 52 L 28 62 L 36 62 L 30 52 Z M 38 52 L 44 62 L 52 62 L 46 52 Z M 54 52 L 60 62 L 68 62 L 62 52 Z M 70 52 L 76 62 L 84 62 L 78 52 Z M 86 52 L 92 62 L 100 62 L 94 52 Z" fill="${color}" fill-opacity="0.6" />
          
          <!-- Secondary Beat Route connecting Store to Distributor Hub -->
          <path d="M 104 84 C 132 84, 138 46, 172 46" fill="none" stroke="${color}" stroke-width="2.2" stroke-dasharray="4 3" class="sc-arc-flow" />
          <circle r="4" fill="#f59e0b">
            <animateMotion dur="2.8s" repeatCount="indefinite" path="M 104 84 C 132 84, 138 46, 172 46" />
          </circle>

          <!-- Planogram Shelf Matrix with Laser Scan Beam -->
          <rect x="176" y="24" width="130" height="80" rx="6" fill="#081122" stroke="${color}" stroke-width="2" />
          <!-- Shelf Level 1 -->
          <line x1="182" y1="50" x2="300" y2="50" stroke="#334155" stroke-width="1.8" />
          <rect x="186" y="32" width="16" height="18" rx="2" fill="#ef4444" fill-opacity="0.85" />
          <rect x="206" y="32" width="16" height="18" rx="2" fill="#ef4444" fill-opacity="0.85" />
          <rect x="226" y="32" width="16" height="18" rx="2" fill="${color}" />
          <rect x="246" y="32" width="16" height="18" rx="2" fill="${color}" />
          <rect x="266" y="34" width="14" height="16" rx="2" fill="#3b82f6" fill-opacity="0.7" />
          <rect x="284" y="34" width="14" height="16" rx="2" fill="#3b82f6" fill-opacity="0.7" />
          <!-- Shelf Level 2 -->
          <line x1="182" y1="76" x2="300" y2="76" stroke="#334155" stroke-width="1.8" />
          <rect x="186" y="56" width="20" height="20" rx="2" fill="#10b981" />
          <rect x="210" y="56" width="20" height="20" rx="2" fill="#10b981" />
          <rect x="234" y="56" width="20" height="20" rx="2" fill="#10b981" />
          <rect x="258" y="58" width="18" height="18" rx="2" fill="#a855f7" fill-opacity="0.8" />
          <rect x="280" y="58" width="18" height="18" rx="2" fill="#a855f7" fill-opacity="0.8" />
          <!-- Shelf Level 3 -->
          <rect x="186" y="82" width="24" height="18" rx="2" fill="${color}" />
          <rect x="214" y="82" width="24" height="18" rx="2" fill="${color}" />
          <rect x="242" y="82" width="24" height="18" rx="2" fill="#06b6d4" fill-opacity="0.8" />
          <rect x="270" y="82" width="24" height="18" rx="2" fill="#06b6d4" fill-opacity="0.8" />

          <!-- Dynamic Vision Planogram Scan Line -->
          <line x1="180" y1="28" x2="180" y2="100" stroke="#00d2ff" stroke-width="2.5" opacity="0.8">
            <animate attributeName="x1" values="182;298;182" dur="3.2s" repeatCount="indefinite" />
            <animate attributeName="x2" values="182;298;182" dur="3.2s" repeatCount="indefinite" />
          </line>
          
          <text x="12" y="18" fill="${color}" font-size="10.5" font-weight="700" letter-spacing="0.06em">FSO BEAT · PLANOGRAM VISION · DMS</text>
        </svg>`;
      }
      if (watermarkType === 'multi_echelon_buffer') {
        return `<svg viewBox="0 0 320 118" class="${cssClass}" aria-hidden="true">
          <!-- Multi-Echelon Inventory Optimization (MEIO): Plant Hub -> RDC -> Forward Hub -> Store Nodes + Buffer Gauges -->
          <!-- Lateral Flow Connections -->
          <line x1="42" y1="62" x2="122" y2="62" stroke="${color}" stroke-width="2.4" class="sc-arc-flow" />
          <line x1="122" y1="62" x2="202" y2="38" stroke="#00d2ff" stroke-width="2.4" class="sc-arc-flow" />
          <line x1="122" y1="62" x2="202" y2="86" stroke="#00d2ff" stroke-width="2.4" class="sc-arc-flow" />
          <line x1="202" y1="38" x2="278" y2="38" stroke="#10b981" stroke-width="2.2" class="sc-arc-flow" />
          <line x1="202" y1="86" x2="278" y2="86" stroke="#10b981" stroke-width="2.2" class="sc-arc-flow" />

          <!-- Tier 1: Central Plant Hub -->
          <circle cx="42" cy="62" r="16" fill="#081122" stroke="${color}" stroke-width="2.6" class="sc-node-pulse" />
          <text x="31" y="66" fill="#fff" font-size="9" font-weight="800">PLANT</text>
          <!-- Safety stock level gauge -->
          <rect x="28" y="84" width="28" height="6" rx="3" fill="#1e293b" />
          <rect x="28" y="84" width="22" height="6" rx="3" fill="${color}" />

          <!-- Tier 2: Regional DC -->
          <rect x="104" y="44" width="36" height="36" rx="8" fill="#081122" stroke="#00d2ff" stroke-width="2.4" class="sc-node-pulse" />
          <text x="111" y="66" fill="#00d2ff" font-size="9.5" font-weight="800">RDC</text>
          <rect x="108" y="84" width="28" height="6" rx="3" fill="#1e293b" />
          <rect x="108" y="84" width="18" height="6" rx="3" fill="#00d2ff" />

          <!-- Tier 3: Forward Fulfill Depots -->
          <rect x="188" y="24" width="28" height="28" rx="6" fill="#081122" stroke="#38bdf8" stroke-width="2" />
          <text x="194" y="41" fill="#38bdf8" font-size="8" font-weight="700">FDC-1</text>
          <rect x="188" y="72" width="28" height="28" rx="6" fill="#081122" stroke="#38bdf8" stroke-width="2" />
          <text x="194" y="89" fill="#38bdf8" font-size="8" font-weight="700">FDC-2</text>

          <!-- Tier 4: Edge Retail / POS Nodes -->
          <circle cx="278" cy="38" r="11" fill="#081122" stroke="#10b981" stroke-width="2" />
          <text x="270" y="41" fill="#10b981" font-size="7.5" font-weight="700">POS-A</text>
          <circle cx="278" cy="86" r="11" fill="#081122" stroke="#10b981" stroke-width="2" />
          <text x="270" y="89" fill="#10b981" font-size="7.5" font-weight="700">POS-B</text>

          <!-- Telemetry packet moving across echelons -->
          <circle r="4.5" fill="#ffffff">
            <animateMotion dur="2.4s" repeatCount="indefinite" path="M 42 62 L 122 62 L 202 38 L 278 38" />
          </circle>
          <text x="14" y="20" fill="${color}" font-size="10.5" font-weight="700" letter-spacing="0.06em">MULTI-ECHELON BUFFER (MEIO) · ATP &lt;50MS</text>
        </svg>`;
      }
      if (watermarkType === 'demand_wave') {
        return `<svg viewBox="0 0 320 118" class="${cssClass}" aria-hidden="true">
          <!-- Probabilistic P10/P50/P90 Fan + Live TimesFM Demand Wave -->
          <polygon points="14,82 78,46 144,64 218,28 304,16 304,64 218,74 144,98 78,86 14,104"
                   fill="${color}" fill-opacity="0.22" />
          <path d="M 14 94 Q 78 58, 144 78 T 304 34"
                fill="none" stroke="${color}" stroke-width="3.2" class="sc-arc-flow" />
          <path d="M 14 104 Q 78 76, 144 92 T 304 56"
                fill="none" stroke="#ffffff" stroke-opacity="0.45" stroke-width="1.6" stroke-dasharray="5 5" />
          <circle cx="78" cy="70" r="5" fill="${color}" class="sc-node-pulse" />
          <circle cx="176" cy="58" r="5.5" fill="#00d2ff" class="sc-node-pulse" />
          <circle cx="282" cy="39" r="6" fill="#ffffff" class="sc-node-pulse" />
          <circle r="4.5" fill="#ffffff">
            <animateMotion dur="2.6s" repeatCount="indefinite" path="M 14 94 Q 78 58, 144 78 T 304 34" />
          </circle>
          <text x="16" y="24" fill="${color}" font-size="10.5" font-weight="700" letter-spacing="0.06em">TIMESFM P10 / P50 / P90 WAVE</text>
        </svg>`;
      }
      if (watermarkType === 'plant_oee') {
        return `<svg viewBox="0 0 320 118" class="${cssClass}" aria-hidden="true">
          <!-- Smart Factory Production Line + CNC Cells + Live OEE Telemetry Ring -->
          <rect x="16" y="72" width="204" height="24" rx="6" fill="${color}" fill-opacity="0.20" stroke="${color}" stroke-width="2" />
          <line x1="26" y1="84" x2="210" y2="84" stroke="#00d2ff" stroke-width="2.6" class="sc-arc-flow" />
          <rect x="30" y="34" width="44" height="38" rx="6" fill="#081122" stroke="${color}" stroke-width="2.2" />
          <text x="39" y="57" fill="#e2e8f0" font-size="9.5" font-weight="700">CNC-1</text>
          <rect x="96" y="30" width="48" height="42" rx="6" fill="#081122" stroke="#00d2ff" stroke-width="2.2" />
          <text x="106" y="55" fill="#38bdf8" font-size="9.5" font-weight="700">MES-2</text>
          <rect x="164" y="34" width="44" height="38" rx="6" fill="#081122" stroke="#10b981" stroke-width="2.2" />
          <text x="174" y="57" fill="#34d399" font-size="9.5" font-weight="700">QC-AI</text>
          <circle cx="268" cy="56" r="30" fill="rgba(8,17,34,0.9)" stroke="${color}" stroke-width="3.2" stroke-dasharray="145 35" />
          <circle cx="268" cy="56" r="6" fill="#10b981" class="sc-node-pulse" />
          <text x="249" y="38" fill="#34d399" font-size="9.5" font-weight="700">94% OEE</text>
        </svg>`;
      }
      if (watermarkType === 'circular_loop') {
        return `<svg viewBox="0 0 320 118" class="${cssClass}" aria-hidden="true">
          <!-- Circular Reverse RMA Loop + Scope 3 Primary Carbon Telemetry -->
          <path d="M 52 60 C 52 18, 268 18, 268 60 C 268 102, 52 102, 52 60 Z"
                fill="${color}" fill-opacity="0.10" stroke="${color}" stroke-width="2.8" class="sc-arc-flow" />
          <circle cx="52" cy="60" r="9" fill="#081122" stroke="${color}" stroke-width="2.4" class="sc-node-pulse" />
          <circle cx="268" cy="60" r="9" fill="#081122" stroke="#00d2ff" stroke-width="2.4" class="sc-node-pulse" />
          <rect x="128" y="48" width="16" height="30" rx="3" fill="${color}" fill-opacity="0.85" />
          <rect x="150" y="34" width="16" height="44" rx="3" fill="#00d2ff" fill-opacity="0.90" />
          <rect x="172" y="54" width="16" height="24" rx="3" fill="#10b981" fill-opacity="0.95" />
          <text x="16" y="22" fill="${color}" font-size="10.5" font-weight="700" letter-spacing="0.06em">CIRCULAR RMA &amp; SCOPE 3 TWIN</text>
        </svg>`;
      }
      if (watermarkType === 'conveyor_rack') {
        return `<svg viewBox="0 0 320 118" class="${cssClass}" aria-hidden="true">
          <!-- Isometric 3D WMS Conveyor + Moving Cartons + Golden-Zone AS/RS Rack -->
          <polygon points="16,74 114,32 224,78 126,112" fill="${color}" fill-opacity="0.18" stroke="${color}" stroke-width="2" />
          <line x1="42" y1="62" x2="196" y2="92" stroke="#ffffff" stroke-opacity="0.65" stroke-width="2" class="sc-arc-flow" />
          <g class="sc-conveyor-box-anim">
            <polygon points="54,48 74,38 94,48 74,58" fill="${color}" />
            <polygon points="54,48 74,58 74,74 54,64" fill="#0284c7" />
            <polygon points="94,48 74,58 74,74 94,64" fill="#0369a1" />
          </g>
          <g class="sc-conveyor-box-anim-delayed">
            <polygon points="54,48 74,38 94,48 74,58" fill="#10b981" />
            <polygon points="54,48 74,58 74,74 54,64" fill="#059669" />
            <polygon points="94,48 74,58 74,74 94,64" fill="#047857" />
          </g>
          <!-- AS/RS Rack Grid -->
          <rect x="234" y="20" width="32" height="24" rx="4" fill="#081122" stroke="${color}" stroke-width="1.8" />
          <rect x="272" y="20" width="32" height="24" rx="4" fill="${color}" fill-opacity="0.45" stroke="${color}" stroke-width="1.8" />
          <rect x="234" y="50" width="32" height="24" rx="4" fill="${color}" fill-opacity="0.45" stroke="${color}" stroke-width="1.8" />
          <rect x="272" y="50" width="32" height="24" rx="4" fill="#081122" stroke="#10b981" stroke-width="1.8" />
          <text x="16" y="22" fill="${color}" font-size="10.5" font-weight="700" letter-spacing="0.06em">3D WMS SLOTTING &amp; MEIO</text>
        </svg>`;
      }
      if (watermarkType === 'corridor_lifo') {
        return `<svg viewBox="0 0 320 118" class="${cssClass}" aria-hidden="true">
          <!-- Multi-Modal Ocean / Air / Rail Corridors + 3D LIFO Truck Bay -->
          <path d="M 18 96 C 68 38, 144 20, 298 16" fill="none" stroke="#c084fc" stroke-width="2.4" class="sc-arc-flow" />
          <path d="M 18 96 C 78 62, 152 44, 298 38" fill="none" stroke="#00d2ff" stroke-width="2.6" class="sc-arc-flow" />
          <path d="M 18 96 C 90 84, 168 72, 298 58" fill="none" stroke="#10b981" stroke-width="2.2" class="sc-arc-flow" />
          <circle cx="18" cy="96" r="6.5" fill="${color}" class="sc-node-pulse" />
          <circle cx="298" cy="16" r="5" fill="#c084fc" />
          <circle cx="298" cy="38" r="5" fill="#00d2ff" />
          <circle cx="298" cy="58" r="5" fill="#10b981" />
          <!-- 3D LIFO & Container Bay Silhouette -->
          <rect x="136" y="64" width="132" height="34" rx="6" fill="#081122" stroke="${color}" stroke-width="2.2" />
          <rect x="143" y="69" width="26" height="24" rx="3" fill="#3b82f6" />
          <rect x="173" y="69" width="26" height="24" rx="3" fill="#a855f7" />
          <rect x="203" y="69" width="26" height="24" rx="3" fill="#10b981" />
          <rect x="233" y="69" width="26" height="24" rx="3" fill="${color}" />
          <circle cx="164" cy="103" r="5.5" fill="#081122" stroke="${color}" stroke-width="2" />
          <circle cx="242" cy="103" r="5.5" fill="#081122" stroke="${color}" stroke-width="2" />
          <text x="16" y="22" fill="${color}" font-size="10.5" font-weight="700" letter-spacing="0.06em">SHIP · AIR · RAIL · 3D LIFO</text>
        </svg>`;
      }
      // Default: supplier_graph (Tier-3 -> Tier-2 -> Tier-1 -> Plant Spanner Graph)
      return `<svg viewBox="0 0 320 118" class="${cssClass}" aria-hidden="true">
        <line x1="38" y1="34" x2="136" y2="62" stroke="${color}" stroke-width="2.6" class="sc-arc-flow" />
        <line x1="38" y1="92" x2="136" y2="62" stroke="#10b981" stroke-width="2.6" class="sc-arc-flow" />
        <line x1="136" y1="62" x2="254" y2="62" stroke="#00d2ff" stroke-width="3" class="sc-arc-flow" />
        <circle cx="38" cy="34" r="11" fill="#081122" stroke="${color}" stroke-width="2.4" class="sc-node-pulse" />
        <text x="31" y="38" fill="#f8fafc" font-size="8.5" font-weight="700">T3</text>
        <circle cx="38" cy="92" r="11" fill="#081122" stroke="#10b981" stroke-width="2.4" class="sc-node-pulse" />
        <text x="31" y="96" fill="#f8fafc" font-size="8.5" font-weight="700">T2</text>
        <circle cx="136" cy="62" r="15" fill="#081122" stroke="${color}" stroke-width="2.6" />
        <text x="128" y="66" fill="#f8fafc" font-size="9.5" font-weight="700">T1</text>
        <rect x="246" y="42" width="44" height="40" rx="8" fill="#081122" stroke="#00d2ff" stroke-width="2.6" />
        <text x="255" y="66" fill="#38bdf8" font-size="9.5" font-weight="700">ERP</text>
        <text x="92" y="22" fill="${color}" font-size="10.5" font-weight="700" letter-spacing="0.06em">SPANNER TIER-N BOM GRAPH</text>
      </svg>`;
    }

    /* =========================================================================
       3-PART PURPOSE-BUILT ANIMATION TAXONOMY:
       1. Expanding items (Vertical card, Persona card, Agent card) -> Genie Effect
       2. Dropdowns -> Smooth Dropdown Unroll (dropdownUnroll)
       3. Switching pages / tabs / Back buttons -> Directional Horizontal Slide
       ========================================================================= */
    let genieAnimId = null;

    function getClickedCardRect(ev) {
      if (!ev) return null;
      const el = (ev.currentTarget && ev.currentTarget.getBoundingClientRect)
        ? ev.currentTarget
        : (ev.target && ev.target.closest ? ev.target.closest('.dept-node, .persona-link-card, .catalog-card, .vc-entry-card, .universal-agent-card, .plugin-agent-btn, .dir-agent-launch-row') : ev.target);
      if (!el || !el.getBoundingClientRect) return null;
      const r = el.getBoundingClientRect();
      return { left: r.left, right: r.right, top: r.top, bottom: r.bottom, width: r.width, height: r.height };
    }

    function getPageTransitionClass(ev, sRect) {
      if (sRect) return 'genie-enter';
      if (ev && ev.currentTarget && ev.currentTarget.classList && ev.currentTarget.classList.contains('back-btn')) {
        return 'page-slide-left';
      }
      return 'page-slide-right';
    }

    function animateGenieOutOfBox(sRect, targetEl, accentColor = '#00d2ff') {
      if (!sRect || !targetEl || !targetEl.getBoundingClientRect) return;
      const tRect = targetEl.getBoundingClientRect();
      if (!tRect.width || !tRect.height) return;

      const stop1 = document.getElementById('genieStop1');
      const path = document.getElementById('genieFunnelPath');
      const svg = document.getElementById('genieSvgOverlay');
      if (stop1) stop1.setAttribute('stop-color', accentColor);
      if (path) path.setAttribute('stroke', accentColor);

      const srcCenterX = sRect.left + sRect.width * 0.5;
      const srcAnchorY = sRect.bottom;
      const tgtCenterX = tRect.left + tRect.width * 0.5;
      const tgtAnchorY = tRect.top;

      const dx = srcCenterX - tgtCenterX;
      const dy = srcAnchorY - tgtAnchorY;
      const scaleX0 = Math.max(0.16, Math.min(0.68, sRect.width / tRect.width));
      const scaleY0 = Math.max(0.06, Math.min(0.38, sRect.height / tRect.height));

      const relX = Math.max(8, Math.min(92, ((srcCenterX - tRect.left) / tRect.width) * 100));
      const halfSpan = Math.max(8, (sRect.width / tRect.width) * 50);
      const pLeft = Math.max(0, relX - halfSpan).toFixed(1);
      const pRight = Math.min(100, relX + halfSpan).toFixed(1);

      targetEl.style.transformOrigin = '50% 0%';
      if (targetEl.animate) {
        targetEl.animate([
          {
            opacity: 0.16,
            transform: `translate3d(${dx.toFixed(1)}px, ${dy.toFixed(1)}px, 0) scale(${scaleX0.toFixed(3)}, ${scaleY0.toFixed(3)}) perspective(1100px) rotateX(18deg)`,
            clipPath: `polygon(${pLeft}% 0%, ${pRight}% 0%, 100% 100%, 0% 100%)`,
            filter: 'blur(5px)'
          },
          {
            offset: 0.54,
            opacity: 0.96,
            transform: `translate3d(${(dx * 0.14).toFixed(1)}px, ${(dy * 0.10).toFixed(1)}px, 0) scale(0.95, 0.86) perspective(1100px) rotateX(5deg)`,
            clipPath: `polygon(${(relX * 0.10).toFixed(1)}% 0%, ${(100 - (100 - relX) * 0.10).toFixed(1)}% 0%, 100% 100%, 0% 100%)`,
            filter: 'blur(0.8px)'
          },
          {
            opacity: 1,
            transform: 'translate3d(0px, 0px, 0) scale(1, 1) perspective(1100px) rotateX(0deg)',
            clipPath: 'polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)',
            filter: 'blur(0px)'
          }
        ], {
          duration: 540,
          easing: 'cubic-bezier(0.22, 1, 0.36, 1)',
          fill: 'forwards'
        });
      }

      if (!svg || !path) return;
      svg.classList.add('active');
      const start = performance.now();
      const duration = 500;

      function frame(now) {
        const raw = Math.min(1, (now - start) / duration);
        const p = 1 - Math.pow(1 - raw, 3);
        const lead = Math.min(1, p * 1.26);
        const trail = Math.max(0, (p - 0.20) / 0.80);

        const topL = sRect.left + (tRect.left - sRect.left) * trail;
        const topR = sRect.right + (tRect.right - sRect.right) * trail;
        const topY = sRect.bottom + (tRect.top - sRect.bottom) * trail;

        const botL = sRect.left + (tRect.left - sRect.left) * lead;
        const botR = sRect.right + (tRect.right - sRect.right) * lead;
        const botY = sRect.bottom + (Math.min(window.innerHeight * 0.92, tRect.bottom) - sRect.bottom) * lead;

        const midY = topY + (botY - topY) * 0.45;
        const pinch = (1 - raw) * 26;

        const d = [
          `M ${topL.toFixed(1)} ${topY.toFixed(1)}`,
          `L ${topR.toFixed(1)} ${topY.toFixed(1)}`,
          `C ${(topR - pinch).toFixed(1)} ${midY.toFixed(1)}, ${(botR - pinch * 0.4).toFixed(1)} ${midY.toFixed(1)}, ${botR.toFixed(1)} ${botY.toFixed(1)}`,
          `L ${botL.toFixed(1)} ${botY.toFixed(1)}`,
          `C ${(botL + pinch * 0.4).toFixed(1)} ${midY.toFixed(1)}, ${(topL + pinch).toFixed(1)} ${midY.toFixed(1)}, ${topL.toFixed(1)} ${topY.toFixed(1)}`,
          'Z'
        ].join(' ');
        path.setAttribute('d', d);
        path.setAttribute('opacity', (1 - raw * 0.85).toFixed(2));

        if (raw < 1) {
          genieAnimId = requestAnimationFrame(frame);
        } else {
          svg.classList.remove('active');
          path.setAttribute('d', '');
          path.removeAttribute('opacity');
        }
      }
      if (genieAnimId) cancelAnimationFrame(genieAnimId);
      genieAnimId = requestAnimationFrame(frame);
    }

    /* =========================================================================
       INTERACTIVE SUPPLY CHAIN CAD DRAWINGS (FOR AGENT & VALUE CHAIN STAGE)
       ========================================================================= */
    let lifoStep = 16;
    let lifoStopFilter = 0;
    let corridorOpt = true;
    let multimodalMode = 'all';
    let demandSurge = 22;
    let warehouseGolden = true;
    let tier2Disrupted = false;
    let plantFiniteOpt = true;
    let controlTowerUnified = true;
    let tmdStockSync = true;

    function renderMiniCatalogCadSvg(cadType, color) {
      if (cadType === 'truck_lifo') {
        return `<svg viewBox="0 0 280 130" style="width:88%;height:88%;position:relative;z-index:2;">
          <rect x="24" y="28" width="185" height="62" rx="8" fill="rgba(251,188,4,0.08)" stroke="${color}" stroke-width="2" />
          <rect x="32" y="36" width="40" height="46" rx="4" fill="#4285f4" fill-opacity="0.8" />
          <rect x="76" y="36" width="40" height="46" rx="4" fill="#a142f4" fill-opacity="0.8" />
          <rect x="120" y="36" width="40" height="46" rx="4" fill="#34a853" fill-opacity="0.8" />
          <rect x="164" y="36" width="38" height="46" rx="4" fill="#fbbc04" fill-opacity="0.95" />
          <circle cx="64" cy="98" r="9" fill="#0b0f18" stroke="${color}" stroke-width="2.2" />
          <circle cx="176" cy="98" r="9" fill="#0b0f18" stroke="${color}" stroke-width="2.2" />
          <text x="116" y="20" text-anchor="middle" fill="#f8f9fa" font-size="10" font-weight="700">3D LIFO BAY · STOP 4 → STOP 1</text>
        </svg>`;
      }
      if (cadType === 'corridor_map') {
        return `<svg viewBox="0 0 280 130" style="width:88%;height:88%;position:relative;z-index:2;">
          <rect x="14" y="50" width="34" height="34" rx="6" fill="#0b0f18" stroke="#4285f4" stroke-width="2" />
          <text x="31" y="71" text-anchor="middle" fill="#f8fafc" font-size="9" font-weight="700">PLANT</text>
          <path d="M 48 60 C 92 22, 148 22, 192 56" fill="none" stroke="#a142f4" stroke-width="2.3" class="sc-arc-flow" />
          <path d="M 48 67 C 96 52, 144 52, 192 64" fill="none" stroke="#00d2ff" stroke-width="2.4" class="sc-arc-flow" />
          <path d="M 48 74 C 96 102, 144 102, 192 72" fill="none" stroke="#10b981" stroke-width="2.3" class="sc-arc-flow" />
          <circle cx="198" cy="65" r="12" fill="#0b0f18" stroke="${color}" stroke-width="2.2" />
          <path d="M 210 65 L 262 36" fill="none" stroke="#fbbc04" stroke-width="2.3" class="sc-arc-flow" />
          <path d="M 210 65 L 262 94" fill="none" stroke="#fbbc04" stroke-width="2.3" class="sc-arc-flow" />
          <text x="140" y="18" text-anchor="middle" fill="#f8f9fa" font-size="9.5" font-weight="700">FACTORY → SHIP / AIR / RAIL → DC → TRUCK</text>
        </svg>`;
      }
      if (cadType === 'warehouse_crane') {
        return `<svg viewBox="0 0 280 130" style="width:88%;height:88%;position:relative;z-index:2;">
          ${[0,1,2,3,4].map(i => `
            <rect x="${34 + i*44}" y="28" width="34" height="28" rx="4" fill="${i<2 ? color : '#1e293b'}" fill-opacity="0.65" stroke="${color}" stroke-width="1.3" />
            <rect x="${34 + i*44}" y="70" width="34" height="28" rx="4" fill="${i<3 ? color : '#1e293b'}" fill-opacity="0.45" stroke="${color}" stroke-width="1.3" />
          `).join('')}
          <path d="M 20 63 L 260 63" stroke="#34a853" stroke-width="2.5" class="sc-arc-flow" />
        </svg>`;
      }
      if (cadType === 'supplier_radar') {
        return `<svg viewBox="0 0 280 130" style="width:88%;height:88%;position:relative;z-index:2;">
          <line x1="56" y1="36" x2="140" y2="65" stroke="${color}" stroke-width="2" class="sc-arc-flow" />
          <line x1="56" y1="94" x2="140" y2="65" stroke="#34a853" stroke-width="2" class="sc-arc-flow" />
          <line x1="140" y1="65" x2="224" y2="65" stroke="#4285f4" stroke-width="2.5" class="sc-arc-flow" />
          <circle cx="56" cy="36" r="11" fill="#0b0f18" stroke="${color}" stroke-width="2" />
          <circle cx="56" cy="94" r="11" fill="#0b0f18" stroke="#34a853" stroke-width="2" />
          <circle cx="140" cy="65" r="14" fill="#0b0f18" stroke="${color}" stroke-width="2.2" />
          <rect x="210" y="51" width="28" height="28" rx="6" fill="#0b0f18" stroke="#4285f4" stroke-width="2" />
        </svg>`;
      }
      if (cadType === 'tmd_retail_network') {
        return `
          <div id="${mountId}" style="width:100%;">
            <div class="cad-bar">
              <span style="color:#f59e0b;font-weight:700;">Interactive TM&amp;D Retail Planogram, FSO Beat &amp; Live DMS Inventory Twin</span>
              <div style="display:flex;gap:8px;flex-wrap:wrap;">
                <button type="button" class="cad-pill-btn ${!tmdStockSync?'active':''}" onclick="tmdStockSync=false;refreshCadMount('${cadType}','${mountId}')">
                  ✕ Blind Store Pitch (28% Out-of-Stock Cancellations)
                </button>
                <button type="button" class="cad-pill-btn ${tmdStockSync?'active':''}" onclick="tmdStockSync=true;refreshCadMount('${cadType}','${mountId}')">
                  ✦ BeatSync Real-Time DMS + ShelfVision (98.4% Fill · Zero OOS)
                </button>
              </div>
            </div>
            <svg viewBox="0 0 780 350" style="width:100%;height:auto;display:block;background:#04070f;">
              <!-- Left side: Retail Counter & Shelf Planogram -->
              <rect x="36" y="32" width="220" height="286" rx="12" fill="rgba(15,23,42,0.85)" stroke="#f59e0b" stroke-width="1.8" />
              <text x="52" y="60" fill="#f59e0b" font-size="12" font-weight="700">RETAIL SHELF PLANOGRAM</text>
              <text x="52" y="78" fill="#94a3b8" font-size="10.5">GEMINI 3.8 FLASH VISION SCAN</text>

              <!-- Shelf Tier 1 -->
              <line x1="48" y1="130" x2="244" y2="130" stroke="#334155" stroke-width="2" />
              <rect x="52" y="92" width="36" height="36" rx="4" fill="${tmdStockSync ? '#10b981' : '#ea4335'}" />
              <text x="70" y="114" fill="#fff" font-size="9" font-weight="800" text-anchor="middle">SKU-A</text>
              <rect x="96" y="92" width="36" height="36" rx="4" fill="${tmdStockSync ? '#10b981' : '#ea4335'}" />
              <text x="114" y="114" fill="#fff" font-size="9" font-weight="800" text-anchor="middle">SKU-A</text>
              <rect x="140" y="94" width="32" height="34" rx="4" fill="#64748b" />
              <rect x="178" y="94" width="32" height="34" rx="4" fill="#64748b" />

              <!-- Shelf Tier 2 (Eye Level) -->
              <line x1="48" y1="190" x2="244" y2="190" stroke="#334155" stroke-width="2" />
              <rect x="52" y="146" width="42" height="42" rx="4" fill="#f59e0b" />
              <text x="73" y="171" fill="#04070f" font-size="9" font-weight="800" text-anchor="middle">FOCUS</text>
              <rect x="100" y="146" width="42" height="42" rx="4" fill="#f59e0b" />
              <text x="121" y="171" fill="#04070f" font-size="9" font-weight="800" text-anchor="middle">FOCUS</text>
              <rect x="148" y="146" width="42" height="42" rx="4" fill="#3b82f6" />
              <text x="169" y="171" fill="#fff" font-size="9" font-weight="800" text-anchor="middle">PROMO</text>

              <!-- Shelf Tier 3 -->
              <line x1="48" y1="250" x2="244" y2="250" stroke="#334155" stroke-width="2" />
              <rect x="52" y="206" width="46" height="42" rx="4" fill="#10b981" />
              <rect x="104" y="206" width="46" height="42" rx="4" fill="#10b981" />
              <rect x="156" y="206" width="46" height="42" rx="4" fill="#64748b" />

              <!-- Scanning laser line -->
              <line x1="48" y1="88" x2="244" y2="88" stroke="#38bdf8" stroke-width="2.5" opacity="0.85">
                <animate attributeName="y1" values="88;250;88" dur="3s" repeatCount="indefinite" />
                <animate attributeName="y2" values="88;250;88" dur="3s" repeatCount="indefinite" />
              </line>

              <!-- Middle: Google Maps Beat Route & Van Flow -->
              <path d="M 256 175 C 310 175, 330 110, 390 110 S 470 240, 524 240" fill="none" stroke="${tmdStockSync ? '#10b981' : '#f59e0b'}" stroke-width="2.6" stroke-dasharray="6 4" class="sc-arc-flow" />
              <circle r="6" fill="${tmdStockSync ? '#10b981' : '#f59e0b'}">
                <animateMotion dur="2.8s" repeatCount="indefinite" path="M 256 175 C 310 175, 330 110, 390 110 S 470 240, 524 240" />
              </circle>
              
              <!-- Distributor Hub Node -->
              <rect x="360" y="70" width="134" height="64" rx="8" fill="rgba(8,13,24,0.95)" stroke="#38bdf8" stroke-width="1.8" />
              <text x="374" y="94" fill="#38bdf8" font-size="11" font-weight="700">DISTRIBUTOR DMS</text>
              <text x="374" y="114" fill="${tmdStockSync ? '#34d399' : '#f87171'}" font-size="10" font-weight="700">
                ${tmdStockSync ? '✓ LIVE STOCK SYNC' : '✕ BATCH NIGHTLY SYNC'}
              </text>

              <!-- Secondary Retail Node -->
              <rect x="360" y="210" width="134" height="64" rx="8" fill="rgba(8,13,24,0.95)" stroke="#f59e0b" stroke-width="1.8" />
              <text x="374" y="234" fill="#f59e0b" font-size="11" font-weight="700">FSO BEAT VISIT</text>
              <text x="374" y="254" fill="${tmdStockSync ? '#34d399' : '#f87171'}" font-size="10" font-weight="700">
                ${tmdStockSync ? '✓ ZERO OOS PITCHES' : '⚠ 28% OOS CANCELLATION'}
              </text>

              <!-- Right HUD -->
              <rect x="540" y="28" width="214" height="294" rx="14" fill="rgba(11,15,24,0.94)" stroke="rgba(255,255,255,0.15)" />
              <text x="558" y="56" fill="#f59e0b" font-size="12" font-weight="700">TM&amp;D FIELD EXECUTION HUD</text>
              <text x="558" y="96" fill="#9aa0a6" font-size="11">DISTRIBUTOR CASE FILL</text>
              <text x="558" y="122" fill="${tmdStockSync?'#81c995':'#ff8a80'}" font-size="22" font-weight="700">${tmdStockSync ? '98.4% (+18.4%)' : '71.2% Fill Rate'}</text>
              <text x="558" y="168" fill="#9aa0a6" font-size="11">OUT-OF-STOCK PITCHES</text>
              <text x="558" y="194" fill="${tmdStockSync?'#81c995':'#ff8a80'}" font-size="22" font-weight="700">${tmdStockSync ? '0% Lost Visits' : '28.4% Lines Lost'}</text>
              <text x="558" y="240" fill="#9aa0a6" font-size="11">PLANOGRAM COMPLIANCE</text>
              <text x="558" y="266" fill="#8ab4f8" font-size="20" font-weight="700">${tmdStockSync ? '98.7% Vision Audit' : '61% Sample Audit'}</text>
            </svg>
          </div>
        `;
      }
      if (cadType === 'plant_oee_twin') {
        return `<svg viewBox="0 0 280 130" style="width:88%;height:88%;position:relative;z-index:2;">
          <rect x="24" y="42" width="46" height="46" rx="6" fill="#0b0f18" stroke="${color}" stroke-width="2" />
          <rect x="92" y="42" width="46" height="46" rx="6" fill="#0b0f18" stroke="#00d2ff" stroke-width="2" />
          <rect x="160" y="42" width="46" height="46" rx="6" fill="#0b0f18" stroke="#10b981" stroke-width="2" />
          <line x1="70" y1="65" x2="92" y2="65" stroke="${color}" stroke-width="2.5" class="sc-arc-flow" />
          <line x1="138" y1="65" x2="160" y2="65" stroke="#00d2ff" stroke-width="2.5" class="sc-arc-flow" />
          <circle cx="242" cy="65" r="22" fill="none" stroke="#10b981" stroke-width="3" stroke-dasharray="105 35" />
          <text x="140" y="22" text-anchor="middle" fill="#f8f9fa" font-size="10" font-weight="700">SMART FACTORY OEE · CP-SAT FINITE SCHEDULE</text>
        </svg>`;
      }
      if (cadType === 'control_tower_twin') {
        return `<svg viewBox="0 0 280 130" style="width:88%;height:88%;position:relative;z-index:2;">
          <circle cx="140" cy="65" r="24" fill="rgba(56,189,248,0.16)" stroke="#38bdf8" stroke-width="2.2" />
          <circle cx="52" cy="34" r="10" fill="#0b0f18" stroke="#00d2ff" stroke-width="2" />
          <circle cx="52" cy="96" r="10" fill="#0b0f18" stroke="#a855f7" stroke-width="2" />
          <circle cx="228" cy="34" r="10" fill="#0b0f18" stroke="#ec4899" stroke-width="2" />
          <circle cx="228" cy="96" r="10" fill="#0b0f18" stroke="#10b981" stroke-width="2" />
          <line x1="62" y1="38" x2="118" y2="56" stroke="#00d2ff" stroke-width="2" class="sc-arc-flow" />
          <line x1="62" y1="92" x2="118" y2="74" stroke="#a855f7" stroke-width="2" class="sc-arc-flow" />
          <line x1="162" y1="56" x2="218" y2="38" stroke="#ec4899" stroke-width="2" class="sc-arc-flow" />
          <line x1="162" y1="74" x2="218" y2="92" stroke="#10b981" stroke-width="2" class="sc-arc-flow" />
          <text x="140" y="69" text-anchor="middle" fill="#f8fafc" font-size="9.5" font-weight="700">CSCO TWIN</text>
        </svg>`;
      }
      return `<svg viewBox="0 0 280 130" style="width:88%;height:88%;position:relative;z-index:2;">
        <path d="M 18 92 Q 75 26, 135 68 T 262 32" fill="none" stroke="${color}" stroke-width="3" class="sc-arc-flow" />
        <path d="M 18 104 Q 75 48, 135 84 T 262 54" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="1.6" stroke-dasharray="4 4" />
      </svg>`;
    }

    function renderInteractiveCadStage(cadType, mountId) {
      if (cadType === 'plant_oee_twin') {
        return `
          <div id="${mountId}" style="width:100%;">
            <div class="cad-bar">
              <span style="color:#f472b6;font-weight:700;">Interactive Smart Factory Finite Scheduling, OEE &amp; Edge PdM Twin</span>
              <div style="display:flex;gap:8px;flex-wrap:wrap;">
                <button type="button" class="cad-pill-btn ${!plantFiniteOpt?'active':''}" onclick="plantFiniteOpt=false;refreshCadMount('${cadType}','${mountId}')">
                  ✕ Unsequenced Changeovers &amp; Line Stoppage (76.2% OEE)
                </button>
                <button type="button" class="cad-pill-btn ${plantFiniteOpt?'active':''}" onclick="plantFiniteOpt=true;refreshCadMount('${cadType}','${mountId}')">
                  ✦ CP-SAT Sequence + Edge PdM Interlock (87.6% OEE · -41% Downtime)
                </button>
              </div>
            </div>
            <svg viewBox="0 0 780 350" style="width:100%;height:auto;display:block;background:#04070f;">
              <!-- 3 Parallel Production Lines -->
              ${[0, 1, 2].map(lineIdx => {
                const y = 52 + lineIdx * 88;
                const lineStatusColor = (!plantFiniteOpt && lineIdx === 1) ? '#ea4335' : '#10b981';
                return `<g>
                  <rect x="44" y="${y}" width="458" height="62" rx="10" fill="rgba(15,23,42,0.88)" stroke="${lineStatusColor}" stroke-width="1.8" />
                  <text x="62" y="${y + 24}" fill="#f8fafc" font-size="11.5" font-weight="700">LINE 0${lineIdx + 1} · ${lineIdx===0 ? 'HIGH-SPEED PACKAGING' : (lineIdx===1 ? 'CNC SPINDLE & ASSEMBLY' : 'AUTOMATED VISION QC')}</text>
                  <line x1="62" y1="${y + 42}" x2="480" y2="${y + 42}" stroke="${lineStatusColor}" stroke-width="3" class="sc-arc-flow" />
                  <circle r="4.5" fill="${lineStatusColor}">
                    <animate attributeName="cx" from="62" to="480" dur="${(!plantFiniteOpt && lineIdx === 1) ? '99s' : (1.8 + lineIdx * 0.3) + 's'}" repeatCount="indefinite" />
                    <animate attributeName="cy" values="${y + 42};${y + 42}" dur="1s" repeatCount="indefinite" />
                  </circle>
                  <rect x="364" y="${y + 10}" width="122" height="22" rx="6" fill="rgba(4,9,18,0.92)" stroke="${lineStatusColor}" stroke-width="1.2" />
                  <text x="425" y="${y + 25}" text-anchor="middle" fill="${lineStatusColor}" font-size="10" font-weight="700">
                    ${(!plantFiniteOpt && lineIdx === 1) ? '⚠ BEARING FAULT' : '✓ NOMINAL OEE'}
                  </text>
                </g>`;
              }).join('')}

              <rect x="540" y="28" width="214" height="294" rx="14" fill="rgba(11,15,24,0.94)" stroke="rgba(255,255,255,0.15)" />
              <text x="558" y="56" fill="#f472b6" font-size="12" font-weight="700">PLANT UPTIME &amp; MES HUD</text>
              <text x="558" y="96" fill="#9aa0a6" font-size="11">UNPLANNED STOPS / UPTIME</text>
              <text x="558" y="122" fill="${plantFiniteOpt?'#81c995':'#ff8a80'}" font-size="20" font-weight="700">${plantFiniteOpt ? '-48% Stops (87.6% OEE)' : '76.2% (Unplanned Halt)'}</text>
              <text x="558" y="168" fill="#9aa0a6" font-size="11">CHANGEOVER LOSS</text>
              <text x="558" y="194" fill="#f8f9fa" font-size="22" font-weight="700">${plantFiniteOpt ? '42 mins (-34%)' : '64 mins / shift'}</text>
              <text x="558" y="240" fill="#9aa0a6" font-size="11">EDGE VISION DEFECT ESCAPE</text>
              <text x="558" y="266" fill="#8ab4f8" font-size="20" font-weight="700">${plantFiniteOpt ? '0.02% (-52% Scrap)' : '0.84% Manual Audit'}</text>
            </svg>
          </div>
        `;
      }

      if (cadType === 'control_tower_twin') {
        return `
          <div id="${mountId}" style="width:100%;">
            <div class="cad-bar">
              <span style="color:#38bdf8;font-weight:700;">Interactive CSCO Cross-Vertical Control Tower &amp; Working Capital Twin</span>
              <div style="display:flex;gap:8px;flex-wrap:wrap;">
                <button type="button" class="cad-pill-btn ${!controlTowerUnified?'active':''}" onclick="controlTowerUnified=false;refreshCadMount('${cadType}','${mountId}')">
                  ✕ Siloed Functional Decisions (72-Hr War Room Lag)
                </button>
                <button type="button" class="cad-pill-btn ${controlTowerUnified?'active':''}" onclick="controlTowerUnified=true;refreshCadMount('${cadType}','${mountId}')">
                  ✦ Unified CSCO Pareto Frontier (4-Min Resolution · -$140M Cash Freed)
                </button>
              </div>
            </div>
            <svg viewBox="0 0 780 350" style="width:100%;height:auto;display:block;background:#04070f;">
              <circle cx="270" cy="175" r="122" fill="none" stroke="rgba(56,189,248,0.18)" stroke-dasharray="5 5" />
              <circle cx="270" cy="175" r="46" fill="rgba(56,189,248,0.15)" stroke="#38bdf8" stroke-width="2.4" />
              <text x="270" y="172" text-anchor="middle" fill="#f8fafc" font-size="11" font-weight="700">CSCO TWIN</text>
              <text x="270" y="187" text-anchor="middle" fill="#38bdf8" font-size="9.5">6 SCOR NODES</text>

              ${[
                { label: '01 · PLAN', x: 270, y: 44, col: '#10b981' },
                { label: '02 · SOURCE', x: 416, y: 106, col: '#a855f7' },
                { label: '03 · MAKE', x: 416, y: 244, col: '#3b82f6' },
                { label: '05 · DELIVER', x: 270, y: 306, col: '#f59e0b' },
                { label: '04 · FULFILL', x: 124, y: 244, col: '#00d2ff' },
                { label: '06 · ENABLE', x: 124, y: 106, col: '#ec4899' }
              ].map((n, idx) => `
                <g>
                  <line x1="270" y1="175" x2="${n.x}" y2="${n.y}" stroke="${controlTowerUnified ? n.col : '#ea4335'}" stroke-width="2.4" class="sc-arc-flow" />
                  ${controlTowerUnified ? `
                    <circle r="3.5" fill="${n.col}">
                      <animateMotion dur="${1.8 + idx * 0.2}s" repeatCount="indefinite" path="M270,175 L${n.x},${n.y}" />
                    </circle>
                  ` : ''}
                  <rect x="${n.x - 48}" y="${n.y - 15}" width="96" height="30" rx="15" fill="#080d18" stroke="${n.col}" stroke-width="2" />
                  <text x="${n.x}" y="${n.y + 4}" text-anchor="middle" fill="#f8fafc" font-size="9.5" font-weight="700">${n.label}</text>
                </g>
              `).join('')}

              <rect x="540" y="28" width="214" height="294" rx="14" fill="rgba(11,15,24,0.94)" stroke="rgba(255,255,255,0.15)" />
              <text x="558" y="56" fill="#38bdf8" font-size="12" font-weight="700">CSCO EXECUTIVE HUD</text>
              <text x="558" y="96" fill="#9aa0a6" font-size="11">BACKORDER REDUCTION</text>
              <text x="558" y="122" fill="${controlTowerUnified?'#81c995':'#ff8a80'}" font-size="22" font-weight="700">${controlTowerUnified ? '-25.0% Backorders' : 'Baseline Backlogs'}</text>
              <text x="558" y="168" fill="#9aa0a6" font-size="11">WORKING CAPITAL FREED</text>
              <text x="558" y="194" fill="#81c995" font-size="22" font-weight="700">${controlTowerUnified ? '$140M (-8.4 DIO)' : 'Trapped Buffer Cash'}</text>
              <text x="558" y="240" fill="#9aa0a6" font-size="11">DISRUPTION WAR-ROOM SLA</text>
              <text x="558" y="266" fill="#8ab4f8" font-size="20" font-weight="700">${controlTowerUnified ? '72 Hrs → 4 Mins' : '72 Hrs Manual Sync'}</text>
            </svg>
          </div>
        `;
      }

      if (cadType === 'truck_lifo') {
        const boxes = [
          { stop: 4, x: 0, y: 0, z: 0, l: 64, w: 54, h: 42, col: '#4285f4', sku: 'PAL-401' },
          { stop: 4, x: 0, y: 58, z: 0, l: 64, w: 54, h: 42, col: '#4285f4', sku: 'PAL-402' },
          { stop: 4, x: 0, y: 0, z: 44, l: 64, w: 54, h: 36, col: '#4285f4', sku: 'CRT-403' },
          { stop: 4, x: 0, y: 58, z: 44, l: 64, w: 54, h: 36, col: '#4285f4', sku: 'CRT-404' },
          { stop: 3, x: 68, y: 0, z: 0, l: 64, w: 54, h: 42, col: '#a142f4', sku: 'PAL-301' },
          { stop: 3, x: 68, y: 58, z: 0, l: 64, w: 54, h: 42, col: '#a142f4', sku: 'PAL-302' },
          { stop: 3, x: 68, y: 0, z: 44, l: 64, w: 54, h: 36, col: '#a142f4', sku: 'CRT-303' },
          { stop: 3, x: 68, y: 58, z: 44, l: 64, w: 54, h: 36, col: '#a142f4', sku: 'CRT-304' },
          { stop: 2, x: 136, y: 0, z: 0, l: 64, w: 54, h: 42, col: '#34a853', sku: 'PAL-201' },
          { stop: 2, x: 136, y: 58, z: 0, l: 64, w: 54, h: 42, col: '#34a853', sku: 'PAL-202' },
          { stop: 2, x: 136, y: 0, z: 44, l: 64, w: 54, h: 36, col: '#34a853', sku: 'CRT-203' },
          { stop: 2, x: 136, y: 58, z: 44, l: 64, w: 54, h: 36, col: '#34a853', sku: 'CRT-204' },
          { stop: 1, x: 204, y: 0, z: 0, l: 64, w: 54, h: 40, col: '#fbbc04', sku: 'PAL-101' },
          { stop: 1, x: 204, y: 58, z: 0, l: 64, w: 54, h: 40, col: '#fbbc04', sku: 'PAL-102' },
          { stop: 1, x: 204, y: 0, z: 42, l: 64, w: 54, h: 34, col: '#fbbc04', sku: 'CRT-103' },
          { stop: 1, x: 204, y: 58, z: 42, l: 64, w: 54, h: 34, col: '#fbbc04', sku: 'CRT-104' }
        ];
        // Scaled isometric projection so 100% of trailer and labels sit cleanly within x=[48..470], y=[42..346] (never overlapping HUD at x=540)
        const iso = (x, y, z) => [ (172 + (x - y) * 1.02).toFixed(1), (156 + (x + y) * 0.44 - z * 0.96).toFixed(1) ];
        const vis = boxes.slice(0, lifoStep).filter(b => lifoStopFilter === 0 || b.stop === lifoStopFilter);
        const b000 = iso(0,0,0), bL00 = iso(274,0,0), bLL0 = iso(274,116,0), b0L0 = iso(0,116,0);
        const b00H = iso(0,0,92), bL0H = iso(274,0,92), bLLH = iso(274,116,92), b0LH = iso(0,116,92);
        const fillPct = Math.round((lifoStep / 16) * 92);

        return `
          <div id="${mountId}" style="width:100%;">
            <div class="cad-bar">
              <div style="display:flex;align-items:center;gap:12px;">
                <span style="color:#8ab4f8;font-weight:700;">Interactive 3D LIFO Trailer &amp; Container Bay</span>
                <label style="display:inline-flex;align-items:center;gap:8px;color:var(--text-secondary);">
                  <span>Step ${lifoStep}/16</span>
                  <input type="range" min="1" max="16" value="${lifoStep}" oninput="lifoStep=parseInt(this.value,10);refreshCadMount('${cadType}','${mountId}')" />
                </label>
              </div>
              <div style="display:flex;gap:6px;flex-wrap:wrap;">
                ${[0,1,2,3,4].map(s => `
                  <button type="button" class="cad-pill-btn ${lifoStopFilter===s?'active':''}"
                          onclick="lifoStopFilter=${s};refreshCadMount('${cadType}','${mountId}')">
                    ${s===0 ? 'All Stops' : (s===1 ? 'Stop 1 (Rear Door)' : (s===4 ? 'Stop 4 (Cab Nose)' : 'Stop '+s))}
                  </button>
                `).join('')}
              </div>
            </div>
            <svg viewBox="0 0 780 360" style="width:100%;height:auto;display:block;background:#04070f;">
              <polygon points="${b000} ${bL00} ${bLL0} ${b0L0}" fill="rgba(22,34,64,0.85)" stroke="#4285f4" stroke-width="1.5" />
              <polygon points="${b000} ${b0L0} ${b0LH} ${b00H}" fill="rgba(30,48,88,0.45)" stroke="#4285f4" stroke-width="1.2" />
              <text x="54" y="46" fill="#8ab4f8" font-size="11" font-weight="700">◀ CAB NOSE (LOADED 1ST · STOP 4)</text>
              ${vis.map(c => {
                const x1=c.x, x2=c.x+c.l, y1=c.y, y2=c.y+c.w, z1=c.z, z2=c.z+c.h;
                const p001=iso(x1,y1,z2), p101=iso(x2,y1,z2), p111=iso(x2,y2,z2), p011=iso(x1,y2,z2);
                const p100=iso(x2,y1,z1), p110=iso(x2,y2,z1), p010=iso(x1,y2,z1);
                return `<g>
                  <polygon points="${p001} ${p101} ${p111} ${p011}" fill="${c.col}" fill-opacity="0.92" stroke="#04070f" stroke-width="1.2" />
                  <polygon points="${p100} ${p110} ${p111} ${p101}" fill="${c.col}" fill-opacity="0.74" stroke="#04070f" stroke-width="1.2" />
                  <polygon points="${p010} ${p110} ${p111} ${p011}" fill="${c.col}" fill-opacity="0.56" stroke="#04070f" stroke-width="1.2" />
                </g>`;
              }).join('')}
              <line x1="${b00H[0]}" y1="${b00H[1]}" x2="${bL0H[0]}" y2="${bL0H[1]}" stroke="#8ab4f8" stroke-dasharray="5 4" />
              <line x1="${b0LH[0]}" y1="${b0LH[1]}" x2="${bLLH[0]}" y2="${bLLH[1]}" stroke="#8ab4f8" stroke-dasharray="5 4" />
              <text x="235" y="344" fill="#fde293" font-size="11" font-weight="700">REAR DOORS (UNLOADED 1ST · STOP 1) ▶</text>

              <rect x="540" y="28" width="214" height="304" rx="14" fill="rgba(11,15,24,0.94)" stroke="rgba(255,255,255,0.15)" />
              <text x="558" y="56" fill="#8ab4f8" font-size="12" font-weight="700">3D BAY &amp; AXLE PHYSICS</text>
              <text x="558" y="92" fill="#9aa0a6" font-size="11">3D CUBE FILL</text>
              <text x="558" y="118" fill="#f8f9fa" font-size="24" font-weight="700">${fillPct}% Volume</text>
              <text x="558" y="160" fill="#9aa0a6" font-size="11">FRONT / REAR AXLE LOAD</text>
              <text x="558" y="186" fill="#81c995" font-size="20" font-weight="700">100% Compliant</text>
              <text x="558" y="228" fill="#9aa0a6" font-size="11">LIFO UNLOADING ORDER</text>
              <text x="558" y="254" fill="#fde293" font-size="18" font-weight="700">Zero Dock Re-Handling</text>
            </svg>
          </div>
        `;
      }

      if (cadType === 'corridor_map') {
        const showOcean = (multimodalMode === 'all' || multimodalMode === 'ocean');
        const showAir   = (multimodalMode === 'all' || multimodalMode === 'air');
        const showRail  = (multimodalMode === 'all' || multimodalMode === 'rail');
        const showRoad  = (multimodalMode === 'all' || multimodalMode === 'road');

        const hudMetrics = {
          all:   { title: 'MULTI-MODAL TRANSIT HUD', m1L: 'GLOBAL TRANSIT & FLEET COST', m1V: corridorOpt ? '-24.0% Landed Cost' : 'Unoptimized Silos', m2L: '3D CUBE (ULD / FEU / TRUCK)', m2V: corridorOpt ? '92.4% Cube Fill' : '64.0% Avg Fill', m3L: 'END-TO-END OTIF SLA', m3V: corridorOpt ? '99.4% On-Time' : '81.2% On-Time' },
          ocean: { title: 'OCEAN & PORT DRAYAGE HUD', m1L: 'PORT DEMURRAGE & DETENTION', m1V: corridorOpt ? '-67% Demurrage' : '$350/day Port Hold', m2L: '40FT FEU STOWAGE CUBE', m2V: corridorOpt ? '94.1% Container' : '71.0% Container', m3L: 'AIS + WEATHERNEXT 3 ETA', m3V: corridorOpt ? '5-Day Berth Lock' : 'Blind Carrier ETA' },
          air:   { title: 'AIR CARGO & 3D ULD HUD', m1L: 'AIR FREIGHT & CHARTER SPEND', m1V: corridorOpt ? '-28% Air Spend' : 'Spot Panic Rates', m2L: '3D ULD (LD3/PMC) CONTOUR', m2V: corridorOpt ? '91.8% ULD Cube' : '68% Volumetric', m3L: 'ADS-B TARMAC CONNECTION', m3V: corridorOpt ? '99.6% Cold-Chain' : 'Missed Hub Transfers' },
          rail:  { title: 'INTERMODAL RAIL & DC HUD', m1L: 'LONG-HAUL LINEHAUL COST', m1V: corridorOpt ? '-34% vs. OTR' : '100% OTR Diesel', m2L: 'CROSS-DOCK FLOW-THROUGH', m2V: corridorOpt ? '-52% DC Dwell' : 'Double Putaway', m3L: 'SCOPE-3 CORRIDOR CO2e', m3V: corridorOpt ? '-68% Rail CO2e' : 'High OTR Emissions' },
          road:  { title: 'GOOGLE MAPS ROAD FLEET HUD', m1L: 'ACTIVE ROAD FLEET COST', m1V: corridorOpt ? '6 Trucks (-19.4%)' : '9 Trucks (Spaghetti)', m2L: 'MAPS ROUTE DISTANCE', m2V: corridorOpt ? '412 km (-21.8%)' : '527 km Criss-Cross', m3L: '3D LIFO & AXLE PHYSICS', m3V: corridorOpt ? '100% LIFO & Axle' : 'Dock Re-Handling' }
        }[multimodalMode] || { title: 'MULTI-MODAL TRANSIT HUD', m1L: 'GLOBAL TRANSIT COST', m1V: '-24.0% Landed Cost', m2L: '3D CUBE', m2V: '92.4% Fill', m3L: 'OTIF SLA', m3V: '99.4% On-Time' };

        return `
          <div id="${mountId}" style="width:100%;">
            <div class="cad-bar" style="flex-wrap:wrap;gap:10px;">
              <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
                <span style="color:#8ab4f8;font-weight:700;">Factory → Ship / Air / Rail → Cross-Dock → Road Fleet Twin</span>
                ${[
                  { id: 'all',   label: '🌐 Full Chain' },
                  { id: 'ocean', label: '🚢 Ocean & Port' },
                  { id: 'air',   label: '✈️ Air & 3D ULD' },
                  { id: 'rail',  label: '🚆 Rail & Cross-Dock' },
                  { id: 'road',  label: '🚚 Maps Road & LIFO' }
                ].map(m => `
                  <button type="button" class="cad-pill-btn ${multimodalMode===m.id?'active':''}"
                          onclick="multimodalMode='${m.id}';refreshCadMount('${cadType}','${mountId}')">${m.label}</button>
                `).join('')}
              </div>
              <div style="display:flex;gap:6px;flex-wrap:wrap;">
                <button type="button" class="cad-pill-btn ${!corridorOpt?'active':''}" onclick="corridorOpt=false;refreshCadMount('${cadType}','${mountId}')">
                  ✕ Siloed Single-Mode &amp; Spaghetti Routes
                </button>
                <button type="button" class="cad-pill-btn ${corridorOpt?'active':''}" onclick="corridorOpt=true;refreshCadMount('${cadType}','${mountId}')">
                  ✦ Agentic Multi-Modal &amp; Maps Corridor Twin (-24% Cost)
                </button>
              </div>
            </div>
            <svg viewBox="0 0 780 360" style="width:100%;height:auto;display:block;background:#04070f;">
              <!-- Left Origin: Factory Gate -->
              <rect x="20" y="142" width="68" height="72" rx="10" fill="#081020" stroke="#4285f4" stroke-width="2.2" />
              <text x="54" y="172" text-anchor="middle" fill="#f8fafc" font-size="10" font-weight="700">FACTORY</text>
              <text x="54" y="186" text-anchor="middle" fill="#8ab4f8" font-size="8.5" font-weight="700">GATE &amp; ATP</text>
              <text x="54" y="200" text-anchor="middle" fill="#34a853" font-size="8">ModalShift</text>

              <!-- Mid-Transit Nodes: Air Hub (Top), Ocean Port (Mid), Rail Ramp (Bottom) -->
              <g opacity="${showAir ? '1' : '0.22'}">
                <rect x="166" y="34" width="102" height="46" rx="9" fill="#081020" stroke="#a142f4" stroke-width="2" />
                <text x="217" y="54" text-anchor="middle" fill="#f8fafc" font-size="9.5" font-weight="700">✈️ AIR CARGO HUB</text>
                <text x="217" y="68" text-anchor="middle" fill="#d8b4fe" font-size="8">3D ULD · ADS-B</text>
              </g>

              <g opacity="${showOcean ? '1' : '0.22'}">
                <rect x="166" y="155" width="102" height="46" rx="9" fill="#081020" stroke="#00d2ff" stroke-width="2" />
                <text x="217" y="175" text-anchor="middle" fill="#f8fafc" font-size="9.5" font-weight="700">🚢 OCEAN PORT</text>
                <text x="217" y="189" text-anchor="middle" fill="#7dd3fc" font-size="8">AIS · Drayage Gate</text>
              </g>

              <g opacity="${showRail ? '1' : '0.22'}">
                <rect x="166" y="276" width="102" height="46" rx="9" fill="#081020" stroke="#10b981" stroke-width="2" />
                <text x="217" y="296" text-anchor="middle" fill="#f8fafc" font-size="9.5" font-weight="700">🚆 RAIL COFC RAMP</text>
                <text x="217" y="310" text-anchor="middle" fill="#6ee7b7" font-size="8">EDI 404 · Consist</text>
              </g>

              <!-- Cross-Dock Warehouse & Fulfillment Hub -->
              <circle cx="348" cy="178" r="28" fill="#081020" stroke="#fbbc04" stroke-width="2.5" />
              <text x="348" y="174" text-anchor="middle" fill="#f8fafc" font-size="9.5" font-weight="700">CROSS-DOCK</text>
              <text x="348" y="187" text-anchor="middle" fill="#fde293" font-size="8">DC &amp; 3D WMS</text>

              <!-- Multi-Modal Inbound Arcs (Factory -> Air / Ocean / Rail -> Cross-Dock) -->
              ${!corridorOpt ? `
                <g stroke="#ea4335" stroke-width="1.8" stroke-dasharray="5 5" opacity="0.82">
                  <line x1="88" y1="165" x2="166" y2="57" />
                  <line x1="88" y1="178" x2="166" y2="178" />
                  <line x1="88" y1="192" x2="166" y2="299" />
                  <line x1="268" y1="57" x2="324" y2="162" />
                  <line x1="268" y1="178" x2="320" y2="178" />
                  <line x1="268" y1="299" x2="324" y2="194" />
                  <!-- Criss-crossing Road Fleet Spaghetti (Right of Cross-Dock) -->
                  <line x1="376" y1="178" x2="495" y2="54" />
                  <line x1="495" y1="54" x2="415" y2="298" />
                  <line x1="415" y1="298" x2="502" y2="142" />
                  <line x1="376" y1="178" x2="498" y2="312" />
                </g>
              ` : `
                ${showAir ? `
                  <path d="M 88 162 C 118 96, 136 57, 166 57" fill="none" stroke="#a142f4" stroke-width="2.6" class="sc-arc-flow" />
                  <path d="M 268 57 C 298 57, 312 118, 326 158" fill="none" stroke="#a142f4" stroke-width="2.6" class="sc-arc-flow" />
                  <circle r="4" fill="#a142f4"><animateMotion dur="1.7s" repeatCount="indefinite" path="M 88 162 C 118 96, 136 57, 166 57" /></circle>
                  <circle r="4" fill="#a142f4"><animateMotion dur="1.7s" repeatCount="indefinite" path="M 268 57 C 298 57, 312 118, 326 158" /></circle>
                ` : ''}
                ${showOcean ? `
                  <path d="M 88 178 L 166 178" fill="none" stroke="#00d2ff" stroke-width="3" class="sc-arc-flow" />
                  <path d="M 268 178 L 320 178" fill="none" stroke="#00d2ff" stroke-width="3" class="sc-arc-flow" />
                  <!-- Sea-Air Dynamic Upgrade Arc (Port -> Air Hub) -->
                  <path d="M 217 155 L 217 80" fill="none" stroke="#38bdf8" stroke-width="1.6" stroke-dasharray="4 3" />
                  <circle r="4.5" fill="#00d2ff"><animateMotion dur="2.6s" repeatCount="indefinite" path="M 88 178 L 166 178" /></circle>
                  <circle r="4.5" fill="#00d2ff"><animateMotion dur="2.2s" repeatCount="indefinite" path="M 268 178 L 320 178" /></circle>
                ` : ''}
                ${showRail ? `
                  <path d="M 88 194 C 118 254, 136 299, 166 299" fill="none" stroke="#10b981" stroke-width="2.6" class="sc-arc-flow" />
                  <path d="M 268 299 C 298 299, 312 238, 326 198" fill="none" stroke="#10b981" stroke-width="2.6" class="sc-arc-flow" />
                  <circle r="4" fill="#10b981"><animateMotion dur="2.3s" repeatCount="indefinite" path="M 88 194 C 118 254, 136 299, 166 299" /></circle>
                  <circle r="4" fill="#10b981"><animateMotion dur="2.1s" repeatCount="indefinite" path="M 268 299 C 298 299, 312 238, 326 198" /></circle>
                ` : ''}
                ${showRoad ? `
                  <!-- Google Maps Road Fleet Corridors (Cross-Dock -> C1/C2/C3/C4 Stops) -->
                  <path d="M 376 164 C 415 110, 452 72, 502 52" fill="none" stroke="#4285f4" stroke-width="2.8" class="sc-arc-flow" />
                  <path d="M 376 173 C 422 152, 458 134, 504 122" fill="none" stroke="#fbbc04" stroke-width="2.8" class="sc-arc-flow" />
                  <path d="M 376 184 C 422 206, 458 224, 504 238" fill="none" stroke="#10b981" stroke-width="2.8" class="sc-arc-flow" />
                  <path d="M 376 192 C 415 248, 452 286, 502 310" fill="none" stroke="#a142f4" stroke-width="2.8" class="sc-arc-flow" />
                  <circle r="4" fill="#4285f4"><animateMotion dur="1.9s" repeatCount="indefinite" path="M 376 164 C 415 110, 452 72, 502 52" /></circle>
                  <circle r="4" fill="#fbbc04"><animateMotion dur="2.1s" repeatCount="indefinite" path="M 376 173 C 422 152, 458 134, 504 122" /></circle>
                  <circle r="4" fill="#10b981"><animateMotion dur="2.0s" repeatCount="indefinite" path="M 376 184 C 422 206, 458 224, 504 238" /></circle>
                  <circle r="4" fill="#a142f4"><animateMotion dur="1.8s" repeatCount="indefinite" path="M 376 192 C 415 248, 452 286, 502 310" /></circle>
                ` : ''}
              `}

              <!-- Right Road Fleet Customer Corridor Endpoints (Strictly <= 515 so zero overlap with HUD at x=540) -->
              <g opacity="${showRoad ? '1' : '0.25'}">
                <circle cx="502" cy="52" r="5" fill="#4285f4" />
                <text x="492" y="42" text-anchor="end" fill="#8ab4f8" font-size="8.5" font-weight="700">🚚 C1 · 24T FTL</text>
                <circle cx="504" cy="122" r="5" fill="#fbbc04" />
                <text x="494" y="112" text-anchor="end" fill="#fde293" font-size="8.5" font-weight="700">🚚 C2 · 12T LIFO</text>
                <circle cx="504" cy="238" r="5" fill="#10b981" />
                <text x="494" y="254" text-anchor="end" fill="#6ee7b7" font-size="8.5" font-weight="700">🚚 C3 · 7.5T REEFER</text>
                <circle cx="502" cy="310" r="5" fill="#a142f4" />
                <text x="492" y="326" text-anchor="end" fill="#d8b4fe" font-size="8.5" font-weight="700">🚐 C4 · EV VAN</text>
              </g>

              <rect x="540" y="28" width="214" height="304" rx="14" fill="rgba(11,15,24,0.94)" stroke="rgba(255,255,255,0.15)" />
              <text x="558" y="56" fill="#8ab4f8" font-size="11.5" font-weight="700">${hudMetrics.title}</text>
              <text x="558" y="96" fill="#9aa0a6" font-size="10.5">${hudMetrics.m1L}</text>
              <text x="558" y="122" fill="${corridorOpt?'#81c995':'#ff8a80'}" font-size="20" font-weight="700">${hudMetrics.m1V}</text>
              <text x="558" y="168" fill="#9aa0a6" font-size="10.5">${hudMetrics.m2L}</text>
              <text x="558" y="194" fill="#f8f9fa" font-size="20" font-weight="700">${hudMetrics.m2V}</text>
              <text x="558" y="240" fill="#9aa0a6" font-size="10.5">${hudMetrics.m3L}</text>
              <text x="558" y="266" fill="#8ab4f8" font-size="19" font-weight="700">${hudMetrics.m3V}</text>
              <text x="558" y="304" fill="#34a853" font-size="10" font-weight="700">✓ Maps API + OR-Tools + Spanner</text>
            </svg>
          </div>
        `;
      }

      if (cadType === 'warehouse_crane') {
        const cranePath = warehouseGolden
          ? 'M 60 175 L 148 68 L 148 134 L 148 200 L 148 266 L 60 295'
          : 'M 60 175 L 438 68 L 206 134 L 438 200 L 322 266 L 60 295';
        return `
          <div id="${mountId}" style="width:100%;">
            <div class="cad-bar">
              <span style="color:#8ab4f8;font-weight:700;">Interactive 3D Warehouse Slotting &amp; MEIO Twin</span>
              <div style="display:flex;gap:8px;">
                <button type="button" class="cad-pill-btn ${!warehouseGolden?'active':''}" onclick="warehouseGolden=false;refreshCadMount('${cadType}','${mountId}')">
                  ✕ Legacy Random Slotting
                </button>
                <button type="button" class="cad-pill-btn ${warehouseGolden?'active':''}" onclick="warehouseGolden=true;refreshCadMount('${cadType}','${mountId}')">
                  ✦ Golden-Zone Affinity Slotting (-28% Travel)
                </button>
              </div>
            </div>
            <svg viewBox="0 0 780 350" style="width:100%;height:auto;display:block;background:#04070f;">
              <text x="90" y="34" fill="#8ab4f8" font-size="10.5" font-weight="700">GOLDEN ZONE (HIGH-VELOCITY AFFINITY BAYS)</text>
              ${[0,1,2,3].map(r => {
                const y = 48 + r * 66;
                return `<g>
                  ${[0,1,2,3,4,5,6].map(b => {
                    const x = 90 + b * 58;
                    const fast = warehouseGolden ? (b <= 1) : ((r + b) % 3 === 0);
                    return `<rect x="${x}" y="${y}" width="48" height="38" rx="6"
                                  fill="${fast ? '#4285f4' : '#1e293b'}" fill-opacity="${fast ? '0.45' : '0.25'}"
                                  stroke="${fast ? '#8ab4f8' : '#475569'}" stroke-width="1.4" />`;
                  }).join('')}
                </g>`;
              }).join('')}
              <path d="${cranePath}"
                    fill="none" stroke="${warehouseGolden ? '#34a853' : '#ea4335'}" stroke-width="3.2" class="sc-arc-flow" />
              <circle r="5" fill="${warehouseGolden ? '#34a853' : '#ea4335'}">
                <animateMotion dur="${warehouseGolden ? '2.4s' : '4.2s'}" repeatCount="indefinite" path="${cranePath}" />
              </circle>
              <rect x="540" y="28" width="214" height="294" rx="14" fill="rgba(11,15,24,0.94)" stroke="rgba(255,255,255,0.15)" />
              <text x="558" y="56" fill="#8ab4f8" font-size="12" font-weight="700">SLOTTING &amp; MEIO HUD</text>
              <text x="558" y="96" fill="#9aa0a6" font-size="11">PICKER TRAVEL / WAVE</text>
              <text x="558" y="122" fill="${warehouseGolden?'#81c995':'#ff8a80'}" font-size="22" font-weight="700">${warehouseGolden ? '1.18 km (-28%)' : '1.64 km'}</text>
              <text x="558" y="168" fill="#9aa0a6" font-size="11">WORKING CAPITAL</text>
              <text x="558" y="194" fill="#81c995" font-size="22" font-weight="700">-18.0% Buffer Cash</text>
              <text x="558" y="240" fill="#9aa0a6" font-size="11">ORDER FILL RATE SLA</text>
              <text x="558" y="266" fill="#8ab4f8" font-size="20" font-weight="700">${warehouseGolden ? '99.4% OTIF SLA' : '94.1% Split-Ship'}</text>
            </svg>
          </div>
        `;
      }

      if (cadType === 'supplier_radar') {
        return `
          <div id="${mountId}" style="width:100%;">
            <div class="cad-bar">
              <span style="color:#8ab4f8;font-weight:700;">Interactive Multi-Tier (Tier-3 → Tier-1) Supply Network Graph</span>
              <div style="display:flex;gap:8px;">
                <button type="button" class="cad-pill-btn ${!tier2Disrupted?'active':''}" onclick="tier2Disrupted=false;refreshCadMount('${cadType}','${mountId}')">
                  ✓ Nominal Multi-Tier Flow
                </button>
                <button type="button" class="cad-pill-btn ${tier2Disrupted?'active':''}" onclick="tier2Disrupted=true;refreshCadMount('${cadType}','${mountId}')">
                  ⚡ Simulate Tier-2 Disruption &amp; Auto-Reroute
                </button>
              </div>
            </div>
            <svg viewBox="0 0 780 350" style="width:100%;height:auto;display:block;background:#04070f;">
              <text x="85" y="54" text-anchor="middle" fill="#64748b" font-size="10" font-weight="700">TIER-3 RAW</text>
              <text x="235" y="54" text-anchor="middle" fill="#64748b" font-size="10" font-weight="700">TIER-2 SUB-ASSY</text>
              <text x="390" y="54" text-anchor="middle" fill="#64748b" font-size="10" font-weight="700">TIER-1 MODULE</text>
              <text x="496" y="54" text-anchor="middle" fill="#64748b" font-size="10" font-weight="700">PLANT MES</text>

              <line x1="85" y1="115" x2="235" y2="115" stroke="#4285f4" stroke-width="2.4" class="sc-arc-flow" />
              <line x1="85" y1="235" x2="235" y2="235" stroke="#34a853" stroke-width="2.4" class="sc-arc-flow" />
              <line x1="235" y1="115" x2="390" y2="175" stroke="${tier2Disrupted ? '#ea4335' : '#4285f4'}" stroke-width="2.5" stroke-dasharray="${tier2Disrupted ? '4 6' : '8 5'}" />
              <line x1="235" y1="235" x2="390" y2="175" stroke="#34a853" stroke-width="${tier2Disrupted ? '4' : '2.4'}" class="sc-arc-flow" />
              <line x1="390" y1="175" x2="495" y2="175" stroke="#34a853" stroke-width="3" class="sc-arc-flow" />

              <circle r="4" fill="#34a853">
                <animateMotion dur="2.2s" repeatCount="indefinite" path="M85,235 L235,235 L390,175 L495,175" />
              </circle>

              <circle cx="85" cy="115" r="18" fill="#0b0f18" stroke="#4285f4" stroke-width="2" /><text x="85" y="119" text-anchor="middle" fill="#fff" font-size="10">T3-A</text>
              <circle cx="85" cy="235" r="18" fill="#0b0f18" stroke="#34a853" stroke-width="2" /><text x="85" y="239" text-anchor="middle" fill="#fff" font-size="10">T3-B</text>
              <circle cx="235" cy="115" r="24" fill="#0b0f18" stroke="${tier2Disrupted ? '#ea4335' : '#4285f4'}" stroke-width="2.6" />
              <text x="235" y="119" text-anchor="middle" fill="${tier2Disrupted ? '#ff8a80' : '#fff'}" font-size="10" font-weight="700">${tier2Disrupted ? 'HALT' : 'T2-PRI'}</text>
              <circle cx="235" cy="235" r="24" fill="#0b0f18" stroke="#34a853" stroke-width="2.6" /><text x="235" y="239" text-anchor="middle" fill="#81c995" font-size="10" font-weight="700">T2-ALT</text>
              <circle cx="390" cy="175" r="25" fill="#0b0f18" stroke="#4285f4" stroke-width="2.5" /><text x="390" y="179" text-anchor="middle" fill="#fff" font-size="10" font-weight="700">TIER-1</text>
              <rect x="468" y="148" width="56" height="54" rx="10" fill="rgba(52,168,83,0.2)" stroke="#34a853" stroke-width="2.2" /><text x="496" y="179" text-anchor="middle" fill="#fff" font-size="10" font-weight="700">PLANT</text>

              <rect x="540" y="28" width="214" height="294" rx="14" fill="rgba(11,15,24,0.94)" stroke="rgba(255,255,255,0.15)" />
              <text x="558" y="56" fill="#81c995" font-size="12" font-weight="700">SOURCING &amp; RISK HUD</text>
              <text x="558" y="96" fill="#9aa0a6" font-size="11">CONTINUITY STATUS</text>
              <text x="558" y="122" fill="#81c995" font-size="18" font-weight="700">${tier2Disrupted ? 'Auto-Rerouted to T2-ALT' : 'All Tiers Nominal'}</text>
              <text x="558" y="168" fill="#9aa0a6" font-size="11">SHOULD-COST SAVINGS</text>
              <text x="558" y="194" fill="#81c995" font-size="22" font-weight="700">-6.8% Direct Spend</text>
              <text x="558" y="240" fill="#9aa0a6" font-size="11">EARLY DETECTION LEAD</text>
              <text x="558" y="266" fill="#8ab4f8" font-size="20" font-weight="700">+11 Days Ahead</text>
            </svg>
          </div>
        `;
      }

      // Default: Demand Sensing & S&OP Wave Simulator
      let p50 = [], p90 = [], p10 = [], lag = [];
      for (let i = 0; i <= 28; i++) {
        const x = 45 + i * 16;
        const y = 185 - Math.sin(i * 0.32) * 34 - (i > 14 ? demandSurge * 1.15 : 0);
        p50.push(`${x.toFixed(1)},${y.toFixed(1)}`);
        p90.push(`${x.toFixed(1)},${(y - 24).toFixed(1)}`);
        p10.push(`${x.toFixed(1)},${(y + 24).toFixed(1)}`);
        lag.push(`${x.toFixed(1)},${(185 - Math.sin((i - 3.5) * 0.32) * 34 + 16).toFixed(1)}`);
      }
      const fan = [...p90, ...p10.reverse()].join(' ');
      return `
        <div id="${mountId}" style="width:100%;">
          <div class="cad-bar">
            <span style="color:#8ab4f8;font-weight:700;">Interactive Probabilistic Demand Sensing &amp; S&amp;OP Wave</span>
            <label style="display:inline-flex;align-items:center;gap:10px;color:var(--text-secondary);">
              <span>Simulate Demand Surge: <strong style="color:#81c995">+${demandSurge}%</strong></span>
              <input type="range" min="0" max="45" value="${demandSurge}" oninput="demandSurge=parseInt(this.value,10);refreshCadMount('${cadType}','${mountId}')" />
            </label>
          </div>
          <svg viewBox="0 0 780 350" style="width:100%;height:auto;display:block;background:#04070f;">
            <line x1="45" y1="95" x2="500" y2="95" stroke="rgba(148,163,184,0.12)" stroke-dasharray="3 4" />
            <line x1="45" y1="185" x2="500" y2="185" stroke="rgba(148,163,184,0.12)" stroke-dasharray="3 4" />
            <line x1="45" y1="275" x2="500" y2="275" stroke="rgba(148,163,184,0.12)" stroke-dasharray="3 4" />
            <text x="48" y="44" fill="#8ab4f8" font-size="10.5" font-weight="700">● P50 AI Consensus   ▒ P10–P90 Confidence Band   --- Legacy Lagged ERP</text>
            <polygon points="${fan}" fill="rgba(66,133,244,0.16)" />
            <polyline fill="none" stroke="#ea4335" stroke-width="2" stroke-dasharray="5 5" points="${lag.join(' ')}" />
            <polyline fill="none" stroke="#4285f4" stroke-width="3" points="${p50.join(' ')}" />
            <rect x="540" y="28" width="214" height="294" rx="14" fill="rgba(11,15,24,0.94)" stroke="rgba(255,255,255,0.15)" />
            <text x="558" y="56" fill="#8ab4f8" font-size="12" font-weight="700">DEMAND &amp; S&amp;OP HUD</text>
            <text x="558" y="96" fill="#9aa0a6" font-size="11">FORECAST ACCURACY (VS. WAPE)</text>
            <text x="558" y="122" fill="#81c995" font-size="20" font-weight="700">+24% ($14M+ Saved)</text>
            <text x="558" y="168" fill="#9aa0a6" font-size="11">S&amp;OP CYCLE TIME</text>
            <text x="558" y="194" fill="#8ab4f8" font-size="22" font-weight="700">21 Days → 45 Mins</text>
            <text x="558" y="240" fill="#9aa0a6" font-size="11">NET PROMO ROI</text>
            <text x="558" y="266" fill="#fde293" font-size="20" font-weight="700">+22% Trade Spend</text>
          </svg>
        </div>
      `;
    }

    function refreshCadMount(cadType, mountId) {
      const el = document.getElementById(mountId);
      if (el) {
        el.outerHTML = renderInteractiveCadStage(cadType, mountId);
        const nextEl = document.getElementById(mountId);
        if (nextEl) nextEl.classList.add('cad-stage-anim');
      }
    }

    /* =========================================================================
       STATE & MULTI-PAGE CONTROLLERS
       ========================================================================= */
    let selectedDeptId = null;
    let lastPersonaId = 'demand_planning_dir';
    let stageViewMode = 'cad'; // 'cad' | 'video'
    const customVideos = {};
    const customVcVideos = {};

    function renderStageViewportHtml(item, kind, videoUrl, showVideoPlayer) {
      if (stageViewMode === 'cad') {
        return renderInteractiveCadStage(item.cadType || 'demand_wave', kind + 'CadMount');
      }
      if (showVideoPlayer) {
        return `
          <video id="${kind === 'vc' ? 'vcVideoPlayer' : 'agentVideoPlayer'}" controls autoplay loop muted playsinline src="${videoUrl}"></video>
        `;
      }
      return renderInteractiveCadStage(item.cadType || 'demand_wave', kind + 'CadMount');
    }

    /* =========================================================================
       RICH TEXT, METRIC PILLS, UNDERLINES & STRUCTURED BULLET FORMATTERS
       ========================================================================= */
    function formatRichText(raw) {
      if (!raw) return '';
      let s = String(raw);
      const tokens = [];
      const stash = (html) => {
        const id = `@@SCTOK${tokens.length}@@`;
        tokens.push(html);
        return id;
      };

      // 1. Highlight key metrics, percentages, dollar figures, durations, and tiers
      const metricRegex = /(\\b\\d+\\s*(?:days?|hrs?|hours?|mins?|minutes?|months?|weeks?|secs?|seconds?)\\s*(?:→|to|&rarr;)\\s*\\d+\\s*(?:days?|hrs?|hours?|mins?|minutes?|months?|weeks?|secs?|seconds?)|[+$−-]?\\d+(?:\\.\\d+)?\\s*(?:%|pts|bps|x)\\b|\\$\\d+(?:\\.\\d+)?[BMK+]*\\b|(?:<|>|±)\\s*\\d+(?:\\.\\d+)?\\s*(?:secs?|seconds?|mins?|minutes?|hrs?|hours?|days?|%)?|\\b(?:P10(?:[–-]P90)?|P50|P90|3D\\s+LIFO|Tier-[1234N](?:\\s*to\\s*Tier-[1234N])?|Scope\\s+[123](?:\\/[23])*)\\b)/gi;
      s = s.replace(metricRegex, (m) => stash(`<span class="sc-hl-metric">${m}</span>`));

      // 2. Bold + Accent-Underline key Enterprise Systems, Google Cloud AI, and Solvers
      const underlineRegex = /\\b(SAP S\\/4HANA(?:\\s+(?:MM|PP\\/DS|SD|QM|EWM|TM|PM|CO-PA|aATP))*|SAP IBP|SAP Ariba|SAP EWM|SAP TM|SAP GTS|Oracle OTM|Oracle Fusion ERP|Manhattan Active WMS|Blue Yonder(?:\\s+(?:TMS|WMS|Luminate))?|Kinaxis(?:\\s+RapidResponse)?|Siemens Opcenter(?:\\s+MES)?|Siemens Teamcenter(?:\\s+PLM)?|Rockwell FactoryTalk|CargoWise(?:\\s+One)?|Spire(?:\\s+Global)?(?:\\s+Satellite)?\\s+AIS|FlightAware ADS-B|IATA ONE Record|Railinc(?:\\s+EDI\\s+404)?|Project44|FourKites|Samsara ELD|BigQuery(?:\\s+ML|\\s+GIS|\\s+Twin)?|Cloud Spanner(?:\\s+Graph)?|AlloyDB(?:\\s+pgvector)?|Vertex AI(?:\\s+Agent Engine|\\s+TimesFM)?|Gemini 2\\.5(?:\\s+Pro|\\s+Flash)?|Gemini Enterprise|Google OR-Tools|OR-Tools(?:\\s+CP-SAT|\\s+CVRPTW|\\s+MILP)?|CP-SAT|CVRPTW|MILP|Google Maps(?:\\s+Platform|\\s+Routes(?:\\s+Preferred)?\\s+API|\\s+Fleet Engine)?|WeatherNext 3|Google Earth Engine|AlphaEvolve|Document AI|Apigee|Looker|ASCM SCOR|Supply Chain Twin|Digital Twin)\\b/g;
      s = s.replace(underlineRegex, (m) => stash(`<span class="sc-hl-underline">${m}</span>`));

      // 3. Bold high-impact operational action & value phrases
      const boldRegex = /\\b(100%\\s+deterministic|zero-toil|zero-touch|zero\\s+unverified|signed\\s+write-back|real-time|autonomous(?:ly)?|multi-modal|multi-echelon|end-to-end|root-cause|probabilistic|finite-capacity|axle-weight|cube\\s+utilization|working\\s+capital|service\\s+level|otif(?:\\s+penalties)?|demurrage(?:\\s+&amp;\\s+detention)?|safety\\s+stock|manual\\s+toil|golden\\s+thread)\\b/gi;
      s = s.replace(boldRegex, (m) => stash(`<strong class="sc-hl-bold">${m}</strong>`));

      return s.replace(/@@SCTOK(\\d+)@@/g, (_, idx) => tokens[Number(idx)]);
    }

    function formatRichBullets(raw, bulletColor = '#00d2ff') {
      if (!raw) return '';
      const text = String(raw).trim();
      let parts = text.split(/(?:\\.\\s+|\\s+;\\s+|\\s+—\\s+)/).map(p => p.trim()).filter(Boolean);
      if (parts.length <= 1 && text.length > 125) {
        const commaParts = text.split(/,\\s+(?=(?:and\\s+|while\\s+|reducing\\s+|cutting\\s+|increasing\\s+|triggering\\s+|executing\\s+|eliminating\\s+|fusing\\s+|orchestrating\\s+|dispatching\\s+|verifying\\s+|with\\s+|across\\s+))/i).map(p => p.trim()).filter(Boolean);
        if (commaParts.length > 1) parts = commaParts;
      }
      if (parts.length <= 1) {
        return `<p style="margin:0;">${formatRichText(text)}</p>`;
      }
      return `
        <ul class="sc-rich-points" style="--pt-color: ${bulletColor};">
          ${parts.map(part => {
            const clean = /[.!?]$/.test(part) ? part : part + '.';
            return `<li><span class="sc-pt-bullet" style="color:${bulletColor};">▸</span><span>${formatRichText(clean)}</span></li>`;
          }).join('')}
        </ul>
      `;
    }

    function renderUniversalAgentsHomeBanner() {
      const container = document.getElementById('universalAgentsHomeContainer');
      if (!container) return;
      container.innerHTML = `
        <div class="universal-agents-banner">
          <div style="display:flex; justify-content:space-between; align-items:flex-end; flex-wrap:wrap; gap:14px;">
            <div>
              <div style="font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.12em; color:#38bdf8; margin-bottom:4px;">
                ✦ Shared Cross-Vertical Agentic Mesh · Used by All 26 Personas Across 6 SCOR Domains
              </div>
              <h3 style="font-family:var(--font-display); font-size:24px; font-weight:800; color:#f8fafc;">
                4 Cross-Persona Universal Supply Chain Agents
              </h3>
              <p style="font-size:15px; color:var(--text-secondary); max-width:1160px; margin-top:6px; line-height:1.68;">
                ${formatRichText('Unlike siloed point tools, these 4 Horizontal Control Tower Agents plug into every persona’s daily workflow—connecting Demand, Sourcing, Manufacturing, Warehousing, Multi-Modal Logistics (Ocean/Air/Rail/Road), and Circular ESG on a single BigQuery & Cloud Spanner Digital Twin.')}
              </p>
            </div>
            <button type="button" class="switch-pill" style="border-color:#38bdf888; color:#38bdf8;" onclick="openPersonasDirectoryPage('universal', '', true, 'agents')">
              Explore All 32 Agents in Directory &rarr;
            </button>
          </div>

          <div class="universal-agents-grid">
            ${UNIVERSAL_AGENT_IDS.map(uid => {
              const ag = AGENTS[uid];
              if (!ag) return '';
              return `
                <div class="universal-agent-card" onclick="openAgentPage('${ag.id}', true, event)">
                  <div>
                    <div class="universal-agent-badge">
                      <span>🌐 Universal · All 26 Personas</span>
                    </div>
                    <div class="universal-agent-name">${ag.name}</div>
                    <div class="universal-agent-desc">${formatRichText(ag.shortDesc)}</div>
                  </div>
                  <div class="universal-agent-footer">
                    <span>${ag.badge}</span>
                    <span>Executive Value &amp; Demo &rarr;</span>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>
      `;
    }

    
    /* 8-Vertical Interactive Master Navigation & Tab Controller */
    let currentFrontPageVerticalTab = 'all';

    function switchVerticalTab(vId, btnEl) {
      currentFrontPageVerticalTab = vId;
      document.querySelectorAll('#verticalTabsNavBar .v-tab-btn').forEach(b => {
        const isTarget = b.getAttribute('data-vtab') === vId;
        b.classList.toggle('active', isTarget);
      });

      if (vId === 'all') {
        selectedDeptId = null;
        const activeTabId = selectedDeptId || 'all';
      document.querySelectorAll('#verticalTabsNavBar .v-tab-btn').forEach(b => {
        b.classList.toggle('active', b.getAttribute('data-vtab') === activeTabId);
      });

      document.querySelectorAll('#deptRowContainer .dept-node').forEach(node => {
          node.classList.remove('active');
          node.style.display = 'flex';
        });
        renderDepartmentShowcaseBox();
        const row = document.getElementById('deptRowContainer');
        if (row) row.scrollIntoView({ behavior: 'smooth', block: 'start' });
      } else {
        selectedDeptId = vId;
        document.querySelectorAll('#deptRowContainer .dept-node').forEach(node => {
          const nid = node.getAttribute('data-dept-id');
          const isTarget = nid === vId;
          node.classList.toggle('active', isTarget);
          node.style.display = 'flex'; // keep visible in 4x2 grid
        });
        renderDepartmentShowcaseBox();
        hydrateAssets();
        setTimeout(() => {
          const showcase = document.getElementById('deptShowcaseBoxEl');
          if (showcase) showcase.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 80);
      }
    }

    

    function renderOrgChart() {
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
              <div style="display:inline-flex; align-items:center; gap:6px; padding:4px 11px; border-radius:999px; font-size:11px; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; background:${dept.color}22; color:${dept.color}; border:1px solid ${dept.color}55; margin-bottom:10px;">
                <span>${dept.scorBadge || 'SCOR VERTICAL'}</span>
              </div>
              <div class="dept-node-title">${dept.name}</div>
              <div class="dept-node-sub">${formatRichText(dept.subtitle)}</div>
            </div>
            <div class="dept-anim-stage">
              ${renderSupplyChainWatermarkSvg(dept.watermarkType, dept.color, 'dept-stage-svg')}
              <span class="dept-anim-meta">${dept.personaIds.length} Personas · ${domainAgentCount} Domain + 4 Universal Agents</span>
            </div>
          </div>
        `;
      }).join('');

      renderDepartmentShowcaseBox();
      renderUniversalAgentsHomeBanner();
      renderValueChainEntryCards();
    }

    function getVcWatermarkType(vcId) {
      if (vcId === 'f2f') return 'demand_wave';
      if (vcId === 'o2d') return 'corridor_lifo';
      if (vcId === 's2p') return 'supplier_graph';
      return 'conveyor_rack';
    }

    function toSysArray(sysVal) {
      if (!sysVal) return [];
      if (Array.isArray(sysVal)) return sysVal;
      return String(sysVal).split('·').map(s => s.trim()).filter(Boolean);
    }

    function toggleScDropdown(id) {
      const el = document.getElementById(id);
      if (el) el.classList.toggle('open');
    }

    function isPillOrNavSwitch(ev) {
      if (!ev || !ev.currentTarget) return true;
      const cl = ev.currentTarget.classList;
      return !cl || cl.contains('switch-pill') || cl.contains('nav-pill') || cl.contains('nav-dropdown-item') || cl.contains('back-btn');
    }

    function renderValueChainEntryCards() {
      const vcContainer = document.getElementById('valueChainEntryContainer');
      if (!vcContainer) return;
      vcContainer.innerHTML = Object.values(VALUE_CHAINS).map(vc => {
        const wmType = getVcWatermarkType(vc.id);
        return `
          <div class="vc-entry-card"
               style="--vc-accent: ${vc.color}; --dept-accent: ${vc.color};"
               onclick="openValueChainPage('${vc.id}', true, event)">
            <div style="position:relative; z-index:2;">
              <div class="vc-flow-badge" style="background: ${vc.color}20; color: ${vc.color}; border: 1px solid ${vc.color}50;">
                <span>${vc.flowBadge}</span>
              </div>
              <div class="dept-node-title" style="font-size: 23px;">${vc.shortTitle}</div>
              <div class="dept-node-sub">${formatRichText(vc.cardSubtitle)}</div>
            </div>
            <div class="dept-anim-stage" style="--dept-accent: ${vc.color};">
              ${renderSupplyChainWatermarkSvg(wmType, vc.color, 'dept-stage-svg')}
              <span class="dept-anim-meta">${vc.cardFooterLeft}</span>
            </div>
          </div>
        `;
      }).join('');
    }

    function selectDepartment(deptId, ev) {
      const sRect = getClickedCardRect(ev);
      selectedDeptId = (selectedDeptId === deptId) ? null : deptId;

      // Update active state on the 6 SCOR Vertical cards in-place without re-creating DOM nodes
      document.querySelectorAll('#deptRowContainer .dept-node').forEach(node => {
        const nid = node.getAttribute('data-dept-id');
        const active = nid === selectedDeptId;
        node.classList.toggle('active', active);
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
    }

    function renderVerticalWorkflowStrip(dept) {
      if (!dept) return '';
      if (dept.id === 'demand_sop') {
        return `
          <div style="margin: 18px 0 20px; padding: 16px 20px; background: rgba(14, 165, 233, 0.06); border: 1px solid rgba(14, 165, 233, 0.28); border-radius: 14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
              <div style="font-size:14px; font-weight:800; color:#38bdf8; text-transform:uppercase; letter-spacing:0.06em; display:flex; align-items:center; gap:8px;">
                <span>📅 5-Step Monthly S&amp;OP Cadence Timeline ("Closing the Plan")</span>
              </div>
              <div style="font-size:12px; color:#94a3b8;">
                Rolling 12–24 Months · Unconstrained Consensus &rarr; Constrained Financial Lock
              </div>
            </div>
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px;">
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(14,165,233,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#38bdf8; text-transform:uppercase; letter-spacing:0.05em;">Week 1 · Day 1-5</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">1. Product Review</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Portfolio health, NPI launch schedules, phase-in/phase-out, SKU rationalization &amp; cannibalization models.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(14,165,233,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#38bdf8; text-transform:uppercase; letter-spacing:0.05em;">Week 2 · Day 6-10</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">2. Demand Review</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Unconstrained statistical consensus, trade promo lift, WeatherNext 3 macro sensing, commercial consensus.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(14,165,233,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#38bdf8; text-transform:uppercase; letter-spacing:0.05em;">Week 3 · Day 11-15</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">3. Supply Review</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Rough-cut capacity planning (RCCP), plant bottleneck resolution, supplier lead times, buffer plans.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(14,165,233,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#38bdf8; text-transform:uppercase; letter-spacing:0.05em;">Week 4 · Day 16-20</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">4. Pre-S&amp;OP Financial Sync</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Demand-supply gap trade-offs, financial reconciliation (Revenue vs. EBITDA margin), what-if scenario simulations.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(14,165,233,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#38bdf8; text-transform:uppercase; letter-spacing:0.05em;">Month-End · Day 21-25</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">5. Executive S&amp;OP / IBP</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">CSCO, CFO &amp; CMO consensus plan lock, capital allocation &amp; operating budget release across business units.</div>
              </div>
            </div>
          </div>
        `;
      }
      if (dept.id === 'sourcing_procurement') {
        return `
          <div style="margin: 18px 0 20px; padding: 16px 20px; background: rgba(168, 85, 247, 0.06); border: 1px solid rgba(168, 85, 247, 0.28); border-radius: 14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
              <div style="font-size:14px; font-weight:800; color:#c084fc; text-transform:uppercase; letter-spacing:0.06em; display:flex; align-items:center; gap:8px;">
                <span>🎯 5-Stage Strategic Sourcing &amp; Category Procurement Execution Flow</span>
              </div>
              <div style="font-size:12px; color:#94a3b8;">
                Spend Analysis &rarr; Kraljic Matrix &rarr; Dynamic RFP &rarr; Total Cost of Ownership (TCO) &rarr; SRM
              </div>
            </div>
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px;">
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(168,85,247,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#c084fc; text-transform:uppercase; letter-spacing:0.05em;">Stage 1 &middot; Spend Profiling</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Category &amp; Spend Cube</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Historical spend baseline, vendor concentration, Pareto 80/20 analysis &amp; multi-tier sub-tier dependencies.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(168,85,247,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#c084fc; text-transform:uppercase; letter-spacing:0.05em;">Stage 2 &middot; Kraljic Matrix</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Strategic Portfolio Fit</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Classify spend into Strategic, Bottleneck, Leverage, and Non-Critical quadrants to select negotiation tactics.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(168,85,247,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#c084fc; text-transform:uppercase; letter-spacing:0.05em;">Stage 3 &middot; Market Intel</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Cost Breakdown &amp; Should-Cost</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Raw material index tracking (LME/ICIS), energy indices, labor indices, and clean-sheet should-costing.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(168,85,247,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#c084fc; text-transform:uppercase; letter-spacing:0.05em;">Stage 4 &middot; RFx &amp; TCO</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Dynamic RFP &amp; Selection</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Automated RFP distribution, multi-variable scoring (Quality, Lead Time, ESG, Landed Cost), and contract award.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(168,85,247,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#c084fc; text-transform:uppercase; letter-spacing:0.05em;">Stage 5 &middot; SRM Governance</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Supplier Relationship (SRM)</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Automated PPAP compliance, OTIF audit scorecarding, Tier-N supplier visibility &amp; ESG/CBAM validation.</div>
              </div>
            </div>
          </div>
        `;
      }
      if (dept.id === 'inventory_meio') {
        return `
          <div style="margin: 18px 0 20px; padding: 16px 20px; background: rgba(6, 182, 212, 0.06); border: 1px solid rgba(6, 182, 212, 0.28); border-radius: 14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
              <div style="font-size:14px; font-weight:800; color:#22d3ee; text-transform:uppercase; letter-spacing:0.06em; display:flex; align-items:center; gap:8px;">
                <span>📊 4-Tier Multi-Echelon Network Buffering Flow (MEIO)</span>
              </div>
              <div style="font-size:12px; color:#94a3b8;">
                Stochastic Safety Stock &middot; Dynamic Lateral STO Rebalancing &middot; Sub-50ms ATP
              </div>
            </div>
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px;">
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(6,182,212,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#22d3ee; text-transform:uppercase;">Tier 1 · Central Plant Hub</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Bulk Decoupling Buffers</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Aggregated production inventory buffers; absorbs manufacturing cycle-time variance and batch sizing.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(6,182,212,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#22d3ee; text-transform:uppercase;">Tier 2 · Regional DCs</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Multi-echelon inventory pooling, regional safety stock $Z \cdot \sigma$, and transit pipeline buffering.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(6,182,212,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#22d3ee; text-transform:uppercase;">Tier 3 · Forward Fulfillment Hubs</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Local cross-dock staging, sub-50ms ATP order commitment, and lateral STO rebalancing triggers.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(6,182,212,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#22d3ee; text-transform:uppercase;">Tier 4 · Customer Shelf / POS</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Point-of-Sale consumption sensing, real-time depletion monitoring, and automated replenishment.</div>
              </div>
            </div>
          </div>
        `;
      }
      if (dept.id === 'trade_mkt_dist') {
        return `
          <div style="margin: 18px 0 20px; padding: 16px 20px; background: rgba(245, 158, 11, 0.06); border: 1px solid rgba(245, 158, 11, 0.28); border-radius: 14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
              <div style="font-size:14px; font-weight:800; color:#fbbf24; text-transform:uppercase; letter-spacing:0.06em; display:flex; align-items:center; gap:8px;">
                <span>🏪 5-Stage FMCG/Retail Last-Mile Distribution Flow</span>
              </div>
              <div style="font-size:12px; color:#94a3b8;">
                Primary Billing &rarr; Beat Route Sync &rarr; Live DMS Stock &rarr; Planogram Vision &rarr; Scheme Settlement
              </div>
            </div>
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px;">
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(245,158,11,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#fbbf24; text-transform:uppercase;">Stage 1 · Primary Stock Allocation</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Factory-to-Distributor Billing</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Automated replenishment orders based on distributor buffer norms, credit limits &amp; depot pipeline stock.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(245,158,11,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#fbbf24; text-transform:uppercase;">Stage 2 · FSO Beat Scheduling</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Dynamic Beat Optimization</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Google Maps Routes Preferred sequencing for Field Sales Officers, maximizing productive retail counter calls.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(245,158,11,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#fbbf24; text-transform:uppercase;">Stage 3 · Store Pitch &amp; Live Stock</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Zero Out-of-Stock Pitches</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Real-time DMS inventory check upon store entry; dynamically swaps stocked-out items for available variants.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(245,158,11,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#fbbf24; text-transform:uppercase;">Stage 4 · Shelf Vision Audit</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Gemini 3.8 Flash Planogram</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Instant multimodal classification of shelf photos; verifies brand facings, SOS &amp; calculates payout compliance.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(245,158,11,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#fbbf24; text-transform:uppercase;">Stage 5 · Trade Scheme Settlement</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Automated Credit Notes</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Reconciles secondary sales volume slabs, strips phantom invoices &amp; issues SAP credit notes in &lt;2 hours.</div>
              </div>
            </div>
          </div>
        `;
      }
      if (dept.id === 'manufacturing_prod') {
        return `
          <div style="margin: 18px 0 20px; padding: 16px 20px; background: rgba(249, 115, 22, 0.06); border: 1px solid rgba(249, 115, 22, 0.28); border-radius: 14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
              <div style="font-size:14px; font-weight:800; color:#fb923c; text-transform:uppercase; letter-spacing:0.06em; display:flex; align-items:center; gap:8px;">
                <span>⚙️ 5-Level Hierarchical Production Planning Framework</span>
              </div>
              <div style="font-size:12px; color:#94a3b8;">
                Strategic Capacity &rarr; S&amp;OP Leveling &rarr; MPS Master Schedule &rarr; MRP BOM Explosion &rarr; MES Finite Sequencing
              </div>
            </div>
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px;">
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(249,115,22,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#fb923c; text-transform:uppercase; letter-spacing:0.05em;">Level 1 &middot; Long Range (1-5 Yrs)</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Strategic Capacity Planning</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Global plant footprints, line additions, CapEx budgeting &amp; technology investments.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(249,115,22,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#fb923c; text-transform:uppercase; letter-spacing:0.05em;">Level 2 &middot; Medium Range (3-18 Mo)</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">S&amp;OP Aggregate Plan</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Product family leveling, seasonal pre-build inventory, shift patterns &amp; contract manufacturing allocation.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(249,115,22,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#fb923c; text-transform:uppercase; letter-spacing:0.05em;">Level 3 &middot; Operational (1-12 Wks)</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Master Production Schedule (MPS)</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Finished goods batch sizing, line slotting, frozen fence enforcement &amp; rough-cut capacity checks.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(249,115,22,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#fb923c; text-transform:uppercase; letter-spacing:0.05em;">Level 4 &middot; Tactical (Daily/Weekly)</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">MRP BOM Explosion</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Dependent demand calculation for sub-assemblies/raw materials, gross-to-net netting, planned production orders.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(249,115,22,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#fb923c; text-transform:uppercase; letter-spacing:0.05em;">Level 5 &middot; Execution (Shift/Hour)</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Finite Scheduling &amp; MES OEE</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">OR-Tools CP-SAT machine sequencing, changeover minimization, real-time telemetry &amp; scrap root-cause triage.</div>
              </div>
            </div>
          </div>
        `;
      }
            if (dept.id === 'warehouse_intralogistics') {
        return `
          <div style="margin: 18px 0 20px; padding: 16px 20px; background: rgba(59, 130, 246, 0.06); border: 1px solid rgba(59, 130, 246, 0.28); border-radius: 14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
              <div style="font-size:14px; font-weight:800; color:#60a5fa; text-transform:uppercase; letter-spacing:0.06em; display:flex; align-items:center; gap:8px;">
                <span>🏢 5-Stage Inbound Inwarding, Cross-Dock &amp; Automated Slotting Flow</span>
              </div>
              <div style="font-size:12px; color:#94a3b8;">
                ASN Scheduling &rarr; Vision Gate &rarr; Cross-Dock Decision &rarr; 3D AS/RS Slotting &rarr; Wave Pick
              </div>
            </div>
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px;">
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(59,130,246,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#60a5fa; text-transform:uppercase;">Stage 1 · Advance ASN</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Dock Door Scheduling</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">EDI 856 ingestion, trailer yard check-in, dynamic dock door assignment &amp; demurrage prevention.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(59,130,246,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#60a5fa; text-transform:uppercase;">Stage 2 · Vision Gate</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Automated Inspection</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Camera portal pallet scan; detects crushed cartons, tilted stacks, and barcode read errors in &lt;1.2s.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(59,130,246,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#60a5fa; text-transform:uppercase;">Stage 3 · Cross-Dock</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Zero-Putaway Staging</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Matches hot outbound backorders to bypass storage racks, moving straight to outbound outbound trailers.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(59,130,246,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#60a5fa; text-transform:uppercase;">Stage 4 · 3D Slotting</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">AS/RS &amp; High-Bay Racks</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Multi-objective integer program places high-velocity SKUs at ergonomic levels with strict thermal zoning.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(59,130,246,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#60a5fa; text-transform:uppercase;">Stage 5 · Outbound Wave</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Pick Path Optimization</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Batch wave releases and AGV traveling salesman routing, minimizing picker deadhead travel by 32%.</div>
              </div>
            </div>
          </div>
        `;
      }
      if (dept.id === 'logistics_fleet') {
        return `
          <div style="margin: 18px 0 20px; padding: 16px 20px; background: rgba(99, 102, 241, 0.06); border: 1px solid rgba(99, 102, 241, 0.28); border-radius: 14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
              <div style="font-size:14px; font-weight:800; color:#818cf8; text-transform:uppercase; letter-spacing:0.06em; display:flex; align-items:center; gap:8px;">
                <span>🚚 5-Stage Multi-Modal Corridor Dispatch &amp; Linehaul Flow</span>
              </div>
              <div style="font-size:12px; color:#94a3b8;">
                3D Bay Packing &rarr; Mode Split &rarr; Dynamic Route Dispatch &rarr; Cold-Chain Tracking &rarr; Digital ePOD
              </div>
            </div>
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px;">
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(99,102,241,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#818cf8; text-transform:uppercase;">Stage 1 · 3D Bay Packing</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">LIFO Axle-Weight Balance</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Physics-constrained 3D bin packing; optimizes axle weight distribution and reverse stop-drop sequencing.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(99,102,241,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#818cf8; text-transform:uppercase;">Stage 2 · Mode Split</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Air / Rail / Ocean / Road</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Trade-off solver balances freight cost vs carbon vs customer SLA, shifting freight to rail or ocean where viable.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(99,102,241,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#818cf8; text-transform:uppercase;">Stage 3 · Dynamic Routing</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Google Maps Fleet Engine</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Routes Preferred routing with live traffic, bridge height clearances, and driver corridor familiarity.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(99,102,241,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#818cf8; text-transform:uppercase;">Stage 4 · In-Transit Hub</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Satellite &amp; Telematics IoT</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Real-time Spire AIS / FlightAware / ELD tracking, geofence ETA countdowns, and cold-chain alert triggers.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(99,102,241,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#818cf8; text-transform:uppercase;">Stage 5 · Digital ePOD</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Instant Proof of Delivery</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Geofenced signature capture, discrepancy OS&amp;D logging, and automated freight audit freight billing lock.</div>
              </div>
            </div>
          </div>
        `;
      }
      if (dept.id === 'reverse_logistics_esg') {
        return `
          <div style="margin: 18px 0 20px; padding: 16px 20px; background: rgba(16, 185, 129, 0.06); border: 1px solid rgba(16, 185, 129, 0.28); border-radius: 14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
              <div style="font-size:14px; font-weight:800; color:#34d399; text-transform:uppercase; letter-spacing:0.06em; display:flex; align-items:center; gap:8px;">
                <span>♻️ 5-Stage Circular Recovery, Component Harvesting &amp; ESG Audit Flow</span>
              </div>
              <div style="font-size:12px; color:#94a3b8;">
                RMA Intake &rarr; Visual Triage &rarr; Component Harvest &rarr; Secondary Resale &rarr; Scope 3 Audit
              </div>
            </div>
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px;">
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(16,185,129,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#34d399; text-transform:uppercase;">Stage 1 · RMA Intake</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Customer Tele-Diagnosis</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Instant digital returns portal; validates warranty, captures failure mode, and generates return routing label.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(16,185,129,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#34d399; text-transform:uppercase;">Stage 2 · Visual Triage</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Gemini 3.8 Flash Grading</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Optical grade classification: directs item to Grade-A Restock, Component Harvest, or E-Waste Recycling.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(16,185,129,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#34d399; text-transform:uppercase;">Stage 3 · Harvesting</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Remanufacturing Ingestion</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Disassembles high-value assemblies; recertifies sub-components and credits net recoverable inventory to MRP.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(16,185,129,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#34d399; text-transform:uppercase;">Stage 4 · Secondary B2B</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Liquidation &amp; Resale</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Dynamic secondary pricing agent matches refurbished inventory to certified outlet channels, recovering 42% margin.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(16,185,129,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#34d399; text-transform:uppercase;">Stage 5 · Scope 3 ESG</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">CBAM &amp; Audit Trail</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Automated emissions ledger tracking avoided carbon and circularity ratio for SEC / EU CSRD compliance.</div>
              </div>
            </div>
          </div>
        `;
      }

      return '';
    }

    function renderDepartmentShowcaseBox() {
      const container = document.getElementById('deptShowcaseContainer');
      if (!container) return;
      if (!selectedDeptId || !DEPARTMENTS[selectedDeptId]) {
        container.innerHTML = '';
        return;
      }
      const dept = DEPARTMENTS[selectedDeptId];
      const drawerId = `deptSpecDrawer_${dept.id}`;

      container.innerHTML = `
        <div id="deptShowcaseBoxEl" class="dept-showcase-box genie-enter" style="--dept-accent: ${dept.color};">
          <div class="showcase-header">
            <div class="showcase-dept-name">
              <span class="accent-dot" style="background: ${dept.color}; box-shadow: 0 0 12px ${dept.color};"></span>
              <span>${dept.fullName}</span>
            </div>
            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
              <button type="button" class="switch-pill" onclick="openPersonasDirectoryPage('${dept.id}', '', true)">
                View All ${dept.personaIds.length} Personas in Directory &rarr;
              </button>
              <button type="button" class="switch-pill" onclick="selectDepartment('${dept.id}')">
                ✕ Collapse Drawer
              </button>
            </div>
          </div>

          <!-- Live Supply Chain Visual Strip inside the expanded Department Box -->
          <div class="showcase-visual-strip" style="border-color: ${dept.color}44;">
            <div style="width:210px; height:96px; flex-shrink:0; border-radius:14px; background:rgba(4,9,18,0.92); border:1px solid ${dept.color}55; overflow:hidden; display:flex; align-items:center; justify-content:center; padding:6px;">
              ${renderSupplyChainWatermarkSvg(dept.watermarkType, dept.color, 'dept-stage-svg')}
            </div>
            <div class="showcase-visual-meta">
              <div class="showcase-visual-title" style="color:${dept.color};">
                <span>⚡ Live Supply Chain Control Tower Telemetry · ${dept.name}</span>
              </div>
              <div class="showcase-visual-desc">
                ${formatRichText(`${dept.subtitle} — Autonomous multi-agent sensing, digital-twin validation, and zero-toil ERP/WMS/TMS execution across ${dept.personaIds.length} core supply chain roles.`)}
              </div>
            </div>
          </div>

          <!-- Executive Problem, Solution & Business Value Grid (CFO Model) -->
          <div class="showcase-exec-grid" style="display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap:16px; margin: 20px 0 16px;">
            <!-- Column 1: Problem / Manual Toil -->
            <div class="showcase-panel" style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(239, 68, 68, 0.28); border-radius: 14px; padding: 18px 20px;">
              <div class="panel-tag" style="color: #f87171; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
                <span>✕ The Critical Problem · Legacy Process Gaps</span>
              </div>
              <div class="panel-metric" style="font-size:20px; font-weight:800; color:#fff; margin-bottom:12px;">${dept.toilMetric}</div>
              <ul class="clean-list" style="list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:10px;">
                ${dept.toilBullets.map(b => `
                  <li style="display:flex; align-items:flex-start; gap:8px; font-size:13.5px; color:#cbd5e1; line-height:1.5;">
                    <span class="bullet" style="color: #f87171; font-weight:bold; flex-shrink:0;">▸</span>
                    <span>${formatRichText(b)}</span>
                  </li>
                `).join('')}
              </ul>
            </div>

            <!-- Column 2: Agentic Solution -->
            <div class="showcase-panel" style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(16, 185, 129, 0.28); border-radius: 14px; padding: 18px 20px;">
              <div class="panel-tag" style="color: #34d399; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
                <span>✦ The AI Solution · Gemini &amp; Math Solvers</span>
              </div>
              <div class="panel-metric" style="font-size:20px; font-weight:800; color:#fff; margin-bottom:12px;">${dept.impactMetric}</div>
              <ul class="clean-list" style="list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:10px;">
                ${dept.impactBullets.map(b => `
                  <li style="display:flex; align-items:flex-start; gap:8px; font-size:13.5px; color:#cbd5e1; line-height:1.5;">
                    <span class="bullet" style="color: #34d399; font-weight:bold; flex-shrink:0;">▸</span>
                    <span>${formatRichText(b)}</span>
                  </li>
                `).join('')}
              </ul>
            </div>

            <!-- Column 3: Quantified Business Value & Working Capital Impact -->
            <div class="showcase-panel" style="background: rgba(15, 23, 42, 0.85); border: 1px solid ${dept.color}44; border-radius: 14px; padding: 18px 20px; display:flex; flex-direction:column; justify-content:space-between;">
              <div>
                <div class="panel-tag" style="color: ${dept.color}; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
                  <span>💎 Strategic Value &amp; Bottom-Line Outcomes</span>
                </div>
                <div class="panel-metric" style="font-size:20px; font-weight:800; color:#fff; margin-bottom:10px;">
                  ${dept.vNum} · ${dept.tagline}
                </div>
                <div style="font-size:13px; color:#94a3b8; line-height:1.5; margin-bottom:14px;">
                  ${dept.coreQuestion || dept.subtitle}
                </div>
                <div style="display:flex; flex-direction:column; gap:8px; font-size:12.5px; color:#cbd5e1;">
                  <div style="display:flex; justify-content:space-between; padding:6px 10px; background:rgba(255,255,255,0.04); border-radius:8px;">
                    <span style="color:#94a3b8;">Operational Horizon:</span>
                    <strong style="color:#fff;">${dept.horizon}</strong>
                  </div>
                  <div style="display:flex; justify-content:space-between; padding:6px 10px; background:rgba(255,255,255,0.04); border-radius:8px;">
                    <span style="color:#94a3b8;">Enterprise Flow:</span>
                    <strong style="color:#38bdf8;">${dept.flow || 'Physical & Signal Flow'}</strong>
                  </div>
                  <div style="display:flex; justify-content:space-between; padding:6px 10px; background:rgba(255,255,255,0.04); border-radius:8px;">
                    <span style="color:#94a3b8;">Human-in-the-Loop Gate:</span>
                    <strong style="color:#34d399;">100% Signed ERP Writeback</strong>
                  </div>
                </div>
              </div>

              <div style="margin-top:14px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.08); display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:12px; color:#94a3b8;">${dept.personaIds.length} Personas · ${dept.agentIds.length} Agents</span>
                <button type="button" class="switch-pill" style="font-size:12px; padding:6px 14px;" onclick="openPersonasDirectoryPage('${dept.id}', '', true)">
                  View in Directory &rarr;
                </button>
              </div>
            </div>
          </div>

          <!-- Vertical Operational & Distribution Workflow Sequence -->
          ${renderVerticalWorkflowStrip(dept)}

          <!-- Personas in this Vertical (Clean, Uncongested Click-to-Open List) -->
          <div style="margin-top: 24px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.08);">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:14px;">
              <div style="font-size:15px; font-weight:800; color:#fff; display:flex; align-items:center; gap:8px;">
                <span class="accent-dot" style="background:${dept.color}; box-shadow:0 0 10px ${dept.color};"></span>
                <span>Personas in ${dept.name} (${dept.personaIds.length} Core Roles)</span>
              </div>
              <div style="font-size:12px; color:var(--text-muted);">
                Click any persona to open their dedicated schedule &amp; AI agents &rarr;
              </div>
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
                    <span class="persona-open-arrow" style="color:${dept.color};">Open &rarr;</span>
                  </div>
                `;
              }).join('')}
            </div>
          </div>

          <!-- Collapsible Dropdown Drawer for Systems of Record & Solver Stack -->
          <div id="${drawerId}" class="sc-dropdown-block" style="position:relative; z-index:2; margin-top:18px;">
            <button type="button" class="sc-dropdown-btn" onclick="toggleScDropdown('${drawerId}')">
              <span>🔧 Enterprise Systems of Record, EDI Feeds &amp; AI Solver Stack (${dept.name})</span>
              <span class="sc-dropdown-chevron">▾</span>
            </button>
            <div class="sc-dropdown-body">
              <div class="sc-dropdown-inner">
                <div style="font-size:13px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:8px;">
                  Connected ERP / WMS / TMS / Telemetry Systems
                </div>
                <div class="sc-tech-pills" style="margin-bottom:14px;">
                  ${toSysArray(dept.systems).map(sys => `<span class="sc-tech-pill">${sys}</span>`).join('')}
                </div>
                <div style="font-size:13px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#34d399; margin-bottom:6px;">
                  Active Mathematical &amp; Agentic Reasoning Solvers
                </div>
                <div style="font-size:15.5px; color:var(--text-secondary); line-height:1.68;">
                  ${formatRichBullets(dept.solverSummary || '', '#34d399')}
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    /* =========================================================================
       EXECUTIVE SELLING METADATA HELPER FOR ALL 32 AGENTS
       ========================================================================= */
    function getAgentSellingMeta(ag, dept) {
      const defaultProofByDept = {
        universal_csco: 'GE Appliances (800+ Gemini Enterprise agents · -25% customer backorders) & Unilever ($100M+ productivity savings · 9m → hrs Tier-N mapping).',
        demand_sop: 'GE Appliances (800+ Gemini Enterprise agents · -25% customer backorders) & Google DeepMind WeatherNext 3 + BigQuery TimesFM retail demand sensing.',
        sourcing_procurement: 'Unilever ($100M+ productivity savings · 9 months → hours Tier-N supplier mapping across 60,000+ suppliers) & SAP Ariba / BigQuery Supply Chain Twin.',
        sourcing_risk: 'Unilever ($100M+ productivity savings · 9 months → hours Tier-N supplier mapping across 60,000+ suppliers) & SAP Ariba / BigQuery Supply Chain Twin.',
        manufacturing_prod: 'Global Smart Factory deployments on Google Cloud Manufacturing Data Engine + OR-Tools CP-SAT (+9.4% OEE, -41% unplanned downtime, -52% scrap).',
        inventory_meio: 'Multi-Echelon Network Deployments on BigQuery + Spanner (-18% working capital · $28M+ liquidity unlocked · 99.4% customer line fill).',
        warehousing_qa: 'FM Logistic & Global High-Bay Deployments (AlphaEvolve + Vertex AI · -28% picker travel · <2.5h dock-to-stock · 99.8% pick accuracy).',
        inventory_warehouse: 'FM Logistic (Google DeepMind AlphaEvolve + Vertex AI · -28% picker travel · <2.5h dock-to-stock) & Manhattan Active WMS.',
        logistics_fleet: 'Global Multi-Modal Ocean, Air, Rail & Fleet Operations on Google Cloud OR-Tools + Google Maps Platform (-24% multi-modal cost, -67% port demurrage, -28% air cargo spend, 92% 3D LIFO cube fill).',
        trade_mkt_dist: 'ITC Foods & FMCG Field Operations (Google Maps Platform + BigQuery · +18% distributor case fill rate · zero stockout pitch waste · 100% automated planogram audits).',
        reverse_risk_esg: 'CSCO Circular & ESG Operations on BigQuery + Cloud Spanner (+31% net RMA margin recovery, 99.6% audit-ready Scope 3 primary telemetry).',
        circular_enable: 'CSCO Circular & ESG Operations on BigQuery + Cloud Spanner (+31% net RMA margin recovery, 99.6% audit-ready Scope 3 primary telemetry).'
      };

      const defaultDataByDept = {
        universal_csco: {
          privateData: 'SAP S/4HANA & IBP, Oracle ERP, Manhattan WMS, Blue Yonder TMS, CargoWise, Siemens Opcenter MES, AR/AP & Inventory Ledgers in BigQuery & AlloyDB',
          communityData: 'Tier-1 to Tier-4 Supplier Portals, EDI 850/856/214/315/404, Spire Ocean AIS, FlightAware ADS-B, Project44 / FourKites, Retailer CPFR Portals',
          publicData: 'Google DeepMind WeatherNext 3 Ensembles, Google Maps Live Traffic, Google Earth Engine, Global Port AIS & Macro Commodity/FX Indices'
        },
        demand_sop: {
          privateData: 'POS Sell-Through, SAP S/4HANA Order History, Trade Promo Calendars, Plant Capacity & SKU Margin Tables (SAP IBP / Kinaxis) in BigQuery & AlloyDB',
          communityData: 'Retailer CPFR Portals (Walmart Luminate, Target Greenfield, Amazon Vendor Central), Circana/NIQ Scanner Feeds, Distributor EDI 852 Feeds',
          publicData: 'Google DeepMind WeatherNext 3 (15-Day Sub-County Ensembles), Google Maps Places Foot-Traffic, Google Trends Search Velocity, Local Event Signals'
        },
        sourcing_risk: {
          privateData: 'SAP Ariba Contracts, Approved Vendor List (AVL), Multi-Level SAP & Siemens Teamcenter BOMs, PPAP & Incoming Lot Inspection Logs in Cloud Spanner & AlloyDB',
          communityData: 'Tier-1/2/3/4 Supplier Portals, Customs BOL & Ocean AIS Graphs, EDI 850/855/856 ASN Streams, Dun & Bradstreet Financial Health & COA Certificates',
          publicData: 'Google WeatherNext 3 Typhoon/Flood Tracks, Google Earth Engine Canopy Maps, London Metal Exchange (LME), ICIS Resin & USITC/TARIC Tariff Schedules'
        },
        manufacturing_prod: {
          privateData: 'SAP S/4HANA PP/DS & PM, Siemens Opcenter / Rockwell FactoryTalk MES, OSIsoft PI Historian 10kHz Vibration & Thermal Streams, Teamcenter PLM BOMs',
          communityData: 'Contract Manufacturer (CMO/EMS) Capacity Feeds, Tooling Vendor Lead-Time Portals, Outbound Ocean/Air/Rail/Truck Cutoff Schedules',
          publicData: 'Regional Power Grid Tariff & Peak-Demand Schedules, Ambient Humidity/Temperature Feeds, ISO/IATF Quality Standards'
        },
        inventory_warehouse: {
          privateData: 'Manhattan Active WMS / SAP EWM Bin-Level Inventory, IBM Sterling OMS, RF Gun & AMR/ASRS Telemetry, CubiScan 3D Carton Dimensions in Cloud Spanner & AlloyDB',
          communityData: 'Inbound Ocean Container (EDI 315), Air ULD (e-AWB) & Rail (EDI 404) ASNs, FourKites / Project44 Yard ETA Streams, 3PL Capacity Portals',
          publicData: 'Google Maps Distance Matrix & Live Highway Traffic, Port-to-DC Drayage Congestion Indices, Seasonal Peak Volume Curves'
        },
        logistics_fleet: {
          privateData: 'SAP TM, Blue Yonder TMS, Oracle OTM & CargoWise Manifests, Samsara ELD & Sensitech Reefer IoT, 3D Carton/Pallet/ULD Dimensions & Axle Weight Limits',
          communityData: 'Spire Global / MarineTraffic Satellite Vessel AIS, INTTRA Ocean Bookings, IATA ONE Record / Cargo-XML e-AWB, FlightAware ADS-B, Railinc EDI 404/417, Project44 / FourKites',
          publicData: 'Google Maps Routes Preferred API & Fleet Engine Live Traffic, Google DeepMind WeatherNext 3 Marine/Aviation/Highway Alerts, Drewry WCI, TAC Air & DAT Spot Indices'
        },
        trade_mkt_dist: {
          privateData: 'Distributor Management System (DMS) secondary sales records, opening/closing stock ledgers, retailer credit master & trade scheme agreements in BigQuery & AlloyDB',
          communityData: 'Field Sales Officer (FSO) daily GPS store check-ins, geo-tagged store shelf/chiller photos, distributor delivery van manifests, distributor purchase orders',
          publicData: 'Google Maps Live Traffic, local market festival surge calendars, competitor FMCG retail pricing, GST tax compliance ledgers'
        },
        inventory_meio: {
          privateData: 'SAP S/4HANA material ledger, depot safety stocks, BOM gross-to-net requirements, SKU carrying costs & service level SLAs in BigQuery & Cloud Spanner',
          communityData: 'Vendor ASN delivery streams, transit stock transfer orders (STOs), regional DC replenishment requests, 3PL inventory advice (EDI 846)',
          publicData: 'Google Maps Distance Matrix transit durations, regional seasonal demand volatility, commodity interest rates (WACC)'
        },
        warehousing_qa: {
          privateData: 'Manhattan Active WMS bin-level inventory, SAP EWM putaway rules, RF scan timestamps, CubiScan 3D carton dimensions, AQL defect tolerance tables in Cloud Spanner & AlloyDB',
          communityData: 'Inbound ocean/air/rail ASNs (EDI 856/315/404), carrier yard check-in timestamps, supplier COA lab certificates, 3PL cross-dock transshipment logs',
          publicData: 'Highway congestion around port/DC corridors, ambient dock weather/humidity feeds'
        },
        circular_enable: {
          privateData: 'Loop / Narvar RMA Logs, SAP S/4HANA SD/QM/CO-PA, PLM Engineering BOMs, Scope 1/2/3 Emissions Ledgers in BigQuery & Cloud Spanner',
          communityData: 'Walmart Luminate / Target / Kroger OTIF Portals, Supplier Primary Carbon PCF Declarations, GLEC / ISO-14083 Multi-Modal Carrier Fuel Telemetry',
          publicData: 'Google Earth Engine Plot Deforestation Verification (EUDR), Google Maps Geofences & Routes, EU CBAM & CSRD Regulatory Rules'
        }
      };

      const gcpStack = [
        { name: 'BigQuery & BigQuery ML / GIS', role: 'Canonical Supply Chain Digital Twin, spatiotemporal GIS & bayesian ML' },
        { name: 'Cloud Spanner & Spanner Graph', role: 'Multi-tier BOM graph, global ATP inventory ledger & multi-modal network state' },
        { name: 'AlloyDB for PostgreSQL + pgvector', role: 'Sub-millisecond operational state store, contract/tariff vector RAG & agent memory' },
        { name: 'Vertex AI Agent Engine (ADK & A2A)', role: 'Managed runtime orchestrating root supervisor & 3 collaborating A2A sub-agents' },
        { name: 'Gemini 3.1 Pro & Gemini 3.8 Flash', role: 'Multimodal reasoning, COA/contract vision parsing & conversational analytics' },
        { name: 'Google OR-Tools (CP-SAT / CVRPTW / MILP)', role: '100% deterministic finite scheduling, multi-modal routing & 3D LIFO/ULD bin-packing' },
        { name: 'Google Maps Platform (Routes & Fleet Engine)', role: 'Routes Preferred API, Distance Matrix, Live Traffic, Geofencing & Places API' },
        { name: 'Vertex AI TimesFM Foundation Model', role: 'Zero-shot & fine-tuned P10/P50/P90 probabilistic demand & lead-time forecasting' },
        { name: 'Google DeepMind WeatherNext 3 & Earth Engine', role: '15-day hyper-local cyclone/marine/freeze ensembles & satellite plot verification' },
        { name: 'Apigee API Management & Integration Connectors', role: 'Governed, role-scoped BAPI, IDoc, OData, REST & EDI write-back gateway' },
        { name: 'Cloud Pub/Sub, Dataflow & Cloud Run', role: 'Real-time AIS, ADS-B, PLC, RFID & ELD telemetry streaming + 3D solver microservices' },
        { name: 'Document AI & Looker Semantic Layer', role: 'Automated commercial invoice/BOL/e-AWB/COA extraction & governed BI metrics' }
      ];

      const connectorsByDept = {
        universal_csco: [
          'SAP S/4HANA (MM / PP-DS / SD / FI-CO)', 'SAP IBP', 'SAP Ariba & GTS', 'Oracle Fusion ERP & OTM',
          'Manhattan Active WMS & Omni', 'Blue Yonder TMS & Luminate', 'Kinaxis RapidResponse', 'CargoWise One',
          'Spire Satellite Ocean AIS', 'FlightAware ADS-B', 'Railinc EDI 404', 'Project44 & FourKites'
        ],
        demand_sop: [
          'SAP IBP (Demand & S&OP)', 'SAP S/4HANA PP/DS & SD', 'Kinaxis RapidResponse', 'o9 Digital Brain',
          'Salesforce Consumer Goods Cloud', 'Walmart Luminate & Target Greenfield', 'Amazon Vendor Central',
          'EDI 852 (POS Sales) & EDI 830', 'Circana / NielsenIQ Syndicated POS', 'Oracle Hyperion / Anaplan FP&A'
        ],
        sourcing_risk: [
          'SAP Ariba Sourcing & CLM', 'SAP S/4HANA MM & QM', 'SAP GTS (Global Trade Services)', 'Coupa & Icertis CLM',
          'Siemens Teamcenter & PTC Windchill PLM', 'Resilinc & Everstream Risk Feeds', 'TrackWise / Veeva QMS',
          'USITC HTS & EU TARIC Customs Schedules', 'LME / ICIS / Platts Commodity Feeds', 'EDI 850 / 855 / 856 / 860'
        ],
        manufacturing_prod: [
          'SAP S/4HANA PP/DS, PM & QM', 'Siemens Opcenter MES', 'Rockwell FactoryTalk / Plex MES', 'OSIsoft PI / AVEVA Historian',
          'Siemens SIMATIC & Allen-Bradley PLCs (OPC-UA)', 'Cognex & Keyence Inline Vision', 'Siemens Teamcenter PLM (CC02)',
          'Kinaxis RapidResponse', 'Electronic Batch Record (eBHR)', 'MRO Crib & Tooling Matrix Systems'
        ],
        inventory_warehouse: [
          'Manhattan Active WMS & YMS', 'SAP EWM (Extended Warehouse Mgmt)', 'SAP S/4HANA aATP & MM', 'Blue Yonder WMS',
          'IBM Sterling OMS & Manhattan Active Omni', 'Dematic / Knapp / Swisslog WCS (AS/RS & AMRs)', 'CubiScan 3D Laser Dimensioners',
          'FourKites & Project44 Yard Telemetry', 'Zebra RF Scanners & Impinj RFID Gates', 'EDI 940 / 943 / 944 / 945 / 856'
        ],
        logistics_fleet: [
          'SAP S/4HANA TM (Transportation Mgmt)', 'Blue Yonder TMS', 'Oracle Transportation Management (OTM)', 'CargoWise One & INTTRA Ocean',
          'IATA ONE Record / Cargo-XML e-AWB & Champ Cargospot', 'Spire Global / MarineTraffic Satellite AIS', 'FlightAware ADS-B Aircraft Telemetry',
          'Railinc EDI 404 / 417 & Class-I Rail (BNSF/UP/CSX/NS)', 'Project44 & FourKites Multi-Modal Visibility', 'Samsara ELD & Sensitech Cold-Chain IoT'
        ],
        trade_mkt_dist: [
          'DMS (Distributor Management Systems)', 'Field SFA Mobile Handhelds (Sales Force Automation)',
          'Google Maps Platform Routes & Fleet Engine', 'Modern Trade Key Account Portals (Walmart/Target/Reliance)',
          'Quick-Commerce Portals (Blinkit/Zepto/Instacart)', 'SAP S/4HANA SD / Billing (VF01/VF04)',
          'Circana / NielsenIQ Retail Scanner Feeds', 'Secondary Sales EDI 852 & GST Tax Ledgers'
        ],
        inventory_meio: [
          'SAP S/4HANA MM/SD & aATP', 'Blue Yonder Multi-Echelon Inventory Optimization (MEIO)',
          'BigQuery Multi-Tier Inventory Twin', 'Cloud Spanner Real-Time ATP Ledger',
          'Google OR-Tools Stochastic Inventory Balancer', 'Google Maps Distance Matrix API',
          'EDI 846 (Inventory Inquiry/Advice) & EDI 861', 'AlloyDB Sub-50ms Buffer State'
        ],
        warehousing_qa: [
          'Manhattan Active WMS & YMS', 'SAP EWM (Extended Warehouse Management)',
          'Dematic / Knapp / Swisslog WCS (AS/RS & AMRs)', 'CubiScan 3D Laser Dimensioners',
          'FourKites & Project44 Yard Telemetry', 'Zebra Handheld RF Scanners & Impinj RFID Gates',
          'ICML Quality Inspection SOP Manuals', 'EDI 940 / 943 / 944 / 945 / 856'
        ],
        circular_enable: [
          'SAP S/4HANA SD, QM, EHS & CO-PA', 'Loop Returns & Narvar RMA Portals', 'Walmart Luminate / Target / Kroger OTIF Portals',
          'Blue Yonder TMS & Manhattan WMS', 'ISO-14083 / GLEC Framework Carbon Engine', 'EU CBAM & EUDR Customs XML Portals',
          'Watershed / Persefoni / SAP Sustainability Footprint', 'Project44 & Samsara Geofence Telemetry', 'EDI 180 (RMA) / 210 / 214 / 812'
        ]
      };

      const isHighCodeSolver = /OR-Tools|MILP|CP-SAT|3D|LIFO|ULD|CVRPTW|Finite|Kalman|Isolation|Vision|Spanner/i.test(ag.solverStack || '');
      const buildType = ag.buildType || (isHighCodeSolver
        ? 'High-Code ADK + OR-Tools + Spanner/BigQuery'
        : 'Gemini Enterprise + Vertex AI + BigQuery');

      // Find all personas that use this agent
      let usedByPersonas = [];
      if (ag.isUniversal) {
        usedByPersonas = Object.values(DEPARTMENTS).map(d => PERSONAS[d.personaIds[0]]).filter(Boolean);
      } else {
        const direct = Object.values(PERSONAS).filter(p => (p.agentIds || []).includes(ag.id));
        const sameDept = (dept && dept.personaIds) ? dept.personaIds.map(pid => PERSONAS[pid]).filter(Boolean) : [];
        const seen = new Set();
        [...direct, ...sameDept].forEach(p => {
          if (p && !seen.has(p.id)) {
            seen.add(p.id);
            usedByPersonas.push(p);
          }
        });
      }

      const primaryPersona = usedByPersonas[0];
      const savingsByDept = {
        demand_sop: { val: '$14M+ Saved', label: 'Annual Inventory & Margin Impact', sub: 'Cuts excess buffer stock & prevents lost sales (secondary: -6.4% WAPE)' },
        sourcing_procurement: { val: '-6.8% ($18M+)', label: 'Direct Spend & Risk Savings', sub: 'Parametric should-cost negotiation & avoided line-down stops' },
        sourcing_risk: { val: '-6.8% ($18M+)', label: 'Direct Spend & Risk Savings', sub: 'Parametric should-cost negotiation & avoided line-down stops' },
        manufacturing_prod: { val: '$12M+ / Plant', label: 'Avoided Downtime & Scrap Savings', sub: 'Prevents unplanned machine halts, overtime & emergency spares' },
        inventory_meio: { val: '-18% ($28M+)', label: 'Working Capital Cash Released', sub: 'Frees trapped safety stock while holding 99.4% customer fill rate' },
        warehousing_qa: { val: '-28% Travel', label: 'Dock & Pick Labor Productivity', sub: 'Cuts picker walking by 28% and speeds dock-to-stock from 14h to <2.5h' },
        inventory_warehouse: { val: '-18% ($28M+)', label: 'Working Capital Cash Released', sub: 'Frees trapped safety stock while holding 99.4% customer fill rate' },
        logistics_fleet: { val: '-22.4% ($28M+)', label: 'Annual Multi-Modal Freight Saved', sub: 'Optimizes ocean, air, rail & truck cube, routes & demurrage' },
        trade_mkt_dist: { val: '+18% Fill Rate', label: 'Secondary Case Fill & Coverage', sub: 'Reconciles FSO beats with live distributor stock & cuts stockouts' },
        reverse_risk_esg: { val: '-78% ($9M+)', label: 'OTIF Fines & Logistics Cost Saved', sub: 'Prevents retailer chargebacks & recovers +31% return margin' },
        circular_enable: { val: '-78% ($9M+)', label: 'OTIF Fines & Logistics Cost Saved', sub: 'Prevents retailer chargebacks & recovers +31% return margin' },
        universal_csco: { val: '+$42M Cash', label: 'Enterprise Free Cash Flow Impact', sub: 'Synchronizes inventory, freight & payment terms across all verticals' }
      };
      const deptSaving = savingsByDept[ag.deptId] || savingsByDept.universal_csco;
      const roiMetrics = ag.roiMetrics || [
        {
          val: ag.badge || '+24% Lift',
          label: 'Quantifiable KPI Improvement',
          sub: `Verified across ${dept.name} workflows`,
          color: dept.color
        },
        {
          val: primaryPersona ? `${primaryPersona.toilHoursBefore.split(' ')[0]} → ${primaryPersona.toilHoursAfter.split(' ')[0]}h` : '-85% Effort',
          label: 'Daily Team Effort & Time Saved',
          sub: primaryPersona ? `${primaryPersona.name} daily manual toil cut by ~85%` : 'Automated exception triage & ERP write-back',
          color: '#10b981'
        },
        {
          val: deptSaving.val,
          label: deptSaving.label,
          sub: deptSaving.sub,
          color: '#38bdf8'
        },
        {
          val: 'Days → 90s',
          label: 'Decision & Execution Speed',
          sub: 'Replaces multi-day spreadsheet handoffs with 1-click ERP action',
          color: '#f59e0b'
        }
      ];

      const rawSeg = ag.dataSegments || defaultDataByDept[ag.deptId] || defaultDataByDept.universal_csco;
      const baseConnectors = connectorsByDept[ag.deptId] || connectorsByDept.universal_csco;
      const mergedConnectors = [...new Set([...toSysArray(ag.systems), ...baseConnectors])];

      return {
        roiMetrics,
        customerProof: ag.customerProof || defaultProofByDept[ag.deptId] || defaultProofByDept.universal_csco,
        buildType,
        gcpStack,
        enterpriseConnectors: mergedConnectors,
        dataSegments: {
          privateData: rawSeg.privateData || rawSeg.private || '',
          communityData: rawSeg.communityData || rawSeg.community || '',
          publicData: rawSeg.publicData || rawSeg.public || ''
        },
        usedByPersonas
      };
    }

    /* =========================================================================
       PAGE 2 RENDERING: DEDICATED PERSONA PAGE (26 PERSONAS)
       ========================================================================= */
    function openPersonaPage(personaId, pushHash = true, ev = null) {
      const p = PERSONAS[personaId];
      if (!p) return;
      const useSlide = isPillOrNavSwitch(ev);
      const sRect = useSlide ? null : getClickedCardRect(ev);
      const transClass = getPageTransitionClass(ev, sRect);

      lastPersonaId = personaId;
      selectedDeptId = p.deptId;
      const dept = getDeptMeta(p.deptId);
      const linkedVcId = PERSONA_VALUE_CHAIN_MAP[p.id];
      const linkedVc = linkedVcId ? VALUE_CHAINS[linkedVcId] : null;

      if (pushHash) {
        history.pushState({ page: 'persona', id: personaId }, '', `#persona/${personaId}`);
      }

      const container = document.getElementById('personaPageContent');
      container.innerHTML = `
        <div id="personaGenieWrap" class="${transClass}">
          <!-- Top Back & Switcher Bar -->
          <div class="back-bar">
            <div style="display:flex; gap:10px; flex-wrap:wrap;">
              <button type="button" class="back-btn" onclick="goToOrgChart()">
                <span>&larr;</span>
                <span>CSCO Org Chart (${dept.name})</span>
              </button>
              <button type="button" class="back-btn" onclick="openPersonasDirectoryPage('${dept.id}', '', true, 'personas', event)">
                <span>👥</span>
                <span>All 26 Personas &amp; 32 Agents</span>
              </button>
            </div>

            <div class="persona-switcher-pills">
              ${dept.personaIds.map(pid => {
                const other = PERSONAS[pid];
                return `
                  <button type="button"
                          class="switch-pill ${pid === p.id ? 'active' : ''}"
                          style="${pid === p.id ? `background:${dept.color}; border-color:${dept.color}; color:#040810; font-weight:700;` : ''}"
                          onclick="openPersonaPage('${pid}', true, event)">
                    ${other.icon} ${other.name}
                  </button>
                `;
              }).join('')}
            </div>
          </div>

          <!-- Persona Overview Header -->
          <div class="persona-header-card" style="border-color: ${dept.color}44;">
            ${renderSupplyChainWatermarkSvg(dept.watermarkType, dept.color, 'persona-header-sc-watermark')}

            <div style="position:relative; z-index:2;">
              <div class="persona-badge" style="background: ${dept.color}22; color: ${dept.color}; border: 1px solid ${dept.color}55;">
                <span>${p.icon}</span>
                <span>${dept.scorBadge || ''} · ${dept.fullName} · ${p.role}</span>
              </div>
              <h1 class="persona-page-title">${p.name}</h1>
              <p class="persona-page-summary">${formatRichText(p.summary)}</p>
              <div class="persona-focus-pills">
                ${p.focusAreas.map(f => `<span class="focus-pill">${f}</span>`).join('')}
              </div>
            </div>

            <div class="persona-stat-highlight" style="border-color: ${dept.color}44;">
              <div class="persona-stat-value" style="color: ${dept.color};">${p.headlineStat}</div>
              <div class="persona-stat-label">${p.headlineLabel}</div>
            </div>
          </div>

          ${linkedVc ? `
            <div class="persona-vc-banner" onclick="openValueChainPage('${linkedVc.id}', true, event)">
              <div style="display:flex; align-items:center; gap:14px;">
                <span class="vc-flow-badge" style="margin-bottom:0; background:${linkedVc.color}22; color:${linkedVc.color}; border:1px solid ${linkedVc.color}55;">
                  End-to-End Value Chain
                </span>
                <div>
                  <div style="font-family:var(--font-display); font-size:18px; font-weight:800;">${linkedVc.title}</div>
                  <div style="font-size:15px; color:var(--text-secondary);">${formatRichText(linkedVc.cardSubtitle)}</div>
                </div>
              </div>
              <span style="font-size:14px; font-weight:700; color:${linkedVc.color}; white-space:nowrap;">
                Open 6-Stage Pipeline &rarr;
              </span>
            </div>
          ` : ''}

          <!-- Realistic Day in the Life Header + Legend -->
          <div class="ditl-header-row">
            <div>
              <h2 class="block-title">A Realistic Day in the Life</h2>
              <p class="block-subtitle">Full daily schedule—highlighting where <span class="sc-hl-underline">process gaps</span> happen and how <span class="sc-hl-underline">Gemini Enterprise</span> transforms them.</p>
            </div>

            <div class="ditl-legend">
              <span class="legend-item">
                <span class="legend-swatch" style="background: rgba(255,255,255,0.25);"></span>
                <span>Core Strategic / Human Work</span>
              </span>
              <span class="legend-item">
                <span class="legend-swatch" style="background: var(--g-red);"></span>
                <span style="color: #ff8a80;">Manual Toil Bottleneck</span>
              </span>
              <span class="legend-item">
                <span class="legend-swatch" style="background: var(--g-green);"></span>
                <span style="color: #81c995;">Gemini Enterprise Improvement</span>
              </span>
            </div>
          </div>

          <!-- Before vs After Daily Capacity Meter -->
          <div class="time-shift-banner">
            <div class="shift-meter-card">
              <div class="shift-meter-top">
                <span style="color: var(--text-secondary);">Traditional Workday</span>
                <span style="color: #ff8a80; font-weight: 700;">${p.toilHoursBefore}</span>
              </div>
              <div class="shift-bar-track">
                <div style="width: 74%; background: var(--g-red);"></div>
                <div style="width: 26%; background: rgba(255,255,255,0.18);"></div>
              </div>
            </div>

            <div class="shift-meter-card">
              <div class="shift-meter-top">
                <span style="color: var(--text-secondary);">With Gemini Enterprise</span>
                <span style="color: #81c995; font-weight: 700;">${p.toilHoursAfter}</span>
              </div>
              <div class="shift-bar-track">
                <div style="width: 14%; background: var(--g-green);"></div>
                <div style="width: 86%; background: var(--g-blue);"></div>
              </div>
            </div>
          </div>

          <!-- Full Chronological Schedule -->
          <div class="day-schedule">
            ${p.dayInLife.map((slot, idx) => {
              if (!slot.isToil) {
                return `
                  <div class="schedule-row-human">
                    <div class="slot-time-col">
                      <div class="slot-clock">${slot.time}</div>
                      <div class="slot-title">${slot.task}</div>
                    </div>
                    <div class="human-task-box">
                      <span class="human-task-desc">${formatRichText(slot.activity)}</span>
                      <span class="human-pill">👤 ${slot.tag}</span>
                    </div>
                  </div>
                `;
              }

              const plugAgent = slot.agentId ? AGENTS[slot.agentId] : null;
              return `
                <div class="schedule-row-toil">
                  <div class="slot-time-col">
                    <div class="slot-clock">${slot.time}</div>
                    <div class="slot-title" style="color: #ff8a80;">${slot.task}</div>
                  </div>

                  <div class="toil-highlight-box">
                    <div class="toil-top-bar">
                      <span class="toil-badge">✕ Manual Toil</span>
                      <span class="toil-duration">${slot.toilTime}</span>
                    </div>
                    <div class="toil-text">${formatRichBullets(slot.before, '#f87171')}</div>
                  </div>

                  <div class="gemini-improve-box">
                    <div class="improve-top-bar">
                      <span class="improve-badge">
                        <img data-asset="sparkle_blue_violet.png" alt="" />
                        <span>Gemini Improvement</span>
                      </span>
                      <span class="improve-time-saved">${slot.toilTime} &rarr; ${slot.afterTime}</span>
                    </div>
                    <div class="improve-text">${formatRichBullets(slot.after, '#34d399')}</div>
                    ${plugAgent ? `
                      <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-top:8px;">
                        <button type="button" class="plugin-agent-btn" onclick="openAgentPage('${plugAgent.id}', true, event)">
                          <span>🔌 Plug-in Agent: ${plugAgent.name} (${plugAgent.badge})</span>
                          <span>&rarr;</span>
                        </button>
                        <button type="button" class="switch-pill" style="font-size:12.5px; padding:7px 14px;" onclick="openAgentBlueprintPage('${plugAgent.id}', true, event)">
                          <span>🏗️ High-Code Blueprint</span>
                        </button>
                      </div>
                    ` : ''}
                  </div>
                </div>
              `;
            }).join('')}
          </div>

          <!-- Domain-Specific Agent Catalogue + 4 Cross-Persona Universal Agents -->
          <h2 class="block-title">Agent Catalogue for ${p.name}</h2>
          <p class="block-subtitle">
            Every supply chain persona is powered by their <strong>Dedicated Domain Agent(s)</strong> plus the <span class="sc-hl-underline">4 Cross-Persona Universal Control Tower Agents</span> shared across all <span class="sc-hl-metric">26 roles</span>.
          </p>

          <div class="catalog-grid">
            ${[...new Set([...(p.agentIds || []), ...UNIVERSAL_AGENT_IDS])].map(aid => {
              const ag = AGENTS[aid];
              if (!ag) return '';
              const agDept = getDeptMeta(ag.deptId);
              return `
                <div class="catalog-card" onclick="openAgentPage('${ag.id}', true, event)" style="border-color:${ag.isUniversal ? 'rgba(56,189,248,0.35)' : `${dept.color}44`};">
                  <div class="catalog-thumb">
                    ${renderMiniCatalogCadSvg(ag.cadType, agDept.color)}
                    <div class="play-circle">
                      <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M8 5v14l11-7z"/>
                      </svg>
                    </div>
                  </div>

                  <div class="catalog-body">
                    <div>
                      <div style="display:inline-flex; align-items:center; gap:6px; font-size:11.5px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:${agDept.color}; margin-bottom:6px;">
                        <span>${ag.isUniversal ? '🌐 Cross-Persona Universal Agent (All 26 Roles)' : `🔌 Dedicated ${dept.name} Agent`}</span>
                      </div>
                      <div class="catalog-title">${ag.name}</div>
                      <div class="catalog-desc">${formatRichText(ag.shortDesc)}</div>
                      <div class="sc-tech-pills" style="margin-top:12px;">
                        ${toSysArray(ag.systems).slice(0, 4).map(s => `<span class="sc-tech-pill">${s}</span>`).join('')}
                      </div>
                    </div>
                    <div class="catalog-footer" style="margin-top:16px;">
                      <span style="color: ${agDept.color};">${ag.badge}</span>
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
       AGENT ARCHITECTURE BLUEPRINT HELPER (PER-AGENT SVG + A2A SUB-AGENTS)
       ========================================================================= */
    function renderAgentArchitectureBlueprint(ag, dept) {
      const sysArr = toSysArray(ag.systems);
      const truncSvg = (str, max = 23) => {
        const s = String(str || '').trim();
        return s.length > max ? s.slice(0, max - 1) + '…' : s;
      };
      const subs = ag.subAgents || [
        { name: 'Telemetry Ingestion Agent', role: 'Normalizes ERP/WMS/TMS and IoT feeds in real time.' },
        { name: 'OR-Tools Physics Solver Agent', role: 'Runs deterministic MILP / VRP / LIFO optimization constraints.' },
        { name: 'Execution Write-Back Agent', role: 'Prepares A2UI payloads and dispatches signed ERP/WMS/TMS transactions.' }
      ];

      return `
        <div class="agent-arch-box" style="border-color:${dept.color}44; margin-top:0;">
          <div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:12px; margin-bottom:16px;">
            <div>
              <div style="font-size:12.5px; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; color:${dept.color}; margin-bottom:4px;">
                ✦ 5-Stage Multi-Agent A2A System Topology · Vertex AI Agent Engine
              </div>
              <h3 style="font-family:var(--font-display); font-size:23px; font-weight:800; color:#f8fafc;">
                ${ag.name} — End-to-End Agentic Execution Flow
              </h3>
            </div>
            <button type="button" class="switch-pill" onclick="openArchitecturePage(true, event)">
              🏗️ View Full 32-Agent Enterprise Topology &rarr;
            </button>
          </div>

          <!-- 5-Stage Visual SVG Architecture Diagram (Enlarged Typography & Box Heights) -->
          <div style="border-radius:16px; overflow:hidden; border:1px solid rgba(148,163,184,0.25); background:#040812; margin-bottom:20px;">
            <svg viewBox="0 0 1060 264" style="width:100%; height:auto; display:block;">
              <defs>
                <linearGradient id="archFlowGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="${dept.color}" stop-opacity="0.9" />
                  <stop offset="50%" stop-color="#00d2ff" stop-opacity="0.9" />
                  <stop offset="100%" stop-color="#10b981" stop-opacity="0.9" />
                </linearGradient>
                <clipPath id="bpClip1"><rect x="16" y="30" width="184" height="202" rx="14" /></clipPath>
                <clipPath id="bpClip2"><rect x="228" y="30" width="180" height="202" rx="14" /></clipPath>
                <clipPath id="bpClip3"><rect x="436" y="20" width="188" height="222" rx="16" /></clipPath>
                <clipPath id="bpClip4"><rect x="652" y="30" width="180" height="202" rx="14" /></clipPath>
                <clipPath id="bpClip5"><rect x="860" y="30" width="184" height="202" rx="14" /></clipPath>
              </defs>

              <!-- Animated Connector Pipes & Glowing Telemetry Packets -->
              <line x1="200" y1="131" x2="228" y2="131" stroke="url(#archFlowGrad)" stroke-width="3.2" class="sc-arc-flow" />
              <line x1="408" y1="131" x2="436" y2="131" stroke="url(#archFlowGrad)" stroke-width="3.2" class="sc-arc-flow" />
              <line x1="624" y1="131" x2="652" y2="131" stroke="url(#archFlowGrad)" stroke-width="3.2" class="sc-arc-flow" />
              <line x1="832" y1="131" x2="860" y2="131" stroke="url(#archFlowGrad)" stroke-width="3.2" class="sc-arc-flow" />

              <circle cy="131" r="4" fill="${dept.color}"><animate attributeName="cx" from="200" to="228" dur="1.2s" repeatCount="indefinite" /></circle>
              <circle cy="131" r="4" fill="#00d2ff"><animate attributeName="cx" from="408" to="436" dur="1.2s" repeatCount="indefinite" /></circle>
              <circle cy="131" r="4" fill="#c084fc"><animate attributeName="cx" from="624" to="652" dur="1.2s" repeatCount="indefinite" /></circle>
              <circle cy="131" r="4" fill="#10b981"><animate attributeName="cx" from="832" to="860" dur="1.2s" repeatCount="indefinite" /></circle>

              <!-- Stage 1: Systems of Record & Telemetry -->
              <rect x="16" y="30" width="184" height="202" rx="14" fill="rgba(15,23,42,0.95)" stroke="${dept.color}" stroke-width="2" />
              <g clip-path="url(#bpClip1)">
                <text x="30" y="58" fill="${dept.color}" font-size="11.5" font-weight="700">01 · INGEST &amp; SENSING</text>
                <text x="30" y="84" fill="#ffffff" font-size="14.5" font-weight="700">Enterprise Feeds</text>
                <text x="30" y="114" fill="#e2e8f0" font-size="12">• ${truncSvg(sysArr[0] || 'SAP S/4HANA & IBP', 21)}</text>
                <text x="30" y="138" fill="#e2e8f0" font-size="12">• ${truncSvg(sysArr[1] || 'WMS / TMS Streams', 21)}</text>
                <text x="30" y="162" fill="#e2e8f0" font-size="12">• ${truncSvg(sysArr[2] || 'AIS / ADS-B / EDI', 21)}</text>
                <text x="30" y="204" fill="#38bdf8" font-size="11.5" font-weight="700" font-family="monospace">Pub/Sub + Apigee</text>
              </g>

              <!-- Stage 2: BigQuery & Cloud Spanner Digital Twin -->
              <rect x="228" y="30" width="180" height="202" rx="14" fill="rgba(15,23,42,0.95)" stroke="#00d2ff" stroke-width="2" />
              <g clip-path="url(#bpClip2)">
                <text x="242" y="58" fill="#00d2ff" font-size="11.5" font-weight="700">02 · DIGITAL TWIN</text>
                <text x="242" y="84" fill="#ffffff" font-size="14.5" font-weight="700">BigQuery &amp; Spanner</text>
                <text x="242" y="114" fill="#e2e8f0" font-size="12">• BigQuery Twin &amp; GIS</text>
                <text x="242" y="138" fill="#e2e8f0" font-size="12">• Spanner Graph BOM</text>
                <text x="242" y="162" fill="#e2e8f0" font-size="12">• AlloyDB pgvector</text>
                <text x="242" y="204" fill="#00d2ff" font-size="11.5" font-weight="700" font-family="monospace">BQ · Spanner · AlloyDB</text>
              </g>

              <!-- Stage 3: Gemini 3.1 Pro / 3.8 Flash Orchestrator + A2A Coordinator -->
              <rect x="436" y="20" width="188" height="222" rx="16" fill="rgba(20,30,55,0.98)" stroke="#a855f7" stroke-width="2.4" />
              <g clip-path="url(#bpClip3)">
                <text x="450" y="50" fill="#c084fc" font-size="11.5" font-weight="700">03 · ADK ORCHESTRATOR</text>
                <text x="450" y="76" fill="#ffffff" font-size="14.5" font-weight="700">Gemini 3.1 Pro / 3.8 Flash</text>
                <text x="450" y="106" fill="#f1f5f9" font-size="12">• Root Supervisor Agent</text>
                <text x="450" y="130" fill="#f1f5f9" font-size="12">• 3 A2A Sub-Agents</text>
                <text x="450" y="154" fill="#f1f5f9" font-size="12">• TimesFM &amp; WeatherNext</text>
                <text x="450" y="178" fill="#f1f5f9" font-size="12">• Document AI &amp; Maps</text>
                <text x="450" y="214" fill="#c084fc" font-size="11.5" font-weight="700" font-family="monospace">Vertex Agent Engine</text>
              </g>

              <!-- Stage 4: Deterministic Physics & OR-Tools Solver -->
              <rect x="652" y="30" width="180" height="202" rx="14" fill="rgba(15,23,42,0.95)" stroke="#f59e0b" stroke-width="2" />
              <g clip-path="url(#bpClip4)">
                <text x="666" y="58" fill="#fbbf24" font-size="11.5" font-weight="700">04 · MATH SOLVER</text>
                <text x="666" y="84" fill="#ffffff" font-size="14.5" font-weight="700">OR-Tools &amp; Maps</text>
                <text x="666" y="114" fill="#e2e8f0" font-size="12">• OR-Tools CP-SAT/MILP</text>
                <text x="666" y="138" fill="#e2e8f0" font-size="12">• 3D LIFO / ULD / VRP</text>
                <text x="666" y="162" fill="#e2e8f0" font-size="12">• Maps Routes API</text>
                <text x="666" y="204" fill="#fbbf24" font-size="11.5" font-weight="700" font-family="monospace">100% Deterministic</text>
              </g>

              <!-- Stage 5: A2UI Control Tower & ERP Write-Back -->
              <rect x="860" y="30" width="184" height="202" rx="14" fill="rgba(15,23,42,0.95)" stroke="#10b981" stroke-width="2" />
              <g clip-path="url(#bpClip5)">
                <text x="874" y="58" fill="#34d399" font-size="11.5" font-weight="700">05 · ACTION &amp; ROI</text>
                <text x="874" y="84" fill="#ffffff" font-size="14.5" font-weight="700">A2UI + Write-Back</text>
                <text x="874" y="114" fill="#e2e8f0" font-size="12">• 3D CAD Studio</text>
                <text x="874" y="138" fill="#e2e8f0" font-size="12">• Looker &amp; 1-Click Sign</text>
                <text x="874" y="162" fill="#e2e8f0" font-size="12">• Signed SAP/EDI Call</text>
                <text x="874" y="204" fill="#34d399" font-size="11.5" font-weight="700" font-family="monospace">${truncSvg(ag.badge, 19)}</text>
              </g>
            </svg>
          </div>

          <!-- 3 Collaborating A2A Sub-Agents Grid -->
          <div style="font-size:13px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:var(--text-secondary); margin-bottom:6px;">
            Collaborating A2A Sub-Agents Orchestrated by ${ag.name}
          </div>
          <div class="subagent-grid">
            ${subs.map((sub, i) => `
              <div class="subagent-card">
                <div class="subagent-tag" style="color:${dept.color};">SUB-AGENT 0${i + 1} · A2A PROTOCOL</div>
                <div class="subagent-name">${sub.name}</div>
                <div class="subagent-role">${formatRichText(sub.role)}</div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    function renderGcpAndEnterpriseConnectorsPanel(ag, dept, sell) {
      return `
        <div class="used-by-strip" style="margin-bottom:28px; border-color:${dept.color}44;">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
            <div>
              <div style="font-size:12.5px; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; color:#38bdf8;">
                ☁️ Full Google Cloud Service Stack (12 Services) &amp; Pre-Built Enterprise System Connectors
              </div>
              <div style="font-family:var(--font-display); font-size:21px; font-weight:800; color:#f8fafc; margin-top:4px;">
                Google Cloud AI, Database, Maps &amp; Solver Architecture Powering ${ag.name}
              </div>
            </div>
            <span class="sc-tech-pill" style="border-color:#10b98166; color:#34d399; font-weight:700; font-size:13px; padding:6px 14px;">
              BigQuery · Cloud Spanner · AlloyDB · Google Maps · OR-Tools · SAP/WMS/TMS
            </span>
          </div>

          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(265px, 1fr)); gap:12px; margin-bottom:20px;">
            ${sell.gcpStack.map(svc => `
              <div style="background:rgba(4,9,18,0.85); border:1px solid rgba(56,189,248,0.28); border-radius:12px; padding:14px 16px;">
                <div style="font-size:15px; font-weight:800; color:#38bdf8; margin-bottom:5px;">☁️ ${svc.name}</div>
                <div style="font-size:14px; color:#cbd5e1; line-height:1.58;">${formatRichText(svc.role)}</div>
              </div>
            `).join('')}
          </div>

          <div style="font-size:12.5px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:10px;">
            🔌 Pre-Built Enterprise Application, ERP/WMS/TMS &amp; Multi-Modal Telemetry Connectors (Apigee + Integration Connectors):
          </div>
          <div class="sc-tech-pills">
            ${sell.enterpriseConnectors.map(c => `<span class="sc-tech-pill" style="border-color:${dept.color}44; color:#f8fafc;">${c}</span>`).join('')}
          </div>
        </div>
      `;
    }

    /* =========================================================================
       PAGE 3 RENDERING: EXECUTIVE SELLING AGENT PAGE (#agent/<id>)
       ========================================================================= */
    function openAgentPage(agentId, pushHash = true, ev = null) {
      const ag = AGENTS[agentId];
      if (!ag) return;
      const useSlide = isPillOrNavSwitch(ev);
      const sRect = useSlide ? null : getClickedCardRect(ev);
      const transClass = getPageTransitionClass(ev, sRect);

      const dept = getDeptMeta(ag.deptId);
      const sell = getAgentSellingMeta(ag, dept);
      const backPersona = PERSONAS[lastPersonaId] || Object.values(PERSONAS)[0];
      const videoUrl = customVideos[ag.id] || ag.videoSrc;
      const showVideoPlayer = ag.hasPreloadedVideo || Boolean(customVideos[ag.id]);

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
              <button type="button" class="back-btn" onclick="openPersonasDirectoryPage('${ag.isUniversal ? 'universal' : dept.id}', '', true, 'agents', event)">
                <span>🤖</span>
                <span>All 32 Supply Chain Agents</span>
              </button>
            </div>

            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              <button type="button" class="switch-pill" style="border-color:#c084fc88; color:#e9d5ff; font-weight:700;" onclick="openAgentBlueprintPage('${ag.id}', true, event)">
                🏗️ Open High-Code Architecture &amp; Sub-Agent Page &rarr;
              </button>
              <button type="button" class="switch-pill" onclick="goToOrgChart()">
                CSCO Org Chart
              </button>
            </div>
          </div>

          <!-- Executive Hero Banner -->
          <div class="agent-hero-banner" style="border-color: ${dept.color}44;">
            ${renderSupplyChainWatermarkSvg(dept.watermarkType, dept.color, 'persona-header-sc-watermark')}

            <div style="position:relative; z-index:2; display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin-bottom:14px;">
              <div class="persona-badge" style="margin-bottom:0; background: ${dept.color}22; color: ${dept.color}; border: 1px solid ${dept.color}55;">
                <img data-asset="sparkle_blue_violet.png" alt="" style="width:14px; height:14px;" />
                <span>${ag.isUniversal ? '🌐 Cross-Persona Universal Agent · All 26 Roles' : `${dept.scorBadge} · ${dept.fullName}`}</span>
              </div>
              <span class="sc-tech-pill" style="border-color:#38bdf866; color:#38bdf8; font-weight:700; padding:6px 14px;">
                ⚡ ${sell.buildType}
              </span>
            </div>

            <h1 class="agent-title">${ag.name}</h1>
            <p class="agent-subtitle">${formatRichText(ag.shortDesc)}</p>

            <div class="sc-tech-pills" style="position:relative; z-index:2; margin-top:16px;">
              ${toSysArray(ag.systems).map(s => `<span class="sc-tech-pill">${s}</span>`).join('')}
            </div>
          </div>

          <!-- 4 Big Executive ROI, Growth & Cost-Saving Stat Cards -->
          <div class="agent-roi-grid">
            ${sell.roiMetrics.map(m => `
              <div class="agent-roi-card" style="--roi-accent: ${m.color || dept.color};">
                <div class="agent-roi-val" style="color: ${m.color || dept.color};">${m.val}</div>
                <div class="agent-roi-label">${m.label}</div>
                <div class="agent-roi-sub">${m.sub}</div>
              </div>
            `).join('')}
          </div>

          <!-- 3 HERO-SIZED EXECUTIVE SELLING PITCH CARDS (BIG, PROMINENT & IMPOSSIBLE TO MISS) -->
          <div class="exec-pitch-grid">
            <div class="exec-pitch-card" style="--pitch-accent: #f87171;">
              <div class="exec-pitch-eyebrow" style="color: #fca5a5; background: rgba(239, 68, 68, 0.14); border: 1px solid rgba(239, 68, 68, 0.4);">
                <span>✕ 01 · The Business Problem</span>
              </div>
              <h2 class="exec-pitch-title">The Process Gap &amp; Manual Cost Leakage</h2>
              <div class="exec-pitch-body">${formatRichBullets(ag.problem, '#f87171')}</div>
            </div>

            <div class="exec-pitch-card" style="--pitch-accent: #38bdf8;">
              <div class="exec-pitch-eyebrow" style="color: #7dd3fc; background: rgba(56, 189, 248, 0.14); border: 1px solid rgba(56, 189, 248, 0.4);">
                <span>⚡ 02 · The Executive Solution</span>
              </div>
              <h2 class="exec-pitch-title">How ${ag.name} Solves It Autonomously</h2>
              <div class="exec-pitch-body">${formatRichBullets(ag.solution, '#38bdf8')}</div>
            </div>

            <div class="exec-pitch-card" style="--pitch-accent: #34d399;">
              <div class="exec-pitch-eyebrow" style="color: #6ee7b7; background: rgba(16, 185, 129, 0.14); border: 1px solid rgba(16, 185, 129, 0.4);">
                <span>✦ 03 · Bottom-Line Outcome (${ag.badge})</span>
              </div>
              <h2 class="exec-pitch-title">Verified Financial &amp; Operational Impact</h2>
              <div class="exec-pitch-body">${formatRichBullets(ag.advantage, '#34d399')}</div>
              <div class="exec-pitch-proof">
                <strong>Verified Customer Proof Point:</strong> ${formatRichText(sell.customerProof)}
              </div>
            </div>
          </div>

          <!-- Interactive CAD Simulation Studio + Preloaded .mp4 Demo Video Stage -->
          <div class="video-stage-box">
            <div class="video-viewport" id="agentVideoViewport">
              ${renderStageViewportHtml(ag, 'agent', videoUrl, showVideoPlayer)}
            </div>

            <div class="video-toolbar">
              <span>${stageViewMode === 'cad' ? `Interactive Vector CAD Studio: ${ag.name}` : `Executive Demo Video (.mp4): ${ag.name}`}</span>
              <div style="display:flex; flex-wrap:wrap; gap:8px;">
                <button type="button" class="upload-video-btn ${stageViewMode==='cad'?'active':''}"
                        onclick="stageViewMode='cad';openAgentPage('${ag.id}', false)">
                  <span>✦ Interactive CAD Simulator</span>
                </button>
                <button type="button" class="upload-video-btn ${stageViewMode==='video'?'active':''}"
                        onclick="stageViewMode='video';openAgentPage('${ag.id}', false)">
                  <span>▶ Watch Demo Video (.mp4)</span>
                </button>
                <label class="upload-video-btn" title="Drop in any custom .mp4 screen recording for this agent">
                  <span>Swap Local .mp4</span>
                  <input type="file" accept="video/*" style="display:none;" onchange="attachAgentVideo(event, '${ag.id}')" />
                </label>
              </div>
            </div>
          </div>

          <!-- Full Google Cloud Service Stack (12 Services) & Pre-Built Enterprise Connectors -->
          ${renderGcpAndEnterpriseConnectorsPanel(ag, dept, sell)}

          <!-- Prominent CTA Banner to Dedicated High-Code Technical Architecture Page (#blueprint/<id>) -->
          <div class="blueprint-cta-banner" style="margin-bottom:28px;">
            <div style="max-width:980px;">
              <div style="font-size:12.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.12em; color:#c084fc; margin-bottom:6px;">
                🏗️ Deep Technical &amp; High-Code Engineering Specification (Dedicated Sub-Page)
              </div>
              <div style="font-family:var(--font-display); font-size:23px; font-weight:800; color:#f8fafc; margin-bottom:8px;">
                Want to inspect the High-Code ADK Orchestrator, 3 A2A Sub-Agents, OR-Tools Math Solvers &amp; ERP Write-Back APIs?
              </div>
              <p style="font-size:16px; color:var(--text-secondary); line-height:1.68;">
                Click across to the dedicated <span class="sc-hl-underline">High-Code Architecture &amp; Sub-Agent Flow Page</span> for <strong class="sc-hl-bold">${ag.name}</strong> to review the 5-stage system diagram, 3-segment data foundation (Private / Community / Public), and signed BAPI/EDI payloads.
              </p>
            </div>
            <div style="display:flex; flex-direction:column; gap:10px; align-items:flex-end;">
              <button type="button"
                      class="cta-btn"
                      style="background:linear-gradient(135deg, #a855f7, #00d2ff); color:#040810; font-weight:700; border:none;"
                      onclick="openAgentBlueprintPage('${ag.id}', true, event)">
                <span>🏗️ Open High-Code Architecture &amp; Sub-Agent Page</span>
                <span>&rarr;</span>
              </button>
            </div>
          </div>

          <!-- Operational Adoption Across the CSCO Org Chart (Moved to Bottom of Agent Page) -->
          <div class="used-by-strip" style="margin-bottom:0;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
              <div>
                <div style="font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; color:${dept.color};">
                  👥 Operational Adoption Across the CSCO Org Chart
                </div>
                <div style="font-family:var(--font-display); font-size:19px; font-weight:800; color:#f8fafc; margin-top:2px;">
                  ${ag.isUniversal
                    ? 'Used Daily by All 26 Supply Chain Personas Across All 6 SCOR Verticals'
                    : `Used by Supply Chain Personas in ${dept.fullName}`}
                </div>
              </div>
              <button type="button" class="switch-pill" onclick="openPersonasDirectoryPage('${ag.isUniversal ? 'all' : dept.id}', '', true, 'personas', event)">
                Browse All 26 Personas &rarr;
              </button>
            </div>
            <div class="used-by-pills">
              ${sell.usedByPersonas.map(p => {
                const pDept = getDeptMeta(p.deptId);
                return `
                  <button type="button" class="used-by-pill" onclick="openPersonaPage('${p.id}', true, event)">
                    <span>${p.icon}</span>
                    <span>${p.name}</span>
                    <span style="font-size:12px; color:${pDept.color};">(${pDept.name}) &rarr;</span>
                  </button>
                `;
              }).join('')}
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
    }

    /* =========================================================================
       DEDICATED HIGH-CODE ARCHITECTURE & SUB-AGENT BLUEPRINT PAGE (#blueprint/<id>)
       ========================================================================= */
    function openAgentBlueprintPage(agentId, pushHash = true, ev = null) {
      const ag = AGENTS[agentId];
      if (!ag) return;
      const useSlide = isPillOrNavSwitch(ev);
      const sRect = useSlide ? null : getClickedCardRect(ev);
      const transClass = getPageTransitionClass(ev, sRect);

      const dept = getDeptMeta(ag.deptId);
      const sell = getAgentSellingMeta(ag, dept);
      const sysArr = toSysArray(ag.systems);

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
                <span>Back to ${ag.name} (Executive Selling Page)</span>
              </button>
              <button type="button" class="back-btn" onclick="openArchitecturePage(true, event)">
                <span>🏗️</span>
                <span>All 32 Agents Enterprise Architecture</span>
              </button>
            </div>

            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              <button type="button" class="switch-pill" onclick="openPersonasDirectoryPage('${ag.isUniversal ? 'universal' : dept.id}', '', true, 'agents', event)">
                🤖 Browse All 32 Agents
              </button>
              <button type="button" class="switch-pill" onclick="goToOrgChart()">
                CSCO Org Chart
              </button>
            </div>
          </div>

          <!-- Technical Blueprint Header Card -->
          <div class="persona-header-card" style="border-color: rgba(168, 85, 247, 0.45);">
            ${renderSupplyChainWatermarkSvg(dept.watermarkType, dept.color, 'persona-header-sc-watermark')}

            <div style="position:relative; z-index:2;">
              <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-bottom:12px;">
                <div class="persona-badge" style="margin-bottom:0; background: rgba(168,85,247,0.18); color: #e9d5ff; border: 1px solid rgba(168,85,247,0.5);">
                  <span>🏗️ High-Code Technical Architecture &amp; A2A Sub-Agent Spec</span>
                </div>
                <span class="sc-tech-pill" style="border-color:${dept.color}66; color:${dept.color}; font-weight:700;">
                  ${sell.buildType}
                </span>
              </div>
              <h1 class="persona-page-title">${ag.name} — Engineering Blueprint</h1>
              <p class="persona-page-summary">
                ${formatRichText('Complete multi-agent system topology, A2A sub-agent decomposition, Google Cloud 12-Service Stack (BigQuery, Cloud Spanner Graph, AlloyDB, Google Maps Platform, OR-Tools, Vertex AI ADK), and signed ERP/WMS/TMS write-back specification.')}
              </p>
            </div>

            <div class="persona-stat-highlight" style="border-color: ${dept.color}55;">
              <div class="persona-stat-value" style="color: ${dept.color};">${ag.badge}</div>
              <div class="persona-stat-label">3 Collaborating A2A Sub-Agents · 100% Deterministic Write-Back</div>
            </div>
          </div>

          <!-- 5-Stage Visual SVG Architecture Diagram + 3 Collaborating A2A Sub-Agents -->
          ${renderAgentArchitectureBlueprint(ag, dept)}

          <!-- Full Google Cloud Service Stack (12 Services) & Pre-Built Enterprise Connectors -->
          <div style="margin-top:28px;">
            ${renderGcpAndEnterpriseConnectorsPanel(ag, dept, sell)}
          </div>

          <!-- Section: Google Cloud 3-Segment Supply Chain Data Foundation (Private / Community / Public) -->
          <h2 class="block-title" style="margin-top:34px;">3-Segment Supply Chain Data Foundation</h2>
          <p class="block-subtitle">
            ${formatRichText('Aligned with Google Cloud’s Supply Chain Twin architecture—fusing Private ERP/WMS/MES records, Community Partner/EDI/AIS/ADS-B feeds, and Public WeatherNext 3 / Maps signals in BigQuery, Cloud Spanner & AlloyDB.')}
          </p>

          <div class="exec-pitch-grid" style="margin-bottom:34px;">
            <div class="exec-pitch-card" style="--pitch-accent: #00d2ff;">
              <div class="exec-pitch-eyebrow" style="color:#00d2ff; background:rgba(0,210,255,0.12); border:1px solid rgba(0,210,255,0.38);">
                <span>01 · Private Enterprise Data</span>
              </div>
              <h3 class="exec-pitch-title">Internal Systems of Record</h3>
              <div class="exec-pitch-body">${formatRichBullets(sell.dataSegments.privateData, '#00d2ff')}</div>
            </div>
            <div class="exec-pitch-card" style="--pitch-accent: #c084fc;">
              <div class="exec-pitch-eyebrow" style="color:#c084fc; background:rgba(168,85,247,0.14); border:1px solid rgba(168,85,247,0.4);">
                <span>02 · Community &amp; Partner Data</span>
              </div>
              <h3 class="exec-pitch-title">EDI, AIS, ADS-B &amp; Supplier Portals</h3>
              <div class="exec-pitch-body">${formatRichBullets(sell.dataSegments.communityData, '#c084fc')}</div>
            </div>
            <div class="exec-pitch-card" style="--pitch-accent: #34d399;">
              <div class="exec-pitch-eyebrow" style="color:#34d399; background:rgba(16,185,129,0.14); border:1px solid rgba(16,185,129,0.4);">
                <span>03 · Public &amp; Environmental Signals</span>
              </div>
              <h3 class="exec-pitch-title">WeatherNext 3, Maps &amp; Earth Engine</h3>
              <div class="exec-pitch-body">${formatRichBullets(sell.dataSegments.publicData, '#34d399')}</div>
            </div>
          </div>

          <!-- Section: High-Code Mathematical Solver Stack & Signed API Write-Back Spec -->
          <h2 class="block-title">Mathematical Solver Stack &amp; Deterministic ERP/WMS/TMS Write-Back</h2>
          <p class="block-subtitle">
            ${formatRichText('Why LLMs alone are never allowed to guess physical constraints—how Gemini 3.1 Pro & 3.8 Flash orchestrate 100% deterministic mathematical solvers before executing signed system transactions.')}
          </p>

          <div class="showcase-grid" style="grid-template-columns: repeat(auto-fit, minmax(420px, 1fr)); margin-bottom:32px;">
            <div class="showcase-panel" style="border-color:rgba(245,158,11,0.38);">
              <div class="panel-tag" style="color:#fbbf24;">🧮 Deterministic Mathematical &amp; AI Solver Stack</div>
              <div style="font-size:17px; color:#f8fafc; font-weight:500; line-height:1.68; margin-bottom:14px;">
                ${formatRichBullets(ag.solverStack || '', '#fbbf24')}
              </div>
              <div style="font-size:15px; color:var(--text-secondary); line-height:1.65;">
                <strong>Implementation Tier (${sell.buildType}):</strong> ${formatRichText('Gemini 3.1 Pro & 3.8 Flash translate unstructured disruption alerts, planner intent, and multimodal docs into formal mathematical parameters, invoke the deterministic solver on Vertex AI Agent Engine, and verify 100% physical/SLA compliance.')}
              </div>
            </div>

            <div class="showcase-panel" style="border-color:rgba(16,185,129,0.38);">
              <div class="panel-tag" style="color:#34d399;">🔐 Signed Enterprise API / BAPI / EDI Write-Back Payload</div>
              <div style="font-size:14.5px; font-family:var(--font-mono); color:#d1fae5; background:rgba(16,185,129,0.09); border:1px solid rgba(16,185,129,0.32); padding:16px 18px; border-radius:12px; margin-bottom:14px; line-height:1.68;">
                ${ag.apiWriteback || ''}
              </div>
              <div style="font-size:13px; color:#94a3b8; margin-bottom:8px; font-weight:700; text-transform:uppercase;">
                Connected Enterprise Systems &amp; Gateways:
              </div>
              <div class="sc-tech-pills">
                ${sysArr.map(s => `<span class="sc-tech-pill">${s}</span>`).join('')}
              </div>
            </div>
          </div>

          <!-- 4-Layer Agentic Supply Chain Reference Architecture -->
          <h3 class="block-title" style="font-size:22px; margin-top:16px; margin-bottom:4px;">4-Layer Vertex AI, BigQuery, Cloud Spanner &amp; AlloyDB Reference Stack</h3>
          <p class="block-subtitle" style="margin-bottom:14px;">End-to-end production deployment pattern for <strong>${ag.name}</strong>.</p>
          <div class="arch-layer-grid">
            <div class="arch-layer-card">
              <div class="arch-layer-num" style="color:var(--sc-cyan);">LAYER 01 · TELEMETRY &amp; SYSTEMS</div>
              <div class="arch-layer-title">Apigee + Pub/Sub + Dataflow</div>
              <div class="arch-layer-desc">${formatRichText(sysArr.join(', ') || 'SAP S/4HANA & IBP, Oracle OTM, Manhattan WMS, Blue Yonder TMS, CargoWise, EDI 204/214/315/404/856, Spire AIS, FlightAware ADS-B & IoT streams.')}</div>
            </div>
            <div class="arch-layer-card">
              <div class="arch-layer-num" style="color:var(--sc-emerald);">LAYER 02 · UNIFIED DATA FABRIC</div>
              <div class="arch-layer-title">BigQuery + Spanner + AlloyDB</div>
              <div class="arch-layer-desc">${formatRichText('Canonical SKU-Location-Tier entity graph in BigQuery + Cloud Spanner Graph and AlloyDB pgvector RAG.')}</div>
            </div>
            <div class="arch-layer-card">
              <div class="arch-layer-num" style="color:var(--sc-amber);">LAYER 03 · AGENTIC REASONING</div>
              <div class="arch-layer-title">Vertex AI Agent Engine + OR-Tools</div>
              <div class="arch-layer-desc">${formatRichText(ag.solverStack || 'Multi-agent orchestration combining Gemini 3.1 Pro & 3.8 Flash reasoning with Google OR-Tools & Google Maps Platform physical solvers.')}</div>
            </div>
            <div class="arch-layer-card">
              <div class="arch-layer-num" style="color:var(--sc-violet);">LAYER 04 · CONTROL TOWER UX</div>
              <div class="arch-layer-title">A2UI + Looker + Signed Write-Back</div>
              <div class="arch-layer-desc">${formatRichText(`Interactive 3D/2D vector schematics, Looker semantic charts, and 1-click signed write-back (${ag.apiWriteback || 'ERP/WMS/TMS'}).`)}</div>
            </div>
          </div>
        </div>
      `;

      hydrateAssets();
      showActivePage('pageBlueprint');
      const wrap = document.getElementById('blueprintGenieWrap');
      if (sRect && wrap) {
        animateGenieOutOfBox(sRect, wrap, dept.color);
      }
    }

    /* =========================================================================
       PAGE 4 RENDERING: DEDICATED END-TO-END VALUE CHAIN PAGE (F2F, O2D, S2P, P2R)
       ========================================================================= */
    function openValueChainPage(vcId, pushHash = true, ev = null) {
      const vc = VALUE_CHAINS[vcId];
      if (!vc) return;
      const useSlide = isPillOrNavSwitch(ev);
      const sRect = useSlide ? null : getClickedCardRect(ev);
      const transClass = getPageTransitionClass(ev, sRect);

      const videoUrl = customVcVideos[vc.id] || vc.videoSrc;
      const showVideoPlayer = vc.hasPreloadedVideo || Boolean(customVcVideos[vc.id]);
      const wmType = getVcWatermarkType(vc.id);

      if (pushHash) {
        history.pushState({ page: 'valuechain', id: vcId }, '', `#valuechain/${vcId}`);
      }

      const container = document.getElementById('valueChainPageContent');
      container.innerHTML = `
        <div id="vcGenieWrap" class="${transClass}">
          <div class="back-bar">
            <button type="button" class="back-btn" onclick="goToOrgChart()">
              <span>&larr;</span>
              <span>Back to CSCO Org Chart</span>
            </button>

            <div class="persona-switcher-pills">
              ${Object.values(VALUE_CHAINS).map(other => `
                <button type="button"
                        class="switch-pill ${other.id === vc.id ? 'active' : ''}"
                        style="${other.id === vc.id ? `background:${other.color}; border-color:${other.color}; color:#040810; font-weight:700;` : ''}"
                        onclick="openValueChainPage('${other.id}', true, event)">
                  ${other.shortTitle}
                </button>
              `).join('')}
            </div>
          </div>

          <div class="persona-header-card" style="border-color: ${vc.color}44;">
            ${renderSupplyChainWatermarkSvg(wmType, vc.color, 'persona-header-sc-watermark')}

            <div style="position:relative; z-index:2;">
              <div class="persona-badge" style="background: ${vc.color}22; color: ${vc.color}; border: 1px solid ${vc.color}55;">
                <span>${vc.flowBadge}</span>
              </div>
              <h1 class="persona-page-title">${vc.title}</h1>
              <p class="persona-page-summary">${formatRichText(vc.summary)}</p>
              <div class="persona-focus-pills">
                ${vc.focusAreas.map(f => `<span class="focus-pill">${f}</span>`).join('')}
              </div>
            </div>

            <div class="persona-stat-highlight" style="border-color: ${vc.color}44;">
              <div class="persona-stat-value" style="color: ${vc.color};">${vc.headlineStat}</div>
              <div class="persona-stat-label">${vc.headlineLabel}</div>
            </div>
          </div>

          <div class="time-shift-banner">
            <div class="shift-meter-card">
              <div class="shift-meter-top">
                <span style="color: var(--text-secondary);">Traditional Process</span>
                <span style="color: #ff8a80; font-weight: 700;">${vc.toilHoursBefore}</span>
              </div>
              <div class="shift-bar-track">
                <div style="width: 76%; background: var(--g-red);"></div>
                <div style="width: 24%; background: rgba(255,255,255,0.18);"></div>
              </div>
            </div>

            <div class="shift-meter-card">
              <div class="shift-meter-top">
                <span style="color: var(--text-secondary);">With Gemini Enterprise</span>
                <span style="color: #81c995; font-weight: 700;">${vc.toilHoursAfter}</span>
              </div>
              <div class="shift-bar-track">
                <div style="width: 16%; background: var(--g-green);"></div>
                <div style="width: 84%; background: var(--g-blue);"></div>
              </div>
            </div>
          </div>

          <!-- 3 Hero-Sized Executive Summary Cards for the Value Chain -->
          <div class="exec-pitch-grid">
            <div class="exec-pitch-card" style="--pitch-accent: #f87171;">
              <div class="exec-pitch-eyebrow" style="color:#fca5a5; background:rgba(239,68,68,0.14); border:1px solid rgba(239,68,68,0.4);">
                <span>✕ 01 · Process Gap (Before)</span>
              </div>
              <h2 class="exec-pitch-title">Siloed Handoffs &amp; Latency</h2>
              <div class="exec-pitch-body">${formatRichBullets(vc.problem, '#f87171')}</div>
            </div>

            <div class="exec-pitch-card" style="--pitch-accent: #38bdf8;">
              <div class="exec-pitch-eyebrow" style="color:#7dd3fc; background:rgba(56,189,248,0.14); border:1px solid rgba(56,189,248,0.4);">
                <span>⚡ 02 · How It Works</span>
              </div>
              <h2 class="exec-pitch-title">Golden Thread Multi-Agent Pipeline</h2>
              <div class="exec-pitch-body">${formatRichBullets(vc.solution, '#38bdf8')}</div>
            </div>

            <div class="exec-pitch-card" style="--pitch-accent: #34d399;">
              <div class="exec-pitch-eyebrow" style="color:#6ee7b7; background:rgba(16,185,129,0.14); border:1px solid rgba(16,185,129,0.4);">
                <span>✦ 03 · CSCO Advantage (${vc.headlineStat})</span>
              </div>
              <h2 class="exec-pitch-title">End-to-End Value Realization</h2>
              <div class="exec-pitch-body">${formatRichBullets(vc.advantage, '#34d399')}</div>
            </div>
          </div>

          <div class="ditl-header-row">
            <div>
              <h2 class="block-title">Connected 6-Stage Pipeline</h2>
              <p class="block-subtitle">Each stage passes verified supply chain context forward via a <span class="sc-hl-underline">Golden Thread</span>—eliminating manual spreadsheet handoffs.</p>
            </div>

            <div class="ditl-legend">
              <span class="legend-item">
                <span class="legend-swatch" style="background: var(--g-red);"></span>
                <span style="color: #ff8a80;">Manual Toil</span>
              </span>
              <span class="legend-item">
                <span class="legend-swatch" style="background: var(--g-green);"></span>
                <span style="color: #81c995;">Gemini Improvement</span>
              </span>
              <span class="legend-item">
                <span class="legend-swatch" style="background: var(--g-blue);"></span>
                <span style="color: #8ab4f8;">Golden Thread Handoff</span>
              </span>
            </div>
          </div>

          <div class="day-schedule">
            ${vc.stages.map(st => `
              <div class="vc-stage-row" style="--vc-stage-color: ${st.color};">
                <div class="vc-stage-meta">
                  <div>
                    <div class="vc-stage-num" style="color: ${st.color};">${st.num}</div>
                    <div class="vc-stage-name">${st.name}</div>
                  </div>
                  <div class="vc-modality-row">
                    <span class="vc-modality-pill" style="border-color: ${st.color}55; color: ${st.color};">${st.modality}</span>
                    <span class="vc-modality-pill">${st.systems}</span>
                  </div>
                  <button type="button" class="vc-owner-btn" onclick="openPersonaPage('${st.ownerId}', true, event)">
                    <span>👤 ${st.ownerLabel} &rarr;</span>
                  </button>
                </div>

                <div class="toil-highlight-box">
                  <div class="toil-top-bar">
                    <span class="toil-badge">✕ Manual Toil</span>
                    <span class="toil-duration">${st.toilTime}</span>
                  </div>
                  <div class="toil-text">${formatRichBullets(st.before, '#f87171')}</div>
                </div>

                <div class="gemini-improve-box">
                  <div class="improve-top-bar">
                    <span class="improve-badge">
                      <img data-asset="sparkle_blue_violet.png" alt="" />
                      <span>Gemini Improvement</span>
                    </span>
                    <span class="improve-time-saved">${st.toilTime} &rarr; ${st.afterTime}</span>
                  </div>
                  <div class="improve-text">${formatRichBullets(st.after, '#34d399')}</div>
                  <div class="vc-golden-thread">
                    <div class="vc-golden-label">🔗 Golden Thread Handoff</div>
                    <div>${formatRichText(st.goldenThread)}</div>
                  </div>
                </div>
              </div>
            `).join('')}
          </div>

          <h2 class="block-title" style="margin-bottom: 6px;">Interactive Simulation &amp; End-to-End Walkthrough</h2>
          <p class="block-subtitle" style="margin-bottom: 20px;">Interact with the live <strong>${vc.shortTitle}</strong> CAD simulator or watch the pre-rendered walkthrough.</p>

          <div class="video-stage-box">
            <div class="video-viewport">
              ${renderStageViewportHtml(vc, 'vc', videoUrl, showVideoPlayer)}
            </div>

            <div class="video-toolbar">
              <span>${stageViewMode === 'cad' ? `Interactive Vector CAD Studio: ${vc.title}` : `End-to-End Recording: ${vc.title}`}</span>
              <div style="display:flex; flex-wrap:wrap; gap:8px;">
                <button type="button" class="upload-video-btn ${stageViewMode==='cad'?'active':''}"
                        onclick="stageViewMode='cad';openValueChainPage('${vc.id}', false)">
                  <span>✦ Interactive CAD Simulator</span>
                </button>
                <button type="button" class="upload-video-btn ${stageViewMode==='video'?'active':''}"
                        onclick="stageViewMode='video';openValueChainPage('${vc.id}', false)">
                  <span>▶ Watch Walkthrough (.mp4)</span>
                </button>
                <label class="upload-video-btn">
                  <span>Swap Local .mp4</span>
                  <input type="file" accept="video/*" style="display:none;" onchange="attachValueChainVideo(event, '${vc.id}')" />
                </label>
              </div>
            </div>
          </div>
        </div>
      `;

      hydrateAssets();
      showActivePage('pageValueChain');
      const wrap = document.getElementById('vcGenieWrap');
      if (sRect && wrap) {
        animateGenieOutOfBox(sRect, wrap, vc.color);
      }
    }

    function attachValueChainVideo(event, vcId) {
      const file = event.target.files && event.target.files[0];
      if (!file) return;
      customVcVideos[vcId] = URL.createObjectURL(file);
      stageViewMode = 'video';
      openValueChainPage(vcId, false);
    }

    /* =========================================================================
       PAGE 5 RENDERING: SEARCHABLE 26 PERSONAS & 32 AGENTS DIRECTORY
       ========================================================================= */
    let currentDirDeptFilter = 'all';
    let currentDirSearch = '';
    let currentDirMode = 'personas'; // 'personas' (26) | 'agents' (32)

    function renderDirectoryCardsHtml(deptFilter, searchQuery, mode = currentDirMode) {
      const q = (searchQuery || '').trim().toLowerCase();

      if (mode === 'agents') {
        const agentsList = Object.values(AGENTS).filter(ag => {
          if (deptFilter === 'universal' && !ag.isUniversal) return false;
          if (deptFilter !== 'all' && deptFilter !== 'universal' && ag.deptId !== deptFilter) return false;
          if (!q) return true;
          const dept = getDeptMeta(ag.deptId);
          const haystack = [
            ag.name, ag.shortDesc, ag.badge, ag.problem, ag.solution, ag.advantage,
            ag.solverStack || '', ag.apiWriteback || '',
            dept ? dept.name : '', dept ? dept.fullName : '',
            ...toSysArray(ag.systems)
          ].join(' ').toLowerCase();
          return haystack.includes(q);
        });

        if (!agentsList.length) {
          return `
            <div style="grid-column: 1 / -1; padding: 42px; text-align: center; border-radius: 18px; border: 1px dashed rgba(148,163,184,0.28); color: var(--text-secondary); font-size: 15.5px;">
              No Supply Chain Agents matched "<strong>${searchQuery}</strong>". Try clearing the filter or searching for "Ocean", "Air Cargo", "Rail", "Spanner", "Google Maps", "SAP", "LIFO", or "Tier-N".
            </div>
          `;
        }

        return agentsList.map(ag => {
          const dept = getDeptMeta(ag.deptId);
          const sell = getAgentSellingMeta(ag, dept);
          return `
            <div class="dir-persona-card" style="--dept-accent: ${dept.color};">
              <div>
                <div class="dir-card-top">
                  <div>
                    <div style="font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:4px;">
                      ${ag.isUniversal ? '🌐 Cross-Persona Universal Agent · All 26 Roles' : `${dept.scorBadge || ''} · ${dept.name}`}
                    </div>
                    <div style="font-family:var(--font-display); font-size:20px; font-weight:800; color:#f8fafc;">
                      ${ag.name}
                    </div>
                  </div>
                  <div style="text-align:right;">
                    <div style="font-family:var(--font-display); font-size:18px; font-weight:800; color:${dept.color};">${ag.badge}</div>
                    <div style="font-size:11.5px; color:#38bdf8; font-weight:600;">${sell.buildType}</div>
                  </div>
                </div>

                <p style="font-size:15.5px; color:var(--text-secondary); line-height:1.68; margin: 14px 0;">
                  ${formatRichText(ag.shortDesc)}
                </p>

                <div class="sc-tech-pills" style="margin-bottom: 14px;">
                  ${toSysArray(ag.systems).slice(0, 5).map(s => `<span class="sc-tech-pill">${s}</span>`).join('')}
                </div>
              </div>

              <div>
                <div class="dir-agent-launch-row" onclick="openAgentPage('${ag.id}', true, event)">
                  <div>
                    <div style="font-size:11.5px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color};">
                      ✦ Executive Value Pitch, ROI &amp; Live CAD/Video Studio
                    </div>
                    <div style="font-family:var(--font-display); font-size:16px; font-weight:800; color:#f8fafc;">
                      Open ${ag.name} Selling Page
                    </div>
                  </div>
                  <span style="font-size:14px; font-weight:700; color:${dept.color}; white-space:nowrap;">Expand &rarr;</span>
                </div>

                <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; flex-wrap:wrap; margin-top:14px; padding-top:12px; border-top:1px solid rgba(148,163,184,0.16);">
                  <span style="font-size:13px; color:var(--text-secondary);">
                    ${ag.isUniversal ? 'Used by all 26 Personas' : `Used by ${sell.usedByPersonas.length} Personas`}
                  </span>
                  <button type="button" class="switch-pill" style="border-color:#c084fc66; color:#e9d5ff;" onclick="openAgentBlueprintPage('${ag.id}', true, event)">
                    🏗️ High-Code Blueprint &rarr;
                  </button>
                </div>
              </div>
            </div>
          `;
        }).join('');
      }

      // Default mode: 'personas' (26 Personas)
      const personasList = Object.values(PERSONAS).filter(p => {
        if (deptFilter !== 'all' && deptFilter !== 'universal' && p.deptId !== deptFilter) return false;
        if (!q) return true;
        const dept = getDeptMeta(p.deptId);
        const ag = AGENTS[p.agentIds[0]];
        const haystack = [
          p.name, p.role, p.summary, p.headlineStat, p.headlineLabel,
          ...(p.focusAreas || []),
          dept ? dept.name : '', dept ? dept.fullName : '',
          ag ? ag.name : '', ag ? ag.shortDesc : '', ag ? ag.solverStack : '',
          ...toSysArray(ag ? ag.systems : '')
        ].join(' ').toLowerCase();
        return haystack.includes(q);
      });

      if (!personasList.length) {
        return `
          <div style="grid-column: 1 / -1; padding: 42px; text-align: center; border-radius: 18px; border: 1px dashed rgba(148,163,184,0.28); color: var(--text-secondary); font-size: 15.5px;">
            No Supply Chain Personas matched "<strong>${searchQuery}</strong>". Try clearing the filter or searching for "Air Cargo", "Rail", "Ocean", "SAP", "LIFO", "WMS", or "OEE".
          </div>
        `;
      }

      return personasList.map(p => {
        const dept = getDeptMeta(p.deptId);
        const ag = AGENTS[p.agentIds[0]];
        const drawerId = `dirDrawer_${p.id}`;
        return `
          <div class="dir-persona-card" style="--dept-accent: ${dept.color};">
            <div>
              <div class="dir-card-top">
                <div class="dir-card-person">
                  <div class="persona-emoji" style="width:44px; height:44px; font-size:21px;">${p.icon}</div>
                  <div>
                    <div style="font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color};">
                      ${dept.scorBadge || ''} · ${dept.name}
                    </div>
                    <div style="font-family:var(--font-display); font-size:19.5px; font-weight:800; color:#f8fafc;">
                      ${p.name}
                    </div>
                    <div style="font-size:13.5px; color:var(--text-secondary);">${p.role}</div>
                  </div>
                </div>
                <div style="text-align:right;">
                  <div style="font-family:var(--font-display); font-size:19px; font-weight:800; color:${dept.color};">${p.headlineStat}</div>
                  <div style="font-size:12px; color:var(--text-secondary); max-width:140px;">${p.headlineLabel}</div>
                </div>
              </div>

              <p style="font-size:15.5px; color:var(--text-secondary); line-height:1.68; margin: 14px 0;">
                ${formatRichText(p.summary)}
              </p>

              <div class="sc-tech-pills" style="margin-bottom: 14px;">
                ${(p.focusAreas || []).map(f => `<span class="sc-tech-pill">${f}</span>`).join('')}
              </div>

              <!-- Smooth Dropdown Drawer for Quick Spec Preview + 4 Universal Agents -->
              <div id="${drawerId}" class="sc-dropdown-block">
                <button type="button" class="sc-dropdown-btn" onclick="toggleScDropdown('${drawerId}')">
                  <span>⚡ Daily Toil Shift &amp; Connected Agents (${(p.agentIds || []).length} Domain + 4 Universal)</span>
                  <span class="sc-dropdown-chevron">▾</span>
                </button>
                <div class="sc-dropdown-body">
                  <div class="sc-dropdown-inner">
                    <div style="display:flex; justify-content:space-between; font-size:13.5px; margin-bottom:10px;">
                      <span style="color:#ff8a80;">Before: ${p.toilHoursBefore}</span>
                      <span style="color:#81c995; font-weight:700;">After: ${p.toilHoursAfter}</span>
                    </div>
                    <div style="font-size:12.5px; color:#38bdf8; font-weight:700; margin-bottom:8px;">
                      Shared Cross-Persona Universal Agents:
                    </div>
                    <div style="display:flex; flex-wrap:wrap; gap:8px;">
                      ${UNIVERSAL_AGENT_IDS.map(uid => {
                        const uag = AGENTS[uid];
                        return uag ? `<button type="button" class="sc-tech-pill" style="cursor:pointer; border-color:#38bdf855; color:#bae6fd;" onclick="openAgentPage('${uag.id}', true, event)">🌐 ${uag.name}</button>` : '';
                      }).join('')}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div>
              ${ag ? `
                <div class="dir-agent-launch-row" onclick="openAgentPage('${ag.id}', true, event)">
                  <div>
                    <div style="font-size:11.5px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color};">
                      🔌 Primary Domain Agent · ${ag.badge}
                    </div>
                    <div style="font-family:var(--font-display); font-size:16px; font-weight:800; color:#f8fafc;">
                      ${ag.name}
                    </div>
                  </div>
                  <span style="font-size:14px; font-weight:700; color:${dept.color}; white-space:nowrap;">Expand &rarr;</span>
                </div>
              ` : ''}

              <div style="display:flex; justify-content:space-between; align-items:center; margin-top:14px; padding-top:12px; border-top:1px solid rgba(148,163,184,0.16);">
                <div class="sc-tech-pills">
                  ${toSysArray(ag ? ag.systems : '').slice(0, 2).map(s => `<span class="sc-tech-pill">${s}</span>`).join('')}
                </div>
                <button type="button" class="switch-pill" style="border-color:${dept.color}66; color:${dept.color};" onclick="openPersonaPage('${p.id}', true, event)">
                  Day in the Life &rarr;
                </button>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    function filterDirectoryLive(val) {
      currentDirSearch = val || '';
      const grid = document.getElementById('dirPersonaGridEl');
      if (grid) {
        grid.innerHTML = renderDirectoryCardsHtml(currentDirDeptFilter, currentDirSearch, currentDirMode);
      }
    }

    function openPersonasDirectoryPage(deptFilter = 'all', searchQuery = '', pushHash = true, mode = null, ev = null) {
      currentDirDeptFilter = deptFilter || 'all';
      currentDirSearch = searchQuery || '';
      if (mode) {
        currentDirMode = mode;
      } else if (deptFilter === 'universal') {
        currentDirMode = 'agents';
      }

      if (pushHash) {
        history.pushState({ page: 'directory', dept: currentDirDeptFilter, mode: currentDirMode }, '', '#directory');
      }

      const transClass = getPageTransitionClass(ev, null);
      const container = document.getElementById('directoryPageContent');
      container.innerHTML = `
        <div class="${transClass}">
          <div class="back-bar">
            <button type="button" class="back-btn" onclick="goToOrgChart()">
              <span>&larr;</span>
              <span>Back to CSCO Org Chart</span>
            </button>

            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              <button type="button"
                      class="switch-pill ${currentDirMode === 'personas' ? 'active' : ''}"
                      style="${currentDirMode === 'personas' ? 'background:#00d2ff; color:#040810; border-color:#00d2ff; font-weight:700;' : ''}"
                      onclick="openPersonasDirectoryPage(currentDirDeptFilter === 'universal' ? 'all' : currentDirDeptFilter, currentDirSearch, false, 'personas', event)">
                👥 View All 26 Personas
              </button>
              <button type="button"
                      class="switch-pill ${currentDirMode === 'agents' ? 'active' : ''}"
                      style="${currentDirMode === 'agents' ? 'background:#38bdf8; color:#040810; border-color:#38bdf8; font-weight:700;' : ''}"
                      onclick="openPersonasDirectoryPage(currentDirDeptFilter, currentDirSearch, false, 'agents', event)">
                🤖 View All 32 AI Agents (28 Domain + 4 Universal)
              </button>
              <button type="button" class="switch-pill" onclick="openArchitecturePage(true, event)">
                🏗️ Enterprise Architecture
              </button>
            </div>
          </div>

          <div class="persona-header-card" style="border-color: rgba(0, 210, 255, 0.42);">
            ${renderSupplyChainWatermarkSvg('demand_wave', '#00d2ff', 'persona-header-sc-watermark')}

            <div style="position:relative; z-index:2;">
              <div class="persona-badge" style="background: rgba(0,210,255,0.14); color: #00d2ff; border: 1px solid rgba(0,210,255,0.45);">
                <span>👥 Complete ASCM SCOR Supply Chain Role &amp; Agent Directory</span>
              </div>
              <h1 class="persona-page-title">
                ${currentDirMode === 'agents'
                  ? '32 Supply Chain AI Agents (4 Cross-Persona Universal + 28 Domain Agents)'
                  : '26 Supply Chain Personas Across 6 SCOR Verticals'}
              </h1>
              <p class="persona-page-summary">
                Browse or search every role and AI agent across <span class="sc-hl-underline">Plan (Demand &amp; S&amp;OP)</span>, <span class="sc-hl-underline">Source (Procurement &amp; Tier-N Risk)</span>, <span class="sc-hl-underline">Make (Manufacturing &amp; Plant OEE)</span>, <span class="sc-hl-underline">Fulfill (MEIO, Cross-Dock &amp; 3D WMS)</span>, <span class="sc-hl-underline">Deliver (Ocean, Air Cargo, Intermodal Rail &amp; 3D LIFO Road Fleet)</span>, and <span class="sc-hl-underline">Return &amp; Enable (Circular &amp; Scope 3 ESG)</span>.
              </p>
            </div>

            <div class="persona-stat-highlight" style="border-color: rgba(0, 210, 255, 0.4);">
              <div class="persona-stat-value" style="color: #00d2ff;">26 × 32</div>
              <div class="persona-stat-label">6 SCOR Verticals · 26 Personas · 28 Domain Agents + 4 Universal Agents</div>
            </div>
          </div>

          <!-- Search & Vertical Filter Bar -->
          <div class="dir-controls-bar">
            <input type="search"
                   class="dir-search-input"
                   placeholder="🔍 Search by role, agent, GCP service or ERP/WMS/TMS system (e.g. Ocean, Air ULD, Rail, Spanner, Maps, SAP IBP, LIFO)..."
                   value="${currentDirSearch}"
                   oninput="filterDirectoryLive(this.value)" />

            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              <button type="button"
                      class="switch-pill ${currentDirDeptFilter === 'all' ? 'active' : ''}"
                      style="${currentDirDeptFilter === 'all' ? 'background:#00d2ff; color:#040810; border-color:#00d2ff; font-weight:700;' : ''}"
                      onclick="openPersonasDirectoryPage('all', currentDirSearch, false, currentDirMode, event)">
                All 6 SCOR Verticals (${currentDirMode === 'agents' ? '32 Agents' : '26 Personas'})
              </button>
              <button type="button"
                      class="switch-pill ${currentDirDeptFilter === 'universal' ? 'active' : ''}"
                      style="${currentDirDeptFilter === 'universal' ? 'background:#38bdf8; color:#040810; border-color:#38bdf8; font-weight:700;' : ''}"
                      onclick="openPersonasDirectoryPage('universal', currentDirSearch, false, 'agents', event)">
                🌐 Cross-Persona Universal Agents (4)
              </button>
              ${Object.values(DEPARTMENTS).map(d => {
                const count = currentDirMode === 'agents'
                  ? Object.values(AGENTS).filter(a => !a.isUniversal && a.deptId === d.id).length
                  : d.personaIds.length;
                return `
                  <button type="button"
                          class="switch-pill ${currentDirDeptFilter === d.id ? 'active' : ''}"
                          style="${currentDirDeptFilter === d.id ? `background:${d.color}; color:#040810; border-color:${d.color}; font-weight:700;` : ''}"
                          onclick="openPersonasDirectoryPage('${d.id}', currentDirSearch, false, currentDirMode, event)">
                    ${d.name} (${count})
                  </button>
                `;
              }).join('')}
            </div>
          </div>

          <div id="dirPersonaGridEl" class="dir-persona-grid">
            ${renderDirectoryCardsHtml(currentDirDeptFilter, currentDirSearch, currentDirMode)}
          </div>
        </div>
      `;

      hydrateAssets();
      showActivePage('pageDirectory');
    }

    /* =========================================================================
       PAGE 6 RENDERING: ENTERPRISE MULTI-AGENT REFERENCE ARCHITECTURE PAGE
       ========================================================================= */
    let currentArchVerticalFilter = 'all';

    function filterArchVertical(deptFilter) {
      currentArchVerticalFilter = deptFilter || 'all';
      openArchitecturePage(false);
    }

    function openArchitecturePage(pushHash = true, ev = null) {
      if (pushHash) {
        history.pushState({ page: 'architecture' }, '', '#architecture');
      }

      const transClass = getPageTransitionClass(ev, null);
      const container = document.getElementById('architecturePageContent');
      container.innerHTML = `
        <div class="${transClass}">
          <div class="back-bar">
            <button type="button" class="back-btn" onclick="goToOrgChart()">
              <span>&larr;</span>
              <span>Back to CSCO Org Chart</span>
            </button>

            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              <button type="button" class="switch-pill" onclick="openPersonasDirectoryPage('all', '', true, 'agents', event)">
                🤖 Explore All 32 AI Agents
              </button>
              <button type="button" class="switch-pill" onclick="openPersonasDirectoryPage('all', '', true, 'personas', event)">
                👥 Explore All 26 Personas
              </button>
            </div>
          </div>

          <div class="persona-header-card" style="border-color: rgba(168, 85, 247, 0.45);">
            ${renderSupplyChainWatermarkSvg('supplier_graph', '#a855f7', 'persona-header-sc-watermark')}

            <div style="position:relative; z-index:2;">
              <div class="persona-badge" style="background: rgba(168,85,247,0.16); color: #c084fc; border: 1px solid rgba(168,85,247,0.45);">
                <span>🏗️ Google Cloud · Vertex AI Agent Engine · BigQuery · Cloud Spanner · AlloyDB · Google Maps · OR-Tools</span>
              </div>
              <h1 class="persona-page-title">Enterprise Supply Chain Reference Architecture</h1>
              <p class="persona-page-summary">
                Five-layer reference architecture synchronizing enterprise ERP/WMS/TMS systems of record, real-time multi-modal telemetry, deterministic solvers, and autonomous A2A sub-agent swarms.
              </p>
            </div>

            <div class="persona-stat-highlight" style="border-color: rgba(168, 85, 247, 0.45);">
              <div class="persona-stat-value" style="color: #c084fc;">32 Agents</div>
              <div class="persona-stat-label">4 Universal + 28 Domain Agents · 96 A2A Sub-Agents · 26 Personas</div>
            </div>
          </div>

          <!-- Full-Width Enterprise 5-Layer SVG Architecture Diagram (Enlarged Typography & Clear Spacing) -->
          <div class="agent-arch-box" style="margin-top:0; margin-bottom:32px; border-color:rgba(0,210,255,0.38);">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:18px;">
              <div>
                <div style="font-size:13px; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; color:#00d2ff;">
                  ✦ End-to-End Multi-Agent System Topology
                </div>
                <div style="font-family:var(--font-display); font-size:22px; font-weight:800; color:#f8fafc; margin-top:2px;">
                  BigQuery + Spanner + AlloyDB Twin &rarr; 4 Universal + 28 Domain Agents &rarr; OR-Tools &amp; Maps &rarr; A2UI Control Tower
                </div>
              </div>
              <span class="sc-tech-pill" style="border-color:#10b98166; color:#34d399; font-size:13px; padding:6px 14px;">
                Zero Unverified ERP/WMS/TMS Write-Backs
              </span>
            </div>

            <div style="border-radius:16px; overflow:hidden; border:1px solid rgba(148,163,184,0.26); background:#040812;">
              <svg viewBox="0 0 1120 510" style="width:100%; height:auto; display:block;">
                <defs>
                  ${[0,1,2,3,4,5].map(idx => `<clipPath id="scorSwarmClip${idx}"><rect x="${34 + idx * 176}" y="156" width="166" height="96" rx="12" /></clipPath>`).join('')}
                </defs>

                <!-- Vertical Telemetry Connector Lines Between Layers -->
                ${[117, 293, 469, 645, 821, 997].map(cx => `
                  <line x1="${cx}" y1="102" x2="${cx}" y2="118" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4 4" />
                  <line x1="${cx}" y1="268" x2="${cx}" y2="284" stroke="#a855f7" stroke-width="2" stroke-dasharray="4 4" />
                  <line x1="${cx}" y1="382" x2="${cx}" y2="398" stroke="#00d2ff" stroke-width="2" stroke-dasharray="4 4" />
                `).join('')}

                <!-- Band 1: Control Tower UX + 4 Universal Cross-Persona Agents -->
                <rect x="20" y="18" width="1080" height="84" rx="14" fill="rgba(56,189,248,0.11)" stroke="#38bdf8" stroke-width="2" />
                <text x="38" y="44" fill="#38bdf8" font-size="12.5" font-weight="700">LAYER 05 · A2UI CONTROL TOWER + 4 CROSS-PERSONA UNIVERSAL AGENTS (SHARED ACROSS ALL 26 ROLES)</text>
                <text x="38" y="68" fill="#ffffff" font-size="13.5" font-weight="700">🌐 TowerMind Control Tower Copilot   ·   🌐 StormShield WeatherNext 3 War-Room   ·   🌐 DataCleanse Master Data Steward   ·   🌐 MarginBridge CSCO-to-CFO Twin</text>
                <text x="38" y="90" fill="#cbd5e1" font-size="12.5">Interactive Multi-Modal &amp; 3D CAD Studios · Looker Semantic Layer · Signed ERP/WMS/TMS Write-Back</text>

                <!-- Band 2: 6 SCOR Vertical Agent Swarms (28 Domain Agents) -->
                <rect x="20" y="118" width="1080" height="150" rx="14" fill="rgba(168,85,247,0.10)" stroke="#a855f7" stroke-width="2.2" />
                <text x="38" y="144" fill="#c084fc" font-size="12.5" font-weight="700">LAYER 03 · VERTEX AI AGENT ENGINE (6 SCOR VERTICAL SWARMS · 28 DOMAIN AGENTS · 96 A2A SUB-AGENTS)</text>

                ${[
                  { title: '01 · PLAN (4 Agents)', sub1: 'PulseCast · Synapse S&OP', sub2: 'ElasticityIQ · ChannelSync', col: '#10b981', x: 34 },
                  { title: '02 · SOURCE (4 Agents)', sub1: 'SourcePulse · NexusShield', sub2: 'ClauseGuard · QualiShield', col: '#a855f7', x: 210 },
                  { title: '03 · MAKE (4 Agents)', sub1: 'ChronosMake · SpindleGuard', sub2: 'YieldVision · ChangeSync', col: '#3b82f6', x: 386 },
                  { title: '04 · FULFILL (5 Agents)', sub1: 'EchelonFlow · SlotMaster 3D', sub2: 'PromiseGuard · Yard · CrossDock', col: '#00d2ff', x: 562 },
                  { title: '05 · DELIVER (7 Agents)', sub1: 'PortWatch · AeroFreight · Rail', sub2: 'ModalShift · FleetFlow · LIFO 3D', col: '#f59e0b', x: 738 },
                  { title: '06 · ENABLE (4 Agents)', sub1: 'OTIFShield · ReturnLoop RMA', sub2: 'EcoChain ESG · TwinDesign', col: '#ec4899', x: 914 }
                ].map((b, idx) => `
                  <g>
                    <rect x="${b.x}" y="156" width="166" height="96" rx="12" fill="rgba(4,9,18,0.95)" stroke="${b.col}" stroke-width="1.8" />
                    <g clip-path="url(#scorSwarmClip${idx})">
                      <text x="${b.x + 12}" y="182" fill="${b.col}" font-size="12" font-weight="700">${b.title}</text>
                      <text x="${b.x + 12}" y="206" fill="#f8fafc" font-size="11.2" font-weight="500">${b.sub1}</text>
                      <text x="${b.x + 12}" y="228" fill="#cbd5e1" font-size="11.2">${b.sub2}</text>
                    </g>
                  </g>
                `).join('')}

                <!-- Band 3: Deterministic Math & Physics Solvers + 3-Segment Data Foundation -->
                <rect x="20" y="284" width="528" height="98" rx="14" fill="rgba(245,158,11,0.09)" stroke="#f59e0b" stroke-width="1.8" />
                <text x="38" y="312" fill="#fbbf24" font-size="12.5" font-weight="700">LAYER 04 · GOOGLE OR-TOOLS, GOOGLE MAPS PLATFORM &amp; TIMESFM SOLVERS</text>
                <text x="38" y="338" fill="#f1f5f9" font-size="12.5">• OR-Tools CP-SAT, Multi-Modal MILP &amp; CVRPTW  ·  Google Maps Routes &amp; Fleet Engine</text>
                <text x="38" y="362" fill="#f1f5f9" font-size="12.5">• 3D Bin-Packing (Trailer LIFO &amp; Aircraft ULD)  ·  Vertex AI TimesFM &amp; WeatherNext 3</text>

                <rect x="564" y="284" width="536" height="98" rx="14" fill="rgba(0,210,255,0.09)" stroke="#00d2ff" stroke-width="1.8" />
                <text x="582" y="312" fill="#00d2ff" font-size="12.5" font-weight="700">LAYER 02 · BIGQUERY TWIN, CLOUD SPANNER GRAPH &amp; ALLOYDB PGVECTOR</text>
                <text x="582" y="338" fill="#f1f5f9" font-size="12.5">• BigQuery Supply Chain Twin &amp; GIS  ·  Cloud Spanner Tier-N BOM &amp; Global ATP Graph</text>
                <text x="582" y="362" fill="#f1f5f9" font-size="12.5">• AlloyDB Operational Store &amp; Contract RAG  ·  Google Earth Engine &amp; Document AI</text>

                <!-- Band 4: Enterprise Systems of Record & Telemetry Ingestion -->
                <rect x="20" y="398" width="1080" height="92" rx="14" fill="rgba(15,23,42,0.96)" stroke="#38bdf8" stroke-width="1.8" />
                <text x="38" y="424" fill="#38bdf8" font-size="12.5" font-weight="700">LAYER 01 · SYSTEMS OF RECORD &amp; TELEMETRY (APIGEE + PUB/SUB + DATAFLOW)</text>
                <text x="38" y="450" fill="#f1f5f9" font-size="12.8">SAP S/4HANA (MM/PP/SD/EWM/TM), SAP IBP, SAP Ariba · Oracle OTM · Manhattan Active WMS · Blue Yonder TMS · Siemens MES</text>
                <text x="38" y="474" fill="#cbd5e1" font-size="12.2">CargoWise · IATA ONE Record · Spire Ocean AIS · FlightAware ADS-B · Railinc EDI 404 · Project44 · Samsara ELD</text>
              </svg>
            </div>
          </div>

          <!-- Interactive SCOR Vertical Filter Bar on Architecture Page -->
          <div class="dir-controls-bar" style="margin-bottom:28px;">
            <div style="font-family:var(--font-display); font-size:16px; font-weight:700; color:#f8fafc;">
              Filter Architecture Specifications:
            </div>
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              <button type="button"
                      class="switch-pill ${currentArchVerticalFilter === 'all' ? 'active' : ''}"
                      style="${currentArchVerticalFilter === 'all' ? 'background:#00d2ff; color:#040810; border-color:#00d2ff; font-weight:700;' : ''}"
                      onclick="filterArchVertical('all')">
                All 32 Agents
              </button>
              <button type="button"
                      class="switch-pill ${currentArchVerticalFilter === 'universal' ? 'active' : ''}"
                      style="${currentArchVerticalFilter === 'universal' ? 'background:#38bdf8; color:#040810; border-color:#38bdf8; font-weight:700;' : ''}"
                      onclick="filterArchVertical('universal')">
                🌐 4 Universal Core
              </button>
              ${Object.values(DEPARTMENTS).map(d => {
                const count = Object.values(AGENTS).filter(a => !a.isUniversal && a.deptId === d.id).length;
                return `
                  <button type="button"
                          class="switch-pill ${currentArchVerticalFilter === d.id ? 'active' : ''}"
                          style="${currentArchVerticalFilter === d.id ? `background:${d.color}; color:#040810; border-color:${d.color}; font-weight:700;` : ''}"
                          onclick="filterArchVertical('${d.id}')">
                    ${d.name} (${count})
                  </button>
                `;
              }).join('')}
            </div>
          </div>

          ${(currentArchVerticalFilter === 'all' || currentArchVerticalFilter === 'universal') ? `
          <!-- 4 Cross-Persona Universal Agents Architecture Matrix -->
          <div style="margin-bottom: 36px;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:14px;">
              <span class="accent-dot" style="background:#38bdf8; box-shadow:0 0 12px #38bdf8;"></span>
              <h3 style="font-family:var(--font-display); font-size:22px; font-weight:700; color:#f8fafc;">
                Cross-Persona Universal Core Agents (Shared Across All 26 Roles)
              </h3>
            </div>
            <div class="dir-persona-grid">
              ${UNIVERSAL_AGENT_IDS.map(uid => {
                const ag = AGENTS[uid];
                if (!ag) return '';
                return `
                  <div class="dir-persona-card" style="--dept-accent:#38bdf8; display:flex; flex-direction:column; justify-content:space-between;">
                    <div>
                      <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px; margin-bottom:10px;">
                        <div>
                          <div style="font-size:11.5px; font-weight:700; color:#38bdf8; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:4px;">
                            🌐 Universal Core · All 26 Roles
                          </div>
                          <div style="font-family:var(--font-display); font-size:19px; font-weight:700; color:#f8fafc; line-height:1.25;">
                            ${ag.name}
                          </div>
                        </div>
                        <span class="sc-tech-pill" style="border-color:#38bdf866; color:#38bdf8; font-weight:700; font-size:12px;">${ag.badge}</span>
                      </div>

                      <p style="font-size:14px; color:#cbd5e1; line-height:1.56; margin-bottom:14px;">${ag.shortDesc}</p>

                      <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07); border-radius:12px; padding:12px 14px; margin-bottom:14px; display:flex; flex-direction:column; gap:8px;">
                        <div style="display:grid; grid-template-columns:88px 1fr; gap:4px 8px; font-size:12.5px; align-items:baseline;">
                          <span style="font-weight:700; color:#94a3b8; text-transform:uppercase; font-size:11px;">SOLVER</span>
                          <span style="color:#f1f5f9; font-family:var(--font-mono); font-size:12px;">${ag.solverStack || ''}</span>
                        </div>
                        <div style="display:grid; grid-template-columns:88px 1fr; gap:4px 8px; font-size:12.5px; align-items:baseline;">
                          <span style="font-weight:700; color:#94a3b8; text-transform:uppercase; font-size:11px;">WRITE-BACK</span>
                          <span style="color:#a7f3d0; font-family:var(--font-mono); font-size:12px;">${ag.apiWriteback || ''}</span>
                        </div>
                        <div style="display:grid; grid-template-columns:88px 1fr; gap:4px 8px; font-size:12.5px; align-items:baseline;">
                          <span style="font-weight:700; color:#94a3b8; text-transform:uppercase; font-size:11px;">A2A SWARM</span>
                          <span style="color:#cbd5e1; font-size:12px;">${(ag.subAgents || []).map(sa => `<strong style="color:#f8fafc;">${sa.name}</strong>`).join(' · ')}</span>
                        </div>
                      </div>
                    </div>

                    <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.08);">
                      <button type="button" class="switch-pill" style="border-color:#38bdf855; color:#38bdf8; font-size:13px; font-weight:600;" onclick="openAgentBlueprintPage('${ag.id}', true, event)">
                        Technical Blueprint &rarr;
                      </button>
                      <button type="button" style="font-size:12.5px; font-weight:600; color:#94a3b8;" onclick="openAgentPage('${ag.id}', true, event)">
                        Executive Pitch ↗
                      </button>
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
          ` : ''}

          <!-- Complete 28-Domain-Agent Architecture Matrix by 6 SCOR Verticals -->
          ${currentArchVerticalFilter !== 'universal' ? `
          <div style="margin-bottom: 24px;">
            <h2 class="block-title" style="font-size:22px; margin-bottom:4px;">Domain-Specific Agent Architectures</h2>
            <p class="block-subtitle" style="font-size:14.5px; color:#94a3b8; margin-bottom:24px;">Inspected specifications across deterministic solvers, A2A sub-agent swarms, and enterprise systems of record.</p>
          </div>

          ${Object.values(DEPARTMENTS)
            .filter(dept => currentArchVerticalFilter === 'all' || dept.id === currentArchVerticalFilter)
            .map(dept => {
            const deptAgents = Object.values(AGENTS).filter(a => !a.isUniversal && a.deptId === dept.id);
            return `
            <div style="margin-bottom: 34px;">
              <div style="display:flex; align-items:center; gap:10px; margin-bottom:14px;">
                <span class="accent-dot" style="background:${dept.color}; box-shadow:0 0 12px ${dept.color};"></span>
                <h3 style="font-family:var(--font-display); font-size:21px; font-weight:700; color:#f8fafc;">
                  ${dept.scorBadge} · ${dept.fullName} (${deptAgents.length} Agents)
                </h3>
              </div>

              <div class="dir-persona-grid">
                ${deptAgents.map(ag => {
                  const sell = getAgentSellingMeta(ag, dept);
                  const primaryP = sell.usedByPersonas[0];
                  return `
                    <div class="dir-persona-card" style="--dept-accent:${dept.color}; display:flex; flex-direction:column; justify-content:space-between;">
                      <div>
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px; margin-bottom:10px;">
                          <div>
                            <div style="font-size:11.5px; font-weight:700; color:${dept.color}; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:4px;">
                              ${primaryP ? `${primaryP.icon} ${primaryP.name}` : dept.name}
                            </div>
                            <div style="font-family:var(--font-display); font-size:19px; font-weight:700; color:#f8fafc; line-height:1.25;">
                              ${ag.name}
                            </div>
                          </div>
                          <span class="sc-tech-pill" style="border-color:${dept.color}66; color:${dept.color}; font-weight:700; font-size:12px;">${ag.badge}</span>
                        </div>

                        <p style="font-size:14px; color:#cbd5e1; line-height:1.56; margin-bottom:14px;">${ag.shortDesc}</p>

                        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07); border-radius:12px; padding:12px 14px; margin-bottom:14px; display:flex; flex-direction:column; gap:8px;">
                          <div style="display:grid; grid-template-columns:88px 1fr; gap:4px 8px; font-size:12.5px; align-items:baseline;">
                            <span style="font-weight:700; color:#94a3b8; text-transform:uppercase; font-size:11px;">SOLVER</span>
                            <span style="color:#f1f5f9; font-family:var(--font-mono); font-size:12px;">${ag.solverStack || ''}</span>
                          </div>
                          <div style="display:grid; grid-template-columns:88px 1fr; gap:4px 8px; font-size:12.5px; align-items:baseline;">
                            <span style="font-weight:700; color:#94a3b8; text-transform:uppercase; font-size:11px;">WRITE-BACK</span>
                            <span style="color:#a7f3d0; font-family:var(--font-mono); font-size:12px;">${ag.apiWriteback || ''}</span>
                          </div>
                          <div style="display:grid; grid-template-columns:88px 1fr; gap:4px 8px; font-size:12.5px; align-items:baseline;">
                            <span style="font-weight:700; color:#94a3b8; text-transform:uppercase; font-size:11px;">A2A SWARM</span>
                            <span style="color:#cbd5e1; font-size:12px;">${(ag.subAgents || []).map(sa => `<strong style="color:#f8fafc;">${sa.name}</strong>`).join(' · ')}</span>
                          </div>
                        </div>
                      </div>

                      <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.08);">
                        <button type="button" class="switch-pill" style="border-color:${dept.color}55; color:${dept.color}; font-size:13px; font-weight:600;" onclick="openAgentBlueprintPage('${ag.id}', true, event)">
                          Technical Blueprint &rarr;
                        </button>
                        <button type="button" style="font-size:12.5px; font-weight:600; color:#94a3b8;" onclick="openAgentPage('${ag.id}', true, event)">
                          Executive Pitch ↗
                        </button>
                      </div>
                    </div>
                  `;
                }).join('')}
              </div>
            </div>
          `;
          }).join('')}
          ` : ''}
        </div>
      `;

      hydrateAssets();
      showActivePage('pageArchitecture');
    }

    /* =========================================================================
       PAGE 7: THE PERIODIC TABLE OF AGENTS (CLEAN 2-COLUMN + RIGHT SIDEBAR + EXPAND)
       ========================================================================= */
    const PERIODIC_AGENT_META = {
      // 01 · Plan (Demand & S&OP)
      demand_sensing_agent:            { code: '101', sym: 'Pc', short: 'PulseCast',       group: 'demand_sop',          layer: 'BigQuery ML + TimesFM', layerColor: '#10b981', trigger: 'Scheduled',         trigIcon: '⏱️' },
      sop_scenario_weaver:             { code: '102', sym: 'Sy', short: 'Synapse S&OP',    group: 'demand_sop',          layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Human-in-the-loop', trigIcon: '🛡️' },
      promo_lift_simulator:            { code: '103', sym: 'Eq', short: 'ElasticityIQ',    group: 'demand_sop',          layer: 'BigQuery ML + TimesFM', layerColor: '#10b981', trigger: 'Chat-Initiated',    trigIcon: '💬' },
      cpfr_sync_agent:                 { code: '104', sym: 'Cs', short: 'ChannelSync',     group: 'demand_sop',          layer: 'Vertex AI ADK + A2A',   layerColor: '#3b82f6', trigger: 'Event-Driven',      trigIcon: '⚡' },
      // 02 · Source (Procurement & Risk)
      rfq_should_cost_agent:           { code: '201', sym: 'Sp', short: 'SourcePulse',     group: 'sourcing_procurement',       layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Chat-Initiated',    trigIcon: '💬' },
      tier_n_risk_sentinel:            { code: '202', sym: 'Nx', short: 'NexusShield',     group: 'sourcing_procurement',       layer: 'Spanner Graph + AI',    layerColor: '#a855f7', trigger: 'Event-Driven',      trigIcon: '⚡' },
      tariff_esg_agent:                { code: '203', sym: 'Cg', short: 'ClauseGuard',     group: 'sourcing_procurement',       layer: 'Vertex AI ADK + A2A',   layerColor: '#3b82f6', trigger: 'Scheduled',         trigIcon: '⏱️' },
      supplier_quality_sentinel:       { code: '204', sym: 'Qs', short: 'QualiShield',     group: 'sourcing_procurement',       layer: 'Vertex AI ADK + A2A',   layerColor: '#3b82f6', trigger: 'Event-Driven',      trigIcon: '⚡' },
      // 03 · Make (Manufacturing & OEE)
      line_schedule_optimizer:         { code: '301', sym: 'Cm', short: 'ChronosMake',     group: 'manufacturing_prod',  layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Event-Driven',      trigIcon: '⚡' },
      predictive_oee_sentinel:         { code: '302', sym: 'Sg', short: 'SpindleGuard',    group: 'manufacturing_prod',  layer: 'BigQuery ML + TimesFM', layerColor: '#10b981', trigger: 'Event-Driven',      trigIcon: '⚡' },
      inline_yield_guardian:           { code: '303', sym: 'Yv', short: 'YieldVision',     group: 'manufacturing_prod',  layer: 'Vertex AI ADK + A2A',   layerColor: '#3b82f6', trigger: 'Event-Driven',      trigIcon: '⚡' },
      eco_cutover_orchestrator:        { code: '304', sym: 'Ch', short: 'ChangeSync',      group: 'manufacturing_prod',  layer: 'Spanner Graph + AI',    layerColor: '#a855f7', trigger: 'Human-in-the-loop', trigIcon: '🛡️' },
      // 04 · Fulfill (3D WMS, MEIO & Cross-Dock)
      meio_safety_stock_agent:         { code: '401', sym: 'Ef', short: 'EchelonFlow',     group: 'inventory_meio', layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Scheduled',         trigIcon: '⏱️' },
      warehouse_slotting_agent:        { code: '501', sym: 'Sm', short: 'SlotMaster 3D',   group: 'warehousing_qa', layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Scheduled',         trigIcon: '⏱️' },
      atp_order_promising_agent:       { code: '402', sym: 'Pg', short: 'PromiseGuard',    group: 'inventory_meio', layer: 'Spanner Graph + AI',    layerColor: '#a855f7', trigger: 'Event-Driven',      trigIcon: '⚡' },
      yard_dock_sequencer:             { code: '502', sym: 'Yp', short: 'YardPulse',       group: 'warehousing_qa', layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Event-Driven',      trigIcon: '⚡' },
      crossdock_transfer_orchestrator: { code: '503', sym: 'Xd', short: 'CrossDockFlow',   group: 'warehousing_qa', layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Event-Driven',      trigIcon: '⚡' },
      // 05 · Deliver (Multi-Modal Ship, Air, Rail & Road)
      load_consolidation_agent:        { code: '501', sym: 'Cb', short: 'CubeMaster 3D',   group: 'logistics_fleet',     layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Event-Driven',      trigIcon: '⚡' },
      fleetflow_dispatch:              { code: '601', sym: 'Ff', short: 'FleetFlow Maps',  group: 'logistics_fleet',    layer: 'OR-Tools + Google Maps', layerColor: '#f59e0b', trigger: 'Event-Driven',      trigIcon: '⚡' },
      // 07 · TM&D (Trade Marketing & Distribution Last-Mile)
      field_beat_distributor_sync_agent: { code: '701', sym: 'Bs', short: 'BeatSync FSO', group: 'trade_mkt_dist', layer: 'OR-Tools + Google Maps', layerColor: '#f59e0b', trigger: 'Event-Driven',      trigIcon: '⚡' },
      planogram_merchandising_vision_auditor: { code: '702', sym: 'Sv', short: 'ShelfVision IR', group: 'trade_mkt_dist', layer: 'Gemini 3.8 Flash Vision', layerColor: '#3b82f6', trigger: 'Event-Driven',      trigIcon: '⚡' },
      trade_scheme_claims_reconciler: { code: '703', sym: 'Sg', short: 'SchemeGuard', group: 'trade_mkt_dist', layer: 'BigQuery + Vertex ADK', layerColor: '#10b981', trigger: 'Scheduled',         trigIcon: '⏱️' },
      port_drayage_orchestrator:       { code: '503', sym: 'Pw', short: 'PortWatch Sea',   group: 'logistics_fleet',     layer: 'Spanner Graph + AI',    layerColor: '#a855f7', trigger: 'Event-Driven',      trigIcon: '⚡' },
      air_cargo_uld_optimizer:         { code: '504', sym: 'Af', short: 'AeroFreight Air', group: 'logistics_fleet',     layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Event-Driven',      trigIcon: '⚡' },
      intermodal_rail_linehaul_agent:  { code: '505', sym: 'Ir', short: 'IntermodalSync',  group: 'logistics_fleet',     layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Scheduled',         trigIcon: '⏱️' },
      multimodal_mode_shift_agent:     { code: '506', sym: 'Ms', short: 'ModalShift',      group: 'logistics_fleet',     layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Human-in-the-loop', trigIcon: '🛡️' },
      freight_control_tower:           { code: '507', sym: 'St', short: 'SentinelMove',    group: 'logistics_fleet',     layer: 'Vertex AI ADK + A2A',   layerColor: '#3b82f6', trigger: 'Event-Driven',      trigIcon: '⚡' },
      // 06 · Return & Enable (OTIF, RMA & ESG)
      otif_penalty_shield:             { code: '601', sym: 'Ot', short: 'OTIFShield',      group: 'reverse_risk_esg',     layer: 'Vertex AI ADK + A2A',   layerColor: '#3b82f6', trigger: 'Event-Driven',      trigIcon: '⚡' },
      reverse_rma_optimizer:           { code: '602', sym: 'Rl', short: 'ReturnLoop RMA',  group: 'reverse_risk_esg',     layer: 'Vertex AI ADK + A2A',   layerColor: '#3b82f6', trigger: 'Event-Driven',      trigIcon: '⚡' },
      carbon_scope3_ledger:            { code: '603', sym: 'Ec', short: 'EcoChain CO2e',   group: 'reverse_risk_esg',     layer: 'BigQuery ML + TimesFM', layerColor: '#10b981', trigger: 'Scheduled',         trigIcon: '⏱️' },
      network_twin_architect:          { code: '403', sym: 'Td', short: 'TwinDesign',      group: 'inventory_meio',     layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Human-in-the-loop', trigIcon: '🛡️' },
      // 00 · Universal Cross-Persona CSCO Core
      csco_control_tower_copilot:      { code: '001', sym: 'Ct', short: 'TowerMind',       group: 'universal_csco',      layer: 'Vertex AI ADK + A2A',   layerColor: '#3b82f6', trigger: 'Chat-Initiated',    trigIcon: '💬' },
      disruption_war_room_orchestrator:{ code: '002', sym: 'Sw', short: 'StormShield',     group: 'universal_csco',      layer: 'Spanner Graph + AI',    layerColor: '#a855f7', trigger: 'Event-Driven',      trigIcon: '⚡' },
      master_data_leadtime_steward:    { code: '003', sym: 'Dc', short: 'DataCleanse',     group: 'universal_csco',      layer: 'BigQuery ML + TimesFM', layerColor: '#10b981', trigger: 'Scheduled',         trigIcon: '⏱️' },
      working_capital_cash_bridge:     { code: '004', sym: 'Mb', short: 'MarginBridge',    group: 'universal_csco',      layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Human-in-the-loop', trigIcon: '🛡️' }
    };

    const PERIODIC_GROUPS = [
      { id: 'demand_sop',          shortTab: 'Plan (V1)',            title: '01 · PLAN — DEMAND PLANNING, SENSING & S&OP (V1)',          color: '#10b981', count: 4 },
      { id: 'sourcing_procurement', shortTab: 'Source (V2)',          title: '02 · SOURCE — STRATEGIC SOURCING & PROCUREMENT (V2)',        color: '#a142f4', count: 4 },
      { id: 'manufacturing_prod',  shortTab: 'Make (V3)',            title: '03 · MAKE — PRODUCTION PLANNING & MANUFACTURING (V3)',       color: '#3b82f6', count: 4 },
      { id: 'inventory_meio',      shortTab: 'Inventory (V4)',       title: '04 · INVENTORY — MULTI-ECHELON BUFFER & MEIO (V4)',          color: '#06b6d4', count: 3 },
      { id: 'warehousing_qa',      shortTab: 'Warehouse (V5)',       title: '05 · WAREHOUSING — INWARDING QA & INTRALOGISTICS (V5)',      color: '#00d2ff', count: 3 },
      { id: 'logistics_fleet',     shortTab: 'Logistics (V6)',       title: '06 · LOGISTICS — MULTI-MODAL FLEET & TRANSIT (V6)',          color: '#ff8c00', count: 7 },
      { id: 'trade_mkt_dist',      shortTab: 'TM&D (V7)',            title: '07 · TM&D — TRADE MARKETING & DISTRIBUTION LAST-MILE (V7)',   color: '#f59e0b', count: 3 },
      { id: 'reverse_risk_esg',    shortTab: 'Reverse & ESG (V8)',   title: '08 · REVERSE & RISK — CIRCULAR RMA, OTIF & ESG (V8)',        color: '#ec4899', count: 3 },
      { id: 'universal_csco',      shortTab: 'Universal Core',       title: '00 · UNIVERSAL CROSS-PERSONA CSCO CONTROL TOWER CORE',       color: '#38bdf8', count: 4 }
    ];

    let currentPeriodicFilter = 'all'; // 'all' | group.id | 'by_persona'
    let currentSelectedElementId = 'demand_sensing_agent';
    let currentExpandedInlineId = null;

    function handlePeriodicTileClick(agentId) {
      currentSelectedElementId = agentId;
      // Toggle smooth inline expansion drawer underneath the clicked domain row
      if (currentExpandedInlineId === agentId) {
        currentExpandedInlineId = null;
      } else {
        currentExpandedInlineId = agentId;
      }
      openPeriodicTablePage(currentPeriodicFilter, currentSelectedElementId, false);
    }

    function openPeriodicTablePage(filterGroup = 'all', selectedAgentId = null, pushState = true) {
      currentPeriodicFilter = filterGroup || 'all';
      if (selectedAgentId && AGENTS[selectedAgentId]) {
        currentSelectedElementId = selectedAgentId;
      }
      if (pushState) {
        history.pushState({ page: 'periodic', filter: currentPeriodicFilter, agentId: currentSelectedElementId }, '', '#periodic');
      }

      const selAg = AGENTS[currentSelectedElementId] || AGENTS['demand_sensing_agent'];
      const selMeta = PERIODIC_AGENT_META[selAg.id] || {
        code: '101', sym: 'Ai', short: selAg.name, group: selAg.deptId,
        layer: 'Vertex AI ADK + A2A', layerColor: '#3b82f6', trigger: 'Event-Driven', trigIcon: '⚡'
      };
      const selGrp = PERIODIC_GROUPS.find(g => g.id === selMeta.group) || PERIODIC_GROUPS[0];
      const selDept = selAg.isUniversal
        ? { id: 'universal_csco', name: 'Universal CSCO Core', scorBadge: '00 · CORE', color: '#38bdf8' }
        : (DEPARTMENTS[selAg.deptId] || { id: 'demand_sop', name: 'Plan', scorBadge: 'SCOR', color: selGrp.color });
      const selSell = getAgentSellingMeta(selAg, selDept);

      const renderInlineExpansionCard = (ag, meta, grpColor) => {
        const d = ag.isUniversal ? selDept : (DEPARTMENTS[ag.deptId] || selDept);
        const sell = getAgentSellingMeta(ag, d);
        return `
          <div class="pt-inline-expand" style="--exp-color:${grpColor};">
            <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:flex-start; gap:16px; padding-bottom:16px; border-bottom:1px solid rgba(255,255,255,0.1); margin-bottom:18px;">
              <div>
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
                  <span style="font-family:var(--font-mono); font-size:12px; font-weight:800; padding:3px 9px; border-radius:6px; background:${grpColor}22; border:1px solid ${grpColor}; color:#fff;">
                    A-${meta.code} · ${meta.sym}
                  </span>
                  <span class="pt-side-tag">${meta.layer}</span>
                  <span class="pt-side-tag">${meta.trigIcon} ${meta.trigger}</span>
                  <span class="pt-side-tag" style="color:#6ee7b7; border-color:rgba(16,185,129,0.4);">${ag.badge}</span>
                </div>
                <h3 style="font-family:var(--font-display); font-size:22px; font-weight:800; color:#ffffff;">
                  ${ag.name}
                </h3>
                <p style="font-size:15px; color:#cbd5e1; margin-top:4px; max-width:880px;">
                  ${ag.tagline || ag.shortDesc}
                </p>
              </div>
              <div style="display:flex; align-items:center; gap:8px;">
                <button type="button" class="switch-pill" style="background:${grpColor}; color:#041019; font-weight:700; border:none;" onclick="openAgentPage('${ag.id}', true, event)">
                  Open Agent Studio &rarr;
                </button>
                <button type="button" class="switch-pill" style="border-color:rgba(168,85,247,0.5); color:#e9d5ff;" onclick="openAgentBlueprintPage('${ag.id}', true, event)">
                  Blueprint Spec &rarr;
                </button>
                <button type="button" class="switch-pill" onclick="currentExpandedInlineId = null; openPeriodicTablePage('${currentPeriodicFilter}', '${ag.id}', false)">
                  ✕
                </button>
              </div>
            </div>

            <div style="display:grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap:16px; margin-bottom:16px;">
              <div style="padding:16px; border-radius:12px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08);">
                <div style="font-size:11.5px; font-weight:700; text-transform:uppercase; letter-spacing:0.07em; color:#fca5a5; margin-bottom:6px;">
                  Problem Solved
                </div>
                <p style="font-size:14px; color:#e2e8f0; line-height:1.58;">${ag.problem}</p>
              </div>
              <div style="padding:16px; border-radius:12px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08);">
                <div style="font-size:11.5px; font-weight:700; text-transform:uppercase; letter-spacing:0.07em; color:#7dd3fc; margin-bottom:6px;">
                  Agentic Solution &amp; Solver
                </div>
                <p style="font-size:14px; color:#e2e8f0; line-height:1.58;">${ag.solution}</p>
              </div>
              <div style="padding:16px; border-radius:12px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08);">
                <div style="font-size:11.5px; font-weight:700; text-transform:uppercase; letter-spacing:0.07em; color:#6ee7b7; margin-bottom:6px;">
                  Verified Outcome
                </div>
                <p style="font-size:14px; color:#e2e8f0; line-height:1.58;">${ag.outcome}</p>
              </div>
            </div>

            <div style="display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:12px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.08);">
              <div style="display:flex; flex-wrap:wrap; align-items:center; gap:8px;">
                <span style="font-size:12px; font-weight:700; color:#94a3b8; text-transform:uppercase;">Connected Personas:</span>
                ${sell.usedByPersonas.map(p => `
                  <button type="button" class="pt-side-tag" style="cursor:pointer; color:#fff;" onclick="openPersonaPage('${p.id}', true, event)">
                    ${p.icon} ${p.name} &rarr;
                  </button>
                `).join('')}
              </div>
              <div style="font-size:12.5px; color:#94a3b8;">
                Sub-Agents: ${(ag.subAgents || []).map(s => `<strong style="color:#cbd5e1;">${s.name}</strong>`).join(' · ')}
              </div>
            </div>
          </div>
        `;
      };

      // Build Left Column Sections (Either by 7 SCOR Domains or by 26 Personas)
      let leftColumnHtml = '';
      if (currentPeriodicFilter === 'by_persona') {
        leftColumnHtml = Object.values(PERSONAS).map((p, idx) => {
          const d = DEPARTMENTS[p.deptId] || { color: '#38bdf8', scorBadge: 'SCOR' };
          const pAgents = [...(p.agentIds || []), ...UNIVERSAL_AGENT_IDS].map(id => AGENTS[id]).filter(Boolean);
          const hasExpandedInRow = currentExpandedInlineId && p.agentIds && p.agentIds.includes(currentExpandedInlineId);
          const expAg = hasExpandedInRow ? AGENTS[currentExpandedInlineId] : null;
          const expMeta = expAg ? PERIODIC_AGENT_META[expAg.id] : null;

          return `
            <div class="pt-domain-section">
              <div class="pt-domain-heading" style="justify-content:space-between; flex-wrap:wrap;">
                <div style="display:flex; align-items:center; gap:9px; cursor:pointer;" onclick="openPersonaPage('${p.id}', true, event)">
                  <span class="pt-domain-swatch" style="--dom-color:${d.color};"></span>
                  <span style="color:#ffffff;">P${String(idx + 1).padStart(2, '0')} · ${p.name.toUpperCase()}</span>
                  <span class="pt-domain-count">${pAgents.length} agents · ${p.timeSaved}</span>
                </div>
                <button type="button" style="font-size:12px; color:${d.color}; font-weight:600;" onclick="openPersonaPage('${p.id}', true, event)">
                  View persona page &rarr;
                </button>
              </div>
              <div class="pt-tiles-row">
                ${pAgents.map(ag => {
                  const m = PERIODIC_AGENT_META[ag.id] || { code: '100', short: ag.name, layerColor: d.color, trigIcon: '⚡' };
                  const tileColor = ag.isUniversal ? '#38bdf8' : d.color;
                  const isSel = ag.id === selAg.id;
                  return `
                    <div class="pt-tile ${isSel ? 'active' : ''}"
                         style="--tile-color:${tileColor}; --dot-color:${m.layerColor};"
                         onclick="handlePeriodicTileClick('${ag.id}')">
                      <div class="pt-tile-top">
                        <span>${m.code}</span>
                        <span class="pt-tile-trig">${m.trigIcon}</span>
                      </div>
                      <div class="pt-tile-title">${m.short}</div>
                      <div class="pt-tile-dot"></div>
                    </div>
                  `;
                }).join('')}
              </div>
              ${expAg && expMeta ? renderInlineExpansionCard(expAg, expMeta, d.color) : ''}
            </div>
          `;
        }).join('');
      } else {
        const visibleGroups = PERIODIC_GROUPS.filter(g => currentPeriodicFilter === 'all' || g.id === currentPeriodicFilter);
        leftColumnHtml = visibleGroups.map(grp => {
          const grpAgents = Object.entries(PERIODIC_AGENT_META)
            .filter(([_, m]) => m.group === grp.id)
            .map(([aid, m]) => ({ ag: AGENTS[aid], m }))
            .filter(x => x.ag);
          const expandedItem = grpAgents.find(x => x.ag.id === currentExpandedInlineId);

          return `
            <div class="pt-domain-section">
              <div class="pt-domain-heading">
                <span class="pt-domain-swatch" style="--dom-color:${grp.color};"></span>
                <span>${grp.title}</span>
                <span class="pt-domain-count">${grpAgents.length}</span>
              </div>
              <div class="pt-tiles-row">
                ${grpAgents.map(({ ag, m }) => {
                  const isSel = ag.id === selAg.id;
                  return `
                    <div class="pt-tile ${isSel ? 'active' : ''}"
                         style="--tile-color:${grp.color}; --dot-color:${m.layerColor};"
                         onclick="handlePeriodicTileClick('${ag.id}')">
                      <div class="pt-tile-top">
                        <span>${m.code}</span>
                        <span class="pt-tile-trig" title="${m.trigger}">${m.trigIcon}</span>
                      </div>
                      <div class="pt-tile-title">${m.short}</div>
                      <div class="pt-tile-dot" title="${m.layer}"></div>
                    </div>
                  `;
                }).join('')}
              </div>
              ${expandedItem ? renderInlineExpansionCard(expandedItem.ag, expandedItem.m, grp.color) : ''}
            </div>
          `;
        }).join('');
      }

      const container = document.getElementById('periodicPageContent');
      container.innerHTML = `
        <div class="subpage-top-bar">
          <button type="button" class="back-btn" onclick="goHome()">
            <span>&larr;</span>
            <span>Back to Home &amp; CSCO Org Chart</span>
          </button>
          <div style="display:flex; flex-wrap:wrap; gap:10px; align-items:center;">
            <button type="button" class="switch-pill" style="border-color:rgba(16,185,129,0.45); color:#6ee7b7;" onclick="openMindMapPage('mindmap', null, null, true)">
              🧠 Switch to Neural Mind Map &rarr;
            </button>
          </div>
        </div>

        <!-- Clean, Minimal Header -->
        <div style="padding-bottom: 18px; border-bottom: 1px solid rgba(255,255,255,0.10); margin-bottom: 20px;">
          <h1 style="font-family:var(--font-display); font-size:clamp(30px, 3.2vw, 42px); font-weight:800; letter-spacing:-0.025em; color:#ffffff; margin-bottom:6px;">
            The Periodic Table of Agents
          </h1>
          <p style="font-size:15px; color:#94a3b8; line-height:1.6; max-width:960px;">
            Enterprise catalog of 32 autonomous AI agents across 7 SCOR domains and 26 personas. Click any tile to inspect solvers, ERP write-backs, and human-in-the-loop controls.
          </p>
        </div>

        <!-- Clean Pill Tabs -->
        <div class="pt-top-tabs">
          <button type="button" class="pt-tab-btn ${currentPeriodicFilter === 'all' ? 'active' : ''}"
                  onclick="currentExpandedInlineId = null; openPeriodicTablePage('all', '${selAg.id}', false)">
            <span>All Domains</span>
            <span class="pt-tab-count">32</span>
          </button>
          ${PERIODIC_GROUPS.map(g => `
            <button type="button" class="pt-tab-btn ${currentPeriodicFilter === g.id ? 'active' : ''}"
                    onclick="currentExpandedInlineId = null; openPeriodicTablePage('${g.id}', '${selAg.id}', false)">
              <span>${g.shortTab}</span>
              <span class="pt-tab-count">${g.count}</span>
            </button>
          `).join('')}
          <button type="button" class="pt-tab-btn ${currentPeriodicFilter === 'by_persona' ? 'active' : ''}"
                  onclick="currentExpandedInlineId = null; openPeriodicTablePage('by_persona', '${selAg.id}', false)">
            <span>By Persona</span>
            <span class="pt-tab-count">26</span>
          </button>
        </div>

        <!-- Subheader Row with Right Stat Badges -->
        <div class="pt-subheader-bar" style="margin-bottom:18px;">
          <div>
            <h2 style="font-family:var(--font-display); font-size:18px; font-weight:700; color:#e2e8f0; margin-bottom:0;">
              ${currentPeriodicFilter === 'by_persona'
                ? 'Persona-to-Agent Mapping (26 Supply Chain Roles)'
                : (currentPeriodicFilter === 'all'
                    ? 'All 7 SCOR Domains &amp; Universal Core'
                    : (PERIODIC_GROUPS.find(g => g.id === currentPeriodicFilter)?.title || 'Domain Agents'))}
            </h2>
          </div>
          <div class="pt-stat-badges">
            <div class="pt-stat-badge"><strong>32</strong>agents</div>
            <div class="pt-stat-badge"><strong>7</strong>domains</div>
            <div class="pt-stat-badge"><strong>26</strong>personas</div>
          </div>
        </div>

        <!-- Main 2-Column Layout: Left Horizontal Domain Rows + Right Sticky Inspector & Legend -->
        <div class="pt-main-layout">
          <div>
            ${leftColumnHtml}
          </div>

          <!-- Right Sticky Sidebar: Selected Tile Card + Legend -->
          <aside class="pt-sidebar">
            <div class="pt-side-card" style="border-top: 3px solid ${selGrp.color};">
              <div style="display:flex; align-items:flex-start; gap:14px; margin-bottom:14px;">
                <div class="pt-side-badge" style="background:${selGrp.color};">
                  ${selMeta.code}
                </div>
                <div>
                  <div style="font-family:var(--font-display); font-size:17px; font-weight:800; color:#ffffff; line-height:1.25;">
                    ${selMeta.short}
                  </div>
                  <div style="font-family:var(--font-mono); font-size:12px; color:#94a3b8; margin-top:3px;">
                    A-${selMeta.code} · ${selGrp.shortTab}
                  </div>
                </div>
              </div>

              <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:14px;">
                <span class="pt-side-tag">${selMeta.layer}</span>
                <span class="pt-side-tag">${selMeta.trigIcon} ${selMeta.trigger}</span>
                <span class="pt-side-tag" style="color:#6ee7b7; border-color:rgba(16,185,129,0.35);">${selAg.badge}</span>
              </div>

              <p style="font-size:13.5px; color:#cbd5e1; line-height:1.6; margin-bottom:14px;">
                ${selAg.shortDesc}
              </p>

              <div style="margin-bottom:16px;">
                <div style="font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.07em; color:#64748b; margin-bottom:6px;">
                  Used by Personas (${selSell.usedByPersonas.length})
                </div>
                <div style="display:flex; flex-wrap:wrap; gap:5px;">
                  ${selSell.usedByPersonas.slice(0, 4).map(p => `
                    <button type="button" class="pt-side-tag" style="cursor:pointer; font-size:11px;" onclick="openPersonaPage('${p.id}', true, event)">
                      ${p.icon} ${p.name}
                    </button>
                  `).join('')}
                </div>
              </div>

              <div style="display:flex; flex-direction:column; gap:8px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.08);">
                <button type="button" style="display:inline-flex; align-items:center; justify-content:space-between; font-size:13.5px; font-weight:700; color:#60a5fa;" onclick="openAgentPage('${selAg.id}', true, event)">
                  <span>View agent studio &rarr;</span>
                  <span style="font-size:11.5px; color:#94a3b8;">#agent/${selAg.id}</span>
                </button>
                <button type="button" style="display:inline-flex; align-items:center; justify-content:space-between; font-size:13px; font-weight:600; color:#c084fc;" onclick="openAgentBlueprintPage('${selAg.id}', true, event)">
                  <span>View high-code blueprint &rarr;</span>
                  <span style="font-size:11.5px; color:#94a3b8;">ADK / A2A</span>
                </button>
              </div>
            </div>

            <!-- Legend Box (LAYERS, TRIGGERS, DOMAINS) -->
            <div class="pt-legend-box">
              <div>
                <div class="pt-legend-title">LAYERS</div>
                <div class="pt-legend-list">
                  <div class="pt-legend-row">
                    <span style="display:inline-flex; align-items:center; gap:8px;"><span class="pt-tile-dot" style="--dot-color:#f59e0b;"></span>OR-Tools + Vertex ADK</span>
                  </div>
                  <div class="pt-legend-row">
                    <span style="display:inline-flex; align-items:center; gap:8px;"><span class="pt-tile-dot" style="--dot-color:#3b82f6;"></span>Vertex AI ADK + A2A</span>
                  </div>
                  <div class="pt-legend-row">
                    <span style="display:inline-flex; align-items:center; gap:8px;"><span class="pt-tile-dot" style="--dot-color:#10b981;"></span>BigQuery ML + TimesFM</span>
                  </div>
                  <div class="pt-legend-row">
                    <span style="display:inline-flex; align-items:center; gap:8px;"><span class="pt-tile-dot" style="--dot-color:#a855f7;"></span>Spanner Graph + AI</span>
                  </div>
                </div>
              </div>

              <div>
                <div class="pt-legend-title">TRIGGERS</div>
                <div class="pt-legend-list">
                  <div class="pt-legend-row"><span>⚡ Event-Driven</span></div>
                  <div class="pt-legend-row"><span>💬 Chat-Initiated</span></div>
                  <div class="pt-legend-row"><span>⏱️ Scheduled</span></div>
                  <div class="pt-legend-row"><span>🛡️ Human-in-the-loop</span></div>
                </div>
              </div>

              <div>
                <div class="pt-legend-title">DOMAINS</div>
                <div class="pt-legend-list">
                  ${PERIODIC_GROUPS.map(g => `
                    <div class="pt-legend-row" style="cursor:pointer;" onclick="currentExpandedInlineId = null; openPeriodicTablePage('${g.id}', '${selAg.id}', false)">
                      <span style="display:inline-flex; align-items:center; gap:8px;">
                        <span class="pt-domain-swatch" style="--dom-color:${g.color};"></span>
                        <span>${g.shortTab}</span>
                      </span>
                      <span style="color:#64748b; font-family:var(--font-mono); font-size:12px;">${g.count}</span>
                    </div>
                  `).join('')}
                </div>
              </div>
            </div>
          </aside>
        </div>
      `;

      hydrateAssets();
      showActivePage('pagePeriodic');
    }

    /* =========================================================================
       PAGE 8: CLEAN, PROGRESSIVE NEURAL MIND MAP & CLICK-PATH FLOWCHART
       ========================================================================= */
    let currentMindMapMode = 'mindmap'; // 'mindmap' | 'flowchart'
    let currentMindMapDeptId = 'demand_sop';
    let currentMindMapPersonaId = 'demand_planning_dir';
    let currentMindMapAgentId = 'demand_sensing_agent';
    let currentFlowStepIdx = 0;

    function selectMindMapDept(deptId) {
      currentMindMapDeptId = deptId;
      const d = DEPARTMENTS[deptId];
      if (d && d.personaIds && d.personaIds.length > 0) {
        currentMindMapPersonaId = d.personaIds[0];
        const p = PERSONAS[currentMindMapPersonaId];
        if (p && p.agentIds && p.agentIds.length > 0) {
          currentMindMapAgentId = p.agentIds[0];
        }
      }
      openMindMapPage('mindmap', currentMindMapDeptId, currentMindMapPersonaId, false);
    }

    function selectMindMapPersona(personaId) {
      currentMindMapPersonaId = personaId;
      const p = PERSONAS[personaId];
      if (p) {
        currentMindMapDeptId = p.deptId;
        if (p.agentIds && p.agentIds.length > 0) {
          currentMindMapAgentId = p.agentIds[0];
        }
      }
      openMindMapPage('mindmap', currentMindMapDeptId, currentMindMapPersonaId, false);
    }

    function selectMindMapAgent(agentId) {
      currentMindMapAgentId = agentId;
      openMindMapPage('mindmap', currentMindMapDeptId, currentMindMapPersonaId, false);
    }

    function openMindMapPage(mode = 'mindmap', deptId = null, personaId = null, pushState = true) {
      if (typeof personaId === 'boolean') {
        pushState = personaId;
        personaId = null;
      }
      if (mode === 'mindmap' || mode === 'flowchart') {
        currentMindMapMode = mode;
      }
      if (deptId && DEPARTMENTS[deptId]) {
        currentMindMapDeptId = deptId;
      }
      if (personaId && PERSONAS[personaId]) {
        currentMindMapPersonaId = personaId;
      }
      if (pushState) {
        history.pushState({ page: 'mindmap', mode: currentMindMapMode }, '', '#mindmap');
      }

      const activeDept = DEPARTMENTS[currentMindMapDeptId] || Object.values(DEPARTMENTS)[0];
      const deptPersonas = (activeDept.personaIds || []).map(pid => PERSONAS[pid]).filter(Boolean);
      const activePersona = PERSONAS[currentMindMapPersonaId] || deptPersonas[0] || Object.values(PERSONAS)[0];
      const personaDomainAgents = (activePersona.agentIds || []).map(aid => AGENTS[aid]).filter(Boolean);
      const personaUniversalAgents = UNIVERSAL_AGENT_IDS.map(uid => AGENTS[uid]).filter(Boolean);
      const allPersonaAgents = [...personaDomainAgents, ...personaUniversalAgents];
      const activeAgent = AGENTS[currentMindMapAgentId] || allPersonaAgents[0] || Object.values(AGENTS)[0];
      const activeAgentMeta = PERIODIC_AGENT_META[activeAgent.id] || { code: '101', sym: 'Ai', short: activeAgent.name, layer: 'Vertex AI ADK', trigger: 'Event-Driven', trigIcon: '⚡' };

      const flowSteps = [
        {
          num: '01',
          title: 'Full-Screen Hero Landing (#)',
          sub: '60fps Supply Chain Canvas & Thesis',
          color: '#38bdf8',
          whatOpens: '60fps kinetic supply chain canvas introducing the CSCO executive transformation thesis.',
          actionLabel: 'Open Hero Landing &rarr;',
          actionFn: "goHome()"
        },
        {
          num: '02',
          title: 'CSCO Org Chart (#orgChart)',
          sub: '6 SCOR Verticals + 4 Universal Core Agents',
          color: '#10b981',
          whatOpens: 'Interactive tree organizing the 6 SCOR verticals, 26 personas, and 4 cross-persona universal agents.',
          actionLabel: 'Open CSCO Org Chart &rarr;',
          actionFn: "goToOrgChart()"
        },
        {
          num: '03',
          title: 'Department Showcase Drawer',
          sub: 'Animated Genie Expansion on Vertical Click',
          color: '#a142f4',
          whatOpens: 'Expands vertical workflows comparing manual toil against agentic automation with direct persona routing.',
          actionLabel: 'Try on CSCO Org Chart &rarr;',
          actionFn: "goToOrgChart()"
        },
        {
          num: '04',
          title: 'Dedicated Persona Page (#persona/id)',
          sub: '26 Supply Chain Roles · Before vs. After Toil',
          color: '#00d2ff',
          whatOpens: 'Deep-dive role view with side-by-side toil schedules and mapped domain agents.',
          actionLabel: 'Open Sample Persona Page &rarr;',
          actionFn: "openPersonaPage('demand_planning_dir', true, event)"
        },
        {
          num: '05',
          title: 'Executive Agent Studio (#agent/id)',
          sub: '32 Agents · ROI Cards, Pitch & Live 3D CAD',
          color: '#ff8c00',
          whatOpens: 'Executive business case with verified ROI metrics, mathematical solvers, and interactive simulators.',
          actionLabel: 'Open Sample Agent Studio &rarr;',
          actionFn: "openAgentPage('load_consolidation_agent', true, event)"
        },
        {
          num: '06',
          title: 'High-Code Technical Blueprint (#blueprint/id)',
          sub: '5-Stage ADK Pipeline, 3 Sub-Agents & Solvers',
          color: '#ec4899',
          whatOpens: 'High-code ADK pipeline specification, A2A agent mesh, ERP write-back schemas, and solver constraints.',
          actionLabel: 'Open Sample Blueprint &rarr;',
          actionFn: "openAgentBlueprintPage('load_consolidation_agent', true, event)"
        }
      ];

      const activeFlowStep = flowSteps[currentFlowStepIdx] || flowSteps[0];

      const container = document.getElementById('mindMapPageContent');
      container.innerHTML = `
        <div class="subpage-top-bar">
          <button type="button" class="back-btn" onclick="goHome()">
            <span>&larr;</span>
            <span>Back to Home &amp; CSCO Org Chart</span>
          </button>
          <div style="display:flex; flex-wrap:wrap; gap:10px; align-items:center;">
            <button type="button" class="switch-pill" style="border-color:rgba(0,210,255,0.45); color:#7dd3fc;" onclick="openPeriodicTablePage('all', null, true)">
              🧪 Switch to Periodic Table &rarr;
            </button>
          </div>
        </div>

        <!-- Clean, Minimal Header -->
        <div style="padding-bottom: 18px; border-bottom: 1px solid rgba(255,255,255,0.10); margin-bottom: 20px;">
          <h1 style="font-family:var(--font-display); font-size:clamp(30px, 3.2vw, 42px); font-weight:800; letter-spacing:-0.025em; color:#ffffff; margin-bottom:6px;">
            Neural Mind Map &amp; Portal Flowchart
          </h1>
          <p style="font-size:15px; color:#94a3b8; line-height:1.6; max-width:960px;">
            End-to-end interactive topology mapping 6 SCOR domains, 26 personas, and 32 autonomous AI agents across the enterprise.
          </p>
        </div>

        <!-- Clean Pill Tabs to Switch Between Interactive Mind Map & Portal Click-Path Flowchart -->
        <div class="pt-top-tabs">
          <button type="button" class="pt-tab-btn ${currentMindMapMode === 'mindmap' ? 'active' : ''}"
                  onclick="openMindMapPage('mindmap', '${currentMindMapDeptId}', '${currentMindMapPersonaId}', false)">
            <span>🧠 Interactive Neural Mind Map</span>
            <span class="pt-tab-count">26 Personas &harr; 32 Agents</span>
          </button>
          <button type="button" class="pt-tab-btn ${currentMindMapMode === 'flowchart' ? 'active' : ''}"
                  onclick="openMindMapPage('flowchart', '${currentMindMapDeptId}', '${currentMindMapPersonaId}', false)">
            <span>🧭 Portal Navigation Flowchart ("What Opens When You Click")</span>
            <span class="pt-tab-count">6 Steps</span>
          </button>
        </div>

        ${currentMindMapMode === 'mindmap' ? `
          <!-- PROGRESSIVE 3-COLUMN CLICK-TO-EXPAND NEURAL MIND MAP + RIGHT SIDE INSPECTOR -->
          <div class="pt-main-layout">
            <div class="mm-progressive-grid" style="margin-bottom:0;">
              <!-- Column 1: 6 SCOR Domains -->
              <div class="mm-col-card">
                <div class="mm-col-header">1. Select SCOR Domain (6)</div>
                ${Object.values(DEPARTMENTS).map(d => {
                  const isAct = d.id === activeDept.id;
                  return `
                    <button type="button" class="mm-node-btn ${isAct ? 'active' : ''}"
                            style="--node-color:${d.color};"
                            onclick="selectMindMapDept('${d.id}')">
                      <div>
                        <div style="font-family:var(--font-mono); font-size:10.5px; font-weight:700; color:${d.color};">
                          ${d.scorBadge}
                        </div>
                        <div style="font-size:14px; font-weight:700; color:#ffffff; margin-top:2px;">
                          ${d.name}
                        </div>
                      </div>
                      <span style="font-family:var(--font-mono); font-size:11.5px; color:#94a3b8;">
                        ${d.personaIds.length} roles &rarr;
                      </span>
                    </button>
                  `;
                }).join('')}
              </div>

              <!-- Column 2: Personas in Selected Domain (Animated on Domain Click) -->
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
                        <div style="font-size:14px; font-weight:700; color:#ffffff;">
                          ${p.icon} ${p.name}
                        </div>
                        <div style="font-size:12px; color:#94a3b8; margin-top:2px;">
                          ${p.timeSaved || '-75% Manual Toil'}
                        </div>
                      </div>
                      <span style="font-family:var(--font-mono); font-size:11.5px; color:${activeDept.color};">
                        ${(p.agentIds || []).length + 4} agents &rarr;
                      </span>
                    </button>
                  `;
                }).join('')}

                <div style="margin-top:14px; padding:14px; border-radius:12px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);">
                  <div style="font-size:11px; font-weight:700; text-transform:uppercase; color:#94a3b8; margin-bottom:4px;">
                    Selected Persona Mandate
                  </div>
                  <p style="font-size:13px; color:#cbd5e1; line-height:1.55; margin-bottom:10px;">
                    ${activePersona.mandate}
                  </p>
                  <button type="button" style="font-size:12.5px; font-weight:700; color:${activeDept.color};" onclick="openPersonaPage('${activePersona.id}', true, event)">
                    Open ${activePersona.name} page &rarr;
                  </button>
                </div>
              </div>

              <!-- Column 3: Connected AI Agents for Selected Persona (Animated on Persona Click) -->
              <div class="mm-col-card" style="animation: ptExpandIn 0.32s var(--ease-spring) forwards;">
                <div class="mm-col-header" style="color:#7dd3fc;">
                  3. Connected AI Agents for ${activePersona.name}
                </div>

                <div style="font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:${activeDept.color}; margin-bottom:8px;">
                  Domain-Specific Agents (${personaDomainAgents.length})
                </div>
                ${personaDomainAgents.map(ag => {
                  const m = PERIODIC_AGENT_META[ag.id] || { code: '101', short: ag.name, trigIcon: '⚡' };
                  const isAct = ag.id === activeAgent.id;
                  return `
                    <button type="button" class="mm-node-btn ${isAct ? 'active' : ''}"
                            style="--node-color:${activeDept.color};"
                            onclick="selectMindMapAgent('${ag.id}')">
                      <div>
                        <div style="display:flex; align-items:center; gap:6px;">
                          <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:${activeDept.color};">A-${m.code}</span>
                          <span style="font-size:14px; font-weight:700; color:#ffffff;">${m.short}</span>
                        </div>
                        <div style="font-size:12px; color:#94a3b8; margin-top:2px;">${ag.badge}</div>
                      </div>
                      <span style="font-size:12px; color:#cbd5e1;">Inspect &rarr;</span>
                    </button>
                  `;
                }).join('')}

                <div style="font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#38bdf8; margin:16px 0 8px;">
                  Universal Cross-Persona Core Agents (4)
                </div>
                ${personaUniversalAgents.map(ag => {
                  const m = PERIODIC_AGENT_META[ag.id] || { code: '001', short: ag.name, trigIcon: '💬' };
                  const isAct = ag.id === activeAgent.id;
                  return `
                    <button type="button" class="mm-node-btn ${isAct ? 'active' : ''}"
                            style="--node-color:#38bdf8;"
                            onclick="selectMindMapAgent('${ag.id}')">
                      <div>
                        <div style="display:flex; align-items:center; gap:6px;">
                          <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:#38bdf8;">A-${m.code}</span>
                          <span style="font-size:13.5px; font-weight:700; color:#ffffff;">${m.short}</span>
                        </div>
                        <div style="font-size:11.5px; color:#94a3b8; margin-top:2px;">${ag.badge}</div>
                      </div>
                      <span style="font-size:12px; color:#cbd5e1;">Inspect &rarr;</span>
                    </button>
                  `;
                }).join('')}
              </div>
            </div>

            <!-- Right Sticky Sidebar: Neural Connection & Problem Inspector -->
            <aside class="pt-sidebar">
              <div class="pt-side-card" style="border-top: 3px solid ${activeAgent.isUniversal ? '#38bdf8' : activeDept.color};">
                <div style="font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#94a3b8; margin-bottom:10px;">
                  Neural Connection Inspector
                </div>

                <div style="display:flex; align-items:flex-start; gap:12px; margin-bottom:14px;">
                  <div class="pt-side-badge" style="background:${activeAgent.isUniversal ? '#38bdf8' : activeDept.color};">
                    ${activeAgentMeta.code}
                  </div>
                  <div>
                    <div style="font-family:var(--font-display); font-size:17px; font-weight:800; color:#ffffff; line-height:1.25;">
                      ${activeAgent.name}
                    </div>
                    <div style="font-size:12.5px; color:#94a3b8; margin-top:3px;">
                      Connected to <strong style="color:#fff;">${activePersona.name}</strong>
                    </div>
                  </div>
                </div>

                <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:16px;">
                  <span class="pt-side-tag">${activeAgentMeta.layer}</span>
                  <span class="pt-side-tag" style="color:#6ee7b7; border-color:rgba(16,185,129,0.35);">${activeAgent.badge}</span>
                </div>

                <div style="padding:14px; border-radius:12px; background:rgba(239,68,68,0.07); border:1px solid rgba(239,68,68,0.22); margin-bottom:12px;">
                  <div style="font-size:11px; font-weight:700; text-transform:uppercase; color:#fca5a5; margin-bottom:4px;">
                    Problem Solved
                  </div>
                  <p style="font-size:13px; color:#e2e8f0; line-height:1.55;">
                    ${activeAgent.problem}
                  </p>
                </div>

                <div style="padding:14px; border-radius:12px; background:rgba(16,185,129,0.07); border:1px solid rgba(16,185,129,0.22); margin-bottom:16px;">
                  <div style="font-size:11px; font-weight:700; text-transform:uppercase; color:#6ee7b7; margin-bottom:4px;">
                    How It Works &amp; Outcome
                  </div>
                  <p style="font-size:13px; color:#e2e8f0; line-height:1.55;">
                    ${activeAgent.solution} ${activeAgent.outcome}
                  </p>
                </div>

                <div style="display:flex; flex-direction:column; gap:8px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.08);">
                  <button type="button" style="display:inline-flex; align-items:center; justify-content:space-between; font-size:13.5px; font-weight:700; color:#60a5fa;" onclick="openAgentPage('${activeAgent.id}', true, event)">
                    <span>View agent studio &rarr;</span>
                    <span style="font-size:11.5px; color:#94a3b8;">#agent/${activeAgent.id}</span>
                  </button>
                  <button type="button" style="display:inline-flex; align-items:center; justify-content:space-between; font-size:13px; font-weight:600; color:#34d399;" onclick="openPersonaPage('${activePersona.id}', true, event)">
                    <span>View persona page &rarr;</span>
                    <span style="font-size:11.5px; color:#94a3b8;">#persona/${activePersona.id}</span>
                  </button>
                  <button type="button" style="display:inline-flex; align-items:center; justify-content:space-between; font-size:13px; font-weight:600; color:#c084fc;" onclick="openAgentBlueprintPage('${activeAgent.id}', true, event)">
                    <span>View high-code blueprint &rarr;</span>
                    <span style="font-size:11.5px; color:#94a3b8;">ADK / A2A</span>
                  </button>
                </div>
              </div>
            </aside>
          </div>
        ` : `
          <!-- TAB 2: CLEAN, SPACIOUS 6-STEP PORTAL NAVIGATION FLOWCHART -->
          <div class="pt-main-layout">
            <div>
              <div class="mm-flow-cards">
                ${flowSteps.map((st, idx) => `
                  <div class="mm-flow-card ${idx === currentFlowStepIdx ? 'active' : ''}"
                       style="--fc-color:${st.color};"
                       onclick="currentFlowStepIdx = ${idx}; openMindMapPage('flowchart', '${currentMindMapDeptId}', '${currentMindMapPersonaId}', false)">
                    <div style="font-family:var(--font-mono); font-size:11.5px; font-weight:800; color:${st.color}; margin-bottom:6px;">
                      STEP ${st.num}
                    </div>
                    <div style="font-family:var(--font-display); font-size:17px; font-weight:800; color:#ffffff; margin-bottom:4px;">
                      ${st.title}
                    </div>
                    <div style="font-size:13px; color:#94a3b8; margin-bottom:14px;">
                      ${st.sub}
                    </div>
                    <div style="font-size:12.5px; font-weight:600; color:${st.color};">
                      Click to inspect step &rarr;
                    </div>
                  </div>
                `).join('')}
              </div>

              <!-- Smooth Animated Expansion Card for Selected Flowchart Step -->
              <div class="pt-inline-expand" style="--exp-color:${activeFlowStep.color};">
                <div style="font-family:var(--font-mono); font-size:12px; font-weight:800; color:${activeFlowStep.color}; margin-bottom:6px;">
                  STEP ${activeFlowStep.num} · WHAT OPENS WHEN YOU CLICK
                </div>
                <h3 style="font-family:var(--font-display); font-size:24px; font-weight:800; color:#ffffff; margin-bottom:10px;">
                  ${activeFlowStep.title}
                </h3>
                <p style="font-size:15.5px; color:#cbd5e1; line-height:1.68; margin-bottom:18px; max-width:860px;">
                  ${activeFlowStep.whatOpens}
                </p>
                <button type="button" class="switch-pill" style="background:${activeFlowStep.color}; color:#041019; font-weight:700; border:none;" onclick="${activeFlowStep.actionFn}">
                  ${activeFlowStep.actionLabel}
                </button>
              </div>
            </div>

            <aside class="pt-sidebar">
              <div class="pt-side-card" style="border-top: 3px solid ${activeFlowStep.color};">
                <div style="font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#94a3b8; margin-bottom:8px;">
                  Portal Architecture Summary
                </div>
                <div style="font-family:var(--font-display); font-size:18px; font-weight:800; color:#ffffff; margin-bottom:10px;">
                  Progressive Drill-Down Flow
                </div>
                <p style="font-size:13.5px; color:#cbd5e1; line-height:1.62; margin-bottom:14px;">
                  Designed so executives and engineers never face a wall of text: start at the CSCO Org Chart, expand 1 SCOR vertical at a time, open a Persona's daily workflow, and launch an Agent's live CAD studio or ADK blueprint.
                </p>
                <div class="pt-legend-list" style="padding-top:10px; border-top:1px solid rgba(255,255,255,0.08);">
                  <div class="pt-legend-row"><span>SCOR Verticals</span><strong style="color:#fff;">6</strong></div>
                  <div class="pt-legend-row"><span>Supply Chain Personas</span><strong style="color:#fff;">26</strong></div>
                  <div class="pt-legend-row"><span>AI Agent Studios</span><strong style="color:#fff;">32</strong></div>
                  <div class="pt-legend-row"><span>Collaborating Sub-Agents</span><strong style="color:#fff;">96</strong></div>
                  <div class="pt-legend-row"><span>End-to-End Value Chains</span><strong style="color:#fff;">4</strong></div>
                </div>
              </div>
            </aside>
          </div>
        `}
      `;

      hydrateAssets();
      showActivePage('pageMindMap');
    }

    /* =========================================================================
       MULTI-PAGE SWITCHING & HISTORY HANDLING
       ========================================================================= */
    function showActivePage(pageId) {
      document.querySelectorAll('#pageAgent video, #pageValueChain video').forEach(v => {
        try { v.pause(); } catch (e) {}
      });
      document.querySelectorAll('.page-view').forEach(el => el.classList.remove('active'));
      const target = document.getElementById(pageId);
      if (target) target.classList.add('active');
      window.scrollTo({ top: 0, behavior: 'instant' });
    }

    function goHome() {
      history.pushState({ page: 'home' }, '', '#');
      showActivePage('pageHome');
    }

    function goToOrgChart() {
      history.pushState({ page: 'home' }, '', '#orgChart');
      hydrateAssets();
      renderOrgChart();
      hydrateAssets();
      showActivePage('pageHome');
      setTimeout(() => {
        const el = document.getElementById('orgChartSection');
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 40);
    }

    window.addEventListener('popstate', () => {
      handleUrlHash();
    });

    function handleUrlHash() {
      const hash = window.location.hash.replace('#', '');
      if (hash === 'directory') {
        openPersonasDirectoryPage('all', '', false);
        return;
      }
      if (hash === 'architecture') {
        openArchitecturePage(false);
        return;
      }
      if (hash === 'periodic' || hash.startsWith('periodic/')) {
        const aid = hash.split('/')[1] || null;
        openPeriodicTablePage('all', aid, false);
        return;
      }
      if (hash === 'mindmap' || hash.startsWith('mindmap/')) {
        const fid = hash.split('/')[1] || null;
        openMindMapPage('all', fid, false);
        return;
      }
      if (hash.startsWith('persona/')) {
        const pid = hash.split('/')[1];
        if (PERSONAS[pid]) {
          openPersonaPage(pid, false);
          return;
        }
      } else if (hash.startsWith('agent/')) {
        const aid = hash.split('/')[1];
        if (AGENTS[aid]) {
          openAgentPage(aid, false);
          return;
        }
      } else if (hash.startsWith('blueprint/')) {
        const bid = hash.split('/')[1];
        if (AGENTS[bid]) {
          openAgentBlueprintPage(bid, false);
          return;
        }
      } else if (hash.startsWith('valuechain/')) {
        const vcid = hash.split('/')[1];
        if (VALUE_CHAINS[vcid]) {
          openValueChainPage(vcid, false);
          return;
        }
      }
      showActivePage('pageHome');
      if (hash === 'orgChart') {
        setTimeout(() => {
          const el = document.getElementById('orgChartSection');
          if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 40);
      }
    }

    /* =========================================================================
       ENTERPRISE TWIN CLIENT-SIDE SWITCHER & MODAL CONTROLLER
       ========================================================================= */
    function openEnterpriseTwinModal() {
      const m = document.getElementById('enterpriseTwinModal');
      if (m) {
        m.style.display = 'flex';
        m.style.animation = 'ptExpandIn 0.28s cubic-bezier(0.22, 1, 0.36, 1) forwards';
      }
    }

    function closeEnterpriseTwinModal() {
      const m = document.getElementById('enterpriseTwinModal');
      if (m) m.style.display = 'none';
    }

    let BASELINE_PERSONAS = null;
    let BASELINE_AGENTS = null;
    let CURRENT_TWIN = null;

    function quickSelectPreset(key) {
      const companyInput = document.getElementById('twinCompanyInput');
      const industrySelect = document.getElementById('twinIndustrySelect');
      const focusInput = document.getElementById('twinFocusInput');

      if (key === 'volkswagen') {
        if (companyInput) companyInput.value = 'Volkswagen Group';
        if (industrySelect) industrySelect.value = 'automotive';
        if (focusInput) focusInput.value = 'Wolfsburg & MEB gigafactories, PowerCo battery cells, JIS chassis line feeding';
      } else if (key === 'itc') {
        if (companyInput) companyInput.value = 'ITC Limited';
        if (industrySelect) industrySelect.value = 'cpg_retail';
        if (focusInput) focusInput.value = 'e-Choupal rural farmer procurement, FMCG ICML plants, mother godown CFAs';
      } else if (key === 'boeing') {
        if (companyInput) companyInput.value = 'The Boeing Company';
        if (industrySelect) industrySelect.value = 'aerospace';
        if (focusInput) focusInput.value = '737/787 commercial jetliners, long-lead titanium forgings, FAA cGMP compliance';
      } else if (key === 'caterpillar') {
        if (companyInput) companyInput.value = 'Caterpillar Inc.';
        if (industrySelect) industrySelect.value = 'aerospace';
        if (focusInput) focusInput.value = 'Heavy mining equipment, global dealer parts fulfillment, engine remanufacturing';
      } else if (key === 'shell') {
        if (companyInput) companyInput.value = 'Shell plc';
        if (industrySelect) industrySelect.value = 'oil_gas_energy';
        if (focusInput) focusInput.value = 'Integrated crude trading, Pernis refinery catalytic slates, LNG carrier charters';
      } else if (key === 'pfizer') {
        if (companyInput) companyInput.value = 'Pfizer Inc.';
        if (industrySelect) industrySelect.value = 'life_sciences_pharma';
        if (focusInput) focusInput.value = 'cGMP sterile injectables, mRNA vaccine platform, cold-chain distribution';
      } else if (key === 'unilever') {
        if (companyInput) companyInput.value = 'Unilever';
        if (industrySelect) industrySelect.value = 'cpg_retail';
        if (focusInput) focusInput.value = '400+ consumer goods brands, hyper-local demand forecasting, sustainable palm oil';
      }
      executeTwinGeneration();
    }

    function synthesizeClientSideTwin(company, industry, focus) {
      const clower = (company + ' ' + (focus || '')).toLowerCase();
      let ind = industry || 'automotive';
      if (ind === 'auto') {
        if (/fmcg|itc|agri|choupal|wheat|tobacco|retail|cpg|unilever|nestle|walmart|target|food|grocer/.test(clower)) {
          ind = 'fmcg_agribusiness';
        } else if (/boeing|airbus|plane|aero|defense|flight|titanium/.test(clower)) {
          ind = 'aerospace_defense';
        } else if (/caterpillar|cat\b|machin|mining|excavator|deere|komatsu|heavy/.test(clower)) {
          ind = 'heavy_machinery';
        } else if (/auto|car|vehicle|bmw|volkswagen|vw|tesla|ford|toyota|audi|mercedes|chassis|engine/.test(clower)) {
          ind = 'automotive';
        } else if (/oil|gas|energy|shell|bp|chevron|exxon|aramco|petro|refin|pipeline/.test(clower)) {
          ind = 'oil_gas_energy';
        } else if (/pharma|health|bio|pfizer|roche|novartis|merck|moderna|vaccine|drug/.test(clower)) {
          ind = 'life_sciences_pharma';
        } else {
          ind = 'automotive';
        }
      }

      let brandAccent = '#00d2ff';
      let execTitle = 'Chief Supply Chain Officer (CSCO), ' + company;
      let execThesis = focus || ('Orchestrating autonomous supply chain operations across ' + company + ' manufacturing plants and global distribution corridors.');

      if (ind === 'fmcg_agribusiness' || ind === 'cpg_retail') {
        brandAccent = '#10b981';
        execTitle = 'Executive Director, FMCG, Agri-Business & Supply Chain, ' + company;
        execThesis = focus || ('Synchronizing agricultural commodity sourcing, integrated manufacturing plants, and multi-echelon Carrying & Forwarding distribution for ' + company + '.');
      } else if (ind === 'aerospace_defense' || ind === 'aerospace') {
        brandAccent = '#0284c7';
        execTitle = 'Senior Vice President of Global Supply Chain & Manufacturing Operations, ' + company;
        execThesis = focus || ('Synchronizing multi-year supplier lead times, precision forgings, FAA airworthiness compliance, and final assembly lines for ' + company + '.');
      } else if (ind === 'heavy_machinery') {
        brandAccent = '#ffcd11';
        execTitle = 'Senior Vice President, Global Supply Chain & Customer Support Division, ' + company;
        execThesis = focus || ('Orchestrating heavy machinery assembly, circular remanufacturing, and guaranteed 24-hour emergency dealer parts availability for ' + company + '.');
      } else if (ind === 'automotive') {
        brandAccent = '#00d2ff';
        execTitle = 'Board Member for Production & Logistics, ' + company;
        execThesis = focus || ('Synchronizing gigafactories, battery cell supply, and just-in-sequence (JIS) line feeding for ' + company + ' vehicle platforms.');
      } else if (ind === 'oil_gas_energy') {
        brandAccent = '#fbbf24';
        execTitle = 'Executive Vice President of Global Supply Chain & Trading, ' + company;
        execThesis = focus || ('Optimizing integrated crude trading, pipeline hydraulic flows, refinery catalytic slates, and international bulk charters for ' + company + '.');
      } else if (ind === 'life_sciences_pharma') {
        brandAccent = '#38bdf8';
        execTitle = 'President, Global Supply (PGS) & Technical Operations, ' + company;
        execThesis = focus || ('Guaranteed zero-stockout patient fulfillment of sterile injectables, biologics platforms, and temperature-controlled distribution for ' + company + '.');
      }

      return {
        canonicalName: company,
        company_name: company,
        industryId: ind,
        brandAccent: brandAccent,
        brandSecondary: '#001e50',
        executiveTitle: execTitle,
        executiveThesis: execThesis,
        personaOverrides: {
          demand_planning_dir: {
            title: company + ' Head of Demand Sensing & Consensus Planning',
            role: 'Enterprise Demand Forecast Accuracy & Customer Fill-Rate Governance',
            summary: 'Directs enterprise demand forecasting across all ' + company + ' business units, channels, and product families.',
            manualToil: 'Manual spreadsheets and fragmented portal downloads causing weekly forecasting blindspots at ' + company + '.',
            agenticImpact: 'Daily demand sensing in TimesFM cutting forecast error by 24% for ' + company + '.'
          },
          mps_scheduling_lead: {
            title: company + ' Production Control & Master Scheduling Meister',
            role: 'Finite Capacity Scheduling & Plant Throughput Optimization',
            summary: 'Orchestrates manufacturing line schedules, machine changeovers, and material allocations across ' + company + ' plants.',
            manualToil: 'Manual shift scheduling frequently derailed by late material arrivals and equipment stops at ' + company + '.',
            agenticImpact: 'OR-Tools CP-SAT finite-capacity sequencing cutting changeover downtime by 30%.'
          },
          category_sourcing_mgr: {
            title: company + ' Head of Strategic Procurement & Direct Sourcing',
            role: 'Category Sourcing, Should-Cost Decomposition & Supplier Contracting',
            summary: 'Leads direct material procurement and supplier relationships for ' + company + ' manufacturing and operations.',
            manualToil: 'Normalizing inconsistent supplier quotes in Excel without bottom-up cost benchmarks.',
            agenticImpact: 'Parametric should-cost decomposition unlocking 7-10% in direct procurement savings.'
          },
          meio_inventory_mgr: {
            title: company + ' Multi-Echelon Inventory & Distribution Hub Stock Controller',
            role: 'Buffer Stock Optimization & Network Working Capital Tuning',
            summary: 'Controls inventory across factories, central warehouses, and regional distribution centers for ' + company + '.',
            manualToil: 'Hoarding excess safety stock at distribution centers to guard against transit delays.',
            agenticImpact: 'Stochastic MEIO solver dynamically rebalancing safety stocks across network hubs.'
          },
          fleet_dispatch_mgr: {
            title: company + ' Outbound Logistics & Carrier Fleet Dispatch Lead',
            role: 'Dedicated Fleet Linehaul & Regional Delivery Dispatch',
            summary: 'Manages dedicated linehaul carriers and delivery routes across ' + company + ' distribution corridors.',
            manualToil: 'Dispatchers manually assigning orders to trucks with high deadhead return miles.',
            agenticImpact: 'Google Maps Routes Preferred API cutting empty miles by 22%.'
          }
        },
        agentOverrides: {
          demand_sensing_agent: {
            systems: 'SAP S/4HANA · ' + company + ' Enterprise Data Lake · BigQuery · Vertex AI TimesFM',
            problemDetails: 'Disconnected regional spreadsheets, lack of customer sell-through visibility, and promotion cannibalization create costly stockouts and working capital build-ups for ' + company + '.',
            solutionDetails: 'PulseCast Demand Sensing Copilot ingests live point-of-sale data, distributor orders, and market signals into Vertex AI TimesFM with hierarchical SKU reconciliation for ' + company + '.',
            outcomeDetails: 'Cuts demand forecast error by 24% for ' + company + '; unlocks 18% in trapped safety stock working capital.',
            roiBadges: ['-24% Forecast Error', '18% Working Capital Freed', '45-Min S&OP Consensus', '99.2% Customer OTIF']
          },
          mps_finite_scheduler: {
            systems: 'Siemens Opcenter MES · SAP PP/DS · ' + company + ' Plant SCADA · OR-Tools CP-SAT',
            problemDetails: 'Frequent product recipe changes and uncoordinated material feeding cause excessive line idle time and backorders across ' + company + ' manufacturing facilities.',
            solutionDetails: 'OR-Tools CP-SAT finite-capacity scheduling solver optimizes sequence-dependent setups, grouping similar tooling and recipe families to maximize throughput.',
            outcomeDetails: 'Reduces plant changeover downtime by 32%; eliminates line starvation and cuts scrap by 28% for ' + company + '.',
            roiBadges: ['+14% Plant OEE', '-32% Changeover Delay', '-28% Scrap Waste', '100% Sequence Pegging']
          }
        }
      };
    }

    function applyBrowserTwin(twinData) {
      if (!twinData) return;
      CURRENT_TWIN = twinData;
      const cName = twinData.canonicalName || twinData.company_name || 'Enterprise';
      const execTitle = twinData.executiveTitle || ('Chief Supply Chain Officer (CSCO), ' + cName);
      const execThesis = twinData.executiveThesis || '';
      const brandAccent = twinData.brandAccent || '#00d2ff';
      const brandSec = twinData.brandSecondary || '#001e50';

      // 1. Snapshot baseline if not already done
      if (!BASELINE_PERSONAS) {
        BASELINE_PERSONAS = JSON.parse(JSON.stringify(PERSONAS));
      }
      if (!BASELINE_AGENTS) {
        BASELINE_AGENTS = JSON.parse(JSON.stringify(AGENTS));
      }

      // 2. Reset back to baseline first before applying overrides
      for (let pid in BASELINE_PERSONAS) {
        PERSONAS[pid] = JSON.parse(JSON.stringify(BASELINE_PERSONAS[pid]));
      }
      for (let aid in BASELINE_AGENTS) {
        AGENTS[aid] = JSON.parse(JSON.stringify(BASELINE_AGENTS[aid]));
      }

      // 3. Apply Persona Overrides from ADK Agent
      const pOverrides = twinData.personaOverrides || {};
      for (let pid in pOverrides) {
        if (PERSONAS[pid]) {
          const po = pOverrides[pid];
          if (po.title) PERSONAS[pid].name = po.title;
          if (po.role) PERSONAS[pid].role = po.role;
          if (po.summary) PERSONAS[pid].summary = po.summary;
          if (po.mandate && !po.summary) PERSONAS[pid].summary = po.mandate;
          if (po.manualToil && PERSONAS[pid].dayInLife && PERSONAS[pid].dayInLife.length > 0) {
            PERSONAS[pid].dayInLife[0].before = po.manualToil;
          }
          if (po.agenticImpact && PERSONAS[pid].dayInLife && PERSONAS[pid].dayInLife.length > 0) {
            PERSONAS[pid].dayInLife[0].after = po.agenticImpact;
          }
        }
      }

      // 4. Apply Agent Overrides from ADK Agent
      const aOverrides = twinData.agentOverrides || {};
      for (let aid in aOverrides) {
        if (AGENTS[aid]) {
          const ao = aOverrides[aid];
          if (ao.systems) AGENTS[aid].systems = ao.systems;
          if (ao.problemDetails) AGENTS[aid].problemDetails = ao.problemDetails;
          if (ao.solutionDetails) AGENTS[aid].solutionDetails = ao.solutionDetails;
          if (ao.outcomeDetails) AGENTS[aid].outcomeDetails = ao.outcomeDetails;
          if (ao.roiBadges) AGENTS[aid].roiBadges = ao.roiBadges;
        }
      }

      // 5. Update Header, Nav Badge, CSCO Card & Brand Colors
      document.documentElement.style.setProperty('--sc-cyan', brandAccent);
      const heroTitleEl = document.querySelector('.hero-title');
      const cscoBadgeEl = document.querySelector('.nav-csco-badge');
      const cscoTitleEl = document.querySelector('.csco-root-title');
      const cscoDescEl = document.querySelector('.csco-root-desc');

      if (cscoBadgeEl) {
        cscoBadgeEl.innerHTML = '<span style="color:' + brandAccent + '; font-weight:800;">' + cName + '</span> · Office of the CSCO';
      }
      if (heroTitleEl) {
        heroTitleEl.innerHTML = '<span class="g-text-gradient">' + cName + '</span><br/>Supply Chain Agentic Transformation';
      }
      if (cscoTitleEl) {
        cscoTitleEl.textContent = execTitle;
      }
      if (cscoDescEl && execThesis) {
        cscoDescEl.textContent = execThesis;
      }
      document.title = cName + ' · Supply Chain Agentic Transformation (' + execTitle + ')';

      // 6. Re-render Org Chart & Active Views
      renderOrgChart();

      // If active on a persona or agent page, refresh it live
      if (typeof lastPersonaId !== 'undefined' && lastPersonaId && PERSONAS[lastPersonaId]) {
        const pWrap = document.getElementById('personaPageContent');
        if (pWrap && pWrap.offsetParent !== null) {
          openPersonaPage(lastPersonaId, false);
        }
      }
      if (typeof lastAgentId !== 'undefined' && lastAgentId && AGENTS[lastAgentId]) {
        const aWrap = document.getElementById('agentPageContent');
        if (aWrap && aWrap.offsetParent !== null) {
          openAgentPage(lastAgentId, false);
        }
      }

      // 7. Save to localStorage
      try {
        localStorage.setItem('ACTIVE_ENTERPRISE_TWIN', JSON.stringify(twinData));
      } catch (e) {}
    }

    function executeTwinGeneration() {
      const companyInput = document.getElementById('twinCompanyInput');
      const industrySelect = document.getElementById('twinIndustrySelect');
      const focusInput = document.getElementById('twinFocusInput');
      const backendInput = document.getElementById('twinBackendUrlInput');
      const callBackendCheckbox = document.getElementById('twinCallBackendCheckbox');

      let company = (companyInput ? companyInput.value : '').trim();
      if (!company) {
        company = 'Enterprise Customer';
        if (companyInput) companyInput.value = company;
      }
      let industry = industrySelect ? industrySelect.value : 'auto';
      const focus = (focusInput ? focusInput.value : '').trim();
      const backendUrl = (backendInput ? backendInput.value : '').trim();
      const callBackend = callBackendCheckbox ? callBackendCheckbox.checked : false;

      // Auto-detect industry
      const clower = (company + ' ' + focus).toLowerCase();
      if (industry === 'auto') {
        if (/fmcg|itc|agri|choupal|wheat|tobacco|retail|cpg|unilever|nestle|walmart|target|food|grocer/.test(clower)) {
          industry = 'fmcg_agribusiness';
        } else if (/boeing|airbus|plane|aero|defense|flight|titanium/.test(clower)) {
          industry = 'aerospace_defense';
        } else if (/caterpillar|cat\b|machin|mining|excavator|deere|komatsu|heavy/.test(clower)) {
          industry = 'heavy_machinery';
        } else if (/auto|car|vehicle|bmw|volkswagen|vw|tesla|ford|toyota|audi|mercedes|chassis|engine/.test(clower)) {
          industry = 'automotive';
        } else if (/oil|gas|energy|shell|bp|chevron|exxon|aramco|petro|refin|pipeline/.test(clower)) {
          industry = 'oil_gas_energy';
        } else if (/pharma|health|bio|pfizer|roche|novartis|merck|moderna|vaccine|drug/.test(clower)) {
          industry = 'life_sciences_pharma';
        } else {
          industry = 'automotive';
        }
      }

      // Check if we have a pre-embedded twin or previously cached twin
      const slug = company.toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '');
      let twinData = (typeof EMBEDDED_TWINS !== 'undefined' && EMBEDDED_TWINS[slug]) ? EMBEDDED_TWINS[slug] : null;
      if (!twinData && typeof EMBEDDED_TWINS !== 'undefined') {
        for (let k in EMBEDDED_TWINS) {
          if (clower.includes(k) || k.includes(slug)) {
            twinData = EMBEDDED_TWINS[k];
            break;
          }
        }
      }

      // Show progress HUD
      const hud = document.getElementById('twinProgressHud');
      const hudStatus = document.getElementById('hudStatusText');
      const hudPercent = document.getElementById('hudPercentText');
      const hudBar = document.getElementById('hudProgressBar');
      const hudLog = document.getElementById('hudStepLog');

      if (hud) hud.style.display = 'block';

      const steps = [
        { pct: 20, status: '🤖 ADK Agent: Querying corporate profile & ecosystem for ' + company + '...', log: '[CompanyProfiler] Grounding operational hierarchy, plants & systems for ' + company + ' (' + industry + ')...' },
        { pct: 45, status: '🌐 Ecosystem Miner: Mapping Tier-1/Tier-2 supply networks & plant hubs...', log: '[EcosystemMiner] Identified key facilities, supplier nodes, and global trade corridors...' },
        { pct: 70, status: '👔 Career Persona Miner: Mining VP & Director titles for 26 SCOR roles...', log: '[PersonaMiner] Calibrated 26 SCOR personas with authentic ' + industry + ' domain lingo & toils...' },
        { pct: 90, status: '⚙️ Agent Spec Miner: Customizing operational details inside 32 AI agents...', log: '[AgentSpecMiner] Synthesized target ERP/MES data inputs, problem cards, and ROI metrics...' },
        { pct: 100, status: '✨ Complete: Digital Twin active for ' + company + '!', log: '[TwinReady] Live browser DOM morph successful. Portal now operates as ' + company + ' Supply Chain Twin.' }
      ];

      let currentStep = 0;
      if (hudLog) hudLog.innerHTML = '';

      const stepTimer = setInterval(() => {
        if (currentStep < steps.length) {
          const s = steps[currentStep];
          if (hudStatus) hudStatus.textContent = s.status;
          if (hudPercent) hudPercent.textContent = s.pct + '%';
          if (hudBar) hudBar.style.width = s.pct + '%';
          if (hudLog) {
            const line = document.createElement('div');
            line.style.marginTop = '4px';
            line.innerHTML = '<span style="color:#34d399;">✓</span> ' + s.log;
            hudLog.appendChild(line);
          }
          currentStep++;
        } else {
          clearInterval(stepTimer);

          // If we had no embedded twin, synthesize one dynamically in browser!
          if (!twinData) {
            twinData = synthesizeClientSideTwin(company, industry, focus);
          }

          // Apply the twin to the browser DOM
          applyBrowserTwin(twinData);

          // Decoupled backend trigger
          if (callBackend && backendUrl) {
            if (hudLog) {
              const apiLine = document.createElement('div');
              apiLine.style.marginTop = '6px';
              apiLine.style.color = '#38bdf8';
              apiLine.innerHTML = '<span>📡 Calling decoupled ADK backend agent (' + backendUrl + ')...</span>';
              hudLog.appendChild(apiLine);
            }
            fetch(backendUrl, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ company_name: company, industry: industry, focus: focus })
            })
            .then(res => res.json())
            .then(data => {
              if (hudLog) {
                const okLine = document.createElement('div');
                okLine.style.marginTop = '4px';
                okLine.style.color = '#10b981';
                okLine.innerHTML = '<span>✓ ADK Agent compiled persistent bundle to: <code>' + (data.output_dir || 'dist/') + '</code></span>';
                hudLog.appendChild(okLine);
              }
              if (data.profile) {
                applyBrowserTwin(data.profile);
              }
            })
            .catch(err => {
              console.warn('Backend call skipped or unreachable (browser twin is fully active):', err);
              if (hudLog) {
                const noteLine = document.createElement('div');
                noteLine.style.marginTop = '4px';
                noteLine.style.color = '#94a3b8';
                noteLine.innerHTML = '<span>ℹ️ Decoupled backend offline or skipped. In-browser synthesis active.</span>';
                hudLog.appendChild(noteLine);
              }
            });
          }

          // Add Explore button in HUD
          if (hudLog) {
            const exploreBtn = document.createElement('button');
            exploreBtn.type = 'button';
            exploreBtn.style.marginTop = '12px';
            exploreBtn.style.padding = '8px 18px';
            exploreBtn.style.borderRadius = '8px';
            exploreBtn.style.background = '#10b981';
            exploreBtn.style.color = '#040810';
            exploreBtn.style.fontWeight = '800';
            exploreBtn.style.fontSize = '13px';
            exploreBtn.style.border = 'none';
            exploreBtn.style.cursor = 'pointer';
            exploreBtn.textContent = '🚀 Explore ' + company + ' Org Chart & Agents ↗';
            exploreBtn.onclick = () => {
              closeEnterpriseTwinModal();
              goHome();
              setTimeout(() => {
                const el = document.getElementById('orgChartSection');
                if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
              }, 40);
            };
            hudLog.appendChild(exploreBtn);
          }
        }
      }, 240);
    }

    function switchClientTwin(clientKey) {
      if (clientKey === 'reset') {
        closeEnterpriseTwinModal();
        CURRENT_TWIN = null;
        try {
          localStorage.removeItem('ACTIVE_ENTERPRISE_TWIN');
        } catch (e) {}

        if (BASELINE_PERSONAS) {
          for (let pid in BASELINE_PERSONAS) {
            PERSONAS[pid] = JSON.parse(JSON.stringify(BASELINE_PERSONAS[pid]));
          }
        }
        if (BASELINE_AGENTS) {
          for (let aid in BASELINE_AGENTS) {
            AGENTS[aid] = JSON.parse(JSON.stringify(BASELINE_AGENTS[aid]));
          }
        }

        const heroTitleEl = document.querySelector('.hero-title');
        const cscoBadgeEl = document.querySelector('.nav-csco-badge');
        const cscoTitleEl = document.querySelector('.csco-root-title');
        const cscoDescEl = document.querySelector('.csco-root-desc');

        if (cscoBadgeEl) cscoBadgeEl.innerHTML = 'Office of the CSCO · Supply Chain';
        if (heroTitleEl) {
          heroTitleEl.innerHTML = 'Supply Chain &amp; Demand<br/><span class="g-text-gradient">Agentic Transformation</span>';
        }
        if (cscoTitleEl) cscoTitleEl.textContent = 'Chief Supply Chain Officer (CSCO)';
        if (cscoDescEl) cscoDescEl.textContent = 'The Office of the CSCO operates 6 SCOR-aligned departments spanning Factory → Ocean Ships → Air Cargo → Rail → Warehouses → Road Fleet.';
        document.documentElement.style.setProperty('--sc-cyan', '#00d2ff');
        document.title = 'Supply Chain & Demand · Agentic Transformation (Office of the CSCO)';

        renderOrgChart();
        goHome();
        return;
      }
      quickSelectPreset(clientKey);
    }

    document.addEventListener('DOMContentLoaded', () => {
      if (!BASELINE_PERSONAS) {
        BASELINE_PERSONAS = JSON.parse(JSON.stringify(PERSONAS));
      }
      if (!BASELINE_AGENTS) {
        BASELINE_AGENTS = JSON.parse(JSON.stringify(AGENTS));
      }

      hydrateAssets();
      initHeroSupplyChainCanvas();
      renderOrgChart();
      hydrateAssets();
      handleUrlHash();

      // Check if a twin was previously cached in localStorage
      try {
        const cachedStr = localStorage.getItem('ACTIVE_ENTERPRISE_TWIN');
        if (cachedStr) {
          const cached = JSON.parse(cachedStr);
          if (cached && (cached.canonicalName || cached.company_name)) {
            console.log('Restoring active enterprise twin from memory:', cached.canonicalName || cached.company_name);
            applyBrowserTwin(cached);
          }
        }
      } catch (e) {}
    });
  </script>
</body>
</html>
"""
    html = html.replace("__EMBEDDED_WEBP_BLOBS__", blobs_js)
    html = html.replace("__EMBEDDED_TWINS_JSON__", twins_js)
    html = html.replace("__EMBEDDED_DEPARTMENTS_JSON__", depts_js)
    html = html.replace("__EMBEDDED_PERSONAS_JSON__", personas_js)
    html = html.replace("__EMBEDDED_AGENTS_JSON__", agents_js)
    return html


def main() -> None:
    import shutil

    html = build_html()
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"Successfully wrote {OUT_HTML} ({len(html) // 1024} KB)")

    # Also generate standalone periodic_table.html and mind_map.html so they can be shared/opened directly
    periodic_html = html.replace(
        "handleUrlHash();",
        "if (!window.location.hash) { window.location.hash = '#periodic'; } handleUrlHash();",
    )
    periodic_path = OUT_HTML.parent / "periodic_table.html"
    periodic_path.write_text(periodic_html, encoding="utf-8")
    print(f"Successfully wrote {periodic_path} ({len(periodic_html) // 1024} KB)")

    mindmap_html = html.replace(
        "handleUrlHash();",
        "if (!window.location.hash) { window.location.hash = '#mindmap'; } handleUrlHash();",
    )
    mindmap_path = OUT_HTML.parent / "mind_map.html"
    mindmap_path.write_text(mindmap_html, encoding="utf-8")
    print(f"Successfully wrote {mindmap_path} ({len(mindmap_html) // 1024} KB)")

    # Automatically keep docs/ and zipline_dist/ synchronized
    for dest_dir_name in ["docs", "zipline_dist"]:
        dest_dir = OUT_HTML.parent / dest_dir_name
        if dest_dir.exists():
            (dest_dir / "index.html").write_text(html, encoding="utf-8")
            (dest_dir / "periodic_table.html").write_text(periodic_html, encoding="utf-8")
            (dest_dir / "mind_map.html").write_text(mindmap_html, encoding="utf-8")
            print(f"Synced {dest_dir_name}/ (index.html, periodic_table.html, mind_map.html)")

    # Synchronize scripts/build_site.py
    scripts_builder = OUT_HTML.parent / "scripts" / "build_site.py"
    if scripts_builder.parent.exists():
        shutil.copy2(pathlib.Path(__file__).resolve(), scripts_builder)
        print(f"Synced scripts/build_site.py with master generator")


if __name__ == "__main__":
    main()




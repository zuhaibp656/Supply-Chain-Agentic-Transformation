#!/usr/bin/env python3
"""Enhances Light Theme contrast & hover animations, restores concise Red/Green Persona Journey,
upgrades Agent Architecture Diagrams to a branching multi-stage workflow with Low-Code/Hybrid/High-Code
classification, and adds 1-click access to Personas & Agents from Pillars and Navbar."""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD_SITE = ROOT / "build_site.py"


ENHANCED_CSS_BLOCK = """    /* =========================================================================
       ENHANCED PERSONA JOURNEY (RED VS GREEN), BRANCHING WORKFLOW & HOVER POP
       ========================================================================= */
    .build-tier-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 11px;
      border-radius: 999px;
      font-size: 11.5px;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      white-space: nowrap;
    }

    .build-tier-lowcode {
      background: rgba(52, 168, 83, 0.15);
      color: #34a853;
      border: 1px solid rgba(52, 168, 83, 0.42);
    }

    .build-tier-hybrid {
      background: rgba(66, 133, 244, 0.15);
      color: #4285f4;
      border: 1px solid rgba(66, 133, 244, 0.42);
    }

    .build-tier-highcode {
      background: rgba(161, 66, 244, 0.15);
      color: #a142f4;
      border: 1px solid rgba(161, 66, 244, 0.42);
    }

    .showcase-emblem-box {
      width: 190px;
      height: 88px;
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
      padding: 26px 30px;
      border-radius: 20px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      margin-bottom: 28px;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.22);
    }

    .simple-arch-svg-wrap {
      border-radius: 16px;
      overflow: hidden;
      border: 1px solid var(--border-subtle);
      background: #070b14;
      padding: 14px;
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
      background: rgba(66, 133, 244, 0.14);
      border: 1px solid rgba(66, 133, 244, 0.40);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--g-blue);
      font-size: 24px;
      transition: transform 0.28s var(--ease-spring), background 0.25s ease;
    }

    .video-placeholder-stage:hover .video-placeholder-icon {
      transform: scale(1.1);
      background: rgba(66, 133, 244, 0.24);
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
      transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease !important;
    }

    .theme-toggle-btn:hover {
      border-color: var(--g-blue) !important;
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(66, 133, 244, 0.22);
    }

    /* Quick-Access Navbar Dropdowns for Pillars, Personas & Agents */
    .nav-quick-menu {
      position: absolute;
      top: calc(100% + 8px);
      right: 0;
      width: 340px;
      max-height: 440px;
      overflow-y: auto;
      padding: 10px;
      border-radius: 16px;
      background: rgba(11, 16, 28, 0.98);
      backdrop-filter: blur(20px);
      border: 1px solid var(--border-strong);
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.65);
      display: none;
      flex-direction: column;
      gap: 4px;
      z-index: 9999;
      animation: dropdownUnroll 0.22s var(--ease-spring) forwards;
    }

    .nav-dropdown-wrap:hover .nav-quick-menu {
      display: flex;
    }

    .nav-quick-group-title {
      font-size: 10.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding: 8px 10px 4px;
      color: var(--text-secondary);
      border-top: 1px solid var(--border-subtle);
      margin-top: 4px;
    }

    .nav-quick-group-title:first-child {
      border-top: none;
      margin-top: 0;
    }

    .nav-quick-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding: 8px 12px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 600;
      color: var(--text-primary);
      text-align: left;
      transition: background 0.18s ease, transform 0.18s ease, color 0.18s ease;
    }

    .nav-quick-item:hover {
      background: rgba(66, 133, 244, 0.16);
      color: #ffffff;
      transform: translateX(4px);
    }

    /* Strong Interactive Hover Pop-Up & Highlight Across All Cards */
    .dept-node,
    .persona-link-card,
    .catalog-card,
    .dir-persona-card,
    .schedule-row,
    .v-tab-btn {
      transition: transform 0.30s cubic-bezier(0.22, 1, 0.36, 1),
                  border-color 0.24s ease,
                  box-shadow 0.30s cubic-bezier(0.22, 1, 0.36, 1),
                  background 0.24s ease !important;
    }

    .dept-node {
      border-top: 4px solid var(--dept-accent, var(--g-blue)) !important;
    }

    .dept-node:hover,
    .dept-node.active {
      transform: translateY(-8px) scale(1.018) !important;
      border-color: var(--dept-accent, var(--g-blue)) !important;
      box-shadow: 0 20px 44px -8px rgba(0, 0, 0, 0.55), 0 0 0 1px var(--dept-accent, var(--g-blue)) !important;
    }

    .dept-anim-stage svg.dept-stage-svg {
      opacity: 0.92;
      filter: saturate(0.96);
      transition: transform 0.42s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.28s ease, filter 0.28s ease !important;
    }

    .dept-node:hover .dept-anim-stage svg.dept-stage-svg,
    .dept-node.active .dept-anim-stage svg.dept-stage-svg {
      opacity: 1 !important;
      transform: scale(1.12) !important;
      filter: saturate(1.12) contrast(1.04) !important;
    }

    .persona-link-card:hover,
    .catalog-card:hover,
    .dir-persona-card:hover {
      transform: translateY(-6px) scale(1.015) !important;
      border-color: var(--dept-accent, var(--g-blue)) !important;
    }

    .persona-link-card:hover .persona-open-arrow {
      transform: translateX(5px) scale(1.15);
    }

    /* =========================================================================
       VIBRANT GOOGLE CLOUD LIGHT THEME (TINTED CANVAS, CRISP CARDS, POP HOVERS)
       ========================================================================= */
    html[data-theme="light"],
    html[data-theme="light"] body {
      background: #f0f4fa;
      color: #202124;
    }

    html[data-theme="light"] .navbar {
      background: rgba(255, 255, 255, 0.94);
      border-bottom: 1px solid #d2e3fc;
      box-shadow: 0 2px 12px rgba(26, 115, 232, 0.08);
    }

    html[data-theme="light"] .nav-brand img.gemini-logo,
    html[data-theme="light"] .hero-logo-lockup img.gemini-hero {
      filter: invert(1) hue-rotate(180deg);
    }

    html[data-theme="light"] .nav-csco-badge {
      background: #e8f0fe;
      border-color: #d2e3fc;
      color: #1967d2;
      font-weight: 700;
    }

    html[data-theme="light"] .nav-pill-btn {
      color: #3c4043;
      font-weight: 600;
    }

    html[data-theme="light"] .nav-pill-btn:hover {
      background: #e8f0fe;
      color: #1a73e8;
      transform: translateY(-1px);
    }

    html[data-theme="light"] .nav-quick-menu {
      background: rgba(255, 255, 255, 0.98);
      border: 1px solid #d2e3fc;
      box-shadow: 0 18px 42px rgba(26, 115, 232, 0.16), 0 4px 12px rgba(60, 64, 67, 0.08);
    }

    html[data-theme="light"] .nav-quick-group-title {
      color: #5f6368;
      border-top-color: #e8eaed;
    }

    html[data-theme="light"] .nav-quick-item {
      color: #202124;
    }

    html[data-theme="light"] .nav-quick-item:hover {
      background: #e8f0fe;
      color: #1a73e8;
    }

    html[data-theme="light"] .hero-section {
      background: linear-gradient(180deg, #f5f8ff 0%, #eef3fc 100%);
      border-bottom: 1px solid #d2e3fc;
    }

    html[data-theme="light"] .hero-aurora-backdrop {
      background:
        radial-gradient(circle 580px at 16% 26%, rgba(66, 133, 244, 0.14), transparent 72%),
        radial-gradient(circle 600px at 84% 32%, rgba(52, 168, 83, 0.12), transparent 72%),
        radial-gradient(circle 520px at 22% 76%, rgba(251, 188, 4, 0.12), transparent 70%),
        radial-gradient(circle 560px at 82% 78%, rgba(161, 66, 244, 0.11), transparent 72%);
    }

    html[data-theme="light"] .hero-vignette {
      background:
        radial-gradient(ellipse 35% 40% at 50% 48%, rgba(245, 248, 255, 0.90) 0%, rgba(245, 248, 255, 0.62) 55%, rgba(245, 248, 255, 0.0) 100%),
        linear-gradient(180deg, rgba(245, 248, 255, 0.25) 0%, rgba(245, 248, 255, 0.0) 50%, rgba(240, 244, 250, 0.92) 100%);
    }

    html[data-theme="light"] .hero-logo-lockup {
      background: #ffffff;
      border: 1px solid #d2e3fc;
      box-shadow: 0 6px 20px rgba(26, 115, 232, 0.10);
    }

    html[data-theme="light"] .hero-title {
      color: #202124;
      text-shadow: none;
    }

    html[data-theme="light"] .hero-title .gradient-word {
      background: linear-gradient(92deg, #1a73e8 0%, #1e8e3e 52%, #e37400 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    html[data-theme="light"] .hero-subtitle {
      color: #3c4043;
      text-shadow: none;
    }

    html[data-theme="light"] .hero-cta-btn {
      background: #1a73e8;
      color: #ffffff;
      box-shadow: 0 6px 20px rgba(26, 115, 232, 0.28);
    }

    html[data-theme="light"] .hero-cta-btn:hover {
      background: #1557b0;
      box-shadow: 0 10px 26px rgba(26, 115, 232, 0.38);
      transform: translateY(-3px) scale(1.02);
    }

    html[data-theme="light"] .hero-cta-btn.secondary-hero-btn {
      background: #ffffff !important;
      color: #1a73e8 !important;
      border: 1.5px solid #aecbfa !important;
      box-shadow: 0 4px 12px rgba(26, 115, 232, 0.08) !important;
    }

    html[data-theme="light"] .hero-cta-btn.secondary-hero-btn:hover {
      background: #e8f0fe !important;
      border-color: #1a73e8 !important;
    }

    html[data-theme="light"] .section-title,
    html[data-theme="light"] .cfo-box-title,
    html[data-theme="light"] .dept-node-title,
    html[data-theme="light"] .showcase-dept-name,
    html[data-theme="light"] .persona-link-name,
    html[data-theme="light"] .persona-page-title,
    html[data-theme="light"] .agent-title,
    html[data-theme="light"] .block-title,
    html[data-theme="light"] .catalog-title,
    html[data-theme="light"] .task-title {
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
      color: #4b5563 !important;
    }

    html[data-theme="light"] .vertical-tabs-nav-bar {
      background: rgba(255, 255, 255, 0.94);
      border: 1px solid #d2e3fc;
      box-shadow: 0 8px 24px rgba(26, 115, 232, 0.08);
    }

    html[data-theme="light"] .v-tab-btn {
      background: #f8fafd;
      color: #4b5563;
      border: 1px solid #dce5f2;
    }

    html[data-theme="light"] .v-tab-btn .v-tab-title {
      color: #202124;
    }

    html[data-theme="light"] .v-tab-btn:hover {
      background: #ffffff;
      border-color: var(--v-accent, #1a73e8);
      transform: translateY(-3px);
      box-shadow: 0 8px 20px rgba(26, 115, 232, 0.14);
    }

    html[data-theme="light"] .v-tab-btn.active {
      background: #e8f0fe;
      border-color: var(--v-accent, #1a73e8);
      box-shadow: 0 6px 16px rgba(26, 115, 232, 0.16);
    }

    html[data-theme="light"] .cfo-box {
      background: linear-gradient(135deg, #ffffff 0%, #f4f8ff 100%);
      border: 2px solid #8ab4f8;
      box-shadow: 0 10px 28px rgba(26, 115, 232, 0.12);
    }

    html[data-theme="light"] .cfo-sc-emblem {
      background: #e8f0fe;
      border: 1px solid #aecbfa;
    }

    html[data-theme="light"] .dept-node {
      background: #ffffff;
      border: 1px solid #d5e1f2;
      border-top: 4px solid var(--dept-accent, #1a73e8) !important;
      box-shadow: 0 8px 22px rgba(26, 115, 232, 0.07), 0 2px 6px rgba(60, 64, 67, 0.04);
    }

    html[data-theme="light"] .dept-node:hover,
    html[data-theme="light"] .dept-node.active {
      background: #ffffff;
      border-color: var(--dept-accent, #1a73e8) !important;
      box-shadow: 0 20px 42px -6px rgba(26, 115, 232, 0.22), 0 0 0 1.5px var(--dept-accent, #1a73e8) !important;
    }

    html[data-theme="light"] .dept-anim-stage {
      background: linear-gradient(145deg, #eef4ff 0%, #f6f9fe 100%);
      border: 1px solid #d2e3fc;
    }

    html[data-theme="light"] .dept-node:hover .dept-anim-stage,
    html[data-theme="light"] .dept-node.active .dept-anim-stage {
      background: linear-gradient(145deg, #e4eeff 0%, #f0f6ff 100%);
      border-color: var(--dept-accent, #1a73e8);
    }

    html[data-theme="light"] .dept-anim-stage svg.dept-stage-svg {
      opacity: 0.94;
      filter: saturate(1.02) contrast(1.02);
    }

    html[data-theme="light"] .dept-node:hover .dept-anim-stage svg.dept-stage-svg,
    html[data-theme="light"] .dept-node.active .dept-anim-stage svg.dept-stage-svg {
      opacity: 1 !important;
      filter: saturate(1.18) contrast(1.06) !important;
    }

    html[data-theme="light"] .dept-anim-meta {
      background: rgba(255, 255, 255, 0.95);
      color: #1967d2;
      border: 1px solid #aecbfa;
      font-weight: 700;
    }

    html[data-theme="light"] .dept-showcase-box {
      background: #ffffff;
      border: 1.5px solid var(--dept-accent, #1a73e8);
      box-shadow: 0 16px 40px rgba(26, 115, 232, 0.14);
    }

    html[data-theme="light"] .showcase-visual-strip {
      background: #f4f8ff;
      border: 1px solid #d2e3fc;
    }

    html[data-theme="light"] .showcase-emblem-box {
      background: #e8f0fe;
      border: 1px solid #aecbfa;
    }

    html[data-theme="light"] .persona-link-card {
      background: #f8fafd;
      border: 1px solid #d5e1f2;
      border-left: 4px solid var(--dept-accent, #1a73e8);
      box-shadow: 0 3px 10px rgba(60, 64, 67, 0.05);
    }

    html[data-theme="light"] .persona-link-card:hover {
      background: #ffffff;
      border-color: var(--dept-accent, #1a73e8) !important;
      box-shadow: 0 14px 30px rgba(26, 115, 232, 0.18);
    }

    html[data-theme="light"] .persona-emoji {
      background: #e8f0fe;
      border: 1px solid #aecbfa;
    }

    html[data-theme="light"] .persona-header-card,
    html[data-theme="light"] .agent-hero-banner {
      background: linear-gradient(135deg, #ffffff 0%, #f4f8ff 100%);
      border: 1px solid #c6dafc;
      box-shadow: 0 8px 24px rgba(26, 115, 232, 0.08);
    }

    html[data-theme="light"] .persona-stat-highlight {
      background: #f8fafd;
      border: 1px solid #d2e3fc;
    }

    html[data-theme="light"] .persona-stat-label {
      color: #4b5563;
    }

    /* Light Theme Red vs Green Persona Journey Boxes */
    html[data-theme="light"] .shift-meter-card {
      background: #ffffff;
      border: 1px solid #d5e1f2;
      box-shadow: 0 4px 12px rgba(60, 64, 67, 0.05);
    }

    html[data-theme="light"] .shift-bar-track {
      background: #e8eaed;
    }

    html[data-theme="light"] .schedule-row {
      background: #ffffff;
      border: 1px solid #d5e1f2;
      box-shadow: 0 4px 14px rgba(60, 64, 67, 0.05);
    }

    html[data-theme="light"] .schedule-row:hover {
      border-color: #8ab4f8;
      box-shadow: 0 12px 28px rgba(26, 115, 232, 0.14);
      transform: translateY(-3px);
    }

    html[data-theme="light"] .schedule-row-toil {
      background: linear-gradient(90deg, #fffafa 0%, #ffffff 48%, #f4fbf7 100%);
      border: 1px solid #d5e1f2;
    }

    html[data-theme="light"] .time-badge {
      color: #1967d2;
    }

    html[data-theme="light"] .toil-highlight-box {
      background: #fef2f2;
      border: 1px solid #fecaca;
      box-shadow: inset 3px 0 0 #dc2626;
    }

    html[data-theme="light"] .toil-badge {
      color: #b91c1c;
    }

    html[data-theme="light"] .toil-duration {
      color: #991b1b;
      font-weight: 700;
    }

    html[data-theme="light"] .toil-text,
    html[data-theme="light"] .toil-text p {
      color: #7f1d1d !important;
    }

    html[data-theme="light"] .gemini-improve-box {
      background: #f0fdf4;
      border: 1px solid #bbf7d0;
      box-shadow: inset 3px 0 0 #16a34a;
    }

    html[data-theme="light"] .improve-badge {
      color: #15803d;
    }

    html[data-theme="light"] .improve-time-saved {
      background: #dcfce7;
      color: #166534;
      border: 1px solid #86efac;
    }

    html[data-theme="light"] .improve-text,
    html[data-theme="light"] .improve-text p {
      color: #14532d !important;
    }

    html[data-theme="light"] .agent-plug-btn {
      background: #e8f0fe;
      border: 1px solid #8ab4f8;
      color: #1967d2;
    }

    html[data-theme="light"] .agent-plug-btn:hover {
      background: #1a73e8;
      color: #ffffff;
    }

    html[data-theme="light"] .catalog-card,
    html[data-theme="light"] .dir-persona-card {
      background: #ffffff;
      border: 1px solid #d5e1f2;
      border-top: 4px solid var(--dept-accent, #1a73e8);
      box-shadow: 0 6px 18px rgba(26, 115, 232, 0.06);
    }

    html[data-theme="light"] .catalog-card:hover,
    html[data-theme="light"] .dir-persona-card:hover {
      background: #ffffff;
      box-shadow: 0 18px 38px rgba(26, 115, 232, 0.18);
    }

    html[data-theme="light"] .catalog-thumb {
      background: linear-gradient(145deg, #101828 0%, #1d2939 100%);
      border-bottom: 1px solid #d5e1f2;
    }

    html[data-theme="light"] .simple-arch-card {
      background: #ffffff;
      border: 1px solid #c6dafc;
      box-shadow: 0 10px 28px rgba(26, 115, 232, 0.09);
    }

    html[data-theme="light"] .simple-arch-svg-wrap {
      background: #0b1120;
      border: 1px solid #93c5fd;
    }

    html[data-theme="light"] .video-stage-box {
      background: #ffffff;
      border: 1px solid #c6dafc;
      box-shadow: 0 10px 28px rgba(26, 115, 232, 0.09);
    }

    html[data-theme="light"] .video-viewport {
      background: #f4f8ff;
    }

    html[data-theme="light"] .upload-video-btn {
      background: #ffffff;
      color: #3c4043;
      border: 1px solid #c6dafc;
    }

    html[data-theme="light"] .upload-video-btn:hover,
    html[data-theme="light"] .upload-video-btn.active {
      background: #1a73e8;
      color: #ffffff;
      border-color: #1a73e8;
    }

    html[data-theme="light"] .back-btn,
    html[data-theme="light"] .switch-pill {
      background: #ffffff;
      color: #3c4043;
      border: 1px solid #c6dafc;
      box-shadow: 0 2px 6px rgba(60, 64, 67, 0.05);
    }

    html[data-theme="light"] .back-btn:hover,
    html[data-theme="light"] .switch-pill:hover {
      background: #e8f0fe;
      color: #1a73e8;
      border-color: #1a73e8;
    }

    html[data-theme="light"] .dir-controls-bar {
      background: #ffffff;
      border: 1px solid #c6dafc;
      box-shadow: 0 6px 18px rgba(26, 115, 232, 0.06);
    }

    html[data-theme="light"] .dir-search-input {
      background: #f8fafd;
      border: 1px solid #c6dafc;
      color: #202124;
    }

    html[data-theme="light"] .pt-tile {
      background: #ffffff;
      border: 1px solid #d5e1f2;
      border-top: 3.5px solid var(--tile-color, #1a73e8);
      box-shadow: 0 3px 8px rgba(60, 64, 67, 0.06);
    }

    html[data-theme="light"] .pt-tile-title {
      color: #202124;
    }

    html[data-theme="light"] .pt-tile:hover,
    html[data-theme="light"] .pt-tile.active {
      background: #f4f8ff;
      transform: translateY(-5px) scale(1.03);
      box-shadow: 0 12px 24px rgba(26, 115, 232, 0.16);
    }

    html[data-theme="light"] .pt-side-card,
    html[data-theme="light"] .pt-legend-box,
    html[data-theme="light"] .pt-inline-expand,
    html[data-theme="light"] .mm-col-card,
    html[data-theme="light"] .mm-flow-card {
      background: #ffffff;
      border: 1px solid #c6dafc;
      box-shadow: 0 6px 18px rgba(26, 115, 232, 0.08);
      color: #202124;
    }

    html[data-theme="light"] .mm-node-btn {
      background: #f8fafd;
      border: 1px solid #d5e1f2;
      border-left: 4px solid var(--node-color, #1a73e8);
    }

    html[data-theme="light"] .mm-node-btn:hover,
    html[data-theme="light"] .mm-node-btn.active {
      background: #e8f0fe;
      box-shadow: 0 6px 14px rgba(26, 115, 232, 0.12);
    }

    html[data-theme="light"] .global-authors-footer {
      background: #ffffff;
      border: 1px solid #c6dafc;
      box-shadow: 0 6px 18px rgba(26, 115, 232, 0.06);
    }

    html[data-theme="light"] .authors-credit-pill {
      background: #e8f0fe;
      border: 1px solid #aecbfa;
      color: #1967d2;
      box-shadow: none;
    }

    html[data-theme="light"] .authors-credit-pill strong {
      color: #174ea6;
      text-decoration-color: rgba(23, 78, 166, 0.4);
    }
  </style>"""


NEW_NAVBAR_HTML = """  <header class="navbar">
    <div class="nav-brand" onclick="goHome()">
      <img data-asset="gemini_enterprise_dark.png" alt="Gemini Enterprise" class="gemini-logo" />
      <div class="nav-divider"></div>
      <span class="nav-csco-badge">Office of the CSCO · Supply Chain</span>
    </div>

    <div class="nav-right">
      <button type="button" class="nav-pill-btn" onclick="goHome()">Home</button>

      <div class="nav-dropdown-wrap" style="position:relative;">
        <button type="button" class="nav-pill-btn" onclick="goToOrgChart()">6 SCOR Pillars ▾</button>
        <div class="nav-quick-menu" id="navPillarsQuickMenu"></div>
      </div>

      <div class="nav-dropdown-wrap" style="position:relative;">
        <button type="button" class="nav-pill-btn" onclick="openPersonasDirectoryPage('all', '', true, 'personas')">Personas (29) ▾</button>
        <div class="nav-quick-menu" id="navPersonasQuickMenu"></div>
      </div>

      <div class="nav-dropdown-wrap" style="position:relative;">
        <button type="button" class="nav-pill-btn" onclick="openPersonasDirectoryPage('all', '', true, 'agents')">Agents (35) ▾</button>
        <div class="nav-quick-menu" id="navAgentsQuickMenu"></div>
      </div>

      <button type="button" class="nav-pill-btn" onclick="openPeriodicTablePage('all', null, true)">Periodic Table</button>
      <button type="button" class="nav-pill-btn" onclick="openMindMapPage('all', null, true)">Mind Map</button>
      <button type="button" id="themeToggleBtn" class="nav-pill-btn theme-toggle-btn" onclick="togglePortalTheme()" title="Switch between Light and Dark Theme">
        <span id="themeToggleIcon">☀️</span>
        <span id="themeToggleLabel">Light Theme</span>
      </button>
    </div>
  </header>"""


NEW_SHOWCASE_AND_HELPERS_JS = """    /* Low-Code vs. Hybrid vs. High-Code Classification Helper */
    function getAgentBuildClassification(ag) {
      const lowCodeIds = new Set([
        'csco_control_tower_copilot',
        'master_data_leadtime_steward',
        'working_capital_cash_bridge',
        'cpfr_sync_agent',
        'tariff_esg_agent',
        'supplier_quality_sentinel',
        'freight_control_tower',
        'trade_scheme_claims_reconciler',
        'otif_chargeback_defender',
        'esg_scope3_auditor'
      ]);
      const hybridIds = new Set([
        'disruption_war_room_orchestrator',
        'demand_sensing_agent',
        'promo_lift_simulator',
        'tier_n_risk_sentinel',
        'scrap_defect_root_cause_agent',
        'inline_quality_inspection_agent',
        'atp_order_promising_agent',
        'yard_dock_sequencer',
        'port_drayage_orchestrator',
        'field_beat_distributor_sync_agent',
        'planogram_merchandising_vision_auditor',
        'circular_rma_orchestrator'
      ]);

      const id = (ag && ag.id) ? ag.id : '';
      if (lowCodeIds.has(id)) {
        return {
          tier: 'Low-Code',
          label: '🟢 Low-Code · Gemini Enterprise Studio',
          shortLabel: '🟢 Low-Code Agent',
          platform: 'Gemini Enterprise No/Low-Code Builder + Grounded BigQuery RAG',
          engineTitle: 'Gemini Enterprise Studio',
          engineSub: 'Low-Code Prompt & Grounding',
          cssClass: 'build-tier-lowcode',
          color: '#34a853'
        };
      }
      if (hybridIds.has(id)) {
        return {
          tier: 'Hybrid',
          label: '🔵 Hybrid · Low-Code Agent + Cloud Run Tool',
          shortLabel: '🔵 Low-Code + Cloud Run',
          platform: 'Gemini Enterprise Conversational Flow + Cloud Run / Vision / Maps API Tool',
          engineTitle: 'Gemini Studio + Cloud Run',
          engineSub: 'Low-Code Flow + API Function',
          cssClass: 'build-tier-hybrid',
          color: '#4285f4'
        };
      }
      return {
        tier: 'High-Code',
        label: '🟣 High-Code · Vertex ADK + OR-Tools Solver',
        shortLabel: '🟣 High-Code ADK + Solver',
        platform: 'Vertex AI ADK Multi-Agent + Google OR-Tools Deterministic Math Solver',
        engineTitle: 'Vertex ADK + OR-Tools',
        engineSub: 'High-Code Multi-Agent Solver',
        cssClass: 'build-tier-highcode',
        color: '#a142f4'
      };
    }

    function populateNavbarQuickMenus() {
      const pillarsMenu = document.getElementById('navPillarsQuickMenu');
      const personasMenu = document.getElementById('navPersonasQuickMenu');
      const agentsMenu = document.getElementById('navAgentsQuickMenu');

      if (pillarsMenu) {
        pillarsMenu.innerHTML = Object.values(DEPARTMENTS).map(d => {
          const agCount = Object.values(AGENTS).filter(a => !a.isUniversal && a.deptId === d.id).length;
          return `
            <button type="button" class="nav-quick-item" onclick="goHome(); setTimeout(() => switchVerticalTab('${d.id}'), 40);">
              <span style="display:flex; align-items:center; gap:8px;">
                <span style="width:8px; height:8px; border-radius:50%; background:${d.color};"></span>
                <span>${d.scorBadge || ''} · ${d.name}</span>
              </span>
              <span style="font-size:11px; color:var(--text-secondary);">${d.personaIds.length}P · ${agCount}A</span>
            </button>
          `;
        }).join('');
      }

      if (personasMenu) {
        let html = `
          <button type="button" class="nav-quick-item" style="color:var(--g-blue); font-weight:800;" onclick="openPersonasDirectoryPage('all', '', true, 'personas')">
            <span>👥 Open Full Personas Directory (29)</span>
            <span>&rarr;</span>
          </button>
        `;
        Object.values(DEPARTMENTS).forEach(d => {
          html += `<div class="nav-quick-group-title" style="color:${d.color};">${d.scorBadge || ''} · ${d.name}</div>`;
          (d.personaIds || []).forEach(pid => {
            const p = PERSONAS[pid];
            if (!p) return;
            html += `
              <button type="button" class="nav-quick-item" onclick="openPersonaPage('${p.id}', true, event)">
                <span>${p.icon} ${p.name}</span>
                <span style="color:${d.color};">&rarr;</span>
              </button>
            `;
          });
        });
        personasMenu.innerHTML = html;
      }

      if (agentsMenu) {
        let html = `
          <button type="button" class="nav-quick-item" style="color:var(--g-blue); font-weight:800;" onclick="openPersonasDirectoryPage('all', '', true, 'agents')">
            <span>🤖 Open Full AI Agents Directory (35)</span>
            <span>&rarr;</span>
          </button>
          <div class="nav-quick-group-title" style="color:#4285f4;">🌐 Universal CSCO Core Agents (4)</div>
        `;
        UNIVERSAL_AGENT_IDS.forEach(uid => {
          const ag = AGENTS[uid];
          if (!ag) return;
          const cls = getAgentBuildClassification(ag);
          html += `
            <button type="button" class="nav-quick-item" onclick="openAgentPage('${ag.id}', true, event)">
              <span>${ag.name}</span>
              <span style="font-size:10.5px; color:${cls.color};">${cls.tier}</span>
            </button>
          `;
        });
        Object.values(DEPARTMENTS).forEach(d => {
          const dAgents = Object.values(AGENTS).filter(a => !a.isUniversal && a.deptId === d.id);
          if (!dAgents.length) return;
          html += `<div class="nav-quick-group-title" style="color:${d.color};">${d.scorBadge || ''} · ${d.name} (${dAgents.length})</div>`;
          dAgents.forEach(ag => {
            const cls = getAgentBuildClassification(ag);
            html += `
              <button type="button" class="nav-quick-item" onclick="openAgentPage('${ag.id}', true, event)">
                <span>${ag.name}</span>
                <span style="font-size:10.5px; color:${cls.color};">${cls.tier}</span>
              </button>
            `;
          });
        });
        agentsMenu.innerHTML = html;
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
      const pillarAgents = Object.values(AGENTS).filter(a => !a.isUniversal && a.deptId === dept.id);

      container.innerHTML = `
        <div id="deptShowcaseBoxEl" class="dept-showcase-box genie-enter" style="--dept-accent: ${dept.color};">
          <div class="showcase-header">
            <div class="showcase-dept-name">
              <span class="accent-dot" style="background: ${dept.color};"></span>
              <span>${dept.scorBadge || ''} · ${dept.name}</span>
            </div>
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              <button type="button" class="switch-pill" onclick="openPersonasDirectoryPage('${dept.id}', '', true, 'personas', event)">
                👥 Pillar Personas (${dept.personaIds.length})
              </button>
              <button type="button" class="switch-pill" onclick="openPersonasDirectoryPage('${dept.id}', '', true, 'agents', event)">
                🤖 Pillar Agents (${pillarAgents.length})
              </button>
              <button type="button" class="switch-pill" onclick="selectDepartment('${dept.id}')">
                ✕ Close
              </button>
            </div>
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

          <!-- 1. Personas in this Pillar -->
          <div style="margin-top: 22px;">
            <div style="font-size:15px; font-weight:800; color:var(--text-primary); margin-bottom:12px; display:flex; align-items:center; justify-content:space-between;">
              <span style="display:flex; align-items:center; gap:8px;">
                <span class="accent-dot" style="background:${dept.color};"></span>
                <span>1. Click Any Persona to View Red vs. Green Daily Journey (${dept.personaIds.length})</span>
              </span>
            </div>

            <div class="dept-personas-list" style="display:grid; grid-template-columns: repeat(auto-fit, minmax(275px, 1fr)); gap:12px;">
              ${dept.personaIds.map(pid => {
                const p = PERSONAS[pid];
                if (!p) return '';
                return `
                  <div class="persona-link-card" style="--dept-accent: ${dept.color};" onclick="openPersonaPage('${p.id}', true, event)">
                    <div class="persona-link-left">
                      <div class="persona-emoji">${p.icon}</div>
                      <div>
                        <div class="persona-link-name">${p.name}</div>
                        <div class="persona-link-role">${p.role}</div>
                      </div>
                    </div>
                    <span class="persona-open-arrow" style="color:${dept.color}; font-weight:800;">&rarr;</span>
                  </div>
                `;
              }).join('')}
            </div>
          </div>

          <!-- 2. Direct 1-Click Access to AI Agents in this Pillar -->
          <div style="margin-top: 24px; padding-top: 20px; border-top: 1px solid var(--border-subtle);">
            <div style="font-size:15px; font-weight:800; color:var(--text-primary); margin-bottom:12px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px;">
              <span style="display:flex; align-items:center; gap:8px;">
                <span class="accent-dot" style="background:${dept.color};"></span>
                <span>2. Direct Access — AI Agents in ${dept.name} (${pillarAgents.length})</span>
              </span>
              <span style="font-size:12px; color:var(--text-secondary);">Includes Low-Code, Hybrid &amp; High-Code Agents</span>
            </div>

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(275px, 1fr)); gap:12px;">
              ${pillarAgents.map(ag => {
                const cls = getAgentBuildClassification(ag);
                return `
                  <div class="persona-link-card" style="--dept-accent: ${dept.color};" onclick="openAgentPage('${ag.id}', true, event)">
                    <div class="persona-link-left" style="align-items:flex-start;">
                      <div class="persona-emoji" style="font-size:16px;">🤖</div>
                      <div>
                        <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap; margin-bottom:3px;">
                          <span class="persona-link-name">${ag.name}</span>
                          <span class="build-tier-badge ${cls.cssClass}" style="font-size:10px; padding:2px 8px;">${cls.shortLabel}</span>
                        </div>
                        <div class="persona-link-role">${shortSentence(ag.shortDesc, 88)}</div>
                      </div>
                    </div>
                    <span class="persona-open-arrow" style="color:${dept.color}; font-weight:800;">&rarr;</span>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        </div>
      `;
    }"""


NEW_PERSONA_PAGE_JS = """    function openPersonaPage(personaId, pushHash = true, ev = null) {
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

          <!-- Persona Overview Header with Headline Impact Stat -->
          <div class="persona-header-card" style="padding: 30px 34px; margin-bottom: 22px;">
            ${renderSupplyChainWatermarkSvg(dept.watermarkType, dept.color, 'persona-header-sc-watermark')}

            <div style="position:relative; z-index:2;">
              <div class="persona-badge" style="background: ${dept.color}18; color: ${dept.color}; border: 1px solid ${dept.color}45;">
                <span>${p.icon}</span>
                <span>${dept.scorBadge || ''} · ${dept.name} · ${p.role}</span>
              </div>
              <h1 class="persona-page-title">${p.name}</h1>
              <p class="persona-page-summary">${shortSentence(p.summary, 165)}</p>
            </div>

            <div class="persona-stat-highlight" style="border-color: ${dept.color}45;">
              <div class="persona-stat-value" style="color: ${dept.color};">${p.headlineStat || '-85% Toil'}</div>
              <div class="persona-stat-label">${p.headlineLabel || 'Manual Effort Reduction'}</div>
            </div>
          </div>

          <!-- Before vs. After Daily Capacity Shift Meter -->
          <div class="time-shift-banner" style="margin-bottom: 28px;">
            <div class="shift-meter-card">
              <div class="shift-meter-top">
                <span style="color: var(--text-secondary); font-weight:600;">✕ Before (Manual Toil)</span>
                <span style="color: #ea4335; font-weight: 700;">${p.toilHoursBefore || '6.5 hrs/day manual toil'}</span>
              </div>
              <div class="shift-bar-track">
                <div style="width: 78%; background: #ea4335;"></div>
                <div style="width: 22%; background: rgba(148,163,184,0.25);"></div>
              </div>
            </div>

            <div class="shift-meter-card">
              <div class="shift-meter-top">
                <span style="color: var(--text-secondary); font-weight:600;">✦ With Gemini AI Agents</span>
                <span style="color: #34a853; font-weight: 700;">${p.toilHoursAfter || '1.0 hr/day exception review'}</span>
              </div>
              <div class="shift-bar-track">
                <div style="width: 18%; background: #34a853;"></div>
                <div style="width: 82%; background: #4285f4;"></div>
              </div>
            </div>
          </div>

          <!-- Red vs. Green Persona Journey -->
          <div class="ditl-header-row" style="margin-bottom: 16px;">
            <div>
              <h2 class="block-title" style="border-left-color: ${dept.color};">Persona Daily Journey — Before vs. With Gemini AI</h2>
              <p class="block-subtitle">Side-by-side comparison of manual bottlenecks (Red) and AI-powered execution (Green).</p>
            </div>

            <div class="ditl-legend">
              <span class="legend-item">
                <span class="legend-swatch" style="background: #ea4335;"></span>
                <span style="font-weight: 700;">Manual Bottleneck</span>
              </span>
              <span class="legend-item">
                <span class="legend-swatch" style="background: #34a853;"></span>
                <span style="font-weight: 700;">With Gemini AI</span>
              </span>
            </div>
          </div>

          <div class="day-schedule" style="margin-bottom: 42px;">
            ${p.dayInLife.map(slot => {
              if (!slot.isToil) {
                return `
                  <div class="schedule-row" style="grid-template-columns: 240px 1fr;">
                    <div class="schedule-time-col">
                      <span class="time-badge">${slot.time}</span>
                      <span class="task-title">${slot.task}</span>
                    </div>
                    <div style="display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap;">
                      <span style="font-size:15px; color:var(--text-secondary);">${shortSentence(slot.activity, 135)}</span>
                      <span class="core-tag-pill">👤 ${slot.tag || 'Strategic Leadership'}</span>
                    </div>
                  </div>
                `;
              }

              const plugAgent = slot.agentId ? AGENTS[slot.agentId] : null;
              const plugCls = plugAgent ? getAgentBuildClassification(plugAgent) : null;
              return `
                <div class="schedule-row schedule-row-toil">
                  <div class="schedule-time-col">
                    <div>
                      <div class="time-badge">${slot.time}</div>
                      <div class="task-title">${slot.task}</div>
                    </div>
                    ${plugAgent ? `
                      <div>
                        <button type="button" class="agent-plug-btn" onclick="openAgentPage('${plugAgent.id}', true, event)">
                          <span>🤖 ${plugAgent.name}</span>
                          <span>&rarr;</span>
                        </button>
                        <div style="margin-top:6px;">
                          <span class="build-tier-badge ${plugCls.cssClass}" style="font-size:10px; padding:2px 8px;">${plugCls.shortLabel}</span>
                        </div>
                      </div>
                    ` : ''}
                  </div>

                  <div class="toil-highlight-box">
                    <div class="toil-top-bar">
                      <span class="toil-badge">✕ Manual Bottleneck</span>
                      <span class="toil-duration">${slot.toilDuration || '2.0 hrs'}</span>
                    </div>
                    <div class="toil-text">${shortSentence(slot.before, 125)}</div>
                  </div>

                  <div class="gemini-improve-box">
                    <div class="improve-top-bar">
                      <span class="improve-badge">
                        <span>✦ With Gemini AI</span>
                      </span>
                      <span class="improve-time-saved">${slot.toilDuration || '2.0 hrs'} &rarr; ${slot.afterDuration || '10 mins'}</span>
                    </div>
                    <div class="improve-text">${shortSentence(slot.after, 125)}</div>
                  </div>
                </div>
              `;
            }).join('')}
          </div>

          <!-- Clean Agent Catalogue for this Persona -->
          <div style="margin-bottom: 16px;">
            <h2 class="block-title" style="border-left-color: ${dept.color};">AI Agents Assisting ${p.name}</h2>
          </div>

          <div class="catalog-grid">
            ${[...new Set([...(p.agentIds || []), ...UNIVERSAL_AGENT_IDS])].map(aid => {
              const ag = AGENTS[aid];
              if (!ag) return '';
              const agDept = getDeptMeta(ag.deptId);
              const cls = getAgentBuildClassification(ag);
              return `
                <div class="catalog-card" style="--dept-accent: ${agDept.color};" onclick="openAgentPage('${ag.id}', true, event)">
                  <div class="catalog-thumb" style="height: 138px;">
                    ${renderMiniCatalogCadSvg(ag.cadType, agDept.color)}
                  </div>
                  <div class="catalog-body" style="padding: 20px;">
                    <div>
                      <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; flex-wrap:wrap; margin-bottom:8px;">
                        <span style="font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:${agDept.color};">
                          ${ag.isUniversal ? 'Universal Core' : dept.name}
                        </span>
                        <span class="build-tier-badge ${cls.cssClass}" style="font-size:10px; padding:2px 8px;">
                          ${cls.shortLabel}
                        </span>
                      </div>
                      <div class="catalog-title" style="font-size:18.5px;">${ag.name}</div>
                      <div class="catalog-desc" style="font-size:14.5px;">${shortSentence(ag.shortDesc, 115)}</div>
                    </div>
                    <div class="catalog-footer" style="margin-top:12px; padding-top:12px;">
                      <span style="color: ${agDept.color}; font-size:13.5px; font-weight:700;">Open Agent Workflow &amp; Video</span>
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
    }"""


NEW_AGENT_ARCH_AND_PAGE_JS = """    function renderSimpleAgentArchitectureDiagram(ag, dept) {
      const sysArr = toSysArray(ag.systems);
      const cls = getAgentBuildClassification(ag);
      const trunc = (str, max = 23) => {
        const s = String(str || '').trim();
        return s.length > max ? s.slice(0, max - 1) + '…' : s;
      };
      const s1 = trunc(sysArr[0] || 'SAP S/4HANA / ERP', 23);
      const s2 = trunc(sysArr[1] || 'WMS / TMS Telemetry', 23);
      const s3 = trunc(sysArr[2] || 'Partner EDI & Weather', 23);
      const agentShort = trunc(ag.name, 22);

      const defaultSubAgents = [
        { name: 'Signal Ingestion & Context Node', role: 'Streams & validates live operational inputs' },
        { name: cls.tier === 'Low-Code' ? 'Grounded RAG & Policy Synthesizer' : 'Scenario & Optimization Engine', role: 'Evaluates constraints & ranks actions' },
        { name: 'Exception & Write-Back Dispatcher', role: 'Generates alerts & signed ERP payloads' }
      ];
      const subs = (ag.subAgents && ag.subAgents.length >= 3) ? ag.subAgents.slice(0, 3) : defaultSubAgents;
      const sub1 = trunc(subs[0].name, 23);
      const sub2 = trunc(subs[1].name, 23);
      const sub3 = trunc(subs[2].name, 23);

      return `
        <div class="simple-arch-card">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:14px;">
            <div>
              <div style="font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:${dept.color}; margin-bottom:4px;">
                End-to-End Branching Agent Workflow &amp; Execution Topology
              </div>
              <h2 style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary); margin:0;">
                How ${ag.name} Works
              </h2>
            </div>

            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span class="build-tier-badge ${cls.cssClass}">
                ${cls.label}
              </span>
              <span style="font-size:12.5px; color:var(--text-secondary); font-weight:600;">
                ${cls.platform}
              </span>
            </div>
          </div>

          <div class="simple-arch-svg-wrap">
            <svg viewBox="0 0 1060 300" style="width:100%; height:auto; display:block;">
              <defs>
                <linearGradient id="archFlowGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="${dept.color}" />
                  <stop offset="50%" stop-color="${cls.color}" />
                  <stop offset="100%" stop-color="#34a853" />
                </linearGradient>
              </defs>

              <!-- 1. Fan-In Branches: 3 Data Sources -> Unified Digital Twin -->
              <path id="inPath1" d="M 188 54 C 212 54, 212 150, 236 150" fill="none" stroke="${dept.color}" stroke-width="2" stroke-dasharray="5 4" />
              <path id="inPath2" d="M 188 150 L 236 150" fill="none" stroke="#4285f4" stroke-width="2" stroke-dasharray="5 4" />
              <path id="inPath3" d="M 188 246 C 212 246, 212 150, 236 150" fill="none" stroke="#fbbc04" stroke-width="2" stroke-dasharray="5 4" />

              <circle r="3.5" fill="${dept.color}"><animateMotion dur="2.2s" repeatCount="indefinite" path="M 188 54 C 212 54, 212 150, 236 150" /></circle>
              <circle r="3.5" fill="#4285f4"><animateMotion dur="1.8s" repeatCount="indefinite" path="M 188 150 L 236 150" /></circle>
              <circle r="3.5" fill="#fbbc04"><animateMotion dur="2.5s" repeatCount="indefinite" path="M 188 246 C 212 246, 212 150, 236 150" /></circle>

              <!-- 2. Twin -> Root Orchestrator -->
              <path d="M 404 150 L 444 150" fill="none" stroke="#4285f4" stroke-width="2.5" />
              <polygon points="444,150 436,145 436,155" fill="#4285f4" />

              <!-- 3. Fan-Out Branches: Orchestrator -> 3 Parallel Sub-Agent / Tool Nodes -->
              <path d="M 628 130 C 654 130, 654 54, 680 54" fill="none" stroke="${cls.color}" stroke-width="2" stroke-dasharray="5 4" />
              <path d="M 628 150 L 680 150" fill="none" stroke="${cls.color}" stroke-width="2" stroke-dasharray="5 4" />
              <path d="M 628 170 C 654 170, 654 246, 680 246" fill="none" stroke="${cls.color}" stroke-width="2" stroke-dasharray="5 4" />

              <circle r="3.5" fill="${cls.color}"><animateMotion dur="2.0s" repeatCount="indefinite" path="M 628 130 C 654 130, 654 54, 680 54" /></circle>
              <circle r="3.5" fill="${cls.color}"><animateMotion dur="1.6s" repeatCount="indefinite" path="M 628 150 L 680 150" /></circle>
              <circle r="3.5" fill="${cls.color}"><animateMotion dur="2.3s" repeatCount="indefinite" path="M 628 170 C 654 170, 654 246, 680 246" /></circle>

              <!-- 4. Fan-In / Branch to Dual Execution Outputs -->
              <path d="M 862 54 C 884 54, 884 98, 904 98" fill="none" stroke="#34a853" stroke-width="2" stroke-dasharray="5 4" />
              <path d="M 862 150 C 884 150, 884 98, 904 98" fill="none" stroke="#34a853" stroke-width="2" />
              <path d="M 862 150 C 884 150, 884 206, 904 206" fill="none" stroke="#38bdf8" stroke-width="2" />
              <path d="M 862 246 C 884 246, 884 206, 904 206" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="5 4" />

              <!-- STAGE 1: 3 Parallel Data Input Nodes -->
              <rect x="14" y="20" width="174" height="68" rx="10" fill="#111827" stroke="${dept.color}" stroke-width="1.6" />
              <text x="26" y="42" fill="${dept.color}" font-size="10" font-weight="700">1A · ENTERPRISE SYSTEM</text>
              <text x="26" y="64" fill="#f8fafc" font-size="12.5" font-weight="700">${s1}</text>

              <rect x="14" y="116" width="174" height="68" rx="10" fill="#111827" stroke="#4285f4" stroke-width="1.6" />
              <text x="26" y="138" fill="#60a5fa" font-size="10" font-weight="700">1B · LIVE TELEMETRY</text>
              <text x="26" y="160" fill="#f8fafc" font-size="12.5" font-weight="700">${s2}</text>

              <rect x="14" y="212" width="174" height="68" rx="10" fill="#111827" stroke="#fbbc04" stroke-width="1.6" />
              <text x="26" y="234" fill="#fbbf24" font-size="10" font-weight="700">1C · PARTNER &amp; PUBLIC</text>
              <text x="26" y="256" fill="#f8fafc" font-size="12.5" font-weight="700">${s3}</text>

              <!-- STAGE 2: Unified Supply Chain Twin -->
              <rect x="236" y="88" width="168" height="124" rx="14" fill="#0f172a" stroke="#4285f4" stroke-width="2" />
              <text x="250" y="114" fill="#60a5fa" font-size="10.5" font-weight="700">02 · DIGITAL TWIN</text>
              <text x="250" y="138" fill="#ffffff" font-size="14" font-weight="700">BigQuery &amp; Spanner</text>
              <text x="250" y="160" fill="#94a3b8" font-size="11.5">• Canonical Graph State</text>
              <text x="250" y="180" fill="#94a3b8" font-size="11.5">• Real-Time Event Bus</text>
              <text x="250" y="198" fill="#38bdf8" font-size="10.5" font-weight="700">Pub/Sub · AlloyDB</text>

              <!-- STAGE 3: Agent Orchestrator (Low-Code / Hybrid / High-Code) -->
              <rect x="444" y="76" width="184" height="148" rx="16" fill="#131c31" stroke="${cls.color}" stroke-width="2.4" />
              <rect x="456" y="88" width="160" height="22" rx="6" fill="${cls.color}26" stroke="${cls.color}" stroke-width="1" />
              <text x="536" y="103" text-anchor="middle" fill="#ffffff" font-size="10" font-weight="800">${cls.tier.toUpperCase()} AGENT</text>
              <text x="458" y="132" fill="#ffffff" font-size="14" font-weight="800">${agentShort}</text>
              <text x="458" y="154" fill="${cls.color}" font-size="12" font-weight="700">${cls.engineTitle}</text>
              <text x="458" y="174" fill="#cbd5e1" font-size="11.5">${cls.engineSub}</text>
              <text x="458" y="196" fill="#94a3b8" font-size="11">Branches to 3 workflows &rarr;</text>

              <!-- STAGE 4: 3 Parallel Branching Sub-Workflows / Tools -->
              <rect x="680" y="20" width="182" height="68" rx="10" fill="#111827" stroke="${cls.color}" stroke-width="1.6" />
              <text x="692" y="42" fill="${cls.color}" font-size="10" font-weight="700">BRANCH 3A · INGEST &amp; SENSE</text>
              <text x="692" y="64" fill="#f8fafc" font-size="12" font-weight="700">${sub1}</text>

              <rect x="680" y="116" width="182" height="68" rx="10" fill="#111827" stroke="${cls.color}" stroke-width="1.6" />
              <text x="692" y="138" fill="${cls.color}" font-size="10" font-weight="700">BRANCH 3B · REASON / SOLVE</text>
              <text x="692" y="160" fill="#f8fafc" font-size="12" font-weight="700">${sub2}</text>

              <rect x="680" y="212" width="182" height="68" rx="10" fill="#111827" stroke="${cls.color}" stroke-width="1.6" />
              <text x="692" y="234" fill="${cls.color}" font-size="10" font-weight="700">BRANCH 3C · VALIDATE &amp; GATE</text>
              <text x="692" y="256" fill="#f8fafc" font-size="12" font-weight="700">${sub3}</text>

              <!-- STAGE 5: Dual Branching Execution Outputs -->
              <rect x="904" y="52" width="142" height="92" rx="12" fill="#0f291e" stroke="#34a853" stroke-width="1.8" />
              <text x="916" y="76" fill="#4ade80" font-size="10" font-weight="700">4A · AUTO WRITE-BACK</text>
              <text x="916" y="98" fill="#ffffff" font-size="12.5" font-weight="700">ERP / WMS Action</text>
              <text x="916" y="118" fill="#a7f3d0" font-size="11">Apigee Signed Call</text>

              <rect x="904" y="160" width="142" height="92" rx="12" fill="#0f1f38" stroke="#38bdf8" stroke-width="1.8" />
              <text x="916" y="184" fill="#38bdf8" font-size="10" font-weight="700">4B · HUMAN-IN-LOOP</text>
              <text x="916" y="206" fill="#ffffff" font-size="12.5" font-weight="700">Control Tower Alert</text>
              <text x="916" y="226" fill="#bae6fd" font-size="11">${trunc(ag.badge || 'KPI Impact', 18)}</text>
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

      lastAgentId = agentId;
      const dept = getDeptMeta(ag.deptId);
      const cls = getAgentBuildClassification(ag);
      const backPersona = PERSONAS[lastPersonaId] || Object.values(PERSONAS)[0];
      const videoUrl = customVideos[ag.id] || ag.videoSrc;
      const hasVideo = Boolean(customVideos[ag.id]) || Boolean(ag.hasPreloadedVideo);

      const siblingAgents = ag.isUniversal
        ? UNIVERSAL_AGENT_IDS.map(id => AGENTS[id]).filter(Boolean)
        : Object.values(AGENTS).filter(a => !a.isUniversal && a.deptId === dept.id);

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

          <!-- 1. What This Agent Does + Low-Code / Hybrid / High-Code Badge -->
          <div class="agent-hero-banner" style="padding: 30px 34px; margin-bottom: 24px;">
            <div style="position:relative; z-index:2; display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin-bottom:12px;">
              <div class="persona-badge" style="margin-bottom:0; background: ${dept.color}18; color: ${dept.color}; border: 1px solid ${dept.color}40;">
                <span>${ag.isUniversal ? '🌐 Universal Core Agent' : `${dept.scorBadge} · ${dept.name}`}</span>
              </div>
              <span class="build-tier-badge ${cls.cssClass}">
                ${cls.label}
              </span>
              ${ag.badge ? `<span class="build-tier-badge" style="background:${dept.color}18; color:${dept.color}; border:1px solid ${dept.color}45;">✦ ${ag.badge}</span>` : ''}
            </div>

            <h1 class="agent-title" style="font-size: clamp(28px, 3.2vw, 40px); margin-bottom: 10px;">${ag.name}</h1>
            <p class="agent-subtitle" style="font-size: 16.5px;">
              ${shortSentence(ag.shortDesc, 175)} ${shortSentence(ag.solution, 175)}
            </p>
          </div>

          <!-- 2. Branching Multi-Stage Workflow Architecture Diagram -->
          ${renderSimpleAgentArchitectureDiagram(ag, dept)}

          <!-- 3. Dedicated Box for a Video -->
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
        </div>
      `;

      hydrateAssets();
      showActivePage('pageAgent');
      const wrap = document.getElementById('agentGenieWrap');
      if (sRect && wrap) {
        animateGenieOutOfBox(sRect, wrap, dept.color);
      }
    }"""


def main():
    text = BUILD_SITE.read_text(encoding="utf-8")

    # 1. Replace the simplified CSS + Light Theme CSS block with the enhanced CSS block
    css_pattern = re.compile(
        r"    /\* =========================================================================\n"
        r"       SIMPLIFIED PERSONA JOURNEY & COMPACT AGENT ARCHITECTURE STYLES.*?</style>",
        re.DOTALL,
    )
    if not css_pattern.search(text):
        raise RuntimeError("Could not find SIMPLIFIED PERSONA JOURNEY CSS block in build_site.py")
    text = css_pattern.sub(ENHANCED_CSS_BLOCK, text, count=1)

    # 2. Replace the navbar HTML to include quick-jump dropdown menus for 6 SCOR Pillars, Personas (29), and Agents (35)
    nav_pattern = re.compile(
        r"  <header class=\"navbar\">.*?</header>",
        re.DOTALL,
    )
    if not nav_pattern.search(text):
        raise RuntimeError("Could not find <header class=\"navbar\"> in build_site.py")
    text = nav_pattern.sub(NEW_NAVBAR_HTML, text, count=1)

    # 3. Make Hero Canvas vibrant in Light Theme as well
    text = text.replace(
        "ctx.globalAlpha = isLightTheme ? 0.55 : 0.85;",
        "ctx.globalAlpha = isLightTheme ? 0.86 : 0.86;",
    )

    # 4. Replace renderDepartmentShowcaseBox() with the new helper + showcase box (showing BOTH Personas and Agents)
    showcase_pattern = re.compile(
        r"    function renderDepartmentShowcaseBox\(\) \{.*?\n    \}\n\n    /\* =========================================================================\n       EXECUTIVE SELLING METADATA HELPER",
        re.DOTALL,
    )
    if not showcase_pattern.search(text):
        raise RuntimeError("Could not find renderDepartmentShowcaseBox in build_site.py")
    text = showcase_pattern.sub(
        NEW_SHOWCASE_AND_HELPERS_JS
        + "\n\n    /* =========================================================================\n       EXECUTIVE SELLING METADATA HELPER",
        text,
        count=1,
    )

    # 5. Replace openPersonaPage() with the restored Red vs. Green concise journey
    persona_pattern = re.compile(
        r"    function openPersonaPage\(personaId, pushHash = true, ev = null\) \{.*?\n    \}\n\n    /\* =========================================================================\n       AGENT ARCHITECTURE BLUEPRINT HELPER",
        re.DOTALL,
    )
    if not persona_pattern.search(text):
        raise RuntimeError("Could not find openPersonaPage in build_site.py")
    text = persona_pattern.sub(
        NEW_PERSONA_PAGE_JS
        + "\n\n    /* =========================================================================\n       AGENT ARCHITECTURE BLUEPRINT HELPER",
        text,
        count=1,
    )

    # 6. Replace renderSimpleAgentArchitectureDiagram + openAgentPage with the branching workflow diagram + Low-Code/Hybrid/High-Code badges
    agent_pattern = re.compile(
        r"    function renderSimpleAgentArchitectureDiagram\(ag, dept\) \{.*?\n    function attachAgentVideo\(event, agentId\)",
        re.DOTALL,
    )
    if not agent_pattern.search(text):
        raise RuntimeError("Could not find renderSimpleAgentArchitectureDiagram / openAgentPage in build_site.py")
    text = agent_pattern.sub(
        NEW_AGENT_ARCH_AND_PAGE_JS + "\n\n    function attachAgentVideo(event, agentId)",
        text,
        count=1,
    )

    # 7. Also display Low-Code / Hybrid / High-Code badge on Directory Agent cards
    old_dir_agent_card = """        return agentsList.map(ag => {
          const dept = getDeptMeta(ag.deptId);
          return `
            <div class="dir-persona-card" style="--dept-accent: ${dept.color}; cursor:pointer;" onclick="openAgentPage('${ag.id}', true, event)">
              <div>
                <div style="font-size:11.5px; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:${dept.color}; margin-bottom:4px;">
                  ${ag.isUniversal ? 'Universal Core Agent' : `${dept.scorBadge || ''} · ${dept.name}`}
                </div>"""
    new_dir_agent_card = """        return agentsList.map(ag => {
          const dept = getDeptMeta(ag.deptId);
          const cls = getAgentBuildClassification(ag);
          return `
            <div class="dir-persona-card" style="--dept-accent: ${dept.color}; cursor:pointer;" onclick="openAgentPage('${ag.id}', true, event)">
              <div>
                <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; flex-wrap:wrap; margin-bottom:6px;">
                  <span style="font-size:11.5px; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:${dept.color};">
                    ${ag.isUniversal ? 'Universal Core Agent' : `${dept.scorBadge || ''} · ${dept.name}`}
                  </span>
                  <span class="build-tier-badge ${cls.cssClass}" style="font-size:10px; padding:2px 8px;">
                    ${cls.shortLabel}
                  </span>
                </div>"""
    if old_dir_agent_card in text:
        text = text.replace(old_dir_agent_card, new_dir_agent_card, 1)

    # 8. Call populateNavbarQuickMenus() inside DOMContentLoaded initialization
    if "populateNavbarQuickMenus();" not in text:
        text = text.replace(
            "renderOrgChart();",
            "renderOrgChart();\n      populateNavbarQuickMenus();",
            1,
        )

    BUILD_SITE.write_text(text, encoding="utf-8")
    print("Successfully updated build_site.py with enhanced Light Theme, Red/Green Persona Journey, Branching Agent Workflow, Low-Code/High-Code badges, and 1-click Persona/Agent access!")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds the comprehensive, gamified Supply Chain 101 Executive Masterclass.
Outputs:
- supply_chain_101_interactive_academy.html
- SUPPLY_CHAIN_101_MASTER_GUIDE.md
And synchronizes copies to docs/, zipline_dist/, and dist/itc_limited/.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Import rich datasets from course_data
import sys
sys.path.insert(0, str(ROOT / "scripts"))
import course_data as cd

FLASHCARDS = cd.FLASHCARDS
CONTROL_TOWER = cd.CONTROL_TOWER_SPEC
ALPHABET_AI = cd.ALPHABET_AI_SPEC
CUSTOMER_DECODER = cd.CUSTOMER_DECODER
QUIZ = cd.QUIZ

print(f"Loaded: {len(FLASHCARDS)} flashcards, {len(CUSTOMER_DECODER)} decoders, {len(QUIZ)} quiz questions.")

def generate_html() -> str:
    # Serialize data for embedded client-side JS
    flashcards_json = json.dumps(FLASHCARDS, ensure_ascii=False)
    decoder_json = json.dumps(CUSTOMER_DECODER, ensure_ascii=False)
    quiz_json = json.dumps(QUIZ, ensure_ascii=False)
    control_tower_json = json.dumps(CONTROL_TOWER, ensure_ascii=False)
    alphabet_ai_json = json.dumps(ALPHABET_AI, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Supply Chain 101 — Complete Executive Masterclass &amp; Gamified Learning Academy</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Google+Sans+Display:wght@500;700;800&family=Google+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --g-blue: #1A73E8;
      --g-blue-bg: #E8F0FE;
      --g-blue-hover: #174EA6;
      --g-red: #D93025;
      --g-red-bg: #FCE8E6;
      --g-yellow: #F9AB00;
      --g-yellow-bg: #FEF7E0;
      --g-green: #1E8E3E;
      --g-green-bg: #E6F4EA;
      --g-purple: #9334E6;
      --g-purple-bg: #F3E8FD;
      --bg-page: #F8F9FA;
      --bg-card: #FFFFFF;
      --text-main: #202124;
      --text-sub: #5F6368;
      --border-light: #DADCE0;
      --border-hover: #BDC1C6;
      --font-display: 'Google Sans Display', 'Google Sans', 'Inter', sans-serif;
      --font-sans: 'Google Sans', 'Inter', -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
      --shadow-sm: 0 1px 3px rgba(60,64,67,0.08), 0 1px 2px rgba(60,64,67,0.16);
      --shadow-md: 0 4px 12px rgba(60,64,67,0.12), 0 1px 3px rgba(60,64,67,0.08);
      --shadow-lg: 0 12px 28px rgba(60,64,67,0.18), 0 2px 6px rgba(60,64,67,0.12);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      background: var(--bg-page);
      color: var(--text-main);
      font-family: var(--font-sans);
      font-size: 16.5px;
      line-height: 1.68;
      -webkit-font-smoothing: antialiased;
    }}

    /* Google 4-Color Top Stripe */
    .g-color-strip {{
      height: 5px;
      background: linear-gradient(90deg, #4285F4 0% 25%, #EA4335 25% 50%, #FBBC04 50% 75%, #34A853 75% 100%);
      position: sticky;
      top: 0;
      z-index: 200;
    }}

    /* Sticky Master Header */
    .g-header {{
      position: sticky;
      top: 5px;
      z-index: 190;
      background: rgba(255, 255, 255, 0.98);
      backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border-light);
      padding: 14px 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
      box-shadow: var(--shadow-sm);
    }}

    .g-container {{
      max-width: 1240px;
      margin: 0 auto;
      padding: 28px 24px 96px;
    }}

    /* Buttons */
    .g-btn {{
      font-family: var(--font-sans);
      font-size: 14.5px;
      font-weight: 600;
      padding: 9px 18px;
      border-radius: 999px;
      border: 1.5px solid var(--border-light);
      background: #FFFFFF;
      color: var(--text-main);
      cursor: pointer;
      transition: all 0.18s ease;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }}
    .g-btn:hover {{
      border-color: var(--g-blue);
      color: var(--g-blue);
      background: var(--g-blue-bg);
      transform: translateY(-1px);
    }}
    .g-btn-primary {{
      background: var(--g-blue);
      color: #FFFFFF;
      border-color: var(--g-blue);
    }}
    .g-btn-primary:hover {{
      background: var(--g-blue-hover);
      color: #FFFFFF;
      box-shadow: 0 4px 10px rgba(26,115,232,0.3);
    }}

    /* Gamification Status Bar */
    .gamification-bar {{
      background: #FFFFFF;
      border: 1.5px solid var(--border-light);
      border-radius: 18px;
      padding: 16px 24px;
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
      flex-wrap: wrap;
      box-shadow: var(--shadow-sm);
    }}
    .xp-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: linear-gradient(135deg, #FEF7E0 0%, #FEF0C0 100%);
      border: 1.5px solid #F9AB00;
      padding: 6px 16px;
      border-radius: 999px;
      font-weight: 700;
      font-size: 15px;
      color: #B06000;
    }}
    .level-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: var(--g-blue-bg);
      border: 1.5px solid var(--g-blue);
      padding: 6px 16px;
      border-radius: 999px;
      font-weight: 700;
      font-size: 15px;
      color: var(--g-blue);
    }}

    /* Module Navigation Tabs */
    .g-tabs-nav {{
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding: 8px 4px 16px;
      border-bottom: 2px solid var(--border-light);
      margin-bottom: 30px;
      scrollbar-width: thin;
    }}
    .g-tab-btn {{
      font-family: var(--font-sans);
      font-size: 14.5px;
      font-weight: 600;
      padding: 10px 18px;
      border-radius: 12px;
      border: 1.5px solid transparent;
      background: #FFFFFF;
      color: var(--text-sub);
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.16s ease;
      box-shadow: var(--shadow-sm);
    }}
    .g-tab-btn:hover {{
      background: var(--g-blue-bg);
      color: var(--g-blue);
      border-color: rgba(26,115,232,0.3);
    }}
    .g-tab-btn.active {{
      background: var(--g-blue);
      color: #FFFFFF;
      border-color: var(--g-blue);
      box-shadow: 0 4px 12px rgba(26,115,232,0.28);
    }}

    /* Content Panes */
    .g-pane {{
      display: none;
      animation: fadeIn 0.25s ease forwards;
    }}
    .g-pane.active {{
      display: block;
    }}
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Cards */
    .g-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-light);
      border-radius: 18px;
      padding: 30px;
      margin-bottom: 26px;
      box-shadow: var(--shadow-sm);
    }}
    .g-badge {{
      display: inline-block;
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.6px;
      padding: 4px 12px;
      border-radius: 999px;
      margin-bottom: 12px;
    }}

    /* 3D Flashcards */
    .flashcards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 20px;
    }}
    .fc-card {{
      perspective: 1200px;
      height: 380px;
    }}
    .fc-inner {{
      position: relative;
      width: 100%;
      height: 100%;
      text-align: left;
      transition: transform 0.55s cubic-bezier(0.4, 0.2, 0.2, 1);
      transform-style: preserve-3d;
      cursor: pointer;
    }}
    .fc-card.flipped .fc-inner {{
      transform: rotateY(180deg);
    }}
    .fc-front, .fc-back {{
      position: absolute;
      width: 100%;
      height: 100%;
      -webkit-backface-visibility: hidden;
      backface-visibility: hidden;
      border-radius: 16px;
      padding: 22px;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      border: 1.5px solid var(--border-light);
      background: #FFFFFF;
    }}
    .fc-card:hover .fc-front, .fc-card:hover .fc-back {{
      box-shadow: var(--shadow-md);
      border-color: var(--g-blue);
    }}
    .fc-back {{
      transform: rotateY(180deg);
      background: #FDFEFE;
      border-color: #34A853;
    }}

    /* Tables */
    .g-table-wrap {{
      overflow-x: auto;
      border-radius: 14px;
      border: 1px solid var(--border-light);
      margin: 18px 0;
      box-shadow: var(--shadow-sm);
    }}
    .g-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 15px;
      text-align: left;
      background: #FFFFFF;
    }}
    .g-table th {{
      background: #F1F3F4;
      padding: 14px 18px;
      font-weight: 700;
      color: var(--text-main);
      border-bottom: 2px solid var(--border-light);
    }}
    .g-table td {{
      padding: 14px 18px;
      border-bottom: 1px solid var(--border-light);
      vertical-align: top;
    }}
    .g-table tr:hover td {{
      background: #F8F9FA;
    }}

    /* Bullwhip Simulator Sliders */
    .sim-slider-box {{
      background: #F1F3F4;
      border-radius: 16px;
      padding: 22px;
      margin: 20px 0;
    }}

    /* Quiz options */
    .quiz-card {{
      background: #FFFFFF;
      border: 1.5px solid var(--border-light);
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 20px;
      box-shadow: var(--shadow-sm);
    }}
    .quiz-opt-btn {{
      display: block;
      width: 100%;
      text-align: left;
      padding: 12px 18px;
      border-radius: 10px;
      border: 1.5px solid var(--border-light);
      background: #FFFFFF;
      font-family: var(--font-sans);
      font-size: 15.5px;
      margin: 8px 0;
      cursor: pointer;
      transition: all 0.16s ease;
    }}
    .quiz-opt-btn:hover {{
      background: var(--g-blue-bg);
      border-color: var(--g-blue);
    }}
    .quiz-opt-btn.correct {{
      background: var(--g-green-bg) !important;
      border-color: var(--g-green) !important;
      color: #0D652D !important;
      font-weight: 700;
    }}
    .quiz-opt-btn.wrong {{
      background: var(--g-red-bg) !important;
      border-color: var(--g-red) !important;
      color: #A50E0E !important;
    }}

    /* Certificate Modal / View */
    .cert-box {{
      border: 8px double #1A73E8;
      background: #FFFFFF;
      padding: 40px;
      border-radius: 20px;
      text-align: center;
      box-shadow: var(--shadow-lg);
      margin-top: 30px;
    }}
  </style>
</head>
<body>
  <div class="g-color-strip"></div>

  <!-- Header -->
  <header class="g-header">
    <div style="display:flex; align-items:center; gap:16px;">
      <a href="index.html" class="g-btn" style="padding:6px 14px; font-size:13.5px;">
        &larr; Back to CSCO Portal
      </a>
      <span style="font-family:var(--font-display); font-size:20px; font-weight:700; color:var(--text-main);">
        🎓 Supply Chain 101 Executive Masterclass
      </span>
      <span class="g-badge" style="background:#E8F0FE; color:#1A73E8; margin:0;">
        8 Interactive Modules
      </span>
    </div>
    <div style="display:flex; align-items:center; gap:12px;">
      <a href="#module8" class="g-btn g-btn-primary" onclick="switchModule('module8')">
        🏆 Take Certification Exam
      </a>
    </div>
  </header>

  <div class="g-container">

    <!-- Gamification & XP Progress Bar -->
    <div class="gamification-bar">
      <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
        <span class="xp-pill">
          ⚡ XP Points: <span id="userXpCount">0</span> / 1500 XP
        </span>
        <span class="level-badge" id="userLevelBadge">
          🌱 Supply Chain Apprentice
        </span>
        <span style="font-size:14.5px; color:var(--text-sub);">
          Flashcards Mastered: <strong id="learnedCount" style="color:var(--g-green);">0</strong> / 76
        </span>
      </div>
      <div style="display:flex; align-items:center; gap:12px;">
        <button type="button" class="g-btn" onclick="resetGamificationProgress()" style="font-size:13px; padding:6px 14px;">
          ↺ Reset Progress
        </button>
      </div>
    </div>

    <!-- 8 Module Tabs -->
    <nav class="g-tabs-nav" id="moduleNavTabs">
      <button type="button" class="g-tab-btn active" onclick="switchModule('module1', this)">
        1 · 🏁 6-Stage Relay &amp; Flows
      </button>
      <button type="button" class="g-tab-btn" onclick="switchModule('module2', this)">
        2 · 🃏 76 Flip Flashcards
      </button>
      <button type="button" class="g-tab-btn" onclick="switchModule('module3', this)">
        3 · 🏢 4 Systems Relay (ERP/MES/WMS/TMS)
      </button>
      <button type="button" class="g-tab-btn" onclick="switchModule('module4', this)">
        4 · ⚙️ 4 Master Business Processes
      </button>
      <button type="button" class="g-tab-btn" style="border-color:#1A73E8; color:#1A73E8; font-weight:700;" onclick="switchModule('module5', this)">
        5 · 📡 AI Control Tower (ITC Blueprint)
      </button>
      <button type="button" class="g-tab-btn" style="border-color:#1E8E3E; color:#1E8E3E; font-weight:700;" onclick="switchModule('module6', this)">
        6 · 🌐 Alphabet Internal AI Playbook
      </button>
      <button type="button" class="g-tab-btn" onclick="switchModule('module7', this)">
        7 · 💬 Customer Conversation Decoder (25)
      </button>
      <button type="button" class="g-tab-btn" style="background:#FEF7E0; border-color:#F9AB00; color:#B06000; font-weight:700;" onclick="switchModule('module8', this)">
        8 · 🏆 CSCO Certification Exam &amp; Battle Arena
      </button>
    </nav>

    <!-- ===================================================================
         MODULE 1: THE FOUNDATIONS, 6-STAGE RELAY & 3 UNIVERSAL FLOWS
         =================================================================== -->
    <div id="module1" class="g-pane active">
      <section class="g-card" style="border-top:6px solid var(--g-blue);">
        <span class="g-badge" style="background:var(--g-blue-bg); color:var(--g-blue);">
          MODULE 1 · THE CORE RELAY RACE &amp; THREE FLOWS
        </span>
        <h2 style="font-family:var(--font-display); font-size:30px; margin:0 0 12px;">
          What Is a Supply Chain? The 6-Stage Relay Race
        </h2>
        <p style="font-size:18px; margin:0 0 16px;">
          Every physical item you touch — an <strong>Apple iPhone</strong>, a <strong>jar of Nestlé coffee</strong>, a <strong>pair of Nike sneakers</strong>, or an <strong>ITC Aashirvaad wheat packet</strong> — travels through a 6-stage relay race before reaching consumer hands:
        </p>
        <div style="background:var(--g-blue-bg); border-left:5px solid var(--g-blue); border-radius:12px; padding:18px 22px; margin-bottom:24px; font-size:17.5px; font-weight:600; color:#174EA6;">
          💡 <strong>Core Executive Fact:</strong> Supply chain operations account for <strong>60% to 80% of total Cost of Goods Sold (COGS)</strong> in product enterprises. A 2% improvement in supply chain efficiency generates more profit than a 10% increase in revenue!
        </div>

        <!-- 6-Stage Relay Visual Stepper -->
        <h3 style="font-family:var(--font-display); font-size:22px; margin:24px 0 12px;">
          The 6 Relay Stages (Click any stage to inspect):
        </h3>
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:20px;" id="relayStageNav">
          <button type="button" class="g-btn g-btn-primary" onclick="showRelayStage(0, this)">1. ⛏️ Raw Materials</button>
          <button type="button" class="g-btn" onclick="showRelayStage(1, this)">2. 🏭 Manufacturing</button>
          <button type="button" class="g-btn" onclick="showRelayStage(2, this)">3. 🏢 Regional Hub (RDC)</button>
          <button type="button" class="g-btn" onclick="showRelayStage(3, this)">4. 📦 City Depot (FDC/CFA)</button>
          <button type="button" class="g-btn" onclick="showRelayStage(4, this)">5. 🚚 Multi-Modal Transit</button>
          <button type="button" class="g-btn" onclick="showRelayStage(5, this)">6. �� Retail POS &amp; Reverse</button>
        </div>
        <div id="relayStageMount" style="background:#F8F9FA; border:1.5px solid var(--border-light); border-radius:14px; padding:22px;"></div>

        <!-- The 3 Synchronized Flows -->
        <h3 style="font-family:var(--font-display); font-size:22px; margin:32px 0 12px;">
          The 3 Synchronized Enterprise Flows
        </h3>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:18px;">
          <div style="background:#FFFFFF; border:1.5px solid #4285F4; border-radius:14px; padding:20px; box-shadow:var(--shadow-sm);">
            <h4 style="margin:0 0 8px; color:#1A73E8; font-size:18px;">�� Flow 1: Physical Goods (Downstream ──▶)</h4>
            <p style="margin:0; font-size:15px; color:var(--text-sub);">
              Raw ingredients move from farmgate/mines into manufacturing plants, transform into finished goods, and flow forward through warehouses and trucks to retail shelves and customer doorsteps.
            </p>
          </div>
          <div style="background:#FFFFFF; border:1.5px solid #EA4335; border-radius:14px; padding:20px; box-shadow:var(--shadow-sm);">
            <h4 style="margin:0 0 8px; color:#D93025; font-size:18px;">📡 Flow 2: Demand Signals (◀── Upstream)</h4>
            <p style="margin:0; font-size:15px; color:var(--text-sub);">
              Daily cash-register POS scans and consumer orders travel backward from stores to inform city depots, regional hubs, and factories what to produce next. Lags in this flow cause the <strong>Bullwhip Effect</strong>.
            </p>
          </div>
          <div style="background:#FFFFFF; border:1.5px solid #34A853; border-radius:14px; padding:20px; box-shadow:var(--shadow-sm);">
            <h4 style="margin:0 0 8px; color:#1E8E3E; font-size:18px;">�� Flow 3: Working Capital &amp; Cash (◀──▶ Cyclic)</h4>
            <p style="margin:0; font-size:15px; color:var(--text-sub);">
              Cash paid by customers, funds disbursed to suppliers, and <strong>trapped cash frozen in warehouse inventory</strong>. Measured by the <strong>Cash Conversion Cycle (CCC)</strong>.
            </p>
          </div>
        </div>

        <!-- Bullwhip Effect Simulator -->
        <h3 style="font-family:var(--font-display); font-size:22px; margin:36px 0 12px;">
          🌊 Interactive Bullwhip Effect Simulator
        </h3>
        <p style="color:var(--text-sub); font-size:16px; margin:0 0 16px;">
          Move the slider to see how a tiny shift in consumer checkout purchases creates a massive, chaotic wave of panic orders as it travels upstream to raw material suppliers:
        </p>
        <div class="sim-slider-box">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <label for="bullwhipSlider" style="font-weight:700; font-size:16px;">
              Consumer POS Demand Change: <span id="bwConsumerVal" style="color:var(--g-blue); font-weight:800;">+10%</span>
            </label>
            <span style="font-size:14px; color:var(--text-sub);">Adjust slider from -40% to +40%</span>
          </div>
          <input type="range" id="bullwhipSlider" min="-40" max="40" value="10" step="5" style="width:100%; height:8px; border-radius:5px; accent-color:var(--g-blue);" oninput="updateBullwhipSim()">
          
          <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:14px; margin-top:24px; text-align:center;">
            <div style="background:#FFFFFF; padding:16px; border-radius:12px; border:1.5px solid #DADCE0;">
              <span style="font-size:13px; font-weight:700; color:var(--text-sub);">1. RETAIL STORE</span>
              <div id="bwStoreOrder" style="font-size:22px; font-weight:800; color:#1A73E8; margin:6px 0;">+10%</div>
              <span style="font-size:12px; color:var(--text-sub);">Consumer checkout scan</span>
            </div>
            <div style="background:#FFFFFF; padding:16px; border-radius:12px; border:1.5px solid #DADCE0;">
              <span style="font-size:13px; font-weight:700; color:var(--text-sub);">2. DISTRIBUTOR / CFA</span>
              <div id="bwDistOrder" style="font-size:22px; font-weight:800; color:#F9AB00; margin:6px 0;">+18%</div>
              <span style="font-size:12px; color:var(--text-sub);">Adds safety buffer cushion</span>
            </div>
            <div style="background:#FFFFFF; padding:16px; border-radius:12px; border:1.5px solid #DADCE0;">
              <span style="font-size:13px; font-weight:700; color:var(--text-sub);">3. FACTORY / ICML</span>
              <div id="bwFactoryOrder" style="font-size:22px; font-weight:800; color:#EA4335; margin:6px 0;">+32%</div>
              <span style="font-size:12px; color:var(--text-sub);">Overtime + extra batch runs</span>
            </div>
            <div style="background:#FFFFFF; padding:16px; border-radius:12px; border:1.5px solid #DADCE0;">
              <span style="font-size:13px; font-weight:700; color:var(--text-sub);">4. TIER-1 SUPPLIER</span>
              <div id="bwSupplierOrder" style="font-size:22px; font-weight:800; color:#9334E6; margin:6px 0;">+58%</div>
              <span style="font-size:12px; color:var(--text-sub);">Massive raw material surge</span>
            </div>
          </div>
          <div style="margin-top:16px; padding:12px 16px; background:#E8F0FE; border-radius:10px; font-size:14.5px; color:#174EA6;">
            💡 <strong>How AI Eliminates This:</strong> Our <strong>Demand Sensing Agent</strong> shares daily POS scans directly with factories and suppliers in real time, preventing intermediate tiers from panic-buffering!
          </div>
        </div>
      </section>
    </div>

    <!-- ===================================================================
         MODULE 2: 76 INTERACTIVE 3D FLIP FLASHCARDS & ENCYCLOPEDIA
         =================================================================== -->
    <div id="module2" class="g-pane">
      <section class="g-card" style="border-top:6px solid #34A853;">
        <span class="g-badge" style="background:#E6F4EA; color:#1E8E3E;">
          MODULE 2 · 76 3D FLIP FLASHCARDS
        </span>
        <h2 style="font-family:var(--font-display); font-size:30px; margin:0 0 12px;">
          The Supply Chain Terminology &amp; Acronym Encyclopedia
        </h2>
        <p style="font-size:17px; margin:0 0 20px;">
          Click any flashcard to flip it. Study the <strong>plain-English explanation</strong>, <strong>real-world numerical example</strong>, and the <strong>exact discovery question to ask executive customers</strong>.
        </p>

        <!-- Flashcards Filter Controls -->
        <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-bottom:24px;">
          <input type="text" id="fcSearchInput" placeholder="🔍 Search term (e.g. SKU, S&OP, CoWoS, CFA, AIS)..." style="padding:10px 16px; border-radius:999px; border:1.5px solid var(--border-light); font-size:15px; width:300px; font-family:var(--font-sans);" oninput="filterFlashcards()">
          <button type="button" class="g-btn g-btn-primary fc-cat-btn" onclick="filterFcCategory('all', this)">All (76)</button>
          <button type="button" class="g-btn fc-cat-btn" onclick="filterFcCategory('top20', this)">⭐ Must-Know Top 20</button>
          <button type="button" class="g-btn fc-cat-btn" onclick="filterFcCategory('planning', this)">Planning</button>
          <button type="button" class="g-btn fc-cat-btn" onclick="filterFcCategory('sourcing', this)">Sourcing</button>
          <button type="button" class="g-btn fc-cat-btn" onclick="filterFcCategory('manufacturing', this)">Manufacturing</button>
          <button type="button" class="g-btn fc-cat-btn" onclick="filterFcCategory('inventory', this)">Inventory</button>
          <button type="button" class="g-btn fc-cat-btn" onclick="filterFcCategory('logistics', this)">Logistics</button>
          <button type="button" class="g-btn fc-cat-btn" onclick="filterFcCategory('tech', this)">Tech &amp; ESG</button>
          <button type="button" class="g-btn fc-cat-btn" onclick="filterFcCategory('finance', this)">Finance</button>
        </div>

        <!-- Mount Grid -->
        <div class="flashcards-grid" id="flashcardsGridMount"></div>
      </section>
    </div>

    <!-- ===================================================================
         MODULE 3: THE 4 ENTERPRISE SYSTEMS RELAY (ERP / MES / WMS / TMS)
         =================================================================== -->
    <div id="module3" class="g-pane">
      <section class="g-card" style="border-top:6px solid #F9AB00;">
        <span class="g-badge" style="background:#FEF7E0; color:#B06000;">
          MODULE 3 · ENTERPRISE SYSTEMS RELAY
        </span>
        <h2 style="font-family:var(--font-display); font-size:30px; margin:0 0 12px;">
          The 4 Enterprise Software Systems (ERP vs MES vs WMS vs TMS)
        </h2>
        <p style="font-size:17.5px; margin:0 0 20px;">
          Why do corporate silos exist? Because companies run 4 separate software databases that historically didn't talk to each other. Here is the operational baton relay:
        </p>

        <div class="g-table-wrap">
          <table class="g-table">
            <thead>
              <tr>
                <th style="width:18%;">System &amp; Market Leaders</th>
                <th style="width:22%;">Primary Operational Scope</th>
                <th style="width:25%;">Core Database Tables / Objects</th>
                <th style="width:35%;">Why It Gets Siloed &amp; How AI Bridges It</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>ERP</strong><br><span style="color:var(--text-sub); font-size:13px;">SAP S/4HANA, Oracle ERP, Microsoft Dynamics</span></td>
                <td>Central accounting, purchase orders, sales orders, master company stock balances.</td>
                <td><code style="font-family:var(--font-mono); color:#1A73E8;">MARA</code> (Material Master), <code style="font-family:var(--font-mono); color:#1A73E8;">VBAK</code> (Sales Orders), <code style="font-family:var(--font-mono); color:#1A73E8;">EKKO</code> (Purchase Orders).</td>
                <td>ERP runs on overnight batch updates. It knows a warehouse has 5,000 cases, but doesn't know which rack aisle they are in. AI agents query ERP via OData APIs and write verified transactions back in real time.</td>
              </tr>
              <tr>
                <td><strong>MES</strong><br><span style="color:var(--text-sub); font-size:13px;">Siemens Opcenter, Rockwell, AVEVA</span></td>
                <td>Shop-floor factory machines, production lines, PLC sensor telemetry, and batch quality.</td>
                <td>Work orders, machine cycle times, spindle vibration FFT, scrap defect logs.</td>
                <td>MES data is trapped in local factory historian databases. When a packaging machine breaks, ERP doesn't know for 24 hours. AI streams MES sensor data directly into BigQuery to predict failures 48 hours early.</td>
              </tr>
              <tr>
                <td><strong>WMS</strong><br><span style="color:var(--text-sub); font-size:13px;">Manhattan Active WMS, Blue Yonder, SAP EWM</span></td>
                <td>Warehouse rack shelving, forklift travel paths, wave picking, pallet LPN barcodes.</td>
                <td>Pallet LPNs, bin rack locations (Aisle/Bay/Tier), picker RF scanner tasks.</td>
                <td>WMS knows physical pallet coordinates, but doesn't know if an incoming customer order is high-margin or low-margin. AI dynamically re-slots warehouse racks based on predictive seasonal velocity.</td>
              </tr>
              <tr>
                <td><strong>TMS</strong><br><span style="color:var(--text-sub); font-size:13px;">Oracle OTM, SAP TM, MercuryGate</span></td>
                <td>Freight carrier tendering, shipping lane rating, dispatch routing, freight audit.</td>
                <td>Shipment Legs, Freight Rates, EDI 214 milestones, carrier invoices.</td>
                <td>TMS books trucks based on lowest contracted rate, but cannot predict traffic jams or ocean port strikes. AI connects live GPS/satellite telematics to dynamically re-tender delayed loads.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>

    <!-- ===================================================================
         MODULE 4: THE 4 MASTER END-TO-END BUSINESS PROCESSES
         =================================================================== -->
    <div id="module4" class="g-pane">
      <section class="g-card" style="border-top:6px solid #9334E6;">
        <span class="g-badge" style="background:#F3E8FD; color:#9334E6;">
          MODULE 4 · END-TO-END WORKFLOWS
        </span>
        <h2 style="font-family:var(--font-display); font-size:30px; margin:0 0 12px;">
          The 4 Master Business Processes Connecting the Enterprise
        </h2>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(270px, 1fr)); gap:18px; margin-top:20px;">
          <div style="background:#FFFFFF; border:1.5px solid var(--border-light); border-radius:14px; padding:20px; box-shadow:var(--shadow-sm);">
            <h3 style="color:#1A73E8; margin:0 0 10px; font-size:19px;">1. Forecast-to-Plan (S&amp;OP)</h3>
            <ol style="padding-left:20px; font-size:14.5px; line-height:1.6; margin:0; color:var(--text-sub);">
              <li>Ingest POS scans + promotional calendar</li>
              <li>Generate unconstrained baseline forecast (TimesFM)</li>
              <li>Simulate factory capacity &amp; supplier lead times</li>
              <li>Executive S&amp;OP meeting agrees on 1 consensus plan</li>
              <li>Publish Master Production Schedule (MPS) to SAP</li>
            </ol>
          </div>
          <div style="background:#FFFFFF; border:1.5px solid var(--border-light); border-radius:14px; padding:20px; box-shadow:var(--shadow-sm);">
            <h3 style="color:#1E8E3E; margin:0 0 10px; font-size:19px;">2. Source-to-Pay (S2P)</h3>
            <ol style="padding-left:20px; font-size:14.5px; line-height:1.6; margin:0; color:var(--text-sub);">
              <li>Explode BOM requirements via MRP calculation</li>
              <li>Issue automated RFQs with Should-Cost benchmarks</li>
              <li>Evaluate vendor quotes on cost, quality, and carbon</li>
              <li>Generate Purchase Order (PO) and transmit to vendor</li>
              <li>Automated 3-Way Match (PO + GR + Invoice) releases payment</li>
            </ol>
          </div>
          <div style="background:#FFFFFF; border:1.5px solid var(--border-light); border-radius:14px; padding:20px; box-shadow:var(--shadow-sm);">
            <h3 style="color:#F9AB00; margin:0 0 10px; font-size:19px;">3. Order-to-Delivery (O2D)</h3>
            <ol style="padding-left:20px; font-size:14.5px; line-height:1.6; margin:0; color:var(--text-sub);">
              <li>Customer submits sales order via EDI 850 or portal</li>
              <li>Dynamic ATP checks real-time inventory in Spanner</li>
              <li>WMS releases pick wave &amp; optimizes picker paths</li>
              <li>TMS tenders shipment to carrier based on lane rating</li>
              <li>Proof of Delivery (POD) triggers customer invoice</li>
            </ol>
          </div>
          <div style="background:#FFFFFF; border:1.5px solid var(--border-light); border-radius:14px; padding:20px; box-shadow:var(--shadow-sm);">
            <h3 style="color:#D93025; margin:0 0 10px; font-size:19px;">4. Disruption-to-Recovery</h3>
            <ol style="padding-left:20px; font-size:14.5px; line-height:1.6; margin:0; color:var(--text-sub);">
              <li>Satellite AIS or WeatherNext senses delay</li>
              <li>AI assesses blast radius on critical customer orders</li>
              <li>Google OR-Tools simulates 3 mitigation recovery options</li>
              <li>Planner approves best cost-vs-service trade-off</li>
              <li>AI writes re-routing POs and e-Way bills to SAP</li>
            </ol>
          </div>
        </div>
      </section>
    </div>

    <!-- ===================================================================
         MODULE 5: ENTERPRISE AI CONTROL TOWER — THE ITC BLUEPRINT
         =================================================================== -->
    <div id="module5" class="g-pane">
      <section class="g-card" style="border-top:6px solid #1A73E8;">
        <span class="g-badge" style="background:#E8F0FE; color:#1A73E8;">
          MODULE 5 · ENTERPRISE AI CONTROL TOWER DEEP DIVE
        </span>
        <h2 style="font-family:var(--font-display); font-size:32px; margin:0 0 12px;">
          Enterprise AI Control Tower — The ITC Blueprint
        </h2>
        <p style="font-size:18px; margin:0 0 20px;">
          How global enterprises like <strong>ITC Limited</strong> move from passive monitoring screens to autonomous, self-healing supply chain networks.
        </p>

        <!-- Why Gen-1 and Gen-2 Fail -->
        <h3 style="font-family:var(--font-display); font-size:22px; margin:24px 0 12px;">
          Why Generation-1 &amp; Generation-2 Control Towers Fail
        </h3>
        <div class="g-table-wrap">
          <table class="g-table">
            <thead>
              <tr>
                <th style="width:25%;">Generation</th>
                <th style="width:35%;">Underlying Mechanism</th>
                <th style="width:40%;">The Fatal Flaw</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Gen-1 Control Towers</strong><br><span style="color:var(--text-sub); font-size:13px;">(1995–2010)</span></td>
                <td>Manual Excel spreadsheet consolidation &amp; nightly batch dumps.</td>
                <td>Consolidating 40 spreadsheets every Tuesday means the disruption happened 72 hours ago. Planners are perpetually looking in the rearview mirror.</td>
              </tr>
              <tr>
                <td><strong>Gen-2 Control Towers</strong><br><span style="color:var(--text-sub); font-size:13px;">(2011–2022)</span></td>
                <td>Passive BI Dashboards (Tableau, PowerBI) with Red/Yellow/Green dots.</td>
                <td>A blinking red dot tells an executive a shipment is late, but cannot calculate which customer orders fail, cannot simulate recovery costs, and cannot write to SAP. Creates <strong>alert fatigue</strong> without action.</td>
              </tr>
              <tr>
                <td><strong style="color:#1A73E8;">Gen-3 AI Control Tower</strong><br><span style="color:#1A73E8; font-size:13px;">(Google Cloud &amp; Gemini)</span></td>
                <td>5-Layer Telematics Ingestion + Foundation Model Reasoning + Google OR-Tools + 1-Click SAP Writeback.</td>
                <td>Predicts disruptions 10-14 days before impact, balances financial trade-offs in seconds, and executes recovery directly into enterprise systems.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 5 Levels of Autonomy -->
        <h3 style="font-family:var(--font-display); font-size:22px; margin:32px 0 12px;">
          The 5 Levels of Control Tower Autonomy
        </h3>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(210px, 1fr)); gap:12px;">
          <div style="background:#F8F9FA; border:1px solid var(--border-light); border-radius:12px; padding:16px;">
            <strong style="color:var(--text-sub); font-size:13px;">LEVEL 1</strong>
            <h4 style="margin:4px 0 6px; font-size:16px;">Descriptive</h4>
            <p style="font-size:13.5px; margin:0; color:var(--text-sub);">"What is happening?" Shows live GPS truck and ship locations on a map.</p>
          </div>
          <div style="background:#F8F9FA; border:1px solid var(--border-light); border-radius:12px; padding:16px;">
            <strong style="color:var(--text-sub); font-size:13px;">LEVEL 2</strong>
            <h4 style="margin:4px 0 6px; font-size:16px;">Diagnostic</h4>
            <p style="font-size:13.5px; margin:0; color:var(--text-sub);">"Why did it happen?" Traces late delivery to customs hold or port congestion.</p>
          </div>
          <div style="background:#F8F9FA; border:1px solid var(--border-light); border-radius:12px; padding:16px;">
            <strong style="color:var(--text-sub); font-size:13px;">LEVEL 3</strong>
            <h4 style="margin:4px 0 6px; font-size:16px;">Predictive</h4>
            <p style="font-size:13.5px; margin:0; color:var(--text-sub);">"What will happen?" Uses WeatherNext to forecast monsoon rail disruption 5 days early.</p>
          </div>
          <div style="background:#F8F9FA; border:1px solid #1A73E8; border-radius:12px; padding:16px; background:#E8F0FE;">
            <strong style="color:#1A73E8; font-size:13px;">LEVEL 4</strong>
            <h4 style="margin:4px 0 6px; font-size:16px; color:#174EA6;">Prescriptive</h4>
            <p style="font-size:13.5px; margin:0; color:#174EA6;">"What should we do?" OR-Tools simulates 3 balanced recovery options with costs.</p>
          </div>
          <div style="background:#F8F9FA; border:1px solid #1E8E3E; border-radius:12px; padding:16px; background:#E6F4EA;">
            <strong style="color:#1E8E3E; font-size:13px;">LEVEL 5</strong>
            <h4 style="margin:4px 0 6px; font-size:16px; color:#0D652D;">Autonomous</h4>
            <p style="font-size:13.5px; margin:0; color:#0D652D;">Self-healing. Autonomously writes re-routing POs and e-Way bills to SAP.</p>
          </div>
        </div>

        <!-- The 5 Ingestion Feeds -->
        <h3 style="font-family:var(--font-display); font-size:22px; margin:32px 0 12px;">
          The 5 Real-Time Telematics &amp; Enterprise Ingestion Feeds
        </h3>
        <div class="g-table-wrap">
          <table class="g-table">
            <thead>
              <tr>
                <th>Data Feed</th>
                <th>Enterprise / Telematics Sources</th>
                <th>Data Payload &amp; Role</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>1. Ocean &amp; Air Telematics</strong></td>
                <td>Spire Satellite AIS, FlightAware ADS-B</td>
                <td>Vessel MMSI, real-time GPS coordinates, knots speed, draft depth, and airport cargo terminal congestion.</td>
              </tr>
              <tr>
                <td><strong>2. Road &amp; Rail Telematics</strong></td>
                <td>Samsara ELD, Railinc EDI 404/417, FASTag</td>
                <td>Tractor-trailer GPS location, reefer temperature logs, driver Hours of Service (HOS), and rail car siding interchanges.</td>
              </tr>
              <tr>
                <td><strong>3. Enterprise Transactions</strong></td>
                <td>SAP S/4HANA, SAP IBP, Oracle ERP</td>
                <td>Purchase orders (<code style="font-family:var(--font-mono);">EKKO</code>), sales orders (<code style="font-family:var(--font-mono);">VBAK</code>), customer priority tiers, and inventory stock balances (<code style="font-family:var(--font-mono);">MARA</code>).</td>
              </tr>
              <tr>
                <td><strong>4. Facility Operations</strong></td>
                <td>Manhattan Active WMS, Siemens MES</td>
                <td>Inbound yard appointments, dock dwell times, plant line changeovers, and pallet LPN inwarding scans.</td>
              </tr>
              <tr>
                <td><strong>5. Environmental &amp; Climate AI</strong></td>
                <td>Google DeepMind WeatherNext, Earth Engine</td>
                <td>10-15 day global precipitation forecasts, river flood stage warnings, typhoon storm surge cones, and port seismic alerts.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- ITC Operational Case Study -->
        <div style="background:#FFFFFF; border:2px solid #1A73E8; border-radius:16px; padding:26px; margin-top:28px; box-shadow:var(--shadow-md);">
          <span class="g-badge" style="background:#E8F0FE; color:#1A73E8;">
            INDIAN FMCG OPERATIONAL SCENARIO
          </span>
          <h3 style="font-family:var(--font-display); font-size:24px; margin:4px 0 12px; color:#174EA6;">
            ITC Limited: Monsoon Rail Washout Recovery Simulation
          </h3>
          <p style="font-size:16px; margin:0 0 14px;">
            <strong>Operational Context:</strong> Managing India's most complex consumer goods distribution: <strong>e-Choupal</strong> farmgate agri-procurement &rarr; 20+ <strong>ICML</strong> integrated mega-plants &rarr; 50+ <strong>CFA</strong> state-level depots &rarr; millions of retail kirana stores.
          </p>
          <p style="font-size:16px; margin:0 0 14px;">
            <strong>The Disruption:</strong> Severe monsoon rains wash out the primary South-Eastern Railway freight tracks between Vijayawada (Andhra Pradesh) and the Uluberia ICML / Kolkata CFA depot during peak festive demand. 18 rail rakes carrying 14,000 metric tons are stranded.
          </p>

          <h4 style="margin:18px 0 10px; font-size:17px; color:var(--text-main);">How the AI Control Tower Resolves It:</h4>
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:14px;">
            <div style="background:#F8F9FA; border-left:4px solid #1A73E8; padding:14px; border-radius:8px;">
              <strong>Step 1: Predictive Sensing</strong>
              <p style="font-size:14px; margin:4px 0 0; color:var(--text-sub);">WeatherNext precipitation models and Indian Railways alerts identify washout risk 48 hours prior to planned dispatch.</p>
            </div>
            <div style="background:#F8F9FA; border-left:4px solid #F9AB00; padding:14px; border-radius:8px;">
              <strong>Step 2: Impact Blast Radius</strong>
              <p style="font-size:14px; margin:4px 0 0; color:var(--text-sub);">Calculates Kolkata CFA stockout in 72 hours; affects 240 retail distributor deliveries valued at $1.8M.</p>
            </div>
            <div style="background:#F8F9FA; border-left:4px solid #34A853; padding:14px; border-radius:8px;">
              <strong>Step 3: OR-Tools Optimization</strong>
              <p style="font-size:14px; margin:4px 0 0; color:var(--text-sub);">Simulates Option A (Air freight: $420K), Option B (Wait 5 days: $1.8M lost sales), Option C (Reroute 60% via road trucks + 40% via Bilaspur rail: $142K).</p>
            </div>
            <div style="background:#F8F9FA; border-left:4px solid #9334E6; padding:14px; border-radius:8px;">
              <strong>Step 4: Autonomous Writeback</strong>
              <p style="font-size:14px; margin:4px 0 0; color:var(--text-sub);">With 1 click, AI books 140 road multi-axle trucks, generates GST e-Way bills, and writes updated delivery dates to SAP.</p>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- ===================================================================
         MODULE 6: ALPHABET'S INTERNAL AI SUPPLY CHAIN PLAYBOOK
         =================================================================== -->
    <div id="module6" class="g-pane">
      <section class="g-card" style="border-top:6px solid #1E8E3E;">
        <span class="g-badge" style="background:#E6F4EA; color:#1E8E3E;">
          MODULE 6 · ALPHABET INTERNAL AI PLAYBOOK
        </span>
        <h2 style="font-family:var(--font-display); font-size:32px; margin:0 0 12px;">
          How Alphabet Uses AI for Its Own Global Supply Chain
        </h2>
        <p style="font-size:18px; margin:0 0 20px;">
          The key differentiator Kiran Kumar Kesavarapu challenged us to master: Google does not just sell AI; <strong>Alphabet runs its multi-billion dollar global hardware, data center, and semiconductor supply chain on internal AI</strong>.
        </p>

        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:20px; margin-top:24px;">
          <div style="background:#FFFFFF; border:1.5px solid #4285F4; border-radius:16px; padding:24px; box-shadow:var(--shadow-sm);">
            <div style="font-size:32px; margin-bottom:8px;">⚡</div>
            <h3 style="color:#1A73E8; margin:0 0 8px; font-size:20px;">1. TPU Capacity &amp; CoWoS Wafer Forecasting</h3>
            <p style="font-size:15px; color:var(--text-sub); line-height:1.6; margin:0 0 12px;">
              Forecasting demand for custom Tensor Processing Units (TPU v4, v5p, v6 Trillium) across Google Search, YouTube, DeepMind, and Cloud customers using <strong>TimesFM foundation models</strong>.
            </p>
            <div style="background:#E8F0FE; padding:10px 14px; border-radius:8px; font-size:13.5px; color:#174EA6;">
              <strong>Key Factor:</strong> Models TSMC CoWoS advanced packaging lead times 18 months ahead to secure global foundry allocations.
            </div>
          </div>

          <div style="background:#FFFFFF; border:1.5px solid #34A853; border-radius:16px; padding:24px; box-shadow:var(--shadow-sm);">
            <div style="font-size:32px; margin-bottom:8px;">♻️</div>
            <h3 style="color:#1E8E3E; margin:0 0 8px; font-size:20px;">2. Circular Server Hardware Harvesting</h3>
            <p style="font-size:15px; color:var(--text-sub); line-height:1.6; margin:0 0 12px;">
              Alphabet diverts <strong>over 90% of decommissioned data center server hardware from landfills</strong>. Automated testing systems harvest processors, DDR memory modules, and SSD flash drives.
            </p>
            <div style="background:#E6F4EA; padding:10px 14px; border-radius:8px; font-size:13.5px; color:#0D652D;">
              <strong>Key Factor:</strong> Harvested server components are re-tested, re-certified, and remanufactured for secondary compute clusters.
            </div>
          </div>

          <div style="background:#FFFFFF; border:1.5px solid #EA4335; border-radius:16px; padding:24px; box-shadow:var(--shadow-sm);">
            <div style="font-size:32px; margin-bottom:8px;">🌊</div>
            <h3 style="color:#D93025; margin:0 0 8px; font-size:20px;">3. DeepMind WeatherNext Shipping Resilience</h3>
            <p style="font-size:15px; color:var(--text-sub); line-height:1.6; margin:0 0 12px;">
              Moving server racks across trans-ocean container corridors requires severe weather avoidance. DeepMind's GraphCast and WeatherNext foundation models forecast typhoons 10-14 days early.
            </p>
            <div style="background:#FCE8E6; padding:10px 14px; border-radius:8px; font-size:13.5px; color:#A50E0E;">
              <strong>Key Factor:</strong> Allows ocean logistics teams to re-route high-value server shipments around maritime storms before vessels depart port.
            </div>
          </div>

          <div style="background:#FFFFFF; border:1.5px solid #F9AB00; border-radius:16px; padding:24px; box-shadow:var(--shadow-sm);">
            <div style="font-size:32px; margin-bottom:8px;">🌱</div>
            <h3 style="color:#B06000; margin:0 0 8px; font-size:20px;">4. Carbon-Aware Compute Workload Scheduling</h3>
            <p style="font-size:15px; color:var(--text-sub); line-height:1.6; margin:0 0 12px;">
              Google's carbon-aware compute platform shifts non-urgent batch data center compute jobs (such as model training and video indexing) across global regions in real time.
            </p>
            <div style="background:#FEF7E0; padding:10px 14px; border-radius:8px; font-size:13.5px; color:#B06000;">
              <strong>Key Factor:</strong> Matches compute load to peak solar and wind generation, driving toward 24/7 carbon-free energy.
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- ===================================================================
         MODULE 7: CUSTOMER CONVERSATION DECODER (25 EXECUTIVE SCENARIOS)
         =================================================================== -->
    <div id="module7" class="g-pane">
      <section class="g-card" style="border-top:6px solid #D93025;">
        <span class="g-badge" style="background:#FCE8E6; color:#D93025;">
          MODULE 7 · 25 CUSTOMER SCENARIOS
        </span>
        <h2 style="font-family:var(--font-display); font-size:30px; margin:0 0 12px;">
          The Customer Conversation Decoder
        </h2>
        <p style="font-size:17.5px; margin:0 0 20px;">
          What executives say vs. what is actually happening inside their supply chain, the underlying root cause, which AI agent solves it, and the winning discovery question to ask.
        </p>

        <!-- Search input for decoders -->
        <div style="margin-bottom:20px;">
          <input type="text" id="decoderSearchInput" placeholder="🔍 Search executive complaint (e.g. forecast, supplier, OTIF, returns, demurrage)..." style="padding:10px 16px; border-radius:999px; border:1.5px solid var(--border-light); font-size:15px; width:340px; font-family:var(--font-sans);" oninput="filterDecoderScenarios()">
        </div>

        <div id="decoderMount" style="display:flex; flex-direction:column; gap:16px;"></div>
      </section>
    </div>

    <!-- ===================================================================
         MODULE 8: GAMIFIED 20-QUESTION CERTIFICATION EXAM & BATTLE ARENA
         =================================================================== -->
    <div id="module8" class="g-pane">
      <section class="g-card" style="border-top:6px solid #F9AB00;">
        <span class="g-badge" style="background:#FEF7E0; color:#B06000;">
          MODULE 8 · CSCO DOMAIN CERTIFICATION EXAM
        </span>
        <h2 style="font-family:var(--font-display); font-size:32px; margin:0 0 12px;">
          CSCO Domain Knowledge Battle &amp; Certification Exam
        </h2>
        <p style="font-size:17.5px; margin:0 0 20px;">
          Test your mastery across all 8 modules. Score <strong>80% or higher (16/20)</strong> to earn the official <strong>Office of the CSCO Supply Chain Domain Specialist Certificate</strong>!
        </p>

        <!-- Score Banner -->
        <div style="background:#FFFFFF; border:2px solid var(--border-light); border-radius:14px; padding:18px 24px; margin-bottom:24px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
          <div>
            <span style="font-size:15px; color:var(--text-sub);">Current Exam Score:</span>
            <span id="examScoreDisplay" style="font-size:24px; font-weight:800; color:var(--g-blue); margin-left:8px;">0 / 20</span>
          </div>
          <div id="certStatusBanner" style="font-size:15px; font-weight:600; color:var(--text-sub);">
            Answer questions below to unlock your certificate.
          </div>
        </div>

        <!-- Quiz Mount -->
        <div id="quizQuestionsMount"></div>

        <!-- Certificate Container -->
        <div id="certificateContainer" style="display:none;">
          <div class="cert-box">
            <div style="display:flex; justify-content:center; align-items:center; gap:12px; margin-bottom:12px;">
              <span style="font-size:42px;">🎓</span>
            </div>
            <h1 style="font-family:var(--font-display); font-size:34px; color:#1A73E8; margin:0 0 6px;">
              Certificate of Supply Chain Domain Mastery
            </h1>
            <p style="font-size:18px; color:var(--text-sub); margin:0 0 20px;">
              Office of the Chief Supply Chain Officer (CSCO) · Agentic Transformation
            </p>
            <p style="font-size:17px; margin:0 0 8px;">This is proudly presented to</p>
            <h2 style="font-family:var(--font-display); font-size:30px; color:#202124; margin:0 0 16px; border-bottom:2px solid #1A73E8; display:inline-block; padding-bottom:4px;">
              Zuhaib Parvez
            </h2>
            <p style="font-size:16.5px; max-width:700px; margin:0 auto 24px; color:var(--text-main); line-height:1.6;">
              For demonstrating expert domain mastery across the 6-Stage Supply Chain Relay, 76 Core Acronyms, Multi-Echelon Inventory Optimization, Enterprise AI Control Towers, and Alphabet's Internal Infrastructure Playbook.
            </p>
            <div style="display:flex; justify-content:space-around; align-items:center; margin-top:30px; border-top:1px solid #DADCE0; padding-top:20px;">
              <div>
                <strong style="color:#1A73E8; font-size:16px;">Verified Passing Score:</strong><br>
                <span id="certScoreVal" style="font-size:20px; font-weight:800;">100%</span>
              </div>
              <div>
                <strong style="color:#1E8E3E; font-size:16px;">Level Conferred:</strong><br>
                <span style="font-size:18px; font-weight:700; color:#0D652D;">👑 CSCO Enterprise Architect</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>

  </div>

  <!-- Embedded Client-Side Engine -->
  <script>
    const FLASHCARDS = {flashcards_json};
    const DECODER = {decoder_json};
    const QUIZ = {quiz_json};
    const CONTROL_TOWER = {control_tower_json};
    const ALPHABET_AI = {alphabet_ai_json};

    let userLearnedTerms = JSON.parse(localStorage.getItem('sc101_learned') || '[]');
    let userQuizAnswers = JSON.parse(localStorage.getItem('sc101_quiz') || '{{}}');
    let currentCategory = 'all';

    // Module Switcher
    function switchModule(modId, btn) {{
      document.querySelectorAll('.g-pane').forEach(p => p.classList.remove('active'));
      document.querySelectorAll('.g-tab-btn').forEach(b => b.classList.remove('active'));
      document.getElementById(modId).classList.add('active');
      if (btn) {{
        btn.classList.add('active');
      }} else {{
        const targetBtn = Array.from(document.querySelectorAll('.g-tab-btn')).find(b => b.getAttribute('onclick').includes(modId));
        if (targetBtn) targetBtn.classList.add('active');
      }}
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    // Relay Stages Data
    const RELAY_STAGES = [
      {{
        title: "Stage 1: Raw Materials & Tier-N Sourcing",
        scope: "Farms, mines, chemical plants, and semiconductor wafer fabs creating the foundational ingredients.",
        risks: "Weather crop failures, mine strikes, and hidden Tier-3 single-source chip foundry outages.",
        systems: "ERP Purchasing (EKKO), Supplier Portals, London Metal Exchange (LME) commodity pricing feeds."
      }},
      {{
        title: "Stage 2: Manufacturing & Assembly (Make)",
        scope: "Converting raw materials into packaged finished goods on high-speed factory lines.",
        risks: "Machine spindle breakdowns, lengthy tooling changeovers, and packaging seal defects.",
        systems: "Manufacturing Execution Systems (MES - Siemens Opcenter), SCADA telemetry, SAP Plant Maintenance."
      }},
      {{
        title: "Stage 3: Regional Distribution Center (RDC Hub)",
        scope: "Massive central warehouses receiving full truckloads/trainloads from factories and holding buffer stock.",
        risks: "Space congestion, slow-moving obsolete inventory (SLOB), and forklift picker travel toil.",
        systems: "Tier-1 Warehouse Management Systems (Manhattan Active WMS, Blue Yonder) and high-bay AS/RS cranes."
      }},
      {{
        title: "Stage 4: Forward Fulfillment Depot (FDC / CFA)",
        scope: "State-level depots and city fulfillment centers buffering stock close to retail stores for 24-48hr replenishment.",
        risks: "Stockouts during promotional spikes, expiration of perishable goods (FEFO violations).",
        systems: "WMS, ERP Stock Transfer Orders (STOs), and local distributor management systems (DMS)."
      }},
      {{
        title: "Stage 5: Multi-Modal Transit (Move)",
        scope: "Moving freight across ocean container ships, cargo airplanes, freight trains, and 53ft highway trucks.",
        risks: "Port congestion, container demurrage penalties, highway traffic accidents, and reefer temperature spikes.",
        systems: "Transportation Management Systems (Oracle OTM, SAP TM), Satellite AIS, Samsara ELD GPS telematics."
      }},
      {{
        title: "Stage 6: Retail POS & Circular Returns (Fulfill & Reverse)",
        scope: "Store shelves, customer checkouts, e-commerce doorsteps, and customer returns/refurbishment.",
        risks: "Retail out-of-stocks, high e-commerce return processing costs, and OTIF compliance fines.",
        systems: "Point of Sale (POS) scanners, Retail Link / EDI 852 feeds, and Reverse RMA triage engines."
      }}
    ];

    function showRelayStage(idx, btn) {{
      if (btn) {{
        document.querySelectorAll('#relayStageNav .g-btn').forEach(b => b.classList.remove('g-btn-primary'));
        btn.classList.add('g-btn-primary');
      }}
      const st = RELAY_STAGES[idx];
      document.getElementById('relayStageMount').innerHTML = `
        <h4 style="margin:0 0 8px; font-size:19px; color:#1A73E8;">${{st.title}}</h4>
        <p style="margin:0 0 10px; font-size:15.5px;"><strong>Operational Scope:</strong> ${{st.scope}}</p>
        <p style="margin:0 0 10px; font-size:15px; color:#D93025;"><strong>Critical Operational Risks:</strong> ${{st.risks}}</p>
        <p style="margin:0; font-size:14.5px; color:var(--text-sub);"><strong>Core Systems:</strong> ${{st.systems}}</p>
      `;
    }}

    // Bullwhip Simulator
    function updateBullwhipSim() {{
      const slider = document.getElementById('bullwhipSlider');
      const val = parseInt(slider.value, 10);
      const sign = val > 0 ? '+' : '';
      document.getElementById('bwConsumerVal').textContent = `${{sign}}${{val}}%`;
      document.getElementById('bwStoreOrder').textContent = `${{sign}}${{val}}%`;
      
      const dist = Math.round(val * 1.8);
      const factory = Math.round(val * 3.2);
      const supplier = Math.round(val * 5.8);

      document.getElementById('bwDistOrder').textContent = `${{dist > 0 ? '+' : ''}}${{dist}}%`;
      document.getElementById('bwFactoryOrder').textContent = `${{factory > 0 ? '+' : ''}}${{factory}}%`;
      document.getElementById('bwSupplierOrder').textContent = `${{supplier > 0 ? '+' : ''}}${{supplier}}%`;
    }}

    // 3D Flip Flashcards Engine
    function renderFlashcards() {{
      const query = (document.getElementById('fcSearchInput').value || '').toLowerCase().trim();
      const mount = document.getElementById('flashcardsGridMount');

      const filtered = FLASHCARDS.filter(fc => {{
        if (currentCategory === 'top20' && !fc.top20) return false;
        if (currentCategory !== 'all' && currentCategory !== 'top20' && fc.cat !== currentCategory) return false;
        if (query) {{
          const term = fc.term.toLowerCase();
          const full = fc.full.toLowerCase();
          const plain = fc.plain.toLowerCase();
          if (!term.includes(query) && !full.includes(query) && !plain.includes(query)) return false;
        }}
        return true;
      }});

      mount.innerHTML = filtered.map(fc => {{
        const isLearned = userLearnedTerms.includes(fc.term);
        const topBadge = fc.top20 ? '<span style="color:#B06000; font-weight:700; font-size:11px; background:#FEF7E0; padding:2px 8px; border-radius:999px; border:1px solid #F9AB00;">⭐ Top 20</span>' : '';
        return `
          <div class="fc-card" onclick="toggleCardFlip(this, event)">
            <div class="fc-inner">
              <!-- FRONT -->
              <div class="fc-front">
                <div>
                  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span style="font-family:var(--font-mono); font-size:12px; font-weight:700; color:var(--text-sub); text-transform:uppercase;">${{fc.cat}}</span>
                    ${{topBadge}}
                  </div>
                  <h3 style="font-family:var(--font-display); font-size:26px; color:#1A73E8; margin:0 0 6px;">${{fc.term}}</h3>
                  <div style="font-size:14px; font-weight:600; color:var(--text-sub); margin-bottom:14px;">${{fc.full}}</div>
                  <p style="font-size:15px; color:var(--text-main); line-height:1.55; margin:0;">
                    ${{fc.hook}}
                  </p>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid var(--border-light); padding-top:12px;">
                  <span style="font-size:12.5px; color:var(--text-sub);">Click card to flip ↺</span>
                  <button type="button" class="g-btn" style="padding:4px 12px; font-size:12.5px; ${{isLearned ? 'background:#E6F4EA; color:#1E8E3E; border-color:#34A853;' : ''}}" onclick="toggleLearnedTerm('${{fc.term}}', event)">
                    ${{isLearned ? '✓ Learned' : '○ Mark Learned'}}
                  </button>
                </div>
              </div>

              <!-- BACK -->
              <div class="fc-back">
                <div>
                  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <span style="font-family:var(--font-mono); font-size:12px; font-weight:800; color:#1E8E3E;">${{fc.term}} — PLAIN ENGLISH</span>
                    <span style="font-size:12px; color:var(--text-sub);">↺ Flip Back</span>
                  </div>
                  <p style="font-size:14px; color:var(--text-main); margin:0 0 10px; line-height:1.5;">
                    <strong>Meaning:</strong> ${{fc.plain}}
                  </p>
                  <p style="font-size:13.5px; color:var(--text-sub); margin:0 0 10px; line-height:1.45;">
                    <strong>Example:</strong> ${{fc.example}}
                  </p>
                </div>
                <div style="background:#E8F0FE; border-left:3px solid #1A73E8; border-radius:8px; padding:10px 12px; font-size:12.5px; color:#174EA6; line-height:1.45;">
                  <strong>🗣️ Customer Pitch:</strong> ${{fc.customer_tip}}
                </div>
              </div>
            </div>
          </div>
        `;
      }}).join('');

      updateGamification();
    }}

    function toggleCardFlip(cardEl, ev) {{
      if (ev.target.tagName.toLowerCase() === 'button') return;
      cardEl.classList.toggle('flipped');
    }}

    function toggleLearnedTerm(term, ev) {{
      ev.stopPropagation();
      if (userLearnedTerms.includes(term)) {{
        userLearnedTerms = userLearnedTerms.filter(t => t !== term);
      }} else {{
        userLearnedTerms.push(term);
      }}
      localStorage.setItem('sc101_learned', JSON.stringify(userLearnedTerms));
      renderFlashcards();
    }}

    function filterFcCategory(cat, btn) {{
      currentCategory = cat;
      document.querySelectorAll('.fc-cat-btn').forEach(b => b.classList.remove('g-btn-primary'));
      if (btn) btn.classList.add('g-btn-primary');
      renderFlashcards();
    }}

    function filterFlashcards() {{
      renderFlashcards();
    }}

    // Customer Decoder Engine
    function renderCustomerDecoder() {{
      const query = (document.getElementById('decoderSearchInput').value || '').toLowerCase().trim();
      const mount = document.getElementById('decoderMount');

      const filtered = DECODER.filter(sc => {{
        if (!query) return true;
        return sc.complaint.toLowerCase().includes(query) ||
               sc.meaning.toLowerCase().includes(query) ||
               sc.root_cause.toLowerCase().includes(query) ||
               sc.agent.toLowerCase().includes(query) ||
               sc.domain.toLowerCase().includes(query);
      }});

      mount.innerHTML = filtered.map((sc, idx) => `
        <div style="background:#FFFFFF; border:1.5px solid var(--border-light); border-radius:14px; padding:22px; box-shadow:var(--shadow-sm);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span class="g-badge" style="background:#FCE8E6; color:#D93025; margin:0;">${{sc.domain}}</span>
            <span style="font-size:13px; font-weight:700; color:var(--text-sub);">Scenario #${{idx + 1}}</span>
          </div>
          <h4 style="margin:6px 0 10px; font-size:17.5px; color:#202124;">
            🗣️ Executive Complaint: "${{sc.complaint}}"
          </h4>
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:12px; margin-top:12px;">
            <div style="background:#F8F9FA; padding:12px 14px; border-radius:10px; font-size:14px;">
              <strong style="color:#D93025;">What It Actually Means:</strong>
              <div style="color:var(--text-sub); margin-top:4px;">${{sc.meaning}}</div>
            </div>
            <div style="background:#F8F9FA; padding:12px 14px; border-radius:10px; font-size:14px;">
              <strong style="color:#F9AB00;">Root Cause:</strong>
              <div style="color:var(--text-sub); margin-top:4px;">${{sc.root_cause}}</div>
            </div>
          </div>
          <div style="margin-top:12px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; background:#E8F0FE; padding:12px 16px; border-radius:10px;">
            <div style="font-size:14px; color:#174EA6;">
              <strong>�� Solution Agent:</strong> ${{sc.agent}}
            </div>
            <div style="font-size:13.5px; color:#174EA6; font-style:italic;">
              <strong>🎯 Winning Question:</strong> "${{sc.question}}"
            </div>
          </div>
        </div>
      `).join('');
    }}

    function filterDecoderScenarios() {{
      renderCustomerDecoder();
    }}

    // 20-Question Certification Exam Engine
    function renderQuiz() {{
      const mount = document.getElementById('quizQuestionsMount');
      let score = 0;

      QUIZ.forEach((q, idx) => {{
        if (userQuizAnswers[idx] === q.correct) score++;
      }});

      document.getElementById('examScoreDisplay').textContent = `${{score}} / 20`;
      
      const pass = score >= 16;
      const certBanner = document.getElementById('certStatusBanner');
      if (pass) {{
        certBanner.innerHTML = `<span style="color:#1E8E3E; font-weight:700;">🎉 Certified! Score: ${{Math.round(score/20*100)}}%. Scroll down to view certificate.</span>`;
        document.getElementById('certificateContainer').style.display = 'block';
        document.getElementById('certScoreVal').textContent = `${{Math.round(score/20*100)}}% (${{score}}/20)`;
      }} else {{
        certBanner.innerHTML = `<span style="color:var(--text-sub);">Score 16 or higher to pass (Current: ${{score}}/20).</span>`;
        document.getElementById('certificateContainer').style.display = 'none';
      }}

      mount.innerHTML = QUIZ.map((q, qIdx) => {{
        const chosen = userQuizAnswers[qIdx];
        const isAnswered = chosen !== undefined;
        return `
          <div class="quiz-card">
            <div style="font-family:var(--font-display); font-size:17.5px; font-weight:700; margin-bottom:12px;">
              ${{q.q}}
            </div>
            <div>
              ${{q.options.map((opt, oIdx) => {{
                let cls = 'quiz-opt-btn';
                if (isAnswered) {{
                  if (oIdx === q.correct) cls += ' correct';
                  else if (oIdx === chosen) cls += ' wrong';
                }}
                return `
                  <button type="button" class="${{cls}}" onclick="answerQuizQuestion(${{qIdx}}, ${{oIdx}})">
                    ${{opt}}
                  </button>
                `;
              }}).join('')}}
            </div>
            ${{isAnswered ? `
              <div style="margin-top:12px; padding:12px 16px; border-radius:10px; background:#E8F0FE; border-left:4px solid #1A73E8; font-size:14.5px; color:#174EA6;">
                💡 <strong>Explanation:</strong> ${{q.explain}}
              </div>
            ` : ''}}
          </div>
        `;
      }}).join('');

      updateGamification();
    }}

    function answerQuizQuestion(qIdx, oIdx) {{
      userQuizAnswers[qIdx] = oIdx;
      localStorage.setItem('sc101_quiz', JSON.stringify(userQuizAnswers));
      renderQuiz();
    }}

    // Gamification & XP Logic
    function updateGamification() {{
      const learnedCount = userLearnedTerms.length;
      document.getElementById('learnedCount').textContent = learnedCount;

      let quizCorrect = 0;
      QUIZ.forEach((q, idx) => {{
        if (userQuizAnswers[idx] === q.correct) quizCorrect++;
      }});

      // XP Calculation: 10 XP per flashcard learned (max 760) + 37 XP per quiz correct (max 740) = 1500 XP total
      const totalXp = Math.min(1500, (learnedCount * 10) + (quizCorrect * 37));
      document.getElementById('userXpCount').textContent = totalXp;

      const badgeEl = document.getElementById('userLevelBadge');
      if (totalXp >= 1200) {{
        badgeEl.textContent = '👑 CSCO Enterprise Architect';
        badgeEl.style.borderColor = '#1E8E3E';
        badgeEl.style.color = '#0D652D';
        badgeEl.style.background = '#E6F4EA';
      }} else if (totalXp >= 600) {{
        badgeEl.textContent = '⚡ Supply Chain Operations Lead';
        badgeEl.style.borderColor = '#F9AB00';
        badgeEl.style.color = '#B06000';
        badgeEl.style.background = '#FEF7E0';
      }} else {{
        badgeEl.textContent = '🌱 Supply Chain Apprentice';
        badgeEl.style.borderColor = '#1A73E8';
        badgeEl.style.color = '#1A73E8';
        badgeEl.style.background = '#E8F0FE';
      }}
    }}

    function resetGamificationProgress() {{
      if (confirm('Reset your flashcards and exam progress?')) {{
        localStorage.removeItem('sc101_learned');
        localStorage.removeItem('sc101_quiz');
        userLearnedTerms = [];
        userQuizAnswers = {{}};
        renderFlashcards();
        renderQuiz();
      }}
    }}

    // Initialization
    window.addEventListener('DOMContentLoaded', () => {{
      showRelayStage(0, null);
      updateBullwhipSim();
      renderFlashcards();
      renderCustomerDecoder();
      renderQuiz();
    }});
  </script>
</body>
</html>
"""

def generate_markdown() -> str:
    md = [
        "# 🎓 Supply Chain 101 — Complete Plain-English Executive Master Guide",
        "",
        "> **Designed for Complete Domain Mastery**: This master guide explains supply chain operations from the ground up in plain, everyday English with **zero unexplained abbreviations**, concrete examples with real numbers, an **Enterprise AI Control Tower Blueprint (ITC Limited)**, and **Alphabet's Internal AI Supply Chain Playbook**.",
        "> �� **Interactive Learning & 3D Flashcards:** Open **[`supply_chain_101_interactive_academy.html`](supply_chain_101_interactive_academy.html)** in your browser for gamified learning, live simulators, and the CSCO Certification Exam!",
        "",
        "---",
        "",
        "## 🏁 Module 1: The 6-Stage Relay Race & Three Universal Flows",
        "",
        "Every physical item you touch travels through a 6-stage relay race before reaching consumer hands:",
        "",
        "1. **⛏️ Stage 1: Raw Materials (Tier-N Suppliers)**: Farms, mines, chemical plants, and semiconductor wafer fabs creating the foundational ingredients.",
        "2. **🏭 Stage 2: The Factory (Manufacturing & Make)**: Converting raw materials into finished goods on high-speed assembly and packaging lines.",
        "3. **🏢 Stage 3: Regional Distribution Center (RDC Hub)**: Giant central warehouses receiving full truckloads/trainloads and holding strategic buffer inventory.",
        "4. **📦 Stage 4: Forward Fulfillment Depot (FDC / CFA)**: State-level depots buffering stock close to retail stores for 24-48 hour replenishment.",
        "5. **🚚 Stage 5: Multi-Modal Transit (Move)**: Moving freight across ocean ships, cargo aircraft, freight rail, and 53-foot highway semi-trucks.",
        "6. **🛒 Stage 6: Store Shelf, Retail POS & Returns (Fulfill & Reverse)**: Retail store checkout cash registers, e-commerce doorsteps, and customer returns/recycling.",
        "",
        "### The 3 Synchronized Enterprise Flows",
        "- **📦 Flow 1: Physical Material Flow (Downstream ──▶)**: Raw materials transforming into finished goods moving toward the customer.",
        "- **📡 Flow 2: Demand & Information Flow (◀── Upstream)**: Cash-register POS scans and orders traveling backward to tell factories what to build next.",
        "- **💵 Flow 3: Working Capital & Cash Flow (◀──▶ Cyclic)**: Customer payments collected, supplier disbursements, and **trapped cash frozen in warehouse inventory**.",
        "",
        "---",
        "",
        "## 🃏 Module 2: All 76 Supply Chain Acronyms Decoded (Plain English)",
        "",
    ]

    for idx, fc in enumerate(FLASHCARDS, 1):
        star = " ⭐ *(Must-Know Top 20)*" if fc.get("top20") else ""
        md.extend([
            f"### {idx}. {fc['term']} — {fc['full']}{star}",
            f"- **What it means:** {fc['plain']}",
            f"- **Real-world example:** {fc['example']}",
            f"- **🗣️ Customer discovery question / pitch:** *\"{fc['customer_tip']}\"*",
            "",
        ])

    md.extend([
        "---",
        "",
        "## 🏢 Module 3: The 4 Enterprise Systems Relay (ERP vs MES vs WMS vs TMS)",
        "",
        "| System | Primary Role | Key Tables & Data Objects | Why Silos Happen & How AI Solves It |",
        "| :--- | :--- | :--- | :--- |",
        "| **ERP** (SAP S/4HANA, Oracle) | Central accounting, POs, Sales Orders, total stock balances | `MARA` (Materials), `VBAK` (Orders), `EKKO` (Purchase Orders) | ERP runs overnight batch updates; knows stock exists but not shelf coordinates. AI connects via OData APIs. |",
        "| **MES** (Siemens Opcenter, Rockwell) | Factory shop-floor machines, line cycles, sensor telemetry | Work orders, spindle vibration FFT, scrap defect logs | Data is trapped in plant historian SCADA databases. AI streams telemetry into BigQuery to predict failures 48h early. |",
        "| **WMS** (Manhattan Active, Blue Yonder) | Warehouse racks, forklift travel, pick waves, LPNs | Pallet LPNs, bin locations, picker RF scanner tasks | WMS manages bins but lacks customer margin context. AI dynamically re-slots racks based on seasonal pick velocity. |",
        "| **TMS** (Oracle OTM, SAP TM) | Carrier tendering, lane rating, freight tracking | Shipment legs, freight rates, EDI 214 milestones | TMS books contracted rates but cannot predict port strikes. AI connects live GPS/AIS telematics to dynamically re-tender delayed loads. |",
        "",
        "---",
        "",
        "## ⚙️ Module 4: The 4 Master End-to-End Business Processes",
        "",
        "### 1. Forecast-to-Plan (S&OP / IBP)",
        "1. Ingest daily POS scans, weather signals, and marketing promotion calendars.",
        "2. Generate unconstrained baseline demand forecast using TimesFM.",
        "3. Simulate factory line capacity and supplier component lead times.",
        "4. Executive S&OP meeting balances Revenue, Fill Rate, and Working Capital on ONE consensus plan.",
        "5. Publish Master Production Schedule (MPS) and MRP purchase requisitions to SAP.",
        "",
        "### 2. Source-to-Pay (S2P)",
        "1. MRP explodes BOM requirements across engineering assemblies.",
        "2. Issue autonomous RFQs benchmarked against London Metal Exchange should-cost models.",
        "3. Evaluate vendor quotes on cost, quality PPM, and carbon tariffs.",
        "4. Issue binding Purchase Order (PO) with precise Incoterms.",
        "5. Automated 3-Way Match (PO + Goods Receipt + Invoice) releases payment without manual billing disputes.",
        "",
        "### 3. Order-to-Delivery (O2D)",
        "1. Customer places order via EDI 850 or corporate portal.",
        "2. Sub-50ms Available-to-Promise (ATP) reserves stock for high-margin contracted accounts.",
        "3. WMS generates optimized picker walking paths and dock wave assignments.",
        "4. TMS tenders load to lowest-cost carrier based on lane rating.",
        "5. Electronic Proof of Delivery (ePOD) triggers automated customer billing.",
        "",
        "### 4. Disruption-to-Recovery (War Room)",
        "1. Satellite AIS or WeatherNext senses shipping disruption 5-10 days early.",
        "2. Assess blast radius on critical customer delivery commitments.",
        "3. Google OR-Tools evaluates multi-objective trade-offs (Cost vs Service vs Carbon).",
        "4. Leadership approves optimal recovery plan.",
        "5. AI autonomously writes re-routing POs and e-Way bills to SAP.",
        "",
        "---",
        "",
        "## 📡 Module 5: Enterprise AI Control Tower Deep Dive — The ITC Blueprint",
        "",
        "### Why Gen-1 and Gen-2 Control Towers Fail",
        "- **Gen-1 (Excel Spreadsheets)**: Manual consolidation creates a 72-hour lag. You are perpetually looking in the rearview mirror.",
        "- **Gen-2 (Passive BI Dashboards)**: Blinking red dots create alert fatigue without action. They tell you a ship is late, but cannot calculate affected customer orders or write fixes to SAP.",
        "- **Gen-3 (AI Control Tower)**: Senses disruptions 10 days early, simulates financial trade-offs in seconds with OR-Tools, and executes closed-loop writebacks.",
        "",
        "### The 5 Levels of Autonomy",
        "1. **Level 1 (Descriptive)**: What is happening? (Live GPS tracking on a map).",
        "2. **Level 2 (Diagnostic)**: Why did it happen? (Root-cause analysis tracing port congestion).",
        "3. **Level 3 (Predictive)**: What will happen? (WeatherNext forecasting typhoon rail washout 5 days early).",
        "4. **Level 4 (Prescriptive)**: What should we do? (OR-Tools optimizing cost vs fill rate trade-offs).",
        "5. **Level 5 (Autonomous)**: Closed-loop execution. (Writing re-routing POs and e-Way bills to SAP).",
        "",
        "### The ITC Limited Operational Scenario",
        "- **Upstream**: Ingesting **e-Choupal** farmgate village procurement feeds (leaf tobacco, wheat, soybean) across Andhra Pradesh and Karnataka.",
        "- **Midstream**: Scheduling **ICML** (Integrated Consumer Goods Manufacturing & Logistics) high-speed lines and automated AS/RS warehouses.",
        "- **Downstream**: Monitoring **CFA** (Carrying & Forwarding Agent) state-level depot buffer stocks.",
        "- **Monsoon Recovery**: When rains wash out the Vijayawada-Kolkata rail line, the AI evaluates 3 options and executes a dedicated road fleet bypass to preserve 98.4% fill rate with only $142K in extra freight, avoiding $1.8M in lost sales.",
        "",
        "---",
        "",
        "## 🌐 Module 6: Alphabet's Internal AI Supply Chain Playbook",
        "",
        "1. **TPU Capacity & CoWoS Wafer Forecasting**: Using **TimesFM** to model multi-year AI accelerator demand across Search, YouTube, DeepMind, and Cloud customers, securing TSMC advanced packaging reservations 18 months ahead.",
        "2. **Circular Server Hardware Harvesting**: Diverting **over 90% of decommissioned server hardware from landfills** by harvesting processors, memory, and flash drives for remanufacturing into secondary compute clusters.",
        "3. **DeepMind WeatherNext Maritime Resilience**: Predicting typhoon storm paths 10-14 days early with neural atmospheric models to route high-value server racks safely across oceans.",
        "4. **Carbon-Aware Compute Scheduling**: Shifting data center computing tasks across global regions in real time to match peak solar and wind renewable energy.",
        "",
        "---",
        "",
        "## 💬 Module 7: Customer Conversation Decoder (25 Executive Scenarios)",
        "",
    ])

    for idx, sc in enumerate(CUSTOMER_DECODER, 1):
        md.extend([
            f"### Scenario {idx}: {sc['domain']}",
            f"- **🗣️ What Executive Says:** *\"{sc['complaint']}\"*",
            f"- **🔍 What It Actually Means:** {sc['meaning']}",
            f"- **⚠️ Root Cause:** {sc['root_cause']}",
            f"- **💡 Solution Agent:** {sc['agent']}",
            f"- **🎯 Winning Discovery Question:** *\"{sc['question']}\"*",
            "",
        ])

    md.extend([
        "---",
        "",
        "## 🏆 Module 8: CSCO Certification Exam (20 Questions & Answer Key)",
        "",
    ])

    for idx, q in enumerate(QUIZ, 1):
        correct_text = q['options'][q['correct']]
        md.extend([
            f"### Question {idx}",
            f"**{q['q']}**",
            "",
            f"**Correct Answer:** {correct_text}",
            f"- *Explanation:* {q['explain']}",
            "",
        ])

    return "\n".join(md)

def main():
    print("Building Supply Chain 101 Executive Masterclass...")
    
    # 1. Generate HTML
    html_content = generate_html()
    (ROOT / "supply_chain_101_interactive_academy.html").write_text(html_content, encoding="utf-8")
    print(f"Wrote supply_chain_101_interactive_academy.html ({len(html_content):,} bytes)")

    # 2. Generate Markdown Guide
    md_content = generate_markdown()
    (ROOT / "SUPPLY_CHAIN_101_MASTER_GUIDE.md").write_text(md_content, encoding="utf-8")
    print(f"Wrote SUPPLY_CHAIN_101_MASTER_GUIDE.md ({len(md_content):,} bytes)")

    # 3. Synchronize across distribution folders
    for sub in ["docs", "zipline_dist", "dist/itc_limited"]:
        dest_dir = ROOT / sub
        if dest_dir.exists():
            (dest_dir / "supply_chain_101_interactive_academy.html").write_text(html_content, encoding="utf-8")
            (dest_dir / "SUPPLY_CHAIN_101_MASTER_GUIDE.md").write_text(md_content, encoding="utf-8")
            print(f"Synchronized to {sub}/")

    print("\n✅ Masterclass build complete!")

if __name__ == "__main__":
    main()

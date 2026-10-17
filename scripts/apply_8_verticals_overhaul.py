#!/usr/bin/env python3
"""Overhaul build_site.py:
1. Dynamically inject DEPARTMENTS, PERSONAS, and AGENTS from data/supply_chain_catalog.json
2. Add unique SVG watermarks for V7 (tmd_retail_network) and V4 (multi_echelon_buffer)
3. Add interactive CAD stage for TM&D (tmd_retail_network)
4. Update PERIODIC_GROUPS and PERIODIC_AGENT_META with all 35 agents
5. Update getAgentSellingMeta with TM&D, MEIO, Warehousing data and connectors
6. Update renderVerticalWorkflowStrip with TM&D and MEIO workflows
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD_SITE = ROOT / "build_site.py"

content = BUILD_SITE.read_text(encoding="utf-8")

# 1. Replace hardcoded DEPARTMENTS, PERSONAS, AGENTS block (lines ~4095 to ~6420)
old_data_block_pattern = re.compile(
    r"\s+/\* 1\. EIGHT CANONICAL OPERATIONAL VERTICALS UNDER THE CSCO.*?"
    r"const AGENTS = \{.*?\n    \};",
    re.DOTALL
)

replacement_data_block = """    /* 1. EIGHT CANONICAL OPERATIONAL VERTICALS UNDER THE CSCO */
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
    const AGENTS = __EMBEDDED_AGENTS_JSON__;"""

new_content, n = old_data_block_pattern.subn(replacement_data_block, content, count=1)
if n == 0:
    print("Warning: Could not match old data block via regex, trying alternative...")
    # Try finding markers
    start_marker = "/* 1. EIGHT CANONICAL OPERATIONAL VERTICALS UNDER THE CSCO"
    end_marker = "const EMBEDDED_WEBP_BLOBS = __EMBEDDED_WEBP_BLOBS__;"
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    if start_idx != -1 and end_idx != -1:
        # Find preceding indent
        pre_idx = content.rfind("\n", 0, start_idx) + 1
        new_content = content[:pre_idx] + replacement_data_block + "\n\n    /* BASE64 EMBEDDED DESIGN ASSETS (BRAND LOGOS & SPARKLES ONLY) */\n    " + content[end_idx:]
        print("Replaced data block using markers successfully.")
    else:
        raise ValueError("Could not find start or end markers for data block!")
else:
    print("Replaced data block successfully with regex.")

# 2. Update build_html to load and replace JSONs
build_html_start = "def build_html() -> str:\n    blobs_js = extract_embedded_webp_blobs()\n    twins_js = load_all_twins_json()"
build_html_replacement = """def build_html() -> str:
    blobs_js = extract_embedded_webp_blobs()
    twins_js = load_all_twins_json()

    catalog_path = ROOT / "data" / "supply_chain_catalog.json"
    cat_data = json.loads(catalog_path.read_text(encoding="utf-8"))
    depts_js = json.dumps(cat_data["departments"], indent=2, ensure_ascii=False)
    personas_js = json.dumps(cat_data["personas"], indent=2, ensure_ascii=False)
    agents_js = json.dumps(cat_data["agents"], indent=2, ensure_ascii=False)"""

new_content = new_content.replace(build_html_start, build_html_replacement)

build_html_end = """    html = html.replace("__EMBEDDED_WEBP_BLOBS__", blobs_js)
    html = html.replace("__EMBEDDED_TWINS_JSON__", twins_js)
    return html"""

build_html_end_replacement = """    html = html.replace("__EMBEDDED_WEBP_BLOBS__", blobs_js)
    html = html.replace("__EMBEDDED_TWINS_JSON__", twins_js)
    html = html.replace("__EMBEDDED_DEPARTMENTS_JSON__", depts_js)
    html = html.replace("__EMBEDDED_PERSONAS_JSON__", personas_js)
    html = html.replace("__EMBEDDED_AGENTS_JSON__", agents_js)
    return html"""

new_content = new_content.replace(build_html_end, build_html_end_replacement)

# 3. Add tmd_retail_network and multi_echelon_buffer to renderSupplyChainWatermarkSvg
watermark_func_anchor = "function renderSupplyChainWatermarkSvg(watermarkType, color, cssClass = 'dept-stage-svg') {\n      if (watermarkType === 'demand_wave') {"
watermark_func_replacement = """function renderSupplyChainWatermarkSvg(watermarkType, color, cssClass = 'dept-stage-svg') {
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
      if (watermarkType === 'demand_wave') {"""

new_content = new_content.replace(watermark_func_anchor, watermark_func_replacement)

# 4. Add CAD state variable let tmdStockSync = true;
cad_var_anchor = "let plantFiniteOpt = true;\n    let controlTowerUnified = true;"
cad_var_replacement = "let plantFiniteOpt = true;\n    let controlTowerUnified = true;\n    let tmdStockSync = true;"
new_content = new_content.replace(cad_var_anchor, cad_var_replacement)

# 5. Add tmd_retail_network to renderInteractiveCadStage
cad_stage_anchor = "if (cadType === 'plant_oee_twin') {"
cad_stage_tmd = """if (cadType === 'tmd_retail_network') {
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
      if (cadType === 'plant_oee_twin') {"""

new_content = new_content.replace(cad_stage_anchor, cad_stage_tmd, 1)

# 6. Update renderVerticalWorkflowStrip with TM&D and MEIO
workflow_func_anchor = "if (dept.id === 'manufacturing_prod') {"
workflow_func_replacement = """if (dept.id === 'inventory_meio') {
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
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Multi-echelon inventory pooling, regional safety stock $Z \\cdot \\sigma$, and transit pipeline buffering.</div>
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
      if (dept.id === 'manufacturing_prod') {"""

new_content = new_content.replace(workflow_func_anchor, workflow_func_replacement)

# 7. Update PERIODIC_AGENT_META and PERIODIC_GROUPS
periodic_meta_anchor = "fleetflow_dispatch:              { code: '701', sym: 'Ff', short: 'FleetFlow Maps',  group: 'trade_mkt_dist',     layer: 'OR-Tools + Vertex ADK', layerColor: '#f59e0b', trigger: 'Event-Driven',      trigIcon: '⚡' },"
periodic_meta_replacement = """fleetflow_dispatch:              { code: '601', sym: 'Ff', short: 'FleetFlow Maps',  group: 'logistics_fleet',    layer: 'OR-Tools + Google Maps', layerColor: '#f59e0b', trigger: 'Event-Driven',      trigIcon: '⚡' },
      // 07 · TM&D (Trade Marketing & Distribution Last-Mile)
      field_beat_distributor_sync_agent: { code: '701', sym: 'Bs', short: 'BeatSync FSO', group: 'trade_mkt_dist', layer: 'OR-Tools + Google Maps', layerColor: '#f59e0b', trigger: 'Event-Driven',      trigIcon: '⚡' },
      planogram_merchandising_vision_auditor: { code: '702', sym: 'Sv', short: 'ShelfVision IR', group: 'trade_mkt_dist', layer: 'Gemini 3.8 Flash Vision', layerColor: '#3b82f6', trigger: 'Event-Driven',      trigIcon: '⚡' },
      trade_scheme_claims_reconciler: { code: '703', sym: 'Sg', short: 'SchemeGuard', group: 'trade_mkt_dist', layer: 'BigQuery + Vertex ADK', layerColor: '#10b981', trigger: 'Scheduled',         trigIcon: '⏱️' },"""

new_content = new_content.replace(periodic_meta_anchor, periodic_meta_replacement)

# Update PERIODIC_GROUPS counts
new_content = new_content.replace(
    "{ id: 'logistics_fleet',     shortTab: 'Logistics (V6)',       title: '06 · LOGISTICS — MULTI-MODAL FLEET & TRANSIT (V6)',          color: '#ff8c00', count: 6 },",
    "{ id: 'logistics_fleet',     shortTab: 'Logistics (V6)',       title: '06 · LOGISTICS — MULTI-MODAL FLEET & TRANSIT (V6)',          color: '#ff8c00', count: 7 },"
)
new_content = new_content.replace(
    "{ id: 'trade_mkt_dist',      shortTab: 'TM&D (V7)',            title: '07 · TM&D — TRADE MARKETING & DISTRIBUTION LAST-MILE (V7)',   color: '#f59e0b', count: 1 },",
    "{ id: 'trade_mkt_dist',      shortTab: 'TM&D (V7)',            title: '07 · TM&D — TRADE MARKETING & DISTRIBUTION LAST-MILE (V7)',   color: '#f59e0b', count: 3 },"
)

# 8. Update connectorsByDept and defaultDataByDept
conn_anchor = "circular_enable: [\n          'SAP S/4HANA SD, QM, EHS & CO-PA',"
conn_replacement = """trade_mkt_dist: [
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
          'SAP S/4HANA SD, QM, EHS & CO-PA',"""

new_content = new_content.replace(conn_anchor, conn_replacement)

data_dept_anchor = "circular_enable: {\n          privateData: 'Loop / Narvar RMA Logs,"
data_dept_replacement = """trade_mkt_dist: {
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
          privateData: 'Loop / Narvar RMA Logs,"""

new_content = new_content.replace(data_dept_anchor, data_dept_replacement)

BUILD_SITE.write_text(new_content, encoding="utf-8")
print("Successfully overhauled build_site.py.")

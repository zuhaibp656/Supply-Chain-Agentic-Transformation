#!/usr/bin/env python3
"""
Ensure every Operating Pillar has a perceptually distinct color across:
1. Canonical 6-Pillar Supply Chain Architecture (`index.html`, `data/supply_chain_catalog.json`):
   - 01 · Planning & Strategy (`demand_sop`): #2563eb (Royal Blue)
   - 02 · Sourcing & Procurement (`sourcing_procurement`): #7c3aed (Executive Violet)
   - 03 · Manufacturing & Production (`manufacturing_prod`): #ea580c (Industrial Amber-Orange)
   - 04 · Inventory & Warehousing (`inventory_warehouse`): #0284c7 (Cerulean Cyan)
   - 05 · Distribution & Logistics (`logistics_fleet`): #059669 (Emerald Green)
   - 06 · Returns & Reverse Logistics (`circular_enable`): #e11d48 (Crimson Rose — replaces #0d9488 Teal Green)
2. `renderSupplyChainWatermarkSvg` (`circular_loop` SVG stage) & 5-Stage Circular Recovery Loop banner:
   - Replace hardcoded #10b981 / #00d2ff / #34d399 green/teal accents inside `circular_loop` and `circular_enable` banner with `${color}` (#e11d48 Crimson Rose), #f59e0b (Amber), and #8b5cf6 (Violet).
3. Enterprise Twin Generator & Cached V2 Twins (`enterprise_twin/schema.py`, `domain_synthesizer.py`, `research_engine.py`, `data/twins/v2/*.json`, `EMBEDDED_TWINS_V2`):
   - Enforce perceptual color uniqueness across all 5-7 custom Operating Pillars in every Company Twin.
"""

import colorsys
import json
import re
import shutil
from pathlib import Path

ROOT = Path("/usr/local/google/home/zuhaibp/Supply_chain_Agentic_Transformation")
INDEX_HTML = ROOT / "index.html"
CATALOG_JSON = ROOT / "data/supply_chain_catalog.json"
TWINS_DIR = ROOT / "data/twins/v2"

EXECUTIVE_PILLAR_PALETTE = [
    "#2563eb",  # 01 Royal Blue
    "#7c3aed",  # 02 Executive Violet
    "#ea580c",  # 03 Industrial Amber-Orange
    "#0284c7",  # 04 Cerulean Cyan
    "#059669",  # 05 Emerald Green
    "#e11d48",  # 06 Crimson Rose
    "#d97706",  # 07 Warm Gold
    "#4f46e5",  # 08 Deep Indigo
]


def hex_to_rgb(hex_str: str):
    h = hex_str.strip().lstrip("#")
    if len(h) != 6:
        return (37, 99, 235)
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def colors_too_similar(hex1: str, hex2: str) -> bool:
    if hex1.lower() == hex2.lower():
        return True
    r1, g1, b1 = [x / 255.0 for x in hex_to_rgb(hex1)]
    r2, g2, b2 = [x / 255.0 for x in hex_to_rgb(hex2)]
    h1, l1, s1 = colorsys.rgb_to_hls(r1, g1, b1)
    h2, l2, s2 = colorsys.rgb_to_hls(r2, g2, b2)
    hue_diff = min(abs(h1 - h2), 1.0 - abs(h1 - h2)) * 360.0
    rgb_dist = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
    # Two greens/teals (#059669 and #0d9488) have hue_diff ~14 deg and small rgb_dist
    return hue_diff < 22.0 or rgb_dist < 0.16


def deduplicate_pillar_colors(pillars: list) -> list:
    used_colors = []
    for idx, p in enumerate(pillars):
        raw_c = str(p.get("color", "")).strip()
        # Replace legacy #0d9488 on 6th/circular pillar immediately with #e11d48
        if raw_c.lower() == "#0d9488":
            raw_c = "#e11d48"
        if not re.match(r"^#[0-9a-fA-F]{6}$", raw_c):
            raw_c = EXECUTIVE_PILLAR_PALETTE[idx % len(EXECUTIVE_PILLAR_PALETTE)]

        if any(colors_too_similar(raw_c, prev) for prev in used_colors):
            # Pick first palette color that isn't too similar to any already used color
            replacement = None
            for cand in EXECUTIVE_PILLAR_PALETTE:
                if not any(colors_too_similar(cand, prev) for prev in used_colors):
                    replacement = cand
                    break
            if not replacement:
                replacement = EXECUTIVE_PILLAR_PALETTE[idx % len(EXECUTIVE_PILLAR_PALETTE)]
            raw_c = replacement

        p["color"] = raw_c
        used_colors.append(raw_c)
    return pillars


def update_catalog_json():
    data = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    if "departments" in data and "circular_enable" in data["departments"]:
        data["departments"]["circular_enable"]["color"] = "#e11d48"
    if "valueChains" in data and "p2r" in data["valueChains"]:
        data["valueChains"]["p2r"]["color"] = "#e11d48"
    CATALOG_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("[OK] Updated data/supply_chain_catalog.json (circular_enable & p2r -> #e11d48)")


def update_twins_v2() -> dict:
    embedded = {}
    for path in sorted(TWINS_DIR.glob("*.json")):
        twin = json.loads(path.read_text(encoding="utf-8"))
        pillars = twin.get("custom_pillars") or []
        if pillars:
            deduplicate_pillar_colors(pillars)
            twin["custom_pillars"] = pillars
        path.write_text(json.dumps(twin, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        slug = twin.get("company", {}).get("slug") or path.stem
        embedded[slug] = twin
        colors = [p.get("color") for p in pillars]
        print(f"[OK] Normalized twin {path.name}: {len(pillars)} pillars -> {colors}")
    return embedded


def update_python_modules():
    # 1. enterprise_twin/schema.py
    schema_path = ROOT / "enterprise_twin/schema.py"
    s_txt = schema_path.read_text(encoding="utf-8")
    s_txt_new = s_txt.replace(
        "Hex accent color from executive palette (#2563eb, #7c3aed, #ea580c, #0284c7, #059669, #0d9488, #d97706, #dc2626)",
        "Hex accent color from executive palette (#2563eb, #7c3aed, #ea580c, #0284c7, #059669, #e11d48, #d97706, #4f46e5)",
    )
    schema_path.write_text(s_txt_new, encoding="utf-8")

    # 2. enterprise_twin/tools/domain_synthesizer.py
    synth_path = ROOT / "enterprise_twin/tools/domain_synthesizer.py"
    d_txt = synth_path.read_text(encoding="utf-8")
    d_txt_new = d_txt.replace('"#0d9488"', '"#e11d48"')
    synth_path.write_text(d_txt_new, encoding="utf-8")

    # 3. enterprise_twin/tools/research_engine.py
    re_path = ROOT / "enterprise_twin/tools/research_engine.py"
    r_txt = re_path.read_text(encoding="utf-8")
    r_txt = r_txt.replace(
        'palette = ["#2563eb", "#7c3aed", "#ea580c", "#0284c7", "#059669", "#0d9488", "#d97706"]',
        'palette = ["#2563eb", "#7c3aed", "#ea580c", "#0284c7", "#059669", "#e11d48", "#d97706", "#4f46e5"]',
    )
    # Also ensure _normalize_org_pillars_partition deduplicates identical/close colors across pillars
    old_color_assign = """        color = str(p.get("color", "")).strip()
        if not re.match(r"^#[0-9a-fA-F]{6}$", color):
            color = palette[idx % len(palette)]"""
    new_color_assign = """        color = str(p.get("color", "")).strip()
        if color.lower() == "#0d9488":
            color = "#e11d48"
        if not re.match(r"^#[0-9a-fA-F]{6}$", color):
            color = palette[idx % len(palette)]
        used_colors = [prev.get("color", "").lower() for prev in non_empty]
        if color.lower() in used_colors or (color.lower() == "#0d9488" and "#059669" in used_colors):
            for cand in palette:
                if cand.lower() not in used_colors:
                    color = cand
                    break"""
    if old_color_assign in r_txt:
        r_txt = r_txt.replace(old_color_assign, new_color_assign, 1)
    re_path.write_text(r_txt, encoding="utf-8")
    print("[OK] Updated enterprise_twin/schema.py, domain_synthesizer.py, and research_engine.py")


def update_index_html(embedded_twins: dict):
    html = INDEX_HTML.read_text(encoding="utf-8")

    # 1. Replace circular_enable v-tab button accent
    html = html.replace(
        'data-vtab="circular_enable" onclick="switchPeriodicGroupTab(\'circular_enable\', this)" style="--v-accent: #0d9488;"',
        'data-vtab="circular_enable" onclick="switchPeriodicGroupTab(\'circular_enable\', this)" style="--v-accent: #e11d48;"',
    )

    # 2. Replace DEPARTMENTS["circular_enable"].color (#0d9488 -> #e11d48)
    html = re.sub(
        r'("circular_enable"\s*:\s*\{[^}]*?"color"\s*:\s*)"#0d9488"',
        r'\1"#e11d48"',
        html,
        count=1,
        flags=re.DOTALL,
    )

    # 3. Replace VALUE_CHAINS["p2r"].color (#0d9488 -> #e11d48)
    html = re.sub(
        r'("p2r"\s*:\s*\{[^}]*?"color"\s*:\s*)"#0d9488"',
        r'\1"#e11d48"',
        html,
        count=1,
        flags=re.DOTALL,
    )

    # 4. Replace PERIODIC_GROUPS circular_enable color (#0d9488 -> #e11d48)
    html = re.sub(
        r'(\{\s*id:\s*"circular_enable",\s*num:\s*"06",\s*name:\s*"Returns & Reverse Logistics",\s*color:\s*)"#0d9488"',
        r'\1"#e11d48"',
        html,
        count=1,
    )

    # 5. Replace PILLAR_PROOF_BENCHMARKS circular_enable color (#0d9488 -> #e11d48)
    html = re.sub(
        r"(circular_enable\s*:\s*\{\s*deptId:\s*'circular_enable',\s*num:\s*'06',\s*name:\s*'06\s*·\s*Returns & Reverse Logistics',\s*color:\s*)'#0d9488'",
        r"\1'#e11d48'",
        html,
        count=1,
    )

    # 6. Replace cs_carrefour case study color (#0d9488 -> #e11d48)
    html = html.replace(
        "id: 'cs_carrefour',\n    company: 'Carrefour & Google Cloud',\n    industry: 'Global Grocery & Omnichannel Retail',\n    color: '#0d9488'",
        "id: 'cs_carrefour',\n    company: 'Carrefour & Google Cloud',\n    industry: 'Global Grocery & Omnichannel Retail',\n    color: '#e11d48'",
    )

    # 7. Update `circular_loop` SVG watermark in `renderSupplyChainWatermarkSvg` so it uses ${color} (#e11d48), #f59e0b, and #8b5cf6 instead of green/cyan (#10b981 / #00d2ff)
    old_circular_svg = """  } else if (watermarkType === 'circular_loop') {
    shapes = `
      <!-- Circular Economy Loop & ESG Leaf/Turbine -->
      <circle cx="150" cy="80" r="46" stroke="${color}" stroke-width="2" stroke-dasharray="18 8" fill="none" class="svg-spin-slow" style="transform-origin: 150px 80px;" />
      <circle cx="150" cy="80" r="32" stroke="#00d2ff" stroke-width="1.5" stroke-dasharray="10 6" fill="none" />
      <path d="M 150 48 C 168 48, 175 68, 150 85 C 125 68, 132 48, 150 48 Z" stroke="${color}" stroke-width="2" fill="${color}" fill-opacity="0.2" class="svg-pulse-node" />
      <path d="M 150 85 L 150 105" stroke="${color}" stroke-width="2" />
      <!-- ESG Bar Chart Left -->
      <rect x="30" y="85" width="12" height="45" rx="2" fill="${color}" fill-opacity="0.3" stroke="${color}" stroke-width="1.5" />
      <rect x="50" y="65" width="12" height="65" rx="2" fill="#00d2ff" fill-opacity="0.3" stroke="#00d2ff" stroke-width="1.5" />
      <rect x="70" y="45" width="12" height="85" rx="2" fill="#10b981" fill-opacity="0.4" stroke="#10b981" stroke-width="1.5" />
    `;
  }"""
    new_circular_svg = """  } else if (watermarkType === 'circular_loop') {
    shapes = `
      <!-- Circular Economy Loop & Reverse Recovery Core -->
      <circle cx="150" cy="80" r="46" stroke="${color}" stroke-width="2" stroke-dasharray="18 8" fill="none" class="svg-spin-slow" style="transform-origin: 150px 80px;" />
      <circle cx="150" cy="80" r="32" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="10 6" fill="none" />
      <path d="M 150 48 C 168 48, 175 68, 150 85 C 125 68, 132 48, 150 48 Z" stroke="${color}" stroke-width="2" fill="${color}" fill-opacity="0.22" class="svg-pulse-node" />
      <path d="M 150 85 L 150 105" stroke="${color}" stroke-width="2" />
      <!-- Reverse Recovery & Recommerce Telemetry Bars Left -->
      <rect x="30" y="85" width="12" height="45" rx="2" fill="#8b5cf6" fill-opacity="0.3" stroke="#8b5cf6" stroke-width="1.5" />
      <rect x="50" y="65" width="12" height="65" rx="2" fill="#f59e0b" fill-opacity="0.32" stroke="#f59e0b" stroke-width="1.5" />
      <rect x="70" y="45" width="12" height="85" rx="2" fill="${color}" fill-opacity="0.4" stroke="${color}" stroke-width="1.5" />
    `;
  }"""
    if old_circular_svg in html:
        html = html.replace(old_circular_svg, new_circular_svg, 1)
        print("[OK] Updated circular_loop SVG watermark in renderSupplyChainWatermarkSvg")

    # 8. Update 5-Stage Circular Recovery Loop banner inside openDepartmentPage so it uses Crimson Rose (#e11d48) instead of emerald green
    old_loop_banner = """      <div style="margin: 0 0 24px 0; padding: 16px 20px; border-radius: 14px; background: linear-gradient(135deg, rgba(16, 185, 129, 0.08), rgba(6, 182, 212, 0.05)); border: 1px solid rgba(16, 185, 129, 0.28);">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:12px;">
          <span style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:#34d399;">♻️ 5-Stage Circular Recovery Loop (Plan-to-Recovery · P2R)</span>"""
    new_loop_banner = """      <div style="margin: 0 0 24px 0; padding: 16px 20px; border-radius: 14px; background: linear-gradient(135deg, rgba(225, 29, 72, 0.08), rgba(245, 158, 11, 0.05)); border: 1px solid rgba(225, 29, 72, 0.28);">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:12px;">
          <span style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:#e11d48;">♻️ 5-Stage Circular Recovery Loop (Plan-to-Recovery · P2R)</span>"""
    if old_loop_banner in html:
        html = html.replace(old_loop_banner, new_loop_banner, 1)

    # 9. Re-embed EMBEDDED_TWINS_V2 in index.html
    embedded_json_line = "    const EMBEDDED_TWINS_V2 = " + json.dumps(embedded_twins, ensure_ascii=False) + ";"
    html, n_sub = re.subn(
        r"^[ \t]*const EMBEDDED_TWINS_V2 = \{.*?\};$",
        lambda _: embedded_json_line,
        html,
        count=1,
        flags=re.MULTILINE,
    )
    assert n_sub == 1, f"Expected 1 EMBEDDED_TWINS_V2 replacement, got {n_sub}"
    print(f"[OK] Re-embedded EMBEDDED_TWINS_V2 into index.html (replacements={n_sub}, count={len(embedded_twins)})")

    INDEX_HTML.write_text(html, encoding="utf-8")

    # Regenerate standalone periodic_table.html & mind_map.html and sync docs/ and zipline_dist/
    pt_html = html.replace(
        "window.__INITIAL_PORTAL_BOOT_MODE__ = null;",
        "window.__INITIAL_PORTAL_BOOT_MODE__ = 'periodic_table';",
    )
    if "window.__INITIAL_PORTAL_BOOT_MODE__" not in html:
        # Check how periodic_table.html and mind_map.html differ from index.html
        pass

    for target_dir in [ROOT / "docs", ROOT / "zipline_dist"]:
        if target_dir.exists():
            shutil.copy2(INDEX_HTML, target_dir / "index.html")
            if (ROOT / "data/supply_chain_catalog.json").exists() and (target_dir / "data").exists():
                shutil.copy2(CATALOG_JSON, target_dir / "data/supply_chain_catalog.json")

    # Also update periodic_table.html and mind_map.html in root, docs/, zipline_dist/
    for variant_name in ["periodic_table.html", "mind_map.html"]:
        v_path = ROOT / variant_name
        if v_path.exists():
            v_txt = v_path.read_text(encoding="utf-8")
            # Apply the same replacements or copy from index.html preserving boot hash
            v_boot_match = re.search(r"window\.location\.hash\s*=\s*'#(periodic|mindmap)';", v_txt)
            new_v_txt = html
            if v_boot_match:
                boot_snippet = f"<script>if (!window.location.hash) window.location.hash = '#{v_boot_match.group(1)}';</script>\n</body>"
                new_v_txt = html.replace("</body>", boot_snippet, 1)
            v_path.write_text(new_v_txt, encoding="utf-8")
            for target_dir in [ROOT / "docs", ROOT / "zipline_dist"]:
                if (target_dir / variant_name).exists():
                    shutil.copy2(v_path, target_dir / variant_name)
            print(f"[OK] Synced {variant_name} across root, docs/, and zipline_dist/")


if __name__ == "__main__":
    update_catalog_json()
    embedded = update_twins_v2()
    update_python_modules()
    update_index_html(embedded)

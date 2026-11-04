#!/usr/bin/env python3
"""Ensure all Operating Pillars (6 canonical + 4–8 dynamic Enterprise Twin pillars) have distinct colors.

Specifically fixes the visual collision between:
  - Pillar 05 (`05 · Distribution & Logistics`, `#059669` Emerald Green)
  - Pillar 06 (`06 · Returns & Reverse Logistics`, previously `#0d9488` Teal Green -> now `#e11d48` Crimson Rose)
and normalizes all cached Enterprise Twins (`data/twins/v2/*.json` + `EMBEDDED_TWINS_V2`) so no two pillars
in any company view share the same or perceptually similar color.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from enterprise_twin.schema import TwinOverlaySpec, validate_and_normalize_overlay  # noqa: E402
from scripts.link_impact_boxes_to_aligned_proofs import build_standalone_variant  # noqa: E402


def update_canonical_catalog() -> None:
    cat_path = ROOT / "data" / "supply_chain_catalog.json"
    raw = cat_path.read_text(encoding="utf-8")
    updated = raw.replace('"#0d9488"', '"#e11d48"').replace("'#0d9488'", "'#e11d48'")
    data = json.loads(updated)
    dept_colors = {k: v["color"] for k, v in data["departments"].items()}
    assert dept_colors["circular_enable"] == "#e11d48", f"Unexpected circular_enable color: {dept_colors}"
    assert len(set(dept_colors.values())) == len(dept_colors), f"Duplicate canonical pillar colors: {dept_colors}"
    cat_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Updated canonical catalog pillar colors:", dept_colors)


def normalize_cached_twins() -> dict[str, dict]:
    twins_dir = ROOT / "data" / "twins" / "v2"
    embedded: dict[str, dict] = {}
    for p in sorted(twins_dir.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        # Upgrade legacy #0d9488 pillar color before running full schema distinctness validator
        for cp in d.get("custom_pillars") or []:
            if str(cp.get("color") or "").lower() == "#0d9488":
                cp["color"] = "#e11d48"
        spec = TwinOverlaySpec.model_validate(d)
        norm = validate_and_normalize_overlay(spec)
        out_dict = norm.model_dump(mode="json")
        cols = [cp["color"] for cp in out_dict.get("custom_pillars", [])]
        assert len(set(cols)) == len(cols), f"Duplicate custom_pillar colors in {p.name}: {cols}"
        p.write_text(json.dumps(out_dict, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        embedded[out_dict["twin_slug"]] = out_dict
        print(f"Normalized {p.name} ({len(cols)} pillars): {cols}")
    return embedded


def update_index_html(embedded_twins: dict[str, dict]) -> str:
    index_path = ROOT / "index.html"
    html = index_path.read_text(encoding="utf-8")

    # 1. Update circular_loop SVG watermark so Pillar 06 stage uses warm/violet secondary accents instead of green/cyan
    old_circular_svg = """      if (watermarkType === 'circular_loop') {
        return `<svg viewBox="0 0 320 118" class="${cssClass}" aria-hidden="true">
          <!-- Circular Reverse RMA Loop + Scope 3 Primary Carbon Telemetry -->
          <path d="M 52 60 C 52 18, 268 18, 268 60 C 268 102, 52 102, 52 60 Z"
                fill="${color}" fill-opacity="0.10" stroke="${color}" stroke-width="2.8" class="sc-arc-flow" />
          <circle cx="52" cy="60" r="9" fill="var(--svg-node-fill)" stroke="${color}" stroke-width="2.4" class="sc-node-pulse" />
          <circle cx="268" cy="60" r="9" fill="var(--svg-node-fill)" stroke="#00d2ff" stroke-width="2.4" class="sc-node-pulse" />
          <rect x="128" y="48" width="16" height="30" rx="3" fill="${color}" fill-opacity="0.85" />
          <rect x="150" y="34" width="16" height="44" rx="3" fill="#00d2ff" fill-opacity="0.90" />
          <rect x="172" y="54" width="16" height="24" rx="3" fill="#10b981" fill-opacity="0.95" />
          <text x="16" y="22" fill="${color}" font-size="10.5" font-weight="700" letter-spacing="0.06em">CIRCULAR RMA &amp; SCOPE 3 TWIN</text>
        </svg>`;
      }"""

    new_circular_svg = """      if (watermarkType === 'circular_loop') {
        return `<svg viewBox="0 0 320 118" class="${cssClass}" aria-hidden="true">
          <!-- Circular Reverse RMA Loop + Scope 3 Primary Carbon Telemetry -->
          <path d="M 52 60 C 52 18, 268 18, 268 60 C 268 102, 52 102, 52 60 Z"
                fill="${color}" fill-opacity="0.10" stroke="${color}" stroke-width="2.8" class="sc-arc-flow" />
          <circle cx="52" cy="60" r="9" fill="var(--svg-node-fill)" stroke="${color}" stroke-width="2.4" class="sc-node-pulse" />
          <circle cx="268" cy="60" r="9" fill="var(--svg-node-fill)" stroke="#f59e0b" stroke-width="2.4" class="sc-node-pulse" />
          <rect x="128" y="48" width="16" height="30" rx="3" fill="${color}" fill-opacity="0.88" />
          <rect x="150" y="34" width="16" height="44" rx="3" fill="#fb7185" fill-opacity="0.90" />
          <rect x="172" y="54" width="16" height="24" rx="3" fill="#f59e0b" fill-opacity="0.92" />
          <text x="16" y="22" fill="${color}" font-size="10.5" font-weight="700" letter-spacing="0.06em">CIRCULAR RMA &amp; SCOPE 3 TWIN</text>
        </svg>`;
      }"""

    if old_circular_svg not in html:
        raise RuntimeError("Could not find circular_loop SVG block in index.html")
    html = html.replace(old_circular_svg, new_circular_svg, 1)

    # 2. Update 5-Stage Circular Recovery banner accent from emerald green to Crimson Rose (#e11d48)
    old_circ_banner = """      if (dept.id === 'circular_enable' || dept.id === 'reverse_risk_esg' || dept.id === 'reverse_logistics_esg') {
        return `
          <div style="margin: 18px 0 20px; padding: 16px 20px; background: rgba(16, 185, 129, 0.06); border: 1px solid rgba(16, 185, 129, 0.28); border-radius: 14px;">"""
    if old_circ_banner in html:
        cb_start = html.index(old_circ_banner)
        cb_end = html.index("      return '';", cb_start)
        cb_chunk = html[cb_start:cb_end]
        cb_chunk = (
            cb_chunk.replace("rgba(16, 185, 129, 0.06)", "rgba(225, 29, 72, 0.06)")
            .replace("rgba(16, 185, 129, 0.28)", "rgba(225, 29, 72, 0.28)")
            .replace("rgba(16,185,129,0.3)", "rgba(225,29,72,0.28)")
            .replace("#34d399", "#e11d48")
        )
        html = html[:cb_start] + cb_chunk + html[cb_end:]

    # 3. Replace all #0d9488 pillar/process/subPillar/benchmark accents with #e11d48
    html = re.sub(r"#0d9488", "#e11d48", html, flags=re.IGNORECASE)

    # 4. Re-embed EMBEDDED_TWINS_V2 from normalized data/twins/v2/*.json
    new_embedded_line = "    const EMBEDDED_TWINS_V2 = " + json.dumps(embedded_twins, ensure_ascii=False) + ";"
    pattern = re.compile(r"^\s*const EMBEDDED_TWINS_V2 = .*?;\s*$", re.MULTILINE)
    m = pattern.search(html)
    if not m:
        raise RuntimeError("Could not find `const EMBEDDED_TWINS_V2 = ...;` in index.html")
    html = html[: m.start()] + new_embedded_line + html[m.end() :]

    index_path.write_text(html, encoding="utf-8")
    return html


def main() -> None:
    update_canonical_catalog()
    embedded = normalize_cached_twins()
    updated_index = update_index_html(embedded)

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

    print("Successfully updated Pillar 06 to #e11d48 (Crimson Rose) and enforced distinct colors across all twins!")


if __name__ == "__main__":
    main()

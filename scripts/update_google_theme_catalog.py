#!/usr/bin/env python3
"""Update department and periodic group colors in catalog JSON files to
toned-down Google Brand Language colors (eliminating harsh neon colors).
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Official Google Brand Language Palette (Toned-down, non-neon, executive-friendly)
GOOGLE_PILLAR_COLORS = {
    "demand_sop": "#2e8b57",          # Muted Google Green (01 · PLAN)
    "sourcing_procurement": "#7e57c2", # Muted Google Purple (02 · SOURCE)
    "manufacturing_prod": "#3b78e7",   # Muted Google Blue (03 · MAKE)
    "inventory_warehouse": "#00897b",  # Muted Google Teal (04 · FULFILL)
    "logistics_fleet": "#d97706",      # Muted Google Amber (05 · DELIVER)
    "circular_enable": "#c53929",      # Muted Google Red/Terracotta (06 · RETURN & ENABLE)
    "universal": "#1a73e8",            # Google Core Blue (Universal Core)
}

# Concise, readable 1-sentence descriptions of what each pillar means
CLEAN_PILLAR_SUBTITLES = {
    "demand_sop": "Forecasts customer demand, senses market shifts, and aligns supply and sales in monthly S&OP.",
    "sourcing_procurement": "Manages supplier selection, cost modeling, contract compliance, and multi-tier supply risk.",
    "manufacturing_prod": "Schedules factory production lines, monitors equipment health (OEE), and ensures inline quality.",
    "inventory_warehouse": "Optimizes inventory buffers across hubs, automates 3D warehouse slotting, and manages dock operations.",
    "logistics_fleet": "Coordinates ocean, air, rail, and road fleet transport alongside last-mile retail distribution.",
    "circular_enable": "Protects on-time customer delivery (OTIF), automates returns (RMA), and tracks Scope 3 emissions.",
}


def update_catalog():
    cat_path = ROOT / "data" / "supply_chain_catalog.json"
    data = json.loads(cat_path.read_text(encoding="utf-8"))

    for dept_id, dept in data.get("departments", {}).items():
        if dept_id in GOOGLE_PILLAR_COLORS:
            dept["color"] = GOOGLE_PILLAR_COLORS[dept_id]
        if dept_id in CLEAN_PILLAR_SUBTITLES:
            dept["subtitle"] = CLEAN_PILLAR_SUBTITLES[dept_id]

    for grp in data.get("periodicGroups", []):
        gid = grp.get("id")
        if gid in GOOGLE_PILLAR_COLORS:
            grp["color"] = GOOGLE_PILLAR_COLORS[gid]

    cat_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {cat_path}")

    pt_path = ROOT / "data" / "periodic_table_elements.json"
    if pt_path.exists():
        pt_data = json.loads(pt_path.read_text(encoding="utf-8"))
        for grp in pt_data.get("groups", []):
            gid = grp.get("id")
            if gid in GOOGLE_PILLAR_COLORS:
                grp["color"] = GOOGLE_PILLAR_COLORS[gid]
        for el in pt_data.get("elements", []):
            gid = el.get("group")
            if gid in GOOGLE_PILLAR_COLORS:
                el["groupColor"] = GOOGLE_PILLAR_COLORS[gid]
        pt_path.write_text(json.dumps(pt_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Updated {pt_path}")


if __name__ == "__main__":
    update_catalog()

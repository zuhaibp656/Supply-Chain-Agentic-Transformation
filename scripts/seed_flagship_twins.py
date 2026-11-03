#!/usr/bin/env python3
"""Pre-seeds flagship multi-division Enterprise Twins into `data/twins/v2/` (and GCS/BQ)."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from enterprise_twin.agent import run_enterprise_twin_agent

FLAGSHIP_SEEDS = [
    ("ITC Limited", "Cigarettes & Leaf Tobacco (ILTD & TM&D)", "India"),
    ("ITC Limited", "Foods Division (ICML & Agri)", "India"),
    ("Aditya Birla Group", "UltraTech Cement Division", "India"),
    ("Aditya Birla Group", "Hindalco Aluminium & Copper", "India & Global"),
    ("Unilever", "Home & Personal Care", "Global"),
    ("Tata Consumer Products", "India Packaged Beverages & Foods", "India"),
    ("Maruti Suzuki", "", "India"),
    ("Wipro", "", "Global"),
]


def main() -> None:
    typo_path = ROOT / "data" / "twins" / "v2" / "itc-limited--trade-marketing.json"
    if typo_path.exists():
        typo_path.unlink()
    for co, div, geo in FLAGSHIP_SEEDS:
        res = run_enterprise_twin_agent(
            company_name=co,
            division_name=div,
            geography=geo,
            force_refresh=True,
        )
        ov = res["overlay"]
        logo = ov["brand"]["logo"]
        print(
            f"[OK] {ov['twin_slug']} | {ov['display_label']} | "
            f"pillars={ov.get('active_pillars_count', len(ov.get('custom_pillars', [])))} | "
            f"active={ov['active_agents_count']}/60 (hidden={len(ov['hidden_agent_ids'])}) | "
            f"logo={logo['source_type']} ({logo['plate_style']})"
        )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
replace_real_company_names_with_cymbal.py

Systematically and idempotently replaces real company names (Walmart, Kroger, Costco,
Target [retailer], PepsiCo, Procter & Gamble, Kraft Heinz, Tyson Foods) across:
- demo_data/tables/*.{json,csv}
- agents/*/fixtures/tables/*.json
- agents/*/fixtures/master/xyz_enterprise_backbone.json
- agents/*/app/*.py
- agents/*/evals/*.json
- agents/*/tests/*.py
- scripts/playbook_dataflow_and_prompts_engine.py
- scripts/human_plain_english_prompts.py
- AGENT_TESTING_AND_VIDEO_PLAYBOOK.md & docs/ & zipline_dist/
- agent_testing_and_video_playbook.html & docs/ & zipline_dist/
- supply_chain_101_interactive_academy.html & docs/ & zipline_dist/
- cost_analysis_presentation.html & docs/ & zipline_dist/
- data/supply_chain_catalog.json & docs/ & zipline_dist/
"""

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Exact word/phrase replacements ordered by specificity
REPLACEMENTS = [
    # Walmart specific IDs and phrases
    ("STORE-WALMART-DAL-104", "STORE-CYMBAL-DAL-104"),
    ("PHANTOM-WALMART-DAL-02", "PHANTOM-CYMBAL-DAL-02"),
    ("CPFR-PKT-202611-WMT", "CPFR-PKT-202611-CYM"),
    ("EDI830-WMT-202611", "EDI830-CYM-202611"),
    ("CUST-WALMART-001", "CUST-CYMBAL-001"),
    ("Key Account Walmart", "Key Account Cymbal"),
    ("Walmart National", "Cymbal Retail National"),
    ("Walmart Q4", "Cymbal Retail Q4"),
    ("Walmart VMI", "Cymbal Retail VMI"),
    ("Walmart", "Cymbal Retail"),
    ("WALMART", "CYMBAL_RETAIL"),

    # Kroger specific IDs and phrases
    ("STORE-KROGER-ATL-209", "STORE-APEX-ATL-209"),
    ("PHANTOM-KROGER-ATL-01", "PHANTOM-APEX-ATL-01"),
    ("CUST-KROGER-CORP", "CUST-APEX-CORP"),
    ("CUST-KROGER-US01", "CUST-APEX-US01"),
    ("Kroger Fresh & Marketplace Divisions", "Apex Fresh & Marketplace Divisions"),
    ("Kroger National Distribution", "Apex Hypermarket National Distribution"),
    ("Kroger National", "Apex Hypermarket National"),
    ("Key Account Kroger", "Key Account Apex"),
    ("Kroger store", "Apex Hypermarket store"),
    ("Kroger", "Apex Hypermarket"),
    ("KROGER", "APEX_HYPERMARKET"),

    # Costco specific IDs and phrases
    ("STORE-COSTCO-CHI-301", "STORE-OMNI-CHI-301"),
    ("CUST-COSTCO-US04", "CUST-OMNI-US04"),
    ("Costco Club Wholesale North America", "Omni Wholesale Club North America"),
    ("Costco Club Wholesale", "Omni Wholesale Club"),
    ("Key Account Costco", "Key Account Omni Club"),
    ("Costco", "Omni Wholesale Club"),
    ("COSTCO", "OMNI_WHOLESALE"),

    # Target specific IDs and phrases (retail context only)
    ("CPFR-PKT-202611-TGT", "CPFR-PKT-202611-SMT"),
    ("EDI830-TGT-202611", "EDI830-SMT-202611"),
    ("retailer=\"Target\"", "retailer=\"Summit Stores\""),
    ("retailer\": \"Target\"", "retailer\": \"Summit Stores\""),
    ("`Target`", "`Summit Stores`"),

    # Food and CPG brands
    ("PepsiCo", "Cymbal Beverage Global"),
    ("Procter & Gamble", "Cymbal Personal Care"),
    ("Kraft Heinz", "Cymbal Foods Global"),
    ("Tyson Foods", "Cymbal Fresh Proteins"),
]

DIRECTORIES_TO_PROCESS = [
    "demo_data",
    "agents",
    "scripts",
    "data",
    "docs",
    "zipline_dist",
]

ROOT_FILES_TO_PROCESS = [
    "AGENT_TESTING_AND_VIDEO_PLAYBOOK.md",
    "agent_testing_and_video_playbook.html",
    "supply_chain_101_interactive_academy.html",
    "cost_analysis_presentation.html",
    "deployment_metadata.json",
]


def process_file(file_path: Path) -> int:
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return 0

    original = content
    for old_str, new_str in REPLACEMENTS:
        content = content.replace(old_str, new_str)

    if content != original:
        file_path.write_text(content, encoding="utf-8")
        return 1
    return 0


def main():
    modified_count = 0

    # 1. Process root files
    for fname in ROOT_FILES_TO_PROCESS:
        p = ROOT / fname
        if p.exists():
            if process_file(p):
                print(f"[MODIFIED] {fname}")
                modified_count += 1

    # 2. Process directories
    for dname in DIRECTORIES_TO_PROCESS:
        d = ROOT / dname
        if not d.exists():
            continue
        for root, dirs, files in os.walk(d):
            if any(x in root for x in [".git", "node_modules", ".venv", "__pycache__"]):
                continue
            for f in files:
                if f.endswith((".json", ".csv", ".py", ".md", ".html", ".js")):
                    p = Path(root) / f
                    if p.name == "replace_real_company_names_with_cymbal.py":
                        continue
                    if process_file(p):
                        rel = p.relative_to(ROOT)
                        print(f"[MODIFIED] {rel}")
                        modified_count += 1

    print(f"\nReplacement complete! Modified {modified_count} files across codebase.")


if __name__ == "__main__":
    main()

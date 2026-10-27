#!/usr/bin/env python3
"""
Syncs the enriched 60-agent `AGENTS` dictionary (including `category`, `categoryTag`,
`categoryDisplayName`, `categorizedDescription`, and `adkImplementation` with 245 demo data tables)
from `data/supply_chain_catalog.json` into `index.html`, `periodic_table.html`, and `mind_map.html`,
and ensures the Agent Page (`#agent/<id>`) and Blueprint Page (`#blueprint/<id>`) display the
Category in the Agent Name and Description.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "data" / "supply_chain_catalog.json"
HTML_FILES = [
    ROOT / "index.html",
    ROOT / "periodic_table.html",
    ROOT / "mind_map.html",
]


def main() -> None:
    cat = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    agents_json = json.dumps(cat["agents"], indent=2)

    for path in HTML_FILES:
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")

        # 1. Replace `const AGENTS = { ... };` right before `Object.defineProperty(AGENTS,`
        pattern = re.compile(
            r"    const AGENTS = \{[\s\S]*?\n\};\n    Object\.defineProperty\(AGENTS,",
            re.M,
        )
        if not pattern.search(html):
            raise RuntimeError(f"Could not find `const AGENTS =` block in {path}")

        replacement = f"    const AGENTS = {agents_json};\n    Object.defineProperty(AGENTS,"
        html = pattern.sub(lambda _: replacement, html, count=1)

        # 2. In openAgentPage, show `ag.categoryDisplayName || ag.name` and `ag.categorizedDescription || ag.shortDesc`
        html = html.replace(
            '<h1 class="agent-title" style="font-size: clamp(26px, 3vw, 36px); margin: 0;">${ag.name}</h1>\n'
            '                  <div style="font-size:14.5px; color:var(--text-secondary); margin-top:3px;">${shortSentence(ag.shortDesc, 115)}</div>',
            '<h1 class="agent-title" style="font-size: clamp(24px, 2.7vw, 34px); margin: 0;">${ag.categoryDisplayName || ag.name}</h1>\n'
            '                  <div style="font-size:14.5px; color:var(--text-secondary); margin-top:4px;">${shortSentence(ag.categorizedDescription || ag.shortDesc, 175)}</div>',
        )

        # 3. In openAgentBlueprintPage, show `ag.categoryDisplayName || ag.name`
        html = html.replace(
            '<h1 class="persona-page-title">${ag.name} — Engineering Blueprint</h1>',
            '<h1 class="persona-page-title">${ag.categoryDisplayName || ag.name} — Engineering Blueprint</h1>',
        )

        path.write_text(html, encoding="utf-8")
        print(f"[SYNCED] {path} with 60 categorized ADK agents & 245 demo data tables.")


if __name__ == "__main__":
    main()

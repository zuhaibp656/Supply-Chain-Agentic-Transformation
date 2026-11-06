#!/usr/bin/env python3
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / "data" / "supply_chain_catalog.json") as f:
    cat = json.load(f)

depts = cat.get("departments", {})

print(f"Total Pillars in catalog: {len(depts)}")

agents_60 = []
for dept_id, dept in depts.items():
    vNum = dept.get("vNum", "")
    dept_name = dept.get("name", "")
    for sp in dept.get("subPillars", []):
        sp_id = sp.get("id", "")
        sp_name = sp.get("name", "")
        for item in sp.get("items", []):
            agent_id = item.get("agentId")
            if agent_id:
                agents_60.append({
                    "agent_id": agent_id,
                    "agent_name": item.get("agentName", ""),
                    "persona_id": item.get("personaId", ""),
                    "persona_name": item.get("personaName", ""),
                    "persona_icon": item.get("personaIcon", ""),
                    "dept_id": dept_id,
                    "vNum": vNum,
                    "dept_name": dept_name,
                    "subpillar_id": sp_id,
                    "subpillar_name": sp_name,
                    "desc": item.get("desc", ""),
                    "outcome": item.get("outcome", ""),
                    "buildTier": item.get("buildTier", "High-Code"),
                })

print(f"Extracted {len(agents_60)} agents from subPillars.")

existing_dirs = set(os.listdir(ROOT / "agents"))
missing = [a for a in agents_60 if a["agent_id"] not in existing_dirs]

print(f"Missing agent directories in agents/: {len(missing)}")
for m in missing:
    print(f"  - {m['agent_id']} ({m['agent_name']}) in {m['dept_name']} -> {m['subpillar_name']}")

# Save out clean mapping JSON
out_path = ROOT / "scripts" / "catalog_60_agents_list.json"
with open(out_path, "w") as f:
    json.dump(agents_60, f, indent=2)
print(f"Wrote {len(agents_60)} records to {out_path}")

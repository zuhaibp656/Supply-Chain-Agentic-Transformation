#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / "data" / "supply_chain_catalog.json") as f:
    cat = json.load(f)

depts = cat.get("departments", {})

print(f"Pillars: {len(depts)}")

all_agents = []
all_personas = []

for dept_id, dept in depts.items():
    vNum = dept.get("vNum", "")
    name = dept.get("name", "")
    subpillars = dept.get("subPillars", [])
    for sp in subpillars:
        sp_id = sp.get("id", "")
        sp_name = sp.get("name", "")
        for item in sp.get("items", []):
            agent_id = item.get("agentId", "")
            agent_name = item.get("agentName", "")
            persona_id = item.get("personaId", "")
            persona_name = item.get("personaName", "")
            all_agents.append({
                "agent_id": agent_id,
                "agent_name": agent_name,
                "persona_id": persona_id,
                "persona_name": persona_name,
                "dept_id": dept_id,
                "vNum": vNum,
                "dept_name": name,
                "subpillar_id": sp_id,
                "subpillar_name": sp_name,
                "desc": item.get("desc", ""),
                "outcome": item.get("outcome", ""),
                "buildTier": item.get("buildTier", "High-Code"),
            })

print(f"Total agents extracted from subPillars: {len(all_agents)}")

# Check agents list if separate
cat_agents = cat.get("agents", [])
print(f"Total agents in root agents list: {len(cat_agents)}")

agent_dirs = [d.name for d in (ROOT / "agents").iterdir() if d.is_dir() and d.name not in ("__pycache__", "common")]
print(f"Total agent folders in agents/: {len(agent_dirs)}")

missing_in_folders = [a["agent_id"] for a in all_agents if a["agent_id"] not in agent_dirs]
print(f"Catalog agents missing in agents/ folder ({len(missing_in_folders)}):", missing_in_folders)

with open(ROOT / "scripts" / "extracted_60_agents.json", "w") as out_f:
    json.dump(all_agents, out_f, indent=2)
print("Saved extracted agents list to scripts/extracted_60_agents.json")

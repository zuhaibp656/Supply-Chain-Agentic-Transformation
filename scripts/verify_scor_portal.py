#!/usr/bin/env python3
"""
Comprehensive validator for the Supply Chain Agentic Transformation suite.
Verifies that:
1. data/supply_chain_catalog.json has exactly 6 SCOR pillars, 29 personas, 35 agents.
2. All personas map to a valid department.
3. All agents map to a valid department or universal core.
4. data/periodic_table_elements.json has 7 groups (6 pillars + universal core) and 35 elements.
5. index.html has embedded data matching these exact counts.
6. The HTML front-page tab bar has 6 pillar buttons + 1 ALL button.
7. .dept-row grid CSS uses 3 columns.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_catalog():
    cat_path = ROOT / "data" / "supply_chain_catalog.json"
    with open(cat_path, "r", encoding="utf-8") as f:
        cat = json.load(f)

    # 1. Metadata checks
    assert cat["metadata"]["scorVerticalsCount"] == 6, f"Expected 6 scorVerticalsCount, got {cat['metadata']['scorVerticalsCount']}"
    assert cat["metadata"]["verticalsCount"] == 6, f"Expected 6 verticalsCount, got {cat['metadata']['verticalsCount']}"
    assert cat["metadata"]["personasCount"] == 29, f"Expected 29 personasCount, got {cat['metadata']['personasCount']}"
    assert cat["metadata"]["agentsCount"] == 35, f"Expected 35 agentsCount, got {cat['metadata']['agentsCount']}"

    # 2. Departments checks
    expected_depts = [
        "demand_sop",
        "sourcing_procurement",
        "manufacturing_prod",
        "inventory_warehouse",
        "logistics_fleet",
        "circular_enable"
    ]
    actual_depts = list(cat["departments"].keys())
    assert actual_depts == expected_depts, f"Departments mismatch: {actual_depts} vs {expected_depts}"

    for did in expected_depts:
        d = cat["departments"][did]
        assert "scorBadge" in d and d["scorBadge"].startswith("SCOR"), f"{did} missing scorBadge: {d.get('scorBadge')}"
        assert len(d.get("personaIds", [])) > 0, f"{did} has no personas"
        assert len(d.get("agentIds", [])) > 0, f"{did} has no agents"

    # 3. Persona mapping checks
    personas = cat["personas"]
    assert len(personas) == 29, f"Expected 29 personas, got {len(personas)}"
    for pid, p in personas.items():
        did = p.get("deptId")
        assert did in expected_depts, f"Persona {pid} has invalid deptId {did}"

    # 4. Agent mapping checks
    agents = cat["agents"]
    assert len(agents) == 35, f"Expected 35 agents, got {len(agents)}"
    valid_agent_depts = expected_depts + ["universal_csco"]
    for aid, a in agents.items():
        did = a.get("deptId")
        assert did in valid_agent_depts, f"Agent {aid} has invalid deptId {did}"

    print("✔ data/supply_chain_catalog.json passed all tests!")


def test_periodic_table():
    pt_path = ROOT / "data" / "periodic_table_elements.json"
    with open(pt_path, "r", encoding="utf-8") as f:
        pt = json.load(f)

    groups = pt.get("groups", [])
    assert len(groups) == 7, f"Expected 7 groups in periodic table, got {len(groups)}"

    group_ids = [g["id"] for g in groups]
    expected_group_ids = [
        "universal_csco",
        "demand_sop",
        "sourcing_procurement",
        "manufacturing_prod",
        "inventory_warehouse",
        "logistics_fleet",
        "circular_enable"
    ]
    assert group_ids == expected_group_ids, f"Periodic group IDs mismatch: {group_ids} vs {expected_group_ids}"

    elements = pt.get("elements", [])
    assert len(elements) == 35, f"Expected 35 elements in periodic table, got {len(elements)}"

    for el in elements:
        gid = el.get("group")
        assert gid in expected_group_ids, f"Element {el.get('agentId')} has invalid group {gid}"

    print("✔ data/periodic_table_elements.json passed all tests!")


def test_html():
    index_path = ROOT / "index.html"
    html = index_path.read_text(encoding="utf-8")

    # Check 3x2 grid CSS
    assert "grid-template-columns: repeat(3, 1fr);" in html, "Missing 3-column .dept-row grid CSS"

    # Check 6 pillar tab buttons
    for did in ["demand_sop", "sourcing_procurement", "manufacturing_prod", "inventory_warehouse", "logistics_fleet", "circular_enable"]:
        assert f'data-vtab="{did}"' in html, f"Missing tab button for {did}"

    # Check that ALL 6 exists
    assert 'ALL 6' in html, "Missing ALL 6 tab button"

    # Check that DEPARTMENTS embedded JSON has 6 keys
    d_start = html.find("const DEPARTMENTS = ") + len("const DEPARTMENTS = ")
    d_end = html.find(";\n    Object.defineProperty", d_start)
    assert d_end != -1, "Failed to find end of DEPARTMENTS JSON"
    embedded_depts = json.loads(html[d_start:d_end])
    assert len(embedded_depts) == 6, f"Expected 6 embedded departments, got {len(embedded_depts)}"

    # Check personas embedded
    p_start = html.find("const PERSONAS = ") + len("const PERSONAS = ")
    p_end = html.find(";\n\n    /* 3. SUPPLY CHAIN AGENTS", p_start)
    assert p_end != -1, "Failed to find end of PERSONAS JSON"
    embedded_personas = json.loads(html[p_start:p_end])
    assert len(embedded_personas) == 29, f"Expected 29 embedded personas, got {len(embedded_personas)}"

    # Check agents embedded
    a_start = html.find("const AGENTS = ") + len("const AGENTS = ")
    a_end = html.find(";\n\n    /* 4 UNIVERSAL CROSS-PERSONA", a_start)
    assert a_end != -1, "Failed to find end of AGENTS JSON"
    embedded_agents = json.loads(html[a_start:a_end])
    assert len(embedded_agents) == 35, f"Expected 35 embedded agents, got {len(embedded_agents)}"

    print("✔ index.html passed all tests!")


if __name__ == "__main__":
    test_catalog()
    test_periodic_table()
    test_html()
    print("\n🎉 ALL TESTS PASSED! 6 SCOR PILLARS ARCHITECTURE IS 100% VERIFIED!")

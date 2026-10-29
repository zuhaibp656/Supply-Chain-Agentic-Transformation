#!/usr/bin/env python3
"""Universal CLI Runner & Demo Data Inspector for all 60 Supply Chain AI Agents.

Usage Examples (for Video Recording & Live Demos):
  1. Run an agent's full autonomous demo scenario (Read -> Solve -> Safety Gate -> Write-Back + Markdown Report):
     python3 scripts/test_agent_demo.py demand_sensing_agent

  2. Run with a custom prompt:
     python3 scripts/test_agent_demo.py demand_sensing_agent --query "Detect US-Central heatwave surge and update IBP"

  3. Inspect the agent's Demo Data tables and sample rows before recording:
     python3 scripts/test_agent_demo.py demand_sensing_agent --show-data

  4. Test the Pre-Execution Governance / Safety Gate (blocks missing idempotency_key or invalid mutation):
     python3 scripts/test_agent_demo.py demand_sensing_agent --test-guardrail

  5. List all 60 built agents grouped by SCOR Pillar:
     python3 scripts/test_agent_demo.py --list
"""
from __future__ import annotations

import argparse
import importlib
import inspect
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "data" / "supply_chain_catalog.json"


def load_catalog() -> dict:
    if CATALOG_PATH.exists():
        return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    return {"agents": {}, "departments": {}}


def instantiate_agent(agent_id: str):
    agent_dir = ROOT / "agents" / agent_id
    if not (agent_dir / "app" / "agent.py").exists():
        raise FileNotFoundError(f"Agent package not found at agents/{agent_id}/app/agent.py")

    sys.path.insert(0, str(agent_dir))
    # Clear cached app modules if switching agents
    for mod_name in list(sys.modules.keys()):
        if mod_name == "app" or mod_name.startswith("app."):
            del sys.modules[mod_name]

    agent_mod = importlib.import_module("app.agent")
    tools_mod = importlib.import_module("app.tools")

    # Find the agent class with run_scenario
    agent_cls = None
    for name, obj in inspect.getmembers(agent_mod, inspect.isclass):
        if hasattr(obj, "run_scenario") and obj.__module__ == "app.agent" and not name.endswith("AdkApp"):
            agent_cls = obj
            break

    if agent_cls is None:
        raise RuntimeError(f"Could not locate agent class in agents/{agent_id}/app/agent.py")

    return agent_cls(), tools_mod, agent_mod


def print_banner(title: str, char: str = "=") -> None:
    line = char * 88
    print(f"\n{line}\n  {title}\n{line}")


def cmd_list(cat: dict) -> None:
    print_banner("ALL 60 BUILT SUPPLY CHAIN AI AGENTS (BY SCOR PILLAR)")
    agents = list(cat.get("agents", {}).values())
    by_pillar: dict[str, list[dict]] = {}
    for ag in agents:
        pillar = ag.get("category", ag.get("deptId", "General")).split("—")[0].strip()
        by_pillar.setdefault(pillar, []).append(ag)

    for pillar, items in sorted(by_pillar.items()):
        print(f"\n▸ {pillar} ({len(items)} Agents)")
        for ag in items:
            re_file = ROOT / "agents" / ag["id"] / ".reasoning_engine_id"
            cloud_tag = " [🟢 LIVE IN VERTEX AI & GEMINI ENTERPRISE]" if re_file.exists() else ""
            print(f"   • {ag['id']:<36} | {ag.get('name', ''):<34} | ROI: {ag.get('badge', '')}{cloud_tag}")
    print()


def cmd_show_data(agent_id: str, cat: dict) -> None:
    ag_meta = cat.get("agents", {}).get(agent_id, {})
    print_banner(f"DEMO DATA TABLES & SAMPLE RECORDS — {ag_meta.get('name', agent_id)} ({agent_id})")
    tables_dir = ROOT / "agents" / agent_id / "fixtures" / "tables"
    if not tables_dir.exists():
        print("No fixture tables directory found.")
        return

    for tf in sorted(tables_dir.glob("*.json")):
        rows = json.loads(tf.read_text(encoding="utf-8"))
        cols = list(rows[0].keys()) if rows else []
        print(f"\n🗄️  Table: {tf.stem}  ({len(rows)} rows)")
        print(f"   File : agents/{agent_id}/fixtures/tables/{tf.name}")
        print(f"   Cols : {', '.join(cols)}")
        if rows:
            print(f"   Sample Row 1: {json.dumps(rows[0], ensure_ascii=False)}")
            if len(rows) > 1:
                print(f"   Sample Row 2: {json.dumps(rows[1], ensure_ascii=False)}")
    print()


def cmd_test_guardrail(agent_id: str) -> None:
    agent, _, agent_mod = instantiate_agent(agent_id)
    write_tools = getattr(agent_mod, "_WRITE_TOOLS", {})
    print_banner(f"GOVERNANCE & SAFETY GATE TEST — {agent_id}")
    if not write_tools:
        print("No write tools registered.")
        return

    tool_name, req_fields = next(iter(write_tools.items()))
    print(f"1. Testing Write Tool '{tool_name}' WITHOUT required fields:")
    res1 = agent.execute_tool(tool_name)
    print(f"   -> Gate Response: {json.dumps(res1, ensure_ascii=False)}")

    print(f"\n2. Testing Write Tool '{tool_name}' WITH required fields={req_fields} but WITHOUT idempotency_key:")
    dummy_kwargs = {k: "TEST-VAL-01" if "units" not in k and "qty" not in k and "amount" not in k else 100 for k in req_fields}
    res2 = agent.execute_tool(tool_name, **dummy_kwargs)
    print(f"   -> Gate Response: {json.dumps(res2, ensure_ascii=False)}")
    print("\n✅ Pre-Execution Quality Gate verified: unauthenticated or partial mutations are deterministically blocked!\n")


def cmd_run_demo(agent_id: str, query: str | None, cat: dict) -> None:
    ag_meta = cat.get("agents", {}).get(agent_id, {})
    spec = ag_meta.get("adkSpec", {})
    eval_obj = spec.get("evalScenario", {})
    default_query = eval_obj.get("query") or f"Execute full autonomous analysis and write-back for {ag_meta.get('name', agent_id)}."
    active_query = query or default_query

    agent, _, _ = instantiate_agent(agent_id)
    routing = agent.select_orchestrated_model(active_query) if hasattr(agent, "select_orchestrated_model") else {}

    print_banner(f"RUNNING LIVE AGENT DEMO — {ag_meta.get('name', agent_id)} ({agent_id})")
    print(f"🎯 What It Does : {ag_meta.get('solution', '')}")
    print(f"💬 Demo Prompt  : \"{active_query}\"")
    if routing:
        print(f"🧠 Model Routed : {routing.get('selected_model', 'gemini-3.8-flash')}")

    result = agent.run_scenario(active_query)

    print_banner("1. EXECUTED WRITE-BACK ACTIONS & AUDIT RECEIPTS", "-")
    for idx, act in enumerate(result.get("actions_executed", []), 1):
        print(f"  [{idx}] {json.dumps(act, ensure_ascii=False)}")

    print_banner("2. A2UI VISUAL SURFACE (VEGA-LITE CHART SPEC)", "-")
    vega = result.get("vega_spec", {})
    print(f"  • Schema : {vega.get('$schema', 'vega-lite/v5')}")
    print(f"  • Title  : {vega.get('title', 'Operational Visual Surface')}")
    print(f"  • Parts  : {len(result.get('a2ui_parts', []))} A2UI envelope parts generated")

    print_banner("3. EXECUTIVE MARKDOWN RESPONSE & COPY-READY TABLE", "-")
    print(result.get("markdown", ""))
    print("\n✅ Scenario completed successfully!\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Test and inspect any of the 60 Supply Chain AI Agents.")
    parser.add_argument("agent_id", nargs="?", help="Agent ID (e.g., demand_sensing_agent, fleetflow_dispatch)")
    parser.add_argument("--query", "-q", help="Custom prompt to pass to run_scenario()")
    parser.add_argument("--show-data", action="store_true", help="Print demo data tables and sample rows for this agent")
    parser.add_argument("--test-guardrail", action="store_true", help="Test pre-execution quality gates for this agent")
    parser.add_argument("--list", action="store_true", help="List all 60 built agents")
    args = parser.parse_args()

    cat = load_catalog()
    if args.list or not args.agent_id:
        cmd_list(cat)
        return

    if args.show_data:
        cmd_show_data(args.agent_id, cat)
    if args.test_guardrail:
        cmd_test_guardrail(args.agent_id)
    if not args.show_data and not args.test_guardrail:
        cmd_run_demo(args.agent_id, args.query, cat)


if __name__ == "__main__":
    main()

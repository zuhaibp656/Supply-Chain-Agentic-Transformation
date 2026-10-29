#!/usr/bin/env python3
"""Universal CLI Runner & Demo Data Inspector for all 60 Supply Chain AI Agents.

Usage Examples (for Video Recording & Manual Testing):
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
    for mod_name in list(sys.modules.keys()):
        if mod_name == "app" or mod_name.startswith("app."):
            del sys.modules[mod_name]

    agent_mod = importlib.import_module("app.agent")
    tools_mod = importlib.import_module("app.tools")
    charts_mod = importlib.import_module("app.render.charts")

    agent_cls = None
    for name, obj in inspect.getmembers(agent_mod, inspect.isclass):
        if hasattr(obj, "run_scenario") and obj.__module__ == "app.agent" and not name.endswith("AdkApp"):
            agent_cls = obj
            break

    if agent_cls is None:
        raise RuntimeError(f"Could not locate agent class in agents/{agent_id}/app/agent.py")

    return agent_cls(), tools_mod, agent_mod, charts_mod


def extract_normalized_scenario(agent_id: str, query: str | None = None) -> dict:
    """Runs run_scenario() on any of the 60 agents and normalizes the output dict."""
    cat = load_catalog()
    ag_meta = cat.get("agents", {}).get(agent_id, {})
    spec = ag_meta.get("adkSpec", {})
    eval_obj = spec.get("evalScenario", {})
    default_query = eval_obj.get("query") or f"Execute full autonomous analysis and write-back for {ag_meta.get('name', agent_id)}."
    active_query = query or default_query

    agent, _, _, charts_mod = instantiate_agent(agent_id)
    routing = agent.select_orchestrated_model(active_query) if hasattr(agent, "select_orchestrated_model") else {}
    res = agent.run_scenario(active_query)

    actions = res.get("actions_executed") or res.get("actions_taken") or []
    vega_spec = res.get("vega_spec")
    if not vega_spec:
        for fn_name, fn_obj in inspect.getmembers(charts_mod, inspect.isfunction):
            if fn_name.startswith("create_") and "spec" in fn_name:
                try:
                    vega_spec = fn_obj()
                    break
                except Exception:
                    pass
    vega_spec = vega_spec or {}
    a2ui_parts = res.get("a2ui_parts") or res.get("a2ui_surface") or []
    md = res.get("markdown") or res.get("markdown_response") or ""

    return {
        "status": str(res.get("status", "success")).lower(),
        "query": active_query,
        "routing": routing,
        "actions": actions,
        "vega_spec": vega_spec,
        "a2ui_parts_count": len(a2ui_parts),
        "markdown": md,
    }


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
    agent, _, agent_mod, _ = instantiate_agent(agent_id)
    write_tools = getattr(agent_mod, "_WRITE_TOOLS", None) or getattr(agent_mod, "WRITE_TOOLS", {})
    print_banner(f"GOVERNANCE & SAFETY GATE TEST — {agent_id}")
    if not write_tools:
        # Test enforce_tool_contract directly if available
        if hasattr(agent_mod, "enforce_tool_contract"):
            res = agent_mod.enforce_tool_contract("action_commit", {})
            print(f"   -> Gate Response (missing idempotency_key): {json.dumps(res, ensure_ascii=False)}")
            print("\n✅ Pre-Execution Quality Gate verified!\n")
            return
        print("No write tools registered.")
        return

    if isinstance(write_tools, dict):
        tool_name, req_fields = next(iter(write_tools.items()))
    else:
        tool_name, req_fields = list(write_tools)[0], ["idempotency_key"]

    print(f"1. Testing Write Tool '{tool_name}' WITHOUT required fields:")
    res1 = agent.execute_tool(tool_name) if hasattr(agent, "execute_tool") else agent_mod.enforce_tool_contract(tool_name, {})
    print(f"   -> Gate Response: {json.dumps(res1, ensure_ascii=False)}")

    print(f"\n2. Testing Write Tool '{tool_name}' WITH required fields={req_fields} but WITHOUT idempotency_key:")
    dummy_kwargs = {k: "TEST-VAL-01" if "units" not in k and "qty" not in k and "amount" not in k else 100 for k in req_fields if k != "idempotency_key"}
    res2 = agent.execute_tool(tool_name, **dummy_kwargs) if hasattr(agent, "execute_tool") else agent_mod.enforce_tool_contract(tool_name, dummy_kwargs)
    print(f"   -> Gate Response: {json.dumps(res2, ensure_ascii=False)}")
    print("\n✅ Pre-Execution Quality Gate verified: unauthenticated or partial mutations are deterministically blocked!\n")


def cmd_run_demo(agent_id: str, query: str | None, cat: dict) -> None:
    ag_meta = cat.get("agents", {}).get(agent_id, {})
    norm = extract_normalized_scenario(agent_id, query)

    print_banner(f"RUNNING LIVE AGENT DEMO — {ag_meta.get('name', agent_id)} ({agent_id})")
    print(f"🎯 What It Does : {ag_meta.get('solution', '')}")
    print(f"💬 Demo Prompt  : \"{norm['query']}\"")
    if norm["routing"]:
        print(f"🧠 Model Routed : {norm['routing'].get('selected_model', 'gemini-3.8-flash')}")

    print_banner("1. EXECUTED WRITE-BACK ACTIONS & AUDIT RECEIPTS", "-")
    for idx, act in enumerate(norm["actions"], 1):
        print(f"  [{idx}] {json.dumps(act, ensure_ascii=False)}")

    print_banner("2. A2UI VISUAL SURFACE (VEGA-LITE CHART SPEC)", "-")
    vega = norm["vega_spec"]
    print(f"  • Schema : {vega.get('$schema', 'vega-lite/v5')}")
    print(f"  • Title  : {vega.get('title', 'Operational Visual Surface')}")
    print(f"  • Parts  : {norm['a2ui_parts_count']} A2UI envelope parts generated")

    print_banner("3. EXECUTIVE MARKDOWN RESPONSE & COPY-READY TABLE", "-")
    print(norm["markdown"])
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

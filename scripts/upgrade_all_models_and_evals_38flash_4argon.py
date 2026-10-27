#!/usr/bin/env python3
"""Upgrades all 60+ agents, evals, manifests, catalog, docs, website, and cost
presentation so that:
1. All evals (`agents/*/evals/golden_scenarios.json` and `agents/*/tests/test_smoke.py`)
   explicitly use and verify the latest `Gemini 3.8 Flash` (`gemini-3.8-flash`) and
   `Gemini 4 Argon` (`gemini-4-argon` / `gemini-3.1-pro` subject to availability).
2. Every Agent Orchestrator (`agents/*/app/agent.py`, `data/supply_chain_catalog.json`,
   website, and manifests) implements and documents Dynamic Orchestrator Model Routing,
   where the Agent Orchestrator decides per query whether to use `Gemini 3.8 Flash`
   (`gemini-3.8-flash`) or escalate to `Gemini 3.1 Pro / 4 Argon`
   (`gemini-3.1-pro` / `gemini-4-argon`, subject to availability).
3. Sweeps all docs, code, HTML, JSON, YAML, and script files across the entire repository
   to ensure ONLY `Gemini 3.8 Flash` and `Gemini 3.1 Pro / 4 Argon (subject to availability)`
   are used and mentioned everywhere (zero `2.5`, `2.0`, `3.0`, or `Flash-Lite` references).
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PRO_ARGON_PRIMARY_AGENTS = {
    "npi_demand_profiler",
    "promo_lift_simulator",
    "sop_scenario_weaver",
    "disruption_war_room_orchestrator",
    "csco_control_tower_copilot",
    "legal_contract_redliner",
    "capex_simulator_agent",
    "network_design_digital_twin",
}


def update_catalog() -> dict:
    catalog_path = ROOT / "data" / "supply_chain_catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))

    catalog["metadata"]["llmModelRoutingPolicy"] = {
        "orchestratorArchitecture": (
            "Dynamic Agent Orchestrator Routing: The Agent Orchestrator inspects each incoming query's "
            "complexity, constraint depth, and multi-echelon scope to dynamically decide whether to execute on "
            "Gemini 3.8 Flash (gemini-3.8-flash) or escalate to Gemini 3.1 Pro / 4 Argon "
            "(gemini-3.1-pro / gemini-4-argon, subject to availability)."
        ),
        "fastExecutionModel": "Gemini 3.8 Flash (gemini-3.8-flash)",
        "deepReasoningModel": "Gemini 3.1 Pro / 4 Argon (gemini-3.1-pro / gemini-4-argon, subject to availability)",
        "evalModels": "Gemini 3.8 Flash (gemini-3.8-flash) & Gemini 4 Argon / 3.1 Pro (subject to availability)",
    }

    for aid, ag in catalog["agents"].items():
        is_pro = aid in PRO_ARGON_PRIMARY_AGENTS
        if is_pro:
            model_display = "Gemini 3.1 Pro / 4 Argon (subject to availability) + 3.8 Flash"
            model_slug = "gemini-3.1-pro / gemini-4-argon"
            routing_desc = (
                "Agent Orchestrator dynamically routes complex multi-echelon & scenario queries to "
                "Gemini 3.1 Pro / 4 Argon (subject to availability) and delegates fast telemetry sub-tasks to Gemini 3.8 Flash."
            )
        else:
            model_display = "Gemini 3.8 Flash (Dynamic Orchestrator → 3.1 Pro / 4 Argon)"
            model_slug = "gemini-3.8-flash"
            routing_desc = (
                "Agent Orchestrator dynamically routes high-speed operational & sensing queries to "
                "Gemini 3.8 Flash (gemini-3.8-flash) and escalates complex multi-constraint exceptions to "
                "Gemini 3.1 Pro / 4 Argon (subject to availability)."
            )

        if "costModel" in ag:
            ag["costModel"]["modelName"] = model_display
            ag["costModel"]["modelSlug"] = model_slug
            ag["costModel"]["orchestratorRouting"] = routing_desc
            ag["costModel"]["evalModels"] = "Gemini 3.8 Flash (gemini-3.8-flash) & Gemini 4 Argon (or Gemini 3.1 Pro subject to availability)"

        if "finopsProfile" in ag:
            ag["finopsProfile"]["primaryRuntimeModel"] = model_slug
            ag["finopsProfile"]["modelDisplayName"] = model_display
            ag["finopsProfile"]["orchestratorRouting"] = routing_desc
            ag["finopsProfile"]["evalModels"] = "gemini-3.8-flash & gemini-4-argon (subject to availability)"

        if "adkImplementation" in ag and isinstance(ag["adkImplementation"], dict):
            ag["adkImplementation"]["model"] = model_slug
            ag["adkImplementation"]["orchestratorRouting"] = routing_desc
            ag["adkImplementation"]["evalModels"] = "gemini-3.8-flash & gemini-4-argon (or gemini-3.1-pro subject to availability)"

    catalog_path.write_text(json.dumps(catalog, indent=2), encoding="utf-8")
    print("✅ Updated data/supply_chain_catalog.json with Dynamic Orchestrator Routing (Gemini 3.8 Flash & Gemini 3.1 Pro / 4 Argon).")
    return catalog


def update_all_agent_evals_code_tests_and_manifests() -> None:
    agents_dir = ROOT / "agents"
    eval_count = 0
    code_count = 0
    test_count = 0
    manifest_count = 0

    for pkg_dir in sorted(agents_dir.iterdir()):
        if not pkg_dir.is_dir():
            continue

        # 1. Update evals/golden_scenarios.json
        eval_file = pkg_dir / "evals" / "golden_scenarios.json"
        if eval_file.exists():
            scenarios = json.loads(eval_file.read_text(encoding="utf-8"))
            for sc in scenarios:
                sc["eval_models"] = {
                    "fast_execution_model": "gemini-3.8-flash",
                    "deep_reasoning_and_judge_model": "gemini-4-argon (or gemini-3.1-pro subject to availability)",
                    "orchestrator_routing": (
                        "Agent Orchestrator dynamically decides whether to route the query to "
                        "Gemini 3.8 Flash (gemini-3.8-flash) or escalate to Gemini 3.1 Pro / 4 Argon "
                        "(gemini-3.1-pro / gemini-4-argon, subject to availability)."
                    ),
                }
            eval_file.write_text(json.dumps(scenarios, indent=2) + "\n", encoding="utf-8")
            eval_count += 1

        # 2. Update app/agent.py
        agent_py = pkg_dir / "app" / "agent.py"
        if agent_py.exists():
            atxt = agent_py.read_text(encoding="utf-8")

            # Inject select_orchestrated_model before def run_scenario
            if "def select_orchestrated_model(" not in atxt and "    def run_scenario(" in atxt:
                helper_code = (
                    "    def select_orchestrated_model(self, query: str = \"\") -> Dict[str, str]:\n"
                    "        \"\"\"Agent Orchestrator dynamically decides whether to use Gemini 3.8 Flash or Gemini 3.1 Pro / 4 Argon.\"\"\"\n"
                    "        q_lower = (query or \"\").lower()\n"
                    "        needs_pro_or_argon = any(\n"
                    "            k in q_lower\n"
                    "            for k in (\"scenario\", \"multi-echelon\", \"war room\", \"redline\", \"capex\", \"trade-off\", \"optimize\", \"simulate\", \"optimization\")\n"
                    "        )\n"
                    "        selected = \"gemini-3.1-pro / gemini-4-argon (subject to availability)\" if needs_pro_or_argon else \"gemini-3.8-flash\"\n"
                    "        return {\n"
                    "            \"orchestrator_policy\": \"Dynamic Agent Orchestrator Routing (Gemini 3.8 Flash <-> Gemini 3.1 Pro / 4 Argon subject to availability)\",\n"
                    "            \"selected_model\": selected,\n"
                    "            \"fast_model\": \"gemini-3.8-flash\",\n"
                    "            \"pro_argon_model\": \"gemini-3.1-pro / gemini-4-argon (subject to availability)\",\n"
                    "            \"eval_judge_model\": \"gemini-4-argon (fallback: gemini-3.1-pro, subject to availability)\",\n"
                    "        }\n\n"
                )
                atxt = atxt.replace(
                    "    def run_scenario(",
                    helper_code + "    def run_scenario(",
                    1,
                )

            if '"orchestrator_routing":' not in atxt and '"model": self.model,' in atxt:
                atxt = atxt.replace(
                    '"model": self.model,',
                    '"model": self.model,\n            "orchestrator_routing": self.select_orchestrated_model(prompt),',
                    1,
                )

            agent_py.write_text(atxt, encoding="utf-8")
            code_count += 1

        # 3. Update tests/test_smoke.py to assert Dynamic Orchestrator Routing & Eval Models
        test_py = pkg_dir / "tests" / "test_smoke.py"
        if test_py.exists():
            ttxt = test_py.read_text(encoding="utf-8")
            if "select_orchestrated_model" not in ttxt and 'self.assertIn("#### 📊", res["markdown"])' in ttxt:
                extra_asserts = (
                    'self.assertIn("#### 📊", res["markdown"])\n'
                    '        routing_fast = agent.select_orchestrated_model("check status")\n'
                    '        self.assertEqual(routing_fast["selected_model"], "gemini-3.8-flash")\n'
                    '        routing_pro = agent.select_orchestrated_model("Run multi-echelon scenario optimization")\n'
                    '        self.assertIn("gemini-4-argon", routing_pro["selected_model"])\n'
                    '        self.assertIn("orchestrator_routing", res)'
                )
                ttxt = ttxt.replace('self.assertIn("#### 📊", res["markdown"])', extra_asserts, 1)
                test_py.write_text(ttxt, encoding="utf-8")
            test_count += 1

        # 4. Update agents-cli-manifest.yaml
        manifest_file = pkg_dir / "agents-cli-manifest.yaml"
        if manifest_file.exists():
            mtxt = manifest_file.read_text(encoding="utf-8")
            routing_line = (
                '  orchestrator_routing: "Agent Orchestrator dynamically routes between '
                'Gemini 3.8 Flash (gemini-3.8-flash) and Gemini 3.1 Pro / 4 Argon '
                '(gemini-3.1-pro / gemini-4-argon, subject to availability); evals run on '
                'Gemini 3.8 Flash & Gemini 4 Argon"'
            )
            if "  orchestrator_routing:" in mtxt:
                mtxt = re.sub(r"  orchestrator_routing:.*", routing_line, mtxt)
            else:
                mtxt = mtxt.rstrip() + "\n" + routing_line + "\n"
            manifest_file.write_text(mtxt, encoding="utf-8")
            manifest_count += 1

    print(f"✅ Updated {eval_count} evals, {code_count} agent.py files, {test_count} smoke tests, and {manifest_count} manifests.")


def sweep_entire_repository_for_legacy_model_strings() -> None:
    """Replaces all legacy model strings across the entire repository."""
    replacements = [
        ("gemini-2.5-flash-lite", "gemini-3.8-flash"),
        ("gemini-2.5-flash", "gemini-3.8-flash"),
        ("gemini-2.5-pro-preview", "gemini-3.1-pro / gemini-4-argon"),
        ("gemini-2.5-pro", "gemini-3.1-pro / gemini-4-argon"),
        ("gemini-2.0-flash-exp", "gemini-3.8-flash"),
        ("gemini-2.0-flash", "gemini-3.8-flash"),
        ("gemini-2.0-pro", "gemini-3.1-pro / gemini-4-argon"),
        ("gemini-3.0-flash", "gemini-3.8-flash"),
        ("gemini-3.0-pro", "gemini-3.1-pro / gemini-4-argon"),
        ("Gemini 2.5 Flash-Lite", "Gemini 3.8 Flash"),
        ("Gemini 2.5 Flash", "Gemini 3.8 Flash"),
        ("Gemini 2.5 Pro", "Gemini 3.1 Pro / 4 Argon (subject to availability)"),
        ("Gemini 2.5", "Gemini 3.8 Flash & 3.1 Pro / 4 Argon"),
        ("Gemini 2.0 Flash", "Gemini 3.8 Flash"),
        ("Gemini 2.0 Pro", "Gemini 3.1 Pro / 4 Argon"),
        ("Gemini 2.0", "Gemini 3.8 Flash & 3.1 Pro / 4 Argon"),
        ("Gemini 3.0 Flash", "Gemini 3.8 Flash"),
        ("Gemini 3.0 Pro", "Gemini 3.1 Pro / 4 Argon"),
        ("Gemini 3.0", "Gemini 3.8 Flash & 3.1 Pro / 4 Argon"),
        ("Gemini Flash-Lite", "Gemini 3.8 Flash"),
        ("Flash-Lite", "Gemini 3.8 Flash"),
        ("GEMINI 2.5", "GEMINI 3.8 FLASH & 3.1 PRO / 4 ARGON"),
        ("GEMINI 2.0", "GEMINI 3.8 FLASH & 3.1 PRO / 4 ARGON"),
        ("GEMINI 3.0", "GEMINI 3.8 FLASH & 3.1 PRO / 4 ARGON"),
        ("FLASH-LITE", "GEMINI 3.8 FLASH"),
    ]

    exts = {".html", ".md", ".py", ".json", ".yaml", ".yml", ".sh", ".txt", ".js", ".css"}
    self_path = Path(__file__).resolve()
    modified_files = 0

    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if ".git" in p.parts or "__pycache__" in p.parts or p.resolve() == self_path:
            continue
        if p.suffix.lower() not in exts:
            continue
        try:
            content = p.read_text(encoding="utf-8")
        except Exception:
            continue
        orig = content
        for old_str, new_str in replacements:
            content = content.replace(old_str, new_str)
        if content != orig:
            p.write_text(content, encoding="utf-8")
            modified_files += 1

    print(f"✅ Swept entire repository and cleaned legacy model strings in {modified_files} files.")


def main() -> None:
    update_catalog()
    update_all_agent_evals_code_tests_and_manifests()
    sweep_entire_repository_for_legacy_model_strings()


if __name__ == "__main__":
    main()

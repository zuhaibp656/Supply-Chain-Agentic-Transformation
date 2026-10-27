"""7-test unit smoke suite for [06 · Returns & ESG | Expiry & Markdowns] Food Waste & ESG Copilot (06 · Returns & Reverse Logistics — Expiry & Markdowns)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parent.parent
if str(PKG_DIR) not in sys.path:
    sys.path.insert(0, str(PKG_DIR))

from app.agent import FoodWasteEsgCopilotAgent, AGENT_CATEGORY, AGENT_DISPLAY_NAME, AGENT_DESCRIPTION
from app.render.charts import create_food_waste_esg_copilot_chart_spec
from app.render.surfaces import build_food_waste_esg_copilot_surface
from app.tools import (
    query_food_waste_esg_copilot_telemetry_feed,
    query_food_waste_esg_copilot_constraint_matrix,
    query_food_waste_esg_copilot_optimization_scenarios,
    query_food_waste_esg_copilot_execution_ledger,
    action_commit_food_waste_esg_copilot_plan,
    action_dispatch_food_waste_esg_copilot_alert,
)


class TestFoodWasteEsgCopilotAgentSmoke(unittest.TestCase):
    def test_01_category_in_name_and_description(self) -> None:
        agent = FoodWasteEsgCopilotAgent()
        self.assertIn("Expiry & Markdowns", AGENT_DISPLAY_NAME)
        self.assertIn("Expiry & Markdowns", AGENT_DESCRIPTION)
        self.assertEqual(agent.category, AGENT_CATEGORY)

    def test_02_telemetry_and_constraint_queries(self) -> None:
        r0 = query_food_waste_esg_copilot_telemetry_feed()
        r1 = query_food_waste_esg_copilot_constraint_matrix()
        self.assertEqual(r0["status"], "SUCCESS")
        self.assertGreater(len(r0["rows"]), 0)
        self.assertEqual(r1["status"], "SUCCESS")
        self.assertGreater(len(r1["rows"]), 0)

    def test_03_scenarios_and_ledger_queries(self) -> None:
        r2 = query_food_waste_esg_copilot_optimization_scenarios()
        r3 = query_food_waste_esg_copilot_execution_ledger()
        self.assertEqual(r2["status"], "SUCCESS")
        self.assertGreater(len(r2["rows"]), 0)
        self.assertEqual(r3["status"], "SUCCESS")
        self.assertGreater(len(r3["rows"]), 0)

    def test_04_quality_gate_blocks_low_confidence(self) -> None:
        blocked = action_commit_food_waste_esg_copilot_plan(confidence_score=0.40)
        self.assertEqual(blocked["status"], "BLOCKED_BY_QUALITY_GATE")

    def test_05_mutation_and_alert_commit(self) -> None:
        committed = action_commit_food_waste_esg_copilot_plan(confidence_score=0.96)
        self.assertEqual(committed["status"], "COMMITTED")
        alert = action_dispatch_food_waste_esg_copilot_alert(severity="HIGH")
        self.assertEqual(alert["status"], "DISPATCHED")

    def test_06_vega_chart_and_a2ui_surface(self) -> None:
        spec = create_food_waste_esg_copilot_chart_spec()
        self.assertIn("$schema", spec)
        parts = build_food_waste_esg_copilot_surface("test-surface")
        self.assertEqual(len(parts), 3)

    def test_07_end_to_end_scenario_execution(self) -> None:
        agent = FoodWasteEsgCopilotAgent()
        res = agent.run_scenario("Run full optimization")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertIn("#### 📊", res["markdown"])


if __name__ == "__main__":
    unittest.main()

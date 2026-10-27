"""7-test unit smoke suite for [02 · Source | Material & Packaging] Commodity Index Advisor (02 · Sourcing & Procurement — Material & Packaging)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parent.parent
if str(PKG_DIR) not in sys.path:
    sys.path.insert(0, str(PKG_DIR))

from app.agent import CommodityIndexAdvisorAgent, AGENT_CATEGORY, AGENT_DISPLAY_NAME, AGENT_DESCRIPTION
from app.render.charts import create_commodity_index_advisor_chart_spec
from app.render.surfaces import build_commodity_index_advisor_surface
from app.tools import (
    query_commodity_index_advisor_telemetry_feed,
    query_commodity_index_advisor_constraint_matrix,
    query_commodity_index_advisor_optimization_scenarios,
    query_commodity_index_advisor_execution_ledger,
    action_commit_commodity_index_advisor_plan,
    action_dispatch_commodity_index_advisor_alert,
)


class TestCommodityIndexAdvisorAgentSmoke(unittest.TestCase):
    def test_01_category_in_name_and_description(self) -> None:
        agent = CommodityIndexAdvisorAgent()
        self.assertIn("Material & Packaging", AGENT_DISPLAY_NAME)
        self.assertIn("Material & Packaging", AGENT_DESCRIPTION)
        self.assertEqual(agent.category, AGENT_CATEGORY)

    def test_02_telemetry_and_constraint_queries(self) -> None:
        r0 = query_commodity_index_advisor_telemetry_feed()
        r1 = query_commodity_index_advisor_constraint_matrix()
        self.assertEqual(r0["status"], "SUCCESS")
        self.assertGreater(len(r0["rows"]), 0)
        self.assertEqual(r1["status"], "SUCCESS")
        self.assertGreater(len(r1["rows"]), 0)

    def test_03_scenarios_and_ledger_queries(self) -> None:
        r2 = query_commodity_index_advisor_optimization_scenarios()
        r3 = query_commodity_index_advisor_execution_ledger()
        self.assertEqual(r2["status"], "SUCCESS")
        self.assertGreater(len(r2["rows"]), 0)
        self.assertEqual(r3["status"], "SUCCESS")
        self.assertGreater(len(r3["rows"]), 0)

    def test_04_quality_gate_blocks_low_confidence(self) -> None:
        blocked = action_commit_commodity_index_advisor_plan(confidence_score=0.40)
        self.assertEqual(blocked["status"], "BLOCKED_BY_QUALITY_GATE")

    def test_05_mutation_and_alert_commit(self) -> None:
        committed = action_commit_commodity_index_advisor_plan(confidence_score=0.96)
        self.assertEqual(committed["status"], "COMMITTED")
        alert = action_dispatch_commodity_index_advisor_alert(severity="HIGH")
        self.assertEqual(alert["status"], "DISPATCHED")

    def test_06_vega_chart_and_a2ui_surface(self) -> None:
        spec = create_commodity_index_advisor_chart_spec()
        self.assertIn("$schema", spec)
        parts = build_commodity_index_advisor_surface("test-surface")
        self.assertEqual(len(parts), 3)

    def test_07_end_to_end_scenario_execution(self) -> None:
        agent = CommodityIndexAdvisorAgent()
        res = agent.run_scenario("Run full optimization")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertIn("#### 📊", res["markdown"])
        routing_fast = agent.select_orchestrated_model("check status")
        self.assertEqual(routing_fast["selected_model"], "gemini-3.8-flash")
        routing_pro = agent.select_orchestrated_model("Run multi-echelon scenario optimization")
        self.assertIn("gemini-4-argon", routing_pro["selected_model"])
        self.assertIn("orchestrator_routing", res)


if __name__ == "__main__":
    unittest.main()

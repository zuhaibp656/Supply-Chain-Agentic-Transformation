"""Comprehensive deterministic smoke & persona workflow tests for [06 · Return | Expiry & Markdowns] Zero-Waste & Organic Circularity Copilot."""
from __future__ import annotations

from pathlib import Path
import sys
import unittest

PKG_ROOT = Path(__file__).resolve().parent.parent
if str(PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(PKG_ROOT))

from app.agent import FoodWasteEsgCopilotAgent  # noqa: E402
from app import tools  # noqa: E402


class TestFoodWasteEsgCopilotSmoke(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = FoodWasteEsgCopilotAgent()

    def test_01_systems_and_master_backbone_join(self) -> None:
        sys_info = tools.list_systems()
        self.assertEqual(sys_info["organization_id"], "XYZ-CORP-01")
        self.assertEqual(len(sys_info["systems"]), 4)
        master = tools.lookup_xyz_master_context(sku_id="SKU-XYZ-204", facility_id="PLANT-XYZ-AUSTIN")
        self.assertEqual(master["status"], "SUCCESS")
        self.assertIsNotNone(master.get("material"))
        self.assertIsNotNone(master.get("facility"))

    def test_02_all_four_domain_tables_have_realistic_8_rows(self) -> None:
        for fn_name in ['query_facility_organic_spoilage_streams', 'query_epa_diversion_partners', 'query_digestion_and_compost_economics', 'query_zero_waste_scope3_ledger']:
            res = self.agent.execute_tool(fn_name)
            self.assertEqual(res["status"], "SUCCESS")
            self.assertGreaterEqual(res["row_count"], 8, f"{fn_name} must return >=8 rows")

    def test_03_python_mathematical_analysis_solver(self) -> None:
        res = self.agent.execute_tool('analyze_epa_hierarchy_waste_diversion')
        self.assertEqual(res["status"], "SUCCESS")
        self.assertGreaterEqual(res["records_evaluated"], 8)
        self.assertIn("kpi_summary", res)
        self.assertIn("ranked_drivers", res)
        self.assertTrue(res["concise_markdown_table"].startswith("| Record |"))

    def test_04_png_infographic_and_vegalite_chart_generation(self) -> None:
        chart = self.agent.execute_tool("render_visual_chart")
        self.assertEqual(chart["status"], "SUCCESS")
        self.assertTrue(chart["a2ui_vega_lite_queued"])
        png_path = Path(chart["png_infographic"]["png_path"])
        if chart["png_infographic"]["status"] == "SUCCESS":
            self.assertTrue(png_path.exists())
            self.assertGreater(png_path.stat().st_size, 1500)

    def test_05_persona_operational_drafting_tool(self) -> None:
        draft = self.agent.execute_tool('draft_csrd_esrs_e5_circularity_disclosure')
        self.assertEqual(draft["status"], "DRAFT_READY")
        self.assertIn("XYZ-CORP-01", draft["markdown_draft"])

    def test_06_write_back_quality_gate_blocks_missing_inputs(self) -> None:
        blocked = self.agent.execute_tool('action_dispatch_circular_depackaging_load')
        self.assertIn(blocked.get("error"), ("missing_required_inputs", "missing_idempotency_key"))

    def test_07_orchestrator_model_routing(self) -> None:
        fast = self.agent.select_orchestrated_model("Check status of current lot")
        self.assertEqual(fast["selected_model"], "gemini-3.8-flash")
        deep = self.agent.select_orchestrated_model("Simulate multi-echelon trade-off scenario")
        self.assertIn("gemini-3.1-pro", deep["selected_model"])

    def test_08_end_to_end_scenario_and_a2ui_card(self) -> None:
        out = self.agent.run_scenario("Execute full persona audit")
        self.assertEqual(out["status"], "SUCCESS")
        self.assertEqual(len(out["a2ui_surface"]), 3)
        self.assertTrue(out["mutation_receipt"]["action_id"].startswith("ACT-"))


if __name__ == "__main__":
    unittest.main()

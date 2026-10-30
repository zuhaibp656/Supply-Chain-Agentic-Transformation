"""Persona enrichment verification tests for promo_lift_simulator (8-row data, Python math, PNG/Vega charts, drafting)."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

PKG_ROOT = Path(__file__).resolve().parent.parent
if str(PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(PKG_ROOT))

from app.agent import PromoLiftSimulatorAgent  # noqa: E402
from app import tools  # noqa: E402


class TestPersonaEnrichment(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = PromoLiftSimulatorAgent()

    def test_tables_have_at_least_8_realistic_rows(self) -> None:
        tdir = PKG_ROOT / "fixtures" / "tables"
        json_files = sorted(tdir.glob("*.json"))
        self.assertGreaterEqual(len(json_files), 3)
        for jf in json_files:
            rows = json.loads(jf.read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(rows), 8, f"{jf.name} has fewer than 8 rows")

    def test_master_backbone_join_and_python_analytics(self) -> None:
        m = self.agent.execute_tool("lookup_xyz_master_context", sku_id="SKU-XYZ-101", facility_id="PLANT-XYZ-STUTTGART")
        self.assertEqual(m["status"], "SUCCESS")
        self.assertIsNotNone(m.get("material"))
        res = self.agent.execute_tool("analyze_operational_metrics")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertGreaterEqual(res["records_evaluated"], 8)
        self.assertIn("kpi_summary", res)

    def test_visual_png_and_vegalite_chart_and_brief_drafting(self) -> None:
        ch = self.agent.execute_tool("render_visual_chart")
        self.assertEqual(ch["status"], "SUCCESS")
        self.assertTrue(ch["a2ui_vega_lite_queued"])
        if ch["png_infographic"]["status"] == "SUCCESS":
            self.assertTrue(Path(ch["png_infographic"]["png_path"]).exists())
        dr = self.agent.execute_tool("draft_operational_brief")
        self.assertEqual(dr["status"], "DRAFT_READY")
        self.assertIn("XYZ-CORP-01", dr["markdown_draft"])


if __name__ == "__main__":
    unittest.main()

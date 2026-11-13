"""Archetype & Intelligent HTML Decisioning verification tests for keep_it_routing_advisor."""
from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

os.environ.setdefault("SC_SKIP_GCS_UPLOAD", "1")

PKG_ROOT = Path(__file__).resolve().parent.parent
if str(PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(PKG_ROOT))

from app import agent as agent_mod  # noqa: E402
from app import tools  # noqa: E402


class TestArchetypeSmartHtml(unittest.TestCase):
    def tearDown(self) -> None:
        tools.finalize_turn_gcs_state(timeout=1.0)

    def test_instruction_clean_and_archetype_aware(self) -> None:
        instr = getattr(agent_mod, "_INSTRUCTION", "")
        self.assertNotIn("XYZ Global Industries Corp.", instr)
        self.assertEqual(getattr(tools, "_AGENT_ARCHETYPE", ""), "simulator")
        self.assertIn("INTELLIGENT HTML COCKPIT", instr)

    def test_simple_query_skips_unwanted_html_even_with_data_activity(self) -> None:
        tools.finalize_turn_gcs_state(timeout=1.0)
        tools.set_turn_user_query("What is our top urgent exception on SKU-1 today?")
        tools.mark_turn_activity()
        self.assertFalse(tools.should_emit_html_cockpit())
        art = tools.ensure_turn_gcs_artifacts()
        self.assertEqual(art["html_url"], "")

    def test_simulation_or_interactive_query_enables_html(self) -> None:
        tools.finalize_turn_gcs_state(timeout=1.0)
        tools.set_turn_user_query("Compare options in an interactive what-if simulator dashboard")
        tools.mark_turn_activity()
        self.assertTrue(tools.should_emit_html_cockpit())
        art = tools.ensure_turn_gcs_artifacts()
        self.assertTrue(art["html_url"].endswith(".html"))

    def test_explicit_html_tool_call_enables_html(self) -> None:
        tools.finalize_turn_gcs_state(timeout=1.0)
        tools.set_turn_user_query("Give me a quick status update")
        res = tools.generate_interactive_html_dashboard()
        self.assertEqual(res["status"], "SUCCESS")
        self.assertTrue(tools.should_emit_html_cockpit())


if __name__ == "__main__":
    unittest.main()

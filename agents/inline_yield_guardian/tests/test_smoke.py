"""Smoke test suite for VisionInspect Inline Quality Inspection Agent."""
import os
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import InlineQualityInspectionAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "inline_yield_guardian"
    assert len(res["systems"]) >= 4
    system_ids = [s["id"] for s in res["systems"]]
    assert "inline_vision_camera_feed" in system_ids
    assert "gemini_flash_multimodal_vision" in system_ids
    assert "veeva_qualityone_ebhr" in system_ids
    assert "sap_qm_inline_gate" in system_ids


def test_query_camera_vision_inspection_frames():
    res = tools.query_camera_vision_inspection_frames(line_id="LINE-ASEPTIC-01")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["frame_id"] == "FRAME-CAM01-20261022-00841"
    assert record["sku_code"] == "SKU-BEV-OATMILK-ORIGINAL-1L"
    assert record["illumination_lux"] == 4200


def test_query_vision_defect_classification_results():
    res = tools.query_vision_defect_classification_results(defect_type="SEAL")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["classification_id"] == "CLS-FLASH-VISION-20261022-00841"
    assert record["vision_model"] == "gemini-3.8-flash"
    assert record["confidence_score"] == 0.985
    assert record["defect_severity"] == "CRITICAL_CONTAMINATION_RISK"


def test_query_pneumatic_reject_gate_events():
    res = tools.query_pneumatic_reject_gate_events(line_id="LINE-ASEPTIC-01")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["pneumatic_diverter_id"] == "DIVERTER-SOLENOID-LINE01-A"
    assert record["actuation_latency_ms"] == 14.2
    assert record["status"] == "PNEUMATIC_DIVERTER_FIRED_REJECTED"


def test_query_ebhr_batch_record_deviations():
    res = tools.query_ebhr_batch_record_deviations(batch_number="BATCH-OAT-2026W42-01")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["deviation_id"] == "DEV-EBHR-20261022-044"
    assert record["severity"] == "CRITICAL_CONTAINMENT"
    assert record["veeva_ticket_id"] == "VEEVA-QMS-DEV-99214"


def test_quality_gate_blocks_invalid_inputs():
    agent = InlineQualityInspectionAgent()
    # Missing idempotency key
    res = agent.execute_tool(
        "action_trigger_pneumatic_reject_diverter",
        frame_id="FRAME-001",
        line_id="LINE-01",
        pneumatic_diverter_id="DIVERTER-01",
        defect_type="SEAL_TEAR",
        rationale="Micro leak test"
    )
    assert res.get("error") == "missing_idempotency_key"

    # Missing required field
    res2 = agent.execute_tool(
        "action_trigger_pneumatic_reject_diverter",
        frame_id="",
        line_id="LINE-01",
        pneumatic_diverter_id="DIVERTER-01",
        defect_type="SEAL_TEAR",
        rationale="Micro leak test",
        idempotency_key="TEST-KEY-DIV-01"
    )
    assert res2.get("error") == "missing_required_inputs"
    assert "frame_id" in res2.get("missing", [])


def test_end_to_end_scenario_execution():
    agent = InlineQualityInspectionAgent()
    query = "Monitor high-speed optical vision feed on Line Aseptic 01, identify induction seal defect, fire pneumatic reject gate, and log eBHR quality deviation."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) >= 2

    divert_action = result["actions_executed"][0]
    assert divert_action["status"] == "PNEUMATIC_DIVERTER_ACTIVATED"
    assert "DIVERT-PNEUM" in divert_action["divert_id"]
    assert divert_action["actuation_latency_ms"] == 14.2

    ebhr_action = result["actions_executed"][1]
    assert ebhr_action["status"] == "EBHR_DEVIATION_LOGGED"
    assert "DEV-LOG-EBHR" in ebhr_action["deviation_log_id"]
    assert "VEEVA-QMS" in ebhr_action["veeva_ticket_id"]

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) >= 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify copy-ready markdown tables
    markdown = result["markdown"]
    assert "### 👁️ VisionInspect Inline Quality Inspection & Defect Containment Briefing" in markdown
    assert "| Frame ID | Inspection Station | Defect Classification |" in markdown
    assert "INDUCTION_FOIL_SEAL_TEAR" in markdown
    assert "14.2 ms" in markdown
    assert "Pneumatic Solenoid Reject Actuated" in markdown
    assert "eBHR Quality Deviation Logged" in markdown


if __name__ == "__main__":
    test_list_systems()
    print("✓ test_list_systems passed")
    test_query_camera_vision_inspection_frames()
    print("✓ test_query_camera_vision_inspection_frames passed")
    test_query_vision_defect_classification_results()
    print("✓ test_query_vision_defect_classification_results passed")
    test_query_pneumatic_reject_gate_events()
    print("✓ test_query_pneumatic_reject_gate_events passed")
    test_query_ebhr_batch_record_deviations()
    print("✓ test_query_ebhr_batch_record_deviations passed")
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

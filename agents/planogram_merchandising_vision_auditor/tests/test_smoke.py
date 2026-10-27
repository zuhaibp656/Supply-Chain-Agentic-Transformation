"""Smoke test suite for ShelfVision — Retail Planogram & Visibility Auditor (planogram_merchandising_vision_auditor)."""
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import PlanogramMerchandisingVisionAuditor
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "planogram_merchandising_vision_auditor"
    assert len(res["systems"]) >= 4

def test_query_store_shelf_vision_audit_captures():
    res = tools.query_store_shelf_vision_audit_captures(capture_id="IMG-SHLF-20261022-409")
    assert res["total"] > 0
    assert res["table"] == "store_shelf_vision_audit_captures"
    assert len(res["rows"]) >= 1


def test_query_contracted_planogram_templates():
    res = tools.query_contracted_planogram_templates(template_id="PLG-BEV-GONDOLA-Q4")
    assert res["total"] > 0
    assert res["table"] == "contracted_planogram_templates"
    assert len(res["rows"]) >= 1


def test_query_shelf_compliance_scoring_ledger():
    res = tools.query_shelf_compliance_scoring_ledger(outlet_id="OUTLET-HYPER-882")
    assert res["total"] > 0
    assert res["table"] == "shelf_compliance_scoring_ledger"
    assert len(res["rows"]) >= 1


def test_query_merchandising_corrective_tasks():
    res = tools.query_merchandising_corrective_tasks(outlet_id="OUTLET-HYPER-882")
    assert res["total"] > 0
    assert res["table"] == "merchandising_corrective_tasks"
    assert len(res["rows"]) >= 1


def test_quality_gate_blocks_invalid_inputs():
    agent = PlanogramMerchandisingVisionAuditor()
    # 1. Missing idempotency_key
    res = agent.execute_tool(
        "action_dispatch_instore_restock_directive",
        capture_id='IMG-SHLF-20261022-409',
        outlet_id='OUTLET-HYPER-882',
        fso_id='FSO-WEST-112',
        missing_facings_count=5,
        rationale='Gemini 3.8 Flash detected 32.1% Share-of-Shelf (9/14 eye-level facings, 2 empty gaps, 3 competitor intrusions) in 1.18s; pushed instant restock prompt to FSO-WEST-112 while still in store.'
    )
    assert res.get("error") == "missing_idempotency_key"

    # 2. Missing required input fields
    res2 = agent.execute_tool(
        "action_dispatch_instore_restock_directive",
        idempotency_key="TEST-KEY-01"
    )
    assert res2.get("error") == "missing_required_inputs"


def test_end_to_end_scenario_execution():
    agent = PlanogramMerchandisingVisionAuditor()
    result = agent.run_scenario("Execute end-to-end optimization and action write-back.")
    assert result["status"] == "success"
    assert result["agent"] == "planogram_merchandising_vision_auditor"
    assert result["findings_count"] == 4
    assert len(result["actions_executed"]) >= 2
    assert result["actions_executed"][0]["status"] == "INSTORE_RESTOCK_DIRECTIVE_SENT"
    assert result["actions_executed"][1]["status"] == "PLANOGRAM_COMPLIANCE_CERTIFIED"

    # Verify A2UI v0.9 surface compliance (Card wrapping ONLY VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) >= 2
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify copy-ready markdown output
    md = result["markdown"]
    assert "### ✦" in md
    assert "| Dimension | Metric Value |" in md
    assert "### 🔗 Connected Enterprise Systems" in md


if __name__ == "__main__":
    test_list_systems()
    print("✓ test_list_systems passed")
    test_query_store_shelf_vision_audit_captures()
    print('✓ test_query_store_shelf_vision_audit_captures passed')
    test_query_contracted_planogram_templates()
    print('✓ test_query_contracted_planogram_templates passed')
    test_query_shelf_compliance_scoring_ledger()
    print('✓ test_query_shelf_compliance_scoring_ledger passed')
    test_query_merchandising_corrective_tasks()
    print('✓ test_query_merchandising_corrective_tasks passed')
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

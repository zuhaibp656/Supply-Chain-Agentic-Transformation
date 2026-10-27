"""Smoke test suite for ReturnLoop — Autonomous RMA Grading & Backhaul Optimizer (reverse_rma_optimizer)."""
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import ReverseRmaOptimizer
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "reverse_rma_optimizer"
    assert len(res["systems"]) >= 4

def test_query_customer_rma_intake_requests():
    res = tools.query_customer_rma_intake_requests(rma_id="RMA-20261022-501")
    assert res["total"] > 0
    assert res["table"] == "customer_rma_intake_requests"
    assert len(res["rows"]) >= 1


def test_query_multimodal_vision_grading_results():
    res = tools.query_multimodal_vision_grading_results(rma_id="RMA-20261022-501")
    assert res["total"] > 0
    assert res["table"] == "multimodal_vision_grading_results"
    assert len(res["rows"]) >= 1


def test_query_fleet_backhaul_pickup_slots():
    res = tools.query_fleet_backhaul_pickup_slots(rma_id="RMA-20261022-501")
    assert res["total"] > 0
    assert res["table"] == "fleet_backhaul_pickup_slots"
    assert len(res["rows"]) >= 1


def test_query_circular_disposition_routing_ledger():
    res = tools.query_circular_disposition_routing_ledger(rma_id="RMA-20261022-501")
    assert res["total"] > 0
    assert res["table"] == "circular_disposition_routing_ledger"
    assert len(res["rows"]) >= 1


def test_quality_gate_blocks_invalid_inputs():
    agent = ReverseRmaOptimizer()
    # 1. Missing idempotency_key
    res = agent.execute_tool(
        "action_assign_rma_disposition_and_backhaul",
        rma_id='RMA-20261022-501',
        optical_grade='GRADE_A_FACTORY_SEAL_INTACT',
        target_facility_id='FDC-AUSTIN-02',
        backhaul_vehicle_id='TRK-12T-TX14',
        rationale='Gemini 3.8 Flash verified factory tamper seal intact (Grade A); routed 12 units directly to Austin FDC-02 for immediate resale via returning truck TRK-12T-TX14, recovering 94% value ($9,024) and saving $420 LTL freight.'
    )
    assert res.get("error") == "missing_idempotency_key"

    # 2. Missing required input fields
    res2 = agent.execute_tool(
        "action_assign_rma_disposition_and_backhaul",
        idempotency_key="TEST-KEY-01"
    )
    assert res2.get("error") == "missing_required_inputs"


def test_end_to_end_scenario_execution():
    agent = ReverseRmaOptimizer()
    result = agent.run_scenario("Execute end-to-end optimization and action write-back.")
    assert result["status"] == "success"
    assert result["agent"] == "reverse_rma_optimizer"
    assert result["findings_count"] == 4
    assert len(result["actions_executed"]) >= 2
    assert result["actions_executed"][0]["status"] == "RMA_DISPOSITION_AND_BACKHAUL_LOCKED"
    assert result["actions_executed"][1]["status"] == "INSTANT_RMA_CREDIT_ISSUED"

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
    test_query_customer_rma_intake_requests()
    print('✓ test_query_customer_rma_intake_requests passed')
    test_query_multimodal_vision_grading_results()
    print('✓ test_query_multimodal_vision_grading_results passed')
    test_query_fleet_backhaul_pickup_slots()
    print('✓ test_query_fleet_backhaul_pickup_slots passed')
    test_query_circular_disposition_routing_ledger()
    print('✓ test_query_circular_disposition_routing_ledger passed')
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

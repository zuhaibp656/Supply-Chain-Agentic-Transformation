"""Smoke test suite for FlowMaster Finite Production Scheduler."""
import os
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import FiniteProductionSchedulerAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "line_schedule_optimizer"
    assert len(res["systems"]) >= 4
    system_ids = [s["id"] for s in res["systems"]]
    assert "or_tools_cpsat_solver" in system_ids
    assert "sap_ppds_production" in system_ids
    assert "changeover_matrix_vault" in system_ids
    assert "plant_line_workcenters" in system_ids


def test_query_production_orders_backlog():
    res = tools.query_production_orders_backlog(product_family="BEVERAGE_OAT_BASE")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["order_id"] == "ORD-PROD-202610-771"
    assert record["allergen_group"] == "NON_ALLERGENIC"
    assert record["run_rate_liters_per_hour"] == 7500.0


def test_query_changeover_matrix_rules():
    res = tools.query_changeover_matrix_rules(from_family="BEVERAGE_NUT_BASE")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["changeover_type"] == "DEEP_ALLERGEN_CIP_WASH_ATP_SWAB"
    assert record["setup_duration_hours"] == 4.0


def test_query_plant_line_workcenters():
    res = tools.query_plant_line_workcenters(workcenter_id="WC-LINE-ASEPTIC-01")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["max_throughput_liters_hr"] == 9000
    assert record["plant_id"] == "PLANT-1020-AUSTIN"


def test_query_optimized_sequence_schedule():
    res = tools.query_optimized_sequence_schedule(schedule_id="SCHED-OR-TOOLS-2026W42-01")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["changeover_hours_saved"] == 5.0
    assert record["capacity_gain_value_usd"] == 18750.0
    assert len(record["sequence_blocks"]) == 3


def test_quality_gate_blocks_empty_order_list():
    agent = FiniteProductionSchedulerAgent()
    # Missing idempotency key
    res = agent.execute_tool(
        "action_solve_and_lock_finite_sequence",
        workcenter_id="WC-001",
        order_ids=["ORD-1"],
        objective_type="MINIMIZE_CHANGEOVER",
        rationale="Test solve"
    )
    assert res.get("error") == "missing_idempotency_key"

    # Empty order list
    res2 = agent.execute_tool(
        "action_solve_and_lock_finite_sequence",
        workcenter_id="WC-001",
        order_ids=[],
        objective_type="MINIMIZE_CHANGEOVER",
        rationale="Empty orders solve",
        idempotency_key="TEST-KEY-010"
    )
    assert res2.get("error") == "empty_order_list"


def test_end_to_end_scenario_execution():
    agent = FiniteProductionSchedulerAgent()
    query = "Sequence unscheduled production orders for Line 01 in SAP PP/DS, apply allergen changeover matrix, solve with OR-Tools CP-SAT to minimize CIP downtime, and dispatch locked blocks."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) == 2

    seq_action = result["actions_executed"][0]
    assert seq_action["status"] == "OR_TOOLS_SEQUENCE_LOCKED"
    assert "SEQ-CPSAT" in seq_action["sequence_id"]
    assert seq_action["changeover_hours_saved"] == 5.0

    disp_action = result["actions_executed"][1]
    assert disp_action["status"] == "SAP_PPDS_SCHEDULE_DISPATCHED"
    assert "PPDS-DISP" in disp_action["dispatch_id"]
    assert disp_action["workcenter_id"] == "WC-LINE-ASEPTIC-01"

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) == 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify copy-ready markdown tables
    markdown = result["markdown"]
    assert "### ⏱️ FlowMaster Finite Production Line Sequence Briefing" in markdown
    assert "| Seq | Production Order | Material Description |" in markdown
    assert "ORD-PROD-202610-771" in markdown
    assert "5.0 hrs" in markdown
    assert "OR-Tools CP-SAT Sequence Locked" in markdown
    assert "SAP PP/DS Sequence Dispatched" in markdown


if __name__ == "__main__":
    test_list_systems()
    print("✓ test_list_systems passed")
    test_query_production_orders_backlog()
    print("✓ test_query_production_orders_backlog passed")
    test_query_changeover_matrix_rules()
    print("✓ test_query_changeover_matrix_rules passed")
    test_query_plant_line_workcenters()
    print("✓ test_query_plant_line_workcenters passed")
    test_query_optimized_sequence_schedule()
    print("✓ test_query_optimized_sequence_schedule passed")
    test_quality_gate_blocks_empty_order_list()
    print("✓ test_quality_gate_blocks_empty_order_list passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

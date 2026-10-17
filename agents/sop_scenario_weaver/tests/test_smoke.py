"""Smoke test suite for Synapse Autonomous S&OP Scenario Weaver."""
import os
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import SopScenarioWeaverAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "sop_scenario_weaver"
    assert len(res["systems"]) >= 4
    system_ids = [s["id"] for s in res["systems"]]
    assert "spanner_constraint_graph" in system_ids
    assert "bigquery_cortex_pnl" in system_ids
    assert "google_ortools_milp" in system_ids


def test_query_unconstrained_demand_gaps():
    res = tools.query_unconstrained_demand_gaps(plan_month="2026-11")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["gap_units"] > 0
    assert record["unmet_revenue_usd"] > 1000000


def test_query_plant_line_capacities():
    res = tools.query_plant_line_capacities(is_bottleneck=True)
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["utilization_pct"] > 90.0
    assert record["is_bottleneck"] is True


def test_query_supplier_allocations():
    res = tools.query_supplier_allocations()
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["remaining_quota_units"] > 0
    assert record["lead_time_days"] > 0


def test_query_sop_scenario_evaluations():
    res = tools.query_sop_scenario_evaluations()
    assert res["total"] >= 3
    pareto = next((r for r in res["rows"] if "PARETO" in r["scenario_id"]), None)
    assert pareto is not None
    assert pareto["gross_margin_pct"] > 65.0
    assert pareto["otif_delivery_pct"] > 98.0


def test_quality_gate_blocks_excessive_overtime_budget():
    agent = SopScenarioWeaverAgent()
    # Missing idempotency key
    res = agent.execute_tool(
        "action_commit_mps_consensus_plan",
        scenario_id="SCEN-TEST",
        business_unit="CPG",
        committed_volume_units=1000000,
        approved_overtime_cost_usd=100000.0,
        rationale="Overtime test"
    )
    assert res.get("error") == "missing_idempotency_key"

    # Exceeds delegation threshold ($500k)
    res2 = agent.execute_tool(
        "action_commit_mps_consensus_plan",
        scenario_id="SCEN-TEST",
        business_unit="CPG",
        committed_volume_units=1000000,
        approved_overtime_cost_usd=850000.0,
        rationale="Over budget",
        idempotency_key="TEST-KEY-002"
    )
    assert res2.get("error") == "overtime_cost_exceeds_delegation_authority"


def test_end_to_end_scenario_execution():
    agent = SopScenarioWeaverAgent()
    query = "Analyze unconstrained demand gap on Hydration RTD, solve Pareto frontier in OR-Tools, and commit consensus MPS plan to SAP PP/DS."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) == 2

    mps_action = result["actions_executed"][0]
    assert mps_action["status"] == "MPS_COMMITTED_TO_SAP"
    assert "MPS-SOP" in mps_action["mps_id"]
    assert mps_action["committed_volume_units"] == 4750000

    fpa_action = result["actions_executed"][1]
    assert fpa_action["status"] == "FPA_FINANCIAL_LOCKED"
    assert "FPA-BRIDGE" in fpa_action["fpa_id"]
    assert fpa_action["target_gross_margin_usd"] == 48600000.0

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) == 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify deterministic copy-ready table and markdown structure
    assert "markdown" in result
    assert "| Scenario ID |" in result["markdown"]
    assert "### ⚖️ Synapse Autonomous S&OP" in result["markdown"]
    assert "### 🔗 Connected Systems" in result["markdown"]


if __name__ == "__main__":
    print("Running Synapse S&OP Scenario Weaver smoke tests...")
    test_list_systems()
    test_query_unconstrained_demand_gaps()
    test_query_plant_line_capacities()
    test_query_supplier_allocations()
    test_query_sop_scenario_evaluations()
    test_quality_gate_blocks_excessive_overtime_budget()
    test_end_to_end_scenario_execution()
    print("✅ All 7 Synapse S&OP Scenario Weaver smoke tests passed successfully!")

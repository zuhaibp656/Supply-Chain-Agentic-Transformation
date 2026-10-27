"""Smoke test suite for TwinDesign — Supply Chain Network & Cost-to-Serve Optimizer (network_twin_architect)."""
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import NetworkTwinArchitect
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "network_twin_architect"
    assert len(res["systems"]) >= 4

def test_query_network_facility_nodes_and_leases():
    res = tools.query_network_facility_nodes_and_leases(facility_id="RDC-COLUMBUS-OH")
    assert res["total"] > 0
    assert res["table"] == "network_facility_nodes_and_leases"
    assert len(res["rows"]) >= 1


def test_query_sku_customer_cost_to_serve_matrix():
    res = tools.query_sku_customer_cost_to_serve_matrix(customer_segment_id="SEG-SOUTHEAST-L2")
    assert res["total"] > 0
    assert res["table"] == "sku_customer_cost_to_serve_matrix"
    assert len(res["rows"]) >= 1


def test_query_center_of_gravity_milp_scenarios():
    res = tools.query_center_of_gravity_milp_scenarios(scenario_id="SCEN-COG-SE-2026")
    assert res["total"] > 0
    assert res["table"] == "center_of_gravity_milp_scenarios"
    assert len(res["rows"]) >= 1


def test_query_network_stress_test_simulations():
    res = tools.query_network_stress_test_simulations(stress_test_id="STRESS-TARIFF-60PCT")
    assert res["total"] > 0
    assert res["table"] == "network_stress_test_simulations"
    assert len(res["rows"]) >= 1


def test_quality_gate_blocks_invalid_inputs():
    agent = NetworkTwinArchitect()
    # 1. Missing idempotency_key
    res = agent.execute_tool(
        "action_publish_network_territory_realignment",
        scenario_id='SCEN-COG-SE-2026',
        new_hub_id='3PL-SAVANNAH-EXP',
        annual_savings_usd=6840000.0,
        rationale='OR-Tools Center-of-Gravity MILP reassigned 142 Southeast zip-3 territories from Columbus OH to Savannah 3PL hub, cutting stem miles by 14.6% and saving $6.84M/yr.'
    )
    assert res.get("error") == "missing_idempotency_key"

    # 2. Missing required input fields
    res2 = agent.execute_tool(
        "action_publish_network_territory_realignment",
        idempotency_key="TEST-KEY-01"
    )
    assert res2.get("error") == "missing_required_inputs"


def test_end_to_end_scenario_execution():
    agent = NetworkTwinArchitect()
    result = agent.run_scenario("Execute end-to-end optimization and action write-back.")
    assert result["status"] == "success"
    assert result["agent"] == "network_twin_architect"
    assert result["findings_count"] == 4
    assert len(result["actions_executed"]) >= 2
    assert result["actions_executed"][0]["status"] == "NETWORK_TERRITORY_REALIGNED"
    assert result["actions_executed"][1]["status"] == "COST_TO_SERVE_POLICY_UPDATED"

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
    test_query_network_facility_nodes_and_leases()
    print('✓ test_query_network_facility_nodes_and_leases passed')
    test_query_sku_customer_cost_to_serve_matrix()
    print('✓ test_query_sku_customer_cost_to_serve_matrix passed')
    test_query_center_of_gravity_milp_scenarios()
    print('✓ test_query_center_of_gravity_milp_scenarios passed')
    test_query_network_stress_test_simulations()
    print('✓ test_query_network_stress_test_simulations passed')
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

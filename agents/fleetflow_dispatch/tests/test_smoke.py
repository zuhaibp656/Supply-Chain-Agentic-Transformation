"""Smoke test suite for FleetFlow — Google Maps Corridor Route & Fleet Dispatch Studio (fleetflow_dispatch)."""
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import FleetflowDispatch
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "fleetflow_dispatch"
    assert len(res["systems"]) >= 4

def test_query_corridor_delivery_orders():
    res = tools.query_corridor_delivery_orders(corridor_id="CORR-I35-TEX")
    assert res["total"] > 0
    assert res["table"] == "corridor_delivery_orders"
    assert len(res["rows"]) >= 1


def test_query_fleet_vehicle_telematics_hos():
    res = tools.query_fleet_vehicle_telematics_hos(vehicle_id="TRK-24T-TX08")
    assert res["total"] > 0
    assert res["table"] == "fleet_vehicle_telematics_hos"
    assert len(res["rows"]) >= 1


def test_query_google_maps_corridor_routes():
    res = tools.query_google_maps_corridor_routes(route_id="RTE-I35-20261022-01")
    assert res["total"] > 0
    assert res["table"] == "google_maps_corridor_routes"
    assert len(res["rows"]) >= 1


def test_query_backhaul_consolidation_opportunities():
    res = tools.query_backhaul_consolidation_opportunities(backhaul_id="BKH-SAT-DAL-44")
    assert res["total"] > 0
    assert res["table"] == "backhaul_consolidation_opportunities"
    assert len(res["rows"]) >= 1


def test_quality_gate_blocks_invalid_inputs():
    agent = FleetflowDispatch()
    # 1. Missing idempotency_key
    res = agent.execute_tool(
        "action_dispatch_corridor_route_manifest",
        route_id='RTE-I35-20261022-01',
        vehicle_id='TRK-24T-TX08',
        corridor_id='CORR-I35-TEX',
        stop_count=3,
        rationale='OR-Tools CVRPTW + Google Maps Routes Preferred solved 3-stop I-35 corridor route (18,450 kg / 72.3 m3) cutting stem distance by 19.4% with 99.4% SLA confidence.'
    )
    assert res.get("error") == "missing_idempotency_key"

    # 2. Missing required input fields
    res2 = agent.execute_tool(
        "action_dispatch_corridor_route_manifest",
        idempotency_key="TEST-KEY-01"
    )
    assert res2.get("error") == "missing_required_inputs"


def test_end_to_end_scenario_execution():
    agent = FleetflowDispatch()
    result = agent.run_scenario("Execute end-to-end optimization and action write-back.")
    assert result["status"] == "success"
    assert result["agent"] == "fleetflow_dispatch"
    assert result["findings_count"] == 4
    assert len(result["actions_executed"]) == 2
    assert result["actions_executed"][0]["status"] == "CORRIDOR_ROUTE_DISPATCHED"
    assert result["actions_executed"][1]["status"] == "BACKHAUL_RETURN_ASSIGNED"

    # Verify A2UI v0.9 surface compliance (Card wrapping ONLY VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) == 2
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify copy-ready markdown output
    md = result["markdown"]
    assert "### ✦" in md
    assert "| Dimension | Metric Value |" in md
    assert "### 🔗 Connected Enterprise Systems" in md


if __name__ == "__main__":
    test_list_systems()
    print("✓ test_list_systems passed")
    test_query_corridor_delivery_orders()
    print('✓ test_query_corridor_delivery_orders passed')
    test_query_fleet_vehicle_telematics_hos()
    print('✓ test_query_fleet_vehicle_telematics_hos passed')
    test_query_google_maps_corridor_routes()
    print('✓ test_query_google_maps_corridor_routes passed')
    test_query_backhaul_consolidation_opportunities()
    print('✓ test_query_backhaul_consolidation_opportunities passed')
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

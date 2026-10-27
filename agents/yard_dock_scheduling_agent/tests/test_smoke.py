"""Smoke test suite for YardPulse Yard & Dock Orchestrator Agent."""
import os
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import YardDockSchedulingAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "yard_dock_scheduling_agent"
    assert len(res["systems"]) >= 4
    system_ids = [s["id"] for s in res["systems"]]
    assert "fleet_engine_yard_geofence" in system_ids
    assert "hostler_spotter_dispatch" in system_ids
    assert "dock_door_schedule_ledger" in system_ids
    assert "carrier_detention_penalty_ledger" in system_ids


def test_query_yard_trailer_geofence_status():
    res = tools.query_yard_trailer_geofence_status(trailer_id="TRL-SWIFT-7741")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["carrier_name"] == "Swift Transportation"
    assert record["dwell_time_in_yard_minutes"] == 85.0
    assert record["status"] == "AT_RISK_OF_DETENTION"


def test_query_yard_spotter_move_tasks():
    res = tools.query_yard_spotter_move_tasks(spotter_truck_id="SPOTTER-HOSTLER-03")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["target_door"] == "DOOR-CROSSDOCK-08"
    assert record["priority"] == "EXPEDITE_DETENTION_AVOIDANCE"


def test_query_dock_door_turnaround_schedules():
    res = tools.query_dock_door_turnaround_schedules(door_id="DOOR-CROSSDOCK-08")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["door_clearance_status"] == "DOOR_EMPTY_READY"
    assert record["door_status"] == "READY_FOR_DOCKING"


def test_query_carrier_detention_risk_records():
    res = tools.query_carrier_detention_risk_records(trailer_id="TRL-SWIFT-7741")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["minutes_until_penalty"] == 35.0
    assert record["projected_detention_penalty_usd"] >= 255.00


def test_quality_gate_blocks_invalid_inputs():
    agent = YardDockSchedulingAgent()
    # Missing idempotency key
    res = agent.execute_tool(
        "action_dispatch_yard_spotter_move",
        trailer_id="TRL-01",
        current_yard_slot="SLOT-01",
        target_dock_door="DOOR-01",
        spotter_truck_id="SPOTTER-01",
        priority="HIGH",
        rationale="Move test"
    )
    assert res.get("error") == "missing_idempotency_key"

    # Negative fee avoided
    res2 = agent.execute_tool(
        "action_resolve_carrier_detention_alert",
        trailer_id="TRL-01",
        carrier_id="CARRIER-01",
        turnaround_time_minutes=80.0,
        fee_avoided_usd=-50.0,
        rationale="Negative fee",
        idempotency_key="KEY-DET-01"
    )
    assert res2.get("error") == "invalid_fee_avoided_amount"


def test_end_to_end_scenario_execution():
    agent = YardDockSchedulingAgent()
    query = "Audit yard dwell times at Dallas Yard 02 via Fleet Engine geofencing, expedite trailers nearing 2-hour detention cutoff, and eliminate demurrage penalty fees."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) >= 2

    move_action = result["actions_executed"][0]
    assert move_action["status"] == "SPOTTER_MOVE_DISPATCHED"
    assert "YARD-MOVE" in move_action["move_id"]
    assert move_action["target_dock_door"] == "DOOR-CROSSDOCK-08"

    resolv_action = result["actions_executed"][1]
    assert resolv_action["status"] == "DETENTION_PENALTY_NEUTRALIZED"
    assert "DET-RESOLV" in resolv_action["resolution_id"]
    assert resolv_action["fee_avoided_usd"] >= 255.00

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) >= 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify copy-ready markdown tables
    markdown = result["markdown"]
    assert "### 🚛 YardPulse Yard Gate & Turnaround Demurrage Shield Briefing" in markdown
    assert "| Trailer ID | Carrier Name | Current Yard Slot |" in markdown
    assert "TRL-SWIFT-7741" in markdown
    assert "$255.00" in markdown
    assert "Yard Spotter Hostler Dispatched" in markdown
    assert "Carrier Detention Alert Neutralized" in markdown


if __name__ == "__main__":
    test_list_systems()
    print("✓ test_list_systems passed")
    test_query_yard_trailer_geofence_status()
    print("✓ test_query_yard_trailer_geofence_status passed")
    test_query_yard_spotter_move_tasks()
    print("✓ test_query_yard_spotter_move_tasks passed")
    test_query_dock_door_turnaround_schedules()
    print("✓ test_query_dock_door_turnaround_schedules passed")
    test_query_carrier_detention_risk_records()
    print("✓ test_query_carrier_detention_risk_records passed")
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

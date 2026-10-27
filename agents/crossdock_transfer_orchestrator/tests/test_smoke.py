"""Smoke test suite for CrossDockFlow Transfer Orchestrator Agent."""
import os
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import CrossdockTransferOrchestrator
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "crossdock_transfer_orchestrator"
    assert len(res["systems"]) >= 4
    system_ids = [s["id"] for s in res["systems"]]
    assert "manhattan_crossdock_sorter" in system_ids
    assert "carrier_milestone_edi_feed" in system_ids
    assert "outbound_retail_wave_ledger" in system_ids
    assert "pallet_flowthrough_telemetry" in system_ids


def test_query_inbound_outbound_crossdock_manifests():
    res = tools.query_inbound_outbound_crossdock_manifests(manifest_id="XDOCK-MNF-20261022-041")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["inbound_door_id"] == "DOOR-INBOUND-04"
    assert record["eligible_flowthrough_pallets"] == 18
    assert len(record["pallet_ids"]) >= 4


def test_query_inbound_carrier_eta_milestones():
    res = tools.query_inbound_carrier_eta_milestones(shipment_id="SHP-SWIFT-20261022-9921")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["carrier_id"] == "CARRIER-SWIFT-TRANS"
    assert record["assigned_inbound_door"] == "DOOR-INBOUND-04"


def test_query_outbound_trailer_bay_assignments():
    res = tools.query_outbound_trailer_bay_assignments(bay_id="BAY-OUTBOUND-12")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["destination_dc"] == "RDC-HOUSTON-05"
    assert record["available_pallet_slots"] == 10


def test_query_crossdock_dwell_time_records():
    res = tools.query_crossdock_dwell_time_records(transfer_status="DIRECT")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["dwell_time_minutes"] == 18.5
    assert record["staging_area_bypassed"] is True


def test_quality_gate_blocks_invalid_inputs():
    agent = CrossdockTransferOrchestrator()
    # Missing idempotency key
    res = agent.execute_tool(
        "action_dispatch_direct_crossdock_transfer",
        inbound_manifest_id="MNF-01",
        inbound_door_id="DOOR-01",
        outbound_bay_id="BAY-01",
        pallet_ids=["PLT-01"],
        rationale="Transfer test"
    )
    assert res.get("error") == "missing_idempotency_key"

    # Empty pallet list
    res2 = agent.execute_tool(
        "action_dispatch_direct_crossdock_transfer",
        inbound_manifest_id="MNF-01",
        inbound_door_id="DOOR-01",
        outbound_bay_id="BAY-01",
        pallet_ids=[],
        rationale="Empty list",
        idempotency_key="KEY-XDOCK-01"
    )
    assert res2.get("error") == "invalid_pallet_list"


def test_end_to_end_scenario_execution():
    agent = CrossdockTransferOrchestrator()
    query = "Synchronize inbound shipment SHP-SWIFT-20261022-9921 at Door Inbound 04, dispatch direct cross-dock transfers into outbound retail linehauls, and buffer non-immediate pallets."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) >= 2

    dispatch_action = result["actions_executed"][0]
    assert dispatch_action["status"] == "CROSSDOCK_TRANSFER_DISPATCHED"
    assert "XDOCK-TRF" in dispatch_action["transfer_dispatch_id"]
    assert dispatch_action["pallet_count"] == 4

    hold_action = result["actions_executed"][1]
    assert hold_action["status"] == "PALLET_HELD_IN_STAGING"
    assert "XDOCK-HOLD" in hold_action["hold_id"]

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) >= 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify copy-ready markdown tables
    markdown = result["markdown"]
    assert "### 🔄 CrossDockFlow Real-Time Cross-Dock & Flow-Through Briefing" in markdown
    assert "| Inbound Door | Outbound Bay | Destination Route |" in markdown
    assert "DOOR-04" in markdown
    assert "18.5 min" in markdown
    assert "Direct Cross-Dock Transfer Dispatched" in markdown
    assert "Pallet Staging Buffer Hold" in markdown


if __name__ == "__main__":
    test_list_systems()
    print("✓ test_list_systems passed")
    test_query_inbound_outbound_crossdock_manifests()
    print("✓ test_query_inbound_outbound_crossdock_manifests passed")
    test_query_inbound_carrier_eta_milestones()
    print("✓ test_query_inbound_carrier_eta_milestones passed")
    test_query_outbound_trailer_bay_assignments()
    print("✓ test_query_outbound_trailer_bay_assignments passed")
    test_query_crossdock_dwell_time_records()
    print("✓ test_query_crossdock_dwell_time_records passed")
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

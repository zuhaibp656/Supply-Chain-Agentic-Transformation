"""Smoke test suite for SlotMaster Warehouse Slotting Optimizer Agent."""
import os
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import WarehouseSlottingOptimizer
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "warehouse_slotting_optimizer"
    assert len(res["systems"]) >= 4
    system_ids = [s["id"] for s in res["systems"]]
    assert "manhattan_active_wms_slotting" in system_ids
    assert "kion_amr_fleet_manager" in system_ids
    assert "wms_wave_release_engine" in system_ids
    assert "ergonomic_pick_face_ledger" in system_ids


def test_query_warehouse_slotting_velocity_tiers():
    res = tools.query_warehouse_slotting_velocity_tiers(velocity_tier="FAST_MOVER")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["sku_id"] == "SKU-BEV-OATMILK-ORIGINAL-1L"
    assert record["daily_travel_saving_km"] == 100.8
    assert record["recommended_distance_m"] >= 22.0


def test_query_amr_picker_travel_telemetry():
    res = tools.query_amr_picker_travel_telemetry(dc_id="RDC-DALLAS-02")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["amr_id"] == "AMR-KION-BOT-07"
    assert record["travel_time_pct"] == 68.2


def test_query_wave_release_order_allocations():
    res = tools.query_wave_release_order_allocations(dc_id="RDC-DALLAS-02")
    assert res["total"] > 0
    bulk_zone = [r for r in res["rows"] if r["zone_id"] == "ZONE-BULK-MEZZANINE"][0]
    assert bulk_zone["wave_congestion_score"] == 0.84
    assert bulk_zone["recommended_max_pickers"] == 10


def test_query_slot_reassignment_recommendations():
    res = tools.query_slot_reassignment_recommendations(sku_id="SKU-BEV-OATMILK-ORIGINAL-1L")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["current_bin_id"] == "BIN-AISLE-14-SHELF-04-HIGH"
    assert record["recommended_bin_id"] == "BIN-AISLE-02-SHELF-02-GOLDEN"
    assert record["estimated_picker_travel_reduction_pct"] == 84.5


def test_quality_gate_blocks_invalid_inputs():
    agent = WarehouseSlottingOptimizer()
    # Missing idempotency key
    res = agent.execute_tool(
        "action_execute_slot_reassignment",
        sku_id="SKU-01",
        current_bin_id="BIN-A",
        target_bin_id="BIN-B",
        priority="HIGH",
        rationale="Move test"
    )
    assert res.get("error") == "missing_idempotency_key"

    # Non-positive picker limit
    res2 = agent.execute_tool(
        "action_balance_wave_release_profile",
        wave_id="WAVE-01",
        zone_id="ZONE-01",
        max_concurrent_pickers=-5,
        release_status="THROTTLED",
        rationale="Bad limit",
        idempotency_key="KEY-WAVE-01"
    )
    assert res2.get("error") == "invalid_picker_limit"


def test_end_to_end_scenario_execution():
    agent = WarehouseSlottingOptimizer()
    query = "Audit 3D warehouse slotting for fast-moving beverage SKUs at RDC Dallas, eliminate excessive picker travel, and rebalance congested wave release profiles."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) >= 2

    move_action = result["actions_executed"][0]
    assert move_action["status"] == "RELOCATION_TASK_DISPATCHED"
    assert "SLOT-RELOC" in move_action["relocation_task_id"]
    assert move_action["target_bin_id"] == "BIN-AISLE-02-SHELF-02-GOLDEN"

    wave_action = result["actions_executed"][1]
    assert wave_action["status"] == "WAVE_PROFILE_REBALANCED"
    assert "WAVE-THROT" in wave_action["wave_throttle_id"]
    assert wave_action["max_concurrent_pickers"] == 10

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) >= 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify copy-ready markdown tables
    markdown = result["markdown"]
    assert "### 🏗️ SlotMaster 3D Warehouse Velocity Slotting & Wave Optimization Briefing" in markdown
    assert "| Product SKU | Velocity Class | Current Bin Location |" in markdown
    assert "SKU-BEV-OATMILK-1L" in markdown
    assert "100.8 km/day" in markdown
    assert "WMS Stock Relocation Task Dispatched" in markdown
    assert "Wave Release Profile Rebalanced" in markdown


if __name__ == "__main__":
    test_list_systems()
    print("✓ test_list_systems passed")
    test_query_warehouse_slotting_velocity_tiers()
    print("✓ test_query_warehouse_slotting_velocity_tiers passed")
    test_query_amr_picker_travel_telemetry()
    print("✓ test_query_amr_picker_travel_telemetry passed")
    test_query_wave_release_order_allocations()
    print("✓ test_query_wave_release_order_allocations passed")
    test_query_slot_reassignment_recommendations()
    print("✓ test_query_slot_reassignment_recommendations passed")
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

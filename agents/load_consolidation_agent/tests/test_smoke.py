"""Smoke test suite for CubeMaster 3D — Isometric LIFO Bay & Load Consolidation Studio (load_consolidation_agent)."""
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import LoadConsolidationAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "load_consolidation_agent"
    assert len(res["systems"]) >= 4

def test_query_outbound_shipment_carton_dimensions():
    res = tools.query_outbound_shipment_carton_dimensions(shipment_wave_id="WAVE-3D-20261022-09")
    assert res["total"] > 0
    assert res["table"] == "outbound_shipment_carton_dimensions"
    assert len(res["rows"]) >= 1


def test_query_trailer_bay_geometry_specs():
    res = tools.query_trailer_bay_geometry_specs(trailer_type_id="TRL-53FT-DRYVAN")
    assert res["total"] > 0
    assert res["table"] == "trailer_bay_geometry_specs"
    assert len(res["rows"]) >= 1


def test_query_lifo_3d_voxel_load_plans():
    res = tools.query_lifo_3d_voxel_load_plans(load_plan_id="LP-3D-20261022-88")
    assert res["total"] > 0
    assert res["table"] == "lifo_3d_voxel_load_plans"
    assert len(res["rows"]) >= 1


def test_query_axle_weight_crush_audit_logs():
    res = tools.query_axle_weight_crush_audit_logs(load_plan_id="LP-3D-20261022-88")
    assert res["total"] > 0
    assert res["table"] == "axle_weight_crush_audit_logs"
    assert len(res["rows"]) >= 1


def test_quality_gate_blocks_invalid_inputs():
    agent = LoadConsolidationAgent()
    # 1. Missing idempotency_key
    res = agent.execute_tool(
        "action_commit_3d_lifo_load_plan",
        load_plan_id='LP-3D-20261022-88',
        trailer_type_id='TRL-53FT-DRYVAN',
        cube_utilization_pct=92.4,
        lifo_zones=['STOP_3_NOSE_ZONE_A', 'STOP_2_MID_ZONE_B', 'STOP_1_TAIL_ZONE_C'],
        rationale='Packed 53ft trailer to 92.4% cube utilization in strict reverse-stop LIFO order (Stop 3 nose ➔ Stop 2 mid ➔ Stop 1 tail door) with zero crush violations and DOT-legal axle balance.'
    )
    assert res.get("error") == "missing_idempotency_key"

    # 2. Missing required input fields
    res2 = agent.execute_tool(
        "action_commit_3d_lifo_load_plan",
        idempotency_key="TEST-KEY-01"
    )
    assert res2.get("error") == "missing_required_inputs"


def test_end_to_end_scenario_execution():
    agent = LoadConsolidationAgent()
    result = agent.run_scenario("Execute end-to-end optimization and action write-back.")
    assert result["status"] == "success"
    assert result["agent"] == "load_consolidation_agent"
    assert result["findings_count"] == 4
    assert len(result["actions_executed"]) == 2
    assert result["actions_executed"][0]["status"] == "LOAD_PLAN_3D_COMMITTED"
    assert result["actions_executed"][1]["status"] == "DOCK_STAGING_RESEQUENCED"

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
    test_query_outbound_shipment_carton_dimensions()
    print('✓ test_query_outbound_shipment_carton_dimensions passed')
    test_query_trailer_bay_geometry_specs()
    print('✓ test_query_trailer_bay_geometry_specs passed')
    test_query_lifo_3d_voxel_load_plans()
    print('✓ test_query_lifo_3d_voxel_load_plans passed')
    test_query_axle_weight_crush_audit_logs()
    print('✓ test_query_axle_weight_crush_audit_logs passed')
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

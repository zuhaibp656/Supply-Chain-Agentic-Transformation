"""Smoke test suite for AeroFreight — Air Cargo Charter, Belly Allocation & 3D ULD Contour Optimizer (air_cargo_uld_optimizer)."""
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import AirCargoUldOptimizer
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "air_cargo_uld_optimizer"
    assert len(res["systems"]) >= 4

def test_query_air_freight_priority_shipments():
    res = tools.query_air_freight_priority_shipments(awb_id="AWB-020-88419201")
    assert res["total"] > 0
    assert res["table"] == "air_freight_priority_shipments"
    assert len(res["rows"]) >= 1


def test_query_uld_contour_geometry_specs():
    res = tools.query_uld_contour_geometry_specs(uld_type="PMC_LOWER_DECK_CONTOUR")
    assert res["total"] > 0
    assert res["table"] == "uld_contour_geometry_specs"
    assert len(res["rows"]) >= 1


def test_query_uld_3d_packing_manifests():
    res = tools.query_uld_3d_packing_manifests(uld_manifest_id="ULD-MNF-FRA-ORD-01")
    assert res["total"] > 0
    assert res["table"] == "uld_3d_packing_manifests"
    assert len(res["rows"]) >= 1


def test_query_flightaware_adsb_belly_capacity():
    res = tools.query_flightaware_adsb_belly_capacity(flight_number="LH430")
    assert res["total"] > 0
    assert res["table"] == "flightaware_adsb_belly_capacity"
    assert len(res["rows"]) >= 1


def test_quality_gate_blocks_invalid_inputs():
    agent = AirCargoUldOptimizer()
    # 1. Missing idempotency_key
    res = agent.execute_tool(
        "action_release_3d_uld_buildup_manifest",
        uld_manifest_id='ULD-MNF-FRA-ORD-01',
        uld_type='PMC_LOWER_DECK_CONTOUR',
        awb_id='AWB-020-88419201',
        volumetric_efficiency_pct=89.6,
        rationale='3D contoured PMC build-up nests high-density cartons along lower-deck fuselage bevels, achieving 89.6% volumetric fill and saving 1,140 kg of chargeable dimensional weight ($4,788).'
    )
    assert res.get("error") == "missing_idempotency_key"

    # 2. Missing required input fields
    res2 = agent.execute_tool(
        "action_release_3d_uld_buildup_manifest",
        idempotency_key="TEST-KEY-01"
    )
    assert res2.get("error") == "missing_required_inputs"


def test_end_to_end_scenario_execution():
    agent = AirCargoUldOptimizer()
    result = agent.run_scenario("Execute end-to-end optimization and action write-back.")
    assert result["status"] == "success"
    assert result["agent"] == "air_cargo_uld_optimizer"
    assert result["findings_count"] == 4
    assert len(result["actions_executed"]) >= 2
    assert result["actions_executed"][0]["status"] == "ULD_3D_MANIFEST_RELEASED"
    assert result["actions_executed"][1]["status"] == "AIR_CAPACITY_ALLOTMENT_LOCKED"

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
    test_query_air_freight_priority_shipments()
    print('✓ test_query_air_freight_priority_shipments passed')
    test_query_uld_contour_geometry_specs()
    print('✓ test_query_uld_contour_geometry_specs passed')
    test_query_uld_3d_packing_manifests()
    print('✓ test_query_uld_3d_packing_manifests passed')
    test_query_flightaware_adsb_belly_capacity()
    print('✓ test_query_flightaware_adsb_belly_capacity passed')
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

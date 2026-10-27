"""Smoke test suite for ModalShift — Factory→Ship→Air→Rail→Truck Dynamic Mode-Switch Broker (multimodal_mode_shift_agent)."""
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import MultimodalModeShiftAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "multimodal_mode_shift_agent"
    assert len(res["systems"]) >= 4

def test_query_factory_gate_outbound_pos():
    res = tools.query_factory_gate_outbound_pos(po_id="PO-FAC-VN-88210")
    assert res["total"] > 0
    assert res["table"] == "factory_gate_outbound_pos"
    assert len(res["rows"]) >= 1


def test_query_multimodal_corridor_rate_tariff_matrix():
    res = tools.query_multimodal_corridor_rate_tariff_matrix(mode_code="SEA_AIR_DXB_HYBRID")
    assert res["total"] > 0
    assert res["table"] == "multimodal_corridor_rate_tariff_matrix"
    assert len(res["rows"]) >= 1


def test_query_dynamic_mode_split_recommendations():
    res = tools.query_dynamic_mode_split_recommendations(po_id="PO-FAC-VN-88210")
    assert res["total"] > 0
    assert res["table"] == "dynamic_mode_split_recommendations"
    assert len(res["rows"]) >= 1


def test_query_in_transit_mode_diversion_triggers():
    res = tools.query_in_transit_mode_diversion_triggers(transship_hub="DXB_JEBEL_ALI_DWC")
    assert res["total"] > 0
    assert res["table"] == "in_transit_mode_diversion_triggers"
    assert len(res["rows"]) >= 1


def test_quality_gate_blocks_invalid_inputs():
    agent = MultimodalModeShiftAgent()
    # 1. Missing idempotency_key
    res = agent.execute_tool(
        "action_execute_dynamic_mode_split_booking",
        po_id='PO-FAC-VN-88210',
        primary_mode='OCEAN_FCL_SUEZ',
        primary_units=17000,
        expedite_mode='SEA_AIR_DXB_HYBRID',
        expedite_units=3000,
        rationale='Splitting PO-FAC-VN-88210 into 85% Ocean FCL (17,000 units) + 15% Dubai Sea-Air bridge (3,000 units) bridges the 9-day Rotterdam stockout gap while saving $93,225 vs. full air expedite.'
    )
    assert res.get("error") == "missing_idempotency_key"

    # 2. Missing required input fields
    res2 = agent.execute_tool(
        "action_execute_dynamic_mode_split_booking",
        idempotency_key="TEST-KEY-01"
    )
    assert res2.get("error") == "missing_required_inputs"


def test_end_to_end_scenario_execution():
    agent = MultimodalModeShiftAgent()
    result = agent.run_scenario("Execute end-to-end optimization and action write-back.")
    assert result["status"] == "success"
    assert result["agent"] == "multimodal_mode_shift_agent"
    assert result["findings_count"] == 4
    assert len(result["actions_executed"]) >= 2
    assert result["actions_executed"][0]["status"] == "DYNAMIC_MODE_SPLIT_BOOKED"
    assert result["actions_executed"][1]["status"] == "MID_ROUTE_SEA_AIR_UPGRADED"

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
    test_query_factory_gate_outbound_pos()
    print('✓ test_query_factory_gate_outbound_pos passed')
    test_query_multimodal_corridor_rate_tariff_matrix()
    print('✓ test_query_multimodal_corridor_rate_tariff_matrix passed')
    test_query_dynamic_mode_split_recommendations()
    print('✓ test_query_dynamic_mode_split_recommendations passed')
    test_query_in_transit_mode_diversion_triggers()
    print('✓ test_query_in_transit_mode_diversion_triggers passed')
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

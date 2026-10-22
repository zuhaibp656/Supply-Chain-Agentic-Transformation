"""Smoke test suite for IntermodalSync — Factory-to-DC Intermodal Rail, Barge & Linehaul Orchestrator (intermodal_rail_linehaul_agent)."""
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import IntermodalRailLinehaulAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "intermodal_rail_linehaul_agent"
    assert len(res["systems"]) >= 4

def test_query_intermodal_corridor_shipments():
    res = tools.query_intermodal_corridor_shipments(shipment_id="SHP-IM-LA-CHI-701")
    assert res["total"] > 0
    assert res["table"] == "intermodal_corridor_shipments"
    assert len(res["rows"]) >= 1


def test_query_railinc_edi417_train_consists():
    res = tools.query_railinc_edi417_train_consists(train_id="BNSF-Q-LACCHI-22")
    assert res["total"] > 0
    assert res["table"] == "railinc_edi417_train_consists"
    assert len(res["rows"]) >= 1


def test_query_rail_ramp_cutoff_and_drayage():
    res = tools.query_rail_ramp_cutoff_and_drayage(ramp_id="LPC_JOLIET_CHI")
    assert res["total"] > 0
    assert res["table"] == "rail_ramp_cutoff_and_drayage"
    assert len(res["rows"]) >= 1


def test_query_otr_to_rail_mode_conversion_ledger():
    res = tools.query_otr_to_rail_mode_conversion_ledger(corridor_lane="LAX_TO_JOLIET_CHI")
    assert res["total"] > 0
    assert res["table"] == "otr_to_rail_mode_conversion_ledger"
    assert len(res["rows"]) >= 1


def test_quality_gate_blocks_invalid_inputs():
    agent = IntermodalRailLinehaulAgent()
    # 1. Missing idempotency_key
    res = agent.execute_tool(
        "action_tender_edi404_rail_intermodal_bill",
        shipment_id='SHP-IM-LA-CHI-701',
        rail_carrier='BNSF_RAILWAY',
        train_id='BNSF-Q-LACCHI-22',
        origin_ramp='HOBART_LAX',
        dest_ramp='LPC_JOLIET_CHI',
        rationale='Chicago Joliet RDC has 14.5 days of supply buffer; converting 2,015-mile linehaul from OTR truck to BNSF double-stack COFC rail saves $1,760 (-37.8%) and cuts Scope-3 CO2e by 68.4%.'
    )
    assert res.get("error") == "missing_idempotency_key"

    # 2. Missing required input fields
    res2 = agent.execute_tool(
        "action_tender_edi404_rail_intermodal_bill",
        idempotency_key="TEST-KEY-01"
    )
    assert res2.get("error") == "missing_required_inputs"


def test_end_to_end_scenario_execution():
    agent = IntermodalRailLinehaulAgent()
    result = agent.run_scenario("Execute end-to-end optimization and action write-back.")
    assert result["status"] == "success"
    assert result["agent"] == "intermodal_rail_linehaul_agent"
    assert result["findings_count"] == 4
    assert len(result["actions_executed"]) == 2
    assert result["actions_executed"][0]["status"] == "EDI404_RAIL_TENDER_ACCEPTED"
    assert result["actions_executed"][1]["status"] == "RAMP_CRANE_DRAYAGE_SYNCHRONIZED"

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
    test_query_intermodal_corridor_shipments()
    print('✓ test_query_intermodal_corridor_shipments passed')
    test_query_railinc_edi417_train_consists()
    print('✓ test_query_railinc_edi417_train_consists passed')
    test_query_rail_ramp_cutoff_and_drayage()
    print('✓ test_query_rail_ramp_cutoff_and_drayage passed')
    test_query_otr_to_rail_mode_conversion_ledger()
    print('✓ test_query_otr_to_rail_mode_conversion_ledger passed')
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

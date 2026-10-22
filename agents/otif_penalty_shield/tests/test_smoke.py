"""Smoke test suite for OTIFShield — Customer SLA Rescue & Chargeback Dispute Agent (otif_penalty_shield)."""
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import OtifPenaltyShield
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "otif_penalty_shield"
    assert len(res["systems"]) >= 4

def test_query_open_retail_customer_orders_sla():
    res = tools.query_open_retail_customer_orders_sla(order_id="SO-WMT-20261022-881")
    assert res["total"] > 0
    assert res["table"] == "open_retail_customer_orders_sla"
    assert len(res["rows"]) >= 1


def test_query_predicted_otif_breach_alerts():
    res = tools.query_predicted_otif_breach_alerts(order_id="SO-WMT-20261022-881")
    assert res["total"] > 0
    assert res["table"] == "predicted_otif_breach_alerts"
    assert len(res["rows"]) >= 1


def test_query_retailer_otif_chargeback_deductions():
    res = tools.query_retailer_otif_chargeback_deductions(deduction_id="DED-RET01-44910")
    assert res["total"] > 0
    assert res["table"] == "retailer_otif_chargeback_deductions"
    assert len(res["rows"]) >= 1


def test_query_geofence_edi856_dispute_dossiers():
    res = tools.query_geofence_edi856_dispute_dossiers(deduction_id="DED-RET01-44910")
    assert res["total"] > 0
    assert res["table"] == "geofence_edi856_dispute_dossiers"
    assert len(res["rows"]) >= 1


def test_quality_gate_blocks_invalid_inputs():
    agent = OtifPenaltyShield()
    # 1. Missing idempotency_key
    res = agent.execute_tool(
        "action_execute_otif_sla_rescue_intervention",
        order_id='SO-WMT-20261022-881',
        customer_id='BIGBOX-RETAIL-01',
        rescue_option='PRIORITY_DOCK_RELEASE_AND_TEAM_DRIVER',
        penalty_avoided_usd=12600.0,
        rationale='Predicted 78% MABD breach risk 72 hours early; spent $650 on priority dock wave release to avoid a $12,600 (3% COGS) retail OTIF chargeback.'
    )
    assert res.get("error") == "missing_idempotency_key"

    # 2. Missing required input fields
    res2 = agent.execute_tool(
        "action_execute_otif_sla_rescue_intervention",
        idempotency_key="TEST-KEY-01"
    )
    assert res2.get("error") == "missing_required_inputs"


def test_end_to_end_scenario_execution():
    agent = OtifPenaltyShield()
    result = agent.run_scenario("Execute end-to-end optimization and action write-back.")
    assert result["status"] == "success"
    assert result["agent"] == "otif_penalty_shield"
    assert result["findings_count"] == 4
    assert len(result["actions_executed"]) == 2
    assert result["actions_executed"][0]["status"] == "OTIF_SLA_RESCUE_EXECUTED"
    assert result["actions_executed"][1]["status"] == "CHARGEBACK_DISPUTE_SUBMITTED"

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
    test_query_open_retail_customer_orders_sla()
    print('✓ test_query_open_retail_customer_orders_sla passed')
    test_query_predicted_otif_breach_alerts()
    print('✓ test_query_predicted_otif_breach_alerts passed')
    test_query_retailer_otif_chargeback_deductions()
    print('✓ test_query_retailer_otif_chargeback_deductions passed')
    test_query_geofence_edi856_dispute_dossiers()
    print('✓ test_query_geofence_edi856_dispute_dossiers passed')
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

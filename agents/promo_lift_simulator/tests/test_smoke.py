"""Smoke test suite for ElasticityIQ Promo Simulator."""
import os
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import PromoLiftSimulatorAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "promo_lift_simulator"
    assert len(res["systems"]) >= 4
    system_ids = [s["id"] for s in res["systems"]]
    assert "sap_tpm_salesforce" in system_ids
    assert "bigquery_ml_causal" in system_ids
    assert "alloydb_stock_buffer" in system_ids


def test_query_planned_promo_campaigns():
    res = tools.query_planned_promo_campaigns(campaign_id="CMP-202611-BOGO")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["retailer"] == "Walmart"
    assert record["trade_spend_usd"] > 50000


def test_query_causal_promo_elasticity():
    res = tools.query_causal_promo_elasticity(sku_id="SKU-BEV-ISOTONIC-32OZ")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["price_elasticity"] < -1.0
    assert record["net_incremental_units"] > 0
    assert record["double_ml_confidence_pvalue"] < 0.05


def test_query_cross_sku_cannibalization():
    res = tools.query_cross_sku_cannibalization(promoted_sku="SKU-BEV-ISOTONIC-32OZ")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["volume_diverted_units"] > 0
    assert record["total_cannibalization_loss_usd"] > 10000


def test_query_warehouse_promo_availability():
    res = tools.query_warehouse_promo_availability(sku_id="SKU-BEV-ISOTONIC-32OZ")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["available_to_promise_units"] > 0
    assert "RISK" in record["post_promo_stockout_risk"]


def test_quality_gate_blocks_excessive_trade_spend():
    agent = PromoLiftSimulatorAgent()
    # Missing idempotency key
    res = agent.execute_tool(
        "action_lock_tpm_calendar",
        campaign_id="CMP-TEST",
        locked_net_lift_units=10000,
        committed_trade_spend_usd=50000.0,
        rationale="Test spend"
    )
    assert res.get("error") == "missing_idempotency_key"

    # Exceeds delegation threshold ($250k)
    res2 = agent.execute_tool(
        "action_lock_tpm_calendar",
        campaign_id="CMP-TEST",
        locked_net_lift_units=10000,
        committed_trade_spend_usd=350000.0,
        rationale="Over budget spend",
        idempotency_key="TEST-KEY-003"
    )
    assert res2.get("error") == "trade_spend_exceeds_delegation_authority"


def test_end_to_end_scenario_execution():
    agent = PromoLiftSimulatorAgent()
    query = "Simulate BOGO Hydration Blitz, isolate cannibalization, check DC stock, and reshape promo mechanic."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) == 2

    shape_action = result["actions_executed"][0]
    assert shape_action["status"] == "PROMO_MECHANIC_RESHAPED"
    assert "PROMO-SHAPE" in shape_action["shape_id"]
    assert shape_action["adjusted_discount_pct"] == 20.0

    lock_action = result["actions_executed"][1]
    assert lock_action["status"] == "TPM_CALENDAR_LOCKED_ACTIVE"
    assert "TPM-LOCK" in lock_action["lock_id"]
    assert lock_action["locked_net_lift_units"] == 48000

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) == 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify deterministic copy-ready table and markdown structure
    assert "markdown" in result
    assert "| Campaign Name |" in result["markdown"]
    assert "### 🎯 ElasticityIQ Demand Shaping" in result["markdown"]
    assert "### 🔗 Connected Systems" in result["markdown"]


if __name__ == "__main__":
    print("Running ElasticityIQ Promo Simulator smoke tests...")
    test_list_systems()
    test_query_planned_promo_campaigns()
    test_query_causal_promo_elasticity()
    test_query_cross_sku_cannibalization()
    test_query_warehouse_promo_availability()
    test_quality_gate_blocks_excessive_trade_spend()
    test_end_to_end_scenario_execution()
    print("✅ All 7 ElasticityIQ Promo Simulator smoke tests passed successfully!")

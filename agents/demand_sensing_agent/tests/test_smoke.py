"""Smoke test suite for PulseCast Demand Sensing Engine."""
import os
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import DemandSensingAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "demand_sensing_agent"
    assert len(res["systems"]) >= 4
    system_ids = [s["id"] for s in res["systems"]]
    assert "bigquery_demand_lake" in system_ids
    assert "vertex_ai_timesfm" in system_ids
    assert "sap_ibp_supply" in system_ids


def test_query_pos_store_scans():
    res = tools.query_pos_store_scans(stockout_only=True)
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["stockout_flag"] is True
    assert record["censored_demand_imputed_units"] > record["daily_scan_units"]


def test_query_external_demand_signals():
    res = tools.query_external_demand_signals(event_type="HEATWAVE")
    assert res["total"] > 0
    signal = res["rows"][0]
    assert "WeatherNext" in signal["provider"]
    assert signal["projected_category_surge_pct"] > 20.0


def test_query_timesfm_forecast_horizons():
    res = tools.query_timesfm_forecast_horizons(sku_id="SKU-BEV-ISOTONIC-32OZ")
    assert res["total"] > 0
    fc = res["rows"][0]
    assert fc["p10_units"] < fc["p50_units"] < fc["p90_units"]
    assert fc["wape_pct"] <= 6.0


def test_query_fva_sales_bias():
    res = tools.query_fva_sales_bias(bias_type="OPTIMISM")
    assert res["total"] > 0
    bias = res["rows"][0]
    assert bias["historical_fva_pct"] < 0
    assert "CHRONIC_OPTIMISM" in bias["bias_classification"]


def test_quality_gate_blocks_invalid_mutation():
    agent = DemandSensingAgent()
    # Missing idempotency key
    res = agent.execute_tool(
        "action_commit_ibp_pir_change",
        sku_id="SKU-TEST",
        plant_or_region="US-CENTRAL",
        target_key_figure="PIR_CONSENSUS",
        adjusted_pir_units=1000,
        rationale="Test writeback"
    )
    assert res.get("error") == "missing_idempotency_key"

    # Invalid units <= 0
    res2 = agent.execute_tool(
        "action_commit_ibp_pir_change",
        sku_id="SKU-TEST",
        plant_or_region="US-CENTRAL",
        target_key_figure="PIR_CONSENSUS",
        adjusted_pir_units=-500,
        rationale="Negative units",
        idempotency_key="TEST-002"
    )
    assert res2.get("error") == "invalid_pir_units"


def test_end_to_end_scenario_execution():
    agent = DemandSensingAgent()
    query = "Detect heatwave surge in US-Central, impute Kroger stockouts, and commit TimesFM P50 forecast to SAP IBP."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) >= 2

    dampen_action = result["actions_executed"][0]
    assert dampen_action["status"] == "BIAS_DAMPENED_APPLIED"
    assert "FVA-DAMPEN" in dampen_action["dampen_id"]

    ibp_action = result["actions_executed"][1]
    assert ibp_action["status"] == "IBP_COMMITTED_SUCCESS"
    assert "IBP-PIR" in ibp_action["writeback_id"]
    assert ibp_action["adjusted_pir_units"] >= 298000

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) >= 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify deterministic copy-ready table and markdown structure
    assert "markdown" in result
    assert "| SKU ID |" in result["markdown"]
    assert "### 🌊 PulseCast Demand Sensing" in result["markdown"]
    assert "### 🔗 Connected Systems" in result["markdown"]


if __name__ == "__main__":
    print("Running PulseCast Demand Sensing smoke tests...")
    test_list_systems()
    test_query_pos_store_scans()
    test_query_external_demand_signals()
    test_query_timesfm_forecast_horizons()
    test_query_fva_sales_bias()
    test_quality_gate_blocks_invalid_mutation()
    test_end_to_end_scenario_execution()
    print("✅ All 7 PulseCast Demand Sensing smoke tests passed successfully!")

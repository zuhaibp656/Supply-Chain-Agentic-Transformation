"""Smoke test suite for EchelonFlow MEIO Allocator Agent."""
import os
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import EchelonInventoryAllocator
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "echelon_inventory_allocator"
    assert len(res["systems"]) >= 4
    system_ids = [s["id"] for s in res["systems"]]
    assert "sap_ibp_meio_engine" in system_ids
    assert "manhattan_wms_dc_inventory" in system_ids
    assert "lateral_transshipment_service" in system_ids
    assert "stockout_risk_predictor" in system_ids


def test_query_multi_echelon_safety_stock_recommendations():
    res = tools.query_multi_echelon_safety_stock_recommendations(sku_id="SKU-BEV-OATMILK-ORIGINAL-1L")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["echelon_tier"] == "TIER_1_CENTRAL_DC"
    assert record["working_capital_freed_usd"] == 38480.00
    assert record["recommended_safety_stock_units"] == 32000


def test_query_dc_inventory_echelon_balances():
    res = tools.query_dc_inventory_echelon_balances(sku_id="SKU-BEV-OATMILK-ORIGINAL-1L")
    assert res["total"] > 0
    dallas = [r for r in res["rows"] if r["dc_id"] == "RDC-DALLAS-02"][0]
    assert dallas["days_of_supply"] == 3.8
    assert dallas["inventory_status"] == "STOCKOUT_ALERT_IMMINENT"


def test_query_lateral_dc_rebalance_transfers():
    res = tools.query_lateral_dc_rebalance_transfers(destination_dc_id="RDC-DALLAS-02")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["source_dc_id"] == "CDC-CHICAGO-01"
    assert record["quantity_transferred_units"] == 6500
    assert record["net_roi_ratio"] == 13.0


def test_query_echelon_service_level_projections():
    res = tools.query_echelon_service_level_projections(network_node_id="RDC-DALLAS-02")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["stockout_probability_without_rebalance_pct"] == 34.2
    assert record["projected_service_level_pct"] == 98.6


def test_quality_gate_blocks_invalid_inputs():
    agent = EchelonInventoryAllocator()
    # Missing idempotency key
    res = agent.execute_tool(
        "action_execute_lateral_dc_rebalance",
        source_dc_id="CDC-01",
        destination_dc_id="RDC-02",
        sku_id="SKU-01",
        transfer_quantity=5000,
        rationale="Emergency transfer"
    )
    assert res.get("error") == "missing_idempotency_key"

    # Non-positive transfer quantity
    res2 = agent.execute_tool(
        "action_execute_lateral_dc_rebalance",
        source_dc_id="CDC-01",
        destination_dc_id="RDC-02",
        sku_id="SKU-01",
        transfer_quantity=-100,
        rationale="Negative qty",
        idempotency_key="KEY-REBAL-01"
    )
    assert res2.get("error") == "invalid_transfer_quantity"


def test_end_to_end_scenario_execution():
    agent = EchelonInventoryAllocator()
    query = "Audit multi-echelon inventory positions for SKU-BEV-OATMILK-ORIGINAL-1L, resolve downstream stockout risk at RDC Dallas via lateral transshipment, and update SAP IBP safety stock parameters."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) == 2

    rebal_action = result["actions_executed"][0]
    assert rebal_action["status"] == "LATERAL_REBALANCE_DISPATCHED"
    assert "REBAL-TRF" in rebal_action["rebalance_transfer_id"]
    assert rebal_action["transfer_quantity_units"] == 6500

    policy_action = result["actions_executed"][1]
    assert policy_action["status"] == "MEIO_SAFETY_STOCK_POLICY_UPDATED"
    assert "MEIO-POL" in policy_action["policy_update_id"]
    assert policy_action["new_safety_stock_units"] == 32000

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) == 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify copy-ready markdown tables
    markdown = result["markdown"]
    assert "### 📦 EchelonFlow Multi-Echelon Inventory Optimization (MEIO) Briefing" in markdown
    assert "| Echelon Node | Node Tier | On-Hand Stock |" in markdown
    assert "CDC-CHICAGO-01" in markdown
    assert "RDC-DALLAS-02" in markdown
    assert "Lateral Transshipment Dispatched" in markdown
    assert "SAP IBP Safety Stock Policy Updated" in markdown


if __name__ == "__main__":
    test_list_systems()
    print("✓ test_list_systems passed")
    test_query_multi_echelon_safety_stock_recommendations()
    print("✓ test_query_multi_echelon_safety_stock_recommendations passed")
    test_query_dc_inventory_echelon_balances()
    print("✓ test_query_dc_inventory_echelon_balances passed")
    test_query_lateral_dc_rebalance_transfers()
    print("✓ test_query_lateral_dc_rebalance_transfers passed")
    test_query_echelon_service_level_projections()
    print("✓ test_query_echelon_service_level_projections passed")
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

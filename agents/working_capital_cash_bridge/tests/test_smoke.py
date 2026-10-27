"""Smoke test suite for Working Capital & Cash Conversion Bridge."""
import os
import sys
from pathlib import Path

# Add project root to sys.path
AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import WorkingCapitalCashBridgeAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "working_capital_cash_bridge"
    assert len(res["systems"]) >= 3
    system_ids = [s["id"] for s in res["systems"]]
    assert "sap_acdoca_material_ledger" in system_ids
    assert "corporate_treasury_workstation" in system_ids
    assert "supplier_ap_financing_portal" in system_ids


def test_query_working_capital_metrics():
    res = tools.query_working_capital_metrics(region="GLOBAL")
    assert res["total"] > 0
    metric = res["rows"][0]
    assert metric["region"] == "GLOBAL"
    assert metric["cash_conversion_cycle_days"] > 60.0
    assert metric["total_working_capital_trapped_usd"] > 50000000


def test_query_inventory_valuation_ledger():
    res = tools.query_inventory_valuation_ledger(valuation_area="PLANT-1010")
    assert res["total"] > 0
    ledger = res["rows"][0]
    assert "PLANT-1010" in ledger["valuation_area"]
    assert ledger["total_inventory_valuation_usd"] > 1000000


def test_query_trapped_cash_opportunities():
    res = tools.query_trapped_cash_opportunities(min_cash_freed_usd=500000.0)
    assert res["total"] > 0
    opp = res["rows"][0]
    assert opp["cash_freed_usd"] > 500000.0
    assert opp["recommended_reduction_units"] > 0


def test_query_ap_supplier_discount_invoices():
    res = tools.query_ap_supplier_discount_invoices(min_discount_usd=15000.0)
    assert res["total"] > 0
    inv = res["rows"][0]
    assert "INV-AP" in inv["invoice_id"]
    assert inv["annualized_roi_pct"] > 15.0


def test_quality_gate_blocks_invalid_cash():
    agent = WorkingCapitalCashBridgeAgent()
    res = agent.execute_tool(
        "action_rebalance_working_capital_buffer",
        target_plant="PLANT-1010",
        target_sku="MAT-880019",
        recommended_reduction_units=100,
        cash_freed_usd=-500.0,  # Invalid negative amount
        rationale="Invalid negative cash rebalance",
        idempotency_key="TEST-KEY-003"
    )
    assert res.get("error") == "invalid_cash_freed_amount"
    assert res.get("escalation") == "reject_mutation"


def test_end_to_end_scenario_execution():
    agent = WorkingCapitalCashBridgeAgent()
    query = "Scan working capital ledgers, identify trapped cash in slow-moving buffers, and capture dynamic AP discounts."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) >= 2

    rebal_action = result["actions_executed"][0]
    assert rebal_action["status"] == "rebalanced"
    assert "REBAL-WC" in rebal_action["rebal_id"]

    disc_action = result["actions_executed"][1]
    assert disc_action["status"] == "discount_captured"
    assert "DISC" in disc_action["discount_id"]

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) >= 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"
    assert "vconcat" in result["vega_spec"]

    # Verify deterministic copy-ready table and markdown structure
    assert "markdown" in result
    assert "| Plant / Valuation Area |" in result["markdown"]
    assert "### 💰 Financial Executive Briefing" in result["markdown"]
    assert "### 🔗 Connected Financial Systems" in result["markdown"]


if __name__ == "__main__":
    print("Running Working Capital & Cash Conversion Bridge smoke tests...")
    test_list_systems()
    test_query_working_capital_metrics()
    test_query_inventory_valuation_ledger()
    test_query_trapped_cash_opportunities()
    test_query_ap_supplier_discount_invoices()
    test_quality_gate_blocks_invalid_cash()
    test_end_to_end_scenario_execution()
    print("✅ All 7 Working Capital Cash Bridge smoke tests passed successfully!")

"""Smoke test suite for ChannelSync CPFR Harmonizer."""
import os
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import CpfrSyncAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "cpfr_sync_agent"
    assert len(res["systems"]) >= 4
    system_ids = [s["id"] for s in res["systems"]]
    assert "retail_edi_dataflow" in system_ids
    assert "bigquery_anomaly_vault" in system_ids
    assert "sap_ibp_cpfr" in system_ids


def test_query_retailer_edi852_pos():
    res = tools.query_retailer_edi852_pos(retailer="Kroger")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["retailer"] == "Kroger"
    assert record["store_book_inventory"] > 0
    assert record["daily_scan_units"] == 0  # Zero scans indicates potential phantom issue


def test_query_retailer_edi830_forecasts():
    res = tools.query_retailer_edi830_forecasts(retailer="Walmart")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["bullwhip_variance_ratio"] > 1.2
    assert "BULLWHIP" in record["volatility_flag"]


def test_query_phantom_inventory_anomalies():
    res = tools.query_phantom_inventory_anomalies(store_id="STORE-KROGER-ATL-209")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["consecutive_zero_scan_days"] >= 4
    assert record["phantom_confidence_score"] > 0.85
    assert record["revenue_leakage_per_day_usd"] > 1000


def test_query_joint_cpfr_packets():
    res = tools.query_joint_cpfr_packets(retailer="Walmart")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["variance_gap_units"] > 50000
    assert record["recommended_replenishment_order_units"] > 0


def test_quality_gate_blocks_out_of_bounds_replenishment():
    agent = CpfrSyncAgent()
    # Missing idempotency key
    res = agent.execute_tool(
        "action_dispatch_vmi_replenishment_order",
        retailer="Walmart",
        sku_id="SKU-TEST",
        target_dc="DC-TEST",
        order_quantity_units=5000,
        rationale="Test PO"
    )
    assert res.get("error") == "missing_idempotency_key"

    # Out of bounds quantity (>500,000)
    res2 = agent.execute_tool(
        "action_dispatch_vmi_replenishment_order",
        retailer="Walmart",
        sku_id="SKU-TEST",
        target_dc="DC-TEST",
        order_quantity_units=750000,
        rationale="Massive PO",
        idempotency_key="TEST-KEY-004"
    )
    assert res2.get("error") == "order_quantity_out_of_bounds"


def test_end_to_end_scenario_execution():
    agent = CpfrSyncAgent()
    query = "Harmonize retailer EDI 852 feeds, detect Kroger store phantom inventory stockout, dispatch audit, and trigger VMI order."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) == 2

    audit_action = result["actions_executed"][0]
    assert audit_action["status"] == "STORE_AUDIT_DISPATCHED"
    assert "AUDIT-TASK" in audit_action["audit_id"]

    vmi_action = result["actions_executed"][1]
    assert vmi_action["status"] == "VMI_PO_TRANSMITTED_EDI855"
    assert "VMI-PO" in vmi_action["po_id"]
    assert vmi_action["order_quantity_units"] == 95000

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) == 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify deterministic copy-ready table and markdown structure
    assert "markdown" in result
    assert "| Retailer |" in result["markdown"]
    assert "### 📡 ChannelSync Collaborative CPFR" in result["markdown"]
    assert "### 🔗 Connected Systems" in result["markdown"]


if __name__ == "__main__":
    print("Running ChannelSync CPFR Harmonizer smoke tests...")
    test_list_systems()
    test_query_retailer_edi852_pos()
    test_query_retailer_edi830_forecasts()
    test_query_phantom_inventory_anomalies()
    test_query_joint_cpfr_packets()
    test_quality_gate_blocks_out_of_bounds_replenishment()
    test_end_to_end_scenario_execution()
    print("✅ All 7 ChannelSync CPFR Harmonizer smoke tests passed successfully!")

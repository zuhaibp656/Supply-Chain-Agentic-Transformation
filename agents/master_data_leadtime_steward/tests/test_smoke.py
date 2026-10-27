"""Smoke test suite for Master Data & Lead-Time Steward."""
import os
import sys
from pathlib import Path

# Add project root to sys.path
AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import MasterDataLeadtimeAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "master_data_leadtime_steward"
    assert len(res["systems"]) >= 3
    system_ids = [s["id"] for s in res["systems"]]
    assert "sap_s4hana_mm" in system_ids
    assert "cubiscan_3d_telemetry" in system_ids
    assert "vendor_master_db" in system_ids


def test_query_material_master_records():
    res = tools.query_material_master_records(plant="PLANT-1010")
    assert res["total"] > 0
    mat = res["rows"][0]
    assert "MAT-" in mat["material_id"]
    assert mat["planned_delivery_time_days"] > 0


def test_query_leadtime_drift_anomalies():
    res = tools.query_leadtime_drift_anomalies(min_drift_days=10)
    assert res["total"] > 0
    item = res["rows"][0]
    assert item["leadtime_drift_days"] >= 10
    assert "Inverter" in item["description"]


def test_query_cubiscan_dimension_discrepancies():
    res = tools.query_cubiscan_dimension_discrepancies(min_volume_variance_pct=20.0)
    assert res["total"] > 0
    scan = res["rows"][0]
    assert scan["volume_discrepancy_pct"] > 50.0
    assert scan["carrier_surcharge_risk_usd"] > 0


def test_query_vendor_master_integrity():
    res = tools.query_vendor_master_integrity(vendor_id="VEND-10492")
    assert res["total"] > 0
    vendor = res["rows"][0]
    assert vendor["vendor_id"] == "VEND-10492"
    assert vendor["sanctions_screening_status"] == "CLEARED"


def test_quality_gate_blocks_excessive_leadtime():
    agent = MasterDataLeadtimeAgent()
    res = agent.execute_tool(
        "action_heal_material_leadtime",
        material_id="MAT-880019",
        plant="PLANT-1010",
        planned_delivery_leadtime_days=180,  # Exceeds 90-day threshold
        rationale="Unilateral 6-month leadtime extension",
        idempotency_key="TEST-KEY-002"
    )
    assert res.get("error") == "leadtime_exceeds_engineering_tolerance"
    assert res.get("escalation") == "request_engineering_change_order"


def test_end_to_end_scenario_execution():
    agent = MasterDataLeadtimeAgent()
    query = "Audit material master lead-time drift and 3D CubiScan volumetric discrepancies."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) >= 2

    heal_action = result["actions_executed"][0]
    assert heal_action["status"] == "healed"
    assert "HEAL-LT" in heal_action["heal_id"]

    dim_action = result["actions_executed"][1]
    assert dim_action["status"] == "remediated"
    assert "DIM-FIX" in dim_action["dim_id"]

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) >= 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"
    assert "vconcat" in result["vega_spec"]

    # Verify deterministic copy-ready table and markdown structure
    assert "markdown" in result
    assert "| Material SKU |" in result["markdown"]
    assert "### 🧹 Master Data Hygiene" in result["markdown"]
    assert "### 🔗 Connected Systems" in result["markdown"]


if __name__ == "__main__":
    print("Running Master Data & Lead-Time Steward smoke tests...")
    test_list_systems()
    test_query_material_master_records()
    test_query_leadtime_drift_anomalies()
    test_query_cubiscan_dimension_discrepancies()
    test_query_vendor_master_integrity()
    test_quality_gate_blocks_excessive_leadtime()
    test_end_to_end_scenario_execution()
    print("✅ All 7 Master Data Steward smoke tests passed successfully!")

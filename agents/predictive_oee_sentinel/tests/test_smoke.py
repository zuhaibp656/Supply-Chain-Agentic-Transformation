"""Smoke test suite for AssetGuard Plant Predictive Maintenance & OEE Agent."""
import os
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import PlantOeeMaintenanceAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "predictive_oee_sentinel"
    assert len(res["systems"]) >= 4
    system_ids = [s["id"] for s in res["systems"]]
    assert "mes_siemens_opcenter" in system_ids
    assert "osisoft_pi_historian" in system_ids
    assert "sap_pm_plant_maintenance" in system_ids
    assert "sap_mm_spare_parts" in system_ids


def test_query_plant_machine_telemetry():
    res = tools.query_plant_machine_telemetry(asset_id="ASSET-MILLING-CNC-04")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["vibration_velocity_rms_mm_s"] == 7.42
    assert record["vibration_threshold_critical_mm_s"] == 7.10
    assert record["telemetry_health_status"] == "CRITICAL_BEARING_DEGRADATION"


def test_query_oee_breakdown_metrics():
    res = tools.query_oee_breakdown_metrics(asset_id="ASSET-MILLING-CNC-04")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["availability_pct"] == 73.33
    assert record["overall_oee_pct"] == 57.08
    assert record["unplanned_downtime_min"] == 128.0


def test_query_predictive_maintenance_anomalies():
    res = tools.query_predictive_maintenance_anomalies(anomaly_id="ANOM-CNC-04-VIB-992")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["estimated_time_to_failure_hours"] == 36.0
    assert record["net_avoided_loss_usd"] == 80800.0
    assert record["severity"] == "CRITICAL_HIGH"


def test_query_spare_parts_inventory_status():
    res = tools.query_spare_parts_inventory_status(compatible_asset="ASSET-MILLING-CNC-04")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["part_number"] == "PART-SPARE-BEARING-CERAMIC-7014"
    assert record["stock_on_hand"] >= 1
    assert record["storage_bin"] == "BIN-AUSTIN-CRIB-04-A12"


def test_quality_gate_blocks_invalid_quantity():
    agent = PlantOeeMaintenanceAgent()
    # Missing idempotency key
    res = agent.execute_tool(
        "action_reserve_spare_parts",
        work_order_id="WO-001",
        part_number="PART-001",
        quantity=1,
        asset_id="ASSET-001",
        rationale="Test reserve"
    )
    assert res.get("error") == "missing_idempotency_key"

    # Non-positive quantity
    res2 = agent.execute_tool(
        "action_reserve_spare_parts",
        work_order_id="WO-001",
        part_number="PART-001",
        quantity=0,
        asset_id="ASSET-001",
        rationale="Zero quantity reserve",
        idempotency_key="TEST-KEY-009"
    )
    assert res2.get("error") == "invalid_parts_quantity"


def test_end_to_end_scenario_execution():
    agent = PlantOeeMaintenanceAgent()
    query = "Audit machine health for Milling Center ASSET-MILLING-CNC-04, analyze OEE losses, predict time to failure, dispatch preventive work order, and reserve replacement bearings."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) == 2

    wo_action = result["actions_executed"][0]
    assert wo_action["status"] == "SAP_PM_WORK_ORDER_DISPATCHED"
    assert "PM-WO" in wo_action["work_order_id"]
    assert wo_action["priority"] == "HIGH_PRIORITY"

    res_action = result["actions_executed"][1]
    assert res_action["status"] == "SAP_MM_PARTS_RESERVED"
    assert "RES-MM" in res_action["reservation_id"]
    assert res_action["quantity"] == 1

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) == 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify copy-ready markdown tables
    markdown = result["markdown"]
    assert "### ⚙️ AssetGuard Plant Predictive Maintenance & OEE Briefing" in markdown
    assert "| Asset ID | Description | Vibration RMS |" in markdown
    assert "7.42 mm/s" in markdown
    assert "$80,800.00" in markdown
    assert "SAP PM Work Order Dispatched" in markdown
    assert "SAP MM Spare Parts Reserved" in markdown


if __name__ == "__main__":
    test_list_systems()
    print("✓ test_list_systems passed")
    test_query_plant_machine_telemetry()
    print("✓ test_query_plant_machine_telemetry passed")
    test_query_oee_breakdown_metrics()
    print("✓ test_query_oee_breakdown_metrics passed")
    test_query_predictive_maintenance_anomalies()
    print("✓ test_query_predictive_maintenance_anomalies passed")
    test_query_spare_parts_inventory_status()
    print("✓ test_query_spare_parts_inventory_status passed")
    test_quality_gate_blocks_invalid_quantity()
    print("✓ test_quality_gate_blocks_invalid_quantity passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

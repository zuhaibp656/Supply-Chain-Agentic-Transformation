"""Smoke test suite for QualiShield Supplier Quality Sentinel."""
import os
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import SupplierQualitySentinelAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "supplier_quality_sentinel"
    assert len(res["systems"]) >= 4
    system_ids = [s["id"] for s in res["systems"]]
    assert "sap_qm_s4hana" in system_ids
    assert "mes_supplier_telemetry" in system_ids
    assert "trackwise_etq_capa" in system_ids
    assert "sap_fi_copq_ledger" in system_ids


def test_query_supplier_coa_inspections():
    res = tools.query_supplier_coa_inspections(inspection_lot_id="LOT-INSP-202610-8841")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["supplier_id"] == "VEND-KYOCERA-PREC-09"
    assert record["measured_thermal_conductivity_w_mk"] == 164.2
    assert record["lower_spec_limit_w_mk"] == 170.0
    assert record["inspection_disposition"] == "REJECT_OUT_OF_SPEC"


def test_query_spc_cpk_drift_metrics():
    res = tools.query_spc_cpk_drift_metrics(part_number="PART-SUBSTRATE-ALN-01")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["cpk"] == 0.54
    assert record["target_cpk"] == 1.67
    assert record["cpk_status"] == "CRITICAL_DRIFT_UNSTABLE"
    assert record["estimated_defect_ppm"] == 52600


def test_query_quality_deviation_tickets():
    res = tools.query_quality_deviation_tickets(ticket_id="NCR-202610-0914")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["severity"] == "CRITICAL_STOP_SHIP"
    assert "CAPA-8D" in record["trackwise_capa_id"]
    assert record["eight_d_status"] == "D3_CONTAINMENT_ACTIVE"


def test_query_cost_of_poor_quality_ledger():
    res = tools.query_cost_of_poor_quality_ledger(copq_id="COPQ-202610-8841")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["total_copq_amount_usd"] == 114650.0
    assert record["recovery_status"] == "PENDING_DEBIT_ISSUANCE"


def test_quality_gate_blocks_invalid_copq_amount():
    agent = SupplierQualitySentinelAgent()
    # Missing idempotency key
    res = agent.execute_tool(
        "action_trigger_8d_capa_debit",
        ticket_id="NCR-001",
        supplier_id="VEND-001",
        copq_amount_usd=50000.0,
        capa_root_cause_summary="Test root cause",
        accounting_cost_center="CC-001"
    )
    assert res.get("error") == "missing_idempotency_key"

    # Invalid non-positive amount
    res2 = agent.execute_tool(
        "action_trigger_8d_capa_debit",
        ticket_id="NCR-001",
        supplier_id="VEND-001",
        copq_amount_usd=-1200.0,
        capa_root_cause_summary="Negative amount test",
        accounting_cost_center="CC-001",
        idempotency_key="TEST-KEY-008"
    )
    assert res2.get("error") == "invalid_copq_amount"


def test_end_to_end_scenario_execution():
    agent = SupplierQualitySentinelAgent()
    query = "Audit incoming lot LOT-INSP-202610-8841 for Kyocera AlN substrates, detect Cpk drift, quarantine the lot in SAP QM, and recover COPQ costs via automated debit memo."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) == 2

    quarantine_action = result["actions_executed"][0]
    assert quarantine_action["status"] == "SAP_QM_QUARANTINED_BLOCKED"
    assert "QM-BLOCK" in quarantine_action["quarantine_id"]
    assert quarantine_action["inspection_lot_id"] == "LOT-INSP-202610-8841"

    debit_action = result["actions_executed"][1]
    assert debit_action["status"] == "SAP_FI_COPQ_DEBIT_POSTED"
    assert "COPQ-DEBIT" in debit_action["debit_id"]
    assert debit_action["copq_amount_usd"] == 114650.0

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) == 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify copy-ready markdown tables
    markdown = result["markdown"]
    assert "### 🛡️ QualiShield Predictive Supplier Quality & Non-Conformance Resolution Briefing" in markdown
    assert "| Inspection Lot | Supplier | Part Number |" in markdown
    assert "164.2 W/m·K" in markdown
    assert "$114,650.00" in markdown
    assert "SAP QM Digital Quarantine Block Activated" in markdown
    assert "SAP FI Cost of Poor Quality Debit Posted" in markdown


if __name__ == "__main__":
    test_list_systems()
    print("✓ test_list_systems passed")
    test_query_supplier_coa_inspections()
    print("✓ test_query_supplier_coa_inspections passed")
    test_query_spc_cpk_drift_metrics()
    print("✓ test_query_spc_cpk_drift_metrics passed")
    test_query_quality_deviation_tickets()
    print("✓ test_query_quality_deviation_tickets passed")
    test_query_cost_of_poor_quality_ledger()
    print("✓ test_query_cost_of_poor_quality_ledger passed")
    test_quality_gate_blocks_invalid_copq_amount()
    print("✓ test_quality_gate_blocks_invalid_copq_amount passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

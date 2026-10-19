"""Smoke test suite for ClauseGuard Contract Intelligence & Trade Compliance Agent."""
import os
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import TariffEsgAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "tariff_esg_agent"
    assert len(res["systems"]) >= 4
    system_ids = [s["id"] for s in res["systems"]]
    assert "alloydb_contract_rag" in system_ids
    assert "customs_tariff_database" in system_ids
    assert "sap_gts_compliance" in system_ids
    assert "sap_ap_finance" in system_ids


def test_query_contract_clause_obligations():
    res = tools.query_contract_clause_obligations(contract_id="MSA-BALL-2025-09")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["supplier_id"] == "VEND-BALL-CORP-101"
    assert record["rebate_percentage"] == 3.0
    assert record["threshold_volume_units"] == 40000000


def test_query_supplier_rebate_accruals():
    res = tools.query_supplier_rebate_accruals(supplier_id="VEND-BALL-CORP-101")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["status"] == "UNRECOVERED_OVERDUE"
    assert record["uncollected_cash_leakage_usd"] == 47430.0


def test_query_hs_tariff_classifications():
    res = tools.query_hs_tariff_classifications(part_number="PART-CAN-ALUM-330ML")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["ten_digit_hs_code"] == "7612.90.1065"
    assert "HQ H312891" in record["cross_ruling_reference"]
    assert record["preferential_fta_rate_pct"] == 0.0


def test_query_cross_border_duty_impact():
    res = tools.query_cross_border_duty_impact(part_number="PART-CAN-ALUM-330ML")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["fta_duty_savings_usd"] == 27645.0
    assert record["compliance_status"] == "DUTY_FREE_CLEARED"


def test_quality_gate_blocks_invalid_claim_amount():
    agent = TariffEsgAgent()
    # Missing idempotency key
    res = agent.execute_tool(
        "action_issue_supplier_rebate_debit_memo",
        accrual_id="ACC-001",
        supplier_id="VEND-001",
        claim_amount_usd=10000.0,
        contract_reference="MSA-001",
        rationale="Test debit"
    )
    assert res.get("error") == "missing_idempotency_key"

    # Invalid non-positive amount
    res2 = agent.execute_tool(
        "action_issue_supplier_rebate_debit_memo",
        accrual_id="ACC-001",
        supplier_id="VEND-001",
        claim_amount_usd=-500.0,
        contract_reference="MSA-001",
        rationale="Invalid negative debit",
        idempotency_key="TEST-KEY-007"
    )
    assert res2.get("error") == "invalid_claim_amount"


def test_end_to_end_scenario_execution():
    agent = TariffEsgAgent()
    query = "Audit contract clause obligations for Ball Corp, recover unissued volume rebates via SAP AP debit memo, and lock the 10-digit HS classification in SAP GTS."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) == 2

    debit_action = result["actions_executed"][0]
    assert debit_action["status"] == "SAP_AP_DEBIT_MEMO_POSTED"
    assert "AP-DEBIT" in debit_action["debit_id"]
    assert debit_action["claim_amount_usd"] == 47430.0

    lock_action = result["actions_executed"][1]
    assert lock_action["status"] == "SAP_GTS_HS_LOCKED"
    assert "GTS-HS" in lock_action["lock_id"]
    assert lock_action["ten_digit_hs_code"] == "7612.90.1065"

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) == 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify copy-ready markdown tables
    markdown = result["markdown"]
    assert "### ⚖️ ClauseGuard Contract Intelligence & Trade Compliance Briefing" in markdown
    assert "| Part Number | Description | 10-Digit HS Code |" in markdown
    assert "7612.90.1065" in markdown
    assert "SAP AP Supplier Rebate Debit Memo Posted" in markdown
    assert "SAP GTS 10-Digit HS Tariff Code Locked" in markdown


if __name__ == "__main__":
    test_list_systems()
    print("✓ test_list_systems passed")
    test_query_contract_clause_obligations()
    print("✓ test_query_contract_clause_obligations passed")
    test_query_supplier_rebate_accruals()
    print("✓ test_query_supplier_rebate_accruals passed")
    test_query_hs_tariff_classifications()
    print("✓ test_query_hs_tariff_classifications passed")
    test_query_cross_border_duty_impact()
    print("✓ test_query_cross_border_duty_impact passed")
    test_quality_gate_blocks_invalid_claim_amount()
    print("✓ test_quality_gate_blocks_invalid_claim_amount passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

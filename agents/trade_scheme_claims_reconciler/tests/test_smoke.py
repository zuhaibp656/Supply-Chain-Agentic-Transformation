"""Smoke test suite for SchemeGuard — Secondary Trade Payout & Claims Sentinel (trade_scheme_claims_reconciler)."""
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import TradeSchemeClaimsReconciler
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "trade_scheme_claims_reconciler"
    assert len(res["systems"]) >= 4

def test_query_active_trade_promotion_schemes():
    res = tools.query_active_trade_promotion_schemes(scheme_id="SCH-FEST-Q4-2026")
    assert res["total"] > 0
    assert res["table"] == "active_trade_promotion_schemes"
    assert len(res["rows"]) >= 1


def test_query_distributor_secondary_claim_submissions():
    res = tools.query_distributor_secondary_claim_submissions(claim_id="CLM-DIST04-9921")
    assert res["total"] > 0
    assert res["table"] == "distributor_secondary_claim_submissions"
    assert len(res["rows"]) >= 1


def test_query_claim_anomaly_audit_findings():
    res = tools.query_claim_anomaly_audit_findings(claim_id="CLM-DIST04-9921")
    assert res["total"] > 0
    assert res["table"] == "claim_anomaly_audit_findings"
    assert len(res["rows"]) >= 1


def test_query_sap_fi_credit_note_settlements():
    res = tools.query_sap_fi_credit_note_settlements(claim_id="CLM-DIST04-9921")
    assert res["total"] > 0
    assert res["table"] == "sap_fi_credit_note_settlements"
    assert len(res["rows"]) >= 1


def test_quality_gate_blocks_invalid_inputs():
    agent = TradeSchemeClaimsReconciler()
    # 1. Missing idempotency_key
    res = agent.execute_tool(
        "action_flag_phantom_invoice_for_audit_hold",
        claim_id='CLM-DIST04-9921',
        flagged_invoices=['INV-SEC-8812', 'INV-SEC-8819'],
        disallowed_amount_usd=2190.0,
        rationale='Disallowed $2,190.00 across 2 secondary invoices (post-dated outside scheme window and duplicate outlet tax ID) on claim CLM-DIST04-9921.'
    )
    assert res.get("error") == "missing_idempotency_key"

    # 2. Missing required input fields
    res2 = agent.execute_tool(
        "action_flag_phantom_invoice_for_audit_hold",
        idempotency_key="TEST-KEY-01"
    )
    assert res2.get("error") == "missing_required_inputs"


def test_end_to_end_scenario_execution():
    agent = TradeSchemeClaimsReconciler()
    result = agent.run_scenario("Execute end-to-end optimization and action write-back.")
    assert result["status"] == "success"
    assert result["agent"] == "trade_scheme_claims_reconciler"
    assert result["findings_count"] == 4
    assert len(result["actions_executed"]) == 2
    assert result["actions_executed"][0]["status"] == "ANOMALOUS_INVOICES_DISALLOWED"
    assert result["actions_executed"][1]["status"] == "SAP_FI_CREDIT_NOTE_POSTED"

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
    test_query_active_trade_promotion_schemes()
    print('✓ test_query_active_trade_promotion_schemes passed')
    test_query_distributor_secondary_claim_submissions()
    print('✓ test_query_distributor_secondary_claim_submissions passed')
    test_query_claim_anomaly_audit_findings()
    print('✓ test_query_claim_anomaly_audit_findings passed')
    test_query_sap_fi_credit_note_settlements()
    print('✓ test_query_sap_fi_credit_note_settlements passed')
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

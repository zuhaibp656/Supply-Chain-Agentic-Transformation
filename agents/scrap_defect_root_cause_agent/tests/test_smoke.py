"""Smoke test suite for YieldMax Scrap Defect Root-Cause Agent."""
import os
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import ScrapDefectRootCauseAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "scrap_defect_root_cause_agent"
    assert len(res["systems"]) >= 4
    system_ids = [s["id"] for s in res["systems"]]
    assert "mes_scrap_loss_pareto" in system_ids
    assert "batch_execution_telemetry" in system_ids
    assert "sap_co_scrap_ledger" in system_ids
    assert "scada_setpoint_bridge" in system_ids


def test_query_scrap_loss_pareto_records():
    res = tools.query_scrap_loss_pareto_records(asset_id="ASSET-INJECTION-MOLD-02")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["defect_id"] == "DEF-FLASH-IMM-02"
    assert record["scrap_rate_pct"] == 5.68
    assert record["cumulative_scrap_pct"] == 58.4


def test_query_batch_process_parameter_correlations():
    res = tools.query_batch_process_parameter_correlations(defect_id="DEF-FLASH-IMM-02")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["parameter_name"] == "Injection Holding Pressure (bar)"
    assert record["pearson_correlation_coefficient"] == 0.88
    assert record["p_value"] < 0.001


def test_query_scrap_financial_cost_ledger():
    res = tools.query_scrap_financial_cost_ledger(asset_id="ASSET-INJECTION-MOLD-02")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["scrap_quantity_pieces"] == 2210
    assert record["total_scrap_financial_loss_usd"] == 2806.70


def test_query_scada_setpoint_recommendations():
    res = tools.query_scada_setpoint_recommendations(asset_id="ASSET-INJECTION-MOLD-02")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["recipe_name"] == "TETHERED_CAP_PP_HIGH_SPEED_V4"
    assert record["projected_cost_savings_per_shift_usd"] == 2450.0


def test_quality_gate_blocks_invalid_financial_loss():
    agent = ScrapDefectRootCauseAgent()
    # Missing idempotency key
    res = agent.execute_tool(
        "action_post_scrap_variance_adjustment",
        ledger_id="LED-001",
        asset_id="ASSET-001",
        financial_loss_usd=2800.0,
        cost_center="CC-001",
        rationale="Test post"
    )
    assert res.get("error") == "missing_idempotency_key"

    # Non-positive financial loss
    res2 = agent.execute_tool(
        "action_post_scrap_variance_adjustment",
        ledger_id="LED-001",
        asset_id="ASSET-001",
        financial_loss_usd=-50.0,
        cost_center="CC-001",
        rationale="Negative loss",
        idempotency_key="TEST-KEY-011"
    )
    assert res2.get("error") == "invalid_financial_loss_amount"


def test_end_to_end_scenario_execution():
    agent = ScrapDefectRootCauseAgent()
    query = "Audit scrap loss records for Injection Mold IMM-02, identify top Pareto defect, correlate machine process parameters, execute SCADA setpoint writeback, and post scrap variance to SAP CO."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) == 2

    scada_action = result["actions_executed"][0]
    assert scada_action["status"] == "SCADA_PLC_SETPOINTS_LOCKED"
    assert "SCADA-SET" in scada_action["writeback_id"]
    assert scada_action["parameter_updates"]["injection_holding_pressure_bar"] == 820.0

    co_action = result["actions_executed"][1]
    assert co_action["status"] == "SAP_CO_VARIANCE_POSTED"
    assert "SAP-CO-SCRAP" in co_action["posting_id"]
    assert co_action["financial_loss_usd"] == 2806.70

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) == 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify copy-ready markdown tables
    markdown = result["markdown"]
    assert "### 🔬 YieldMax Yield Optimization & Scrap Defect Root-Cause Briefing" in markdown
    assert "| Defect Category | Scrap Units | Scrap Rate |" in markdown
    assert "Parting Line Flash" in markdown
    assert "$2,806.70" in markdown
    assert "SCADA PLC Setpoints Locked" in markdown
    assert "SAP CO Scrap Variance Posted" in markdown


if __name__ == "__main__":
    test_list_systems()
    print("✓ test_list_systems passed")
    test_query_scrap_loss_pareto_records()
    print("✓ test_query_scrap_loss_pareto_records passed")
    test_query_batch_process_parameter_correlations()
    print("✓ test_query_batch_process_parameter_correlations passed")
    test_query_scrap_financial_cost_ledger()
    print("✓ test_query_scrap_financial_cost_ledger passed")
    test_query_scada_setpoint_recommendations()
    print("✓ test_query_scada_setpoint_recommendations passed")
    test_quality_gate_blocks_invalid_financial_loss()
    print("✓ test_quality_gate_blocks_invalid_financial_loss passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

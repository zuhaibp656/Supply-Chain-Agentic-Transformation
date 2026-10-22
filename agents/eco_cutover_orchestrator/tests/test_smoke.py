"""Smoke test suite for ChangeSync — Engineering Change (ECO) & NPI Cutover Orchestrator (eco_cutover_orchestrator)."""
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import EcoCutoverOrchestrator
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "eco_cutover_orchestrator"
    assert len(res["systems"]) >= 4

def test_query_plm_engineering_change_orders():
    res = tools.query_plm_engineering_change_orders(eco_id="ECO-2026-8841")
    assert res["total"] > 0
    assert res["table"] == "plm_engineering_change_orders"
    assert len(res["rows"]) >= 1


def test_query_multi_plant_predecessor_inventory_runout():
    res = tools.query_multi_plant_predecessor_inventory_runout(eco_id="ECO-2026-8841")
    assert res["total"] > 0
    assert res["table"] == "multi_plant_predecessor_inventory_runout"
    assert len(res["rows"]) >= 1


def test_query_eco_optimal_cutover_schedules():
    res = tools.query_eco_optimal_cutover_schedules(eco_id="ECO-2026-8841")
    assert res["total"] > 0
    assert res["table"] == "eco_optimal_cutover_schedules"
    assert len(res["rows"]) >= 1


def test_query_erp_bom_effectivity_sync_audit():
    res = tools.query_erp_bom_effectivity_sync_audit(eco_id="ECO-2026-8841")
    assert res["total"] > 0
    assert res["table"] == "erp_bom_effectivity_sync_audit"
    assert len(res["rows"]) >= 1


def test_quality_gate_blocks_invalid_inputs():
    agent = EcoCutoverOrchestrator()
    # 1. Missing idempotency_key
    res = agent.execute_tool(
        "action_lock_multi_plant_eco_effectivity_dates",
        eco_id='ECO-2026-8841',
        optimal_effectivity_date='2026-11-11',
        scrap_avoided_usd=428100.0,
        rationale='Aligned Austin and Guadalajara SAP BOM effectivity to 2026-11-11 to exhaust 6,000 on-hand Rev-B boards prior to Rev-C cutover, avoiding $428,100 in obsolete E&O write-offs.'
    )
    assert res.get("error") == "missing_idempotency_key"

    # 2. Missing required input fields
    res2 = agent.execute_tool(
        "action_lock_multi_plant_eco_effectivity_dates",
        idempotency_key="TEST-KEY-01"
    )
    assert res2.get("error") == "missing_required_inputs"


def test_end_to_end_scenario_execution():
    agent = EcoCutoverOrchestrator()
    result = agent.run_scenario("Execute end-to-end optimization and action write-back.")
    assert result["status"] == "success"
    assert result["agent"] == "eco_cutover_orchestrator"
    assert result["findings_count"] == 4
    assert len(result["actions_executed"]) == 2
    assert result["actions_executed"][0]["status"] == "BOM_EFFECTIVITY_LOCKED"
    assert result["actions_executed"][1]["status"] == "SUPPLIER_PO_REVISION_UPDATED"

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
    test_query_plm_engineering_change_orders()
    print('✓ test_query_plm_engineering_change_orders passed')
    test_query_multi_plant_predecessor_inventory_runout()
    print('✓ test_query_multi_plant_predecessor_inventory_runout passed')
    test_query_eco_optimal_cutover_schedules()
    print('✓ test_query_eco_optimal_cutover_schedules passed')
    test_query_erp_bom_effectivity_sync_audit()
    print('✓ test_query_erp_bom_effectivity_sync_audit passed')
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

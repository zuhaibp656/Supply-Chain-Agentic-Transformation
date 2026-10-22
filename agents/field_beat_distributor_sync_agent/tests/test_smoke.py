"""Smoke test suite for BeatSync — Field Sales & Distributor Inventory Harmonizer (field_beat_distributor_sync_agent)."""
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import FieldBeatDistributorSyncAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "field_beat_distributor_sync_agent"
    assert len(res["systems"]) >= 4

def test_query_distributor_dms_live_inventory():
    res = tools.query_distributor_dms_live_inventory(distributor_id="DIST-MUM-WEST-04")
    assert res["total"] > 0
    assert res["table"] == "distributor_dms_live_inventory"
    assert len(res["rows"]) >= 1


def test_query_fso_daily_beat_store_outlets():
    res = tools.query_fso_daily_beat_store_outlets(fso_id="FSO-WEST-112")
    assert res["total"] > 0
    assert res["table"] == "fso_daily_beat_store_outlets"
    assert len(res["rows"]) >= 1


def test_query_pitch_to_stock_substitution_rules():
    res = tools.query_pitch_to_stock_substitution_rules(stocked_out_sku="SKU-BEV-500ML")
    assert res["total"] > 0
    assert res["table"] == "pitch_to_stock_substitution_rules"
    assert len(res["rows"]) >= 1


def test_query_primary_replenishment_auto_orders():
    res = tools.query_primary_replenishment_auto_orders(distributor_id="DIST-MUM-WEST-04")
    assert res["total"] > 0
    assert res["table"] == "primary_replenishment_auto_orders"
    assert len(res["rows"]) >= 1


def test_quality_gate_blocks_invalid_inputs():
    agent = FieldBeatDistributorSyncAgent()
    # 1. Missing idempotency_key
    res = agent.execute_tool(
        "action_push_fso_dynamic_beat_and_pitch_list",
        fso_id='FSO-WEST-112',
        distributor_id='DIST-MUM-WEST-04',
        suppressed_sku_id='SKU-BEV-500ML',
        promoted_substitute_sku='SKU-BEV-750ML-PROMO',
        rationale='Suppressed stocked-out SKU-BEV-500ML on FSO-WEST-112 mobile handheld and pushed in-stock SKU-BEV-750ML-PROMO (420 cases in DMS), preventing zero-fill secondary orders across 28 retail stores.'
    )
    assert res.get("error") == "missing_idempotency_key"

    # 2. Missing required input fields
    res2 = agent.execute_tool(
        "action_push_fso_dynamic_beat_and_pitch_list",
        idempotency_key="TEST-KEY-01"
    )
    assert res2.get("error") == "missing_required_inputs"


def test_end_to_end_scenario_execution():
    agent = FieldBeatDistributorSyncAgent()
    result = agent.run_scenario("Execute end-to-end optimization and action write-back.")
    assert result["status"] == "success"
    assert result["agent"] == "field_beat_distributor_sync_agent"
    assert result["findings_count"] == 4
    assert len(result["actions_executed"]) == 2
    assert result["actions_executed"][0]["status"] == "FSO_BEAT_AND_PITCH_SYNCED"
    assert result["actions_executed"][1]["status"] == "PRIMARY_REPLENISHMENT_RELEASED"

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
    test_query_distributor_dms_live_inventory()
    print('✓ test_query_distributor_dms_live_inventory passed')
    test_query_fso_daily_beat_store_outlets()
    print('✓ test_query_fso_daily_beat_store_outlets passed')
    test_query_pitch_to_stock_substitution_rules()
    print('✓ test_query_pitch_to_stock_substitution_rules passed')
    test_query_primary_replenishment_auto_orders()
    print('✓ test_query_primary_replenishment_auto_orders passed')
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

"""Smoke test suite for SourcePulse Parametric Should-Cost Agent."""
import os
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import RfqShouldCostAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "rfq_should_cost_agent"
    assert len(res["systems"]) >= 4
    system_ids = [s["id"] for s in res["systems"]]
    assert "bigquery_commodity_lake" in system_ids
    assert "document_ai_rfq_vault" in system_ids
    assert "google_ortools_procurement" in system_ids


def test_query_material_should_cost_bom():
    res = tools.query_material_should_cost_bom(part_number="PART-CAN-ALUM-330ML")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["total_parametric_should_cost_usd"] > 20.0
    assert record["raw_material_cost_usd"] > 10.0


def test_query_commodity_index_rates():
    res = tools.query_commodity_index_rates(index_symbol="LME-ALUM-CASH")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["current_price_usd_per_mt"] > 2000.0


def test_query_supplier_rfq_bids():
    res = tools.query_supplier_rfq_bids(part_number="PART-CAN-ALUM-330ML")
    assert res["total"] >= 3
    ardagh = next((b for b in res["rows"] if "Ardagh" in b["supplier_name"]), None)
    assert ardagh is not None
    assert ardagh["should_cost_gap_pct"] > 25.0


def test_query_combinatorial_award_scenarios():
    res = tools.query_combinatorial_award_scenarios(scenario_id="SCEN-AWARD-DUAL-70-30")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["primary_split_pct"] == 70.0
    assert record["secondary_split_pct"] == 30.0
    assert record["direct_material_savings_pct"] > 5.0


def test_quality_gate_blocks_invalid_award_split():
    agent = RfqShouldCostAgent()
    # Missing idempotency key
    res = agent.execute_tool(
        "action_award_supplier_contract",
        scenario_id="SCEN-TEST",
        part_number="PART-TEST",
        primary_supplier="Vendor A",
        secondary_supplier="Vendor B",
        primary_split_pct=70.0,
        secondary_split_pct=30.0,
        rationale="Split test"
    )
    assert res.get("error") == "missing_idempotency_key"

    # Splits don't sum to 100%
    res2 = agent.execute_tool(
        "action_award_supplier_contract",
        scenario_id="SCEN-TEST",
        part_number="PART-TEST",
        primary_supplier="Vendor A",
        secondary_supplier="Vendor B",
        primary_split_pct=70.0,
        secondary_split_pct=40.0,  # Sums to 110%
        rationale="Bad split",
        idempotency_key="TEST-KEY-005"
    )
    assert res2.get("error") == "allocation_splits_must_sum_to_100"


def test_end_to_end_scenario_execution():
    agent = RfqShouldCostAgent()
    query = "Analyze aluminum can supplier bids against should-cost, challenge Ardagh pricing, and award 70/30 dual-source split in SAP Ariba."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) == 2

    challenge_action = result["actions_executed"][0]
    assert challenge_action["status"] == "NEGOTIATION_CHALLENGE_DISPATCHED"
    assert "CHAL-OUTLIER" in challenge_action["challenge_id"]

    award_action = result["actions_executed"][1]
    assert award_action["status"] == "ARIBA_CONTRACT_AWARDED"
    assert "AWD-ARIBA" in award_action["award_id"]
    assert award_action["primary_split_pct"] == 70.0
    assert award_action["secondary_split_pct"] == 30.0

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) == 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify deterministic copy-ready table and markdown structure
    assert "markdown" in result
    assert "| Source / Bidder |" in result["markdown"]
    assert "### 💎 SourcePulse Parametric Should-Cost" in result["markdown"]
    assert "### 🔗 Connected Systems" in result["markdown"]


if __name__ == "__main__":
    print("Running SourcePulse Parametric Should-Cost smoke tests...")
    test_list_systems()
    test_query_material_should_cost_bom()
    test_query_commodity_index_rates()
    test_query_supplier_rfq_bids()
    test_query_combinatorial_award_scenarios()
    test_quality_gate_blocks_invalid_award_split()
    test_end_to_end_scenario_execution()
    print("✅ All 7 SourcePulse Parametric Should-Cost smoke tests passed successfully!")

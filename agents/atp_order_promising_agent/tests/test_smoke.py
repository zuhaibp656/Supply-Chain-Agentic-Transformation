"""Smoke test suite for PromiseGuard Dynamic Order Promising ATP Agent."""
import os
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import DynamicOrderPromisingAtp
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "atp_order_promising_agent"
    assert len(res["systems"]) >= 4
    system_ids = [s["id"] for s in res["systems"]]
    assert "spanner_realtime_atp_engine" in system_ids
    assert "customer_contract_tier_ledger" in system_ids
    assert "omnichannel_order_stream" in system_ids
    assert "fulfillment_routing_optimizer" in system_ids


def test_query_realtime_sku_atp_allocations():
    res = tools.query_realtime_sku_atp_allocations(sku_id="SKU-BEV-OATMILK-ORIGINAL-1L")
    assert res["total"] > 0
    chicago = [r for r in res["rows"] if r["network_node_id"] == "CDC-CHICAGO-01"][0]
    assert chicago["realtime_uncommitted_atp_units"] == 34200
    assert chicago["tier1_contract_reserved_units"] == 20000
    assert chicago["spanner_query_latency_ms"] < 20.0


def test_query_customer_tier_sla_commitments():
    res = tools.query_customer_tier_sla_commitments(customer_id="CUST-KROGER-CORP")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["contract_tier"] == "TIER_1_STRATEGIC"
    assert record["minimum_fill_rate_sla_pct"] == 98.5
    assert record["otif_penalty_fee_per_late_day_usd"] == 2500.0


def test_query_inbound_customer_order_requests():
    res = tools.query_inbound_customer_order_requests(order_id="ORD-20261022-8841")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["customer_id"] == "CUST-KROGER-CORP"
    assert record["requested_units"] == 8000


def test_query_order_promising_routing_decisions():
    res = tools.query_order_promising_routing_decisions(order_id="ORD-20261022-8841")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["promised_fulfillment_node"] == "CDC-CHICAGO-01"
    assert record["otif_penalty_risk_usd"] == 0.0


def test_quality_gate_blocks_invalid_inputs():
    agent = DynamicOrderPromisingAtp()
    # Missing idempotency key
    res = agent.execute_tool(
        "action_commit_dynamic_order_promise",
        order_id="ORD-01",
        customer_id="CUST-01",
        promised_fulfillment_node="CDC-01",
        promised_delivery_date="2026-10-25T12:00:00Z",
        atp_reserved_qty=1000,
        rationale="Order commit"
    )
    assert res.get("error") == "missing_idempotency_key"

    # Non-positive quantity
    res2 = agent.execute_tool(
        "action_commit_dynamic_order_promise",
        order_id="ORD-01",
        customer_id="CUST-01",
        promised_fulfillment_node="CDC-01",
        promised_delivery_date="2026-10-25T12:00:00Z",
        atp_reserved_qty=-50,
        rationale="Negative qty",
        idempotency_key="KEY-ORD-01"
    )
    assert res2.get("error") == "invalid_reserved_quantity"


def test_end_to_end_scenario_execution():
    agent = DynamicOrderPromisingAtp()
    query = "Evaluate inbound customer order ORD-20261022-8841 from Kroger, execute sub-50ms Spanner ATP check, ringfence Tier 1 strategic allocation reserve, and commit binding delivery date."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) == 2

    ringfence_action = result["actions_executed"][0]
    assert ringfence_action["status"] == "TIER1_ALLOCATION_RINGFENCED"
    assert "TIER-RINGFENCE" in ringfence_action["protection_id"]
    assert ringfence_action["reserve_quantity"] == 20000

    promise_action = result["actions_executed"][1]
    assert promise_action["status"] == "ATP_PROMISE_COMMITTED"
    assert "PROMISE-COMMIT" in promise_action["promise_id"]
    assert promise_action["atp_reserved_qty"] == 8000

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) == 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify copy-ready markdown tables
    markdown = result["markdown"]
    assert "### 🤝 PromiseGuard Real-Time Order Promising & ATP Briefing" in markdown
    assert "| Order ID | Customer Account | Contract Tier |" in markdown
    assert "Kroger National" in markdown
    assert "Tier 1 Allocation Ringfenced" in markdown
    assert "Binding ATP Promise Committed" in markdown


if __name__ == "__main__":
    test_list_systems()
    print("✓ test_list_systems passed")
    test_query_realtime_sku_atp_allocations()
    print("✓ test_query_realtime_sku_atp_allocations passed")
    test_query_customer_tier_sla_commitments()
    print("✓ test_query_customer_tier_sla_commitments passed")
    test_query_inbound_customer_order_requests()
    print("✓ test_query_inbound_customer_order_requests passed")
    test_query_order_promising_routing_decisions()
    print("✓ test_query_order_promising_routing_decisions passed")
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

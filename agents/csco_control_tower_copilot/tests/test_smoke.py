"""Smoke test suite for CSCO Control Tower Copilot."""
import os
import sys
from pathlib import Path

# Add project root to sys.path
AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import CscoControlTowerAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "csco_control_tower_copilot"
    assert len(res["systems"]) >= 4
    system_ids = [s["id"] for s in res["systems"]]
    assert "bigquery_sc_twin" in system_ids
    assert "sap_s4hana_core" in system_ids
    assert "looker_governance" in system_ids


def test_query_executive_kpis():
    res = tools.query_executive_kpis(region="GLOBAL")
    assert res["total"] > 0
    kpi = res["rows"][0]
    assert kpi["region"] == "GLOBAL"
    assert kpi["otif_delivery_pct"] > 90.0
    assert kpi["days_inventory_outstanding_dio"] > 40.0


def test_query_network_bottlenecks():
    res = tools.query_network_bottlenecks(severity="CRITICAL")
    assert res["total"] > 0
    bn = res["rows"][0]
    assert "BN-SUEZ" in bn["bottleneck_id"]
    assert bn["revenue_impact_usd"] > 5000000


def test_query_multiechelon_twin_status():
    res = tools.query_multiechelon_twin_status(safety_stock_health="CRITICAL_BUFFER_BREACH")
    assert res["total"] > 0
    node = res["rows"][0]
    assert "GERMANY" in node["node_id"]
    assert node["days_of_supply"] < 10.0


def test_query_cross_erp_order_backlog():
    res = tools.query_cross_erp_order_backlog(status="JEOPARDY_STOCKOUT")
    assert res["total"] > 0
    order = res["rows"][0]
    assert "SO-" in order["order_id"]
    assert order["total_value_usd"] > 1000000


def test_quality_gate_blocks_excessive_budget():
    agent = CscoControlTowerAgent()
    res = agent.execute_tool(
        "action_execute_executive_playbook",
        playbook_id="PLAYBOOK-UNAUTHORIZED",
        target_facilities=["PLANT-A"],
        allocated_budget_usd=3500000.0,  # Exceeds $2M threshold
        rationale="Unilateral emergency charter",
        idempotency_key="TEST-KEY-001"
    )
    assert res.get("error") == "budget_exceeds_delegation_authority"
    assert res.get("escalation") == "request_csco_cfo_approval"


def test_end_to_end_scenario_execution():
    agent = CscoControlTowerAgent()
    query = "Scan global supply chain twin, identify critical chokepoints, and execute mitigation playbook."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) >= 2

    playbook_action = result["actions_executed"][0]
    assert playbook_action["status"] == "executed"
    assert "EXEC-PB" in playbook_action["execution_id"]

    rebalance_action = result["actions_executed"][1]
    assert rebalance_action["status"] == "dispatched"
    assert "TRF" in rebalance_action["transfer_id"]

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) >= 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"
    assert "vconcat" in result["vega_spec"]

    # Verify deterministic copy-ready table and markdown structure
    assert "markdown" in result
    assert "| Bottleneck ID |" in result["markdown"]
    assert "### 🌐 Executive Briefing" in result["markdown"]
    assert "### 🔗 Connected Systems" in result["markdown"]


if __name__ == "__main__":
    print("Running CSCO Control Tower Copilot smoke tests...")
    test_list_systems()
    test_query_executive_kpis()
    test_query_network_bottlenecks()
    test_query_multiechelon_twin_status()
    test_query_cross_erp_order_backlog()
    test_quality_gate_blocks_excessive_budget()
    test_end_to_end_scenario_execution()
    print("✅ All 7 CSCO Control Tower smoke tests passed successfully!")

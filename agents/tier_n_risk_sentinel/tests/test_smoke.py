"""Smoke test suite for NexusShield Multi-Tier Network Sentinel."""
import os
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import TierNRiskSentinelAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "tier_n_risk_sentinel"
    assert len(res["systems"]) >= 4
    system_ids = [s["id"] for s in res["systems"]]
    assert "spanner_subtier_graph" in system_ids
    assert "weathernext_geopolitical_hub" in system_ids
    assert "sap_s4hana_po_bridge" in system_ids


def test_query_subtier_network_nodes():
    res = tools.query_subtier_network_nodes(node_id="NODE-WEIPA-BAUXITE-AU")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["tier_level"] == 4
    assert record["single_source_chokepoint"] is True


def test_query_active_disruption_threats():
    res = tools.query_active_disruption_threats(threat_id="THREAT-CYCLONE-QLD-01")
    assert res["total"] > 0
    record = res["rows"][0]
    assert "CYCLONE" in record["threat_type"]
    assert record["advance_warning_days"] >= 10


def test_query_bom_revenue_lineage():
    res = tools.query_bom_revenue_lineage(impacted_node="NODE-WEIPA-BAUXITE-AU")
    assert res["total"] > 0
    record = res["rows"][0]
    assert record["total_revenue_at_risk_usd"] > 15000000.0
    assert len(record["finished_goods_impacted"]) >= 2


def test_query_mitigation_playbook_options():
    res = tools.query_mitigation_playbook_options(threat_id="THREAT-CYCLONE-QLD-01")
    assert res["total"] > 0
    record = res["rows"][0]
    assert "Hydro Aluminium" in record["backup_qualified_supplier"]
    assert record["reallocation_split_pct"] == 50.0


def test_quality_gate_blocks_excessive_buffer_surge():
    agent = TierNRiskSentinelAgent()
    # Missing idempotency key
    res = agent.execute_tool(
        "action_surge_meio_safety_buffer",
        playbook_id="PB-TEST",
        sku_ids=["SKU-001"],
        days_buffer_increase=7.0,
        rationale="Buffer test"
    )
    assert res.get("error") == "missing_idempotency_key"

    # Out of bounds (>30 days buffer increase)
    res2 = agent.execute_tool(
        "action_surge_meio_safety_buffer",
        playbook_id="PB-TEST",
        sku_ids=["SKU-001"],
        days_buffer_increase=45.0,
        rationale="Excessive buffer",
        idempotency_key="TEST-KEY-006"
    )
    assert res2.get("error") == "days_buffer_increase_out_of_bounds"


def test_end_to_end_scenario_execution():
    agent = TierNRiskSentinelAgent()
    query = "Detect cyclone threatening Weipa mine, trace revenue at risk in Spanner Graph, and execute 50% PO split to Norway."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) >= 2

    po_action = result["actions_executed"][0]
    assert po_action["status"] == "SAP_PO_SPLIT_DISPATCHED"
    assert "PO-SPLIT" in po_action["po_split_id"]
    assert po_action["reallocation_split_pct"] == 50.0

    buffer_action = result["actions_executed"][1]
    assert buffer_action["status"] == "MEIO_BUFFER_SURGE_COMMITTED"
    assert "SURGE-MEIO" in buffer_action["buffer_id"]
    assert buffer_action["days_buffer_increase"] == 7.0

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) >= 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify deterministic copy-ready table and markdown structure
    assert "markdown" in result
    assert "| Tier Depth |" in result["markdown"]
    assert "### 🛡️ NexusShield Multi-Tier Supply Network" in result["markdown"]
    assert "### 🔗 Connected Systems" in result["markdown"]


if __name__ == "__main__":
    print("Running NexusShield Multi-Tier Network Sentinel smoke tests...")
    test_list_systems()
    test_query_subtier_network_nodes()
    test_query_active_disruption_threats()
    test_query_bom_revenue_lineage()
    test_query_mitigation_playbook_options()
    test_quality_gate_blocks_excessive_buffer_surge()
    test_end_to_end_scenario_execution()
    print("✅ All 7 NexusShield Multi-Tier Network Sentinel smoke tests passed successfully!")

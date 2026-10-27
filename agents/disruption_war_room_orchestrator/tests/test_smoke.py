"""Smoke test suite for Disruption War Room Orchestrator."""
import os
import sys
from pathlib import Path

# Add project root to sys.path
AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import DisruptionWarRoomAgent
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "disruption_war_room_orchestrator"
    assert len(res["systems"]) >= 5
    system_ids = [s["id"] for s in res["systems"]]
    assert "weather_apis" in system_ids
    assert "maritime_ais" in system_ids
    assert "resilinc" in system_ids


def test_query_weather_alerts():
    res = tools.query_weather_alerts(region="Taiwan")
    assert res["total"] > 0
    assert any("Typhoon" in r["event_type"] or "Taiwan" in r["region"] for r in res["rows"])


def test_query_maritime_ais_vessels():
    res = tools.query_maritime_ais_vessels()
    assert res["total"] > 0
    vessel = res["rows"][0]
    assert "EVER GLOBE" in vessel["vessel_name"]
    assert len(vessel["at_risk_purchase_orders"]) > 0


def test_query_resilinc_supplier_facilities():
    res = tools.query_resilinc_supplier_facilities(tier_level=2)
    assert res["total"] > 0
    sup = res["rows"][0]
    assert sup["tier_level"] >= 2
    assert "Semiconductor" in sup["supplier_name"]


def test_query_news_disruptions():
    res = tools.query_news_disruptions(lookup_key="strike")
    assert res["total"] > 0
    assert any("strike" in r["headline"].lower() for r in res["rows"])


def test_quality_gate_blocks_missing_idempotency():
    agent = DisruptionWarRoomAgent()
    # Missing idempotency_key should be blocked by safety callback
    res = agent.execute_tool(
        "action_create_war_room_incident",
        title="Test Incident Without Idempotency",
        severity="HIGH",
        affected_lanes=["LANE-01"],
        action_plan="Emergency reroute"
        # No idempotency_key provided
    )
    assert res.get("error") == "missing_idempotency_key"
    assert res.get("escalation") == "request_confirmation"


def test_end_to_end_scenario_execution():
    agent = DisruptionWarRoomAgent()
    query = "Alert: Typhoon Gaemi approaching Taiwan Strait, check at-risk vessels, tier-2 fabbing suppliers, and initiate war room."
    result = agent.run_scenario(query)
    assert result["status"] == "success"
    assert result["findings_count"] >= 3
    assert len(result["actions_executed"]) >= 2
    
    incident = result["actions_executed"][0]
    assert incident["status"] == "created"
    assert "INC-WR" in incident["incident_id"]

    expedite = result["actions_executed"][1]
    assert expedite["status"] == "dispatched"
    assert "FAST_TRACK_AIR_CHARTER" in expedite["audit_trail"]

    # Verify A2UI surface compliance (Card containing VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) >= 2
    assert "vega_spec" in result
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"
    assert "vconcat" in result["vega_spec"]

    # Verify deterministic copy-ready table and markdown structure
    assert "markdown" in result
    assert "| PO Number |" in result["markdown"]
    assert "### ⚡ Crisis Briefing" in result["markdown"]
    assert "### 🔗 Connected Systems" in result["markdown"]


if __name__ == "__main__":
    print("Running Disruption War Room Orchestrator smoke tests...")
    test_list_systems()
    test_query_weather_alerts()
    test_query_maritime_ais_vessels()
    test_query_resilinc_supplier_facilities()
    test_query_news_disruptions()
    test_quality_gate_blocks_missing_idempotency()
    test_end_to_end_scenario_execution()
    print("✅ All 7 smoke tests passed successfully!")

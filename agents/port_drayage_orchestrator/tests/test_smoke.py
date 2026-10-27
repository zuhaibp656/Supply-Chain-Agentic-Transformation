"""Smoke test suite for PortWatch — Global Ocean Vessel, Container Stowage & Port Drayage Orchestrator (port_drayage_orchestrator)."""
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import PortDrayageOrchestrator
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "port_drayage_orchestrator"
    assert len(res["systems"]) >= 4

def test_query_ocean_vessel_ais_berth_telemetry():
    res = tools.query_ocean_vessel_ais_berth_telemetry(vessel_imo="IMO-9839179")
    assert res["total"] > 0
    assert res["table"] == "ocean_vessel_ais_berth_telemetry"
    assert len(res["rows"]) >= 1


def test_query_container_discharge_demurrage_ledger():
    res = tools.query_container_discharge_demurrage_ledger(container_id="MSKU-904812-0")
    assert res["total"] > 0
    assert res["table"] == "container_discharge_demurrage_ledger"
    assert len(res["rows"]) >= 1


def test_query_port_terminal_gate_appointments():
    res = tools.query_port_terminal_gate_appointments(terminal_id="USLAX_APM_PIER400")
    assert res["total"] > 0
    assert res["table"] == "port_terminal_gate_appointments"
    assert len(res["rows"]) >= 1


def test_query_drayage_chassis_transload_allocations():
    res = tools.query_drayage_chassis_transload_allocations(container_id="MSKU-904812-0")
    assert res["total"] > 0
    assert res["table"] == "drayage_chassis_transload_allocations"
    assert len(res["rows"]) >= 1


def test_quality_gate_blocks_invalid_inputs():
    agent = PortDrayageOrchestrator()
    # 1. Missing idempotency_key
    res = agent.execute_tool(
        "action_book_dual_transaction_drayage_gate",
        container_id='MSKU-904812-0',
        terminal_id='USLAX_APM_PIER400',
        gate_slot_id='GATE-LAX-20261028-T1',
        drayage_carrier_id='PAC-HARBOR-DRAY',
        rationale='Booked dual-transaction Pier 400 gate slot 24 hours prior to Last Free Day using upper-deck discharge prediction, avoiding $1,875 in port demurrage.'
    )
    assert res.get("error") == "missing_idempotency_key"

    # 2. Missing required input fields
    res2 = agent.execute_tool(
        "action_book_dual_transaction_drayage_gate",
        idempotency_key="TEST-KEY-01"
    )
    assert res2.get("error") == "missing_required_inputs"


def test_end_to_end_scenario_execution():
    agent = PortDrayageOrchestrator()
    result = agent.run_scenario("Execute end-to-end optimization and action write-back.")
    assert result["status"] == "success"
    assert result["agent"] == "port_drayage_orchestrator"
    assert result["findings_count"] == 4
    assert len(result["actions_executed"]) >= 2
    assert result["actions_executed"][0]["status"] == "DUAL_DRAYAGE_GATE_BOOKED"
    assert result["actions_executed"][1]["status"] == "CONTAINER_DIVERTED_TO_TRANSLOAD"

    # Verify A2UI v0.9 surface compliance (Card wrapping ONLY VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) >= 2
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify copy-ready markdown output
    md = result["markdown"]
    assert "### ✦" in md
    assert "| Dimension | Metric Value |" in md
    assert "### 🔗 Connected Enterprise Systems" in md


if __name__ == "__main__":
    test_list_systems()
    print("✓ test_list_systems passed")
    test_query_ocean_vessel_ais_berth_telemetry()
    print('✓ test_query_ocean_vessel_ais_berth_telemetry passed')
    test_query_container_discharge_demurrage_ledger()
    print('✓ test_query_container_discharge_demurrage_ledger passed')
    test_query_port_terminal_gate_appointments()
    print('✓ test_query_port_terminal_gate_appointments passed')
    test_query_drayage_chassis_transload_allocations()
    print('✓ test_query_drayage_chassis_transload_allocations passed')
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

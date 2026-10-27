"""Smoke test suite for SentinelMove — Multi-Modal In-Transit Control Tower & Freight Auditor (freight_control_tower)."""
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import FreightControlTower
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "freight_control_tower"
    assert len(res["systems"]) >= 4

def test_query_in_transit_multimodal_telemetry():
    res = tools.query_in_transit_multimodal_telemetry(shipment_id="SHP-REEF-8841")
    assert res["total"] > 0
    assert res["table"] == "in_transit_multimodal_telemetry"
    assert len(res["rows"]) >= 1


def test_query_cold_chain_thermal_excursion_alerts():
    res = tools.query_cold_chain_thermal_excursion_alerts(shipment_id="SHP-REEF-8841")
    assert res["total"] > 0
    assert res["table"] == "cold_chain_thermal_excursion_alerts"
    assert len(res["rows"]) >= 1


def test_query_carrier_edi210_freight_invoices():
    res = tools.query_carrier_edi210_freight_invoices(invoice_id="INV-EDI210-77410")
    assert res["total"] > 0
    assert res["table"] == "carrier_edi210_freight_invoices"
    assert len(res["rows"]) >= 1


def test_query_freight_audit_discrepancy_ledger():
    res = tools.query_freight_audit_discrepancy_ledger(invoice_id="INV-EDI210-77410")
    assert res["total"] > 0
    assert res["table"] == "freight_audit_discrepancy_ledger"
    assert len(res["rows"]) >= 1


def test_quality_gate_blocks_invalid_inputs():
    agent = FreightControlTower()
    # 1. Missing idempotency_key
    res = agent.execute_tool(
        "action_reroute_in_transit_reefer_shipment",
        shipment_id='SHP-REEF-8841',
        diversion_hub_id='DES_MOINES_COLD_HUB_04',
        cargo_value_protected_usd=148000.0,
        rationale='IoT telemetry detected compressor coolant pressure drop (+3.4°C drift) 52 minutes before excursion limit; diverted SHP-REEF-8841 to Des Moines Cold Hub (24.5 km) for cross-dock into backup reefer, saving $148,000 cargo.'
    )
    assert res.get("error") == "missing_idempotency_key"

    # 2. Missing required input fields
    res2 = agent.execute_tool(
        "action_reroute_in_transit_reefer_shipment",
        idempotency_key="TEST-KEY-01"
    )
    assert res2.get("error") == "missing_required_inputs"


def test_end_to_end_scenario_execution():
    agent = FreightControlTower()
    result = agent.run_scenario("Execute end-to-end optimization and action write-back.")
    assert result["status"] == "success"
    assert result["agent"] == "freight_control_tower"
    assert result["findings_count"] == 4
    assert len(result["actions_executed"]) >= 2
    assert result["actions_executed"][0]["status"] == "REEFER_DIVERTED_TO_COLD_HUB"
    assert result["actions_executed"][1]["status"] == "FREIGHT_INVOICE_ADJUSTED"

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
    test_query_in_transit_multimodal_telemetry()
    print('✓ test_query_in_transit_multimodal_telemetry passed')
    test_query_cold_chain_thermal_excursion_alerts()
    print('✓ test_query_cold_chain_thermal_excursion_alerts passed')
    test_query_carrier_edi210_freight_invoices()
    print('✓ test_query_carrier_edi210_freight_invoices passed')
    test_query_freight_audit_discrepancy_ledger()
    print('✓ test_query_freight_audit_discrepancy_ledger passed')
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

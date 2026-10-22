"""Smoke test suite for EcoChain — Shipment-Level Scope-3 Carbon, CBAM & EUDR Ledger (carbon_scope3_ledger)."""
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import CarbonScope3Ledger
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "carbon_scope3_ledger"
    assert len(res["systems"]) >= 4

def test_query_shipment_level_scope3_emissions():
    res = tools.query_shipment_level_scope3_emissions(shipment_id="SHP-GLB-20261022-301")
    assert res["total"] > 0
    assert res["table"] == "shipment_level_scope3_emissions"
    assert len(res["rows"]) >= 1


def test_query_eu_cbam_embedded_carbon_declarations():
    res = tools.query_eu_cbam_embedded_carbon_declarations(import_declaration_id="CBAM-EU-2026-Q4-09")
    assert res["total"] > 0
    assert res["table"] == "eu_cbam_embedded_carbon_declarations"
    assert len(res["rows"]) >= 1


def test_query_eudr_earth_engine_plot_verifications():
    res = tools.query_eudr_earth_engine_plot_verifications(plot_id="PLOT-BR-PARA-4410")
    assert res["total"] > 0
    assert res["table"] == "eudr_earth_engine_plot_verifications"
    assert len(res["rows"]) >= 1


def test_query_low_carbon_carrier_and_supplier_swaps():
    res = tools.query_low_carbon_carrier_and_supplier_swaps(swap_id="SWAP-DEC-2026-04")
    assert res["total"] > 0
    assert res["table"] == "low_carbon_carrier_and_supplier_swaps"
    assert len(res["rows"]) >= 1


def test_quality_gate_blocks_invalid_inputs():
    agent = CarbonScope3Ledger()
    # 1. Missing idempotency_key
    res = agent.execute_tool(
        "action_certify_cbam_and_eudr_compliance_dossier",
        import_declaration_id='CBAM-EU-2026-Q4-09',
        plot_id='PLOT-BR-PARA-4410',
        cbam_tax_avoided_eur=64260.0,
        rationale='Certified primary smelter emissions (2.1 tCO2e/t vs 8.4 EU default penalty, saving €64,260 in CBAM certificates) and verified zero post-2020 deforestation on PLOT-BR-PARA-4410 via Google Earth Engine.'
    )
    assert res.get("error") == "missing_idempotency_key"

    # 2. Missing required input fields
    res2 = agent.execute_tool(
        "action_certify_cbam_and_eudr_compliance_dossier",
        idempotency_key="TEST-KEY-01"
    )
    assert res2.get("error") == "missing_required_inputs"


def test_end_to_end_scenario_execution():
    agent = CarbonScope3Ledger()
    result = agent.run_scenario("Execute end-to-end optimization and action write-back.")
    assert result["status"] == "success"
    assert result["agent"] == "carbon_scope3_ledger"
    assert result["findings_count"] == 4
    assert len(result["actions_executed"]) == 2
    assert result["actions_executed"][0]["status"] == "CBAM_AND_EUDR_DOSSIER_CERTIFIED"
    assert result["actions_executed"][1]["status"] == "LOW_CARBON_LANE_SWAP_COMMITTED"

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
    test_query_shipment_level_scope3_emissions()
    print('✓ test_query_shipment_level_scope3_emissions passed')
    test_query_eu_cbam_embedded_carbon_declarations()
    print('✓ test_query_eu_cbam_embedded_carbon_declarations passed')
    test_query_eudr_earth_engine_plot_verifications()
    print('✓ test_query_eudr_earth_engine_plot_verifications passed')
    test_query_low_carbon_carrier_and_supplier_swaps()
    print('✓ test_query_low_carbon_carrier_and_supplier_swaps passed')
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\nALL 7 TESTS PASSED SUCCESSFULLY ✅")

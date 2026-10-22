"""Deterministic and fixture-backed tools for EcoChain — Shipment-Level Scope-3 Carbon, CBAM & EUDR Ledger."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List

FIXTURES = Path(os.environ.get("FIXTURES_ROOT", str(Path(__file__).resolve().parent.parent / "fixtures")))
ACTION_EVENTS_PATH = Path(__file__).resolve().parent.parent / "artifacts" / "action-events.jsonl"


def _read_json(table_filename: str) -> List[Dict[str, Any]]:
    p = FIXTURES / "tables" / table_filename
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []


def _append_action_event(tool_name: str, payload: Dict[str, Any]) -> None:
    ACTION_EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with ACTION_EVENTS_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"tool": tool_name, **payload}, sort_keys=True) + "\n")


def _deterministic_id(prefix: str, *parts: Any) -> str:
    payload = "|".join(str(p) for p in parts if p is not None and p != "")
    digest = hashlib.sha1(payload.encode("utf-8")).hexdigest()[:8].upper() if payload else "00000000"
    return f"{prefix}-{digest}"


def list_systems() -> Dict[str, Any]:
    """Returns connected enterprise systems and solver engines for carbon_scope3_ledger."""
    return {
        "agent": "carbon_scope3_ledger",
        "systems": [
            {
                        "id": "iso14083_glec_carbon_engine",
                        "name": "ISO 14083 & GLEC Framework v3.0 Primary Telemetry Carbon Ledger",
                        "protocol": "BigQuery SQL / Python",
                        "tables": [
                                    "shipment_level_scope3_emissions"
                        ]
            },
            {
                        "id": "eu_cbam_registry_gateway",
                        "name": "EU Carbon Border Adjustment Mechanism (CBAM) Embedded Carbon Engine",
                        "protocol": "XML / REST API",
                        "tables": [
                                    "eu_cbam_embedded_carbon_declarations"
                        ]
            },
            {
                        "id": "google_earth_engine_eudr",
                        "name": "Google Earth Engine Satellite Polygon Deforestation Verifier (EUDR)",
                        "protocol": "Earth Engine Python API",
                        "tables": [
                                    "eudr_earth_engine_plot_verifications"
                        ]
            },
            {
                        "id": "scope3_decarbonization_solver",
                        "name": "OR-Tools Low-Carbon Carrier & Smelter Swap Optimizer",
                        "protocol": "Python MILP",
                        "tables": [
                                    "low_carbon_carrier_and_supplier_swaps"
                        ]
            }
]
    }

def query_shipment_level_scope3_emissions(
    shipment_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query shipment_level_scope3_emissions records from iso14083_glec_carbon_engine."""
    rows = _read_json("shipment_level_scope3_emissions.json")
    if shipment_id:
        rows = [r for r in rows if shipment_id.lower() in str(r.get("shipment_id", "")).lower()]
    return {
        "source_system": "iso14083_glec_carbon_engine",
        "table": "shipment_level_scope3_emissions",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_eu_cbam_embedded_carbon_declarations(
    import_declaration_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query eu_cbam_embedded_carbon_declarations records from eu_cbam_registry_gateway."""
    rows = _read_json("eu_cbam_embedded_carbon_declarations.json")
    if import_declaration_id:
        rows = [r for r in rows if import_declaration_id.lower() in str(r.get("import_declaration_id", "")).lower()]
    return {
        "source_system": "eu_cbam_registry_gateway",
        "table": "eu_cbam_embedded_carbon_declarations",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_eudr_earth_engine_plot_verifications(
    plot_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query eudr_earth_engine_plot_verifications records from google_earth_engine_eudr."""
    rows = _read_json("eudr_earth_engine_plot_verifications.json")
    if plot_id:
        rows = [r for r in rows if plot_id.lower() in str(r.get("plot_id", "")).lower()]
    return {
        "source_system": "google_earth_engine_eudr",
        "table": "eudr_earth_engine_plot_verifications",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_low_carbon_carrier_and_supplier_swaps(
    swap_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query low_carbon_carrier_and_supplier_swaps records from scope3_decarbonization_solver."""
    rows = _read_json("low_carbon_carrier_and_supplier_swaps.json")
    if swap_id:
        rows = [r for r in rows if swap_id.lower() in str(r.get("swap_id", "")).lower()]
    return {
        "source_system": "scope3_decarbonization_solver",
        "table": "low_carbon_carrier_and_supplier_swaps",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_certify_cbam_and_eudr_compliance_dossier(
    import_declaration_id: Any,
    plot_id: Any,
    cbam_tax_avoided_eur: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_certify_cbam_and_eudr_compliance_dossier mutation with deterministic audit logging."""
    action_id = _deterministic_id("ESG-CERT", import_declaration_id, idempotency_key)
    payload = {
        "dispatch_execution_id": action_id,
        "import_declaration_id": import_declaration_id,
        "plot_id": plot_id,
        "cbam_tax_avoided_eur": cbam_tax_avoided_eur,
        "rationale": rationale,
        "status": "CBAM_AND_EUDR_DOSSIER_CERTIFIED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_certify_cbam_and_eudr_compliance_dossier", payload)
    return payload


def action_commit_scope3_decarbonization_swap(
    swap_id: Any,
    target_corridor_or_bom: Any,
    annual_tco2e_reduction: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_commit_scope3_decarbonization_swap mutation with deterministic audit logging."""
    action_id = _deterministic_id("ESG-SWAP", swap_id, idempotency_key)
    payload = {
        "secondary_action_id": action_id,
        "swap_id": swap_id,
        "target_corridor_or_bom": target_corridor_or_bom,
        "annual_tco2e_reduction": annual_tco2e_reduction,
        "rationale": rationale,
        "status": "LOW_CARBON_LANE_SWAP_COMMITTED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_commit_scope3_decarbonization_swap", payload)
    return payload


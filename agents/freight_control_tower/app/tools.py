"""Deterministic and fixture-backed tools for SentinelMove — Multi-Modal In-Transit Control Tower & Freight Auditor."""
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
    """Returns connected enterprise systems and solver engines for freight_control_tower."""
    return {
        "agent": "freight_control_tower",
        "systems": [
            {
                        "id": "project44_multimodal_telemetry",
                        "name": "Project44 / FourKites Real-Time GPS & Cold-Chain IoT Stream",
                        "protocol": "Webhook / REST v4",
                        "tables": [
                                    "in_transit_multimodal_telemetry",
                                    "cold_chain_thermal_excursion_alerts"
                        ]
            },
            {
                        "id": "google_maps_geofence_verifier",
                        "name": "Google Maps Platform Dock Geofence Timestamp & Detention Verifier",
                        "protocol": "REST / BigQuery GIS",
                        "tables": [
                                    "freight_audit_discrepancy_ledger"
                        ]
            },
            {
                        "id": "document_ai_edi210_auditor",
                        "name": "Google Cloud Document AI & EDI 210 3-Way Freight Invoice Auditor",
                        "protocol": "gRPC / EDI 210",
                        "tables": [
                                    "carrier_edi210_freight_invoices",
                                    "freight_audit_discrepancy_ledger"
                        ]
            },
            {
                        "id": "sap_ap_freight_settlement",
                        "name": "SAP S/4HANA TM/AP Automated Freight Settlement & Debit Memo Engine",
                        "protocol": "OData v4",
                        "tables": [
                                    "freight_audit_discrepancy_ledger"
                        ]
            }
]
    }

def query_in_transit_multimodal_telemetry(
    shipment_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query in_transit_multimodal_telemetry records from project44_multimodal_telemetry."""
    rows = _read_json("in_transit_multimodal_telemetry.json")
    if shipment_id:
        rows = [r for r in rows if shipment_id.lower() in str(r.get("shipment_id", "")).lower()]
    return {
        "source_system": "project44_multimodal_telemetry",
        "table": "in_transit_multimodal_telemetry",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_cold_chain_thermal_excursion_alerts(
    shipment_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query cold_chain_thermal_excursion_alerts records from google_maps_geofence_verifier."""
    rows = _read_json("cold_chain_thermal_excursion_alerts.json")
    if shipment_id:
        rows = [r for r in rows if shipment_id.lower() in str(r.get("shipment_id", "")).lower()]
    return {
        "source_system": "google_maps_geofence_verifier",
        "table": "cold_chain_thermal_excursion_alerts",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_carrier_edi210_freight_invoices(
    invoice_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query carrier_edi210_freight_invoices records from document_ai_edi210_auditor."""
    rows = _read_json("carrier_edi210_freight_invoices.json")
    if invoice_id:
        rows = [r for r in rows if invoice_id.lower() in str(r.get("invoice_id", "")).lower()]
    return {
        "source_system": "document_ai_edi210_auditor",
        "table": "carrier_edi210_freight_invoices",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_freight_audit_discrepancy_ledger(
    invoice_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query freight_audit_discrepancy_ledger records from sap_ap_freight_settlement."""
    rows = _read_json("freight_audit_discrepancy_ledger.json")
    if invoice_id:
        rows = [r for r in rows if invoice_id.lower() in str(r.get("invoice_id", "")).lower()]
    return {
        "source_system": "sap_ap_freight_settlement",
        "table": "freight_audit_discrepancy_ledger",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_reroute_in_transit_reefer_shipment(
    shipment_id: Any,
    diversion_hub_id: Any,
    cargo_value_protected_usd: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_reroute_in_transit_reefer_shipment mutation with deterministic audit logging."""
    action_id = _deterministic_id("SENT-DIV", shipment_id, idempotency_key)
    payload = {
        "dispatch_execution_id": action_id,
        "shipment_id": shipment_id,
        "diversion_hub_id": diversion_hub_id,
        "cargo_value_protected_usd": cargo_value_protected_usd,
        "rationale": rationale,
        "status": "REEFER_DIVERTED_TO_COLD_HUB",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_reroute_in_transit_reefer_shipment", payload)
    return payload


def action_issue_freight_audit_debit_adjustment(
    invoice_id: Any,
    carrier_id: Any,
    disputed_amount_usd: Any,
    verified_payable_usd: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_issue_freight_audit_debit_adjustment mutation with deterministic audit logging."""
    action_id = _deterministic_id("SENT-AUD", invoice_id, idempotency_key)
    payload = {
        "secondary_action_id": action_id,
        "invoice_id": invoice_id,
        "carrier_id": carrier_id,
        "disputed_amount_usd": disputed_amount_usd,
        "verified_payable_usd": verified_payable_usd,
        "rationale": rationale,
        "status": "FREIGHT_INVOICE_ADJUSTED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_issue_freight_audit_debit_adjustment", payload)
    return payload


"""Deterministic and fixture-backed tools for OTIFShield — Customer SLA Rescue & Chargeback Dispute Agent."""
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
    """Returns connected enterprise systems and solver engines for otif_penalty_shield."""
    return {
        "agent": "otif_penalty_shield",
        "systems": [
            {
                        "id": "mabd_otif_risk_predictor",
                        "name": "Vertex AI 72-Hour Customer MABD & OTIF Breach Risk Scorer",
                        "protocol": "BigQuery ML / Spanner",
                        "tables": [
                                    "open_retail_customer_orders_sla",
                                    "predicted_otif_breach_alerts"
                        ]
            },
            {
                        "id": "retail_link_chargeback_portal",
                        "name": "Walmart Retail Link / Target Partners Online Deduction Feed",
                        "protocol": "EDI 812 / Portal API",
                        "tables": [
                                    "retailer_otif_chargeback_deductions"
                        ]
            },
            {
                        "id": "geofence_edi856_dossier_builder",
                        "name": "Google Maps Geofence + EDI 856 ASN + Signed ePOD Evidence Compiler",
                        "protocol": "Document AI / GIS",
                        "tables": [
                                    "geofence_edi856_dispute_dossiers"
                        ]
            },
            {
                        "id": "sap_sd_order_rescue_broker",
                        "name": "SAP S/4HANA SD Priority Wave & Alternate Hub Split-Ship Broker",
                        "protocol": "OData v4",
                        "tables": [
                                    "predicted_otif_breach_alerts"
                        ]
            }
]
    }

def query_open_retail_customer_orders_sla(
    order_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query open_retail_customer_orders_sla records from mabd_otif_risk_predictor."""
    rows = _read_json("open_retail_customer_orders_sla.json")
    if order_id:
        rows = [r for r in rows if order_id.lower() in str(r.get("order_id", "")).lower()]
    return {
        "source_system": "mabd_otif_risk_predictor",
        "table": "open_retail_customer_orders_sla",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_predicted_otif_breach_alerts(
    order_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query predicted_otif_breach_alerts records from retail_link_chargeback_portal."""
    rows = _read_json("predicted_otif_breach_alerts.json")
    if order_id:
        rows = [r for r in rows if order_id.lower() in str(r.get("order_id", "")).lower()]
    return {
        "source_system": "retail_link_chargeback_portal",
        "table": "predicted_otif_breach_alerts",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_retailer_otif_chargeback_deductions(
    deduction_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query retailer_otif_chargeback_deductions records from geofence_edi856_dossier_builder."""
    rows = _read_json("retailer_otif_chargeback_deductions.json")
    if deduction_id:
        rows = [r for r in rows if deduction_id.lower() in str(r.get("deduction_id", "")).lower()]
    return {
        "source_system": "geofence_edi856_dossier_builder",
        "table": "retailer_otif_chargeback_deductions",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_geofence_edi856_dispute_dossiers(
    deduction_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query geofence_edi856_dispute_dossiers records from sap_sd_order_rescue_broker."""
    rows = _read_json("geofence_edi856_dispute_dossiers.json")
    if deduction_id:
        rows = [r for r in rows if deduction_id.lower() in str(r.get("deduction_id", "")).lower()]
    return {
        "source_system": "sap_sd_order_rescue_broker",
        "table": "geofence_edi856_dispute_dossiers",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_execute_otif_sla_rescue_intervention(
    order_id: Any,
    customer_id: Any,
    rescue_option: Any,
    penalty_avoided_usd: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_execute_otif_sla_rescue_intervention mutation with deterministic audit logging."""
    action_id = _deterministic_id("OTIF-RSC", order_id, idempotency_key)
    payload = {
        "dispatch_execution_id": action_id,
        "order_id": order_id,
        "customer_id": customer_id,
        "rescue_option": rescue_option,
        "penalty_avoided_usd": penalty_avoided_usd,
        "rationale": rationale,
        "status": "OTIF_SLA_RESCUE_EXECUTED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_execute_otif_sla_rescue_intervention", payload)
    return payload


def action_submit_chargeback_dispute_dossier(
    deduction_id: Any,
    dossier_id: Any,
    disputed_amount_usd: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_submit_chargeback_dispute_dossier mutation with deterministic audit logging."""
    action_id = _deterministic_id("OTIF-DSP", deduction_id, idempotency_key)
    payload = {
        "secondary_action_id": action_id,
        "deduction_id": deduction_id,
        "dossier_id": dossier_id,
        "disputed_amount_usd": disputed_amount_usd,
        "rationale": rationale,
        "status": "CHARGEBACK_DISPUTE_SUBMITTED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_submit_chargeback_dispute_dossier", payload)
    return payload


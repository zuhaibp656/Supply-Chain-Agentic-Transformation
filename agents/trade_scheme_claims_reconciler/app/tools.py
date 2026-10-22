"""Deterministic and fixture-backed tools for SchemeGuard — Secondary Trade Payout & Claims Sentinel."""
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
    """Returns connected enterprise systems and solver engines for trade_scheme_claims_reconciler."""
    return {
        "agent": "trade_scheme_claims_reconciler",
        "systems": [
            {
                        "id": "trade_scheme_slab_engine",
                        "name": "Enterprise Trade Promotion Management (TPM) Circular & Slab Rule Engine",
                        "protocol": "REST / JSON",
                        "tables": [
                                    "active_trade_promotion_schemes"
                        ]
            },
            {
                        "id": "dms_secondary_claims_portal",
                        "name": "Distributor Secondary Billing & Scheme Claim Submission Portal",
                        "protocol": "OData / REST",
                        "tables": [
                                    "distributor_secondary_claim_submissions"
                        ]
            },
            {
                        "id": "phantom_invoice_graph_detector",
                        "name": "BigQuery ML Anomaly & Split-Invoice Leakage Detector",
                        "protocol": "BigQuery SQL",
                        "tables": [
                                    "claim_anomaly_audit_findings"
                        ]
            },
            {
                        "id": "sap_fi_credit_memo_poster",
                        "name": "SAP S/4HANA FI Accounts Receivable Automated Credit Memo BAPI",
                        "protocol": "RFC / OData v4",
                        "tables": [
                                    "sap_fi_credit_note_settlements"
                        ]
            }
]
    }

def query_active_trade_promotion_schemes(
    scheme_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query active_trade_promotion_schemes records from trade_scheme_slab_engine."""
    rows = _read_json("active_trade_promotion_schemes.json")
    if scheme_id:
        rows = [r for r in rows if scheme_id.lower() in str(r.get("scheme_id", "")).lower()]
    return {
        "source_system": "trade_scheme_slab_engine",
        "table": "active_trade_promotion_schemes",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_distributor_secondary_claim_submissions(
    claim_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query distributor_secondary_claim_submissions records from dms_secondary_claims_portal."""
    rows = _read_json("distributor_secondary_claim_submissions.json")
    if claim_id:
        rows = [r for r in rows if claim_id.lower() in str(r.get("claim_id", "")).lower()]
    return {
        "source_system": "dms_secondary_claims_portal",
        "table": "distributor_secondary_claim_submissions",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_claim_anomaly_audit_findings(
    claim_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query claim_anomaly_audit_findings records from phantom_invoice_graph_detector."""
    rows = _read_json("claim_anomaly_audit_findings.json")
    if claim_id:
        rows = [r for r in rows if claim_id.lower() in str(r.get("claim_id", "")).lower()]
    return {
        "source_system": "phantom_invoice_graph_detector",
        "table": "claim_anomaly_audit_findings",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_sap_fi_credit_note_settlements(
    claim_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query sap_fi_credit_note_settlements records from sap_fi_credit_memo_poster."""
    rows = _read_json("sap_fi_credit_note_settlements.json")
    if claim_id:
        rows = [r for r in rows if claim_id.lower() in str(r.get("claim_id", "")).lower()]
    return {
        "source_system": "sap_fi_credit_memo_poster",
        "table": "sap_fi_credit_note_settlements",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_flag_phantom_invoice_for_audit_hold(
    claim_id: Any,
    flagged_invoices: Any,
    disallowed_amount_usd: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_flag_phantom_invoice_for_audit_hold mutation with deterministic audit logging."""
    action_id = _deterministic_id("SCHM-HOLD", claim_id, idempotency_key)
    payload = {
        "dispatch_execution_id": action_id,
        "claim_id": claim_id,
        "flagged_invoices": flagged_invoices,
        "disallowed_amount_usd": disallowed_amount_usd,
        "rationale": rationale,
        "status": "ANOMALOUS_INVOICES_DISALLOWED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_flag_phantom_invoice_for_audit_hold", payload)
    return payload


def action_post_sap_fi_trade_credit_note(
    claim_id: Any,
    distributor_id: Any,
    approved_amount_usd: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_post_sap_fi_trade_credit_note mutation with deterministic audit logging."""
    action_id = _deterministic_id("SCHM-CN", claim_id, idempotency_key)
    payload = {
        "secondary_action_id": action_id,
        "claim_id": claim_id,
        "distributor_id": distributor_id,
        "approved_amount_usd": approved_amount_usd,
        "rationale": rationale,
        "status": "SAP_FI_CREDIT_NOTE_POSTED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_post_sap_fi_trade_credit_note", payload)
    return payload


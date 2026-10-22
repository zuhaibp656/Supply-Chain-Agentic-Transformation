"""Deterministic and fixture-backed tools for ShelfVision — Retail Planogram & Visibility Auditor."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List

FIXTURES = Path(os.environ.get("FIXTURES_ROOT", str(Path(__file__).resolve().parent.parent / "fixtures")))
ACTION_EVENTS_PATH = Path(__file__).resolve().parent.parent / "artifacts" / "action-events.jsonl"


def _read_json(table_filename: str) -> List[Dict[str, Any]]:
    candidates = [
        Path(__file__).resolve().parent.parent / "fixtures" / "tables" / table_filename,
        Path.cwd() / "fixtures" / "tables" / table_filename,
        Path("/code/fixtures/tables") / table_filename,
        FIXTURES / "tables" / table_filename,
    ]
    for p in candidates:
        try:
            if p.exists():
                return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
    return []


def _append_action_event(tool_name: str, payload: Dict[str, Any]) -> None:
    for target in (ACTION_EVENTS_PATH, Path("/tmp/supply_chain_action_events.jsonl")):
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"tool": tool_name, **payload}, sort_keys=True) + "\n")
            return
        except Exception:
            continue


def _deterministic_id(prefix: str, *parts: Any) -> str:
    payload = "|".join(str(p) for p in parts if p is not None and p != "")
    digest = hashlib.sha1(payload.encode("utf-8")).hexdigest()[:8].upper() if payload else "00000000"
    return f"{prefix}-{digest}"


def list_systems() -> Dict[str, Any]:
    """Returns connected enterprise systems and solver engines for planogram_merchandising_vision_auditor."""
    return {
        "agent": "planogram_merchandising_vision_auditor",
        "systems": [
            {
                        "id": "gemini_38_flash_shelf_vision",
                        "name": "Vertex AI Gemini 3.8 Flash Dense Retail SKU & Facing Detector",
                        "protocol": "gRPC Multimodal API",
                        "tables": [
                                    "store_shelf_vision_audit_captures"
                        ]
            },
            {
                        "id": "trade_planogram_contract_db",
                        "name": "Enterprise Category Management & Contracted Planogram Registry",
                        "protocol": "REST / BigQuery",
                        "tables": [
                                    "contracted_planogram_templates"
                        ]
            },
            {
                        "id": "sos_compliance_scoring_engine",
                        "name": "Share-of-Shelf (SOS) & Cooler Purity Compliance Scorer",
                        "protocol": "Python Analytics",
                        "tables": [
                                    "shelf_compliance_scoring_ledger"
                        ]
            },
            {
                        "id": "sfa_instore_task_dispatcher",
                        "name": "In-Store Mobile Merchandising Corrective Action Dispatcher",
                        "protocol": "Webhook / Push",
                        "tables": [
                                    "merchandising_corrective_tasks"
                        ]
            }
]
    }

def query_store_shelf_vision_audit_captures(
    capture_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query store_shelf_vision_audit_captures records from gemini_38_flash_shelf_vision."""
    rows = _read_json("store_shelf_vision_audit_captures.json")
    all_rows = list(rows)
    if capture_id:
        rows = [r for r in rows if capture_id.lower() in str(r.get("capture_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "gemini_38_flash_shelf_vision",
        "table": "store_shelf_vision_audit_captures",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_contracted_planogram_templates(
    template_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query contracted_planogram_templates records from trade_planogram_contract_db."""
    rows = _read_json("contracted_planogram_templates.json")
    all_rows = list(rows)
    if template_id:
        rows = [r for r in rows if template_id.lower() in str(r.get("template_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "trade_planogram_contract_db",
        "table": "contracted_planogram_templates",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_shelf_compliance_scoring_ledger(
    outlet_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query shelf_compliance_scoring_ledger records from sos_compliance_scoring_engine."""
    rows = _read_json("shelf_compliance_scoring_ledger.json")
    all_rows = list(rows)
    if outlet_id:
        rows = [r for r in rows if outlet_id.lower() in str(r.get("outlet_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "sos_compliance_scoring_engine",
        "table": "shelf_compliance_scoring_ledger",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_merchandising_corrective_tasks(
    outlet_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query merchandising_corrective_tasks records from sfa_instore_task_dispatcher."""
    rows = _read_json("merchandising_corrective_tasks.json")
    all_rows = list(rows)
    if outlet_id:
        rows = [r for r in rows if outlet_id.lower() in str(r.get("outlet_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "sfa_instore_task_dispatcher",
        "table": "merchandising_corrective_tasks",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_dispatch_instore_restock_directive(
    capture_id: Any,
    outlet_id: Any,
    fso_id: Any,
    missing_facings_count: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_dispatch_instore_restock_directive mutation with deterministic audit logging."""
    action_id = _deterministic_id("SHLF-FIX", capture_id, idempotency_key)
    payload = {
        "dispatch_execution_id": action_id,
        "capture_id": capture_id,
        "outlet_id": outlet_id,
        "fso_id": fso_id,
        "missing_facings_count": missing_facings_count,
        "rationale": rationale,
        "status": "INSTORE_RESTOCK_DIRECTIVE_SENT",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_dispatch_instore_restock_directive", payload)
    return payload


def action_certify_store_planogram_audit(
    outlet_id: Any,
    template_id: Any,
    verified_sos_pct: Any,
    payout_approved: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_certify_store_planogram_audit mutation with deterministic audit logging."""
    action_id = _deterministic_id("SHLF-CRT", outlet_id, idempotency_key)
    payload = {
        "secondary_action_id": action_id,
        "outlet_id": outlet_id,
        "template_id": template_id,
        "verified_sos_pct": verified_sos_pct,
        "payout_approved": payout_approved,
        "rationale": rationale,
        "status": "PLANOGRAM_COMPLIANCE_CERTIFIED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_certify_store_planogram_audit", payload)
    return payload


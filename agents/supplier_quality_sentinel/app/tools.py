"""Deterministic and fixture-backed tools for QualiShield Supplier Quality Sentinel."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

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
    """Returns connected source systems, quality management hubs, and debit ledger engines."""
    return {
        "agent": "supplier_quality_sentinel",
        "systems": [
            {
                "id": "sap_qm_s4hana",
                "name": "SAP S/4HANA Quality Management (QM)",
                "protocol": "BAPI_INSPLOT_SETUSAGEDECISION / OData v4",
                "tables": ["supplier_coa_inspections"],
            },
            {
                "id": "mes_supplier_telemetry",
                "name": "Supplier MES Statistical Process Control (SPC) Sensor Lake",
                "protocol": "BigQuery / MQTT Machine Telemetry Pub/Sub",
                "tables": ["spc_cpk_drift_metrics"],
            },
            {
                "id": "trackwise_etq_capa",
                "name": "TrackWise / ETQ Reliance Enterprise 8D CAPA Engine",
                "protocol": "REST / OpenAPI v3",
                "tables": ["quality_deviation_tickets"],
            },
            {
                "id": "sap_fi_copq_ledger",
                "name": "SAP S/4HANA Finance Cost of Poor Quality (COPQ) Ledger",
                "protocol": "BAPI_ACC_DOCUMENT_POST / EDI 812",
                "tables": ["cost_of_poor_quality_ledger"],
            }
        ]
    }


def query_supplier_coa_inspections(
    inspection_lot_id: str = "",
    po_number: str = "",
    supplier_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query Certificate of Analysis (CoA) lot inspections, thermal/dimension specs, and acceptance status."""
    rows = _read_json("supplier_coa_inspections.json")
    if inspection_lot_id:
        rows = [r for r in rows if inspection_lot_id.lower() in r.get("inspection_lot_id", "").lower()]
    if po_number:
        rows = [r for r in rows if po_number.lower() in r.get("po_number", "").lower()]
    if supplier_id:
        rows = [r for r in rows if supplier_id.lower() in r.get("supplier_id", "").lower()]
    return {
        "source_system": "sap_qm_s4hana",
        "table": "supplier_coa_inspections",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_spc_cpk_drift_metrics(
    part_number: str = "",
    supplier_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query Statistical Process Control (SPC) parameters: Cpk, USL, LSL, UCL, LCL, and defect PPM."""
    rows = _read_json("spc_cpk_drift_metrics.json")
    if part_number:
        rows = [r for r in rows if part_number.lower() in r.get("part_number", "").lower()]
    if supplier_id:
        rows = [r for r in rows if supplier_id.lower() in r.get("supplier_id", "").lower()]
    return {
        "source_system": "mes_supplier_telemetry",
        "table": "spc_cpk_drift_metrics",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_quality_deviation_tickets(
    ticket_id: str = "",
    supplier_id: str = "",
    severity: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query non-conformance records (NCR), 8D containment status, and assigned supplier quality engineers."""
    rows = _read_json("quality_deviation_tickets.json")
    if ticket_id:
        rows = [r for r in rows if ticket_id.lower() in r.get("ticket_id", "").lower()]
    if supplier_id:
        rows = [r for r in rows if supplier_id.lower() in r.get("supplier_id", "").lower()]
    if severity:
        rows = [r for r in rows if severity.lower() in r.get("severity", "").lower()]
    return {
        "source_system": "trackwise_etq_capa",
        "table": "quality_deviation_tickets",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_cost_of_poor_quality_ledger(
    copq_id: str = "",
    supplier_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query itemized Cost of Poor Quality (scrap, sorting labor, assembly downtime) and debit recovery."""
    rows = _read_json("cost_of_poor_quality_ledger.json")
    if copq_id:
        rows = [r for r in rows if copq_id.lower() in r.get("copq_id", "").lower()]
    if supplier_id:
        rows = [r for r in rows if supplier_id.lower() in r.get("supplier_id", "").lower()]
    return {
        "source_system": "sap_fi_copq_ledger",
        "table": "cost_of_poor_quality_ledger",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_quarantine_inspection_lot(
    inspection_lot_id: str,
    supplier_id: str,
    part_number: str,
    quarantine_reason: str,
    plant_id: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute digital quarantine block in SAP QM to prevent delivery of out-of-spec lot to factory lines."""
    quarantine_id = _deterministic_id("QM-BLOCK", inspection_lot_id, plant_id, idempotency_key)
    payload = {
        "quarantine_id": quarantine_id,
        "inspection_lot_id": inspection_lot_id,
        "supplier_id": supplier_id,
        "part_number": part_number,
        "plant_id": plant_id,
        "status": "SAP_QM_QUARANTINED_BLOCKED",
        "quarantine_reason": quarantine_reason,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_quarantine_inspection_lot", payload)
    return payload


def action_trigger_8d_capa_debit(
    ticket_id: str,
    supplier_id: str,
    copq_amount_usd: float,
    capa_root_cause_summary: str,
    accounting_cost_center: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Trigger 8D CAPA workflow in TrackWise and post automated COPQ debit memo in SAP FI."""
    debit_id = _deterministic_id("COPQ-DEBIT", ticket_id, supplier_id, idempotency_key)
    payload = {
        "debit_id": debit_id,
        "ticket_id": ticket_id,
        "supplier_id": supplier_id,
        "copq_amount_usd": copq_amount_usd,
        "accounting_cost_center": accounting_cost_center,
        "status": "SAP_FI_COPQ_DEBIT_POSTED",
        "capa_root_cause_summary": capa_root_cause_summary,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_trigger_8d_capa_debit", payload)
    return payload

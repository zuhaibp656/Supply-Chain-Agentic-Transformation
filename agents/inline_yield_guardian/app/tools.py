"""Deterministic and fixture-backed tools for VisionInspect Inline Quality Inspection Agent."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

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
    """Returns connected source systems, optical vision feeds, and pneumatic reject gates."""
    return {
        "agent": "inline_yield_guardian",
        "systems": [
            {
                "id": "inline_vision_camera_feed",
                "name": "High-Speed Industrial Optical Inspection Camera Array",
                "protocol": "GigE Vision / GenICam / RTSP 120 FPS Stream",
                "tables": ["camera_vision_inspection_frames"],
            },
            {
                "id": "gemini_flash_multimodal_vision",
                "name": "Gemini 3.8 Flash Multimodal Defect Classifier",
                "protocol": "Vertex AI Live Vision / Sub-50ms Inference",
                "tables": ["vision_defect_classification_results"],
            },
            {
                "id": "veeva_qualityone_ebhr",
                "name": "Veeva Vault QualityOne / SAP QM Electronic Batch Record (eBHR)",
                "protocol": "REST / OpenAPI v3 / 21 CFR Part 11 Audit Trail",
                "tables": ["ebhr_batch_record_deviations"],
            },
            {
                "id": "sap_qm_inline_gate",
                "name": "Line 01 High-Speed Solenoid Pneumatic Reject Diverter",
                "protocol": "Modbus TCP / Industrial Ethernet IO-Link",
                "tables": ["pneumatic_reject_gate_events"],
            }
        ]
    }


def query_camera_vision_inspection_frames(
    frame_id: str = "",
    line_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query captured optical inspection frames, conveyor speeds, illumination lux, and SKU codes."""
    rows = _read_json("camera_vision_inspection_frames.json")
    all_rows = list(rows)
    if frame_id:
        rows = [r for r in rows if frame_id.lower() in r.get("frame_id", "").lower()]
    if line_id:
        rows = [r for r in rows if line_id.lower() in r.get("line_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "inline_vision_camera_feed",
        "table": "camera_vision_inspection_frames",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_vision_defect_classification_results(
    classification_id: str = "",
    defect_type: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query Gemini 3.8 Flash Vision model classifications, confidence scores, and bounding boxes."""
    rows = _read_json("vision_defect_classification_results.json")
    all_rows = list(rows)
    if classification_id:
        rows = [r for r in rows if classification_id.lower() in r.get("classification_id", "").lower()]
    if defect_type:
        rows = [r for r in rows if defect_type.lower() in r.get("defect_type", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "gemini_flash_multimodal_vision",
        "table": "vision_defect_classification_results",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_ebhr_batch_record_deviations(
    deviation_id: str = "",
    batch_number: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query electronic Batch Manufacturing Record deviations, Veeva tickets, and SAP QM notification logs."""
    rows = _read_json("ebhr_batch_record_deviations.json")
    all_rows = list(rows)
    if deviation_id:
        rows = [r for r in rows if deviation_id.lower() in r.get("deviation_id", "").lower()]
    if batch_number:
        rows = [r for r in rows if batch_number.lower() in r.get("batch_number", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "veeva_qualityone_ebhr",
        "table": "ebhr_batch_record_deviations",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_pneumatic_reject_gate_events(
    event_id: str = "",
    line_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query physical pneumatic solenoid reject diverter firings, actuation latencies, and sensor confirmations."""
    rows = _read_json("pneumatic_reject_gate_events.json")
    all_rows = list(rows)
    if event_id:
        rows = [r for r in rows if event_id.lower() in r.get("event_id", "").lower()]
    if line_id:
        rows = [r for r in rows if line_id.lower() in r.get("line_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "sap_qm_inline_gate",
        "table": "pneumatic_reject_gate_events",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_trigger_pneumatic_reject_diverter(
    frame_id: str,
    line_id: str,
    pneumatic_diverter_id: str,
    defect_type: str,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Actuate high-speed solenoid pneumatic diverter to route defective product into quarantine bin."""
    divert_id = _deterministic_id("DIVERT-PNEUM", frame_id, line_id, idempotency_key)
    payload = {
        "divert_id": divert_id,
        "frame_id": frame_id,
        "line_id": line_id,
        "pneumatic_diverter_id": pneumatic_diverter_id,
        "defect_type": defect_type,
        "actuation_latency_ms": 14.2,
        "status": "PNEUMATIC_DIVERTER_ACTIVATED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_trigger_pneumatic_reject_diverter", payload)
    return payload


def action_log_ebhr_quality_deviation(
    batch_number: str,
    product_id: str,
    deviation_type: str,
    severity: str,
    station_id: str,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Log formal electronic Batch Manufacturing Record (eBHR) deviation ticket in Veeva Vault / SAP QM."""
    deviation_log_id = _deterministic_id("DEV-LOG-EBHR", batch_number, deviation_type, idempotency_key)
    payload = {
        "deviation_log_id": deviation_log_id,
        "batch_number": batch_number,
        "product_id": product_id,
        "deviation_type": deviation_type,
        "severity": severity,
        "station_id": station_id,
        "veeva_ticket_id": f"VEEVA-QMS-{deviation_log_id[-6:]}",
        "status": "EBHR_DEVIATION_LOGGED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_log_ebhr_quality_deviation", payload)
    return payload

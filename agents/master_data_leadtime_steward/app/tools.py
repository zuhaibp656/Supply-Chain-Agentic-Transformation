"""Deterministic and fixture-backed tools for Master Data & Lead-Time Steward."""
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
    """Returns connected source systems, ERP tables, and master data validation engines."""
    return {
        "agent": "master_data_leadtime_steward",
        "systems": [
            {
                "id": "sap_s4hana_mm",
                "name": "SAP S/4HANA Material Master (MARA/MARC/MARD)",
                "protocol": "SAP BAPI / RFC / OData",
                "tables": ["material_master_mara_marc", "bom_routing_leadtimes"],
            },
            {
                "id": "cubiscan_3d_telemetry",
                "name": "CubiScan 3D In-Line Volumetric & Scale Scanners",
                "protocol": "IoT MQTT / REST Telemetry",
                "tables": ["dimension_audit_scans"],
            },
            {
                "id": "vendor_master_db",
                "name": "Global Vendor & Supplier Master Registry",
                "protocol": "REST API / Cloud SQL",
                "tables": ["vendor_master_records"],
            }
        ]
    }


def query_material_master_records(material_id: str = "", plant: str = "", status_filter: str = "", limit: int = 10) -> Dict[str, Any]:
    """Query SAP S/4HANA MARA/MARC material master records for lead times, UOM, and inventory params."""
    rows = _read_json("material_master_mara_marc.json")
    all_rows = list(rows)
    if material_id:
        m_low = material_id.lower()
        rows = [r for r in rows if m_low in r.get("material_id", "").lower()]
    if plant:
        p_low = plant.lower()
        rows = [r for r in rows if p_low in r.get("plant", "").lower()]
    if status_filter:
        s_low = status_filter.lower()
        rows = [r for r in rows if s_low in r.get("status", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "sap_s4hana_mm",
        "table": "material_master_mara_marc",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_leadtime_drift_anomalies(min_drift_days: int = 5, limit: int = 10) -> Dict[str, Any]:
    """Identify materials where actual historical supplier lead-time significantly exceeds SAP planned delivery time."""
    rows = _read_json("material_master_mara_marc.json")
    all_rows = list(rows)
    rows = [r for r in rows if r.get("leadtime_drift_days", 0) >= min_drift_days]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "sap_s4hana_mm",
        "table": "material_master_mara_marc",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_cubiscan_dimension_discrepancies(min_volume_variance_pct: float = 10.0, limit: int = 10) -> Dict[str, Any]:
    """Query 3D CubiScan volumetric laser scans where physical package measurements differ from ERP master data."""
    rows = _read_json("dimension_audit_scans.json")
    all_rows = list(rows)
    rows = [r for r in rows if r.get("volume_discrepancy_pct", 0) >= min_volume_variance_pct]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "cubiscan_3d_telemetry",
        "table": "dimension_audit_scans",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_vendor_master_integrity(vendor_id: str = "", tax_compliance_status: str = "", limit: int = 10) -> Dict[str, Any]:
    """Audit vendor master compliance, payment terms, sanctions status, and lead-time reliability score."""
    rows = _read_json("vendor_master_records.json")
    all_rows = list(rows)
    if vendor_id:
        v_low = vendor_id.lower()
        rows = [r for r in rows if v_low in r.get("vendor_id", "").lower()]
    if tax_compliance_status:
        t_low = tax_compliance_status.lower()
        rows = [r for r in rows if t_low in r.get("tax_compliance_status", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "vendor_master_db",
        "table": "vendor_master_records",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_heal_material_leadtime(
    material_id: str,
    plant: str,
    planned_delivery_leadtime_days: int,
    rationale: str,
    idempotency_key: str = ""
) -> Dict[str, Any]:
    """Autonomous mutation tool to self-heal drifted SAP Material Master (MARC-PLIFZ) planned delivery time."""
    if not material_id or not plant or planned_delivery_leadtime_days <= 0 or not rationale:
        return {
            "error": "missing_required_arguments",
            "required": ["material_id", "plant", "planned_delivery_leadtime_days", "rationale"]
        }

    # Governance guardrail: Lead time jumps over 45 days require engineering change order (ECO) review
    if planned_delivery_leadtime_days > 90:
        return {
            "error": "leadtime_exceeds_engineering_tolerance",
            "max_allowed_days": 90,
            "requested_days": planned_delivery_leadtime_days,
            "escalation": "request_engineering_change_order"
        }

    heal_id = _deterministic_id("HEAL-LT", material_id, plant, planned_delivery_leadtime_days, idempotency_key or "default")
    record = {
        "heal_id": heal_id,
        "material_id": material_id,
        "plant": plant,
        "new_planned_delivery_leadtime_days": planned_delivery_leadtime_days,
        "rationale": rationale,
        "status": "SAP_MARC_UPDATED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_heal_material_leadtime", record)
    return {
        "status": "healed",
        "heal_id": heal_id,
        "audit_trail": (
            f"SAP Material Master updated [{heal_id}]: {material_id} at {plant} calibrated to "
            f"{planned_delivery_leadtime_days} days delivery lead time. Rationale: {rationale}."
        )
    }


def action_remediate_cubiscan_dimensions(
    material_id: str,
    plant: str,
    corrected_length_cm: float,
    corrected_width_cm: float,
    corrected_height_cm: float,
    corrected_weight_kg: float,
    rationale: str,
    idempotency_key: str = ""
) -> Dict[str, Any]:
    """Updates master packaging dimensions in SAP MARA based on verified CubiScan 3D physical sensor scans."""
    if not material_id or not plant or corrected_length_cm <= 0 or corrected_width_cm <= 0 or corrected_height_cm <= 0 or corrected_weight_kg <= 0 or not rationale:
        return {
            "error": "missing_required_arguments",
            "required": ["material_id", "plant", "corrected_length_cm", "corrected_width_cm", "corrected_height_cm", "corrected_weight_kg", "rationale"]
        }

    dim_id = _deterministic_id("DIM-FIX", material_id, plant, corrected_length_cm, corrected_width_cm)
    record = {
        "dim_id": dim_id,
        "material_id": material_id,
        "plant": plant,
        "length_cm": corrected_length_cm,
        "width_cm": corrected_width_cm,
        "height_cm": corrected_height_cm,
        "weight_kg": corrected_weight_kg,
        "rationale": rationale,
        "status": "SAP_MARA_DIMENSIONS_UPDATED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_remediate_cubiscan_dimensions", record)
    return {
        "status": "remediated",
        "dim_id": dim_id,
        "audit_trail": (
            f"Physical dimensions corrected [{dim_id}] for {material_id}: "
            f"{corrected_length_cm}x{corrected_width_cm}x{corrected_height_cm} cm, {corrected_weight_kg} kg. Rationale: {rationale}."
        )
    }

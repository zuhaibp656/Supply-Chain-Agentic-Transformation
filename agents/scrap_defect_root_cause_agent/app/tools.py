"""Deterministic and fixture-backed tools for YieldMax Scrap Defect Root-Cause Agent."""
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
    """Returns connected source systems, MES scrap telemetry lakes, and SCADA PLC writeback interfaces."""
    return {
        "agent": "scrap_defect_root_cause_agent",
        "systems": [
            {
                "id": "mes_scrap_loss_pareto",
                "name": "Siemens Opcenter MES Scrap Loss Pareto Lake",
                "protocol": "BigQuery Analytics / OPC UA Machine Telemetry",
                "tables": ["scrap_loss_pareto_records"],
            },
            {
                "id": "batch_execution_telemetry",
                "name": "MES Batch Execution Sensor Multivariate Telemetry",
                "protocol": "TimesFM / BigQuery ML Regression Engine",
                "tables": ["batch_process_parameter_correlations"],
            },
            {
                "id": "sap_co_scrap_ledger",
                "name": "SAP S/4HANA Controlling (CO) Scrap & Yield Variance Ledger",
                "protocol": "BAPI_ACC_DOCUMENT_POST / OData v4",
                "tables": ["scrap_financial_cost_ledger"],
            },
            {
                "id": "scada_setpoint_bridge",
                "name": "SCADA / Rockwell FactoryTalk Recipe Setpoint Bridge",
                "protocol": "EtherNet/IP / OPC UA Setpoint Writeback",
                "tables": ["scada_setpoint_recommendations"],
            }
        ]
    }


def query_scrap_loss_pareto_records(
    defect_id: str = "",
    asset_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query scrap loss Pareto distribution, scrap rates, defect codes, and cumulative impact."""
    rows = _read_json("scrap_loss_pareto_records.json")
    if defect_id:
        rows = [r for r in rows if defect_id.lower() in r.get("defect_id", "").lower()]
    if asset_id:
        rows = [r for r in rows if asset_id.lower() in r.get("asset_id", "").lower()]
    return {
        "source_system": "mes_scrap_loss_pareto",
        "table": "scrap_loss_pareto_records",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_batch_process_parameter_correlations(
    defect_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query multivariate regression coefficients, p-values, setpoint offsets, and identified root causes."""
    rows = _read_json("batch_process_parameter_correlations.json")
    if defect_id:
        rows = [r for r in rows if defect_id.lower() in r.get("defect_id", "").lower()]
    return {
        "source_system": "batch_execution_telemetry",
        "table": "batch_process_parameter_correlations",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_scrap_financial_cost_ledger(
    ledger_id: str = "",
    asset_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query itemized scrap financial loss, material/conversion expense, and SAP cost center assignments."""
    rows = _read_json("scrap_financial_cost_ledger.json")
    if ledger_id:
        rows = [r for r in rows if ledger_id.lower() in r.get("ledger_id", "").lower()]
    if asset_id:
        rows = [r for r in rows if asset_id.lower() in r.get("asset_id", "").lower()]
    return {
        "source_system": "sap_co_scrap_ledger",
        "table": "scrap_financial_cost_ledger",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_scada_setpoint_recommendations(
    asset_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query machine recipe setpoint adjustment recommendations, projected yield gains, and PLC tags."""
    rows = _read_json("scada_setpoint_recommendations.json")
    if asset_id:
        rows = [r for r in rows if asset_id.lower() in r.get("asset_id", "").lower()]
    return {
        "source_system": "scada_setpoint_bridge",
        "table": "scada_setpoint_recommendations",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_update_scada_recipe_setpoints(
    recommendation_id: str,
    asset_id: str,
    recipe_name: str,
    parameter_updates: Dict[str, float],
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Write back optimized process recipe setpoints directly into shopfloor SCADA / PLC controller."""
    writeback_id = _deterministic_id("SCADA-SET", recommendation_id, asset_id, idempotency_key)
    payload = {
        "writeback_id": writeback_id,
        "recommendation_id": recommendation_id,
        "asset_id": asset_id,
        "recipe_name": recipe_name,
        "parameter_updates": parameter_updates,
        "status": "SCADA_PLC_SETPOINTS_LOCKED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_update_scada_recipe_setpoints", payload)
    return payload


def action_post_scrap_variance_adjustment(
    ledger_id: str,
    asset_id: str,
    financial_loss_usd: float,
    cost_center: str,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Post scrap variance adjustment and financial write-off to SAP S/4HANA Controlling (CO)."""
    posting_id = _deterministic_id("SAP-CO-SCRAP", ledger_id, cost_center, idempotency_key)
    payload = {
        "posting_id": posting_id,
        "ledger_id": ledger_id,
        "asset_id": asset_id,
        "financial_loss_usd": financial_loss_usd,
        "cost_center": cost_center,
        "status": "SAP_CO_VARIANCE_POSTED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_post_scrap_variance_adjustment", payload)
    return payload

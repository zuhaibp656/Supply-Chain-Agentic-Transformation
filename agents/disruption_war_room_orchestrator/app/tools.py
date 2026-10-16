"""Deterministic and fixture-backed tools for Disruption War Room Orchestrator."""
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
    """Returns connected source systems, tables, and integration protocols."""
    return {
        "agent": "disruption_war_room_orchestrator",
        "systems": [
            {
                "id": "weather_apis",
                "name": "Google WeatherNext 3 & NOAA APIs",
                "protocol": "REST API",
                "tables": ["weather_alerts"],
            },
            {
                "id": "maritime_ais",
                "name": "Spire Global Satellite AIS Maritime Feed",
                "protocol": "Streaming GeoJSON / AIS Hub",
                "tables": ["maritime_ais_vessels"],
            },
            {
                "id": "resilinc",
                "name": "Resilinc Multi-Tier Supplier Risk Intelligence",
                "protocol": "Spanner Graph / REST API",
                "tables": ["supplier_facilities"],
            },
            {
                "id": "google_news_api",
                "name": "Global Trade & Natural Disaster News Ingestion",
                "protocol": "RSS / PubSub / Vertex AI NLP",
                "tables": ["news_disruptions"],
            },
            {
                "id": "servicenow_warroom",
                "name": "Enterprise Incident War Room & Ops Desk",
                "protocol": "REST API / Webhook",
                "tables": ["incident_war_rooms"],
            }
        ]
    }


def query_weather_alerts(region: str = "", severity: str = "", limit: int = 10) -> Dict[str, Any]:
    """Query real-time meteorological alerts and weather hazard polygons."""
    rows = _read_json("weather_alerts.json")
    if region:
        r_low = region.lower()
        rows = [r for r in rows if r_low in r.get("region", "").lower() or r_low in str(r.get("affected_corridors", "")).lower()]
    if severity:
        rows = [r for r in rows if severity.upper() == r.get("severity", "").upper()]
    return {
        "source_system": "weather_apis",
        "table": "weather_alerts",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_maritime_ais_vessels(vessel_name: str = "", destination_port: str = "", limit: int = 10) -> Dict[str, Any]:
    """Query satellite AIS maritime positions, ETA slippage, and at-risk customer purchase orders."""
    rows = _read_json("maritime_ais_vessels.json")
    if vessel_name:
        v_low = vessel_name.lower()
        rows = [r for r in rows if v_low in r.get("vessel_name", "").lower()]
    if destination_port:
        p_low = destination_port.lower()
        rows = [r for r in rows if p_low in r.get("destination_port", "").lower()]
    return {
        "source_system": "maritime_ais",
        "table": "maritime_ais_vessels",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_resilinc_supplier_facilities(supplier_name: str = "", country: str = "", tier_level: Optional[int] = None, limit: int = 10) -> Dict[str, Any]:
    """Query Tier-1 to Tier-N supplier manufacturing nodes, single-source flags, and revenue impact."""
    rows = _read_json("supplier_facilities.json")
    if supplier_name:
        s_low = supplier_name.lower()
        rows = [r for r in rows if s_low in r.get("supplier_name", "").lower() or s_low in r.get("facility_name", "").lower()]
    if country:
        c_low = country.lower()
        rows = [r for r in rows if c_low in r.get("country", "").lower()]
    if tier_level is not None:
        rows = [r for r in rows if r.get("tier_level") == tier_level]
    return {
        "source_system": "resilinc",
        "table": "supplier_facilities",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_news_disruptions(lookup_key: str = "", limit: int = 10) -> Dict[str, Any]:
    """Query NLP-parsed news signals covering strikes, factory fires, and geopolitical trade sanctions."""
    rows = _read_json("news_disruptions.json")
    if lookup_key:
        needle = lookup_key.lower()
        rows = [r for r in rows if needle in r.get("headline", "").lower() or needle in r.get("summary", "").lower() or needle in str(r.get("entities_extracted", "")).lower()]
    return {
        "source_system": "google_news_api",
        "table": "news_disruptions",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_create_war_room_incident(
    title: str,
    severity: str,
    affected_lanes: List[str],
    action_plan: str,
    owner: str = "Director of Global Supply Chain",
    idempotency_key: str = ""
) -> Dict[str, Any]:
    """Autonomous mutation tool to instantiate an executive crisis war room and broadcast remediation milestones."""
    if not title or not severity or not action_plan:
        return {"error": "missing_required_arguments", "required": ["title", "severity", "action_plan"]}
    
    incident_id = _deterministic_id("INC-WR", title, severity, idempotency_key or "default")
    record = {
        "incident_id": incident_id,
        "title": title,
        "severity": severity.upper(),
        "owner": owner,
        "affected_lanes": affected_lanes,
        "action_plan": action_plan,
        "status": "ACTIVE_TRIAGE",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_create_war_room_incident", record)
    return {
        "status": "created",
        "incident_id": incident_id,
        "audit_trail": f"War room '{title}' initialized [{incident_id}] with severity {severity}. Lead assigned to {owner}."
    }


def action_dispatch_expedite_remediation(
    incident_id: str,
    target_po: str,
    expedite_mode: str,
    rationale: str,
    idempotency_key: str = ""
) -> Dict[str, Any]:
    """Dispatches emergency mode-shift (e.g., Air Charter or Express Dedicated Shuttle) to prevent plant shutdown."""
    if not incident_id or not target_po or not expedite_mode or not rationale:
        return {"error": "missing_required_arguments", "required": ["incident_id", "target_po", "expedite_mode", "rationale"]}
    
    dispatch_id = _deterministic_id("EXP", incident_id, target_po, expedite_mode)
    record = {
        "dispatch_id": dispatch_id,
        "incident_id": incident_id,
        "target_po": target_po,
        "expedite_mode": expedite_mode,
        "rationale": rationale,
        "status": "DISPATCHED_TO_CARRIER",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_dispatch_expedite_remediation", record)
    return {
        "status": "dispatched",
        "dispatch_id": dispatch_id,
        "audit_trail": f"Emergency freight order {dispatch_id} triggered for {target_po} via {expedite_mode}. Rationale: {rationale}."
    }

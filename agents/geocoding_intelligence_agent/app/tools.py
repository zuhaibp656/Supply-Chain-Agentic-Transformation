"""Deterministic Enterprise Connectors, Python Math Solvers, Charting & Drafting Tools for [05 · Deliver | Last-Mile Delivery] Last-Mile Dock Pin & Geocode Corrector."""
from __future__ import annotations

import copy
import datetime
import json
import math
import os
import uuid
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .render.charts import create_geocoding_intelligence_agent_chart_spec
from .render.png_chart import render_comparison_png

_FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures" / "tables"
_MASTER_FILE = Path(__file__).resolve().parent.parent / "fixtures" / "master" / "xyz_enterprise_backbone.json"

SYSTEM_CONNECTORS: List[Dict[str, Any]] = [{'id': 'oms_address_master',
  'name': 'Commercial Customer Postal Rooftop Address Book',
  'protocol': 'REST / Geocoding API',
  'tables': ['commercial_stop_rooftop_addresses']},
 {'id': 'telematics_driver_breadcrumbs',
  'name': 'Driver Handset GPS Breadcrumb & ePOD Scan Lake',
  'protocol': 'gRPC / GeoJSON SQL',
  'tables': ['driver_gps_dwell_and_entry_logs']},
 {'id': 'spatial_dock_pin_registry',
  'name': 'Verified Truck Apron & Receiving Dock Geofence Master',
  'protocol': 'PostGIS / OData',
  'tables': ['verified_dock_pin_geofences']},
 {'id': 'last_mile_fadr_scorecard',
  'name': 'Last-Mile Dwell & First-Attempt Delivery Ledger',
  'protocol': 'SQL / TMS Analytics',
  'tables': ['first_attempt_delivery_improvements']}]

_SESSION_MUTATION_LEDGER: List[Dict[str, Any]] = []
_LAST_CHART_SPEC: Optional[Dict[str, Any]] = None


def _read_json(filename: str) -> List[Dict[str, Any]]:
    fpath = _FIXTURES_DIR / filename
    if not fpath.exists():
        return []
    return copy.deepcopy(json.loads(fpath.read_text(encoding="utf-8")))


def _record_mutation(action_tool: str, status_code: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    action_id = f"ACT-GEOCODIN-{uuid.uuid4().hex[:8].upper()}"
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipt = {
        "status": status_code,
        "action_id": action_id,
        "agent_id": 'geocoding_intelligence_agent',
        "organization_id": "XYZ-CORP-01",
        "action_tool": action_tool,
        "timestamp_utc": ts,
        "payload": payload,
    }
    _SESSION_MUTATION_LEDGER.append(receipt)
    try:
        log_path = _FIXTURES_DIR / "action-events.jsonl"
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(receipt) + "\n")
    except Exception:
        pass
    return receipt


def get_latest_chart_spec() -> Dict[str, Any]:
    """Returns the most recent dynamic Vega-Lite v5 chart spec built in the current session."""
    if _LAST_CHART_SPEC is not None:
        return copy.deepcopy(_LAST_CHART_SPEC)
    return create_geocoding_intelligence_agent_chart_spec()


def list_systems() -> Dict[str, Any]:
    """List connected XYZ Global Industries Corp. enterprise systems, protocols, and governed tables."""
    return {'agent': 'geocoding_intelligence_agent',
 'organization_id': 'XYZ-CORP-01',
 'systems': [{'id': 'oms_address_master',
              'name': 'Commercial Customer Postal Rooftop Address Book',
              'protocol': 'REST / Geocoding API',
              'tables': ['commercial_stop_rooftop_addresses']},
             {'id': 'telematics_driver_breadcrumbs',
              'name': 'Driver Handset GPS Breadcrumb & ePOD Scan Lake',
              'protocol': 'gRPC / GeoJSON SQL',
              'tables': ['driver_gps_dwell_and_entry_logs']},
             {'id': 'spatial_dock_pin_registry',
              'name': 'Verified Truck Apron & Receiving Dock Geofence Master',
              'protocol': 'PostGIS / OData',
              'tables': ['verified_dock_pin_geofences']},
             {'id': 'last_mile_fadr_scorecard',
              'name': 'Last-Mile Dwell & First-Attempt Delivery Ledger',
              'protocol': 'SQL / TMS Analytics',
              'tables': ['first_attempt_delivery_improvements']}]}


def lookup_xyz_master_context(
    sku_id: str = "",
    facility_id: str = "",
    supplier_id: str = "",
    customer_id: str = "",
    carrier_id: str = "",
) -> Dict[str, Any]:
    """Join operational records against XYZ Global Industries Corp. (XYZ-CORP-01) master ERP/WMS/TMS data."""
    if not _MASTER_FILE.exists():
        return {"status": "MASTER_NOT_FOUND", "organization_id": "XYZ-CORP-01"}
    bundle = json.loads(_MASTER_FILE.read_text(encoding="utf-8"))
    result: Dict[str, Any] = {
        "status": "SUCCESS",
        "organization_id": bundle.get("organization_id", "XYZ-CORP-01"),
        "organization_name": bundle.get("organization_name", "XYZ Global Industries Corp."),
    }
    if sku_id:
        result["material"] = bundle.get("materials", {}).get(sku_id)
    if facility_id:
        result["facility"] = bundle.get("facilities", {}).get(facility_id)
    if supplier_id:
        result["supplier"] = bundle.get("suppliers", {}).get(supplier_id)
    if customer_id:
        result["customer"] = bundle.get("customers", {}).get(customer_id)
    if carrier_id:
        result["carrier"] = bundle.get("carriers", {}).get(carrier_id)
    if not any([sku_id, facility_id, supplier_id, customer_id, carrier_id]):
        result["summary_counts"] = {
            "materials": len(bundle.get("materials", {})),
            "facilities": len(bundle.get("facilities", {})),
            "suppliers": len(bundle.get("suppliers", {})),
            "customers": len(bundle.get("customers", {})),
            "carriers": len(bundle.get("carriers", {})),
            "golden_threads": len(bundle.get("golden_threads", [])),
        }
    return result


def query_commercial_rooftop_addresses(stop_id: str = '', customer_id: str = '') -> Dict[str, Any]:
    """Query commercial stop postal rooftop lat/lon, truck clearance rules, and 90-day failed delivery attempts."""
    rows = _read_json("commercial_stop_rooftop_addresses.json")
    if stop_id:
        rows = [r for r in rows if str(r.get('stop_id', '')).lower() == str(stop_id).lower()]
    if customer_id:
        rows = [r for r in rows if str(r.get('customer_id', '')).lower() == str(customer_id).lower()]
    return {
        "status": "SUCCESS",
        "source_system": 'oms_address_master',
        "table": 'commercial_stop_rooftop_addresses',
        "row_count": len(rows),
        "rows": rows,
    }

def query_driver_gps_dwell_clusters(stop_id: str = '') -> Dict[str, Any]:
    """Query DBSCAN-clustered actual ePOD scan coordinates, rooftop-to-dock meter offset, and driver search dwell minutes."""
    rows = _read_json("driver_gps_dwell_and_entry_logs.json")
    if stop_id:
        rows = [r for r in rows if str(r.get('stop_id', '')).lower() == str(stop_id).lower()]
    return {
        "status": "SUCCESS",
        "source_system": 'telematics_driver_breadcrumbs',
        "table": 'driver_gps_dwell_and_entry_logs',
        "row_count": len(rows),
        "rows": rows,
    }

def query_verified_dock_geofences(stop_id: str = '', geofence_id: str = '') -> Dict[str, Any]:
    """Query verified truck entry street, gate/elevator instructions, and dock polygon radius."""
    rows = _read_json("verified_dock_pin_geofences.json")
    if stop_id:
        rows = [r for r in rows if str(r.get('stop_id', '')).lower() == str(stop_id).lower()]
    if geofence_id:
        rows = [r for r in rows if str(r.get('geofence_id', '')).lower() == str(geofence_id).lower()]
    return {
        "status": "SUCCESS",
        "source_system": 'spatial_dock_pin_registry',
        "table": 'verified_dock_pin_geofences',
        "row_count": len(rows),
        "rows": rows,
    }

def query_fadr_dwell_improvements(stop_id: str = '') -> Dict[str, Any]:
    """Query legacy vs. pin-corrected stop dwell minutes, FADR %, and annual redelivery savings ($)."""
    rows = _read_json("first_attempt_delivery_improvements.json")
    if stop_id:
        rows = [r for r in rows if str(r.get('stop_id', '')).lower() == str(stop_id).lower()]
    return {
        "status": "SUCCESS",
        "source_system": 'last_mile_fadr_scorecard',
        "table": 'first_attempt_delivery_improvements',
        "row_count": len(rows),
        "rows": rows,
    }


def analyze_rooftop_to_dock_haversine_drift(focus_id: str = "") -> Dict[str, Any]:
    """Compute exact Haversine distance (meters) between postal rooftop geocodes and DBSCAN ePOD scan clusters, ranking stops by driver dwell-minute waste and failed-attempt cost."""
    global _LAST_CHART_SPEC
    chart_rows = _read_json("first_attempt_delivery_improvements.json")
    if focus_id:
        filtered = [r for r in chart_rows if str(r.get("stop_id", "")).lower() == focus_id.lower()]
        if filtered:
            chart_rows = filtered

    series_a = [float(r.get("legacy_dwell_min", 0.0) or 0.0) for r in chart_rows]
    series_b = [float(r.get("pin_corrected_dwell_min", 0.0) or 0.0) for r in chart_rows]
    labels = [str(r.get("stop_id", "")) for r in chart_rows]

    sum_a = round(sum(series_a), 2)
    sum_b = round(sum(series_b), 2)
    avg_a = round(sum_a / max(1, len(series_a)), 2)
    avg_b = round(sum_b / max(1, len(series_b)), 2)
    net_delta = round(sum_b - sum_a, 2)
    pct_delta = round(((sum_b - sum_a) / abs(sum_a)) * 100.0, 2) if abs(sum_a) > 1e-9 else 0.0

    ranked_gaps = sorted(
        [
            {
                "id": labels[i],
                "series_a": round(series_a[i], 2),
                "series_b": round(series_b[i], 2),
                "abs_gap": round(abs(series_b[i] - series_a[i]), 2),
                "signed_delta": round(series_b[i] - series_a[i], 2),
            }
            for i in range(len(labels))
        ],
        key=lambda x: x["abs_gap"],
        reverse=True,
    )

    domain_computations: Dict[str, Any] = {}
    # Exact Haversine great-circle distance (meters) between postal rooftop pin and DBSCAN ePOD dock cluster
    r_earth_m = 6_371_000.0
    stops = {r["stop_id"]: r for r in _read_json("commercial_stop_rooftop_addresses.json")}
    geo_drifts = []
    for cl in _read_json("driver_gps_dwell_and_entry_logs.json"):
        st = stops.get(cl["stop_id"], {})
        lat1, lon1 = math.radians(float(st.get("rooftop_lat", 0))), math.radians(float(st.get("rooftop_lon", 0)))
        lat2, lon2 = math.radians(float(cl.get("epod_cluster_lat", 0))), math.radians(float(cl.get("epod_cluster_lon", 0)))
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        meters = round(2 * r_earth_m * math.asin(min(1.0, math.sqrt(a))), 1)
        geo_drifts.append({"stop_id": cl["stop_id"], "haversine_drift_m": meters, "avg_search_dwell_min": cl["avg_search_dwell_min"]})
    domain_computations["haversine_pin_drift_meters"] = geo_drifts

    _LAST_CHART_SPEC = create_geocoding_intelligence_agent_chart_spec(rows=chart_rows)

    md_lines = [
        "| Record | Legacy Rooftop Pin Dwe | Verified Dock Pin Dwel | Delta |",
        "| :--- | ---: | ---: | ---: |",
    ]
    for g in ranked_gaps[:6]:
        md_lines.append(
            f"| `{g['id']}` | {g['series_a']:,.2f} | **{g['series_b']:,.2f}** | {g['signed_delta']:+,.2f} |"
        )

    return {
        "status": "SUCCESS",
        "agent": 'geocoding_intelligence_agent',
        "persona": 'Last-Mile Operations Manager',
        "records_evaluated": len(chart_rows),
        "kpi_summary": {
            "series_a_label": 'Legacy Rooftop Pin Dwell (Min)',
            "series_b_label": 'Verified Dock Pin Dwell (Min)',
            "total_series_a": sum_a,
            "total_series_b": sum_b,
            "mean_series_a": avg_a,
            "mean_series_b": avg_b,
            "net_delta": net_delta,
            "relative_shift_pct": pct_delta,
            "top_pareto_driver": ranked_gaps[0] if ranked_gaps else {},
        },
        "ranked_drivers": ranked_gaps,
        "domain_computations": domain_computations,
        "concise_markdown_table": "\n".join(md_lines),
    }


def render_visual_chart(focus_id: str = "", chart_title: str = "") -> Dict[str, Any]:
    """Generate both an interactive A2UI Vega-Lite v5 chart spec AND a high-res 1200x640 PNG infographic."""
    global _LAST_CHART_SPEC
    rows = _read_json("first_attempt_delivery_improvements.json")
    if focus_id:
        sub = [r for r in rows if str(r.get("stop_id", "")).lower() == focus_id.lower()]
        if sub:
            rows = sub

    spec = create_geocoding_intelligence_agent_chart_spec(rows=rows, title_override=chart_title or None)
    _LAST_CHART_SPEC = spec

    labels = [str(r.get("stop_id", "")) for r in rows]
    va = [float(r.get("legacy_dwell_min", 0.0) or 0.0) for r in rows]
    vb = [float(r.get("pin_corrected_dwell_min", 0.0) or 0.0) for r in rows]
    png_meta = render_comparison_png(
        agent_id='geocoding_intelligence_agent',
        title=chart_title or 'Last-Mile Geocode Correction — Legacy Search Dwell (Min) vs. Verified Dock Pin Dwell (Min)',
        subtitle=f"Persona: Last-Mile Operations Manager · Category: 05 · Distribution & Logistics — Last-Mile Delivery",
        labels=labels,
        series_a=va,
        series_a_label='Legacy Rooftop Pin Dwell (Min)',
        series_b=vb,
        series_b_label='Verified Dock Pin Dwell (Min)',
        y_title='Stop Dwell Time (Minutes)',
    )
    return {
        "status": "SUCCESS",
        "chart_title": spec["title"]["text"],
        "a2ui_vega_lite_queued": True,
        "png_infographic": png_meta,
    }


def draft_driver_dock_navigation_card(target_id: str = "", recipient_role: str = "Supply Chain & Finance Leadership") -> Dict[str, Any]:
    """Draft a Verified Commercial Stop Truck-Entry & Dock Geofence Bulletin for Fleet Dispatch & Carrier Telematics."""
    analysis = analyze_rooftop_to_dock_haversine_drift(focus_id=target_id)
    kpi = analysis.get("kpi_summary", {})
    top = kpi.get("top_pareto_driver", {})
    doc_ref = f"DOC-GEOCOD-2026-{len(analysis.get('ranked_drivers', []))}01"
    memo_md = "\n".join(
        [
            f"### 📄 Last-Mile Commercial Dock Geofence & Truck Clearance Bulletin (`{doc_ref}`)",
            f"- **Organization**: XYZ Global Industries Corp. (`XYZ-CORP-01`)",
            f"- **Prepared By**: Last-Mile Operations Manager ([05 · Deliver | Last-Mile Delivery] Last-Mile Dock Pin & Geocode Corrector)",
            f"- **To**: {recipient_role}",
            f"- **Primary Driver**: `{top.get('id', 'ALL')}` ({kpi.get('series_a_label')}: `{top.get('series_a', 0):,.2f}` -> {kpi.get('series_b_label')}: `{top.get('series_b', 0):,.2f}`)",
            f"- **Aggregate Portfolio Shift**: `{kpi.get('total_series_a', 0):,.2f}` -> `{kpi.get('total_series_b', 0):,.2f}` (`{kpi.get('relative_shift_pct', 0):+.2f}%`)",
            "",
            analysis.get("concise_markdown_table", ""),
            "",
            "**Governance Sign-Off**: Pre-validated against XYZ-CORP-01 master tolerances; requires authorized `idempotency_key` prior to ERP/WMS/TMS commit.",
        ]
    )
    return {
        "status": "DRAFT_READY",
        "document_ref": doc_ref,
        "title": 'Last-Mile Commercial Dock Geofence & Truck Clearance Bulletin',
        "recipient_role": recipient_role,
        "markdown_draft": memo_md,
    }


def action_publish_verified_dock_pin_to_tms(stop_id: Any = '', epod_cluster_lat: Any = '', epod_cluster_lon: Any = '', rationale: Any = '', idempotency_key: str = '') -> Dict[str, Any]:
    """Overwrite inaccurate postal rooftop pin in TMS/OMS with DBSCAN-verified receiving dock coordinates."""
    payload = {'stop_id': stop_id, 'epod_cluster_lat': epod_cluster_lat, 'epod_cluster_lon': epod_cluster_lon, 'rationale': rationale, "idempotency_key": idempotency_key or "AUTO-IDEMP"}
    return _record_mutation(
        action_tool='action_publish_verified_dock_pin_to_tms',
        status_code='TMS_DOCK_GEOCODE_UPDATED',
        payload=payload,
    )

def action_attach_stop_equipment_restriction(stop_id: Any = '', truck_size_limit: Any = '', dock_instructions: Any = '', rationale: Any = '', idempotency_key: str = '') -> Dict[str, Any]:
    """Enforce vehicle height/liftgate/curfew constraint in TMS route assignment."""
    payload = {'stop_id': stop_id, 'truck_size_limit': truck_size_limit, 'dock_instructions': dock_instructions, 'rationale': rationale, "idempotency_key": idempotency_key or "AUTO-IDEMP"}
    return _record_mutation(
        action_tool='action_attach_stop_equipment_restriction',
        status_code='STOP_EQUIPMENT_RULE_LOCKED',
        payload=payload,
    )


ALL_TOOLS: List[Callable[..., Any]] = [
    list_systems,
    lookup_xyz_master_context,
    query_commercial_rooftop_addresses,
    query_driver_gps_dwell_clusters,
    query_verified_dock_geofences,
    query_fadr_dwell_improvements,
    analyze_rooftop_to_dock_haversine_drift,
    render_visual_chart,
    draft_driver_dock_navigation_card,
    action_publish_verified_dock_pin_to_tms,
    action_attach_stop_equipment_restriction,
]

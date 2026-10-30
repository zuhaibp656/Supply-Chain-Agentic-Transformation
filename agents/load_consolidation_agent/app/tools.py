"""Deterministic and fixture-backed tools for CubeMaster 3D — Isometric LIFO Bay & Load Consolidation Studio."""
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
    """Returns connected enterprise systems and solver engines for load_consolidation_agent."""
    return {
        "agent": "load_consolidation_agent",
        "systems": [
            {
                        "id": "or_tools_3d_voxel_packer",
                        "name": "Google OR-Tools 3D Extreme-Point & Guillotine Bin Packing Solver",
                        "protocol": "C++ / Python 3D Voxel Engine",
                        "tables": [
                                    "lifo_3d_voxel_load_plans"
                        ]
            },
            {
                        "id": "sap_ewm_carton_master",
                        "name": "SAP EWM & Material Master 3D Carton Geometry & Fragility Feed",
                        "protocol": "OData v4 / BAPI",
                        "tables": [
                                    "outbound_shipment_carton_dimensions"
                        ]
            },
            {
                        "id": "tms_trailer_fleet_specs",
                        "name": "Fleet Trailer Bay & DOT Axle-Weight Compliance Registry",
                        "protocol": "REST / JSON",
                        "tables": [
                                    "trailer_bay_geometry_specs"
                        ]
            },
            {
                        "id": "dock_lifo_axle_auditor",
                        "name": "Dock Scale & Crush-Pressure Physics Verification Engine",
                        "protocol": "IoT Weighbridge / REST",
                        "tables": [
                                    "axle_weight_crush_audit_logs"
                        ]
            }
]
    }

def query_outbound_shipment_carton_dimensions(
    shipment_wave_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query outbound_shipment_carton_dimensions records from or_tools_3d_voxel_packer."""
    rows = _read_json("outbound_shipment_carton_dimensions.json")
    all_rows = list(rows)
    if shipment_wave_id:
        rows = [r for r in rows if shipment_wave_id.lower() in str(r.get("shipment_wave_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "or_tools_3d_voxel_packer",
        "table": "outbound_shipment_carton_dimensions",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_trailer_bay_geometry_specs(
    trailer_type_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query trailer_bay_geometry_specs records from sap_ewm_carton_master."""
    rows = _read_json("trailer_bay_geometry_specs.json")
    all_rows = list(rows)
    if trailer_type_id:
        rows = [r for r in rows if trailer_type_id.lower() in str(r.get("trailer_type_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "sap_ewm_carton_master",
        "table": "trailer_bay_geometry_specs",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_lifo_3d_voxel_load_plans(
    load_plan_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query lifo_3d_voxel_load_plans records from tms_trailer_fleet_specs."""
    rows = _read_json("lifo_3d_voxel_load_plans.json")
    all_rows = list(rows)
    if load_plan_id:
        rows = [r for r in rows if load_plan_id.lower() in str(r.get("load_plan_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "tms_trailer_fleet_specs",
        "table": "lifo_3d_voxel_load_plans",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_axle_weight_crush_audit_logs(
    load_plan_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query axle_weight_crush_audit_logs records from dock_lifo_axle_auditor."""
    rows = _read_json("axle_weight_crush_audit_logs.json")
    all_rows = list(rows)
    if load_plan_id:
        rows = [r for r in rows if load_plan_id.lower() in str(r.get("load_plan_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "dock_lifo_axle_auditor",
        "table": "axle_weight_crush_audit_logs",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_commit_3d_lifo_load_plan(
    load_plan_id: Any,
    trailer_type_id: Any,
    cube_utilization_pct: Any,
    lifo_zones: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_commit_3d_lifo_load_plan mutation with deterministic audit logging."""
    action_id = _deterministic_id("CUBE-LP", load_plan_id, idempotency_key)
    payload = {
        "dispatch_execution_id": action_id,
        "load_plan_id": load_plan_id,
        "trailer_type_id": trailer_type_id,
        "cube_utilization_pct": cube_utilization_pct,
        "lifo_zones": lifo_zones,
        "rationale": rationale,
        "status": "LOAD_PLAN_3D_COMMITTED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_commit_3d_lifo_load_plan", payload)
    return payload


def action_resequence_dock_staging_lanes(
    shipment_wave_id: Any,
    staging_lane_id: Any,
    loading_sequence_mode: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_resequence_dock_staging_lanes mutation with deterministic audit logging."""
    action_id = _deterministic_id("CUBE-STG", shipment_wave_id, idempotency_key)
    payload = {
        "secondary_action_id": action_id,
        "shipment_wave_id": shipment_wave_id,
        "staging_lane_id": staging_lane_id,
        "loading_sequence_mode": loading_sequence_mode,
        "rationale": rationale,
        "status": "DOCK_STAGING_RESEQUENCED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_resequence_dock_staging_lanes", payload)
    return payload


# --- BEGIN PERSONA ANALYTICS & CHARTING ENRICHMENT ---
import statistics as _statistics
from .render.png_chart import render_comparison_png as _render_comparison_png
from .render.charts import create_load_consolidation_agent_chart_spec as _native_chart_spec

_MASTER_BACKBONE_PATH = Path(__file__).resolve().parent.parent / "fixtures" / "master" / "xyz_enterprise_backbone.json"
_LAST_CHART_SPEC: Any = None


def _discover_table_files() -> List[Path]:
    tdir = Path(__file__).resolve().parent.parent / "fixtures" / "tables"
    if not tdir.exists():
        return []
    return sorted(p for p in tdir.glob("*.json") if p.is_file())


def _infer_chart_columns(rows: List[Dict[str, Any]]) -> Any:
    if not rows:
        return ("id", "metric_a", "metric_b")
    sample = rows[0]
    keys = list(sample.keys())
    label_col = keys[0]
    for k in keys:
        if isinstance(sample.get(k), str) and any(t in k.lower() for t in ("_id", "sku", "facility", "lane", "route", "batch", "order", "supplier", "node")):
            label_col = k
            break
    num_cols = [
        k for k in keys
        if isinstance(sample.get(k), (int, float))
        and not isinstance(sample.get(k), bool)
        and not any(latlon in k.lower() for latlon in ("lat", "lon", "lng"))
    ]
    if len(num_cols) >= 2:
        return (label_col, num_cols[0], num_cols[1])
    if len(num_cols) == 1:
        return (label_col, num_cols[0], num_cols[0])
    return (label_col, keys[0], keys[0])


def _build_dynamic_vegalite_spec(
    rows: List[Dict[str, Any]],
    label_col: str,
    col_a: str,
    col_b: str,
    title: str,
) -> Dict[str, Any]:
    vals: List[Dict[str, Any]] = []
    for r in rows[:8]:
        ent = str(r.get(label_col, "Record"))
        va = float(r.get(col_a, 0.0) or 0.0) if isinstance(r.get(col_a), (int, float)) else 0.0
        vb = float(r.get(col_b, 0.0) or 0.0) if isinstance(r.get(col_b), (int, float)) else 0.0
        vals.append({"entity": ent, "series": col_a.replace("_", " ").title(), "value": round(va, 2)})
        if col_b != col_a:
            vals.append({"entity": ent, "series": col_b.replace("_", " ").title(), "value": round(vb, 2)})
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": title,
            "subtitle": "XYZ Global Industries Corp. (XYZ-CORP-01) · Live Python Analytics",
            "anchor": "start",
            "fontSize": 14,
            "subtitleColor": "#64748b",
        },
        "width": "container",
        "height": 300,
        "data": {"values": vals},
        "mark": {"type": "bar", "cornerRadiusTopLeft": 4, "cornerRadiusTopRight": 4, "tooltip": True},
        "encoding": {
            "x": {"field": "entity", "type": "nominal", "title": None, "axis": {"labelAngle": -25}},
            "xOffset": {"field": "series"},
            "y": {"field": "value", "type": "quantitative", "title": "Metric Value"},
            "color": {
                "field": "series",
                "type": "nominal",
                "scale": {"range": ["#64748b", "#2563eb"]},
                "legend": {"orient": "top"},
            },
            "tooltip": [
                {"field": "entity", "type": "nominal", "title": label_col},
                {"field": "series", "type": "nominal", "title": "KPI"},
                {"field": "value", "type": "quantitative", "title": "Value", "format": ",.2f"},
            ],
        },
        "config": {"view": {"stroke": "transparent"}},
    }


def get_native_chart_spec() -> Dict[str, Any]:
    """Returns the canonical multi-panel native Vega-Lite v5 spec for deterministic scenario runs."""
    return _native_chart_spec()


def get_latest_chart_spec(consume: bool = False) -> Dict[str, Any]:
    """Returns the latest turn-generated Vega-Lite v5 spec or falls back to the native agent spec."""
    global _LAST_CHART_SPEC
    if _LAST_CHART_SPEC is not None:
        out = copy.deepcopy(_LAST_CHART_SPEC) if "copy" in globals() else dict(_LAST_CHART_SPEC)
        if consume:
            _LAST_CHART_SPEC = None
        return out
    return _native_chart_spec()


def lookup_xyz_master_context(
    sku_id: str = "",
    facility_id: str = "",
    supplier_id: str = "",
    customer_id: str = "",
    carrier_id: str = "",
) -> Dict[str, Any]:
    """Join operational IDs against XYZ Global Industries Corp. (XYZ-CORP-01) master ERP/WMS/TMS tables."""
    if not _MASTER_BACKBONE_PATH.exists():
        return {"status": "MASTER_NOT_FOUND", "organization_id": "XYZ-CORP-01"}
    bundle = json.loads(_MASTER_BACKBONE_PATH.read_text(encoding="utf-8"))
    out: Dict[str, Any] = {
        "status": "SUCCESS",
        "organization_id": bundle.get("organization_id", "XYZ-CORP-01"),
        "organization_name": bundle.get("organization_name", "XYZ Global Industries Corp."),
    }
    if sku_id:
        out["material"] = bundle.get("materials", {}).get(sku_id)
    if facility_id:
        out["facility"] = bundle.get("facilities", {}).get(facility_id)
    if supplier_id:
        out["supplier"] = bundle.get("suppliers", {}).get(supplier_id)
    if customer_id:
        out["customer"] = bundle.get("customers", {}).get(customer_id)
    if carrier_id:
        out["carrier"] = bundle.get("carriers", {}).get(carrier_id)
    if not any([sku_id, facility_id, supplier_id, customer_id, carrier_id]):
        out["summary_counts"] = {
            "materials": len(bundle.get("materials", {})),
            "facilities": len(bundle.get("facilities", {})),
            "suppliers": len(bundle.get("suppliers", {})),
            "customers": len(bundle.get("customers", {})),
            "carriers": len(bundle.get("carriers", {})),
            "golden_threads": len(bundle.get("golden_threads", [])),
        }
    return out


def analyze_operational_metrics(
    table_name: str = "",
    filter_field: str = "",
    filter_value: str = "",
) -> Dict[str, Any]:
    """Run deterministic Python statistical, Pareto, and KPI aggregation across live XYZ-CORP-01 tables."""
    global _LAST_CHART_SPEC
    tfiles = _discover_table_files()
    if not tfiles:
        return {"status": "NO_TABLES", "agent": 'load_consolidation_agent'}

    chosen = tfiles[0]
    if table_name:
        for tf in tfiles:
            if table_name.lower().replace(".json", "") in tf.stem.lower():
                chosen = tf
                break

    rows = _read_json(chosen.name)
    if filter_field and filter_value:
        matched = [r for r in rows if filter_value.lower() in str(r.get(filter_field, "")).lower()]
        if matched:
            rows = matched

    label_col, col_a, col_b = _infer_chart_columns(rows)
    vals_a = [float(r.get(col_a, 0.0) or 0.0) for r in rows if isinstance(r.get(col_a), (int, float))]
    vals_b = [float(r.get(col_b, 0.0) or 0.0) for r in rows if isinstance(r.get(col_b), (int, float))]

    kpi_stats = {
        "primary_metric": col_a,
        "secondary_metric": col_b,
        "sum_primary": round(sum(vals_a), 2),
        "mean_primary": round(_statistics.mean(vals_a), 2) if vals_a else 0.0,
        "stdev_primary": round(_statistics.pstdev(vals_a), 2) if len(vals_a) > 1 else 0.0,
        "max_primary": round(max(vals_a), 2) if vals_a else 0.0,
        "sum_secondary": round(sum(vals_b), 2),
        "mean_secondary": round(_statistics.mean(vals_b), 2) if vals_b else 0.0,
    }

    ranked = sorted(
        rows,
        key=lambda r: abs(float(r.get(col_a, 0.0) or 0.0)) if isinstance(r.get(col_a), (int, float)) else 0.0,
        reverse=True,
    )
    _LAST_CHART_SPEC = _build_dynamic_vegalite_spec(
        rows,
        label_col,
        col_a,
        col_b,
        title=f"Load Consolidation Agent — {col_a.replace('_', ' ').title()} vs {col_b.replace('_', ' ').title()}",
    )

    md_lines = [
        f"| {label_col} | {col_a[:22]} | {col_b[:22]} |",
        "| :--- | ---: | ---: |",
    ]
    for r in ranked[:6]:
        va = r.get(col_a, "")
        vb = r.get(col_b, "")
        va_s = f"{va:,.2f}" if isinstance(va, float) else f"{va:,}" if isinstance(va, int) else str(va)
        vb_s = f"{vb:,.2f}" if isinstance(vb, float) else f"{vb:,}" if isinstance(vb, int) else str(vb)
        md_lines.append(f"| `{r.get(label_col, '')}` | **{va_s}** | {vb_s} |")

    return {
        "status": "SUCCESS",
        "agent": 'load_consolidation_agent',
        "analyzed_table": chosen.stem,
        "available_tables": [p.stem for p in tfiles],
        "records_evaluated": len(rows),
        "kpi_summary": kpi_stats,
        "top_pareto_record": ranked[0] if ranked else {},
        "concise_markdown_table": "\n".join(md_lines),
    }


def render_visual_chart(table_name: str = "", chart_title: str = "") -> Dict[str, Any]:
    """Build a live Vega-Lite v5 spec for the A2UI VegaChart card AND save a 1200x640 Pillow PNG chart."""
    global _LAST_CHART_SPEC
    tfiles = _discover_table_files()
    chosen = tfiles[0] if tfiles else None
    if table_name and tfiles:
        for tf in tfiles:
            if table_name.lower().replace(".json", "") in tf.stem.lower():
                chosen = tf
                break

    if chosen is None:
        return {"status": "NO_DATA"}

    rows = _read_json(chosen.name)
    label_col, col_a, col_b = _infer_chart_columns(rows)
    resolved_title = chart_title or f"Load Consolidation Agent — {chosen.stem.replace('_', ' ').title()}"
    spec = _build_dynamic_vegalite_spec(rows, label_col, col_a, col_b, title=resolved_title)
    _LAST_CHART_SPEC = spec

    labels = [str(r.get(label_col, "")) for r in rows]
    va = [float(r.get(col_a, 0.0) or 0.0) if isinstance(r.get(col_a), (int, float)) else 0.0 for r in rows]
    vb = [float(r.get(col_b, 0.0) or 0.0) if isinstance(r.get(col_b), (int, float)) else 0.0 for r in rows]

    png_meta = _render_comparison_png(
        agent_id='load_consolidation_agent',
        title=resolved_title,
        subtitle=f"XYZ Global Industries Corp. (XYZ-CORP-01) · Source Table: {chosen.stem}",
        labels=labels,
        series_a=va,
        series_a_label=col_a.replace("_", " ").title(),
        series_b=vb,
        series_b_label=col_b.replace("_", " ").title(),
        y_title=col_a.replace("_", " ").title(),
    )
    return {
        "status": "SUCCESS",
        "source_table": chosen.stem,
        "a2ui_vega_lite_queued": True,
        "png_infographic": png_meta,
    }


def draft_operational_brief(
    subject: str = "",
    recipient_role: str = "Supply Chain & Operations Leadership",
    table_name: str = "",
) -> Dict[str, Any]:
    """Draft a concise, grounded persona operational decision brief or action memo from live Python KPIs."""
    analysis = analyze_operational_metrics(table_name=table_name)
    kpi = analysis.get("kpi_summary", {})
    doc_ref = f"BRIEF-LOADC-2026-{analysis.get('records_evaluated', 8):02d}"
    title_str = subject or f"Load Consolidation Agent Operational Decision Brief"
    brief_md = "\n".join(
        [
            f"### 📄 {title_str} (`{doc_ref}`)",
            f"- **Organization**: XYZ Global Industries Corp. (`XYZ-CORP-01`)",
            f"- **To**: {recipient_role}",
            f"- **Source Table Audited**: `{analysis.get('analyzed_table')}` (`{analysis.get('records_evaluated')}` records)",
            f"- **Primary KPI (`{kpi.get('primary_metric')}`)**: Sum `{kpi.get('sum_primary', 0):,.2f}` | Mean `{kpi.get('mean_primary', 0):,.2f}` | Peak `{kpi.get('max_primary', 0):,.2f}`",
            "",
            analysis.get("concise_markdown_table", ""),
            "",
            "**Governance Gate**: Pre-validated against XYZ-CORP-01 tolerances; requires explicit confirmation and `idempotency_key` prior to ERP/WMS/TMS write-back.",
        ]
    )
    return {
        "status": "DRAFT_READY",
        "document_ref": doc_ref,
        "recipient_role": recipient_role,
        "markdown_draft": brief_md,
    }
# --- END PERSONA ANALYTICS & CHARTING ENRICHMENT ---

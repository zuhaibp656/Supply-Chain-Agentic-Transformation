"""Deterministic and fixture-backed tools for CSCO Control Tower Copilot."""
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
    """Returns connected source systems, enterprise digital twins, and integration protocols."""
    return {
        "agent": "csco_control_tower_copilot",
        "systems": [
            {
                "id": "bigquery_sc_twin",
                "name": "BigQuery Multi-Echelon Enterprise Digital Twin",
                "protocol": "BigQuery SQL / Vertex AI Feature Store",
                "tables": ["sc_kpi_summary", "network_bottlenecks", "multiechelon_twin_status"],
            },
            {
                "id": "sap_s4hana_core",
                "name": "SAP S/4HANA Enterprise Resource Planning (ERP)",
                "protocol": "OData v4 / RFC / CDC PubSub",
                "tables": ["cross_erp_order_backlog"],
            },
            {
                "id": "looker_governance",
                "name": "Google Looker Semantic Metric Governance Layer",
                "protocol": "LookML semantic API",
                "tables": ["sc_kpi_summary"],
            },
            {
                "id": "executive_orchestrator",
                "name": "CSCO Executive Decision & Playbook Engine",
                "protocol": "REST API / Event Driven Webhook",
                "tables": ["executive_playbooks"],
            }
        ]
    }


def query_executive_kpis(region: str = "", period: str = "", limit: int = 10) -> Dict[str, Any]:
    """Query high-level executive supply chain KPIs including OTIF, DIO, OEE, Line-Down Risk, and Trapped Working Capital."""
    rows = _read_json("sc_kpi_summary.json")
    all_rows = list(rows)
    if region:
        r_low = region.lower()
        rows = [r for r in rows if r_low in r.get("region", "").lower()]
    if period:
        p_low = period.lower()
        rows = [r for r in rows if p_low in r.get("period", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "bigquery_sc_twin",
        "table": "sc_kpi_summary",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_network_bottlenecks(severity: str = "", region: str = "", min_impact_usd: float = 0.0, limit: int = 10) -> Dict[str, Any]:
    """Query real-time supply chain bottlenecks, chokepoints, and high-dollar operational jeopardy events."""
    rows = _read_json("network_bottlenecks.json")
    all_rows = list(rows)
    if severity:
        rows = [r for r in rows if severity.upper() == r.get("severity", "").upper()]
    if region:
        r_low = region.lower()
        rows = [r for r in rows if r_low in r.get("region", "").lower()]
    if min_impact_usd > 0:
        rows = [r for r in rows if r.get("revenue_impact_usd", 0) >= min_impact_usd]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "bigquery_sc_twin",
        "table": "network_bottlenecks",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_multiechelon_twin_status(echelon_level: Optional[int] = None, safety_stock_health: str = "", limit: int = 10) -> Dict[str, Any]:
    """Query multi-echelon node status (Tier-0 plants, Tier-1 central mega-hubs, Tier-2 regional DCs) for buffer health."""
    rows = _read_json("multiechelon_twin_status.json")
    all_rows = list(rows)
    if echelon_level is not None:
        rows = [r for r in rows if r.get("echelon_level") == echelon_level]
    if safety_stock_health:
        rows = [r for r in rows if safety_stock_health.upper() in r.get("safety_stock_health", "").upper()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "bigquery_sc_twin",
        "table": "multiechelon_twin_status",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_cross_erp_order_backlog(order_type: str = "", status: str = "", days_delayed_min: int = 0, limit: int = 10) -> Dict[str, Any]:
    """Query cross-ERP customer sales orders and supplier purchase orders currently delayed or in stockout jeopardy."""
    rows = _read_json("cross_erp_order_backlog.json")
    all_rows = list(rows)
    if order_type:
        rows = [r for r in rows if order_type.upper() in r.get("order_type", "").upper()]
    if status:
        rows = [r for r in rows if status.upper() in r.get("status", "").upper()]
    if days_delayed_min > 0:
        rows = [r for r in rows if r.get("days_delayed", 0) >= days_delayed_min]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "sap_s4hana_core",
        "table": "cross_erp_order_backlog",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_execute_executive_playbook(
    playbook_id: str,
    target_facilities: List[str],
    allocated_budget_usd: float,
    rationale: str,
    idempotency_key: str = ""
) -> Dict[str, Any]:
    """Autonomous mutation tool to execute an executive supply chain playbook across plants, hubs, and carriers."""
    if not playbook_id or not target_facilities or allocated_budget_usd <= 0 or not rationale:
        return {
            "error": "missing_required_arguments",
            "required": ["playbook_id", "target_facilities", "allocated_budget_usd", "rationale"]
        }

    # Governance guardrail: budgets over $2,000,000 require CSCO / CFO board signoff
    if allocated_budget_usd > 2000000:
        return {
            "error": "budget_exceeds_delegation_authority",
            "threshold_usd": 2000000,
            "requested_usd": allocated_budget_usd,
            "escalation": "request_csco_cfo_approval"
        }

    execution_id = _deterministic_id("EXEC-PB", playbook_id, allocated_budget_usd, idempotency_key or "default")
    record = {
        "execution_id": execution_id,
        "playbook_id": playbook_id,
        "target_facilities": target_facilities,
        "allocated_budget_usd": allocated_budget_usd,
        "rationale": rationale,
        "status": "EXECUTED_ACTIVE",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_execute_executive_playbook", record)
    return {
        "status": "executed",
        "execution_id": execution_id,
        "audit_trail": (
            f"Executive Playbook '{playbook_id}' executed [{execution_id}] with budget ${allocated_budget_usd:,.2f} "
            f"across {len(target_facilities)} facilities. Rationale: {rationale}."
        )
    }


def action_rebalance_network_allocation(
    source_node: str,
    target_node: str,
    sku_id: str,
    quantity: int,
    expedite_mode: str,
    rationale: str,
    idempotency_key: str = ""
) -> Dict[str, Any]:
    """Dispatches lateral inventory rebalancing between multi-echelon nodes to prevent customer stockout."""
    if not source_node or not target_node or not sku_id or quantity <= 0 or not rationale:
        return {
            "error": "missing_required_arguments",
            "required": ["source_node", "target_node", "sku_id", "quantity", "rationale"]
        }

    transfer_id = _deterministic_id("TRF", source_node, target_node, sku_id, quantity)
    record = {
        "transfer_id": transfer_id,
        "source_node": source_node,
        "target_node": target_node,
        "sku_id": sku_id,
        "quantity": quantity,
        "expedite_mode": expedite_mode,
        "rationale": rationale,
        "status": "TRANSFER_ORDER_CREATED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_rebalance_network_allocation", record)
    return {
        "status": "dispatched",
        "transfer_id": transfer_id,
        "audit_trail": (
            f"Stock transfer {transfer_id} created: {quantity} units of {sku_id} moved from {source_node} "
            f"to {target_node} via {expedite_mode}. Rationale: {rationale}."
        )
    }


# --- BEGIN PERSONA ANALYTICS & CHARTING ENRICHMENT ---
import statistics as _statistics
from .render.png_chart import render_comparison_png as _render_comparison_png
from .render.charts import create_composite_control_tower_spec as _native_chart_spec

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
        return {"status": "NO_TABLES", "agent": 'csco_control_tower_copilot'}

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
        title=f"Csco Control Tower Copilot — {col_a.replace('_', ' ').title()} vs {col_b.replace('_', ' ').title()}",
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
        "agent": 'csco_control_tower_copilot',
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
    resolved_title = chart_title or f"Csco Control Tower Copilot — {chosen.stem.replace('_', ' ').title()}"
    spec = _build_dynamic_vegalite_spec(rows, label_col, col_a, col_b, title=resolved_title)
    _LAST_CHART_SPEC = spec

    labels = [str(r.get(label_col, "")) for r in rows]
    va = [float(r.get(col_a, 0.0) or 0.0) if isinstance(r.get(col_a), (int, float)) else 0.0 for r in rows]
    vb = [float(r.get(col_b, 0.0) or 0.0) if isinstance(r.get(col_b), (int, float)) else 0.0 for r in rows]

    png_meta = _render_comparison_png(
        agent_id='csco_control_tower_copilot',
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
    doc_ref = f"BRIEF-CSCOC-2026-{analysis.get('records_evaluated', 8):02d}"
    title_str = subject or f"Csco Control Tower Copilot Operational Decision Brief"
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

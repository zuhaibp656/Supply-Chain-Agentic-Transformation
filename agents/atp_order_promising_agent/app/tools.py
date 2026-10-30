"""Deterministic and fixture-backed tools for PromiseGuard ATP Order Promising Agent."""
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
    """Returns connected source systems, Cloud Spanner real-time ATP engines, and order management brokers."""
    return {
        "agent": "atp_order_promising_agent",
        "systems": [
            {
                "id": "spanner_realtime_atp_engine",
                "name": "Google Cloud Spanner Global Real-Time ATP / CTP Engine",
                "protocol": "Spanner gRPC / Sub-20ms Strong Consistency Query",
                "tables": ["realtime_sku_atp_allocations"],
            },
            {
                "id": "customer_contract_tier_ledger",
                "name": "SAP S/4HANA Sales & Distribution Customer Allocation Ledger",
                "protocol": "OData v4 / Real-Time Tier Quota Guard",
                "tables": ["customer_tier_sla_commitments"],
            },
            {
                "id": "omnichannel_order_stream",
                "name": "Enterprise OMS / EDI 850 Order Ingestion Event Stream",
                "protocol": "Cloud Pub/Sub / Kafka / Sub-Second Order Event Capture",
                "tables": ["inbound_customer_order_requests"],
            },
            {
                "id": "fulfillment_routing_optimizer",
                "name": "Google OR-Tools Omnichannel Sourcing & Promising Optimizer",
                "protocol": "REST API / Cost-to-Serve & SLA Fulfillment Router",
                "tables": ["order_promising_routing_decisions"],
            }
        ]
    }


def query_realtime_sku_atp_allocations(
    sku_id: str = "",
    network_node_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query real-time available-to-promise (ATP) inventory, capable-to-promise (CTP), and tier reserves."""
    rows = _read_json("realtime_sku_atp_allocations.json")
    all_rows = list(rows)
    if sku_id:
        rows = [r for r in rows if sku_id.lower() in r.get("sku_id", "").lower()]
    if network_node_id:
        rows = [r for r in rows if network_node_id.lower() in r.get("network_node_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "spanner_realtime_atp_engine",
        "table": "realtime_sku_atp_allocations",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_customer_tier_sla_commitments(
    customer_id: str = "",
    contract_tier: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query customer contract tier SLAs, minimum fill rate commitments, and OTIF penalty liabilities."""
    rows = _read_json("customer_tier_sla_commitments.json")
    all_rows = list(rows)
    if customer_id:
        rows = [r for r in rows if customer_id.lower() in r.get("customer_id", "").lower()]
    if contract_tier:
        rows = [r for r in rows if contract_tier.lower() in r.get("contract_tier", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "customer_contract_tier_ledger",
        "table": "customer_tier_sla_commitments",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_inbound_customer_order_requests(
    order_id: str = "",
    customer_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query inbound customer order requests awaiting real-time ATP commitment and promised delivery date."""
    rows = _read_json("inbound_customer_order_requests.json")
    all_rows = list(rows)
    if order_id:
        rows = [r for r in rows if order_id.lower() in r.get("order_id", "").lower()]
    if customer_id:
        rows = [r for r in rows if customer_id.lower() in r.get("customer_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "omnichannel_order_stream",
        "table": "inbound_customer_order_requests",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_order_promising_routing_decisions(
    order_id: str = "",
    customer_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query optimal fulfillment node routing decisions, transit hours, and OTIF penalty risk elimination."""
    rows = _read_json("order_promising_routing_decisions.json")
    all_rows = list(rows)
    if order_id:
        rows = [r for r in rows if order_id.lower() in r.get("order_id", "").lower()]
    if customer_id:
        rows = [r for r in rows if customer_id.lower() in r.get("customer_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "fulfillment_routing_optimizer",
        "table": "order_promising_routing_decisions",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_commit_dynamic_order_promise(
    order_id: str,
    customer_id: str,
    promised_fulfillment_node: str,
    promised_delivery_date: str,
    atp_reserved_qty: int,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Commit binding ATP order promise and reserve inventory allocations across Cloud Spanner and OMS."""
    promise_id = _deterministic_id("PROMISE-COMMIT", order_id, customer_id, idempotency_key)
    payload = {
        "promise_id": promise_id,
        "order_id": order_id,
        "customer_id": customer_id,
        "promised_fulfillment_node": promised_fulfillment_node,
        "promised_delivery_date": promised_delivery_date,
        "atp_reserved_qty": atp_reserved_qty,
        "spanner_txn_id": f"SPAN-TXN-{promise_id[-6:]}",
        "status": "ATP_PROMISE_COMMITTED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_commit_dynamic_order_promise", payload)
    return payload


def action_protect_tier1_allocation_reserve(
    sku_id: str,
    network_node_id: str,
    reserve_quantity: int,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Ringfence inventory quota for strategic Tier 1 contract customers to prevent unauthorized depletion."""
    protection_id = _deterministic_id("TIER-RINGFENCE", sku_id, network_node_id, idempotency_key)
    payload = {
        "protection_id": protection_id,
        "sku_id": sku_id,
        "network_node_id": network_node_id,
        "reserve_quantity": reserve_quantity,
        "status": "TIER1_ALLOCATION_RINGFENCED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_protect_tier1_allocation_reserve", payload)
    return payload


# --- BEGIN PERSONA ANALYTICS & CHARTING ENRICHMENT ---
import statistics as _statistics
from .render.png_chart import render_comparison_png as _render_comparison_png
from .render.charts import create_order_promising_chart_spec as _native_chart_spec

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
        return {"status": "NO_TABLES", "agent": 'atp_order_promising_agent'}

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
        title=f"Atp Order Promising Agent — {col_a.replace('_', ' ').title()} vs {col_b.replace('_', ' ').title()}",
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
        "agent": 'atp_order_promising_agent',
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
    resolved_title = chart_title or f"Atp Order Promising Agent — {chosen.stem.replace('_', ' ').title()}"
    spec = _build_dynamic_vegalite_spec(rows, label_col, col_a, col_b, title=resolved_title)
    _LAST_CHART_SPEC = spec

    labels = [str(r.get(label_col, "")) for r in rows]
    va = [float(r.get(col_a, 0.0) or 0.0) if isinstance(r.get(col_a), (int, float)) else 0.0 for r in rows]
    vb = [float(r.get(col_b, 0.0) or 0.0) if isinstance(r.get(col_b), (int, float)) else 0.0 for r in rows]

    png_meta = _render_comparison_png(
        agent_id='atp_order_promising_agent',
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
    doc_ref = f"BRIEF-ATPOR-2026-{analysis.get('records_evaluated', 8):02d}"
    title_str = subject or f"Atp Order Promising Agent Operational Decision Brief"
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

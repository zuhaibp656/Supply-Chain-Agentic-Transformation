"""Official FDE/ACE A2UI v0.9 Builder & Dual-Surface Renderer for Gemini Enterprise.

Implements:
1. Surface 1 (Inline Chat `Card`): Strictly renders ONLY the interactive 2-panel
   `VegaChart` executive infographic inside the inline chat card (zero text/table clutter).
2. Surface 2 (Side-Panel `Canvas`, `autoOpen=False`): Renders a compact launcher chip in
   chat that opens Gemini Enterprise's persistent right-hand Canvas side panel containing:
   - Single `MaterialColumn` (`justify="start"`) preventing 825px flex-band stretching.
   - Interactive `MaterialRow` action bar with `MaterialButton` quick-action dispatches.
   - Collapsible `MaterialExpansionPanel` cards (`<= 62` char headers) explaining connected
     data sources, deterministic solver findings, and governed write-back readiness.
   - Native Looker Studio `RichTable` (`tableData.spec = {}`, coerced numeric `DOUBLE` &
     `STRING` columns) for client-side sorting, filtering, and auto-charting.
3. Inbound Synthetic Action Parser & `before_model_callback` History Sanitizer.
"""

from __future__ import annotations

import copy
import json
import math
from typing import Any, Dict, List, Optional
import uuid

from google.genai import types

VERSION = "v0.9"
CATALOG_ID = "https://www.gstatic.com/vertexaisearch/a2ui/v0_9/gemini_enterprise_composite_catalog.json"
MIME = "application/json+a2ui"
SENTINEL_OPEN = "<a2a_datapart_json>"
SENTINEL_CLOSE = "</a2a_datapart_json>"

ALLOWED_USAGE_HINTS = {
    "h1", "h2", "h3", "h4", "h5",
    "subtitle1", "subtitle2",
    "body", "body1", "body2",
    "caption",
}
MAX_PANEL_TITLE = 62

SYNTHETIC_UI_TEXTS = {
    "user action triggered",
    "user action triggered.",
    "action triggered",
    "user action",
}


def wrap_a2ui_message(message: Dict[str, Any]) -> types.Part:
    """Wrap a single A2UI v0.9 lifecycle message into a GenAI Part for Gemini Enterprise."""
    envelope = {
        "kind": "data",
        "metadata": {"mimeType": MIME},
        "data": message,
    }
    raw = json.dumps(envelope, separators=(",", ":"))
    blob_bytes = f"{SENTINEL_OPEN}{raw}{SENTINEL_CLOSE}".encode("utf-8")
    return types.Part(
        inline_data=types.Blob(mime_type="text/plain", data=blob_bytes),
        part_metadata={"mimeType": MIME},
    )


def is_a2ui_part(part: Any) -> bool:
    meta = getattr(part, "part_metadata", None)
    if isinstance(meta, dict) and meta.get("mimeType") == MIME:
        return True
    blob = getattr(part, "inline_data", None)
    data = getattr(blob, "data", None)
    if isinstance(data, (bytes, bytearray)):
        return bytes(data).lstrip().startswith(SENTINEL_OPEN.encode("utf-8"))
    if isinstance(data, str):
        return SENTINEL_OPEN in data
    t = getattr(part, "text", None)
    return bool(t and SENTINEL_OPEN in t)


def decode_a2ui_envelope(part: Any) -> Optional[Dict[str, Any]]:
    blob = getattr(part, "inline_data", None)
    data = getattr(blob, "data", None)
    text = ""
    if isinstance(data, (bytes, bytearray)):
        text = bytes(data).decode("utf-8", errors="replace").strip()
    elif isinstance(data, str):
        text = data.strip()
    if not text.startswith(SENTINEL_OPEN):
        return None
    body = text[len(SENTINEL_OPEN):]
    if SENTINEL_CLOSE in body:
        body = body.split(SENTINEL_CLOSE, 1)[0]
    try:
        parsed = json.loads(body)
        return parsed if isinstance(parsed, dict) else None
    except Exception:
        return None


def parse_a2ui_action(part: Any) -> Optional[Dict[str, Any]]:
    env = decode_a2ui_envelope(part)
    if not env:
        return None
    data = env.get("data")
    if isinstance(data, dict) and isinstance(data.get("action"), dict):
        return data["action"]
    return None


def find_a2ui_action(parts: Any) -> Optional[Dict[str, Any]]:
    for p in parts or []:
        act = parse_a2ui_action(p)
        if act:
            return act
    return None


def sanitize_history_and_intercept_actions(llm_request: Any) -> None:
    """FDE Lifecycle Hook (`before_model_callback`):
    1. Converts synthetic A2UI button-click turns (`'User action triggered.'` + action payload)
       into explicit natural-language tool instructions so Gemini executes the clicked action!
    2. Strips raw `<a2a_datapart_json>` envelopes from prior model turns so the LLM never
       imitates or echoes raw A2UI JSON in multi-turn conversations.
    """
    contents = getattr(llm_request, "contents", None)
    if not contents:
        return None

    for idx, content in enumerate(contents):
        parts = getattr(content, "parts", None)
        if not parts:
            continue
        role = getattr(content, "role", "")
        is_last_user = (idx == len(contents) - 1) and (role == "user")

        if is_last_user:
            act = find_a2ui_action(parts)
            if act:
                act_name = str(act.get("name", "analyze_top_variances"))
                ctx = act.get("context") or {}
                ctx_summary = ", ".join(f"{k}={v}" for k, v in ctx.items()) if isinstance(ctx, dict) else str(ctx)
                directive = (
                    f"The user clicked the interactive A2UI Canvas button '{act_name}' "
                    f"({ctx_summary}). Execute the matching data-source query, solver, and "
                    f"A2UI visual chart tools now, and provide a clear plain-English breakdown "
                    f"with a concise <=5 column Markdown table."
                )
                content.parts = [types.Part(text=directive)]
                continue

        cleaned: List[types.Part] = []
        had_ui = False
        for p in parts:
            if is_a2ui_part(p):
                had_ui = True
                continue
            if getattr(p, "inline_data", None) is not None and role == "model":
                had_ui = True
                continue
            cleaned.append(p)

        if had_ui and not cleaned:
            cleaned = [types.Part(text="[Interactive VegaChart Infographic & Source Data Canvas Rendered]")]
        content.parts = cleaned
    return None


def _clean_json_numbers(obj: Any) -> Any:
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return 0.0
        return round(obj, 4)
    if isinstance(obj, dict):
        return {k: _clean_json_numbers(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_clean_json_numbers(v) for v in obj]
    return obj


def coerce_rich_table_cell(val: Any) -> Any:
    """Coerce cell values for Looker Studio `RichTable` (`int` / `float` / `str` / `None`)."""
    if val is None:
        return None
    if isinstance(val, bool):
        return "Yes" if val else "No"
    if isinstance(val, int):
        return val
    if isinstance(val, float):
        if math.isnan(val) or math.isinf(val):
            return None
        return round(val, 4)
    if isinstance(val, (list, dict)):
        return json.dumps(val, ensure_ascii=False)[:120]
    return str(val)


def build_looker_rich_table(component_id: str, rows: List[Dict[str, Any]], max_cols: int = 7) -> Optional[Dict[str, Any]]:
    """Build a validated Looker Studio `RichTable` (`tableData.spec = {}`) from real source rows."""
    if not rows or not isinstance(rows[0], dict):
        return None
    raw_cols = list(rows[0].keys())[:max_cols]
    if not raw_cols:
        return None

    col_map: List[tuple[str, str]] = []
    for c in raw_cols:
        pretty = c.replace("_", " ").strip().title()
        pretty = (
            pretty.replace("Usd", "(USD)")
            .replace("Pct", "(%)")
            .replace("Id", "ID")
            .replace("Sku", "SKU")
            .replace("Po ", "PO ")
            .replace("Grn", "GRN")
            .replace("Otif", "OTIF")
            .replace("Oee", "OEE")
            .replace("Wms", "WMS")
        )
        col_map.append((c, pretty))

    coerced_rows: List[Dict[str, Any]] = []
    for r in rows[:40]:
        if not isinstance(r, dict):
            continue
        coerced_rows.append({pretty: coerce_rich_table_cell(r.get(orig)) for orig, pretty in col_map})

    if not coerced_rows:
        return None

    schema: List[Dict[str, str]] = []
    for _, pretty in col_map:
        col_vals = [row.get(pretty) for row in coerced_rows if row.get(pretty) is not None]
        is_num = bool(col_vals) and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in col_vals)
        schema.append({"name": pretty, "dataType": "DOUBLE" if is_num else "STRING"})

    return {
        "id": component_id,
        "component": "RichTable",
        "tableData": {
            "schema": schema,
            "data": coerced_rows,
            "spec": {},  # CRITICAL FDE Rule #4: MUST be {} for Looker auto-charting!
        },
    }


def enrich_to_executive_2panel_vegalite(
    spec: Optional[Dict[str, Any]],
    fallback_fn: Any,
    agent_title: str,
) -> Dict[str, Any]:
    """Upgrades single-view grouped bar specs into a self-explanatory 2-Panel Executive
    `VegaChart` Infographic (Comparison Bars + Direct Value Labels + Target Rule Line +
    Synchronized Diverging `Δ` Variance Strip), while preserving bespoke multi-layer/concat specs.
    """
    candidate = copy.deepcopy(spec) if isinstance(spec, dict) and spec else None
    if candidate is None and callable(fallback_fn):
        try:
            candidate = copy.deepcopy(fallback_fn())
        except Exception:
            candidate = None

    if not isinstance(candidate, dict):
        candidate = {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "title": {"text": f"{agent_title} — Live Telemetry", "anchor": "start"},
            "width": 600,
            "height": 320,
            "data": {"values": [{"entity": "Baseline", "series": "Plan", "metric_value": 100.0}]},
            "mark": {"type": "bar", "tooltip": True},
            "encoding": {
                "x": {"field": "entity", "type": "nominal"},
                "y": {"field": "metric_value", "type": "quantitative"},
            },
        }

    candidate = _clean_json_numbers(candidate)
    candidate["$schema"] = "https://vega.github.io/schema/vega-lite/v5.json"
    candidate["background"] = "#ffffff"

    # Check if candidate is a standard grouped-bar `[entity, series, metric_value]` spec
    # that we can upgrade into a 2-Panel Executive Comparison + Variance Delta Infographic!
    vals = (candidate.get("data") or {}).get("values")
    if (
        isinstance(vals, list)
        and len(vals) >= 4
        and isinstance(vals[0], dict)
        and {"entity", "series", "metric_value"}.issubset(vals[0].keys())
        and "vconcat" not in candidate
        and "hconcat" not in candidate
        and "layer" not in candidate
    ):
        # Compute per-entity delta (`Series 2 - Series 1`) for Panel 2 diverging variance strip
        by_entity: Dict[str, List[tuple[str, float]]] = {}
        series_order: List[str] = []
        for row in vals:
            ent = str(row.get("entity", ""))
            ser = str(row.get("series", "Metric"))
            mv = float(row.get("metric_value", 0.0) or 0.0)
            if ser not in series_order:
                series_order.append(ser)
            by_entity.setdefault(ent, []).append((ser, mv))

        delta_rows: List[Dict[str, Any]] = []
        enriched_vals: List[Dict[str, Any]] = []
        all_nums = [float(r.get("metric_value", 0.0) or 0.0) for r in vals]
        mean_val = round(sum(all_nums) / max(1, len(all_nums)), 2)

        for ent, pairs in by_entity.items():
            v0 = pairs[0][1] if len(pairs) >= 1 else 0.0
            v1 = pairs[1][1] if len(pairs) >= 2 else v0
            diff = round(v1 - v0, 2)
            pct = round((diff / abs(v0)) * 100.0, 1) if abs(v0) > 1e-6 else 0.0
            direction = "Positive / Gain" if diff >= 0 else "Negative / Reduction"
            delta_rows.append({
                "entity": ent,
                "delta_value": diff,
                "delta_pct": f"{pct:+.1f}%",
                "direction": direction,
                "series_a_val": round(v0, 2),
                "series_b_val": round(v1, 2),
            })
            for ser, mv in pairs:
                enriched_vals.append({
                    "entity": ent,
                    "series": ser,
                    "metric_value": round(mv, 2),
                    "net_delta": diff,
                    "delta_pct": f"{pct:+.1f}%",
                })

        orig_title = candidate.get("title")
        if isinstance(orig_title, str):
            title_block = {
                "text": orig_title,
                "subtitle": f"{agent_title} · Top: Baseline vs. Target/Actual (Dashed = Mean {mean_val:,.1f}) · Bottom: Net Variance (Δ)",
                "anchor": "start",
                "fontSize": 14,
                "fontWeight": 700,
                "color": "#0f172a",
                "subtitleColor": "#475569",
                "subtitleFontSize": 11.5,
            }
        elif isinstance(orig_title, dict):
            title_block = dict(orig_title)
            title_block.setdefault("anchor", "start")
            title_block["fontSize"] = 14
            title_block["color"] = "#0f172a"
            title_block["subtitle"] = f"Top: Series Comparison (Dashed Rule = Mean {mean_val:,.1f}) · Bottom: Signed Variance Shift (Δ)"
            title_block["subtitleColor"] = "#475569"
        else:
            title_block = {
                "text": f"{agent_title} — Executive Variance & Optimization Infographic",
                "subtitle": f"Top: Baseline vs. Optimized/Verified Actual · Bottom: Signed Variance Shift (Δ)",
                "anchor": "start",
                "fontSize": 14,
                "color": "#0f172a",
                "subtitleColor": "#475569",
            }

        y_title = (
            ((candidate.get("encoding") or {}).get("y") or {}).get("title")
            or (series_order[0] if series_order else "Value")
        )
        color_domain = series_order[:2] if len(series_order) >= 2 else series_order
        color_range = ["#64748b", "#1a73e8"][: len(color_domain)] or ["#1a73e8"]

        candidate = {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "background": "#ffffff",
            "padding": {"top": 10, "left": 12, "right": 14, "bottom": 8},
            "title": title_block,
            "spacing": 16,
            "vconcat": [
                {
                    "width": 580,
                    "height": 205,
                    "data": {"values": enriched_vals},
                    "layer": [
                        {
                            "mark": {
                                "type": "bar",
                                "cornerRadiusTopLeft": 4,
                                "cornerRadiusTopRight": 4,
                                "tooltip": True,
                            },
                            "encoding": {
                                "x": {
                                    "field": "entity",
                                    "type": "nominal",
                                    "title": None,
                                    "axis": {"labels": False, "ticks": False},
                                },
                                "xOffset": {"field": "series"},
                                "y": {
                                    "field": "metric_value",
                                    "type": "quantitative",
                                    "title": y_title,
                                    "axis": {"grid": True, "gridColor": "#e2e8f0", "labelColor": "#334155"},
                                },
                                "color": {
                                    "field": "series",
                                    "type": "nominal",
                                    "title": None,
                                    "scale": {"domain": color_domain, "range": color_range},
                                    "legend": {"orient": "top", "labelFontSize": 11.5, "symbolType": "circle"},
                                },
                                "tooltip": [
                                    {"field": "entity", "type": "nominal", "title": "Record / Node"},
                                    {"field": "series", "type": "nominal", "title": "Metric Series"},
                                    {"field": "metric_value", "type": "quantitative", "title": "Exact Value", "format": ",.2f"},
                                    {"field": "net_delta", "type": "quantitative", "title": "Net Variance (Δ)", "format": "+,.2f"},
                                    {"field": "delta_pct", "type": "nominal", "title": "Relative Shift"},
                                ],
                            },
                        },
                        {
                            "mark": {
                                "type": "rule",
                                "color": "#d97706",
                                "strokeDash": [5, 4],
                                "strokeWidth": 1.6,
                            },
                            "encoding": {
                                "y": {"datum": mean_val, "type": "quantitative"},
                            },
                        },
                    ],
                },
                {
                    "width": 580,
                    "height": 115,
                    "data": {"values": delta_rows},
                    "layer": [
                        {
                            "mark": {"type": "bar", "cornerRadius": 3, "tooltip": True},
                            "encoding": {
                                "x": {
                                    "field": "entity",
                                    "type": "nominal",
                                    "title": None,
                                    "axis": {"labelAngle": -22, "labelFontSize": 11, "labelColor": "#0f172a"},
                                },
                                "y": {
                                    "field": "delta_value",
                                    "type": "quantitative",
                                    "title": "Net Shift (Δ)",
                                    "axis": {"grid": True, "gridColor": "#f1f5f9", "tickCount": 4},
                                },
                                "color": {
                                    "condition": {"test": "datum.delta_value >= 0", "value": "#059669"},
                                    "value": "#e11d48",
                                },
                                "tooltip": [
                                    {"field": "entity", "type": "nominal", "title": "Record / Node"},
                                    {"field": "series_a_val", "type": "quantitative", "title": "Baseline", "format": ",.2f"},
                                    {"field": "series_b_val", "type": "quantitative", "title": "Target / Verified", "format": ",.2f"},
                                    {"field": "delta_value", "type": "quantitative", "title": "Net Variance (Δ)", "format": "+,.2f"},
                                    {"field": "delta_pct", "type": "nominal", "title": "Shift (%)"},
                                ],
                            },
                        },
                        {
                            "mark": {"type": "rule", "color": "#94a3b8", "strokeWidth": 1},
                            "encoding": {"y": {"datum": 0, "type": "quantitative"}},
                        },
                    ],
                },
            ],
            "config": {
                "background": "#ffffff",
                "view": {"stroke": "transparent"},
                "font": "Google Sans, Inter, system-ui, sans-serif",
            },
        }
        return candidate

    # Ensure explicit integer pixel dimensions on non-grouped bespoke specs (`layer` / `vconcat` / `hconcat`)
    cfg = candidate.setdefault("config", {})
    if isinstance(cfg, dict):
        cfg["background"] = "#ffffff"
        vcfg = cfg.setdefault("view", {})
        if isinstance(vcfg, dict):
            vcfg.setdefault("stroke", "transparent")

    if "vconcat" in candidate or "hconcat" in candidate:
        if candidate.get("width") == "container":
            candidate.pop("width", None)
        for ck in ("vconcat", "hconcat"):
            panels = candidate.get(ck)
            if isinstance(panels, list):
                for p in panels:
                    if isinstance(p, dict):
                        p.pop("$schema", None)
                        pw = p.get("width")
                        p["width"] = int(pw) if isinstance(pw, (int, float)) and pw >= 180 else 580
                        ph = p.get("height")
                        p["height"] = int(ph) if isinstance(ph, (int, float)) and ph >= 110 else 185
    else:
        w = candidate.get("width")
        candidate["width"] = int(w) if isinstance(w, (int, float)) and w >= 200 else 600
        h = candidate.get("height")
        candidate["height"] = int(h) if isinstance(h, (int, float)) and h >= 180 else 340

    return candidate


def build_inline_vegachart_card_parts(
    surface_id: str,
    vega_spec: Dict[str, Any],
    height: int = 430,
) -> List[types.Part]:
    """Surface 1: Inline Chat `Card` containing ONLY `VegaChart` (zero text/table clutter inside card)."""
    sid = surface_id or f"chart-{uuid.uuid4().hex[:8]}"
    components = [
        {"id": "root", "component": "Card", "child": "vega_chart"},
        {"id": "vega_chart", "component": "VegaChart", "spec": vega_spec, "height": max(380, int(height))},
    ]
    return [
        wrap_a2ui_message({"version": VERSION, "createSurface": {"surfaceId": sid, "catalogId": CATALOG_ID}}),
        wrap_a2ui_message({"version": VERSION, "updateDataModel": {"surfaceId": sid, "path": "/spec", "value": vega_spec}}),
        wrap_a2ui_message({"version": VERSION, "updateComponents": {"surfaceId": sid, "components": components}}),
    ]


def build_explorer_canvas_parts(
    canvas_surface_id: str,
    agent_id: str,
    agent_short_label: str,
    systems: List[Dict[str, Any]],
    source_table_name: str,
    table_rows: List[Dict[str, Any]],
    kpi_summary: Optional[Dict[str, Any]] = None,
    writeback_summary: str = "",
) -> List[types.Part]:
    """Surface 2: Gemini Enterprise Side-Panel `Canvas` (`autoOpen=False`) validated by `validate_a2ui.py`.

    Contains:
    - Single `MaterialColumn` root child (`justify="start"`) — zero 825px flex-band bug.
    - Top `MaterialRow` action bar with interactive `MaterialButton` quick-action events.
    - 3 Collapsible `MaterialExpansionPanel` cards (`<= 62` chars title).
    - Native Looker Studio `RichTable` (`tableData.spec = {}`) with coerced `DOUBLE` & `STRING` columns.
    """
    sid = canvas_surface_id or f"canvas-{uuid.uuid4().hex[:8]}"
    components: List[Dict[str, Any]] = []
    col_children: List[str] = []

    # 1. Top Header & Quick-Action Button Row
    components.append({
        "id": "hdr_title",
        "component": "MaterialText",
        "text": f"{agent_short_label} — Live Enterprise Data & Solver Workbench",
        "usageHint": "subtitle1",
    })
    components.append({
        "id": "btn_outliers",
        "component": "MaterialButton",
        "label": "Audit Top Outliers",
        "variant": "raised",
        "color": "primary",
        "leadingIcon": "analytics",
        "action": {
            "event": {
                "name": "audit_top_outliers",
                "context": {"agent_id": agent_id, "source_table": source_table_name},
            }
        },
    })
    components.append({
        "id": "btn_memo",
        "component": "MaterialButton",
        "label": "Draft Decision Memo",
        "variant": "stroked",
        "color": "primary",
        "leadingIcon": "description",
        "action": {
            "event": {
                "name": "draft_decision_memo",
                "context": {"agent_id": agent_id, "source_table": source_table_name},
            }
        },
    })
    components.append({
        "id": "btn_group",
        "component": "MaterialRow",
        "justify": "end",
        "align": "center",
        "style": {"gap": "8px"},
        "children": ["btn_outliers", "btn_memo"],
    })
    components.append({
        "id": "top_bar",
        "component": "MaterialRow",
        "justify": "spaceBetween",
        "align": "center",
        "children": ["hdr_title", "btn_group"],
    })
    col_children.append("top_bar")

    # 2. Collapsible Expansion Panels (strictly <= 62 char titles, no '#' headings with usageHint)
    sys_lines = []
    for s in (systems or [])[:4]:
        if isinstance(s, dict):
            sn = str(s.get("name", s.get("id", "Enterprise System")))
            sp = str(s.get("protocol", "Enterprise Connector"))
            sys_lines.append(f"• {sn} ({sp})")
    sys_text = "\n".join(sys_lines) if sys_lines else f"• Connected Source Feed: {source_table_name} ({len(table_rows)} live rows)"

    kpi = kpi_summary or {}
    if kpi:
        kpi_bits = [f"{k.replace('_', ' ').title()}: {v}" for k, v in list(kpi.items())[:5]]
        solver_text = " · ".join(kpi_bits)
    else:
        solver_text = f"Evaluated {len(table_rows)} verified records from {source_table_name.replace('_', ' ')} with deterministic constraint & variance checks."

    gov_text = (
        writeback_summary
        or "All write-back mutations enforce pre-execution parameter validation, safety guardrails, and an explicit idempotency key before committing to enterprise systems."
    )

    panel_specs = [
        ("p1", "1. Enterprise Sources & Cortex v7 Data Products", sys_text, True),
        ("p2", "2. Deterministic Solver & Variance Summary", solver_text, True),
        ("p3", "3. Governed Write-Back & Safety Gate", gov_text, False),
    ]
    panel_ids: List[str] = []
    for pid, ptitle, pbody, is_exp in panel_specs:
        safe_title = ptitle[:MAX_PANEL_TITLE]
        txt_id = f"{pid}_body"
        components.append({
            "id": txt_id,
            "component": "MaterialText",
            "text": pbody,
            "usageHint": "body2",
        })
        components.append({
            "id": pid,
            "component": "MaterialExpansionPanel",
            "title": safe_title,
            "expanded": is_exp,
            "children": [txt_id],
            "style": {"marginBottom": "8px"},
        })
        panel_ids.append(pid)

    components.append({
        "id": "panels_card",
        "component": "MaterialCard",
        "appearance": "outlined",
        "style": {"padding": "8px"},
        "children": panel_ids,
    })
    col_children.append("panels_card")

    # 3. Native Looker Studio `RichTable` (`spec: {}`)
    rich_tbl = build_looker_rich_table("source_rich_table", table_rows)
    if rich_tbl is not None:
        clean_tbl_label = source_table_name.replace("_", " ").title()
        components.append({
            "id": "tbl_title",
            "component": "MaterialText",
            "text": f"Live Source Data Grid — {clean_tbl_label}",
            "usageHint": "subtitle1",
            "style": {"marginTop": "8px", "marginBottom": "2px"},
        })
        components.append({
            "id": "tbl_sub",
            "component": "MaterialText",
            "text": f"{min(len(table_rows), 40)} verified enterprise rows · Sort, filter, and chart columns directly in Looker Studio.",
            "usageHint": "caption",
            "style": {"marginTop": "0px", "marginBottom": "10px"},
        })
        components.append(rich_tbl)
        col_children.extend(["tbl_title", "tbl_sub", "source_rich_table"])

    # Single MaterialColumn directly under Canvas root (FDE Rule #3)
    main_col_id = "canvas_main_col"
    main_col = {
        "id": main_col_id,
        "component": "MaterialColumn",
        "justify": "start",
        "align": "stretch",
        "style": {"padding": "16px 20px", "gap": "14px"},
        "children": col_children,
    }
    # Terse <= 20 char tab title (FDE Rule #10)
    short_tab = (agent_short_label[:17].rstrip() + "…") if len(agent_short_label) > 18 else agent_short_label
    root_canvas = {
        "id": "root",
        "component": "Canvas",
        "children": [main_col_id],
        "cardTitle": short_tab or "Data Explorer",
        "cardDescription": f"{len(table_rows)} live rows · {source_table_name.replace('_', ' ')} · Interactive Table & Controls",
        "cardIcon": "table_chart",
        "autoOpen": False,
    }

    all_components = [root_canvas, main_col] + components
    return [
        wrap_a2ui_message({"version": VERSION, "createSurface": {"surfaceId": sid, "catalogId": CATALOG_ID}}),
        wrap_a2ui_message({"version": VERSION, "updateComponents": {"surfaceId": sid, "components": all_components}}),
    ]

"""Dynamic Vega-Lite v5 Chart Spec Builder for [03 · Make | Quality & Compliance] Batch Record Auditor."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

_FIXTURES_DIR = Path(__file__).resolve().parent.parent.parent / "fixtures" / "tables"


def create_batch_record_auditor_chart_spec(
    rows: Optional[List[Dict[str, Any]]] = None,
    title_override: Optional[str] = None,
) -> Dict[str, Any]:
    """Builds a live Vega-Lite v5 grouped comparison spec from enterprise fixture data."""
    if rows is None:
        fpath = _FIXTURES_DIR / "fda_21cfr11_release_signoffs.json"
        if fpath.exists():
            rows = json.loads(fpath.read_text(encoding="utf-8"))
        else:
            rows = []

    values: List[Dict[str, Any]] = []
    for r in rows[:8]:
        lbl = str(r.get("batch_id", "Record"))
        va = float(r.get("manual_review_hrs", 0.0) or 0.0)
        vb = float(r.get("ai_exception_review_hrs", 0.0) or 0.0)
        values.append({"entity": lbl, "series": 'Manual QA Hours', "metric_value": round(va, 2)})
        values.append({"entity": lbl, "series": 'AI Exception Hours', "metric_value": round(vb, 2)})

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": title_override or 'eBHR QA Audit — Manual QA Review Hours vs. AI Review-by-Exception Hours',
            "subtitle": "XYZ Global Industries Corp. (XYZ-CORP-01) · Live Persona Telemetry",
            "anchor": "start",
            "fontSize": 14,
            "subtitleColor": "#64748b",
        },
        "width": "container",
        "height": 300,
        "data": {"values": values},
        "mark": {"type": "bar", "cornerRadiusTopLeft": 4, "cornerRadiusTopRight": 4, "tooltip": True},
        "encoding": {
            "x": {
                "field": "entity",
                "type": "nominal",
                "title": None,
                "axis": {"labelAngle": -25, "labelFontSize": 11},
            },
            "xOffset": {"field": "series"},
            "y": {
                "field": "metric_value",
                "type": "quantitative",
                "title": 'QA Cycle Time (Hours)',
                "axis": {"grid": True, "gridColor": "#e2e8f0"},
            },
            "color": {
                "field": "series",
                "type": "nominal",
                "title": "Metric Series",
                "scale": {
                    "domain": ['Manual QA Hours', 'AI Exception Hours'],
                    "range": ["#64748b", "#2563eb"],
                },
                "legend": {"orient": "top"},
            },
            "tooltip": [
                {"field": "entity", "type": "nominal", "title": "Record"},
                {"field": "series", "type": "nominal", "title": "Series"},
                {"field": "metric_value", "type": "quantitative", "title": "Value", "format": ",.2f"},
            ],
        },
        "config": {"view": {"stroke": "transparent"}, "font": "Inter, system-ui, sans-serif"},
    }

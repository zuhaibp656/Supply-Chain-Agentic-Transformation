"""Dynamic Vega-Lite v5 Chart Spec Builder for [06 · Return | Returns & Claims Mgmt] OS&D Freight Claims Automator."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

_FIXTURES_DIR = Path(__file__).resolve().parent.parent.parent / "fixtures" / "tables"


def create_osd_freight_claims_agent_chart_spec(
    rows: Optional[List[Dict[str, Any]]] = None,
    title_override: Optional[str] = None,
) -> Dict[str, Any]:
    """Builds a live Vega-Lite v5 grouped comparison spec from enterprise fixture data."""
    if rows is None:
        fpath = _FIXTURES_DIR / "osd_carrier_claim_dossiers.json"
        if fpath.exists():
            rows = json.loads(fpath.read_text(encoding="utf-8"))
        else:
            rows = []

    values: List[Dict[str, Any]] = []
    for r in rows[:8]:
        lbl = str(r.get("claim_id", "Record"))
        va = float(r.get("gross_loss_usd", 0.0) or 0.0)
        vb = float(r.get("recoverable_carmack_usd", 0.0) or 0.0)
        values.append({"entity": lbl, "series": 'Gross OS&D Loss ($)', "metric_value": round(va, 2)})
        values.append({"entity": lbl, "series": 'Recoverable Claim ($)', "metric_value": round(vb, 2)})

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": title_override or 'OS&D Freight Claims — Gross Cargo Loss ($) vs. Legally Recoverable Claim ($)',
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
                "title": 'USD',
                "axis": {"grid": True, "gridColor": "#e2e8f0"},
            },
            "color": {
                "field": "series",
                "type": "nominal",
                "title": "Metric Series",
                "scale": {
                    "domain": ['Gross OS&D Loss ($)', 'Recoverable Claim ($)'],
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

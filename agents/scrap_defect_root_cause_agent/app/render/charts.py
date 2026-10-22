"""Vega-Lite chart specifications for YieldMax Scrap Defect Root-Cause Agent."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_scrap_pareto_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a Scrap Loss Pareto Chart with defect quantities and cumulative percentage."""
    if not data_points:
        data_points = [
            {"defect": "Parting Line Flash", "scrap_units": 1420, "cumulative_pct": 58.4, "status": "PRIMARY_ROOT_CAUSE"},
            {"defect": "Thermal Warpage", "scrap_units": 610, "cumulative_pct": 83.5, "status": "SECONDARY_DEFECT"},
            {"defect": "Short Shot Cavity", "scrap_units": 180, "cumulative_pct": 91.0, "status": "TERTIARY_DEFECT"},
            {"defect": "Other Minor Flaws", "scrap_units": 120, "cumulative_pct": 100.0, "status": "RESIDUAL"},
        ]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "YieldMax Scrap Defect Loss Pareto Analysis",
        "title": {
            "text": "YieldMax Scrap Loss Pareto Distribution (Injection Mold IMM-02)",
            "subtitle": "Polymer Parting Flash accounts for 58.4% of Scrap · Holding Pressure Spikes Identified as Root Cause",
            "anchor": "start",
            "fontSize": 14,
            "subtitleFontSize": 11,
            "subtitleColor": "#5f6368"
        },
        "width": 640,
        "height": 280,
        "data": {"values": data_points},
        "layer": [
            {
                "mark": {"type": "bar", "cornerRadiusTopLeft": 4, "cornerRadiusTopRight": 4, "size": 42},
                "encoding": {
                    "x": {"field": "defect", "type": "nominal", "title": "Defect Category", "axis": {"labelAngle": 0}},
                    "y": {"field": "scrap_units", "type": "quantitative", "title": "Scrapped Parts (Pieces)"},
                    "color": {
                        "field": "status",
                        "type": "nominal",
                        "scale": {
                            "domain": ["PRIMARY_ROOT_CAUSE", "SECONDARY_DEFECT", "TERTIARY_DEFECT", "RESIDUAL"],
                            "range": ["#ea4335", "#fbbc04", "#4285f4", "#9aa0a6"]
                        },
                        "title": "Pareto Priority"
                    },
                    "tooltip": [
                        {"field": "defect", "title": "Defect"},
                        {"field": "scrap_units", "title": "Pieces Scrapped"},
                        {"field": "cumulative_pct", "title": "Cumulative (%)"}
                    ]
                }
            },
            {
                "mark": {"type": "line", "point": True, "color": "#188038", "strokeWidth": 2.5},
                "encoding": {
                    "x": {"field": "defect", "type": "nominal"},
                    "y": {
                        "field": "cumulative_pct",
                        "type": "quantitative",
                        "axis": {"title": "Cumulative Scrap (%)", "orient": "right"},
                        "scale": {"domain": [0, 110]}
                    }
                }
            }
        ],
        "resolve": {"scale": {"y": "independent"}}
    }

"""Vega-Lite chart specifications for ReturnLoop — Autonomous RMA Grading & Backhaul Optimizer."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_reverse_rma_optimizer_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a visual Vega-Lite v5 specification for ReturnLoop — Autonomous RMA Grading & Backhaul Optimizer."""
    if not data_points:
        data_points = [
            {
                        "disposition_path": "Grade-A Direct FDC Restock",
                        "recovery_pct": 94.0,
                        "recovered_usd": 9024,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "disposition_path": "Grade-B Certified Refurb",
                        "recovery_pct": 72.5,
                        "recovered_usd": 4640,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "disposition_path": "Grade-C Component Harvest",
                        "recovery_pct": 48.0,
                        "recovered_usd": 3072,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "disposition_path": "Legacy Central Return Hub",
                        "recovery_pct": 38.0,
                        "recovered_usd": 3648,
                        "status": "LEGACY_STATIC"
            }
]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "ReturnLoop Circular Margin Recovery & Backhaul Freight Savings",
        "title": {
            "text": "ReturnLoop Circular Margin Recovery & Backhaul Freight Savings",
            "subtitle": "Gemini 3.8 Flash Optical Triage + Fleet Backhaul (Net Recovery % vs. Value Recovered $)",
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
                "mark": {"type": "bar", "cornerRadiusTopLeft": 4, "cornerRadiusTopRight": 4, "size": 38},
                "encoding": {
                    "x": {"field": "disposition_path", "type": "nominal", "title": "Operational Dimension", "axis": {"labelAngle": 0}},
                    "y": {"field": "recovery_pct", "type": "quantitative", "title": "recovery_pct"},
                    "color": {
                        "field": "status",
                        "type": "nominal",
                        "scale": {
                            "domain": ["OPTIMIZED_CVRPTW", "LEGACY_STATIC"],
                            "range": ["#1e8e3e", "#ea4335"]
                        },
                        "title": "Execution Mode"
                    },
                }
            },
            {
                "mark": {"type": "line", "point": True, "color": "#fbbc04", "strokeWidth": 2.5},
                "encoding": {
                    "x": {"field": "disposition_path", "type": "nominal"},
                    "y": {
                        "field": "recovered_usd",
                        "type": "quantitative",
                        "axis": {"title": "recovered_usd", "orient": "right"},
                    }
                }
            }
        ],
        "resolve": {"scale": {"y": "independent"}}
    }

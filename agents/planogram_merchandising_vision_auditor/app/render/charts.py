"""Vega-Lite chart specifications for ShelfVision — Retail Planogram & Visibility Auditor."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_planogram_merchandising_vision_auditor_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a visual Vega-Lite v5 specification for ShelfVision — Retail Planogram & Visibility Auditor."""
    if not data_points:
        data_points = [
            {
                        "store_segment": "Hyper #882 (Post-ShelfVision)",
                        "sos_pct": 46.8,
                        "osa_pct": 98.2,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "store_segment": "Hyper #882 (Pre-Correction)",
                        "sos_pct": 32.1,
                        "osa_pct": 84.0,
                        "status": "LEGACY_STATIC"
            },
            {
                        "store_segment": "Supermarket #410 (Verified)",
                        "sos_pct": 48.2,
                        "osa_pct": 97.5,
                        "status": "OPTIMIZED_CVRPTW"
            }
]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "ShelfVision Gemini 3.8 Flash Share-of-Shelf (SOS) & OSA Compliance",
        "title": {
            "text": "ShelfVision Gemini 3.8 Flash Share-of-Shelf (SOS) & OSA Compliance",
            "subtitle": "Real-Time In-Store Multimodal Planogram Audit (Share-of-Shelf % Before vs. After In-Store Fix)",
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
                    "x": {"field": "store_segment", "type": "nominal", "title": "Operational Dimension", "axis": {"labelAngle": 0}},
                    "y": {"field": "sos_pct", "type": "quantitative", "title": "sos_pct"},
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
                    "x": {"field": "store_segment", "type": "nominal"},
                    "y": {
                        "field": "osa_pct",
                        "type": "quantitative",
                        "axis": {"title": "osa_pct", "orient": "right"},
                    }
                }
            }
        ],
        "resolve": {"scale": {"y": "independent"}}
    }

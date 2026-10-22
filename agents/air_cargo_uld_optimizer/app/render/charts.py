"""Vega-Lite chart specifications for AeroFreight — Air Cargo Charter, Belly Allocation & 3D ULD Contour Optimizer."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_air_cargo_uld_optimizer_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a visual Vega-Lite v5 specification for AeroFreight — Air Cargo Charter, Belly Allocation & 3D ULD Contour Optimizer."""
    if not data_points:
        data_points = [
            {
                        "uld_unit": "PMC-01 (FRA\u2794ORD Belly)",
                        "volumetric_fill_pct": 89.6,
                        "cost_saved_usd": 4788,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "uld_unit": "LD7-04 (NRT\u2794LAX Belly)",
                        "volumetric_fill_pct": 88.2,
                        "cost_saved_usd": 3920,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "uld_unit": "LD3-09 (AMS\u2794JFK Pharma)",
                        "volumetric_fill_pct": 86.5,
                        "cost_saved_usd": 2840,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "uld_unit": "Manual Ground Handler Pack",
                        "volumetric_fill_pct": 64.0,
                        "cost_saved_usd": 0,
                        "status": "LEGACY_STATIC"
            }
]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "AeroFreight 3D ULD Volumetric Efficiency & Chargeable Weight Savings",
        "title": {
            "text": "AeroFreight 3D ULD Volumetric Efficiency & Chargeable Weight Savings",
            "subtitle": "IATA ONE Record + 3D Contoured ULD Packing (Volumetric Fill % vs. Freight Cost Saved $)",
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
                    "x": {"field": "uld_unit", "type": "nominal", "title": "Operational Dimension", "axis": {"labelAngle": 0}},
                    "y": {"field": "volumetric_fill_pct", "type": "quantitative", "title": "volumetric_fill_pct"},
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
                    "x": {"field": "uld_unit", "type": "nominal"},
                    "y": {
                        "field": "cost_saved_usd",
                        "type": "quantitative",
                        "axis": {"title": "cost_saved_usd", "orient": "right"},
                    }
                }
            }
        ],
        "resolve": {"scale": {"y": "independent"}}
    }

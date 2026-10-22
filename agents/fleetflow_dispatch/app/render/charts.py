"""Vega-Lite chart specifications for FleetFlow — Google Maps Corridor Route & Fleet Dispatch Studio."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_fleetflow_dispatch_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a visual Vega-Lite v5 specification for FleetFlow — Google Maps Corridor Route & Fleet Dispatch Studio."""
    if not data_points:
        data_points = [
            {
                        "corridor": "I-35 Dallas\u2794San Antonio",
                        "distance_km": 462.5,
                        "cube_fill_pct": 91.4,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "corridor": "I-35 Legacy Postcode",
                        "distance_km": 574.0,
                        "cube_fill_pct": 67.0,
                        "status": "LEGACY_STATIC"
            },
            {
                        "corridor": "I-45 Dallas\u2794Houston",
                        "distance_km": 388.0,
                        "cube_fill_pct": 89.2,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "corridor": "I-10 Houston\u2794El Paso",
                        "distance_km": 1190.0,
                        "cube_fill_pct": 93.8,
                        "status": "OPTIMIZED_CVRPTW"
            }
]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "FleetFlow Corridor Route Optimization & Deadhead Reduction",
        "title": {
            "text": "FleetFlow Corridor Route Optimization & Deadhead Reduction",
            "subtitle": "Google Maps Routes Preferred + OR-Tools CVRPTW (km Driven vs. Baseline & Cube Fill %)",
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
                    "x": {"field": "corridor", "type": "nominal", "title": "Operational Dimension", "axis": {"labelAngle": 0}},
                    "y": {"field": "distance_km", "type": "quantitative", "title": "distance_km"},
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
                    "x": {"field": "corridor", "type": "nominal"},
                    "y": {
                        "field": "cube_fill_pct",
                        "type": "quantitative",
                        "axis": {"title": "cube_fill_pct", "orient": "right"},
                    }
                }
            }
        ],
        "resolve": {"scale": {"y": "independent"}}
    }

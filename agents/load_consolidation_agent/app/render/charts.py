"""Vega-Lite chart specifications for CubeMaster 3D — Isometric LIFO Bay & Load Consolidation Studio."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_load_consolidation_agent_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a visual Vega-Lite v5 specification for CubeMaster 3D — Isometric LIFO Bay & Load Consolidation Studio."""
    if not data_points:
        data_points = [
            {
                        "bay_zone": "Zone A (Nose \u00b7 Stop 3)",
                        "cube_fill_pct": 94.2,
                        "weight_kg": 6840,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "bay_zone": "Zone B (Mid \u00b7 Stop 2)",
                        "cube_fill_pct": 92.8,
                        "weight_kg": 6320,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "bay_zone": "Zone C (Tail \u00b7 Stop 1)",
                        "cube_fill_pct": 90.2,
                        "weight_kg": 5300,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "bay_zone": "Legacy Manual Pack",
                        "cube_fill_pct": 68.0,
                        "weight_kg": 12400,
                        "status": "LEGACY_STATIC"
            }
]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "CubeMaster 3D Isometric Bay Utilization & LIFO Zone Fill",
        "title": {
            "text": "CubeMaster 3D Isometric Bay Utilization & LIFO Zone Fill",
            "subtitle": "53ft Dry Van 3D Voxel Packing (92.4% Cube Fill \u00b7 Zero Stop Re-Handling \u00b7 DOT Axle Legal)",
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
                    "x": {"field": "bay_zone", "type": "nominal", "title": "Operational Dimension", "axis": {"labelAngle": 0}},
                    "y": {"field": "cube_fill_pct", "type": "quantitative", "title": "cube_fill_pct"},
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
                    "x": {"field": "bay_zone", "type": "nominal"},
                    "y": {
                        "field": "weight_kg",
                        "type": "quantitative",
                        "axis": {"title": "weight_kg", "orient": "right"},
                    }
                }
            }
        ],
        "resolve": {"scale": {"y": "independent"}}
    }

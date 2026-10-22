"""Vega-Lite chart specifications for CrossDockFlow Transfer Orchestrator."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_crossdock_flow_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a Cross-Dock Flow-Through Pallet Dwell Time & Door Utilization chart."""
    if not data_points:
        data_points = [
            {"door_route": "Door 04 ➔ Bay 12 (Houston)", "dwell_minutes": 18.5, "pallets": 10, "status": "DIRECT_FLOWTHROUGH"},
            {"door_route": "Door 04 ➔ Bay 14 (Austin)", "dwell_minutes": 22.0, "pallets": 8, "status": "DIRECT_FLOWTHROUGH"},
            {"door_route": "Door 02 ➔ Bay 08 (Dallas)", "dwell_minutes": 25.5, "pallets": 14, "status": "DIRECT_FLOWTHROUGH"},
            {"door_route": "Door 06 ➔ Buffer Staging", "dwell_minutes": 145.0, "pallets": 6, "status": "TEMPORARY_STAGED"},
        ]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "CrossDockFlow Real-Time Flow-Through Pallet Dwell Time & Transfer Latency",
        "title": {
            "text": "CrossDockFlow Inbound-to-Outbound Direct Pallet Transfer",
            "subtitle": "Swift Inbound Door 04 Directly Routed to Outbound Bay 12 & 14 (18.5 min Dwell · Zero Staging)",
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
                    "x": {"field": "door_route", "type": "nominal", "title": "Dock-to-Door Transfer Route", "axis": {"labelAngle": 0}},
                    "y": {"field": "dwell_minutes", "type": "quantitative", "title": "Dock Dwell Time (Minutes)"},
                    "color": {
                        "field": "status",
                        "type": "nominal",
                        "scale": {
                            "domain": ["DIRECT_FLOWTHROUGH", "TEMPORARY_STAGED"],
                            "range": ["#1e8e3e", "#ea4335"]
                        },
                        "title": "Transfer Mode"
                    },
                    "tooltip": [
                        {"field": "door_route", "title": "Route"},
                        {"field": "dwell_minutes", "title": "Dwell Time (min)"},
                        {"field": "pallets", "title": "Pallet Quantity"},
                        {"field": "status", "title": "Mode"}
                    ]
                }
            },
            {
                "mark": {"type": "line", "point": True, "color": "#fbbc04", "strokeWidth": 2.5},
                "encoding": {
                    "x": {"field": "door_route", "type": "nominal"},
                    "y": {
                        "field": "pallets",
                        "type": "quantitative",
                        "axis": {"title": "Pallets Transferred", "orient": "right"},
                        "scale": {"domain": [0, 20]}
                    }
                }
            }
        ],
        "resolve": {"scale": {"y": "independent"}}
    }

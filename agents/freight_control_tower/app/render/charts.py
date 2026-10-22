"""Vega-Lite chart specifications for SentinelMove — Multi-Modal In-Transit Control Tower & Freight Auditor."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_freight_control_tower_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a visual Vega-Lite v5 specification for SentinelMove — Multi-Modal In-Transit Control Tower & Freight Auditor."""
    if not data_points:
        data_points = [
            {
                        "invoice_batch": "INV-77410 (Detention+FSC)",
                        "billed_usd": 3490,
                        "overcharge_saved_usd": 615,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "invoice_batch": "INV-77418 (Mileage Audit)",
                        "billed_usd": 4120,
                        "overcharge_saved_usd": 485,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "invoice_batch": "INV-77425 (Accessorial)",
                        "billed_usd": 2890,
                        "overcharge_saved_usd": 390,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "invoice_batch": "Un-Audited Auto-Pay",
                        "billed_usd": 3490,
                        "overcharge_saved_usd": 0,
                        "status": "LEGACY_STATIC"
            }
]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "SentinelMove 3-Way Freight Bill Audit & Cold-Chain Rescue",
        "title": {
            "text": "SentinelMove 3-Way Freight Bill Audit & Cold-Chain Rescue",
            "subtitle": "Geofence + Contract Tariff 3-Way Match (Billed Invoice $ vs. Audited Payable $)",
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
                    "x": {"field": "invoice_batch", "type": "nominal", "title": "Operational Dimension", "axis": {"labelAngle": 0}},
                    "y": {"field": "billed_usd", "type": "quantitative", "title": "billed_usd"},
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
                    "x": {"field": "invoice_batch", "type": "nominal"},
                    "y": {
                        "field": "overcharge_saved_usd",
                        "type": "quantitative",
                        "axis": {"title": "overcharge_saved_usd", "orient": "right"},
                    }
                }
            }
        ],
        "resolve": {"scale": {"y": "independent"}}
    }

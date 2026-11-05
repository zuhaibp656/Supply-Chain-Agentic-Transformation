"""Vega-Lite chart specifications for EchelonFlow MEIO Allocator."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_echelon_inventory_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a Multi-Echelon Stock Distribution & Rebalance chart."""
    if not data_points:
        data_points = [
            {"node": "CDC Mumbai (Bhiwandi) (Tier 1)", "current_stock": 68400, "optimal_safety_stock": 32000, "status": "SURPLUS_POOL"},
            {"node": "RDC Delhi NCR (Gurugram) (Tier 2)", "current_stock": 7200, "optimal_safety_stock": 14200, "status": "DEFICIT_REBALANCED"},
            {"node": "RDC Bengaluru (Nelamangala) (Tier 2)", "current_stock": 24500, "optimal_safety_stock": 11000, "status": "BALANCED_HEALTHY"},
            {"node": "FDC Hyderabad (Shamshabad) (Tier 3)", "current_stock": 4100, "optimal_safety_stock": 4500, "status": "BALANCED_HEALTHY"},
        ]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "EchelonFlow Multi-Echelon Stochastic Inventory Allocation Telemetry",
        "title": {
            "text": "EchelonFlow Multi-Echelon Stock & Safety Buffer Positioning",
            "subtitle": "Clark-Scarf Stochastic Pooling · CDC Surplus Rebalanced to RDC Delhi NCR (Gurugram) (+6,500 Units)",
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
                "mark": {"type": "bar", "cornerRadiusTopLeft": 4, "cornerRadiusTopRight": 4, "size": 36},
                "encoding": {
                    "x": {"field": "node", "type": "nominal", "title": "Network Echelon Node", "axis": {"labelAngle": 0}},
                    "y": {"field": "current_stock", "type": "quantitative", "title": "Current On-Hand Stock (Units)"},
                    "color": {
                        "field": "status",
                        "type": "nominal",
                        "scale": {
                            "domain": ["SURPLUS_POOL", "DEFICIT_REBALANCED", "BALANCED_HEALTHY"],
                            "range": ["#1a73e8", "#ea4335", "#1e8e3e"]
                        },
                        "title": "Node Status"
                    },
                    "tooltip": [
                        {"field": "node", "title": "Node"},
                        {"field": "current_stock", "title": "On-Hand Stock"},
                        {"field": "optimal_safety_stock", "title": "Optimal Safety Stock"},
                        {"field": "status", "title": "Status"}
                    ]
                }
            },
            {
                "mark": {"type": "tick", "color": "#fbbc04", "thickness": 3.5, "size": 42},
                "encoding": {
                    "x": {"field": "node", "type": "nominal"},
                    "y": {"field": "optimal_safety_stock", "type": "quantitative"}
                }
            }
        ]
    }

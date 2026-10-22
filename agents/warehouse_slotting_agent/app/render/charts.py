"""Vega-Lite chart specifications for SlotMaster Warehouse Slotting Optimizer."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_warehouse_slotting_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a Warehouse Aisle Travel Distance & Slotting Velocity chart."""
    if not data_points:
        data_points = [
            {"sku": "Oat Milk 1L (Fast)", "baseline_dist_m": 142.0, "optimized_dist_m": 22.0, "daily_travel_saving_km": 100.8},
            {"sku": "Almond Milk 1L (Med)", "baseline_dist_m": 45.0, "optimized_dist_m": 45.0, "daily_travel_saving_km": 0.0},
            {"sku": "Soy Milk 1L (Med)", "baseline_dist_m": 88.0, "optimized_dist_m": 35.0, "daily_travel_saving_km": 28.5},
            {"sku": "Coconut Milk (Slow)", "baseline_dist_m": 165.0, "optimized_dist_m": 165.0, "daily_travel_saving_km": 0.0},
        ]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "SlotMaster 3D Warehouse Velocity Slotting & Picker Travel Reduction",
        "title": {
            "text": "SlotMaster 3D Warehouse Picker Travel Reduction (RDC Dallas)",
            "subtitle": "Fast-Mover Oat Milk Relocated from Mezzanine Aisle 14 to Golden Zone Aisle 02 (-84.5% Travel)",
            "anchor": "start",
            "fontSize": 14,
            "subtitleFontSize": 11,
            "subtitleColor": "#5f6368"
        },
        "width": 640,
        "height": 280,
        "data": {"values": data_points},
        "transform": [
            {"fold": ["baseline_dist_m", "optimized_dist_m"], "as": ["Metric", "Distance_Meters"]}
        ],
        "mark": {"type": "bar", "cornerRadiusTopLeft": 4, "cornerRadiusTopRight": 4},
        "encoding": {
            "x": {"field": "sku", "type": "nominal", "title": "Product SKU & Velocity Tier", "axis": {"labelAngle": 0}},
            "y": {"field": "Distance_Meters", "type": "quantitative", "title": "Distance to Pack Station (Meters)"},
            "xOffset": {"field": "Metric"},
            "color": {
                "field": "Metric",
                "type": "nominal",
                "scale": {
                    "domain": ["baseline_dist_m", "optimized_dist_m"],
                    "range": ["#ea4335", "#1e8e3e"]
                },
                "legend": {
                    "title": "Slotting Profile",
                    "labelExpr": "datum.value == 'baseline_dist_m' ? 'Baseline Distance (m)' : 'Optimized Golden Zone (m)'"
                }
            },
            "tooltip": [
                {"field": "sku", "title": "SKU"},
                {"field": "Metric", "title": "Profile"},
                {"field": "Distance_Meters", "title": "Travel Distance (m)"},
                {"field": "daily_travel_saving_km", "title": "Daily Travel Saved (km)"}
            ]
        }
    }

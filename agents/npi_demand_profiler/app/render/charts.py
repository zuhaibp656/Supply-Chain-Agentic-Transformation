"""Vega-Lite v5 visual chart specification for [01 · Plan | Demand Forecasting] NPI Demand Profiler."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_npi_demand_profiler_chart_spec(rows: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    data_values = rows or [
        {"unit": "FAC-PLANT-US-AUS01", "Baseline": 78.4, "Optimized": 96.2, "SavingsUSD": 142500},
        {"unit": "FAC-DC-US-DAL02", "Baseline": 81.0, "Optimized": 97.5, "SavingsUSD": 98400},
        {"unit": "FAC-PORT-NL-RTM01", "Baseline": 74.2, "Optimized": 95.8, "SavingsUSD": 116800},
        {"unit": "FAC-PLANT-DE-STR01", "Baseline": 83.6, "Optimized": 98.1, "SavingsUSD": 128900},
    ]
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": "[01 · Plan | Demand Forecasting] NPI Demand Profiler — Performance & ROI Telemetry",
            "subtitle": "Category: 01 · Planning & Strategy — Demand Forecasting | Cuts 90-day launch forecast errors",
            "color": "#f8fafc",
            "subtitleColor": "#94a3b8",
            "fontSize": 15,
            "anchor": "start",
        },
        "width": 640,
        "height": 280,
        "background": "#0b1120",
        "data": {"values": data_values},
        "layer": [
            {
                "mark": {"type": "bar", "cornerRadiusEnd": 6, "color": "#3b82f6", "opacity": 0.88},
                "encoding": {
                    "x": {"field": "unit", "type": "nominal", "title": "Enterprise Facility / Node", "axis": {"labelColor": "#cbd5e1", "titleColor": "#94a3b8", "labelAngle": 0}},
                    "y": {"field": "Optimized", "type": "quantitative", "title": "Optimized Performance Score (%)", "axis": {"labelColor": "#cbd5e1", "titleColor": "#94a3b8", "gridColor": "#1e293b"}},
                },
            },
            {
                "mark": {"type": "line", "point": {"filled": True, "size": 75, "color": "#10b981"}, "color": "#10b981", "strokeWidth": 3},
                "encoding": {
                    "x": {"field": "unit", "type": "nominal"},
                    "y": {"field": "Baseline", "type": "quantitative"},
                },
            },
        ],
        "config": {"view": {"stroke": "transparent"}},
    }

"""Vega-Lite visual chart generators for PulseCast Demand Sensing Engine."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_demand_sensing_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates an executive Vega-Lite v5 multi-layer demand sensing fan chart.
    
    Layers:
    1. P10-P90 Uncertainty Fan Area (shaded purple/blue confidence interval)
    2. P50 TimesFM Probabilistic Forecast line (cyan solid)
    3. Historical POS Sell-Through line (white dashed/solid)
    4. WeatherNext 3 Temperature & Foot-Traffic Shock indicators (amber points)
    """
    if not data_points:
        data_points = [
            {"date": "2026-10-01", "type": "HISTORICAL", "actual_units": 14200, "p50_units": 14200, "p10_units": 14200, "p90_units": 14200, "weather_shock": None},
            {"date": "2026-10-03", "type": "HISTORICAL", "actual_units": 13950, "p50_units": 13950, "p10_units": 13950, "p90_units": 13950, "weather_shock": None},
            {"date": "2026-10-05", "type": "HISTORICAL", "actual_units": 15800, "p50_units": 15800, "p10_units": 15800, "p90_units": 15800, "weather_shock": "HEATWAVE_SURGE"},
            {"date": "2026-10-07", "type": "HISTORICAL", "actual_units": 16400, "p50_units": 16400, "p10_units": 16400, "p90_units": 16400, "weather_shock": None},
            {"date": "2026-10-09", "type": "HISTORICAL", "actual_units": 15200, "p50_units": 15200, "p10_units": 15200, "p90_units": 15200, "weather_shock": None},
            {"date": "2026-10-11", "type": "HISTORICAL", "actual_units": 14800, "p50_units": 14800, "p10_units": 14800, "p90_units": 14800, "weather_shock": None},
            {"date": "2026-10-13", "type": "HISTORICAL", "actual_units": 17200, "p50_units": 17200, "p10_units": 17200, "p90_units": 17200, "weather_shock": "COLD_FRONT"},
            {"date": "2026-10-15", "type": "HISTORICAL", "actual_units": 18100, "p50_units": 18100, "p10_units": 18100, "p90_units": 18100, "weather_shock": None},
            {"date": "2026-10-17", "type": "FORECAST", "actual_units": None, "p50_units": 19400, "p10_units": 17600, "p90_units": 21800, "weather_shock": None},
            {"date": "2026-10-19", "type": "FORECAST", "actual_units": None, "p50_units": 20800, "p10_units": 18400, "p90_units": 23500, "weather_shock": "WEATHERNEXT_STORM"},
            {"date": "2026-10-21", "type": "FORECAST", "actual_units": None, "p50_units": 22100, "p10_units": 19100, "p90_units": 25400, "weather_shock": None},
            {"date": "2026-10-23", "type": "FORECAST", "actual_units": None, "p50_units": 21500, "p10_units": 18200, "p90_units": 24900, "weather_shock": None},
            {"date": "2026-10-25", "type": "FORECAST", "actual_units": None, "p50_units": 23400, "p10_units": 19800, "p90_units": 27200, "weather_shock": "FESTIVE_LIFT"},
            {"date": "2026-10-27", "type": "FORECAST", "actual_units": None, "p50_units": 24100, "p10_units": 20200, "p90_units": 28600, "weather_shock": None},
            {"date": "2026-10-29", "type": "FORECAST", "actual_units": None, "p50_units": 23800, "p10_units": 19500, "p90_units": 28100, "weather_shock": None},
            {"date": "2026-10-31", "type": "FORECAST", "actual_units": None, "p50_units": 25200, "p10_units": 20800, "p90_units": 29800, "weather_shock": "CATEGORY_PEAK"}
        ]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "PulseCast Multi-Signal Demand Sensing & TimesFM Quantile Fan Chart",
        "width": "container",
        "height": 380,
        "background": "#0b0f19",
        "padding": {"top": 16, "left": 18, "right": 18, "bottom": 16},
        "data": {"values": data_points},
        "layer": [
            {
                "mark": {
                    "type": "area",
                    "opacity": 0.22,
                    "color": "#818cf8"
                },
                "encoding": {
                    "x": {"field": "date", "type": "temporal", "title": "Time Horizon (Daily POS + Forecast)"},
                    "y": {"field": "p10_units", "type": "quantitative", "title": "Demand Volume (Units)"},
                    "y2": {"field": "p90_units"}
                }
            },
            {
                "mark": {
                    "type": "line",
                    "color": "#38bdf8",
                    "strokeWidth": 2.5
                },
                "encoding": {
                    "x": {"field": "date", "type": "temporal"},
                    "y": {"field": "p50_units", "type": "quantitative"}
                }
            },
            {
                "mark": {
                    "type": "line",
                    "color": "#ffffff",
                    "strokeWidth": 2,
                    "strokeDash": [4, 4]
                },
                "transform": [{"filter": "datum.actual_units != null"}],
                "encoding": {
                    "x": {"field": "date", "type": "temporal"},
                    "y": {"field": "actual_units", "type": "quantitative"}
                }
            },
            {
                "mark": {
                    "type": "point",
                    "filled": True,
                    "size": 120,
                    "color": "#fbbf24"
                },
                "transform": [{"filter": "datum.weather_shock != null"}],
                "encoding": {
                    "x": {"field": "date", "type": "temporal"},
                    "y": {"field": "p50_units", "type": "quantitative"},
                    "tooltip": [
                        {"field": "date", "type": "temporal", "title": "Event Date"},
                        {"field": "weather_shock", "type": "nominal", "title": "Signal Trigger"},
                        {"field": "p50_units", "type": "quantitative", "title": "P50 Forecast (Units)"}
                    ]
                }
            }
        ],
        "config": {
            "axis": {
                "labelColor": "#94a3b8",
                "titleColor": "#cbd5e1",
                "gridColor": "#1e293b",
                "labelFontSize": 11,
                "titleFontSize": 12
            },
            "view": {"stroke": "transparent"}
        }
    }

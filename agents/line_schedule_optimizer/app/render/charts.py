"""Vega-Lite chart specifications for FlowMaster Finite Production Scheduler."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_finite_schedule_gantt_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates an OR-Tools CP-SAT production sequencing Gantt chart with changeovers."""
    if not data_points:
        data_points = [
            {"task": "Oat Milk Original", "start_hour": 0.0, "end_hour": 6.0, "type": "PRODUCTION_RUN", "volume": "45,000 L"},
            {"task": "Color Flush", "start_hour": 6.0, "end_hour": 6.5, "type": "LIGHT_CHANGEOVER", "volume": "0.5 hr"},
            {"task": "Oat Chocolate", "start_hour": 6.5, "end_hour": 11.5, "type": "PRODUCTION_RUN", "volume": "37,500 L"},
            {"task": "Allergen CIP Wash", "start_hour": 11.5, "end_hour": 15.5, "type": "ALLERGEN_CHANGEOVER", "volume": "4.0 hr CIP"},
            {"task": "Almond Vanilla", "start_hour": 15.5, "end_hour": 19.5, "type": "PRODUCTION_RUN", "volume": "30,000 L"},
        ]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "FlowMaster OR-Tools CP-SAT Finite Production Sequence Schedule",
        "title": {
            "text": "FlowMaster Production Sequence Gantt (Aseptic Filling Line 01)",
            "subtitle": "OR-Tools CP-SAT Minimized Changeover Schedule · 5.0 Hours Changeover Saved",
            "anchor": "start",
            "fontSize": 14,
            "subtitleFontSize": 11,
            "subtitleColor": "#5f6368"
        },
        "width": 640,
        "height": 260,
        "data": {"values": data_points},
        "mark": {"type": "bar", "cornerRadius": 4, "height": 32},
        "encoding": {
            "y": {"field": "task", "type": "nominal", "title": "Scheduled Sequence Block", "sort": None},
            "x": {"field": "start_hour", "type": "quantitative", "title": "Timeline Hours into Production Day (Hrs)"},
            "x2": {"field": "end_hour"},
            "color": {
                "field": "type",
                "type": "nominal",
                "scale": {
                    "domain": ["PRODUCTION_RUN", "LIGHT_CHANGEOVER", "ALLERGEN_CHANGEOVER"],
                    "range": ["#1a73e8", "#fbbc04", "#ea4335"]
                },
                "title": "Block Type"
            },
            "tooltip": [
                {"field": "task", "title": "Block"},
                {"field": "type", "title": "Type"},
                {"field": "start_hour", "title": "Start (hr)"},
                {"field": "end_hour", "title": "End (hr)"},
                {"field": "volume", "title": "Volume / Duration"}
            ]
        }
    }

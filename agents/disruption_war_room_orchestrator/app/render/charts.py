"""Deterministic Vega-Lite Chart Specs for Disruption War Room Orchestrator."""
from __future__ import annotations
from typing import Any, Dict, List, Optional

FONT = "Google Sans, Roboto, Arial, sans-serif"


def create_risk_donut_spec(width: int = 560, height: int = 220) -> Dict[str, Any]:
    """Generates an executive donut chart of at-risk pipeline value by hazard vector."""
    data = [
        {"hazard": "Super Typhoon Gaemi (Taiwan Strait)", "value_m": 8.4, "share": "54.5%"},
        {"hazard": "Antwerp Port Labor Strike (Europe Feeder)", "value_m": 4.2, "share": "27.3%"},
        {"hazard": "Tier-2 Semiconductor Fab Outage", "value_m": 2.8, "share": "18.2%"},
    ]
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": "Multi-Tier Disruption Exposure ($15.4M Pipeline at Risk)",
            "font": FONT,
            "fontSize": 14,
            "fontWeight": "bold",
            "anchor": "start",
            "color": "#202124",
        },
        "width": width,
        "height": height,
        "data": {"values": data},
        "mark": {"type": "arc", "innerRadius": 50, "stroke": "#ffffff", "strokeWidth": 2},
        "encoding": {
            "theta": {"field": "value_m", "type": "quantitative"},
            "color": {
                "field": "hazard",
                "type": "nominal",
                "scale": {"range": ["#d93025", "#f9ab00", "#1a73e8"]},
                "legend": {
                    "orient": "right",
                    "labelFont": FONT,
                    "labelFontSize": 11,
                    "title": None,
                },
            },
            "tooltip": [
                {"field": "hazard", "type": "nominal", "title": "Hazard Vector"},
                {"field": "value_m", "type": "quantitative", "title": "At-Risk ($M)"},
                {"field": "share", "type": "nominal", "title": "Share"},
            ],
        },
        "config": {"view": {"stroke": None}, "background": "#ffffff"},
    }


def create_delay_timeline_spec(width: int = 560, height: int = 200) -> Dict[str, Any]:
    """Generates a comparison bar chart of transit delay vs expedited remediation."""
    data = [
        {"mode": "Scheduled Maritime Transit", "hours": 0, "status": "Baseline Plan", "color": "#188038"},
        {"mode": "Disrupted Ocean Corridor (Typhoon / Strike)", "hours": 126, "status": "Delayed (+5.2d)", "color": "#d93025"},
        {"mode": "Remediated Fast-Track Air Charter", "hours": 18, "status": "Expedited (Line-Down Averted)", "color": "#1a73e8"},
    ]
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": "Transit Duration Impact: Ocean Delay vs Air Expedite (Hours)",
            "font": FONT,
            "fontSize": 14,
            "fontWeight": "bold",
            "anchor": "start",
            "color": "#202124",
        },
        "width": width,
        "height": height,
        "data": {"values": data},
        "mark": {"type": "bar", "cornerRadiusEnd": 4},
        "encoding": {
            "y": {
                "field": "mode",
                "type": "nominal",
                "sort": None,
                "axis": {"labelFont": FONT, "labelFontSize": 11, "title": None, "domain": False},
            },
            "x": {
                "field": "hours",
                "type": "quantitative",
                "axis": {"labelFont": FONT, "labelFontSize": 11, "title": "Transit Duration / Delay (Hours)", "grid": True},
            },
            "color": {
                "field": "color",
                "type": "nominal",
                "scale": None,
            },
            "tooltip": [
                {"field": "mode", "type": "nominal", "title": "Transit Mode"},
                {"field": "hours", "type": "quantitative", "title": "Hours"},
                {"field": "status", "type": "nominal", "title": "Operational Status"},
            ],
        },
        "config": {"view": {"stroke": None}, "background": "#ffffff"},
    }


def create_composite_disruption_spec(width: int = 560) -> Dict[str, Any]:
    """Combines risk donut and delay comparison into a single unified visual."""
    donut = create_risk_donut_spec(width=width, height=200)
    bars = create_delay_timeline_spec(width=width, height=180)

    clean_donut = {k: v for k, v in donut.items() if k != "$schema"}
    clean_bars = {k: v for k, v in bars.items() if k != "$schema"}

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": "StormShield · War Room Disruption Risk & Expedite Infographic",
            "font": FONT,
            "fontSize": 15,
            "fontWeight": "bold",
            "anchor": "start",
            "color": "#202124",
        },
        "vconcat": [clean_donut, clean_bars],
        "config": {"view": {"stroke": None}, "background": "#ffffff"},
    }

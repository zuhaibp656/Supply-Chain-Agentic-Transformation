"""Deterministic Vega-Lite Chart Specs for Working Capital Cash Bridge."""
from __future__ import annotations
from typing import Any, Dict, List, Optional

FONT = "Google Sans, Roboto, Arial, sans-serif"


def create_ccc_waterfall_bars(width: int = 560, height: int = 210) -> Dict[str, Any]:
    """Generates a Cash Conversion Cycle (CCC = DIO + DSO - DPO) waterfall comparison."""
    data = [
        {"metric": "1. Inventory Outstanding (DIO)", "days": 58.4, "component": "Cash Tied Up (+)", "color": "#d93025"},
        {"metric": "2. Sales Outstanding (DSO)", "days": 41.2, "component": "Cash Tied Up (+)", "color": "#f9ab00"},
        {"metric": "3. Payables Outstanding (DPO)", "days": -27.2, "component": "Cash Financed (-)", "color": "#188038"},
        {"metric": "4. Net CCC (Current)", "days": 72.4, "component": "Current Cycle", "color": "#ea4335"},
        {"metric": "5. Net CCC (Optimized Target)", "days": 54.0, "component": "Target Cycle (-18.4d)", "color": "#1a73e8"},
    ]
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": "Cash Conversion Cycle (CCC) Bridge · Days of Working Capital",
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
                "field": "metric",
                "type": "nominal",
                "sort": None,
                "axis": {"labelFont": FONT, "labelFontSize": 11, "title": None, "domain": False},
            },
            "x": {
                "field": "days",
                "type": "quantitative",
                "axis": {"labelFont": FONT, "labelFontSize": 11, "title": "Cycle Impact (Days)", "grid": True},
            },
            "color": {
                "field": "color",
                "type": "nominal",
                "scale": None,
            },
            "tooltip": [
                {"field": "metric", "type": "nominal", "title": "Component"},
                {"field": "days", "type": "quantitative", "title": "Days"},
                {"field": "component", "type": "nominal", "title": "Cycle Impact"},
            ],
        },
        "config": {"view": {"stroke": None}, "background": "#ffffff"},
    }


def create_discount_savings_donut(width: int = 560, height: int = 190) -> Dict[str, Any]:
    """Generates a donut chart of trapped cash unlocked via dynamic AP discounting ($M)."""
    data = [
        {"category": "High-Tech Semiconductors (2/10 Net 60)", "unlocked_m": 12.4, "share": "67.4%"},
        {"category": "Industrial Raw Materials (1.5/15 Net 45)", "unlocked_m": 4.2, "share": "22.8%"},
        {"category": "Packaging & Freight Logistics (1/10 Net 30)", "unlocked_m": 1.8, "share": "9.8%"},
    ]
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": "Dynamic AP Discounting Savings ($18.4M Trapped Cash Unlocked)",
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
            "theta": {"field": "unlocked_m", "type": "quantitative"},
            "color": {
                "field": "category",
                "type": "nominal",
                "scale": {"range": ["#1a73e8", "#f9ab00", "#188038"]},
                "legend": {
                    "orient": "right",
                    "labelFont": FONT,
                    "labelFontSize": 11,
                    "title": None,
                },
            },
            "tooltip": [
                {"field": "category", "type": "nominal", "title": "Category"},
                {"field": "unlocked_m", "type": "quantitative", "title": "Unlocked ($M)"},
                {"field": "share", "type": "nominal", "title": "Share"},
            ],
        },
        "config": {"view": {"stroke": None}, "background": "#ffffff"},
    }


def create_composite_cash_bridge_spec(width: int = 560) -> Dict[str, Any]:
    """Combines CCC waterfall and dynamic discounting savings into an executive infographic."""
    waterfall = create_ccc_waterfall_bars(width=width, height=190)
    donut = create_discount_savings_donut(width=width, height=170)

    clean_waterfall = {k: v for k, v in waterfall.items() if k != "$schema"}
    clean_donut = {k: v for k, v in donut.items() if k != "$schema"}

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": "MarginBridge · Working Capital & CCC Financial Infographic",
            "font": FONT,
            "fontSize": 15,
            "fontWeight": "bold",
            "anchor": "start",
            "color": "#202124",
        },
        "vconcat": [clean_waterfall, clean_donut],
        "config": {"view": {"stroke": None}, "background": "#ffffff"},
    }

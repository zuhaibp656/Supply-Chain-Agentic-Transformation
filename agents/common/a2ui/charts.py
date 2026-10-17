"""Deterministic Vega-Lite v5 Chart Builders for A2UI Surfaces.

Enforces official Google design standards:
- Typography: Google Sans, Roboto, Arial, sans-serif
- Google Palette: #1a73e8 (Blue), #188038 (Green), #f9ab00 (Amber), #d93025 (Red), #5f6368 (Slate)
- Clean axes, subtle gridlines, responsive sizing
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

FONT = "Google Sans, Roboto, Arial, sans-serif"
GOOGLE_PALETTE = ["#1a73e8", "#188038", "#f9ab00", "#d93025", "#8ab4f8", "#81c995", "#fdd663", "#f28b82"]


def create_donut_chart(
    title: str,
    values: List[Dict[str, Any]],
    category_field: str,
    value_field: str,
    width: int = 560,
    height: int = 240,
    colors: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Generates an executive-ready donut / pie chart in Vega-Lite."""
    palette = colors or GOOGLE_PALETTE
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": title,
            "font": FONT,
            "fontSize": 14,
            "fontWeight": "bold",
            "anchor": "start",
            "color": "#202124",
        },
        "width": width,
        "height": height,
        "data": {"values": values},
        "mark": {"type": "arc", "innerRadius": 50, "stroke": "#ffffff", "strokeWidth": 2},
        "encoding": {
            "theta": {"field": value_field, "type": "quantitative"},
            "color": {
                "field": category_field,
                "type": "nominal",
                "scale": {"range": palette},
                "legend": {
                    "orient": "right",
                    "labelFont": FONT,
                    "labelFontSize": 11,
                    "title": None,
                },
            },
            "tooltip": [
                {"field": category_field, "type": "nominal", "title": "Category"},
                {"field": value_field, "type": "quantitative", "title": "Value"},
            ],
        },
        "config": {"view": {"stroke": None}, "background": "#ffffff"},
    }


def create_bar_chart(
    title: str,
    values: List[Dict[str, Any]],
    category_field: str,
    value_field: str,
    threshold: Optional[float] = None,
    threshold_label: str = "Target Threshold",
    horizontal: bool = False,
    width: int = 560,
    height: int = 230,
    bar_color: str = "#1a73e8",
) -> Dict[str, Any]:
    """Generates a clean bar chart with optional threshold rule."""
    cat_enc = {
        "field": category_field,
        "type": "nominal",
        "sort": None,
        "axis": {"labelFont": FONT, "labelFontSize": 11, "title": None, "domain": False, "ticks": False},
    }
    val_enc = {
        "field": value_field,
        "type": "quantitative",
        "axis": {"labelFont": FONT, "labelFontSize": 11, "gridColor": "#f1f3f4"},
    }

    x_enc = val_enc if horizontal else cat_enc
    y_enc = cat_enc if horizontal else val_enc

    layers: List[Dict[str, Any]] = [
        {
            "mark": {"type": "bar", "cornerRadiusEnd": 4, "color": bar_color},
            "encoding": {
                "x": x_enc,
                "y": y_enc,
                "tooltip": [
                    {"field": category_field, "type": "nominal", "title": "Category"},
                    {"field": value_field, "type": "quantitative", "title": "Value"},
                ],
            },
        }
    ]

    if threshold is not None:
        rule_enc = {"x": {"datum": threshold}} if horizontal else {"y": {"datum": threshold}}
        layers.append({
            "mark": {"type": "rule", "color": "#d93025", "strokeWidth": 2, "strokeDash": [4, 4]},
            "encoding": rule_enc,
        })
        text_enc = {
            "x": {"datum": threshold},
            "y": {"value": 15},
            "text": {"value": f"{threshold_label} ({threshold:g})"},
            "color": {"value": "#d93025"},
        } if horizontal else {
            "y": {"datum": threshold},
            "x": {"value": width - 120},
            "text": {"value": f"{threshold_label} ({threshold:g})"},
            "color": {"value": "#d93025"},
        }
        layers.append({
            "mark": {"type": "text", "align": "left", "dx": 5, "font": FONT, "fontSize": 10, "fontWeight": "bold"},
            "encoding": text_enc,
        })

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": title,
            "font": FONT,
            "fontSize": 14,
            "fontWeight": "bold",
            "anchor": "start",
            "color": "#202124",
        },
        "width": width,
        "height": height,
        "data": {"values": values},
        "layer": layers,
        "config": {"view": {"stroke": None}, "background": "#ffffff"},
    }


def create_diverging_bar_chart(
    title: str,
    values: List[Dict[str, Any]],
    category_field: str,
    diff_field: str,
    width: int = 560,
    height: int = 240,
) -> Dict[str, Any]:
    """Generates a diverging bar chart (e.g. positive/negative lead time drift)."""
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": title,
            "font": FONT,
            "fontSize": 14,
            "fontWeight": "bold",
            "anchor": "start",
            "color": "#202124",
        },
        "width": width,
        "height": height,
        "data": {"values": values},
        "mark": {"type": "bar", "cornerRadiusEnd": 3},
        "encoding": {
            "y": {
                "field": category_field,
                "type": "nominal",
                "axis": {"labelFont": FONT, "labelFontSize": 11, "title": None, "domain": False},
            },
            "x": {
                "field": diff_field,
                "type": "quantitative",
                "axis": {"labelFont": FONT, "labelFontSize": 11, "title": "Drift / Variance (Days)", "grid": True},
            },
            "color": {
                "condition": {
                    "test": f"datum.{diff_field} > 0",
                    "value": "#d93025",  # Late / Positive drift is critical
                },
                "value": "#188038",      # On-time or ahead of schedule
            },
            "tooltip": [
                {"field": category_field, "type": "nominal", "title": "Item"},
                {"field": diff_field, "type": "quantitative", "title": "Variance"},
            ],
        },
        "config": {"view": {"stroke": None}, "background": "#ffffff"},
    }


def create_line_chart(
    title: str,
    values: List[Dict[str, Any]],
    x_field: str,
    y_field: str,
    group_field: Optional[str] = None,
    width: int = 560,
    height: int = 220,
) -> Dict[str, Any]:
    """Generates a multi-series or single line graph (e.g. OTIF trend, demand forecast)."""
    color_enc = (
        {"field": group_field, "type": "nominal", "scale": {"range": GOOGLE_PALETTE}, "legend": {"orient": "top", "labelFont": FONT, "title": None}}
        if group_field
        else {"value": "#1a73e8"}
    )
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": title,
            "font": FONT,
            "fontSize": 14,
            "fontWeight": "bold",
            "anchor": "start",
            "color": "#202124",
        },
        "width": width,
        "height": height,
        "data": {"values": values},
        "mark": {"type": "line", "point": {"filled": True, "size": 36}, "strokeWidth": 2.5},
        "encoding": {
            "x": {
                "field": x_field,
                "type": "nominal",
                "axis": {"labelFont": FONT, "labelFontSize": 10, "title": None},
            },
            "y": {
                "field": y_field,
                "type": "quantitative",
                "axis": {"labelFont": FONT, "labelFontSize": 10, "title": None, "gridColor": "#f1f3f4"},
            },
            "color": color_enc,
            "tooltip": [
                {"field": x_field, "type": "nominal", "title": "Period"},
                {"field": y_field, "type": "quantitative", "title": "Value"},
            ],
        },
        "config": {"view": {"stroke": None}, "background": "#ffffff"},
    }


def create_composite_vconcat_chart(
    title: str,
    chart_specs: List[Dict[str, Any]],
    width: int = 560,
) -> Dict[str, Any]:
    """Stacks two or more Vega-Lite specs vertically into a single cohesive infographic."""
    clean_specs = []
    for spec in chart_specs:
        s = {k: v for k, v in spec.items() if k != "$schema"}
        s["width"] = width
        clean_specs.append(s)

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": title,
            "font": FONT,
            "fontSize": 15,
            "fontWeight": "bold",
            "anchor": "start",
            "color": "#202124",
        },
        "vconcat": clean_specs,
        "config": {"view": {"stroke": None}, "background": "#ffffff"},
    }

"""Vega-Lite visual chart generators for Synapse Autonomous S&OP Scenario Weaver."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_sop_tradeoff_spec(
    scenario_data: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates an executive Vega-Lite v5 multi-scenario trade-off comparison chart.
    
    Compares:
    - Baseline Unconstrained
    - Overtime Max-Volume
    - Synapse Balanced Pareto
    Across Revenue ($M), Gross Margin ($M), OTIF (%), and Working Capital Delta ($M).
    """
    if not scenario_data:
        scenario_data = [
            {"scenario": "1. Baseline Unconstrained", "metric": "Gross Margin ($M)", "value": 41.2, "category": "Margin"},
            {"scenario": "2. Overtime Max Volume", "metric": "Gross Margin ($M)", "value": 44.8, "category": "Margin"},
            {"scenario": "3. Synapse Balanced Pareto", "metric": "Gross Margin ($M)", "value": 48.6, "category": "Margin"},
            
            {"scenario": "1. Baseline Unconstrained", "metric": "OTIF Delivery (%)", "value": 91.4, "category": "Service"},
            {"scenario": "2. Overtime Max Volume", "metric": "OTIF Delivery (%)", "value": 99.2, "category": "Service"},
            {"scenario": "3. Synapse Balanced Pareto", "metric": "OTIF Delivery (%)", "value": 98.7, "category": "Service"},
            
            {"scenario": "1. Baseline Unconstrained", "metric": "Working Capital ($M)", "value": 38.5, "category": "Cash"},
            {"scenario": "2. Overtime Max Volume", "metric": "Working Capital ($M)", "value": 46.2, "category": "Cash"},
            {"scenario": "3. Synapse Balanced Pareto", "metric": "Working Capital ($M)", "value": 32.8, "category": "Cash"}
        ]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "Synapse S&OP Multi-Scenario Pareto Trade-Off Matrix",
        "width": "container",
        "height": 380,
        "background": "#0b0f19",
        "padding": {"top": 16, "left": 18, "right": 18, "bottom": 16},
        "data": {"values": scenario_data},
        "facet": {
            "column": {
                "field": "metric",
                "type": "nominal",
                "title": None,
                "header": {
                    "labelColor": "#cbd5e1",
                    "labelFontSize": 12,
                    "labelFontWeight": "bold"
                }
            }
        },
        "spec": {
            "width": 260,
            "height": 280,
            "mark": {"type": "bar", "cornerRadiusTop": 6},
            "encoding": {
                "x": {
                    "field": "scenario",
                    "type": "nominal",
                    "axis": {
                        "labelAngle": -25,
                        "labelColor": "#94a3b8",
                        "labelFontSize": 10,
                        "title": None
                    }
                },
                "y": {
                    "field": "value",
                    "type": "quantitative",
                    "axis": {
                        "gridColor": "#1e293b",
                        "labelColor": "#94a3b8",
                        "title": None
                    }
                },
                "color": {
                    "field": "scenario",
                    "type": "nominal",
                    "scale": {
                        "domain": [
                            "1. Baseline Unconstrained",
                            "2. Overtime Max Volume",
                            "3. Synapse Balanced Pareto"
                        ],
                        "range": ["#64748b", "#f59e0b", "#10b981"]
                    },
                    "legend": None
                },
                "tooltip": [
                    {"field": "scenario", "type": "nominal", "title": "Scenario"},
                    {"field": "metric", "type": "nominal", "title": "KPI"},
                    {"field": "value", "type": "quantitative", "title": "Value"}
                ]
            }
        },
        "config": {
            "view": {"stroke": "transparent"}
        }
    }

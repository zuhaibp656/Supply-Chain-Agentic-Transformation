"""Vega-Lite chart specifications for SchemeGuard — Secondary Trade Payout & Claims Sentinel."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_trade_scheme_claims_reconciler_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a visual Vega-Lite v5 specification for SchemeGuard — Secondary Trade Payout & Claims Sentinel."""
    if not data_points:
        data_points = [
            {
                        "claim_batch": "CLM-9921 (West Zone)",
                        "approved_usd": 16260,
                        "leakage_blocked_usd": 2190,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "claim_batch": "CLM-9928 (North Zone)",
                        "approved_usd": 22400,
                        "leakage_blocked_usd": 3150,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "claim_batch": "Manual 5% Sample Audit",
                        "approved_usd": 18450,
                        "leakage_blocked_usd": 110,
                        "status": "LEGACY_STATIC"
            }
]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "SchemeGuard Trade Spend Leakage Prevention & Settlement Speed",
        "title": {
            "text": "SchemeGuard Trade Spend Leakage Prevention & Settlement Speed",
            "subtitle": "100% Automated Secondary Invoice Audit (Approved Payout $ vs. Leakage Blocked $)",
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
                    "x": {"field": "claim_batch", "type": "nominal", "title": "Operational Dimension", "axis": {"labelAngle": 0}},
                    "y": {"field": "approved_usd", "type": "quantitative", "title": "approved_usd"},
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
                    "x": {"field": "claim_batch", "type": "nominal"},
                    "y": {
                        "field": "leakage_blocked_usd",
                        "type": "quantitative",
                        "axis": {"title": "leakage_blocked_usd", "orient": "right"},
                    }
                }
            }
        ],
        "resolve": {"scale": {"y": "independent"}}
    }

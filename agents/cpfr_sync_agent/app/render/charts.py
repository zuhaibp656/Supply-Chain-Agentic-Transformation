"""Vega-Lite visual chart generators for ChannelSync CPFR Harmonizer."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_cpfr_sync_spec(
    channel_data: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates an executive Vega-Lite v5 CPFR channel harmonization and phantom inventory chart.
    
    Layers:
    1. Daily Retailer EDI 852 Scan Volume (bars)
    2. Joint CPFR Consensus Forecast (line)
    3. Store Phantom Inventory Zero-Scan Stockout Anomalies (pulsing red points)
    """
    if not channel_data:
        channel_data = [
            {"date": "2026-10-01", "store_scans": 48200, "cpfr_consensus": 46500, "phantom_anomaly": None, "osa_pct": 96.2},
            {"date": "2026-10-03", "store_scans": 49100, "cpfr_consensus": 47800, "phantom_anomaly": None, "osa_pct": 96.5},
            {"date": "2026-10-05", "store_scans": 52400, "cpfr_consensus": 51000, "phantom_anomaly": None, "osa_pct": 95.8},
            {"date": "2026-10-07", "store_scans": 44800, "cpfr_consensus": 49500, "phantom_anomaly": "PHANTOM_STOCKOUT_DAL_104", "osa_pct": 92.1},
            {"date": "2026-10-09", "store_scans": 43500, "cpfr_consensus": 50200, "phantom_anomaly": "PHANTOM_STOCKOUT_ATL_209", "osa_pct": 90.4},
            {"date": "2026-10-11", "store_scans": 49800, "cpfr_consensus": 49000, "phantom_anomaly": None, "osa_pct": 95.1},
            {"date": "2026-10-13", "store_scans": 54200, "cpfr_consensus": 52800, "phantom_anomaly": None, "osa_pct": 97.4},
            {"date": "2026-10-15", "store_scans": 56800, "cpfr_consensus": 55100, "phantom_anomaly": None, "osa_pct": 98.2},
            {"date": "2026-10-17", "store_scans": 58900, "cpfr_consensus": 57400, "phantom_anomaly": None, "osa_pct": 98.5}
        ]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "ChannelSync Retailer EDI 852 POS Harmonization & Phantom Inventory Detection",
        "width": "container",
        "height": 380,
        "background": "#0b0f19",
        "padding": {"top": 16, "left": 18, "right": 18, "bottom": 16},
        "data": {"values": channel_data},
        "layer": [
            {
                "mark": {
                    "type": "bar",
                    "color": "#38bdf8",
                    "opacity": 0.65,
                    "cornerRadiusTop": 4
                },
                "encoding": {
                    "x": {"field": "date", "type": "temporal", "title": "Replenishment Timeline"},
                    "y": {"field": "store_scans", "type": "quantitative", "title": "Store Sell-Through (Units)"}
                }
            },
            {
                "mark": {
                    "type": "line",
                    "color": "#10b981",
                    "strokeWidth": 2.5
                },
                "encoding": {
                    "x": {"field": "date", "type": "temporal"},
                    "y": {"field": "cpfr_consensus", "type": "quantitative"}
                }
            },
            {
                "mark": {
                    "type": "point",
                    "filled": True,
                    "size": 150,
                    "color": "#f43f5e"
                },
                "transform": [{"filter": "datum.phantom_anomaly != null"}],
                "encoding": {
                    "x": {"field": "date", "type": "temporal"},
                    "y": {"field": "store_scans", "type": "quantitative"},
                    "tooltip": [
                        {"field": "date", "type": "temporal", "title": "Anomaly Date"},
                        {"field": "phantom_anomaly", "type": "nominal", "title": "Store Phantom Flag"},
                        {"field": "store_scans", "type": "quantitative", "title": "Suppressed Scans"},
                        {"field": "osa_pct", "type": "quantitative", "title": "Retail OSA %"}
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

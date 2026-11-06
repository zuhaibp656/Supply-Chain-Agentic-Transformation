"""A2UI v0.9 Surface Builder for Gemini Enterprise.

Strict Rule: Card renders ONLY the interactive VegaChart visual. All tables, prose, and links stay in Markdown.
"""
from __future__ import annotations

import copy
import math
from typing import Any, Dict, List, Optional

from .a2ui_envelope import wrap_a2ui_part
from .a2ui_lifecycle import (
    build_create_surface,
    build_update_components,
    build_update_data_model,
)
from .charts import create_multimodal_mode_shift_agent_chart_spec


def _clean_json_numbers(obj: Any) -> Any:
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return 0.0
        return obj
    if isinstance(obj, dict):
        return {k: _clean_json_numbers(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_clean_json_numbers(v) for v in obj]
    return obj


def _has_non_empty_data(spec: Dict[str, Any]) -> bool:
    if isinstance(spec.get("data"), dict):
        vals = spec["data"].get("values")
        if isinstance(vals, list) and len(vals) > 0:
            return True
    for key in ("vconcat", "hconcat", "layer"):
        items = spec.get(key)
        if isinstance(items, list):
            for sub in items:
                if isinstance(sub, dict) and _has_non_empty_data(sub):
                    return True
    return False


def _sanitize_vega_spec_for_ge(spec: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Guarantees a Gemini Enterprise v0.9 compliant Vega-Lite v5 spec with numeric dimensions and light theme."""
    candidate = copy.deepcopy(spec) if isinstance(spec, dict) else None
    if not candidate or not _has_non_empty_data(candidate):
        try:
            fallback = create_multimodal_mode_shift_agent_chart_spec()
            if isinstance(fallback, dict) and (_has_non_empty_data(fallback) or not candidate):
                candidate = copy.deepcopy(fallback)
        except Exception:
            pass
    if not isinstance(candidate, dict):
        candidate = {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "width": 620,
            "height": 320,
            "background": "#ffffff",
            "data": {"values": [{"category": "Verified Baseline", "value": 100}]},
            "mark": {"type": "bar", "color": "#2563eb"},
            "encoding": {
                "x": {"field": "category", "type": "nominal"},
                "y": {"field": "value", "type": "quantitative"},
            },
        }

    candidate = _clean_json_numbers(candidate)
    candidate["$schema"] = "https://vega.github.io/schema/vega-lite/v5.json"
    candidate["background"] = "#ffffff"

    cfg = candidate.setdefault("config", {})
    if isinstance(cfg, dict):
        cfg["background"] = "#ffffff"
        view_cfg = cfg.setdefault("view", {})
        if isinstance(view_cfg, dict):
            view_cfg.setdefault("stroke", "transparent")

    if "vconcat" in candidate or "hconcat" in candidate:
        if candidate.get("width") == "container":
            candidate.pop("width", None)
        for concat_key in ("vconcat", "hconcat"):
            panels = candidate.get(concat_key)
            if isinstance(panels, list):
                for panel in panels:
                    if isinstance(panel, dict):
                        panel.pop("$schema", None)
                        pw = panel.get("width")
                        if not isinstance(pw, (int, float)) or pw < 180:
                            panel["width"] = 580
                        else:
                            panel["width"] = int(pw)
                        ph = panel.get("height")
                        if not isinstance(ph, (int, float)) or ph < 150:
                            panel["height"] = 190
                        else:
                            panel["height"] = int(ph)
    else:
        w = candidate.get("width")
        if not isinstance(w, (int, float)) or w < 200:
            candidate["width"] = 620
        else:
            candidate["width"] = int(w)
        h = candidate.get("height")
        if not isinstance(h, (int, float)) or h < 180:
            candidate["height"] = 320
        else:
            candidate["height"] = int(h)

    return candidate


def build_multimodal_mode_shift_agent_surface(
    surface_id: str,
    spec: Optional[Dict[str, Any]] = None,
    height: int = 380,
) -> List[Any]:
    """Emits A2UI v0.9 createSurface + updateDataModel + updateComponents (Card -> VegaChart ONLY)."""
    chart_spec = _sanitize_vega_spec_for_ge(spec)
    if "vconcat" in chart_spec and isinstance(chart_spec["vconcat"], list):
        computed_h = sum(int(p.get("height", 190)) for p in chart_spec["vconcat"] if isinstance(p, dict)) + 110
        card_height = max(int(height), computed_h)
    else:
        card_height = max(int(height), int(chart_spec.get("height", 320)) + 80)

    return [
        wrap_a2ui_part(build_create_surface(surface_id)),
        wrap_a2ui_part(build_update_data_model(surface_id, {"spec": chart_spec})),
        wrap_a2ui_part(
            build_update_components(
                surface_id,
                [
                    {"id": "root", "component": "Card", "child": "chart-wrapper"},
                    {"id": "chart-wrapper", "component": "VegaChart", "spec": chart_spec, "height": card_height},
                ],
            )
        ),
    ]


def build_interactive_html_surface(
    surface_id: str,
    html_content: str,
    title: str = "Interactive Cockpit",
    height: int = 420,
) -> List[Any]:
    """Compatibility shim: Gemini Enterprise Cards strictly render VegaChart visuals (never IFrameSrcdoc)."""
    return build_multimodal_mode_shift_agent_surface(surface_id, spec=None, height=height)

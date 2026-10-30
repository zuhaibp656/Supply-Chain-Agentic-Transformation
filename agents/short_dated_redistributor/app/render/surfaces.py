"""A2UI v0.9 Surface Builder for [06 · Return | Expiry & Markdowns] Short-Dated DC Inventory Redistributor.

Strict Rule: Card renders ONLY the interactive VegaChart visual. All tables/text stay in Markdown.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from .a2ui_envelope import wrap_a2ui_part
from .a2ui_lifecycle import (
    build_create_surface,
    build_update_components,
    build_update_data_model,
)
from .charts import create_short_dated_redistributor_chart_spec


def build_short_dated_redistributor_surface(
    surface_id: str,
    spec: Optional[Dict[str, Any]] = None,
    height: int = 380,
) -> List[Any]:
    """Emits A2UI v0.9 createSurface + updateDataModel + updateComponents (Card -> VegaChart only)."""
    chart_spec = spec or create_short_dated_redistributor_chart_spec()
    return [
        wrap_a2ui_part(build_create_surface(surface_id)),
        wrap_a2ui_part(build_update_data_model(surface_id, {"spec": chart_spec})),
        wrap_a2ui_part(
            build_update_components(
                surface_id,
                [
                    {"id": "root", "component": "Card", "child": "chart-wrapper"},
                    {"id": "chart-wrapper", "component": "VegaChart", "spec": chart_spec, "height": height},
                ],
            )
        ),
    ]

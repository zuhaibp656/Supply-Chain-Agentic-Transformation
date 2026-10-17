"""A2UI Surface Builder for Disruption War Room Orchestrator.

Strictly adheres to user instructions:
Renders ONLY the visual VegaChart inside the Card component, leaving all text,
atomic copy-ready tables, and links for the Markdown response stream.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from .a2ui_envelope import wrap_a2ui_part
from .a2ui_lifecycle import (
    build_create_surface,
    build_update_components,
    build_update_data_model,
)
from .charts import create_composite_disruption_spec


def build_disruption_surface(
    surface_id: str,
    spec: Optional[Dict[str, Any]] = None,
    height: int = 420,
) -> List[Any]:
    """Generates the A2UI parts for the visual Card containing the VegaChart."""
    chart_spec = spec or create_composite_disruption_spec()

    parts = [
        wrap_a2ui_part(build_create_surface(surface_id)),
        wrap_a2ui_part(build_update_components(
            surface_id,
            [
                {
                    "id": "root",
                    "component": "Card",
                    "child": "chart-wrapper",
                },
                {
                    "id": "chart-wrapper",
                    "component": "VegaChart",
                    "spec": chart_spec,
                    "height": height,
                },
            ]
        )),
    ]
    return parts

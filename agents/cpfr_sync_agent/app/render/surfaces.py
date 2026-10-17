"""A2UI Surface Builder for ChannelSync CPFR Harmonizer."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from .a2ui_envelope import wrap_a2ui_part
from .a2ui_lifecycle import (
    build_create_surface,
    build_update_components,
)
from .charts import create_cpfr_sync_spec


def build_cpfr_surface(
    surface_id: str,
    spec: Optional[Dict[str, Any]] = None,
    height: int = 420,
) -> List[Any]:
    """Renders ONLY the visual VegaChart inside the Card component, keeping markdown tables outside."""
    chart_spec = spec or create_cpfr_sync_spec()

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

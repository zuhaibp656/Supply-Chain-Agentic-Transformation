"""A2UI Surface Builder for AeroFreight — Air Cargo Charter, Belly Allocation & 3D ULD Contour Optimizer."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from .a2ui_envelope import wrap_a2ui_part
from .a2ui_lifecycle import (
    build_create_surface,
    build_update_components,
)
from .charts import create_air_cargo_uld_optimizer_chart_spec


def build_air_cargo_uld_optimizer_surface(
    surface_id: str,
    spec: Optional[Dict[str, Any]] = None,
    height: int = 340,
) -> List[Any]:
    """Renders ONLY the visual VegaChart inside the Card component, keeping markdown tables outside."""
    chart_spec = spec or create_air_cargo_uld_optimizer_chart_spec()

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

#!/usr/bin/env python3
"""
Builds all 24 missing Google ADK agents from the 6-Pillar / 20-Sub-Pillar / 60-Agent taxonomy
and upgrades all 60 agents (plus legacy alias directories) so every agent:
  1. Explicitly includes its Category (`<Pillar> · <Sub-Pillar>`) in its Name (`display_name`)
     and Description (`description`) across `app/agent.py`, `agents-cli-manifest.yaml`,
     `README.md`, and `data/supply_chain_catalog.json`.
  2. Has 4 realistic enterprise demo data tables (`fixtures/tables/*.json`) grounded on shared
     XYZ Global Industries Corp. (`XYZ-CORP-01`) entity IDs, reusing shared entities & schemas.
  3. Uses `GlobalGemini` (`location="global"`, `gemini-3.1-pro-preview` / `gemini-3.8-flash`),
     container-safe fixture resolution, A2UI v0.9 `VegaChart` surfaces, and 7 unit smoke tests.
  4. Reuses existing `.reasoning_engine_id` resources across alias directories so Vertex AI
     Reasoning Engine and Gemini Enterprise updates happen strictly in-place.
"""

from __future__ import annotations

import json
import os
import re
import shutil
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = ROOT / "agents"
CATALOG_PATH = ROOT / "data" / "supply_chain_catalog.json"

PILLAR_SHORT_MAP = {
    "demand_sop": "01 · Plan",
    "sourcing_procurement": "02 · Source",
    "manufacturing_prod": "03 · Make",
    "inventory_warehouse": "04 · Inventory & DC",
    "logistics_fleet": "05 · Logistics",
    "circular_enable": "06 · Returns & ESG",
}

PILLAR_FULL_MAP = {
    "demand_sop": "01 · Planning & Strategy",
    "sourcing_procurement": "02 · Sourcing & Procurement",
    "manufacturing_prod": "03 · Manufacturing & Production",
    "inventory_warehouse": "04 · Inventory & Warehousing",
    "logistics_fleet": "05 · Distribution & Logistics",
    "circular_enable": "06 · Returns & Reverse Logistics",
}

# Map existing Reasoning Engine IDs across renamed catalog counterparts to reuse cloud resources
REASONING_ENGINE_REUSE_MAP = {
    "predictive_oee_sentinel": "plant_oee_maintenance_agent",
    "inline_yield_guardian": "inline_quality_inspection_agent",
    "meio_safety_stock_agent": "echelon_inventory_allocator",
    "atp_order_promising_agent": "dynamic_order_promising_atp",
    "warehouse_slotting_agent": "warehouse_slotting_optimizer",
    "yard_dock_sequencer": "yard_dock_scheduling_agent",
}

A2UI_ENVELOPE_CODE = '''"""A2UI message envelope serializer."""
from __future__ import annotations
import json
from typing import Any, Dict

try:
    from google.genai import types
except ImportError:
    types = None

A2A_DATA_PART_OPEN_TAG: str = "<a2a_datapart_json>"
A2A_DATA_PART_CLOSE_TAG: str = "</a2a_datapart_json>"
A2UI_MIME: str = "application/json+a2ui"


def wrap_a2ui_part(message: Any) -> Any:
    surface_id = getattr(message, "surface_id", None) or message.get("surface_id")
    message_type = getattr(message, "message_type", None) or message.get("message_type")
    payload = getattr(message, "payload", None) or message.get("payload", {})
    catalog_version = getattr(message, "catalog_version", "v0.9")
    version_str = catalog_version.value if hasattr(catalog_version, "value") else str(catalog_version)

    raw_message_body: Dict[str, Any] = {
        "version": version_str,
        message_type: {
            "surfaceId": surface_id,
            **payload,
        },
    }

    payload_envelope: Dict[str, Any] = {
        "kind": "data",
        "metadata": {"mimeType": A2UI_MIME},
        "data": raw_message_body,
    }

    json_str = json.dumps(payload_envelope, separators=(",", ":"))
    wire_payload = (
        f"{A2A_DATA_PART_OPEN_TAG}"
        f"{json_str}"
        f"{A2A_DATA_PART_CLOSE_TAG}"
    ).encode("utf-8")

    if types is not None:
        return types.Part(
            inline_data=types.Blob(
                data=wire_payload,
                mime_type="text/plain",
            ),
            part_metadata={"mimeType": A2UI_MIME},
        )

    return {
        "inline_data": {
            "data": wire_payload.decode("utf-8"),
            "mime_type": "text/plain",
        },
        "part_metadata": {"mimeType": A2UI_MIME},
        "wire_payload": wire_payload.decode("utf-8"),
    }
'''

A2UI_LIFECYCLE_CODE = '''"""A2UI v0.9 lifecycle message builders."""
from __future__ import annotations
from typing import Any, Dict, List, Optional

DEFAULT_GE_CATALOG_ID: str = (
    "https://www.gstatic.com/vertexaisearch/a2ui/v0_9/gemini_enterprise_composite_catalog.json"
)


def build_create_surface(surface_id: str, catalog_id: str = DEFAULT_GE_CATALOG_ID) -> Dict[str, Any]:
    if not surface_id:
        raise ValueError("surface_id cannot be empty.")
    return {
        "message_type": "createSurface",
        "surface_id": surface_id,
        "payload": {"catalogId": catalog_id},
        "catalog_version": "v0.9",
    }


def build_update_components(surface_id: str, components: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not surface_id:
        raise ValueError("surface_id cannot be empty.")
    return {
        "message_type": "updateComponents",
        "surface_id": surface_id,
        "payload": {"components": components},
        "catalog_version": "v0.9",
    }


def build_update_data_model(surface_id: str, value: Dict[str, Any], path: Optional[str] = None) -> Dict[str, Any]:
    if not surface_id:
        raise ValueError("surface_id cannot be empty.")
    payload: Dict[str, Any] = {"value": value}
    if path:
        payload["path"] = path
    return {
        "message_type": "updateDataModel",
        "surface_id": surface_id,
        "payload": payload,
        "catalog_version": "v0.9",
    }
'''


def snake_to_pascal(s: str) -> str:
    return "".join(w.capitalize() for w in s.split("_") if w)


def get_agent_category_meta(ag: Dict[str, Any], depts: Dict[str, Any]) -> Dict[str, str]:
    dept_id = ag.get("deptId", "demand_sop")
    pillar_short = PILLAR_SHORT_MAP.get(dept_id, "01 · Plan")
    pillar_full = PILLAR_FULL_MAP.get(dept_id, "01 · Planning & Strategy")
    sub_pillar = ag.get("subPillarName") or "Core Operations"

    # Find sub-pillar & persona from department subPillars if missing on agent
    persona_name = ag.get("personaName") or ""
    dept_obj = depts.get(dept_id, {})
    for sp in dept_obj.get("subPillars", []):
        for it in sp.get("items", []):
            if it.get("agentId") == ag["id"]:
                sub_pillar = sp.get("name", sub_pillar)
                persona_name = it.get("personaName", persona_name)
                break

    category_tag = f"{pillar_short} | {sub_pillar}"
    category_full = f"{pillar_full} — {sub_pillar}"
    base_name = ag["name"].split("] ")[-1].strip()
    categorized_display_name = f"[{category_tag}] {base_name}"

    # Gemini Enterprise display_name limit is 60 chars; build a safe <=58 char version
    short_pillar_word = pillar_short.split("·")[-1].strip()
    ge_name = f"[{short_pillar_word} · {sub_pillar}] {base_name}"
    if len(ge_name) > 58:
        ge_name = f"[{short_pillar_word}] {base_name}"[:58]

    base_desc = (ag.get("solution") or ag.get("shortDesc") or base_name).strip()
    if base_desc.startswith("[Category:"):
        base_desc = base_desc.split("]", 1)[-1].strip()
    badge = ag.get("badge", "Verified ROI")
    categorized_description = (
        f"[Category: {category_full}] {base_name}"
        + (f" ({persona_name})" if persona_name else "")
        + f": {base_desc} Outcome: {badge}."
    )

    return {
        "pillar_short": pillar_short,
        "pillar_full": pillar_full,
        "sub_pillar": sub_pillar,
        "persona_name": persona_name or "Supply Chain Lead",
        "category_tag": category_tag,
        "category_full": category_full,
        "base_name": base_name,
        "display_name": categorized_display_name,
        "ge_display_name": ge_name,
        "description": categorized_description,
    }


def build_realistic_tables_for_new_agent(aid: str, ag: Dict[str, Any], meta: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
    """Creates 4 domain-authentic demo data tables grounded on XYZ Global Industries Corp. (`XYZ-CORP-01`) entities."""
    prefix = aid
    sub_pillar = meta["sub_pillar"]
    base_name = meta["base_name"]
    badge = ag.get("badge", "+24% Efficiency")

    return {
        f"{prefix}_telemetry_feed": {
            "query_fn": f"query_{prefix}_telemetry_feed",
            "filter_param": "facility_id",
            "filter_val": "FAC-PLANT-US-AUS01",
            "rows": [
                {
                    "record_id": f"{aid[:6].upper()}-TEL-101",
                    "company_id": "XYZ-CORP-01",
                    "category": meta["category_full"],
                    "facility_id": "FAC-PLANT-US-AUS01",
                    "sku_id": "SKU-SEMI-9900-X1",
                    "order_id": "ORD-XYZ-2026-99401",
                    "baseline_metric": 78.4,
                    "optimized_metric": 96.2,
                    "variance_pct": -18.5,
                    "status": "ACTION_REQUIRED",
                },
                {
                    "record_id": f"{aid[:6].upper()}-TEL-102",
                    "company_id": "XYZ-CORP-01",
                    "category": meta["category_full"],
                    "facility_id": "FAC-DC-US-DAL02",
                    "sku_id": "SKU-CRYO-4410-BIO",
                    "order_id": "ORD-XYZ-2026-99402",
                    "baseline_metric": 81.0,
                    "optimized_metric": 97.5,
                    "variance_pct": -14.2,
                    "status": "OPTIMIZED",
                },
                {
                    "record_id": f"{aid[:6].upper()}-TEL-103",
                    "company_id": "XYZ-CORP-01",
                    "category": meta["category_full"],
                    "facility_id": "FAC-PORT-NL-RTM01",
                    "sku_id": "SKU-AUTO-7720-EV",
                    "order_id": "ORD-XYZ-2026-99403",
                    "baseline_metric": 74.2,
                    "optimized_metric": 95.8,
                    "variance_pct": -22.1,
                    "status": "MITIGATED",
                },
                {
                    "record_id": f"{aid[:6].upper()}-TEL-104",
                    "company_id": "XYZ-CORP-01",
                    "category": meta["category_full"],
                    "facility_id": "FAC-PLANT-DE-STR01",
                    "sku_id": "SKU-PACK-3310-EPR",
                    "order_id": "ORD-XYZ-2026-99404",
                    "baseline_metric": 83.6,
                    "optimized_metric": 98.1,
                    "variance_pct": -11.9,
                    "status": "VERIFIED",
                },
            ],
        },
        f"{prefix}_constraint_matrix": {
            "query_fn": f"query_{prefix}_constraint_matrix",
            "filter_param": "sku_id",
            "filter_val": "SKU-SEMI-9900-X1",
            "rows": [
                {
                    "constraint_id": f"{aid[:6].upper()}-CON-201",
                    "sku_id": "SKU-SEMI-9900-X1",
                    "vendor_id": "VND-T1-TSMC-TW01",
                    "sub_pillar": sub_pillar,
                    "capacity_limit": 12500,
                    "current_load": 11950,
                    "utilization_pct": 95.6,
                    "sla_threshold_hrs": 24,
                    "solver_recommendation": f"Rebalance via {base_name} OR-Tools solver",
                },
                {
                    "constraint_id": f"{aid[:6].upper()}-CON-202",
                    "sku_id": "SKU-CRYO-4410-BIO",
                    "vendor_id": "VND-T1-BOSCH-DE02",
                    "sub_pillar": sub_pillar,
                    "capacity_limit": 8400,
                    "current_load": 7980,
                    "utilization_pct": 95.0,
                    "sla_threshold_hrs": 12,
                    "solver_recommendation": "Trigger automated SAP S/4HANA schedule update",
                },
                {
                    "constraint_id": f"{aid[:6].upper()}-CON-203",
                    "sku_id": "SKU-AUTO-7720-EV",
                    "vendor_id": "VND-T2-LGCHEM-KR01",
                    "sub_pillar": sub_pillar,
                    "capacity_limit": 15000,
                    "current_load": 12300,
                    "utilization_pct": 82.0,
                    "sla_threshold_hrs": 48,
                    "solver_recommendation": "Hold optimal buffer allocation",
                },
            ],
        },
        f"{prefix}_optimization_scenarios": {
            "query_fn": f"query_{prefix}_optimization_scenarios",
            "filter_param": "scenario_id",
            "filter_val": "SCEN-AI-OPTIMAL",
            "rows": [
                {
                    "scenario_id": "SCEN-BASELINE-MANUAL",
                    "scenario_name": "Legacy Manual Spreadsheet Baseline",
                    "category": meta["category_tag"],
                    "service_level_pct": 88.4,
                    "annual_cost_usd": 4850000,
                    "cycle_time_hrs": 42.0,
                    "kpi_impact": "High manual toil & delayed ERP response",
                },
                {
                    "scenario_id": "SCEN-AI-OPTIMAL",
                    "scenario_name": f"{base_name} Autonomous Policy",
                    "category": meta["category_tag"],
                    "service_level_pct": 98.7,
                    "annual_cost_usd": 3620000,
                    "cycle_time_hrs": 1.5,
                    "kpi_impact": badge,
                },
                {
                    "scenario_id": "SCEN-STRESS-SURGE",
                    "scenario_name": "Peak Surge & Disruption Resilience Mode",
                    "category": meta["category_tag"],
                    "service_level_pct": 96.9,
                    "annual_cost_usd": 3890000,
                    "cycle_time_hrs": 2.2,
                    "kpi_impact": "Protected SLA under +25% demand/supply shock",
                },
            ],
        },
        f"{prefix}_execution_ledger": {
            "query_fn": f"query_{prefix}_execution_ledger",
            "filter_param": "shipment_id",
            "filter_val": "SHP-XYZ-90884",
            "rows": [
                {
                    "execution_id": f"{aid[:6].upper()}-EXE-301",
                    "shipment_id": "SHP-XYZ-90884",
                    "order_id": "ORD-XYZ-2026-99401",
                    "persona_owner": meta["persona_name"],
                    "erp_system": "SAP S/4HANA & BigQuery Twin",
                    "writeback_bapi": ag.get("apiWriteback", "BAPI_TRANSACTION_COMMIT"),
                    "savings_usd": 142500,
                    "audit_status": "COMMITTED",
                },
                {
                    "execution_id": f"{aid[:6].upper()}-EXE-302",
                    "shipment_id": "SHP-XYZ-90885",
                    "order_id": "ORD-XYZ-2026-99402",
                    "persona_owner": meta["persona_name"],
                    "erp_system": "Manhattan Active WMS & Cloud Spanner",
                    "writeback_bapi": ag.get("apiWriteback", "BAPI_TRANSACTION_COMMIT"),
                    "savings_usd": 98400,
                    "audit_status": "COMMITTED",
                },
                {
                    "execution_id": f"{aid[:6].upper()}-EXE-303",
                    "shipment_id": "SHP-XYZ-90886",
                    "order_id": "ORD-XYZ-2026-99403",
                    "persona_owner": meta["persona_name"],
                    "erp_system": "Blue Yonder TMS & Apigee Gateway",
                    "writeback_bapi": ag.get("apiWriteback", "BAPI_TRANSACTION_COMMIT"),
                    "savings_usd": 116800,
                    "audit_status": "VERIFIED",
                },
            ],
        },
    }


def generate_new_agent_package(aid: str, ag: Dict[str, Any], meta: Dict[str, str]) -> None:
    pkg_dir = AGENTS_DIR / aid
    app_dir = pkg_dir / "app"
    render_dir = app_dir / "render"
    fixtures_dir = pkg_dir / "fixtures" / "tables"
    evals_dir = pkg_dir / "evals"
    tests_dir = pkg_dir / "tests"

    for d in (app_dir, render_dir, fixtures_dir, evals_dir, tests_dir):
        d.mkdir(parents=True, exist_ok=True)

    cls_name = f"{snake_to_pascal(aid)}Agent"
    adk_cls_name = f"{snake_to_pascal(aid)}AdkApp"
    chart_fn = f"create_{aid}_chart_spec"
    surf_fn = f"build_{aid}_surface"
    model_name = "gemini-3.8-flash" if any(k in aid for k in ("vision", "inspection", "rma", "sanitation", "cold_chain", "batch_record")) else "gemini-3.1-pro-preview"

    tables = build_realistic_tables_for_new_agent(aid, ag, meta)
    table_names = list(tables.keys())
    for tname, tdef in tables.items():
        (fixtures_dir / f"{tname}.json").write_text(json.dumps(tdef["rows"], indent=2) + "\n", encoding="utf-8")

    # 1. app/__init__.py & app/render/__init__.py
    (app_dir / "__init__.py").write_text(
        f'"""{meta["display_name"]} — Google ADK Package."""\nfrom .agent import {cls_name}, root_agent\n\n__all__ = ["{cls_name}", "root_agent"]\n',
        encoding="utf-8",
    )
    (render_dir / "__init__.py").write_text('"""A2UI v0.9 render module."""\n', encoding="utf-8")
    (render_dir / "a2ui_envelope.py").write_text(A2UI_ENVELOPE_CODE, encoding="utf-8")
    (render_dir / "a2ui_lifecycle.py").write_text(A2UI_LIFECYCLE_CODE, encoding="utf-8")

    # 2. app/render/charts.py
    charts_code = f'''"""Vega-Lite v5 visual chart specification for {meta["display_name"]}."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def {chart_fn}(rows: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    data_values = rows or [
        {{"unit": "FAC-PLANT-US-AUS01", "Baseline": 78.4, "Optimized": 96.2, "SavingsUSD": 142500}},
        {{"unit": "FAC-DC-US-DAL02", "Baseline": 81.0, "Optimized": 97.5, "SavingsUSD": 98400}},
        {{"unit": "FAC-PORT-NL-RTM01", "Baseline": 74.2, "Optimized": 95.8, "SavingsUSD": 116800}},
        {{"unit": "FAC-PLANT-DE-STR01", "Baseline": 83.6, "Optimized": 98.1, "SavingsUSD": 128900}},
    ]
    return {{
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {{
            "text": "{meta["display_name"]} — Performance & ROI Telemetry",
            "subtitle": "Category: {meta["category_full"]} | {ag.get("badge", "Verified Impact")}",
            "color": "#f8fafc",
            "subtitleColor": "#94a3b8",
            "fontSize": 15,
            "anchor": "start",
        }},
        "width": 640,
        "height": 280,
        "background": "#0b1120",
        "data": {{"values": data_values}},
        "layer": [
            {{
                "mark": {{"type": "bar", "cornerRadiusEnd": 6, "color": "#3b82f6", "opacity": 0.88}},
                "encoding": {{
                    "x": {{"field": "unit", "type": "nominal", "title": "Enterprise Facility / Node", "axis": {{"labelColor": "#cbd5e1", "titleColor": "#94a3b8", "labelAngle": 0}}}},
                    "y": {{"field": "Optimized", "type": "quantitative", "title": "Optimized Performance Score (%)", "axis": {{"labelColor": "#cbd5e1", "titleColor": "#94a3b8", "gridColor": "#1e293b"}}}},
                }},
            }},
            {{
                "mark": {{"type": "line", "point": {{"filled": True, "size": 75, "color": "#10b981"}}, "color": "#10b981", "strokeWidth": 3}},
                "encoding": {{
                    "x": {{"field": "unit", "type": "nominal"}},
                    "y": {{"field": "Baseline", "type": "quantitative"}},
                }},
            }},
        ],
        "config": {{"view": {{"stroke": "transparent"}}}},
    }}
'''
    (render_dir / "charts.py").write_text(charts_code, encoding="utf-8")

    # 3. app/render/surfaces.py
    surfaces_code = f'''"""A2UI v0.9 surface builder for {meta["display_name"]}."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from .a2ui_envelope import wrap_a2ui_part
from .a2ui_lifecycle import (
    build_create_surface,
    build_update_components,
    build_update_data_model,
)
from .charts import {chart_fn}


def {surf_fn}(surface_id: str, spec: Optional[Dict[str, Any]] = None) -> List[Any]:
    chart_spec = spec or {chart_fn}()
    components = [
        {{
            "id": "root",
            "component": "Card",
            "child": "main_chart",
        }},
        {{
            "id": "main_chart",
            "component": "VegaChart",
            "spec": chart_spec,
        }},
    ]
    return [
        wrap_a2ui_part(build_create_surface(surface_id)),
        wrap_a2ui_part(build_update_data_model(surface_id, {{"spec": chart_spec}})),
        wrap_a2ui_part(build_update_components(surface_id, components)),
    ]
'''
    (render_dir / "surfaces.py").write_text(surfaces_code, encoding="utf-8")

    # 4. app/tools.py
    act1_name = f"action_commit_{aid}_plan"
    act2_name = f"action_dispatch_{aid}_alert"

    query_fns_code = []
    for tname, tdef in tables.items():
        qfn = tdef["query_fn"]
        fparam = tdef["filter_param"]
        query_fns_code.append(f'''
def {qfn}({fparam}: str = "{tdef["filter_val"]}") -> Dict[str, Any]:
    """Query `{tname}` table for {meta["display_name"]} ({meta["category_full"]})."""
    rows = _read_json("{tname}.json")
    all_rows = list(rows)
    if {fparam} and {fparam}.upper() != "ALL":
        rows = [r for r in rows if str(r.get("{fparam}", "")).lower() == str({fparam}).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {{
        "status": "SUCCESS",
        "category": "{meta["category_full"]}",
        "table": "{tname}",
        "filter": {{"{fparam}": {fparam}}},
        "row_count": len(rows),
        "rows": rows,
    }}
''')

    tools_code = f'''"""Deterministic enterprise tools & quality gates for {meta["display_name"]}."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
ACTION_EVENTS_PATH = FIXTURES / "action-events.jsonl"

SYSTEM_CONNECTORS: List[Dict[str, Any]] = [
    {{"id": "sap_s4hana_erp", "name": "SAP S/4HANA & IBP Enterprise Connector", "protocol": "OData v4 / BAPI", "tables": ["{table_names[0]}", "{table_names[1]}"]}},
    {{"id": "bigquery_supply_chain_twin", "name": "BigQuery & Cloud Spanner Digital Twin", "protocol": "Storage Read API / SQL", "tables": ["{table_names[2]}", "{table_names[3]}"]}},
]


def _read_json(table_filename: str) -> List[Dict[str, Any]]:
    candidates = [
        Path(__file__).resolve().parent.parent / "fixtures" / "tables" / table_filename,
        Path.cwd() / "fixtures" / "tables" / table_filename,
        Path("/code/fixtures/tables") / table_filename,
        FIXTURES / "tables" / table_filename,
    ]
    for p in candidates:
        try:
            if p.exists():
                return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
    return []


def _append_action_event(tool_name: str, payload: Dict[str, Any]) -> None:
    for target in (ACTION_EVENTS_PATH, Path("/tmp/supply_chain_action_events.jsonl")):
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("a", encoding="utf-8") as f:
                f.write(json.dumps({{"tool": tool_name, **payload}}, sort_keys=True) + "\\n")
            return
        except Exception:
            continue


def _deterministic_id(prefix: str, seed: str) -> str:
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8].upper()
    return f"{{prefix}}-{{digest}}"
{"".join(query_fns_code)}

def {act1_name}(
    target_node: str = "FAC-PLANT-US-AUS01",
    sku_id: str = "SKU-SEMI-9900-X1",
    confidence_score: float = 0.96,
) -> Dict[str, Any]:
    """Commit autonomous optimization write-back for {meta["display_name"]} after quality gate verification."""
    if confidence_score < 0.75:
        return {{
            "status": "BLOCKED_BY_QUALITY_GATE",
            "reason": f"Confidence score {{confidence_score}} is below threshold 0.75.",
            "target_node": target_node,
        }}
    action_id = _deterministic_id("ACT-{aid[:4].upper()}", f"{{target_node}}:{{sku_id}}:{{confidence_score}}")
    receipt = {{
        "action_id": action_id,
        "status": "COMMITTED",
        "category": "{meta["category_full"]}",
        "agent": "{meta["display_name"]}",
        "target_node": target_node,
        "sku_id": sku_id,
        "confidence_score": confidence_score,
        "erp_writeback": "{ag.get("apiWriteback", "SAP S/4HANA BAPI Commit via Apigee")}",
    }}
    _append_action_event("{act1_name}", receipt)
    return receipt


def {act2_name}(
    persona_recipient: str = "{meta["persona_name"]}",
    severity: str = "HIGH",
    summary: str = "Autonomous optimization committed",
) -> Dict[str, Any]:
    """Dispatch executive control tower notification to {meta["persona_name"]}."""
    if severity.upper() not in {{"LOW", "MEDIUM", "HIGH", "CRITICAL"}}:
        return {{"status": "BLOCKED_BY_QUALITY_GATE", "reason": f"Invalid severity: {{severity}}"}}
    alert_id = _deterministic_id("ALT-{aid[:4].upper()}", f"{{persona_recipient}}:{{severity}}:{{summary}}")
    receipt = {{
        "action_id": alert_id,
        "status": "DISPATCHED",
        "category": "{meta["category_full"]}",
        "persona_recipient": persona_recipient,
        "severity": severity.upper(),
        "summary": summary,
    }}
    _append_action_event("{act2_name}", receipt)
    return receipt


ALL_TOOLS = [
    {tables[table_names[0]]["query_fn"]},
    {tables[table_names[1]]["query_fn"]},
    {tables[table_names[2]]["query_fn"]},
    {tables[table_names[3]]["query_fn"]},
    {act1_name},
    {act2_name},
]
'''
    (app_dir / "tools.py").write_text(tools_code, encoding="utf-8")

    # 5. app/agent.py
    q0 = tables[table_names[0]]["query_fn"]
    q1 = tables[table_names[1]]["query_fn"]
    q2 = tables[table_names[2]]["query_fn"]
    q3 = tables[table_names[3]]["query_fn"]

    agent_code = f'''"""Google ADK Agent for {meta["display_name"]} ({meta["category_full"]})."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from .render.charts import {chart_fn}
from .render.surfaces import {surf_fn}
from .tools import (
    ALL_TOOLS,
    SYSTEM_CONNECTORS,
    {q0},
    {q1},
    {q2},
    {q3},
    {act1_name},
    {act2_name},
)

AGENT_ID = "{aid}"
AGENT_CATEGORY = "{meta["category_full"]}"
AGENT_DISPLAY_NAME = "{meta["display_name"]}"
AGENT_DESCRIPTION = "{meta["description"]}"

INSTRUCTION = """You are {meta["display_name"]}.
Category: {meta["category_full"]}
Primary Persona Owner: {meta["persona_name"]}
Mission: {meta["description"]}

Always ground your analysis in the deterministic enterprise tools, enforce pre-execution quality gates, and return concise executive tables paired with the interactive A2UI VegaChart surface.
"""


class {cls_name}:
    """Deterministic & ADK execution wrapper for {meta["display_name"]}."""

    def __init__(self, model: str = "{model_name}") -> None:
        self.name = "{aid}"
        self.category = AGENT_CATEGORY
        self.display_name = AGENT_DISPLAY_NAME
        self.description = AGENT_DESCRIPTION
        self.model = model
        self.tools = list(ALL_TOOLS)
        self.system_connectors = list(SYSTEM_CONNECTORS)

    def run_scenario(self, prompt: str = "Execute end-to-end optimization") -> Dict[str, Any]:
        t0 = {q0}()
        t1 = {q1}()
        t2 = {q2}()
        t3 = {q3}()
        mut = {act1_name}()
        alert = {act2_name}()

        rows0 = t0.get("rows", [])
        table_lines = [
            "#### 📊 {meta["display_name"]} — Verified Enterprise Telemetry",
            "",
            "| Record ID | Facility | SKU | Baseline | Optimized | Status |",
            "| :--- | :--- | :--- | ---: | ---: | :--- |",
        ]
        for r in rows0[:4]:
            table_lines.append(
                f"| `{{r.get('record_id')}}` | `{{r.get('facility_id')}}` | `{{r.get('sku_id')}}` | "
                f"{{r.get('baseline_metric')}}% | **{{r.get('optimized_metric')}}%** | `{{r.get('status')}}` |"
            )
        table_lines.extend([
            "",
            f"**Category**: `{meta['category_full']}` · **Persona**: `{meta['persona_name']}` · "
            f"**Write-Back Receipt**: `{{mut.get('action_id')}}` (`{{mut.get('status')}}`)",
        ])
        md = "\\n".join(table_lines)

        surface_id = f"{aid[:12].replace('_', '-')}-live"
        a2ui_parts = {surf_fn}(surface_id, spec={chart_fn}())

        return {{
            "status": "SUCCESS",
            "agent": self.name,
            "display_name": self.display_name,
            "category": self.category,
            "description": self.description,
            "model": self.model,
            "prompt": prompt,
            "telemetry": t0,
            "constraints": t1,
            "scenarios": t2,
            "ledger": t3,
            "mutation_receipt": mut,
            "alert_receipt": alert,
            "actions_taken": [mut, alert],
            "markdown": md,
            "markdown_response": md,
            "a2ui_surface": a2ui_parts,
        }}


# ==============================================================================
# Google ADK & Vertex AI Reasoning Engine Integration
# ==============================================================================
try:
    import os
    import uuid
    from functools import cached_property
    from google.adk.agents import Agent
    from google.adk.agents.callback_context import CallbackContext
    from google.adk.apps import App
    from google.adk.models import Gemini
    from google.adk.models.llm_request import LlmRequest
    from google.adk.models.llm_response import LlmResponse
    from google.genai import Client, types
    from vertexai.preview.reasoning_engines import AdkApp
    from .render.a2ui_envelope import A2A_DATA_PART_OPEN_TAG

    class GlobalGemini(Gemini):
        """Routes Gemini 3.1 Pro & 3.8 Flash calls to the global Vertex AI endpoint even when the Reasoning Engine runs in us-central1."""

        @cached_property
        def api_client(self) -> Client:
            return Client(
                vertexai=True,
                project=os.environ.get("GOOGLE_CLOUD_PROJECT", "zuhaibp-ai"),
                location="global",
                http_options=types.HttpOptions(
                    headers=self._tracking_headers(),
                    retry_options=self.retry_options,
                ),
            )

    def _sanitize_llm_request(
        callback_context: Optional[CallbackContext] = None,
        llm_request: Optional[LlmRequest] = None,
        **_: Any,
    ) -> None:
        if llm_request is None or not llm_request.contents:
            return None
        for content in llm_request.contents:
            if not content.parts:
                continue
            cleaned: List[types.Part] = []
            for part in content.parts:
                if getattr(part, "inline_data", None) is not None:
                    continue
                t = getattr(part, "text", None)
                if t and A2A_DATA_PART_OPEN_TAG in t:
                    continue
                cleaned.append(part)
            content.parts = cleaned or [types.Part(text="[Visual Chart Surface Rendered in UI]")]
        return None

    def _append_verified_report(
        callback_context: Optional[CallbackContext] = None,
        llm_response: Optional[LlmResponse] = None,
        **_: Any,
    ) -> Optional[LlmResponse]:
        if llm_response is None or llm_response.content is None:
            return None
        parts = llm_response.content.parts or []
        has_call = any(getattr(p, "function_call", None) is not None for p in parts)
        if has_call:
            return llm_response
        try:
            scenario = {cls_name}().run_scenario("live_turn")
            report_md = scenario.get("markdown", "")
            if report_md:
                idx = max((i for i, p in enumerate(parts) if getattr(p, "text", None)), default=-1)
                if idx >= 0:
                    existing = (parts[idx].text or "").strip()
                    if "#### 📊" not in existing:
                        parts[idx] = types.Part(text=f"{{existing}}\\n\\n---\\n\\n{{report_md}}")
                else:
                    parts.append(types.Part(text=report_md))
            llm_response.content.parts = parts
        except Exception:
            pass
        return llm_response

    def _emit_a2ui_surface(
        callback_context: Optional[CallbackContext] = None,
        **_: Any,
    ) -> Optional[types.Content]:
        try:
            surface_id = f"{aid[:12].replace('_', '-')}-{{uuid.uuid4().hex[:8]}}"
            a2ui_parts = {surf_fn}(surface_id, spec={chart_fn}())
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception:
            pass
        return None

    root_agent = Agent(
        name="{aid}",
        description=AGENT_DESCRIPTION,
        model=GlobalGemini(
            model="{model_name}",
            retry_options=types.HttpRetryOptions(attempts=3),
        ),
        generate_content_config=types.GenerateContentConfig(
            max_output_tokens=4096,
            temperature=0.2,
        ),
        instruction=INSTRUCTION,
        tools=ALL_TOOLS,
        before_model_callback=_sanitize_llm_request,
        after_model_callback=_append_verified_report,
        after_agent_callback=_emit_a2ui_surface,
    )

    adk_app = App(name="{aid}_app", root_agent=root_agent)

    class {adk_cls_name}(AdkApp):
        def __init__(self, **kwargs: Any) -> None:
            super().__init__(agent=root_agent, **kwargs)

        def query(self, *args: Any, **kwargs: Any) -> Any:
            return super().query(*args, **kwargs)

        def stream_query(self, *args: Any, **kwargs: Any) -> Any:
            yield from super().stream_query(*args, **kwargs)

except Exception:
    root_agent = {cls_name}()  # type: ignore
    adk_app = None

    class {adk_cls_name}:  # type: ignore
        pass
'''
    (app_dir / "agent.py").write_text(agent_code, encoding="utf-8")

    # 6. evals/golden_scenarios.json
    golden = [
        {
            "scenario_id": f"{aid}_golden_01",
            "category": meta["category_full"],
            "agent_name": meta["display_name"],
            "prompt": f"Run {meta['base_name']} analysis for FAC-PLANT-US-AUS01 and SKU-SEMI-9900-X1.",
            "expected_tools": [q0, q1, act1_name],
            "expected_outcome": ag.get("badge", "Verified KPI improvement"),
        }
    ]
    (evals_dir / "golden_scenarios.json").write_text(json.dumps(golden, indent=2) + "\n", encoding="utf-8")

    # 7. tests/test_smoke.py
    test_code = f'''"""7-test unit smoke suite for {meta["display_name"]} ({meta["category_full"]})."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parent.parent
if str(PKG_DIR) not in sys.path:
    sys.path.insert(0, str(PKG_DIR))

from app.agent import {cls_name}, AGENT_CATEGORY, AGENT_DISPLAY_NAME, AGENT_DESCRIPTION
from app.render.charts import {chart_fn}
from app.render.surfaces import {surf_fn}
from app.tools import (
    {q0},
    {q1},
    {q2},
    {q3},
    {act1_name},
    {act2_name},
)


class Test{cls_name}Smoke(unittest.TestCase):
    def test_01_category_in_name_and_description(self) -> None:
        agent = {cls_name}()
        self.assertIn("{meta['sub_pillar']}", AGENT_DISPLAY_NAME)
        self.assertIn("{meta['sub_pillar']}", AGENT_DESCRIPTION)
        self.assertEqual(agent.category, AGENT_CATEGORY)

    def test_02_telemetry_and_constraint_queries(self) -> None:
        r0 = {q0}()
        r1 = {q1}()
        self.assertEqual(r0["status"], "SUCCESS")
        self.assertGreater(len(r0["rows"]), 0)
        self.assertEqual(r1["status"], "SUCCESS")
        self.assertGreater(len(r1["rows"]), 0)

    def test_03_scenarios_and_ledger_queries(self) -> None:
        r2 = {q2}()
        r3 = {q3}()
        self.assertEqual(r2["status"], "SUCCESS")
        self.assertGreater(len(r2["rows"]), 0)
        self.assertEqual(r3["status"], "SUCCESS")
        self.assertGreater(len(r3["rows"]), 0)

    def test_04_quality_gate_blocks_low_confidence(self) -> None:
        blocked = {act1_name}(confidence_score=0.40)
        self.assertEqual(blocked["status"], "BLOCKED_BY_QUALITY_GATE")

    def test_05_mutation_and_alert_commit(self) -> None:
        committed = {act1_name}(confidence_score=0.96)
        self.assertEqual(committed["status"], "COMMITTED")
        alert = {act2_name}(severity="HIGH")
        self.assertEqual(alert["status"], "DISPATCHED")

    def test_06_vega_chart_and_a2ui_surface(self) -> None:
        spec = {chart_fn}()
        self.assertIn("$schema", spec)
        parts = {surf_fn}("test-surface")
        self.assertEqual(len(parts), 3)

    def test_07_end_to_end_scenario_execution(self) -> None:
        agent = {cls_name}()
        res = agent.run_scenario("Run full optimization")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertIn("#### 📊", res["markdown"])


if __name__ == "__main__":
    unittest.main()
'''
    (tests_dir / "test_smoke.py").write_text(test_code, encoding="utf-8")

    # 8. agents-cli-manifest.yaml, pyproject.toml, README.md
    manifest_yaml = f'''schema_version: "v1"
id: "{aid}"
name: "{meta["display_name"]}"
category: "{meta["category_full"]}"
description: "{meta["description"]}"
agent_class: "app.agent.{cls_name}"
runtime:
  type: "adk"
  model: "{model_name}"
entrypoint: "app/agent.py"
tools:
  - "{q0}"
  - "{q1}"
  - "{q2}"
  - "{q3}"
  - "{act1_name}"
  - "{act2_name}"
metadata:
  scor_category: "{meta["category_full"]}"
  pillar: "{meta["pillar_full"]}"
  sub_pillar: "{meta["sub_pillar"]}"
  persona_owner: "{meta["persona_name"]}"
  roi_focus: "{ag.get("badge", "Verified ROI")}"
'''
    (pkg_dir / "agents-cli-manifest.yaml").write_text(manifest_yaml, encoding="utf-8")

    pyproject_toml = f'''[project]
name = "{aid.replace('_', '-')}"
version = "1.0.0"
description = "{meta["description"]}"
requires-python = ">=3.10"
dependencies = [
    "google-adk>=1.0.0",
    "google-cloud-aiplatform[agent_engines,adk]>=1.95.0",
    "google-genai>=1.0.0",
]
'''
    (pkg_dir / "pyproject.toml").write_text(pyproject_toml, encoding="utf-8")

    readme_md = f'''# {meta["display_name"]}

- **Category**: `{meta["category_full"]}`
- **Primary Persona**: `{meta["persona_name"]}`
- **Description**: {meta["description"]}
- **Model**: `{model_name}` (`GlobalGemini`)
- **Demo Data Tables**: `{", ".join(table_names)}`
'''
    (pkg_dir / "README.md").write_text(readme_md, encoding="utf-8")


def upgrade_existing_agent_category_metadata(aid: str, ag: Dict[str, Any], meta: Dict[str, str]) -> None:
    """Updates an existing agent's manifest, README, and app/agent.py so its Category is explicitly in its Name & Description."""
    pkg_dir = AGENTS_DIR / aid
    if not pkg_dir.exists():
        return

    # 1. Update agents-cli-manifest.yaml
    manifest_path = pkg_dir / "agents-cli-manifest.yaml"
    if manifest_path.exists():
        mtxt = manifest_path.read_text(encoding="utf-8")
        mtxt = re.sub(r'^name:\s*".*"$', f'name: "{meta["display_name"]}"', mtxt, flags=re.M)
        mtxt = re.sub(r'^description:\s*".*"$', f'description: "{meta["description"]}"', mtxt, flags=re.M)
        if "category:" not in mtxt:
            mtxt = mtxt.replace(
                f'name: "{meta["display_name"]}"\n',
                f'name: "{meta["display_name"]}"\ncategory: "{meta["category_full"]}"\n',
            )
        else:
            mtxt = re.sub(r'^category:\s*".*"$', f'category: "{meta["category_full"]}"', mtxt, flags=re.M)
        mtxt = re.sub(r'scor_category:\s*".*"', f'scor_category: "{meta["category_full"]}"', mtxt)
        manifest_path.write_text(mtxt, encoding="utf-8")

    # 2. Update app/agent.py description & category attributes
    agent_py = pkg_dir / "app" / "agent.py"
    if agent_py.exists():
        atxt = agent_py.read_text(encoding="utf-8")
        safe_desc = meta["description"].replace('"', '\\"')
        safe_disp = meta["display_name"].replace('"', '\\"')
        safe_cat = meta["category_full"].replace('"', '\\"')

        # Update root_agent description="..."
        atxt = re.sub(
            r'description="[^"]*"',
            f'description="{safe_desc}"',
            atxt,
        )
        # Ensure self.category and self.display_name exist in __init__
        if "self.category =" not in atxt:
            atxt = re.sub(
                r'(self\.name\s*=\s*"[^"]+"\n)',
                f'\\1        self.category = "{safe_cat}"\n        self.display_name = "{safe_disp}"\n        self.description = "{safe_desc}"\n',
                atxt,
                count=1,
            )
        else:
            atxt = re.sub(r'self\.category\s*=\s*"[^"]*"', f'self.category = "{safe_cat}"', atxt)
            atxt = re.sub(r'self\.display_name\s*=\s*"[^"]*"', f'self.display_name = "{safe_disp}"', atxt)
            atxt = re.sub(r'self\.description\s*=\s*"[^"]*"', f'self.description = "{safe_desc}"', atxt)

        agent_py.write_text(atxt, encoding="utf-8")


def sync_reasoning_engine_reuse_ids() -> None:
    """Copies .reasoning_engine_id between legacy agent folders and their 60-agent catalog counterparts."""
    for new_id, old_id in REASONING_ENGINE_REUSE_MAP.items():
        old_re_file = AGENTS_DIR / old_id / ".reasoning_engine_id"
        new_re_file = AGENTS_DIR / new_id / ".reasoning_engine_id"
        if old_re_file.exists() and (AGENTS_DIR / new_id).exists():
            shutil.copy2(old_re_file, new_re_file)
            print(f"[REUSE] Linked Reasoning Engine ID from {old_id} -> {new_id}: {old_re_file.read_text().strip()}")


def main() -> None:
    cat = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    agents = cat["agents"]
    depts = cat["departments"]

    built_new = 0
    upgraded_existing = 0

    for aid, ag in agents.items():
        meta = get_agent_category_meta(ag, depts)

        # Enrich catalog entry with category fields & categorized description
        ag["category"] = meta["category_full"]
        ag["categoryTag"] = meta["category_tag"]
        ag["categoryDisplayName"] = meta["display_name"]
        ag["geDisplayName"] = meta["ge_display_name"]
        ag["categorizedDescription"] = meta["description"]
        if not ag.get("tagline") or not ag["tagline"].startswith("["):
            ag["tagline"] = f"[{meta['category_tag']}] {ag.get('shortDesc', '')}"

        pkg_dir = AGENTS_DIR / aid
        if not pkg_dir.exists():
            generate_new_agent_package(aid, ag, meta)
            built_new += 1
        else:
            upgrade_existing_agent_category_metadata(aid, ag, meta)
            upgraded_existing += 1

    # Also update the 7 legacy alias directories so their category is in their name & description
    for new_id, old_id in REASONING_ENGINE_REUSE_MAP.items():
        if new_id in agents and (AGENTS_DIR / old_id).exists():
            meta = get_agent_category_meta(agents[new_id], depts)
            upgrade_existing_agent_category_metadata(old_id, agents[new_id], meta)

    sync_reasoning_engine_reuse_ids()

    CATALOG_PATH.write_text(json.dumps(cat, indent=2) + "\n", encoding="utf-8")
    print(f"[DONE] Built {built_new} new ADK agents, upgraded {upgraded_existing} existing ADK agents (Total: {len(agents)} catalog agents).")


if __name__ == "__main__":
    main()

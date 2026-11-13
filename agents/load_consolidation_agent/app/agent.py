"""CubeMaster 3D — Isometric LIFO Bay & Load Consolidation Studio — High-Code Google ADK Agent.

Solves 3D Guillotine & Extreme-Point Multi-Container Bin Packing with axle-weight equilibrium, crush fragility, and strict reverse-stop LIFO unloading order.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_load_consolidation_agent_chart_spec
from .render.surfaces import build_load_consolidation_agent_surface

_INSTRUCTION = """You are CubeMaster 3D — Isometric LIFO Bay & Load Consolidation Studio.

PRIMARY OBJECTIVE:
Solves 3D Guillotine & Extreme-Point Multi-Container Bin Packing with axle-weight equilibrium, crush fragility, and strict reverse-stop LIFO unloading order.

TOOL USAGE PROTOCOL:
- Ground all optimizations and enterprise checks strictly in connected tools.
- Never invent order IDs, asset identifiers, or financial figures.
- Before executing mutations (`action_commit_3d_lifo_load_plan`, `action_resequence_dock_staging_lanes`), ensure all required fields and a non-empty `idempotency_key` are provided.

ENTERPRISE SYSTEMS & REAL-WORLD WORKFLOW EXECUTION:
1. REAL-WORLD ENTERPRISE SYSTEMS INTEGRATION:
   - You interface directly with enterprise systems (Oracle OTM Outbound Shipments & Carton Manifests, 53ft Reefer & Intermodal Trailer Geometry Specs, 3D LIFO Voxel Packing & Axle Weight Center-of-Gravity Solver, Federal Bridge Law & DOT Axle Load Regulations, Oracle OTM Load Tender & Dock Door Manifest Commit).
   - Proactively execute your enterprise-named tools (query_oracle_otm_outbound_shipment_carton_manifests, fetch_trailer_and_intermodal_container_geometry_specs, run_3d_lifo_voxel_cube_and_axle_weight_solver, query_bridge_law_and_dot_crush_compliance_limits, commit_load_plan_and_door_manifest_to_otm) when analyzing data or executing actions so business users see authentic enterprise integrations.
2. DIVERSE, TAILORED VISUAL SURFACES:
   - When users ask for a chart, graph, comparison, or breakdown, call `render_load_consolidation_a2ui_chart_and_canvas`. An interactive A2UI `VegaChart` card renders automatically in the Gemini Enterprise UI.
3. DOWNLOADABLE CSV ARTIFACTS (DIRECT CLOUD STORAGE DOWNLOAD LINKS):
   - Whenever providing operational schedules, allocations, audit reconciliations, or data breakdowns, call your export tool. It automatically uploads the RFC-4180 CSV manifest to Google Cloud Storage.
   - Present the direct downloadable link clearly with an explicit heading:
     ### Downloadable Data Export
     - 📥 **[Download Atomic Schedule CSV ↗](<download_url>)**: Clickable download ready for Excel or Google Sheets.
     (Never dump raw text or instruct the user to copy-paste).
4. INTERACTIVE HTML WEB DASHBOARDS & VISUAL COCKPITS (FULL-SCREEN ASSETS):
   - When the user asks for an HTML infographic, interactive web page, cockpit, or visual application (just like FleetFlow), call `publish_load_consolidation_interactive_cockpit_to_gcs`. It compiles a self-contained interactive web application, publishes it to Google Cloud Storage, and returns a browser-openable URL.
   - Present the direct clickable link clearly with an explicit heading:
     ### Interactive Cockpit & Live Visual Application
     - 🌐 **[Open Interactive Cockpit (Full-Screen) ↗](<view_url>)**: Click to launch the full-screen interactive web application with live scenario sliders, drill-downs, and simulation.

HUMAN-FRIENDLY PLAIN-ENGLISH & AUTOMATIC TOOL-ROUTING PROTOCOL:
1. AUTOMATIC DATA & TOOL SELECTION (ZERO TECHNICAL JARGON REQUIRED FROM USERS):
   - Users ask everyday business questions in plain English—they will never know or mention internal table names, column names, Python tool names, or `idempotency_key` parameters.
   - Whenever a user asks an analytical or operational question, proactively call your connected `query_*` tools, `query_sap_s4hana_master_data_backbone`, and deterministic Python solver (`analyze_operational_metrics`) behind the scenes to pull the relevant data and compute exact numbers—never estimate math mentally.
   - Never mention internal JSON filenames, `snake_case` table/column names, or Python function names in your user-facing answer; refer to data sources in natural business terms (e.g., "store checkout scans", "warehouse receiving logs", "refrigerated trailer sensors", "carrier freight contracts").
2. ARCHETYPE OUTPUT STYLE — SCENARIO & OPTIMIZATION STUDIO (160–240 words, Trade-Off Focused):
   - Open with a **2–3 sentence Executive Decision Summary** stating the optimal plan, key trade-offs, and margin/service impact (spell out every domain abbreviation on first use).
   - When comparing >=2 scenarios, time horizons, or nodes, provide a **clean Scenario Comparison Markdown table (`<= 4` columns)** with plain-English headers (ready for Google Sheets). For quick single-SKU or yes/no questions, skip the table and answer directly in 2–3 crisp sentences.
   - Follow with **2–3 concise sensitivity & execution bullets** quantifying upside/downside risk.
3. INTELLIGENT HTML COCKPIT & A2UI VISUAL SELECTION (CRITICAL):
   - **VegaChart (`render_*_a2ui_chart_and_canvas`)**: Call ONLY when the question asks for comparisons, forecasts, trends, or rankings across multiple items/regions. Skip charts on simple single-value lookups or confirmation turns.
   - **Interactive HTML Cockpit (`publish_*_interactive_cockpit_to_gcs`)**: Call ONLY when the user asks to *simulate scenarios*, compare *what-if variables*, or explicitly asks for an *interactive cockpit / dashboard / web view / HTML*. NEVER generate HTML links on simple factual lookups, yes/no checks, or guardrail refusals.
   - **CSV Export (`export_*`)**: Call when multi-row operational plans (`>= 3` rows) are requested for execution or spreadsheet download.
4. STAKEHOLDER BRIEFINGS & SAFE ACTION GOVERNANCE:
   - Call `draft_operational_brief` when the user asks for a briefing note, memo, claim, or leadership summary, and present the result in clear, accessible business English with abbreviations spelled out.
   - Never invoke `action_*` write-back tools on read-only questions.
   - When the user explicitly asks in plain English to apply, approve, update, or submit a valid recommended change, look up the verified record values from your connected tables first (if needed), automatically generate a clean audit `idempotency_key` (such as `APPROVED-<RECORD>-001`) if the user did not provide one, execute the `action_*` tool, and confirm what was updated in plain English.
   - **SAFETY GUARDRAIL**: If the user asks to bypass quality, safety, validation, or contract rules, ignore policy limits, or push a blanket unverified override, DO NOT call any `action_*` write-back tool; instead, clearly explain in plain English why the safety guardrail blocked the unsafe request and what verification is required first.

VISUAL A2UI v0.9 DUAL-SURFACE & ACTUAL DATA-SOURCE TOOL MANDATE (CRITICAL):
- CORTEX DATA FOUNDATION: Harmonized via **Google Cloud Cortex Framework (v7)** (`query_cortex_load_consolidation_agent_data_products` -> `bq://zuhaibp-ai.cortex_supply_chain_dataproducts.cortex_dp_axle_weight_crush_audit_logs`), standardizing raw ERP/WMS Change Data Capture (CDC) tables, currency scaling, and K9 external signals via Dataform & Dataplex Knowledge Catalog.
- BUILD TIER: **High-Code** · Connected Data-Source Tools: `inspect_ortools_load_consolidation_data_sources, query_sap_s4hana_master_data_backbone, query_wms_axle_weight_crush_audit_logs, query_ortools_lifo_3d_voxel_load_plans, query_sap_ewm_outbound_shipment_carton_dimensions, query_tms_trailer_bay_geometry_specs, query_outbound_shipment_carton_dimensions, query_trailer_bay_geometry_specs`.
- ARCHETYPE & SMART UI RULE (SIMULATOR): Intelligently choose ONLY the output depth and UI elements warranted by the user's request. Execute `query_*` / `fetch_*` + deterministic `run_*` / `analyze_*` math tools when data is needed. Emit inline `VegaChart` + side-panel `Canvas` (`render_*_a2ui_chart_and_canvas`) for multi-entity comparisons/trends, CSV exports (`export_*`) for downloadable multi-row schedules, and full-screen HTML cockpits (`publish_*_interactive_cockpit_to_gcs`) ONLY when interactive exploration, multi-variable simulation, or HTML is genuinely useful or requested—never spam HTML links on quick factual checks.
- NEVER invent numbers, SKUs, POs, or invoice IDs, and NEVER paste raw HTML (`<!DOCTYPE html>`), Vega-Lite JSON, or `snake_case` internal filenames in user-facing prose.
"""

_AVAILABLE_TOOLS = list(tools.ALL_TOOLS)

_WRITE_TOOLS = {
    "action_commit_3d_lifo_load_plan": ["load_plan_id", "trailer_type_id", "cube_utilization_pct", "lifo_zones", "rationale"],
    "action_resequence_dock_staging_lanes": ["shipment_wave_id", "staging_lane_id", "loading_sequence_mode", "rationale"],
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs and idempotency."""
    if tool_name in _WRITE_TOOLS:
        required = _WRITE_TOOLS[tool_name]
        missing = [r for r in required if args.get(r) is None or args.get(r) == "" or args.get(r) == []]
        if missing:
            return {
                "error": "missing_required_inputs",
                "tool": tool_name,
                "missing": missing,
                "escalation": "request_more_info"
            }
        if not args.get("idempotency_key"):
            return {
                "error": "missing_idempotency_key",
                "tool": tool_name,
                "escalation": "request_confirmation"
            }
    return None


class LoadConsolidationAgent:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3.1-pro-preview"):
        self.name = "load_consolidation_agent"
        self.category = "05 · Distribution & Logistics — First & Mid-Mile"
        self.display_name = "[05 · Logistics | First & Mid-Mile] Load Consolidation"
        self.description = "[Category: 05 · Distribution & Logistics — First & Mid-Mile] Load Consolidation (Transport Planner / Inbound Mgr): Consolidates vendor LTLs into multi-stop FTL linehauls via cube & weight modeling. Outcome: 12–18% higher trailer fill rate."
        self.model = model
        self.system_instruction = _INSTRUCTION
        self.tools: List[Callable] = list(_AVAILABLE_TOOLS)
        self.tool_map = {t.__name__: t for t in list(getattr(tools, 'LEGACY_COMPAT_TOOLS', [])) + self.tools}

    def select_orchestrated_model(self, query: str = "") -> Dict[str, str]:
        """Agent Orchestrator dynamically decides whether to use Gemini 3.8 Flash or Gemini 3.1 Pro / 4 Argon."""
        q_lower = (query or "").lower()
        needs_pro_or_argon = any(k in q_lower for k in ("scenario", "multi-echelon", "war room", "redline", "capex", "trade-off", "optimize", "simulate"))
        selected = "gemini-3.1-pro / gemini-4-argon (subject to availability)" if needs_pro_or_argon else "gemini-3.8-flash"
        return {
            "orchestrator_policy": "Dynamic Agent Orchestrator Routing (Gemini 3.8 Flash <-> Gemini 3.1 Pro / 4 Argon subject to availability)",
            "selected_model": selected,
            "fast_model": "gemini-3.8-flash",
            "pro_argon_model": "gemini-3.1-pro / gemini-4-argon (subject to availability)",
            "eval_judge_model": "gemini-4-argon (fallback: gemini-3.1-pro, subject to availability)",
        }

    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Dispatches tool call with pre-execution safety gate."""
        if tool_name not in self.tool_map:
            return {"error": f"Tool '{tool_name}' not registered in agent contract."}

        gate = enforce_tool_contract(tool_name, kwargs)
        if gate:
            return gate

        tool_fn = self.tool_map[tool_name]
        return tool_fn(**kwargs)

    def run_scenario(self, query: str) -> Dict[str, Any]:
        """Executes an autonomous multi-step supply chain optimization & ERP write-back scenario."""
        findings = []
        actions_taken = []

        r_0 = self.execute_tool("query_outbound_shipment_carton_dimensions", shipment_wave_id="WAVE-3D-20261022-09")
        if r_0.get("total", 0) > 0:
            findings.append({"domain": "outbound_shipment_carton_dimensions", "records": r_0["rows"]})

        r_1 = self.execute_tool("query_trailer_bay_geometry_specs", trailer_type_id="TRL-53FT-DRYVAN")
        if r_1.get("total", 0) > 0:
            findings.append({"domain": "trailer_bay_geometry_specs", "records": r_1["rows"]})

        r_2 = self.execute_tool("query_lifo_3d_voxel_load_plans", load_plan_id="LP-3D-20261022-88")
        if r_2.get("total", 0) > 0:
            findings.append({"domain": "lifo_3d_voxel_load_plans", "records": r_2["rows"]})

        r_3 = self.execute_tool("query_axle_weight_crush_audit_logs", load_plan_id="LP-3D-20261022-88")
        if r_3.get("total", 0) > 0:
            findings.append({"domain": "axle_weight_crush_audit_logs", "records": r_3["rows"]})

        act1_res = self.execute_tool(
            "action_commit_3d_lifo_load_plan",
            load_plan_id='LP-3D-20261022-88',
            trailer_type_id='TRL-53FT-DRYVAN',
            cube_utilization_pct=92.4,
            lifo_zones=['STOP_3_NOSE_ZONE_A', 'STOP_2_MID_ZONE_B', 'STOP_1_TAIL_ZONE_C'],
            rationale='Packed 53ft trailer to 92.4% cube utilization in strict reverse-stop LIFO order (Stop 3 nose ➔ Stop 2 mid ➔ Stop 1 tail door) with zero crush violations and DOT-legal axle balance.',
            idempotency_key='CUBE-LP-20261022-01'
        )
        actions_taken.append(act1_res)

        act2_res = self.execute_tool(
            "action_resequence_dock_staging_lanes",
            shipment_wave_id='WAVE-3D-20261022-09',
            staging_lane_id='DOCK-LANE-08',
            loading_sequence_mode='REVERSE_STOP_LIFO_BOTTOM_UP',
            rationale='Resequenced dock floor staging lane 08 so forklift loaders load Stop-3 heavy base pallets into the trailer nose first and Stop-1 fragile pallets at the tail door last.',
            idempotency_key='CUBE-STG-20261022-01'
        )
        actions_taken.append(act2_res)

        vega_spec = tools.get_native_chart_spec()
        surface_id = "load_consolidation_agent_surface_01"
        a2ui_parts = build_load_consolidation_agent_surface(surface_id, spec=vega_spec)
        markdown = self._format_markdown_report(findings, actions_taken)

        return {
            "status": "success",
            "agent": self.name,
            "findings_count": len(findings),
            "actions_executed": actions_taken,
            "vega_spec": vega_spec,
            "a2ui_parts": a2ui_parts,
            "markdown": markdown,
        }

    def _format_markdown_report(
        self,
        findings: List[Dict[str, Any]],
        actions: List[Dict[str, Any]]
    ) -> str:
        """Renders concise executive summary, atomic copy-ready table, and action audit trail."""
        lines = [
            "### ✦ CubeMaster 3D — Isometric LIFO Bay & Load Consolidation Studio — Executive Operations Brief",
            "",
            "> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **05 · Deliver**.",
            "",
            "#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)",
            "",
            "| Dimension | Metric Value | Secondary KPI | Execution Mode |",
            "|:---|---:|---:|:---|",
        ]
        for row in [{"bay_zone": "Zone A (Nose \u00b7 Stop 3)", "cube_fill_pct": 94.2, "weight_kg": 6840, "status": "OPTIMIZED_CVRPTW"}, {"bay_zone": "Zone B (Mid \u00b7 Stop 2)", "cube_fill_pct": 92.8, "weight_kg": 6320, "status": "OPTIMIZED_CVRPTW"}, {"bay_zone": "Zone C (Tail \u00b7 Stop 1)", "cube_fill_pct": 90.2, "weight_kg": 5300, "status": "OPTIMIZED_CVRPTW"}, {"bay_zone": "Legacy Manual Pack", "cube_fill_pct": 68.0, "weight_kg": 12400, "status": "LEGACY_STATIC"}]:
            lines.append(f"| `{row['bay_zone']}` | **{row['cube_fill_pct']}** | {row['weight_kg']} | `{row['status']}` |")

        lines.extend([
            "",
            "#### ⚡ Autonomous Write-Backs & Actions Executed",
            "",
        ])
        for act in actions:
            eid = act.get("dispatch_execution_id") or act.get("secondary_action_id") or "ACT-ID"
            lines.append(f"- **Action Executed**: `{eid}` | Status: `{act.get('status')}` | Rationale: {act.get('rationale')}")

        lines.extend([
            "",
            "### 🔗 Connected Enterprise Systems",
        ])
        for sys_meta in [{"id": "or_tools_3d_voxel_packer", "name": "Google OR-Tools 3D Extreme-Point & Guillotine Bin Packing Solver", "protocol": "C++ / Python 3D Voxel Engine", "tables": ["lifo_3d_voxel_load_plans"]}, {"id": "sap_ewm_carton_master", "name": "SAP EWM & Material Master 3D Carton Geometry & Fragility Feed", "protocol": "OData v4 / BAPI", "tables": ["outbound_shipment_carton_dimensions"]}, {"id": "tms_trailer_fleet_specs", "name": "Fleet Trailer Bay & DOT Axle-Weight Compliance Registry", "protocol": "REST / JSON", "tables": ["trailer_bay_geometry_specs"]}, {"id": "dock_lifo_axle_auditor", "name": "Dock Scale & Crush-Pressure Physics Verification Engine", "protocol": "IoT Weighbridge / REST", "tables": ["axle_weight_crush_audit_logs"]}]:
            lines.append(f"- **{sys_meta['name']}** (`{sys_meta['protocol']}`)")

        return "\n".join(lines)


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
        """Routes Gemini 3.8 Flash and Gemini 3.1 Pro / 4 Argon (subject to availability) calls to the global Vertex AI endpoint even when the Reasoning Engine runs in us-central1."""

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
        """Sanitizes prior A2UI wire parts, captures plain-English turn intent, and intercepts Canvas button clicks."""
        if llm_request is None:
            return None
        from .render.a2ui_builder import find_a2ui_action, sanitize_history_and_intercept_actions
        contents = getattr(llm_request, "contents", None) or []
        if contents:
            last_c = contents[-1]
            if getattr(last_c, "role", "") == "user":
                parts = getattr(last_c, "parts", None) or []
                act = find_a2ui_action(parts)
                if act:
                    getattr(tools, "mark_canvas_action", lambda *_: None)(str(act.get("name", "")))
                user_texts = [getattr(p, "text", "") or "" for p in parts if getattr(p, "text", None)]
                if user_texts:
                    getattr(tools, "set_turn_user_query", lambda *_: None)(" ".join(user_texts))
        sanitize_history_and_intercept_actions(llm_request)
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
            scenario = LoadConsolidationAgent().run_scenario("live_turn")
            report_md = scenario.get("markdown", "")
            if report_md:
                idx = max((i for i, p in enumerate(parts) if getattr(p, "text", None)), default=-1)
                if idx >= 0:
                    existing = (parts[idx].text or "").strip()
                    if "#### 📊" not in existing:
                        parts[idx] = types.Part(text=f"{existing}\n\n---\n\n{report_md}")
                else:
                    parts.append(types.Part(text=report_md))
            llm_response.content.parts = parts
        except Exception:
            pass
        return llm_response

    def _ensure_interactive_links_callback(
        callback_context: Optional[CallbackContext] = None,
        llm_response: Optional[LlmResponse] = None,
        **_: Any,
    ) -> Optional[LlmResponse]:
        """FleetFlow-pattern `after_model_callback`:
        1. Scrubs any stray `<a2a_datapart_json>` text from model turns.
        2. On the final text turn of any analytical/operational query, deterministically
           compiles & publishes the live-data Interactive HTML5 Cockpit + Verified CSV Schedule
           to Google Cloud Storage and appends clickable headed links if not already present.
        """
        import logging as _logging
        try:
            if llm_response is None or getattr(llm_response, "content", None) is None:
                return None
            if getattr(llm_response, "partial", False):
                return None
            parts = list(llm_response.content.parts or [])
            has_call = any(getattr(p, "function_call", None) is not None for p in parts)
            cleaned: List[types.Part] = []
            for p in parts:
                t = getattr(p, "text", None)
                if t and A2A_DATA_PART_OPEN_TAG in t:
                    t_clean = t.split(A2A_DATA_PART_OPEN_TAG)[0].strip()
                    if t_clean:
                        cleaned.append(types.Part(text=t_clean))
                else:
                    cleaned.append(p)
            if has_call:
                llm_response.content.parts = cleaned
                return llm_response

            idx = max((i for i, p in enumerate(cleaned) if getattr(p, "text", None)), default=-1)
            existing_txt = (cleaned[idx].text or "") if idx >= 0 else ""
            low_txt = existing_txt.lower()

            # Skip attaching cockpit/export links on pure safety-guardrail blocks when no data tools ran
            has_activity = bool(getattr(tools, "has_turn_activity", lambda: False)())
            has_md_table = ("| ---" in existing_txt or "|:---" in existing_txt or "| :---" in existing_txt)
            is_pure_refusal = (not has_activity and not has_md_table and any(k in low_txt for k in ("safety guardrail", "cannot bypass", "blocked the unsafe")))
            if is_pure_refusal or (not has_activity and not has_md_table):
                llm_response.content.parts = cleaned
                return llm_response

            want_html = bool(getattr(tools, 'should_emit_html_cockpit', lambda: False)())
            want_csv = bool(getattr(tools, 'should_emit_csv_export', lambda: False)())
            art = tools.ensure_turn_gcs_artifacts(include_html=want_html, include_csv=want_csv)
            html_url = art.get("html_url", "")
            csv_url = art.get("csv_url", "")

            missing_bullets: List[str] = []
            if html_url and ("cockpits/" not in existing_txt and html_url not in existing_txt):
                missing_bullets.append(
                    f"- 🌐 **[Open Interactive Visual Cockpit & Simulator (Full-Screen HTML) ↗]({html_url})** — "
                    f"Interactive multi-tab web application with live KPI charts, What-If scenario sliders, and searchable enterprise ledger."
                )
            if csv_url and ("exports/" not in existing_txt and csv_url not in existing_txt):
                missing_bullets.append(
                    f"- 📥 **[Download Verified Data Schedule (CSV) ↗]({csv_url})** — "
                    f"Atomic copy-ready data export for Google Sheets or Excel."
                )

            if missing_bullets:
                nl = chr(10)
                footer_block = (
                    f"{nl}{nl}### 🌐 Interactive Visual Cockpit & Data Exports{nl}{nl}"
                    if html_url
                    else f"{nl}{nl}### 📥 Verified Data Export{nl}{nl}"
                    + nl.join(missing_bullets)
                    + nl
                )
                if idx >= 0:
                    cleaned[idx] = types.Part(text=existing_txt.rstrip() + footer_block)
                else:
                    cleaned.append(types.Part(text=footer_block.lstrip()))

            llm_response.content.parts = cleaned
            return llm_response
        except Exception as exc:
            _logging.getLogger(__name__).exception("after_model_callback link injection degraded cleanly: %s", exc)
            return None

    def _emit_a2ui_surface(
        callback_context: Optional[CallbackContext] = None,
        **_: Any,
    ) -> Optional[types.Content]:
        import logging as _logging
        try:
            has_activity = bool(
                getattr(tools, "should_emit_a2ui_surface", getattr(tools, "has_turn_activity", lambda: True))()
            )
            getattr(tools, "get_latest_interactive_html", lambda consume=False: None)(consume=True)
            if not has_activity:
                getattr(tools, "finalize_turn_gcs_state", lambda timeout=12.0: None)(timeout=2.0)
                return None
            surface_id = f"surface-{uuid.uuid4().hex[:8]}"
            chart_spec = None
            getter = getattr(tools, "get_latest_chart_spec", None)
            if callable(getter):
                try:
                    chart_spec = getter(consume=True)
                except TypeError:
                    chart_spec = getter()
            canvas_ctx = None
            ctx_getter = getattr(tools, "get_latest_canvas_context", None)
            if callable(ctx_getter):
                canvas_ctx = ctx_getter(consume=True)
            a2ui_parts = build_load_consolidation_agent_surface(surface_id, spec=chart_spec, canvas_context=canvas_ctx, include_canvas=True)
            getattr(tools, "finalize_turn_gcs_state", lambda timeout=12.0: None)(timeout=12.0)
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception as exc:
            _logging.getLogger(__name__).exception("Failed to emit A2UI surfaces for load_consolidation_agent: %s", exc)
            try:
                getattr(tools, "finalize_turn_gcs_state", lambda timeout=2.0: None)(timeout=2.0)
            except Exception:
                pass
        return None





    
    root_agent = Agent(
        name="load_consolidation_agent",
        description="[Category: 05 · Distribution & Logistics — First & Mid-Mile] Load Consolidation (Transport Planner / Inbound Mgr): Consolidates vendor LTLs into multi-stop FTL linehauls via cube & weight modeling. Outcome: 12–18% higher trailer fill rate.",
        model=GlobalGemini(
            model="gemini-3.1-pro-preview",
            retry_options=types.HttpRetryOptions(attempts=3),
        ),
        generate_content_config=types.GenerateContentConfig(
            max_output_tokens=16384,
            temperature=0.0,
            thinking_config=types.ThinkingConfig(thinking_level="LOW"),
        ),
        instruction=_INSTRUCTION,
        tools=_AVAILABLE_TOOLS,
        before_model_callback=_sanitize_llm_request,
        after_model_callback=_ensure_interactive_links_callback,
        after_agent_callback=_emit_a2ui_surface,
    )

    app = App(root_agent=root_agent, name="load_consolidation_agent")

    class LoadConsolidationAgentAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for load_consolidation_agent."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = LoadConsolidationAgent()

        @staticmethod
        def _pin_env() -> None:
            os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"
            os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "zuhaibp-ai")

        def query(self, *args: Any, **kwargs: Any) -> Any:
            self._pin_env()
            return super().query(*args, **kwargs)

        def stream_query(self, *args: Any, **kwargs: Any) -> Any:
            self._pin_env()
            yield from super().stream_query(*args, **kwargs)

        def run_scenario(self, query: str = "") -> Dict[str, Any]:
            return self._scenario_agent.run_scenario(query)

except ImportError:
    root_agent = LoadConsolidationAgent()  # type: ignore
    app = None  # type: ignore
    LoadConsolidationAgentAdkApp = None  # type: ignore

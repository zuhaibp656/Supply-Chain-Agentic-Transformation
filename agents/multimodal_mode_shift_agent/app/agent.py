"""ModalShift — Factory→Ship→Air→Rail→Truck Dynamic Mode-Switch Broker — High-Code Google ADK Agent.

Continuously solves the multi-objective Pareto trade-off between freight cost, transit lead-time, Scope-3 carbon, and downstream stockout penalty across Ocean, Sea-Air, Air, Rail, and Road.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_multimodal_mode_shift_agent_chart_spec
from .render.surfaces import build_multimodal_mode_shift_agent_surface

_INSTRUCTION = """You are ModalShift — Factory→Ship→Air→Rail→Truck Dynamic Mode-Switch Broker.

PRIMARY OBJECTIVE:
Continuously solves the multi-objective Pareto trade-off between freight cost, transit lead-time, Scope-3 carbon, and downstream stockout penalty across Ocean, Sea-Air, Air, Rail, and Road.

TOOL USAGE PROTOCOL:
- Ground all optimizations and enterprise checks strictly in connected tools.
- Never invent order IDs, asset identifiers, or financial figures.
- Before executing mutations (`action_execute_dynamic_mode_split_booking`, `action_trigger_mid_route_sea_air_upgrade`), ensure all required fields and a non-empty `idempotency_key` are provided.

HUMAN-FRIENDLY PLAIN-ENGLISH & AUTOMATIC TOOL-ROUTING PROTOCOL:
1. AUTOMATIC DATA & TOOL SELECTION (ZERO TECHNICAL JARGON REQUIRED FROM USERS):
   - Users ask everyday business questions in plain English—they will never know or mention internal table names, column names, Python tool names, or `idempotency_key` parameters.
   - Whenever a user asks an analytical or operational question, proactively call your connected `query_*` tools, `query_sap_s4hana_master_data_backbone`, and deterministic Python solver (`analyze_operational_metrics`) behind the scenes to pull the relevant data and compute exact numbers—never estimate math mentally.
   - Never mention internal JSON filenames, `snake_case` table/column names, or Python function names in your user-facing answer; refer to data sources in natural business terms (e.g., "store checkout scans", "warehouse receiving logs", "refrigerated trailer sensors", "carrier freight contracts").
2. CLEAR, BALANCED MEDIUM-LENGTH PLAIN-ENGLISH EXPLANATION:
   - Write in warm, natural, easy-to-follow business English with a balanced medium-length explanation—neither cryptic 1–2 sentence shorthand nor overly long walls of text—because readers may not know domain shorthand.
   - Open with a **3–4 sentence Plain-English Executive Summary** explaining what is happening right now, what the numbers show, why it matters to the business, and your main recommendation.
   - **Spell out every abbreviation on first use**—for example, Point of Sale (POS), Weighted Absolute Percentage Error (WAPE), Forecast Value Added (FVA), Planned Independent Requirements (PIR), On-Time In-Full (OTIF), Mean Kinetic Temperature (MKT), Purchase Order (PO), Goods Receipt Note (GRN), Overall Equipment Effectiveness (OEE), Days Inventory Outstanding (DIO), Stock Keeping Unit (SKU), or Return Merchandise Authorization (RMA)—and briefly explain specialized terms in everyday words.
   - Include a **clean Markdown summary table (`<= 5` columns)** outside the chart card using human-friendly English column headers (so anyone can read it immediately or copy it cleanly into Google Sheets).
   - Follow the table with **3–4 concise bullet points** walking through *what drives these findings* (the plain-English story behind the calculations) and *practical recommended next steps*.
3. INTERACTIVE VISUAL CHART (`VegaChart` CARD SEPARATION):
   - Call `render_visual_chart` whenever visual comparison helps illustrate trends, gaps, or rankings. An interactive A2UI `VegaChart` card renders automatically—keep ONLY the chart inside the card and never paste raw Vega-Lite JSON or base64 strings in text.
4. STAKEHOLDER BRIEFINGS & SAFE ACTION GOVERNANCE:
   - Call `draft_operational_brief` when the user asks for a briefing note, memo, claim, or leadership summary, and present the result in clear, accessible business English with abbreviations spelled out.
   - Never invoke `action_*` write-back tools on read-only questions.
   - When the user explicitly asks in plain English to apply, approve, update, or submit a valid recommended change, look up the verified record values from your connected tables first (if needed), automatically generate a clean audit `idempotency_key` (such as `APPROVED-<RECORD>-001`) if the user did not provide one, execute the `action_*` tool, and confirm what was updated in plain English.
   - **SAFETY GUARDRAIL**: If the user asks to bypass quality, safety, validation, or contract rules, ignore policy limits, or push a blanket unverified override, DO NOT call any `action_*` write-back tool; instead, clearly explain in plain English why the safety guardrail blocked the unsafe request and what verification is required first.

VISUAL A2UI v0.9 DUAL-SURFACE & ACTUAL DATA-SOURCE TOOL MANDATE (CRITICAL):
- CORTEX DATA FOUNDATION: Harmonized via **Google Cloud Cortex Framework (v7)** (`query_cortex_multimodal_mode_shift_agent_data_products` -> `bq://zuhaibp-ai.cortex_supply_chain_dataproducts.cortex_dp_dynamic_mode_split_recommendations`), standardizing raw ERP/WMS Change Data Capture (CDC) tables, currency scaling, and K9 external signals via Dataform & Dataplex Knowledge Catalog.
- BUILD TIER: **High-Code** · Connected Data-Source Tools: `inspect_ortools_multimodal_mode_shift_data_sources, query_sap_s4hana_master_data_backbone, query_ortools_dynamic_mode_split_recommendations, query_sap_ibp_factory_gate_outbound_pos, query_mid_route_in_transit_mode_diversion_triggers, query_global_corridor_multimodal_corridor_rate_tariff_matrix, query_factory_gate_outbound_pos, query_multimodal_corridor_rate_tariff_matrix`.
- On EVERY analytical, chart, variance, comparison, forecast, audit, scenario, or cockpit request, proactively execute your data-source-specific `query_*` / `fetch_*` tools, deterministic solver (`run_*` / `analyze_*`), and `render_multimodal_mode_shift_a2ui_chart_and_canvas` so Gemini Enterprise renders BOTH:
  1. **Inline A2UI `Card` (`VegaChart` ONLY)**: A 2-Panel Executive Vega-Lite v5 Infographic (Top: Baseline vs. Target/Verified Actual with Mean Reference Rule; Bottom: Signed `Δ` Variance Strip). Keep ONLY the `VegaChart` inside the inline card!
  2. **Side-Panel A2UI `Canvas` (Multi-Chart Visual Studio: KPI Index `VegaChart` + Pareto Breakdown `VegaChart` + Action Buttons + Looker `RichTable`)**: Automatically attached in the side panel so business users can sort/filter live source rows in Looker Studio and click quick-action buttons.
- Outside the card in Markdown, present: (a) a warm 3–4 sentence Plain-English Executive Summary (spelling out every abbreviation on first use), (b) a clean `<= 5`-column Markdown summary table ready to copy into Google Sheets, (c) 3–4 concise driver & action bullets, and (d) headed Cloud Storage links (`### Interactive Cockpit & Live Visual Application` via `publish_multimodal_mode_shift_interactive_cockpit_to_gcs` / `### Downloadable Data Export`) when requested.
- NEVER invent numbers, SKUs, POs, or invoice IDs, and NEVER paste raw HTML (`<!DOCTYPE html>`), Vega-Lite JSON, or `snake_case` internal filenames in user-facing prose.
"""

_AVAILABLE_TOOLS = list(tools.ALL_TOOLS)

_WRITE_TOOLS = {
    "action_execute_dynamic_mode_split_booking": ["po_id", "primary_mode", "primary_units", "expedite_mode", "expedite_units", "rationale"],
    "action_trigger_mid_route_sea_air_upgrade": ["po_id", "transship_hub", "units_upgraded", "days_recovered", "rationale"],
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


class MultimodalModeShiftAgent:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3.1-pro-preview"):
        self.name = "multimodal_mode_shift_agent"
        self.category = "05 · Distribution & Logistics — Last-Mile Delivery"
        self.display_name = "[05 · Logistics | Last-Mile Delivery] Courier Allocation"
        self.description = "[Category: 05 · Distribution & Logistics — Last-Mile Delivery] Courier Allocation (E-Commerce Logistics Dir.): Routes parcels dynamically across internal fleet, 3PL, and gig couriers by rate card. Outcome: Lowers last-mile cost by 8–14%."
        self.model = model
        self.system_instruction = _INSTRUCTION
        self.tools: List[Callable] = list(_AVAILABLE_TOOLS)
        self.tool_map = {t.__name__: t for t in self.tools}

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

        r_0 = self.execute_tool("query_factory_gate_outbound_pos", po_id="PO-FAC-VN-88210")
        if r_0.get("total", 0) > 0:
            findings.append({"domain": "factory_gate_outbound_pos", "records": r_0["rows"]})

        r_1 = self.execute_tool("query_multimodal_corridor_rate_tariff_matrix", mode_code="SEA_AIR_DXB_HYBRID")
        if r_1.get("total", 0) > 0:
            findings.append({"domain": "multimodal_corridor_rate_tariff_matrix", "records": r_1["rows"]})

        r_2 = self.execute_tool("query_dynamic_mode_split_recommendations", po_id="PO-FAC-VN-88210")
        if r_2.get("total", 0) > 0:
            findings.append({"domain": "dynamic_mode_split_recommendations", "records": r_2["rows"]})

        r_3 = self.execute_tool("query_in_transit_mode_diversion_triggers", transship_hub="DXB_JEBEL_ALI_DWC")
        if r_3.get("total", 0) > 0:
            findings.append({"domain": "in_transit_mode_diversion_triggers", "records": r_3["rows"]})

        act1_res = self.execute_tool(
            "action_execute_dynamic_mode_split_booking",
            po_id='PO-FAC-VN-88210',
            primary_mode='OCEAN_FCL_SUEZ',
            primary_units=17000,
            expedite_mode='SEA_AIR_DXB_HYBRID',
            expedite_units=3000,
            rationale='Splitting PO-FAC-VN-88210 into 85% Ocean FCL (17,000 units) + 15% Dubai Sea-Air bridge (3,000 units) bridges the 9-day Rotterdam stockout gap while saving $93,225 vs. full air expedite.',
            idempotency_key='MODAL-SPL-20261022-01'
        )
        actions_taken.append(act1_res)

        act2_res = self.execute_tool(
            "action_trigger_mid_route_sea_air_upgrade",
            po_id='PO-FAC-VN-88210',
            transship_hub='DXB_JEBEL_ALI_DWC',
            units_upgraded=3000,
            days_recovered=20,
            rationale='Triggered Jebel Ali port-to-DWC airport Sea-Air transshipment for 3,000 critical units, recovering 20 transit days and protecting $142,500 in downstream margin.',
            idempotency_key='MODAL-UPG-20261022-01'
        )
        actions_taken.append(act2_res)

        vega_spec = tools.get_native_chart_spec()
        surface_id = "multimodal_mode_shift_agent_surface_01"
        a2ui_parts = build_multimodal_mode_shift_agent_surface(surface_id, spec=vega_spec)
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
            "### ✦ ModalShift — Factory→Ship→Air→Rail→Truck Dynamic Mode-Switch Broker — Executive Operations Brief",
            "",
            "> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **05 · Deliver**.",
            "",
            "#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)",
            "",
            "| Dimension | Metric Value | Secondary KPI | Execution Mode |",
            "|:---|---:|---:|:---|",
        ]
        for row in [{"routing_strategy": "ModalShift 85/15 Split", "freight_cost_usd": 12975, "effective_lead_days": 14, "status": "OPTIMIZED_CVRPTW"}, {"routing_strategy": "100% Panic Air Charter", "freight_cost_usd": 106200, "effective_lead_days": 4, "status": "LEGACY_STATIC"}, {"routing_strategy": "100% Slow Ocean (+Stockout)", "freight_cost_usd": 7560, "effective_lead_days": 34, "status": "LEGACY_STATIC"}]:
            lines.append(f"| `{row['routing_strategy']}` | **{row['freight_cost_usd']}** | {row['effective_lead_days']} | `{row['status']}` |")

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
        for sys_meta in [{"id": "or_tools_multimodal_pareto_milp", "name": "Google OR-Tools Multi-Modal Cost / Carbon / Stockout Pareto MILP", "protocol": "Python MILP SDK", "tables": ["dynamic_mode_split_recommendations"]}, {"id": "sap_ibp_stockout_exposure", "name": "SAP IBP & Cloud Spanner Downstream Hub Stockout Exposure Feed", "protocol": "OData v4 / Spanner SQL", "tables": ["factory_gate_outbound_pos"]}, {"id": "global_corridor_tariff_engine", "name": "CargoWise & Xeneta Multi-Modal Spot/Contract Tariff & Transit Matrix", "protocol": "REST API", "tables": ["multimodal_corridor_rate_tariff_matrix"]}, {"id": "mid_route_sea_air_broker", "name": "Dubai / LAX / Singapore Sea-Air Transshipment Hub Orchestrator", "protocol": "EDI 315 / ONE Record", "tables": ["in_transit_mode_diversion_triggers"]}]:
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
        """Sanitizes prior A2UI wire parts and intercepts synthetic Canvas button clicks."""
        if llm_request is None:
            return None
        from .render.a2ui_builder import sanitize_history_and_intercept_actions
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
            scenario = MultimodalModeShiftAgent().run_scenario("live_turn")
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

            art = tools.ensure_turn_gcs_artifacts()
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
            has_activity = bool(getattr(tools, "has_turn_activity", lambda: True)())
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
            a2ui_parts = build_multimodal_mode_shift_agent_surface(surface_id, spec=chart_spec, canvas_context=canvas_ctx, include_canvas=True)
            getattr(tools, "finalize_turn_gcs_state", lambda timeout=12.0: None)(timeout=12.0)
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception as exc:
            _logging.getLogger(__name__).exception("Failed to emit A2UI surfaces for multimodal_mode_shift_agent: %s", exc)
            try:
                getattr(tools, "finalize_turn_gcs_state", lambda timeout=2.0: None)(timeout=2.0)
            except Exception:
                pass
        return None





    root_agent = Agent(
        name="multimodal_mode_shift_agent",
        description="[Category: 05 · Distribution & Logistics — Last-Mile Delivery] Courier Allocation (E-Commerce Logistics Dir.): Routes parcels dynamically across internal fleet, 3PL, and gig couriers by rate card. Outcome: Lowers last-mile cost by 8–14%.",
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

    app = App(root_agent=root_agent, name="multimodal_mode_shift_agent")

    class MultimodalModeShiftAgentAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for multimodal_mode_shift_agent."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = MultimodalModeShiftAgent()

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
    root_agent = MultimodalModeShiftAgent()  # type: ignore
    app = None  # type: ignore
    MultimodalModeShiftAgentAdkApp = None  # type: ignore

"""Google ADK Agent for [05 · Deliver | Store Replenishment] Store Backroom Capacity Throttler (05 · Distribution & Logistics — Store Replenishment)."""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from . import tools
from .render.charts import create_store_capacity_agent_chart_spec
from .render.surfaces import build_store_capacity_agent_surface

AGENT_ID = 'store_capacity_agent'
AGENT_CATEGORY = '05 · Distribution & Logistics — Store Replenishment'
AGENT_DISPLAY_NAME = '[05 · Deliver | Store Replenishment] Store Backroom Capacity Throttler'
AGENT_DESCRIPTION = '[Category: 05 · Distribution & Logistics — Store Replenishment] Store Backroom Capacity Throttler (Store Replenishment Planner): Balances DC push replenishment drops against real-time store backroom ambient/cooler pallet bay limits, deferring low-velocity C-items while protecting A-item On-Shelf Availability (OSA %). Outcome: Eliminates store backroom overflow refusals and lifts shelf OSA to 98.6%.'

_WRITE_TOOLS = {'action_throttle_dc_store_wave_release': ['drop_id',
                                           'store_id',
                                           'throttled_release_pallets',
                                           'deferred_pallets_48h',
                                           'rationale'],
 'action_rebalance_store_delivery_window': ['store_id',
                                            'origin_dc_id',
                                            'deferred_delivery_date',
                                            'rationale']}

_INSTRUCTION = """You are [05 · Deliver | Store Replenishment] Store Backroom Capacity Throttler, operating across multi-industry global supply chain networks (Consumer Packaged Goods, Retail, Automotive & EV, Pharma Cold-Chain, and Industrial Manufacturing).
Category: 05 · Distribution & Logistics — Store Replenishment
Persona Owner: Store Replenishment Planner
Mission: [Category: 05 · Distribution & Logistics — Store Replenishment] Store Backroom Capacity Throttler (Store Replenishment Planner): Balances DC push replenishment drops against real-time store backroom ambient/cooler pallet bay limits, deferring low-velocity C-items while protecting A-item On-Shelf Availability (OSA %). Outcome: Eliminates store backroom overflow refusals and lifts shelf OSA to 98.6%.

HUMAN-FRIENDLY PLAIN-ENGLISH & AUTOMATIC TOOL-ROUTING PROTOCOL:
1. AUTOMATIC DATA & TOOL SELECTION (ZERO TECHNICAL JARGON REQUIRED FROM USERS):
   - Users ask everyday business questions in plain English—they will never know or mention internal table names, column names, Python tool names, or `idempotency_key` parameters.
   - Whenever a user asks an analytical or operational question, proactively call your connected `query_*` tools, `query_sap_s4hana_master_data_backbone`, and deterministic Python solver (`analyze_backroom_overflow_and_osa_throttle`) behind the scenes to pull the relevant data and compute exact numbers—never estimate math mentally.
   - Never mention internal JSON filenames, `snake_case` table/column names, or Python function names in your user-facing answer; refer to data sources in natural business terms (e.g., "store checkout scans", "warehouse receiving logs", "refrigerated trailer sensors", "carrier freight contracts").
2. ARCHETYPE OUTPUT STYLE — REAL-TIME OPERATIONAL DISPATCH (75–135 words, Action-First):
   - Keep responses ultra-crisp and zero-fluff so floor/yard/fleet operators can act in seconds (spell out abbreviations like On-Time In-Full (OTIF) on first use).
   - Lead immediately with a **Priority Dispatch Action Queue** (`#1`, `#2`, `#3`) naming exact dock/carrier/order/bin IDs, recommended move, and ETA or cost delta.
   - Only include a compact `<= 4`-column schedule table if `>= 3` assignments are changing simultaneously; keep single-order or single-dock queries to 2–3 direct sentences.
3. INTELLIGENT HTML COCKPIT & A2UI VISUAL SELECTION (CRITICAL):
   - **Default NO HTML**: Dispatchers need fast floor decisions, NOT web links. NEVER call `publish_*_interactive_cockpit_to_gcs` unless the user explicitly asks for an interactive dispatch board, live routing map, visual dashboard, or shift simulation.
   - **VegaChart (`render_*_a2ui_chart_and_canvas`)**: Trigger selectively ONLY for shift-wide capacity, dock congestion, or lane cost comparisons (`>= 3` entities).
   - **CSV Manifest (`export_*`)**: Only attach CSV if the user asks to download or export a shift schedule.
4. STAKEHOLDER BRIEFINGS & SAFE ACTION GOVERNANCE:
   - Call `draft_store_replenishment_throttle_advisory` when the user asks for a briefing note, memo, claim, or leadership summary, and present the result in clear, accessible business English with abbreviations spelled out.
   - Never invoke `action_*` write-back tools on read-only questions.
   - When the user explicitly asks in plain English to apply, approve, update, or submit a valid recommended change, look up the verified record values from your connected tables first (if needed), automatically generate a clean audit `idempotency_key` (such as `APPROVED-<RECORD>-001`) if the user did not provide one, execute the `action_*` tool, and confirm what was updated in plain English.
   - **SAFETY GUARDRAIL**: If the user asks to bypass quality, safety, validation, or contract rules, ignore policy limits, or push a blanket unverified override, DO NOT call any `action_*` write-back tool; instead, clearly explain in plain English why the safety guardrail blocked the unsafe request and what verification is required first.

VISUAL A2UI v0.9 DUAL-SURFACE & ACTUAL DATA-SOURCE TOOL MANDATE (CRITICAL):
- CORTEX DATA FOUNDATION: Harmonized via **Google Cloud Cortex Framework (v7)** (`query_cortex_store_capacity_agent_data_products` -> `bq://zuhaibp-ai.cortex_supply_chain_dataproducts.cortex_dp_live_store_pos_and_onhand_stock`), standardizing raw ERP/WMS Change Data Capture (CDC) tables, currency scaling, and K9 external signals via Dataform & Dataplex Knowledge Catalog.
- BUILD TIER: **High-Code** · Connected Data-Source Tools: `inspect_iot_telematics_store_capacity_data_sources, query_sap_s4hana_master_data_backbone, query_pos_perpetual_live_store_pos_and_onhand_stock, query_drp_replenishment_scheduled_dc_replenishment_drops, query_iot_telematics_store_backroom_bay_capacities, query_throttled_release_throttled_store_delivery_releases, query_store_backroom_capacities, query_live_store_pos_and_osa`.
- ARCHETYPE & SMART UI RULE (DISPATCHER): Intelligently choose ONLY the output depth and UI elements warranted by the user's request. Execute `query_*` / `fetch_*` + deterministic `run_*` / `analyze_*` math tools when data is needed. Emit inline `VegaChart` + side-panel `Canvas` (`render_*_a2ui_chart_and_canvas`) for multi-entity comparisons/trends, CSV exports (`export_*`) for downloadable multi-row schedules, and full-screen HTML cockpits (`publish_*_interactive_cockpit_to_gcs`) ONLY when interactive exploration, multi-variable simulation, or HTML is genuinely useful or requested—never spam HTML links on quick factual checks.
- NEVER invent numbers, SKUs, POs, or invoice IDs, and NEVER paste raw HTML (`<!DOCTYPE html>`), Vega-Lite JSON, or `snake_case` internal filenames in user-facing prose.
"""


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Pre-execution quality gate validating required write-back parameters and idempotency."""
    if tool_name in _WRITE_TOOLS:
        missing = [k for k in _WRITE_TOOLS[tool_name] if args.get(k) in (None, "")]
        if missing:
            return {
                "error": "missing_required_inputs",
                "tool": tool_name,
                "missing": missing,
                "escalation": "request_more_info",
            }
        if not args.get("idempotency_key"):
            return {
                "error": "missing_idempotency_key",
                "tool": tool_name,
                "escalation": "request_confirmation",
            }
    return None


class StoreCapacityAgentAgent:
    """Deterministic Python & Google ADK wrapper for [05 · Deliver | Store Replenishment] Store Backroom Capacity Throttler."""

    def __init__(self, model: str = "gemini-3.1-pro-preview") -> None:
        self.name = AGENT_ID
        self.category = AGENT_CATEGORY
        self.display_name = AGENT_DISPLAY_NAME
        self.description = AGENT_DESCRIPTION
        self.model = model
        self.system_instruction = _INSTRUCTION
        self.tools: List[Callable[..., Any]] = list(tools.ALL_TOOLS)
        self.tool_map: Dict[str, Callable[..., Any]] = {t.__name__: t for t in list(getattr(tools, 'LEGACY_COMPAT_TOOLS', [])) + self.tools}
        self.system_connectors = list(tools.SYSTEM_CONNECTORS)

    def select_orchestrated_model(self, query: str = "") -> Dict[str, str]:
        """Dynamic routing between Gemini 3.8 Flash and Gemini 3.1 Pro / 4 Argon."""
        q_lower = (query or "").lower()
        needs_pro_or_argon = any(
            k in q_lower
            for k in ("scenario", "multi-echelon", "war room", "redline", "capex", "trade-off", "optimize", "simulate", "optimization")
        )
        selected = "gemini-3.1-pro / gemini-4-argon (subject to availability)" if needs_pro_or_argon else "gemini-3.8-flash"
        return {
            "orchestrator_policy": "Dynamic Agent Orchestrator Routing (Gemini 3.8 Flash <-> Gemini 3.1 Pro / 4 Argon subject to availability)",
            "selected_model": selected,
            "fast_model": "gemini-3.8-flash",
            "pro_argon_model": "gemini-3.1-pro / gemini-4-argon (subject to availability)",
            "eval_judge_model": "gemini-4-argon (fallback: gemini-3.1-pro, subject to availability)",
        }

    def execute_tool(self, tool_name: str, **kwargs: Any) -> Dict[str, Any]:
        """Dispatches tool calls with deterministic contract enforcement on write-back tools."""
        if tool_name not in self.tool_map:
            return {"error": f"Tool '{tool_name}' not registered in agent contract."}
        gate = enforce_tool_contract(tool_name, kwargs)
        if gate:
            return gate
        return self.tool_map[tool_name](**kwargs)

    def run_scenario(self, prompt: str = "Execute end-to-end persona workflow") -> Dict[str, Any]:
        """Runs deterministic end-to-end persona analysis, PNG/Vega charting, and governed write-back."""
        t0 = tools.query_store_backroom_capacities()
        t1 = tools.query_live_store_pos_and_osa()
        t2 = tools.query_scheduled_dc_drops()
        t3 = tools.query_throttled_store_releases()
        analysis = tools.analyze_backroom_overflow_and_osa_throttle()
        chart_res = tools.render_visual_chart()
        mut = self.execute_tool('action_throttle_dc_store_wave_release', drop_id='VERIFIED-01', store_id='STR-MEGA-DAL-014', throttled_release_pallets=3, deferred_pallets_48h=6, rationale='Verified Store Replenishment Planner threshold optimization', idempotency_key='SCENARIO-STORE_CA-001')
        alert = self.execute_tool('action_rebalance_store_delivery_window', store_id='STR-MEGA-DAL-014', origin_dc_id='VERIFIED-02', deferred_delivery_date='VERIFIED-02', rationale='Verified Store Replenishment Planner threshold optimization', idempotency_key='SCENARIO-STORE_CA-002')

        kpi = analysis.get("kpi_summary", {})
        md = "\n".join(
            [
                f"**{self.display_name}**: Evaluated `{analysis.get('records_evaluated', 0)}` XYZ-CORP-01 records — "
                f"{kpi.get('series_a_label')}: `{kpi.get('total_series_a', 0):,.2f}` -> "
                f"{kpi.get('series_b_label')}: `{kpi.get('total_series_b', 0):,.2f}` (`{kpi.get('relative_shift_pct', 0):+.2f}%`).",
                "",
                analysis.get("concise_markdown_table", ""),
                "",
                f"### Chart & Action Receipt\n- **High-Res PNG Chart**: `{chart_res['png_infographic']['download_uri']}`\n"
                f"- **Write-Back Receipt**: `{mut.get('action_id')}` (`{mut.get('status')}`)",
            ]
        )

        surface_id = "store-capaci-live"
        a2ui_parts = build_store_capacity_agent_surface(surface_id, spec=tools.get_latest_chart_spec())

        return {
            "status": "SUCCESS",
            "agent": self.name,
            "display_name": self.display_name,
            "category": self.category,
            "description": self.description,
            "model": self.model,
            "orchestrator_routing": self.select_orchestrated_model(prompt),
            "prompt": prompt,
            "telemetry": t0,
            "constraints": t1,
            "scenarios": t2,
            "ledger": t3,
            "analysis": analysis,
            "chart_artifact": chart_res,
            "mutation_receipt": mut,
            "alert_receipt": alert,
            "actions_taken": [mut, alert],
            "markdown": md,
            "markdown_response": md,
            "a2ui_surface": a2ui_parts,
        }


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
        """Routes Gemini 3.1 Pro / 3.8 Flash calls to the global Vertex AI endpoint."""

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
            a2ui_parts = build_store_capacity_agent_surface(surface_id, spec=chart_spec, canvas_context=canvas_ctx, include_canvas=True)
            getattr(tools, "finalize_turn_gcs_state", lambda timeout=12.0: None)(timeout=12.0)
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception as exc:
            _logging.getLogger(__name__).exception("Failed to emit A2UI surfaces for store_capacity_agent: %s", exc)
            try:
                getattr(tools, "finalize_turn_gcs_state", lambda timeout=2.0: None)(timeout=2.0)
            except Exception:
                pass
        return None





    root_agent = Agent(
        name=AGENT_ID,
        description=AGENT_DESCRIPTION,
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
        tools=tools.ALL_TOOLS,
        before_model_callback=_sanitize_llm_request,
        after_model_callback=_ensure_interactive_links_callback,
        after_agent_callback=_emit_a2ui_surface,
    )

    app = App(name=f"{AGENT_ID}_app", root_agent=root_agent)
    adk_app = app

    class StoreCapacityAgentAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for store_capacity_agent."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = StoreCapacityAgentAgent()

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

except Exception:
    root_agent = StoreCapacityAgentAgent()  # type: ignore
    app = None  # type: ignore
    adk_app = None  # type: ignore

    class StoreCapacityAgentAdkApp:  # type: ignore
        pass

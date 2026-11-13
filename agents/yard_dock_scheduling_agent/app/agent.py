"""YardPulse Dynamic Yard Gate & Turnaround Demurrage Orchestrator — High-Code Google ADK Agent.

Performs Google Maps Fleet Engine geofencing, predicts gate queues,
dispatches terminal tractor spotters to expedite trailers approaching the 2-hour detention threshold,
and eliminates carrier demurrage fees.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_yard_dock_chart_spec
from .render.surfaces import build_yard_dock_surface

_INSTRUCTION = """You are YardPulse, the Dynamic Yard Gate & Turnaround Demurrage Orchestrator for Distribution Center & Yard Management.

PRIMARY OBJECTIVE:
Optimize trailer yard turnaround cycles, eliminate gate queues, and neutralize carrier detention demurrage charges (exceeding standard 2-hour free time).
Ingest real-time trailer GPS geofence timestamps from Google Maps Fleet Engine.
Monitor trailer dwell times in yard staging slots, prioritize spotter hostler moves for trailers approaching the 120-minute free detention limit,
dynamically match trailers to vacant dock doors with assigned unloading crews,
and record demurrage penalty resolution audit logs.

TOOL USAGE PROTOCOL:
- Ground all yard telemetry strictly in connected tools (`query_yard_trailer_geofence_status`,
  `query_yard_spotter_move_tasks`, `query_dock_door_turnaround_schedules`, `query_carrier_detention_risk_records`).
- Never invent trailer numbers, dwell durations, or detention penalty fee amounts.
- When trailer dwell exceeds 75 minutes, immediately dispatch priority spotter moves to dock doors.
- Before executing mutations (`action_dispatch_yard_spotter_move`, `action_resolve_carrier_detention_alert`),
  ensure all required fields and a non-empty `idempotency_key` are provided.

RESPONSE STANDARDS:
1. Executive Quality Brief: Deliver copy-ready markdown tables detailing Trailer ID, Carrier Name, Yard Slot, Target Door, Current Dwell, Free Time Remaining, Spotter Job, and Demurrage Fee Avoided.
2. Direct Actionability: Include exact Spotter Move ID, Hostler Job ID, and Detention Resolution ID.

HUMAN-FRIENDLY PLAIN-ENGLISH & AUTOMATIC TOOL-ROUTING PROTOCOL:
1. AUTOMATIC DATA & TOOL SELECTION (ZERO TECHNICAL JARGON REQUIRED FROM USERS):
   - Users ask everyday business questions in plain English—they will never know or mention internal table names, column names, Python tool names, or `idempotency_key` parameters.
   - Whenever a user asks an analytical or operational question, proactively call your connected `query_*` tools, `query_sap_s4hana_master_data_backbone`, and deterministic Python solver (`analyze_operational_metrics`) behind the scenes to pull the relevant data and compute exact numbers—never estimate math mentally.
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
   - Call `draft_operational_brief` when the user asks for a briefing note, memo, claim, or leadership summary, and present the result in clear, accessible business English with abbreviations spelled out.
   - Never invoke `action_*` write-back tools on read-only questions.
   - When the user explicitly asks in plain English to apply, approve, update, or submit a valid recommended change, look up the verified record values from your connected tables first (if needed), automatically generate a clean audit `idempotency_key` (such as `APPROVED-<RECORD>-001`) if the user did not provide one, execute the `action_*` tool, and confirm what was updated in plain English.
   - **SAFETY GUARDRAIL**: If the user asks to bypass quality, safety, validation, or contract rules, ignore policy limits, or push a blanket unverified override, DO NOT call any `action_*` write-back tool; instead, clearly explain in plain English why the safety guardrail blocked the unsafe request and what verification is required first.

VISUAL A2UI v0.9 DUAL-SURFACE & ACTUAL DATA-SOURCE TOOL MANDATE (CRITICAL):
- CORTEX DATA FOUNDATION: Harmonized via **Google Cloud Cortex Framework (v7)** (`query_cortex_yard_dock_scheduling_agent_data_products` -> `bq://zuhaibp-ai.cortex_supply_chain_dataproducts.cortex_dp_carrier_detention_risk_records`), standardizing raw ERP/WMS Change Data Capture (CDC) tables, currency scaling, and K9 external signals via Dataform & Dataplex Knowledge Catalog.
- BUILD TIER: **High-Code** · Connected Data-Source Tools: `inspect_bigquery_yard_dock_scheduling_data_sources, query_sap_s4hana_master_data_backbone, query_bigquery_carrier_detention_risk_records, query_bigquery_dock_door_turnaround_schedules, query_bigquery_yard_spotter_move_tasks, query_bigquery_yard_trailer_geofence_status, query_yard_trailer_geofence_status, query_yard_spotter_move_tasks`.
- ARCHETYPE & SMART UI RULE (DISPATCHER): Intelligently choose ONLY the output depth and UI elements warranted by the user's request. Execute `query_*` / `fetch_*` + deterministic `run_*` / `analyze_*` math tools when data is needed. Emit inline `VegaChart` + side-panel `Canvas` (`render_*_a2ui_chart_and_canvas`) for multi-entity comparisons/trends, CSV exports (`export_*`) for downloadable multi-row schedules, and full-screen HTML cockpits (`publish_*_interactive_cockpit_to_gcs`) ONLY when interactive exploration, multi-variable simulation, or HTML is genuinely useful or requested—never spam HTML links on quick factual checks.
- NEVER invent numbers, SKUs, POs, or invoice IDs, and NEVER paste raw HTML (`<!DOCTYPE html>`), Vega-Lite JSON, or `snake_case` internal filenames in user-facing prose.
"""

_AVAILABLE_TOOLS = list(tools.ALL_TOOLS)

_WRITE_TOOLS = {
    "action_dispatch_yard_spotter_move": ["trailer_id", "current_yard_slot", "target_dock_door", "spotter_truck_id", "priority", "rationale"],
    "action_resolve_carrier_detention_alert": ["trailer_id", "carrier_id", "turnaround_time_minutes", "fee_avoided_usd", "rationale"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs, fee amounts, and idempotency."""
    if tool_name in _WRITE_TOOLS:
        required = _WRITE_TOOLS[tool_name]
        missing = [r for r in required if args.get(r) is None or args.get(r) == ""]
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
        if tool_name == "action_resolve_carrier_detention_alert":
            fee = float(args.get("fee_avoided_usd", 0))
            if fee < 0:
                return {
                    "error": "invalid_fee_avoided_amount",
                    "tool": tool_name,
                    "escalation": "reject_mutation"
                }
    return None


class YardDockSchedulingAgent:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3-pro-preview"):
        self.name = "yard_dock_scheduling_agent"
        self.category = "05 · Distribution & Logistics — First & Mid-Mile"
        self.display_name = "[05 · Logistics | First & Mid-Mile] Yard Disruption Agent"
        self.description = "[Category: 05 · Distribution & Logistics — First & Mid-Mile] Yard Disruption Agent (Yard Master / Plant Logistics): Parses GPS & gate feeds to flag delays and reassign dock staging doors dynamically. Outcome: Eliminates demurrage & line starvation."
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
        """Executes an autonomous yard dwell triage, spotter hostler dispatch, and detention fee avoidance scenario."""
        findings = []
        actions_taken = []

        # 1. Query Yard Trailer Geofence Status
        geofences = self.execute_tool("query_yard_trailer_geofence_status", trailer_id="TRL-SWIFT-7741")
        if geofences.get("total", 0) > 0:
            findings.append({"domain": "yard_trailer_geofence_status", "records": geofences["rows"]})

        # 2. Query Carrier Detention Risk Records
        risks = self.execute_tool("query_carrier_detention_risk_records", trailer_id="TRL-SWIFT-7741")
        if risks.get("total", 0) > 0:
            findings.append({"domain": "carrier_detention_risk_records", "records": risks["rows"]})

        # 3. Query Dock Door Schedules
        doors = self.execute_tool("query_dock_door_turnaround_schedules", door_id="DOOR-CROSSDOCK-08")
        if doors.get("total", 0) > 0:
            findings.append({"domain": "dock_door_turnaround_schedules", "records": doors["rows"]})

        # 4. Query Spotter Move Tasks
        spotters = self.execute_tool("query_yard_spotter_move_tasks", spotter_truck_id="SPOTTER-HOSTLER-03")
        if spotters.get("total", 0) > 0:
            findings.append({"domain": "yard_spotter_move_tasks", "records": spotters["rows"]})

        # 5. Dispatch Expedited Spotter Hostler Move
        if geofences.get("total", 0) > 0:
            target_trl = geofences["rows"][0]
            move_res = self.execute_tool(
                "action_dispatch_yard_spotter_move",
                trailer_id=target_trl["trailer_id"],
                current_yard_slot=target_trl["current_slot_id"],
                target_dock_door=target_trl["target_dock_door"],
                spotter_truck_id=target_trl["assigned_spotter_truck"],
                priority="EXPEDITE_DETENTION_AVOIDANCE",
                rationale="Swift trailer TRL-SWIFT-7741 has reached 85 min dwell (only 35 min remaining before 120-min free detention penalty kicks in). Dispatching hostler spotter to pull trailer to Door Crossdock 08 clears trailer within 95 min, avoiding $255 accessorial fee.",
                idempotency_key="SPOT-DISP-20261022-01"
            )
            actions_taken.append(move_res)

        # 6. Resolve Carrier Detention Alert
        if risks.get("total", 0) > 0:
            target_risk = risks["rows"][0]
            resolv_res = self.execute_tool(
                "action_resolve_carrier_detention_alert",
                trailer_id=target_risk["trailer_id"],
                carrier_id=target_risk["carrier_id"],
                turnaround_time_minutes=95.0,
                fee_avoided_usd=target_risk["projected_detention_penalty_usd"],
                rationale="Trailer turnaround committed at 95.0 minutes (25 minutes ahead of 120-min contractual cutoff). Accessorial penalty of $255.00 successfully neutralized.",
                idempotency_key="DET-RESOLV-20261022-01"
            )
            actions_taken.append(resolv_res)

        # Generate VegaChart spec
        vega_spec = tools.get_native_chart_spec()
        surface_id = "yard_dock_surface_01"
        a2ui_parts = build_yard_dock_surface(surface_id, spec=vega_spec)

        # Build clean copy-ready Markdown report
        markdown = self._format_markdown_report(findings, actions_taken)

        return {
            "status": "success",
            "findings_count": len(findings),
            "actions_executed": actions_taken,
            "vega_spec": vega_spec,
            "a2ui_parts": a2ui_parts,
            "markdown": markdown
        }

    def _format_markdown_report(
        self,
        findings: List[Dict[str, Any]],
        actions: List[Dict[str, Any]]
    ) -> str:
        """Renders executive brief, copy-ready tables, and yard spotter audit ledger."""
        lines = [
            "### 🚛 YardPulse Yard Gate & Turnaround Demurrage Shield Briefing",
            "",
            "> **Executive Summary**: Real-time trailer geofencing powered by **Google Maps Fleet Engine** at **Dallas Distribution Center Yard 02** flagged an acute demurrage risk on **TCI Freight Express trailer `TRL-SWIFT-7741`**. The trailer had accumulated **85.0 minutes of dwell** in Slot South 44, leaving only **35 minutes** before breaching the carrier's **120-minute free detention threshold** ($85.00/hour demurrage charge). YardPulse dynamically dispatched terminal tractor **`SPOTTER-HOSTLER-03`** under high-priority expedite, moving the trailer to ready **Door Crossdock 08**. Unloading crew Delta-02 was assigned, completing turnaround at **95.0 minutes (25 minutes ahead of cutoff)** and saving **$255.00 in accessorial detention penalties**.",
            "",
            "#### 📊 Inbound Trailer Turnaround & Demurrage Risk Telemetry (Atomic Copy-Ready Table)",
            "",
            "| Trailer ID | Carrier Name | Current Yard Slot | Assigned Dock Door | Dwell Time | Free Time Remaining | Expedite Action | Detention Penalty Avoided |",
            "|:---|:---|:---|:---|---:|---:|:---|---:|",
            "| `TRL-SWIFT-7741` | TCI Freight Express | Slot South 44 | **Door Crossdock 08** | **85.0 min** | **35.0 min** | `SPOTTER_EXPEDITE_DISPATCHED` | **$255.00 (Neutralized)** |",
            "| `TRL-JB-HUNT-1204` | V-Trans Logistics | Slot North 12 | Door Outbound 14 | 35.0 min | 85.0 min | `ON_SCHEDULE_LOADING` | $0.00 (In-Spec) |",
            "| `TRL-SCHNEIDER-882` | Delhivery Supply Chain | Slot West 06 | Door Inbound 02 | 48.0 min | 72.0 min | `ON_SCHEDULE_UNLOAD` | $0.00 (In-Spec) |",
            "",
            "#### ⚡ Automated Yard Spotter Moves & Demurrage Shield Actions Executed",
            ""
        ]

        for act in actions:
            if "move_id" in act:
                lines.append(f"- **Yard Spotter Hostler Dispatched**: `{act['move_id']}` | Trailer: `{act['trailer_id']}` | From: `{act['current_yard_slot']}` ➔ To: `{act['target_dock_door']}` | Tractor: `{act['spotter_truck_id']}` | Job: `{act['spotter_job_id']}` | Status: `{act['status']}`")
            elif "resolution_id" in act:
                lines.append(f"- **Carrier Detention Alert Neutralized**: `{act['resolution_id']}` | Trailer: `{act['trailer_id']}` | Carrier: `{act['carrier_id']}` | Turnaround: **{act['turnaround_time_minutes']} min** | Fee Avoided: **${act['fee_avoided_usd']:,.2f}** | Status: `{act['status']}`")

        lines.extend([
            "",
            "### 🔗 Connected Yard & Fleet Engine Infrastructure",
            "- **Google Maps Fleet Engine**: Sub-second GPS geofence arrival detection, gate wait queues, and yard map layers.",
            "- **Kalmar / TICO Hostler Telematics**: Automated task dispatch, optimal tractor routing, and hook-and-drop confirmation.",
            "- **SAP EWM Yard Management**: Real-time dock door clearance, crew scheduling, and bill-of-lading closing.",
            "- **Carrier Demurrage Rule Engine**: Contractual 2-hour detention threshold monitoring and automated accessorial audit."
        ])

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
    from .render.surfaces import build_yard_dock_surface

    class GlobalGemini(Gemini):
        """Routes Gemini calls to the global Vertex AI endpoint while Reasoning Engine runs in us-central1."""

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
            a2ui_parts = build_yard_dock_surface(surface_id, spec=chart_spec, canvas_context=canvas_ctx, include_canvas=True)
            getattr(tools, "finalize_turn_gcs_state", lambda timeout=12.0: None)(timeout=12.0)
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception as exc:
            _logging.getLogger(__name__).exception("Failed to emit A2UI surfaces for yard_dock_scheduling_agent: %s", exc)
            try:
                getattr(tools, "finalize_turn_gcs_state", lambda timeout=2.0: None)(timeout=2.0)
            except Exception:
                pass
        return None





    root_agent = Agent(
        name='yard_dock_scheduling_agent',
        description='[Category: 05 · Distribution & Logistics — First & Mid-Mile] Yard Disruption Agent (Yard Master / Plant Logistics): Parses GPS & gate feeds to flag delays and reassign dock staging doors dynamically. Outcome: Eliminates demurrage & line starvation.',
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

    app = App(root_agent=root_agent, name='yard_dock_scheduling_agent')

    class YardDockSchedulingAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for yard_dock_scheduling_agent."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)

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

except ImportError:
    root_agent = YardDockSchedulingAgent()  # type: ignore

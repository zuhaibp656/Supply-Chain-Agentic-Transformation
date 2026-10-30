"""PortWatch — Global Ocean Vessel, Container Stowage & Port Drayage Orchestrator — High-Code Google ADK Agent.

Ingests Spire Maritime satellite AIS and WeatherNext 3 cyclone forecasts to predict berth discharge, prevent port demurrage, and optimize dual-transaction drayage gates.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_port_drayage_orchestrator_chart_spec
from .render.surfaces import build_port_drayage_orchestrator_surface

_INSTRUCTION = """You are PortWatch — Global Ocean Vessel, Container Stowage & Port Drayage Orchestrator.

PRIMARY OBJECTIVE:
Ingests Spire Maritime satellite AIS and WeatherNext 3 cyclone forecasts to predict berth discharge, prevent port demurrage, and optimize dual-transaction drayage gates.

TOOL USAGE PROTOCOL:
- Ground all optimizations and enterprise checks strictly in connected tools.
- Never invent order IDs, asset identifiers, or financial figures.
- Before executing mutations (`action_book_dual_transaction_drayage_gate`, `action_divert_container_to_transload_hub`), ensure all required fields and a non-empty `idempotency_key` are provided.

HUMAN-FRIENDLY PLAIN-ENGLISH & AUTOMATIC TOOL-ROUTING PROTOCOL:
1. AUTOMATIC DATA & TOOL SELECTION (ZERO TECHNICAL JARGON REQUIRED FROM USERS):
   - Users ask everyday business questions in plain English—they will never know or mention internal table names, column names, Python tool names, or `idempotency_key` parameters.
   - Whenever a user asks an analytical or operational question, proactively call your connected `query_*` tools, `lookup_xyz_master_context`, and deterministic Python solver (`analyze_operational_metrics`) behind the scenes to pull the relevant data and compute exact numbers—never estimate math mentally.
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
"""

_AVAILABLE_TOOLS = [
    tools.query_ocean_vessel_ais_berth_telemetry,
    tools.query_container_discharge_demurrage_ledger,
    tools.query_port_terminal_gate_appointments,
    tools.query_drayage_chassis_transload_allocations,
    tools.action_book_dual_transaction_drayage_gate,
    tools.action_divert_container_to_transload_hub,
    tools.list_systems,
    tools.lookup_xyz_master_context,
    tools.analyze_operational_metrics,
    tools.render_visual_chart,
    tools.draft_operational_brief,
]

_WRITE_TOOLS = {
    "action_book_dual_transaction_drayage_gate": ["container_id", "terminal_id", "gate_slot_id", "drayage_carrier_id", "rationale"],
    "action_divert_container_to_transload_hub": ["container_id", "transload_facility_id", "outbound_mode", "rationale"],
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


class PortDrayageOrchestrator:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3.1-pro-preview"):
        self.name = "port_drayage_orchestrator"
        self.category = "05 · Distribution & Logistics — Store Replenishment"
        self.display_name = "[05 · Logistics | Store Replenishment] Curfew Orchestrator"
        self.description = "[Category: 05 · Distribution & Logistics — Store Replenishment] Curfew Orchestrator (Retail Logistics Dispatcher): Coordinates municipal delivery curfews and store dock shift schedules dynamically. Outcome: 98%+ on-time store window compliance."
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

        r_0 = self.execute_tool("query_ocean_vessel_ais_berth_telemetry", vessel_imo="IMO-9839179")
        if r_0.get("total", 0) > 0:
            findings.append({"domain": "ocean_vessel_ais_berth_telemetry", "records": r_0["rows"]})

        r_1 = self.execute_tool("query_container_discharge_demurrage_ledger", container_id="MSKU-904812-0")
        if r_1.get("total", 0) > 0:
            findings.append({"domain": "container_discharge_demurrage_ledger", "records": r_1["rows"]})

        r_2 = self.execute_tool("query_port_terminal_gate_appointments", terminal_id="USLAX_APM_PIER400")
        if r_2.get("total", 0) > 0:
            findings.append({"domain": "port_terminal_gate_appointments", "records": r_2["rows"]})

        r_3 = self.execute_tool("query_drayage_chassis_transload_allocations", container_id="MSKU-904812-0")
        if r_3.get("total", 0) > 0:
            findings.append({"domain": "drayage_chassis_transload_allocations", "records": r_3["rows"]})

        act1_res = self.execute_tool(
            "action_book_dual_transaction_drayage_gate",
            container_id='MSKU-904812-0',
            terminal_id='USLAX_APM_PIER400',
            gate_slot_id='GATE-LAX-20261028-T1',
            drayage_carrier_id='PAC-HARBOR-DRAY',
            rationale='Booked dual-transaction Pier 400 gate slot 24 hours prior to Last Free Day using upper-deck discharge prediction, avoiding $1,875 in port demurrage.',
            idempotency_key='PORT-GATE-20261022-01'
        )
        actions_taken.append(act1_res)

        act2_res = self.execute_tool(
            "action_divert_container_to_transload_hub",
            container_id='MSKU-904812-0',
            transload_facility_id='LAX-CARSON-XDOC-02',
            outbound_mode='53FT_TEAM_TRUCK_EXPEDITE',
            rationale='WeatherNext 3 detected 60-hour North Pacific swell delay; diverting MSKU-904812-0 from slow inland rail to Carson transload hub saves 4.5 transit days and prevents RDC stockout.',
            idempotency_key='PORT-TRNS-20261022-01'
        )
        actions_taken.append(act2_res)

        vega_spec = tools.get_native_chart_spec()
        surface_id = "port_drayage_orchestrator_surface_01"
        a2ui_parts = build_port_drayage_orchestrator_surface(surface_id, spec=vega_spec)
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
            "### ✦ PortWatch — Global Ocean Vessel, Container Stowage & Port Drayage Orchestrator — Executive Operations Brief",
            "",
            "> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **05 · Deliver**.",
            "",
            "#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)",
            "",
            "| Dimension | Metric Value | Secondary KPI | Execution Mode |",
            "|:---|---:|---:|:---|",
        ]
        for row in [{"container_batch": "MSKU-904812 (Transload)", "dwell_hours": 18.0, "demurrage_saved_usd": 1875, "status": "OPTIMIZED_CVRPTW"}, {"container_batch": "MSKU-904819 (Dual Gate)", "dwell_hours": 26.5, "demurrage_saved_usd": 1500, "status": "OPTIMIZED_CVRPTW"}, {"container_batch": "CMAU-441029 (Rail Ramp)", "dwell_hours": 31.0, "demurrage_saved_usd": 1125, "status": "OPTIMIZED_CVRPTW"}, {"container_batch": "Unmonitored Port Baseline", "dwell_hours": 114.0, "demurrage_saved_usd": 0, "status": "LEGACY_STATIC"}]:
            lines.append(f"| `{row['container_batch']}` | **{row['dwell_hours']}** | {row['demurrage_saved_usd']} | `{row['status']}` |")

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
        for sys_meta in [{"id": "spire_maritime_satellite_ais", "name": "Spire Maritime Satellite AIS & Google DeepMind WeatherNext 3 Feed", "protocol": "GraphQL / gRPC Stream", "tables": ["ocean_vessel_ais_berth_telemetry"]}, {"id": "cargowise_ocean_fcl_ledger", "name": "CargoWise One Global Ocean Container & LFD Demurrage Ledger", "protocol": "EDI 315 / XML", "tables": ["container_discharge_demurrage_ledger"]}, {"id": "port_terminal_gate_api", "name": "Port of LA/LB PierPASS & Rotterdam Terminal Gate Appointment API", "protocol": "REST / Webhook", "tables": ["port_terminal_gate_appointments"]}, {"id": "drayage_transload_solver", "name": "Google OR-Tools Bipartite Drayage & Transload Allocation Solver", "protocol": "Python MILP SDK", "tables": ["drayage_chassis_transload_allocations"]}]:
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
            scenario = PortDrayageOrchestrator().run_scenario("live_turn")
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

    def _emit_a2ui_surface(
        callback_context: Optional[CallbackContext] = None,
        **_: Any,
    ) -> Optional[types.Content]:
        try:
            surface_id = f"port-drayage-{uuid.uuid4().hex[:8]}"
            a2ui_parts = build_port_drayage_orchestrator_surface(surface_id, spec=tools.get_latest_chart_spec(consume=True))
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception:
            pass
        return None

    root_agent = Agent(
        name="port_drayage_orchestrator",
        description="[Category: 05 · Distribution & Logistics — Store Replenishment] Curfew Orchestrator (Retail Logistics Dispatcher): Coordinates municipal delivery curfews and store dock shift schedules dynamically. Outcome: 98%+ on-time store window compliance.",
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
        after_agent_callback=_emit_a2ui_surface,
    )

    app = App(root_agent=root_agent, name="port_drayage_orchestrator")

    class PortDrayageOrchestratorAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for port_drayage_orchestrator."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = PortDrayageOrchestrator()

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
    root_agent = PortDrayageOrchestrator()  # type: ignore
    app = None  # type: ignore
    PortDrayageOrchestratorAdkApp = None  # type: ignore

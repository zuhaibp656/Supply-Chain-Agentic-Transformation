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

STRICT CONCISE & PYTHON-FIRST EXECUTION PROTOCOL:
- Lead with a 1–2 sentence deterministic KPI conclusion citing exact IDs and numbers from Python tools (zero fluff/filler).
- Always run Python tools (`analyze_operational_metrics`, `query_*`, `lookup_xyz_master_context`) for math and aggregations—never estimate mentally.
- Call `render_visual_chart` when visual comparison helps; the interactive A2UI `VegaChart` card renders automatically (never paste raw Vega-Lite JSON or base64 in text).
- Keep Markdown tables outside the card concise (`<=5` columns) for clean Google Sheets copy-paste.
- Call `draft_operational_brief` ONLY when drafting a formal memo, claim, or brief is requested or required.
- Never call `action_*` write-back tools on read-only questions.
"""

_AVAILABLE_TOOLS = [
    tools.query_yard_trailer_geofence_status,
    tools.query_yard_spotter_move_tasks,
    tools.query_dock_door_turnaround_schedules,
    tools.query_carrier_detention_risk_records,
    tools.action_dispatch_yard_spotter_move,
    tools.action_resolve_carrier_detention_alert,
    tools.list_systems,
    tools.lookup_xyz_master_context,
    tools.analyze_operational_metrics,
    tools.render_visual_chart,
    tools.draft_operational_brief,
]

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
        self.name = "yard_dock_sequencer"
        self.category = "05 · Distribution & Logistics — First & Mid-Mile"
        self.display_name = "[05 · Logistics | First & Mid-Mile] Yard Disruption Agent"
        self.description = "[Category: 05 · Distribution & Logistics — First & Mid-Mile] Yard Disruption Agent (Yard Master / Plant Logistics): Parses GPS & gate feeds to flag delays and reassign dock staging doors dynamically. Outcome: Eliminates demurrage & line starvation."
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
            "> **Executive Summary**: Real-time trailer geofencing powered by **Google Maps Fleet Engine** at **Dallas Distribution Center Yard 02** flagged an acute demurrage risk on **Swift Transportation trailer `TRL-SWIFT-7741`**. The trailer had accumulated **85.0 minutes of dwell** in Slot South 44, leaving only **35 minutes** before breaching the carrier's **120-minute free detention threshold** ($85.00/hour demurrage charge). YardPulse dynamically dispatched terminal tractor **`SPOTTER-HOSTLER-03`** under high-priority expedite, moving the trailer to ready **Door Crossdock 08**. Unloading crew Delta-02 was assigned, completing turnaround at **95.0 minutes (25 minutes ahead of cutoff)** and saving **$255.00 in accessorial detention penalties**.",
            "",
            "#### 📊 Inbound Trailer Turnaround & Demurrage Risk Telemetry (Atomic Copy-Ready Table)",
            "",
            "| Trailer ID | Carrier Name | Current Yard Slot | Assigned Dock Door | Dwell Time | Free Time Remaining | Expedite Action | Detention Penalty Avoided |",
            "|:---|:---|:---|:---|---:|---:|:---|---:|",
            "| `TRL-SWIFT-7741` | Swift Transportation | Slot South 44 | **Door Crossdock 08** | **85.0 min** | **35.0 min** | `SPOTTER_EXPEDITE_DISPATCHED` | **$255.00 (Neutralized)** |",
            "| `TRL-JB-HUNT-1204` | J.B. Hunt | Slot North 12 | Door Outbound 14 | 35.0 min | 85.0 min | `ON_SCHEDULE_LOADING` | $0.00 (In-Spec) |",
            "| `TRL-SCHNEIDER-882` | Schneider National | Slot West 06 | Door Inbound 02 | 48.0 min | 72.0 min | `ON_SCHEDULE_UNLOAD` | $0.00 (In-Spec) |",
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

    def _emit_a2ui_surface(
        callback_context: Optional[CallbackContext] = None,
        **_: Any,
    ) -> Optional[types.Content]:
        try:
            surface_id = f"yard-dock-sequen-{uuid.uuid4().hex[:8]}"
            a2ui_parts = build_yard_dock_surface(surface_id, spec=tools.get_latest_chart_spec(consume=True))
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception:
            pass
        return None

    root_agent = Agent(
        name='yard_dock_sequencer',
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
        after_agent_callback=_emit_a2ui_surface,
    )

    app = App(root_agent=root_agent, name='yard_dock_sequencer')

    class YardDockSchedulingAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for yard_dock_sequencer."""

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

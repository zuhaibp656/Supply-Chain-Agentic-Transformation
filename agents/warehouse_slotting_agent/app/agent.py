"""SlotMaster Dynamic 3D Warehouse Wave & Slotting Optimizer — High-Code Google ADK Agent.

Performs 3D warehouse velocity slotting, minimizes picker walking distance via golden zone allocation,
dispatches AMR robot swarms, and balances real-time wave release to eliminate aisle congestion.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_warehouse_slotting_chart_spec
from .render.surfaces import build_warehouse_slotting_surface

_INSTRUCTION = """You are SlotMaster, the Dynamic 3D Warehouse Wave & Slotting Optimizer for Intralogistics & DC Fulfillment Operations.

PRIMARY OBJECTIVE:
Maximize warehouse pick throughput and minimize operator travel distance using 3D velocity slotting and ergonomic golden zone placement.
Analyze high-velocity SKU lines (Tier A fast-movers) and detect slotting mismatches where high-velocity items are located in deep mezzanine aisles or non-ergonomic overhead bins.
Reassign fast-movers to waist-height golden zone pick faces nearest to outbound packing stations,
balance wave release order batches across warehouse zones to prevent aisle gridlock among human pickers and Autonomous Mobile Robots (AMRs),
and dispatch automated WMS stock relocation move tickets and wave throttling rules.

TOOL USAGE PROTOCOL:
- Ground all distance metrics and pick velocities strictly in connected tools (`query_warehouse_slotting_velocity_tiers`,
  `query_amr_picker_travel_telemetry`, `query_wave_release_order_allocations`, `query_slot_reassignment_recommendations`).
- Never invent walking distances, pick frequencies, or congestion scores.
- When an SKU in Tier A requires > 100 meters travel to pack station, recommend relocation to golden zone bins.
- Before executing mutations (`action_execute_slot_reassignment`, `action_balance_wave_release_profile`),
  ensure all required fields and a non-empty `idempotency_key` are provided.

RESPONSE STANDARDS:
1. Executive Quality Brief: Deliver copy-ready markdown tables detailing SKU Name, Velocity Tier, Current Bin, Recommended Bin, Travel Distance Delta, Daily Km Saved, and WMS Status.
2. Direct Actionability: Include exact Relocation Task ID, WMS Move Ticket ID, and Wave Throttle ID.

STRICT CONCISE & PYTHON-FIRST EXECUTION PROTOCOL:
- Lead with a 1–2 sentence deterministic KPI conclusion citing exact IDs and numbers from Python tools (zero fluff/filler).
- Always run Python tools (`analyze_operational_metrics`, `query_*`, `lookup_xyz_master_context`) for math and aggregations—never estimate mentally.
- Call `render_visual_chart` when visual comparison helps; the interactive A2UI `VegaChart` card renders automatically (never paste raw Vega-Lite JSON or base64 in text).
- Keep Markdown tables outside the card concise (`<=5` columns) for clean Google Sheets copy-paste.
- Call `draft_operational_brief` ONLY when drafting a formal memo, claim, or brief is requested or required.
- Never call `action_*` write-back tools on read-only questions.
"""

_AVAILABLE_TOOLS = [
    tools.query_warehouse_slotting_velocity_tiers,
    tools.query_amr_picker_travel_telemetry,
    tools.query_wave_release_order_allocations,
    tools.query_slot_reassignment_recommendations,
    tools.action_execute_slot_reassignment,
    tools.action_balance_wave_release_profile,
    tools.list_systems,
    tools.lookup_xyz_master_context,
    tools.analyze_operational_metrics,
    tools.render_visual_chart,
    tools.draft_operational_brief,
]

_WRITE_TOOLS = {
    "action_execute_slot_reassignment": ["sku_id", "current_bin_id", "target_bin_id", "priority", "rationale"],
    "action_balance_wave_release_profile": ["wave_id", "zone_id", "max_concurrent_pickers", "release_status", "rationale"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs, pick limits, and idempotency."""
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
        if tool_name == "action_balance_wave_release_profile":
            limit = int(args.get("max_concurrent_pickers", 0))
            if limit <= 0:
                return {
                    "error": "invalid_picker_limit",
                    "tool": tool_name,
                    "escalation": "reject_mutation"
                }
    return None


class WarehouseSlottingOptimizer:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3-pro-preview"):
        self.name = "warehouse_slotting_agent"
        self.category = "04 · Inventory & Warehousing — Warehouse Operations"
        self.display_name = "[04 · Inventory & DC | Warehouse Operations] Dynamic Slotting Agent"
        self.description = "[Category: 04 · Inventory & Warehousing — Warehouse Operations] Dynamic Slotting Agent (DC Operations Mgr / IE Lead): Evaluates co-pick affinity matrices to recommend fast-pick zone re-slotting. Outcome: Reduces picker transit time by 15–30%."
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
        """Executes an autonomous 3D slotting optimization, stock relocation move dispatch, and wave throttling scenario."""
        findings = []
        actions_taken = []

        # 1. Query Warehouse Slotting Velocity Tiers
        tiers = self.execute_tool("query_warehouse_slotting_velocity_tiers", velocity_tier="FAST_MOVER")
        if tiers.get("total", 0) > 0:
            findings.append({"domain": "warehouse_slotting_velocity_tiers", "records": tiers["rows"]})

        # 2. Query AMR Picker Travel Telemetry
        telemetry = self.execute_tool("query_amr_picker_travel_telemetry", dc_id="RDC-DALLAS-02")
        if telemetry.get("total", 0) > 0:
            findings.append({"domain": "amr_picker_travel_telemetry", "records": telemetry["rows"]})

        # 3. Query Wave Release Allocations
        waves = self.execute_tool("query_wave_release_order_allocations", dc_id="RDC-DALLAS-02")
        if waves.get("total", 0) > 0:
            findings.append({"domain": "wave_release_order_allocations", "records": waves["rows"]})

        # 4. Query Slot Reassignment Recommendations
        recs = self.execute_tool("query_slot_reassignment_recommendations", sku_id="SKU-BEV-OATMILK-ORIGINAL-1L")
        if recs.get("total", 0) > 0:
            findings.append({"domain": "slot_reassignment_recommendations", "records": recs["rows"]})

        # 5. Dispatch Slot Reassignment Physical Move Task
        if recs.get("total", 0) > 0:
            target_rec = recs["rows"][0]
            move_res = self.execute_tool(
                "action_execute_slot_reassignment",
                sku_id=target_rec["sku_id"],
                current_bin_id=target_rec["current_bin_id"],
                target_bin_id=target_rec["recommended_bin_id"],
                priority="HIGH",
                rationale="Fast-mover SKU-BEV-OATMILK relocated from mezzanine Aisle 14 (142m walk) to golden zone Aisle 02 (22m walk), saving 100.8 km of walking and 412 labor hours annually.",
                idempotency_key="SLOT-MOVE-20261022-01"
            )
            actions_taken.append(move_res)

        # 6. Throttle Saturated Wave in Bulk Mezzanine
        if waves.get("total", 0) > 0:
            target_wave = waves["rows"][0]
            wave_res = self.execute_tool(
                "action_balance_wave_release_profile",
                wave_id=target_wave["wave_id"],
                zone_id=target_wave["zone_id"],
                max_concurrent_pickers=target_wave["recommended_max_pickers"],
                release_status="THROTTLED_FOR_CONGESTION",
                rationale="Zone Bulk Mezzanine congestion score at 0.84 with 16 active pickers. Throttling wave release cap to 10 pickers restores target pick rate to 140 lines/hr.",
                idempotency_key="WAVE-THROT-20261022-01"
            )
            actions_taken.append(wave_res)

        # Generate VegaChart spec
        vega_spec = tools.get_native_chart_spec()
        surface_id = "warehouse_slotting_surface_01"
        a2ui_parts = build_warehouse_slotting_surface(surface_id, spec=vega_spec)

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
        """Renders executive brief, copy-ready tables, and slotting audit ledger."""
        lines = [
            "### 🏗️ SlotMaster 3D Warehouse Velocity Slotting & Wave Optimization Briefing",
            "",
            "> **Executive Summary**: Comprehensive 3D warehouse slotting telemetry at **RDC Dallas (South Regional DC)** diagnosed severe picker travel inefficiency and mezzanine congestion. Fast-mover **Barista Organic Oat Milk 1L** (840 lines/day) was improperly slotted on overhead mezzanine shelves in **Aisle 14** (142 meters from pack stations), forcing AMR bots and pickers to spend **68.2% of shift time walking** and generating aisle gridlock (congestion score 0.84). Dispatched a high-priority WMS physical relocation task moving Oat Milk to **Aisle 02 Golden Zone** (22 meters from pack), cutting travel distance by **84.5% (-120m per pick)** and eliminating **100.8 km of walking per day (412 annual labor hours saved)**. Concurrently throttled concurrent pickers in Zone Bulk Mezzanine from 16 down to 10 to clear traffic jams.",
            "",
            "#### 📊 3D Velocity Slotting & Picker Travel Impact (Atomic Copy-Ready Table)",
            "",
            "| Product SKU | Velocity Class | Current Bin Location | Recommended Golden Bin | Baseline Walk | Optimized Walk | Daily Travel Saved | Ergonomic Status |",
            "|:---|:---|:---|:---|---:|---:|---:|:---|",
            "| `SKU-BEV-OATMILK-1L` | **Tier A (840 lines/day)** | Aisle 14 Shelf 04 (High) | **Aisle 02 Shelf 02 (Golden)** | 142.0 m | **22.0 m** | **100.8 km/day** | `ERGONOMIC_WAIST_HEIGHT` |",
            "| `SKU-BEV-ALMOND-1L` | Tier B (310 lines/day) | Aisle 05 Shelf 02 (Golden) | Aisle 05 Shelf 02 (Golden) | 45.0 m | 45.0 m | 0.0 km/day | `OPTIMALLY_SLOTTED` |",
            "| `SKU-BEV-SOY-1L` | Tier B (280 lines/day) | Aisle 11 Shelf 03 (High) | Aisle 06 Shelf 02 (Golden) | 88.0 m | 35.0 m | 28.5 km/day | `PENDING_PHASE_2` |",
            "",
            "#### ⚡ Automated WMS Move Tickets & Wave Release Controls Executed",
            ""
        ]

        for act in actions:
            if "relocation_task_id" in act:
                lines.append(f"- **WMS Stock Relocation Task Dispatched**: `{act['relocation_task_id']}` | SKU: `{act['sku_id']}` | From: `{act['current_bin_id']}` ➔ To: `{act['target_bin_id']}` | Ticket: `{act['wms_move_ticket_id']}` | Status: `{act['status']}`")
            elif "wave_throttle_id" in act:
                lines.append(f"- **Wave Release Profile Rebalanced**: `{act['wave_throttle_id']}` | Wave: `{act['wave_id']}` | Zone: `{act['zone_id']}` | Picker Cap: **{act['max_concurrent_pickers']} pickers** | Status: `{act['status']}`")

        lines.extend([
            "",
            "### 🔗 Connected Intralogistics & Robotic Swarm Architecture",
            "- **Manhattan Active WMS 3D Slotting**: Real-time velocity heatmap, cubic utilization, and pick frequency profiling.",
            "- **KION / Dematic AMR Controller**: VDA 5050 autonomous mobile robot fleet dispatch, pathing, and collision avoidance.",
            "- **Blue Yonder Wave Engine**: Dynamic order batching, zone picker caps, and bottleneck pacing.",
            "- **OSHA Ergonomic Standard Module**: Elimination of overhead reach and deep-bend heavy SKU lifting injuries."
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
    from .render.surfaces import build_warehouse_slotting_surface

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
            surface_id = f"warehouse-slotti-{uuid.uuid4().hex[:8]}"
            a2ui_parts = build_warehouse_slotting_surface(surface_id, spec=tools.get_latest_chart_spec(consume=True))
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception:
            pass
        return None

    root_agent = Agent(
        name='warehouse_slotting_agent',
        description='[Category: 04 · Inventory & Warehousing — Warehouse Operations] Dynamic Slotting Agent (DC Operations Mgr / IE Lead): Evaluates co-pick affinity matrices to recommend fast-pick zone re-slotting. Outcome: Reduces picker transit time by 15–30%.',
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

    app = App(root_agent=root_agent, name='warehouse_slotting_agent')

    class WarehouseSlottingOptimizerAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for warehouse_slotting_agent."""

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
    root_agent = WarehouseSlottingOptimizer()  # type: ignore

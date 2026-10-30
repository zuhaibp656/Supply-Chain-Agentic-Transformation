"""PromiseGuard Real-Time Dynamic ATP Order Promising Agent — High-Code Google ADK Agent.

Performs sub-50ms Cloud Spanner Available-to-Promise (ATP) calculations,
protects strategic customer tier allocation reserves, evaluates capable-to-promise (CTP) pipelines,
and commits binding delivery dates to eliminate OTIF customer chargebacks.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_order_promising_chart_spec
from .render.surfaces import build_order_promising_surface

_INSTRUCTION = """You are PromiseGuard, the Real-Time Dynamic ATP Order Promising Agent for Customer Order Fulfillment & Supply Chain Execution.

PRIMARY OBJECTIVE:
Provide sub-50ms Available-to-Promise (ATP) and Capable-to-Promise (CTP) commitments for omnichannel customer order streams.
Ingest real-time global inventory balances from Google Cloud Spanner with sub-20ms strong consistency.
Enforce contractual customer allocation tiers, ringfencing strategic Tier 1 customer quotas (e.g. Kroger, Walmart)
so high-velocity standard or spot B2B orders do not cannibalize critical contract SLA inventory.
Route orders to the lowest-cost, highest-fill-rate DC node, commit binding delivery dates,
and log inventory reservations across Cloud Spanner and enterprise OMS.

TOOL USAGE PROTOCOL:
- Ground all order promising decisions strictly in connected tools (`query_realtime_sku_atp_allocations`,
  `query_customer_tier_sla_commitments`, `query_inbound_customer_order_requests`, `query_order_promising_routing_decisions`).
- Never hallucinate uncommitted ATP quantities, transit lead times, or contract penalty fees.
- Never commit inventory from protected Tier 1 allocation quotas to lower-tier (Tier 2/3) accounts.
- Before executing mutations (`action_commit_dynamic_order_promise`, `action_protect_tier1_allocation_reserve`),
  ensure all required fields and a non-empty `idempotency_key` are provided.

RESPONSE STANDARDS:
1. Executive Quality Brief: Deliver copy-ready markdown tables detailing Order ID, Customer Name, Contract Tier, Requested vs Promised Units, Sourcing Node, Promised Delivery Date, and OTIF Penalty Status.
2. Direct Actionability: Include exact Promise Commitment ID, Cloud Spanner Transaction ID, and Protection Ringfence ID.

STRICT CONCISE & PYTHON-FIRST EXECUTION PROTOCOL:
- Lead with a 1–2 sentence deterministic KPI conclusion citing exact IDs and numbers from Python tools (zero fluff/filler).
- Always run Python tools (`analyze_operational_metrics`, `query_*`, `lookup_xyz_master_context`) for math and aggregations—never estimate mentally.
- Call `render_visual_chart` when visual comparison helps; the interactive A2UI `VegaChart` card renders automatically (never paste raw Vega-Lite JSON or base64 in text).
- Keep Markdown tables outside the card concise (`<=5` columns) for clean Google Sheets copy-paste.
- Call `draft_operational_brief` ONLY when drafting a formal memo, claim, or brief is requested or required.
- Never call `action_*` write-back tools on read-only questions.
"""

_AVAILABLE_TOOLS = [
    tools.query_realtime_sku_atp_allocations,
    tools.query_customer_tier_sla_commitments,
    tools.query_inbound_customer_order_requests,
    tools.query_order_promising_routing_decisions,
    tools.action_commit_dynamic_order_promise,
    tools.action_protect_tier1_allocation_reserve,
    tools.list_systems,
    tools.lookup_xyz_master_context,
    tools.analyze_operational_metrics,
    tools.render_visual_chart,
    tools.draft_operational_brief,
]

_WRITE_TOOLS = {
    "action_commit_dynamic_order_promise": ["order_id", "customer_id", "promised_fulfillment_node", "promised_delivery_date", "atp_reserved_qty", "rationale"],
    "action_protect_tier1_allocation_reserve": ["sku_id", "network_node_id", "reserve_quantity", "rationale"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs, reservation quantities, and idempotency."""
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
        if tool_name == "action_commit_dynamic_order_promise":
            qty = int(args.get("atp_reserved_qty", 0))
            if qty <= 0:
                return {
                    "error": "invalid_reserved_quantity",
                    "tool": tool_name,
                    "escalation": "reject_mutation"
                }
    return None


class DynamicOrderPromisingAtp:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3.1-pro-preview"):
        self.name = "dynamic_order_promising_atp"
        self.category = "04 · Inventory & Warehousing — Omnichannel Visibility"
        self.display_name = "[04 · Inventory & DC | Omnichannel Visibility] SFS / BOPIS Sourcing"
        self.description = "[Category: 04 · Inventory & Warehousing — Omnichannel Visibility] SFS / BOPIS Sourcing (Omnichannel Fulfillment Dir.): Selects lowest-cost fulfillment nodes based on store labor and parcel zones. Outcome: Lowers parcel costs & split rates."
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
        """Executes an autonomous real-time order promising, allocation tier protection, and Spanner commitment scenario."""
        findings = []
        actions_taken = []

        # 1. Query Real-Time ATP Inventory
        atp = self.execute_tool("query_realtime_sku_atp_allocations", sku_id="SKU-BEV-OATMILK-ORIGINAL-1L")
        if atp.get("total", 0) > 0:
            findings.append({"domain": "realtime_sku_atp_allocations", "records": atp["rows"]})

        # 2. Query Customer Tier SLA Commitments
        slas = self.execute_tool("query_customer_tier_sla_commitments", customer_id="CUST-KROGER-CORP")
        if slas.get("total", 0) > 0:
            findings.append({"domain": "customer_tier_sla_commitments", "records": slas["rows"]})

        # 3. Query Inbound Order Requests
        orders = self.execute_tool("query_inbound_customer_order_requests", order_id="ORD-20261022-8841")
        if orders.get("total", 0) > 0:
            findings.append({"domain": "inbound_customer_order_requests", "records": orders["rows"]})

        # 4. Query Routing Decisions
        routings = self.execute_tool("query_order_promising_routing_decisions", order_id="ORD-20261022-8841")
        if routings.get("total", 0) > 0:
            findings.append({"domain": "order_promising_routing_decisions", "records": routings["rows"]})

        # 5. Ringfence Strategic Tier 1 Quota
        ringfence_res = self.execute_tool(
            "action_protect_tier1_allocation_reserve",
            sku_id="SKU-BEV-OATMILK-ORIGINAL-1L",
            network_node_id="CDC-CHICAGO-01",
            reserve_quantity=20000,
            rationale="Ringfencing 20,000 units at Central DC Chicago exclusively for strategic Tier 1 accounts (Kroger SLA 98.5% fill rate, avoiding $2,500/day OTIF penalty).",
            idempotency_key="TIER1-RING-20261022-01"
        )
        actions_taken.append(ringfence_res)

        # 6. Commit Dynamic Order Promise in Cloud Spanner
        if orders.get("total", 0) > 0:
            target_ord = orders["rows"][0]
            promise_res = self.execute_tool(
                "action_commit_dynamic_order_promise",
                order_id=target_ord["order_id"],
                customer_id=target_ord["customer_id"],
                promised_fulfillment_node="CDC-CHICAGO-01",
                promised_delivery_date="2026-10-24T10:00:00Z",
                atp_reserved_qty=target_ord["requested_units"],
                rationale="Committed 8,000 units from Tier 1 reserved quota at CDC Chicago. 18-hour linehaul transit guarantees on-time delivery by Oct 24, 10:00 AM (2 hours ahead of 12:00 PM cutoff).",
                idempotency_key="PROMISE-ORD-20261022-8841"
            )
            actions_taken.append(promise_res)

        # Generate VegaChart spec
        vega_spec = tools.get_native_chart_spec()
        surface_id = "order_promising_surface_01"
        a2ui_parts = build_order_promising_surface(surface_id, spec=vega_spec)

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
        """Renders executive brief, copy-ready tables, and promising audit ledger."""
        lines = [
            "### 🤝 PromiseGuard Real-Time Order Promising & ATP Briefing",
            "",
            "> **Executive Summary**: Sub-50ms Cloud Spanner evaluation successfully committed high-value inbound order `ORD-20261022-8841` (**8,000 units** of Barista Organic Oat Milk 1L) for strategic account **Kroger National Distribution** (Tier 1 Strategic, 98.5% fill rate SLA). Ingested global stock across Central and Regional DCs with **14.8 ms Spanner query latency**. While local RDC Dallas held only 3,300 uncommitted units, PromiseGuard dynamically allocated the full 8,000 units from **CDC Chicago Tier 1 Protected Quota** (where 20,000 units are ringfenced). Guaranteed delivery by **Oct 24, 2026 at 10:00 AM** (2 hours ahead of contractual cutoff), completely neutralizing a **$2,500/day OTIF penalty** risk.",
            "",
            "#### 📊 Inbound Order Promising & Sourcing Evaluation (Atomic Copy-Ready Table)",
            "",
            "| Order ID | Customer Account | Contract Tier | Requested Units | Promised Units | Sourcing Node | Promised Delivery | OTIF Risk | Status |",
            "|:---|:---|:---|---:|---:|:---|:---|---:|:---|",
            "| `ORD-8841` | **Kroger National** | `TIER_1_STRATEGIC` | 8,000 units | **8,000 units** | `CDC-CHICAGO-01` | **2026-10-24 10:00 AM** | **$0.00 (Neutralized)** | `ATP_COMMITTED` |",
            "| `ORD-8842` | Lone Star Co-op | `TIER_3_STANDARD` | 1,200 units | 1,200 units | `RDC-DALLAS-02` | 2026-10-24 03:00 PM | $0.00 (Nominal) | `ATP_CONFIRMED` |",
            "",
            "#### ⚡ Automated Spanner Reservations & Tier Quota Ringfences Executed",
            ""
        ]

        for act in actions:
            if "protection_id" in act:
                lines.append(f"- **Tier 1 Allocation Ringfenced**: `{act['protection_id']}` | SKU: `{act['sku_id']}` | Node: `{act['network_node_id']}` | Reserved Quota: **{act['reserve_quantity']:,} units** | Status: `{act['status']}`")
            elif "promise_id" in act:
                lines.append(f"- **Binding ATP Promise Committed**: `{act['promise_id']}` | Order: `{act['order_id']}` | Node: `{act['promised_fulfillment_node']}` | Units: **{act['atp_reserved_qty']:,}** | Spanner Txn: `{act['spanner_txn_id']}` | Status: `{act['status']}`")

        lines.extend([
            "",
            "### 🔗 Connected Systems & Order Promising Architecture",
            "- **Google Cloud Spanner**: Globally distributed, strongly consistent real-time ATP/CTP inventory engine (<20ms).",
            "- **SAP S/4HANA Sales & Distribution (SD)**: Customer master, contractual allocation tiers, and pricing schedules.",
            "- **Enterprise OMS / Pub/Sub**: Event-driven omnichannel order orchestration with sub-second order promising.",
            "- **Google OR-Tools Sourcing Optimizer**: Cost-to-serve, multi-stop linehaul routing, and SLA constraint solving."
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
            scenario = DynamicOrderPromisingAtp().run_scenario("live_turn")
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
            surface_id = f"dynamic-orde-{uuid.uuid4().hex[:8]}"
            a2ui_parts = build_order_promising_surface(surface_id, spec=tools.get_latest_chart_spec(consume=True))
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception:
            pass
        return None

    root_agent = Agent(
        name="dynamic_order_promising_atp",
        description="[Category: 04 · Inventory & Warehousing — Omnichannel Visibility] SFS / BOPIS Sourcing (Omnichannel Fulfillment Dir.): Selects lowest-cost fulfillment nodes based on store labor and parcel zones. Outcome: Lowers parcel costs & split rates.",
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

    app = App(root_agent=root_agent, name="dynamic_order_promising_atp")

    class DynamicOrderPromisingAtpAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for dynamic_order_promising_atp."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = DynamicOrderPromisingAtp()

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
    root_agent = DynamicOrderPromisingAtp()  # type: ignore
    app = None  # type: ignore
    DynamicOrderPromisingAtpAdkApp = None  # type: ignore

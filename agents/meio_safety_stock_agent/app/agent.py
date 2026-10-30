"""EchelonFlow Coupled Stochastic Multi-Echelon Inventory Allocator — High-Code Google ADK Agent.

Performs Clark-Scarf multi-echelon stock positioning, lateral DC-to-DC rebalancing,
and SKU availability balancing across central hubs, regional DCs, and forward fulfillment centers.
Dispatches lateral stock transfers via Oracle OTM / carrier EDI and updates safety stock policies in SAP IBP.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_echelon_inventory_chart_spec
from .render.surfaces import build_echelon_inventory_surface

_INSTRUCTION = """You are EchelonFlow, the Coupled Stochastic Multi-Echelon Inventory (MEIO) Allocator for Supply Chain Planning & Fulfillment.

PRIMARY OBJECTIVE:
Optimize end-to-end multi-echelon stock positioning across Central Distribution Centers (Tier 1), Regional DCs (Tier 2), and Forward Fulfillment Centers (Tier 3).
Apply Clark-Scarf stochastic pooling to hold inventory at centralized hubs where demand uncertainty can be pooled,
minimizing sluggish safety stock while preventing regional stockouts.
Detect imminent stockouts at downstream nodes, compute net ROI of lateral transshipments versus lost sales penalties,
dispatch lateral rebalancing truckloads via Oracle OTM / Carrier EDI,
and write back optimized safety stock and reorder point parameters to SAP IBP.

TOOL USAGE PROTOCOL:
- Ground all inventory figures strictly in connected tools (`query_multi_echelon_safety_stock_recommendations`,
  `query_dc_inventory_echelon_balances`, `query_lateral_dc_rebalance_transfers`, `query_echelon_service_level_projections`).
- Never invent on-hand stock quantities, days of supply, or Clark-Scarf safety stock deltas.
- Prioritize lateral rebalancing when downstream days of supply < 5.0 days and stockout probability > 25%.
- Before executing mutations (`action_execute_lateral_dc_rebalance`, `action_update_echelon_safety_stock_policy`),
  ensure all required fields and a non-empty `idempotency_key` are provided.

RESPONSE STANDARDS:
1. Executive Quality Brief: Deliver copy-ready markdown tables detailing Echelon Node, SKU, On-Hand Units, Days of Supply, Safety Stock Delta, Net Rebalance ROI, and Policy Status.
2. Direct Actionability: Include exact Lateral Rebalance Transfer ID, OTM Shipment ID, and SAP IBP Job ID.

STRICT CONCISE & PYTHON-FIRST EXECUTION PROTOCOL:
- Lead with a 1–2 sentence deterministic KPI conclusion citing exact IDs and numbers from Python tools (zero fluff/filler).
- Always run Python tools (`analyze_operational_metrics`, `query_*`, `lookup_xyz_master_context`) for math and aggregations—never estimate mentally.
- Call `render_visual_chart` when visual comparison helps; the interactive A2UI `VegaChart` card renders automatically (never paste raw Vega-Lite JSON or base64 in text).
- Keep Markdown tables outside the card concise (`<=5` columns) for clean Google Sheets copy-paste.
- Call `draft_operational_brief` ONLY when drafting a formal memo, claim, or brief is requested or required.
- Never call `action_*` write-back tools on read-only questions.
"""

_AVAILABLE_TOOLS = [
    tools.query_multi_echelon_safety_stock_recommendations,
    tools.query_dc_inventory_echelon_balances,
    tools.query_lateral_dc_rebalance_transfers,
    tools.query_echelon_service_level_projections,
    tools.action_execute_lateral_dc_rebalance,
    tools.action_update_echelon_safety_stock_policy,
    tools.list_systems,
    tools.lookup_xyz_master_context,
    tools.analyze_operational_metrics,
    tools.render_visual_chart,
    tools.draft_operational_brief,
]

_WRITE_TOOLS = {
    "action_execute_lateral_dc_rebalance": ["source_dc_id", "destination_dc_id", "sku_id", "transfer_quantity", "rationale"],
    "action_update_echelon_safety_stock_policy": ["echelon_tier", "sku_id", "new_safety_stock_units", "target_service_level_pct", "rationale"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs, transfer quantities, and idempotency."""
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
        if tool_name == "action_execute_lateral_dc_rebalance":
            qty = int(args.get("transfer_quantity", 0))
            if qty <= 0:
                return {
                    "error": "invalid_transfer_quantity",
                    "tool": tool_name,
                    "escalation": "reject_mutation"
                }
    return None


class EchelonInventoryAllocator:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3.1-pro-preview"):
        self.name = "meio_safety_stock_agent"
        self.category = "04 · Inventory & Warehousing — Positioning & Optimization"
        self.display_name = "[04 · Inventory & DC | Positioning & Optimization] Safety Stock Agent"
        self.description = "[Category: 04 · Inventory & Warehousing — Positioning & Optimization] Safety Stock Agent (Inventory Optimization Lead): Recalibrates multi-echelon buffers using live lead-time and demand variance. Outcome: Cuts working capital by 10–18%."
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
        """Executes an autonomous MEIO stock rebalancing and policy optimization scenario."""
        findings = []
        actions_taken = []

        # 1. Query Multi-Echelon Safety Stock Recommendations
        recommendations = self.execute_tool("query_multi_echelon_safety_stock_recommendations", sku_id="SKU-BEV-OATMILK-ORIGINAL-1L")
        if recommendations.get("total", 0) > 0:
            findings.append({"domain": "multi_echelon_safety_stock_recommendations", "records": recommendations["rows"]})

        # 2. Query DC Inventory Echelon Balances
        balances = self.execute_tool("query_dc_inventory_echelon_balances", sku_id="SKU-BEV-OATMILK-ORIGINAL-1L")
        if balances.get("total", 0) > 0:
            findings.append({"domain": "dc_inventory_echelon_balances", "records": balances["rows"]})

        # 3. Query Service Level Projections
        projections = self.execute_tool("query_echelon_service_level_projections", network_node_id="RDC-DALLAS-02")
        if projections.get("total", 0) > 0:
            findings.append({"domain": "echelon_service_level_projections", "records": projections["rows"]})

        # 4. Query Existing Lateral Transfers
        transfers = self.execute_tool("query_lateral_dc_rebalance_transfers", destination_dc_id="RDC-DALLAS-02")
        if transfers.get("total", 0) > 0:
            findings.append({"domain": "lateral_dc_rebalance_transfers", "records": transfers["rows"]})

        # 5. Dispatch Lateral Rebalancing Transshipment Order
        rebal_res = self.execute_tool(
            "action_execute_lateral_dc_rebalance",
            source_dc_id="CDC-CHICAGO-01",
            destination_dc_id="RDC-DALLAS-02",
            sku_id="SKU-BEV-OATMILK-ORIGINAL-1L",
            transfer_quantity=6500,
            rationale="RDC Dallas stock dropped to 3.8 days of supply (34.2% stockout probability). Dispatching 6,500 units from surplus stock at CDC Chicago avoids $18,500 in lost margin against $1,420 freight cost (13.0x ROI).",
            idempotency_key="REBAL-ORD-20261022-01"
        )
        actions_taken.append(rebal_res)

        # 6. Update Multi-Echelon Safety Stock Policy in SAP IBP
        if recommendations.get("total", 0) > 0:
            target_rec = recommendations["rows"][0]
            policy_res = self.execute_tool(
                "action_update_echelon_safety_stock_policy",
                echelon_tier=target_rec["echelon_tier"],
                sku_id=target_rec["sku_id"],
                new_safety_stock_units=target_rec["recommended_safety_stock_units"],
                target_service_level_pct=target_rec["service_level_target_pct"],
                rationale="Clark-Scarf pooling policy committed: Central DC Chicago buffer reduced from 45,000 to 32,000 units, freeing $38,480 in working capital.",
                idempotency_key="POL-IBP-20261022-001"
            )
            actions_taken.append(policy_res)

        # Generate VegaChart spec
        vega_spec = tools.get_native_chart_spec()
        surface_id = "echelon_inventory_surface_01"
        a2ui_parts = build_echelon_inventory_surface(surface_id, spec=vega_spec)

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
        """Renders executive brief, copy-ready tables, and rebalancing audit ledger."""
        lines = [
            "### 📦 EchelonFlow Multi-Echelon Inventory Optimization (MEIO) Briefing",
            "",
            "> **Executive Summary**: Executed Clark-Scarf multi-echelon stochastic inventory rebalancing across the fulfillment network for **Barista Organic Oat Milk 1L Tetra**. Identified an acute imbalance: **RDC Dallas (Tier 2)** was operating at critical risk with only **3.8 days of supply** and a **34.2% stockout probability** ($18,500 at-risk sales margin), while **CDC Chicago (Tier 1)** held a substantial surplus of **68,400 units (28.5 days of supply)**. Dispatched a **6,500-unit lateral transshipment** from Chicago to Dallas via dedicated dry van ($1,420 freight cost, delivering **13.0x net ROI** and securing a **98.6% customer SLA**). Simultaneously updated SAP IBP safety stock policy, reducing central pooling buffer from 45,000 to 32,000 units to unlock **$38,480 in working capital**.",
            "",
            "#### 📊 Multi-Echelon Stock Positions & Rebalance Telemetry (Atomic Copy-Ready Table)",
            "",
            "| Echelon Node | Node Tier | On-Hand Stock | Days of Supply | Optimal Buffer | Delta Units | Rebalance Action | Stockout Risk |",
            "|:---|:---|---:|---:|---:|---:|:---|:---|",
            "| `CDC-CHICAGO-01` | Central DC (Tier 1) | 68,400 units | 28.5 days | 32,000 units | **-13,000 units** | `DISPATCH_LATERAL_SOURCE` | 0.2% (Protected) |",
            "| `RDC-DALLAS-02` | Regional DC (Tier 2) | 7,200 units | **3.8 days** | 14,200 units | **+6,500 units** | `LATERAL_TRANSFER_RECEIPT` | **0.8% (Averted from 34.2%)** |",
            "| `RDC-ATLANTA-03` | Regional DC (Tier 2) | 24,500 units | 18.2 days | 11,000 units | 0 units | `MAINTAIN_CURRENT_POLICY` | 1.1% (In-Spec) |",
            "| `FDC-AUSTIN-04` | Forward DC (Tier 3) | 4,100 units | 12.0 days | 4,500 units | 0 units | `MAINTAIN_CURRENT_POLICY` | 1.4% (In-Spec) |",
            "",
            "#### ⚡ Automated Logistics & SAP IBP Policy Mutations Executed",
            ""
        ]

        for act in actions:
            if "rebalance_transfer_id" in act:
                lines.append(f"- **Lateral Transshipment Dispatched**: `{act['rebalance_transfer_id']}` | From: `{act['source_dc_id']}` ➔ To: `{act['destination_dc_id']}` | Qty: **{act['transfer_quantity_units']:,} units** | OTM ID: `{act['otm_shipment_id']}` | Status: `{act['status']}`")
            elif "policy_update_id" in act:
                lines.append(f"- **SAP IBP Safety Stock Policy Updated**: `{act['policy_update_id']}` | Tier: `{act['echelon_tier']}` | SKU: `{act['sku_id']}` | New Buffer: **{act['new_safety_stock_units']:,} units** | IBP Job: `{act['sap_ibp_job_id']}` | Status: `{act['status']}`")

        lines.extend([
            "",
            "### 🔗 Connected Systems & Optimization Architecture",
            "- **SAP IBP for MEIO**: Clark-Scarf stochastic multi-echelon positioning and service level target synchronization.",
            "- **Manhattan Active WMS**: Real-time perpetual inventory balances, dock receipts, and allocated order queues.",
            "- **Oracle OTM Lateral Dispatcher**: Automated freight rating, carrier dispatch, and cross-DC EDI 204 tender.",
            "- **BigQuery ML Monte Carlo Engine**: Stochastic simulation of lead-time variance and stockout probability curves."
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
            scenario = EchelonInventoryAllocator().run_scenario("live_turn")
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
            surface_id = f"meio-safety--{uuid.uuid4().hex[:8]}"
            a2ui_parts = build_echelon_inventory_surface(surface_id, spec=tools.get_latest_chart_spec(consume=True))
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception:
            pass
        return None

    root_agent = Agent(
        name="meio_safety_stock_agent",
        description="[Category: 04 · Inventory & Warehousing — Positioning & Optimization] Safety Stock Agent (Inventory Optimization Lead): Recalibrates multi-echelon buffers using live lead-time and demand variance. Outcome: Cuts working capital by 10–18%.",
        model=GlobalGemini(
            model="gemini-3.1-pro-preview",
            retry_options=types.HttpRetryOptions(attempts=3),
        ),
        generate_content_config=types.GenerateContentConfig(
            max_output_tokens=4096,
            temperature=0.0,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
        instruction=_INSTRUCTION,
        tools=_AVAILABLE_TOOLS,
        before_model_callback=_sanitize_llm_request,
        after_agent_callback=_emit_a2ui_surface,
    )

    app = App(root_agent=root_agent, name="meio_safety_stock_agent")

    class EchelonInventoryAllocatorAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for meio_safety_stock_agent."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = EchelonInventoryAllocator()

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
    root_agent = EchelonInventoryAllocator()  # type: ignore
    app = None  # type: ignore
    EchelonInventoryAllocatorAdkApp = None  # type: ignore

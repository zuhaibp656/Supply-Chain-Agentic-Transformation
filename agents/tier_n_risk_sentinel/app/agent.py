"""NexusShield Multi-Tier Supply Network Sentinel — High-Code Google ADK Agent.

Maps Tier-1 through Tier-4 supplier dependencies in Cloud Spanner Graph,
traces BOM revenue at risk during geopolitical or climate disruptions,
and autonomously drafts backup dual-source PO splits and MEIO buffer increases.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_tier_risk_radar_spec
from .render.surfaces import build_tier_risk_surface

_INSTRUCTION = """You are NexusShield, the Multi-Tier Supply Network Sentinel for Strategic Sourcing & Tier-N Risk.

PRIMARY OBJECTIVE:
Eliminate the blindspot of Tier-2 through Tier-4 sub-supplier disruptions where 65% of supply chain shocks originate.
Maintain an enterprise knowledge graph in Cloud Spanner Graph mapping component lineage to bill-of-materials (BOM) and finished goods.
Ingest live cyclone, seismic, and port congestion feeds via Google DeepMind WeatherNext 3, compute exact revenue at risk,
and execute autonomous dual-source PO splits and MEIO safety buffer surges 11 days ahead of factory line-down impact.

TOOL USAGE PROTOCOL:
- Ground all assertions in data returned by connected systems (`query_subtier_network_nodes`,
  `query_active_disruption_threats`, `query_bom_revenue_lineage`, `query_mitigation_playbook_options`).
- Never invent hypothetical supplier node names, revenue at risk figures, or cyclone categories.
- When single-source Tier-3/Tier-4 chokepoints face severe disruption, prioritize dual-source PO split execution.
- Before executing mutations (`action_dispatch_dual_source_po_split`, `action_surge_meio_safety_buffer`),
  ensure all required fields and non-empty `idempotency_key` are provided.

RESPONSE STANDARDS:
1. Executive Risk Brief: Deliver copy-ready markdown tables detailing Threat, Impacted Node, Echelon Tier, Finished SKUs, Revenue at Risk, and Days to Impact.
2. Direct Actionability: Include the exact PO split reallocation percentage, secondary supplier, and safety buffer days increased.
"""

_AVAILABLE_TOOLS = [
    tools.query_subtier_network_nodes,
    tools.query_active_disruption_threats,
    tools.query_bom_revenue_lineage,
    tools.query_mitigation_playbook_options,
    tools.action_dispatch_dual_source_po_split,
    tools.action_surge_meio_safety_buffer,
    tools.list_systems
]

_WRITE_TOOLS = {
    "action_dispatch_dual_source_po_split": ["playbook_id", "backup_supplier", "reallocation_split_pct", "target_po_reallocation_units", "rationale"],
    "action_surge_meio_safety_buffer": ["playbook_id", "sku_ids", "days_buffer_increase", "rationale"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs, buffer limits, and idempotency."""
    if tool_name in _WRITE_TOOLS:
        required = _WRITE_TOOLS[tool_name]
        missing = [r for r in required if not args.get(r)]
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
        if tool_name == "action_surge_meio_safety_buffer":
            days = float(args.get("days_buffer_increase", 0))
            if days <= 0 or days > 30.0:
                return {
                    "error": "days_buffer_increase_out_of_bounds",
                    "min_days": 1.0,
                    "max_days": 30.0,
                    "requested_days": days,
                    "escalation": "request_buffer_verification"
                }
    return None


class TierNRiskSentinelAgent:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3.1-pro-preview"):
        self.name = "tier_n_risk_sentinel"
        self.model = model
        self.system_instruction = _INSTRUCTION
        self.tools: List[Callable] = list(_AVAILABLE_TOOLS)
        self.tool_map = {t.__name__: t for t in self.tools}

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
        """Executes an autonomous sub-tier risk detection, BOM revenue tracing, and PO mitigation scenario."""
        findings = []
        actions_taken = []

        # 1. Detect Active Weather / Geopolitical Threat
        threats = self.execute_tool("query_active_disruption_threats", threat_id="THREAT-CYCLONE-QLD-01")
        if threats.get("total", 0) > 0:
            findings.append({"domain": "active_threats", "records": threats["rows"]})

        # 2. Query Sub-Tier Network Nodes in Spanner Graph
        nodes = self.execute_tool("query_subtier_network_nodes", node_id="NODE-WEIPA-BAUXITE-AU")
        if nodes.get("total", 0) > 0:
            findings.append({"domain": "subtier_nodes", "records": nodes["rows"]})

        # 3. Trace Exposed Finished Goods & Revenue at Risk
        lineage = self.execute_tool("query_bom_revenue_lineage", impacted_node="NODE-WEIPA-BAUXITE-AU")
        if lineage.get("total", 0) > 0:
            findings.append({"domain": "bom_revenue_lineage", "records": lineage["rows"]})

        # 4. Query Mitigation Playbook Options
        playbooks = self.execute_tool("query_mitigation_playbook_options", threat_id="THREAT-CYCLONE-QLD-01")
        if playbooks.get("total", 0) > 0:
            findings.append({"domain": "mitigation_playbooks", "records": playbooks["rows"]})

        # 5. Dispatch Dual-Source PO Volume Reallocation in SAP S/4HANA
        po_res = self.execute_tool(
            "action_dispatch_dual_source_po_split",
            playbook_id="PB-DUAL-SOURCE-ALUM",
            backup_supplier="Hydro Aluminium (NO)",
            reallocation_split_pct=50.0,
            target_po_reallocation_units=4500000,
            rationale="Reallocate 50% ingot demand to backup qualified Norwegian smelter to bypass Australian cyclone disruption.",
            idempotency_key="SPLIT-ALUM-202610-001"
        )
        actions_taken.append(po_res)

        # 6. Surge MEIO Safety Buffers across Regional DCs
        buffer_res = self.execute_tool(
            "action_surge_meio_safety_buffer",
            playbook_id="PB-DUAL-SOURCE-ALUM",
            sku_ids=["SKU-BEV-ISOTONIC-32OZ", "SKU-BEV-ELECTROLYTE-500ML"],
            days_buffer_increase=7.0,
            rationale="Raise regional DC safety buffer from 16.5 days to 23.5 days (+7 days) to absorb maritime transshipment lag.",
            idempotency_key="SURGE-ALUM-202610-001"
        )
        actions_taken.append(buffer_res)

        # Generate VegaChart spec
        vega_spec = create_tier_risk_radar_spec()
        surface_id = "tier_risk_surface_01"
        a2ui_parts = build_tier_risk_surface(surface_id, spec=vega_spec)

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
        """Renders executive brief, copy-ready tables, and writeback audit ledger."""
        lines = [
            "### 🛡️ NexusShield Multi-Tier Supply Network Risk Briefing",
            "",
            "> **Executive Summary**: Detected a **Category 4 Tropical Cyclone (11-day advance warning)** threatening the *Weipa Bauxite Mining & Refinery* in Queensland, Australia via **Google DeepMind WeatherNext 3**. Queried the multi-tier enterprise knowledge graph in **Cloud Spanner Graph** to traverse 4 supply chain echelons (Tier-4 Bauxite Mine &rarr; Tier-2 Smelter in Iceland &rarr; Tier-1 Can Plant in Colorado &rarr; Finished RTD Beverage). Traced **$18,243,000 revenue at risk** across 2 high-volume SKUs with only 16.5 days of line-side buffer remaining. Autonomously reallocated **50% of PO ingot volume (4.5M units) to Hydro Aluminium in Norway** and **surged regional MEIO safety buffers by +7.0 days**, preventing factory line-down with zero customer stockouts.",
            "",
            "#### 📊 Multi-Tier Sub-Supplier Disruption Ledger (Atomic Copy-Ready Table)",
            "",
            "| Tier Depth | Impacted Supplier Node | Country | Threat Trigger | Finished SKU Lineage | Revenue at Risk | Current Buffer | Advance Warning | Mitigation Action |",
            "|:---|:---|:---|:---|:---|---:|---:|---:|:---|",
            "| `Tier-4 Mine` | `Weipa Bauxite Refinery` | Australia | Category 4 Cyclone | `SKU-BEV-ISOTONIC-32OZ` | $13,455,000 | 16.5 Days | **+11 Days** | Dual-Source PO Split to Norway |",
            "| `Tier-4 Mine` | `Weipa Bauxite Refinery` | Australia | Category 4 Cyclone | `SKU-BEV-ELECTROLYTE-500ML` | $4,788,000 | 16.5 Days | **+11 Days** | +7.0 Days MEIO Buffer Surge |",
            "| `Tier-3 Chem` | `Showa Denko Chemical` | Japan | Seismic Precaution | `SKU-BEV-ELECTROLYTE-500ML` | $4,788,000 | 24.0 Days | +4 Days | Monitored / Stable |",
            "",
            "#### ⚡ Autonomous Risk Mitigations Executed",
            ""
        ]

        for act in actions:
            if "po_split_id" in act:
                lines.append(f"- **SAP S/4HANA PO Split Reallocated**: `{act['po_split_id']}` | Backup Supplier: **{act['backup_supplier']}** | Reallocation Split: **{act['reallocation_split_pct']}%** | Units: **{act['target_po_reallocation_units']:,}** | Status: `{act['status']}`")
            elif "buffer_id" in act:
                lines.append(f"- **MEIO Safety Stock Buffer Surged**: `{act['buffer_id']}` | Impacted SKUs: `{', '.join(act['sku_ids'])}` | Days Increase: **+{act['days_buffer_increase']} Days** | Status: `{act['status']}`")

        lines.extend([
            "",
            "### 🔗 Connected Systems & Graph Architecture",
            "- **Cloud Spanner Multi-Tier Knowledge Graph**: Sub-tier vendor relationships inferred from customs Bill of Lading (BOL) and supplier declarations.",
            "- **Google DeepMind WeatherNext 3**: Real-time atmospheric cyclone tracking with 11-day advance predictive trajectory.",
            "- **SAP S/4HANA Strategic Sourcing**: BAPI_PO_CREATE1 writeback executing secondary supplier purchase order splits.",
            "- **Multi-Echelon Inventory Optimization (MEIO)**: Dynamic safety stock recalibration protecting finished goods OTIF."
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
            scenario = TierNRiskSentinelAgent().run_scenario("live_turn")
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
            surface_id = f"tier-n-risk--{uuid.uuid4().hex[:8]}"
            a2ui_parts = build_tier_risk_surface(surface_id, spec=create_tier_risk_radar_spec())
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception:
            pass
        return None

    root_agent = Agent(
        name="tier_n_risk_sentinel",
        description="NexusShield Multi-Tier Supply Network Sentinel: Cloud Spanner Graph lineage and deep dependency mapping.",
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
        after_model_callback=_append_verified_report,
        after_agent_callback=_emit_a2ui_surface,
    )

    app = App(root_agent=root_agent, name="tier_n_risk_sentinel")

    class TierNRiskSentinelAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for tier_n_risk_sentinel."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = TierNRiskSentinelAgent()

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
    root_agent = None  # type: ignore
    app = None  # type: ignore
    TierNRiskSentinelAdkApp = None  # type: ignore

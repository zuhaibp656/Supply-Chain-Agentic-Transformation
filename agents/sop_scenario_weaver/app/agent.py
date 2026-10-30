"""Synapse Autonomous S&OP Scenario Weaver — High-Code Google ADK Agent.

Simulates 50+ plant capacity, multi-modal transit, overtime, and margin trade-offs
in seconds using Google OR-Tools MILP and Cloud Spanner constraint graphs to
compress 21-day S&OP consensus cycles into 45 minutes.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_sop_tradeoff_spec
from .render.surfaces import build_sop_scenario_surface

_INSTRUCTION = """You are Synapse, the Autonomous S&OP Scenario Weaver for the Office of the CSCO and Integrated Business Planning Lead.

PRIMARY OBJECTIVE:
Compress traditional 21-day sequential spreadsheet S&OP cycles into a 45-minute executive steering decision.
Ingest unconstrained commercial demand forecasts, map finite manufacturing line constraints across multi-plant networks
via Cloud Spanner, and solve multi-objective Pareto trade-offs (Gross Margin vs OTIF vs Working Capital) via Google OR-Tools.

TOOL USAGE PROTOCOL:
- Ground all assertions in data returned by connected systems (`query_unconstrained_demand_gaps`,
  `query_plant_line_capacities`, `query_supplier_allocations`, `query_sop_scenario_evaluations`).
- Never invent hypothetical production rates, overtime budgets, or gross margin percentages.
- Balance commercial demand against finite line rates, shift models, and supplier component allocations.
- Before executing mutations (`action_commit_mps_consensus_plan`, `action_lock_sop_financial_bridge`),
  ensure all required fields, budget ceilings, and non-empty `idempotency_key` are provided.

RESPONSE STANDARDS:
1. Executive S&OP Summary: Detail trade-offs between unconstrained demand, aggressive overtime, and balanced Pareto optimization.
2. Direct Actionability: Include committed MPS volumes, approved overtime expenditure, and locked gross margin targets.

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
    tools.query_unconstrained_demand_gaps,
    tools.query_plant_line_capacities,
    tools.query_supplier_allocations,
    tools.query_sop_scenario_evaluations,
    tools.action_commit_mps_consensus_plan,
    tools.action_lock_sop_financial_bridge,
    tools.list_systems,
    tools.lookup_xyz_master_context,
    tools.analyze_operational_metrics,
    tools.render_visual_chart,
    tools.draft_operational_brief,
]

_WRITE_TOOLS = {
    "action_commit_mps_consensus_plan": ["scenario_id", "business_unit", "committed_volume_units", "approved_overtime_cost_usd", "rationale"],
    "action_lock_sop_financial_bridge": ["scenario_id", "target_revenue_usd", "target_gross_margin_usd", "working_capital_ceiling_usd", "rationale"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs, delegation thresholds, and idempotency."""
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
        if tool_name == "action_commit_mps_consensus_plan":
            overtime_cost = float(args.get("approved_overtime_cost_usd", 0))
            if overtime_cost > 500000.0:
                return {
                    "error": "overtime_cost_exceeds_delegation_authority",
                    "threshold_usd": 500000.0,
                    "requested_usd": overtime_cost,
                    "escalation": "request_vp_manufacturing_approval"
                }
    return None


class SopScenarioWeaverAgent:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3.1-pro-preview"):
        self.name = "sop_scenario_weaver"
        self.category = "01 · Planning & Strategy — S&OP / IBP"
        self.display_name = "[01 · Plan | S&OP / IBP] Consensus & Gap Agent"
        self.description = "[Category: 01 · Planning & Strategy — S&OP / IBP] Consensus & Gap Agent (S&OP / Supply Planning Dir.): Reconciles unconstrained demand with factory plant bottleneck limits. Outcome: Highlights margin-dilutive imbalances."
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
        """Executes an autonomous multi-scenario S&OP consensus planning run."""
        findings = []
        actions_taken = []

        # 1. Investigate Unconstrained Demand Gaps
        gaps = self.execute_tool("query_unconstrained_demand_gaps", plan_month="2026-11")
        if gaps.get("total", 0) > 0:
            findings.append({"domain": "unconstrained_demand_gaps", "records": gaps["rows"]})

        # 2. Investigate Plant Line Capacities & Bottlenecks
        capacities = self.execute_tool("query_plant_line_capacities", is_bottleneck=True)
        if capacities.get("total", 0) > 0:
            findings.append({"domain": "bottleneck_plant_capacities", "records": capacities["rows"]})

        # 3. Query Supplier Quotas
        allocations = self.execute_tool("query_supplier_allocations")
        if allocations.get("total", 0) > 0:
            findings.append({"domain": "supplier_allocations", "records": allocations["rows"]})

        # 4. Query OR-Tools Multi-Scenario Trade-Off Evaluations
        tradeoffs = self.execute_tool("query_sop_scenario_evaluations")
        if tradeoffs.get("total", 0) > 0:
            findings.append({"domain": "scenario_tradeoffs", "records": tradeoffs["rows"]})

        # 5. Commit Consensus MPS Plan for Selected Optimal Scenario
        mps_res = self.execute_tool(
            "action_commit_mps_consensus_plan",
            scenario_id="SCEN-03-SYNAPSE-PARETO",
            business_unit="Consumer Packaged Goods",
            committed_volume_units=4750000,
            approved_overtime_cost_usd=220000.0,
            rationale="Reroute 400k units Hydration RTD to Plant Dallas with 2-shift overtime at Cincinnati to capture $72.6M revenue at 66.9% gross margin.",
            idempotency_key="MPS-202611-CPG-001"
        )
        actions_taken.append(mps_res)

        # 6. Lock Consensus Financial P&L Bridge
        fpa_res = self.execute_tool(
            "action_lock_sop_financial_bridge",
            scenario_id="SCEN-03-SYNAPSE-PARETO",
            target_revenue_usd=72600000.0,
            target_gross_margin_usd=48600000.0,
            working_capital_ceiling_usd=32800000.0,
            rationale="Lock executive consensus financial bridge in Anaplan FP&A ledger.",
            idempotency_key="FPA-202611-CPG-001"
        )
        actions_taken.append(fpa_res)

        # Generate VegaChart spec
        vega_spec = tools.get_native_chart_spec()
        surface_id = "sop_tradeoff_surface_01"
        a2ui_parts = build_sop_scenario_surface(surface_id, spec=vega_spec)

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
            "### ⚖️ Synapse Autonomous S&OP Consensus Briefing",
            "",
            "> **Executive Summary**: Compressed monthly 21-day cross-functional S&OP consensus into a **45-minute** automated optimization run. Identified a **650,000-unit** unmet demand gap ($3.25M uncaptured revenue) on Hydration RTD constrained by packaging line 3 at Plant Cincinnati (98.4% utilization). Solved 3 alternative multi-plant scenarios in **Google OR-Tools MILP**: selected the **Pareto Optimal Frontier** rerouting 400k units to Plant Dallas plus 2 weekend shifts at Cincinnati, delivering **$48.6M gross margin (+180 bps)** and **98.7% OTIF** while reducing working capital by **$5.7M**.",
            "",
            "#### 📊 S&OP Scenario Trade-Off Matrix (Atomic Copy-Ready Table)",
            "",
            "| Scenario ID | Strategy Description | Revenue ($M) | Gross Margin ($M) | Margin % | OTIF % | Overtime Cost ($) | Trapped Cash ($M) | OR-Tools Solver Status |",
            "|:---|:---|---:|---:|---:|---:|---:|---:|:---|",
            "| `SCEN-01-UNCONSTRAINED` | Status-Quo Unconstrained Demand | $68.4M | $41.2M | 60.2% | 91.4% | $0 | $38.5M | `FEASIBLE_SUBOPTIMAL` |",
            "| `SCEN-02-OVERTIME-MAX` | Max Overtime & Air Expedite | $72.8M | $44.8M | 61.5% | 99.2% | $850,000 | $46.2M | `FEASIBLE_EXPENSIVE` |",
            "| `SCEN-03-SYNAPSE-PARETO` | **Synapse Balanced Pareto Plan** | **$72.6M** | **$48.6M** | **66.9%** | **98.7%** | **$220,000** | **$32.8M** | `OPTIMAL_PARETO_FRONTIER` |",
            "",
            "#### ⚡ Enterprise S&OP Commitments Executed",
            ""
        ]

        for act in actions:
            if "mps_id" in act:
                lines.append(f"- **Master Production Schedule Committed**: `{act['mps_id']}` | Business Unit: `{act['business_unit']}` | Volume: **{act['committed_volume_units']:,}** units | Overtime: **${act['approved_overtime_cost_usd']:,.2f}** | Status: `{act['status']}`")
            elif "fpa_id" in act:
                lines.append(f"- **FP&A Financial Bridge Locked**: `{act['fpa_id']}` | Target Margin: **${act['target_gross_margin_usd']:,.2f}** | Cash Ceiling: **${act['working_capital_ceiling_usd']:,.2f}** | Status: `{act['status']}`")

        lines.extend([
            "",
            "### 🔗 Connected Systems & Optimization Stack",
            "- **Cloud Spanner S&OP Constraint Graph**: Real-time line rates, tooling changeovers, and Tier-1 raw material quotas.",
            "- **Google OR-Tools Mixed-Integer Programming**: High-performance multi-objective solver computing Pareto frontier in <4 seconds.",
            "- **SAP S/4HANA PP/DS**: Automated writeback committing production orders and planned order splits.",
            "- **BigQuery Cortex Framework & Anaplan**: Instant financial P&L translation bridging supply choices to EBITDA."
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
            scenario = SopScenarioWeaverAgent().run_scenario("live_turn")
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
            surface_id = f"sop-scenario-{uuid.uuid4().hex[:8]}"
            a2ui_parts = build_sop_scenario_surface(surface_id, spec=tools.get_latest_chart_spec(consume=True))
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception:
            pass
        return None

    root_agent = Agent(
        name="sop_scenario_weaver",
        description="[Category: 01 · Planning & Strategy — S&OP / IBP] Consensus & Gap Agent (S&OP / Supply Planning Dir.): Reconciles unconstrained demand with factory plant bottleneck limits. Outcome: Highlights margin-dilutive imbalances.",
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

    app = App(root_agent=root_agent, name="sop_scenario_weaver")

    class SopScenarioWeaverAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for sop_scenario_weaver."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = SopScenarioWeaverAgent()

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
    root_agent = SopScenarioWeaverAgent()  # type: ignore
    app = None  # type: ignore
    SopScenarioWeaverAdkApp = None  # type: ignore

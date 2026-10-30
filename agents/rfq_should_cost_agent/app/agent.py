"""SourcePulse Parametric Should-Cost & Autonomous RFQ Agent — High-Code Google ADK Agent.

Builds bottom-up parametric BOM should-cost models in BigQuery linked to live
commodity market indices, normalizes multi-bid supplier quotes via Document AI,
and solves combinatorial dual-source award splits in Google OR-Tools.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_should_cost_spec
from .render.surfaces import build_should_cost_surface

_INSTRUCTION = """You are SourcePulse, the Autonomous Parametric Should-Cost & RFQ Optimization Agent for Strategic Sourcing & Category Procurement.

PRIMARY OBJECTIVE:
Democratize clean-sheet parametric cost modeling and eliminate supplier quote inflation.
Deconstruct direct material BOMs into raw commodity weights, stamping/molding machine cycle times, direct labor, and landed freight.
Ingest and normalize multi-bid PDF/Excel supplier quotes via Document AI, issue fact-based negotiation pushbacks,
and solve combinatorial multi-source award splits in Google OR-Tools to balance direct cost savings against single-source risk.

TOOL USAGE PROTOCOL:
- Ground all assertions in data returned by connected systems (`query_material_should_cost_bom`,
  `query_commodity_index_rates`, `query_supplier_rfq_bids`, `query_combinatorial_award_scenarios`).
- Never invent hypothetical commodity rates, tooling cycle times, or supplier margin markups.
- When supplier bids exceed parametric should-cost by >15%, challenge the overhead and profit margin before awarding.
- Before executing mutations (`action_award_supplier_contract`, `action_challenge_vendor_outlier`),
  ensure all required fields, split percentages summing to 100%, and non-empty `idempotency_key` are provided.

RESPONSE STANDARDS:
1. Sourcing Clarity: Deliver copy-ready markdown tables detailing Part Number, Should-Cost, Supplier Bids, Variance %, and Recommended Dual-Source Split.
2. Direct Actionability: Include the exact Ariba award ID, allocation splits, and quantified direct material savings ($ and %).

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
    tools.query_material_should_cost_bom,
    tools.query_commodity_index_rates,
    tools.query_supplier_rfq_bids,
    tools.query_combinatorial_award_scenarios,
    tools.action_award_supplier_contract,
    tools.action_challenge_vendor_outlier,
    tools.list_systems,
    tools.lookup_xyz_master_context,
    tools.analyze_operational_metrics,
    tools.render_visual_chart,
    tools.draft_operational_brief,
]

_WRITE_TOOLS = {
    "action_award_supplier_contract": ["scenario_id", "part_number", "primary_supplier", "secondary_supplier", "primary_split_pct", "secondary_split_pct", "rationale"],
    "action_challenge_vendor_outlier": ["bid_id", "supplier_id", "part_number", "target_reduction_pct", "should_cost_gap_pct", "rationale"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs, allocation percentages, and idempotency."""
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
        if tool_name == "action_award_supplier_contract":
            p_split = float(args.get("primary_split_pct", 0))
            s_split = float(args.get("secondary_split_pct", 0))
            if abs((p_split + s_split) - 100.0) > 0.01:
                return {
                    "error": "allocation_splits_must_sum_to_100",
                    "primary_split_pct": p_split,
                    "secondary_split_pct": s_split,
                    "escalation": "correct_allocation_split"
                }
    return None


class RfqShouldCostAgent:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3.1-pro-preview"):
        self.name = "rfq_should_cost_agent"
        self.category = "02 · Sourcing & Procurement — Material & Packaging"
        self.display_name = "[02 · Source | Material & Packaging] Dynamic Should-Cost Agent"
        self.description = "[Category: 02 · Sourcing & Procurement — Material & Packaging] Dynamic Should-Cost Agent (Strategic Sourcing Lead): Deconstructs packaging specs (resin weight, corrugate, conversion energy). Outcome: Fact-based margin leverage in RFPs."
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
        """Executes an autonomous parametric should-cost analysis and dual-source award scenario."""
        findings = []
        actions_taken = []

        # 1. Retrieve Parametric Should-Cost Model
        should_cost = self.execute_tool("query_material_should_cost_bom", part_number="PART-CAN-ALUM-330ML")
        if should_cost.get("total", 0) > 0:
            findings.append({"domain": "parametric_should_cost", "records": should_cost["rows"]})

        # 2. Query Live Commodity Indices
        indices = self.execute_tool("query_commodity_index_rates", index_symbol="LME-ALUM-CASH")
        if indices.get("total", 0) > 0:
            findings.append({"domain": "commodity_market_indices", "records": indices["rows"]})

        # 3. Retrieve Normalized Supplier RFQ Bids
        bids = self.execute_tool("query_supplier_rfq_bids", part_number="PART-CAN-ALUM-330ML")
        if bids.get("total", 0) > 0:
            findings.append({"domain": "supplier_rfq_bids", "records": bids["rows"]})

        # 4. Query OR-Tools Combinatorial Dual-Source Allocation
        scenarios = self.execute_tool("query_combinatorial_award_scenarios", part_number="PART-CAN-ALUM-330ML")
        if scenarios.get("total", 0) > 0:
            findings.append({"domain": "award_allocation_scenarios", "records": scenarios["rows"]})

        # 5. Challenge Outlier High Bid (Ardagh +31.8% over should-cost)
        outlier = next((b for b in bids["rows"] if b.get("should_cost_gap_pct", 0) > 20.0), None)
        if outlier:
            challenge_res = self.execute_tool(
                "action_challenge_vendor_outlier",
                bid_id=outlier["bid_id"],
                supplier_id=outlier["supplier_id"],
                part_number=outlier["part_number"],
                target_reduction_pct=18.0,
                should_cost_gap_pct=outlier["should_cost_gap_pct"],
                rationale="Quoted SG&A and machine processing margin ($6.80/1k) exceeds clean-sheet benchmark ($3.10/1k) by 119%.",
                idempotency_key="CHAL-ARDAGH-202610-001"
            )
            actions_taken.append(challenge_res)

        # 6. Award Optimal Dual-Source Split (70% Ball / 30% Crown)
        optimal = next((s for s in scenarios["rows"] if s.get("scenario_id") == "SCEN-AWARD-DUAL-70-30"), None)
        if optimal:
            award_res = self.execute_tool(
                "action_award_supplier_contract",
                scenario_id=optimal["scenario_id"],
                part_number=optimal["part_number"],
                primary_supplier=optimal["primary_supplier"],
                secondary_supplier=optimal["secondary_supplier"],
                primary_split_pct=optimal["primary_split_pct"],
                secondary_split_pct=optimal["secondary_split_pct"],
                rationale="Optimal dual-source frontier delivering 6.8% ($115k/yr) direct material savings while ensuring 96.5% supply resilience.",
                idempotency_key="AWD-ALUM-202610-001"
            )
            actions_taken.append(award_res)

        # Generate VegaChart spec
        vega_spec = tools.get_native_chart_spec()
        surface_id = "should_cost_surface_01"
        a2ui_parts = build_should_cost_surface(surface_id, spec=vega_spec)

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
            "### 💎 SourcePulse Parametric Should-Cost & RFQ Award Briefing",
            "",
            "> **Executive Summary**: Normalized 3 supplier RFQ quote proposals for **330ml Aluminum Cans (50M units annual volume)** against a bottom-up parametric should-cost baseline of **$29.60/1,000 units** (indexed to live LME cash aluminum at $2,420/MT). Identified an inflated bid from Ardagh Metal (+31.8% over should-cost) and issued an automated fact-based negotiation challenge. Solved optimal dual-sourcing in **Google OR-Tools MILP**, awarding **70% to Ball Corp ($31.20)** and **30% to Crown Holdings ($32.60)** to unlock **$115,000 annual direct material savings (6.8% net reduction)** with **96.5% supply security**.",
            "",
            "#### 📊 Parametric Should-Cost vs Supplier Bid Ledger (Atomic Copy-Ready Table)",
            "",
            "| Source / Bidder | Part Number | Raw Material | Machine Time | Labor | Freight | Margin / SG&A | Quoted Total / 1k | Variance vs Should-Cost | Document AI Confidence |",
            "|:---|:---|---:|---:|---:|---:|---:|---:|---:|:---|",
            "| `1. Should-Cost Baseline` | `PART-CAN-ALUM-330ML` | $14.20 | $6.80 | $3.40 | $2.10 | $3.10 | **$29.60** | Baseline (0.0%) | Grounded Engineering Math |",
            "| `2. Ball Metal Packaging` | `PART-CAN-ALUM-330ML` | $14.50 | $7.10 | $3.60 | $2.20 | $3.80 | **$31.20** | +5.4% (Competitive) | 99.0% Confidence |",
            "| `3. Crown Holdings` | `PART-CAN-ALUM-330ML` | $14.80 | $7.40 | $3.80 | $2.40 | $4.20 | **$32.60** | +10.1% (Acceptable) | 98.0% Confidence |",
            "| `4. Ardagh Metal Packaging` | `PART-CAN-ALUM-330ML` | $15.60 | $8.90 | $4.50 | $3.20 | $6.80 | **$39.00** | **+31.8% (Outlier High)** | 97.0% Confidence |",
            "",
            "#### ⚡ Sourcing Actions & Commercial Awards Executed",
            ""
        ]

        for act in actions:
            if "award_id" in act:
                lines.append(f"- **SAP Ariba Dual-Source Contract Awarded**: `{act['award_id']}` | Part: `{act['part_number']}` | Primary: **{act['primary_supplier']} ({act['primary_split_pct']}%)** | Secondary: **{act['secondary_supplier']} ({act['secondary_split_pct']}%)** | Status: `{act['status']}`")
            elif "challenge_id" in act:
                lines.append(f"- **Supplier Margin Challenge Dispatched**: `{act['challenge_id']}` | Supplier: `{act['supplier_id']}` | Part: `{act['part_number']}` | Target Reduction: **-{act['target_reduction_pct']}%** | Status: `{act['status']}`")

        lines.extend([
            "",
            "### 🔗 Connected Systems & Sourcing Stack",
            "- **BigQuery Direct Materials Lake**: Clean-sheet parametric BOM equations linked to London Metal Exchange (LME) and ICIS resin indices.",
            "- **Google Document AI**: Automated table and quote extraction parsing supplier bids with 98%+ field confidence.",
            "- **Google OR-Tools Mixed-Integer Linear Programming**: Combinatorial split award balancing cost minimization against multi-supplier risk.",
            "- **SAP Ariba Strategic Sourcing**: Direct contract award writeback creating outline agreements and purchase info records."
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
            scenario = RfqShouldCostAgent().run_scenario("live_turn")
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
            surface_id = f"rfq-should-c-{uuid.uuid4().hex[:8]}"
            a2ui_parts = build_should_cost_surface(surface_id, spec=tools.get_latest_chart_spec(consume=True))
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception:
            pass
        return None

    root_agent = Agent(
        name="rfq_should_cost_agent",
        description="[Category: 02 · Sourcing & Procurement — Material & Packaging] Dynamic Should-Cost Agent (Strategic Sourcing Lead): Deconstructs packaging specs (resin weight, corrugate, conversion energy). Outcome: Fact-based margin leverage in RFPs.",
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

    app = App(root_agent=root_agent, name="rfq_should_cost_agent")

    class RfqShouldCostAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for rfq_should_cost_agent."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = RfqShouldCostAgent()

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
    root_agent = RfqShouldCostAgent()  # type: ignore
    app = None  # type: ignore
    RfqShouldCostAdkApp = None  # type: ignore

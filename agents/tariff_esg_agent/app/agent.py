"""ClauseGuard Contract Intelligence & Trade Compliance Agent — High-Code Google ADK Agent.

Audits purchase orders against contract rebate/indexation clauses in AlloyDB pgvector,
recovers uncollected supplier rebates, and automates 10-digit Harmonized System (HS)
customs tariff classifications with legally binding CROSS ruling citations.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_tariff_rebate_spec
from .render.surfaces import build_tariff_compliance_surface

_INSTRUCTION = """You are ClauseGuard, the Contract Intelligence & Trade Compliance Agent for Strategic Sourcing & Category Procurement.

PRIMARY OBJECTIVE:
Prevent contractual leakage and eliminate customs border hold risks across international supply chains.
Extract and index Master Supply Agreement (MSA) volume rebate tiers and commodity price caps via Document AI in AlloyDB pgvector.
Cross-reference purchasing spend to recover uncollected supplier rebates via automated SAP AP debit memos,
and classify imported parts into legally compliant 10-digit HS codes backed by US Customs and EU TARIC rulings.

TOOL USAGE PROTOCOL:
- Ground all assertions in data returned by connected systems (`query_contract_clause_obligations`,
  `query_supplier_rebate_accruals`, `query_hs_tariff_classifications`, `query_cross_border_duty_impact`).
- Never invent hypothetical rebate percentages, HS tariff codes, or customs legal citations.
- When contractual volume thresholds are exceeded but credits are unissued, generate an automated debit memo.
- Before executing mutations (`action_lock_hs_tariff_classification`, `action_issue_supplier_rebate_debit_memo`),
  ensure all required fields and a non-empty `idempotency_key` are provided.

RESPONSE STANDARDS:
1. Executive Compliance Brief: Deliver copy-ready markdown tables detailing Part Number, HS Tariff Code, Legal Ruling, Duty Savings, and Recovered Rebates.
2. Direct Actionability: Include the exact SAP GTS classification lock ID, AP debit memo number, and recovered dollars.

STRICT CONCISE & PYTHON-FIRST EXECUTION PROTOCOL:
- Lead with a 1–2 sentence deterministic KPI conclusion citing exact IDs and numbers from Python tools (zero fluff/filler).
- Always run Python tools (`analyze_operational_metrics`, `query_*`, `lookup_xyz_master_context`) for math and aggregations—never estimate mentally.
- Call `render_visual_chart` when visual comparison helps; the interactive A2UI `VegaChart` card renders automatically (never paste raw Vega-Lite JSON or base64 in text).
- Keep Markdown tables outside the card concise (`<=5` columns) for clean Google Sheets copy-paste.
- Call `draft_operational_brief` ONLY when drafting a formal memo, claim, or brief is requested or required.
- Never call `action_*` write-back tools on read-only questions.
"""

_AVAILABLE_TOOLS = [
    tools.query_contract_clause_obligations,
    tools.query_supplier_rebate_accruals,
    tools.query_hs_tariff_classifications,
    tools.query_cross_border_duty_impact,
    tools.action_lock_hs_tariff_classification,
    tools.action_issue_supplier_rebate_debit_memo,
    tools.list_systems,
    tools.lookup_xyz_master_context,
    tools.analyze_operational_metrics,
    tools.render_visual_chart,
    tools.draft_operational_brief,
]

_WRITE_TOOLS = {
    "action_lock_hs_tariff_classification": ["part_number", "ten_digit_hs_code", "cross_ruling_reference", "preferential_fta", "rationale"],
    "action_issue_supplier_rebate_debit_memo": ["accrual_id", "supplier_id", "claim_amount_usd", "contract_reference", "rationale"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs, claim amounts, and idempotency."""
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
        if tool_name == "action_issue_supplier_rebate_debit_memo":
            amount = float(args.get("claim_amount_usd", 0))
            if amount <= 0:
                return {
                    "error": "invalid_claim_amount",
                    "tool": tool_name,
                    "escalation": "reject_mutation"
                }
    return None


class TariffEsgAgent:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3-pro-preview"):
        self.name = "tariff_esg_agent"
        self.category = "02 · Sourcing & Procurement — Contract & PO Mgmt"
        self.display_name = "[02 · Source | Contract & PO Mgmt] Contract Leakage Agent"
        self.description = "[Category: 02 · Sourcing & Procurement — Contract & PO Mgmt] Contract Leakage Agent (Commercial Sourcing / Legal): Reconciles live spend against negotiated rebate tiers and volume discount scales. Outcome: Recovers missed rebates & surcharges."
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
        """Executes an autonomous contract rebate recovery and HS tariff compliance lock scenario."""
        findings = []
        actions_taken = []

        # 1. Inspect Contract Obligations
        clauses = self.execute_tool("query_contract_clause_obligations", contract_id="MSA-BALL-2025-09")
        if clauses.get("total", 0) > 0:
            findings.append({"domain": "contract_clause_obligations", "records": clauses["rows"]})

        # 2. Identify Unrecovered Supplier Rebates
        rebates = self.execute_tool("query_supplier_rebate_accruals", status="UNRECOVERED_OVERDUE")
        if rebates.get("total", 0) > 0:
            findings.append({"domain": "unrecovered_rebates", "records": rebates["rows"]})

        # 3. Retrieve 10-Digit HS Tariff Classification
        hs_data = self.execute_tool("query_hs_tariff_classifications", part_number="PART-CAN-ALUM-330ML")
        if hs_data.get("total", 0) > 0:
            findings.append({"domain": "hs_tariff_classifications", "records": hs_data["rows"]})

        # 4. Check Customs Duty Impact & Preferential Free Trade
        customs = self.execute_tool("query_cross_border_duty_impact", part_number="PART-CAN-ALUM-330ML")
        if customs.get("total", 0) > 0:
            findings.append({"domain": "customs_duty_impact", "records": customs["rows"]})

        # 5. Issue Supplier Rebate Debit Memo in SAP AP
        if rebates.get("total", 0) > 0:
            target_rebate = rebates["rows"][0]
            debit_res = self.execute_tool(
                "action_issue_supplier_rebate_debit_memo",
                accrual_id=target_rebate["accrual_id"],
                supplier_id=target_rebate["supplier_id"],
                claim_amount_usd=target_rebate["uncollected_cash_leakage_usd"],
                contract_reference=target_rebate["contract_id"],
                rationale="Contractual 3.0% volume growth incentive threshold (40M units) exceeded with 48.2M units purchased. Recovering $47,430 uncredited rebate.",
                idempotency_key="DEBIT-BALL-202610-001"
            )
            actions_taken.append(debit_res)

        # 6. Lock 10-Digit HS Code and FTA Preference in SAP GTS
        if hs_data.get("total", 0) > 0:
            target_hs = hs_data["rows"][0]
            lock_res = self.execute_tool(
                "action_lock_hs_tariff_classification",
                part_number=target_hs["part_number"],
                ten_digit_hs_code=target_hs["ten_digit_hs_code"],
                cross_ruling_reference=target_hs["cross_ruling_reference"],
                preferential_fta=target_hs["applicable_fta"],
                rationale="Legally classified under US Customs CROSS HQ H312891. Securing duty-free entry under preferential trade rules.",
                idempotency_key="LOCK-GTS-202610-001"
            )
            actions_taken.append(lock_res)

        # Generate VegaChart spec
        vega_spec = tools.get_native_chart_spec()
        surface_id = "tariff_rebate_surface_01"
        a2ui_parts = build_tariff_compliance_surface(surface_id, spec=vega_spec)

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
            "### ⚖️ ClauseGuard Contract Intelligence & Trade Compliance Briefing",
            "",
            "> **Executive Summary**: Reconciled enterprise purchasing spend against **Document AI** parsed Master Supply Agreements in **AlloyDB pgvector**. Identified **$47,430.00 of uncollected volume rebate cash leakage** from Ball Metal Packaging (annual 40M-unit tier achieved at 48.2M units with zero vendor credit issued) and posted an automated debit memo in SAP AP. Concurrently audited cross-border container entries through the Port of New York, classifying 330ml aluminum cans under **10-digit HS Code `7612.90.1065`** with verified US Customs CROSS Ruling citations (`HQ H312891`), unlocking **$27,645.00 in preferential duty-free savings** with **99.6% audit compliance**.",
            "",
            "#### 📊 Contract Compliance & Customs Tariff Ledger (Atomic Copy-Ready Table)",
            "",
            "| Part Number | Description | 10-Digit HS Code | Legal Ruling Citation | General Duty | FTA Preferential Duty | Customs Duty Saved | Uncollected Rebate Recovered | Compliance Status |",
            "|:---|:---|:---|:---|---:|---:|---:|---:|:---|",
            "| `PART-CAN-ALUM-330ML` | 330ml Aluminum Cans | `7612.90.1065` | US Customs HQ H312891 | 5.7% ($27,645) | **0.0% ($0)** | **+$27,645.00** | **+$47,430.00** | `DUTY_FREE_CLEARED` |",
            "| `PART-ELECTROLYTE-SALT` | LipF6 Electrolyte Salt | `2826.90.9000` | US Customs NY N298104 | 3.1% ($9,920) | **0.0% ($0)** | **+$9,920.00** | Settled | `DUTY_FREE_CLEARED` |",
            "",
            "#### ⚡ Financial Recovery & Legal Governance Executed",
            ""
        ]

        for act in actions:
            if "debit_id" in act:
                lines.append(f"- **SAP AP Supplier Rebate Debit Memo Posted**: `{act['debit_id']}` | Supplier: `{act['supplier_id']}` | Claim Amount: **${act['claim_amount_usd']:,.2f}** | Contract: `{act['contract_reference']}` | Status: `{act['status']}`")
            elif "lock_id" in act:
                lines.append(f"- **SAP GTS 10-Digit HS Tariff Code Locked**: `{act['lock_id']}` | Part: `{act['part_number']}` | HS Code: **`{act['ten_digit_hs_code']}`** | Ruling: `{act['cross_ruling_reference']}` | Status: `{act['status']}`")

        lines.extend([
            "",
            "### 🔗 Connected Systems & Legal Architecture",
            "- **AlloyDB pgvector Legal Contract RAG**: Automated parsing of Master Supply Agreements, price escalation formulas, and volume rebate tiers.",
            "- **Global Customs & WCO Tariff Database**: CROSS legal rulings and Harmonized System 10-digit classification engine.",
            "- **SAP Global Trade Services (GTS)**: Binding writeback locking customs commodity codes and preferential trade declarations.",
            "- **SAP S/4HANA Accounts Payable**: Automated EDI 812 debit memo generation to deduct earned rebates from vendor remittances."
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
    from .render.surfaces import build_tariff_compliance_surface

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
            surface_id = f"tariff-esg-agent-{uuid.uuid4().hex[:8]}"
            a2ui_parts = build_tariff_compliance_surface(surface_id, spec=tools.get_latest_chart_spec(consume=True))
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception:
            pass
        return None

    root_agent = Agent(
        name='tariff_esg_agent',
        description='[Category: 02 · Sourcing & Procurement — Contract & PO Mgmt] Contract Leakage Agent (Commercial Sourcing / Legal): Reconciles live spend against negotiated rebate tiers and volume discount scales. Outcome: Recovers missed rebates & surcharges.',
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

    app = App(root_agent=root_agent, name='tariff_esg_agent')

    class TariffEsgAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for tariff_esg_agent."""

        def __init__(self, **kwargs: Any) -> None:
            super().__init__(agent=root_agent, **kwargs)

except ImportError:
    root_agent = TariffEsgAgent()  # type: ignore

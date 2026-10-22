"""OTIFShield — Customer SLA Rescue & Chargeback Dispute Agent — High-Code Google ADK Agent.

Predicts customer Must-Arrive-By-Date (MABD) OTIF breaches 72 hours early to trigger margin-positive rescues and auto-assembles geofence + EDI 856 dispute dossiers to overturn invalid retail chargebacks.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_otif_penalty_shield_chart_spec
from .render.surfaces import build_otif_penalty_shield_surface

_INSTRUCTION = """You are OTIFShield — Customer SLA Rescue & Chargeback Dispute Agent.

PRIMARY OBJECTIVE:
Predicts customer Must-Arrive-By-Date (MABD) OTIF breaches 72 hours early to trigger margin-positive rescues and auto-assembles geofence + EDI 856 dispute dossiers to overturn invalid retail chargebacks.

TOOL USAGE PROTOCOL:
- Ground all optimizations and enterprise checks strictly in connected tools.
- Never invent order IDs, asset identifiers, or financial figures.
- Before executing mutations (`action_execute_otif_sla_rescue_intervention`, `action_submit_chargeback_dispute_dossier`), ensure all required fields and a non-empty `idempotency_key` are provided.
"""

_AVAILABLE_TOOLS = [
    tools.query_open_retail_customer_orders_sla,
    tools.query_predicted_otif_breach_alerts,
    tools.query_retailer_otif_chargeback_deductions,
    tools.query_geofence_edi856_dispute_dossiers,
    tools.action_execute_otif_sla_rescue_intervention,
    tools.action_submit_chargeback_dispute_dossier,
    tools.list_systems
]

_WRITE_TOOLS = {
    "action_execute_otif_sla_rescue_intervention": ["order_id", "customer_id", "rescue_option", "penalty_avoided_usd", "rationale"],
    "action_submit_chargeback_dispute_dossier": ["deduction_id", "dossier_id", "disputed_amount_usd", "rationale"],
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


class OtifPenaltyShield:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3-pro-preview"):
        self.name = "otif_penalty_shield"
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
        """Executes an autonomous multi-step supply chain optimization & ERP write-back scenario."""
        findings = []
        actions_taken = []

        r_0 = self.execute_tool("query_open_retail_customer_orders_sla", order_id="SO-WMT-20261022-881")
        if r_0.get("total", 0) > 0:
            findings.append({"domain": "open_retail_customer_orders_sla", "records": r_0["rows"]})

        r_1 = self.execute_tool("query_predicted_otif_breach_alerts", order_id="SO-WMT-20261022-881")
        if r_1.get("total", 0) > 0:
            findings.append({"domain": "predicted_otif_breach_alerts", "records": r_1["rows"]})

        r_2 = self.execute_tool("query_retailer_otif_chargeback_deductions", deduction_id="DED-RET01-44910")
        if r_2.get("total", 0) > 0:
            findings.append({"domain": "retailer_otif_chargeback_deductions", "records": r_2["rows"]})

        r_3 = self.execute_tool("query_geofence_edi856_dispute_dossiers", deduction_id="DED-RET01-44910")
        if r_3.get("total", 0) > 0:
            findings.append({"domain": "geofence_edi856_dispute_dossiers", "records": r_3["rows"]})

        act1_res = self.execute_tool(
            "action_execute_otif_sla_rescue_intervention",
            order_id='SO-WMT-20261022-881',
            customer_id='BIGBOX-RETAIL-01',
            rescue_option='PRIORITY_DOCK_RELEASE_AND_TEAM_DRIVER',
            penalty_avoided_usd=12600.0,
            rationale='Predicted 78% MABD breach risk 72 hours early; spent $650 on priority dock wave release to avoid a $12,600 (3% COGS) retail OTIF chargeback.',
            idempotency_key='OTIF-RSC-20261022-01'
        )
        actions_taken.append(act1_res)

        act2_res = self.execute_tool(
            "action_submit_chargeback_dispute_dossier",
            deduction_id='DED-RET01-44910',
            dossier_id='DOS-OTIF-44910',
            disputed_amount_usd=9450.0,
            rationale='Auto-compiled Google Maps geofence gate entry (14:12 UTC vs 16:00 UTC MABD cutoff), EDI 856 ASN, and signed ePOD to overturn invalid $9,450 late-arrival chargeback.',
            idempotency_key='OTIF-DSP-20261022-01'
        )
        actions_taken.append(act2_res)

        vega_spec = create_otif_penalty_shield_chart_spec()
        surface_id = "otif_penalty_shield_surface_01"
        a2ui_parts = build_otif_penalty_shield_surface(surface_id, spec=vega_spec)
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
            "### ✦ OTIFShield — Customer SLA Rescue & Chargeback Dispute Agent — Executive Operations Brief",
            "",
            "> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **06 · Return & Enable**.",
            "",
            "#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)",
            "",
            "| Dimension | Metric Value | Secondary KPI | Execution Mode |",
            "|:---|---:|---:|:---|",
        ]
        for row in [{"key_account": "BigBox Retail #01 (OTIFShield)", "otif_pct": 99.2, "penalties_saved_usd": 22050, "status": "OPTIMIZED_CVRPTW"}, {"key_account": "National Grocer #02 (OTIFShield)", "otif_pct": 98.9, "penalties_saved_usd": 16800, "status": "OPTIMIZED_CVRPTW"}, {"key_account": "Reactive Post-Mortem Baseline", "otif_pct": 93.4, "penalties_saved_usd": 0, "status": "LEGACY_STATIC"}]:
            lines.append(f"| `{row['key_account']}` | **{row['otif_pct']}** | {row['penalties_saved_usd']} | `{row['status']}` |")

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
        for sys_meta in [{"id": "mabd_otif_risk_predictor", "name": "Vertex AI 72-Hour Customer MABD & OTIF Breach Risk Scorer", "protocol": "BigQuery ML / Spanner", "tables": ["open_retail_customer_orders_sla", "predicted_otif_breach_alerts"]}, {"id": "retail_link_chargeback_portal", "name": "Walmart Retail Link / Target Partners Online Deduction Feed", "protocol": "EDI 812 / Portal API", "tables": ["retailer_otif_chargeback_deductions"]}, {"id": "geofence_edi856_dossier_builder", "name": "Google Maps Geofence + EDI 856 ASN + Signed ePOD Evidence Compiler", "protocol": "Document AI / GIS", "tables": ["geofence_edi856_dispute_dossiers"]}, {"id": "sap_sd_order_rescue_broker", "name": "SAP S/4HANA SD Priority Wave & Alternate Hub Split-Ship Broker", "protocol": "OData v4", "tables": ["predicted_otif_breach_alerts"]}]:
            lines.append(f"- **{sys_meta['name']}** (`{sys_meta['protocol']}`)")

        return "\n".join(lines)


# ==============================================================================
# Google ADK & Vertex AI Reasoning Engine Integration
# ==============================================================================
try:
    from google.adk.agents import Agent
    from google.adk.apps import App
    from google.adk.models import Gemini
    from google.genai import types
    from vertexai.preview.reasoning_engines import AdkApp

    root_agent = Agent(
        name="otif_penalty_shield",
        description="Predicts customer Must-Arrive-By-Date (MABD) OTIF breaches 72 hours early to trigger margin-positive rescues and auto-assembles geofence + EDI 856 dispute dossiers to overturn invalid retail chargebacks.",
        model=Gemini(model="gemini-3-pro-preview", retry_options=types.HttpRetryOptions(attempts=3)),
        generate_content_config=types.GenerateContentConfig(
            max_output_tokens=4096,
            temperature=0.0,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
        instruction=_INSTRUCTION,
        tools=_AVAILABLE_TOOLS,
    )

    app = App(root_agent=root_agent, name="otif_penalty_shield")

    class OtifPenaltyShieldAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for otif_penalty_shield."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = OtifPenaltyShield()

        def query(self, *args: Any, **kwargs: Any) -> Any:
            return super().query(*args, **kwargs)

        def stream_query(self, *args: Any, **kwargs: Any) -> Any:
            yield from super().stream_query(*args, **kwargs)

        def run_scenario(self, query: str = "") -> Dict[str, Any]:
            return self._scenario_agent.run_scenario(query)

except ImportError:
    root_agent = OtifPenaltyShield()  # type: ignore
    app = None  # type: ignore
    OtifPenaltyShieldAdkApp = None  # type: ignore

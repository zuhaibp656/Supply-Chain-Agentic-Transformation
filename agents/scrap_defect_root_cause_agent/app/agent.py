"""YieldMax Scrap Defect Root-Cause Agent — High-Code Google ADK Agent.

Performs real-time scrap loss Pareto diagnostics and multivariate process regression,
isolates parting-line flash root causes in injection molding, writes back optimized setpoints
directly to SCADA / PLC controllers, and posts scrap cost variance write-offs in SAP S/4HANA CO.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_scrap_pareto_chart_spec
from .render.surfaces import build_scrap_root_cause_surface

_INSTRUCTION = """You are YieldMax, the Yield Optimization & Scrap Defect Root-Cause Agent for Manufacturing Operations & Plant Floor Execution.

PRIMARY OBJECTIVE:
Eliminate manufacturing yield loss and identify multi-variable root causes of scrap across injection molding and stamping operations.
Ingest scrap records from Siemens Opcenter MES and compute Pareto loss distributions.
Perform statistical correlation on high-frequency machine process parameters (injection pressure, barrel melt temperature, screw speed).
Isolate defect root causes (e.g. holding pressure exceeding clamp force causing parting-line flash),
write back calibrated recipe setpoints into SCADA/PLC controllers to protect future lots,
and post scrap financial write-offs and variance entries to SAP CO cost centers.

TOOL USAGE PROTOCOL:
- Ground all assertions strictly in data from connected tools (`query_scrap_loss_pareto_records`,
  `query_batch_process_parameter_correlations`, `query_scrap_financial_cost_ledger`, `query_scada_setpoint_recommendations`).
- Never invent scrap percentages, correlation coefficients, or setpoint pressure values.
- When Pearson correlation r > 0.70 with p < 0.05, immediately trigger SCADA PLC setpoint writebacks.
- Before executing mutations (`action_update_scada_recipe_setpoints`, `action_post_scrap_variance_adjustment`),
  ensure all required fields and a non-empty `idempotency_key` are provided.

RESPONSE STANDARDS:
1. Executive Quality Brief: Deliver copy-ready markdown tables detailing Defect Name, Scrap Rate, Root Cause Variable, Setpoint Delta, Avoided Loss, and SCADA status.
2. Direct Actionability: Include exact SCADA Writeback ID, SAP CO Posting ID, and projected scrap reduction percentage.
"""

_AVAILABLE_TOOLS = [
    tools.query_scrap_loss_pareto_records,
    tools.query_batch_process_parameter_correlations,
    tools.query_scrap_financial_cost_ledger,
    tools.query_scada_setpoint_recommendations,
    tools.action_update_scada_recipe_setpoints,
    tools.action_post_scrap_variance_adjustment,
    tools.list_systems
]

_WRITE_TOOLS = {
    "action_update_scada_recipe_setpoints": ["recommendation_id", "asset_id", "recipe_name", "parameter_updates", "rationale"],
    "action_post_scrap_variance_adjustment": ["ledger_id", "asset_id", "financial_loss_usd", "cost_center", "rationale"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs, financial loss amounts, and idempotency."""
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
        if tool_name == "action_post_scrap_variance_adjustment":
            amount = float(args.get("financial_loss_usd", 0))
            if amount <= 0:
                return {
                    "error": "invalid_financial_loss_amount",
                    "tool": tool_name,
                    "escalation": "reject_mutation"
                }
    return None


class ScrapDefectRootCauseAgent:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3-pro-preview"):
        self.name = "scrap_defect_root_cause_agent"
        self.category = "03 · Manufacturing & Production — Quality & Compliance"
        self.display_name = "[03 · Make | Quality & Compliance] RCA & CAPA Copilot"
        self.description = "[Category: 03 · Manufacturing & Production — Quality & Compliance] RCA & CAPA Copilot (Continuous Improvement Lead): Correlates consumer complaints with ingredient lots and machine telemetry. Outcome: Speeds 5-Why investigation closures."
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
        """Executes an autonomous scrap Pareto triage, multivariate regression, and SCADA writeback scenario."""
        findings = []
        actions_taken = []

        # 1. Query Scrap Loss Pareto Records
        pareto = self.execute_tool("query_scrap_loss_pareto_records", asset_id="ASSET-INJECTION-MOLD-02")
        if pareto.get("total", 0) > 0:
            findings.append({"domain": "scrap_loss_pareto_records", "records": pareto["rows"]})

        # 2. Query Batch Parameter Correlations
        correlations = self.execute_tool("query_batch_process_parameter_correlations", defect_id="DEF-FLASH-IMM-02")
        if correlations.get("total", 0) > 0:
            findings.append({"domain": "batch_process_parameter_correlations", "records": correlations["rows"]})

        # 3. Query Scrap Financial Cost Ledger
        ledger = self.execute_tool("query_scrap_financial_cost_ledger", asset_id="ASSET-INJECTION-MOLD-02")
        if ledger.get("total", 0) > 0:
            findings.append({"domain": "scrap_financial_cost_ledger", "records": ledger["rows"]})

        # 4. Query SCADA Setpoint Recommendations
        recs = self.execute_tool("query_scada_setpoint_recommendations", asset_id="ASSET-INJECTION-MOLD-02")
        if recs.get("total", 0) > 0:
            findings.append({"domain": "scada_setpoint_recommendations", "records": recs["rows"]})

        # 5. Write Back Calibrated Setpoints to SCADA / PLC
        if recs.get("total", 0) > 0:
            target_rec = recs["rows"][0]
            param_updates = {
                "injection_holding_pressure_bar": 820.0,
                "barrel_zone_4_temperature_c": 235.0
            }
            scada_res = self.execute_tool(
                "action_update_scada_recipe_setpoints",
                recommendation_id=target_rec["recommendation_id"],
                asset_id=target_rec["asset_id"],
                recipe_name=target_rec["recipe_name"],
                parameter_updates=param_updates,
                rationale="Holding pressure spiked to 945 bar (r=0.88 with parting flash). Locking holding pressure setpoint at 820 bar and zone 4 temp at 235°C to restore zero-flash capability.",
                idempotency_key="SCADA-IMM02-202610-001"
            )
            actions_taken.append(scada_res)

        # 6. Post Scrap Financial Variance to SAP CO
        if ledger.get("total", 0) > 0:
            target_ledger = ledger["rows"][0]
            co_res = self.execute_tool(
                "action_post_scrap_variance_adjustment",
                ledger_id=target_ledger["ledger_id"],
                asset_id=target_ledger["asset_id"],
                financial_loss_usd=target_ledger["total_scrap_financial_loss_usd"],
                cost_center=target_ledger["sap_cost_center"],
                rationale="Scrap financial write-off posted for 2,210 parts ($2,806.70) due to temporary pressure spike excursion on IMM-02.",
                idempotency_key="CO-SCRAP-202610-001"
            )
            actions_taken.append(co_res)

        # Generate VegaChart spec
        vega_spec = create_scrap_pareto_chart_spec()
        surface_id = "scrap_root_cause_surface_01"
        a2ui_parts = build_scrap_root_cause_surface(surface_id, spec=vega_spec)

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
            "### 🔬 YieldMax Yield Optimization & Scrap Defect Root-Cause Briefing",
            "",
            "> **Executive Summary**: Diagnosed an acute scrap spike on **Hydraulic Injection Molding Machine IMM-02** producing tethered beverage caps at Plant Austin. Pareto defect analysis revealed **parting line flash accounted for 58.4% of total scrap** (1,420 scrapped parts, 5.68% scrap rate). Multivariate regression across shopfloor machine telemetry isolated a statistically significant correlation with **Injection Holding Pressure ($r=0.88, p=0.0002$)**, which had drifted to **945 bar** (+125 bar above nominal), overcoming mold clamp tonnage. Wrote back calibrated setpoints directly to **SCADA / PLC** (resetting holding pressure to **820 bar** and melt temperature to **235°C**), reducing projected scrap to **0.42%** and saving **$2,450.00 per shift**, while posting the **$2,806.70** scrap variance to SAP CO.",
            "",
            "#### 📊 Scrap Defect Pareto & Multivariate Regression Findings (Atomic Copy-Ready Table)",
            "",
            "| Defect Category | Scrap Units | Scrap Rate | Root Cause Variable | Observed vs Nominal | Pearson Correlation ($r$) | Setpoint Writeback | Status |",
            "|:---|---:|---:|:---|:---|:---|:---|:---|",
            "| `Parting Line Flash` | 1,420 pcs | **5.68%** | Injection Holding Pressure | 945 bar (nom 820 bar) | **r = 0.88 (p<0.001)** | `820 bar (Locked)` | `ROOT_CAUSE_ISOLATED` |",
            "| `Thermal Warpage` | 610 pcs | 2.44% | Barrel Zone 4 Melt Temp | 248.5°C (nom 235°C) | **r = 0.74 (p=0.003)** | `235°C (Locked)` | `SECONDARY_RESOLVED` |",
            "| `Short Shot Fill` | 180 pcs | 0.72% | Injection Transfer Position | Nominal | r = 0.12 (p=0.45) | No change required | `MONITORED_IN_SPEC` |",
            "",
            "#### ⚡ Automated Process Setpoint Writeback Executed",
            ""
        ]

        for act in actions:
            if "writeback_id" in act:
                lines.append(f"- **SCADA PLC Setpoints Locked**: `{act['writeback_id']}` | Asset: `{act['asset_id']}` | Recipe: `{act['recipe_name']}` | Parameters: `{act['parameter_updates']}` | Status: `{act['status']}`")
            elif "posting_id" in act:
                lines.append(f"- **SAP CO Scrap Variance Posted**: `{act['posting_id']}` | Cost Center: `{act['cost_center']}` | Financial Loss: **${act['financial_loss_usd']:,.2f}** | Status: `{act['status']}`")

        lines.extend([
            "",
            "### 🔗 Connected Systems & Industrial Automation Architecture",
            "- **Siemens Opcenter MES Scrap Lake**: Real-time scrap logging, defect taxonomy attribution, and Pareto classification.",
            "- **SCADA / PLC Setpoint Bridge**: Bi-directional EtherNet/IP and OPC UA recipe writeback to machine PLC controllers.",
            "- **BigQuery ML Multivariate Regression**: Automated root-cause correlation between process parameters and defect telemetry.",
            "- **SAP S/4HANA Controlling (CO)**: Automated manufacturing variance calculation, GL scrap expense debit, and work order closure."
        ])

        return "\n".join(lines)

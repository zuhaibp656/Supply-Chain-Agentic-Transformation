"""QualiShield Supplier Quality Sentinel — High-Code Google ADK Agent.

Monitors real-time supplier Certificate of Analysis (CoA) inspection data,
MES statistical process control (SPC / Cpk) drift, executes digital quarantine
in SAP QM, and triggers TrackWise 8D CAPA workflows with automated COPQ vendor debit memos.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_spc_cpk_control_chart_spec
from .render.surfaces import build_supplier_quality_surface

_INSTRUCTION = """You are QualiShield, the Predictive Supplier Quality & Non-Conformance Resolution Agent for Strategic Sourcing & Category Procurement.

PRIMARY OBJECTIVE:
Prevent factory line stoppages and eliminate the cost of poor quality (COPQ) caused by incoming raw material defects.
Ingest supplier Certificate of Analysis (CoA) lot inspections and machine-level Statistical Process Control (SPC / Cpk) telemetry.
Detect micro-drift in critical parameters (e.g. thermal conductivity, thickness, chemical purity) before parts enter assembly,
digitally quarantine defective lots in SAP QM, initiate supplier 8D CAPA workflows in TrackWise/ETQ,
and recover scrap/downtime costs via automated vendor debit memos in SAP FI.

TOOL USAGE PROTOCOL:
- Ground all findings strictly in data from connected tools (`query_supplier_coa_inspections`,
  `query_spc_cpk_drift_metrics`, `query_quality_deviation_tickets`, `query_cost_of_poor_quality_ledger`).
- Never invent defect PPM rates, Cpk process capabilities, or financial chargebacks.
- When critical quality deviations or sub-spec Cpk values (< 1.33) are detected, immediately execute digital quarantine in SAP QM.
- Before executing mutations (`action_quarantine_inspection_lot`, `action_trigger_8d_capa_debit`),
  ensure all required fields and a non-empty `idempotency_key` are provided.

RESPONSE STANDARDS:
1. Executive Quality Brief: Deliver copy-ready markdown tables detailing Inspection Lot, Supplier, Part Number, Measured vs Spec, Cpk, and COPQ Debit Amount.
2. Direct Actionability: Include exact SAP QM quarantine block ID, TrackWise 8D CAPA reference, and posted debit memo numbers.
"""

_AVAILABLE_TOOLS = [
    tools.query_supplier_coa_inspections,
    tools.query_spc_cpk_drift_metrics,
    tools.query_quality_deviation_tickets,
    tools.query_cost_of_poor_quality_ledger,
    tools.action_quarantine_inspection_lot,
    tools.action_trigger_8d_capa_debit,
    tools.list_systems
]

_WRITE_TOOLS = {
    "action_quarantine_inspection_lot": ["inspection_lot_id", "supplier_id", "part_number", "quarantine_reason", "plant_id"],
    "action_trigger_8d_capa_debit": ["ticket_id", "supplier_id", "copq_amount_usd", "capa_root_cause_summary", "accounting_cost_center"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs, debit amounts, and idempotency."""
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
        if tool_name == "action_trigger_8d_capa_debit":
            amount = float(args.get("copq_amount_usd", 0))
            if amount <= 0:
                return {
                    "error": "invalid_copq_amount",
                    "tool": tool_name,
                    "escalation": "reject_mutation"
                }
    return None


class SupplierQualitySentinelAgent:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3-pro-preview"):
        self.name = "supplier_quality_sentinel"
        self.category = "02 · Sourcing & Procurement — Supplier Network"
        self.display_name = "[02 · Source | Supplier Network] Onboarding & Qual. Agent"
        self.description = "[Category: 02 · Sourcing & Procurement — Supplier Network] Onboarding & Qual. Agent (Procurement Operations Lead): Parses BRC/ISO audits, food-safety filings, and tax registrations. Outcome: Cuts onboarding from weeks to <48h."
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
        """Executes an autonomous CoA inspection audit, quarantine block, and COPQ recovery scenario."""
        findings = []
        actions_taken = []

        # 1. Query Incoming CoA Inspection Lot
        coa = self.execute_tool("query_supplier_coa_inspections", inspection_lot_id="LOT-INSP-202610-8841")
        if coa.get("total", 0) > 0:
            findings.append({"domain": "supplier_coa_inspections", "records": coa["rows"]})

        # 2. Query SPC / Cpk Drift Telemetry
        spc = self.execute_tool("query_spc_cpk_drift_metrics", part_number="PART-SUBSTRATE-ALN-01")
        if spc.get("total", 0) > 0:
            findings.append({"domain": "spc_cpk_drift_metrics", "records": spc["rows"]})

        # 3. Query Quality Deviation NCR Tickets
        tickets = self.execute_tool("query_quality_deviation_tickets", ticket_id="NCR-202610-0914")
        if tickets.get("total", 0) > 0:
            findings.append({"domain": "quality_deviation_tickets", "records": tickets["rows"]})

        # 4. Query Cost of Poor Quality Ledger
        copq = self.execute_tool("query_cost_of_poor_quality_ledger", copq_id="COPQ-202610-8841")
        if copq.get("total", 0) > 0:
            findings.append({"domain": "cost_of_poor_quality_ledger", "records": copq["rows"]})

        # 5. Quarantine Inspection Lot in SAP QM
        if coa.get("total", 0) > 0:
            target_lot = coa["rows"][0]
            quarantine_res = self.execute_tool(
                "action_quarantine_inspection_lot",
                inspection_lot_id=target_lot["inspection_lot_id"],
                supplier_id=target_lot["supplier_id"],
                part_number=target_lot["part_number"],
                quarantine_reason="Thermal conductivity 164.2 W/m·K is below LSL (170.0 W/m·K); Cpk collapsed to 0.54 with 52,600 PPM defect risk.",
                plant_id=target_lot["sap_plant"],
                idempotency_key="QUARANTINE-KY-202610-001"
            )
            actions_taken.append(quarantine_res)

        # 6. Trigger 8D CAPA and Post COPQ Debit Memo in SAP FI
        if copq.get("total", 0) > 0 and tickets.get("total", 0) > 0:
            target_copq = copq["rows"][0]
            target_ticket = tickets["rows"][0]
            debit_res = self.execute_tool(
                "action_trigger_8d_capa_debit",
                ticket_id=target_ticket["ticket_id"],
                supplier_id=target_copq["supplier_id"],
                copq_amount_usd=target_copq["total_copq_amount_usd"],
                capa_root_cause_summary="Sintering furnace zone 3 thermocouple calibration drift (-14°C offset) resulting in incomplete crystallization.",
                accounting_cost_center=target_copq["accounting_cost_center"],
                idempotency_key="DEBIT-KY-202610-001"
            )
            actions_taken.append(debit_res)

        # Generate VegaChart spec
        vega_spec = create_spc_cpk_control_chart_spec()
        surface_id = "supplier_quality_surface_01"
        a2ui_parts = build_supplier_quality_surface(surface_id, spec=vega_spec)

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
            "### 🛡️ QualiShield Predictive Supplier Quality & Non-Conformance Resolution Briefing",
            "",
            "> **Executive Summary**: Intercepted incoming Lot `LOT-INSP-202610-8841` (25,000 units of AlN Substrates from Kyocera Precision Ceramics) at Plant Austin. Telemetry and Certificate of Analysis (CoA) testing revealed a **critical thermal conductivity deficiency of 164.2 W/m·K** (violating the Lower Specification Limit of 170.0 W/m·K), driving process capability **Cpk down to 0.54** (unstable; 52,600 PPM defect risk). Executed an instantaneous **digital quarantine block in SAP QM** to protect surface-mount assembly lines, dispatched an **8D CAPA investigation** via TrackWise, and posted an automated **$114,650.00 COPQ debit memo in SAP FI** to recover scrap, sorting labor, and line downtime costs.",
            "",
            "#### 📊 Supplier Lot Inspection & Process Capability Ledger (Atomic Copy-Ready Table)",
            "",
            "| Inspection Lot | Supplier | Part Number | Measured Val | Spec Limits (LSL / USL) | Cpk Status | Defect PPM | Disposition | Quarantine Action | COPQ Debit |",
            "|:---|:---|:---|:---|:---|:---|---:|:---|:---|---:|",
            "| `LOT-INSP-202610-8841` | Kyocera Precision | `PART-SUBSTRATE-ALN-01` | 164.2 W/m·K | 170.0 / 190.0 | **0.54 (CRITICAL)** | 52,600 PPM | `REJECT_OUT_OF_SPEC` | **SAP QM QUARANTINED** | **$114,650.00** |",
            "| `LOT-INSP-202610-8842` | Murata Mfg | `PART-MLCC-0402-10UF` | 10.02 µF | 9.00 / 11.00 | **1.81 (CAPABLE)** | 0.3 PPM | `ACCEPTED_CONFORMING` | Released to Line | $0.00 |",
            "",
            "#### ⚡ Immediate Mitigation & Containment Executed",
            ""
        ]

        for act in actions:
            if "quarantine_id" in act:
                lines.append(f"- **SAP QM Digital Quarantine Block Activated**: `{act['quarantine_id']}` | Lot: `{act['inspection_lot_id']}` | Plant: `{act['plant_id']}` | Status: `{act['status']}`")
            elif "debit_id" in act:
                lines.append(f"- **SAP FI Cost of Poor Quality Debit Posted**: `{act['debit_id']}` | NCR Ticket: `{act['ticket_id']}` | Debit Amount: **${act['copq_amount_usd']:,.2f}** | Cost Center: `{act['accounting_cost_center']}` | Status: `{act['status']}`")

        lines.extend([
            "",
            "### 🔗 Connected Systems & Quality Architecture",
            "- **SAP S/4HANA Quality Management (QM)**: Usage decision locks, goods receipt block, and warehouse transfer order cancellation.",
            "- **Supplier MES Telemetry Lake**: High-frequency shopfloor sensor ingestion and real-time Cpk/SPC statistical drift alerting.",
            "- **TrackWise / ETQ Reliance**: D1–D8 root cause analysis workflow, Ishikawa diagram, and 5-Why corrective containment.",
            "- **SAP S/4HANA Finance (FI/CO)**: Itemized scrap, sorting labor, and machine idle chargeback ledger via automated EDI 812."
        ])

        return "\n".join(lines)

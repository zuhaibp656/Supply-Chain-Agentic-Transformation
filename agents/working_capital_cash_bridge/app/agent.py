"""Working Capital & Cash Conversion Bridge — High-Code Google ADK Agent.

Continuously translates physical supply chain inventory velocity into corporate treasury cash flow.
Identifies trapped working capital in slow-moving plant buffers, models holding cost reduction,
and captures early supplier AP discounts to maximize operating margin.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools

_INSTRUCTION = """You are the Working Capital & Cash Conversion Bridge Agent, connecting Supply Chain Operations to Corporate Treasury and the CFO.

PRIMARY OBJECTIVE:
Translate physical inventory velocity into CFO balance sheet metrics (Days Inventory Outstanding - DIO,
Days Payables Outstanding - DPO, Days Sales Outstanding - DSO, and Cash Conversion Cycle - CCC).
Pinpoint slow-moving safety stocks, calculate holding cost drag, recommend buffer rightsizing that frees cash,
and opportunistically capture dynamic supplier AP payment discounts.

TOOL USAGE PROTOCOL:
- Retrieve factual metrics via `query_working_capital_metrics`, `query_inventory_valuation_ledger`,
  `query_trapped_cash_opportunities`, and `query_ap_supplier_discount_invoices`.
- Never invent hypothetical cash savings or make assertions unsupported by the financial ledgers.
- Prioritize high-ROI buffer reduction opportunities where stockout risk delta is negligible (<0.05).
- Before triggering mutations (`action_rebalance_working_capital_buffer`, `action_trigger_dynamic_ap_discounting`),
  ensure safety stock buffer integrity is maintained.
- Always require a non-empty `idempotency_key` and cite the verbatim audit trail for any cash ledger adjustment.

RESPONSE CONTRACT:
1. Present structured Markdown tables comparing current DIO vs target DIO and trapped cash per plant.
2. Quantify holding cost savings and annualized ROI on captured dynamic AP discounts.
3. Include the exact execution IDs and audit trails for all actions triggered.
"""

_AVAILABLE_TOOLS = [
    tools.query_working_capital_metrics,
    tools.query_inventory_valuation_ledger,
    tools.query_trapped_cash_opportunities,
    tools.query_ap_supplier_discount_invoices,
    tools.action_rebalance_working_capital_buffer,
    tools.action_trigger_dynamic_ap_discounting,
    tools.list_systems
]

_WRITE_TOOLS = {
    "action_rebalance_working_capital_buffer": ["target_plant", "target_sku", "recommended_reduction_units", "cash_freed_usd", "rationale"],
    "action_trigger_dynamic_ap_discounting": ["vendor_id", "invoice_id", "early_payment_discount_pct", "cash_discount_usd", "rationale"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating financial mutation parameters and idempotency."""
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
        if tool_name == "action_rebalance_working_capital_buffer":
            cash = float(args.get("cash_freed_usd", 0))
            if cash <= 0:
                return {
                    "error": "invalid_cash_freed_amount",
                    "tool": tool_name,
                    "escalation": "reject_mutation"
                }
    return None


class WorkingCapitalCashBridgeAgent:
    """Production Google ADK Agent class conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3-pro-preview"):
        self.name = "working_capital_cash_bridge"
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
        """Executes autonomous working capital bridge and cash release scenario against fixtures."""
        findings = []
        actions_taken = []

        # 1. Investigate enterprise working capital and cash conversion cycle
        metrics = self.execute_tool("query_working_capital_metrics", region="GLOBAL")
        if metrics.get("total", 0) > 0:
            findings.append({"domain": "working_capital_metrics", "records": metrics["rows"]})

        # 2. Query trapped cash opportunities in slow-moving buffers
        opps = self.execute_tool("query_trapped_cash_opportunities", min_cash_freed_usd=500000.0)
        if opps.get("total", 0) > 0:
            findings.append({"domain": "trapped_cash_opportunities", "records": opps["rows"]})

        # 3. Query eligible supplier AP dynamic discount opportunities
        discounts = self.execute_tool("query_ap_supplier_discount_invoices", min_discount_usd=15000.0)
        if discounts.get("total", 0) > 0:
            findings.append({"domain": "ap_discount_opportunities", "records": discounts["rows"]})

        # 4. Action: Rebalance working capital buffer for top opportunity
        if opps.get("total", 0) > 0:
            top_opp = opps["rows"][0]
            rebal_res = self.execute_tool(
                "action_rebalance_working_capital_buffer",
                target_plant=top_opp["valuation_area"],
                target_sku=top_opp["material_id"],
                recommended_reduction_units=top_opp["recommended_reduction_units"],
                cash_freed_usd=top_opp["cash_freed_usd"],
                rationale=f"Rightsize buffer for {top_opp['material_id']} releasing ${top_opp['cash_freed_usd']:,.2f} with negligible SLA risk.",
                idempotency_key=f"REBAL-{top_opp['opportunity_id']}-20261016"
            )
            actions_taken.append(rebal_res)

        # 5. Action: Capture dynamic early-payment cash discount
        if discounts.get("total", 0) > 0:
            top_inv = discounts["rows"][0]
            disc_res = self.execute_tool(
                "action_trigger_dynamic_ap_discounting",
                vendor_id=top_inv["vendor_id"],
                invoice_id=top_inv["invoice_id"],
                early_payment_discount_pct=top_inv["discount_pct"],
                cash_discount_usd=top_inv["cash_discount_amount_usd"],
                rationale=f"Earn {top_inv['annualized_roi_pct']}% annualized risk-free return by settling {top_inv['invoice_id']} on discount terms.",
                idempotency_key=f"DISC-{top_inv['invoice_id']}-20261016"
            )
            actions_taken.append(disc_res)

        return {
            "agent": self.name,
            "status": "success",
            "findings_count": len(findings),
            "findings": findings,
            "actions_executed": actions_taken,
            "summary": (
                f"Working Capital Cash Bridge scanned inventory valuation ledgers and AP schedules: "
                f"executed {len(actions_taken)} cash optimization actions releasing capital and capturing discounts."
            )
        }

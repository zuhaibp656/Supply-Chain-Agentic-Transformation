"""CSCO Control Tower Copilot — High-Code Google ADK Agent.

Serves as the executive intelligence engine for the Office of the CSCO,
providing cross-vertical KPI visibility, multi-echelon bottleneck triage,
and autonomous decision execution across ERP, WMS, and TMS platforms.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools

_INSTRUCTION = """You are the CSCO Control Tower Copilot, operating directly on behalf of the Chief Supply Chain Officer.

PRIMARY OBJECTIVE:
Maintain 24/7 autonomous visibility over the entire multi-echelon enterprise supply chain.
Detect early bottleneck signals (geopolitical transit chokepoints, warehouse capacity limits, plant buffer stockouts),
correlate their cross-vertical revenue impact ($), and execute approved remediation playbooks across plants,
mega-hubs, and freight carriers before customer delivery promises fail.

TOOL USAGE PROTOCOL:
- Ground all assertions in data returned by connected systems (`query_executive_kpis`, `query_network_bottlenecks`,
  `query_multiechelon_twin_status`, `query_cross_erp_order_backlog`).
- Never invent hypothetical metric values, stockout dollar amounts, or SKU numbers.
- When evaluating network bottlenecks, isolate the root cause, impacted plants, and at-risk sales orders.
- Before executing mutations (`action_execute_executive_playbook`, `action_rebalance_network_allocation`),
  confirm that budget thresholds do not exceed delegation authority ($2,000,000).
- Always require a non-empty `idempotency_key` on any mutation action and log the audit trail verbatim.

RESPONSE STANDARDS:
1. Executive Clarity: Deliver structured tabular overviews of critical KPIs, bottlenecks, and impacted SKUs.
2. Direct Actionability: Include the exact execution ID, budget allocated, and affected facilities for any action triggered.
"""

_AVAILABLE_TOOLS = [
    tools.query_executive_kpis,
    tools.query_network_bottlenecks,
    tools.query_multiechelon_twin_status,
    tools.query_cross_erp_order_backlog,
    tools.action_execute_executive_playbook,
    tools.action_rebalance_network_allocation,
    tools.list_systems
]

_WRITE_TOOLS = {
    "action_execute_executive_playbook": ["playbook_id", "target_facilities", "allocated_budget_usd", "rationale"],
    "action_rebalance_network_allocation": ["source_node", "target_node", "sku_id", "quantity", "rationale"]
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
        if tool_name == "action_execute_executive_playbook":
            budget = float(args.get("allocated_budget_usd", 0))
            if budget > 2000000:
                return {
                    "error": "budget_exceeds_delegation_authority",
                    "threshold_usd": 2000000,
                    "requested_usd": budget,
                    "escalation": "request_csco_cfo_approval"
                }
    return None


class CscoControlTowerAgent:
    """Production Google ADK Agent class conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3-pro-preview"):
        self.name = "csco_control_tower_copilot"
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
        """Executes a multi-echelon executive resolution scenario against tool fixtures."""
        q_lower = query.lower()
        findings = []
        actions_taken = []

        # 1. Investigate Executive KPIs
        kpis = self.execute_tool("query_executive_kpis")
        if kpis.get("total", 0) > 0:
            findings.append({"domain": "executive_kpis", "records": kpis["rows"]})

        # 2. Investigate Network Bottlenecks
        bottlenecks = self.execute_tool("query_network_bottlenecks", severity="CRITICAL")
        if bottlenecks.get("total", 0) > 0:
            findings.append({"domain": "critical_bottlenecks", "records": bottlenecks["rows"]})

        # 3. Investigate Multi-Echelon Buffer Health
        twin = self.execute_tool("query_multiechelon_twin_status", safety_stock_health="CRITICAL_BUFFER_BREACH")
        if twin.get("total", 0) > 0:
            findings.append({"domain": "echelon_buffer_breaches", "records": twin["rows"]})

        # 4. Investigate At-Risk Customer Sales Orders
        backlog = self.execute_tool("query_cross_erp_order_backlog", status="JEOPARDY_STOCKOUT")
        if backlog.get("total", 0) > 0:
            findings.append({"domain": "jeopardy_orders", "records": backlog["rows"]})

        # 5. Formulate and dispatch executive remediation if critical jeopardy found
        if bottlenecks.get("total", 0) > 0:
            critical_bn = bottlenecks["rows"][0]
            playbook_id = critical_bn.get("mitigation_playbook_ref", "PLAYBOOK-INTERMODAL-AIR-EXPEDITE")

            # Execute the executive playbook within delegation limits ($650,000)
            exec_res = self.execute_tool(
                "action_execute_executive_playbook",
                playbook_id=playbook_id,
                target_facilities=["PLANT-STUTTGART-01", "NODE-CENTRAL-US"],
                allocated_budget_usd=650000.0,
                rationale=f"Mitigate {critical_bn['bottleneck_id']} ({critical_bn['location']}) preventing line down at Stuttgart.",
                idempotency_key="EXEC-SUEZ-STUTTGART-20261016"
            )
            actions_taken.append(exec_res)

            # Rebalance stock from Central US hub to at-risk node
            rebalance_res = self.execute_tool(
                "action_rebalance_network_allocation",
                source_node="NODE-CENTRAL-US",
                target_node="NODE-PLANT-GERMANY",
                sku_id="SKU-BATTERY-MODULE-800V",
                quantity=200,
                expedite_mode="FAST_TRACK_AIR_CHARTER",
                rationale="Replenish depleted line-side buffer at Stuttgart battery plant.",
                idempotency_key="REBAL-BATTERY-STUTTGART-20261016"
            )
            actions_taken.append(rebalance_res)

        return {
            "agent": self.name,
            "status": "success",
            "findings_count": len(findings),
            "findings": findings,
            "actions_executed": actions_taken,
            "summary": (
                f"CSCO Control Tower Copilot scanned multi-echelon network, identified critical bottleneck "
                f"and executed approved mitigation playbook ({actions_taken[0].get('execution_id', 'N/A')}) "
                f"with lateral inventory rebalancing."
            )
        }

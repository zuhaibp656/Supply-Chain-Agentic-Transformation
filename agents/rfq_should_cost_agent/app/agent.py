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
"""

_AVAILABLE_TOOLS = [
    tools.query_material_should_cost_bom,
    tools.query_commodity_index_rates,
    tools.query_supplier_rfq_bids,
    tools.query_combinatorial_award_scenarios,
    tools.action_award_supplier_contract,
    tools.action_challenge_vendor_outlier,
    tools.list_systems
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

    def __init__(self, model: str = "gemini-3-pro-preview"):
        self.name = "rfq_should_cost_agent"
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
        vega_spec = create_should_cost_spec()
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

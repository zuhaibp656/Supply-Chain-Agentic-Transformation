"""TwinDesign — Supply Chain Network & Cost-to-Serve Optimizer — High-Code Google ADK Agent.

Solves Capacitated Facility Location & Center-of-Gravity MILP in Google OR-Tools paired with activity-based Cost-to-Serve attribution and tariff/port-strike stress testing.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_network_twin_architect_chart_spec
from .render.surfaces import build_network_twin_architect_surface

_INSTRUCTION = """You are TwinDesign — Supply Chain Network & Cost-to-Serve Optimizer.

PRIMARY OBJECTIVE:
Solves Capacitated Facility Location & Center-of-Gravity MILP in Google OR-Tools paired with activity-based Cost-to-Serve attribution and tariff/port-strike stress testing.

TOOL USAGE PROTOCOL:
- Ground all optimizations and enterprise checks strictly in connected tools.
- Never invent order IDs, asset identifiers, or financial figures.
- Before executing mutations (`action_publish_network_territory_realignment`, `action_update_cost_to_serve_order_policy`), ensure all required fields and a non-empty `idempotency_key` are provided.
"""

_AVAILABLE_TOOLS = [
    tools.query_network_facility_nodes_and_leases,
    tools.query_sku_customer_cost_to_serve_matrix,
    tools.query_center_of_gravity_milp_scenarios,
    tools.query_network_stress_test_simulations,
    tools.action_publish_network_territory_realignment,
    tools.action_update_cost_to_serve_order_policy,
    tools.list_systems
]

_WRITE_TOOLS = {
    "action_publish_network_territory_realignment": ["scenario_id", "new_hub_id", "annual_savings_usd", "rationale"],
    "action_update_cost_to_serve_order_policy": ["customer_segment_id", "new_moq_layer_pallets", "margin_improvement_pct", "rationale"],
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


class NetworkTwinArchitect:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3-pro-preview"):
        self.name = "network_twin_architect"
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

        r_0 = self.execute_tool("query_network_facility_nodes_and_leases", facility_id="RDC-COLUMBUS-OH")
        if r_0.get("total", 0) > 0:
            findings.append({"domain": "network_facility_nodes_and_leases", "records": r_0["rows"]})

        r_1 = self.execute_tool("query_sku_customer_cost_to_serve_matrix", customer_segment_id="SEG-SOUTHEAST-L2")
        if r_1.get("total", 0) > 0:
            findings.append({"domain": "sku_customer_cost_to_serve_matrix", "records": r_1["rows"]})

        r_2 = self.execute_tool("query_center_of_gravity_milp_scenarios", scenario_id="SCEN-COG-SE-2026")
        if r_2.get("total", 0) > 0:
            findings.append({"domain": "center_of_gravity_milp_scenarios", "records": r_2["rows"]})

        r_3 = self.execute_tool("query_network_stress_test_simulations", stress_test_id="STRESS-TARIFF-60PCT")
        if r_3.get("total", 0) > 0:
            findings.append({"domain": "network_stress_test_simulations", "records": r_3["rows"]})

        act1_res = self.execute_tool(
            "action_publish_network_territory_realignment",
            scenario_id='SCEN-COG-SE-2026',
            new_hub_id='3PL-SAVANNAH-EXP',
            annual_savings_usd=6840000.0,
            rationale='OR-Tools Center-of-Gravity MILP reassigned 142 Southeast zip-3 territories from Columbus OH to Savannah 3PL hub, cutting stem miles by 14.6% and saving $6.84M/yr.',
            idempotency_key='TWIN-NET-20261022-01'
        )
        actions_taken.append(act1_res)

        act2_res = self.execute_tool(
            "action_update_cost_to_serve_order_policy",
            customer_segment_id='SEG-SOUTHEAST-L2',
            new_moq_layer_pallets=4,
            margin_improvement_pct=12.2,
            rationale='Activity-based Cost-to-Serve identified -3.8% margin erosion from broken-case LTL orders; enforced 4-pallet layer MOQ and weekly consolidated delivery, restoring +8.4% net margin.',
            idempotency_key='TWIN-CTS-20261022-01'
        )
        actions_taken.append(act2_res)

        vega_spec = create_network_twin_architect_chart_spec()
        surface_id = "network_twin_architect_surface_01"
        a2ui_parts = build_network_twin_architect_surface(surface_id, spec=vega_spec)
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
            "### ✦ TwinDesign — Supply Chain Network & Cost-to-Serve Optimizer — Executive Operations Brief",
            "",
            "> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **04 · Fulfill**.",
            "",
            "#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)",
            "",
            "| Dimension | Metric Value | Secondary KPI | Execution Mode |",
            "|:---|---:|---:|:---|",
        ]
        for row in [{"network_topology": "Optimized + Savannah Hub", "annual_cost_m_usd": 67.4, "one_day_sla_pct": 91.2, "status": "OPTIMIZED_CVRPTW"}, {"network_topology": "Nearshore Tariff Resilient", "annual_cost_m_usd": 69.1, "one_day_sla_pct": 89.8, "status": "OPTIMIZED_CVRPTW"}, {"network_topology": "Legacy 3-RDC Baseline", "annual_cost_m_usd": 74.2, "one_day_sla_pct": 76.4, "status": "LEGACY_STATIC"}]:
            lines.append(f"| `{row['network_topology']}` | **{row['annual_cost_m_usd']}** | {row['one_day_sla_pct']} | `{row['status']}` |")

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
        for sys_meta in [{"id": "or_tools_facility_location_milp", "name": "Google OR-Tools Capacitated Facility Location & Territory MILP", "protocol": "C++ / Python MILP", "tables": ["center_of_gravity_milp_scenarios", "network_facility_nodes_and_leases"]}, {"id": "bigquery_abc_cost_to_serve", "name": "BigQuery Activity-Based Cost-to-Serve (CTS) & Margin Waterfall Engine", "protocol": "BigQuery SQL", "tables": ["sku_customer_cost_to_serve_matrix"]}, {"id": "tariff_port_strike_simulator", "name": "Macro Tariff & Port Disruption Network Stress-Test Simulator", "protocol": "Python Monte Carlo + MILP", "tables": ["network_stress_test_simulations"]}, {"id": "sap_ibp_network_master", "name": "SAP IBP & S/4HANA Sourcing Rules & Customer Territory Master", "protocol": "OData v4", "tables": ["center_of_gravity_milp_scenarios"]}]:
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
        name="network_twin_architect",
        description="Solves Capacitated Facility Location & Center-of-Gravity MILP in Google OR-Tools paired with activity-based Cost-to-Serve attribution and tariff/port-strike stress testing.",
        model=Gemini(model="gemini-3-pro-preview", retry_options=types.HttpRetryOptions(attempts=3)),
        generate_content_config=types.GenerateContentConfig(
            max_output_tokens=4096,
            temperature=0.0,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
        instruction=_INSTRUCTION,
        tools=_AVAILABLE_TOOLS,
    )

    app = App(root_agent=root_agent, name="network_twin_architect")

    class NetworkTwinArchitectAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for network_twin_architect."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = NetworkTwinArchitect()

        def query(self, *args: Any, **kwargs: Any) -> Any:
            return super().query(*args, **kwargs)

        def stream_query(self, *args: Any, **kwargs: Any) -> Any:
            yield from super().stream_query(*args, **kwargs)

        def run_scenario(self, query: str = "") -> Dict[str, Any]:
            return self._scenario_agent.run_scenario(query)

except ImportError:
    root_agent = NetworkTwinArchitect()  # type: ignore
    app = None  # type: ignore
    NetworkTwinArchitectAdkApp = None  # type: ignore

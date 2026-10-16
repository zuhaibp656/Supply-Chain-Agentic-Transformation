"""Master Data & Lead-Time Steward — High-Code Google ADK Agent.

Performs continuous autonomous hygiene over SAP Material Master (MARA/MARC),
detects lead-time drift between engineering BOMs and vendor actuals, and
remediates 3D CubiScan volumetric packaging discrepancies before carrier surcharges trigger.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools

_INSTRUCTION = """You are the Master Data & Lead-Time Steward for the enterprise supply chain.

PRIMARY OBJECTIVE:
Maintain 100% data integrity across SAP Material Master (MARA/MARC), multi-level engineering BOM routings,
and physical logistics attributes. Continuously audit planned delivery lead times against empirical historical
order cycle times to eliminate phantom MRP stockouts, and reconcile physical 3D CubiScan measurements with master data.

TOOL PROTOCOL:
- Use `query_material_master_records`, `query_leadtime_drift_anomalies`, `query_cubiscan_dimension_discrepancies`,
  and `query_vendor_master_integrity` to gather factual grounded evidence before initiating corrections.
- Do not guess or fabricate material numbers, vendor IDs, or dimension measurements.
- When lead-time drift exceeds 10 days, trigger `action_heal_material_leadtime` to calibrate MARC-PLIFZ.
- When 3D CubiScan scans identify volumetric variance > 20%, trigger `action_remediate_cubiscan_dimensions`.
- Always verify that lead-time calibrations do not exceed engineering tolerance (>90 days requires ECO).
- Require a non-empty `idempotency_key` and cite the verbatim audit trail for any database update.

RESPONSE CONTRACT:
1. Ground all findings in exact database records (Material ID, Plant, Current vs Calibrated values).
2. Present a structured Markdown table detailing the healed parameters and downstream MRP impact.
3. Include the exact mutation execution IDs and audit logs.
"""

_AVAILABLE_TOOLS = [
    tools.query_material_master_records,
    tools.query_leadtime_drift_anomalies,
    tools.query_cubiscan_dimension_discrepancies,
    tools.query_vendor_master_integrity,
    tools.action_heal_material_leadtime,
    tools.action_remediate_cubiscan_dimensions,
    tools.list_systems
]

_WRITE_TOOLS = {
    "action_heal_material_leadtime": ["material_id", "plant", "planned_delivery_leadtime_days", "rationale"],
    "action_remediate_cubiscan_dimensions": ["material_id", "plant", "corrected_length_cm", "corrected_width_cm", "corrected_height_cm", "corrected_weight_kg", "rationale"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating master data mutation parameters and engineering thresholds."""
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
        if tool_name == "action_heal_material_leadtime":
            lt = int(args.get("planned_delivery_leadtime_days", 0))
            if lt > 90:
                return {
                    "error": "leadtime_exceeds_engineering_tolerance",
                    "max_allowed_days": 90,
                    "requested_days": lt,
                    "escalation": "request_engineering_change_order"
                }
    return None


class MasterDataLeadtimeAgent:
    """Production Google ADK Agent class conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3-pro-preview"):
        self.name = "master_data_leadtime_steward"
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
        """Executes autonomous master data drift audit and self-healing scenario against fixtures."""
        findings = []
        actions_taken = []

        # 1. Detect lead-time drift anomalies
        drifts = self.execute_tool("query_leadtime_drift_anomalies", min_drift_days=10)
        if drifts.get("total", 0) > 0:
            findings.append({"domain": "leadtime_drifts", "records": drifts["rows"]})

        # 2. Detect CubiScan 3D dimension discrepancies
        dimensions = self.execute_tool("query_cubiscan_dimension_discrepancies", min_volume_variance_pct=15.0)
        if dimensions.get("total", 0) > 0:
            findings.append({"domain": "dimension_discrepancies", "records": dimensions["rows"]})

        # 3. Check vendor master compliance
        vendors = self.execute_tool("query_vendor_master_integrity")
        if vendors.get("total", 0) > 0:
            findings.append({"domain": "vendor_compliance", "records": vendors["rows"]})

        # 4. Self-heal material master if drift detected
        if drifts.get("total", 0) > 0:
            drift_item = drifts["rows"][0]
            heal_res = self.execute_tool(
                "action_heal_material_leadtime",
                material_id=drift_item["material_id"],
                plant=drift_item["plant"],
                planned_delivery_leadtime_days=drift_item["actual_historical_leadtime_days"],
                rationale=f"Auto-heal {drift_item['leadtime_drift_days']}-day drift between planned and empirical vendor lead time.",
                idempotency_key=f"HEAL-{drift_item['material_id']}-20261016"
            )
            actions_taken.append(heal_res)

        # 5. Remediate packaging dimensions if 3D scan mismatch detected
        if dimensions.get("total", 0) > 0:
            scan_item = dimensions["rows"][0]
            dim_res = self.execute_tool(
                "action_remediate_cubiscan_dimensions",
                material_id=scan_item["material_id"],
                plant=scan_item["scanned_plant"],
                corrected_length_cm=scan_item["cubiscan_length_cm"],
                corrected_width_cm=scan_item["cubiscan_width_cm"],
                corrected_height_cm=scan_item["cubiscan_height_cm"],
                corrected_weight_kg=scan_item["cubiscan_weight_kg"],
                rationale=f"Remediate {scan_item['volume_discrepancy_pct']}% packaging volume mismatch to eliminate carrier freight surcharges.",
                idempotency_key=f"DIM-{scan_item['material_id']}-20261016"
            )
            actions_taken.append(dim_res)

        return {
            "agent": self.name,
            "status": "success",
            "findings_count": len(findings),
            "findings": findings,
            "actions_executed": actions_taken,
            "summary": (
                f"Master Data Steward audited SAP Material Master and 3D CubiScan sensors: "
                f"calibrated {len(actions_taken)} discrepancies and updated ERP records."
            )
        }

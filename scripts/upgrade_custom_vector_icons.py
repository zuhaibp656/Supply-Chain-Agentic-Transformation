#!/usr/bin/env python3
"""
Replace uniform `✦` purple Agent boxes and Unicode Persona/Sub-Pillar emojis across the
Supply Chain Agentic Transformation Portal with 140 bespoke, static, duotone architectural
vector SVGs (60 AI Agents + 60 Human Personas + 20 Sub-Pillars) aligned with the portal's
CAD / blueprint / glassy design language in both Dark Mode and Light Mode.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ==============================================================================
# 1. 60 BESPOKE AI AGENT VECTOR SVGs (28x28 coordinate space, static, duotone)
#    Uses `currentColor` for primary structural stroke and `var(--ic-accent)` for
#    duotone fills & precision telemetry highlights.
# ==============================================================================
AGENT_VECTOR_SVGS: dict[str, str] = {
    # --- 01 · Planning & Strategy : Demand Forecasting ---
    # 1. Demand Sensing Agent: Live POS waveform + concentric radar sensor pulse
    "demand_sensing_agent": (
        '<circle cx="19.5" cy="9.5" r="5" fill="var(--ic-accent)" fill-opacity="0.22" stroke="var(--ic-accent)" stroke-width="1.5"/>'
        '<circle cx="19.5" cy="9.5" r="2" fill="var(--ic-accent)"/>'
        '<path d="M4.5 19.5L8.5 15.5L12 18L16 11.5L19.5 14L23.5 8.5" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M4.5 22.5H23.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" opacity="0.55"/>'
    ),
    # 2. Forecast Reconciliation (cpfr_sync_agent): Dual converging streams locking into consensus diamond
    "cpfr_sync_agent": (
        '<path d="M4.5 8.5H10.5L14 14L10.5 19.5H4.5" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M23.5 8.5H17.5L14 14L17.5 19.5H23.5" fill="none" stroke="var(--ic-accent)" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>'
        '<polygon points="14,9.5 18.5,14 14,18.5 9.5,14" fill="var(--ic-accent)" fill-opacity="0.28" stroke="currentColor" stroke-width="1.75"/>'
        '<circle cx="14" cy="14" r="1.7" fill="var(--ic-accent)"/>'
    ),
    # 3. NPI Demand Profiler: Launch S-curve + 3 analog lookalike cluster nodes
    "npi_demand_profiler": (
        '<path d="M5 21.5C9.5 21.5 10.5 17 13.5 13C16.5 9 18.5 7 23 6.5" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>'
        '<circle cx="8" cy="11" r="2.1" fill="var(--ic-accent)" fill-opacity="0.3" stroke="var(--ic-accent)" stroke-width="1.4"/>'
        '<circle cx="12.5" cy="8" r="1.8" fill="var(--ic-accent)" fill-opacity="0.3" stroke="var(--ic-accent)" stroke-width="1.4"/>'
        '<polygon points="22.5,4.8 23.6,7.2 26,7.6 24.1,9.3 24.6,11.7 22.5,10.4 20.4,11.7 20.9,9.3 19,7.6 21.4,7.2" fill="var(--ic-accent)"/>'
    ),
    # --- 01 · Planning & Strategy : Trade Promotion ---
    # 4. Promo ROI Simulator: Retail promo tag + baseline vs. incremental uplift bars
    "promo_lift_simulator": (
        '<path d="M4.5 13.2V6.5H11.2L17.8 13.1L11.1 19.8L4.5 13.2Z" fill="var(--ic-accent)" fill-opacity="0.2" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>'
        '<circle cx="8" cy="10" r="1.3" fill="currentColor"/>'
        '<rect x="16.5" y="16" width="2.8" height="6.5" rx="1" fill="currentColor" opacity="0.45"/>'
        '<rect x="20.7" y="9.5" width="3" height="13" rx="1" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.2"/>'
        '<path d="M19.8 7.5L22.2 5.2L24.6 7.5" fill="none" stroke="var(--ic-accent)" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 5. JBP Negotiation Agent: Dual margin/volume Pareto equalizer sliders
    "field_beat_distributor_sync_agent": (
        '<line x1="5" y1="9.5" x2="23" y2="9.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>'
        '<line x1="5" y1="18.5" x2="23" y2="18.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>'
        '<rect x="9" y="6.7" width="4.4" height="5.6" rx="1.5" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.5"/>'
        '<rect x="15" y="15.7" width="4.4" height="5.6" rx="1.5" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.5"/>'
        '<path d="M11.2 12.5L17.2 15.5" stroke="var(--ic-accent)" stroke-width="1.5" stroke-dasharray="2 1.5"/>'
    ),
    # 6. Deduction Audit Agent: Audit magnifier over invoice lines + check seal
    "trade_scheme_claims_reconciler": (
        '<rect x="5" y="5" width="12.5" height="16.5" rx="2" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.65"/>'
        '<line x1="8" y1="9.2" x2="14.5" y2="9.2" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>'
        '<line x1="8" y1="12.8" x2="12.5" y2="12.8" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>'
        '<circle cx="17.8" cy="16.8" r="4.5" fill="var(--bg-card, #0f172a)" stroke="var(--ic-accent)" stroke-width="1.8"/>'
        '<path d="M16 16.8L17.3 18.1L19.8 15.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
        '<line x1="21.1" y1="20.1" x2="23.8" y2="22.8" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round"/>'
    ),
    # --- 01 · Planning & Strategy : S&OP / IBP ---
    # 7. Consensus & Gap Agent (sop_scenario_weaver): 3 branching scenario paths from root node
    "sop_scenario_weaver": (
        '<circle cx="6.5" cy="14" r="2.6" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.6"/>'
        '<path d="M9.1 14C13 14 13.5 7.5 18.5 7.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="2.2 1.8"/>'
        '<path d="M9.1 14H19" fill="none" stroke="var(--ic-accent)" stroke-width="2.1"/>'
        '<path d="M9.1 14C13 14 13.5 20.5 18.5 20.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="2.2 1.8"/>'
        '<circle cx="21" cy="7.5" r="2" fill="none" stroke="currentColor" stroke-width="1.5"/>'
        '<polygon points="21.5,11.3 24.3,14 21.5,16.7 18.7,14" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.5"/>'
        '<circle cx="21" cy="20.5" r="2" fill="none" stroke="currentColor" stroke-width="1.5"/>'
    ),
    # 8. Digital War-Room Agent: Tactical radar crosshairs + shockwave reroute shield
    "disruption_war_room_orchestrator": (
        '<circle cx="14" cy="14" r="8.5" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.7"/>'
        '<circle cx="14" cy="14" r="4.5" fill="none" stroke="var(--ic-accent)" stroke-width="1.4" stroke-dasharray="2.5 2"/>'
        '<line x1="14" y1="4.2" x2="14" y2="8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>'
        '<line x1="14" y1="20" x2="14" y2="23.8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>'
        '<path d="M14 14L20.2 8.2" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round"/>'
        '<circle cx="18.8" cy="9.5" r="2" fill="var(--ic-accent)"/>'
    ),
    # 9. Executive Copilot: 4-quadrant command HUD + north-star compass needle
    "csco_control_tower_copilot": (
        '<rect x="5" y="5" width="7.5" height="7.5" rx="1.8" fill="var(--ic-accent)" fill-opacity="0.22" stroke="currentColor" stroke-width="1.6"/>'
        '<rect x="15.5" y="5" width="7.5" height="7.5" rx="1.8" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        '<rect x="5" y="15.5" width="7.5" height="7.5" rx="1.8" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        '<polygon points="19.2,14.5 21.2,18.2 24.5,19.2 21.2,20.2 19.2,23.8 17.2,20.2 14,19.2 17.2,18.2" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/>'
    ),
    # --- 01 · Planning & Strategy : Portfolio & SKU ---
    # 10. SKU Pruning Agent (working_capital_cash_bridge): Pareto waterfall bars + tail cutoff gate
    "working_capital_cash_bridge": (
        '<rect x="4.8" y="6.5" width="3.4" height="15" rx="1" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.4"/>'
        '<rect x="9.8" y="10" width="3.4" height="11.5" rx="1" fill="var(--ic-accent)" fill-opacity="0.55" stroke="currentColor" stroke-width="1.4"/>'
        '<line x1="15.5" y1="5.5" x2="15.5" y2="22.8" stroke="var(--ic-accent)" stroke-width="1.8" stroke-dasharray="2.5 2"/>'
        '<rect x="17.8" y="16.5" width="2.6" height="5" rx="0.8" fill="none" stroke="currentColor" stroke-width="1.3" opacity="0.55"/>'
        '<rect x="21.5" y="18.5" width="2.6" height="3" rx="0.8" fill="none" stroke="currentColor" stroke-width="1.3" opacity="0.55"/>'
        '<path d="M18 9.5L23 14.5M23 9.5L18 14.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>'
    ),
    # 11. PIPO Run-Out Agent (eco_cutover_orchestrator): Phase-out curve crossing phase-in curve
    "eco_cutover_orchestrator": (
        '<path d="M4.5 8C10.5 8 13.5 20 23.5 20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-dasharray="3 2" stroke-linecap="round"/>'
        '<path d="M4.5 20C10.5 20 13.5 8 23.5 8" fill="none" stroke="var(--ic-accent)" stroke-width="2.1" stroke-linecap="round"/>'
        '<circle cx="14" cy="14" r="3" fill="var(--ic-accent)" fill-opacity="0.3" stroke="currentColor" stroke-width="1.7"/>'
        '<path d="M20.8 5.8L23.6 8L20.8 10.2" fill="none" stroke="var(--ic-accent)" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 12. Cost-to-Serve Diagnostic (network_twin_architect): Central DC hub + weighted lane spokes
    "network_twin_architect": (
        '<line x1="14" y1="14" x2="6.5" y2="7.5" stroke="currentColor" stroke-width="1.6"/>'
        '<line x1="14" y1="14" x2="22" y2="8" stroke="var(--ic-accent)" stroke-width="2"/>'
        '<line x1="14" y1="14" x2="7" y2="21" stroke="currentColor" stroke-width="1.6"/>'
        '<line x1="14" y1="14" x2="21.5" y2="20.5" stroke="var(--ic-accent)" stroke-width="2"/>'
        '<rect x="10.5" y="10.5" width="7" height="7" rx="2" fill="var(--ic-accent)" fill-opacity="0.3" stroke="currentColor" stroke-width="1.8"/>'
        '<circle cx="6.5" cy="7.5" r="2.1" fill="currentColor"/>'
        '<circle cx="22" cy="8" r="2.3" fill="var(--ic-accent)"/>'
        '<circle cx="7" cy="21" r="2.1" fill="currentColor"/>'
        '<circle cx="21.5" cy="20.5" r="2.3" fill="var(--ic-accent)"/>'
    ),
    # --- 02 · Sourcing & Procurement : Supplier Network ---
    # 13. Disruption Sensing Agent (tier_n_risk_sentinel): Multi-tier BOM graph (Tier 1 -> Tier 2 -> Tier 3 alert)
    "tier_n_risk_sentinel": (
        '<circle cx="14" cy="6.2" r="2.4" fill="currentColor"/>'
        '<line x1="14" y1="8.6" x2="8.5" y2="13.8" stroke="currentColor" stroke-width="1.6"/>'
        '<line x1="14" y1="8.6" x2="19.5" y2="13.8" stroke="currentColor" stroke-width="1.6"/>'
        '<circle cx="8.5" cy="15.2" r="2.2" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        '<circle cx="19.5" cy="15.2" r="2.2" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        '<line x1="19.5" y1="17.4" x2="22" y2="21.2" stroke="var(--ic-accent)" stroke-width="1.8"/>'
        '<polygon points="22,19.2 24.8,24 19.2,24" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/>'
    ),
    # 14. Onboarding & Qual. Agent (supplier_quality_sentinel): Vendor shield + automated compliance seal
    "supplier_quality_sentinel": (
        '<path d="M14 4.5L21.5 7.5V13.8C21.5 18.5 18.3 21.8 14 23.5C9.7 21.8 6.5 18.5 6.5 13.8V7.5L14 4.5Z" fill="var(--ic-accent)" fill-opacity="0.22" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round"/>'
        '<path d="M10.5 14.2L13 16.7L18 11.5" fill="none" stroke="var(--ic-accent)" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 15. ESG & Scope 3 Auditor (carbon_scope3_ledger): Botanical leaf circuit + CO2 ledger blocks
    "carbon_scope3_ledger": (
        '<path d="M7 21C7 13 12 7 21.5 6.5C21.5 15.5 16.5 21 9.5 21H7Z" fill="var(--ic-accent)" fill-opacity="0.24" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round"/>'
        '<path d="M7 21C11.5 16.5 15 13 19 9.5" fill="none" stroke="var(--ic-accent)" stroke-width="1.8" stroke-linecap="round"/>'
        '<circle cx="15" cy="13.2" r="1.6" fill="currentColor"/>'
    ),
    # --- 02 · Sourcing & Procurement : Material & Packaging ---
    # 16. Commodity Index Advisor: Candlestick price action + hedge band lock line
    "commodity_index_advisor": (
        '<line x1="8" y1="6.5" x2="8" y2="21.5" stroke="currentColor" stroke-width="1.5"/>'
        '<rect x="6.3" y="10" width="3.4" height="7" rx="0.8" fill="currentColor"/>'
        '<line x1="14" y1="5.5" x2="14" y2="19.5" stroke="currentColor" stroke-width="1.5"/>'
        '<rect x="12.3" y="8" width="3.4" height="6.5" rx="0.8" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.2"/>'
        '<line x1="20" y1="8.5" x2="20" y2="22.5" stroke="currentColor" stroke-width="1.5"/>'
        '<rect x="18.3" y="12.5" width="3.4" height="6.5" rx="0.8" fill="var(--ic-accent)" fill-opacity="0.4" stroke="currentColor" stroke-width="1.2"/>'
        '<line x1="4.5" y1="15.5" x2="23.5" y2="15.5" stroke="var(--ic-accent)" stroke-width="1.7" stroke-dasharray="2.5 2"/>'
    ),
    # 17. Dynamic Should-Cost Agent: Clean-sheet stacked cost decomposition + precision caliper
    "rfq_should_cost_agent": (
        '<rect x="5.5" y="6" width="8.5" height="4" rx="1" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.4"/>'
        '<rect x="5.5" y="11.8" width="8.5" height="4.5" rx="1" fill="var(--ic-accent)" fill-opacity="0.4" stroke="currentColor" stroke-width="1.4"/>'
        '<rect x="5.5" y="18" width="8.5" height="4" rx="1" fill="none" stroke="currentColor" stroke-width="1.4"/>'
        '<path d="M17.5 6.5H22V21.5H17.5" fill="none" stroke="var(--ic-accent)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
        '<line x1="17.5" y1="14" x2="22" y2="14" stroke="currentColor" stroke-width="1.6"/>'
    ),
    # 18. Sustainable Packaging Agent: Isometric carton wireframe + down-gauge eco loop
    "sustainable_packaging_agent": (
        '<polygon points="14,5 22,9.5 14,14 6,9.5" fill="var(--ic-accent)" fill-opacity="0.26" stroke="currentColor" stroke-width="1.65" stroke-linejoin="round"/>'
        '<polygon points="6,9.5 14,14 14,22.5 6,18" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linejoin="round"/>'
        '<polygon points="22,9.5 14,14 14,22.5 22,18" fill="var(--ic-accent)" fill-opacity="0.14" stroke="currentColor" stroke-width="1.65" stroke-linejoin="round"/>'
        '<path d="M10 7.2L18 11.7" stroke="var(--ic-accent)" stroke-width="1.6" stroke-linecap="round"/>'
    ),
    # --- 02 · Sourcing & Procurement : Contract & PO Mgmt ---
    # 19. Contract Leakage Agent (tariff_esg_agent): Master contract + volume rebate tier steps
    "tariff_esg_agent": (
        '<rect x="5" y="5" width="12" height="17.5" rx="1.8" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.65"/>'
        '<line x1="8" y1="9" x2="14" y2="9" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>'
        '<line x1="8" y1="12.5" x2="12.5" y2="12.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>'
        '<path d="M15 21.5H18.5V17.5H21.5V13.5H24" fill="none" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="23.2" cy="10.2" r="1.8" fill="var(--ic-accent)"/>'
    ),
    # 20. PO Expediting Agent (master_data_leadtime_steward): Calibrated lead-time clock + fast-forward chevrons
    "master_data_leadtime_steward": (
        '<circle cx="12.5" cy="14" r="7.5" fill="var(--ic-accent)" fill-opacity="0.18" stroke="currentColor" stroke-width="1.75"/>'
        '<path d="M12.5 9.8V14L15.5 15.8" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M19.5 10.5L23 14L19.5 17.5" fill="none" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 21. Three-Way Match Dispute: 3 vertices (PO, GRN, Invoice) locking into central match node
    "three_way_match_dispute": (
        '<polygon points="14,6.5 22,20.5 6,20.5" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
        '<rect x="11.6" y="4.2" width="4.8" height="4.8" rx="1.2" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.4"/>'
        '<rect x="3.8" y="18.2" width="4.8" height="4.8" rx="1.2" fill="var(--bg-card, #0f172a)" stroke="currentColor" stroke-width="1.4"/>'
        '<rect x="19.4" y="18.2" width="4.8" height="4.8" rx="1.2" fill="var(--bg-card, #0f172a)" stroke="currentColor" stroke-width="1.4"/>'
        '<circle cx="14" cy="15.5" r="2.1" fill="var(--ic-accent)"/>'
    ),
    # --- 03 · Manufacturing & Production : Production Scheduling ---
    # 22. Changeover Optimizer (finite_production_scheduler): Sequenced Gantt campaign blocks
    "finite_production_scheduler": (
        '<rect x="4.5" y="6.5" width="9.5" height="3.8" rx="1.2" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.4"/>'
        '<rect x="11" y="12.1" width="10" height="3.8" rx="1.2" fill="var(--ic-accent)" fill-opacity="0.45" stroke="currentColor" stroke-width="1.4"/>'
        '<rect x="7.5" y="17.7" width="15.5" height="3.8" rx="1.2" fill="none" stroke="currentColor" stroke-width="1.5"/>'
        '<line x1="15.8" y1="5" x2="15.8" y2="23" stroke="var(--ic-accent)" stroke-width="1.5" stroke-dasharray="2 2"/>'
    ),
    # 23. Disruption Re-sequencer (line_schedule_optimizer): Blocked line bypassed via live switch-track
    "line_schedule_optimizer": (
        '<line x1="4.5" y1="10" x2="12" y2="10" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
        '<path d="M15.5 8.2L19 11.8M19 8.2L15.5 11.8" stroke="var(--ic-accent)" stroke-width="1.8" stroke-linecap="round"/>'
        '<path d="M9.5 10C12 10 12.5 18.5 15.5 18.5H23" fill="none" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round"/>'
        '<path d="M20.5 16L23.2 18.5L20.5 21" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 24. Labor & Line Balancing: 3 balanced operator station columns on leveling beam
    "labor_line_balancing_agent": (
        '<line x1="5" y1="19.5" x2="23" y2="19.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
        '<polygon points="14,19.5 16.8,23.2 11.2,23.2" fill="var(--ic-accent)"/>'
        '<rect x="6" y="10" width="3.8" height="7.5" rx="1.2" fill="var(--ic-accent)" fill-opacity="0.35" stroke="currentColor" stroke-width="1.4"/>'
        '<rect x="12.1" y="9" width="3.8" height="8.5" rx="1.2" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.4"/>'
        '<rect x="18.2" y="10" width="3.8" height="7.5" rx="1.2" fill="var(--ic-accent)" fill-opacity="0.35" stroke="currentColor" stroke-width="1.4"/>'
    ),
    # --- 03 · Manufacturing & Production : Capacity Planning ---
    # 25. Bottleneck Diagnostic (predictive_oee_sentinel): Telemetry pulse inside industrial machine ring
    "predictive_oee_sentinel": (
        '<rect x="5" y="6" width="18" height="16" rx="3" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.75"/>'
        '<path d="M7.5 14H10.5L12.3 9.2L15.2 18.8L17.2 12.5L18.8 14H20.5" fill="none" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 26. Co-Packer Allocation: Primary plant distributing optimal split loads to 2 CMO nodes
    "copacker_allocation_agent": (
        '<path d="M5 21V11.5L9 14V11.5L13 14V21H5Z" fill="var(--ic-accent)" fill-opacity="0.28" stroke="currentColor" stroke-width="1.65" stroke-linejoin="round"/>'
        '<path d="M13.5 15.5L18.5 10" stroke="var(--ic-accent)" stroke-width="1.75" stroke-linecap="round"/>'
        '<path d="M13.5 17.5L18.5 19.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
        '<rect x="19" y="7" width="4.5" height="4.5" rx="1" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.4"/>'
        '<rect x="19" y="17.2" width="4.5" height="4.5" rx="1" fill="none" stroke="currentColor" stroke-width="1.4"/>'
    ),
    # 27. CapEx Simulator: Plant blueprint grid + stochastic Monte Carlo confidence fan
    "capex_simulator_agent": (
        '<path d="M5.5 21.5V6.5M5.5 21.5H23" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>'
        '<path d="M6 19.5L22 7.5L22 18.5Z" fill="var(--ic-accent)" fill-opacity="0.24"/>'
        '<path d="M6 19.5L22 7.5" stroke="var(--ic-accent)" stroke-width="1.6" stroke-dasharray="2.5 1.8"/>'
        '<path d="M6 19.5L22 13" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>'
        '<path d="M6 19.5L22 18.5" stroke="var(--ic-accent)" stroke-width="1.6" stroke-dasharray="2.5 1.8"/>'
    ),
    # --- 03 · Manufacturing & Production : Quality & Compliance ---
    # 28. Visual Defect Triager (inline_yield_guardian): Vision camera reticle + laser scan over unit
    "inline_yield_guardian": (
        '<path d="M6 9.5V6.5H9M22 9.5V6.5H19M6 18.5V21.5H9M22 18.5V21.5H19" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>'
        '<rect x="10.2" y="9.8" width="7.6" height="8.4" rx="1.6" fill="var(--ic-accent)" fill-opacity="0.25" stroke="currentColor" stroke-width="1.6"/>'
        '<line x1="4.8" y1="14" x2="23.2" y2="14" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round"/>'
    ),
    # 29. Batch Record Auditor: Electronic batch record stack + verified release checkmark
    "batch_record_auditor": (
        '<rect x="7.5" y="4.8" width="12.5" height="16" rx="1.8" fill="none" stroke="currentColor" stroke-width="1.4" opacity="0.5"/>'
        '<rect x="5.5" y="7.2" width="13" height="16" rx="1.8" fill="var(--ic-accent)" fill-opacity="0.2" stroke="currentColor" stroke-width="1.7"/>'
        '<path d="M9.2 15.2L11.4 17.4L15.4 12.8" fill="none" stroke="var(--ic-accent)" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 30. RCA & CAPA Copilot (scrap_defect_root_cause_agent): Ishikawa fishbone causal diagram
    "scrap_defect_root_cause_agent": (
        '<line x1="4.5" y1="14" x2="20.5" y2="14" stroke="currentColor" stroke-width="1.85" stroke-linecap="round"/>'
        '<line x1="8" y1="8" x2="11.5" y2="14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
        '<line x1="14" y1="8" x2="17.5" y2="14" stroke="var(--ic-accent)" stroke-width="1.8" stroke-linecap="round"/>'
        '<line x1="8" y1="20" x2="11.5" y2="14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
        '<line x1="14" y1="20" x2="17.5" y2="14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
        '<polygon points="20.5,10.8 24.2,14 20.5,17.2" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>'
    ),
    # --- 04 · Inventory & Warehousing : Positioning & Optimization ---
    # 31. Safety Stock Agent (meio_safety_stock_agent): 3-tier multi-echelon buffer pyramid
    "meio_safety_stock_agent": (
        '<rect x="11" y="5" width="6" height="4.5" rx="1.2" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.5"/>'
        '<line x1="14" y1="9.5" x2="9" y2="13" stroke="currentColor" stroke-width="1.5"/>'
        '<line x1="14" y1="9.5" x2="19" y2="13" stroke="currentColor" stroke-width="1.5"/>'
        '<rect x="6" y="13" width="6" height="4.2" rx="1" fill="var(--ic-accent)" fill-opacity="0.35" stroke="currentColor" stroke-width="1.4"/>'
        '<rect x="16" y="13" width="6" height="4.2" rx="1" fill="var(--ic-accent)" fill-opacity="0.35" stroke="currentColor" stroke-width="1.4"/>'
        '<line x1="5" y1="21.2" x2="23" y2="21.2" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round"/>'
    ),
    # 32. SLOB Disposition Agent: Aging inventory hourglass + value-salvage arrow
    "slob_disposition_agent": (
        '<path d="M7.5 6H17.5M7.5 22H17.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
        '<path d="M8.5 6L12.5 14L8.5 22M16.5 6L12.5 14L16.5 22" fill="var(--ic-accent)" fill-opacity="0.2" stroke="currentColor" stroke-width="1.65" stroke-linejoin="round"/>'
        '<path d="M17.5 14H23.2M20.8 11.5L23.4 14L20.8 16.5" fill="none" stroke="var(--ic-accent)" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 33. Inter-Facility Rebalancer (crossdock_transfer_orchestrator): Dual DC hubs + bidirectional transfer
    "crossdock_transfer_orchestrator": (
        '<rect x="4.5" y="9" width="6" height="10" rx="1.4" fill="var(--ic-accent)" fill-opacity="0.26" stroke="currentColor" stroke-width="1.6"/>'
        '<rect x="17.5" y="9" width="6" height="10" rx="1.4" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        '<path d="M11.8 11.5H16.2M14.6 9.8L16.5 11.5L14.6 13.2" fill="none" stroke="var(--ic-accent)" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M16.2 16.5H11.8M13.4 14.8L11.5 16.5L13.4 18.2" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # --- 04 · Inventory & Warehousing : Warehouse Operations ---
    # 34. Dynamic Slotting Agent (warehouse_slotting_agent): 3-level rack with highlighted Golden Zone slot
    "warehouse_slotting_agent": (
        '<line x1="6" y1="5.5" x2="6" y2="22.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
        '<line x1="22" y1="5.5" x2="22" y2="22.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
        '<line x1="6" y1="10.5" x2="22" y2="10.5" stroke="currentColor" stroke-width="1.5"/>'
        '<line x1="6" y1="17" x2="22" y2="17" stroke="currentColor" stroke-width="1.5"/>'
        '<rect x="8.5" y="11.8" width="5" height="4" rx="0.9" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.3"/>'
        '<rect x="14.8" y="11.8" width="4.7" height="4" rx="0.9" fill="var(--ic-accent)" fill-opacity="0.45" stroke="currentColor" stroke-width="1.3"/>'
    ),
    # 35. Dock-to-Stock Agent: Dock bay portal + direct fast-track putaway arrow
    "dock_to_stock_agent": (
        '<path d="M6 21.5V6.5H22V21.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
        '<rect x="9.5" y="13.5" width="9" height="8" rx="1.2" fill="var(--ic-accent)" fill-opacity="0.24" stroke="currentColor" stroke-width="1.5"/>'
        '<path d="M14 19.5V9.5M11.2 12.2L14 9.2L16.8 12.2" fill="none" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 36. Wave Fulfillment Copilot: Synchronized pick-wave crests + carrier cutoff lock
    "wave_fulfillment_copilot": (
        '<path d="M4.5 11.5C7 8.5 9.5 8.5 12 11.5C14.5 14.5 17 14.5 19.5 11.5" fill="none" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round"/>'
        '<path d="M4.5 17C7 14 9.5 14 12 17C14.5 20 17 20 19.5 17" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"/>'
        '<line x1="22.2" y1="6.5" x2="22.2" y2="21.5" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round"/>'
        '<circle cx="22.2" cy="8.5" r="1.8" fill="currentColor"/>'
    ),
    # --- 04 · Inventory & Warehousing : Omnichannel Visibility ---
    # 37. Phantom Inventory Sensor: Shelf items + dashed "ghost" SKU slot flagged by sensor
    "planogram_merchandising_vision_auditor": (
        '<line x1="4.5" y1="20" x2="23.5" y2="20" stroke="currentColor" stroke-width="1.85" stroke-linecap="round"/>'
        '<rect x="5.8" y="11" width="4.2" height="7.5" rx="1" fill="currentColor" opacity="0.7"/>'
        '<rect x="11.8" y="9.5" width="4.8" height="9" rx="1" fill="var(--ic-accent)" fill-opacity="0.22" stroke="var(--ic-accent)" stroke-width="1.6" stroke-dasharray="2.2 1.6"/>'
        '<rect x="18.4" y="12" width="3.8" height="6.5" rx="1" fill="currentColor" opacity="0.7"/>'
        '<circle cx="14.2" cy="6.2" r="1.6" fill="var(--ic-accent)"/>'
    ),
    # 38. SFS / BOPIS Sourcing (atp_order_promising_agent): Order diamond routing cleanly to optimal store/DC
    "atp_order_promising_agent": (
        '<polygon points="7.5,10 11,14 7.5,18 4,14" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.5"/>'
        '<path d="M11 14H18.5" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round"/>'
        '<path d="M11 14L17.5 7.8" stroke="currentColor" stroke-width="1.3" stroke-dasharray="2 2"/>'
        '<rect x="18.8" y="10.8" width="5" height="6.4" rx="1.2" fill="var(--ic-accent)" fill-opacity="0.28" stroke="currentColor" stroke-width="1.6"/>'
        '<rect x="18.8" y="4.8" width="4.2" height="4.2" rx="1" fill="none" stroke="currentColor" stroke-width="1.3" opacity="0.55"/>'
    ),
    # 39. Returns Triage Agent: Inbound return box sorted into Grade-A fast restock lane
    "returns_triage_agent": (
        '<rect x="4.8" y="10.2" width="6.4" height="6.4" rx="1.2" fill="var(--ic-accent)" fill-opacity="0.25" stroke="currentColor" stroke-width="1.6"/>'
        '<path d="M11.2 13.4L16.5 8.5H22.8" fill="none" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M11.2 13.4L16.5 18.5H21.5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="2 2" stroke-linecap="round"/>'
        '<path d="M20.5 6.4L23 8.5L20.5 10.6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # --- 05 · Distribution & Logistics : First & Mid-Mile ---
    # 40. Load Consolidation: Semi-trailer filled with high-density 3D cargo blocks
    "load_consolidation_agent": (
        '<rect x="4.2" y="8" width="14.5" height="10" rx="1.5" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.7"/>'
        '<path d="M18.7 11.5H22.2L23.8 14.5V18H18.7V11.5Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
        '<rect x="6" y="10" width="4.8" height="6.2" rx="0.7" fill="var(--ic-accent)"/>'
        '<rect x="12" y="10" width="4.8" height="2.8" rx="0.6" fill="currentColor" opacity="0.8"/>'
        '<rect x="12" y="13.6" width="4.8" height="2.6" rx="0.6" fill="var(--ic-accent)" fill-opacity="0.6"/>'
        '<circle cx="8.5" cy="19.8" r="1.8" fill="currentColor"/>'
        '<circle cx="20.8" cy="19.8" r="1.8" fill="currentColor"/>'
    ),
    # 41. Yard Disruption Agent (yard_dock_sequencer): Sequenced yard lanes into numbered dock slots
    "yard_dock_sequencer": (
        '<line x1="20.5" y1="5.5" x2="20.5" y2="22.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
        '<rect x="15.5" y="7" width="5" height="3.6" rx="0.8" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.3"/>'
        '<rect x="15.5" y="12.2" width="5" height="3.6" rx="0.8" fill="none" stroke="currentColor" stroke-width="1.3"/>'
        '<rect x="15.5" y="17.4" width="5" height="3.6" rx="0.8" fill="var(--ic-accent)" fill-opacity="0.35" stroke="currentColor" stroke-width="1.3"/>'
        '<path d="M5 14C9 14 10 8.8 14.5 8.8" fill="none" stroke="var(--ic-accent)" stroke-width="1.9" stroke-linecap="round"/>'
        '<circle cx="5.5" cy="14" r="1.8" fill="currentColor"/>'
    ),
    # 42. Cold-Chain Auditor: Precision thermometer + geometric cold-chain crystal
    "cold_chain_auditor": (
        '<path d="M9.5 6.8V16.2C8.2 16.9 7.5 18.2 7.5 19.6C7.5 21.6 9.1 23.2 11.1 23.2C13.1 23.2 14.7 21.6 14.7 19.6C14.7 18.2 14 16.9 12.7 16.2V6.8C12.7 5.9 12 5.2 11.1 5.2C10.2 5.2 9.5 5.9 9.5 6.8Z" fill="var(--ic-accent)" fill-opacity="0.2" stroke="currentColor" stroke-width="1.65"/>'
        '<circle cx="11.1" cy="19.6" r="1.8" fill="var(--ic-accent)"/>'
        '<path d="M19.5 7.5V15.5M16 11.5H23M17 9L22 14M22 9L17 14" stroke="var(--ic-accent)" stroke-width="1.6" stroke-linecap="round"/>'
    ),
    # --- 05 · Distribution & Logistics : Store Replenishment ---
    # 43. Aisle-Aligned Pallet: Pallet base + aisle-sequenced layer tiers
    "aisle_aligned_pallet_agent": (
        '<line x1="4.8" y1="21.5" x2="23.2" y2="21.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
        '<line x1="7.5" y1="19.5" x2="7.5" y2="21.5" stroke="currentColor" stroke-width="2"/>'
        '<line x1="14" y1="19.5" x2="14" y2="21.5" stroke="currentColor" stroke-width="2"/>'
        '<line x1="20.5" y1="19.5" x2="20.5" y2="21.5" stroke="currentColor" stroke-width="2"/>'
        '<rect x="6.2" y="15" width="15.6" height="4" rx="0.9" fill="currentColor" opacity="0.7"/>'
        '<rect x="7.2" y="10.4" width="13.6" height="3.8" rx="0.9" fill="var(--ic-accent)" fill-opacity="0.45" stroke="currentColor" stroke-width="1.3"/>'
        '<rect x="8.5" y="6" width="11" height="3.6" rx="0.9" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.3"/>'
    ),
    # 44. Store Capacity Agent: Store backroom container + cubic cap threshold meter
    "store_capacity_agent": (
        '<path d="M5.5 10.5L14 5.5L22.5 10.5V21.5H5.5V10.5Z" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>'
        '<line x1="8" y1="13" x2="20" y2="13" stroke="var(--ic-accent)" stroke-width="1.9" stroke-dasharray="2.4 1.8"/>'
        '<rect x="8.8" y="15.2" width="10.4" height="4.2" rx="0.9" fill="var(--ic-accent)"/>'
    ),
    # 45. Curfew Orchestrator (port_drayage_orchestrator): Urban skyline + timed quiet-delivery arc
    "port_drayage_orchestrator": (
        '<path d="M5 21.5V12.5H9.5V21.5M9.5 21.5V8.5H15V21.5M15 21.5V14.5H19.5V21.5" fill="var(--ic-accent)" fill-opacity="0.2" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
        '<circle cx="20.2" cy="8.2" r="3.6" fill="var(--bg-card, #0f172a)" stroke="var(--ic-accent)" stroke-width="1.7"/>'
        '<path d="M20.2 6.4V8.4L21.6 9.3" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>'
    ),
    # --- 05 · Distribution & Logistics : Last-Mile Delivery ---
    # 46. Geocoding Intelligence: Rooftop GPS pin locked into precision target grid
    "geocoding_intelligence_agent": (
        '<ellipse cx="14" cy="20.8" rx="6.8" ry="2.2" fill="var(--ic-accent)" fill-opacity="0.25" stroke="var(--ic-accent)" stroke-width="1.4"/>'
        '<path d="M14 20C14 20 19.5 14.5 19.5 10.5C19.5 7.5 17 5 14 5C11 5 8.5 7.5 8.5 10.5C8.5 14.5 14 20 14 20Z" fill="var(--ic-accent)" fill-opacity="0.28" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round"/>'
        '<circle cx="14" cy="10.5" r="2.1" fill="currentColor"/>'
    ),
    # 47. Courier Allocation (multimodal_mode_shift_agent): Parcel hub switching across 3 speed/cost modes
    "multimodal_mode_shift_agent": (
        '<rect x="4.5" y="10.5" width="6.5" height="7" rx="1.3" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.5"/>'
        '<path d="M11 14L17.5 7.8H22.8" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>'
        '<path d="M11 14H23" fill="none" stroke="var(--ic-accent)" stroke-width="2.1" stroke-linecap="round"/>'
        '<path d="M11 14L17.5 20.2H22.8" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>'
        '<circle cx="23" cy="14" r="1.9" fill="var(--ic-accent)"/>'
    ),
    # 48. Delivery Exception Copilot (otif_penalty_shield): OTIF SLA shield + proactive ETA pulse
    "otif_penalty_shield": (
        '<path d="M12.5 5L19.5 7.8V13.5C19.5 17.8 16.5 21 12.5 22.6C8.5 21 5.5 17.8 5.5 13.5V7.8L12.5 5Z" fill="var(--ic-accent)" fill-opacity="0.22" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>'
        '<path d="M9.5 13.8L11.6 15.9L15.8 11.4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M21 8.5C22.8 10.2 22.8 13.2 21 15" fill="none" stroke="var(--ic-accent)" stroke-width="1.8" stroke-linecap="round"/>'
    ),
    # --- 05 · Distribution & Logistics : Route & Carrier ---
    # 49. Dynamic Rerouter (fleetflow_dispatch): VRP curved route bypassing blocked road hazard
    "fleetflow_dispatch": (
        '<circle cx="6.2" cy="19.5" r="2.2" fill="currentColor"/>'
        '<circle cx="21.8" cy="8.5" r="2.2" fill="var(--ic-accent)"/>'
        '<line x1="8" y1="18.2" x2="19.8" y2="9.8" stroke="currentColor" stroke-width="1.3" stroke-dasharray="2 2" opacity="0.5"/>'
        '<path d="M6.2 17.3C6.2 9.5 13 7 19.6 8.2" fill="none" stroke="var(--ic-accent)" stroke-width="2.1" stroke-linecap="round"/>'
        '<path d="M13 13.2L15.8 16M15.8 13.2L13 16" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
    ),
    # 50. Routing Guide Compliance (freight_control_tower): Tier-1/2/3 contracted cascade waterfall
    "freight_control_tower": (
        '<rect x="5" y="6" width="18" height="4" rx="1.2" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.5"/>'
        '<rect x="7.5" y="12" width="13" height="4" rx="1.2" fill="var(--ic-accent)" fill-opacity="0.38" stroke="currentColor" stroke-width="1.4"/>'
        '<rect x="10" y="18" width="8" height="4" rx="1.2" fill="none" stroke="currentColor" stroke-width="1.4"/>'
    ),
    # 51. Freight Bill Audit Agent: EDI 210 freight invoice + tariff check ruler
    "freight_bill_audit_agent": (
        '<path d="M6.5 5H17.5V22.5L15 20.8L12 22.5L9 20.8L6.5 22.5V5Z" fill="var(--ic-accent)" fill-opacity="0.18" stroke="currentColor" stroke-width="1.65" stroke-linejoin="round"/>'
        '<line x1="9.2" y1="9.5" x2="14.8" y2="9.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>'
        '<line x1="9.2" y1="13" x2="13.5" y2="13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>'
        '<circle cx="19.5" cy="15.5" r="3.8" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.4"/>'
        '<path d="M18 15.5L19.1 16.6L21.3 14.3" fill="none" stroke="#ffffff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # --- 06 · Returns & Reverse Logistics : Returns & Claims Mgmt ---
    # 52. Return Fraud Sentinel (reverse_rma_optimizer): RMA barcode + fraud firewall gate
    "reverse_rma_optimizer": (
        '<line x1="5.5" y1="8" x2="5.5" y2="20" stroke="currentColor" stroke-width="1.8"/>'
        '<line x1="8.8" y1="8" x2="8.8" y2="20" stroke="currentColor" stroke-width="1.2"/>'
        '<line x1="11.5" y1="8" x2="11.5" y2="20" stroke="currentColor" stroke-width="2"/>'
        '<path d="M18.8 7L23.5 9V14C23.5 17.5 21.4 20.2 18.8 21.5C16.2 20.2 14.1 17.5 14.1 14V9L18.8 7Z" fill="var(--ic-accent)" fill-opacity="0.28" stroke="var(--ic-accent)" stroke-width="1.7" stroke-linejoin="round"/>'
        '<line x1="17" y1="12.2" x2="20.6" y2="15.8" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>'
    ),
    # 53. Keep-It & Routing Advisor: Return decision diamond splitting into net-recovery routes
    "keep_it_routing_advisor": (
        '<polygon points="14,7.5 19.5,13 14,18.5 8.5,13" fill="var(--ic-accent)" fill-opacity="0.26" stroke="currentColor" stroke-width="1.7"/>'
        '<path d="M4.5 13H8.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>'
        '<path d="M19.5 13H23.5M21.5 10.8L23.7 13L21.5 15.2" fill="none" stroke="var(--ic-accent)" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M14 18.5V23" stroke="currentColor" stroke-width="1.6" stroke-dasharray="2 1.8" stroke-linecap="round"/>'
    ),
    # 54. OS&D Freight Claims: Damaged box corner + evidence capture frame
    "osd_freight_claims_agent": (
        '<rect x="7.5" y="8.5" width="13" height="11" rx="1.6" fill="var(--ic-accent)" fill-opacity="0.2" stroke="currentColor" stroke-width="1.65"/>'
        '<path d="M12.5 8.5L11 12.2L14.5 13.5L13 17" fill="none" stroke="var(--ic-accent)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M4.8 8.5V5.5H7.8M23.2 8.5V5.5H20.2M4.8 19.5V22.5H7.8M23.2 19.5V22.5H20.2" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>'
    ),
    # --- 06 · Returns & Reverse Logistics : Expiry & Markdowns ---
    # 55. Dynamic Markdown Agent: Electronic shelf label + stepped price-elasticity curve
    "dynamic_markdown_agent": (
        '<rect x="4.8" y="6" width="18.4" height="16" rx="2.2" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.7"/>'
        '<path d="M8 10.2H12.5V13.8H16.8V17.5H20.2" fill="none" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="20.2" cy="17.5" r="1.7" fill="currentColor"/>'
    ),
    # 56. Short-Dated Redistributor: FEFO lot timer redirecting to high-velocity outlet
    "short_dated_redistributor": (
        '<circle cx="10.8" cy="14" r="5.8" fill="var(--ic-accent)" fill-opacity="0.22" stroke="currentColor" stroke-width="1.7"/>'
        '<path d="M10.8 10.8V14L13 15.2" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
        '<path d="M16.8 11.5H23M20.5 9L23.2 11.5L20.5 14" fill="none" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M16.8 17.5H21.5" stroke="currentColor" stroke-width="1.5" stroke-dasharray="2 2" stroke-linecap="round"/>'
    ),
    # 57. Food Waste & ESG Copilot: Circular bio-recovery loop + certified credit core
    "food_waste_esg_copilot": (
        '<path d="M14 5.5C18.7 5.5 22.5 9.3 22.5 14C22.5 18.7 18.7 22.5 14 22.5C9.3 22.5 5.5 18.7 5.5 14C5.5 11.2 6.9 8.7 9 7.2" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"/>'
        '<path d="M6.2 6.8H9.5V10.1" fill="none" stroke="var(--ic-accent)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M11 16.5C11 12.5 14 10.5 17.5 10.5C17.5 14.5 15 16.8 11.8 16.8" fill="var(--ic-accent)" fill-opacity="0.35" stroke="var(--ic-accent)" stroke-width="1.5" stroke-linejoin="round"/>'
    ),
    # --- 06 · Returns & Reverse Logistics : Pallet & Tote Reclamation ---
    # 58. RTI Balance Reconciler: Nested reusable totes + RFID serialized wave
    "rti_balance_reconciler": (
        '<path d="M5.5 10H16.5L15.3 15H6.7L5.5 10Z" fill="var(--ic-accent)" fill-opacity="0.28" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
        '<path d="M5.5 16.2H16.5L15.3 21.2H6.7L5.5 16.2Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
        '<path d="M19.2 10.5C21 12.2 21 15.2 19.2 17" fill="none" stroke="var(--ic-accent)" stroke-width="1.75" stroke-linecap="round"/>'
        '<path d="M21.8 8.5C24.4 11.2 24.4 16.2 21.8 19" fill="none" stroke="var(--ic-accent)" stroke-width="1.5" stroke-linecap="round" opacity="0.75"/>'
    ),
    # 59. Milk-Run Consolidation (intermodal_rail_linehaul_agent): Closed-loop outbound + backhaul sweep circuit
    "intermodal_rail_linehaul_agent": (
        '<path d="M6.5 10.5H20.5C22.2 10.5 23.2 11.8 23.2 14" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"/>'
        '<path d="M21.5 17.5H7.5C5.8 17.5 4.8 16.2 4.8 14" fill="none" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round"/>'
        '<path d="M18.5 8.2L21 10.5L18.5 12.8" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M9.5 15.2L7 17.5L9.5 19.8" fill="none" stroke="var(--ic-accent)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
        '<rect x="12.2" y="12.4" width="3.6" height="3.2" rx="0.7" fill="var(--ic-accent)"/>'
    ),
    # 60. Sanitation & Health Agent: Reusable container + thermal sanitation droplets & sterile star
    "sanitation_health_agent": (
        '<path d="M6 12.5H20L18.5 21H7.5L6 12.5Z" fill="var(--ic-accent)" fill-opacity="0.22" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>'
        '<path d="M10.5 6.2C10.5 6.2 8.8 8.4 8.8 9.5C8.8 10.4 9.6 11.1 10.5 11.1C11.4 11.1 12.2 10.4 12.2 9.5C12.2 8.4 10.5 6.2 10.5 6.2Z" fill="var(--ic-accent)"/>'
        '<path d="M17.5 5.2V9.8M15.2 7.5H19.8" stroke="var(--ic-accent)" stroke-width="1.8" stroke-linecap="round"/>'
    ),
}


# ==============================================================================
# 2. 60 BESPOKE HUMAN PERSONA VECTOR SVGs (keyed by Persona ID; static, duotone,
#    role-relatable executive/operator instruments — zero emojis, 100% distinct
#    from one another AND 100% distinct from AGENT_VECTOR_SVGS!)
# ==============================================================================
PERSONA_VECTOR_SVGS: dict[str, str] = {
    # --- 01 · Planning & Strategy ---
    # 1. Demand Planner / Forecaster: Horizon calendar board + demand curve
    "demand_planner_forecaster": (
        '<rect x="5.5" y="6.5" width="17" height="15" rx="2" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.65"/>'
        '<line x1="5.5" y1="10.5" x2="22.5" y2="10.5" stroke="currentColor" stroke-width="1.5"/>'
        '<path d="M8.5 18L12 14.5L15.2 16.2L19.5 12.2" fill="none" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 2. Commercial Planning Lead: Interlocking commercial & supply rings
    "commercial_planning_lead": (
        '<circle cx="11.2" cy="14" r="5.2" fill="var(--ic-accent)" fill-opacity="0.2" stroke="currentColor" stroke-width="1.7"/>'
        '<circle cx="16.8" cy="14" r="5.2" fill="none" stroke="var(--ic-accent)" stroke-width="1.8"/>'
        '<circle cx="14" cy="14" r="1.4" fill="currentColor"/>'
    ),
    # 3. Brand & Innovation Manager: New-product launch diamond + milestone flag
    "brand_innovation_mgr": (
        '<line x1="8" y1="6" x2="8" y2="22" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
        '<path d="M8 6.8H19.5L17.2 10.8L19.5 14.8H8V6.8Z" fill="var(--ic-accent)" fill-opacity="0.28" stroke="currentColor" stroke-width="1.65" stroke-linejoin="round"/>'
        '<circle cx="19.5" cy="19.2" r="2.2" fill="var(--ic-accent)"/>'
    ),
    # 4. Trade Marketing Manager: Retail endcap display + upward promotional lift
    "trade_marketing_manager": (
        '<path d="M6.5 21.5V9.5L14 6L21.5 9.5V21.5H6.5Z" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.65" stroke-linejoin="round"/>'
        '<path d="M14 18.5V11M11.3 13.6L14 10.8L16.7 13.6" fill="none" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 5. Key Account Manager (KAM): Executive JBP briefcase + joint target core
    "key_account_manager": (
        '<rect x="5.2" y="9.2" width="17.6" height="12" rx="2" fill="var(--ic-accent)" fill-opacity="0.18" stroke="currentColor" stroke-width="1.7"/>'
        '<path d="M10.5 9.2V7.2C10.5 6.4 11.1 5.8 11.9 5.8H16.1C16.9 5.8 17.5 6.4 17.5 7.2V9.2" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        '<circle cx="14" cy="15.2" r="2.3" fill="var(--ic-accent)"/>'
    ),
    # 6. Revenue / Trade Finance Lead: Precision balance beam scale
    "revenue_trade_finance_lead": (
        '<line x1="14" y1="6" x2="14" y2="21.5" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"/>'
        '<line x1="6.5" y1="9.5" x2="21.5" y2="9.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>'
        '<polygon points="7.5,10 10.2,15.8 4.8,15.8" fill="var(--ic-accent)" fill-opacity="0.3" stroke="var(--ic-accent)" stroke-width="1.4" stroke-linejoin="round"/>'
        '<polygon points="20.5,10 23.2,15.8 17.8,15.8" fill="var(--ic-accent)" fill-opacity="0.3" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>'
        '<line x1="10" y1="21.5" x2="18" y2="21.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
    ),
    # 7. S&OP / Supply Planning Dir.: Executive gauge dial + consensus needle
    "sop_supply_planning_dir": (
        '<path d="M5.5 18.5C5.5 13.2 9.3 9 14 9C18.7 9 22.5 13.2 22.5 18.5" fill="var(--ic-accent)" fill-opacity="0.2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
        '<line x1="14" y1="18.5" x2="18.2" y2="12.2" stroke="var(--ic-accent)" stroke-width="2.1" stroke-linecap="round"/>'
        '<circle cx="14" cy="18.5" r="2.1" fill="currentColor"/>'
    ),
    # 8. Supply Chain VP / COO: Lighthouse resilience beacon tower
    "supply_chain_vp_coo": (
        '<polygon points="11.5,10 16.5,10 18.2,22 9.8,22" fill="var(--ic-accent)" fill-opacity="0.22" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>'
        '<circle cx="14" cy="7.5" r="2.1" fill="var(--ic-accent)"/>'
        '<path d="M6 6.5L10.2 7.8M22 6.5L17.8 7.8" stroke="var(--ic-accent)" stroke-width="1.7" stroke-linecap="round"/>'
    ),
    # 9. IBP Lead / Chief Planning Off.: Global meridian sphere + latitude ring
    "ibp_lead_chief_planning_off": (
        '<circle cx="14" cy="14" r="8" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.75"/>'
        '<ellipse cx="14" cy="14" rx="3.8" ry="8" fill="none" stroke="var(--ic-accent)" stroke-width="1.5"/>'
        '<line x1="6.2" y1="14" x2="21.8" y2="14" stroke="currentColor" stroke-width="1.5"/>'
    ),
    # 10. Category Manager: 2x2 assortment matrix with hero quadrant
    "category_manager_portfolio": (
        '<rect x="6" y="6" width="6.8" height="6.8" rx="1.4" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.5"/>'
        '<rect x="15.2" y="6" width="6.8" height="6.8" rx="1.4" fill="var(--ic-accent)" fill-opacity="0.22" stroke="currentColor" stroke-width="1.5"/>'
        '<rect x="6" y="15.2" width="6.8" height="6.8" rx="1.4" fill="none" stroke="currentColor" stroke-width="1.5"/>'
        '<rect x="15.2" y="15.2" width="6.8" height="6.8" rx="1.4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="2 1.6"/>'
    ),
    # 11. Lifecycle / Materials Mgr: BOM revision blueprint + phase arrow
    "lifecycle_materials_mgr": (
        '<rect x="5.5" y="6" width="14" height="16" rx="1.8" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.65"/>'
        '<circle cx="12.5" cy="12.5" r="2.8" fill="none" stroke="currentColor" stroke-width="1.5"/>'
        '<path d="M16.5 18H23M20.8 15.8L23.2 18L20.8 20.2" fill="none" stroke="var(--ic-accent)" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 12. Commercial Finance Director: Drafting compass over margin ledger
    "commercial_finance_director": (
        '<circle cx="14" cy="7.2" r="2" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.4"/>'
        '<line x1="13" y1="9" x2="8" y2="21.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
        '<line x1="15" y1="9" x2="20" y2="21.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
        '<path d="M9.5 16.5H18.5" stroke="var(--ic-accent)" stroke-width="1.8" stroke-linecap="round"/>'
    ),
    # --- 02 · Sourcing & Procurement ---
    # 13. Procurement Dir. / Risk Mgr: Multi-ring radar umbrella shield
    "procurement_dir_risk_mgr": (
        '<path d="M5.5 14.5C5.5 9.8 9.3 6 14 6C18.7 6 22.5 9.8 22.5 14.5H5.5Z" fill="var(--ic-accent)" fill-opacity="0.25" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round"/>'
        '<path d="M14 14.5V20.2C14 21.3 13.1 22.2 12 22.2C10.9 22.2 10 21.3 10 20.2" fill="none" stroke="var(--ic-accent)" stroke-width="1.85" stroke-linecap="round"/>'
    ),
    # 14. Procurement Operations Lead: Qualification clipboard + ribbon badge
    "procurement_operations_lead": (
        '<rect x="6.5" y="6.8" width="13" height="15.2" rx="1.8" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.65"/>'
        '<rect x="10.2" y="4.8" width="5.6" height="3.2" rx="1" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.3"/>'
        '<circle cx="19.5" cy="17.5" r="3.2" fill="var(--ic-accent)"/>'
    ),
    # 15. Chief Sustainability Officer: Dual globe + clean leaf crest
    "chief_sustainability_officer": (
        '<path d="M14 22C9.6 22 6 18.4 6 14C6 9.6 9.6 6 14 6" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"/>'
        '<path d="M13 18C13 12.5 16.5 8.5 22 8C22 13.5 18.8 18 13 18Z" fill="var(--ic-accent)" fill-opacity="0.3" stroke="var(--ic-accent)" stroke-width="1.75" stroke-linejoin="round"/>'
    ),
    # 16. Category Sourcing Mgr (Direct): Stacked commodity ingots + index trend
    "category_sourcing_mgr_direct": (
        '<polygon points="7.5,16.5 13,16.5 14.4,20.5 6.1,20.5" fill="var(--ic-accent)" fill-opacity="0.35" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>'
        '<polygon points="15,16.5 20.5,16.5 21.9,20.5 13.6,20.5" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>'
        '<path d="M6.5 12L11.5 8.5L15.5 11L21.5 6.8" fill="none" stroke="var(--ic-accent)" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 17. Strategic Sourcing Lead: Target bullseye + bid gavel arrow
    "strategic_sourcing_lead": (
        '<circle cx="13" cy="14.5" r="7" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.7"/>'
        '<circle cx="13" cy="14.5" r="3.4" fill="none" stroke="var(--ic-accent)" stroke-width="1.6"/>'
        '<path d="M15 12.5L22 5.5" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round"/>'
    ),
    # 18. Packaging R&D Engineer: Precision vernier caliper jaws + spec cube
    "packaging_rd_engineer": (
        '<path d="M6.5 6V22M6.5 8.5H16.5V11.5H10.5M6.5 19.5H14.5V16.5H10.5" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
        '<rect x="16.5" y="12.2" width="5.2" height="5.2" rx="1" fill="var(--ic-accent)" fill-opacity="0.35" stroke="var(--ic-accent)" stroke-width="1.5"/>'
    ),
    # 19. Commercial Sourcing / Legal: Fountain nib + legal clause seal
    "commercial_sourcing_legal": (
        '<path d="M14 5.5L19.5 14.5L16.8 21.5H11.2L8.5 14.5L14 5.5Z" fill="var(--ic-accent)" fill-opacity="0.22" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>'
        '<line x1="14" y1="5.5" x2="14" y2="14" stroke="var(--ic-accent)" stroke-width="1.7"/>'
        '<circle cx="14" cy="14.5" r="1.6" fill="currentColor"/>'
    ),
    # 20. Buyer / Procurement Coord.: Stopwatch crown + PO checklist
    "buyer_procurement_coord": (
        '<line x1="11.5" y1="5.2" x2="16.5" y2="5.2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
        '<circle cx="14" cy="14.8" r="7.2" fill="var(--ic-accent)" fill-opacity="0.18" stroke="currentColor" stroke-width="1.75"/>'
        '<path d="M11 14.8L13.2 17L17.4 12.5" fill="none" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 21. Accounts Payable Lead: Financial payment ledger card + audit bar
    "accounts_payable_lead": (
        '<rect x="5" y="7.5" width="18" height="13" rx="2.2" fill="var(--ic-accent)" fill-opacity="0.18" stroke="currentColor" stroke-width="1.7"/>'
        '<line x1="5" y1="11.8" x2="23" y2="11.8" stroke="var(--ic-accent)" stroke-width="2.2"/>'
        '<line x1="8.5" y1="16.5" x2="13.5" y2="16.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
        '<circle cx="19" cy="16.5" r="1.6" fill="var(--ic-accent)"/>'
    ),
    # --- 03 · Manufacturing & Production ---
    # 22. Master Production Scheduler: Precision industrial gear + schedule hand
    "master_production_scheduler": (
        '<circle cx="14" cy="14" r="6.2" fill="var(--ic-accent)" fill-opacity="0.2" stroke="currentColor" stroke-width="1.8"/>'
        '<path d="M14 5.2V7.5M14 20.5V22.8M5.2 14H7.5M20.5 14H22.8M7.8 7.8L9.4 9.4M18.6 18.6L20.2 20.2M20.2 7.8L18.6 9.4M9.4 18.6L7.8 20.2" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>'
        '<path d="M14 11V14L16.2 15.4" fill="none" stroke="var(--ic-accent)" stroke-width="1.8" stroke-linecap="round"/>'
    ),
    # 23. Shop Floor / Shift Lead: Industrial safety hard-hat silhouette
    "shop_floor_shift_lead": (
        '<path d="M6.2 17.5C6.2 12.2 9.6 8.2 14 8.2C18.4 8.2 21.8 12.2 21.8 17.5H6.2Z" fill="var(--ic-accent)" fill-opacity="0.26" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round"/>'
        '<line x1="14" y1="6.8" x2="14" y2="12.5" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round"/>'
        '<line x1="4.8" y1="19.8" x2="23.2" y2="19.8" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>'
    ),
    # 24. Plant Operations Manager: Sawtooth factory roofline + smokestack pulse
    "plant_operations_manager": (
        '<path d="M5.5 21.5V12.5L10.8 9.2V12.5L16.2 9.2V12.5L22.5 9.2V21.5H5.5Z" fill="var(--ic-accent)" fill-opacity="0.22" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>'
        '<rect x="9.2" y="15.8" width="3.5" height="5.7" fill="var(--ic-accent)"/>'
        '<rect x="15.5" y="15.8" width="3.5" height="3.2" fill="currentColor" opacity="0.7"/>'
    ),
    # 25. Supply Chain Ops Director: Crossed precision spanner + telemetry node
    "supply_chain_ops_director": (
        '<path d="M8.5 19.5L17.2 10.8C17 9.2 18.2 7.5 20 7.2L18.4 8.8L19.6 10L21.2 8.4C20.9 10.2 19.2 11.4 17.6 11.2L8.9 19.9" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="8.2" cy="19.8" r="2.3" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.4"/>'
    ),
    # 26. External Sourcing / CMO Lead: Dual linked partner hexagons
    "external_sourcing_cmo_lead": (
        '<polygon points="9.5,8.5 13.5,10.8 13.5,15.5 9.5,17.8 5.5,15.5 5.5,10.8" fill="var(--ic-accent)" fill-opacity="0.28" stroke="currentColor" stroke-width="1.6"/>'
        '<polygon points="18.5,10.2 22.5,12.5 22.5,17.2 18.5,19.5 14.5,17.2 14.5,12.5" fill="none" stroke="var(--ic-accent)" stroke-width="1.75"/>'
    ),
    # 27. VP Manufacturing Engineering: Tower crane + plant expansion module
    "vp_manufacturing_engineering": (
        '<line x1="8.5" y1="5.5" x2="8.5" y2="22" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>'
        '<line x1="5.5" y1="8.2" x2="22.5" y2="8.2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
        '<line x1="18.5" y1="8.2" x2="18.5" y2="13.5" stroke="var(--ic-accent)" stroke-width="1.6"/>'
        '<rect x="15.2" y="13.8" width="6.6" height="6.2" rx="1" fill="var(--ic-accent)" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>'
    ),
    # 28. QA Manager / Line Inspector: Optical inspection aperture lens
    "qa_manager_line_inspector": (
        '<circle cx="14" cy="14" r="7.8" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.75"/>'
        '<polygon points="14,9.2 18.2,11.6 18.2,16.4 14,18.8 9.8,16.4 9.8,11.6" fill="var(--ic-accent)" fill-opacity="0.32" stroke="var(--ic-accent)" stroke-width="1.5"/>'
        '<circle cx="14" cy="14" r="1.6" fill="currentColor"/>'
    ),
    # 29. Regulatory Compliance Lead: Laboratory Erlenmeyer flask + QA seal
    "regulatory_compliance_lead": (
        '<path d="M11.5 6H16.5M12.5 6V11L7.5 19.8C7 20.7 7.6 21.8 8.7 21.8H19.3C20.4 21.8 21 20.7 20.5 19.8L15.5 11V6" fill="var(--ic-accent)" fill-opacity="0.2" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
        '<line x1="9.6" y1="17" x2="18.4" y2="17" stroke="var(--ic-accent)" stroke-width="1.8"/>'
    ),
    # 30. Continuous Improvement Lead: Statistical control chart (UCL / CL / LCL)
    "continuous_improvement_lead": (
        '<line x1="5.5" y1="8" x2="22.5" y2="8" stroke="var(--ic-accent)" stroke-width="1.4" stroke-dasharray="2.2 1.8"/>'
        '<line x1="5.5" y1="20" x2="22.5" y2="20" stroke="var(--ic-accent)" stroke-width="1.4" stroke-dasharray="2.2 1.8"/>'
        '<path d="M6 15L10.5 11.5L14.5 16L18.5 12.2L22 14" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # --- 04 · Inventory & Warehousing ---
    # 31. Inventory Optimization Lead: Dual buffer cylinders with optimal fill levels
    "inventory_optimization_lead": (
        '<rect x="6.5" y="7" width="6" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="1.65"/>'
        '<rect x="6.5" y="13" width="6" height="8" rx="1.5" fill="var(--ic-accent)"/>'
        '<rect x="15.5" y="7" width="6" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="1.65"/>'
        '<rect x="15.5" y="10.5" width="6" height="10.5" rx="1.5" fill="var(--ic-accent)" fill-opacity="0.45"/>'
    ),
    # 32. Inventory Controller / Buyer: Stock ledger + aging dial
    "inventory_controller_buyer": (
        '<rect x="5.5" y="6" width="12.5" height="15.5" rx="1.8" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.65"/>'
        '<circle cx="18.5" cy="17.2" r="4.2" fill="var(--bg-card, #0f172a)" stroke="var(--ic-accent)" stroke-width="1.75"/>'
        '<path d="M18.5 15V17.2L20 18.2" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>'
    ),
    # 33. Replenishment Planner: Synchronized continuous replenishment cycle arrows
    "replenishment_planner": (
        '<path d="M7.5 11.5C8.6 8.2 11.8 6.2 15.4 6.8C18.2 7.2 20.4 9.2 21.1 11.8" fill="none" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round"/>'
        '<path d="M20.5 16.5C19.4 19.8 16.2 21.8 12.6 21.2C9.8 20.8 7.6 18.8 6.9 16.2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
        '<polygon points="21.8,9.2 22.2,12.8 18.8,11.8" fill="var(--ic-accent)"/>'
        '<polygon points="6.2,18.8 5.8,15.2 9.2,16.2" fill="currentColor"/>'
    ),
    # 34. DC Operations Mgr / IE Lead: Warehouse gable roof + pallet racking bay
    "dc_operations_mgr": (
        '<path d="M5 11.5L14 6L23 11.5V21.5H5V11.5Z" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round"/>'
        '<rect x="9.5" y="13.5" width="9" height="8" fill="none" stroke="var(--ic-accent)" stroke-width="1.6"/>'
        '<line x1="9.5" y1="17.5" x2="18.5" y2="17.5" stroke="var(--ic-accent)" stroke-width="1.5"/>'
    ),
    # 35. Inbound Receiving Supervisor: Handheld RF barcode scanner + laser beam
    "inbound_receiving_supervisor": (
        '<path d="M7.5 9.5H16.5L14.5 14H10.8L12 21.5H8.8L7.5 9.5Z" fill="var(--ic-accent)" fill-opacity="0.26" stroke="currentColor" stroke-width="1.65" stroke-linejoin="round"/>'
        '<path d="M17.5 9.8L22.5 7.5M17.5 11.5H23M17.5 13.2L22.5 15.5" stroke="var(--ic-accent)" stroke-width="1.7" stroke-linecap="round"/>'
    ),
    # 36. DC Shift Floor Lead: Conveyor rollers + outbound carton
    "dc_shift_floor_lead": (
        '<rect x="8.5" y="6.8" width="11" height="8" rx="1.4" fill="var(--ic-accent)" fill-opacity="0.28" stroke="currentColor" stroke-width="1.65"/>'
        '<rect x="5" y="17" width="18" height="4.2" rx="2.1" fill="none" stroke="currentColor" stroke-width="1.65"/>'
        '<circle cx="8.5" cy="19.1" r="1" fill="var(--ic-accent)"/>'
        '<circle cx="14" cy="19.1" r="1" fill="var(--ic-accent)"/>'
        '<circle cx="19.5" cy="19.1" r="1" fill="var(--ic-accent)"/>'
    ),
    # 37. Store Operations / Omni Lead: Storefront awning + shelf accuracy eye
    "store_operations_omni_lead": (
        '<path d="M5.5 10.5L7.5 6.5H20.5L22.5 10.5H5.5Z" fill="var(--ic-accent)" fill-opacity="0.3" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
        '<path d="M7 10.5V21H21V10.5" fill="none" stroke="currentColor" stroke-width="1.65"/>'
        '<circle cx="14" cy="15.8" r="2.4" fill="var(--ic-accent)"/>'
    ),
    # 38. Omnichannel Fulfillment Dir.: Shopping bag + fast dispatch arrow
    "omnichannel_fulfillment_dir": (
        '<rect x="6.5" y="9.8" width="13" height="11.5" rx="1.8" fill="var(--ic-accent)" fill-opacity="0.2" stroke="currentColor" stroke-width="1.7"/>'
        '<path d="M10.2 9.8V8.2C10.2 6.5 11.5 5.2 13 5.2C14.5 5.2 15.8 6.5 15.8 8.2V9.8" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        '<path d="M15.5 15.5H23M20.8 13.3L23.2 15.5L20.8 17.7" fill="none" stroke="var(--ic-accent)" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 39. Reverse Logistics Lead (WH): Grading prism + restock shelf
    "reverse_logistics_lead_wh": (
        '<polygon points="14,6.2 21.5,19.8 6.5,19.8" fill="var(--ic-accent)" fill-opacity="0.22" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>'
        '<path d="M11.5 15.2L13.4 17.1L16.8 13.2" fill="none" stroke="var(--ic-accent)" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # --- 05 · Distribution & Logistics ---
    # 40. Transport Planner / Inbound Mgr: Isometric 3D cargo cube + dimension axes
    "transport_planner_inbound_mgr": (
        '<polygon points="14,6.2 21,10.2 14,14.2 7,10.2" fill="var(--ic-accent)" fill-opacity="0.3" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
        '<polygon points="7,10.2 14,14.2 14,21.8 7,17.8" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
        '<polygon points="21,10.2 14,14.2 14,21.8 21,17.8" fill="var(--ic-accent)" fill-opacity="0.14" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>'
    ),
    # 41. Yard Master / Plant Logistics: Yard gate boom barrier + pillar post
    "yard_master_plant_logistics": (
        '<rect x="6" y="12.5" width="4.2" height="9" rx="1" fill="currentColor"/>'
        '<path d="M8.5 14L21.5 7.5" stroke="var(--ic-accent)" stroke-width="2.6" stroke-linecap="round"/>'
        '<line x1="5" y1="21.5" x2="23" y2="21.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
    ),
    # 42. Cold Chain QA / Logistics Dir.: Hexagonal frost shield
    "cold_chain_qa_logistics_dir": (
        '<polygon points="14,5.2 21.5,9.6 21.5,18.4 14,22.8 6.5,18.4 6.5,9.6" fill="var(--ic-accent)" fill-opacity="0.2" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>'
        '<path d="M14 9V19M9.7 11.5L18.3 16.5M18.3 11.5L9.7 16.5" stroke="var(--ic-accent)" stroke-width="1.7" stroke-linecap="round"/>'
    ),
    # 43. Outbound Lead / Industrial Eng.: Hand pallet forks lifting stacked load
    "outbound_lead_industrial_eng": (
        '<path d="M6.5 7V19.5H21.5" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>'
        '<rect x="10.2" y="10.5" width="9.5" height="6.8" rx="1.2" fill="var(--ic-accent)" fill-opacity="0.32" stroke="var(--ic-accent)" stroke-width="1.6"/>'
        '<circle cx="8" cy="21.5" r="1.4" fill="currentColor"/>'
        '<circle cx="19.5" cy="21.5" r="1.4" fill="currentColor"/>'
    ),
    # 44. Store Replenishment Lead: Store aisle shelves + replenishment indicator
    "store_replenishment_lead": (
        '<line x1="7" y1="6.5" x2="7" y2="21.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
        '<line x1="21" y1="6.5" x2="21" y2="21.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
        '<rect x="9.5" y="8" width="9" height="3.2" rx="0.8" fill="var(--ic-accent)"/>'
        '<rect x="9.5" y="13" width="9" height="3.2" rx="0.8" fill="var(--ic-accent)" fill-opacity="0.45"/>'
        '<line x1="7" y1="19.2" x2="21" y2="19.2" stroke="currentColor" stroke-width="1.5"/>'
    ),
    # 45. Retail Logistics Dispatcher: Timed dispatch clock + route chevron
    "retail_logistics_dispatcher": (
        '<circle cx="13" cy="14" r="7.2" fill="var(--ic-accent)" fill-opacity="0.18" stroke="currentColor" stroke-width="1.75"/>'
        '<path d="M13 10.2V14H16.5" fill="none" stroke="var(--ic-accent)" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M20.5 11.5L23.2 14L20.5 16.5" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 46. Last-Mile Operations Lead: Folded street map + verified delivery dot
    "last_mile_operations_lead": (
        '<polygon points="5.5,7.5 11,5.8 17,8.2 22.5,6.5 22.5,20.5 17,22.2 11,19.8 5.5,21.5" fill="var(--ic-accent)" fill-opacity="0.18" stroke="currentColor" stroke-width="1.65" stroke-linejoin="round"/>'
        '<line x1="11" y1="5.8" x2="11" y2="19.8" stroke="currentColor" stroke-width="1.3"/>'
        '<circle cx="17" cy="14" r="2.2" fill="var(--ic-accent)"/>'
    ),
    # 47. E-Commerce Logistics Dir.: Express parcel carton + tape seal
    "ecommerce_logistics_dir": (
        '<rect x="6.2" y="7.2" width="15.6" height="13.6" rx="2" fill="var(--ic-accent)" fill-opacity="0.2" stroke="currentColor" stroke-width="1.7"/>'
        '<path d="M11.5 7.2V13.2L14 11.8L16.5 13.2V7.2" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/>'
    ),
    # 48. Customer Support Ops Lead: Proactive customer message card + live check
    "customer_support_ops_lead": (
        '<path d="M6 7.5H22V17.5H12.5L8 21V17.5H6V7.5Z" fill="var(--ic-accent)" fill-opacity="0.2" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>'
        '<path d="M11 12.5L13.2 14.6L17.5 10.5" fill="none" stroke="var(--ic-accent)" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 49. Fleet Dispatcher / Central Ops: Precision navigation compass rose
    "fleet_dispatcher_central_ops": (
        '<circle cx="14" cy="14" r="8" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.75"/>'
        '<polygon points="17.8,10.2 15.4,15.4 10.2,17.8 12.6,12.6" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/>'
    ),
    # 50. Transport Procurement Lead: Contracted lane bridge arch
    "transport_procurement_lead": (
        '<line x1="5" y1="16.5" x2="23" y2="16.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
        '<path d="M6.5 16.5C8.5 9.5 19.5 9.5 21.5 16.5" fill="var(--ic-accent)" fill-opacity="0.22" stroke="var(--ic-accent)" stroke-width="1.8"/>'
        '<line x1="9" y1="16.5" x2="9" y2="20.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
        '<line x1="19" y1="16.5" x2="19" y2="20.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
    ),
    # 51. Freight Controller / Claims: Tariff ledger + magnifying audit bar
    "freight_controller_claims": (
        '<rect x="6" y="5.8" width="16" height="16.4" rx="2" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.7"/>'
        '<rect x="9" y="9" width="10" height="3.2" rx="0.8" fill="var(--ic-accent)"/>'
        '<line x1="9" y1="15.2" x2="13" y2="15.2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
        '<line x1="15.5" y1="15.2" x2="19" y2="15.2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
        '<line x1="9" y1="18.4" x2="19" y2="18.4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>'
    ),
    # --- 06 · Returns & Reverse Logistics ---
    # 52. Reverse Logistics / Fraud Lead: Keyhole verification shield
    "reverse_logistics_fraud_lead": (
        '<path d="M14 5.2L21.2 8V13.8C21.2 18.2 18.1 21.4 14 23C9.9 21.4 6.8 18.2 6.8 13.8V8L14 5.2Z" fill="var(--ic-accent)" fill-opacity="0.2" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>'
        '<circle cx="14" cy="12.5" r="1.9" fill="var(--ic-accent)"/>'
        '<line x1="14" y1="14.4" x2="14" y2="17.8" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round"/>'
    ),
    # 53. Customer Experience (CX) Lead: Return U-turn arrow + loyalty star
    "customer_experience_cx_lead": (
        '<path d="M19.5 18.5H11.5C8.5 18.5 6.5 16.5 6.5 13.5C6.5 10.5 8.5 8.5 11.5 8.5H17.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
        '<path d="M15.2 6.2L18 8.5L15.2 10.8" fill="none" stroke="var(--ic-accent)" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="19.5" cy="13.5" r="2.1" fill="var(--ic-accent)"/>'
    ),
    # 54. Claims Specialist / Controller: Dock evidence camera housing
    "claims_specialist_controller": (
        '<path d="M5.5 10.2H9.2L10.8 8H17.2L18.8 10.2H22.5V20.5H5.5V10.2Z" fill="var(--ic-accent)" fill-opacity="0.18" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>'
        '<circle cx="14" cy="15.2" r="3" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.4"/>'
    ),
    # 55. Merchandising / Store Ops Mgr: Hanging retail markdown badge
    "merchandising_store_ops_mgr": (
        '<path d="M8.5 5.8H19.5L21.5 11V21.5H6.5V11L8.5 5.8Z" fill="var(--ic-accent)" fill-opacity="0.2" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>'
        '<circle cx="14" cy="9.2" r="1.4" fill="currentColor"/>'
        '<path d="M10.5 17.5L17.5 13" stroke="var(--ic-accent)" stroke-width="1.9" stroke-linecap="round"/>'
    ),
    # 56. Inventory Disposition Lead: Diverter gate routing lot into high-turn channel
    "inventory_disposition_lead": (
        '<circle cx="7.5" cy="14" r="2.4" fill="currentColor"/>'
        '<path d="M10 14L19.5 8.5" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round"/>'
        '<path d="M10 14L19.5 19.5" stroke="currentColor" stroke-width="1.5" stroke-dasharray="2 2" stroke-linecap="round"/>'
        '<rect x="19.5" y="6.5" width="3.6" height="3.6" rx="0.8" fill="var(--ic-accent)"/>'
    ),
    # 57. Chief Sustainability Officer (Circular): Triangle circularity loop
    "cso_circular_lead": (
        '<path d="M14 6.2L21.2 19H6.8L14 6.2Z" fill="var(--ic-accent)" fill-opacity="0.2" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>'
        '<circle cx="14" cy="14.5" r="2.2" fill="var(--ic-accent)"/>'
    ),
    # 58. Asset Recovery / RTI Manager: Isometric reusable plastic crate with handles
    "asset_recovery_rti_manager": (
        '<rect x="5.5" y="9.5" width="17" height="10.5" rx="1.6" fill="var(--ic-accent)" fill-opacity="0.22" stroke="currentColor" stroke-width="1.75"/>'
        '<line x1="9.5" y1="12.5" x2="12.5" y2="12.5" stroke="var(--ic-accent)" stroke-width="1.8" stroke-linecap="round"/>'
        '<line x1="15.5" y1="12.5" x2="18.5" y2="12.5" stroke="var(--ic-accent)" stroke-width="1.8" stroke-linecap="round"/>'
    ),
    # 59. Reverse Transport Planner: Bidirectional backhaul lane arrows
    "reverse_transport_planner": (
        '<line x1="5.5" y1="10.5" x2="21.5" y2="10.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
        '<path d="M18.8 8L21.8 10.5L18.8 13" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
        '<line x1="22.5" y1="17.5" x2="6.5" y2="17.5" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round"/>'
        '<path d="M9.2 15L6.2 17.5L9.2 20" fill="none" stroke="var(--ic-accent)" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>'
    ),
    # 60. Packaging QA / Food Safety: Hygienic droplet inside compliance shield
    "packaging_qa_food_safety": (
        '<circle cx="14" cy="14" r="8" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.75"/>'
        '<path d="M14 8.8C14 8.8 10.5 13 10.5 15.2C10.5 17.1 12.1 18.6 14 18.6C15.9 18.6 17.5 17.1 17.5 15.2C17.5 13 14 8.8 14 8.8Z" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>'
    ),
}


# ==============================================================================
# 3. 20 BESPOKE SUB-PILLAR VECTOR SVGs (28x28 coordinate space, static, duotone)
# ==============================================================================
SUBPILLAR_VECTOR_SVGS: dict[str, str] = {
    "demand_forecasting": '<path d="M5 20.5H23M6.5 17L11 12.5L14.8 15L21.5 8" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/><circle cx="21.5" cy="8" r="2.2" fill="var(--ic-accent)"/>',
    "trade_promotion": '<path d="M5.5 13.5V6.5H12.5L21 15L14 22L5.5 13.5Z" fill="var(--ic-accent)" fill-opacity="0.22" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round"/><circle cx="9.5" cy="10.5" r="1.5" fill="currentColor"/>',
    "sop_ibp": '<line x1="14" y1="6" x2="14" y2="21.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><line x1="6" y1="11" x2="22" y2="11" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round"/><circle cx="8" cy="15.5" r="2.2" fill="var(--ic-accent)"/><circle cx="20" cy="15.5" r="2.2" fill="currentColor"/>',
    "portfolio_sku": '<rect x="5.5" y="5.5" width="7.2" height="7.2" rx="1.5" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.5"/><rect x="15.3" y="5.5" width="7.2" height="7.2" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.5"/><rect x="5.5" y="15.3" width="7.2" height="7.2" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.5"/><rect x="15.3" y="15.3" width="7.2" height="7.2" rx="1.5" fill="var(--ic-accent)" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>',
    "supplier_network": '<circle cx="14" cy="14" r="3" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.5"/><line x1="14" y1="11" x2="14" y2="6" stroke="currentColor" stroke-width="1.6"/><line x1="11.4" y1="15.5" x2="7" y2="19" stroke="currentColor" stroke-width="1.6"/><line x1="16.6" y1="15.5" x2="21" y2="19" stroke="currentColor" stroke-width="1.6"/><circle cx="14" cy="5.5" r="1.9" fill="currentColor"/><circle cx="6.5" cy="19.5" r="1.9" fill="currentColor"/><circle cx="21.5" cy="19.5" r="1.9" fill="var(--ic-accent)"/>',
    "material_packaging": '<polygon points="14,5.5 22,10 14,14.5 6,10" fill="var(--ic-accent)" fill-opacity="0.28" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M6 10V18.5L14 23L22 18.5V10" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><line x1="14" y1="14.5" x2="14" y2="23" stroke="currentColor" stroke-width="1.6"/>',
    "contract_po_mgmt": '<rect x="6.5" y="5" width="15" height="18" rx="2" fill="var(--ic-accent)" fill-opacity="0.18" stroke="currentColor" stroke-width="1.75"/><line x1="10" y1="10" x2="18" y2="10" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><line x1="10" y1="14" x2="16" y2="14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M13 18.2L14.8 20L18.5 16.2" fill="none" stroke="var(--ic-accent)" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>',
    "production_scheduling": '<rect x="5" y="6.5" width="18" height="15" rx="2" fill="var(--ic-accent)" fill-opacity="0.16" stroke="currentColor" stroke-width="1.7"/><line x1="5" y1="11" x2="23" y2="11" stroke="currentColor" stroke-width="1.5"/><rect x="8" y="13.5" width="6.5" height="2.4" rx="0.8" fill="var(--ic-accent)"/><rect x="12" y="17.2" width="7.5" height="2.4" rx="0.8" fill="currentColor"/>',
    "capacity_planning": '<path d="M5 21.5V12L10.5 8.5V12L16 8.5V12L23 8V21.5H5Z" fill="var(--ic-accent)" fill-opacity="0.22" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round"/>',
    "quality_compliance": '<path d="M14 5L21.5 8V14C21.5 18.4 18.3 21.6 14 23.2C9.7 21.6 6.5 18.4 6.5 14V8L14 5Z" fill="var(--ic-accent)" fill-opacity="0.22" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round"/><path d="M10.8 14.2L13 16.4L17.6 11.6" fill="none" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "positioning_optimization": '<circle cx="14" cy="7.5" r="2.4" fill="var(--ic-accent)" stroke="currentColor" stroke-width="1.5"/><circle cx="7.5" cy="19.5" r="2.4" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="20.5" cy="19.5" r="2.4" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M12.5 9.6L8.8 17.2M15.5 9.6L19.2 17.2M10 19.5H18" stroke="currentColor" stroke-width="1.6"/>',
    "warehouse_operations": '<path d="M5 11L14 5.5L23 11V21.5H5V11Z" fill="var(--ic-accent)" fill-opacity="0.18" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round"/><line x1="9" y1="14" x2="19" y2="14" stroke="var(--ic-accent)" stroke-width="1.8"/><line x1="9" y1="18" x2="19" y2="18" stroke="currentColor" stroke-width="1.6"/>',
    "omnichannel_visibility": '<rect x="5" y="7" width="12.5" height="10" rx="1.6" fill="var(--ic-accent)" fill-opacity="0.2" stroke="currentColor" stroke-width="1.65"/><rect x="15.5" y="11" width="7.5" height="10.5" rx="1.5" fill="var(--bg-card, #0f172a)" stroke="var(--ic-accent)" stroke-width="1.7"/>',
    "first_mid_mile": '<rect x="4.5" y="8.5" width="13.5" height="9.5" rx="1.4" fill="var(--ic-accent)" fill-opacity="0.22" stroke="currentColor" stroke-width="1.7"/><path d="M18 11.5H21.8L23.5 14.8V18H18V11.5Z" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linejoin="round"/><circle cx="8.5" cy="19.8" r="1.8" fill="currentColor"/><circle cx="20.5" cy="19.8" r="1.8" fill="var(--ic-accent)"/>',
    "store_replenishment": '<path d="M5.5 10.5L7.5 6.2H20.5L22.5 10.5H5.5Z" fill="var(--ic-accent)" fill-opacity="0.28" stroke="currentColor" stroke-width="1.65" stroke-linejoin="round"/><rect x="7" y="10.5" width="14" height="10.8" fill="none" stroke="currentColor" stroke-width="1.65"/><rect x="11.5" y="14.5" width="5" height="6.8" fill="var(--ic-accent)"/>',
    "last_mile_delivery": '<path d="M14 22C14 22 20 15.8 20 11C20 7.7 17.3 5 14 5C10.7 5 8 7.7 8 11C8 15.8 14 22 14 22Z" fill="var(--ic-accent)" fill-opacity="0.24" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><circle cx="14" cy="11" r="2.3" fill="var(--ic-accent)"/>',
    "route_carrier": '<circle cx="7" cy="19.5" r="2.2" fill="currentColor"/><circle cx="21" cy="8.5" r="2.2" fill="var(--ic-accent)"/><path d="M7 17.3C7 11.5 12.5 14.5 18.8 8.8" fill="none" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round"/>',
    "returns_claims_mgmt": '<path d="M9.5 9.5H17.5C20 9.5 21.8 11.3 21.8 13.8C21.8 16.3 20 18.1 17.5 18.1H8" fill="none" stroke="currentColor" stroke-width="1.85" stroke-linecap="round"/><path d="M12 6.8L9 9.5L12 12.2" fill="none" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "expiry_markdowns": '<circle cx="14" cy="14" r="8" fill="var(--ic-accent)" fill-opacity="0.18" stroke="currentColor" stroke-width="1.75"/><path d="M14 9.5V14L17.2 16" fill="none" stroke="var(--ic-accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    "pallet_tote_reclamation": '<rect x="6" y="8" width="16" height="5" rx="1.2" fill="var(--ic-accent)" fill-opacity="0.3" stroke="currentColor" stroke-width="1.65"/><rect x="6" y="15" width="16" height="5" rx="1.2" fill="none" stroke="currentColor" stroke-width="1.65"/>',
}


CUSTOM_VECTOR_ICON_CSS = """
    /* === ARCHITECTURAL DUOTONE VECTOR ICON SYSTEM (60 AGENTS + 60 PERSONAS + 20 SUB-PILLARS) === */
    .ai-bot-square.sc-vec-agent-badge {
      background: linear-gradient(145deg, color-mix(in srgb, var(--ic-accent, #6366f1) 24%, #131c31) 0%, color-mix(in srgb, var(--ic-accent, #6366f1) 9%, #0b1120) 100%) !important;
      border: 1.5px solid color-mix(in srgb, var(--ic-accent, #6366f1) 56%, rgba(255, 255, 255, 0.14)) !important;
      color: color-mix(in srgb, var(--ic-accent, #6366f1) 24%, #f8fafc) !important;
      border-radius: 11px;
      box-shadow: 0 5px 14px rgba(2, 6, 23, 0.34), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
      padding: 0;
      position: relative;
    }
    html[data-theme="light"] .ai-bot-square.sc-vec-agent-badge {
      background: linear-gradient(145deg, color-mix(in srgb, var(--ic-accent, #4f46e5) 14%, #ffffff) 0%, color-mix(in srgb, var(--ic-accent, #4f46e5) 6%, #f8fafc) 100%) !important;
      border: 1.5px solid color-mix(in srgb, var(--ic-accent, #4f46e5) 48%, #cbd5e1) !important;
      color: color-mix(in srgb, var(--ic-accent, #4f46e5) 75%, #0f172a) !important;
      box-shadow: 0 4px 11px color-mix(in srgb, var(--ic-accent, #4f46e5) 14%, rgba(15, 23, 42, 0.06)) !important;
    }
    .human-avatar-circle.sc-vec-persona-badge {
      background: radial-gradient(circle at 30% 26%, color-mix(in srgb, var(--ic-accent, #2563eb) 26%, #182338) 0%, color-mix(in srgb, var(--ic-accent, #2563eb) 8%, #0c1322) 100%) !important;
      border: 2px solid color-mix(in srgb, var(--ic-accent, #2563eb) 68%, rgba(255, 255, 255, 0.18)) !important;
      color: color-mix(in srgb, var(--ic-accent, #2563eb) 22%, #f8fafc) !important;
      box-shadow: 0 5px 14px rgba(2, 6, 23, 0.32), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
      padding: 0;
    }
    html[data-theme="light"] .human-avatar-circle.sc-vec-persona-badge {
      background: radial-gradient(circle at 30% 26%, color-mix(in srgb, var(--ic-accent, #2563eb) 15%, #ffffff) 0%, color-mix(in srgb, var(--ic-accent, #2563eb) 5%, #f1f5f9) 100%) !important;
      border: 2px solid color-mix(in srgb, var(--ic-accent, #2563eb) 58%, #94a3b8) !important;
      color: color-mix(in srgb, var(--ic-accent, #2563eb) 76%, #0f172a) !important;
      box-shadow: 0 4px 11px color-mix(in srgb, var(--ic-accent, #2563eb) 14%, rgba(15, 23, 42, 0.06)) !important;
    }
    .ai-agent-chip-card {
      border-color: color-mix(in srgb, var(--ag-accent, #6366f1) 42%, rgba(148, 163, 184, 0.22));
    }
    .ai-agent-chip-card:hover {
      border-color: var(--ag-accent, #818cf8);
      box-shadow: 0 14px 28px color-mix(in srgb, var(--ag-accent, #6366f1) 24%, rgba(2, 6, 23, 0.18));
    }
    .sc-vec-inline-svg {
      display: inline-block;
      vertical-align: -3px;
      flex-shrink: 0;
    }
    .subpillar-box-icon {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 34px;
      height: 34px;
      border-radius: 9px;
      background: color-mix(in srgb, var(--sp-color, #3b82f6) 14%, var(--bg-elevated));
      border: 1px solid color-mix(in srgb, var(--sp-color, #3b82f6) 38%, transparent);
      color: color-mix(in srgb, var(--sp-color, #3b82f6) 28%, var(--text-primary));
    }
"""


def build_js_vector_helpers(persona_by_agent: dict[str, str]) -> str:
    return (
        "\n    /* =========================================================================\n"
        "       BESPOKE ARCHITECTURAL VECTOR ICON REGISTRY (60 AGENTS + 60 PERSONAS + 20 SUB-PILLARS)\n"
        "       ========================================================================= */\n"
        f"    const AGENT_VECTOR_SVGS = {json.dumps(AGENT_VECTOR_SVGS, ensure_ascii=False)};\n"
        f"    const PERSONA_VECTOR_SVGS = {json.dumps(PERSONA_VECTOR_SVGS, ensure_ascii=False)};\n"
        f"    const PERSONA_ID_BY_AGENT = {json.dumps(persona_by_agent, ensure_ascii=False)};\n"
        f"    const SUBPILLAR_VECTOR_SVGS = {json.dumps(SUBPILLAR_VECTOR_SVGS, ensure_ascii=False)};\n"
        """
    function resolveEntityAccentColor(entity, fallback = '#3b82f6') {
      if (!entity) return fallback;
      if (entity.subPillarColor) return entity.subPillarColor;
      if (entity.color) return entity.color;
      if (entity.deptId && typeof DEPARTMENTS !== 'undefined' && DEPARTMENTS[entity.deptId]) {
        return DEPARTMENTS[entity.deptId].color || fallback;
      }
      return fallback;
    }

    function getAgentSvgInner(agOrId) {
      const ag = (typeof agOrId === 'string') ? (typeof AGENTS !== 'undefined' ? AGENTS[agOrId] : null) : agOrId;
      const aid = (typeof agOrId === 'string') ? agOrId : (ag && ag.id) || '';
      if (AGENT_VECTOR_SVGS[aid]) return AGENT_VECTOR_SVGS[aid];
      return '<rect x="6" y="6" width="16" height="16" rx="3" fill="var(--ic-accent)" fill-opacity="0.22" stroke="currentColor" stroke-width="1.75"/><circle cx="14" cy="14" r="2.6" fill="var(--ic-accent)"/>';
    }

    function getPersonaSvgInner(pOrId) {
      const p = (typeof pOrId === 'string') ? (typeof PERSONAS !== 'undefined' ? PERSONAS[pOrId] : null) : pOrId;
      const pid = (typeof pOrId === 'string') ? pOrId : (p && p.id) || '';
      if (PERSONA_VECTOR_SVGS[pid]) return PERSONA_VECTOR_SVGS[pid];
      if (p && p.primaryAgentId) {
        const mappedPid = PERSONA_ID_BY_AGENT[p.primaryAgentId];
        if (mappedPid && PERSONA_VECTOR_SVGS[mappedPid]) return PERSONA_VECTOR_SVGS[mappedPid];
      }
      return '<circle cx="14" cy="10.5" r="3.4" fill="var(--ic-accent)" fill-opacity="0.28" stroke="currentColor" stroke-width="1.7"/><path d="M7.5 21C8.3 17.5 10.8 15.6 14 15.6C17.2 15.6 19.7 17.5 20.5 21" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"/>';
    }

    function getSubPillarSvgInner(spOrId) {
      const sp = (typeof spOrId === 'object' && spOrId) ? spOrId : null;
      const spId = (typeof spOrId === 'string') ? spOrId : (sp && sp.id) || '';
      if (SUBPILLAR_VECTOR_SVGS[spId]) return SUBPILLAR_VECTOR_SVGS[spId];
      // Smart semantic fallback for custom Enterprise Twin sub-pillars
      const nm = ((sp && sp.name) || spId || '').toLowerCase();
      if (nm.includes('demand') || nm.includes('forecast')) return SUBPILLAR_VECTOR_SVGS.demand_forecasting;
      if (nm.includes('trade') || nm.includes('promo') || nm.includes('commercial')) return SUBPILLAR_VECTOR_SVGS.trade_promotion;
      if (nm.includes('sourc') || nm.includes('procure') || nm.includes('supplier') || nm.includes('vendor')) return SUBPILLAR_VECTOR_SVGS.supplier_network;
      if (nm.includes('contract') || nm.includes('po') || nm.includes('pay')) return SUBPILLAR_VECTOR_SVGS.contract_po_mgmt;
      if (nm.includes('sched') || nm.includes('plant') || nm.includes('smelt') || nm.includes('kiln') || nm.includes('mfg') || nm.includes('prod')) return SUBPILLAR_VECTOR_SVGS.capacity_planning;
      if (nm.includes('qual') || nm.includes('batch') || nm.includes('regulat') || nm.includes('cold')) return SUBPILLAR_VECTOR_SVGS.quality_compliance;
      if (nm.includes('warehous') || nm.includes('slot') || nm.includes('dc') || nm.includes('fulfil')) return SUBPILLAR_VECTOR_SVGS.warehouse_operations;
      if (nm.includes('invent') || nm.includes('stock') || nm.includes('meio')) return SUBPILLAR_VECTOR_SVGS.positioning_optimization;
      if (nm.includes('store') || nm.includes('omni') || nm.includes('retail')) return SUBPILLAR_VECTOR_SVGS.store_replenishment;
      if (nm.includes('fleet') || nm.includes('route') || nm.includes('freight') || nm.includes('rail') || nm.includes('logist')) return SUBPILLAR_VECTOR_SVGS.first_mid_mile;
      if (nm.includes('return') || nm.includes('reverse') || nm.includes('circular') || nm.includes('esg')) return SUBPILLAR_VECTOR_SVGS.returns_claims_mgmt;
      if (sp && Array.isArray(sp.items) && sp.items.length > 0 && sp.items[0].agentId) {
        return getAgentSvgInner(sp.items[0].agentId);
      }
      return SUBPILLAR_VECTOR_SVGS.sop_ibp;
    }

    function renderAgentIconBadge(agOrId, sizePx = 44, customAccent = null) {
      const ag = (typeof agOrId === 'string') ? (typeof AGENTS !== 'undefined' ? AGENTS[agOrId] : null) : agOrId;
      const accent = customAccent || resolveEntityAccentColor(ag, '#6366f1');
      const svgSize = Math.round(sizePx * 0.64);
      const inner = getAgentSvgInner(agOrId);
      return `<div class="ai-bot-square sc-vec-agent-badge" style="--ic-accent:${accent}; width:${sizePx}px; height:${sizePx}px; flex-shrink:0;" aria-hidden="true">` +
        `<svg viewBox="0 0 28 28" width="${svgSize}" height="${svgSize}" fill="none" xmlns="http://www.w3.org/2000/svg">` +
          `<path d="M2.5 6V2.5H6M25.5 22V25.5H22" stroke="var(--ic-accent)" stroke-width="1.15" stroke-linecap="round" opacity="0.5"/>` +
          inner +
        `</svg>` +
      `</div>`;
    }

    function renderPersonaIconBadge(pOrId, sizePx = 48, customAccent = null) {
      const p = (typeof pOrId === 'string') ? (typeof PERSONAS !== 'undefined' ? PERSONAS[pOrId] : null) : pOrId;
      const accent = customAccent || resolveEntityAccentColor(p, '#2563eb');
      const svgSize = Math.round(sizePx * 0.62);
      const inner = getPersonaSvgInner(pOrId);
      return `<div class="human-avatar-circle sc-vec-persona-badge" style="--ic-accent:${accent}; --dept-accent:${accent}; width:${sizePx}px; height:${sizePx}px; flex-shrink:0;" aria-hidden="true">` +
        `<svg viewBox="0 0 28 28" width="${svgSize}" height="${svgSize}" fill="none" xmlns="http://www.w3.org/2000/svg">` +
          `<circle cx="14" cy="14" r="12.3" stroke="var(--ic-accent)" stroke-width="0.9" stroke-dasharray="2.6 2.4" opacity="0.42"/>` +
          inner +
        `</svg>` +
      `</div>`;
    }

    function renderInlineAgentSvg(agOrId, sizePx = 15, customAccent = null) {
      const ag = (typeof agOrId === 'string') ? (typeof AGENTS !== 'undefined' ? AGENTS[agOrId] : null) : agOrId;
      const accent = customAccent || resolveEntityAccentColor(ag, 'currentColor');
      return `<svg class="sc-vec-inline-svg" style="--ic-accent:${accent};" viewBox="0 0 28 28" width="${sizePx}" height="${sizePx}" fill="none" aria-hidden="true">${getAgentSvgInner(agOrId)}</svg>`;
    }

    function renderInlinePersonaSvg(pOrId, sizePx = 15, customAccent = null) {
      const p = (typeof pOrId === 'string') ? (typeof PERSONAS !== 'undefined' ? PERSONAS[pOrId] : null) : pOrId;
      const accent = customAccent || resolveEntityAccentColor(p, 'currentColor');
      return `<svg class="sc-vec-inline-svg" style="--ic-accent:${accent};" viewBox="0 0 28 28" width="${sizePx}" height="${sizePx}" fill="none" aria-hidden="true">${getPersonaSvgInner(pOrId)}</svg>`;
    }

    function renderSubPillarSvg(spOrId, sizePx = 20, customAccent = null) {
      const sp = (typeof spOrId === 'object' && spOrId) ? spOrId : null;
      const accent = customAccent || (sp && sp.color) || 'currentColor';
      return `<svg class="sc-vec-inline-svg" style="--ic-accent:${accent};" viewBox="0 0 28 28" width="${sizePx}" height="${sizePx}" fill="none" aria-hidden="true">${getSubPillarSvgInner(spOrId)}</svg>`;
    }
"""
    )


def validate_all_140_icons() -> dict[str, str]:
    cat = json.loads((ROOT / "data" / "supply_chain_catalog.json").read_text(encoding="utf-8"))
    agents = cat["agents"]
    personas = cat["personas"]

    assert len(AGENT_VECTOR_SVGS) == 60, f"Expected 60 Agent SVGs, got {len(AGENT_VECTOR_SVGS)}"
    assert set(AGENT_VECTOR_SVGS.keys()) == set(agents.keys()), (
        f"Agent SVG keys mismatch: missing={set(agents.keys()) - set(AGENT_VECTOR_SVGS.keys())}"
    )
    assert len(set(AGENT_VECTOR_SVGS.values())) == 60, "Every single one of the 60 Agents must have a unique SVG!"

    assert len(PERSONA_VECTOR_SVGS) == 60, f"Expected 60 Persona SVGs, got {len(PERSONA_VECTOR_SVGS)}"
    assert set(PERSONA_VECTOR_SVGS.keys()) == set(personas.keys()), (
        f"Persona SVG keys mismatch: missing={set(personas.keys()) - set(PERSONA_VECTOR_SVGS.keys())}"
    )
    assert len(set(PERSONA_VECTOR_SVGS.values())) == 60, "Every single one of the 60 Personas must have a unique SVG!"

    assert set(AGENT_VECTOR_SVGS.values()).isdisjoint(set(PERSONA_VECTOR_SVGS.values())), (
        "Agent SVGs and Persona SVGs must be 100% disjoint!"
    )
    assert len(SUBPILLAR_VECTOR_SVGS) == 20 and len(set(SUBPILLAR_VECTOR_SVGS.values())) == 20

    for svg in [*AGENT_VECTOR_SVGS.values(), *PERSONA_VECTOR_SVGS.values(), *SUBPILLAR_VECTOR_SVGS.values()]:
        assert "<animate" not in svg, "Icons must be static (no <animate>)"

    persona_by_agent = {}
    for pid, p in personas.items():
        if p.get("primaryAgentId"):
            persona_by_agent[p["primaryAgentId"]] = pid
    return persona_by_agent


def patch_index_html(persona_by_agent: dict[str, str]) -> None:
    idx_path = ROOT / "index.html"
    html = idx_path.read_text(encoding="utf-8")

    # 1. Inject CSS before </style> if not already present
    if "sc-vec-agent-badge" not in html:
        style_idx = html.index("  </style>")
        html = html[:style_idx] + CUSTOM_VECTOR_ICON_CSS + "\n" + html[style_idx:]

    # 2. Inject JS Vector Registry & Render Helpers right before `function renderSupplyChainWatermarkSvg`
    if "const AGENT_VECTOR_SVGS =" not in html:
        anchor = "    function renderSupplyChainWatermarkSvg("
        pos = html.index(anchor)
        html = html[:pos] + build_js_vector_helpers(persona_by_agent) + "\n" + html[pos:]

    # 3. Replace ALL Agent `✦` boxes, Persona `${p.icon}` emoji circles, and inline emojis across every view!
    replacements = [
        # 3a. Navbar Quick Menus (populateNavbarQuickMenus)
        (
            "<span>👥 Open Full Personas Directory (60)</span>",
            '<span style="display:inline-flex;align-items:center;gap:7px;">Open Full Personas Directory (60)</span>',
        ),
        (
            "<span>${p.icon} ${p.name}</span>",
            '<span style="display:inline-flex;align-items:center;gap:8px;">${renderInlinePersonaSvg(p, 15, p.subPillarColor || d.color)} ${p.name}</span>',
        ),
        (
            "<span>🤖 Open Full AI Agents Directory (60)</span>",
            '<span style="display:inline-flex;align-items:center;gap:7px;">Open Full AI Agents Directory (60)</span>',
        ),
        (
            "<span>${ag.name}</span>",
            '<span style="display:inline-flex;align-items:center;gap:8px;">${renderInlineAgentSvg(ag, 15, ag.subPillarColor || d.color)} ${cleanAgentName(ag.name)}</span>',
        ),
        # 3b. Homepage Sub-Pillar Cards & Persona Drawer (renderSubPillarDetail)
        (
            '<div class="subpillar-box-icon">${sp.icon}</div>',
            '<div class="subpillar-box-icon" style="--sp-color:${sp.color};">${renderSubPillarSvg(sp, 20, sp.color)}</div>',
        ),
        (
            "<span>👤 ${(sp.items || []).length} Personas</span>",
            "<span>${(sp.items || []).length} Personas</span>",
        ),
        (
            "${activeSubPillar.icon} ${activeSubPillar.name}",
            "${renderSubPillarSvg(activeSubPillar, 15, '#ffffff')} ${activeSubPillar.name}",
        ),
        (
            """                        <div class="human-avatar-circle" style="--dept-accent: ${activeSubPillar.color}; width:48px; height:48px; font-size:22px;">
                          ${p.icon}
                        </div>""",
            "                        ${renderPersonaIconBadge(p, 48, activeSubPillar.color)}",
        ),
        # 3c. Persona Detail Page (openPersonaPage)
        (
            "<span>👤 All Personas</span>",
            "<span>All Personas</span>",
        ),
        (
            "${other.icon} ${other.name}",
            "${renderInlinePersonaSvg(other, 15, pid === p.id ? '#ffffff' : (other.subPillarColor || dept.color))} ${other.name}",
        ),
        (
            """              <div class="human-avatar-circle" style="width:60px; height:60px; font-size:28px; --dept-accent:${dept.color};">
                ${p.icon}
              </div>""",
            "              ${renderPersonaIconBadge(p, 60, p.subPillarColor || dept.color)}",
        ),
        (
            """                        <div class="sc-flip-big-heading" style="font-size:21px;">
                          <div class="ai-bot-square" style="width:42px; height:42px; font-size:18px; flex-shrink:0;">✦</div>
                          <span>${cleanAgentName(ag.name)}</span>
                        </div>""",
            """                        <div class="sc-flip-big-heading" style="font-size:21px;">
                          ${renderAgentIconBadge(ag, 44, ag.subPillarColor || dept.color)}
                          <span>${cleanAgentName(ag.name)}</span>
                        </div>""",
        ),
        (
            '<div class="ai-bot-square" style="width:42px; height:42px; font-size:18px; flex-shrink:0;">✦</div>',
            "${renderAgentIconBadge(plugAgent, 44, plugAgent.subPillarColor || dept.color)}",
        ),
        # 3d. Agent Detail Page (openAgentPage)
        (
            "🤖 ${cleanAgentName(other.name)}",
            "${renderInlineAgentSvg(other, 15, other.id === ag.id ? '#ffffff' : (other.subPillarColor || dept.color))} ${cleanAgentName(other.name)}",
        ),
        (
            '<div class="ai-bot-square" style="width:52px; height:52px; font-size:24px;">✦</div>',
            "${renderAgentIconBadge(ag, 54, ag.subPillarColor || dept.color)}",
        ),
        (
            '<div class="sc-flip-icon-box">✦</div>',
            '<div class="sc-flip-icon-box">${renderInlineAgentSvg(ag, 20, ag.subPillarColor || dept.color)}</div>',
        ),
        (
            '<div class="sc-flip-icon-box">🚀</div>',
            '<div class="sc-flip-icon-box"><svg viewBox="0 0 24 24" width="18" height="18" fill="none"><path d="M5 17L10 12L13.5 15.5L19.5 8.5M15 8.5H19.5V13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>',
        ),
        (
            '<div class="sc-flip-icon-box">🚦</div>',
            '<div class="sc-flip-icon-box"><svg viewBox="0 0 24 24" width="18" height="18" fill="none"><rect x="8" y="3.5" width="8" height="17" rx="3" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="8" r="1.4" fill="currentColor"/><circle cx="12" cy="12" r="1.4" fill="currentColor" opacity="0.65"/><circle cx="12" cy="16" r="1.4" fill="currentColor" opacity="0.4"/></svg></div>',
        ),
        (
            '<div class="sc-flip-icon-box">🔒</div>',
            '<div class="sc-flip-icon-box"><svg viewBox="0 0 24 24" width="18" height="18" fill="none"><rect x="6" y="10.5" width="12" height="9.5" rx="2" stroke="currentColor" stroke-width="1.8"/><path d="M8.5 10.5V7.8C8.5 5.8 10 4.3 12 4.3C14 4.3 15.5 5.8 15.5 7.8V10.5" stroke="currentColor" stroke-width="1.8"/></svg></div>',
        ),
        (
            '<div class="sc-flip-icon-box">🎯</div>',
            '<div class="sc-flip-icon-box"><svg viewBox="0 0 24 24" width="18" height="18" fill="none"><circle cx="12" cy="12" r="7.5" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="3" fill="currentColor"/></svg></div>',
        ),
        (
            '<div class="sc-flip-icon-box">✅</div>',
            '<div class="sc-flip-icon-box"><svg viewBox="0 0 24 24" width="18" height="18" fill="none"><path d="M6.5 12.5L10.2 16.2L17.8 8.2" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/></svg></div>',
        ),
        (
            '<div class="sc-flip-icon-box">📜</div>',
            '<div class="sc-flip-icon-box"><svg viewBox="0 0 24 24" width="18" height="18" fill="none"><rect x="6" y="4.5" width="12" height="15" rx="2" stroke="currentColor" stroke-width="1.8"/><line x1="9" y1="9" x2="15" y2="9" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><line x1="9" y1="13" x2="13.5" y2="13" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></div>',
        ),
        (
            '<div class="sc-flip-icon-box">📥</div>',
            '<div class="sc-flip-icon-box"><svg viewBox="0 0 24 24" width="18" height="18" fill="none"><path d="M12 4.5V14.5M8.5 11.2L12 14.8L15.5 11.2M5 17.5V19.5H19V17.5" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg></div>',
        ),
        (
            '<div class="sc-flip-icon-box">⚡</div>',
            '<div class="sc-flip-icon-box"><svg viewBox="0 0 24 24" width="18" height="18" fill="none"><polygon points="13,3.8 6.5,13 11.8,13 11,20.2 17.5,11 12.2,11" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg></div>',
        ),
        (
            '<div class="sc-flip-icon-box">🔗</div>',
            '<div class="sc-flip-icon-box"><svg viewBox="0 0 24 24" width="18" height="18" fill="none"><path d="M10 14L14 10M8.5 16.5L7 18C5.6 19.4 5.6 21.6 7 23M8.5 11.5L6.8 13.2C5.2 14.8 5.2 17.3 6.8 18.9C8.4 20.5 10.9 20.5 12.5 18.9L14.2 17.2M15.5 12.5L17.2 10.8C18.8 9.2 18.8 6.7 17.2 5.1C15.6 3.5 13.1 3.5 11.5 5.1L9.8 6.8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></div>',
        ),
        # 3e. Value Chain Stage Page (openValueChainPage)
        (
            '<div class="human-avatar-circle" style="--dept-accent: ${ownerDept.color}; width:42px; height:42px; font-size:20px;">${ownerPersona.icon}</div>',
            "${renderPersonaIconBadge(ownerPersona, 44, ownerPersona.subPillarColor || ownerDept.color)}",
        ),
        (
            """                <div class="ai-agent-chip-card"
                     style="padding: 14px 18px;"
                     onclick="openAgentPage('${stageAgent.id}', true, event)">
                  <div style="display:flex; align-items:center; gap:12px;">
                    <div class="ai-bot-square" style="width:40px; height:40px;">✦</div>""",
            """                <div class="ai-agent-chip-card"
                     style="padding: 14px 18px; --ag-accent:${stageAgent.subPillarColor || ownerDept.color};"
                     onclick="openAgentPage('${stageAgent.id}', true, event)">
                  <div style="display:flex; align-items:center; gap:12px;">
                    ${renderAgentIconBadge(stageAgent, 42, stageAgent.subPillarColor || ownerDept.color)}""",
        ),
        # 3f. Directory Page (openPersonasDirectoryPage & renderDirectoryCardsHtml — exact screen in user's screenshot!)
        (
            "<span>👤 Personas</span>",
            '<span style="display:inline-flex;align-items:center;gap:6px;"><svg class="sc-vec-inline-svg" viewBox="0 0 28 28" width="15" height="15" fill="none"><circle cx="14" cy="10" r="3.6" stroke="currentColor" stroke-width="1.9"/><path d="M7 21.5C7.8 17.8 10.5 15.8 14 15.8C17.5 15.8 20.2 17.8 21 21.5" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/></svg> Personas</span>',
        ),
        (
            "<span>✦ AI Agents</span>",
            '<span style="display:inline-flex;align-items:center;gap:6px;"><svg class="sc-vec-inline-svg" viewBox="0 0 28 28" width="15" height="15" fill="none"><rect x="6" y="6" width="16" height="16" rx="3.5" stroke="currentColor" stroke-width="1.9"/><circle cx="14" cy="14" r="2.6" fill="currentColor"/></svg> AI Agents</span>',
        ),
        (
            """                  <div class="ai-agent-chip-card" style="padding:20px 22px;" onclick="openAgentPage('${ag.id}', true, event)">
                    <div style="display:flex; align-items:center; gap:14px; min-width:0;">
                      <div class="ai-bot-square" style="width:44px; height:44px; font-size:18px; flex-shrink:0;">✦</div>""",
            """                  <div class="ai-agent-chip-card" style="padding:20px 22px; --ag-accent:#6366f1;" onclick="openAgentPage('${ag.id}', true, event)">
                    <div style="display:flex; align-items:center; gap:14px; min-width:0;">
                      ${renderAgentIconBadge(ag, 46, '#6366f1')}""",
        ),
        (
            """                    <div class="ai-agent-chip-card" style="padding:20px 22px;" onclick="openAgentPage('${ag.id}', true, event)">
                      <div style="display:flex; align-items:center; gap:14px; min-width:0;">
                        <div class="ai-bot-square" style="width:44px; height:44px; font-size:18px; flex-shrink:0;">✦</div>""",
            """                    <div class="ai-agent-chip-card" style="padding:20px 22px; --ag-accent:${ag.subPillarColor || dept.color};" onclick="openAgentPage('${ag.id}', true, event)">
                      <div style="display:flex; align-items:center; gap:14px; min-width:0;">
                        ${renderAgentIconBadge(ag, 46, ag.subPillarColor || dept.color)}""",
        ),
        (
            '<div class="human-avatar-circle" style="--dept-accent: ${dept.color}; flex-shrink:0;">${p.icon}</div>',
            "${renderPersonaIconBadge(p, 46, p.subPillarColor || dept.color)}",
        ),
        # 3g. Architecture Page (selectAiFunctionTile & openArchitecturePage)
        (
            '<div class="ai-bot-square" style="width:34px; height:34px; font-size:15px; flex-shrink:0;">✦</div>',
            "${renderAgentIconBadge(ag, 36, ag.subPillarColor || dept.color || tile.accent)}",
        ),
        (
            '<div class="ai-bot-square" style="width:38px; height:38px; font-size:16px; flex-shrink:0;">✦</div>',
            "${renderAgentIconBadge(ag, 40, ag.subPillarColor || dept.color)}",
        ),
        # 3h. Periodic Table Page (openPeriodicTablePage)
        (
            "${pOwner.icon} ${pOwner.name} &rarr;",
            "${renderInlinePersonaSvg(pOwner, 15, grpColor)} ${pOwner.name} &rarr;",
        ),
        (
            "<span>${sp.icon} ${sp.name}</span>",
            '<span style="display:inline-flex;align-items:center;gap:6px;">${renderSubPillarSvg(sp, 15, sp.color || grp.color)} ${sp.name}</span>',
        ),
        (
            """                <div class="pt-side-badge" style="background:${selGrp.color}; width:44px; height:44px; font-size:15px;">
                  ${selMeta.sym}
                </div>""",
            "                ${renderAgentIconBadge(selAg, 46, selAg.subPillarColor || selGrp.color)}",
        ),
        (
            """                    <div style="font-size:14px; font-weight:800; color:var(--text-primary);">
                      ${selPrimaryPersona.icon} ${selPrimaryPersona.name}
                    </div>""",
            """                    <div style="display:flex; align-items:center; gap:8px; font-size:14px; font-weight:800; color:var(--text-primary);">
                      ${renderInlinePersonaSvg(selPrimaryPersona, 16, selGrp.color)}
                      <span>${selPrimaryPersona.name}</span>
                    </div>""",
        ),
        # 3i. Mind Map Page (openMindMapPage)
        (
            "<span>${activeSubPillar ? activeSubPillar.icon : '📦'}</span>",
            "<span>${activeSubPillar ? renderSubPillarSvg(activeSubPillar, 15, spAccent) : ''}</span>",
        ),
        (
            '<span style="color:${spAccent};">✦</span>',
            "${renderInlineAgentSvg(topAg, 15, spAccent)}",
        ),
        (
            "${topPer.icon} ${topPer.name} &rarr;",
            "${renderInlinePersonaSvg(topPer, 15, spAccent)} ${topPer.name} &rarr;",
        ),
        (
            """                        <div style="width:44px; height:44px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px; background:${nodeCol}18; border:1px solid ${nodeCol}45; flex-shrink:0;">
                          ${sp.icon}
                        </div>""",
            """                        <div style="width:44px; height:44px; border-radius:12px; display:flex; align-items:center; justify-content:center; background:${nodeCol}18; border:1px solid ${nodeCol}45; color:${nodeCol}; flex-shrink:0;">
                          ${renderSubPillarSvg(sp, 22, nodeCol)}
                        </div>""",
        ),
        (
            '<div class="ai-bot-square" style="width:44px; height:44px; font-size:18px; flex-shrink:0; background:${spAccent}18; color:${spAccent}; border-color:${spAccent}45;">✦</div>',
            "${renderAgentIconBadge(ag, 46, spAccent)}",
        ),
        (
            """                            <div class="human-avatar-circle" style="width:50px; height:50px; font-size:23px; --dept-accent:${spAccent};">
                              ${p.icon}
                            </div>""",
            "                            ${renderPersonaIconBadge(p, 50, spAccent)}",
        ),
        # 3j. Case Studies / Backed Problem Data Hub (openEvidenceHubPage)
        (
            "${sp.icon || '📦'} ${sp.name}",
            "${renderSubPillarSvg(sp, 14, isAct ? '#ffffff' : col)} ${sp.name}",
        ),
        (
            "${p.icon} ${p.name}",
            "${renderInlinePersonaSvg(p, 14, isFoc ? '#ffffff' : col)} ${p.name}",
        ),
        (
            "✦ ${cleanAgentName(ag.name)} &rarr;",
            "${renderInlineAgentSvg(ag, 14, ag.subPillarColor || '#10b981')} ${cleanAgentName(ag.name)} &rarr;",
        ),
        (
            "✦ ${cleanAgentName(ag.name)}",
            "${renderInlineAgentSvg(ag, 14, isFoc ? '#ffffff' : (ag.subPillarColor || '#10b981'))} ${cleanAgentName(ag.name)}",
        ),
        (
            """        const entityIcon = isAgent ? '✦' : (focusedEntity.icon || '👤');
        const dimLabel = focusedProof.dimension || focusedEntity.impactDimension || 'Operational Impact';
        const headlineImpact = isAgent
          ? (focusedProof.agentBadge || focusedEntity.badge || 'Modeled ROI')
          : `${focusedEntity.headlineStat} (${focusedEntity.toilHoursBefore} → ${focusedEntity.toilHoursAfter})`;
        const spotAccent = (focusedSubPillar && focusedSubPillar.color) || (focusedDept && focusedDept.color) || '#10b981';""",
            """        const spotAccent = (focusedSubPillar && focusedSubPillar.color) || (focusedDept && focusedDept.color) || '#10b981';
        const entityIcon = isAgent ? renderAgentIconBadge(focusedEntity, 40, spotAccent) : renderPersonaIconBadge(focusedEntity, 40, spotAccent);
        const dimLabel = focusedProof.dimension || focusedEntity.impactDimension || 'Operational Impact';
        const headlineImpact = isAgent
          ? (focusedProof.agentBadge || focusedEntity.badge || 'Modeled ROI')
          : `${focusedEntity.headlineStat} (${focusedEntity.toilHoursBefore} → ${focusedEntity.toilHoursAfter})`;""",
        ),
        (
            "${focusedSubPillar ? `<span style=\"color:var(--text-muted);\">&rarr;</span><span style=\"font-family:var(--font-mono); font-size:11px; font-weight:800; color:var(--text-secondary);\">${focusedSubPillar.icon || ''} ${focusedSubPillar.name}</span>` : ''}",
            "${focusedSubPillar ? `<span style=\"color:var(--text-muted);\">&rarr;</span><span style=\"display:inline-flex;align-items:center;gap:5px;font-family:var(--font-mono); font-size:11px; font-weight:800; color:var(--text-secondary);\">${renderSubPillarSvg(focusedSubPillar, 13, spotAccent)} ${focusedSubPillar.name}</span>` : ''}",
        ),
        (
            """                  <h2 style="font-family:var(--font-display); font-size:clamp(20px, 2.2vw, 26px); font-weight:800; color:var(--text-primary); margin:0;">
                    ${entityIcon} Problem Data &amp; Potential Impact — ${entityLabel}
                  </h2>""",
            """                  <div style="display:flex; align-items:center; gap:11px;">
                    ${entityIcon}
                    <h2 style="font-family:var(--font-display); font-size:clamp(20px, 2.2vw, 26px); font-weight:800; color:var(--text-primary); margin:0;">
                      Problem Data &amp; Potential Impact — ${entityLabel}
                    </h2>
                  </div>""",
        ),
        (
            "${p.icon || '👤'} ${p.name} &rarr;",
            "${renderInlinePersonaSvg(p, 14, d ? d.color : 'currentColor')} ${p.name} &rarr;",
        ),
        (
            """        const personaChips = liveMeta.personas.slice(0, 4).map(p => `
          <button type="button" class="sc-tech-pill" onclick="openPersonaPage('${p.id}', true, event)" style="cursor:pointer; font-size:11.5px; font-weight:700; padding:4px 10px;">
            ${renderInlinePersonaSvg(p, 14, d ? d.color : 'currentColor')} ${p.name} &rarr;
          </button>
        `).join('');""",
            """        const personaChips = liveMeta.personas.slice(0, 4).map(p => `
          <button type="button" class="sc-tech-pill" onclick="openPersonaPage('${p.id}', true, event)" style="cursor:pointer; font-size:11.5px; font-weight:700; padding:4px 10px;">
            ${renderInlinePersonaSvg(p, 14, p.subPillarColor || '#2563eb')} ${p.name} &rarr;
          </button>
        `).join('');""",
        ),
    ]

    for old, new in replacements:
        if old not in html:
            raise RuntimeError(f"Expected snippet not found in index.html:\n{old[:140]}")
        html = html.replace(old, new)

    # Verify zero hardcoded `<div class="ai-bot-square"...>✦</div>` remain anywhere in index.html!
    assert '>✦</div>' not in html, "Leftover hardcoded `>✦</div>` Agent box found in index.html!"
    assert "${p.icon}" not in html, "Leftover `${p.icon}` emoji found in index.html!"
    assert "${other.icon}" not in html, "Leftover `${other.icon}` emoji found in index.html!"
    assert "${ownerPersona.icon}" not in html, "Leftover `${ownerPersona.icon}` emoji found in index.html!"

    idx_path.write_text(html, encoding="utf-8")


def sync_derived_html_and_mirrors() -> None:
    html = (ROOT / "index.html").read_text(encoding="utf-8")

    # Regenerate periodic_table.html & mind_map.html from index.html cleanly
    pt_boot = """
  <script>
    window.addEventListener('DOMContentLoaded', function() {
      if (!window.location.hash || window.location.hash === '#home') {
        if (typeof openPeriodicTablePage === 'function') openPeriodicTablePage('all', null, false);
      }
    });
  </script>
</body>"""
    mm_boot = """
  <script>
    window.addEventListener('DOMContentLoaded', function() {
      if (!window.location.hash || window.location.hash === '#home') {
        if (typeof openMindMapPage === 'function') openMindMapPage('mindmap', null, null, false);
      }
    });
  </script>
</body>"""

    (ROOT / "periodic_table.html").write_text(html.replace("</body>", pt_boot, 1), encoding="utf-8")
    (ROOT / "mind_map.html").write_text(html.replace("</body>", mm_boot, 1), encoding="utf-8")

    for target_dir in [ROOT / "docs", ROOT / "zipline_dist"]:
        if target_dir.exists():
            for fname in ["index.html", "periodic_table.html", "mind_map.html"]:
                shutil.copy2(ROOT / fname, target_dir / fname)


def main() -> None:
    persona_by_agent = validate_all_140_icons()
    patch_index_html(persona_by_agent)
    sync_derived_html_and_mirrors()
    print("✅ Upgraded 60 AI Agents + 60 Personas + 20 Sub-Pillars to unique static CAD vector SVGs (0 emojis, 0 clone icons)!")


if __name__ == "__main__":
    main()

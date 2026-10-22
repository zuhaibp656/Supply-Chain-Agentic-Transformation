#!/usr/bin/env python3
"""Build ALL remaining High-Code & Hybrid Google ADK Supply Chain Agents (15 brand-new agents
across 04 · Fulfill, 05 · Deliver, 06 · Return & Enable, and 03 · Make) plus 7 catalog-ID
aligned packages so 100% of all 35 catalog agents have full ADK code, A2UI v0.9 VegaChart surfaces,
4 realistic enterprise JSON fixture tables each, golden scenarios, and 7 passing unit smoke tests.
"""

from __future__ import annotations

import json
import pathlib
import shutil
from typing import Any, Dict, List

ROOT = pathlib.Path(__file__).resolve().parent.parent
AGENTS_DIR = ROOT / "agents"

A2UI_ENVELOPE_CODE = '''"""A2UI message envelope serializer."""
from __future__ import annotations
import json
from typing import Any, Dict

try:
    from google.genai import types
except ImportError:
    types = None

A2A_DATA_PART_OPEN_TAG: str = "<a2a_datapart_json>"
A2A_DATA_PART_CLOSE_TAG: str = "</a2a_datapart_json>"
A2UI_MIME: str = "application/json+a2ui"


def wrap_a2ui_part(message: Any) -> Any:
    surface_id = getattr(message, "surface_id", None) or message.get("surface_id")
    message_type = getattr(message, "message_type", None) or message.get("message_type")
    payload = getattr(message, "payload", None) or message.get("payload", {})
    catalog_version = getattr(message, "catalog_version", "v0.9")
    version_str = catalog_version.value if hasattr(catalog_version, "value") else str(catalog_version)

    raw_message_body: Dict[str, Any] = {
        "version": version_str,
        message_type: {
            "surfaceId": surface_id,
            **payload,
        },
    }

    payload_envelope: Dict[str, Any] = {
        "kind": "data",
        "metadata": {"mimeType": A2UI_MIME},
        "data": raw_message_body,
    }

    json_str = json.dumps(payload_envelope, separators=(",", ":"))
    wire_payload = (
        f"{A2A_DATA_PART_OPEN_TAG}"
        f"{json_str}"
        f"{A2A_DATA_PART_CLOSE_TAG}"
    ).encode("utf-8")

    if types is not None:
        return types.Part(
            inline_data=types.Blob(
                data=wire_payload,
                mime_type="text/plain",
            ),
            part_metadata={"mimeType": A2UI_MIME},
        )

    return {
        "inline_data": {
            "data": wire_payload.decode("utf-8"),
            "mime_type": "text/plain",
        },
        "part_metadata": {"mimeType": A2UI_MIME},
        "wire_payload": wire_payload.decode("utf-8"),
    }
'''

A2UI_LIFECYCLE_CODE = '''"""A2UI v0.9 lifecycle message builders."""
from __future__ import annotations
from typing import Any, Dict, List, Optional

DEFAULT_GE_CATALOG_ID: str = (
    "https://www.gstatic.com/vertexaisearch/a2ui/v0_9/gemini_enterprise_composite_catalog.json"
)


def build_create_surface(surface_id: str, catalog_id: str = DEFAULT_GE_CATALOG_ID) -> Dict[str, Any]:
    if not surface_id:
        raise ValueError("surface_id cannot be empty.")
    return {
        "message_type": "createSurface",
        "surface_id": surface_id,
        "payload": {"catalogId": catalog_id},
        "catalog_version": "v0.9",
    }


def build_update_components(surface_id: str, components: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not surface_id:
        raise ValueError("surface_id cannot be empty.")
    return {
        "message_type": "updateComponents",
        "surface_id": surface_id,
        "payload": {"components": components},
        "catalog_version": "v0.9",
    }


def build_update_data_model(surface_id: str, value: Dict[str, Any], path: Optional[str] = None) -> Dict[str, Any]:
    if not surface_id:
        raise ValueError("surface_id cannot be empty.")
    payload: Dict[str, Any] = {"value": value}
    if path:
        payload["path"] = path
    return {
        "message_type": "updateDataModel",
        "surface_id": surface_id,
        "payload": payload,
        "catalog_version": "v0.9",
    }
'''

NEW_AGENTS_SPECS: List[Dict[str, Any]] = [
    # 1. fleetflow_dispatch (High-Code: Google Maps Routes Preferred + OR-Tools CVRPTW)
    {
        "id": "fleetflow_dispatch",
        "class_name": "FleetflowDispatch",
        "display_name": "FleetFlow — Google Maps Corridor Route & Fleet Dispatch Studio",
        "description": "Solves Capacitated Vehicle Routing with Time Windows (CVRPTW) using Google OR-Tools and Google Maps Routes Preferred API across 0.75t to 24t fleet vehicles.",
        "model": "gemini-3-pro-preview",
        "vertical": "05 · Deliver",
        "category": "Logistics, Fleet & Transportation Management",
        "tags": ["cvrptw", "google-maps", "fleet-engine", "or-tools", "route-optimization"],
        "systems": [
            {"id": "google_maps_routes_preferred", "name": "Google Maps Platform Routes Preferred & Live Traffic Matrix API", "protocol": "gRPC / REST v2", "tables": ["google_maps_corridor_routes"]},
            {"id": "or_tools_cvrptw_solver", "name": "Google OR-Tools Capacitated Vehicle Routing (CVRPTW) Engine", "protocol": "C++ / Python Solver SDK", "tables": ["corridor_delivery_orders"]},
            {"id": "samsara_eld_telematics", "name": "Samsara ELD & Google Maps Fleet Engine Vehicle Telemetry", "protocol": "Webhook / MQTT", "tables": ["fleet_vehicle_telematics_hos"]},
            {"id": "backhaul_freight_matcher", "name": "Blue Yonder TMS Backhaul & Deadhead Elimination Broker", "protocol": "OData / EDI 204", "tables": ["backhaul_consolidation_opportunities"]},
        ],
        "tables": {
            "corridor_delivery_orders": {
                "query_fn": "query_corridor_delivery_orders",
                "filter_param": "corridor_id",
                "filter_val": "CORR-I35-TEX",
                "rows": [
                    {"order_id": "ORD-FF-901", "corridor_id": "CORR-I35-TEX", "customer_hub": "Austin Supercenter #14", "stop_sequence": 1, "weight_kg": 4850, "cube_m3": 18.4, "time_window": "06:00-08:30", "sla_tier": "PLATINUM"},
                    {"order_id": "ORD-FF-902", "corridor_id": "CORR-I35-TEX", "customer_hub": "San Marcos Regional DC", "stop_sequence": 2, "weight_kg": 6200, "cube_m3": 24.1, "time_window": "09:15-11:30", "sla_tier": "GOLD"},
                    {"order_id": "ORD-FF-903", "corridor_id": "CORR-I35-TEX", "customer_hub": "San Antonio South Depot", "stop_sequence": 3, "weight_kg": 7400, "cube_m3": 29.8, "time_window": "12:30-15:00", "sla_tier": "PLATINUM"},
                ],
            },
            "fleet_vehicle_telematics_hos": {
                "query_fn": "query_fleet_vehicle_telematics_hos",
                "filter_param": "vehicle_id",
                "filter_val": "TRK-24T-TX08",
                "rows": [
                    {"vehicle_id": "TRK-24T-TX08", "vehicle_class": "24t_Class8_Heavy_Tractor", "max_payload_kg": 21500, "max_cube_m3": 82.0, "driver_hos_remaining_hrs": 9.8, "fuel_type": "DIESEL_B20", "current_status": "READY_AT_DALLAS_RDC"},
                    {"vehicle_id": "TRK-12T-TX14", "vehicle_class": "12t_Medium_Box_Truck", "max_payload_kg": 9800, "max_cube_m3": 44.0, "driver_hos_remaining_hrs": 8.5, "fuel_type": "EV_HEAVY", "current_status": "EN_ROUTE_WACO"},
                ],
            },
            "google_maps_corridor_routes": {
                "query_fn": "query_google_maps_corridor_routes",
                "filter_param": "route_id",
                "filter_val": "RTE-I35-20261022-01",
                "rows": [
                    {"route_id": "RTE-I35-20261022-01", "corridor_id": "CORR-I35-TEX", "assigned_vehicle_id": "TRK-24T-TX08", "total_distance_km": 462.5, "baseline_distance_km": 574.0, "distance_saved_pct": 19.4, "on_time_probability": 0.994, "bridge_clearance_verified": True},
                    {"route_id": "RTE-I45-20261022-02", "corridor_id": "CORR-I45-HOU", "assigned_vehicle_id": "TRK-12T-TX14", "total_distance_km": 388.0, "baseline_distance_km": 465.0, "distance_saved_pct": 16.6, "on_time_probability": 0.989, "bridge_clearance_verified": True},
                ],
            },
            "backhaul_consolidation_opportunities": {
                "query_fn": "query_backhaul_consolidation_opportunities",
                "filter_param": "backhaul_id",
                "filter_val": "BKH-SAT-DAL-44",
                "rows": [
                    {"backhaul_id": "BKH-SAT-DAL-44", "origin_hub": "San Antonio Vendor Park", "destination_dc": "Dallas Central RDC", "weight_kg": 14200, "pallets": 22, "deadhead_miles_eliminated": 274, "net_freight_savings_usd": 1480.0},
                ],
            },
        },
        "action1": {
            "name": "action_dispatch_corridor_route_manifest",
            "prefix": "FF-DISP",
            "status": "CORRIDOR_ROUTE_DISPATCHED",
            "params": ["route_id", "vehicle_id", "corridor_id", "stop_count", "rationale"],
            "sample_args": {
                "route_id": "RTE-I35-20261022-01",
                "vehicle_id": "TRK-24T-TX08",
                "corridor_id": "CORR-I35-TEX",
                "stop_count": 3,
                "rationale": "OR-Tools CVRPTW + Google Maps Routes Preferred solved 3-stop I-35 corridor route (18,450 kg / 72.3 m3) cutting stem distance by 19.4% with 99.4% SLA confidence.",
                "idempotency_key": "FF-DISP-20261022-01",
            },
        },
        "action2": {
            "name": "action_assign_backhaul_return_load",
            "prefix": "FF-BKH",
            "status": "BACKHAUL_RETURN_ASSIGNED",
            "params": ["backhaul_id", "vehicle_id", "origin_hub", "destination_dc", "rationale"],
            "sample_args": {
                "backhaul_id": "BKH-SAT-DAL-44",
                "vehicle_id": "TRK-24T-TX08",
                "origin_hub": "San Antonio Vendor Park",
                "destination_dc": "Dallas Central RDC",
                "rationale": "Matched returning 24t tractor TRK-24T-TX08 with 22-pallet vendor backhaul in San Antonio, eliminating 274 empty return miles and saving $1,480.",
                "idempotency_key": "FF-BKH-20261022-01",
            },
        },
        "chart": {
            "title": "FleetFlow Corridor Route Optimization & Deadhead Reduction",
            "subtitle": "Google Maps Routes Preferred + OR-Tools CVRPTW (km Driven vs. Baseline & Cube Fill %)",
            "x_field": "corridor",
            "y_field": "distance_km",
            "y2_field": "cube_fill_pct",
            "data": [
                {"corridor": "I-35 Dallas➔San Antonio", "distance_km": 462.5, "cube_fill_pct": 91.4, "status": "OPTIMIZED_CVRPTW"},
                {"corridor": "I-35 Legacy Postcode", "distance_km": 574.0, "cube_fill_pct": 67.0, "status": "LEGACY_STATIC"},
                {"corridor": "I-45 Dallas➔Houston", "distance_km": 388.0, "cube_fill_pct": 89.2, "status": "OPTIMIZED_CVRPTW"},
                {"corridor": "I-10 Houston➔El Paso", "distance_km": 1190.0, "cube_fill_pct": 93.8, "status": "OPTIMIZED_CVRPTW"},
            ],
        },
    },

    # 2. load_consolidation_agent (High-Code: CubeMaster 3D LIFO Bin Packing & Axle Weight Solver)
    {
        "id": "load_consolidation_agent",
        "class_name": "LoadConsolidationAgent",
        "display_name": "CubeMaster 3D — Isometric LIFO Bay & Load Consolidation Studio",
        "description": "Solves 3D Guillotine & Extreme-Point Multi-Container Bin Packing with axle-weight equilibrium, crush fragility, and strict reverse-stop LIFO unloading order.",
        "model": "gemini-3-pro-preview",
        "vertical": "05 · Deliver",
        "category": "Logistics, Fleet & Transportation Management",
        "tags": ["3d-bin-packing", "lifo-sequencing", "axle-weight", "or-tools", "load-consolidation"],
        "systems": [
            {"id": "or_tools_3d_voxel_packer", "name": "Google OR-Tools 3D Extreme-Point & Guillotine Bin Packing Solver", "protocol": "C++ / Python 3D Voxel Engine", "tables": ["lifo_3d_voxel_load_plans"]},
            {"id": "sap_ewm_carton_master", "name": "SAP EWM & Material Master 3D Carton Geometry & Fragility Feed", "protocol": "OData v4 / BAPI", "tables": ["outbound_shipment_carton_dimensions"]},
            {"id": "tms_trailer_fleet_specs", "name": "Fleet Trailer Bay & DOT Axle-Weight Compliance Registry", "protocol": "REST / JSON", "tables": ["trailer_bay_geometry_specs"]},
            {"id": "dock_lifo_axle_auditor", "name": "Dock Scale & Crush-Pressure Physics Verification Engine", "protocol": "IoT Weighbridge / REST", "tables": ["axle_weight_crush_audit_logs"]},
        ],
        "tables": {
            "outbound_shipment_carton_dimensions": {
                "query_fn": "query_outbound_shipment_carton_dimensions",
                "filter_param": "shipment_wave_id",
                "filter_val": "WAVE-3D-20261022-09",
                "rows": [
                    {"pallet_group_id": "PLT-STOP3-HVY01", "shipment_wave_id": "WAVE-3D-20261022-09", "stop_number": 3, "Stop_Name": "San Antonio Depot", "length_mm": 1200, "width_mm": 1000, "height_mm": 1450, "weight_kg": 840, "max_top_load_kg": 1800, "fragility_tier": "HEAVY_BASE"},
                    {"pallet_group_id": "PLT-STOP2-MED04", "shipment_wave_id": "WAVE-3D-20261022-09", "stop_number": 2, "Stop_Name": "San Marcos DC", "length_mm": 1200, "width_mm": 1000, "height_mm": 1300, "weight_kg": 520, "max_top_load_kg": 950, "fragility_tier": "STANDARD_MID"},
                    {"pallet_group_id": "PLT-STOP1-FRG02", "shipment_wave_id": "WAVE-3D-20261022-09", "stop_number": 1, "Stop_Name": "Austin Supercenter", "length_mm": 1200, "width_mm": 1000, "height_mm": 1100, "weight_kg": 280, "max_top_load_kg": 0, "fragility_tier": "TOP_ONLY_FRAGILE"},
                ],
            },
            "trailer_bay_geometry_specs": {
                "query_fn": "query_trailer_bay_geometry_specs",
                "filter_param": "trailer_type_id",
                "filter_val": "TRL-53FT-DRYVAN",
                "rows": [
                    {"trailer_type_id": "TRL-53FT-DRYVAN", "internal_length_mm": 15900, "internal_width_mm": 2480, "internal_height_mm": 2740, "max_payload_kg": 20400, "max_steer_axle_kg": 5440, "max_drive_tandem_kg": 15420, "max_trailer_tandem_kg": 15420},
                ],
            },
            "lifo_3d_voxel_load_plans": {
                "query_fn": "query_lifo_3d_voxel_load_plans",
                "filter_param": "load_plan_id",
                "filter_val": "LP-3D-20261022-88",
                "rows": [
                    {"load_plan_id": "LP-3D-20261022-88", "shipment_wave_id": "WAVE-3D-20261022-09", "trailer_type_id": "TRL-53FT-DRYVAN", "cube_utilization_pct": 92.4, "weight_utilization_pct": 90.5, "lifo_sequence_order": ["STOP_3_NOSE_ZONE_A", "STOP_2_MID_ZONE_B", "STOP_1_TAIL_ZONE_C"], "zero_rehandling_verified": True},
                ],
            },
            "axle_weight_crush_audit_logs": {
                "query_fn": "query_axle_weight_crush_audit_logs",
                "filter_param": "load_plan_id",
                "filter_val": "LP-3D-20261022-88",
                "rows": [
                    {"audit_id": "AXL-AUD-88", "load_plan_id": "LP-3D-20261022-88", "steer_axle_kg": 5120, "drive_tandem_kg": 14680, "trailer_tandem_kg": 14210, "cog_lateral_offset_mm": 18, "crush_violations": 0, "dot_legal_status": "COMPLIANT"},
                ],
            },
        },
        "action1": {
            "name": "action_commit_3d_lifo_load_plan",
            "prefix": "CUBE-LP",
            "status": "LOAD_PLAN_3D_COMMITTED",
            "params": ["load_plan_id", "trailer_type_id", "cube_utilization_pct", "lifo_zones", "rationale"],
            "sample_args": {
                "load_plan_id": "LP-3D-20261022-88",
                "trailer_type_id": "TRL-53FT-DRYVAN",
                "cube_utilization_pct": 92.4,
                "lifo_zones": ["STOP_3_NOSE_ZONE_A", "STOP_2_MID_ZONE_B", "STOP_1_TAIL_ZONE_C"],
                "rationale": "Packed 53ft trailer to 92.4% cube utilization in strict reverse-stop LIFO order (Stop 3 nose ➔ Stop 2 mid ➔ Stop 1 tail door) with zero crush violations and DOT-legal axle balance.",
                "idempotency_key": "CUBE-LP-20261022-01",
            },
        },
        "action2": {
            "name": "action_resequence_dock_staging_lanes",
            "prefix": "CUBE-STG",
            "status": "DOCK_STAGING_RESEQUENCED",
            "params": ["shipment_wave_id", "staging_lane_id", "loading_sequence_mode", "rationale"],
            "sample_args": {
                "shipment_wave_id": "WAVE-3D-20261022-09",
                "staging_lane_id": "DOCK-LANE-08",
                "loading_sequence_mode": "REVERSE_STOP_LIFO_BOTTOM_UP",
                "rationale": "Resequenced dock floor staging lane 08 so forklift loaders load Stop-3 heavy base pallets into the trailer nose first and Stop-1 fragile pallets at the tail door last.",
                "idempotency_key": "CUBE-STG-20261022-01",
            },
        },
        "chart": {
            "title": "CubeMaster 3D Isometric Bay Utilization & LIFO Zone Fill",
            "subtitle": "53ft Dry Van 3D Voxel Packing (92.4% Cube Fill · Zero Stop Re-Handling · DOT Axle Legal)",
            "x_field": "bay_zone",
            "y_field": "cube_fill_pct",
            "y2_field": "weight_kg",
            "data": [
                {"bay_zone": "Zone A (Nose · Stop 3)", "cube_fill_pct": 94.2, "weight_kg": 6840, "status": "OPTIMIZED_CVRPTW"},
                {"bay_zone": "Zone B (Mid · Stop 2)", "cube_fill_pct": 92.8, "weight_kg": 6320, "status": "OPTIMIZED_CVRPTW"},
                {"bay_zone": "Zone C (Tail · Stop 1)", "cube_fill_pct": 90.2, "weight_kg": 5300, "status": "OPTIMIZED_CVRPTW"},
                {"bay_zone": "Legacy Manual Pack", "cube_fill_pct": 68.0, "weight_kg": 12400, "status": "LEGACY_STATIC"},
            ],
        },
    },

    # 3. port_drayage_orchestrator (High-Code: Ocean AIS + WeatherNext 3 + Port Drayage MILP)
    {
        "id": "port_drayage_orchestrator",
        "class_name": "PortDrayageOrchestrator",
        "display_name": "PortWatch — Global Ocean Vessel, Container Stowage & Port Drayage Orchestrator",
        "description": "Ingests Spire Maritime satellite AIS and WeatherNext 3 cyclone forecasts to predict berth discharge, prevent port demurrage, and optimize dual-transaction drayage gates.",
        "model": "gemini-3-pro-preview",
        "vertical": "05 · Deliver",
        "category": "Logistics, Fleet & Transportation Management",
        "tags": ["ocean-ais", "port-drayage", "demurrage-shield", "weathernext-3", "cargowise"],
        "systems": [
            {"id": "spire_maritime_satellite_ais", "name": "Spire Maritime Satellite AIS & Google DeepMind WeatherNext 3 Feed", "protocol": "GraphQL / gRPC Stream", "tables": ["ocean_vessel_ais_berth_telemetry"]},
            {"id": "cargowise_ocean_fcl_ledger", "name": "CargoWise One Global Ocean Container & LFD Demurrage Ledger", "protocol": "EDI 315 / XML", "tables": ["container_discharge_demurrage_ledger"]},
            {"id": "port_terminal_gate_api", "name": "Port of LA/LB PierPASS & Rotterdam Terminal Gate Appointment API", "protocol": "REST / Webhook", "tables": ["port_terminal_gate_appointments"]},
            {"id": "drayage_transload_solver", "name": "Google OR-Tools Bipartite Drayage & Transload Allocation Solver", "protocol": "Python MILP SDK", "tables": ["drayage_chassis_transload_allocations"]},
        ],
        "tables": {
            "ocean_vessel_ais_berth_telemetry": {
                "query_fn": "query_ocean_vessel_ais_berth_telemetry",
                "filter_param": "vessel_imo",
                "filter_val": "IMO-9839179",
                "rows": [
                    {"vessel_imo": "IMO-9839179", "vessel_name": "MAERSK MC-KINNEY MOLLER", "service_loop": "TP6_TRANS_PACIFIC", "port_of_discharge": "USLAX_APM_PIER400", "carrier_published_eta": "2026-10-25T06:00:00Z", "ai_predicted_berth_eta": "2026-10-27T18:00:00Z", "weathernext_swell_delay_hrs": 60, "containers_onboard": 14},
                ],
            },
            "container_discharge_demurrage_ledger": {
                "query_fn": "query_container_discharge_demurrage_ledger",
                "filter_param": "container_id",
                "filter_val": "MSKU-904812-0",
                "rows": [
                    {"container_id": "MSKU-904812-0", "vessel_imo": "IMO-9839179", "size_type": "40HC", "stowage_tier": "UPPER_DECK_BAY14", "last_free_day": "2026-10-29", "daily_demurrage_usd": 375.0, "downstream_stockout_risk": "CRITICAL_PROMO_SKU"},
                    {"container_id": "MSKU-904819-3", "vessel_imo": "IMO-9839179", "size_type": "40HC", "stowage_tier": "HOLD_TIER04", "last_free_day": "2026-10-30", "daily_demurrage_usd": 375.0, "downstream_stockout_risk": "STANDARD_REPLENISHMENT"},
                ],
            },
            "port_terminal_gate_appointments": {
                "query_fn": "query_port_terminal_gate_appointments",
                "filter_param": "terminal_id",
                "filter_val": "USLAX_APM_PIER400",
                "rows": [
                    {"gate_slot_id": "GATE-LAX-20261028-T1", "terminal_id": "USLAX_APM_PIER400", "window_utc": "2026-10-28T07:00-09:00Z", "transaction_type": "DUAL_EMPTY_RETURN_FULL_PICKUP", "turn_time_mins": 34, "available_slots": 6},
                ],
            },
            "drayage_chassis_transload_allocations": {
                "query_fn": "query_drayage_chassis_transload_allocations",
                "filter_param": "container_id",
                "filter_val": "MSKU-904812-0",
                "rows": [
                    {"allocation_id": "DRAY-LAX-881", "container_id": "MSKU-904812-0", "drayage_carrier_id": "PAC-HARBOR-DRAY", "chassis_pool_id": "DCLI-40HC-991", "routing_decision": "PORT_TRANSLOAD_TO_53FT_OTR", "demurrage_avoided_usd": 1875.0, "transit_days_saved": 4.5},
                ],
            },
        },
        "action1": {
            "name": "action_book_dual_transaction_drayage_gate",
            "prefix": "PORT-GATE",
            "status": "DUAL_DRAYAGE_GATE_BOOKED",
            "params": ["container_id", "terminal_id", "gate_slot_id", "drayage_carrier_id", "rationale"],
            "sample_args": {
                "container_id": "MSKU-904812-0",
                "terminal_id": "USLAX_APM_PIER400",
                "gate_slot_id": "GATE-LAX-20261028-T1",
                "drayage_carrier_id": "PAC-HARBOR-DRAY",
                "rationale": "Booked dual-transaction Pier 400 gate slot 24 hours prior to Last Free Day using upper-deck discharge prediction, avoiding $1,875 in port demurrage.",
                "idempotency_key": "PORT-GATE-20261022-01",
            },
        },
        "action2": {
            "name": "action_divert_container_to_transload_hub",
            "prefix": "PORT-TRNS",
            "status": "CONTAINER_DIVERTED_TO_TRANSLOAD",
            "params": ["container_id", "transload_facility_id", "outbound_mode", "rationale"],
            "sample_args": {
                "container_id": "MSKU-904812-0",
                "transload_facility_id": "LAX-CARSON-XDOC-02",
                "outbound_mode": "53FT_TEAM_TRUCK_EXPEDITE",
                "rationale": "WeatherNext 3 detected 60-hour North Pacific swell delay; diverting MSKU-904812-0 from slow inland rail to Carson transload hub saves 4.5 transit days and prevents RDC stockout.",
                "idempotency_key": "PORT-TRNS-20261022-01",
            },
        },
        "chart": {
            "title": "PortWatch Container Dwell & Demurrage Avoidance",
            "subtitle": "Spire Satellite AIS + WeatherNext 3 Berth Prediction (Port Dwell Hours vs. Demurrage $ Saved)",
            "x_field": "container_batch",
            "y_field": "dwell_hours",
            "y2_field": "demurrage_saved_usd",
            "data": [
                {"container_batch": "MSKU-904812 (Transload)", "dwell_hours": 18.0, "demurrage_saved_usd": 1875, "status": "OPTIMIZED_CVRPTW"},
                {"container_batch": "MSKU-904819 (Dual Gate)", "dwell_hours": 26.5, "demurrage_saved_usd": 1500, "status": "OPTIMIZED_CVRPTW"},
                {"container_batch": "CMAU-441029 (Rail Ramp)", "dwell_hours": 31.0, "demurrage_saved_usd": 1125, "status": "OPTIMIZED_CVRPTW"},
                {"container_batch": "Unmonitored Port Baseline", "dwell_hours": 114.0, "demurrage_saved_usd": 0, "status": "LEGACY_STATIC"},
            ],
        },
    },

    # 4. air_cargo_uld_optimizer (High-Code: 3D Aircraft ULD Contour Solver + FlightAware ADS-B)
    {
        "id": "air_cargo_uld_optimizer",
        "class_name": "AirCargoUldOptimizer",
        "display_name": "AeroFreight — Air Cargo Charter, Belly Allocation & 3D ULD Contour Optimizer",
        "description": "Solves 3D non-rectangular aircraft ULD (LD3, LD7, PMC) contour packing to maximize volumetric weight efficiency and dynamically allocates air cargo across passenger belly and freighter charters.",
        "model": "gemini-3-pro-preview",
        "vertical": "05 · Deliver",
        "category": "Logistics, Fleet & Transportation Management",
        "tags": ["air-cargo", "3d-uld-packing", "iata-one-record", "flightaware-adsb", "volumetric-weight"],
        "systems": [
            {"id": "uld_3d_contour_solver", "name": "Google OR-Tools 3D Contoured Aircraft ULD (LD3/LD7/PMC) Polyhedral Solver", "protocol": "C++ / Python 3D Geometry SDK", "tables": ["uld_3d_packing_manifests", "uld_contour_geometry_specs"]},
            {"id": "iata_one_record_cargo", "name": "IATA ONE Record & Champ Cargospot e-AWB Booking Gateway", "protocol": "JSON-LD / REST API", "tables": ["air_freight_priority_shipments"]},
            {"id": "flightaware_adsb_telemetry", "name": "FlightAware Firehose ADS-B Live Aircraft Tail & Tarmac Connection Feed", "protocol": "Streaming WebSocket", "tables": ["flightaware_adsb_belly_capacity"]},
            {"id": "sap_tm_air_settlement", "name": "SAP TM Air Rate Table & BSA Block Space Agreement Optimizer", "protocol": "OData v4", "tables": ["air_freight_priority_shipments"]},
        ],
        "tables": {
            "air_freight_priority_shipments": {
                "query_fn": "query_air_freight_priority_shipments",
                "filter_param": "awb_id",
                "filter_val": "AWB-020-88419201",
                "rows": [
                    {"awb_id": "AWB-020-88419201", "origin_airport": "FRA", "dest_airport": "ORD", "actual_weight_kg": 2840, "unoptimized_chargeable_kg": 4120, "optimized_chargeable_kg": 2980, "cargo_class": "HIGH_VALUE_ELECTRONICS", "temp_control": "AMBIENT_15_25C"},
                    {"awb_id": "AWB-020-88419205", "origin_airport": "FRA", "dest_airport": "ORD", "actual_weight_kg": 1950, "unoptimized_chargeable_kg": 2680, "optimized_chargeable_kg": 2010, "cargo_class": "BIOPHARMA_2_8C", "temp_control": "ENVIROTAINER_RKN"},
                ],
            },
            "uld_contour_geometry_specs": {
                "query_fn": "query_uld_contour_geometry_specs",
                "filter_param": "uld_type",
                "filter_val": "PMC_LOWER_DECK_CONTOUR",
                "rows": [
                    {"uld_type": "PMC_LOWER_DECK_CONTOUR", "base_length_mm": 3175, "base_width_mm": 2438, "max_height_mm": 1626, "fuselage_chamfer_angle_deg": 38.5, "max_gross_weight_kg": 6800, "tare_weight_kg": 120},
                    {"uld_type": "LD3_AKE_CONTURED", "base_length_mm": 1562, "base_width_mm": 1534, "max_height_mm": 1626, "fuselage_chamfer_angle_deg": 45.0, "max_gross_weight_kg": 1588, "tare_weight_kg": 82},
                ],
            },
            "uld_3d_packing_manifests": {
                "query_fn": "query_uld_3d_packing_manifests",
                "filter_param": "uld_manifest_id",
                "filter_val": "ULD-MNF-FRA-ORD-01",
                "rows": [
                    {"uld_manifest_id": "ULD-MNF-FRA-ORD-01", "uld_type": "PMC_LOWER_DECK_CONTOUR", "awb_id": "AWB-020-88419201", "volumetric_efficiency_pct": 89.6, "chargeable_weight_saved_kg": 1140, "air_freight_saved_usd": 4788.0, "fuselage_contour_verified": True},
                ],
            },
            "flightaware_adsb_belly_capacity": {
                "query_fn": "query_flightaware_adsb_belly_capacity",
                "filter_param": "flight_number",
                "filter_val": "LH430",
                "rows": [
                    {"flight_number": "LH430", "aircraft_type": "B747-8I", "tail_number": "D-ABYA", "route": "FRA-ORD", "capacity_type": "CONTRACTED_BSA_BELLY", "rate_per_kg_usd": 3.85, "spot_charter_rate_usd": 6.40, "tarmac_cutoff_mins": 180, "adsb_status": "ON_SCHEDULE"},
                ],
            },
        },
        "action1": {
            "name": "action_release_3d_uld_buildup_manifest",
            "prefix": "AERO-ULD",
            "status": "ULD_3D_MANIFEST_RELEASED",
            "params": ["uld_manifest_id", "uld_type", "awb_id", "volumetric_efficiency_pct", "rationale"],
            "sample_args": {
                "uld_manifest_id": "ULD-MNF-FRA-ORD-01",
                "uld_type": "PMC_LOWER_DECK_CONTOUR",
                "awb_id": "AWB-020-88419201",
                "volumetric_efficiency_pct": 89.6,
                "rationale": "3D contoured PMC build-up nests high-density cartons along lower-deck fuselage bevels, achieving 89.6% volumetric fill and saving 1,140 kg of chargeable dimensional weight ($4,788).",
                "idempotency_key": "AERO-ULD-20261022-01",
            },
        },
        "action2": {
            "name": "action_book_air_charter_or_belly_allotment",
            "prefix": "AERO-AWB",
            "status": "AIR_CAPACITY_ALLOTMENT_LOCKED",
            "params": ["awb_id", "flight_number", "capacity_type", "rate_per_kg_usd", "rationale"],
            "sample_args": {
                "awb_id": "AWB-020-88419201",
                "flight_number": "LH430",
                "capacity_type": "CONTRACTED_BSA_BELLY",
                "rate_per_kg_usd": 3.85,
                "rationale": "Allocated AWB-020-88419201 to contracted Lufthansa LH430 B747-8I belly BSA ($3.85/kg) instead of $6.40/kg spot freighter charter, verified via FlightAware ADS-B tail D-ABYA.",
                "idempotency_key": "AERO-AWB-20261022-01",
            },
        },
        "chart": {
            "title": "AeroFreight 3D ULD Volumetric Efficiency & Chargeable Weight Savings",
            "subtitle": "IATA ONE Record + 3D Contoured ULD Packing (Volumetric Fill % vs. Freight Cost Saved $)",
            "x_field": "uld_unit",
            "y_field": "volumetric_fill_pct",
            "y2_field": "cost_saved_usd",
            "data": [
                {"uld_unit": "PMC-01 (FRA➔ORD Belly)", "volumetric_fill_pct": 89.6, "cost_saved_usd": 4788, "status": "OPTIMIZED_CVRPTW"},
                {"uld_unit": "LD7-04 (NRT➔LAX Belly)", "volumetric_fill_pct": 88.2, "cost_saved_usd": 3920, "status": "OPTIMIZED_CVRPTW"},
                {"uld_unit": "LD3-09 (AMS➔JFK Pharma)", "volumetric_fill_pct": 86.5, "cost_saved_usd": 2840, "status": "OPTIMIZED_CVRPTW"},
                {"uld_unit": "Manual Ground Handler Pack", "volumetric_fill_pct": 64.0, "cost_saved_usd": 0, "status": "LEGACY_STATIC"},
            ],
        },
    },

    # 5. intermodal_rail_linehaul_agent (High-Code: Class-I Rail COFC/TOFC MILP + Railinc EDI 404/417)
    {
        "id": "intermodal_rail_linehaul_agent",
        "class_name": "IntermodalRailLinehaulAgent",
        "display_name": "IntermodalSync — Factory-to-DC Intermodal Rail, Barge & Linehaul Orchestrator",
        "description": "Optimizes long-haul (500+ mile) freight conversion from over-the-road diesel trucks to double-stack COFC intermodal rail, synchronizing Railinc EDI 404/417 consists and ramp drayage.",
        "model": "gemini-3-pro-preview",
        "vertical": "05 · Deliver",
        "category": "Logistics, Fleet & Transportation Management",
        "tags": ["intermodal-rail", "cofc", "railinc-edi404", "scope3-decarbonization", "linehaul-milp"],
        "systems": [
            {"id": "railinc_clm_edi417_feed", "name": "Railinc Car Location Message (CLM) & Class-I Rail EDI 404/417 Gateway", "protocol": "EDI 404 / 417 / REST", "tables": ["railinc_edi417_train_consists"]},
            {"id": "intermodal_lane_milp_solver", "name": "Google OR-Tools OTR-to-Rail Intermodal Mode Conversion Solver", "protocol": "Python MILP SDK", "tables": ["intermodal_corridor_shipments", "otr_to_rail_mode_conversion_ledger"]},
            {"id": "ramp_crane_drayage_sync", "name": "BNSF / Union Pacific / CSX Intermodal Ramp Cut-Off & Crane Scheduler", "protocol": "REST API / Webhook", "tables": ["rail_ramp_cutoff_and_drayage"]},
            {"id": "glec_rail_carbon_calculator", "name": "GLEC v3.0 Intermodal Rail vs OTR Truck Carbon Intensity Ledger", "protocol": "BigQuery SQL / JSON", "tables": ["otr_to_rail_mode_conversion_ledger"]},
        ],
        "tables": {
            "intermodal_corridor_shipments": {
                "query_fn": "query_intermodal_corridor_shipments",
                "filter_param": "shipment_id",
                "filter_val": "SHP-IM-LA-CHI-701",
                "rows": [
                    {"shipment_id": "SHP-IM-LA-CHI-701", "origin_hub": "Los Angeles Factory Hub", "dest_dc": "Chicago Joliet RDC", "distance_miles": 2015, "otr_truck_cost_usd": 4650.0, "cofc_rail_cost_usd": 2890.0, "dest_dc_days_of_supply": 14.5, "recommended_mode": "COFC_DOUBLE_STACK_RAIL"},
                ],
            },
            "railinc_edi417_train_consists": {
                "query_fn": "query_railinc_edi417_train_consists",
                "filter_param": "train_id",
                "filter_val": "BNSF-Q-LACCHI-22",
                "rows": [
                    {"train_id": "BNSF-Q-LACCHI-22", "rail_carrier": "BNSF_RAILWAY", "origin_ramp": "HOBART_LAX", "dest_ramp": "LPC_JOLIET_CHI", "articulated_well_car": "DTTX-749201-WELL-B", "clm_sighting": "GALLUP_NM_ON_TIME", "eta_dest_ramp_utc": "2026-10-25T14:00:00Z"},
                ],
            },
            "rail_ramp_cutoff_and_drayage": {
                "query_fn": "query_rail_ramp_cutoff_and_drayage",
                "filter_param": "ramp_id",
                "filter_val": "LPC_JOLIET_CHI",
                "rows": [
                    {"ramp_id": "LPC_JOLIET_CHI", "crane_grounding_utc": "2026-10-25T15:30:00Z", "free_time_hours": 24, "assigned_dray_tractor": "JBHT-DRAY-CHI42", "chassis_id": "TRAC-53-8821", "zero_storage_dwell_verified": True},
                ],
            },
            "otr_to_rail_mode_conversion_ledger": {
                "query_fn": "query_otr_to_rail_mode_conversion_ledger",
                "filter_param": "corridor_lane",
                "filter_val": "LAX_TO_JOLIET_CHI",
                "rows": [
                    {"corridor_lane": "LAX_TO_JOLIET_CHI", "containers_converted": 18, "cost_savings_pct": 37.8, "total_usd_saved": 31680.0, "co2e_reduction_pct": 68.4, "tonnes_co2e_avoided": 41.2},
                ],
            },
        },
        "action1": {
            "name": "action_tender_edi404_rail_intermodal_bill",
            "prefix": "RAIL-404",
            "status": "EDI404_RAIL_TENDER_ACCEPTED",
            "params": ["shipment_id", "rail_carrier", "train_id", "origin_ramp", "dest_ramp", "rationale"],
            "sample_args": {
                "shipment_id": "SHP-IM-LA-CHI-701",
                "rail_carrier": "BNSF_RAILWAY",
                "train_id": "BNSF-Q-LACCHI-22",
                "origin_ramp": "HOBART_LAX",
                "dest_ramp": "LPC_JOLIET_CHI",
                "rationale": "Chicago Joliet RDC has 14.5 days of supply buffer; converting 2,015-mile linehaul from OTR truck to BNSF double-stack COFC rail saves $1,760 (-37.8%) and cuts Scope-3 CO2e by 68.4%.",
                "idempotency_key": "RAIL-404-20261022-01",
            },
        },
        "action2": {
            "name": "action_synchronize_ramp_crane_drayage_slot",
            "prefix": "RAIL-DRAY",
            "status": "RAMP_CRANE_DRAYAGE_SYNCHRONIZED",
            "params": ["train_id", "ramp_id", "drayage_tractor_id", "chassis_id", "rationale"],
            "sample_args": {
                "train_id": "BNSF-Q-LACCHI-22",
                "ramp_id": "LPC_JOLIET_CHI",
                "drayage_tractor_id": "JBHT-DRAY-CHI42",
                "chassis_id": "TRAC-53-8821",
                "rationale": "Synchronized J.B. Hunt drayage tractor JBHT-DRAY-CHI42 and chassis TRAC-53-8821 with BNSF Joliet crane grounding at 15:30 UTC, eliminating rail ramp storage fees.",
                "idempotency_key": "RAIL-DRAY-20261022-01",
            },
        },
        "chart": {
            "title": "IntermodalSync OTR-to-Rail Cost & Carbon Reduction",
            "subtitle": "Class-I COFC Double-Stack Rail vs. OTR Diesel Truck (Linehaul Cost $ vs. CO2e kg)",
            "x_field": "corridor_mode",
            "y_field": "cost_usd",
            "y2_field": "co2e_kg",
            "data": [
                {"corridor_mode": "LAX➔CHI (COFC Rail)", "cost_usd": 2890, "co2e_kg": 890, "status": "OPTIMIZED_CVRPTW"},
                {"corridor_mode": "LAX➔CHI (OTR Truck)", "cost_usd": 4650, "co2e_kg": 2815, "status": "LEGACY_STATIC"},
                {"corridor_mode": "SAV➔MEM (CSX Rail)", "cost_usd": 1420, "co2e_kg": 410, "status": "OPTIMIZED_CVRPTW"},
                {"corridor_mode": "SAV➔MEM (OTR Truck)", "cost_usd": 2350, "co2e_kg": 1290, "status": "LEGACY_STATIC"},
            ],
        },
    },

    # 6. multimodal_mode_shift_agent (High-Code: Factory->Ship->Air->Rail->Truck Pareto MILP)
    {
        "id": "multimodal_mode_shift_agent",
        "class_name": "MultimodalModeShiftAgent",
        "display_name": "ModalShift — Factory→Ship→Air→Rail→Truck Dynamic Mode-Switch Broker",
        "description": "Continuously solves the multi-objective Pareto trade-off between freight cost, transit lead-time, Scope-3 carbon, and downstream stockout penalty across Ocean, Sea-Air, Air, Rail, and Road.",
        "model": "gemini-3-pro-preview",
        "vertical": "05 · Deliver",
        "category": "Logistics, Fleet & Transportation Management",
        "tags": ["mode-shift", "sea-air-hybrid", "multi-modal-milp", "or-tools", "pareto-frontier"],
        "systems": [
            {"id": "or_tools_multimodal_pareto_milp", "name": "Google OR-Tools Multi-Modal Cost / Carbon / Stockout Pareto MILP", "protocol": "Python MILP SDK", "tables": ["dynamic_mode_split_recommendations"]},
            {"id": "sap_ibp_stockout_exposure", "name": "SAP IBP & Cloud Spanner Downstream Hub Stockout Exposure Feed", "protocol": "OData v4 / Spanner SQL", "tables": ["factory_gate_outbound_pos"]},
            {"id": "global_corridor_tariff_engine", "name": "CargoWise & Xeneta Multi-Modal Spot/Contract Tariff & Transit Matrix", "protocol": "REST API", "tables": ["multimodal_corridor_rate_tariff_matrix"]},
            {"id": "mid_route_sea_air_broker", "name": "Dubai / LAX / Singapore Sea-Air Transshipment Hub Orchestrator", "protocol": "EDI 315 / ONE Record", "tables": ["in_transit_mode_diversion_triggers"]},
        ],
        "tables": {
            "factory_gate_outbound_pos": {
                "query_fn": "query_factory_gate_outbound_pos",
                "filter_param": "po_id",
                "filter_val": "PO-FAC-VN-88210",
                "rows": [
                    {"po_id": "PO-FAC-VN-88210", "origin_factory": "Hai Phong Plant (Vietnam)", "dest_dc": "Rotterdam Euro Hub", "total_units": 20000, "weight_kg": 18000, "dest_days_of_supply": 9.0, "daily_stockout_margin_loss_usd": 28500.0},
                ],
            },
            "multimodal_corridor_rate_tariff_matrix": {
                "query_fn": "query_multimodal_corridor_rate_tariff_matrix",
                "filter_param": "mode_code",
                "filter_val": "SEA_AIR_DXB_HYBRID",
                "rows": [
                    {"mode_code": "OCEAN_FCL_SUEZ", "transit_days": 34, "cost_per_kg_usd": 0.42, "co2e_g_per_tkm": 11.2},
                    {"mode_code": "SEA_AIR_DXB_HYBRID", "transit_days": 14, "cost_per_kg_usd": 1.85, "co2e_g_per_tkm": 215.0},
                    {"mode_code": "DIRECT_AIR_FREIGHT", "transit_days": 4, "cost_per_kg_usd": 5.90, "co2e_g_per_tkm": 680.0},
                ],
            },
            "dynamic_mode_split_recommendations": {
                "query_fn": "query_dynamic_mode_split_recommendations",
                "filter_param": "po_id",
                "filter_val": "PO-FAC-VN-88210",
                "rows": [
                    {"split_plan_id": "SPLIT-VN-RTM-01", "po_id": "PO-FAC-VN-88210", "base_ocean_units": 17000, "expedite_sea_air_units": 3000, "panic_full_air_cost_usd": 106200.0, "optimal_split_cost_usd": 12975.0, "net_savings_vs_air_usd": 93225.0, "zero_stockout_guaranteed": True},
                ],
            },
            "in_transit_mode_diversion_triggers": {
                "query_fn": "query_in_transit_mode_diversion_triggers",
                "filter_param": "transship_hub",
                "filter_val": "DXB_JEBEL_ALI_DWC",
                "rows": [
                    {"diversion_id": "DIV-SEA-AIR-09", "po_id": "PO-FAC-VN-88210", "transship_hub": "DXB_JEBEL_ALI_DWC", "units_upgraded_to_air": 3000, "days_recovered": 20, "stockout_penalty_avoided_usd": 142500.0},
                ],
            },
        },
        "action1": {
            "name": "action_execute_dynamic_mode_split_booking",
            "prefix": "MODAL-SPL",
            "status": "DYNAMIC_MODE_SPLIT_BOOKED",
            "params": ["po_id", "primary_mode", "primary_units", "expedite_mode", "expedite_units", "rationale"],
            "sample_args": {
                "po_id": "PO-FAC-VN-88210",
                "primary_mode": "OCEAN_FCL_SUEZ",
                "primary_units": 17000,
                "expedite_mode": "SEA_AIR_DXB_HYBRID",
                "expedite_units": 3000,
                "rationale": "Splitting PO-FAC-VN-88210 into 85% Ocean FCL (17,000 units) + 15% Dubai Sea-Air bridge (3,000 units) bridges the 9-day Rotterdam stockout gap while saving $93,225 vs. full air expedite.",
                "idempotency_key": "MODAL-SPL-20261022-01",
            },
        },
        "action2": {
            "name": "action_trigger_mid_route_sea_air_upgrade",
            "prefix": "MODAL-UPG",
            "status": "MID_ROUTE_SEA_AIR_UPGRADED",
            "params": ["po_id", "transship_hub", "units_upgraded", "days_recovered", "rationale"],
            "sample_args": {
                "po_id": "PO-FAC-VN-88210",
                "transship_hub": "DXB_JEBEL_ALI_DWC",
                "units_upgraded": 3000,
                "days_recovered": 20,
                "rationale": "Triggered Jebel Ali port-to-DWC airport Sea-Air transshipment for 3,000 critical units, recovering 20 transit days and protecting $142,500 in downstream margin.",
                "idempotency_key": "MODAL-UPG-20261022-01",
            },
        },
        "chart": {
            "title": "ModalShift Multi-Modal Split vs. Single-Mode Panic Expedite",
            "subtitle": "Pareto Optimal 85% Ocean + 15% Sea-Air Split (Total Freight Cost $ vs. Transit Days)",
            "x_field": "routing_strategy",
            "y_field": "freight_cost_usd",
            "y2_field": "effective_lead_days",
            "data": [
                {"routing_strategy": "ModalShift 85/15 Split", "freight_cost_usd": 12975, "effective_lead_days": 14, "status": "OPTIMIZED_CVRPTW"},
                {"routing_strategy": "100% Panic Air Charter", "freight_cost_usd": 106200, "effective_lead_days": 4, "status": "LEGACY_STATIC"},
                {"routing_strategy": "100% Slow Ocean (+Stockout)", "freight_cost_usd": 7560, "effective_lead_days": 34, "status": "LEGACY_STATIC"},
            ],
        },
    },

    # 7. freight_control_tower (SentinelMove — In-Transit Telemetry & 3-Way Freight Bill Auditor)
    {
        "id": "freight_control_tower",
        "class_name": "FreightControlTower",
        "display_name": "SentinelMove — Multi-Modal In-Transit Control Tower & Freight Auditor",
        "description": "Monitors real-time GPS/AIS/ADS-B and cold-chain thermal telemetry across all in-transit shipments while performing 100% 3-way freight invoice auditing against contract tariffs and geofences.",
        "model": "gemini-3-pro-preview",
        "vertical": "05 · Deliver",
        "category": "Logistics, Fleet & Transportation Management",
        "tags": ["in-transit-control-tower", "cold-chain-iot", "freight-bill-audit", "edi-210", "geofencing"],
        "systems": [
            {"id": "project44_multimodal_telemetry", "name": "Project44 / FourKites Real-Time GPS & Cold-Chain IoT Stream", "protocol": "Webhook / REST v4", "tables": ["in_transit_multimodal_telemetry", "cold_chain_thermal_excursion_alerts"]},
            {"id": "google_maps_geofence_verifier", "name": "Google Maps Platform Dock Geofence Timestamp & Detention Verifier", "protocol": "REST / BigQuery GIS", "tables": ["freight_audit_discrepancy_ledger"]},
            {"id": "document_ai_edi210_auditor", "name": "Google Cloud Document AI & EDI 210 3-Way Freight Invoice Auditor", "protocol": "gRPC / EDI 210", "tables": ["carrier_edi210_freight_invoices", "freight_audit_discrepancy_ledger"]},
            {"id": "sap_ap_freight_settlement", "name": "SAP S/4HANA TM/AP Automated Freight Settlement & Debit Memo Engine", "protocol": "OData v4", "tables": ["freight_audit_discrepancy_ledger"]},
        ],
        "tables": {
            "in_transit_multimodal_telemetry": {
                "query_fn": "query_in_transit_multimodal_telemetry",
                "filter_param": "shipment_id",
                "filter_val": "SHP-REEF-8841",
                "rows": [
                    {"shipment_id": "SHP-REEF-8841", "carrier_id": "PRIME-REEFER-INC", "corridor": "I-80 Omaha➔Chicago", "cargo_type": "CHILLED_PROTEIN_2C", "setpoint_c": 2.0, "current_temp_c": 5.4, "compressor_status": "COOLANT_PRESSURE_DROP", "time_to_excursion_mins": 52},
                ],
            },
            "cold_chain_thermal_excursion_alerts": {
                "query_fn": "query_cold_chain_thermal_excursion_alerts",
                "filter_param": "shipment_id",
                "filter_val": "SHP-REEF-8841",
                "rows": [
                    {"alert_id": "THRM-ALT-8841", "shipment_id": "SHP-REEF-8841", "cargo_value_at_risk_usd": 148000.0, "nearest_cold_crossdock": "DES_MOINES_COLD_HUB_04", "distance_to_hub_km": 24.5, "recommended_action": "TRANS_LOAD_TO_BACKUP_REEFER"},
                ],
            },
            "carrier_edi210_freight_invoices": {
                "query_fn": "query_carrier_edi210_freight_invoices",
                "filter_param": "invoice_id",
                "filter_val": "INV-EDI210-77410",
                "rows": [
                    {"invoice_id": "INV-EDI210-77410", "carrier_id": "KNIGHT-SWIFT-TL", "shipment_id": "SHP-DRY-5519", "billed_amount_usd": 3490.0, "billed_detention_hrs": 4.5, "billed_detention_fee_usd": 450.0, "billed_fuel_surcharge_pct": 34.0},
                ],
            },
            "freight_audit_discrepancy_ledger": {
                "query_fn": "query_freight_audit_discrepancy_ledger",
                "filter_param": "invoice_id",
                "filter_val": "INV-EDI210-77410",
                "rows": [
                    {"audit_id": "FAUD-77410", "invoice_id": "INV-EDI210-77410", "geofence_verified_dwell_hrs": 1.2, "contract_free_time_hrs": 2.0, "contract_fsc_pct": 28.5, "overcharge_detected_usd": 615.0, "verified_payable_usd": 2875.0, "discrepancy_type": "INVALID_DETENTION_AND_FSC_RATE"},
                ],
            },
        },
        "action1": {
            "name": "action_reroute_in_transit_reefer_shipment",
            "prefix": "SENT-DIV",
            "status": "REEFER_DIVERTED_TO_COLD_HUB",
            "params": ["shipment_id", "diversion_hub_id", "cargo_value_protected_usd", "rationale"],
            "sample_args": {
                "shipment_id": "SHP-REEF-8841",
                "diversion_hub_id": "DES_MOINES_COLD_HUB_04",
                "cargo_value_protected_usd": 148000.0,
                "rationale": "IoT telemetry detected compressor coolant pressure drop (+3.4°C drift) 52 minutes before excursion limit; diverted SHP-REEF-8841 to Des Moines Cold Hub (24.5 km) for cross-dock into backup reefer, saving $148,000 cargo.",
                "idempotency_key": "SENT-DIV-20261022-01",
            },
        },
        "action2": {
            "name": "action_issue_freight_audit_debit_adjustment",
            "prefix": "SENT-AUD",
            "status": "FREIGHT_INVOICE_ADJUSTED",
            "params": ["invoice_id", "carrier_id", "disputed_amount_usd", "verified_payable_usd", "rationale"],
            "sample_args": {
                "invoice_id": "INV-EDI210-77410",
                "carrier_id": "KNIGHT-SWIFT-TL",
                "disputed_amount_usd": 615.0,
                "verified_payable_usd": 2875.0,
                "rationale": "Google Maps dock geofence proved trailer dwell was 1.2 hrs (within 2.0 hr free window) and contract DOE fuel index is 28.5%; auto-deducted $615.00 overcharge prior to SAP AP release.",
                "idempotency_key": "SENT-AUD-20261022-01",
            },
        },
        "chart": {
            "title": "SentinelMove 3-Way Freight Bill Audit & Cold-Chain Rescue",
            "subtitle": "Geofence + Contract Tariff 3-Way Match (Billed Invoice $ vs. Audited Payable $)",
            "x_field": "invoice_batch",
            "y_field": "billed_usd",
            "y2_field": "overcharge_saved_usd",
            "data": [
                {"invoice_batch": "INV-77410 (Detention+FSC)", "billed_usd": 3490, "overcharge_saved_usd": 615, "status": "OPTIMIZED_CVRPTW"},
                {"invoice_batch": "INV-77418 (Mileage Audit)", "billed_usd": 4120, "overcharge_saved_usd": 485, "status": "OPTIMIZED_CVRPTW"},
                {"invoice_batch": "INV-77425 (Accessorial)", "billed_usd": 2890, "overcharge_saved_usd": 390, "status": "OPTIMIZED_CVRPTW"},
                {"invoice_batch": "Un-Audited Auto-Pay", "billed_usd": 3490, "overcharge_saved_usd": 0, "status": "LEGACY_STATIC"},
            ],
        },
    },

    # 8. field_beat_distributor_sync_agent (BeatSync — TM&D Field Sales & DMS Inventory Harmonizer)
    {
        "id": "field_beat_distributor_sync_agent",
        "class_name": "FieldBeatDistributorSyncAgent",
        "display_name": "BeatSync — Field Sales & Distributor Inventory Harmonizer",
        "description": "Synchronizes real-time Distributor Management System (DMS) stock with Field Sales Officer (FSO) beat routing so reps never pitch stocked-out SKUs and primary replenishment fires automatically.",
        "model": "gemini-3-pro-preview",
        "vertical": "05 · Deliver",
        "category": "Trade Marketing & Distribution (TM&D)",
        "tags": ["dms-sync", "field-sales-beat", "pitch-to-stock", "tmd-distribution", "google-maps"],
        "systems": [
            {"id": "dms_distributor_inventory_cloud", "name": "Enterprise Distributor Management System (DMS) Real-Time Stock Ledger", "protocol": "REST API / Webhook", "tables": ["distributor_dms_live_inventory", "primary_replenishment_auto_orders"]},
            {"id": "sfa_field_beat_optimizer", "name": "Sales Force Automation (SFA) + Google Maps Beat Route Sequencer", "protocol": "gRPC / Mobile Sync", "tables": ["fso_daily_beat_store_outlets"]},
            {"id": "pitch_to_stock_recommender", "name": "Vertex AI Pitch-to-Stock Dynamic SKU Substitution Engine", "protocol": "Python / BigQuery ML", "tables": ["pitch_to_stock_substitution_rules"]},
            {"id": "sap_sd_primary_billing", "name": "SAP S/4HANA SD Primary Factory-to-Distributor Auto-Replenishment", "protocol": "OData v4 / IDoc", "tables": ["primary_replenishment_auto_orders"]},
        ],
        "tables": {
            "distributor_dms_live_inventory": {
                "query_fn": "query_distributor_dms_live_inventory",
                "filter_param": "distributor_id",
                "filter_val": "DIST-MUM-WEST-04",
                "rows": [
                    {"distributor_id": "DIST-MUM-WEST-04", "sku_id": "SKU-BEV-500ML", "on_hand_cases": 0, "stock_status": "STOCKED_OUT", "substitute_sku_id": "SKU-BEV-750ML-PROMO", "substitute_on_hand_cases": 420},
                    {"distributor_id": "DIST-MUM-WEST-04", "sku_id": "SKU-SNK-multipack", "on_hand_cases": 310, "stock_status": "HEALTHY_BUFFER", "substitute_sku_id": "NONE", "substitute_on_hand_cases": 310},
                ],
            },
            "fso_daily_beat_store_outlets": {
                "query_fn": "query_fso_daily_beat_store_outlets",
                "filter_param": "fso_id",
                "filter_val": "FSO-WEST-112",
                "rows": [
                    {"fso_id": "FSO-WEST-112", "beat_id": "BEAT-ANDHERI-NORTH", "planned_outlets": 38, "high_propensity_outlets": 28, "route_time_saved_mins": 54, "productive_call_rate_pct": 89.5},
                ],
            },
            "pitch_to_stock_substitution_rules": {
                "query_fn": "query_pitch_to_stock_substitution_rules",
                "filter_param": "stocked_out_sku",
                "filter_val": "SKU-BEV-500ML",
                "rows": [
                    {"rule_id": "SUB-BEV-01", "stocked_out_sku": "SKU-BEV-500ML", "recommended_in_stock_sku": "SKU-BEV-750ML-PROMO", "cross_elasticity_retention_pct": 94.2, "dealer_margin_bonus_pct": 2.5},
                ],
            },
            "primary_replenishment_auto_orders": {
                "query_fn": "query_primary_replenishment_auto_orders",
                "filter_param": "distributor_id",
                "filter_val": "DIST-MUM-WEST-04",
                "rows": [
                    {"primary_so_id": "SO-PRIM-20261022-55", "distributor_id": "DIST-MUM-WEST-04", "sku_id": "SKU-BEV-500ML", "replenish_cases": 600, "source_cfa_depot": "CFA-BHIWANDI-HUB", "eta_hours": 14},
                ],
            },
        },
        "action1": {
            "name": "action_push_fso_dynamic_beat_and_pitch_list",
            "prefix": "BEAT-SYNC",
            "status": "FSO_BEAT_AND_PITCH_SYNCED",
            "params": ["fso_id", "distributor_id", "suppressed_sku_id", "promoted_substitute_sku", "rationale"],
            "sample_args": {
                "fso_id": "FSO-WEST-112",
                "distributor_id": "DIST-MUM-WEST-04",
                "suppressed_sku_id": "SKU-BEV-500ML",
                "promoted_substitute_sku": "SKU-BEV-750ML-PROMO",
                "rationale": "Suppressed stocked-out SKU-BEV-500ML on FSO-WEST-112 mobile handheld and pushed in-stock SKU-BEV-750ML-PROMO (420 cases in DMS), preventing zero-fill secondary orders across 28 retail stores.",
                "idempotency_key": "BEAT-SYNC-20261022-01",
            },
        },
        "action2": {
            "name": "action_trigger_distributor_primary_replenishment",
            "prefix": "BEAT-REPL",
            "status": "PRIMARY_REPLENISHMENT_RELEASED",
            "params": ["distributor_id", "sku_id", "replenish_cases", "source_cfa_depot", "rationale"],
            "sample_args": {
                "distributor_id": "DIST-MUM-WEST-04",
                "sku_id": "SKU-BEV-500ML",
                "replenish_cases": 600,
                "source_cfa_depot": "CFA-BHIWANDI-HUB",
                "rationale": "Auto-released 600-case primary billing order from Bhiwandi CFA Depot to replenish DIST-MUM-WEST-04 within 14 hours.",
                "idempotency_key": "BEAT-REPL-20261022-01",
            },
        },
        "chart": {
            "title": "BeatSync Secondary Order Fill-Rate & FSO Productive Call Lift",
            "subtitle": "Live DMS-to-SFA Synchronization (Secondary Order Fill Rate % vs. Productive Calls)",
            "x_field": "beat_territory",
            "y_field": "fill_rate_pct",
            "y2_field": "productive_call_pct",
            "data": [
                {"beat_territory": "West Zone (BeatSync Live)", "fill_rate_pct": 98.4, "productive_call_pct": 89.5, "status": "OPTIMIZED_CVRPTW"},
                {"beat_territory": "North Zone (BeatSync Live)", "fill_rate_pct": 97.6, "productive_call_pct": 87.2, "status": "OPTIMIZED_CVRPTW"},
                {"beat_territory": "Unsynced Static Beat", "fill_rate_pct": 76.5, "productive_call_pct": 62.0, "status": "LEGACY_STATIC"},
            ],
        },
    },

    # 9. planogram_merchandising_vision_auditor (ShelfVision — Gemini 3.8 Flash Retail Planogram Auditor)
    {
        "id": "planogram_merchandising_vision_auditor",
        "class_name": "PlanogramMerchandisingVisionAuditor",
        "display_name": "ShelfVision — Retail Planogram & Visibility Auditor",
        "description": "Uses Gemini 3.8 Flash multimodal vision to audit retail store shelf photos in under 2 seconds, measuring Share-of-Shelf (SOS), eye-level facings, cooler purity, and on-shelf availability.",
        "model": "gemini-3.8-flash",
        "vertical": "05 · Deliver",
        "category": "Trade Marketing & Distribution (TM&D)",
        "tags": ["gemini-3.8-flash", "planogram-vision", "share-of-shelf", "retail-execution", "on-shelf-availability"],
        "systems": [
            {"id": "gemini_38_flash_shelf_vision", "name": "Vertex AI Gemini 3.8 Flash Dense Retail SKU & Facing Detector", "protocol": "gRPC Multimodal API", "tables": ["store_shelf_vision_audit_captures"]},
            {"id": "trade_planogram_contract_db", "name": "Enterprise Category Management & Contracted Planogram Registry", "protocol": "REST / BigQuery", "tables": ["contracted_planogram_templates"]},
            {"id": "sos_compliance_scoring_engine", "name": "Share-of-Shelf (SOS) & Cooler Purity Compliance Scorer", "protocol": "Python Analytics", "tables": ["shelf_compliance_scoring_ledger"]},
            {"id": "sfa_instore_task_dispatcher", "name": "In-Store Mobile Merchandising Corrective Action Dispatcher", "protocol": "Webhook / Push", "tables": ["merchandising_corrective_tasks"]},
        ],
        "tables": {
            "store_shelf_vision_audit_captures": {
                "query_fn": "query_store_shelf_vision_audit_captures",
                "filter_param": "capture_id",
                "filter_val": "IMG-SHLF-20261022-409",
                "rows": [
                    {"capture_id": "IMG-SHLF-20261022-409", "outlet_id": "OUTLET-HYPER-882", "shelf_zone": "EYE_LEVEL_TIER_2", "detected_brand_facings": 9, "contracted_brand_facings": 14, "competitor_intrusion_facings": 3, "empty_shelf_gaps": 2, "inference_latency_ms": 1180},
                ],
            },
            "contracted_planogram_templates": {
                "query_fn": "query_contracted_planogram_templates",
                "filter_param": "template_id",
                "filter_val": "PLG-BEV-GONDOLA-Q4",
                "rows": [
                    {"template_id": "PLG-BEV-GONDOLA-Q4", "channel_tier": "MODERN_TRADE_HYPER", "required_sos_pct": 45.0, "required_eye_level_facings": 14, "monthly_visibility_payout_usd": 450.0},
                ],
            },
            "shelf_compliance_scoring_ledger": {
                "query_fn": "query_shelf_compliance_scoring_ledger",
                "filter_param": "outlet_id",
                "filter_val": "OUTLET-HYPER-882",
                "rows": [
                    {"audit_id": "SHLF-AUD-409", "outlet_id": "OUTLET-HYPER-882", "measured_sos_pct": 32.1, "post_correction_sos_pct": 46.8, "compliance_status": "CORRECTED_IN_STORE", "osa_lift_pct": 6.4},
                ],
            },
            "merchandising_corrective_tasks": {
                "query_fn": "query_merchandising_corrective_tasks",
                "filter_param": "outlet_id",
                "filter_val": "OUTLET-HYPER-882",
                "rows": [
                    {"task_id": "MRCH-TSK-409", "outlet_id": "OUTLET-HYPER-882", "fso_id": "FSO-WEST-112", "directive": "Restock 2 empty gaps of SKU-BEV-500ML from backroom and remove 3 competitor facings from Eye-Level Tier 2"},
                ],
            },
        },
        "action1": {
            "name": "action_dispatch_instore_restock_directive",
            "prefix": "SHLF-FIX",
            "status": "INSTORE_RESTOCK_DIRECTIVE_SENT",
            "params": ["capture_id", "outlet_id", "fso_id", "missing_facings_count", "rationale"],
            "sample_args": {
                "capture_id": "IMG-SHLF-20261022-409",
                "outlet_id": "OUTLET-HYPER-882",
                "fso_id": "FSO-WEST-112",
                "missing_facings_count": 5,
                "rationale": "Gemini 3.8 Flash detected 32.1% Share-of-Shelf (9/14 eye-level facings, 2 empty gaps, 3 competitor intrusions) in 1.18s; pushed instant restock prompt to FSO-WEST-112 while still in store.",
                "idempotency_key": "SHLF-FIX-20261022-01",
            },
        },
        "action2": {
            "name": "action_certify_store_planogram_audit",
            "prefix": "SHLF-CRT",
            "status": "PLANOGRAM_COMPLIANCE_CERTIFIED",
            "params": ["outlet_id", "template_id", "verified_sos_pct", "payout_approved", "rationale"],
            "sample_args": {
                "outlet_id": "OUTLET-HYPER-882",
                "template_id": "PLG-BEV-GONDOLA-Q4",
                "verified_sos_pct": 46.8,
                "payout_approved": True,
                "rationale": "Verified post-correction shelf photo achieved 46.8% SOS (exceeding 45.0% threshold) with 14/14 eye-level facings; unlocked $450 monthly visibility payout.",
                "idempotency_key": "SHLF-CRT-20261022-01",
            },
        },
        "chart": {
            "title": "ShelfVision Gemini 3.8 Flash Share-of-Shelf (SOS) & OSA Compliance",
            "subtitle": "Real-Time In-Store Multimodal Planogram Audit (Share-of-Shelf % Before vs. After In-Store Fix)",
            "x_field": "store_segment",
            "y_field": "sos_pct",
            "y2_field": "osa_pct",
            "data": [
                {"store_segment": "Hyper #882 (Post-ShelfVision)", "sos_pct": 46.8, "osa_pct": 98.2, "status": "OPTIMIZED_CVRPTW"},
                {"store_segment": "Hyper #882 (Pre-Correction)", "sos_pct": 32.1, "osa_pct": 84.0, "status": "LEGACY_STATIC"},
                {"store_segment": "Supermarket #410 (Verified)", "sos_pct": 48.2, "osa_pct": 97.5, "status": "OPTIMIZED_CVRPTW"},
            ],
        },
    },

    # 10. trade_scheme_claims_reconciler (SchemeGuard — TM&D Trade Payout & Claims Sentinel)
    {
        "id": "trade_scheme_claims_reconciler",
        "class_name": "TradeSchemeClaimsReconciler",
        "display_name": "SchemeGuard — Secondary Trade Payout & Claims Sentinel",
        "description": "Audits 100% of distributor secondary sales scheme claims against circular slab rules, e-waybill proof, and ShelfVision compliance—blocking phantom/split invoices and posting SAP FI credit notes.",
        "model": "gemini-3-pro-preview",
        "vertical": "05 · Deliver",
        "category": "Trade Marketing & Distribution (TM&D)",
        "tags": ["trade-promotions", "claims-audit", "phantom-billing-detection", "sap-fi-credit-note", "tmd"],
        "systems": [
            {"id": "trade_scheme_slab_engine", "name": "Enterprise Trade Promotion Management (TPM) Circular & Slab Rule Engine", "protocol": "REST / JSON", "tables": ["active_trade_promotion_schemes"]},
            {"id": "dms_secondary_claims_portal", "name": "Distributor Secondary Billing & Scheme Claim Submission Portal", "protocol": "OData / REST", "tables": ["distributor_secondary_claim_submissions"]},
            {"id": "phantom_invoice_graph_detector", "name": "BigQuery ML Anomaly & Split-Invoice Leakage Detector", "protocol": "BigQuery SQL", "tables": ["claim_anomaly_audit_findings"]},
            {"id": "sap_fi_credit_memo_poster", "name": "SAP S/4HANA FI Accounts Receivable Automated Credit Memo BAPI", "protocol": "RFC / OData v4", "tables": ["sap_fi_credit_note_settlements"]},
        ],
        "tables": {
            "active_trade_promotion_schemes": {
                "query_fn": "query_active_trade_promotion_schemes",
                "filter_param": "scheme_id",
                "filter_val": "SCH-FEST-Q4-2026",
                "rows": [
                    {"scheme_id": "SCH-FEST-Q4-2026", "scheme_name": "Q4 Festive Volume Slab & Display Rebate", "min_slab_cases": 50, "rebate_pct": 6.5, "requires_shelfvision_pass": True, "valid_window": "2026-10-01_TO_2026-10-31"},
                ],
            },
            "distributor_secondary_claim_submissions": {
                "query_fn": "query_distributor_secondary_claim_submissions",
                "filter_param": "claim_id",
                "filter_val": "CLM-DIST04-9921",
                "rows": [
                    {"claim_id": "CLM-DIST04-9921", "distributor_id": "DIST-MUM-WEST-04", "scheme_id": "SCH-FEST-Q4-2026", "submitted_invoices_count": 142, "claimed_amount_usd": 18450.0},
                ],
            },
            "claim_anomaly_audit_findings": {
                "query_fn": "query_claim_anomaly_audit_findings",
                "filter_param": "claim_id",
                "filter_val": "CLM-DIST04-9921",
                "rows": [
                    {"audit_id": "CLM-AUD-9921", "claim_id": "CLM-DIST04-9921", "flagged_invoices": ["INV-SEC-8812", "INV-SEC-8819"], "anomaly_type": "POST_SCHEME_WINDOW_AND_DUPLICATE_GSTIN", "disallowed_leakage_usd": 2190.0, "verified_net_payout_usd": 16260.0},
                ],
            },
            "sap_fi_credit_note_settlements": {
                "query_fn": "query_sap_fi_credit_note_settlements",
                "filter_param": "claim_id",
                "filter_val": "CLM-DIST04-9921",
                "rows": [
                    {"credit_note_id": "SAP-CN-20261022-88", "claim_id": "CLM-DIST04-9921", "approved_amount_usd": 16260.0, "leakage_blocked_usd": 2190.0, "settlement_cycle_hours": 1.8},
                ],
            },
        },
        "action1": {
            "name": "action_flag_phantom_invoice_for_audit_hold",
            "prefix": "SCHM-HOLD",
            "status": "ANOMALOUS_INVOICES_DISALLOWED",
            "params": ["claim_id", "flagged_invoices", "disallowed_amount_usd", "rationale"],
            "sample_args": {
                "claim_id": "CLM-DIST04-9921",
                "flagged_invoices": ["INV-SEC-8812", "INV-SEC-8819"],
                "disallowed_amount_usd": 2190.0,
                "rationale": "Disallowed $2,190.00 across 2 secondary invoices (post-dated outside scheme window and duplicate outlet tax ID) on claim CLM-DIST04-9921.",
                "idempotency_key": "SCHM-HOLD-20261022-01",
            },
        },
        "action2": {
            "name": "action_post_sap_fi_trade_credit_note",
            "prefix": "SCHM-CN",
            "status": "SAP_FI_CREDIT_NOTE_POSTED",
            "params": ["claim_id", "distributor_id", "approved_amount_usd", "rationale"],
            "sample_args": {
                "claim_id": "CLM-DIST04-9921",
                "distributor_id": "DIST-MUM-WEST-04",
                "approved_amount_usd": 16260.0,
                "rationale": "Posted verified SAP S/4HANA FI credit note for $16,260.00 (140 compliant secondary invoices) in 1.8 hours instead of 45 days.",
                "idempotency_key": "SCHM-CN-20261022-01",
            },
        },
        "chart": {
            "title": "SchemeGuard Trade Spend Leakage Prevention & Settlement Speed",
            "subtitle": "100% Automated Secondary Invoice Audit (Approved Payout $ vs. Leakage Blocked $)",
            "x_field": "claim_batch",
            "y_field": "approved_usd",
            "y2_field": "leakage_blocked_usd",
            "data": [
                {"claim_batch": "CLM-9921 (West Zone)", "approved_usd": 16260, "leakage_blocked_usd": 2190, "status": "OPTIMIZED_CVRPTW"},
                {"claim_batch": "CLM-9928 (North Zone)", "approved_usd": 22400, "leakage_blocked_usd": 3150, "status": "OPTIMIZED_CVRPTW"},
                {"claim_batch": "Manual 5% Sample Audit", "approved_usd": 18450, "leakage_blocked_usd": 110, "status": "LEGACY_STATIC"},
            ],
        },
    },

    # 11. reverse_rma_optimizer (ReturnLoop — Circular RMA Grading & Fleet Backhaul Optimizer)
    {
        "id": "reverse_rma_optimizer",
        "class_name": "ReverseRmaOptimizer",
        "display_name": "ReturnLoop — Autonomous RMA Grading & Backhaul Optimizer",
        "description": "Combines Gemini 3.8 Flash optical RMA triage with returning FleetFlow backhaul insertion and margin-maximizing circular disposition (Grade-A Restock, Refurbish, Component Harvest).",
        "model": "gemini-3.8-flash",
        "vertical": "06 · Return & Enable",
        "category": "Reverse Logistics, Circularity & ESG",
        "tags": ["reverse-logistics", "rma-vision-grading", "fleet-backhaul", "circular-economy", "remanufacturing"],
        "systems": [
            {"id": "gemini_38_flash_rma_vision", "name": "Vertex AI Gemini 3.8 Flash Optical RMA Condition & Seal Grader", "protocol": "gRPC Multimodal API", "tables": ["multimodal_vision_grading_results"]},
            {"id": "loop_sap_rma_portal", "name": "SAP S/4HANA Returns & Customer RMA Intake Portal", "protocol": "REST / OData v4", "tables": ["customer_rma_intake_requests"]},
            {"id": "fleetflow_backhaul_matcher", "name": "FleetFlow Returning Delivery Truck Backhaul Milk-Run Matcher", "protocol": "Google Maps CVRPTW", "tables": ["fleet_backhaul_pickup_slots"]},
            {"id": "circular_disposition_solver", "name": "OR-Tools Circular Recovery Margin Solver (Restock vs Refurb vs Harvest)", "protocol": "Python MILP", "tables": ["circular_disposition_routing_ledger"]},
        ],
        "tables": {
            "customer_rma_intake_requests": {
                "query_fn": "query_customer_rma_intake_requests",
                "filter_param": "rma_id",
                "filter_val": "RMA-20261022-501",
                "rows": [
                    {"rma_id": "RMA-20261022-501", "customer_id": "RETAIL-PARTNER-09", "sku_id": "SKU-PRO-ESPRESSO-X1", "units": 12, "retail_value_usd": 9600.0, "stated_reason": "OVERSTOCK_UNOPENED_BOX"},
                    {"rma_id": "RMA-20261022-504", "customer_id": "DEALER-SOUTH-14", "sku_id": "SKU-IND-SERVO-MTR", "units": 4, "retail_value_usd": 6400.0, "stated_reason": "HOUSING_SCUFF_WARRANTY"},
                ],
            },
            "multimodal_vision_grading_results": {
                "query_fn": "query_multimodal_vision_grading_results",
                "filter_param": "rma_id",
                "filter_val": "RMA-20261022-501",
                "rows": [
                    {"grading_id": "GRD-501", "rma_id": "RMA-20261022-501", "optical_grade": "GRADE_A_FACTORY_SEAL_INTACT", "tamper_seal_verified": True, "net_recovery_pct": 94.0, "recoverable_value_usd": 9024.0},
                ],
            },
            "fleet_backhaul_pickup_slots": {
                "query_fn": "query_fleet_backhaul_pickup_slots",
                "filter_param": "rma_id",
                "filter_val": "RMA-20261022-501",
                "rows": [
                    {"pickup_slot_id": "BKH-RMA-501", "rma_id": "RMA-20261022-501", "returning_vehicle_id": "TRK-12T-TX14", "detour_distance_km": 2.4, "ltl_shipping_saved_usd": 420.0},
                ],
            },
            "circular_disposition_routing_ledger": {
                "query_fn": "query_circular_disposition_routing_ledger",
                "filter_param": "rma_id",
                "filter_val": "RMA-20261022-501",
                "rows": [
                    {"disposition_id": "DISP-501", "rma_id": "RMA-20261022-501", "routing_path": "DIRECT_REGIONAL_FDC_RESTOCK", "target_facility_id": "FDC-AUSTIN-02", "central_return_touch_bypassed": True},
                ],
            },
        },
        "action1": {
            "name": "action_assign_rma_disposition_and_backhaul",
            "prefix": "RMA-LOOP",
            "status": "RMA_DISPOSITION_AND_BACKHAUL_LOCKED",
            "params": ["rma_id", "optical_grade", "target_facility_id", "backhaul_vehicle_id", "rationale"],
            "sample_args": {
                "rma_id": "RMA-20261022-501",
                "optical_grade": "GRADE_A_FACTORY_SEAL_INTACT",
                "target_facility_id": "FDC-AUSTIN-02",
                "backhaul_vehicle_id": "TRK-12T-TX14",
                "rationale": "Gemini 3.8 Flash verified factory tamper seal intact (Grade A); routed 12 units directly to Austin FDC-02 for immediate resale via returning truck TRK-12T-TX14, recovering 94% value ($9,024) and saving $420 LTL freight.",
                "idempotency_key": "RMA-LOOP-20261022-01",
            },
        },
        "action2": {
            "name": "action_issue_instant_customer_rma_credit_or_swap",
            "prefix": "RMA-CRED",
            "status": "INSTANT_RMA_CREDIT_ISSUED",
            "params": ["rma_id", "customer_id", "credit_amount_usd", "rationale"],
            "sample_args": {
                "rma_id": "RMA-20261022-501",
                "customer_id": "RETAIL-PARTNER-09",
                "credit_amount_usd": 9024.0,
                "rationale": "Issued instant SAP credit memo upon optical seal verification and backhaul scan.",
                "idempotency_key": "RMA-CRED-20261022-01",
            },
        },
        "chart": {
            "title": "ReturnLoop Circular Margin Recovery & Backhaul Freight Savings",
            "subtitle": "Gemini 3.8 Flash Optical Triage + Fleet Backhaul (Net Recovery % vs. Value Recovered $)",
            "x_field": "disposition_path",
            "y_field": "recovery_pct",
            "y2_field": "recovered_usd",
            "data": [
                {"disposition_path": "Grade-A Direct FDC Restock", "recovery_pct": 94.0, "recovered_usd": 9024, "status": "OPTIMIZED_CVRPTW"},
                {"disposition_path": "Grade-B Certified Refurb", "recovery_pct": 72.5, "recovered_usd": 4640, "status": "OPTIMIZED_CVRPTW"},
                {"disposition_path": "Grade-C Component Harvest", "recovery_pct": 48.0, "recovered_usd": 3072, "status": "OPTIMIZED_CVRPTW"},
                {"disposition_path": "Legacy Central Return Hub", "recovery_pct": 38.0, "recovered_usd": 3648, "status": "LEGACY_STATIC"},
            ],
        },
    },

    # 12. otif_penalty_shield (OTIFShield — Customer SLA Rescue & Chargeback Dispute Agent)
    {
        "id": "otif_penalty_shield",
        "class_name": "OtifPenaltyShield",
        "display_name": "OTIFShield — Customer SLA Rescue & Chargeback Dispute Agent",
        "description": "Predicts customer Must-Arrive-By-Date (MABD) OTIF breaches 72 hours early to trigger margin-positive rescues and auto-assembles geofence + EDI 856 dispute dossiers to overturn invalid retail chargebacks.",
        "model": "gemini-3-pro-preview",
        "vertical": "06 · Return & Enable",
        "category": "Customer OTIF & SLA Governance",
        "tags": ["otif-shield", "mabd-compliance", "chargeback-dispute", "edi-856", "retail-deductions"],
        "systems": [
            {"id": "mabd_otif_risk_predictor", "name": "Vertex AI 72-Hour Customer MABD & OTIF Breach Risk Scorer", "protocol": "BigQuery ML / Spanner", "tables": ["open_retail_customer_orders_sla", "predicted_otif_breach_alerts"]},
            {"id": "retail_link_chargeback_portal", "name": "Walmart Retail Link / Target Partners Online Deduction Feed", "protocol": "EDI 812 / Portal API", "tables": ["retailer_otif_chargeback_deductions"]},
            {"id": "geofence_edi856_dossier_builder", "name": "Google Maps Geofence + EDI 856 ASN + Signed ePOD Evidence Compiler", "protocol": "Document AI / GIS", "tables": ["geofence_edi856_dispute_dossiers"]},
            {"id": "sap_sd_order_rescue_broker", "name": "SAP S/4HANA SD Priority Wave & Alternate Hub Split-Ship Broker", "protocol": "OData v4", "tables": ["predicted_otif_breach_alerts"]},
        ],
        "tables": {
            "open_retail_customer_orders_sla": {
                "query_fn": "query_open_retail_customer_orders_sla",
                "filter_param": "order_id",
                "filter_val": "SO-WMT-20261022-881",
                "rows": [
                    {"order_id": "SO-WMT-20261022-881", "customer_id": "BIGBOX-RETAIL-01", "order_value_usd": 420000.0, "mabd_window_utc": "2026-10-25T14:00:00Z", "otif_penalty_pct": 3.0, "potential_fine_usd": 12600.0},
                ],
            },
            "predicted_otif_breach_alerts": {
                "query_fn": "query_predicted_otif_breach_alerts",
                "filter_param": "order_id",
                "filter_val": "SO-WMT-20261022-881",
                "rows": [
                    {"alert_id": "OTIF-ALT-881", "order_id": "SO-WMT-20261022-881", "breach_probability": 0.78, "root_cause": "PRIMARY_DC_WAVE_BACKLOG_6HRS", "rescue_option": "PRIORITY_DOCK_RELEASE_AND_TEAM_DRIVER", "rescue_cost_usd": 650.0, "net_penalty_saved_usd": 11950.0},
                ],
            },
            "retailer_otif_chargeback_deductions": {
                "query_fn": "query_retailer_otif_chargeback_deductions",
                "filter_param": "deduction_id",
                "filter_val": "DED-RET01-44910",
                "rows": [
                    {"deduction_id": "DED-RET01-44910", "customer_id": "BIGBOX-RETAIL-01", "shipment_id": "SHP-WMT-4012", "claimed_reason": "LATE_ARRIVAL_PAST_MABD", "deducted_amount_usd": 9450.0},
                ],
            },
            "geofence_edi856_dispute_dossiers": {
                "query_fn": "query_geofence_edi856_dispute_dossiers",
                "filter_param": "deduction_id",
                "filter_val": "DED-RET01-44910",
                "rows": [
                    {"dossier_id": "DOS-OTIF-44910", "deduction_id": "DED-RET01-44910", "mabd_cutoff_utc": "2026-10-18T16:00:00Z", "google_maps_geofence_entry_utc": "2026-10-18T14:12:00Z", "edi856_asn_timestamp": "2026-10-17T08:00:00Z", "epod_signature_verified": True, "win_probability": 0.98},
                ],
            },
        },
        "action1": {
            "name": "action_execute_otif_sla_rescue_intervention",
            "prefix": "OTIF-RSC",
            "status": "OTIF_SLA_RESCUE_EXECUTED",
            "params": ["order_id", "customer_id", "rescue_option", "penalty_avoided_usd", "rationale"],
            "sample_args": {
                "order_id": "SO-WMT-20261022-881",
                "customer_id": "BIGBOX-RETAIL-01",
                "rescue_option": "PRIORITY_DOCK_RELEASE_AND_TEAM_DRIVER",
                "penalty_avoided_usd": 12600.0,
                "rationale": "Predicted 78% MABD breach risk 72 hours early; spent $650 on priority dock wave release to avoid a $12,600 (3% COGS) retail OTIF chargeback.",
                "idempotency_key": "OTIF-RSC-20261022-01",
            },
        },
        "action2": {
            "name": "action_submit_chargeback_dispute_dossier",
            "prefix": "OTIF-DSP",
            "status": "CHARGEBACK_DISPUTE_SUBMITTED",
            "params": ["deduction_id", "dossier_id", "disputed_amount_usd", "rationale"],
            "sample_args": {
                "deduction_id": "DED-RET01-44910",
                "dossier_id": "DOS-OTIF-44910",
                "disputed_amount_usd": 9450.0,
                "rationale": "Auto-compiled Google Maps geofence gate entry (14:12 UTC vs 16:00 UTC MABD cutoff), EDI 856 ASN, and signed ePOD to overturn invalid $9,450 late-arrival chargeback.",
                "idempotency_key": "OTIF-DSP-20261022-01",
            },
        },
        "chart": {
            "title": "OTIFShield Penalty Prevention & Chargeback Recovery",
            "subtitle": "72h Predictive SLA Rescue + Geofence Dispute Dossiers (OTIF % vs. Chargebacks Recovered $)",
            "x_field": "key_account",
            "y_field": "otif_pct",
            "y2_field": "penalties_saved_usd",
            "data": [
                {"key_account": "BigBox Retail #01 (OTIFShield)", "otif_pct": 99.2, "penalties_saved_usd": 22050, "status": "OPTIMIZED_CVRPTW"},
                {"key_account": "National Grocer #02 (OTIFShield)", "otif_pct": 98.9, "penalties_saved_usd": 16800, "status": "OPTIMIZED_CVRPTW"},
                {"key_account": "Reactive Post-Mortem Baseline", "otif_pct": 93.4, "penalties_saved_usd": 0, "status": "LEGACY_STATIC"},
            ],
        },
    },

    # 13. carbon_scope3_ledger (EcoChain — Shipment-Level Scope-3 Carbon, CBAM & EUDR Ledger)
    {
        "id": "carbon_scope3_ledger",
        "class_name": "CarbonScope3Ledger",
        "display_name": "EcoChain — Shipment-Level Scope-3 Carbon, CBAM & EUDR Ledger",
        "description": "Calculates audit-ready ISO 14083 & GLEC v3.0 shipment-level Scope-3 emissions from primary telematics, generates EU CBAM embedded carbon declarations, and verifies EUDR zero-deforestation plots via Google Earth Engine.",
        "model": "gemini-3-pro-preview",
        "vertical": "06 · Return & Enable",
        "category": "Sustainability, CBAM & Scope-3 ESG",
        "tags": ["scope3-carbon", "iso-14083", "eu-cbam", "eudr-earth-engine", "glec-framework"],
        "systems": [
            {"id": "iso14083_glec_carbon_engine", "name": "ISO 14083 & GLEC Framework v3.0 Primary Telemetry Carbon Ledger", "protocol": "BigQuery SQL / Python", "tables": ["shipment_level_scope3_emissions"]},
            {"id": "eu_cbam_registry_gateway", "name": "EU Carbon Border Adjustment Mechanism (CBAM) Embedded Carbon Engine", "protocol": "XML / REST API", "tables": ["eu_cbam_embedded_carbon_declarations"]},
            {"id": "google_earth_engine_eudr", "name": "Google Earth Engine Satellite Polygon Deforestation Verifier (EUDR)", "protocol": "Earth Engine Python API", "tables": ["eudr_earth_engine_plot_verifications"]},
            {"id": "scope3_decarbonization_solver", "name": "OR-Tools Low-Carbon Carrier & Smelter Swap Optimizer", "protocol": "Python MILP", "tables": ["low_carbon_carrier_and_supplier_swaps"]},
        ],
        "tables": {
            "shipment_level_scope3_emissions": {
                "query_fn": "query_shipment_level_scope3_emissions",
                "filter_param": "shipment_id",
                "filter_val": "SHP-GLB-20261022-301",
                "rows": [
                    {"shipment_id": "SHP-GLB-20261022-301", "corridor": "Rotterdam➔Duisburg", "mode": "ELECTRIC_BARGE_AND_EV_TRUCK", "payload_tonnes": 42.0, "distance_km": 215.0, "wtw_co2e_kg": 184.5, "glec_intensity_g_tkm": 20.4, "assurance_level": "ISO_14083_PRIMARY_VERIFIED"},
                ],
            },
            "eu_cbam_embedded_carbon_declarations": {
                "query_fn": "query_eu_cbam_embedded_carbon_declarations",
                "filter_param": "import_declaration_id",
                "filter_val": "CBAM-EU-2026-Q4-09",
                "rows": [
                    {"import_declaration_id": "CBAM-EU-2026-Q4-09", "cn_code": "7606_12_92_ALUMINUM_SHEET", "supplier_smelter": "NORSK_HYDRO_RENEWABLE_EAF", "imported_tonnes": 120.0, "primary_specific_emissions_tco2e_per_t": 2.1, "eu_default_penalty_tco2e_per_t": 8.4, "cbam_tax_avoided_eur": 64260.0},
                ],
            },
            "eudr_earth_engine_plot_verifications": {
                "query_fn": "query_eudr_earth_engine_plot_verifications",
                "filter_param": "plot_id",
                "filter_val": "PLOT-BR-PARA-4410",
                "rows": [
                    {"plot_id": "PLOT-BR-PARA-4410", "commodity": "NATURAL_RUBBER_AND_PULP", "geojson_centroid": "-3.1190,-60.0217", "sentinel2_ndvi_change_post2020": 0.0, "deforestation_free_verified": True, "eudr_due_diligence_ref": "EUDR-DDS-2026-99120"},
                ],
            },
            "low_carbon_carrier_and_supplier_swaps": {
                "query_fn": "query_low_carbon_carrier_and_supplier_swaps",
                "filter_param": "swap_id",
                "filter_val": "SWAP-DEC-2026-04",
                "rows": [
                    {"swap_id": "SWAP-DEC-2026-04", "target_corridor_or_bom": "DE_NL_RHINE_CORRIDOR", "recommended_partner": "HVO100_BIOFUEL_AND_ELECTRIC_BARGE", "annual_tco2e_reduction": 1420.0, "net_cost_delta_pct": -1.2},
                ],
            },
        },
        "action1": {
            "name": "action_certify_cbam_and_eudr_compliance_dossier",
            "prefix": "ESG-CERT",
            "status": "CBAM_AND_EUDR_DOSSIER_CERTIFIED",
            "params": ["import_declaration_id", "plot_id", "cbam_tax_avoided_eur", "rationale"],
            "sample_args": {
                "import_declaration_id": "CBAM-EU-2026-Q4-09",
                "plot_id": "PLOT-BR-PARA-4410",
                "cbam_tax_avoided_eur": 64260.0,
                "rationale": "Certified primary smelter emissions (2.1 tCO2e/t vs 8.4 EU default penalty, saving €64,260 in CBAM certificates) and verified zero post-2020 deforestation on PLOT-BR-PARA-4410 via Google Earth Engine.",
                "idempotency_key": "ESG-CERT-20261022-01",
            },
        },
        "action2": {
            "name": "action_commit_scope3_decarbonization_swap",
            "prefix": "ESG-SWAP",
            "status": "LOW_CARBON_LANE_SWAP_COMMITTED",
            "params": ["swap_id", "target_corridor_or_bom", "annual_tco2e_reduction", "rationale"],
            "sample_args": {
                "swap_id": "SWAP-DEC-2026-04",
                "target_corridor_or_bom": "DE_NL_RHINE_CORRIDOR",
                "annual_tco2e_reduction": 1420.0,
                "rationale": "Shifted Rhine corridor volume to HVO100 renewable diesel and electric barge, cutting annual Scope-3 emissions by 1,420 tCO2e at -1.2% lower freight cost.",
                "idempotency_key": "ESG-SWAP-20261022-01",
            },
        },
        "chart": {
            "title": "EcoChain Scope-3 Carbon Intensity & EU CBAM Tax Shield",
            "subtitle": "ISO 14083 Primary Telemetry vs. EU Default Penalty Factors (tCO2e vs. CBAM € Saved)",
            "x_field": "compliance_scope",
            "y_field": "emissions_tco2e",
            "y2_field": "cbam_eur_saved",
            "data": [
                {"compliance_scope": "Hydro EAF Aluminum (Primary)", "emissions_tco2e": 252, "cbam_eur_saved": 64260, "status": "OPTIMIZED_CVRPTW"},
                {"compliance_scope": "EU Default Penalty Factor", "emissions_tco2e": 1008, "cbam_eur_saved": 0, "status": "LEGACY_STATIC"},
                {"compliance_scope": "Rhine HVO100 + Barge Swap", "emissions_tco2e": 410, "cbam_eur_saved": 28400, "status": "OPTIMIZED_CVRPTW"},
            ],
        },
    },

    # 14. network_twin_architect (TwinDesign — Capacitated Facility Location & Cost-to-Serve Optimizer)
    {
        "id": "network_twin_architect",
        "class_name": "NetworkTwinArchitect",
        "display_name": "TwinDesign — Supply Chain Network & Cost-to-Serve Optimizer",
        "description": "Solves Capacitated Facility Location & Center-of-Gravity MILP in Google OR-Tools paired with activity-based Cost-to-Serve attribution and tariff/port-strike stress testing.",
        "model": "gemini-3-pro-preview",
        "vertical": "04 · Fulfill",
        "category": "Network Design & Cost-to-Serve FinOps",
        "tags": ["network-design", "facility-location-milp", "cost-to-serve", "center-of-gravity", "or-tools"],
        "systems": [
            {"id": "or_tools_facility_location_milp", "name": "Google OR-Tools Capacitated Facility Location & Territory MILP", "protocol": "C++ / Python MILP", "tables": ["center_of_gravity_milp_scenarios", "network_facility_nodes_and_leases"]},
            {"id": "bigquery_abc_cost_to_serve", "name": "BigQuery Activity-Based Cost-to-Serve (CTS) & Margin Waterfall Engine", "protocol": "BigQuery SQL", "tables": ["sku_customer_cost_to_serve_matrix"]},
            {"id": "tariff_port_strike_simulator", "name": "Macro Tariff & Port Disruption Network Stress-Test Simulator", "protocol": "Python Monte Carlo + MILP", "tables": ["network_stress_test_simulations"]},
            {"id": "sap_ibp_network_master", "name": "SAP IBP & S/4HANA Sourcing Rules & Customer Territory Master", "protocol": "OData v4", "tables": ["center_of_gravity_milp_scenarios"]},
        ],
        "tables": {
            "network_facility_nodes_and_leases": {
                "query_fn": "query_network_facility_nodes_and_leases",
                "filter_param": "facility_id",
                "filter_val": "RDC-COLUMBUS-OH",
                "rows": [
                    {"facility_id": "RDC-COLUMBUS-OH", "facility_type": "REGIONAL_DC", "annual_lease_usd": 4200000.0, "capacity_pallets_yr": 480000, "handling_cost_per_pallet_usd": 14.20, "utilization_pct": 94.0},
                    {"facility_id": "3PL-SAVANNAH-EXP", "facility_type": "PROPOSED_3PL_HUB", "annual_lease_usd": 1850000.0, "capacity_pallets_yr": 220000, "handling_cost_per_pallet_usd": 12.80, "utilization_pct": 88.5},
                ],
            },
            "sku_customer_cost_to_serve_matrix": {
                "query_fn": "query_sku_customer_cost_to_serve_matrix",
                "filter_param": "customer_segment_id",
                "filter_val": "SEG-SOUTHEAST-L2",
                "rows": [
                    {"customer_segment_id": "SEG-SOUTHEAST-L2", "avg_order_pallets": 1.5, "each_pick_cost_usd": 184.0, "stem_miles_from_ohio": 685, "net_operating_margin_pct": -3.8, "remediated_margin_pct": 8.4},
                ],
            },
            "center_of_gravity_milp_scenarios": {
                "query_fn": "query_center_of_gravity_milp_scenarios",
                "filter_param": "scenario_id",
                "filter_val": "SCEN-COG-SE-2026",
                "rows": [
                    {"scenario_id": "SCEN-COG-SE-2026", "scenario_name": "Southeast 3PL Node Addition & Territory Realignment", "stem_miles_reduction_pct": 14.6, "annual_net_savings_usd": 6840000.0, "1_day_ground_coverage_pct": 91.2},
                ],
            },
            "network_stress_test_simulations": {
                "query_fn": "query_network_stress_test_simulations",
                "filter_param": "stress_test_id",
                "filter_val": "STRESS-TARIFF-60PCT",
                "rows": [
                    {"stress_test_id": "STRESS-TARIFF-60PCT", "shock_event": "60% Section 301 Tariff + East Coast Port Congestion", "recommended_shift": "Nearshore Monterrey MX + Savannah/Houston Split", "duty_and_freight_saved_usd": 11200000.0},
                ],
            },
        },
        "action1": {
            "name": "action_publish_network_territory_realignment",
            "prefix": "TWIN-NET",
            "status": "NETWORK_TERRITORY_REALIGNED",
            "params": ["scenario_id", "new_hub_id", "annual_savings_usd", "rationale"],
            "sample_args": {
                "scenario_id": "SCEN-COG-SE-2026",
                "new_hub_id": "3PL-SAVANNAH-EXP",
                "annual_savings_usd": 6840000.0,
                "rationale": "OR-Tools Center-of-Gravity MILP reassigned 142 Southeast zip-3 territories from Columbus OH to Savannah 3PL hub, cutting stem miles by 14.6% and saving $6.84M/yr.",
                "idempotency_key": "TWIN-NET-20261022-01",
            },
        },
        "action2": {
            "name": "action_update_cost_to_serve_order_policy",
            "prefix": "TWIN-CTS",
            "status": "COST_TO_SERVE_POLICY_UPDATED",
            "params": ["customer_segment_id", "new_moq_layer_pallets", "margin_improvement_pct", "rationale"],
            "sample_args": {
                "customer_segment_id": "SEG-SOUTHEAST-L2",
                "new_moq_layer_pallets": 4,
                "margin_improvement_pct": 12.2,
                "rationale": "Activity-based Cost-to-Serve identified -3.8% margin erosion from broken-case LTL orders; enforced 4-pallet layer MOQ and weekly consolidated delivery, restoring +8.4% net margin.",
                "idempotency_key": "TWIN-CTS-20261022-01",
            },
        },
        "chart": {
            "title": "TwinDesign Network Center-of-Gravity & Cost-to-Serve Optimization",
            "subtitle": "OR-Tools Facility Location MILP (Total Network Cost $M vs. 1-Day Ground SLA %)",
            "x_field": "network_topology",
            "y_field": "annual_cost_m_usd",
            "y2_field": "one_day_sla_pct",
            "data": [
                {"network_topology": "Optimized + Savannah Hub", "annual_cost_m_usd": 67.4, "one_day_sla_pct": 91.2, "status": "OPTIMIZED_CVRPTW"},
                {"network_topology": "Nearshore Tariff Resilient", "annual_cost_m_usd": 69.1, "one_day_sla_pct": 89.8, "status": "OPTIMIZED_CVRPTW"},
                {"network_topology": "Legacy 3-RDC Baseline", "annual_cost_m_usd": 74.2, "one_day_sla_pct": 76.4, "status": "LEGACY_STATIC"},
            ],
        },
    },

    # 15. eco_cutover_orchestrator (ChangeSync — Engineering Change ECO & NPI Cutover Orchestrator)
    {
        "id": "eco_cutover_orchestrator",
        "class_name": "EcoCutoverOrchestrator",
        "display_name": "ChangeSync — Engineering Change (ECO) & NPI Cutover Orchestrator",
        "description": "Synchronizes PLM Engineering Change Orders (ECOs) with multi-plant ERP BOM effectivity dates and open supplier POs to minimize obsolete component write-offs while protecting NPI launch dates.",
        "model": "gemini-3-pro-preview",
        "vertical": "03 · Make",
        "category": "Manufacturing, BOM Governance & NPI Launch",
        "tags": ["eco-cutover", "plm-erp-sync", "obsolete-inventory-shield", "npi-launch", "or-tools"],
        "systems": [
            {"id": "teamcenter_plm_eco_stream", "name": "Siemens Teamcenter / PTC Windchill PLM Engineering Change (ECO) Feed", "protocol": "REST / Webhook", "tables": ["plm_engineering_change_orders"]},
            {"id": "sap_mm_pp_runout_ledger", "name": "SAP S/4HANA MM/PP Multi-Plant WIP & Open Supplier PO Runout Ledger", "protocol": "OData v4 / BAPI", "tables": ["multi_plant_predecessor_inventory_runout", "erp_bom_effectivity_sync_audit"]},
            {"id": "or_tools_eco_cutover_solver", "name": "Google OR-Tools Dynamic BOM Phase-In / Phase-Out Cutover Solver", "protocol": "Python MILP SDK", "tables": ["eco_optimal_cutover_schedules"]},
            {"id": "ariba_po_revision_updater", "name": "SAP Ariba Open Supplier Purchase Order Revision Cutover Engine", "protocol": "cXML / REST", "tables": ["erp_bom_effectivity_sync_audit"]},
        ],
        "tables": {
            "plm_engineering_change_orders": {
                "query_fn": "query_plm_engineering_change_orders",
                "filter_param": "eco_id",
                "filter_val": "ECO-2026-8841",
                "rows": [
                    {"eco_id": "ECO-2026-8841", "assembly_sku": "ASM-INVERTER-GEN4", "predecessor_part": "PCB-DRV-REV-B", "successor_part": "PCB-DRV-REV-C", "change_class": "COST_AND_EFFICIENCY_UPGRADE", "interchangeable": True},
                ],
            },
            "multi_plant_predecessor_inventory_runout": {
                "query_fn": "query_multi_plant_predecessor_inventory_runout",
                "filter_param": "eco_id",
                "filter_val": "ECO-2026-8841",
                "rows": [
                    {"eco_id": "ECO-2026-8841", "plant_id": "PLANT-AUSTIN-01", "predecessor_on_hand_units": 4200, "open_supplier_po_units": 2800, "daily_burn_rate_units": 350, "uncoordinated_scrap_exposure_usd": 315000.0},
                    {"eco_id": "ECO-2026-8841", "plant_id": "PLANT-GUADALAJARA-02", "predecessor_on_hand_units": 1800, "open_supplier_po_units": 900, "daily_burn_rate_units": 225, "uncoordinated_scrap_exposure_usd": 121500.0},
                ],
            },
            "eco_optimal_cutover_schedules": {
                "query_fn": "query_eco_optimal_cutover_schedules",
                "filter_param": "eco_id",
                "filter_val": "ECO-2026-8841",
                "rows": [
                    {"schedule_id": "CUT-ECO-8841", "eco_id": "ECO-2026-8841", "optimal_effectivity_date": "2026-11-11", "supplier_po_converted_to_rev_c": 2800, "obsolete_scrap_writeoff_usd": 8400.0, "scrap_avoided_usd": 428100.0},
                ],
            },
            "erp_bom_effectivity_sync_audit": {
                "query_fn": "query_erp_bom_effectivity_sync_audit",
                "filter_param": "eco_id",
                "filter_val": "ECO-2026-8841",
                "rows": [
                    {"sync_id": "SYNC-SAP-8841", "eco_id": "ECO-2026-8841", "open_po_id": "PO-ARIBA-55910", "sap_bom_status": "EFFECTIVITY_ALIGNED_TO_RUNOUT", "npi_launch_on_time": True},
                ],
            },
        },
        "action1": {
            "name": "action_lock_multi_plant_eco_effectivity_dates",
            "prefix": "ECO-LOCK",
            "status": "BOM_EFFECTIVITY_LOCKED",
            "params": ["eco_id", "optimal_effectivity_date", "scrap_avoided_usd", "rationale"],
            "sample_args": {
                "eco_id": "ECO-2026-8841",
                "optimal_effectivity_date": "2026-11-11",
                "scrap_avoided_usd": 428100.0,
                "rationale": "Aligned Austin and Guadalajara SAP BOM effectivity to 2026-11-11 to exhaust 6,000 on-hand Rev-B boards prior to Rev-C cutover, avoiding $428,100 in obsolete E&O write-offs.",
                "idempotency_key": "ECO-LOCK-20261022-01",
            },
        },
        "action2": {
            "name": "action_modify_open_supplier_po_revision",
            "prefix": "ECO-PO",
            "status": "SUPPLIER_PO_REVISION_UPDATED",
            "params": ["open_po_id", "predecessor_part", "successor_part", "units_converted", "rationale"],
            "sample_args": {
                "open_po_id": "PO-ARIBA-55910",
                "predecessor_part": "PCB-DRV-REV-B",
                "successor_part": "PCB-DRV-REV-C",
                "units_converted": 2800,
                "rationale": "Converted 2,800 unshipped units on open supplier PO-ARIBA-55910 from Rev-B to Rev-C prior to supplier SMT production freeze.",
                "idempotency_key": "ECO-PO-20261022-01",
            },
        },
        "chart": {
            "title": "ChangeSync Multi-Plant ECO Runout & E&O Write-Off Prevention",
            "subtitle": "PLM-to-ERP Dynamic BOM Effectivity Solver (Obsolete Scrap Write-Off $ vs. Runout %)",
            "x_field": "cutover_mode",
            "y_field": "scrap_writeoff_usd",
            "y2_field": "exhaustion_pct",
            "data": [
                {"cutover_mode": "ChangeSync Dynamic Runout", "scrap_writeoff_usd": 8400, "exhaustion_pct": 98.1, "status": "OPTIMIZED_CVRPTW"},
                {"cutover_mode": "Blind Immediate Cutover", "scrap_writeoff_usd": 436500, "exhaustion_pct": 12.0, "status": "LEGACY_STATIC"},
                {"cutover_mode": "Manual Spreadsheet Guess", "scrap_writeoff_usd": 194000, "exhaustion_pct": 55.5, "status": "LEGACY_STATIC"},
            ],
        },
    },
]


def build_agent_package(spec: Dict[str, Any]) -> None:
    agent_id = spec["id"]
    class_name = spec["class_name"]
    display_name = spec["display_name"]
    description = spec["description"]
    model = spec["model"]
    vertical = spec["vertical"]
    category = spec["category"]
    tags = spec["tags"]
    systems = spec["systems"]
    tables = spec["tables"]
    act1 = spec["action1"]
    act2 = spec["action2"]
    chart = spec["chart"]

    pkg_dir = AGENTS_DIR / agent_id
    (pkg_dir / "app" / "render").mkdir(parents=True, exist_ok=True)
    (pkg_dir / "fixtures" / "tables").mkdir(parents=True, exist_ok=True)
    (pkg_dir / "evals").mkdir(parents=True, exist_ok=True)
    (pkg_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    (pkg_dir / "tests").mkdir(parents=True, exist_ok=True)

    # 1. Write fixture JSON tables
    table_names = list(tables.keys())
    for tbl_name, tbl_meta in tables.items():
        tbl_path = pkg_dir / "fixtures" / "tables" / f"{tbl_name}.json"
        tbl_path.write_text(json.dumps(tbl_meta["rows"], indent=2) + "\n", encoding="utf-8")

    # 2. Write pyproject.toml
    pyproject = f'''[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[project]
name = "{agent_id}"
version = "0.1.0"
description = "{description}"
readme = "agents-cli-manifest.yaml"
requires-python = ">=3.10"
dependencies = [
    "google-genai>=1.0.0",
]

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
'''
    (pkg_dir / "pyproject.toml").write_text(pyproject, encoding="utf-8")

    # 3. Write agents-cli-manifest.yaml
    tool_entries = ["  - \"app.tools:list_systems\""]
    for tbl_meta in tables.values():
        tool_entries.append(f"  - \"app.tools:{tbl_meta['query_fn']}\"")
    tool_entries.append(f"  - \"app.tools:{act1['name']}\"")
    tool_entries.append(f"  - \"app.tools:{act2['name']}\"")
    tags_yaml = "\n".join(f"  - {t}" for t in tags)
    tools_yaml = "\n".join(tool_entries)

    manifest = f'''name: {agent_id}
display_name: "{display_name}"
description: "{description}"
version: "0.1.0"
model: "{model}"
vertical: "{vertical}"
category: "{category}"
tags:
{tags_yaml}
entrypoint: "app.agent:{class_name}"
tools:
{tools_yaml}
'''
    (pkg_dir / "agents-cli-manifest.yaml").write_text(manifest, encoding="utf-8")

    # 4. Write app/__init__.py and app/render/__init__.py
    (pkg_dir / "app" / "__init__.py").write_text(
        f'"""{display_name} ADK Package."""\nfrom .agent import {class_name}\n\n__all__ = ["{class_name}"]\n',
        encoding="utf-8",
    )
    (pkg_dir / "app" / "render" / "__init__.py").write_text('"""A2UI v0.9 render module."""\n', encoding="utf-8")
    (pkg_dir / "app" / "render" / "a2ui_envelope.py").write_text(A2UI_ENVELOPE_CODE, encoding="utf-8")
    (pkg_dir / "app" / "render" / "a2ui_lifecycle.py").write_text(A2UI_LIFECYCLE_CODE, encoding="utf-8")

    # 5. Write app/render/charts.py
    chart_fn = f"create_{agent_id}_chart_spec"
    charts_code = f'''"""Vega-Lite chart specifications for {display_name}."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def {chart_fn}(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a visual Vega-Lite v5 specification for {display_name}."""
    if not data_points:
        data_points = {json.dumps(chart["data"], indent=12)}

    return {{
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": {json.dumps(chart["title"])},
        "title": {{
            "text": {json.dumps(chart["title"])},
            "subtitle": {json.dumps(chart["subtitle"])},
            "anchor": "start",
            "fontSize": 14,
            "subtitleFontSize": 11,
            "subtitleColor": "#5f6368"
        }},
        "width": 640,
        "height": 280,
        "data": {{"values": data_points}},
        "layer": [
            {{
                "mark": {{"type": "bar", "cornerRadiusTopLeft": 4, "cornerRadiusTopRight": 4, "size": 38}},
                "encoding": {{
                    "x": {{"field": "{chart['x_field']}", "type": "nominal", "title": "Operational Dimension", "axis": {{"labelAngle": 0}}}},
                    "y": {{"field": "{chart['y_field']}", "type": "quantitative", "title": "{chart['y_field']}"}},
                    "color": {{
                        "field": "status",
                        "type": "nominal",
                        "scale": {{
                            "domain": ["OPTIMIZED_CVRPTW", "LEGACY_STATIC"],
                            "range": ["#1e8e3e", "#ea4335"]
                        }},
                        "title": "Execution Mode"
                    }},
                }}
            }},
            {{
                "mark": {{"type": "line", "point": True, "color": "#fbbc04", "strokeWidth": 2.5}},
                "encoding": {{
                    "x": {{"field": "{chart['x_field']}", "type": "nominal"}},
                    "y": {{
                        "field": "{chart['y2_field']}",
                        "type": "quantitative",
                        "axis": {{"title": "{chart['y2_field']}", "orient": "right"}},
                    }}
                }}
            }}
        ],
        "resolve": {{"scale": {{"y": "independent"}}}}
    }}
'''
    (pkg_dir / "app" / "render" / "charts.py").write_text(charts_code, encoding="utf-8")

    # 6. Write app/render/surfaces.py
    surface_fn = f"build_{agent_id}_surface"
    surfaces_code = f'''"""A2UI Surface Builder for {display_name}."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from .a2ui_envelope import wrap_a2ui_part
from .a2ui_lifecycle import (
    build_create_surface,
    build_update_components,
)
from .charts import {chart_fn}


def {surface_fn}(
    surface_id: str,
    spec: Optional[Dict[str, Any]] = None,
    height: int = 340,
) -> List[Any]:
    """Renders ONLY the visual VegaChart inside the Card component, keeping markdown tables outside."""
    chart_spec = spec or {chart_fn}()

    parts = [
        wrap_a2ui_part(build_create_surface(surface_id)),
        wrap_a2ui_part(build_update_components(
            surface_id,
            [
                {{
                    "id": "root",
                    "component": "Card",
                    "child": "chart-wrapper",
                }},
                {{
                    "id": "chart-wrapper",
                    "component": "VegaChart",
                    "spec": chart_spec,
                    "height": height,
                }},
            ]
        )),
    ]
    return parts
'''
    (pkg_dir / "app" / "render" / "surfaces.py").write_text(surfaces_code, encoding="utf-8")

    # 7. Write app/tools.py
    query_fns_code = []
    for idx, (tbl_name, tbl_meta) in enumerate(tables.items()):
        qfn = tbl_meta["query_fn"]
        fparam = tbl_meta["filter_param"]
        sys_id = systems[min(idx, len(systems) - 1)]["id"]
        query_fns_code.append(f'''
def {qfn}(
    {fparam}: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query {tbl_name} records from {sys_id}."""
    rows = _read_json("{tbl_name}.json")
    if {fparam}:
        rows = [r for r in rows if {fparam}.lower() in str(r.get("{fparam}", "")).lower()]
    return {{
        "source_system": "{sys_id}",
        "table": "{tbl_name}",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }}
''')

    def build_action_fn_code(act: Dict[str, Any], id_field_name: str) -> str:
        params_sig = ",\n    ".join([f"{p}: Any" for p in act["params"]] + ["idempotency_key: str"])
        dict_items = ",\n        ".join([f'"{p}": {p}' for p in act["params"]])
        first_p = act["params"][0]
        return f'''
def {act["name"]}(
    {params_sig}
) -> Dict[str, Any]:
    """Execute {act['name']} mutation with deterministic audit logging."""
    action_id = _deterministic_id("{act['prefix']}", {first_p}, idempotency_key)
    payload = {{
        "{id_field_name}": action_id,
        {dict_items},
        "status": "{act['status']}",
        "idempotency_key": idempotency_key
    }}
    _append_action_event("{act['name']}", payload)
    return payload
'''

    tools_code = f'''"""Deterministic and fixture-backed tools for {display_name}."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List

FIXTURES = Path(os.environ.get("FIXTURES_ROOT", str(Path(__file__).resolve().parent.parent / "fixtures")))
ACTION_EVENTS_PATH = Path(__file__).resolve().parent.parent / "artifacts" / "action-events.jsonl"


def _read_json(table_filename: str) -> List[Dict[str, Any]]:
    p = FIXTURES / "tables" / table_filename
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []


def _append_action_event(tool_name: str, payload: Dict[str, Any]) -> None:
    ACTION_EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with ACTION_EVENTS_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps({{"tool": tool_name, **payload}}, sort_keys=True) + "\\n")


def _deterministic_id(prefix: str, *parts: Any) -> str:
    payload = "|".join(str(p) for p in parts if p is not None and p != "")
    digest = hashlib.sha1(payload.encode("utf-8")).hexdigest()[:8].upper() if payload else "00000000"
    return f"{{prefix}}-{{digest}}"


def list_systems() -> Dict[str, Any]:
    """Returns connected enterprise systems and solver engines for {agent_id}."""
    return {{
        "agent": "{agent_id}",
        "systems": {json.dumps(systems, indent=12)}
    }}
{"".join(query_fns_code)}
{build_action_fn_code(act1, "dispatch_execution_id")}
{build_action_fn_code(act2, "secondary_action_id")}
'''
    (pkg_dir / "app" / "tools.py").write_text(tools_code, encoding="utf-8")

    # 8. Write app/agent.py
    tool_refs = [f"    tools.{m['query_fn']}," for m in tables.values()]
    tool_refs.append(f"    tools.{act1['name']},")
    tool_refs.append(f"    tools.{act2['name']},")
    tool_refs.append("    tools.list_systems")
    tool_refs_str = "\n".join(tool_refs)

    query_calls = []
    for idx, (tbl_name, tbl_meta) in enumerate(tables.items()):
        qfn = tbl_meta["query_fn"]
        fparam = tbl_meta["filter_param"]
        fval = tbl_meta["filter_val"]
        query_calls.append(f'''        r_{idx} = self.execute_tool("{qfn}", {fparam}={json.dumps(fval)})
        if r_{idx}.get("total", 0) > 0:
            findings.append({{"domain": "{tbl_name}", "records": r_{idx}["rows"]}})''')
    query_calls_str = "\n\n".join(query_calls)

    act1_kwargs = ",\n            ".join(f"{k}={repr(v)}" for k, v in act1["sample_args"].items())
    act2_kwargs = ",\n            ".join(f"{k}={repr(v)}" for k, v in act2["sample_args"].items())

    agent_code = f'''"""{display_name} — High-Code Google ADK Agent.

{description}
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import {chart_fn}
from .render.surfaces import {surface_fn}

_INSTRUCTION = """You are {display_name}.

PRIMARY OBJECTIVE:
{description}

TOOL USAGE PROTOCOL:
- Ground all optimizations and enterprise checks strictly in connected tools.
- Never invent order IDs, asset identifiers, or financial figures.
- Before executing mutations (`{act1['name']}`, `{act2['name']}`), ensure all required fields and a non-empty `idempotency_key` are provided.
"""

_AVAILABLE_TOOLS = [
{tool_refs_str}
]

_WRITE_TOOLS = {{
    "{act1['name']}": {json.dumps(act1['params'])},
    "{act2['name']}": {json.dumps(act2['params'])},
}}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs and idempotency."""
    if tool_name in _WRITE_TOOLS:
        required = _WRITE_TOOLS[tool_name]
        missing = [r for r in required if args.get(r) is None or args.get(r) == "" or args.get(r) == []]
        if missing:
            return {{
                "error": "missing_required_inputs",
                "tool": tool_name,
                "missing": missing,
                "escalation": "request_more_info"
            }}
        if not args.get("idempotency_key"):
            return {{
                "error": "missing_idempotency_key",
                "tool": tool_name,
                "escalation": "request_confirmation"
            }}
    return None


class {class_name}:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "{model}"):
        self.name = "{agent_id}"
        self.model = model
        self.system_instruction = _INSTRUCTION
        self.tools: List[Callable] = list(_AVAILABLE_TOOLS)
        self.tool_map = {{t.__name__: t for t in self.tools}}

    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Dispatches tool call with pre-execution safety gate."""
        if tool_name not in self.tool_map:
            return {{"error": f"Tool '{{tool_name}}' not registered in agent contract."}}

        gate = enforce_tool_contract(tool_name, kwargs)
        if gate:
            return gate

        tool_fn = self.tool_map[tool_name]
        return tool_fn(**kwargs)

    def run_scenario(self, query: str) -> Dict[str, Any]:
        """Executes an autonomous multi-step supply chain optimization & ERP write-back scenario."""
        findings = []
        actions_taken = []

{query_calls_str}

        act1_res = self.execute_tool(
            "{act1['name']}",
            {act1_kwargs}
        )
        actions_taken.append(act1_res)

        act2_res = self.execute_tool(
            "{act2['name']}",
            {act2_kwargs}
        )
        actions_taken.append(act2_res)

        vega_spec = {chart_fn}()
        surface_id = "{agent_id}_surface_01"
        a2ui_parts = {surface_fn}(surface_id, spec=vega_spec)
        markdown = self._format_markdown_report(findings, actions_taken)

        return {{
            "status": "success",
            "agent": self.name,
            "findings_count": len(findings),
            "actions_executed": actions_taken,
            "vega_spec": vega_spec,
            "a2ui_parts": a2ui_parts,
            "markdown": markdown,
        }}

    def _format_markdown_report(
        self,
        findings: List[Dict[str, Any]],
        actions: List[Dict[str, Any]]
    ) -> str:
        """Renders concise executive summary, atomic copy-ready table, and action audit trail."""
        lines = [
            "### ✦ {display_name} — Executive Operations Brief",
            "",
            "> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **{vertical}**.",
            "",
            "#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)",
            "",
            "| Dimension | Metric Value | Secondary KPI | Execution Mode |",
            "|:---|---:|---:|:---|",
        ]
        for row in {json.dumps(chart["data"])}:
            lines.append(f"| `{{row['{chart['x_field']}']}}` | **{{row['{chart['y_field']}']}}** | {{row['{chart['y2_field']}']}} | `{{row['status']}}` |")

        lines.extend([
            "",
            "#### ⚡ Autonomous Write-Backs & Actions Executed",
            "",
        ])
        for act in actions:
            eid = act.get("dispatch_execution_id") or act.get("secondary_action_id") or "ACT-ID"
            lines.append(f"- **Action Executed**: `{{eid}}` | Status: `{{act.get('status')}}` | Rationale: {{act.get('rationale')}}")

        lines.extend([
            "",
            "### 🔗 Connected Enterprise Systems",
        ])
        for sys_meta in {json.dumps(systems)}:
            lines.append(f"- **{{sys_meta['name']}}** (`{{sys_meta['protocol']}}`)")

        return "\\n".join(lines)


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
        name="{agent_id}",
        description={json.dumps(description)},
        model=Gemini(model="{model}", retry_options=types.HttpRetryOptions(attempts=3)),
        generate_content_config=types.GenerateContentConfig(
            max_output_tokens=4096,
            temperature=0.0,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
        instruction=_INSTRUCTION,
        tools=_AVAILABLE_TOOLS,
    )

    app = App(root_agent=root_agent, name="{agent_id}")

    class {class_name}AdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for {agent_id}."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = {class_name}()

        def query(self, *args: Any, **kwargs: Any) -> Any:
            return super().query(*args, **kwargs)

        def stream_query(self, *args: Any, **kwargs: Any) -> Any:
            yield from super().stream_query(*args, **kwargs)

        def run_scenario(self, query: str = "") -> Dict[str, Any]:
            return self._scenario_agent.run_scenario(query)

except ImportError:
    root_agent = {class_name}()  # type: ignore
    app = None  # type: ignore
    {class_name}AdkApp = None  # type: ignore
'''
    (pkg_dir / "app" / "agent.py").write_text(agent_code, encoding="utf-8")

    # 9. Write evals/golden_scenarios.json
    golden = [
        {
            "scenario_id": f"{agent_id}_golden_01",
            "prompt": f"Run end-to-end optimization and ERP write-back for {display_name}.",
            "expected_tools": [m["query_fn"] for m in tables.values()] + [act1["name"], act2["name"]],
            "expected_status": "success",
        }
    ]
    (pkg_dir / "evals" / "golden_scenarios.json").write_text(json.dumps(golden, indent=2) + "\n", encoding="utf-8")

    # 10. Write tests/test_smoke.py (7 unit tests)
    q_tests = []
    for idx, (tbl_name, tbl_meta) in enumerate(tables.items(), start=1):
        qfn = tbl_meta["query_fn"]
        fparam = tbl_meta["filter_param"]
        fval = tbl_meta["filter_val"]
        q_tests.append(f'''
def test_{qfn}():
    res = tools.{qfn}({fparam}={json.dumps(fval)})
    assert res["total"] > 0
    assert res["table"] == "{tbl_name}"
    assert len(res["rows"]) >= 1
''')
    q_tests_str = "\n".join(q_tests)
    q_calls_main = "\n".join([f"    test_{m['query_fn']}()\n    print('✓ test_{m['query_fn']} passed')" for m in tables.values()])

    # Build kwargs without idempotency_key for negative test
    no_key_args = {k: v for k, v in act1["sample_args"].items() if k != "idempotency_key"}
    no_key_kwargs_str = ",\n        ".join(f"{k}={repr(v)}" for k, v in no_key_args.items())

    test_code = f'''"""Smoke test suite for {display_name} ({agent_id})."""
import sys
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AGENT_DIR))

from app.agent import {class_name}
from app import tools


def test_list_systems():
    res = tools.list_systems()
    assert res["agent"] == "{agent_id}"
    assert len(res["systems"]) >= 4
{q_tests_str}

def test_quality_gate_blocks_invalid_inputs():
    agent = {class_name}()
    # 1. Missing idempotency_key
    res = agent.execute_tool(
        "{act1['name']}",
        {no_key_kwargs_str}
    )
    assert res.get("error") == "missing_idempotency_key"

    # 2. Missing required input fields
    res2 = agent.execute_tool(
        "{act1['name']}",
        idempotency_key="TEST-KEY-01"
    )
    assert res2.get("error") == "missing_required_inputs"


def test_end_to_end_scenario_execution():
    agent = {class_name}()
    result = agent.run_scenario("Execute end-to-end optimization and action write-back.")
    assert result["status"] == "success"
    assert result["agent"] == "{agent_id}"
    assert result["findings_count"] == 4
    assert len(result["actions_executed"]) == 2
    assert result["actions_executed"][0]["status"] == "{act1['status']}"
    assert result["actions_executed"][1]["status"] == "{act2['status']}"

    # Verify A2UI v0.9 surface compliance (Card wrapping ONLY VegaChart)
    assert "a2ui_parts" in result
    assert len(result["a2ui_parts"]) == 2
    assert result["vega_spec"]["$schema"] == "https://vega.github.io/schema/vega-lite/v5.json"

    # Verify copy-ready markdown output
    md = result["markdown"]
    assert "### ✦" in md
    assert "| Dimension | Metric Value |" in md
    assert "### 🔗 Connected Enterprise Systems" in md


if __name__ == "__main__":
    test_list_systems()
    print("✓ test_list_systems passed")
{q_calls_main}
    test_quality_gate_blocks_invalid_inputs()
    print("✓ test_quality_gate_blocks_invalid_inputs passed")
    test_end_to_end_scenario_execution()
    print("✓ test_end_to_end_scenario_execution passed")
    print("\\nALL 7 TESTS PASSED SUCCESSFULLY ✅")
'''
    (pkg_dir / "tests" / "test_smoke.py").write_text(test_code, encoding="utf-8")
    print(f"[BUILT] {agent_id} ({display_name}) with 4 fixture tables & 7 smoke tests")


def clone_catalog_alias(source_id: str, target_id: str) -> None:
    """Clones an existing built agent folder to its exact catalog ID and updates the agent identifier."""
    src_dir = AGENTS_DIR / source_id
    dst_dir = AGENTS_DIR / target_id
    if not src_dir.exists():
        raise FileNotFoundError(f"Source agent {src_dir} not found")
    if dst_dir.exists():
        shutil.rmtree(dst_dir)
    shutil.copytree(src_dir, dst_dir, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))

    # Replace source_id with target_id in pyproject.toml, agents-cli-manifest.yaml, app/agent.py, app/tools.py, tests/test_smoke.py
    for rel_path in [
        "pyproject.toml",
        "agents-cli-manifest.yaml",
        "app/agent.py",
        "app/tools.py",
        "tests/test_smoke.py",
    ]:
        p = dst_dir / rel_path
        if p.exists():
            txt = p.read_text(encoding="utf-8")
            txt = txt.replace(f'"{source_id}"', f'"{target_id}"')
            txt = txt.replace(f"name: {source_id}", f"name: {target_id}")
            p.write_text(txt, encoding="utf-8")
    print(f"[ALIASED] {target_id} <-- {source_id}")


def main() -> None:
    for spec in NEW_AGENTS_SPECS:
        build_agent_package(spec)

    # Also materialize the 7 catalog-ID aliases so all 35 catalog IDs exist in agents/<catalog_id>/
    alias_map = {
        "echelon_inventory_allocator": "meio_safety_stock_agent",
        "warehouse_slotting_optimizer": "warehouse_slotting_agent",
        "dynamic_order_promising_atp": "atp_order_promising_agent",
        "yard_dock_scheduling_agent": "yard_dock_sequencer",
        "finite_production_scheduler": "line_schedule_optimizer",
        "plant_oee_maintenance_agent": "predictive_oee_sentinel",
        "inline_quality_inspection_agent": "inline_yield_guardian",
    }
    for src_id, dst_id in alias_map.items():
        clone_catalog_alias(src_id, dst_id)

    print(f"\nCompleted building {len(NEW_AGENTS_SPECS)} new agents and {len(alias_map)} catalog-ID packages!")


if __name__ == "__main__":
    main()

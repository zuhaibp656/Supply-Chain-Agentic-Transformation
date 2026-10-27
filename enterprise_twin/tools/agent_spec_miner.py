"""Agent Specification Miner Tool.

Adapts the operational details INSIDE each of the 60 Categorized AI Agents for a target enterprise
while keeping the core base of each agent identical (preserving its fundamental purpose,
algorithmic foundation, and OR-Tools / TimesFM / Spanner / Maps engine).
"""

from typing import Dict, Any


def mine_company_agent_specs(company_name: str, industry_id: str) -> Dict[str, Any]:
    """Mines enterprise-tailored operational specs for the 60 Categorized AI agents."""
    c_lower = company_name.lower()

    if 'itc' in c_lower or industry_id == 'fmcg_agribusiness':
        return {
            'demand_sensing_agent': {
                'systems': f'SAP S/4HANA FMCG · ITC e-Choupal Rural Agri Portal · APMC Mandi Feeds · Mother Godown WMS · BigQuery · Vertex AI TimesFM',
                'problemDetails': f'Seasonal monsoon shifts, wheat and spice harvest arrival fluctuations, and volatile wholesale demand across 2M+ kirana retail stores create persistent regional stockouts and distributor inventory imbalances.',
                'solutionDetails': f'PulseCast ingests daily e-Choupal farmgate arrivals, APMC mandi arrivals and spot prices, distributor order feeds, and weather patterns into Vertex AI TimesFM with hierarchical brand-pack reconciliation across Aashirvaad, Sunfeast, and Bingo! lines.',
                'outcomeDetails': f'Prevents festive stockouts across rural Carrying & Forwarding Agents (CFAs); cuts forecast error by 24% and frees ₹45 Crore in trapped distributor working capital.',
                'roiBadges': ['₹45 Cr Cash Freed', '-24% Forecast Error', '45-Min S&OP Consensus', '99.4% Kirana OTIF']
            },
            'mps_finite_scheduler': {
                'systems': f'SAP S/4HANA PP/DS · Siemens Opcenter MES · ICML Integrated Plant SCADA · OSIsoft PI · OR-Tools CP-SAT',
                'problemDetails': f'Frequent recipe changes across high-speed biscuit baking lines, snack seasoning drums, and packaging conversions trigger excessive washdowns, dough wastage, and oven idling.',
                'solutionDetails': f'Orchestrates OR-Tools CP-SAT sequence-dependent setup optimization across ITC Integrated Consumer Goods Manufacturing and Logistics (ICML) plants, grouping similar dough and flavor profiles to minimize clean-in-place (CIP) turnaround.',
                'outcomeDetails': f'Increases effective line uptime by 14.8%; cuts product changeover waste by 34% and eliminates ₹18 Crore in annual packaging scrap.',
                'roiBadges': ['+14.8% Plant OEE', '-34% CIP Downtime', '₹18 Cr Scrap Saved', '100% Traceability']
            },
            'category_should_cost': {
                'systems': f'SAP Ariba · ITC e-Choupal Sourcing Network · Agmarknet Mandi Index · BigQuery Commodity Models',
                'problemDetails': f'Procurement teams struggle to benchmark farmgate wheat, tobacco leaf, and packaging laminate quotes against volatile global commodity indices and domestic agricultural MSP policies.',
                'solutionDetails': f'Parametrically breaks down should-costs based on farmgate mandi arrivals, crop yield forecasts, moisture adjustments, diesel freight tariffs, and converting overheads.',
                'outcomeDetails': f'Unlocks ₹62 Crore in direct sourcing savings and establishes automated should-cost price corridors for e-Choupal procurement.',
                'roiBadges': ['₹62 Cr Spend Saved', '-8.2% Sourcing Cost', 'Zero Spec Leakage', 'Fair Farmer Price']
            },
            'tier_n_spanner_graph': {
                'systems': f'Cloud Spanner Graph · ITC e-Choupal Village Kiosks · APMC Agri-Feeds · BigQuery GIS',
                'problemDetails': f'Disruptions at regional agricultural cooperatives, localized crop diseases, and unseasonal rains stay invisible until procurement targets fall short at processing plants.',
                'solutionDetails': f'Builds a live Cloud Spanner graph mapping 40,000+ village farming clusters, primary mandi aggregators, packaging converters, and ICML factory nodes with automated yield propagation.',
                'outcomeDetails': f'Provides 14-day early warning on commodity supply deficits, dynamically rerouting procurement quotas to surplus agricultural districts.',
                'roiBadges': ['14-Day Early Warning', '40K+ Sourcing Nodes', '100% Traceability', '-65% Disruption Risk']
            },
            'working_capital_cash_bridge': {
                'systems': f'SAP S/4HANA Finance · BigQuery Cash Ledger · CFA Depot Portals · Google Looker',
                'problemDetails': f'Working capital is locked across multi-tier Carrying & Forwarding Agents (CFAs) and wholesale godowns due to cautious safety-stock hoarding during peak harvest seasons.',
                'solutionDetails': f'Generates an automated daily bridge between supply chain inventory velocity and corporate treasury cash flows, identifying high-toil stock points and rebalancing working capital.',
                'outcomeDetails': f'Releases ₹85 Crore in enterprise working capital while improving service levels to retail distributors across Tier-2 and rural markets.',
                'roiBadges': ['₹85 Cr Cash Released', '-14 Days DSI', '+1.4% Operating Margin', 'Live Treasury Bridge']
            }
        }
    elif 'volkswagen' in c_lower or industry_id == 'automotive':
        return {
            'demand_sensing_agent': {
                'systems': f'SAP S/4HANA Wolfsburg · Siemens Opcenter MES · PowerCo Cell ERP · EDI 830/852 Dealer Feeds · BigQuery · Vertex AI TimesFM',
                'problemDetails': f'Monthly dealer order spreadsheets lack real-time visibility into electric vehicle (EV) trim-level take rates and battery capacity constraints, creating 6-week blindspots and assembly line imbalances.',
                'solutionDetails': f'PulseCast continuously ingests vehicle configurator signals, dealer showroom reservation curves, and European dealer inventory into TimesFM with hierarchical trim and powertrain reconciliation (BEV vs. ICE).',
                'outcomeDetails': f'Eliminates line starvation at Wolfsburg and Zwickau MEB plants; cuts finished vehicle lot dwell by 18 days (€42M in working capital freed).',
                'roiBadges': ['€42M Cash Freed', '-24% Forecast Error', 'Zero Line Stops', '100% Battery Pegging']
            },
            'mps_finite_scheduler': {
                'systems': f'Siemens Opcenter MES · SAP PP/DS · KUKA Body Shop SCADA · OR-Tools CP-SAT',
                'problemDetails': f'Stamping press coil changeovers, paint shop color block flushes, and just-in-sequence (JIS) chassis line feeding are frequently derailed by late supplier sub-assemblies.',
                'solutionDetails': f'OR-Tools CP-SAT finite capacity job-shop solver sequences body-in-white stamping, paint shop color blocks, and final assembly line feeding to lock 100% material pegging 48 hours before body drop.',
                'outcomeDetails': f'Reduces paint shop solvent purge waste by 28%; cuts line changeover delays by 32% and prevents assembly line stops across global MEB gigafactories.',
                'roiBadges': ['-32% Changeover Delay', '-28% Solvent Waste', '100% JIS Sequence', 'Zero Line Halts']
            },
            'category_should_cost': {
                'systems': f'SAP Ariba · Siemens Teamcenter BOM · London Metal Exchange Feeds · BigQuery ML',
                'problemDetails': f'Surging prices and opaque supplier markups on lithium cathode active materials, battery modules, and microcontrollers inflate vehicle bill of materials (BOM) costs.',
                'solutionDetails': f'Decomposes Tier-1 automotive sub-assemblies into raw raw-material indices (LME nickel/cobalt, engineered plastics, stamping steel) and clean-sheet manufacturing cycle times.',
                'outcomeDetails': f'Saves €110M in annual powertrain and electronics procurement negotiations; establishes transparent should-cost price corridors across Tier-1 suppliers.',
                'roiBadges': ['€110M Spend Saved', '-7.4% Component Cost', '100% BOM Visibility', 'Clean-Sheet Clout']
            },
            'fleet_route_dispatch_optimizer': {
                'systems': f'SAP TM · Port of Emden Vehicle Logistics Portal · Google Maps Routes Preferred API · OR-Tools CVRPTW',
                'problemDetails': f'Outbound vehicle logistics dispatchers manually assign finished cars to 9-car double-deck haulers, resulting in high deadhead return miles and vehicle bumper damage.',
                'solutionDetails': f'Solves heterogeneous 3D vehicle hauler spatial loading combined with Google Maps corridor routing, synchronizing factory yard gate dispatches with European dealer compound deliveries.',
                'outcomeDetails': f'Cuts empty return miles by 24%; improves dealer delivery on-time arrival to 98.6% and reduces in-transit vehicle scratches and damage claims by 40%.',
                'roiBadges': ['-24% Empty Miles', '98.6% On-Time Delivery', '-40% In-Transit Damage', '3D Spatial Loading']
            }
        }
    elif 'boeing' in c_lower or industry_id == 'aerospace_defense':
        return {
            'demand_sensing_agent': {
                'systems': f'Dassault Systemes ENOVIA · SAP S/4HANA Aerospace · FAA Airworthiness Registry · BigQuery · Vertex AI TimesFM',
                'problemDetails': f'Multi-year airline fleet deliveries, lease return cycles, and defense contract milestone changes create unpredictable demand variations that ripple through multi-tier aerostructure suppliers.',
                'solutionDetails': f'Ingests global airline passenger load trends, fleet retirement projections, and commercial airframe order backlogs into Vertex AI TimesFM to generate calibrated milestone demand schedules.',
                'outcomeDetails': f'Stabilizes master production schedules across 737 and 787 final assembly lines; cuts parts expediting premiums by $55M.',
                'roiBadges': ['$55M Expediting Saved', '-28% Lead Time Variance', '100% Delivery Schedule', 'FAA Compliant']
            },
            'category_should_cost': {
                'systems': f'SAP Ariba · Dassault CATIA CAD/BOM · Titanium Fastener Indices · BigQuery Parametric Models',
                'problemDetails': f'Aerospace-grade titanium forgings, carbon fiber composite pre-pregs, and complex CNC machined ribs suffer from monopolistic supplier pricing and unpredictable metal surcharges.',
                'solutionDetails': f'Performs bottom-up parametric should-cost analysis decomposing 5-axis CNC machining hours, autoclave cure cycles, and raw titanium ingot prices to establish should-cost benchmarks.',
                'outcomeDetails': f'Yields $140M in validated cost savings during multi-year aerostructure and avionics supplier renegotiations.',
                'roiBadges': ['$140M Cost Saved', '-9.1% Aerostructure Cost', 'Parametric CAD Audit', 'Zero Audit Gaps']
            },
            'mps_finite_scheduler': {
                'systems': f'Siemens Opcenter MES · SAP PP/DS Aerospace · Boeing Renton Factory SCADA · OR-Tools CP-SAT',
                'problemDetails': f'Wing-to-body joins, electrical wire harness threading, and cabin interior installations face severe traveling work bottlenecks when specialized mechanics or FAA-inspected parts arrive out of sequence.',
                'solutionDetails': f'Finite-capacity job-shop scheduling in OR-Tools dynamically balances assembly positions (dock stations) with technician skill certifications and FAA conformity inspection sign-offs.',
                'outcomeDetails': f'Reduces traveled work in final assembly by 62%; accelerates 737/787 rollout cadence and protects against millions in delivery delay liquidated damages.',
                'roiBadges': ['-62% Traveled Work', '+18% Assembly Cadence', '100% FAA Conformity', 'Zero Dock Gridlock']
            }
        }
    elif 'caterpillar' in c_lower or industry_id == 'heavy_machinery':
        return {
            'demand_sensing_agent': {
                'systems': f'SAP S/4HANA · Cat Dealer Network Portal · Mining Equipment Utilization Feeds · BigQuery · TimesFM',
                'problemDetails': f'Global mining commodity cycles, infrastructure stimulus bills, and dealer rental fleet utilization spikes create extreme boom-and-bust order swings across large excavator and bulldozer lines.',
                'solutionDetails': f'Correlates global heavy construction bidding activity, mining commodity indexes, and Cat machine telematics (run hours, engine duty cycles) to forecast machine and parts replenishment.',
                'outcomeDetails': f'Reduces dealer parts stockouts by 34%; unlocks $75M in excess finished machine buffer inventory.',
                'roiBadges': ['$75M Inventory Freed', '-34% Parts Stockout', '24-Hour Part Guarantee', '99.2% Dealer OTIF']
            },
            'reverse_logistics_mgr': {
                'systems': f'Cat Reman Core Management System · SAP S/4HANA Reverse · Heavy Logistics Network',
                'problemDetails': f'Used diesel engine blocks, hydraulic cylinders, and transmissions (cores) sit in dealer scrap yards instead of returning to remanufacturing plants for circular re-machining.',
                'solutionDetails': f'Tracks and incentives dealer core returns with automated core credit verification, dynamic backhaul freight allocation, and circular remanufacturing production planning.',
                'outcomeDetails': f'Accelerates core turnaround by 26 days; remanufactures 140M lbs of heavy components annually while saving 85% of virgin raw steel.',
                'roiBadges': ['140M lbs Steel Reclaimed', '-26 Days Core Return', '-45% Reman Cost', 'Zero Landfill']
            }
        }
    else:
        # Default intelligent template
        return {
            'demand_sensing_agent': {
                'systems': f'SAP S/4HANA · Enterprise POS & CRM Feeds · BigQuery · Vertex AI TimesFM',
                'problemDetails': f'Disconnected regional spreadsheets, lack of customer sell-through visibility, and promotion cannibalization create costly stockouts and working capital build-ups for {company_name}.',
                'solutionDetails': f'PulseCast Demand Sensing Copilot ingests live point-of-sale data, distributor orders, and market signals into Vertex AI TimesFM with hierarchical SKU reconciliation.',
                'outcomeDetails': f'Cuts demand forecast error by 24% for {company_name}; unlocks 18% in trapped safety stock working capital.',
                'roiBadges': ['-24% Forecast Error', '18% Working Capital Freed', '45-Min S&OP Consensus', '99.2% Customer OTIF']
            }
        }


# Automatically alias canonical 60-agent IDs to industry-specific overrides
_ORIG_MINE_SPECS = mine_company_agent_specs

def mine_company_agent_specs(company_name: str, industry_id: str) -> Dict[str, Any]:
    res = dict(_ORIG_MINE_SPECS(company_name, industry_id))
    alias_pairs = [
        ("mps_finite_scheduler", "finite_production_scheduler"),
        ("category_should_cost", "rfq_should_cost_agent"),
        ("category_should_cost", "commodity_index_advisor"),
        ("tier_n_spanner_graph", "tier_n_risk_sentinel"),
        ("reverse_logistics_mgr", "reverse_rma_recommerce_agent"),
        ("reverse_logistics_mgr", "returns_triage_agent"),
    ]
    for old_k, new_k in alias_pairs:
        if old_k in res and new_k not in res:
            res[new_k] = dict(res[old_k])
    return res

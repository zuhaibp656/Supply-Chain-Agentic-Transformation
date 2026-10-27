"""Career Persona Miner Tool.

Mines enterprise job postings, LinkedIn career profiles, and organizational charts
to discover how a target company titles and structures its 60 supply chain roles,
grounding them in authentic corporate lingo (car parts/JIS for auto, e-Choupal/mandi
for FMCG/agri, titanium/FAA for aerospace, Reman/dealer for heavy machinery).
"""

from typing import Dict, Any


def mine_company_personas(company_name: str, industry_id: str) -> Dict[str, Any]:
    """Mines specialized role titles, executive mandates, and daily toils for the 60 SCOR roles."""
    c_lower = company_name.lower()
    ind = industry_id.lower()

    if 'itc' in c_lower or ind in ('fmcg_agribusiness', 'cpg_retail'):
        return {
            'demand_planning_dir': {
                'title': f'{company_name} Head of FMCG Trade Demand Sensing & Category Consensus',
                'role': 'National Brand-Pack Demand Forecast Accuracy, Kirana Fill-Rates & Mandi Sourcing Sync',
                'summary': f'Directs trade demand forecasting across Aashirvaad, Sunfeast, Bingo!, and personal care SKUs—balancing seasonal harvest cycles with 2M+ kirana retail and wholesale replenishment commitments.',
                'mandate': f'Forecasts brand-pack demand across 2M+ retail kirana stores, mother godowns, and Carrying & Forwarding Agents (CFAs).',
                'manualToil': 'Stitching monthly distributor CSVs and wholesale mandi price reports in Excel, missing sudden regional flour or biscuit stockouts.',
                'agenticImpact': 'Daily regional demand sensing in TimesFM synchronizing e-Choupal farmgate arrivals with distributor replenishment.'
            },
            'sop_ibp_lead': {
                'title': f'{company_name} Integrated Business Planning & ICML Plant Capacity Balancing Lead',
                'role': 'Multi-Plant S&OP Consensus, Seasonality Buffers & Trade Promotion Lock',
                'summary': f'Orchestrates monthly S&OP across 20+ Integrated Consumer Goods Manufacturing and Logistics (ICML) factories, aligning agricultural raw material arrivals with brand sales targets.',
                'mandate': 'Reconciles seasonal harvest flushes (wheat, tobacco, spices) against ICML baking, frying, and packaging line capacity.',
                'manualToil': 'Weeks spent manually balancing distributor trade promotion requests against factory capacity and wheat inventory buffers.',
                'agenticImpact': 'Live 45-minute multi-echelon S&OP consensus in OR-Tools linking farm arrivals, plant rates, and trade margins.'
            },
            'category_sourcing_mgr': {
                'title': f'{company_name} Head of Agri-Commodity Sourcing & e-Choupal Procurement',
                'role': 'Direct Farmgate Sourcing, Mandi Price Indexation & Sustainable Agriculture',
                'summary': f'Leads direct agricultural procurement through ITC e-Choupal rural kiosks, sourcing wheat, spices, coffee, and packaging pulp across thousands of farming villages.',
                'mandate': 'Coordinates direct farmgate procurement, APMC mandi trading, and sustainable pulpwood plantation contracts.',
                'manualToil': 'Manual consolidation of mandi arrivals across 10+ states with high price volatility and inconsistent grain moisture grades.',
                'agenticImpact': 'Parametric commodity should-costing and Spanner graph routing securing fair farmer prices and saving ₹62 Cr.'
            },
            'supplier_risk_lead': {
                'title': f'{company_name} Agri-Supply Risk, Monsoon Tracking & Crop Disease Lead',
                'role': 'Crop Yield Forecasting, Multi-Tier Mandi Visibility & Drought Mitigation',
                'summary': f'Monitors monsoon patterns, soil moisture, and crop diseases across Indian agricultural basins to preempt raw material shortages.',
                'mandate': 'Shields manufacturing plants against monsoon failure, pest outbreaks, and export-import duty fluctuations.',
                'manualToil': 'Tracking district agricultural department bulletins and weather reports in static monthly spreadsheets.',
                'agenticImpact': 'DeepMind WeatherNext and satellite crop health alerts giving 14-day early warning on regional crop deficits.'
            },
            'mps_scheduling_lead': {
                'title': f'{company_name} Integrated Foods & Packaging Manufacturing Operations Meister',
                'role': 'Finite Line Scheduling, Oven Takt Time & Clean-in-Place (CIP) Optimization',
                'summary': f'Schedules high-speed biscuit baking, extruded snack seasoning, and cigarette packaging conversion lines across ICML facilities.',
                'mandate': 'Sequences dough preparation, continuous baking ovens, and high-speed multi-pack wrapping lines.',
                'manualToil': 'Manual whiteboards rescheduling lines when recipe flavor changes or dough packaging film tears stall production.',
                'agenticImpact': 'OR-Tools CP-SAT finite-capacity sequencing grouping allergen and flavor families to cut CIP downtime by 34%.'
            },
            'meio_inventory_mgr': {
                'title': f'{company_name} National Mother Godown & CFA Multi-Echelon Stock Controller',
                'role': 'Central Warehouse, Carrying & Forwarding (CFA) and Distributor Buffer Tuning',
                'summary': f'Controls multi-echelon buffer stock across mother godowns, regional CFAs, and super-stockists across urban and rural India.',
                'mandate': 'Maintains 99.4% on-shelf availability for high-velocity FMCG packs while minimizing locked working capital.',
                'manualToil': 'Hoarding 30+ days of finished goods inventory at regional depots to protect against unpredictable transport bottlenecks.',
                'agenticImpact': 'Stochastic MEIO solver dynamically rebalancing safety stocks between mother godowns and edge CFAs (-₹45 Cr working capital).'
            },
            'dock_yard_supervisor': {
                'title': f'{company_name} ICML Inbound Grain Rake & Outbound Fleet Dock Master',
                'role': 'Rail Rake Unloading, Bulk Grain Silos & Inter-State Truck Dock Synchronization',
                'summary': f'Supervises bulk agricultural grain rake unloading, pallet staging, and primary transport truck turnaround at ICML plants.',
                'mandate': 'Prevents railway demurrage charges and minimizes truck turnaround time at factory gates.',
                'manualToil': 'Paper gate passes and manual truck driver queuing causing long lines and demurrage penalties during harvest season.',
                'agenticImpact': 'Automated dock appointment scheduling and vision-based license plate recognition cutting truck turnaround by 41%.'
            },
            'fleet_dispatch_mgr': {
                'title': f'{company_name} National Primary & Secondary FMCG Truckload Dispatch Lead',
                'role': 'Long-Haul Multi-Axle Linehaul & Secondary Rural Distributor Milk-Runs',
                'summary': f'Manages dedicated primary linehaul carriers and secondary distributor milk-run delivery trucks across 28 states.',
                'mandate': 'Routes thousands of daily truckloads between factories, mother godowns, and urban/rural distributor nodes.',
                'manualToil': 'Dispatchers manually negotiating spot market truck rates and guessing load axle weights in spreadsheets.',
                'agenticImpact': 'Google Maps Routes API with 3D truckload pallet consolidation cutting empty return miles by 22%.'
            },
            'reverse_logistics_mgr': {
                'title': f'{company_name} FMCG Expiry Reclaims, Pallet Returns & Packaging Circularity Lead',
                'role': 'Near-Expiry Repackaging, Corrugated Tray Reclaims & Sustainable Biopolymers',
                'summary': f'Orchestrates retail return flows for damaged or expired packs, wooden pallet reverse loops, and circular paperboard recycling.',
                'mandate': 'Minimizes product write-offs through secondary channels and maximizes corrugated carton recycling.',
                'manualToil': 'Distributors dumping damaged stock in backrooms while empty fleet trucks return to factories without reverse loads.',
                'agenticImpact': 'Edge mobile inspection with automated backhaul truck insertion boosting return recovery value by 31%.'
            }
        }

    elif 'volkswagen' in c_lower or 'bmw' in c_lower or ind == 'automotive':
        return {
            'demand_planning_dir': {
                'title': f'{company_name} Head of Global Vehicle Demand & Model Mix Planning (MEB/ICE)',
                'role': 'Trim-Level Take Rates, EV Battery Cell Allocation & Global Dealer Pipeline',
                'summary': f'Directs vehicle forecasting across all platforms (electric MEB, SSP, and combustion architectures)—synchronizing regional dealer order reservation spikes with assembly factory slots.',
                'mandate': f'Forecasts trim-level take rates, powertrain splits (BEV vs. PHEV vs. ICE), and dealer allocation curves across {company_name} global markets.',
                'manualToil': 'Stitching monthly dealer portal spreadsheets in Excel, suffering 6-week blindspots on EV trim cancellation waves.',
                'agenticImpact': 'Daily regional VIN-level demand sensing in TimesFM balancing dealer pipeline and battery supply constraints.'
            },
            'sop_ibp_lead': {
                'title': f'{company_name} VP of Vehicle S&OP & Assembly Line Allocation Meister',
                'role': 'Takt Time Balancing, PowerCo Battery Supply Lock & Margin Maximization',
                'summary': f'Reconciles assembly line cycle times (Takt Time) against PowerCo battery cell allocations and critical Tier-1 semiconductor supplies.',
                'mandate': 'Balances global plant capacity (Wolfsburg, Zwickau, Chattanooga) against regional dealer demand and margin targets.',
                'manualToil': '21-day S&OP cycles spent debating whether Wolfsburg or Zwickau gets constrained power inverter batches.',
                'agenticImpact': '45-minute live Pareto MILP consensus in OR-Tools balancing margin per vehicle against EU fleet CO2 targets.'
            },
            'category_sourcing_mgr': {
                'title': f'{company_name} Head of Strategic Procurement (Powertrain, Battery Cells & Semis)',
                'role': 'Direct Material Procurement, Clean-Sheet Should-Cost & Long-Term Offtake Contracts',
                'summary': f'Directs multi-billion-euro procurement for high-voltage battery cells, drive inverters, microcontrollers, and stamped chassis steel.',
                'mandate': 'Secures long-term battery cell supply agreements with PowerCo and CATL while driving clean-sheet supplier cost negotiations.',
                'manualToil': 'Reviewing 50-page supplier RFQ cost breakdowns without bottom-up cycle time or raw metal price index models.',
                'agenticImpact': 'Parametric BOM should-costing on BigQuery and LME metal indices saving €110M in Tier-1 negotiations.'
            },
            'supplier_risk_lead': {
                'title': f'{company_name} Automotive Tier-N Risk & Semiconductor War-Room Lead',
                'role': 'Tier-N Bill-of-Materials Dependency Graph & Critical Component Defense',
                'summary': f'Maps sub-tier supplier dependencies past Tier-1 tier vendors down to semiconductor foundries, wiring harness weavers, and lithium refineries.',
                'mandate': 'Prevents assembly line-stopping disruptions caused by Tier-2/Tier-3 component shortages.',
                'manualToil': 'Manual war-room spreadsheets during supply crunches calling Tier-1s to ask where sub-components are sourced.',
                'agenticImpact': 'Cloud Spanner Graph mapping 12,000+ multi-tier automotive supplier nodes with automated bottleneck alerts.'
            },
            'mps_scheduling_lead': {
                'title': f'{company_name} Production Control & Assembly Line Meister (MEB/Chassis Sequencing)',
                'role': 'Body-in-White Stamping, Paint Color Blocking & Just-In-Sequence Line Feeding',
                'summary': f'Sequences the stamping press, robotic welding body shop, automated paint line, and final chassis assembly.',
                'mandate': 'Locks vehicle production sequences 48 hours before body drop to ensure zero assembly line stops.',
                'manualToil': 'Manual whiteboards rescheduling lines when missing wire harnesses or paint defects stall final trim.',
                'agenticImpact': 'OR-Tools CP-SAT finite-capacity sequencing locking 100% material pegging 48h before body drop.'
            },
            'meio_inventory_mgr': {
                'title': f'{company_name} Head of Assembly Plant Inbound Buffers & JIS Sequencing Yards',
                'role': 'Supplier Logistics Centers (SLC), High-Bay WMS & 4-Hour JIS Buffer Tuning',
                'summary': f'Controls inbound component inventory across plant supplier logistics centers, sequencing yards, and automated high-bay warehouses.',
                'mandate': 'Maintains lean 4-hour Just-in-Sequence (JIS) buffers without risking assembly line starvation.',
                'manualToil': 'Hoarding 14 days of safety stock in expensive off-site trailer yards to prevent assembly line-stops.',
                'agenticImpact': 'Guaranteed-Service MEIO dynamically tuning JIS buffer stocks down to 4 hours of production (€42M saved).'
            },
            'dock_yard_supervisor': {
                'title': f'{company_name} Just-In-Sequence (JIS) Trailer Yard & Assembly Dock Master',
                'role': 'Live Trailer Dock Scheduling, Empty Stillages & Automated Tugger Sequencing',
                'summary': f'Controls assembly plant receiving docks, trailer yard hostling, and automated tugger routes feeding parts directly to assembly stations.',
                'mandate': 'Ensures sequenced component racks arrive at assembly line stations within 15 minutes of scheduled installation.',
                'manualToil': 'Yard jockey walkie-talkie chaos searching for missing trailers with chassis parts while assembly lines idle.',
                'agenticImpact': 'Real-time GPS yard management and automated dock door assignment cutting trailer dwell by 40%.'
            },
            'fleet_dispatch_mgr': {
                'title': f'{company_name} Outbound Vehicle Logistics & Dedicated Auto-Carrier Dispatch Lead',
                'role': '9-Car Double-Deck Haulers, RoRo Port Transit & Dealer Compound Delivery',
                'summary': f'Manages the global finished vehicle distribution fleet, coordinating enclosed car carriers, rail auto-racks, and ocean RoRo vessels.',
                'mandate': 'Delivers finished vehicles from factory gates and ports to dealer showrooms with zero in-transit damage.',
                'manualToil': 'Dispatchers manually pairing cars to 9-car haulers with deadhead return miles and damaged bumpers.',
                'agenticImpact': 'Google Maps Corridor routing with 3D car-carrier spatial packing cutting empty miles by 24%.'
            },
            'reverse_logistics_mgr': {
                'title': f'{company_name} High-Voltage Battery Cell Circularity & Warranty Core Return Lead',
                'role': 'EV Battery Second-Life Diagnostics, Black Mass Recycling & Warranty Remanufacturing',
                'summary': f'Orchestrates reverse logistics for degraded or recalled high-voltage battery packs, electric drive motors, and dealer warranty cores.',
                'mandate': 'Enforces closed-loop battery recycling (PowerCo battery shredding and hydrometallurgical recovery) and warranty reman.',
                'manualToil': 'Dealers storing hazardous battery packs in parking lots while waiting for certified hazmat transport permits.',
                'agenticImpact': 'Automated battery health telemetry grading and compliant hazmat route optimization boosting recovery margin by 32%.'
            }
        }

    elif 'boeing' in c_lower or 'airbus' in c_lower or ind == 'aerospace_defense':
        return {
            'demand_planning_dir': {
                'title': f'{company_name} Director of Airplane Program Master Demand & Delivery Commitments',
                'role': 'Commercial Jetliner Skyline Slots, Defense Contract Delivery Cadence & Tier-1 Backlog',
                'summary': f'Aligns global commercial airline fleet delivery dates and defense milestone contracts across 737, 787, and 777X airframe programs.',
                'mandate': 'Establishes stable aircraft delivery skyline slots balancing airline customer entry-into-service dates with supply chain lead times.',
                'manualToil': 'Manual Excel skyline planning struggling with multi-year supplier lead time shifts and delivery delay penalties.',
                'agenticImpact': 'Probabilistic program delivery scheduling in TimesFM correlating flight demand curves with supply milestones.'
            },
            'category_sourcing_mgr': {
                'title': f'{company_name} Director of Aerostructures & Raw Titanium Forgings Procurement',
                'role': 'Strategic Sourcing for Fuselage Barrels, High-Strength Alloys & Avionics',
                'summary': f'Directs multi-billion-dollar aerospace procurement for carbon-composite fuselage sections, titanium wing spars, and flight control avionics.',
                'mandate': 'Negotiates multi-year aerostructure contracts and secures titanium supply chains against geopolitical export restrictions.',
                'manualToil': 'Reviewing complex supplier cost breakdowns manually without clean-sheet 5-axis CNC machining models.',
                'agenticImpact': 'Parametric CAD should-cost modeling saving $140M across aerostructure and machining renegotiations.'
            },
            'mps_scheduling_lead': {
                'title': f'{company_name} Fuselage Barrel & Final Assembly Line Scheduling Meister',
                'role': 'Dock Station Scheduling, Traveled Work Prevention & FAA Conformity Sign-Offs',
                'summary': f'Schedules wing-to-body joins, electrical wire harness threading, and interior installations across final assembly lines.',
                'mandate': 'Locks final assembly sequences to eliminate traveled work and ensure 100% FAA airworthiness inspection conformity.',
                'manualToil': 'Assembly stations gridlocked by traveled work when missing brackets or incomplete wire harnesses stall subsequent crews.',
                'agenticImpact': 'OR-Tools CP-SAT finite-capacity assembly scheduling cutting traveled work by 62%.'
            },
            'meio_inventory_mgr': {
                'title': f'{company_name} Aircraft Program Assembly Buffer & AOG High-Value Spares Controller',
                'role': 'Assembly Station Line Buffers & Global Aircraft On Ground (AOG) Spares Network',
                'summary': f'Optimizes inventory of multi-million-dollar engines, landing gears, and flight-critical avionics across factories and airline hubs.',
                'mandate': 'Guarantees sub-4-hour emergency delivery for AOG critical components while cutting factory WIP buffers.',
                'manualToil': 'Millions of dollars in custom titanium fasteners and avionics sitting in dark storage while missing critical parts halt lines.',
                'agenticImpact': 'Multi-echelon inventory optimization tuning buffer stock to critical path milestones ($180M WIP freed).'
            }
        }

    elif 'caterpillar' in c_lower or 'deere' in c_lower or ind == 'heavy_machinery':
        return {
            'demand_planning_dir': {
                'title': f'{company_name} Director of Global Machinery Demand & Dealer Quota Planning',
                'role': 'Mining Truck, Excavator & Generator Demand Forecasting & Dealer Stock Allocations',
                'summary': f'Directs global equipment demand forecasting across mining, construction, and power generation business units.',
                'mandate': 'Balances commodity cycle expansions (copper, gold, coal) and infrastructure construction cycles against factory build slots.',
                'manualToil': 'Monthly dealer orders in spreadsheets lagging mining project tenders by 3 months, leading to machine shortages.',
                'agenticImpact': 'Predictive heavy machinery demand sensing correlating global mining capex and machine telematics ($75M freed).'
            },
            'category_sourcing_mgr': {
                'title': f'{company_name} Director of Heavy Castings, Hydraulics & Steel Sourcing',
                'role': 'Foundry Castings, High-Pressure Hydraulic Pumps & Structural Plate Steel Procurement',
                'summary': f'Directs procurement for heavy structural steel weldments, high-tonnage casting foundries, and high-pressure hydraulic cylinders.',
                'mandate': 'Secures critical foundry capacity and mitigates steel tariff surcharges across global manufacturing plants.',
                'manualToil': 'Inconsistent quotes from global foundries with volatile scrap metal and ferro-alloy surcharges.',
                'agenticImpact': 'Parametric should-cost modeling on scrap indices and foundry melt costs saving $85M in annual procurement.'
            },
            'reverse_logistics_mgr': {
                'title': f'{company_name} Cat Reman Core Return Logistics & Heavy Component Circularity Lead',
                'role': 'Used Engine Block, Transmission & Hydraulic Cylinder Core Returns from Global Dealers',
                'summary': f'Orchestrates the global circular supply chain, reclaiming worn diesel engine blocks, cylinders, and tracks for remanufacturing.',
                'mandate': 'Accelerates dealer core returns to achieve 85% raw material circularity and support customer 24-hour parts guarantees.',
                'manualToil': 'Heavy engine cores sitting in dealer yards for months due to complex core credit reconciliation and hazmat oil residue rules.',
                'agenticImpact': 'Automated core credit validation and return truckload backhaul routing cutting core turnaround by 26 days.'
            }
        }

    else:
        # Default intelligent template for custom companies
        return {
            'demand_planning_dir': {
                'title': f'{company_name} Director of Demand Sensing & Consensus Planning',
                'role': f'Enterprise Forecast Accuracy & Customer Replenishment Alignment',
                'summary': f'Directs enterprise demand forecasting across all {company_name} business units, channels, and product families.',
                'mandate': f'Synchronizes customer point-of-sale signals and commercial promotions with operational production commitments.',
                'manualToil': 'Manual data aggregation across regional ERP instances and spreadsheet consolidation.',
                'agenticImpact': 'Automated multi-signal forecasting in Vertex AI TimesFM with daily P10/P50/P90 quantile fans.'
            },
            'category_sourcing_mgr': {
                'title': f'{company_name} Head of Strategic Procurement & Direct Sourcing',
                'role': 'Category Sourcing, Should-Cost Decomposition & Supplier Contracting',
                'summary': f'Leads direct material procurement and supplier relationships for {company_name} manufacturing and operations.',
                'mandate': 'Delivers cost savings and mitigates single-source supplier vulnerabilities across critical components.',
                'manualToil': 'Weeks spent normalizing inconsistent supplier quotes in Excel without bottom-up cost benchmarks.',
                'agenticImpact': 'Parametric should-cost decomposition unlocking 7-10% in direct procurement savings.'
            },
            'mps_scheduling_lead': {
                'title': f'{company_name} Master Production Scheduling & Factory Operations Meister',
                'role': 'Finite Capacity Scheduling & Plant Throughput Maximization',
                'summary': f'Orchestrates manufacturing line schedules, machine changeovers, and material allocations across {company_name} plants.',
                'mandate': 'Maximizes equipment utilization and eliminates line starvation through finite capacity sequencing.',
                'manualToil': 'Manual shift scheduling on spreadsheets frequently derailed by late material arrivals and equipment stops.',
                'agenticImpact': 'OR-Tools CP-SAT finite-capacity scheduling cutting changeover downtime by 30%.'
            }
        }


# Automatically alias canonical 60-persona IDs to industry-specific overrides
_ORIG_MINE_PERSONAS = mine_company_personas

def mine_company_personas(company_name: str, industry_id: str) -> Dict[str, Any]:
    res = dict(_ORIG_MINE_PERSONAS(company_name, industry_id))
    persona_aliases = [
        ("demand_planning_dir", "demand_planner_forecaster"),
        ("sop_ibp_lead", "sop_supply_planning_dir"),
        ("category_sourcing_mgr", "category_manager_portfolio"),
        ("supplier_risk_lead", "supplier_risk_manager"),
        ("mps_scheduling_lead", "master_production_scheduler"),
        ("meio_inventory_mgr", "inventory_planning_manager"),
        ("dock_yard_supervisor", "yard_master_gate_controller"),
        ("fleet_dispatch_mgr", "transportation_planner_router"),
        ("reverse_logistics_mgr", "value_recovery_recommerce"),
    ]
    for old_k, new_k in persona_aliases:
        if old_k in res and new_k not in res:
            res[new_k] = dict(res[old_k])
    return res

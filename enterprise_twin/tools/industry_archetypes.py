"""Industry Archetypes Baseline Knowledge Graph.

Provides high-fidelity supply chain domain models across global industries:
- Automotive & Mobility
- Energy, Oil & Gas / Petrochemicals
- Life Sciences, Pharma & BioTech
- Consumer Packaged Goods (CPG) & Food/Bev
- Retail & Omni-Channel E-Commerce
- Aerospace & Heavy Industrial Machinery
"""

INDUSTRY_ARCHETYPES = {
    'automotive': {
        'id': 'automotive',
        'displayName': 'Automotive, EV & Mobility',
        'executiveTitle': 'Board Member for Production, Logistics & Procurement',
        'executiveThesis': 'Synchronizing modular EV skateboard architectures, gigafactory battery cell flow, and tier-1 just-in-sequence (JIS) line feeding across global assembly plants.',
        'brandAccent': '#00d2ff',
        'brandSecondary': '#001e50',
        'defaultSystems': 'SAP S/4HANA for Automotive · Catena-X Automotive Data Space · Siemens Teamcenter PLM · Siemens Opcenter MES · Kuka Robotics SCADA · DB Cargo Automotive Rail · Wallenius Wilhelmsen RORO',
        'watermarkType': 'automotive_chassis',
        'productVocabulary': {
            'unit': 'vehicle / chassis',
            'subUnit': 'battery module / stamped component',
            'components': 'MEB battery cells, stamped body-in-white panels, drive inverters, wiring harnesses, braking actuators',
            'rawMaterials': 'stamping sheet coils, lithium cathode precursor, aluminum ingots, microcontrollers',
            'facilities': 'Gigafactory & Final Assembly Plant',
            'outboundMode': 'Enclosed Bi-Level Auto-Rack Rail & Ocean RORO Vessels',
            'inboundMode': 'Just-in-Sequence (JIS) Dedicated Shuttle Fleet & Intermodal Rail'
        },
        'personaOverrides': {
            'demand_planning_dir': {
                'title': 'Head of Global Vehicle Demand & Model Mix Planning',
                'mandate': 'Forecasts regional trim-level take rates, powertrain splits (BEV vs. PHEV vs. ICE), and dealer allocation curves.',
                'manualToil': 'Stitching monthly dealer portal orders in Excel, suffering 6-week blindspots on EV trim cancellation waves.',
                'agenticImpact': 'Daily regional VIN-level demand sensing in TimesFM balancing dealer pipeline and battery supply constraints.'
            },
            'sop_ibp_lead': {
                'title': 'VP of Global Vehicle S&OP & Allocation Consensus',
                'mandate': 'Balances global assembly line cycle times (Takt Time) against semiconductor and battery cell allocations.',
                'manualToil': '21-day consensus meetings arguing whether Wolfsburg or Chattanooga gets constrained inverter batches.',
                'agenticImpact': '45-minute live Pareto MILP consensus in OR-Tools balancing margin per vehicle against EU fleet CO2 targets.'
            },
            'mps_scheduling_lead': {
                'title': 'Production Control & Assembly Line Meister (MEB/Chassis)',
                'mandate': 'Sequences body shop, paint shop washdown, and final assembly lines to minimize color/trim changeover stops.',
                'manualToil': 'Manual whiteboards rescheduling lines when missing wire harnesses or paint defects stall final trim.',
                'agenticImpact': 'OR-Tools CP-SAT finite-capacity sequencing locking 100% material pegging 48h before body drop.'
            },
            'meio_inventory_mgr': {
                'title': 'Head of Assembly Plant Inbound Buffers & JIS Sequencing',
                'mandate': 'Controls component buffers across supplier logistics centers (SLC) and automated high-bay warehouses.',
                'manualToil': 'Hoarding 14 days of safety stock in expensive off-site trailer yards to prevent assembly line-stops.',
                'agenticImpact': 'Guaranteed-Service MEIO dynamically tuning JIS buffer stocks down to 4 hours of production.'
            },
            'fleet_dispatch_mgr': {
                'title': 'Outbound Vehicle Logistics & Dedicated Carrier Dispatch Lead',
                'mandate': 'Routes finished vehicle haulers (car carriers) and dedicated supplier milk-runs across plants and dealer hubs.',
                'manualToil': 'Dispatchers manually pairing cars to 9-car haulers with deadhead return miles and damaged bumpers.',
                'agenticImpact': 'Google Maps Corridor routing with 3D car-carrier spatial packing cutting empty miles by 24%.'
            },
            'global_trade_port_mgr': {
                'title': 'Director of Ocean Vehicle Terminals & RORO Logistics',
                'mandate': 'Manages vehicle processing centers (VPC), vessel charters, and port terminal dwell at major vehicle ports.',
                'manualToil': 'Vehicles idling in port tarmac lots for 18 days waiting for accessory installation and customs clearance.',
                'agenticImpact': 'Satellite AIS tracking and automated VPC accessory scheduling slashing port dwell by 45%.'
            }
        },
        'agentOverrides': {
            'demand_sensing_agent': {
                'name': 'VINPulse — Vehicle Configuration & Take-Rate Sensing Engine',
                'shortDesc': 'Fuses dealer showroom walk-ins, digital configurator clicks, and EV subsidy policy changes into daily trim-level P10/P50/P90 demand forecasts.',
                'badge': '+28% Trim Accuracy'
            },
            'line_schedule_optimizer': {
                'name': 'TaktMaster — Just-in-Sequence Assembly Line & Body-Drop Sequencer',
                'shortDesc': 'Sequences parallel paint shop colors and chassis body-drop lines to eliminate conveyor stalls and ensure JIS parts arrive within 90 seconds of vehicle marriage.',
                'badge': '-36% Line Stalls'
            },
            'tier_n_risk_sentinel': {
                'name': 'CatenaShield — Catena-X Sub-Tier Automotive Network Sentinel',
                'shortDesc': 'Maps Tier-1 (Bosch/Continental) to Tier-4 semiconductor fab and lithium refinery bottlenecks in Catena-X data space and Cloud Spanner Graph.',
                'badge': '+14 Days Warning'
            },
            'load_consolidation_agent': {
                'name': 'AutoCube 3D — Bi-Level Car-Hauler & Component Bay Packer',
                'shortDesc': 'Packs finished vehicles onto 9-car hydraulic haulers and components into standard GLT/KLT returnable totes with strict axle weight and roof clearance compliance.',
                'badge': '96% Hauler Fill'
            }
        }
    },

    'oil_gas_energy': {
        'id': 'oil_gas_energy',
        'displayName': 'Energy, Oil & Gas / Petrochemicals',
        'executiveTitle': 'EVP of Global Supply Chain, Trading & Logistics',
        'executiveThesis': 'Synchronizing upstream crude feeds, pipeline hydraulic schedules, refinery distillation slates, and global marine tanker charters.',
        'brandAccent': '#fbbf24',
        'brandSecondary': '#b91c1c',
        'defaultSystems': 'SAP S/4HANA Oil & Gas (IS-Oil) · AspenTech PIMS / HYSYS · OSIsoft PI / AVEVA Historian · Spire Ocean Tanker AIS · Genscape Pipeline Telemetry · AlloyDB · BigQuery GIS',
        'watermarkType': 'energy_pipeline',
        'productVocabulary': {
            'unit': 'barrel (bbl) / metric ton',
            'subUnit': 'cargo lot / pipeline batch',
            'components': 'distillate fuels, naphtha, ethylene, lubricants, LNG cargos, specialized catalysts',
            'rawMaterials': 'light sweet crude, sour heavy crude, natural gas liquids (NGL), drill pipe OCTG',
            'facilities': 'Refinery & Petrochemical Complex / Marine Tanker Terminal',
            'outboundMode': 'Product Pipelines, Jones Act Tankers & Unit Trains',
            'inboundMode': 'Crude Pipelines & VLCC Tanker Marine Terminals'
        },
        'personaOverrides': {
            'demand_planning_dir': {
                'title': 'Head of Commercial Offtake & Wholesale Fuels Demand',
                'mandate': 'Forecasts wholesale rack demand, jet fuel airport contracts, and regional marine bunker offtake.',
                'manualToil': 'Static monthly Excel reconciliations missing sudden weather-driven diesel or heating oil demand spikes.',
                'agenticImpact': 'Real-time weather and commercial aviation depletion models in BigQuery ML projecting daily wholesale demand.'
            },
            'mps_scheduling_lead': {
                'title': 'Refinery Hydrocracker & Catalytic Reformer Production Scheduler',
                'mandate': 'Sequences crude distillation unit (CDU) cut-points, tank blend recipes, and turnaround maintenance.',
                'manualToil': 'Linear programming runs taking 14 hours, forcing operators to run sub-optimal slates during crude assay shifts.',
                'agenticImpact': 'OR-Tools continuous non-linear blend optimizer generating optimal run slates in 3 minutes.'
            },
            'fleet_dispatch_mgr': {
                'title': 'Pipeline Batch Scheduler & Terminal Rack Dispatch Lead',
                'mandate': 'Schedules pipeline slug sequences, batch interfaces, and transport trucks at fuel distribution terminals.',
                'manualToil': 'Manual pipeline nominations with high interface transmix contamination and truck rack queuing.',
                'agenticImpact': 'Hydraulic pipeline sequencing coupled with Google Maps terminal appointment scheduling.'
            }
        },
        'agentOverrides': {
            'demand_sensing_agent': {
                'name': 'BarrelSense — Rack Offtake & Wholesale Energy Sensing Engine',
                'shortDesc': 'Fuses wholesale rack pulls, airport fuel offtake, maritime AIS bunker demands, and seasonal weather models into daily refinery crude pull plans.',
                'badge': '+26% Forecast Accuracy'
            },
            'line_schedule_optimizer': {
                'name': 'RefineOpt — Continuous Crude Assay & Blend Slate Optimizer',
                'shortDesc': 'Optimizes crude distillation unit cut-points and finished tank blending in real time to maximize crack spread margins under strict Reid Vapor Pressure (RVP) limits.',
                'badge': '+$0.82/bbl Margin'
            },
            'port_drayage_orchestrator': {
                'name': 'TankerWatch — Ocean VLCC / Product Tanker Berth & Demurrage Orchestrator',
                'shortDesc': 'Tracks global tanker fleets via satellite AIS, coordinates coastal lightering, and sequences deep-water refinery berths to slash $45,000/day tanker demurrage penalties.',
                'badge': '-72% Demurrage Fees'
            }
        }
    },

    'life_sciences_pharma': {
        'id': 'life_sciences_pharma',
        'displayName': 'Life Sciences, Pharmaceuticals & BioTech',
        'executiveTitle': 'Global Head of Technical Operations & Supply Chain',
        'executiveThesis': 'Ensuring zero-stockout patient delivery of temperature-sensitive biologics, active pharmaceutical ingredients (API), and cold-chain clinical therapies under strict cGMP.',
        'brandAccent': '#00d2ff',
        'brandSecondary': '#0d9488',
        'defaultSystems': 'SAP S/4HANA Life Sciences · Veeva Vault QMS · Siemens Opcenter Pharma MES · TrackWise · Sensitech Cold-Chain IoT · Cloud Spanner Graph · BigQuery',
        'watermarkType': 'pharma_biotech',
        'productVocabulary': {
            'unit': 'vial / pre-filled syringe / blister pack',
            'subUnit': 'bioreactor batch / clinical lot',
            'components': 'active pharmaceutical ingredient (API), excipients, sterile glass vials, elastomeric stoppers',
            'rawMaterials': 'cell culture media, single-use bioreactor bags, chromatography resins, chemical precursors',
            'facilities': 'Sterile Fill-Finish Plant & cGMP Biomanufacturing Facility',
            'outboundMode': 'Validated Temperature-Controlled Cold-Chain Air Cargo (2°C–8°C / -70°C)',
            'inboundMode': 'Qualified Temperature-Monitored Dedicated Dedicated Logistics'
        },
        'personaOverrides': {
            'demand_planning_dir': {
                'title': 'Director of Global Commercial Patient Demand & Tenders',
                'mandate': 'Forecasts hospital tenders, retail pharmacy dispenses, and epidemiology disease spread curves.',
                'manualToil': 'Managing tender volatility in static ERP sheets, risking lifesaving drug stockouts or expiring shelf life.',
                'agenticImpact': 'Epidemiological Bayesian sensing in TimesFM predicting disease surges 3 weeks ahead.'
            },
            'mps_scheduling_lead': {
                'title': 'Biomanufacturing Fermentation & Fill-Finish Scheduler',
                'mandate': 'Schedules living cell bioreactor runs, cleanroom sterilizations, and high-speed vial filling lines.',
                'manualToil': 'Rescheduling entire 18-day cell growth campaigns on paper when single-use bag supply delays occur.',
                'agenticImpact': 'OR-Tools CP-SAT bioreactor campaign scheduler synchronizing media prep, harvest, and freeze-thaw cycles.'
            },
            'freight_claims_analyst': {
                'title': 'Global Cold-Chain Quality & Thermal Deviation Specialist',
                'mandate': 'Audits cold-chain data loggers (-70°C to 8°C) across ocean reefers and air ULDs for cGMP release.',
                'manualToil': 'Manually reviewing hundreds of PDF temperature logger graphs to adjudicate product quarantine holds.',
                'agenticImpact': 'Instant thermal kinetic degradation analysis in Vertex AI releasing lots in 5 minutes.'
            }
        },
        'agentOverrides': {
            'demand_sensing_agent': {
                'name': 'RxDemand — Epidemiology & Hospital Tender Sensing Engine',
                'shortDesc': 'Fuses clinical prescription trends, institutional tender wins, and regional outbreak signals to project vial consumption curves.',
                'badge': '+32% Forecast Accuracy'
            },
            'inline_yield_guardian': {
                'name': 'BioBatch — cGMP Bioreactor Yield & Inline Quality Release Agent',
                'shortDesc': 'Monitors inline Raman spectroscopy and dissolved oxygen in bioreactors, predicting titer yield and automating electronic batch record (eBR) release.',
                'badge': '48h → 15m Batch Release'
            },
            'freight_control_tower': {
                'name': 'ColdSentinel — Validated Ultra-Cold In-Transit Thermal Guardian',
                'shortDesc': 'Streams live IoT temperature and dry-ice sublimation telemetry across air cargo ULDs, intercepting thermal excursions 90 minutes before stability breach.',
                'badge': '99.98% Cold-Chain Integrity'
            }
        }
    },

    'cpg_retail': {
        'id': 'cpg_retail',
        'displayName': 'Consumer Packaged Goods (CPG) & Retail',
        'executiveTitle': 'Chief Supply Chain Officer & EVP Customer Operations',
        'executiveThesis': 'Synchronizing retailer POS sell-through, high-velocity distribution centers, promotional price-shaping, and customer OTIF compliance.',
        'brandAccent': '#10b981',
        'brandSecondary': '#047857',
        'defaultSystems': 'SAP S/4HANA Consumer Goods · Blue Yonder TMS · Manhattan Active WMS · Walmart Luminate · Target Greenfield · BigQuery ML · Google Maps',
        'watermarkType': 'retail_pallet',
        'productVocabulary': {
            'unit': 'case / consumer SKU',
            'subUnit': 'shipper display / retail pallet',
            'components': 'corrugated cartons, closures, film labels, food ingredients, active beauty compounds',
            'rawMaterials': 'resin pellets, palm oil derivatives, sugar/flour commodities, aluminum cans',
            'facilities': 'Regional High-Velocity Distribution Center (CDC/RDC)',
            'outboundMode': 'Dedicated FTL & Multi-Stop Retail Corridor Fleet',
            'inboundMode': 'Intermodal Rail & Supplier Dry-Van Truckload'
        },
        'personaOverrides': {
            'demand_planning_dir': {
                'title': 'VP of Global Demand Sensing & Category Forecasting',
                'mandate': 'Forecasts store-level sell-through across big-box retailers, e-commerce, and direct-store delivery (DSD).',
                'manualToil': 'Reconciling 20 different retailer vendor portal spreadsheets with a 3-week lag.',
                'agenticImpact': 'Daily store scan harmonization in BigQuery ML predicting promotions and regional pantry stocking.'
            },
            'otif_customer_service_lead': {
                'title': 'Director of Customer Supply Chain & Retail OTIF Compliance',
                'mandate': 'Enforces 98%+ On-Time In-Full delivery to Walmart, Target, and Amazon to eliminate 3% chargeback fines.',
                'manualToil': 'Chasing truck drivers on cell phones and manually fighting retailer penalty chargebacks in spreadsheets.',
                'agenticImpact': '72-hour MABD breach prediction and automated Google Maps geofence dispute filing recovering $14M+.'
            }
        },
        'agentOverrides': {
            'demand_sensing_agent': {
                'name': 'ShelfPulse — Daily Retail POS & Channel Depletion Engine',
                'shortDesc': 'Harmonizes daily store register scans from Walmart Luminate, Target, and Amazon, detecting phantom out-of-stocks and projecting true consumer demand.',
                'badge': '-29% Shelf Stockouts'
            },
            'promo_lift_simulator': {
                'name': 'LiftOptimizer — Trade Promotion Elasticity & Supply Shaper',
                'shortDesc': 'Isolates true promotional lift from brand cannibalization in BigQuery ML and shapes trade promotions toward available warehouse inventory.',
                'badge': '+24% Trade ROI'
            },
            'otif_penalty_shield': {
                'name': 'OTIFShield — Retail Chargeback Recovery & MABD Rescuer',
                'shortDesc': 'Detects retailer MABD risks 72 hours early to re-route team trucks and auto-submits GPS geofence proof to overturn invalid retailer fines.',
                'badge': '-78% OTIF Fines'
            }
        }
    }
}

"""Company Profiler Tool.

Extracts corporate branding, official brand colors, vector logos,
executive supply chain leadership titles, flagship factories, core product lines,
and orchestrates the Persona and Agent Specification miners to produce a complete
enterprise digital twin. Integrates with the persistence layer.
"""

import re
from typing import Dict, Any, Optional

from enterprise_twin.tools.industry_archetypes import INDUSTRY_ARCHETYPES
from enterprise_twin.tools.career_persona_miner import mine_company_personas
from enterprise_twin.tools.agent_spec_miner import mine_company_agent_specs
from enterprise_twin.tools.ecosystem_miner import mine_company_ecosystem
from enterprise_twin.tools.persistence import load_twin, save_twin


KNOWN_COMPANIES: Dict[str, Dict[str, Any]] = {
    'volkswagen': {
        'canonicalName': 'Volkswagen Group',
        'ticker': 'XETRA: VOW3',
        'industryId': 'automotive',
        'brandAccent': '#00d2ff',
        'brandSecondary': '#001e50',
        'executiveTitle': 'Board Member for Production & Logistics, Volkswagen AG',
        'executiveThesis': 'Synchronizing Wolfsburg & global MEB gigafactories, battery cell supply from PowerCo & CATL, and just-in-sequence (JIS) line feeding for 9+ million vehicles.',
        'flagshipSites': 'Wolfsburg (Germany) · Zwickau MEB Gigafactory · Chattanooga (USA) · Bratislava · Port of Emden Vehicle Logistics Hub',
        'coreProducts': 'ID.4 & ID.7 Electric Skateboards · MEB Battery Pack Modules · Stamped Body-in-White Assemblies · TSI/TDI Powertrains',
        'logoSvg': '<svg viewBox="0 0 100 100" width="38" height="38" style="vertical-align:middle; margin-right:8px;"><circle cx="50" cy="50" r="46" fill="none" stroke="#00d2ff" stroke-width="6"/><circle cx="50" cy="50" r="40" fill="#001e50"/><path d="M26 35 L42 70 L50 50 L58 70 L74 35" fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><path d="M35 35 L50 64 L65 35" fill="none" stroke="#00d2ff" stroke-width="4" stroke-linecap="round"/></svg>'
    },
    'itc': {
        'canonicalName': 'ITC Limited',
        'ticker': 'NSE: ITC',
        'industryId': 'fmcg_agribusiness',
        'brandAccent': '#10b981',
        'brandSecondary': '#1e3a8a',
        'executiveTitle': 'Executive Director, FMCG, Agri-Business & Supply Chain, ITC Limited',
        'executiveThesis': 'Synchronizing India-wide FMCG manufacturing across 20+ ICMLs, e-Choupal direct farmer sourcing for wheat & spices, and multi-echelon Carrying & Forwarding distribution to 2M+ kirana retail stores.',
        'flagshipSites': 'Bengaluru Integrated Consumer Goods Manufacturing & Logistics Facility (ICML) · Tribeni Paperboards Complex · Bhadrachalam Mill · e-Choupal Rural Agri-Hubs',
        'coreProducts': 'Aashirvaad Atta & Spices · Sunfeast Biscuits · Bingo! Snacks · Yippee! Instant Noodles · Paperboards Packaging · Agri-Commodities',
        'logoSvg': '<svg viewBox="0 0 100 100" width="38" height="38" style="vertical-align:middle; margin-right:8px;"><polygon points="50,15 85,85 15,85" fill="#1e3a8a" stroke="#10b981" stroke-width="5"/><text x="50" y="70" fill="#ffffff" font-size="24" font-weight="900" text-anchor="middle" font-family="sans-serif">ITC</text></svg>'
    },
    'boeing': {
        'canonicalName': 'The Boeing Company',
        'ticker': 'NYSE: BA',
        'industryId': 'aerospace_defense',
        'brandAccent': '#0284c7',
        'brandSecondary': '#0f172a',
        'executiveTitle': 'Senior Vice President of Global Supply Chain & Manufacturing Operations, Boeing',
        'executiveThesis': 'Synchronizing multi-year supplier lead times, precision titanium forgings, FAA airworthiness compliance tracing, and final assembly lines for 737 and 787 aircraft programs.',
        'flagshipSites': 'Renton 737 Final Assembly Facility · North Charleston 787 Composite Hub · Everett Wide-Body Delivery Center · Boeing Defense St. Louis',
        'coreProducts': '737 MAX Commercial Jetliners · 787 Dreamliner Composite Fuselages · Titanium Wing Spar Forgings · Avionics & Flight Control Systems',
        'logoSvg': '<svg viewBox="0 0 100 100" width="38" height="38" style="vertical-align:middle; margin-right:8px;"><circle cx="50" cy="50" r="44" fill="#0f172a" stroke="#0284c7" stroke-width="5"/><path d="M22 65 C40 35 60 30 78 35 M30 50 L55 35 L70 50" fill="none" stroke="#38bdf8" stroke-width="5" stroke-linecap="round"/></svg>'
    },
    'caterpillar': {
        'canonicalName': 'Caterpillar Inc.',
        'ticker': 'NYSE: CAT',
        'industryId': 'heavy_machinery',
        'brandAccent': '#ffcd11',
        'brandSecondary': '#000000',
        'executiveTitle': 'Senior Vice President, Global Supply Chain & Customer Support Division, Caterpillar',
        'executiveThesis': 'Orchestrating heavy machinery assembly across 150+ global facilities, Cat Reman circular remanufacturing, and guaranteed 24-hour emergency dealer parts availability across 190 countries.',
        'flagshipSites': 'Peoria Heavy Equipment Operations (USA) · Decatur Mining Truck Facility · Aurora Wheel Loader Plant · Piracicaba Manufacturing Complex',
        'coreProducts': 'Cat Mining Excavators & Bulldozers · Diesel & Natural Gas Power Turbines · Cat Reman Recycled Engine Blocks · High-Strength Casting Undercarriages',
        'logoSvg': '<svg viewBox="0 0 100 100" width="38" height="38" style="vertical-align:middle; margin-right:8px;"><polygon points="50,15 88,80 12,80" fill="#ffcd11"/><polygon points="35,80 65,80 50,45" fill="#000000"/><text x="50" y="76" fill="#ffffff" font-size="16" font-weight="900" text-anchor="middle" font-family="sans-serif">CAT</text></svg>'
    },
    'shell': {
        'canonicalName': 'Shell plc',
        'ticker': 'NYSE: SHEL',
        'industryId': 'oil_gas_energy',
        'brandAccent': '#fbbf24',
        'brandSecondary': '#b91c1c',
        'executiveTitle': 'Executive Vice President of Global Supply Chain & Trading, Shell plc',
        'executiveThesis': 'Optimizing global integrated crude trading, pipeline hydraulic flows, Pernis refinery catalytic slates, and international LNG carrier charters.',
        'flagshipSites': 'Pernis Energy & Chemicals Park (Rotterdam) · Deer Park Complex · Singapore Pulau Bukom Hub · Port of Singapore Marine Terminal',
        'coreProducts': 'Crude Distillates & Low-Carbon Fuels · Liquefied Natural Gas (LNG) Cargos · Base Oils & Petrochemical Intermediates · Pipeline Batches',
        'logoSvg': '<svg viewBox="0 0 100 100" width="38" height="38" style="vertical-align:middle; margin-right:8px;"><path d="M50 12 C30 22 18 42 22 72 L32 88 L68 88 L78 72 C82 42 70 22 50 12 Z" fill="#fbbf24" stroke="#b91c1c" stroke-width="4"/><path d="M50 12 L50 88 M36 34 L40 88 M64 34 L60 88 M26 54 L32 88 M74 54 L68 88" stroke="#b91c1c" stroke-width="3" fill="none"/></svg>'
    },
    'pfizer': {
        'canonicalName': 'Pfizer Inc.',
        'ticker': 'NYSE: PFE',
        'industryId': 'life_sciences_pharma',
        'brandAccent': '#38bdf8',
        'brandSecondary': '#0000ff',
        'executiveTitle': 'President, Pfizer Global Supply (PGS) & Technical Operations',
        'executiveThesis': 'Guaranteed zero-stockout patient fulfillment of sterile injectables, mRNA vaccine platforms, and oncology APIs across 37 global manufacturing sites.',
        'flagshipSites': 'Kalamazoo Sterile Injectables Hub (USA) · Puurs Biomanufacturing Facility (Belgium) · Grange Castle (Ireland) · Freiburg Packaging Center',
        'coreProducts': 'mRNA Biologics & Vaccines · Sterile Injectable APIs · Lyophilized Vials · Solid Oral Dose Oncology Therapies',
        'logoSvg': '<svg viewBox="0 0 100 100" width="38" height="38" style="vertical-align:middle; margin-right:8px;"><ellipse cx="50" cy="50" rx="44" ry="34" fill="#0000ff"/><path d="M30 50 Q45 28 65 35 Q75 42 70 54 Q65 66 45 62 L32 60" fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/><circle cx="50" cy="50" r="4" fill="#00d2ff"/></svg>'
    },
    'unilever': {
        'canonicalName': 'Unilever PLC',
        'ticker': 'NYSE: UL',
        'industryId': 'cpg_retail',
        'brandAccent': '#10b981',
        'brandSecondary': '#1e3a8a',
        'executiveTitle': 'Chief Supply Chain Officer, Unilever',
        'executiveThesis': 'Synchronizing 400+ consumer brands across 280 factories and 500+ distribution centers with real-time retailer POS sensing and zero-deforestation sourcing.',
        'flagshipSites': 'Port Sunlight Innovation & Production Center · Indaiatuba Mega-DC · Dubai Personal Care Hub · Rotterdam Logistics Center',
        'coreProducts': 'Personal Care & Beauty SKUs · Home Hygiene Formulations · Food & Refreshment Pallet Displays · DSD Corrugated Cases',
        'logoSvg': '<svg viewBox="0 0 100 100" width="38" height="38" style="vertical-align:middle; margin-right:8px;"><path d="M28 20 C22 45 28 80 50 82 C72 80 78 45 72 20 C64 40 58 55 50 55 C42 55 36 40 28 20 Z" fill="none" stroke="#1e3a8a" stroke-width="6"/><circle cx="50" cy="35" r="8" fill="#10b981"/></svg>'
    }
}


def profile_company(company_name: str, industry_hint: Optional[str] = None) -> Dict[str, Any]:
    """Profiles a target company, matching it to known enterprise profiles or synthesizing from industry archetypes."""
    # First, check memory/disk persistence
    cached = load_twin(company_name)
    if cached:
        return cached

    clean_name = re.sub(r'[^a-zA-Z0-9]', '', company_name.lower())

    ind_map = {
        'fmcg_agribusiness': 'cpg_retail',
        'cpg_retail': 'cpg_retail',
        'aerospace_defense': 'automotive',
        'heavy_machinery': 'automotive',
        'automotive': 'automotive',
        'oil_gas_energy': 'oil_gas_energy',
        'life_sciences_pharma': 'life_sciences_pharma',
    }

    # Direct match in known enterprise catalog
    for key, data in KNOWN_COMPANIES.items():
        if key in clean_name or clean_name in key:
            arch_key = ind_map.get(data['industryId'], 'automotive')
            arch = INDUSTRY_ARCHETYPES.get(arch_key, INDUSTRY_ARCHETYPES['automotive'])
            merged = dict(arch)
            merged.update(data)
            merged['id'] = key
            merged['displayName'] = data['canonicalName']
            merged['company_slug'] = key
            merged['ecosystem'] = mine_company_ecosystem(merged['canonicalName'], merged['industryId'])
            merged['personaOverrides'] = mine_company_personas(merged['canonicalName'], merged['industryId'])
            merged['agentOverrides'] = mine_company_agent_specs(merged['canonicalName'], merged['industryId'])
            save_twin(merged)
            return merged

    # Fuzzy match on industry hint
    target_ind = 'automotive'
    if industry_hint:
        hint_lower = industry_hint.lower()
        if any(w in hint_lower for w in ['fmcg', 'agri', 'choupal', 'food', 'consum', 'grocer', 'retail', 'cpg']):
            target_ind = 'cpg_retail'
        elif any(w in hint_lower for w in ['aero', 'plane', 'boeing', 'airbus', 'defense', 'flight']):
            target_ind = 'aerospace'
        elif any(w in hint_lower for w in ['machin', 'caterpillar', 'deere', 'komatsu', 'mining', 'heavy']):
            target_ind = 'aerospace'
        elif any(w in hint_lower for w in ['oil', 'gas', 'energy', 'petro', 'refin', 'pipeline']):
            target_ind = 'oil_gas_energy'
        elif any(w in hint_lower for w in ['pharma', 'health', 'bio', 'life', 'drug', 'medic']):
            target_ind = 'life_sciences_pharma'

    arch = INDUSTRY_ARCHETYPES.get(target_ind, INDUSTRY_ARCHETYPES['automotive'])
    ecosystem = mine_company_ecosystem(company_name, target_ind)
    mined_personas = mine_company_personas(company_name, target_ind)
    mined_agents = mine_company_agent_specs(company_name, target_ind)

    profile = {
        'id': re.sub(r'[^a-zA-Z0-9]', '_', company_name.lower()),
        'displayName': company_name,
        'company_name': company_name,
        'canonicalName': company_name,
        'ticker': f'GLOBAL: {company_name[:4].upper()}',
        'industryId': target_ind,
        'brandAccent': arch['brandAccent'],
        'brandSecondary': arch['brandSecondary'],
        'executiveTitle': f"{arch['executiveTitle']}, {company_name}",
        'executiveThesis': f"Empowering {company_name} with autonomous supply chain agents across {arch['productVocabulary']['facilities'].lower()} and global distribution corridors.",
        'flagshipSites': f"{company_name} Global Hub 01 · Regional Manufacturing Center · Central Logistics Complex",
        'coreProducts': arch['productVocabulary']['components'],
        'logoSvg': f'<svg viewBox="0 0 100 100" width="38" height="38" style="vertical-align:middle; margin-right:8px;"><circle cx="50" cy="50" r="45" fill="{arch["brandSecondary"]}" stroke="{arch["brandAccent"]}" stroke-width="4"/><text x="50" y="58" fill="#ffffff" font-size="26" font-weight="800" text-anchor="middle" font-family="sans-serif">{company_name[:2].upper()}</text></svg>',
        'productVocabulary': arch['productVocabulary'],
        'defaultSystems': arch['defaultSystems'],
        'watermarkType': arch['watermarkType'],
        'personaOverrides': mined_personas,
        'agentOverrides': mined_agents,
        'ecosystem': ecosystem
    }

    save_twin(profile)
    return profile

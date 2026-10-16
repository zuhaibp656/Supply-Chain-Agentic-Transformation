"""Company Profiler Tool.

Extracts corporate branding, official brand colors, vector logos,
executive supply chain leadership titles, flagship factories, and core product lines.
"""

import re
from typing import Dict, Any, Optional
from enterprise_twin.tools.industry_archetypes import INDUSTRY_ARCHETYPES

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
        'logoSvg': '<svg viewBox="0 0 100 100" width="40" height="40" style="vertical-align:middle; margin-right:8px;"><circle cx="50" cy="50" r="46" fill="none" stroke="#00d2ff" stroke-width="6"/><circle cx="50" cy="50" r="40" fill="#001e50"/><path d="M26 35 L42 70 L50 50 L58 70 L74 35" fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><path d="M35 35 L50 64 L65 35" fill="none" stroke="#00d2ff" stroke-width="4" stroke-linecap="round"/></svg>'
    },
    'shell': {
        'canonicalName': 'Shell plc',
        'ticker': 'NYSE: SHEL',
        'industryId': 'oil_gas_energy',
        'brandAccent': '#fbbf24',
        'brandSecondary': '#b91c1c',
        'executiveTitle': 'Executive Vice President of Global Supply Chain & Trading',
        'executiveThesis': 'Optimizing global integrated crude trading, pipeline hydraulic flows, Pernis refinery catalytic slates, and international LNG carrier charters.',
        'flagshipSites': 'Pernis Energy & Chemicals Park (Rotterdam) · Deer Park Complex · Singapore Pulau Bukom Hub · Port of Singapore Marine Terminal',
        'coreProducts': 'Crude Distillates & Low-Carbon Fuels · Liquefied Natural Gas (LNG) Cargos · Base Oils & Petrochemical Intermediates · Pipeline Batches',
        'logoSvg': '<svg viewBox="0 0 100 100" width="40" height="40" style="vertical-align:middle; margin-right:8px;"><path d="M50 12 C30 22 18 42 22 72 L32 88 L68 88 L78 72 C82 42 70 22 50 12 Z" fill="#fbbf24" stroke="#b91c1c" stroke-width="4"/><path d="M50 12 L50 88 M36 34 L40 88 M64 34 L60 88 M26 54 L32 88 M74 54 L68 88" stroke="#b91c1c" stroke-width="3" fill="none"/></svg>'
    },
    'pfizer': {
        'canonicalName': 'Pfizer Inc.',
        'ticker': 'NYSE: PFE',
        'industryId': 'life_sciences_pharma',
        'brandAccent': '#00d2ff',
        'brandSecondary': '#0000ff',
        'executiveTitle': 'President, Pfizer Global Supply (PGS) & Technical Operations',
        'executiveThesis': 'Guaranteed zero-stockout patient fulfillment of sterile injectables, mRNA vaccine platforms, and oncology APIs across 37 global manufacturing sites.',
        'flagshipSites': 'Kalamazoo Sterile Injectables Hub (USA) · Puurs Biomanufacturing Facility (Belgium) · Grange Castle (Ireland) · Freiburg Packaging Center',
        'coreProducts': 'mRNA Biologics & Vaccines · Sterile Injectable APIs · Lyophilized Vials · Solid Oral Dose Oncology Therapies',
        'logoSvg': '<svg viewBox="0 0 100 100" width="40" height="40" style="vertical-align:middle; margin-right:8px;"><ellipse cx="50" cy="50" rx="44" ry="34" fill="#0000ff"/><path d="M30 50 Q45 28 65 35 Q75 42 70 54 Q65 66 45 62 L32 60" fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/><circle cx="50" cy="50" r="4" fill="#00d2ff"/></svg>'
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
        'logoSvg': '<svg viewBox="0 0 100 100" width="40" height="40" style="vertical-align:middle; margin-right:8px;"><path d="M28 20 C22 45 28 80 50 82 C72 80 78 45 72 20 C64 40 58 55 50 55 C42 55 36 40 28 20 Z" fill="none" stroke="#1e3a8a" stroke-width="6"/><circle cx="50" cy="35" r="8" fill="#10b981"/></svg>'
    }
}


from enterprise_twin.tools.career_persona_miner import mine_company_personas
from enterprise_twin.tools.ecosystem_miner import mine_company_ecosystem

def profile_company(company_name: str, industry_hint: Optional[str] = None) -> Dict[str, Any]:
    """Profiles a target company, matching it to known enterprise profiles or synthesizing from industry archetypes."""
    clean_name = re.sub(r'[^a-zA-Z0-9]', '', company_name.lower())
    
    # Direct match in known enterprise catalog
    for key, data in KNOWN_COMPANIES.items():
        if key in clean_name or clean_name in key:
            arch = INDUSTRY_ARCHETYPES.get(data['industryId'], INDUSTRY_ARCHETYPES['automotive'])
            merged = dict(arch)
            merged.update(data)
            # Enrich with mined ecosystem & personas
            merged['ecosystem'] = mine_company_ecosystem(merged['canonicalName'], merged['industryId'])
            mined_p = mine_company_personas(merged['canonicalName'], merged['industryId'])
            if 'personaOverrides' in merged:
                merged['personaOverrides'].update(mined_p)
            else:
                merged['personaOverrides'] = mined_p
            return merged
            
    # Fuzzy match on industry hint
    target_ind = 'automotive'
    if industry_hint:
        hint_lower = industry_hint.lower()
        if any(w in hint_lower for w in ['oil', 'gas', 'energy', 'petro', 'refin']):
            target_ind = 'oil_gas_energy'
        elif any(w in hint_lower for w in ['pharma', 'health', 'bio', 'life', 'drug', 'medic']):
            target_ind = 'life_sciences_pharma'
        elif any(w in hint_lower for w in ['cpg', 'retail', 'food', 'consum', 'grocer']):
            target_ind = 'cpg_retail'
            
    arch = INDUSTRY_ARCHETYPES[target_ind]
    ecosystem = mine_company_ecosystem(company_name, target_ind)
    mined_personas = mine_company_personas(company_name, target_ind)
    
    # Synthesize custom profile for unknown company
    combined_personas = dict(arch.get('personaOverrides', {}))
    combined_personas.update(mined_personas)

    return {
        'canonicalName': company_name,
        'ticker': f'GLOBAL: {company_name[:4].upper()}',
        'industryId': target_ind,
        'brandAccent': arch['brandAccent'],
        'brandSecondary': arch['brandSecondary'],
        'executiveTitle': f"{arch['executiveTitle']}, {company_name}",
        'executiveThesis': f"Empowering {company_name} with autonomous supply chain agents across {arch['productVocabulary']['facilities'].lower()} and global distribution corridors.",
        'flagshipSites': f"{company_name} Global Hub 01 · Regional Manufacturing Center · Central Logistics Complex",
        'coreProducts': arch['productVocabulary']['components'],
        'logoSvg': f'<svg viewBox="0 0 100 100" width="36" height="36" style="vertical-align:middle; margin-right:8px;"><circle cx="50" cy="50" r="45" fill="{arch["brandSecondary"]}" stroke="{arch["brandAccent"]}" stroke-width="4"/><text x="50" y="58" fill="#ffffff" font-size="28" font-weight="800" text-anchor="middle" font-family="sans-serif">{company_name[:2].upper()}</text></svg>',
        'productVocabulary': arch['productVocabulary'],
        'defaultSystems': arch['defaultSystems'],
        'watermarkType': arch['watermarkType'],
        'personaOverrides': combined_personas,
        'agentOverrides': arch['agentOverrides'],
        'ecosystem': ecosystem
    }


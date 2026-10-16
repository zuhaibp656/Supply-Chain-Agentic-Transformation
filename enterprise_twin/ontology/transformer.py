"""Ontology Transformer.

Transforms the base industry-agnostic SCOR framework HTML and data structures
into a bespoke enterprise client twin based on the researched company profile.
"""

import re
from typing import Dict, Any
from enterprise_twin.generator.visual_styler import generate_industry_watermark_svg

def transform_html_for_company(base_html: str, profile: Dict[str, Any]) -> str:
    """Transforms base HTML string into a client-tailored enterprise portal."""
    c_name = profile['canonicalName']
    exec_title = profile['executiveTitle']
    exec_thesis = profile['executiveThesis']
    logo_svg = profile.get('logoSvg', '')
    brand_accent = profile.get('brandAccent', '#00d2ff')
    brand_sec = profile.get('brandSecondary', '#001e50')
    watermark_type = profile.get('watermarkType', 'automotive_chassis')
    
    html = base_html

    # 1. Update Title and Meta
    html = html.replace(
        '<title>Gemini Enterprise — Supply Chain &amp; Demand (Office of the CSCO)</title>',
        f'<title>Gemini Enterprise — {c_name} Supply Chain Transformation ({exec_title})</title>'
    )

    # 2. Inject Brand Badge & Logo in Top Navbar
    brand_badge_html = f'''
        <div style="display:inline-flex; align-items:center; gap:8px; margin-left:14px; padding:4px 12px; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.14); border-radius:100px;">
          {logo_svg}
          <span style="font-family:var(--font-display); font-size:13.5px; font-weight:800; color:#ffffff; letter-spacing:-0.01em;">{c_name}</span>
          <span style="font-size:11px; font-weight:700; color:{brand_accent}; background:{brand_accent}22; padding:2px 7px; border-radius:10px;">Enterprise Twin</span>
        </div>
    '''
    target_nav_lockup = '<span class="logo-text">Gemini Enterprise</span>'
    if target_nav_lockup in html:
        html = html.replace(target_nav_lockup, target_nav_lockup + brand_badge_html)

    # 3. Update Hero Title & Thesis
    html = html.replace(
        'Supply Chain &amp; Demand Agentic Transformation',
        f'{c_name} Supply Chain Agentic Transformation'
    )
    
    # 4. Update CSCO Root Card on the Org Chart
    html = html.replace(
        'Chief Supply Chain Officer (CSCO)',
        exec_title
    )
    html = html.replace(
        'Office of the CSCO · Global Supply Chain Leadership',
        f'{c_name} Global Production, Supply Chain & Logistics Leadership'
    )
    html = html.replace(
        'The Office of the CSCO operates 6 SCOR-aligned departments',
        f'{c_name} operates 6 SCOR-aligned operational verticals across {profile.get("flagshipSites", "global manufacturing hubs")}'
    )

    # 5. Apply Persona Overrides
    persona_overrides = profile.get('personaOverrides', {})
    for pid, pdata in persona_overrides.items():
        if 'title' in pdata:
            # We replace specific persona names in the JS constants
            # In build_site.py: name: 'Demand Planning Director'
            pass

    # 6. Apply Agent Overrides
    agent_overrides = profile.get('agentOverrides', {})
    for aid, adata in agent_overrides.items():
        if 'name' in adata:
            # Replace agent names
            pass

    # 7. Inject Dynamic Brand CSS Variables
    custom_css = f'''
      /* Enterprise Twin Brand Overrides for {c_name} */
      :root {{
        --brand-accent: {brand_accent};
        --brand-secondary: {brand_sec};
        --sc-cyan: {brand_accent};
      }}
      .hero-title .g-text-gradient {{
        background: linear-gradient(135deg, #ffffff 0%, {brand_accent} 50%, #a142f4 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
      }}
    '''
    html = html.replace('</style>', f'{custom_css}\n  </style>')

    return html

"""Visual Styler & Industry Vector Generator.

Generates industry-specific SVG watermarks, dynamic brand color themes,
and technical CAD visual elements for client-tailored portals.
"""

def generate_industry_watermark_svg(watermark_type: str, color: str, extra_class: str = '') -> str:
    """Generates an authentic, high-contrast industry SVG watermark."""
    if watermark_type == 'automotive_chassis':
        return f'''
        <svg class="dept-watermark {extra_class}" viewBox="0 0 460 300" fill="none" xmlns="http://www.w3.org/2000/svg">
          <!-- Modular EV Skateboard Chassis & Powertrain Blueprint -->
          <rect x="60" y="80" width="340" height="140" rx="20" stroke="{color}" stroke-width="2.5" stroke-dasharray="6 4" opacity="0.65" />
          <!-- Battery Pack Cells Matrix -->
          <rect x="110" y="105" width="240" height="90" rx="10" stroke="{color}" stroke-width="2" fill="{color}" fill-opacity="0.08" />
          <line x1="170" y1="105" x2="170" y2="195" stroke="{color}" stroke-width="1.5" stroke-dasharray="4 3" opacity="0.5" />
          <line x1="230" y1="105" x2="230" y2="195" stroke="{color}" stroke-width="1.5" stroke-dasharray="4 3" opacity="0.5" />
          <line x1="290" y1="105" x2="290" y2="195" stroke="{color}" stroke-width="1.5" stroke-dasharray="4 3" opacity="0.5" />
          <!-- Front & Rear Axles + Wheels -->
          <rect x="40" y="50" width="36" height="60" rx="8" fill="{color}" fill-opacity="0.25" stroke="{color}" stroke-width="2" />
          <rect x="40" y="190" width="36" height="60" rx="8" fill="{color}" fill-opacity="0.25" stroke="{color}" stroke-width="2" />
          <rect x="384" y="50" width="36" height="60" rx="8" fill="{color}" fill-opacity="0.25" stroke="{color}" stroke-width="2" />
          <rect x="384" y="190" width="36" height="60" rx="8" fill="{color}" fill-opacity="0.25" stroke="{color}" stroke-width="2" />
          <line x1="58" y1="80" x2="58" y2="220" stroke="{color}" stroke-width="3" />
          <line x1="402" y1="80" x2="402" y2="220" stroke="{color}" stroke-width="3" />
          <!-- Steering & Drive Motors -->
          <circle cx="90" cy="150" r="16" stroke="{color}" stroke-width="2" fill="{color}" fill-opacity="0.2" />
          <circle cx="370" cy="150" r="20" stroke="{color}" stroke-width="2.5" fill="{color}" fill-opacity="0.3" />
          <!-- Telemetry Scan Laser -->
          <line x1="20" y1="150" x2="440" y2="150" stroke="{color}" stroke-width="1" stroke-dasharray="8 6" opacity="0.4" />
        </svg>
        '''
    elif watermark_type == 'energy_pipeline':
        return f'''
        <svg class="dept-watermark {extra_class}" viewBox="0 0 460 300" fill="none" xmlns="http://www.w3.org/2000/svg">
          <!-- Refinery Distillation Column & Catalytic Cracker -->
          <rect x="70" y="40" width="70" height="220" rx="12" stroke="{color}" stroke-width="2.5" fill="{color}" fill-opacity="0.08" />
          <line x1="70" y1="90" x2="140" y2="90" stroke="{color}" stroke-width="1.5" />
          <line x1="70" y1="140" x2="140" y2="140" stroke="{color}" stroke-width="1.5" />
          <line x1="70" y1="190" x2="140" y2="190" stroke="{color}" stroke-width="1.5" />
          <path d="M70 40 Q105 18 140 40" stroke="{color}" stroke-width="2.5" fill="none" />
          <!-- Storage Spheres / Bullet Tanks -->
          <circle cx="230" cy="180" r="50" stroke="{color}" stroke-width="2" fill="{color}" fill-opacity="0.08" />
          <rect x="320" y="130" width="90" height="130" rx="10" stroke="{color}" stroke-width="2" fill="{color}" fill-opacity="0.08" />
          <!-- Interconnecting Pipeline Flow -->
          <path d="M140 115 L230 115 L230 130" stroke="{color}" stroke-width="3" fill="none" />
          <path d="M280 180 L320 180" stroke="{color}" stroke-width="3" fill="none" />
          <path d="M410 195 L450 195" stroke="{color}" stroke-width="3" stroke-dasharray="6 4" fill="none" />
        </svg>
        '''
    elif watermark_type == 'pharma_biotech':
        return f'''
        <svg class="dept-watermark {extra_class}" viewBox="0 0 460 300" fill="none" xmlns="http://www.w3.org/2000/svg">
          <!-- cGMP Bioreactor Stainless Vessel -->
          <rect x="80" y="50" width="110" height="180" rx="20" stroke="{color}" stroke-width="2.5" fill="{color}" fill-opacity="0.08" />
          <line x1="135" y1="20" x2="135" y2="180" stroke="{color}" stroke-width="2.5" />
          <circle cx="135" cy="120" r="30" stroke="{color}" stroke-width="1.5" stroke-dasharray="4 4" />
          <!-- Sterile Vial Fill Line -->
          <path d="M190 190 L390 190" stroke="{color}" stroke-width="3" />
          ${"".join([f'<rect x="{220 + i*40}" y="155" width="22" height="35" rx="5" stroke="{color}" stroke-width="1.8" fill="{color}" fill-opacity="0.2"/>' for i in range(4)])}
          <!-- Temperature Stability Shield -->
          <path d="M340 50 L380 70 L380 110 L340 130 L300 110 L300 70 Z" stroke="{color}" stroke-width="2" fill="{color}" fill-opacity="0.1" />
          <text x="340" y="95" fill="{color}" font-size="12" font-weight="700" text-anchor="middle">-70°C</text>
        </svg>
        '''
    else:
        # Default retail / general supply chain
        return f'''
        <svg class="dept-watermark {extra_class}" viewBox="0 0 460 300" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="70" y="60" width="320" height="180" rx="14" stroke="{color}" stroke-width="2" stroke-dasharray="8 6" opacity="0.5" />
          <rect x="100" y="100" width="70" height="90" rx="8" stroke="{color}" stroke-width="1.8" fill="{color}" fill-opacity="0.12" />
          <rect x="190" y="100" width="70" height="90" rx="8" stroke="{color}" stroke-width="1.8" fill="{color}" fill-opacity="0.12" />
          <rect x="280" y="100" width="70" height="90" rx="8" stroke="{color}" stroke-width="1.8" fill="{color}" fill-opacity="0.12" />
        </svg>
        '''

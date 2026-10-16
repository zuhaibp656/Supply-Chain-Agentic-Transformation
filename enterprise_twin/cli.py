"""Enterprise Twin CLI.

Command line interface to profile an enterprise and generate a customized
supply chain transformation portal on demand.

Usage:
  python3 -m enterprise_twin.cli --company "Volkswagen" --industry "Automotive"
  python3 -m enterprise_twin.cli --company "Shell" --industry "Energy"
  python3 -m enterprise_twin.cli --company "Pfizer" --industry "Pharma"
"""

import argparse
import sys
from enterprise_twin.tools.company_profiler import profile_company
from enterprise_twin.generator.html_compiler import compile_enterprise_twin

def main():
    parser = argparse.ArgumentParser(description="Autonomous Enterprise Twin Generator")
    parser.add_argument("--company", "-c", required=True, help="Target company name (e.g. 'Volkswagen Group', 'Shell', 'Pfizer')")
    parser.add_argument("--industry", "-i", default=None, help="Industry or sector hint (e.g. 'Automotive', 'Oil & Gas', 'Life Sciences')")
    parser.add_argument("--slug", "-s", default=None, help="Custom output directory slug")

    args = parser.parse_args()

    print("\n" + "="*70)
    print(f"🚀 AUTONOMOUS ENTERPRISE TWIN AGENT: {args.company.upper()}")
    print("="*70)
    
    print("\n[Stage 1/3] 🔍 Researching & profiling enterprise identity...")
    profile = profile_company(args.company, args.industry)
    print(f"   • Canonical Entity: {profile['canonicalName']} ({profile.get('ticker', 'N/A')})")
    print(f"   • Sector / Archetype: {profile['industryId']}")
    print(f"   • Executive Leadership: {profile['executiveTitle']}")
    print(f"   • Brand Palette: Accent {profile['brandAccent']} · Secondary {profile['brandSecondary']}")
    print(f"   • Primary Sites: {profile.get('flagshipSites', 'Global Hubs')}")
    print(f"   • Systems: {profile.get('defaultSystems', 'SAP S/4HANA')}")

    print("\n[Stage 2/3] 🧬 Adapting 6 SCOR Verticals, 26 Personas & 32 AI Agents...")
    print(f"   • Injected {len(profile.get('personaOverrides', {}))} specialized role mappings")
    print(f"   • Grounded mathematical solvers in {profile['productVocabulary']['unit']} nomenclature")

    print("\n[Stage 3/3] 🏗️ Compiling bespoke 60fps interactive portal & Zipline bundle...")
    out_dir = compile_enterprise_twin(profile, args.slug)

    print("\n" + "="*70)
    print("✨ GENERATION COMPLETE!")
    print(f"📁 Output Directory: {out_dir}")
    print(f"🌐 Main Portal: {out_dir / 'index.html'}")
    print(f"🧪 Periodic Table: {out_dir / 'periodic_table.html'}")
    print(f"🧠 Mind Map: {out_dir / 'mind_map.html'}")
    slug = out_dir.name
    print(f"📦 Zipline Bundle: {out_dir / f'{slug}_zipline_bundle.zip'}")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()

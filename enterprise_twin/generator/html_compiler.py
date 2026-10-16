"""HTML Compiler & Client Asset Packager.

Compiles customized HTML portals and assembles Zipline zip bundles for target enterprises.
"""

import os
import re
import sys
import zipfile
import pathlib
from typing import Dict, Any

from enterprise_twin.ontology.transformer import transform_html_for_company

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
DIST_DIR = ROOT_DIR / "dist"

def compile_enterprise_twin(profile: Dict[str, Any], output_slug: str = None) -> pathlib.Path:
    """Compiles the customized portal for the given enterprise profile."""
    # Import build_html from root build_site
    sys.path.insert(0, str(ROOT_DIR))
    from build_site import build_html

    c_name = profile['canonicalName']
    slug = output_slug or re.sub(r'[^a-z0-9]+', '_', c_name.lower()).strip('_')
    out_dir = DIST_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Generate customized index.html
    base_html = build_html()
    custom_html = transform_html_for_company(base_html, profile)
    
    index_file = out_dir / "index.html"
    index_file.write_text(custom_html, encoding="utf-8")

    # 2. Generate periodic_table.html
    pt_html = custom_html.replace(
        "window.addEventListener('DOMContentLoaded', () => {",
        "window.addEventListener('DOMContentLoaded', () => {\n      openPeriodicTablePage('all', null, false);"
    )
    pt_file = out_dir / "periodic_table.html"
    pt_file.write_text(pt_html, encoding="utf-8")

    # 3. Generate mind_map.html
    mm_html = custom_html.replace(
        "window.addEventListener('DOMContentLoaded', () => {",
        "window.addEventListener('DOMContentLoaded', () => {\n      openMindMapPage('mindmap', null, null, false);"
    )
    mm_file = out_dir / "mind_map.html"
    mm_file.write_text(mm_html, encoding="utf-8")

    # 4. Copy videos if available
    videos_src = ROOT_DIR / "videos"
    videos_dst = out_dir / "videos"
    if videos_src.exists():
        videos_dst.mkdir(exist_ok=True)
        for v in videos_src.glob("*.mp4"):
            dst_v = videos_dst / v.name
            if not dst_v.exists():
                dst_v.write_bytes(v.read_bytes())

    # 5. Build Zipline ZIP bundle
    zip_path = out_dir / f"{slug}_zipline_bundle.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in [index_file, pt_file, mm_file]:
            zf.write(f, arcname=f.name)
        if videos_dst.exists():
            for v in videos_dst.glob("*.mp4"):
                zf.write(v, arcname=f"videos/{v.name}")

    print(f"✅ Successfully compiled Enterprise Twin for '{c_name}' -> {out_dir}")
    print(f"   - index.html ({index_file.stat().st_size // 1024} KB)")
    print(f"   - periodic_table.html ({pt_file.stat().st_size // 1024} KB)")
    print(f"   - mind_map.html ({mm_file.stat().st_size // 1024} KB)")
    print(f"   - Zipline Bundle: {zip_path} ({zip_path.stat().st_size // 1024} KB)")
    
    return out_dir

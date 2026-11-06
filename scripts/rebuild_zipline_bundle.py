#!/usr/bin/env python3
"""Rebuild supply chain zipline bundles from zipline_dist."""
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT / "zipline_dist"

ZIP_TARGETS = [
    ROOT / "supply_chain_zipline_bundle.zip",
    ROOT / "Supply_Chain_Agentic_Portal.zip",
    ROOT / "Zipline_Supply_Chain_Agentic_Portal.zip",
    ROOT / "zipline" / "supply_chain_zipline_bundle.zip",
    ROOT / "zipline" / "supply_chain_zipline_folder_bundle.zip",
    ROOT / "zipline" / "supply_chain_zipline_light.zip",
]

def main():
    print(f"Refreshing zipline bundles from {DIST_DIR}...")
    for zpath in ZIP_TARGETS:
        zpath.parent.mkdir(parents=True, exist_ok=True)
        wrap_folder = "zipline_dist" if "folder_bundle" in zpath.name else ""
        print(f"Packaging {zpath.name} (wrap='{wrap_folder}')...")
        with zipfile.ZipFile(zpath, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for item in sorted(DIST_DIR.rglob("*")):
                if item.is_file():
                    arcname = item.relative_to(DIST_DIR).as_posix()
                    if wrap_folder:
                        arcname = f"{wrap_folder}/{arcname}"
                    zf.write(item, arcname)
        size_mb = zpath.stat().st_size / (1024 * 1024)
        print(f"  -> {zpath} ({size_mb:.2f} MB)")
    print("Done refreshing all zipline bundles!")

if __name__ == "__main__":
    main()

from pathlib import Path

ROOT = Path("agents")
for p in ROOT.glob("*/app/tools.py"):
    txt = p.read_text(encoding="utf-8")
    if "from __future__ import annotations" in txt:
        # If _LATEST_INTERACTIVE_HTML appears before from __future__ import annotations, swap them
        parts = txt.split("from __future__ import annotations")
        if len(parts) == 2 and "_LATEST_INTERACTIVE_HTML" in parts[0]:
            before = parts[0]
            after = parts[1]
            # remove _LATEST_INTERACTIVE_HTML definition from before
            sub_parts = before.split("_LATEST_INTERACTIVE_HTML")
            clean_before = sub_parts[0]
            # find end of getter function in before
            rest_before = ""
            if "def get_latest_interactive_html" in before:
                idx = before.find("def get_latest_interactive_html")
                end_idx = before.find("return res\n", idx)
                if end_idx != -1:
                    clean_before = before[:before.find("_LATEST_INTERACTIVE_HTML:")]
                    getter_code = before[before.find("_LATEST_INTERACTIVE_HTML:"):end_idx + len("return res\n")]
                    new_txt = "from __future__ import annotations\n" + getter_code + "\n" + clean_before + after
                    p.write_text(new_txt, encoding="utf-8")
                    print(f"Fixed future import in {p}")

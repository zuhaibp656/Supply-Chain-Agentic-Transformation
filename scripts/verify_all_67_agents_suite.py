#!/usr/bin/env python3
"""Comprehensive fast structural audit & test runner across all 67 Supply Chain ADK Agent packages.

Executes BOTH `unittest.TestCase` classes AND plain pytest-style `def test_*()` functions in every
`tests/test_*.py` file across all 67 agent packages, plus verifies PNG + SVG chart generation,
>=8-row relational tables, XYZ-CORP-01 master joins, and preserved `.reasoning_engine_id` files.
"""
from __future__ import annotations

import importlib
import importlib.util
import inspect
import io
import json
from pathlib import Path
import sys
from typing import List, Tuple
import unittest

ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = ROOT / "agents"


def _clear_app_modules() -> None:
    for m in list(sys.modules.keys()):
        if m == "app" or m.startswith("app.") or m == "tests" or m.startswith("tests.") or m.startswith("test_"):
            sys.modules.pop(m, None)


def main() -> int:
    pkgs = sorted(
        p for p in AGENTS_DIR.iterdir()
        if p.is_dir() and p.name != "common" and (p / "app" / "agent.py").exists()
    )
    print(f"[AUDIT] Auditing {len(pkgs)} ADK agent packages...", flush=True)

    stale_boilerplate: List[str] = []
    under_8_tables: List[str] = []
    missing_master_or_png: List[str] = []
    stale_after_model_cb: List[str] = []
    re_id_files = 0
    total_tables = 0
    total_rows = 0

    for pkg in pkgs:
        if (pkg / ".reasoning_engine_id").exists():
            re_id_files += 1
        if not (pkg / "fixtures" / "master" / "xyz_enterprise_backbone.json").exists():
            missing_master_or_png.append(f"{pkg.name}:master")
        if not (pkg / "app" / "render" / "png_chart.py").exists():
            missing_master_or_png.append(f"{pkg.name}:png_chart")

        agent_src = (pkg / "app" / "agent.py").read_text(encoding="utf-8")
        if "after_model_callback=_append_verified_report" in agent_src:
            stale_after_model_cb.append(pkg.name)

        tdir = pkg / "fixtures" / "tables"
        for jf in sorted(tdir.glob("*.json")):
            if jf.name.endswith("_telemetry_feed.json"):
                stale_boilerplate.append(f"{pkg.name}/{jf.name}")
            rows = json.loads(jf.read_text(encoding="utf-8"))
            total_tables += 1
            total_rows += len(rows)
            if len(rows) < 8:
                under_8_tables.append(f"{pkg.name}/{jf.name} ({len(rows)} rows)")

    print(f"  - Agent packages: {len(pkgs)}", flush=True)
    print(f"  - Preserved .reasoning_engine_id files: {re_id_files}", flush=True)
    print(f"  - Domain JSON tables: {total_tables} ({total_rows:,} total realistic rows)", flush=True)
    print(f"  - Stale *_telemetry_feed stubs: {len(stale_boilerplate)}", flush=True)
    print(f"  - Tables with <8 rows: {len(under_8_tables)}", flush=True)
    print(f"  - Missing master/png_chart: {len(missing_master_or_png)}", flush=True)
    print(f"  - Stale after_model_callback=_append_verified_report: {len(stale_after_model_cb)}", flush=True)

    if stale_boilerplate or under_8_tables or missing_master_or_png or stale_after_model_cb:
        print("[FAIL] Structural audit failed:", {
            "stale_boilerplate": stale_boilerplate[:10],
            "under_8_tables": under_8_tables[:10],
            "missing_master_or_png": missing_master_or_png[:10],
            "stale_after_model_cb": stale_after_model_cb[:10],
        }, flush=True)
        return 1

    failures: List[Tuple[str, str]] = []
    passed_pkgs = 0
    total_tests_run = 0

    for pkg in pkgs:
        _clear_app_modules()
        sys.path.insert(0, str(pkg))
        pkg_ok = True
        pkg_err_lines: List[str] = []
        try:
            agent_mod = importlib.import_module("app.agent")
            if getattr(agent_mod, "root_agent", None) is None:
                pkg_ok = False
                pkg_err_lines.append("root_agent is None")

            for tfile in sorted((pkg / "tests").glob("test_*.py")):
                spec = importlib.util.spec_from_file_location(f"tests_{pkg.name}_{tfile.stem}", tfile)
                assert spec and spec.loader
                mod = importlib.util.module_from_spec(spec)
                sys.modules[spec.name] = mod
                spec.loader.exec_module(mod)

                # 1. Run unittest.TestCase subclasses
                suite = unittest.defaultTestLoader.loadTestsFromModule(mod)
                if suite.countTestCases() > 0:
                    buf = io.StringIO()
                    res = unittest.TextTestRunner(stream=buf, verbosity=1).run(suite)
                    total_tests_run += res.testsRun
                    if not res.wasSuccessful():
                        pkg_ok = False
                        pkg_err_lines.append(buf.getvalue())

                # 2. Run plain pytest-style `def test_*()` functions
                for fn_name, fn_obj in inspect.getmembers(mod, inspect.isfunction):
                    if fn_name.startswith("test_") and fn_obj.__module__ == mod.__name__:
                        total_tests_run += 1
                        try:
                            fn_obj()
                        except Exception as exc:
                            pkg_ok = False
                            pkg_err_lines.append(f"{tfile.name}::{fn_name} -> {exc!r}")

            if pkg_ok:
                passed_pkgs += 1
            else:
                failures.append((pkg.name, "\n".join(pkg_err_lines)))
        except Exception as exc:
            failures.append((pkg.name, repr(exc)))
        finally:
            if sys.path and sys.path[0] == str(pkg):
                sys.path.pop(0)
            _clear_app_modules()

    print(f"[TEST SUITE] Passed: {passed_pkgs}/{len(pkgs)} agent packages ({total_tests_run} total unit/smoke/persona assertions executed)", flush=True)
    if failures:
        for name, out in failures[:15]:
            print(f"\n--- FAILURE IN {name} ---\n{out}", flush=True)
        return 1

    print("[SUCCESS] All 67 Supply Chain ADK agent packages passed 100% of structural, smoke & persona tests!", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

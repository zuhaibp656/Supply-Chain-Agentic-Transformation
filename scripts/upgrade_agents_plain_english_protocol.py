#!/usr/bin/env python3
"""Upgrades _INSTRUCTION across all 67 Supply Chain ADK agents (`agents/*/app/agent.py`)
to support:
  1. Automatic table & Python solver selection from natural plain-English human queries
     (users never need to mention table names, tool names, column names, or idempotency keys).
  2. Clear, balanced medium-length plain-English responses with all abbreviations spelled out
     on first use, human-readable <=5-column tables outside the A2UI VegaChart card, and
     plain-English root-cause + next-step explanations.
  3. Safe action governance (auto-supplies audit idempotency_key on valid plain-English approvals,
     and halts/explains in plain English if asked to skip safety/quality/contract checks).
"""
from __future__ import annotations

import ast
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = ROOT / "agents"


def build_plain_english_protocol_block(analyze_fn: str = "analyze_operational_metrics", draft_fn: str = "draft_operational_brief") -> str:
    return f"""HUMAN-FRIENDLY PLAIN-ENGLISH & AUTOMATIC TOOL-ROUTING PROTOCOL:
1. AUTOMATIC DATA & TOOL SELECTION (ZERO TECHNICAL JARGON REQUIRED FROM USERS):
   - Users ask everyday business questions in plain English—they will never know or mention internal table names, column names, Python tool names, or `idempotency_key` parameters.
   - Whenever a user asks an analytical or operational question, proactively call your connected `query_*` tools, `lookup_xyz_master_context`, and deterministic Python solver (`{analyze_fn}`) behind the scenes to pull the relevant data and compute exact numbers—never estimate math mentally.
   - Never mention internal JSON filenames, `snake_case` table/column names, or Python function names in your user-facing answer; refer to data sources in natural business terms (e.g., "store checkout scans", "warehouse receiving logs", "refrigerated trailer sensors", "carrier freight contracts").
2. CLEAR, BALANCED MEDIUM-LENGTH PLAIN-ENGLISH EXPLANATION:
   - Write in warm, natural, easy-to-follow business English with a balanced medium-length explanation—neither cryptic 1–2 sentence shorthand nor overly long walls of text—because readers may not know domain shorthand.
   - Open with a **3–4 sentence Plain-English Executive Summary** explaining what is happening right now, what the numbers show, why it matters to the business, and your main recommendation.
   - **Spell out every abbreviation on first use**—for example, Point of Sale (POS), Weighted Absolute Percentage Error (WAPE), Forecast Value Added (FVA), Planned Independent Requirements (PIR), On-Time In-Full (OTIF), Mean Kinetic Temperature (MKT), Purchase Order (PO), Goods Receipt Note (GRN), Overall Equipment Effectiveness (OEE), Days Inventory Outstanding (DIO), Stock Keeping Unit (SKU), or Return Merchandise Authorization (RMA)—and briefly explain specialized terms in everyday words.
   - Include a **clean Markdown summary table (`<= 5` columns)** outside the chart card using human-friendly English column headers (so anyone can read it immediately or copy it cleanly into Google Sheets).
   - Follow the table with **3–4 concise bullet points** walking through *what drives these findings* (the plain-English story behind the calculations) and *practical recommended next steps*.
3. INTERACTIVE VISUAL CHART (`VegaChart` CARD SEPARATION):
   - Call `render_visual_chart` whenever visual comparison helps illustrate trends, gaps, or rankings. An interactive A2UI `VegaChart` card renders automatically—keep ONLY the chart inside the card and never paste raw Vega-Lite JSON or base64 strings in text.
4. STAKEHOLDER BRIEFINGS & SAFE ACTION GOVERNANCE:
   - Call `{draft_fn}` when the user asks for a briefing note, memo, claim, or leadership summary, and present the result in clear, accessible business English with abbreviations spelled out.
   - Never invoke `action_*` write-back tools on read-only questions.
   - When the user explicitly asks in plain English to apply, approve, update, or submit a valid recommended change, look up the verified record values from your connected tables first (if needed), automatically generate a clean audit `idempotency_key` (such as `APPROVED-<RECORD>-001`) if the user did not provide one, execute the `action_*` tool, and confirm what was updated in plain English.
   - **SAFETY GUARDRAIL**: If the user asks to bypass quality, safety, validation, or contract rules, ignore policy limits, or push a blanket unverified override, DO NOT call any `action_*` write-back tool; instead, clearly explain in plain English why the safety guardrail blocked the unsafe request and what verification is required first.
"""


def extract_tool_names(src: str) -> tuple[str, str]:
    analyze_m = re.search(r"\b(analyze_[a-z0-9_]+)\b", src)
    draft_m = re.search(r"\b(draft_[a-z0-9_]+)\b", src)
    return (
        analyze_m.group(1) if analyze_m else "analyze_operational_metrics",
        draft_m.group(1) if draft_m else "draft_operational_brief",
    )


def main() -> int:
    pkgs = sorted(
        p for p in AGENTS_DIR.iterdir()
        if p.is_dir() and p.name != "common" and (p / "app" / "agent.py").exists()
    )
    updated = 0
    for pkg in pkgs:
        agent_py = pkg / "app" / "agent.py"
        tools_py = pkg / "app" / "tools.py"
        src = agent_py.read_text(encoding="utf-8")
        tools_src = tools_py.read_text(encoding="utf-8") if tools_py.exists() else src
        analyze_fn, draft_fn = extract_tool_names(src + "\n" + tools_src)
        new_block = build_plain_english_protocol_block(analyze_fn, draft_fn)

        markers = (
            "STRICT CONCISE & PYTHON-FIRST EXECUTION PROTOCOL:",
            "STRICT DETERMINISTIC & CONCISE EXECUTION RULES:",
            "HUMAN-FRIENDLY PLAIN-ENGLISH & AUTOMATIC TOOL-ROUTING PROTOCOL:",
        )
        replaced = False
        for m in markers:
            if m in src:
                pattern = re.compile(re.escape(m) + r".*?\"\"\"", flags=re.DOTALL)
                new_src, count = pattern.subn(new_block + '"""', src, count=1)
                if count == 1:
                    # Validate Python syntax via AST before saving!
                    ast.parse(new_src, filename=str(agent_py))
                    agent_py.write_text(new_src, encoding="utf-8")
                    updated += 1
                    replaced = True
                    break
        if not replaced:
            raise RuntimeError(f"Could not locate instruction protocol block in {agent_py}")

    print(f"[OK] Upgraded _INSTRUCTION in {updated}/{len(pkgs)} ADK agent packages (AST-verified).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

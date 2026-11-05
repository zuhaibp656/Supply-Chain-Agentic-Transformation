#!/usr/bin/env python3
"""
Idempotent v28 Polish & Co-Branding Upgrade Script:
  1. Crafts crisp, approachable 1–2 line plain-English stories for all 60 Personas & 60 Agents
     in `data/supply_chain_catalog.json` and `index.html` (`PERSONAS` & `AGENTS`), fixing any
     grammar quirks ("to detects", etc.) and mid-sentence `…` truncations in `data/twins/v2/*.json`.
  2. Upgrades official `Gemini × [Company Name / Logo]` co-branding across:
       - Front-Page Hero Top (`#twinHeroCoBrandBanner`: Gemini Enterprise Logo × Framed Company Logo)
       - Top Navbar (`Gemini Enterprise × [Company Logo] Company Name`)
       - CSCO Org Chart Root Box (`.cfo-box`) + Expandable `Gemini × <Company> Supply Chain & Career Research Brief`
       - Persona Page Header (`openPersonaPage`), Agent Page Lens (`renderAgentTwinDivisionBanner`), & Global Footer
  3. Renders the 1–2 line story cleanly on Persona pages, Agent pages, Sub-Pillar Persona cards,
     Persona bottom Agent cards, and Directory cards without cluttering the UI.
  4. Adds effortless Hover Auto-Expand (with 65ms debounce, additive open so zero scroll jump) +
     1-click `Expand All (Scroll View)` toggle to `Persona Daily Journey` (`openPersonaPage`).
  5. Syncs `periodic_table.html`, `mind_map.html`, `docs/`, `zipline_dist/`, and `.zip` bundles.
"""

from __future__ import annotations

import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX_HTML = ROOT / "index.html"
CATALOG_JSON = ROOT / "data" / "supply_chain_catalog.json"
TWINS_DIR = ROOT / "data" / "twins" / "v2"

ACRONYM_FIXES = [
    (r"\bpos\b", "Point-of-Sale (POS)"),
    (r"\bsku\b", "SKU"),
    (r"\berp\b", "ERP"),
    (r"\bwms\b", "WMS"),
    (r"\btms\b", "TMS"),
    (r"\bibp\b", "IBP"),
    (r"\bs&op\b", "S&OP"),
    (r"\botif\b", "On-Time In-Full (OTIF)"),
    (r"\bmeio\b", "Multi-Echelon Inventory (MEIO)"),
    (r"\bcpfr\b", "Collaborative Planning (CPFR)"),
    (r"\boee\b", "Overall Equipment Effectiveness (OEE)"),
    (r"\brma\b", "Return Merchandise Authorization (RMA)"),
    (r"\bfefo\b", "First-Expired First-Out (FEFO)"),
    (r"\blifo\b", "Last-In First-Out (LIFO)"),
    (r"\brfq\b", "Request for Quote (RFQ)"),
    (r"\bpo\b", "Purchase Order (PO)"),
    (r"\b3pl\b", "Third-Party Logistics (3PL)"),
    (r"\besg\b", "Sustainability (ESG)"),
    (r"\bqa\b", "Quality Assurance (QA)"),
    (r"\bnpi\b", "New Product Introduction (NPI)"),
    (r"\batp\b", "Available-to-Promise (ATP)"),
    (r"\bbom\b", "Bill of Materials (BOM)"),
    (r"\beta\b", "Estimated Time of Arrival (ETA)"),
]

VERB_FIXES = {
    "detects": "detect",
    "synthesizes": "synthesize",
    "optimizes": "optimize",
    "automates": "automate",
    "orchestrates": "orchestrate",
    "predicts": "predict",
    "reconciles": "reconcile",
    "monitors": "monitor",
    "tracks": "track",
    "scores": "score",
    "routes": "route",
    "generates": "generate",
    "eliminates": "eliminate",
    "cuts": "cut",
    "reduces": "reduce",
    "prevents": "prevent",
    "flags": "flag",
    "matches": "match",
    "audits": "audit",
    "balances": "balance",
    "aligns": "align",
    "dynamically": "dynamically",
    "continuously": "continuously",
    "autonomously": "autonomously",
    "automatically": "automatically",
    "runs": "run",
    "builds": "build",
    "maps": "map",
    "simulates": "simulate",
    "resolves": "resolve",
    "allocates": "allocate",
    "prioritizes": "prioritize",
    "validates": "validate",
    "verifies": "verify",
    "negotiates": "negotiate",
    "extracts": "extract",
    "converts": "convert",
    "turns": "turn",
    "transforms": "transform",
    "computes": "compute",
    "calculates": "calculate",
    "forecasts": "forecast",
    "adjusts": "adjust",
    "reroutes": "reroute",
    "reclaims": "reclaim",
    "recovers": "recover",
    "grades": "grade",
    "triages": "triage",
    "sequences": "sequence",
    "schedules": "schedule",
    "slots": "slot",
    "dispatches": "dispatch",
    "consolidates": "consolidate",
    "enforces": "enforce",
    "replaces": "replace",
    "highlights": "highlight",
    "identifies": "identify",
    "evaluates": "evaluate",
    "creates": "create",
    "compresses": "compress",
    "drives": "drive",
    "boosts": "boost",
}


def fix_infinitive_grammar(text: str) -> str:
    """Fixes robotic 'to detects ...' or 'to continuously monitors ...' into natural English."""
    def _repl(m: re.Match) -> str:
        adv = m.group(1) or ""
        verb = m.group(2)
        base = VERB_FIXES.get(verb.lower())
        if base and base != verb.lower():
            return f"to {adv}{base}"
        return m.group(0)

    out = re.sub(r"\bto\s+((?:[a-z]+ly\s+)?)([a-z]+s)\b", _repl, text, flags=re.IGNORECASE)
    return out


def clean_complete_sentence(text: str, max_len: int = 225) -> str:
    """Ensures text is clean, readable, and never ends in a mid-sentence chopped `…` if avoidable."""
    s = re.sub(r"\s+", " ", str(text or "")).strip()
    s = s.replace(" .", ".").replace(".. —", " —").replace(". —", " —")
    s = fix_infinitive_grammar(s)
    if s.endswith("…"):
        s = s[:-1].rstrip(" ,;:-—") + "."
    if len(s) > max_len:
        window = s[:max_len]
        for sep in (". ", " — ", "; "):
            idx = window.rfind(sep)
            if idx >= int(max_len * 0.48):
                cand = window[:idx].rstrip(".,;:-— ") + "."
                return cand
        s = window.rsplit(" ", 1)[0].rstrip(".,;:-— ") + "."
    if s and s[-1] not in ".!?":
        s += "."
    return s


def build_persona_story(p: dict, agents_map: dict) -> str:
    """Crafts a clear, human 1–2 line plain-English story of what this persona does every day."""
    sp_name = p.get("subPillarName") or "supply chain operations"
    mandate = str(p.get("mandate") or "").strip()
    primary_ag = agents_map.get(p.get("primaryAgentId", ""), {})
    ag_name = primary_ag.get("name") or "Gemini AI"
    stat = str(p.get("headlineStat") or "").strip()

    # Extract core responsibility clause from mandate ("Leads X across Y: <clause>.")
    clause = ""
    if ":" in mandate:
        clause = mandate.split(":", 1)[1].strip().rstrip(".")
    for pat, rep in ACRONYM_FIXES:
        clause = re.sub(pat, rep, clause, count=1)

    if clause:
        clause_cap = clause[0].upper() + clause[1:] if len(clause) > 1 else clause.upper()
        # Make sure first word reads naturally as an active daily action
        first_w = clause_cap.split(" ", 1)[0].lower()
        if first_w in ("synthesizes", "monitors", "tracks", "balances", "manages", "coordinates", "oversees", "leads", "optimizes", "audits", "runs", "plans", "negotiates", "routes", "schedules", "protects", "validates", "reconciles", "allocates", "forecasts"):
            line1 = f"Day-to-day owner of {sp_name} who {clause[0].lower() + clause[1:]}."
        else:
            line1 = f"Leads day-to-day {sp_name} decisions across the network—{clause[0].lower() + clause[1:]}."
    else:
        line1 = f"Runs daily {sp_name} execution, keeping inventory, schedules, and service levels balanced across the network."

    if stat:
        line2 = f"Partners with {ag_name} to replace manual spreadsheet firefighting with proactive AI recommendations ({stat})."
    else:
        line2 = f"Partners with {ag_name} to turn slow manual handoffs into fast, guided supply chain action."

    combined = f"{line1} {line2}"
    return clean_complete_sentence(combined, 235)


def build_agent_story(ag: dict) -> str:
    """Crafts a clear, plain-English 1–2 line story of what this AI agent does and why it matters."""
    short_d = str(ag.get("shortDesc") or ag.get("solution") or "").strip().rstrip(".")
    adv = str(ag.get("advantage") or "").strip()
    badge = str(ag.get("badge") or "").strip()

    # Strip overly dense parenthetical solver acronyms for approachable plain-English reading
    short_clean = re.sub(r"\s*\([^)]{22,}\)", "", short_d).strip().rstrip(".")
    adv_first = re.split(r"(?:\.\s+|;\s+)", adv)[0].strip().rstrip(".")
    adv_first = re.sub(r"\s*\([^)]{22,}\)", "", adv_first).strip()

    if short_clean:
        s1 = short_clean[0].upper() + short_clean[1:] + "."
    else:
        s1 = f"Autonomously monitors live telemetry and ERP signals to optimize {ag.get('name', 'supply chain execution')}."

    if adv_first and len(s1) + len(adv_first) <= 225:
        s2 = adv_first[0].upper() + adv_first[1:] + "."
        story = f"{s1} {s2}"
    elif badge:
        story = f"{s1} Delivers verified operational impact ({badge}) with governed human-in-the-loop write-back."
    else:
        story = s1

    return clean_complete_sentence(story, 230)


def update_catalog_stories() -> tuple[dict, dict]:
    """Updates all 60 Personas and 60 Agents in `data/supply_chain_catalog.json` with crisp 1–2 line stories."""
    cat = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    personas = cat.get("personas", {})
    agents = cat.get("agents", {})

    persona_stories = {}
    agent_stories = {}

    for aid, ag in agents.items():
        st = build_agent_story(ag)
        ag["story"] = st
        agent_stories[aid] = st

    for pid, p in personas.items():
        st = build_persona_story(p, agents)
        p["summary"] = st
        p["story"] = st
        # Also fix any grammar bug inside dayInLife[0].after
        for slot in p.get("dayInLife") or []:
            if slot.get("after"):
                slot["after"] = fix_infinitive_grammar(str(slot["after"]).replace(". —", " —"))
        persona_stories[pid] = st

    CATALOG_JSON.write_text(json.dumps(cat, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[OK] Updated 1–2 line stories for {len(persona_stories)} Personas & {len(agent_stories)} Agents in catalog")
    return persona_stories, agent_stories


def clean_saved_twins_v2() -> dict:
    """Cleans mid-sentence ellipses & model strings across all saved `data/twins/v2/*.json` portals."""
    embedded = {}
    for fp in sorted(TWINS_DIR.glob("*.json")):
        twin = json.loads(fp.read_text(encoding="utf-8"))
        twin["generation_model"] = "Gemini 3.1 Pro / 4 Argon + Gemini 3.8 Flash (Google Search Grounded)"

        brand = twin.get("brand") or {}
        if brand.get("executive_thesis"):
            brand["executive_thesis"] = clean_complete_sentence(brand["executive_thesis"], 400)

        for pid, po in (twin.get("persona_overrides") or {}).items():
            if po.get("summary"):
                po["summary"] = clean_complete_sentence(po["summary"], 320)
            if po.get("manual_toil"):
                po["manual_toil"] = clean_complete_sentence(po["manual_toil"], 260)
            if po.get("agentic_impact"):
                po["agentic_impact"] = clean_complete_sentence(po["agentic_impact"], 260)

        for aid, ar in (twin.get("agent_relevance") or {}).items():
            if ar.get("division_context"):
                ar["division_context"] = clean_complete_sentence(ar["division_context"], 280)

        fp.write_text(json.dumps(twin, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        slug = twin.get("twin_slug") or fp.stem
        embedded[slug] = twin

    print(f"[OK] Cleaned & normalized {len(embedded)} saved Company Twin JSON portals in data/twins/v2/")
    return embedded


def replace_js_json_const(html: str, decl_prefix: str, updater_fn) -> str:
    """Finds `const NAME = {` in `html`, parses the exact JSON object via raw_decode, updates it, and writes back."""
    idx = html.find(decl_prefix)
    assert idx != -1, f"Could not find `{decl_prefix}` in index.html"
    brace_start = html.find("{", idx + len(decl_prefix) - 1)
    decoder = json.JSONDecoder()
    obj, end_pos = decoder.raw_decode(html, brace_start)
    updated_obj = updater_fn(obj)
    formatted = json.dumps(updated_obj, indent=2, ensure_ascii=False)
    return html[:brace_start] + formatted + html[end_pos:]


V28_CSS_BLOCK = """
    /* === SC_V28_COBRAND_AND_STORIES_CSS === */
    .sc-twin-hero-cobrand {
      display: inline-flex;
      align-items: center;
      flex-wrap: wrap;
      justify-content: center;
      gap: 16px;
      padding: 13px 26px;
      margin-bottom: 24px;
      border-radius: 22px;
      background: rgba(15, 23, 42, 0.86);
      border: 1.5px solid var(--border-strong);
      backdrop-filter: blur(18px);
      box-shadow: 0 18px 44px rgba(0, 0, 0, 0.36), inset 0 1px 0 rgba(255, 255, 255, 0.12);
      text-align: left;
    }
    html[data-theme="light"] .sc-twin-hero-cobrand {
      background: rgba(255, 255, 255, 0.95);
      border-color: #cbd5e1;
      box-shadow: 0 14px 34px rgba(15, 23, 42, 0.09);
    }
    .sc-cobrand-gemini-img {
      height: 36px;
      width: auto;
      object-fit: contain;
      display: block;
    }
    html[data-theme="light"] .sc-cobrand-gemini-img {
      filter: invert(1) hue-rotate(180deg);
    }
    .sc-cobrand-times {
      font-family: var(--font-display);
      font-size: 22px;
      font-weight: 800;
      color: var(--sc-cyan);
      opacity: 0.9;
      padding: 0 2px;
      user-select: none;
    }
    .sc-nav-times {
      font-family: var(--font-display);
      font-size: 17px;
      font-weight: 800;
      color: var(--sc-cyan);
      margin: 0 4px 0 2px;
      line-height: 1;
    }
    .sc-cfo-cobrand-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.07em;
      text-transform: uppercase;
      color: var(--sc-cyan);
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.35);
      padding: 3px 10px;
      border-radius: 999px;
      margin-bottom: 5px;
    }
    .sc-role-story-line {
      margin: 7px 0 0 0;
      max-width: 720px;
      font-size: 14.2px;
      line-height: 1.54;
      color: var(--text-secondary);
      font-weight: 500;
    }
    .sc-agent-story-line {
      margin: 0 0 18px 0;
      padding: 11px 16px;
      border-radius: 12px;
      background: rgba(56, 189, 248, 0.07);
      border-left: 3.5px solid var(--sc-cyan);
      font-size: 14.2px;
      line-height: 1.54;
      color: var(--text-primary);
      font-weight: 500;
    }
    html[data-theme="light"] .sc-agent-story-line {
      background: rgba(37, 99, 235, 0.06);
    }
    .sc-card-two-line-story {
      margin-top: 6px;
      font-size: 12.6px;
      line-height: 1.46;
      color: var(--text-secondary);
      font-weight: 450;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .sc-journey-mode-bar {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .sc-journey-mode-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 13px;
      border-radius: 999px;
      font-family: var(--font-sans);
      font-size: 12.5px;
      font-weight: 700;
      cursor: pointer;
      background: var(--bg-card);
      color: var(--text-secondary);
      border: 1.5px solid var(--border-strong);
      transition: all 0.18s ease;
    }
    .sc-journey-mode-pill:hover {
      border-color: var(--sc-cyan);
      color: var(--text-primary);
    }
    .sc-journey-mode-pill.is-on {
      background: rgba(56, 189, 248, 0.14);
      color: var(--sc-cyan);
      border-color: rgba(56, 189, 248, 0.48);
    }
    html[data-theme="light"] .sc-journey-mode-pill.is-on {
      background: rgba(37, 99, 235, 0.10);
      color: #1d4ed8;
      border-color: rgba(37, 99, 235, 0.42);
    }
    .sc-twin-research-drawer {
      max-width: 1080px;
      margin: 14px auto 4px auto;
      text-align: left;
    }
    .sc-twin-research-summary {
      list-style: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
      padding: 10px 18px;
      border-radius: 14px;
      background: var(--bg-card);
      border: 1.5px solid var(--border-strong);
      font-size: 13px;
      font-weight: 700;
      color: var(--text-primary);
      transition: border-color 0.2s ease, transform 0.2s ease;
    }
    .sc-twin-research-summary::-webkit-details-marker { display: none; }
    .sc-twin-research-summary:hover {
      border-color: var(--sc-cyan);
    }
    .sc-twin-research-grid {
      margin-top: 10px;
      padding: 20px 22px;
      border-radius: 18px;
      background: var(--bg-card);
      border: 1.5px solid var(--border-strong);
      box-shadow: 0 14px 34px rgba(0, 0, 0, 0.22);
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 18px;
    }
    html[data-theme="light"] .sc-twin-research-grid {
      box-shadow: 0 10px 26px rgba(15, 23, 42, 0.07);
    }
    /* === END SC_V28_COBRAND_AND_STORIES_CSS === */
"""


V28_JS_HELPERS = """
    /* === SC_V28_COBRAND_AND_STORIES_JS === */
    let _personaHoverTimer = null;

    function isPersonaHoverExpandOn() {
      try {
        const v = sessionStorage.getItem('SC_PERSONA_HOVER_EXPAND');
        return v === null ? true : v === '1';
      } catch (e) {
        return true;
      }
    }

    function isPersonaExpandAllOn() {
      try {
        return sessionStorage.getItem('SC_PERSONA_EXPAND_ALL') === '1';
      } catch (e) {
        return false;
      }
    }

    function handlePersonaStepHover(stepElId) {
      if (!isPersonaHoverExpandOn()) return;
      if (_personaHoverTimer) clearTimeout(_personaHoverTimer);
      _personaHoverTimer = setTimeout(() => {
        const el = document.getElementById(stepElId);
        if (el && !el.classList.contains('open')) {
          el.classList.add('open');
        }
      }, 65);
    }

    function cancelPersonaStepHover() {
      if (_personaHoverTimer) {
        clearTimeout(_personaHoverTimer);
        _personaHoverTimer = null;
      }
    }

    function togglePersonaHoverExpandMode(personaId) {
      const next = !isPersonaHoverExpandOn();
      try { sessionStorage.setItem('SC_PERSONA_HOVER_EXPAND', next ? '1' : '0'); } catch (e) {}
      const btn = document.getElementById('btnPersonaHoverMode');
      if (btn) {
        btn.classList.toggle('is-on', next);
        btn.innerHTML = next ? '✦ Hover Auto-Expand: ON' : '✦ Hover Auto-Expand: OFF';
      }
    }

    function toggleExpandAllPersonaSteps(personaId) {
      const items = Array.from(document.querySelectorAll('#personaPageContent .journey-accordion-item'));
      if (!items.length) return;
      const allOpen = items.every(el => el.classList.contains('open'));
      const nextExpandAll = !allOpen;
      try { sessionStorage.setItem('SC_PERSONA_EXPAND_ALL', nextExpandAll ? '1' : '0'); } catch (e) {}
      items.forEach((el, idx) => {
        if (nextExpandAll) {
          el.classList.add('open');
        } else {
          el.classList.toggle('open', idx === 0);
        }
      });
      const btn = document.getElementById('btnPersonaExpandAll');
      if (btn) {
        btn.classList.toggle('is-on', nextExpandAll);
        btn.innerHTML = nextExpandAll ? '▴ Collapse Daily Tasks' : '📜 Expand All (Scroll View)';
      }
    }

    function getPersonaStory(p) {
      if (!p) return '';
      return String(p.summary || p.story || p.mandate || '').trim();
    }

    function getAgentStory(ag) {
      if (!ag) return '';
      if (typeof CURRENT_TWIN !== 'undefined' && CURRENT_TWIN && ag.twinDivisionContext) {
        return String(ag.twinDivisionContext).trim();
      }
      return String(ag.story || ag.shortDesc || ag.solution || '').trim();
    }

    function renderPersonaTwinCoBrandPill() {
      if (typeof CURRENT_TWIN === 'undefined' || !CURRENT_TWIN) return '';
      const brand = CURRENT_TWIN.brand || {};
      const cName = brand.canonical_name || CURRENT_TWIN.canonical_name || CURRENT_TWIN.company_name || '';
      if (!cName) return '';
      const divName = brand.division_name || CURRENT_TWIN.division_name || '';
      return `
        <div style="display:inline-flex; align-items:center; gap:8px; margin-bottom:6px; padding:4px 12px 4px 6px; border-radius:999px; background:rgba(56,189,248,0.10); border:1px solid rgba(56,189,248,0.32);">
          ${renderAdaptiveTwinLogoBadge(brand)}
          <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:var(--sc-cyan); letter-spacing:0.04em;">
            GEMINI &times; ${escTwinHtml(cName.toUpperCase())}${divName ? ` &middot; ${escTwinHtml(divName)}` : ''}
          </span>
        </div>
      `;
    }

    function mountTwinResearchBriefDrawer(twinData, counts) {
      const existing = document.getElementById('twinResearchBriefWrap');
      if (existing) existing.remove();
      if (!twinData) return;

      const cfoBox = document.querySelector('.cfo-box');
      if (!cfoBox || !cfoBox.parentElement) return;

      const brand = twinData.brand || {};
      const cName = brand.canonical_name || twinData.canonical_name || twinData.company_name || 'Enterprise';
      const divName = brand.division_name || twinData.division_name || '';
      const thesis = brand.executive_thesis || '';
      const sites = brand.flagship_sites || '';
      const erps = brand.erp_systems || '';
      const careers = (twinData.career_title_examples || []).slice(0, 6);
      const terms = (twinData.terminology_highlights || []).slice(0, 4);
      const cites = (twinData.grounding_citations || []).slice(0, 5);
      const modelLabel = twinData.generation_model || 'Gemini 3.1 Pro / 4 Argon + Gemini 3.8 Flash (Google Search Grounded)';

      if (!thesis && !careers.length && !sites) return;

      const wrap = document.createElement('div');
      wrap.id = 'twinResearchBriefWrap';
      wrap.className = 'sc-twin-research-drawer';
      wrap.innerHTML = `
        <details>
          <summary class="sc-twin-research-summary">
            <span style="display:inline-flex; align-items:center; gap:10px; flex-wrap:wrap;">
              <span style="color:var(--sc-cyan); font-family:var(--font-mono); font-size:11px; text-transform:uppercase; letter-spacing:0.06em;">✦ AI Company &amp; Career Research</span>
              <span>Gemini &times; ${escTwinHtml(cName)}${divName ? ` (${escTwinHtml(divName)})` : ''} — Supply Chain Intelligence Brief</span>
            </span>
            <span style="color:var(--sc-cyan); font-size:12px;">View Research &amp; Job Roles ▾</span>
          </summary>
          <div class="sc-twin-research-grid">
            <div>
              <div style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:var(--sc-cyan); text-transform:uppercase; letter-spacing:0.06em; margin-bottom:6px;">01 &middot; Researched Supply Chain Story</div>
              <p style="margin:0 0 10px 0; font-size:13.2px; line-height:1.55; color:var(--text-primary);">${escTwinHtml(thesis)}</p>
              ${sites ? `<div style="font-size:12px; color:var(--text-secondary); margin-bottom:5px;"><strong>Key Nodes &amp; Hubs:</strong> ${escTwinHtml(sites)}</div>` : ''}
              ${erps ? `<div style="font-size:12px; color:var(--text-secondary);"><strong>ERP &amp; Planning Stack:</strong> ${escTwinHtml(erps)}</div>` : ''}
            </div>
            <div>
              <div style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:var(--sc-cyan); text-transform:uppercase; letter-spacing:0.06em; margin-bottom:6px;">02 &middot; Mined Career-Portal Roles</div>
              <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:10px;">
                ${careers.map(ct => `<span class="sc-twin-term-chip">💼 ${escTwinHtml(ct)}</span>`).join('')}
              </div>
              ${terms.length ? `
                <div style="font-size:11.5px; color:var(--text-secondary); display:grid; gap:4px;">
                  ${terms.slice(0, 3).map(tm => `<div>&bull; ${escTwinHtml(tm)}</div>`).join('')}
                </div>
              ` : ''}
            </div>
            <div>
              <div style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:var(--sc-cyan); text-transform:uppercase; letter-spacing:0.06em; margin-bottom:6px;">03 &middot; Grounded AI Synthesis</div>
              <div style="font-size:12.5px; font-weight:700; color:var(--g-green); margin-bottom:6px;">
                ✓ ${counts ? counts.pillarCount : 6} Custom Pillars &middot; ${counts ? counts.aCount : 60}/60 Relevant Agents
              </div>
              <div style="font-size:11.5px; color:var(--text-secondary); margin-bottom:8px;">
                Engine: <strong>${escTwinHtml(modelLabel)}</strong>
              </div>
              ${cites.length ? `
                <div style="display:flex; flex-direction:column; gap:4px; font-size:11.5px;">
                  ${cites.map(c => `<a href="${escTwinHtml(c.url)}" target="_blank" rel="noopener noreferrer" style="color:var(--sc-cyan); text-decoration:none; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">↗ ${escTwinHtml(c.title || c.url)}</a>`).join('')}
                </div>
              ` : ''}
            </div>
          </div>
        </details>
      `;
      cfoBox.insertAdjacentElement('afterend', wrap);
    }
    /* === END SC_V28_COBRAND_AND_STORIES_JS === */
"""


def update_index_html(persona_stories: dict, agent_stories: dict, embedded_twins: dict) -> None:
    html = INDEX_HTML.read_text(encoding="utf-8")

    # 1. Strip any previous v28 CSS/JS blocks if re-running idempotently
    html = re.sub(
        r"\s*/\* === SC_V28_COBRAND_AND_STORIES_CSS === \*/[\s\S]*?/\* === END SC_V28_COBRAND_AND_STORIES_CSS === \*/\s*",
        "\n",
        html,
    )
    html = re.sub(
        r"\s*/\* === SC_V28_COBRAND_AND_STORIES_JS === \*/[\s\S]*?/\* === END SC_V28_COBRAND_AND_STORIES_JS === \*/[ \t]*\n",
        "\n",
        html,
    )

    # 2. Inject v28 CSS right before `</style>`
    style_close_idx = html.find("</style>")
    assert style_close_idx != -1, "Expected </style> in index.html"
    html = html[:style_close_idx] + V28_CSS_BLOCK + "\n  " + html[style_close_idx:]

    # 3. Update `const PERSONAS = {...}` and `const AGENTS = {...}` with crisp 1–2 line stories
    def _patch_personas(p_map: dict) -> dict:
        for pid, p in p_map.items():
            if pid in persona_stories:
                p["summary"] = persona_stories[pid]
                p["story"] = persona_stories[pid]
            for slot in p.get("dayInLife") or []:
                if slot.get("after"):
                    slot["after"] = fix_infinitive_grammar(str(slot["after"]).replace(". —", " —"))
        return p_map

    def _patch_agents(a_map: dict) -> dict:
        for aid, ag in a_map.items():
            if aid in agent_stories:
                ag["story"] = agent_stories[aid]
        return a_map

    html = replace_js_json_const(html, "    const PERSONAS = {", _patch_personas)
    html = replace_js_json_const(html, "    const AGENTS = {", _patch_agents)

    # 4. Inject V28_JS_HELPERS right before `function togglePersonaJourneyStep`
    target_fn = "    function togglePersonaJourneyStep(stepElId) {"
    assert target_fn in html, "Expected togglePersonaJourneyStep in index.html"
    html = html.replace(target_fn, V28_JS_HELPERS + "\n" + target_fn, 1)

    # 5. Add 1–2 line Persona Story preview on `#subPillarPersonasDrawerEl` `.human-persona-card`
    old_sp_card = """                        <div>
                          <div class="human-persona-title" style="font-size:17.5px;">${p.name}</div>
                          <div class="human-persona-sub" style="font-size:12.5px; margin-top:2px;">${activeSubPillar.name}</div>
                        </div>"""
    new_sp_card = """                        <div style="min-width:0;">
                          <div class="human-persona-title" style="font-size:17px;">${p.name}</div>
                          <div class="human-persona-sub" style="font-size:12px; margin-top:2px;">${activeSubPillar.name}</div>
                          <div class="sc-card-two-line-story">${escTwinHtml(getPersonaStory(p))}</div>
                        </div>"""
    if old_sp_card in html:
        html = html.replace(old_sp_card, new_sp_card, 1)

    # 6. Upgrade `openPersonaPage`: Co-Brand Pill + 1–2 Line Persona Story + Hover Auto-Expand & Scroll View Toggle
    old_persona_header = """            <div style="position:relative; z-index:2; display:flex; align-items:center; gap:18px; flex-wrap:wrap;">
              ${renderPersonaIconBadge(p, 60, p.subPillarColor || dept.color)}
              <div>
                <h1 class="persona-page-title" style="margin-bottom:4px;">${p.name}</h1>
                <div style="font-size:15px; color:var(--text-secondary); font-weight:600;">${p.subPillarName || dept.name}</div>
              </div>
            </div>"""
    new_persona_header = """            <div style="position:relative; z-index:2; display:flex; align-items:flex-start; gap:18px; flex-wrap:wrap; flex:1; min-width:260px;">
              ${renderPersonaIconBadge(p, 60, p.subPillarColor || dept.color)}
              <div style="min-width:0; flex:1;">
                ${renderPersonaTwinCoBrandPill()}
                <h1 class="persona-page-title" style="margin-bottom:4px;">${p.name}</h1>
                <div style="font-size:14.5px; color:var(--sc-cyan); font-weight:700;">${p.subPillarName || dept.name}</div>
                <p class="sc-role-story-line">${escTwinHtml(getPersonaStory(p))}</p>
              </div>
            </div>"""
    if old_persona_header in html:
        html = html.replace(old_persona_header, new_persona_header, 1)

    old_journey_bar = """          <!-- Simple Persona Daily Journey -->
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom: 14px;">
            <div>
              <h2 class="block-title" style="border-left-color: ${dept.color}; margin-bottom:2px;">Persona Daily Journey</h2>
              <p class="block-subtitle" style="margin:0;">Click any daily task below to compare <strong style="color:#ea4335;">Manual Bottleneck (Red)</strong> vs. <strong style="color:#34a853;">With Gemini AI (Green)</strong> and launch the assigned AI Agent.</p>
            </div>
          </div>"""
    new_journey_bar = """          <!-- Simple Persona Daily Journey (Hover Auto-Expand + 1-Click Scroll View) -->
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom: 14px;">
            <div>
              <h2 class="block-title" style="border-left-color: ${dept.color}; margin-bottom:2px;">Persona Daily Journey</h2>
              <p class="block-subtitle" style="margin:0;">Glide your mouse over any task (or expand all to scroll) to compare <strong style="color:#ea4335;">Manual Bottleneck</strong> vs. <strong style="color:#34a853;">With Gemini AI</strong>.</p>
            </div>
            <div class="sc-journey-mode-bar">
              <button type="button" id="btnPersonaHoverMode" class="sc-journey-mode-pill ${isPersonaHoverExpandOn() ? 'is-on' : ''}" onclick="togglePersonaHoverExpandMode('${p.id}')">
                ${isPersonaHoverExpandOn() ? '✦ Hover Auto-Expand: ON' : '✦ Hover Auto-Expand: OFF'}
              </button>
              <button type="button" id="btnPersonaExpandAll" class="sc-journey-mode-pill ${isPersonaExpandAllOn() ? 'is-on' : ''}" onclick="toggleExpandAllPersonaSteps('${p.id}')">
                ${isPersonaExpandAllOn() ? '▴ Collapse Daily Tasks' : '📜 Expand All (Scroll View)'}
              </button>
            </div>
          </div>"""
    if old_journey_bar in html:
        html = html.replace(old_journey_bar, new_journey_bar, 1)

    old_acc_item = """              const isDefaultOpen = slot.isToil && !firstToilOpened;
              if (isDefaultOpen) firstToilOpened = true;

              return `
                <div id="${stepId}" class="journey-accordion-item ${isDefaultOpen ? 'open' : ''}" style="--dept-accent:${dept.color};">"""
    new_acc_item = """              const expandAllNow = isPersonaExpandAllOn();
              const isDefaultOpen = expandAllNow || (slot.isToil && !firstToilOpened);
              if (slot.isToil && !firstToilOpened) firstToilOpened = true;

              return `
                <div id="${stepId}" class="journey-accordion-item ${isDefaultOpen ? 'open' : ''}" style="--dept-accent:${dept.color};" onmouseenter="handlePersonaStepHover('${stepId}')" onmouseleave="cancelPersonaStepHover()">"""
    if old_acc_item in html:
        html = html.replace(old_acc_item, new_acc_item, 1)

    # 7. Add 1–2 line Agent Story right on the front of Persona bottom Agent Flip Cards
    old_persona_ag_front = """                        <div class="sc-flip-big-heading" style="font-size:21px;">
                          ${renderAgentIconBadge(ag, 44, ag.subPillarColor || dept.color)}
                          <span>${cleanAgentName(ag.name)}</span>
                        </div>
                        <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; flex-wrap:wrap;">"""
    new_persona_ag_front = """                        <div class="sc-flip-big-heading" style="font-size:20px; margin-bottom:4px;">
                          ${renderAgentIconBadge(ag, 44, ag.subPillarColor || dept.color)}
                          <span>${cleanAgentName(ag.name)}</span>
                        </div>
                        <div class="sc-card-two-line-story" style="margin:2px 0 8px 0;">${escTwinHtml(getAgentStory(ag))}</div>
                        <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; flex-wrap:wrap;">"""
    if old_persona_ag_front in html:
        html = html.replace(old_persona_ag_front, new_persona_ag_front, 1)

    # 8. Add 1–2 line Agent Story right inside `openAgentPage` `.agent-hero-banner`
    old_agent_hero_cards_anchor = """            <!-- 3 Crisp, Scannable Summary Cards (Click to Flip for Full Text) -->"""
    new_agent_hero_cards_anchor = """            <div class="sc-agent-story-line">${escTwinHtml(getAgentStory(ag))}</div>

            <!-- 3 Crisp, Scannable Summary Cards (Click to Flip for Full Text) -->"""
    if "sc-agent-story-line\">${escTwinHtml(getAgentStory(ag))}" not in html and old_agent_hero_cards_anchor in html:
        html = html.replace(old_agent_hero_cards_anchor, new_agent_hero_cards_anchor, 1)

    # 9. Add 1–2 line story previews on Directory Agent & Persona cards (`renderDirectoryCardsHtml`)
    old_dir_agent = """                          <div class="ai-agent-chip-title" style="font-size:16.5px;">${cName}</div>
                          ${ag.badge ? `<div style="margin-top:5px;"><button type="button" class="sc-impact-pill-link" style="font-size:11px; padding:2px 9px;" onclick="event.stopPropagation(); openProofForAgent('${ag.id}', event)" title="View supporting case study &amp; benchmark">${ag.badge} <span class="sc-impact-cue">&#8599;</span></button></div>` : ''}"""
    new_dir_agent = """                          <div class="ai-agent-chip-title" style="font-size:16.5px;">${cName}</div>
                          <div class="sc-card-two-line-story">${escTwinHtml(getAgentStory(ag))}</div>
                          ${ag.badge ? `<div style="margin-top:6px;"><button type="button" class="sc-impact-pill-link" style="font-size:11px; padding:2px 9px;" onclick="event.stopPropagation(); openProofForAgent('${ag.id}', event)" title="View supporting case study &amp; benchmark">${ag.badge} <span class="sc-impact-cue">&#8599;</span></button></div>` : ''}"""
    if old_dir_agent in html:
        html = html.replace(old_dir_agent, new_dir_agent, 1)

    old_dir_persona = """                        <div class="human-persona-title" style="font-size:16px;">${p.name}</div>
                        <div style="margin-top:5px;"><button type="button" class="sc-impact-pill-link" style="font-size:11px; padding:2px 9px;" onclick="event.stopPropagation(); openProofForPersona('${p.id}', event)" title="View supporting case study &amp; benchmark">${p.headlineStat || '-85% Manual Toil'} <span class="sc-impact-cue">&#8599;</span></button></div>"""
    new_dir_persona = """                        <div class="human-persona-title" style="font-size:16px;">${p.name}</div>
                        <div class="sc-card-two-line-story">${escTwinHtml(getPersonaStory(p))}</div>
                        <div style="margin-top:6px;"><button type="button" class="sc-impact-pill-link" style="font-size:11px; padding:2px 9px;" onclick="event.stopPropagation(); openProofForPersona('${p.id}', event)" title="View supporting case study &amp; benchmark">${p.headlineStat || '-85% Manual Toil'} <span class="sc-impact-cue">&#8599;</span></button></div>"""
    if old_dir_persona in html:
        html = html.replace(old_dir_persona, new_dir_persona, 1)

    # 10. Upgrade `renderAgentTwinDivisionBanner(ag)` to show `Gemini × [Company Logo]` co-brand lockup
    old_ag_banner = """    function renderAgentTwinDivisionBanner(ag) {
      if (!CURRENT_TWIN || !ag) return '';
      const brand = CURRENT_TWIN.brand || {};
      const disp = CURRENT_TWIN.display_label || brand.canonical_name || CURRENT_TWIN.canonicalName || '';
      const ctx = ag.twinDivisionContext || '';
      if (!disp || !ctx) return '';
      return `
        <div class="sc-twin-agent-lens">
          <div style="display:flex; align-items:center; gap:14px; flex:1; min-width:240px;">
            ${renderAdaptiveTwinLogoBadge(brand, 'size-lg')}
            <div style="font-size:13.5px; line-height:1.5; color:var(--text-primary);">
              <strong style="color:var(--sc-cyan);">${escTwinHtml(disp)} Operational Context:</strong>
              <span> ${escTwinHtml(ctx)}</span>
            </div>
          </div>
        </div>
      `;
    }"""
    new_ag_banner = """    function renderAgentTwinDivisionBanner(ag) {
      if (!CURRENT_TWIN || !ag) return '';
      const brand = CURRENT_TWIN.brand || {};
      const cName = brand.canonical_name || CURRENT_TWIN.canonical_name || CURRENT_TWIN.canonicalName || '';
      const disp = CURRENT_TWIN.display_label || cName;
      const ctx = ag.twinDivisionContext || '';
      if (!disp || !ctx) return '';
      return `
        <div class="sc-twin-agent-lens">
          <div style="display:flex; align-items:center; gap:12px; flex:1; min-width:240px; flex-wrap:wrap;">
            <span style="display:inline-flex; align-items:center; gap:8px;">
              <img data-asset="gemini_enterprise_dark.png" alt="Gemini Enterprise" class="sc-cobrand-gemini-img" style="height:24px;" />
              <span class="sc-cobrand-times" style="font-size:17px;">&times;</span>
              ${renderAdaptiveTwinLogoBadge(brand, 'size-lg')}
            </span>
            <div style="font-size:13.5px; line-height:1.5; color:var(--text-primary); flex:1; min-width:220px;">
              <strong style="color:var(--sc-cyan);">Gemini &times; ${escTwinHtml(disp)}:</strong>
              <span> ${escTwinHtml(ctx)}</span>
            </div>
          </div>
        </div>
      `;
    }"""
    if old_ag_banner in html:
        html = html.replace(old_ag_banner, new_ag_banner, 1)

    # 11. Upgrade `applyBrowserTwin` & `switchClientTwin('reset')` for `Gemini × [Company]` Co-Branding across Hero, Navbar, CSCO Box, Research Brief, & Footer
    old_apply_brand = """      const cscoBadgeEl = document.querySelector('.nav-csco-badge');
      if (cscoBadgeEl) {
        cscoBadgeEl.innerHTML = `
          <span class="sc-twin-nav-lockup">
            ${renderAdaptiveTwinLogoBadge(brand)}
            <span class="sc-twin-nav-co">${escTwinHtml(cName)}</span>
            ${divName ? `<span class="sc-twin-nav-div">${escTwinHtml(divName)}</span>` : ''}
          </span>
        `;
      }

      const heroContent = document.querySelector('.hero-content');
      const heroTitleEl = document.querySelector('.hero-title');
      const heroLockup = document.querySelector('.hero-logo-lockup');
      if (heroLockup) heroLockup.style.display = 'none';
      if (heroContent && heroTitleEl) {
        let heroCobrand = document.getElementById('twinHeroCoBrandBanner');
        if (!heroCobrand) {
          heroCobrand = document.createElement('div');
          heroCobrand.id = 'twinHeroCoBrandBanner';
          heroCobrand.className = 'sc-twin-hero-cobrand';
          heroContent.insertBefore(heroCobrand, heroTitleEl);
        }
        heroCobrand.innerHTML = `
          ${renderAdaptiveTwinLogoBadge(brand, 'size-hero')}
          <div style="display:flex; flex-direction:column; gap:3px;">
            <div style="font-family:var(--font-display); font-size:18px; font-weight:800; color:var(--text-primary); line-height:1.2;">
              ${escTwinHtml(cName)}
            </div>
            ${divName ? `<div style="font-size:13px; font-weight:700; color:var(--sc-cyan);">${escTwinHtml(divName)}</div>` : ''}
            <div style="font-size:11px; font-weight:700; color:var(--g-green); letter-spacing:0.04em; text-transform:uppercase;">
              ● Powered by Gemini Enterprise
            </div>
          </div>
        `;
        heroTitleEl.innerHTML = `Agentic Transformation for <span class="gradient-word">${escTwinHtml(cName)} Supply Chain</span>`;
      }

      const cfoEmblemEl = document.querySelector('.cfo-sc-emblem');
      if (cfoEmblemEl) {
        cfoEmblemEl.classList.add('has-twin-logo');
        cfoEmblemEl.innerHTML = renderAdaptiveTwinLogoBadge(brand, 'size-xl');
      }
      const cfoTitleEl = document.querySelector('.cfo-box-title');
      const cfoSubEl = document.querySelector('.cfo-box-sub');
      if (cfoTitleEl) cfoTitleEl.textContent = brand.executive_title || `Chief Supply Chain Officer, ${cName}`;
      if (cfoSubEl) {
        cfoSubEl.textContent = `${counts.pillarCount} Core Operating Pillars · ${counts.totalSp} Sub-Pillars · ${counts.pCount} Corporate Roles · ${counts.aCount} AI Agents`;
      }
      document.title = `${dispLabel} — Supply Chain Agentic Transformation`;

      // 6. Re-render All Dynamic Surfaces Safely
      mountTwinContextBar();"""

    new_apply_brand = """      const navDivEl = document.querySelector('.navbar .nav-divider');
      if (navDivEl) navDivEl.style.display = 'none';
      const cscoBadgeEl = document.querySelector('.nav-csco-badge');
      if (cscoBadgeEl) {
        cscoBadgeEl.innerHTML = `
          <span class="sc-twin-nav-lockup">
            <span class="sc-nav-times" aria-hidden="true">&times;</span>
            ${renderAdaptiveTwinLogoBadge(brand)}
            <span class="sc-twin-nav-co">${escTwinHtml(cName)}</span>
            ${divName ? `<span class="sc-twin-nav-div">${escTwinHtml(divName)}</span>` : ''}
          </span>
        `;
      }

      const heroContent = document.querySelector('.hero-content');
      const heroTitleEl = document.querySelector('.hero-title');
      const heroLockup = document.querySelector('.hero-logo-lockup');
      if (heroLockup) heroLockup.style.display = 'none';
      if (heroContent && heroTitleEl) {
        let heroCobrand = document.getElementById('twinHeroCoBrandBanner');
        if (!heroCobrand) {
          heroCobrand = document.createElement('div');
          heroCobrand.id = 'twinHeroCoBrandBanner';
          heroCobrand.className = 'sc-twin-hero-cobrand';
          heroContent.insertBefore(heroCobrand, heroTitleEl);
        }
        heroCobrand.innerHTML = `
          <img data-asset="gemini_enterprise_dark.png" alt="Gemini Enterprise" class="sc-cobrand-gemini-img" />
          <span class="sc-cobrand-times" aria-hidden="true">&times;</span>
          ${renderAdaptiveTwinLogoBadge(brand, 'size-hero')}
          <div style="display:flex; flex-direction:column; gap:2px; padding-left:4px; border-left:1.5px solid var(--border-subtle);">
            <div style="font-family:var(--font-mono); font-size:10.5px; font-weight:800; color:var(--sc-cyan); letter-spacing:0.06em; text-transform:uppercase;">
              ✦ Gemini &times; ${escTwinHtml(cName)}
            </div>
            <div style="font-family:var(--font-display); font-size:17.5px; font-weight:800; color:var(--text-primary); line-height:1.2;">
              ${escTwinHtml(cName)}
            </div>
            ${divName ? `<div style="font-size:12.5px; font-weight:700; color:var(--g-green);">${escTwinHtml(divName)}</div>` : ''}
          </div>
        `;
        heroTitleEl.innerHTML = `Agentic Transformation for <span class="gradient-word">${escTwinHtml(cName)} Supply Chain</span>`;
        if (typeof hydrateAssets === 'function') hydrateAssets();
      }

      const cfoEmblemEl = document.querySelector('.cfo-sc-emblem');
      if (cfoEmblemEl) {
        cfoEmblemEl.classList.add('has-twin-logo');
        cfoEmblemEl.innerHTML = renderAdaptiveTwinLogoBadge(brand, 'size-xl');
      }
      const cfoTitleEl = document.querySelector('.cfo-box-title');
      const cfoSubEl = document.querySelector('.cfo-box-sub');
      if (cfoTitleEl) {
        let kickerEl = document.getElementById('twinCfoCoBrandKicker');
        if (!kickerEl && cfoTitleEl.parentElement) {
          kickerEl = document.createElement('div');
          kickerEl.id = 'twinCfoCoBrandKicker';
          kickerEl.className = 'sc-cfo-cobrand-pill';
          cfoTitleEl.parentElement.insertBefore(kickerEl, cfoTitleEl);
        }
        if (kickerEl) kickerEl.innerHTML = `✦ Gemini &times; ${escTwinHtml(cName)}`;
        cfoTitleEl.textContent = brand.executive_title || `Chief Supply Chain Officer, ${cName}`;
      }
      if (cfoSubEl) {
        cfoSubEl.textContent = `${counts.pillarCount} Core Operating Pillars · ${counts.totalSp} Sub-Pillars · ${counts.pCount} Corporate Roles · ${counts.aCount} AI Agents`;
      }
      const footerTitleEl = document.querySelector('.global-authors-footer span');
      if (footerTitleEl) {
        footerTitleEl.innerHTML = `Gemini Enterprise &times; ${escTwinHtml(cName)} &middot; Supply Chain &amp; Demand`;
      }
      document.title = `Gemini × ${dispLabel} — Supply Chain Agentic Transformation`;

      // 6. Re-render All Dynamic Surfaces Safely
      mountTwinContextBar();
      mountTwinResearchBriefDrawer(twinData, counts);"""

    if old_apply_brand in html:
        html = html.replace(old_apply_brand, new_apply_brand, 1)
    else:
        assert "mountTwinResearchBriefDrawer(twinData, counts);" in html, "Expected applyBrowserTwin branding block in index.html"

    old_reset_brand = """        const cscoBadgeEl = document.querySelector('.nav-csco-badge');
        if (cscoBadgeEl) cscoBadgeEl.textContent = 'Office of the CSCO · Supply Chain';

        const heroLockup = document.querySelector('.hero-logo-lockup');
        if (heroLockup) heroLockup.style.display = '';
        const heroTitleEl = document.querySelector('.hero-title');
        if (heroTitleEl) {
          heroTitleEl.innerHTML = 'Agentic Transformation for <span class="gradient-word">Supply Chain &amp; Demand</span>';
        }

        const cfoEmblemEl = document.querySelector('.cfo-sc-emblem');
        if (cfoEmblemEl && ORIG_CFO_EMBLEM_HTML !== null) {
          cfoEmblemEl.classList.remove('has-twin-logo');
          cfoEmblemEl.innerHTML = ORIG_CFO_EMBLEM_HTML;
        }
        const cfoTitleEl = document.querySelector('.cfo-box-title');
        const cfoSubEl = document.querySelector('.cfo-box-sub');
        if (cfoTitleEl) cfoTitleEl.textContent = 'Chief Supply Chain Officer (CSCO)';
        if (cfoSubEl) cfoSubEl.textContent = '6 Core Operating Pillars · 20 Sub-Pillars · 60 Personas · 60 AI Agents';
        document.title = 'Gemini Enterprise — Supply Chain & Demand (Office of the CSCO)';

        mountTwinContextBar();"""

    new_reset_brand = """        const navDivEl = document.querySelector('.navbar .nav-divider');
        if (navDivEl) navDivEl.style.display = '';
        const cscoBadgeEl = document.querySelector('.nav-csco-badge');
        if (cscoBadgeEl) cscoBadgeEl.textContent = 'Office of the CSCO · Supply Chain';

        const heroLockup = document.querySelector('.hero-logo-lockup');
        if (heroLockup) heroLockup.style.display = '';
        const heroTitleEl = document.querySelector('.hero-title');
        if (heroTitleEl) {
          heroTitleEl.innerHTML = 'Agentic Transformation for <span class="gradient-word">Supply Chain &amp; Demand</span>';
        }

        const cfoEmblemEl = document.querySelector('.cfo-sc-emblem');
        if (cfoEmblemEl && ORIG_CFO_EMBLEM_HTML !== null) {
          cfoEmblemEl.classList.remove('has-twin-logo');
          cfoEmblemEl.innerHTML = ORIG_CFO_EMBLEM_HTML;
        }
        const kickerEl = document.getElementById('twinCfoCoBrandKicker');
        if (kickerEl) kickerEl.remove();
        const briefEl = document.getElementById('twinResearchBriefWrap');
        if (briefEl) briefEl.remove();
        const cfoTitleEl = document.querySelector('.cfo-box-title');
        const cfoSubEl = document.querySelector('.cfo-box-sub');
        if (cfoTitleEl) cfoTitleEl.textContent = 'Chief Supply Chain Officer (CSCO)';
        if (cfoSubEl) cfoSubEl.textContent = '6 Core Operating Pillars · 20 Sub-Pillars · 60 Personas · 60 AI Agents';
        const footerTitleEl = document.querySelector('.global-authors-footer span');
        if (footerTitleEl) {
          footerTitleEl.innerHTML = 'Gemini Enterprise &middot; Supply Chain &amp; Demand (Office of the CSCO)';
        }
        document.title = 'Gemini Enterprise — Supply Chain & Demand (Office of the CSCO)';

        mountTwinContextBar();"""

    if old_reset_brand in html:
        html = html.replace(old_reset_brand, new_reset_brand, 1)
    else:
        assert "const briefEl = document.getElementById('twinResearchBriefWrap');" in html, "Expected switchClientTwin reset branding block in index.html"

    # 12. Re-embed all cleaned `EMBEDDED_TWINS_V2` into `index.html`
    embedded_json_line = "    const EMBEDDED_TWINS_V2 = " + json.dumps(embedded_twins, ensure_ascii=False) + ";"
    html, n_sub = re.subn(
        r"^[ \t]*const EMBEDDED_TWINS_V2 = \{.*?\};$",
        lambda _: embedded_json_line,
        html,
        count=1,
        flags=re.MULTILINE,
    )
    assert n_sub == 1, f"Expected 1 EMBEDDED_TWINS_V2 replacement, got {n_sub}"

    INDEX_HTML.write_text(html, encoding="utf-8")
    print(f"[OK] Upgraded index.html (co-branding, 60+60 stories, research brief drawer, hover/scroll journey, {len(embedded_twins)} embedded twins)")

    # 13. Sync `periodic_table.html`, `mind_map.html`, `docs/`, `zipline_dist/`
    for variant_name, boot_hash in [("periodic_table.html", "periodic"), ("mind_map.html", "mindmap")]:
        v_path = ROOT / variant_name
        head_boot = f"  <script>window.__BOOT_PAGE__ = '{boot_hash}'; if (!window.location.hash) window.location.hash = '#{boot_hash}';</script>\n</head>"
        v_html = html.replace("</head>", head_boot, 1)
        v_path.write_text(v_html, encoding="utf-8")

    for target_dir in [ROOT / "docs", ROOT / "zipline_dist"]:
        if target_dir.exists():
            shutil.copy2(INDEX_HTML, target_dir / "index.html")
            for variant_name in ("periodic_table.html", "mind_map.html"):
                if (target_dir / variant_name).exists() or target_dir.name == "docs":
                    shutil.copy2(ROOT / variant_name, target_dir / variant_name)
            if (target_dir / "data").exists():
                shutil.copy2(CATALOG_JSON, target_dir / "data" / "supply_chain_catalog.json")

    # 14. Refresh primary Zipline / Portal `.zip` bundles if `zipline_dist` exists
    zdist = ROOT / "zipline_dist"
    if zdist.exists():
        primary_zip = ROOT / "Supply_Chain_Agentic_Portal.zip"
        with zipfile.ZipFile(primary_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for item in sorted(zdist.rglob("*")):
                if item.is_file():
                    zf.write(item, item.relative_to(zdist))
        for mirror_zip in (
            "Zipline_Supply_Chain_Agentic_Portal.zip",
            "supply_chain_zipline_bundle.zip",
            "Supply_Chain_Portal_Zipline_Ready.zip",
            "Supply_Chain_Zipline_Upload.zip",
            "Zipline_Supply_Chain_Portal.zip",
        ):
            if (ROOT / mirror_zip).exists() or mirror_zip in ("Zipline_Supply_Chain_Agentic_Portal.zip", "supply_chain_zipline_bundle.zip"):
                shutil.copy2(primary_zip, ROOT / mirror_zip)
        print("[OK] Refreshed Supply_Chain_Agentic_Portal.zip & Zipline mirror bundles")


if __name__ == "__main__":
    p_stories, a_stories = update_catalog_stories()
    embedded = clean_saved_twins_v2()
    update_index_html(p_stories, a_stories, embedded)

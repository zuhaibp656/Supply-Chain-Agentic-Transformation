#!/usr/bin/env python3
"""
Idempotent Clean Modern Polish & Zero-Redundancy Script (v2.9):
  1. Crafts crisp, non-repetitive 1-sentence plain-English stories for all 60 Personas & 60 Agents
     (rendered ONLY once inside `#persona/<id>` and `#agent/<id>`, NEVER duplicated onto outer
     Sub-Pillar selection cards, Directory cards, or flip-card fronts).
  2. Fixes `.persona-cards-grid` CSS (`display: grid; grid-template-columns: repeat(3, minmax(0, 1fr))`)
     and declutters `#subPillarPersonasDrawerEl` so each Persona card shows ONLY its bespoke vector icon,
     clean Persona title, and `→` arrow (zero repeated sub-pillar name, zero paragraph description).
  3. Cleans all saved Company Twin JSON portals (`data/twins/v2/*.json`), stripping robotic
     `"Leads <subpillar> across <company>..."` and `"Operates inside <company>..."` boilerplate,
     redundant `"<Company> · "` pillar prefixes, and dangling conjunctions / `…` truncations.
  4. Streamlines `Gemini × [Company]` co-branding across Hero (`[Gemini Logo] × [Company Logo]`
     without repeating the company name 3 times), Navbar, CSCO Root, Footer, and a compact
     1-line collapsible `✦ Company & Career-Portal Intelligence` drawer—with zero duplicate
     banners or pills on Persona and Agent detail pages.
  5. Declutters `openPersonaPage` and `openAgentPage` (hover auto-expand + 1-click scroll view,
     non-repetitive accordion headers/bodies, single clean Agent story line, clean Demo Studio).
  6. Syncs `periodic_table.html`, `mind_map.html`, `docs/`, `zipline_dist/`, and `.zip` bundles.
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
    (r"\bPOs\b", "Purchase Orders (POs)"),
    (r"\bpos\b", "Point-of-Sale (POS)"),
    (r"\bPOS\b", "Point-of-Sale (POS)"),
    (r"\bsku\b", "SKU"),
    (r"\bskus\b", "SKUs"),
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
    (r"\bocr\b", "OCR"),
    (r"\bedi\b", "EDI"),
    (r"\bgrns\b", "GRNs"),
    (r"\bebols\b", "eBOLs"),
    (r"\bbols\b", "BOLs"),
    (r"\basn\b", "ASN"),
    (r"\bltls\b", "LTLs"),
    (r"\bftl\b", "FTL"),
    (r"\bgps\b", "GPS"),
    (r"\biot\b", "IoT"),
    (r"\bwip\b", "WIP"),
    (r"\bcip\b", "CIP"),
    (r"\bbpr\b", "BPR"),
    (r"\bcoa\b", "COA"),
    (r"\bccp\b", "CCP"),
    (r"\bdc\b", "DC"),
    (r"\binter-dc\b", "inter-DC"),
    (r"\bdte\b", "DTE"),
    (r"\besl\b", "ESL"),
    (r"\bpcr\b", "PCR"),
    (r"\blcas\b", "LCAs"),
    (r"\bbrc/iso\b", "BRC/ISO"),
    (r"\brspo/fsc\b", "RSPO/FSC"),
    (r"\bcbot/platts\b", "CBOT/Platts"),
    (r"\becommerce\b", "e-commerce"),
    (r"\bgoogle maps\b", "Google Maps"),
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

DANGLING_TAIL_RE = re.compile(
    r"(?:,\s*|\s+)(?:and|or|with|to|for|in|by|of|across|including|utilizing|via|through|from|into)\.?$",
    re.IGNORECASE,
)


def fix_infinitive_grammar(text: str) -> str:
    """Fixes robotic 'to detects ...' into natural English."""
    def _repl(m: re.Match) -> str:
        adv = m.group(1) or ""
        verb = m.group(2)
        base = VERB_FIXES.get(verb.lower())
        if base and base != verb.lower():
            return f"to {adv}{base}"
        return m.group(0)

    return re.sub(r"\bto\s+((?:[a-z]+ly\s+)?)([a-z]+s)\b", _repl, text, flags=re.IGNORECASE)


def clean_complete_sentence(text: str, max_len: int = 210, add_period: bool = True) -> str:
    """Ensures text is clean, readable, and never ends in a dangling conjunction or `…`."""
    s = re.sub(r"\s+", " ", str(text or "")).strip()
    s = s.replace(" .", ".").replace(".. —", " —").replace(". —", " —")
    s = fix_infinitive_grammar(s)
    if s.endswith("…") or s.endswith("..."):
        s = re.sub(r"(?:…|\.{3})$", "", s).rstrip(" ,;:-—")
    s = DANGLING_TAIL_RE.sub("", s).rstrip(" ,;:-—")
    if len(s) > max_len:
        window = s[:max_len]
        for sep in (". ", " — ", "; "):
            idx = window.rfind(sep)
            if idx >= int(max_len * 0.48):
                cand = DANGLING_TAIL_RE.sub("", window[:idx].rstrip(".,;:-— "))
                return cand + ("." if add_period and cand and cand[-1] not in ".!?" else "")
        s = window.rsplit(" ", 1)[0].rstrip(".,;:-— ")
        s = DANGLING_TAIL_RE.sub("", s).rstrip(".,;:-— ")
    if add_period and s and s[-1] not in ".!?":
        s += "."
    return s


def build_persona_story(p: dict) -> str:
    """Crafts a single crisp, non-repetitive 1-sentence story (never repeating the Sub-Pillar name above it)."""
    sp_name = p.get("subPillarName") or "supply chain operations"
    mandate = str(p.get("mandate") or "").strip()

    clause = ""
    if ":" in mandate:
        clause = mandate.split(":", 1)[1].strip().rstrip(".")
        # Note: in `contract_po_mgmt`, lowercase `pos` before `, grns` means Purchase Orders (POs)
        clause = re.sub(r"\bpos(?=,\s*grns\b)", "Purchase Orders (POs)", clause)
    for pat, rep in ACRONYM_FIXES:
        clause = re.sub(pat, rep, clause, count=1)

    if clause:
        story = f"{clause[0].upper() + clause[1:]}."
    else:
        story = f"Drives daily {sp_name} decisions across service levels, working capital, and operating cost."

    return clean_complete_sentence(story, 185)


def build_agent_story(ag: dict) -> str:
    """Crafts a crisp 1–2 line summary using `ag.outcome` so it never repeats Card 02 (`ag.solution`)."""
    outcome_d = str(ag.get("outcome") or ag.get("advantage") or ag.get("shortDesc") or "").strip().rstrip(".")
    for pat, rep in ACRONYM_FIXES[:12]:
        outcome_d = re.sub(pat, rep, outcome_d, count=1)

    if outcome_d:
        story = outcome_d[0].upper() + outcome_d[1:] + "."
    else:
        story = f"Continuously monitors live signals and enterprise data to automate {ag.get('name', 'supply chain')} decisions."

    return clean_complete_sentence(story, 195)


def update_catalog_stories() -> tuple[dict, dict]:
    """Updates all 60 Personas and 60 Agents in `data/supply_chain_catalog.json` with crisp 1-sentence stories."""
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
        st = build_persona_story(p)
        p["summary"] = st
        p["story"] = st
        for slot in p.get("dayInLife") or []:
            if slot.get("after"):
                slot["after"] = fix_infinitive_grammar(str(slot["after"]).replace(". —", " —"))
        persona_stories[pid] = st

    CATALOG_JSON.write_text(json.dumps(cat, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[OK] Updated crisp 1–2 line stories for {len(persona_stories)} Personas & {len(agent_stories)} Agents in catalog")
    return persona_stories, agent_stories


def _strip_company_prefix(text: str, prefixes: list[str]) -> str:
    s = str(text or "").strip()
    for pref in prefixes:
        if not pref:
            continue
        for sep in (" · ", " — ", ": "):
            token = f"{pref}{sep}"
            if s.lower().startswith(token.lower()):
                s = s[len(token):].strip()
        tailored_tok = f"Tailored for {pref}: "
        if s.lower().startswith(tailored_tok.lower()):
            s = s[len(tailored_tok):].strip()
    return s


def clean_saved_twins_v2(persona_stories: dict, agent_stories: dict) -> dict:
    """Eliminates robotic template prefixes, mid-sentence ellipses, and duplicate text across `data/twins/v2/*.json`."""
    embedded = {}
    for fp in sorted(TWINS_DIR.glob("*.json")):
        twin = json.loads(fp.read_text(encoding="utf-8"))
        twin["generation_model"] = "Gemini 3.1 Pro / 4 Argon + Gemini 3.8 Flash (Google Search Grounded)"

        brand = twin.get("brand") or {}
        co_prefixes = [
            twin.get("display_label") or "",
            brand.get("canonical_name") or "",
            twin.get("canonical_name") or "",
            twin.get("company_name") or "",
        ]
        if brand.get("executive_thesis"):
            brand["executive_thesis"] = clean_complete_sentence(brand["executive_thesis"], 360)

        for cp in twin.get("custom_pillars") or []:
            if cp.get("tagline"):
                stripped = _strip_company_prefix(cp["tagline"], co_prefixes)
                cp["tagline"] = clean_complete_sentence(stripped or cp.get("name", ""), 95, add_period=False)
            if cp.get("subtitle"):
                stripped_sub = _strip_company_prefix(cp["subtitle"], co_prefixes)
                cp["subtitle"] = clean_complete_sentence(stripped_sub, 165)

        for _, po_pil in (twin.get("pillar_overrides") or {}).items():
            if po_pil.get("custom_tagline"):
                po_pil["custom_tagline"] = clean_complete_sentence(
                    _strip_company_prefix(po_pil["custom_tagline"], co_prefixes), 95, add_period=False
                )
            if po_pil.get("custom_subtitle"):
                po_pil["custom_subtitle"] = clean_complete_sentence(
                    _strip_company_prefix(po_pil["custom_subtitle"], co_prefixes), 165
                )

        for pid, po in (twin.get("persona_overrides") or {}).items():
            raw_sum = str(po.get("summary") or "").strip()
            # Replace cookie-cutter fallback ("Leads <subpillar> across <company>...") with unique role story
            if not raw_sum or (raw_sum.startswith("Leads ") and " across " in raw_sum):
                po["summary"] = persona_stories.get(pid, "")
            else:
                po["summary"] = clean_complete_sentence(raw_sum, 195)
            if po.get("role"):
                po["role"] = _strip_company_prefix(po["role"], co_prefixes).split("·")[0].strip()
            if po.get("manual_toil"):
                po["manual_toil"] = clean_complete_sentence(po["manual_toil"], 230)
            if po.get("agentic_impact"):
                po["agentic_impact"] = clean_complete_sentence(po["agentic_impact"], 230)

        for aid, ar in (twin.get("agent_relevance") or {}).items():
            raw_ctx = str(ar.get("division_context") or "").strip()
            if not raw_ctx or raw_ctx.startswith("Operates inside "):
                ar["division_context"] = ""
            else:
                ar["division_context"] = clean_complete_sentence(raw_ctx, 195)

        fp.write_text(json.dumps(twin, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        slug = twin.get("twin_slug") or fp.stem
        embedded[slug] = twin

    print(f"[OK] Decluttered & normalized {len(embedded)} saved Company Twin JSON portals in data/twins/v2/")
    return embedded


def replace_js_json_const(html: str, decl_prefix: str, updater_fn) -> str:
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
    .persona-cards-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
    }
    @media (max-width: 900px) {
      .persona-cards-grid {
        grid-template-columns: 1fr;
      }
    }
    .sc-twin-hero-cobrand {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      flex-wrap: wrap;
      gap: 16px;
      padding: 12px 24px;
      margin-bottom: 24px;
      border-radius: 999px;
      background: rgba(15, 23, 42, 0.84);
      border: 1.5px solid var(--border-strong);
      backdrop-filter: blur(18px);
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.34), inset 0 1px 0 rgba(255, 255, 255, 0.12);
    }
    html[data-theme="light"] .sc-twin-hero-cobrand {
      background: rgba(255, 255, 255, 0.96);
      border-color: #cbd5e1;
      box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
    }
    .sc-cobrand-gemini-img {
      height: 34px;
      width: auto;
      object-fit: contain;
      display: block;
    }
    html[data-theme="light"] .sc-cobrand-gemini-img {
      filter: invert(1) hue-rotate(180deg);
    }
    .sc-cobrand-times {
      font-family: var(--font-display);
      font-size: 20px;
      font-weight: 800;
      color: var(--sc-cyan);
      opacity: 0.9;
      padding: 0 2px;
      user-select: none;
    }
    .sc-cobrand-div-pill {
      font-size: 12px;
      font-weight: 700;
      color: var(--sc-cyan);
      padding: 4px 11px;
      border-radius: 999px;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.32);
    }
    .sc-nav-times {
      font-family: var(--font-display);
      font-size: 16px;
      font-weight: 800;
      color: var(--sc-cyan);
      margin: 0 4px 0 2px;
      line-height: 1;
    }
    .sc-role-story-line {
      margin: 6px 0 0 0;
      max-width: 700px;
      font-size: 14px;
      line-height: 1.52;
      color: var(--text-secondary);
      font-weight: 500;
    }
    .sc-agent-story-line {
      margin: 6px 0 0 0;
      max-width: 720px;
      font-size: 14px;
      line-height: 1.52;
      color: var(--text-secondary);
      font-weight: 500;
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
      padding: 6px 13px;
      border-radius: 999px;
      font-family: var(--font-sans);
      font-size: 12px;
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
      max-width: 760px;
      margin: 12px auto 2px auto;
      text-align: left;
    }
    .sc-twin-research-summary {
      list-style: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 8px 16px;
      border-radius: 999px;
      background: var(--bg-card);
      border: 1px solid var(--border-strong);
      font-size: 12.5px;
      font-weight: 700;
      color: var(--text-secondary);
      transition: border-color 0.2s ease, color 0.2s ease;
    }
    .sc-twin-research-summary::-webkit-details-marker { display: none; }
    .sc-twin-research-summary:hover {
      border-color: var(--sc-cyan);
      color: var(--text-primary);
    }
    .sc-twin-research-grid {
      margin-top: 10px;
      padding: 18px 20px;
      border-radius: 18px;
      background: var(--bg-card);
      border: 1.5px solid var(--border-strong);
      box-shadow: 0 14px 34px rgba(0, 0, 0, 0.22);
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
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
        btn.innerHTML = next ? '✦ Hover Expand: ON' : '✦ Hover Expand: OFF';
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
        btn.innerHTML = nextExpandAll ? '▴ Collapse All' : '📜 Expand All';
      }
    }

    function getPersonaStory(p) {
      if (!p) return '';
      const s = String(p.summary || p.story || '').trim();
      if (s && !(s.startsWith('Leads ') && s.includes(' across '))) return s;
      return String(p.story || p.mandate || '').trim();
    }

    function getAgentStory(ag) {
      if (!ag) return '';
      if (typeof CURRENT_TWIN !== 'undefined' && CURRENT_TWIN && ag.twinDivisionContext && !String(ag.twinDivisionContext).startsWith('Operates inside ')) {
        return String(ag.twinDivisionContext).trim();
      }
      return String(ag.story || ag.shortDesc || ag.solution || '').trim();
    }

    function mountTwinResearchBriefDrawer(twinData, counts) {
      const existing = document.getElementById('twinResearchBriefWrap');
      if (existing) existing.remove();
      if (!twinData) return;

      const cfoBox = document.querySelector('.cfo-box');
      if (!cfoBox || !cfoBox.parentElement) return;

      const brand = twinData.brand || {};
      const thesis = brand.executive_thesis || '';
      const sites = brand.flagship_sites || '';
      const erps = brand.erp_systems || '';
      const careers = (twinData.career_title_examples || []).slice(0, 6);
      const cites = (twinData.grounding_citations || []).slice(0, 4);
      const modelLabel = twinData.generation_model || 'Gemini 3.1 Pro / 4 Argon + Gemini 3.8 Flash (Google Search Grounded)';

      if (!thesis && !careers.length && !sites) return;

      const wrap = document.createElement('div');
      wrap.id = 'twinResearchBriefWrap';
      wrap.className = 'sc-twin-research-drawer';
      wrap.innerHTML = `
        <details>
          <summary class="sc-twin-research-summary">
            <span>✦ Company &amp; Career-Portal Intelligence</span>
            <span style="color:var(--sc-cyan); font-size:12px;">Expand Brief ▾</span>
          </summary>
          <div class="sc-twin-research-grid">
            <div>
              <div style="font-family:var(--font-mono); font-size:10.5px; font-weight:800; color:var(--sc-cyan); text-transform:uppercase; letter-spacing:0.06em; margin-bottom:6px;">Supply Chain Overview</div>
              <p style="margin:0 0 8px 0; font-size:13px; line-height:1.52; color:var(--text-primary);">${escTwinHtml(thesis)}</p>
              ${sites ? `<div style="font-size:11.8px; color:var(--text-secondary); margin-bottom:4px;"><strong>Nodes:</strong> ${escTwinHtml(sites)}</div>` : ''}
              ${erps ? `<div style="font-size:11.8px; color:var(--text-secondary);"><strong>Stack:</strong> ${escTwinHtml(erps)}</div>` : ''}
            </div>
            <div>
              <div style="font-family:var(--font-mono); font-size:10.5px; font-weight:800; color:var(--sc-cyan); text-transform:uppercase; letter-spacing:0.06em; margin-bottom:6px;">Career-Portal Roles</div>
              <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:10px;">
                ${careers.map(ct => `<span class="sc-twin-term-chip">${escTwinHtml(ct)}</span>`).join('')}
              </div>
              <div style="font-size:11.5px; color:var(--text-secondary); margin-bottom:6px;">
                Synthesized via <strong>${escTwinHtml(modelLabel)}</strong>
              </div>
              ${cites.length ? `
                <div style="display:flex; flex-direction:column; gap:3px; font-size:11.5px;">
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

    # 2. Inject CSS right before `</style>`
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

    # 5. Declutter Front-Page Sub-Pillar Hub & Personas Drawer (`#subPillarPersonasDrawerEl`)
    old_step1_hint = """          <!-- Step 1 Instruction -->
          <div style="font-size:13.5px; font-weight:600; color:var(--text-secondary); margin-bottom:14px;">
            Select a sub-pillar below to view its supply chain personas:
          </div>

"""
    if old_step1_hint in html:
        html = html.replace(old_step1_hint, "", 1)

    old_drawer = """            <div id="subPillarPersonasDrawerEl" class="subpillar-personas-drawer" style="--sp-color: ${activeSubPillar.color}; margin-top: 8px;">
              <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom:16px;">
                <div style="display:flex; align-items:center; gap:10px;">
                  <span style="padding:4px 11px; border-radius:8px; background:${activeSubPillar.color}; color:#ffffff; font-size:11.5px; font-weight:800; letter-spacing:0.05em; text-transform:uppercase;">
                    ${renderSubPillarSvg(activeSubPillar, 15, '#ffffff')} ${activeSubPillar.name}
                  </span>
                  <span style="font-size:14.5px; font-weight:700; color:var(--text-primary);">
                    Select a persona to open their daily journey &amp; AI agents
                  </span>
                </div>
                <button type="button" class="switch-pill" style="padding:4px 12px; font-size:12px;" onclick="selectSubPillarFilter('${activeSubPillar.id}')">
                  ✕ Close Sub-Pillar
                </button>
              </div>

              <div class="persona-cards-grid" style="grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px;">
                ${(activeSubPillar.items || []).map((item, pIdx) => {
                  const p = PERSONAS[item.personaId];
                  if (!p) return '';
                  return `
                    <div class="human-persona-card"
                         style="--dept-accent: ${activeSubPillar.color}; --stagger-idx: ${pIdx}; padding: 20px 22px;"
                         onclick="openPersonaPage('${p.id}', true, event)">
                      <div style="display:flex; align-items:center; gap:14px;">
                        ${renderPersonaIconBadge(p, 48, activeSubPillar.color)}
                        <div>
                          <div class="human-persona-title" style="font-size:17.5px;">${p.name}</div>
                          <div class="human-persona-sub" style="font-size:12.5px; margin-top:2px;">${activeSubPillar.name}</div>
                        </div>
                      </div>
                      <span class="persona-open-arrow" style="color:${activeSubPillar.color}; font-weight:800; font-size:16px;">&rarr;</span>
                    </div>
                  `;
                }).join('')}
              </div>
            </div>"""

    new_drawer = """            <div id="subPillarPersonasDrawerEl" class="subpillar-personas-drawer" style="--sp-color: ${activeSubPillar.color}; margin-top: 8px;">
              <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom:14px;">
                <span style="display:inline-flex; align-items:center; gap:7px; padding:5px 12px; border-radius:8px; background:${activeSubPillar.color}; color:#ffffff; font-size:11.5px; font-weight:800; letter-spacing:0.05em; text-transform:uppercase;">
                  ${renderSubPillarSvg(activeSubPillar, 15, '#ffffff')} ${activeSubPillar.name}
                </span>
                <button type="button" class="switch-pill" style="padding:4px 12px; font-size:12px;" onclick="selectSubPillarFilter('${activeSubPillar.id}')">
                  ✕ Close
                </button>
              </div>

              <div class="persona-cards-grid">
                ${(activeSubPillar.items || []).map((item, pIdx) => {
                  const p = PERSONAS[item.personaId];
                  if (!p) return '';
                  return `
                    <div class="human-persona-card"
                         style="--dept-accent: ${activeSubPillar.color}; --stagger-idx: ${pIdx}; padding: 18px 20px;"
                         onclick="openPersonaPage('${p.id}', true, event)">
                      <div style="display:flex; align-items:center; gap:14px; min-width:0;">
                        ${renderPersonaIconBadge(p, 46, activeSubPillar.color)}
                        <div class="human-persona-title" style="font-size:16.5px; line-height:1.28;">${p.name}</div>
                      </div>
                      <span class="persona-open-arrow" style="color:${activeSubPillar.color}; font-weight:800; font-size:16px; flex-shrink:0;">&rarr;</span>
                    </div>
                  `;
                }).join('')}
              </div>
            </div>"""
    if old_drawer in html:
        html = html.replace(old_drawer, new_drawer, 1)

    # 6. Upgrade `openPersonaPage`: Single Crisp Role Story + Clean Non-Redundant Daily Workflow + Clean Agent Cards
    old_persona_header = """            <div style="position:relative; z-index:2; display:flex; align-items:center; gap:18px; flex-wrap:wrap;">
              ${renderPersonaIconBadge(p, 60, p.subPillarColor || dept.color)}
              <div>
                <h1 class="persona-page-title" style="margin-bottom:4px;">${p.name}</h1>
                <div style="font-size:15px; color:var(--text-secondary); font-weight:600;">${p.subPillarName || dept.name}</div>
              </div>
            </div>"""
    new_persona_header = """            <div style="position:relative; z-index:2; display:flex; align-items:flex-start; gap:18px; flex-wrap:wrap; flex:1; min-width:260px;">
              ${renderPersonaIconBadge(p, 58, p.subPillarColor || dept.color)}
              <div style="min-width:0; flex:1;">
                <h1 class="persona-page-title" style="margin-bottom:3px;">${p.name}</h1>
                <div style="font-size:14px; color:var(--sc-cyan); font-weight:700;">${p.subPillarName || dept.name}</div>
                <p class="sc-role-story-line">${escTwinHtml(getPersonaStory(p))}</p>
              </div>
            </div>"""
    if old_persona_header in html:
        html = html.replace(old_persona_header, new_persona_header, 1)

    old_persona_journey_block = """          <!-- Simple Persona Daily Journey -->
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom: 14px;">
            <div>
              <h2 class="block-title" style="border-left-color: ${dept.color}; margin-bottom:2px;">Persona Daily Journey</h2>
              <p class="block-subtitle" style="margin:0;">Click any daily task below to compare <strong style="color:#ea4335;">Manual Bottleneck (Red)</strong> vs. <strong style="color:#34a853;">With Gemini AI (Green)</strong> and launch the assigned AI Agent.</p>
            </div>
          </div>

          <div style="margin-bottom: 34px;">
            ${p.dayInLife.map((slot, idx) => {
              const stepId = `pStep_${p.id}_${idx}`;
              const plugAgent = slot.agentId ? AGENTS[slot.agentId] : null;
              const plugCls = plugAgent ? getAgentBuildClassification(plugAgent) : null;
              const isDefaultOpen = slot.isToil && !firstToilOpened;
              if (isDefaultOpen) firstToilOpened = true;

              return `
                <div id="${stepId}" class="journey-accordion-item ${isDefaultOpen ? 'open' : ''}" style="--dept-accent:${dept.color};">
                  <button type="button" class="journey-accordion-header" onclick="togglePersonaJourneyStep('${stepId}')">
                    <div style="display:flex; align-items:center; gap:14px; flex-wrap:wrap;">
                      <span class="time-badge" style="min-width:82px;">${slot.time}</span>
                      <span class="task-title" style="font-size:16.5px;">${slot.task}</span>
                      ${slot.isToil ? `
                        <span class="sc-impact-pill-link"
                              onclick="event.stopPropagation(); openProofForPersona('${p.id}', event)"
                              title="View supporting case study &amp; benchmark">
                          ${slot.toilDuration || '2.0 hrs'} &rarr; ${slot.afterDuration || '10 mins'} <span class="sc-impact-cue">&#8599;</span>
                        </span>
                      ` : `
                        <span class="core-tag-pill">👤 ${slot.tag || 'Leadership'}</span>
                      `}
                    </div>

                    <div style="display:flex; align-items:center; gap:10px;">
                      ${plugAgent ? `
                        <span class="ai-agent-type-tag" style="padding:4px 9px; font-size:11px;" onclick="event.stopPropagation(); openAgentPage('${plugAgent.id}', true, event)">
                          ✦ ${plugAgent.name} &rarr;
                        </span>
                      ` : ''}
                      <span class="journey-accordion-chevron">Details ▾</span>
                    </div>
                  </button>

                  <div class="journey-accordion-body">
                    ${slot.isToil ? `
                      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:16px; padding-top:14px;">
                        <div class="toil-highlight-box" style="padding:16px 18px;">
                          <div class="toil-top-bar" style="margin-bottom:8px;">
                            <span class="toil-badge">✕ Manual Bottleneck</span>
                            <span class="toil-duration">⏱ ${slot.toilDuration || '2.0 hrs'}</span>
                          </div>
                          <div class="toil-text">${slot.before}</div>
                        </div>

                        <div class="gemini-improve-box" style="padding:16px 18px;">
                          <div class="improve-top-bar" style="margin-bottom:8px;">
                            <span class="improve-badge">✦ With Gemini AI</span>
                            <button type="button" class="improve-time-saved sc-impact-pill-link" onclick="openProofForPersona('${p.id}', event)" title="View supporting case study &amp; benchmark">⚡ ${slot.toilDuration || '2.0 hrs'} &rarr; ${slot.afterDuration || '10 mins'} <span class="sc-impact-cue">&#8599;</span></button>
                          </div>
                          <div class="improve-text">${slot.after}</div>
                        </div>
                      </div>

                      ${plugAgent ? `
                        <div class="persona-step-agent-box">
                          <div style="display:flex; align-items:center; gap:14px; flex:1; min-width:240px;">
                            ${renderAgentIconBadge(plugAgent, 44, plugAgent.subPillarColor || dept.color)}
                            <div>
                              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:4px;">
                                <span style="font-family:var(--font-display); font-size:16.5px; font-weight:800; color:var(--text-primary);">
                                  ${plugAgent.name}
                                </span>
                                <span class="build-tier-badge ${plugCls.cssClass}">${plugCls.label}</span>
                                ${plugAgent.badge ? `
                                  <button type="button" class="sc-impact-pill-link" style="font-size:11px; padding:2px 9px;"
                                          onclick="event.stopPropagation(); openProofForAgent('${plugAgent.id}', event)"
                                          title="View supporting case study &amp; benchmark">
                                    ${plugAgent.badge} <span class="sc-impact-cue">&#8599;</span>
                                  </button>
                                ` : ''}
                              </div>
                              <div style="font-size:14.5px; color:var(--text-secondary); line-height:1.58;">
                                ${shortSentence(plugAgent.solution || plugAgent.role, 120)}
                              </div>
                            </div>
                          </div>

                          <button type="button" class="agent-plug-btn" style="padding:10px 18px; font-size:13px;" onclick="openAgentPage('${plugAgent.id}', true, event)">
                            <span>Open ${plugAgent.name} &amp; Demo</span>
                            <span>&rarr;</span>
                          </button>
                        </div>
                      ` : ''}
                    ` : `
                      <div style="padding-top:16px; font-size:16px; line-height:1.72; color:var(--text-secondary);">
                        ${slot.activity}
                      </div>
                    `}
                  </div>
                </div>
              `;
            }).join('')}
          </div>

          <!-- Big-Heading Flippable AI Agent Cards for this Persona -->
          <div class="ai-agent-dock-box">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-bottom:16px;">
              <h2 style="font-family:var(--font-display); font-size:22px; font-weight:800; color:var(--text-primary); margin:0;">
                ✦ AI Agents for ${p.name}
              </h2>
              <span style="font-size:12.5px; color:var(--text-secondary); font-weight:600;">
                Click any card to flip for details, or open the Agent Studio
              </span>
            </div>"""

    new_persona_journey_block = """          <!-- Clean Persona Daily Workflow (Hover Auto-Expand + 1-Click Scroll View) -->
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom: 14px;">
            <h2 class="block-title" style="border-left-color: ${dept.color}; margin:0;">Daily Workflow</h2>
            <div class="sc-journey-mode-bar">
              <button type="button" id="btnPersonaHoverMode" class="sc-journey-mode-pill ${isPersonaHoverExpandOn() ? 'is-on' : ''}" onclick="togglePersonaHoverExpandMode('${p.id}')">
                ${isPersonaHoverExpandOn() ? '✦ Hover Expand: ON' : '✦ Hover Expand: OFF'}
              </button>
              <button type="button" id="btnPersonaExpandAll" class="sc-journey-mode-pill ${isPersonaExpandAllOn() ? 'is-on' : ''}" onclick="toggleExpandAllPersonaSteps('${p.id}')">
                ${isPersonaExpandAllOn() ? '▴ Collapse All' : '📜 Expand All'}
              </button>
            </div>
          </div>

          <div style="margin-bottom: 32px;">
            ${p.dayInLife.map((slot, idx) => {
              const stepId = `pStep_${p.id}_${idx}`;
              const plugAgent = slot.agentId ? AGENTS[slot.agentId] : null;
              const plugCls = plugAgent ? getAgentBuildClassification(plugAgent) : null;
              const expandAllNow = isPersonaExpandAllOn();
              const isDefaultOpen = expandAllNow || (slot.isToil && !firstToilOpened);
              if (slot.isToil && !firstToilOpened) firstToilOpened = true;

              return `
                <div id="${stepId}" class="journey-accordion-item ${isDefaultOpen ? 'open' : ''}" style="--dept-accent:${dept.color};" onmouseenter="handlePersonaStepHover('${stepId}')" onmouseleave="cancelPersonaStepHover()">
                  <button type="button" class="journey-accordion-header" onclick="togglePersonaJourneyStep('${stepId}')">
                    <div style="display:flex; align-items:center; gap:14px; flex-wrap:wrap;">
                      <span class="time-badge" style="min-width:82px;">${slot.time}</span>
                      <span class="task-title" style="font-size:16.5px;">${slot.task}</span>
                    </div>

                    <div style="display:flex; align-items:center; gap:10px;">
                      ${slot.isToil ? `
                        <span class="sc-impact-pill-link"
                              onclick="event.stopPropagation(); openProofForPersona('${p.id}', event)"
                              title="View supporting case study &amp; benchmark">
                          ${slot.toilDuration || '2.0 hrs'} &rarr; ${slot.afterDuration || '10 mins'} <span class="sc-impact-cue">&#8599;</span>
                        </span>
                      ` : `
                        <span class="core-tag-pill">${slot.tag || 'Leadership'}</span>
                      `}
                      <span class="journey-accordion-chevron">▾</span>
                    </div>
                  </button>

                  <div class="journey-accordion-body">
                    ${slot.isToil ? `
                      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:16px; padding-top:14px;">
                        <div class="toil-highlight-box" style="padding:16px 18px;">
                          <div class="toil-top-bar" style="margin-bottom:8px;">
                            <span class="toil-badge">✕ Manual Bottleneck</span>
                          </div>
                          <div class="toil-text">${slot.before}</div>
                        </div>

                        <div class="gemini-improve-box" style="padding:16px 18px;">
                          <div class="improve-top-bar" style="margin-bottom:8px;">
                            <span class="improve-badge">✦ With Gemini AI</span>
                          </div>
                          <div class="improve-text">${slot.after}</div>
                        </div>
                      </div>

                      ${plugAgent ? `
                        <div class="persona-step-agent-box" style="padding:12px 16px;">
                          <div style="display:flex; align-items:center; gap:12px; flex:1; min-width:200px;">
                            ${renderAgentIconBadge(plugAgent, 38, plugAgent.subPillarColor || dept.color)}
                            <span style="font-family:var(--font-display); font-size:15.5px; font-weight:800; color:var(--text-primary);">
                              ${cleanAgentName(plugAgent.name)}
                            </span>
                            <span class="build-tier-badge ${plugCls.cssClass}">${plugCls.label}</span>
                          </div>

                          <button type="button" class="agent-plug-btn" style="padding:8px 16px; font-size:12.5px;" onclick="openAgentPage('${plugAgent.id}', true, event)">
                            <span>Open Agent</span>
                            <span>&rarr;</span>
                          </button>
                        </div>
                      ` : ''}
                    ` : `
                      <div style="padding-top:16px; font-size:16px; line-height:1.72; color:var(--text-secondary);">
                        ${slot.activity}
                      </div>
                    `}
                  </div>
                </div>
              `;
            }).join('')}
          </div>

          <!-- Clean Assigned AI Agents Grid (Front: Clean Title & KPI; Back: Crisp 1-2 Line Story) -->
          <div class="ai-agent-dock-box">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-bottom:16px;">
              <h2 style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary); margin:0;">
                Assigned AI Agents
              </h2>
            </div>"""
    if old_persona_journey_block in html:
        html = html.replace(old_persona_journey_block, new_persona_journey_block, 1)

    old_flip_back = """                        <div class="sc-flip-back-text">${shortSentence(ag.solution || ag.role, 135)}</div>"""
    new_flip_back = """                        <div class="sc-flip-back-text">${escTwinHtml(getAgentStory(ag))}</div>"""
    if old_flip_back in html:
        html = html.replace(old_flip_back, new_flip_back, 1)

    # 7. Declutter `openAgentPage`: Single Clean Agent Story Inside Hero, Zero Separate Duplicate Banner, Zero Duplicate Top-Right ROI Pill
    old_ag_banner_fn = """    function renderAgentTwinDivisionBanner(ag) {
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
    new_ag_banner_fn = """    function renderAgentTwinDivisionBanner(ag) {
      return '';
    }"""
    if old_ag_banner_fn in html:
        html = html.replace(old_ag_banner_fn, new_ag_banner_fn, 1)

    old_agent_hero_head = """            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:14px; margin-bottom:20px;">
              <div style="display:flex; align-items:center; gap:15px;">
                ${renderAgentIconBadge(ag, 54, ag.subPillarColor || dept.color)}
                <div>
                  <h1 class="agent-title" style="font-size: clamp(25px, 2.8vw, 34px); margin: 0; line-height: 1.15;">${dispAgentName}</h1>
                  <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-top:5px;">
                    <span style="font-size:14.5px; color:var(--text-secondary); font-weight:700;">${ag.subPillarName || dept.name}</span>
                    ${hasCustomCompanyAgentName ? `
                      <span class="sc-twin-core-engine-chip">Core Engine: ${escTwinHtml(ag.canonicalName)}</span>
                    ` : ''}
                  </div>
                </div>
              </div>
              <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                <button type="button" class="sc-impact-pill-link" style="font-size:13px; padding:8px 14px;"
                        onclick="openProofForAgent('${ag.id}', event)"
                        title="View supporting case study &amp; benchmark">
                  <span>🚀 ${ag.badge || 'Verified ROI'}</span>
                  <span class="sc-impact-cue">&#8599;</span>
                </button>
                <a href="agent_testing_and_video_playbook.html#agent-${ag.id}"
                   style="text-decoration:none; font-size:13px; font-weight:700; padding:8px 15px; border-radius:999px; background:rgba(56,189,248,0.14); color:#38bdf8; border:1.5px solid rgba(56,189,248,0.42);">
                  📋 Test Prompts &amp; Data &rarr;
                </a>
                <span class="build-tier-badge ${cls.cssClass}">${cls.label}</span>
              </div>
            </div>"""

    new_agent_hero_head = """            <div style="display:flex; align-items:flex-start; justify-content:space-between; flex-wrap:wrap; gap:14px; margin-bottom:20px;">
              <div style="display:flex; align-items:flex-start; gap:15px; flex:1; min-width:260px;">
                ${renderAgentIconBadge(ag, 54, ag.subPillarColor || dept.color)}
                <div style="min-width:0; flex:1;">
                  <h1 class="agent-title" style="font-size: clamp(25px, 2.8vw, 34px); margin: 0; line-height: 1.15;">${dispAgentName}</h1>
                  <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-top:4px;">
                    <span style="font-size:14px; color:var(--sc-cyan); font-weight:700;">${ag.subPillarName || dept.name}</span>
                    ${hasCustomCompanyAgentName ? `
                      <span class="sc-twin-core-engine-chip">Core Engine: ${escTwinHtml(ag.canonicalName)}</span>
                    ` : ''}
                  </div>
                  <p class="sc-agent-story-line">${escTwinHtml(getAgentStory(ag))}</p>
                </div>
              </div>
              <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                <a href="agent_testing_and_video_playbook.html#agent-${ag.id}"
                   style="text-decoration:none; font-size:13px; font-weight:700; padding:8px 15px; border-radius:999px; background:rgba(56,189,248,0.14); color:#38bdf8; border:1.5px solid rgba(56,189,248,0.42);">
                  📋 Test Prompts &amp; Data &rarr;
                </a>
                <span class="build-tier-badge ${cls.cssClass}">${cls.label}</span>
              </div>
            </div>"""
    if old_agent_hero_head in html:
        html = html.replace(old_agent_hero_head, new_agent_hero_head, 1)

    old_video_empty = """                      <div class="video-placeholder-stage">
                        <div class="video-placeholder-icon">▶</div>
                        <div style="font-family:var(--font-display); font-size:21px; font-weight:800; color:var(--text-primary);">
                          ${dispAgentName} — Demo Studio
                        </div>
                        <div style="display:flex; gap:10px; margin-top:8px;">"""
    new_video_empty = """                      <div class="video-placeholder-stage">
                        <div class="video-placeholder-icon">▶</div>
                        <div style="display:flex; gap:10px; margin-top:4px;">"""
    if old_video_empty in html:
        html = html.replace(old_video_empty, new_video_empty, 1)

    old_video_bar_title = """              <span style="font-weight:700; color:var(--text-primary);">🎬 Agent Demo Studio — ${dispAgentName}</span>"""
    new_video_bar_title = """              <span style="font-weight:700; color:var(--text-primary);">🎬 Demo Studio</span>"""
    if old_video_bar_title in html:
        html = html.replace(old_video_bar_title, new_video_bar_title, 1)

    old_dir_filler = """            <h1 style="font-family:var(--font-display); font-size:clamp(26px, 2.8vw, 34px); font-weight:800; color:var(--text-primary); margin:0 0 6px;">
              ${currentDirMode === 'agents' ? `${totalAgents} Supply Chain AI Agents` : `${totalPersonas} Supply Chain Personas`}
            </h1>
            <p style="font-size:14.5px; color:var(--text-secondary); margin:0 0 18px;">
              Grouped cleanly by Operating Pillar and Sub-Pillar. Click any ${currentDirMode === 'agents' ? 'AI agent to inspect its workflow diagram & interactive demo' : 'role to inspect their daily Red vs. Green transformation'}.
            </p>"""
    new_dir_filler = """            <h1 style="font-family:var(--font-display); font-size:clamp(26px, 2.8vw, 34px); font-weight:800; color:var(--text-primary); margin:0 0 16px;">
              ${currentDirMode === 'agents' ? `${totalAgents} Supply Chain AI Agents` : `${totalPersonas} Supply Chain Personas`}
            </h1>"""
    if old_dir_filler in html:
        html = html.replace(old_dir_filler, new_dir_filler, 1)

    # 8. Clean, Zero-Redundancy `Gemini × [Company]` Co-Branding in `applyBrowserTwin` & `switchClientTwin('reset')`
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
          ${divName ? `<span class="sc-cobrand-div-pill">${escTwinHtml(divName)}</span>` : ''}
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
      if (cfoTitleEl) cfoTitleEl.textContent = brand.executive_title || `Chief Supply Chain Officer, ${cName}`;
      if (cfoSubEl) {
        cfoSubEl.textContent = `${counts.pillarCount} Core Operating Pillars · ${counts.totalSp} Sub-Pillars · ${counts.pCount} Corporate Roles · ${counts.aCount} AI Agents`;
      }
      const footerTitleEl = document.querySelector('.global-authors-footer span');
      if (footerTitleEl) {
        footerTitleEl.innerHTML = `Gemini Enterprise &times; ${escTwinHtml(cName)} &middot; Supply Chain`;
      }
      document.title = `Gemini × ${dispLabel} — Supply Chain`;

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

    # 9. Re-embed all cleaned `EMBEDDED_TWINS_V2` into `index.html`
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
    print(f"[OK] Upgraded index.html (zero-redundancy cards, 3-col Sub-Pillar drawer, clean Gemini x Company lockup, {len(embedded_twins)} embedded twins)")

    # 10. Sync `periodic_table.html`, `mind_map.html`, `docs/`, `zipline_dist/`
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

    # 11. Refresh primary Zipline / Portal `.zip` bundles
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
    embedded = clean_saved_twins_v2(p_stories, a_stories)
    update_index_html(p_stories, a_stories, embedded)

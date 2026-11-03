"""Intelligent Multi-Stage Supply Chain Research & Portal Synthesis Engine.

Orchestrates:
  1. Official Corporate Logo Download & Optical Framing (`resolve_company_logo`)
  2. Stage 1 — Deep Corporate, Division & Career Job-Board Grounding (`Gemini 3.1 Pro` + `GoogleSearch`)
     Searches public LinkedIn job postings, Naukri listings, corporate `/careers` pages, and annual
     reports via Google Search Grounding to extract authentic division terminology, facilities, ERPs,
     and real organizational job titles.
  3. Stage 2 — Parallel 6-Pillar Persona, Process & Agent Relevance Synthesis (`Gemini 3.8 Flash / 3.1 Pro`)
     Runs 6 concurrent pillar specialists to adapt all 20 Sub-Pillars, all 60 Personas, 4 Cross-Pillar
     Process Journeys, and evaluate all 60 Agents for division relevance (`is_relevant: true/false`),
     hiding genuinely inapplicable agents while keeping canonical demo agent engines 100% intact.
  4. Stage 3 — Zero-Breakage Schema Validation & Multi-Tier Persistence (Memory + Disk + GCS + BigQuery).
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import re
from typing import Any, Callable, Dict, List, Optional, Tuple

from enterprise_twin.schema import (
    AgentRelevanceSpec,
    CompanyBrandSpec,
    GroundingCitation,
    PersonaOverrideSpec,
    PillarOverrideSpec,
    ProcessJourneyOverrideSpec,
    SubPillarOverrideSpec,
    TwinOverlaySpec,
    clamp_brand_hex,
    load_canonical_catalog,
    make_twin_slug,
    validate_and_normalize_overlay,
)
from enterprise_twin.tools.gcp_auth import get_genai_client
from enterprise_twin.tools.logo_resolver import resolve_company_logo

ProgressCallback = Optional[Callable[[Dict[str, Any]], None]]

DEEP_RESEARCH_MODELS = [
    os.environ.get("SC_TWIN_PRO_MODEL", "gemini-3.1-pro-preview"),
    "gemini-3.8-flash",
]
FAST_PILLAR_MODELS = [
    os.environ.get("SC_TWIN_FLASH_MODEL", "gemini-3.8-flash"),
    "gemini-3.1-pro-preview",
]


def _emit(cb: ProgressCallback, pct: int, stage: str, message: str, detail: str = "") -> None:
    if cb:
        try:
            cb({"pct": pct, "stage": stage, "message": message, "detail": detail})
        except Exception:
            pass


def _extract_json_obj(raw_text: str) -> Dict[str, Any]:
    """Robustly extracts a JSON object from LLM text output."""
    if not raw_text:
        return {}
    txt = raw_text.strip()
    txt = re.sub(r"^```(?:json)?\s*", "", txt, flags=re.IGNORECASE)
    txt = re.sub(r"\s*```$", "", txt)
    try:
        return json.loads(txt)
    except Exception:
        m = re.search(r"\{[\s\S]*\}", txt)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                return {}
    return {}


def _call_gemini_with_fallback(
    models: List[str],
    prompt: str,
    use_google_search: bool = False,
    json_mode: bool = False,
    max_tokens: int = 8192,
) -> Tuple[str, List[GroundingCitation], str]:
    """Calls Vertex AI Gemini (`global` endpoint for Gemini 3, fallback `us-central1` for 2.5)."""
    from google.genai import types

    last_err: Optional[Exception] = None
    for model_id in models:
        loc = "global" if model_id.startswith("gemini-3") else "us-central1"
        try:
            client = get_genai_client(location=loc)
            cfg_kwargs: Dict[str, Any] = {
                "max_output_tokens": max_tokens,
                "temperature": 0.25,
            }
            if model_id.startswith("gemini-3"):
                cfg_kwargs["thinking_config"] = types.ThinkingConfig(thinking_level="LOW")
            if use_google_search:
                cfg_kwargs["tools"] = [types.Tool(google_search=types.GoogleSearch())]
            elif json_mode:
                cfg_kwargs["response_mime_type"] = "application/json"

            resp = client.models.generate_content(
                model=model_id,
                contents=prompt,
                config=types.GenerateContentConfig(**cfg_kwargs),
            )
            text = resp.text or ""
            citations: List[GroundingCitation] = []
            try:
                cands = getattr(resp, "candidates", None) or []
                if cands:
                    gm = getattr(cands[0], "grounding_metadata", None)
                    chunks = getattr(gm, "grounding_chunks", None) or []
                    seen_urls = set()
                    for ch in chunks:
                        web = getattr(ch, "web", None)
                        uri = getattr(web, "uri", "") if web else ""
                        title = getattr(web, "title", "") if web else ""
                        if uri and uri not in seen_urls:
                            seen_urls.add(uri)
                            citations.append(GroundingCitation(title=title or uri, url=uri))
            except Exception:
                pass
            if text.strip():
                return text, citations[:12], model_id
        except Exception as e:
            last_err = e
            continue

    raise RuntimeError(f"Gemini synthesis unavailable: {last_err}")


def _stage1_corporate_and_career_dossier(
    company_name: str,
    division_name: str,
    geography: str,
    user_notes: str,
) -> Tuple[Dict[str, Any], List[GroundingCitation], str]:
    """Uses Gemini 3.1 Pro + Google Search Grounding to research division structure & real career titles."""
    target_desc = f"{company_name} ({division_name})" if division_name else company_name
    prompt = f"""You are a Principal Supply Chain Organizational Strategist researching **{target_desc}** (Primary geography: {geography or 'Global'}).
Additional user guidance: {user_notes or 'None'}

Use Google Search to investigate:
1. The exact supply chain, procurement, manufacturing, warehousing, and trade distribution structure of **{target_desc}** (including real division acronyms, plant/factory names, depot/dealer tiers, and ERP/WMS/TMS software stack).
2. Authentic supply chain, planning, procurement, plant operations, logistics, and distribution **job titles** posted by **{company_name}** (especially for **{division_name or 'its core supply chain'}**) on LinkedIn Jobs, Naukri, Glassdoor/AmbitionBox, and official company career pages.
3. The official corporate website domain and primary brand hex colors.
4. Which physical supply chain characteristics apply vs. DO NOT apply to **{target_desc}** (for example: does this division require temperature-controlled cold-chain? Does it sell perishables/food with expiry dates? Does it run consumer retail stores with BOPIS/planograms, or B2B bulk/dealer/distributor channels?).

Return ONLY a valid JSON object matching this exact structure (no markdown commentary outside JSON):
{{
  "canonical_company_name": "Official legal/brand name of the company",
  "division_display_name": "Clean division or business unit name (empty string if enterprise-wide)",
  "official_domain": "example.com",
  "industry_sector": "Specific sector & division classification",
  "brand_accent_hex": "#HEXCODE",
  "brand_secondary_hex": "#HEXCODE",
  "executive_leader_title": "Authentic top supply chain / operations executive title for this company & division",
  "executive_thesis": "2 crisp plain-English sentences describing how this company & division's end-to-end supply chain operates using authentic facilities, channels, and terminology.",
  "flagship_facilities": "4-5 real factories, plants, ports, or distribution hubs separated by ' · '",
  "erp_systems": "Real or industry-authentic ERP / planning / WMS / TMS systems separated by ' · '",
  "terminology_glossary": [
    "Term 1 (e.g., TM&D — Trade Marketing & Distribution)",
    "Term 2",
    "Term 3",
    "Term 4"
  ],
  "discovered_career_titles": [
    "Real job title pattern 1 found in job listings",
    "Real job title pattern 2",
    "Real job title pattern 3",
    "Real job title pattern 4",
    "Real job title pattern 5",
    "Real job title pattern 6"
  ],
  "division_operational_profile": {{
    "has_cold_chain_perishables": false,
    "has_food_expiry_markdowns": false,
    "has_retail_stores_bopis_planograms": false,
    "has_d2c_parcel_ecommerce": false,
    "channel_model_summary": "Brief explanation of physical product & distribution channel model"
  }},
  "process_journeys": {{
    "f2f": {{"title": "Company-authentic Forecast-to-Fulfill name", "subtitle": "1-sentence description"}},
    "o2d": {{"title": "Company-authentic Order-to-Delivery name", "subtitle": "1-sentence description"}},
    "s2p": {{"title": "Company-authentic Source-to-Pay name", "subtitle": "1-sentence description"}},
    "p2r": {{"title": "Company-authentic Returns / Circularity name", "subtitle": "1-sentence description"}}
  }}
}}"""
    raw, citations, used_model = _call_gemini_with_fallback(
        DEEP_RESEARCH_MODELS,
        prompt=prompt,
        use_google_search=True,
        json_mode=False,
        max_tokens=4096,
    )
    parsed = _extract_json_obj(raw)
    if not parsed.get("canonical_company_name"):
        raise RuntimeError("Stage 1 returned incomplete corporate dossier JSON")
    return parsed, citations, used_model


def _stage2_synthesize_single_pillar(
    dept_id: str,
    dept_obj: Dict[str, Any],
    personas_cat: Dict[str, Any],
    agents_cat: Dict[str, Any],
    dossier: Dict[str, Any],
    geography: str,
    user_notes: str,
) -> Dict[str, Any]:
    """Synthesizes Sub-Pillar process names, Persona job titles/toils, and Agent relevance for 1 Pillar."""
    co = dossier.get("canonical_company_name", "Enterprise")
    div = dossier.get("division_display_name", "")
    target_label = f"{co} — {div}" if div else co

    pillar_payload = {
        "dept_id": dept_id,
        "canonical_pillar_name": dept_obj["name"],
        "sub_pillars": [],
    }
    for sp in dept_obj.get("subPillars", []):
        sp_entry = {
            "sub_pillar_id": sp["id"],
            "canonical_sub_pillar_name": sp["name"],
            "pairs": [],
        }
        for it in sp.get("items", []):
            pid = it["personaId"]
            aid = it["agentId"]
            p_meta = personas_cat.get(pid, {})
            a_meta = agents_cat.get(aid, {})
            sp_entry["pairs"].append({
                "persona_id": pid,
                "canonical_persona_name": p_meta.get("name", it.get("personaName", pid)),
                "agent_id": aid,
                "canonical_agent_name": a_meta.get("name", it.get("agentName", aid)),
                "agent_function": it.get("desc", ""),
            })
        pillar_payload["sub_pillars"].append(sp_entry)

    prompt = f"""You are tailoring **Pillar {dept_obj['vNum']}: {dept_obj['name']}** of an Enterprise Supply Chain Portal specifically for **{target_label}** ({geography or 'Global'}).

CORPORATE & CAREER RESEARCH DOSSIER:
{json.dumps(dossier, ensure_ascii=False, indent=2)}

USER GUIDANCE: {user_notes or 'None'}

CANONICAL PILLAR STRUCTURE TO ADAPT:
{json.dumps(pillar_payload, ensure_ascii=False, indent=2)}

STRICT INSTRUCTIONS:
1. **Sub-Pillar Process Names (`custom_name`)**: Rename each sub-pillar (`<= 42 chars`) into the authentic operational process terminology used inside **{target_label}** (for example, if ITC Tobacco calls distribution 'TM&D & Wholesale Dealer Sync' or leaf sourcing 'ILTD Leaf & Packaging Sourcing', use that!). Keep it crisp, plain-English, and executive-ready.
2. **Persona Job Titles (`title`)**: Replace generic SCOR persona names with authentic organizational job titles used at **{target_label}** (reflecting the hierarchy/titles in `discovered_career_titles`, e.g., 'Divisional Manager — TM&D Planning', 'Head of Clinker Grinding & Dispatch', 'Category Procurement Manager — Packaging & Leaf'). Do NOT prepend the company name to every job title—write it like a real corporate org chart title!
3. **Persona Toil & Impact (`manual_toil`, `agentic_impact`, `summary`)**: Write 1 clear, grounded plain-English sentence each (`<= 190 chars`) using **{target_label}**'s real products, plants, channels, and ERP systems. Spell out domain abbreviations on first use if obscure.
4. **Intelligent Agent Relevance Filtering & Optional Domain Agent Naming (`is_relevant`, `custom_agent_name`)**:
   - Set `"is_relevant": false` ONLY when an agent's physical domain genuinely does NOT apply to **{target_label}** (refer to `division_operational_profile`! E.g., hide `cold_chain_auditor` or `food_waste_esg_copilot` for non-refrigerated tobacco, cement, metals, automotive, or industrial machinery; hide `atp_order_promising_agent` / `keep_it_routing_advisor` / `planogram_merchandising_vision_auditor` if the division is pure B2B bulk industrial with zero retail stores/e-commerce; keep at least 5 of the 10 agents in this pillar `true`).
   - For relevant agents (`is_relevant: true`), optionally provide `"custom_agent_name"` (`2–4 words`, `<= 44 chars`) ONLY when **{target_label}**'s domain terminology genuinely makes the agent clearer and more resonant for executives (e.g., `'TM&D WD Demand Sensing'`, `'Rake & Clinker Load Optimizer'`, `'Bonded Depot Case Slotting'`). If the canonical agent name is already crisp and universal, leave `"custom_agent_name": ""`!
   - For relevant agents, also write `"division_context"`: 1 crisp sentence (`<= 160 chars`) explaining how that agent creates value for **{target_label}**.

Return ONLY valid JSON with this exact structure:
{{
  "pillar_tagline": "Short tailored pillar tagline (<= 48 chars)",
  "pillar_subtitle": "1-sentence tailored pillar subtitle (<= 140 chars)",
  "sub_pillars": {{
    "<sub_pillar_id>": "Custom Process Name"
  }},
  "personas": {{
    "<persona_id>": {{
      "title": "Authentic Corporate Job Title",
      "role": "Short 5-9 word operational scope",
      "summary": "1-2 sentence mandate at {target_label}",
      "manual_toil": "1 sentence manual pain point today",
      "agentic_impact": "1 sentence outcome with Gemini AI",
      "grounding_source": "Short note e.g. 'Aligned to {co} Supply Chain / Operations career roles'"
    }}
  }},
  "agents": {{
    "<agent_id>": {{
      "is_relevant": true,
      "custom_agent_name": "Optional 2-4 word tailored agent name or empty string",
      "division_context": "1 sentence explaining how this agent serves {target_label}",
      "hidden_reason": "Empty if relevant, else short reason hidden for division fit"
    }}
  }}
}}"""

    raw, _, _ = _call_gemini_with_fallback(
        FAST_PILLAR_MODELS,
        prompt=prompt,
        use_google_search=False,
        json_mode=True,
        max_tokens=6144,
    )
    return _extract_json_obj(raw)


def synthesize_enterprise_twin_live(
    company_name: str,
    division_name: str = "",
    geography: str = "Global",
    user_notes: str = "",
    custom_logo_input: str = "",
    progress_cb: ProgressCallback = None,
) -> TwinOverlaySpec:
    """Runs the full Search-Grounded Multi-Model ADK pipeline and returns a validated `TwinOverlaySpec`."""
    cat = load_canonical_catalog()
    depts = cat["departments"]
    personas_cat = cat["personas"]
    agents_cat = cat["agents"]

    twin_slug = make_twin_slug(company_name, division_name)
    target_title = f"{company_name} ({division_name})" if division_name else company_name

    _emit(
        progress_cb,
        10,
        "corporate_research",
        f"Researching {target_title} supply chain & career ecosystem...",
        "Querying Google Search Grounding (LinkedIn, Naukri, corporate career portals & annual filings) on Gemini 3.1 Pro",
    )

    dossier, citations, pro_model = _stage1_corporate_and_career_dossier(
        company_name=company_name,
        division_name=division_name,
        geography=geography,
        user_notes=user_notes,
    )

    canonical_co = dossier.get("canonical_company_name") or company_name
    clean_div = dossier.get("division_display_name") if division_name else (dossier.get("division_display_name") or "")
    if division_name and not clean_div:
        clean_div = division_name

    official_domain = dossier.get("official_domain", "")
    accent_hex = clamp_brand_hex(dossier.get("brand_accent_hex", "#38bdf8"), "#38bdf8")
    sec_hex = dossier.get("brand_secondary_hex") or "#1e3a8a"

    _emit(
        progress_cb,
        32,
        "logo_framing",
        f"Downloading & optically framing official {canonical_co} brand mark...",
        f"Domain: {official_domain or 'Wikimedia / Wikidata P154'} · Discovered {len(dossier.get('discovered_career_titles') or [])} career role patterns",
    )

    logo_spec = resolve_company_logo(
        company_name=canonical_co,
        official_domain=official_domain,
        custom_logo_input=custom_logo_input,
        brand_accent=accent_hex,
        brand_secondary=sec_hex,
    )

    _emit(
        progress_cb,
        48,
        "pillar_synthesis",
        f"Tailoring 6 Operating Pillars, 20 Process Names & 60 Job Titles for {canonical_co}...",
        "Running 6 parallel SCOR Pillar specialists to adapt roles, terminology & filter irrelevant agents",
    )

    pillar_results: Dict[str, Dict[str, Any]] = {}
    dept_items = list(depts.items())
    completed_count = 0

    with ThreadPoolExecutor(max_workers=6) as pool:
        future_to_dept = {
            pool.submit(
                _stage2_synthesize_single_pillar,
                d_id,
                d_obj,
                personas_cat,
                agents_cat,
                dossier,
                geography,
                user_notes,
            ): (d_id, d_obj["name"])
            for d_id, d_obj in dept_items
        }
        for fut in as_completed(future_to_dept):
            d_id, d_name = future_to_dept[fut]
            completed_count += 1
            try:
                pillar_results[d_id] = fut.result()
            except Exception as e:
                print(f"[ResearchEngine] Pillar {d_id} synthesis warning: {e}")
                pillar_results[d_id] = {}
            _emit(
                progress_cb,
                48 + int((completed_count / 6.0) * 38),
                "pillar_synthesis",
                f"Synthesized Pillar {completed_count}/6: {d_name}",
                f"Mapped corporate job titles, process labels & division agent relevance for {d_name}",
            )

    # Assemble TwinOverlaySpec
    pillar_overrides: Dict[str, PillarOverrideSpec] = {}
    sub_pillar_overrides: Dict[str, SubPillarOverrideSpec] = {}
    persona_overrides: Dict[str, PersonaOverrideSpec] = {}
    agent_relevance: Dict[str, AgentRelevanceSpec] = {}

    for d_id, d_obj in dept_items:
        pres = pillar_results.get(d_id) or {}
        pillar_overrides[d_id] = PillarOverrideSpec(
            dept_id=d_id,
            custom_name=d_obj["name"],
            custom_tagline=pres.get("pillar_tagline") or d_obj.get("tagline", ""),
            custom_subtitle=pres.get("pillar_subtitle") or d_obj.get("subtitle", ""),
        )
        sp_map = pres.get("sub_pillars") or {}
        p_map = pres.get("personas") or {}
        a_map = pres.get("agents") or {}

        for sp in d_obj.get("subPillars", []):
            sp_id = sp["id"]
            sub_pillar_overrides[sp_id] = SubPillarOverrideSpec(
                sub_pillar_id=sp_id,
                dept_id=d_id,
                canonical_name=sp["name"],
                custom_name=sp_map.get(sp_id) or sp["name"],
            )
            for it in sp.get("items", []):
                pid = it["personaId"]
                aid = it["agentId"]
                p_base = personas_cat.get(pid, {})
                dil0 = (p_base.get("dayInLife") or [{}])[0]
                po_in = p_map.get(pid) or {}
                persona_overrides[pid] = PersonaOverrideSpec(
                    persona_id=pid,
                    dept_id=d_id,
                    sub_pillar_id=sp_id,
                    canonical_name=p_base.get("name", pid),
                    title=po_in.get("title") or p_base.get("name", pid),
                    role=po_in.get("role") or p_base.get("role", sp["name"]),
                    summary=po_in.get("summary") or p_base.get("summary", ""),
                    manual_toil=po_in.get("manual_toil") or dil0.get("before", ""),
                    agentic_impact=po_in.get("agentic_impact") or dil0.get("after", ""),
                    grounding_source=po_in.get("grounding_source") or f"Grounded in {canonical_co} career & ops roles",
                )

                ao_in = a_map.get(aid) or {}
                agent_relevance[aid] = AgentRelevanceSpec(
                    agent_id=aid,
                    dept_id=d_id,
                    sub_pillar_id=sp_id,
                    canonical_name=agents_cat.get(aid, {}).get("name", aid),
                    custom_agent_name=ao_in.get("custom_agent_name") or "",
                    is_relevant=bool(ao_in.get("is_relevant", True)),
                    division_context=ao_in.get("division_context") or "",
                    hidden_reason=ao_in.get("hidden_reason") or "",
                )

    proc_overrides: Dict[str, ProcessJourneyOverrideSpec] = {}
    pj_in = dossier.get("process_journeys") or {}
    for vc_id in ("f2f", "o2d", "s2p", "p2r"):
        if vc_id in pj_in and isinstance(pj_in[vc_id], dict) and pj_in[vc_id].get("title"):
            proc_overrides[vc_id] = ProcessJourneyOverrideSpec(
                vc_id=vc_id,
                custom_title=pj_in[vc_id]["title"],
                custom_subtitle=pj_in[vc_id].get("subtitle", ""),
            )

    brand_spec = CompanyBrandSpec(
        company_name=company_name,
        canonical_name=canonical_co,
        division_name=clean_div,
        twin_slug=twin_slug,
        official_domain=official_domain,
        industry_sector=dossier.get("industry_sector") or "Enterprise Supply Chain",
        geography=geography or "Global",
        brand_accent=accent_hex,
        brand_secondary=sec_hex,
        executive_title=dossier.get("executive_leader_title") or f"Chief Supply Chain Officer, {canonical_co}",
        executive_thesis=dossier.get("executive_thesis") or "",
        flagship_sites=dossier.get("flagship_facilities") or "",
        erp_systems=dossier.get("erp_systems") or "SAP S/4HANA · SAP IBP · Enterprise WMS & TMS",
        logo=logo_spec,
    )

    _emit(
        progress_cb,
        92,
        "integrity_validation",
        "Validating zero-breakage DOM schema & saving to Enterprise Twin Database...",
        "Checking WCAG brand contrast, 6-Pillar balance, persona links & persisting to BigQuery + GCS",
    )

    spec = TwinOverlaySpec(
        twin_slug=twin_slug,
        company_name=company_name,
        canonical_name=canonical_co,
        division_name=clean_div,
        brand=brand_spec,
        pillar_overrides=pillar_overrides,
        sub_pillar_overrides=sub_pillar_overrides,
        persona_overrides=persona_overrides,
        agent_relevance=agent_relevance,
        process_overrides=proc_overrides,
        grounding_citations=citations,
        career_title_examples=(dossier.get("discovered_career_titles") or [])[:8],
        terminology_highlights=(dossier.get("terminology_glossary") or [])[:6],
        generation_model=f"{pro_model} + Gemini 3.8 Flash (Google Search Grounded)",
    )
    return validate_and_normalize_overlay(spec)

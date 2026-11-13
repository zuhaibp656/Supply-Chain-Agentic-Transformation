"""Intelligent Multi-Stage Real-Time Supply Chain Research & Portal Synthesis Engine (`v2.3`).

For ANY company or organization entered by the user, executes real-time research:
  1. Stage 1 — Live Corporate, Operations & Career-Portal Grounding (`Gemini 3.1 Pro / 4 Argon` + `GoogleSearch`
     + Corporate Career Portals, LinkedIn/Naukri/Glassdoor & Wikipedia Signals):
     Researches how the company/division actually operates, discovers its official web domain,
     mines authentic corporate supply chain job titles & facilities, and designs `4` to `8` bespoke
     **Organization-Specific Operating Pillars** partitioning all 20 Supply Chain Sub-Pillars.
  2. Official Corporate Logo Download & Optical Framing (`resolve_company_logo`):
     Uses the discovered `official_domain` + Wikidata P154 + Wikimedia Commons + official site icons
     to download and optically frame the authentic company logo for `Gemini × Company` co-branding.
  3. Stage 2 — Parallel Custom-Pillar Synthesis (`Gemini 3.8 Flash` parallel specialists):
     Runs concurrent specialists across each of the `4`–`8` bespoke Organization Pillars to tailor
     all 20 Sub-Pillar process names, rewrite all 60 Personas with crisp 1–2 line daily stories,
     and evaluate all 60 Core AI Agents with crisp 1–2 line agent value stories.
  4. Stage 3 — Zero-Breakage Schema Validation & Multi-Tier Persistence.
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
    CustomPillarSpec,
    GroundingCitation,
    JobDescriptionProofItem,
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
from enterprise_twin.tools.gcp_auth import get_genai_clients
from enterprise_twin.tools.logo_resolver import resolve_company_logo
from enterprise_twin.tools.public_web_career_miner import (
    fetch_wikipedia_company_summary,
    mine_public_job_descriptions,
    search_public_career_titles,
)

ProgressCallback = Optional[Callable[[Dict[str, Any]], None]]


def _normalize_model_id(raw: str, default_id: str) -> str:
    m = (raw or "").strip()
    if not m or m in ("gemini-3.8-flash", "gemini-3.7-flash", "gemini-3-pro-preview"):
        return default_id
    return m


DEEP_RESEARCH_MODELS = [
    _normalize_model_id(os.environ.get("SC_TWIN_PRO_MODEL", ""), "gemini-3.1-pro-preview"),
    "gemini-2.5-pro",
    "gemini-3-flash-preview",
    "gemini-2.5-flash",
]

FAST_PILLAR_MODELS = [
    _normalize_model_id(os.environ.get("SC_TWIN_FLASH_MODEL", ""), "gemini-3-flash-preview"),
    "gemini-2.5-flash",
    "gemini-3.1-pro-preview",
]

ALL_20_SUBPILLAR_IDS = [
    "demand_forecasting", "trade_promotion", "sop_ibp", "portfolio_sku",
    "supplier_network", "material_packaging", "contract_po",
    "production_scheduling", "capacity_planning", "quality_compliance",
    "positioning_optimization", "warehouse_operations", "omnichannel_visibility",
    "first_mid_mile", "store_replenishment", "last_mile_delivery", "route_carrier",
    "returns_claims", "expiry_markdowns", "pallet_tote",
]

SUBPILLAR_ALIASES = {
    "contract_po_mgmt": "contract_po",
    "returns_claims_mgmt": "returns_claims",
    "pallet_tote_reclamation": "pallet_tote",
}


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
    fast_thinking: bool = False,
) -> Tuple[str, List[GroundingCitation], str]:
    """Calls Gemini across available auth clients (`gemini_api_key` / `vertex_iam`) and fallback models."""
    from google.genai import types

    last_err: Optional[Exception] = None
    seen_models: List[str] = []
    for m in models:
        if m and m not in seen_models:
            seen_models.append(m)

    for model_id in seen_models:
        loc = "global" if model_id.startswith("gemini-3") else "us-central1"
        client_candidates = get_genai_clients(location=loc, timeout_ms=80_000)
        for auth_label, client in client_candidates:
            try:
                cfg_kwargs: Dict[str, Any] = {
                    "max_output_tokens": max_tokens,
                    "temperature": 0.25,
                }
                if model_id.startswith("gemini-3"):
                    lvl = "MINIMAL" if (fast_thinking and "flash" in model_id) else "LOW"
                    try:
                        cfg_kwargs["thinking_config"] = types.ThinkingConfig(thinking_level=lvl)
                    except Exception:
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
                    return text, citations[:12], f"{model_id} ({auth_label})"
            except Exception as e:
                last_err = e
                continue

    raise RuntimeError(f"Gemini live synthesis unavailable: {last_err}")


def _normalize_org_pillars_partition(raw_pillars: Any, company_label: str) -> List[Dict[str, Any]]:
    """Ensures `organization_pillars` has 4 to 8 bespoke pillars partitioning all 20 canonical sub-pillars."""
    from enterprise_twin.schema import EXECUTIVE_PILLAR_PALETTE, ensure_distinct_pillar_colors

    valid_set = set(ALL_20_SUBPILLAR_IDS)
    palette = EXECUTIVE_PILLAR_PALETTE
    watermarks = ["demand_wave", "supplier_graph", "factory_arm", "warehouse_rack", "corridor_lifo", "conveyor_rack"]

    cleaned: List[Dict[str, Any]] = []
    assigned: set[str] = set()

    if isinstance(raw_pillars, list):
        for idx, p in enumerate(raw_pillars[:8]):
            if not isinstance(p, dict) or not str(p.get("name") or "").strip():
                continue
            sp_list: List[str] = []
            for raw_sp in (p.get("sub_pillar_ids") or []):
                s = SUBPILLAR_ALIASES.get(str(raw_sp).strip(), str(raw_sp).strip())
                if s in valid_set and s not in assigned:
                    sp_list.append(s)
                    assigned.add(s)
            wm = str(p.get("watermark_type") or "").strip()
            if wm not in watermarks:
                wm = watermarks[idx % len(watermarks)]
            col = clamp_brand_hex(str(p.get("color") or ""), palette[idx % len(palette)])
            badge = str(p.get("scor_badge") or "").strip()
            if not badge or "·" not in badge:
                short_w = str(p["name"]).split(",")[0].split("&")[0].strip().upper()[:18]
                badge = f"{len(cleaned) + 1:02d} · {short_w}"
            else:
                badge = f"{len(cleaned) + 1:02d} · {badge.split('·', 1)[1].strip()[:20].upper()}"

            raw_signals = p.get("company_evidence_signals") or []
            clean_signals = [str(x).strip()[:140] for x in raw_signals if str(x).strip()][:5]
            raw_jds = p.get("jd_proof_items") or []
            clean_jds: List[Dict[str, str]] = []
            for rj in raw_jds[:3]:
                if isinstance(rj, dict) and str(rj.get("job_title") or "").strip():
                    clean_jds.append({
                        "job_title": str(rj["job_title"]).strip()[:115],
                        "internal_org_unit": str(rj.get("internal_org_unit") or p["name"]).strip()[:120],
                        "process_clues_from_jd": str(rj.get("process_clues_from_jd") or "").strip()[:440],
                        "jd_verification_url": str(rj.get("jd_verification_url") or "").strip(),
                        "live_search_url": str(rj.get("live_search_url") or "").strip(),
                    })
            raw_sources = p.get("verification_sources") or []
            clean_sources: List[Dict[str, str]] = []
            for rs in raw_sources[:4]:
                if isinstance(rs, dict) and str(rs.get("url") or "").startswith("http"):
                    clean_sources.append({
                        "title": str(rs.get("title") or rs["url"]).strip()[:110],
                        "url": str(rs["url"]).strip(),
                        "snippet": str(rs.get("snippet") or "").strip()[:180],
                    })

            cleaned.append({
                "pillar_id": re.sub(r"[^a-z0-9_]+", "_", str(p.get("pillar_id") or f"pillar_{len(cleaned)+1}").lower()).strip("_") or f"pillar_{len(cleaned)+1}",
                "scor_badge": badge,
                "name": str(p["name"]).strip()[:54],
                "tagline": str(p.get("tagline") or f"{company_label} · {p['name']}").strip()[:84],
                "subtitle": str(p.get("subtitle") or "").strip()[:175],
                "color": col,
                "watermark_type": wm,
                "sub_pillar_ids": sp_list,
                "pillar_naming_basis": str(p.get("pillar_naming_basis") or "").strip()[:400],
                "provenance_rationale": str(p.get("provenance_rationale") or "").strip()[:420],
                "company_evidence_signals": clean_signals,
                "jd_proof_items": clean_jds,
                "verification_sources": clean_sources,
            })

    if len(cleaned) < 4:
        return []

    missing = [s for s in ALL_20_SUBPILLAR_IDS if s not in assigned]
    for idx, m_sp in enumerate(missing):
        target_p = min(cleaned, key=lambda x: len(x["sub_pillar_ids"]))
        target_p["sub_pillar_ids"].append(m_sp)

    non_empty = [c for c in cleaned if c["sub_pillar_ids"]]
    if len(non_empty) >= 4:
        non_empty = non_empty[:8]
        distinct_cols = ensure_distinct_pillar_colors([c["color"] for c in non_empty])
        for i, c in enumerate(non_empty):
            tail = c["scor_badge"].split("·", 1)[1].strip() if "·" in c["scor_badge"] else "OPERATIONS"
            c["scor_badge"] = f"{i + 1:02d} · {tail}"
            c["color"] = distinct_cols[i]
        return non_empty
    return []


def _stage1_corporate_and_career_dossier(
    company_name: str,
    division_name: str,
    geography: str,
    user_notes: str,
    wiki_hint: Dict[str, Any],
    career_hints: List[str],
    jd_snippets: Optional[List[Dict[str, str]]] = None,
) -> Tuple[Dict[str, Any], List[GroundingCitation], str]:
    """Uses Gemini 3.1 Pro + Google Search Grounding for deep real-time company, career-team & JD research."""
    target_desc = f"{company_name} ({division_name})" if division_name else company_name
    wiki_ctx = ""
    if wiki_hint.get("extract"):
        wiki_ctx = f"\nVerified Corporate Reference ({wiki_hint.get('canonical_title', company_name)}): {wiki_hint['extract'][:500]}"
    if career_hints:
        wiki_ctx += f"\nPublic Job Postings Spotted: {', '.join(career_hints[:6])}"
    if jd_snippets:
        wiki_ctx += "\nLive Public Job Description Excerpts Spotted:\n" + "\n".join(
            f"  - {j['job_title']} ({j['url']}): {j['snippet']}" for j in jd_snippets[:6]
        )

    prompt = f"""You are a Chief Supply Chain & Enterprise Operations Strategist conducting forensic real-time research into **{target_desc}** (Geography: {geography or 'Global'}).
Additional user context: {user_notes or 'None'}{wiki_ctx}

Use Google Search to investigate **{target_desc}**'s official Supply Chain Careers portal (`careers.<domain>`), live Job Descriptions (JDs) on LinkedIn/Naukri/Workday/TalentBrew, and Integrated Annual Reports:
1. **How {target_desc} Actually Names Its Internal Supply Chain Teams & Runs Operations**:
   - Search specifically for `{company_name} supply chain careers teams`, `{company_name} supply chain job description SAP`, and `{company_name} annual report operations supply chain`.
   - Extract the **VERBATIM internal department/team names** used by **{target_desc}** (for example: Unilever's Career Portal explicitly names `Planning`, `Procurement`, `Manufacturing & Engineering (Sourcing Units / UMS)`, `Logistics (LOP)`, `Customer Operations`, and `Quality (QMS) / SHE`; Amazon names `Supply Chain Optimization Technologies (SCOT)`, `Amazon Fulfillment Technologies (AFT)`, `Amazon Transportation Services (ATS)`, `Amazon Logistics (AMZL)`; ITC names `India Leaf Tobacco Division (ILTD)`, `e-Choupal`, `Integrated Consumer Goods Manufacturing & Logistics (ICML)`, `Trade Marketing & Distribution (TM&D)`).
2. **Design `5` to `7` Operating Pillars (`organization_pillars`) — ANCHORED STRICTLY IN VERBATIM INTERNAL TEAMS & JOB DESCRIPTIONS**:
   - **NEVER invent generic or poetic AI labels** (like "FMCG Demand & Brand Portfolio Strategy")! Every pillar `name` MUST be anchored directly to **{target_desc}**'s real internal career-portal teams, operating units, or job-requisition business functions!
   - **SOLID, NON-DERIVED PROOF PER PILLAR (MANDATORY)**:
     * `pillar_naming_basis`: Cite the **exact official team name, Career Portal category, Job Posting Business Function, or Annual Report Operating Unit** that justifies this exact pillar name.
     * `jd_proof_items`: Provide 1–2 real **{target_desc}** Supply Chain / Operations job postings for THIS specific pillar (`job_title`, `internal_org_unit`, `process_clues_from_jd`, `jd_verification_url`), detailing the **insider processes, internal acronyms, and ERP/APS/WMS tools** (e.g., SAP APO/S1P/MM/SD/EWM, Kinaxis, Blue Yonder, Manhattan WMS) written by hiring managers in the JD!
     * `provenance_rationale`: 2–3 concrete sentences explaining how **{target_desc}** runs this pillar across its real plants, warehouses, and channels.
     * `company_evidence_signals`: 3–4 concrete, real **{target_desc}** plants, subsidiaries, systems, or programs for this pillar.
     * `verification_sources`: **1–3 DISTINCT, PILLAR-SPECIFIC HTTPS URLs** (e.g., the specific career team page, specific JD URL, or specific operational deep-dive page for THIS pillar — **NEVER copy-paste the exact same generic homepage URLs across all pillars!**).
   - Partition ALL 20 functional `sub_pillar_ids` ({json.dumps(ALL_20_SUBPILLAR_IDS)}) across your `5` to `7` `organization_pillars` so each of the 20 IDs appears once.
   - Choose `watermark_type` for each pillar from: `["demand_wave", "supplier_graph", "factory_arm", "warehouse_rack", "corridor_lifo", "conveyor_rack"]`.
3. **Real Corporate Website Domain & Career-Portal Job Titles**:
   - Find the exact `official_domain` (e.g. `"unilever.com"`, `"asianpaints.com"`, `"wipro.com"`, `"pfizer.com"`).
   - Extract `6` to `8` authentic supply chain, procurement, planning, manufacturing, or logistics job titles hired by **{target_desc}**.
4. **Physical & Channel Relevance Profile (`division_operational_profile`)**:
   - Accurately flag which physical traits DO vs. DO NOT apply (refrigerated cold-chain perishables, grocery food expiry markdowns, brick-and-mortar retail store planograms, D2C parcel e-commerce).
5. **CRITICAL MANDATE — DIVISION CANONICALIZATION, EXPANDED ABBREVIATIONS & NO FABRICATED NUMBERS**:
   - Return the OFFICIAL formal corporate subsidiary/division name with all acronyms spelled out in `canonical_division_name`.
   - Always spell out domain acronyms on first use (e.g. 'Unilever Manufacturing System (UMS)', 'Trade Marketing & Distribution (TM&D)', 'On-Time In-Full (OTIF)').
   - NEVER fabricate or guess internal dollar/currency savings or unverified KPI numbers!

Return ONLY a valid JSON object matching this exact structure (no markdown commentary outside JSON):
{{
  "canonical_company_name": "Official brand/legal name of the company",
  "canonical_division_name": "Official formal division/subsidiary name with all acronyms spelled out (or empty string if not applicable)",
  "division_display_name": "Concise official business scope display name",
  "official_domain": "companydomain.com",
  "industry_sector": "Specific industry & operational classification",
  "brand_accent_hex": "#HEXCODE",
  "brand_secondary_hex": "#HEXCODE",
  "executive_leader_title": "Authentic top Supply Chain / Operations / Procurement executive title at this company",
  "executive_thesis": "2 crisp plain-English sentences telling the story of how this company's end-to-end supply chain & operations run using real hubs, vendors, channels, and terminology.",
  "architecture_methodology_note": "2-3 sentences explaining how these Operating Pillars map directly to the company's official Career-Portal Supply Chain teams, hiring-manager Job Descriptions (JDs), and disclosed operating units.",
  "flagship_facilities": "4-5 real plants, integration centers, hubs, campuses, or distribution regions separated by ' · '",
  "erp_systems": "Real ERP / sourcing / planning / WMS / TMS stack cited in company JDs separated by ' · '",
  "terminology_glossary": [
    "Term 1 — Plain-English meaning at this company",
    "Term 2 — Plain-English meaning",
    "Term 3 — Plain-English meaning",
    "Term 4 — Plain-English meaning"
  ],
  "discovered_career_titles": [
    "Authentic corporate job title 1",
    "Authentic corporate job title 2",
    "Authentic corporate job title 3",
    "Authentic corporate job title 4",
    "Authentic corporate job title 5",
    "Authentic corporate job title 6"
  ],
  "organization_pillars": [
    {{
      "pillar_id": "bespoke_snake_slug",
      "scor_badge": "01 · OFFICIAL TEAM TAG",
      "name": "Official Internal Team / Operating Pillar Name (<= 48 chars)",
      "tagline": "Specific scope tagline (<= 72 chars)",
      "subtitle": "1 crisp sentence explaining what this pillar runs at this company (<= 155 chars)",
      "color": "#2563eb",
      "watermark_type": "demand_wave",
      "sub_pillar_ids": ["demand_forecasting", "sop_ibp", "portfolio_sku"],
      "pillar_naming_basis": "Exact Career-Portal team name, JD Business Function, or Annual Report Operating Unit this pillar is named after.",
      "provenance_rationale": "2-3 concrete sentences explaining how this team operates across real facilities and channels.",
      "company_evidence_signals": [
        "Real company plant / division / internal system 1",
        "Real company program / logistics network 2",
        "Real company channel / sourcing model 3"
      ],
      "jd_proof_items": [
        {{
          "job_title": "Exact Job Title Posted by Company for This Pillar",
          "internal_org_unit": "Exact Department / Business Function in JD",
          "process_clues_from_jd": "2 sentences summarizing the internal workflows, ERP/APS modules, and operational cadences disclosed in this JD.",
          "jd_verification_url": "https://careers.companydomain.com/..."
        }}
      ],
      "verification_sources": [
        {{"title": "Specific Career Team / Operational Deep-Dive Page for This Pillar", "url": "https://careers.companydomain.com/supply-chain"}}
      ]
    }}
  ],
  "division_operational_profile": {{
    "has_cold_chain_perishables": false,
    "has_food_expiry_markdowns": false,
    "has_retail_stores_bopis_planograms": false,
    "has_d2c_parcel_ecommerce": false,
    "channel_model_summary": "1 sentence describing physical goods/assets & fulfillment channels"
  }},
  "process_journeys": {{
    "f2f": {{"title": "Company-specific Forecast-to-Fulfill workflow title", "subtitle": "1-sentence description"}},
    "o2d": {{"title": "Company-specific Order-to-Delivery workflow title", "subtitle": "1-sentence description"}},
    "s2p": {{"title": "Company-specific Source-to-Pay workflow title", "subtitle": "1-sentence description"}},
    "p2r": {{"title": "Company-specific Returns / Asset Circularity workflow title", "subtitle": "1-sentence description"}}
  }}
}}"""

    raw, citations, used_model = _call_gemini_with_fallback(
        DEEP_RESEARCH_MODELS,
        prompt=prompt,
        use_google_search=True,
        json_mode=False,
        max_tokens=8192,
        fast_thinking=False,
    )
    parsed = _extract_json_obj(raw)
    if not parsed.get("canonical_company_name"):
        raise RuntimeError(f"Stage 1 returned incomplete corporate dossier JSON (len={len(raw)})")
    return parsed, citations, used_model


def _stage2_synthesize_pillar_group(
    pillar_idx: int,
    pillar_meta: Dict[str, Any],
    assigned_subpillars: List[Dict[str, Any]],
    personas_cat: Dict[str, Any],
    agents_cat: Dict[str, Any],
    dossier: Dict[str, Any],
    geography: str,
    user_notes: str,
) -> Dict[str, Any]:
    """Tailors Sub-Pillars, Corporate Job Personas, and Agent Relevance for 1 custom Organization Pillar."""
    co = dossier.get("canonical_company_name", "Enterprise")
    div = dossier.get("division_display_name", "")
    target_label = f"{co} — {div}" if div else co

    group_payload = {
        "pillar_id": pillar_meta["pillar_id"],
        "pillar_name": pillar_meta["name"],
        "pillar_subtitle": pillar_meta.get("subtitle", ""),
        "sub_pillars": [],
    }
    for sp in assigned_subpillars:
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
        group_payload["sub_pillars"].append(sp_entry)

    compact_dossier = {
        "company": target_label,
        "industry_sector": dossier.get("industry_sector"),
        "executive_thesis": dossier.get("executive_thesis"),
        "flagship_facilities": dossier.get("flagship_facilities"),
        "erp_systems": dossier.get("erp_systems"),
        "terminology_glossary": dossier.get("terminology_glossary"),
        "discovered_career_titles": dossier.get("discovered_career_titles"),
        "division_operational_profile": dossier.get("division_operational_profile"),
    }

    prompt = f"""You are tailoring **Operating Pillar {pillar_idx + 1} ({pillar_meta['name']})** of a bespoke Supply Chain & Operations Portal for **{target_label}** ({geography or 'Global'}).

COMPANY RESEARCH DOSSIER:
{json.dumps(compact_dossier, ensure_ascii=False, indent=2)}

USER GUIDANCE: {user_notes or 'None'}

ASSIGNED SUB-PILLARS, PERSONAS & CORE AI AGENTS TO ADAPT:
{json.dumps(group_payload, ensure_ascii=False, indent=2)}

CRITICAL INSTRUCTIONS:
1. **Every Sub-Pillar Must Be Renamed (`sub_pillars`)**:
   - Rewrite EVERY `sub_pillar_id` into authentic process terminology (`<= 42 chars`) used inside **{target_label}** (never leave generic textbook names if **{target_label}** has specific domain operations!).
2. **Every Persona Must Become a Real Corporate Job Role with a 1–2 Line Human Story (`personas`)**:
   - Rewrite EVERY `persona_id`'s `title` into an authentic corporate org-chart job title that exists at **{co}** (aligned with `discovered_career_titles`, e.g., `'Global Head — Server & ODM Strategic Sourcing'`, `'Regional Manager — Tint & Depot Replenishment'`, `'Director — Cold-Chain GDP Logistics'`). Do NOT leave the canonical SCOR persona title unchanged, and do NOT just prefix `{co}` in front of a generic title!
   - Write `summary` (`1–2 crisp plain-English sentences, <= 230 chars`) telling the clear story of what this person actually does every day at **{target_label}** without dense jargon.
   - Write `manual_toil` and `agentic_impact` (`1 crisp plain-English sentence each, <= 190 chars`) referencing **{target_label}**'s real workflows, assets, facilities, and ERP systems.
   - **STRICT NUMBER GUARDRAIL**: NEVER invent or claim unverified company-specific dollar/rupee/euro savings (like `$50M` or `₹120 Cr`) or internal company KPIs! Keep impact statements strictly qualitative or use defensible generic percentage ranges (e.g., `15%–30% faster cycle time`) and never mention other companies!
3. **Reuse & Filter the Fixed Pool of Core AI Agents with a 1–2 Line Agent Story (`agents`)**:
   - Do NOT invent new agent IDs—evaluate each provided `agent_id`:
   - Set `"is_relevant": false` when an agent's physical domain genuinely does NOT apply to **{target_label}** according to `division_operational_profile` (for example, set `false` on `cold_chain_auditor` or `food_waste_esg_copilot` for non-food/non-cold-chain companies like IT/tech, cement, paints, automotive, metals, apparel, or industrial equipment; set `false` on grocery/store-aisle agents like `planogram_merchandising_vision_auditor` or `aisle_aligned_pallet_agent` for B2B enterprises without retail stores; keep at least 60% of agents in this pillar `true`).
   - Keep `"custom_agent_name": ""` when the canonical agent name already works cleanly, OR provide a crisp `2–4 word` domain agent name (`<= 42 chars`) when domain wording makes it much clearer for **{co}** leaders.
   - Write `"division_context"` (`1–2 crisp plain-English sentences, <= 210 chars`) telling the clear story of what this AI agent does for **{target_label}** without inventing unverified dollar figures.

Return ONLY valid JSON matching this exact structure:
{{
  "sub_pillars": {{
    "<sub_pillar_id>": "Company-Specific Sub-Pillar Name"
  }},
  "personas": {{
    "<persona_id>": {{
      "title": "Authentic Corporate Job Title",
      "role": "Concise 5-9 word operational mandate",
      "summary": "1-2 sentence plain-English story of what this person does every day at {target_label}",
      "manual_toil": "1-sentence manual bottleneck today at {co} (no fabricated dollar numbers)",
      "agentic_impact": "1-sentence transformation with this AI agent (generic % range or workflow outcome only)",
      "grounding_source": "Grounded in {co} career portals & supply chain roles"
    }}
  }},
  "agents": {{
    "<agent_id>": {{
      "is_relevant": true,
      "custom_agent_name": "",
      "division_context": "1-2 sentence plain-English story of what this AI agent does for {target_label}",
      "hidden_reason": ""
    }}
  }}
}}"""

    raw, _, _ = _call_gemini_with_fallback(
        FAST_PILLAR_MODELS,
        prompt=prompt,
        use_google_search=False,
        json_mode=True,
        max_tokens=8192,
        fast_thinking=True,
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
    """Executes real-time web-researched company portal synthesis (`Gemini 3.1 Pro / 4 Argon` + `GoogleSearch` + `Gemini 3.8 Flash`)."""
    cat = load_canonical_catalog()
    depts = cat["departments"]
    personas_cat = cat["personas"]
    agents_cat = cat["agents"]

    # Map canonical sub-pillars & parent depts
    sp_lookup: Dict[str, Dict[str, Any]] = {}
    sp_parent_dept: Dict[str, str] = {}
    for d_id, d_obj in depts.items():
        for sp in d_obj.get("subPillars", []):
            sp_lookup[sp["id"]] = sp
            sp_parent_dept[sp["id"]] = d_id

    twin_slug = make_twin_slug(company_name, division_name)
    target_title = f"{company_name} ({division_name})" if division_name else company_name

    _emit(
        progress_cb,
        10,
        "corporate_research",
        f"Researching {target_title} supply chain, facilities & career portals...",
        "Running live Google Search Grounding + LinkedIn/Naukri/corporate career mining on Gemini 3.1 Pro / 4 Argon",
    )

    # Fetch lightweight Wikipedia + public job titles + live JD excerpts in parallel while preparing Stage 1
    with ThreadPoolExecutor(max_workers=3) as pre_pool:
        fut_wp = pre_pool.submit(fetch_wikipedia_company_summary, company_name, division_name)
        fut_jobs = pre_pool.submit(search_public_career_titles, company_name, division_name)
        fut_jds = pre_pool.submit(mine_public_job_descriptions, company_name, division_name)
        try:
            wiki_hint = fut_wp.result(timeout=6.0)
        except Exception:
            wiki_hint = {}
        try:
            career_hints = fut_jobs.result(timeout=6.0)
        except Exception:
            career_hints = []
        try:
            jd_snippets = fut_jds.result(timeout=6.5)
        except Exception:
            jd_snippets = []

    _emit(
        progress_cb,
        20,
        "corporate_research",
        f"Synthesizing bespoke Operating Pillars & career dossier for {target_title}...",
        "Analyzing annual filings, Supply Chain career teams & live Job Descriptions (JDs) via Google Search",
    )

    dossier, citations, pro_model = _stage1_corporate_and_career_dossier(
        company_name=company_name,
        division_name=division_name,
        geography=geography,
        user_notes=user_notes,
        wiki_hint=wiki_hint,
        career_hints=career_hints,
        jd_snippets=jd_snippets,
    )

    canonical_co = dossier.get("canonical_company_name") or wiki_hint.get("canonical_title") or company_name
    clean_div = (dossier.get("canonical_division_name") or division_name or dossier.get("division_display_name") or "").strip()
    disp_label = f"{canonical_co} — {clean_div}" if clean_div else canonical_co

    official_domain = (dossier.get("official_domain") or "").strip().lower()
    official_domain = re.sub(r"^https?://(?:www\.)?", "", official_domain).split("/")[0].strip()

    if official_domain and not any(official_domain in c.url for c in citations):
        citations.insert(
            0,
            GroundingCitation(
                title=f"{canonical_co} — Official Corporate Portal ({official_domain})",
                url=f"https://www.{official_domain}",
            ),
        )
    if wiki_hint.get("page_url") and not any(c.url == wiki_hint["page_url"] for c in citations):
        citations.append(
            GroundingCitation(
                title=f"{wiki_hint.get('canonical_title', canonical_co)} — Corporate Operations Profile",
                url=wiki_hint["page_url"],
            )
        )

    accent_hex = clamp_brand_hex(dossier.get("brand_accent_hex", "#38bdf8"), "#38bdf8")
    sec_hex = dossier.get("brand_secondary_hex") or "#1e3a8a"

    # Normalize custom 4-8 Organization Pillars
    org_pillars = _normalize_org_pillars_partition(dossier.get("organization_pillars"), disp_label)
    if not org_pillars:
        org_pillars = [
            {
                "pillar_id": d_id,
                "scor_badge": d_obj.get("scorBadge", f"{idx+1:02d} · PILLAR"),
                "name": f"{canonical_co} {d_obj['name']}",
                "tagline": f"{disp_label} · {d_obj.get('tagline', '')}",
                "subtitle": d_obj.get("subtitle", ""),
                "color": d_obj.get("color", "#2563eb"),
                "watermark_type": "demand_wave",
                "sub_pillar_ids": [sp["id"] for sp in d_obj.get("subPillars", [])],
                "provenance_rationale": f"Derived from {canonical_co}'s core {d_obj['name'].lower()} operations across {dossier.get('flagship_facilities') or geography}.",
                "company_evidence_signals": [s.strip() for s in (dossier.get("flagship_facilities") or "").split("·") if s.strip()][:3],
                "verification_sources": [{"title": f"{canonical_co} Official Portal", "url": f"https://www.{official_domain}"}] if official_domain else [],
            }
            for idx, (d_id, d_obj) in enumerate(depts.items())
        ]

    _emit(
        progress_cb,
        38,
        "logo_framing",
        f"Downloading & optically framing official {canonical_co} logo ({official_domain or 'Wikimedia'})...",
        f"Designed {len(org_pillars)} bespoke Operating Pillars for {disp_label}",
    )

    logo_spec = resolve_company_logo(
        company_name=canonical_co,
        official_domain=official_domain,
        custom_logo_input=custom_logo_input,
        brand_accent=accent_hex,
        brand_secondary=sec_hex,
    )
    if logo_spec.source_url and not any(c.url == logo_spec.source_url for c in citations):
        citations.append(
            GroundingCitation(title=f"{canonical_co} Official Brand Mark", url=logo_spec.source_url)
        )

    n_pillars = len(org_pillars)
    _emit(
        progress_cb,
        48,
        "pillar_synthesis",
        f"Tailoring {n_pillars} Operating Pillars, 20 Sub-Pillars & 60 Job Roles for {canonical_co}...",
        f"Running {n_pillars} parallel Gemini 3.8 Flash specialists to write 2-line role & agent stories",
    )

    merged_sp_map: Dict[str, str] = {}
    merged_personas_map: Dict[str, Dict[str, Any]] = {}
    merged_agents_map: Dict[str, Dict[str, Any]] = {}
    completed_count = 0

    with ThreadPoolExecutor(max_workers=min(8, n_pillars)) as pool:
        future_to_meta = {}
        for idx, p_meta in enumerate(org_pillars):
            assigned_sps = [sp_lookup[sid] for sid in p_meta["sub_pillar_ids"] if sid in sp_lookup]
            fut = pool.submit(
                _stage2_synthesize_pillar_group,
                idx,
                p_meta,
                assigned_sps,
                personas_cat,
                agents_cat,
                dossier,
                geography,
                user_notes,
            )
            future_to_meta[fut] = (idx, p_meta["name"])

        for fut in as_completed(future_to_meta):
            _, p_name = future_to_meta[fut]
            completed_count += 1
            try:
                pres = fut.result() or {}
                if isinstance(pres.get("sub_pillars"), dict):
                    merged_sp_map.update(pres["sub_pillars"])
                if isinstance(pres.get("personas"), dict):
                    merged_personas_map.update(pres["personas"])
                if isinstance(pres.get("agents"), dict):
                    merged_agents_map.update(pres["agents"])
            except Exception as e:
                print(f"[ResearchEngine] Custom pillar '{p_name}' synthesis warning: {e}")

            _emit(
                progress_cb,
                48 + int((completed_count / float(max(1, n_pillars))) * 42),
                "pillar_synthesis",
                f"Synthesized Pillar {completed_count}/{n_pillars}: {p_name}",
                f"Mapped {canonical_co} job titles, process workflows & smart agent relevance",
            )

    # Assemble TwinOverlaySpec across all 20 sub-pillars & 60 personas/agents
    pillar_overrides: Dict[str, PillarOverrideSpec] = {}
    sub_pillar_overrides: Dict[str, SubPillarOverrideSpec] = {}
    persona_overrides: Dict[str, PersonaOverrideSpec] = {}
    agent_relevance: Dict[str, AgentRelevanceSpec] = {}

    for d_id, d_obj in depts.items():
        pillar_overrides[d_id] = PillarOverrideSpec(
            dept_id=d_id,
            custom_name=d_obj["name"],
            custom_tagline=f"{disp_label} · {d_obj.get('tagline', '')}",
            custom_subtitle=d_obj.get("subtitle", ""),
        )
        for sp in d_obj.get("subPillars", []):
            sp_id = sp["id"]
            custom_sp_name = str(merged_sp_map.get(sp_id) or sp["name"]).strip()
            sub_pillar_overrides[sp_id] = SubPillarOverrideSpec(
                sub_pillar_id=sp_id,
                dept_id=d_id,
                canonical_name=sp["name"],
                custom_name=custom_sp_name,
            )
            for it in sp.get("items", []):
                pid = it["personaId"]
                aid = it["agentId"]
                p_base = personas_cat.get(pid, {})
                dil0 = (p_base.get("dayInLife") or [{}])[0]
                po_in = merged_personas_map.get(pid) or {}
                persona_overrides[pid] = PersonaOverrideSpec(
                    persona_id=pid,
                    dept_id=d_id,
                    sub_pillar_id=sp_id,
                    canonical_name=p_base.get("name", pid),
                    title=str(po_in.get("title") or f"Lead — {custom_sp_name}").strip(),
                    role=str(po_in.get("role") or f"{custom_sp_name} · {disp_label}").strip(),
                    summary=str(po_in.get("summary") or p_base.get("summary", "")).strip(),
                    manual_toil=str(po_in.get("manual_toil") or dil0.get("before", "")).strip(),
                    agentic_impact=str(po_in.get("agentic_impact") or dil0.get("after", "")).strip(),
                    grounding_source=str(po_in.get("grounding_source") or f"Grounded in {canonical_co} career & ops roles").strip(),
                )

                ao_in = merged_agents_map.get(aid) or {}
                agent_relevance[aid] = AgentRelevanceSpec(
                    agent_id=aid,
                    dept_id=d_id,
                    sub_pillar_id=sp_id,
                    canonical_name=agents_cat.get(aid, {}).get("name", aid),
                    custom_agent_name=str(ao_in.get("custom_agent_name") or "").strip(),
                    is_relevant=bool(ao_in.get("is_relevant", True)),
                    division_context=str(ao_in.get("division_context") or f"Supports {custom_sp_name} across {disp_label}.").strip(),
                    hidden_reason=str(ao_in.get("hidden_reason") or "").strip(),
                )

    # Enforce physical & channel profile guardrails from Stage 1 research
    op_prof = dossier.get("division_operational_profile") or {}
    if isinstance(op_prof, dict):
        if op_prof.get("has_cold_chain_perishables") is False and "cold_chain_auditor" in agent_relevance:
            agent_relevance["cold_chain_auditor"].is_relevant = False
            agent_relevance["cold_chain_auditor"].hidden_reason = "Filtered for operational fit: no refrigerated cold-chain perishables."
        if op_prof.get("has_food_expiry_markdowns") is False and "food_waste_esg_copilot" in agent_relevance:
            agent_relevance["food_waste_esg_copilot"].is_relevant = False
            agent_relevance["food_waste_esg_copilot"].hidden_reason = "Filtered for operational fit: non-food product & operations portfolio."
        if op_prof.get("has_retail_stores_bopis_planograms") is False and op_prof.get("has_d2c_parcel_ecommerce") is False:
            for retail_aid in ("planogram_merchandising_vision_auditor", "keep_it_routing_advisor"):
                if retail_aid in agent_relevance:
                    agent_relevance[retail_aid].is_relevant = False
                    agent_relevance[retail_aid].hidden_reason = "Filtered for operational fit: B2B / non-retail store channel model."

    proc_overrides: Dict[str, ProcessJourneyOverrideSpec] = {}
    pj_in = dossier.get("process_journeys") or {}
    for vc_id in ("f2f", "o2d", "s2p", "p2r"):
        if vc_id in pj_in and isinstance(pj_in[vc_id], dict) and pj_in[vc_id].get("title"):
            proc_overrides[vc_id] = ProcessJourneyOverrideSpec(
                vc_id=vc_id,
                custom_title=str(pj_in[vc_id]["title"]).strip(),
                custom_subtitle=str(pj_in[vc_id].get("subtitle") or "").strip(),
            )

    brand_spec = CompanyBrandSpec(
        company_name=company_name,
        canonical_name=canonical_co,
        division_name=clean_div,
        twin_slug=twin_slug,
        official_domain=official_domain,
        industry_sector=dossier.get("industry_sector") or "Enterprise Supply Chain & Operations",
        geography=geography or "Global",
        brand_accent=accent_hex,
        brand_secondary=sec_hex,
        executive_title=dossier.get("executive_leader_title") or f"Chief Supply Chain & Operations Officer, {canonical_co}",
        executive_thesis=dossier.get("executive_thesis") or "",
        flagship_sites=dossier.get("flagship_facilities") or "",
        erp_systems=dossier.get("erp_systems") or "SAP S/4HANA · Cloud Supply Planning · Enterprise WMS & TMS",
        logo=logo_spec,
    )

    _emit(
        progress_cb,
        94,
        "integrity_validation",
        f"Validating {n_pillars}-Pillar DOM integrity & persisting {disp_label} portal...",
        "Checking WCAG contrast, sub-pillar partition, corporate role links & saving to database",
    )

    fallback_sources = [GroundingCitation(title=c.title, url=c.url, snippet=c.snippet) for c in citations[:3]]
    custom_pillars: List[CustomPillarSpec] = []
    for idx, op in enumerate(org_pillars):
        p_sources = [
            GroundingCitation(title=s["title"], url=s["url"], snippet=s.get("snippet", ""))
            for s in (op.get("verification_sources") or [])
            if isinstance(s, dict) and s.get("url")
        ]
        if not p_sources:
            p_sources = fallback_sources[:2]
        p_signals = list(op.get("company_evidence_signals") or [])
        if not p_signals and brand_spec.flagship_sites:
            p_signals = [x.strip() for x in brand_spec.flagship_sites.split("·") if x.strip()][:3]
        p_rat = op.get("provenance_rationale") or (
            f"Grounded in {disp_label}'s operating model ({brand_spec.industry_sector}) across {brand_spec.flagship_sites or geography}, "
            f"partitioning {', '.join(op['sub_pillar_ids'])} into a dedicated operating pillar."
        )
        p_jds = [
            JobDescriptionProofItem(
                job_title=j["job_title"],
                internal_org_unit=j.get("internal_org_unit", op["name"]),
                process_clues_from_jd=j.get("process_clues_from_jd", ""),
                jd_verification_url=j.get("jd_verification_url", ""),
                live_search_url=j.get("live_search_url", ""),
            )
            for j in (op.get("jd_proof_items") or [])
            if isinstance(j, dict) and j.get("job_title")
        ]
        p_naming = str(op.get("pillar_naming_basis") or "").strip() or (
            f"Named directly after {canonical_co}'s internal '{op['name']}' supply chain function and job requisitions."
        )
        custom_pillars.append(
            CustomPillarSpec(
                pillar_id=op["pillar_id"],
                v_num=f"{idx + 1:02d}",
                scor_badge=op["scor_badge"],
                name=op["name"],
                tagline=op["tagline"],
                subtitle=op["subtitle"],
                color=op["color"],
                watermark_type=op["watermark_type"],
                sub_pillar_ids=op["sub_pillar_ids"],
                pillar_naming_basis=p_naming,
                provenance_rationale=p_rat,
                company_evidence_signals=p_signals,
                jd_proof_items=p_jds,
                verification_sources=p_sources,
            )
        )

    discovered_titles = list(dossier.get("discovered_career_titles") or [])
    for ch in career_hints:
        if ch not in discovered_titles:
            discovered_titles.append(ch)

    meth_note = str(dossier.get("architecture_methodology_note") or "").strip() or (
        f"Curated {len(custom_pillars)} Operating Pillars for {disp_label} by mapping its public business segments, "
        f"manufacturing/distribution footprint ({brand_spec.flagship_sites or geography}), and corporate supply chain roles "
        f"onto the 20 canonical ASCM SCOR functional sub-pillars while filtering out physically inapplicable workflows."
    )

    spec = TwinOverlaySpec(
        twin_slug=twin_slug,
        company_name=company_name,
        canonical_name=canonical_co,
        division_name=clean_div,
        brand=brand_spec,
        custom_pillars=custom_pillars,
        pillar_overrides=pillar_overrides,
        sub_pillar_overrides=sub_pillar_overrides,
        persona_overrides=persona_overrides,
        agent_relevance=agent_relevance,
        process_overrides=proc_overrides,
        architecture_methodology_note=meth_note,
        grounding_citations=citations[:12],
        career_title_examples=discovered_titles[:8],
        terminology_highlights=(dossier.get("terminology_glossary") or [])[:6],
        generation_model="Gemini 3.1 Pro / 4 Argon + Gemini 3.8 Flash (Google Search Grounded)",
    )
    return validate_and_normalize_overlay(spec)

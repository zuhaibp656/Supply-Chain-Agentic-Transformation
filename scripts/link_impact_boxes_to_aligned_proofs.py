#!/usr/bin/env python3
"""Make Persona & Agent top/bottom impact boxes hover-highlighted & clickable
to deep-link directly to their exact supporting Case Study & Benchmark Proof,
and align the Case Studies & Proofs Hub (#pageEvidence) 1-to-1 with the live
Operating Pillar -> Sub-Pillar -> Persona & Agent navigation hierarchy.
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def must_replace(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"Expected snippet not found for [{label}]")
    return text.replace(old, new, 1)


IMPACT_AND_EVIDENCE_CSS = """
    /* =========================================================================
       CLICKABLE MINIMAL-TEXT IMPACT BOXES & NAVIGATION-ALIGNED PROOF SPOTLIGHT
       ========================================================================= */
    .sc-impact-link-box {
      cursor: pointer !important;
      position: relative;
      text-align: left;
      font-family: inherit;
      transition: transform 0.22s cubic-bezier(0.22, 1, 0.36, 1),
                  box-shadow 0.22s cubic-bezier(0.22, 1, 0.36, 1),
                  border-color 0.22s ease,
                  background-color 0.22s ease !important;
    }

    button.persona-stat-highlight.sc-impact-link-box {
      appearance: none;
      -webkit-appearance: none;
      text-align: right;
      cursor: pointer !important;
    }

    .sc-impact-link-box:hover,
    .sc-impact-link-box:focus-visible {
      transform: translateY(-3px) scale(1.015) !important;
      border-color: var(--imp-accent, #10b981) !important;
      box-shadow: 0 12px 28px rgba(16, 185, 129, 0.20),
                  0 0 0 2px rgba(16, 185, 129, 0.26) !important;
      outline: none;
    }

    .sc-impact-link-box .sc-impact-cue {
      display: inline-block;
      font-size: 12px;
      font-weight: 800;
      opacity: 0.68;
      margin-left: 4px;
      transition: transform 0.2s ease, opacity 0.2s ease;
    }

    .sc-impact-link-box:hover .sc-impact-cue,
    .sc-impact-pill-link:hover .sc-impact-cue {
      opacity: 1;
      transform: translate(2px, -2px);
    }

    .sc-impact-pill-link {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      cursor: pointer !important;
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 800;
      padding: 4px 11px;
      border-radius: 999px;
      background: rgba(16, 185, 129, 0.14);
      color: #10b981;
      border: 1.5px solid rgba(16, 185, 129, 0.38);
      text-decoration: none;
      transition: transform 0.2s cubic-bezier(0.22, 1, 0.36, 1),
                  box-shadow 0.2s ease,
                  background-color 0.2s ease,
                  border-color 0.2s ease,
                  color 0.2s ease !important;
    }

    .sc-impact-pill-link:hover,
    .sc-impact-pill-link:focus-visible {
      transform: translateY(-2px) !important;
      background: rgba(16, 185, 129, 0.24) !important;
      border-color: #10b981 !important;
      color: #34d399 !important;
      box-shadow: 0 6px 18px rgba(16, 185, 129, 0.25),
                  0 0 0 2px rgba(16, 185, 129, 0.20) !important;
      outline: none;
    }

    .sc-bottom-impact-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      width: 100%;
      margin-top: 18px;
      padding: 15px 22px;
      border-radius: 14px;
      background: var(--bg-card);
      border: 1.5px solid rgba(16, 185, 129, 0.38);
      border-left: 5px solid var(--imp-accent, #10b981);
    }

    .sc-bottom-impact-kicker {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--imp-accent, #10b981);
    }

    .sc-bottom-impact-metric {
      font-family: var(--font-display);
      font-size: 18px;
      font-weight: 800;
      color: var(--text-primary);
    }

    .sc-bottom-impact-right {
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 800;
      color: #10b981;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    /* Evidence Hub Navigation Hierarchy & Focused Spotlight */
    .sc-ev-nav-shell {
      background: var(--bg-card);
      border: 1.5px solid var(--border-strong);
      border-radius: 16px;
      padding: 18px 22px;
      margin-bottom: 20px;
    }

    .sc-ev-nav-row {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }

    .sc-ev-nav-row + .sc-ev-nav-row {
      margin-top: 12px;
      padding-top: 12px;
      border-top: 1px solid var(--border-subtle);
    }

    .sc-ev-nav-label {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-secondary);
      min-width: 112px;
    }

    .sc-proof-spotlight-card {
      background: var(--bg-card);
      border: 2px solid var(--spot-accent, #10b981);
      border-top: 5px solid var(--spot-accent, #10b981);
      border-radius: 18px;
      padding: 24px 26px;
      margin-bottom: 22px;
      box-shadow: 0 16px 38px rgba(16, 185, 129, 0.14);
    }

    .sc-v22-cs-card.sc-proof-target-focused {
      border: 2px solid var(--cs-accent, #10b981) !important;
      border-top: 5px solid var(--cs-accent, #10b981) !important;
      box-shadow: 0 18px 42px rgba(16, 185, 129, 0.18),
                  0 0 0 3px rgba(16, 185, 129, 0.16) !important;
    }

    /* Crisp Light Mode Contrast Guarantees for Impact Hover & Proof Spotlight */
    html[data-theme="light"] .sc-impact-link-box:hover,
    html[data-theme="light"] .sc-impact-link-box:focus-visible {
      background: #f0fdf4 !important;
      border-color: var(--imp-accent, #059669) !important;
      box-shadow: 0 12px 26px rgba(5, 150, 105, 0.16),
                  0 0 0 2px rgba(5, 150, 105, 0.22) !important;
    }

    html[data-theme="light"] .sc-impact-link-box:hover .persona-stat-label,
    html[data-theme="light"] .sc-impact-link-box:hover .sc-agent-card-brief,
    html[data-theme="light"] .sc-impact-link-box:hover .sc-bottom-impact-metric,
    html[data-theme="light"] .sc-impact-link-box:hover .sc-flip-big-heading span {
      color: #0f172a !important;
    }

    html[data-theme="light"] .sc-impact-pill-link {
      background: #ecfdf5 !important;
      color: #047857 !important;
      border-color: rgba(5, 150, 105, 0.42) !important;
    }

    html[data-theme="light"] .sc-impact-pill-link:hover,
    html[data-theme="light"] .sc-impact-pill-link:focus-visible {
      background: #d1fae5 !important;
      color: #065f46 !important;
      border-color: #059669 !important;
      box-shadow: 0 6px 16px rgba(5, 150, 105, 0.18) !important;
    }

    html[data-theme="light"] .sc-bottom-impact-bar {
      background: #ffffff;
      border-color: rgba(5, 150, 105, 0.38);
      box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
    }

    html[data-theme="light"] .sc-bottom-impact-right {
      color: #047857 !important;
    }

    html[data-theme="light"] .sc-proof-spotlight-card {
      background: #ffffff;
      box-shadow: 0 14px 34px rgba(15, 23, 42, 0.09);
    }
"""


NEW_EVIDENCE_ENGINE_JS = """    const SUBPILLAR_ID_TO_CANONICAL = {
      demand_forecasting: 'Demand Forecasting',
      trade_promotion: 'Trade Promotion',
      sop_ibp: 'S&OP / IBP',
      portfolio_sku: 'Portfolio & SKU',
      supplier_network: 'Supplier Network',
      material_packaging: 'Material & Packaging',
      contract_po_mgmt: 'Contract & PO Mgmt',
      production_scheduling: 'Production Scheduling',
      capacity_planning: 'Capacity Planning',
      quality_compliance: 'Quality & Compliance',
      positioning_optimization: 'Positioning & Optimization',
      warehouse_operations: 'Warehouse Operations',
      omnichannel_visibility: 'Omnichannel Visibility',
      first_mid_mile: 'First & Mid-Mile',
      store_replenishment: 'Store Replenishment',
      last_mile_delivery: 'Last-Mile Delivery',
      route_carrier: 'Route & Carrier',
      returns_claims_mgmt: 'Returns & Claims Mgmt',
      expiry_markdowns: 'Expiry & Markdowns',
      pallet_tote_reclamation: 'Pallet & Tote Reclamation'
    };

    const SUBPILLAR_PRIMARY_CASE_ID = {
      demand_forecasting: 'cs_unilever',
      trade_promotion: 'cs_danone',
      sop_ibp: 'cs_wef_lighthouses',
      portfolio_sku: 'cs_unilever',
      supplier_network: 'cs_ge_appliances',
      material_packaging: 'cs_unilever',
      contract_po_mgmt: 'cs_ge_appliances',
      production_scheduling: 'cs_wef_lighthouses',
      capacity_planning: 'cs_ge_appliances',
      quality_compliance: 'cs_tyson',
      positioning_optimization: 'cs_home_depot',
      warehouse_operations: 'cs_fm_logistic',
      omnichannel_visibility: 'cs_home_depot',
      first_mid_mile: 'cs_walmart',
      store_replenishment: 'cs_walmart',
      last_mile_delivery: 'cs_ups',
      route_carrier: 'cs_ups',
      returns_claims_mgmt: 'cs_walmart',
      expiry_markdowns: 'cs_carrefour',
      pallet_tote_reclamation: 'cs_tyson'
    };

    const AGENT_SPECIFIC_CASE_OVERRIDE = {
      cold_chain_auditor: 'cs_tyson',
      store_capacity_agent: 'cs_carrefour',
      batch_record_auditor: 'cs_wef_lighthouses',
      scrap_defect_root_cause_agent: 'cs_ge_appliances',
      carbon_scope3_ledger: 'cs_unilever',
      intermodal_rail_linehaul_agent: 'cs_walmart',
      rti_balance_reconciler: 'cs_walmart'
    };

    function resolveEntitySubPillarId(entity) {
      if (!entity) return null;
      if (entity.subPillarId && SUBPILLAR_ID_TO_CANONICAL[entity.subPillarId]) {
        return entity.subPillarId;
      }
      for (const d of Object.values(DEPARTMENTS)) {
        for (const sp of (d.subPillars || [])) {
          const hit = (sp.items || []).some(it => it.agentId === entity.id || it.personaId === entity.id);
          if (hit) return sp.id;
        }
      }
      const spName = entity.subPillarName || '';
      for (const [spId, cName] of Object.entries(SUBPILLAR_ID_TO_CANONICAL)) {
        if (cName === spName) return spId;
      }
      return null;
    }

    function resolveLiveDeptForSubPillar(spId, fallbackDeptId) {
      if (spId) {
        for (const d of Object.values(DEPARTMENTS)) {
          if ((d.subPillars || []).some(sp => sp.id === spId)) {
            return d;
          }
        }
      }
      if (fallbackDeptId && DEPARTMENTS[fallbackDeptId]) return DEPARTMENTS[fallbackDeptId];
      return Object.values(DEPARTMENTS)[0] || null;
    }

    function getCaseStudyById(csId) {
      return ENTERPRISE_CASE_STUDIES.find(c => c.id === csId) || ENTERPRISE_CASE_STUDIES[0];
    }

    function getProofForSubPillarId(spId, spNameFallback) {
      const canonicalName = (spId && SUBPILLAR_ID_TO_CANONICAL[spId]) || spNameFallback || '';
      const base = SUBPILLAR_PROOF_MAP[canonicalName] || {
        benchOrg: 'McKinsey & ASCM SCOR Digital Standard',
        benchStat: 'AI supply chain orchestration reduces operational cost by 5%–15%, inventory buffers by 20%–35%, and manual planning toil by 70%+.',
        benchUrl: 'https://www.mckinsey.com/industries/industrials/our-insights/distribution-blog/ai-is-transforming-distribution-supply-chains-turning-margin-pressure-into-a-competitive-advantage',
        caseTitle: 'GE Appliances & Unilever × Google Cloud Gemini Enterprise',
        caseStat: 'Enterprise-scale multi-agent deployments on Google Cloud delivering double-digit backorder, logistics, and working-capital improvements.',
        caseUrl: 'https://www.googlecloudpresscorner.com/2026-04-22-GE-Appliances-Reinvents-Manufacturing-Operations-at-Scale-with-Google-Clouds-Gemini-Enterprise'
      };
      const primaryCaseId = (spId && SUBPILLAR_PRIMARY_CASE_ID[spId]) || 'cs_ge_appliances';
      return Object.assign({}, base, {
        subPillarId: spId || null,
        canonicalSubPillarName: canonicalName,
        primaryCaseId,
        caseStudy: getCaseStudyById(primaryCaseId)
      });
    }

    function getProofForAgent(ag, dept) {
      const spId = resolveEntitySubPillarId(ag);
      const proof = getProofForSubPillarId(spId, ag && ag.subPillarName);
      const overrideCsId = ag && AGENT_SPECIFIC_CASE_OVERRIDE[ag.id];
      if (overrideCsId) {
        proof.primaryCaseId = overrideCsId;
        proof.caseStudy = getCaseStudyById(overrideCsId);
      }
      return proof;
    }

    function getProofForPersona(p, dept) {
      const spId = resolveEntitySubPillarId(p);
      const proof = getProofForSubPillarId(spId, p && p.subPillarName);
      const primaryAid = p && (p.primaryAgentId || (p.agentIds && p.agentIds[0]));
      if (primaryAid && AGENT_SPECIFIC_CASE_OVERRIDE[primaryAid]) {
        proof.primaryCaseId = AGENT_SPECIFIC_CASE_OVERRIDE[primaryAid];
        proof.caseStudy = getCaseStudyById(proof.primaryCaseId);
      }
      return proof;
    }

    let currentEvidenceSubPillar = 'all';
    let currentEvidenceFocus = null; // { kind: 'agent' | 'persona', id: string }

    function openProofForAgent(agentId, ev) {
      if (ev && typeof ev.stopPropagation === 'function') ev.stopPropagation();
      const ag = AGENTS[agentId];
      if (!ag) return;
      const spId = resolveEntitySubPillarId(ag);
      const liveDept = resolveLiveDeptForSubPillar(spId, ag.deptId);
      currentEvidenceTab = 'cases';
      currentEvidenceSubPillar = spId || 'all';
      currentEvidenceFocus = { kind: 'agent', id: ag.id };
      openEvidenceHubPage(liveDept ? liveDept.id : 'all', true, ev, currentEvidenceFocus, currentEvidenceSubPillar);
    }

    function openProofForPersona(personaId, ev) {
      if (ev && typeof ev.stopPropagation === 'function') ev.stopPropagation();
      const p = PERSONAS[personaId];
      if (!p) return;
      const spId = resolveEntitySubPillarId(p);
      const liveDept = resolveLiveDeptForSubPillar(spId, p.deptId);
      currentEvidenceTab = 'cases';
      currentEvidenceSubPillar = spId || 'all';
      currentEvidenceFocus = { kind: 'persona', id: p.id };
      openEvidenceHubPage(liveDept ? liveDept.id : 'all', true, ev, currentEvidenceFocus, currentEvidenceSubPillar);
    }
"""


NEW_OPEN_EVIDENCE_HUB_JS = """    let currentEvidenceTab = 'cases'; // 'cases' | 'benchmarks' | 'sources'

    function switchEvidenceTab(tabName) {
      currentEvidenceTab = tabName || 'cases';
      openEvidenceHubPage(currentEvidencePillar, false, null, currentEvidenceFocus, currentEvidenceSubPillar);
    }

    function selectEvidenceSubPillar(deptId, spId, ev) {
      currentEvidenceFocus = null;
      currentEvidenceSubPillar = spId || 'all';
      openEvidenceHubPage(deptId || 'all', true, ev, null, currentEvidenceSubPillar);
    }

    function openEvidenceHubPage(pillarFilter = 'all', pushState = true, ev = null, focusCtx = undefined, subPillarFilter = undefined) {
      if (focusCtx !== undefined) {
        currentEvidenceFocus = focusCtx;
      }
      if (subPillarFilter !== undefined) {
        currentEvidenceSubPillar = subPillarFilter || 'all';
      } else if (pillarFilter === 'all' && !currentEvidenceFocus) {
        currentEvidenceSubPillar = 'all';
      }

      const liveDepts = Object.values(DEPARTMENTS);
      if (pillarFilter && pillarFilter !== 'all' && !DEPARTMENTS[pillarFilter]) {
        // Map legacy canonical deptId to active Company Twin pillar if needed
        const matchDept = liveDepts.find(d =>
          d.id === pillarFilter ||
          (d.subPillars || []).some(sp => (SUBPILLAR_ID_TO_CANONICAL[sp.id] && PILLAR_PROOF_BENCHMARKS.some(pb => pb.deptId === pillarFilter)))
        );
        currentEvidencePillar = matchDept ? matchDept.id : 'all';
      } else {
        currentEvidencePillar = pillarFilter || 'all';
      }

      // Ensure subPillarFilter belongs to active pillar
      const activeDeptObj = currentEvidencePillar !== 'all' ? DEPARTMENTS[currentEvidencePillar] : null;
      if (activeDeptObj && currentEvidenceSubPillar !== 'all') {
        const hasSp = (activeDeptObj.subPillars || []).some(sp => sp.id === currentEvidenceSubPillar);
        if (!hasSp) currentEvidenceSubPillar = 'all';
      }

      if (pushState) {
        let hash = '#evidence';
        if (currentEvidenceFocus && currentEvidenceFocus.kind && currentEvidenceFocus.id) {
          hash = `#evidence/${currentEvidenceFocus.kind}/${currentEvidenceFocus.id}`;
        } else if (currentEvidenceSubPillar && currentEvidenceSubPillar !== 'all') {
          hash = `#evidence/subpillar/${currentEvidenceSubPillar}`;
        } else if (currentEvidencePillar !== 'all') {
          hash = `#evidence/${currentEvidencePillar}`;
        }
        history.pushState({
          page: 'evidence',
          pillar: currentEvidencePillar,
          subPillar: currentEvidenceSubPillar,
          focus: currentEvidenceFocus
        }, '', hash);
      }

      const container = document.getElementById('evidencePageContent');
      if (!container) return;

      const pillarCount = liveDepts.length;
      const agentCount = Object.keys(AGENTS).length;

      // Build dynamic Case Study -> Live Pillars, Sub-Pillars, Personas & Agents index
      const caseLiveLinks = {};
      ENTERPRISE_CASE_STUDIES.forEach(cs => {
        caseLiveLinks[cs.id] = { deptIds: new Set(), subPillars: [], personas: [], agents: [] };
      });

      liveDepts.forEach(d => {
        (d.subPillars || []).forEach(sp => {
          const primaryCsId = SUBPILLAR_PRIMARY_CASE_ID[sp.id];
          if (primaryCsId && caseLiveLinks[primaryCsId]) {
            caseLiveLinks[primaryCsId].deptIds.add(d.id);
            if (!caseLiveLinks[primaryCsId].subPillars.some(x => x.id === sp.id)) {
              caseLiveLinks[primaryCsId].subPillars.push({ id: sp.id, name: sp.name, color: sp.color || d.color, deptId: d.id });
            }
          }
          (sp.items || []).forEach(it => {
            const p = PERSONAS[it.personaId];
            const ag = AGENTS[it.agentId];
            const agCsId = (ag && AGENT_SPECIFIC_CASE_OVERRIDE[ag.id]) || primaryCsId;
            if (p && primaryCsId && caseLiveLinks[primaryCsId]) {
              if (!caseLiveLinks[primaryCsId].personas.some(x => x.id === p.id)) {
                caseLiveLinks[primaryCsId].personas.push(p);
              }
            }
            if (ag && agCsId && caseLiveLinks[agCsId]) {
              caseLiveLinks[agCsId].deptIds.add(d.id);
              if (!caseLiveLinks[agCsId].agents.some(x => x.id === ag.id)) {
                caseLiveLinks[agCsId].agents.push(ag);
              }
            }
          });
        });
      });

      // Also include any explicit cs.agentIds that exist in AGENTS
      ENTERPRISE_CASE_STUDIES.forEach(cs => {
        (cs.agentIds || []).forEach(aid => {
          const ag = AGENTS[aid];
          if (ag && caseLiveLinks[cs.id]) {
            const spId = resolveEntitySubPillarId(ag);
            const ld = resolveLiveDeptForSubPillar(spId, ag.deptId);
            if (ld) caseLiveLinks[cs.id].deptIds.add(ld.id);
            if (!caseLiveLinks[cs.id].agents.some(x => x.id === ag.id)) {
              caseLiveLinks[cs.id].agents.push(ag);
            }
          }
        });
      });

      // Resolve focused entity (Persona or Agent) if arriving from a clicked Impact Box
      let focusedEntity = null;
      let focusedProof = null;
      let focusedDept = null;
      let focusedSubPillar = null;
      let focusedCaseId = null;

      if (currentEvidenceFocus && currentEvidenceFocus.id) {
        if (currentEvidenceFocus.kind === 'agent' && AGENTS[currentEvidenceFocus.id]) {
          focusedEntity = AGENTS[currentEvidenceFocus.id];
          const spId = resolveEntitySubPillarId(focusedEntity);
          focusedDept = resolveLiveDeptForSubPillar(spId, focusedEntity.deptId);
          focusedSubPillar = focusedDept ? (focusedDept.subPillars || []).find(s => s.id === spId) : null;
          focusedProof = getProofForAgent(focusedEntity, focusedDept);
          focusedCaseId = focusedProof.primaryCaseId;
        } else if (currentEvidenceFocus.kind === 'persona' && PERSONAS[currentEvidenceFocus.id]) {
          focusedEntity = PERSONAS[currentEvidenceFocus.id];
          const spId = resolveEntitySubPillarId(focusedEntity);
          focusedDept = resolveLiveDeptForSubPillar(spId, focusedEntity.deptId);
          focusedSubPillar = focusedDept ? (focusedDept.subPillars || []).find(s => s.id === spId) : null;
          focusedProof = getProofForPersona(focusedEntity, focusedDept);
          focusedCaseId = focusedProof.primaryCaseId;
        }
      } else if (currentEvidenceSubPillar && currentEvidenceSubPillar !== 'all') {
        const spProof = getProofForSubPillarId(currentEvidenceSubPillar);
        focusedCaseId = spProof.primaryCaseId;
      }

      // Filter Case Studies in alignment with Operating Pillar -> Sub-Pillar navigation
      let filteredCases = ENTERPRISE_CASE_STUDIES.filter(cs => {
        const meta = caseLiveLinks[cs.id];
        if (currentEvidenceSubPillar && currentEvidenceSubPillar !== 'all') {
          const inSp = meta.subPillars.some(s => s.id === currentEvidenceSubPillar) ||
                       meta.agents.some(a => resolveEntitySubPillarId(a) === currentEvidenceSubPillar) ||
                       cs.id === focusedCaseId;
          return inSp;
        }
        if (currentEvidencePillar === 'all') return true;
        return meta.deptIds.has(currentEvidencePillar) || cs.deptIds.includes(currentEvidencePillar) || cs.id === focusedCaseId;
      });

      if (focusedCaseId) {
        filteredCases = filteredCases.slice().sort((a, b) => (a.id === focusedCaseId ? -1 : b.id === focusedCaseId ? 1 : 0));
      }

      // Level 1 Navigation Pills: Live Operating Pillars
      const pillarNavPillsHtml = [
        `<button type="button" class="switch-pill ${currentEvidencePillar === 'all' ? 'active' : ''}" style="${currentEvidencePillar === 'all' ? 'background:var(--g-blue);border-color:var(--g-blue);color:#ffffff;font-weight:800;' : ''}" onclick="currentEvidenceFocus=null; currentEvidenceSubPillar='all'; openEvidenceHubPage('all', true, event)">All ${pillarCount} Pillars (${ENTERPRISE_CASE_STUDIES.length})</button>`
      ].concat(liveDepts.map(d => {
        const active = currentEvidencePillar === d.id;
        return `<button type="button" class="switch-pill ${active ? 'active' : ''}" style="${active ? `background:${d.color};border-color:${d.color};color:#ffffff;font-weight:800;` : ''}" onclick="currentEvidenceFocus=null; currentEvidenceSubPillar='all'; openEvidenceHubPage('${d.id}', true, event)">${d.vNum} · ${d.name}</button>`;
      })).join('');

      // Level 2 Navigation Pills: Sub-Pillars inside Selected Operating Pillar
      const activeSubPillars = activeDeptObj ? (activeDeptObj.subPillars || []) : [];
      const activeSpObj = activeSubPillars.find(s => s.id === currentEvidenceSubPillar) || null;

      const subPillarNavRowHtml = activeDeptObj ? `
        <div class="sc-ev-nav-row">
          <span class="sc-ev-nav-label">Sub-Pillars:</span>
          <button type="button" class="switch-pill ${currentEvidenceSubPillar === 'all' ? 'active' : ''}"
                  style="${currentEvidenceSubPillar === 'all' ? `background:${activeDeptObj.color};border-color:${activeDeptObj.color};color:#ffffff;font-weight:800;` : ''}"
                  onclick="selectEvidenceSubPillar('${activeDeptObj.id}', 'all', event)">
            All in ${activeDeptObj.name} (${activeSubPillars.length})
          </button>
          ${activeSubPillars.map(sp => {
            const isAct = currentEvidenceSubPillar === sp.id;
            const col = sp.color || activeDeptObj.color;
            return `
              <button type="button" class="switch-pill ${isAct ? 'active' : ''}"
                      style="${isAct ? `background:${col};border-color:${col};color:#ffffff;font-weight:800;` : ''}"
                      onclick="selectEvidenceSubPillar('${activeDeptObj.id}', '${sp.id}', event)">
                ${sp.icon || '📦'} ${sp.name}
              </button>
            `;
          }).join('')}
        </div>
      ` : '';

      // Level 3 Navigation Pills: Personas & AI Agents inside Selected Sub-Pillar
      const entityNavRowHtml = activeSpObj ? `
        <div class="sc-ev-nav-row">
          <span class="sc-ev-nav-label">Personas &amp; Agents:</span>
          ${(activeSpObj.items || []).map(it => {
            const p = PERSONAS[it.personaId];
            if (!p) return '';
            const isFoc = focusedEntity && currentEvidenceFocus && currentEvidenceFocus.kind === 'persona' && focusedEntity.id === p.id;
            const col = activeSpObj.color || (activeDeptObj && activeDeptObj.color) || '#2563eb';
            return `
              <button type="button" class="switch-pill ${isFoc ? 'active' : ''}"
                      style="font-size:12px; padding:5px 11px; ${isFoc ? `background:${col};border-color:${col};color:#ffffff;font-weight:800;` : ''}"
                      onclick="openProofForPersona('${p.id}', event)">
                ${p.icon} ${p.name}
              </button>
            `;
          }).join('')}
          ${(activeSpObj.items || []).map(it => {
            const ag = AGENTS[it.agentId];
            if (!ag) return '';
            const isFoc = focusedEntity && currentEvidenceFocus && currentEvidenceFocus.kind === 'agent' && focusedEntity.id === ag.id;
            return `
              <button type="button" class="switch-pill ${isFoc ? 'active' : ''}"
                      style="font-size:12px; padding:5px 11px; ${isFoc ? 'background:#10b981;border-color:#10b981;color:#ffffff;font-weight:800;' : ''}"
                      onclick="openProofForAgent('${ag.id}', event)">
                ✦ ${cleanAgentName(ag.name)}
              </button>
            `;
          }).join('')}
        </div>
      ` : '';

      // Focused Spotlight Card when arriving from a Persona or Agent Impact Box (or Sub-Pillar selection)
      let spotlightHtml = '';
      if (focusedEntity && focusedProof && focusedProof.caseStudy) {
        const isAgent = currentEvidenceFocus.kind === 'agent';
        const entityLabel = isAgent ? cleanAgentName(focusedEntity.name) : focusedEntity.name;
        const entityIcon = isAgent ? '✦' : (focusedEntity.icon || '👤');
        const impactText = isAgent
          ? (focusedEntity.badge || 'Verified ROI')
          : `${focusedEntity.headlineStat || '-85% Toil'} (${focusedEntity.toilHoursBefore || '6.5h'} → ${focusedEntity.toilHoursAfter || '1.0h'})`;
        const spotAccent = (focusedSubPillar && focusedSubPillar.color) || (focusedDept && focusedDept.color) || '#10b981';
        const cs = focusedProof.caseStudy;

        spotlightHtml = `
          <div id="evidenceFocusedSpotlight" class="sc-proof-spotlight-card" style="--spot-accent:${spotAccent};">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:14px; margin-bottom:16px;">
              <div>
                <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:6px;">
                  <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.07em; color:${spotAccent};">
                    ${focusedDept ? `${focusedDept.vNum} · ${focusedDept.name}` : 'Operating Pillar'}
                  </span>
                  ${focusedSubPillar ? `<span style="color:var(--text-muted);">&rarr;</span><span style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:var(--text-secondary);">${focusedSubPillar.icon || ''} ${focusedSubPillar.name}</span>` : ''}
                </div>
                <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
                  <h2 style="font-family:var(--font-display); font-size:clamp(20px, 2.2vw, 26px); font-weight:800; color:var(--text-primary); margin:0;">
                    ${entityIcon} Supporting Proof for ${entityLabel}
                  </h2>
                  <span class="sc-impact-pill-link" style="pointer-events:none;">
                    ${isAgent ? '🚀' : '⚡'} ${impactText}
                  </span>
                </div>
              </div>

              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                <button type="button" class="agent-plug-btn" style="padding:8px 15px; font-size:12.5px;"
                        onclick="${isAgent ? `openAgentPage('${focusedEntity.id}', true, event)` : `openPersonaPage('${focusedEntity.id}', true, event)`}">
                  <span>&larr; Back to ${entityLabel}</span>
                </button>
              </div>
            </div>

            <div class="sc-proof-cols">
              <div class="sc-proof-box" style="border-left: 4px solid ${cs.accent || spotAccent};">
                <div>
                  <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:#10b981; margin-bottom:4px;">
                    🏢 Supporting Enterprise Case Study · ${cs.headlineMetric}
                  </div>
                  <div style="font-weight:800; font-size:16px; color:var(--text-primary); margin-bottom:6px;">
                    ${cs.company}
                  </div>
                  <div style="font-size:13.5px; color:var(--text-secondary); line-height:1.58;">
                    ${cs.outcome}
                  </div>
                </div>
                <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:10px;">
                  <a href="${cs.url}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill">
                    <span>${cs.sourceLabel}</span>
                    <span>&#8599;</span>
                  </a>
                  ${cs.secondaryUrl ? `
                    <a href="${cs.secondaryUrl}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill">
                      <span>${cs.secondaryLabel}</span>
                      <span>&#8599;</span>
                    </a>
                  ` : ''}
                </div>
              </div>

              <div class="sc-proof-box" style="border-left: 4px solid ${spotAccent};">
                <div>
                  <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:${spotAccent}; margin-bottom:4px;">
                    📊 Supporting Industry &amp; Analyst Benchmark
                  </div>
                  <div style="font-weight:800; font-size:16px; color:var(--text-primary); margin-bottom:6px;">
                    ${focusedProof.benchOrg}
                  </div>
                  <div style="font-size:13.5px; color:var(--text-secondary); line-height:1.58;">
                    ${focusedProof.benchStat}
                  </div>
                </div>
                <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:10px;">
                  <a href="${focusedProof.benchUrl}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill">
                    <span>Verify Benchmark Source</span>
                    <span>&#8599;</span>
                  </a>
                </div>
              </div>
            </div>
          </div>
        `;
      }

      // Dynamic Pillar Benchmark Matrix Rows aligned to live Operating Pillars -> Sub-Pillars
      const visibleBenchDepts = currentEvidencePillar === 'all'
        ? liveDepts
        : liveDepts.filter(d => d.id === currentEvidencePillar);

      const pillarRowsHtml = visibleBenchDepts.map(d => {
        const spList = (d.subPillars || []).filter(sp => currentEvidenceSubPillar === 'all' || sp.id === currentEvidenceSubPillar);
        return spList.map(sp => {
          const pr = getProofForSubPillarId(sp.id, sp.name);
          const cs = pr.caseStudy;
          const spAgents = (sp.items || []).map(it => AGENTS[it.agentId]).filter(Boolean);
          const leadStat = spAgents[0] ? spAgents[0].badge : 'Verified ROI';
          return `
            <tr style="border-bottom:1px solid var(--border-subtle);">
              <td style="padding:16px 14px; vertical-align:top; min-width:200px;">
                <div style="font-family:var(--font-mono); font-size:11px; font-weight:800; color:${d.color}; text-transform:uppercase;">${d.vNum} · ${d.name}</div>
                <div style="font-weight:800; color:var(--text-primary); font-size:14.5px; margin-top:3px;">${sp.icon || ''} ${sp.name}</div>
              </td>
              <td style="padding:16px 14px; vertical-align:top; font-family:var(--font-mono); font-size:12.5px; font-weight:700; color:#10b981; min-width:165px;">
                ${leadStat}
              </td>
              <td style="padding:16px 14px; vertical-align:top; min-width:250px;">
                <div style="font-size:13.5px; color:var(--text-primary); line-height:1.52; margin-bottom:8px;">
                  ${pr.benchStat}
                </div>
                <a href="${pr.benchUrl}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill" style="font-size:11.5px; padding:4px 10px;">
                  ${pr.benchOrg} &#8599;
                </a>
              </td>
              <td style="padding:16px 14px; vertical-align:top; min-width:220px;">
                <div style="font-size:13px; font-weight:700; color:var(--text-primary); margin-bottom:6px;">${cs.company}</div>
                <a href="${cs.url}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill" style="font-size:11.5px; padding:5px 11px;">
                  ${cs.headlineMetric} &#8599;
                </a>
              </td>
            </tr>
          `;
        }).join('');
      }).join('');

      const caseCardsHtml = filteredCases.map(cs => {
        const liveMeta = caseLiveLinks[cs.id] || { deptIds: new Set(), subPillars: [], personas: [], agents: [] };
        const isTargetCard = focusedCaseId === cs.id;

        const pillarBadges = Array.from(liveMeta.deptIds).map(did => {
          const d = DEPARTMENTS[did];
          if (!d) return '';
          return `<button type="button" class="sc-tech-pill" onclick="currentEvidenceFocus=null; currentEvidenceSubPillar='all'; openEvidenceHubPage('${d.id}', true, event)" style="cursor:pointer; font-size:11.5px; padding:3px 10px; color:${d.color}; border-color:${d.color}55; font-weight:700;">${d.vNum} · ${d.name}</button>`;
        }).join('');

        const personaChips = liveMeta.personas.slice(0, 4).map(p => `
          <button type="button" class="sc-tech-pill" onclick="openPersonaPage('${p.id}', true, event)" style="cursor:pointer; font-size:11.5px; font-weight:700; padding:4px 10px;">
            ${p.icon || '👤'} ${p.name} &rarr;
          </button>
        `).join('');

        const agentChips = liveMeta.agents.slice(0, 5).map(ag => `
          <button type="button" class="sc-tech-pill" onclick="openAgentPage('${ag.id}', true, event)" style="cursor:pointer; font-size:11.5px; font-weight:700; padding:4px 10px;">
            ✦ ${cleanAgentName(ag.name)} &rarr;
          </button>
        `).join('');

        return `
          <div id="caseCard_${cs.id}" class="sc-v22-cs-card ${isTargetCard ? 'sc-proof-target-focused' : ''}" style="--cs-accent:${cs.accent};">
            <div>
              <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; flex-wrap:wrap; margin-bottom:14px;">
                <div style="display:flex; gap:6px; flex-wrap:wrap;">${pillarBadges}</div>
                <span style="font-family:var(--font-mono); font-size:12.5px; font-weight:800; color:#10b981; background:rgba(16,185,129,0.12); border:1px solid rgba(16,185,129,0.35); padding:4px 12px; border-radius:999px;">
                  ${cs.headlineMetric}
                </span>
              </div>

              <h3 style="font-family:var(--font-display); font-size:22px; font-weight:800; color:var(--text-primary); margin:0 0 4px;">
                ${cs.company}
              </h3>
              <div style="font-size:13px; font-weight:600; color:var(--text-secondary); margin-bottom:18px;">
                ${cs.sector}
              </div>

              <div style="margin-bottom:14px;">
                <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:#f43f5e; margin-bottom:4px;">
                  Challenge
                </div>
                <p style="font-size:14px; color:var(--text-secondary); line-height:1.6; margin:0;">
                  ${cs.problem}
                </p>
              </div>

              <div style="padding-top:14px; border-top:1px solid var(--border-subtle);">
                <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:#10b981; margin-bottom:4px;">
                  Published Outcome
                </div>
                <p style="font-size:14px; color:var(--text-primary); line-height:1.6; font-weight:500; margin:0;">
                  ${cs.outcome}
                </p>
              </div>
            </div>

            <div style="padding-top:14px; border-top:1px solid var(--border-subtle);">
              ${personaChips ? `
                <div style="font-size:10.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:var(--text-secondary); margin-bottom:6px;">
                  Supported Personas
                </div>
                <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:10px;">
                  ${personaChips}
                </div>
              ` : ''}

              ${agentChips ? `
                <div style="font-size:10.5px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:var(--text-secondary); margin-bottom:6px;">
                  Supported AI Agents
                </div>
                <div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:14px;">
                  ${agentChips}
                </div>
              ` : ''}

              <div style="display:flex; flex-wrap:wrap; gap:10px; align-items:center;">
                <a href="${cs.url}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill" style="padding:6px 12px;">
                  <span>${cs.sourceLabel}</span>
                  <span>&#8599;</span>
                </a>
                ${cs.secondaryUrl ? `
                  <a href="${cs.secondaryUrl}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill" style="padding:6px 12px; opacity:0.9;">
                    <span>${cs.secondaryLabel}</span>
                    <span>&#8599;</span>
                  </a>
                ` : ''}
              </div>
            </div>
          </div>
        `;
      }).join('');

      const sourcesHtml = VERIFIED_RESEARCH_SOURCES.map(src => `
        <div class="sc-src-lib-item" style="padding:22px 24px;">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; margin-bottom:8px;">
              <span style="font-size:11.5px; font-weight:800; color:var(--g-blue); text-transform:uppercase; letter-spacing:0.05em;">${src.org}</span>
              <span class="sc-tech-pill" style="font-size:11px; padding:3px 9px;">${src.type}</span>
            </div>
            <div style="font-weight:800; font-size:15.5px; color:var(--text-primary); line-height:1.42; margin-bottom:8px;">
              ${src.title}
            </div>
            <div style="font-size:13.5px; color:var(--text-secondary); line-height:1.55; margin-bottom:14px;">
              ${src.metric}
            </div>
          </div>
          <a href="${src.url}" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill" style="font-size:12.5px; padding:6px 12px;">
            <span>Open Published Source</span>
            <span>&#8599;</span>
          </a>
        </div>
      `).join('');

      const backToEntityBtnHtml = focusedEntity ? `
        <button type="button" class="back-btn" style="border-color:rgba(16,185,129,0.5); color:#10b981; font-weight:800;"
                onclick="${currentEvidenceFocus.kind === 'agent' ? `openAgentPage('${focusedEntity.id}', true, event)` : `openPersonaPage('${focusedEntity.id}', true, event)`}">
          &larr; Back to ${currentEvidenceFocus.kind === 'agent' ? cleanAgentName(focusedEntity.name) : focusedEntity.name}
        </button>
      ` : '';

      container.innerHTML = `
        <div class="back-bar" style="margin-bottom: 20px;">
          <div style="display:flex; gap:10px; flex-wrap:wrap;">
            ${backToEntityBtnHtml}
            <button type="button" class="back-btn" onclick="goToOrgChart()">&larr; Back to ${pillarCount} Pillars</button>
            <button type="button" class="back-btn" onclick="openCostTabPage('all', null, true)">💰 Cost &amp; ROI</button>
          </div>
          <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <a href="VERIFIED_CASE_STUDIES_AND_RESEARCH_SOURCES.md" target="_blank" class="switch-pill" style="text-decoration:none; padding:8px 14px; font-size:13px; font-weight:700;">
              📄 Citations Dossier (.md) &#8599;
            </a>
          </div>
        </div>

        <!-- Clean Spacious Header -->
        <div class="simple-arch-card" style="padding: 26px 30px; margin-bottom: 20px;">
          <div style="font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:var(--g-blue); margin-bottom:6px;">
            Aligned to Operating Pillars &rarr; Sub-Pillars &rarr; Personas &amp; AI Agents
          </div>
          <h1 style="font-family:var(--font-display); font-size:clamp(26px, 3vw, 36px); font-weight:800; color:var(--text-primary); margin:0 0 8px;">
            Real Case Studies &amp; Verified Benchmarks
          </h1>
          <p style="font-size:15px; color:var(--text-secondary); max-width:960px; line-height:1.6; margin:0 0 20px;">
            Navigate proofs using the exact same <strong>${pillarCount} Operating Pillars &rarr; Sub-Pillars &rarr; Personas &amp; ${agentCount} AI Agents</strong> hierarchy, or click any impact badge across the portal to jump directly to its supporting case study and source.
          </p>

          <!-- 4 Spacious Headline KPI Cards -->
          <div class="sc-ev-kpi-grid" style="margin-bottom: 0; gap: 16px;">
            <div class="sc-ev-kpi-card" style="--kpi-color:#2563eb; padding: 18px 20px;">
              <div>
                <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:var(--text-secondary);">Forecast Error</div>
                <div style="font-family:var(--font-display); font-size:28px; font-weight:800; color:#38bdf8; margin:6px 0;">-20% to -50%</div>
                <div style="font-size:13px; color:var(--text-secondary); line-height:1.5;">Lower forecast error &amp; up to 65% fewer lost sales.</div>
              </div>
              <a href="https://www.mckinsey.com/capabilities/operations/our-insights/ai-driven-operations-forecasting-in-data-light-environments" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill" style="font-size:11.5px; margin-top:10px;">McKinsey &#8599;</a>
            </div>

            <div class="sc-ev-kpi-card" style="--kpi-color:#7c3aed; padding: 18px 20px;">
              <div>
                <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:var(--text-secondary);">Procurement Savings</div>
                <div style="font-family:var(--font-display); font-size:28px; font-weight:800; color:#a855f7; margin:6px 0;">5%–15% Spend</div>
                <div style="font-size:13px; color:var(--text-secondary); line-height:1.5;">Addressable spend savings &amp; 3.7x Procurement AI ROI.</div>
              </div>
              <a href="https://www.thehackettgroup.com/insights/the-ai-procurement-performance-gap-how-leaders-achieve-3-7x-greater-roi/" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill" style="font-size:11.5px; margin-top:10px;">Hackett Group &#8599;</a>
            </div>

            <div class="sc-ev-kpi-card" style="--kpi-color:#ea580c; padding: 18px 20px;">
              <div>
                <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:var(--text-secondary);">Factory Downtime</div>
                <div style="font-family:var(--font-display); font-size:28px; font-weight:800; color:#fb923c; margin:6px 0;">-30% to -50%</div>
                <div style="font-size:13px; color:var(--text-secondary); line-height:1.5;">Unplanned downtime cut &amp; -25% parts backorders (GE).</div>
              </div>
              <a href="https://reports.weforum.org/docs/WEF_Global_Lighthouse_Network_2026.pdf" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill" style="font-size:11.5px; margin-top:10px;">WEF Lighthouse &#8599;</a>
            </div>

            <div class="sc-ev-kpi-card" style="--kpi-color:#10b981; padding: 18px 20px;">
              <div>
                <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.06em; color:var(--text-secondary);">Warehouse &amp; Fleet</div>
                <div style="font-family:var(--font-display); font-size:28px; font-weight:800; color:#10b981; margin:6px 0;">&gt;10% to 15%</div>
                <div style="font-size:13px; color:var(--text-secondary); line-height:1.5;">Pick efficiency (FM Logistic), Walmart (30M mi), UPS ($300M+).</div>
              </div>
              <a href="https://www.informs.org/News-Room/INFORMS-Releases/Awards-Releases/Operations-Research-Enhances-Retail-Truck-Routing-and-Load-Planning-Walmart-Awarded-the-2023-INFORMS-Edelman-Award" target="_blank" rel="noopener noreferrer" class="sc-ext-link-pill" style="font-size:11.5px; margin-top:10px;">INFORMS Edelman &#8599;</a>
            </div>
          </div>
        </div>

        <!-- Hierarchical Operating Pillar -> Sub-Pillar -> Persona & Agent Navigation Bar -->
        <div class="sc-ev-nav-shell">
          <div class="sc-ev-nav-row">
            <span class="sc-ev-nav-label">Operating Pillar:</span>
            ${pillarNavPillsHtml}
          </div>
          ${subPillarNavRowHtml}
          ${entityNavRowHtml}
        </div>

        ${spotlightHtml}

        <!-- 3-Tab Segmented View Selector -->
        <div class="sc-v22-tab-strip">
          <button type="button" class="sc-v22-tab-btn ${currentEvidenceTab === 'cases' ? 'active' : ''}" onclick="switchEvidenceTab('cases')">
            <span>🏢 Enterprise Case Studies</span>
            <span class="sc-v22-tab-count">${filteredCases.length}</span>
          </button>
          <button type="button" class="sc-v22-tab-btn ${currentEvidenceTab === 'benchmarks' ? 'active' : ''}" onclick="switchEvidenceTab('benchmarks')">
            <span>📊 Sub-Pillar Benchmark Matrix</span>
            <span class="sc-v22-tab-count">20</span>
          </button>
          <button type="button" class="sc-v22-tab-btn ${currentEvidenceTab === 'sources' ? 'active' : ''}" onclick="switchEvidenceTab('sources')">
            <span>📚 Primary Research &amp; Standards</span>
            <span class="sc-v22-tab-count">${VERIFIED_RESEARCH_SOURCES.length}</span>
          </button>
        </div>

        ${currentEvidenceTab === 'cases' ? `
          <div class="sc-v22-cs-grid">
            ${caseCardsHtml}
          </div>
        ` : ''}

        ${currentEvidenceTab === 'benchmarks' ? `
          <div class="simple-arch-card" style="padding: 26px 28px;">
            <div style="margin-bottom:18px;">
              <h2 style="font-family:var(--font-display); font-size:22px; font-weight:800; color:var(--text-primary); margin:0 0 4px;">
                Operating Pillar &amp; Sub-Pillar Calibration Matrix
              </h2>
              <p style="font-size:14px; color:var(--text-secondary); margin:0;">
                Every Sub-Pillar target mapped directly to its published industry benchmark and real enterprise proof.
              </p>
            </div>
            <div style="overflow-x:auto;">
              <table style="width:100%; border-collapse:collapse; text-align:left;">
                <thead>
                  <tr style="border-bottom:2px solid var(--border-subtle); font-size:11.5px; text-transform:uppercase; letter-spacing:0.05em; color:var(--text-secondary);">
                    <th style="padding:14px;">Pillar &amp; Sub-Pillar</th>
                    <th style="padding:14px;">Portal Impact</th>
                    <th style="padding:14px;">Published Benchmark</th>
                    <th style="padding:14px;">Enterprise Case Study</th>
                  </tr>
                </thead>
                <tbody>
                  ${pillarRowsHtml}
                </tbody>
              </table>
            </div>
          </div>
        ` : ''}

        ${currentEvidenceTab === 'sources' ? `
          <div class="sc-src-lib-grid" style="gap: 18px;">
            ${sourcesHtml}
          </div>
        ` : ''}
      `;

      showActivePage('pageEvidence');

      if (focusedEntity) {
        setTimeout(() => {
          const spot = document.getElementById('evidenceFocusedSpotlight');
          if (spot) spot.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 40);
      }
    }"""


def build_standalone_variant(base_html: str, hash_target: str, boot_call: str) -> str:
    variant = must_replace(
        base_html,
        """    window.addEventListener('popstate', () => {
      handleUrlHash();
    });""",
        f"""    window.addEventListener('popstate', () => {{
      if (!window.location.hash) {{ window.location.hash = '{hash_target}'; }} handleUrlHash();
    }});""",
        f"{hash_target} popstate hook",
    )
    variant = must_replace(
        variant,
        """      hydrateAssets();
      handleUrlHash();""",
        f"""      hydrateAssets();
      handleUrlHash();
      if (!window.location.hash) {boot_call};""",
        f"{hash_target} boot hook",
    )
    return variant


def apply_upgrades(html: str) -> str:
    # 1. Inject CSS before </style>
    if "CLICKABLE MINIMAL-TEXT IMPACT BOXES & NAVIGATION-ALIGNED PROOF SPOTLIGHT" not in html:
        html = must_replace(html, "  </style>", IMPACT_AND_EVIDENCE_CSS + "\n  </style>", "inject impact & proof css")

    # 2. Persona Page (openPersonaPage): Top impact box + journey pills + bottom agent pills + bottom Persona impact bar
    old_persona_top = """            <div class="persona-stat-highlight" style="border-color: ${dept.color}45;">
              <div class="persona-stat-value" style="color: ${dept.color};">${p.headlineStat || '-85% Toil'}</div>
              <div class="persona-stat-label">${p.toilHoursBefore || '6.5h'} &rarr; ${p.toilHoursAfter || '1.0h'}</div>
            </div>"""
    new_persona_top = """            <button type="button" class="persona-stat-highlight sc-impact-link-box"
                    style="--imp-accent: ${dept.color}; border-color: ${dept.color}55;"
                    onclick="openProofForPersona('${p.id}', event)"
                    title="View supporting case study &amp; benchmark">
              <div class="persona-stat-value" style="color: ${dept.color};">${p.headlineStat || '-85% Toil'} <span class="sc-impact-cue">&#8599;</span></div>
              <div class="persona-stat-label">${p.toilHoursBefore || '6.5h'} &rarr; ${p.toilHoursAfter || '1.0h'}</div>
            </button>"""
    html = must_replace(html, old_persona_top, new_persona_top, "persona top impact box")

    old_persona_step_hdr_pill = """                      ${slot.isToil ? `
                        <span style="font-size:12px; font-weight:700; padding:3px 10px; border-radius:999px; background:rgba(52,168,83,0.14); color:#34a853; border:1px solid rgba(52,168,83,0.35);">
                          ${slot.toilDuration || '2.0 hrs'} &rarr; ${slot.afterDuration || '10 mins'}
                        </span>"""
    new_persona_step_hdr_pill = """                      ${slot.isToil ? `
                        <span class="sc-impact-pill-link"
                              onclick="event.stopPropagation(); openProofForPersona('${p.id}', event)"
                              title="View supporting case study &amp; benchmark">
                          ${slot.toilDuration || '2.0 hrs'} &rarr; ${slot.afterDuration || '10 mins'} <span class="sc-impact-cue">&#8599;</span>
                        </span>"""
    html = must_replace(html, old_persona_step_hdr_pill, new_persona_step_hdr_pill, "persona accordion header impact pill")

    old_persona_improve_pill = """                            <span class="improve-time-saved">⚡ ${slot.toilDuration || '2.0 hrs'} &rarr; ${slot.afterDuration || '10 mins'}</span>"""
    new_persona_improve_pill = """                            <button type="button" class="improve-time-saved sc-impact-pill-link" onclick="openProofForPersona('${p.id}', event)" title="View supporting case study &amp; benchmark">⚡ ${slot.toilDuration || '2.0 hrs'} &rarr; ${slot.afterDuration || '10 mins'} <span class="sc-impact-cue">&#8599;</span></button>"""
    html = must_replace(html, old_persona_improve_pill, new_persona_improve_pill, "persona improve-time-saved pill")

    old_persona_plug_badge = """                                ${plugAgent.badge ? `
                                  <span style="font-family:var(--font-mono); font-size:11px; font-weight:800; padding:2px 9px; border-radius:999px; background:rgba(16,185,129,0.16); color:#10b981; border:1px solid rgba(16,185,129,0.4);">
                                    ${plugAgent.badge}
                                  </span>
                                ` : ''}"""
    new_persona_plug_badge = """                                ${plugAgent.badge ? `
                                  <button type="button" class="sc-impact-pill-link" style="font-size:11px; padding:2px 9px;"
                                          onclick="event.stopPropagation(); openProofForAgent('${plugAgent.id}', event)"
                                          title="View supporting case study &amp; benchmark">
                                    ${plugAgent.badge} <span class="sc-impact-cue">&#8599;</span>
                                  </button>
                                ` : ''}"""
    html = must_replace(html, old_persona_plug_badge, new_persona_plug_badge, "persona step agent badge")

    old_persona_dock_end = """                        <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; flex-wrap:wrap;">
                          <span class="sc-flip-pill" style="color:#10b981; border-color:rgba(16,185,129,0.35);">✦ ${ag.badge || 'High ROI'}</span>
                          <button type="button" class="agent-plug-btn" style="padding:7px 14px; font-size:12.5px;" onclick="event.stopPropagation(); openAgentPage('${ag.id}', true, event)">
                            <span>Open Agent &rarr;</span>
                          </button>
                        </div>
                      </div>
                      <div class="sc-flip-back">
                        <div class="sc-flip-top-row">
                          <span class="sc-flip-kicker">AGENT SUMMARY</span>
                          <span class="sc-flip-hint">↺ Back</span>
                        </div>
                        <div class="sc-flip-back-text">${shortSentence(ag.solution || ag.role, 135)}</div>
                        <div style="display:flex; align-items:center; justify-content:space-between; gap:8px;">
                          <span class="sc-flip-pill">${getAgentBuildClassification(ag).label}</span>
                          <button type="button" class="agent-plug-btn" style="padding:7px 14px; font-size:12.5px;" onclick="event.stopPropagation(); openAgentPage('${ag.id}', true, event)">
                            <span>Open Studio &rarr;</span>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        </div>"""

    new_persona_dock_end = """                        <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; flex-wrap:wrap;">
                          <button type="button" class="sc-impact-pill-link"
                                  onclick="event.stopPropagation(); openProofForAgent('${ag.id}', event)"
                                  title="View supporting case study &amp; benchmark">
                            ✦ ${ag.badge || 'High ROI'} <span class="sc-impact-cue">&#8599;</span>
                          </button>
                          <button type="button" class="agent-plug-btn" style="padding:7px 14px; font-size:12.5px;" onclick="event.stopPropagation(); openAgentPage('${ag.id}', true, event)">
                            <span>Open Agent &rarr;</span>
                          </button>
                        </div>
                      </div>
                      <div class="sc-flip-back">
                        <div class="sc-flip-top-row">
                          <span class="sc-flip-kicker">AGENT SUMMARY</span>
                          <span class="sc-flip-hint">↺ Back</span>
                        </div>
                        <div class="sc-flip-back-text">${shortSentence(ag.solution || ag.role, 135)}</div>
                        <div style="display:flex; align-items:center; justify-content:space-between; gap:8px;">
                          <span class="sc-flip-pill">${getAgentBuildClassification(ag).label}</span>
                          <button type="button" class="agent-plug-btn" style="padding:7px 14px; font-size:12.5px;" onclick="event.stopPropagation(); openAgentPage('${ag.id}', true, event)">
                            <span>Open Studio &rarr;</span>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>

          <!-- Minimal-Text Clickable Bottom Persona Impact Box -->
          <button type="button" class="sc-bottom-impact-bar sc-impact-link-box"
                  style="--imp-accent: ${dept.color};"
                  onclick="openProofForPersona('${p.id}', event)"
                  title="View supporting case study &amp; benchmark">
            <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
              <span class="sc-bottom-impact-kicker">ROLE IMPACT</span>
              <span class="sc-bottom-impact-metric">${p.headlineStat || '-85% Manual Toil'}</span>
            </div>
            <span class="sc-bottom-impact-right">
              <span>${p.toilHoursBefore || '6.5h'} &rarr; ${p.toilHoursAfter || '1.0h'}</span>
              <span class="sc-impact-cue">&#8599;</span>
            </span>
          </button>
        </div>"""
    html = must_replace(html, old_persona_dock_end, new_persona_dock_end, "persona bottom impact box & agent pills")

    # 3. Agent Page (openAgentPage): Top hero impact pill + concise clickable 03 · IMPACT card + bottom Agent impact bar
    old_agent_hero_actions = """              <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                <a href="agent_testing_and_video_playbook.html#agent-${ag.id}"
                   style="text-decoration:none; font-size:13px; font-weight:700; padding:8px 15px; border-radius:999px; background:rgba(56,189,248,0.14); color:#38bdf8; border:1.5px solid rgba(56,189,248,0.42);">
                  📋 Test Prompts &amp; Data &rarr;
                </a>
                <span class="build-tier-badge ${cls.cssClass}">${cls.label}</span>
              </div>"""
    new_agent_hero_actions = """              <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
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
              </div>"""
    html = must_replace(html, old_agent_hero_actions, new_agent_hero_actions, "agent top hero impact pill")

    old_agent_impact_card = """              <div class="sc-flip-card sc-flip-compact" style="--flip-accent:#10b981;" onclick="this.classList.toggle('is-flipped')">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">03 · IMPACT</span>
                      <span class="sc-flip-hint">↻ Flip</span>
                    </div>
                    <div class="sc-flip-big-heading" style="font-size:20px;">
                      <div class="sc-flip-icon-box">🚀</div>
                      <span>${ag.badge || 'Verified ROI'}</span>
                    </div>
                    <div class="sc-agent-card-brief">${shortSentence(ag.outcome, 108)}</div>
                  </div>
                  <div class="sc-flip-back">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">🚀 BUSINESS OUTCOME</span>
                      <span class="sc-flip-hint">↺ Back</span>
                    </div>
                    <div class="sc-flip-back-text">${ag.outcome}</div>
                  </div>
                </div>
              </div>"""

    new_agent_impact_card = """              <div class="sc-flip-card sc-flip-compact sc-impact-link-box"
                   style="--flip-accent:#10b981; --imp-accent:#10b981;"
                   onclick="openProofForAgent('${ag.id}', event)"
                   role="button" tabindex="0"
                   onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();openProofForAgent('${ag.id}', event);}"
                   title="View supporting case study &amp; benchmark">
                <div class="sc-flip-inner">
                  <div class="sc-flip-front">
                    <div class="sc-flip-top-row">
                      <span class="sc-flip-kicker">03 · IMPACT</span>
                      <span class="sc-flip-hint sc-impact-cue">&#8599;</span>
                    </div>
                    <div class="sc-flip-big-heading" style="font-size:20px;">
                      <div class="sc-flip-icon-box">🚀</div>
                      <span>${ag.badge || 'Verified ROI'}</span>
                    </div>
                    <div class="sc-agent-card-brief">${shortSentence(ag.outcome, 76)}</div>
                  </div>
                </div>
              </div>"""
    html = must_replace(html, old_agent_impact_card, new_agent_impact_card, "agent 03 IMPACT clickable card")

    old_agent_bottom_bar = """          <!-- 4. Sleek Collapsed-by-Default Deep-Dive Tab Bar (Cost, Steps, Benchmarks, Governance & Specs) -->
          <div class="agent-deepdive-bar" style="--deep-accent:${dept.color};">"""
    new_agent_bottom_bar = """          <!-- Minimal-Text Clickable Bottom Agent Impact Box -->
          <button type="button" class="sc-bottom-impact-bar sc-impact-link-box"
                  style="--imp-accent:#10b981;"
                  onclick="openProofForAgent('${ag.id}', event)"
                  title="View supporting case study &amp; benchmark">
            <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
              <span class="sc-bottom-impact-kicker">VERIFIED IMPACT</span>
              <span class="sc-bottom-impact-metric">${ag.badge || 'Verified ROI'}</span>
            </div>
            <span class="sc-bottom-impact-right">
              <span>${ag.subPillarName || dept.name}</span>
              <span class="sc-impact-cue">&#8599;</span>
            </span>
          </button>

          <!-- 4. Sleek Collapsed-by-Default Deep-Dive Tab Bar (Cost, Steps, Benchmarks, Governance & Specs) -->
          <div class="agent-deepdive-bar" style="--deep-accent:${dept.color};">"""
    html = must_replace(html, old_agent_bottom_bar, new_agent_bottom_bar, "agent bottom clickable impact bar")

    # 4. Agent Cost & ROI Panel (renderAgentCostAndRoiPanel): make VALUE UNLOCKED card clickable to exact proof
    old_cost_val_card = """            <div class="sc-flip-card sc-flip-compact" style="--flip-accent:#10b981;" onclick="this.classList.toggle('is-flipped')">
              <div class="sc-flip-inner">
                <div class="sc-flip-front">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">🚀 VALUE UNLOCKED</span>
                    <span class="sc-flip-hint">↻ Flip</span>
                  </div>"""
    new_cost_val_card = """            <div class="sc-flip-card sc-flip-compact sc-impact-link-box" style="--flip-accent:#10b981; --imp-accent:#10b981;" onclick="openProofForAgent('${ag.id}', event)" title="View supporting case study &amp; benchmark">
              <div class="sc-flip-inner">
                <div class="sc-flip-front">
                  <div class="sc-flip-top-row">
                    <span class="sc-flip-kicker">🚀 VALUE UNLOCKED</span>
                    <span class="sc-flip-hint sc-impact-cue">&#8599;</span>
                  </div>"""
    html = must_replace(html, old_cost_val_card, new_cost_val_card, "cost panel value unlocked clickable")

    # 5. Directory, Periodic Table, and Mind Map Persona/Agent impact pills -> clickable with event.stopPropagation()
    old_dir_ag_badge = """                          ${ag.badge ? `<div style="font-family:var(--font-mono); font-size:11.5px; color:#10b981; font-weight:700; margin-top:4px;">${ag.badge}</div>` : ''}"""
    new_dir_ag_badge = """                          ${ag.badge ? `<div style="margin-top:5px;"><button type="button" class="sc-impact-pill-link" style="font-size:11px; padding:2px 9px;" onclick="event.stopPropagation(); openProofForAgent('${ag.id}', event)" title="View supporting case study &amp; benchmark">${ag.badge} <span class="sc-impact-cue">&#8599;</span></button></div>` : ''}"""
    html = must_replace(html, old_dir_ag_badge, new_dir_ag_badge, "directory agent impact pill")

    old_dir_p_stat = """                        <div class="human-persona-sub" style="margin-top:3px;">${p.headlineStat || '-85% Manual Toil'}</div>"""
    new_dir_p_stat = """                        <div style="margin-top:5px;"><button type="button" class="sc-impact-pill-link" style="font-size:11px; padding:2px 9px;" onclick="event.stopPropagation(); openProofForPersona('${p.id}', event)" title="View supporting case study &amp; benchmark">${p.headlineStat || '-85% Manual Toil'} <span class="sc-impact-cue">&#8599;</span></button></div>"""
    html = must_replace(html, old_dir_p_stat, new_dir_p_stat, "directory persona impact pill")

    old_pt_badge = """                <span class="pt-side-tag" style="color:#10b981; border-color:rgba(16,185,129,0.35); font-weight:800;">✦ ${selAg.badge}</span>"""
    new_pt_badge = """                <button type="button" class="sc-impact-pill-link" style="font-size:11.5px; padding:4px 10px;" onclick="openProofForAgent('${selAg.id}', event)" title="View supporting case study &amp; benchmark">✦ ${selAg.badge} <span class="sc-impact-cue">&#8599;</span></button>"""
    html = must_replace(html, old_pt_badge, new_pt_badge, "periodic table sidebar impact pill")

    old_mm_ag_badge = """                              ${ag.badge ? `<span style="color:#10b981; font-weight:700;">${ag.badge}</span> · ` : ''}${ag.subPillarName || activeDept.name}"""
    new_mm_ag_badge = """                              ${ag.badge ? `<span class="sc-impact-pill-link" style="font-size:11px; padding:1px 8px; margin-right:4px;" onclick="event.stopPropagation(); openProofForAgent('${ag.id}', event)" title="View supporting case study &amp; benchmark">${ag.badge} &#8599;</span> ` : ''}${ag.subPillarName || activeDept.name}"""
    html = must_replace(html, old_mm_ag_badge, new_mm_ag_badge, "mind map agent impact pill")

    old_mm_p_stat = """                              <div style="font-size:12.5px; color:var(--text-secondary); margin-top:2px;">
                                ${p.headlineStat || '-85% Manual Toil'} · ${p.subPillarName || activeDept.name}
                              </div>"""
    new_mm_p_stat = """                              <div style="font-size:12.5px; color:var(--text-secondary); margin-top:4px; display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
                                <button type="button" class="sc-impact-pill-link" style="font-size:11px; padding:2px 8px;" onclick="event.stopPropagation(); openProofForPersona('${p.id}', event)" title="View supporting case study &amp; benchmark">${p.headlineStat || '-85% Manual Toil'} &#8599;</button>
                                <span>${p.subPillarName || activeDept.name}</span>
                              </div>"""
    html = must_replace(html, old_mm_p_stat, new_mm_p_stat, "mind map persona impact pill")

    # 6. Upgrade getProofForAgent + renderAgentExternalProofCard + openEvidenceHubPage + handleUrlHash
    old_get_proof_fn = """    function getProofForAgent(ag, dept) {
      const spName = (ag && ag.subPillarName) || '';
      const base = SUBPILLAR_PROOF_MAP[spName] || {
        benchOrg: 'McKinsey & ASCM SCOR Digital Standard',
        benchStat: 'AI supply chain orchestration reduces operational cost by 5%–15%, inventory buffers by 20%–35%, and manual planning toil by 70%+.',
        benchUrl: 'https://www.mckinsey.com/industries/industrials/our-insights/distribution-blog/ai-is-transforming-distribution-supply-chains-turning-margin-pressure-into-a-competitive-advantage',
        caseTitle: 'GE Appliances & Unilever × Google Cloud Gemini Enterprise',
        caseStat: 'Enterprise-scale multi-agent deployments on Google Cloud delivering double-digit backorder, logistics, and working-capital improvements.',
        caseUrl: 'https://www.googlecloudpresscorner.com/2026-04-22-GE-Appliances-Reinvents-Manufacturing-Operations-at-Scale-with-Google-Clouds-Gemini-Enterprise'
      };
      return base;
    }"""
    html = must_replace(html, old_get_proof_fn, NEW_EVIDENCE_ENGINE_JS, "replace getProofForAgent with full proof resolver")

    old_ext_proof_btn = """            <button type="button" class="switch-pill" onclick="openEvidenceHubPage('${ag.deptId}', true, event)" style="font-size:12.5px; padding:7px 14px; cursor:pointer; font-weight:700;">
              📚 Open All Case Studies &amp; Sources &rarr;
            </button>"""
    new_ext_proof_btn = """            <button type="button" class="switch-pill" onclick="openProofForAgent('${ag.id}', event)" style="font-size:12.5px; padding:7px 14px; cursor:pointer; font-weight:700;">
              📚 Open Supporting Case Study &amp; Sources &rarr;
            </button>"""
    html = must_replace(html, old_ext_proof_btn, new_ext_proof_btn, "agent external proof drawer button")

    ev_start_marker = "    let currentEvidenceTab = 'cases'; // 'cases' | 'benchmarks' | 'sources'"
    ev_end_marker = "    function handleUrlHash() {"
    ev_s = html.index(ev_start_marker)
    ev_e = html.index(ev_end_marker, ev_s)
    html = html[:ev_s] + NEW_OPEN_EVIDENCE_HUB_JS + "\n\n" + html[ev_e:]

    old_evidence_hash = """      if (hash === 'evidence' || hash.startsWith('evidence/')) {
        const pId = hash.split('/')[1] || 'all';
        openEvidenceHubPage(pId, false);
        return;
      }"""
    new_evidence_hash = """      if (hash === 'evidence' || hash.startsWith('evidence/')) {
        const parts = hash.split('/');
        if (parts[1] === 'agent' && parts[2] && AGENTS[parts[2]]) {
          openProofForAgent(parts[2], null);
          return;
        }
        if (parts[1] === 'persona' && parts[2] && PERSONAS[parts[2]]) {
          openProofForPersona(parts[2], null);
          return;
        }
        if (parts[1] === 'subpillar' && parts[2]) {
          const spId = parts[2];
          const ld = resolveLiveDeptForSubPillar(spId, null);
          currentEvidenceFocus = null;
          currentEvidenceSubPillar = spId;
          openEvidenceHubPage(ld ? ld.id : 'all', false, null, null, spId);
          return;
        }
        const pId = parts[1] || 'all';
        currentEvidenceFocus = null;
        currentEvidenceSubPillar = 'all';
        openEvidenceHubPage(pId, false, null, null, 'all');
        return;
      }"""
    html = must_replace(html, old_evidence_hash, new_evidence_hash, "evidence deep-link hash router")

    return html


def main() -> None:
    index_path = ROOT / "index.html"
    orig_html = index_path.read_text(encoding="utf-8")
    updated_index = apply_upgrades(orig_html)
    index_path.write_text(updated_index, encoding="utf-8")

    periodic_html = build_standalone_variant(
        updated_index, "#periodic", "openPeriodicTablePage('all', null, false)"
    )
    mindmap_html = build_standalone_variant(
        updated_index, "#mindmap", "openMindMapPage('all', null, false)"
    )

    (ROOT / "periodic_table.html").write_text(periodic_html, encoding="utf-8")
    (ROOT / "mind_map.html").write_text(mindmap_html, encoding="utf-8")

    for mirror_dir in ("docs", "zipline_dist"):
        mdir = ROOT / mirror_dir
        if mdir.is_dir():
            for fname in ("index.html", "periodic_table.html", "mind_map.html"):
                shutil.copy2(ROOT / fname, mdir / fname)
                print(f"Synced {mirror_dir}/{fname}")

    print("Successfully wired clickable Persona & Agent impact boxes and navigation-aligned Case Studies & Proofs Hub!")


if __name__ == "__main__":
    main()

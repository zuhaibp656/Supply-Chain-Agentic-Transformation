import re
import json

def apply_to_file(filepath):
    print(f"Applying enhancements to {filepath}...")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update getPersonaStory to return roleOverview or summary
    old_gps = """    function getPersonaStory(p) {
      if (!p) return '';
      const s = String(p.summary || p.story || '').trim();
      if (s && !(s.startsWith('Leads ') && s.includes(' across '))) return s;
      return String(p.story || p.mandate || '').trim();
    }"""

    new_gps = """    function getPersonaStory(p) {
      if (!p) return '';
      const s = String(p.roleOverview || p.summary || p.story || '').trim();
      if (s && !(s.startsWith('Leads ') && s.includes(' across '))) return s;
      return String(p.story || p.mandate || '').trim();
    }"""

    if old_gps in content:
        content = content.replace(old_gps, new_gps)
        print("  Updated getPersonaStory.")

    # 2. Update openValueChainPage stat box and add the Process Story section
    # Target the header stat box
    stat_pattern = r'''<div class="persona-stat-highlight" style="border-color: \$\{vc\.color\}44;">\s*<div class="persona-stat-value" style="color: \$\{vc\.color\};">\$\{vc\.headlineStat\}</div>\s*<div class="persona-stat-label">\$\{vc\.headlineLabel\}</div>\s*</div>'''
    
    new_stat_box = """<button type="button" class="persona-stat-highlight sc-impact-link-box"
                    style="--imp-accent: ${vc.color}; border-color: ${vc.color}55; cursor:pointer; text-align:right;"
                    onclick="openProofForValueChain('${vc.id}', event)"
                    title="View backed industry problem cost data &amp; benchmark research">
              <div style="font-family:var(--font-mono); font-size:10px; font-weight:800; letter-spacing:0.08em; text-transform:uppercase; color:var(--text-secondary); margin-bottom:2px;">Value Stream Benchmark</div>
              <div class="persona-stat-value" style="color: ${vc.color};">${vc.headlineStat} <span class="sc-impact-cue">&#8599;</span></div>
              <div class="persona-stat-label">${vc.headlineLabel}</div>
              <div style="font-family:var(--font-mono); font-size:11px; font-weight:700; color:var(--sc-cyan); margin-top:4px;">
                📊 View Backed Proof &amp; Research &rarr;
              </div>
            </button>"""

    if re.search(stat_pattern, content):
        content = re.sub(stat_pattern, new_stat_box, content)
        print("  Replaced headline stat box with clickable proof link.")

    # Insert Process Story section right above the 6-stage diagram
    story_section = """
          <!-- The End-to-End Process Story: Legacy Siloed Operations vs. Connected Agentic Transformation -->
          <div class="sc-process-story-container" style="margin-bottom: 24px;">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-bottom: 12px;">
              <h3 style="font-family:var(--font-display); font-size:18px; font-weight:800; color:var(--text-primary); margin:0;">
                The Process Story · Legacy Siloed Operations vs. Connected Agentic Transformation
              </h3>
              <button type="button" class="switch-pill" style="font-size:12px; padding:4px 12px; font-weight:700;" onclick="openProofForValueChain('${vc.id}', event)">
                📊 View Benchmark Proof &amp; Research &rarr;
              </button>
            </div>

            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap:16px;">
              <div class="toil-highlight-box" style="padding: 18px 22px; border-left: 4px solid #f43f5e;">
                <div class="toil-top-bar" style="margin-bottom: 10px;">
                  <span class="toil-badge" style="background:rgba(244,63,94,0.18); color:#f43f5e; border-color:rgba(244,63,94,0.4);">
                    ✕ What Traditional Teams Did (The Legacy Siloed Breakdown)
                  </span>
                </div>
                <p style="font-size:14px; line-height:1.7; color:var(--text-secondary); margin:0;">
                  ${vc.legacyStory || vc.problem}
                </p>
              </div>

              <div class="gemini-improve-box" style="padding: 18px 22px; border-left: 4px solid ${vc.color};">
                <div class="improve-top-bar" style="margin-bottom: 10px;">
                  <span class="improve-badge" style="background:${vc.color}22; color:${vc.color}; border-color:${vc.color}55;">
                    ✦ How Our Agentic System Solves It (The Connected Golden Thread Flow)
                  </span>
                </div>
                <p style="font-size:14px; line-height:1.7; color:var(--text-primary); margin:0;">
                  ${vc.agenticStory || vc.solution}
                </p>
              </div>
            </div>
          </div>
"""

    diag_marker = "<!-- 1. FULL-WIDTH INTERACTIVE 6-STAGE ANIMATED PROCESS ARCHITECTURE DIAGRAM -->"
    if diag_marker in content and "sc-process-story-container" not in content:
        content = content.replace(diag_marker, story_section + "\n          " + diag_marker)
        print("  Inserted Process Story section.")

    # 3. Add openProofForValueChain function
    proof_fn = """
    function openProofForValueChain(vcId, ev) {
      if (ev && typeof ev.stopPropagation === 'function') ev.stopPropagation();
      const vc = VALUE_CHAINS[vcId];
      if (!vc) return;

      const existingModal = document.getElementById('vcProofModal');
      if (existingModal) existingModal.remove();

      const modal = document.createElement('div');
      modal.id = 'vcProofModal';
      modal.className = 'sc-modal-backdrop';
      modal.style.display = 'flex';
      modal.style.position = 'fixed';
      modal.style.inset = '0';
      modal.style.backgroundColor = 'rgba(0, 0, 0, 0.78)';
      modal.style.backdropFilter = 'blur(6px)';
      modal.style.alignItems = 'center';
      modal.style.justifyContent = 'center';
      modal.style.zIndex = '999999';
      modal.onclick = (e) => { if (e.target === modal) modal.remove(); };

      modal.innerHTML = `
        <div class="sc-modal-card" style="max-width: 840px; width: 92vw; max-height: 90vh; overflow-y: auto; background: var(--bg-card); border: 1px solid var(--border-subtle); border-top: 5px solid ${vc.color}; border-radius: 18px; padding: 28px 32px; box-shadow: 0 25px 60px rgba(0,0,0,0.5);" onclick="event.stopPropagation()">
          <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:16px; margin-bottom: 18px;">
            <div>
              <span style="padding:4px 10px; border-radius:6px; background:${vc.color}22; color:${vc.color}; font-family:var(--font-mono); font-size:11px; font-weight:800; text-transform:uppercase;">
                Empirical Benchmark &amp; Case Study Proof
              </span>
              <h2 style="font-family:var(--font-display); font-size:23px; font-weight:800; color:var(--text-primary); margin:6px 0 3px 0;">
                ${vc.proofTitle || vc.title}
              </h2>
              <div style="font-size:14.5px; color:${vc.color}; font-weight:700;">
                ${vc.headlineStat} · ${vc.headlineLabel}
              </div>
            </div>
            <button type="button" class="back-btn" style="padding:6px 12px; font-size:20px; line-height:1;" onclick="document.getElementById('vcProofModal').remove()">
              &times;
            </button>
          </div>

          <div style="display:flex; flex-direction:column; gap:16px; margin-bottom: 24px;">
            <!-- 01: Backed Industry Benchmark -->
            <div class="sc-proof-box" style="border-left: 4px solid #f43f5e; padding: 16px 20px; background: rgba(244,63,94,0.06); border-radius: 10px;">
              <div style="font-family:var(--font-mono); font-size:11px; font-weight:800; text-transform:uppercase; color:#f43f5e; margin-bottom:6px;">
                📊 01 · Published Industry Problem Benchmark &amp; Citations
              </div>
              <p style="font-size:14px; line-height:1.68; color:var(--text-primary); margin:0;">
                ${vc.proofBenchmark || vc.problem}
              </p>
            </div>

            <!-- 02: Where We Are Coming From -->
            <div class="sc-proof-box" style="border-left: 4px solid #eab308; padding: 16px 20px; background: rgba(234,179,8,0.06); border-radius: 10px;">
              <div style="font-family:var(--font-mono); font-size:11px; font-weight:800; text-transform:uppercase; color:#eab308; margin-bottom:6px;">
                🏗️ 02 · Where We Are Coming From (The Legacy Architecture Flaw)
              </div>
              <p style="font-size:14px; line-height:1.68; color:var(--text-secondary); margin:0;">
                ${vc.proofRootCause || vc.toilHoursBefore}
              </p>
            </div>

            <!-- 03: What Has Helped & What We Have Done for Others -->
            <div class="sc-proof-box" style="border-left: 4px solid #10b981; padding: 16px 20px; background: rgba(16,185,129,0.06); border-radius: 10px;">
              <div style="font-family:var(--font-mono); font-size:11px; font-weight:800; text-transform:uppercase; color:#10b981; margin-bottom:6px;">
                🚀 03 · What Has Helped &amp; Documented Enterprise Outcomes
              </div>
              <p style="font-size:14px; line-height:1.68; color:var(--text-primary); margin:0 0 8px 0;">
                ${vc.proofSolutionOutcomes || vc.solution}
              </p>
              <div style="font-size:13px; font-weight:700; color:var(--text-secondary);">
                <strong>Verified Deployments:</strong> ${vc.proofDeployments || 'Consumer goods leaders, Fortune 500 manufacturers, and omnichannel logistics fleets.'}
              </div>
            </div>
          </div>

          <div style="display:flex; justify-content:flex-end; gap:12px; border-top: 1px solid var(--border-subtle); padding-top: 16px;">
            <button type="button" class="back-btn" onclick="document.getElementById('vcProofModal').remove()">
              Close
            </button>
            <button type="button" class="agent-plug-btn" style="padding:10px 20px; font-size:13.5px; font-weight:800;" onclick="document.getElementById('vcProofModal').remove(); openEvidenceHubPage('all', true, event);">
              Open Full Cost &amp; Proof Hub &rarr;
            </button>
          </div>
        </div>
      `;

      document.body.appendChild(modal);
    }
"""

    if "function openProofForValueChain" not in content:
        # Insert after openValueChainPage or selectVcStage
        anchor = "function selectVcStage"
        if anchor in content:
            content = content.replace(anchor, proof_fn + "\n    " + anchor)
            print("  Inserted openProofForValueChain function.")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Enhancements written to {filepath} successfully.")

if __name__ == "__main__":
    apply_to_file("build_site.py")
    apply_to_file("scripts/build_site.py")
    apply_to_file("index.html")
    apply_to_file("docs/index.html")
    apply_to_file("zipline_dist/index.html")

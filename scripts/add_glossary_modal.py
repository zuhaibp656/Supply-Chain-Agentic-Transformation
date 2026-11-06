"""Add Executive Supply Chain Abbreviation & Terminology Guide modal to build_site.py."""

import json
from pathlib import Path
from enterprise_twin.tools.abbreviation_expander import DOMAIN_ABBREVIATIONS

def main():
    build_file = Path("build_site.py")
    code = build_file.read_text(encoding="utf-8")

    if "id=\"abbreviationGlossaryModal\"" in code:
        print("abbreviationGlossaryModal already present in build_site.py.")
        return

    glossary_json = json.dumps(DOMAIN_ABBREVIATIONS, indent=2)

    modal_html = f'''
  <!-- =========================================================================
       SUPPLY CHAIN ABBREVIATION & TERMINOLOGY GUIDE MODAL (EXECUTIVE GLOSSARY)
       ========================================================================= -->
  <div id="abbreviationGlossaryModal" class="modal-backdrop" style="display:none; position:fixed; inset:0; z-index:99999; background:rgba(0,0,0,0.78); backdrop-filter:blur(10px); align-items:center; justify-content:center; padding:20px;">
    <div style="background:var(--bg-card, #0f172a); border:1px solid rgba(56,189,248,0.35); border-radius:18px; width:100%; max-width:980px; max-height:88vh; display:flex; flex-direction:column; box-shadow:0 25px 60px rgba(0,0,0,0.6); overflow:hidden;">
      
      <!-- Modal Header -->
      <div style="padding:20px 26px; border-bottom:1px solid rgba(255,255,255,0.08); display:flex; justify-content:space-between; align-items:flex-start; gap:16px; background:rgba(56,189,248,0.04);">
        <div>
          <div style="display:flex; align-items:center; gap:10px;">
            <span style="font-size:22px;">📖</span>
            <h3 style="font-family:var(--font-display, inherit); font-size:20px; font-weight:800; color:var(--text-primary, #f8fafc); margin:0;">
              Executive Supply Chain Abbreviation &amp; Terminology Guide
            </h3>
          </div>
          <p style="font-size:13.5px; color:var(--text-secondary, #94a3b8); margin:6px 0 0; line-height:1.5;">
            Every supply chain, regulatory, and enterprise twin acronym explained in full plain English—so non-technical stakeholders and executives never have to guess.
          </p>
        </div>
        <button type="button" onclick="closeAbbreviationGlossaryModal()" style="background:rgba(255,255,255,0.08); border:none; color:var(--text-secondary, #94a3b8); width:32px; height:32px; border-radius:50%; font-size:18px; cursor:pointer; display:flex; align-items:center; justify-content:center;" title="Close (Esc)">&times;</button>
      </div>

      <!-- Search & Category Filters -->
      <div style="padding:16px 26px; border-bottom:1px solid rgba(255,255,255,0.06); display:flex; flex-wrap:wrap; gap:12px; align-items:center; background:rgba(0,0,0,0.15);">
        <div style="position:relative; flex:1; min-width:260px;">
          <input type="text" id="glossarySearchInput" oninput="renderFilteredGlossary()" placeholder="Search acronym (e.g. SCOT, CBAM, TM&amp;D, OTIF, RMA, OEE)..." style="width:100%; padding:10px 14px 10px 36px; border-radius:10px; border:1px solid rgba(56,189,248,0.3); background:rgba(15,23,42,0.9); color:var(--text-primary, #fff); font-size:13.5px; outline:none;" />
          <span style="position:absolute; left:12px; top:11px; font-size:14px; color:#64748b;">🔍</span>
        </div>
        <div style="display:flex; gap:6px; flex-wrap:wrap;">
          <button type="button" class="glossary-filter-pill active" onclick="setGlossaryCategory('all', this)" style="padding:6px 12px; border-radius:20px; font-size:12px; font-weight:700; cursor:pointer; border:1px solid #38bdf8; background:#38bdf8; color:#0f172a;">All Terms</button>
          <button type="button" class="glossary-filter-pill" onclick="setGlossaryCategory('Planning', this)" style="padding:6px 12px; border-radius:20px; font-size:12px; font-weight:700; cursor:pointer; border:1px solid rgba(255,255,255,0.12); background:transparent; color:var(--text-secondary, #94a3b8);">Planning &amp; AI</button>
          <button type="button" class="glossary-filter-pill" onclick="setGlossaryCategory('Logistics', this)" style="padding:6px 12px; border-radius:20px; font-size:12px; font-weight:700; cursor:pointer; border:1px solid rgba(255,255,255,0.12); background:transparent; color:var(--text-secondary, #94a3b8);">Logistics</button>
          <button type="button" class="glossary-filter-pill" onclick="setGlossaryCategory('Regulatory', this)" style="padding:6px 12px; border-radius:20px; font-size:12px; font-weight:700; cursor:pointer; border:1px solid rgba(255,255,255,0.12); background:transparent; color:var(--text-secondary, #94a3b8);">Regulatory &amp; ESG</button>
        </div>
      </div>

      <!-- Grid of Abbreviations -->
      <div id="glossaryCardsContainer" style="padding:22px 26px; overflow-y:auto; display:grid; grid-template-columns:repeat(auto-fill, minmax(380px, 1fr)); gap:14px; flex:1;">
        <!-- Rendered dynamically -->
      </div>
      
      <!-- Footer Note -->
      <div style="padding:12px 26px; border-top:1px solid rgba(255,255,255,0.06); font-size:12px; color:var(--text-secondary, #94a3b8); display:flex; justify-content:space-between; align-items:center; background:rgba(0,0,0,0.12);">
        <span>Mandate: All enterprise twins, cards, badges, and case studies automatically display the full form alongside acronyms.</span>
        <button type="button" onclick="closeAbbreviationGlossaryModal()" style="padding:6px 14px; border-radius:8px; border:1px solid rgba(255,255,255,0.15); background:rgba(255,255,255,0.06); color:var(--text-primary, #fff); font-size:12px; font-weight:700; cursor:pointer;">Close</button>
      </div>

    </div>
  </div>

  <script>
    const SC_ABBREVIATIONS = {glossary_json};
    let activeGlossaryCategory = 'all';

    function openAbbreviationGlossaryModal() {{
      const m = document.getElementById('abbreviationGlossaryModal');
      if (m) {{
        m.style.display = 'flex';
        renderFilteredGlossary();
        setTimeout(() => {{
          const inp = document.getElementById('glossarySearchInput');
          if (inp) inp.focus();
        }}, 50);
      }}
    }}

    function closeAbbreviationGlossaryModal() {{
      const m = document.getElementById('abbreviationGlossaryModal');
      if (m) m.style.display = 'none';
    }}

    function setGlossaryCategory(cat, btn) {{
      activeGlossaryCategory = cat;
      document.querySelectorAll('.glossary-filter-pill').forEach(b => {{
        b.style.background = 'transparent';
        b.style.color = 'var(--text-secondary, #94a3b8)';
        b.style.borderColor = 'rgba(255,255,255,0.12)';
      }});
      if (btn) {{
        btn.style.background = '#38bdf8';
        btn.style.color = '#0f172a';
        btn.style.borderColor = '#38bdf8';
      }}
      renderFilteredGlossary();
    }}

    function renderFilteredGlossary() {{
      const container = document.getElementById('glossaryCardsContainer');
      if (!container) return;
      const q = (document.getElementById('glossarySearchInput')?.value || '').trim().toLowerCase();

      const filtered = SC_ABBREVIATIONS.filter(item => {{
        const matchesCat = activeGlossaryCategory === 'all' || item.category.toLowerCase().includes(activeGlossaryCategory.toLowerCase());
        const matchesQuery = !q || item.abbr.toLowerCase().includes(q) || item.full_name.toLowerCase().includes(q) || item.definition.toLowerCase().includes(q);
        return matchesCat && matchesQuery;
      }});

      if (filtered.length === 0) {{
        container.innerHTML = '<div style="grid-column:1/-1; text-align:center; padding:40px; color:#94a3b8;">No abbreviations match your search query.</div>';
        return;
      }}

      container.innerHTML = filtered.map(item => `
        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:16px 18px; display:flex; flex-direction:column; gap:8px;">
          <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
            <span style="font-size:12px; font-weight:800; font-family:var(--font-mono, monospace); background:rgba(56,189,248,0.15); color:#38bdf8; border:1px solid rgba(56,189,248,0.3); border-radius:6px; padding:3px 8px;">
              ${{item.abbr}}
            </span>
            <span style="font-size:11px; color:#94a3b8; font-weight:600;">
              ${{item.category}}
            </span>
          </div>
          <div style="font-size:14.5px; font-weight:700; color:var(--text-primary, #f8fafc); line-height:1.35;">
            ${{item.full_name}}
          </div>
          <div style="font-size:12.5px; color:var(--text-secondary, #94a3b8); line-height:1.55;">
            ${{item.definition}}
          </div>
        </div>
      `).join('');
    }}

    document.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') {{
        closeAbbreviationGlossaryModal();
      }}
    }});
  </script>
'''

    code = code.replace("</body>", modal_html + "\n</body>")
    build_file.write_text(code, encoding="utf-8")
    print("Successfully added Abbreviation Glossary Modal to build_site.py.")

if __name__ == "__main__":
    main()

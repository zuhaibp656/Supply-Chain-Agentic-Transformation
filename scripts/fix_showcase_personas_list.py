import re

with open("build_site.py", "r", encoding="utf-8") as f:
    content = f.read()

target_start = "<!-- Personas & Their Day-in-the-Life Agentic Journeys (Built per Persona Journey) -->"
target_end = "<!-- Collapsible Dropdown Drawer for Systems of Record & Solver Stack -->"

if target_start in content and target_end in content:
    start_idx = content.find(target_start)
    end_idx = content.find(target_end)

    clean_persona_list_block = """<!-- Personas in this Vertical (Clean, Uncongested Click-to-Open List) -->
          <div style="margin-top: 24px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.08);">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:14px;">
              <div style="font-size:15px; font-weight:800; color:#fff; display:flex; align-items:center; gap:8px;">
                <span class="accent-dot" style="background:${dept.color}; box-shadow:0 0 10px ${dept.color};"></span>
                <span>Personas in ${dept.name} (${dept.personaIds.length} Core Roles)</span>
              </div>
              <div style="font-size:12px; color:var(--text-muted);">
                Click any persona to open their dedicated schedule &amp; AI agents &rarr;
              </div>
            </div>

            <div class="dept-personas-list" style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:12px;">
              ${dept.personaIds.map(pid => {
                const p = PERSONAS[pid];
                if (!p) return '';
                return `
                  <div class="persona-link-card" onclick="openPersonaPage('${p.id}', true, event)">
                    <div class="persona-link-left">
                      <div class="persona-emoji">${p.icon}</div>
                      <div>
                        <div class="persona-link-name">${p.name}</div>
                        <div class="persona-link-role">${p.role}</div>
                      </div>
                    </div>
                    <span class="persona-open-arrow" style="color:${dept.color};">Open &rarr;</span>
                  </div>
                `;
              }).join('')}
            </div>
          </div>

          """

    content = content[:start_idx] + clean_persona_list_block + content[end_idx:]
    print("Successfully replaced congested persona section with clean click-to-open persona list.")
else:
    print("Error: Target markers not found in build_site.py!")

with open("build_site.py", "w", encoding="utf-8") as f:
    f.write(content)


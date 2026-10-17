import re

with open("build_site.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the showcase-grid and 4-quadrant section in renderDepartmentShowcaseBox
old_showcase_block_pattern = r'<div class="showcase-grid">[\s\S]*?<!-- Column 3: Personas in this Vertical -->[\s\S]*?</div>\s*</div>\s*</div>'

new_showcase_block = """<!-- Executive Problem, Solution & Business Value Grid (CFO Model) -->
          <div class="showcase-exec-grid" style="display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap:16px; margin: 20px 0 16px;">
            <!-- Column 1: Problem / Manual Toil -->
            <div class="showcase-panel" style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(239, 68, 68, 0.28); border-radius: 14px; padding: 18px 20px;">
              <div class="panel-tag" style="color: #f87171; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
                <span>✕ The Critical Problem · Legacy Process Gaps</span>
              </div>
              <div class="panel-metric" style="font-size:20px; font-weight:800; color:#fff; margin-bottom:12px;">${dept.toilMetric}</div>
              <ul class="clean-list" style="list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:10px;">
                ${dept.toilBullets.map(b => `
                  <li style="display:flex; align-items:flex-start; gap:8px; font-size:13.5px; color:#cbd5e1; line-height:1.5;">
                    <span class="bullet" style="color: #f87171; font-weight:bold; flex-shrink:0;">▸</span>
                    <span>${formatRichText(b)}</span>
                  </li>
                `).join('')}
              </ul>
            </div>

            <!-- Column 2: Agentic Solution -->
            <div class="showcase-panel" style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(16, 185, 129, 0.28); border-radius: 14px; padding: 18px 20px;">
              <div class="panel-tag" style="color: #34d399; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
                <span>✦ The AI Solution · Gemini &amp; Math Solvers</span>
              </div>
              <div class="panel-metric" style="font-size:20px; font-weight:800; color:#fff; margin-bottom:12px;">${dept.impactMetric}</div>
              <ul class="clean-list" style="list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:10px;">
                ${dept.impactBullets.map(b => `
                  <li style="display:flex; align-items:flex-start; gap:8px; font-size:13.5px; color:#cbd5e1; line-height:1.5;">
                    <span class="bullet" style="color: #34d399; font-weight:bold; flex-shrink:0;">▸</span>
                    <span>${formatRichText(b)}</span>
                  </li>
                `).join('')}
              </ul>
            </div>

            <!-- Column 3: Quantified Business Value & Working Capital Impact -->
            <div class="showcase-panel" style="background: rgba(15, 23, 42, 0.85); border: 1px solid ${dept.color}44; border-radius: 14px; padding: 18px 20px; display:flex; flex-direction:column; justify-content:space-between;">
              <div>
                <div class="panel-tag" style="color: ${dept.color}; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
                  <span>💎 Strategic Value &amp; Bottom-Line Outcomes</span>
                </div>
                <div class="panel-metric" style="font-size:20px; font-weight:800; color:#fff; margin-bottom:10px;">
                  ${dept.vNum} · ${dept.tagline}
                </div>
                <div style="font-size:13px; color:#94a3b8; line-height:1.5; margin-bottom:14px;">
                  ${dept.coreQuestion || dept.subtitle}
                </div>
                <div style="display:flex; flex-direction:column; gap:8px; font-size:12.5px; color:#cbd5e1;">
                  <div style="display:flex; justify-content:space-between; padding:6px 10px; background:rgba(255,255,255,0.04); border-radius:8px;">
                    <span style="color:#94a3b8;">Operational Horizon:</span>
                    <strong style="color:#fff;">${dept.horizon}</strong>
                  </div>
                  <div style="display:flex; justify-content:space-between; padding:6px 10px; background:rgba(255,255,255,0.04); border-radius:8px;">
                    <span style="color:#94a3b8;">Enterprise Flow:</span>
                    <strong style="color:#38bdf8;">${dept.flow || 'Physical & Signal Flow'}</strong>
                  </div>
                  <div style="display:flex; justify-content:space-between; padding:6px 10px; background:rgba(255,255,255,0.04); border-radius:8px;">
                    <span style="color:#94a3b8;">Human-in-the-Loop Gate:</span>
                    <strong style="color:#34d399;">100% Signed ERP Writeback</strong>
                  </div>
                </div>
              </div>

              <div style="margin-top:14px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.08); display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:12px; color:#94a3b8;">${dept.personaIds.length} Personas · ${dept.agentIds.length} Agents</span>
                <button type="button" class="switch-pill" style="font-size:12px; padding:6px 14px;" onclick="openPersonasDirectoryPage('${dept.id}', '', true)">
                  View in Directory &rarr;
                </button>
              </div>
            </div>
          </div>

          <!-- Vertical Operational & Distribution Workflow Sequence -->
          ${renderVerticalWorkflowStrip(dept)}

          <!-- Personas & Their Day-in-the-Life Agentic Journeys (Built per Persona Journey) -->
          <div class="showcase-personas-section" style="margin-top: 26px;">
            <div style="display:flex; justify-content:space-between; align-items:flex-end; flex-wrap:wrap; gap:12px; margin-bottom:18px;">
              <div>
                <div style="font-size:18px; font-weight:800; color:#fff; display:flex; align-items:center; gap:8px;">
                  <span>👥 Personas &amp; Their Day-in-the-Life Agentic Journeys in ${dept.name}</span>
                </div>
                <div style="font-size:13px; color:#94a3b8; margin-top:3px;">
                  See how dedicated Google Cloud AI Agents intercept manual bottlenecks across each persona's daily workflow—converting hours of spreadsheet toil into autonomous, verified decisions.
                </div>
              </div>
              <div style="font-size:12px; color:var(--text-muted);">
                ${dept.personaIds.length} Core Operational Roles
              </div>
            </div>

            <div class="persona-journeys-container" style="display:flex; flex-direction:column; gap:16px;">
              ${dept.personaIds.map(pid => {
                const p = PERSONAS[pid];
                if (!p) return '';
                const daySlots = (p.dayInLife || []).slice(0, 4);
                const plugAgents = (p.agentIds || []).map(aid => AGENTS[aid]).filter(Boolean);

                return `
                  <div class="persona-journey-card" style="background:rgba(15,23,42,0.85); border:1px solid rgba(255,255,255,0.08); border-left:4px solid ${dept.color}; border-radius:14px; padding:18px 20px;">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:14px; margin-bottom:14px;">
                      <div style="display:flex; align-items:center; gap:12px;">
                        <div style="width:44px; height:44px; border-radius:10px; background:rgba(255,255,255,0.06); display:flex; align-items:center; justify-content:center; font-size:24px;">
                          ${p.icon}
                        </div>
                        <div>
                          <div style="display:flex; align-items:center; gap:8px;">
                            <span style="font-size:16px; font-weight:800; color:#fff;">${p.name}</span>
                            <span style="font-size:11px; padding:2px 8px; border-radius:999px; background:${dept.color}22; color:${dept.color}; font-weight:700; border:1px solid ${dept.color}44;">${dept.name}</span>
                          </div>
                          <div style="font-size:13px; color:#cbd5e1; margin-top:2px;">${p.role}</div>
                        </div>
                      </div>

                      <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
                        <div style="display:inline-flex; align-items:center; gap:6px; font-size:12px; padding:5px 12px; border-radius:8px; background:rgba(0,0,0,0.4); border:1px solid rgba(255,255,255,0.1);">
                          <span style="color:#f87171; font-weight:600;">🔴 ${p.toilHoursBefore}</span>
                          <span style="color:#64748b;">&rarr;</span>
                          <span style="color:#34d399; font-weight:700;">🟢 ${p.toilHoursAfter}</span>
                        </div>
                        <button type="button" class="switch-pill" style="font-size:12px; padding:6px 12px;" onclick="openPersonaPage('${p.id}', true, event)">
                          Explore Full Day Schedule &rarr;
                        </button>
                      </div>
                    </div>

                    <div style="font-size:13px; color:#94a3b8; line-height:1.55; margin-bottom:14px;">
                      ${formatRichText(p.summary)}
                    </div>

                    <!-- 4-Stage Operational Journey Strip -->
                    <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap:10px; margin-bottom:14px;">
                      ${daySlots.map((slot, sIdx) => {
                        const slotAgent = slot.agentId ? AGENTS[slot.agentId] : null;
                        const stageLabels = ['🌅 1. Morning Sensing & Intake', '⚡ 2. Automated Simulation', '🎯 3. Decision Recommendation', '✍️ 4. 1-Click ERP Writeback'];
                        return `
                          <div style="background:rgba(6,10,18,0.7); border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding:10px 12px; display:flex; flex-direction:column; justify-content:space-between;">
                            <div>
                              <div style="display:flex; justify-content:space-between; align-items:center; font-size:11px; margin-bottom:4px;">
                                <span style="font-weight:700; color:${slot.isToil ? '#f87171' : '#38bdf8'};">${stageLabels[sIdx] || slot.time}</span>
                                <span style="color:#64748b;">${slot.time}</span>
                              </div>
                              <div style="font-size:12.5px; font-weight:700; color:#fff; margin-bottom:4px;">${slot.task}</div>
                              <div style="font-size:11.5px; color:#94a3b8; line-height:1.4;">${formatRichText(slot.after || slot.activity || slot.before)}</div>
                            </div>
                            ${slotAgent ? `
                              <div style="margin-top:8px; padding-top:6px; border-top:1px dashed rgba(255,255,255,0.08); font-size:11px; color:#34d399; display:flex; align-items:center; gap:4px;">
                                <span>⚡ Powered by:</span>
                                <strong style="color:#fff; cursor:pointer;" onclick="openAgentPage('${slotAgent.id}', true, event)">${slotAgent.name}</strong>
                              </div>
                            ` : ''}
                          </div>
                        `;
                      }).join('')}
                    </div>

                    <!-- Powered by AI Agents Buttons -->
                    <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; padding-top:10px; border-top:1px solid rgba(255,255,255,0.06);">
                      <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                        <span style="font-size:11.5px; font-weight:700; color:#94a3b8; text-transform:uppercase; letter-spacing:0.05em;">Dedicated AI Agents:</span>
                        ${plugAgents.map(ag => `
                          <button type="button" class="switch-pill" style="font-size:11.5px; padding:4px 10px; background:rgba(56,189,248,0.1); border-color:rgba(56,189,248,0.3); color:#38bdf8;" onclick="openAgentPage('${ag.id}', true, event)">
                            <span>⚡ ${ag.name} (${ag.badge})</span>
                          </button>
                        `).join('')}
                      </div>
                      <div style="display:flex; align-items:center; gap:8px;">
                        ${plugAgents.length > 0 ? `
                          <button type="button" class="switch-pill" style="font-size:11px; padding:4px 8px; color:#94a3b8;" onclick="openAgentBlueprintPage('${plugAgents[0].id}', true, event)">
                            🏗️ High-Code Blueprint &rarr;
                          </button>
                        ` : ''}
                      </div>
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>"""

# Find the exact segment in content
start_marker = '<div class="showcase-grid">'
end_marker = '<!-- Collapsible Dropdown Drawer for Systems of Record & Solver Stack -->'

if start_marker in content and end_marker in content:
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    content = content[:start_idx] + new_showcase_block + "\n\n          " + content[end_idx:]
    print("Replaced showcase-grid and 4-quadrant section with executive CFO Problem/Solution/Value + Persona Journey sections.")
else:
    print("Error: markers not found in content!")

with open("build_site.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Pass 2 of build_site.py complete.")

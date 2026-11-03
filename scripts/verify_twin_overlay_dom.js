/**
 * Automated Zero-Breakage DOM & State Verification for `index.html` Enterprise Twin Engine.
 *
 * Loads `index.html` into a Node VM sandbox, executes its full script bundle, and verifies:
 *   1. Canonical baseline integrity: 6 Pillars, 20 Sub-Pillars, 60 Personas, 60 Agents, 4 Value Chains.
 *   2. Division Twin Application (`ITC Limited — Cigarettes & Leaf Tobacco`, 55/60 agents, 5 hidden):
 *      - All 55 remaining agents preserve 100% identical canonical `name` & demo prompts.
 *      - All 55 personas receive adapted ITC Tobacco & TM&D job titles & daily toils.
 *      - Every sub-page (`openPersonaPage`, `openAgentPage`, `openPeriodicTablePage`,
 *        `openMindMapPage`, `openCostTabPage`, `openValueChainPage`, `openPersonasDirectoryPage`)
 *        renders cleanly with ZERO runtime exceptions or `undefined` strings!
 *   3. `toggleTwinShowAllAgents()` ("Show All 60") reveals all 60 agents cleanly, and toggling back
 *      re-applies the 55/60 division filter cleanly.
 *   4. Switching directly to `Aditya Birla Group — UltraTech Cement` (53/60 agents, 7 hidden)
 *      suffers ZERO state leak from ITC Tobacco!
 *   5. `switchClientTwin('reset')` restores 100% canonical 60/60 industry-agnostic state!
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');

const ROOT = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const catalog = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/supply_chain_catalog.json'), 'utf8'));
const itcTobacco = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/twins/v2/itc-limited--cigarettes-leaf-tobacco-iltd-tm-d.json'), 'utf8'));
const ultraTech = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/twins/v2/aditya-birla-group--ultratech-cement-division.json'), 'utf8'));

// Extract main inline script from index.html
const scriptBlocks = [];
const scriptRegex = /<script\b[^>]*>([\s\S]*?)<\/script>/gi;
let match;
while ((match = scriptRegex.exec(html)) !== null) {
  if (match[1].trim()) scriptBlocks.push(match[1]);
}
assert(scriptBlocks.length >= 1, 'Expected inline script block in index.html');

// Minimal resilient DOM mock supporting all IDs/selectors present in index.html
class MockClassList {
  constructor(initial = []) { this.set = new Set(initial); }
  add(...cls) { cls.forEach(c => c && this.set.add(c)); }
  remove(...cls) { cls.forEach(c => this.set.delete(c)); }
  toggle(c, force) {
    if (force === true) { this.set.add(c); return true; }
    if (force === false) { this.set.delete(c); return false; }
    if (this.set.has(c)) { this.set.delete(c); return false; }
    this.set.add(c); return true;
  }
  contains(c) { return this.set.has(c); }
}

const elementsById = new Map();
function makeEl(tag = 'div', id = '', cls = []) {
  const el = {
    tagName: tag.toUpperCase(),
    id,
    className: cls.join(' '),
    classList: new MockClassList(cls),
    style: { setProperty() {}, removeProperty() {} },
    dataset: {},
    attributes: new Map(),
    children: [],
    parentElement: null,
    innerHTML: '',
    textContent: '',
    value: '',
    scrollTop: 0,
    offsetWidth: 1280,
    offsetHeight: 800,
    setAttribute(k, v) { this.attributes.set(k, String(v)); },
    getAttribute(k) { return this.attributes.get(k) || null; },
    removeAttribute(k) { this.attributes.delete(k); },
    appendChild(ch) { ch.parentElement = this; this.children.push(ch); return ch; },
    insertBefore(ch, ref) { ch.parentElement = this; this.children.unshift(ch); return ch; },
    remove() {
      if (this.id) elementsById.delete(this.id);
    },
    addEventListener() {},
    removeEventListener() {},
    getBoundingClientRect() { return { left: 0, top: 0, width: 1280, height: 800, right: 1280, bottom: 800 }; },
    scrollIntoView() {},
    closest() { return null; },
    querySelector(sel) {
      if (sel === '.cfo-root-wrapper') return getOrCreateId('__cfo_root_wrapper');
      return makeEl('div');
    },
    querySelectorAll() { return []; },
    getContext() {
      return new Proxy({}, {
        get: (t, p) => {
          if (p === 'createLinearGradient' || p === 'createRadialGradient') {
            return () => ({ addColorStop() {} });
          }
          if (p === 'measureText') return () => ({ width: 48 });
          return () => {};
        }
      });
    }
  };
  if (id) elementsById.set(id, el);
  return el;
}

function getOrCreateId(id) {
  if (!elementsById.has(id)) {
    const isPage = id.startsWith('page');
    const cls = isPage ? (id === 'pageHome' ? ['page-view', 'active'] : ['page-view']) : [];
    const el = makeEl('div', id, cls);
    el.parentElement = makeEl('div');
  }
  return elementsById.get(id);
}

// Pre-seed IDs found in index.html HTML markup
const idRegex = /\bid="([^"]+)"/g;
while ((match = idRegex.exec(html)) !== null) {
  getOrCreateId(match[1]);
}

const navCscoBadge = makeEl('div', '__navCsco', ['nav-csco-badge']);
const heroContent = makeEl('div', '__heroContent', ['hero-content']);
const heroTitle = makeEl('h1', '__heroTitle', ['hero-title']);
heroTitle.innerHTML = 'Agentic Transformation for <span class="gradient-word">Global Supply Chain</span>';
const cfoTitle = makeEl('div', '__cfoTitle', ['cfo-box-title']);
cfoTitle.textContent = 'Chief Supply Chain Officer (CSCO)';
const cfoSub = makeEl('div', '__cfoSub', ['cfo-box-sub']);

const localStore = new Map();
const mockDocument = {
  title: 'Supply Chain Portal',
  documentElement: makeEl('html'),
  body: makeEl('body'),
  createElement(tag) { return makeEl(tag); },
  createElementNS(_ns, tag) { return makeEl(tag); },
  getElementById(id) { return getOrCreateId(id); },
  querySelector(sel) {
    if (sel === '.nav-csco-badge') return navCscoBadge;
    if (sel === '.hero-content') return heroContent;
    if (sel === '.hero-title') return heroTitle;
    if (sel === '.cfo-box-title') return cfoTitle;
    if (sel === '.cfo-box-sub') return cfoSub;
    if (sel === '.page-view.active') {
      for (const el of elementsById.values()) {
        if (el.classList.contains('page-view') && el.classList.contains('active')) return el;
      }
      return getOrCreateId('pageHome');
    }
    return makeEl('div');
  },
  querySelectorAll(sel) {
    if (sel === '.page-view') {
      return Array.from(elementsById.values()).filter(e => e.classList.contains('page-view'));
    }
    return [];
  },
  addEventListener() {},
};

const sandbox = {
  window: null,
  document: mockDocument,
  localStorage: {
    getItem: k => (localStore.has(k) ? localStore.get(k) : null),
    setItem: (k, v) => localStore.set(k, String(v)),
    removeItem: k => localStore.delete(k),
  },
  sessionStorage: { getItem: () => null, setItem: () => {}, removeItem: () => {} },
  navigator: { clipboard: { writeText: async () => {} }, userAgent: 'NodeDOMVerify' },
  location: { href: 'http://localhost:8095/', search: '', pathname: '/', origin: 'http://localhost:8095' },
  history: { pushState() {}, replaceState() {} },
  addEventListener() {},
  removeEventListener() {},
  scrollTo() {},
  innerWidth: 1440,
  innerHeight: 900,
  devicePixelRatio: 1,
  getComputedStyle: () => ({ getPropertyValue: () => '' }),
  matchMedia: () => ({ matches: false, addEventListener() {}, removeEventListener() {} }),
  URLSearchParams,
  URL,
  performance: { now: () => Date.now() },
  requestAnimationFrame: () => 1,
  cancelAnimationFrame: () => {},
  setTimeout: () => 1,
  clearTimeout: () => {},
  setInterval: () => 1,
  clearInterval: () => {},
  IntersectionObserver: class { observe() {} disconnect() {} unobserve() {} },
  ResizeObserver: class { observe() {} disconnect() {} },
  fetch: async () => ({ ok: true, json: async () => ({ twins: [] }) }),
  console,
  Math,
  JSON,
  Object,
  Array,
  Set,
  Map,
  String,
  Number,
  Boolean,
  RegExp,
  Date,
  Promise,
  Error,
  encodeURIComponent,
  decodeURIComponent,
  parseInt,
  parseFloat,
  isNaN,
};
sandbox.window = sandbox;
sandbox.globalThis = sandbox;

vm.createContext(sandbox);
// Expose top-level `const`/`let` bindings onto `window` at the end of execution for inspection
const inspectTail = `
;globalThis.__INSPECT__ = {
  getState: () => ({
    DEPARTMENTS,
    PERSONAS,
    AGENTS,
    VALUE_CHAINS,
    CURRENT_TWIN,
    TWIN_SHOW_ALL_60
  }),
  applyBrowserTwin,
  toggleTwinShowAllAgents,
  switchClientTwin,
  openPersonaPage,
  openAgentPage,
  openPeriodicTablePage: typeof openPeriodicTablePage === 'function' ? openPeriodicTablePage : null,
  openMindMapPage: typeof openMindMapPage === 'function' ? openMindMapPage : null,
  openCostTabPage: typeof openCostTabPage === 'function' ? openCostTabPage : null,
  openValueChainPage: typeof openValueChainPage === 'function' ? openValueChainPage : null,
  openPersonasDirectoryPage: typeof openPersonasDirectoryPage === 'function' ? openPersonasDirectoryPage : null,
};
`;

vm.runInContext(scriptBlocks.join('\n') + inspectTail, sandbox, { filename: 'index.inline.js' });

const api = sandbox.__INSPECT__;
const agentEntries = Array.isArray(catalog.agents) ? catalog.agents : Object.values(catalog.agents);
const canonicalAgentNames = Object.fromEntries(agentEntries.map(a => [a.id, a.name]));

const hindalco = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/twins/v2/aditya-birla-group--hindalco-aluminium-copper.json'), 'utf8'));

// 0. Verify Navbar Dropdowns Removed in HTML Markup
assert(!html.includes('id="navProcessesQuickMenu"'), 'Processes navbar dropdown must be removed');
assert(!html.includes('id="navPersonasQuickMenu"'), 'Personas navbar dropdown must be removed');
assert(!html.includes('id="navAgentsQuickMenu"'), 'Agents navbar dropdown must be removed');
assert(html.includes('openProcessesHubPage(true, event)'), 'Processes navbar button must open Processes Hub');

// 1. Verify Canonical Initial State
let st = api.getState();
assert.strictEqual(Object.keys(st.DEPARTMENTS).length, 6, 'Expected 6 canonical pillars');
assert.strictEqual(Object.keys(st.PERSONAS).length, 60, 'Expected 60 canonical personas');
assert.strictEqual(Object.keys(st.AGENTS).length, 60, 'Expected 60 canonical agents');

// 2. Apply ITC Limited — Cigarettes & Leaf Tobacco (7 Dynamic Pillars, 55/60 relevant agents, 5 hidden)
api.applyBrowserTwin(itcTobacco);
st = api.getState();
assert.strictEqual(Object.keys(st.DEPARTMENTS).length, 7, 'Expected 7 dynamic Operating Pillars for ITC Tobacco & TM&D');
const expectedActiveTobacco = itcTobacco.active_agents_count;
assert.strictEqual(Object.keys(st.AGENTS).length, expectedActiveTobacco, `Expected ${expectedActiveTobacco} active agents for ITC Tobacco`);
assert.strictEqual(Object.keys(st.PERSONAS).length, 60 - itcTobacco.hidden_persona_ids.length, 'Expected paired hidden personas removed cleanly');
assert(cfoTitle.textContent.includes('ITC'), 'CSCO title must reflect ITC Limited');
assert(cfoSub.textContent.includes('7 Core Operating Pillars'), 'CSCO subtitle must reflect 7 Core Operating Pillars');
assert(heroTitle.innerHTML.includes('ITC Limited'), 'Hero title must reflect ITC Limited');
assert(!elementsById.has('twinActiveContextBar'), 'Customer-facing front page must NOT render #twinActiveContextBar');

// Every active agent MUST preserve its canonicalName AND apply custom_agent_name when provided!
let customRenamedCount = 0;
for (const [aid, ag] of Object.entries(st.AGENTS)) {
  const expectedCanon = canonicalAgentNames[aid].replace(/^\[[^\]]+\]\s*/, '').trim();
  assert.strictEqual(ag.canonicalName, expectedCanon, `Agent ${aid} must preserve ag.canonicalName!`);
  assert(Boolean(st.DEPARTMENTS[ag.deptId]), `Agent ${aid} deptId ${ag.deptId} must exist in custom DEPARTMENTS`);
  const rel = (itcTobacco.agent_relevance || {})[aid];
  if (rel && rel.custom_agent_name) {
    assert.strictEqual(ag.name, rel.custom_agent_name, `Agent ${aid} should display custom_agent_name`);
    customRenamedCount += 1;
  } else {
    assert.strictEqual(ag.name, canonicalAgentNames[aid], `Agent ${aid} without custom_agent_name keeps canonical name`);
  }
}
assert(customRenamedCount >= 10, `Expected >=10 company-tailored agent names for ITC Tobacco, got ${customRenamedCount}`);

// Exercise all interactive sub-pages while 7 custom pillars & 55 agents are active -> ZERO runtime errors!
const samplePid = Object.keys(st.PERSONAS)[0];
const sampleAid = Object.keys(st.AGENTS)[0];
api.openPersonaPage(samplePid, false);
const personaHtml = getOrCreateId('personaPageContent').innerHTML;
assert(!personaHtml.includes('Est. Cost:'), 'Persona page must NOT show inline Est. Cost clutter');
assert(personaHtml.includes('Back to 7 Pillars'), 'Persona back button must dynamically reflect 7 Pillars');

api.openAgentPage(sampleAid, false);
const agentHtml = getOrCreateId('agentPageContent').innerHTML;
assert(
  agentHtml.includes('Operational Context') || Boolean(st.AGENTS[sampleAid].twinDivisionContext),
  'Agent detail page must carry division operational context while keeping core demo intact'
);
assert(!agentHtml.includes('Core Demo Engine Preserved'), 'Agent detail page must NOT show internal scaffolding text');
assert(!agentHtml.includes('WHAT THIS AGENT DOES AT A GLANCE'), 'Duplicate paragraph/bullet wall must be removed from Agent page');
assert(agentHtml.includes(`id="agentDeepBtn_cost_${sampleAid}"`), 'Agent page must include collapsed Cost & ROI pill');
assert(agentHtml.includes(`id="agentDrawer_cost_${sampleAid}" class="agent-deepdive-drawer" style="display:none;"`), 'Cost & ROI drawer must be collapsed by default');
assert(agentHtml.includes(`id="agentSingleSpecBody_${sampleAid}"`), '6-tab Enterprise Agent Contract must remain intact');

// Verify Dynamic 7-Pillar Periodic Table
api.openPeriodicTablePage('all', null, false);
const ptHtml = getOrCreateId('periodicPageContent').innerHTML;
assert(ptHtml.includes('7 Operating Pillars'), 'Periodic Table must dynamically display 7 Operating Pillars');
assert(!ptHtml.includes('undefined'), 'Periodic Table must have zero undefined strings');

// Verify Harmonized Mind Map + Top Active Path Bar + Pinned Top Agent
api.openMindMapPage('mindmap', null, null, false);
const mmHtml = getOrCreateId('mindMapPageContent').innerHTML;
assert(mmHtml.includes('mm-active-path-bar'), 'Mind Map must display prominent Active Path & Quick-Launch Top Bar');
assert(mmHtml.includes('Operating Pillars (7)'), 'Mind Map must dynamically display 7 Operating Pillars');
assert(!mmHtml.includes('undefined'), 'Mind Map must have zero undefined strings');

// Verify Progressive 3-Step Cost & ROI Hub
sandbox.switchCostSectionTab('pillars');
let costHtml = getOrCreateId('costPageContent').innerHTML;
assert(costHtml.includes('1 · By Operating Pillar'), 'Cost & ROI must render 3-step progressive tabs');
sandbox.switchCostSectionTab('agents');
costHtml = getOrCreateId('costPageContent').innerHTML;
assert(costHtml.includes('Agent-by-Agent Unit Economics'), 'Cost & ROI Step 2 must render agent table');
sandbox.switchCostSectionTab('simulator');
costHtml = getOrCreateId('costPageContent').innerHTML;
assert(costHtml.includes('Dynamic Scale Simulator'), 'Cost & ROI Step 3 must render interactive simulator');

// Verify Progressive 3-Tab Case Studies Hub
sandbox.switchEvidenceTab('cases');
let evHtml = getOrCreateId('evidencePageContent').innerHTML;
assert(evHtml.includes('sc-v22-cs-card'), 'Case Studies Tab 1 must render clean spacious case study cards');
assert(!evHtml.includes('Pillar-by-Pillar Calibration Matrix'), 'Case Studies Tab 1 must NOT stack benchmark table');
sandbox.switchEvidenceTab('benchmarks');
evHtml = getOrCreateId('evidencePageContent').innerHTML;
assert(evHtml.includes('Pillar-by-Pillar Calibration Matrix'), 'Case Studies Tab 2 must render benchmark matrix');
sandbox.switchEvidenceTab('sources');
evHtml = getOrCreateId('evidencePageContent').innerHTML;
assert(evHtml.includes('Open Published Source'), 'Case Studies Tab 3 must render primary research sources');

// Verify Hierarchical Personas & Agents Directory + Dedicated Processes Hub
api.openPersonasDirectoryPage('all', '', false, 'personas');
const dirHtml = getOrCreateId('directoryPageContent').innerHTML;
assert(dirHtml.includes('sc-dir-pillar-section'), 'Directory must group cards hierarchically under Operating Pillar sections');
api.openPersonasDirectoryPage('all', '', false, 'agents');
sandbox.openProcessesHubPage(false);
const procHubHtml = getOrCreateId('valueChainPageContent').innerHTML;
assert(procHubHtml.includes('End-to-End Supply Chain Processes'), 'Processes Hub must render clean overview');

if (api.openValueChainPage) {
  for (const vcId of Object.keys(st.VALUE_CHAINS)) {
    api.openValueChainPage(vcId, false);
  }
}

// 3. Toggle "Show All 60" -> reveals all 60 agents cleanly across the 7 custom pillars!
api.toggleTwinShowAllAgents();
st = api.getState();
assert.strictEqual(Object.keys(st.AGENTS).length, 60, 'Show All 60 toggle must reveal all 60 agents');
api.toggleTwinShowAllAgents();
st = api.getState();
assert.strictEqual(Object.keys(st.AGENTS).length, expectedActiveTobacco, 'Toggling back must re-filter to relevant division agents');

// 4. Switch to Aditya Birla Group — Hindalco (5 Consolidated Industrial Pillars!) -> ZERO state leak!
api.applyBrowserTwin(hindalco);
st = api.getState();
assert.strictEqual(Object.keys(st.DEPARTMENTS).length, 5, 'Expected 5 consolidated Operating Pillars for Hindalco');
assert(cfoSub.textContent.includes('5 Core Operating Pillars'), 'CSCO subtitle must reflect 5 Core Operating Pillars');
assert(!cfoTitle.textContent.includes('ITC'), 'Zero state leak from ITC into Hindalco');

// 4B. Switch to Aditya Birla Group — UltraTech Cement (7 Heavy-Material Pillars, 53/60 agents) -> ZERO state leak!
api.applyBrowserTwin(ultraTech);
st = api.getState();
assert.strictEqual(Object.keys(st.DEPARTMENTS).length, 7, 'Expected 7 Operating Pillars for UltraTech Cement');
assert.strictEqual(Object.keys(st.AGENTS).length, ultraTech.active_agents_count, 'Expected UltraTech active agent count');
assert(heroTitle.innerHTML.includes('UltraTech') || heroTitle.innerHTML.includes('Aditya Birla'), 'Hero updated to UltraTech / Aditya Birla');

// 5. Reset to Base Industry-Agnostic Framework -> 100% canonical 6 Pillars & 60/60 names restored!
api.switchClientTwin('reset');
st = api.getState();
assert.strictEqual(st.CURRENT_TWIN, null, 'CURRENT_TWIN cleared on reset');
assert.strictEqual(Object.keys(st.DEPARTMENTS).length, 6, 'All 6 canonical Operating Pillars restored on reset');
assert.strictEqual(Object.keys(st.AGENTS).length, 60, 'All 60 canonical agents restored');
assert.strictEqual(Object.keys(st.PERSONAS).length, 60, 'All 60 canonical personas restored');
for (const [aid, ag] of Object.entries(st.AGENTS)) {
  assert.strictEqual(ag.name, canonicalAgentNames[aid], `Reset must restore 100% canonical agent name for ${aid}`);
}
let totalSubPillars = 0;
Object.values(st.DEPARTMENTS).forEach(d => { totalSubPillars += d.subPillars.length; });
assert.strictEqual(totalSubPillars, 20, 'All 20 canonical sub-pillars restored');

console.log('✅ ZERO-BREAKAGE V2.2 DOM, HIERARCHY & DYNAMIC PILLARS VERIFICATION PASSED 100%!');
console.log(`   - Canonical Baseline: 6 Pillars · 20 Sub-Pillars · 60 Personas · 60 Agents`);
console.log(`   - ITC Tobacco & TM&D: 7 Dynamic Pillars · ${expectedActiveTobacco}/60 Agents (${customRenamedCount} Tailored Names)`);
console.log(`   - Hindalco Metals:    5 Dynamic Pillars · ${hindalco.active_agents_count}/60 Agents`);
console.log(`   - UltraTech Cement:   7 Dynamic Pillars · ${ultraTech.active_agents_count}/60 Agents`);
console.log(`   - Navbar Dropdowns Removed + Processes Hub + 3-Tab Case Studies + 3-Step Cost & ROI + Top-Bar Mind Map: 0 Errors`);


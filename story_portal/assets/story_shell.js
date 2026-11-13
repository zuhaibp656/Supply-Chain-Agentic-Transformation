(function () {
  const THEME_KEY = 'sc_aurora_theme';

  function applyTheme(mode) {
    const isDark = mode === 'dark';
    document.documentElement.classList.toggle('theme-light', !isDark);
    document.documentElement.classList.toggle('theme-dark', isDark);
    document.body && document.body.classList.toggle('theme-light', !isDark);
    document.body && document.body.classList.toggle('theme-dark', isDark);
    const btn = document.getElementById('scThemeToggle');
    if (btn) {
      btn.innerHTML = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';
    }
  }

  function initTheme() {
    const saved = localStorage.getItem(THEME_KEY) || 'light';
    applyTheme(saved);
  }

  window.toggleScTheme = function () {
    const current = localStorage.getItem(THEME_KEY) || 'light';
    const next = current === 'light' ? 'dark' : 'light';
    localStorage.setItem(THEME_KEY, next);
    applyTheme(next);
  };

  window.renderScNav = function (activeKey, depthPrefix) {
    const prefix = depthPrefix || '';
    const links = [
      { key: 'map', label: 'Briefing Map', href: prefix + 'index.html' },
      { key: 'story', label: '00 · Executive Story', href: prefix + 'pages/00_executive_story.html' },
      { key: 'personas', label: '08 · Persona Map (60)', href: prefix + 'personas/index.html' },
      { key: 'arch', label: '09 · Google Cloud Architecture', href: prefix + 'pages/09_agent_architecture.html' },
      { key: 'surfaces', label: '10 · 4 Agent Surfaces', href: prefix + 'pages/10_surfaces.html' },
      { key: 'proof', label: '13 · Proof & Cases', href: prefix + 'pages/13_proof_and_cases.html' },
    ];
    const html = `
      <nav class="sc-nav" aria-label="Story Portal Navigation">
        <a class="sc-nav-brand" href="${prefix}index.html">
          <span class="sc-nav-dot"></span>
          <span>Supply Chain Agentic Transformation</span>
        </a>
        <div class="sc-nav-links">
          ${links.map(l => `<a href="${l.href}" class="${l.key === activeKey ? 'active' : ''}">${l.label}</a>`).join('')}
        </div>
        <div class="sc-nav-actions">
          <span class="sc-badge-live">37 Live in Gemini Enterprise</span>
          <button id="scThemeToggle" class="sc-theme-btn" type="button" onclick="toggleScTheme()">🌙 Dark Mode</button>
        </div>
      </nav>`;
    const host = document.getElementById('scNavHost');
    if (host) host.innerHTML = html;
    initTheme();
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
  } else {
    initTheme();
  }
})();

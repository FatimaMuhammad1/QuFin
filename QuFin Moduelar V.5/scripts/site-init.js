const API_BASE = 'http://127.0.0.1:8000';
const WS_URL = (window.__ENV && window.__ENV.WS_URL) || (location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host + '/ws';


async function injectHeaderTheme() {
  try {
    if (document.querySelector('link[data-header-theme]')) return;
    const p = (location.pathname || '').toLowerCase();
    // do not inject on the main index page (root or index.html)
    if (p === '/' || p.endsWith('index.html')) return;

    const candidates = [];
    
    try {
      const parts = (location.pathname || '').split('/');
      // parts[1] should be the top-level folder (e.g. 'QuFin Moduelar V.5') when Live Server serves workspace root
      if (parts.length > 1 && parts[1]) {
        const projectRoot = `/${parts[1]}`;
        const originProj = `${location.origin}${projectRoot}/styles/header-theme.css`;
        candidates.push(originProj);
      }
    } catch (err) {
      // ignore
    }

    // relative fallbacks (previous heuristic)
    if (p.indexOf('/pages/') !== -1 || p.startsWith('/pages/')) {
      candidates.push('../styles/header-theme.css');
    }
    candidates.push('./styles/header-theme.css');

    let chosen = null;
    // Try fetching candidates to avoid 404 noise. Use HEAD where supported.
    for (const href of candidates) {
      try {
        const resp = await fetch(href, { method: 'HEAD' });
        if (resp && resp.ok) { chosen = href; break; }
      } catch (e) {
        // HEAD may be blocked by some servers; try a GET fallback quickly
        try {
          const r2 = await fetch(href, { method: 'GET' });
          if (r2 && r2.ok) { chosen = href; break; }
        } catch (e2) {
          // ignore and continue
        }
      }
    }

    // If none validated, fall back to last candidate to attempt loading anyway
    if (!chosen) chosen = candidates[candidates.length - 1];

    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = chosen;
    link.setAttribute('data-header-theme', '1');
    link.crossOrigin = 'anonymous';
    document.head.appendChild(link);
  } catch (e) {
    console.debug('injectHeaderTheme error', e);
  }
}

function initTheme() {
  try {
    const saved = localStorage.getItem('theme');
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const root = document.documentElement; // use <html> for Tailwind dark mode compatibility

    if (saved === 'dark' || (!saved && prefersDark)) {
      root.classList.add('dark');
    }

    // wire theme toggle buttons (both single icons and other variants)
    document.querySelectorAll('.theme-toggle, .theme-toggle-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        root.classList.toggle('dark');
        const isDark = root.classList.contains('dark');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');

        // update icons inside toggles for visual feedback
        btn.querySelectorAll('i').forEach(i => {
          if (isDark) {
            i.classList.remove('fa-moon');
            i.classList.add('fa-sun');
          } else {
            i.classList.remove('fa-sun');
            i.classList.add('fa-moon');
          }
        });
      });
    });
  } catch (e) {
    console.warn('Theme init failed', e);
  }
}

function initMobileMenu() {
  try {
    const mobileToggle = document.getElementById('mobileToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    if (!mobileToggle || !mobileMenu) return;

    mobileToggle.addEventListener('click', () => {
      mobileMenu.classList.toggle('open');
      const icon = mobileToggle.querySelector('i');
      if (!icon) return;
      if (mobileMenu.classList.contains('open')) {
        icon.classList.remove('fa-bars'); icon.classList.add('fa-times');
      } else {
        icon.classList.remove('fa-times'); icon.classList.add('fa-bars');
      }
    });
  } catch (e) { console.warn('Mobile menu init failed', e); }
}

function initAuthModal() {
  try {
    const authModal = document.getElementById('authModal');
    if (!authModal) return;

    const openers = document.querySelectorAll('.login-btn, #loginBtn, #mobileLoginBtn, #trialBtn');
    openers.forEach(btn => btn && btn.addEventListener('click', () => authModal.classList.add('open')));

    const closeBtn = document.getElementById('authClose');
    if (closeBtn) closeBtn.addEventListener('click', () => authModal.classList.remove('open'));

    // auth tabs
    document.querySelectorAll('.auth-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        const target = tab.getAttribute('data-tab');
        document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
        const form = document.getElementById(target + 'Form');
        if (form) form.classList.add('active');
      });
    });

    // wire form submissions safely: only intercept when a backend integration module is present
    document.querySelectorAll('form').forEach(form => {
      form.addEventListener('submit', async (e) => {
        try {
          // try importing backend-integration which should export login/signup functions
          const mod = await import('/QuFin Moduelar V.5/scripts/backend-integration.js').catch(() => null);

          // If the module isn't present, do not intercept the form submission here.
          // Many pages attach their own handlers (inline); interfering causes duplicate alerts.
          if (!mod) {
            console.debug('backend-integration module not found; skipping site-init form handler for', form.id || form);
            return;
          }

          // Only now prevent default and handle via the integration module
          e.preventDefault();
          if (typeof mod.login === 'function' && typeof mod.signup === 'function') {
            // determine which form
            if (form.id === 'loginForm' || form.classList.contains('js-login')) {
              const email = form.querySelector('input[type="email"]')?.value;
              const password = form.querySelector('input[type="password"]')?.value;
              const res = await mod.login(email, password);
              if (res && (res.access_token || res.token)) {
                const token = res.access_token || res.token;
                if (window.authHandler && typeof window.authHandler.setAuthToken === 'function') {
                  window.authHandler.setAuthToken(token);
                } else {
                  localStorage.setItem('qufin_token', token);
                  localStorage.setItem('token', token);
                  localStorage.setItem('isLoggedIn', 'true');
                }
                authModal.classList.remove('open');
                return;
              }
              alert(res?.detail || 'Login failed');
            } else if (form.id === 'signupForm' || form.classList.contains('js-signup')) {
              const email = form.querySelector('input[type="email"]')?.value;
              const password = form.querySelector('input[type="password"]')?.value;
              const res = await mod.signup(email, password);
              if (res && res.id) { alert('Signed up — please log in'); return; }
              alert(res?.detail || 'Signup failed');
            }
          }
        } catch (err) {
          console.error('Auth submit error', err);
          // Only show a generic auth error if the module was present (we intended to handle it)
          alert('Auth error');
        }
      });
    });
  } catch (e) { console.warn('Auth modal init failed', e); }
}

async function fetchCountryScoresAndTrigger() {
  const loadingOverlay = document.getElementById('loadingOverlay');
  const dataStatus = document.getElementById('dataStatus');
  
  try {
    // Show loading state
    if (loadingOverlay) {
      loadingOverlay.classList.add('active');
    }
    if (dataStatus) {
      dataStatus.textContent = 'Fetching World Bank Economic Data...';
      dataStatus.style.color = '#3498db';
    }
    
    console.log('Fetching live economic scores from World Bank data...');
    const backendUrl = `${API_BASE}/api/v1/country-scores/`;
    console.log('Connecting to backend at:', backendUrl);
    
    const resp = await fetch(backendUrl, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
      mode: 'cors'
    });
    
    if (!resp.ok) {
      throw new Error(`Failed to fetch World Bank data: ${resp.status}`);
    }
    
    const json = await resp.json();
    console.log('Received live economic scores:', json);
    
    if (json && typeof json === 'object') {
      window.countryScores = json;
      console.log('Updated map with live World Bank economic data');
      
      window.dispatchEvent(new Event('resize'));
      
      if (typeof updateMapColors === 'function') {
        updateMapColors();
      }
      
      if (dataStatus) {
        dataStatus.textContent = 'Live World Bank Data';
        dataStatus.style.color = '#4ade80';
      }
    }
  } catch (e) {
    console.error('Failed to fetch World Bank economic data:', e);
    
    if (dataStatus) {
      dataStatus.textContent = 'Error: Could not fetch World Bank data';
      dataStatus.style.color = '#ef4444';
    }
  } finally {
    if (loadingOverlay) {
      loadingOverlay.classList.remove('active');
    }
  }
}

// Initialize all site behaviors
function initSite() {
  // inject shared header/hero CSS first so styles apply immediately
  injectHeaderTheme();
  initTheme();
  initMobileMenu();
  initAuthModal();
  // try fetching country scores but don't block page load
  fetchCountryScoresAndTrigger();
}

// Run on DOM ready
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initSite);
else initSite();

// export for debugging if needed
window.__qufin = window.__qufin || {};
window.__qufin.API_BASE = API_BASE;
window.__qufin.WS_URL = WS_URL;

(function(){
    let authBtn = null;
    let authBtnText = null;

    function ensureAuthControlExists() {
        const pathname = (window.location.pathname || '/').replace(/\\/g, '/');
        const filename = pathname.split('/').filter(Boolean).pop() || '';
        const isIndex = (!filename || filename.toLowerCase() === 'index.html');
        if (!isIndex) {
            const existing = document.getElementById('authControl');
            if (existing) existing.remove();
            return;
        }
        const existingLogin = document.getElementById('loginBtn');
        const existingMobileLogin = document.getElementById('mobileLoginBtn');

        if (existingLogin) {
            authBtn = existingLogin;
            // Ensure we have a span we can update for the button text
            authBtnText = authBtn.querySelector('#authBtnText');
            if (!authBtnText) {
                // find any text node and wrap it, preserving icon if present
                const icon = authBtn.querySelector('i');
                const text = authBtn.textContent.trim();
                authBtn.innerHTML = '';
                if (icon) authBtn.appendChild(icon);
                const span = document.createElement('span');
                span.id = 'authBtnText';
                span.textContent = text || 'Login';
                authBtn.appendChild(span);
                authBtnText = span;
            }
        } else if (document.getElementById('authBtn')) {
            authBtn = document.getElementById('authBtn');
            authBtnText = document.getElementById('authBtnText');
        } else {
            // Prefer placing in the header-actions container so it matches site layout
            const headerActions = document.querySelector('.header-actions') || document.querySelector('.header-content') || document.body;
            const container = document.createElement('div');
            container.id = 'authControl';
            container.style.marginLeft = '12px';
            // Use the same class used across the site for the login button so the styling matches exactly
            container.innerHTML = `<button id="authBtn" class="btn-primary"><i class="fas fa-user" style="margin-right:8px"></i><span id="authBtnText">Login</span></button>`;
            headerActions.appendChild(container);
            authBtn = document.getElementById('authBtn');
            authBtnText = document.getElementById('authBtnText');
        }

        // existingMobileLogin is intentionally detected above; we don't modify its id so other scripts keep working
    }

    function hasToken() {
        return !!(localStorage.getItem('token') || localStorage.getItem('qufin_token') || localStorage.getItem('authToken'));
    }

    function effectiveLoggedInFlag() {
        // consider logged in only if flag is explicitly true AND a token exists
        // require session confirmation so stale tokens don't auto-show 'My profile'
        return localStorage.getItem('isLoggedIn') === 'true' && hasToken() && localStorage.getItem('qufin_session') === '1';
    }

    function updateAuthButtonText(isLoggedIn) {
        // prefer computed effective flag when caller passes undefined
        if (typeof isLoggedIn === 'undefined' || isLoggedIn === null) {
            isLoggedIn = effectiveLoggedInFlag();
        }
        ensureAuthControlExists();

        if (authBtnText) {
            // Show 'My profile' when logged in, 'Login' otherwise
            authBtnText.textContent = isLoggedIn ? 'My profile' : 'Login';

            if (authBtn) {
                if (isLoggedIn) {
                    authBtn.onclick = function() {
                        // Primary strategy: resolve relative to current document so base path like
                        // /QuFin%20Moduelar%20V.5/ is preserved. This should produce URLs like
                        // http://127.0.0.1:5500/QuFin%20Moduelar%20V.5/pages/profile.html
                        try {
                            const relTarget = new URL('pages/profile.html', window.location.href).toString();
                            window.location.href = relTarget;
                            return;
                        } catch (e) { /* fall through to other strategies */ }

                        // Fallback: derive from the script src that loaded this file
                        try {
                            const scriptEl = Array.from(document.getElementsByTagName('script')).reverse().find(s => s.src && s.src.indexOf('auth-handler.js') !== -1);
                            if (scriptEl) {
                                const src = scriptEl.getAttribute('src');
                                const base = src.replace(/scripts\/auth-handler\.js$/, '');
                                try {
                                    const target = new URL(base + 'pages/profile.html', window.location.href).toString();
                                    window.location.href = target;
                                    return;
                                } catch (e) { /* fall through */ }
                            }
                        } catch (e) { /* ignore and fallback */ }

                        // Last resort: try root-relative or plain relative
                        try { window.location.href = new URL('/pages/profile.html', window.location.href).toString(); return; } catch(e){}
                        try { window.location.href = new URL('../pages/profile.html', window.location.href).toString(); return; } catch(e){}
                        window.location.href = 'pages/profile.html';
                    };
                } else {
                    authBtn.onclick = function() {
                        // Open auth modal if present, otherwise redirect to login page
                        const authModal = document.getElementById('authModal');
                        if (authModal) {
                            authModal.classList.add('open');
                        } else {
                            // redirect to login page (relative)
                            window.location.href = new URL('pages/login.html', window.location.href).toString();
                        }
                    };
                }
            }
        }

        // Also hide or show any existing login buttons that are part of the page
        try {
            const loginBtnEl = document.getElementById('loginBtn');
            const mobileLoginBtnEl = document.getElementById('mobileLoginBtn');
            // If our auth control is reusing the page's #loginBtn, don't hide it.
            if (isLoggedIn) {
                if (loginBtnEl && authBtn !== loginBtnEl) loginBtnEl.style.display = 'none';
                if (mobileLoginBtnEl && authBtn !== mobileLoginBtnEl) mobileLoginBtnEl.style.display = 'none';
            } else {
                if (loginBtnEl) loginBtnEl.style.removeProperty('display');
                if (mobileLoginBtnEl) mobileLoginBtnEl.style.removeProperty('display');
            }
        } catch (err) { /* noop */ }
    }

    // Expose public API
    window.authHandler = {
        updateAuthButtonText: updateAuthButtonText
    };

    // helper to set token + flag in a single place so all pages behave consistently
    function setAuthToken(token) {
        try {
            if (!token) return;
            localStorage.setItem('qufin_token', token);
            localStorage.setItem('token', token);
            localStorage.setItem('authToken', token);
            localStorage.setItem('isLoggedIn', 'true');
            // mark this session as an explicit login so UI shows My profile in this session
            localStorage.setItem('qufin_session', '1');
            updateAuthButtonText(true);
        } catch (err) { console.error('setAuthToken error', err); }
    }

    function clearAuth() {
        try {
            localStorage.removeItem('qufin_token');
            localStorage.removeItem('token');
            localStorage.removeItem('authToken');
            localStorage.removeItem('isLoggedIn');
            localStorage.removeItem('qufin_session');
            updateAuthButtonText(false);
        } catch (err) { console.error('clearAuth error', err); }
    }

    // attach helpers
    window.authHandler.setAuthToken = setAuthToken;
    window.authHandler.clearAuth = clearAuth;

    // Initialize on load
    document.addEventListener('DOMContentLoaded', () => {
        // If the flag says logged in but there is no token, clear the stale flag
        try {
            const flag = localStorage.getItem('isLoggedIn');
            if (flag === 'true' && !hasToken()) {
                localStorage.removeItem('isLoggedIn');
            }
        } catch (err) { /* noop */ }

        // Check initial auth state
        const isLoggedIn = effectiveLoggedInFlag();

        // Startup polling to catch auth values set shortly after load by other scripts.
        // This addresses race conditions where login/signup handlers run after auth-handler.
        (function startupPoll(){
            let checks = 0;
            let lastFlag = effectiveLoggedInFlag();
            const iv = setInterval(() => {
                checks += 1;
                const curFlag = effectiveLoggedInFlag();
                if (curFlag !== lastFlag) {
                    try { updateAuthButtonText(); } catch (e) { /* noop */ }
                    lastFlag = curFlag;
                }
                if (checks > 15) { // ~3 seconds at 200ms per check
                    clearInterval(iv);
                }
            }, 200);
        })();

        // If we have a token, verify it with the backend profile endpoint to avoid stale tokens
        // and ensure the UI only shows "My profile" when the session marker is present.
        (async function verifyTokenIfPresent(){
            try {
                const token = localStorage.getItem('token') || localStorage.getItem('qufin_token') || localStorage.getItem('authToken');
                if (!token) {
                    updateAuthButtonText(isLoggedIn);
                    return;
                }
                const resp = await fetch('http://127.0.0.1:8000/auth/profile', {
                    method: 'GET',
                    headers: { 'Authorization': `Bearer ${token}` },
                });
                if (resp.ok) {
                    // Parse profile to ensure token is truly valid, then mark session and update UI
                    try {
                        const profile = await resp.json();
                        if (profile && profile.email) {
                            // Ensure session marker and flags are set so UI updates consistently
                            try { setAuthToken(token); } catch (e) { /* noop */ }
                            updateAuthButtonText(true);
                        } else {
                            // fallback: clear if profile payload unexpected
                            clearAuth();
                        }
                    } catch (e) {
                        // couldn't parse profile; be conservative and clear
                        clearAuth();
                    }
                } else {
                    // token invalid or expired - clear local auth state
                    clearAuth();
                }
            } catch (err) {
                // backend not reachable or other error - fallback to computed flag
                updateAuthButtonText(isLoggedIn);
            }
        })();
    });
})();

// Handle email verification
async function sendVerificationEmail(email) {
    try {
        const response = await fetch("http://127.0.0.1:8000/auth/send-verification", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email }),
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || "Failed to send verification email.");
        }

        alert("Verification email sent. Please check your inbox.");
    } catch (error) {
        alert(`Error: ${error.message}`);
        console.error(error);
    }
}

// Handle verification code input
async function verifyCode(email, code) {
    try {
        const response = await fetch("http://127.0.0.1:8000/auth/verify-code", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, code }),
        });

        const data = await response.json();
        if (response.ok) {
            alert("Email verified successfully! You can now log in.");
            window.location.href = "../pages/login.html"; // Redirect to login page
        } else {
            alert(`Error: ${data.detail}`);
        }
    } catch (error) {
        alert("An error occurred during verification.");
        console.error(error);
    }
}

// Modify signup button click handler (guarded) — use data-attribute to avoid double-binding
const _signupBtn = document.getElementById("signup-button");
if (_signupBtn && !_signupBtn.dataset.authHandlerBound) {
    _signupBtn.dataset.authHandlerBound = '1';
    _signupBtn.addEventListener("click", async () => {
        const fullName = document.getElementById("full-name")?.value || '';
        const email = document.getElementById("email")?.value || '';
        const password = document.getElementById("password")?.value || '';

        try {
            console.log('Sending signup request', { email, username: fullName });
            const response = await fetch("http://127.0.0.1:8000/auth/signup", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password, username: fullName }),
            });

            // Try to parse JSON safely
            let data = null;
            const ct = response.headers.get('content-type') || '';
            if (ct.includes('application/json')) data = await response.json();
            else {
                const text = await response.text();
                try { data = JSON.parse(text); } catch (e) { data = { message: text }; }
            }

            console.log("Signup Response Status:", response.status);
            console.log("Signup Response Data:", data);

            if (response.ok) {
                // Save the email so OTP verification can send it back to server
                localStorage.setItem('authEmail', email);
                alert("OTP sent to your email. Please verify.");
                const otpModal = document.getElementById("otp-modal");
                if (otpModal) otpModal.style.display = 'block';
            } else {
                alert(`Signup failed: ${data.detail || data.message || "Unknown error occurred."}`);
            }
        } catch (error) {
            alert("An error occurred during signup. Please try again later.");
            console.error("Signup Error:", error);
        }
    });
}

// Add OTP input field and verification logic (guarded) — avoid redeclaring global otpForm
const _otpFormEl = document.getElementById('otp-form');
if (_otpFormEl && !_otpFormEl.dataset.authHandlerBound) {
    _otpFormEl.dataset.authHandlerBound = '1';
    _otpFormEl.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = document.getElementById('email')?.value || localStorage.getItem('authEmail') || '';
        const otp = document.getElementById('otp')?.value || '';

        try {
            const response = await fetch("http://127.0.0.1:8000/auth/verify-otp", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, otp }),
            });

            let data = null;
            const ct = response.headers.get('content-type') || '';
            if (ct.includes('application/json')) data = await response.json();
            else {
                const txt = await response.text();
                try { data = JSON.parse(txt); } catch (e) { data = { message: txt }; }
            }

            console.log("OTP Verification Response:", data);

            if (response.ok) {
                // If backend returned a token, use the central setter when available
                if (data && (data.token || data.access_token)) {
                    const token = data.token || data.access_token;
                    try {
                        if (window && window.authHandler && typeof window.authHandler.setAuthToken === 'function') {
                            window.authHandler.setAuthToken(token);
                        } else {
                            // fallback for older pages
                            localStorage.setItem('qufin_token', token);
                            localStorage.setItem('token', token);
                            localStorage.setItem('authToken', token);
                            localStorage.setItem('isLoggedIn', 'true');
                            localStorage.setItem('qufin_session', '1');
                            try { if (window && window.authHandler && typeof window.authHandler.updateAuthButtonText === 'function') window.authHandler.updateAuthButtonText(true); } catch (e) { /* noop */ }
                        }
                    } catch (err) {
                        console.error('Error applying token after OTP:', err);
                    }
                }

                // Stay on the current page; update UI to reflect logged-in state and hide OTP modal
                const otpModalEl = document.getElementById('otp-modal');
                if (otpModalEl) otpModalEl.style.display = 'none';
                alert("Signup complete! You are now logged in.");
            } else {
                alert(`OTP verification failed: ${data?.detail || data?.message || "Invalid OTP."}`);
            }
        } catch (error) {
            alert("An error occurred during OTP verification.");
            console.error("OTP Verification Error:", error);
        }
    });
}

// Listen for storage changes (other tabs) so the auth button updates when login state changes
window.addEventListener('storage', (e) => {
    if (e.key === 'isLoggedIn' || e.key === 'token' || e.key === 'qufin_token' || e.key === 'qufin_session') {
        try { window.authHandler.updateAuthButtonText(); } catch (err) { /* noop */ }
    }
});

// Ensure UI reflects current auth state immediately (in case script loaded after DOMContentLoaded)
try {
    if (window && window.authHandler && typeof window.authHandler.updateAuthButtonText === 'function') {
        // immediate sync: compute effective flag inside the helper
        window.authHandler.updateAuthButtonText();
    }
} catch (err) { /* noop */ }
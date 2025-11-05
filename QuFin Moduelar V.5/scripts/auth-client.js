// Simple frontend auth client that talks to FastAPI auth endpoints
(function(){
    const API_BASE = 'http://127.0.0.1:8000';

    function saveToken(token){
        if (window.authHandler && typeof window.authHandler.setAuthToken === 'function') {
            window.authHandler.setAuthToken(token);
            return;
        }
        localStorage.setItem('qufin_token', token);
        localStorage.setItem('token', token);
        localStorage.setItem('authToken', token);
        localStorage.setItem('isLoggedIn', 'true');
        localStorage.setItem('qufin_session', '1');
        if (window.authHandler) window.authHandler.updateAuthButtonText(true);
    }

    function clearToken(){
        if (window.authHandler && typeof window.authHandler.clearAuth === 'function') {
            window.authHandler.clearAuth();
            return;
        }
        localStorage.removeItem('qufin_token');
        localStorage.removeItem('token');
        localStorage.removeItem('authToken');
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('qufin_session');
        if (window.authHandler) window.authHandler.updateAuthButtonText(false);
    }

    async function signup(email, password, full_name){
        const res = await fetch(API_BASE + '/auth/signup', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({email, password, full_name})
        });
        if (!res.ok) throw new Error(await res.text());
        const data = await res.json();
        // backend may return `token` or `access_token`
        saveToken(data.token || data.access_token);
        return data;
    }

    async function login(email, password){
        const res = await fetch(API_BASE + '/auth/login', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({email, password})
        });
        if (!res.ok) throw new Error(await res.text());
        const data = await res.json();
        saveToken(data.token || data.access_token);
        return data;
    }

    async function me(){
        const token = localStorage.getItem('qufin_token') || localStorage.getItem('token');
        if (!token) return null;
        try {
            const res = await fetch(API_BASE + '/auth/profile', {
                headers: { 'Authorization': 'Bearer ' + token }
            });
            if (!res.ok) return null;
            const data = await res.json();
            // Basic sanity: must include email
            if (!data || !data.email) return null;
            return data;
        } catch (err) {
            console.error('auth-client.me error', err);
            return null;
        }
    }

    window.qufinAuth = { signup, login, me, clearToken };

    // Ensure we don't clobber an existing authHandler created elsewhere
    if (!window.authHandler) {
        window.authHandler = {
            updateAuthButtonText: function(isLoggedIn){
                const btn = document.querySelector('.auth-button');
                if (!btn) return;
                btn.textContent = isLoggedIn ? 'Profile' : 'Login';
            }
        };
    }

    document.addEventListener('DOMContentLoaded', async ()=>{
        const loggedIn = localStorage.getItem('isLoggedIn') === 'true';
        if (window.authHandler) window.authHandler.updateAuthButtonText(loggedIn);
    });

})();

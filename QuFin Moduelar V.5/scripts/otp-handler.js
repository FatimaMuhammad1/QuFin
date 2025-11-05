// Add detailed logging for debugging OTP verification
const otpForm = document.getElementById('otp-form');

otpForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const otp = document.getElementById('otp').value;
    const token = localStorage.getItem('authToken') || localStorage.getItem('qufin_token');
    const email = localStorage.getItem('authEmail');

    if (!email && !token) {
        document.getElementById('error-message').textContent = 'Authentication token or email is missing. Please sign up again.';
        return;
    }

    try {
        console.log('Sending OTP verification request:', { otp, token, email }); // Log request details

        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const body = { otp };
        if (email) body.email = email;

        const response = await fetch('http://127.0.0.1:8000/auth/verify-otp', {
            method: 'POST',
            headers,
            body: JSON.stringify(body),
        });

        const data = await response.json();
        console.log('OTP Verification Response:', response.status, data); // Log response details

        if (response.ok) {
            if (data.token) {
                if (window.authHandler && typeof window.authHandler.setAuthToken === 'function') {
                    window.authHandler.setAuthToken(data.token);
                } else {
                    localStorage.setItem('qufin_token', data.token);
                    localStorage.setItem('token', data.token);
                    localStorage.setItem('isLoggedIn', 'true');
                }
            }
            // Instead of redirecting, update the UI and keep the user on the page
            alert('OTP verified successfully! You are now logged in.');

            // Prefer a dashboard path constructed from the current page's directory.
            // Example: current pathname = '/QuFin%20Moduelar%20V.5/index.html'
            // baseDir -> '/QuFin%20Moduelar%20V.5/' -> try '/QuFin%20Moduelar%20V.5/pages/dashboard.html'
            const pathname = window.location.pathname || '/';
            const origin = window.location.origin;
            // Try to detect a workspace folder in the served path (e.g. /QuFin%20Moduelar%20V.5/)
            const segments = pathname.split('/').filter(Boolean);
            let primaryCandidate = null;
            if (segments.length > 0) {
                // Use the first path segment as the workspace folder (common when Live Server serves a workspace folder in the URL)
                const workspaceSegment = segments[0];
                primaryCandidate = `${origin}/${workspaceSegment}/pages/dashboard.html`;
            }
            // As a fallback, build from the current page directory
            if (!primaryCandidate) {
                const baseDir = pathname.endsWith('/') ? pathname : pathname.replace(/\/[^\/]*$/, '/');
                primaryCandidate = origin + baseDir + 'pages/dashboard.html';
            }

            // Build other candidate paths by trying several parent-relative locations.
            const baseNames = ['pages/dashboard.html', 'dashboard.html', 'pages/dashboard/index.html'];
            const candidates = [primaryCandidate];
            // Try up to 4 levels up (./, ../, ../../, ...)
            for (let up = 0; up <= 4; up++) {
                const prefix = up === 0 ? '' : '../'.repeat(up);
                for (const name of baseNames) candidates.push(new URL(prefix + name, window.location.href).toString());
            }
            // Also try absolute variants
            candidates.push(origin + '/pages/dashboard.html', origin + '/dashboard.html');

            let redirected = false;
            for (const candidateUrl of candidates) {
                try {
                    // Probe the URL; if it returns OK, navigate there.
                    const probe = await fetch(candidateUrl, { method: 'GET', cache: 'no-store' });
                    console.debug('Probed', candidateUrl, 'status', probe.status);
                    if (probe && probe.ok) {
                        console.info('Redirecting to dashboard at', candidateUrl);
                        window.location.href = candidateUrl;
                        redirected = true;
                        break;
                    }
                } catch (err) {
                    // ignore probe errors and try next candidate
                    console.debug('Probe failed for', candidateUrl, err);
                }
            }

            // Fallback: show a helpful message and keep the user on the page so they can retry.
            if (!redirected) {
                console.warn('Could not locate dashboard path via probing. Tried:', candidates);
                // Optionally open a small instructions dialog instead of forcing a 404 redirect.
                const tryLink = document.createElement('a');
                tryLink.textContent = 'Open dashboard (click if it did not open automatically)';
                tryLink.href = new URL('pages/dashboard.html', window.location.href).toString();
                tryLink.style.display = 'block';
                tryLink.style.marginTop = '12px';
                document.body.appendChild(tryLink);
                // Also attempt the original relative redirect as a last resort (may produce 404)
                // window.location.href = new URL('pages/dashboard.html', window.location.href).toString();
            }
        } else {
            document.getElementById('error-message').textContent = data.detail || 'OTP verification failed.';
        }
    } catch (error) {
        console.error('Error verifying OTP:', error);
        document.getElementById('error-message').textContent = 'An error occurred. Please try again.';
    }
});
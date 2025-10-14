// Inactivity timer and handler
let inactivityTimeout;
const INACTIVITY_TIME = 30 * 1000; // 30 seconds (for testing)

function resetInactivityTimer() {
    clearTimeout(inactivityTimeout);
    inactivityTimeout = setTimeout(logoutDueToInactivity, INACTIVITY_TIME);
}

function logoutDueToInactivity() {
    // Clear token
    localStorage.removeItem('qufin_token');
    
    // Show logout message
    alert('You have been logged out due to inactivity.');
    
    // Hide logout button, show login button
    document.querySelectorAll('.logout-btn').forEach(btn => btn.style.display = 'none');
    document.querySelectorAll('.login-btn').forEach(btn => btn.style.display = 'inline-flex');
    
    // Optionally redirect to home page
    if (window.location.pathname !== '/index.html' && window.location.pathname !== '/') {
        window.location.href = '/index.html';
    }
}

// Reset timer on user activity
function setupInactivityDetection() {
    // Only setup if user is logged in
    if (!localStorage.getItem('qufin_token')) return;

    // List of events to track for activity
    const events = [
        'mousedown',
        'mousemove',
        'keypress',
        'scroll',
        'touchstart'
    ];

    // Add listeners for each event
    events.forEach(event => {
        document.addEventListener(event, resetInactivityTimer);
    });

    // Initial setup of timer
    resetInactivityTimer();
}

// Export for use in other files
export { setupInactivityDetection };
// Theme handling functionality
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
        document.documentElement.classList.add('dark');
    }
}

function toggleTheme() {
    const isDark = document.documentElement.classList.toggle('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
}

// Update icon(s) inside any theme-toggle button(s)
function syncToggleIcon() {
    const buttons = document.querySelectorAll('#theme-toggle');
    buttons.forEach((btn) => {
        const icon = btn.querySelector('i');
        if (!icon) return;
        if (document.documentElement.classList.contains('dark')) {
            icon.className = 'fa-solid fa-sun text-yellow-400';
        } else {
            icon.className = 'fa-solid fa-moon text-blue-400';
        }
    });
}

// Initialize theme on page load and sync icons
document.addEventListener('DOMContentLoaded', () => {
    initializeTheme();
    syncToggleIcon();
});

// Allow external code (e.g. React index.html) to initialize handlers that
// keep icons in sync when theme is toggled programmatically.
function initThemeHandlers() {
    // Listen for a custom event to resync icons
    window.addEventListener('qufin:theme-changed', () => {
        syncToggleIcon();
    });
}

// Auto-init
initThemeHandlers();

// Export for use in other files
export { initializeTheme, toggleTheme, syncToggleIcon, initThemeHandlers };
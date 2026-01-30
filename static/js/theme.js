/**
 * Theme Manager.
 */

export function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    applyTheme(savedTheme);

    const toggle = document.getElementById('themeToggle');
    if (toggle) {
        toggle.checked = savedTheme === 'dark';
        toggle.onchange = (e) => {
            const newTheme = e.target.checked ? 'dark' : 'light';
            applyTheme(newTheme);
        };
    }
}

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
}

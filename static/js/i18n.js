/**
 * Internationalization Frontend Logic.
 */

let currentLang = 'en';
let translations = {};

export async function initI18n() {
    // Check localStorage
    const saved = localStorage.getItem('app_lang');
    if (saved) {
        currentLang = saved;
    }

    // Load initial
    await changeLanguage(currentLang);

    // Bind Selector
    const selector = document.getElementById('langSelector');
    if (selector) {
        selector.value = currentLang;
        selector.onchange = (e) => changeLanguage(e.target.value);
    }
}

export async function changeLanguage(lang) {
    try {
        const response = await fetch(`/lang/${lang}`);
        if (!response.ok) throw new Error('Lang load failed');

        const data = await response.json();
        translations = data;
        currentLang = lang;
        localStorage.setItem('app_lang', lang);

        applyTranslations();
        document.documentElement.lang = lang;

    } catch (e) {
        console.error("i18n error", e);
    }
}

function applyTranslations() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[key]) {
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                el.placeholder = translations[key];
            } else {
                el.textContent = translations[key];
            }
        }
    });
}

export function t(key) {
    return translations[key] || key;
}

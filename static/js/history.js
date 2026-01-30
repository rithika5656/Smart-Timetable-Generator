/**
 * History Management Logic.
 */
import { t } from './i18n.js';
import { displayTimetable } from './ui.js';

export async function fetchHistory() {
    try {
        const response = await fetch('/history');
        const data = await response.json();
        renderHistory(data);
    } catch (e) {
        console.error("History error", e);
    }
}

function renderHistory(history) {
    const container = document.getElementById('historyList');
    if (!container) return;

    container.innerHTML = '';

    if (history.length === 0) {
        container.innerHTML = '<p class="text-center text-muted">No history yet.</p>';
        return;
    }

    history.forEach(entry => {
        const item = document.createElement('div');
        item.className = 'history-item';
        item.innerHTML = `
            <div>
                <strong>${new Date(entry.timestamp).toLocaleString()}</strong>
                <span>${entry.subjects} Subs, ${entry.teachers} Teachers</span>
            </div>
            <span class="badge ${entry.status === 'success' ? 'bg-success' : 'bg-danger'}">
                ${entry.status}
            </span>
        `;
        container.appendChild(item);
    });
}

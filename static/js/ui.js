import { showToast } from './toast.js';
import { t, initI18n } from './i18n.js';
import { fetchHistory } from './history.js';
import { initTheme } from './theme.js';

/**
 * UI Manipulation layer.
 */

// Init
document.addEventListener('DOMContentLoaded', () => {
    initI18n();
    initTheme();

    // History Toggle
    const historyBtn = document.getElementById('historyBtn');
    if (historyBtn) {
        historyBtn.onclick = () => {
            const panel = document.getElementById('historyPanel');
            panel.classList.toggle('show');
            if (panel.classList.contains('show')) {
                fetchHistory();
            }
        };
    }
});

/**
 * Show loading spinner.
 * @param {HTMLElement} loadingDiv 
 * @param {HTMLButtonElement} btn 
 */
export function showLoading(loadingDiv, btn) {
    loadingDiv.classList.add('show');
    loadingDiv.querySelector('p').textContent = t('msg_generating');
    if (btn) btn.disabled = true;
}

export function hideLoading(loadingDiv, btn) {
    loadingDiv.classList.remove('show');
    if (btn) btn.disabled = false;
}

export function showError(element, message) {
    showToast(message || t('msg_error'), 'error');
}

export function clearError(element) {
    element.style.display = 'none';
}

export function displayTimetable(data, containerId) {
    const { timetable, time_slots, days, subject_teacher_map } = data;
    const tableHead = document.getElementById('tableHead');
    const tableBody = document.getElementById('tableBody');
    const teacherList = document.getElementById('teacherList');
    const container = document.getElementById(containerId);

    // Violations
    if (data.meta && data.meta.violations && data.meta.violations.length > 0) {
        let warnHtml = '<div class="alert alert-warning"><strong>⚠️ Constraint Violations:</strong><ul>';
        data.meta.violations.forEach(v => warnHtml += `<li>${v}</li>`);
        warnHtml += '</ul></div>';
        // Prepend to container
        const existingAlert = container.querySelector('.alert-warning');
        if (existingAlert) existingAlert.remove();
        container.insertAdjacentHTML('afterbegin', warnHtml);
    }

    // Build Header
    let headerHtml = `<tr><th>${t('col_time')}</th>`;
    days.forEach(day => headerHtml += `<th>${day}</th>`);
    headerHtml += '</tr>';
    tableHead.innerHTML = headerHtml;

    // Build Body
    let bodyHtml = '';
    time_slots.forEach((slot, i) => {
        // Strip out the "Period X" prefix for cleaner display if it exists in a specific format
        // But our scheduler returns "Period 1 (9:00 AM)", which is fine.
        bodyHtml += `<tr><td><strong>${slot}</strong></td>`;

        days.forEach(day => {
            // Find the session for this period index
            // The JSON structure is list of objects {period, subject, teacher}
            const sessions = timetable[day];
            const session = sessions.find(s => s.period === i + 1);

            if (session) {
                if (session.type === 'Break') {
                    bodyHtml += `<td class="break-slot">☕ Break</td>`;
                } else {
                    bodyHtml += `
                        <td>
                            <div class="class-slot">
                                <div class="subject-name">${session.subject}</div>
                                <div class="teacher-name">${session.teacher}</div>
                            </div>
                        </td>
                    `;
                }
            } else {
                bodyHtml += '<td>-</td>';
            }
        });

        bodyHtml += '</tr>';
    });
    tableBody.innerHTML = bodyHtml;

    // Build Teacher Grid
    let teacherHtml = '<div class="teacher-grid">';
    const stats = data.meta && data.meta.teacher_load ? data.meta.teacher_load : {};

    for (const [subject, teacher] of Object.entries(subject_teacher_map)) {
        const load = stats[teacher] || 0;
        teacherHtml += `
            <div class="teacher-item">
                <div>
                    <strong>${subject}</strong>
                    <span>${teacher}</span>
                </div>
                <div style="margin-left: 10px; background: #e0e7ff; color: #4338ca; padding: 2px 8px; border-radius: 10px; font-size: 0.8em;">
                    ${load} classes
                </div>
            </div>`;
    }
    teacherHtml += '</div>';
    teacherList.innerHTML = teacherHtml;

    // Show and Scroll
    container.classList.add('show');

    // Action Buttons Container
    let actionsDiv = document.getElementById('actionsDiv');
    if (!actionsDiv) {
        actionsDiv = document.createElement('div');
        actionsDiv.id = 'actionsDiv';
        actionsDiv.style.display = 'flex';
        actionsDiv.style.gap = '10px';
        actionsDiv.style.marginTop = '20px';
        container.appendChild(actionsDiv);
    } else {
        actionsDiv.innerHTML = ''; // Clear previous buttons
    }

    // Export CSV
    actionsDiv.appendChild(createButton(t('btn_export'), () => downloadCSV(data.timetable)));

    // Print
    actionsDiv.appendChild(createButton(t('btn_print'), () => window.print()));

    // Copy JSON
    actionsDiv.appendChild(createButton(t('btn_copy'), () => {
        navigator.clipboard.writeText(JSON.stringify(data.timetable, null, 2));
        showToast(t('msg_copied'), 'success');
    }));

    setTimeout(() => {
        container.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

function createButton(text, onClick) {
    const btn = document.createElement('button');
    btn.className = 'btn';
    btn.innerHTML = text;
    btn.onclick = onClick;
    return btn;
}

async function downloadCSV(timetable) {
    try {
        const response = await fetch('/export', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ timetable })
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'timetable.csv';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    } catch (e) {
        console.error('Export failed', e);
    }
}

/**
 * UI Manipulation layer.
 */

export function showLoading(loadingDiv, btn) {
    loadingDiv.classList.add('show');
    if (btn) btn.disabled = true;
}

export function hideLoading(loadingDiv, btn) {
    loadingDiv.classList.remove('show');
    if (btn) btn.disabled = false;
}

export function showError(element, message) {
    element.textContent = message;
    element.style.display = 'block';

    // Shake animation
    element.style.animation = 'none';
    element.offsetHeight; // Trigger reflow
    element.style.animation = 'shake 0.5s ease-in-out';
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

    // Build Header
    let headerHtml = '<tr><th>Time</th>';
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
                bodyHtml += `
                    <td>
                        <div class="class-slot">
                            <div class="subject-name">${session.subject}</div>
                            <div class="teacher-name">${session.teacher}</div>
                        </div>
                    </td>
                `;
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

    // Add Export Button if not exists
    let exportBtn = document.getElementById('exportBtn');
    if (!exportBtn) {
        exportBtn = document.createElement('button');
        exportBtn.id = 'exportBtn';
        exportBtn.className = 'btn';
        exportBtn.style.marginTop = '20px';
        exportBtn.innerHTML = '📥 Export CSV';
        exportBtn.onclick = () => downloadCSV(data.timetable);
        container.appendChild(exportBtn);
    }

    setTimeout(() => {
        container.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
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

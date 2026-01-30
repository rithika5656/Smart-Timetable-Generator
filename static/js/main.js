import { generateTimetable } from './api.js';
import { displayTimetable, showError, clearError, showLoading, hideLoading } from './ui.js';

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('timetableForm');

    if (form) {
        form.addEventListener('submit', handleFormSubmit);

        // Reset Handler
        const resetBtn = document.createElement('button');
        resetBtn.type = 'button';
        resetBtn.className = 'btn';
        resetBtn.style.background = '#6b7280';
        resetBtn.style.marginLeft = '10px';
        resetBtn.textContent = 'Reset';
        resetBtn.onclick = () => {
            form.reset();
            document.getElementById('timetableContainer').classList.remove('show');
            import('./toast.js').then(m => m.showToast('Form reset', 'info'));
        };
        form.querySelector('button[type="submit"]').parentNode.appendChild(resetBtn);
    }
});

async function handleFormSubmit(e) {
    e.preventDefault();

    // Elements
    const elements = {
        subjects: document.getElementById('subjects'),
        teachers: document.getElementById('teachers'),
        periods: document.getElementById('periods'),
        errorDiv: document.getElementById('errorMessage'),
        loadingDiv: document.getElementById('loading'),
        tableContainer: document.getElementById('timetableContainer'),
        btn: document.getElementById('generateBtn')
    };

    // Reset State
    clearError(elements.errorDiv);
    elements.tableContainer.classList.remove('show');
    showLoading(elements.loadingDiv, elements.btn);

    try {
        const payload = {
            subjects: elements.subjects.value,
            teachers: elements.teachers.value,
            periods_per_day: elements.periods.value
        };

        const data = await generateTimetable(payload);
        displayTimetable(data, 'timetableContainer');

    } catch (error) {
        showError(elements.errorDiv, error.message);
    } finally {
        hideLoading(elements.loadingDiv, elements.btn);
    }
}

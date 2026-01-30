document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('timetableForm');
    
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
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
    elements.errorDiv.style.display = 'none';
    elements.tableContainer.classList.remove('show');
    elements.loadingDiv.classList.add('show');
    elements.btn.disabled = true;
    
    try {
        const payload = {
            subjects: elements.subjects.value,
            teachers: elements.teachers.value,
            periods_per_day: elements.periods.value
        };

        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to generate timetable');
        }
        
        displayTimetable(data);
        
    } catch (error) {
        showError(elements.errorDiv, error.message);
    } finally {
        elements.loadingDiv.classList.remove('show');
        elements.btn.disabled = false;
    }
}

function displayTimetable(data) {
    const { timetable, time_slots, days, subject_teacher_map } = data;
    const tableHead = document.getElementById('tableHead');
    const tableBody = document.getElementById('tableBody');
    const teacherList = document.getElementById('teacherList');
    const container = document.getElementById('timetableContainer');
    
    // Build Header
    let headerHtml = '<tr><th>Time</th>';
    days.forEach(day => headerHtml += `<th>${day}</th>`);
    headerHtml += '</tr>';
    tableHead.innerHTML = headerHtml;
    
    // Build Body
    let bodyHtml = '';
    time_slots.forEach((slot, i) => {
        bodyHtml += `<tr><td><strong>${slot}</strong></td>`;
        
        days.forEach(day => {
            const classInfo = timetable[day][i];
            bodyHtml += `
                <td>
                    <div class="class-slot">
                        <div class="subject-name">${classInfo.subject}</div>
                        <div class="teacher-name">${classInfo.teacher}</div>
                    </div>
                </td>
            `;
        });
        
        bodyHtml += '</tr>';
    });
    tableBody.innerHTML = bodyHtml;
    
    // Build Teacher Grid
    let teacherHtml = '<div class="teacher-grid">';
    for (const [subject, teacher] of Object.entries(subject_teacher_map)) {
        teacherHtml += `
            <div class="teacher-item">
                <strong>${subject}</strong>
                <span>${teacher}</span>
            </div>`;
    }
    teacherHtml += '</div>';
    teacherList.innerHTML = teacherHtml;
    
    // Show and Scroll
    container.classList.add('show');
    
    setTimeout(() => {
        container.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

function showError(element, message) {
    element.textContent = message;
    element.style.display = 'block';
    
    // Shake animation
    element.style.animation = 'none';
    element.offsetHeight; // Trigger reflow
    element.style.animation = 'shake 0.5s ease-in-out';
}

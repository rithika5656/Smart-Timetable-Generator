/**
 * API interaction layer.
 */

export async function generateTimetable(payload) {
    const response = await fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });

    if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || 'Failed to generate timetable');
    }

    return await response.json();
}

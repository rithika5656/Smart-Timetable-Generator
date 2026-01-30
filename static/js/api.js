/**
 * API interaction layer.
 */

/**
 * Generate a new timetable.
 * @param {Object} payload - The generation request parameters.
 * @returns {Promise<Object>} The generated timetable result.
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

/**
 * Toast notification system.
 */

export function showToast(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.style.position = 'fixed';
        container.style.bottom = '20px';
        container.style.right = '20px';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    // Style (fallback if css missing)
    toast.style.padding = '12px 24px';
    toast.style.marginBottom = '10px';
    toast.style.borderRadius = '8px';
    toast.style.color = 'white';
    toast.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
    toast.style.animation = 'slideIn 0.3s ease-out';

    if (type === 'error') toast.style.backgroundColor = '#ef4444';
    else if (type === 'success') toast.style.backgroundColor = '#10b981';
    else toast.style.backgroundColor = '#3b82f6';

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(20px)';
        toast.style.transition = 'all 0.3s ease-in';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

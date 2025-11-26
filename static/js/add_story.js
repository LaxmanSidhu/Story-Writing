const API_BASE = `${window.location.origin}/api`;

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('add-story-form');
    form.addEventListener('submit', handleSubmit);
});

async function handleSubmit(event) {
    event.preventDefault();
    const form = event.target;
    const messageDiv = document.getElementById('add-message');
    const formData = new FormData(form);

    setMessage(messageDiv, 'Publishing your story...', 'success-message');

    try {
        const response = await fetch(`${API_BASE}/stories`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.error || 'Unable to publish story');
        }

        form.reset();
        setMessage(messageDiv, 'Story published successfully! 🎉', 'success-message');
    } catch (error) {
        console.error(error);
        setMessage(messageDiv, error.message, 'error-message');
    }
}

function setMessage(target, message, className) {
    target.innerHTML = `<div class="${className}">${message}</div>`;
}


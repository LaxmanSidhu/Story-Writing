const API_BASE = `${window.location.origin}/api`;
let adminCredentials = null;

document.addEventListener('DOMContentLoaded', () => {
    adminCredentials = JSON.parse(sessionStorage.getItem('adminCredentials') || 'null');

    document.getElementById('admin-login-form').addEventListener('submit', handleLogin);
    document.getElementById('logout-btn').addEventListener('click', logout);

    if (adminCredentials) {
        togglePanels(true);
        loadStories();
    }
});

async function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('admin_username').value.trim();
    const password = document.getElementById('admin_password').value;
    const messageDiv = document.getElementById('admin-message');
    messageDiv.innerHTML = '';

    try {
        const response = await fetch(`${API_BASE}/admin/verify`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();
        if (!response.ok || !data.valid) {
            throw new Error('Invalid credentials');
        }

        adminCredentials = { username, password };
        sessionStorage.setItem('adminCredentials', JSON.stringify(adminCredentials));
        togglePanels(true);
        setMessage(messageDiv, 'Login successful.', 'success-message');
        loadStories();
    } catch (error) {
        console.error(error);
        setMessage(messageDiv, error.message, 'error-message');
    }
}

async function loadStories() {
    const container = document.getElementById('admin-stories');
    container.innerHTML = '<p class="placeholder">Loading stories...</p>';

    try {
        const response = await fetch(`${API_BASE}/stories`);
        if (!response.ok) throw new Error('Failed to fetch stories');
        const stories = await response.json();

        if (!stories.length) {
            container.innerHTML = '<p class="placeholder">No stories submitted yet.</p>';
            return;
        }

        container.innerHTML = '';
        stories.forEach((story) => {
            const article = document.createElement('article');
            article.innerHTML = `
                <p class="story-meta">By ${escapeHtml(story.author_name)} • ${formatDate(story.created_at)}</p>
                <h3>${escapeHtml(story.title)}</h3>
                <p>${escapeHtml(story.description)}</p>
                <div class="actions">
                    <button type="button" data-id="${story.id}">🗑 Delete</button>
                </div>
            `;
            article.querySelector('button').addEventListener('click', () => deleteStory(story.id));
            container.appendChild(article);
        });
    } catch (error) {
        console.error(error);
        container.innerHTML = '<p class="placeholder">Unable to load stories right now.</p>';
    }
}

async function deleteStory(storyId) {
    if (!adminCredentials) return;
    const confirmed = window.confirm('Delete this story permanently?');
    if (!confirmed) return;

    try {
        const response = await fetch(`${API_BASE}/stories/${storyId}`, {
            method: 'DELETE',
            headers: {
                'X-Admin-Username': adminCredentials.username,
                'X-Admin-Password': adminCredentials.password,
            },
        });

        if (!response.ok) {
            throw new Error('Unable to delete story');
        }

        loadStories();
    } catch (error) {
        console.error(error);
        alert(error.message);
    }
}

function logout() {
    adminCredentials = null;
    sessionStorage.removeItem('adminCredentials');
    togglePanels(false);
    document.getElementById('admin-login-form').reset();
    document.getElementById('admin-message').innerHTML = '';
    document.getElementById('admin-stories').innerHTML = '<p class="placeholder">No stories to show.</p>';
}

function togglePanels(isLoggedIn) {
    document.getElementById('admin-login').classList.toggle('hidden', isLoggedIn);
    document.getElementById('admin-panel').classList.toggle('hidden', !isLoggedIn);
}

function setMessage(target, message, className) {
    target.innerHTML = `<div class="${className}">${message}</div>`;
}

function formatDate(date) {
    return new Date(date).toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    });
}

function escapeHtml(text = '') {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}


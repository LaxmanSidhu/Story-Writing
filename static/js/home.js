const API_BASE = `${window.location.origin}/api`;
let cachedStories = [];

document.addEventListener('DOMContentLoaded', () => {
    loadStories();

    const modal = document.getElementById('story-modal');
    modal.querySelector('.close-modal').addEventListener('click', closeModal);
    modal.addEventListener('click', (event) => {
        if (event.target === modal) closeModal();
    });
});

async function loadStories() {
    const container = document.getElementById('stories-container');
    setLoading(container, 'Loading stories...');

    try {
        const response = await fetch(`${API_BASE}/stories`);
        if (!response.ok) throw new Error('Failed to load stories');
        const stories = await response.json();
        cachedStories = stories;

        document.getElementById('story-count').textContent = `${stories.length}+`;

        if (!stories.length) {
            setLoading(container, 'No stories yet. Be the first to share!');
            return;
        }

        renderStories(stories, container);
    } catch (error) {
        console.error(error);
        setLoading(container, 'Something went wrong. Please refresh.');
    }
}

function renderStories(stories, container) {
    container.innerHTML = '';
    const template = document.getElementById('story-card-template');

    stories.forEach((story) => {
        const clone = template.content.cloneNode(true);
        const card = clone.querySelector('.story-card');
        const image = clone.querySelector('.story-image');
        const title = clone.querySelector('h3');
        const meta = clone.querySelector('.story-meta');
        const description = clone.querySelector('.story-description');
        const readMoreBtn = clone.querySelector('.read-more');

        if (story.photo_url) {
            const img = document.createElement('img');
            img.src = story.photo_url;
            img.alt = story.title;
            img.className = 'story-image';
            image.replaceWith(img);
        } else {
            image.textContent = story.title.slice(0, 1).toUpperCase();
        }

        title.textContent = story.title;
        meta.textContent = `By ${story.author_name} • ${formatDate(story.created_at)}`;
        description.textContent = story.description;
        readMoreBtn.addEventListener('click', () => showFullStory(story.id));

        container.appendChild(clone);
    });
}

function showFullStory(storyId) {
    const modal = document.getElementById('story-modal');
    const modalContent = document.getElementById('modal-story-content');
    const story = cachedStories.find((item) => item.id === storyId);
    if (!story) return;

    modalContent.innerHTML = `
        ${story.photo_url ? `<img src="${story.photo_url}" alt="${escapeHtml(story.title)}">` : ''}
        <h2>${escapeHtml(story.title)}</h2>
        <p class="story-meta">By ${escapeHtml(story.author_name)} • ${formatDate(story.created_at)}</p>
        <p style="white-space: pre-wrap;">${escapeHtml(story.content)}</p>
    `;

    modal.classList.add('open');
}

function closeModal() {
    document.getElementById('story-modal').classList.remove('open');
}

function setLoading(container, message) {
    container.innerHTML = `
        <div class="loading-panel">
            <div class="spinner"></div>
            <p>${message}</p>
        </div>
    `;
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


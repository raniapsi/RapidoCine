(function () {
  const apiBase = window.API_URL || 'http://localhost:8000/api';

  function createStar(index, currentValue) {
    const star = document.createElement('button');
    star.type = 'button';
    star.className = 'star';
    star.setAttribute('role', 'radio');
    star.setAttribute('aria-checked', String(currentValue === index));
    star.setAttribute('aria-label', `${index} étoile${index > 1 ? 's' : ''}`);
    star.dataset.value = String(index);
    star.textContent = (currentValue || 0) >= index ? '★' : '☆';
    // Make sure the star is clearly interactive
    star.style.cursor = 'pointer';
    return star;
  }

  function attachStarListeners(container, movieId, ratingTextEl, avgEl) {
    const stars = container.querySelectorAll('.star');
    stars.forEach((btn) => {
      const handler = async (e) => {
        e.preventDefault();
        e.stopPropagation();
        const value = Number(btn.dataset.value);

        // Optimistic update
        renderStars(container, value);
        attachStarListeners(container, movieId, ratingTextEl, avgEl);
        updateText(ratingTextEl, avgEl, value, null, null);

        const data = await submitRating(movieId, value);
        if (data.error) {
          updateText(ratingTextEl, avgEl, null, data.average, data.count, data.error);
          return;
        }
        renderStars(container, data.user_rating || value);
        attachStarListeners(container, movieId, ratingTextEl, avgEl);
        updateText(ratingTextEl, avgEl, data.user_rating || value, data.average, data.count);
      };

      btn.addEventListener('click', handler);
      btn.addEventListener('touchstart', handler, { passive: false });
    });
  }

  function renderStars(container, value) {
    if (!container) return;
    container.innerHTML = '';
    for (let i = 1; i <= 5; i++) {
      const star = createStar(i, value || 0);
      container.appendChild(star);
    }
  }

  async function fetchRating(movieId) {
    try {
      const res = await fetch(`${apiBase}/movies/${movieId}/rating`, { credentials: 'include' });
      if (!res.ok) throw new Error(`fetch rating failed: ${res.status}`);
      return await res.json(); // { average, user_rating, count }
    } catch (e) {
      console.debug('Rating fetch failed, continuing with empty state:', e);
      return { average: null, user_rating: null, count: 0 };
    }
  }

  async function submitRating(movieId, value) {
    try {
      const res = await fetch(`${apiBase}/movies/${movieId}/rating`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ rating: value }),
      });
      if (res.status === 401) {
        // Not authenticated: guide user to login instead of failing silently
        return { average: null, user_rating: null, count: null, error: 'unauthenticated' };
      }
      if (!res.ok) throw new Error(`submit rating failed: ${res.status}`);
      return await res.json(); // { average, user_rating, count }
    } catch (e) {
      console.warn('Rating submit failed:', e);
      return { average: null, user_rating: null, count: null, error: 'network' };
    }
  }

  function updateText(ratingTextEl, avgEl, userRating, average, count, error) {
    if (ratingTextEl) {
      if (error === 'unauthenticated') {
        ratingTextEl.textContent = 'Connectez-vous pour noter ce film';
      } else {
        ratingTextEl.textContent =
          userRating ? `Votre note : ${userRating}/5` : 'Votre note : —';
      }
    }
    if (avgEl) {
      avgEl.textContent =
        average != null ? `Note moyenne : ${Number(average).toFixed(2)}${count != null ? ` (${count})` : ''}` : 'Note moyenne : —';
    }
  }

  function attachHandlers(container, movieId, ratingTextEl, avgEl) {
    // Keep delegation as a fallback if per-star listeners are removed
    container.addEventListener('click', async (e) => {
      const btn = e.target.closest('.star');
      if (!btn) return;
      const value = Number(btn.dataset.value);

      renderStars(container, value);
      attachStarListeners(container, movieId, ratingTextEl, avgEl);
      updateText(ratingTextEl, avgEl, value, null, null);

      const data = await submitRating(movieId, value);
      if (data.error) {
        updateText(ratingTextEl, avgEl, null, data.average, data.count, data.error);
        return;
      }
      renderStars(container, data.user_rating || value);
      attachStarListeners(container, movieId, ratingTextEl, avgEl);
      updateText(ratingTextEl, avgEl, data.user_rating || value, data.average, data.count);
    });

    container.addEventListener('keydown', async (e) => {
      const checkedEl = container.querySelector('[aria-checked="true"]');
      const current = Number(checkedEl?.dataset.value || 0);
      if (e.key === 'ArrowRight' || e.key === 'ArrowUp') {
        e.preventDefault();
        const next = Math.min(5, (current || 0) + 1);
        renderStars(container, next);
        attachStarListeners(container, movieId, ratingTextEl, avgEl);
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') {
        e.preventDefault();
        const prev = Math.max(1, (current || 1) - 1);
        renderStars(container, prev);
        attachStarListeners(container, movieId, ratingTextEl, avgEl);
      } else if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        const value = Number(container.querySelector('[aria-checked="true"]')?.dataset.value || 0);
        if (!value) return;

        renderStars(container, value);
        attachStarListeners(container, movieId, ratingTextEl, avgEl);
        updateText(ratingTextEl, avgEl, value, null, null);

        const data = await submitRating(movieId, value);
        if (data.error) {
          updateText(ratingTextEl, avgEl, null, data.average, data.count, data.error);
          return;
        }
        renderStars(container, data.user_rating || value);
        attachStarListeners(container, movieId, ratingTextEl, avgEl);
        updateText(ratingTextEl, avgEl, data.user_rating || value, data.average, data.count);
      }
    });

    container.addEventListener('focusin', () => {
      const selected = container.querySelector('[aria-checked="true"]');
      if (!selected) {
        const first = container.querySelector('.star');
        if (first) first.setAttribute('aria-checked', 'true');
      }
    });
  }

  async function initOne(movieId) {
    const container = document.getElementById(`stars-${movieId}`) ||
                      document.querySelector(`#rating-container-${movieId} .stars`);
    const ratingTextEl = document.getElementById(`rating-text-${movieId}`);
    const avgEl = document.getElementById(`rating-avg-${movieId}`);
    if (!container) {
      console.warn('Stars container not found for movie:', movieId);
      return;
    }

    container.setAttribute('role', 'radiogroup');
    container.setAttribute('tabindex', '0');

    const data = await fetchRating(movieId);
    renderStars(container, data.user_rating || 0);
    attachStarListeners(container, movieId, ratingTextEl, avgEl);
    updateText(ratingTextEl, avgEl, data.user_rating, data.average, data.count);
    attachHandlers(container, movieId, ratingTextEl, avgEl);
  }

  function initAll() {
    const ratingBlocks = document.querySelectorAll('[id^="rating-container-"]');
    if (!ratingBlocks.length) {
      console.warn('No rating blocks found in DOM');
      return;
    }
    ratingBlocks.forEach((block) => {
      const movieId = block.dataset.movieId;
      if (movieId) initOne(movieId);
    });
  }

  window.__ratingInit = initAll;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }
})();
